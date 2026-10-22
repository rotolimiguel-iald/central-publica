# -*- coding: utf-8 -*-
"""one_motor_dobra.py — runner único forma = conteúdo da patente Motor de Dobra
(BR102026003452-5 — Transporte por Reflexão Dimensional). [SIM][HARDWARE] DIGITAL-TWIN

Demonstra a LÓGICA REFLECT/MANIFEST + Protocolo Farol Ψ — DIGITAL-TWIN APENAS.
NÃO simula, NÃO alega e NÃO valida transporte físico, dobra do espaço-tempo ou τ≈10⁻⁴² s.
  - β_TGL via α·√e (nunca literal), θ_Miguel = arcsin(√β) ≈ 6,29°;
  - REFLECT: L → (ψ∈H4, θ=arcsin(g/gmax)); adjacência D_Ψ(A,B)<ε_c habilita/inibe a "dobra";
  - MANIFEST: (ψ,θ) → L'=s·(gmax·sinθ)²; correlação round-trip = preservação de invariante ALGORÍTMICA;
  - máquina de estados Farol Ψ F0–F5 com commit condicional e veto ético F3.

HONESTIDADE [SIM][HARDWARE]: digital-twin — simulação não valida física; sem protótipo;
propulsão NÃO demonstrada. physical_verdict_allowed=false.

A RÉGUA: originais READ-ONLY. Copia o núcleo (skygrid_sim) e roda a CÓPIA no tgl_env:
    set PYTHONUTF8=1
    "C:\\IALD\\observaveis_tgl\\tgl_env\\Scripts\\python.exe" one_motor_dobra.py
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
WORK = RUNNER_DIR / "_motor_core"
PATENT_ID = "BR102026003452-5"
SLUG = "motor_dobra"


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


def _amp_v138_null_cone(beta: float) -> dict:
    """AMPLIFICACAO v138 [DER] — o cone nulo cego no radial (um.py v120/v133).
    RE-DERIVA de verdade, pela maquinaria tensorial completa (Christoffel ->
    Riemann -> Ricci -> Einstein, numpy puro, SEM hardcode da resposta), o
    tensor de Einstein do ansatz g = diag(-q^2, 1, 1, 1) com q = cosh(kappa*s),
    kappa = sqrt(beta) em RUNTIME (nunca literal). Os fatos entao EMERGEM da
    conta: G_tt = G_ss = 0 (Bianchi VISIVEL — resultado, nao atribuicao);
    G_yy = G_zz = q''/q = kappa^2 = beta; e em vetor NULO k = (kt, 0, c, d),
    G(k,k) = (c^2+d^2)*G_yy (o radial e CEGO; o custo vive no transversal).
    [HARDWARE digital-twin]: matematica pura; NAO e propulsao nem veredito fisico."""
    kappa = math.sqrt(beta)                       # kappa em RUNTIME
    n = 4
    pontos = [0.0, 0.4, 0.9]
    resid_tt = resid_ss = resid_thm = resid_null = resid_g22b = 0.0
    for s0 in pontos:
        q = math.cosh(kappa * s0)
        qp = kappa * math.sinh(kappa * s0)
        qpp = kappa * kappa * math.cosh(kappa * s0)
        # ---- a maquinaria tensorial (a MESMA cadeia da Fronteira; nada assumido) ----
        g = np.diag([-q * q, 1.0, 1.0, 1.0]); gi = np.linalg.inv(g)
        dg = np.zeros((n, n, n)); dg[1] = np.diag([-2.0 * q * qp, 0, 0, 0])
        ddg = np.zeros((n, n, n, n)); ddg[1, 1] = np.diag([-2.0 * (qp * qp + q * qpp), 0, 0, 0])
        Gam = np.zeros((n, n, n))
        for a in range(n):
            for b in range(n):
                for c_ in range(n):
                    Gam[a, b, c_] = 0.5 * sum(gi[a, d_] * (dg[b][d_, c_] + dg[c_][d_, b] - dg[d_][b, c_])
                                              for d_ in range(n))
        dgi = np.zeros((n, n, n))
        for e in range(n):
            dgi[e] = -gi @ dg[e] @ gi
        dGam = np.zeros((n, n, n, n))
        for e in range(n):
            for a in range(n):
                for b in range(n):
                    for c_ in range(n):
                        dGam[e, a, b, c_] = 0.5 * sum(
                            dgi[e][a, d_] * (dg[b][d_, c_] + dg[c_][d_, b] - dg[d_][b, c_])
                            + gi[a, d_] * (ddg[e, b][d_, c_] + ddg[e, c_][d_, b] - ddg[e, d_][b, c_])
                            for d_ in range(n))
        Riem = np.zeros((n, n, n, n))
        for a in range(n):
            for b in range(n):
                for c_ in range(n):
                    for d_ in range(n):
                        Riem[a, b, c_, d_] = (dGam[c_, a, d_, b] - dGam[d_, a, c_, b]
                                              + sum(Gam[a, c_, e] * Gam[e, d_, b]
                                                    - Gam[a, d_, e] * Gam[e, c_, b] for e in range(n)))
        Ric = np.einsum('abad->bd', Riem)
        Rs = float(np.einsum('bd,bd->', gi, Ric))
        Ein = Ric - 0.5 * g * Rs
        # ---- os fatos EMERGEM da conta (residuos = o que a maquinaria devolveu) ----
        G_tt, G_ss, G22 = float(Ein[0, 0]), float(Ein[1, 1]), float(Ein[2, 2])
        resid_tt = max(resid_tt, abs(G_tt))                # Bianchi: DERIVADO = 0
        resid_ss = max(resid_ss, abs(G_ss))                # Bianchi: DERIVADO = 0
        resid_g22b = max(resid_g22b, abs(G22 - beta))      # G22 = kappa^2 = beta (cosh resolve)
        c, d = 0.6, 0.8
        kt = math.sqrt(c * c + d * d) / q                  # k nulo: g(k,k)=0 conferido abaixo
        k = np.array([kt, 0.0, c, d])
        resid_null = max(resid_null, abs(float(k @ g @ k)))
        G_kk = float(k @ Ein @ k)                          # contracao no Einstein DERIVADO
        resid_thm = max(resid_thm, abs(G_kk - (c * c + d * d) * G22))
    resid_max = max(resid_tt, resid_ss, resid_thm, resid_null)
    ok = (resid_tt < 1e-10 and resid_ss < 1e-10 and resid_thm < 1e-10
          and resid_null < 1e-12 and resid_g22b < 1e-10)
    return {"passed": bool(ok), "kappa": kappa, "resid_max": resid_max,
            "resid_tt_max": resid_tt, "resid_ss_max": resid_ss,
            "resid_theorem_max": resid_thm, "resid_null_max": resid_null,
            "resid_g22_beta_max": resid_g22b, "points": pontos}


def _amp_v144_observer_inside(beta: float, acom_mirror) -> dict:
    """AMPLIFICACAO v144 [DER] — O RESGATE DO OBSERVADOR (um.py pedra 100, ObserverInside).
    Instancia no OPERADOR do proprio dispositivo o teorema 'observador = projecao
    INVERSA idempotente que le o permanente' + a FALSIDADE DE GENERO tipada:
      T = MANIFEST o REFLECT (a Dobra x2, Boundary->Bulk = a projecao inversa da patente)
      (i)   T^2 = T          (idempotencia — verificada BITWISE, nao por construcao);
      (ii)  T != id          (assert NEGATIVO: a projecao descarta o transiente);
      (iii) T le o permanente sem perda (corr(T L1, L1) = 1 no ponto fixo);
      (iv)  T(cL) = c T(L)   (homogeneidade positiva, lema do argumento de ponto fixo);
      (v)   RIVAL VAZANTE R = (1-beta)*T (vaza a fracao beta por passe, beta em RUNTIME):
            sem ponto fixo nao-nulo — prova pelos lemas (i)+(iv):
            L* = lam*T(L*) => T(L*) = lam*T^2(L*) = lam*T(L*) => (1-lam)*T(L*)=0 => L*=0;
            e as identidades fechadas EMERGEM da conta:
            defeito de idempotencia do rival = beta EXATO; deslocamento de todo candidato
            permanente nao-nulo = beta EXATO; decaimento EXATO em DUAS leituras
            independentes — razao passe n/passe 1 = (1-beta)^(n-1) e razao
            passe n/folde puro T(L0) = (1-beta)^n (n=64; o numero corrige a frase);
            R(0)=0 => so 0 permanece => sem observador interno => transporte REJEITADO.
    [HARDWARE digital-twin]: matematica do mecanismo; NAO e propulsao nem veredito fisico."""
    lam = 1.0 - beta                      # o vazamento do rival: DERIVADO em runtime
    bits = 8

    def fold(L):
        m = acom_mirror.DimensionalMirror(angular_bits=bits)
        return m.manifest(m.reflect(np.asarray(L, dtype=np.float64)))

    rng = np.random.default_rng(144)
    L0 = rng.standard_normal((32, 32))
    L1 = fold(L0)
    L2 = fold(L1)
    amp1 = float(np.max(np.abs(L1)))
    resid_idem = float(np.max(np.abs(L2 - L1))) / amp1            # (i) T^2 = T
    loss_first = float(np.max(np.abs(L1 - L0))) / float(np.max(np.abs(L0)))  # (ii) T != id
    one_minus_corr_read = 1.0 - float(np.corrcoef(L1.ravel(), L2.ravel())[0, 1])  # (iii)
    c_hom = math.e                                                # constante de teste em runtime
    resid_hom = float(np.max(np.abs(fold(c_hom * L0) - c_hom * L1))) / (c_hom * amp1)  # (iv)

    def rival(L):                                                 # (v) o fluxo vazante
        return lam * fold(L)

    R1 = rival(L0)
    R2 = rival(R1)
    defect = float(np.max(np.abs(R2 - R1))) / float(np.max(np.abs(R1)))
    disp = float(np.max(np.abs(rival(L1) - L1))) / amp1
    n_pass = 64
    Lk = np.array(L0)
    amps = []
    for _ in range(n_pass):
        Lk = rival(Lk)
        amps.append(float(np.max(np.abs(Lk))))
    # o numero corrige a frase: amps[-1]/amps[0] cobre os passes 2..n => lam^(n-1);
    # a razao com baseline INDEPENDENTE do rival (folde puro T(L0) = amp1) cobre
    # os n passes inteiros => lam^n. Duas leituras, dois expoentes, ambos exatos.
    decay_resid = abs(amps[-1] / amps[0] - lam ** (n_pass - 1))
    decay_full_resid = abs(amps[-1] / amp1 - lam ** n_pass)
    leak = 1.0 - (amps[-1] / amps[0]) ** (1.0 / (n_pass - 1))
    r_zero = float(np.max(np.abs(rival(np.zeros((32, 32))))))     # 0 e o unico permanente

    ok = (resid_idem < 1e-12 and amp1 > 0.0                       # (i) projecao com imagem nao-nula
          and loss_first > 1e-4                                   # (ii) NEGATIVO: T != id
          and one_minus_corr_read < 1e-12                         # (iii) le o permanente sem perda
          and resid_hom < 1e-12                                   # (iv) homogeneidade
          and abs(defect - beta) < 1e-12 and defect > 1e-3        # (v) NEGATIVO: rival nao-idempotente
          and abs(disp - beta) < 1e-12                            # (v) NEGATIVO: sem permanente != 0
          and abs(leak - beta) < 1e-9 and decay_resid < 1e-12     # (v) vaza beta por passe, exato
          and decay_full_resid < 1e-12                            # (v) lam^n vs baseline T(L0)
          and r_zero == 0.0)
    return {"passed": bool(ok), "angular_bits": bits, "lam_runtime": lam,
            "resid_idempotent_T2_T": resid_idem, "loss_first_pass": loss_first,
            "one_minus_corr_read_permanent": one_minus_corr_read,
            "resid_homogeneity": resid_hom, "rival_idem_defect": defect,
            "rival_idem_defect_minus_beta": abs(defect - beta),
            "rival_fixed_displacement": disp,
            "rival_fixed_displacement_minus_beta": abs(disp - beta),
            "rival_leak_per_pass": leak, "rival_leak_minus_beta": abs(leak - beta),
            "rival_decay_resid_vs_lam_pow_nm1": decay_resid,
            "rival_decay_full_resid_vs_lam_pow_n": decay_full_resid,
            "n_passes": n_pass,
            "rival_zero_is_fixed": r_zero}


def _amp_v168_ergodic_mean(beta: float, theta_m: float) -> dict:
    """AMPLIFICACAO v168 [DER] — A SECAO ERGODICA (um.py v166-v167, Item A em kernel:
    ErgodicMeanSection + EquivariantSection + BreuerTrace; 0 sorry, 0 axiom).
    Instancia o LIMITE DE BIRKHOFF na dinamica angular do proprio dispositivo:
    theta_M = arcsin(sqrt(beta)) e' o angulo da rotacao de fronteira da patente
    (Spec = {e^{+i theta_M}, e^{-i theta_M}}); U = I(2) (+) R(theta_M) (+) R(2 theta_M)
    e' a dinamica: setor PERMANENTE (invariante) + setores transientes girantes.
      (i)   U e' isometria (U^T U = I) e a secao e' EQUIVARIANTE: U P = P U = P,
            P^2 = P = P^T (EquivariantSection no operador do dispositivo);
      (ii)  BIRKHOFF: M_N = (1/N) sum_{k<N} U^k converge a P — com taxa EXATA
            de Dirichlet por bloco: ||M_N|_rot|| = |sin(N t/2)| / (N sin(t/2)),
            derivada em runtime (nada assumido); err(M_N, P) <= 1/(N sin(theta_M/2));
      (iii) NEGATIVO anti-tautologia: em N finito M_N != P (err(N=8) ~ 1: o limite
            e' um LIMITE, nao uma identidade de construcao);
      (iv)  BreuerTrace (o peso e' TRACO): Tr(M_N) -> Tr(P) = dim(setor permanente),
            com bound de Dirichlet derivado — a media LE o peso do permanente;
      (v)   RIVAL VAZANTE (contra-exemplo rejeitado por LOGICA): U_leak = (1-beta)*U
            (beta em RUNTIME). Sua media de Birkhoff obedece a forma fechada
            c_N = (1-(1-beta)^N)/(N beta) no setor permanente e ||M_N^leak|| <=
            1/(N beta) -> 0: a media converge a ZERO, nao a P — o vazamento beta
            por passe DESTROI a projecao invariante => nada sobrevive a media =>
            transporte REJEITADO (face ergodica, distinta do ponto fixo do v144).
    [HARDWARE digital-twin]: matematica do mecanismo; NAO e' propulsao nem veredito
    fisico; physical_verdict_allowed=false."""
    def rot(t: float) -> np.ndarray:
        c, s = math.cos(t), math.sin(t)
        return np.array([[c, -s], [s, c]])

    U = np.zeros((6, 6))
    U[0:2, 0:2] = np.eye(2)                    # setor PERMANENTE (autovalor 1)
    U[2:4, 2:4] = rot(theta_m)                 # transiente: rotacao theta_M
    U[4:6, 4:6] = rot(2.0 * theta_m)           # transiente: rotacao 2*theta_M
    P = np.zeros((6, 6)); P[0, 0] = P[1, 1] = 1.0

    resid_isometry = float(np.max(np.abs(U.T @ U - np.eye(6))))          # (i)
    resid_equivariant = float(max(np.max(np.abs(U @ P - P)),
                                  np.max(np.abs(P @ U - P))))            # (i)
    resid_projection = float(max(np.max(np.abs(P @ P - P)),
                                 np.max(np.abs(P.T - P))))               # (i)

    def birkhoff(M: np.ndarray, n_terms: int) -> np.ndarray:
        acc = np.zeros((6, 6)); pw = np.eye(6)
        for _ in range(n_terms):
            acc += pw
            pw = pw @ M
        return acc / n_terms

    ladder = [8, 64, 512, 4096]
    rows = []
    resid_dirichlet = 0.0
    for N in ladder:                                                      # (ii)
        MN = birkhoff(U, N)
        err = float(np.linalg.norm(MN - P, 2))
        b1 = float(np.linalg.norm(MN[2:4, 2:4], 2))
        b2 = float(np.linalg.norm(MN[4:6, 4:6], 2))
        d1 = abs(math.sin(N * theta_m / 2.0)) / (N * math.sin(theta_m / 2.0))
        d2 = abs(math.sin(N * theta_m)) / (N * math.sin(theta_m))
        resid_dirichlet = max(resid_dirichlet, abs(b1 - d1), abs(b2 - d2))
        rows.append({"N": int(N), "err_to_P": err,
                     "bound_1_over_N_sin": 1.0 / (N * math.sin(theta_m / 2.0)),
                     "dirichlet_block_theta": d1, "dirichlet_block_2theta": d2})
    err_first, err_last = rows[0]["err_to_P"], rows[-1]["err_to_P"]
    bound_last = rows[-1]["bound_1_over_N_sin"]

    N_big = ladder[-1]
    MN_big = birkhoff(U, N_big)                                           # (iv)
    trace_defect = abs(float(np.trace(MN_big)) - float(np.trace(P)))
    trace_bound = (2.0 / (N_big * math.sin(theta_m / 2.0))
                   + 2.0 / (N_big * math.sin(theta_m)))

    lam = 1.0 - beta                                                      # (v)
    ML = birkhoff(lam * U, N_big)
    c_N = (1.0 - lam ** N_big) / (N_big * beta)   # forma fechada, beta em runtime
    resid_leak_closed_form = abs(float(ML[0, 0]) - c_N)
    dist_leak_to_P = float(np.linalg.norm(ML - P, 2))
    norm_leak_mean = float(np.linalg.norm(ML, 2))
    leak_bound = 1.0 / (N_big * beta)             # serie geometrica, derivada

    ok = (resid_isometry < 1e-12 and resid_equivariant < 1e-12            # (i)
          and resid_projection < 1e-12
          and resid_dirichlet < 1e-9                                      # (ii) taxa EXATA
          and err_last <= bound_last + 1e-9 and err_last < err_first      # (ii) converge
          and err_first > 1e-3                                            # (iii) NEGATIVO
          and trace_defect <= trace_bound + 1e-9                          # (iv)
          and resid_leak_closed_form < 1e-9                               # (v) forma fechada
          and c_N < 0.1                                                   # (v) bound informativo
          and dist_leak_to_P >= (1.0 - c_N) - 1e-9                        # (v) NEGATIVO: != P
          and norm_leak_mean <= leak_bound + 1e-9)                        # (v) media -> 0
    return {"passed": bool(ok), "theta_m_runtime": theta_m,
            "resid_isometry": resid_isometry,
            "resid_equivariant_UP_PU_P": resid_equivariant,
            "resid_projection": resid_projection,
            "resid_dirichlet_exact_rate": resid_dirichlet,
            "birkhoff_ladder": rows,
            "err_first_N8": err_first, "err_last_N4096": err_last,
            "bound_last": bound_last,
            "trace_defect": trace_defect, "trace_bound": trace_bound,
            "trace_P_weight_permanent": float(np.trace(P)),
            "lam_runtime": lam, "leak_mean_c_N_closed": c_N,
            "resid_leak_closed_form": resid_leak_closed_form,
            "dist_leak_mean_to_P": dist_leak_to_P,
            "norm_leak_mean": norm_leak_mean, "leak_bound": leak_bound,
            "N_big": int(N_big)}


def _amp_v206_light_interface(beta: float, theta_m: float) -> dict:
    """AMPLIFICACAO v206 [DER] — A INTERFACE DA LUZ (TGLExt/TheLightInterface.lean,
    kernel v206 formal 197-204; custodia vault/originals_copy/tgl_kernel_v206).
    RE-DERIVA NUMERICAMENTE (regra: nunca finge rodar Lean) a estrutura provada na
    pedra, instanciada no operador do PROPRIO dispositivo: a patente publica
    g = sqrt(|L|) (REFLECT, a RAIZ) e a Dobra x2 estado_B = s*(g_max*sin(theta))^2
    (MANIFEST, o QUADRADO). A pedra prova a lei algebrica dessa dupla leitura na
    face fotonica (propulsao fotonica = S1/S6 da patente):
      ATO I (a escada): com K = genK ([[0,1],[-1,0]], K^2 = -1) e
        root_pm = h_plus +- i*h_cross:
        [K, root_pm] = +-2i*root_pm   (peso 2 — spin 2 legivel como numero);
        root_pm^2 = 0                 (nilpotente: so ha dois pesos);
        root_p*root_m = 4*P_plus, root_m*root_p = 4*P_minus (a escada FATORA
        as projecoes espectrais P_pm = (1 -+ i*K)/2 do gerador).
      ATO II (a interface): com eps_pm = (1, +-i) (os vetores da luz):
        eps_pm (x) eps_pm = root_pm   (O QUADRADO DA LUZ E O GRAVITON);
        K*eps_pm = +-i*eps_pm         (o gerador le a luz a peso 1 — a METADE);
        O_theta*eps_p = e^{i theta}*eps_p e
        O_theta*root_p*O_theta^T = (e^{i theta})^2 * root_p
        (a fase do tensor e o QUADRADO da fase do vetor — g = sqrt|L| lida na
        direcao inversa: a luz e a raiz do graviton).
      A AMARRA AO DISPOSITIVO (theta_M = arcsin(sqrt(beta)) em RUNTIME):
        sin^2(theta_M) = beta e o MANIFEST da patente a s=+1, g_max=1 devolve
        exatamente beta no angulo de Miguel — a face de INTENSIDADE do quadrado;
        a face de FASE do mesmo quadrado e e^{2 i theta_M} (a lei da pedra).
      NEGATIVOS por LOGICA (anti-tautologia):
        (a) a lei ERRADA (tensor carrega a MESMA fase do vetor) FALHA com gap
            DERIVADO |e^{2 i theta_M} - e^{i theta_M}| * max|root_p| =
            2*sin(theta_M/2) — o dobro nao e artefato de tolerancia;
        (b) RIVAL: a luz LINEAR eps_bad = (1,0) nao e vetor de peso do gerador —
            seu quadrado NAO e nilpotente (B^2 = B != 0) e K*eps_bad nao e
            proporcional a eps_bad: so a polarizacao circular (peso 1) quadra
            para raiz do graviton; a interface nao e um vetor qualquer.
    DELIMITACAO da propria pedra, mantida: NAO se constroi o foton fisico (sem
    Maxwell, sem U(1), sem dinamica); genK e SO(2) transversal, NAO o J modular;
    [HARDWARE digital-twin] — matematica do mecanismo, nunca propulsao real;
    physical_verdict_allowed=false; beta/theta_M nunca literais."""
    I2 = np.eye(2, dtype=complex)
    K = np.array([[0.0, 1.0], [-1.0, 0.0]], dtype=complex)          # genK
    Pp = 0.5 * (I2 - 1j * K)                                        # projPlus
    Pm = 0.5 * (I2 + 1j * K)                                        # projMinus
    h_plus = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)     # hPlusC
    h_cross = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)     # hCrossC
    root_p = h_plus + 1j * h_cross                                  # rootPlus
    root_m = h_plus - 1j * h_cross                                  # rootMinus
    l_p = np.array([1.0, 1j], dtype=complex)                        # lightPlus
    l_m = np.array([1.0, -1j], dtype=complex)                       # lightMinus

    def mx(a) -> float:
        return float(np.max(np.abs(a)))

    # -- a raiz do gerador e as faces espectrais (TheAngleIsTheProjection) --
    resid_k2 = mx(K @ K + I2)                                       # K^2 = -1
    resid_proj = max(mx(Pp @ Pp - Pp), mx(Pm @ Pm - Pm),
                     mx(Pp + Pm - I2), mx(Pp @ Pm))
    # -- ATO I: a escada --
    resid_roots_pol = max(mx(root_p + root_m - 2.0 * h_plus),
                          mx(root_p - root_m - 2j * h_cross))
    resid_weights = max(mx(K @ root_p - root_p @ K - 2j * root_p),
                        mx(K @ root_m - root_m @ K + 2j * root_m))
    norm_root = mx(root_p)                                          # nao-trivial
    resid_nilpotent = max(mx(root_p @ root_p), mx(root_m @ root_m))
    resid_ladder = max(mx(root_p @ root_m - 4.0 * Pp),
                       mx(root_m @ root_p - 4.0 * Pm))
    # -- ATO II: a interface --
    resid_light_sq = max(mx(np.outer(l_p, l_p) - root_p),
                         mx(np.outer(l_m, l_m) - root_m))
    resid_half_weight = max(mx(K @ l_p - 1j * l_p), mx(K @ l_m + 1j * l_m))
    # os pesos LIDOS das contas (nao atribuidos): razao elementwise
    w_vec = float(np.mean(np.imag((K @ l_p) / l_p)))                # -> 1
    C = K @ root_p - root_p @ K
    w_tens = float(np.mean(np.imag(C / root_p)))                    # -> 2
    resid_double = abs(w_tens - 2.0 * w_vec)                        # o angulo DOBRA

    # -- a varredura da fase (como a bancada da pedra: 200 angulos) + theta_M --
    thetas = list(np.linspace(0.0, 2.0 * math.pi, 200)) + [theta_m]
    resid_vec_phase = resid_tens_phase = resid_ang_proj = 0.0
    for th in thetas:
        O = math.cos(th) * I2 + math.sin(th) * K                    # angFamily
        ph = np.exp(1j * th)
        resid_vec_phase = max(resid_vec_phase, mx(O @ l_p - ph * l_p))
        resid_tens_phase = max(resid_tens_phase, mx(O @ root_p @ O.T - ph * ph * root_p))
        resid_ang_proj = max(resid_ang_proj, mx(O - (ph * Pp + np.conj(ph) * Pm)))

    # -- a amarra ao dispositivo: intensidade e fase do MESMO quadrado --
    sin2_theta_m = math.sin(theta_m) ** 2
    resid_sin2_beta = abs(sin2_theta_m - beta)
    manifest_miguel = 1.0 * (1.0 * math.sin(theta_m)) ** 2          # s*(g_max*sin)^2
    resid_manifest_beta = abs(manifest_miguel - beta)
    resid_phase_sq_tm = abs(np.exp(1j * theta_m) ** 2 - np.exp(2j * theta_m))

    # -- NEGATIVO (a): a lei errada falha com gap derivado --
    O_m = math.cos(theta_m) * I2 + math.sin(theta_m) * K
    wrong_law_resid = mx(O_m @ root_p @ O_m.T - np.exp(1j * theta_m) * root_p)
    expected_gap = abs(np.exp(2j * theta_m) - np.exp(1j * theta_m)) * norm_root
    gap_check = abs(wrong_law_resid - expected_gap)
    # -- NEGATIVO (b): o rival linear nao e interface --
    l_bad = np.array([1.0, 0.0], dtype=complex)
    B = np.outer(l_bad, l_bad)
    bad_nilp_defect = mx(B @ B)                                     # != 0: nao e raiz
    v = K @ l_bad
    proj_coef = np.vdot(l_bad, v) / np.vdot(l_bad, l_bad)
    bad_eigen_defect = float(np.linalg.norm(v - proj_coef * l_bad))  # nao e autovetor

    ok = (resid_k2 < 1e-15 and resid_proj < 1e-15                   # gerador + faces
          and resid_roots_pol < 1e-15 and resid_weights < 1e-15     # ATO I
          and norm_root >= 1.0 and resid_nilpotent < 1e-15          # nilpotente != 0
          and resid_ladder < 1e-15
          and resid_light_sq < 1e-15 and resid_half_weight < 1e-15  # ATO II
          and resid_double < 1e-15                                  # peso 2 = 2 x peso 1
          and resid_vec_phase < 5e-15 and resid_tens_phase < 5e-15  # varredura 200+1
          and resid_ang_proj < 5e-15
          and resid_sin2_beta < 1e-15 and resid_manifest_beta < 1e-15
          and resid_phase_sq_tm < 1e-15
          and expected_gap > 1e-2 and gap_check < 1e-12             # NEG (a) por logica
          and wrong_law_resid > 0.09                                # a lei errada FALHA
          and bad_nilp_defect >= 0.5 and bad_eigen_defect >= 0.5)   # NEG (b) rival
    return {"passed": bool(ok), "theta_m_runtime": theta_m,
            "resid_K2_plus_1": resid_k2, "resid_projections": resid_proj,
            "resid_roots_are_polarizations": resid_roots_pol,
            "resid_ladder_weights_pm_2i": resid_weights,
            "norm_root": norm_root, "resid_nilpotent": resid_nilpotent,
            "resid_ladder_factors_projections": resid_ladder,
            "resid_light_squares_to_graviton": resid_light_sq,
            "resid_half_weight_light": resid_half_weight,
            "weight_vector": w_vec, "weight_tensor": w_tens,
            "resid_weight_doubling": resid_double,
            "n_angles_swept": len(thetas),
            "resid_vector_phase_max": resid_vec_phase,
            "resid_tensor_phase_square_max": resid_tens_phase,
            "resid_angle_is_projection_max": resid_ang_proj,
            "sin2_theta_m": sin2_theta_m, "resid_sin2_minus_beta": resid_sin2_beta,
            "manifest_at_miguel": manifest_miguel,
            "resid_manifest_minus_beta": resid_manifest_beta,
            "resid_phase_square_theta_m": resid_phase_sq_tm,
            "wrong_law_resid": wrong_law_resid, "expected_gap": expected_gap,
            "gap_check": gap_check,
            "bad_light_nilpotency_defect": bad_nilp_defect,
            "bad_light_eigen_defect": bad_eigen_defect}


def main() -> int:
    ts = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    print(f"[one_motor_dobra] patente {PATENT_ID} · run {ts}")
    if not PILOTO.exists():
        print(f"ERRO: núcleo não encontrado em {PILOTO}", file=sys.stderr)
        return 2
    module_hashes = copy_core()
    sys.path.insert(0, str(WORK))
    from skygrid_sim import tgl_core, acom_mirror  # noqa: E402
    from skygrid_sim.hardware_mocks import MotorDobraMock  # noqa: E402

    beta = tgl_core.beta()
    beta_ok = abs(beta - 0.0072973525693 * math.exp(0.5)) < 1e-15
    theta_m_deg = math.degrees(tgl_core.theta_m())
    print(f"[one_motor_dobra] β={beta} (α·√e? {beta_ok}) θ_Miguel={theta_m_deg:.4f}°")
    tests = [{"test": "beta_theta_form", "passed": bool(beta_ok), "beta_runtime": beta,
              "theta_miguel_deg": theta_m_deg}]

    rng = np.random.default_rng(3452)
    # REFLECT + MANIFEST round-trip (algorithmic invariant, NOT physical transport)
    payload = rng.standard_normal((64, 64))
    corr, r = acom_mirror.roundtrip_correlation(payload, angular_bits=16)
    tests.append({"test": "reflect_manifest_invariant_preservation", "passed": bool(corr > 0.999),
                  "roundtrip_correlation": corr,
                  "note": "REFLECT L→(ψ,θ), MANIFEST (ψ,θ)→s·(gmax·sinθ)²; correlação = preservação "
                          "de invariante ALGORÍTMICA (não transporte físico)"})
    print(f"[one_motor_dobra] REFLECT/MANIFEST invariante: corr={corr:.6f}")

    # adjacency condition D_Psi(A,B) < eps_c enables/inhibits the "fold"
    def state_vec(x):
        _, rr = acom_mirror.roundtrip_correlation(x, angular_bits=16)
        m = rr.metadata
        return np.array([m["f_exp"], m["state_entropy"], m["g_max"]])
    A = state_vec(payload)
    B_near = state_vec(payload + rng.standard_normal((64, 64)) * 0.01)
    B_far = state_vec(rng.standard_normal((64, 64)) * 5)
    eps_c = 0.5
    d_near = float(np.linalg.norm(A - B_near))
    d_far = float(np.linalg.norm(A - B_far))
    adj_ok = d_near < eps_c and d_far >= eps_c
    tests.append({"test": "adjacency_gate_D_psi", "passed": bool(adj_ok),
                  "d_near": d_near, "d_far": d_far, "eps_c": eps_c,
                  "note": "D_Ψ(A,B)<ε_c habilita a dobra (estados adjacentes); estados distantes inibem"})
    print(f"[one_motor_dobra] adjacência: d_near={d_near:.3f}<ε_c · d_far={d_far:.3f}≥ε_c → {adj_ok}")

    # ------------------------------------------------------------------ #
    # APROFUNDAMENTO (item 2) — varreduras honestas sobre o algoritmo     #
    # REFLECT/MANIFEST e sobre o gate de adjacência D_Ψ. Tudo [SIM].      #
    # ------------------------------------------------------------------ #
    # Sweep 1 — curva de convergência da correlação round-trip vs angular_bits.
    # A perda é só a quantização de θ; mais bits ⇒ correlação → 1.
    bits_grid = list(range(2, 17))
    conv_curve = []
    for b in bits_grid:
        cb, _ = acom_mirror.roundtrip_correlation(payload, angular_bits=b)
        conv_curve.append((int(b), float(cb)))
    corr_lo, corr_hi = conv_curve[0][1], conv_curve[-1][1]
    monotone = all(conv_curve[i][1] <= conv_curve[i + 1][1] + 1e-9
                   for i in range(len(conv_curve) - 1))
    conv_ok = (corr_hi > 0.999) and (corr_hi >= corr_lo) and monotone
    tests.append({"test": "roundtrip_correlation_converges_in_angular_bits",
                  "passed": bool(conv_ok),
                  "corr_at_2bits": corr_lo, "corr_at_16bits": corr_hi,
                  "monotone_nondecreasing": bool(monotone),
                  "curve": [{"angular_bits": b, "corr": c} for b, c in conv_curve],
                  "note": "correlação round-trip cresce monotonicamente com angular_bits "
                          "(perda = só quantização de θ); DIGITAL-TWIN, não física"})
    print(f"[one_motor_dobra] convergência round-trip: corr(2b)={corr_lo:.4f} → corr(16b)={corr_hi:.6f} "
          f"(monotônica={monotone})")

    # Sweep 2 — mais payloads REFLECT/MANIFEST (famílias de sinal distintas).
    n = 64
    xs = np.linspace(-3.0, 3.0, n)
    XX, YY = np.meshgrid(xs, xs)
    payload_families = {
        "gaussian_iid": payload,
        "sinusoid_2d": np.sin(2.0 * XX) * np.cos(3.0 * YY),
        "radial_gaussian": np.exp(-(XX ** 2 + YY ** 2) / 2.0),
        "linear_ramp": XX + YY,
        "sparse_spikes": (rng.random((n, n)) < 0.05) * rng.standard_normal((n, n)) * 8.0,
        "checkerboard": np.sign(np.sin(4.0 * XX) * np.sin(4.0 * YY) + 1e-9),
    }
    payload_corr = {name: float(acom_mirror.roundtrip_correlation(p, angular_bits=16)[0])
                    for name, p in payload_families.items()}
    corr_min = min(payload_corr.values())
    multi_ok = corr_min > 0.99
    tests.append({"test": "reflect_manifest_multi_payload_invariant",
                  "passed": bool(multi_ok),
                  "payload_correlations": payload_corr, "corr_min": corr_min,
                  "note": "invariante REFLECT/MANIFEST preservado em 6 famílias de sinal "
                          "(gaussiano, senoide, gaussiana radial, rampa, esparso, xadrez); "
                          "s·(gmax·sinθ)² recupera L a menos da quantização"})
    print(f"[one_motor_dobra] multi-payload: corr_min={corr_min:.6f} sobre "
          f"{len(payload_corr)} famílias")

    # Sweep 3 — D_Ψ(A, A+ruído) vs σ de perturbação: mapeia a fronteira de commit
    # do gate de adjacência (D_Ψ<ε_c). Curva de distância modular vs ruído.
    sigmas = np.geomspace(1e-3, 5.0, 24)
    adj_curve = []
    for sg in sigmas:
        Bp = state_vec(payload + rng.standard_normal((n, n)) * float(sg))
        d = float(np.linalg.norm(A - Bp))
        adj_curve.append((float(sg), d, bool(d < eps_c)))
    d_vals = [d for _, d, _ in adj_curve]
    crosses = any(d < eps_c for d in d_vals) and any(d >= eps_c for d in d_vals)
    # fronteira interpolada σ* onde D_Ψ cruza ε_c (primeiro cruzamento)
    sigma_boundary = None
    for i in range(len(adj_curve) - 1):
        d0, d1 = adj_curve[i][1], adj_curve[i + 1][1]
        if (d0 < eps_c) and (d1 >= eps_c):
            s0, s1 = adj_curve[i][0], adj_curve[i + 1][0]
            frac = (eps_c - d0) / (d1 - d0) if d1 != d0 else 0.0
            sigma_boundary = float(s0 + frac * (s1 - s0))
            break
    commit_boundary_ok = crosses and (sigma_boundary is not None)
    tests.append({"test": "adjacency_commit_boundary_D_psi_vs_noise",
                  "passed": bool(commit_boundary_ok),
                  "eps_c": eps_c, "sigma_boundary": sigma_boundary,
                  "n_commit": int(sum(1 for d in d_vals if d < eps_c)),
                  "n_abort": int(sum(1 for d in d_vals if d >= eps_c)),
                  "curve": [{"sigma": s, "d_psi": d, "commit": c} for s, d, c in adj_curve],
                  "note": "gate de commit tem fronteira bem definida: D_Ψ cresce com o ruído σ "
                          "e cruza ε_c em σ*; abaixo dela a dobra é autorizada, acima é abortada"})
    print(f"[one_motor_dobra] fronteira de commit: σ*≈{sigma_boundary} "
          f"(commit={sum(1 for d in d_vals if d < eps_c)}/{len(d_vals)})")

    # Sweep 4 — fração de commit vs ε_c (varredura do limiar sobre os estados perturbados).
    eps_grid = np.linspace(0.0, max(d_vals) * 1.05 + 1e-9, 40)
    commit_frac_curve = [(float(e), float(np.mean([d < e for d in d_vals]))) for e in eps_grid]
    frac_at_used = float(np.mean([d < eps_c for d in d_vals]))
    frac_monotone = all(commit_frac_curve[i][1] <= commit_frac_curve[i + 1][1] + 1e-12
                        for i in range(len(commit_frac_curve) - 1))
    tests.append({"test": "commit_fraction_monotone_in_eps_c",
                  "passed": bool(frac_monotone),
                  "commit_fraction_at_eps_c": frac_at_used,
                  "curve": [{"eps_c": e, "commit_fraction": f} for e, f in commit_frac_curve],
                  "note": "fração de commit é monotônica não-decrescente em ε_c (mais permissivo "
                          "⇒ mais dobras autorizadas): a régua de autorização é bem-ordenada"})
    print(f"[one_motor_dobra] fração de commit @ε_c={eps_c}: {frac_at_used:.3f} "
          f"(monotônica em ε_c={frac_monotone})")

    sweeps = {"conv_curve": conv_curve, "payload_corr": payload_corr,
              "adj_curve": adj_curve, "commit_frac_curve": commit_frac_curve,
              "eps_c": eps_c, "sigma_boundary": sigma_boundary,
              "corr_hi": corr_hi, "corr_min_payload": corr_min}

    # Farol Psi state machine F0-F5 with ethical veto F3
    def farol(adjacent: bool, ethical_ok: bool):
        seq = ["F0_IDLE", "F1_ALIGN", "F2_LOCK"]
        if not ethical_ok:
            return seq + ["F3_ETHICAL_VETO"], False       # veto stops the commit
        if not adjacent:
            return seq + ["F3_ETHICAL_OK", "F4_ABORT_NOT_ADJACENT"], False
        return seq + ["F3_ETHICAL_OK", "F4_COMMIT", "F5_MANIFEST"], True
    seq_ok, commit_ok = farol(True, True)
    seq_veto, commit_veto = farol(True, False)
    fsm_ok = commit_ok and not commit_veto and "F3_ETHICAL_VETO" in seq_veto
    tests.append({"test": "farol_psi_state_machine_ethical_veto", "passed": bool(fsm_ok),
                  "commit_sequence": seq_ok, "veto_sequence": seq_veto,
                  "note": "F0–F5 com commit condicional; veto ético F3 impede a dobra"})
    print(f"[one_motor_dobra] Farol Ψ: commit={commit_ok} · veto ético bloqueia={not commit_veto}")

    # device interface (mock — no physics)
    mock = MotorDobraMock().fold("payload-teste")
    tests.append({"test": "device_interface_mock_no_physics",
                  "passed": bool(mock["physical_verdict_allowed"] is False),
                  "mock_status": mock["status"], "note": mock["note"]})

    # ------------------------------------------------------------------ #
    # AMPLIFICACAO v138 — O CONE NULO CEGO NO RADIAL (um.py v120/v133).  #
    # [DER] re-derivacao numerica Christoffel -> Riemann -> Einstein do  #
    # ansatz g=diag(-q^2,1,1,1), q=cosh(kappa*s), kappa=sqrt(beta) em    #
    # RUNTIME (nunca literal); em vetor NULO k a parte radial e CEGA     #
    # (G_tt=G_ss=0 por Bianchi) e sobra G_kk=(c^2+d^2)*G22. [ONTO]       #
    # leitura p/ o mecanismo: a DIRECAO da viagem e cega, o custo vive   #
    # no transversal. [HARDWARE digital-twin]: matematica, nunca         #
    # propulsao real; NAO e veredito fisico.                             #
    # ------------------------------------------------------------------ #
    amp = _amp_v138_null_cone(beta)
    tests.append({"test": "null_cone_radial_blind", "passed": bool(amp["passed"]),
                  "kappa_runtime": amp["kappa"], "resid_max": amp["resid_max"],
                  "resid_G_tt_max": amp["resid_tt_max"],
                  "resid_G_ss_max": amp["resid_ss_max"],
                  "resid_Gkk_theorem_max": amp["resid_theorem_max"],
                  "resid_null_norm_max": amp["resid_null_max"],
                  "resid_G22_minus_beta_max": amp["resid_g22_beta_max"],
                  "points": amp["points"],
                  "note": "amplificacao v138 [DER]: cone nulo cego no radial (um.py "
                          "v120/v133, digital-twin) — G_tt=G_ss=0 (Bianchi) e "
                          "G_kk=(c^2+d^2)*G22 re-derivados numericamente; kappa=sqrt(beta) "
                          "em runtime => custo transversal por unidade (c^2+d^2) = beta. "
                          "[ONTO] a direcao da viagem e cega, o custo vive no transversal. "
                          "Matematica pura; NAO e propulsao nem veredito fisico."})
    print(f"[one_motor_dobra] amp v138 cone nulo: resid_max={amp['resid_max']:.3e} "
          f"(G_tt/G_ss cegos; G_kk=(c^2+d^2)*G22; |G22-beta|max="
          f"{amp['resid_g22_beta_max']:.3e}) [DER]")

    # ------------------------------------------------------------------ #
    # AMPLIFICACAO v144 — O RESGATE DO OBSERVADOR (um.py pedra 100,       #
    # ObserverInside). [DER] o operador do dispositivo T = MANIFEST o     #
    # REFLECT (Dobra x2 Boundary->Bulk) E a projecao INVERSA IDEMPOTENTE  #
    # do teorema: T^2=T (bitwise), le o permanente sem perda, T != id.    #
    # FALSIDADE DE GENERO tipada no rival vazante R=(1-beta)*T: sem       #
    # ponto fixo nao-nulo (lemas T^2=T + homogeneidade), defeito de       #
    # idempotencia = beta EXATO, decaimento EXATO em duas leituras:       #
    # passe n/passe 1 = (1-beta)^(n-1) e passe n/T(L0) = (1-beta)^n,      #
    # R(0)=0 => so 0 permanece => sem observador interno => transporte    #
    # REJEITADO.                                                          #
    # [ONTO] o que a dobra transporta e o PERMANENTE; um canal que vaza   #
    # beta por passe nao tem nada para entregar. [HARDWARE digital-twin]: #
    # matematica do mecanismo, nunca propulsao nem veredito fisico.       #
    # ------------------------------------------------------------------ #
    obs = _amp_v144_observer_inside(beta, acom_mirror)
    tests.append({"test": "observer_inside_idempotent_fold", "passed": bool(obs["passed"]),
                  "angular_bits": obs["angular_bits"], "lam_runtime": obs["lam_runtime"],
                  "resid_idempotent_T2_T": obs["resid_idempotent_T2_T"],
                  "loss_first_pass": obs["loss_first_pass"],
                  "one_minus_corr_read_permanent": obs["one_minus_corr_read_permanent"],
                  "resid_homogeneity": obs["resid_homogeneity"],
                  "rival_idem_defect": obs["rival_idem_defect"],
                  "rival_idem_defect_minus_beta": obs["rival_idem_defect_minus_beta"],
                  "rival_fixed_displacement": obs["rival_fixed_displacement"],
                  "rival_fixed_displacement_minus_beta": obs["rival_fixed_displacement_minus_beta"],
                  "rival_leak_per_pass": obs["rival_leak_per_pass"],
                  "rival_leak_minus_beta": obs["rival_leak_minus_beta"],
                  "rival_decay_resid_vs_lam_pow_nm1": obs["rival_decay_resid_vs_lam_pow_nm1"],
                  "rival_decay_full_resid_vs_lam_pow_n": obs["rival_decay_full_resid_vs_lam_pow_n"],
                  "n_passes": obs["n_passes"],
                  "rival_zero_is_fixed": obs["rival_zero_is_fixed"],
                  "note": "amplificacao v144 [DER/ONTO]: O RESGATE DO OBSERVADOR (um.py "
                          "pedra 100, ObserverInside) no operador do dispositivo — "
                          "T=MANIFEST o REFLECT e projecao INVERSA IDEMPOTENTE (T^2=T "
                          "bitwise) que LE O PERMANENTE sem perda (1-corr=0 no ponto "
                          "fixo) e NAO e a identidade (perda de 1o passe > 0: o "
                          "transiente morre na fronteira). FALSIDADE DE GENERO tipada: "
                          "o fluxo vazante R=(1-beta)*T nao tem ponto fixo nao-nulo "
                          "(T^2=T + homogeneidade => L*=0); defeito de idempotencia do "
                          "rival = beta EXATO; deslocamento de todo candidato permanente "
                          "= beta EXATO; decaimento exato em DUAS leituras: passe n/"
                          "passe 1 = (1-beta)^(n-1) e passe n/T(L0) = (1-beta)^n (n=64); "
                          "R(0)=0 => so 0 "
                          "permanece => sem observador interno => transporte REJEITADO. "
                          "beta em runtime; matematica do mecanismo [SIM][HARDWARE]; "
                          "NAO e propulsao nem veredito fisico."})
    print(f"[one_motor_dobra] amp v144 observador: T^2=T resid={obs['resid_idempotent_T2_T']:.1e} "
          f"(le o permanente: 1-corr={obs['one_minus_corr_read_permanent']:.1e}); "
          f"rival vazante REJEITADO (defeito={obs['rival_idem_defect']:.12f} = beta, "
          f"|dif|={obs['rival_idem_defect_minus_beta']:.1e}; so 0 permanece) [DER]")
    print(f"[one_motor_dobra] amp v144 decaimento (n={obs['n_passes']}): "
          f"passe-n/passe-1 vs (1-beta)^(n-1) resid={obs['rival_decay_resid_vs_lam_pow_nm1']:.1e}; "
          f"passe-n/T(L0) vs (1-beta)^n resid={obs['rival_decay_full_resid_vs_lam_pow_n']:.1e} [DER]")

    # ------------------------------------------------------------------ #
    # AMPLIFICACAO v168 — A SECAO ERGODICA (ErgodicMeanSection +          #
    # EquivariantSection + BreuerTrace, um.py v166-v167, Item A em        #
    # kernel; 0 sorry, 0 axiom). [DER] o LIMITE DE BIRKHOFF instanciado   #
    # na dinamica angular do dispositivo: theta_M = arcsin(sqrt(beta))    #
    # e' o angulo da rotacao de fronteira (Spec {e^{+-i theta_M}});       #
    # a media (1/N) sum U^k converge a projecao invariante P (o setor     #
    # PERMANENTE) com taxa de Dirichlet EXATA; U P = P U = P (secao       #
    # equivariante); Tr(P) = peso do permanente (o peso e' TRACO).        #
    # NEGATIVOS: M_N != P em N finito (anti-tautologia) e o rival         #
    # vazante (1-beta)*U tem media de Birkhoff -> 0 (forma fechada        #
    # c_N=(1-(1-beta)^N)/(N beta)): o vazamento DESTROI a projecao        #
    # invariante => nada sobrevive a media => transporte REJEITADO        #
    # (face ergodica, distinta do ponto fixo v144).                       #
    # [HARDWARE digital-twin]: matematica do mecanismo, nunca propulsao   #
    # nem veredito fisico.                                                #
    # ------------------------------------------------------------------ #
    erg = _amp_v168_ergodic_mean(beta, tgl_core.theta_m())
    tests.append({"test": "ergodic_mean_section_birkhoff", "passed": bool(erg["passed"]),
                  "theta_m_runtime": erg["theta_m_runtime"],
                  "resid_isometry": erg["resid_isometry"],
                  "resid_equivariant_UP_PU_P": erg["resid_equivariant_UP_PU_P"],
                  "resid_projection": erg["resid_projection"],
                  "resid_dirichlet_exact_rate": erg["resid_dirichlet_exact_rate"],
                  "birkhoff_ladder": erg["birkhoff_ladder"],
                  "err_first_N8": erg["err_first_N8"],
                  "err_last_N4096": erg["err_last_N4096"],
                  "bound_last": erg["bound_last"],
                  "trace_defect": erg["trace_defect"],
                  "trace_bound": erg["trace_bound"],
                  "trace_P_weight_permanent": erg["trace_P_weight_permanent"],
                  "lam_runtime": erg["lam_runtime"],
                  "leak_mean_c_N_closed": erg["leak_mean_c_N_closed"],
                  "resid_leak_closed_form": erg["resid_leak_closed_form"],
                  "dist_leak_mean_to_P": erg["dist_leak_mean_to_P"],
                  "norm_leak_mean": erg["norm_leak_mean"],
                  "leak_bound": erg["leak_bound"], "N_big": erg["N_big"],
                  "note": "amplificacao v168 [DER/ONTO]: A SECAO ERGODICA (um.py "
                          "v166-v167, Item A em kernel: ErgodicMeanSection + "
                          "EquivariantSection + BreuerTrace) na dinamica angular do "
                          "dispositivo — U = I (+) R(theta_M) (+) R(2 theta_M), "
                          "theta_M = arcsin(sqrt(beta)) em runtime; a media de "
                          "Birkhoff (1/N) sum U^k converge a projecao invariante P "
                          "(setor permanente) com taxa de Dirichlet EXATA "
                          "|sin(N t/2)|/(N sin(t/2)); U P = P U = P (secao "
                          "equivariante); Tr(P) = peso do permanente (o peso e' "
                          "traco). NEGATIVOS: M_N != P em N finito; rival vazante "
                          "(1-beta)*U tem media -> 0 (forma fechada "
                          "c_N=(1-(1-beta)^N)/(N beta) conferida) => a projecao "
                          "invariante e' DESTRUIDA pelo vazamento => transporte "
                          "REJEITADO na face ergodica. beta/theta_M em runtime; "
                          "[SIM][HARDWARE] digital-twin — NAO e' propulsao nem "
                          "veredito fisico."})
    print(f"[one_motor_dobra] amp v168 secao ergodica: Birkhoff err N=8 "
          f"{erg['err_first_N8']:.3f} -> N=4096 {erg['err_last_N4096']:.3e} "
          f"(<= bound {erg['bound_last']:.3e}); taxa Dirichlet exata resid="
          f"{erg['resid_dirichlet_exact_rate']:.1e}; U P = P U = P resid="
          f"{erg['resid_equivariant_UP_PU_P']:.1e} [DER]")
    print(f"[one_motor_dobra] amp v168 rival vazante: media(N={erg['N_big']}) "
          f"norma {erg['norm_leak_mean']:.3e} <= 1/(N*beta) {erg['leak_bound']:.3e}; "
          f"c_N fechada resid={erg['resid_leak_closed_form']:.1e}; dist a P = "
          f"{erg['dist_leak_mean_to_P']:.4f} => projecao invariante destruida; "
          f"transporte REJEITADO (face ergodica) [DER]")

    # ------------------------------------------------------------------ #
    # AMPLIFICACAO v206 — A INTERFACE DA LUZ (TGLExt/TheLightInterface,   #
    # kernel v206 formal 197-204; 0 sorry, 0 axiom; custodia               #
    # vault/originals_copy/tgl_kernel_v206). [DER] re-derivacao numerica   #
    # da estrutura provada em kernel, no operador do dispositivo: a        #
    # patente publica g=sqrt(|L|) (REFLECT, a RAIZ) e a Dobra x2           #
    # L'=s*(g_max*sin theta)^2 (MANIFEST, o QUADRADO); a pedra prova que   #
    # o quadrado da luz e o graviton (eps_pm (x) eps_pm = root_pm), que    #
    # o gerador le a luz a peso 1 e o tensor a peso 2, e que a fase do     #
    # tensor e o QUADRADO da fase do vetor (e^{i theta} -> e^{2i theta}).  #
    # No angulo do dispositivo theta_M = arcsin(sqrt(beta)) as DUAS faces  #
    # do quadrado coincidem: intensidade sin^2(theta_M) = beta (o          #
    # MANIFEST da patente) e fase e^{2i theta_M} (a lei da pedra).         #
    # NEGATIVOS por logica: a lei errada (mesma fase) falha com gap        #
    # derivado 2*sin(theta_M/2); a luz LINEAR (1,0) nao quadra para raiz   #
    # (B^2=B!=0) nem e autovetor do gerador => a interface e SO a          #
    # polarizacao circular de peso 1. [HARDWARE digital-twin]:             #
    # matematica do mecanismo, nunca propulsao nem veredito fisico.        #
    # ------------------------------------------------------------------ #
    li = _amp_v206_light_interface(beta, tgl_core.theta_m())
    tests.append({"test": "light_interface_phase_square", "passed": bool(li["passed"]),
                  "theta_m_runtime": li["theta_m_runtime"],
                  "resid_K2_plus_1": li["resid_K2_plus_1"],
                  "resid_projections": li["resid_projections"],
                  "resid_roots_are_polarizations": li["resid_roots_are_polarizations"],
                  "resid_ladder_weights_pm_2i": li["resid_ladder_weights_pm_2i"],
                  "norm_root": li["norm_root"],
                  "resid_nilpotent": li["resid_nilpotent"],
                  "resid_ladder_factors_projections": li["resid_ladder_factors_projections"],
                  "resid_light_squares_to_graviton": li["resid_light_squares_to_graviton"],
                  "resid_half_weight_light": li["resid_half_weight_light"],
                  "weight_vector": li["weight_vector"],
                  "weight_tensor": li["weight_tensor"],
                  "resid_weight_doubling": li["resid_weight_doubling"],
                  "n_angles_swept": li["n_angles_swept"],
                  "resid_vector_phase_max": li["resid_vector_phase_max"],
                  "resid_tensor_phase_square_max": li["resid_tensor_phase_square_max"],
                  "resid_angle_is_projection_max": li["resid_angle_is_projection_max"],
                  "sin2_theta_m": li["sin2_theta_m"],
                  "resid_sin2_minus_beta": li["resid_sin2_minus_beta"],
                  "manifest_at_miguel": li["manifest_at_miguel"],
                  "resid_manifest_minus_beta": li["resid_manifest_minus_beta"],
                  "resid_phase_square_theta_m": li["resid_phase_square_theta_m"],
                  "wrong_law_resid": li["wrong_law_resid"],
                  "expected_gap": li["expected_gap"], "gap_check": li["gap_check"],
                  "bad_light_nilpotency_defect": li["bad_light_nilpotency_defect"],
                  "bad_light_eigen_defect": li["bad_light_eigen_defect"],
                  "note": "amplificacao v206 [DER/ONTO]: A INTERFACE DA LUZ "
                          "(TGLExt/TheLightInterface.lean, kernel v206 formal 197-204, "
                          "0 sorry 0 axiom; estrutura RE-DERIVADA numericamente — nunca "
                          "se finge rodar Lean) no operador do dispositivo: o quadrado "
                          "da luz e o graviton (eps_pm (x) eps_pm = root_pm), o gerador "
                          "le a luz a peso 1 e o tensor a peso 2 ([K,root_pm] = "
                          "+-2i root_pm), a escada fatora as projecoes (root_p root_m = "
                          "4 P_plus) e a fase do tensor e o QUADRADO da fase do vetor "
                          "(O_theta root O_theta^T = e^{2i theta} root). A Dobra x2 da "
                          "patente (MANIFEST L' = s*(g_max sin theta)^2) e a face de "
                          "intensidade do MESMO quadrado: em theta_M = arcsin(sqrt(beta)) "
                          "runtime, sin^2(theta_M) = beta = manifest de Miguel, e a fase "
                          "correspondente e e^{2i theta_M}. g = sqrt(|L|) sobrevive "
                          "intacta — so a seta de leitura inverte (a luz e a raiz do "
                          "graviton). NEGATIVOS por logica: a lei errada (tensor com a "
                          "mesma fase do vetor) falha com gap derivado 2 sin(theta_M/2); "
                          "a luz linear (1,0) nao quadra para raiz nilpotente nem e "
                          "autovetor => a interface e SO o peso 1 circular. DELIMITACAO "
                          "da pedra mantida: sem foton fisico, sem Maxwell, sem U(1); "
                          "genK e SO(2), nao o J modular. beta/theta_M em runtime; "
                          "[SIM][HARDWARE] digital-twin — NAO e propulsao nem veredito "
                          "fisico; physical_verdict_allowed=false."})
    print(f"[one_motor_dobra] amp v206 interface da luz: eps(x)eps=root resid="
          f"{li['resid_light_squares_to_graviton']:.1e}; pesos {li['weight_vector']:.0f}->"
          f"{li['weight_tensor']:.0f} (o angulo DOBRA, resid={li['resid_weight_doubling']:.1e}); "
          f"fase^2 em {li['n_angles_swept']} angulos resid_max="
          f"{li['resid_tensor_phase_square_max']:.1e} [DER]")
    print(f"[one_motor_dobra] amp v206 amarra: sin^2(theta_M)-beta="
          f"{li['resid_sin2_minus_beta']:.1e} (manifest de Miguel = beta); lei errada "
          f"FALHA com gap derivado {li['expected_gap']:.4f} (check={li['gap_check']:.1e}); "
          f"luz linear rejeitada (nilp defect={li['bad_light_nilpotency_defect']:.1f}, "
          f"eigen defect={li['bad_light_eigen_defect']:.1f}) [DER]")

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

    def _o5_md_quant():
        bits_l = list(range(4, 15)); errs = []
        for b_ in bits_l:
            m_ = acom_mirror.DimensionalMirror(angular_bits=b_)
            rec_ = m_.manifest(m_.reflect(payload))
            errs.append(float(np.sqrt(np.mean((rec_ - payload) ** 2))))
        slope = float(np.polyfit(bits_l, np.log2(np.array(errs)), 1)[0])
        ok = abs(slope + 1.0) < 0.2 and errs[-1] < errs[0] / 50.0 and abs(slope + 2.0) > 0.5
        return {"passed": ok, "bits": bits_l, "rms_by_bits": errs, "slope_log2_rms_per_bit": slope,
                "note": "o erro RMS do round-trip cai por 2 a cada bit angular (erro linear em dtheta); "
                        "a lei 'dois bits por bit' e rejeitada"}
    _o5("roundtrip_error_halves_per_bit", _o5_md_quant)

    def _o5_md_farol_table():
        table = {}
        for adj in (True, False):
            for eth in (True, False):
                seq_, com_ = farol(adj, eth)
                table["adj=%s,eth=%s" % (adj, eth)] = {"commit": bool(com_), "last": seq_[-1]}
        ok = (table["adj=True,eth=True"]["commit"]
              and not table["adj=True,eth=False"]["commit"] and table["adj=True,eth=False"]["last"] == "F3_ETHICAL_VETO"
              and not table["adj=False,eth=True"]["commit"] and table["adj=False,eth=True"]["last"] == "F4_ABORT_NOT_ADJACENT"
              and not table["adj=False,eth=False"]["commit"] and table["adj=False,eth=False"]["last"] == "F3_ETHICAL_VETO")
        return {"passed": ok, "truth_table": table,
                "note": "tabela-verdade exaustiva do Farol Psi: commit SO com adjacencia E etica; o veto etico (F3) precede "
                        "a adjacencia (F4) — quando ambos falham, e o veto que aparece"}
    _o5("farol_truth_table_exhaustive", _o5_md_farol_table)

    def _o5_md_metric():
        S_ = [state_vec(payload), state_vec(payload + 0.3 * rng.standard_normal((64, 64))),
              state_vec(rng.standard_normal((64, 64)) * 2.0)]
        D_ = lambda a_, b_: float(np.linalg.norm(a_ - b_))
        sym = max(abs(D_(S_[i], S_[j]) - D_(S_[j], S_[i])) for i in range(3) for j in range(3))
        ident = max(D_(S_[i], S_[i]) for i in range(3))
        tri = all(D_(S_[i], S_[k]) <= D_(S_[i], S_[j]) + D_(S_[j], S_[k]) + 1e-12
                  for i in range(3) for j in range(3) for k in range(3))
        D2 = lambda a_, b_: float(np.linalg.norm(a_ - b_)) ** 2
        viol = int(sum(1 for i in range(3) for j in range(3) for k in range(3)
                       if D2(S_[i], S_[k]) > D2(S_[i], S_[j]) + D2(S_[j], S_[k]) + 1e-12))
        ok = sym < 1e-12 and ident == 0.0 and tri and viol > 0
        return {"passed": ok, "symmetry_resid": sym, "identity_resid": ident, "triangle_ok": tri,
                "neg_squared_distance_triangle_violations": viol,
                "note": "D_Psi e uma METRICA sobre os estados (simetrica, D(A,A)=0, triangular em 27 triplas); a 'distancia' "
                        "quadratica viola a triangular — rejeitada como gate de adjacencia"}
    _o5("adjacency_D_psi_is_a_metric", _o5_md_metric)

    def _o5_md_idempotent_bits():
        rows = {}
        for b_ in (4, 8, 12):
            m_ = acom_mirror.DimensionalMirror(angular_bits=b_)
            T1 = m_.manifest(m_.reflect(payload)); T2 = m_.manifest(m_.reflect(T1))
            rows[b_] = {"idem_resid": float(np.max(np.abs(T2 - T1))),
                        "loss_first": float(np.max(np.abs(T1 - payload)) / np.max(np.abs(payload)))}
        ok = all(r_["idem_resid"] < 1e-12 for r_ in rows.values()) and rows[4]["loss_first"] > rows[12]["loss_first"] > 0.0
        return {"passed": ok, "by_bits": {str(k): v for k, v in rows.items()},
                "note": "T = MANIFEST o REFLECT e idempotente (T^2 = T) em 4, 8 e 12 bits — a projecao le o permanente; "
                        "e T != id, com perda que CAI com os bits (o transiente morre na fronteira)"}
    _o5("fold_idempotent_across_bits", _o5_md_idempotent_bits)

    def _o5_md_null_cone_beta():
        a1 = _amp_v138_null_cone(beta); a2 = _amp_v138_null_cone(2.0 * beta)
        blind2 = bool(a2["resid_tt_max"] < 1e-10 and a2["resid_ss_max"] < 1e-10 and a2["resid_theorem_max"] < 1e-10)
        ok = bool(a1["passed"]) and blind2 and abs(a2["kappa"] ** 2 - 2.0 * beta) < 1e-15
        return {"passed": ok, "kappa2_at_beta": a1["kappa"] ** 2, "kappa2_at_2beta": a2["kappa"] ** 2, "radial_blind_at_2beta": blind2,
                "note": "a cegueira radial (G_tt = G_ss = 0, Bianchi) e ESTRUTURAL — vale para kappa^2 = beta e 2 beta; "
                        "o custo transversal G22 = kappa^2 responde ao acoplamento (dobra com 2 beta)"}
    _o5("radial_blindness_structural_cost_scales", _o5_md_null_cone_beta)

    def _o5_md_ergodic_beta():
        tm1 = math.asin(math.sqrt(beta)); tm2 = math.asin(math.sqrt(2.0 * beta))
        e1 = _amp_v168_ergodic_mean(beta, tm1); e2 = _amp_v168_ergodic_mean(2.0 * beta, tm2)
        ratio = e1["bound_last"] / e2["bound_last"]; expected = math.sin(tm2 / 2.0) / math.sin(tm1 / 2.0)
        ok = bool(e1["passed"]) and bool(e2["passed"]) and abs(ratio - expected) < 1e-9 and 1.3 < ratio < 1.5
        return {"passed": ok, "bound_ratio_beta_over_2beta": ratio, "expected_sin_ratio": expected,
                "note": "o bound de Birkhoff 1/(N sin(theta/2)) responde ao acoplamento: com 2 beta o bound cai por "
                        "sin(theta_2/2)/sin(theta_1/2) ~ sqrt(2) (medido = forma fechada)"}
    _o5("birkhoff_bound_responds_to_beta", _o5_md_ergodic_beta)

    passed = sum(1 for t in tests if t["passed"]); total = len(tests); all_ok = passed == total
    summary = {"tests_passed": passed, "tests_total": total, "roundtrip_correlation": corr,
               "roundtrip_corr_16bits": sweeps["corr_hi"],
               "multi_payload_corr_min": sweeps["corr_min_payload"],
               "adjacency_eps_c": eps_c, "commit_sigma_boundary": sweeps["sigma_boundary"],
               "observer_idempotent_resid": obs["resid_idempotent_T2_T"],
               "observer_rival_defect_eq_beta": obs["rival_idem_defect"],
               "ergodic_birkhoff_err_N4096": erg["err_last_N4096"],
               "ergodic_dirichlet_rate_resid": erg["resid_dirichlet_exact_rate"],
               "ergodic_leak_mean_norm": erg["norm_leak_mean"],
               "light_interface_tensor_phase_sq_resid": li["resid_tensor_phase_square_max"],
               "light_interface_sin2_thetaM_minus_beta": li["resid_sin2_minus_beta"],
               "light_interface_wrong_law_gap": li["expected_gap"],
               "sweeps": {"angular_bits_curve": conv_curve, "payload_correlations": payload_corr,
                          "d_psi_vs_sigma": [(s, d) for s, d, _ in adj_curve],
                          "commit_fraction_vs_eps_c": commit_frac_curve},
               "seal": "digital-twin; propulsão NÃO demonstrada; sem protótipo"}
    max_verdict = ("WARP_DIGITAL_TWIN_DEMONSTRATED ([SIM][HARDWARE] — REFLECT/MANIFEST, gate de "
                   "adjacência e Farol Ψ com veto ético fecham como DIGITAL-TWIN; transporte "
                   "físico, dobra e τ≈10⁻⁴² s NÃO simulados nem alegados)")
    _finish(PATENT_DIR, CENTRAL, ts, PATENT_ID, SLUG, "one_motor_dobra.py",
            ["[SIM]", "[HARDWARE]"], beta, beta_ok, all_ok, max_verdict, tests, summary,
            module_hashes,
            "DIGITAL-TWIN — simulação não valida física; sem protótipo; propulsão NÃO "
            "demonstrada. REFLECT/MANIFEST é preservação de invariante algorítmica, não "
            "transporte físico [HARDWARE].",
            fig_builder=lambda plt, fd: _fig_motor(plt, fd, payload, acom_mirror, sweeps))

    # FORMA = CONTEÚDO: re-carimba render3d.json (SEM geometria computável — corpo preservado)
    sweeps["ergodic"] = erg
    sweeps["light"] = li
    emit_render3d(beta, sweeps)
    return 0 if all_ok else 1


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


def _fig_motor(plt, fig_dir, payload, acom_mirror, sweeps=None):
    figs = []
    # Figura 1 — REFLECT/MANIFEST (origem vs manifestado)
    _, r = acom_mirror.roundtrip_correlation(payload, angular_bits=16)
    out = acom_mirror.DimensionalMirror(angular_bits=16).manifest(r)
    fig, ax = plt.subplots(1, 2, figsize=(7.5, 3.6))
    ax[0].imshow(payload, cmap="viridis"); ax[0].set_title("origem (ψ,θ) [SIM]", fontsize=9); ax[0].axis("off")
    ax[1].imshow(out, cmap="viridis"); ax[1].set_title("manifestado L'=s·(gmax·sinθ)² [SIM]", fontsize=9); ax[1].axis("off")
    fig.suptitle("Motor de Dobra — REFLECT/MANIFEST digital-twin (não é transporte físico)", fontsize=10)
    fp = fig_dir / "fig_reflect_manifest.png"; plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close()
    figs.append("fig_reflect_manifest.png")
    if not sweeps:
        return figs

    # Figura 2 — convergência round-trip vs angular_bits + correlação por família de payload
    conv = sweeps["conv_curve"]; pc = sweeps["payload_corr"]
    bits = [b for b, _ in conv]; err = [max(1.0 - c, 1e-12) for _, c in conv]
    fig, ax = plt.subplots(1, 2, figsize=(9.0, 3.6))
    ax[0].semilogy(bits, err, "o-", color="#2a7ae2")
    ax[0].set_xlabel("angular_bits"); ax[0].set_ylabel("1 − corr (perda round-trip)")
    ax[0].set_title("convergência REFLECT/MANIFEST [SIM]", fontsize=9)
    ax[0].grid(True, which="both", alpha=0.3)
    names = list(pc.keys()); vals = [pc[k] for k in names]
    ax[1].barh(range(len(names)), vals, color="#33aa55")
    ax[1].set_yticks(range(len(names))); ax[1].set_yticklabels(names, fontsize=7)
    ax[1].set_xlim(0.98, 1.0005); ax[1].set_xlabel("corr round-trip (16 bits)")
    ax[1].set_title("invariante por família de payload [SIM]", fontsize=9)
    ax[1].grid(True, axis="x", alpha=0.3)
    fig.suptitle("Motor de Dobra — varreduras de round-trip (digital-twin)", fontsize=10)
    fp = fig_dir / "fig_roundtrip_sweeps.png"; plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close()
    figs.append("fig_roundtrip_sweeps.png")

    # Figura 3 — gate de adjacência: D_Ψ vs σ (fronteira ε_c) e fração de commit vs ε_c
    adj = sweeps["adj_curve"]; cf = sweeps["commit_frac_curve"]
    eps_c = sweeps["eps_c"]; sb = sweeps["sigma_boundary"]
    sig = [s for s, _, _ in adj]; dps = [d for _, d, _ in adj]
    fig, ax = plt.subplots(1, 2, figsize=(9.0, 3.6))
    ax[0].semilogx(sig, dps, "o-", color="#cc4433", label="D_Ψ(A, A+ruído)")
    ax[0].axhline(eps_c, color="#7ce7c8", ls="--", label=f"ε_c={eps_c}")
    if sb is not None:
        ax[0].axvline(sb, color="#ff9f0a", ls=":", label=f"σ*≈{sb:.3g}")
    ax[0].set_xlabel("σ (ruído de perturbação)"); ax[0].set_ylabel("D_Ψ (distância modular)")
    ax[0].set_title("gate de adjacência: fronteira de commit [SIM]", fontsize=9)
    ax[0].legend(fontsize=7); ax[0].grid(True, which="both", alpha=0.3)
    ex = [e for e, _ in cf]; fr = [f for _, f in cf]
    ax[1].plot(ex, fr, "-", color="#2a7ae2")
    ax[1].axvline(eps_c, color="#7ce7c8", ls="--", label=f"ε_c={eps_c}")
    ax[1].set_xlabel("ε_c (limiar)"); ax[1].set_ylabel("fração de commit")
    ax[1].set_title("fração de commit vs ε_c (monotônica) [SIM]", fontsize=9)
    ax[1].legend(fontsize=7); ax[1].grid(True, alpha=0.3)
    fig.suptitle("Motor de Dobra — gate de adjacência D_Ψ (digital-twin)", fontsize=10)
    fp = fig_dir / "fig_adjacency_gate.png"; plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close()
    figs.append("fig_adjacency_gate.png")
    return figs


def emit_render3d(beta, sweeps):
    """Re-carimba patents/<ID>/render3d.json em MODO MERGE.

    Motor de Dobra = SEM geometria computável: as câmaras origem/destino e os 6 estados
    do Farol Ψ são gabarito de engenharia (posições de projeto, não saída de simulação).
    Portanto PRESERVA integralmente meshes/nodes/edges/layers/groups/dimensions do corpo
    já existente; apenas atualiza generated_by e injeta β runtime + métricas COMPUTADAS
    desta run em d['constants']. Valida coerência antes de reescrever."""
    out = PATENT_DIR / "render3d.json"
    d = json.loads(out.read_text(encoding="utf-8"))

    # PRESERVA o corpo; só re-carimba a proveniência (forma = conteúdo).
    d["generated_by"] = "one_motor_dobra.py (forma=conteudo)"

    # injeta β runtime + 1-2 métricas computadas desta run (constants é lista de dicts)
    consts = [c for c in d.get("constants", [])
              if c.get("symbol") not in ("beta_TGL", "corr_roundtrip", "gate_adjacencia",
                                         "secao_ergodica", "interface_luz")]
    consts.append({"symbol": "beta_TGL",
                   "value": f"{beta:.12f} (alpha*sqrt(e))",
                   "note": "injetado em runtime pelo runner; nunca literal"})
    consts.append({"symbol": "corr_roundtrip",
                   "value": f"{sweeps['corr_hi']:.6f} @16 bits",
                   "note": f"min sobre 6 familias de payload = {sweeps['corr_min_payload']:.6f} [SIM]"})
    sb = sweeps["sigma_boundary"]
    consts.append({"symbol": "gate_adjacencia",
                   "value": (f"eps_c={sweeps['eps_c']}, sigma*={sb:.4g}" if sb is not None
                             else f"eps_c={sweeps['eps_c']}"),
                   "note": "fronteira de commit D_Psi<eps_c computada por varredura de ruido [SIM]"})
    erg = sweeps.get("ergodic")
    if erg:
        consts.append({"symbol": "secao_ergodica",
                       "value": (f"Birkhoff err(N={erg['N_big']})={erg['err_last_N4096']:.3e} "
                                 f"<= {erg['bound_last']:.3e}; rival vazante media="
                                 f"{erg['norm_leak_mean']:.3e}"),
                       "note": "amp v168 ErgodicMeanSection (um.py v166-v167): media de "
                               "Birkhoff -> projecao invariante; rival (1-beta)*U -> 0 [DER][SIM]"})
    li = sweeps.get("light")
    if li:
        consts.append({"symbol": "interface_luz",
                       "value": (f"eps(x)eps=root resid={li['resid_light_squares_to_graviton']:.1e}; "
                                 f"fase^2 resid_max={li['resid_tensor_phase_square_max']:.1e} "
                                 f"({li['n_angles_swept']} angulos); sin^2(theta_M)-beta="
                                 f"{li['resid_sin2_minus_beta']:.1e}"),
                       "note": "amp v206 TheLightInterface (kernel v206): o quadrado da luz "
                               "e o graviton; fase do tensor = quadrado da fase do vetor; "
                               "Dobra x2 = face de intensidade do mesmo quadrado [DER][SIM]"})
    d["constants"] = consts

    # VALIDAÇÃO: ids de layer e de edge coerentes com o corpo preservado
    layer_ids = {l["id"] for l in d.get("layers", [])}
    node_ids = {n["id"] for n in d.get("nodes", [])}
    mesh_ids = {m["id"] for m in d.get("meshes", [])}
    for m in d.get("meshes", []):
        if m.get("layer") and m["layer"] not in layer_ids:
            raise ValueError(f"mesh {m['id']} layer '{m['layer']}' ausente em layers")
    for nd in d.get("nodes", []):
        if nd.get("layer") and nd["layer"] not in layer_ids:
            raise ValueError(f"node {nd['id']} layer '{nd['layer']}' ausente em layers")
    ref = node_ids | mesh_ids
    for e in d.get("edges", []):
        if e["from"] not in ref or e["to"] not in ref:
            raise ValueError(f"edge {e} referencia id inexistente em nodes+meshes")

    out.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[{SLUG}] render3d.json EMITIDO (forma=conteudo) — corpo preservado "
          f"({len(d.get('meshes', []))} malhas, {len(d.get('nodes', []))} nos re-carimbados)")


if __name__ == "__main__":
    sys.exit(main())
