# -*- coding: utf-8 -*-
"""O REGISTRO da custódia nas superfícies de memória — C2 (inscrição ACOM), C13 (diário do site, memórias da sessão, Atlas, MEMORY.md, rota),
C16 («PUBLICADA») e C17 (transições ACOM t1..t3). Generaliza `registro_vNNN.py`, `registro_vNNN_publicada.py`, `acom_*` — e conserta o que
a ESPEC achou neles:

  L2  o registro NÃO era idempotente (`ap()` acrescentava sempre; a troca do MEMORY.md casava o prefixo que a linha nova também tem):
      agora cada apêndice leva uma SENTINELA `<!-- custodia:vN:<bloco> -->` e a troca da linha só ocorre se ela ainda não diz
      CUSTODIADO/PUBLICADA;
  L3  números do console entravam no texto sem recibo: agora vêm dos recibos de passo (runs\\), dos arquivos e do git;
  L19 `tocar()` lia, alterava e substituía o arquivo inteiro (o Atlas tem 8,6 MB) e uma escrita alheia no meio se perdia em silêncio:
      agora há CAS por (tamanho, mtime) antes do `os.replace`, com releitura e refação;
  L7  o t1 do ACOM foi gravado depois do commit e ainda dizia «falta commit»: cada transição é gerada do estado REAL dos recibos.
Backup de BYTES antes de tocar (regra de 22/08/2026); correção AO LADO, nunca por cima; MEMORY.md < 24 KB (alarme a 90%, parada a 98%).

  L23 a FILA DA MEMÓRIA (26/10/2026, ordem do operador; memory\\fila\\README.md): só a gerência c1 escreve MEMORY.md, MEMORY_2.md e os
      arquivos-tópico do diretório da memória. C13/C16 DEPOSITAM (memoria.py depositar --quem claude-site), uma vez por sentinela; o
      «já aplicado» aceita o depósito ou a promoção (que leva a sentinela ao tópico). DIARIO_DO_SITE.md e o Atlas seguem como estavam."""
import glob
import hashlib
import json
import os
import re
import uuid
from datetime import datetime
from pathlib import Path

from . import patches, textos, util
from .motor import Passo, aplicado, falta, indeterminado
from .util import Parar, FalhaLeitura

TETO_MEMORY = 24 * 1024


# =================================================================== escrita segura com CAS e sentinela
def tocar_cas(p, f, pode_encolher=False, tentativas=3):
    """Lê, aplica `f(texto, nl) -> texto|None`, e substitui — se o arquivo NÃO mudou desde a leitura (tamanho, mtime); senão relê e refaz."""
    p = Path(p)
    for _ in range(tentativas):
        st0 = p.stat()
        raw = util.ler_bytes(p)
        nl = "\r\n" if b"\r\n" in raw else "\n"
        novo = f(raw.decode("utf-8"), nl)
        if novo is None:
            return {"estado": "ja_aplicado"}
        dados = novo.encode("utf-8")
        st1 = p.stat()
        if (st1.st_size, st1.st_mtime_ns) != (st0.st_size, st0.st_mtime_ns):
            continue                                           # alguém escreveu no meio: reler e refazer
        r = util.escrever_atomico(p, dados, backup=True, exigir_cresceu=not pode_encolher, pode_encolher=pode_encolher)
        r["estado"] = "aplicado"
        return r
    raise Parar("o arquivo mudou durante %d tentativas (concorrência): %s" % (tentativas, p.name))


def ap(p, texto, sentinela):
    """Apêndice datado, UMA vez (sentinela no fim do bloco). Devolve o estado."""
    def f(t, nl):
        if sentinela in t:
            return None
        return t.rstrip("\r\n") + nl + nl + (texto.strip("\n") + "\n" + sentinela).replace("\n", nl) + nl
    return tocar_cas(p, f)


def agora():
    return datetime.now().strftime("%d/%m/%Y %H:%M")


def sent(ctx, bloco):
    return "<!-- custodia:%s:%s -->" % (ctx.versao, bloco)


# =================================================================== a FILA DA MEMÓRIA (L23)
QUEM_FILA = "claude-site"


def _na_memoria(ctx, p):
    """O arquivo mora no diretório da memória (onde só a gerência c1 escreve)?"""
    return os.path.normcase(str(Path(p).parent)) == os.path.normcase(str(ctx.c.MEM))


def _depositos_com(ctx, sentinela):
    d = ctx.c.MEM / "fila" / "depositos" / QUEM_FILA
    return [x for x in sorted(d.glob("*.md")) if sentinela in util.ler_texto(x, "replace")] if d.is_dir() else []


def depositar(ctx, alvo, texto, sentinela, bloco):
    """Deposita UMA vez na fila (a sentinela vai no corpo): já depositado, ou já promovido (a sentinela no tópico), nada faz."""
    if _depositos_com(ctx, sentinela):
        return {"estado": "ja_depositado"}
    t = ctx.c.MEM / alvo
    if alvo.endswith(".md") and t.is_file() and sentinela in util.ler_texto(t, "replace"):
        return {"estado": "ja_aplicado"}
    slug = re.sub(r"[^a-z0-9_-]+", "-", ("custodia_%s_%s" % (ctx.versao, bloco)).lower()).strip("-")[:64]
    arq = ctx.W / "fila_da_memoria" / (slug + ".md")
    arq.parent.mkdir(parents=True, exist_ok=True)
    util.escrever_atomico(arq, (texto.strip("\n") + "\n" + sentinela + "\n").encode("utf-8"), backup=True)
    r = util.rodar([str(ctx.c.PYTHON), "-X", "utf8", str(ctx.c.MEM / "fila" / "memoria.py"), "depositar", "--quem", QUEM_FILA, "--tipo", "project",
                    "--estatuto", "REAL", "--alvo", alvo, "--fonte", str(ctx.handoff.caminho), "--texto-arquivo", str(arq), "--slug", slug])
    if r["rc"] != 0:
        raise Parar("memoria.py depositar recusou o depósito para %s" % alvo, r["saida"].strip().splitlines()[-4:])
    return {"estado": "depositado"}


