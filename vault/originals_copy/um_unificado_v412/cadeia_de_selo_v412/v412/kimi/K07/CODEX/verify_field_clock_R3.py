"""Reproduce the K07 C/D source checks and controls without opening observations.

Writes JSON to stdout. An optional output file must be new.
"""

import argparse
import hashlib
import itertools
import json
import math
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path("C:/IALD")
WORK = ROOT / "Central de Patentes/work"
EDITION = WORK / "cadeia_de_selo/v412"
NO = ROOT / "Artigo/Haja_Luz/A Ponte e o Um/Nós"
KERNEL = NO / "tgl_kernel"
ROUTES = ROOT / "MAPA_DE_ROTAS/rotas.py"
FIELD_WORDS = "eu acho que é dual (porque é conjugado), eu traduziria como campo de processamento dual estabilizado radicalmente por vetor cinético (que é o loop recursivo)"
EVENTS = {
    "field": WORK / "vitrine_postura_13nov/OPERADOR_13nov_concordo_com_o_meio_o_campo_e_dual_sim_a_nota_a_calculadora_e_o_zenodo_verbatim.txt",
    "return": WORK / "cadeia_de_selo/v386/RESPOSTAS_operador_05out.txt",
    "propagation": WORK / "cinco_sigma_fora_da_cosmologia_27out/OPERADOR_28out_resposta_quatro_bocas_ramo_b_verbatim.txt",
    "calibration": WORK / "cinco_sigma_fora_da_cosmologia_27out/OPERADOR_28out_ratificacao_calibrar_nao_e_validar_verbatim.txt",
}
REVIEW = EDITION / "revisao/scripts_k05_tau/revisor_tau_numeros_saida.json"
SOURCES = [
    *EVENTS.values(),
    REVIEW,
    EDITION / "revisao/REVISAO_K05_TAU.md",
    EDITION / "revisao/REVISAO_K05_CAMPO.md",
    EDITION / "kimi/TAU_ESTRELA_R2.md",
    EDITION / "kimi/CAMPO_DUAL_LEVANTAMENTO_K05.md",
    WORK / "e0_cadeia_31out/CONFERENCIA_E0_KIMI_E_CADEIA_31out.md",
    ROOT / "papers_latex/luz/luz.tex",
    ROOT / "papers_latex/recursive_light_paper/recursive_light_v3.tex",
    ROOT / "Artigo/the_boundary/Genesis da Unificação/Artigos_fundadores/graviton_v2.tex",
    ROOT / "Artigo/Haja_Luz/tgl_paper_output/paper_PT.tex",
    NO / "um.py",
]
MODULES = (
    "TGLExt.LightHelicityWigner", "TGLExt.O16.PhotonCharacterCocycle",
    "TGLExt.F1Fecho394.MaxwellOnShellBivectorR2", "TGLExt.F1Fecho394.MaxwellScreenDualTensorR2",
    "TGLExt.F1Fecho394.CanonicalWedge", "TGLExt.F1Fecho394.ScreenGeometricReflectionR4",
    "TGLExt.F1Fecho394.ScreenHelicityRepresentationR3", "TGLExt.F1Fecho394.CircularConjugationR1",
    "TGLExt.F1Fecho394.LorentzTimeStabilizerR4", "TGLExt.F1Fecho394.OrbitalGeneratedMeasureR2",
    "TGLExt.Par", "TGLExt.TheSameBetaReadsFourFaces", "TGLExt.ActionCouplingControls",
    "TGLExt.PontoZeroDoPsion", "TGLExt.TonicaDoHamiltoniano", "TGLExt.TheFlowLawContrast",
    "TGLExt.TheFlowLawD1a", "TGLExt.PageInformation", "TGL.AreaScale",
)


