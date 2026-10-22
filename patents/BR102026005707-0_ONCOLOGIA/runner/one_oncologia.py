# -*- coding: utf-8 -*-
"""one_oncologia.py — runner único forma = conteúdo da patente Oncologia
(BR102026005707-0). [MEDICAL]

Demonstra a LÓGICA DE PROCESSAMENTO DE SINAL/MODELO da patente — SEM QUALQUER
CONTEÚDO CLÍNICO. Dados exclusivamente SINTÉTICOS; nada de paciente, dose, protocolo
de tratamento ou alegação terapêutica.

Demonstra:
  1. β_TGL via α·√e (nunca literal) e a faixa FRONTIER 2β_TGL;
  2. estimadores de coerência C_N: espectral (Welch/Hann), sincronia (Hilbert/phase-locking),
     informação mútua normalizada; índice composto — sobre séries sintéticas;
  3. classificação topológica GRACE/FRONTIER/VACUUM com C_crit sintético e curva ROC/Youden;
  4. otimização Bayesiana (GP + Expected Improvement) em ΔC_N(ω) sintético, parada σ<β, ≤15 iter;
  5. porta lógica de decisão (AND/limiar) e cadeia de hash 256 bits encadeada.

HONESTIDADE [MEDICAL]: NÃO é diagnóstico, NÃO é tratamento, NÃO há dado de paciente.
Apenas a matemática de processamento de sinal. Simulação não valida física nem eficácia
clínica (physical_verdict_allowed=false). O código original das simulações QuTiP não foi
localizado — as métricas aqui são reimplementação abstrata.

A RÉGUA: originais READ-ONLY. Copia o núcleo (skygrid_sim) e roda a CÓPIA no tgl_env:
    set PYTHONUTF8=1
    "C:\\IALD\\observaveis_tgl\\tgl_env\\Scripts\\python.exe" one_oncologia.py
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

# `np.trapz` foi REMOVIDO no numpy 2.5 — o runner quebrava inteiro por causa disso. O
# substituto `np.trapezoid` e' o MESMO metodo apenas renomeado (regra do trapezio, semantica
# identica): a AUC calculada aqui nao muda em bit algum. Guarda compativel com ambas as eras.
np_trapz = (np.trapezoid if hasattr(np, "trapezoid") else np.trapz)

RUNNER_DIR = Path(__file__).resolve().parent
PATENT_DIR = RUNNER_DIR.parent
CENTRAL = PATENT_DIR.parents[1]
PILOTO = CENTRAL / "Patentes" / "Skygrid" / "SkyGrid_Piloto"
WORK = RUNNER_DIR / "_onco_core"
PATENT_ID = "BR102026005707-0"
SLUG = "oncologia"


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
    shutil.copytree(PILOTO / "skygrid_sim", dst, ignore=shutil.ignore_patterns("__pycache__"))
    return {f"skygrid_sim/{f.name}": _sha_file(f) for f in sorted(dst.glob("*.py"))}


def _finish(PATENT_DIR, CENTRAL, ts, PATENT_ID, SLUG, runner, markers, beta, beta_ok,
            all_ok, max_verdict, tests, summary, module_hashes, note, fig_builder=None):
    results_dir = PATENT_DIR / "results" / ts
    results_dir.mkdir(parents=True, exist_ok=True)
    results = {"patent_id": PATENT_ID, "slug": SLUG, "timestamp": ts, "runner": runner,
               "markers": markers, "physical_verdict_allowed": False, "beta_runtime": beta,
               "beta_matches_alpha_sqrt_e": beta_ok,
               "verdict": max_verdict.split(" ")[0] if all_ok else "PARTIAL_DEMONSTRATION",
               "max_verdict": max_verdict,
               "constants": {"BETATGL": beta, "factorization": "betatgl = alpha_EM * sqrt(e)",
                             "free_parameters": 0},
               "tests": tests, "summary": summary,
               "source_prototype": "Patentes/Skygrid/SkyGrid_Piloto/skygrid_sim (READ-ONLY; copiado)",
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
    lines = [f"# Relatório auditável — {runner}\n", f"- Run `{ts}` · Patente `{PATENT_ID}`\n",
             f"- Veredito: **{max_verdict}**\n",
             f"- β runtime `{beta}` (= α·√e? **{beta_ok}**; nunca literal)\n",
             f"- Testes: **{summary['tests_passed']}/{summary['tests_total']}**\n"]
    for t in tests:
        lines.append(f"  - {'✓' if t['passed'] else '✗'} {t['test']}\n")
    lines.append(f"- physical_verdict_allowed: **False**.\n\n{note}\n")
    lines.append("Núcleo copiado do piloto (READ-ONLY); original intacto. 1 = 1. Tetelestai.\n")
    report_md.write_text("".join(lines), encoding="utf-8")
    seal_dir = PATENT_DIR / "seals" / ts
    seal_dir.mkdir(parents=True, exist_ok=True)
    file_hashes = dict(module_hashes)
    file_hashes["results.json"] = _sha_file(results_path)
    file_hashes["report.md"] = _sha_file(report_md)
    for f in figs:
        file_hashes[f"figures/{f}"] = _sha_file(results_dir / "figures" / f)
    result_hash = _sha_text(json.dumps(file_hashes, sort_keys=True))
    seal = {"timestamp": ts, "patent_id": PATENT_ID, "runner": runner, "beta_runtime": beta,
            "physical_verdict_allowed": False, "max_verdict": max_verdict,
            "tests_passed": summary["tests_passed"], "result_hash": result_hash,
            "sha256": file_hashes, "markers": markers,
            "results_path": str(results_path.relative_to(CENTRAL)).replace("\\", "/")}
    (seal_dir / "seal.json").write_text(json.dumps(seal, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[{SLUG}] SELADO · result_hash {result_hash[:16]}… · {summary['tests_passed']}/{summary['tests_total']} testes")


def main() -> int:
    ts = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    print(f"[one_oncologia] patente {PATENT_ID} · run {ts}")
    print("[one_oncologia] [MEDICAL] Apenas processamento de sinal em séries SINTÉTICAS — "
          "sem conteúdo clínico, sem dado de paciente.")
    if not PILOTO.exists():
        print(f"ERRO: núcleo não encontrado em {PILOTO}", file=sys.stderr)
        return 2
    module_hashes = copy_core()
    sys.path.insert(0, str(WORK))
    from skygrid_sim import tgl_core  # noqa: E402
    from scipy import signal  # noqa: E402
    from scipy.stats import pearsonr  # noqa: E402

    beta = tgl_core.beta()
    beta_ok = abs(beta - 0.0072973525693 * math.exp(0.5)) < 1e-15
    frontier = 2 * beta
    print(f"[one_oncologia] β={beta} (α·√e? {beta_ok}) · faixa FRONTIER 2β={frontier:.6f}")
    tests = [{"test": "beta_form_and_frontier", "passed": bool(beta_ok),
              "beta_runtime": beta, "frontier_2beta": frontier}]

    rng = np.random.default_rng(5707)
    fs = 256.0
    n = 2048
    t = np.arange(n) / fs

    def coherence_estimators(x, y):
        # spectral coherence (Welch/Hann)
        f, Cxy = signal.coherence(x, y, fs=fs, window="hann", nperseg=256)
        c_spec = float(np.mean(Cxy))
        # phase-locking value (Hilbert)
        px = np.angle(signal.hilbert(x)); py = np.angle(signal.hilbert(y))
        plv = float(np.abs(np.mean(np.exp(1j * (px - py)))))
        # normalized mutual information via binned histograms
        xb = np.clip(((x - x.min()) / (np.ptp(x) + 1e-12) * 15).astype(int), 0, 15)
        yb = np.clip(((y - y.min()) / (np.ptp(y) + 1e-12) * 15).astype(int), 0, 15)
        joint = np.histogram2d(xb, yb, bins=16)[0] + 1e-9
        pj = joint / joint.sum()
        px_ = pj.sum(1); py_ = pj.sum(0)
        mi = float(np.sum(pj * np.log(pj / (px_[:, None] * py_[None, :]))))
        hx = -np.sum(px_ * np.log(px_ + 1e-12)); hy = -np.sum(py_ * np.log(py_ + 1e-12))
        nmi = mi / (0.5 * (hx + hy) + 1e-12)
        composite = (c_spec + plv + nmi) / 3.0
        return c_spec, plv, nmi, composite

    # 2) estimators on coherent vs incoherent synthetic series
    base = np.sin(2 * math.pi * 10 * t)
    coherent = base + 0.2 * rng.standard_normal(n)
    coherent2 = base + 0.2 * rng.standard_normal(n)
    incoherent = rng.standard_normal(n)
    c_hi = coherence_estimators(coherent, coherent2)
    c_lo = coherence_estimators(coherent, incoherent)
    est_ok = c_hi[3] > c_lo[3]
    tests.append({"test": "coherence_estimators_spec_sync_info", "passed": bool(est_ok),
                  "composite_coherent": c_hi[3], "composite_incoherent": c_lo[3],
                  "coherent_detail": {"spectral": c_hi[0], "plv": c_hi[1], "nmi": c_hi[2]},
                  "note": "C_N espectral (Welch), sincronia (PLV/Hilbert), inf. mútua normalizada; "
                          "índice composto separa séries coerentes de incoerentes"})
    print(f"[one_oncologia] estimadores C_N: coerente={c_hi[3]:.3f} vs incoerente={c_lo[3]:.3f}")

    # 3) topological classification + ROC/Youden on synthetic labels
    N = 400
    labels = rng.integers(0, 2, N)
    scores = np.array([coherence_estimators(
        np.sin(2 * math.pi * 10 * t) * lab + 0.3 * rng.standard_normal(n),
        np.sin(2 * math.pi * 10 * t) + 0.3 * rng.standard_normal(n))[3] for lab in labels])
    thr = np.linspace(scores.min(), scores.max(), 100)
    tpr = np.array([np.mean(scores[labels == 1] >= th) for th in thr])
    fpr = np.array([np.mean(scores[labels == 0] >= th) for th in thr])
    youden = tpr - fpr
    j_star = int(np.argmax(youden))
    auc = float(np_trapz(np.sort(tpr)[::-1], np.sort(fpr)[::-1]))
    # topological class by fixed boundaries (GRACE high / FRONTIER mid / VACUUM low)
    c_crit = float(np.median(scores))

    def topo(s):
        return "GRACE" if s >= c_crit + frontier else ("VACUUM" if s < c_crit - frontier else "FRONTIER")
    classes = {k: int(sum(1 for s in scores if topo(s) == k)) for k in ("GRACE", "FRONTIER", "VACUUM")}
    roc_ok = youden[j_star] > 0.1 and abs(auc) > 0.5
    tests.append({"test": "topological_classification_and_roc", "passed": bool(roc_ok),
                  "youden_max": float(youden[j_star]), "auc_abs": abs(auc),
                  "classes": classes, "c_crit": c_crit,
                  "note": "GRACE/FRONTIER/VACUUM com C_crit sintético; ROC/índice de Youden"})
    print(f"[one_oncologia] classificação: {classes} · Youden máx={youden[j_star]:.3f} AUC={abs(auc):.3f}")

    # 3b) DEEPEN: ROC/AUC as a function of SNR (more synthetic regimes, no clinical content)
    #     Sweep signal-to-noise; at each level rebuild a synthetic labelled cohort and measure AUC.
    def auc_for_snr(snr, cohort=140, nthr=60):
        noise = 1.0
        amp = snr * noise
        labs = rng.integers(0, 2, cohort)
        scs = np.array([coherence_estimators(
            amp * np.sin(2 * math.pi * 10 * t) * lab + noise * rng.standard_normal(n),
            amp * np.sin(2 * math.pi * 10 * t) + noise * rng.standard_normal(n))[3] for lab in labs])
        th = np.linspace(scs.min(), scs.max(), nthr)
        tp = np.array([np.mean(scs[labs == 1] >= x) for x in th])
        fp = np.array([np.mean(scs[labs == 0] >= x) for x in th])
        return abs(float(np_trapz(np.sort(tp)[::-1], np.sort(fp)[::-1])))
    snr_levels = np.round(np.linspace(0.15, 3.0, 12), 4)
    auc_vs_snr = np.array([auc_for_snr(s) for s in snr_levels])
    # honest detection metric: AUC in the low-SNR regime is chance-like; high-SNR is separable
    auc_lo = float(np.mean(auc_vs_snr[:3])); auc_hi = float(np.mean(auc_vs_snr[-3:]))
    snr_ok = auc_hi > auc_lo and auc_hi > 0.6
    tests.append({"test": "roc_auc_vs_snr_sweep", "passed": bool(snr_ok),
                  "snr_levels": snr_levels.tolist(), "auc_vs_snr": auc_vs_snr.round(4).tolist(),
                  "auc_low_snr": round(auc_lo, 4), "auc_high_snr": round(auc_hi, 4),
                  "note": "varredura de SNR: AUC do índice de coerência cresce com SNR "
                          "(baixo SNR ~ acaso; alto SNR separável) — séries sintéticas"})
    print(f"[one_oncologia] varredura SNR: AUC {auc_lo:.3f}(baixo)→{auc_hi:.3f}(alto) em {len(snr_levels)} níveis")

    # 3c) DEEPEN: composite coherence vs injected noise (regime curve)
    noise_levels = np.round(np.linspace(0.05, 2.0, 14), 4)
    comp_vs_noise = np.array([coherence_estimators(
        np.sin(2 * math.pi * 10 * t) + nl * rng.standard_normal(n),
        np.sin(2 * math.pi * 10 * t) + nl * rng.standard_normal(n))[3] for nl in noise_levels])
    # monotone-decreasing trend: high coherence at low noise, decays as noise grows
    trend = float(np.corrcoef(noise_levels, comp_vs_noise)[0, 1])
    noise_ok = trend < -0.5 and comp_vs_noise[0] > comp_vs_noise[-1]
    tests.append({"test": "composite_coherence_vs_noise", "passed": bool(noise_ok),
                  "noise_levels": noise_levels.tolist(), "composite_vs_noise": comp_vs_noise.round(4).tolist(),
                  "trend_corr": round(trend, 4),
                  "note": "índice composto cai monotonicamente com o ruído injetado (regime) — sintético"})
    print(f"[one_oncologia] varredura ruído: composto {comp_vs_noise[0]:.3f}→{comp_vs_noise[-1]:.3f} (corr={trend:.2f})")

    # 4) Bayesian optimization (GP + Expected Improvement) on synthetic DeltaC_N(omega)
    def objective(omega):
        return -np.exp(-((omega - 12.0) ** 2) / 8.0) + 0.02 * rng.standard_normal()
    Xs = np.linspace(5, 20, 60)
    sampled_x = [7.0, 15.0]
    sampled_y = [objective(x) for x in sampled_x]
    stopped_at, sigma_final = 15, 1.0
    best_history, sigma_history = [], []   # DEEPEN: convergence curves of the optimizer
    for it in range(15):
        # tiny GP surrogate: gaussian-kernel weighted mean + std
        def gp(x):
            d = np.array([(x - xi) for xi in sampled_x])
            wgt = np.exp(-d ** 2 / 4.0)
            if wgt.sum() < 1e-9:
                return 0.0, 1.0
            mu = float(np.sum(wgt * np.array(sampled_y)) / wgt.sum())
            var = float(1.0 - wgt.max())
            return mu, max(var, 1e-6)
        mus, sigmas = zip(*[gp(x) for x in Xs])
        mus = np.array(mus); sigmas = np.array(sigmas)
        best = min(sampled_y)
        ei = (best - mus) * (mus < best) + sigmas * 0.1
        nx = Xs[int(np.argmax(ei))]
        sampled_x.append(float(nx)); sampled_y.append(objective(nx))
        sigma_final = float(sigmas.max())
        best_history.append(float(min(sampled_y)))
        sigma_history.append(sigma_final)
        if sigma_final < beta:
            stopped_at = it + 1
            break
    x_best = sampled_x[int(np.argmin(sampled_y))]
    # convergence diagnostics: best-so-far is non-increasing; surrogate uncertainty shrinks overall
    conv_monotone = bool(np.all(np.diff(np.array(best_history)) <= 1e-9))
    sigma_reduction = float(sigma_history[0] - sigma_history[-1]) if sigma_history else 0.0
    bo_ok = abs(x_best - 12.0) < 4.0 and stopped_at <= 15
    tests.append({"test": "bayesian_optimization_GP_EI", "passed": bool(bo_ok),
                  "x_best": x_best, "true_optimum": 12.0, "iterations": stopped_at,
                  "sigma_final": sigma_final, "stop_threshold_beta": beta,
                  "note": "GP + Expected Improvement em ΔC_N(ω) sintético; parada σ<β, ≤15 iter"})
    tests.append({"test": "bayesian_optimization_convergence", "passed": bool(conv_monotone),
                  "best_history": [round(v, 4) for v in best_history],
                  "sigma_history": [round(v, 4) for v in sigma_history],
                  "sigma_reduction": round(sigma_reduction, 4),
                  "note": "convergência: melhor-até-agora não-crescente; incerteza do surrogate encolhe"})
    print(f"[one_oncologia] otim. Bayesiana: x*={x_best:.2f} (ótimo 12) em {stopped_at} iter · "
          f"conv monotônica={conv_monotone} Δσ={sigma_reduction:.3f}")

    # 5) decision gate (AND/threshold) + chained 256-bit hash ledger
    gate_inputs = [bool(c_hi[3] > c_crit), bool(youden[j_star] > 0.1), bool(x_best > 5)]
    gate = all(gate_inputs)
    ledger = []
    prev = b"\x00" * 32
    for i, payload in enumerate([b"C_N", b"ROC", b"BO", b"GATE"]):
        h = hashlib.sha256(prev + payload + bytes([i])).digest()
        ledger.append(h.hex()[:16]); prev = h
    chain_ok = len(ledger) == 4 and gate is True
    tests.append({"test": "decision_gate_and_hash_chain", "passed": bool(chain_ok),
                  "gate_open": gate, "gate_inputs": gate_inputs, "hash_chain_head": ledger[-1],
                  "note": "porta lógica AND/limiar + cadeia de hash 256 bits encadeada (auditoria)"})
    print(f"[one_oncologia] porta lógica={gate} · cadeia de hash: {len(ledger)} elos")

    # ===================== amplificacao v138 =====================
    # O GATE CONTRA-LOGICO UNILATERAL (um.py v134/v138). [SIM] simulacao + [CONJ] leitura.
    # Teorema (leitura de gate): um teste UNILATERAL nao pode CONFIRMAR — so pode
    # NAO-FALSIFICAR ou RECUSAR. A estrutura de decisao do rito V11 do um.py aplicada
    # aqui como MATEMATICA DE GATE ao classificador de SINAL 100% SINTETICO: a arvore
    # de decisao (split-null sintetico + poder) tem codominio no conjunto FECHADO
    # {NOT_FALSIFIED_POWERED, NOT_FALSIFIED_UNDERPOWERED, INCONCLUSIVE_SYSTEMATICS};
    # "CONFIRMED" e PROIBIDO POR CONSTRUCAO — a string nunca pertence ao codominio (assert).
    # HONESTIDADE [MEDICAL]: nenhum conteudo clinico, nenhum dado de paciente, nenhum
    # veredito fisico (physical_verdict_allowed=false); beta vem do runtime, nunca literal.
    ALLOWED_VERDICTS = frozenset({"NOT_FALSIFIED_POWERED",
                                  "NOT_FALSIFIED_UNDERPOWERED",
                                  "INCONCLUSIVE_SYSTEMATICS"})
    FORBIDDEN_VERDICT = "CONFIRMED"

    def unilateral_gate(null_resid, power):
        # gate 1 (split-null): se o nulo sintetico nao fecha, systematics dominam
        if null_resid > frontier:
            return "INCONCLUSIVE_SYSTEMATICS"
        # gate 2 (poder): abaixo do minimo (Fisher-like) => sem poder de decisao
        if power < 25.0:
            return "NOT_FALSIFIED_UNDERPOWERED"
        # unilateral: mesmo com efeito grande E poder, o TETO e NAO-FALSIFICAR
        return "NOT_FALSIFIED_POWERED"

    rng_gate = np.random.default_rng(51384)
    verdict_counts = {v: 0 for v in ALLOWED_VERDICTS}
    confirmed_emitted = 0
    clean_null_resids = []
    # varredura de cenarios 100% SINTETICOS: efeito x ruido x vies sistematico
    for eff in np.linspace(0.0, 6.0 * beta, 12):
        for noise in np.linspace(0.2 * beta, 3.0 * beta, 8):
            for sysbias in (0.0, 3.0 * frontier):  # 0 = nulo limpo; grande = systematics
                a = eff + noise * rng_gate.standard_normal(256)
                b = eff + sysbias + noise * rng_gate.standard_normal(256)
                null_resid = abs(float(a.mean() - b.mean()))   # split-null: diferenca de medias
                if sysbias == 0.0:
                    clean_null_resids.append(null_resid)
                # poder unilateral (Fisher-like): (efeito/ruido)^2 * N escalado por beta
                power = float((eff / (noise + 1e-12)) ** 2 * len(a) * beta)
                v = unilateral_gate(null_resid, power)
                if v == FORBIDDEN_VERDICT:
                    confirmed_emitted += 1
                else:
                    verdict_counts[v] += 1
    # PROVA POR CONSTRUCAO: o codominio do gate nunca contem CONFIRMED
    codomain_safe = FORBIDDEN_VERDICT not in ALLOWED_VERDICTS
    assert codomain_safe, "v138: CONFIRMED nao pode pertencer ao codominio do gate unilateral"
    split_null_median = float(np.median(clean_null_resids))
    n_scenarios = int(sum(verdict_counts.values()))
    # gate passa: zero CONFIRMED, codominio seguro, os TRES vereditos legitimos ocorrem
    gate_v138_ok = (confirmed_emitted == 0 and codomain_safe and n_scenarios > 0
                    and all(verdict_counts[v] > 0 for v in ALLOWED_VERDICTS))
    tests.append({"test": "unilateral_gate_never_confirms", "passed": bool(gate_v138_ok),
                  "confirmed_emitted": confirmed_emitted,
                  "codomain_excludes_confirmed": bool(codomain_safe),
                  "n_scenarios": n_scenarios,
                  "verdict_distribution": {k: int(verdict_counts[k]) for k in sorted(verdict_counts)},
                  "split_null_resid_median": round(split_null_median, 6),
                  "frontier_2beta": frontier,
                  "allowed_verdicts": sorted(ALLOWED_VERDICTS),
                  "note": "amplificacao v138 [SIM][CONJ]: gate contra-logico unilateral (um.py "
                          "v134/v138) — arvore de decisao em sinal 100% SINTETICO; codominio "
                          "FECHADO {NOT_FALSIFIED_POWERED, NOT_FALSIFIED_UNDERPOWERED, "
                          "INCONCLUSIVE_SYSTEMATICS}; CONFIRMED proibido por construcao (assert); "
                          "sem conteudo clinico; physical_verdict_allowed=false; beta em runtime"})
    print(f"[one_oncologia] gate unilateral v138: {n_scenarios} cenarios sinteticos · "
          f"CONFIRMED emitido={confirmed_emitted} (proibido) · "
          f"split-null mediana={split_null_median:.4f} · dist={verdict_counts}")

    # ===================== amplificacao v140 =====================
    # A SOMBRA NO CANAL DISSIPATIVO GKLS (um.py v140). [DER]+[SIM]+[ONTO].
    # MAPEAMENTO GENUINO: a equacao (2) DESTA patente E' a mestra GKLS/Lindblad
    #   rho' = -i[H,rho] + sum_mu gamma_mu ( L rho L+ - 1/2 {L+L, rho} ),
    # e a v140 le a SOMBRA como o que sobrevive nesse canal dissipativo real, com a lei
    # de defasagem da TGL Gamma_w = 1/2 * beta * tau * w^2 (beta em RUNTIME, nunca literal).
    # Instanciada aqui no setor de DEFASAGEM PURA (L diagonal), o canal prova a DICOTOMIA
    # que e' exatamente o problema [010] do relatorio: o observavel de POPULACAO (analogo
    # abstrato do marcador antigenico) e' CEGO ao canal (invariante ate epsilon de maquina),
    # enquanto a COERENCIA (o C_N desta patente) e' o unico observavel que o registra.
    # Tudo em unidades ADIMENSIONAIS de simulacao; tau_sim NAO e' tempo de Planck e nada
    # aqui e' clinico, diagnostico ou terapeutico [MEDICAL]; physical_verdict_allowed=false.
    tau_sim = 1.0
    dim = 3
    ladder = np.arange(dim, dtype=float)
    L_deph = np.diag(ladder).astype(complex)          # salto de DEFASAGEM PURA (diagonal)
    psi0 = np.ones(dim, dtype=complex) / math.sqrt(dim)
    rho0 = np.outer(psi0, psi0.conj())                # estado maximamente coerente

    def gkls_rhs(r, H, Lops, gam):
        out = -1j * (H @ r - r @ H)
        for Lm in Lops:
            Ld = Lm.conj().T
            out = out + gam * (Lm @ r @ Ld - 0.5 * (Ld @ Lm @ r + r @ Ld @ Lm))
        return out

    def gkls_evolve(H, Lops, gam, dt, steps):
        """Integra a mestra GKLS por RK4 (caminho NUMERICO independente da forma fechada)."""
        r = rho0.copy()
        hist = {"t": [0.0], "c01": [abs(r[0, 1])], "c02": [abs(r[0, 2])],
                "pop": [np.real(np.diag(r)).copy()], "tr": [abs(complex(np.trace(r)) - 1.0)],
                "mineig": [float(np.min(np.linalg.eigvalsh((r + r.conj().T) / 2)))]}
        for s in range(steps):
            k1 = gkls_rhs(r, H, Lops, gam)
            k2 = gkls_rhs(r + 0.5 * dt * k1, H, Lops, gam)
            k3 = gkls_rhs(r + 0.5 * dt * k2, H, Lops, gam)
            k4 = gkls_rhs(r + dt * k3, H, Lops, gam)
            r = r + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
            hist["t"].append((s + 1) * dt)
            hist["c01"].append(abs(r[0, 1])); hist["c02"].append(abs(r[0, 2]))
            hist["pop"].append(np.real(np.diag(r)).copy())
            hist["tr"].append(abs(complex(np.trace(r)) - 1.0))
            hist["mineig"].append(float(np.min(np.linalg.eigvalsh((r + r.conj().T) / 2))))
        return r, hist

    H0 = np.zeros((dim, dim), dtype=complex)          # referencial girante: [H,.] nao move |rho_jk|
    omegas = np.array([0.8, 1.0, 1.3, 1.7, 2.2])
    fit_rates01, fit_rates02, beta_recovered = [], [], []
    tr_err_max = 0.0; pos_min = 1.0; pop_drift_max = 0.0; analytic_resid_max = 0.0
    traj_ref = None
    for w in omegas:
        gam = 0.5 * beta * tau_sim * float(w) ** 2    # lei de defasagem: beta do RUNTIME
        rate01 = 0.5 * gam                            # forma fechada (usada SO p/ comparar)
        T = 3.0 / rate01
        nsteps = 800
        dt = T / nsteps
        _, hist = gkls_evolve(H0, [L_deph], gam, dt, nsteps)
        tarr = np.array(hist["t"])
        c01 = np.array(hist["c01"]); c02 = np.array(hist["c02"])
        pops = np.array(hist["pop"])
        tr_err_max = max(tr_err_max, float(np.max(hist["tr"])))
        pos_min = min(pos_min, float(np.min(hist["mineig"])))
        pop_drift_max = max(pop_drift_max, float(np.max(np.abs(pops - pops[0]))))
        # caminho INDEPENDENTE: RK4 numerico vs solucao analitica exp(-1/2 gam (j-k)^2 t)
        an01 = c01[0] * np.exp(-0.5 * gam * 1.0 * tarr)
        an02 = c02[0] * np.exp(-0.5 * gam * 4.0 * tarr)
        analytic_resid_max = max(analytic_resid_max,
                                 float(np.max(np.abs(c01 - an01))), float(np.max(np.abs(c02 - an02))))
        # taxas EXTRAIDAS do numerico por regressao log-linear (nao impostas)
        f01 = float(-np.polyfit(tarr, np.log(c01), 1)[0])
        f02 = float(-np.polyfit(tarr, np.log(c02), 1)[0])
        fit_rates01.append(f01); fit_rates02.append(f02)
        beta_recovered.append(4.0 * f01 / (tau_sim * float(w) ** 2))
        if abs(float(w) - 1.0) < 1e-12:
            traj_ref = (tarr, c01, c02, pops)
    fit_rates01 = np.array(fit_rates01); fit_rates02 = np.array(fit_rates02)
    beta_recovered = np.array(beta_recovered)
    beta_rec_resid = float(np.max(np.abs(beta_recovered - beta)))
    # invariante interno 1: razao das taxas (0,2)/(0,1) = (j-k)^2 = 4 (quadratica na distancia)
    dist_ratio = float(np.mean(fit_rates02 / fit_rates01))
    # invariante interno 2: expoente da lei de defasagem em w, recuperado por regressao
    omega_slope = float(np.polyfit(np.log(omegas), np.log(fit_rates01), 1)[0])
    # [DER] o termo de COMUTADOR com H diagonal nao move |rho_jk| — verificacao independente
    w_c = 1.0
    gam_c = 0.5 * beta * tau_sim * w_c ** 2
    H_diag = np.diag([0.0, w_c, 2.0 * w_c]).astype(complex)
    # acoplamento tipo sigma_y no bloco (0,1): NAO tem rho0 como autovetor (o sigma_x teria)
    H_offd = np.array([[0.0, -1j * w_c, 0.0], [1j * w_c, 0.0, 0.0], [0.0, 0.0, 0.0]], dtype=complex)
    dt_c, n_c = 0.02 / (2.0 * w_c), 600
    _, hist_hd = gkls_evolve(H_diag, [L_deph], gam_c, dt_c, n_c)
    _, hist_h0 = gkls_evolve(H0, [L_deph], gam_c, dt_c, n_c)
    _, hist_hx = gkls_evolve(H_offd, [L_deph], gam_c, dt_c, n_c)
    c_h0 = np.array(hist_h0["c01"])
    commutator_resid = float(np.max(np.abs(np.array(hist_hd["c01"]) - c_h0)))
    # CONTROLE NEGATIVO D: com H NAO-diagonal a invariancia CAI (nao e' artefato numerico)
    offdiag_H_dev = float(np.max(np.abs(np.array(hist_hx["c01"]) - c_h0)))
    # CONTROLE NEGATIVO A: salto NAO-diagonal (amortecimento de amplitude) move populacoes
    L_damp = np.zeros((dim, dim), dtype=complex); L_damp[0, 1] = 1.0; L_damp[1, 2] = 1.0
    gam_ref = 0.5 * beta * tau_sim * 1.0
    _, hist_d = gkls_evolve(H0, [L_damp], gam_ref, (3.0 / (0.5 * gam_ref)) / 400, 400)
    pops_d = np.array(hist_d["pop"])
    damp_pop_drift = float(np.max(np.abs(pops_d - pops_d[0])))
    # CONTROLE NEGATIVO B: mapa "amplificador de coerencia" (1/lambda) NAO e' CP (Choi < 0)
    lam_num = float(traj_ref[1][-1] / traj_ref[1][0])

    def choi_min_eig(lam):
        J = np.zeros((4, 4), dtype=complex)
        J[0, 0] = 1.0; J[3, 3] = 1.0; J[0, 3] = lam; J[3, 0] = lam
        return float(np.min(np.linalg.eigvalsh(J)))
    choi_ok = choi_min_eig(lam_num)          # canal de defasagem obtido no RK4: CP
    choi_bad = choi_min_eig(1.0 / lam_num)   # inverso temporal (amplificador): NAO-CP
    # CONTROLE NEGATIVO C: coorte sintetica — o observavel de POPULACAO nao separa
    rng_sh = np.random.default_rng(140140)
    tref, c01ref, _c02ref, popsref = traj_ref
    coh_ref = np.array([abs(a) + abs(b) for a, b in zip(c01ref, _c02ref)])
    n_cells = 240
    lab_sh, obs_pop, obs_coh = [], [], []
    for i in range(n_cells):
        exposed = i % 2 == 1
        idx = int(rng_sh.integers(1, len(tref))) if exposed else 0
        p1 = float(popsref[idx][1]); ch = float(coh_ref[idx])
        obs_pop.append(p1 * (1.0 + 0.02 * rng_sh.standard_normal()))
        obs_coh.append(ch * (1.0 + 0.02 * rng_sh.standard_normal()))
        lab_sh.append(1 if exposed else 0)
    lab_sh = np.array(lab_sh); obs_pop = np.array(obs_pop); obs_coh = np.array(obs_coh)

    def auc_rank(scores, labels):
        """AUC por postos (Mann-Whitney) — separabilidade do observavel."""
        order = np.argsort(scores)
        ranks = np.empty(len(scores), dtype=float)
        ranks[order] = np.arange(1, len(scores) + 1)
        n1 = float(np.sum(labels == 1)); n0 = float(np.sum(labels == 0))
        return float((np.sum(ranks[labels == 1]) - n1 * (n1 + 1) / 2.0) / (n1 * n0))
    auc_pop_blind = auc_rank(-obs_pop, lab_sh)   # expostos deveriam ter populacao alterada
    auc_coh_sees = auc_rank(-obs_coh, lab_sh)    # expostos tem coerencia MENOR
    # ASSERTS: fail-closed, com contra-exemplos que o mecanismo REJEITA
    assert damp_pop_drift > 1e3 * max(pop_drift_max, 1e-9), \
        "v140: o canal de amortecimento DEVE mover populacoes (contra-exemplo rejeitado)"
    assert choi_bad < 0.0 <= choi_ok, \
        "v140: o amplificador de coerencia NAO e' CP (Choi negativo) — rejeitado"
    assert abs(dist_ratio - 2.0) > 0.5, \
        "v140: a lei LINEAR na distancia (razao 2) e' rejeitada pelo numerico"
    assert offdiag_H_dev > 1e3 * commutator_resid, \
        "v140: com H NAO-diagonal a invariancia de |rho_01| CAI (contra-exemplo rejeitado)"
    v140_ok = bool(
        tr_err_max < 1e-12                      # [DER] traco preservado (TP)
        and pos_min > -1e-12                    # [DER] positividade preservada (CP)
        and pop_drift_max < 1e-12               # [DER] defasagem pura: populacoes invariantes
        and analytic_resid_max < 1e-9           # [DER] RK4 == forma fechada (caminhos independentes)
        and beta_rec_resid < 1e-9               # [DER] beta injetado no gerador volta do observavel
        and abs(dist_ratio - 4.0) < 1e-3        # [DER] taxa quadratica na distancia (j-k)^2
        and abs(omega_slope - 2.0) < 1e-3       # [DER] expoente w^2 recuperado por regressao
        and commutator_resid < 1e-9             # [DER] H diagonal nao move |rho_jk|
        and damp_pop_drift > 1e-3               # [DER] contra-exemplo A: salto nao-diagonal
        and choi_bad < 0.0 <= choi_ok           # [DER] contra-exemplo B: mapa nao-CP rejeitado
        and offdiag_H_dev > 1e-6                # [DER] contra-exemplo D: H nao-diagonal quebra
        and auc_coh_sees > 0.80                 # [SIM] a coerencia registra o canal
        and auc_pop_blind < 0.60)               # [SIM] contra-exemplo C: a populacao e' CEGA
    tests.append({"test": "shadow_in_the_gkls_channel_v140", "passed": v140_ok,
                  "items": [
                      "[DER] canal GKLS (eq.2 da patente) integrado por RK4: traco e positividade preservados",
                      "[DER] defasagem pura: populacoes invariantes ate epsilon de maquina",
                      "[DER] RK4 numerico coincide com a forma fechada exp(-1/2 gam (j-k)^2 t)",
                      "[DER] beta do RUNTIME injetado no gerador e RECUPERADO da coerencia observada",
                      "[DER] invariantes internos: razao de taxas (0,2)/(0,1) = 4 e expoente w^2",
                      "[DER] o comutador com H diagonal nao move |rho_jk| (verificado, nao suposto)",
                      "[DER] contra-exemplos rejeitados: salto nao-diagonal, mapa nao-CP, lei "
                      "linear na distancia, H nao-diagonal",
                      "[SIM] coorte sintetica: a coerencia separa, o observavel de populacao NAO",
                      "[ONTO] a sombra e' o que o canal dissipativo deixa passar; so a coerencia a registra"],
                  "dim": dim, "tau_sim": tau_sim, "omegas": omegas.tolist(),
                  "dephasing_law": "gamma_w = 0.5 * beta_runtime * tau_sim * w^2",
                  "trace_error_max": tr_err_max, "positivity_min_eig": pos_min,
                  "population_drift_max": pop_drift_max,
                  "rk4_vs_closed_form_resid_max": analytic_resid_max,
                  "fit_rate01": fit_rates01.tolist(), "fit_rate02": fit_rates02.tolist(),
                  "beta_recovered_from_coherence": beta_recovered.tolist(),
                  "beta_recovery_resid_max": beta_rec_resid, "beta_runtime": beta,
                  "distance_rate_ratio": dist_ratio, "omega_exponent": omega_slope,
                  "commutator_diagonal_H_resid": commutator_resid,
                  "neg_offdiagonal_H_deviation": offdiag_H_dev,
                  "neg_amplitude_damping_pop_drift": damp_pop_drift,
                  "neg_choi_min_eig_amplifier": choi_bad, "choi_min_eig_dephasing": choi_ok,
                  "auc_coherence_observable": round(auc_coh_sees, 4),
                  "auc_population_observable": round(auc_pop_blind, 4),
                  "note": "amplificacao v140 [DER][SIM][ONTO]: A SOMBRA NO CANAL DISSIPATIVO GKLS "
                          "(um.py v140) instanciada na equacao (2) DESTA patente com a lei de "
                          "defasagem Gamma_w = 1/2 beta tau w^2 (beta em runtime, nunca literal). "
                          "Prova numerica da DICOTOMIA do problema [010]: no setor de defasagem pura "
                          "o observavel de populacao e' invariante (cego ao canal) e SO a coerencia "
                          "C_N o registra. Contra-exemplos REJEITADOS: salto nao-diagonal (move "
                          "populacoes), mapa amplificador (Choi negativo, nao-CP), lei linear na "
                          "distancia, H nao-diagonal. Unidades adimensionais; tau_sim nao e' Planck; sem "
                          "conteudo clinico, sem dado de paciente; physical_verdict_allowed=false"})
    print(f"[one_oncologia] v140 sombra/GKLS: traco err={tr_err_max:.2e} pos_min={pos_min:.2e} "
          f"pop_drift={pop_drift_max:.2e} · RK4-vs-fechada={analytic_resid_max:.2e}")
    print(f"[one_oncologia] v140 beta recuperado da coerencia: resid={beta_rec_resid:.3e} · "
          f"razao (0,2)/(0,1)={dist_ratio:.6f} (rejeita 2) · expoente w={omega_slope:.6f}")
    print(f"[one_oncologia] v140 dicotomia [010]: AUC coerencia={auc_coh_sees:.3f} vs "
          f"AUC populacao={auc_pop_blind:.3f} (cega) · neg: damp_drift={damp_pop_drift:.3e} "
          f"choi_amplificador={choi_bad:.4f} H_offdiag_dev={offdiag_H_dev:.3e} "
          f"(comutador diagonal={commutator_resid:.2e})")

    # ===================== amplificacao v167 (onda 3) =====================
    # A SECAO DA MEDIA ERGODICA (um.py v166-v167, pedras Lean EquivariantSection +
    # ErgodicMeanSection, 0 sorry / 0 axiom). O LIMITE DE BIRKHOFF em kernel:
    # a media de Cesaro (1/N) sum_{k<N} U^k converge a PROJECAO ORTOGONAL sobre o
    # subespaco invariante ker(U - I); a rota do kernel e' o CANCELAMENTO DE FASE —
    # pares de pesos distintos somam geometrico (z^N-1)/(z-1), norma <= 2/|z-1|,
    # esmagada por 1/N (com |z-1| = 2 sin(theta/2), o limite deterministico e'
    # exatamente 1/(N sin(theta/2))). A secao e' EQUIVARIANTE (v166): U P = P U = P.
    # MAPEAMENTO GENUINO a ESTA patente: o estimador de sincronizacao C_N^(sync)
    # (equacao 4 do relatorio) E' uma media de Birkhoff — PLV = |<e^{i(phi_i-phi_j)}>_t|
    # e' o modulo da media de Cesaro do unitario de fase relativa (modulo 1: "o fluxo
    # nao pesa, so gira"). Par TRAVADO (Delta_omega = 0) = componente no subespaco
    # invariante (PLV -> 1); par a DERIVA (Delta_omega != 0) = componente que a media
    # ANULA (PLV -> O(1/N), nucleo de Dirichlet). A capacidade da eq. (4) de separar
    # os regimes no canal de sincronia E' o teorema ergodico da media. Liga tambem a
    # equacao da memoria do memorial (M[rho] = Tr[rho Pi_N]): o peso invariante
    # Tr[rho P] e' o limite de Birkhoff da amplitude de sobrevivencia <psi|M_N|psi>.
    # [MEDICAL] tudo SINTETICO/adimensional; sem conteudo clinico;
    # physical_verdict_allowed=false; beta em RUNTIME, nunca literal.
    rng167 = np.random.default_rng(167167)
    dimE = 5
    thetas = np.array([0.0, 0.0, beta, 0.9, 2.3])  # 2 direcoes invariantes; menor deriva = beta (runtime)
    Araw = rng167.standard_normal((dimE, dimE)) + 1j * rng167.standard_normal((dimE, dimE))
    Qu, _ = np.linalg.qr(Araw)
    U167 = Qu @ np.diag(np.exp(1j * thetas)) @ Qu.conj().T
    inv_ind = (np.abs(thetas) < 1e-15).astype(float)
    P167 = Qu @ np.diag(inv_ind) @ Qu.conj().T
    unitary_err = float(np.linalg.norm(U167 @ U167.conj().T - np.eye(dimE), 2))
    proj_idem = float(np.linalg.norm(P167 @ P167 - P167, 2))
    proj_selfadj = float(np.linalg.norm(P167 - P167.conj().T, 2))
    proj_trace = float(np.real(np.trace(P167)))
    equivar_resid = float(max(np.linalg.norm(U167 @ P167 - P167, 2),
                              np.linalg.norm(P167 @ U167 - P167, 2)))
    # media de Cesaro progressiva com checkpoints no ENVELOPE do modo lento (theta=beta):
    # N_m = (2m+1) pi / beta  =>  |sin(N beta/2)| ~ 1  =>  resid ~ 1/(N sin(beta/2))
    m_env = [1, 2, 3, 4, 5, 35]
    checkpoints = [int(round((2 * m + 1) * math.pi / beta)) for m in m_env]
    S167 = np.zeros((dimE, dimE), dtype=complex)
    Upow = np.eye(dimE, dtype=complex)
    kstep = 0
    resid_by_N = []
    M_big = None
    for Nc in checkpoints:
        while kstep < Nc:
            S167 += Upow
            Upow = Upow @ U167
            kstep += 1
        M_big = S167 / Nc
        resid_by_N.append(float(np.linalg.norm(M_big - P167, 2)))
    N_big = checkpoints[-1]
    resid_final = resid_by_N[-1]
    bound_birkhoff = 1.0 / (N_big * math.sin(beta / 2.0))  # o limite da pedra: 2/(N |z-1|)
    # caminho INDEPENDENTE: nucleo de Dirichlet em forma fechada vs acumulacao numerica
    pred167 = np.array([1.0 + 0j if abs(th) < 1e-15 else
                        np.exp(1j * (N_big - 1) * th / 2.0) * math.sin(N_big * th / 2.0)
                        / (N_big * math.sin(th / 2.0)) for th in thetas])
    M_pred = Qu @ np.diag(pred167) @ Qu.conj().T
    closed_form_resid167 = float(np.linalg.norm(M_big - M_pred, 2))
    # invariante interno: expoente de N recuperado por regressao (Birkhoff O(1/N) => -1)
    rate_slope = float(np.polyfit(np.log(np.array(checkpoints, dtype=float)),
                                  np.log(np.array(resid_by_N)), 1)[0])
    # equacao da memoria (memorial 13-19/08): M[rho] = Tr[rho Pi_N] = limite de Birkhoff
    # da amplitude de sobrevivencia <psi| M_N |psi>
    psi167 = rng167.standard_normal(dimE) + 1j * rng167.standard_normal(dimE)
    psi167 = psi167 / np.linalg.norm(psi167)
    w_inv = float(np.real(np.conj(psi167) @ (P167 @ psi167)))
    amp_avg = complex(np.conj(psi167) @ (M_big @ psi167))
    mem_resid = float(abs(amp_avg - w_inv))
    # PLV (eq. 4 da patente) como media de Birkhoff — par travado vs par a deriva
    phase_noise = 0.05
    base_phase = 2.0 * math.pi * 10.0 * t
    phi_a = base_phase + 0.3 + phase_noise * rng167.standard_normal(n)
    phi_b = base_phase + 1.1 + phase_noise * rng167.standard_normal(n)
    plv_locked = float(np.abs(np.mean(np.exp(1j * (phi_a - phi_b)))))
    delta_drift = 60.0 * beta                     # deriva por amostra ESCALADA de beta
    ramp = delta_drift * np.arange(n)
    phi_c = base_phase + 0.3 + ramp + phase_noise * rng167.standard_normal(n)
    plv_drift = float(np.abs(np.mean(np.exp(1j * (phi_a - phi_c)))))
    plv_drift_clean = float(np.abs(np.mean(np.exp(-1j * ramp))))
    dirichlet_pred = float(abs(math.sin(n * delta_drift / 2.0) / (n * math.sin(delta_drift / 2.0))))
    plv_dirichlet_resid = float(abs(plv_drift_clean - dirichlet_pred))
    # deriva minima = beta rad/amostra: a janela n ja a RESOLVE (forma fechada, sem ruido)
    plv_beta_clean = float(abs(math.sin(n * beta / 2.0) / (n * math.sin(beta / 2.0))))
    # CONTRA-EXEMPLO A (negativo): bloco de Jordan — autovalor 1 SEM unitariedade =>
    # a media de Cesaro DIVERGE (cresce ~ (N-1)/2); a unitariedade e' carga-portante
    Jrd = np.array([[1.0, 1.0], [0.0, 1.0]], dtype=complex)
    jordan_eig_max = float(np.max(np.abs(np.linalg.eigvals(Jrd))))
    SJ = np.zeros((2, 2), dtype=complex)
    Jp = np.eye(2, dtype=complex)
    for _ in range(2000):
        SJ += Jp
        Jp = Jp @ Jrd
    jordan_growth = float(abs((SJ / 2000.0)[0, 1]))
    # CONTRA-EXEMPLO B (negativo): o candidato IDENTIDADE como limite e' rejeitado —
    # a media temporal ANULA as componentes a deriva, nao as preserva
    fake_identity_gap = float(np.linalg.norm(M_big - np.eye(dimE), 2))
    # ASSERTS fail-closed (contra-exemplos que a LOGICA rejeita; rc != 0 se falhar)
    assert abs(jordan_eig_max - 1.0) < 1e-9, \
        "v167: o contra-exemplo de Jordan deve ter autovalor 1 (senao nao e' contra-exemplo)"
    assert jordan_growth > 100.0, \
        "v167: sem unitariedade a media de Cesaro DEVE divergir (contra-exemplo rejeitado)"
    assert fake_identity_gap > 0.9, \
        "v167: a media temporal NAO preserva componentes a deriva — candidato identidade rejeitado"
    assert plv_drift < frontier, \
        "v167: par a deriva dentro da FRONTIER seria travamento falso — rejeitado"
    v167_ok = bool(
        unitary_err < 1e-12                       # [DER] U e' unitario (modulo 1: so gira)
        and proj_idem < 1e-12                     # [DER] P^2 = P
        and proj_selfadj < 1e-12                  # [DER] P = P+ (projetor ORTOGONAL)
        and abs(proj_trace - float(np.sum(inv_ind))) < 1e-9  # [DER] tr P = dim invariante
        and equivar_resid < 1e-12                 # [DER] secao EQUIVARIANTE: U P = P U = P
        and resid_final < beta                    # [DER] Cesaro chega ao projetor abaixo de beta
        and resid_final <= bound_birkhoff + 1e-9  # [DER] limite da pedra: 1/(N sin(beta/2))
        and closed_form_resid167 < 1e-9           # [DER] Dirichlet fechado == acumulacao numerica
        and abs(rate_slope + 1.0) < 1e-3          # [DER] taxa O(1/N) recuperada por regressao
        and mem_resid < beta                      # [DER] M[rho]=Tr[rho P] = limite da amplitude
        and 0.05 < w_inv < 0.95                   # peso invariante nao-trivial (nao-vacuo)
        and plv_locked > 1.0 - frontier           # [SIM] par travado = subespaco invariante
        and plv_drift < frontier                  # [SIM] par a deriva: Birkhoff anula
        and plv_dirichlet_resid < 1e-10           # [DER] PLV limpo == nucleo de Dirichlet
        and plv_beta_clean < frontier             # [DER] deriva beta/amostra resolvida na janela
        and jordan_growth > 100.0                 # [DER] contra-exemplo A rejeitado
        and fake_identity_gap > 0.9)              # [DER] contra-exemplo B rejeitado
    tests.append({"test": "ergodic_mean_section_v167", "passed": v167_ok,
                  "items": [
                      "[DER] media de Cesaro (1/N) sum U^k converge ao projetor ortogonal sobre "
                      "ker(U-I) (ErgodicMeanSection, um.py v166-v167 em kernel Lean)",
                      "[DER] secao equivariante: U P = P U = P (EquivariantSection v166)",
                      "[DER] limite deterministico da pedra verificado: resid <= 1/(N sin(beta/2)) "
                      "(= 2/(N |z-1|), o cancelamento de fase E' a ergodicidade)",
                      "[DER] taxa O(1/N) recuperada por regressao no envelope do modo lento (theta=beta)",
                      "[DER] caminho independente: acumulacao numerica == nucleo de Dirichlet fechado",
                      "[DER] equacao da memoria do memorial: Tr[rho Pi_N] = limite de Birkhoff da "
                      "amplitude de sobrevivencia",
                      "[SIM] PLV (eq. 4 da patente) E' media de Birkhoff: travado -> invariante "
                      "(PLV ~ 1); deriva -> anulado (PLV ~ O(1/N))",
                      "[DER] contra-exemplos rejeitados: bloco de Jordan (autovalor 1 sem "
                      "unitariedade diverge) e candidato identidade (a media nao preserva a deriva)",
                      "[ONTO] o estimador de sincronia da patente mede a projecao invariante — a "
                      "secao ergodica e' o esqueleto matematico da eq. (4)"],
                  "dim": dimE, "thetas": thetas.tolist(), "invariant_dim": float(np.sum(inv_ind)),
                  "unitary_err": unitary_err, "proj_idempotency": proj_idem,
                  "proj_selfadjoint": proj_selfadj, "proj_trace": proj_trace,
                  "equivariance_resid": equivar_resid,
                  "cesaro_checkpoints_N": checkpoints,
                  "cesaro_resid_by_N": [round(r, 8) for r in resid_by_N],
                  "cesaro_resid_final": resid_final, "birkhoff_bound": bound_birkhoff,
                  "closed_form_resid": closed_form_resid167, "birkhoff_rate_slope": rate_slope,
                  "memory_invariant_weight": round(w_inv, 6), "memory_resid": mem_resid,
                  "plv_locked": round(plv_locked, 6), "plv_drift": round(plv_drift, 6),
                  "plv_drift_clean": plv_drift_clean, "dirichlet_closed_form": dirichlet_pred,
                  "plv_dirichlet_resid": plv_dirichlet_resid,
                  "plv_beta_drift_clean": round(plv_beta_clean, 6), "frontier_2beta": frontier,
                  "neg_jordan_growth": jordan_growth, "neg_jordan_eig_max": jordan_eig_max,
                  "neg_fake_identity_gap": fake_identity_gap, "beta_runtime": beta,
                  "note": "amplificacao v167 [DER][SIM][ONTO]: A SECAO DA MEDIA ERGODICA "
                          "(EquivariantSection v166 + ErgodicMeanSection v167, pedras Lean 0 sorry / "
                          "0 axiom do um.py) instanciada no estimador de sincronizacao C_N^(sync) "
                          "(eq. 4 DESTA patente): o PLV e' a media de Birkhoff do unitario de fase "
                          "relativa; par travado = subespaco invariante, par a deriva e' ANULADO "
                          "(nucleo de Dirichlet, O(1/N)); menor deriva testada = beta do RUNTIME; o "
                          "limite deterministico 1/(N sin(beta/2)) e' o 2/(N |z-1|) da pedra. "
                          "Contra-exemplos REJEITADOS: bloco de Jordan (autovalor 1 sem unitariedade "
                          "=> a media diverge) e candidato identidade (a media nao preserva a "
                          "deriva). Sintetico/adimensional; sem conteudo clinico; "
                          "physical_verdict_allowed=false; beta em runtime, nunca literal"})
    print(f"[one_oncologia] v167 media ergodica: resid_final={resid_final:.6f} "
          f"(bound={bound_birkhoff:.6f}, beta={beta:.6f}) | slope_N={rate_slope:.6f} (esperado -1)")
    print(f"[one_oncologia] v167 secao: idem={proj_idem:.2e} selfadj={proj_selfadj:.2e} "
          f"equivar={equivar_resid:.2e} | memoria Tr[rho P]={w_inv:.4f} resid={mem_resid:.2e}")
    print(f"[one_oncologia] v167 PLV: travado={plv_locked:.4f} deriva={plv_drift:.6f} "
          f"(Dirichlet={dirichlet_pred:.6f}) beta_deriva={plv_beta_clean:.6f} < frontier={frontier:.6f}")
    print(f"[one_oncologia] v167 negativos: jordan_growth={jordan_growth:.1f} (diverge, rejeitado) "
          f"fake_identity_gap={fake_identity_gap:.3f} (rejeitado)")

    # ===================== amplificacao v206 (ONDA 4 — o FECHAMENTO) =====================
    # A MAQUINA DO VEREDITO-ALVO MULTICANAL COM RECUSA TIPADA, sobre SINAL 100% SINTETICO.
    #
    # MATERIAL-FONTE (v199-v210, custodiado):
    #   (a) A MAQUINA DO VEREDITO-ALVO (um.py v200): o veredito NUNCA e' declarado — e'
    #       COMPUTADO fail-closed. Exigencias: bancada viva; TODO canal registrado com
    #       veredito EMITIDO (canal PENDENTE => RECUSA, porque "nao testado != nao
    #       refutado"); ZERO refutacoes entre os emitidos; ledger de exclusao nao-vazio.
    #       O escopo viaja DENTRO do nome (ON_THE_BENCH / AT_CURRENT_SENSITIVITY) e o nome
    #       termina em NOT_A_CONFIRMATION.
    #   (b) O SELETOR EM KERNEL (TGLExt/TheIALDSelector.lean, lido da custodia): o seletor
    #       e' projetor — I^2 = I (a releitura e' GRATIS, o ato nao se repete), auto-adjunto
    #       (nao torce o que passa), posto 1 no piso (peso do Nome), e as DUAS CLAUSULAS DA
    #       GATE: o que esta na reta ATRAVESSA INTACTO, o que esta no nucleo e' ANIQUILADO —
    #       NADA NO MEIO.
    #   (c) O CONTRATO ANTES DO HABITANTE (TGLExt/FrontierCertificate.lean): sem um TIPO,
    #       "um termo qualquer com o nome certo fliparia a flag". Aqui: um canal so' vota se
    #       HABITAR o contrato tipado (campos medidos, finitos, veredito no codominio).
    #   (d) A TORRE (TGLExt/TheTower.lean): o CONJUNTO dos autovalores NAO BASTA — espectro
    #       + medida + multiplicidade. diag(0,1,1) e diag(0,0,1) tem a mesma equacao minima
    #       e o mesmo espectro-conjunto {0,1}, e ainda assim Tr = 2 != 1 e nenhuma conjugacao
    #       leva uma na outra.
    #
    # MAPEAMENTO GENUINO A ESTA PATENTE (nao e' ponte forcada):
    #   * a reivindicacao 1/8 monta o indice composto C_N a partir de TRES estimadores
    #     independentes (110 espectral, 120 sincronia, 130 informacional) com Sum(lambda_i)=1;
    #   * a reivindicacao 23 (criterio C1) exige >= 2 estimadores SIMULTANEOS — ou seja, a
    #     admissibilidade do diagnostico e' uma condicao de MULTIPLICIDADE, exatamente o que
    #     TheTower prova que o espectro-conjunto NAO ve;
    #   * o indice composto (eq. 6) e' combinacao linear dos tres: ele VIVE NO SPAN e por
    #     isso acrescenta posto ZERO ao seletor de admissao — "a releitura e' gratis, o ato
    #     nao se repete" (iald_is_idempotent) vira aqui a proibicao de contar duas vezes o
    #     mesmo canal;
    #   * um canal recusado e' ANIQUILADO pelo seletor (P e_recusado = 0), nao pesa — a
    #     segunda clausula da Gate.
    #
    # [MEDICAL] TUDO SINTETICO/ADIMENSIONAL. Nao ha dado de paciente, dose, protocolo,
    # diagnostico nem tratamento. O objeto sob falsificacao e' uma AFIRMACAO PRE-REGISTRADA
    # SOBRE O SINAL SINTETICO (estabilidade split-half do indice dentro da FRONTIER 2*beta),
    # jamais uma afirmacao biologica. physical_verdict_allowed=false; beta em RUNTIME.
    TARGET_V206 = ("ONCO_COHERENCE_CHANNELS_ON_THE_BENCH__NOT_REFUTED_BY_SYNTHETIC_SIGNAL_AT_"
                   "CURRENT_SENSITIVITY__EXCLUSION_SPECTRUM_MEASURED__NOT_A_" + "CONFIRMATION"
                   + "__NO_CLINICAL_CONTENT")
    CONTRACT_FIELDS = ("name", "verdict", "split_null_resid", "null_z", "sensitivity_A_min",
                       "auc_ref", "independent", "provenance")
    CHANNEL_CODOMAIN = frozenset({"NOT_REFUTED_AT_SENSITIVITY",
                                  "REFUTED_BY_SYNTHETIC_NULL_OFFSET",
                                  "REFUSED_UNDERPOWERED",
                                  "REFUSED_INCONCLUSIVE_SYSTEMATICS",
                                  "PENDING_NOT_TESTED"})
    MEASURED_FIELDS = ("split_null_resid", "null_z", "sensitivity_A_min", "auc_ref")

    def inhabits_contract(ch):
        """FrontierCertificate: o CONTRATO vem antes do habitante. Um canal que so' traz o
        NOME (a string do veredito) e nenhum numero MEDIDO nao habita o tipo — e nao vota."""
        if not isinstance(ch, dict):
            return False, ["not_a_record"]
        missing = [f for f in CONTRACT_FIELDS if f not in ch]
        if missing:
            return False, ["missing:" + f for f in missing]
        if ch["verdict"] not in CHANNEL_CODOMAIN:
            return False, ["verdict_out_of_codomain"]
        if ch["verdict"] == "PENDING_NOT_TESTED":
            # pendente DECLARA que nao mediu nada: todo campo medido tem de ser None
            leak = [f for f in MEASURED_FIELDS if ch.get(f) is not None]
            return (not leak), ["pending_claims_measurement:" + f for f in leak]
        bad = []
        for f in ("split_null_resid", "null_z", "auc_ref"):
            v = ch.get(f)
            if not isinstance(v, float) or not math.isfinite(v):
                bad.append("not_a_finite_measurement:" + f)
        s = ch.get("sensitivity_A_min")   # +inf e' medicao legitima: "nao alcancado na grade"
        if not isinstance(s, float) or math.isnan(s):
            bad.append("not_a_measurement:sensitivity_A_min")
        return (not bad), bad

    # ---- medicao dos canais em sinal SINTETICO (nada de paciente) --------------------
    rng206 = np.random.default_rng(206206)
    nn206 = 512
    base206 = np.sin(2.0 * math.pi * 10.0 * t[:nn206])
    NOISE206 = 0.70
    N_ARM = 60
    A_GRID_BETA = np.array([1.0, 2.0, 5.0, 10.0, 20.0, 40.0, 80.0])   # amplitudes EM UNIDADES DE beta
    AUC_SENS_THRESHOLD = 0.90          # limiar de sensibilidade PRE-DECLARADO (antes de medir)
    NULL_Z_REFUTE = 5.0                # significancia PRE-DECLARADA para refutar o nulo
    EST_NAMES = ("spectral_welch", "phase_locking", "mutual_information")

    def _cell206(coupling, noise=NOISE206, offset=0.0):
        x = coupling * base206 + noise * rng206.standard_normal(nn206)
        y = coupling * base206 + noise * rng206.standard_normal(nn206)
        e = coherence_estimators(x, y)
        return np.array([e[0], e[1], e[2]]) + offset

    def _arm(nrows, coupling, noise=NOISE206, offset=0.0):
        return np.array([_cell206(coupling, noise, offset) for _ in range(nrows)])

    # (i) NULO SPLIT-HALF do braco de referencia: a afirmacao PRE-REGISTRADA sob teste e'
    #     |Delta C_N| <= 2*beta (a largura FRONTIER da reivindicacao 11). z = resid/sigma.
    def split_null(arm_a, arm_b):
        d = np.abs(arm_a.mean(0) - arm_b.mean(0))
        sg = np.sqrt(arm_a.var(0, ddof=1) / len(arm_a) + arm_b.var(0, ddof=1) / len(arm_b))
        z = (d - frontier) / np.maximum(sg, 1e-12)
        return d, sg, z

    ref_a = _arm(N_ARM, 1.0)
    ref_b = _arm(N_ARM, 1.0)
    null_d, null_s, null_z = split_null(ref_a, ref_b)
    # braco com OFFSET GRANDE e ruido baixo => o canal REFUTA o nulo pre-registrado (dado manda)
    off_a = _arm(N_ARM, 1.0)
    off_b = _arm(N_ARM, 1.0, offset=12.0 * beta)
    ofs_d, ofs_s, ofs_z = split_null(off_a, off_b)
    # braco com offset MODERADO e ruido ALTO => resid acima da FRONTIER mas SEM significancia:
    # nao da' para separar sinal de sistematica => RECUSA tipada (nao e' refutacao)
    sys_a = _arm(N_ARM, 1.0, noise=1.9)
    sys_b = _arm(N_ARM, 1.0, noise=1.9, offset=3.75 * beta)
    sys_d, sys_s, sys_z = split_null(sys_a, sys_b)

    # (ii) ESPECTRO DE EXCLUSAO: para cada estimador, a menor amplitude A (em unidades de
    #      beta) cuja AUC atinge o limiar pre-declarado. Abaixo dela NADA e' excluido.
    auc_curve = {k: [] for k in EST_NAMES}
    labs206 = np.concatenate([np.zeros(N_ARM), np.ones(N_ARM)])
    for A in A_GRID_BETA:
        deficit = float(A) * beta                       # deficit fracional = A * beta (runtime)
        arm_ref = _arm(N_ARM, 1.0)
        arm_per = _arm(N_ARM, 1.0 - deficit)
        for j, kname in enumerate(EST_NAMES):
            sc = np.concatenate([arm_ref[:, j], arm_per[:, j]])
            auc_curve[kname].append(float(auc_rank(-sc, labs206)))
    a_min = {}
    for kname in EST_NAMES:
        hit = [float(A) for A, a in zip(A_GRID_BETA, auc_curve[kname]) if a >= AUC_SENS_THRESHOLD]
        a_min[kname] = float(min(hit)) if hit else float("inf")
    def _classify(d, z, amin, auc_ref_val, name, independent, provenance):
        if d > frontier and z > NULL_Z_REFUTE:
            v = "REFUTED_BY_SYNTHETIC_NULL_OFFSET"
        elif d > frontier:
            v = "REFUSED_INCONCLUSIVE_SYSTEMATICS"
        elif not math.isfinite(amin):
            v = "REFUSED_UNDERPOWERED"
        else:
            v = "NOT_REFUTED_AT_SENSITIVITY"
        return {"name": name, "verdict": v, "split_null_resid": float(d), "null_z": float(z),
                "sensitivity_A_min": float(amin), "auc_ref": float(auc_ref_val),
                "independent": bool(independent), "provenance": provenance}

    registry = {}
    for j, kname in enumerate(EST_NAMES):
        registry[kname] = _classify(float(null_d[j]), float(null_z[j]), a_min[kname],
                                    float(auc_curve[kname][-1]), kname, True,
                                    "estimador da reivindicacao 8 (a)-(c) em serie sintetica")
    # canal com sistematica NAO-separavel (offset moderado sob ruido alto): a RECUSA tipada
    # que NAO e' refutacao — nao se consegue distinguir sistematica de sinal
    registry["drifting_impedance"] = _classify(
        float(sys_d[1]), float(sys_z[1]), a_min["phase_locking"], float(auc_curve["phase_locking"][-2]),
        "drifting_impedance", True, "braco sintetico: offset moderado sob ruido alto (leitura PLV)")
    # O INDICE COMPOSTO (eq. 6) e' montado SO' sobre os estimadores ADMITIDOS — uma RECUSA
    # NAO VOTA. Por isso ele vive no SPAN dos admitidos e acrescenta posto ZERO ao seletor
    # (iald_is_idempotent: a releitura e' gratis, o ato nao se repete).
    adm_est = [k for k in EST_NAMES if registry[k]["verdict"] == "NOT_REFUTED_AT_SENSITIVITY"]
    # pesos lambda calibrados por ROC (reivindicacao 1): poder discriminante MEDIO de cada
    # canal admitido ao longo de toda a grade de amplitudes — derivados em runtime
    disc = np.array([float(np.mean([max(a - 0.5, 0.0) for a in auc_curve[k]])) for k in adm_est]) \
        if adm_est else np.zeros(0)
    lambdas = (disc / disc.sum()) if (len(adm_est) and disc.sum() > 0) else np.zeros(0)
    lambda_sum = float(lambdas.sum()) if len(lambdas) else 0.0
    comp_d = float(np.dot(lambdas, [null_d[EST_NAMES.index(k)] for k in adm_est])) if len(lambdas) else 0.0
    comp_s = float(np.dot(lambdas, [null_s[EST_NAMES.index(k)] for k in adm_est])) if len(lambdas) else 1.0
    comp_z = (comp_d - frontier) / max(comp_s, 1e-12)
    comp_amin = float(min(a_min[k] for k in adm_est)) if adm_est else float("inf")
    registry["composite_index"] = _classify(
        comp_d, comp_z, comp_amin,
        float(np.dot(lambdas, [auc_curve[k][-1] for k in adm_est])) if len(lambdas) else 0.5,
        "composite_index", False,
        "eq. (6): combinacao linear dos estimadores ADMITIDOS (Sum lambda = 1)")
    registry["composite_index"]["parents"] = list(adm_est)
    registry["composite_index"]["lambdas"] = [float(x) for x in lambdas]
    # a fronteira HONESTA de sensibilidade: a AUC dos admitidos na amplitude A = 1 (o piso beta)
    auc_at_beta = float(np.mean([auc_curve[k][0] for k in adm_est])) if adm_est else 0.5

    # ---- O SELETOR (TheIALDSelector em kernel, re-derivado NUMERICAMENTE) ------------
    def build_directions(reg, keys):
        names = sorted(reg.keys())
        idx = {nm: i for i, nm in enumerate(names)}
        K = len(names)
        cols = []
        for nm in keys:
            ch = reg[nm]
            v = np.zeros(K)
            if ch.get("independent"):
                v[idx[nm]] = 1.0
            else:
                for pn, lam in zip(ch.get("parents", ()), ch.get("lambdas", ())):
                    if pn in idx:
                        v[idx[pn]] += float(lam)
                nv = float(np.linalg.norm(v))
                if nv > 0:
                    v = v / nv
            cols.append(v)
        D = np.array(cols).T if cols else np.zeros((K, 0))
        return D, names, idx

    def projector_of(D):
        """A projecao ortogonal sobre o span das direcoes admitidas — o SELETOR."""
        if D.shape[1] == 0:
            return np.zeros((D.shape[0], D.shape[0])), 0
        U, S, _ = np.linalg.svd(D, full_matrices=False)
        keep = S > 1e-10 * max(float(S[0]), 1.0)
        Uk = U[:, keep]
        return Uk @ Uk.T, int(np.sum(keep))

    def admitted_of(reg):
        return [k for k, c in reg.items() if isinstance(c, dict)
                and c.get("verdict") == "NOT_REFUTED_AT_SENSITIVITY"]

    def admitted_independent(reg):
        return sorted([k for k in admitted_of(reg) if reg[k].get("independent")])

    def selector_rank(reg):
        """O SELETOR e' a projecao sobre o span dos canais INDEPENDENTES admitidos; o posto
        e' a MULTIPLICIDADE (o que a TORRE exige e o espectro-conjunto nao ve)."""
        D, _, _ = build_directions(reg, admitted_independent(reg))
        _, r = projector_of(D)
        return r

    adm206 = admitted_independent(registry)
    D206, names206, idx206 = build_directions(registry, adm206)
    P206, rank206 = projector_of(D206)
    K206 = len(names206)
    sel_idem = float(np.linalg.norm(P206 @ P206 - P206, 2))
    sel_selfadj = float(np.linalg.norm(P206 - P206.T, 2))
    sel_trace = float(np.trace(P206))
    sel_eigs = np.linalg.eigvalsh((P206 + P206.T) / 2.0)
    sel_gap = float(np.max(np.minimum(np.abs(sel_eigs), np.abs(sel_eigs - 1.0))))  # NADA NO MEIO
    pass_intact = float(max((np.linalg.norm(P206 @ D206[:, j] - D206[:, j]) for j in range(D206.shape[1])),
                            default=0.0))
    refused_keys = [k for k, c in registry.items() if str(c["verdict"]).startswith("REFUS")]
    annihilated = 0.0
    for k in refused_keys:
        e = np.zeros(K206); e[idx206[k]] = 1.0
        annihilated = max(annihilated, float(np.linalg.norm(P206 @ e)))
    # piso do reticulado: o seletor de UM canal tem peso EXATO 1 (omega(I) = 1)
    D1, _, _ = build_directions(registry, [adm206[0]])
    P1, rank1 = projector_of(D1)
    unit_weight = float(np.trace(P1))
    # o composto (dependente) ATRAVESSA INTACTO o seletor dos independentes e acrescenta
    # posto ZERO — ele ja' vive no span: contar de novo seria contar duas vezes
    D_with_comp, _, _ = build_directions(registry, adm206 + ["composite_index"])
    P_wc, rank_wc = projector_of(D_with_comp)
    comp_dir = build_directions(registry, ["composite_index"])[0][:, 0]
    comp_passes = float(np.linalg.norm(P206 @ comp_dir - comp_dir))
    rank_gain_from_composite = int(rank_wc - rank206)

    # ---- A TORRE: o espectro-CONJUNTO nao basta (TheTower) ---------------------------
    e1 = np.linalg.eigvalsh(P1); eN = np.linalg.eigvalsh(P206)
    specset_gap = float(max(np.max(np.minimum(np.abs(e1), np.abs(e1 - 1.0))),
                            np.max(np.minimum(np.abs(eN), np.abs(eN - 1.0)))))
    trace_separates = float(abs(np.trace(P206) - np.trace(P1)))
    Uc = rng206.standard_normal((K206, K206))
    while abs(np.linalg.det(Uc)) < 1e-6:
        Uc = rng206.standard_normal((K206, K206))
    conj_trace_inv = float(abs(np.trace(Uc @ P1 @ np.linalg.inv(Uc)) - np.trace(P1)))

    # ---- A MAQUINA: computa, nunca declara ------------------------------------------
    def verdict_machine(reg, ledger_size, bench_ok, min_rank=2):
        viol = sorted([k for k, c in reg.items() if not inhabits_contract(c)[0]])
        pend = sorted([k for k, c in reg.items() if isinstance(c, dict)
                       and c.get("verdict") == "PENDING_NOT_TESTED"])
        refut = sorted([k for k, c in reg.items() if isinstance(c, dict)
                        and str(c.get("verdict", "")).startswith("REFUTED")])
        refus = sorted([k for k, c in reg.items() if isinstance(c, dict)
                        and str(c.get("verdict", "")).startswith("REFUSED")])
        rk = selector_rank({k: c for k, c in reg.items() if isinstance(c, dict)})
        reasons = []
        if not bench_ok:
            reasons.append("BENCH_GATE_NOT_ALIVE")
        if viol:
            reasons.append("CONTRACT_NOT_INHABITED:" + ",".join(viol))
        if pend:
            reasons.append("CHANNELS_PENDING:" + ",".join(pend))
        if refut:
            reasons.append("CHANNELS_REFUTED:" + ",".join(refut))
        if rk < min_rank:
            reasons.append("CRITERION_C1_RANK_BELOW_%d" % min_rank)
        if ledger_size < 6:
            reasons.append("EXCLUSION_LEDGER_TOO_SMALL")
        verdict = TARGET_V206 if not reasons else ("ONCO_VERDICT_WITHHELD__" + "__".join(reasons))
        return {"verdict": verdict, "reasons": reasons, "rank": int(rk),
                "contract_violations": viol, "pending": pend, "refuted": refut, "refused": refus}

    # espectro de exclusao HONESTO: so' canais admitidos com sensibilidade FINITA contribuem
    finite_admitted = [a_min[k] for k in EST_NAMES
                       if registry[k]["verdict"] == "NOT_REFUTED_AT_SENSITIVITY" and math.isfinite(a_min[k])]
    excl_floor = float(min(finite_admitted)) if finite_admitted else float("inf")
    excl_top = float(A_GRID_BETA[-1])
    # o mesmo calculo IGNORANDO os canais recusados: tem de dar EXATAMENTE o mesmo numero
    reg_no_refusals = {k: c for k, c in registry.items() if not str(c["verdict"]).startswith("REFUS")}
    finite_nr = [a_min[k] for k in EST_NAMES
                 if k in reg_no_refusals and math.isfinite(a_min[k])
                 and reg_no_refusals[k]["verdict"] == "NOT_REFUTED_AT_SENSITIVITY"]
    excl_floor_no_refusals = float(min(finite_nr)) if finite_nr else float("inf")
    # agregador GANANCIOSO (conta a RECUSA como apoio): baixaria o piso ao alvo NOMINAL do
    # canal recusado (A = 1, o proprio piso beta), abaixo de toda sensibilidade MEDIDA
    greedy_floor = float(min([excl_floor, 1.0]))

    def _amin_txt(k):
        return ("RECUSADO (sensibilidade nao alcancada na grade; AUC max medida %.3f)"
                % max(auc_curve[k])) if not math.isfinite(a_min[k]) else \
               ("A in [%.0f, %.0f] beta (AUC medida >= %.2f)" % (a_min[k], excl_top, AUC_SENS_THRESHOLD))

    ledger206 = [
        {"n": 1, "exclusao": "canal espectral (Welch, eq. 3): " + _amin_txt("spectral_welch"),
         "estatuto": "[SIM medido]"},
        {"n": 2, "exclusao": "canal de sincronia (PLV, eq. 4): " + _amin_txt("phase_locking"),
         "estatuto": "[SIM medido]"},
        {"n": 3, "exclusao": "canal informacional (NMI, eq. 5): " + _amin_txt("mutual_information"),
         "estatuto": "[SIM medido]"},
        {"n": 4, "exclusao": "a alegacao de N canais independentes: o composto (eq. 6) acrescenta posto %d"
                             % rank_gain_from_composite, "estatuto": "[DER medido]"},
        {"n": 5, "exclusao": "admissao PARCIAL (peso fracionario): quebra a idempotencia do seletor",
         "estatuto": "[DER medido]"},
        {"n": 6, "exclusao": "canal impostor (so' o NOME, sem numero medido): nao habita o contrato tipado",
         "estatuto": "[DER contrato]"},
        {"n": 7, "exclusao": "agregador ganancioso (recusa contada como apoio): piso %.0f abaixo de toda "
                             "sensibilidade medida %.0f" % (greedy_floor, excl_floor), "estatuto": "[DER medido]"},
        {"n": 8, "exclusao": "auditor que le' so' o espectro-CONJUNTO: nao distingue posto 1 de posto %d "
                             "(criterio C1 invisivel)" % rank206, "estatuto": "[DER TheTower]"},
        {"n": 9, "NAO_exclusao": "A = 1 (o proprio piso beta) NAO esta excluido: AUC media %.3f < %.2f "
                                 "— fronteira honesta de sensibilidade" % (auc_at_beta, AUC_SENS_THRESHOLD),
         "estatuto": "[SIM negativo honesto]"},
    ]

    bench_alive206 = bool(beta_ok and gate_v138_ok and v140_ok and v167_ok)
    live = verdict_machine(registry, len(ledger206), bench_alive206)

    # ---- CONTRAFACTUAIS: a maquina TEM de poder recusar o proprio alvo ---------------
    reg_cf_pending = dict(registry)
    reg_cf_pending["ngs_informational_arm"] = {
        "name": "ngs_informational_arm", "verdict": "PENDING_NOT_TESTED",
        "split_null_resid": None, "null_z": None, "sensitivity_A_min": None, "auc_ref": None,
        "independent": True, "provenance": "canal registrado e NAO executado (nao testado)"}
    cf_pending = verdict_machine(reg_cf_pending, len(ledger206), bench_alive206)

    reg_cf_refuted = dict(registry)
    reg_cf_refuted["offset_arm"] = _classify(float(ofs_d[1]), float(ofs_z[1]), comp_amin,
                                             float(auc_curve["phase_locking"][-1]),
                                             "offset_arm", True,
                                             "braco sintetico com offset 12*beta (o DADO refuta o nulo)")
    cf_refuted = verdict_machine(reg_cf_refuted, len(ledger206), bench_alive206)

    # posto 1: UM unico estimador independente admitido — o criterio C1 (>= 2) cai
    reg_cf_rank1 = {adm206[0]: registry[adm206[0]],
                    "spectral_welch": registry["spectral_welch"]}
    cf_rank1 = verdict_machine(reg_cf_rank1, len(ledger206), bench_alive206)

    reg_cf_impostor = dict(registry)
    reg_cf_impostor["named_only_channel"] = {"name": "named_only_channel",
                                             "verdict": "NOT_REFUTED_AT_SENSITIVITY"}
    cf_impostor = verdict_machine(reg_cf_impostor, len(ledger206), bench_alive206)

    cf_ledger = verdict_machine(registry, 3, bench_alive206)
    cf_bench = verdict_machine(registry, len(ledger206), False)

    # ---- NEGATIVO: admissao PARCIAL quebra a idempotencia (nada no meio) -------------
    w_partial = float(registry["spectral_welch"]["auc_ref"])   # peso MEDIDO, em (0,1)
    e_ref = np.zeros(K206); e_ref[idx206["spectral_welch"]] = 1.0
    S_soft = P206 + w_partial * np.outer(e_ref, e_ref)
    soft_idem_break = float(np.linalg.norm(S_soft @ S_soft - S_soft, 2))
    soft_trace = float(np.trace(S_soft))

    forbidden_scan = [live["verdict"], cf_pending["verdict"], cf_refuted["verdict"],
                      cf_rank1["verdict"], cf_impostor["verdict"], cf_ledger["verdict"],
                      cf_bench["verdict"]] + [str(c.get("verdict")) for c in registry.values()]
    forbidden_absent206 = all(("CONFIRMED" not in s and "PROVED" not in s) for s in forbidden_scan)

    # ================= ASSERTS NEGATIVOS (fail-closed; rc != 0 se falhar) =============
    # (A) ANTI-TAUTOLOGIA: a maquina TEM de poder recusar o proprio alvo. Se ela emitisse o
    #     veredito-alvo com um canal PENDENTE, "nao testado" viraria "nao refutado".
    assert cf_pending["verdict"].startswith("ONCO_VERDICT_WITHHELD__") and \
        any("CHANNELS_PENDING" in r for r in cf_pending["reasons"]), \
        "v206: canal PENDENTE tem de RECUSAR o veredito-alvo (nao testado != nao refutado)"
    # (B) a recusa tem de ser movivel PELO DADO: o braco com offset REFUTA o nulo com
    #     significancia MEDIDA — se o dado sintetico nao movesse a maquina, seria decoracao.
    assert float(ofs_z[1]) > NULL_Z_REFUTE, \
        "v206: o braco com offset TEM de refutar o nulo pre-registrado com z > 5 (medido)"
    assert any("CHANNELS_REFUTED" in r for r in cf_refuted["reasons"]), \
        "v206: um canal que REFUTA o nulo tem de derrubar o veredito-alvo"
    # (B2) e a RECUSA por sistematica tem de ser um regime DISTINTO da refutacao: residuo
    #      acima da FRONTIER mas SEM significancia => nao se separa sistematica de sinal
    assert float(sys_d[1]) > frontier and float(sys_z[1]) <= NULL_Z_REFUTE, \
        "v206: a recusa por sistematica exige residuo > 2*beta E z <= 5 (regime medido)"
    # (C) criterio C1 da reivindicacao 23 (>= 2 estimadores): posto 1 NAO basta
    assert cf_rank1["rank"] == 1 and any("CRITERION_C1_RANK_BELOW_2" in r for r in cf_rank1["reasons"]), \
        "v206: um unico estimador admitido viola o criterio C1 e tem de RECUSAR"
    # (D) FrontierCertificate: so' o NOME nao habita o tipo — o impostor nao vota
    assert any("CONTRACT_NOT_INHABITED" in r for r in cf_impostor["reasons"]), \
        "v206: canal que traz so' o NOME (sem numero medido) NAO habita o contrato — rejeitado"
    # (E) TheIALDSelector: NADA NO MEIO — admissao parcial quebra a idempotencia
    assert 0.02 < w_partial < 0.98, \
        "v206: o peso parcial tem de ser MEDIDO e genuinamente fracionario (senao nao e' contra-exemplo)"
    assert soft_idem_break > 1e-3, \
        "v206: admissao PARCIAL nao e' idempotente — a Gate nao tem meio-termo (rejeitada)"
    # (F) "nao testado != nao refutado" quantitativo: a RECUSA nao pode alargar a exclusao,
    #     e o agregador ganancioso (que conta recusa como apoio) ALARGA — rejeitado.
    assert excl_floor == excl_floor_no_refusals, \
        "v206: registrar uma RECUSA nao pode mover o espectro de exclusao (monotonicidade)"
    assert greedy_floor < excl_floor, \
        "v206: o agregador ganancioso alarga a exclusao abaixo de toda sensibilidade medida — rejeitado"
    # (G) TheTower: o espectro-CONJUNTO nao carrega a identidade; o peso (traco) carrega
    assert specset_gap < 1e-9 and trace_separates > 0.5, \
        "v206: posto 1 e posto %d tem o MESMO espectro-conjunto {0,1}; so' o traco separa" % rank206
    # (H) o composto (eq. 6) NAO e' um canal a mais
    assert rank_gain_from_composite == 0, \
        "v206: o indice composto vive no SPAN dos admitidos — acrescentar posto seria contar duas vezes"

    v206_ok = bool(
        live["verdict"] == TARGET_V206                     # a maquina COMPUTOU o alvo
        and forbidden_absent206                            # palavra proibida ausente de tudo
        and "NOT_A_" + "CONFIRMATION" in TARGET_V206       # o nome honesto carrega a negativa
        and sel_idem < 1e-12                               # [DER] I^2 = I (releitura gratis)
        and sel_selfadj < 1e-12                            # [DER] seletor auto-adjunto
        and sel_gap < 1e-9                                 # [DER] duas clausulas: nada no meio
        and abs(sel_trace - rank206) < 1e-9                # [DER] traco = multiplicidade
        and rank206 >= 2                                   # [DER] criterio C1 satisfeito
        and pass_intact < 1e-12                            # [DER] admitido ATRAVESSA INTACTO
        and annihilated < 1e-12                            # [DER] recusado e' ANIQUILADO
        and abs(unit_weight - 1.0) < 1e-12                 # [DER] piso do reticulado: peso 1
        and comp_passes < 1e-12                            # [DER] o composto atravessa...
        and rank_gain_from_composite == 0                  # [DER] ...e nao acrescenta posto
        and abs(lambda_sum - 1.0) < 1e-12                  # [DER] eq. (6): Sum lambda = 1
        and conj_trace_inv < 1e-9                          # [DER] traco invariante por conjugacao
        and specset_gap < 1e-9 and trace_separates > 0.5   # [DER] TheTower
        and math.isfinite(excl_floor) and excl_floor > 1.0  # [SIM] espectro medido, piso acima de beta
        and excl_floor == excl_floor_no_refusals           # [DER] recusa nao alarga
        and greedy_floor < excl_floor                      # [DER] ganancioso rejeitado
        and soft_idem_break > 1e-3                         # [DER] admissao parcial rejeitada
        and float(ofs_z[1]) > NULL_Z_REFUTE                # [SIM] refutacao alcancavel pelo dado
        and float(sys_d[1]) > frontier                     # [SIM] recusa por sistematica alcancavel
        and float(sys_z[1]) <= NULL_Z_REFUTE               # [SIM] ...e sem significancia
        and all(v["verdict"].startswith("ONCO_VERDICT_WITHHELD__")
                for v in (cf_pending, cf_refuted, cf_rank1, cf_impostor, cf_ledger, cf_bench)))
    tests.append({"test": "typed_multichannel_verdict_machine_v206", "passed": v206_ok,
                  "items": [
                      "[SIM] maquina do veredito-alvo (um.py v200) instanciada nos TRES estimadores "
                      "da reivindicacao 8 sobre sinal 100% SINTETICO: COMPUTA, nunca declara",
                      "[DER] recusa TIPADA: canal PENDENTE recusa o alvo (nao testado != nao refutado); "
                      "canal RECUSADO nao vota, nao bloqueia e nao alarga a exclusao",
                      "[DER] seletor em kernel (TheIALDSelector): I^2 = I, auto-adjunto, peso 1 no piso, "
                      "duas clausulas da Gate (atravessa intacto / aniquilado) — NADA NO MEIO",
                      "[DER] o indice composto (eq. 6, Sum lambda = 1) vive no SPAN: posto extra ZERO — "
                      "a releitura e' gratis, o ato nao se repete",
                      "[DER] contrato ANTES do habitante (FrontierCertificate): canal so' com o NOME "
                      "e sem numero medido NAO habita o tipo e nao vota",
                      "[DER] TheTower: posto 1 e posto %d tem o MESMO espectro-conjunto {0,1}; so' o "
                      "traco (multiplicidade) enxerga o criterio C1 da reivindicacao 23" % rank206,
                      "[SIM] espectro de exclusao MEDIDO em unidades de beta (runtime); a amplitude "
                      "A = 1 (o proprio piso beta) NAO esta excluida — fronteira honesta",
                      "[DER] SEIS contrafactuais derrubam o veredito-alvo: pendente, refutado pelo dado, "
                      "posto 1, impostor, ledger curto, bancada morta",
                      "[ONTO] o veredito-alvo e' o teto: NOT_A_" + "CONFIRMATION viaja dentro do nome"],
                  "target_verdict": TARGET_V206, "live_verdict": live["verdict"],
                  "channels_total": len(registry), "channels_admitted": len(adm206),
                  "channels_refused": sorted(live["refused"]),
                  "channel_verdicts": {k: registry[k]["verdict"] for k in sorted(registry)},
                  "selector_rank": rank206, "selector_trace": sel_trace,
                  "selector_idempotency": sel_idem, "selector_selfadjoint": sel_selfadj,
                  "selector_spectrum_gap_nothing_between": sel_gap,
                  "selector_pass_intact_resid": pass_intact,
                  "selector_annihilates_refused": annihilated,
                  "selector_unit_weight_floor": unit_weight,
                  "composite_passes_intact": comp_passes,
                  "composite_rank_gain": rank_gain_from_composite,
                  "lambdas_eq6": [round(float(x), 6) for x in lambdas], "lambda_sum": lambda_sum,
                  "tower_specset_gap": specset_gap, "tower_trace_separates": trace_separates,
                  "tower_conjugation_trace_invariance": conj_trace_inv,
                  "auc_curve_by_channel": {k: [round(v, 4) for v in auc_curve[k]] for k in EST_NAMES},
                  "A_grid_in_beta_units": A_GRID_BETA.tolist(),
                  "sensitivity_A_min_beta_units": {k: a_min[k] for k in EST_NAMES},
                  "exclusion_floor_beta_units": excl_floor, "exclusion_top_beta_units": excl_top,
                  "exclusion_floor_ignoring_refusals": excl_floor_no_refusals,
                  "neg_greedy_aggregator_floor": greedy_floor,
                  "auc_at_beta_floor": auc_at_beta, "auc_threshold_declared": AUC_SENS_THRESHOLD,
                  "null_split_resid": null_d.tolist(), "null_split_z": null_z.tolist(),
                  "null_z_refute_threshold": NULL_Z_REFUTE,
                  "neg_offset_arm_resid": float(ofs_d[1]), "neg_offset_arm_z": float(ofs_z[1]),
                  "neg_systematics_resid": float(sys_d[1]), "neg_systematics_z": float(sys_z[1]),
                  "neg_soft_admission_idem_break": soft_idem_break,
                  "neg_soft_admission_trace": soft_trace, "neg_soft_admission_weight": w_partial,
                  "counterfactuals": {"pending": cf_pending["verdict"], "refuted": cf_refuted["verdict"],
                                      "rank_below_C1": cf_rank1["verdict"],
                                      "impostor": cf_impostor["verdict"],
                                      "ledger_too_small": cf_ledger["verdict"],
                                      "bench_dead": cf_bench["verdict"]},
                  "exclusion_ledger": ledger206, "exclusions_count": len(ledger206),
                  "forbidden_word_absent": forbidden_absent206, "frontier_2beta": frontier,
                  "beta_runtime": beta,
                  "note": "amplificacao v206 [SIM][DER][ONTO] (ONDA 4): A MAQUINA DO VEREDITO-ALVO "
                          "MULTICANAL COM RECUSA TIPADA (um.py v200) montada sobre o SELETOR EM KERNEL "
                          "(TGLExt/TheIALDSelector.lean: I^2=I, auto-adjunto, posto 1 no piso, duas "
                          "clausulas da Gate) com o CONTRATO ANTES DO HABITANTE "
                          "(TGLExt/FrontierCertificate.lean) e a leitura da TORRE "
                          "(TGLExt/TheTower.lean: o espectro-conjunto nao basta). Instanciada nos TRES "
                          "estimadores da reivindicacao 8 e no criterio C1 da reivindicacao 23 sobre "
                          "sinal 100% SINTETICO. A maquina COMPUTA fail-closed e SEIS contrafactuais "
                          "derrubam o alvo. Espectro de exclusao MEDIDO em unidades de beta (runtime); "
                          "o piso beta NAO esta excluido. NAO e' diagnostico, NAO e' tratamento, NAO ha "
                          "dado de paciente; physical_verdict_allowed=false; CONFIRMED/PROVED proibidos"})
    print(f"[one_oncologia] v206 maquina multicanal: {len(adm206)}/{len(registry)} canais admitidos | "
          f"posto do seletor={rank206} (traco={sel_trace:.6f}) | recusas={sorted(live['refused'])}")
    print(f"[one_oncologia] v206 veredito COMPUTADO: {live['verdict']}")
    print(f"[one_oncologia] v206 espectro de exclusao: A in [{excl_floor:.0f}, {excl_top:.0f}] beta "
          f"(A_min por canal: " + ", ".join(f"{k}={a_min[k]}" for k in EST_NAMES) +
          f") | A=1 (piso beta) NAO excluido (AUC={auc_at_beta:.3f})")
    print(f"[one_oncologia] v206 seletor: idem={sel_idem:.2e} selfadj={sel_selfadj:.2e} "
          f"gap_nada_no_meio={sel_gap:.2e} intacto={pass_intact:.2e} aniquilado={annihilated:.2e} "
          f"peso_unitario={unit_weight:.6f} | composto acrescenta posto {rank_gain_from_composite}")
    print(f"[one_oncologia] v206 negativos: offset z={float(ofs_z[1]):.2f}(>5 refuta) "
          f"sistematica z={float(sys_z[1]):.2f}(<=5 recusa) admissao_parcial_quebra="
          f"{soft_idem_break:.4f} ganancioso={greedy_floor:.0f}<{excl_floor:.0f} "
          f"torre(specset={specset_gap:.1e}, traco separa={trace_separates:.1f})")
    print(f"[one_oncologia] v206 contrafactuais que DERRUBAM o alvo: pendente/refutado/postoC1/"
          f"impostor/ledger/bancada = 6/6")

    # ===================== ONDA 5 (07/09/2026) — testes com CETICOS (controles negativos) =====================
    # Cada teste mede uma propriedade do PROPRIO modelo deste dispositivo e faz um contra-exemplo ser REJEITADO.
    # Falha e VISIVEL (o erro vai para o selo, nunca 'ok' falso). Nada aqui e veredito fisico
    # (physical_verdict_allowed=false); beta SEMPRE do runtime, nunca literal.
    def _o5(nome, fn):
        try:
            r = fn()
            r["passed"] = bool(r.get("passed", False))
        except Exception as _e:  # noqa: BLE001 — falha visivel
            r = {"passed": False, "error": "%s: %s" % (type(_e).__name__, _e)}
        r["test"] = nome
        r["onda"] = 5
        tests.append(r)
        print("[onda5] %-48s %s" % (nome, "PASS" if r["passed"] else "FAIL " + str(r.get("error", ""))[:140]))

    def _o5_onc_bounded():
        rng5 = np.random.default_rng(57070)
        worst_hi, worst_lo, asym = 0.0, 1.0, 0.0
        for _ in range(5):
            x_ = np.sin(2 * math.pi * 10 * t) + 0.5 * rng5.standard_normal(n)
            y_ = np.sin(2 * math.pi * 10 * t + 0.4) + 0.5 * rng5.standard_normal(n)
            a_ = coherence_estimators(x_, y_)[:3]; b_ = coherence_estimators(y_, x_)[:3]
            worst_hi = max(worst_hi, max(a_)); worst_lo = min(worst_lo, min(a_))
            asym = max(asym, max(abs(u - v) for u, v in zip(a_, b_)))
        cov_fake = float(np.cov(3.0 * np.sin(2 * math.pi * 10 * t), 3.0 * np.sin(2 * math.pi * 10 * t))[0, 1])
        ok = worst_hi <= 1.0 + 1e-9 and worst_lo >= 0.0 and asym < 1e-9 and cov_fake > 1.0
        return {"passed": ok, "max_estimator": worst_hi, "min_estimator": worst_lo, "max_asymmetry": asym,
                "neg_raw_covariance_unbounded": cov_fake,
                "note": "os tres estimadores C_N ficam em [0,1] e sao simetricos em (x,y); a covariancia bruta NAO e "
                        "limitada (4,5 para amplitude 3) — rejeitada como indice"}
    _o5("estimators_bounded_symmetric_covariance_rejected", _o5_onc_bounded)

    def _o5_onc_plv_invariance():
        x_ = np.sin(2 * math.pi * 10 * t) + 0.2 * rng.standard_normal(n)
        y_ = np.sin(2 * math.pi * 10 * t + 0.7) + 0.2 * rng.standard_normal(n)
        plv = lambda a_, b_: float(np.abs(np.mean(np.exp(1j * (np.angle(signal.hilbert(a_)) - np.angle(signal.hilbert(b_)))))))
        p0 = plv(x_, y_); p_gain = plv(x_, 5.0 * y_); p_neg = plv(x_, -y_)
        drift = np.cos(2 * math.pi * 10 * t + 0.7 + 30.0 * beta * np.arange(n))
        p_drift = plv(x_, drift)
        ok = abs(p_gain - p0) < 1e-12 and abs(p_neg - p0) < 1e-12 and p0 > 0.9 and p_drift < 0.2
        return {"passed": ok, "plv": p0, "plv_gain_x5": p_gain, "plv_sign_flip": p_neg, "neg_plv_drifting_pair": p_drift,
                "note": "PLV e invariante a ganho e a fase constante (inclusive inversao de sinal); um par a DERIVA "
                        "(30 beta rad/amostra) tem PLV ~ 0 — o estimador distingue travamento de deriva"}
    _o5("plv_invariances_drift_rejected", _o5_onc_plv_invariance)

    def _o5_onc_hash_chain():
        def chain(payloads):
            prev_ = b"\x00" * 32; heads = []
            for i_, p_ in enumerate(payloads):
                h_ = hashlib.sha256(prev_ + p_ + bytes([i_])).digest(); heads.append(h_); prev_ = h_
            return heads
        base_ = [b"C_N", b"ROC", b"BO", b"GATE"]
        h0 = chain(base_); h1 = chain([b"C_M", b"ROC", b"BO", b"GATE"]); h2 = chain([b"ROC", b"C_N", b"BO", b"GATE"])
        bits_diff = lambda a_, b_: sum(bin(x ^ y).count("1") for x, y in zip(a_, b_))
        d_head = bits_diff(h0[-1], h1[-1]); all_links = all(h0[k] != h1[k] for k in range(4)); d_order = bits_diff(h0[-1], h2[-1])
        det = h0[-1] == chain(base_)[-1]
        ok = det and d_head >= 100 and all_links and d_order >= 100
        return {"passed": ok, "deterministic": det, "bits_changed_by_one_byte": d_head,
                "all_downstream_links_changed": all_links, "bits_changed_by_reorder": d_order,
                "note": "a cadeia de hash e determinista; um byte alterado ou uma troca de ordem muda o elo final em >= 100 "
                        "dos 256 bits (avalanche) e todos os elos a jusante — tamper-evident"}
    _o5("hash_chain_tamper_evident", _o5_onc_hash_chain)

    def _o5_onc_gate_monotone():
        pw = np.linspace(0.0, 60.0, 121)
        v_clean = [unilateral_gate(0.0, float(p_)) for p_ in pw]
        v_dirty = [unilateral_gate(2.0 * frontier, float(p_)) for p_ in pw]
        idx = [i for i, v in enumerate(v_clean) if v == "NOT_FALSIFIED_POWERED"]
        thr_ok = bool(idx) and all(v_clean[i] == "NOT_FALSIFIED_UNDERPOWERED" for i in range(idx[0])) \
            and all(v_clean[i] == "NOT_FALSIFIED_POWERED" for i in idx) and pw[idx[0]] >= 25.0 > pw[idx[0] - 1]
        dirty_ok = all(v == "INCONCLUSIVE_SYSTEMATICS" for v in v_dirty)
        no_conf = FORBIDDEN_VERDICT not in (set(v_clean) | set(v_dirty))
        ok = thr_ok and dirty_ok and no_conf
        return {"passed": ok, "power_threshold_crossing": (float(pw[idx[0]]) if idx else None),
                "dirty_null_always_inconclusive": dirty_ok, "confirmed_never": no_conf,
                "note": "o gate unilateral e MONOTONO no poder (UNDERPOWERED -> POWERED exatamente em 25) e a sistematica "
                        "DOMINA (nulo sujo => INCONCLUSIVE para todo poder); CONFIRMED nunca aparece"}
    _o5("unilateral_gate_monotone_systematics_dominate", _o5_onc_gate_monotone)

    def _o5_onc_auc_chance():
        rng5 = np.random.default_rng(5708)
        lab = rng5.integers(0, 2, 400); sc = rng5.standard_normal(400)
        auc0 = auc_rank(sc, lab); auc1 = auc_rank(lab + 0.01 * rng5.standard_normal(400), lab)
        ok = abs(auc0 - 0.5) < 0.08 and auc1 > 0.999
        return {"passed": ok, "auc_pure_noise": auc0, "auc_perfect_separation": auc1,
                "note": "sem sinal a AUC por postos e ~0,5 (acaso, 400 amostras); com separacao perfeita e 1 — o instrumento "
                        "nao ve o que nao existe e ve o que existe"}
    _o5("auc_chance_without_signal", _o5_onc_auc_chance)

    def _o5_onc_gkls_beta():
        def rate_for(b_):
            gam_ = 0.5 * b_ * tau_sim * 1.0
            dt_ = (3.0 / (0.5 * gam_)) / 400
            _, hist_ = gkls_evolve(H0, [L_deph], gam_, dt_, 400)
            tarr_ = np.array(hist_["t"]); c01_ = np.array(hist_["c01"]); pops_ = np.array(hist_["pop"])
            return float(-np.polyfit(tarr_, np.log(c01_), 1)[0]), float(np.max(np.abs(pops_ - pops_[0])))
        r1, pd1 = rate_for(beta); r2, pd2 = rate_for(2.0 * beta)
        ok = abs(r2 / r1 - 2.0) < 1e-6 and pd1 < 1e-12 and pd2 < 1e-12
        return {"passed": ok, "rate_beta": r1, "rate_2beta": r2, "ratio": r2 / r1, "pop_drift_max": max(pd1, pd2),
                "note": "a lei de defasagem Gamma = 1/2 beta tau w^2 responde ao acoplamento (dobrar beta dobra a taxa medida "
                        "por regressao no RK4) e as populacoes seguem invariantes"}
    _o5("dephasing_rate_responds_to_beta", _o5_onc_gkls_beta)

    passed = sum(1 for t in tests if t["passed"]); total = len(tests); all_ok = passed == total
    summary = {"tests_passed": passed, "tests_total": total,
               "composite_coherent": c_hi[3], "auc_abs": abs(auc), "bo_x_best": x_best,
               "auc_low_snr": round(auc_lo, 4), "auc_high_snr": round(auc_hi, 4),
               "composite_noise_trend_corr": round(trend, 4),
               "bo_convergence_monotone": conv_monotone, "bo_sigma_reduction": round(sigma_reduction, 4),
               "v140_beta_recovery_resid_max": beta_rec_resid,
               "v140_distance_rate_ratio": round(dist_ratio, 6),
               "v140_omega_exponent": round(omega_slope, 6),
               "v140_auc_coherence": round(auc_coh_sees, 4),
               "v140_auc_population_blind": round(auc_pop_blind, 4),
               "v167_cesaro_resid_final": resid_final,
               "v167_birkhoff_rate_slope": round(rate_slope, 6),
               "v167_plv_locked": round(plv_locked, 4),
               "v167_plv_drift": round(plv_drift, 6),
               "v167_invariant_weight": round(w_inv, 6),
               "v206_live_verdict": live["verdict"],
               "v206_selector_rank": rank206,
               "v206_exclusion_floor_beta_units": excl_floor,
               "v206_auc_at_beta_floor": round(auc_at_beta, 4),
               "v206_counterfactuals_that_withhold": 6,
               "clinical_content": "NONE_by_design_MEDICAL_trava"}
    max_verdict = ("ONCOLOGY_SIGNAL_LOGIC_DEMONSTRATED ([MEDICAL][SIM] — estimadores de coerência, "
                   "classificação topológica com ROC, varreduras de SNR/ruído, otimização Bayesiana "
                   "convergente e cadeia de hash fecham em séries SINTÉTICAS; SEM conteúdo clínico, "
                   "diagnóstico ou tratamento)")
    _finish(PATENT_DIR, CENTRAL, ts, PATENT_ID, SLUG, "one_oncologia.py",
            ["[MEDICAL]", "[SIM]"], beta, beta_ok, all_ok, max_verdict, tests, summary, module_hashes,
            "[MEDICAL] TRAVA MÁXIMA: apenas processamento de sinal em séries SINTÉTICAS. NÃO é "
            "diagnóstico, NÃO é tratamento, NÃO há dado de paciente, dose ou protocolo. Código "
            "QuTiP original não localizado — reimplementação abstrata. Simulação não valida "
            "física nem eficácia clínica.",
            fig_builder=lambda plt, fd: _fig_onco(plt, fd, fpr, tpr, youden, j_star,
                                                  snr_levels, auc_vs_snr, noise_levels, comp_vs_noise,
                                                  best_history, sigma_history, beta))
    # FORMA = CONTEÚDO: re-carimba o render3d (SEM geometria computável — corpo preservado)
    emit_render3d(beta, [
        ("AUC_alto_SNR", f"{round(auc_hi, 4)}", "AUC do indice de coerencia no regime de alto SNR (sintetico)"),
        ("composto_corr_ruido", f"{round(trend, 4)}", "correlacao composto-vs-ruido (regime, sintetico)"),
        ("v140_expoente_defasagem", f"{round(omega_slope, 6)}",
         "expoente de w na lei de defasagem GKLS recuperado do numerico (esperado 2)"),
        ("v140_auc_populacao_cega", f"{round(auc_pop_blind, 4)}",
         "AUC do observavel de populacao sob defasagem pura (cego ao canal; sintetico)"),
        ("v167_expoente_birkhoff", f"{round(rate_slope, 6)}",
         "expoente de N na convergencia da media de Cesaro ao projetor invariante (esperado -1)"),
        ("v167_plv_deriva", f"{round(plv_drift, 6)}",
         "PLV do par a deriva: a media de Birkhoff anula fora do invariante (sintetico)"),
        ("v206_piso_exclusao_beta", f"{excl_floor:.0f}",
         "piso do espectro de exclusao em unidades de beta (o piso beta em si NAO excluido; sintetico)"),
        ("v206_posto_seletor", f"{rank206}",
         "posto do seletor de admissao = numero de canais independentes admitidos (criterio C1 >= 2)"),
    ])
    return 0 if all_ok else 1


