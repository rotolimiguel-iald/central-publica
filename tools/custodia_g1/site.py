# -*- coding: utf-8 -*-
"""Perna 1b — o SITE da TGL (E13..E19): dados literais do selo, aplicar o selo, corpo inteiro e gêmeo Markdown, sitemap e manifesto, subida em
ensaio, subida, leitor de IA. Os geradores e o `subir_site.py` são os de hoje; G1 acrescenta o que faltava (ESPEC_ESPELHO §E17):

  - o CONJUNTO ESPERADO da subida (L10): o ensaio só pode diferir nos arquivos que esta custódia escreveu (index, i18n, read-brief, llms*,
    index.md, sitemap, secoes\\*); qualquer DIFERENTE/NOVO/AUSENTE fora dele (por exemplo em `central\\**`) PARA a custódia — o manifesto
    cobre o site INTEIRO e publicaria o meio-trabalho de outra sessão;
  - `--sem-guarda` e `--permitir-ftp-em-claro` NUNCA são passados (a regra é do operador); credenciais não são lidas por G1;
  - cada passo confere o código de saída (nada de `| tail` escondendo rc).

MARCAS POR CONTEÚDO, NÃO POR NOME (achado ALTA dos céticos, 24/10/2026). Antes, E17 e E18 eram «já aplicados» se um relatório CITASSE O NOME do
manifesto — e E16, que regera o manifesto, só conferia 4 dos 1.428 arquivos: depois de E16 a marca seguia «ok» e o conteúdo novo nunca subia. Agora:

  - o ALVO é o conteúdo do SITE: na versão corrente, o DISCO agora (sha256 de cada arquivo, com as regras de exclusão do próprio manifesto);
    na histórica, o `manifesto_vNNN.json` da versão;
  - E18 lê o REGISTRO das subidas (`subidas\\<carimbo>\\MANIFESTO_SUBIDA.json` = o manifesto que subiu, + «SUBIDA VERIFICADA» no relatório) e repete,
    do mais novo ao mais velho, o que o ar passou a ter: o ar tem o alvo se, para cada arquivo, a subida VERIFICADA mais nova que o cita levou o mesmo sha256
    (subida não verificada deixa o arquivo DESCONHECIDO). Qualquer subida que o cubra vale — a da perna 3 (Central pública) inclusive;
  - E17 exige um ensaio cujas linhas (sha16 local de CADA arquivo) coincidem com o alvo; se o ar já tem o alvo, o ensaio é dispensado (SUPERADO);
  - E16 confere o manifesto contra o disco inteiro; se o manifesto está velho mas o ar já tem o disco, o manifesto é só o registro do momento (SUPERADO);
  - E17..E19 ficam FALTA enquanto E16 estiver FALTA (a cadeia manifesto -> ensaio -> subida -> leitor não pula elo).

«NADA A SUBIR» (achado MEDIA do cético final, 24/10/2026). Quando o ar já é igual ao manifesto, `subir_site.py` grava uma pasta com a cópia do manifesto e um relatório
«nada a subir: o ar já é igual ao manifesto» — SEM «SUBIDA VERIFICADA». Antes, essa pasta (a mais nova a citar cada arquivo) deixava o ar DESCONHECIDO e escondia a subida
verificada anterior: E18 virava FALTA e `_ap_e18` travava (não achava «SUBIDA VERIFICADA»). Agora o relatório é lido linha a linha: a linha «IGUAL» (sha256 comparado por HTTP,
no ato) atesta o hash; «IGUAL EM TAMANHO»/«PRESENTE» não decide (as subidas mais antigas decidem); linha que contradiz o título deixa o arquivo DESCONHECIDO; `_ap_e18` aceita as duas
terminações. E19 (achado BAIXA): só o relatório do leitor de IA MAIS NOVO conta (um R1 antigo que passou não cobre um mais recente que falhou) e ele tem de ser POSTERIOR à última subida verificada.
A subida é o ato PARA FORA do site: só com --publicar."""
import fnmatch
import os
import re
from datetime import datetime
from pathlib import Path

from . import util
from .espelho import _banc, exigir_rc0, _historica
from .motor import Passo, aplicado, falta, superado, superado_rel, indeterminado, bloqueado
from .util import Parar, Divergencia

ESPERADOS = (re.compile(r"^index\.html$"), re.compile(r"^i18n\.js$"), re.compile(r"^index\.md$"), re.compile(r"^llms-full\.txt$"), re.compile(r"^llms\.txt$"),
             re.compile(r"^read-brief\.(md|txt)$"), re.compile(r"^estado\.(json|txt)$"), re.compile(r"^sitemap\.xml$"),  # 25/10: o cartao de estado (E15)
             re.compile(r"^secoes/"), re.compile(r"^\.htaccess$"))
