# -*- coding: utf-8 -*-
"""Os TEXTOS da custódia: MOLDES com campos lidos de `fatos` (números), do core (citações verbatim) e do HANDOFF (blocos entre
marcadores) — ESPEC_ESPELHO §3 e ESPEC_CENTRAL §4.5. Nenhum texto científico é inventado:

  - o que tem fonte (parágrafos `PARAGRAFO_*` do handoff, títulos do diário, números do core) entra VERBATIM ou calculado;
  - a prosa que hoje a gerência escreve à mão (título EN, «what entered», itens 3 e 4 da errata, arco EN/PT, corpo do commit)
    sai do molde CURTO E FACTUAL; o handoff a SUBSTITUI se trouxer o marcador `<!-- INICIO_<ID> -->`:
        TITULO_EN_vN · ENTROU_EN_vN · KERNEL_LEITURA_EN_vN · ABERTOS_EN_vN · ARCO_EN_vN · ARCO_PT_vN · COMMIT_vN
    Sem o marcador, a execução PARA com a lista do que falta, a menos de `--aceitar-molde` (aí usa o molde factual e diz, no recibo).
  - todo texto passa pelo PORTÃO DE TEXTO antes de qualquer escrita (§4.5): sem CONFIRMED fora da fórmula da régua, sem hash que
    a rodada não calculou, sem «pós-dição» como demérito, sem `physical_verdict_allowed` verdadeiro, campo de rota sem `CONFIRM`."""
import re
from dataclasses import dataclass, field

from . import util
from .util import Parar

# --------------------------------------------------------------------------- marcadores que o handoff PODE trazer
MARCADORES_OPCIONAIS = ("TITULO_EN", "ENTROU_EN", "KERNEL_LEITURA_EN", "ABERTOS_EN", "ARCO_EN", "ARCO_PT", "COMMIT")

# fórmulas da régua em que CONFIRMED/CONFIRMADA/PROVADA podem aparecer (o resto é violação)
FORMULAS = ("CONFIRMED is accreditation, the one refused word", "PROVADA ≠ CONFIRMADA", "PROVADA ≠ CONFIRMADA", "CONFIRMADA = creditação, recusada",
            "NOT_CONFIRMED", "NOT_A_CONFIRMATION", "Not falsified is not a confirmation", "NOT_FALSIFIED nunca é CONFIRMED", "Proved is not a judgement of nature",
            "PROVED is validity", "PROVADA = validade", "nunca é a palavra da creditação")


# =================================================================== utilidades
def _plural(n, um, varios):
    return um if n == 1 else varios


def _base(modulo):
    return re.sub(r"\.lean$", "", modulo.rsplit("/", 1)[-1])


def sem_aspas_simples(t):
    return t.replace("'", "’")


def deposito_zenodo(c):
    """O depósito Zenodo lido do CITATION.cff do espelho (L16: nada de DOI digitado nos geradores)."""
    t = util.ler_texto(c.TB / "CITATION.cff", "replace")
    v = re.search(r'^version:\s*"(v\d+)"', t, re.M)
    doi = re.search(r'^doi:\s*"([^"]+)"', t, re.M)
    d = re.search(r"Zenodo deposit of (v\d+), deposited (\d{4}-\d\d-\d\d) \(byte-identical to the seal: um\.py sha256 ([0-9a-f]{16})", t)
    if not (v and doi and d):
        raise Parar("CITATION.cff sem a linha do depósito Zenodo (version/doi/«Zenodo deposit of vK…»)")
    return {"versao": v.group(1), "doi": doi.group(1), "data": d.group(2), "pin16": d.group(3)}


def _data_da_ordem(ordem):
    """dd/mm da ordem do operador, pelo nome do arquivo verbatim (OPERADOR_23out_...)."""
    if not ordem:
        return None
    m = re.search(r"(\d{2})(jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez)", ordem.name)
    if not m:
        return None
    meses = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
    return "%s/%02d" % (m.group(1), meses.index(m.group(2)) + 1)