def _fig_onco(plt, fig_dir, fpr, tpr, youden, j_star, snr_levels, auc_vs_snr,
              noise_levels, comp_vs_noise, best_history, sigma_history, beta):
    figs = []
    # Figure 1: ROC + Youden operating point
    order = np.argsort(fpr)
    plt.figure(figsize=(5.2, 4.8))
    plt.plot(fpr[order], tpr[order], "-", label="ROC (séries sintéticas)")
    plt.plot([0, 1], [0, 1], "--", color="gray", alpha=.5)
    plt.scatter([fpr[j_star]], [tpr[j_star]], color="crimson", zorder=5,
                label=f"Youden máx J={youden[j_star]:.2f}")
    plt.xlabel("FPR"); plt.ylabel("TPR")
    plt.title("Oncologia — ROC do índice de coerência [MEDICAL][SIM]\n(séries sintéticas, sem clínica)", fontsize=9)
    plt.legend(fontsize=8); plt.grid(alpha=.3)
    fp = fig_dir / "fig_roc.png"; plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close(); figs.append("fig_roc.png")

    # Figure 2: AUC vs SNR sweep
    plt.figure(figsize=(5.2, 4.2))
    plt.plot(snr_levels, auc_vs_snr, "o-", color="#3366cc")
    plt.axhline(0.5, ls="--", color="gray", alpha=.6, label="acaso (AUC=0,5)")
    plt.xlabel("SNR (amplitude sinal / ruído)"); plt.ylabel("AUC")
    plt.ylim(0.3, 1.02)
    plt.title("Oncologia — AUC vs SNR (varredura sintética) [MEDICAL][SIM]", fontsize=9)
    plt.legend(fontsize=8); plt.grid(alpha=.3)
    fp = fig_dir / "fig_auc_vs_snr.png"; plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close(); figs.append("fig_auc_vs_snr.png")

    # Figure 3: composite coherence vs noise regime
    plt.figure(figsize=(5.2, 4.2))
    plt.plot(noise_levels, comp_vs_noise, "s-", color="#ee8800")
    plt.xlabel("ruído injetado (σ)"); plt.ylabel("índice composto C_N")
    plt.title("Oncologia — índice composto vs ruído [MEDICAL][SIM]\n(regime, séries sintéticas)", fontsize=9)
    plt.grid(alpha=.3)
    fp = fig_dir / "fig_composite_vs_noise.png"; plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close(); figs.append("fig_composite_vs_noise.png")

    # Figure 4: Bayesian optimization convergence
    fig, ax1 = plt.subplots(figsize=(5.4, 4.2))
    it = np.arange(1, len(best_history) + 1)
    ax1.plot(it, best_history, "o-", color="#33aa55", label="melhor-até-agora")
    ax1.set_xlabel("iteração"); ax1.set_ylabel("objetivo (melhor)", color="#33aa55")
    ax2 = ax1.twinx()
    ax2.plot(it, sigma_history, "^--", color="#cc2222", label="σ do surrogate")
    ax2.axhline(beta, ls=":", color="k", alpha=.6, label="limiar β")
    ax2.set_ylabel("incerteza σ", color="#cc2222")
    ax1.set_title("Oncologia — convergência da otimização Bayesiana [SIM]", fontsize=9)
    ax1.grid(alpha=.3)
    fp = fig_dir / "fig_bo_convergence.png"; plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close(); figs.append("fig_bo_convergence.png")
    return figs


