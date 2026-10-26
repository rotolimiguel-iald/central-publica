# -*- coding: utf-8 -*-
"""A PEDRA GENÉRICA do runner da Fronteira (G1; ESPEC_CENTRAL §6): `medir_custodia_generica(oc, versao, anterior)` — o cofre `versao` contra o
cofre `anterior`, lidos PELO NOME (exata para sempre), com as expectativas CONGELADAS em `FATOS_CUSTODIA.json` DENTRO do cofre `versao`
(sha256 pinado no CUSTODY_MANIFEST.json), e DOIS CÉTICOS por injeção. Substitui a função de ~129 linhas escrita à mão a cada versão.

AUTOCONTIDA (só biblioteca padrão): é carregada POR CAMINHO pelo runner (`_custodia_generica`), instalada em
fronteira_tgl\\runner\\custodia_generica.py por work\\custodia_G1\\patches\\instalar_g1_0.py (a cópia-fonte mora em tools\\custodia_g1\\generico\\).

O que lê (S1..S14, mecânico, sem semântica por versão): identidade · blocos novos (bem formados, não movem o gate) · bandeiras ·
cobertura kh · escada · kernel · registro PT/EN e vereditos mudados («só dígitos e pino») · gate · ausência de CONFIRMED · contratos ·
monotonia · negações congeladas · cunhagens. O que NÃO lê (autoria humana, revisada ao lado em SEMANTICA_CUSTODIA.rev<n>.json): o SENTIDO das
negações, mudanças de veredito fora do padrão, nomes definitivos. Sem revisão a pedra roda `DECLARADO (sem revisao)` e diz.
physical_verdict_allowed é sempre False; nada aqui move o gate."""
import copy
import hashlib
import json
import re
from pathlib import Path

TRIO = ("propext", "Classical.choice", "Quot.sound")
RE_REG = re.compile(r"^([a-z][a-z0-9_]{3,}) & ([A-Z][A-Z0-9_]{12,})", re.M)
RX_CONF = re.compile(r"(?<![A-Za-z])(?<!NOT_)(?<!NEVER_)CONFIRMED")      # «CONFIRMED» só depois de NOT_/NEVER_ (a régua); medido sem falso positivo em v394..v398


