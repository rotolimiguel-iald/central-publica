# -*- coding: utf-8 -*-
"""Perna 3 — a CENTRAL PÚBLICA (C18): três repositórios, `/central/` do site, `um.acom`. G1 NÃO a reimplementa: chama o encadeador que já existe
(`work\\central_publica_22out\\atualizar_central_publica.py`, 27 passos medidos) e acrescenta o que ele não tem:

  - ORDEM IMPOSTA (ESPEC_ESPELHO §5, L10/L11): a perna 1 INTEIRA (E18 subida verificada e E19 leitor de IA) antes — senão a subida de uma publicaria o
    meio-trabalho da outra, porque o manifesto de ambas cobre o `v3.0` inteiro. A cauda do site do encadeador (llms_site, sitemap, manifesto, subir)
    NÃO é removida: o `/central/` e o `um.acom` mudam arquivos do site que só ESTA subida leva ao ar. O que G1 faz é partir a chamada em duas
    — até o ensaio da subida e, depois do CONJUNTO ESPERADO conferido, a subida —, para não subir o que não se esperava;
  - as pré-condições que ficavam fora da cadeia (L15): `frontend\\dist_publica` mais novo que `frontend\\src` e o backend local em 127.0.0.1:8765 respondendo;
  - o passo `estado_do_organismo` é do C19 (quadro), não daqui.
Ato para fora (push nos repositórios públicos, subida): só com --publicar."""
import re
import urllib.request
from datetime import datetime

from . import util
from .motor import Passo, aplicado, falta, superado_rel, indeterminado
from .util import Parar

ESPERADOS_PERNA3 = (r"^central/", r"^llms\.txt$", r"^llms-full\.txt$", r"^sitemap\.xml$", r"^linhas-de-pesquisa\.html$", r"^index\.html$", r"^index\.md$", r"^read-brief\.md$",
                    r"^\.htaccess$", r"^secoes/")
FORA_DA_CHAMADA = ("estado_do_organismo",)


def _encadeador(ctx):
    return ctx.c.CEN / "work" / "central_publica_22out" / "atualizar_central_publica.py"


def _passos_do_encadeador(ctx):
    r = util.rodar([str(ctx.c.PYTHON), "-X", "utf8", str(_encadeador(ctx)), "--listar"], cwd=ctx.c.CEN, timeout=120)
    if r["rc"] != 0:
        raise Parar("atualizar_central_publica.py --listar falhou", r["saida"].strip().splitlines()[-4:])
    nomes = []
    for ln in r["saida"].splitlines():
        m = re.match(r"^(\S+)\s+(repos|site|fim)\b", ln)
        if m:
            nomes.append(m.group(1))
    return nomes


def _rodada_completa_ate_o_ensaio(ctx, ate_ensaio):
    """A rodada do encadeador MAIS NOVA que (a) terminou `ok`, (b) rodou todos os passos até `subir_ensaio` com rc 0, (c) é POSTERIOR ao commit da
    custódia na Central (C14: o que ela leva ao público é o estado commitado) e (d) deixou o manifesto do seu carimbo. Devolve (carimbo, manifesto) ou None.
    Lição da v401/v402 (25 e 27/10/2026): a chamada partida em duas rodadas perdia o manifesto da primeira (o encadeador o nomeia pelo carimbo da rodada
    corrente) e a retomada refazia os 26 passos (~80 min, com 3 publicações). Rodada completa posterior ao commit não se refaz: a subida a reaproveita."""
    c = ctx.c
    h = util.commit_da_custodia(c.CEN, ctx.versao)
    if not h:
        return None
    t_commit = util.data_do_commit(c.CEN, h)
    pasta = c.CEN / "work" / "central_publica_22out" / "rodadas"
    for p in sorted(pasta.glob("*.json"), reverse=True):
        try:
            d = util.ler_json(p)
        except Exception:  # noqa: BLE001
            continue
        if not isinstance(d, dict) or d.get("ok") is not True:
            continue
        feitos = {x.get("nome"): x for x in d.get("passos", []) if isinstance(x, dict)}
        if any(n not in feitos or feitos[n].get("rc") != 0 for n in ate_ensaio):
            continue
        carimbo = str(d.get("rodada") or p.stem)
        try:
            t = datetime.strptime(carimbo, "%Y%m%d_%H%M%S")
        except ValueError:
            continue
        if t < t_commit:
            continue
        man = c.BANC / "revisoes" / ("manifesto_central_publica_%s.json" % carimbo)
        if man.is_file():
            return carimbo, man
    return None


def _ja_c18(ctx):
    from . import quadro
    c = ctx.c
    if not ctx.corrente:
        ok = '"custodia.%s"' % ctx.versao in util.ler_texto(c.ROTAS_JSONL, "replace")
        return (superado_rel("a Central pública segue a versão corrente; a rota custodia.%s existe (G1 não tem o retrato público desta versão)" % ctx.versao) if ok
                else falta("rota custodia.%s ausente" % ctx.versao))
    q = quadro.ler_quadro(ctx)
    if not q:
        return indeterminado("sem ESTADO_DO_ORGANISMO.json (rode o quadro: C19)")
    ok_fresco, motivo = quadro.fresco(q, quadro.marcos_c18(ctx))          # nunca se decide por quadro VELHO (achado dos céticos)
    if not ok_fresco:
        return indeterminado(motivo)
    its = [i for i in q["itens"] if i["superficie"].startswith("Central pública")]
    ruins = [i for i in its if i["estado"] in ("DEFASADO", "FALHA")]
    if not its:
        return indeterminado("o quadro não tem itens da Central pública")
    if ruins:
        return falta("%d de %d itens da Central pública defasados no quadro de %s (ex.: %s)" % (len(ruins), len(its), q.get("medido_em"), ruins[0]["item"][:70]))
    return aplicado("quadro de %s: %d itens da Central pública, nenhum defasado" % (q.get("medido_em"), len(its)))