def registrar_memoria(ctx, nome, texto, bloco):
    """Uma superfície do diretório da memória: deposita para a gerência (o tópico que ainda não existe vai como novo:<slug>)."""
    p = ctx.c.memoria(nome)
    alvo = nome if p.is_file() else "novo:" + nome[:-3]
    return depositar(ctx, alvo, texto, sent(ctx, bloco), bloco)


# =================================================================== os fatos verificados que entram no texto (cada um com recibo/arquivo/git)
def _esp(ctx):
    h, o = util.git(ctx.c.TB, "rev-parse", "--short", "HEAD"), util.git(ctx.c.TB, "rev-parse", "--short", "origin/main")
    if h != o:
        raise Parar("o espelho não está publicado (HEAD %s != origin/main %s): o registro vem depois do push" % (h, o))
    return h


def fatos_verificados(ctx):
    c, v = ctx.c, ctx.versao
    Fa = ctx.fatos
    V = c.cofre(v)
    man = util.ler_json(V / "CUSTODY_MANIFEST.json")
    man16 = util.sha16(V / "CUSTODY_MANIFEST.json")
    ctx.hashes.add(man16)
    km = util.ler_json(c.cofre_kernel(v) / "CUSTODY_MANIFEST.json")
    if km["formal_files"] != Fa["kernel"]["formais"] or km["declaracoes_no_axiom_report"] != Fa["kernel"]["declaracoes"] or km.get("fora_do_trio") != 0:
        raise Parar("o kernel do cofre diverge dos fatos")
    res = sorted(glob.glob(str(c.CEN / "fronteira_tgl" / "results" / "fronteira_*.json")), key=os.path.getmtime)[-1]
    rr = util.ler_json(res)
    vf = str(rr.get("verdict") or "")
    if not vf.startswith("FRONTEIRA_SINCRONIZADA_%s" % v.upper()) or rr["the_station"]["custodia_%s" % v]["pass"] is not True:
        raise Parar("o último resultado do runner não é FRONTEIRA_SINCRONIZADA_%s com a pedra aprovada" % v.upper())
    led = util.ler_json(c.CEN / "fronteira_tgl" / "ledger_de_pinos.json")
    if led.get("erros") != 0:
        raise Parar("ledger de pinos com erros: %s" % led.get("erros"))
    pats = sorted(glob.glob(str(c.CEN / "patents" / "BR*")))
    n_disp = 0
    for p in pats:
        rs = sorted(glob.glob(os.path.join(p, "results", "*", "results.json")), key=os.path.getmtime)
        if rs and ('"camada_%s_no_cofre"' % v) in Path(rs[-1]).read_text(encoding="utf-8", errors="replace"):
            n_disp += 1
    if n_disp != len(pats):
        raise Parar("camada %s em %d/%d dispositivos" % (v, n_disp, len(pats)))
    snaps = sorted(d for d in glob.glob(str(c.BKCEN / "Chatgpt_*")) if os.path.isfile(os.path.join(d, "MANIFEST.json")))
    sm = util.ler_json(os.path.join(snaps[-1], "MANIFEST.json")) if snaps else {}
    dia = (ctx.selo_nos.get("timestamp", "")[:10]).replace("-", "")
    if not (str(sm.get("snapshot", ""))[:8] >= dia and sm.get("conferido_contra_origem") is True):
        raise Parar("snapshot do Chatgpt\\ do dia do selo ausente ou não conferido")
    mapa = util.ler_json(c.ESP / "fontes_pinadas" / "MAPA_FONTES_PINADAS.json")
    c11, c9 = _recibo(ctx, "C11"), _recibo(ctx, "C9")
    return {"esp": _esp(ctx), "man16": man16, "man": man, "km": km, "veredito": vf, "runner_n": patches.runner_numeros(util.ler_eol(c.CEN / "fronteira_tgl" / "runner" / "one_fronteira.py")[0])[0], "ledger": led, "n_disp": n_disp, "n_dev": len(pats), "snap": os.path.basename(snaps[-1]), "sm": sm, "mapa": mapa,
            "final": (c11 or {}).get("ok"), "c9": (c9 or {}).get("ok")}


def _recibo(ctx, nome):
    from .central import _recibo_lido
    return _recibo_lido(ctx, nome)


def site_verificado(ctx):
    """«SUBIDA VERIFICADA» e «R1: PASSA», lidos dos relatórios — ou a frase honesta de que não foi verificado (nunca afirmar)."""
    from .site import _ja_e18, _ja_e19
    a, b = _ja_e18(ctx), _ja_e19(ctx)
    if a.estado == "APLICADO" and b.estado == "APLICADO":
        return "SITE no ar: SUBIDA VERIFICADA (%s); leitor de IA R1 passa (%s)." % (a.detalhe.split(":")[0], b.detalhe.split(":")[0])
    return "SITE: não verificado nesta rodada (%s; %s)." % (a.detalhe[:60], b.detalhe[:60])


