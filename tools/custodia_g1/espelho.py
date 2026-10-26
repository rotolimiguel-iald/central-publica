# -*- coding: utf-8 -*-
"""Perna 1a — o ESPELHO `the_boundary` (E00..E12). Cada passo: (marca de «já aplicado», pré, aplicar, conferir).
Mapa para a ESPEC_ESPELHO: E01 passo zero · E02+E03 (conferir e copiar) viram E03 · E04 geradores (prosa por molde) · E05 ESTADO_ATUAL ·
E06 portas nº 1 (com a varredura de sensíveis BLOQUEANTE, L09) · E07+E08 viram E08 (laço portas ⇄ README ⇄ geradores do site até o
PONTO FIXO e o AUDITOR de números citados, L04) · E09 verificações · E10 commit · E11 push · E12 pós-push.

Os geradores fixos do espelho e da bancada continuam sendo os de hoje (gerar_portas, gerar_readme_frente, ...): G1 os chama com o
código de saída À VISTA e os gates que eles não têm (verificar_portas ganha código de saída por leitura da saída — L08)."""
import os
import re
import time
from pathlib import Path

from . import espelho_pares as EP
from . import nos, recibos, textos, util
from .motor import Passo, aplicado, bloqueado, falta, superado, superado_rel, indeterminado, na, operador
from .util import Parar, FalhaLeitura, Divergencia

SENSIVEIS = re.compile(r"\.bak|\.tmp|\.env|auth\.json|\.pem$|\.key$|iald_stack_v7|iald_psion_state", re.I)
CANDIDATAS_CITADAS = ("TB:read-brief.md", "SITE:read-brief.md", "SITE:llms.txt", "SITE:llms-full.txt", "SITE:index.md", "TB:llms.txt")


# =================================================================== utilidades da perna
def _py(ctx):
    return str(ctx.c.PYTHON)


def _tb(ctx, script, *args, timeout=1800):
    return util.rodar([_py(ctx), "-X", "utf8", "tools/" + script] + list(args), cwd=ctx.c.TB, timeout=timeout)


def _banc(ctx, script, *args, timeout=1800):
    return util.rodar([_py(ctx), "-X", "utf8", "tools/" + script] + list(args), cwd=ctx.c.BANC, timeout=timeout)


def exigir_rc0(r, rotulo):
    if r["rc"] != 0:
        raise Parar("%s falhou (rc %s)" % (rotulo, r["rc"]), [l for l in r["saida"].strip().splitlines()[-8:]])
    return r


def _diario(ctx):
    return ctx.memo("diario_blocos", lambda: nos.blocos_do_diario(ctx.c))


def _historica(ctx):
    return ctx.rel_espelho == "adiante"


def _commit_da_custodia(repo, v):
    """O commit `custodia(vN): ...` mais recente no repositório, ou None. Aceita a custódia CONJUNTA (`custodia(v393+v394)`). Erro de git é FalhaLeitura
    (nunca «sem commit»)."""
    return util.commit_da_custodia(repo, v)


def _tree_limpa(repo):
    """O `git status` (vazio = árvore limpa). Se o git falha, levanta FalhaLeitura: falha de leitura NUNCA vira «árvore limpa»."""
    return util.git(repo, "status", "--porcelain", "--untracked-files=no")


# =================================================================== E00 — gatilho
def _ja_e00(ctx):
    m = ctx.nos_marcas
    if m.estado in ("PRONTA", "SUPERADA"):
        return aplicado("as três marcas de %s: %s%s" % (ctx.versao, m.estado, ("; em obra no Nós: " + ", ".join(m.em_obra_versoes)) if m.em_obra_versoes else ""))
    return falta("; ".join(m.faltam))


def _ap_e00(ctx):
    nos.exigir_pronta(ctx.c, ctx.versao)
    return {"estado": ctx.nos_marcas.estado}


# =================================================================== E01 — passo zero: backup de BYTES do que ESTÁ no espelho
AMOSTRA_DO_BACKUP = 48        # quantos arquivos da lista do manifesto têm o sha256 reconferido: os CRÍTICOS sempre + passos regulares pela lista ordenada
CRITICOS_DO_BACKUP = ("um.py", "um_absoluto_selo.json", "um_absoluto.json", "Lean/tgl_kernel_proof_manifest.json")


def _com_prefixo_longo(p):
    """O caminho absoluto com o prefixo de caminho longo do Windows: as fontes pinadas do espelho passam de 250 caracteres."""
    s = os.path.abspath(str(p))
    return ("\\\\?\\" + s) if os.name == "nt" and not s.startswith("\\\\?\\") else s


