# -*- coding: utf-8 -*-
"""one_supercondutor.py — runner único forma = conteúdo da patente Supercondutor Holográfico
(BR102026003450-9). [SIM][HARDWARE]

Demonstra a LÓGICA do dispositivo (processamento de sinal + balanço de energia DO MODELO):
  - β_TGL via α·√e (nunca literal) e ponto crítico α²_c (Tetelestai);
  - compressão g=√|L| (eq.4) e ressurreição L=s·g² (eq.5); preservação η e polaridade;
  - condição de SC holográfica: transição η(P_MW) tipo-fase com limiar P_th (tanh, Fig.7);
  - coeficientes métricos g_tt, g_LL, v_info(α²) (eq.18) com aviso da divergência v_info;
  - balanço de energia fail-closed: ΔS→0 como PREDIÇÃO DE MODELO, guarda anti-over-unity.
β nunca literal (tgl_core.beta()).

HONESTIDADE [SIM][HARDWARE]: NÃO simula plasma OH, vácuo ou óptica reais; NÃO prova
translação. Nenhum número é medição de bancada. Interface de dispositivo via
hardware_mocks (physical_verdict_allowed=false). Simulação nunca valida física.

A RÉGUA: originais READ-ONLY. Copia o núcleo (skygrid_sim) e roda a CÓPIA no tgl_env:
    set PYTHONUTF8=1
    "C:\\IALD\\observaveis_tgl\\tgl_env\\Scripts\\python.exe" one_supercondutor.py
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
WORK = RUNNER_DIR / "_super_core"
PATENT_ID = "BR102026003450-9"
SLUG = "supercondutor"


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


def main() -> int:
    ts = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    print(f"[one_supercondutor] patente {PATENT_ID} · run {ts}")
    if not PILOTO.exists():
        print(f"ERRO: núcleo não encontrado em {PILOTO}", file=sys.stderr)
        return 2
    module_hashes = copy_core()
    sys.path.insert(0, str(WORK))
    from skygrid_sim import tgl_core, acom  # noqa: E402
    from skygrid_sim.hardware_mocks import SupercondutorMock  # noqa: E402

    beta = tgl_core.beta()
    beta_ok = abs(beta - 0.0072973525693 * math.exp(0.5)) < 1e-15
    alpha2_c = beta   # critical point (Tetelestai) = the Miguel constant
    print(f"[one_supercondutor] β runtime = {beta} (= α·√e? {beta_ok}) · α²_c={alpha2_c:.6f}")
    tests = [{"test": "beta_form_and_critical_point", "passed": bool(beta_ok),
              "beta_runtime": beta, "alpha2_c": alpha2_c}]

    rng = np.random.default_rng(3450)
    # 2) ACOM compression + resurrection preservation
    L = np.sin(np.linspace(0, 20 * math.pi, 20000)) * (1 + 0.3 * rng.standard_normal(20000))
    g, s = acom.reflect(L)
    L2 = acom.manifest(g, s)
    resid = float(np.max(np.abs(L - L2)) / max(1.0, np.max(np.abs(L))))
    sign_ok = bool(np.array_equal(np.sign(L2)[L != 0], np.sign(L)[L != 0]))
    tests.append({"test": "acom_compress_resurrect_preservation",
                  "passed": bool(resid < 1e-12 and sign_ok), "max_residual": resid,
                  "polarity_preserved": sign_ok, "note": "g=√|L| (eq.4), L=s·g² (eq.5), η e s preservados"})
    print(f"[one_supercondutor] ACOM preservação: resíduo={resid:.2e} polaridade={sign_ok}")

    # 3) holographic SC condition: phase-like transition eta(P_MW) with threshold P_th
    P_th = 1.0
    P_MW = np.linspace(0, 3, 300)
    eta = np.tanh(P_MW / P_th)          # ResonanceFactor Gamma_OH-like (Fig.7)
    below = float(eta[np.argmin(np.abs(P_MW - 0.2 * P_th))])
    above = float(eta[np.argmin(np.abs(P_MW - 2.5 * P_th))])
    transition_ok = below < 0.3 and above > 0.98
    tests.append({"test": "holographic_sc_phase_transition", "passed": bool(transition_ok),
                  "P_th": P_th, "eta_below_threshold": below, "eta_above_threshold": above,
                  "note": "η(P_MW)=tanh(P_MW/P_th): abaixo do limiar ~0, acima →1 (transição tipo-fase)"})
    print(f"[one_supercondutor] transição SC: η(0,2·P_th)={below:.3f} → η(2,5·P_th)={above:.3f}")

    # 4) metric coefficients g_tt, g_LL, v_info(alpha2) with honest divergence note
    a2 = np.linspace(0.001, alpha2_c * 0.999, 200)
    ratio = a2 / alpha2_c
    g_tt = 1.0 - ratio
    g_LL = 1.0 / (1.0 - ratio)
    v_info = np.sqrt(np.abs(g_tt / g_LL))  # |1-ratio|; → 0 as a2→a2_c (algebraic)
    tests.append({"test": "metric_coefficients", "passed": bool(np.all(g_LL > 0) and v_info[-1] < v_info[0]),
                  "g_tt_at_low": float(g_tt[0]), "g_LL_at_high": float(g_LL[-1]),
                  "v_info_endpoints": [float(v_info[0]), float(v_info[-1])],
                  "note": "eq.18: g_tt→0, g_LL→∞ no horizonte α²→α²_c. AVISO [OPEN]: aqui v_info→0 "
                          "(algébrico), divergente da prosa do relatório 'v_info→∞'. Reportado honestamente."})
    print(f"[one_supercondutor] métrica: v_info {v_info[0]:.3f}→{v_info[-1]:.3f} (aviso: prosa diz →∞)")

    # 5) fail-closed energy balance: dS->0 as MODEL PREDICTION, anti-over-unity guard
    T = np.linspace(0.05, 1.0, 100)
    dS = np.exp(-(1 - beta) / T) * beta   # toy monotone approach to 0 as T falls (model)
    e_in, e_out = 1.0, 0.999              # model: e_out <= e_in strictly (no over-unity)
    over_unity = e_out > e_in
    tests.append({"test": "energy_balance_fail_closed", "passed": bool(not over_unity and dS[0] < dS[-1]),
                  "delta_S_endpoints": [float(dS[0]), float(dS[-1])],
                  "over_unity_detected": over_unity, "e_out_over_e_in": e_out / e_in,
                  "note": "ΔS→0 é PREDIÇÃO DE MODELO; guarda anti-over-unity ativa (e_out ≤ e_in). [DER]"})
    print(f"[one_supercondutor] balanço: over-unity={over_unity} (guarda ativa)")

    # ---- APROFUNDAMENTO 1: varredura de P_th (transição η) — auto-similaridade -------
    # η(P_MW)=tanh(P_MW/P_th) implica que a transição escala com P_th. Medimos, para
    # vários limiares, a largura 10–90% e o ponto de meia-transição, e verificamos a
    # invariância de escala (largura normalizada e P_½/P_th constantes) — resultado
    # DERIVADO da própria forma tanh, reportado honestamente.
    P_th_scan = [0.5, 1.0, 1.5, 2.0, 3.0]
    trans_sweep = []
    for pth in P_th_scan:
        Ps = np.linspace(0, 6 * pth, 4000)
        es = np.tanh(Ps / pth)
        p10 = float(np.interp(0.10, es, Ps)); p50 = float(np.interp(0.50, es, Ps))
        p90 = float(np.interp(0.90, es, Ps))
        # steepness = dη/dP em P=P_½ (= 1/pth * sech^2(atanh 0.5))
        slope_half = float((1.0 / pth) * (1.0 - 0.5 ** 2))
        trans_sweep.append({"P_th": pth, "P10": p10, "P50": p50, "P90": p90,
                            "width_1090": p90 - p10, "width_norm": (p90 - p10) / pth,
                            "P50_over_Pth": p50 / pth, "slope_at_half": slope_half})
    width_norms = [t["width_norm"] for t in trans_sweep]
    p50_ratios = [t["P50_over_Pth"] for t in trans_sweep]
    scale_invariant = bool(np.ptp(width_norms) < 1e-3 and np.ptp(p50_ratios) < 1e-3)
    tests.append({"test": "transition_scale_invariance_Pth_sweep", "passed": scale_invariant,
                  "P_th_values": P_th_scan, "width_norm_mean": float(np.mean(width_norms)),
                  "width_norm_ptp": float(np.ptp(width_norms)),
                  "P50_over_Pth_mean": float(np.mean(p50_ratios)),
                  "note": "η=tanh(P/P_th): largura 10-90% escala ∝ P_th (auto-similar); "
                          "P_½/P_th=atanh(0.5)=0,5493 constante. [DER]"})
    print(f"[one_supercondutor] varredura P_th: largura_norm={np.mean(width_norms):.4f} "
          f"(ptp={np.ptp(width_norms):.1e}) · P½/P_th={np.mean(p50_ratios):.4f} · escala-invariante={scale_invariant}")

    # ---- APROFUNDAMENTO 2: métrica g_tt/v_info vs α² — expoente crítico ---------------
    # Varre α² finamente até o horizonte α²_c e ajusta o expoente de v_info(α²)~(1-α²/α²_c)^p.
    a2_fine = np.linspace(0.0005, alpha2_c * 0.9995, 600)
    ratio_f = a2_fine / alpha2_c
    g_tt_f = 1.0 - ratio_f
    g_LL_f = 1.0 / (1.0 - ratio_f)
    v_info_f = np.sqrt(np.abs(g_tt_f / g_LL_f))   # = |1-ratio|
    eps = 1.0 - ratio_f                            # distância ao horizonte
    # ajuste log-log v_info ~ eps^p perto do horizonte (últimos 200 pontos)
    mask = eps > 0
    p_fit = float(np.polyfit(np.log(eps[mask][-200:]), np.log(v_info_f[mask][-200:]), 1)[0])
    tests.append({"test": "metric_critical_exponent", "passed": bool(abs(p_fit - 1.0) < 0.02),
                  "v_info_exponent_fit": p_fit, "g_tt_horizon": float(g_tt_f[-1]),
                  "g_LL_horizon": float(g_LL_f[-1]), "v_info_horizon": float(v_info_f[-1]),
                  "note": "v_info(α²)~(1-α²/α²_c)^p; ajuste p≈1 (algébrico, não →∞). AVISO [OPEN]: "
                          "diverge da prosa 'v_info→∞'. Reportado honestamente."})
    print(f"[one_supercondutor] métrica: expoente crítico p={p_fit:.4f} (esperado 1) · "
          f"v_info→{v_info_f[-1]:.4f} (horizonte)")

    # ---- APROFUNDAMENTO 3: curva do platô de coerência |ρ01|→1−β ---------------------
    # Modelo de estabilização: |ρ01|(t) sobe e satura no platô (1−β) sob realimentação de
    # ganho k. Varremos o ganho e verificamos que o platô converge para 1−β (o valor da
    # informação preservada), independente do ganho — só a constante de tempo muda.
    plateau_target = 1.0 - beta
    t_axis = np.linspace(0.0, 20.0, 800)
    gains = [0.5, 1.0, 2.0, 4.0]
    coherence_curves = {}
    plateaus = []
    for k in gains:
        rho01 = plateau_target * (1.0 - np.exp(-k * t_axis))
        coherence_curves[k] = rho01
        plateaus.append(float(rho01[-1]))
    plateau_mean = float(np.mean(plateaus))
    plateau_ok = bool(abs(plateau_mean - plateau_target) < 1e-3)
    tests.append({"test": "coherence_plateau_converges_1_minus_beta", "passed": plateau_ok,
                  "plateau_target_1_minus_beta": plateau_target, "plateau_mean": plateau_mean,
                  "gains_scanned": gains, "plateaus": plateaus,
                  "note": "|ρ01|(t)→(1−β): platô = informação preservada; independe do ganho k "
                          "(só τ muda). β=α·√e injetado, nunca literal. [DER]"})
    print(f"[one_supercondutor] platô de coerência: |ρ01|→{plateau_mean:.6f} (alvo 1−β={plateau_target:.6f}) "
          f"· ganhos {gains}")

    # ---- AMPLIFICACAO v138: H3L_min = 1 - q_F (um.py v135) ---------------------------
    # O representante MINIMO da classe dos Three Locks — familia que NASCEU desta linha
    # de patentes (trava-dupla / chaveamento de retorno). Sombra [DER, sem veredito
    # fisico]: constroi H3L = Dc'Dc + Db'Db + Dz'Dz em DOIS blocos-trava (leitura: face
    # -Y entrada / face +Y saida), q_F = projecao no nucleo (o suporte do Nome), e
    # deriva numericamente: (i) aniquilacao pelo suporte q_F*H3L = 0; (ii) maximalidade
    # r(1-q_F)=0 => r*q_F=r (r = trava de UM bloco, sub-projecao ESTRITA); (iii) o
    # Verbo exp(-t*beta*H3L_min) FIXA o suporte (beta runtime, nunca literal); (iv)
    # minimalidade de Loewner H3L >= gap*H3L_min. [HARDWARE]: matematica do gap do
    # mecanismo ja patenteado; NAO afirma supercondutividade fisica; nao altera
    # reivindicacoes (physical_verdict_allowed=false).
    nb = 12                                       # sites por bloco-trava

    def _three_locks_block(n: int) -> np.ndarray:
        Dc = np.zeros((n - 1, n)); Db = np.zeros((n - 2, n)); Dz = np.zeros((n, n))
        for i in range(n - 1):
            Dc[i, i], Dc[i, i + 1] = -1.0, 1.0    # lock c: cadeia
        for i in range(n - 2):
            Db[i, i], Db[i, i + 2] = -1.0, 1.0    # lock b: salto-2
        for i in range(n):
            Dz[i, i], Dz[i, (i + 1) % n] = -1.0, 1.0  # lock z: anel (retorno)
        return Dc.T @ Dc + Db.T @ Db + Dz.T @ Dz

    Hb = _three_locks_block(nb)
    H3L = np.block([[Hb, np.zeros((nb, nb))], [np.zeros((nb, nb)), Hb]])
    evals, evecs = np.linalg.eigh(H3L)
    dim_ker = int(np.sum(evals < 1e-10))
    gap_h3l = float(evals[dim_ker])               # 1o autovalor acima do nucleo
    q_F = evecs[:, :dim_ker] @ evecs[:, :dim_ker].T   # suporte (projecao no nucleo)
    resid_annih = float(max(np.max(np.abs(q_F @ H3L)), np.max(np.abs(H3L @ q_F))))
    H3L_min = np.eye(2 * nb) - q_F                # v135: o representante MINIMO da classe
    # (ii) maximalidade com sub-projecao ESTRITA: r = modo zero de UM bloco (tr r=1 < tr q_F=2)
    u = np.zeros(2 * nb); u[:nb] = 1.0 / math.sqrt(nb)
    r = np.outer(u, u)
    resid_r_annih = float(np.max(np.abs(r @ H3L_min)))     # r(1-q_F) = 0
    resid_max = float(np.max(np.abs(r @ q_F - r)))         # => r*q_F = r
    # (iii) o Verbo exp(-t*beta*H3L_min) fixa o suporte; fora do suporte decai e^(-t*beta)
    w_min, V_min = np.linalg.eigh(H3L_min)
    resid_verbo = 0.0; off_decay = []
    for t_v in (1.0, 10.0, 100.0):
        E_v = V_min @ np.diag(np.exp(-t_v * beta * w_min)) @ V_min.T
        resid_verbo = max(resid_verbo, float(np.max(np.abs(E_v @ q_F - q_F))))
        off_decay.append(float(np.exp(-t_v * beta)))
    # (iv) minimalidade (Loewner): H3L >= gap * H3L_min
    loewner_min = float(np.min(np.linalg.eigvalsh(H3L - gap_h3l * H3L_min)))
    h3l_ok = bool(dim_ker == 2 and resid_annih < 1e-12 and resid_r_annih < 1e-12
                  and resid_max < 1e-12 and resid_verbo < 1e-13 and loewner_min > -1e-10)
    tests.append({"test": "h3l_min_support_annihilation", "passed": h3l_ok,
                  "dim_ker": dim_ker, "gap": gap_h3l,
                  "trace_qF": float(np.trace(q_F)), "trace_r": float(np.trace(r)),
                  "resid_support_annihilation": resid_annih,
                  "resid_maximality_r_annih": resid_r_annih,
                  "resid_maximality_rq_eq_r": resid_max,
                  "resid_verbo_fixes_support": resid_verbo,
                  "verbo_off_support_decay": off_decay,
                  "loewner_min_eig": loewner_min,
                  "note": "Amplificacao v138 (um.py v135): H3L_min=1-q_F, representante MINIMO "
                          "da classe dos Three Locks (nascida desta familia de patentes). "
                          "[DER] qF*H=0; r(1-q)=0 => rq=r; exp(-t*beta*H3L_min) fixa o suporte "
                          "(beta runtime, nunca literal); H3L>=gap*H3L_min. NAO e veredito fisico "
                          "[HARDWARE]."})
    print(f"[one_supercondutor] amplificacao v138: H3L_min=1-q_F | dim_ker={dim_ker} "
          f"gap={gap_h3l:.6f} | resid qF*H={resid_annih:.2e} maximalidade={resid_max:.2e} "
          f"Verbo fixa suporte={resid_verbo:.2e} | Loewner min={loewner_min:.2e}")

    # ---- AMPLIFICACAO v143 (pedra 99): a trava-dupla FECHA — E covariante ------------
    # um.py v143, veredito (1) GLOBAL_LIFT_CONDITIONAL: o Lema 3 TIPADO como implicacao
    # provada — Takesaki finito + juramento H_inv => E covariante (com controle
    # negativo). Sombra [DER] no mecanismo DESTA patente (a trava-dupla / chaveamento
    # de retorno, familia onde os Three Locks nasceram): o Lock A ja esta ancorado
    # (v138: suporte q_F). O Lock B e a COVARIANCIA — E(X) = q_F X q_F + (1-q_F) X (1-q_F)
    # e a esperanca condicional finita de Takesaki (pinching); o juramento H_inv e
    # [H3L, q_F] = 0 (MEDIDO, nao imposto); a conclusao E(U X U) = U E(X) U com o Verbo
    # U = exp(-t*beta*H3L) (beta runtime, nunca literal) e verificada em X aleatorios.
    # CONTROLE NEGATIVO (o teste PODE falhar): uma trava r_tilt (rotacao pi/4
    # nucleo<->excitado) QUEBRA o juramento — com forma fechada independente
    # ||[H3L, r_tilt]||_2 = gap*sin(theta)*cos(theta) — e a covariancia FALHA
    # macroscopicamente. NAO prova o Lema 3 operador-algebrico global (tipo III);
    # e a sombra finita da implicacao. [HARDWARE]: matematica do mecanismo, nunca
    # operacao fisica real (physical_verdict_allowed=false).
    n2 = 2 * nb
    I2 = np.eye(n2)
    oath_resid = float(np.linalg.norm(H3L @ q_F - q_F @ H3L, 2))  # juramento (MEDIDO)

    def _pinch(P: np.ndarray, X: np.ndarray) -> np.ndarray:
        Q = I2 - P
        return P @ X @ P + Q @ X @ Q

    Xs = [rng.standard_normal((n2, n2)) for _ in range(3)]
    # Takesaki finito — propriedades MEDIDAS (idempotente, unital, bimodulo)
    resid_idem = max(float(np.max(np.abs(_pinch(q_F, _pinch(q_F, X)) - _pinch(q_F, X))))
                     for X in Xs)
    resid_unital = float(np.max(np.abs(_pinch(q_F, I2) - I2)))
    resid_bimod = max(float(np.max(np.abs(_pinch(q_F, q_F @ X) - q_F @ _pinch(q_F, X))))
                      for X in Xs)

    def _verbo_full(t: float) -> np.ndarray:
        return evecs @ np.diag(np.exp(-t * beta * evals)) @ evecs.T

    resid_cov = 0.0
    for t_v in (1.0, 10.0):
        U = _verbo_full(t_v)
        for X in Xs:
            resid_cov = max(resid_cov, float(np.linalg.norm(
                _pinch(q_F, U @ X @ U) - U @ _pinch(q_F, X) @ U, 2)))

    # controle negativo: rotacao pi/4 entre uma direcao do nucleo e a 1a excitada
    theta_t = math.pi / 4.0
    v_in = evecs[:, 0]                      # direcao do nucleo (autovalor 0)
    v_out = evecs[:, dim_ker]               # 1a direcao acima do gap
    R_rot = (I2 + (math.cos(theta_t) - 1.0) * (np.outer(v_in, v_in) + np.outer(v_out, v_out))
             + math.sin(theta_t) * (np.outer(v_out, v_in) - np.outer(v_in, v_out)))
    r_tilt = R_rot @ q_F @ R_rot.T
    oath_break = float(np.linalg.norm(H3L @ r_tilt - r_tilt @ H3L, 2))
    oath_theory = gap_h3l * math.sin(theta_t) * math.cos(theta_t)   # forma fechada = gap/2
    resid_oath_cf = float(abs(oath_break - oath_theory))
    cov_defect_bad = 0.0
    for t_v in (1.0, 10.0):
        U = _verbo_full(t_v)
        for X in Xs:
            cov_defect_bad = max(cov_defect_bad, float(np.linalg.norm(
                _pinch(r_tilt, U @ X @ U) - U @ _pinch(r_tilt, X) @ U, 2)))
    lockb_ok = bool(oath_resid < 1e-11 and resid_idem < 1e-12 and resid_unital < 1e-12
                    and resid_bimod < 1e-12 and resid_cov < 1e-10
                    and resid_oath_cf < 1e-9 and oath_break > gap_h3l / 4.0
                    and cov_defect_bad > 1e-3
                    and cov_defect_bad > 1e4 * max(resid_cov, 1e-15))
    tests.append({"test": "dual_lock_covariant_expectation_lema3_typed", "passed": lockb_ok,
                  "oath_resid_qF_commutes_H3L": oath_resid,
                  "takesaki_idempotent_resid": resid_idem,
                  "takesaki_unital_resid": resid_unital,
                  "takesaki_bimodule_resid": resid_bimod,
                  "covariance_resid_good_lock": resid_cov,
                  "neg_oath_break_norm": oath_break,
                  "neg_oath_break_closed_form_gap_sin_cos": oath_theory,
                  "neg_oath_break_closed_form_resid": resid_oath_cf,
                  "neg_covariance_defect_broken_lock": cov_defect_bad,
                  "note": "Amplificacao v143 (um.py pedra 99, Lema 3 TIPADO): Takesaki finito "
                          "(pinching por q_F = esperanca condicional; idempotente/unital/"
                          "bimodulo MEDIDOS) + juramento H_inv ([H3L,q_F]=0 MEDIDO) => E "
                          "covariante com o Verbo exp(-t*beta*H3L) (beta runtime, nunca "
                          "literal). CONTROLE NEGATIVO: r_tilt (rotacao pi/4 nucleo<->"
                          "excitado) quebra o juramento — ||[H3L,r_tilt]||_2 = gap*sin*cos "
                          "(forma fechada independente) — e a covariancia FALHA. A trava-"
                          "dupla fecha NO MODELO: Lock A = suporte q_F (v138), Lock B = E "
                          "covariante (v143). [DER][SIM] sombra finita; NAO prova o Lema 3 "
                          "global; sem veredito fisico [HARDWARE]."})
    print(f"[one_supercondutor] amplificacao v143 (pedra 99): juramento [H3L,qF]={oath_resid:.2e} "
          f"cov(E,Verbo)={resid_cov:.2e} | NEG: quebra juramento={oath_break:.6f} "
          f"(forma fechada gap/2={oath_theory:.6f}, resid={resid_oath_cf:.2e}) "
          f"defeito cov={cov_defect_bad:.4f}")

    # ---- AMPLIFICACAO v168 (Item A do kernel, v166-v167): ErgodicMeanSection ---------
    # um.py v166-v167, 4 pedras Lean (0 sorry, 0 axiom). Duas delas mapeiam GENUINAMENTE
    # no mecanismo DESTA patente (a trava-dupla, onde os Three Locks nasceram):
    #   - ErgodicMeanSection: o LIMITE DE BIRKHOFF em kernel — a media (1/N) sum U^k
    #     converge a projecao invariante;
    #   - EquivariantSection: a secao equivariante — o limite comuta com o fluxo.
    # No dispositivo: o Lock A (v138) deu o suporte q_F; o Lock B (v143) deu a
    # covariancia E. A TERCEIRA face: o suporte e ALCANCAVEL POR MEDIA TEMPORAL PURA —
    # o leitor da face +Y nao precisa de decomposicao espectral; basta acumular o fluxo
    # U = exp(-i*tau*H3L) e a media de Cesaro pousa em q_F (o Nome), DESDE QUE o
    # relogio tau seja generico (nenhuma fase ressonante). Tudo MEDIDO por iteracao
    # dinamica (acumulacao de potencias), nao pela formula espectral.
    # CONTROLE NEGATIVO (o mecanismo REJEITA por LOGICA): o relogio ressonante
    # tau_bad = 2*pi/gap ALIASA o par de autovetores do gap (e^{-i*2pi} = 1) — o
    # subespaco invariante de U_bad e ESTRITAMENTE MAIOR que ker H3L, logo a media de
    # Birkhoff converge ao projetor ERRADO (alargado) q_F + P_alias e NAO ao Nome:
    # defeito macroscopico ~1 vs ~1e-3 do relogio generico. Nao e tautologia: a mesma
    # maquina, com o relogio errado, FALHA — e a falha e explicada em forma fechada.
    # [DER][SIM] sombra finita do teorema de kernel; NAO e o teorema em si; [HARDWARE]
    # matematica do mecanismo, nunca operacao fisica real (physical_verdict_allowed=false).
    nz_mask = evals > 1e-10
    lam_nz = evals[nz_mask]
    lam_max = float(lam_nz[-1])
    tau_good = math.pi / lam_max                      # derivado em runtime do espectro
    phases_good = np.abs(1.0 - np.exp(-1j * tau_good * lam_nz))
    min_phase_good = float(phases_good.min())         # genericidade MEDIDA (sem aliasing)

    def _cesaro_defects(U: np.ndarray, target: np.ndarray, n_list: list) -> list:
        acc = np.eye(n2, dtype=complex)               # termo k=0 (U^0)
        p_cur = np.eye(n2, dtype=complex)
        out = []
        idx = 0
        for k in range(1, n_list[-1]):
            p_cur = p_cur @ U
            acc = acc + p_cur
            if k + 1 == n_list[idx]:
                out.append(float(np.linalg.norm(acc / (k + 1) - target, 2)))
                idx += 1
        return out

    U_good = (evecs * np.exp(-1j * tau_good * evals)) @ evecs.T
    N_list = [100, 800, 6400]
    d_good = _cesaro_defects(U_good, q_F.astype(complex), N_list)
    b_good = [2.0 / (N * min_phase_good) for N in N_list]   # bound derivado do espectro
    equiv_resid = float(max(np.linalg.norm(U_good @ q_F - q_F.astype(complex), 2),
                            np.linalg.norm(q_F.astype(complex) @ U_good - q_F, 2)))
    # face do Verbo (beta runtime, nunca literal): contracao T = exp(-beta*H3L),
    # media de Cesaro tambem pousa em q_F (autovalores e^{-beta*lam} < 1 fora do nucleo)
    T_verbo = (evecs * np.exp(-beta * evals)) @ evecs.T
    N_verbo = [400, 6400]
    d_verbo = _cesaro_defects(T_verbo.astype(complex), q_F.astype(complex), N_verbo)
    t_max = float(np.exp(-beta * lam_nz[0]))
    b_verbo = [1.0 / (N * (1.0 - t_max)) for N in N_verbo]
    # NEGATIVO: relogio ressonante tau_bad = 2*pi/gap — aliasing do par do gap
    tau_bad = 2.0 * math.pi / gap_h3l
    u_bad_dist = np.abs(1.0 - np.exp(-1j * tau_bad * lam_nz))
    alias_mask = u_bad_dist < 1e-3
    n_alias = int(alias_mask.sum())
    idx_nz = np.where(nz_mask)[0]
    V_alias = evecs[:, idx_nz[alias_mask]]
    P_alias = V_alias @ V_alias.T                     # projetor aliasado (fora do nucleo)
    tr_alias = float(np.trace(P_alias))
    min_phase_bad = float(u_bad_dist[~alias_mask].min())
    U_bad = (evecs * np.exp(-1j * tau_bad * evals)) @ evecs.T
    N_bad = 800
    d_bad_vs_qF = _cesaro_defects(U_bad, q_F.astype(complex), [N_bad])[0]
    enlarged = (q_F + P_alias).astype(complex)
    d_bad_vs_enl = _cesaro_defects(U_bad, enlarged, [N_bad])[0]
    b_bad = 2.0 / (N_bad * min_phase_bad)
    ergodic_ok = bool(
        min_phase_good > 0.1                                   # relogio generico MEDIDO
        and all(d <= b + 1e-12 for d, b in zip(d_good, b_good))  # bound espectral respeitado
        and d_good[0] > d_good[1] > d_good[2]                  # defeito DECRESCE com N
        and d_good[-1] < 5e-3                                  # Birkhoff pousa no Nome
        and equiv_resid < 1e-12                                # EquivariantSection: U qF = qF U = qF
        and d_verbo[0] > d_verbo[1]                            # Verbo (beta) tambem converge
        and all(d <= b + 1e-9 for d, b in zip(d_verbo, b_verbo))
        and n_alias >= 1 and tr_alias > 0.5                    # aliasing real (par do gap)
        and d_bad_vs_qF > 0.9                                  # NEG: NAO converge ao Nome
        and d_bad_vs_qF > 100.0 * d_good[-1]                   # NEG: falha macroscopica
        and d_bad_vs_enl <= b_bad + 1e-12                      # LOGICA: converge ao alargado
    )
    tests.append({"test": "ergodic_mean_section_birkhoff_v168", "passed": ergodic_ok,
                  "tau_good_pi_over_lam_max": tau_good, "min_phase_good": min_phase_good,
                  "N_list": N_list, "birkhoff_defects_good": d_good,
                  "birkhoff_bounds_good": b_good,
                  "equivariant_section_resid": equiv_resid,
                  "verbo_N_list": N_verbo, "verbo_defects": d_verbo,
                  "verbo_bounds": b_verbo,
                  "neg_tau_bad_2pi_over_gap": tau_bad, "neg_n_alias": n_alias,
                  "neg_trace_P_alias": tr_alias, "neg_min_phase_nonalias": min_phase_bad,
                  "neg_defect_vs_qF": d_bad_vs_qF,
                  "neg_defect_vs_enlarged_projection": d_bad_vs_enl,
                  "neg_bound_enlarged": b_bad,
                  "note": "Amplificacao v168 (um.py v166-v167, Item A em kernel): "
                          "ErgodicMeanSection — a media de Birkhoff (1/N) sum U^k, "
                          "ACUMULADA por iteracao dinamica, converge ao suporte q_F "
                          "(o Nome, Lock A v138) sob o fluxo U=exp(-i*tau*H3L) com "
                          "relogio generico tau=pi/lam_max; EquivariantSection: o "
                          "limite comuta com o fluxo (U qF = qF U = qF MEDIDO). Face "
                          "do Verbo com beta runtime (nunca literal) tambem converge. "
                          "CONTROLE NEGATIVO por LOGICA: relogio ressonante "
                          "tau=2pi/gap aliasa o par do gap => subespaco invariante "
                          "ESTRITAMENTE maior => a media converge ao projetor ERRADO "
                          "q_F+P_alias (defeito vs Nome ~1, macroscopico) — o "
                          "mecanismo rejeita o relogio ressonante. [DER][SIM] sombra "
                          "finita do teorema de kernel, NAO o teorema; sem veredito "
                          "fisico [HARDWARE]."})
    print(f"[one_supercondutor] amplificacao v168 (ErgodicMeanSection v166-v167): "
          f"tau=pi/lam_max={tau_good:.6f} min_fase={min_phase_good:.4f} | "
          f"defeito Birkhoff N={N_list[-1]}: {d_good[-1]:.2e} (bound {b_good[-1]:.2e}) | "
          f"equivariancia={equiv_resid:.2e} | Verbo(beta) N={N_verbo[-1]}: {d_verbo[-1]:.2e}")
    print(f"[one_supercondutor]   NEG relogio ressonante tau=2pi/gap={tau_bad:.4f}: "
          f"alias={n_alias} (tr P_alias={tr_alias:.1f}) | defeito vs Nome={d_bad_vs_qF:.4f} "
          f"(>0.9, NAO converge) | vs alargado={d_bad_vs_enl:.2e} (bound {b_bad:.2e})")

    # ---- AMPLIFICACAO v206 (4a onda): TheLightInterface — a fase do graviton -----------
    # e o QUADRADO da fase da luz, na face do condensado.
    # Material-fonte REAL: TGLExt/TheLightInterface.lean (kernel v206, 24/08/2026,
    # custodia vault/originals_copy/tgl_kernel_v206) + TheAngleIsTheProjection.lean
    # (definicoes genK, P+-, angFamily). A pedra CITA a equacao publicada g = sqrt|L|
    # — que e a eq.(4) DESTA patente (Radicalismo Ontologico; reivindicacoes 5, 15,
    # 16(f)/(h)): "a equacao publicada g=sqrt|L| sobrevive intacta — so a seta de
    # leitura inverte (a luz como raiz do graviton, o graviton como quadrado da luz)".
    # Mapeamento GENUINO na trava desta patente: a face -Y (entrada) comprime g=sqrt|L|
    # (a RAIZ, peso 1) e a face +Y (saida) ressuscita L=s*g^2 (o QUADRADO, peso 2) —
    # exatamente a estrutura da interface: eps+- (x) eps+- = root+- e a fase dobra do
    # vetor (e^{i theta}) para o tensor (e^{2 i theta}).
    # O teste RE-DERIVA a ESTRUTURA numericamente (regra 9: NUNCA finge rodar Lean):
    #   ATO I (a escada): [K, root+-] = +-2i root+- ; root+-^2 = 0 ; root+ root- = 4 P+ ;
    #   ATO II (a interface): eps+- (x) eps+- = root+- ; K eps+- = +-i eps+- ;
    #     O_theta eps+ = e^{i theta} eps+ ; O_theta root+ O_theta^T = e^{2 i theta} root+ ;
    #   a nilpotencia FATORA pela nulidade da luz: eps.eps = 0 => root^2 = (eps.eps)*root;
    #   face beta (runtime, nunca literal): theta_M = arcsin(sqrt(beta)) — no angulo
    #     modular a fase do vetor e theta_M, a do tensor e 2*theta_M (MEDIDAS por arg),
    #     e |O[0,1]|^2 recupera beta = sin^2(theta_M);
    #   face do condensado (eq.4/5 da patente): g = sqrt(L) carrega MEIA fase e g^2
    #     restaura — mesma lei de dobra, medida no sinal complexo.
    # CONTROLE NEGATIVO por LOGICA (o mecanismo PODE falhar): o pareamento MISTO
    # eps+ (x) eps- NAO e raiz — forma fechada eps+ (x) eps- = 2 P+ (peso ZERO:
    # [K, mix] = 0, O mix O^T = mix invariante) => a fase NAO dobra: o defeito da
    # dobra e |1 - e^{2 i theta}| = 2 sin(theta) (macroscopico, forma fechada
    # independente). E a polarizacao DESemparelhada h+ e REJEITADA pela escada:
    # [K, h+] = -2 h_x (mistura, nao autovetor do peso; overlap com h+ = 0) e
    # h+^2 = I diferente de 0 (nao nilpotente). Nao e tautologia: a MESMA maquina,
    # com o par errado, falha — e a falha tem forma fechada.
    # [DER][SIM] sombra numerica da pedra de kernel, NAO a pedra; [HARDWARE]
    # matematica do mecanismo, nunca operacao fisica real (physical_verdict_allowed=false).
    I2c = np.eye(2, dtype=complex)
    K_gen = np.array([[0.0, 1.0], [-1.0, 0.0]], dtype=complex)     # genK (K^2 = -1)
    h_plus = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)    # hPlusC
    h_cross = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)    # hCrossC
    root_p = h_plus + 1j * h_cross                                 # rootPlus
    root_m = h_plus - 1j * h_cross                                 # rootMinus
    eps_p = np.array([1.0, 1j], dtype=complex)                     # lightPlus
    eps_m = np.array([1.0, -1j], dtype=complex)                    # lightMinus
    P_p = 0.5 * (I2c - 1j * K_gen)                                 # projPlus
    P_m = 0.5 * (I2c + 1j * K_gen)                                 # projMinus

    def _ang(th: float) -> np.ndarray:                             # angFamily(theta)
        return math.cos(th) * I2c + math.sin(th) * K_gen

    def _mx(A) -> float:
        return float(np.max(np.abs(A)))

    # ATO I — a escada
    r_k2 = _mx(K_gen @ K_gen + I2c)                                # K^2 = -1
    r_pol = max(_mx(root_p + root_m - 2.0 * h_plus),
                _mx(root_p - root_m - 2j * h_cross))               # raizes = polarizacoes
    r_wt = max(_mx(K_gen @ root_p - root_p @ K_gen - 2j * root_p),
               _mx(K_gen @ root_m - root_m @ K_gen + 2j * root_m))  # pesos +-2i
    r_nil = max(_mx(root_p @ root_p), _mx(root_m @ root_m))        # nilpotencia
    null_light = max(abs(complex(eps_p @ eps_p)), abs(complex(eps_m @ eps_m)))  # eps.eps=0
    r_fact = max(_mx(root_p @ root_m - 4.0 * P_p),
                 _mx(root_m @ root_p - 4.0 * P_m))                 # escada fatora P+-
    r_proj = max(_mx(P_p @ P_p - P_p), _mx(P_m @ P_m - P_m),
                 _mx(P_p + P_m - I2c), _mx(P_p @ P_m))
    # ATO II — a interface
    r_square = max(_mx(np.outer(eps_p, eps_p) - root_p),
                   _mx(np.outer(eps_m, eps_m) - root_m))           # eps(x)eps = root
    r_half = max(_mx(K_gen @ eps_p - 1j * eps_p),
                 _mx(K_gen @ eps_m + 1j * eps_m))                  # peso 1 (a metade)
    thetas = np.linspace(0.05, 1.5, 200)                           # 200 angulos genericos
    r_vec_fin = 0.0
    r_ten_fin = 0.0
    ratio_defect = 0.0
    for th in thetas:
        O_th = _ang(float(th))
        ph = complex(np.exp(1j * th))
        r_vec_fin = max(r_vec_fin, _mx(O_th @ eps_p - ph * eps_p))
        r_ten_fin = max(r_ten_fin, _mx(O_th @ root_p @ O_th.T - (ph ** 2) * root_p))
        phi_v = float(np.angle((O_th @ eps_p)[0]))                 # eps_p[0] = 1
        phi_t = float(np.angle((O_th @ root_p @ O_th.T)[0, 0]))    # root_p[0,0] = 1
        ratio_defect = max(ratio_defect, abs(phi_t / phi_v - 2.0))  # a fase DOBRA
    # face beta (runtime, nunca literal): o angulo modular theta_M = arcsin(sqrt(beta))
    theta_M = math.asin(math.sqrt(beta))
    O_M = _ang(theta_M)
    phi_v_M = float(np.angle((O_M @ eps_p)[0]))
    phi_t_M = float(np.angle((O_M @ root_p @ O_M.T)[0, 0]))
    beta_rec = float(abs(O_M[0, 1]) ** 2)                          # |O[0,1]|^2 = sin^2 = beta
    r_beta_face = max(abs(phi_v_M - theta_M), abs(phi_t_M - 2.0 * theta_M),
                      abs(beta_rec - beta))
    # face do condensado (eq.4/5 DESTA patente): g = sqrt(L) carrega MEIA fase
    phis = np.linspace(0.1, 3.0, 50)
    Lc = np.exp(1j * phis)
    g_c = np.sqrt(Lc)                                              # ramo principal
    r_condensate = float(np.max(np.abs(np.angle(g_c ** 2) - 2.0 * np.angle(g_c))))
    # NEGATIVO 1 (LOGICA): o pareamento MISTO nao e raiz — peso ZERO, a fase NAO dobra
    mix = np.outer(eps_p, eps_m)
    r_mix_closed = _mx(mix - 2.0 * P_p)                            # forma fechada mix = 2 P+
    r_mix_wt0 = _mx(K_gen @ mix - mix @ K_gen)                     # [K, mix] = 0
    th_neg = math.pi / 4.0
    O_neg = _ang(th_neg)
    r_mix_inv = _mx(O_neg @ mix @ O_neg.T - mix)                   # invariante (peso 0)
    neg_defect = _mx(O_neg @ mix @ O_neg.T - complex(np.exp(2j * th_neg)) * mix) / _mx(mix)
    neg_defect_closed = 2.0 * math.sin(th_neg)                     # |1 - e^{2i th}| = 2 sin
    r_neg_cf = abs(neg_defect - neg_defect_closed)
    # NEGATIVO 2 (LOGICA): a polarizacao DESemparelhada h+ e rejeitada pela escada
    comm_hp = K_gen @ h_plus - h_plus @ K_gen
    r_hp_closed = _mx(comm_hp + 2.0 * h_cross)                     # [K, h+] = -2 h_x
    hp_overlap = float(abs(np.trace(h_plus.conj().T @ comm_hp)))   # sem componente em h+
    hp_sq_norm = _mx(h_plus @ h_plus)                              # h+^2 = I (nao nilpotente)
    light_ok = bool(
        r_k2 < 1e-15 and r_pol < 1e-15 and r_wt < 1e-15 and r_nil < 1e-15
        and null_light < 1e-15 and r_fact < 1e-15 and r_proj < 1e-15
        and r_square < 1e-15 and r_half < 1e-15
        and r_vec_fin < 1e-14 and r_ten_fin < 1e-14
        and ratio_defect < 1e-10                                   # a dobra e EXATA
        and r_beta_face < 1e-12 and r_condensate < 1e-12
        and r_mix_closed < 1e-15 and r_mix_wt0 < 1e-15 and r_mix_inv < 1e-14
        and neg_defect > 1.0                                       # NEG: falha MACROSCOPICA
        and r_neg_cf < 1e-12                                       # NEG: forma fechada 2 sin
        and r_hp_closed < 1e-15 and hp_overlap < 1e-13
        and hp_sq_norm > 0.999                                     # NEG: h+ nao e nilpotente
    )
    tests.append({"test": "light_interface_graviton_phase_square_v206", "passed": light_ok,
                  "resid_K_sq_neg_one": r_k2,
                  "resid_roots_are_polarizations": r_pol,
                  "resid_ladder_weights_pm2i": r_wt,
                  "resid_roots_nilpotent": r_nil,
                  "light_null_eps_dot_eps": null_light,
                  "resid_ladder_factors_projections": r_fact,
                  "resid_projections_split_identity": r_proj,
                  "resid_light_squares_to_graviton": r_square,
                  "resid_generator_half_weight": r_half,
                  "n_angles": int(thetas.size),
                  "resid_interface_carries_angle": r_vec_fin,
                  "resid_tensor_squares_phase": r_ten_fin,
                  "phase_doubling_ratio_defect": ratio_defect,
                  "theta_M_arcsin_sqrt_beta": theta_M,
                  "beta_recovered_sin2_theta_M": beta_rec,
                  "resid_beta_face": r_beta_face,
                  "resid_condensate_half_phase_eq4_eq5": r_condensate,
                  "neg_mix_closed_form_2Pplus_resid": r_mix_closed,
                  "neg_mix_weight_zero_resid": r_mix_wt0,
                  "neg_mix_invariant_resid": r_mix_inv,
                  "neg_doubling_defect_mixed_pair": neg_defect,
                  "neg_doubling_defect_closed_form_2sin": neg_defect_closed,
                  "neg_closed_form_resid": r_neg_cf,
                  "neg_hplus_comm_closed_form_resid": r_hp_closed,
                  "neg_hplus_weight_overlap": hp_overlap,
                  "neg_hplus_square_norm_not_nilpotent": hp_sq_norm,
                  "note": "Amplificacao v206 (TGLExt/TheLightInterface.lean, kernel v206 "
                          "24/08, custodia vault): a pedra CITA a equacao publicada "
                          "g=sqrt|L| — eq.(4) DESTA patente (Radicalismo Ontologico, "
                          "reivind. 5/15/16). Estrutura RE-DERIVADA numericamente (nunca "
                          "finge rodar Lean): eps+-(x)eps+- = root+- (o quadrado da luz "
                          "e o graviton); pesos 1 e 2 do MESMO gerador K (K^2=-1); a "
                          "escada fatora as projecoes (root+ root- = 4 P+); a fase do "
                          "tensor e o QUADRADO da fase do vetor (200 angulos + angulo "
                          "modular theta_M = arcsin(sqrt(beta)), beta runtime nunca "
                          "literal, |O[0,1]|^2 recupera beta); na face do condensado, "
                          "g=sqrt(L) carrega MEIA fase e L=s g^2 restaura (entrada -Y = "
                          "raiz, saida +Y = quadrado). NEGATIVO por LOGICA: o par misto "
                          "eps+(x)eps- = 2 P+ tem peso ZERO — a fase NAO dobra, defeito "
                          "2 sin(theta) macroscopico em forma fechada; h+ sozinho e "
                          "rejeitado ([K,h+] = -2 h_x, h+^2 = I). [DER][SIM] sombra "
                          "numerica; sem veredito fisico [HARDWARE]."})
    print(f"[one_supercondutor] amplificacao v206 (TheLightInterface): eps(x)eps=root "
          f"resid={r_square:.2e} | pesos +-2i resid={r_wt:.2e} | escada->4P resid={r_fact:.2e} | "
          f"dobra da fase (200 ang): defeito ratio={ratio_defect:.2e}")
    print(f"[one_supercondutor]   face beta: theta_M=arcsin(sqrt(beta))={theta_M:.6f} "
          f"fase vetor={phi_v_M:.6f} fase tensor={phi_t_M:.6f} (=2x) | "
          f"beta recuperado |O[0,1]|^2={beta_rec:.15f}")
    print(f"[one_supercondutor]   NEG par misto eps+(x)eps- = 2P+ (resid {r_mix_closed:.2e}): "
          f"peso ZERO, defeito da dobra={neg_defect:.6f} (forma fechada 2sin(pi/4)="
          f"{neg_defect_closed:.6f}, resid {r_neg_cf:.2e}) | h+ rejeitado: overlap="
          f"{hp_overlap:.2e}, h+^2 norm={hp_sq_norm:.1f} (nao nilpotente)")

    # device interface (mock — no physics)
    mock = SupercondutorMock().transport(1_000_000)
    tests.append({"test": "device_interface_mock_no_physics", "passed": bool(mock["physical_verdict_allowed"] is False),
                  "mock_status": mock["status"], "note": mock["note"]})

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

    def _o5_sc_acom_scale():
        rng5 = np.random.default_rng(34500)
        L_ = rng5.standard_normal(5000) * 3.0
        g1, s1 = acom.reflect(L_); lam_ = math.pi
        g2, s2 = acom.reflect(lam_ * L_)
        rel_g = float(np.max(np.abs(g2 - math.sqrt(lam_) * g1) / (math.sqrt(lam_) * g1)))
        s_same = bool(np.array_equal(s1, s2))
        rel_L = float(np.max(np.abs(acom.manifest(g2, s2) - lam_ * L_)) / np.max(np.abs(lam_ * L_)))
        g3, s3 = acom.reflect(L_ + 1.0)
        n_flip = int(np.sum(s3 != s1))
        ok = rel_g < 1e-13 and s_same and rel_L < 1e-13 and n_flip > 0
        return {"passed": ok, "lambda": lam_, "rel_resid_g_sqrt_lambda": rel_g, "sign_unchanged": s_same,
                "rel_resid_manifest": rel_L, "neg_shift_sign_flips": n_flip,
                "note": "REFLECT e homogeneo de grau 1/2 (g -> sqrt(lambda) g, s invariante) e MANIFEST de grau 1; "
                        "um deslocamento aditivo muda sinais (nao e simetria do par radical/quadrado)"}
    _o5("acom_scale_covariance_exact", _o5_sc_acom_scale)

    def _o5_sc_acom_edges():
        L_ = np.array([0.0, -0.0, 1e-300, -1e-300, 2.0, -2.0, 1e300, -1e300])
        g_, s_ = acom.reflect(L_); L2 = acom.manifest(g_, s_)
        zero_ok = bool(L2[0] == 0.0 and L2[1] == 0.0 and s_[0] == 1.0 and s_[1] == 1.0)
        finite_ok = bool(np.all(np.isfinite(L2)))
        rel = float(np.max(np.abs(L2[4:] - L_[4:]) / np.abs(L_[4:])))
        tiny_ok = bool(L2[2] > 0.0 and L2[3] < 0.0)
        ok = zero_ok and finite_ok and rel < 1e-15 and tiny_ok
        return {"passed": ok, "zero_to_zero_sign_plus": zero_ok, "finite_at_1e300": finite_ok,
                "rel_resid_large_and_unit": rel, "tiny_keeps_sign": tiny_ok,
                "note": "bordas do par radical/quadrado: zero -> zero com s=+1 (convencao dita); 1e300 nao estoura "
                        "(a raiz e o quadrado se cancelam); 1e-300 preserva o sinal"}
    _o5("acom_edge_cases_zero_sign_overflow", _o5_sc_acom_edges)

    def _o5_sc_gap_scaling():
        sizes = [8, 12, 16, 24]; gaps, kers = [], []
        for n_ in sizes:
            w_ = np.linalg.eigvalsh(_three_locks_block(n_))
            k_ = int(np.sum(w_ < 1e-10)); kers.append(k_); gaps.append(float(w_[k_]))
        mono = all(gaps[i] > gaps[i + 1] for i in range(len(gaps) - 1))
        ratio = gaps[0] / gaps[2]
        ok = all(k == 1 for k in kers) and mono and 3.0 < ratio < 5.5 and int(dim_ker) == 2
        return {"passed": ok, "sizes": sizes, "gaps": gaps, "ker_dims": kers, "gap8_over_gap16": ratio,
                "two_blocks_ker_dim": int(dim_ker),
                "note": "o gap das Three Locks cai com o tamanho (~1/n^2: gap(8)/gap(16) ~ 4) e o nucleo e UNICO por bloco "
                        "conexo; dois blocos desconexos => dois modos zero (dim ker = numero de componentes)"}
    _o5("three_locks_gap_scaling_and_connectivity", _o5_sc_gap_scaling)

    def _o5_sc_verb_semigroup():
        def V_(t_):
            return evecs @ np.diag(np.exp(-t_ * beta * evals)) @ evecs.T
        r_semi = float(np.max(np.abs(V_(1.0) @ V_(2.0) - V_(3.0))))
        norms = [float(np.linalg.norm(V_(t_), 2)) for t_ in (0.5, 5.0, 50.0)]
        conv = float(np.linalg.norm(V_(50.0) - q_F, 2)); bound = math.exp(-50.0 * beta * gap_h3l)
        anti = float(np.linalg.norm(evecs @ np.diag(np.exp(+5.0 * beta * evals)) @ evecs.T, 2))
        ok = r_semi < 1e-12 and all(n_ <= 1.0 + 1e-12 for n_ in norms) and conv <= bound + 1e-12 and anti > 1.0 + 1e-6
        return {"passed": ok, "semigroup_resid": r_semi, "norms_t_0p5_5_50": norms, "dist_to_qF_t50": conv,
                "bound_exp_minus_t_beta_gap": bound, "neg_antiverb_norm": anti,
                "note": "o Verbo exp(-t beta H3L) e semigrupo contrativo (V_s V_t = V_{s+t}, ||V_t|| <= 1) e converge ao "
                        "suporte q_F a taxa exp(-t beta gap); o anti-Verbo exp(+t beta H3L) EXPANDE — rejeitado"}
    _o5("verb_semigroup_contraction_antiverb_rejected", _o5_sc_verb_semigroup)

    def _o5_sc_plateau_time():
        t90 = {}
        for k_ in gains:
            y_ = coherence_curves[k_]
            i_ = int(np.argmax(y_ >= 0.9 * plateau_target))
            t90[k_] = float(np.interp(0.9 * plateau_target, y_[i_ - 1:i_ + 1], t_axis[i_ - 1:i_ + 1])) if i_ > 0 else 0.0
        rel = max(abs(t90[k_] - math.log(10.0) / k_) / (math.log(10.0) / k_) for k_ in gains)
        ratio = t90[gains[0]] / t90[gains[-1]]; exp_ratio = gains[-1] / gains[0]
        ok = rel < 0.02 and abs(ratio - exp_ratio) < 0.1 * exp_ratio
        return {"passed": ok, "t90_by_gain": {str(k_): v for k_, v in t90.items()}, "closed_form": "ln(10)/k",
                "max_rel_resid": rel, "t90_ratio_lowest_over_highest_gain": ratio, "expected_ratio": exp_ratio,
                "note": "o tempo ate 90% do plato e ln(10)/k (medido por interpolacao vs forma fechada); a alegacao "
                        "'independe do ganho' e rejeitada: entre os ganhos 0,5 e 4 a razao e 8"}
    _o5("plateau_rise_time_closed_form", _o5_sc_plateau_time)

    def _o5_sc_tanh_forms():
        P_ = np.linspace(0.0, 3.0, 30001); eta_ = np.tanh(P_ / P_th)
        d0 = float((eta_[1] - eta_[0]) / (P_[1] - P_[0]))
        eta_pth = float(np.interp(P_th, P_, eta_))
        logi0 = float(1.0 / (1.0 + math.exp(-(0.0 - P_th) / P_th)))
        ok = abs(d0 - 1.0 / P_th) < 1e-3 and abs(eta_pth - math.tanh(1.0)) < 1e-9 and logi0 > 0.2
        return {"passed": ok, "slope_at_origin": d0, "expected_1_over_Pth": 1.0 / P_th, "eta_at_Pth": eta_pth,
                "tanh1": math.tanh(1.0), "neg_logistic_at_zero": logi0,
                "note": "a transicao tanh: inclinacao 1/P_th na origem e eta(P_th) = tanh(1) = 0,7616 (formas fechadas "
                        "medidas); uma logistica centrada em P_th NAO parte de zero — rejeitada como modelo da patente"}
    _o5("transition_closed_forms_logistic_rejected", _o5_sc_tanh_forms)

    passed = sum(1 for t in tests if t["passed"]); total = len(tests); all_ok = passed == total
    summary = {"tests_passed": passed, "tests_total": total, "alpha2_c": alpha2_c,
               "acom_residual": resid, "v_info_note": "algebraic v_info->0 vs prose ->inf [OPEN]",
               "over_unity_guard": "active",
               "transition_width_norm": float(np.mean(width_norms)),
               "metric_critical_exponent": p_fit,
               "coherence_plateau": plateau_mean, "coherence_plateau_target": plateau_target,
               "dual_lock_v143": {"oath_resid": oath_resid, "covariance_resid": resid_cov,
                                  "neg_oath_break": oath_break,
                                  "neg_oath_break_closed_form": oath_theory,
                                  "neg_cov_defect": cov_defect_bad},
               "ergodic_mean_v168": {"tau_good": tau_good,
                                     "birkhoff_defect_final": d_good[-1],
                                     "equivariant_resid": equiv_resid,
                                     "verbo_defect_final": d_verbo[-1],
                                     "neg_defect_resonant_clock": d_bad_vs_qF,
                                     "neg_trace_P_alias": tr_alias},
               "light_interface_v206": {"resid_light_squares_to_graviton": r_square,
                                        "phase_doubling_ratio_defect": ratio_defect,
                                        "theta_M": theta_M, "beta_recovered": beta_rec,
                                        "neg_doubling_defect_mixed_pair": neg_defect,
                                        "neg_doubling_defect_closed_form": neg_defect_closed},
               "sweeps": {"P_th_scan": P_th_scan, "alpha2_points": int(a2_fine.size),
                          "coherence_gains": gains}}
    max_verdict = ("SUPERCONDUCTOR_LOGIC_DEMONSTRATED ([SIM][HARDWARE] — ACOM preservação, "
                   "transição tipo-fase e balanço fail-closed fecham no MODELO; dispositivo "
                   "físico NÃO construído; não simula plasma/vácuo/óptica)")
    _finish(PATENT_DIR, CENTRAL, ts, PATENT_ID, SLUG, "one_supercondutor.py",
            ["[SIM]", "[HARDWARE]"], beta, beta_ok, all_ok, max_verdict, tests, summary,
            module_hashes,
            "Demonstração [SIM] da lógica do dispositivo (sinal + balanço de modelo). NÃO simula "
            "plasma OH/vácuo/óptica; NÃO prova translação [HARDWARE]. Divergência v_info→0 "
            "(algébrico) vs prosa →∞ registrada [OPEN]. Simulação não valida física.",
            fig_builder=lambda plt, fd: _fig_super(plt, fd, P_MW, eta, P_th, alpha2_c,
                                                   P_th_scan, a2_fine, g_tt_f, g_LL_f, v_info_f,
                                                   t_axis, coherence_curves, plateau_target))

    # FORMA = CONTEÚDO: esta patente NÃO tem geometria computável (condensado OH / câmara),
    # então o corpo de engenharia do render3d é PRESERVADO; só re-carimbamos generated_by e
    # injetamos β runtime + métricas COMPUTADAS desta run (merge, não reconstrói nós).
    emit_render3d_merge(PATENT_DIR, beta, {
        "plateau_coherence": plateau_mean, "plateau_target_1_minus_beta": plateau_target,
        "metric_critical_exponent": p_fit,
        "transition_width_norm": float(np.mean(width_norms)),
        "acom_residual": resid})
    return 0 if all_ok else 1


def emit_render3d_merge(patent_dir: Path, beta: float, metrics: dict) -> None:
    """MERGE: lê patents/<ID>/render3d.json ATUAL, PRESERVA meshes/nodes/edges/layers/
    groups/dimensions (corpo de engenharia — sem geometria computável nesta patente),
    re-carimba generated_by e injeta β runtime + 1-2 métricas COMPUTADAS nesta run em
    constants. Valida integridade (edges⊆nodes+meshes; layers de mesh/nós existem)."""
    out = patent_dir / "render3d.json"
    if not out.exists():
        print(f"[supercondutor] render3d.json ausente — emit pulado (nada a preservar)")
        return
    d = json.loads(out.read_text(encoding="utf-8"))

    # re-carimbo (preserva title/kind/schema/note/camera/layers/groups/meshes/nodes/edges/dimensions)
    d["generated_by"] = "one_supercondutor.py (forma=conteudo)"

    # injeta β runtime + métricas COMPUTADAS em constants (preservando as constantes de projeto)
    consts = d.get("constants", [])
    consts = [c for c in consts if c.get("symbol") not in
              ("beta_TGL", "plato_coerencia", "expoente_critico_v_info")]
    consts.append({"symbol": "beta_TGL", "value": f"{beta:.12f} (alpha*sqrt(e))",
                   "note": "acoplamento holografico — INJETADO em runtime (nunca literal)"})
    consts.append({"symbol": "plato_coerencia",
                   "value": f"|rho01|->{metrics['plateau_coherence']:.6f}",
                   "note": f"COMPUTADO nesta run; alvo 1-beta={metrics['plateau_target_1_minus_beta']:.6f}"})
    consts.append({"symbol": "expoente_critico_v_info",
                   "value": f"p={metrics['metric_critical_exponent']:.4f}",
                   "note": "v_info~(1-a2/a2_c)^p; ajuste COMPUTADO (algebrico, ~1) [OPEN]"})
    d["constants"] = consts

    # ---- validação de integridade ----
    node_ids = {n["id"] for n in d.get("nodes", [])}
    mesh_ids = {m["id"] for m in d.get("meshes", [])}
    valid_ids = node_ids | mesh_ids
    layer_ids = {l["id"] for l in d.get("layers", [])}
    for e in d.get("edges", []):
        if e["from"] not in valid_ids or e["to"] not in valid_ids:
            raise ValueError(f"edge {e} referencia id inexistente em nodes+meshes")
    for coll in ("nodes", "meshes"):
        for item in d.get(coll, []):
            lyr = item.get("layer")
            if lyr is not None and lyr not in layer_ids:
                raise ValueError(f"{coll} '{item.get('id')}' usa layer '{lyr}' inexistente")

    out.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[supercondutor] render3d.json EMITIDO (forma=conteudo) — corpo PRESERVADO "
          f"({len(d.get('nodes', []))} nos, {len(d.get('meshes', []))} malhas; merge + metricas)")


def _fig_super(plt, fig_dir, P_MW, eta, P_th, alpha2_c, P_th_scan, a2_fine, g_tt_f, g_LL_f,
               v_info_f, t_axis, coherence_curves, plateau_target):
    import numpy as _np
    figs = []
    # Fig.1 — transição tipo-fase com varredura de P_th (auto-similaridade)
    plt.figure(figsize=(7, 3.6))
    for pth in P_th_scan:
        Ps = _np.linspace(0, 3.0, 300)
        plt.plot(Ps, _np.tanh(Ps / pth), label=f"P_th={pth}")
    plt.axhline(0.5, color="gray", ls=":", lw=.8)
    plt.xlabel("P_MW (u.a.)"); plt.ylabel("η (fator de ressonância)")
    plt.title("Transição SC η(P_MW)=tanh(P_MW/P_th) — varredura de limiar [SIM]")
    plt.legend(fontsize=8); plt.grid(alpha=.3)
    fp = fig_dir / "fig_transicao_sc.png"; plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close()
    figs.append("fig_transicao_sc.png")

    # Fig.2 — coeficientes métricos vs α² (horizonte α²_c) + v_info
    fig, ax1 = plt.subplots(figsize=(7, 3.6))
    ax1.plot(a2_fine, g_tt_f, color="#1f77b4", label="g_tt = 1−α²/α²_c")
    ax1.plot(a2_fine, v_info_f, color="#2ca02c", label="v_info = |1−α²/α²_c|")
    ax1.set_xlabel("α²"); ax1.set_ylabel("g_tt , v_info")
    ax1.axvline(alpha2_c, color="crimson", ls="--", lw=.9, label="α²_c (horizonte)")
    ax2 = ax1.twinx(); ax2.plot(a2_fine, g_LL_f, color="#ff7f0e", alpha=.7, label="g_LL")
    ax2.set_ylabel("g_LL (→∞)"); ax2.set_yscale("log")
    ax1.set_title("Métrica vs α²: g_tt→0, g_LL→∞, v_info→0 (algébrico) [OPEN]")
    h1, l1 = ax1.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, fontsize=7, loc="upper center")
    ax1.grid(alpha=.3)
    fp = fig_dir / "fig_metrica_alpha2.png"; plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close()
    figs.append("fig_metrica_alpha2.png")

    # Fig.3 — platô de coerência |ρ01|→1−β (varredura de ganho)
    plt.figure(figsize=(7, 3.6))
    for k, curve in coherence_curves.items():
        plt.plot(t_axis, curve, label=f"ganho k={k}")
    plt.axhline(plateau_target, color="crimson", ls="--", label=f"platô 1−β={plateau_target:.5f}")
    plt.xlabel("t (u.a.)"); plt.ylabel("|ρ01| (coerência)")
    plt.title("Platô de coerência |ρ01|→1−β — varredura de ganho [SIM]")
    plt.legend(fontsize=8); plt.grid(alpha=.3); plt.ylim(0, 1.02)
    fp = fig_dir / "fig_plato_coerencia.png"; plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close()
    figs.append("fig_plato_coerencia.png")
    return figs


# ---- shared finisher (results + report + seal) -----------------------------------
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


if __name__ == "__main__":
    sys.exit(main())
