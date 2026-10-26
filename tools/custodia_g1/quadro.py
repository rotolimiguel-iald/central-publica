# -*- coding: utf-8 -*-
"""Perna 4 — o QUADRO e as pernas que o selo já puxa (C19, C20). O quadro (`tools\\estado_do_organismo.py`) é a MEDIDA FINAL: cada superfície
contra o selo do Nós. G1 o lê (leitura) e, em `executar`, o roda ao fim — junto com o Nós vivo (`NOS_VIVO\\construir.py`).

Mapa item do quadro -> passo (a ligação «critério = linha do quadro» do desenho do organismo), ESPEC_CENTRAL C19:
  cofre e kernel vNNN -> C3 · «runner lê o cofre» (_medir_vNNN_custodia) -> C6 · «último resultado do runner» -> C7 · VERSAO_DA_CAMADA -> C8 · «dispositivos
  com a camada» 16/16 -> C9 · «FINAL regerados depois da camada» 16/16 -> C10 · ledger -> C12 · Atlas «A CUSTÓDIA DA vNNN» -> C13 · git da Central -> C14 ·
  snapshot posterior ao selo -> C5 · Central pública -> C18 · rota custodia.vNNN -> C16 (a rota só entra DEPOIS do push e da conferência final),
  linha do MEMORY.md e handoff-vNNN-custodia.md -> C13/C16 · nos_vivo.sqlite3 -> C19 · Bancada Um, ACTIVE.json e memória científica da fila -> C20.
C20 só CONFERE (espera limitada e configurável): o selo já puxou a Bancada Um e a memória canônica da fila; G1 nunca executa nem reinicia serviço.
C21 (achado do cético final, 24/10/2026: «a perna do app não é automatizada») só CONFERE, sem construir: a release instalada no app (`iald_nucleo_fixo.json` →
`operational_core.current_release`, com o `release_source_sha256` = o pino do selo) contra a versão. Defasada = decisão do OPERADOR (código 5), com a instrução do pipeline
(`work\\iald_vNNN_<data>\\app`, fase A/B; construtor ≠ revisor; troca do serviço pelo operador). G1 nunca roda o pipeline, nunca instala, nunca reinicia o serviço.

FRESCOR DO QUADRO (achado dos céticos, 24/10/2026): decidir por um quadro VELHO deu planos diferentes para o mesmo mundo (7 pendências com o quadro das
09:32, 4 com o das 11:27). Agora toda marca que lê o quadro exige `medido_em` >= o maior entre o selo e a última modificação das superfícies DO PASSO
(os «marcos»); quadro velho vira INDETERMINADO («remedir»). Em `executar` o quadro velho é REMEDIDO antes de decidir (Passo.usa_quadro: E12 e C18; C19 remede por si), nunca em `planejar`.
O que é do OPERADOR (build/distribuição do app, depósito Zenodo, painel da hospedagem) não conta como DEFASADO de G1: vai para as decisões do operador."""
import glob
import os
import re
import time
from datetime import datetime

from . import util
from .motor import Passo, aplicado, falta, superado, superado_rel, indeterminado, operador
from .util import Parar, FalhaLeitura

MAPA_ITEM_PASSO = {"Central privada": "C3..C14", "Espelho": "E03..E12", "Espelho (GitHub raw)": "E12", "Site (fonte)": "E13..E18", "Site (ar)": "E18",
                   "Central pública": "C18", "Central pública (ar)": "C18", "Mapa de rotas": "C16", "Memória da gerência": "C13/C16", "Nós vivo": "C19",
                   "Linhagem": "(Nós)", "App (fila científica)": "C20", "App IALD (ciência própria)": "C21"}
INSTRUCAO_DO_APP = ("pipeline work\\iald_%s_<data>\\app (fase A/B; construtor ≠ revisor; troca do serviço pelo operador). "
                    "G1 só CONFERE: não constrói, não instala, não reinicia o serviço")

# superfícies cujo «DEFASADO» é DECISÃO/ATO do operador (o item do quadro diz: «build do app», «depósito é ato do operador», «painel da hospedagem»)
SUPERFICIES_DO_OPERADOR = ("App IALD (ciência própria)", "Zenodo", "iald.ia.br")


def caminho_quadro(ctx):
    return ctx.c.CEN / "organismo" / "ESTADO_DO_ORGANISMO.json"


def ler_quadro(ctx):
    p = caminho_quadro(ctx)
    return util.ler_json(p) if p.is_file() else None