def ordem_padrao(c):
    """A regra permanente do operador (23/10): o arquivo verbatim, se existir."""
    cand = sorted((c.CEN / "work").glob("*/OPERADOR_*_custodiar_quando_o_handoff_aparecer_verbatim.txt"))
    return cand[0] if cand else None


# =================================================================== o portão de texto (ESPEC_CENTRAL §4.5)
def portao(texto, conhecidos=(), campo_de_rota=False, rotulo="texto"):
    """Lista de violações (vazia = passa). `conhecidos`: hashes (16 ou 64 hex) que a rodada calculou ou leu do handoff."""
    v = []
    t = texto
    # 1) CONFIRMED / CONFIRMADA só dentro das fórmulas da régua
    limpo = t
    for f in FORMULAS:
        limpo = limpo.replace(f, " ")
    if re.search(r"(?<![A-Z_])CONFIRMED(?![A-Z_])", limpo):
        v.append("%s: «CONFIRMED» fora da fórmula da régua" % rotulo)
    if re.search(r"CONFIRMAD[AO]S?\b", limpo):
        v.append("%s: «CONFIRMADA» fora da fórmula da régua" % rotulo)
    # 2) provada/PROVED sem estatuto na mesma frase
    for fr in re.split(r"(?<=[.;:!?])\s+|\n", t):
        if re.search(r"\b(PROVADA|PROVED|provada|proved)\b", fr) and not re.search(r"validade|validity|≠|≠|creditação|creditacao|accreditation|creditation|judgement|nature", fr, re.I):
            v.append("%s: «provada/proved» sem estatuto na mesma frase: %r" % (rotulo, fr[:80]))
    # 3) pós-dição como demérito
    if re.search(r"p[óo]s-?di[cç][ãa]o|post-?diction|postdiction", t, re.I):
        v.append("%s: «pós-dição» como demérito (a frase vigente é «retrodição sem ajuste (novidade de uso)»)" % rotulo)
    # 4) hash que a rodada não calculou
    conh = {str(x).lower() for x in conhecidos}
    for h in set(re.findall(r"(?<![0-9a-fA-F])[0-9a-f]{64}(?![0-9a-fA-F])", t)) | set(re.findall(r"(?<![0-9a-fA-F])[0-9a-f]{16}(?![0-9a-fA-F])", t)):
        if h not in conh and h[:16] not in conh:
            v.append("%s: hash %s não está entre os calculados/lidos nesta rodada" % (rotulo, h[:16]))
    # 5) campo de rota: nem a substring CONFIRM
    if campo_de_rota and "CONFIRM" in t.upper():
        v.append("%s: campo de rota contém a substring CONFIRM" % rotulo)
    # 6) veredito físico
    if re.search(r"physical_verdict_allowed\W+(true|1)\b", t, re.I):
        v.append("%s: physical_verdict_allowed verdadeiro" % rotulo)
    return v


def conhecidos_da_rodada(ctx):
    """Todo hash que um texto gerado pode citar: os da rodada (selo, cofre, recibos) e os que o próprio handoff traz."""
    s = set()
    F = None
    try:
        F = ctx.fatos
    except Exception:  # noqa: BLE001
        pass
    if F:
        s |= {F["pin"], F["pin16"], F.get("anterior_pin16") or ""}
        s |= set((F.get("origem") or {}).values())
        s |= {x["sha16"] for x in (F["cadeia"].get("recibos_bn") or {}).values()}
        for b in F.get("blocos", {}).values():
            s.add(b["verdict_sha16"])
    h = ctx.handoff
    if h:
        s |= set(re.findall(r"(?<![0-9a-fA-F])[0-9a-f]{16}(?![0-9a-fA-F])", h.texto))
        s |= set(re.findall(r"(?<![0-9a-fA-F])[0-9a-f]{64}(?![0-9a-fA-F])", h.texto))
    try:
        s.add(deposito_zenodo(ctx.c)["pin16"])
    except Exception:  # noqa: BLE001
        pass
    s |= set(getattr(ctx, "hashes", ()))
    bd = ctx.bloco_diario
    if bd:
        s.add(bd.pin16)
    o = ctx.ordem or ordem_padrao(ctx.c)
    if o and o.is_file():
        s.add(util.sha256_arquivo(o))
        s.add(util.sha16(o))
    return {x.lower() for x in s if x}