def conferir_backup(b, m, P, pin16):
    """O `BACKUP_MANIFEST.json` é AUTODECLARADO («conferido_contra_origem: true» é só uma frase): aqui o CONTEÚDO é conferido (achado BAIXA do cético final, 24/10/2026).
    (a) a lista do manifesto tem n_arquivos itens, todos existem na pasta com o tamanho declarado e nada sobra na pasta; (b) o sha256 de uma AMOSTRA (os críticos + passos regulares) é o
    do manifesto; (c) o selo DENTRO do backup diz que é a versão P, com o pino do diário, e cada artefato selado que o backup traz tem o sha256 do selo (âncora que não depende do manifesto).
    Devolve (erro | None, detalhe)."""
    arqs = m.get("arquivos")
    if not isinstance(arqs, dict) or not arqs:
        return "o BACKUP_MANIFEST.json não traz a lista de arquivos com sha256 (autodeclarado, não conferível)", ""
    if m.get("n_arquivos") != len(arqs):
        return "n_arquivos (%s) != itens da lista do manifesto (%d)" % (m.get("n_arquivos"), len(arqs)), ""
    base = _com_prefixo_longo(b)
    presentes = {}
    for raiz, _dirs, files in os.walk(base):
        for fn in files:
            full = os.path.join(raiz, fn)
            presentes[os.path.relpath(full, base).replace(os.sep, "/")] = os.path.getsize(full)
    presentes.pop("BACKUP_MANIFEST.json", None)
    faltam = sorted(r for r in arqs if r not in presentes)
    tam = sorted(r for r, a in arqs.items() if r in presentes and presentes[r] != a.get("bytes"))
    sobram = sorted(r for r in presentes if r not in arqs)
    if faltam or tam or sobram:
        return ("o backup não bate com o próprio manifesto: %d faltam (ex.: %s), %d com tamanho diferente (ex.: %s), %d sobram na pasta (ex.: %s)" % (
            len(faltam), ", ".join(faltam[:2]) or "-", len(tam), ", ".join(tam[:2]) or "-", len(sobram), ", ".join(sobram[:2]) or "-")), ""
    rels = sorted(arqs)
    amostra = [r for r in CRITICOS_DO_BACKUP if r in arqs]
    passo = max(1, len(rels) // AMOSTRA_DO_BACKUP)
    amostra += [r for r in rels[::passo] if r not in amostra][: max(0, AMOSTRA_DO_BACKUP - len(amostra))]
    ruins = [r for r in amostra if util.sha256_arquivo(os.path.join(base, r.replace("/", os.sep))) != arqs[r].get("sha256")]
    if ruins:
        return "o sha256 de %d dos %d arquivos da amostra difere do manifesto (ex.: %s)" % (len(ruins), len(amostra), ", ".join(ruins[:3])), ""
    sp = b / "um_absoluto_selo.json"
    if not sp.is_file():
        return "o backup não traz o um_absoluto_selo.json (a âncora de conteúdo da versão %s)" % P, ""
    selo = util.ler_json(sp)
    if selo.get("um_version") != P:
        return "o selo DENTRO do backup diz %s, não %s" % (selo.get("um_version"), P), ""
    if str((selo.get("sha256") or {}).get("um.py", ""))[:16] != pin16:
        return "o pino do selo dentro do backup (%s) != o sha16 do diário (%s)" % (str((selo.get("sha256") or {}).get("um.py", ""))[:16], pin16), ""
    selados, divergem = 0, []
    for nome, h in (selo.get("sha256") or {}).items():
        sub = EP.DESTINO_SELADOS.get(nome)
        q = (b / sub / nome) if sub else (b / nome)
        if q.is_file():
            selados += 1
            if util.sha256_arquivo(q) != h:
                divergem.append(nome)
    if divergem:
        return "artefato selado do backup difere do sha256 do selo dele: %s" % ", ".join(divergem[:4]), ""
    return None, "lista e tamanhos conferem (%d arquivos); sha256 de uma amostra de %d arquivos e de %d selados confere" % (len(arqs), len(amostra), selados)


def backup_valido(ctx, P):
    c = ctx.c
    pin = _diario(ctx).get(P)
    if not pin or not pin.pin16:
        return None, "sha16 de %s não achado no diário" % P
    bks = sorted(c.BK.glob("um_%s_*" % P)) if c.BK.is_dir() else []
    if len(bks) != 1:
        return None, "esperava 1 pasta um_%s_* em %s, achei %d" % (P, c.BK, len(bks))
    b = bks[0]
    mf = b / "BACKUP_MANIFEST.json"
    if not mf.is_file():
        return None, "sem BACKUP_MANIFEST.json em %s" % b.name
    m = util.ler_json(mf)
    if not (m.get("conferido_contra_origem") is True and m.get("versao") == P):
        return None, "manifesto de %s não confere (conferido_contra_origem/versao)" % b.name
    if util.sha16(b / "um.py") != pin.pin16:
        return None, "o um.py do backup não bate com o sha16 do diário para %s" % P
    erro, det = ctx.memo("backup_conferido_" + b.name, lambda: conferir_backup(b, m, P, pin.pin16))
    if erro:
        return None, "o backup %s não confere com o próprio manifesto: %s" % (b.name, erro)
    return b, "%s (%s arquivos; %s)" % (b.name, m.get("n_arquivos"), det)


def _ja_e01(ctx):
    b, det = backup_valido(ctx, ctx.anterior_espelho)
    return aplicado(det) if b else falta(det)


def _pre_e01(ctx):
    c, P = ctx.c, ctx.anterior_espelho
    f = []
    pin = _diario(ctx).get(P)
    if not pin:
        return ["sha16 de %s não achado no diário — PARAR" % P]
    if ctx.rel_espelho != "atras":
        f.append("o espelho não está atrás de %s (está em %s): o passo zero é ANTES da cópia" % (ctx.versao, ctx.selo_espelho.get("um_version")))
    pe = util.sha16(c.ESP / "um.py")
    if pe != ctx.selo_espelho["sha256"]["um.py"][:16] or pe != pin.pin16:
        f.append("um.py do espelho (%s) != selo do espelho / diário (%s) — PARAR" % (pe, pin.pin16))
    for pu in EP.PULADAS:
        if list(c.BK.glob("um_%s_*" % pu)):
            f.append("existe pasta de semente da %s — não deveria" % pu)
    return f


def _ap_e01(ctx):
    c, P = ctx.c, ctx.anterior_espelho
    pin16 = _diario(ctx)[P].pin16
    dest = c.BK / ("um_%s_%s" % (P, pin16))
    man = {"versao": P, "um_py_sha16": pin16, "origem": str(c.ESP), "data_backup": util.agora_iso(),
           "regra": "backup byte a byte da versão que ESTAVA no espelho, ANTES de sobrescrever (custódia %s; molde da custódia %s)" % (ctx.versao, P),
           "gerador": "Central de Patentes/tools/custodia_g1 (passo E01)", "excluidos": ["PORTA.md", "PORTA.json", "bancada/", "cache/"], "arquivos": {}}
    n = 0
    for src in sorted(c.ESP.rglob("*")):
        if not src.is_file():
            continue
        rel = src.relative_to(c.ESP).as_posix()
        if rel.split("/")[-1] in ("PORTA.md", "PORTA.json") or rel.startswith(("bancada/", "cache/")):
            continue
        util.copiar_bytes(src, dest / rel)
        man["arquivos"][rel] = {"bytes": src.stat().st_size, "sha256": util.sha256_arquivo(src)}
        n += 1
    div = [r for r, m in man["arquivos"].items() if util.sha256_arquivo(dest / r) != m["sha256"]]
    man["n_arquivos"], man["conferido_contra_origem"] = n, (len(div) == 0)
    util.escrever_json(dest / "BACKUP_MANIFEST.json", man, backup=False)
    if div:
        raise Parar("backup do passo zero diverge da origem", div[:10])
    return {"backup": dest.name, "arquivos": n}


def _conf_e01(ctx):
    b, det = backup_valido(ctx, ctx.anterior_espelho)
    return [] if b else [det]


# =================================================================== E03 — espelho: conferir e copiar
def _ja_e03(ctx):
    c, v = ctx.c, ctx.versao
    rel = ctx.rel_espelho
    if rel == "atras":
        return falta("o espelho está em %s; falta copiar a %s" % (ctx.selo_espelho.get("um_version"), v))
    if rel == "adiante":
        tracos = [("rodadas/rodada_%s_stdout.txt" % v), ("diferencas_%s" % v), ("recibos_bancada_%s" % v)]
        falt = [t for t in tracos if not (c.ESP / t).exists()]
        rp = c.BANC / "revisoes" / ("custodia_%s_espelho.json" % v)
        if falt:
            return falta("versão histórica sem rastro no espelho: %s" % ", ".join(falt))
        # a PROVA (achado dos céticos): os blobs do commit custodia(vN) do espelho têm os mesmos bytes do cofre (um.py, selo, core, manifesto de prova)
        h = _commit_da_custodia(c.TB, v)
        cof = c.cofre(v)
        if h and cof.is_dir():
            base = c.ESP.relative_to(c.TB).as_posix()
            ok, ruins = [], []
            for rel_esp, rel_cof in (("um.py", "um.py"), ("um_absoluto_selo.json", "um_absoluto_selo.json"), ("um_absoluto.json", "um_absoluto.json"),
                                     ("Lean/tgl_kernel_proof_manifest.json", "tgl_kernel_proof_manifest.json")):
                if not (cof / rel_cof).is_file():
                    continue
                (ok if util.git_blob_sha256(c.TB, h, base + "/" + rel_esp) == util.sha256_arquivo(cof / rel_cof) else ruins).append(rel_cof)
            if ruins:
                return bloqueado("os blobs do commit %s do espelho DIFEREM dos bytes do cofre %s: %s" % (h[:8], cof.name, ", ".join(ruins)))
            if ok:
                return superado("espelho em %s; os blobs do commit %s (%s) têm os bytes do cofre %s; rastros de %s presentes%s" % (
                    ctx.selo_espelho["um_version"], h[:8], ", ".join(ok), cof.name, v, "; relatório " + rp.name if rp.is_file() else ""))
        return superado_rel("espelho em %s; rastros de %s presentes (rodada, diferenças, recibos) — sem commit/cofre para comparar os blobs%s" % (
            ctx.selo_espelho["um_version"], v, "; relatório " + rp.name if rp.is_file() else ""))
    if not ctx.corrente:
        return indeterminado("o Nós já não está em %s" % v)
    P = EP.montar_pares(ctx)
    if P.faltas:
        return falta("insumos ausentes: %s" % "; ".join(P.faltas[:3]))
    barr = _barrados_do_relatorio(ctx)
    pend, tot = EP.comparar(P, profundo=("SELADO",), barrados=barr)        # existe+tamanho em tudo; sha256 nos selados (o que o selo lista)
    ruim, orf = EP.comparar_kernel(ctx, P, profundo=True)                  # kernel: sha256 de cada arquivo formal (≈0,3 s)
    # 25/10/2026: o TÚNEL é pasta VIVA; com o espelho na versão, o que entrou ou mudou nele depois da cópia vai na PRÓXIMA custódia
    tun = [x for x in pend if x[2] == "TUNEL" and x[3] in ("destino ausente", "tamanho difere")] if rel == "igual" else []
    pend = [x for x in pend if x not in tun]
    if pend or ruim or orf:
        return falta("%d de %d pares por copiar/diferentes; kernel: %d faltando/diferentes, %d órfãos" % (len(pend), tot, len(ruim), len(orf)))
    return aplicado("%d pares presentes no espelho (selados e kernel conferidos por sha256; %d barrados pela guarda, ditos no relatório); kernel %d arquivos%s" % (
        tot, len(barr), len(P.kernel["fmap"]), ("; túnel vivo: %d registro(s) novo(s) desde a cópia, para a próxima custódia" % len(tun)) if tun else ""))


def _barrados_do_relatorio(ctx):
    p = ctx.c.BANC / "revisoes" / ("custodia_%s_espelho.json" % ctx.versao)
    if not p.is_file():
        return []
    try:
        return [b["arquivo"] for b in util.ler_json(p).get("varredura_privada", {}).get("barrados", [])]
    except (FalhaLeitura, KeyError, TypeError):
        return []


def _pre_e03(ctx):
    c = ctx.c
    f = []
    if ctx.rel_espelho != "atras":
        f.append("o espelho não está atrás de %s" % ctx.versao)
    if _tree_limpa(c.TB):
        f.append("a árvore do espelho não está limpa (meio-trabalho alheio entraria no commit): %s" % _tree_limpa(c.TB)[:120])
    h, o = util.git(c.TB, "rev-parse", "HEAD"), util.git(c.TB, "rev-parse", "origin/main")
    if h != o:
        f.append("HEAD do espelho (%s) != origin/main (%s)" % (h[:8], o[:8]))
    b, det = backup_valido(ctx, ctx.anterior_espelho)
    if not b:
        f.append("passo zero: " + det)
    if not ctx.leitura and not (Path.home() / ".iald_privado" / "marcadores_privado.json").is_file():      # no plano (leitura) nem se toca no que é privado
        f.append("conjunto privado de marcadores ausente (a guarda de 7 termos sozinha é fraca)")
    return f


def _gates_do_selo(ctx):
    """G-esp-1..G-esp-12 (ESPEC_ESPELHO §E03): selo confere com o disco, autoteste, rodada COMPLETA, gate idêntico, kernel confere."""
    c, v = ctx.c, ctx.versao
    selo, selo_esp = ctx.selo_nos, ctx.selo_espelho
    if selo.get("fail_closed_selftest") != "FAIL_CLOSED_SELFTEST_PASSED":
        raise Parar("autoteste não passou — PARAR")
    arts, div = nos.artefatos_selados(c)
    if div:
        raise Parar("selo != disco do Nós", div)
    rc = selo.get("rite_checkpoints") or {}
    if not (rc.get("switch_on") is False and rc.get("reused") == 0):
        raise Parar("NÃO é rodada COMPLETA", [str(rc)])
    gate, gate_esp = str(selo.get("qg_closure_verdict")), str(selo_esp.get("qg_closure_verdict"))
    if gate != gate_esp:
        raise Parar("O GATE MUDOU em relação ao espelho — PARAR E AVISAR O OPERADOR (o gate não se move por custódia)", [gate_esp, gate])
    confirmados = [k for k, x in selo.items() if isinstance(x, str) and re.search(r"(?<![A-Za-z])(?<!NOT_)(?<!NEVER_)CONFIRMED", x) and k.endswith("_verdict")]
    if confirmados:      # L09(b): o relatório só imprimia; agora BLOQUEIA (nenhum veredito do selo diz CONFIRMED)
        raise Parar("campos do selo com a palavra CONFIRMED (ler um a um antes de publicar)", confirmados)
    man = util.ler_json(c.NOS / "tgl_kernel_proof_manifest.json")
    fmap, ar = man["formal_files_sha256"], man["axiom_report"]
    sujos = sum(1 for x in ar.values() if set(x or []) - set(nos.TRIO))
    kfalta = [n for n, h in fmap.items() if not (c.NOS / "tgl_kernel" / n).is_file() or util.sha256_arquivo(c.NOS / "tgl_kernel" / n) != h]
    if kfalta or sujos:
        raise Parar("kernel não confere", ["%d arquivos ausentes/divergentes, %d declarações fora do trio" % (len(kfalta), sujos)])
    old = util.ler_json(c.ESP / "Lean" / "tgl_kernel_proof_manifest.json")
    ofmap, oar = old["formal_files_sha256"], old["axiom_report"]
    teor = nos.escada_do_stdout(c, v)
    if teor is None:
        raise Parar("«teoremas limpos: a/b» não achado no stdout da rodada")
    a, b = teor.split("/")
    if a != b:
        raise Parar("teoremas limpos não fecham: %s" % teor)
    core = util.ler_json(c.NOS / "um_absoluto.json").get("core") or {}
    core_esp = util.ler_json(c.ESP / "um_absoluto.json").get("core") or {}
    kf, kf_esp = core.get("kernel_formalization") or {}, core_esp.get("kernel_formalization") or {}
    flags = {k: x for k, x in kf.items() if k.startswith(("gpf_", "gpi_", "qgf_"))}
    flags_esp = {k: x for k, x in kf_esp.items() if k.startswith(("gpf_", "gpi_", "qgf_"))}
    return {"pin16": selo["sha256"]["um.py"][:16], "pin": selo["sha256"]["um.py"], "bytes_um_py": (c.NOS / "um.py").stat().st_size, "timestamp": selo.get("timestamp"),
            "result_hash": selo.get("result_hash"), "gate": gate, "gate_identico_ao_espelho": True, "rodada": rc, "teoremas_limpos": teor,
            "campos_com_CONFIRMED_a_ler": confirmados,
            "bandeiras": {"total": len(flags), "ligadas": sorted(k for k, x in flags.items() if x is True), "apagadas": sorted(k for k, x in flags.items() if x is False),
                          "mudaram_desde_o_espelho": sorted(k for k in set(flags) | set(flags_esp) if flags.get(k) != flags_esp.get(k))},
            "kernel": {"formais": len(fmap), "termos": len(ar), "fora_do_trio": sujos, "formais_espelho": len(ofmap), "termos_espelho": len(oar),
                       "novos": sorted(set(fmap) - set(ofmap)), "removidos": sorted(set(ofmap) - set(fmap)),
                       "alterados": sorted(n for n in set(fmap) & set(ofmap) if fmap[n] != ofmap[n])},
            "selo_esp_campos_novos": sorted(set(selo) - set(selo_esp))}, man


def _nao_levados(ctx):
    """Dicionário `nao_levados` = o do relatório da custódia anterior + UMA entrada gerada desta versão (L19: nenhuma chave cita v395..v397 hoje)."""
    c, v = ctx.c, ctx.versao
    base = {}
    prev = [p for p in (c.BANC / "revisoes").glob("custodia_v*_espelho.json") if p.name != "custodia_%s_espelho.json" % v]
    prev = sorted(prev, key=lambda p: util.versao_num(re.search(r"(v\d+)", p.name).group(1)))
    prev = [p for p in prev if util.versao_num(re.search(r"(v\d+)", p.name).group(1)) < ctx.n]
    if prev:
        try:
            base = dict(util.ler_json(prev[-1]).get("nao_levados") or {})
        except FalhaLeitura:
            base = {}
    base["HANDOFF_%s_CUSTODIA.md" % v] = "documento de trabalho; fica no Nós e no cofre da Central (um_unificado_%s)" % v
    return base


def _ap_e03(ctx):
    c, v = ctx.c, ctx.versao
    priv = EP.carregar_marcadores_privados()
    P = EP.montar_pares(ctx)
    if P.faltas:
        raise Parar("insumos do espelho ausentes", P.faltas)
    R = {"gerado_em": util.agora_iso(), "versao": v, "modo": "copiar"}
    bk, _ = backup_valido(ctx, ctx.anterior_espelho)
    bm = util.ler_json(bk / "BACKUP_MANIFEST.json")
    R["passo_zero"] = {"backup": bk.name, "n_arquivos": bm["n_arquivos"], "pulada": list(EP.PULADAS),
                       "guarda": {"termos_da_casa": len(EP.GUARDA), "marcadores_privados": len(priv)}}
    R["selo"], man = _gates_do_selo(ctx)
    fmap = man["formal_files_sha256"]
    # varredura de material privado: nenhum termo-guarda a MAIS que no espelho em artefato do programa
    barrados, varridos = [], 0
    for src, dst, tipo in P.lista:
        if src.suffix.lower() == ".pdf":
            continue
        nn = EP.guarda_conta(src, priv)
        nv = EP.guarda_conta(dst, priv) if dst.is_file() else 0
        varridos += 1
        if nn and nn > (nv or 0):
            barrados.append({"arquivo": str(src), "tipo": tipo, "ocorrencias_novo": nn, "ocorrencias_espelho": nv})
    R["varredura_privada"] = {"termos_da_casa": [g.pattern for g in EP.GUARDA], "marcadores_privados": "%d (padroes nao gravados)" % len(priv),
                              "arquivos_varridos": varridos, "barrados": barrados}
    criticos = [b for b in barrados if b["tipo"] not in ("TUNEL", "FONTE_TUNEL")]
    if criticos:
        raise Parar("termo-guarda cresceu em artefato do programa — PARAR E AVISAR O OPERADOR", [b["arquivo"] for b in criticos])
    barr = {b["arquivo"] for b in barrados}
    cont = {}
    for src, dst, tipo in P.lista:
        if str(src) in barr:
            continue
        if util.copiar_bytes(src, dst):
            cont[tipo] = cont.get(tipo, 0) + 1
    selo = ctx.selo_nos
    for nome, esp in selo["sha256"].items():
        sub = EP.DESTINO_SELADOS.get(nome)
        d = (c.ESP / sub / nome) if sub else (c.ESP / nome)
        if util.sha256_arquivo(d) != esp:
            raise Parar("cópia selada diverge: " + nome)
    K_DST = c.ESP / "Lean" / "tgl_kernel"
    kd = 0
    for nome, hh in fmap.items():
        d_ = K_DST / nome
        if not d_.is_file() or util.sha256_arquivo(d_) != hh:
            util.copiar_bytes(c.NOS / "tgl_kernel" / nome, d_)
            kd += 1
    for extra in EP.KERNEL_EXTRAS:
        if (c.NOS / "tgl_kernel" / extra).is_file():
            util.copiar_bytes(c.NOS / "tgl_kernel" / extra, K_DST / extra)
    orf = []
    for p in list(K_DST.rglob("*.lean")):
        rel = p.relative_to(K_DST).as_posix()
        if rel not in fmap and rel not in ("TGL.lean", "TGLExt.lean"):
            p.unlink()                         # órfão: o git guarda a história (como no script de hoje)
            orf.append(rel)
    if util.sha16(c.ESP / "um.py") != ctx.selo_nos["sha256"]["um.py"][:16]:
        raise Parar("um.py do espelho != pino do selo depois da cópia")
    for e in P.fontes_mapa:
        if e.get("publicado") and e["caminho_exigido_pelo_um_py"] in barr:
            e.update({"publicado": False, "motivo": "barrado pela varredura de material privado (termo-guarda)", "caminho_no_espelho": None})
    (c.ESP / "fontes_pinadas").mkdir(parents=True, exist_ok=True)
    mapa = {"gerado_em": util.agora_iso(), "um_py_pin": selo["sha256"]["um.py"],
            "leia": "O um.py relê cada fonte pelo caminho absoluto em caminho_exigido_pelo_um_py e confere sha256 e bytes; para reproduzir os registros (v392 em diante) em outra "
                    "máquina, copie cada arquivo de caminho_no_espelho para esse caminho. Sem isso o registro diz NOT_SEALED_THIS_RUN (fail-closed), por desenho.",
            "n_fontes": len(P.fontes_mapa), "n_publicadas": sum(1 for e in P.fontes_mapa if e.get("publicado")), "fontes": P.fontes_mapa}
    util.escrever_json(c.ESP / "fontes_pinadas" / "MAPA_FONTES_PINADAS.json", mapa, backup=False)
    R["fontes_pinadas"] = {"n": len(P.fontes_mapa), "publicadas": mapa["n_publicadas"], "fora": [(e["chave"], e["motivo"]) for e in P.fontes_mapa if not e.get("publicado")]}
    R["copiados"], R["kernel_copiados"], R["kernel_orfaos_removidos"] = cont, kd, orf
    R["nao_levados"] = _nao_levados(ctx)
    util.escrever_json(c.BANC / "revisoes" / ("custodia_%s_espelho.json" % v), R, backup=True)
    return {"copiados": cont, "kernel_copiados": kd, "orfaos": len(orf), "barrados": len(barrados)}


def _conf_e03(ctx):
    P = EP.montar_pares(ctx)
    pend, _ = EP.comparar(P, profundo=True, barrados=_barrados_do_relatorio(ctx))
    ruim, orf = EP.comparar_kernel(ctx, P, profundo=True)
    f = ["%s: %s" % (m, str(s)[-70:]) for s, d, tp, m in pend[:8]]
    return f + (["kernel diverge: %s" % ruim[:5]] if ruim else []) + (["órfãos do kernel: %s" % orf[:5]] if orf else [])


# =================================================================== E04 — geradores: a prosa da versão (molde + handoff)
_ESTADO_ANCORA = re.compile(r'    L\.append\(""\)\n    L\.append\("## What is PROVED[^\n]*\n')

_BLOCO_ESTADO = r'''    # custódia @V@ (@DATA@, sessão @SESSAO@ da Central): ao lado; sha16 e rito LIDOS do diário; o parágrafo pronto do handoff, verbatim; os quadros anteriores ficam onde estão
    L.append("")
    L.append("### @V@ · the custody `[REAL — sha16 and rite read from MEMORIA_DA_LINHAGEM.md]`")
    L.append("")
    L.append("| version | `um.py` sha16 | rite | round | what entered |")
    L.append("|---|---|---|---|---|")
    mm@N@ = re.search(r"^## [^\n]*\*\*@V@ SELADA[^*\n]*\*\*[^\n]*\n", diario, re.M)
    if mm@N@:
        fim@N@ = diario.find("\n## ", mm@N@.end())
        bl@N@ = diario[mm@N@.end(): fim@N@ if fim@N@ > 0 else len(diario)]
        sh@N@ = re.findall(r"`um\.py` sha16 `([0-9a-f]{16})`", bl@N@) or re.findall(r"`([0-9a-f]{16})`", mm@N@.group(0))
        ri@N@ = re.findall(r"\*\*(\d+)/(\d+)\*\*", bl@N@)
        L.append("| @V@ | `%s` | %s | COMPLETE | %s |" % (sh@N@[-1] if sh@N@ else "?", ("%s/%s" % ri@N@[-1]) if ri@N@ else "?", @TXT@))
    L.append("")
    L.append(@NOTA@)
    L.append("")
    L.append(@ERR@)
'''


def bloco_gerar_estado(ctx, T, fonte_py):
    """O trecho de código que entra em `gerar_estado_atual.py` (a forma do remendo da v398, gerada do molde). Os parágrafos do handoff
    entram UMA vez cada: já presente e idêntico = pula; presente e diferente = PARA (L05)."""
    s = _BLOCO_ESTADO
    for k, val in (("@V@", ctx.versao), ("@N@", str(ctx.n)), ("@DATA@", ctx.data), ("@SESSAO@", ctx.sessao), ("@TXT@", repr(T.txt_en.texto)),
                   ("@NOTA@", repr(T.nota_en.texto)), ("@ERR@", repr(T.err_en.texto))):
        s = s.replace(k, val)
    for ident, bloco in T.paragrafos:
        if repr(bloco) in fonte_py:
            continue
        if ("INICIO_" + ident) in fonte_py:
            raise Parar("o bloco %s já está no gerador do ESTADO com texto DIFERENTE do handoff — decisão da gerência (errata ao lado)" % ident)
        s += '    L.append("")\n    L.append(%s)\n' % repr(bloco)
    return s


def _marcas_e04(ctx):
    c, v, n = ctx.c, ctx.versao, ctx.n
    m = {}
    gea = util.ler_texto(c.TB / "tools" / "gerar_estado_atual.py")
    m["gerar_estado_atual"] = ("custódia %s (" % v) in gea
    m["LEDGER"] = ("### The custody — %s (COMPLETE round)" % v) in ctx.ler(c.TB / "LEDGER.md")
    m["arco_json"] = (c.BANC / "revisoes" / ("arco_%s_texto.json" % v)).is_file()
    m["index.html"] = ('data-i18n="art.c.cl.arc%d"' % n) in ctx.ler(c.SITE / "index.html")
    m["i18n.js"] = ("'art.c.cl.arc%d'" % n) in ctx.ler(c.SITE / "i18n.js")
    if not _historica(ctx):
        m["CITATION"] = ("(%s on" % v) in ctx.ler(c.TB / "CITATION.cff")
    return m


def _ja_e04(ctx):
    if ctx.rel_espelho == "atras":
        return falta("o espelho ainda não recebeu a cópia (E03)")
    m = _marcas_e04(ctx)
    faltam = [k for k, ok in m.items() if not ok]
    return aplicado("as %d marcas presentes (%s)" % (len(m), ", ".join(sorted(m)))) if not faltam else falta("faltam: %s" % ", ".join(faltam))


def _sem_commit(ctx, quem):
    h = _commit_da_custodia(ctx.c.TB, ctx.versao)
    if h:
        return ["o commit custodia(%s) (%s) já existe: %s regenera arquivos já commitados — reparar o espelho DEPOIS do commit é uma errata ao lado, "
                "decisão da gerência; G1 não o faz sozinho" % (ctx.versao, h[:8], quem)]
    return []


def _pre_e04(ctx):
    f = _sem_commit(ctx, "E04")
    if ctx.rel_espelho == "atras":
        f.append("rode antes o E03 (cópia)")
    a = textos.avaliar_fontes(ctx)
    f += a["bloqueios"]
    if a["faltam"] and not ctx.aceitar_molde:
        f.append("o handoff não traz estes marcadores (a prosa sairia do molde factual; passe --aceitar-molde ou peça ao autor do handoff): %s" % ", ".join(a["faltam"]))
    return f


def _ap_e04(ctx):
    c, v, n = ctx.c, ctx.versao, ctx.n
    T = textos.construir(ctx)
    if T.violacoes:
        raise Parar("o portão de texto reprovou", T.violacoes)
    F_ = ctx.fatos
    dep = textos.deposito_zenodo(c)
    ts = util.carimbo()
    saidas = {}
    gea = c.TB / "tools" / "gerar_estado_atual.py"
    fonte = util.ler_texto(gea)
    if not _ESTADO_ANCORA.search(fonte.replace("\r\n", "\n")) or len(_ESTADO_ANCORA.findall(fonte.replace("\r\n", "\n"))) != 1:
        raise Parar("âncora «## What is PROVED» do gerar_estado_atual.py não casou exatamente uma vez")
    anc = _ESTADO_ANCORA.search(fonte.replace("\r\n", "\n")).group(0)
    novo = bloco_gerar_estado(ctx, T, fonte)
    saidas["gerar_estado_atual"] = util.patch_bytes(gea, [(anc, novo + anc)], "custódia %s (" % v, ts=ts, rot="ESTADO")
    led = c.TB / "LEDGER.md"
    anc_led = "\n## What is closed / What remains open"
    bloco = T.bloco_ledger.texto
    saidas["LEDGER"] = util.patch_bytes(led, [(anc_led, bloco + anc_led)], "### The custody — %s (COMPLETE round)" % v, ts=ts, rot="LEDGER")
    cff = c.TB / "CITATION.cff"
    pares = textos.citation_pares(ctx, util.ler_texto(cff), F_, dep) if ("(%s on" % v) not in util.ler_texto(cff) else []
    saidas["CITATION"] = util.patch_bytes(cff, pares, "(%s on" % v, exige_crescer=False, ts=ts, rot="CITATION") if pares else {"estado": "ja_aplicado"}
    # o arco do site (index.html + i18n.js): depois do arco da versão anterior que a página já tem
    arco_json = c.BANC / "revisoes" / ("arco_%s_texto.json" % v)
    if not arco_json.is_file():
        util.escrever_json(arco_json, {"gerador": "Central de Patentes/tools/custodia_g1", "pin16": F_["pin16"], "en": T.arco_en.texto, "pt": T.arco_pt.texto,
                                       "origem": {"en": T.arco_en.origem, "pt": T.arco_pt.origem}}, backup=False)
    idx, i18 = c.SITE / "index.html", c.SITE / "i18n.js"
    html = util.ler_texto(idx)
    ks = sorted(int(x) for x in re.findall(r'data-i18n="art\.c\.cl\.arc(\d+)"', html) if int(x) < n)
    if not ks:
        raise Parar("index.html não tem nenhuma linha art.c.cl.arcK anterior à %s" % v)
    k = ks[-1]
    ant_json = c.BANC / "revisoes" / ("arco_v%d_texto.json" % k)
    if not ant_json.is_file():
        raise Parar("arco_v%d_texto.json ausente (âncora do arco anterior)" % k)
    a = util.ler_json(ant_json)
    old = '<div><span data-i18n="art.c.cl.arc%d">%s</span></div>' % (k, a["en"])
    saidas["index.html"] = util.patch_bytes(idx, [(old, old + '<div><span data-i18n="art.c.cl.arc%d">%s</span></div>' % (n, T.arco_en.texto))], 'data-i18n="art.c.cl.arc%d"' % n, ts=ts, rot="index")
    oe, op = "'art.c.cl.arc%d': '%s'" % (k, a["en"]), "'art.c.cl.arc%d': '%s'" % (k, a["pt"])
    saidas["i18n.js"] = util.patch_bytes(i18, [(oe, oe + ", 'art.c.cl.arc%d': '%s'" % (n, T.arco_en.texto)), (op, op + ", 'art.c.cl.arc%d': '%s'" % (n, T.arco_pt.texto))],
                                         "'art.c.cl.arc%d'" % n, ts=ts, rot="i18n")
    saidas["molde_usado"] = T.molde_usado
    return {k_: (v_["estado"] if isinstance(v_, dict) else v_) for k_, v_ in saidas.items()}


def _conf_e04(ctx):
    ctx._memo.pop("fatos", None)
    ctx._cache_t.clear()
    return ["marca ausente: " + k for k, ok in _marcas_e04(ctx).items() if not ok]


# =================================================================== E05 — ESTADO_ATUAL.md
def _ja_e05(ctx):
    c, v = ctx.c, ctx.versao
    if ctx.rel_espelho == "atras":
        return falta("espelho atrás de %s" % v)
    t = ctx.ler(c.TB / "ESTADO_ATUAL.md")
    tem_bloco = ("### %s · the custody" % v) in t
    if _historica(ctx):
        return superado("a página é regenerada a cada versão; o bloco de %s está nela" % v) if tem_bloco else falta("ESTADO_ATUAL.md sem o bloco ### %s · the custody" % v)
    ok = tem_bloco and ctx.pin16 in t
    return aplicado("ESTADO_ATUAL.md traz %s e o bloco da custódia (%d bytes)" % (ctx.pin16, len(t.encode("utf-8")))) if ok else falta("ESTADO_ATUAL.md sem o pino/bloco de %s" % v)


def _pre_e05(ctx):
    return _sem_commit(ctx, "E05")


def _ap_e05(ctx):
    r = exigir_rc0(_tb(ctx, "gerar_estado_atual.py"), "gerar_estado_atual.py")
    return {"ultima_linha": r["saida"].strip().splitlines()[-1][:160]}


def _conf_e05(ctx):
    ctx._cache_t.clear()
    t = ctx.ler(ctx.c.TB / "ESTADO_ATUAL.md")
    f = []
    if ctx.pin16 not in t or ("### %s · the custody" % ctx.versao) not in t:
        f.append("ESTADO_ATUAL.md não traz o pino/bloco")
    i = t.find("## Reading order")
    if i > 100000:
        ctx.aviso("L02: «Reading order» começa no caractere %d (> 100.000): a página quebra a regra que ensina (decisão estrutural pendente)" % i)
    return f


# =================================================================== E06 — varredura de sensíveis (BLOQUEANTE) + git add -A + portas nº 1
def varredura_sensiveis(repo):
    """Qualquer arquivo novo/alterado que case os padrões sensíveis. Imprimir não basta (L09): o chamador PARA."""
    out = util.git(repo, "status", "--porcelain", "--untracked-files=all")
    return [l for l in out.splitlines() if SENSIVEIS.search(l[3:])]


def _portas_ok(ctx):
    c, v = ctx.c, ctx.versao
    p = ctx.lido(c.TB / "PORTA.json").get("selo_corrente", {})
    t = ctx.lido(c.TB / "TUNEL.json").get("selo", {})
    return (p.get("versao_do_selo") == v and p.get("pin_um_py_16") == ctx.pin16 and t.get("pin_um_py_16") == ctx.pin16 and ctx.pin16 in ctx.ler(c.TB / "README.md"))


def _ja_e06(ctx):
    if ctx.rel_espelho == "atras":
        return falta("espelho atrás")
    if _historica(ctx):
        return superado_rel("PORTAS são regeradas a cada versão (G1 não tem a cópia desta versão: só o commit)")
    return aplicado("PORTA.json/TUNEL.json/README com %s" % ctx.pin16) if _portas_ok(ctx) else falta("PORTA/TUNEL/README não trazem %s" % ctx.pin16)


def _pre_e06(ctx):
    return _sem_commit(ctx, "E06")


def _pre_e08(ctx):
    return _sem_commit(ctx, "E08")


def _ap_e06(ctx):
    c = ctx.c
    s = varredura_sensiveis(c.TB)
    if s:
        raise Parar("arquivos sensíveis ou temporários no índice do espelho (nada vai ao commit)", s[:8])
    exigir_rc0(_rodar_git(ctx, "add", "-A"), "git add -A")
    r = exigir_rc0(_tb(ctx, "gerar_portas.py"), "gerar_portas.py")
    return {"portas": r["saida"].strip().splitlines()[-1][:120]}


def _rodar_git(ctx, *args):
    return util.rodar(["git", "-c", "core.quotepath=off", "-C", str(ctx.c.TB)] + list(args))


# =================================================================== E08 — o laço portas ⇄ README ⇄ geradores do site, até o PONTO FIXO
def auditar_numeros_citados(ctx):
    """L04: para cada «arquivo (N bytes)» nas superfícies publicadas, N == tamanho real. Devolve a lista de divergências."""
    c = ctx.c
    base = {"TB": c.TB, "SITE": c.SITE}
    div = []
    # «arquivo.ext (N bytes)» (read-brief, llms-full) E «[título](url/arquivo.ext) (N bytes; espelho: …)» (llms.txt, index.md): o `)` que fecha o link vem entre o nome e o «(N bytes».
    # Antes o regex exigia «bytes)» logo depois do nome e não via NENHUMA das 14 citações do llms.txt nem das 8 do index.md (o L04 da v398 estava justamente aí).
    rx = re.compile(r"([A-Za-z0-9_./%-]+\.[A-Za-z0-9]{1,5})\)?\s*\(([0-9][0-9.,]*)\s*bytes\b")
    for ref in CANDIDATAS_CITADAS:
        raiz, nome = ref.split(":", 1)
        p = base[raiz] / nome
        if not p.is_file():
            continue
        for m in rx.finditer(util.ler_texto(p, "replace")):
            alvo = m.group(1).split("/secoes/")[-1] if "/secoes/" in m.group(1) else m.group(1).rsplit("/", 1)[-1]
            rel = ("secoes/" + alvo) if "/secoes/" in m.group(1) else alvo
            cit = int(re.sub(r"[.,]", "", m.group(2)))
            cand = [base["TB"] / rel, base["SITE"] / rel]
            real = next((q.stat().st_size for q in cand if q.is_file()), None)
            if real is not None and real != cit:
                div.append({"superficie": ref, "arquivo": rel, "citado": cit, "real": real})
    return div


def rotulo_do_teste_no_readme(ctx):
    """L03: o rótulo de versão do «Unique Word Test» no README é o do REGISTRO, não o do selo corrente."""
    t = ctx.ler(ctx.c.TB / "README.md")
    m = re.search(r"Unique Word Test \((v\d+),[^)]*\)[^\n]*?registry\s+`?teste_de_veracidade_fase9_(v\d+)", t)
    if m and m.group(1) != m.group(2):
        return ["README rotula o Teste da Única Palavra como %s sobre o registro %s (gerar_readme_frente.py l.263-267, L03)" % (m.group(1), m.group(2))]
    return []


def _ja_e08(ctx):
    if ctx.rel_espelho == "atras":
        return falta("espelho atrás")
    if _historica(ctx):
        return superado_rel("README/PORTAS/geradores do site são regerados a cada versão (G1 não tem a cópia desta versão)")
    if not _portas_ok(ctx):
        return falta("PORTA/TUNEL/README não trazem %s" % ctx.pin16)
    if ("| version \u00b7 vers\u00e3o | **%s** (sealed" % ctx.versao) not in ctx.ler(ctx.c.TB / "README.md"):   # 25/10/2026: o pin16 do bloco das portas não prova a frente
        return falta("a frente do README não foi regerada para %s (linha «version · versão» da tabela ausente)" % ctx.versao)
    d = auditar_numeros_citados(ctx)
    l3 = rotulo_do_teste_no_readme(ctx)
    if d or l3:
        det = []
        if d:
            det.append("%d números citados defasados (L04): %s" % (len(d), "; ".join("%s cita %s=%s, real %s" % (x["superficie"], x["arquivo"], x["citado"], x["real"]) for x in d[:3])))
        det += l3
        return falta(" | ".join(det))
    return aplicado("portas/README/geradores no ponto fixo; 0 números citados defasados")


def _assinatura(ctx):
    c = ctx.c
    import hashlib
    h = hashlib.sha256()
    itens = [c.TB / "README.md", c.TB / "ESTADO_ATUAL.md", c.TB / "read-brief.md", c.TB / "llms.txt", c.TB / "TUNEL.json", c.TB / "TUNEL.md", c.TB / "PORTA.json", c.TB / "PORTA.md",
             c.SITE / "read-brief.md", c.SITE / "llms.txt"] + sorted((c.TB / "secoes").glob("*")) + sorted((c.SITE / "secoes").glob("*"))
    for p in itens:
        if not p.is_file():
            continue
        t = util.ler_texto(p, "replace")
        t = re.sub(r"\d{4}-\d\d-\d\d(T[\d:]+Z)?", "<D>", t)       # gerado_utc e rodapés com data: normalizados
        h.update(p.name.encode("utf-8") + b"\0" + t.encode("utf-8"))
    return h.hexdigest()[:16]


def _ap_e08(ctx):
    c = ctx.c
    sig_ant, passadas = None, []
    for i in range(1, 5):
        exigir_rc0(_banc(ctx, "gerar_secoes.py"), "gerar_secoes.py")
        exigir_rc0(_rodar_git(ctx, "add", "-A"), "git add -A")
        exigir_rc0(_tb(ctx, "gerar_portas.py"), "gerar_portas.py")
        for _ in range(3):                                          # README ⇄ portas até o README parar de mudar
            antes = util.sha256_arquivo(c.TB / "README.md", 16)
            exigir_rc0(_tb(ctx, "gerar_readme_frente.py"), "gerar_readme_frente.py")
            exigir_rc0(_rodar_git(ctx, "add", "-A"), "git add -A")
            exigir_rc0(_tb(ctx, "gerar_portas.py"), "gerar_portas.py")
            if util.sha256_arquivo(c.TB / "README.md", 16) == antes:
                break
        for g in ("gerar_read_brief.py", "gerar_llms_site.py", "gerar_head_camada_texto.py"):
            exigir_rc0(_banc(ctx, g), g)
        exigir_rc0(_rodar_git(ctx, "add", "-A"), "git add -A")
        exigir_rc0(_tb(ctx, "gerar_portas.py"), "gerar_portas.py (hash final)")
        sig = _assinatura(ctx)
        passadas.append(sig)
        if sig == sig_ant:
            return {"passadas": i, "assinatura": sig}
        sig_ant = sig
    raise Parar("o laço não convergiu em 4 passadas (arquivos oscilam)", passadas)


def _conf_e08(ctx):
    ctx._cache_t.clear()
    ctx._cache_j.clear()
    f = []
    d = auditar_numeros_citados(ctx)
    f += ["número citado defasado: %s cita %s=%s, real %s" % (x["superficie"], x["arquivo"], x["citado"], x["real"]) for x in d]
    f += rotulo_do_teste_no_readme(ctx)
    if len(ctx.ler(ctx.c.TB / "README.md").encode("utf-8")) > 40960:
        f.append("README passou do teto de 40.960 bytes (L01)")
    return f


# =================================================================== E08B — os parágrafos prontos do handoff no README (L01)
TETO_README = 40960


def _paragrafos_novos(ctx):
    h = ctx.handoff
    return [(i, b) for i, b in h.paragrafos_prontos() if i.endswith("_" + ctx.versao)] if h else []


def _ja_e08b(ctx):
    if ctx.rel_espelho == "atras":
        return falta("espelho atrás")
    if _historica(ctx):
        return superado_rel("o README é regerado a cada versão (G1 não tem a cópia desta versão)")
    novos = _paragrafos_novos(ctx)
    if not novos:
        return na("o handoff não traz parágrafo pronto NOVO desta versão (marcador PARAGRAFO_*_%s)" % ctx.versao)
    readme = ctx.ler(ctx.c.TB / "README.md")
    tam = len(readme.encode("utf-8"))
    faltando = []
    for i, b in novos:
        m = re.search(r"^###\s*(.+?)\s*(?:\u2014|-)\s*par", b, re.M) or re.search(r"^###\s*(.+)$", b, re.M)
        chave = (m.group(1).strip() if m else i)
        if chave not in readme:
            faltando.append((i, chave, len(b.encode("utf-8"))))
    if not faltando:
        return aplicado("o README traz os parágrafos prontos desta versão")
    soma = sum(x[2] for x in faltando)
    return operador("L01: o parágrafo %s (%d B) NÃO está no README (%d B de %d): %s. gerar_readme_frente.py não tem slot para ele e a frente não tem folga; a decisão é estrutural "
                    "(mover «Read in this order» para o ESTADO_ATUAL e fixar um slot «última custódia» com orçamento, ou rever o teto): do operador/gerência — G1 não corta o README"
                    % (faltando[0][0], soma, tam, TETO_README, "cabe só se o slot existir" if tam + soma <= TETO_README else "não cabe"))


# =================================================================== E09 — verificações do espelho
def verificar_espelho(ctx, detalhe=False):
    """As duas verificações do espelho. Devolve a lista de falhas (vazia = passa); com `detalhe`, (falhas, o que cada uma disse — para o recibo)."""
    r = _tb(ctx, "verificar_portas.py")
    ok_vp = bool(re.search(r"ERROS\s*\.+\s*0\b", r["saida"])) and "TODAS AS PORTAS RESOLVEM" in r["saida"]
    r2 = _tb(ctx, "guarda_do_selo.py")
    ok_gs = r2["rc"] == 0 and bool(re.search(r"ERROS\s*\.+\s*0\b", r2["saida"])) and "O QUE SE PUBLICA E O QUE O SELO DESCREVE" in r2["saida"]
    f = []
    if not ok_vp:
        f.append("verificar_portas.py: sem «ERROS … 0» e «TODAS AS PORTAS RESOLVEM» (L08: o script não tem código de saída): " + r["saida"].strip().splitlines()[-1][:100])
    if not ok_gs:
        f.append("guarda_do_selo.py reprovou (rc %s)" % r2["rc"])
    if not detalhe:
        return f
    return f, {"verificar_portas": {"rc": r["rc"], "ok": ok_vp, "ultima_linha": r["saida"].strip().splitlines()[-1][:160] if r["saida"].strip() else "",
                                    "saida_sha16": util.sha256_bytes(r["saida"].encode("utf-8"))[:16]},
               "guarda_do_selo": {"rc": r2["rc"], "ok": ok_gs, "ultima_linha": r2["saida"].strip().splitlines()[-1][:160] if r2["saida"].strip() else "",
                                  "saida_sha16": util.sha256_bytes(r2["saida"].encode("utf-8"))[:16]}}


def _ja_e09(ctx):
    """Só conta o que G1 PROVA: o recibo de verificar_portas/guarda_do_selo (com a assinatura das superfícies verificadas). O commit sozinho prova que a
    gerência confiou, não que as verificações rodaram: sem recibo vira SUPERADO_REL (dito), nunca APLICADO."""
    h = _commit_da_custodia(ctx.c.TB, ctx.versao)
    rec = recibos.ler(ctx, "E09")
    if rec and rec.get("ok") is True:
        if h or not ctx.corrente or ctx.rel_espelho != "igual":
            return aplicado("recibo de E09 (%s): verificar_portas ERROS 0 e guarda_do_selo ok%s" % (rec.get("gravado_em", "?")[:19], "; commit " + h[:8] if h else ""))
        if rec.get("assinatura") == _assinatura(ctx):
            return aplicado("recibo de E09 (%s): as verificações rodaram sobre as superfícies de hoje (mesma assinatura)" % rec.get("gravado_em", "?")[:19])
        return falta("as superfícies do espelho mudaram depois do recibo de E09 (assinatura diferente): verificar de novo")
    if h:
        return superado_rel("coberto pelo commit custodia(%s) (%s); sem recibo de G1 que prove que verificar_portas/guarda_do_selo rodaram" % (ctx.versao, h[:8]))
    return falta("verificações ainda não rodadas para o commit")


def _ap_e09(ctx):
    f, det = verificar_espelho(ctx, detalhe=True)
    if f:
        raise Parar("as verificações do espelho reprovaram", f)
    recibos.gravar(ctx, "E09", {"ok": True, "assinatura": _assinatura(ctx), "verificacoes": det})
    return {"verificar_portas": "ERROS 0", "guarda_do_selo": "ok"}


# =================================================================== E10 — commit · E11 — push · E12 — pós-push
def _ja_e10(ctx):
    h = _commit_da_custodia(ctx.c.TB, ctx.versao)
    return aplicado("commit %s" % h[:8]) if h else falta("sem commit custodia(%s): no espelho" % ctx.versao)


def _pre_e10(ctx):
    c = ctx.c
    f = []
    if util.git(c.TB, "diff", "--name-only"):
        f.append("há mudanças NÃO staged no espelho (git add -A não foi o último ato)")
    staged = util.git(c.TB, "diff", "--cached", "--name-only").splitlines()
    if not staged:
        f.append("nada staged para commitar")
    f += ["arquivo sensível staged: %s" % x for x in staged if SENSIVEIS.search(x)]
    if not ctx.leitura:                  # no plano (leitura) não se rodam os scripts de verificação: o recibo de E09 e `executar` os cobrem
        f += verificar_espelho(ctx)
    return f


def _ap_e10(ctx):
    T = textos.construir(ctx)
    if T.violacoes:
        raise Parar("o portão de texto reprovou a mensagem", T.violacoes)
    ctx.W.mkdir(parents=True, exist_ok=True)
    msg = ctx.W / ("commit_espelho_%s.txt" % ctx.versao)
    util.escrever_atomico(msg, T.commit_espelho.texto.encode("utf-8"), backup=True)
    exigir_rc0(util.rodar(["git", "-C", str(ctx.c.TB), "commit", "-q", "-F", str(msg)]), "git commit")
    return {"commit": util.git(ctx.c.TB, "log", "-1", "--format=%h %s")[:120]}


def _ja_e11(ctx):
    c = ctx.c
    h = _commit_da_custodia(c.TB, ctx.versao)
    if not h:
        return falta("sem commit para empurrar")
    if util.git_ancestral(c.TB, h, "origin/main"):
        return aplicado("commit %s contido em origin/main (ref local%s)" % (h[:8], "" if not ctx.rede else "; conferir com ls-remote"))
    return falta("commit %s ainda não está em origin/main" % h[:8])


def _ap_e11(ctx):
    exigir_rc0(util.rodar(["git", "-C", str(ctx.c.TB), "push", "origin", "main"], timeout=900), "git push origin main")
    return {"head": util.git(ctx.c.TB, "rev-parse", "--short", "HEAD")}


def _conf_e11(ctx):
    h, o = util.git(ctx.c.TB, "rev-parse", "HEAD"), util.git(ctx.c.TB, "rev-parse", "origin/main")
    return [] if h == o else ["HEAD %s != origin/main %s depois do push" % (h[:8], o[:8])]


def _raw_readme_tem_pino(ctx):
    import urllib.request
    rq = urllib.request.Request(ctx.c.RAW + "README.md", headers={"Cache-Control": "no-cache", "User-Agent": "iald-custodia-g1"})
    with urllib.request.urlopen(rq, timeout=60) as r:
        return ctx.pin16 in r.read().decode("utf-8", "replace")


def _ja_e12(ctx):
    if _historica(ctx):
        return superado_rel("o GitHub serve o espelho corrente; %s é histórica (G1 não tem o raw dela)" % ctx.versao)
    if ctx.rede:
        try:
            return aplicado("README raw traz o pino") if _raw_readme_tem_pino(ctx) else falta("README raw NÃO traz o pino (CDN velho ou push não feito)")
        except Exception as e:  # noqa: BLE001
            return indeterminado("sem leitura do raw: %r" % (e,))
    from . import quadro
    return quadro.item_do_quadro(ctx, "Espelho (GitHub raw)", "README raw traz o pino", marcos=quadro.marcos_e12(ctx))


def _ap_e12(ctx):
    ult = None
    for tentativa in range(6):
        r = _tb(ctx, "pos_push.py", timeout=900)
        ult = r
        if r["rc"] == 0:
            return {"tentativas": tentativa + 1}
        if r["rc"] == 1:
            raise Divergencia("pos_push.py: divergência real entre o GitHub e o selo", r["saida"].strip().splitlines()[-6:])
        time.sleep(60)           # rc 2 (CDN velho) ou 3 (inconclusivo): recuo e repete
    raise Divergencia("pos_push.py não convergiu em 6 tentativas (rc %s)" % ult["rc"], ult["saida"].strip().splitlines()[-6:])


# =================================================================== a lista de passos
def passos_fase_a(ctx):
    return [
        Passo("E00", 1, "gatilho: as três marcas do Nós", _ja_e00, aplicar=_ap_e00, escreve="(só leitura)"),
        Passo("E01", 1, "passo zero: backup de bytes de %s" % "P", _ja_e01, aplicar=_ap_e01, pre=_pre_e01, conferir=_conf_e01, escreve="BK\\um_vP_<pin>\\ (fora do repositório)"),
        Passo("E03", 1, "espelho: conferir e copiar", _ja_e03, aplicar=_ap_e03, pre=_pre_e03, conferir=_conf_e03, longo=True,
              escreve="ESP\\**, TB\\cache\\**, fontes_pinadas, Lean\\tgl_kernel; BANC\\revisoes\\custodia_vN_espelho.json"),
        Passo("E04", 1, "geradores: ESTADO, LEDGER, CITATION, arco do site", _ja_e04, aplicar=_ap_e04, pre=_pre_e04, conferir=_conf_e04,
              escreve="TB\\tools\\gerar_estado_atual.py, TB\\LEDGER.md, TB\\CITATION.cff, BANC\\revisoes\\arco_vN_texto.json, SITE\\index.html, SITE\\i18n.js"),
        Passo("E05", 1, "ESTADO_ATUAL.md", _ja_e05, aplicar=_ap_e05, pre=_pre_e05, conferir=_conf_e05, escreve="TB\\ESTADO_ATUAL.md"),
        Passo("E06", 1, "varredura de sensíveis, git add -A, portas nº 1", _ja_e06, aplicar=_ap_e06, pre=_pre_e06, escreve="PORTA.*, llms.txt, TUNEL.*, bloco AS PORTAS do README (índice do git)"),
        Passo("E08", 1, "laço portas ⇄ README ⇄ geradores do site (ponto fixo)", _ja_e08, aplicar=_ap_e08, pre=_pre_e08, conferir=_conf_e08, longo=True,
              escreve="README.md, PORTA/TUNEL, read-brief, llms.txt, head da camada de texto, secoes\\*"),
        Passo("E08B", 1, "parágrafos prontos do handoff no README (teto de 40 KB)", _ja_e08b, aplicar=None, escreve="(ato do operador/gerência: decisão estrutural, L01)"),
        Passo("E09", 1, "verificações: portas e guarda do selo", _ja_e09, aplicar=_ap_e09, escreve="(só leitura)"),
    ]


def passos_fase_b(ctx):
    return [
        Passo("E10", 1, "commit do espelho", _ja_e10, aplicar=_ap_e10, pre=_pre_e10, externo=True, fase="B", escreve=".git do espelho (commit local)"),
        Passo("E11", 1, "push do espelho", _ja_e11, aplicar=_ap_e11, conferir=_conf_e11, externo=True, fase="B", rede=True, escreve="GitHub (origin/main)"),
        Passo("E12", 1, "pós-push: o raw serve o que o selo descreve", _ja_e12, aplicar=_ap_e12, fase="B", rede=True, usa_quadro=True, escreve="(só leitura de rede)"),
    ]
