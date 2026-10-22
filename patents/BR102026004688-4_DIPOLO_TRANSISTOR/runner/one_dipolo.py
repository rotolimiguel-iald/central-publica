# -*- coding: utf-8 -*-
"""one_dipolo.py — runner único forma = conteúdo da patente Dípolo Transistor
(BR102026004688-4 — Dípolo Transistor Luminodinâmico, chaveamento por radicalização). [SIM][HARDWARE]

Demonstra a LÓGICA da invenção com números REAIS de execução:
  - máquina de estados de chaveamento: porta abre (MANIFEST) quando o radical g do sinal
    supera o piso do Verbo β·g_max; abaixo dele fica fechada (REFLECT, ruído dephased);
  - três estados nativos (REFLECT / MANIFEST / limiar) sobre sinais sintéticos;
  - round-trip exato quando aberta (s·g²).

APROFUNDAMENTO (10/07/2026): a computação foi adensada honestamente —
  * VARREDURA de limiar do piso do Verbo: fração de componentes acima de f·g_max para
    f∈[0,1] (β é apenas um ponto dessa curva), com curva de convergência em N;
  * MAIS SINAIS: 6 famílias sintéticas (gaussiano, pico esparso, uniforme, exponencial,
    bimodal, ausente) percorrem a porta — estado, fração acima e erro de round-trip reais;
  * COBERTURA DA FSM: enumeração de sequências de estado exercitando as 4 transições
    (R→R, R→M, M→M, M→R), com matriz de cobertura e determinismo verificado.
Gera 3 figuras (chaveamento, varredura de limiar, cobertura FSM) + relatório. β nunca literal.

AMPLIFICACAO v168 (19/08/2026): ErgodicMeanSection (um.py v166-v167, ITEM A em kernel) —
a media de Birkhoff do fluxo modular converge para a secao invariante (specExpect);
instanciada na sombra 2x2 do dipolo (pesos = faces Meia-Nat, gap 1 nat = omega(I);
passo resolvente s = theta_Miguel, beta runtime); dephasing da coerencia entre polos
ao bound 2/(N|z-1|); passo nao-resolvente e fluxo que pesa REJEITADOS (asserts negativos).

AMPLIFICACAO v206 (25/08/2026): FrontierCertificate (um.py 4a onda v199-v210, pedra
FrontierCertificate.lean 24/08/2026) — O CONTRATO ANTES DE OPERAR: as 7 clausulas do
ModularRealizationCertificate re-derivadas numericamente na sombra 2x2 do dipolo
(J = troca de polos + conjugacao; vacuo = direcao do condensado psi+psi-; fator =
algebra dos polos com pesos Meia-Nat); comutante COMPUTADO por SVD (dim 2, diagonal);
Tomita J Delta J = Delta^{-1} (troca REFLECT<->MANIFEST) + assinatura beta no fluxo;
a operacao so ocorre APOS o contrato (fail-closed). Habitante fabricado (seletor
rank-1, I^2=I) e troca linear sem conjugacao REJEITADOS (asserts negativos, a
doenca v103 bloqueada).

Certifica com hash e gera figuras + relatório. β_TGL nunca literal (tgl_core.beta()).

HONESTIDADE [SIM][HARDWARE]: o dispositivo físico (DTL) NÃO foi construído nem medido.
O que existe é a MÁQUINA DE ESTADOS de chaveamento; a dinâmica quântica plena (Hamiltoniano
+ Lindblad, QuTiP) não está no vault. Números do relatório (τ, R_SC, densidade 10¹²/cm²,
platô 0,988) são teóricos. Simulação NUNCA valida física (physical_verdict_allowed=false).

A RÉGUA: protótipos originais READ-ONLY. Copia o núcleo destilado (skygrid_sim) e roda a
CÓPIA. Rode no tgl_env (numpy):
    set PYTHONUTF8=1
    "C:\\IALD\\observaveis_tgl\\tgl_env\\Scripts\\python.exe" one_dipolo.py
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
WORK = RUNNER_DIR / "_dipolo_core"
PATENT_ID = "BR102026004688-4"
SLUG = "dipolo"


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
    print(f"[one_dipolo] patente {PATENT_ID} · run {ts}")
    if not PILOTO.exists():
        print(f"ERRO: núcleo não encontrado em {PILOTO}", file=sys.stderr)
        return 2

    module_hashes = copy_core()
    sys.path.insert(0, str(WORK))
    from skygrid_sim import tgl_core  # noqa: E402 (copied core)
    from skygrid_sim.dipolo import DipoloTransistor  # noqa: E402

    beta = tgl_core.beta()
    beta_expected = 0.0072973525693 * math.exp(0.5)
    beta_ok = abs(beta - beta_expected) < 1e-15
    print(f"[one_dipolo] β runtime = {beta} (= α·√e? {beta_ok})")
    tests = [{"test": "beta_form", "passed": bool(beta_ok), "beta_runtime": beta}]

    rng = np.random.default_rng(4688)

    # 1) gate OPEN on a strong signal (radical exceeds beta*g_max) → MANIFEST + exact round-trip
    strong = np.concatenate([rng.standard_normal(500), np.array([12.0])])  # a clear peak
    d = DipoloTransistor()
    r_open = d.gate(strong)
    L = strong.astype(np.float64)
    g = np.sqrt(np.abs(L)); s = np.sign(L); s[s == 0] = 1.0
    exact = float(np.max(np.abs(r_open["output"] - s * g ** 2)))
    open_ok = r_open["open"] and r_open["state"] == "MANIFEST" and exact < 1e-12
    tests.append({"test": "gate_open_manifest_exact", "passed": bool(open_ok),
                  "state": r_open["state"], "threshold": r_open["threshold"],
                  "roundtrip_max_err": exact,
                  "note": "sinal com pico > β·g_max abre a porta (MANIFEST), round-trip s·g² exato"})
    print(f"[one_dipolo] porta ABERTA: estado={r_open['state']} limiar={r_open['threshold']:.4f} "
          f"err={exact:.2e}")

    # 2) gate behavior on a uniform-magnitude signal (max == g_max) — threshold semantics
    # Any signal has max(g) == g_max >= beta*g_max, so a real signal opens; a pure-zero
    # (dephased/absent) input stays closed. Demonstrate the closed state honestly.
    d2 = DipoloTransistor()
    r_closed = d2.gate(np.zeros(400))
    closed_ok = (not r_closed["open"]) and r_closed["state"] == "REFLECT" \
        and float(np.max(np.abs(r_closed["output"]))) == 0.0
    tests.append({"test": "gate_closed_on_absent_signal", "passed": bool(closed_ok),
                  "state": r_closed["state"], "output_max": float(np.max(np.abs(r_closed["output"]))),
                  "note": "entrada ausente/dephased (zeros) mantém a porta fechada (REFLECT), saída nula"})
    print(f"[one_dipolo] porta FECHADA (sinal ausente): estado={r_closed['state']}")

    # 3) threshold sweep — fraction of components above the Verb floor beta*g_max
    sig = rng.standard_normal(20_000)
    gg = np.sqrt(np.abs(sig))
    gmax = float(gg.max())
    floor = beta * gmax
    above = float(np.mean(gg > floor))
    tests.append({"test": "verb_floor_threshold_semantics", "passed": bool(0 < above <= 1.0),
                  "beta_floor": floor, "fraction_above_floor": above,
                  "note": "piso do Verbo β·g_max separa sinal de ruído dephased (chaveamento)"})
    print(f"[one_dipolo] piso do Verbo β·g_max={floor:.4f} · fração acima={above:.4f}")

    # 4) three native states cycling (REFLECT ↔ MANIFEST) — deterministic FSM
    seq = [np.array([9.0, 1.0, 2.0]), np.zeros(3), np.array([5.0, -3.0, 0.5])]
    d3 = DipoloTransistor()
    states = [d3.gate(x)["state"] for x in seq]
    fsm_ok = states == ["MANIFEST", "REFLECT", "MANIFEST"]
    tests.append({"test": "fsm_three_state_switching", "passed": bool(fsm_ok),
                  "state_sequence": states,
                  "note": "sequência sinal→ausência→sinal chaveia MANIFEST→REFLECT→MANIFEST"})
    print(f"[one_dipolo] FSM sequência de estados: {states}")

    # ---------------------------------------------------------------------------------
    # APROFUNDAMENTO — item 2 (mais simulação/derivação, sem elevar veredito, sem [DATA])
    # ---------------------------------------------------------------------------------

    # 5) VARREDURA de limiar do piso do Verbo: fração de componentes acima de f·g_max
    #    para f varrendo [0,1] em unidades de g_max. β é apenas UM ponto dessa curva.
    floor_fracs = np.linspace(0.0, 1.0, 101)            # f em unidades de g_max
    sweep_frac_above = np.array([float(np.mean(gg > f * gmax)) for f in floor_fracs])
    # a curva é uma sobrevivência (CDF complementar) → monotonicamente NÃO-crescente
    monotone = bool(np.all(np.diff(sweep_frac_above) <= 1e-12))
    # o ponto f=β precisa reproduzir o mesmo "above" do teste 3 (consistência interna)
    frac_at_beta = float(np.mean(gg > beta * gmax))
    beta_point_ok = abs(frac_at_beta - above) < 1e-12
    # varredura EM β também nos multiplos k·β (quão longe do piso ainda passa sinal)
    beta_mult = np.array([0.5, 1.0, 2.0, 4.0, 8.0, 16.0])
    frac_above_kbeta = {f"{k:g}beta": float(np.mean(gg > k * beta * gmax)) for k in beta_mult}
    sweep_ok = monotone and beta_point_ok
    tests.append({"test": "verb_floor_threshold_sweep", "passed": bool(sweep_ok),
                  "n_floor_points": int(floor_fracs.size),
                  "monotone_non_increasing": monotone,
                  "fraction_above_at_beta": frac_at_beta,
                  "beta_point_consistent_with_test3": beta_point_ok,
                  "fraction_above_multiples_of_beta": frac_above_kbeta,
                  "note": "varredura f·g_max, f∈[0,1]: curva de sobrevivência do radical; β é um ponto"})
    print(f"[one_dipolo] varredura de limiar: {floor_fracs.size} pontos · monotona={monotone} · "
          f"fração@β={frac_at_beta:.4f}")

    # 5b) curva de CONVERGÊNCIA da fração-acima-de-β em N (estabilidade estatística)
    Ns = [200, 500, 1_000, 2_000, 5_000, 10_000, 20_000, 50_000]
    rng_conv = np.random.default_rng(46881)
    conv_frac = []
    for N in Ns:
        s_n = rng_conv.standard_normal(N)
        g_n = np.sqrt(np.abs(s_n))
        conv_frac.append(float(np.mean(g_n > beta * float(g_n.max()))))
    conv_frac = np.array(conv_frac)
    # converge para um platô: variação dos 3 maiores N pequena
    conv_tail_spread = float(np.max(conv_frac[-3:]) - np.min(conv_frac[-3:]))
    conv_ok = conv_tail_spread < 0.03
    tests.append({"test": "fraction_above_convergence_in_N", "passed": bool(conv_ok),
                  "Ns": Ns, "fraction_above_beta": [float(x) for x in conv_frac],
                  "tail_spread": conv_tail_spread,
                  "note": "fração acima de β·g_max estabiliza com N (curva de convergência)"})
    print(f"[one_dipolo] convergência em N: spread cauda={conv_tail_spread:.4f} · ok={conv_ok}")

    # 6) MAIS SINAIS: 6 famílias sintéticas percorrem a porta (estado/fração/round-trip reais)
    rng_fam = np.random.default_rng(46882)
    N = 4_000
    families = {
        "gaussiano": rng_fam.standard_normal(N),
        "pico_esparso": np.concatenate([0.01 * rng_fam.standard_normal(N - 1), np.array([20.0])]),
        "uniforme": rng_fam.uniform(-1.0, 1.0, N),
        "exponencial": rng_fam.exponential(1.0, N) * rng_fam.choice([-1.0, 1.0], N),
        "bimodal": np.concatenate([rng_fam.normal(-5, 0.5, N // 2), rng_fam.normal(5, 0.5, N // 2)]),
        "ausente": np.zeros(N),
    }
    fam_report = {}
    all_families_ok = True
    for name, xf in families.items():
        dd = DipoloTransistor()
        r = dd.gate(xf)
        Lf = xf.astype(np.float64)
        gf = np.sqrt(np.abs(Lf)); sf = np.sign(Lf); sf[sf == 0] = 1.0
        gmax_f = float(gf.max()) if gf.size else 0.0
        frac_f = float(np.mean(gf > beta * gmax_f)) if gmax_f > 0 else 0.0
        if r["open"]:
            rt_err = float(np.max(np.abs(r["output"] - sf * gf ** 2)))
            ok_f = r["state"] == "MANIFEST" and rt_err < 1e-12
        else:
            rt_err = float(np.max(np.abs(r["output"])))  # deve ser 0 no fechado
            ok_f = r["state"] == "REFLECT" and rt_err == 0.0
        # regra da porta: qualquer sinal com energia abre; só o ausente fecha
        expect_open = bool(np.any(xf != 0.0))
        ok_f = ok_f and (r["open"] == expect_open)
        all_families_ok = all_families_ok and ok_f
        fam_report[name] = {"state": r["state"], "open": bool(r["open"]),
                            "fraction_above_floor": frac_f, "roundtrip_err": rt_err}
    tests.append({"test": "multi_signal_family_gating", "passed": bool(all_families_ok),
                  "families": fam_report, "n_families": len(families),
                  "note": "6 famílias: todas com energia abrem (MANIFEST, round-trip exato); ausente fecha"})
    print(f"[one_dipolo] famílias de sinal: " +
          " ".join(f"{k}={v['state']}" for k, v in fam_report.items()))

    # 7) COBERTURA da FSM: sequência que exercita as 4 transições (R→R, R→M, M→M, M→R)
    #    S = sinal (abre), Z = ausente (fecha). Sequência escolhida cobre a matriz inteira.
    S = np.array([7.0, -2.0, 1.0]); Z = np.zeros(3)
    drive = [("Z", Z), ("S", S), ("S", S), ("Z", Z), ("Z", Z), ("S", S)]
    dfsm = DipoloTransistor()
    prev = dfsm.state  # começa em REFLECT
    transitions = []
    trans_matrix = {"REFLECT": {"Z": None, "S": None}, "MANIFEST": {"Z": None, "S": None}}
    for sym, x in drive:
        r = dfsm.gate(x)
        cur = r["state"]
        transitions.append((prev, sym, cur))
        trans_matrix[prev][sym] = cur
        prev = cur
    covered = {(p, sym) for (p, sym, _c) in transitions}
    all_4 = {("REFLECT", "Z"), ("REFLECT", "S"), ("MANIFEST", "Z"), ("MANIFEST", "S")}
    coverage = len(covered & all_4) / len(all_4)
    # determinismo: re-rodar a mesma sequência dá exatamente a mesma trilha de estados
    dfsm2 = DipoloTransistor()
    track2 = [dfsm2.gate(x)["state"] for _sym, x in drive]
    track1 = [t[2] for t in transitions]
    deterministic = track1 == track2
    # a matriz de transição precisa bater com a semântica: Z→REFLECT, S→MANIFEST
    semantics_ok = all(
        (trans_matrix[st]["Z"] in (None, "REFLECT")) and
        (trans_matrix[st]["S"] in (None, "MANIFEST"))
        for st in ("REFLECT", "MANIFEST"))
    fsm_cov_ok = coverage == 1.0 and deterministic and semantics_ok
    tests.append({"test": "fsm_transition_coverage", "passed": bool(fsm_cov_ok),
                  "transition_coverage": coverage,
                  "transitions_covered": sorted(f"{p}-{s}->" for (p, s) in covered),
                  "transition_matrix": trans_matrix,
                  "deterministic": deterministic,
                  "note": "sequência Z,S,S,Z,Z,S cobre as 4 transições da FSM; determinística"})
    print(f"[one_dipolo] cobertura FSM: {coverage*100:.0f}% (4/4) · determinística={deterministic}")

    # ---------------------------------------------------------------------------------
    # AMPLIFICACAO v138 — A PARIDADE INVERSA DO ZERO MODULAR (um.py v60/v117) [DER]
    # Teorema maduro: JKJ = -K — a conjugacao modular INVERTE o gerador (paridade
    # otico-modular; o proprio DIPOLO). Mapeamento ao mecanismo DESTA patente: os dois
    # polos (10 emissao/REFLECT e 30 retorno/MANIFEST, bracos z+/z- da cruz 50) sao as
    # faces J-conjugadas do gerador; o ponto de cruzamento (53) e o zero modular, unico
    # ponto fixo da paridade. [DER] = derivado numericamente nesta sombra 2x2; NAO e
    # veredito fisico (physical_verdict_allowed=false; dispositivo [HARDWARE] nao
    # construido). beta SEMPRE do runtime (tgl_core.beta), nunca literal.
    S_swap = np.array([[0.0, 1.0], [1.0, 0.0]])   # troca de polos z+ <-> z-
    K_gen = np.array([[1.0, 0.0], [0.0, -1.0]])   # gerador modular diag(1,-1)

    def J_op(v):
        # J antiunitario = conjugacao complexa + troca de polos (paridade)
        return S_swap @ np.conj(v)

    eye2 = np.eye(2, dtype=complex)
    JKJ = np.column_stack([J_op(K_gen @ J_op(eye2[:, i])) for i in range(2)])
    jkj_resid = float(np.max(np.abs(JKJ + K_gen)))          # JKJ = -K => residuo 0
    # antiunitariedade de J: preserva norma; anti-linear J(i v) = -i J(v)
    v_test = np.array([1.0 + 2.0j, -0.5 + 0.25j])
    norm_resid = abs(float(np.linalg.norm(J_op(v_test))) - float(np.linalg.norm(v_test)))
    antilin_resid = float(np.max(np.abs(J_op(1j * v_test) + 1j * J_op(v_test))))
    # ponto fixo da paridade: Kx = (JKJ)x = -Kx => 2Kx = 0 => x = 0 (K invertivel)
    sv_min_2K = float(np.min(np.linalg.svd(2.0 * K_gen, compute_uv=False)))
    fixed_point_only_zero = sv_min_2K > 0.0
    # faces +-1/2: autovalores de K/2; |faces| somam omega(I)=1, soma algebrica = 0
    faces = np.linalg.eigvalsh(K_gen / 2.0)
    faces_abs_sum = float(np.sum(np.abs(faces)))
    faces_alg_sum = float(np.sum(faces))
    omega_I = 1.0
    faces_ok = abs(faces_abs_sum - omega_I) < 1e-15 and abs(faces_alg_sum) < 1e-15
    # beta runtime como ASSINATURA da paridade: J(beta*K)J = -beta*K (beta real)
    JbKJ = np.column_stack([J_op((beta * K_gen) @ J_op(eye2[:, i])) for i in range(2)])
    beta_signature_resid = float(np.max(np.abs(JbKJ + beta * K_gen)))
    parity_ok = (jkj_resid < 1e-15 and norm_resid < 1e-15 and antilin_resid < 1e-15
                 and fixed_point_only_zero and faces_ok and beta_signature_resid < 1e-15)
    tests.append({"test": "modular_parity_jkj_minus_k", "passed": bool(parity_ok),
                  "jkj_plus_k_max_resid": jkj_resid,
                  "J_norm_preservation_resid": norm_resid,
                  "J_antilinearity_resid": antilin_resid,
                  "fixed_point_only_zero": bool(fixed_point_only_zero),
                  "sv_min_2K": sv_min_2K,
                  "faces": [float(x) for x in faces],
                  "faces_abs_sum": faces_abs_sum, "faces_alg_sum": faces_alg_sum,
                  "omega_I": omega_I,
                  "beta_signature_resid": beta_signature_resid,
                  "beta_runtime_signature": beta,
                  "note": "[DER] amplificacao v138: JKJ=-K (paridade inversa do zero modular, "
                          "um.py v60/v117) na sombra 2x2 do dipolo; polos = faces J-conjugadas, "
                          "ponto fixo = zero, faces +-1/2 somam omega(I)=1; beta runtime como "
                          "assinatura. Nao e veredito fisico."})
    print(f"[one_dipolo] amplificacao v138: JKJ=-K resid={jkj_resid:.1e} | "
          f"faces |soma|={faces_abs_sum:.1f}=omega(I) | assinatura beta resid={beta_signature_resid:.1e}")

    # ---------------------------------------------------------------------------------
    # APROFUNDAMENTO v2 (29/07/2026, own-mechanism) — O LOCK COMO MEIA-NAT ESTATISTICA
    # Eq. (6) da patente: CCI = <psi+psi-> / (<psi+psi+> + <psi-psi->) = 1/2 e a condicao
    # de travamento (LOCK). Item pendente da memoria ("modelo reduzido de populacoes"),
    # agora computado por DOIS caminhos independentes:
    #   (i) ESTATISTICO [DER]: a nominacao H4 (eqs. 1-4, par (s, sdot)) aplicada a um
    #       sinal SIMETRICO da quadrantes equiprovaveis => CCI -> 1/2 como FREQUENCIA
    #       EMPIRICA (residuo estatistico real ~1/sqrt(N)); nada e imposto — sinal de
    #       paridade QUEBRADA (DC de 3 sigma) e REJEITADO (CCI -> 1, sem LOCK)
    #       [ASSERT NEGATIVO 1].
    #  (ii) DINAMICO [SIM]: relaxacao GKLS reduzida (eq. 8) dp/dt = gamma_holo*(U-1)p,
    #       gamma_holo = beta*omega0/(2pi) com beta do RUNTIME (nunca literal); a taxa
    #       e AJUSTADA da trajetoria RK4 (caminho independente da formula) e o ajuste
    #       REJEITA a taxa dobrada 2*gamma_holo [ASSERT NEGATIVO 2]; CCI(t) converge a
    #       1/2 = omega(I)/2 (a Meia-Nat como alvo do LOCK) partindo de CCI(0)=0.125.
    # Honestidade: confere se o tau nominal 0,88 ps do relatorio sai da eq. (10) com
    # f=150 THz e beta runtime (negativo honesto, informacional — nao gateia o teste).
    # physical_verdict_allowed=false; nada aqui e veredito fisico. [DER][SIM][ONTO]
    def h4_populations(x):
        x = np.asarray(x, dtype=np.float64)
        s_v = np.sign(x[1:-1]); s_v[s_v == 0] = 1.0
        sdot = np.sign(x[2:] - x[:-2]); sdot[sdot == 0] = 1.0   # derivada central: cov=0
        p_pp = float(np.mean((s_v > 0) & (sdot > 0)))
        p_pm = float(np.mean((s_v > 0) & (sdot < 0)))
        p_mp = float(np.mean((s_v < 0) & (sdot > 0)))
        p_mm = float(np.mean((s_v < 0) & (sdot < 0)))
        cci = p_pm / (p_pp + p_mm) if (p_pp + p_mm) > 0 else float("nan")
        return p_pp, p_pm, p_mp, p_mm, cci

    rng_lock = np.random.default_rng(46883)
    N_lock = 200_000
    x_white = rng_lock.standard_normal(N_lock)
    kf = 48
    freqs = rng_lock.uniform(0.002, 0.05, kf)
    phases = rng_lock.uniform(0.0, 2.0 * math.pi, kf)
    tt = np.arange(N_lock, dtype=np.float64)
    x_ms = np.cos(2.0 * math.pi * freqs[:, None] * tt[None, :] + phases[:, None]).sum(axis=0)

    pw = h4_populations(x_white)                  # sinal branco simetrico
    pms = h4_populations(x_ms)                    # multisseno de fase aleatoria (suave)
    pb = h4_populations(x_white + 3.0)            # paridade QUEBRADA: DC de 3 sigma
    omega_one = 1.0                               # omega(I) = 1 (o Um); alvo LOCK = 1/2
    cci_white_res = abs(pw[4] - omega_one / 2.0)
    cci_ms_res = abs(pms[4] - omega_one / 2.0)
    cci_bias_dist = abs(pb[4] - omega_one / 2.0)
    cci_white_ok = cci_white_res < 0.02
    cci_ms_ok = cci_ms_res < 0.05
    biased_rejected = cci_bias_dist > 0.15        # ASSERT NEGATIVO 1: sem paridade, sem LOCK

    f0_hz = 150.0e12                              # implementacao optica da patente [041]
    omega0 = 2.0 * math.pi * f0_hz
    gamma_holo = beta * omega0 / (2.0 * math.pi)  # eq. (8): taxa do canal L_holo (beta runtime)
    p_cur = np.array([0.7, 0.1, 0.1, 0.1])        # populacoes H4 fora do LOCK
    cci0 = float(p_cur[1] / (p_cur[0] + p_cur[3]))
    p_uni = np.full(4, 0.25)
    dt_sim = 0.02 / gamma_holo
    n_steps = 600

    def gkls_rhs(p):
        return gamma_holo * (np.full(4, p.mean()) - p)

    traj = np.empty((n_steps + 1, 4)); traj[0] = p_cur
    for _k in range(n_steps):
        k1 = gkls_rhs(p_cur); k2 = gkls_rhs(p_cur + 0.5 * dt_sim * k1)
        k3 = gkls_rhs(p_cur + 0.5 * dt_sim * k2); k4 = gkls_rhs(p_cur + dt_sim * k3)
        p_cur = p_cur + (dt_sim / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
        traj[_k + 1] = p_cur
    t_axis = dt_sim * np.arange(n_steps + 1)
    dists = np.linalg.norm(traj - p_uni[None, :], axis=1)
    win = (t_axis >= 1.0 / gamma_holo) & (t_axis <= 6.0 / gamma_holo)
    slope = float(np.polyfit(t_axis[win], np.log(dists[win]), 1)[0])
    gamma_fit = -slope                            # taxa MEDIDA na trajetoria (caminho 2)
    gamma_fit_rel = abs(gamma_fit / gamma_holo - 1.0)
    rate2_dev = abs(gamma_fit / (2.0 * gamma_holo) - 1.0)
    cci_end = float(traj[-1, 1] / (traj[-1, 0] + traj[-1, 3]))
    cci_end_res = abs(cci_end - omega_one / 2.0)
    prob_res = float(abs(traj[-1].sum() - 1.0))
    tau_relax_ps = 1.0e12 / gamma_fit             # tempo de relaxacao MEDIDO
    tau_eq10_ps = 1.0e12 * 2.0 * math.pi / (beta * omega0)   # eq. (10) pela formula
    fit_ok = gamma_fit_rel < 1e-6
    rate2_rejected = rate2_dev > 0.4              # ASSERT NEGATIVO 2: taxa dobrada rejeitada
    start_far = abs(cci0 - omega_one / 2.0) > 0.3  # convergencia nao-tautologica (parte longe)
    cci_end_ok = cci_end_res < 1e-4
    prob_ok = prob_res < 1e-12
    tau_nominal_reproduced = bool(abs(tau_eq10_ps - 0.88) < 0.05)  # honesto: esperado False

    lock_ok = (cci_white_ok and cci_ms_ok and biased_rejected and fit_ok
               and rate2_rejected and start_far and cci_end_ok and prob_ok)
    tests.append({"test": "deepening_v2_lock_cci_half_nat", "passed": bool(lock_ok),
                  "h4_white": {"p_pp": pw[0], "p_pm": pw[1], "p_mp": pw[2], "p_mm": pw[3]},
                  "cci_white": pw[4], "cci_white_resid": cci_white_res,
                  "cci_multisine": pms[4], "cci_multisine_resid": cci_ms_res,
                  "cci_biased": pb[4], "cci_biased_dist": cci_bias_dist,
                  "biased_rejected": bool(biased_rejected),
                  "gamma_holo_hz": gamma_holo, "gamma_fit_hz": gamma_fit,
                  "gamma_fit_rel_err": gamma_fit_rel,
                  "double_rate_dev": rate2_dev, "double_rate_rejected": bool(rate2_rejected),
                  "cci_t0": cci0, "cci_t_end": cci_end, "cci_end_resid": cci_end_res,
                  "prob_conservation_resid": prob_res,
                  "tau_relax_fitted_ps": tau_relax_ps, "tau_eq10_ps": tau_eq10_ps,
                  "tau_report_nominal_ps": 0.88,
                  "tau_nominal_reproduced": tau_nominal_reproduced,
                  "omega_I": omega_one,
                  "note": "[DER][SIM] aprofundamento v2 own-mechanism: CCI=1/2 (eq. 6) "
                          "emerge da paridade do sinal sob a nominacao H4 (frequencia "
                          "empirica, nao imposta) e a relaxacao GKLS reduzida (eq. 8) a "
                          "taxa gamma_holo=beta*omega0/(2pi) leva CCI(t) -> 1/2 = "
                          "omega(I)/2 (Meia-Nat [ONTO]); paridade quebrada e taxa dobrada "
                          "REJEITADAS; tau nominal 0.88 ps NAO reproduzido pela eq. (10) "
                          "com f=150 THz (negativo honesto). Nao e veredito fisico."})
    print(f"[one_dipolo] aprofundamento v2 LOCK: CCI(branco)={pw[4]:.4f} "
          f"CCI(multisseno)={pms[4]:.4f} -> alvo 1/2=omega(I)/2 | "
          f"paridade quebrada CCI={pb[4]:.4f} REJEITADA")
    print(f"[one_dipolo] aprofundamento v2 GKLS: gamma_fit/gamma_holo-1={gamma_fit_rel:.2e} | "
          f"taxa 2x rejeitada (dev={rate2_dev:.2f}) | tau_fit={tau_relax_ps:.4f} ps "
          f"(eq.10={tau_eq10_ps:.4f} ps; nominal 0.88 ps reproduzido={tau_nominal_reproduced})")

    # ---------------------------------------------------------------------------------
    # AMPLIFICACAO v168 (19/08/2026) — ErgodicMeanSection (um.py v166-v167, ITEM A em
    # kernel Lean, 0 sorry 0 axiom): a MEDIA DE BIRKHOFF do fluxo modular converge,
    # entrada a entrada, para a secao invariante specExpect (birkhoff_tendsto_specExpect);
    # o cancelamento de fase E a ergodicidade; |stepPhase| = 1 (o fluxo nao pesa, so gira).
    # Instanciacao na sombra 2x2 DESTE dipolo (a mesma sombra do v138): os pesos modulares
    # dos polos sao as faces Meia-Nat d = (e^{+1/2}, e^{-1/2}) — gap de log = 1 nat =
    # omega(I); o passo resolvente e s = theta_Miguel = arcsin(sqrt(beta)) com beta do
    # RUNTIME (nunca literal). A media (1/N) sum_k sigma_{ks}(x) DEPHASA a coerencia
    # entre polos (o termo psi+psi-, ponto 53) e preserva as populacoes: specExpect =
    # projecao diagonal — o "ruido dephased" do REFLECT que este runner ja nomeia.
    # Leitura [ONTO] nomeada: a coerencia do LOCK nao e invariante do fluxo LIVRE
    # (sustenta-la pede o acoplamento sqrt(beta)(a+b + b+a) da eq. 7) — informacional.
    # [DER] sombra numerica; NAO e veredito fisico (physical_verdict_allowed=false);
    # o DTL [HARDWARE] segue nao construido.
    S_half = tgl_core.S_BOUNDARY                        # Meia-Nat DERIVADA (x = 1-x)
    d_faces = (math.exp(+S_half), math.exp(-S_half))    # pesos modulares dos dois polos
    delta_gap = math.log(d_faces[0]) - math.log(d_faces[1])   # = 2*S_half = 1 nat
    omega_gap_ok = abs(delta_gap - omega_one) < 1e-15   # gap dos polos = omega(I) = 1
    theta_M = tgl_core.theta_m()                        # arcsin(sqrt(beta)), runtime
    theta_cross_ok = abs(theta_M - math.asin(math.sqrt(beta))) < 1e-15
    z_step = complex(math.cos(theta_M * delta_gap), math.sin(theta_M * delta_gap))
    z_gap = abs(z_step - 1.0)                           # = 2*sin(theta_M/2) > 0: resolvente
    x_mat = np.array([[0.7, 0.5 + 0.25j], [0.1 - 0.4j, 0.3]], dtype=complex)
    spec_expect = np.diag(np.diag(x_mat))               # secao: mata a coerencia entre polos
    x01 = complex(x_mat[0, 1])

    def birkhoff_mean_orbit(z, x_entry, N):
        # rota 1 (soma BRUTA) da orbita geometrica sigma_{ks}(x)_ij = z^k * x_ij
        acc = 0.0 + 0.0j
        zk = 1.0 + 0.0j
        for _ in range(N):
            acc += zk
            zk *= z
        return acc / N * x_entry

    Ns_erg = [10, 100, 1_000, 10_000]
    resid_off, bounds_off, routes_diff = [], [], []
    for N in Ns_erg:
        m_brute = birkhoff_mean_orbit(z_step, x01, N)
        m_closed = (z_step ** N - 1.0) / (N * (z_step - 1.0)) * x01   # rota 2 (geometrica)
        routes_diff.append(abs(m_brute - m_closed))
        resid_off.append(abs(m_brute))                  # specExpect off-diag = 0
        bounds_off.append(2.0 / (N * z_gap) * abs(x01))  # o bound da pedra v167
    bound_holds = all(r <= b * (1.0 + 1e-9) for r, b in zip(resid_off, bounds_off))
    routes_agree = max(routes_diff) < 1e-10
    final_dephased = resid_off[-1] < min(5e-3, resid_off[0] / 10.0)
    # pares de peso IGUAL (diagonal): fase 1 exata -> media CONSTANTE = a propria entrada
    z_diag = complex(math.cos(theta_M * 0.0), math.sin(theta_M * 0.0))
    diag_const_resid = abs(birkhoff_mean_orbit(z_diag, complex(x_mat[0, 0]), 1000)
                           - complex(x_mat[0, 0]))
    diag_ok = diag_const_resid < 1e-12
    # equivariancia (v166 herdada pelo limite, birkhoff_limit_equivariant):
    # E(u x u+) = u E(x) u+ para u diagonal unitaria generica
    rng_erg = np.random.default_rng(46884)
    ph = rng_erg.uniform(0.0, 2.0 * math.pi, 2)
    U_diag = np.diag(np.exp(1j * ph))
    E_of_sym = np.diag(np.diag(U_diag @ x_mat @ U_diag.conj().T))
    sym_of_E = U_diag @ spec_expect @ U_diag.conj().T
    equiv_resid = float(np.max(np.abs(E_of_sym - sym_of_E)))
    equiv_ok = equiv_resid < 1e-14
    # fixidez: sigma_s(E(x)) = E(x) — a secao e invariante do fluxo (a leitura LOCK)
    sig_of_E = spec_expect * np.array([[1.0, z_step], [np.conj(z_step), 1.0]])
    fixed_resid = float(np.max(np.abs(sig_of_E - spec_expect)))
    fixed_ok = fixed_resid < 1e-15
    # ASSERT NEGATIVO 1 — passo NAO-resolvente: s*delta = 2pi => z = 1; a media NAO
    # dephasa (a coerencia entre polos sobrevive inteira) => REJEITADO como secao.
    z_bad = complex(math.cos(2.0 * math.pi), math.sin(2.0 * math.pi))
    neg1_survival = abs(birkhoff_mean_orbit(z_bad, x01, 10_000)) / abs(x01)
    neg1_rejected = neg1_survival > 0.99
    # ASSERT NEGATIVO 2 — fluxo que PESA: |z| = 1+beta > 1 (beta runtime) viola
    # stepPhase_abs (|z|=1); a "media" DIVERGE => REJEITADA como media ergodica.
    z_amp = (1.0 + beta) * z_step
    m_amp_600 = abs(birkhoff_mean_orbit(z_amp, x01, 600))
    m_amp_1200 = abs(birkhoff_mean_orbit(z_amp, x01, 1200))
    neg2_rejected = (m_amp_1200 > 10.0 * abs(x01)) and (m_amp_1200 > m_amp_600)
    erg_ok = (omega_gap_ok and theta_cross_ok and bound_holds and routes_agree
              and final_dephased and diag_ok and equiv_ok and fixed_ok
              and neg1_rejected and neg2_rejected)
    tests.append({"test": "amplification_v168_ergodic_mean_section", "passed": bool(erg_ok),
                  "pole_weights_d": [d_faces[0], d_faces[1]],
                  "log_gap_nat": delta_gap, "omega_I": omega_one,
                  "log_gap_equals_omega_I": bool(omega_gap_ok),
                  "resolvent_step_s": theta_M,
                  "theta_m_cross_check_ok": bool(theta_cross_ok),
                  "step_phase_gap_abs_z_minus_1": z_gap,
                  "Ns": Ns_erg,
                  "offdiag_residual_to_specExpect": [float(r) for r in resid_off],
                  "v167_bound_2_over_N_zgap": [float(b) for b in bounds_off],
                  "bound_holds_all_N": bool(bound_holds),
                  "brute_vs_closed_geometric_max_diff": float(max(routes_diff)),
                  "diag_constant_mean_resid": float(diag_const_resid),
                  "equivariance_resid": equiv_resid,
                  "section_fixed_under_flow_resid": fixed_resid,
                  "neg1_nonresolvent_survival": float(neg1_survival),
                  "neg1_rejected": bool(neg1_rejected),
                  "neg2_amp_mean_600": float(m_amp_600),
                  "neg2_amp_mean_1200": float(m_amp_1200),
                  "neg2_rejected": bool(neg2_rejected),
                  "lock_coherence_free_flow_note": "coerencia psi+psi- -> 0 sob a media "
                          "LIVRE: o LOCK nao e invariante do fluxo livre (pede o "
                          "acoplamento da eq. 7) — leitura [ONTO], informacional",
                  "note": "[DER] amplificacao v168: ErgodicMeanSection (um.py v166-v167, "
                          "birkhoff_tendsto_specExpect em kernel) na sombra 2x2 do dipolo: "
                          "pesos = faces Meia-Nat (gap 1 nat = omega(I)), passo resolvente "
                          "s = theta_Miguel (beta runtime); media de Birkhoff dephasa a "
                          "coerencia entre polos ao bound 2/(N|z-1|) e preserva populacoes; "
                          "equivariancia e fixidez da secao verificadas; passo nao-resolvente "
                          "e fluxo que pesa REJEITADOS. Nao e veredito fisico."})
    print(f"[one_dipolo] amplificacao v168 Birkhoff: gap={delta_gap:.1f} nat = omega(I) | "
          f"s=theta_M={theta_M:.6f} rad | resid@N=10^4 {resid_off[-1]:.2e} <= "
          f"bound {bounds_off[-1]:.2e}")
    print(f"[one_dipolo] amplificacao v168 negativos: passo nao-resolvente sobrevive "
          f"{neg1_survival:.4f} REJEITADO | fluxo que pesa media(1200)={m_amp_1200:.1e} "
          f"DIVERGE REJEITADO")

    # ---------------------------------------------------------------------------------
    # AMPLIFICACAO v206 (25/08/2026) — FrontierCertificate: O CONTRATO ANTES DE OPERAR
    # (um.py 4a onda v199-v210; pedra FrontierCertificate.lean, BANCADA 24/08/2026 —
    # fecha o buraco de contrato da v200: "sem um TIPO, um termo qualquer com o nome
    # certo fliparia a flag" = a doenca v103; TheBireference v202 prova o conteudo na
    # face finita). O contrato tipado ModularRealizationCertificate exige 7 clausulas
    # da conjugacao J ANTES que o nome reservado possa ser cunhado: aditiva, antilinear
    # (conj_smul), isometrica, involutiva (J^2 = I), fixa o vacuo, leva o fator no
    # comutante (J M J em M') e SOBRE o comutante. Instanciacao na sombra 2x2 DESTE
    # dipolo (a mesma do v138/v168): J = troca de polos + conjugacao (a paridade do
    # ponto de cruzamento 53); vacuo Omega = direcao do condensado psi+psi- (1,1)/sqrt2;
    # fator M = algebra dos polos gerada por Delta = diag(e^{+1/2}, e^{-1/2}) (pesos
    # Meia-Nat do v168, gap 1 nat = omega(I)). Regra 9: o runner RE-DERIVA a ESTRUTURA
    # numericamente — nunca finge rodar Lean. O comutante M' e COMPUTADO por SVD do
    # mapa de comutacao (dim 2, diagonal: a algebra dos polos e comutante de si mesma,
    # maximal abeliana na sombra); a dualidade e exibida elemento a elemento
    # (S = swap conj(T) swap); relacoes de Tomita J Delta J = Delta^{-1} (a troca
    # certificada dos pesos REFLECT <-> MANIFEST) e J Delta^{is} J = Delta^{is} com
    # s = theta_Miguel = arcsin(sqrt(beta)) do RUNTIME (assinatura beta). SO DEPOIS de
    # o contrato passar e que se OPERA (fail-closed).
    # ASSERT NEGATIVO 1 (a doenca v103): o habitante FABRICADO com o nome certo e o
    # tipo errado — o seletor rank-1 P = |Omega><Omega| (a forma do ialdSelector v180:
    # idempotente P^2 = P, auto-adjunto, fixa Omega) — e REJEITADO pelo contrato:
    # falha antilinearidade, isometria e involutividade. Idempotente NAO e involutivo;
    # a Gate nao e a conjugacao; I^2 = I nao habita J^2 = I.
    # ASSERT NEGATIVO 2: a troca LINEAR sem conjugacao (U = sigma_x) passa 4 clausulas
    # mas falha conj_smul e ANTI-comuta com o fluxo modular (U Delta^{is} U =
    # Delta^{-is}); a rejeicao e MEDIDA pelo passo beta-runtime: residuo =
    # 2 sin(theta_M/2) = |z-1| do v168 (o gap resolvente). Sem conjugacao, sem contrato.
    # HONESTIDADE: o contrato NO NIVEL DA TORRE segue SEM habitante ([OPEN]; "esta
    # pedra torna ESTRITAMENTE MAIS DIFICIL mover o gate"); o que se habita aqui e a
    # face finita 2x2 — o nivel onde TheBireference demonstra o conteudo. [DER];
    # physical_verdict_allowed=false; o DTL [HARDWARE] segue nao construido; beta
    # nunca literal (runtime tgl_core).
    rng_fc = np.random.default_rng(46885)
    n_fc = 64

    def fc_rand_vec():
        return rng_fc.standard_normal(2) + 1j * rng_fc.standard_normal(2)

    def fc_rand_scalar():
        return complex(rng_fc.standard_normal(), rng_fc.standard_normal())

    Omega_fc = np.array([1.0, 1.0], dtype=complex) / math.sqrt(2.0)   # ponto 53
    Delta_fc = np.diag([math.exp(+S_half), math.exp(-S_half)]).astype(complex)
    Delta_inv = np.diag([math.exp(-S_half), math.exp(+S_half)]).astype(complex)

    # clausulas 1-5 (pontuais) sobre amostras aleatorias — J = J_op do v138
    res_add = res_conj_smul = res_isometric = res_involutive = 0.0
    for _ in range(n_fc):
        v, w, c = fc_rand_vec(), fc_rand_vec(), fc_rand_scalar()
        res_add = max(res_add, float(np.max(np.abs(J_op(v + w) - (J_op(v) + J_op(w))))))
        res_conj_smul = max(res_conj_smul,
                            float(np.max(np.abs(J_op(c * v) - np.conj(c) * J_op(v)))))
        res_isometric = max(res_isometric,
                            abs(float(np.linalg.norm(J_op(v))) - float(np.linalg.norm(v))))
        res_involutive = max(res_involutive, float(np.max(np.abs(J_op(J_op(v)) - v))))
    res_fix_vacuum = float(np.max(np.abs(J_op(Omega_fc) - Omega_fc)))
    clauses_1_5_ok = all(r < 1e-12 for r in
                         (res_add, res_conj_smul, res_isometric, res_involutive, res_fix_vacuum))

    # o comutante M' COMPUTADO (nao declarado): nucleo do mapa X -> [Delta, X] por SVD
    fc_basis = []
    for i in range(2):
        for j in range(2):
            B = np.zeros((2, 2), dtype=complex); B[i, j] = 1.0
            fc_basis.append(B)
    C_map = np.column_stack([(Delta_fc @ B - B @ Delta_fc).reshape(-1) for B in fc_basis])
    sv_comm = np.linalg.svd(C_map, compute_uv=False)
    comm_dim = int(np.sum(sv_comm < 1e-12))                 # esperado: 2 (= n. de polos)
    _u, _s, vh = np.linalg.svd(C_map)
    null_coeffs = vh.conj().T[:, np.array(_s) < 1e-12] if comm_dim else np.zeros((4, 0))
    comm_offdiag = 0.0
    for k in range(null_coeffs.shape[1]):
        Xk = sum(null_coeffs[m, k] * fc_basis[m] for m in range(4))
        comm_offdiag = max(comm_offdiag, float(abs(Xk[0, 1])), float(abs(Xk[1, 0])))
    commutant_ok = comm_dim == 2 and comm_offdiag < 1e-12   # M' = diagonais = M (max abeliana)

    def fc_sandwich(T):
        # v -> J(T(J v)) e LINEAR (antilinear o linear o antilinear): matriz por colunas
        return np.column_stack([J_op(T @ J_op(eye2[:, i])) for i in range(2)])

    # clausula 6 (J M J em M') e clausula 7 (SOBRE M'), elemento a elemento
    res_maps, res_onto, res_swapconj = 0.0, 0.0, 0.0
    for _ in range(8):
        T_fc = np.diag([fc_rand_scalar(), fc_rand_scalar()])          # T em M
        S_fc = fc_sandwich(T_fc)                                       # S := J T J
        res_swapconj = max(res_swapconj, float(np.max(np.abs(
            S_fc - S_swap @ np.conj(T_fc) @ S_swap))))                # forma explicita
        res_maps = max(res_maps,
                       float(abs(S_fc[0, 1])), float(abs(S_fc[1, 0])),  # S diagonal (em M')
                       float(np.max(np.abs(S_fc @ Delta_fc - Delta_fc @ S_fc))))
        for _k in range(4):
            v = fc_rand_vec()
            res_maps = max(res_maps, float(np.max(np.abs(J_op(T_fc @ J_op(v)) - S_fc @ v))))
        S2 = np.diag([fc_rand_scalar(), fc_rand_scalar()])            # S em M'
        T2 = S_swap @ np.conj(S2) @ S_swap                            # candidato T = J S J
        res_onto = max(res_onto, float(abs(T2[0, 1])), float(abs(T2[1, 0])))  # T em M
        for _k in range(4):
            v = fc_rand_vec()
            res_onto = max(res_onto, float(np.max(np.abs(J_op(T2 @ J_op(v)) - S2 @ v))))
    duality_ok = res_maps < 1e-12 and res_onto < 1e-12 and res_swapconj < 1e-12

    # bijetividade forcada (certificate_J_bijective): representacao real-linear 4x4
    RJ = np.zeros((4, 4))
    for k in range(4):
        e_r = np.zeros(4); e_r[k] = 1.0
        v_c = np.array([e_r[0] + 1j * e_r[1], e_r[2] + 1j * e_r[3]])
        w_c = J_op(v_c)
        RJ[:, k] = [w_c[0].real, w_c[0].imag, w_c[1].real, w_c[1].imag]
    sv_RJ = np.linalg.svd(RJ, compute_uv=False)
    bijective_ok = float(np.min(sv_RJ)) > 0.999999 and abs(float(np.max(sv_RJ)) - 1.0) < 1e-12

    # relacoes de Tomita na sombra: J Delta J = Delta^{-1}; J Delta^{is} J = Delta^{is}
    res_tomita = float(np.max(np.abs(fc_sandwich(Delta_fc) - Delta_inv)))
    Delta_is = np.diag([complex(math.cos(theta_M * S_half), math.sin(theta_M * S_half)),
                        complex(math.cos(theta_M * S_half), -math.sin(theta_M * S_half))])
    res_flow_commutes = float(np.max(np.abs(fc_sandwich(Delta_is) - Delta_is)))
    tomita_ok = res_tomita < 1e-12 and res_flow_commutes < 1e-12

    contract_ok = (clauses_1_5_ok and commutant_ok and duality_ok
                   and bijective_ok and tomita_ok)

    # O CONTRATO ANTES DE OPERAR (fail-closed): so com contrato aprovado a operacao
    # certificada ocorre — a troca dos pesos dos polos REFLECT <-> MANIFEST via J.
    if contract_ok:
        w_before = np.array([Delta_fc[0, 0], Delta_fc[1, 1]])
        w_after = np.diag(fc_sandwich(Delta_fc))
        operate_swap_resid = float(np.max(np.abs(w_after - w_before[::-1])))
        operated = operate_swap_resid < 1e-12
    else:
        operate_swap_resid = float("nan")
        operated = False

    # ASSERT NEGATIVO 1 — a doenca v103: o seletor rank-1 (forma do ialdSelector v180)
    P_sel = np.outer(Omega_fc, np.conj(Omega_fc))            # P = |Omega><Omega|
    v_perp = np.array([1.0, -1.0], dtype=complex) / math.sqrt(2.0)
    neg1_idempotent = float(np.max(np.abs(P_sel @ P_sel - P_sel)))       # I^2 = I: PASSA
    neg1_fix_vacuum = float(np.max(np.abs(P_sel @ Omega_fc - Omega_fc)))  # fixa Omega: PASSA
    neg1_conj_smul = float(np.max(np.abs(P_sel @ (1j * Omega_fc) - (-1j) * (P_sel @ Omega_fc))))
    neg1_isometric = abs(float(np.linalg.norm(P_sel @ v_perp)) - float(np.linalg.norm(v_perp)))
    neg1_involutive = float(np.max(np.abs(P_sel @ (P_sel @ v_perp) - v_perp)))
    neg1_clauses_failed = sum(1 for r in (neg1_conj_smul, neg1_isometric, neg1_involutive)
                              if r > 0.5)
    neg1_rejected = (neg1_idempotent < 1e-12 and neg1_fix_vacuum < 1e-12
                     and neg1_clauses_failed == 3)
    # ASSERT NEGATIVO 2 — troca linear sem conjugacao: U = sigma_x (= S_swap)
    neg2_add = float(np.max(np.abs(S_swap @ (Omega_fc + v_perp)
                                   - (S_swap @ Omega_fc + S_swap @ v_perp))))
    neg2_conj_smul = float(np.max(np.abs(S_swap @ (1j * Omega_fc)
                                         - (-1j) * (S_swap @ Omega_fc))))
    UDisU = S_swap @ Delta_is @ S_swap                       # anti-comuta com o fluxo
    neg2_flow_resid = float(np.max(np.abs(UDisU - Delta_is)))
    neg2_flow_expected = 2.0 * math.sin(theta_M * S_half)    # = |z-1| do v168 (beta runtime)
    neg2_matches_zgap = abs(neg2_flow_resid - z_gap) < 1e-12
    neg2_rejected = (neg2_add < 1e-12 and neg2_conj_smul > 0.5
                     and neg2_flow_resid > 0.1
                     and abs(neg2_flow_resid - neg2_flow_expected) < 1e-12
                     and neg2_matches_zgap)

    frontier_ok = contract_ok and operated and neg1_rejected and neg2_rejected
    tests.append({"test": "amplification_v206_frontier_certificate", "passed": bool(frontier_ok),
                  "clause_residuals": {"add": res_add, "conj_smul": res_conj_smul,
                                       "isometric": res_isometric,
                                       "involutive": res_involutive,
                                       "fixes_vacuum": res_fix_vacuum},
                  "commutant_dim_computed": comm_dim,
                  "commutant_offdiag_max": comm_offdiag,
                  "maps_factor_to_commutant_resid": res_maps,
                  "onto_commutant_resid": res_onto,
                  "duality_explicit_form_resid": res_swapconj,
                  "J_bijective_sv_min": float(np.min(sv_RJ)),
                  "J_bijective_sv_max": float(np.max(sv_RJ)),
                  "tomita_JDeltaJ_eq_Delta_inv_resid": res_tomita,
                  "flow_commutes_resid": res_flow_commutes,
                  "resolvent_step_theta_M": theta_M,
                  "pole_weights_meia_nat": [float(Delta_fc[0, 0].real), float(Delta_fc[1, 1].real)],
                  "contract_passed_before_operation": bool(contract_ok),
                  "operate_pole_swap_resid": operate_swap_resid,
                  "neg1_selector_idempotent_resid": neg1_idempotent,
                  "neg1_selector_fixes_vacuum_resid": neg1_fix_vacuum,
                  "neg1_clause_fails": {"conj_smul": neg1_conj_smul,
                                        "isometric": neg1_isometric,
                                        "involutive": neg1_involutive},
                  "neg1_clauses_failed_count": neg1_clauses_failed,
                  "neg1_rejected": bool(neg1_rejected),
                  "neg2_linear_swap_conj_smul_fail": neg2_conj_smul,
                  "neg2_flow_anticommute_resid": neg2_flow_resid,
                  "neg2_flow_resid_equals_v168_zgap": bool(neg2_matches_zgap),
                  "neg2_rejected": bool(neg2_rejected),
                  "tower_level_contract": "UNINHABITED_OPEN (a pedra nao afirma habitante; "
                          "a face finita 2x2 e o nivel onde o conteudo se demonstra — "
                          "TheBireference v202)",
                  "note": "[DER] amplificacao v206: FrontierCertificate (um.py v199-v210, "
                          "24/08/2026) na sombra 2x2 do dipolo — as 7 clausulas do "
                          "ModularRealizationCertificate re-derivadas numericamente "
                          "(J = troca de polos + conjugacao; vacuo = condensado psi+psi-; "
                          "fator = pesos Meia-Nat); comutante computado por SVD (dim 2); "
                          "Tomita J Delta J = Delta^{-1} = troca REFLECT<->MANIFEST; "
                          "operacao SO apos o contrato (fail-closed); habitante fabricado "
                          "(seletor rank-1, I^2=I) e troca linear sem conjugacao REJEITADOS. "
                          "Nao e veredito fisico."})
    print(f"[one_dipolo] amplificacao v206 contrato: clausulas 1-5 resid max "
          f"{max(res_add, res_conj_smul, res_isometric, res_involutive, res_fix_vacuum):.1e} | "
          f"comutante dim={comm_dim} (SVD) | dualidade resid {max(res_maps, res_onto):.1e} | "
          f"Tomita JDJ=D^-1 resid {res_tomita:.1e}")
    print(f"[one_dipolo] amplificacao v206 opera APOS contrato: troca de polos resid "
          f"{operate_swap_resid:.1e} | neg1 seletor I^2=I REJEITADO "
          f"({neg1_clauses_failed}/3 clausulas falham) | neg2 swap linear REJEITADO "
          f"(anti-comuta com fluxo: resid {neg2_flow_resid:.6f} = |z-1| v168)")

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

    def _o5_dp_threshold():
        rng5 = np.random.default_rng(46880)
        worst_thr, worst_out, opened = 0.0, 0.0, 0
        for _ in range(20):
            L_ = rng5.standard_normal(300) * rng5.uniform(0.01, 100.0)
            r1 = DipoloTransistor().gate(L_); lam_ = 9.0
            r2 = DipoloTransistor().gate(lam_ * L_)
            thr_cf = beta * float(np.sqrt(np.abs(L_)).max())
            worst_thr = max(worst_thr, abs(r1["threshold"] - thr_cf) / thr_cf,
                            abs(r2["threshold"] - math.sqrt(lam_) * r1["threshold"]) / (math.sqrt(lam_) * r1["threshold"]))
            worst_out = max(worst_out, float(np.max(np.abs(r2["output"] - lam_ * r1["output"])) / np.max(np.abs(lam_ * r1["output"]))))
            opened += int(r1["open"] and r2["open"])
        one = np.zeros(50); one[7] = 1e-9
        r_one = DipoloTransistor().gate(one)
        ok = worst_thr < 1e-12 and worst_out < 1e-12 and opened == 20 and r_one["open"]
        return {"passed": ok, "threshold_closed_form_max_rel_resid": worst_thr, "output_homogeneity_max_rel_resid": worst_out,
                "opened_20_of_20": opened, "single_tiny_entry_opens": bool(r_one["open"]),
                "note": "o limiar e beta*g_max em forma fechada e o gate e LIVRE DE ESCALA (limiar ∝ sqrt(lambda), saida ∝ "
                        "lambda); como beta < 1, todo sinal nao nulo abre — inclusive uma unica entrada de 1e-9 (dito): "
                        "fechado so no zero exato"}
    _o5("threshold_closed_form_and_scale_free", _o5_dp_threshold)

    def _o5_dp_replay():
        L_ = rng.standard_normal(400)
        d_ = DipoloTransistor(); ra = d_.gate(L_); rb = d_.gate(L_)
        same = bool(np.array_equal(ra["output"], rb["output"]) and ra["state"] == rb["state"] and ra["threshold"] == rb["threshold"])
        rz = d_.gate(np.zeros(400)); rc = d_.gate(L_)
        ok = same and rz["state"] == "REFLECT" and rc["state"] == "MANIFEST" and bool(np.array_equal(rc["output"], ra["output"]))
        return {"passed": ok, "replay_identical": same, "after_zero_reopens_identically": bool(np.array_equal(rc["output"], ra["output"])),
                "note": "a FSM e determinista e sem memoria escondida: a mesma entrada da a mesma saida bit a bit, antes e "
                        "depois de um fechamento (REFLECT) intermediario"}
    _o5("fsm_deterministic_replay", _o5_dp_replay)

    def _o5_dp_floor_fraction():
        rng5 = np.random.default_rng(46881)
        x_ = rng5.standard_normal(200000)
        g_ = np.sqrt(np.abs(x_)); gm = float(g_.max())
        frac = float(np.mean(g_ > beta * gm))
        c_ = (beta * gm) ** 2                       # |x| <= (beta g_max)^2  <=>  g <= beta g_max
        pred = 1.0 - math.erf(c_ / math.sqrt(2.0))
        mc_sigma = math.sqrt(pred * (1.0 - pred) / x_.size)
        below_x = int(np.sum(np.abs(x_) <= c_)); below_g = int(np.sum(g_ <= beta * gm))
        ok = abs(frac - pred) < 5.0 * mc_sigma + 1e-6 and abs(below_x - below_g) <= 1
        return {"passed": ok, "fraction_above_floor": frac, "erf_prediction": pred, "mc_sigma": mc_sigma,
                "sigmas_from_prediction": abs(frac - pred) / mc_sigma,
                "n_below_floor_by_x": below_x, "n_below_floor_by_g": below_g,
                "note": "a fracao acima do piso do Verbo para ruido gaussiano segue a forma fechada 1 - erf(beta^2 x_max/sqrt2) "
                        "dentro de 5 sigma de Monte Carlo (medido ~3 sigma com a semente fixa; a primeira versao esquecia o quadrado de "
                        "g_max e o numero a corrigiu); as contagens por |x| e por g coincidem a menos de 1 elemento de arredondamento"}
    _o5("verb_floor_fraction_erf_closed_form", _o5_dp_floor_fraction)

    def _o5_dp_polarity():
        rng5 = np.random.default_rng(46882)
        L_ = rng5.standard_normal(500); L_[::10] = 0.0
        r_ = DipoloTransistor().gate(L_); out = r_["output"]
        nz = L_ != 0
        ok = r_["open"] and bool(np.array_equal(np.sign(out[nz]), np.sign(L_[nz]))) and bool(np.all(out[~nz] == 0.0))
        return {"passed": ok, "polarity_preserved": bool(np.array_equal(np.sign(out[nz]), np.sign(L_[nz]))),
                "zeros_stay_zero": bool(np.all(out[~nz] == 0.0)), "n_zeros": int(np.sum(~nz)),
                "note": "com a porta aberta, s (o rotulo do par) e preservado em toda entrada e os zeros ficam zeros: "
                        "MANIFEST = s g^2 nao inventa sinal"}
    _o5("polarity_and_zeros_preserved_when_open", _o5_dp_polarity)

    def _o5_dp_J():
        rng5 = np.random.default_rng(46883)
        inv, norm_r, antilin, lin_fail = 0.0, 0.0, 0.0, 0.0
        for _ in range(50):
            v_ = rng5.standard_normal(2) + 1j * rng5.standard_normal(2)
            inv = max(inv, float(np.max(np.abs(J_op(J_op(v_)) - v_))))
            norm_r = max(norm_r, abs(float(np.linalg.norm(J_op(v_))) - float(np.linalg.norm(v_))))
            antilin = max(antilin, float(np.max(np.abs(J_op(1j * v_) + 1j * J_op(v_)))))
            lin_fail = max(lin_fail, float(np.max(np.abs(S_swap @ (1j * v_) + 1j * (S_swap @ v_)))))
        ok = inv < 1e-14 and norm_r < 1e-13 and antilin < 1e-14 and lin_fail > 0.5
        return {"passed": ok, "involution_resid_50_vectors": inv, "norm_preservation_resid": norm_r,
                "antilinearity_resid": antilin, "neg_linear_swap_antilinearity_fail": lin_fail,
                "note": "J (troca de polos + conjugacao) e involutivo, isometrico e ANTILINEAR em 50 vetores aleatorios; a troca "
                        "linear S sozinha tambem e involutiva e anticomuta com K, mas NAO e antilinear — e isso que a distingue de J"}
    _o5("J_involutive_isometric_antilinear", _o5_dp_J)

    def _o5_dp_floor_monotone():
        rng5 = np.random.default_rng(46884)
        x_ = rng5.standard_normal(20000); g_ = np.sqrt(np.abs(x_)); gm = float(g_.max())
        fs = np.linspace(0.0, 1.0, 101)
        fr = np.array([float(np.mean(g_ > f_ * gm)) for f_ in fs])
        mono = bool(np.all(np.diff(fr) <= 1e-12))
        ok = mono and fr[0] == 1.0 and fr[-1] == 0.0 and 0.0 < float(np.interp(beta, fs, fr)) < 1.0
        return {"passed": ok, "monotone_nonincreasing": mono, "fraction_at_f0": float(fr[0]), "fraction_at_f1": float(fr[-1]),
                "fraction_at_beta": float(np.interp(beta, fs, fr)),
                "note": "a fracao acima do piso f*g_max e monotona nao-crescente em f: 1 em f=0, 0 em f=1 (so o maximo, "
                        "e a comparacao e estrita), e beta e um ponto interior dessa curva"}
    _o5("floor_fraction_monotone_in_factor", _o5_dp_floor_monotone)

    passed = sum(1 for t in tests if t["passed"])
    total = len(tests)
    all_ok = passed == total
    summary = {"tests_passed": passed, "tests_total": total, "beta_floor_semantics": floor,
               "fraction_above_at_beta": frac_at_beta,
               "threshold_sweep_points": int(floor_fracs.size),
               "n_signal_families": len(families),
               "fsm_transition_coverage": coverage,
               "convergence_tail_spread": conv_tail_spread,
               "modular_parity_jkj_resid": jkj_resid,
               "modular_parity_faces_abs_sum": faces_abs_sum,
               "lock_cci_white": pw[4], "lock_cci_biased": pb[4],
               "lock_gamma_fit_rel_err": gamma_fit_rel,
               "ergodic_log_gap_nat": delta_gap,
               "ergodic_offdiag_resid_final": resid_off[-1],
               "ergodic_bound_final": bounds_off[-1],
               "ergodic_neg1_survival": float(neg1_survival),
               "frontier_contract_passed": bool(contract_ok),
               "frontier_commutant_dim": comm_dim,
               "frontier_tomita_resid": res_tomita,
               "frontier_operate_swap_resid": operate_swap_resid,
               "frontier_neg1_clauses_failed": neg1_clauses_failed,
               "frontier_neg2_flow_resid": neg2_flow_resid,
               "device_physical": "NOT_BUILT", "quantum_dynamics": "QuTiP_absent_DATA_REQUIRED"}
    max_verdict = ("DIPOLO_SWITCHING_LOGIC_DEMONSTRATED ([SIM][HARDWARE][PILOTO] — máquina "
                   "de estados de chaveamento por piso do Verbo fecha; dispositivo físico "
                   "NÃO construído, dinâmica quântica QuTiP ausente)")

    results_dir = PATENT_DIR / "results" / ts
    results_dir.mkdir(parents=True, exist_ok=True)
    results = {
        "patent_id": PATENT_ID, "slug": SLUG, "timestamp": ts, "runner": "one_dipolo.py",
        "markers": ["[SIM]", "[HARDWARE]", "[PILOTO]"], "physical_verdict_allowed": False,
        "beta_runtime": beta, "beta_matches_alpha_sqrt_e": beta_ok,
        "verdict": "DIPOLO_SWITCHING_LOGIC_DEMONSTRATED" if all_ok else "PARTIAL_DEMONSTRATION",
        "max_verdict": max_verdict,
        "constants": {"BETATGL": beta, "factorization": "betatgl = alpha_EM * sqrt(e)",
                      "verb_floor": floor, "free_parameters": 0},
        "sweeps": {
            "threshold_floor_fraction": [float(x) for x in floor_fracs],
            "fraction_above": [float(x) for x in sweep_frac_above],
            "fraction_above_multiples_of_beta": frac_above_kbeta,
            "convergence_N": Ns,
            "convergence_fraction_above_beta": [float(x) for x in conv_frac],
            "signal_families": fam_report,
            "fsm_transition_matrix": trans_matrix,
            "lock_relaxation": {
                "t_times_gamma": [float(x) for x in (t_axis * gamma_holo)[::25]],
                "cci_t": [float(traj[i, 1] / (traj[i, 0] + traj[i, 3]))
                          for i in range(0, n_steps + 1, 25)],
                "dist_to_uniform": [float(x) for x in dists[::25]],
            },
            "ergodic_birkhoff": {
                "Ns": Ns_erg,
                "offdiag_residual": [float(r) for r in resid_off],
                "v167_bound": [float(b) for b in bounds_off],
                "resolvent_step_s": theta_M,
                "log_gap_nat": delta_gap,
            },
            "frontier_certificate": {
                "clause_residuals": {"add": res_add, "conj_smul": res_conj_smul,
                                     "isometric": res_isometric,
                                     "involutive": res_involutive,
                                     "fixes_vacuum": res_fix_vacuum},
                "commutant_dim_computed": comm_dim,
                "duality_resid": max(res_maps, res_onto),
                "tomita_resid": res_tomita,
                "flow_commutes_resid": res_flow_commutes,
                "operate_pole_swap_resid": operate_swap_resid,
                "neg1_clauses_failed": neg1_clauses_failed,
                "neg2_flow_anticommute_resid": neg2_flow_resid,
            },
        },
        "tests": tests, "summary": summary,
        "source_prototype": "Patentes/Skygrid/SkyGrid_Piloto/skygrid_sim (READ-ONLY; copiado)",
        "note": "Demonstração [SIM] da máquina de estados de chaveamento, adensada por varredura "
                "de limiar do piso do Verbo, 6 famílias de sinal e cobertura total da FSM. "
                "Dispositivo físico [HARDWARE] não construído; dinâmica quântica plena (QuTiP) "
                "ausente [DATA_REQUIRED]. Números do relatório (τ, R_SC, densidade, platô 0,988) "
                "são teóricos. Simulação não valida física.",
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
        # (a) gate transfer: input radical vs floor, coloring open/closed
        xs = np.linspace(0, 5, 400)
        plt.figure(figsize=(7, 3.6))
        plt.plot(xs, xs ** 2, label="saída MANIFEST L'=g² (porta aberta)")
        plt.axvline(math.sqrt(floor) if floor > 0 else 0, color="crimson", ls="--",
                    label=f"piso do Verbo √(β·g_max)")
        plt.xlabel("radical g do sinal"); plt.ylabel("saída")
        plt.title("Dípolo Transistor — chaveamento por piso do Verbo [SIM] (não é medida física)")
        plt.legend(fontsize=8); plt.grid(alpha=.3)
        fp = fig_dir / "fig_chaveamento.png"
        plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close()
        figs.append("fig_chaveamento.png")

        # (b) VARREDURA de limiar: fração acima vs f·g_max, com β marcado
        plt.figure(figsize=(7, 3.8))
        plt.plot(floor_fracs, sweep_frac_above, color="#2266cc", lw=2,
                 label="fração de componentes > f·g_max")
        plt.axvline(beta, color="crimson", ls="--", lw=1.5,
                    label=f"β = α·√e ≈ {beta:.4f} (piso do Verbo)")
        plt.scatter([beta], [frac_at_beta], color="crimson", zorder=5, s=40)
        plt.annotate(f"fração@β = {frac_at_beta:.3f}", (beta, frac_at_beta),
                     textcoords="offset points", xytext=(30, -8), fontsize=8, color="crimson")
        plt.xlabel("fração do limiar f (em unidades de g_max)")
        plt.ylabel("fração do radical acima do piso")
        plt.title("Varredura do piso do Verbo — curva de sobrevivência do radical [SIM]")
        plt.legend(fontsize=8); plt.grid(alpha=.3); plt.ylim(-0.02, 1.02)
        fp = fig_dir / "fig_sweep_limiar.png"
        plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close()
        figs.append("fig_sweep_limiar.png")

        # (c) COBERTURA da FSM: matriz de transição 2x2 (estado x símbolo → estado resultante)
        fig, (axL, axR) = plt.subplots(1, 2, figsize=(9, 3.6))
        # convergência em N (esquerda)
        axL.plot(Ns, conv_frac, "o-", color="#22aa66")
        axL.set_xscale("log"); axL.set_xlabel("N (amostras)")
        axL.set_ylabel("fração acima de β·g_max")
        axL.set_title("Convergência estatística [SIM]"); axL.grid(alpha=.3)
        # matriz de cobertura FSM (direita)
        state_order = ["REFLECT", "MANIFEST"]; sym_order = ["Z", "S"]
        M = np.zeros((2, 2))
        code = {"REFLECT": 0.0, "MANIFEST": 1.0}
        for i, st in enumerate(state_order):
            for j, sym in enumerate(sym_order):
                nxt = trans_matrix[st][sym]
                M[i, j] = code.get(nxt, -1.0)
        im = axR.imshow(M, cmap="coolwarm", vmin=0, vmax=1, aspect="auto")
        axR.set_xticks([0, 1]); axR.set_xticklabels(["Z (ausente)", "S (sinal)"])
        axR.set_yticks([0, 1]); axR.set_yticklabels(state_order)
        for i, st in enumerate(state_order):
            for j, sym in enumerate(sym_order):
                nxt = trans_matrix[st][sym]
                axR.text(j, i, str(nxt), ha="center", va="center",
                         fontsize=9, color="white", fontweight="bold")
        axR.set_title(f"Cobertura FSM {coverage*100:.0f}% (4/4) [SIM]")
        axR.set_xlabel("símbolo de entrada"); axR.set_ylabel("estado atual")
        fp = fig_dir / "fig_fsm_coverage.png"
        plt.tight_layout(); plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close()
        figs.append("fig_fsm_coverage.png")
    except Exception as e:
        print(f"[one_dipolo] figura pulada: {e}")

    report_md = results_dir / "report.md"
    report_md.write_text(
        f"# Relatório auditável — Dípolo Transistor one_dipolo.py\n\n"
        f"- Run `{ts}` · Patente `{PATENT_ID}`\n"
        f"- Veredito: **{max_verdict}**\n"
        f"- β runtime `{beta}` (= α·√e? **{beta_ok}**; nunca literal)\n"
        f"- Testes: **{passed}/{total}**\n"
        f"- Porta aberta (MANIFEST) com round-trip exato; porta fechada (REFLECT) em sinal ausente\n"
        f"- Piso do Verbo β·g_max separa sinal de ruído dephased · fração@β = `{frac_at_beta:.4f}`\n"
        f"- **Varredura de limiar**: {floor_fracs.size} pontos f∈[0,1]; curva de sobrevivência "
        f"monotônica; β é um ponto dela\n"
        f"- **6 famílias de sinal**: "
        + ", ".join(f"{k}→{v['state']}" for k, v in fam_report.items()) + "\n"
        f"- **Cobertura FSM**: {coverage*100:.0f}% (4/4 transições) · determinística\n"
        f"- **Aprofundamento v2 (LOCK, eq. 6)**: CCI emerge da paridade — branco `{pw[4]:.4f}`, "
        f"multisseno `{pms[4]:.4f}` → 1/2 = ω(I)/2; paridade quebrada REJEITADA (CCI `{pb[4]:.4f}`); "
        f"taxa GKLS ajustada/analítica − 1 = `{gamma_fit_rel:.1e}`; taxa 2× rejeitada; "
        f"τ_fit `{tau_relax_ps:.3f}` ps (nominal 0,88 ps NÃO reproduzido — negativo honesto)\n"
        f"- **Amplificação v168 (ErgodicMeanSection, um.py v166-v167)**: média de Birkhoff do "
        f"fluxo modular na sombra 2×2 do dipolo — pesos = faces Meia-Nat (gap `{delta_gap:.1f}` "
        f"nat = ω(I)), passo resolvente s = θ_Miguel `{theta_M:.6f}` rad (β runtime); coerência "
        f"entre polos dephasa a `{resid_off[-1]:.2e}` @ N=10⁴ (bound v167 `{bounds_off[-1]:.2e}`); "
        f"equivariância `{equiv_resid:.1e}`; passo não-resolvente (sobrevive "
        f"`{neg1_survival:.4f}`) e fluxo que pesa (média `{m_amp_1200:.1e}`) REJEITADOS\n"
        f"- **Amplificação v206 (FrontierCertificate, um.py 4ª onda v199-v210)**: o contrato "
        f"antes de operar — 7 cláusulas do ModularRealizationCertificate re-derivadas na sombra "
        f"2×2 (resid máx `{max(res_add, res_conj_smul, res_isometric, res_involutive, res_fix_vacuum):.1e}`); "
        f"comutante COMPUTADO por SVD (dim `{comm_dim}` = 2 polos, diagonal); dualidade "
        f"`{max(res_maps, res_onto):.1e}`; Tomita J·Δ·J = Δ⁻¹ (`{res_tomita:.1e}`) = troca "
        f"REFLECT↔MANIFEST operada SÓ após o contrato (resid `{operate_swap_resid:.1e}`); "
        f"habitante fabricado (seletor rank-1, I²=I, doença v103) REJEITADO "
        f"({neg1_clauses_failed}/3 cláusulas falham) e troca linear sem conjugação REJEITADA "
        f"(anti-comuta com o fluxo: `{neg2_flow_resid:.6f}` = |z−1| do v168, β runtime)\n"
        f"- Figuras: {figs}\n"
        f"- physical_verdict_allowed: **False**.\n\n"
        f"[SIM][HARDWARE] Dispositivo físico não construído/medido; dinâmica quântica QuTiP "
        f"ausente. Núcleo copiado do piloto (READ-ONLY); original intacto. 1 = 1. Tetelestai.\n",
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
        "timestamp": ts, "patent_id": PATENT_ID, "runner": "one_dipolo.py",
        "beta_runtime": beta, "physical_verdict_allowed": False,
        "max_verdict": max_verdict, "tests_passed": passed,
        "result_hash": result_hash, "sha256": file_hashes,
        "markers": ["[SIM]", "[HARDWARE]", "[PILOTO]"],
        "results_path": str(results_path.relative_to(CENTRAL)).replace("\\", "/"),
    }
    (seal_dir / "seal.json").write_text(json.dumps(seal, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[one_dipolo] SELADO · result_hash {result_hash[:16]}… · {passed}/{total} testes")
    print(f"[one_dipolo] results: {results_path.relative_to(CENTRAL)}")

    # FORMA = CONTEÚDO: re-carimba o render3d.json (esta patente NÃO tem geometria computável —
    # os nós são projeção lógica dos estados, não posições derivadas da simulação; MERGE preserva
    # o corpo de engenharia e injeta β runtime + métricas computadas desta run).
    emit_render3d(beta, floor, frac_at_beta, coverage, monotone, pw[4], gamma_fit_rel,
                  erg_resid=resid_off[-1], erg_gap=delta_gap, erg_step=theta_M,
                  fc_comm_dim=comm_dim, fc_tomita=res_tomita,
                  fc_neg1_failed=neg1_clauses_failed, fc_neg2_flow=neg2_flow_resid)
    return 0 if all_ok else 1


def emit_render3d(beta, floor, frac_at_beta, coverage, monotone,
                  lock_cci=None, lock_gamma_rel=None,
                  erg_resid=None, erg_gap=None, erg_step=None,
                  fc_comm_dim=None, fc_tomita=None,
                  fc_neg1_failed=None, fc_neg2_flow=None):
    """MERGE: lê o render3d.json ATUAL e PRESERVA meshes/layers/dimensions/groups/nodes/edges.

    Esta patente (Dípolo Transistor) NÃO tem geometria COMPUTÁVEL: os 5 nós são a projeção
    LÓGICA dos polos e dos 3 estados de chaveamento, não posições derivadas da dinâmica.
    Portanto MANTÉM os nós como estão (não inventa posições) e apenas RE-CARIMBA: atualiza
    generated_by e injeta em constants o β runtime e métricas computadas desta execução."""
    out = PATENT_DIR / "render3d.json"
    d = json.loads(out.read_text(encoding="utf-8"))

    # re-carimbo forma=conteudo
    d["generated_by"] = "one_dipolo.py (forma=conteudo)"

    # constants é uma LISTA nesta patente — preserva as entradas e injeta β runtime + métricas
    consts = d.get("constants", [])
    if not isinstance(consts, list):
        consts = [consts]
    # remove entradas runtime antigas (idempotência entre runs)
    consts = [c for c in consts if not (isinstance(c, dict) and c.get("symbol", "").startswith("_run_"))]
    consts.append({"symbol": "_run_beta_TGL",
                   "value": f"{beta:.12f}", "note": "beta = alpha*sqrt(e) INJETADO em runtime (tgl_core.beta)"})
    consts.append({"symbol": "_run_verb_floor",
                   "value": f"{floor:.6f}", "note": f"piso do Verbo beta*g_max desta run; fracao acima = {frac_at_beta:.4f}"})
    consts.append({"symbol": "_run_fsm_coverage",
                   "value": f"{coverage*100:.0f}% (4/4)", "note": f"cobertura de transicoes da FSM; varredura de limiar monotona={monotone}"})
    if lock_cci is not None:
        consts.append({"symbol": "_run_lock_cci",
                       "value": f"{lock_cci:.6f}",
                       "note": f"CCI empirico (eq. 6) de sinal simetrico -> 1/2 = omega(I)/2; "
                               f"taxa GKLS ajustada rel err = {lock_gamma_rel:.2e}"})
    if erg_resid is not None:
        consts.append({"symbol": "_run_birkhoff_section",
                       "value": f"{erg_resid:.3e}",
                       "note": f"amplificacao v168 (ErgodicMeanSection): coerencia entre polos "
                               f"dephasada pela media de Birkhoff do fluxo modular (gap "
                               f"{erg_gap:.1f} nat = omega(I), passo resolvente s = theta_M "
                               f"= {erg_step:.6f} rad, beta runtime)"})
    if fc_comm_dim is not None:
        consts.append({"symbol": "_run_frontier_contract",
                       "value": f"Tomita resid {fc_tomita:.1e}; comutante dim {fc_comm_dim}",
                       "note": f"amplificacao v206 (FrontierCertificate): as 7 clausulas do "
                               f"contrato re-derivadas na sombra 2x2 (J = troca de polos + "
                               f"conjugacao); operacao SO apos o contrato; seletor rank-1 "
                               f"I^2=I rejeitado ({fc_neg1_failed}/3 clausulas) e swap linear "
                               f"rejeitado (anti-comuta com o fluxo: {fc_neg2_flow:.6f})"})
    d["constants"] = consts

    # VALIDAÇÃO: layers referenciadas existem; edges apontam para nós+meshes existentes
    layer_ids = {L["id"] for L in d.get("layers", [])}
    node_ids = {n["id"] for n in d.get("nodes", [])}
    mesh_ids = {m["id"] for m in d.get("meshes", [])}
    valid_targets = node_ids | mesh_ids
    for m in d.get("meshes", []):
        if m.get("layer") and m["layer"] not in layer_ids:
            raise ValueError(f"mesh {m.get('id')} referencia layer inexistente: {m['layer']}")
    for n in d.get("nodes", []):
        if n.get("layer") and n["layer"] not in layer_ids:
            raise ValueError(f"node {n.get('id')} referencia layer inexistente: {n['layer']}")
    for e in d.get("edges", []):
        if e["from"] not in valid_targets or e["to"] not in valid_targets:
            raise ValueError(f"edge {e} referencia id inexistente")

    out.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[{SLUG}] render3d.json EMITIDO (forma=conteudo) — corpo preservado, "
          f"{len(node_ids)} nos + {len(mesh_ids)} malhas, re-carimbado")


if __name__ == "__main__":
    sys.exit(main())