RE_NOTA = re.compile(r'Current seal: <strong>(v\d{3,})</strong>, pin <span class="notranslate">([0-9a-f]{16})')
RE_LINHA_ENSAIO = re.compile(r"^\| `([^`]+)` \|.*\| (IGUAL|DIFERENTE|NOVO|AUSENTE|A ENVIAR SEMPRE)[^|]*\|\s*$", re.M)
# a tabela «O ar antes» (a 1ª do relatório): | arquivo | bytes local | sha16 local | HTTP | bytes ar | content-type | estado |
RE_LINHA_COMPLETA = re.compile(r"^\| `([^`]+)` \| ([\d.]+) \| ([0-9a-f]{16}) \|(?: [^|]*\|){3} ([^|]*?) \|\s*$", re.M)
# o título que `subir_site.py` grava quando o ar já é igual ao manifesto: «# SUBIDA <carimbo> — nada a subir: o ar já é igual ao manifesto»
RE_NADA = re.compile(r"^# SUBIDA\s+\S+\s+[\u2014-]+\s+nada a subir:\s+o ar j\u00e1 \u00e9 igual ao manifesto", re.M)
# o cabeçalho do relatório do leitor de IA: «# LEITOR-IA (R1) — dd/mm/aaaa hh:mm:ss»
RE_LEITOR_T = re.compile(r"^# LEITOR-IA \(R1\)\s+[\u2014-]+\s+(\d\d/\d\d/\d{4} \d\d:\d\d:\d\d)", re.M)
# as regras de exclusão do gerador de manifesto, usadas SÓ se nenhum manifesto traz a sua cópia (`regras_exclusao`)
REGRAS_PADRAO = {"dirs": ["_identidade", "Versões Anteriores", "Música", "v3.0_bancada", "_SUBIR_*", "node_modules", ".git"],
                 "files": ["*.bak_*", "_gen_device_lines.py", "SUBIR_*.md", "tgl_demo_dipole_ORIGINAL_backup.mp4", ".env", "CLAUDE.md", "LEIA-ME.md",
                           "MANIFESTO_SUBIDA.json", "*.tmp", "Thumbs.db", ".DS_Store", "*.bak"]}
MAX_ENSAIOS = 8          # quantos ensaios (do mais novo) se examinam na versão corrente


def _manifesto(ctx):
    return ctx.c.BANC / "revisoes" / ("manifesto_%s.json" % ctx.versao)


def _nota_do_index(ctx):
    m = RE_NOTA.search(ctx.ler(ctx.c.SITE / "index.html"))
    return m.groups() if m else (None, None)


# =================================================================== o registro das subidas (relatórios e cópias do manifesto)
def _subidas(ctx, dry):
    d = ctx.c.BANC / "subidas"
    out = []
    if d.is_dir():
        for p in sorted(d.iterdir()):
            if not p.is_dir() or p.name.startswith("_") or not (p / "RELATORIO.md").is_file():
                continue
            if p.name.endswith("_dryrun") != dry:
                continue
            out.append(p)
    return out


def _natureza(ctx, p):
    """Como a subida `p` terminou, lido do RELATORIO.md (memo por execução):
      VERIFICADA  «SUBIDA VERIFICADA»: o que foi enviado foi verificado no ar (HTTP, bytes, sha256) e o resto estava IGUAL antes;
      NADA        «nada a subir: o ar já é igual ao manifesto»: `subir_site.py` comparou o ar arquivo a arquivo e não enviou nada — vale como VERIFICAÇÃO do ar, linha a linha
                  da tabela (só a linha «IGUAL», sha256 comparado por HTTP, atesta o hash; ver `_linhas_nada`);
      OUTRA       falhou, reverteu, a guarda falhou ou ficou sem veredito: deixa o ar DESCONHECIDO nos arquivos que cita."""
    cache = ctx.memo("subidas_natureza", dict)
    if p.name not in cache:
        t = util.ler_texto(p / "RELATORIO.md", "replace")
        cache[p.name] = "VERIFICADA" if "SUBIDA VERIFICADA" in t else ("NADA" if RE_NADA.search(t) else "OUTRA")
    return cache[p.name]


def _verificada(ctx, p):
    """A subida terminou em «SUBIDA VERIFICADA» (uma subida sem isso deixa o ar DESCONHECIDO — salvo o «nada a subir», que atesta linha a linha: ver `_natureza`)."""
    return _natureza(ctx, p) == "VERIFICADA"


def _linhas_nada(ctx, p):
    """{caminho: (sha16, estado)} da tabela do relatório de «nada a subir» da pasta `p` (memo). `estado` é o da última coluna: «IGUAL», «IGUAL EM TAMANHO (…)», …"""
    cache = ctx.memo("subidas_nada", dict)
    if p.name not in cache:
        texto = util.ler_texto(p / "RELATORIO.md", "replace")
        cache[p.name] = {k: (v[1], v[2].strip()) for k, v in linhas_do_relatorio(texto).items()}
    return cache[p.name]


def _copia_do_manifesto(ctx, p):
    """{caminho: sha256} do `MANIFESTO_SUBIDA.json` que a subida `p` levou (a cópia exata), ou None se a pasta não a tem."""
    mp = p / "MANIFESTO_SUBIDA.json"
    if not mp.is_file():
        return None
    d = ctx.lido(mp)
    return {a["caminho"]: a["sha256"] for a in d.get("arquivos", [])}