# =================================================================== as fontes de cada texto
@dataclass
class Item:
    texto: str
    origem: str                    # 'handoff:<ID>' | 'core:<registro>' | 'diario' | 'molde-factual'
    faltam: list = field(default_factory=list)   # marcadores que o handoff poderia trazer


def _marcador(ctx, ident):
    h = ctx.handoff
    if not h:
        return None
    corpo = h.corpos.get("%s_%s" % (ident, ctx.versao))
    return corpo.strip("\n") if corpo else None


# quais marcadores opcionais cada passo CONSOME (só os passos pendentes precisam de fonte; o que já foi aplicado não pede prosa)
NECESSIDADE = {"E04": ("TITULO_EN", "ENTROU_EN", "KERNEL_LEITURA_EN", "ABERTOS_EN", "ARCO_EN", "ARCO_PT"), "E10": ("COMMIT",)}


def avaliar_fontes(ctx, pend_ids=None):
    """O que cada texto pendente tem como fonte (para o `planejar --seco`): do handoff, do core, molde factual, ou o que FALTA.
    `pend_ids`: só os marcadores que os passos PENDENTES consomem entram em `necessarios`/`faltam`. Não monta nada (leitura barata)."""
    h = ctx.handoff
    out = {"handoff": bool(h), "marcadores_presentes": sorted(h.marcadores) if h else [], "problemas_de_marcador": list(h.problemas) if h else [],
           "do_handoff": [], "molde_factual": [], "faltam": [], "bloqueios": [], "necessarios": [], "bloqueia": False}
    if not h:
        out["bloqueios"].append("HANDOFF_%s_CUSTODIA.md ausente" % ctx.versao)
        return out
    if ctx.bloco_diario is None or not ctx.bloco_diario.titulo_pt:
        out["bloqueios"].append("título PT não lido do diário (bloco «%s SELADA» sem o cabeçalho esperado)" % ctx.versao)
    precisa = {i for p, ids in NECESSIDADE.items() if (pend_ids is None or p in pend_ids) for i in ids}
    for ident in MARCADORES_OPCIONAIS:
        k = "%s_%s" % (ident, ctx.versao)
        (out["do_handoff"] if k in h.corpos else out["molde_factual"]).append(k)
        if ident in precisa:
            out["necessarios"].append(k)
            if k not in h.corpos:
                out["faltam"].append(k)
    for i in h.problemas:
        out["bloqueios"].append("handoff: " + i)
    out["paragrafos_prontos"] = [i for i, _ in h.paragrafos_prontos()]
    out["bloqueia"] = bool((out["faltam"] and not ctx.aceitar_molde) or (out["bloqueios"] and precisa))
    return out


# =================================================================== a construção dos textos
@dataclass
class Textos:
    versao: str
    txt_en: Item = None
    err_en: Item = None
    nota_en: Item = None
    bloco_ledger: Item = None
    arco_en: Item = None
    arco_pt: Item = None
    commit_espelho: Item = None
    paragrafos: list = field(default_factory=list)         # [(id, bloco com marcadores)] do handoff, na ordem
    citation: dict = field(default_factory=dict)
    molde_usado: list = field(default_factory=list)        # ids opcionais que caíram no molde
    violacoes: list = field(default_factory=list)
    conhecidos: set = field(default_factory=set)