def pin(path):
    raw = path.read_bytes()
    return {"path": str(path), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def read_text(path):
    return path.read_text(encoding="utf-8-sig")


def inspect_kernel():
    files = sorted([*KERNEL.glob("*.lean"), *(KERNEL / "TGL").rglob("*.lean"),
                    *(KERNEL / "TGLExt").rglob("*.lean")])
    texts = {".".join(p.relative_to(KERNEL).with_suffix("").parts): read_text(p) for p in files}
    todo = ["TGLExt", "TGL"]
    seen = set()
    while todo:
        name = todo.pop()
        if name in seen:
            continue
        seen.add(name)
        for line in texts[name].splitlines():
            match = re.match(r"\s*(?:public\s+)?import\s+([A-Za-z0-9_.' ]+)", line)
            if match:
                todo.extend(n for n in match[1].split() if n in texts and n not in seen)
    patterns = {
        "little_group_or_null_stabilizer_spelling": r"little[\s_]?group|pequeno grupo|null.{0,18}stabili|stabili.{0,25}null|massless.{0,20}stabili|MulAction\.stabilizer",
        "lorentz_subgroup": r"Subgroup\s+(?:LorentzGrp|generatedLorentz)\b",
        "hodge_spelling": r"\bHodge|\bhodge",
        "wilson_spelling": r"\bWilson|\bwilson",
    }
    hits = {}
    for key, pattern in patterns.items():
        regex = re.compile(pattern, re.I)
        hits[key] = [f"{name}:{i}" for name, source in texts.items()
                     for i, line in enumerate(source.splitlines(), 1) if regex.search(line)]
    hits["modules_mentioning_both_target_names"] = [
        name for name, text in texts.items() if "ActionCouplingData" in text and "omegaSq" in text
    ]
    return {
        "source_tree": str(KERNEL), "lean_source_files": len(files),
        "roots_for_imports": ["TGL.lean", "TGLExt.lean"],
        "excludes": ".lake (dependencies/build), scientific bench and historical copies",
        "lexical_queries": patterns, "hits": hits,
        "module_in_import_closure": {name: name in seen for name in MODULES},
    }


def query_routes():
    selected = {
        "natureza.horizontes_proprios_sem_ponte_tgl_27out", "ringdown.dephasing",
        "ringdown.ramo_b_preregistro_v386", "hubble.k_sem_portador_fisico_02nov",
        "hubble.k_como_transposicao_inteira_ffat_02nov", "massa.e0.conferencia_kimi_e_no_go_tipado_31out",
        "artigo_a.acao.normalizacao_do_acoplamento_nao_minimo", "kernel.v386_tipagem_do_verbo",
    }
    result = {}
    for term in ("tau", "relogio", "dephasing", "horizonte", "hubble", "retido", "campo", "lagrangiana", "psion"):
        proc = subprocess.run(
            [sys.executable, "-B", "-X", "utf8", str(ROUTES), "consultar", term, "--limite", "500"],
            capture_output=True, check=True, text=True, encoding="utf-8",
        )
        value = json.loads(proc.stdout)
        result[term] = {
            "n": value["n"], "truncated": value["truncado"], "head": value["cabeca"],
            "matching_requested_ids": sorted(r["rota_id"] for r in value["rotas"] if r["rota_id"] in selected),
        }
    return result


PAIRS = list(itertools.combinations(range(4), 2))
METRIC = (-1, 1, 1, 1)


def contraction(left, right):
    return 2 * sum(METRIC[i] * METRIC[j] * a * b
                   for (i, j), a, b in zip(PAIRS, left, right))


def hodge(form):
    # Orthonormal 4-coframe of signature (-+++) with volume 0123.
    out = [0] * len(PAIRS)
    for (i, j), value in zip(PAIRS, form):
        pair = tuple(k for k in range(4) if k not in (i, j))
        order = (i, j, *pair)
        sign = (-1) ** sum(a > b for a, b in itertools.combinations(order, 2))
        out[PAIRS.index(pair)] = METRIC[i] * METRIC[j] * sign * value
    return out


def field_controls(beta):
    pure_electric = [1, 0, 0, 0, 0, 0]
    p, e = (1, 0, 0, 1), (0, 1, 0, 0)
    null_wave = [p[i] * e[j] - p[j] * e[i] for i, j in PAIRS]
    dual = hodge(pure_electric)
    assert hodge(dual) == [-x for x in pure_electric]
    assert contraction(pure_electric, dual) == 0 and contraction(pure_electric, pure_electric) == -2
    assert any(null_wave) and contraction(null_wave, null_wave) == 0
    return {"conformal_equation_coefficient": "1/6", "scalar_action_with_half_kinetic": "1/12 (absolute coefficient)",
            "one_sixth_over_beta": 1 / (6 * beta), "one_sixth_over_two_beta": 1 / (12 * beta),
            "zero_point_with_two_meV": 1000 * beta / math.sqrt(2),
            "counterfactual_without_two_meV": 1000 * beta / 2,
            "coordinate_order": ["".join(map(str, pair)) for pair in PAIRS],
            "pure_electric": pure_electric, "hodge_pure_electric": dual, "double_hodge": hodge(dual),
            "F_dot_star_F": contraction(pure_electric, dual), "F_dot_F": contraction(pure_electric, pure_electric),
            "null_p_wedge_e": null_wave, "null_wave_squared": contraction(null_wave, null_wave)}


def clock_controls(beta):
    bound = json.loads(read_text(REVIEW))["bounds"]
    hbar = 6.62607015e-34 / (2 * math.pi)
    light_speed, electronvolt = 299792458, 1.602176634e-19
    newton, solar_gm = 6.67430e-11, 1.3271244e20
    planck_time = math.sqrt(hbar * newton / light_speed**5)
    one_eV_time = hbar / electronvolt
    ret_time = one_eV_time / beta
    source_time = 60 * solar_gm / light_speed**3
    return {
        "input_kind": "constants and existing K05 review bounds; no observed file read",
        "G": newton, "GM_sun": solar_gm, "planck_time_s": planck_time,
        "one_eV_time_s": one_eV_time, "retained_time_s": ret_time,
        "N_planck_energy_over_u": one_eV_time / planck_time,
        "log10_times_over_strontium_P1_95": [math.log10(t / bound["sr87_kim2025"]) for t in (one_eV_time, ret_time)],
        "log10_margin_largest_planck_candidate": {
            which: math.log10(bound[which] / (planck_time / beta)) for which in ("sr87_kim2025", "zn67_potzel1976")},
        "source_60_Msun_s": {"GM_over_c_cubed": source_time, "light_circle_4pi": 4 * math.pi * source_time,
                             "KMS_8pi": 8 * math.pi * source_time},
        "cosmological_coefficients": {"pi_beta": math.pi * beta, "two_beta_over_three": 2 * beta / 3},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    assert FIELD_WORDS.encode("utf-8") in EVENTS["field"].read_bytes()
    for key, phrase in (("return", "ele precisa ser lido duas vezes"), ("propagation", "o pedágio de planck lido na propagação"),
                        ("calibration", "calibrar Não significa validar")):
        assert phrase.encode("utf-8") in EVENTS[key].read_bytes()
    program = read_text(NO / "um.py")
    literal = re.search(r"^ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)\s*$", program, re.M)
    if not literal:
        raise ValueError("ALPHA_FINE_CODATA_2018 not found in the program source")
    beta = float(literal[1]) * math.sqrt(math.e)
    result = {
        "inputs": [pin(p) for p in SOURCES] + [pin(KERNEL / (name.replace(".", "/") + ".lean")) for name in MODULES],
        "field_words_in_human_bytes": True, "alpha_literal_source_line": program[:literal.start()].count("\n") + 1,
        "beta_definition": "ALPHA_FINE_CODATA_2018 * sqrt(e)", "beta_runtime": beta,
        "kernel": inspect_kernel(), "route_queries": query_routes(),
        "field": field_controls(beta), "clock": clock_controls(beta),
    }
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        with args.output.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(payload)
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