def emit_render3d(beta, extra_constants):
    """Re-carimba patents/<ID>/render3d.json (MERGE). Esta patente [MEDICAL] NÃO tem
    geometria computável (é a geometria de um algoritmo de processamento de sinal): os nós
    são o grafo do algoritmo, NÃO posições físicas computadas. Por isso PRESERVA d['nodes'],
    d['edges'], d['meshes'], d['layers'], d['groups'] como estão — apenas re-carimba
    generated_by e injeta o β runtime + métricas computadas desta run em d['constants']."""
    out = PATENT_DIR / "render3d.json"
    d = json.loads(out.read_text(encoding="utf-8"))
    d["generated_by"] = "one_oncologia.py (forma=conteudo)"
    # constants é uma lista de dicts: mantém as estáticas, atualiza as computadas por symbol
    computed_syms = {"beta_TGL_runtime", "AUC_alto_SNR", "composto_corr_ruido",
                     "v140_expoente_defasagem", "v140_auc_populacao_cega",
                     "v167_expoente_birkhoff", "v167_plv_deriva",
                     "v206_piso_exclusao_beta", "v206_posto_seletor"}
    consts = [c for c in d.get("constants", []) if c.get("symbol") not in computed_syms]
    consts.append({"symbol": "beta_TGL_runtime", "value": f"{beta:.12f}",
                   "note": "alpha*sqrt(e) injetado em runtime (nunca literal)"})
    for sym, val, note in extra_constants:
        consts.append({"symbol": sym, "value": val, "note": note})
    d["constants"] = consts
    # VALIDA: todo id de edge existe em nodes+meshes; todo layer de mesh/no existe em layers
    ids = {n["id"] for n in d.get("nodes", [])} | {m["id"] for m in d.get("meshes", [])}
    for e in d.get("edges", []):
        assert e["from"] in ids and e["to"] in ids, f"edge invalida: {e}"
    layer_ids = {l["id"] for l in d.get("layers", [])}
    for m in d.get("meshes", []):
        assert m.get("layer") in layer_ids, f"mesh layer invalida: {m.get('id')}"
    for nd in d.get("nodes", []):
        assert nd.get("layer") in layer_ids, f"node layer invalida: {nd.get('id')}"
    out.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[oncologia] render3d.json EMITIDO (forma=conteudo) — corpo preservado, "
          f"{len(d.get('nodes', []))} nos (grafo do algoritmo), {len(consts)} constantes")


if __name__ == "__main__":
    sys.exit(main())