def estado_central(ctx):
    """O texto das seis superfícies, em segmentos — cada um com a sua fonte (ESPEC_CENTRAL C13). Passa pelo portão antes de escrever."""
    c, v = ctx.c, ctx.versao
    Fa = ctx.fatos
    fv = fatos_verificados(ctx)
    o = ctx.ordem or textos.ordem_padrao(c)
    citacao, data_ordem = "", ""
    if o and o.is_file():
        citacao = o.read_text(encoding="utf-8").strip()
        d = textos._data_da_ordem(o)
        data_ordem = (" de %s/2026" % d) if d else ""
    hh = datetime.fromtimestamp(ctx.handoff.caminho.stat().st_mtime).strftime("%H:%M")
    mods = ", ".join("`%s`" % x for x in Fa["kernel"]["modulos_novos"]) or "nenhum"
    mapa = fv["mapa"]
    seg = []
    seg.append("Custódia %s (sessão %s da Central, pela regra do operador%s — «%s»; handoff `Nós\\HANDOFF_%s_CUSTODIA.md`, aparecido às %s; as três marcas conferidas)."
               % (v, ctx.sessao, data_ordem, citacao, v, hh))
    seg.append("ESPELHO the_boundary `%s` = origin/main: `um.py` %s `%s` (%s), os módulos novos %s, as fontes pinadas da %s (%d de %d no mapa), `recibos_bancada_%s/`, "
               "`diferencas_%s/`; ESTADO/LEDGER/CITATION/PORTAS/README regenerados com o PARÁGRAFO PRONTO do handoff; backup da %s fora do repo."
               % (fv["esp"], v, Fa["pin16"], Fa["escada"]["texto"], mods, v, mapa["n_publicadas"], mapa["n_fontes"], v, v, Fa["anterior"]))
    seg.append(site_verificado(ctx))
    final = ("%s FINAL regerados e rodados (rc 0 em %s/%d)" % (fv["final"], fv["final"], fv["n_dev"])) if fv["final"] else "%d FINAL regerados (o resultado da execução não tem recibo nesta rodada)" % fv["n_dev"]
    seg.append("CENTRAL: cofre `um_unificado_%s` (manifesto `%s`; %s artefatos, %s divergentes) + `tgl_kernel_%s` (%d formais / %d declarações); runner da Fronteira v%d `%s…` "
               "(a pedra genérica lê o cofre %s contra o %s pelo nome, dois céticos reprovam as injeções); camada %s dos %d dispositivos %d/%d; %s; ledger de pinos %s erros, %s avisos; "
               "snapshot `%s` (%s copiados, %s idênticos à base, 0 divergentes)."
               % (v, fv["man16"], fv["man"].get("n_artifacts"), fv["man"].get("mismatches"), v, fv["km"]["formal_files"], fv["km"]["declaracoes_no_axiom_report"], fv["runner_n"],
                  fv["veredito"][:60], v, Fa["anterior"], v, fv["n_dev"], fv["n_disp"], fv["n_dev"], final, fv["ledger"].get("erros"), fv["ledger"].get("avisos"), fv["snap"], fv["sm"].get("n_copiados"),
                  fv["sm"].get("n_identicos_a_base")))
    pend = ctx.handoff.secao("Pendências SÓ do operador")
    if pend:
        seg.append("DO OPERADOR (verbatim do handoff): " + re.sub(r"^\*\*[^*]+\*\*\s*", "", pend).replace("\n", " "))
    seg.append("PROVADA = validade; a creditação segue recusada; o gate não se moveu.")
    return " ".join(seg)


# =================================================================== C13 — registro nas superfícies
def _memory_ja(ctx, marcas):
    p = ctx.c.memoria("MEMORY.md")
    linhas = [l for l in util.ler_texto(p, "replace").splitlines() if l.startswith("- [HANDOFF %s " % ctx.versao)]
    return linhas[0] if linhas else None, any(m in (linhas[0] if linhas else "") for m in marcas)


def _superficies_c13(ctx):
    """As superfícies que C13 escreve (o que `_ap_c13` toca), com o bloco da sentinela de cada uma. A rota NÃO é daqui: entra em C16, depois do push e da conferência."""
    c, v = ctx.c, ctx.versao
    return [("DIARIO_DO_SITE.md", c.BANC / "DIARIO_DO_SITE.md", "diario_do_site"), ("site-sessao-estado.md", c.memoria("site-sessao-estado.md"), "site_sessao_estado"),
            ("tgl-fronteira-teorica.md", c.memoria("tgl-fronteira-teorica.md"), "fronteira_teorica"),
            ("central-de-patentes-estado.md", c.memoria("central-de-patentes-estado.md"), "central_estado"),
            ("dispositivos-formula-completa.md", c.memoria("dispositivos-formula-completa.md"), "dispositivos"),
            ("handoff-%s-custodia.md" % v, c.memoria("handoff-%s-custodia.md" % v), "handoff_custodiado")]


def _registrada_na_superficie(ctx, texto, bloco):
    """O apêndice da custódia está no texto: pela SENTINELA de G1 ou, nas versões registradas à mão (sem sentinela), pelo rastro «custódia … vN» ou por um
    título de seção («## … camada vN») que cita a versão."""
    v = ctx.versao
    if sent(ctx, bloco) in texto:
        return True
    return bool(re.search(r"cust[óo]dia[^\n]{0,240}\b%s\b|\b%s\b[^\n]{0,240}cust[óo]dia" % (v, v), texto, re.I) or re.search(r"^##[^\n]*\b%s\b" % v, texto, re.M))


def _ja_c13(ctx):
    """As 7 superfícies que C13 escreve (6 memórias/diários + Atlas) e a linha do MEMORY.md. A rota custodia.vN NÃO é de C13: registrá-la aqui diria «publicada e
    conferida» (REAL) antes do push da Central e da conferência final — ela entra em C16 (achado ALTA dos céticos)."""
    c, v = ctx.c, ctx.versao
    faltam = []
    if ("A CUSTÓDIA DA %s" % v) not in util.ler_texto(c.ATLAS, "replace"):
        faltam.append("Atlas «A CUSTÓDIA DA %s»" % v)
    for nome, p, bloco in _superficies_c13(ctx):
        if _na_memoria(ctx, p) and _depositos_com(ctx, sent(ctx, bloco)):
            continue                                           # depositada na fila: a promoção é da gerência c1 (L23)
        if not p.is_file():
            faltam.append("%s ausente" % nome)
        elif not _registrada_na_superficie(ctx, util.ler_texto(p, "replace"), bloco):
            faltam.append("%s sem o registro da custódia" % nome)
    lin, ok = _memory_ja(ctx, ("CUSTODIADO", "PUBLICADA"))
    if lin is None:
        faltam.append("linha «- [HANDOFF %s » no MEMORY.md" % v)
    elif not ok and not _depositos_com(ctx, sent(ctx, "indice:custodiado")):
        faltam.append("linha do MEMORY.md ainda sem CUSTODIADO/PUBLICADA (nem a troca depositada na fila)")
    return aplicado(("Atlas, as 6 memórias/diários (%s) e a linha do MEMORY.md" % ", ".join(n for n, _, _ in _superficies_c13(ctx)))[:150] + "; as do diretório da memória pela fila (L23)") if not faltam else falta("faltam: " + "; ".join(faltam))