def instante_da_ultima_subida(ctx):
    """Quando terminou a subida VERIFICADA mais nova (mtime do relatório); None se nenhuma."""
    for p in reversed(_subidas(ctx, False)):
        if _verificada(ctx, p):
            return datetime.fromtimestamp((p / "RELATORIO.md").stat().st_mtime)
    return None


def instante_da_subida_que_vale(ctx):
    """Para E19: quando terminou a subida VERIFICADA que deixou o conteúdo no ar — a mais nova (versão corrente) ou a que levou o manifesto da versão (histórica). O relatório
    do leitor de IA (R1) tem de ser POSTERIOR a ela. «Nada a subir» não muda o ar: não conta. None se nenhuma."""
    if ctx.corrente:
        return instante_da_ultima_subida(ctx)
    alvo, _desc, desde = _alvo(ctx)
    if alvo is None:
        return None
    p = subida_que_levou(ctx, alvo, desde, so_verificadas=True)
    return datetime.fromtimestamp((p / "RELATORIO.md").stat().st_mtime) if p else None


def ar_pelo_registro(ctx, alvo):
    """O que o AR tem de `alvo` {caminho: sha256}, repetindo as subidas do mais novo ao mais velho: o arquivo vale o que a subida mais nova que o cita levou
    — se ela foi VERIFICADA; se não, o arquivo é DESCONHECIDO. Uma pasta de «nada a subir» (o ar já era igual) é uma VERIFICAÇÃO do ar, linha a linha: a linha «IGUAL» atesta o
    sha256 do manifesto; «IGUAL EM TAMANHO»/«PRESENTE» não decide (a subida mais antiga decide, o registro anterior continua válido); linha que contradiz o título deixa DESCONHECIDO.
    Devolve {n, iguais, diferentes[], desconhecidos[], nunca[], ultima, ultima_tipo, ok}."""
    resolvido, pend, ultima, ultima_tipo = {}, set(alvo), None, None
    for p in reversed(_subidas(ctx, False)):
        if not pend:
            break
        arqs = _copia_do_manifesto(ctx, p)
        if arqs is None:
            continue
        nat = _natureza(ctx, p)
        if nat == "VERIFICADA" and ultima is None:
            ultima, ultima_tipo = p.name, nat
        for path in sorted(x for x in pend if x in arqs):
            if nat == "VERIFICADA":
                resolvido[path] = (arqs[path], p.name)
            elif nat == "NADA":
                sha16, estado = _linhas_nada(ctx, p).get(path, (None, "sem linha no relatório"))
                if estado == "IGUAL" and sha16 == arqs[path][:16]:
                    resolvido[path] = (arqs[path], p.name)              # o ar foi comparado, sha256 a sha256, e era igual ao manifesto desta pasta
                    if ultima is None:
                        ultima, ultima_tipo = p.name, nat
                elif estado.startswith(("IGUAL EM TAMANHO", "PRESENTE")):
                    continue                                              # o hash não foi comparado: não decide; as subidas mais antigas decidem
                else:
                    resolvido[path] = (None, p.name)                      # a linha contradiz o título «nada a subir»: DESCONHECIDO
            else:
                resolvido[path] = (None, p.name)
            pend.discard(path)
    iguais = sum(1 for k in alvo if k in resolvido and resolvido[k][0] == alvo[k])
    dif = sorted(k for k in alvo if k in resolvido and resolvido[k][0] not in (None, alvo[k]))
    desc = sorted(k for k in alvo if k in resolvido and resolvido[k][0] is None)
    nunca = sorted(k for k in alvo if k not in resolvido)
    return {"n": len(alvo), "iguais": iguais, "diferentes": dif, "desconhecidos": desc, "nunca": nunca, "ultima": ultima, "ultima_tipo": ultima_tipo,
            "ok": bool(alvo) and iguais == len(alvo)}


def subida_que_levou(ctx, alvo, desde=None, so_verificadas=False):
    """Versão histórica: uma subida VERIFICADA cuja cópia do manifesto leva EXATAMENTE o conteúdo de `alvo` (todo caminho, mesmo sha256). Do mais novo
    ao mais velho; `desde` (datetime) limita às subidas depois da geração do manifesto da versão. Uma pasta de «nada a subir» também vale (o ar JÁ era igual ao alvo),
    se a tabela traz «IGUAL» com o sha16 do alvo em CADA arquivo — salvo `so_verificadas` (quem pergunta quando o ar MUDOU). Devolve a pasta ou None."""
    for p in reversed(_subidas(ctx, False)):
        t = util.instante(p.name)
        if desde is not None and t is not None and t < desde:
            break
        nat = _natureza(ctx, p)
        if nat == "OUTRA" or (nat == "NADA" and so_verificadas):
            continue
        arqs = _copia_do_manifesto(ctx, p)
        if arqs is None or not all(arqs.get(k) == h for k, h in alvo.items()):
            continue
        if nat == "NADA":
            linhas = _linhas_nada(ctx, p)
            if not all(k in linhas and linhas[k][1] == "IGUAL" and linhas[k][0] == h[:16] for k, h in alvo.items()):
                continue
        return p
    return None


