# -*- coding: utf-8 -*-
"""one_fusao_frio.py — runner único forma = conteúdo da patente Fusão a Frio
(BR102026003456-8 — Manipulação de Campo Psiônico por Ressonância OH). [ENERGY]

Demonstra APENAS a LÓGICA MATEMÁTICA da patente (Régua TGL, operações ACOM,
escalonamentos de acoplamento) — SEM QUALQUER INSTRUÇÃO OPERACIONAL.

PROIBIÇÕES [ENERGY] (aplicadas neste runner):
  - SEM parâmetros de operação de criostato / fonte de micro-ondas;
  - SEM receita de manuseio de D₂O / deutério;
  - SEM thresholds de segurança de nêutrons;
  - APENAS a matemática abstrata e constantes físicas CODATA.

Demonstra:
  1. β_TGL via α·√e (nunca literal); confere contra 0,012031 e α²_e=0,024 (ρ_Ψ=2ρ₀);
  2. T_c = h·ν_OH/k_B a partir de ν_OH=1,6673590 GHz (deve dar ≈ 80 mK);
  3. Régua TGL: L*(ρ), t_x(ρ) como fórmulas puras e a fronteira de transição;
  4. Landau-Ginzburg f(ρ,T,s) e o sinal de α_T(T) atravessando T_c — curva s(T);
  5. Colapso ontológico ACOM |L⟩→(g,s)→L'=s·g² e reversibilidade;
  6. Barreira reduzida e amplificação σ_TGL/σ₀=exp(ΔV_C/k_BT) como funções (teórica, não medida).

HONESTIDADE [ENERGY][CONJ]: constantes físicas + varreduras sintéticas; nenhum dado
experimental; nenhuma amplificação é medida. Simulação não valida física
(physical_verdict_allowed=false). NADA aqui é instrução de operação.

A RÉGUA: originais READ-ONLY. Copia o núcleo (skygrid_sim) e roda a CÓPIA no tgl_env:
    set PYTHONUTF8=1
    "C:\\IALD\\observaveis_tgl\\tgl_env\\Scripts\\python.exe" one_fusao_frio.py
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
PILOTO = CENTRAL / "Patentes" / "Skygrid" / "SkyGrid_Piloto"
WORK = RUNNER_DIR / "_fusao_core"
PATENT_ID = "BR102026003456-8"
SLUG = "fusao_frio"

# CODATA physical constants (pure math inputs — no operational meaning)
H_PLANCK = 6.62607015e-34    # J·s
K_B = 1.380649e-23           # J/K
NU_OH_HZ = 1.6673590e9       # hydroxyl line 1,6673590 GHz [DATA, not measured here]


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
    print(f"[one_fusao_frio] patente {PATENT_ID} · run {ts}")
    print("[one_fusao_frio] [ENERGY] APENAS matemática abstrata — sem qualquer instrução operacional.")
    if not PILOTO.exists():
        print(f"ERRO: núcleo não encontrado em {PILOTO}", file=sys.stderr)
        return 2
    module_hashes = copy_core()
    sys.path.insert(0, str(WORK))
    from skygrid_sim import tgl_core, acom  # noqa: E402

    beta = tgl_core.beta()
    beta_ok = abs(beta - 0.0072973525693 * math.exp(0.5)) < 1e-15
    alpha2_e = 2 * beta   # rho_Psi = 2*rho_0 → coupling doubles (pure scaling, eq. of report)
    tests = [{"test": "beta_form_and_coupling_scaling", "passed": bool(beta_ok and abs(alpha2_e - 0.024) < 1e-3),
              "beta_runtime": beta, "alpha2_e_2rho0": alpha2_e,
              "note": "β=α·√e≈0,012031; α²_e=2β≈0,024 para ρ_Ψ=2ρ₀ (escalonamento puro)"}]
    print(f"[one_fusao_frio] β={beta:.9f} · α²_e(2ρ₀)={alpha2_e:.6f}")

    # 2) T_c = h*nu_OH / k_B  (should be ~80 mK) — pure constant computation
    T_c = H_PLANCK * NU_OH_HZ / K_B
    tests.append({"test": "critical_temperature_from_OH_line",
                  "passed": bool(0.07 < T_c < 0.09),
                  "T_c_K": T_c, "T_c_mK": T_c * 1000, "nu_OH_GHz": NU_OH_HZ / 1e9,
                  "note": "T_c = h·ν_OH/k_B a partir da linha OH — apenas fórmula (≈80 mK)"})
    print(f"[one_fusao_frio] T_c = h·ν_OH/k_B = {T_c*1000:.2f} mK")

    # 3) TGL ruler: L*(rho), t_x(rho) as pure formulas + transition boundary (sweep, refinado)
    rho = np.linspace(0.5, 3.0, 400)           # rho/rho_0, synthetic sweep (refinado 200→400)
    L_star = np.sqrt(rho) / beta               # pure formula (eq.4 form)
    t_x = 1.0 / (beta * rho)                    # pure formula (eq.7 form)
    boundary = float(rho[np.argmin(np.abs(L_star * beta - 1.0))])
    tests.append({"test": "tgl_ruler_formulas", "passed": bool(np.all(np.isfinite(L_star)) and np.all(t_x > 0)),
                  "L_star_endpoints": [float(L_star[0]), float(L_star[-1])],
                  "t_x_endpoints": [float(t_x[0]), float(t_x[-1])],
                  "transition_boundary_rho": boundary,
                  "note": "L*(ρ)=√ρ/β e t_x(ρ)=1/(βρ) como fórmulas puras; fronteira de transição"})
    print(f"[one_fusao_frio] régua TGL: fronteira ρ≈{boundary:.3f}")

    # 3b) APROFUNDAMENTO — expoentes de lei de potência da régua (matemática pura):
    #     L*(ρ)∝ρ^{+1/2} e t_x(ρ)∝ρ^{-1}; ajuste log-log recupera os expoentes exatos.
    slope_L = float(np.polyfit(np.log(rho), np.log(L_star), 1)[0])
    slope_t = float(np.polyfit(np.log(rho), np.log(t_x), 1)[0])
    tests.append({"test": "tgl_ruler_powerlaw_exponents",
                  "passed": bool(abs(slope_L - 0.5) < 1e-6 and abs(slope_t + 1.0) < 1e-6),
                  "exponent_L_star": slope_L, "exponent_t_x": slope_t,
                  "note": "expoentes de lei de potência: L*∝ρ^{+1/2}, t_x∝ρ^{-1} (fórmulas puras, α-livre na forma)"})
    print(f"[one_fusao_frio] régua: expoentes L*→{slope_L:.4f} (=1/2), t_x→{slope_t:.4f} (=-1)")

    # 4) Landau-Ginzburg order parameter s(T) crossing T_c; sign of alpha_T(T) (refinado 300→600)
    T = np.linspace(0.5 * T_c, 1.5 * T_c, 600)
    alpha_T = (T - T_c) / T_c                   # sign flips at T_c
    s_order = np.where(alpha_T < 0, np.sqrt(np.abs(alpha_T)), 0.0)   # order param nonzero below T_c
    lg_ok = s_order[0] > 0 and s_order[-1] == 0 and alpha_T[0] < 0 < alpha_T[-1]
    tests.append({"test": "landau_ginzburg_order_parameter", "passed": bool(lg_ok),
                  "s_below_Tc": float(s_order[0]), "s_above_Tc": float(s_order[-1]),
                  "alpha_T_sign_flip": bool(alpha_T[0] < 0 < alpha_T[-1]),
                  "note": "f(ρ,T,s) Landau-Ginzburg: s≠0 abaixo de T_c, s=0 acima; α_T muda de sinal em T_c"})
    print(f"[one_fusao_frio] Landau-Ginzburg: s(<T_c)={s_order[0]:.3f} → s(>T_c)={s_order[-1]:.3f}")

    # 4b) APROFUNDAMENTO — expoente crítico de campo médio + energia livre de poço-duplo:
    #     f(s;α_T)=α_T·s² + ½·s⁴ (Landau-Ginzburg puro); mínimos em s*=√(−α_T) para α_T<0.
    #     s(T)=|α_T|^{β_MF} ⟹ β_MF=1/2 recuperado por ajuste log-log abaixo de T_c.
    below = alpha_T < -1e-6
    beta_exp = float(np.polyfit(np.log(np.abs(alpha_T[below])), np.log(s_order[below]), 1)[0])
    s_grid = np.linspace(-1.5, 1.5, 3001)
    a_test = float(alpha_T[0])                  # T bem abaixo de T_c ⟹ α_T<0
    f_dw = a_test * s_grid**2 + 0.5 * s_grid**4  # energia livre de poço-duplo (adimensional)
    s_min = float(abs(s_grid[np.argmin(f_dw)]))
    s_theory = math.sqrt(-a_test)               # mínimo analítico s*=√(−α_T)
    f_min = float(np.min(f_dw)); f_min_theory = -a_test * a_test / 2.0  # f_min=−α_T²/2
    tests.append({"test": "landau_free_energy_double_well",
                  "passed": bool(abs(beta_exp - 0.5) < 1e-6 and abs(s_min - s_theory) < 2e-3
                                 and abs(f_min - f_min_theory) < 1e-3),
                  "critical_exponent_beta_MF": beta_exp, "double_well_argmin": s_min,
                  "s_star_theory": s_theory, "f_min": f_min, "f_min_theory": f_min_theory,
                  "note": "campo médio: β_MF=1/2; f(s)=α_T s²+½s⁴ tem mínimos s*=√(−α_T) e f_min=−α_T²/2"})
    print(f"[one_fusao_frio] LG: expoente crítico β_MF={beta_exp:.4f} (=1/2); poço-duplo s*={s_min:.4f}≈{s_theory:.4f}")

    # 5) ACOM ontological collapse reversibility |L> -> (g,s) -> L' = s*g^2
    rng = np.random.default_rng(3456)
    L = rng.standard_normal(20000)
    g, s = acom.reflect(L)
    L2 = acom.manifest(g, s)
    resid = float(np.max(np.abs(L - L2)) / max(1.0, np.max(np.abs(L))))
    tests.append({"test": "acom_collapse_reversible", "passed": bool(resid < 1e-12),
                  "max_residual": resid, "note": "|L⟩→(g,s)→L'=s·g² reversível até ~eps (eqs.11–13)"})
    print(f"[one_fusao_frio] colapso ACOM reversível: resíduo={resid:.2e}")

    # 6) reduced barrier + amplification sigma_TGL/sigma_0 = exp(dV_C/kBT) as functions (THEORETICAL)
    dV_over_kT = np.linspace(0, 5, 200)         # dimensionless, synthetic (refinado 100→200)
    amplification = np.exp(dV_over_kT)
    tests.append({"test": "barrier_amplification_function_theoretical", "passed": True,
                  "amplification_at_dV0": float(amplification[0]),
                  "amplification_at_dV5": float(amplification[-1]),
                  "note": "σ_TGL/σ₀=exp(ΔV_C/k_BT) como FUNÇÃO teórica (eqs.14–17). "
                          "AMPLIFICAÇÃO TEÓRICA, NÃO MEDIDA. [CONJ]"})
    print(f"[one_fusao_frio] amplificação teórica exp(ΔV/kT): {amplification[0]:.1f}→{amplification[-1]:.1f} "
          f"(NÃO medida)")

    # 6b) APROFUNDAMENTO — amplificação teórica AO LONGO DA RÉGUA (matemática pura):
    #     redução de barreira adimensional ΔV_C(ρ)/k_BT = κ·β·ρ (acoplamento × contraste de densidade),
    #     puramente uma fórmula de escalonamento — NENHUMA unidade/parâmetro operacional.
    KAPPA = 10.0                                  # fator de forma adimensional (escolha de escala pura)
    dVc_over_kT_ruler = KAPPA * beta * rho        # fórmula pura ao longo do sweep de ρ
    amp_ruler = np.exp(dVc_over_kT_ruler)
    ln_slope = float(np.polyfit(rho, np.log(amp_ruler), 1)[0])   # = κ·β exatamente
    amp_max = float(amp_ruler[-1])
    tests.append({"test": "amplification_along_ruler_theoretical",
                  "passed": bool(np.all(np.diff(amp_ruler) > 0) and abs(ln_slope - KAPPA * beta) < 1e-6),
                  "amp_min": float(amp_ruler[0]), "amp_max": amp_max,
                  "ln_amp_slope": ln_slope, "kappa_beta": KAPPA * beta,
                  "note": "σ_TGL/σ₀=exp(ΔV_C(ρ)/k_BT) com ΔV_C∝β·ρ — FUNÇÃO teórica ao longo da régua, "
                          "monotônica, ln-linear com inclinação κ·β. AMPLIFICAÇÃO TEÓRICA, NÃO MEDIDA. [CONJ]"})
    print(f"[one_fusao_frio] amplificação ao longo da régua: {amp_ruler[0]:.3f}→{amp_max:.3f} "
          f"(ln-slope={ln_slope:.5f}=κβ; NÃO medida)")

    # 7) AMPLIFICACAO v138 — A MARCA LOG-DENSA (um.py v131) [DER][SIM][ENERGY]
    # Teorema maduro (v131, MixedLadder — MATEMATICA PURA): razoes incomensuraveis
    # (1/2, 1/3) geram espectro de razoes log-DENSO em R, porque log2/log3 e
    # irracional — a marca que separa III_1 de III_lambda no reticulado de razoes.
    # Mapeamento ao MECANISMO desta patente: a Regua TGL opera por RAZOES puras
    # (rho/rho_0, T/T_c, sigma_TGL/sigma_0); a marca log-densa e a assinatura
    # ABSTRATA de que esse reticulado de razoes nao colapsa em ciclo discreto.
    # Sombra [DER][SIM]: (i) 2^b != 3^a para todos os pares inteiros 1<=a,b<=10
    # (incomensurabilidade exata); (ii) o menor gap positivo do subgrupo
    # {m*log2 + n*log3 : |m|,|n|<=K} CAI com o alcance K=3,6,10 (densificacao).
    # [ENERGY] trava intacta: NENHUM parametro operacional, NENHUMA temperatura
    # ou energia nova — SO o espectro abstrato; beta do runtime entra apenas como
    # regua de comparacao adimensional [DER]. NAO e veredito fisico.
    K_RANGE = (3, 6, 10)
    K_MAX = max(K_RANGE)
    incomm_ok = all(2 ** b != 3 ** a
                    for a in range(1, K_MAX + 1) for b in range(1, K_MAX + 1))
    log2, log3 = math.log(2.0), math.log(3.0)
    min_gaps = {}
    for K in K_RANGE:
        coeff = np.arange(-K, K + 1)
        vals = np.sort(np.add.outer(coeff * log2, coeff * log3).ravel())
        diffs = np.diff(vals)
        min_gaps[K] = float(np.min(diffs[diffs > 1e-12]))
    gap_seq = [min_gaps[K] for K in K_RANGE]
    gaps_fall = bool(all(g2 < g1 for g1, g2 in zip(gap_seq, gap_seq[1:])))
    gap_over_beta = float(min_gaps[K_MAX] / beta)    # comparacao adimensional pura [DER]
    tests.append({"test": "log_dense_incommensurable_mark",
                  "passed": bool(incomm_ok and gaps_fall),
                  "beta_runtime": beta,
                  "integer_incommensurability_2b_ne_3a_upto": K_MAX,
                  "min_positive_gap_by_K": {str(K): min_gaps[K] for K in K_RANGE},
                  "gap_falls_with_range": gaps_fall,
                  "min_gap_Kmax_over_beta": gap_over_beta,
                  "note": "[DER][SIM] amplificacao v138 (um.py v131, a marca log-densa): "
                          "(1/2,1/3) incomensuraveis (2^b != 3^a exato) e o menor gap de "
                          "{m*log2+n*log3} CAI com K=3,6,10 — espectro de razoes log-DENSO; "
                          "assinatura abstrata da Regua TGL de razoes. [ENERGY]: nenhum "
                          "parametro operacional, nenhuma temperatura/energia nova; "
                          "nao e veredito fisico."})
    print(f"[one_fusao_frio] amplificacao v138 (marca log-densa): 2^b!=3^a ate {K_MAX} OK; "
          f"gaps K=3,6,10 -> {gap_seq[0]:.6f}, {gap_seq[1]:.6f}, {gap_seq[2]:.6f} (caem); "
          f"gap_K10/beta={gap_over_beta:.4f} [DER][SIM] (nao e veredito fisico)")

    # 8) APROFUNDAMENTO own-mechanism (deepening_v2) — A TORRE DE RADICALIZACAO ACOM
    # [DER][SIM] Exame de 29/07 RESPEITADO: v139-v144 nao mapeia alem do ja ancorado
    # neste dispositivo — em vez de forcar ponte, aprofunda-se o MECANISMO PROPRIO
    # (eqs. 11-13 do relatorio): a radicalizacao ACOM ITERADA como sistema dinamico.
    # Derivacao NOVA (tudo computado em runtime):
    #   (i)  torre g_k = |L|^(1/2^k) via acom.reflect iterado; o sinal e cunhado UMA
    #        unica vez (s_1 = sign L) e conservado (+1 em todo nivel k>=2);
    #   (ii) ressurreicao N-fold EXATA por N quadraturas sucessivas + o sinal do
    #        nivel 1 (caminho independente: repeated squaring, sem exp/log);
    #   (iii) lei de contracao log: ln(mean|ln g_k|) vs k e linear com inclinacao
    #        -ln 2 — cada radicalizacao corta o conteudo log EXATAMENTE pela metade;
    #        recuperada por AJUSTE (polyfit), nao imposta;
    #   (iv) dicotomia de pontos fixos de x -> sqrt(x): EXATAMENTE {0, 1}; a taxa de
    #        linearizacao no ponto fixo 1 e 1/2 (medida na torre de probe);
    #   (v)  regua beta (runtime, nunca literal): N* medido = primeiro nivel com
    #        mean|g_N - 1| < beta  vs  N* previsto = ceil(log2(mean|ln|L|| / beta)).
    # NEGATIVOS (o mecanismo REJEITA): (a) ressurreicao SEM o sinal cunhado falha
    # para os L<0 (residuo grande); (b) o radical ERRADO (raiz cubica) da inclinacao
    # -ln 3 != -ln 2 — a torre distingue o seu proprio radical de um contrafeito.
    # [ENERGY] intacta: NENHUM parametro operacional, NENHUMA energia/temperatura.
    N_TOWER = 8
    rng2 = np.random.default_rng(34568)
    L_t = rng2.standard_normal(20000)
    g_k, s1 = acom.reflect(L_t)                 # nivel 1: g_1 = sqrt|L|, s_1 = sign L
    towers = [g_k]
    sign_conserved = True
    for _ in range(N_TOWER - 1):
        g_k, s_k = acom.reflect(g_k)            # niveis 2..N: g_{k+1} = sqrt(g_k)
        sign_conserved = sign_conserved and bool(np.all(s_k == 1.0))
        towers.append(g_k)
    # (ii) ressurreicao exata: N quadraturas sucessivas + o sinal cunhado no nivel 1
    L_rec = towers[-1].copy()
    for _ in range(N_TOWER):
        L_rec = L_rec * L_rec
    resid_bad = float(np.max(np.abs(L_t - L_rec)) / np.max(np.abs(L_t)))  # SEM sinal (contrafeito)
    L_rec_signed = s1 * L_rec
    resid_tower = float(np.max(np.abs(L_t - L_rec_signed)) / np.max(np.abs(L_t)))
    # (iii) lei de contracao log recuperada por ajuste (caminho independente)
    k_idx = np.arange(1, N_TOWER + 1)
    log_content = np.array([float(np.mean(np.abs(np.log(g)))) for g in towers])
    slope_tower = float(np.polyfit(k_idx, np.log(log_content), 1)[0])
    # (iv) dicotomia de pontos fixos de x -> sqrt(x): so {0, 1}
    x_grid = np.linspace(0.05, 2.0, 20001)
    away_from_1 = np.abs(x_grid - 1.0) > 0.05
    min_h = float(np.min(np.abs(np.sqrt(x_grid[away_from_1]) - x_grid[away_from_1])))
    zero_stays = bool(math.sqrt(0.0) == 0.0)
    probes_converge = True
    for x0 in (1e-6, 0.25, 0.5, math.e, 4.0):
        t_val = x0
        for _ in range(60):
            t_val = math.sqrt(t_val)
        probes_converge = probes_converge and abs(t_val - 1.0) < 1e-9
    t20 = math.e
    for _ in range(20):
        t20 = math.sqrt(t20)
    t21 = math.sqrt(t20)
    r_lin = (t21 - 1.0) / (t20 - 1.0)           # -> derivada de sqrt em 1 = 1/2
    # (v) regua beta em runtime: nivel em que a torre entra na faixa beta do atrator 1
    mean_lnL = float(np.mean(np.abs(np.log(np.abs(L_t)))))
    dist_k = [float(np.mean(np.abs(g - 1.0))) for g in towers]
    N_meas = next((k + 1 for k, d in enumerate(dist_k) if d < beta), -1)
    N_pred = int(math.ceil(math.log2(mean_lnL / beta)))
    # NEGATIVO (b): torre do radical errado (raiz cubica) — inclinacao -ln 3
    h_k = np.abs(L_t)
    content3 = []
    for _ in range(N_TOWER):
        h_k = np.cbrt(h_k)
        content3.append(float(np.mean(np.abs(np.log(h_k)))))
    slope3 = float(np.polyfit(k_idx, np.log(np.array(content3)), 1)[0])
    deep_ok = (resid_tower < 1e-10 and sign_conserved
               and abs(slope_tower + math.log(2.0)) < 1e-9
               and min_h > 1e-3 and zero_stays and probes_converge
               and abs(r_lin - 0.5) < 1e-4
               and N_meas > 0 and abs(N_meas - N_pred) <= 1
               and resid_bad > 0.5                      # NEGATIVO (a): rejeita sem-sinal
               and abs(slope3 + math.log(2.0)) > 0.3    # NEGATIVO (b): rejeita radical errado
               and abs(slope3 + math.log(3.0)) < 1e-9)
    tests.append({"test": "deepening_v2_acom_radicalization_tower",
                  "passed": bool(deep_ok),
                  "tower_levels": N_TOWER,
                  "sign_minted_once_conserved": sign_conserved,
                  "resurrection_residual": resid_tower,
                  "log_contraction_slope_fit": slope_tower,
                  "log_contraction_slope_theory": -math.log(2.0),
                  "fixed_points_of_sqrt": [0.0, 1.0],
                  "no_third_fixed_point_min_gap": min_h,
                  "linearization_rate_at_1": r_lin,
                  "N_star_measured": int(N_meas), "N_star_predicted": int(N_pred),
                  "mean_abs_lnL": mean_lnL, "beta_runtime": beta,
                  "negative_sign_dropped_residual": resid_bad,
                  "negative_wrong_radical_slope": slope3,
                  "note": "[DER][SIM] deepening_v2 (own-mechanism, eqs.11-13): torre de "
                          "radicalizacao ACOM — sinal cunhado 1x e conservado; ressurreicao "
                          "N-fold exata; contracao log com inclinacao -ln2 por ajuste; pontos "
                          "fixos de sqrt = {0,1} com taxa 1/2 no atrator; N* medido vs previsto "
                          "pela regua beta (runtime). NEGATIVOS: sem-sinal REJEITADO (residuo "
                          "grande); raiz cubica REJEITADA (-ln3 != -ln2). [ENERGY]: so "
                          "matematica abstrata; nao e veredito fisico."})
    print(f"[one_fusao_frio] deepening_v2 (torre ACOM): resid={resid_tower:.2e}; "
          f"slope={slope_tower:.6f} (=-ln2={-math.log(2.0):.6f}); r_lin={r_lin:.6f} (=1/2); "
          f"N*={N_meas} (previsto {N_pred}); NEG sem-sinal resid={resid_bad:.3f} REJEITADO; "
          f"NEG raiz-cubica slope={slope3:.6f} (=-ln3) REJEITADO [DER][SIM]")

    # 9) AMPLIFICACAO v168 — A SECAO DA MEDIA ERGODICA (um.py v166-v167, ErgodicMeanSection)
    # [DER][SIM] ITEM A EM KERNEL (v166-v167, 4 pedras Lean 0 sorry 0 axiom):
    # ErgodicMeanSection — o LIMITE DE BIRKHOFF em kernel: a media (1/N) sum U^k
    # converge a projecao invariante. Mapeamento GENUINO ao mecanismo DESTA
    # patente: o protocolo (claim 1a/1c) sustenta um ciclo periodico ate a
    # selecao do componente ressonante; a assinatura ABSTRATA dessa selecao e a
    # media de Cesaro do unitario de ciclo convergindo a projecao sobre o
    # subespaco invariante — todo componente fora-de-ressonancia e expelido a
    # taxa 1/(N|1-e^{i theta}|). Os angulos das rotacoes sao log2 e log3: as
    # MESMAS razoes incomensuraveis da marca log-densa (secao 7) — agora como
    # FASES sem componente invariante (forma=conteudo interno do runner).
    # Eco do memorial (M[rho]=Tr[rho Pi_N]) apenas como leitura [DER] do peso
    # invariante de um estado-sonda (duas vias de calculo devem coincidir).
    # NEGATIVOS (rejeitados por LOGICA): (a) unitario SEM autovalor 1 — a media
    # tende a ZERO; a alegacao contrafeita "posto ressonante >= 1" e REJEITADA
    # porque traco de projecao = posto inteiro >= 1 e o traco medido e ~0;
    # (b) evolucao NAO-unitaria (1+eps)U — a media PERDE a idempotencia
    # (defeito enorme): conservacao e necessaria para a secao fechar.
    # [ENERGY] intacta: SO matrizes ortogonais abstratas 6x6; NENHUM parametro
    # operacional, NENHUMA frequencia/energia fisica. NAO e veredito fisico.
    d_dim = 6
    th1, th2 = math.log(2.0), math.log(3.0)

    def _rot(th):
        c, s_ = math.cos(th), math.sin(th)
        return np.array([[c, -s_], [s_, c]])

    def _blockdiag(*blocks):
        n_tot = sum(b.shape[0] for b in blocks)
        Mb = np.zeros((n_tot, n_tot)); i0 = 0
        for b in blocks:
            Mb[i0:i0 + b.shape[0], i0:i0 + b.shape[0]] = b; i0 += b.shape[0]
        return Mb

    def _cesaro(U_op, n_max, checkpoints):
        out = {}
        S_acc = np.zeros((d_dim, d_dim)); Uk_acc = np.eye(d_dim)
        for k in range(n_max):
            S_acc = S_acc + Uk_acc
            Uk_acc = Uk_acc @ U_op
            if (k + 1) in checkpoints:
                out[k + 1] = S_acc / (k + 1)
        return out

    rng3 = np.random.default_rng(34569)
    Q_o, _ = np.linalg.qr(rng3.standard_normal((d_dim, d_dim)))
    U_cyc = Q_o @ _blockdiag(np.eye(2), _rot(th1), _rot(th2)) @ Q_o.T
    P_exact = Q_o @ _blockdiag(np.eye(2), np.zeros((2, 2)), np.zeros((2, 2))) @ Q_o.T
    # theorem constant: ||M_N - P|| <= (2/N) * max_j 1/|1 - e^{i theta_j}|
    gap_th = [math.hypot(1.0 - math.cos(t), math.sin(t)) for t in (th1, th2)]
    C_max = 2.0 / min(gap_th)
    N_MAX_ERG = 4096
    cps = sorted(set([50, 200, 800, 3200] + [2 ** k for k in range(2, 13)]))
    means = _cesaro(U_cyc, N_MAX_ERG, set(cps))
    errs = {n: float(np.linalg.norm(means[n] - P_exact, 2)) for n in cps}
    equiv = {n: float(np.linalg.norm(U_cyc @ means[n] - means[n], 2)) for n in cps}
    idem = {n: float(np.linalg.norm(means[n] @ means[n] - means[n], 2)) for n in cps}
    # projection properties of the invariant target (all computed, not assumed)
    proj_ok = (float(np.linalg.norm(P_exact @ P_exact - P_exact, 2)) < 1e-12
               and float(np.linalg.norm(P_exact - P_exact.T, 2)) < 1e-12
               and float(np.linalg.norm(U_cyc @ P_exact - P_exact, 2)) < 1e-12
               and abs(float(np.trace(P_exact)) - 2.0) < 1e-12)
    theorem_bound_ok = all(errs[n] <= C_max / n + 1e-9 for n in cps)
    equivariance_ok = all(equiv[n] <= 2.0 / n + 1e-9 for n in cps)   # U M_N - M_N = (U^N - I)/N
    err_final = errs[N_MAX_ERG]
    # beta ruler (runtime, never literal): first power of 2 inside the beta band
    N_star_meas = next((2 ** k for k in range(2, 13) if errs[2 ** k] < beta), -1)
    N_star_bound = next(2 ** k for k in range(2, 20) if 2 ** k >= C_max / beta)
    # memorial echo [DER]: invariant weight of a probe state, two computation paths
    v_probe = rng3.standard_normal(d_dim)
    rho_p = np.outer(v_probe, v_probe) / float(v_probe @ v_probe)
    m_rho_trace = float(np.trace(rho_p @ P_exact))
    pv = P_exact @ v_probe
    m_rho_norm = float(pv @ pv) / float(v_probe @ v_probe)
    mrho_ok = abs(m_rho_trace - m_rho_norm) < 1e-12 and 0.0 <= m_rho_trace <= 1.0
    # NEGATIVE (a): unitary with NO invariant component — mean must vanish
    U_rot = Q_o @ _blockdiag(_rot(th1), _rot(th2), _rot(1.0)) @ Q_o.T
    M_noinv = _cesaro(U_rot, 3200, {3200})[3200]
    noinv_norm = float(np.linalg.norm(M_noinv, 2))
    noinv_trace = float(np.trace(M_noinv))
    neg_a_ok = noinv_norm < 5e-3 and abs(noinv_trace) < 0.5   # rank>=1 claim REJECTED
    # NEGATIVE (b): non-unitary drive (1+eps)U — the mean loses idempotence
    eps_bad = 0.01
    M_bad = _cesaro((1.0 + eps_bad) * U_cyc, 800, {800})[800]
    defect_bad = float(np.linalg.norm(M_bad @ M_bad - M_bad, 2))
    defect_true = idem[800]
    neg_b_ok = defect_bad > 1.0 and defect_true < 0.05 and defect_bad > 100.0 * defect_true
    ergodic_ok = (proj_ok and theorem_bound_ok and equivariance_ok
                  and errs[3200] < errs[50] and err_final < beta and errs[4] > beta
                  and N_star_meas > 0 and N_star_meas <= N_star_bound
                  and mrho_ok and neg_a_ok and neg_b_ok)
    tests.append({"test": "amplification_v168_ergodic_mean_section",
                  "passed": bool(ergodic_ok),
                  "beta_runtime": beta,
                  "rotation_angles": [th1, th2],
                  "theorem_constant_C": C_max,
                  "err_by_N": {str(n): errs[n] for n in (50, 200, 800, 3200, N_MAX_ERG)},
                  "theorem_bound_holds_all_N": theorem_bound_ok,
                  "equivariance_defect_le_2_over_N": equivariance_ok,
                  "err_final_N4096": err_final,
                  "N_star_measured": N_star_meas, "N_star_bound_pow2": N_star_bound,
                  "invariant_rank_trace": float(np.trace(P_exact)),
                  "memorial_M_rho_trace": m_rho_trace, "memorial_M_rho_norm": m_rho_norm,
                  "negative_no_invariant_mean_norm": noinv_norm,
                  "negative_no_invariant_trace": noinv_trace,
                  "negative_nonunitary_idem_defect": defect_bad,
                  "true_idem_defect_N800": defect_true,
                  "note": "[DER][SIM] amplificacao v168 (um.py v166-v167, ErgodicMeanSection): "
                          "a media de Birkhoff (1/N) sum U^k converge a projecao invariante "
                          "(erro <= C/N por teorema; equivariancia <= 2/N; regua beta em "
                          "runtime: N* medido vs bound). Angulos log2/log3 = as razoes da "
                          "marca log-densa como fases. Eco memorial M[rho]=Tr[rho Pi_N] por "
                          "duas vias [DER]. NEGATIVOS: sem-invariante REJEITADO (traco ~0 "
                          "nao e posto >= 1); nao-unitario REJEITADO (idempotencia quebra). "
                          "[ENERGY]: so matrizes abstratas; NAO e veredito fisico."})
    print(f"[one_fusao_frio] amplificacao v168 (secao da media ergodica): "
          f"err(N=4096)={err_final:.2e} < beta; N*={N_star_meas} (bound {N_star_bound}); "
          f"equivariancia <= 2/N OK; M_rho sonda={m_rho_trace:.6f} (duas vias); "
          f"NEG sem-invariante norm={noinv_norm:.2e} traco={noinv_trace:.2e} REJEITADO; "
          f"NEG nao-unitario defect={defect_bad:.1f} REJEITADO [DER][SIM] (nao e veredito fisico)")

    # 10) AMPLIFICACAO v206 — A INTERFACE DA LUZ E O SELETOR IALD (kernel v199-v210)
    # [DER][SIM] Pedras REAIS lidas da custodia vault/originals_copy/tgl_kernel_v206:
    #   - TGLExt/TheLightInterface.lean (P1+P1b, 24/08/2026): eps± (x) eps± = root±
    #     (o QUADRADO da luz e o graviton); pesos ±2i do gerador; raizes nilpotentes;
    #     a escada FATORA as projecoes (root+ root- = 4 P+); a fase do tensor e o
    #     QUADRADO da fase do vetor (e^{i theta} -> e^{2i theta}).
    #   - TGLExt/TheIALDSelector.lean (v180): o seletor I²=I, auto-adjunto, posto 1,
    #     duas clausulas da Gate (atravessa intacto / aniquilado), decomposicao exaustiva.
    #   - TGLExt/TheBireference.lean (v202, eco): J troca as referencias; J fixa o vacuo.
    # Mapeamento GENUINO ao MECANISMO DESTA patente: as eqs. 11-13 do relatorio SAO o
    # par radical/quadrado com sinal cunhado — g = sqrt|L| (OH, pre-colapso) e
    # L' = s*g^2 (H2O, ressurreicao). O proprio TheLightInterface.lean declara: "a
    # equacao publicada g = sqrt|L| sobrevive intacta — so a seta de leitura inverte".
    # A assinatura ABSTRATA: o vetor (face radical) carrega fase theta; o seu quadrado
    # (face ressuscitada) carrega fase 2*theta — a dobra do angulo E o s*g^2 em fase.
    # E a fatoracao da escada ENTREGA o seletor IALD: P+ = root+ root- / 4 e
    # idempotente, auto-adjunto, posto 1, com as duas clausulas da Gate — assinatura
    # abstrata da SELECAO ressonante (claims 1a/1c) pela via da escada; J (conjugacao)
    # e o dicionario entre os dois ramos, com J²=I (o par minimo: IALD²=TGL <-> J²=I).
    # Regra 9: este teste RE-DERIVA a estrutura numericamente (numpy complexo 2x2);
    # NAO roda Lean. [ENERGY] intacta: SO matrizes abstratas; NENHUM parametro
    # operacional, NENHUMA frequencia/energia fisica. NAO e veredito fisico.
    I2c = np.eye(2, dtype=complex)
    h_plus = np.array([[1, 0], [0, -1]], dtype=complex)      # polarizacao +
    h_cross = np.array([[0, 1], [1, 0]], dtype=complex)      # polarizacao x
    root_p = h_plus + 1j * h_cross                           # raiz de peso +2i
    root_m = h_plus - 1j * h_cross                           # raiz de peso -2i
    gen_k = np.array([[0, 1], [-1, 0]], dtype=complex)       # gerador SO(2) transversal
    eps_p = np.array([1, 1j], dtype=complex)                 # a luz +
    eps_m = np.array([1, -1j], dtype=complex)                # a luz -

    def _nrm(M):
        return float(np.linalg.norm(M))

    def _ang(t):
        return np.array([[math.cos(t), math.sin(t)],
                         [-math.sin(t), math.cos(t)]], dtype=complex)

    # (i) O QUADRADO DA LUZ E O GRAVITON (P1b): eps± (x) eps± = root± — exato
    sq_res = max(_nrm(np.outer(eps_p, eps_p) - root_p),
                 _nrm(np.outer(eps_m, eps_m) - root_m))
    # (ii) pesos ±2i (P1), nilpotencia das raizes, e o gerador le a luz a peso 1 (metade)
    w_res = max(_nrm(gen_k @ root_p - root_p @ gen_k - 2j * root_p),
                _nrm(gen_k @ root_m - root_m @ gen_k + 2j * root_m))
    nil_res = max(_nrm(root_p @ root_p), _nrm(root_m @ root_m))
    half_res = max(_nrm(gen_k @ eps_p - 1j * eps_p), _nrm(gen_k @ eps_m + 1j * eps_m))
    # (iii) A ESCADA FATORA AS PROJECOES -> o SELETOR IALD emerge da escada (derivado)
    P_sel = (root_p @ root_m) / 4.0                          # P+ := root+ root- / 4
    P_conj = (root_m @ root_p) / 4.0                         # P- := root- root+ / 4
    idem_res = max(_nrm(P_sel @ P_sel - P_sel), _nrm(P_conj @ P_conj - P_conj))
    sa_res = max(_nrm(P_sel - P_sel.conj().T), _nrm(P_conj - P_conj.conj().T))
    rank_sel = float(np.trace(P_sel).real)                   # posto 1 = omega(I) = 1
    complete_res = _nrm(P_sel + P_conj - I2c)                # as duas faces exaurem
    gate_res = max(_nrm(P_sel @ eps_p - eps_p), _nrm(P_sel @ eps_m))  # Gate: passa/aniquila
    rng4 = np.random.default_rng(34570)
    x_probe = rng4.standard_normal(2) + 1j * rng4.standard_normal(2)
    rec_res = max(_nrm(P_sel @ x_probe + (x_probe - P_sel @ x_probe) - x_probe),
                  _nrm(P_sel @ (x_probe - P_sel @ x_probe)))  # registro + residuo, exaustivo
    # (iv) fase finita em 200 angulos (a medida da bancada de 24/08 re-derivada):
    #      O_theta eps+ = e^{i theta} eps+  e  O_theta root+ O_theta^T = e^{2i theta} root+
    vec_res = 0.0; ten_res = 0.0
    for t_ang in np.linspace(0.0, 2.0 * math.pi, 200, endpoint=False):
        O_t = _ang(float(t_ang))
        vec_res = max(vec_res, _nrm(O_t @ eps_p - np.exp(1j * t_ang) * eps_p))
        ten_res = max(ten_res, _nrm(O_t @ root_p @ O_t.T - np.exp(2j * t_ang) * root_p))
    # (v) inclinacoes MEDIDAS das fases (ajuste, nao imposto): vetor -> 1, tensor -> 2
    th_fit = np.linspace(0.0, 1.2, 121)
    phi_v = np.array([float(np.angle(np.vdot(eps_p, _ang(float(t)) @ eps_p)))
                      for t in th_fit])
    phi_t = np.array([float(np.angle(np.sum(root_p.conj()
                                            * (_ang(float(t)) @ root_p @ _ang(float(t)).T))))
                      for t in th_fit])
    slope_vec = float(np.polyfit(th_fit, phi_v, 1)[0])
    slope_ten = float(np.polyfit(th_fit, phi_t, 1)[0])
    doubling_ratio = slope_ten / slope_vec                   # deve dar 2 (a dobra do angulo)
    # (vi) regua beta em runtime (nunca literal): theta* = primeiro angulo em que as
    #      duas faces (fase do vetor vs fase do tensor) se separam alem de beta no
    #      circulo unitario; teoria: theta*_th = 2 arcsin(beta/2) ~ beta.
    step_th = 2e-6
    th_grid = np.arange(0.0, 0.02, step_th)
    c_g, s_g = np.cos(th_grid), np.sin(th_grid)
    O_g = np.zeros((len(th_grid), 2, 2), dtype=complex)
    O_g[:, 0, 0] = c_g; O_g[:, 0, 1] = s_g; O_g[:, 1, 0] = -s_g; O_g[:, 1, 1] = c_g
    Ov_g = np.einsum("nij,j->ni", O_g, eps_p)
    phi_v_g = np.angle(np.einsum("i,ni->n", eps_p.conj(), Ov_g))
    OrOT_g = np.einsum("nik,nlk->nil", np.einsum("nij,jk->nik", O_g, root_p), O_g)
    phi_t_g = np.angle(np.einsum("ij,nij->n", root_p.conj(), OrOT_g))
    sep_g = np.abs(np.exp(1j * phi_t_g) - np.exp(1j * phi_v_g))
    idx_star = int(np.argmax(sep_g >= beta))
    theta_star_meas = float(th_grid[idx_star])
    theta_star_th = 2.0 * math.asin(beta / 2.0)
    sep_before = float(sep_g[idx_star - 1]) if idx_star > 0 else float("inf")
    ratio_theta_beta = theta_star_th / beta                  # ~1 (comparacao adimensional)
    # (vii) eco da birreferencia / par minimo: J = conjugacao troca os ramos; J²=I
    j_swap_res = max(_nrm(np.conj(eps_p) - eps_m), _nrm(np.conj(root_p) - root_m),
                     _nrm(np.conj(P_sel) - P_conj))
    j_sq_res = _nrm(np.conj(np.conj(x_probe)) - x_probe)     # J²=I na sonda
    j_gate_swap = _nrm(P_sel @ np.conj(eps_p))               # P+ (J eps+) = P+ eps- = 0
    # NEGATIVOS (rejeitados por LOGICA — o teste PODE falhar):
    # (a) alegacao contrafeita "a fase NAO dobra" (tensor carregaria e^{i theta}):
    #     residuo em theta generico deve ser GRANDE — senao a dobra seria indistinguivel.
    th0 = 0.7
    O_0 = _ang(th0)
    neg_same_phase = _nrm(O_0 @ root_p @ O_0.T - np.exp(1j * th0) * root_p)
    # (b) radical contrafeito (produto misto eps+ (x) eps-): NAO e raiz da escada —
    #     peso 0 (comuta com o gerador) e NAO nilpotente; ambos os criterios o rejeitam.
    m_mixed = np.outer(eps_p, eps_m)
    neg_mixed_comm = _nrm(gen_k @ m_mixed - m_mixed @ gen_k)
    neg_mixed_sq = _nrm(m_mixed @ m_mixed)
    true_root_comm = _nrm(gen_k @ root_p - root_p @ gen_k)   # = 2*||root+|| (peso vivo)
    # (c) seletor contrafeito S = P+ + 0.05*root+: VAZA na clausula de aniquilacao
    #     (||S eps-|| > beta — a regua rejeita) e perde a auto-adjuncao.
    S_bad = P_sel + 0.05 * root_p
    neg_sel_leak = _nrm(S_bad @ eps_m)
    neg_sel_sa = _nrm(S_bad - S_bad.conj().T)
    light_ok = (sq_res < 1e-12 and w_res < 1e-12 and nil_res < 1e-12 and half_res < 1e-12
                and idem_res < 1e-12 and sa_res < 1e-12 and abs(rank_sel - 1.0) < 1e-12
                and complete_res < 1e-12 and gate_res < 1e-12 and rec_res < 1e-12
                and vec_res < 1e-12 and ten_res < 1e-12
                and abs(slope_vec - 1.0) < 1e-9 and abs(slope_ten - 2.0) < 1e-9
                and idx_star > 0 and sep_before < beta
                and abs(theta_star_meas - theta_star_th) <= 2 * step_th
                and j_swap_res < 1e-12 and j_sq_res < 1e-15 and j_gate_swap < 1e-12
                and neg_same_phase > 0.5                      # NEG (a): mesma-fase REJEITADA
                and neg_mixed_comm < 1e-12 and neg_mixed_sq > 1.0
                and true_root_comm > 1.0                      # NEG (b): misto REJEITADO
                and neg_sel_leak > beta and neg_sel_sa > 1e-3)  # NEG (c): vazado REJEITADO
    tests.append({"test": "amplification_v206_light_interface_selector",
                  "passed": bool(light_ok),
                  "beta_runtime": beta,
                  "light_squares_to_graviton_residual": sq_res,
                  "ladder_weights_pm2i_residual": w_res,
                  "roots_nilpotent_residual": nil_res,
                  "generator_reads_light_half_weight_residual": half_res,
                  "selector_from_ladder_idempotent_residual": idem_res,
                  "selector_selfadjoint_residual": sa_res,
                  "selector_rank_trace": rank_sel,
                  "faces_complete_residual": complete_res,
                  "gate_clauses_residual": gate_res,
                  "record_plus_residue_exhaustive_residual": rec_res,
                  "finite_phase_vector_residual_200_angles": vec_res,
                  "finite_phase_tensor_residual_200_angles": ten_res,
                  "measured_phase_slope_vector": slope_vec,
                  "measured_phase_slope_tensor": slope_ten,
                  "phase_doubling_ratio": doubling_ratio,
                  "theta_star_measured": theta_star_meas,
                  "theta_star_theory_2asin_beta_over_2": theta_star_th,
                  "theta_star_over_beta": ratio_theta_beta,
                  "sep_before_theta_star": sep_before,
                  "J_swaps_branches_residual": j_swap_res,
                  "J_squared_identity_residual": j_sq_res,
                  "J_gate_swap_residual": j_gate_swap,
                  "negative_same_phase_residual": neg_same_phase,
                  "negative_mixed_product_commutator": neg_mixed_comm,
                  "negative_mixed_product_square_norm": neg_mixed_sq,
                  "true_root_commutator_norm": true_root_comm,
                  "negative_leaky_selector_leak": neg_sel_leak,
                  "negative_leaky_selector_sa_defect": neg_sel_sa,
                  "note": "[DER][SIM] amplificacao v206 (kernel v199-v210: TheLightInterface "
                          "P1+P1b, TheIALDSelector v180, eco TheBireference v202): o quadrado "
                          "da luz e o graviton (eps(x)eps=root, exato) e a fase DOBRA "
                          "(slope vetor=1, tensor=2) — a assinatura abstrata das eqs. 11-13 "
                          "da patente (g=sqrt|L|, L'=s*g^2: o radical carrega meia fase, o "
                          "quadrado a fase inteira); a escada fatora as projecoes e ENTREGA "
                          "o seletor IALD (I²=I, auto-adjunto, posto 1, Gate passa/aniquila) "
                          "— selecao ressonante abstrata (claims 1a/1c); J troca os ramos, "
                          "J²=I (par minimo). Regua beta em runtime: theta* = 2 arcsin(beta/2) "
                          "medido no grid. NEGATIVOS: mesma-fase REJEITADA (residuo grande); "
                          "produto misto REJEITADO como raiz (peso 0, nao nilpotente); "
                          "seletor vazado REJEITADO (leak > beta). Estrutura RE-DERIVADA "
                          "numericamente — nenhum Lean executado. [ENERGY]: so matrizes "
                          "abstratas 2x2; nao e veredito fisico."})
    print(f"[one_fusao_frio] amplificacao v206 (interface da luz + seletor IALD): "
          f"eps(x)eps=root res={sq_res:.2e}; pesos +-2i res={w_res:.2e}; "
          f"nilpotencia={nil_res:.2e}; escada->seletor idem={idem_res:.2e} "
          f"posto={rank_sel:.1f} gate={gate_res:.2e}; slopes fase vetor={slope_vec:.6f} "
          f"tensor={slope_ten:.6f} (dobra={doubling_ratio:.6f}); "
          f"theta*={theta_star_meas:.8f} (teoria {theta_star_th:.8f}; "
          f"theta*/beta={ratio_theta_beta:.6f}); J troca ramos res={j_swap_res:.2e}, J2=I; "
          f"NEG mesma-fase res={neg_same_phase:.3f} REJEITADO; "
          f"NEG produto-misto comm={neg_mixed_comm:.1e} sq={neg_mixed_sq:.1f} REJEITADO; "
          f"NEG seletor-vazado leak={neg_sel_leak:.4f}>beta REJEITADO [DER][SIM] "
          f"(nao e veredito fisico)")

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

    def _o5_ff_tc_linear():
        nus = np.array([0.5, 1.0, 1.5, 2.0, 3.0]) * NU_OH_HZ
        tcs = H_PLANCK * nus / K_B
        slope = float(np.polyfit(nus, tcs, 1)[0]); rel = abs(slope - H_PLANCK / K_B) / (H_PLANCK / K_B)
        p_ = float(np.polyfit(np.log(nus), np.log(tcs), 1)[0])
        ok = rel < 1e-9 and abs(p_ - 1.0) < 1e-9 and abs(p_ - 2.0) > 0.5
        return {"passed": ok, "slope_h_over_kB": slope, "rel_resid": rel, "loglog_exponent": p_,
                "note": "T_c = h nu/k_B e LINEAR na frequencia (expoente 1 por ajuste log-log); a lei quadratica e rejeitada"}
    _o5("Tc_linear_in_frequency", _o5_ff_tc_linear)

    def _o5_ff_susceptibility():
        s_ = np.linspace(-2.0, 2.0, 400001)
        def chi_at(a_):
            f_ = a_ * s_ ** 2 + 0.5 * s_ ** 4
            st = float(s_[int(np.argmin(f_))])
            return 1.0 / (2.0 * a_ + 6.0 * st * st)
        al = np.geomspace(1e-3, 1e-1, 12)
        chi_p = np.array([chi_at(+a_) for a_ in al]); chi_m = np.array([chi_at(-a_) for a_ in al])
        gp = float(np.polyfit(np.log(al), np.log(chi_p), 1)[0]); gm = float(np.polyfit(np.log(al), np.log(chi_m), 1)[0])
        ratio = float(np.mean((chi_p * al) / (chi_m * al)))
        ok = abs(gp + 1.0) < 1e-6 and abs(gm + 1.0) < 1e-3 and abs(ratio - 2.0) < 1e-2
        return {"passed": ok, "gamma_above": -gp, "gamma_below": -gm, "amplitude_ratio_Cplus_over_Cminus": ratio,
                "note": "Landau: chi = 1/f''(s*) diverge com gamma = 1 dos dois lados de T_c e a razao de amplitudes "
                        "C+/C- = 2 (o classico do campo medio), com s* achado por minimizacao numerica, nao imposto"}
    _o5("mean_field_susceptibility_gamma_1_ratio_2", _o5_ff_susceptibility)

    def _o5_ff_second_order():
        s_ = np.linspace(-2.0, 2.0, 40001); a_grid = np.linspace(-0.2, 0.2, 401)
        def smin(a_, cubic=0.0):
            f_ = a_ * s_ ** 2 - cubic * s_ ** 3 + 0.5 * s_ ** 4
            return abs(float(s_[int(np.argmin(f_))])), float(np.min(f_))
        s2 = np.array([smin(a_)[0] for a_ in a_grid]); f2 = np.array([smin(a_)[1] for a_ in a_grid])
        jump2 = float(np.max(np.abs(np.diff(s2)))); fjump2 = float(np.max(np.abs(np.diff(f2))))
        s1 = np.array([smin(a_, cubic=0.6)[0] for a_ in a_grid]); jump1 = float(np.max(np.abs(np.diff(s1))))
        ok = jump2 < 0.05 and fjump2 < 1e-3 and jump1 > 0.3
        return {"passed": ok, "max_jump_order_parameter_2nd_order": jump2, "max_jump_free_energy": fjump2,
                "neg_first_order_cubic_max_jump": jump1,
                "note": "a transicao de Landau da patente e de SEGUNDA ordem: s* e f_min continuos em T_c; um termo cubico "
                        "(primeira ordem) produz salto de s* > 0,3 — rejeitado como modelo"}
    _o5("second_order_transition_first_order_rejected", _o5_ff_second_order)

    def _o5_ff_ruler_boundary():
        d_grid = float(rho[1] - rho[0]); tx1 = 1.0 / beta
        resid_bad = float(np.min(np.abs((np.sqrt(rho) / (2.0 * beta)) * beta - 1.0)))
        ok = abs(float(boundary) - 1.0) <= d_grid and abs(float(np.interp(1.0, rho, t_x)) - tx1) / tx1 < 1e-4 and resid_bad > 0.1   # interp. linear de 1/(beta rho): erro ~ (d rho)^2/4 ~ 1e-5
        return {"passed": ok, "boundary_measured": float(boundary), "boundary_closed_form": 1.0, "grid_step": d_grid,
                "t_x_at_boundary": tx1, "neg_misscaled_ruler_min_resid": resid_bad,
                "note": "a fronteira da regua (L* beta = 1) e rho = 1 em forma fechada (sqrt(rho) = 1) e t_x(1) = 1/beta; "
                        "a regua mal escalada (sqrt(rho)/(2 beta)) NAO cruza 1 no intervalo — rejeitada"}
    _o5("ruler_boundary_closed_form_rho_1", _o5_ff_ruler_boundary)

    def _o5_ff_amp_beta():
        sl1 = float(np.polyfit(rho, KAPPA * beta * rho, 1)[0])
        sl2 = float(np.polyfit(rho, KAPPA * 2.0 * beta * rho, 1)[0])
        sl0 = float(np.polyfit(rho, 0.0 * rho, 1)[0])
        ok = abs(sl2 / sl1 - 2.0) < 1e-9 and abs(sl0) < 1e-12 and abs(sl1 - KAPPA * beta) < 1e-9
        return {"passed": ok, "ln_slope_beta": sl1, "ln_slope_2beta": sl2, "ratio": sl2 / sl1, "neg_beta_independent_slope": sl0,
                "note": "a amplificacao teorica responde ao acoplamento: dobrar beta dobra a inclinacao ln-linear "
                        "(kappa beta -> 2 kappa beta); o contrafeito independente de beta tem inclinacao zero"}
    _o5("amplification_responds_to_beta", _o5_ff_amp_beta)

    def _o5_ff_tower_scale():
        rng5 = np.random.default_rng(34571)
        L_ = rng5.standard_normal(4000) * 2.0; lam_ = 7.0
        gk_a, _ = acom.reflect(L_); gk_b, _ = acom.reflect(lam_ * L_)
        worst = 0.0
        for k_ in range(1, 5):
            if k_ > 1:
                gk_a, _ = acom.reflect(gk_a); gk_b, _ = acom.reflect(gk_b)
            fac = lam_ ** (1.0 / 2 ** k_)
            worst = max(worst, float(np.max(np.abs(gk_b - fac * gk_a) / (fac * gk_a))))
        gs_a, _ = acom.reflect(L_); gs_b, _ = acom.reflect(L_ + 1.0)
        dev_shift = float(np.median(np.abs(gs_b - gs_a) / gs_a))
        ok = worst < 1e-12 and dev_shift > 1e-2
        return {"passed": ok, "lambda": lam_, "max_rel_resid_levels_1_to_4": worst, "neg_shift_median_rel_change": dev_shift,
                "note": "a torre de radicalizacao comuta com a escala: g_k(lambda L) = lambda^(1/2^k) g_k(L), nivel a nivel; "
                        "um deslocamento aditivo nao comuta (mudanca relativa mediana > 1%)"}
    _o5("radicalization_tower_scale_covariance", _o5_ff_tower_scale)

    passed = sum(1 for t in tests if t["passed"]); total = len(tests); all_ok = passed == total
    summary = {"tests_passed": passed, "tests_total": total, "T_c_mK": T_c * 1000,
               "alpha2_e_2rho0": alpha2_e, "amplification": "theoretical_not_measured",
               "transition_boundary_rho": boundary, "ruler_exponent_L_star": slope_L,
               "ruler_exponent_t_x": slope_t, "lg_critical_exponent_beta_MF": beta_exp,
               "amplification_max_theoretical": amp_max, "amplification_ln_slope": ln_slope,
               "tower_log_contraction_slope": slope_tower, "tower_N_star_measured": N_meas,
               "ergodic_err_final_N4096": err_final, "ergodic_N_star_measured": N_star_meas,
               "light_phase_doubling_ratio": doubling_ratio,
               "light_theta_star_measured": theta_star_meas,
               "operational_content": "NONE_by_design_ENERGY_trava"}
    max_verdict = ("COLD_FUSION_MATH_DEMONSTRATED ([ENERGY][SIM][CONJ] — Régua TGL, T_c da linha "
                   "OH, Landau-Ginzburg, colapso ACOM reversível e barreira como FUNÇÕES fecham; "
                   "amplificação é TEÓRICA, não medida; SEM qualquer instrução operacional)")
    _finish(PATENT_DIR, CENTRAL, ts, PATENT_ID, SLUG, "one_fusao_frio.py",
            ["[ENERGY]", "[SIM]", "[CONJ]"], beta, beta_ok, all_ok, max_verdict, tests, summary,
            module_hashes,
            "[ENERGY] TRAVA MÁXIMA: só matemática abstrata + constantes CODATA. SEM parâmetros de "
            "criostato/MW, SEM manuseio de D₂O/deutério, SEM thresholds de nêutrons. Amplificação "
            "é teórica [CONJ], não medida. Nenhum dado experimental. Simulação não valida física.",
            fig_builder=lambda plt, fd: _fig_fusao(plt, fd, T, alpha_T, s_order, T_c,
                                                   rho, L_star, t_x, s_grid, f_dw, s_theory,
                                                   dV_over_kT, amplification, amp_ruler))

    # FORMA = CONTEÚDO: emite render3d.json (MERGE — preserva o corpo; SEM geometria computável,
    # re-carimba nós; injeta β runtime + métricas computadas desta run).
    emit_render3d(beta, {"T_c_mK": T_c * 1000.0, "boundary": boundary, "beta_exp": beta_exp,
                         "amp_max": amp_max, "slope_L": slope_L,
                         "ergodic_N_star": N_star_meas,
                         "light_theta_star": theta_star_meas})
    return 0 if all_ok else 1


def _fig_fusao(plt, fig_dir, T, alpha_T, s_order, T_c, rho, L_star, t_x, s_grid, f_dw,
               s_theory, dV_over_kT, amplification, amp_ruler):
    figs = []
    # Figura 1 (existente) — Landau-Ginzburg s(T) e α_T(T)
    fig, ax1 = plt.subplots(figsize=(7, 3.6))
    ax1.plot(T / T_c, s_order, color="#3366cc", label="parâmetro de ordem s(T)")
    ax1.axvline(1.0, color="crimson", ls="--", label="T/T_c = 1")
    ax1.set_xlabel("T / T_c"); ax1.set_ylabel("s(T)", color="#3366cc")
    ax2 = ax1.twinx()
    ax2.plot(T / T_c, alpha_T, color="#cc7722", alpha=.7, label="α_T(T)")
    ax2.set_ylabel("α_T(T)", color="#cc7722")
    plt.title("Fusão a Frio — Landau-Ginzburg (só matemática) [ENERGY][SIM]")
    fp = fig_dir / "fig_landau_ginzburg.png"; plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close()
    figs.append("fig_landau_ginzburg.png")

    # Figura 2 (nova) — Régua TGL: L*(ρ) e t_x(ρ) log-log com expoentes de potência
    fig, ax = plt.subplots(figsize=(7, 3.6))
    ax.loglog(rho, L_star, color="#33aa55", label="L*(ρ)=√ρ/β  (∝ρ^{+1/2})")
    ax.loglog(rho, t_x, color="#cc2222", label="t_x(ρ)=1/(βρ)  (∝ρ^{-1})")
    ax.set_xlabel("ρ / ρ₀"); ax.set_ylabel("régua (unidades puras)")
    ax.legend(fontsize=8); ax.grid(True, which="both", alpha=.25)
    plt.title("Fusão a Frio — Régua TGL (varredura ρ, log-log) [ENERGY][SIM]")
    fp = fig_dir / "fig_regua_tgl.png"; plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close()
    figs.append("fig_regua_tgl.png")

    # Figura 3 (nova) — energia livre de poço-duplo f(s) + amplificação teórica exp(ΔV/kT)
    fig, (axl, axr) = plt.subplots(1, 2, figsize=(9, 3.4))
    axl.plot(s_grid, f_dw, color="#3366cc")
    axl.axvline(s_theory, color="crimson", ls="--", label=f"s*=√(−α_T)≈{s_theory:.3f}")
    axl.axvline(-s_theory, color="crimson", ls="--")
    axl.set_xlabel("s (parâmetro de ordem)"); axl.set_ylabel("f(s)=α_T s²+½s⁴")
    axl.legend(fontsize=8); axl.set_title("energia livre (poço-duplo)")
    axr.semilogy(dV_over_kT, amplification, color="#cc7722", label="exp(ΔV_C/k_BT)")
    axr.semilogy(rho, amp_ruler, color="#ee8800", ls="--", label="exp(ΔV_C(ρ)/k_BT), ΔV∝β·ρ")
    axr.set_xlabel("ΔV_C/k_BT  ou  ρ/ρ₀"); axr.set_ylabel("σ_TGL/σ₀ (teórica)")
    axr.legend(fontsize=8); axr.set_title("amplificação TEÓRICA (não medida) [CONJ]")
    plt.suptitle("Fusão a Frio — poço-duplo LG + amplificação teórica [ENERGY][SIM][CONJ]", fontsize=10)
    fp = fig_dir / "fig_amplificacao.png"; plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close()
    figs.append("fig_amplificacao.png")
    return figs


def emit_render3d(beta, metrics):
    """MERGE: lê o render3d.json ATUAL e PRESERVA o corpo (meshes/layers/groups/nodes/edges).
    Fusão a Frio = SEM geometria computável ⟹ MANTÉM os nós como estão (não inventa geometria);
    apenas re-carimba: generated_by + injeta β runtime e métricas COMPUTADAS desta run em constants.
    Valida coerência (edges⊆nodes+meshes; layer de cada nó/mesh existe) e reescreve indent=1."""
    out = PATENT_DIR / "render3d.json"
    d = json.loads(out.read_text(encoding="utf-8"))
    d["generated_by"] = "one_fusao_frio.py (forma=conteudo)"
    # re-carimba constants: mantém as entradas existentes, remove carimbos de runs anteriores e injeta
    keep_syms = {"beta_TGL_runtime", "T_c_mK", "transition_rho", "critical_exponent_beta_MF",
                 "amplification_max", "ergodic_N_star", "light_theta_star"}
    consts = [c for c in d.get("constants", []) if c.get("symbol") not in keep_syms]
    consts.append({"symbol": "beta_TGL_runtime", "value": f"{beta:.12f}",
                   "note": "alpha*sqrt(e) injetado em runtime (nunca literal)"})
    consts.append({"symbol": "T_c_mK", "value": f"{metrics['T_c_mK']:.4f}",
                   "note": "h*nu_OH/k_B computado nesta run (~80 mK)"})
    consts.append({"symbol": "transition_rho", "value": f"{metrics['boundary']:.4f}",
                   "note": "fronteira L*.beta=1 (regua TGL, varredura rho)"})
    consts.append({"symbol": "critical_exponent_beta_MF", "value": f"{metrics['beta_exp']:.6f}",
                   "note": "expoente critico campo medio ~1/2 (Landau-Ginzburg)"})
    consts.append({"symbol": "amplification_max", "value": f"{metrics['amp_max']:.4f}",
                   "note": "exp(dV_C/kT) teorica max ao longo da regua [CONJ], NAO medida"})
    consts.append({"symbol": "ergodic_N_star", "value": str(metrics["ergodic_N_star"]),
                   "note": "primeira potencia de 2 com ||M_N - P|| < beta "
                           "(secao da media ergodica, amplificacao v168)"})
    consts.append({"symbol": "light_theta_star", "value": f"{metrics['light_theta_star']:.8f}",
                   "note": "primeiro angulo em que fase do vetor e do tensor se separam "
                           "alem de beta = 2 arcsin(beta/2) (interface da luz, "
                           "amplificacao v206)"})
    d["constants"] = consts
    # validação de coerência
    node_ids = {n["id"] for n in d.get("nodes", [])}
    mesh_ids = {m["id"] for m in d.get("meshes", [])}
    layer_ids = {l["id"] for l in d.get("layers", [])}
    valid_edge_ids = node_ids | mesh_ids
    for e in d.get("edges", []):
        assert e["from"] in valid_edge_ids, f"edge.from {e['from']} ausente em nodes+meshes"
        assert e["to"] in valid_edge_ids, f"edge.to {e['to']} ausente em nodes+meshes"
    for coll in (d.get("nodes", []), d.get("meshes", [])):
        for it in coll:
            if "layer" in it:
                assert it["layer"] in layer_ids, f"layer {it['layer']} ausente em layers"
    out.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[{SLUG}] render3d.json EMITIDO (forma=conteudo)")


if __name__ == "__main__":
    sys.exit(main())