def _pre_c13(ctx):
    f = []
    try:
        _esp(ctx)
    except Parar as e:
        f.append(e.motivo)
    from .central import _ja_c5
    if _ja_c5(ctx).estado == "INDETERMINADO":
        f.append("o snapshot ainda está em curso: espere o MANIFEST.json conferido (C5)")
    for rot, pth in (("handoff-%s-custodia.md" % ctx.versao, ctx.c.memoria("handoff-%s-custodia.md" % ctx.versao)),):
        if not pth.is_file():
            ctx.aviso("%s não existe: vai à fila como novo:%s (a gerência c1 cria o tópico)" % (rot, rot[:-3]))
    lin, _ = _memory_ja(ctx, ())
    if lin is None:
        f.append("a linha «- [HANDOFF %s » não existe no MEMORY.md (criada pela gerência c1 ao emitir o handoff)" % ctx.versao)
    return f


def _linha_nova_memory(ctx, antiga, rotulo, extra):
    corte = antiga.split(") \u2014 ")[0]
    titulo = (corte + ")") if corte != antiga else antiga.split(" \u2014 **")[0]
    return "%s \u2014 **%s: %s** (%s) \u00b7 `%s`" % (titulo, ctx.data[:5], rotulo, extra, ctx.pin16)


def trocar_linha_memory(ctx, marcas_ja, rotulo, extra, bloco_sentinela):
    p, p2 = ctx.c.memoria("MEMORY.md"), ctx.c.memoria("MEMORY_2.md")
    antiga, ok = _memory_ja(ctx, marcas_ja)
    if antiga is None:
        raise Parar("a linha «- [HANDOFF %s » não existe no MEMORY.md" % ctx.versao)
    if ok:
        return {"estado": "ja_aplicado"}
    nova = _linha_nova_memory(ctx, antiga, rotulo, extra)
    tam = len(util.ler_bytes(p)) - len(antiga.encode("utf-8")) + len(nova.encode("utf-8"))
    if tam > 0.98 * TETO_MEMORY:
        raise Parar("MEMORY.md passaria de 98%% do teto de 24 KB (%d B): mover linhas antigas para o MEMORY_2.md primeiro (regra dos dois arquivos, L14)" % tam)
    if tam > 0.90 * TETO_MEMORY:
        ctx.aviso("MEMORY.md a %.0f%% do teto de 24 KB" % (100.0 * tam / TETO_MEMORY))
    ap(p2, "## %s \u2014 linha movida do MEMORY.md (regra dos dois arquivos), VERBATIM\n\n%s" % (agora(), antiga), sent(ctx, "memory2:" + bloco_sentinela))
    return tocar_cas(p, lambda t, nl: t.replace(antiga, nova, 1), pode_encolher=True)


def propor_linha_memory(ctx, marcas_ja, rotulo, extra, bloco):
    """A troca da linha «- [HANDOFF vN » do índice, DEPOSITADA para a gerência c1 (L23): a antiga e a nova, verbatim; trocar e mover a antiga ao
    MEMORY_2.md (regra dos dois arquivos) é ato da gerência."""
    p = ctx.c.memoria("MEMORY.md")
    antiga, ok = _memory_ja(ctx, marcas_ja)
    if antiga is None:
        raise Parar("a linha «- [HANDOFF %s » não existe no MEMORY.md" % ctx.versao)
    if ok:
        return {"estado": "ja_aplicado"}
    nova = _linha_nova_memory(ctx, antiga, rotulo, extra)
    tam = len(util.ler_bytes(p)) - len(antiga.encode("utf-8")) + len(nova.encode("utf-8"))
    nota = ""
    if tam > 0.90 * TETO_MEMORY:
        nota = " Medido: com a troca, o MEMORY.md iria a %d B (%.0f%% do teto de 24 KB)." % (tam, 100.0 * tam / TETO_MEMORY)
        ctx.aviso("a troca depositada levaria o MEMORY.md a %.0f%% do teto de 24 KB" % (100.0 * tam / TETO_MEMORY))
    texto = ("Troca proposta da linha do índice da custódia %s (%s). Ato da gerência: substituir a linha ANTIGA pela NOVA e levar a antiga, VERBATIM, "
             "ao MEMORY_2.md (regra dos dois arquivos).%s\n\nANTIGA:\n%s\n\nNOVA:\n%s" % (ctx.versao, rotulo, nota, antiga, nova))
    return depositar(ctx, "MEMORY.md (linha de indice)", texto, sent(ctx, "indice:" + bloco), "indice_" + bloco)