# =================================================================== o alvo: o conteúdo que o site deve ter
def _excluido(rel, regras):
    partes = rel.split("/")
    for d in partes[:-1]:
        if any(fnmatch.fnmatch(d, pat) for pat in regras["dirs"]):
            return True
    nome = partes[-1]
    if ".bak_" in nome:
        return True
    return any(fnmatch.fnmatch(nome, pat) for pat in regras["files"])


def _regras_de_referencia(ctx):
    """As regras de exclusão que o PRÓPRIO gerador gravou no manifesto (o da versão; senão a cópia da subida mais nova); o padrão só em último caso."""
    mp = _manifesto(ctx)
    if mp.is_file():
        r = ctx.lido(mp).get("regras_exclusao")
        if r:
            return r
    for p in reversed(_subidas(ctx, False)):
        mp2 = p / "MANIFESTO_SUBIDA.json"
        if mp2.is_file():
            r = ctx.lido(mp2).get("regras_exclusao")
            if r:
                return r
    return REGRAS_PADRAO


def disco_atual(ctx):
    """{caminho relativo (posix): sha256} de TODO arquivo do site que sobe (regras de exclusão do gerador), lido do disco AGORA (memo por execução)."""
    def f():
        base = ctx.c.SITE
        regras = _regras_de_referencia(ctx)
        base_s = str(util.lp(base))
        out = {}
        for root, dirs, files in os.walk(base_s):
            dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(d, pat) for pat in regras["dirs"])]
            for fn in files:
                full = os.path.join(root, fn)
                rel = os.path.relpath(full, base_s).replace(os.sep, "/")
                if _excluido(rel, regras):
                    continue
                out[rel] = util.sha256_arquivo(full)
        return out
    return ctx.memo("disco_atual", f)


def manifesto_vs_disco(ctx):
    """O manifesto da versão contra o disco inteiro: {n, mudados[], novos[], sumidos[]} (caminho a caminho, sha256)."""
    m = ctx.lido(_manifesto(ctx))
    esp = {a["caminho"]: a["sha256"] for a in m.get("arquivos", [])}
    listados_fora = {e["caminho"] for e in m.get("excluidos", [])}
    disco = disco_atual(ctx)
    mudados = sorted(k for k, h in esp.items() if k in disco and disco[k] != h)
    sumidos = sorted(k for k in esp if k not in disco)
    novos = sorted(k for k in disco if k not in esp and k not in listados_fora)
    return {"n": len(esp), "mudados": mudados, "novos": novos, "sumidos": sumidos}


def manifesto_integro(m):
    arqs = m.get("arquivos", [])
    return m.get("n") == len(arqs) and m.get("total_bytes") == sum(a.get("bytes", 0) for a in arqs)


def _alvo(ctx):
    """(alvo {caminho: sha256}, descrição, desde): corrente -> o DISCO agora; histórica -> o manifesto da versão. Sem o manifesto da versão histórica:
    (None, motivo, None) — é FALTA do insumo, não falha de leitura."""
    if ctx.corrente:
        return disco_atual(ctx), "disco de %s" % ctx.c.SITE.name, None
    mp = _manifesto(ctx)
    if not mp.is_file():
        return None, "manifesto_%s.json ausente (o alvo da versão histórica)" % ctx.versao, None
    m = ctx.lido(mp)
    return {a["caminho"]: a["sha256"] for a in m["arquivos"]}, "manifesto_%s.json" % ctx.versao, util.instante(m.get("gerado_em"))


def _txt_dif(r, k=3):
    partes = []
    for rot, lst in (("diferem", r["diferentes"]), ("desconhecidos", r["desconhecidos"]), ("nunca subiram", r["nunca"])):
        if lst:
            partes.append("%d %s (ex.: %s)" % (len(lst), rot, ", ".join(lst[:k])))
    return "; ".join(partes) or "nenhuma diferença"


def _ar_do_alvo(ctx):
    """O estado do ar frente ao alvo desta versão (memo): corrente -> repetição das subidas contra o disco; histórica -> uma subida que levou o manifesto."""
    def f():
        alvo, desc, desde = _alvo(ctx)
        if alvo is None:
            return {"n": 0, "ok": False, "ultima": None, "descricao": desc, "iguais": 0, "diferentes": [], "desconhecidos": [], "nunca": [], "sem_alvo": True}
        if ctx.corrente:
            r = ar_pelo_registro(ctx, alvo)
            r["descricao"] = desc
            return r
        p = subida_que_levou(ctx, alvo, desde)
        return {"n": len(alvo), "ok": p is not None, "ultima": p.name if p else None, "ultima_tipo": _natureza(ctx, p) if p else None, "descricao": desc,
                "iguais": len(alvo) if p else 0, "diferentes": [], "desconhecidos": [], "nunca": [] if p else sorted(alvo)}
    return ctx.memo("ar_do_alvo", f)


def _dep_e16(ctx):
    """E17..E19 ficam FALTA enquanto E16 estiver FALTA (versão corrente)."""
    if not ctx.corrente:
        return None
    m = _ja_e16(ctx)
    if not m.satisfeita:
        return falta("depende de E16 (%s)" % m.detalhe[:140])
    return None