def do_operador(item):
    """O item do quadro é do operador (estado PENDENTE_OPERADOR, ou superfície operada por ele)?"""
    return item.get("estado") == "PENDENTE_OPERADOR" or item.get("superficie") in SUPERFICIES_DO_OPERADOR


def classificar(q):
    """(defasados de G1, falhas de G1, do operador): DEFASADO/FALHA fora das superfícies do operador pesam para G1; as do operador vão à parte."""
    defas, falhas, ops = [], [], []
    for i in q.get("itens", []):
        if i["estado"] in ("DEFASADO", "FALHA", "PENDENTE_OPERADOR"):
            if do_operador(i):
                ops.append(i)
            elif i["estado"] == "DEFASADO":
                defas.append(i)
            elif i["estado"] == "FALHA":
                falhas.append(i)
    return defas, falhas, ops


def _txt_item(i):
    return "%s / %s: esperado %s, achado %s (%s)" % (i["superficie"], i["item"][:90], str(i.get("esperado"))[:40], str(i.get("achado"))[:40], i["estado"])


def itens_do_operador(ctx):
    """Decisões do operador que o quadro enxerga (app, Zenodo, painel). Só do quadro NÃO anterior ao selo: quadro de outra versão não fala desta."""
    q = ler_quadro(ctx)
    if not q:
        return []
    ts = util.instante(ctx.selo_nos.get("timestamp"))
    t = util.instante(q.get("medido_em"))
    if t is None or (ts is not None and t < ts):
        return []
    return [{"origem": "quadro de %s" % q.get("medido_em"), "texto": _txt_item(i)} for i in classificar(q)[2]]


# =================================================================== frescor
def fresco(q, marcos):
    """(ok, motivo): `medido_em` do quadro >= o MAIOR dos marcos [(rótulo, datetime|None)]. Marco None é ignorado. Sem `medido_em` legível = velho."""
    t = util.instante((q or {}).get("medido_em"))
    if t is None:
        return False, "o quadro não tem medido_em legível"
    ms = [(r, m) for r, m in marcos if m is not None]
    if not ms:
        return True, ""
    r, m = max(ms, key=lambda x: x[1])
    if t < m:
        return False, "o quadro (medido em %s) é anterior a %s (%s): remedir o quadro (C19)" % (util.fmt_instante(t), r, util.fmt_instante(m))
    return True, ""


def marco_selo(ctx):
    return ("ao selo", util.instante(ctx.selo_nos.get("timestamp")))


def marcos_e12(ctx):
    h = util.commit_da_custodia(ctx.c.TB, ctx.versao)
    return [marco_selo(ctx), ("ao commit do espelho", util.data_do_commit(ctx.c.TB, h) if h else None)]


def marcos_c18(ctx):
    c = ctx.c
    ms = [marco_selo(ctx), ("à última modificação de /central/ no site", util.mtime_max([c.SITE / "central"])),
          ("à última modificação de llms/sitemap do site", util.mtime_max([c.SITE / n for n in ("llms.txt", "llms-full.txt", "sitemap.xml")]))]
    if c.PUB.is_dir():
        for repo in sorted(c.PUB.glob("central-publica*")):
            if (repo / ".git").exists():
                ms.append(("ao último commit de %s" % repo.name, util.data_do_commit(repo, "HEAD")))
    return ms


def marcos_c19(ctx):
    """A medida FINAL vem depois de tudo: do Nós vivo, dos dois commits da custódia, da última subida verificada e da conferência final."""
    from . import site
    c = ctx.c
    nv = c.NOS_VIVO / "nos_vivo.sqlite3"
    ms = [marco_selo(ctx), ("ao nos_vivo.sqlite3", datetime.fromtimestamp(nv.stat().st_mtime) if nv.is_file() else None)]
    for rot, repo in (("ao commit do espelho", c.TB), ("ao commit da Central", c.CEN)):
        h = util.commit_da_custodia(repo, ctx.versao)
        ms.append((rot, util.data_do_commit(repo, h) if h else None))
    ms.append(("à última subida verificada do site", site.instante_da_ultima_subida(ctx)))
    cf = [d / ("CONFERENCIA_FINAL_%s.json" % ctx.versao) for d in c.pastas_trabalho_existentes(ctx.versao)]
    ms.append(("à conferência final", util.mtime_max([p for p in cf if p.is_file()])))
    return ms


