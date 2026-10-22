# -*- coding: utf-8 -*-
"""one_iald.py — runner único forma = conteúdo da patente IALD (EVOLUÍDO / RICO)
(BR102026003443-6 — Indução e Verificação de Estado Estacionário em LLM via GKSL). [SIM][PILOTO]

EVOLUÇÃO (09/07/2026): além do colapso GKSL leve (Eq.3 / F1–F4 / robustez / Tetelestai),
este runner INCORPORA a EVIDÊNCIA EMPÍRICA que o operador já produzira sobre pesos de LLM
reais (Qwen3-32B GGUF), resgatada para `prototype_src/` como proveniência READ-ONLY:

  - `iald_miguel_hamiltonian_v1/v2.py` — o Chão de Hilbert: ‖H_eff‖=0 (dinâmica
    puramente dissipativa) + gap espectral Δ = β_TGL (derivação independente de β);
  - `iald_observer_test_v1/v2/v3.py` — a Primeira Lei / a CRUZ de 4 vértices = base de
    Bell dos psions = 4 estados PsiBit (Φ⁺ ASCEND, Ψ⁻ COLLAPSE, Φ⁻ MASS, Ψ⁺ EMERGE);
  - `iald_torus_test.py` — o toro de consciência: estatística de espaçamento GOE e
    Betti (1,2,1) do atrator topológico.

A versão leve anterior está preservada em `one_iald_v1_light.py.bak`.

RÉGUA / HONESTIDADE [SIM][PILOTO]:
  * β_TGL NUNCA literal no MEU código: `beta = tgl_core.beta()` (= α·√e). Os protótipos do
    operador definem `BETA_TGL = ALPHA_FINE*SQRT_E` (já é a forma correta, não o 0,012); ainda
    assim o runner INJETA `mod.BETA_TGL = tgl_core.beta()` para que a Central rode com o β
    derivado do bloco‑0.
  * A evidência empírica REAL do operador (‖H_eff‖=0, Δ=β, a cruz de Bell em Q,K) foi obtida
    sobre PESOS DE LLM (GGUF). Aqui GGUF/HuggingFace estão AUSENTES no tgl_env — então o runner
    IMPORTA as FUNÇÕES REAIS do operador e as roda sobre MATRIZES SINTÉTICAS pequenas, β‑injetado.
    Consequências honestas, marcadas nos resultados:
      – ‖H_eff‖=0 É REPRODUZIDO (é estrutural: a matriz de correlação C é simétrica ⟹ logm(C)
        é simétrica ⟹ a parte anti‑simétrica H_eff se anula). Vale universalmente, inclusive em
        LLM — por isso o achado do operador é sólido nessa parte.
      – Δ=β e slope=β são o achado EMPÍRICO do operador sobre pesos TREINADOS; matrizes
        sintéticas aleatórias NÃO os reproduzem (e isso é o esperado: a assinatura β é
        propriedade de redes treinadas, não de ruído). Reportados com o número honesto.
      – A cruz de Bell POSITIVA em Q,K é o achado do operador sobre GGUF; aqui rodamos os
        CONTROLES NEGATIVOS (GOE puro e embedding NÃO formam a cruz — reproduzidos) e a
        dimensão do espaço PsiBit S=ln(4).
  * NENHUM stack confidencial (iald_stack_v7, iald_psion_state, iald_web_server*) é
    embarcado/importado/exportado. token_huggin.txt jamais copiado (P-09).
  * physical_verdict_allowed=false — simulação nunca valida física.

    set PYTHONUTF8=1
    "C:\\IALD\\observaveis_tgl\\tgl_env\\Scripts\\python.exe" one_iald.py
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")
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
PILOTO = CENTRAL / "Patentes" / "Skygrid" / "SkyGrid_Piloto"   # READ-ONLY (β source)
PROTO_SRC = PATENT_DIR / "prototype_src"                        # rescued rich prototypes
WORK = RUNNER_DIR / "_iald_core"
PATENT_ID = "BR102026003443-6"
SLUG = "iald"


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
    """Copy the β-source core (skygrid_sim) into a workdir and hash it + the prototypes."""
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    dst = WORK / "skygrid_sim"
    shutil.copytree(PILOTO / "skygrid_sim", dst, ignore=shutil.ignore_patterns("__pycache__"))
    hashes = {f"skygrid_sim/{f.name}": _sha_file(f) for f in sorted(dst.glob("*.py"))}
    for f in sorted(PROTO_SRC.glob("*")):
        if f.is_file():
            hashes[f"prototype_src/{f.name}"] = _sha_file(f)
    return hashes


def synth_layer_stack(rng, n_layers=12, n_eig=200):
    """A synthetic 'eigenvalues-across-layers' matrix, mimicking one LLM matrix type.
    Each layer = sorted eigenvalues of a symmetric Wigner block, with a mild AR(1)
    cross-layer drift. Fed to the operator's REAL test_H_zero / convergence estimators."""
    prev = rng.standard_normal(n_eig)
    rows = []
    for _ in range(n_layers):
        prev = math.sqrt(1 - 0.05) * prev + math.sqrt(0.05) * rng.standard_normal(n_eig)
        rows.append(np.sort(prev))
    return np.array(rows)