# =================================================================== E13 — dados literais do selo
def _ja_e13(ctx):
    if ctx.rel_espelho == "atras":
        return falta("o espelho ainda não está em %s" % ctx.versao)
    v_nota, p_nota = _nota_do_index(ctx)
    if v_nota is None:
        return indeterminado("nota «Current seal» do index.html não achada")
    if v_nota == ctx.versao and p_nota == ctx.pin16:
        return aplicado("nota «Current seal» = %s %s" % (ctx.versao, p_nota))
    if util.versao_num(v_nota) > ctx.n:
        return superado_rel("o site já diz %s (versão posterior; o site de %s não é mais lido)" % (v_nota, ctx.versao))
    return falta("o site diz %s %s; o selo é %s %s" % (v_nota, p_nota, ctx.versao, ctx.pin16))


def _pre_e13(ctx):
    f = []
    if ctx.rel_espelho != "igual":
        f.append("o espelho não está em %s" % ctx.versao)
    v_nota, _ = _nota_do_index(ctx)
    if v_nota and not list(ctx.c.BK.glob("um_%s_*" % v_nota)):
        f.append("sem BK\\um_%s_* (o backup da versão que o site diz hoje; E01 da custódia em que ele entrou)" % v_nota)
    if not (ctx.c.BANC / "revisoes" / ("arco_%s_texto.json" % ctx.versao)).is_file():
        f.append("arco_%s_texto.json ausente (E04)" % ctx.versao)
    return f


def _ap_e13(ctx):
    r0 = exigir_rc0(_banc(ctx, "atualizar_dados_selo_site.py", "--conferir"), "atualizar_dados_selo_site.py --conferir")
    r = exigir_rc0(_banc(ctx, "atualizar_dados_selo_site.py"), "atualizar_dados_selo_site.py")
    return {"conferir": r0["saida"].strip().splitlines()[-1][:120], "ultima": r["saida"].strip().splitlines()[-1][:120]}


def _conf_e13(ctx):
    ctx._cache_t.clear()
    v_nota, p_nota = _nota_do_index(ctx)
    return [] if (v_nota, p_nota) == (ctx.versao, ctx.pin16) else ["nota «Current seal» = %s %s depois do passo" % (v_nota, p_nota)]


# =================================================================== E14 — aplicar o selo ao index
def _ja_e14(ctx):
    if ctx.rel_espelho == "atras":
        return falta("o espelho ainda não está em %s" % ctx.versao)
    h = ctx.ler(ctx.c.SITE / "index.html")
    if ("%s · %s" % (ctx.versao, ctx.pin16)) in h:
        return aplicado("index.html diz «%s · %s»" % (ctx.versao, ctx.pin16))
    v_nota, _ = _nota_do_index(ctx)
    if v_nota and util.versao_num(v_nota) > ctx.n:
        return superado_rel("o site já diz %s (versão posterior)" % v_nota)
    return falta("index.html não diz «%s · %s»" % (ctx.versao, ctx.pin16))


def _ap_e14(ctx):
    exigir_rc0(_banc(ctx, "aplicar_selo.py"), "aplicar_selo.py")
    r = exigir_rc0(_banc(ctx, "aplicar_selo.py", "--conferir"), "aplicar_selo.py --conferir")
    if "O INDEX DIZ O QUE O SELO DESCREVE" not in r["saida"]:
        raise Parar("aplicar_selo.py --conferir sem o veredito «O INDEX DIZ O QUE O SELO DESCREVE»", r["saida"].strip().splitlines()[-4:])
    return {"veredito": "O INDEX DIZ O QUE O SELO DESCREVE"}


# =================================================================== E15 — corpo inteiro e gêmeo Markdown
def _ja_e15(ctx):
    if ctx.rel_espelho == "atras":
        return falta("o espelho ainda não está em %s" % ctx.versao)
    faltam = [n for n in ("llms-full.txt", "index.md", "estado.json", "estado.txt") if ctx.pin16 not in ctx.ler(ctx.c.SITE / n)]
    if not faltam:
        return aplicado("llms-full.txt, index.md e o cartão de estado trazem %s" % ctx.pin16)
    if _historica(ctx):
        return superado_rel("regerados a cada versão (G1 não tem a cópia desta versão)")
    return falta("sem o pino em: %s" % ", ".join(faltam))


def _ap_e15(ctx):
    exigir_rc0(_banc(ctx, "gerar_cartao_estado.py"), "gerar_cartao_estado.py")   # 25/10/2026 (ORDEM 023): estado.json, estado.txt, read-brief.txt
    exigir_rc0(_banc(ctx, "gerar_llms_full.py"), "gerar_llms_full.py")
    exigir_rc0(_banc(ctx, "gerar_index_md.py"), "gerar_index_md.py")
    return {}