def _ler_json(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def _ler_txt(p):
    return Path(p).read_text(encoding="utf-8", errors="replace")


def _sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def _norm(x):
    x = re.sub(r"[0-9a-f]{16,64}", "<PIN>", str(x))
    return re.sub(r"\d+", "#", x)


def _segmentos_negacao(verdict):
    out = set()
    for s in str(verdict or "").split("__"):
        if re.search(r"(^|_)(NOT|NO|NEVER)_", s) or s.endswith(("_UNMOVED", "_UNTOUCHED")):
            out.add(_norm(s))
    return out


def _checks_ok(ch):
    if ch is None:
        return True
    if isinstance(ch, dict):
        return all((x.get("ok") if isinstance(x, dict) else bool(x)) is True for x in ch.values())
    # 25/10/2026 (v399): os registros novos trazem checks como pares [descrição, bool]; aceitos com o mesmo rigor (todos True)
    return all((isinstance(x, dict) and x.get("ok") is True)
               or (isinstance(x, (list, tuple)) and len(x) == 2 and isinstance(x[0], str) and x[1] is True) for x in ch)


def bloco_ok(b):
    """S3: all_verified, does_not_gate_core, GATE_UNMOVED/UNTOUCHED, sem CONFIRMED sem NOT_, checks todos ok, guarda_p18_violacoes vazio."""
    if not isinstance(b, dict):
        return False
    vd = str(b.get("verdict") or "")
    return bool(b.get("all_verified") is True and b.get("does_not_gate_core") is True and ("GATE_UNMOVED" in vd or "GATE_UNTOUCHED" in vd)
                and not RX_CONF.search(vd) and _checks_ok(b.get("checks")) and not b.get("guarda_p18_violacoes"))


def fatos_do_cofre(cv):
    """FATOS_CUSTODIA.json do cofre, com o sha256 conferido contra o CUSTODY_MANIFEST (D1: a expectativa mora no cofre, que o git rastreia)."""
    man = _ler_json(cv / "CUSTODY_MANIFEST.json")
    ref = man.get("fatos_custodia") or {}
    p = cv / (ref.get("arquivo") or "FATOS_CUSTODIA.json")
    if not p.is_file() or _sha(p) != ref.get("sha256"):
        raise ValueError("FATOS_CUSTODIA.json ausente ou com sha256 diferente do pino do CUSTODY_MANIFEST")
    return _ler_json(p), man


def semantica_de_maior_revisao(cv, man):
    """SEMANTICA_CUSTODIA.json (rascunho) ou a maior SEMANTICA_CUSTODIA.rev<n>.json ao lado; None se não existir."""
    cand = sorted(cv.glob("SEMANTICA_CUSTODIA*.json"), key=lambda p: (len(p.name), p.name))
    revs = [p for p in cand if re.search(r"\.rev(\d+)\.json$", p.name)]
    if revs:
        return _ler_json(max(revs, key=lambda p: int(re.search(r"\.rev(\d+)\.json$", p.name).group(1))))
    p = cv / "SEMANTICA_CUSTODIA.json"
    return _ler_json(p) if p.is_file() else None


def _contratos(um_text):
    out = {}
    for m in re.finditer(r"^(_V\d{3}_\w*_CONTRACT)\s*=\s*\{", um_text, re.M):
        prox = re.compile(r"\n(?=[A-Za-z_@#])").search(um_text, m.end())
        regiao = um_text[m.start(): prox.start() if prox else len(um_text)]
        ach = re.findall(r"""['"]expected_ladder['"]\s*:\s*(\d+)""", regiao)
        out[m.group(1)] = int(ach[0]) if len(ach) == 1 else (None if not ach else "não literal")
    return out


# =================================================================== a semântica pura (roda também sobre as cópias injetadas)
def semantica(core, F, S):
    """S3 · S5 · S6 · S13 · S14 · S15 sobre um `core`. Pura: devolve (ok, {id: bool})."""
    r = {}
    v = F["versao"]
    novos = F["registros_novos"]
    r["S3_blocos_novos_bem_formados"] = all(bloco_ok(core.get(k)) for k in novos) and bool(novos)
    kh = core.get("kh_n1_cobertura_" + v) or {}
    L = kh.get("lido") or {}
    r["S5_kh"] = (L.get("constantes_cobertas") == F["kh"]["constantes"] and L.get("teoremas_cobertos") == F["kh"]["teoremas"]
                  and "NONE_OUTSIDE_THE_TRIO" in str(kh.get("verdict"))) if kh else True
    e = core.get("estatuto_da_prova_v391") or {}
    p1 = e.get("prova_1_kernel") or {}
    esc = F["escada"]["esperadas"]
    r["S6_escada"] = bool(p1.get("n_theorems_clean") == p1.get("n_theorems_expected") == esc and p1.get("declaracoes_auditadas") == p1.get("no_trio") == F["escada"]["declaracoes_auditadas"]
                          and ("KERNEL_%d_OF_%d_FLAGS" % (esc, esc)) in str(e.get("verdict")))
    neg_ok = True
    for k, b in (F.get("blocos") or {}).items():
        presentes = _segmentos_negacao((core.get(k) or {}).get("verdict"))
        if not set(b.get("negacoes") or []) <= presentes:
            neg_ok = False
    r["S13_negacoes_congeladas"] = neg_ok
    cu = core.get("cunhagens_" + v)
    if cu is not None:
        kn = cu.get("kernel") or {}
        a, b = list(kn.get("bandeiras") or []), list(kn.get("declaracoes_no_trio") or [])
        r["S14_cunhagens"] = bool(len(a) == 2 and a[0] == a[1] and a[0] > 0 and len(b) == 2 and b[0] == b[1] and b[0] > 0 and len(cu.get("verbatim") or {}) >= 1)
    s15 = True
    if S:
        for k, regra in (S.get("blocos") or {}).items():
            vd = str((core.get(k) or {}).get("verdict") or "")
            for t in regra.get("verdict_deve_conter") or []:
                if t not in vd:
                    s15 = False
            for t in regra.get("verdict_nao_deve_conter") or []:
                if t in vd:
                    s15 = False
            for campo in regra.get("campos") or []:
                cur = core.get(k) or {}
                for parte in campo["caminho"].split("."):
                    cur = cur.get(parte) if isinstance(cur, dict) else None
                if campo.get("par_igual") and not (isinstance(cur, list) and len(cur) == 2 and cur[0] == cur[1] and cur[0] > 0):
                    s15 = False
    r["S15_semantica_declarada"] = s15
    return all(r.values()), r


def _injetar_negacao_removida(core, F):
    """Cético 1: de UM bloco novo com negação, tira o `NOT_` do primeiro segmento negativo."""
    for k, b in (F.get("blocos") or {}).items():
        if not b.get("negacoes") or not isinstance(core.get(k), dict):
            continue
        segs = str(core[k].get("verdict") or "").split("__")
        for i, s in enumerate(segs):
            if re.search(r"(^|_)NOT_", s):
                segs[i] = s.replace("NOT_", "", 1)
                core[k]["verdict"] = "__".join(segs)
                return "%s: «NOT_» retirado de um segmento do veredito" % k
    novos = F.get("registros_novos") or []
    if novos and isinstance(core.get(novos[0]), dict):
        core[novos[0]]["all_verified"] = False
        return "%s.all_verified = False (nenhum bloco novo tem negação)" % novos[0]
    return "nada a injetar"


def _injetar_contagem(core, F):
    """Cético 2: soma 1 à escada esperada; se há cunhagens_vNNN, tira 1 de kernel.bandeiras[0]."""
    try:
        core["estatuto_da_prova_v391"]["prova_1_kernel"]["n_theorems_expected"] += 1
    except (KeyError, TypeError):
        pass
    cu = core.get("cunhagens_" + F["versao"])
    if isinstance(cu, dict):
        try:
            cu["kernel"]["bandeiras"][0] -= 1
        except (KeyError, TypeError, IndexError):
            pass
    return "n_theorems_expected + 1" + ("; cunhagens.kernel.bandeiras[0] - 1" if cu else "")


# =================================================================== a pedra
def medir_custodia_generica(oc, v, a, fatos=None, semantica_dada=None):
    """`oc` = vault\\originals_copy; `v` = «vNNN»; `a` = «vANT». `fatos`/`semantica_dada` só para replays (default: lidos do cofre, com o pino)."""
    oc = Path(oc)
    out = {"pass": False, "physical_verdict_allowed": False,
           "estatuto": "REAL(lido do cofre %s e do %s pelo nome) / dois ceticos por injecao" % (v, a)}
    try:
        cv, ca = oc / ("um_unificado_" + v), oc / ("um_unificado_" + a)
        if fatos is None:
            F, man_v = fatos_do_cofre(cv)
        else:
            F, man_v = fatos, _ler_json(cv / "CUSTODY_MANIFEST.json")
        S = semantica_dada if semantica_dada is not None else semantica_de_maior_revisao(cv, man_v)
        man_a = _ler_json(ca / "CUSTODY_MANIFEST.json")
        core, core_a = _ler_json(cv / "um_absoluto.json")["core"], _ler_json(ca / "um_absoluto.json")["core"]
        selo = _ler_json(cv / "um_absoluto_selo.json")
        pm = _ler_json(oc / ("tgl_kernel_" + v) / "tgl_kernel_proof_manifest.json")
        pm_a = _ler_json(oc / ("tgl_kernel_" + a) / "tgl_kernel_proof_manifest.json")
        pt, en, pt_a = _ler_txt(cv / "um_absoluto_pt.txt"), _ler_txt(cv / "um_absoluto_en.txt"), _ler_txt(ca / "um_absoluto_pt.txt")
        um_sha = _sha(cv / "um.py")
        um_text = _ler_txt(cv / "um.py")
    except (OSError, ValueError, KeyError) as e:
        out["erro"] = "cofre ilegivel: %r" % (e,)
        return out
    C = {}                                                   # S1..S14: cada um {ok, esperado, achado}

    def chk(id_, ok, esperado, achado):
        C[id_] = {"ok": bool(ok), "esperado": esperado, "achado": achado}

    chk("S1_identidade", F["versao"] == v and selo.get("um_version") == v and selo["sha256"]["um.py"] == F["pin"] == um_sha,
        {"versao": v, "pin16": F["pin"][:16]}, {"selo": selo.get("um_version"), "sha_um_py_16": um_sha[:16]})
    novos = sorted(k for k in core if k not in core_a)
    sumidos = sorted(k for k in core_a if k not in core)
    chk("S2_blocos_novos", novos == sorted(F["registros_novos"]) and not sumidos and sumidos == F["registros_sumidos"], F["registros_novos"], {"novos": novos, "sumidos": sumidos})
    maus = [k for k in novos if not bloco_ok(core[k])]
    chk("S3_blocos_bem_formados", not maus, [], maus)
    kf, kf_a = core.get("kernel_formalization") or {}, core_a.get("kernel_formalization") or {}
    band = [k for k in kf if k not in kf_a]
    chk("S4_bandeiras", band == F["bandeiras_novas"] and all(kf[k] is True for k in band), len(F["bandeiras_novas"]), len(band))
    sem_ok, sem = semantica(core, F, S)
    chk("S5_kh", sem["S5_kh"], F["kh"], (core.get("kh_n1_cobertura_" + v) or {}).get("lido"))
    chk("S6_escada", sem["S6_escada"], F["escada"]["texto"], "ver estatuto_da_prova_v391")
    fm, ar = pm["formal_files_sha256"], pm["axiom_report"]
    fm_a = pm_a["formal_files_sha256"]
    fora = [k for k, x in ar.items() if set(x or []) - set(TRIO)]
    chk("S7_kernel", len(fm) == F["kernel"]["formais"] and len(ar) == F["kernel"]["declaracoes"] and not fora
        and sorted(set(fm) - set(fm_a)) == F["kernel"]["modulos_novos"] and not (set(fm_a) - set(fm)),
        {"formais": F["kernel"]["formais"], "declaracoes": F["kernel"]["declaracoes"]}, {"formais": len(fm), "declaracoes": len(ar), "fora_do_trio": len(fora)})
    reg_pt, reg_en, reg_a = dict(RE_REG.findall(pt)), dict(RE_REG.findall(en)), dict(RE_REG.findall(pt_a))
    mud = sorted(k for k in reg_a if reg_pt.get(k) != reg_a[k])
    permitidos = {m["nome"] for m in ((S or {}).get("mudados_permitidos") or [])}
    mud_ruins = []
    for k in mud:
        va, vb = (core.get(k) or {}).get("verdict"), (core_a.get(k) or {}).get("verdict")
        if not (va is not None and vb is not None and _norm(va) == _norm(vb)) and k not in permitidos:
            mud_ruins.append(k)
    chk("S8_registro", len(reg_pt) == len(reg_en) == F["registro"]["pt"] and len(reg_a) == F["registro"]["anterior"] and all(k in reg_pt for k in reg_a)
        and sorted(k for k in reg_pt if k not in reg_a) == novos and mud == [m["nome"] for m in F["registro"]["mudados"]] and not mud_ruins,
        {"pt": F["registro"]["pt"], "mudados": [m["nome"] for m in F["registro"]["mudados"]]}, {"pt": len(reg_pt), "en": len(reg_en), "mudados": mud, "fora_do_padrao": mud_ruins})
    gate = ((core.get("qg_closure") or {}).get("gate") or {})
    chk("S9_gate", gate.get("full_static_witness_exists") is False and str(selo.get("qg_closure_verdict")) == str(man_a.get("gate")) == str(F["gate"]),
        "gate identico ao do cofre " + a, str(selo.get("qg_closure_verdict"))[:60])
    confs = [k for k, x in selo.items() if str(k).endswith("_verdict") and RX_CONF.search(str(x))]
    chk("S10_sem_CONFIRMED", not confs, [], confs)
    contratos = _contratos(um_text)
    chk("S11_contratos", contratos == F["contratos_expected_ladder"] and all(x == F["escada"]["esperadas"] for x in contratos.values()),
        F["escada"]["esperadas"], contratos)
    mono = (F["kernel"]["formais"] >= F["kernel"]["formais_anterior"] and F["kernel"]["declaracoes"] >= F["kernel"]["declaracoes_anterior"]
            and F["escada"]["esperadas"] >= F["escada_anterior"]["esperadas"] and F["registro"]["pt"] >= F["registro"]["anterior"]
            and F["kh"]["constantes"] >= F["kh"]["constantes_anterior"] and F["kh"]["teoremas"] >= F["kh"]["teoremas_anterior"] and not F["kernel"]["modulos_removidos"])
    chk("S12_monotonia", mono, "formais, declaracoes, escada, registro e kh nao diminuem", "ver fatos")
    chk("S13_negacoes", sem["S13_negacoes_congeladas"], {k: b.get("negacoes") for k, b in (F.get("blocos") or {}).items()}, "ver veredito dos blocos")
    if "S14_cunhagens" in sem:
        chk("S14_cunhagens", sem["S14_cunhagens"], "kernel.bandeiras e declaracoes_no_trio com par igual e > 0", (core.get("cunhagens_" + v) or {}).get("kernel"))
    chk("S15_semantica", sem["S15_semantica_declarada"], "SEMANTICA_CUSTODIA", "REVISADA rev%s" % (S or {}).get("revisao", "?") if (S or {}).get("revisor") else "DECLARADO (sem revisao)")
    c1 = copy.deepcopy(core)
    inj1 = _injetar_negacao_removida(c1, F)
    cet1 = (semantica(c1, F, S)[0] is False)
    c2 = copy.deepcopy(core)
    inj2 = _injetar_contagem(c2, F)
    cet2 = (semantica(c2, F, S)[0] is False)
    ok = bool(all(x["ok"] for x in C.values()) and cet1 and cet2)
    out.update({
        "blocos_novos_desde_" + a: {"n": len(novos), "nomes": novos, "sumidos": sumidos, "fora_da_regra": maus, "ok": C["S2_blocos_novos"]["ok"] and C["S3_blocos_bem_formados"]["ok"]},
        "bandeiras_novas_desde_" + a: {"n": len(band), "ok": C["S4_bandeiras"]["ok"]},
        "registros_" + v: {"ok": all(C[k]["ok"] for k in ("S5_kh", "S6_escada", "S13_negacoes", "S15_semantica")), "estatuto": "lidos do cofre e conferidos contra o FATOS_CUSTODIA congelado"},
        "ceticos": {"1_injecao": inj1, "1_reprovou": cet1, "2_injecao": inj2, "2_reprovou": cet2,
                    "leitura": "se uma injecao NAO reprovasse, o check nao discriminaria e a pedra reprovaria"},
        "gate": {"full_static_witness_exists": gate.get("full_static_witness_exists"), "identico_ao_cofre_" + a: C["S9_gate"]["ok"]},
        "registro_de_vereditos": {"pt": len(reg_pt), "en": len(reg_en), "esperado": F["registro"]["pt"], "nomes_" + a: len(reg_a), "novos": len(novos),
                                  "mudados_desde_" + a: mud, "ok": C["S8_registro"]["ok"]},
        "kernel": {"formais": len(fm), "termos": len(ar), "ok": C["S7_kernel"]["ok"]},
        "vereditos_do_selo_com_CONFIRMED": confs,
        "semantica": ("REVISADA rev%s" % S.get("revisao")) if (S and S.get("revisor")) else "DECLARADO (sem revisao)",
        "fatos_sha16": hashlib.sha256(json.dumps(F, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()[:16],
        "checks": C,
        "nao_se_afirma": ["que a TGL esteja discriminada do LCDM a 5 sigma (o degrau da creditacao nao foi alcancado)", "que ln B seja sigma",
                          "qual leitura da paridade da patente ACOM Mirror e canonica (decisao do operador [LEGAL])",
                          "qualquer veredito fisico (physical_verdict_allowed=False; gate INALTERADO)"] + list((S or {}).get("nao_se_afirma_extra") or []),
        "pass": ok})
    return out