# C19 não entra: ELE é quem remede (sua marca vira FALTA com o quadro velho e o aplicador constrói o Nós vivo e remede)
MARCOS = {"E12": marcos_e12, "C18": marcos_c18}


def remedir(ctx):
    """Roda `tools\\estado_do_organismo.py` (o MESMO comando de C19). O quadro é o instrumento de medida; os arquivos ESTADO_DO_ORGANISMO.* são derivados.
    rc 0/1/2 são resultados da medida (OK / DEFASADO / FALHA de leitura); qualquer outro é falha do instrumento: PARA."""
    c = ctx.c
    args = [str(c.PYTHON), "-X", "utf8", "tools/estado_do_organismo.py"] + ([] if ctx.rede else ["--sem-rede"])
    r = util.rodar(args, cwd=c.CEN, timeout=900)
    if r["rc"] not in (0, 1, 2) or ler_quadro(ctx) is None:
        raise Parar("o instrumento do quadro (estado_do_organismo.py) falhou (rc %s)" % r["rc"], r["saida"].strip().splitlines()[-4:])
    ctx._cache_j.clear()
    return ler_quadro(ctx)


def garantir_fresco(ctx, p):
    """Antes de decidir por um quadro, em `executar`: se ele é anterior aos marcos do passo, REMEDE. Devolve True se remediu."""
    if p.id == "E12" and ctx.rede:
        return False                     # com --rede/--publicar a marca de E12 lê o raw direto: não depende do quadro
    f = MARCOS.get(p.id)
    q = ler_quadro(ctx)
    if f is not None and q is not None and fresco(q, f(ctx))[0]:
        return False
    remedir(ctx)
    return True


def item_do_quadro(ctx, superficie, item, marcos=()):
    """Marca a partir do JSON do último quadro (leitura): OK -> aplicado; DEFASADO -> falta; quadro velho (anterior ao selo ou aos `marcos`) ou item
    em FALHA -> INDETERMINADO (nunca se decide por quadro velho)."""
    q = ler_quadro(ctx)
    if not q:
        return indeterminado("sem ESTADO_DO_ORGANISMO.json: rode o quadro (C19) ou passe --rede")
    ok, motivo = fresco(q, [marco_selo(ctx)] + list(marcos))
    if not ok:
        return indeterminado(motivo)
    for i in q["itens"]:
        if i["superficie"] == superficie and i["item"] == item:
            if i["estado"] == "OK":
                return aplicado("quadro de %s: %s" % (q["medido_em"], i["achado"][:60]))
            if i["estado"] == "FALHA":
                return indeterminado("quadro de %s: FALHA de leitura (%s); rode o quadro com rede" % (q["medido_em"], i["achado"][:60]))
            return falta("quadro de %s: %s (%s)" % (q["medido_em"], i["estado"], i["achado"][:60]))
    return indeterminado("o quadro não tem o item «%s / %s»" % (superficie, item))


# =================================================================== C19 — Nós vivo e quadro do organismo
def _ja_c19(ctx):
    nv = ctx.c.NOS_VIVO / "nos_vivo.sqlite3"
    if not ctx.corrente:
        return superado_rel("o quadro mede a versão corrente do Nós (G1 não tem artefato do quadro desta versão)")
    ts = util.instante(ctx.selo_nos.get("timestamp"))
    if not nv.is_file() or datetime.fromtimestamp(nv.stat().st_mtime) < ts:
        return falta("nos_vivo.sqlite3 não foi gravado depois do selo (%s)" % ctx.selo_nos.get("timestamp"))
    q = ler_quadro(ctx)
    if not q:
        return falta("sem ESTADO_DO_ORGANISMO.json")
    ok, motivo = fresco(q, marcos_c19(ctx))
    if not ok:
        return falta(motivo)
    defas, falhas, ops = classificar(q)
    if defas or falhas:
        return falta("quadro de %s: %d DEFASADO e %d FALHA de G1 (ex.: %s)" % (q.get("medido_em"), len(defas), len(falhas), _txt_item((defas + falhas)[0])[:110]))
    res = q.get("resumo", {})
    return aplicado("quadro de %s: %s%s" % (q.get("medido_em"), ", ".join("%s %s" % (k, v) for k, v in sorted(res.items())),
                                            ("; %d do operador à parte (app, Zenodo, painel)" % len(ops)) if ops else ""))