# =================================================================== E16 — sitemap e manifesto de subida
def _ja_e16(ctx):
    if ctx.rel_espelho == "atras":
        return falta("o espelho ainda não está em %s" % ctx.versao)
    mp = _manifesto(ctx)
    if not mp.is_file():
        return falta("manifesto_%s.json ausente" % ctx.versao)
    m = ctx.lido(mp)
    if not ctx.corrente:                                  # versão histórica: o manifesto é o registro; o disco já andou
        if not manifesto_integro(m):
            return indeterminado("manifesto_%s.json não é íntegro (n/total_bytes não batem com a lista)" % ctx.versao)
        return superado("manifesto_%s.json existe e é íntegro (%d arquivos, %s bytes)" % (ctx.versao, m["n"], util.fmt_milhar(m["total_bytes"])))
    if not (ctx.c.SITE / "sitemap.xml").is_file():
        return falta("sitemap.xml ausente")
    r = manifesto_vs_disco(ctx)
    if not (r["mudados"] or r["novos"] or r["sumidos"]):
        return aplicado("manifesto confere com o disco inteiro: %d arquivos, 0 mudados, 0 novos, 0 sumidos" % r["n"])
    quebra = "%d mudados (ex.: %s), %d novos, %d sumidos" % (len(r["mudados"]), ", ".join(r["mudados"][:3]) or "-", len(r["novos"]), len(r["sumidos"]))
    ar = _ar_do_alvo(ctx)
    if ar["ok"]:                                          # o ar já tem o disco: o manifesto velho é só o registro do momento
        return superado("o ar (pelo registro das subidas verificadas, última %s) já tem o conteúdo do disco; manifesto_%s.json é o registro do momento (%s desde então)"
                        % (ar["ultima"], ctx.versao, quebra))
    return falta("o manifesto está velho frente ao disco: %s" % quebra)


def _ap_e16(ctx):
    c = ctx.c
    r1 = exigir_rc0(_banc(ctx, "gerar_sitemap.py", "--saida", str(c.SITE / "sitemap.xml"), "--base", str(c.SITE)), "gerar_sitemap.py")
    fora = [l for l in r1["saida"].splitlines() if l.strip().startswith("fora:")]
    r2 = exigir_rc0(_banc(ctx, "gerar_manifesto.py", "--base", str(c.SITE), "--saida", str(_manifesto(ctx)), "--url-base", c.URL_SITE), "gerar_manifesto.py")
    return {"sitemap_fora": len(fora), "manifesto": r2["saida"].strip().splitlines()[-1][:120]}


def _conf_e16(ctx):
    ctx._cache_j.clear()
    ctx._memo.pop("disco_atual", None)
    ctx._memo.pop("ar_do_alvo", None)
    r = manifesto_vs_disco(ctx)
    return ["o manifesto recém-gerado não confere com o disco: %d mudados, %d novos, %d sumidos" % (len(r["mudados"]), len(r["novos"]), len(r["sumidos"]))] if (
        r["mudados"] or r["novos"] or r["sumidos"]) else []


# =================================================================== E17 — subida em ensaio (dry-run) e o CONJUNTO ESPERADO
def _diferencas_do_ensaio(texto):
    return [(m.group(1), m.group(2)) for m in RE_LINHA_ENSAIO.finditer(texto) if m.group(2) != "IGUAL"]


def fora_do_esperado(difs):
    return [(p, e) for p, e in difs if not any(rx.match(p) for rx in ESPERADOS)]


def linhas_do_relatorio(texto):
    """{caminho: (bytes, sha16, estado)} da PRIMEIRA tabela do relatório (o ar antes / o que o ar diz hoje)."""
    corte = texto.find("\n## ", texto.find("\n## ") + 1)
    sec = texto[:corte] if corte > 0 else texto
    out = {}
    for m in RE_LINHA_COMPLETA.finditer(sec):
        out[m.group(1)] = (int(m.group(2).replace(".", "")), m.group(3), m.group(4))
    return out


def ensaio_que_cobre(ctx, alvo, desde=None, maximo=MAX_ENSAIOS):
    """O ensaio (dry-run) mais novo cujas linhas trazem, para CADA arquivo do alvo, o sha16 local igual ao do alvo. Devolve (pasta, texto do relatório, quase)
    onde `quase` descreve o ensaio mais novo que NÃO cobriu (para a mensagem de FALTA)."""
    quase = None
    for i, p in enumerate(reversed(_subidas(ctx, True))):
        t = util.instante(p.name)
        if i >= maximo or (desde is not None and t is not None and t < desde):
            break
        texto = util.ler_texto(p / "RELATORIO.md", "replace")
        linhas = linhas_do_relatorio(texto)
        dif = [k for k, h in alvo.items() if k not in linhas or linhas[k][1] != h[:16]]
        if not dif:
            return p, texto, None
        if quase is None:
            quase = "o ensaio mais novo (%s) difere do alvo em %d arquivos (ex.: %s)" % (p.name, len(dif), ", ".join(dif[:3]))
    return None, None, quase


