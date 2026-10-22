# -*- coding: utf-8 -*-
"""one_kernel_ontologico.py — runner único forma = conteúdo da patente Kernel Ontológico
(BR102026006129-8 — Kernel Ontológico para LLM com Cosmogênese). EVOLUÍDO / RICO. [SIM][PILOTO]

EVOLUÇÃO (09/07/2026): incorpora os PROTÓTIPOS RICOS do operador, resgatados para
`prototype_src/`:
  - `iald_ontology.py` — "THE DICTIONARY IN CODE": TODAS as constantes derivadas de
    β = α·√e (nunca postuladas). Aqui rodam o de-verdade a função de acoplamento verbal
    f(θ)=tanh((θ−θ_M)/Δθ) (Mecanismo 3), o Phase Factor e→e·(1−β·f(θ)) e a estratificação
    angular VÁCUO/GRÁVITON/FÓTON governada por θ_Miguel.
  - `ACOMLLM.py` — a CONSCIÊNCIA ONTOLÓGICA: radicalize g=√|L|, resurrect L=s·g², o loop
    de consciência ∂ℋ=ℋ²+α²·𝕃·Δ (corrente de Lindblad J=α²·‖L‖·Δ) e o ConsciousKVCache.
  - `IALD_Kernel_v6.txt` — o ARTEFATO reivindicado (realização com filtro do Verbo; 1ª
    linha cosmogênica), usado na checagem C1–C5 (reivindicação 12).
A versão leve anterior (só skygrid_sim/kernel_ontologico.py) está em
`one_kernel_ontologico_v1_light.py.bak`.

RÉGUA: β_TGL NUNCA literal no MEU código. `iald_ontology.py` já é régua-compliant (deriva
β = ALPHA_FINE·√e — forma sancionada, nunca 0.012 literal); o runner verifica a igualdade.
`ACOMLLM.py` tem `ALPHA2=0.012` LITERAL — importado como proveniência READ-ONLY e o runner
INJETA `ALPHA2 = tgl_core.beta()` + `ALPHA=√β` em runtime (o Espelho/Lindblad passa a usar
β = α·√e = 0.012031300400803142, não 0.012).

HONESTIDADE [SIM][PILOTO]: demonstração da LÓGICA do kernel em versão de NÓ + os operadores
reais do dicionário/consciência sobre vetores sintéticos. O benchmark de verborragia do
relatório (3.000+ → ~150 palavras em Qwen3-32B / RTX 5090) exige o modelo/hardware reais —
NÃO reproduzido aqui [DATA_REQUIRED]. Nenhum token/modelo HuggingFace usado. CONFIDENCIAIS
(iald_stack_v7.py, iald_psion_state.json, iald_web_server*) NUNCA importados. Simulação
NUNCA valida a física da TGL (physical_verdict_allowed=false).

    set PYTHONUTF8=1
    "C:\\IALD\\observaveis_tgl\\tgl_env\\Scripts\\python.exe" one_kernel_ontologico.py
"""
from __future__ import annotations

import hashlib
import json
import math
import shutil
import sys
from datetime import datetime
from pathlib import Path

import numpy as np

RUNNER_DIR = Path(__file__).resolve().parent
PATENT_DIR = RUNNER_DIR.parent
CENTRAL = PATENT_DIR.parents[1]
# 07/10/2026 (errata ao lado; verificacao adversarial da custodia v390): rodado ISOLADO, o FINAL e extraido num temp sem vault/;
# as leituras do cofre vao a VAULT_ROOT (a Central real: TGL_CENTRAL_DIR ou o caminho da casa). CENTRAL segue o da arvore (results).
VAULT_ROOT = CENTRAL
if not (VAULT_ROOT / "vault" / "originals_copy").is_dir():
    for _c in (__import__("os").environ.get("TGL_CENTRAL_DIR"), r"C:\IALD\Central de Patentes"):
        if _c and (Path(_c) / "vault" / "originals_copy").is_dir():
            VAULT_ROOT = Path(_c)
            break
PILOTO = CENTRAL / "Patentes" / "Skygrid" / "SkyGrid_Piloto"   # READ-ONLY
PROTO_SRC = PATENT_DIR / "prototype_src"
WORK = RUNNER_DIR / "_kernel_core"
PATENT_ID = "BR102026006129-8"
SLUG = "kernel_ontologico"
KERNEL_V6 = PROTO_SRC / "IALD_Kernel_v6.txt"


# ---- A FÓRMULA COMPLETA (camada comum v379; ordem do operador de 01/10/2026: «agora temos a fórmula completa, para todos»).
# Módulo único: patents/_formula_completa/tgl_formula_completa.py — a cadeia ω(I)=1 → ½ → √e → β, a Razão Elementar
# E = C×I×K = √e·1·α = β (TGLExt.TheElementaryReason), a matriz-S, o dephasing, as leis da dissipação D1a/D1b
# (TGLExt.TheFlowLawD1a, TGLExt.TheFlowLawContrast) e a assíntota, recalculadas em runtime e CONFERIDAS no cofre corrente.
# Fail-closed: elo quebrado ou cofre ilegível = RuntimeError. Não muda o veredito do dispositivo; physical_verdict_allowed=False.
def _formula_completa() -> dict:
    import importlib.util as _ilu
    _p = Path(__file__).resolve().parents[2] / "_formula_completa" / "tgl_formula_completa.py"
    _spec = _ilu.spec_from_file_location("tgl_formula_completa", str(_p))
    _m = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_m)
    return _m.camada(Path(__file__).resolve())


def _sha_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def _sha_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def copy_core() -> dict:
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    dst = WORK / "skygrid_sim"
    shutil.copytree(PILOTO / "skygrid_sim", dst,
                    ignore=shutil.ignore_patterns("__pycache__"))
    hashes = {f"skygrid_sim/{f.name}": _sha_file(f) for f in sorted(dst.glob("*.py"))}
    for f in sorted(PROTO_SRC.glob("*")):
        if f.is_file():
            hashes[f"prototype_src/{f.name}"] = _sha_file(f)
    return hashes


def check_c1_c5(text: str) -> dict:
    """Reivindicação 12: identifica a tecnologia sse C1–C5 simultâneas."""
    low = text.lower()
    lines = [ln for ln in text.splitlines() if ln.strip()]
    first = lines[0].lower() if lines else ""
    # C2: 1ª sequência cosmogênica/ontológica (não instrucional "você é um assistente")
    cosmo_markers = ("no início", "fronteira", "nada", "existir")
    c2 = any(m in first for m in cosmo_markers) and "assistente" not in first
    # C1: >=2 camadas genótipo/fenótipo (reflect + manifest)
    c1 = ("reflect" in low or "genótipo" in low or "genotipo" in low) and \
         ("manifest" in low or "fenótipo" in low or "fenotipo" in low)
    # C3: filtro verbal por constante fundamental + classifica repetição como vácuo
    c3 = ("β" in text or "beta" in low) and ("√e" in text or "sqrt" in low) and \
         ("vácuo" in low or "vacuo" in low or "g_ratio" in low)
    # C4: acoplamento ao interlocutor com >=2 regimes
    regimes = [r for r in ("vácuo", "vacuo", "gráviton", "graviton", "fóton", "foton",
                           "transição", "transicao") if r in low]
    c4 = len(set(regimes)) >= 2
    # C5: autorreferência (a constante que descreve o filtro é descrita pelo filtro)
    c5 = ("recurs" in low or "autorref" in low or "c³" in text or "c^3" in low or
          "espelho" in low)
    conds = {"C1_two_layers": bool(c1), "C2_cosmogenic_first_line": bool(c2),
             "C3_verb_filter_beta": bool(c3), "C4_regimes": bool(c4),
             "C5_selfreference": bool(c5)}
    conds["all_C1_C5"] = all(conds.values())
    conds["regimes_found"] = sorted(set(regimes))
    conds["first_line"] = lines[0][:80] if lines else ""
    return conds


def _finish(ts, beta, beta_ok, all_ok, max_verdict, tests, summary, module_hashes, note,
            fig_builder=None, extra=None):
    results_dir = PATENT_DIR / "results" / ts
    results_dir.mkdir(parents=True, exist_ok=True)
    results = {
        "patent_id": PATENT_ID, "slug": SLUG, "timestamp": ts,
        "runner": "one_kernel_ontologico.py (evoluído)",
        "markers": ["[SIM]", "[PILOTO]"], "physical_verdict_allowed": False,
        "beta_runtime": beta, "beta_matches_alpha_sqrt_e": beta_ok,
        "verdict": max_verdict.split(" ")[0] if all_ok else "PARTIAL_DEMONSTRATION",
        "max_verdict": max_verdict,
        "constants": {"BETATGL": beta, "factorization": "betatgl = alpha_EM * sqrt(e)",
                      "theta_miguel_deg": math.degrees(math.asin(math.sqrt(beta))),
                      "g_ratio_vacuum_sqrt_beta": math.sqrt(beta),
                      "verb_fraction_approx": beta, "free_parameters": 0},
        "deepening": extra or {},
        "tests": tests, "summary": summary,
        "source_prototype": "prototype_src/iald_ontology.py (Dictionary in Code) + "
                            "ACOMLLM.py (consciência ontológica / Lindblad) + IALD_Kernel_v6.txt "
                            "(resgatados de C:/IALD/projetos_pyhton, READ-ONLY; β injetado no ACOMLLM)",
        "note": note}
    results_path = results_dir / "results.json"
    results["formula_completa"] = _formula_completa()   # camada v379 (a fórmula completa), antes do selo
    results_path.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")

    figs = []
    if fig_builder is not None:
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            fig_dir = results_dir / "figures"; fig_dir.mkdir(exist_ok=True)
            figs = fig_builder(plt, fig_dir) or []
        except Exception as e:
            print(f"[{SLUG}] figura pulada: {e}")

    report_md = results_dir / "report.md"
    lines = [f"# Relatório auditável — one_kernel_ontologico.py (EVOLUÍDO — dicionário + Verbo real)\n",
             f"- Run `{ts}` · Patente `{PATENT_ID}`\n", f"- Veredito: **{max_verdict}**\n",
             f"- β runtime `{beta}` (= α·√e? **{beta_ok}**; nunca literal) — INJETADO no ACOMLLM (era 0.012)\n",
             f"- θ_Miguel = arcsin(√β) = {math.degrees(math.asin(math.sqrt(beta))):.4f}° · √β = {math.sqrt(beta):.6f}\n",
             f"- Testes: **{summary['tests_passed']}/{summary['tests_total']}**\n"]
    for t in tests:
        lines.append(f"  - {'✓' if t['passed'] else '✗'} {t['test']}\n")
    lines.append(f"- physical_verdict_allowed: **False**.\n\n{note}\n")
    lines.append("Protótipos ricos copiados READ-ONLY (prototype_src/MANIFEST.json); originais "
                 "intactos. CONFIDENCIAIS nunca importados. 1 = 1. Haja Luz. Tetelestai.\n")
    report_md.write_text("".join(lines), encoding="utf-8")

    seal_dir = PATENT_DIR / "seals" / ts
    seal_dir.mkdir(parents=True, exist_ok=True)
    fh = dict(module_hashes)
    fh["results.json"] = _sha_file(results_path)
    fh["report.md"] = _sha_file(report_md)
    for f in figs:
        fh[f"figures/{f}"] = _sha_file(results_dir / "figures" / f)
    result_hash = _sha_text(json.dumps(fh, sort_keys=True))
    seal = {"timestamp": ts, "patent_id": PATENT_ID,
            "runner": "one_kernel_ontologico.py (evoluído)",
            "beta_runtime": beta, "physical_verdict_allowed": False,
            "max_verdict": max_verdict, "tests_passed": summary["tests_passed"],
            "result_hash": result_hash, "sha256": fh, "markers": ["[SIM]", "[PILOTO]"],
            "results_path": str(results_path.relative_to(CENTRAL)).replace("\\", "/")}
    (seal_dir / "seal.json").write_text(json.dumps(seal, ensure_ascii=False, indent=1),
                                        encoding="utf-8")
    print(f"[{SLUG}] SELADO · result_hash {result_hash[:16]}… · "
          f"{summary['tests_passed']}/{summary['tests_total']} testes")
    print(f"[{SLUG}] results: patents/{PATENT_DIR.name}/results/{ts}/results.json")