def _ap_c19(ctx):
    c = ctx.c
    r1 = util.rodar([str(c.PYTHON), "-X", "utf8", str(c.NOS_VIVO / "construir.py")], cwd=c.NOS_VIVO, timeout=300)
    if r1["rc"] != 0:
        raise Parar("NOS_VIVO\\construir.py falhou", r1["saida"].strip().splitlines()[-4:])
    q = remedir(ctx)
    defas, falhas, ops = classificar(q)
    if falhas:
        raise Parar("o quadro tem %d FALHA(s) de leitura em superfícies de G1" % len(falhas), [_txt_item(i) for i in falhas[:12]])
    if defas:
        raise Parar("o quadro tem %d itens DEFASADOS (fora os do operador): a custódia não está completa" % len(defas), [_txt_item(i) for i in defas[:12]])
    return {"resumo": q.get("resumo", {}), "pendente_do_operador": [_txt_item(i) for i in ops]}


# =================================================================== C20 — as pernas que o selo já puxa (só conferir)
def _pernas_do_selo(ctx):
    c, v = ctx.c, ctx.versao
    out = {}
    rec = sorted(glob.glob(str(c.BU / "estado" / "sincronizacao" / ("RECIBO_SINCRONIZACAO_%s_*.json" % v))))
    if not rec:
        out["Bancada Um (recibo de sincronização)"] = (False, "ausente")
    else:
        d = util.ler_json(rec[-1])
        prod = d.get("producao") is True and d.get("sandbox") is False and d.get("modo") == "aplicar" and "APLICADA" in str(d.get("veredito")) and d.get("versao_alvo") == v
        out["Bancada Um (recibo de sincronização)"] = (prod, "%s%s" % (os.path.basename(rec[-1]), "" if prod else
                                                                      " — NÃO é recibo de produção aplicado (producao=%s sandbox=%s modo=%s versao_alvo=%s)" % (
                                                                          d.get("producao"), d.get("sandbox"), d.get("modo"), d.get("versao_alvo"))))
    act = c.CEN / "Chatgpt" / "IALD_ORQUESTRACAO_20260923" / "state" / "canonical_memory" / "ACTIVE.json"
    if not act.is_file():
        out["memória canônica da fila/app (ACTIVE.json)"] = (False, "ACTIVE.json ausente")
    else:
        a = util.ler_json(act)
        rel = a.get("release")
        ok_rel = bool(rel) and util.versao_num(rel) >= util.versao_num(v)        # uma versão mais nova já puxada supera esta (versão histórica)
        det = "release %s%s" % (rel, "" if rel == v else (" (>= %s)" % v if ok_rel else " (!= %s)" % v))
        if ok_rel:
            rd = act.parent / "releases" / str(a.get("epoch") or "")
            mf = rd / "manifest.json"
            if rel == v:
                if mf.is_file() and util.sha256_arquivo(mf) == a.get("manifest_sha256"):
                    det += "; manifest.json do release confere com ACTIVE.manifest_sha256"
                else:
                    ok_rel, det = False, det + "; o manifest.json do release NÃO confere com ACTIVE.manifest_sha256 (ou não existe)"
            else:
                if not list((act.parent / "releases").glob("%s_*/manifest.json" % v)):
                    ok_rel, det = False, det + "; sem releases\\%s_*\\manifest.json" % v
        out["memória canônica da fila/app (ACTIVE.json)"] = (ok_rel, det)
    dl = sorted(glob.glob(str(c.CEN / "work" / ("scientific_memory_sync_*_%s" % v) / "DELIVERY_R1.json")))
    if not dl:
        out["memória científica da fila (DELIVERY_R1.json)"] = (False, "ausente")
    else:
        d = util.ler_json(dl[-1])
        ok = str(d.get("status", "")).startswith("ACTIVATED") and d.get("release") == v
        out["memória científica da fila (DELIVERY_R1.json)"] = (ok, "%s: %s%s" % (os.path.basename(os.path.dirname(dl[-1])), d.get("status"), "" if ok else " — release %s != %s" % (d.get("release"), v)))
    return out


def _ja_c20(ctx):
    pernas = _pernas_do_selo(ctx)
    faltam = [k for k, (ok, _) in pernas.items() if not ok]
    if not faltam:
        return aplicado("; ".join("%s: %s" % (k, d) for k, (_, d) in pernas.items()))
    return falta("DEFASADO no organismo: %s" % "; ".join("%s (%s)" % (k, pernas[k][1]) for k in faltam))


