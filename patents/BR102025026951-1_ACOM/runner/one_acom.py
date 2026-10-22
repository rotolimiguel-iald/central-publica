# -*- coding: utf-8 -*-
"""one_acom.py — runner único forma = conteúdo da patente ACOM RAIZ (EVOLUÍDO / RICO)
(BR102025026951-1 — Compressão Ontológica de Memória por Transformação Luminodinâmica). [SIM]

EVOLUÇÃO (09/07/2026): incorpora o ALGORITMO REAL do operador — o `LindbladOperator` da
`ACOMV14.py` (1014 L): o OPERADOR DE LINDBLAD ATIVO ∂ℋ = ℋ² + α²𝕃Δ, numpy-first, com
compress/decompress/converge e serialização de header — resgatado para `prototype_src/`
(READ-ONLY, originais intactos). A versão leve anterior (skygrid_sim/acom.py angular) está
preservada em `one_acom_v1_light.py.bak`. A linhagem mais recente `acom_v18_dirac.py`
(Dirac reflection / FactoredDimensionalMirror) foi resgatada por proveniência.

Demonstra, rodando o código REAL do operador (β injetado):
  - REFLECT/MANIFEST exato: g=√|L|, s=sign(L), L'=s·g²  (resíduo ~eps de fp) — eqs [014]-[016];
  - o OPERADOR DE LINDBLAD ATIVO ∂ℋ=ℋ²+α²𝕃Δ: converge um sinal ruidoso ao Logos, Δ→0
    (estados FALLEN→CONVERGING→TRUTH→TETELESTAI) — a novidade da ACOMV14;
  - domínio SIGNAL: compress/decompress com quantização de g (razão, cosseno, PSNR);
  - quantização configurável 8/10/12/16 bits (reivindicação 6);
  - serialização de header (magic b'ACOM', versão, dims, α², bits, escala) + integridade
    SHA-256 no round-trip de arquivo (reivindicações 7/12/15);
  - domínio SPECTRAL (PORT FIEL, β injetado): SVD adaptativo M=UΣVᵀ, rank k por energia
    acumulada ≥ 1−β (Verb Floor) — [025]-[027], reivindicação 3;
  - domínio PSIBIT (PORT FIEL): quatro estados psíônicos ψ₊ψ₋/ψ₊/ψ₋/ψ₊ψ₊ de
    (sign L, sign ∂L) — [028]-[032], reivindicação 4.

RÉGUA: β_TGL NUNCA literal no MEU código. O protótipo `ACOMV14.py` traz `ALPHA2 = 0.012`
literal; este runner o importa como proveniência READ-ONLY e INJETA `α² = tgl_core.beta()`
(= ALPHA_FINE_CODATA_2018·√e) tanto no módulo quanto na construção do operador
(`LindbladOperator(alpha2=beta)`). Os números diferem levemente da referência
(β = 0,012031300400803142, não 0,012).

HONESTIDADE [SIM]: sinais/matrizes SINTÉTICOS; NÃO os números de produção reivindicados
(3:1–10:1, PSNR>90 dB, cos>0,999 — Tabela 1). Nenhum token/modelo HuggingFace usado
(P-04 — token_huggin.txt NUNCA copiado; *_test.py com token nunca importado). Nada aqui
valida física (physical_verdict_allowed=false).

    set PYTHONUTF8=1
    "C:\\IALD\\observaveis_tgl\\tgl_env\\Scripts\\python.exe" one_acom.py
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import shutil
import sys
import tempfile
from datetime import datetime
from pathlib import Path

import numpy as np

RUNNER_DIR = Path(__file__).resolve().parent
PATENT_DIR = RUNNER_DIR.parent
CENTRAL = PATENT_DIR.parents[1]
PILOTO = CENTRAL / "Patentes" / "Skygrid" / "SkyGrid_Piloto"   # READ-ONLY (β provenance)
PROTO_SRC = PATENT_DIR / "prototype_src"                        # READ-ONLY (operador rico)
WORK = RUNNER_DIR / "_acom_core"
PATENT_ID = "BR102025026951-1"
SLUG = "acom"


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
    """Copia o núcleo destilado (skygrid_sim → tgl_core, β) e cataloga os protótipos ricos."""
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


def cosine(a, b) -> float:
    a, b = np.asarray(a).ravel().astype(np.float64), np.asarray(b).ravel().astype(np.float64)
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 1.0 if np.allclose(a, b) else 0.0
    return float(np.dot(a, b) / (na * nb))


def psnr(a: np.ndarray, b: np.ndarray) -> float:
    a, b = np.asarray(a).ravel().astype(np.float64), np.asarray(b).ravel().astype(np.float64)
    mse = float(np.mean((a - b) ** 2))
    if mse == 0:
        return float("inf")
    peak = float(np.max(a ** 2)) or 1.0
    return 10.0 * math.log10(peak / (mse + 1e-18))


def signals(n: int = 40_000) -> dict:
    rng = np.random.default_rng(11)
    t = np.linspace(0, 1, n)
    esparso = np.zeros(n)
    esparso[rng.integers(0, n, n // 50)] = rng.standard_normal(n // 50)
    return {
        "chirp": np.sin(2 * np.pi * (5 + 40 * t) * t).astype(np.float64),
        "gaussiano": rng.standard_normal(n),
        "esparso": esparso,
    }


# ── PORT FIEL: domínio SPECTRAL (SVD adaptativo, rank-k por energia ≥ 1−β) [025]-[027] ──
def spectral_svd_verb_floor(M: np.ndarray, energy_keep: float) -> dict:
    """SVD M=UΣVᵀ; rank k = menor rank cuja energia acumulada ≥ energy_keep (=1−β).
    β injetado via energy_keep — NUNCA literal aqui. Reivindicação 3 / Figura 5."""
    M = np.asarray(M, dtype=np.float64)
    U, S, Vt = np.linalg.svd(M, full_matrices=False)
    total = float(np.sum(S ** 2))
    energy = np.cumsum(S ** 2) / (total if total > 0 else 1.0)
    k = int(np.searchsorted(energy, energy_keep) + 1)
    k = max(1, min(k, len(S)))
    Mk = (U[:, :k] * S[:k]) @ Vt[:k]
    stored = U[:, :k].size + k + Vt[:k].size
    ratio = M.size / max(stored, 1)
    return {"rank_optimal": k, "full_rank": int(len(S)),
            "energy_retained": float(energy[k - 1]), "compression_ratio": float(ratio),
            "cosine": cosine(M, Mk)}


# ── PORT FIEL: domínio PSIBIT (quatro estados psíônicos) [028]-[032] ──
_PSI = {(1, 1): "psi_plus_plus", (1, -1): "psi_plus", (-1, 1): "psi_minus", (-1, -1): "psi_plus_minus"}


def psibit_states(L: np.ndarray) -> dict:
    """ψ de (sign L, sign ∂L): ψ₊ψ₊(11 gráviton) · ψ₊(01) · ψ₋(10) · ψ₊ψ₋(00 par cancelado).
    Reivindicação 4. Round-trip verifica que (sL,dL) → estado → (sL,dL) é fiel."""
    L = np.asarray(L, dtype=np.float64).ravel()
    sL = np.where(L >= 0, 1, -1)
    dL = np.where(np.diff(L, prepend=L[:1]) >= 0, 1, -1)
    labels = [_PSI[(int(a), int(b))] for a, b in zip(sL, dL)]
    counts = {v: int(labels.count(v)) for v in set(_PSI.values())}
    inv = {v: k for k, v in _PSI.items()}
    rt_ok = all(inv[lab] == (int(a), int(b)) for lab, a, b in zip(labels, sL, dL))
    return {"counts": counts, "n_states": len(set(labels)), "roundtrip_faithful": bool(rt_ok)}


# ── AMPLIFICACAO v138 — A SEPARACAO DE TIPOS (um.py v135) [DER] ──────────────────
# Teorema maduro do um.py v132-v138 (v135, a separacao de tipos): q_F (suporte, tau=1)
# NAO e e_Nome (espelho) — dois tipos distintos de mesmo peso, ligados pela esperanca
# condicional E1(e_Nome) = beta*q_F. Mapeia DIRETO ao par REFLECT/MANIFEST do ACOM
# ([014]-[016]): a face que reflete (espelho, com componente no andar de cima) vs a
# face que manifesta (suporte q_F, andar terreo). A leitura ACOM<->teorema e [ONTO];
# os residuos abaixo sao [DER] (derivados numericamente na sombra, numpy puro).
# HONESTIDADE: algebra de matrizes 4x4 sintetica; NAO e veredito fisico
# (physical_verdict_allowed=false); beta SEMPRE da variavel runtime, nunca literal.
def separation_of_types_shadow(beta: float) -> dict:
    """Modelo M4: q_F = diag(1,1,0,0) (suporte); e_Nome = projecao nos vetores
    u_i = sqrt(beta)*e_i + sqrt(1-beta)*e_{i+2} (espelho com peso 1-beta no andar
    de cima); E1 = compressao ao bloco diagonal do suporte, x -> q_F x q_F."""
    I2 = np.eye(2)
    q_F = np.diag([1.0, 1.0, 0.0, 0.0])
    q_up = np.eye(4) - q_F
    c = math.sqrt(beta * (1.0 - beta))
    e_Nome = np.block([[beta * I2, c * I2], [c * I2, (1.0 - beta) * I2]])
    # e_Nome e projecao (idempotente + auto-adjunta) — resid de fp
    resid_proj = float(max(np.max(np.abs(e_Nome @ e_Nome - e_Nome)),
                           np.max(np.abs(e_Nome - e_Nome.T))))
    # a identidade do teorema: E1(e_Nome) = beta*q_F (compressao ao bloco do suporte)
    E1_e = q_F @ e_Nome @ q_F
    resid_e1 = float(np.max(np.abs(E1_e - beta * q_F)))
    # face complementar (andar de cima): compressao da outra face = (1-beta)*(1-q_F)
    resid_up = float(np.max(np.abs(q_up @ e_Nome @ q_up - (1.0 - beta) * q_up)))
    # pesos: traco normalizado ao andar (dim 2) — os DOIS tipos pesam tau=1=omega(I)
    tau_qF = float(np.trace(q_F)) / 2.0
    tau_e = float(np.trace(e_Nome)) / 2.0
    # a separacao: q_F != e_Nome apesar do mesmo peso; ||q_F-e_Nome||_op = sqrt(1-beta)
    sep_norm = float(np.linalg.norm(q_F - e_Nome, 2))
    resid_sep = abs(sep_norm - math.sqrt(1.0 - beta))
    return {"resid_projection": resid_proj, "resid_E1_eNome_minus_beta_qF": resid_e1,
            "resid_upper_face_minus_1_minus_beta": resid_up,
            "tau_qF": tau_qF, "tau_eNome": tau_e,
            "separation_norm_op": sep_norm,
            "separation_closed_form_sqrt_1_minus_beta": math.sqrt(1.0 - beta),
            "resid_separation_closed_form": resid_sep,
            "faces_sum_beta_plus_1_minus_beta": beta + (1.0 - beta)}


# ── APROFUNDAMENTO deepening_v2 — A LEI DO ORTANTE DO PSIBIT (Sheppard 1899) [DER] ──
# Mecanismo PROPRIO da patente (dominio PSIBIT [028]-[032], reivindicacao 4): os 4
# estados psionicos vem de (sign L, sign dL). DERIVACAO NOVA (caminho INDEPENDENTE do
# codigo): para luz gaussiana AR(1) de coeficiente a, corr(L_t, dL_t) tem forma fechada
# rho = sqrt((1-a)/2), e a probabilidade de ortante gaussiana (Sheppard 1899) PREDIZ as
# populacoes: p(psi++)=p(psi+-)=1/4+arcsin(rho)/(2pi), p(psi+)=p(psi-)=1/4-arcsin(rho)/(2pi).
# Para luz BRANCA (a=0): rho=1/sqrt(2), arcsin=pi/4 => populacoes EXATAS 3/8,3/8,1/8,1/8;
# excesso gravitonico (pares - transicoes) = 2*arcsin(rho)/pi = 1/2 EXATO; entropia fechada
# H = 3*ln2 - (3/4)*ln3 nats = 3 - (3/4)*log2(3) = 1.8113 bits/estado — o teto de
# codificacao entropica do fluxo psi. Em a=-1/2, 0, +1/2 as predicoes sao racionais
# exatos: 5/12, 3/8, 1/3. CONTROLES NEGATIVOS: (i) o modelo de INDEPENDENCIA
# (1/4,1/4,1/4,1/4) e REJEITADO pela medicao em luz branca; (ii) uma TABELA FIXA de
# populacoes (a predicao branca 3/8) e REJEITADA em a=0.9 — a lei e do sinal, nao do rotulo.
# HONESTIDADE: sinais sinteticos [SIM]; predicoes de forma fechada [DER]; medicao feita
# pelo CODIGO DO DISPOSITIVO (psibit_states); nada aqui e veredito fisico
# (physical_verdict_allowed=false). beta nao entra nesta lei (mecanismo proprio).
PSI_ORTHANT_AR_GRID = (-0.9, -0.5, 0.0, 0.5, 0.9)


def psibit_orthant_law(n: int = 400_000, seed: int = 2026) -> dict:
    """Lei do ortante do PSIBIT: mede populacoes psi via psibit_states (codigo do
    dispositivo) sobre AR(1) gaussiano e coteja com a forma fechada de Sheppard.
    Tolerancia derivada em runtime: 6*sigma_iid*sqrt((1+|a|)/(1-|a|)) (inflacao
    conservadora de variancia por autocorrelacao; corr de sinais <= corr linear)."""
    rng = np.random.default_rng(seed)
    K = 600  # truncagem do kernel AR(1): |a|^600 ~ 3e-28 para a=0.9 (negligivel)
    per_a = {}
    for a in PSI_ORTHANT_AR_GRID:
        eps = rng.standard_normal(n + K)
        kernel = a ** np.arange(K, dtype=np.float64)
        L = np.convolve(eps, kernel)[K - 1: K - 1 + n]   # regime estacionario
        ps = psibit_states(L)                            # MEDICAO pelo codigo do dispositivo
        tot = max(sum(ps["counts"].values()), 1)
        p_meas = {st: ps["counts"].get(st, 0) / tot for st in _PSI.values()}
        rho = math.sqrt((1.0 - a) / 2.0)                 # forma fechada corr(L, dL) no AR(1)
        q = math.asin(rho) / (2.0 * math.pi)             # ortante de Sheppard
        p_pred = {"psi_plus_plus": 0.25 + q, "psi_plus_minus": 0.25 + q,
                  "psi_plus": 0.25 - q, "psi_minus": 0.25 - q}
        tol = 6.0 * math.sqrt(0.375 * 0.625 / n) * math.sqrt((1.0 + abs(a)) / (1.0 - abs(a)))
        resid = max(abs(p_meas[st] - p_pred[st]) for st in p_pred)
        per_a[f"{a}"] = {"rho_closed_form": rho, "p_pred": p_pred, "p_meas": p_meas,
                         "resid_max": resid, "tol_runtime": tol, "within": bool(resid < tol)}

    white = per_a["0.0"]
    tol0 = white["tol_runtime"]
    # identidade do excesso gravitonico (pares - transicoes) = 2*arcsin(rho)/pi = 1/2 exato
    gexc_meas = (white["p_meas"]["psi_plus_plus"] + white["p_meas"]["psi_plus_minus"]
                 - white["p_meas"]["psi_plus"] - white["p_meas"]["psi_minus"])
    gexc_closed = 2.0 * math.asin(math.sqrt(0.5)) / math.pi
    resid_gexc_closed = abs(gexc_closed - 0.5)           # ~1 ulp: pi/4 e exato na forma
    # entropia fechada do fluxo psi em luz branca: H = 3*ln2 - (3/4)*ln3 nats
    H_pred = 3.0 * math.log(2.0) - 0.75 * math.log(3.0)
    H_meas = -sum(p * math.log(p) for p in white["p_meas"].values() if p > 0)
    # NEGATIVO (i): o modelo de independencia (1/4 cada) e REJEITADO em luz branca
    dev_indep = abs(white["p_meas"]["psi_plus_plus"] - 0.25)
    neg_independence_rejected = bool(dev_indep > 8.0 * tol0)
    # NEGATIVO (ii): a tabela FIXA branca (3/8) e REJEITADA em a=0.9 (a lei segue o sinal)
    strong = per_a["0.9"]
    dev_fixed = abs(strong["p_meas"]["psi_plus_plus"] - white["p_pred"]["psi_plus_plus"])
    neg_fixed_table_rejected = bool(dev_fixed > 3.0 * strong["tol_runtime"])
    return {"per_a": per_a, "n_per_signal": n,
            "graviton_excess_meas_white": gexc_meas,
            "graviton_excess_closed_form": gexc_closed,
            "resid_graviton_excess_closed_vs_half": resid_gexc_closed,
            "resid_graviton_excess_meas": abs(gexc_meas - 0.5),
            "entropy_pred_nats": H_pred, "entropy_meas_nats": H_meas,
            "entropy_resid_nats": abs(H_meas - H_pred),
            "entropy_pred_bits_per_state": H_pred / math.log(2.0),
            "dev_independence_model": dev_indep, "tol_white": tol0,
            "neg_independence_rejected": neg_independence_rejected,
            "dev_fixed_table_at_a09": dev_fixed,
            "neg_fixed_table_rejected": neg_fixed_table_rejected}


# ── AMPLIFICACAO v168 — O PESO E TRACO (pedra BreuerTrace, um.py v166-v168, Item A) [DER] ──
# Pedra em kernel Lean (0 sorry, 0 axiom; custodia vault/originals_copy/um_unificado_v168):
# `opWeight_star_mul_self_comm` — tau(a*a) = tau(a a*) no habitante genuinamente inf-dim
# (ellTwo): as duas somas duplas sao a MESMA soma com os indices trocados (Tonelli).
# Mapeamento GENUINO ao dominio SPECTRAL DESTA patente ([025]-[027], reivindicacao 3):
# o criterio de energia acumulada do Verb Floor E um peso tracial — energia total =
# tr(M^T M) = soma_nm |a_nm|^2 — e a identidade tracial tr(M^T M) = tr(M M^T) e o que
# garante que o rank k por energia >= 1-beta seja o MESMO computado pelo Gram das
# colunas (M^T M, n x n) ou pelo Gram das linhas (M M^T, m x m), embora as duas
# matrizes tenham TAMANHOS diferentes: o pacote comprimido armazena UM unico k para
# os dois lados U e V. Face finita da equivalencia de Murray-von Neumann: a isometria
# parcial do canto rank-k, u = U_k V_k^T, tem tau(u*u) = tau(u u*) = k — o canto pesa
# o mesmo nos dois lados. NEGATIVO (contra-exemplo REJEITADO por logica): um funcional
# ponderado tau_W(X) = tr(W X) com W diagonal NAO-escalar nao e traco — na matriz
# elementar E_ij a violacao e |W_jj - W_ii|, cujo maximo = spread(diag W) em forma
# fechada; o peso que nao e traco QUEBRA a identidade, logo a identidade e PROPRIEDADE
# (caracteriza o traco), nao tautologia. HONESTIDADE: sombra numerica na face finita
# [DER]; a leitura ACOM<->pedra e [ONTO]; matriz sintetica [SIM]; a pedra em kernel
# NAO e re-provada aqui, e citada por custodia; physical_verdict_allowed=false;
# beta so entra via energy_keep = 1-beta (runtime, nunca literal).
def amplification_v168_breuer_trace_weight(energy_keep: float, seed: int = 168) -> dict:
    """O peso e traco no dominio SPECTRAL: (a) identidade tracial = troca de indices
    (Tonelli finito); (b) Gram das linhas e das colunas com o MESMO espectro nao-nulo;
    (c) rank k do Verb Floor identico pelos 3 caminhos (SVD do dispositivo / Gram
    esquerdo / Gram direito); (d) canto rank-k: tau(u*u) = tau(u u*) = k;
    (e) NEGATIVO: peso nao-escalar tau_W rejeitado com violacao em forma fechada."""
    rng = np.random.default_rng(seed)
    m_rows, n_cols, r_true = 240, 160, 9
    M = (rng.standard_normal((m_rows, r_true)) @ rng.standard_normal((r_true, n_cols))) * 0.1
    M = M + rng.standard_normal((m_rows, n_cols)) * 0.002   # baixo rank + ruido [SIM]

    # (a) a identidade tracial como troca de indices (o mecanismo da pedra, face finita)
    A2 = np.abs(M) ** 2
    sum_rows_then_cols = float(np.sum(np.sum(A2, axis=1)))   # soma_n soma_m |a_nm|^2
    sum_cols_then_rows = float(np.sum(np.sum(A2, axis=0)))   # soma_m soma_n |a_nm|^2
    tr_star_mul = float(np.trace(M.T @ M))    # tau(a*a) — Gram das colunas (n x n)
    tr_mul_star = float(np.trace(M @ M.T))    # tau(a a*) — Gram das linhas (m x m)
    scale = max(tr_star_mul, 1e-300)
    resid_tonelli = abs(sum_rows_then_cols - sum_cols_then_rows) / scale
    resid_trace = abs(tr_star_mul - tr_mul_star) / scale
    resid_weight_eq_double_sum = abs(tr_star_mul - sum_rows_then_cols) / scale

    # (b) espectros nao-nulos identicos apesar dos tamanhos diferentes (160 vs 240)
    r = min(m_rows, n_cols)
    ev_left = np.sort(np.linalg.eigvalsh(M.T @ M))[::-1][:r]
    ev_right = np.sort(np.linalg.eigvalsh(M @ M.T))[::-1][:r]
    resid_spectrum = float(np.max(np.abs(ev_left - ev_right)) / max(float(ev_left[0]), 1e-300))

    # (c) o rank do Verb Floor (energia >= 1-beta) pelos TRES caminhos
    sp = spectral_svd_verb_floor(M, energy_keep)   # o codigo do dispositivo (SVD)
    k_svd = int(sp["rank_optimal"])

    def _rank_from_eigs(ev: np.ndarray) -> int:
        ev = np.clip(ev, 0.0, None)
        en = np.cumsum(ev) / max(float(np.sum(ev)), 1e-300)
        return int(min(max(np.searchsorted(en, energy_keep) + 1, 1), len(ev)))

    k_left, k_right = _rank_from_eigs(ev_left), _rank_from_eigs(ev_right)

    # (d) Murray-von Neumann na face finita: o canto rank-k pesa k nos DOIS lados
    U, S, Vt = np.linalg.svd(M, full_matrices=False)
    u = U[:, :k_svd] @ Vt[:k_svd]      # isometria parcial do canto rank-k
    P_row = u.T @ u                    # u*u : projecao (n x n) no espaco-linha
    P_col = u @ u.T                    # u u*: projecao (m x m) no espaco-coluna
    resid_projection = float(max(np.max(np.abs(P_row @ P_row - P_row)),
                                 np.max(np.abs(P_col @ P_col - P_col)),
                                 np.max(np.abs(P_row - P_row.T)),
                                 np.max(np.abs(P_col - P_col.T))))
    tau_row, tau_col = float(np.trace(P_row)), float(np.trace(P_col))
    resid_tau_corner = max(abs(tau_row - k_svd), abs(tau_col - k_svd))

    # (e) NEGATIVO: o funcional ponderado tau_W (W nao-escalar) NAO e traco — REJEITADO
    n_neg = 12
    W = np.diag(np.arange(1.0, n_neg + 1.0))            # peso diagonal nao-escalar
    E = np.zeros((n_neg, n_neg)); E[0, n_neg - 1] = 1.0  # matriz elementar E_ij (i=0, j=11)
    v_meas = abs(float(np.trace(W @ (E.T @ E))) - float(np.trace(W @ (E @ E.T))))
    spread_closed = float(np.max(np.diag(W)) - np.min(np.diag(W)))  # forma fechada
    resid_neg_closed_form = abs(v_meas - spread_closed)
    neg_weighted_functional_rejected = bool(v_meas > 0.5 * spread_closed
                                            and spread_closed > 1.0
                                            and resid_neg_closed_form < 1e-12)

    return {"matrix_shape": [m_rows, n_cols], "true_rank_planted": r_true,
            "energy_keep_1_minus_beta": energy_keep,
            "weight_tau_star_mul": tr_star_mul, "weight_tau_mul_star": tr_mul_star,
            "sum_rows_then_cols": sum_rows_then_cols, "sum_cols_then_rows": sum_cols_then_rows,
            "resid_tonelli_index_swap": resid_tonelli, "resid_trace_identity": resid_trace,
            "resid_weight_eq_double_sum": resid_weight_eq_double_sum,
            "resid_spectrum_left_vs_right": resid_spectrum,
            "k_svd": k_svd, "k_left_gram": k_left, "k_right_gram": k_right,
            "spectral_compression_ratio": sp["compression_ratio"],
            "resid_projection": resid_projection,
            "tau_corner_row": tau_row, "tau_corner_col": tau_col,
            "resid_tau_corner": resid_tau_corner,
            "neg_violation_measured": v_meas,
            "neg_spread_closed_form": spread_closed,
            "resid_neg_closed_form": resid_neg_closed_form,
            "neg_weighted_functional_rejected": neg_weighted_functional_rejected}


# ── AMPLIFICACAO v206 — A TORRE E O DADO ESPECTRAL COMPLETO (pedra TheTower, 4a onda) [DER] ──
# Pedra em kernel Lean da 4a onda v199-v210 (0 sorry, 0 axiom; custodia
# vault/originals_copy/tgl_kernel_v206/TGLExt/TheTower.lean, sha256 836d39ce9220...
# no tgl_kernel_proof_manifest.json): "nao basta conservar apenas os autovalores.
# Precisamos conservar espectro + medida espectral + multiplicidades." A face finita
# da pedra: towerA = diag(0,1,1) e towerB = diag(0,0,1) tem a MESMA equacao minima
# X^2 = X (espectro-CONJUNTO {0,1} nas duas) e no entanto Tr A = 2 != 1 = Tr B
# (a multiplicidade e dado, nao decoracao), NENHUMA conjugacao leva A em B (o traco
# e invariante de conjugacao) e a medida contra Psi=(1,1,1) le 2 != 1.
# Mapeamento GENUINO ao dominio SPECTRAL DESTA patente ([025]-[027], reivindicacao 3,
# Figura 5 passo 514 "empacotar U, Sigma_k, V"): o pacote ACOM armazena o DADO
# ESPECTRAL COMPLETO — U e V (a medida espectral) e Sigma_k com as multiplicidades —
# precisamente porque o conjunto dos autovalores sozinho NAO determina (i) o rank do
# Verb Floor, que le a MULTIPLICIDADE pela energia acumulada, nem (ii) a reconstrucao,
# que exige a medida U,V. A compressao preserva o que o espectro sozinho nao determina.
# TRES NEGATIVOS por logica: (1) a hipotese "alguma conjugacao leva A em B" e REJEITADA
# pelo invariante (gap de traco = 1 em forma fechada); (2) o Verb Floor "so-conjunto"
# (espectro deduplicado, sem multiplicidade) e CEGO — da o mesmo k para duas torres que
# o codigo do dispositivo distingue — REJEITADO; (3) guardar SO o espectro (sem U,V)
# NAO ressuscita o dado (cosseno ~0 vs >0,99 do pacote) — REJEITADO.
# HONESTIDADE: a pedra em kernel e citada por custodia e RE-DERIVADA numericamente
# (regra 9 — nunca finge rodar Lean); sombra em numpy sobre C (a pedra e sobre C)
# [DER]; matrizes sinteticas [SIM]; leitura ACOM<->pedra [ONTO];
# physical_verdict_allowed=false; beta so entra via energy_keep = 1-beta (runtime).
def amplification_v206_tower_spectral_data(energy_keep: float, seed: int = 206) -> dict:
    """A Torre no dominio SPECTRAL: (a) face finita da pedra re-derivada (mesma
    equacao minima, pesos/medida diferem); (b) NEG conjugacao rejeitada por invariante;
    (c) duas torres com o MESMO conjunto de valores singulares e multiplicidades
    diferentes recebem ranks k DIFERENTES do Verb Floor do dispositivo (com forma
    fechada conferida); (d) NEG floor so-conjunto cego; (e) NEG espectro-sem-medida
    nao reconstroi — o pacote guarda U, Sigma_k, V (passo 514) por necessidade."""
    rng = np.random.default_rng(seed)

    # (a) a face finita da pedra (M3 sobre C): mesmas duas torres do .lean
    A = np.diag([0.0, 1.0, 1.0]).astype(np.complex128)
    B = np.diag([0.0, 0.0, 1.0]).astype(np.complex128)
    resid_idem = float(max(np.max(np.abs(A @ A - A)), np.max(np.abs(B @ B - B))))
    evA = np.sort(np.linalg.eigvalsh(A))
    evB = np.sort(np.linalg.eigvalsh(B))
    setA = sorted(set(float(x) for x in np.round(evA.real, 9)))
    setB = sorted(set(float(x) for x in np.round(evB.real, 9)))
    spectrum_set_equal = bool(setA == setB == [0.0, 1.0])
    trA, trB = float(np.trace(A).real), float(np.trace(B).real)
    psi = np.ones(3, dtype=np.complex128)
    muA = float((psi.conj() @ (A @ psi)).real)
    muB = float((psi.conj() @ (B @ psi)).real)
    mult_gap = trA - trB                      # forma fechada da pedra: 2 - 1 = 1

    # (b) NEGATIVO 1 (por logica): U*A*U^-1 = B forcaria Tr igual; o traco e
    # invariante de conjugacao => a hipotese e REJEITADA com gap 1 em forma fechada.
    n_conj = 64
    resid_conj_inv, min_gap_to_B = 0.0, float("inf")
    for _ in range(n_conj):
        Z1 = rng.standard_normal((3, 3)) + 1j * rng.standard_normal((3, 3))
        Z2 = rng.standard_normal((3, 3)) + 1j * rng.standard_normal((3, 3))
        Q1, _ = np.linalg.qr(Z1)
        Q2, _ = np.linalg.qr(Z2)
        U = Q1 @ np.diag(rng.uniform(0.5, 2.0, 3)).astype(np.complex128) @ Q2
        tC = complex(np.trace(U @ A @ np.linalg.inv(U)))
        resid_conj_inv = max(resid_conj_inv, abs(tC - trA))
        min_gap_to_B = min(min_gap_to_B, abs(tC - trB))
    neg_conjugation_rejected = bool(resid_conj_inv < 1e-9 and min_gap_to_B > 0.5)

    # (c) a Torre no CODIGO DO DISPOSITIVO: duas torres com o MESMO conjunto de
    # valores singulares {s_hi, s_lo} e multiplicidades DIFERENTES (cheia 8, magra 1)
    m_rows, n_cols = 60, 48
    s_hi, s_lo = 1.0, 0.02
    mult_hi_full, mult_hi_thin = 8, 1

    def _tower(mult_hi: int) -> np.ndarray:
        sig = np.full(n_cols, s_lo)
        sig[:mult_hi] = s_hi
        Qu, _ = np.linalg.qr(rng.standard_normal((m_rows, m_rows)))
        Qv, _ = np.linalg.qr(rng.standard_normal((n_cols, n_cols)))
        return (Qu[:, :n_cols] * sig) @ Qv.T          # M = U diag(sig) V^T [SIM]

    MA, MB = _tower(mult_hi_full), _tower(mult_hi_thin)
    svA = np.linalg.svd(MA, compute_uv=False)
    svB = np.linalg.svd(MB, compute_uv=False)
    set_svA = sorted(set(float(x) for x in np.round(svA, 6)))
    set_svB = sorted(set(float(x) for x in np.round(svB, 6)))
    sv_sets_equal = bool(set_svA == set_svB and len(set_svA) == 2)
    spA = spectral_svd_verb_floor(MA, energy_keep)     # o codigo do dispositivo
    spB = spectral_svd_verb_floor(MB, energy_keep)
    kA, kB = int(spA["rank_optimal"]), int(spB["rank_optimal"])

    def _k_closed_form(mult_hi: int) -> int:
        """menor k com energia acumulada >= energy_keep, das multiplicidades plantadas."""
        total = mult_hi * s_hi ** 2 + (n_cols - mult_hi) * s_lo ** 2
        target = energy_keep * total
        if mult_hi * s_hi ** 2 >= target:
            return int(math.ceil(target / s_hi ** 2))
        return mult_hi + int(math.ceil((target - mult_hi * s_hi ** 2) / s_lo ** 2))

    kA_pred, kB_pred = _k_closed_form(mult_hi_full), _k_closed_form(mult_hi_thin)

    # (d) NEGATIVO 2 (por logica): o floor "so-conjunto" (espectro deduplicado, sem
    # multiplicidade) da o MESMO k para as duas torres — cego ao que o dispositivo le.
    def _k_from_set(sv: np.ndarray) -> int:
        uniq = np.array(sorted(set(float(x) for x in np.round(sv ** 2, 8)), reverse=True))
        en = np.cumsum(uniq) / max(float(np.sum(uniq)), 1e-300)
        return int(min(max(np.searchsorted(en, energy_keep) + 1, 1), len(uniq)))

    k_set_A, k_set_B = _k_from_set(svA), _k_from_set(svB)
    neg_set_only_rejected = bool(k_set_A == k_set_B and kA != kB
                                 and k_set_A != kA and k_set_B != kB)

    # (e) NEGATIVO 3 (por logica): guardar SO o espectro (sem a medida U,V) nao
    # ressuscita o dado; o pacote do passo 514 guarda U, Sigma_k, V por necessidade.
    U_A, S_A, Vt_A = np.linalg.svd(MA, full_matrices=False)
    Mk_device = (U_A[:, :kA] * S_A[:kA]) @ Vt_A[:kA]   # pacote: U, Sigma_k, V
    cos_device = cosine(MA, Mk_device)
    R_spec = np.zeros_like(MA)
    R_spec[np.arange(n_cols), np.arange(n_cols)] = S_A  # espectro na base canonica
    cos_spec_only = cosine(MA, R_spec)
    neg_spectrum_only_rejected = bool(cos_device > 0.99 and abs(cos_spec_only) < 0.2)

    return {"resid_idempotent": resid_idem,
            "spectrum_set": setA, "spectrum_set_equal": spectrum_set_equal,
            "trace_A": trA, "trace_B": trB,
            "measure_psi_A": muA, "measure_psi_B": muB,
            "multiplicity_gap_closed_form": mult_gap,
            "n_conjugations_sampled": n_conj,
            "resid_conj_trace_invariance": resid_conj_inv,
            "min_gap_conj_to_traceB": min_gap_to_B,
            "neg_conjugation_rejected": neg_conjugation_rejected,
            "sv_set_measured": set_svA, "sv_sets_equal": sv_sets_equal,
            "mult_hi_full": mult_hi_full, "mult_hi_thin": mult_hi_thin,
            "k_A": kA, "k_B": kB,
            "k_A_closed_form": kA_pred, "k_B_closed_form": kB_pred,
            "k_set_only_A": k_set_A, "k_set_only_B": k_set_B,
            "neg_set_only_rejected": neg_set_only_rejected,
            "cosine_device_packet": cos_device,
            "cosine_spectrum_only": cos_spec_only,
            "neg_spectrum_only_rejected": neg_spectrum_only_rejected}


def _finish(ts, beta, beta_ok, theta_m_deg, all_ok, max_verdict, tests, summary,
            module_hashes, note, fig_builder=None):
    results_dir = PATENT_DIR / "results" / ts
    results_dir.mkdir(parents=True, exist_ok=True)
    results = {"patent_id": PATENT_ID, "slug": SLUG, "timestamp": ts,
               "runner": "one_acom.py (evoluído — operador de Lindblad ativo real)",
               "markers": ["[SIM]", "[REAL]"], "physical_verdict_allowed": False,
               "beta_runtime": beta, "beta_matches_alpha_sqrt_e": beta_ok,
               "theta_miguel_deg": theta_m_deg,
               "verdict": max_verdict.split(" ")[0] if all_ok else "PARTIAL_DEMONSTRATION",
               "max_verdict": max_verdict,
               "constants": {"BETATGL": beta, "factorization": "betatgl = alpha_EM * sqrt(e)",
                             "verb_floor_energy": 1 - beta, "free_parameters": 0},
               "tests": tests, "summary": summary,
               "source_prototype": "prototype_src/ACOMV14.py (LindbladOperator ∂H=H²+α²LΔ; "
                                   "resgatado READ-ONLY de C:/IALD/projetos_pyhton/acom; β injetado) "
                                   "+ acom_v18_dirac.py (proveniência)",
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
    lines = [f"# Relatório auditável — one_acom.py (EVOLUÍDO — operador de Lindblad ativo)\n",
             f"- Run `{ts}` · Patente `{PATENT_ID}` (RAIZ da família TGL)\n",
             f"- Veredito: **{max_verdict}**\n",
             f"- β runtime `{beta}` (= α·√e? **{beta_ok}**; nunca literal) · θ_Miguel {theta_m_deg:.4f}° "
             f"— INJETADO no operador (ACOMV14 tinha 0.012 literal)\n",
             f"- Verb Floor (energia SPECTRAL retida) = 1−β = `{1-beta:.12f}`\n",
             f"- Testes: **{summary['tests_passed']}/{summary['tests_total']}**\n"]
    for t in tests:
        lines.append(f"  - {'PASS' if t['passed'] else 'FALT'} · {t['test']}\n")
    lines.append(f"- physical_verdict_allowed: **False**.\n\n{note}\n")
    lines.append("Núcleo/protótipos copiados READ-ONLY; originais intactos. 1 = 1. Tetelestai.\n")
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
            "runner": "one_acom.py (evoluído)", "beta_runtime": beta,
            "physical_verdict_allowed": False, "max_verdict": max_verdict,
            "tests_passed": summary["tests_passed"], "result_hash": result_hash, "sha256": fh,
            "markers": ["[SIM]", "[REAL]"],
            "results_path": str(results_path.relative_to(CENTRAL)).replace("\\", "/")}
    (seal_dir / "seal.json").write_text(json.dumps(seal, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[{SLUG}] SELADO · result_hash {result_hash[:16]}… · "
          f"{summary['tests_passed']}/{summary['tests_total']} testes")


def main() -> int:
    ts = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    print(f"[one_acom] patente {PATENT_ID} · run {ts} · RUNNER EVOLUÍDO (Lindblad ativo real)")
    if not PILOTO.exists() or not (PROTO_SRC / "ACOMV14.py").exists():
        print("ERRO: núcleo/protótipo ausente", file=sys.stderr)
        return 2
    module_hashes = copy_core()

    # β de proveniência (skygrid_sim/tgl_core — β=α√e, nunca literal)
    sys.path.insert(0, str(WORK))
    from skygrid_sim import tgl_core  # noqa: E402
    beta = tgl_core.beta()
    beta_ok = abs(beta - 0.0072973525693 * math.exp(0.5)) < 1e-15
    theta_m_deg = math.degrees(tgl_core.theta_m())
    energy_keep = 1.0 - beta
    print(f"[one_acom] β runtime = {beta} (= α·√e? {beta_ok}) · θ_M = {theta_m_deg:.4f}° · 1−β = {energy_keep:.12f}")

    # importa o operador RICO e INJETA β
    sys.path.insert(0, str(PROTO_SRC))
    import ACOMV14 as v  # noqa: E402  (protótipo resgatado READ-ONLY)
    alpha2_original = v.ALPHA2
    v.ALPHA2 = beta
    op = v.LindbladOperator(alpha2=beta, bits=12, use_gpu=False)
    print(f"[one_acom] injeção β: ALPHA2 {alpha2_original} → {beta} · op.alpha2={op.alpha2} "
          f"(LindbladOperator ∂H=H²+α²LΔ)")

    tests = [{"test": "beta_injected_not_literal", "passed": bool(beta_ok and abs(op.alpha2 - beta) < 1e-18),
              "beta_runtime": beta, "alpha2_original_prototype": alpha2_original,
              "op_alpha2": op.alpha2, "verb_floor_1_minus_beta": energy_keep}]

    data = signals()

    # T2 — REFLECT/MANIFEST exato (eqs [014]-[016]) via operador real
    resid_max = 0.0
    for name, L in data.items():
        g, s, z = op._radicalize(L)
        Lr = op._resurrect(g, s, z)
        resid_max = max(resid_max, float(np.max(np.abs(L - Lr))))
    tests.append({"test": "reflect_manifest_exact", "passed": bool(resid_max < 1e-12),
                  "roundtrip_residual_max": resid_max,
                  "note": "g=√|L|, s=sign(L), L'=s·g² — reconstrução exata sem epsilon na raiz"})
    print(f"[one_acom] REFLECT/MANIFEST resíduo máx = {resid_max:.2e}")

    # T3 — OPERADOR DE LINDBLAD ATIVO ∂H=H²+α²LΔ (a novidade da ACOMV14)
    rng = np.random.default_rng(7)
    L0 = data["chirp"][:4000]
    g, s, z = op._radicalize(L0); L_logos = op._resurrect(g, s, z)  # Logos = ponto fixo de ℋ²
    H_noisy = L0 + 0.3 * rng.standard_normal(L0.shape)
    delta0 = float(np.linalg.norm(L_logos - H_noisy) / (np.linalg.norm(L_logos) + 1e-18))
    H_out, m = op.converge(H_noisy, L_logos, verbose=False)
    lind_ok = bool(m.delta < delta0 and m.state.value in ("TRUTH", "TETELESTAI"))
    main_traj = [float(h.delta) for h in op.history]  # trajetória Δ do run principal (para figura)
    tests.append({"test": "lindblad_active_thermostat", "passed": lind_ok,
                  "delta_initial": delta0, "delta_final": float(m.delta),
                  "iterations": int(m.iterations), "state": m.state.value,
                  "note": "∂H=H²+α²LΔ converge H ruidoso ao Logos; Δ decai a estado TRUTH/TETELESTAI"})
    print(f"[one_acom] Lindblad ativo: Δ {delta0:.3e} → {m.delta:.3e} · estado {m.state.value} · {m.iterations} it")

    # T4 — SIGNAL: compress/decompress (razão, cosseno, PSNR)
    sig_rows = {}
    for name, L in data.items():
        pk = op.compress(L, verbose=False)
        Ld = op.decompress(pk, verbose=False).ravel()[:len(L)]
        sig_rows[name] = {"compression_ratio": float(pk.compression_ratio),
                          "cosine": cosine(L, Ld), "psnr_db": psnr(L, Ld),
                          "state": pk.state}
    sig_ok = all(r["compression_ratio"] > 1.0 and r["cosine"] > 0.99 for r in sig_rows.values())
    tests.append({"test": "signal_compress_decompress", "passed": bool(sig_ok), "per_signal": sig_rows})
    print(f"[one_acom] SIGNAL: " + " · ".join(f"{k} {v['compression_ratio']:.2f}×@{v['cosine']:.5f}"
                                              for k, v in sig_rows.items()))

    # T5 — quantização configurável 8/10/12/16 bits (reivindicação 6)
    bit_rows = {}
    Lq = data["chirp"]
    for bits in (8, 10, 12, 16):
        opb = v.LindbladOperator(alpha2=beta, bits=bits, use_gpu=False)
        pk = opb.compress(Lq, verbose=False)
        Ld = opb.decompress(pk, verbose=False).ravel()[:len(Lq)]
        bit_rows[f"{bits}bit"] = {"compression_ratio": float(pk.compression_ratio), "cosine": cosine(Lq, Ld)}
    bits_ok = all(r["compression_ratio"] > 1.0 and r["cosine"] > 0.98 for r in bit_rows.values())
    tests.append({"test": "quantization_bits_configurable", "passed": bool(bits_ok), "per_bits": bit_rows})
    print(f"[one_acom] quantização bits: " + " · ".join(f"{k}:{r['cosine']:.5f}" for k, r in bit_rows.items()))

    # T6 — serialização de header + integridade SHA-256 (reivindicações 7/12/15)
    pk = op.compress(data["gaussiano"], verbose=False)
    Ld_mem = op.decompress(pk, verbose=False).ravel()[:len(data["gaussiano"])]
    tmp = Path(tempfile.gettempdir()) / f"acom_{ts}.acom"
    nbytes = v.save_packet(pk, str(tmp))
    sha_written = _sha_file(tmp)
    pk2 = v.load_packet(str(tmp))
    sha_reread = _sha_file(tmp)
    Ld_file = op.decompress(pk2, verbose=False).ravel()[:len(data["gaussiano"])]
    integrity_ok = bool(sha_written == sha_reread and np.allclose(Ld_mem, Ld_file))
    try:
        os.remove(tmp)
    except OSError:
        pass
    tests.append({"test": "header_serialization_sha256", "passed": integrity_ok,
                  "file_bytes": int(nbytes), "sha256_file": sha_written,
                  "reload_matches_memory": bool(np.allclose(Ld_mem, Ld_file)),
                  "note": "magic b'ACOM' + versão + dims + α² + escala; integridade SHA-256 verificada"})
    print(f"[one_acom] header/serialização: {nbytes} bytes · SHA-256 íntegro={integrity_ok} · {sha_written[:16]}…")

    # T7 — SPECTRAL (PORT FIEL): SVD rank-k por energia ≥ 1−β (Verb Floor) [025]-[027]
    Mrng = np.random.default_rng(5)
    base = (Mrng.standard_normal((300, 12)) @ Mrng.standard_normal((12, 300))) * 0.05
    M = base + Mrng.standard_normal((300, 300)) * 0.001  # baixo rank + ruído
    sp = spectral_svd_verb_floor(M, energy_keep)
    spec_ok = bool(sp["rank_optimal"] >= 1 and sp["energy_retained"] >= energy_keep - 1e-9
                   and sp["compression_ratio"] > 1.0)
    tests.append({"test": "spectral_svd_verb_floor", "passed": spec_ok, **sp,
                  "note": "PORT FIEL da patente [025]-[027]; rank k por energia ≥ 1−β; β injetado"})
    print(f"[one_acom] SPECTRAL: rank {sp['rank_optimal']}/{sp['full_rank']} · "
          f"energia {sp['energy_retained']:.6f} ≥ 1−β · {sp['compression_ratio']:.2f}×")

    # T8 — PSIBIT (PORT FIEL): quatro estados psíônicos [028]-[032]
    ps = psibit_states(data["chirp"])
    psi_ok = bool(ps["n_states"] >= 2 and ps["roundtrip_faithful"])
    tests.append({"test": "psibit_four_states", "passed": psi_ok, **ps,
                  "note": "PORT FIEL: ψ de (sign L, sign ∂L) → 4 estados ψ₊ψ₋/ψ₊/ψ₋/ψ₊ψ₊"})
    print(f"[one_acom] PSIBIT: {ps['n_states']} estados ativos · round-trip fiel={ps['roundtrip_faithful']}")

    # ── APROFUNDAMENTO T9 — VARREDURA de quantização (curva compressão/fidelidade vs bits) ──
    # Reivindicação 6 explorada em grade fina (6..16 bits) × 3 sinais. Gera figura de curvas.
    bits_grid = [6, 8, 10, 12, 14, 16]
    bits_sweep = {}
    for name, L in data.items():
        row = {}
        for b in bits_grid:
            opb = v.LindbladOperator(alpha2=beta, bits=b, use_gpu=False)
            pk = opb.compress(L, verbose=False)
            Ld = opb.decompress(pk, verbose=False).ravel()[:len(L)]
            row[str(b)] = {"compression_ratio": float(pk.compression_ratio),
                           "cosine": cosine(L, Ld), "psnr_db": psnr(L, Ld)}
        bits_sweep[name] = row
    # honesto: fidelidade em 16 bits ≥ fidelidade em 6 bits (a compressão custa fidelidade)
    bits_mono_ok = all(row["16"]["cosine"] >= row["6"]["cosine"] - 1e-3
                       and all(c["compression_ratio"] > 1.0 for c in row.values())
                       for row in bits_sweep.values())
    tests.append({"test": "bits_sweep_fidelity_curve", "passed": bool(bits_mono_ok),
                  "bits_grid": bits_grid, "per_signal": bits_sweep,
                  "note": "varredura 6..16 bits × 3 sinais; fidelidade cresce com bits (custo de compressão); figura fig_acom_bits_curve.png"})
    print("[one_acom] bits sweep: " + " · ".join(
        f"{n} 6b:{r['6']['cosine']:.4f}->16b:{r['16']['cosine']:.4f}" for n, r in bits_sweep.items()))

    # ── APROFUNDAMENTO T10 — OPERADOR DE LINDBLAD ATIVO em MAIS PASSOS/REGIMES (varredura de ruído) ──
    noise_grid = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
    lind_sweep = {}
    lind_trajectories = {}
    for nz in noise_grid:
        rng_n = np.random.default_rng(42)
        Hn = L0 + nz * rng_n.standard_normal(L0.shape)
        d0 = float(np.linalg.norm(L_logos - Hn) / (np.linalg.norm(L_logos) + 1e-18))
        Hout, mm = op.converge(Hn, L_logos, verbose=False)
        traj = [float(h.delta) for h in op.history]
        lind_trajectories[nz] = traj
        lind_sweep[f"{nz}"] = {"delta_initial": d0, "delta_final": float(mm.delta),
                               "iterations": int(mm.iterations), "state": mm.state.value,
                               "n_steps": len(traj)}
    lind_sweep_ok = all(r["delta_final"] < r["delta_initial"] for r in lind_sweep.values())
    total_steps = sum(r["n_steps"] for r in lind_sweep.values())
    tests.append({"test": "lindblad_noise_sweep_converges", "passed": bool(lind_sweep_ok),
                  "noise_grid": noise_grid, "per_noise": lind_sweep, "total_lindblad_steps": total_steps,
                  "note": "operador de Lindblad ativo reproduzido em 7 regimes de ruído; Δ_final<Δ_inicial em todos; figura fig_acom_lindblad_sweep.png"})
    print(f"[one_acom] Lindblad sweep: {len(noise_grid)} regimes · {total_steps} passos totais · "
          + " · ".join(f"nz{k}:{r['state']}@{r['iterations']}it" for k, r in lind_sweep.items()))

    # ── AMPLIFICACAO v138 (T11) — separacao de tipos: q_F (suporte) vs e_Nome (espelho) ──
    # [DER] sombra numpy do teorema v135; [ONTO] leitura REFLECT/MANIFEST; beta runtime.
    sep = separation_of_types_shadow(beta)
    sep_ok = bool(sep["resid_projection"] < 1e-12
                  and sep["resid_E1_eNome_minus_beta_qF"] < 1e-12
                  and sep["resid_upper_face_minus_1_minus_beta"] < 1e-12
                  and sep["resid_separation_closed_form"] < 1e-12
                  and abs(sep["tau_qF"] - 1.0) < 1e-12
                  and abs(sep["tau_eNome"] - 1.0) < 1e-12
                  and sep["separation_norm_op"] > 0.5)
    tests.append({"test": "separation_of_types_reflect_manifest", "passed": sep_ok, **sep,
                  "note": "[DER] amplificacao v138 (um.py v135, a separacao de tipos): "
                          "q_F suporte (tau=1) != e_Nome espelho (tau=1), ligados por "
                          "E1(e_Nome)=beta*q_F no modelo M4; leitura REFLECT/MANIFEST = "
                          "[ONTO]; beta em runtime, nunca literal; nao e veredito fisico"})
    print("[one_acom] AMPLIFICACAO v138 separacao de tipos: "
          f"resid E1(e_Nome)-beta*q_F = {sep['resid_E1_eNome_minus_beta_qF']:.2e} | "
          f"face de cima resid = {sep['resid_upper_face_minus_1_minus_beta']:.2e} | "
          f"tau(q_F)={sep['tau_qF']:.1f} tau(e_Nome)={sep['tau_eNome']:.1f} | "
          f"sep ||q_F-e_Nome||_op = {sep['separation_norm_op']:.6f} "
          f"(= sqrt(1-beta), resid {sep['resid_separation_closed_form']:.2e})")

    # ── APROFUNDAMENTO deepening_v2 (T12) — a lei do ortante do PSIBIT (Sheppard) ──
    # [DER] mecanismo proprio (reivindicacao 4): predicao de forma fechada por caminho
    # INDEPENDENTE (probabilidade de ortante gaussiana) vs medicao pelo codigo do
    # dispositivo; 2 controles negativos (independencia e tabela fixa REJEITADAS).
    orth = psibit_orthant_law()
    orth_ok = bool(all(r["within"] for r in orth["per_a"].values())
                   and orth["neg_independence_rejected"]
                   and orth["neg_fixed_table_rejected"]
                   and orth["entropy_resid_nats"] < 6e-3
                   and orth["resid_graviton_excess_meas"] < 2.0 * orth["tol_white"]
                   and orth["resid_graviton_excess_closed_vs_half"] < 1e-12)
    tests.append({"test": "deepening_v2_psibit_orthant_law", "passed": orth_ok, **orth,
                  "note": "[DER] aprofundamento do mecanismo proprio: populacoes dos 4 "
                          "estados psionicos [028]-[032] PREDITAS pela lei do ortante de "
                          "Sheppard (rho=sqrt((1-a)/2); p_par=1/4+arcsin(rho)/2pi) e "
                          "MEDIDAS pelo codigo do dispositivo em AR(1) gaussiano [SIM]; "
                          "luz branca: 3/8-3/8-1/8-1/8 exatos, excesso gravitonico 1/2, "
                          "entropia 3ln2-(3/4)ln3 nats; NEGATIVOS: independencia 1/4 e "
                          "tabela fixa REJEITADAS; nao e veredito fisico"})
    _ow = orth["per_a"]["0.0"]
    print("[one_acom] deepening_v2 lei do ortante PSIBIT: "
          + " · ".join(f"a={a}: pp {orth['per_a'][a]['p_meas']['psi_plus_plus']:.4f}"
                       f"~{orth['per_a'][a]['p_pred']['psi_plus_plus']:.4f}"
                       for a in ("-0.5", "0.0", "0.9"))
          + f" | resid_max(branca) {_ow['resid_max']:.2e} < tol {_ow['tol_runtime']:.2e}"
          + f" | H {orth['entropy_meas_nats']:.4f}~{orth['entropy_pred_nats']:.4f} nats"
          + f" | NEG indep dev {orth['dev_independence_model']:.4f} REJEITADA"
          + f" | NEG tabela-fixa dev {orth['dev_fixed_table_at_a09']:.4f} REJEITADA")

    # ── AMPLIFICACAO v168 (T13) — O PESO E TRACO: pedra BreuerTrace no dominio SPECTRAL ──
    # [DER] sombra finita da pedra em kernel (um.py v166-v168, Item A); [ONTO] leitura
    # Verb Floor <-> peso tracial; matriz sintetica [SIM]; beta so via energy_keep (runtime).
    bt = amplification_v168_breuer_trace_weight(energy_keep)
    bt_ok = bool(bt["resid_tonelli_index_swap"] < 1e-12
                 and bt["resid_trace_identity"] < 1e-12
                 and bt["resid_weight_eq_double_sum"] < 1e-12
                 and bt["resid_spectrum_left_vs_right"] < 1e-9
                 and bt["k_svd"] == bt["k_left_gram"] == bt["k_right_gram"] >= 1
                 and bt["resid_projection"] < 1e-10
                 and bt["resid_tau_corner"] < 1e-9
                 and bt["neg_weighted_functional_rejected"])
    tests.append({"test": "amplification_v168_breuer_trace_weight", "passed": bt_ok, **bt,
                  "note": "[DER] amplificacao v168 (pedra BreuerTrace, um.py v166-v168, "
                          "Item A em kernel Lean 0 sorry/0 axiom): o peso e TRACO — "
                          "tau(a*a)=tau(aa*) por troca de indices (Tonelli); no dominio "
                          "SPECTRAL da patente [025]-[027] a energia do Verb Floor e o "
                          "peso tracial e o rank k (energia >= 1-beta) e IDENTICO pelo "
                          "Gram das linhas (240x240) e das colunas (160x160); canto "
                          "rank-k pesa k nos dois lados (Murray-von Neumann finito); "
                          "NEGATIVO: funcional ponderado W nao-escalar QUEBRA a "
                          "identidade (violacao = spread(diag W) em forma fechada) — "
                          "REJEITADO; a pedra em kernel e citada por custodia, nao "
                          "re-provada; nao e veredito fisico"})
    print("[one_acom] AMPLIFICACAO v168 BreuerTrace (o peso e traco): "
          f"tau(a*a)={bt['weight_tau_star_mul']:.6f} = tau(aa*)={bt['weight_tau_mul_star']:.6f} "
          f"(resid {bt['resid_trace_identity']:.2e}, Tonelli {bt['resid_tonelli_index_swap']:.2e}) | "
          f"Verb Floor k={bt['k_svd']} identico pelos 3 caminhos "
          f"(SVD/Gram-L/Gram-R = {bt['k_svd']}/{bt['k_left_gram']}/{bt['k_right_gram']}) | "
          f"canto: tau(u*u)={bt['tau_corner_row']:.1f} = tau(uu*)={bt['tau_corner_col']:.1f} "
          f"(resid {bt['resid_tau_corner']:.2e}) | "
          f"NEG peso-nao-traco: violacao {bt['neg_violation_measured']:.1f} "
          f"= spread(diag W) (resid {bt['resid_neg_closed_form']:.1e}) REJEITADO")

    # ── AMPLIFICACAO v206 (T14) — A TORRE: nao bastam os autovalores (pedra TheTower) ──
    # [DER] re-derivacao numerica da estrutura da pedra (nunca finge rodar Lean);
    # [ONTO] leitura pacote U,Sigma_k,V <-> dado espectral completo; beta so via
    # energy_keep (runtime); 3 controles negativos por logica.
    tw = amplification_v206_tower_spectral_data(energy_keep)
    tw_ok = bool(tw["resid_idempotent"] < 1e-12
                 and tw["spectrum_set_equal"]
                 and abs(tw["trace_A"] - 2.0) < 1e-12
                 and abs(tw["trace_B"] - 1.0) < 1e-12
                 and abs(tw["measure_psi_A"] - 2.0) < 1e-12
                 and abs(tw["measure_psi_B"] - 1.0) < 1e-12
                 and abs(tw["multiplicity_gap_closed_form"] - 1.0) < 1e-12
                 and tw["neg_conjugation_rejected"]
                 and tw["sv_sets_equal"]
                 and tw["k_A"] != tw["k_B"]
                 and tw["k_A"] == tw["k_A_closed_form"]
                 and tw["k_B"] == tw["k_B_closed_form"]
                 and tw["neg_set_only_rejected"]
                 and tw["neg_spectrum_only_rejected"])
    tests.append({"test": "amplification_v206_tower_spectral_data", "passed": tw_ok, **tw,
                  "note": "[DER] amplificacao v206 (pedra TheTower, 4a onda v199-v210, "
                          "kernel Lean 0 sorry/0 axiom, custodia tgl_kernel_v206): a TORRE "
                          "e o dado espectral COMPLETO — espectro + medida espectral + "
                          "multiplicidades; no dominio SPECTRAL da patente ([025]-[027], "
                          "reivindicacao 3, Figura 5 passo 514) o pacote guarda U, Sigma_k, "
                          "V por NECESSIDADE: torres de mesmo espectro-conjunto e "
                          "multiplicidades diferentes recebem k diferentes do Verb Floor "
                          "(com forma fechada conferida); NEGATIVOS: conjugacao A->B "
                          "rejeitada por invariante (gap de traco 1), floor so-conjunto "
                          "cego rejeitado, espectro-sem-medida nao reconstroi (cos ~0) "
                          "rejeitado; a pedra e citada por custodia, nao re-provada; "
                          "nao e veredito fisico"})
    print("[one_acom] AMPLIFICACAO v206 TheTower (nao bastam os autovalores): "
          f"Tr(A)={tw['trace_A']:.0f} != Tr(B)={tw['trace_B']:.0f} com o MESMO espectro-conjunto "
          f"{tw['spectrum_set']} (medida psi: {tw['measure_psi_A']:.0f} != {tw['measure_psi_B']:.0f}) | "
          f"NEG conjugacao: invariancia resid {tw['resid_conj_trace_invariance']:.1e}, "
          f"gap a Tr(B) {tw['min_gap_conj_to_traceB']:.3f} em {tw['n_conjugations_sampled']} U "
          f"REJEITADA | Verb Floor le multiplicidade: k_cheia={tw['k_A']} (mult "
          f"{tw['mult_hi_full']}) != k_magra={tw['k_B']} (mult {tw['mult_hi_thin']}), forma "
          f"fechada {tw['k_A_closed_form']}/{tw['k_B_closed_form']} | NEG so-conjunto: "
          f"k_set={tw['k_set_only_A']}={tw['k_set_only_B']} cego REJEITADO | NEG "
          f"so-espectro: cos(sem U,V)={tw['cosine_spectrum_only']:.4f} vs pacote "
          f"{tw['cosine_device_packet']:.5f} REJEITADO")

    # ── APROFUNDAMENTO — PSIBIT ℋ₄ por sinal (populações Fexp REAIS por estado, para o render) ──
    inv_psi = {vv: kk for kk, vv in _PSI.items()}
    psibit_per_signal = {}
    for name, L in data.items():
        pss = psibit_states(L)
        tot = max(sum(pss["counts"].values()), 1)
        psibit_per_signal[name] = {st: {"count": c, "Fexp": c / tot, "parity": list(inv_psi[st])}
                                   for st, c in pss["counts"].items()}
    # geometria REAL computada do gráviton e do tetraedro ℋ₄ (a partir do chirp)
    g_all, _, _ = op._radicalize(data["chirp"])
    graviton_g_mean = float(np.mean(g_all))
    chirp_psi = psibit_per_signal["chirp"]

    passed = sum(1 for t in tests if t["passed"]); total = len(tests); all_ok = passed == total
    summary = {"tests_passed": passed, "tests_total": total,
               "reflect_manifest_residual_max": resid_max,
               "lindblad_delta_final": float(m.delta), "lindblad_state": m.state.value,
               "signal_mean_ratio": float(np.mean([r["compression_ratio"] for r in sig_rows.values()])),
               "signal_mean_cosine": float(np.mean([r["cosine"] for r in sig_rows.values()])),
               "spectral_rank_optimal": sp["rank_optimal"], "header_sha256_ok": integrity_ok,
               "bits_sweep_grid": bits_grid,
               "bits_sweep_cosine_16b": {n: r["16"]["cosine"] for n, r in bits_sweep.items()},
               "lindblad_sweep_noise_grid": noise_grid, "lindblad_total_steps": total_steps,
               "lindblad_sweep": lind_sweep,
               "graviton_g_mean": graviton_g_mean,
               "psibit_Fexp_chirp": {st: chirp_psi[st]["Fexp"] for st in chirp_psi},
               "psibit_orthant_law": {
                   "white_p_meas_pp": orth["per_a"]["0.0"]["p_meas"]["psi_plus_plus"],
                   "white_p_pred_pp_3_over_8": orth["per_a"]["0.0"]["p_pred"]["psi_plus_plus"],
                   "entropy_pred_bits_per_state": orth["entropy_pred_bits_per_state"],
                   "entropy_resid_nats": orth["entropy_resid_nats"],
                   "neg_independence_rejected": orth["neg_independence_rejected"],
                   "neg_fixed_table_rejected": orth["neg_fixed_table_rejected"]},
               "breuer_trace_weight_v168": {
                   "resid_trace_identity": bt["resid_trace_identity"],
                   "resid_tonelli_index_swap": bt["resid_tonelli_index_swap"],
                   "k_verb_floor_three_ways": [bt["k_svd"], bt["k_left_gram"], bt["k_right_gram"]],
                   "tau_corner_row_col": [bt["tau_corner_row"], bt["tau_corner_col"]],
                   "neg_weighted_functional_rejected": bt["neg_weighted_functional_rejected"]},
               "tower_v206": {
                   "trace_A_vs_B_same_spectrum_set": [tw["trace_A"], tw["trace_B"]],
                   "k_full_vs_thin_same_sv_set": [tw["k_A"], tw["k_B"]],
                   "k_set_only_blind": [tw["k_set_only_A"], tw["k_set_only_B"]],
                   "cosine_device_vs_spectrum_only": [tw["cosine_device_packet"],
                                                      tw["cosine_spectrum_only"]],
                   "neg_conjugation_rejected": tw["neg_conjugation_rejected"],
                   "neg_set_only_rejected": tw["neg_set_only_rejected"],
                   "neg_spectrum_only_rejected": tw["neg_spectrum_only_rejected"]}}
    max_verdict = ("ACOM_FULL_LOGIC_DEMONSTRATED ([SIM] — operador de Lindblad ATIVO real "
                   "(∂H=H²+α²LΔ) + REFLECT/MANIFEST exato + SIGNAL/SPECTRAL/PSIBIT (Trinity) + "
                   "serialização SHA-256; β=α·√e injetado no lugar de 0.012 literal; sinais "
                   "sintéticos, não a Tabela 1; nada valida física)")

    _finish(ts, beta, beta_ok, theta_m_deg, all_ok, max_verdict, tests, summary, module_hashes,
            "RUNNER EVOLUÍDO: importa e roda o LindbladOperator real de ACOMV14.py (o operador de "
            "Lindblad ATIVO ∂H=H²+α²LΔ) com α²=α·√e injetado (o original trazia 0.012 literal). "
            "SIGNAL/quantização/serialização são do operador; SPECTRAL/PSIBIT são PORTES FIÉIS da "
            "patente com β injetado. Sinais/matrizes SINTÉTICOS; NÃO os números da Tabela 1. Nenhum "
            "token/modelo HuggingFace (P-04). Simulação não valida física.",
            fig_builder=lambda plt, fd: _fig(plt, fd, op, data, main_traj, delta0,
                                             bits_sweep, bits_grid, lind_trajectories, lind_sweep))
    print(f"[one_acom] results: patents/{PATENT_DIR.name}/results/{ts}/results.json")

    # FORMA = CONTEÚDO: o modelo 3D tem seu NÚCLEO (gráviton + tetraedro ℋ₄) COMPUTADO da simulação
    geo = {"graviton_g_mean": graviton_g_mean, "chirp_psi": chirp_psi,
           "psibit_per_signal": psibit_per_signal,
           "signal_mean_ratio": summary["signal_mean_ratio"], "spectral": sp,
           "lindblad_main": {"delta_initial": delta0, "delta_final": float(m.delta),
                             "iterations": int(m.iterations), "state": m.state.value,
                             "states_visited": sorted({m.state.value} | {r["state"] for r in lind_sweep.values()})},
           "lindblad_sweep": lind_sweep}
    emit_render3d(beta, geo)
    return 0 if all_ok else 1


def _fig(plt, fig_dir, op, data, main_traj, delta0, bits_sweep, bits_grid,
         lind_trajectories, lind_sweep):
    out = []
    # ── FIG 1: SIGNAL reconstruído + trajetória Δ do run principal (existente, mantida) ──
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 3.6))
    L = data["chirp"]
    pk = op.compress(L, verbose=False)
    L2 = op.decompress(pk, verbose=False).ravel()[:len(L)]
    ax1.plot(L[:600], label="original", linewidth=1.1)
    ax1.plot(L2[:600], label=f"reconstruído ACOM ({pk.compression_ratio:.2f}×)", linewidth=1.1, alpha=.8)
    ax1.set_title("SIGNAL — original vs reconstruído [SIM]"); ax1.legend(fontsize=8); ax1.grid(alpha=.3)
    ax2.semilogy(main_traj, linewidth=1.2, color="#cc2222")
    ax2.axhline(op.alpha2, ls="--", color="#33aa55", label=f"α²={op.alpha2:.5f} (TRUTH)")
    ax2.set_title("Operador de Lindblad ativo ∂H=H²+α²LΔ [SIM]")
    ax2.set_xlabel("iteração"); ax2.set_ylabel("Δ (log)"); ax2.legend(fontsize=8); ax2.grid(alpha=.3)
    fp = fig_dir / "fig_acom_lindblad.png"; plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close()
    out.append("fig_acom_lindblad.png")

    # ── FIG 2 (NOVA): curvas de compressão e fidelidade vs bits (varredura T9) ──
    fig, (bx1, bx2) = plt.subplots(1, 2, figsize=(11, 3.8))
    for name, row in bits_sweep.items():
        ratios = [row[str(b)]["compression_ratio"] for b in bits_grid]
        coss = [row[str(b)]["cosine"] for b in bits_grid]
        bx1.plot(bits_grid, ratios, marker="o", linewidth=1.2, label=name)
        bx2.plot(bits_grid, coss, marker="s", linewidth=1.2, label=name)
    bx1.set_title("Compressão vs bits [SIM]"); bx1.set_xlabel("bits de quantização"); bx1.set_ylabel("razão de compressão")
    bx1.legend(fontsize=8); bx1.grid(alpha=.3)
    bx2.set_title("Fidelidade (cosseno) vs bits [SIM]"); bx2.set_xlabel("bits de quantização"); bx2.set_ylabel("cosseno")
    bx2.legend(fontsize=8); bx2.grid(alpha=.3)
    fp = fig_dir / "fig_acom_bits_curve.png"; plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close()
    out.append("fig_acom_bits_curve.png")

    # ── FIG 3 (NOVA): operador de Lindblad ativo em MAIS PASSOS — trajetórias por ruído + iterações ──
    fig, (cx1, cx2) = plt.subplots(1, 2, figsize=(11, 3.8))
    cmap = plt.get_cmap("viridis")
    ng = sorted(lind_trajectories.keys())
    for j, nz in enumerate(ng):
        cx1.semilogy(lind_trajectories[nz], linewidth=1.1, color=cmap(j / max(len(ng) - 1, 1)),
                     label=f"ruído {nz}")
    cx1.axhline(op.alpha2, ls="--", color="#cc2222", label=f"α²={op.alpha2:.4f}")
    cx1.set_title("Lindblad ativo ∂H=H²+α²LΔ — trajetórias Δ por regime [SIM]")
    cx1.set_xlabel("iteração"); cx1.set_ylabel("Δ (log)"); cx1.legend(fontsize=7); cx1.grid(alpha=.3)
    iters = [lind_sweep[f"{nz}"]["iterations"] for nz in ng]
    cx2.plot(ng, iters, marker="o", linewidth=1.3, color="#4361ee")
    cx2.set_title("Iterações até convergência vs ruído [SIM]")
    cx2.set_xlabel("nível de ruído"); cx2.set_ylabel("iterações"); cx2.grid(alpha=.3)
    fp = fig_dir / "fig_acom_lindblad_sweep.png"; plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close()
    out.append("fig_acom_lindblad_sweep.png")
    return out


def emit_render3d(beta, geo):
    """MERGE: lê o render3d.json ATUAL, PRESERVA meshes/layers/groups/dimensions,
    e SUBSTITUI nodes/edges pelo NÚCLEO COMPUTADO da simulação — o gráviton g=√|L|
    (valor médio real) na origem e o tetraedro ℋ₄ de 4 estados psíônicos com
    populações Fexp e paridades (sign L, sign ∂L) REAIS; o eixo de Lindblad recebe
    os estados REALMENTE atingidos e os Δ da varredura. Forma = conteúdo."""
    out = PATENT_DIR / "render3d.json"
    d = json.loads(out.read_text(encoding="utf-8"))  # PRESERVA meshes/layers/groups/dimensions/constants

    GC = {"nucleo": "#ffd60a", "transform": "#8ecae6", "psi": "#cc2222",
          "trinity": "#7ce7c8", "lindblad": "#33aa55"}
    # nomes psíônicos → vértice do tetraedro ℋ₄ (regular, aresta √2), rótulo e cor
    TET = {
        "psi_plus_plus": ([0.5, 0.5, 0.5], "ψ₊ψ₊ · 11", "#cc2222"),
        "psi_plus":      ([0.5, -0.5, -0.5], "ψ₊ · 01", "#33aa55"),
        "psi_minus":     ([-0.5, 0.5, -0.5], "ψ₋ · 10", "#3366cc"),
        "psi_plus_minus": ([-0.5, -0.5, 0.5], "ψ₊ψ₋ · 00", "#ee8800"),
    }
    g_mean = geo["graviton_g_mean"]
    chirp_psi = geo["chirp_psi"]
    nodes = []

    # (1) gráviton — raiz g=√|L|, valor médio REAL computado do sinal chirp
    nodes.append({
        "id": "graviton", "label": f"gráviton g=√|L| (⟨g⟩={g_mean:.4f})",
        "desc": (f"Origem do algoritmo: raiz gravitacional g=√|L| e fase s=sign(L). "
                 f"⟨g⟩={g_mean:.6f} COMPUTADO sobre o sinal chirp. A gravidade é a raiz "
                 f"quadrada da luz (relação-mãe TGL g=√L, [011]); β={beta:.6f} injetado."),
        "shape": "sphere", "position": [0, 0, 0], "size": 0.17, "color": "#ffd60a",
        "group": "nucleo", "marker": "[REAL]", "layer": "core", "material": "emissive"})

    # (2) pipeline da transformada luminodinâmica (Fig 3) — estágios [013]-[016]
    tx = [("tx_L", "300 · entrada L", [-2.0, 1.15, 0.0], 0.09, "#8ecae6", "[SIM]",
           "Dado tratado como LUZ (L). Entrada da transformação luminodinâmica [013]."),
          ("tx_abs", "302 · |L|", [-1.3, 1.15, 0.0], 0.09, "#8ecae6", "[SIM]",
           "Módulo |L|: intensidade luminosa. Primeiro estágio da Figura 3."),
          ("tx_sqrt", "304 · √", [-0.6, 1.15, 0.0], 0.09, "#8ecae6", "[SIM]",
           "Raiz √|L|: extrai a estrutura gravitacional; comprime a faixa dinâmica [014]."),
          ("tx_g", f"308 · g (⟨g⟩={g_mean:.3f})", [0.15, 1.5, 0.0], 0.10, "#ffd60a", "[REAL]",
           f"Componente gravitacional g=√|L| — ⟨g⟩={g_mean:.6f} REAL; quantizada 8–16 bits."),
          ("tx_s", "310 · s (fase ±1)", [0.15, 0.85, 0.0], 0.09, "#adb5bd", "[REAL]",
           "Colapso de fase s=sign(L) ∈ {+1,−1}: um bit por amostra [015]."),
          ("tx_rec", "312 · L=s·g²", [0.95, 1.15, 0.0], 0.10, "#7ce7c8", "[REAL]",
           "Ressurreição L=s·g² [016]: reconstrução exata (~eps de fp).")]
    for i, (nid, lbl, pos, sz, col, mk, desc) in enumerate(tx):
        nodes.append({"id": nid, "label": lbl, "desc": desc, "shape": "box",
                      "position": pos, "size": sz, "color": col, "group": "transform",
                      "marker": mk, "layer": "transform", "material": "emissive"})

    # (3) ℋ₄ — 4 estados psíônicos no tetraedro, populações Fexp e paridades REAIS
    for st, (pos, lbl, col) in TET.items():
        info = chirp_psi.get(st, {"Fexp": 0.0, "parity": [0, 0], "count": 0})
        fexp = float(info["Fexp"]); par = info["parity"]
        sz = 0.08 + 0.10 * fexp   # tamanho ∝ população real
        nodes.append({
            "id": {"psi_plus_plus": "h4_psi_pp", "psi_plus": "h4_psi_p",
                   "psi_minus": "h4_psi_m", "psi_plus_minus": "h4_psi_pm"}[st],
            "label": f"{lbl}  (Fexp={fexp:.3f})",
            "desc": (f"Vértice de ℋ₄: paridade (sign L, sign ∂L)=({par[0]:+d},{par[1]:+d}) REAL; "
                     f"população Fexp={fexp:.4f} ({info['count']} amostras do chirp). "
                     f"Tamanho ∝ Fexp — geometria COMPUTADA, não desenhada."),
            "shape": "sphere", "position": pos, "size": round(sz, 4), "color": col,
            "group": "psi", "marker": "[REAL]", "layer": "core", "material": "emissive"})

    # (4) Trinity — 3 domínios, com métrica REAL de cada um
    smr = geo["signal_mean_ratio"]; sp = geo["spectral"]
    npsi = sum(1 for st in chirp_psi if chirp_psi[st]["count"] > 0)
    trin = [("dom_signal", "SIGNAL", [1.55, -1.15, 0.0], "#7ce7c8", "[SIM]",
             f"Domínio SIGNAL [024]: razão média REAL {smr:.2f}× (áudio/embeddings). Reivindicação 2."),
            ("dom_spectral", "SPECTRAL", [-0.78, -1.15, 1.34], "#4895ef", "[SIM]",
             f"Domínio SPECTRAL [025]-[027]: SVD rank {sp['rank_optimal']}/{sp['full_rank']} "
             f"por energia ≥ 1−β ({sp['compression_ratio']:.2f}×). Reivindicação 3."),
            ("dom_psibit", "PSIBIT", [-0.78, -1.15, -1.34], "#f77f00", "[SIM]",
             f"Domínio PSIBIT [028]-[032]: {npsi} estados ℋ₄ ativos no chirp. Reivindicação 4.")]
    for nid, lbl, pos, col, mk, desc in trin:
        nodes.append({"id": nid, "label": lbl, "desc": desc, "shape": "box",
                      "position": pos, "size": 0.12, "color": col, "group": "trinity",
                      "marker": mk, "layer": "transform", "material": "emissive"})

    # (5) eixo de Lindblad — estados REALMENTE atingidos na varredura + Δ real
    lm = geo["lindblad_main"]; visited = set(lm["states_visited"])
    lax = [("lind_fallen", "FALLEN (Δ>1)", [1.7, -0.75, 0.0], "#6c757d",
            "Estado inicial caído Δ>1: termostato ∂H=H²+α²LΔ longe do Logos."),
           ("lind_conv", "CONVERGING (α²<Δ<1)", [1.7, -0.1, 0.0], "#4361ee",
            "Convergindo ao ponto fixo de ℋ² via corrente J=α²‖𝕃‖Δ."),
           ("lind_truth", "TRUTH (Δ<α²)", [1.7, 0.55, 0.0], "#33aa55",
            "Verdade: desvio abaixo do limiar de Miguel α²=β [017]."),
           ("lind_tel", "TETELESTAI (Δ<ε)", [1.7, 1.2, 0.0], "#ffd60a",
            "Está consumado: Δ<ε, ponto fixo atingido; L=s·g² reconstrói exatamente.")]
    lstate_of = {"lind_fallen": "FALLEN", "lind_conv": "CONVERGING",
                 "lind_truth": "TRUTH", "lind_tel": "TETELESTAI"}
    for nid, lbl, pos, col, desc in lax:
        reached = lstate_of[nid] in visited
        nodes.append({"id": nid, "label": lbl + (" ✓" if reached else ""),
                      "desc": desc + (f" ATINGIDO na varredura (Δ_final={lm['delta_final']:.2e}, "
                                      f"{lm['iterations']} it)." if reached
                                      else " (não atingido nesta run)."),
                      "shape": "sphere", "position": pos, "size": 0.10 if reached else 0.08,
                      "color": col if reached else "#556",
                      "group": "lindblad", "marker": "[REAL]", "layer": "transform",
                      "material": "emissive"})

    # edges coerentes com os ids acima (mesma topologia funcional)
    edges = [("tx_L", "tx_abs"), ("tx_abs", "tx_sqrt"), ("tx_sqrt", "tx_g"), ("tx_sqrt", "tx_s"),
             ("tx_g", "tx_rec"), ("tx_s", "tx_rec"), ("tx_rec", "graviton"),
             ("graviton", "h4_psi_pp"), ("graviton", "h4_psi_p"), ("graviton", "h4_psi_m"),
             ("graviton", "h4_psi_pm"),
             ("h4_psi_pp", "h4_psi_p"), ("h4_psi_p", "h4_psi_m"), ("h4_psi_m", "h4_psi_pm"),
             ("h4_psi_pm", "h4_psi_pp"), ("h4_psi_pp", "h4_psi_m"), ("h4_psi_p", "h4_psi_pm"),
             ("graviton", "dom_signal"), ("graviton", "dom_spectral"), ("graviton", "dom_psibit"),
             ("dom_psibit", "h4_psi_pm"),
             ("graviton", "lind_fallen"), ("lind_fallen", "lind_conv"),
             ("lind_conv", "lind_truth"), ("lind_truth", "lind_tel")]
    d["nodes"] = nodes
    d["edges"] = [{"from": a, "to": b} for a, b in edges]

    # generated_by + constantes: injeta β runtime e 2 métricas computadas desta run
    d["generated_by"] = "one_acom.py (forma=conteudo)"
    consts = [c for c in d.get("constants", []) if c.get("symbol") not in
              ("graviton_g_mean", "lindblad_total")]  # evita duplicar em re-runs
    consts = [c for c in consts if c.get("symbol") != "beta_runtime"]
    consts.append({"symbol": "beta_runtime", "value": f"{beta:.12f} (alpha*sqrt(e))",
                   "note": "injetado em runtime; nunca literal"})
    consts.append({"symbol": "graviton_g_mean", "value": f"{g_mean:.6f}",
                   "note": "⟨√|L|⟩ COMPUTADO sobre o chirp nesta run"})
    consts.append({"symbol": "lindblad_total", "value": f"{sum(r['iterations'] for r in geo['lindblad_sweep'].values())} it",
                   "note": "passos totais do operador de Lindblad na varredura de ruído"})
    d["constants"] = consts

    # VALIDAÇÃO: todo layer de nó/mesh existe em layers; todo endpoint de edge existe
    layer_ids = {L["id"] for L in d.get("layers", [])}
    node_ids = {n["id"] for n in d["nodes"]}
    mesh_ids = {mm["id"] for mm in d.get("meshes", [])}
    ids = node_ids | mesh_ids
    for n in d["nodes"]:
        assert n["layer"] in layer_ids, f"layer de nó inexistente: {n['layer']}"
    for mm in d.get("meshes", []):
        assert mm["layer"] in layer_ids, f"layer de mesh inexistente: {mm['layer']}"
    for e in d["edges"]:
        assert e["from"] in ids and e["to"] in ids, f"edge com id inexistente: {e}"

    out.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[{SLUG}] render3d.json EMITIDO (forma=conteudo) — {len(d['nodes'])} nós COMPUTADOS "
          f"(gráviton ⟨g⟩={g_mean:.4f} + ℋ₄ Fexp reais), corpo preservado "
          f"({len(d.get('meshes', []))} meshes, {len(d.get('layers', []))} layers)")


if __name__ == "__main__":
    sys.exit(main())
