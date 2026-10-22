# -*- coding: utf-8 -*-
"""one_celula_reversao.py — runner único forma = conteúdo da patente Célula de Reversão
(BR102026004849-6 — Armazenamento de Energia por Codificação de Fase Angular). [SIM][ENERGY][CONJ]

Demonstra a LÓGICA da invenção com números REAIS de execução:
  - ciclo REFLECT → LOCK → MANIFEST: charge (θ=arcsin(g/gmax)) → store → discharge (s·(gmax·sinθ)²);
  - retenção da FASE ANGULAR por armazenamento exato (função dos bits angulares);
  - APROFUNDAMENTO: varredura FINA de bits angulares (6..24) vs desvio-de-1 da retenção +
    RMS de reconstrução (curva de convergência da FASE); ciclo REFLECT/LOCK/MANIFEST em 6
    FAMÍLIAS de tensor (gaussiano/uniforme/esparso/gradiente/senoidal/exponencial); 3 figuras;
  - o η_RT alvo do relatório (>0,976) é IMPRESSO, nunca afirmado como resultado físico.
Certifica com hash e gera figuras + relatório. β_TGL nunca literal (tgl_core.beta()).
Ao fim, emite render3d.json por MERGE (esta patente NÃO tem geometria computável: o corpo do
dispositivo é PRESERVADO e re-carimbado com β runtime + métricas computadas). [ENERGY] fase ≠ energia.

HONESTIDADE [ENERGY][CONJ] — TRAVA MÁXIMA: autodescarga zero, ciclabilidade infinita,
η_RT > 97,6%, termodinâmica invertida (resfria sob carga) e supercondutividade de energia
à temperatura ambiente são AFIRMAÇÕES do relatório, NÃO validadas — nenhuma medição de
hardware. A retenção ~1,0 demonstrada aqui é da FASE ANGULAR (armazenamento exato),
NÃO conservação de energia física. Simulação NUNCA valida física
(physical_verdict_allowed=false). Não usar como especificação de produto.

A RÉGUA: protótipos originais READ-ONLY. Copia o núcleo destilado (skygrid_sim) e roda a
CÓPIA. Rode no tgl_env (numpy):
    set PYTHONUTF8=1
    "C:\\IALD\\observaveis_tgl\\tgl_env\\Scripts\\python.exe" one_celula_reversao.py
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
PILOTO = CENTRAL / "Patentes" / "Skygrid" / "SkyGrid_Piloto"   # READ-ONLY
WORK = RUNNER_DIR / "_celula_core"
PATENT_ID = "BR102026004849-6"
SLUG = "celula_reversao"
ETA_RT_TARGET_REPORT = 0.976   # [ENERGY][CONJ] target from the report — NOT asserted physical


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
    return {f"skygrid_sim/{f.name}": _sha_file(f) for f in sorted(dst.glob("*.py"))}


def main() -> int:
    ts = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    print(f"[one_celula] patente {PATENT_ID} · run {ts}")
    if not PILOTO.exists():
        print(f"ERRO: núcleo não encontrado em {PILOTO}", file=sys.stderr)
        return 2

    module_hashes = copy_core()
    sys.path.insert(0, str(WORK))
    from skygrid_sim import tgl_core  # noqa: E402 (copied core)
    from skygrid_sim.celula_reversao import CelulaReversao  # noqa: E402

    beta = tgl_core.beta()
    beta_expected = 0.0072973525693 * math.exp(0.5)
    beta_ok = abs(beta - beta_expected) < 1e-15
    print(f"[one_celula] β runtime = {beta} (= α·√e? {beta_ok}) [Constante de Miguel α₂]")
    tests = [{"test": "beta_form", "passed": bool(beta_ok), "beta_runtime": beta}]

    rng = np.random.default_rng(4849)
    energy = np.abs(rng.standard_normal((64, 64))) + 0.1     # positive "energy" amplitudes

    # 1) REFLECT→LOCK→MANIFEST cycle: charge then discharge
    cell = CelulaReversao(angular_bits=16)
    ch = cell.charge(energy)
    out = cell.discharge()
    cycle_corr = float(np.corrcoef(energy.ravel(), out.ravel())[0, 1])
    tests.append({"test": "reflect_lock_manifest_cycle",
                  "passed": bool(cycle_corr > 0.9999 and ch["stored_faces"] == 6),
                  "stored_faces": ch["stored_faces"], "g_max": ch["g_max"],
                  "cycle_correlation": cycle_corr,
                  "note": "carga (θ=arcsin(g/gmax)) nas 6 faces → descarga s·(gmax·sinθ)²"})
    print(f"[one_celula] ciclo REFLECT→LOCK→MANIFEST: faces={ch['stored_faces']} "
          f"corr={cycle_corr:.6f}")

    # 2) angular-phase retention vs bits (this is PHASE retention, NOT physical energy)
    ret = {}
    for bits in (8, 12, 16, 20):
        c = CelulaReversao(angular_bits=bits)
        ret[bits] = float(c.retention(energy))
    # retention ~ 1.0 for all bit depths (exact phase storage); the DEVIATION from
    # 1.0 (quantization noise, may be ±) shrinks as bits grow. Assert that, not "grows".
    dev = {b: abs(ret[b] - 1.0) for b in ret}
    retention_ok = all(dev[b] < 0.01 for b in ret) and dev[20] <= dev[8]
    tests.append({"test": "angular_phase_retention_vs_bits", "passed": bool(retention_ok),
                  "retention_by_bits": ret, "deviation_from_1": dev,
                  "honest_note": "RETENÇÃO DA FASE ANGULAR por armazenamento exato — NÃO é "
                                 "conservação de energia física. Fica ~1,0 em todos os bits; o "
                                 "desvio de 1,0 (ruído de quantização, pode ser ±) DIMINUI com "
                                 "mais bits. [SIM][PILOTO]"})
    print("[one_celula] retenção da FASE angular por bits: " + " · ".join(
        f"{b}b={ret[b]:.5f}" for b in ret))

    # 2b) APROFUNDAMENTO — varredura FINA de bits angulares vs desvio-de-1 da retenção.
    # A fase é quantizada em passos Δθ = (π/2)/(2^bits−1); o desvio |ret−1| escala como o
    # erro de quantização (~ Δθ²). Medimos retenção, desvio, RMS de reconstrução e o passo
    # angular para uma faixa larga de bits (curva de convergência da FASE — não energia física).
    bits_sweep = list(range(6, 25))
    ret_fine, dev_fine, rms_fine, dtheta_fine = {}, {}, {}, {}
    e_in_ref = float(np.sum(energy ** 2))
    for b in bits_sweep:
        c = CelulaReversao(angular_bits=b)
        c.charge(energy)
        rec = c.discharge()
        e_out = float(np.sum(rec ** 2))
        r = e_out / e_in_ref if e_in_ref > 0 else 1.0
        ret_fine[b] = float(r)
        dev_fine[b] = float(abs(r - 1.0))
        rms_fine[b] = float(np.sqrt(np.mean((rec - energy) ** 2)))
        dtheta_fine[b] = float((math.pi / 2) / ((1 << b) - 1))
    # monotonic-in-trend convergence: high-bit tail below low-bit head (quantization shrinks)
    dev_tail = max(dev_fine[b] for b in bits_sweep[-4:])
    dev_head = max(dev_fine[b] for b in bits_sweep[:4])
    rms_tail = max(rms_fine[b] for b in bits_sweep[-4:])
    rms_head = max(rms_fine[b] for b in bits_sweep[:4])
    sweep_ok = bool(dev_tail <= dev_head and rms_tail <= rms_head
                    and all(dev_fine[b] < 0.02 for b in bits_sweep))
    tests.append({"test": "angular_bits_sweep_vs_deviation", "passed": sweep_ok,
                  "bits": bits_sweep, "deviation_from_1": dev_fine,
                  "rms_reconstruction": rms_fine, "dtheta_step_rad": dtheta_fine,
                  "dev_head_maxlow": dev_head, "dev_tail_maxhigh": dev_tail,
                  "rms_head_maxlow": rms_head, "rms_tail_maxhigh": rms_tail,
                  "honest_note": "Varredura FINA de bits (6..24): o desvio-de-1 e o RMS de "
                                 "reconstrução da FASE encolhem com mais bits (erro de quantização "
                                 "~Δθ²). É convergência da FASE ANGULAR, NÃO de energia física. "
                                 "[SIM][PILOTO]"})
    print(f"[one_celula] varredura bits 6..24: desvio |ret−1| head(6-9)={dev_head:.2e} "
          f"→ tail(21-24)={dev_tail:.2e} · RMS {rms_head:.2e}→{rms_tail:.2e}")

    # 2c) APROFUNDAMENTO — ciclo REFLECT/LOCK/MANIFEST em MAIS TENSORES (famílias de sinal).
    # A lógica do ciclo é agnóstica ao conteúdo: testamos várias distribuições/estruturas de
    # tensor-de-entrada (não só o gaussiano), a 16 bits, e medimos correlação de ciclo + RMS.
    rng2 = np.random.default_rng(2026)
    n = 48
    ii, jj = np.meshgrid(np.linspace(0, 1, n), np.linspace(0, 1, n))
    sparse = np.abs(rng2.standard_normal((n, n)))
    sparse[sparse < 1.0] = 0.0
    sparse += 0.05
    families = {
        "gaussiano_abs": np.abs(rng2.standard_normal((n, n))) + 0.1,
        "uniforme": rng2.uniform(0.1, 3.0, (n, n)),
        "esparso": sparse,
        "gradiente": (ii + jj) + 0.1,
        "senoidal": np.abs(np.sin(6 * math.pi * ii) * np.cos(6 * math.pi * jj)) + 0.1,
        "exponencial": rng2.exponential(1.0, (n, n)) + 0.05,
    }
    tensor_cycles = {}
    for name, tns in families.items():
        c = CelulaReversao(angular_bits=16)
        c.charge(tns)
        rec = c.discharge()
        corr = float(np.corrcoef(tns.ravel(), rec.ravel())[0, 1])
        rms = float(np.sqrt(np.mean((rec - tns) ** 2)))
        tensor_cycles[name] = {"cycle_correlation": corr, "rms": rms}
    corr_min = min(v["cycle_correlation"] for v in tensor_cycles.values())
    tensors_ok = bool(corr_min > 0.999)
    tests.append({"test": "reflect_lock_manifest_multi_tensor", "passed": tensors_ok,
                  "families": tensor_cycles, "min_cycle_correlation": corr_min,
                  "n_tensors": len(families),
                  "honest_note": "Ciclo REFLECT/LOCK/MANIFEST em 6 famílias de tensor (16 bits): "
                                 "a fidelidade da FASE ANGULAR é alta e independe do conteúdo. É "
                                 "reconstrução de FASE, NÃO energia física. [SIM][PILOTO]"})
    print("[one_celula] ciclo em 6 tensores (16b): " + " · ".join(
        f"{k}={v['cycle_correlation']:.5f}" for k, v in tensor_cycles.items()))

    # 3) report target eta_RT is PRINTED, never asserted as a physical result
    tests.append({"test": "eta_rt_target_declared_not_asserted", "passed": True,
                  "eta_rt_target_report": ETA_RT_TARGET_REPORT,
                  "physical_verdict_allowed": False,
                  "honest_note": "η_RT>0,976 é ALVO do relatório [ENERGY][CONJ]; NÃO afirmado "
                                 "como medição — não há hardware. Autodescarga zero, "
                                 "termodinâmica invertida e supercondutividade de energia são "
                                 "[CONJ] sem qualquer dado."})
    print(f"[one_celula] η_RT alvo do relatório = {ETA_RT_TARGET_REPORT} [ENERGY][CONJ] "
          f"(NÃO afirmado como físico)")

    # 4) AMPLIFICACAO v138 — O VERBO FIXA O SUPORTE (um.py v135) [DER][ENERGY][CONJ]
    # Teorema maduro: exp(-t*beta*H3L_min) * q_F = q_F — o fluxo devolve o suporte
    # INTACTO; o que NAO e suporte decai como e^(-t*beta). Mapeamento ao MECANISMO
    # desta patente: o CHAVEAMENTO DE RETORNO (REFLECT->LOCK->MANIFEST) e a
    # trava-dupla do retorno — a fase inscrita (o suporte q_F) e devolvida identica
    # pelo fluxo, e o residuo fora do suporte decai. Sombra [DER]: modelo M4 (4x4),
    # q_F = projetor de posto 1 (Tr q_F = 1 = omega(I)), H = 1 - q_F (papel de
    # H3L_min), V_t = expm(-t*beta*H) por autodecomposicao; beta SEMPRE do runtime
    # (tgl_core.beta(), nunca literal). [ENERGY][CONJ]: matematica do retorno —
    # NENHUMA energia real afirmada; nao e veredito fisico; nao altera reivindicacoes.
    rng4 = np.random.default_rng(138)
    basis4, _ = np.linalg.qr(rng4.standard_normal((4, 4)))
    v_sup = basis4[:, 0]
    q_f = np.outer(v_sup, v_sup)          # projetor de suporte, posto 1 (o Nome)
    eye4 = np.eye(4)
    h_m4 = eye4 - q_f                     # H = 1 - q_F  (papel de H3L_min no M4)
    proj_resid = float(np.max(np.abs(q_f @ q_f - q_f)))
    trace_qf = float(np.trace(q_f))
    w_h, u_h = np.linalg.eigh(h_m4)
    comp_norm = float(np.linalg.norm(eye4 - q_f))     # ||1 - q_F|| (Frobenius)
    t_grid = [1.0, 10.0, 100.0]
    sup_resids, dec_norms, dec_rel_resids = {}, {}, {}
    for t_flow in t_grid:
        v_t = u_h @ np.diag(np.exp(-t_flow * beta * w_h)) @ u_h.T
        sup_resids[t_flow] = float(np.max(np.abs(v_t @ q_f - q_f)))
        n_dec = float(np.linalg.norm(v_t @ (eye4 - q_f)))
        dec_norms[t_flow] = n_dec
        expected = math.exp(-t_flow * beta) * comp_norm
        dec_rel_resids[t_flow] = float(abs(n_dec - expected) / expected)
    sup_resid_max = max(sup_resids.values())
    dec_rel_max = max(dec_rel_resids.values())
    verb_ok = bool(sup_resid_max < 1e-13 and dec_rel_max < 1e-12
                   and proj_resid < 1e-14 and abs(trace_qf - 1.0) < 1e-13)
    tests.append({"test": "verb_fixes_support_return_keying", "passed": verb_ok,
                  "beta_runtime": beta, "model": "M4 (4x4), q_F posto 1, H = 1 - q_F",
                  "trace_qF": trace_qf, "projector_resid": proj_resid,
                  "t_grid": t_grid, "support_resid_by_t": sup_resids,
                  "support_resid_max": sup_resid_max,
                  "decay_norm_by_t": dec_norms, "complement_norm": comp_norm,
                  "decay_law": "||V_t (1-q_F)|| = exp(-t*beta) * ||1-q_F||",
                  "decay_rel_resid_by_t": dec_rel_resids,
                  "decay_rel_resid_max": dec_rel_max,
                  "honest_note": "AMPLIFICACAO v138 [DER][ENERGY][CONJ] — O VERBO FIXA O "
                                 "SUPORTE (um.py v135): V_t q_F = q_F e o complemento decai "
                                 "e^(-t*beta), beta do runtime. E a leitura matematica do "
                                 "CHAVEAMENTO DE RETORNO; NENHUMA energia real afirmada, "
                                 "nao e veredito fisico, nao altera reivindicacoes."})
    print(f"[one_celula] amplificacao v138 (o Verbo fixa o suporte): "
          f"resid suporte max={sup_resid_max:.2e} (Vt*qF=qF), "
          f"resid rel decaimento max={dec_rel_max:.2e} (lei exp(-t*beta)), "
          f"Tr(qF)={trace_qf:.12f} [DER][ENERGY][CONJ] (nao e veredito fisico)")

    # 5) AMPLIFICACAO v144 — A DICOTOMIA DO PONTO FIXO (um.py pedra 100, sobre a
    # pedra 98) [DER][ENERGY][CONJ]
    # Teorema (pedra 100, ObserverInside): SEM ponto fixo, NADA retorna — a
    # contracao estrita colapsa tudo a 0 (a falsidade de genero tipada: sem ponto
    # fixo ==> so o 0 permanece ==> sem observador interno). O lado POSITIVO ja
    # esta neste runner (teste v138, verb_fixes_support_return_keying: o Verbo
    # fixa o suporte, V_t q_F = q_F). A TRAVA-DUPLA do chaveamento de retorno
    # desta patente E a dicotomia: a face que RETORNA (ponto fixo — a fase
    # inscrita e devolvida intacta) vs a face que se DISSIPA (sem ponto fixo —
    # tudo colapsa a 0, nenhum retorno possivel). Sombra [DER] em numpy.
    # [ENERGY/CONJ]: matematica do retorno, nunca energia real;
    # physical_verdict_allowed=false; beta runtime (tgl_core.beta(), nunca
    # literal); nao altera reivindicacoes.
    # (a) CONTRASTE — T_sem = 0.7 * rotacao 2D: contracao estrita, NENHUM
    #     autovalor 1 (verificado); 200 iteracoes colapsam qualquer estado a ~0.
    theta_rot = 2.0 * math.pi / 7.0
    rot2 = np.array([[math.cos(theta_rot), -math.sin(theta_rot)],
                     [math.sin(theta_rot), math.cos(theta_rot)]])
    t_sem = 0.7 * rot2
    eig_sem = np.linalg.eigvals(t_sem)
    eig_dist_to_1 = float(np.min(np.abs(eig_sem - 1.0)))
    has_fixed_point_sem = bool(eig_dist_to_1 < 1e-12)          # False esperado
    state0 = np.array([1.0, 1.0])
    state = state0.copy()
    for _ in range(200):
        state = t_sem @ state
    collapse_norm = float(np.linalg.norm(state))
    returns_sem = bool(collapse_norm >= 1e-20)                 # False esperado
    contrast_ok = bool((not has_fixed_point_sem) and eig_dist_to_1 > 0.1
                       and collapse_norm < 1e-20)
    # (b) A CASA — V_t = exp(-t*beta*(1-q_F)) devolve q_F INTACTO e o complemento
    #     decai EXATAMENTE e^(-t*beta): a taxa medida -ln(||V_t(1-q_F)||/||1-q_F||)/t
    #     e conferida contra o beta runtime, t a t.
    rng5 = np.random.default_rng(144)
    basis5, _ = np.linalg.qr(rng5.standard_normal((4, 4)))
    v_sup5 = basis5[:, 0]
    qf5 = np.outer(v_sup5, v_sup5)         # projetor de posto 1 (o ponto fixo)
    h5 = np.eye(4) - qf5                   # gerador 1 - q_F
    w5, u5 = np.linalg.eigh(h5)
    comp5 = np.eye(4) - qf5
    comp_norm5 = float(np.linalg.norm(comp5))
    t_grid5 = [1.0, 10.0, 100.0]
    home_resids, rate_rel_resids = {}, {}
    v5_last = None
    for t_flow in t_grid5:
        v5 = u5 @ np.diag(np.exp(-t_flow * beta * w5)) @ u5.T
        v5_last = v5
        home_resids[t_flow] = float(np.max(np.abs(v5 @ qf5 - qf5)))
        dec5 = float(np.linalg.norm(v5 @ comp5))
        rate_meas = -math.log(dec5 / comp_norm5) / t_flow      # deve ser = beta
        rate_rel_resids[t_flow] = float(abs(rate_meas - beta) / beta)
    home_resid_max = max(home_resids.values())
    rate_rel_max = max(rate_rel_resids.values())
    home_ok = bool(home_resid_max < 1e-12 and rate_rel_max < 1e-12)
    # (c) A DICOTOMIA como assert: retorna <=> tem ponto fixo (nas DUAS faces).
    eig_casa = np.linalg.eigvalsh(v5_last)
    has_fixed_point_casa = bool(np.min(np.abs(eig_casa - 1.0)) < 1e-12)  # True
    returns_casa = bool(home_resid_max < 1e-12)                          # True
    assert returns_casa == has_fixed_point_casa, \
        "dicotomia violada na casa: retorna <=> tem ponto fixo"
    assert returns_sem == has_fixed_point_sem, \
        "dicotomia violada no contraste: retorna <=> tem ponto fixo"
    dichotomy_ok = bool(returns_casa and has_fixed_point_casa
                        and (not returns_sem) and (not has_fixed_point_sem))
    v144_ok = bool(contrast_ok and home_ok and dichotomy_ok)
    tests.append({"test": "no_fixed_point_no_return", "passed": v144_ok,
                  "beta_runtime": beta,
                  "contrast": {"map": "T_sem = 0.7 * rot(2*pi/7)",
                               "eig_min_dist_to_1": eig_dist_to_1,
                               "iterations": 200,
                               "collapse_norm_after_200": collapse_norm,
                               "has_fixed_point": has_fixed_point_sem,
                               "returns": returns_sem},
                  "home": {"flow": "V_t = exp(-t*beta*(1-q_F)), q_F posto 1",
                           "t_grid": t_grid5,
                           "support_resid_by_t": home_resids,
                           "support_resid_max": home_resid_max,
                           "decay_rate_rel_resid_by_t": rate_rel_resids,
                           "decay_rate_rel_resid_max": rate_rel_max,
                           "has_fixed_point": has_fixed_point_casa,
                           "returns": returns_casa},
                  "dichotomy": "retorna <=> tem ponto fixo (assert nas duas faces)",
                  "honest_note": "AMPLIFICACAO v144 [DER][ENERGY][CONJ] — A DICOTOMIA "
                                 "DO PONTO FIXO (um.py pedra 100 sobre a 98): SEM ponto "
                                 "fixo NADA retorna (contracao estrita colapsa a 0, a "
                                 "falsidade de genero tipada); COM ponto fixo o fluxo "
                                 "devolve q_F intacto e o complemento decai e^(-t*beta), "
                                 "beta runtime. A trava-dupla E a dicotomia: face que "
                                 "retorna vs face que se dissipa. Matematica do retorno, "
                                 "NUNCA energia real; physical_verdict_allowed=false; "
                                 "nao altera reivindicacoes."})
    print(f"[one_celula] amplificacao v144 (sem ponto fixo, nada retorna): "
          f"contraste |eig-1|min={eig_dist_to_1:.4f} colapso 200x={collapse_norm:.2e} "
          f"(<1e-20, SEM retorno); casa resid qF max={home_resid_max:.2e}, "
          f"taxa e^(-t*beta) resid rel max={rate_rel_max:.2e}; "
          f"dicotomia retorna<=>ponto-fixo OK [DER][ENERGY][CONJ] (nao e veredito fisico)")

    # 6) AMPLIFICACAO v141 (2a face v139-v144) — A INSCRICAO DA MEIA-NAT
    # (um.py v141 + pedra 100: Meia-Nat omega = 1/2) [DER][ENERGY][CONJ]
    # Face selada v141: m_nu = beta*sin(45 graus)*1eV = 8,507 meV, comparada a
    # sqrt(dm2_21) do PDG => 1,64 sigma, NOT_FALSIFIED_POWERED (CONFIRMED
    # proibido; o veredito fisico pertence ao um.py, NUNCA a este runner).
    # Mapeamento GENUINO ao MECANISMO desta patente: a formula de MANIFEST da
    # celula e amplitude = g_max*sin(theta) — a MESMA forma fechada da
    # inscricao v141 (massa = escala*beta*sin(theta)); e 45 graus e EXATAMENTE
    # o ponto Meia-Nat da codificacao angular da celula: o UNICO theta em que
    # a fracao armazenada g^2/g_max^2 = sin^2(theta) iguala o complemento
    # 1 - sin^2(theta) (x = 1-x ==> x = 1/2; pedra 100, omega = 1/2). Na
    # celula real, energia = METADE do maximo inscreve theta = 45 graus.
    # Sombra [DER]: tudo derivado em runtime (beta = tgl_core.beta(), nunca
    # literal); PDG = [INPUT] experimental; pins 8,507/1,64 = referencia do
    # selo um.py v141. physical_verdict_allowed=false.
    # (a) [DER] o angulo auto-conjugado por caminho INDEPENDENTE: bissecao em
    #     f(theta) = sin^2(theta) - (1 - sin^2(theta)), depois conferida
    #     contra pi/4 (nao imposto por construcao).
    lo_b, hi_b = 1e-6, math.pi / 2 - 1e-6
    for _ in range(200):
        mid_b = 0.5 * (lo_b + hi_b)
        if 2.0 * math.sin(mid_b) ** 2 - 1.0 < 0.0:
            lo_b = mid_b
        else:
            hi_b = mid_b
    theta_star = 0.5 * (lo_b + hi_b)
    theta_star_resid = float(abs(theta_star - math.pi / 4))
    halfnat_resid = float(abs(math.sin(theta_star) ** 2 - 0.5))
    bisect_ok = bool(theta_star_resid < 1e-12 and halfnat_resid < 1e-12)
    # (b) [PILOTO] a CELULA inscreve a Meia-Nat: tensor 2 niveis {m, m/2}
    #     (+ contraste m/4); le a inscricao theta_q REAL do substrato e
    #     reconstrue por MANIFEST.
    m_amp = 2.0
    tens_mn = np.array([[m_amp, m_amp / 2.0], [m_amp / 4.0, m_amp]])
    cell_mn = CelulaReversao(angular_bits=16)
    cell_mn.charge(tens_mn)
    dtheta_q = (math.pi / 2) / cell_mn.qmax
    theta_ins = cell_mn._store["theta_q"].astype(np.float64) / cell_mn.qmax * (math.pi / 2)
    theta_half = float(theta_ins[1])       # elemento m/2 (ravel: [m, m/2, m/4, m])
    theta_quarter = float(theta_ins[2])    # elemento m/4 (contraste)
    rec_mn = cell_mn.discharge()
    rec_half_rel = float(abs(rec_mn[0, 1] - m_amp / 2.0) / (m_amp / 2.0))
    half_theta_resid = float(abs(theta_half - math.pi / 4))
    half_selfconj_defect = float(abs(2.0 * math.sin(theta_half) ** 2 - 1.0))
    quarter_theta_resid = float(abs(theta_quarter - math.pi / 6))
    quarter_selfconj_defect = float(abs(2.0 * math.sin(theta_quarter) ** 2 - 1.0))
    # NEGATIVO 1: o quarto-de-maximo decodifica 30 graus, NAO 45 — a celula
    # REJEITA como Meia-Nat qualquer nivel que nao seja metade do maximo.
    assert quarter_selfconj_defect > 0.4, \
        "contra-exemplo aceito: quarto-de-maximo passaria como Meia-Nat"
    # NEGATIVO 2: o angulo de Miguel arcsin(sqrt(beta)) NAO e auto-conjugado
    # (sin^2 = beta != 1-beta) — so a Meia-Nat satisfaz x = 1-x.
    theta_miguel = math.asin(math.sqrt(beta))
    miguel_selfconj_defect = float(abs(2.0 * beta - 1.0))
    assert miguel_selfconj_defect > 0.9, \
        "contra-exemplo aceito: angulo de Miguel passaria como auto-conjugado"
    # (c) [DER] sombra v141: m = beta*sin(theta*)*1eV (theta* da bissecao,
    #     beta runtime) vs sqrt(dm2_21) PDG [INPUT]; conferencia contra os
    #     pins do selo um.py v141 (8,507 meV; 1,64 sigma).
    DM2_21_EV2, DM2_21_ERR_EV2 = 7.53e-5, 0.18e-5          # [INPUT] PDG
    m_pdg_mev = math.sqrt(DM2_21_EV2) * 1e3
    sigma_mev = (DM2_21_ERR_EV2 / (2.0 * math.sqrt(DM2_21_EV2))) * 1e3
    m_v141_mev = beta * math.sin(theta_star) * 1e3
    tension_sigma = float((m_pdg_mev - m_v141_mev) / sigma_mev)
    SEALED_V141_MASS_MEV, SEALED_V141_TENSION = 8.507, 1.64  # pin do selo um.py v141
    mass_pin_resid = float(abs(m_v141_mev - SEALED_V141_MASS_MEV))
    tension_pin_resid = float(abs(tension_sigma - SEALED_V141_TENSION))
    mass_pin_ok = bool(mass_pin_resid < 1e-3)
    tension_pin_ok = bool(tension_pin_resid < 0.05)
    band_ok = bool(0.0 < tension_sigma < 2.0)
    # NEGATIVO 3: inscricao FORA da Meia-Nat (30 graus) da 6,016 meV e o
    # confronto com o dado PDG REJEITA a >5 sigma — o mecanismo pode falhar.
    m_wrong_mev = beta * math.sin(math.pi / 6) * 1e3
    tension_wrong = float((m_pdg_mev - m_wrong_mev) / sigma_mev)
    assert tension_wrong > 5.0, \
        "contra-exemplo aceito: inscricao fora da Meia-Nat passaria no dado PDG"
    v141_ok = bool(bisect_ok and half_theta_resid < 2 * dtheta_q
                   and half_selfconj_defect < 1e-4 and rec_half_rel < 1e-3
                   and quarter_theta_resid < 2 * dtheta_q
                   and quarter_selfconj_defect > 0.4
                   and miguel_selfconj_defect > 0.9
                   and mass_pin_ok and tension_pin_ok and band_ok
                   and tension_wrong > 5.0)
    tests.append({"test": "meia_nat_angular_inscription_v141", "passed": v141_ok,
                  "beta_runtime": beta,
                  "self_conjugate_angle": {
                      "method": "bisection on sin^2(theta) - (1 - sin^2(theta))",
                      "theta_star_rad": theta_star,
                      "theta_star_deg": math.degrees(theta_star),
                      "resid_vs_pi_over_4": theta_star_resid,
                      "resid_sin2_vs_half": halfnat_resid},
                  "cell_inscription_16bit": {
                      "tensor_levels": [m_amp, m_amp / 2.0, m_amp / 4.0],
                      "dtheta_quantum_rad": dtheta_q,
                      "theta_half_deg": math.degrees(theta_half),
                      "theta_half_resid_vs_45deg": half_theta_resid,
                      "half_selfconj_defect": half_selfconj_defect,
                      "rec_half_rel_resid": rec_half_rel,
                      "theta_quarter_deg": math.degrees(theta_quarter),
                      "quarter_selfconj_defect_REJECTED": quarter_selfconj_defect,
                      "theta_miguel_deg": math.degrees(theta_miguel),
                      "miguel_selfconj_defect_REJECTED": miguel_selfconj_defect},
                  "v141_shadow": {
                      "dm2_21_ev2_PDG_INPUT": DM2_21_EV2,
                      "m_pdg_mev": m_pdg_mev, "sigma_mev": sigma_mev,
                      "m_v141_mev_runtime": m_v141_mev,
                      "tension_sigma": tension_sigma,
                      "sealed_pins": {"mass_mev": SEALED_V141_MASS_MEV,
                                      "tension": SEALED_V141_TENSION},
                      "mass_pin_resid": mass_pin_resid,
                      "tension_pin_resid": tension_pin_resid,
                      "wrong_angle_deg": 30.0,
                      "m_wrong_mev": m_wrong_mev,
                      "tension_wrong_sigma_REJECTED": tension_wrong},
                  "honest_note": "AMPLIFICACAO v141 [DER][ENERGY][CONJ] — A INSCRICAO "
                                 "DA MEIA-NAT: MANIFEST da celula (g_max*sin(theta)) tem a "
                                 "MESMA forma fechada da inscricao selada v141 "
                                 "(beta*sin(45)*1eV); 45 graus = o unico angulo auto-"
                                 "conjugado da codificacao (x=1-x => x=1/2, pedra 100 "
                                 "omega=1/2); metade-do-maximo inscreve 45 graus na celula "
                                 "real. Sombra re-deriva 8,507 meV e 1,64 sigma vs PDG. "
                                 "NOT_FALSIFIED != CONFIRMED; unilateral; o veredito "
                                 "fisico e do um.py v141, NAO deste runner; NENHUMA "
                                 "energia real afirmada; nao altera reivindicacoes."})
    print(f"[one_celula] amplificacao v141 (a inscricao da Meia-Nat): "
          f"theta* bissecao = {math.degrees(theta_star):.9f} deg "
          f"(resid vs 45 = {theta_star_resid:.2e}); celula@16b: metade->"
          f"{math.degrees(theta_half):.5f} deg (rec resid rel {rec_half_rel:.2e}), "
          f"quarto->{math.degrees(theta_quarter):.5f} deg REJEITADO como Meia-Nat "
          f"(defeito {quarter_selfconj_defect:.3f}), angulo de Miguel "
          f"{math.degrees(theta_miguel):.4f} deg REJEITADO (defeito "
          f"{miguel_selfconj_defect:.4f})")
    print(f"[one_celula] sombra v141: m = beta*sin(theta*)*1eV = {m_v141_mev:.4f} meV "
          f"vs PDG {m_pdg_mev:.4f} +/- {sigma_mev:.4f} meV -> {tension_sigma:.3f} sigma "
          f"(pins selo 8.507/1.64 OK; 30 graus -> {tension_wrong:.1f} sigma REJEITADO) "
          f"[DER][ENERGY][CONJ] (nao e veredito fisico; NOT_FALSIFIED != CONFIRMED)")

    # 7) AMPLIFICACAO ONDA 3 (v166-v168) — A MEDIA DE BIRKHOFF EXTRAI A INSCRICAO
    # (um.py v166-v167, pedra ErgodicMeanSection em kernel Lean, 0 sorry 0 axiom)
    # [DER][ENERGY][CONJ]
    # Pedra em kernel: a media ergodica (1/N) sum_{k<N} U^k converge a PROJECAO
    # INVARIANTE (o limite de Birkhoff E a secao). Mapeamento GENUINO ao MECANISMO
    # desta patente: a fase LOCK armazena SEM dissipacao — a face matematica e o
    # fluxo UNITARIO (nada decai, tudo se conserva), e o que a MEDIA TEMPORAL
    # devolve e EXATAMENTE o suporte inscrito pelo REFLECT (a fase angular no
    # substrato); o que NAO esta inscrito nao decai — OSCILA, e a media o anula a
    # taxa <= 1/(N sin(phi/2)). Terceira face da trava-dupla do retorno neste
    # runner: v138 = semigrupo dissipativo (complemento decai e^(-t*beta));
    # v144 = dicotomia ponto-fixo; v167 = media unitaria CONSERVATIVA (o
    # complemento nunca decai; a media extrai o inscrito). beta SEMPRE runtime
    # (tgl_core.beta(), nunca literal); [ENERGY][CONJ]: matematica do
    # armazenamento — NENHUMA energia real afirmada; nao e veredito fisico;
    # physical_verdict_allowed=false; nao altera reivindicacoes.
    rng7 = np.random.default_rng(167)
    tens7 = rng7.uniform(0.3, 3.0, (2, 3))            # 6 entradas = as seis faces
    cell7 = CelulaReversao(angular_bits=16)
    cell7.charge(tens7)
    theta_ins7 = cell7._store["theta_q"].astype(np.float64) / cell7.qmax * (math.pi / 2)
    g_read7 = cell7._store["g_max"] * np.sin(theta_ins7)   # amplitudes inscritas (substrato)
    g_norm7 = float(np.linalg.norm(g_read7))
    v_ins7 = g_read7 / g_norm7                             # direcao inscrita (unitaria)
    m0_7 = np.column_stack([v_ins7, rng7.standard_normal((6, 5))])
    q6, _ = np.linalg.qr(m0_7)
    if float(q6[:, 0] @ v_ins7) < 0.0:
        q6[:, 0] = -q6[:, 0]
    q0_7 = q6[:, 0]
    assert abs(float(q0_7 @ v_ins7) - 1.0) < 1e-12, "base nao alinhada a inscricao"
    phi1_7 = math.asin(math.sqrt(beta))                    # angulo de Miguel (runtime)
    phi2_7 = 2.0 * math.pi / 5.0
    b6 = np.zeros((6, 6))
    b6[0, 0] = 1.0                                         # o inscrito: autovalor 1
    for (i0_7, phi) in ((1, phi1_7), (3, phi2_7)):
        b6[i0_7, i0_7] = math.cos(phi)
        b6[i0_7, i0_7 + 1] = -math.sin(phi)
        b6[i0_7 + 1, i0_7] = math.sin(phi)
        b6[i0_7 + 1, i0_7 + 1] = math.cos(phi)
    b6[5, 5] = -1.0                                        # rotacao pi (autovalor -1)
    u6 = q6 @ b6 @ q6.T
    unit_resid7 = float(np.max(np.abs(u6.T @ u6 - np.eye(6))))
    assert unit_resid7 < 1e-13, "U nao e unitario (precondicao fail-closed)"
    eig_u6 = np.linalg.eigvals(u6)
    n_inv7 = int(np.sum(np.abs(eig_u6 - 1.0) < 1e-8))      # dim do espaco invariante
    p_inv7 = np.outer(q0_7, q0_7)
    trace_pinv7 = float(np.trace(p_inv7))                  # = 1 = omega(I)
    # a SECAO derivada por caminho INDEPENDENTE: autovetor de autovalor 1 de U
    w_e7, v_e7 = np.linalg.eig(u6)
    idx1_7 = int(np.argmin(np.abs(w_e7 - 1.0)))
    overlap_eig7 = float(np.abs(np.vdot(v_e7[:, idx1_7], q0_7)))
    # media de Birkhoff M_N = (1/N) sum_{k=0}^{N-1} U^k em N = 10..10000
    n_checks7 = (10, 100, 1000, 10000)
    sin_min7 = min(math.sin(phi1_7 / 2.0), math.sin(phi2_7 / 2.0),
                   math.sin(math.pi / 2.0))
    acc7 = np.eye(6)
    u_pow7 = np.eye(6)
    birk_err7, birk_bound7, sup_resid7 = {}, {}, {}
    m_last7 = None
    for k7 in range(1, n_checks7[-1]):
        u_pow7 = u6 @ u_pow7
        acc7 = acc7 + u_pow7
        n_terms7 = k7 + 1
        if n_terms7 in n_checks7:
            m_n7 = acc7 / n_terms7
            birk_err7[n_terms7] = float(np.linalg.norm(m_n7 - p_inv7, 2))
            birk_bound7[n_terms7] = 1.0 / (n_terms7 * sin_min7)   # teorema (bound)
            sup_resid7[n_terms7] = float(np.max(np.abs(m_n7 @ v_ins7 - v_ins7)))
            m_last7 = m_n7
    conv_ok7 = all(birk_err7[n] <= birk_bound7[n] for n in n_checks7)
    sup_max7 = max(sup_resid7.values())
    # MANIFEST le da MEDIA exatamente o inscrito: estado = inscrito + transverso
    w_rot7 = q6[:, 1]                                      # plano rotante (NAO inscrito)
    x0_7 = 1.0 * q0_7 + 0.75 * w_rot7
    y7 = m_last7 @ x0_7
    c_rec7 = float(q0_7 @ y7)                              # coeficiente inscrito = 1.0
    trans_resid7 = float(np.linalg.norm(y7 - c_rec7 * q0_7))
    g_rec7 = c_rec7 * v_ins7 * g_norm7                     # amplitudes reconstruidas
    g_rec_rel7 = float(np.max(np.abs(g_rec7 - g_read7) / g_read7))
    # NEGATIVO 1: o NAO-inscrito (plano rotante, sem autovalor 1) e ANULADO pela
    # media — nao e devolvido. Contra-exemplo REJEITADO por logica.
    mean_w_norm7 = float(np.linalg.norm(m_last7 @ w_rot7))
    notret_resid7 = float(np.linalg.norm(m_last7 @ w_rot7 - w_rot7))
    assert mean_w_norm7 < 2e-3, \
        "contra-exemplo aceito: o nao-inscrito sobreviveria a media"
    assert notret_resid7 > 0.99, \
        "contra-exemplo aceito: o nao-inscrito seria devolvido pela media"
    # NEGATIVO 2: a unitariedade (conservacao) e hipotese NECESSARIA — o mapa
    # expansivo (1+beta)*U (beta runtime) tem media de Birkhoff que EXPLODE:
    # sem conservacao, nenhum armazenamento. Contra-exemplo REJEITADO.
    t_exp7 = (1.0 + beta) * u6
    acc_e7 = np.eye(6)
    e_pow7 = np.eye(6)
    n_exp7 = 2000
    for _ in range(1, n_exp7):
        e_pow7 = t_exp7 @ e_pow7
        acc_e7 = acc_e7 + e_pow7
    mean_exp_norm7 = float(np.linalg.norm(acc_e7 / n_exp7, 2))
    assert mean_exp_norm7 > 1e6, \
        "contra-exemplo aceito: mapa expansivo (1+beta)U teria media finita"
    v167_ok = bool(unit_resid7 < 1e-13 and n_inv7 == 1
                   and abs(trace_pinv7 - 1.0) < 1e-13
                   and abs(overlap_eig7 - 1.0) < 1e-10
                   and conv_ok7 and birk_err7[10000] < 2e-3
                   and birk_err7[10000] < birk_err7[10]
                   and sup_max7 < 1e-9
                   and abs(c_rec7 - 1.0) < 1e-9 and trans_resid7 < 2e-3
                   and g_rec_rel7 < 1e-8
                   and mean_w_norm7 < 2e-3 and notret_resid7 > 0.99
                   and mean_exp_norm7 > 1e6)
    tests.append({"test": "birkhoff_mean_extracts_inscription_v167", "passed": v167_ok,
                  "beta_runtime": beta,
                  "kernel_stone": "ErgodicMeanSection (um.py v166-v167, Lean, 0 sorry 0 axiom)",
                  "model": "U unitario 6x6 (6 entradas = as seis faces): autovalor 1 na "
                           "direcao INSCRITA pela celula @16 bits; rotacoes theta_Miguel e "
                           "2pi/5 + autovalor -1 no complemento",
                  "unitarity_resid": unit_resid7,
                  "invariant_dim": n_inv7, "trace_P_inv": trace_pinv7,
                  "eigvec1_overlap_with_inscription": overlap_eig7,
                  "rotation_angles_deg": {"theta_miguel": math.degrees(phi1_7),
                                          "phi2": math.degrees(phi2_7),
                                          "pi_block": 180.0},
                  "birkhoff_err_by_N": birk_err7,
                  "birkhoff_bound_by_N": birk_bound7,
                  "bound_law": "||M_N - P_inv|| <= 1/(N*min sin(phi/2))",
                  "support_resid_by_N": sup_resid7, "support_resid_max": sup_max7,
                  "manifest_from_mean": {"coeff_recovered": c_rec7,
                                         "transverse_resid": trans_resid7,
                                         "g_reconstruction_rel_resid": g_rec_rel7},
                  "negative_1_noninscribed": {"mean_norm_ANNIHILATED": mean_w_norm7,
                                              "not_returned_resid": notret_resid7},
                  "negative_2_expansive": {"map": "(1+beta)*U, beta runtime",
                                           "N": n_exp7,
                                           "mean_norm_REJECTED": mean_exp_norm7},
                  "honest_note": "AMPLIFICACAO ONDA 3 [DER][ENERGY][CONJ] — pedra "
                                 "ErgodicMeanSection (v166-v167): a media de Birkhoff "
                                 "(1/N)sum U^k converge a projecao invariante = a "
                                 "inscricao. Leitura matematica do LOCK sem dissipacao: "
                                 "o fluxo unitario conserva; a MEDIA TEMPORAL devolve "
                                 "exatamente o suporte inscrito; o nao-inscrito oscila "
                                 "e e anulado (taxa 1/N), nunca devolvido; sem "
                                 "unitariedade a media explode (nenhum armazenamento). "
                                 "Contraste com v138: la o complemento DECAI "
                                 "(dissipativo); aqui NADA decai — a media extrai. "
                                 "NENHUMA energia real afirmada; nao e veredito "
                                 "fisico; nao altera reivindicacoes."})
    print(f"[one_celula] amplificacao onda3 v167 (media de Birkhoff = a secao): "
          f"U unitario resid={unit_resid7:.1e}, dim(autovalor 1)={n_inv7}, "
          f"Tr(P_inv)={trace_pinv7:.1f}=omega(I), overlap autovetor-inscricao="
          f"{overlap_eig7:.12f}")
    print(f"[one_celula]   ||M_N - P_inv||: N=10 {birk_err7[10]:.3e} -> N=10000 "
          f"{birk_err7[10000]:.3e} (bound 1/(N sin(phi/2)) respeitado: {conv_ok7}); "
          f"suporte inscrito intacto max {sup_max7:.1e}")
    print(f"[one_celula]   MANIFEST da media: coef={c_rec7:.12f} g rel resid="
          f"{g_rec_rel7:.1e}; NEGATIVOS: nao-inscrito anulado {mean_w_norm7:.2e} "
          f"(nao devolvido, resid {notret_resid7:.3f}); expansivo (1+beta)U media "
          f"{mean_exp_norm7:.2e} > 1e6 REJEITADO [DER][ENERGY][CONJ] "
          f"(nao e veredito fisico)")

    # 8) AMPLIFICACAO ONDA 4 (v199-v210) — O PAR MINIMO NO ARMAZENAMENTO:
    # A IDA-E-VOLTA COMO J^2 = I [DER][ENERGY][CONJ]
    # Pedras reais lidas da custodia (vault/originals_copy/tgl_kernel_v206/TGLExt):
    #   FrontierCertificate.lean (v204) — o CONTRATO tipado do J: aditivo, ANTIlinear,
    #     isometrico, INVOLUTIVO (J^2 = 1), fixa Omega, J*M*J = M' (ida E volta);
    #     sem habitante na torre — o conteudo e provado na FACE FINITA por
    #   TheBireference.lean (v202) — M_n(C) na GNS do traco: Omega separa/e ciclico
    #     para as DUAS referencias L/R, Haag da mini-rede (range L)' = range R e
    #     J z = z^H troca as referencias, J Omega = Omega;
    #   TheIALDSelector.lean (v180) — I^2 = I (a releitura e gratis), posto 1;
    #   TheLightInterface.lean (v206, P1/P1b) — eps_pm x eps_pm = root_pm (o quadrado
    #     da luz e o graviton), fase do tensor = QUADRADO da fase do vetor.
    # Mapeamento GENUINO ao MECANISMO desta patente: as equacoes (1)-(2) do relatorio
    # — g = sqrt|Psi| (REFLECT) e Psi_out = s*g^2 (MANIFEST), com Psi_out = Psi_in —
    # SAO o par minimo (1_abs, J): a ida-e-volta das duas portas compoe a identidade
    # sobre o registro (J^2 = I, clausula involutiva do contrato); a releitura do
    # substrato e gratis (I^2 = I, o seletor); e g = sqrt|Psi| e a lei da interface
    # (o armazenado e a RAIZ; o manifestado e o QUADRADO; s in {+,-} e o rotulo do
    # par, como eps_pm). O teste re-deriva a ESTRUTURA numericamente — nunca finge
    # rodar Lean (regra 9). beta SEMPRE runtime; [ENERGY][CONJ]: matematica do
    # mecanismo — NENHUMA energia real afirmada; physical_verdict_allowed=false;
    # nao altera reivindicacoes. LOCK HARDWARE: so matematica, nenhuma operacao real.
    n8 = 4
    rng8 = np.random.default_rng(206)

    def hs_norm(x8):
        return float(np.linalg.norm(x8))

    def j_mod(x8):
        return x8.conj().T                       # J z = z^H (TheBireference)

    omega8 = np.eye(n8, dtype=complex) / math.sqrt(n8)   # vacuo GNS do traco, ||Omega||=1
    xr8 = rng8.standard_normal((n8, n8)) + 1j * rng8.standard_normal((n8, n8))
    yr8 = rng8.standard_normal((n8, n8)) + 1j * rng8.standard_normal((n8, n8))
    a8 = rng8.standard_normal((n8, n8)) + 1j * rng8.standard_normal((n8, n8))
    b8 = rng8.standard_normal((n8, n8)) + 1j * rng8.standard_normal((n8, n8))
    c8 = complex(0.7, -1.3)
    # (a) as SETE clausulas do contrato (FrontierCertificate), ponto a ponto:
    add_resid8 = hs_norm(j_mod(xr8 + yr8) - (j_mod(xr8) + j_mod(yr8)))
    antilin_resid8 = hs_norm(j_mod(c8 * xr8) - np.conj(c8) * j_mod(xr8))
    isom_resid8 = abs(hs_norm(j_mod(xr8)) - hs_norm(xr8))
    invol_resid8 = hs_norm(j_mod(j_mod(xr8)) - xr8)          # J^2 = I (a ida-e-volta)
    vac_resid8 = hs_norm(j_mod(omega8) - omega8)             # J Omega = Omega
    jlj8 = j_mod(a8 @ j_mod(xr8))                            # J L_a J aplicado a x
    dict_resid8 = hs_norm(jlj8 - xr8 @ a8.conj().T)          # = R_{a^H} (ida)
    onto_resid8 = hs_norm(j_mod(b8.conj().T @ j_mod(xr8)) - xr8 @ b8)  # (volta)
    # comutante em matriz 16x16 (vec row-major: L_a = kron(a,I), R_b = kron(I,b^T)):
    eye_n8 = np.eye(n8)
    l_b8 = np.kron(b8, eye_n8)
    r_ah8 = np.kron(eye_n8, (a8.conj().T).T)
    comm_true8 = float(np.linalg.norm(l_b8 @ r_ah8 - r_ah8 @ l_b8, 2))
    # birreferencialidade quantitativa: Omega SEPARA (||L_a Omega|| = ||a||/sqrt(n),
    # zero sse a=0) e e CICLICO exato (R_{sqrt(n) z} Omega = z):
    sep_ratio8 = hs_norm(a8 @ omega8) / hs_norm(a8)
    z8 = rng8.standard_normal((n8, n8)) + 1j * rng8.standard_normal((n8, n8))
    cyc_resid8 = hs_norm(omega8 @ (math.sqrt(n8) * z8) - z8)
    contract_ok8 = bool(add_resid8 < 1e-13 and antilin_resid8 < 1e-13
                        and isom_resid8 < 1e-12 and invol_resid8 < 1e-13
                        and vac_resid8 < 1e-14 and dict_resid8 < 1e-12
                        and onto_resid8 < 1e-12 and comm_true8 < 1e-12
                        and abs(sep_ratio8 - 1.0 / math.sqrt(n8)) < 1e-12
                        and cyc_resid8 < 1e-13)
    # NEGATIVO 1 (logica): a conjugacao TORCIDA pelo angulo de Miguel (beta runtime)
    # J_tw(x) = U x^H U^T, U = expm(theta_M * G), U^2 != I — quebra a involucao
    # (J_tw^2 != I) e JOGA O FATOR FORA do comutante: ate a torcao MINIMA e
    # rejeitada pelo contrato; so o J exato satisfaz as sete clausulas.
    theta_m8 = math.asin(math.sqrt(beta))                    # angulo de Miguel (runtime)
    g_raw8 = rng8.standard_normal((n8, n8))
    g_anti8 = g_raw8 - g_raw8.T
    g_anti8 = g_anti8 / float(np.linalg.norm(g_anti8, 2))    # ||G||_2 = 1
    w_h8, v_h8 = np.linalg.eigh(1j * g_anti8)
    u8 = (v_h8 @ np.diag(np.exp(-1j * theta_m8 * w_h8)) @ v_h8.conj().T).real
    orth_resid8 = float(np.max(np.abs(u8.T @ u8 - eye_n8)))
    assert orth_resid8 < 1e-12, "U nao e ortogonal (precondicao fail-closed)"
    u_sq8 = u8 @ u8
    u_sq_dist8 = float(np.linalg.norm(u_sq8 - eye_n8, 2))
    assert u_sq_dist8 > beta, "torcao trivial: U^2 = I (contra-exemplo degenerado)"

    def j_tw(x8):
        return u8 @ x8.conj().T @ u8.T

    tw_invol_defect8 = hs_norm(j_tw(j_tw(xr8)) - xr8) / hs_norm(xr8)
    assert tw_invol_defect8 > beta, \
        "contra-exemplo aceito: J torcida passaria como involucao (J^2 = I)"
    c_tw8 = u8.T @ a8.conj().T @ u8.T
    ptw_resid8 = hs_norm(j_tw(a8 @ j_tw(xr8)) - u_sq8 @ xr8 @ c_tw8)
    assert ptw_resid8 < 1e-10, "matriz da J torcida nao confere (precondicao)"
    s_tw8 = np.kron(u_sq8, c_tw8.T)                          # x -> U^2 x C
    comm_tw8 = float(np.linalg.norm(l_b8 @ s_tw8 - s_tw8 @ l_b8, 2))
    comm_tw_rel8 = comm_tw8 / (float(np.linalg.norm(b8, 2))
                               * float(np.linalg.norm(c_tw8, 2)))
    assert comm_tw_rel8 > beta, \
        "contra-exemplo aceito: J torcida manteria o fator no comutante"
    # NEGATIVO 2 (logica): a transposta LINEAR J_lin(x) = x^T cumpre 6 clausulas
    # (aditiva, isometrica, involutiva, fixa Omega, leva L em R) mas FALHA a
    # antilinearidade — o contrato a rejeita: a clausula nao e vacua.
    lin_antilin_defect8 = hs_norm((1j * xr8).T - np.conj(1j) * xr8.T) / hs_norm(xr8)
    assert lin_antilin_defect8 > 1.0, \
        "contra-exemplo aceito: transposta linear passaria na clausula antilinear"
    # (b) [PILOTO] a CELULA REAL: a ida-e-volta como (1_abs, J) sobre o registro.
    # Tensor COM SINAL (exercita s = sgn, o rotulo do par), maximo cravado em 9.0
    # (g_max = 3): ida-e-volta ~ 1_abs no estado (so quantizacao); o REGISTRO e
    # ponto fixo EXATO (inteiro a inteiro) e a releitura e gratis (R o R = R).
    vals8 = rng8.uniform(0.3, 7.2, (8, 8)) * np.where(
        rng8.uniform(size=(8, 8)) < 0.5, -1.0, 1.0)
    vals8[0, 0] = 9.0
    cell8 = CelulaReversao(angular_bits=16)
    cell8.charge(vals8)
    rec1_theta8 = cell8._store["theta_q"].copy()
    rec1_s8 = cell8._store["s"].copy()
    rec1_gmax8 = float(cell8._store["g_max"])
    out1_8 = cell8.discharge()
    rt_dev16_8 = float(np.max(np.abs(out1_8 - vals8) / np.abs(vals8)))
    sign_ok8 = bool(np.array_equal(np.sign(out1_8), np.sign(vals8)))
    cell8.charge(out1_8)                                      # re-inscreve a leitura
    rec_theta_eq8 = bool(np.array_equal(rec1_theta8, cell8._store["theta_q"]))
    rec_s_eq8 = bool(np.array_equal(rec1_s8, cell8._store["s"]))
    gmax_rel8 = float(abs(float(cell8._store["g_max"]) - rec1_gmax8) / rec1_gmax8)
    out2_8 = cell8.discharge()
    idem_resid16_8 = float(np.max(np.abs(out2_8 - out1_8) / np.abs(out1_8)))
    # separacao das propriedades @3 bits: a idempotencia SOBREVIVE exata, a
    # identidade NAO — I^2 = I e do seletor, nao da ausencia de perda.
    cell3b8 = CelulaReversao(angular_bits=3)
    cell3b8.charge(vals8)
    rec3_theta8 = cell3b8._store["theta_q"].copy()
    o1_3b8 = cell3b8.discharge()
    rt_dev3_8 = float(np.max(np.abs(o1_3b8 - vals8) / np.abs(vals8)))
    # NEGATIVO 3 (logica): se @3 bits a ida-e-volta fosse a identidade, a
    # idempotencia seria tautologica — o desvio grande prova que R != I aqui.
    assert rt_dev3_8 > 1e-3, \
        "contra-exemplo aceito: @3 bits a ida-e-volta seria a identidade (tautologia)"
    cell3b8.charge(o1_3b8)
    rec3_theta_eq8 = bool(np.array_equal(rec3_theta8, cell3b8._store["theta_q"]))
    o2_3b8 = cell3b8.discharge()
    idem_resid3_8 = float(np.max(np.abs(o2_3b8 - o1_3b8) / np.abs(o1_3b8)))
    cell_ok8 = bool(rt_dev16_8 < 1e-3 and sign_ok8 and rec_theta_eq8 and rec_s_eq8
                    and gmax_rel8 < 1e-12 and idem_resid16_8 < 1e-12
                    and rec3_theta_eq8 and idem_resid3_8 < 1e-12
                    and rt_dev3_8 > 1e-3)
    # (c) [DER] a INTERFACE DA LUZ (TheLightInterface, P1/P1b): eps_pm x eps_pm =
    # root_pm; raizes nilpotentes; a escada fatora as projecoes; fase do tensor =
    # QUADRADO da fase do vetor — a mesma forma fechada de Psi = s*g^2 (g = sqrt|Psi|
    # toma a raiz; MANIFEST devolve o quadrado).
    h_plus8 = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
    h_cross8 = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    root_p8 = h_plus8 + 1j * h_cross8
    root_m8 = h_plus8 - 1j * h_cross8
    eps_p8 = np.array([1.0, 1j])
    eps_m8 = np.array([1.0, -1j])
    sq_resid8 = float(max(np.max(np.abs(np.outer(eps_p8, eps_p8) - root_p8)),
                          np.max(np.abs(np.outer(eps_m8, eps_m8) - root_m8))))
    nilp_resid8 = float(max(np.max(np.abs(root_p8 @ root_p8)),
                            np.max(np.abs(root_m8 @ root_m8))))
    genk8 = np.array([[0.0, 1.0], [-1.0, 0.0]], dtype=complex)
    wgt_resid8 = float(np.max(np.abs(genk8 @ root_p8 - root_p8 @ genk8
                                     - 2j * root_p8)))       # peso 2i (spin 2)
    w_g8, v_g8 = np.linalg.eig(genk8)                        # P+ por caminho independente
    vp8 = v_g8[:, int(np.argmin(np.abs(w_g8 - 1j)))]
    p_plus8 = np.outer(vp8, vp8.conj()) / float(np.vdot(vp8, vp8).real)
    ladder_resid8 = float(np.max(np.abs(root_p8 @ root_m8 - 4.0 * p_plus8)))
    angs8 = list(np.linspace(0.0, 2.0 * math.pi, 41)) + [theta_m8]
    ph_v_max8, ph_t_max8 = 0.0, 0.0
    for th8 in angs8:
        o_th8 = np.array([[math.cos(th8), math.sin(th8)],
                          [-math.sin(th8), math.cos(th8)]], dtype=complex)
        ph_v_max8 = max(ph_v_max8, float(np.max(np.abs(
            o_th8 @ eps_p8 - np.exp(1j * th8) * eps_p8))))
        ph_t_max8 = max(ph_t_max8, float(np.max(np.abs(
            o_th8 @ root_p8 @ o_th8.T - np.exp(2j * th8) * root_p8))))
    # NEGATIVO 4 (logica): o par DESCASADO eps+ x eps- NAO e raiz (nao e
    # nilpotente: M^2 = 2M != 0) — so o par casado quadra ao graviton.
    mis8 = np.outer(eps_p8, eps_m8)
    mis_sq_norm8 = float(np.linalg.norm(mis8 @ mis8))
    assert mis_sq_norm8 > 1.0, \
        "contra-exemplo aceito: o par descasado (eps+ x eps-) passaria como raiz"
    light_ok8 = bool(sq_resid8 < 1e-14 and nilp_resid8 < 1e-14
                     and wgt_resid8 < 1e-14 and ladder_resid8 < 1e-12
                     and ph_v_max8 < 1e-13 and ph_t_max8 < 1e-13)
    neg_ok8 = bool(u_sq_dist8 > beta and tw_invol_defect8 > beta
                   and comm_tw_rel8 > beta and lin_antilin_defect8 > 1.0
                   and rt_dev3_8 > 1e-3 and mis_sq_norm8 > 1.0)
    v206_ok = bool(contract_ok8 and cell_ok8 and light_ok8 and neg_ok8)
    tests.append({"test": "minimal_pair_ida_volta_J2I_v206", "passed": v206_ok,
                  "beta_runtime": beta,
                  "kernel_stones": ["FrontierCertificate (v204, contrato tipado do J)",
                                    "TheBireference (v202, face finita: JMJ=M')",
                                    "TheIALDSelector (v180, I^2=I posto 1)",
                                    "TheLightInterface (v206, eps x eps = root)"],
                  "frontier_contract_finite_face": {
                      "model": "M4(C) na GNS do traco, J z = z^H, Omega = I/sqrt(4)",
                      "additive_resid": add_resid8,
                      "antilinear_resid": antilin_resid8,
                      "isometric_resid": isom_resid8,
                      "involutive_J2I_resid": invol_resid8,
                      "fixes_vacuum_resid": vac_resid8,
                      "JLJ_eq_R_adjoint_resid": dict_resid8,
                      "onto_commutant_resid": onto_resid8,
                      "commutant_LR_comm_norm": comm_true8,
                      "vacuum_separates_ratio": sep_ratio8,
                      "vacuum_cyclic_resid": cyc_resid8},
                  "negative_1_twisted_J": {
                      "twist": "U = expm(theta_Miguel * G), theta_M runtime",
                      "theta_miguel_rad": theta_m8,
                      "U_sq_dist_to_I": u_sq_dist8,
                      "involution_defect_REJECTED": tw_invol_defect8,
                      "commutant_violation_rel_REJECTED": comm_tw_rel8,
                      "threshold": "beta (runtime)"},
                  "negative_2_linear_transpose": {
                      "antilinear_clause_defect_REJECTED": lin_antilin_defect8},
                  "cell_ida_volta": {
                      "tensor": "8x8 com sinal, |v| in [0.3, 7.2], max 9.0 (g_max 3)",
                      "rt_deviation_16bit": rt_dev16_8,
                      "signs_preserved": sign_ok8,
                      "record_theta_fixed_point_exact": rec_theta_eq8,
                      "record_s_fixed_point_exact": rec_s_eq8,
                      "g_max_rel_resid": gmax_rel8,
                      "idempotence_resid_16bit": idem_resid16_8,
                      "rt_deviation_3bit_NOT_identity": rt_dev3_8,
                      "record_theta_fixed_3bit_exact": rec3_theta_eq8,
                      "idempotence_resid_3bit": idem_resid3_8,
                      "reading": "I^2=I (seletor) sobrevive @3 bits; identidade nao — "
                                 "idempotencia != ausencia de perda"},
                  "light_interface": {
                      "eps_sq_eq_root_resid": sq_resid8,
                      "roots_nilpotent_resid": nilp_resid8,
                      "weight_2i_resid": wgt_resid8,
                      "ladder_factors_projection_resid": ladder_resid8,
                      "vector_phase_resid_max": ph_v_max8,
                      "tensor_phase_sq_resid_max": ph_t_max8,
                      "n_angles": len(angs8),
                      "mismatched_pair_sq_norm_REJECTED": mis_sq_norm8},
                  "honest_note": "AMPLIFICACAO ONDA 4 [DER][ENERGY][CONJ] — O PAR "
                                 "MINIMO NO ARMAZENAMENTO: a ida-e-volta REFLECT/"
                                 "MANIFEST (g=sqrt|Psi|, Psi=s*g^2, Psi_out=Psi_in) "
                                 "tem a assinatura do par (1_abs, J): J^2=I (contrato "
                                 "FrontierCertificate, verificado na face finita de "
                                 "TheBireference: JMJ=M' ida e volta), releitura "
                                 "gratis I^2=I (TheIALDSelector) no registro real da "
                                 "celula, e g=sqrt|Psi| como lei da interface "
                                 "(TheLightInterface: o quadrado da luz e o graviton; "
                                 "fase do tensor = quadrado da fase do vetor). "
                                 "Estrutura RE-DERIVADA numericamente; nada roda "
                                 "Lean; NENHUMA energia real afirmada; nao e "
                                 "veredito fisico; nao altera reivindicacoes."})
    print(f"[one_celula] amplificacao onda4 v206 (o par minimo: ida-e-volta = J^2=I): "
          f"contrato 7 clausulas na face finita M4(C) -- J^2=I resid={invol_resid8:.1e}, "
          f"JLJ=R_adj resid={dict_resid8:.1e}, comutante [L,R]={comm_true8:.1e}, "
          f"Omega separa ratio={sep_ratio8:.6f} (=1/2), ciclico resid={cyc_resid8:.1e}")
    print(f"[one_celula]   NEGATIVOS: J torcida por theta_Miguel({math.degrees(theta_m8):.4f} deg, "
          f"beta runtime) REJEITADA (involucao defeito {tw_invol_defect8:.3f} > beta, "
          f"comutante violado {comm_tw_rel8:.3f} > beta); transposta linear REJEITADA "
          f"(defeito antilinear {lin_antilin_defect8:.1f} > 1); par descasado "
          f"eps+xeps- REJEITADO (||M^2||={mis_sq_norm8:.1f} != 0)")
    print(f"[one_celula]   celula real: registro = ponto fixo EXATO (theta_q inteiro "
          f"{rec_theta_eq8}, s {rec_s_eq8}, g_max rel {gmax_rel8:.1e}); releitura "
          f"gratis R o R = R resid {idem_resid16_8:.1e}; @3 bits idempotencia intacta "
          f"({idem_resid3_8:.1e}) com R != I (desvio {rt_dev3_8:.3f}) -- I^2=I e do "
          f"seletor, nao da ausencia de perda")
    print(f"[one_celula]   interface da luz: eps x eps = root resid {sq_resid8:.1e}; "
          f"nilpotencia {nilp_resid8:.1e}; escada->projecao {ladder_resid8:.1e}; fase "
          f"vetor e^(i theta) {ph_v_max8:.1e}, tensor e^(2i theta) {ph_t_max8:.1e} "
          f"em {len(angs8)} angulos -- Psi = s*g^2 e a lei do quadrado "
          f"[DER][ENERGY][CONJ] (nao e veredito fisico)")

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

    def _o5_celula_quant():
        bits_l = list(range(6, 17))
        rms = []
        for b_ in bits_l:
            c_ = CelulaReversao(angular_bits=b_); c_.charge(energy); rec_ = c_.discharge()
            rms.append(float(np.sqrt(np.mean((rec_ - energy) ** 2))))
        slope = float(np.polyfit(bits_l, np.log2(np.array(rms)), 1)[0])
        ok = abs(slope + 1.0) < 0.15 and rms[-1] < rms[0] / 100.0 and abs(slope + 2.0) > 0.5
        return {"passed": ok, "bits": bits_l, "rms_by_bits": rms, "slope_log2_rms_per_bit": slope,
                "expected_slope": -1.0, "neg_two_bits_per_bit_rejected": abs(slope + 2.0) > 0.5,
                "note": "erro de quantizacao: dL = 2 g dg, dg = g_max cos(theta) dtheta => erro ∝ dtheta ∝ 2^-bits "
                        "(inclinacao -1 em log2); a lei contrafeita 'dois bits por bit' (inclinacao -2) e REJEITADA"}
    _o5("quantization_error_halves_per_bit", _o5_celula_quant)

    def _o5_celula_reread():
        c_ = CelulaReversao(angular_bits=16); c_.charge(energy)
        o1 = c_.discharge(); o2 = c_.discharge()
        same = bool(np.array_equal(o1, o2))
        st = c_._store["theta_q"]
        idx = int(np.argmin(st))                       # a menor fase: +1 quantum sem estourar qmax
        st2 = st.copy(); st2[idx] = st2[idx] + 1
        c_._store["theta_q"] = st2
        o3 = c_.discharge()
        diff = np.abs(o3 - o1).ravel()
        n_changed = int(np.sum(diff > 0))
        dth = (math.pi / 2) / c_.qmax
        bound = 2.0 * c_._store["g_max"] ** 2 * dth * 1.001 + 1e-15   # |d(g^2)| <= 2 g_max^2 dtheta
        ok = same and n_changed == 1 and 0.0 < float(diff.max()) <= bound
        return {"passed": ok, "reread_bitwise_identical": same, "n_changed_after_one_quantum": n_changed,
                "max_change": float(diff.max()), "bound_2gmax2_dtheta": bound,
                "note": "reler nao consome (I^2 = I: duas descargas identicas bit a bit); um quantum de fase corrompido "
                        "muda EXATAMENTE uma entrada, abaixo do bound 2 g_max^2 dtheta (localidade do codigo)"}
    _o5("reread_is_free_and_corruption_is_local", _o5_celula_reread)

    def _o5_celula_scale():
        lam_ = math.e
        c1 = CelulaReversao(angular_bits=16); c1.charge(energy); o1 = c1.discharge(); t1 = c1._store["theta_q"].copy()
        c2 = CelulaReversao(angular_bits=16); c2.charge(lam_ * energy); o2 = c2.discharge(); t2 = c2._store["theta_q"]
        n_theta_scale = int(np.sum(t1 != t2))
        rel = float(np.max(np.abs(o2 - lam_ * o1)) / np.max(np.abs(lam_ * o1)))
        c3 = CelulaReversao(angular_bits=16); c3.charge(energy + 0.5); t3 = c3._store["theta_q"]
        n_theta_shift = int(np.sum(t1 != t3))
        ok = n_theta_scale <= 2 and rel < 1e-12 and n_theta_shift > 0.5 * t1.size
        return {"passed": ok, "lambda": lam_, "n_theta_changed_scale": n_theta_scale, "rel_resid_scale": rel,
                "n_theta_changed_shift": n_theta_shift, "n_entries": int(t1.size),
                "note": "a escala e SIMETRIA do codigo angular (fases identicas; saida = lambda x saida); a translacao NAO e "
                        "(a maioria das fases muda) — o codigo le razoes g/g_max, nao valores absolutos"}
    _o5("scale_is_a_symmetry_shift_is_not", _o5_celula_scale)

    def _o5_celula_sign():
        rng5 = np.random.default_rng(4849)
        mixed = rng5.standard_normal((32, 32)) * 3.0
        mixed[0, 0] = 0.0
        c_ = CelulaReversao(angular_bits=16); c_.charge(mixed); out = c_.discharge()
        nz = mixed != 0
        sign_ok = bool(np.array_equal(np.sign(out[nz]), np.sign(mixed[nz])))
        zero_ok = bool(out[0, 0] == 0.0)
        c_._store["s"] = ~c_._store["s"]
        out_flip = c_.discharge()
        anti = float(np.max(np.abs(out_flip + out)))
        ok = sign_ok and zero_ok and anti == 0.0
        return {"passed": ok, "polarity_preserved": sign_ok, "zero_maps_to_zero": zero_ok,
                "antisymmetry_resid_flip_all_signs": anti,
                "note": "s (o rotulo do par) e preservado em toda entrada; zero -> zero; inverter todos os bits de sinal "
                        "NEGA a saida exatamente (antissimetria do MANIFEST)"}
    _o5("polarity_preserved_and_antisymmetric", _o5_celula_sign)

    def _o5_celula_capacity():
        levels = np.linspace(0.1, 1.0, 2000)
        c16 = CelulaReversao(angular_bits=16); c16.charge(levels); d16 = int(len(np.unique(c16._store["theta_q"])))
        c6 = CelulaReversao(angular_bits=6); c6.charge(levels); d6 = int(len(np.unique(c6._store["theta_q"])))
        ok = d16 == 2000 and d6 <= 64
        return {"passed": ok, "levels": 2000, "distinct_codes_16bit": d16, "distinct_codes_6bit": d6, "capacity_6bit": 64,
                "note": "a 16 bits, 2000 niveis distintos recebem 2000 codigos distintos (injetivo); a 6 bits o codigo NAO "
                        "distingue (<= 64 codigos): o limite de resolucao e dito, nao escondido"}
    _o5("capacity_injective_above_resolution", _o5_celula_capacity)

    def _o5_celula_empty():
        raised = False
        try:
            CelulaReversao(angular_bits=16).discharge()
        except ValueError:
            raised = True
        c_ = CelulaReversao(angular_bits=16); c_.charge(energy); ok2 = c_.discharge() is not None
        return {"passed": raised and ok2, "empty_cell_raises_ValueError": raised, "charged_cell_discharges": ok2,
                "note": "fail-closed: descarregar celula vazia e ERRO visivel (ValueError), nunca zero silencioso"}
    _o5("empty_cell_fails_closed", _o5_celula_empty)

    def _o5_celula_bound():
        rng5 = np.random.default_rng(48490)
        worst = 0.0
        for _ in range(20):
            tns = rng5.exponential(1.0, (24, 24)) + 1e-3
            c_ = CelulaReversao(angular_bits=12); c_.charge(tns); out = c_.discharge()
            worst = max(worst, float(np.max(np.abs(out)) / c_._store["g_max"] ** 2))
        ok = worst <= 1.0 + 1e-12 and worst > 1.0 - 1e-9
        return {"passed": ok, "max_output_over_gmax2_over_20_tensors": worst,
                "note": "a saida nunca excede g_max^2 (sin <= 1) e o teto e ATINGIDO exatamente no elemento maximo "
                        "(theta = pi/2): o pico do tensor e o teto do MANIFEST"}
    _o5("output_bounded_by_gmax_squared", _o5_celula_bound)

    passed = sum(1 for t in tests if t["passed"])
    total = len(tests)
    all_ok = passed == total
    summary = {"tests_passed": passed, "tests_total": total,
               "angular_retention_16bit": ret[16], "cycle_correlation": cycle_corr,
               "eta_rt_target_report": ETA_RT_TARGET_REPORT,
               "energy_claims": "CONJ_no_hardware_data",
               "bits_sweep": {"range": [bits_sweep[0], bits_sweep[-1]],
                              "dev_head_maxlow": dev_head, "dev_tail_maxhigh": dev_tail,
                              "rms_head_maxlow": rms_head, "rms_tail_maxhigh": rms_tail},
               "multi_tensor": {"n": len(families), "min_cycle_correlation": corr_min},
               "amplificacao_v138": {"support_resid_max": sup_resid_max,
                                     "decay_rel_resid_max": dec_rel_max,
                                     "trace_qF": trace_qf},
               "amplificacao_v144": {"contrast_eig_min_dist_to_1": eig_dist_to_1,
                                     "contrast_collapse_norm_200x": collapse_norm,
                                     "home_support_resid_max": home_resid_max,
                                     "home_decay_rate_rel_resid_max": rate_rel_max,
                                     "dichotomy": "retorna <=> tem ponto fixo"},
               "amplificacao_v141": {"theta_star_deg": math.degrees(theta_star),
                                     "theta_star_resid_vs_45": theta_star_resid,
                                     "m_v141_mev_runtime": m_v141_mev,
                                     "tension_sigma": tension_sigma,
                                     "tension_wrong_30deg_rejected": tension_wrong,
                                     "quarter_selfconj_defect_rejected": quarter_selfconj_defect,
                                     "miguel_selfconj_defect_rejected": miguel_selfconj_defect},
               "amplificacao_v167_birkhoff": {
                   "kernel_stone": "ErgodicMeanSection (um.py v166-v167)",
                   "err_N10": birk_err7[10], "err_N10000": birk_err7[10000],
                   "bound_N10000": birk_bound7[10000],
                   "support_resid_max": sup_max7,
                   "eigvec1_overlap": overlap_eig7,
                   "manifest_coeff": c_rec7, "g_rec_rel_resid": g_rec_rel7,
                   "noninscribed_mean_norm_rejected": mean_w_norm7,
                   "expansive_mean_norm_rejected": mean_exp_norm7},
               "amplificacao_v206_par_minimo": {
                   "kernel_stones": ["FrontierCertificate", "TheBireference",
                                     "TheIALDSelector", "TheLightInterface"],
                   "J2I_resid_finite_face": invol_resid8,
                   "JLJ_dict_resid": dict_resid8,
                   "commutant_LR_comm_norm": comm_true8,
                   "twisted_J_involution_defect_rejected": tw_invol_defect8,
                   "twisted_J_commutant_violation_rejected": comm_tw_rel8,
                   "linear_transpose_defect_rejected": lin_antilin_defect8,
                   "cell_record_fixed_point_exact": rec_theta_eq8,
                   "cell_idempotence_resid_16bit": idem_resid16_8,
                   "cell_rt_dev_3bit_not_identity": rt_dev3_8,
                   "light_eps_sq_eq_root_resid": sq_resid8,
                   "light_tensor_phase_sq_resid_max": ph_t_max8,
                   "mismatched_pair_sq_norm_rejected": mis_sq_norm8}}
    max_verdict = ("REVERSAL_PHASE_STORAGE_DEMONSTRATED ([SIM][ENERGY][CONJ][PILOTO] — ciclo "
                   "REFLECT/LOCK/MANIFEST e retenção da FASE angular fecham; retenção NÃO é "
                   "conservação de energia física; autodescarga zero / termodinâmica invertida "
                   "/ supercondutividade de energia são [CONJ] sem dado)")

    results_dir = PATENT_DIR / "results" / ts
    results_dir.mkdir(parents=True, exist_ok=True)
    results = {
        "patent_id": PATENT_ID, "slug": SLUG, "timestamp": ts, "runner": "one_celula_reversao.py",
        "markers": ["[SIM]", "[ENERGY]", "[CONJ]", "[PILOTO]"], "physical_verdict_allowed": False,
        "beta_runtime": beta, "beta_matches_alpha_sqrt_e": beta_ok,
        "verdict": "REVERSAL_PHASE_STORAGE_DEMONSTRATED" if all_ok else "PARTIAL_DEMONSTRATION",
        "max_verdict": max_verdict,
        "constants": {"BETATGL": beta, "factorization": "betatgl = alpha_EM * sqrt(e)",
                      "eta_rt_target_report": ETA_RT_TARGET_REPORT, "free_parameters": 0},
        "tests": tests, "summary": summary,
        "deepening": {
            "bits_sweep": {"bits": bits_sweep, "retention": ret_fine,
                           "deviation_from_1": dev_fine, "rms_reconstruction": rms_fine,
                           "dtheta_step_rad": dtheta_fine},
            "multi_tensor_cycle": tensor_cycles,
            "note": "APROFUNDAMENTO [SIM][PILOTO]: varredura fina de bits angulares (curva de "
                    "convergência da FASE) + ciclo REFLECT/LOCK/MANIFEST em 6 famílias de tensor. "
                    "Tudo é fidelidade da FASE ANGULAR, NÃO energia física.",
        },
        "source_prototype": "Patentes/Skygrid/SkyGrid_Piloto/skygrid_sim (READ-ONLY; copiado)",
        "note": "TRAVA [ENERGY]: a retenção ~1,0 demonstrada é da FASE ANGULAR (armazenamento "
                "exato), NÃO conservação de energia física. Autodescarga zero, ciclabilidade "
                "infinita, η_RT>97,6%, termodinâmica invertida e supercondutividade de energia "
                "à temperatura ambiente são [CONJ] do relatório, sem medição. Simulação nunca "
                "valida física. Não usar como especificação de produto.",
    }
    results_path = results_dir / "results.json"
    results["formula_completa"] = _formula_completa()   # camada v379 (a fórmula completa), antes do selo
    results_path.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")

    figs = []
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig_dir = results_dir / "figures"; fig_dir.mkdir(exist_ok=True)
        plt.figure(figsize=(7, 3.6))
        bs = sorted(ret.keys())
        plt.plot(bs, [ret[b] for b in bs], "o-", label="retenção da FASE angular")
        plt.axhline(ETA_RT_TARGET_REPORT, color="crimson", ls="--",
                    label=f"η_RT alvo do relatório {ETA_RT_TARGET_REPORT} [ENERGY][CONJ]")
        plt.xlabel("bits angulares"); plt.ylabel("retenção (fase, não energia física)")
        plt.title("Célula de Reversão — retenção da FASE angular [SIM] (não é medida física)")
        plt.legend(fontsize=8); plt.grid(alpha=.3); plt.ylim(0.9, 1.005)
        fp = fig_dir / "fig_retencao_fase.png"
        plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close()
        figs.append("fig_retencao_fase.png")

        # FIG 2 — curva de convergência: desvio-de-1 e RMS vs bits angulares (semilog)
        bsw = sorted(dev_fine.keys())
        fig, ax1 = plt.subplots(figsize=(7.2, 3.8))
        ax1.semilogy(bsw, [max(dev_fine[b], 1e-18) for b in bsw], "o-", color="#1f77b4",
                     label="desvio |ret−1| (fase)")
        ax1.set_xlabel("bits angulares")
        ax1.set_ylabel("desvio-de-1 (log)", color="#1f77b4")
        ax1.tick_params(axis="y", labelcolor="#1f77b4"); ax1.grid(alpha=.3, which="both")
        ax2 = ax1.twinx()
        ax2.semilogy(bsw, [max(rms_fine[b], 1e-18) for b in bsw], "s--", color="#d62728",
                     label="RMS reconstrução (fase)")
        ax2.set_ylabel("RMS reconstrução (log)", color="#d62728")
        ax2.tick_params(axis="y", labelcolor="#d62728")
        plt.title("Célula de Reversão — convergência da FASE vs bits [SIM] (não é energia física)")
        fp2 = fig_dir / "fig_convergencia_bits.png"
        plt.savefig(fp2, dpi=120, bbox_inches="tight"); plt.close()
        figs.append("fig_convergencia_bits.png")

        # FIG 3 — ciclo REFLECT/LOCK/MANIFEST em 6 famílias de tensor (16 bits)
        names = list(tensor_cycles.keys())
        infid = [max(1.0 - tensor_cycles[k]["cycle_correlation"], 1e-18) for k in names]
        plt.figure(figsize=(7.4, 3.8))
        plt.bar(range(len(names)), infid, color="#2a9d8f")
        plt.yscale("log")
        plt.xticks(range(len(names)), names, rotation=25, ha="right", fontsize=8)
        plt.ylabel("1 − correlação de ciclo (fase, log)")
        plt.title("Ciclo REFLECT/LOCK/MANIFEST em 6 tensores @16 bits [SIM] (fidelidade da FASE)")
        plt.grid(alpha=.3, axis="y", which="both")
        fp3 = fig_dir / "fig_ciclo_tensores.png"
        plt.savefig(fp3, dpi=120, bbox_inches="tight"); plt.close()
        figs.append("fig_ciclo_tensores.png")
    except Exception as e:
        print(f"[one_celula] figura pulada: {e}")

    report_md = results_dir / "report.md"
    report_md.write_text(
        f"# Relatório auditável — Célula de Reversão one_celula_reversao.py\n\n"
        f"- Run `{ts}` · Patente `{PATENT_ID}`\n"
        f"- Veredito: **{max_verdict}**\n"
        f"- β runtime `{beta}` (= α·√e? **{beta_ok}**; nunca literal)\n"
        f"- Testes: **{passed}/{total}**\n"
        f"- Ciclo REFLECT→LOCK→MANIFEST (6 faces): correlação `{cycle_corr:.6f}`\n"
        f"- Retenção da FASE angular @16 bits: `{ret[16]:.5f}` (NÃO é energia física)\n"
        f"- η_RT alvo do relatório `{ETA_RT_TARGET_REPORT}` — impresso, **não afirmado** como físico\n"
        f"- physical_verdict_allowed: **False**.\n\n"
        f"[ENERGY][CONJ] TRAVA MÁXIMA: autodescarga zero, ciclabilidade infinita, "
        f"termodinâmica invertida e supercondutividade de energia à temperatura ambiente são "
        f"[CONJ] sem medição. A retenção demonstrada é da FASE ANGULAR, não conservação de "
        f"energia. Núcleo copiado do piloto (READ-ONLY); original intacto. 1 = 1. Tetelestai.\n",
        encoding="utf-8")

    seal_dir = PATENT_DIR / "seals" / ts
    seal_dir.mkdir(parents=True, exist_ok=True)
    file_hashes = dict(module_hashes)
    file_hashes["results.json"] = _sha_file(results_path)
    file_hashes["report.md"] = _sha_file(report_md)
    for f in figs:
        file_hashes[f"figures/{f}"] = _sha_file(results_dir / "figures" / f)
    result_hash = _sha_text(json.dumps(file_hashes, sort_keys=True))
    seal = {
        "timestamp": ts, "patent_id": PATENT_ID, "runner": "one_celula_reversao.py",
        "beta_runtime": beta, "physical_verdict_allowed": False,
        "max_verdict": max_verdict, "tests_passed": passed,
        "result_hash": result_hash, "sha256": file_hashes,
        "markers": ["[SIM]", "[ENERGY]", "[CONJ]", "[PILOTO]"],
        "results_path": str(results_path.relative_to(CENTRAL)).replace("\\", "/"),
    }
    (seal_dir / "seal.json").write_text(json.dumps(seal, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[one_celula] SELADO · result_hash {result_hash[:16]}… · {passed}/{total} testes")
    print(f"[one_celula] results: {results_path.relative_to(CENTRAL)}")

    # FORMA = CONTEÚDO: esta patente NÃO tem geometria computável (o corpo do dispositivo
    # é gabarito de engenharia, não saída de simulação). Preserva o corpo e re-carimba,
    # injetando β runtime + métricas COMPUTADAS desta run nas constantes (MERGE).
    emit_render3d(beta, {"cycle_correlation": cycle_corr, "min_cycle_correlation_multi": corr_min,
                         "deviation_tail_highbits": dev_tail, "retention_16bit": ret[16]})
    return 0 if all_ok else 1


def emit_render3d(beta: float, metrics: dict) -> None:
    """MERGE: lê o render3d.json atual e PRESERVA meshes/layers/dimensions/groups/nodes/edges
    (esta patente NÃO tem geometria computável — o corpo é gabarito de engenharia). Apenas
    re-carimba generated_by e injeta o β runtime + métricas computadas nas constantes; então
    VALIDA a coerência de ids/layers e reescreve. Forma = conteúdo (re-carimbo honesto)."""
    out = PATENT_DIR / "render3d.json"
    if not out.exists():
        print("[celula_reversao] render3d.json ausente — emit pulado (nada a preservar)")
        return
    d = json.loads(out.read_text(encoding="utf-8"))

    d["generated_by"] = "one_celula_reversao.py (forma=conteudo)"
    note = d.get("note", "")
    stamp = (" Corpo de engenharia PRESERVADO (sem geometria computavel); re-carimbado pelo "
             "runner com beta runtime e metricas COMPUTADAS desta run. [SIM][ENERGY][CONJ]")
    if "PRESERVADO" not in note:
        d["note"] = note + stamp

    # inject runtime β + computed metrics into constants (preserving existing entries)
    consts = d.get("constants", [])
    consts = [c for c in consts if c.get("symbol") not in
              ("beta_TGL_runtime", "cycle_correlation", "min_cycle_corr_multi", "retention_16bit")]
    consts.append({"symbol": "beta_TGL_runtime", "value": f"{beta:.12f}",
                   "note": "alpha*sqrt(e) injetado em runtime (nunca literal) - Constante de Miguel"})
    consts.append({"symbol": "cycle_correlation", "value": f"{metrics['cycle_correlation']:.6f}",
                   "note": "correlacao do ciclo REFLECT/LOCK/MANIFEST (COMPUTADA, fase nao energia)"})
    consts.append({"symbol": "min_cycle_corr_multi",
                   "value": f"{metrics['min_cycle_correlation_multi']:.6f}",
                   "note": "menor correlacao de ciclo entre 6 familias de tensor (COMPUTADA)"})
    consts.append({"symbol": "retention_16bit", "value": f"{metrics['retention_16bit']:.6f}",
                   "note": "retencao da FASE angular @16 bits (COMPUTADA, NAO energia fisica)"})
    d["constants"] = consts

    # VALIDATE coherence
    node_ids = {nd["id"] for nd in d.get("nodes", [])}
    mesh_ids = {m["id"] for m in d.get("meshes", [])}
    layer_ids = {ly["id"] for ly in d.get("layers", [])}
    valid_ids = node_ids | mesh_ids
    for e in d.get("edges", []):
        if e["from"] not in valid_ids or e["to"] not in valid_ids:
            raise ValueError(f"edge referencia id inexistente: {e}")
    for nd in d.get("nodes", []):
        if nd.get("layer") and nd["layer"] not in layer_ids:
            raise ValueError(f"no {nd['id']} usa layer inexistente: {nd['layer']}")
    for m in d.get("meshes", []):
        if m.get("layer") and m["layer"] not in layer_ids:
            raise ValueError(f"mesh {m['id']} usa layer inexistente: {m['layer']}")

    out.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[celula_reversao] render3d.json EMITIDO (forma=conteudo) — corpo preservado "
          f"({len(d.get('nodes', []))} nos, {len(d.get('meshes', []))} malhas), re-carimbado")


if __name__ == "__main__":
    sys.exit(main())