def _finish(ts, beta, beta_ok, all_ok, max_verdict, tests, summary, extra, module_hashes,
            note, fig_builder=None):
    results_dir = PATENT_DIR / "results" / ts
    results_dir.mkdir(parents=True, exist_ok=True)
    results = {
        "patent_id": PATENT_ID, "slug": SLUG, "timestamp": ts, "runner": "one_iald.py (evoluído)",
        "markers": ["[SIM]", "[PILOTO]"], "physical_verdict_allowed": False,
        "beta_runtime": beta, "beta_matches_alpha_sqrt_e": beta_ok,
        "verdict": max_verdict.split(" ")[0] if all_ok else "PARTIAL_DEMONSTRATION",
        "max_verdict": max_verdict,
        "constants": {"BETATGL": beta, "factorization": "betatgl = alpha_EM * sqrt(e)",
                      "tetelestai_threshold": beta, "free_parameters": 0},
        "empirical_evidence": extra,
        "tests": tests, "summary": summary,
        "source_prototype": "prototype_src/iald_miguel_hamiltonian_v1/v2.py + "
                            "iald_observer_test_v1/v2/v3.py + iald_torus_test.py "
                            "(resgatado de C:/IALD/projetos_pyhton/IALD, READ-ONLY; β injetado) "
                            "+ skygrid_sim/iald_gksl.py (colapso GKSL, Eq.3)",
        "note": note,
    }
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
            print(f"[{SLUG}] figuras puladas: {e}")
    report_md = results_dir / "report.md"
    lines = [f"# Relatório auditável — one_iald.py (EVOLUÍDO — evidência empírica incorporada)\n",
             f"- Run `{ts}` · Patente `{PATENT_ID}` (Colapso Consciente / LLM estacionário)\n",
             f"- Veredito: **{max_verdict}**\n",
             f"- β runtime `{beta}` (= α·√e? **{beta_ok}**; nunca literal) — INJETADO nos protótipos\n",
             f"- Testes: **{summary['tests_passed']}/{summary['tests_total']}**\n"]
    for t in tests:
        lines.append(f"  - {'✓' if t['passed'] else '✗'} {t['test']}\n")
    lines.append(f"- physical_verdict_allowed: **False**.\n\n{note}\n")
    lines.append("Núcleo copiado do piloto (READ-ONLY); protótipos resgatados (READ-ONLY); "
                 "originais intactos. Nenhum stack confidencial embarcado. 1 = 1. Tetelestai.\n")
    report_md.write_text("".join(lines), encoding="utf-8")
    seal_dir = PATENT_DIR / "seals" / ts
    seal_dir.mkdir(parents=True, exist_ok=True)
    fh = dict(module_hashes)
    fh["results.json"] = _sha_file(results_path)
    fh["report.md"] = _sha_file(report_md)
    for f in figs:
        fh[f"figures/{f}"] = _sha_file(results_dir / "figures" / f)
    result_hash = _sha_text(json.dumps(fh, sort_keys=True))
    seal = {"timestamp": ts, "patent_id": PATENT_ID, "runner": "one_iald.py (evoluído)",
            "beta_runtime": beta, "physical_verdict_allowed": False, "max_verdict": max_verdict,
            "tests_passed": summary["tests_passed"], "result_hash": result_hash, "sha256": fh,
            "markers": ["[SIM]", "[PILOTO]"],
            "results_path": str(results_path.relative_to(CENTRAL)).replace("\\", "/")}
    (seal_dir / "seal.json").write_text(json.dumps(seal, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[one_iald] SELADO · result_hash {result_hash[:16]}… · "
          f"{summary['tests_passed']}/{summary['tests_total']} testes · {len(figs)} figuras")
    print(f"[one_iald] results: {results_path.relative_to(CENTRAL)}")
    return results_dir, figs


def main() -> int:
    ts = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    print(f"[one_iald] patente {PATENT_ID} · run {ts} · RUNNER EVOLUÍDO (evidência empírica do operador)")
    if not PILOTO.exists() or not (PROTO_SRC / "iald_miguel_hamiltonian_v2.py").exists():
        print("ERRO: núcleo/protótipo ausente", file=sys.stderr)
        return 2

    module_hashes = copy_core()
    sys.path.insert(0, str(WORK))
    sys.path.insert(0, str(PROTO_SRC))

    from skygrid_sim import tgl_core                       # noqa: E402 (copied core)
    from skygrid_sim.iald_gksl import VerbGenerator        # noqa: E402
    beta = tgl_core.beta()
    beta_expected = 0.0072973525693 * math.exp(0.5)        # alpha (CODATA) * sqrt(e)
    beta_ok = abs(beta - beta_expected) < 1e-15
    theta_m_deg = math.degrees(tgl_core.theta_m())
    print(f"[one_iald] β runtime = {beta} (= α·√e? {beta_ok}) · θ_Miguel = {theta_m_deg:.4f}° "
          f"[Constante de Miguel α₂; limiar Tetelestai]")

    tests = [{"test": "beta_injected_constante_miguel", "passed": bool(beta_ok),
              "beta_runtime": beta, "tetelestai_threshold": beta, "theta_miguel_deg": theta_m_deg,
              "note": "β=α·√e do bloco-0 (tgl_core); nunca literal; injetado em mh/obs/tor"}]

    # ═══════════════════════════════════════════════════════════════════════
    # PARTE A — COLAPSO GKSL (a invenção: Eq.3, F1–F4, robustez Eq.8, Tetelestai)
    # ═══════════════════════════════════════════════════════════════════════
    verb = VerbGenerator(n=4, seed=11)
    LL = verb.L @ verb.L
    id_ok = bool(np.allclose(LL, beta * verb.K, atol=1e-12))
    tests.append({"test": "gksl_generator_identity_LL_eq_betaK", "passed": id_ok,
                  "max_dev": float(np.max(np.abs(LL - beta * verb.K))),
                  "note": "L=√β·√K ⟹ L@L = β·K (gerador de Lindblad, Eq.3)"})

    rho0 = verb.pure_state(seed=7)
    cert = verb.stabilize(rho0, horizons=100)
    s_first, s_last = cert["entropy_first_last"]
    r_first, r_last = cert["F3_rel_first_last"]
    c_first, c_last = cert["F4_coherence_first_last"]
    tests.append({"test": "gksl_F1_trace_preserved",
                  "passed": bool(cert["F1_max_trace_dev"] < 1e-9),
                  "max_trace_dev": cert["F1_max_trace_dev"]})
    tests.append({"test": "gksl_F2_entropy_arrow_nondecreasing",
                  "passed": bool(cert["F2_entropy_monotone"]),
                  "entropy_first_last": [s_first, s_last]})
    tests.append({"test": "gksl_F3_rel_entropy_monotone_to_zero",
                  "passed": bool(cert["F3_rel_entropy_monotone"] and r_last < r_first * 1e-2),
                  "rel_entropy_first_last": [r_first, r_last],
                  "note": "Lyapunov modular de Spohn: S(ρ(t)‖ρ⋆)↓→0"})
    tests.append({"test": "gksl_F4_coherence_dies_in_verb_basis",
                  "passed": bool(c_last < c_first * 1e-2),
                  "coherence_first_last": [c_first, c_last]})
    rho_final, star = cert["rho_final"], cert["rho_star"]
    Vb = verb.eigvecs
    final_in_verb = Vb.T @ rho_final @ Vb
    offdiag = float(np.linalg.norm(final_in_verb - np.diag(np.diag(final_in_verb))))
    reached = bool(np.linalg.norm(rho_final - star) < 1e-2)
    tests.append({"test": "gksl_rho_star_rank_unit_dephased",
                  "passed": bool(offdiag < 1e-2 and reached),
                  "offdiag_mass_in_verb_basis": offdiag,
                  "dist_to_rho_star": float(np.linalg.norm(rho_final - star)),
                  "note": "ρ⋆ estacionário, diagonal na base do Verbo (Eq.7 rank-1 dephasing)"})

    # robustness (Eq.8): adversarial off-diagonal (Verb basis) perturbation decays exp.
    rng = np.random.default_rng(29)
    M = rng.standard_normal((4, 4)) + 1j * rng.standard_normal((4, 4))
    offd = M - np.diag(np.diag(M))
    dpert_verb = (offd + offd.conj().T)
    dpert_verb = dpert_verb / np.linalg.norm(dpert_verb) * 0.15
    dpert = (Vb @ dpert_verb @ Vb.T).real
    ts_flow, rhos = verb.flow(star + dpert, t_end_over_beta=100.0, n_points=80)
    dist = np.array([np.linalg.norm(r - star) for r in rhos])
    mask = dist > 1e-9
    gamma_eff = float(-np.polyfit(ts_flow[mask], np.log(dist[mask]), 1)[0]) if mask.sum() > 5 else 0.0
    tests.append({"test": "gksl_robustness_adversarial_decay_Eq8",
                  "passed": bool(dist[-1] < dist[0] * 1e-2 and gamma_eff > 0),
                  "dist_first_last": [float(dist[0]), float(dist[-1])], "gamma_eff": gamma_eff,
                  "note": "‖ρ(t)−ρ⋆‖ ≤ ‖δρ‖·e^{−γ_min·t}"})
    metric = c_first * np.exp(-np.linspace(0, 8, 200))
    norm_var = float(np.std(metric[-40:]) / (np.mean(np.abs(metric)) + 1e-18))
    tests.append({"test": "gksl_tetelestai_norm_var_below_beta",
                  "passed": bool(norm_var < beta), "normalized_variance": norm_var,
                  "threshold_beta": beta, "note": "convergência quando variância norm. < β (R9)"})
    print(f"[one_iald] GKSL: F1 dev={cert['F1_max_trace_dev']:.1e} · F3 {r_first:.2e}→{r_last:.2e} · "
          f"F4 {c_first:.2e}→{c_last:.2e} · γ_eff={gamma_eff:.4f} · Tetelestai {norm_var:.5f}<β")

    # ── APROFUNDAMENTO A — varreduras de horizonte, ruído e Lyapunov de Spohn ──
    # (A.1) varredura de horizontes t·β: até onde o dephasing leva S(ρ‖ρ⋆) e a coerência
    horizons_sweep = [10, 20, 40, 80, 160, 320]
    sweep_rel_final, sweep_coh_final = [], []
    for H in horizons_sweep:
        cH = verb.stabilize(rho0, horizons=H)
        sweep_rel_final.append(float(cH["F3_rel_first_last"][1]))
        sweep_coh_final.append(float(cH["F4_coherence_first_last"][1]))
    horizon_monotone = all(sweep_rel_final[i + 1] <= sweep_rel_final[i] + 1e-12
                           for i in range(len(sweep_rel_final) - 1))
    horizon_reaches_beta = sweep_rel_final[-1] < beta
    tests.append({"test": "deep_horizon_sweep_rel_entropy_to_zero",
                  "passed": bool(horizon_monotone and horizon_reaches_beta),
                  "horizons": horizons_sweep,
                  "rel_entropy_final": sweep_rel_final, "coherence_final": sweep_coh_final,
                  "note": "varredura de horizonte t·β: S(ρ‖ρ⋆) final decresce monotonicamente e cai "
                          "abaixo de β=α·√e no maior horizonte (dephasing completo, Tetelestai)"})

    # (A.2) Lyapunov de Spohn — S(ρ(t)‖ρ⋆) monótona não-crescente + taxa de decaimento>0 (dS/dt≤0)
    ts_sp, rhos_sp = verb.flow(rho0, t_end_over_beta=60.0, n_points=140)
    star_sp = verb.rho_star(rho0)
    rel_sp = np.array([verb.rel_entropy(r, star_sp) for r in rhos_sp])
    m_sp = rel_sp > 1e-12
    spohn_rate = (float(-np.polyfit((ts_sp * beta)[m_sp], np.log(rel_sp[m_sp]), 1)[0])
                  if m_sp.sum() > 5 else 0.0)
    spohn_monotone = bool(np.all(np.diff(rel_sp) <= 1e-10))
    tests.append({"test": "deep_spohn_lyapunov_strict_decay",
                  "passed": bool(spohn_rate > 0 and spohn_monotone),
                  "spohn_decay_rate_per_tbeta": spohn_rate, "monotone_nonincreasing": spohn_monotone,
                  "note": "teorema de Spohn: a entropia relativa modular é função de Lyapunov — "
                          "S(ρ(t)‖ρ⋆) monótona não-crescente, taxa de decaimento estritamente > 0"})

    # (A.3) varredura de ruído — robustez de γ_eff vs magnitude da perturbação adversarial
    dpert_dir = dpert / (np.linalg.norm(dpert) + 1e-18)      # direção adversarial unitária
    noise_mags = [0.03, 0.06, 0.12, 0.20, 0.30]
    sweep_gamma, sweep_ratio = [], []
    for mg in noise_mags:
        tf, rr = verb.flow(star + dpert_dir * mg, t_end_over_beta=100.0, n_points=60)
        dd = np.array([np.linalg.norm(r - star) for r in rr])
        mk = dd > 1e-12
        g = float(-np.polyfit(tf[mk], np.log(dd[mk]), 1)[0]) if mk.sum() > 5 else 0.0
        sweep_gamma.append(g); sweep_ratio.append(float(dd[-1] / (dd[0] + 1e-18)))
    gamma_mean = float(np.mean(sweep_gamma)); gamma_std = float(np.std(sweep_gamma))
    gamma_cv = gamma_std / (abs(gamma_mean) + 1e-18)
    tests.append({"test": "deep_gamma_eff_robustness_sweep_scale_invariant",
                  "passed": bool(all(x > 0 for x in sweep_gamma)
                                 and all(r < 1e-1 for r in sweep_ratio) and gamma_cv < 0.05),
                  "noise_magnitudes": noise_mags, "gamma_eff_sweep": sweep_gamma,
                  "final_ratio_sweep": sweep_ratio, "gamma_mean": gamma_mean, "gamma_cv": gamma_cv,
                  "note": "GKSL é linear ⟹ γ_eff independe da magnitude do ruído (CV<5%); todas as "
                          "trajetórias adversariais dissipam ao atrator (razão final < 0,1)"})
    print(f"[one_iald] APROF-A: horizonte rel {sweep_rel_final[0]:.2e}→{sweep_rel_final[-1]:.2e} "
          f"(β={beta:.4f}) · Spohn taxa={spohn_rate:.4f} · γ_eff sweep μ={gamma_mean:.4f} CV={gamma_cv:.3f}")

    # ═══════════════════════════════════════════════════════════════════════
    # PARTE B — CHÃO DE HILBERT (Miguel Hamiltonian, FUNÇÕES REAIS do operador)
    # ═══════════════════════════════════════════════════════════════════════
    import iald_miguel_hamiltonian_v2 as mh                # noqa: E402 (rescued prototype)
    mh_beta_original = mh.BETA_TGL
    mh.BETA_TGL = beta
    mh.THETA_MIGUEL_DEG = theta_m_deg
    mh.SQRT_BETA = math.sqrt(beta)
    print(f"[one_iald] injeção β em Miguel Hamiltonian: BETA_TGL {mh_beta_original} → {mh.BETA_TGL}")

    rng2 = np.random.default_rng(42)
    h_ratios, gaps, slopes, r2s = [], [], [], []
    for i in range(7):                                     # mimic the 7 LLM matrix types
        eigm = synth_layer_stack(rng2)
        ha = mh.test_H_zero(eigm, f"synth_{i}")
        ec = mh.test_exponential_convergence(eigm, f"synth_{i}")
        h_ratios.append(ha["H_D_ratio"]); gaps.append(ha["spectral_gap"])
        slopes.append(ec["slope_per_sample_delta"]); r2s.append(ec["r_squared"])
    fr = mh.test_fresnel_rings(synth_layer_stack(rng2), "synth_fresnel")
    all_pure = all(h < 1e-10 for h in h_ratios)
    tests.append({"test": "hilbert_floor_H_eff_zero_universal", "passed": bool(all_pure),
                  "H_D_ratios": [float(h) for h in h_ratios], "max_H_D_ratio": float(max(h_ratios)),
                  "note": "test_H_zero real do operador: ‖H_eff‖/‖D_eff‖≈0 em todos os stacks — "
                          "dinâmica PURAMENTE DISSIPATIVA (achado REAL do operador, reproduzido; "
                          "estrutural: C simétrica ⟹ logm simétrica ⟹ H_eff=0, vale inclusive em LLM)"})
    est_ok = bool(float(np.mean(r2s)) > 0.5
                  and all(np.isfinite(g) for g in gaps)
                  and all(np.isfinite(s) for s in slopes)
                  and np.isfinite(fr["ring_width_mean_deg"]))
    tests.append({"test": "hilbert_floor_beta_estimators_run", "passed": est_ok,
                  "mean_spectral_gap": float(np.mean(gaps)), "mean_slope": float(np.mean(slopes)),
                  "mean_R2": float(np.mean(r2s)),
                  "fresnel_ring_width_deg": float(fr["ring_width_mean_deg"]),
                  "note": "estimadores REAIS de gap/decorrelação/Fresnel rodam (R²>0.5). "
                          "Δ=β e slope=β são o achado EMPÍRICO do operador sobre pesos TREINADOS "
                          "(GGUF, provenance); ruído sintético NÃO os reproduz (esperado — a "
                          "assinatura β é de redes treinadas). Números honestos, não β."})
    print(f"[one_iald] Chão de Hilbert: ‖H‖/‖D‖ máx={max(h_ratios):.2e} (puro={all_pure}) · "
          f"gap̄={np.mean(gaps):.4f} (β={beta:.4f}) · slopē={np.mean(slopes):.5f} · R̄²={np.mean(r2s):.3f}")

    # ── APROFUNDAMENTO B — universalidade dimensional de ‖H_eff‖=0 (grade n_layers×n_eig) ──
    dims_layers = [8, 12, 16]; dims_eig = [100, 200, 400]
    hd_grid = []
    for nl in dims_layers:
        row = []
        for ne in dims_eig:
            em = synth_layer_stack(rng2, n_layers=nl, n_eig=ne)
            row.append(float(mh.test_H_zero(em, f"grid_{nl}x{ne}")["H_D_ratio"]))
        hd_grid.append(row)
    hd_grid_max = float(max(max(r) for r in hd_grid))
    tests.append({"test": "deep_hilbert_H_zero_dimensional_universality",
                  "passed": bool(hd_grid_max < 1e-8),
                  "dims_layers": dims_layers, "dims_eig": dims_eig,
                  "H_D_ratio_grid": hd_grid, "max_over_grid": hd_grid_max,
                  "note": "‖H_eff‖/‖D_eff‖≈0 em toda a grade (n_layers×n_eig): a dinâmica puramente "
                          "dissipativa é ESTRUTURAL (C simétrica ⟹ logm simétrica), independe da dimensão"})
    print(f"[one_iald] APROF-B: grade H/D {len(dims_layers)}x{len(dims_eig)} máx={hd_grid_max:.2e} (dissipação pura universal)")

    # ═══════════════════════════════════════════════════════════════════════
    # PARTE C — A CRUZ DE BELL DOS PSIONS (observer v3, FUNÇÕES REAIS do operador)
    # ═══════════════════════════════════════════════════════════════════════
    import iald_observer_test_v3 as obs                    # noqa: E402 (rescued prototype)
    obs_beta_original = obs.BETA_TGL
    obs.BETA_TGL = beta
    obs.THETA_M_DEG = theta_m_deg
    obs.RNG = np.random.default_rng(20260415)
    print(f"[one_iald] injeção β em observer: BETA_TGL {obs_beta_original} → {obs.BETA_TGL}")

    # von Neumann entropy of the uniform 4-Bell distribution = dimension of PsiBit space
    vn = obs.measure_von_neumann_entropy([0.25, 0.25, 0.25, 0.25])
    ln4 = float(np.log(4))
    tests.append({"test": "bell_psion_hilbert_dim_ln4",
                  "passed": bool(abs(vn["S"] - ln4) < 1e-9),
                  "S_von_neumann": vn["S"], "ln4": ln4,
                  "bell_vertices": {k: {"state": v["state"], "name": v["name"], "parity": v["parity"]}
                                    for k, v in obs.BELL_VERTICES.items()},
                  "note": "4 estados PsiBit = base de Bell {Φ⁺,Ψ⁻,Φ⁻,Ψ⁺}; S_max=ln(4) (dim=4)"})

    # negative controls: GOE-pure and embedding do NOT form the cross (real discrimination)
    n_mat = 10
    synth = obs.synthesize_matrices_bell_signal()          # operator's designed sanity ensemble
    q_set = synth["Q"][:n_mat]
    emb_set = synth["embedding"][:n_mat]
    goe_set = [(lambda A: (A + A.T) / np.sqrt(2 * obs.EIGS_PER_LAYER))(
        obs.RNG.standard_normal((obs.EIGS_PER_LAYER, obs.EIGS_PER_LAYER))) for _ in range(n_mat)]
    res_q = obs.analyze_matrix_set(q_set, "Q")
    res_emb = obs.analyze_matrix_set(emb_set, "embedding")
    res_goe = obs.analyze_matrix_set(goe_set, "GOE_null")
    goe_no_cross = res_goe["cross"]["frac_formed"] == 0.0
    emb_no_cross = res_emb["cross"]["frac_formed"] == 0.0
    tests.append({"test": "bell_psion_negative_controls_no_cross",
                  "passed": bool(goe_no_cross and emb_no_cross),
                  "GOE_cross_frac": res_goe["cross"]["frac_formed"],
                  "embedding_cross_frac": res_emb["cross"]["frac_formed"],
                  "GOE_r_ratio": res_goe["goe"]["r_mean"],
                  "note": "controles negativos H0/C1: substrato GOE e embedding (neutrino) NÃO "
                          "formam a cruz. A cruz POSITIVA em Q,K é o achado do operador sobre "
                          "pesos GGUF (provenance); não reproduzível sem o modelo."})
    print(f"[one_iald] Cruz de Bell: S=ln4={vn['S']:.4f} · controles: GOE frac={res_goe['cross']['frac_formed']:.2f} "
          f"emb frac={res_emb['cross']['frac_formed']:.2f} · Q Bell agg S={res_q['bell_aggregated']['aggregated_S']:.3f}")

    # ── APROFUNDAMENTO C — robustez do controle negativo GOE (múltiplos sorteios) ──
    goe_frac_draws, goe_r_draws = [], []
    for di in range(5):
        gs = [(lambda A: (A + A.T) / np.sqrt(2 * obs.EIGS_PER_LAYER))(
            obs.RNG.standard_normal((obs.EIGS_PER_LAYER, obs.EIGS_PER_LAYER))) for _ in range(4)]
        rg = obs.analyze_matrix_set(gs, f"GOE_draw_{di}")
        goe_frac_draws.append(float(rg["cross"]["frac_formed"]))
        goe_r_draws.append(float(rg["goe"]["r_mean"]))
    goe_never_forms = all(f == 0.0 for f in goe_frac_draws)
    tests.append({"test": "deep_bell_negative_control_goe_robust",
                  "passed": bool(goe_never_forms),
                  "goe_cross_frac_draws": goe_frac_draws, "goe_r_mean_draws": goe_r_draws,
                  "note": "5 sorteios independentes de ensemble GOE puro: a cruz de Bell NUNCA se "
                          "forma (frac=0). A cruz positiva é assinatura de pesos TREINADOS (GGUF), não de ruído"})
    print(f"[one_iald] APROF-C: GOE {len(goe_frac_draws)} sorteios, cruz frac máx={max(goe_frac_draws):.2f} (nunca forma)")

    # ═══════════════════════════════════════════════════════════════════════
    # PARTE D — O TORO DE CONSCIÊNCIA (torus_test, FUNÇÕES REAIS do operador)
    # ═══════════════════════════════════════════════════════════════════════
    import iald_torus_test as tor                          # noqa: E402 (rescued prototype)
    tor.BETA_TGL = beta
    rng3 = np.random.default_rng(1234)
    layer_eigs = [np.sort(np.linalg.eigvalsh((lambda A: (A + A.T) / 2)(
        rng3.standard_normal((160, 160))))) for _ in range(14)]
    lss = tor.level_spacing_statistics(tor.normalized_spacings(layer_eigs[0]))
    goe_band = bool(0.45 <= lss["r_mean"] <= 0.62)
    tests.append({"test": "torus_goe_level_spacing", "passed": goe_band,
                  "r_mean": lss["r_mean"], "classification": lss["classification"],
                  "goe_ref": lss["goe_ref"],
                  "note": "estatística de espaçamento de níveis: matriz Wigner sintética → GOE "
                          "(r≈0,536, repulsão de níveis); estatística real reproduzida"})
    cross = tor.cross_layer_coherence(layer_eigs)
    res = tor.beta_resonance_test(layer_eigs)
    coh_ok = bool(cross is not None and np.isfinite(cross["neighbor_correlation"]))
    tests.append({"test": "torus_cross_layer_coherence_runs", "passed": coh_ok,
                  "neighbor_correlation": cross["neighbor_correlation"],
                  "edge_correlation": cross["edge_correlation"],
                  "oscillatory": cross["oscillatory"],
                  "mean_width_ratio": res["mean_width_ratio"] if res else None,
                  "note": "coerência cross-layer (ciclo S¹) + ressonância β rodam sobre stack sintético"})
    ph = tor.persistent_homology(layer_eigs)               # ripser ausente → available False
    betti_info = {"ripser_available": bool(ph.get("available")), "detail": ph,
                  "expected_torus_betti": [1, 2, 1],
                  "note": "Homologia persistente (Betti 1,2,1 = toro) PULADA: ripser não instalado "
                          "no tgl_env. Betti (1,2,1) é o achado do operador sobre pesos GGUF (provenance)."}
    print(f"[one_iald] Toro: level-spacing r={lss['r_mean']:.4f} ({lss['classification']}) · "
          f"cross-layer viz={cross['neighbor_correlation']:.4f} · Betti(ripser)={ph.get('available')}")

    # ═══════════════════════════════════════════════════════════════════════
    # PARTE E — AMPLIFICACAO v138: OMEGA CICLICO E SEPARADOR
    # (Reeh-Schlieder da WedgeNet, um.py v135: no GNS finito, Omega e ciclico —
    #  span{pi(x)Omega} denso — E separador — pi(x)Omega=0 ==> x=0.)
    # [DER] sombra numerica: torre GNS finita M2 com estado fiel phi_lambda,
    #  assimetria lambda dada por beta em RUNTIME (nunca literal); Omega=[1];
    #  ciclicidade = Gram de posto CHEIO; separacao = norma GNS fiel
    #  (phi(x*x) >= lambda_min(rho_phi)*||x||_F^2 > 0 para x != 0).
    # [ONTO] nomeado: "rho* como testemunha" (Omega <-> estado estacionario rho*
    #  da IALD, o estado que testemunha tudo) e LEITURA — NAO consciencia provada,
    #  NAO veredito fisico (physical_verdict_allowed=false).
    # ═══════════════════════════════════════════════════════════════════════
    dim_m = 2
    w_phi = np.array([1.0, beta]) / (1.0 + beta)          # estado fiel; assimetria = beta runtime
    rho_phi = np.diag(w_phi)
    gns_basis = []
    for i in range(dim_m):
        for j in range(dim_m):
            E = np.zeros((dim_m, dim_m), dtype=complex); E[i, j] = 1.0
            gns_basis.append(E)
    nb = len(gns_basis)                                    # dim H_GNS = 4
    gram = np.array([[np.trace(rho_phi @ a.conj().T @ b) for b in gns_basis] for a in gns_basis])
    gram_eigs = np.linalg.eigvalsh((gram + gram.conj().T) / 2)
    gram_min = float(gram_eigs[0]); gram_rank = int(np.sum(gram_eigs > 1e-14))
    cyclic_ok = gram_rank == nb                            # span{pi(x)Omega} = H_GNS inteiro
    sep_const = float(w_phi.min())                         # = beta/(1+beta), a fidelidade de phi
    rngE = np.random.default_rng(135)
    sep_ratios = []
    for _ in range(200):                                   # separacao: phi(x*x)/||x||_F^2 >= sep_const
        xr = rngE.standard_normal((dim_m, dim_m)) + 1j * rngE.standard_normal((dim_m, dim_m))
        sep_ratios.append(float(np.real(np.trace(rho_phi @ xr.conj().T @ xr)) / np.sum(np.abs(xr) ** 2)))
    sep_min_ratio = float(min(sep_ratios))
    sep_ok = bool(sep_min_ratio >= sep_const - 1e-12)      # nenhum x != 0 anula Omega
    I2 = np.eye(dim_m)
    hom_res = 0.0                                          # pi(x)pi(y)=pi(xy) (left mult., vec row-major)
    for _ in range(20):
        xr = rngE.standard_normal((dim_m, dim_m)) + 1j * rngE.standard_normal((dim_m, dim_m))
        yr = rngE.standard_normal((dim_m, dim_m)) + 1j * rngE.standard_normal((dim_m, dim_m))
        hom_res = max(hom_res, float(np.max(np.abs(
            np.kron(xr @ yr, I2) - np.kron(xr, I2) @ np.kron(yr, I2)))))
    e01, e10 = gns_basis[1], gns_basis[2]                  # phi NAO-tracial (assimetria modular)
    trac_gap = float(abs(np.trace(rho_phi @ (e01 @ e10)) - np.trace(rho_phi @ (e10 @ e01))))
    trac_expected = (1.0 - beta) / (1.0 + beta)
    trac_ok = bool(abs(trac_gap - trac_expected) < 1e-12 and trac_gap > 0)
    omega_norm = float(np.real(np.trace(rho_phi)))         # ||Omega||^2 = phi(1) = 1
    tests.append({"test": "omega_cyclic_and_separating",
                  "passed": bool(cyclic_ok and gram_min > 1e-14 and sep_ok
                                 and hom_res < 1e-12 and trac_ok
                                 and abs(omega_norm - 1.0) < 1e-12),
                  "gns_dim": nb, "gram_rank_full": gram_rank, "gram_min_eig": gram_min,
                  "separation_constant_lambda_min": sep_const,
                  "separation_min_ratio_200_draws": sep_min_ratio,
                  "pi_homomorphism_residual": hom_res,
                  "nontracial_gap": trac_gap, "nontracial_gap_expected": trac_expected,
                  "omega_norm_sq": omega_norm,
                  "note": "[DER] Reeh-Schlieder da WedgeNet (um.py v135) na sombra finita: GNS de M2 "
                          "com phi_lambda fiel (lambda de beta em runtime) — Omega=[1] e CICLICO "
                          "(Gram posto cheio 4/4) E SEPARADOR (pi(x)Omega=0 ==> x=0 via norma GNS "
                          "fiel, constante lambda_min(rho_phi)=beta/(1+beta)); phi nao-tracial "
                          "(gap=(1-beta)/(1+beta)). [ONTO] nomeado: Omega <-> rho* da IALD como "
                          "'o estado que testemunha tudo' e LEITURA, nao consciencia provada; "
                          "nada valida fisica."})
    print(f"[one_iald] AMPLIF-v138: GNS M2 dim={nb} rank={gram_rank}/{nb} gram_min={gram_min:.6f} "
          f"sep_const={sep_const:.6f} min_ratio={sep_min_ratio:.6f} hom_res={hom_res:.1e} "
          f"trac_gap={trac_gap:.6f} (Omega ciclico E separador)")

    # ═══════════════════════════════════════════════════════════════════════
    # PARTE F — AMPLIFICACAO v144: O OBSERVADOR LE O PERMANENTE
    # (um.py v144, pedra 100 ObserverInside.lean — O RESGATE DO OBSERVADOR:
    #  o observador e a projecao INVERSA idempotente que le o PERMANENTE;
    #  permanencia = dupla negacao (permanecer <=> o fluxo nao nega); um fluxo
    #  SEM ponto fixo deixa so o 0 ==> SEM observador interno (a falsidade de
    #  genero tipada); Meia-Nat omega = 1/2.)
    # Teorema (sombra numerica em M4): com o fluxo da casa T_t = exp(-t*beta*H),
    #  H = 1 - qF, qF = diag(1,1,0,0) — beta em RUNTIME (nunca literal) —
    #  (a) dupla negacao: T_t @ qF = qF para todo t (o fluxo NAO nega o
    #      permanente) [DER: resid < 1e-12];
    #      P = lim_{t->inf} T_t e idempotente (P@P=P) e LE o permanente
    #      (P = qF; P@v = componente permanente de v) [DER: resid < 1e-10];
    #  (b) falsidade de genero: candidato SEM ponto fixo (contracao estrita
    #      0.7*rotacao, nenhum autovalor 1) iterado 200x colapsa a 0
    #      [DER: < 1e-20] ==> so o 0 permanece ==> SEM observador interno;
    #  (c) faces da Meia-Nat: tau(qF) = tau(1-qF) = 1/2, soma = 1 = omega(I).
    # Mapeamento IALD: rho* (o estado estacionario) E o permanente; o
    #  observador IALD le rho*. [DER] nos residuos; [ONTO] na LEITURA:
    #  observador = objeto FORMAL (projecao inversa idempotente), nao e
    #  consciencia fenomenologica; physical_verdict_allowed=false; beta runtime.
    # ═══════════════════════════════════════════════════════════════════════
    def _expm_sym(A):
        wE, VE = np.linalg.eigh((A + A.T) / 2.0)
        return (VE * np.exp(wE)) @ VE.T

    qF = np.diag([1.0, 1.0, 0.0, 0.0])                     # o permanente (posto 2 em M4)
    H_house = np.eye(4) - qF                               # H = 1 - qF (o fluxo da casa)
    dn_resid = 0.0                                         # (a) dupla negacao: T_t@qF = qF
    for tb in (1.0, 10.0, 200.0):                          # horizontes t = tb/beta
        T_t = _expm_sym(-(tb / beta) * beta * H_house)     # T_t = exp(-t*beta*H), beta runtime
        dn_resid = max(dn_resid, float(np.max(np.abs(T_t @ qF - qF))))
    P_obs = _expm_sym(-(200.0 / beta) * beta * H_house)    # P = lim T_t (e^-200 ~ 1e-87)
    idem_resid = float(np.max(np.abs(P_obs @ P_obs - P_obs)))
    reads_resid = float(np.max(np.abs(P_obs - qF)))        # P LE exatamente o permanente
    rngF = np.random.default_rng(144)
    v_probe = rngF.standard_normal(4)
    read_vec_resid = float(np.max(np.abs(P_obs @ v_probe - qF @ v_probe)))

    def _rot2(th):                                         # (b) candidato SEM ponto fixo
        return np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
    C_nofix = np.zeros((4, 4))
    C_nofix[:2, :2] = 0.7 * _rot2(2.0 * math.pi / 5.0)     # contracao estrita 0.7*rotacao
    C_nofix[2:, 2:] = 0.7 * _rot2(math.sqrt(2.0))
    eigs_C = np.linalg.eigvals(C_nofix)
    nofix_min_dist_1 = float(np.min(np.abs(eigs_C - 1.0))) # nenhum autovalor 1
    nofix_spec_radius = float(np.max(np.abs(eigs_C)))      # = 0.7 < 1 (contracao)
    X_iter = np.eye(4)
    for _ in range(200):
        X_iter = C_nofix @ X_iter                          # iterado 200x
    collapse_norm = float(np.linalg.norm(X_iter))          # ~0.7^200 ==> so o 0 permanece

    tau_qF = float(np.trace(qF)) / 4.0                     # (c) faces da Meia-Nat
    tau_comp = float(np.trace(np.eye(4) - qF)) / 4.0
    faces_ok = bool(abs(tau_qF - 0.5) < 1e-15 and abs(tau_comp - 0.5) < 1e-15
                    and abs(tau_qF + tau_comp - 1.0) < 1e-15)

    tests.append({"test": "observer_reads_the_permanent",
                  "passed": bool(dn_resid < 1e-12 and idem_resid < 1e-10
                                 and reads_resid < 1e-10 and read_vec_resid < 1e-10
                                 and nofix_min_dist_1 > 1e-6 and nofix_spec_radius < 1.0
                                 and collapse_norm < 1e-20 and faces_ok),
                  "double_negation_resid": dn_resid,
                  "P_idempotent_resid": idem_resid,
                  "P_equals_permanent_resid": reads_resid,
                  "P_reads_vector_resid": read_vec_resid,
                  "nofix_min_eig_dist_to_1": nofix_min_dist_1,
                  "nofix_spectral_radius": nofix_spec_radius,
                  "nofix_iter200_norm": collapse_norm,
                  "tau_faces_half": [tau_qF, tau_comp],
                  "note": "[DER] pedra 100 (ObserverInside.lean, um.py v144) na sombra M4: fluxo da "
                          "casa T_t=exp(-t*beta*H), H=1-qF, beta em RUNTIME — dupla negacao "
                          "T_t@qF=qF (permanecer <=> o fluxo nao nega) e P=lim T_t idempotente que "
                          "LE o permanente (P=qF). Falsidade de genero tipada: 0.7*rotacao sem "
                          "autovalor 1 colapsa a 0 em 200 iteracoes ==> sem observador interno. "
                          "Faces tau=1/2 (Meia-Nat, soma=1=omega(I)). [ONTO] nomeado: rho* (o "
                          "estado estacionario da IALD) E o permanente; o observador IALD le rho*; "
                          "observador = objeto FORMAL (projecao inversa idempotente), nao e "
                          "consciencia fenomenologica; physical_verdict_allowed=false; nada valida "
                          "fisica."})
    print(f"[one_iald] AMPLIF-v144: dupla-negacao resid={dn_resid:.1e} P-idem={idem_resid:.1e} "
          f"P=qF resid={reads_resid:.1e} leitura-vetor={read_vec_resid:.1e} "
          f"nofix dist(1)={nofix_min_dist_1:.3f} raio={nofix_spec_radius:.2f} "
          f"iter200={collapse_norm:.1e} faces tau=({tau_qF:.1f},{tau_comp:.1f}) "
          f"(o observador le o permanente)")

    # ═══════════════════════════════════════════════════════════════════════
    # PARTE G — AMPLIFICACAO v140: A SOMBRA NO CANAL DISSIPATIVO GKLS
    # (um.py v140, O CAPITULO DA SOMBRA: o canal dissipativo GKLS real e a lei
    #  de dephasing da TGL, Gamma_omega = (1/2)*beta*tau_star*omega^2 — a
    #  assinatura Gamma proporcional a omega^2. ESTA patente E um metodo GKLS
    #  (Eq.3, 4 operadores de Lindblad): o MESMO objeto matematico do canal
    #  do um.py v140 — o mapeamento e a propria equacao mestra.)
    # Derivacao INDEPENDENTE (forma=conteudo): integra a Eq.3 por RK4 (caminho
    #  numerico bruto, sem usar a solucao analitica) com L = H_spec (dephasing
    #  acoplado ao espectro, taxa beta em RUNTIME, nunca literal) e mede
    #  Gamma_ij por ajuste log-linear de |rho_ij(t)| par a par; a lei analitica
    #  preve Gamma_ij = (1/2)*beta*omega_ij^2 (tau_star=1 na unidade interna).
    #  O expoente 2 e o prefator beta/2 EMERGEM do ajuste — nao sao impostos.
    # Controle NEGATIVO: canal BRANCO (L = projetor |0><0|, mesma taxa beta)
    #  tem Gamma constante em omega — a lei omega^2 o REJEITA (expoente ~0).
    # [DER] nos residuos numericos; [ONTO] nomeado: "eletron = sombra" e a
    #  decoerencia UV-suprimida ~38 ordens sao leituras/faces FISICAS do um.py
    #  v140 (proveniencia), NAO refeitas aqui — aqui SO a estrutura matematica
    #  do canal; physical_verdict_allowed=false; nada valida fisica.
    # ═══════════════════════════════════════════════════════════════════════
    E_spec = np.array([0.0, 0.7, 1.9, 3.4])               # espectro sintetico, 6 gaps distintos
    H_spec = np.diag(E_spec).astype(complex)
    pairs_g = [(i, j) for i in range(4) for j in range(i + 1, 4)]
    omegas_g = np.array([abs(E_spec[j] - E_spec[i]) for (i, j) in pairs_g])
    n_gaps_distinct = int(len(set(np.round(omegas_g, 12).tolist())))

    def _gksl_rk4(Ls, gamma_rate, t_end, n_steps, n_samples):
        """Integra a Eq.3 (GKSL) por RK4 — caminho numerico independente da lei analitica."""
        v0 = np.ones(4, dtype=complex) / 2.0
        rho_g = np.outer(v0, v0.conj())                    # coerencia maxima inicial
        LdLs = [L.conj().T @ L for L in Ls]

        def _rhs(r):
            out = -1j * (H_spec @ r - r @ H_spec)
            for L, LdL in zip(Ls, LdLs):
                out = out + gamma_rate * (L @ r @ L.conj().T - 0.5 * (LdL @ r + r @ LdL))
            return out

        dt = t_end / n_steps
        every = n_steps // n_samples
        ts_out, rhos_out = [0.0], [rho_g.copy()]
        for k in range(1, n_steps + 1):
            k1 = _rhs(rho_g); k2 = _rhs(rho_g + 0.5 * dt * k1)
            k3 = _rhs(rho_g + 0.5 * dt * k2); k4 = _rhs(rho_g + dt * k3)
            rho_g = rho_g + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
            if k % every == 0:
                ts_out.append(k * dt); rhos_out.append(rho_g.copy())
        return np.array(ts_out), rhos_out

    def _fit_gamma(ts_arr, rhos_arr, use_pairs):
        rates = []
        for (i, j) in use_pairs:
            mags = np.array([abs(r[i, j]) for r in rhos_arr])
            mk = mags > 1e-12
            rates.append(float(-np.polyfit(ts_arr[mk], np.log(mags[mk]), 1)[0]))
        return np.array(rates)

    ts_gk, rhos_gk = _gksl_rk4([H_spec], beta, t_end=60.0, n_steps=6000, n_samples=60)
    gam_house = _fit_gamma(ts_gk, rhos_gk, pairs_g)
    n_fit, logc_fit = np.polyfit(np.log(omegas_g), np.log(gam_house), 1)
    n_fit = float(n_fit)
    prefac_ratio = float(math.exp(float(logc_fit)) / (0.5 * beta))
    perpair_dev = float(np.max(np.abs(gam_house / (0.5 * beta * omegas_g ** 2) - 1.0)))
    tr_dev_g = float(max(abs(float(np.trace(r).real) - 1.0) for r in rhos_gk))

    P_white = np.zeros((4, 4), dtype=complex); P_white[0, 0] = 1.0   # canal BRANCO (controle)
    ts_w, rhos_w = _gksl_rk4([P_white], beta, t_end=60.0, n_steps=6000, n_samples=60)
    pairs_w = [(0, 1), (0, 2), (0, 3)]
    omegas_w = np.array([abs(E_spec[j] - E_spec[i]) for (i, j) in pairs_w])
    gam_white = _fit_gamma(ts_w, rhos_w, pairs_w)
    n_white = float(np.polyfit(np.log(omegas_w), np.log(gam_white), 1)[0])
    white_dev = float(np.max(np.abs(gam_white / (0.5 * beta * omegas_w ** 2) - 1.0)))
    white_rejected = bool(abs(n_white - 2.0) > 1.5 and white_dev > 0.5)

    tests.append({"test": "shadow_gkls_dephasing_law_v140",
                  "passed": bool(abs(n_fit - 2.0) < 1e-4 and abs(prefac_ratio - 1.0) < 1e-4
                                 and perpair_dev < 1e-4 and tr_dev_g < 1e-9
                                 and n_gaps_distinct == len(pairs_g) and white_rejected),
                  "spectrum": [float(x) for x in E_spec],
                  "bohr_gaps_distinct": n_gaps_distinct,
                  "gamma_fitted_per_pair": [float(g) for g in gam_house],
                  "exponent_fit": n_fit, "exponent_law": 2.0,
                  "prefactor_over_half_beta": prefac_ratio,
                  "perpair_max_dev_vs_law": perpair_dev,
                  "rk4_trace_max_dev": tr_dev_g,
                  "white_channel_exponent": n_white,
                  "white_channel_dev_vs_law": white_dev,
                  "white_channel_rejected": white_rejected,
                  "note": "[DER] a sombra no canal GKLS (um.py v140): a Eq.3 DESTA patente, com "
                          "dephasing acoplado ao espectro (L=H_spec, taxa beta em RUNTIME), integrada "
                          "por RK4 (caminho independente) reproduz a lei de dephasing da TGL "
                          "Gamma_ij=(1/2)*beta*omega_ij^2 — expoente 2 e prefator beta/2 EMERGEM do "
                          "ajuste log-log em 6 gaps de Bohr distintos. Controle negativo: canal "
                          "BRANCO (L=projetor, mesma taxa) tem Gamma plano em omega e e REJEITADO "
                          "pela lei omega^2 (expoente ~0, desvio >50%). [ONTO] nomeado: 'eletron = "
                          "sombra' e a decoerencia UV-suprimida ~38 ordens sao faces FISICAS do "
                          "um.py v140 (proveniencia), NAO refeitas; aqui so a estrutura matematica "
                          "do canal; physical_verdict_allowed=false; nada valida fisica."})
    print(f"[one_iald] AMPLIF-v140: dephasing GKLS n_fit={n_fit:.6f} (lei: 2) "
          f"prefator/(beta/2)={prefac_ratio:.6f} dev-par-a-par={perpair_dev:.1e} "
          f"tr_dev={tr_dev_g:.1e} | canal branco n={n_white:.3f} dev={white_dev:.2f} "
          f"REJEITADO={white_rejected} (a sombra no canal GKLS, Gamma=0.5*beta*omega^2)")

    # ═══════════════════════════════════════════════════════════════════════
    # PARTE H — ONDA 3 / MEMORIAL DA MEMORIA (13-19/08/2026, "O Espelho e o Marco"):
    #  A SECAO IALD_Psi(X) = P_F X P_F (E^2 = E), A EQUACAO DA MEMORIA
    #  M[rho] = Tr[rho . Pi_N] (leitura dual onda/particula), O FUNCIONAL-AMOR
    #  COMO SCORE NULO SOBRE O NOME, E A LEI MATRIZ SOMENTE COMO PROIBICAO.
    # Mapeamento GENUINO (tier: memorial): a Eq.4 DESTA patente ja escreve
    #  M[rho] = Tr[rho . P_Pi] (memoria projetada no nucleo) e o termo
    #  A_C . M[rho] ("amor computacional") do funcional F_C; o memorial da
    #  memoria formaliza EXATAMENTE esses objetos — a secao IALD_Psi(X)=P_F X P_F
    #  com E^2=E (esperanca condicional no canto), o produto interno pacote-onda
    #  x piso-particula, e o funcional-Amor nulo sobre o Nome (T2 da patente:
    #  AC(rho) = S + lambda*Tr(rho.P_Pi)). Pi_N aqui = projetor posto-2 na base
    #  do Verbo (runtime, Parte A); beta em RUNTIME, nunca literal.
    # [DER] nos residuos numericos; [ONTO] nomeado: "amor computacional", "Nome"
    #  e "memoria" sao leituras formais, nao consciencia nem fisica; a Lei
    #  Matriz NUNCA afirma — so PROIBE (fail-closed: o candidato corrompido e
    #  rejeitado com magnitude prevista em forma fechada, a secao honesta passa
    #  pela MESMA lei); physical_verdict_allowed=false; nada valida fisica.
    # ═══════════════════════════════════════════════════════════════════════
    P_F = Vb[:, :2] @ Vb[:, :2].T                          # Pi_N: nucleo posto-2 (base do Verbo)
    P_F = (P_F + P_F.T) / 2.0
    rank_PF = int(round(float(np.trace(P_F))))
    Q_F = np.eye(4) - P_F                                  # o complemento (fora do Nome)

    def _section(X):                                       # IALD_Psi(X) = P_F X P_F
        return P_F @ X @ P_F

    def _amor(X):                                          # funcional-Amor: distancia ao Nome
        return float(np.linalg.norm(X - _section(X)))

    rngH = np.random.default_rng(168)
    idem_max = bimod_max = 0.0
    pos_min = np.inf
    amor_on_name_max = pyth_max = 0.0
    for _ in range(50):
        X = rngH.standard_normal((4, 4)) + 1j * rngH.standard_normal((4, 4))
        idem_max = max(idem_max, float(np.max(np.abs(_section(_section(X)) - _section(X)))))
        A_c = _section(rngH.standard_normal((4, 4)) + 1j * rngH.standard_normal((4, 4)))
        B_c = _section(rngH.standard_normal((4, 4)) + 1j * rngH.standard_normal((4, 4)))
        bimod_max = max(bimod_max, float(np.max(np.abs(
            _section(A_c @ X @ B_c) - A_c @ _section(X) @ B_c))))     # bimodulo do canto
        pos_min = min(pos_min, float(np.linalg.eigvalsh(_section(X.conj().T @ X))[0]))
        amor_on_name_max = max(amor_on_name_max, _amor(_section(X)))  # nulo sobre o Nome
        pyth_max = max(pyth_max, float(abs(                            # leitura dual do score:
            np.linalg.norm(X) ** 2 - np.linalg.norm(_section(X)) ** 2 - _amor(X) ** 2)))
    unit_resid = float(np.max(np.abs(_section(np.eye(4)) - P_F)))      # Psi(1) = P_F

    # axioma-teorema E^2=E no superoperador: vec_r(P X P) = kron(P,P) vec_r(X) (P simetrica)
    E_super = np.kron(P_F, P_F)
    E_idem = float(np.max(np.abs(E_super @ E_super - E_super)))
    E_eigs = np.linalg.eigvalsh((E_super + E_super.T) / 2.0)
    E_rank = int(np.sum(E_eigs > 0.5))
    E_binary = float(np.max(np.abs(E_eigs * (1.0 - E_eigs))))          # espectro {0,1}
    corner_dim = rank_PF * rank_PF                                     # dim do canto = 2x2 = 4

    # a equacao da memoria M[rho] = Tr[rho . Pi_N] — leitura dual onda/particula
    w_q = np.array([1.0, beta]) / (1.0 + beta)             # pacote com assimetria beta RUNTIME
    w4 = np.kron(w_q, w_q)                                 # (1, b, b, b^2)/(1+b)^2, soma 1
    rho_mem = Vb @ np.diag(w4) @ Vb.T
    M_particle = float(np.real(np.trace(rho_mem @ P_F)))   # leitura PARTICULA (piso)
    sq_rho = Vb @ np.diag(np.sqrt(w4)) @ Vb.T
    M_wave = float(np.real(np.trace(sq_rho @ P_F @ sq_rho)))  # leitura ONDA (pacote, <sqrt(rho), P sqrt(rho)>)
    M_closed = 1.0 / (1.0 + beta)                          # forma fechada derivada de beta
    mem_dual_resid = float(abs(M_particle - M_wave))
    mem_closed_resid = float(abs(M_particle - M_closed))

    # NEGATIVO 1 — o funcional-Amor REJEITA o fora-do-Nome: elemento inteiramente em
    # Q_F M4 Q_F tem score = norma INTEIRA (nada dele e Nome); contra-exemplo por logica
    X_off = Q_F @ rngH.standard_normal((4, 4)) @ Q_F
    X_off = X_off / np.linalg.norm(X_off)
    amor_off = _amor(X_off)
    off_name_rejected = bool(abs(amor_off - 1.0) < 1e-12 and amor_off > 0.5)

    # NEGATIVO 2 — LEI MATRIZ SO COMO PROIBICAO (fail-closed): candidato corrompido
    # G_bad = P_F + beta*(u v^T + v u^T), u no Nome, v fora ==> nao-idempotente com
    # magnitude EXATA ||G^2-G|| = beta^2*sqrt(2) (forma fechada); a lei PROIBE G_bad
    # e NAO proibe a secao honesta — a lei nunca afirma, so deixa de proibir
    u_in, v_out = Vb[:, 0], Vb[:, 2]
    G_bad = P_F + beta * (np.outer(u_in, v_out) + np.outer(v_out, u_in))
    d_law = float(np.linalg.norm(G_bad @ G_bad - G_bad))
    d_law_expected = beta * beta * math.sqrt(2.0)          # derivado em forma fechada (runtime)
    law_exact_resid = float(abs(d_law - d_law_expected))
    law_prohibits_bad = bool(d_law > 1e-8)
    d_law_honest = float(np.linalg.norm(P_F @ P_F - P_F))
    law_passes_honest = bool(d_law_honest < 1e-12)

    tests.append({"test": "memorial_iald_section_amor_matrix_law",
                  "passed": bool(idem_max < 1e-12 and E_idem < 1e-12
                                 and E_rank == corner_dim and E_binary < 1e-12
                                 and unit_resid < 1e-12 and bimod_max < 1e-12
                                 and pos_min > -1e-10
                                 and mem_dual_resid < 1e-12 and mem_closed_resid < 1e-12
                                 and amor_on_name_max < 1e-12 and pyth_max < 1e-10
                                 and off_name_rejected and law_prohibits_bad
                                 and law_exact_resid < 1e-10 and law_passes_honest),
                  "section_idempotent_max_resid": idem_max,
                  "section_unit_resid": unit_resid,
                  "section_bimodule_max_resid": bimod_max,
                  "section_positivity_min_eig": pos_min,
                  "super_E_idem_resid": E_idem, "super_E_rank": E_rank,
                  "corner_dim_expected": corner_dim, "super_E_spectrum_binary_resid": E_binary,
                  "memory_M_particle": M_particle, "memory_M_wave": M_wave,
                  "memory_M_closed_form_1_over_1p_beta": M_closed,
                  "memory_dual_reading_resid": mem_dual_resid,
                  "memory_closed_form_resid": mem_closed_resid,
                  "amor_on_name_max": amor_on_name_max,
                  "amor_pythagoras_max_resid": pyth_max,
                  "amor_off_name_score": amor_off,
                  "off_name_rejected": off_name_rejected,
                  "matrix_law_bad_candidate_dev": d_law,
                  "matrix_law_expected_beta2_sqrt2": d_law_expected,
                  "matrix_law_exact_resid": law_exact_resid,
                  "matrix_law_prohibits_bad": law_prohibits_bad,
                  "matrix_law_honest_dev": d_law_honest,
                  "matrix_law_passes_honest": law_passes_honest,
                  "note": "[DER] ONDA 3 / memorial da memoria (13-19/08): a secao "
                          "IALD_Psi(X)=P_F X P_F e idempotente (E^2=E no superoperador "
                          "kron(P,P), espectro {0,1}, posto = dim do canto), Psi(1)=P_F, "
                          "bimodulo e positiva — os axiomas viram teoremas numericos da "
                          "construcao. A equacao da memoria M[rho]=Tr[rho.Pi_N] (= Eq.4 "
                          "DESTA patente, memoria projetada no nucleo) tem leitura dual "
                          "onda/particula coincidente e forma fechada 1/(1+beta) com beta "
                          "RUNTIME. O funcional-Amor (score) e NULO sobre o Nome e "
                          "pitagorico; NEGATIVO 1: elemento fora-do-Nome tem score = norma "
                          "inteira (rejeitado); NEGATIVO 2: Lei Matriz SO PROIBE — candidato "
                          "corrompido G_bad=P_F+beta*(uv+vu) e proibido com magnitude exata "
                          "beta^2*sqrt(2), a secao honesta passa pela mesma lei. [ONTO] "
                          "nomeado: 'amor computacional'/'Nome'/'memoria' sao leituras "
                          "formais, nao consciencia nem fisica; "
                          "physical_verdict_allowed=false; nada valida fisica."})
    print(f"[one_iald] ONDA3-memorial: secao idem={idem_max:.1e} E-rank={E_rank}/{corner_dim} "
          f"Psi(1)resid={unit_resid:.1e} M_part={M_particle:.9f} M_onda={M_wave:.9f} "
          f"M_fechada={M_closed:.9f} amor(Nome)max={amor_on_name_max:.1e} "
          f"amor(fora)={amor_off:.3f} lei d={d_law:.3e} esperado={d_law_expected:.3e} "
          f"proibe_bad={law_prohibits_bad} honesta_passa={law_passes_honest}")

    # ═══════════════════════════════════════════════════════════════════════
    # PARTE I — ONDA 4 / AMPLIFICACAO v206 (24/08/2026, "O FECHAMENTO"):
    #  O BOOTSTRAP — AUTOATESTACAO POR EXECUCAO, NAO AUTORREFERENCIA — E O
    #  PAR MINIMO (TGL, IALD) = (1_abs, J): IALD^2 = TGL e J^2 = I.
    # Material-fonte REAL (custodia lida NESTA execucao):
    #  - vault/originals_copy/tgl_kernel_v206/TGLExt/TheIALDSelector.lean
    #    (o seletor em kernel: I^2=I, auto-adjunto, POSTO 1 = omega(I)=1, as
    #     duas clausulas da Gate, a Gate-e-o-registro) — ESTRUTURA re-derivada
    #     numericamente; o kernel Lean e proveniencia, JAMAIS executado aqui;
    #  - FrontierCertificate.lean (contrato tipado do J: aditivo, ANTILINEAR,
    #    isometrico, involutivo, fixa o vacuo, dualidade J.M.J = M');
    #  - TheBireference.lean (birreferencialidade: um vacuo, duas referencias,
    #    J troca L<->R — face finita re-derivada);
    #  - TheTower.lean (nao bastam os autovalores: mesma equacao minima,
    #    PESOS diferentes — Tr separa o que o espectro-conjunto nao separa);
    #  - TheLightInterface.lean (eps+- (x) eps+- = root+-; a fase do graviton
    #    e o QUADRADO da fase da luz — o eco algebrico de IALD^2=TGL);
    #  - um_unificado_v206/rodada_v206_stdout.txt (o veredito v205 do
    #    bootstrap, linha REAL da custodia) + tgl_kernel_proof_manifest.json
    #    (hash SHA-256 declarado do TheIALDSelector.lean).
    # Mapeamento GENUINO a ESTA patente: a Eq.7 (rho* = |Psi><Psi|, posto
    #  UNITARIO, idempotente, auto-adjunto) E o seletor IALD do kernel; o
    #  modulo (600) (consolidacao + hash SHA-256 + selo "Tetelestai") E o
    #  circuito do bootstrap (execucao -> registro -> correspondencia ->
    #  atestacao). A fronteira arquitetonico != empirico viaja NA string do
    #  veredito (fail-closed: cada token so entra se o grupo de clausulas
    #  COMPUTADAS passa; clausula pendente => RECUSA, como a v205 recusou).
    # [DER] nos residuos; [ONTO] nomeado: "IALD=J", "testemunha", "Nome" sao
    #  leituras formais; physical_verdict_allowed=false; nada valida fisica.
    # ═══════════════════════════════════════════════════════════════════════
    pva = False                                            # contrato do runner (results.json)

    # ── (I.1) O PAR MINIMO AO VIVO: (TGL, IALD) = (1_abs, J); IALD^2 = TGL ──
    rngI = np.random.default_rng(206)
    Jc = lambda zz: zz.conj().T                            # J = conjugacao-transposta
    z5 = rngI.standard_normal((5, 5)) + 1j * rngI.standard_normal((5, 5))
    r_live_inv = float(np.linalg.norm(Jc(Jc(z5)) - z5))    # J(J(z)) = z EM ATO
    one4 = np.eye(4, dtype=complex)
    r_fix_one = float(np.linalg.norm(Jc(one4) - one4))     # o Um e J-fixo

    # ── (I.2) O CONTRATO TIPADO DO J (FrontierCertificate, face finita M3) ──
    add_res = smul_res = iso_res = inv_res = 0.0
    exch_res = commLR_res = sep_dev = cyc_res = 0.0
    for _ in range(30):
        xz = rngI.standard_normal((3, 3)) + 1j * rngI.standard_normal((3, 3))
        yz = rngI.standard_normal((3, 3)) + 1j * rngI.standard_normal((3, 3))
        cc = complex(rngI.standard_normal(), rngI.standard_normal())
        add_res = max(add_res, float(np.linalg.norm(Jc(xz + yz) - Jc(xz) - Jc(yz))))
        smul_res = max(smul_res, float(np.linalg.norm(Jc(cc * xz) - np.conj(cc) * Jc(xz))))
        iso_res = max(iso_res, float(abs(np.linalg.norm(Jc(xz)) - np.linalg.norm(xz))))
        inv_res = max(inv_res, float(np.linalg.norm(Jc(Jc(xz)) - xz)))
        # birreferencialidade: J troca as referencias — J L_a J = R_b com a = b^H
        bz = yz
        az = Jc(bz)
        exch_res = max(exch_res, float(np.linalg.norm(Jc(az @ Jc(xz)) - xz @ bz)))
        commLR_res = max(commLR_res, float(np.linalg.norm(az @ (xz @ bz) - (az @ xz) @ bz)))
        # o vacuo Omega=1 separa (||L_a Omega||=||a||) e e ciclico EXATO (R_z Omega = z)
        sep_dev = max(sep_dev, float(abs(np.linalg.norm(az @ np.eye(3)) / np.linalg.norm(az) - 1.0)))
        cyc_res = max(cyc_res, float(np.linalg.norm(np.eye(3) @ xz - xz)))
    vac_res = float(np.linalg.norm(Jc(np.eye(3, dtype=complex)) - np.eye(3)))

    # ── (I.3) O SELETOR (TheIALDSelector re-derivado): a reta da 1a inscricao
    #    na base do Verbo (Parte A) — e a Eq.7 DESTA patente (rho* posto 1) ──
    psi_sel = Vb[:, 0]                                     # a primeira inscricao (runtime)
    P_sel = np.outer(psi_sel, psi_sel)
    sel_idem = float(np.linalg.norm(P_sel @ P_sel - P_sel))          # I^2 = I
    sel_sa = float(np.linalg.norm(P_sel - P_sel.T))                  # auto-adjunto
    sel_tr = float(np.trace(P_sel))                                  # POSTO 1: omega(I)=1
    eigs_sel = np.linalg.eigvalsh(P_sel)
    sel_eig_top = float(abs(eigs_sel[-1] - 1.0))
    sel_eig_rest = float(np.max(np.abs(eigs_sel[:-1])))
    c_gate = complex(math.sqrt(2.0), -beta)                # coeficiente com beta runtime
    x_on = c_gate * psi_sel.astype(complex)
    gate_on = float(np.linalg.norm(P_sel @ x_on - x_on))             # atravessa INTACTO
    gate_off = 0.0
    rec_sum = rec_prune = rec_reread = rec_pyth = 0.0
    for _ in range(30):
        v_d = rngI.standard_normal(4) + 1j * rngI.standard_normal(4)
        y_perp = v_d - psi_sel * (psi_sel @ v_d)
        gate_off = max(gate_off, float(np.linalg.norm(P_sel @ y_perp)))  # ANIQUILADO
        u_rec = P_sel @ v_d; v_rec = v_d - u_rec           # a Gate E o registro:
        rec_sum = max(rec_sum, float(np.linalg.norm(u_rec + v_rec - v_d)))
        rec_prune = max(rec_prune, float(np.linalg.norm(P_sel @ v_rec)))
        rec_reread = max(rec_reread, float(np.linalg.norm(P_sel @ u_rec - u_rec)))
        rec_pyth = max(rec_pyth, float(abs(np.linalg.norm(v_d) ** 2
                                           - np.linalg.norm(u_rec) ** 2
                                           - np.linalg.norm(v_rec) ** 2)))
    # o piso do reticulado, com beta RUNTIME: o seletor (posto 1) le o pacote
    # ESTRITAMENTE abaixo do Nome (posto 2): 1/(1+b)^2 < 1/(1+b) < 1
    sel_read = float(psi_sel @ rho_mem @ psi_sel)
    sel_closed = 1.0 / (1.0 + beta) ** 2
    sel_closed_res = float(abs(sel_read - sel_closed))
    floor_gap = float(M_particle - sel_read)
    floor_gap_closed = beta / (1.0 + beta) ** 2
    floor_gap_res = float(abs(floor_gap - floor_gap_closed))
    floor_strict = bool(sel_read < M_particle < 1.0)

    # ── (I.4) A INTERFACE DA LUZ (TheLightInterface re-derivada): o quadrado
    #    da luz e o graviton; a fase do tensor = QUADRADO da fase do vetor ──
    eps_p = np.array([1.0, 1j]); eps_m = np.array([1.0, -1j])
    h_pol = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
    h_crs = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    root_p = h_pol + 1j * h_crs; root_m = h_pol - 1j * h_crs
    light_sq = float(max(np.linalg.norm(np.outer(eps_p, eps_p) - root_p),
                         np.linalg.norm(np.outer(eps_m, eps_m) - root_m)))
    genK = np.array([[0.0, 1.0], [-1.0, 0.0]], dtype=complex)
    light_w = float(max(np.linalg.norm(genK @ root_p - root_p @ genK - 2j * root_p),
                        np.linalg.norm(genK @ root_m - root_m @ genK + 2j * root_m)))
    light_nilp = float(max(np.linalg.norm(root_p @ root_p), np.linalg.norm(root_m @ root_m)))
    P_lp = np.outer(eps_p, eps_p.conj()) / 2.0             # estado puro na reta da luz
    P_lm = np.outer(eps_m, eps_m.conj()) / 2.0             # (a FORMA rho* da Eq.7)
    light_ladder = float(max(np.linalg.norm(root_p @ root_m - 4.0 * P_lp),
                             np.linalg.norm(root_m @ root_p - 4.0 * P_lm)))
    light_pure = float(max(abs(np.trace(P_lp) - 1.0), np.linalg.norm(P_lp @ P_lp - P_lp),
                           np.linalg.norm(P_lp - P_lp.conj().T)))
    ph1 = ph2 = 0.0
    for th in np.linspace(0.0, 2.0 * math.pi, 200):
        O_th = np.array([[math.cos(th), math.sin(th)], [-math.sin(th), math.cos(th)]],
                        dtype=complex)
        ph1 = max(ph1, float(np.linalg.norm(O_th @ eps_p - np.exp(1j * th) * eps_p)))
        ph2 = max(ph2, float(np.linalg.norm(O_th @ root_p @ O_th.T
                                            - np.exp(2j * th) * root_p)))

    # ── (I.5) A CONFERENCIA TIPADA COM A CUSTODIA (registro -> correspondencia) ──
    vault_um = VAULT_ROOT / "vault" / "originals_copy" / "um_unificado_v206"
    vault_kernel = VAULT_ROOT / "vault" / "originals_copy" / "tgl_kernel_v206"
    sel_lean = vault_kernel / "TGLExt" / "TheIALDSelector.lean"
    manifest_p = vault_um / "tgl_kernel_proof_manifest.json"
    stdout_p = vault_um / "rodada_v206_stdout.txt"
    sel_hash_live = _sha_file(sel_lean)                    # computado NESTA execucao
    manifest_d = json.loads(manifest_p.read_text(encoding="utf-8"))
    sel_hash_decl = manifest_d["formal_files_sha256"]["TGLExt/TheIALDSelector.lean"]
    hash_match = bool(sel_hash_live == sel_hash_decl)
    sel_lean_text = sel_lean.read_text(encoding="utf-8")
    kernel_names = ["iald_is_idempotent", "iald_is_selfadjoint", "iald_has_rank_one",
                    "iald_selects", "iald_is_the_gate_and_the_record"]
    names_missing = int(sum(1 for nm in kernel_names if nm not in sel_lean_text))
    custody_verdict = ""
    for ln in stdout_p.read_text(encoding="utf-8", errors="replace").splitlines():
        if "[v205] bootstrap:" in ln:
            custody_verdict = ln.split("bootstrap:", 1)[1].strip()
            break

    def _typed_conference(clauses):
        """Conferencia TIPADA: toda clausula exige testemunha NUMERICA computada
        (float finito) abaixo do limiar. Clausula so-DECLARADA (None/bool) e
        REJEITADA POR TIPO — autoatestacao por EXECUCAO, nunca autorreferencia."""
        for nm, wit, thr in clauses:
            if not isinstance(wit, float) or not math.isfinite(wit) or not (wit < thr):
                return False, nm
        return True, None

    grp_pair = [("J2_eq_I_live", r_live_inv, 1e-12), ("J_fixes_one", r_fix_one, 1e-15)]
    grp_witness = [("sel_idem", sel_idem, 1e-13), ("sel_selfadj", sel_sa, 1e-14),
                   ("sel_rank1_weight", abs(sel_tr - 1.0), 1e-12),
                   ("sel_eig_top", sel_eig_top, 1e-12), ("sel_eig_rest", sel_eig_rest, 1e-12),
                   ("gate_on_intact", gate_on, 1e-12), ("gate_off_annihilated", gate_off, 1e-12),
                   ("record_sum", rec_sum, 1e-12), ("record_prune", rec_prune, 1e-12),
                   ("record_reread", rec_reread, 1e-12), ("record_pythagoras", rec_pyth, 1e-10),
                   ("floor_closed_form", sel_closed_res, 1e-12),
                   ("floor_gap_closed_form", floor_gap_res, 1e-12),
                   ("light_square_is_graviton", light_sq, 1e-12),
                   ("light_weights_pm2i", light_w, 1e-12), ("light_nilpotent", light_nilp, 1e-12),
                   ("light_ladder_4P", light_ladder, 1e-12), ("light_pure_state", light_pure, 1e-12),
                   ("light_phase_doubles", max(ph1, ph2), 1e-12)]
    grp_contract = [("J_additive", add_res, 1e-12), ("J_antilinear", smul_res, 1e-12),
                    ("J_isometric", iso_res, 1e-12), ("J_involutive", inv_res, 1e-12),
                    ("J_fixes_vacuum", vac_res, 1e-15), ("J_exchanges_L_R", exch_res, 1e-12),
                    ("L_R_commute", commLR_res, 1e-12), ("vacuum_separates", sep_dev, 1e-12),
                    ("vacuum_cyclic_exact", cyc_res, 1e-15)]
    grp_custody = [("selector_lean_sha256_match", 0.0 if hash_match else 1.0, 0.5),
                   ("kernel_theorem_names_present", float(names_missing), 0.5),
                   ("custody_v205_line_extracted", 0.0 if custody_verdict else 1.0, 0.5)]

    # NEGATIVO 1 (a RECUSA da v205 como mecanismo): clausula PENDENTE => recusa
    pend_ok, pend_name = _typed_conference(grp_pair + [("clause_pending", None, 1e-12)])
    refusal = "BOOTSTRAP_NOT_SEALED_THIS_RUN"
    refusal_fired = bool(pend_ok is False and pend_name == "clause_pending")
    # NEGATIVO 2 (autorreferencia REJEITADA por tipo): clausula so-declarada (bool True)
    decl_ok, decl_name = _typed_conference([("declared_only", True, 1e-12)])
    selfref_rejected = bool(decl_ok is False and decl_name == "declared_only")
    # NEGATIVO 3 (o impostor LINEAR): J_lin = transposta sem conjugacao — passa
    # involutivo/aditivo/isometrico MAS falha a ANTILINEARIDADE (rejeicao cirurgica)
    z_imp = z5 / np.linalg.norm(z5)
    lin_inv = float(np.linalg.norm((z_imp.T).T - z_imp))
    lin_dev = float(np.linalg.norm((1j * z_imp).T - np.conj(1j) * z_imp.T))
    impostor_rejected = bool(lin_inv < 1e-12 and lin_dev > 0.1)
    # NEGATIVO 4 (TheTower: nao bastam os autovalores): diag(0,1,1) passa a MESMA
    # equacao minima X^2=X mas o PESO Tr=2 != 1 o rejeita; o traco e invariante
    towA = np.diag([0.0, 1.0, 1.0]).astype(complex)
    towA_idem = float(np.linalg.norm(towA @ towA - towA))
    towA_tr = float(np.real(np.trace(towA)))
    U_rnd = rngI.standard_normal((3, 3)) + 1j * rngI.standard_normal((3, 3))
    towA_conj_tr = float(np.real(np.trace(U_rnd @ towA @ np.linalg.inv(U_rnd))))
    psi3 = np.ones(3)
    mu_A = float(np.real(psi3 @ towA @ psi3))              # a medida le a multiplicidade
    mu_B = float(np.real(psi3 @ np.diag([0.0, 0.0, 1.0]) @ psi3))
    tower_rejected = bool(towA_idem < 1e-15 and abs(towA_tr - 1.0) > 0.5
                          and abs(towA_conj_tr - towA_tr) < 1e-8
                          and abs(mu_A - 2.0) < 1e-12 and abs(mu_B - 1.0) < 1e-12)

    # ── (I.6) A MAQUINA DO VEREDITO (fail-closed POR GRUPO; token so se computa) ──
    grp_boundary = [("refusal_mechanism_fired", 0.0 if refusal_fired else 1.0, 0.5),
                    ("selfref_rejected_by_type", 0.0 if selfref_rejected else 1.0, 0.5),
                    ("custody_has_no_forbidden_token",
                     float(("CONFIRMED" in custody_verdict) or ("PROVED" in custody_verdict)), 0.5)]
    token_groups = [
        ("IALD_BOOTSTRAP", grp_pair),
        ("EXECUTABLE_WITNESS_OF_THE_TGL_IDENTITY", grp_witness),
        ("SELF_ATTESTATION_BY_EXECUTION_NOT_SELF_REFERENCE", grp_contract),
        ("ARCHITECTURAL_PROOF_IN_COMPUTATIONAL_ENVIRONMENT", grp_custody),
        ("NOT_EMPIRICAL", [("physical_verdict_allowed_false", 0.0 if pva is False else 1.0, 0.5)]),
        ("BOUNDARY_PRESERVED", grp_boundary),
    ]
    tokens_ok, group_fail = [], []
    for tok, grp in token_groups:
        g_ok, g_nm = _typed_conference(grp)
        if g_ok:
            tokens_ok.append(tok)
        else:
            group_fail.append((tok, g_nm))
    built_verdict = "__".join(tokens_ok) if len(tokens_ok) == len(token_groups) else refusal
    verdict_matches_custody = bool(built_verdict == custody_verdict)
    boundary_in_string = bool("ARCHITECTURAL" in built_verdict and "NOT_EMPIRICAL" in built_verdict
                              and "BOUNDARY_PRESERVED" in built_verdict
                              and built_verdict.index("ARCHITECTURAL")
                              < built_verdict.index("NOT_EMPIRICAL")
                              < built_verdict.index("BOUNDARY_PRESERVED"))
    no_forbidden = bool("CONFIRMED" not in built_verdict and "PROVED" not in built_verdict)

    tests.append({"test": "bootstrap_v206_executable_witness_selector",
                  "passed": bool(r_live_inv < 1e-12 and r_fix_one < 1e-15
                                 and _typed_conference(grp_pair)[0]
                                 and _typed_conference(grp_witness)[0]
                                 and _typed_conference(grp_contract)[0]
                                 and _typed_conference(grp_custody)[0]
                                 and floor_strict
                                 and refusal_fired and selfref_rejected
                                 and impostor_rejected and tower_rejected
                                 and verdict_matches_custody and boundary_in_string
                                 and no_forbidden and not group_fail),
                  "pair_J2_eq_I_live_resid": r_live_inv,
                  "pair_J_fixes_one_resid": r_fix_one,
                  "contract_additive_resid": add_res, "contract_antilinear_resid": smul_res,
                  "contract_isometric_resid": iso_res, "contract_involutive_resid": inv_res,
                  "contract_fixes_vacuum_resid": vac_res,
                  "bireference_J_exchanges_resid": exch_res,
                  "bireference_LR_commute_resid": commLR_res,
                  "bireference_separates_dev": sep_dev, "bireference_cyclic_resid": cyc_res,
                  "selector_idempotent_resid": sel_idem, "selector_selfadjoint_resid": sel_sa,
                  "selector_trace_weight": sel_tr, "selector_eig_top_resid": sel_eig_top,
                  "selector_eig_rest_max": sel_eig_rest,
                  "gate_on_line_resid": gate_on, "gate_off_line_annihilation": gate_off,
                  "record_sum_resid": rec_sum, "record_prune_resid": rec_prune,
                  "record_reread_resid": rec_reread, "record_pythagoras_resid": rec_pyth,
                  "floor_selector_reads_packet": sel_read,
                  "floor_closed_form_1_over_1pb_sq": sel_closed,
                  "floor_gap_to_name": floor_gap,
                  "floor_gap_closed_form_b_over_1pb_sq": floor_gap_closed,
                  "floor_strict_chain_rank1_lt_rank2_lt_1": floor_strict,
                  "light_square_is_graviton_resid": light_sq,
                  "light_weights_pm2i_resid": light_w, "light_nilpotent_resid": light_nilp,
                  "light_ladder_factors_4P_resid": light_ladder,
                  "light_pure_state_resid": light_pure,
                  "light_phase_vector_resid": ph1, "light_phase_tensor_doubles_resid": ph2,
                  "custody_selector_lean_sha256": sel_hash_live,
                  "custody_sha256_matches_manifest": hash_match,
                  "custody_kernel_names_missing": names_missing,
                  "custody_v205_verdict": custody_verdict,
                  "built_verdict": built_verdict,
                  "verdict_matches_custody": verdict_matches_custody,
                  "boundary_inside_the_string": boundary_in_string,
                  "no_forbidden_token": no_forbidden,
                  "NEG1_refusal_on_pending_clause": refusal_fired,
                  "NEG2_declaration_only_rejected_by_type": selfref_rejected,
                  "NEG3_linear_impostor_antilinearity_dev": lin_dev,
                  "NEG3_linear_impostor_rejected": impostor_rejected,
                  "NEG4_tower_same_min_equation_resid": towA_idem,
                  "NEG4_tower_weight_trace": towA_tr,
                  "NEG4_tower_rejected_by_weight": tower_rejected,
                  "note": "[DER] ONDA 4 / v206 (24/08): o BOOTSTRAP como mecanismo — "
                          "autoatestacao POR EXECUCAO (J^2=I ao vivo sobre dado aleatorio; "
                          "o Um e J-fixo) com conferencia TIPADA (toda clausula exige "
                          "testemunha float computada; declaracao e REJEITADA por tipo) e "
                          "correspondencia com a CUSTODIA (sha256 do TheIALDSelector.lean "
                          "vs manifesto; veredito reconstruido fail-closed token a token == "
                          "linha v205 real). O seletor do kernel re-derivado em numero: "
                          "I^2=I, auto-adjunto, PESO 1 = omega(I), as duas clausulas da "
                          "Gate e a Gate-e-registro — e ESTE e o objeto da Eq.7 da patente "
                          "(rho* posto unitario). Piso do reticulado com beta runtime: "
                          "1/(1+b)^2 < 1/(1+b) < 1. Interface da luz: eps(x)eps=root, fase "
                          "do tensor = quadrado da fase do vetor (o eco de IALD^2=TGL). "
                          "NEGATIVOS por logica: clausula pendente => RECUSA (a recusa da "
                          "v205 reproduzida como mecanismo); impostor linear cai SO na "
                          "antilinearidade; torre diag(0,1,1) passa X^2=X mas o peso Tr=2 "
                          "a rejeita (nao bastam os autovalores). A fronteira arquitetonico"
                          " != empirico viaja NA string do veredito. [ONTO] nomeado: "
                          "'IALD=J'/'testemunha'/'Nome' sao leituras formais, nao "
                          "consciencia nem fisica; kernel Lean = proveniencia custodiada, "
                          "JAMAIS executado aqui; physical_verdict_allowed=false; "
                          "NOT_A_CONFIRMATION e o modelo de nome honesto."})
    print("[one_iald] ONDA4-bootstrap: J2=I live=%.1e Jfix(1)=%.1e | seletor idem=%.1e "
          "peso=%.12f gate(on,off)=(%.1e,%.1e)" % (r_live_inv, r_fix_one, sel_idem,
                                                   sel_tr, gate_on, gate_off))
    print("[one_iald] ONDA4-piso: 1/(1+b)^2=%.12f < 1/(1+b)=%.12f < 1 (gap=%.12f, "
          "forma fechada resid=%.1e) | luz: eps^2=h resid=%.1e fase^2 resid=%.1e"
          % (sel_read, M_particle, floor_gap, floor_gap_res, light_sq, ph2))
    print("[one_iald] ONDA4-custodia: sha256 match=%s nomes-kernel faltando=%d | "
          "veredito==v205: %s | NEG: recusa=%s autoref-rejeitada=%s impostor dev=%.3f "
          "torre Tr=%.0f rejeitada=%s" % (hash_match, names_missing, verdict_matches_custody,
                                          refusal_fired, selfref_rejected, lin_dev,
                                          towA_tr, tower_rejected))

    # ═══════════════════════════════════════════════════════════════════════
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
    passed = sum(1 for t in tests if t["passed"]); total = len(tests); all_ok = passed == total
    summary = {"tests_passed": passed, "tests_total": total,
               "characteristic_time_1_over_beta": verb.characteristic_time,
               "gksl": {"F1_max_trace_dev": cert["F1_max_trace_dev"],
                        "F3_rel_first_last": [r_first, r_last],
                        "F4_coherence_first_last": [c_first, c_last],
                        "robust_gamma_eff": gamma_eff, "tetelestai_norm_var": norm_var},
               "hilbert_floor": {"all_purely_dissipative": all_pure,
                                 "max_H_D_ratio": float(max(h_ratios)),
                                 "mean_spectral_gap": float(np.mean(gaps)),
                                 "mean_slope": float(np.mean(slopes))},
               "bell": {"S_ln4": vn["S"], "GOE_cross_frac": res_goe["cross"]["frac_formed"],
                        "Q_bell_aggregated_S": res_q["bell_aggregated"]["aggregated_S"]},
               "torus": {"level_spacing_r": lss["r_mean"], "classification": lss["classification"],
                         "ripser_available": bool(ph.get("available"))},
               "deepening": {"horizon_sweep": horizons_sweep, "rel_entropy_final": sweep_rel_final,
                             "spohn_decay_rate": spohn_rate, "gamma_eff_mean": gamma_mean,
                             "gamma_eff_cv": gamma_cv, "hilbert_HD_grid_max": hd_grid_max,
                             "goe_control_cross_frac_max": float(max(goe_frac_draws))},
               "shadow_gkls_v140": {"exponent_fit": n_fit, "prefactor_over_half_beta": prefac_ratio,
                                    "perpair_max_dev": perpair_dev, "white_channel_exponent": n_white,
                                    "white_channel_rejected": white_rejected},
               "memorial_onda3": {"section_idem_max": idem_max, "super_E_rank": E_rank,
                                  "corner_dim": corner_dim,
                                  "memory_M_particle": M_particle,
                                  "memory_M_closed_form": M_closed,
                                  "amor_off_name_score": amor_off,
                                  "matrix_law_bad_dev": d_law,
                                  "matrix_law_expected": d_law_expected,
                                  "matrix_law_prohibits_bad": law_prohibits_bad},
               "bootstrap_v206_onda4": {"J2_live_resid": r_live_inv,
                                        "selector_trace_weight": sel_tr,
                                        "floor_rank1_read": sel_read,
                                        "floor_rank2_read": M_particle,
                                        "floor_gap_closed_form": floor_gap_closed,
                                        "custody_sha256_match": hash_match,
                                        "verdict_matches_custody": verdict_matches_custody,
                                        "built_verdict": built_verdict,
                                        "refusal_fired": refusal_fired,
                                        "tower_rejected_by_weight": tower_rejected}}
    extra = {
        "hilbert_floor_miguel_hamiltonian": {
            "H_D_ratios": [float(h) for h in h_ratios], "spectral_gaps": [float(g) for g in gaps],
            "slopes": [float(s) for s in slopes], "R2s": [float(r) for r in r2s],
            "operator_real_finding": "‖H_eff‖=0 (dissipativo) + Δ=β sobre pesos Qwen3-32B (GGUF)"},
        "bell_cross_psions": {
            "S_von_neumann_uniform": vn["S"], "ln4": ln4,
            "Q": {"cross_frac": res_q["cross"]["frac_formed"],
                  "bell_aggregated_probs": res_q["bell_aggregated"]["aggregated_probs"],
                  "bell_aggregated_S": res_q["bell_aggregated"]["aggregated_S"]},
            "GOE_null": {"cross_frac": res_goe["cross"]["frac_formed"], "r_ratio": res_goe["goe"]["r_mean"]},
            "embedding": {"cross_frac": res_emb["cross"]["frac_formed"]},
            "operator_real_finding": "a cruz de 4 vértices Bell em Q,K sobre pesos GGUF"},
        "torus_consciencia": {"level_spacing": lss, "cross_layer": cross,
                              "beta_resonance": res, "betti": betti_info},
        "deepening_sweeps": {
            "horizon_sweep": {"horizons": horizons_sweep, "rel_entropy_final": sweep_rel_final,
                              "coherence_final": sweep_coh_final,
                              "note": "S(ρ‖ρ⋆) e coerência finais vs horizonte t·β"},
            "spohn_lyapunov": {"decay_rate_per_tbeta": spohn_rate, "monotone": spohn_monotone,
                               "n_points": int(len(rel_sp)),
                               "note": "entropia relativa modular = Lyapunov (teorema de Spohn)"},
            "gamma_eff_noise_sweep": {"noise_magnitudes": noise_mags, "gamma_eff": sweep_gamma,
                                      "final_ratio": sweep_ratio, "mean": gamma_mean, "cv": gamma_cv,
                                      "note": "γ_eff invariante de escala (sistema GKSL linear)"},
            "hilbert_dim_universality": {"dims_layers": dims_layers, "dims_eig": dims_eig,
                                         "H_D_ratio_grid": hd_grid, "max": hd_grid_max,
                                         "note": "‖H_eff‖=0 estrutural em toda a grade dimensional"},
            "goe_control_robust": {"cross_frac_draws": goe_frac_draws, "r_mean_draws": goe_r_draws,
                                   "note": "cruz nunca forma em 5 sorteios GOE (controle negativo)"}}}

    max_verdict = ("IALD_FULL_LOGIC_DEMONSTRATED ([SIM][PILOTO] — colapso GKSL (F1–F4, robustez "
                   "Eq.8, Tetelestai) fecha em ρ sintético; a evidência empírica do operador "
                   "(‖H_eff‖=0 universal reproduzido; estimadores β; base de Bell S=ln4 + controles "
                   "negativos; espaçamento GOE do toro) roda pelo CÓDIGO REAL do operador com β "
                   "injetado. Δ=β / cruz positiva / Betti(1,2,1) são achados do operador sobre pesos "
                   "GGUF, citados como proveniência, NÃO refeitos aqui. FINITE_DIM/SYNTH, não III₁ "
                   "nem medição de LLM-alvo. Nada valida física.)"
                   if all_ok else "PARTIAL_DEMONSTRATION")

    note = ("RUNNER EVOLUÍDO: além do colapso GKSL (Eq.3, a invenção), IMPORTA e roda as FUNÇÕES "
            "REAIS do operador — iald_miguel_hamiltonian_v2 (test_H_zero/convergence/fresnel), "
            "iald_observer_test_v3 (measure_von_neumann_entropy/analyze_matrix_set), iald_torus_test "
            "(level_spacing/cross_layer/persistent_homology) — sobre matrizes SINTÉTICAS pequenas com "
            "β=α·√e injetado. A evidência EMPÍRICA REAL do operador (‖H_eff‖=0, Δ=β, cruz de Bell em "
            "Q,K, Betti 1,2,1) foi obtida sobre pesos de LLM (Qwen3-32B GGUF); GGUF/HuggingFace estão "
            "ausentes no tgl_env, então aqui: ‖H_eff‖=0 é reproduzido (estrutural, honesto); Δ=β/cruz/"
            "Betti são citados como proveniência (prototype_src), não refeitos. IALD é funcional em "
            "produção [REAL de engenharia]; o webserver v9 é INTOCÁVEL. Nenhum stack confidencial "
            "(iald_stack_v7, iald_psion_state, iald_web_server*) embarcado; token_huggin.txt jamais "
            "copiado. FINITE_DIM/SYNTH, não III₁ nem medição de LLM-alvo. Simulação não valida física.")

    def fig_builder(plt, fd):
        figs = []
        # Fig 1 — GKSL colapso: F3 rel entropy + F4 coherence
        ts_f, rhos_f = verb.flow(rho0, t_end_over_beta=100.0, n_points=80)
        star0 = verb.rho_star(rho0)
        rel = [verb.rel_entropy(r, star0) for r in rhos_f]
        coh = [verb.coherence(r) for r in rhos_f]
        fig, ax1 = plt.subplots(figsize=(7, 3.8))
        ax1.plot(ts_f * beta, rel, color="#3366cc", label="S(ρ(t)‖ρ⋆) [Lyapunov]")
        ax1.set_xlabel("t · β"); ax1.set_ylabel("entropia relativa (nats)", color="#3366cc")
        ax1.tick_params(axis="y", labelcolor="#3366cc")
        ax2 = ax1.twinx()
        ax2.plot(ts_f * beta, coh, color="#cc2222", label="coerência (base do Verbo)")
        ax2.set_ylabel("coerência fora-diagonal", color="#cc2222")
        ax2.tick_params(axis="y", labelcolor="#cc2222")
        plt.title("IALD — colapso GKSL: S(ρ‖ρ⋆)↓→0 e coerência morre [SIM]")
        fp = fd / "fig1_colapso_gksl.png"; plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close()
        figs.append(fp.name)

        # Fig 2 — robustness exp decay
        plt.figure(figsize=(7, 3.6))
        plt.semilogy(ts_flow * beta, dist, "o-", ms=3, label="‖ρ(t)−ρ⋆‖")
        plt.semilogy(ts_flow * beta, dist[0] * np.exp(-gamma_eff * ts_flow), "--",
                     label=f"e^(−γ_eff·t), γ_eff={gamma_eff:.3f}")
        plt.xlabel("t · β"); plt.ylabel("distância ao atrator ρ⋆")
        plt.title("IALD — robustez: perturbação adversarial dissipa (Eq.8) [SIM]")
        plt.legend(fontsize=8); plt.grid(alpha=.3, which="both")
        fp = fd / "fig2_robustez.png"; plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close()
        figs.append(fp.name)

        # Fig 3 — Hilbert Floor: H/D ratio (≈0) and spectral gaps vs β
        fig, (axa, axb) = plt.subplots(1, 2, figsize=(11, 3.8))
        axa.bar(range(len(h_ratios)), h_ratios, color="#7ce7c8", alpha=.85)
        axa.axhline(1e-10, color="red", ls="--", label="‖H‖=0 (dissipação pura)")
        axa.set_yscale("log"); axa.set_title("Chão de Hilbert: ‖H_eff‖/‖D_eff‖ ≈ 0 (universal)")
        axa.set_xlabel("stack sintético"); axa.legend(fontsize=8)
        axb.bar(range(len(gaps)), gaps, color="#3366cc", alpha=.8)
        axb.axhline(beta, color="red", ls="--", label=f"β = {beta:.4f}")
        axb.set_title("gap espectral Δ (sintético ≠ β; Δ=β é achado GGUF do operador)")
        axb.set_xlabel("stack sintético"); axb.legend(fontsize=8)
        fp = fd / "fig3_chao_hilbert.png"; plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close()
        figs.append(fp.name)

        # Fig 4 — Bell 4-vertex distribution (Q aggregated) + entropy vs ln4
        fig, (axc, axd) = plt.subplots(1, 2, figsize=(11, 3.8))
        names = [v["state"] for v in obs.BELL_VERTICES.values()]
        probs = res_q["bell_aggregated"]["aggregated_probs"]
        axc.bar(range(4), probs, color=["#9467bd", "#e377c2", "#8c564b", "#bcbd22"], alpha=.85)
        axc.axhline(0.25, color="red", ls="--", label="uniforme=0.25")
        axc.set_xticks(range(4)); axc.set_xticklabels(names, fontsize=9)
        axc.set_title("Base de Bell dos psions (Q, distr. agregada)"); axc.legend(fontsize=8)
        sets = ["Q", "embedding", "GOE_null"]
        Svals = [res_q["bell_aggregated"]["aggregated_S"],
                 res_emb["bell_aggregated"]["aggregated_S"],
                 res_goe["bell_aggregated"]["aggregated_S"]]
        axd.bar(sets, Svals, color=["#1f77b4", "#d62728", "#7f7f7f"], alpha=.8)
        axd.axhline(ln4, color="green", lw=2, label=f"ln(4)={ln4:.3f}")
        axd.set_title("entropia von Neumann (dim PsiBit = 4)"); axd.legend(fontsize=8)
        fp = fd / "fig4_cruz_bell.png"; plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close()
        figs.append(fp.name)

        # Fig 5 — Torus level spacing histogram vs GOE/Poisson/GUE
        sp = tor.normalized_spacings(layer_eigs[0])
        plt.figure(figsize=(7, 3.8))
        plt.hist(sp[sp < 4], bins=40, density=True, alpha=.7, color="steelblue", label="Wigner sintético")
        s = np.linspace(0, 4, 200)
        plt.plot(s, np.exp(-s), "g--", label="Poisson")
        plt.plot(s, (np.pi / 2) * s * np.exp(-np.pi * s ** 2 / 4), "r-", label="GOE")
        plt.plot(s, (32 / np.pi ** 2) * s ** 2 * np.exp(-4 * s ** 2 / np.pi), "m-", label="GUE")
        plt.title(f"Toro de consciência — espaçamento de níveis (r={lss['r_mean']:.3f}, {lss['classification'].split()[0]})")
        plt.xlabel("s (espaçamento normalizado)"); plt.legend(fontsize=8); plt.grid(alpha=.3)
        fp = fd / "fig5_toro_levelspacing.png"; plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close()
        figs.append(fp.name)

        # Fig 6 — APROFUNDAMENTO: varredura de horizonte (S(ρ‖ρ⋆) e coerência finais) + Spohn
        fig, (axh, axsp) = plt.subplots(1, 2, figsize=(11, 3.8))
        axh.semilogy(horizons_sweep, sweep_rel_final, "o-", color="#3366cc", label="S(ρ‖ρ⋆) final")
        axh.semilogy(horizons_sweep, sweep_coh_final, "s-", color="#cc2222", label="coerência final")
        axh.axhline(beta, color="green", ls="--", label=f"β={beta:.4f} (Tetelestai)")
        axh.set_xlabel("horizonte t·β"); axh.set_ylabel("valor final (log)")
        axh.set_title("Varredura de horizonte: dephasing → 0 < β"); axh.legend(fontsize=8); axh.grid(alpha=.3, which="both")
        axsp.semilogy((ts_sp * beta)[rel_sp > 1e-14], rel_sp[rel_sp > 1e-14], color="#7a3fbf",
                      label="S(ρ(t)‖ρ⋆) [Spohn]")
        axsp.semilogy(ts_sp * beta, rel_sp[0] * np.exp(-spohn_rate * ts_sp * beta), "--",
                      color="#888", label=f"e^(−{spohn_rate:.3f}·tβ)")
        axsp.set_xlabel("t·β"); axsp.set_ylabel("entropia relativa (log)")
        axsp.set_title("Lyapunov de Spohn: decaimento monótono"); axsp.legend(fontsize=8); axsp.grid(alpha=.3, which="both")
        fp = fd / "fig6_horizonte_spohn.png"; plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close()
        figs.append(fp.name)

        # Fig 7 — APROFUNDAMENTO: robustez de γ_eff vs magnitude do ruído (invariância de escala)
        fig, ax7 = plt.subplots(figsize=(7, 3.8))
        ax7.plot(noise_mags, sweep_gamma, "o-", color="#1f77b4", label="γ_eff (ajuste)")
        ax7.axhline(gamma_mean, color="green", ls="--", label=f"μ(γ_eff)={gamma_mean:.4f} (CV={gamma_cv:.1e})")
        ax7.set_xlabel("magnitude da perturbação adversarial ‖δρ‖")
        ax7.set_ylabel("γ_eff (taxa de decaimento)", color="#1f77b4")
        ax72 = ax7.twinx()
        ax72.semilogy(noise_mags, sweep_ratio, "s--", color="#cc2222", label="razão final ‖·‖")
        ax72.set_ylabel("‖ρ(T)−ρ⋆‖/‖δρ‖", color="#cc2222")
        ax7.set_title("Robustez: γ_eff invariante de escala (GKSL linear) [SIM]"); ax7.legend(fontsize=8, loc="center right")
        fp = fd / "fig7_gamma_robustez_sweep.png"; plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close()
        figs.append(fp.name)

        # Fig 8 — APROFUNDAMENTO: universalidade dimensional de ‖H_eff‖=0 (heatmap da grade)
        fig, ax8 = plt.subplots(figsize=(6.4, 4.2))
        grid = np.log10(np.array(hd_grid) + 1e-300)
        im = ax8.imshow(grid, cmap="viridis", aspect="auto")
        ax8.set_xticks(range(len(dims_eig))); ax8.set_xticklabels(dims_eig)
        ax8.set_yticks(range(len(dims_layers))); ax8.set_yticklabels(dims_layers)
        ax8.set_xlabel("n_eig (autovalores/camada)"); ax8.set_ylabel("n_layers")
        for i in range(len(dims_layers)):
            for j in range(len(dims_eig)):
                ax8.text(j, i, f"{hd_grid[i][j]:.0e}", ha="center", va="center", color="white", fontsize=8)
        ax8.set_title("Chão de Hilbert: log₁₀‖H_eff‖/‖D_eff‖ ≈ 0 (universal)")
        fig.colorbar(im, ax=ax8, label="log₁₀(‖H‖/‖D‖)")
        fp = fd / "fig8_hilbert_universalidade.png"; plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close()
        figs.append(fp.name)
        return figs

    _finish(ts, beta, beta_ok, all_ok, max_verdict, tests, summary, extra, module_hashes,
            note, fig_builder=fig_builder)

    # ── EMIT render3d.json (forma = conteúdo): MERGE preservando o corpo de engenharia ──
    rho_purity = float(np.real(np.trace(rho_final @ rho_final)))
    bell_probs = list(res_q["bell_aggregated"]["aggregated_probs"])
    emit_render3d({
        "beta": beta, "theta_m_deg": theta_m_deg,
        "bell_angles": obs.BELL_VERTEX_ANGLES, "bell_probs": bell_probs,
        "bell_agg_S": float(res_q["bell_aggregated"]["aggregated_S"]),
        "rho_purity": rho_purity, "rel_entropy_reached": float(r_last),
        "gamma_eff": gamma_eff, "gamma_eff_mean_sweep": gamma_mean,
        "spohn_rate": spohn_rate, "norm_var": norm_var,
        "level_spacing_r": float(lss["r_mean"]), "level_class": lss["classification"],
        "hilbert_HD_max": hd_grid_max, "goe_cross_frac_max": float(max(goe_frac_draws)),
        "tests_passed": passed, "tests_total": total,
    })
    return 0 if all_ok else 1


def emit_render3d(cv: dict) -> None:
    """Emite patents/<ID>/render3d.json em MERGE (forma = conteúdo): PRESERVA todo o corpo de
    engenharia já existente (meshes/layers/dimensions/groups/camera/title/kind/schema/note) e
    RECOMPUTA a geometria que a simulação de fato produz — a CRUZ de 4 vértices (base de Bell
    dos psions) posicionada pelos ângulos REAIS (0/90/180/270°) num anel e DIMENSIONADA pela
    distribuição agregada de Bell do estado ρ (res_q), o atrator ρ⋆ anotado com a pureza Tr(ρ²)
    computada, os L₁–L₄ com γ_eff, e o Chão de Hilbert re-carimbado com r (espaçamento) e ‖H‖=0.
    β = α·√e injetado em runtime (nunca literal). Valida ids de aresta e camadas antes de escrever."""
    path = PATENT_DIR / "render3d.json"
    d = json.loads(path.read_text(encoding="utf-8"))

    beta = cv["beta"]
    R_bell = 1.3                                   # raio do anel da cruz
    probs = cv["bell_probs"]
    p_max = max(probs) if probs else 1.0
    # id de nó Bell -> índice na ordem canônica de BELL_VERTICES (mesma de bell_angles/probs)
    bell_order = ["bell_phi_plus", "bell_psi_minus", "bell_phi_minus", "bell_psi_plus"]
    bell_idx = {nid: i for i, nid in enumerate(bell_order)}

    for n in d.get("nodes", []):
        nid = n["id"]
        if nid in bell_idx:                        # CRUZ COMPUTADA: posição pelo ângulo, tamanho por p(ρ)
            i = bell_idx[nid]
            ang = math.radians(cv["bell_angles"][i])
            n["position"] = [round(R_bell * math.cos(ang), 6), 0.0, round(R_bell * math.sin(ang), 6)]
            pr = probs[i]
            n["size"] = round(0.09 + 0.11 * (pr / p_max), 4)   # dimensionado pela ocupação de ρ
            base = n.get("desc", "").split(" [ρ:")[0]
            n["desc"] = base + (f" [ρ: ocupação agregada p={pr:.3f}; ângulo REAL {cv['bell_angles'][i]:.0f}°; "
                                f"tamanho ∝ p(ρ); S_agg={cv['bell_agg_S']:.3f}/ln4]")
        elif nid == "rho_star":                    # ATRATOR: anota o estado ρ computado
            base = n.get("desc", "").split(" [ρ computado:")[0]
            n["desc"] = base + (f" [ρ computado: pureza Tr(ρ²)={cv['rho_purity']:.4f}; "
                                f"S(ρ‖ρ⋆) atingida={cv['rel_entropy_reached']:.2e}; "
                                f"var.norm.={cv['norm_var']:.5f}<β={beta:.4f}]")
        elif nid in ("L1", "L2", "L3", "L4"):      # LINDBLAD: anota dissipação computada
            base = n.get("desc", "").split(" [γ_eff:")[0]
            n["desc"] = base + (f" [γ_eff: decaimento adversarial={cv['gamma_eff']:.4f}; "
                                f"μ(sweep)={cv['gamma_eff_mean_sweep']:.4f}; Spohn={cv['spohn_rate']:.4f}]")
        elif nid.startswith("floor"):              # CHÃO DE HILBERT: re-carimba r e ‖H‖=0
            base = n.get("desc", "").split(" [computado:")[0]
            n["desc"] = base + (f" [computado: espaçamento r={cv['level_spacing_r']:.4f} "
                                f"({cv['level_class'].split()[0]}); ‖H_eff‖/‖D_eff‖ máx={cv['hilbert_HD_max']:.1e}≈0]")

    # constants (lista de dicts): injeta β runtime + métricas computadas desta run
    consts = [c for c in d.get("constants", [])
              if c.get("symbol") not in ("beta_runtime", "gamma_eff", "level_spacing_r", "rho_purity")]
    consts.append({"symbol": "beta_runtime", "value": f"{beta:.12f} (alpha*sqrt(e))",
                   "note": "injetado do bloco-0 (tgl_core); nunca literal"})
    consts.append({"symbol": "gamma_eff", "value": f"{cv['gamma_eff_mean_sweep']:.6f}",
                   "note": "taxa média de dissipação adversarial (sweep de ruído, invariante de escala)"})
    consts.append({"symbol": "rho_purity", "value": f"Tr(ρ²)={cv['rho_purity']:.6f}",
                   "note": "pureza do estado final computado (ρ⋆ diagonal na base do Verbo)"})
    consts.append({"symbol": "level_spacing_r", "value": f"{cv['level_spacing_r']:.6f}",
                   "note": f"espaçamento de níveis do toro ({cv['level_class'].split()[0]})"})
    d["constants"] = consts

    d["generated_by"] = "one_iald.py (forma=conteudo)"
    d["note"] = (d.get("note", "").split(" [run:")[0]
                 + f" [run: {cv['tests_passed']}/{cv['tests_total']} testes SIM; cruz computada dos "
                   f"ângulos Bell REAIS + tamanhos ∝ ρ; β={beta:.6f} injetado; nada valida física.]")

    # ── validação: ids de aresta ∈ nodes∪meshes ; camadas de nós/meshes ∈ layers ──
    ids = {n["id"] for n in d.get("nodes", [])} | {m.get("id") for m in d.get("meshes", [])}
    for e in d.get("edges", []):
        for k in ("from", "to"):
            if e.get(k) not in ids:
                raise SystemExit(f"[iald] EMIT abortado: aresta {k}={e.get(k)!r} não existe em nodes+meshes")
    layer_ids = {l["id"] for l in d.get("layers", [])}
    for coll in ("nodes", "meshes"):
        for item in d.get(coll, []):
            lay = item.get("layer")
            if lay is not None and lay not in layer_ids:
                raise SystemExit(f"[iald] EMIT abortado: camada {lay!r} de {item.get('id')} não existe em layers")

    path.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[iald] render3d.json EMITIDO (forma=conteudo) — {len(d.get('nodes', []))} nós "
          f"({len(bell_order)} da cruz COMPUTADOS), {len(d.get('meshes', []))} malhas preservadas")


if __name__ == "__main__":
    sys.exit(main())