def construir(ctx):
    """Monta TODOS os textos da perna 1 de `ctx.versao` e passa cada um pelo portão. Levanta Parar se faltar fonte obrigatória."""
    F = ctx.fatos
    c, v = ctx.c, ctx.versao
    core = _core_da_versao(ctx)
    bd = ctx.bloco_diario
    h = ctx.handoff
    if h is None:
        raise Parar("HANDOFF_%s_CUSTODIA.md ausente: nenhum texto pode ser composto" % v)
    if not (bd and bd.titulo_pt):
        raise Parar("título PT não lido do diário para %s" % v)
    if h.problemas:
        raise Parar("marcadores do handoff com problema", h.problemas)
    if not F["handoff"].get("ok"):
        raise Parar("o handoff diverge dos fatos medidos", F["handoff"].get("divergencias"))
    T = Textos(versao=v)
    T.conhecidos = conhecidos_da_rodada(ctx)
    dep = deposito_zenodo(c)
    ant = F["anterior"]
    mods = [_base(m) for m in F["kernel"]["modulos_novos"]]
    nmod = len(mods)
    nb = len(F["bandeiras_novas"])
    grupos = ", ".join("`%s` %d" % (k, n) for k, n in sorted(_grupos(F["bandeiras_novas"]).items()))
    teor, termos = F["escada"]["texto"], F["kernel"]["declaracoes"]
    kt = F["kh"]["teoremas"]
    novos_mec = [k for k in F["registros_novos"] if not re.match(r"(kh_n1_cobertura|cunhagens)_v\d+$", k)]
    cun = F.get("cunhagens")
    ver = F.get("veracidade")
    # --- título EN (marcador) ---
    tit_en = _marcador(ctx, "TITULO_EN")
    T.molde_usado += [] if tit_en else ["TITULO_EN_" + v]
    # --- a oração do Teste da Única Palavra: o número corrige a frase (a regra do 4,44) ---
    clausula_ver_en = clausula_ver_pt = ""
    if ver and ver.get("z_disc_calibrado") is not None:
        zd, pd = ver["z_disc_calibrado"], ver["p_disc_unilateral"]
        if not zd < 5:
            raise Parar("z_disc calibrado = %.2f não está abaixo do degrau de 5σ: o texto muda de estatuto e isso é decisão do operador" % zd)
        vreg = ver["versao_do_registro"]
        pd_en = ("%.1e" % pd).replace("e-0", "e-").replace("e+0", "e+")
        clausula_ver_en = ("the panel of the Unique Word Test (%s) stays at the top, unchanged (z_disc = %.2f, calibrated, one-sided p %s, below the 5σ step of "
                           "accreditation, which was not reached)" % (vreg, zd, pd_en))
        clausula_ver_pt = ("o quadro do Teste da Única Palavra (%s) segue no topo, intocado: z_disc = %s, calibrado, p unilateral %s, abaixo do degrau de 5σ da "
                           "creditação, que não foi alcançado" % (vreg, ("%.2f" % zd).replace(".", ","), pd_en.replace("e-", "e−").replace(".", ",")))
    # --- TXT: what entered ---
    m = _marcador(ctx, "ENTROU_EN")
    if m:
        txt = Item(m, "handoff:ENTROU_EN_" + v)
    else:
        T.molde_usado.append("ENTROU_EN_" + v)
        regs = "; ".join("`%s` (%s checks%s)" % (k, F["blocos"][k]["n_checks"], ", all verified" if F["blocos"][k]["checks_ok"] else "") for k in novos_mec if F["blocos"].get(k)) or "none besides the fixed ones"
        partes = ["%s: %d new kernel module%s (%s), %d new flag%s (%s); ladder %s -> %s (%d audited declarations, %d theorems, none outside the trio)"
                  % ((tit_en or v.upper()), nmod, _plural(nmod, "", "s"), ", ".join("`%s`" % x for x in mods), nb, _plural(nb, "", "s"), grupos or "-",
                     F["escada_anterior"]["texto"], teor, termos, kt),
                  "new registries (names provisional; the operator names them): %s" % regs]
        if cun:
            partes.append("`cunhagens_%s`: %d inscriptions%s by sha256" % (v, cun["n"], (" of " + cun["data"][:5]) if cun.get("data") else ""))
        partes.append("kh_n1 %d constants / %d theorems" % (F["kh"]["constantes"], kt))
        if clausula_ver_en:
            partes.append(clausula_ver_en)
        partes.append("certified by the sha256 the program reads of itself (%s)" % F["pin16"])
        txt = Item("; ".join(partes), "molde-factual", ["ENTROU_EN_" + v])
    T.txt_en = txt
    # --- ERR: errata beside ---
    itens = []
    khp = F.get("kh_registro_anterior") or ("kh_n1_cobertura_" + ant)   # 25/10/2026 (revisão v401): o registro que VALE para a anterior
    if F["kh"].get("constantes_anterior") is None or F["kh"].get("teoremas_anterior") is None:
        raise Parar("a cobertura do kernel da anterior não foi lida (kh anterior ausente nos fatos) — PARAR, não escrever None na errata")
    erratas_kh = (core.get("kh_n1_cobertura_" + v) or {}).get("erratas") or []
    carga = "" if not erratas_kh else (" `%s` now charges floors where its errata says so; the exact equalities live in `kh_n1_cobertura_%s`." % (khp, v))
    itens.append("> 1. *kh_n1 coverage*: %s -> %s constants, %s -> %s theorems; the formal tree of the Nós %d -> %d entries.%s"
                 % (F["kh"]["constantes_anterior"], F["kh"]["constantes"], F["kh"]["teoremas_anterior"], kt,
                    F["kernel"]["formais_anterior"], F["kernel"]["formais"], carga))
    contratos = sorted(F["contratos_expected_ladder"])
    esc = F["escada"]["esperadas"]
    if contratos:
        if not all(F["contratos_expected_ladder"][k] == esc for k in contratos):
            raise Parar("contrato com expected_ladder != escada %d" % esc, ["%s=%s" % (k, F["contratos_expected_ladder"][k]) for k in contratos if F["contratos_expected_ladder"][k] != esc])
        itens.append("> 2. *The %d contracts* (%s) now read `expected_ladder` = %d, the ladder of this version (the consumer requires exact equality with the "
                     "rite’s ladder; only the number changes)." % (len(contratos), ", ".join("`%s`" % x for x in contratos), esc))
    m = _marcador(ctx, "KERNEL_LEITURA_EN")
    if m:
        itens.append("> %d. *What the kernel proves and what is reading*: %s" % (len(itens) + 1, m))
    else:
        T.molde_usado.append("KERNEL_LEITURA_EN_" + v)
    m = _marcador(ctx, "ABERTOS_EN")
    if m:
        itens.append("> %d. *What stays open*: %s" % (len(itens) + 1, m))
    else:
        T.molde_usado.append("ABERTOS_EN_" + v)
        pend = h.secao("Pendências SÓ do operador")
        itens.append("> %d. *What stays open* (verbatim from the handoff of %s, in Portuguese): %s"
                     % (len(itens) + 1, v, re.sub(r"^\*\*[^*]+\*\*\s*", "", pend or "see the handoff").replace("\n", " ")))
    cab = ("> **Errata beside (%s, the custody of %s; read from the registries of the sealed core, from the lineage diary and from the handoff, none typed):**\n"
           % (ctx.data, v))
    T.err_en = Item(cab + "\n".join(itens), "molde-factual" if (not m) else "handoff+molde")
    # --- NOTA ---
    ap = F["bandeiras_do_gate"]["apagadas"]
    fontes_desc = "the new stones (%s), the KH-N1 coverage of %s%s" % (", ".join(mods) or "none", v, (" and the %d inscriptions of %s" % (cun["n"], cun["data"][:5])) if cun else "")
    ver_nota = ""
    if ver and ver.get("z_disc_calibrado") is not None:
        pdn = ("%.1e" % ver["p_disc_unilateral"]).replace("e-0", "e-")
        ver_nota = (" (the Unique Word Test, %s, reads z_disc = %.2f, calibrated, one-sided p %s: below the 5σ step, which was not reached)"
                    % (ver["versao_do_registro"], ver["z_disc_calibrado"], pdn))
    nota = ("*Status that goes with %s (not to be cut): PROVED is validity, by the operator’s ruling of 07/10 — the kernel proves the implication; validity in the "
            "kernel is not accreditation. CONFIRMED is accreditation, the one refused word; what nature decides about beta_TGL waits for 5 sigma%s. The reservation of v392 "
            "(15 computed + 3 literal gate flags; the unilateral V11 step) is [DECLARED by the audit] and F8.1 is open. Per-term flags %s stay False. The %s copy lives outside "
            "the repository; the stdout %s is in `rodadas/`; the diffs of %s are in `diferencas_%s/`; the pinned sources that the registries reread by absolute path are in "
            "`fontes_pinadas/` with their map (now with the %s sources: %s); the B(n) receipts of the Bancada are in `recibos_bancada_%s/`. The Zenodo deposit holds %s (%s). "
            "Not falsified is not a confirmation.*" % (v, ver_nota, " / ".join(ap) if ap else "(none)", ant, v, v, v, v, fontes_desc, v, dep["versao"], dep["doi"]))
    T.nota_en = Item(nota, "molde-factual")
    # --- parágrafos prontos do handoff (verbatim) ---
    T.paragrafos = h.paragrafos_prontos()
    # --- ARCO (site) ---
    for ident, attr, lang in (("ARCO_EN", "arco_en", "en"), ("ARCO_PT", "arco_pt", "pt")):
        mk = _marcador(ctx, ident)
        if mk:
            setattr(T, attr, Item(sem_aspas_simples(mk.replace("\n", " ")), "handoff:%s_%s" % (ident, v)))
        else:
            T.molde_usado.append("%s_%s" % (ident, v))
            setattr(T, attr, Item(sem_aspas_simples(_arco_molde(lang, v, tit_en, bd.titulo_pt, mods, nb, teor, termos, F, cun, clausula_ver_en if lang == "en" else clausula_ver_pt, ant)),
                                  "molde-factual", ["%s_%s" % (ident, v)]))
    # --- LEDGER ---
    T.bloco_ledger = Item(_bloco_ledger(ctx, F, T, dep, core, novos_mec, bd), "molde-factual")
    # --- commit do espelho ---
    mk = _marcador(ctx, "COMMIT")
    T.commit_espelho = Item(_commit_espelho(ctx, F, mods, nb, grupos, mk, bd), "handoff:COMMIT_" + v if mk else "molde-factual", [] if mk else ["COMMIT_" + v])
    # --- portão ---
    for rot, it in (("TXT", T.txt_en), ("ERR", T.err_en), ("NOTA", T.nota_en), ("ARCO_EN", T.arco_en), ("ARCO_PT", T.arco_pt), ("LEDGER", T.bloco_ledger)):
        T.violacoes += portao(it.texto, T.conhecidos, rotulo=rot)
    for ident, bloco in T.paragrafos:                 # o parágrafo do handoff é citado verbatim: só confere hash/CONFIRMED
        T.violacoes += portao(bloco, T.conhecidos, rotulo="handoff:" + ident)
    for rot, it in (("ARCO_EN", T.arco_en), ("ARCO_PT", T.arco_pt)):
        t = it.texto
        if "'" in t or "<" in t or "\\" in t or "\n" in t:
            T.violacoes.append("%s: aspa simples, «<», barra invertida ou quebra de linha (o texto vai em HTML e em JS)" % rot)
    return T