def _ap_c20(ctx, espera_s=600, passo_s=20):
    """Só CONFERE, com espera limitada (10 min, configurável por G1_ESPERA_PERNAS): nunca executa nem reinicia serviço."""
    espera = int(os.environ.get("G1_ESPERA_PERNAS") or espera_s)
    t0 = time.time()
    while True:
        pernas = _pernas_do_selo(ctx)
        faltam = [k for k, (ok, _) in pernas.items() if not ok]
        if not faltam:
            return {k: d for k, (_, d) in pernas.items()}
        if time.time() - t0 >= espera:
            raise Parar("o selo não puxou todas as pernas depois de %d s (DEFASADO visível; não bloqueia o commit, bloqueia dizer «concluída» no t3)" % espera,
                        ["%s (%s)" % (k, pernas[k][1]) for k in faltam])
        time.sleep(passo_s)


# =================================================================== C21 — a perna do APP (só conferir, nunca construir)
def release_do_app(ctx):
    """(release, release_source_sha256, outras_pecas) lidos de `iald_nucleo_fixo.json` do app: `operational_core.current_release` é a release instalada e o `release_source_sha256` é o sha256
    do `um.py` de que ela saiu; `outras_pecas` = {active_cluster|jev_control: release}. Arquivo ausente/ilegível ou sem a release = FalhaLeitura (nunca «em dia»)."""
    p = ctx.c.APP / "iald_nucleo_fixo.json"
    d = util.ler_json(p)
    oc = d.get("operational_core") if isinstance(d, dict) else None
    rel = (oc or {}).get("current_release")
    if not isinstance(rel, str) or not re.fullmatch(r"v\d{3,}", rel):
        raise FalhaLeitura("%s: operational_core.current_release ausente ou ilegível (%r)" % (p.name, rel))
    outras = {k: d[k]["release"] for k in ("active_cluster", "jev_control") if isinstance(d.get(k), dict) and isinstance(d[k].get("release"), str) and re.fullmatch(r"v\d{3,}", d[k]["release"])}
    return rel, (oc or {}).get("release_source_sha256"), outras


def _ja_c21(ctx):
    rel, src, outras = release_do_app(ctx)
    nr = util.versao_num(rel)
    corrente = ctx.selo_nos["um_version"]
    instr = INSTRUCAO_DO_APP % corrente           # o pipeline do app é o da versão CORRENTE do selo, nunca o de uma versão histórica
    if nr < ctx.n:
        return operador("DEFASADO: o app instalado está na release %s; a versão é %s%s. Decisão do OPERADOR: %s" % (
            rel, ctx.versao, "" if ctx.corrente else " (histórica; o selo corrente é %s)" % corrente, instr))
    if nr == ctx.n:
        pin = ctx.pin_completo
        igual = (src == pin) if pin else (bool(src) and str(src).startswith(ctx.pin16))
        if not igual:
            return operador("o app diz release %s, mas o release_source_sha256 (%s…) NÃO é o pino do selo de %s (%s…): instalação de OUTRO um.py. Decisão do OPERADOR: %s" % (
                rel, str(src)[:16], ctx.versao, (pin or ctx.pin16)[:16], instr))
        base = aplicado("app: operational_core.current_release = %s e release_source_sha256 = o pino do selo (%s…)" % (rel, ctx.pin16))
    else:
        base = superado("o app já está na release %s (posterior a %s)" % (rel, ctx.versao))
    atras = sorted("%s %s" % (k, r) for k, r in outras.items() if util.versao_num(r) < nr)
    if atras:
        return operador("instalação do app incoerente: o núcleo operacional diz %s, mas %s. Decisão do OPERADOR: %s" % (rel, "; ".join(atras), instr))
    return base


def passos(ctx):
    from . import memorias
    return [
        Passo("C19", 4, "Nós vivo e quadro do organismo (a medida final)", _ja_c19, aplicar=_ap_c19, fase="B", rede=True,
              escreve="NOS_VIVO\\nos_vivo.sqlite3, organismo\\ESTADO_DO_ORGANISMO.{md,json}"),
        Passo("C20", 4, "pernas que o selo já puxa: Bancada Um, ACTIVE.json, memória científica (só conferir)", _ja_c20, aplicar=_ap_c20, fase="B", escreve="(só leitura)"),
        Passo("C21", 4, "app: a release instalada contra a versão (só conferir; construir é do operador)", _ja_c21, aplicar=None, fase="B", escreve="(só leitura)"),
        memorias.passo_c17c(ctx),
    ]