def _pre_c18(ctx):
    from . import site
    f = []
    for rot, m in (("E18 (subida do site)", site._ja_e18(ctx)), ("E19 (leitor de IA)", site._ja_e19(ctx))):
        if m.estado not in ("APLICADO", "SUPERADO", "SUPERADO_REL"):
            f.append("a perna 1 não terminou: %s — %s (a Central pública vem DEPOIS)" % (rot, m.detalhe))
    fe = ctx.c.CEN / "frontend"
    src_t = max((p.stat().st_mtime for p in (fe / "src").rglob("*") if p.is_file()), default=0)
    dist = fe / "dist_publica" / "index.html"
    if not dist.is_file() or dist.stat().st_mtime < src_t:
        f.append("frontend\\dist_publica está mais velho que frontend\\src (o `vite build` não está na cadeia: é da frente da web)")
    try:
        with urllib.request.urlopen("http://127.0.0.1:8765/api/health", timeout=5) as r:
            if r.status != 200:
                f.append("/api/health respondeu %s" % r.status)
    except Exception as e:  # noqa: BLE001
        f.append("o backend local 127.0.0.1:8765 não respondeu (o `retrato` precisa dele): %r" % (e,))
    return f


def _ap_c18(ctx):
    from .site import _subidas, _diferencas_do_ensaio
    enc = [str(ctx.c.PYTHON), "-X", "utf8", str(_encadeador(ctx))]
    passos = [n for n in _passos_do_encadeador(ctx) if n not in FORA_DA_CHAMADA]
    if "subir_ensaio" not in passos or "subir" not in passos:
        raise Parar("o encadeador mudou: sem subir_ensaio/subir na lista de passos", passos)
    ate_ensaio = passos[: passos.index("subir_ensaio") + 1]
    pronta = _rodada_completa_ate_o_ensaio(ctx, ate_ensaio)
    if pronta is None:
        r1 = util.rodar(enc + ["--so", ",".join(ate_ensaio), "--publicar"], cwd=ctx.c.CEN, timeout=4 * 3600)
        if r1["rc"] != 0:
            raise Parar("a Central pública parou antes da subida (rc %s)" % r1["rc"], r1["saida"].strip().splitlines()[-8:])
        pronta = _rodada_completa_ate_o_ensaio(ctx, ate_ensaio)
        if pronta is None:
            raise Parar("a rodada do encadeador terminou, mas não há rodada completa até o ensaio, posterior ao commit da Central, com o manifesto do seu carimbo",
                        ["work/central_publica_22out/rodadas/*.json", "v3.0_bancada/revisoes/manifesto_central_publica_<carimbo>.json"])
    carimbo, manifesto = pronta
    # o ensaio que vale é o DESSE manifesto (o relatório o cita), não o dry-run mais novo de qualquer origem
    ens = [p for p in _subidas(ctx, True) if manifesto.name in util.ler_texto(p / "RELATORIO.md", "replace")]
    if not ens:
        raise Parar("o ensaio da Central pública não deixou RELATORIO.md que cite o manifesto %s" % manifesto.name)
    difs = _diferencas_do_ensaio(util.ler_texto(ens[-1] / "RELATORIO.md", "replace"))
    permitido = [re.compile(x) for x in ESPERADOS_PERNA3]
    fora = [(p, e) for p, e in difs if not any(rx.match(p) for rx in permitido)]
    if fora:
        raise Parar("o ensaio da subida da Central pública difere FORA do conjunto esperado (L10): nada sobe", ["%s: %s" % x for x in fora[:20]])
    r2 = util.rodar(enc + ["--so", "subir", "--publicar", "--manifesto", str(manifesto)], cwd=ctx.c.CEN, timeout=2 * 3600)
    if r2["rc"] != 0:
        raise Parar("a subida da Central pública falhou (rc %s)" % r2["rc"], r2["saida"].strip().splitlines()[-8:])
    # a subida da perna 3 MUDOU o ar (index, llms, sitemap, /central/): a marca de E19 exige um relatório do leitor de IA (R1) POSTERIOR à última subida verificada
    # (achado do cético final); sem esta releitura a execução terminaria com E19 velho e só uma 2ª passada o refaria. É leitura (HTTP) + um relatório em BANC\revisoes.
    from . import site
    try:
        site._ap_e19(ctx)
    except Parar as e:
        raise Parar("a Central pública SUBIU, mas o leitor de IA (R1) depois da subida reprovou: %s" % e.motivo, e.faltam)
    return {"passos_ate_o_ensaio": len(ate_ensaio), "rodada_ate_o_ensaio": carimbo, "manifesto": manifesto.name, "diferencas_esperadas": len(difs),
            "leitor_ia_depois_da_subida": "R1 relido"}


def passos(ctx):
    return [Passo("C18", 3, "Central pública: 3 repositórios, /central/, um.acom", _ja_c18, aplicar=_ap_c18, pre=_pre_c18, externo=True, fase="B", longo=True, rede=True, usa_quadro=True,
                  escreve="C:\\IALD\\Central_publica\\* (push), /central/ no ar, um.acom, llms.txt, sitemap, manifesto, subida")]