def montar_rota(ctx, estado):
    c, v = ctx.c, ctx.versao
    Fa = ctx.fatos
    fv = fatos_verificados(ctx)
    bd = ctx.bloco_diario
    rota = {"tipo": "ROTA", "rota_id": "custodia.%s" % v, "dominio": "CUSTODIA",
            "titulo": "Custódia da %s (%s): espelho, frente, site, cofre %s, runner v%d, %d dispositivos, FINAL, ledger, snapshot — pela regra «custodiar quando o handoff aparecer»"
                      % (v, (bd.titulo_pt.capitalize() if bd else v), v, fv["runner_n"], fv["n_dev"]),
            "pergunta": "A %s (%s) pode ser custodiada por G1 (tools/custodiar.py), com cada artefato conferido por hash, os números lidos do core e do selo, os textos por molde e "
                        "blocos do handoff, e sem errata nas pedras antigas — a partir das três marcas, sem ordem nova do operador?" % (v, Fa["pin16"]),
            "dados": ["Nós (um.py %s, selo, core, artigos, rodada_%s_stdout, HANDOFF_%s com os parágrafos prontos)" % (v, v, v), "work/cadeia_de_selo/%s e %s_selo" % (v, v),
                      "as fontes pinadas que os registros v392 em diante releem por caminho absoluto"],
            "metodo": "tools/custodiar.py: vigiar (três marcas) -> sondar (fatos esquema 2) -> planejar -> executar, com marca de «já aplicado» em cada passo, gates que PARAM, "
                      "recibos em work/custodia_G1/runs e ato para fora só com --publicar. Perna 1: passo zero, cópia ao espelho por pares calculados, geradores por molde, laço "
                      "portas/README até o ponto fixo, subida com conjunto esperado, leitor de IA. Perna 2: cofre (L1 consertado), pedra e camada genéricas, os dispositivos, FINAL, ledger.",
            "resultado": estado, "veredito": "CUSTODIA_%s_PUBLICADA_POR_G1__SEM_ERRATA_NAS_PEDRAS_ANTIGAS__GATE_INALTERADO" % v.upper(), "estatuto": "REAL", "status": "EXAMINADA",
            "olhou_dados": False,
            "defeito": ("; ".join(ctx.avisos) if ctx.avisos else "nenhum defeito de esteira medido nesta rodada"),
            "nao_refazer": "A custódia %s está publicada e conferida. A próxima sai de tools/custodiar.py com a mesma ordem." % v,
            "proximo_passo": "Na v%d: custodiar.py vigiar; os nomes provisórios dos registros e a paridade [LEGAL] do ACOM Mirror são decisões do operador." % (ctx.n + 1),
            "onde": str(ctx.W),
            "artefatos": [str(c.cofre(v) / "CUSTODY_MANIFEST.json"), str(c.cofre_kernel(v) / "CUSTODY_MANIFEST.json"), str(c.CEN / "fronteira_tgl" / "runner" / "one_fronteira.py"),
                          str(c.CEN / "patents" / "_formula_completa" / "tgl_formula_completa.py"), str(c.BANC / "revisoes" / ("custodia_%s_espelho.json" % v)),
                          str(ctx.W / ("fatos_%s.json" % v))],
            "refs": ["custodia.%s" % Fa["anterior"], "iald.organismo.torre_de_comando_23out"], "nota": "Sessão %s da Central (G1), %s." % (ctx.sessao, ctx.data)}
    for k, x in rota.items():
        if isinstance(x, str) and "CONFIRM" in x.upper():
            raise Parar("campo de rota %r contém a substring CONFIRM" % k)
    return rota


def _ap_c13(ctx):
    c, v = ctx.c, ctx.versao
    Fa = ctx.fatos
    estado = estado_central(ctx)
    viol = textos.portao(estado, textos.conhecidos_da_rodada(ctx), rotulo="registro")
    if viol:
        raise Parar("o portão de texto reprovou o registro", viol)
    when = agora()
    saidas = {}
    saidas["DIARIO_DO_SITE"] = ap(c.BANC / "DIARIO_DO_SITE.md", "## %s \u2014 a custódia da %s (sessão %s da Central)\n\n%s" % (when, v, ctx.sessao, estado), sent(ctx, "diario_do_site"))
    saidas["site-sessao-estado"] = registrar_memoria(ctx, "site-sessao-estado.md", "## %s \u2014 %s no ar\n\n%s" % (when, v, estado), "site_sessao_estado")
    fv = fatos_verificados(ctx)
    saidas["tgl-fronteira-teorica"] = registrar_memoria(ctx, "tgl-fronteira-teorica.md",
        "## %s \u2014 runner v%d (%s)\n\nVeredito `%s…`. A pedra genérica `_medir_%s_custodia` (G1) lê o cofre %s contra o %s PELO NOME, com as expectativas congeladas em FATOS_CUSTODIA.json "
        "do cofre; %d blocos novos verificados sem efeito no gate, %d bandeiras, registro %d com os %d da %s e %d vereditos mudados (só dígitos e pino), kernel %d/%d; dois céticos reprovam. "
        "NENHUMA errata nas pedras antigas." % (when, fv["runner_n"], v, fv["veredito"][:90], v, v, Fa["anterior"], len(Fa["registros_novos"]), len(Fa["bandeiras_novas"]),
                                                  Fa["registro"]["pt"], Fa["registro"]["anterior"], Fa["anterior"], len(Fa["registro"]["mudados"]), Fa["kernel"]["formais"], Fa["kernel"]["declaracoes"]),
        "fronteira_teorica")
    saidas["central-de-patentes-estado"] = registrar_memoria(ctx, "central-de-patentes-estado.md", "## %s \u2014 custódia %s\n\n%s" % (when, v, estado), "central_estado")
    saidas["dispositivos-formula-completa"] = registrar_memoria(ctx, "dispositivos-formula-completa.md",
        "## %s \u2014 camada %s\n\nOs registros novos da %s (%s) lidos e conferidos no cofre, sem interpretação, contra o FATOS_CUSTODIA.json; a escada %s. %d/%d com a camada; %s FINAL "
        "regerados. Nada muda número de dispositivo." % (when, v, v, ", ".join(Fa["registros_novos"]), Fa["escada"]["texto"], fv["n_disp"], fv["n_dev"], fv["final"] if fv["final"] else fv["n_dev"]),
        "dispositivos")
    h = c.memoria("handoff-%s-custodia.md" % v)
    molde = "" if h.is_file() else ("Handoff: `Nós\\HANDOFF_%s_CUSTODIA.md` (sha16 `%s`); o tópico ainda não existe: a gerência c1 o cria.\n\n" % (v, ctx.handoff.sha16_arquivo))
    saidas["handoff-memoria"] = registrar_memoria(ctx, "handoff-%s-custodia.md" % v, "%s## %s \u2014 CUSTODIADO pela sessão %s da Central\n\n%s" % (molde, when, ctx.sessao, estado), "handoff_custodiado")
    saidas["Atlas"] = ap(c.ATLAS, "[%s \u2014 §X append, re-ancorado ao selo %s `%s`: A CUSTÓDIA DA %s] %s" % (when, v, Fa["pin16"], v, estado), sent(ctx, "atlas"))
    saidas["MEMORY.md"] = propor_linha_memory(ctx, ("CUSTODIADO", "PUBLICADA"), "CUSTODIADO",
                                              "the_boundary `%s`; Central: cofre %s, runner v%d, %d/%d, FINAL, ledger %s" % (fv["esp"], v, fv["runner_n"], fv["n_disp"], fv["n_dev"], fv["ledger"].get("erros")), "custodiado")
    return {k: (x["estado"] if isinstance(x, dict) else x) for k, x in saidas.items()}