def _ja_e17(ctx):
    if ctx.rel_espelho == "atras":
        return falta("o espelho ainda não está em %s" % ctx.versao)
    dep = _dep_e16(ctx)
    if dep:
        return dep
    alvo, desc, desde = _alvo(ctx)
    if alvo is None:
        return falta(desc)
    ar = _ar_do_alvo(ctx)
    if ctx.corrente and ar["ok"]:          # o ar já tem o conteúdo do disco: o ensaio (que antecede uma subida) não tem mais o que gatear
        return superado("o ar já tem o conteúdo do alvo (%s) (E18, pelo registro das subidas verificadas; última %s): o ensaio é dispensado" % (desc, ar["ultima"]))
    p, texto, quase = ensaio_que_cobre(ctx, alvo, desde)
    if p is not None:
        difs = _diferencas_do_ensaio(texto)
        fora = fora_do_esperado(difs)
        if fora and ctx.corrente:
            return bloqueado("o ensaio %s cobre o alvo mas difere FORA do conjunto esperado (L10): %s" % (p.name, "; ".join("%s: %s" % x for x in fora[:5])))
        if fora:          # versão histórica: o gate L10 é de G1 e não existia na custódia manual da época — a ressalva fica dita, o passado não é reprovado
            return aplicado("ensaio %s cobre o alvo (%s): %d arquivos, sha16 de cada um igual; ressalva: a custódia da época subiu com %d diferença(s) FORA do conjunto "
                            "esperado de G1 (ex.: %s)" % (p.name, desc, len(alvo), len(fora), "; ".join("%s: %s" % x for x in fora[:2])))
        return aplicado("ensaio %s cobre o alvo (%s): %d arquivos, sha16 de cada um igual; %d diferenças com o ar, todas no conjunto esperado" % (p.name, desc, len(alvo), len(difs)))
    ar = _ar_do_alvo(ctx)
    if ar["ok"]:
        return superado("o ar já tem o conteúdo do alvo (%s) (E18, subida %s): o ensaio é dispensado" % (desc, ar["ultima"]))
    return falta("nenhum ensaio cobre o alvo (%s)%s" % (desc, (": " + quase) if quase else ""))


def _ap_e17(ctx):
    exigir_rc0(_banc(ctx, "subir_site.py", "--manifesto", str(_manifesto(ctx)), "--dry-run", timeout=3600), "subir_site.py --dry-run")
    ens = _subidas(ctx, True)
    if not ens:
        raise Parar("o ensaio não deixou RELATORIO.md em subidas\\")
    difs = _diferencas_do_ensaio(util.ler_texto(ens[-1] / "RELATORIO.md", "replace"))
    fora = fora_do_esperado(difs)
    if fora:
        raise Parar("o ensaio da subida difere FORA do conjunto esperado desta custódia (publicaria meio-trabalho de outra sessão — L10)", ["%s: %s" % x for x in fora[:20]])
    return {"relatorio": ens[-1].name, "diferencas_esperadas": len(difs)}


# =================================================================== E18 — subida (ato para fora)
def _ja_e18(ctx):
    if ctx.rel_espelho == "atras":
        return falta("o espelho ainda não está em %s" % ctx.versao)
    dep = _dep_e16(ctx)
    if dep:
        return dep
    ar = _ar_do_alvo(ctx)
    if ar["ok"]:
        nada = ar.get("ultima_tipo") == "NADA"
        if ctx.corrente:
            return aplicado("o ar (pelo registro das subidas verificadas%s; última: %s) tem os %d arquivos do alvo (%s), cada sha256 igual" % (
                " e dos «nada a subir», em que o ar foi comparado e já era igual" if nada else "", ar["ultima"], ar["n"], ar["descricao"]))
        if nada:
            return aplicado("%s: «nada a subir» — o ar já era igual ao conteúdo exato do alvo (%s): %d arquivos, sha256 comparado por HTTP" % (ar["ultima"], ar["descricao"], ar["n"]))
        return aplicado("%s: SUBIDA VERIFICADA levou o conteúdo exato do alvo (%s): %d arquivos" % (ar["ultima"], ar["descricao"], ar["n"]))
    if ar.get("sem_alvo"):
        return falta(ar["descricao"])
    if ctx.corrente:
        return falta("o ar (pelo registro das subidas verificadas) difere do alvo (%s): %s" % (ar["descricao"], _txt_dif(ar)))
    return falta("nenhuma subida verificada levou o conteúdo exato do alvo (%s)" % ar["descricao"])


def _ap_e18(ctx):
    r = util.rodar([str(ctx.c.PYTHON), "-X", "utf8", "tools/subir_site.py", "--manifesto", str(_manifesto(ctx))], cwd=ctx.c.BANC, timeout=7200)
    verificada, nada = "SUBIDA VERIFICADA" in r["saida"], bool(RE_NADA.search(r["saida"]))
    if r["rc"] != 0 or not (verificada or nada):
        raise Divergencia("subir_site.py não terminou em «SUBIDA VERIFICADA» nem em «nada a subir: o ar já é igual ao manifesto» (rc %s)" % r["rc"], r["saida"].strip().splitlines()[-8:])
    return {"veredito": "SUBIDA VERIFICADA" if verificada else "NADA A SUBIR: o ar já era igual ao manifesto (comparado por HTTP, sha256 de cada arquivo)"}


# =================================================================== E19 — leitor de IA
def _leitores(ctx):
    return sorted((ctx.c.BANC / "revisoes").glob("leitor_ia_*_%s.md" % ctx.versao))