def _core_da_versao(ctx):
    from . import fatos as F
    return F.Artefatos(ctx.c, ctx.versao, "nos" if (ctx.corrente and ctx.nos_marcas.um_py_confere) else "cofre").core


def _grupos(bandeiras):
    g = {}
    for b in bandeiras:
        mm = re.match(r"^(.*?)_?\d+$", b)
        k = mm.group(1) if mm else b
        g[k] = g.get(k, 0) + 1
    return g


def _arco_molde(lang, v, tit_en, tit_pt, mods, nb, teor, termos, F, cun, clausula_ver, ant):
    nmod = len(mods)
    if lang == "en":
        t = "The custody of %s (complete round): " % v
        if tit_en:
            t += tit_en.lower() + " — "
        t += ("%d new kernel module%s (%s), %d new flags, ladder %s (named declarations with axioms in the trio; %d audited declarations, none outside the trio)."
              % (nmod, _plural(nmod, "", "s"), ", ".join(mods), nb, teor, termos))
        novos = [k for k in F["registros_novos"] if not re.match(r"(kh_n1_cobertura|cunhagens)_v\d+$", k)]
        if novos:
            t += " New registries read from the sealed core (names provisional): %s." % ", ".join(novos)
        if cun:
            t += " %d inscriptions%s by sha256." % (cun["n"], (" of " + cun["data"][:5]) if cun.get("data") else "")
        if clausula_ver:
            t += " " + clausula_ver[0].upper() + clausula_ver[1:] + "."
        t += (" Certified by the sha256 the program reads of itself (%s). Kernel %d files / %d terms. Proved is not a judgement of nature; the gate did not move"
              % (F["pin16"], F["kernel"]["formais"], termos))
        return t
    t = "A custódia da %s (rodada completa): " % v
    t += tit_pt.capitalize() + " — "
    t += ("%d módulo%s novo%s no kernel (%s), %d bandeiras novas, escada %s (%d declarações auditadas, nenhuma fora do trio)."
          % (nmod, _plural(nmod, "", "s"), _plural(nmod, "", "s"), ", ".join(mods), nb, teor, termos))
    novos = [k for k in F["registros_novos"] if not re.match(r"(kh_n1_cobertura|cunhagens)_v\d+$", k)]
    if novos:
        t += " Registros novos lidos do core selado (nomes provisórios): %s." % ", ".join(novos)
    if cun:
        t += " %d inscrições%s por sha256." % (cun["n"], (" de " + cun["data"][:5]) if cun.get("data") else "")
    if clausula_ver:
        t += " " + clausula_ver[0].upper() + clausula_ver[1:] + "."
    t += (" Certificada pelo sha256 que o programa lê de si (%s). Kernel %d arquivos / %d termos. PROVADA ≠ CONFIRMADA; o gate não se moveu"
          % (F["pin16"], F["kernel"]["formais"], termos))
    return t