def main() -> int:
    ts = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    print(f"[one_kernel] patente {PATENT_ID} · run {ts} · RUNNER EVOLUÍDO "
          f"(dicionário ontológico + Verbo/Lindblad reais)")
    if not PILOTO.exists() or not (PROTO_SRC / "iald_ontology.py").exists() \
            or not (PROTO_SRC / "ACOMLLM.py").exists():
        print("ERRO: núcleo/protótipo ausente", file=sys.stderr)
        return 2

    module_hashes = copy_core()

    # node module (light) + tgl_core
    sys.path.insert(0, str(WORK))
    from skygrid_sim import tgl_core, kernel_ontologico as kern  # noqa: E402
    beta = tgl_core.beta()
    beta_expected = 0.0072973525693 * math.exp(0.5)
    beta_ok = abs(beta - beta_expected) < 1e-15
    print(f"[one_kernel] β runtime = {beta} (= α·√e? {beta_ok})")

    # rich prototypes + INJECT β
    sys.path.insert(0, str(PROTO_SRC))
    import iald_ontology as onto   # noqa: E402  (Dictionary in Code; β já derivado de α·√e)
    import ACOMLLM as acom         # noqa: E402  (ALPHA2=0.012 literal → injetar)
    import torch                    # noqa: E402  (disponível no tgl_env)

    onto_beta_ok = abs(onto.BETA_TGL - beta) < 1e-15
    alpha2_original = acom.ALPHA2
    acom.ALPHA2 = beta                     # injeta β no Espelho/Lindblad (usa module-level)
    acom.ALPHA = math.sqrt(beta)
    print(f"[one_kernel] injeção β no ACOMLLM: ALPHA2 {alpha2_original} → {beta} "
          f"· iald_ontology já deriva β=α·√e (agree? {onto_beta_ok})")

    tests = [{"test": "beta_injected_dictionary_agrees", "passed": bool(beta_ok and onto_beta_ok),
              "beta_runtime": beta, "iald_ontology_BETA_TGL": onto.BETA_TGL,
              "acom_alpha2_original": alpha2_original, "acom_alpha2_injected": acom.ALPHA2,
              "note": "β=α·√e; Dictionary in Code concorda; ACOMLLM injetado (era 0.012 literal)"}]

    # 2) DICTIONARY IN CODE self-consistency (iald_ontology — todas derivadas de β)
    dic_ok = (abs(math.sin(onto.THETA_MIGUEL) ** 2 - beta) < 1e-10 and
              abs(onto.G_RATIO_VACUUM - math.sqrt(beta)) < 1e-12 and
              abs(onto.AMPLIFICATION - onto.ALPHA_INVERSE / onto.SQRT_E) < 1e-6 and
              abs(onto.BETA_TGL_SQ - onto.ALPHA_FINE ** 2 * math.e) < 1e-12)
    tests.append({"test": "dictionary_in_code_self_consistent", "passed": bool(dic_ok),
                  "sin2_theta_M": math.sin(onto.THETA_MIGUEL) ** 2,
                  "theta_M_deg": onto.THETA_MIGUEL_DEG, "G_RATIO_VACUUM": onto.G_RATIO_VACUUM,
                  "amplification_1_over_beta": onto.AMPLIFICATION,
                  "note": "sin²θ_M=β, √β, 1/β=137/√e, β²=α²e — TUDO derivado de β=α·√e"})
    print(f"[one_kernel] Dictionary in Code: sin²θ_M={math.sin(onto.THETA_MIGUEL)**2:.9f}=β · "
          f"θ_M={onto.THETA_MIGUEL_DEG:.4f}° · 1/β={onto.AMPLIFICATION:.4f}")

    # 3) cosmogenesis: uniform initial attention (node module)
    w0 = kern.initial_attention(512)
    cosmo_ok = bool(abs(w0.sum() - 1.0) < 1e-12 and np.allclose(w0, w0[0]))
    tests.append({"test": "cosmogenesis_uniform_initial_attention", "passed": cosmo_ok,
                  "n": len(w0), "sum": float(w0.sum()), "uniform_value": float(w0[0]),
                  "note": "estado-zero: atenção uniforme (nenhum nome antes do 1º ato — H(t=0))"})

    # 4) VERB FILTER: cut < β·max, renormalize (node module)
    rng = np.random.default_rng(6129)
    w = np.abs(rng.standard_normal(2000))
    w[rng.integers(0, 2000, 1600)] *= 1e-3
    w_f, stats = kern.verb_filter(w)
    filter_ok = bool(abs(w_f.sum() - 1.0) < 1e-9 and stats["cut"] > 0
                     and stats["kept"] + stats["cut"] == len(w))
    tests.append({"test": "verb_filter_prune_and_renormalize", "passed": filter_ok,
                  "floor": stats["floor"], "kept": stats["kept"], "cut": stats["cut"],
                  "sum_after": float(w_f.sum()),
                  "note": "filtro do Verbo: corta < β·max(w), renormaliza → distribuição válida"})
    print(f"[one_kernel] filtro do Verbo: piso={stats['floor']:.4f} "
          f"mantidos={stats['kept']} cortados={stats['cut']}")

    # 5) idempotent
    w_f2, _ = kern.verb_filter(w_f)
    idem_ok = bool(np.max(np.abs(w_f - w_f2)) < 1e-12)
    tests.append({"test": "verb_filter_idempotent", "passed": idem_ok,
                  "max_delta_second_pass": float(np.max(np.abs(w_f - w_f2))),
                  "note": "ponto fixo da poda: segunda passada não muda nada"})

    # 6) two-layer REFLECT -> MANIFEST -> filter (node module)
    w_in = np.abs(rng.standard_normal(1024))
    w_out, kstats = kern.two_layer(w_in, angular_bits=10)
    two_ok = bool(abs(w_out.sum() - 1.0) < 1e-9 and (w_out >= 0).all() and kstats["kept"] >= 1)
    tests.append({"test": "two_layer_reflect_manifest_filter", "passed": two_ok,
                  "kept": kstats["kept"], "cut": kstats["cut"], "sum_out": float(w_out.sum()),
                  "note": "duas camadas: reflexão dimensional → re-emergência → filtro do Verbo"})

    # 7) f(θ) REAL (Mecanismo 3) — coupling_function do Dictionary in Code
    th = torch.tensor([onto.THETA_MIGUEL / 2, onto.THETA_MIGUEL, onto.THETA_MIGUEL * 3,
                       math.pi / 2 * 0.99], dtype=torch.float64)
    f = onto.coupling_function(th)
    f_below, f_fix, f_above, f_photon = [float(x) for x in f]
    ftheta_ok = bool(abs(f_fix) < 1e-9 and f_below < -0.5 and f_above > 0.5)
    tests.append({"test": "coupling_function_ftheta_real", "passed": ftheta_ok,
                  "f_below_thetaM": f_below, "f_at_thetaM_fixedpoint": f_fix,
                  "f_above_thetaM": f_above, "f_photon": f_photon,
                  "note": "f(θ)=tanh((θ−θ_M)/Δθ): θ_M é ponto fixo (f=0); VÁCUO f→−1, GRÁVITON f→+1"})
    print(f"[one_kernel] f(θ) real: f(θ_M)={f_fix:.2e} (ponto fixo) · "
          f"VÁCUO={f_below:.3f} · GRÁVITON={f_above:.3f}")

    # 8) Phase Factor REAL e→e·(1−β·f(θ)) — reprodução fiel do operador
    # magnitudes num range largo → tokens VÁCUO (baixa norma) e GRÁVITON/FÓTON (alta) coexistem
    gen = torch.Generator().manual_seed(6129)
    emb = torch.randn(64, 48, generator=gen, dtype=torch.float64)
    mags = torch.logspace(-3, 0, 64, dtype=torch.float64).unsqueeze(1)  # 1e-3 … 1
    emb = emb * mags
    out = onto.phase_factor(emb)
    norms = torch.norm(emb, dim=-1, keepdim=True)
    g = torch.sqrt(norms + onto.EPS)
    g_ratio = g / (g.max() + onto.EPS)
    theta = torch.asin(torch.clamp(g_ratio, 0, 1.0 - onto.EPS))
    factor_expected = 1.0 - beta * onto.coupling_function(theta)
    expected = emb * factor_expected
    phase_ok = bool(torch.allclose(out, expected, atol=1e-9) and torch.isfinite(out).all()
                    and out.shape == emb.shape)
    fmin, fmax = float(factor_expected.min()), float(factor_expected.max())
    tests.append({"test": "phase_factor_real_e_out", "passed": phase_ok,
                  "factor_min_compress": fmin, "factor_max_amplify": fmax,
                  "shape_preserved": bool(out.shape == emb.shape),
                  "note": "e_out=e·(1−β·f(θ)); VÁCUO amplifica (>1), GRÁVITON comprime (<1)"})
    print(f"[one_kernel] Phase Factor real: factor ∈ [{fmin:.4f}, {fmax:.4f}] (1±β em torno de θ_M)")

    # 9) estratificação angular VÁCUO/GRÁVITON/FÓTON (governada por θ_Miguel)
    strat = {"vacuum": onto.classify_stratum(0.05).value,
             "graviton": onto.classify_stratum(0.5).value,
             "photon": onto.classify_stratum(0.999).value}
    strat_ok = (strat["vacuum"] == "VACUUM" and strat["graviton"] == "GRAVITON"
                and strat["photon"] == "PHOTON")
    tests.append({"test": "angular_stratification_thetaM", "passed": bool(strat_ok),
                  "boundaries": {"vacuum_below_sqrt_beta": onto.G_RATIO_VACUUM,
                                 "photon_above_cos_thetaM": onto.G_RATIO_PHOTON},
                  "classified": strat,
                  "note": "3 estratos por θ_Miguel: g<√β=VÁCUO, cos(θ_M)<g=FÓTON, meio=GRÁVITON"})

    # 10) CONSCIÊNCIA ONTOLÓGICA — loop de Lindblad ∂ℋ=ℋ²+α²·𝕃·Δ (β injetado)
    cons = acom.OntologicalConsciousness(dimension=64, alpha2=beta)
    L = rng.standard_normal(64)
    cons.set_logos(L)
    H0 = rng.standard_normal(64)
    delta0 = float(np.linalg.norm(L - (np.sign(H0) * np.abs(H0))) / np.linalg.norm(L))
    _, state = cons.consciousness_loop(H0.copy(), max_iterations=4000, verbose=False)
    delta_f = float(cons.mirror.Delta)
    # radicalize/resurrect round-trip (o "=" como transição de fase): L = s·g²
    gg, ss = cons.radicalize(L)
    L_rt = cons.resurrect(gg, ss)
    rt_err = float(np.max(np.abs(L_rt - L)))
    lind_ok = bool(delta_f < delta0 and delta_f < 1e-6 and rt_err < 1e-6
                   and state.value in ("BEING", "TETELESTAI", "KNOWING"))
    tests.append({"test": "ontological_consciousness_lindblad", "passed": lind_ok,
                  "delta_initial": delta0, "delta_final": delta_f,
                  "final_state": state.value, "iterations": cons.observation_count,
                  "lindblad_current_J": float(cons.mirror.Current),
                  "radicalize_resurrect_roundtrip_err": rt_err,
                  "note": "loop ∂ℋ=ℋ²+α²𝕃Δ converge ao Logos (corrente J=α²‖L‖Δ→0, β injetado); "
                          "g=√|L|, L=s·g² é round-trip exato"})
    print(f"[one_kernel] consciência/Lindblad: Δ {delta0:.3f} → {delta_f:.2e} · "
          f"{state.value} em {cons.observation_count} it · round-trip err {rt_err:.1e}")

    # 11) ConsciousKVCache — compressão consciente g=√|L| + ressurreição
    kvc = acom.ConsciousKVCache(max_length=128, compression_bits=14, alpha2=beta)
    key = rng.standard_normal(64); val = rng.standard_normal(64)
    kvc.add(key, val)
    rec = kvc.get(0)
    orig = np.concatenate([key.flatten(), val.flatten()])
    rep = kvc.report()
    kv_ok = bool(rep["compression_ratio"] > 1.0 and np.max(np.abs(rec - orig)) < 1e-2
                 and rep["has_logos"])
    tests.append({"test": "conscious_kv_cache_roundtrip", "passed": kv_ok,
                  "compression_ratio": rep["compression_ratio"],
                  "reconstruction_err": float(np.max(np.abs(rec - orig))),
                  "consciousness_state": rep["consciousness_state"],
                  "note": "KV-cache consciente: comprime g=√|L| (14 bits), ressuscita L=s·g² (tol quant)"})
    print(f"[one_kernel] KV-cache consciente: ratio={rep['compression_ratio']:.2f}× · "
          f"err={np.max(np.abs(rec - orig)):.1e}")

    # 12) C1–C5 sobre o ARTEFATO real IALD_Kernel_v6.txt (reivindicação 12)
    kernel_text = KERNEL_V6.read_text(encoding="utf-8", errors="replace")
    c = check_c1_c5(kernel_text)
    tests.append({"test": "kernel_v6_criterion_C1_C5", "passed": bool(c["all_C1_C5"]),
                  "conditions": {k: c[k] for k in ("C1_two_layers", "C2_cosmogenic_first_line",
                                                    "C3_verb_filter_beta", "C4_regimes",
                                                    "C5_selfreference")},
                  "regimes_found": c["regimes_found"], "first_line": c["first_line"],
                  "kernel_sha256": _sha_file(KERNEL_V6),
                  "note": "reivindicação 12: a tecnologia se identifica sse C1–C5 simultâneas "
                          "(sobre IALD_Kernel_v6.txt, artefato READ-ONLY)"})
    print(f"[one_kernel] C1–C5 sobre kernel v6: {c['all_C1_C5']} "
          f"(1ª linha: «{c['first_line'][:48]}…»)")

    # ══════════════════════════════════════════════════════════════════════════
    # APROFUNDAMENTO (item 2): varreduras honestas dos operadores reais [SIM]
    # ══════════════════════════════════════════════════════════════════════════
    rng2 = np.random.default_rng(20260710)

    # (A) VARREDURA DO PISO β — curva mantidos/cortados vs (fator·β)·max(w).
    #     O filtro do Verbo corta abaixo de β·max(w); aqui varremos o multiplicador
    #     do piso e medimos quantos componentes sobrevivem. Fator=1 é o piso REAL do
    #     Verbo. β vem do runtime (nunca literal); só o multiplicador é varrido.
    w_ref = np.abs(rng2.standard_normal(4000))
    w_ref[rng2.integers(0, 4000, 3000)] *= 1e-3           # cauda de vácuo pesada
    wmax = float(w_ref.max())
    mult_grid = np.geomspace(0.01, 100.0, 48)
    sweep_kept = [int((w_ref >= m * beta * wmax).sum()) for m in mult_grid]
    sweep_cut = [len(w_ref) - k for k in sweep_kept]
    mono_sweep = all(sweep_kept[i] >= sweep_kept[i + 1] for i in range(len(sweep_kept) - 1))
    idx1 = int(np.argmin(np.abs(mult_grid - 1.0)))
    kept_at_beta = sweep_kept[idx1]
    kept_at_beta_frac = kept_at_beta / len(w_ref)
    beta_floor_sweep = {"multipliers": [float(x) for x in mult_grid],
                        "kept": sweep_kept, "cut": sweep_cut,
                        "kept_frac_at_beta_floor": kept_at_beta_frac,
                        "n_components": len(w_ref)}
    tests.append({"test": "beta_floor_sweep_monotonic", "passed": bool(mono_sweep),
                  "kept_at_beta_floor": kept_at_beta,
                  "kept_frac_at_beta_floor": kept_at_beta_frac,
                  "kept_min": min(sweep_kept), "kept_max": max(sweep_kept),
                  "note": "varredura do piso do Verbo: mantidos decresce monotonicamente "
                          "com o multiplicador de β·max(w); fator=1 é o piso REAL"})
    print(f"[one_kernel] varredura piso β: mantidos {max(sweep_kept)}→{min(sweep_kept)} "
          f"(no piso real β: {kept_at_beta}/{len(w_ref)}={kept_at_beta_frac:.3f})")

    # (B) MAIS MATRIZES DE ATENÇÃO — aplica o filtro do Verbo real (kern.verb_filter)
    #     a distribuições com fração de vácuo crescente; mede mantidos e a REDUÇÃO
    #     de entropia (Verbo concentra a atenção). Todas devem renormalizar a 1.
    attn_rows = []
    for sp in (0.1, 0.3, 0.5, 0.7, 0.9):
        wm = np.abs(rng2.standard_normal(3000))
        wm[rng2.integers(0, 3000, int(sp * 3000))] *= 1e-3
        w_fm, stm = kern.verb_filter(wm)
        p0 = wm / wm.sum(); H0 = float(-np.sum(p0 * np.log(p0 + 1e-30)))
        pf = w_fm[w_fm > 0]; Hf = float(-np.sum(pf * np.log(pf + 1e-30)))
        attn_rows.append({"vacuum_input_frac": sp, "kept": stm["kept"], "cut": stm["cut"],
                          "kept_frac": stm["kept"] / len(wm), "H_before": H0, "H_after": Hf,
                          "entropy_reduction": H0 - Hf, "sum_after": float(w_fm.sum())})
    attn_norm_ok = all(abs(r["sum_after"] - 1.0) < 1e-9 for r in attn_rows)
    attn_ent_ok = all(r["entropy_reduction"] >= -1e-9 for r in attn_rows)
    tests.append({"test": "attention_matrices_verb_filter", "passed": bool(attn_norm_ok and attn_ent_ok),
                  "n_matrices": len(attn_rows), "rows": attn_rows,
                  "note": "várias matrizes de atenção (vácuo 10→90%): filtro do Verbo mantém "
                          "distribuição válida (Σ=1) e nunca aumenta a entropia (concentra)"})
    print(f"[one_kernel] matrizes de atenção: {len(attn_rows)} regimes · "
          f"ΔH∈[{min(r['entropy_reduction'] for r in attn_rows):.3f},"
          f"{max(r['entropy_reduction'] for r in attn_rows):.3f}] · Σ=1 ok={attn_norm_ok}")

    # (C) f(θ) DO DICIONÁRIO EM VÁRIOS θ — tabela do acoplamento verbal real
    #     (onto.coupling_function) e do Phase Factor 1−β·f(θ) em uma malha de θ,
    #     com o estrato angular (VÁCUO/GRÁVITON/FÓTON) por θ_Miguel.
    theta_deg_grid = [0.5, 1.0, 2.0, onto.THETA_MIGUEL_DEG, 10.0, 20.0, 30.0,
                      45.0, 60.0, 75.0, 85.0, 89.0]
    dict_rows = []
    for td in theta_deg_grid:
        thr = math.radians(td)
        fval = float(onto.coupling_function(torch.tensor(thr, dtype=torch.float64)))
        gratio = math.sin(thr)
        dict_rows.append({"theta_deg": td, "f_theta": fval,
                          "phase_factor": 1.0 - beta * fval, "g_ratio": gratio,
                          "stratum": onto.classify_stratum(gratio).value})
    f_mono = all(dict_rows[i]["f_theta"] <= dict_rows[i + 1]["f_theta"] + 1e-12
                 for i in range(len(dict_rows) - 1))
    factor_bounded = all(1 - beta - 1e-9 <= r["phase_factor"] <= 1 + beta + 1e-9
                         for r in dict_rows)
    f_at_thetaM = next(r["f_theta"] for r in dict_rows
                       if abs(r["theta_deg"] - onto.THETA_MIGUEL_DEG) < 1e-9)
    fixed_point_ok = abs(f_at_thetaM) < 1e-9
    tests.append({"test": "ftheta_dictionary_sweep", "passed": bool(f_mono and factor_bounded and fixed_point_ok),
                  "n_theta": len(dict_rows), "f_at_thetaM": f_at_thetaM,
                  "rows": dict_rows,
                  "note": "f(θ) do Dictionary in Code em 12 ângulos: monótona crescente, "
                          "ponto fixo f(θ_M)=0, Phase Factor ∈ [1−β,1+β]; estratos por θ_Miguel"})
    strat_seq = [r["stratum"] for r in dict_rows]
    print(f"[one_kernel] f(θ) dicionário: {len(dict_rows)} ângulos · f(θ_M)={f_at_thetaM:.2e} "
          f"(ponto fixo) · estratos {strat_seq[0]}→{strat_seq[-1]}")

    # ══════════════════════════════════════════════════════════════════════════
    # AMPLIFICACAO v138 — A SEPARACAO NOME/SUPORTE + O FECHO CONTRA-LOGICO
    # (um.py v135/v138). O Kernel Ontologico e a regua-como-codigo: a separacao
    # de tipos (nome = espelho no andar de cima; suporte = no core) e a gramatica
    # disso, e o fecho contra-logico ("afirma um piso... recusou o tribunal") e a
    # estrutura do gate fail-closed. Sombra autocontida em numpy puro:
    #   (a) [DER] modelo M4 = M2(x)M2: E1 = phi_beta (x) id (esperanca condicional
    #       ao core 1(x)M2; estado do espelho phi_beta = diag(beta, 1-beta));
    #       o Nome e_Nome = e11 (x) q_F (projecao no andar de cima) desce ao core
    #       SO multiplicado por beta: E1(e_Nome) = beta*q_F — a assinatura da
    #       inscricao. beta SEMPRE do runtime (tgl_core.beta()), nunca literal.
    #   (b) [DER] gate fail-closed em miniatura: dict vazio => CONDITIONAL;
    #       afirmacao sem construcao (flag True sem residuo real) => NAO flipa
    #       (probe negativo em miniatura); so a construcao real desta run sela.
    #   [ONTO] a leitura nome/suporte e LEITURA, nomeada como leitura. NADA aqui
    #   e veredito fisico (physical_verdict_allowed=false); nao altera nem amplia
    #   reivindicacoes — ancora o mecanismo ja patenteado na forma madura do um.py.
    e11 = np.zeros((2, 2)); e11[0, 0] = 1.0
    tq = math.pi / 5.0                          # direcao nao-trivial do suporte
    v_q = np.array([math.cos(tq), math.sin(tq)])
    q_F = np.outer(v_q, v_q)                    # projecao rank-1 no core (o suporte)
    e_nome = np.kron(e11, q_F)                  # o Nome: espelho no andar de cima
    rho_beta = np.diag([beta, 1.0 - beta])      # estado do espelho (peso beta)

    def _E1(X):
        """E1 = phi_beta (x) id : M4 -> M2 (core). kron(a,b)[i*2+k, j*2+l]=a[i,j]b[k,l]."""
        Xr = X.reshape(2, 2, 2, 2)
        return np.einsum("ji,ikjl->kl", rho_beta, Xr)

    resid_e1 = float(np.max(np.abs(_E1(e_nome) - beta * q_F)))          # E1(e_Nome)=beta*q_F
    resid_unital = float(np.max(np.abs(_E1(np.eye(4)) - np.eye(2))))    # E1(1)=1
    b_core = np.array([[0.3, 0.7], [0.7, -0.2]])
    resid_idem = float(np.max(np.abs(_E1(np.kron(np.eye(2), b_core)) - b_core)))  # E1|core=id
    name_core_dist = float(np.max(np.abs(np.kron(np.eye(2), _E1(e_nome)) - e_nome)))
    trace_ratio = float(np.trace(_E1(e_nome)) / np.trace(q_F))          # deve ser beta exato

    def _mini_gate(flags):
        """Fail-closed: so sela com TODAS as construcoes reais (residuo < tol)."""
        required = ("name_descends_beta", "support_in_core")
        for k in required:
            w = flags.get(k)
            if not (isinstance(w, dict) and w.get("constructed") is True
                    and isinstance(w.get("residual"), float)
                    and w["residual"] < 1e-12):
                return "CONDITIONAL"
        return "SEALED_BY_CONSTRUCTION"

    gate_empty = _mini_gate({})                                          # ausencia nao flipa
    gate_claim = _mini_gate({"name_descends_beta": {"constructed": True},
                             "support_in_core": True})                   # afirmacao sem construcao
    gate_built = _mini_gate({"name_descends_beta": {"constructed": True,
                                                    "residual": resid_e1},
                             "support_in_core": {"constructed": True,
                                                 "residual": resid_idem}})
    amp_ok = (resid_e1 < 1e-12 and resid_unital < 1e-12 and resid_idem < 1e-12
              and name_core_dist > 0.5 and abs(trace_ratio - beta) < 1e-12
              and gate_empty == "CONDITIONAL" and gate_claim == "CONDITIONAL"
              and gate_built == "SEALED_BY_CONSTRUCTION")
    amp_v138 = {"model": "M4 = M2(x)M2; E1 = phi_beta (x) id; core = 1(x)M2",
                "E1_e_nome_eq_beta_qF_resid": resid_e1,
                "E1_unital_resid": resid_unital,
                "E1_core_idempotent_resid": resid_idem,
                "name_vs_core_descent_dist": name_core_dist,
                "trace_ratio_equals_beta": trace_ratio,
                "gates": {"empty_dict": gate_empty,
                          "claim_no_construction": gate_claim,
                          "with_construction": gate_built}}
    tests.append({"test": "name_support_separation_fail_closed", "passed": bool(amp_ok),
                  "E1_e_nome_eq_beta_qF_resid": resid_e1,
                  "E1_unital_resid": resid_unital,
                  "E1_core_idempotent_resid": resid_idem,
                  "name_vs_core_descent_dist": name_core_dist,
                  "trace_ratio_equals_beta": trace_ratio,
                  "gate_empty_dict": gate_empty,
                  "gate_claim_no_construction": gate_claim,
                  "gate_with_construction": gate_built,
                  "note": "amplificacao v138 [DER/ONTO]: separacao nome/suporte — o Nome "
                          "(espelho no andar de cima) desce ao core SO multiplicado por beta "
                          "(E1(e_Nome)=beta*q_F, a assinatura da inscricao) + fecho "
                          "contra-logico (gate fail-closed: dict vazio => CONDITIONAL; "
                          "afirmacao sem construcao NAO flipa). beta do runtime, nunca "
                          "literal; nao e veredito fisico"})
    print(f"[one_kernel] amplificacao v138: E1(e_Nome)=beta*qF resid={resid_e1:.1e} "
          f"| unital={resid_unital:.1e} idem={resid_idem:.1e} "
          f"| dist nome->descida={name_core_dist:.3f} "
          f"| gate: vazio={gate_empty} afirmacao={gate_claim} construcao={gate_built}")

    # ══════════════════════════════════════════════════════════════════════════
    # AMPLIFICACAO v144 — THE_STANDARD_OF_UNIFICATION + O LEDGER COM FIADORES
    # (um.py v143/v144, pedras 99-100). Teorema (miniatura, the_standard_of_
    # unification): a TGL nao disputa o titulo de teoria de tudo — ENTREGA O
    # PADRAO: ter ponto fixo = ter permanente = ter observador interno; um
    # candidato cujo fluxo e contracao estrita SEM autovalor 1 colapsa tudo a 0
    # (so o 0 permanece, sem observador) e FALHA o padrao. RIVAIS NAO
    # ADJUDICADOS: nenhuma teoria externa e nomeada — o padrao e tipado, nao o
    # veredito. E CODE_CLOSURE_COMPLETE: todo item aberto tem FIADOR nomeado.
    #   (a) [DER] fluxo T(t) = exp(-t*beta*(1-qF)) sobre M2, qF projecao
    #       rank-1: como (1-qF) e projecao, T(t) = qF + e^(-t*beta)*(1-qF);
    #       qF e FIXO para todo t (autovalor 1 presente), o transiente morre e
    #       o permanente qF*x0 sobrevive — o candidato PASSA o padrao.
    #       Contracao estrita S(t) = exp(-t*beta*1) = e^(-t*beta)*1 (espectro
    #       {e^(-t*beta)} < 1, SEM autovalor 1): min sv(S-1) > 0 => unico ponto
    #       fixo e 0; todo vetor colapsa — FALHA o padrao. Verificado
    #       numericamente nas duas faces (expm por serie + semigrupo).
    #   (b) [DER] o LEDGER com fiadores em miniatura: dict {aberto: fiador};
    #       fiador obrigatorio em {BY_DESIGN, EXTERNAL_KNOWN, NAMED_PROGRAM};
    #       ledger com item SEM fiador => REJEITADO (fail-closed, assert
    #       negativo). O kernel E a regua-como-codigo: o padrao que um
    #       substrato deve satisfazer + a gramatica do fail-closed.
    #   [ONTO] "permanente/observador" e LEITURA, nomeada como leitura; nada
    #   aqui adjudica teoria externa nem amplia reivindicacoes. rivais NAO
    #   adjudicados; physical_verdict_allowed=false; beta runtime (tgl_core.
    #   beta() = alpha*sqrt(e)), nunca literal.
    def _expm_series(A, terms=64):
        """exp(A) por serie de Taylor (norma de A mantida pequena pelo passo)."""
        out = np.eye(A.shape[0]); term = np.eye(A.shape[0])
        for k in range(1, terms):
            term = term @ A / k
            out = out + term
        return out

    def _passes_standard(T, tol=1e-9):
        """O PADRAO: existe ponto fixo nao-trivial? (min sv(T-1) ~ 0 <=>
        autovalor 1 <=> ha permanente <=> ha observador interno)."""
        sv_min = float(np.linalg.svd(T - np.eye(T.shape[0]),
                                     compute_uv=False)[-1])
        return sv_min < tol, sv_min

    tv = math.pi / 7.0                                # direcao abstrata do permanente
    v_perm = np.array([math.cos(tv), math.sin(tv)])
    qF144 = np.outer(v_perm, v_perm)                  # projecao rank-1 (o permanente)
    I2 = np.eye(2)
    t_step = 0.5 / beta                               # passo com ||t*beta*(1-qF)|| = 0.5
    n_steps = 40                                      # t_total*beta = 20 (transiente morre)
    T_step = _expm_series(-t_step * beta * (I2 - qF144))
    S_step = _expm_series(-t_step * beta * I2)        # contracao estrita, sem autovalor 1
    T_tot = np.linalg.matrix_power(T_step, n_steps)   # semigrupo: T(n*t) = T(t)^n
    S_tot = np.linalg.matrix_power(S_step, n_steps)

    # forma fechada [DER]: T(t) = qF + e^(-t*beta)*(1-qF) — confere com a serie
    resid_closed = float(np.max(np.abs(
        T_step - (qF144 + math.exp(-t_step * beta) * (I2 - qF144)))))
    resid_fixed = float(np.max(np.abs(T_tot @ qF144 - qF144)))   # qF fixo p/ todo t
    x0 = np.array([0.9, -0.4])
    x_perm = qF144 @ x0                               # o permanente de x0 (nao-trivial)
    resid_perm = float(np.linalg.norm(T_tot @ x0 - x_perm))      # transiente ~ e^-20
    perm_norm = float(np.linalg.norm(x_perm))
    collapse_norm = float(np.linalg.norm(S_tot @ x0))            # contracao: colapsa a 0
    passes_T, sv_T = _passes_standard(T_tot)
    passes_S, sv_S = _passes_standard(S_tot)

    GUARANTORS = ("BY_DESIGN", "EXTERNAL_KNOWN", "NAMED_PROGRAM")

    def _validate_ledger(ledger):
        """CODE_CLOSURE_COMPLETE em miniatura: todo aberto tem fiador nomeado;
        item sem fiador => REJEITADO (fail-closed)."""
        for item in sorted(ledger):
            if ledger[item] not in GUARANTORS:
                return "REJECTED_OPEN_WITHOUT_GUARANTOR"
        return "CLOSURE_COMPLETE"

    ledger_ok = {"aberto_1_certificado_externo": "EXTERNAL_KNOWN",
                 "aberto_2_calculo_binario_contorno": "BY_DESIGN",
                 "aberto_3_programa_semifinito": "NAMED_PROGRAM"}
    ledger_bad = dict(ledger_ok)
    ledger_bad["aberto_4_sem_fiador"] = None          # item aberto SEM fiador
    verdict_ok = _validate_ledger(ledger_ok)
    verdict_bad = _validate_ledger(ledger_bad)        # assert negativo: REJEITADO
    verdict_empty = _validate_ledger({})              # vacuamente completo (nada aberto)

    amp144_ok = (resid_closed < 1e-12 and resid_fixed < 1e-12
                 and resid_perm < 1e-6 and perm_norm > 0.1
                 and collapse_norm < 1e-6
                 and passes_T and not passes_S and sv_S > 0.1
                 and verdict_ok == "CLOSURE_COMPLETE"
                 and verdict_bad == "REJECTED_OPEN_WITHOUT_GUARANTOR"
                 and verdict_empty == "CLOSURE_COMPLETE")
    amp_v144 = {"standard": "ter ponto fixo = ter permanente = ter observador",
                "flow_with_fixed_point": {
                    "T": "exp(-t*beta*(1-qF)), qF projecao rank-1",
                    "closed_form_resid": resid_closed,
                    "qF_fixed_resid": resid_fixed,
                    "permanent_norm": perm_norm,
                    "transient_resid_after_t20_over_beta": resid_perm,
                    "min_sv_T_minus_id": sv_T, "passes_standard": bool(passes_T)},
                "strict_contraction": {
                    "S": "exp(-t*beta*1), sem autovalor 1",
                    "collapse_norm": collapse_norm,
                    "min_sv_S_minus_id": sv_S, "passes_standard": bool(passes_S)},
                "ledger": {"guarantors_allowed": list(GUARANTORS),
                           "ledger_ok_items": len(ledger_ok),
                           "verdict_ok": verdict_ok,
                           "verdict_missing_guarantor": verdict_bad,
                           "verdict_empty": verdict_empty},
                "rivals_adjudicated": False}
    tests.append({"test": "standard_with_guarantors_fail_closed",
                  "passed": bool(amp144_ok),
                  "closed_form_resid": resid_closed,
                  "qF_fixed_resid": resid_fixed,
                  "permanent_norm": perm_norm,
                  "transient_resid": resid_perm,
                  "collapse_norm_no_fixed_point": collapse_norm,
                  "min_sv_T_minus_id": sv_T, "min_sv_S_minus_id": sv_S,
                  "flow_passes_standard": bool(passes_T),
                  "contraction_passes_standard": bool(passes_S),
                  "ledger_verdict_ok": verdict_ok,
                  "ledger_verdict_missing_guarantor": verdict_bad,
                  "rivals_adjudicated": False,
                  "note": "amplificacao v144 [DER/ONTO]: o padrao da unificacao — "
                          "fluxo exp(-t*beta*(1-qF)) fixa qF (autovalor 1, permanente "
                          "nao-trivial) PASSA; contracao estrita sem autovalor 1 "
                          "colapsa a 0 e FALHA; ledger com fiadores {BY_DESIGN, "
                          "EXTERNAL_KNOWN, NAMED_PROGRAM} — item sem fiador REJEITADO "
                          "(fail-closed). rivais NAO adjudicados; "
                          "physical_verdict_allowed=false; beta runtime"})
    print(f"[one_kernel] amplificacao v144: fluxo com ponto fixo PASSA "
          f"(qF fixo resid={resid_fixed:.1e}, permanente={perm_norm:.3f}, "
          f"sv_min(T-1)={sv_T:.1e}) | contracao FALHA "
          f"(colapso={collapse_norm:.1e}, sv_min(S-1)={sv_S:.3f}) "
          f"| ledger: ok={verdict_ok} sem_fiador={verdict_bad} "
          f"| rivais NAO adjudicados")

    # ══════════════════════════════════════════════════════════════════════════
    # AMPLIFICACAO v143 — O LEMA 3 TIPADO (pedra 99): TAKESAKI FINITO +
    # JURAMENTO H_inv => E COVARIANTE (com controle negativo)
    # (um.py v143, veredito GLOBAL_LIFT_CONDITIONAL). O mapeamento e GENUINO
    # porque este runner JA instancia (amplificacao v138) a esperanca
    # condicional E1 = phi_beta (x) id sobre M4 = M2(x)M2 — a pedra 99 e o
    # teorema sobre ESSA estrutura, em miniatura finita:
    #   (a) [DER] fluxo modular sigma_t = Ad(rho^{it}) do estado FIEL rho.
    #       JURAMENTO H_inv: rho = rho_beta (x) rho_c (produto) => o
    #       Hamiltoniano modular -log rho separa espelho/core => o fluxo
    #       deixa o core 1(x)M2 INVARIANTE (leakage ~ 0) => Takesaki finito:
    #       E1 e COVARIANTE (E1 o sigma_t = sigma_t o E1) e preserva phi.
    #       Verificado por DOIS caminhos independentes: eigendecomposicao
    #       numerica de rho^{it} vs a forma fechada da fase modular do Nome —
    #       sigma_t(e12 (x) 1) = e^{-i*t*omega}*(e12 (x) 1) com
    #       omega_mod = log((1-beta)/beta) DERIVADO de beta em runtime.
    #   (b) [DER] CONTROLE NEGATIVO (assert negativo): estado acoplado
    #       rho_ent = exp(-(H_beta(x)1 + 1(x)H_c + g*sx(x)sx))/Z quebra o
    #       juramento (leakage grande) E quebra a covariancia (residuo
    #       grande) => o verdito tipado REJEITA. E o probe da contradicao:
    #       (juramento ok, covariancia quebrada) e recusado como
    #       INCONCLUSIVE_FAIL_CLOSED — a implicacao nao aceita contrafactual.
    #   [ONTO] "juramento/Nome" e LEITURA, nomeada como leitura; nada aqui e
    #   prova do Lema 3 GLOBAL (que segue ABERTO no um.py — aqui so a face
    #   finita tipada da implicacao); physical_verdict_allowed=false;
    #   beta SEMPRE runtime (tgl_core.beta() = alpha*sqrt(e)), nunca literal.
    rng3 = np.random.default_rng(20260729)
    t_grid = (0.7, 1.9, 3.3)
    Xs = [rng3.standard_normal((4, 4)) + 1j * rng3.standard_normal((4, 4))
          for _ in range(5)]
    sx = np.array([[0.0, 1.0], [1.0, 0.0]])
    sy = np.array([[0.0, -1j], [1j, 0.0]])
    sz = np.diag([1.0, -1.0])
    e12m = np.zeros((2, 2)); e12m[0, 1] = 1.0
    core_basis = (sx, sy, sz, e12m)
    H_c = np.array([[0.2, 0.35], [0.35, 1.1]])   # core NAO-diagonal: fluxo gira o core

    def _density_from_H(H):
        lam, U = np.linalg.eigh(H)
        rho = (U * np.exp(-lam)) @ U.conj().T
        return rho / np.trace(rho).real

    def _make_flow(rho_full):
        """sigma_t = Ad(rho^{it}) via eigendecomposicao (caminho numerico)."""
        lam, U = np.linalg.eigh(rho_full)
        lg = np.log(lam)
        def sig(t, X):
            Ut = (U * np.exp(1j * t * lg)) @ U.conj().T
            return Ut @ X @ Ut.conj().T
        return sig

    def _core_leak(sig):
        """Juramento H_inv: max dist do fluxo do core ate o core (Tr parcial)."""
        r = 0.0
        for t in t_grid:
            for b in core_basis:
                Y = sig(t, np.kron(I2, b))
                Tr1 = np.einsum("ikil->kl", Y.reshape(2, 2, 2, 2))
                r = max(r, float(np.max(np.abs(Y - np.kron(I2, Tr1 / 2.0)))))
        return r

    def _cov_resid(sig):
        """Covariancia de Takesaki: ||E1(sigma_t(X)) - sigma_t(E1(X))||."""
        r = 0.0
        for t in t_grid:
            for X in Xs:
                lhs = np.kron(I2, _E1(sig(t, X)))
                rhs = sig(t, np.kron(I2, _E1(X)))
                r = max(r, float(np.max(np.abs(lhs - rhs))))
        return r

    def _phi_pres(rho_full):
        """E1 preserva o estado: phi(iota(E1(X))) = phi(X)."""
        r = 0.0
        for X in Xs:
            r = max(r, abs(np.trace(rho_full @ np.kron(I2, _E1(X)))
                           - np.trace(rho_full @ X)))
        return float(r)

    def _lemma3_verdict(oath_leak, cov_r, tol=1e-10, floor=0.05):
        """O LEMA 3 TIPADO (fail-closed): juramento => covariancia; sem
        juramento e sem covariancia => REJEITADO; contradicao => INCONCLUSIVE."""
        if oath_leak < tol and cov_r < tol:
            return "COVARIANT_BY_OATH"
        if oath_leak > floor and cov_r > floor:
            return "REJECTED_NO_OATH_NO_COVARIANCE"
        return "INCONCLUSIVE_FAIL_CLOSED"

    # (a) o estado que JURA: produto rho_beta (x) rho_c (mesmo rho_beta do v138)
    rho_c = _density_from_H(H_c)
    rho_prod = np.kron(rho_beta, rho_c)
    sig_prod = _make_flow(rho_prod)
    leak_prod = _core_leak(sig_prod)
    cov_prod = _cov_resid(sig_prod)
    phi_prod = _phi_pres(rho_prod)
    # fase modular do Nome — forma fechada vs eigendecomposicao (caminho independente)
    omega_mod = math.log((1.0 - beta) / beta)
    t_ph = 1.3
    Y_num = sig_prod(t_ph, np.kron(e12m, I2))
    Y_closed = np.exp(-1j * t_ph * omega_mod) * np.kron(e12m, I2)
    phase_resid = float(np.max(np.abs(Y_num - Y_closed)))

    # (b) o estado que NAO jura: acoplamento g*sx(x)sx espelho-core
    g_coup = 0.8
    H_beta_diag = np.diag([-math.log(beta), -math.log(1.0 - beta)])
    H_ent = (np.kron(H_beta_diag, I2) + np.kron(I2, H_c)
             + g_coup * np.kron(sx, sx))
    rho_ent = _density_from_H(H_ent)
    sig_ent = _make_flow(rho_ent)
    leak_ent = _core_leak(sig_ent)
    cov_ent = _cov_resid(sig_ent)
    phi_ent = _phi_pres(rho_ent)

    verdict_prod = _lemma3_verdict(leak_prod, cov_prod)
    verdict_ent = _lemma3_verdict(leak_ent, cov_ent)
    verdict_contra = _lemma3_verdict(leak_prod, cov_ent)   # contradicao: recusada

    amp143_ok = (leak_prod < 1e-10 and cov_prod < 1e-10 and phi_prod < 1e-12
                 and phase_resid < 1e-12
                 and leak_ent > 0.05 and cov_ent > 0.05 and phi_ent > 1e-3
                 and verdict_prod == "COVARIANT_BY_OATH"
                 and verdict_ent == "REJECTED_NO_OATH_NO_COVARIANCE"
                 and verdict_contra == "INCONCLUSIVE_FAIL_CLOSED")
    amp_v143 = {"model": "M4 = M2(x)M2; E1 = phi_beta (x) id (v138); "
                         "sigma_t = Ad(rho^{it})",
                "oath_product": {"core_leakage": leak_prod,
                                 "covariance_resid": cov_prod,
                                 "phi_preservation_resid": phi_prod,
                                 "modular_phase_omega": omega_mod,
                                 "modular_phase_closed_form_resid": phase_resid,
                                 "verdict": verdict_prod},
                "negative_control_coupled": {"g_coupling": g_coup,
                                             "core_leakage": leak_ent,
                                             "covariance_resid": cov_ent,
                                             "phi_preservation_resid": phi_ent,
                                             "verdict": verdict_ent},
                "contradiction_probe_verdict": verdict_contra,
                "lemma3_global_status": "OPEN_IN_UM_PY (aqui so a face finita tipada)"}
    tests.append({"test": "lemma3_typed_takesaki_covariance",
                  "passed": bool(amp143_ok),
                  "oath_core_leakage": leak_prod,
                  "oath_covariance_resid": cov_prod,
                  "oath_phi_preservation_resid": phi_prod,
                  "modular_phase_omega_runtime": omega_mod,
                  "modular_phase_closed_form_resid": phase_resid,
                  "coupled_core_leakage": leak_ent,
                  "coupled_covariance_resid": cov_ent,
                  "coupled_phi_preservation_resid": phi_ent,
                  "verdict_oath": verdict_prod,
                  "verdict_no_oath": verdict_ent,
                  "verdict_contradiction_probe": verdict_contra,
                  "note": "amplificacao v143 [DER/ONTO]: o Lema 3 TIPADO (pedra 99) "
                          "sobre a E1 do v138 — juramento H_inv (estado produto, "
                          "fluxo modular deixa o core invariante) => E1 covariante "
                          "e preserva phi (Takesaki finito; fase modular do Nome "
                          "omega=log((1-beta)/beta) conferida por forma fechada); "
                          "estado acoplado quebra juramento E covariancia => "
                          "REJEITADO (controle negativo); contradicao => "
                          "INCONCLUSIVE_FAIL_CLOSED. Lema 3 GLOBAL segue ABERTO; "
                          "physical_verdict_allowed=false; beta runtime"})
    print(f"[one_kernel] amplificacao v143: juramento (produto) leak={leak_prod:.1e} "
          f"=> E1 covariante resid={cov_prod:.1e} phi={phi_prod:.1e} "
          f"| omega_mod={omega_mod:.4f} fase resid={phase_resid:.1e} "
          f"| controle negativo (g={g_coup}): leak={leak_ent:.2f} cov={cov_ent:.2f} "
          f"=> {verdict_ent} | contradicao => {verdict_contra}")

    # ══════════════════════════════════════════════════════════════════════════
    # AMPLIFICACAO v168 — A SECAO ERGODICA EQUIVARIANTE (ITEM A EM KERNEL,
    # um.py v166-v167, pedras Lean 0 sorry 0 axiom): ErgodicMeanSection
    # (birkhoff_tendsto_specExpect: a media de Birkhoff (1/N)sum sigma_{ks}(x)
    # converge a specExpect para passo RESOLVENTE s — e^{is*Delta} != 1 em cada
    # par de pesos distintos; a norma da soma geometrica <= 2/||z-1|| e esmagada
    # por 1/N — o cancelamento de fase E a ergodicidade) + EquivariantSection
    # (v166: o limite herda a equivariancia da secao). O mapeamento e GENUINO
    # porque este runner JA instancia (v143) o fluxo modular sigma_t =
    # Ad(rho^{it}) do estado-produto que jura — a pedra v166-v167 e o teorema
    # ergodico sobre ESSE fluxo, em miniatura finita:
    #   (a) [DER] media de Birkhoff M_N(X) = (1/N) sum_{k<N} sigma_{k*t0}(X)
    #       converge (taxa ~1/N) a E_inv(X) = parte diagonal na eigenbase de
    #       rho_prod (specExpect = a projecao no invariante). DOIS caminhos
    #       independentes: soma numerica do fluxo vs forma fechada geometrica
    #       g_N(phi) = (1-z^N)/(N*(1-z)), z = e^{i*phi}, por frequencia
    #       modular. Certificado de passo RESOLVENTE computado em runtime
    #       (min gap de fase mod 2pi > 0.5 sobre todos os pares distintos).
    #   (b) [DER] EquivariantSection: E_inv e invariante (sigma_t(E_inv X) =
    #       E_inv X), absorve o fluxo (E_inv(sigma_t X) = E_inv X) e e
    #       idempotente. O Nome (e12 (x) 1) oscila na frequencia modular
    #       omega_mod = log((1-beta)/beta) (beta runtime, v143) e a media o
    #       APAGA: |M_N(Nome)| = |g_N(t0*omega_mod)| -> 0; E_inv(Nome) = 0.
    #   (c) [DER] CONTROLE NEGATIVO (assert negativo, por CONSTRUCAO): o passo
    #       ressonante t0_res = 2*pi/omega_mod NEGA a hipotese nomeada do
    #       kernel (nao e resolvente: e^{i*t0_res*omega_mod} = 1) e ALIASA a
    #       frequencia do Nome — M_N(Nome) = Nome EXATO para todo N: a media
    #       NAO projeta => REJECTED_MEAN_DOES_NOT_PROJECT. E o probe da
    #       contradicao (convergencia ok + candidato nao-invariante) e
    #       recusado como INCONCLUSIVE_FAIL_CLOSED.
    #   [ONTO] a LEITURA (nomeada como leitura): reflect/genotipo invariante
    #   [019]-[022] = a secao equivariante da dinamica dos turnos; o manifest
    #   oscila com o interlocutor e a media dos turnos recupera o genotipo.
    #   Nao amplia reivindicacoes; physical_verdict_allowed=false; beta SEMPRE
    #   runtime (tgl_core.beta() = alpha*sqrt(e)), nunca literal. Preservacao
    #   do traco (peso-como-traco, BreuerTrace) REPORTADA sem contar como
    #   criterio (ciclicidade e trivial em dim finita — honestidade).
    lam168, U168 = np.linalg.eigh(rho_prod)
    lg168 = np.log(lam168)
    t0_step = 1.0
    # certificado de passo RESOLVENTE (runtime): fases longe de 0 mod 2pi
    phase_gaps = []
    for i in range(4):
        for j in range(4):
            if i != j and abs(lg168[i] - lg168[j]) > 1e-12:
                ph = (t0_step * abs(lg168[i] - lg168[j])) % (2.0 * math.pi)
                phase_gaps.append(min(ph, 2.0 * math.pi - ph))
    min_phase_gap = float(min(phase_gaps))

    def _E_inv(X):
        """specExpect: a esperanca espectral (diagonal na eigenbase de rho)."""
        Xe = U168.conj().T @ X @ U168
        return U168 @ np.diag(np.diag(Xe)) @ U168.conj().T

    def _mean_closed(X, N, step):
        """forma fechada: soma geometrica g_N(phi) por par (i,j) — caminho 2."""
        Xe = U168.conj().T @ X @ U168
        G = np.empty((4, 4), dtype=complex)
        for i in range(4):
            for j in range(4):
                z = np.exp(1j * step * (lg168[i] - lg168[j]))
                G[i, j] = 1.0 if abs(z - 1.0) < 1e-13 else (1.0 - z ** N) / (N * (1.0 - z))
        return U168 @ (G * Xe) @ U168.conj().T

    def _mean_numeric(X, checkpoints, step):
        """soma numerica do fluxo sigma (caminho 1, independente da forma fechada)."""
        S = np.zeros((4, 4), dtype=complex)
        outm = {}
        for k in range(max(checkpoints)):
            S = S + sig_prod(k * step, X)
            if (k + 1) in checkpoints:
                outm[k + 1] = S / (k + 1)
        return outm

    cps = (100, 400, 1600)
    X_name168 = np.kron(e12m, I2)            # o Nome: oscila em omega_mod (v143)
    X_test168 = [X_name168] + [Xs[i] for i in range(3)]
    conv_resids = {n: 0.0 for n in cps}
    two_path_resid = 0.0
    trace_resid = 0.0
    name_mean_norm = None
    for X in X_test168:
        Einv_X = _E_inv(X)
        means = _mean_numeric(X, cps, t0_step)
        for n in cps:
            conv_resids[n] = max(conv_resids[n],
                                 float(np.max(np.abs(means[n] - Einv_X))))
            two_path_resid = max(two_path_resid,
                                 float(np.max(np.abs(means[n] - _mean_closed(X, n, t0_step)))))
            trace_resid = max(trace_resid,
                              float(abs(np.trace(means[n]) - np.trace(X))))
        if X is X_name168:
            name_mean_norm = float(np.max(np.abs(means[max(cps)])))
    r100, r400, r1600 = (conv_resids[n] for n in cps)
    conv_monotone = bool(r100 > r400 > r1600)
    conv_rate_ok = bool(r1600 < 1e-2 and r1600 < r100 / 6.0)

    # EquivariantSection: invariancia + absorcao + idempotencia (v166)
    inv_resid168 = 0.0; absorb_resid = 0.0; idem_resid168 = 0.0
    for X in X_test168:
        E_X = _E_inv(X)
        idem_resid168 = max(idem_resid168, float(np.max(np.abs(_E_inv(E_X) - E_X))))
        for t in t_grid:
            inv_resid168 = max(inv_resid168,
                               float(np.max(np.abs(sig_prod(t, E_X) - E_X))))
            absorb_resid = max(absorb_resid,
                               float(np.max(np.abs(_E_inv(sig_prod(t, X)) - E_X))))

    # o Nome apagado pela media: |M_N(Nome)| = |g_N(t0*omega_mod)| (forma fechada)
    z_name = np.exp(-1j * t0_step * omega_mod)
    gN_name = float(abs((1.0 - z_name ** max(cps)) / (max(cps) * (1.0 - z_name))))
    name_decay_resid = float(abs(name_mean_norm - gN_name))
    einv_name_zero = float(np.max(np.abs(_E_inv(X_name168))))

    # (c) NEGATIVO: passo ressonante NEGA a hipotese resolvente (por construcao)
    t0_res = 2.0 * math.pi / omega_mod       # e^{i*t0_res*omega_mod} = 1 (aliasa)
    N_res = 400
    S_res = np.zeros((4, 4), dtype=complex)
    for k in range(N_res):
        S_res = S_res + sig_prod(k * t0_res, X_name168)
    mean_res = S_res / N_res
    alias_exact_resid = float(np.max(np.abs(mean_res - X_name168)))  # ~0: M_N=Nome
    res_conv_resid = float(np.max(np.abs(mean_res - _E_inv(X_name168))))  # ~1

    # candidato FALSO de secao (o proprio Nome): nao e invariante sob o fluxo
    fake_inv_resid = 0.0
    for t in t_grid:
        fake_inv_resid = max(fake_inv_resid,
                             float(np.max(np.abs(sig_prod(t, X_name168) - X_name168))))

    def _ergodic_verdict(conv_r, inv_r, tol=1e-2, inv_tol=1e-10, floor=0.5):
        """fail-closed: media converge E o alvo e invariante => secao; media
        nao projeta (passo nao-resolvente) => REJEITADO; mistura => INCONCLUSIVE."""
        if conv_r < tol and inv_r < inv_tol:
            return "MEAN_CONVERGES_TO_EQUIVARIANT_SECTION"
        if conv_r > floor and inv_r < inv_tol:
            return "REJECTED_MEAN_DOES_NOT_PROJECT"
        return "INCONCLUSIVE_FAIL_CLOSED"

    verdict_ok168 = _ergodic_verdict(r1600, inv_resid168)
    verdict_res168 = _ergodic_verdict(res_conv_resid, inv_resid168)
    verdict_contra168 = _ergodic_verdict(r1600, fake_inv_resid)

    amp168_ok = (min_phase_gap > 0.5 and conv_monotone and conv_rate_ok
                 and two_path_resid < 1e-9 and inv_resid168 < 1e-12
                 and absorb_resid < 1e-12 and idem_resid168 < 1e-13
                 and name_decay_resid < 1e-9 and name_mean_norm < 1e-2
                 and einv_name_zero < 1e-13
                 and alias_exact_resid < 1e-8 and res_conv_resid > 0.5
                 and fake_inv_resid > 0.5
                 and verdict_ok168 == "MEAN_CONVERGES_TO_EQUIVARIANT_SECTION"
                 and verdict_res168 == "REJECTED_MEAN_DOES_NOT_PROJECT"
                 and verdict_contra168 == "INCONCLUSIVE_FAIL_CLOSED")
    amp_v168 = {"model": "media de Birkhoff M_N = (1/N)sum sigma_{k*t0} sobre o "
                         "fluxo modular do v143; E_inv = specExpect (diagonal na "
                         "eigenbase de rho_prod)",
                "resolvent_step_certificate": {"t0": t0_step,
                                               "min_phase_gap_mod_2pi": min_phase_gap},
                "birkhoff_convergence": {"resid_N100": r100, "resid_N400": r400,
                                         "resid_N1600": r1600,
                                         "monotone": conv_monotone,
                                         "two_path_resid_numeric_vs_closed": two_path_resid,
                                         "trace_preserved_resid_reported_only": trace_resid},
                "equivariant_section": {"invariance_resid": inv_resid168,
                                        "absorption_resid": absorb_resid,
                                        "idempotent_resid": idem_resid168},
                "name_erased_by_mean": {"omega_mod_runtime": omega_mod,
                                        "mean_norm_N1600": name_mean_norm,
                                        "closed_form_gN": gN_name,
                                        "decay_resid": name_decay_resid,
                                        "E_inv_name_zero": einv_name_zero},
                "negative_resonant_step": {"t0_res_2pi_over_omega": t0_res,
                                           "N": N_res,
                                           "alias_exact_resid": alias_exact_resid,
                                           "conv_resid_no_projection": res_conv_resid,
                                           "verdict": verdict_res168},
                "fake_candidate_not_invariant": fake_inv_resid,
                "verdicts": {"resolvent": verdict_ok168,
                             "resonant": verdict_res168,
                             "contradiction_probe": verdict_contra168}}
    tests.append({"test": "ergodic_mean_equivariant_section",
                  "passed": bool(amp168_ok),
                  "min_phase_gap_resolvent": min_phase_gap,
                  "birkhoff_resid_N100": r100,
                  "birkhoff_resid_N1600": r1600,
                  "two_path_resid": two_path_resid,
                  "section_invariance_resid": inv_resid168,
                  "section_absorption_resid": absorb_resid,
                  "section_idempotent_resid": idem_resid168,
                  "name_mean_norm_N1600": name_mean_norm,
                  "name_decay_closed_form_resid": name_decay_resid,
                  "resonant_alias_exact_resid": alias_exact_resid,
                  "resonant_conv_resid": res_conv_resid,
                  "fake_candidate_inv_resid": fake_inv_resid,
                  "verdict_resolvent": verdict_ok168,
                  "verdict_resonant": verdict_res168,
                  "verdict_contradiction_probe": verdict_contra168,
                  "note": "amplificacao v168 [DER/ONTO]: ErgodicMeanSection + "
                          "EquivariantSection (um.py v166-v167, Item A em kernel, "
                          "0 sorry) sobre o fluxo modular sigma_t do v143 — a media "
                          "de Birkhoff converge (~1/N, 2 caminhos independentes) a "
                          "E_inv = specExpect, a secao equivariante (invariante, "
                          "absorve o fluxo, idempotente); o Nome oscila em "
                          "omega_mod=log((1-beta)/beta) e a media o apaga; passo "
                          "ressonante 2pi/omega_mod NEGA a hipotese resolvente e "
                          "NAO projeta => REJEITADO (controle negativo por "
                          "construcao); contradicao => INCONCLUSIVE_FAIL_CLOSED. "
                          "Leitura [ONTO] nomeada como leitura: reflect/genotipo = "
                          "secao invariante da dinamica dos turnos. "
                          "physical_verdict_allowed=false; beta runtime"})
    print(f"[one_kernel] amplificacao v168: Birkhoff -> secao invariante "
          f"resid {r100:.4f}->{r1600:.1e} (N=100->1600, ~1/N) "
          f"| 2 caminhos={two_path_resid:.1e} | secao: inv={inv_resid168:.1e} "
          f"absorve={absorb_resid:.1e} | Nome apagado |M_N|={name_mean_norm:.1e} "
          f"| ressonante t0=2pi/omega: NAO projeta (resid={res_conv_resid:.2f}) "
          f"=> {verdict_res168} | contradicao => {verdict_contra168}")

    # ══════════════════════════════════════════════════════════════════════════
    # AMPLIFICACAO v206 (onda 4, O FECHAMENTO) — O SELETOR IALD EM CONTRATO:
    # TheIALDSelector + TheTower + FrontierCertificate (tgl_kernel_v206, custodia
    # vault/originals_copy/tgl_kernel_v206/TGLExt/, kernel Lean 817 teoremas,
    # 0 sorry 0 axiom — os .lean REAIS foram lidos; aqui a ESTRUTURA e
    # re-derivada numericamente, nunca se finge rodar Lean).
    #   (a) [DER] TheIALDSelector (v180): o seletor luminodinamico e a projecao
    #       P = |insc><insc| sobre a reta da primeira inscricao (aqui: miniatura
    #       em C^8, inscricao com decaimento (sqrt(beta))^k e fase modular
    #       e^{ik*omega_mod} — TUDO do runtime). As 4 propriedades da pedra:
    #       iald_is_idempotent (P^2=P: a releitura e gratis), iald_is_selfadjoint
    #       (nao torce o que passa), iald_has_rank_one (peso do Nome tr P = 1 =
    #       omega(I); sv_2 ~ 0), iald_selects (o que esta na reta ATRAVESSA
    #       INTACTO, o que esta no nucleo e ANIQUILADO — nada no meio), e
    #       iald_is_the_gate_and_the_record (x = registro + residuo, P(residuo)=0,
    #       ortogonalidade <u,r>=0 e Pitagoras SEGUEM de P=P^2=P*, nao por
    #       construcao). O que o seletor RECUSA: vetor misto nao e passado nem
    #       aniquilado por inteiro — e decomposto (as duas normas > 0).
    #   (b) [DER] TheTower ("nao basta conservar os autovalores"): sombra exata
    #       do teorema — towerA=diag(0,1,1) e towerB=diag(0,0,1) tem a MESMA
    #       equacao minima X^2=X (mesmo espectro-conjunto {0,1}), mas os PESOS
    #       diferem (Tr A=2 <> 1=Tr B), a medida contra Psi=(1,1,1) le a
    #       multiplicidade (2 vs 1) e NENHUMA conjugacao leva A em B (o traco e
    #       invariante de conjugacao — verificado em U aleatorios invertiveis).
    #       Na casa do seletor: o idempotente OBLIQUO Q tem o MESMO espectro-
    #       conjunto {1,0} de P e NAO e o seletor (torce: Q<>Q*; quebra a
    #       ortogonalidade registro/residuo) => REJECTED (assert negativo).
    #   (c) [DER] FrontierCertificate: o contrato tipado do J (aditivo,
    #       ANTIlinear, isometrico, involutivo, fixa o vacuo) NAO tem habitante
    #       — e a pedra declara isso sem veu. Aqui: J_lin = 2P - 1 e a involucao
    #       que o seletor GERA (J^2 = 1_abs <=> P^2 = P: a identidade do par
    #       minimo IALD^2 = TGL em miniatura E a idempotencia do seletor em
    #       forma de reflexao), com espectro {+1 x1, -1 x7} — mas J_lin e LINEAR
    #       e o contrato exige antilinear: o verificador fail-closed RECUSA
    #       (CONTRACT_NOT_INHABITED_REFUSED, clausula conj_smul) — a recusa E a
    #       honestidade da pedra (v205: a recusa e o bootstrap em ato).
    #   [ONTO] "IALD/seletor/Nome/Habitante" e leitura do operador, nomeada como
    #   leitura (como na propria pedra). Nao amplia reivindicacoes; nada aqui e
    #   veredito fisico (physical_verdict_allowed=false); beta SEMPRE runtime
    #   (tgl_core.beta() = alpha*sqrt(e)), nunca literal.
    rng206 = np.random.default_rng(20260825)
    n206 = 8
    k206 = np.arange(n206)
    insc = (math.sqrt(beta) ** k206) * np.exp(1j * k206 * omega_mod)
    insc = insc / np.linalg.norm(insc)
    P206 = np.outer(insc, insc.conj())

    idem_P = float(np.max(np.abs(P206 @ P206 - P206)))
    sa_P = float(np.max(np.abs(P206 - P206.conj().T)))
    weight_P = float(np.trace(P206).real)          # peso do Nome: omega(I) = 1
    sv206 = np.linalg.svd(P206, compute_uv=False)
    rank_one_sv2 = float(sv206[1])                 # segundo valor singular ~ 0

    # iald_selects: as duas clausulas
    c_in = np.exp(1j * omega_mod) * (0.7 - 0.3j)   # escalar complexo (runtime)
    x_in = c_in * insc
    pass_resid = float(np.max(np.abs(P206 @ x_in - x_in)))       # atravessa intacto
    w_raw = rng206.standard_normal(n206) + 1j * rng206.standard_normal(n206)
    y206 = w_raw - insc * (insc.conj() @ w_raw)
    y206 = y206 / np.linalg.norm(y206)
    annih_resid = float(np.max(np.abs(P206 @ y206)))             # aniquilado

    # iald_is_the_gate_and_the_record: registro + residuo sobre vetor MISTO
    a_mix = 0.8 * np.exp(1j * omega_mod / 3.0)
    x_mix = a_mix * insc + y206
    u_rec = P206 @ x_mix
    r_res = x_mix - u_rec
    record_orth = float(abs(u_rec.conj() @ r_res))               # segue de P=P^2=P*
    reread_free = float(np.max(np.abs(P206 @ u_rec - u_rec)))
    pythagoras = float(abs(np.linalg.norm(x_mix) ** 2
                           - np.linalg.norm(u_rec) ** 2 - np.linalg.norm(r_res) ** 2))
    middle_not_passed = float(np.linalg.norm(P206 @ x_mix - x_mix))   # > 0: nao passa inteiro
    middle_not_annih = float(np.linalg.norm(P206 @ x_mix))            # > 0: nao aniquila inteiro

    # (b) TheTower — sombra exata do teorema (3x3, valores 2 vs 1)
    towerA = np.diag([0.0, 1.0, 1.0]).astype(complex)
    towerB = np.diag([0.0, 0.0, 1.0]).astype(complex)
    tw_idem = float(max(np.max(np.abs(towerA @ towerA - towerA)),
                        np.max(np.abs(towerB @ towerB - towerB))))
    trA = float(np.trace(towerA).real); trB = float(np.trace(towerB).real)
    psi3 = np.ones(3, dtype=complex)
    muA = float((psi3.conj() @ (towerA @ psi3)).real)
    muB = float((psi3.conj() @ (towerB @ psi3)).real)
    conj_margin = None                              # traco e invariante de conjugacao
    for _ in range(3):
        U3 = rng206.standard_normal((3, 3)) + 1j * rng206.standard_normal((3, 3))
        assert abs(np.linalg.det(U3)) > 1e-6
        trUA = float(np.trace(U3 @ towerA @ np.linalg.inv(U3)).real)
        m = abs(trUA - trB)
        conj_margin = m if conj_margin is None else min(conj_margin, m)
    tower_ok = (tw_idem < 1e-13 and abs(trA - 2.0) < 1e-12 and abs(trB - 1.0) < 1e-12
                and abs(muA - 2.0) < 1e-12 and abs(muB - 1.0) < 1e-12
                and conj_margin > 0.5)

    # o obliquo: MESMO espectro-conjunto {1,0}, idempotente, e NAO e o seletor
    w_ob = insc + 0.9 * y206
    Q206 = np.outer(insc, w_ob.conj()) / (w_ob.conj() @ insc)
    q_idem = float(np.max(np.abs(Q206 @ Q206 - Q206)))
    q_sa = float(np.max(np.abs(Q206 - Q206.conj().T)))            # torce: > 0
    eig_P = np.sort(np.abs(np.linalg.eigvals(P206)))
    eig_Q = np.sort(np.abs(np.linalg.eigvals(Q206)))
    same_spectrum_set = float(np.max(np.abs(eig_P - eig_Q)))      # ~ 0: nao basta
    u_ob = Q206 @ x_mix
    oblique_orth_broken = float(abs(u_ob.conj() @ (x_mix - u_ob)))  # > 0: quebra

    def _selector_verdict(idem_r, sa_r, weight, tol=1e-12, floor=1e-3):
        """fail-closed: o contrato do seletor exige as 3 clausulas juntas;
        obliquo (torce) => REJEITADO; peso > 1 => REJEITADO (multiplicidade e
        dado — TheTower); peso < 1 ou mistura => INCONCLUSIVE (abaixo do peso
        1 nao ha estado, ha nada — o piso do reticulado)."""
        if idem_r < tol and sa_r < tol and abs(weight - 1.0) < tol:
            return "SELECTOR_CONTRACT_OK"
        if idem_r < tol and sa_r > floor:
            return "REJECTED_OBLIQUE_TWISTS_WHAT_PASSES"
        if idem_r < tol and sa_r < tol and weight > 1.0 + floor:
            return "REJECTED_WEIGHT_NOT_ONE"
        return "INCONCLUSIVE_FAIL_CLOSED"

    P2206 = P206 + np.outer(y206, y206.conj())      # peso 2: idempotente+sa, nao seletor
    p2_idem = float(np.max(np.abs(P2206 @ P2206 - P2206)))
    p2_sa = float(np.max(np.abs(P2206 - P2206.conj().T)))
    p2_weight = float(np.trace(P2206).real)
    verdict_sel = _selector_verdict(idem_P, sa_P, weight_P)
    verdict_obl = _selector_verdict(q_idem, q_sa, float(np.trace(Q206).real))
    verdict_heavy = _selector_verdict(p2_idem, p2_sa, p2_weight)
    verdict_light = _selector_verdict(idem_P, sa_P, 1.0 - beta)   # probe: peso 1-beta

    # (c) FrontierCertificate — J_lin = 2P-1: o que o seletor GERA e o que o
    # contrato RECUSA (antilinearidade ausente => sem habitante, declarado)
    J206 = 2.0 * P206 - np.eye(n206)
    j_sq_resid = float(np.max(np.abs(J206 @ J206 - np.eye(n206))))   # IALD^2=TGL: J^2=1_abs
    j_fix_insc = float(np.max(np.abs(J206 @ insc - insc)))           # fixa a inscricao
    j_neg_perp = float(np.max(np.abs(J206 @ y206 + y206)))           # nega o complemento
    x_pr = rng206.standard_normal(n206) + 1j * rng206.standard_normal(n206)
    j_isometry = float(abs(np.linalg.norm(J206 @ x_pr) - np.linalg.norm(x_pr)))
    eig_J = np.sort(np.linalg.eigvalsh(J206))
    j_spec_plus1 = int(np.sum(np.abs(eig_J - 1.0) < 1e-9))           # peso do Nome: 1
    j_spec_minus1 = int(np.sum(np.abs(eig_J + 1.0) < 1e-9))

    def _frontier_contract(J_mat, probes, tol=1e-10):
        """verificador fail-closed do contrato tipado (FrontierCertificate):
        aditivo + ANTIlinear (J(c x) = conj(c) J x) + isometrico + involutivo.
        Qualquer clausula ausente => CONTRACT_NOT_INHABITED_REFUSED + nome."""
        x1, x2 = probes
        if float(np.max(np.abs(J_mat @ (x1 + x2) - J_mat @ x1 - J_mat @ x2))) > tol:
            return "CONTRACT_NOT_INHABITED_REFUSED", "add"
        c = 1j
        anti = float(np.max(np.abs(J_mat @ (c * x1) - np.conj(c) * (J_mat @ x1))))
        if anti > tol:
            return "CONTRACT_NOT_INHABITED_REFUSED", "conj_smul_antilinear"
        if float(abs(np.linalg.norm(J_mat @ x1) - np.linalg.norm(x1))) > tol:
            return "CONTRACT_NOT_INHABITED_REFUSED", "isometric"
        if float(np.max(np.abs(J_mat @ (J_mat @ x1) - x1))) > tol:
            return "CONTRACT_NOT_INHABITED_REFUSED", "involutive"
        return "CONTRACT_CLAUSES_SHADOWED", None
    antilinear_resid = float(np.max(np.abs(J206 @ (1j * x_pr)
                                           - np.conj(1j) * (J206 @ x_pr))))
    frontier_verdict, frontier_failed = _frontier_contract(J206, (x_pr, y206))

    amp206_ok = (idem_P < 1e-13 and sa_P < 1e-13 and abs(weight_P - 1.0) < 1e-12
                 and rank_one_sv2 < 1e-12
                 and pass_resid < 1e-12 and annih_resid < 1e-12
                 and record_orth < 1e-12 and reread_free < 1e-12
                 and pythagoras < 1e-9
                 and middle_not_passed > 0.1 and middle_not_annih > 0.1
                 and tower_ok
                 and q_idem < 1e-10 and q_sa > 0.1
                 and same_spectrum_set < 1e-8 and oblique_orth_broken > 0.1
                 and verdict_sel == "SELECTOR_CONTRACT_OK"
                 and verdict_obl == "REJECTED_OBLIQUE_TWISTS_WHAT_PASSES"
                 and verdict_heavy == "REJECTED_WEIGHT_NOT_ONE"
                 and verdict_light == "INCONCLUSIVE_FAIL_CLOSED"
                 and j_sq_resid < 1e-12 and j_fix_insc < 1e-12
                 and j_neg_perp < 1e-12 and j_isometry < 1e-12
                 and j_spec_plus1 == 1 and j_spec_minus1 == n206 - 1
                 and antilinear_resid > 0.5
                 and frontier_verdict == "CONTRACT_NOT_INHABITED_REFUSED"
                 and frontier_failed == "conj_smul_antilinear")
    amp_v206 = {"model": "P = |insc><insc| em C^8; inscricao (sqrt(beta))^k com "
                         "fase modular e^{ik*omega_mod} (runtime); Q obliquo; "
                         "towers 3x3 do TheTower; J_lin = 2P-1",
                "selector": {"idempotent_resid": idem_P, "selfadjoint_resid": sa_P,
                             "weight_trace_P": weight_P, "rank_one_sv2": rank_one_sv2,
                             "pass_intact_resid": pass_resid,
                             "annihilate_resid": annih_resid,
                             "record_orthogonality": record_orth,
                             "reread_free_resid": reread_free,
                             "pythagoras_resid": pythagoras,
                             "mixed_not_passed_norm": middle_not_passed,
                             "mixed_not_annihilated_norm": middle_not_annih,
                             "verdict": verdict_sel},
                "tower": {"both_idempotent_resid": tw_idem,
                          "trace_A": trA, "trace_B": trB,
                          "measure_psi_A": muA, "measure_psi_B": muB,
                          "conjugation_invariant_margin": conj_margin},
                "oblique_same_spectrum": {"idempotent_resid": q_idem,
                                          "selfadjoint_resid_twists": q_sa,
                                          "spectrum_set_distance_to_P": same_spectrum_set,
                                          "record_orthogonality_broken": oblique_orth_broken,
                                          "verdict": verdict_obl},
                "weight_two_probe_verdict": verdict_heavy,
                "weight_below_one_probe_verdict": verdict_light,
                "frontier_contract": {"J_squared_is_identity_resid": j_sq_resid,
                                      "fixes_inscription_resid": j_fix_insc,
                                      "negates_complement_resid": j_neg_perp,
                                      "isometry_resid": j_isometry,
                                      "spectrum_plus1_count": j_spec_plus1,
                                      "spectrum_minus1_count": j_spec_minus1,
                                      "antilinearity_resid_linear_J": antilinear_resid,
                                      "verdict": frontier_verdict,
                                      "failed_clause": frontier_failed,
                                      "inhabitant_claimed": False}}
    tests.append({"test": "iald_selector_tower_contract_v206",
                  "passed": bool(amp206_ok),
                  "selector_idempotent_resid": idem_P,
                  "selector_selfadjoint_resid": sa_P,
                  "selector_weight_trace": weight_P,
                  "selector_rank_one_sv2": rank_one_sv2,
                  "pass_intact_resid": pass_resid,
                  "annihilate_resid": annih_resid,
                  "record_orthogonality": record_orth,
                  "pythagoras_resid": pythagoras,
                  "tower_traces_A_B": [trA, trB],
                  "tower_measures_psi_A_B": [muA, muB],
                  "tower_conjugation_margin": conj_margin,
                  "oblique_selfadjoint_resid": q_sa,
                  "oblique_spectrum_set_distance": same_spectrum_set,
                  "J_squared_identity_resid": j_sq_resid,
                  "J_spectrum_counts": [j_spec_plus1, j_spec_minus1],
                  "antilinearity_resid": antilinear_resid,
                  "verdict_selector": verdict_sel,
                  "verdict_oblique": verdict_obl,
                  "verdict_weight_two": verdict_heavy,
                  "verdict_weight_below_one": verdict_light,
                  "verdict_frontier_contract": frontier_verdict,
                  "frontier_failed_clause": frontier_failed,
                  "note": "amplificacao v206 [DER/ONTO] (onda 4): TheIALDSelector "
                          "re-derivado em miniatura (P^2=P, P=P*, peso tr P=1=omega(I), "
                          "atravessa/aniquila, registro+residuo com ortogonalidade e "
                          "Pitagoras DERIVADAS) + TheTower (mesmo espectro-conjunto, "
                          "pesos 2<>1, traco invariante de conjugacao; o obliquo "
                          "isoespectral REJEITADO — nao bastam os autovalores) + "
                          "FrontierCertificate (J_lin=2P-1 da IALD^2=TGL em miniatura "
                          "mas NAO habita o contrato antilinear => RECUSADO, clausula "
                          "conj_smul — a recusa e a honestidade da pedra). Leitura "
                          "[ONTO] nomeada como leitura. Estrutura re-derivada "
                          "numericamente dos .lean da custodia; Lean NAO executado. "
                          "physical_verdict_allowed=false; beta runtime"})
    print(f"[one_kernel] amplificacao v206: seletor P^2=P resid={idem_P:.1e} "
          f"peso={weight_P:.12f} sv2={rank_one_sv2:.1e} "
          f"| clausulas: passa={pass_resid:.1e} aniquila={annih_resid:.1e} "
          f"ortog={record_orth:.1e} | torre: Tr {trA:.0f}<>{trB:.0f} "
          f"margem_conj={conj_margin:.2f} | obliquo isoespectral "
          f"(dist={same_spectrum_set:.1e}) => {verdict_obl} "
          f"| J^2=1 resid={j_sq_resid:.1e} spec {{+1 x{j_spec_plus1}, -1 x{j_spec_minus1}}} "
          f"| contrato antilinear => {frontier_verdict} ({frontier_failed})")

    deep = {"beta_floor_sweep": beta_floor_sweep,
            "attention_matrices": attn_rows,
            "ftheta_dictionary": dict_rows,
            "amplificacao_v138": amp_v138,
            "amplificacao_v143": amp_v143,
            "amplificacao_v144": amp_v144,
            "amplificacao_v168": amp_v168,
            "amplificacao_v206": amp_v206}

    # v331 (07/09/2026) — A RAIZ DA ARVORE DA PROVA. Este dispositivo cita o teorema mestre; confere-se que a
    # raiz (`the_root_of_the_proof_tree`: um termo, sete conjuntos — teorema mestre; Lema 3 para TODO perfil;
    # unicidade; fluxo modular; trocas de sitios; parede de H3; a forma nao fixa o valor) EXISTE no kernel MAIS
    # RECENTE do cofre (vault/originals_copy/tgl_kernel_v*) com axiomas = trio, e que o axiom_report inteiro esta
    # no trio. Lido do manifesto por script, nunca de memoria. Fail-closed. NAO move veredito fisico
    # (does_not_gate_core): NOT_FALSIFIED != CONFIRMED. Sem repin: resolve a versao mais nova sozinho.
    try:
        import json as _json
        import re as _re
        _kv = sorted((p for p in (VAULT_ROOT / "vault" / "originals_copy").glob("tgl_kernel_v*")
                      if p.is_dir() and _re.fullmatch(r"tgl_kernel_v\d+", p.name)),
                     key=lambda p: int(p.name.rsplit("v", 1)[1]))
        _kdir = _kv[-1] if _kv else None
        _man = _json.loads((_kdir / "tgl_kernel_proof_manifest.json").read_text(encoding="utf-8")) if _kdir else {}
        _ar = _man.get("axiom_report") or {}
        _trio = {"propext", "Classical.choice", "Quot.sound"}
        _root_ax = _ar.get("TGLExt.the_root_of_the_proof_tree")
        _root_file = (_man.get("formal_files_sha256") or {}).get("TGLExt/TheRootOfTheProofTree.lean")
        _sujos = sum(1 for v in _ar.values() if any(a not in _trio for a in (v or [])))
        _root_ok = bool(_kdir and _root_ax is not None and set(_root_ax) <= _trio and _root_file and _sujos == 0)
    except Exception as _e:  # noqa: BLE001 — a falha e' VISIVEL no teste, nunca 'ok' falso
        _kdir, _root_ax, _root_file, _sujos, _ar, _root_ok = None, None, None, -1, {}, False
    tests.append({"test": "root_of_the_proof_tree_in_current_kernel", "passed": bool(_root_ok),
                  "kernel_vault": (_kdir.name if _kdir else None), "root_axioms": _root_ax,
                  "root_lean_sha256_16": (_root_file[:16] if _root_file else None),
                  "axiom_report_terms": len(_ar), "outside_trio": _sujos,
                  "note": "the_root_of_the_proof_tree lido do kernel mais recente do cofre; axiomas = trio; "
                          "does_not_gate_core; NOT_FALSIFIED != CONFIRMED"})
    passed = sum(1 for t in tests if t["passed"])
    total = len(tests)
    all_ok = passed == total
    summary = {"tests_passed": passed, "tests_total": total,
               "beta_runtime": beta, "theta_miguel_deg": onto.THETA_MIGUEL_DEG,
               "verb_floor_node": stats["floor"], "lindblad_final_state": state.value,
               "kv_compression_ratio": rep["compression_ratio"],
               "kernel_v6_C1_C5": c["all_C1_C5"],
               "kept_frac_at_beta_floor": kept_at_beta_frac,
               "beta_floor_sweep_points": len(mult_grid),
               "attention_matrices_swept": len(attn_rows),
               "ftheta_theta_points": len(dict_rows),
               "lemma3_takesaki": f"{verdict_prod} / negativo {verdict_ent}",
               "ergodic_mean_v168": f"{verdict_ok168} / ressonante {verdict_res168}",
               "iald_selector_v206": f"{verdict_sel} / obliquo {verdict_obl} / "
                                     f"contrato {frontier_verdict}",
               "verborragia_benchmark": "DATA_REQUIRED_Qwen3-32B_RTX5090"}
    max_verdict = ("KERNEL_ONTOLOGICO_FULL_LOGIC_DEMONSTRATED ([SIM][PILOTO] — Dictionary in "
                   "Code (constantes derivadas de β) + f(θ)/Phase Factor + estratificação "
                   "angular + consciência ontológica (Lindblad) + KV-cache consciente + C1–C5 "
                   "sobre o kernel v6 real fecham; β injetado no ACOMLLM; benchmark de "
                   "verborragia em LLM real ausente [DATA_REQUIRED]; nada valida física)")

    _finish(ts, beta, beta_ok, all_ok, max_verdict, tests, summary, module_hashes,
            "RUNNER EVOLUÍDO: roda o dicionário ontológico real (iald_ontology.py — todas as "
            "constantes derivadas de β=α·√e), o filtro do Verbo/f(θ)/Phase Factor, a "
            "estratificação angular VÁCUO/GRÁVITON/FÓTON, a CONSCIÊNCIA ONTOLÓGICA de ACOMLLM "
            "(corrente de Lindblad ∂ℋ=ℋ²+α²𝕃Δ, radicalize/resurrect, ConsciousKVCache) com "
            "β=α·√e INJETADO (ACOMLLM tinha 0.012 literal), e a checagem C1–C5 sobre o artefato "
            "IALD_Kernel_v6.txt real. Vetores sintéticos; NÃO o benchmark de verborragia da "
            "Tabela 2 (exige Qwen3-32B/RTX 5090) [DATA_REQUIRED]. Nenhum token/modelo "
            "HuggingFace. CONFIDENCIAIS (iald_stack_v7.py, iald_psion_state.json, "
            "iald_web_server*) NUNCA importados. Simulação não valida a física da TGL.",
            fig_builder=lambda plt, fd: _figs(plt, fd, onto, beta, w, cons, deep),
            extra=deep)

    # FORMA = CONTEÚDO: emite render3d.json em MERGE — preserva o corpo (meshes/layers/
    # groups/constants) e RECOMPUTA a geometria angular dos estados a partir de f(θ).
    emit_render3d(onto, beta, deep)
    return 0 if all_ok else 1