def leitores_ordenados(ctx):
    """[(instante, caminho, texto)] dos relatórios do leitor de IA da versão, do mais antigo ao mais novo. O instante é o do CABEÇALHO («# LEITOR-IA (R1) — dd/mm/aaaa hh:mm:ss»);
    sem ele, o mtime do arquivo."""
    out = []
    for p in _leitores(ctx):
        t = util.ler_texto(p, "replace")
        m = RE_LEITOR_T.search(t)
        i = util.instante(m.group(1)) if m else None
        out.append((i or datetime.fromtimestamp(p.stat().st_mtime), p, t))
    out.sort(key=lambda x: (x[0], x[1].name))
    return out


def _ja_e19(ctx):
    """O leitor de IA (R1): SÓ o relatório MAIS NOVO conta (um R1 antigo que passou não cobre um R1 recente que falhou) e ele tem de ser POSTERIOR à última subida verificada
    (se o ar mudou depois do relatório, o relatório não diz nada sobre o ar de hoje). Achado BAIXA do cético final, 24/10/2026."""
    if ctx.rel_espelho == "atras":
        return falta("o espelho ainda não está em %s" % ctx.versao)
    e18 = _ja_e18(ctx)
    if not e18.satisfeita:
        return falta("depende de E18 (%s)" % e18.detalhe[:140])
    rels = leitores_ordenados(ctx)
    if not rels:
        return falta("sem relatório do leitor de IA (R1: PASSA) para %s" % ctx.versao)
    t, p, texto = rels[-1]
    if "R1: PASSA" not in texto:
        linha = re.search(r"\*\*R1: [^\n]*", texto)
        return falta("o relatório MAIS NOVO do leitor de IA (%s, %s) não diz «R1: PASSA»%s (um R1 mais antigo que passou não o cobre)" % (
            p.name, util.fmt_instante(t), (": " + linha.group(0)[:110]) if linha else ""))
    lim = instante_da_subida_que_vale(ctx)
    if lim is not None and t < lim.replace(microsecond=0):          # o cabeçalho do relatório tem resolução de segundo
        return falta("o relatório MAIS NOVO do leitor de IA (%s, %s) é anterior à última subida verificada (%s): o ar mudou depois dele; o leitor precisa reler o ar" % (
            p.name, util.fmt_instante(t), util.fmt_instante(lim)))
    return aplicado("%s (%s): R1 passa%s" % (p.name, util.fmt_instante(t), ("; posterior à última subida verificada (%s)" % util.fmt_instante(lim)) if lim else ""))


def _backup_de_bytes(p):
    """Cópia de BYTES ao lado (`<arquivo>.bak_<carimbo>`), conferida; `leitor_ia.py` troca o relatório por os.replace, sem backup."""
    p = Path(p)
    bak = p.with_name(p.name + ".bak_" + util.carimbo())
    raw = util.ler_bytes(p)
    bak.write_bytes(raw)
    if bak.stat().st_size != len(raw):
        raise Parar("backup de bytes do relatório do leitor incompleto: %s" % bak.name)
    return bak


def _ap_e19(ctx):
    rel = "revisoes/leitor_ia_%s_%s.md" % (ctx.data.split("/")[2] + ctx.data.split("/")[1] + ctx.data.split("/")[0], ctx.versao)
    if (ctx.c.BANC / rel).is_file():           # a mesma data: o leitor troca o arquivo sem guardar o anterior (a regra do backup imediato é nossa)
        _backup_de_bytes(ctx.c.BANC / rel)
    r = _banc(ctx, "leitor_ia.py", "--relatorio", rel)
    if r["rc"] != 0:
        raise Parar("leitor de IA reprovou (rc %s)" % r["rc"], r["saida"].strip().splitlines()[-6:])
    return {"relatorio": rel}


def passos(ctx):
    return [
        Passo("E13", 1, "site: dados literais do selo", _ja_e13, aplicar=_ap_e13, pre=_pre_e13, conferir=_conf_e13, fase="B", escreve="SITE\\index.html, SITE\\i18n.js"),
        Passo("E14", 1, "site: aplicar o selo ao index", _ja_e14, aplicar=_ap_e14, fase="B", escreve="SITE\\index.html"),
        Passo("E15", 1, "site: corpo inteiro e gêmeo Markdown", _ja_e15, aplicar=_ap_e15, fase="B", escreve="SITE\\llms-full.txt, SITE\\index.md, SITE\\estado.json, SITE\\estado.txt, SITE\\read-brief.txt"),
        Passo("E16", 1, "site: sitemap e manifesto de subida", _ja_e16, aplicar=_ap_e16, conferir=_conf_e16, fase="B", escreve="SITE\\sitemap.xml, BANC\\revisoes\\manifesto_vN.json"),
        Passo("E17", 1, "site: subida em ensaio (conjunto esperado)", _ja_e17, aplicar=_ap_e17, fase="B", rede=True, escreve="BANC\\subidas\\<stamp>_dryrun\\RELATORIO.md"),
        Passo("E18", 1, "site: subida", _ja_e18, aplicar=_ap_e18, externo=True, fase="B", rede=True, escreve="o ar (SFTP) + BANC\\subidas\\<stamp>\\"),
        Passo("E19", 1, "site: leitor de IA (R1)", _ja_e19, aplicar=_ap_e19, fase="B", rede=True, escreve="BANC\\revisoes\\leitor_ia_<data>_vN.md"),
    ]