def _bloco_ledger(ctx, F, T, dep, core, novos_mec, bd):
    v, ant = ctx.versao, F["anterior"]
    o = ctx.ordem or ordem_padrao(ctx.c)
    ordem_txt = ""
    if o and o.is_file():
        d = _data_da_ordem(o)
        ordem_txt = (" under the operator’s standing order%s (verbatim file `%s`, sha16 `%s`)" % ((" of " + d) if d else "", o.name, util.sha16(o)))
    ver_vs = [str((core.get(k) or {}).get("verdict")) for k in novos_mec if (core.get(k) or {}).get("verdict")]
    verd = ("Verdicts read from the sealed core: %s. " % " and ".join("`%s`" % x for x in ver_vs)) if ver_vs else ""
    g = F["bandeiras_do_gate"]
    pars = "\n\n".join(b for _, b in T.paragrafos)
    nota = T.nota_en.texto.strip("*")
    return ("\n### The custody — %s (COMPLETE round)\n\nPrepared by the session %s of the Central on %s%s (handoff %s of the management c1). The repository head is now "
            "`um.py` %s `%s` (%s bytes; **%s**; **COMPLETE round**; `FAIL_CLOSED_SELFTEST_PASSED`; sealed %s; `um_version` = %s in the seal).\n\n- **%s** `%s` "
            "(rite **%s**, COMPLETE round): %s.\n\n%s%s Kernel **%d formal files / %d audited terms**, all in the trio. The gate is **identical** to %s; the flags %d lit / %d off. "
            "The %s copy is kept outside the repository by sha16. The Zenodo deposit holds %s (%s); a new Zenodo version is the operator’s act. The gate did not move by this custody.\n\n%s\n\n%s\n"
            % (v, ctx.sessao, ctx.data, ordem_txt, v, v, F["pin16"], util.fmt_milhar(F["bytes_um_py"]), F["escada"]["texto"],
               F["timestamp"], v, v, F["pin16"], bd.ladder_no_corpo or F["escada"]["texto"], T.txt_en.texto.rstrip("."), verd, nota, F["kernel"]["formais"], F["kernel"]["declaracoes"],
               ant, len(g["ligadas"]), len(g["apagadas"]), ant, dep["versao"], dep["doi"], T.err_en.texto, pars))