def registrar_rota(ctx, estado):
    """Registra a rota custodia.vN no mapa de rotas (livro SÓ-ACRÉSCIMO com cadeia de hash: o que entra não se corrige, só se emenda com ERRATA). Por isso
    só é chamada por C16, DEPOIS do push da Central e da conferência final independente: `nao_refazer` diz «publicada e conferida» e agora é verdade."""
    c, v = ctx.c, ctx.versao
    rota = montar_rota(ctx, estado)
    ctx.W.mkdir(parents=True, exist_ok=True)
    rp = ctx.W / ("rota_custodia_%s.json" % v)
    util.escrever_atomico(rp, json.dumps(rota, ensure_ascii=False, indent=1).encode("utf-8"), backup=True)
    existe = util.rodar([str(c.PYTHON), "-X", "utf8", str(c.MAPA / "rotas.py"), "ver", "custodia.%s" % v])
    try:
        dj = json.loads(existe["saida"].split("\n[stderr]")[0])        # `ver` de rota inexistente sai com rc 0 e {"erro": ...}: o rc não basta
    except ValueError:
        dj = {}
    if existe["rc"] == 0 and dj and "erro" not in dj:
        return "ja_existe"
    r = util.rodar([str(c.PYTHON), "-X", "utf8", str(c.MAPA / "rotas.py"), "registrar", str(rp), "--quem", "%s (custódia %s)" % (ctx.ator, v)])
    if r["rc"] != 0:
        raise Parar("rotas.py registrar falhou", r["saida"].strip().splitlines()[-4:])
    return "registrada"


def passo_c13(ctx):
    return Passo("C13", 4, "registro: diário do site, Atlas; memórias e linha do MEMORY.md pela fila da memória (a rota é de C16)", _ja_c13, aplicar=_ap_c13, pre=_pre_c13, fase="B",
                 escreve="DIARIO_DO_SITE.md, TGL_ATLAS.md (só acréscimo), depósitos em memory\\fila\\depositos\\claude-site (memórias da sessão e a troca da linha do MEMORY.md)")


# =================================================================== C16 — «PUBLICADA»
def _conf_final(ctx):
    for d in reversed(ctx.c.pastas_trabalho_existentes(ctx.versao)):
        p = d / ("CONFERENCIA_FINAL_%s.json" % ctx.versao)
        if p.is_file():
            return util.ler_json(p)
    return None


def _rota_registrada(ctx):
    return '"custodia.%s"' % ctx.versao in util.ler_texto(ctx.c.ROTAS_JSONL, "replace")


def _ja_c16(ctx):
    """«PUBLICADA» nas memórias E a rota custodia.vN no mapa de rotas — a rota só entra aqui, depois do push e da conferência final (achado ALTA dos céticos)."""
    lin, ok = _memory_ja(ctx, ("PUBLICADA",))
    if lin is None:
        return falta("linha do handoff %s ausente no MEMORY.md" % ctx.versao)
    ok = ok or bool(_depositos_com(ctx, sent(ctx, "indice:publicada")))
    h = ctx.c.memoria("handoff-%s-custodia.md" % ctx.versao)
    tem = (h.is_file() and "PUBLICADA (pós-push)" in util.ler_texto(h, "replace")) or bool(_depositos_com(ctx, sent(ctx, "publicada_handoff")))
    rota = _rota_registrada(ctx)
    if ok and tem and rota:
        return aplicado("MEMORY.md e handoff-%s-custodia.md dizem PUBLICADA (ou a fila da memória o tem para a gerência); rota custodia.%s registrada" % (ctx.versao, ctx.versao))
    return falta("sem PUBLICADA/rota em: %s" % ", ".join(x for x, y in (("MEMORY.md", ok), ("handoff-%s-custodia.md" % ctx.versao, tem), ("rota custodia.%s" % ctx.versao, rota)) if not y))


def _pre_c16(ctx):
    cf = _conf_final(ctx)
    f = []
    if not cf or cf.get("ok") != cf.get("total"):
        f.append("a conferência final não está completa (%s)" % (("%s/%s" % (cf.get("ok"), cf.get("total"))) if cf else "ausente"))
    try:
        _esp(ctx)
    except Parar as e:
        f.append(e.motivo)
    cen, cen_o = util.git(ctx.c.CEN, "rev-parse", "--short=8", "HEAD"), util.git(ctx.c.CEN, "rev-parse", "--short=8", "origin/main")
    if cen != cen_o:
        f.append("a Central não está publicada (HEAD %s != origin/main %s)" % (cen, cen_o))
    return f


def _ap_c16(ctx):
    c, v = ctx.c, ctx.versao
    cf = _conf_final(ctx)
    esp = _esp(ctx)
    cen = util.git(c.CEN, "rev-parse", "--short=8", "HEAD")
    fv = fatos_verificados(ctx)
    txt = ("PUBLICADA. Espelho the_boundary `%s` = origin/main; Central `%s` = origin/main (privado); %s Conferência final independente (`work/custodia_%s_*/CONFERENCIA_FINAL_%s.json`, "
           "sem importar a esteira): **%d/%d ok** — o um.py igual no Nós, no espelho, no cofre e no raw do GitHub (o pino); o cofre e o kernel conferem; o site no ar e o README raw "
           "trazem o pino; os dois repositórios sem nada pendente nos caminhos da custódia. Os nomes dos registros novos e a paridade [LEGAL] do ACOM Mirror seguem decisão do "
           "operador. O gate não se moveu." % (esp, cen, site_verificado(ctx), v, v, cf["ok"], cf["total"]))
    viol = textos.portao(txt, textos.conhecidos_da_rodada(ctx), rotulo="publicada")
    if viol:
        raise Parar("o portão de texto reprovou", viol)
    when = agora()
    s = {}
    s["handoff"] = registrar_memoria(ctx, "handoff-%s-custodia.md" % v, "## %s \u2014 PUBLICADA (pós-push)\n\n%s" % (when, txt), "publicada_handoff")
    s["central-estado"] = registrar_memoria(ctx, "central-de-patentes-estado.md", "## %s \u2014 custódia %s publicada\n\n%s" % (when, v, txt), "publicada_central")
    s["diario"] = ap(c.BANC / "DIARIO_DO_SITE.md", "## %s \u2014 a custódia %s PUBLICADA\n\n%s" % (when, v, txt), sent(ctx, "publicada_diario"))
    s["MEMORY.md"] = propor_linha_memory(ctx, ("PUBLICADA",), "PUBLICADA", "the_boundary `%s`; Central `%s`; cofre %s, runner v%d, %d/%d, FINAL, ledger %s; conferência final %d/%d" % (esp, cen, v, fv["runner_n"], fv["n_disp"], fv["n_dev"], fv["ledger"].get("erros"), cf["ok"], cf["total"]), "publicada")
    # a ROTA entra por último e só aqui: o livro é só-acréscimo (cadeia de hash); registrar «publicada e conferida» antes do push seria uma frase que o número ainda não sustenta
    s["rota"] = registrar_rota(ctx, txt)
    return {k: (x["estado"] if isinstance(x, dict) else x) for k, x in s.items()}


