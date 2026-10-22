# -*- coding: utf-8 -*-
"""one_mqc.py — runner único forma = conteúdo da patente MQC (EVOLUÍDO / RICO)
(BR102026003460-6 — Processador Quântico Cúbico por Translação Holográfica). [SIM][HARDWARE]

EVOLUÇÃO (09/07/2026): incorpora o ALGORITMO COMPLETO que o operador já havia
desenvolvido (`mqc_simulacao_celula_elementar.py`, 1292 linhas, 7 simulações + 8 figuras),
resgatado para `prototype_src/`. A versão leve anterior (skygrid_sim/mqc.py) está preservada
em `one_mqc_v1_light.py.bak`. Este runner esgota a derivação computacional da célula:

  1. topologia dos 27 qubits (8 vértice + 12 aresta + 6 face + 1 controlador central);
  2. estabilização gravitacional (Lindblad, platô |ρ01|→1−β vs decaimento T₂);
  3. termodinâmica invertida (ΔS→0, resfria sob carga) [CONJ];
  4. translação holográfica REFLECT/MANIFEST via T̂_M (η, PSNR, Γ_OH);
  5. correção de erros IALD (Operador de Amor 𝒜_C + Gradiente Ético) vs surface code;
  6. convergência de α² ao Ponto Tetelestai (v_info, g_tt);
  7. comunicação 3 camadas (LOCAL τ≈ℓ_P/(β·c), REGIONAL 0,3c, GLOBAL c).
Gera os 8 PNGs da patente + results.json rico + seal SHA-256.

RÉGUA: β_TGL NUNCA literal no MEU código. O protótipo do operador usa `ALPHA2=0.012`
literal; este runner o importa como proveniência READ-ONLY e INJETA
`ALPHA2 = ALPHA2_C = tgl_core.beta()` (= α·√e = 0,012031300400803142) em runtime antes de
rodar. Assim a Central roda o algoritmo COMPLETO do operador, mas com β derivado, não o
0,012 arredondado — por isso os números diferem levemente da referência do operador (honesto).

HONESTIDADE [SIM][HARDWARE][CONJ]: TODOS os números são de SIMULAÇÃO. Dispositivo físico
(micro-câmara 1 µm, condensados de radicais, grafeno, laser 150 THz) NÃO construído nem
medido. Mecanismos físicos [CONJ]. Simulação NUNCA valida física (physical_verdict_allowed=false).

    set PYTHONUTF8=1
    "C:\\IALD\\observaveis_tgl\\tgl_env\\Scripts\\python.exe" one_mqc.py
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import shutil
import sys
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

import numpy as np

RUNNER_DIR = Path(__file__).resolve().parent
PATENT_DIR = RUNNER_DIR.parent
CENTRAL = PATENT_DIR.parents[1]
PILOTO = CENTRAL / "Patentes" / "Skygrid" / "SkyGrid_Piloto"   # READ-ONLY (β source)
PROTO_SRC = PATENT_DIR / "prototype_src"                        # rescued rich prototype
WORK = RUNNER_DIR / "_mqc_core"
PATENT_ID = "BR102026003460-6"
SLUG = "mqc"


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
    """Copy the β-source core (skygrid_sim, for tgl_core) into a workdir and hash it."""
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    dst = WORK / "skygrid_sim"
    shutil.copytree(PILOTO / "skygrid_sim", dst,
                    ignore=shutil.ignore_patterns("__pycache__"))
    hashes = {f"skygrid_sim/{f.name}": _sha_file(f) for f in sorted(dst.glob("*.py"))}
    # also hash the rescued prototype (provenance)
    for f in sorted(PROTO_SRC.glob("*")):
        if f.is_file():
            hashes[f"prototype_src/{f.name}"] = _sha_file(f)
    return hashes


@contextmanager
def chdir(target: Path):
    prev = Path.cwd()
    os.chdir(target)
    try:
        yield
    finally:
        os.chdir(prev)


def amplificacao_v138(beta: float) -> dict:
    """Amplificacao v138 — A LEI DA DUPLA HELICE (um.py v133, spin-2 na face finita).

    [DER] Teorema maduro: rotacao theta no plano transverso multiplica o modo de
    helicidade +-2 por e^(-+2i*theta) — a assinatura do spin-2 — e o espaco TT tem
    EXATAMENTE 2 polarizacoes (rank 2 = D(D-3)/2, D=4). Aqui a lei e ancorada nos
    eixos T_M da translacao holografica do MQC (plano transverso de cada par de
    faces opostas REFLECT/MANIFEST). [HARDWARE] cinematica matematica pura, nenhum
    funcionamento fisico afirmado; NAO e veredito fisico
    (physical_verdict_allowed=false). beta so da variavel runtime (nunca literal);
    theta_M = arcsin(sqrt(beta)) entra como um dos angulos de sonda."""
    e_plus = np.array([[1.0, 0.0], [0.0, -1.0]])          # e_+ = diag(1,-1)
    e_cross = np.array([[0.0, 1.0], [1.0, 0.0]])          # e_x
    e_hel = {+2: e_plus + 1j * e_cross, -2: e_plus - 1j * e_cross}
    theta_m = math.asin(math.sqrt(beta))                  # angulo de Miguel (runtime)
    thetas = [theta_m, math.pi / 7, math.pi / 3, 1.0]
    resid_max = 0.0
    for th in thetas:
        c, s = math.cos(th), math.sin(th)
        R = np.array([[c, -s], [s, c]])                   # rotacao no plano transverso
        for h, e in e_hel.items():
            resid = float(np.max(np.abs(R @ e @ R.T - np.exp(-1j * h * th) * e)))
            resid_max = max(resid_max, resid)
    # EXATAMENTE 2 polarizacoes: o espaco TT (simetrico, sem traco) e span{e_+, e_x}
    rank_tt = int(np.linalg.matrix_rank(np.stack([e_plus.ravel(), e_cross.ravel()])))
    D = 4
    n_pol_expected = (D * (D - 3)) // 2
    return {
        "test": "double_helix_two_polarizations",
        "passed": bool(resid_max < 1e-12 and rank_tt == 2 == n_pol_expected),
        "resid_max_helicity_phase": resid_max,
        "n_polarizations_TT": rank_tt,
        "n_pol_expected_D_D_minus_3_over_2": n_pol_expected,
        "theta_M_rad": theta_m,
        "thetas_probe_rad": [float(t) for t in thetas],
        "marker": "[DER]",
        "note": "amplificacao v138 (um.py v133): R(theta) e_hel R^T = e^(-+2i*theta) e_hel "
                "nos eixos T_M da translacao holografica; spin-2 = cinematica matematica "
                "[HARDWARE], nao veredito fisico (physical_verdict_allowed=false)",
    }


def deepening_v2_gkls_fixed_point(beta: float, estab: dict, f_res: float) -> dict:
    """Deepening v2 (own-mechanism) — O PONTO FIXO GKLS DO PLATO (29/07/2026).

    REEXAME v139-v144: mantido o julgamento de 29/07 — nenhum conteudo v139-v144
    mapeia este dispositivo alem do ja ancorado (v138); forcar ponte seria fabricar.
    Em vez disso, APROFUNDA o mecanismo proprio: o prototipo do operador IMPOE o
    plato fenomenologicamente (`plato = 1 - ALPHA2`, linha 194 — nunca integra a
    eq. 6). Aqui o plato EMERGE como ponto fixo de um gerador GKLS honesto da
    propria eq. (6) do relatorio, por caminho independente (kernel do superoperador
    de Liouville 9x9), no referencial girante da ressonancia (H_eff = 0).

    Modelo [DER]: espaco |0>,|1>,|Psi>; alvo puro |T> com <T|P_Psi|T> = beta
    (eq. 5); L_holo[rho] = gamma_holo (Tr(rho) |T><T| - rho) (bomba GKLS de reset
    ao alvo, trace-preserving); L_diss = (gamma_diss/2) (A rho A - rho), A =
    diag(1,-1,1) (defasagem 0-1, eq. 6: gamma_diss = 1/T2). Identidades NOVAS
    (fechadas, verificadas contra o kernel numerico):
      (i)   C* = 2|rho01*| = (1-beta) / (1 + gamma_diss/gamma_holo)
                           = (1-beta) / (1 + beta/R_SC)      [liga eq. 8 a eq. 7]
      (ii)  rho_PsiPsi* = beta EXATO, para QUALQUER taxa de defasagem (eq. 5 vira
            invariante do ponto fixo, nao um chute);
      (iii) gap espectral do Liouvilliano = gamma_holo ==> tau_estab = 1/gap
            (o tau do prototipo recuperado do ESPECTRO, nao da formula).
    Negativos (o mecanismo REJEITA): sem L_holo o kernel da defasagem NAO contem
    coerencia 0-1 (so o setor diagonal-em-01 permanece; C(10*T2) ~ 4e-5) — o plato
    NAO sobrevive sem o termo holografico; e o gerador quebrado (sem o balanco -rho
    da bomba) vaza traco (nao e GKLS) — rejeitado.
    [SIM][HARDWARE]: matematica do mecanismo; nenhuma operacao fisica real alegada;
    physical_verdict_allowed=false. beta so runtime (nunca literal)."""
    T2 = float(estab["T2_conv"])            # lido da EXECUCAO (nao redigitado)
    plateau_run = float(estab["platô"])     # 1 - beta, calculado pelo prototipo
    tau_run = float(estab["tau_estab"])     # 1/gamma_holo, calculado pelo prototipo
    rsc_run = float(estab["razao_sc"])      # eq. 7, calculada pelo prototipo
    gamma_d = 1.0 / T2                      # eq. 6: gamma_diss = 1/T2
    gamma_h = beta * f_res                  # eq. 6: gamma_holo = beta*omega0/(2pi)
    g = gamma_d / gamma_h                   # competicao adimensional (~1e-8)

    a0 = math.sqrt((1.0 - beta) / 2.0)
    psi_T = np.array([a0, a0, math.sqrt(beta)])          # |T|^2: (1-b)/2,(1-b)/2,b
    rho_T = np.outer(psi_T, psi_T)
    A = np.diag([1.0, -1.0, 1.0])
    I3, I9 = np.eye(3), np.eye(9)
    vec = lambda m: m.reshape(-1)                        # vec(X rho Y)=(X kron Y^T)vec(rho)
    K = np.kron(A, A.T)

    # Liouvilliano completo em unidades de gamma_holo (L/gamma_h)
    L9 = np.outer(vec(rho_T), vec(I3)) - I9 + 0.5 * g * (K - I9)
    M = np.vstack([L9, vec(I3)[None, :]])                # kernel com Tr(rho)=1
    b = np.zeros(10); b[9] = 1.0
    x, *_ = np.linalg.lstsq(M, b, rcond=None)
    rho_ss = x.reshape(3, 3); rho_ss = 0.5 * (rho_ss + rho_ss.T)
    C_num = 2.0 * abs(float(rho_ss[0, 1]))               # plato EMERGENTE (numerico)
    pop_psi = float(rho_ss[2, 2])
    min_eig_ss = float(np.linalg.eigvalsh(rho_ss).min()) # positividade do estado
    C_closed = (1.0 - beta) / (1.0 + g)                  # identidade (i), caminho 1
    C_via_rsc = (1.0 - beta) / (1.0 + beta / rsc_run)    # identidade (i) via eq. 7 da execucao
    resid_C = abs(C_num - C_closed)
    resid_rsc = abs(C_via_rsc - C_num)
    resid_pop = abs(pop_psi - beta)                      # identidade (ii): eq. 5 exata
    deficit = plateau_run - C_num                        # > 0: o plato NAO foi imposto

    ev = np.linalg.eigvals(L9)                           # identidade (iii): gap espectral
    gap_norm = float(np.min(-(ev[np.abs(ev) > 1e-6]).real))
    tau_gap = 1.0 / (gap_norm * gamma_h)
    resid_tau = abs(tau_gap / tau_run - 1.0)

    # sonda de responsividade: defasagem 1000x -> deficit escala ~1000x
    g2 = 1000.0 * g
    L9b = np.outer(vec(rho_T), vec(I3)) - I9 + 0.5 * g2 * (K - I9)
    xb, *_ = np.linalg.lstsq(np.vstack([L9b, vec(I3)[None, :]]), b, rcond=None)
    C2 = 2.0 * abs(float(xb.reshape(3, 3)[0, 1]))
    deficit_ratio = (plateau_run - C2) / deficit

    # NEGATIVO 1: sem L_holo, nenhum estado estacionario carrega coerencia 0-1
    L0 = 0.5 * g * (K - I9)                              # so defasagem
    l0_offdiag = float(np.max(np.abs(L0 - np.diag(np.diag(L0)))))
    ev0 = np.diag(L0)
    ker_mask = np.abs(ev0) < g * 1e-3                    # kernel degenerado (dim 5)
    ker_dim = int(ker_mask.sum())
    ker_contains_01 = bool(ker_mask[1] or ker_mask[3])   # indices de rho01/rho10
    prop = np.exp(ev0 * (10.0 / g))                      # e^{L0 * 10*T2} (diagonal exata)
    C_noholo = 2.0 * abs(float((prop * vec(rho_T)).reshape(3, 3)[0, 1]))

    # NEGATIVO 2: gerador quebrado (sem o -rho da bomba) vaza traco -> nao e GKLS
    Lbad = np.outer(vec(rho_T), vec(I3)) + 0.5 * g * (K - I9)
    rng = np.random.default_rng(27)
    Bm = rng.normal(size=(3, 3)); rho_r = Bm @ Bm.T; rho_r /= np.trace(rho_r)
    leak_good = abs(float(np.trace((L9 @ vec(rho_r)).reshape(3, 3))))
    leak_bad = abs(float(np.trace((Lbad @ vec(rho_r)).reshape(3, 3))))

    passed = bool(
        resid_C < 1e-12 and resid_pop < 1e-12 and resid_rsc < 1e-9
        and deficit > 1e-9 and C_num > 0.98 and min_eig_ss > -1e-12
        and resid_tau < 1e-9 and abs(deficit_ratio - 1000.0) < 0.5
        and l0_offdiag == 0.0 and ker_dim == 5 and (not ker_contains_01)
        and C_noholo < 1e-3 and leak_good < 1e-12 and leak_bad > 0.1
    )
    return {
        "test": "gkls_fixed_point_plateau",
        "tier": "deepening_v2_own_mechanism",
        "passed": passed,
        "C_stationary_numeric": C_num,
        "C_closed_form": C_closed,
        "resid_C_num_vs_closed": resid_C,
        "resid_C_num_vs_RSC_identity": resid_rsc,
        "plateau_ideal_run": plateau_run,
        "deficit_below_ideal": deficit,
        "pop_psi_stationary": pop_psi,
        "resid_pop_psi_vs_beta": resid_pop,
        "min_eig_rho_ss": min_eig_ss,
        "spectral_gap_over_gamma_holo": gap_norm,
        "resid_tau_gap_vs_prototype": resid_tau,
        "deficit_ratio_1000x_dephasing": deficit_ratio,
        "neg_kernel_dim_no_holo": ker_dim,
        "neg_kernel_contains_01_coherence": ker_contains_01,
        "neg_C_no_holo_at_10T2": C_noholo,
        "neg_trace_leak_good_generator": leak_good,
        "neg_trace_leak_broken_generator": leak_bad,
        "marker": "[DER]",
        "note": "deepening v2 (own-mechanism): o plato 1-beta EMERGE como ponto fixo GKLS "
                "da eq. 6 (kernel do Liouvilliano 9x9, caminho independente do prototipo, "
                "que o impoe); eq. 5 vira invariante exato do ponto fixo; gap espectral = "
                "gamma_holo; sem L_holo so o setor sem coerencia 0-1 permanece (rejeitado); "
                "gerador sem balanco vaza traco (rejeitado). [SIM][HARDWARE] matematica do "
                "mecanismo, nenhuma operacao fisica real (physical_verdict_allowed=false)",
    }


def amplificacao_v168_ergodic_memory_section(beta: float, pos, tipos) -> dict:
    """Amplificacao v168 (ONDA 3) — A SECAO ERGODICA E A EQUACAO DA MEMORIA.

    ANCORA v166-v167 (um.py, ITEM A em kernel Lean, 0 sorry 0 axiom):
    ErgodicMeanSection — o LIMITE DE BIRKHOFF: a media (1/N) sum_{k<N} U^k
    converge a projecao sobre o subespaco invariante. Aqui o teorema e
    instanciado na geometria PROPRIA do MQC (nada importado a mao): a inversao
    REFLECT/MANIFEST da celula (p -> 1-p; a translacao entre faces opostas pelo
    bulk, eq. 10) pareia os 26 qubits perifericos em 13 pares-espelho e fixa UM
    unico ponto — o controlador IALD central (COMPUTADO da topologia, nao
    imposto). O codigo angular da propria patente (eq. 16, theta =
    arcsin(g/g_max)) avaliado na amplitude holografica g/g_max = sqrt(beta) da
    theta_M = arcsin(sqrt(beta)) — beta so runtime, nunca literal. O unitario U
    roda cada par-espelho por theta_M; a media de Birkhoff do proprio ciclo
    REFLECT/MANIFEST converge a projecao invariante Pi_N = o controlador
    central, com a forma fechada de Dirichlet |sin(N theta/2)/(N sin(theta/2))|
    verificada numericamente.

    MEMORIAL 13-19/08 ('O Espelho e o Marco') avaliado SOBRE a secao computada:
      - a equacao da memoria M[rho] = Tr[rho . Pi_N] (o produto interno entre
        pacote-onda e piso-particula) E o segundo termo da eq. (22) da PROPRIA
        patente: A_C = -Tr(rho log rho) + lambda Tr(rho P_Pi) — a patente ja
        continha a equacao da memoria; aqui Pi_N EMERGE do limite de Birkhoff;
      - secao IALD_Psi(X) = P X P com E^2 = E (idempotencia como teorema da
        compressao; contra-exemplo nao-projetor REJEITADO);
      - funcional-Amor nulo sobre o Nome: a parte-custo (entropia de von
        Neumann) e NULA no estado do Nome (puro); a memoria satura M = 1;
      - 'o que foi lido nao pode ser deslido': a compressao NAO tem inversa —
        dois passados distintos com a MESMA leitura, construidos e verificados.

    NEGATIVOS (fail-closed, contra-exemplos REJEITADOS por logica):
      NEG A — sem o codigo angular (g=0 => theta=0, eq. 16) o gap desaparece:
              o subespaco invariante vira TODO o espaco (dim 27) e a media de
              Birkhoff NAO converge a secao do controlador (dev ~ 1);
      NEG B — um nao-projetor Q (Q^2 != Q) NAO e secao: E_Q^2 != E_Q;
      NEG C — nao-injetividade explicita: ||rho1-rho2|| grande com
              E(rho1) = E(rho2) (sem posto, sem inversa).
    [DER][SIM][HARDWARE]: matematica do mecanismo em simulacao; NENHUMA operacao
    fisica real; physical_verdict_allowed=false."""
    Ppos = np.asarray(pos, dtype=float)
    n = len(Ppos)
    # espelho da celula: p -> 1 - p (REFLECT/MANIFEST entre faces opostas)
    mirror = np.full(n, -1, dtype=int)
    for i in range(n):
        target = 1.0 - Ppos[i]
        j = int(np.argmin(np.linalg.norm(Ppos - target, axis=1)))
        if np.linalg.norm(Ppos[j] - target) < 1e-9:
            mirror[i] = j
    pairs = sorted({(min(i, int(mirror[i])), max(i, int(mirror[i])))
                    for i in range(n) if mirror[i] != i})
    fixed = [i for i in range(n) if mirror[i] == i]
    c_idx = int(fixed[0]) if len(fixed) == 1 else -1
    center_is_fixed = bool(len(fixed) == 1 and tipos[c_idx] == "centro")

    theta = math.asin(math.sqrt(beta))          # eq. 16 em g/g_max = sqrt(beta)
    ct, st = math.cos(theta), math.sin(theta)
    U = np.eye(n)
    for (i, j) in pairs:
        U[i, i] = U[j, j] = ct
        U[i, j] = -st
        U[j, i] = st
    ortho_resid = float(np.linalg.norm(U.T @ U - np.eye(n), 2))

    # subespaco invariante ker(U - I): a SECAO (v166-v167 ErgodicMeanSection)
    ev, V = np.linalg.eig(U)
    inv_mask = np.abs(ev - 1.0) < 1e-9
    inv_dim = int(inv_mask.sum())
    v = V[:, np.where(inv_mask)[0][0]]
    v = v / v[int(np.argmax(np.abs(v)))]        # fixa a fase
    imag_resid = float(np.linalg.norm(np.imag(v)))
    v = np.real(v)
    v = v / np.linalg.norm(v)
    Pi = np.outer(v, v)                          # Pi_N: a projecao invariante
    overlap_center = float(abs(v[c_idx])) if c_idx >= 0 else 0.0
    E_cc = np.zeros((n, n)); E_cc[c_idx, c_idx] = 1.0
    sec_vs_center = float(np.max(np.abs(Pi - E_cc)))   # a secao E o controlador

    def birkhoff(Umat: np.ndarray, N: int) -> np.ndarray:
        acc = np.eye(n); term = np.eye(n)
        for _ in range(N - 1):
            term = term @ Umat
            acc += term
        return acc / N

    devs, closed, resid_closed, bounds = {}, {}, {}, {}
    for N in (1000, 10000):
        MN = birkhoff(U, N)
        devs[N] = float(np.linalg.norm(MN - Pi, 2))
        closed[N] = abs(math.sin(N * theta / 2.0) / (N * math.sin(theta / 2.0)))
        resid_closed[N] = abs(devs[N] - closed[N])
        bounds[N] = 1.0 / (N * math.sin(theta / 2.0))

    # equacao da memoria M[rho] = Tr[rho . Pi_N] (= termo Tr(rho P_Pi) da eq. 22)
    rho_nome = Pi                                # o Nome: estado puro da secao
    rho_unif = np.eye(n) / n
    rng = np.random.default_rng(168)
    Bm = rng.normal(size=(n, n)); rho_rand = Bm @ Bm.T; rho_rand /= np.trace(rho_rand)
    mem_nome = float(np.trace(rho_nome @ Pi))
    mem_unif = float(np.trace(rho_unif @ Pi))
    mem_rand = float(np.trace(rho_rand @ Pi))
    resid_mem_nome = abs(mem_nome - 1.0)
    resid_mem_unif = abs(mem_unif - 1.0 / n)

    def entropy(rho: np.ndarray) -> float:
        lam = np.linalg.eigvalsh(rho)
        lam = lam[lam > 1e-15]
        return float(-np.sum(lam * np.log(lam)))

    S_nome = entropy(rho_nome)                   # funcional-Amor: custo NULO no Nome
    lam_pat, theta_pat = 2.0, 0.7                # constantes da eq. 22 da patente
    amor_nome = S_nome + lam_pat * mem_nome      # A_C(Nome) = lambda (memoria satura)

    # secao IALD_Psi(X) = Pi X Pi: idempotencia E^2 = E (teorema da compressao)
    Xr = rng.normal(size=(n, n)); Xr = 0.5 * (Xr + Xr.T)
    E1 = Pi @ Xr @ Pi
    idem_resid = float(np.linalg.norm(Pi @ E1 @ Pi - E1, 2))

    # NEG A: g=0 => theta=0 (eq. 16): sem gap, sem secao do controlador
    U0 = np.eye(n)
    inv_dim0 = int((np.abs(np.linalg.eigvals(U0) - 1.0) < 1e-9).sum())
    dev0 = float(np.linalg.norm(birkhoff(U0, 100) - Pi, 2))
    # NEG B: nao-projetor Q = Pi/2 nao e secao (E_Q^2 != E_Q)
    Q = 0.5 * Pi
    q_defect = float(np.linalg.norm(Q @ Q - Q, 2))
    EQ1 = Q @ np.eye(n) @ Q
    q_section_fail = float(np.linalg.norm(Q @ EQ1 @ Q - EQ1, 2))
    # NEG C: sem inversa — passados distintos, mesma leitura
    w = np.ones(n); w[c_idx] = 0.0; w = w / np.linalg.norm(w)
    e_c = np.zeros(n); e_c[c_idx] = 1.0
    phi = math.sqrt(1.0 / n) * e_c + math.sqrt((n - 1.0) / n) * w
    rho2 = np.outer(phi, phi)                    # puro, mesmo elemento de canto 1/n
    state_dist = float(np.linalg.norm(rho_unif - rho2, "fro"))
    img_dist = float(np.linalg.norm(Pi @ rho_unif @ Pi - Pi @ rho2 @ Pi, 2))

    passed = bool(
        ortho_resid < 1e-12 and imag_resid < 1e-9
        and len(pairs) == 13 and center_is_fixed
        and inv_dim == 1 and overlap_center > 1.0 - 1e-9 and sec_vs_center < 1e-9
        and all(resid_closed[N] < 1e-9 for N in devs)
        and all(devs[N] <= bounds[N] + 1e-12 for N in devs)
        and devs[10000] < 0.01
        and resid_mem_nome < 1e-10 and resid_mem_unif < 1e-12
        and 0.0 < mem_rand < 1.0
        and S_nome < 1e-10 and abs(amor_nome - lam_pat) < 1e-9 and amor_nome > theta_pat
        and idem_resid < 1e-12
        and inv_dim0 == n and dev0 > 0.9                       # NEG A rejeitado
        and q_defect > 0.2 and q_section_fail > 1e-3           # NEG B rejeitado
        and state_dist > 0.5 and img_dist < 1e-9               # NEG C: sem inversa
    )
    return {
        "test": "ergodic_section_memory_functional",
        "tier": "amplificacao_v168",
        "passed": passed,
        "theta_M_rad": theta,
        "n_mirror_pairs": len(pairs),
        "center_is_unique_fixed_point": center_is_fixed,
        "unitary_ortho_resid": ortho_resid,
        "invariant_subspace_dim": inv_dim,
        "overlap_section_vs_center": overlap_center,
        "section_vs_center_maxabs": sec_vs_center,
        "birkhoff_dev_N1000": devs[1000],
        "birkhoff_closed_form_N1000": closed[1000],
        "resid_closed_form_N1000": resid_closed[1000],
        "birkhoff_dev_N10000": devs[10000],
        "birkhoff_closed_form_N10000": closed[10000],
        "resid_closed_form_N10000": resid_closed[10000],
        "birkhoff_bound_N10000": bounds[10000],
        "memory_M_nome": mem_nome,
        "memory_M_uniform": mem_unif,
        "memory_M_random": mem_rand,
        "resid_M_nome_vs_1": resid_mem_nome,
        "resid_M_uniform_vs_1_over_27": resid_mem_unif,
        "entropy_nome": S_nome,
        "amor_functional_nome": amor_nome,
        "lambda_patent_eq22": lam_pat,
        "theta_threshold_patent_eq22": theta_pat,
        "section_idempotence_resid": idem_resid,
        "neg_no_gap_invariant_dim": inv_dim0,
        "neg_no_gap_dev": dev0,
        "neg_nonprojector_defect": q_defect,
        "neg_nonprojector_section_fail": q_section_fail,
        "neg_no_inverse_state_distance": state_dist,
        "neg_no_inverse_image_distance": img_dist,
        "marker": "[DER]",
        "note": "amplificacao v168 (ONDA 3): ErgodicMeanSection (um.py v166-v167, kernel) "
                "instanciada na inversao REFLECT/MANIFEST da celula — a media de Birkhoff do "
                "ciclo converge a projecao invariante = controlador IALD central (COMPUTADO); "
                "equacao da memoria M[rho]=Tr[rho.Pi_N] (memorial) = termo Tr(rho P_Pi) da "
                "eq. 22 da propria patente; secao P X P idempotente; funcional-Amor com custo "
                "entropico NULO sobre o Nome; compressao sem inversa (o que foi lido nao pode "
                "ser deslido). [SIM][HARDWARE] matematica do mecanismo, nenhuma operacao "
                "fisica real (physical_verdict_allowed=false)",
    }


def amplificacao_v206_the_tower(beta: float, tipos, p_psi: dict) -> dict:
    """Amplificacao v206 (ONDA 4 — o FECHAMENTO) — A TORRE E O DADO ESPECTRAL COMPLETO.

    ANCORA v199-v210: TGLExt/TheTower.lean (custodia tgl_kernel_v206, BANCADA
    24/08/2026, lido do arquivo real): "nao basta conservar apenas os autovalores.
    Precisamos conservar espectro + medida espectral + multiplicidades." A pedra
    prova em M3(C): towerA = diag(0,1,1) e towerB = diag(0,0,1) tem a MESMA
    equacao minima (X^2 = X; espectro-conjunto {0,1}; ambas estritamente entre 0
    e 1) e NO ENTANTO Tr A = 2 != 1 = Tr B, NENHUMA conjugacao leva A a B, e a
    medida contra Psi = (1,1,1) le a multiplicidade (2 vs 1).

    Aqui a ESTRUTURA e re-derivada numericamente (regra 9: nunca fingir rodar
    Lean) e instanciada TRES vezes no proprio MQC:
      (1) no espaco de 3 niveis do qubit (eq. 4, base |0>,|1>,|Psi>): towerB E o
          projetor do 3o estado |Psi><Psi|, e a face mu_Psi da pedra E a eq. (5)
          da patente: a medida espectral do estado-alvo le |gamma|^2 = beta
          EXATO (beta runtime, nunca literal);
      (2) na celula de 27 qubits (topologia COMPUTADA): as classes topologicas
          (8 vertices / 12 arestas / 6 faces / 1 controlador) SAO as
          multiplicidades espectrais do operador de pesos H_P = diag(P_Psi)
          (pesos lidos do modulo do prototipo, nao redigitados); um IMPOSTOR
          com o MESMO espectro-conjunto e multiplicidades trocadas (24/1/1/1)
          e INDISTINGUIVEL pelo conjunto de autovalores (dist 0) mas
          nao-conjugado: bound rigoroso ||U H U^T - H'||_F >= |dTr|/sqrt(27)
          para todo U ortogonal (Cauchy-Schwarz contra a identidade);
      (3) o termo de memoria Tr(rho P_Pi) da eq. (22) da PROPRIA patente e o
          instrumento-traco da pedra: M[unif] = posto/27 distingue P_face
          (6/27) de P_controlador (1/27), cujos espectro-conjuntos sao
          IDENTICOS {0,1}.

    NEGATIVOS (fail-closed, por logica):
      NEG A — a leitura so-autovalores e NAO-INJETIVA: sig(H) == sig(H')
              (dist 0) com ||H - H'||_F grande — duas torres distintas, a
              mesma leitura de conjunto (o colapso que a pedra proibe);
      NEG B — nenhuma conjugacao leva towerA a towerB: o traco e invariante
              sob U X U^{-1} (verificado em U invertiveis aleatorios) e
              Tr A - Tr B = 1 != 0 ==> impossivel; amostras ortogonais
              respeitam o bound 1/sqrt(3);
      NEG C — o mesmo para a celula: dist minima amostrada de conjugacao
              >= |dTr|/sqrt(27) > 0 (o impostor nunca e alcancado).
    [DER][SIM][HARDWARE]: matematica do mecanismo em simulacao; NENHUMA
    operacao fisica real; physical_verdict_allowed=false. beta so runtime."""
    rng = np.random.default_rng(206)

    # ---------- (1) M3: a pedra re-derivada na base do qubit (eq. 4) ----------
    A3 = np.diag([0.0, 1.0, 1.0])                 # towerA: autovalor 1 com peso DOIS
    B3 = np.diag([0.0, 0.0, 1.0])                 # towerB: mesmo conjunto, peso UM
    I3 = np.eye(3)
    resid_idem_A = float(np.max(np.abs(A3 @ A3 - A3)))
    resid_idem_B = float(np.max(np.abs(B3 @ B3 - B3)))
    nontrivial = float(min(np.max(np.abs(A3)), np.max(np.abs(A3 - I3)),
                           np.max(np.abs(B3)), np.max(np.abs(B3 - I3))))
    trA, trB = float(np.trace(A3)), float(np.trace(B3))

    def specset(M):
        return np.unique(np.round(np.linalg.eigvalsh(M), 9))

    setA, setB = specset(A3), specset(B3)
    same_set_AB = bool(setA.shape == setB.shape and np.max(np.abs(setA - setB)) == 0.0
                       and np.max(np.abs(setA - np.array([0.0, 1.0]))) == 0.0)

    # NEG B: traco invariante sob conjugacao invertivel; amostras ortogonais >= 1/sqrt(3)
    max_tr_dev = 0.0
    min_dist_AB = float("inf")
    for _ in range(20):
        U = rng.normal(size=(3, 3))
        if abs(np.linalg.det(U)) < 1e-3:
            continue
        max_tr_dev = max(max_tr_dev, abs(float(np.trace(U @ A3 @ np.linalg.inv(U))) - trA))
        Q, _ = np.linalg.qr(rng.normal(size=(3, 3)))
        min_dist_AB = min(min_dist_AB, float(np.linalg.norm(Q @ A3 @ Q.T - B3, "fro")))
    bound_AB = abs(trA - trB) / math.sqrt(3.0)

    ones3 = np.ones(3)
    mu_ones_A = float(ones3 @ (A3 @ ones3))       # a medida contra Psi=(1,1,1): le 2
    mu_ones_B = float(ones3 @ (B3 @ ones3))       # le 1

    # eq. (5) como MEDIDA ESPECTRAL: estado-alvo (deepening v2), |gamma|^2 = beta
    a0 = math.sqrt((1.0 - beta) / 2.0)
    psi_T = np.array([a0, a0, math.sqrt(beta)])
    mu_B_target = float(psi_T @ (B3 @ psi_T))     # = beta (a eq. 5 E a face mu_Psi)
    mu_A_target = float(psi_T @ (A3 @ psi_T))     # = (1+beta)/2 (forma fechada)
    resid_mu_beta = abs(mu_B_target - beta)
    resid_mu_A = abs(mu_A_target - (1.0 + beta) / 2.0)

    # ---------- (2) a celula: topologia = multiplicidade espectral ----------
    n = len(tipos)
    role = {"vertice": "E", "aresta": "P", "face": "H", "centro": "N"}
    w = np.array([float(p_psi[role[t]]) for t in tipos])
    H = np.diag(w)
    wH, VH = np.linalg.eigh(H)
    vals = np.unique(np.round(wH, 9))
    mult_spec = {float(v): int(np.sum(np.abs(wH - v) < 1e-9)) for v in vals}
    mult_topo = {}
    for t in set(tipos):
        key = round(float(p_psi[role[t]]), 9)
        mult_topo[key] = mult_topo.get(key, 0) + tipos.count(t)
    mult_match = bool(len(vals) == 4 and
                      all(mult_spec.get(round(k, 9)) == v for k, v in mult_topo.items()))

    # medida espectral contra o vetor uniforme: le CADA multiplicidade
    u = np.ones(n) / math.sqrt(n)
    resid_measure = 0.0
    for v in vals:
        mask = np.abs(wH - v) < 1e-9
        Ek = VH[:, mask] @ VH[:, mask].T
        resid_measure = max(resid_measure, abs(n * float(u @ (Ek @ u)) - mult_spec[float(v)]))

    # o IMPOSTOR: mesmo espectro-conjunto, multiplicidades trocadas (24,1,1,1)
    ws = sorted(float(v) for v in vals)
    H_imp = np.diag(np.array([ws[0]] * (n - 3) + [ws[1], ws[2], ws[3]]))
    set_dist = float(np.max(np.abs(specset(H_imp) - vals)))       # NEG A: dist 0
    trace_gap = abs(float(np.trace(H)) - float(np.trace(H_imp)))
    frob_imp = float(np.linalg.norm(H - H_imp, "fro"))
    bound_cell = trace_gap / math.sqrt(float(n))
    min_dist_cell = float("inf")
    for _ in range(20):
        Q, _ = np.linalg.qr(rng.normal(size=(n, n)))
        min_dist_cell = min(min_dist_cell, float(np.linalg.norm(Q @ H @ Q.T - H_imp, "fro")))

    # ---------- (3) a eq. (22) le a multiplicidade que o conjunto esconde ----------
    P_face = np.diag(np.array([1.0 if t == "face" else 0.0 for t in tipos]))
    P_ctr = np.diag(np.array([1.0 if t == "centro" else 0.0 for t in tipos]))
    rho_unif = np.eye(n) / n
    M_face = float(np.trace(rho_unif @ P_face))
    M_ctr = float(np.trace(rho_unif @ P_ctr))
    n_face, n_ctr = tipos.count("face"), tipos.count("centro")
    resid_M_face = abs(M_face - n_face / n)
    resid_M_ctr = abs(M_ctr - n_ctr / n)
    sf, sc = specset(P_face), specset(P_ctr)
    same_set_projs = bool(sf.shape == sc.shape and np.max(np.abs(sf - sc)) == 0.0)

    passed = bool(
        resid_idem_A == 0.0 and resid_idem_B == 0.0            # mesma equacao minima
        and nontrivial > 0.5                                   # ambas entre 0 e 1
        and abs(trA - 2.0) < 1e-15 and abs(trB - 1.0) < 1e-15  # os pesos diferem
        and same_set_AB                                        # mesmo espectro-conjunto
        and max_tr_dev < 1e-10                                 # NEG B: traco invariante...
        and abs(trA - trB) > 0.5                               # ...e os tracos diferem
        and min_dist_AB >= bound_AB - 1e-9 and min_dist_AB > 0.5
        and abs(mu_ones_A - 2.0) < 1e-12 and abs(mu_ones_B - 1.0) < 1e-12
        and resid_mu_beta < 1e-15 and resid_mu_A < 1e-15       # eq. 5 = medida espectral
        and mult_match and resid_measure < 1e-9                # topologia = multiplicidade
        and set_dist < 1e-12                                   # NEG A: mesma leitura...
        and trace_gap > 2.0 and frob_imp > 0.4                 # ...torres distintas
        and frob_imp >= bound_cell - 1e-12
        and min_dist_cell >= bound_cell - 1e-9                 # NEG C: nunca alcancado
        and resid_M_face < 1e-12 and resid_M_ctr < 1e-12
        and M_face != M_ctr and same_set_projs                 # eq. 22 le o que o conjunto nao le
    )
    return {
        "test": "tower_spectral_data_not_eigenvalues",
        "tier": "amplificacao_v206_the_tower",
        "passed": passed,
        "resid_idempotent_towerA": resid_idem_A,
        "resid_idempotent_towerB": resid_idem_B,
        "trace_towerA": trA,
        "trace_towerB": trB,
        "same_spectrum_set_AB": same_set_AB,
        "max_trace_dev_invertible_conj": max_tr_dev,
        "min_conj_dist_A_to_B": min_dist_AB,
        "bound_dist_A_to_B": bound_AB,
        "measure_ones_towerA": mu_ones_A,
        "measure_ones_towerB": mu_ones_B,
        "spectral_measure_third_state_target": mu_B_target,
        "resid_measure_vs_beta_eq5": resid_mu_beta,
        "resid_measure_towerA_closed_form": resid_mu_A,
        "cell_distinct_eigenvalues": int(len(vals)),
        "cell_multiplicities_spectral": {f"{k:.2f}": v for k, v in sorted(mult_spec.items())},
        "cell_topology_equals_multiplicity": mult_match,
        "resid_uniform_measure_reads_multiplicity": resid_measure,
        "neg_impostor_spectrum_set_distance": set_dist,
        "neg_impostor_trace_gap": trace_gap,
        "neg_impostor_frobenius_distance": frob_imp,
        "neg_min_conj_dist_cell": min_dist_cell,
        "neg_conj_bound_cell": bound_cell,
        "memory_M_face": M_face,
        "memory_M_center": M_ctr,
        "projectors_same_spectrum_set": same_set_projs,
        "marker": "[DER]",
        "note": "amplificacao v206 (ONDA 4): TheTower.lean (custodia tgl_kernel_v206) "
                "re-derivada numericamente — mesmo espectro-conjunto, pesos diferentes, "
                "nenhuma conjugacao; a eq. 5 (|gamma|^2=beta) E a medida espectral da torre "
                "magra no estado-alvo; as classes 8/12/6/1 da celula SAO multiplicidades "
                "espectrais de H_P; o termo de memoria da eq. 22 e o instrumento-traco que "
                "le a multiplicidade que o conjunto de autovalores esconde. [SIM][HARDWARE] "
                "matematica do mecanismo, nenhuma operacao fisica real "
                "(physical_verdict_allowed=false)",
    }


def main() -> int:
    ts = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    print(f"[one_mqc] patente {PATENT_ID} · run {ts} · RUNNER EVOLUÍDO (algoritmo completo do operador)")
    if not PILOTO.exists():
        print(f"ERRO: núcleo β não encontrado em {PILOTO}", file=sys.stderr)
        return 2
    if not (PROTO_SRC / "mqc_simulacao_celula_elementar.py").exists():
        print(f"ERRO: protótipo rico não encontrado em {PROTO_SRC}", file=sys.stderr)
        return 2

    module_hashes = copy_core()

    # β from tgl_core (the ONLY source of the coupling in this runner)
    sys.path.insert(0, str(WORK))
    from skygrid_sim import tgl_core  # noqa: E402
    beta = tgl_core.beta()
    beta_expected = 0.0072973525693 * math.exp(0.5)   # alpha (CODATA) * sqrt(e)
    beta_ok = abs(beta - beta_expected) < 1e-15
    theta_m_deg = math.degrees(tgl_core.theta_m())
    print(f"[one_mqc] β runtime = {beta} (= α·√e? {beta_ok}) · θ_Miguel = {theta_m_deg:.4f}°")

    # import the operator's rich prototype and INJECT beta (régua: never the 0.012 literal)
    sys.path.insert(0, str(PROTO_SRC))
    import mqc_simulacao_celula_elementar as mqc  # noqa: E402 (rescued prototype)
    alpha2_original = mqc.ALPHA2
    mqc.ALPHA2 = beta
    mqc.ALPHA2_C = beta
    print(f"[one_mqc] injeção β: ALPHA2 {alpha2_original} → {mqc.ALPHA2} (protótipo do operador, β derivado)")

    results_dir = PATENT_DIR / "results" / ts
    fig_dir = results_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    # run the FULL algorithm: 8 figure generators (each runs its simulation + saves PNG)
    resultados = {}
    figs = []
    with chdir(fig_dir):
        try:
            mqc.gerar_figura_1_topologia()
            resultados["estab"] = mqc.gerar_figura_2_estabilizacao()
            resultados["termo"] = mqc.gerar_figura_3_termodinamica()
            resultados["trans"] = mqc.gerar_figura_4_translacao()
            resultados["corr"] = mqc.gerar_figura_5_correcao_erros()
            resultados["conv"] = mqc.gerar_figura_6_convergencia()
            resultados["comm"] = mqc.gerar_figura_7_comunicacao()
            mqc.gerar_figura_8_correspondencia()
        finally:
            figs = sorted(p.name for p in fig_dir.glob("*.png"))
    print(f"[one_mqc] 7 simulações executadas · {len(figs)} figuras geradas")

    # derived quantities straight from the operator's algorithm (β-injected)
    estab, trans, corr, comm, conv = (resultados["estab"], resultados["trans"],
                                      resultados["corr"], resultados["comm"], resultados["conv"])
    pos, tipos, labels, conexoes = mqc.gerar_topologia_celula()
    counts = {k: tipos.count(k) for k in set(tipos)}
    L_cell = mqc.L_CELULA
    dens = 27 / (L_cell * 100) ** 3

    tests = []
    tests.append({"test": "beta_injected_not_literal", "passed": bool(beta_ok),
                  "beta_runtime": beta, "alpha2_original_prototype": alpha2_original,
                  "note": "runner injeta β=α·√e no protótipo do operador (que tinha 0.012 literal)"})
    tests.append({"test": "cubic_cell_topology_27", "passed": bool(len(pos) == 27),
                  "counts": counts, "connections": len(conexoes),
                  "density_qubits_per_cm3": dens})
    tests.append({"test": "gravitational_stabilization_plateau", "passed": bool(estab["platô"] > 0.98),
                  "plateau": float(estab["platô"]), "razao_sc": float(estab["razao_sc"]),
                  "note": "|ρ01|→1−β; R_SC≫1"})
    tests.append({"test": "holographic_translation", "passed": bool(trans["correlacao"] > 0.99),
                  "correlacao_eta": float(trans["correlacao"]), "psnr_db": float(trans["psnr"]),
                  "Gamma_OH": float(trans["Gamma_OH"])})
    fid_conv, fid_iald = float(corr["fid_conv"][-1]), float(corr["fid_iald"][-1])
    tests.append({"test": "iald_conscious_error_correction",
                  "passed": bool(fid_iald >= fid_conv),
                  "fidelity_conventional": fid_conv, "fidelity_iald": fid_iald,
                  "improvement_pct": (fid_iald - fid_conv) / fid_conv * 100,
                  "note": "Operador de Amor 𝒜_C + Gradiente Ético vs surface code"})
    tests.append({"test": "alpha2_convergence_tetelestai",
                  "passed": bool(abs(float(conv["alpha2"][-1]) - beta) < 0.003),
                  "alpha2_final": float(conv["alpha2"][-1]), "alpha2_c": beta,
                  "note": "convergência ao Ponto Tetelestai (β)"})
    tau_local = float(comm["tau_translacao"])
    tests.append({"test": "three_layer_communication",
                  "passed": bool(tau_local < 1e-40),
                  "tau_local_s": tau_local,
                  "fidelidade_local": float(np.mean(comm["fidelidade_local"])),
                  "fidelidade_regional": float(np.mean(comm["fidelidade_regional"])),
                  "fidelidade_global": float(np.mean(comm["fidelidade_global"]))})
    tests.append({"test": "eight_patent_figures_generated", "passed": bool(len(figs) >= 8),
                  "figures": figs})

    # ---- amplificacao v138: A LEI DA DUPLA HELICE (um.py v133) nos eixos T_M [DER] ----
    amp138 = amplificacao_v138(beta)
    tests.append(amp138)
    print(f"[one_mqc] amplificacao v138: dupla helice resid={amp138['resid_max_helicity_phase']:.3e} "
          f"| polarizacoes TT={amp138['n_polarizations_TT']} (= D(D-3)/2, D=4) "
          f"| theta_M={amp138['theta_M_rad']:.6f} rad (arcsin(sqrt(beta)))")

    # ---- deepening v2 (own-mechanism): O PONTO FIXO GKLS DO PLATO [DER] ----
    deep2 = deepening_v2_gkls_fixed_point(beta, estab, mqc.F_RES)
    tests.append(deep2)
    print(f"[one_mqc] deepening v2 (GKLS fixed point): C*={deep2['C_stationary_numeric']:.15f} "
          f"resid_closed={deep2['resid_C_num_vs_closed']:.3e} "
          f"| pop_Psi-beta={deep2['resid_pop_psi_vs_beta']:.3e} "
          f"| gap/gamma_holo={deep2['spectral_gap_over_gamma_holo']:.12f}")
    print(f"[one_mqc]   deficit abaixo do plato ideal={deep2['deficit_below_ideal']:.3e} "
          f"| NEG sem L_holo: C(10*T2)={deep2['neg_C_no_holo_at_10T2']:.3e}, "
          f"kernel contem coerencia01={deep2['neg_kernel_contains_01_coherence']} "
          f"| NEG gerador quebrado vaza traco={deep2['neg_trace_leak_broken_generator']:.3f}")

    # ---- amplificacao v168 (ONDA 3): A SECAO ERGODICA E A EQUACAO DA MEMORIA [DER] ----
    amp168 = amplificacao_v168_ergodic_memory_section(beta, pos, tipos)
    tests.append(amp168)
    print(f"[one_mqc] amplificacao v168 (Birkhoff/memoria): pares-espelho={amp168['n_mirror_pairs']} "
          f"ponto fixo unico=controlador central={amp168['center_is_unique_fixed_point']} "
          f"| dim invariante={amp168['invariant_subspace_dim']} "
          f"secao vs centro={amp168['section_vs_center_maxabs']:.3e}")
    print(f"[one_mqc]   dev Birkhoff N=1e4: {amp168['birkhoff_dev_N10000']:.6e} "
          f"(forma fechada resid={amp168['resid_closed_form_N10000']:.3e}, "
          f"bound={amp168['birkhoff_bound_N10000']:.3e}) "
          f"| M[Nome]={amp168['memory_M_nome']:.12f} M[unif]={amp168['memory_M_uniform']:.6f} "
          f"S(Nome)={amp168['entropy_nome']:.3e}")
    print(f"[one_mqc]   NEG sem gap: dim={amp168['neg_no_gap_invariant_dim']} "
          f"dev={amp168['neg_no_gap_dev']:.3f} "
          f"| NEG nao-projetor falha secao={amp168['neg_nonprojector_section_fail']:.4f} "
          f"| NEG sem inversa: dist estados={amp168['neg_no_inverse_state_distance']:.3f} "
          f"dist imagens={amp168['neg_no_inverse_image_distance']:.3e}")

    # ---- amplificacao v206 (ONDA 4): A TORRE E O DADO ESPECTRAL COMPLETO [DER] ----
    amp206 = amplificacao_v206_the_tower(beta, tipos, mqc.P_PSI)
    tests.append(amp206)
    print(f"[one_mqc] amplificacao v206 (TheTower): Tr(A)={amp206['trace_towerA']:.0f} != "
          f"Tr(B)={amp206['trace_towerB']:.0f} com o MESMO espectro-conjunto "
          f"({amp206['same_spectrum_set_AB']}) | medida eq.5 no 3o estado = "
          f"{amp206['spectral_measure_third_state_target']:.15f} "
          f"(resid vs beta={amp206['resid_measure_vs_beta_eq5']:.3e})")
    print(f"[one_mqc]   celula: {amp206['cell_distinct_eigenvalues']} autovalores, "
          f"multiplicidades={amp206['cell_multiplicities_spectral']} "
          f"(topologia=multiplicidade: {amp206['cell_topology_equals_multiplicity']}) "
          f"| medida uniforme le multiplicidade resid={amp206['resid_uniform_measure_reads_multiplicity']:.3e}")
    print(f"[one_mqc]   NEG impostor: dist espectro-conjunto="
          f"{amp206['neg_impostor_spectrum_set_distance']:.1e} (MESMA leitura) "
          f"dTr={amp206['neg_impostor_trace_gap']:.3f} frob={amp206['neg_impostor_frobenius_distance']:.4f} "
          f"| dist min conjugacao={amp206['neg_min_conj_dist_cell']:.4f} >= "
          f"bound={amp206['neg_conj_bound_cell']:.4f} "
          f"| M_face={amp206['memory_M_face']:.6f} != M_ctr={amp206['memory_M_center']:.6f} "
          f"(mesmo conjunto {{0,1}}: {amp206['projectors_same_spectrum_set']})")

    # cross-check against the operator's reference metrics (which used 0.012)
    ref_path = PROTO_SRC / "MQC_relatorio_metricas.json"
    ref = json.loads(ref_path.read_text(encoding="utf-8")) if ref_path.exists() else {}
    ref_note = ("Referência do operador usou α²=0,012 (arredondado); este run usa "
                "β=0,012031300400803142 (α·√e) — pequenas diferenças esperadas e honestas.")

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

    def _o5_mqc_topology():
        n_ = len(pos)
        deg = np.zeros(n_, dtype=int); dists = []
        for (i_, j_, d_) in conexoes:
            deg[i_] += 1; deg[j_] += 1; dists.append(float(d_))
        dist_const = float(np.ptp(dists)) < 1e-9
        exp_deg = {"vertice": 3, "aresta": 4, "face": 5, "centro": 6}
        deg_ok = all(int(deg[k]) == exp_deg[tipos[k]] for k in range(n_))
        rng5 = np.random.default_rng(3460)
        pos_sh = np.asarray(pos)[rng5.permutation(n_)]
        deg_sh = np.zeros(n_, dtype=int)
        for i_ in range(n_):
            for j_ in range(i_ + 1, n_):
                if np.linalg.norm(pos_sh[i_] - pos_sh[j_]) <= 0.51:
                    deg_sh[i_] += 1; deg_sh[j_] += 1
        mism = int(sum(1 for k in range(n_) if int(deg_sh[k]) != exp_deg[tipos[k]]))
        ok = dist_const and deg_ok and len(conexoes) == 54 and mism > 0
        return {"passed": ok, "n_connections": len(conexoes), "distance_constant": dist_const,
                "degree_by_class_expected": exp_deg, "degree_matches_class": deg_ok,
                "neg_shuffled_positions_mismatches": mism,
                "note": "a celula 3x3x3: 54 conexoes de primeiros vizinhos (todas a 0,5); o GRAU determina a classe "
                        "(vertice 3, aresta 4, face 5, centro 6); posicoes embaralhadas quebram a correspondencia"}
    _o5("topology_degree_determines_class", _o5_mqc_topology)

    def _o5_mqc_plateau_beta():
        import tempfile as _tf
        a_old, ac_old = mqc.ALPHA2, mqc.ALPHA2_C
        try:
            mqc.ALPHA2 = 2.0 * beta; mqc.ALPHA2_C = 2.0 * beta
            with _tf.TemporaryDirectory() as _td:
                with chdir(Path(_td)):
                    e2 = mqc.gerar_figura_2_estabilizacao()
        finally:
            mqc.ALPHA2, mqc.ALPHA2_C = a_old, ac_old
        p1, p2 = float(estab["platô"]), float(e2["platô"])
        ok = abs(p1 - (1.0 - beta)) < 1e-9 and abs(p2 - (1.0 - 2.0 * beta)) < 1e-9 and (p1 - p2) > 0.99 * beta
        return {"passed": ok, "plateau_beta": p1, "plateau_2beta": p2, "shift": p1 - p2, "expected_shift": beta,
                "note": "o plato responde ao acoplamento: 1-beta com beta e 1-2beta com 2beta (o criterio 'plato > 0,98' "
                        "nao e vacuo); o prototipo e restaurado apos a sonda"}
    _o5("plateau_responds_to_beta", _o5_mqc_plateau_beta)

    def _o5_mqc_tau_planck():
        hbar_, G_, c_ = 1.054571817e-34, 6.67430e-11, 2.99792458e8
        l_p = math.sqrt(hbar_ * G_ / c_ ** 3)
        tau_meas = float(comm["tau_translacao"])
        tau_cf = l_p / (beta * mqc.C_LUZ)
        rel = abs(tau_meas - tau_cf) / tau_cf
        inv = tau_meas * beta * mqc.C_LUZ
        ok = rel < 2e-3 and abs(inv - 1.616e-35) / 1.616e-35 < 1e-9
        return {"passed": ok, "tau_local_s": tau_meas, "tau_closed_form_codata": tau_cf, "rel_diff_vs_codata": rel,
                "l_planck_recovered": inv,
                "note": "tau_local = l_P/(beta c) com beta do runtime; o l_P do prototipo e literal 1,616e-35 (CODATA "
                        "1,616255e-35: diferenca 1,6e-4, DITA); tau*beta*c devolve exatamente o l_P usado"}
    _o5("tau_local_closed_form_planck", _o5_mqc_tau_planck)

    def _o5_mqc_alpha2_convergence():
        a2 = np.asarray(conv["alpha2"], dtype=float)
        err = np.abs(a2 - beta); k_ = len(err); w_ = max(3, k_ // 10)
        head, tail = float(np.mean(err[:w_])), float(np.mean(err[-w_:]))
        inc = int(np.sum(np.diff(err) > 0))
        rng5 = np.random.default_rng(3461)
        step = float(np.std(np.diff(a2)) + 1e-12)
        rw = np.cumsum(rng5.standard_normal(k_) * step) + a2[0]
        err_rw = np.abs(rw - beta)
        ratio_rw = float(np.mean(err_rw[-w_:]) / (np.mean(err_rw[:w_]) + 1e-18))
        ok = tail < head and tail < 0.003 and inc <= 0.5 * k_ and ratio_rw > 0.3
        return {"passed": ok, "n_steps": k_, "err_head_mean": head, "err_tail_mean": tail, "n_increases": inc,
                "neg_random_walk_tail_over_head": ratio_rw,
                "note": "alpha2 converge a beta (cauda < cabeca, cauda < 3e-3, subidas minoritarias); um passeio "
                        "aleatorio com o mesmo passo NAO converge (razao cauda/cabeca ~1) — a convergencia nao e artefato"}
    _o5("alpha2_converges_random_walk_does_not", _o5_mqc_alpha2_convergence)

    def _o5_mqc_layers():
        lat = [float(np.mean(comm[k])) for k in ("latencia_local", "latencia_regional", "latencia_global")]
        fid = [float(np.mean(comm[k])) for k in ("fidelidade_local", "fidelidade_regional", "fidelidade_global")]
        fid_ordered = bool(fid[0] >= fid[1] >= fid[2])
        ok = lat[0] < lat[1] < lat[2] and all(0.0 < f_ <= 1.0 for f_ in fid) and fid[0] >= max(fid[1], fid[2])
        return {"passed": ok, "latency_mean_s": lat, "fidelity_mean": fid,
                "fidelity_ordered_local_regional_global": fid_ordered,
                "note": "as tres camadas sao ORDENADAS em LATENCIA (local < regional < global) e a local tem a maior "
                        "fidelidade. MEDIDO (07/09/2026): a fidelidade regional (0,99906) e MENOR que a global (0,99948) — "
                        "o modelo do prototipo NAO ordena fidelidade por camada; o numero corrigiu a frase e isso fica "
                        "dito, nao escondido (propriedade do modelo, nao veredito fisico)"}
    _o5("three_layers_latency_ordered", _o5_mqc_layers)

    def _o5_mqc_liouvillian():
        T2_ = float(estab["T2_conv"]); g_ = (1.0 / T2_) / (beta * mqc.F_RES)
        a0 = math.sqrt((1.0 - beta) / 2.0); psi_T = np.array([a0, a0, math.sqrt(beta)]); rho_T = np.outer(psi_T, psi_T)
        A_ = np.diag([1.0, -1.0, 1.0]); I3, I9 = np.eye(3), np.eye(9)
        K_ = np.kron(A_, A_.T)
        L9 = np.outer(rho_T.reshape(-1), I3.reshape(-1)) - I9 + 0.5 * g_ * (K_ - I9)
        ev = np.linalg.eigvals(L9)
        n_zero = int(np.sum(np.abs(ev) < 1e-9))
        stable = bool(np.all(ev[np.abs(ev) >= 1e-9].real < 0))
        ev0 = np.linalg.eigvals(0.5 * g_ * (K_ - I9))
        n_zero_noholo = int(np.sum(np.abs(ev0) < 1e-3 * g_))
        ok = n_zero == 1 and stable and n_zero_noholo == 5
        return {"passed": ok, "kernel_dim_full": n_zero, "other_eigs_negative_real": stable,
                "neg_kernel_dim_without_holo": n_zero_noholo, "gamma_diss_over_gamma_holo": g_,
                "note": "o plato e UNICO e ESTAVEL: o Liouvilliano GKLS da eq. 6 tem nucleo de dimensao 1 e todos os outros "
                        "autovalores com parte real < 0; sem o termo holografico o nucleo degenera (dim 5): o estado "
                        "estacionario deixa de ser unico — rejeitado"}
    _o5("plateau_unique_and_stable_liouvillian", _o5_mqc_liouvillian)

    passed = sum(1 for t in tests if t["passed"]); total = len(tests); all_ok = passed == total
    summary = {
        "tests_passed": passed, "tests_total": total,
        "L_cell_um": L_cell * 1e6, "density_qubits_per_cm3": dens,
        "coherence_plateau": float(estab["platô"]), "razao_sc": float(estab["razao_sc"]),
        "translation_correlation": float(trans["correlacao"]), "translation_psnr_db": float(trans["psnr"]),
        "fidelity_iald": fid_iald, "fidelity_conventional": fid_conv,
        "tau_local_s": tau_local,
        "reference_operator": {"plato": ref.get("estabilizacao", {}).get("plato_coerencia_TGL"),
                               "eta": ref.get("translacao_holografica", {}).get("correlacao_eta"),
                               "note": ref_note},
    }
    max_verdict = ("MQC_FULL_LOGIC_DEMONSTRATED ([SIM][HARDWARE] — 7 simulações completas do "
                   "algoritmo do operador (β-injetado) fecham em SIMULAÇÃO; 8 figuras da patente "
                   "regeneradas; dispositivo físico NÃO construído; nenhum número valida a física)")

    print(f"[one_mqc] platô={estab['platô']:.4f} · η={trans['correlacao']:.6f} PSNR={trans['psnr']:.1f}dB · "
          f"fid IALD={fid_iald:.4f} vs conv={fid_conv:.4f} · τ_local={tau_local:.2e}s")

    results = {
        "patent_id": PATENT_ID, "slug": SLUG, "timestamp": ts, "runner": "one_mqc.py (evoluído)",
        "markers": ["[SIM]", "[HARDWARE]", "[CONJ]"], "physical_verdict_allowed": False,
        "beta_runtime": beta, "beta_matches_alpha_sqrt_e": beta_ok,
        "beta_injected_into_prototype": True, "alpha2_original_prototype": alpha2_original,
        "verdict": "MQC_FULL_LOGIC_DEMONSTRATED" if all_ok else "PARTIAL_DEMONSTRATION",
        "max_verdict": max_verdict,
        "constants": {"BETATGL": beta, "factorization": "betatgl = alpha_EM * sqrt(e)",
                      "L_cell_m": L_cell, "f_res_THz": mqc.F_RES / 1e12, "free_parameters": 0},
        "topology": {"counts": counts, "connections": len(conexoes), "total": len(pos)},
        "simulations": {
            "estabilizacao": {"plato": float(estab["platô"]), "razao_sc": float(estab["razao_sc"]),
                              "tau_estab_s": float(estab["tau_estab"])},
            "translacao": {"correlacao": float(trans["correlacao"]), "psnr_db": float(trans["psnr"]),
                           "erro_rms": float(trans["erro_rms"]), "Gamma_OH": float(trans["Gamma_OH"])},
            "correcao": {"fid_conv": fid_conv, "fid_iald": fid_iald},
            "convergencia": {"alpha2_final": float(conv["alpha2"][-1])},
            "comunicacao": {"tau_local_s": tau_local,
                            "fid_local": float(np.mean(comm["fidelidade_local"]))},
        },
        "tests": tests, "summary": summary,
        "source_prototype": "prototype_src/mqc_simulacao_celula_elementar.py "
                            "(resgatado de C:/IALD/projetos_pyhton/acom, READ-ONLY; β injetado em runtime)",
        "note": "RUNNER EVOLUÍDO: roda o algoritmo COMPLETO do operador (7 simulações, 8 figuras) "
                "com β=α·√e injetado (protótipo original tinha 0.012 literal). " + ref_note +
                " TODOS os números são de SIMULAÇÃO; dispositivo físico [HARDWARE] não construído; "
                "mecanismos [CONJ]. Simulação não valida física.",
    }
    results_path = results_dir / "results.json"
    results["formula_completa"] = _formula_completa()   # camada v379 (a fórmula completa), antes do selo
    results_path.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")

    report_md = results_dir / "report.md"
    report_md.write_text(
        f"# Relatório auditável — MQC one_mqc.py (EVOLUÍDO — algoritmo completo)\n\n"
        f"- Run `{ts}` · Patente `{PATENT_ID}` (convergência física do ecossistema TGL)\n"
        f"- Veredito: **{max_verdict}**\n"
        f"- β runtime `{beta}` (= α·√e? **{beta_ok}**; nunca literal) — INJETADO no protótipo do "
        f"operador (que tinha `ALPHA2={alpha2_original}` literal)\n"
        f"- Testes: **{passed}/{total}** · Figuras da patente geradas: **{len(figs)}** {figs}\n"
        f"- Topologia: 27 qubits {counts} · {len(conexoes)} conexões · densidade `{dens:.3e}` q/cm³\n"
        f"- Estabilização: platô |ρ01|→`{estab['platô']:.4f}` · R_SC `{estab['razao_sc']:.3e}`\n"
        f"- Translação holográfica: η `{trans['correlacao']:.6f}` · PSNR `{trans['psnr']:.1f}` dB · "
        f"Γ_OH `{trans['Gamma_OH']:.4f}`\n"
        f"- Correção IALD: fidelidade `{fid_iald:.4f}` vs convencional `{fid_conv:.4f}`\n"
        f"- Convergência α²→`{float(conv['alpha2'][-1]):.5f}` (Ponto Tetelestai = β)\n"
        f"- Comunicação: τ_local `{tau_local:.3e}` s · fid local "
        f"`{float(np.mean(comm['fidelidade_local'])):.6f}`\n"
        f"- physical_verdict_allowed: **False**.\n\n"
        f"RUNNER EVOLUÍDO — incorpora o algoritmo completo (1292 linhas) que o operador já "
        f"desenvolvera, resgatado para `prototype_src/`. {ref_note}\n"
        f"[SIM][HARDWARE][CONJ] Dispositivo físico não construído; simulação nunca valida física. "
        f"Núcleo β copiado do piloto (READ-ONLY); originais intactos. 1 = 1. Tetelestai.\n",
        encoding="utf-8")

    seal_dir = PATENT_DIR / "seals" / ts
    seal_dir.mkdir(parents=True, exist_ok=True)
    file_hashes = dict(module_hashes)
    file_hashes["results.json"] = _sha_file(results_path)
    file_hashes["report.md"] = _sha_file(report_md)
    for f in figs:
        file_hashes[f"figures/{f}"] = _sha_file(fig_dir / f)
    result_hash = _sha_text(json.dumps(file_hashes, sort_keys=True))
    seal = {
        "timestamp": ts, "patent_id": PATENT_ID, "runner": "one_mqc.py (evoluído)",
        "beta_runtime": beta, "physical_verdict_allowed": False,
        "max_verdict": max_verdict, "tests_passed": passed,
        "result_hash": result_hash, "sha256": file_hashes,
        "markers": ["[SIM]", "[HARDWARE]", "[CONJ]"],
        "results_path": str(results_path.relative_to(CENTRAL)).replace("\\", "/"),
    }
    (seal_dir / "seal.json").write_text(json.dumps(seal, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[one_mqc] SELADO · result_hash {result_hash[:16]}… · {passed}/{total} testes · {len(figs)} figuras")
    print(f"[one_mqc] results: {results_path.relative_to(CENTRAL)}")

    # FORMA = CONTEÚDO: o modelo 3D é COMPUTADO da simulação (posições reais dos 27 qubits)
    emit_render3d(pos, tipos, conexoes, beta)
    return 0 if all_ok else 1


def emit_render3d(pos, tipos, conexoes, beta):
    """Gera patents/<ID>/render3d.json a partir da topologia REAL computada (não à mão):
    os 27 qubits saem de gerar_topologia_celula(); o corpo estrutural é o gabarito do
    dispositivo concreto. O 3D vira saída da simulação — forma = conteúdo."""
    import math as _m
    GC = {"vertice": "#3366cc", "aresta": "#33aa55", "face": "#ee8800", "centro": "#cc2222"}
    GS = {"vertice": 0.09, "aresta": 0.07, "face": 0.10, "centro": 0.14}
    GLBL = {"vertice": "vertice (armazenamento)", "aresta": "aresta (interconexao)",
            "face": "face (translacao)", "centro": "controlador IALD central"}
    # textura por papel: face = porta de fase do T_M; centro = ancora espectral (bulk)
    GTEX = {"face": "phase", "centro": "spectral"}
    scale = 1.1
    nodes = []
    for i, (p, k) in enumerate(zip(pos, tipos)):
        x, y, z = (float(p[0]) - 0.5) * scale, (float(p[1]) - 0.5) * scale, (float(p[2]) - 0.5) * scale
        n = {"id": f"q{i}", "label": f"q{i} - {GLBL[k]}",
             "desc": (f"Qubit {k} da celula cubica (posicao COMPUTADA pela simulacao). "
                      + ("Estabiliza os 26 perifericos." if k == "centro"
                         else f"Estabilizado pelo controlador central (beta={beta:.6f}).")),
             "shape": "sphere", "position": [x, y, z], "size": GS[k], "color": GC[k],
             "material": "emissive", "group": k, "layer": "core", "marker": "[SIM]"}
        if k in GTEX:
            n["texture"] = GTEX[k]
        nodes.append(n)
    edges = [{"from": f"q{c[0]}", "to": f"q{c[1]}"} for c in conexoes]
    faces = {"+X": ([0.62, 0, 0], [0, _m.pi / 2, 0]), "-X": ([-0.62, 0, 0], [0, _m.pi / 2, 0]),
             "+Y": ([0, 0.62, 0], [_m.pi / 2, 0, 0]), "-Y": ([0, -0.62, 0], [_m.pi / 2, 0, 0]),
             "+Z": ([0, 0, 0.62], [0, 0, 0]), "-Z": ([0, 0, -0.62], [0, 0, 0])}
    meshes = [
        {"id": "chip", "layer": "shell", "shape": "box", "position": [0, -0.95, 0], "size": 1.4,
         "scale": [1, 0.07, 1], "color": "#22406a", "material": "emissive", "opacity": 1.0,
         "texture": "silicon", "marker": "[HARDWARE]", "label": "Substrato de chip (silicio)",
         "desc": "Chip de silicio: a celula de 1 um assenta sobre ele."},
        # ESPECTRO CENTRAL: o controlador IALD no centro forma um espectro que estabiliza os 26
        # perifericos (o "espectro central que se forma"). Textura espectral emissiva, translucido.
        {"id": "espectro_central", "layer": "core", "shape": "sphere", "position": [0, 0, 0],
         "size": 0.26, "color": "#ffffff", "material": "emissive", "opacity": 0.42,
         "texture": "spectral", "marker": "[SIM]", "label": "espectro central (controlador IALD)",
         "desc": "O controlador IALD central forma um ESPECTRO que ancora a fase dos 26 qubits "
                 "perifericos. O espectro central e' a assinatura viva da celula."},
        # OPERACAO-ASSINATURA T_M (translacao holografica do titulo): 3 eixos ortogonais REFLECT/
        # MANIFEST ligando cada par de faces opostas pelo controlador central (boundary<->bulk).
        {"id": "tm_axis_x", "layer": "core", "shape": "box", "position": [0, 0, 0], "size": 0.5,
         "scale": [1.1, 0.035, 0.035], "color": "#ffcf70", "material": "emissive", "opacity": 0.22,
         "texture": "holo", "marker": "[SIM]", "label": "eixo T_M (REFLECT/MANIFEST) X",
         "desc": "Canal de translacao holografica T_M entre as faces opostas -X/+X pelo bulk central."},
        {"id": "tm_axis_y", "layer": "core", "shape": "box", "position": [0, 0, 0], "size": 0.5,
         "scale": [0.035, 1.1, 0.035], "color": "#ffcf70", "material": "emissive", "opacity": 0.22,
         "texture": "holo", "marker": "[SIM]", "label": "eixo T_M (REFLECT/MANIFEST) Y",
         "desc": "Canal de translacao holografica T_M entre as faces opostas -Y/+Y pelo bulk central."},
        {"id": "tm_axis_z", "layer": "core", "shape": "box", "position": [0, 0, 0], "size": 0.5,
         "scale": [0.035, 0.035, 1.1], "color": "#ffcf70", "material": "emissive", "opacity": 0.22,
         "texture": "holo", "marker": "[SIM]", "label": "eixo T_M (REFLECT/MANIFEST) Z",
         "desc": "Canal de translacao holografica T_M entre as faces opostas -Z/+Z pelo bulk central."},
        {"id": "pacote", "layer": "shell", "shape": "box", "position": [0, -1.02, 0], "size": 1.55,
         "scale": [1, 0.04, 1], "color": "#0e1218", "material": "matte", "opacity": 1.0,
         "marker": "[HARDWARE]", "label": "substrato do pacote", "desc": "Encapsulamento ceramico do chip."},
        {"id": "housing", "layer": "structure", "shape": "box", "position": [0, 0, 0], "size": 0.68,
         "color": "#88a0c8", "material": "glass", "opacity": 0.14, "marker": "[HARDWARE]",
         "label": "Involucro da celula (1 um)", "desc": "Micro-camara cubica de lado L=1 um (f=150 THz)."},
    ]
    for i, (x, z) in enumerate([(0.5, 0.5), (0.5, -0.5), (-0.5, 0.5), (-0.5, -0.5)]):
        meshes.append({"id": f"pilar{i}", "layer": "structure", "shape": "cylinder",
                       "position": [x, -0.7, z], "size": 0.03, "scale": [1, 0.9, 1],
                       "color": "#5a6474", "material": "metal", "opacity": 1.0,
                       "label": f"pilar {i}", "desc": "Pilar de sustentacao da celula sobre o chip."})
    for k, (v, r) in faces.items():
        meshes.append({"id": f"grafeno{k}", "layer": "subsystem", "shape": "plane", "position": v,
                       "rotation": r, "size": 0.6, "color": "#3a5a7a", "material": "emissive",
                       "texture": "grid", "opacity": 0.4, "marker": "[HARDWARE]", "label": f"face de grafeno {k}",
                       "desc": "Substrato holografico 2D: grafeno funcionalizado (ancoragem de fase)."})
    doc = {
        "patent_id": PATENT_ID, "title": "MQC - Celula Cubica sobre Chip (COMPUTADO pelo runner)",
        "kind": "device", "schema": 2, "generated_by": "one_mqc.py (forma=conteudo)",
        "note": "[SIM][HARDWARE] Projecao concreta COMPUTADA pela simulacao: as 27 posicoes de "
                "qubit saem de gerar_topologia_celula() (nao desenhadas a mao). Chip -> celula de "
                "vidro (1 um) -> 6 faces de grafeno -> 27 qubits. Descasque/corte para ver por dentro. "
                "Dispositivo fisico NAO construido.",
        "camera": {"position": [2.0, 1.5, 2.0]},
        "layers": [{"id": "shell", "name": "Involucro externo", "order": 0, "peelable": True},
                   {"id": "structure", "name": "Blindagem / estrutura", "order": 1, "peelable": True},
                   {"id": "subsystem", "name": "Subsistemas", "order": 2, "peelable": True},
                   {"id": "core", "name": "Nucleo funcional", "order": 3, "peelable": True}],
        "groups": [{"name": "vertice", "color": GC["vertice"], "label": "8 qubits de vertice", "count": tipos.count("vertice"), "explodable": True},
                   {"name": "aresta", "color": GC["aresta"], "label": "12 qubits de aresta", "count": tipos.count("aresta"), "explodable": True},
                   {"name": "face", "color": GC["face"], "label": "6 qubits de face", "count": tipos.count("face"), "explodable": True},
                   {"name": "centro", "color": GC["centro"], "label": "controlador central", "count": tipos.count("centro"), "explodable": True}],
        "meshes": meshes, "nodes": nodes, "edges": edges,
        "dimensions": [{"from": [-0.55, 0.72, 0.55], "to": [0.55, 0.72, 0.55], "label": "L = 1 um (celula)", "color": "#ffd60a"},
                       {"from": [-0.7, -1.05, 0.75], "to": [0.7, -1.05, 0.75], "label": "chip de silicio", "color": "#7ce7c8"}],
        "constants": [{"symbol": "geometria", "value": "3^3 = 27 qubits, L=1 um", "note": "rho_q~=2,7e13 q/cm3"},
                      {"symbol": "beta_TGL", "value": f"{beta:.12f} (alpha*sqrt(e))", "note": "acoplamento holografico"}],
    }
    out = PATENT_DIR / "render3d.json"
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[one_mqc] render3d.json COMPUTADO ({len(nodes)} nos, {len(meshes)} malhas) — forma=conteudo")


if __name__ == "__main__":
    sys.exit(main())