def _commit_espelho(ctx, F, mods, nb, grupos, marcador, bd):
    v, ant = ctx.versao, F["anterior"]
    tit = util.ascii_sem_acento(bd.titulo_pt).lower()
    assunto = "custodia(%s): %s - selo, modulo%s %s, escada %s, fontes pinadas da %s, PORTAS, README" % (v, tit, "" if len(mods) == 1 else "s", " e ".join(mods) if mods else "nenhum", F["escada"]["texto"], v)
    corpo = ["um.py %s %s (rodada COMPLETA, autoteste fail-closed; gate identico ao da %s)." % (v, F["pin16"], ant),
             "Kernel %d formais / %d declaracoes, todas no trio; %d bandeiras novas (%s)." % (F["kernel"]["formais"], F["kernel"]["declaracoes"], nb, util.ascii_sem_acento(grupos).replace("`", "") or "-"),
             "Backup da %s fora do repositorio (um_%s_%s)." % (ant, ant, F["anterior_pin16"]),
             "ESTADO_ATUAL, LEDGER e CITATION (selo corrente) ao lado; o resto sai dos geradores."]
    if marcador:
        corpo.append("")
        corpo.append(util.ascii_sem_acento(marcador))
    corpo += ["", "PROVADA = validade; a creditacao segue recusada; o gate nao se moveu."]
    if ctx.coautor:
        corpo += ["", "Co-Authored-By: %s" % ctx.coautor]
    return assunto + "\n\n" + "\n".join(corpo) + "\n"