def passo_c16(ctx):
    return Passo("C16", 4, "registro «PUBLICADA» (pós-push) e a rota custodia.vN", _ja_c16, aplicar=_ap_c16, pre=_pre_c16, fase="B",
                 escreve="DIARIO_DO_SITE.md, depósitos na fila da memória (memórias da sessão e a troca da linha do MEMORY.md; o Atlas não se toca depois do push), mapa de rotas (só-acréscimo)")


# =================================================================== ACOM — C2 (init) e C17 (transições gerados do estado real)
CLI_ACOM = lambda c: [str(c.PYTHON), "-X", "utf8", str(c.ACOM / "session_memory.py")]


def _refs_acom(ctx):
    d = ctx.c.ACOM / "sessions"
    v = ctx.versao
    return sorted(list(d.glob("*custodia-%s-*.json" % v)) + list(d.glob("custodia_%s_*.json" % v))) if d.is_dir() else []


def acom_chamar(ctx, req):
    r = util.rodar(CLI_ACOM(ctx.c), entrada=json.dumps(req, ensure_ascii=False).encode("utf-8"), timeout=300)
    try:
        d = json.loads(r["saida"].split("\n[stderr]")[0])
    except ValueError:
        raise FalhaLeitura("o CLI do ACOM não devolveu JSON", )
    return d


def acom_revisao(ctx, ref):
    d = acom_chamar(ctx, {"operation": "project", "reference": str(ref)})
    if d.get("ok") is not True:
        raise FalhaLeitura("project falhou: %s %s" % (d.get("error"), str(d.get("message"))[:100]))
    rc = d["result"]["receipt"]
    return rc["revision"], rc.get("event_id", "")


def _ja_c2(ctx):
    refs = _refs_acom(ctx)
    return aplicado("referência %s" % refs[-1].name) if refs else falta("sem referência ACOM própria da custódia %s" % ctx.versao)


def _ap_c2(ctx):
    c, v = ctx.c, ctx.versao
    obj = ctx.ordem or textos.ordem_padrao(c)
    if not obj:
        raise Parar("sem arquivo da ordem do operador para o objetivo ACOM (passe --ordem)")
    ref = c.ACOM / "sessions" / ("custodia_%s_%s.json" % (v, ctx.pin16[:8]))
    if ref.exists():
        return {"referencia": ref.name, "estado": "ja_existe"}
    req = {"operation": "init", "objective_file": str(obj), "objective_sha256": hashlib.sha256(obj.read_bytes()).hexdigest(), "request_id": str(uuid.uuid4()),
           "scope": {"house": "IALD", "principal": "operator"}, "actor": {"id": ctx.ator, "kind": "agent"}, "write_reference": str(ref)}
    d = acom_chamar(ctx, req)
    if d.get("ok") is not True:
        raise Parar("ACOM init falhou: %s %s" % (d.get("error"), str(d.get("message"))[:200]))
    return {"referencia": ref.name}


def passo_c2(ctx):
    return Passo("C2", 4, "ACOM: inscrição (init) da custódia", _ja_c2, aplicar=_ap_c2, externo=True, fase="B", escreve="C:\\IALD\\MEMORIA_IALD\\sessions\\custodia_vN_<pin8>.json (banco comum)")


def _transicao(ctx, n, slug, records, flow):
    """Uma transição t<n>: sha256 de cada fonte calculado AGORA; revisão esperada lida do `project` (nunca digitada)."""
    ref = _refs_acom(ctx)[-1]
    rev, _ = acom_revisao(ctx, ref)
    if rev >= n:
        return {"estado": "ja_aplicado", "revisao": rev}
    if rev != n - 1:
        raise Parar("revisão ACOM %d != esperada %d para a transição t%d" % (rev, n - 1, n))
    for r in records:
        for s in r.get("sources", []):
            if s.get("kind") == "artifact":
                s["sha256"] = hashlib.sha256(Path(s["ref"]).read_bytes()).hexdigest()
    ctx.W.mkdir(parents=True, exist_ok=True)
    ch = ctx.W / ("t%d_changes.json" % n)
    ch.write_text(json.dumps({"records": records, "flow": flow}, ensure_ascii=False), encoding="utf-8")
    req = {"operation": "transition", "reference": str(ref), "expected_revision": rev, "event_id": "%s-custodia-%s-%s-t%d-%s" % (ctx.ator, ctx.versao, ctx.ddmes, n, slug),
           "actor": {"id": ctx.ator, "kind": "agent"}, "changes_file": str(ch), "changes_sha256": hashlib.sha256(ch.read_bytes()).hexdigest()}
    d = acom_chamar(ctx, req)
    if d.get("ok") is not True:
        raise Parar("ACOM transition t%d falhou: %s %s" % (n, d.get("error"), str(d.get("message"))[:200]))
    return {"revisao": d.get("result", {}).get("receipt", {}).get("revision")}


def _ja_t(n):
    def f(ctx):
        refs = _refs_acom(ctx)
        if not refs:
            return falta("sem referência ACOM")
        try:
            rev, ev = acom_revisao(ctx, refs[-1])
        except FalhaLeitura as e:
            return indeterminado(e.motivo)
        return aplicado("revisão ACOM %d (≥ %d); último evento %s" % (rev, n, ev[-50:])) if rev >= n else falta("revisão ACOM %d < %d" % (rev, n))
    return f