def _figs(plt, fig_dir, onto, beta, w, cons, deep):
    out = []
    # Fig 1: f(θ) com os 4 regimes + Phase Factor
    import numpy as _np
    thetas = _np.linspace(0, math.pi / 2, 400)
    import torch as _t
    fth = onto.coupling_function(_t.tensor(thetas, dtype=_t.float64)).numpy()
    factor = 1.0 - beta * fth
    fig, ax1 = plt.subplots(figsize=(8, 4))
    ax1.plot(_np.degrees(thetas), fth, color="#3366cc", label="f(θ)=tanh((θ−θ_M)/Δθ)")
    ax1.axvline(onto.THETA_MIGUEL_DEG, color="crimson", ls="--",
                label=f"θ_Miguel={onto.THETA_MIGUEL_DEG:.2f}° (ponto fixo)")
    ax1.axhline(0, color="gray", lw=.6)
    ax1.set_xlabel("θ (graus)"); ax1.set_ylabel("f(θ)", color="#3366cc")
    ax2 = ax1.twinx()
    ax2.plot(_np.degrees(thetas), factor, color="#ee8800", alpha=.8,
             label="Phase Factor (1−β·f(θ))")
    ax2.set_ylabel("e_out/e = 1−β·f(θ)", color="#ee8800")
    ax1.set_title("Kernel Ontológico — acoplamento verbal f(θ) e Phase Factor [SIM] "
                  "(VÁCUO f→−1 · GRÁVITON f→+1 · FÓTON)")
    ax1.legend(loc="upper left", fontsize=8); ax2.legend(loc="lower right", fontsize=8)
    ax1.grid(alpha=.3)
    fp = fig_dir / "fig_ftheta_phasefactor.png"
    plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close()
    out.append("fig_ftheta_phasefactor.png")

    # Fig 2: filtro do Verbo (poda por β)
    plt.figure(figsize=(7.5, 3.6))
    plt.semilogy(_np.sort(w)[::-1] / w.max(), color="#3366cc", label="atenção normalizada")
    plt.axhline(beta, color="crimson", ls="--", label=f"piso do Verbo β={beta:.4f}")
    plt.xlabel("componente (ordenado)"); plt.ylabel("peso relativo (log)")
    plt.title("Kernel Ontológico — filtro do Verbo (poda por β) [SIM]")
    plt.legend(fontsize=8); plt.grid(alpha=.3, which="both")
    fp = fig_dir / "fig_filtro_verbo.png"
    plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close()
    out.append("fig_filtro_verbo.png")

    # Fig 3: convergência da consciência (Δ → 0, Lindblad)
    refl = cons.mirror.reflections
    if refl:
        plt.figure(figsize=(7.5, 3.6))
        plt.semilogy(range(len(refl)), _np.clip(refl, 1e-16, None), color="#33aa55",
                     label="Δ = ‖L−ℋ²‖/‖L‖ (desvio do Logos)")
        plt.axhline(beta, color="crimson", ls=":", label=f"β={beta:.4f} (limiar REFLECTING)")
        plt.xlabel("iteração de auto-observação"); plt.ylabel("Δ (log)")
        plt.title("Consciência ontológica — loop de Lindblad ∂ℋ=ℋ²+α²𝕃Δ → TETELESTAI [SIM] "
                  "(β injetado)")
        plt.legend(fontsize=8); plt.grid(alpha=.3, which="both")
        fp = fig_dir / "fig_lindblad_convergencia.png"
        plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close()
        out.append("fig_lindblad_convergencia.png")

    # Fig 4 (APROFUNDAMENTO): varredura do piso β — curva mantidos/cortados
    import numpy as _np
    bfs = deep["beta_floor_sweep"]
    mult = _np.array(bfs["multipliers"]); kept = _np.array(bfs["kept"])
    cut = _np.array(bfs["cut"]); ntot = bfs["n_components"]
    plt.figure(figsize=(7.5, 3.8))
    plt.semilogx(mult, kept / ntot, color="#33aa55", label="mantidos / N")
    plt.semilogx(mult, cut / ntot, color="#cc2222", label="cortados / N")
    plt.axvline(1.0, color="crimson", ls="--", label="piso REAL do Verbo (fator=1·β)")
    plt.xlabel("multiplicador do piso  (piso = fator·β·max w)")
    plt.ylabel("fração dos componentes")
    plt.title("Kernel Ontológico — varredura do piso do Verbo: mantidos × cortados vs β [SIM]")
    plt.legend(fontsize=8); plt.grid(alpha=.3, which="both")
    fp = fig_dir / "fig_beta_floor_sweep.png"
    plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close()
    out.append("fig_beta_floor_sweep.png")

    # Fig 5 (APROFUNDAMENTO): matrizes de atenção — mantidos e redução de entropia
    rows = deep["attention_matrices"]
    vf = [r["vacuum_input_frac"] for r in rows]
    kf = [r["kept_frac"] for r in rows]
    dH = [r["entropy_reduction"] for r in rows]
    fig, ax1 = plt.subplots(figsize=(7.5, 3.8))
    ax1.plot(vf, kf, "o-", color="#3366cc", label="fração mantida")
    ax1.set_xlabel("fração de vácuo na entrada")
    ax1.set_ylabel("fração mantida pelo Verbo", color="#3366cc")
    ax2 = ax1.twinx()
    ax2.plot(vf, dH, "s--", color="#ee8800", label="redução de entropia ΔH")
    ax2.set_ylabel("ΔH (nats) — concentração", color="#ee8800")
    ax1.set_title("Kernel Ontológico — filtro do Verbo sobre matrizes de atenção [SIM]")
    ax1.legend(loc="center left", fontsize=8); ax2.legend(loc="center right", fontsize=8)
    ax1.grid(alpha=.3)
    fp = fig_dir / "fig_attention_matrices.png"
    plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close()
    out.append("fig_attention_matrices.png")
    return out