# =================================================================== CITATION.cff: só as duas descrições do selo corrente
def citation_pares(ctx, cff_texto, F, dep):
    """Os (velho, novo) do CITATION (L16: DOI e pino do depósito lidos do próprio arquivo, nunca digitados). Devolve lista de trocas."""
    v = ctx.versao
    data = F["timestamp"].split(" ")[0]
    d_old = re.search(r'    description: "the current seal of the repository, one page, regenerated at every custody \((v\d+) on [0-9-]{10}; the Zenodo deposit holds (v\d+)\)"\n', cff_texto)
    p_old = re.search(r'  - type: other\n    value: "sha256:[0-9a-f]{64}"\n    description: "the pin of um\.py at (v\d+), the repository head \([\d,]+ bytes; sealed [0-9: -]+\); the Zenodo deposit ([0-9.a-z/]+) holds (v\d+) \(([0-9a-f]{16})…\)"\n', cff_texto)
    if not (d_old and p_old):
        raise Parar("CITATION.cff: as duas descrições do selo corrente não casaram", ["descrição do ESTADO_ATUAL: %s" % bool(d_old), "descrição do pino: %s" % bool(p_old)])
    return [(d_old.group(0), '    description: "the current seal of the repository, one page, regenerated at every custody (%s on %s; the Zenodo deposit holds %s)"\n' % (v, data, dep["versao"])),
            (p_old.group(0), '  - type: other\n    value: "sha256:%s"\n    description: "the pin of um.py at %s, the repository head (%s bytes; sealed %s); the Zenodo deposit %s holds %s (%s…)"\n'
             % (F["pin"], v, util.fmt_milhar(F["bytes_um_py"]), F["timestamp"], dep["doi"], dep["versao"], dep["pin16"]))]