def _art(*ps):
    return [{"kind": "artifact", "ref": str(p)} for p in ps if Path(p).is_file()]


def _ap_t1(ctx):
    c, v = ctx.c, ctx.versao
    Fa = ctx.fatos
    fv = fatos_verificados(ctx)
    rec = [{"id": "f1_espelho_%s_publicado" % v, "kind": "fact", "statute": "REAL",
            "text": "Espelho the_boundary: commit %s = origin/main; um.py %s %s (%s; kernel %d/%d no trio); módulos novos %s; fontes pinadas %d de %d; recibos_bancada_%s; diferencas_%s." % (
                fv["esp"], v, Fa["pin16"], Fa["escada"]["texto"], Fa["kernel"]["formais"], Fa["kernel"]["declaracoes"], ", ".join(Fa["kernel"]["modulos_novos"]) or "nenhum",
                fv["mapa"]["n_publicadas"], fv["mapa"]["n_fontes"], v, v),
            "sources": _art(c.BANC / "revisoes" / ("custodia_%s_espelho.json" % v), c.TB / "ESTADO_ATUAL.md")},
           {"id": "f2_site_%s" % v, "kind": "fact", "statute": "REAL", "text": site_verificado(ctx),
            "sources": _art(c.BANC / "revisoes" / ("manifesto_%s.json" % v))},
           {"id": "f3_central_%s_local" % v, "kind": "fact", "statute": "REAL",
            "text": "Central: cofre um_unificado_%s (%s artefatos, %s divergentes) + tgl_kernel_%s; runner v%d aprovado; camada %s %d/%d; ledger %s erros; snapshot %s." % (
                v, fv["man"].get("n_artifacts"), fv["man"].get("mismatches"), v, fv["runner_n"], v, fv["n_disp"], fv["n_dev"], fv["ledger"].get("erros"), fv["snap"]),
            "sources": _art(c.cofre(v) / "CUSTODY_MANIFEST.json")},
           {"id": "d1_gatilho", "kind": "decision", "statute": "INPUT",
            "text": "Gatilho: a regra permanente do operador («custodiar sempre que o handoff aparecer»); as três marcas conferidas por tools/custodiar.py vigiar.", "sources": _art(Path(r"C:\IALD\Central de Patentes\work\php_e_v396_22out\OPERADOR_23out_custodiar_quando_o_handoff_aparecer_verbatim.txt"), ctx.handoff.caminho)}]
    flow = {"phase": "custodia_local_pronta__commit_e_push_da_central_pendentes", "next_action": "commit e push da Central (C14), conferência final (C15), registro PUBLICADA (C16)",
            "handles": [{"id": "git_espelho", "commit": fv["esp"], "status": "empurrado_e_conferido"}]}
    return _transicao(ctx, 1, "espelho-site-central", rec, flow)


def _ap_t2(ctx):
    c, v = ctx.c, ctx.versao
    cf = _conf_final(ctx)
    cen = util.git(c.CEN, "rev-parse", "--short=8", "HEAD")
    esp = _esp(ctx)
    rec = [{"id": "f4_custodia_%s_publicada" % v, "kind": "fact", "statute": "REAL",
            "text": "Custódia %s publicada: espelho %s = origin/main; Central %s = origin/main; conferência final independente %d/%d." % (v, esp, cen, cf["ok"], cf["total"]),
            "sources": _art(ctx.W / ("CONFERENCIA_FINAL_%s.json" % v), ctx.W / ("rota_custodia_%s.json" % v))}]
    pend = ctx.handoff.secao("Pendências SÓ do operador")
    if pend:
        rec.append({"id": "p1_do_operador", "kind": "pending", "statute": "OPEN", "text": re.sub(r"^\*\*[^*]+\*\*\s*", "", pend).replace("\n", " ")[:1500], "sources": _art(ctx.handoff.caminho)})
    flow = {"phase": "custodia_privada_publicada", "next_action": "Central pública (C18) e quadro do organismo (C19)",
            "handles": [{"id": "git_espelho", "commit": esp, "status": "empurrado_e_conferido"}, {"id": "git_central", "commit": cen, "status": "empurrado_e_conferido"}]}
    return _transicao(ctx, 2, "custodia-publicada", rec, flow)


def _ap_t3(ctx):
    from . import quadro
    q = quadro.ler_quadro(ctx)
    ok_fresco, motivo = quadro.fresco(q, quadro.marcos_c19(ctx)) if q else (False, "sem ESTADO_DO_ORGANISMO.json")
    if not ok_fresco:                     # o fato «organismo medido» não se grava sobre um quadro VELHO (achado dos céticos)
        raise Parar("a transição t3 cita o quadro do organismo, e ele não é fresco: %s" % motivo)
    res = (q or {}).get("resumo", {})
    rec = [{"id": "f6_quadro_%s" % ctx.versao, "kind": "fact", "statute": "REAL",
            "text": "Quadro do organismo medido em %s: %s." % ((q or {}).get("medido_em"), ", ".join("%s %s" % (k, x) for k, x in sorted(res.items())) or "sem leitura"),
            "sources": _art(ctx.c.CEN / "organismo" / "ESTADO_DO_ORGANISMO.json")}]
    flow = {"phase": "custodia_concluida_organismo_medido", "next_action": "nenhuma além das pendências do operador", "handles": []}
    return _transicao(ctx, 3, "concluida-organismo-medido", rec, flow)


def passo_c17a(ctx):
    return Passo("C17A", 4, "ACOM: transição t1 (espelho, site, Central local)", _ja_t(1), aplicar=_ap_t1, externo=True, fase="B", escreve="banco ACOM (transição t1, CAS, evento idempotente)")


def passo_c17b(ctx):
    return Passo("C17B", 4, "ACOM: transição t2 (custódia publicada)", _ja_t(2), aplicar=_ap_t2, externo=True, fase="B", escreve="banco ACOM (transição t2)")


def passo_c17c(ctx):
    return Passo("C17C", 4, "ACOM: transição t3 (organismo medido)", _ja_t(3), aplicar=_ap_t3, externo=True, fase="B", escreve="banco ACOM (transição t3)")