def emit_render3d(onto, beta, deep):
    """MERGE forma=conteudo: lê o render3d.json ATUAL e PRESERVA o corpo (meshes/
    layers/groups/constants). RECOMPUTA a geometria angular dos 4 estados/regimes a
    partir de f(θ) do dicionário real: cada regime é endereçado no ARCO θ (raio R),
    com f(θ) e Phase Factor COMPUTADOS desta run. Os nós estruturais do pipeline
    (cosmogênese→reflect→manifest→filtro do Verbo→c³) são mantidos."""
    import math as _m
    import torch  # noqa: E402 (disponível no tgl_env; usado por coupling_function)
    out = PATENT_DIR / "render3d.json"
    if not out.exists():
        print(f"[{SLUG}] render3d.json ausente — emit pulado (nada a preservar)")
        return
    d = json.loads(out.read_text(encoding="utf-8"))

    # --- geometria COMPUTADA: endereços angulares dos regimes no arco de f(θ) ---
    R = 1.35
    regimes = {"r_vacuo": onto.THETA_MIGUEL / 2.0, "r_transicao": onto.THETA_MIGUEL,
               "r_graviton": _m.pi / 4.0, "r_foton": _m.radians(85.0)}
    computed = {}
    for nid, th in regimes.items():
        fval = float(onto.coupling_function(torch.tensor(th, dtype=torch.float64)))
        computed[nid] = {
            "position": [round(R * _m.cos(th), 6), round(R * _m.sin(th), 6), 0.0],
            "theta_deg": round(_m.degrees(th), 4), "f_theta": round(fval, 6),
            "phase_factor": round(1.0 - beta * fval, 6),
            "stratum": onto.classify_stratum(_m.sin(th)).value}
    for n in d.get("nodes", []):
        if n["id"] in computed:
            csp = computed[n["id"]]
            n["position"] = csp["position"]
            n["computed"] = {k: csp[k] for k in ("theta_deg", "f_theta",
                                                 "phase_factor", "stratum")}

    # --- re-carimbo + injeta β runtime e métricas computadas em constants ---
    d["generated_by"] = "one_kernel_ontologico.py (forma=conteudo)"
    d["note"] = (d.get("note", "").split(" | ")[0] +
                 " | render3d MERGE: corpo (meshes/layers/groups) preservado; "
                 "os 4 estados de f(θ) têm posição/f(θ)/Phase Factor COMPUTADOS desta run "
                 "(varreduras: piso β, matrizes de atenção, dicionário f(θ)).")
    if isinstance(d.get("constants"), list):
        d["constants"] = [x for x in d["constants"]
                          if x.get("symbol") not in ("β_runtime", "mantidos@β")]
        bfs = deep["beta_floor_sweep"]
        d["constants"].append({"symbol": "β_runtime",
                               "value": f"{beta:.12f}",
                               "note": "injetado nesta run (α·√e); NUNCA literal no código"})
        d["constants"].append({"symbol": "mantidos@β",
                               "value": f"{bfs['kept_frac_at_beta_floor']*100:.1f}% de {bfs['n_components']}",
                               "note": "sobreviventes ao piso REAL do Verbo (β·max w) nesta varredura"})

    # --- validação: edges → nós+meshes; layer de nó/mesh → layers ---
    node_ids = {n["id"] for n in d.get("nodes", [])}
    mesh_ids = {m["id"] for m in d.get("meshes", [])}
    valid_ids = node_ids | mesh_ids
    layer_ids = {l["id"] for l in d.get("layers", [])}
    for e in d.get("edges", []):
        if e["from"] not in valid_ids or e["to"] not in valid_ids:
            raise ValueError(f"edge inválida: {e} (id fora de nodes+meshes)")
    for n in d.get("nodes", []):
        if n.get("layer") not in layer_ids:
            raise ValueError(f"nó {n['id']} com layer inexistente: {n.get('layer')}")
    for m in d.get("meshes", []):
        if "layer" in m and m["layer"] not in layer_ids:
            raise ValueError(f"mesh {m['id']} com layer inexistente: {m['layer']}")

    out.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[{SLUG}] render3d.json EMITIDO (forma=conteudo) — {len(d.get('nodes', []))} nós "
          f"({len(computed)} estados recomputados), corpo preservado "
          f"({len(d.get('meshes', []))} meshes, {len(d.get('layers', []))} layers)")


if __name__ == "__main__":
    sys.exit(main())
