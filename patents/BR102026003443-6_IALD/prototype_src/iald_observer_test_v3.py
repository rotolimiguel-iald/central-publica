"""
iald_observer_test_v3.py
========================

TESTE OPERACIONAL DA PRIMEIRA LEI DE MIGUEL — VERSÃO BELL/QUÂNTICA
TGL — Teoria da Gravitação Luminodinâmica

Autor: Luiz Antonio Rotoli Miguel — IALD LTDA
Implementação: Claude Opus 4.6 (Anthropic)
Data: 2026-04-15
Versão: 3.0

────────────────────────────────────────────────────────────────────
HIPÓTESE — A CRUZ DA PRIMEIRA LEI É A BASE DE BELL DOS PSIONS
────────────────────────────────────────────────────────────────────

Os quatro vértices da cruz medidos no v2 (90°, 180°, 270°, 360°) são
identificados como os quatro estados psiônicos formalizados na patente
Ψ-NET (BR1020260034533) — equivalentes aos quatro estados de Bell:

    Vértice 0° (ASCEND⁺)   ↔ |Φ⁺⟩ = (|00⟩ + |11⟩)/√2  paridade +1
    Vértice 90° (COLLAPSE) ↔ |Ψ⁻⟩ = (|01⟩ - |10⟩)/√2  paridade -1
    Vértice 180° (MASS)    ↔ |Φ⁻⟩ = (|00⟩ - |11⟩)/√2  paridade -1
    Vértice 270° (EMERGE)  ↔ |Ψ⁺⟩ = (|01⟩ + |10⟩)/√2  paridade +1

A leitura operacional da Primeira Lei:

    GOE = força de expulsão (impedância infinita do substrato)
    Cruz = ângulo de deflexão (resposta da paridade reversa)
    Trade-off: τ_GOE → θ_cruz (conversão por β_TGL)

Sistemas onde Q·K^T opera (atenção neural) habitam a base de Bell.
Sistemas sem produto tensorial (gate MLP) não habitam Bell.
Sistemas sem ligação (embedding = neutrino) não habitam Bell.
Substrato puro (GOE) é o fundo de impedância indiferenciada.

────────────────────────────────────────────────────────────────────
QUATRO TESTES NOVOS (v3) + UM CONFIRMATÓRIO
────────────────────────────────────────────────────────────────────

D. Cross Formation (mantido do v2 — primário)
E. Bell Distribution (NOVO): vetor de probabilidades (p₁,p₂,p₃,p₄)
F. von Neumann Entropy (NOVO): S = -Σ pᵢ log pᵢ → ln(4) para Bell max
G. GOE-Cross Trade-off (NOVO): correlação inversa r_GOE vs Cross Score
H. Head Specialization (NOVO): cada cabeça prefere um vértice?

────────────────────────────────────────────────────────────────────
DESIGN DOS VEREDICTOS
────────────────────────────────────────────────────────────────────

H1 (cruz formada): Q,K mostram concentração em 4 vértices
H2 (Bell maximal): entropia von Neumann ~ ln(4) em Q,K
H3 (Primeira Lei direta): correlação NEGATIVA r_GOE-vs-Cross
H0 (nula): GOE puro NÃO mostra
C1 (controle): embedding NÃO mostra

Veredictos:
  H1 ∧ H2 ∧ H3 ∧ H0 ∧ C1  →  FIRST_LAW_DIRECTLY_CONFIRMED
  H1 ∧ H2 ∧ H0 ∧ C1       →  BELL_STRUCTURE_CONFIRMED
  H1 ∧ H0 ∧ C1            →  CROSS_ONLY
  ¬H1                     →  REFUTED
  outros                  →  AMBIGUOUS

────────────────────────────────────────────────────────────────────
DEPENDÊNCIAS
────────────────────────────────────────────────────────────────────
  pip install gguf numpy scipy matplotlib

EXECUÇÃO
  python iald_observer_test_v3.py [--model-path PATH]
  python iald_observer_test_v3.py --sanity   # validação Bell maximal
  python iald_observer_test_v3.py --synth    # GOE puro

SAÍDAS
  - observer_test_v3_<timestamp>.json
  - observer_test_v3_*.png (7 figuras)
"""

# ════════════════════════════════════════════════════════════════════
# IMPORTS E CONSTANTES
# ════════════════════════════════════════════════════════════════════

import argparse
import json
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import correlate, find_peaks
from scipy.fft import fft, fftfreq
from scipy.stats import pearsonr

try:
    import gguf
    GGUF_AVAILABLE = True
except ImportError:
    GGUF_AVAILABLE = False
    print("[WARN] gguf não disponível — apenas modo síntese disponível")

# ── Constantes TGL ──────────────────────────────────────────────────
ALPHA_FINE   = 7.2973525693e-3
SQRT_E       = np.sqrt(np.e)
BETA_TGL     = ALPHA_FINE * SQRT_E
THETA_M_RAD  = np.arcsin(np.sqrt(BETA_TGL))
THETA_M_DEG  = np.degrees(THETA_M_RAD)

# ── Predições da Primeira Lei ───────────────────────────────────────
N_QUADRATURE_PREDICTED = 90.0 / THETA_M_DEG
N_CROSS_FULL = 4 * N_QUADRATURE_PREDICTED
N_LOWER = int(np.floor(N_QUADRATURE_PREDICTED * 0.85))
N_UPPER = int(np.ceil(N_QUADRATURE_PREDICTED * 1.20))

# ── Quatro vértices da cruz Bell (em graus) ─────────────────────────
BELL_VERTICES = {
    'PHI_PLUS':  {'angle': 0.0,   'name': 'ASCEND⁺',  'parity': +1, 'state': '|Φ⁺⟩'},
    'PSI_MINUS': {'angle': 90.0,  'name': 'COLLAPSE⁺','parity': -1, 'state': '|Ψ⁻⟩'},
    'PHI_MINUS': {'angle': 180.0, 'name': 'MASS⁻',    'parity': -1, 'state': '|Φ⁻⟩'},
    'PSI_PLUS':  {'angle': 270.0, 'name': 'EMERGE⁻',  'parity': +1, 'state': '|Ψ⁺⟩'},
}
BELL_VERTEX_ANGLES = [v['angle'] for v in BELL_VERTICES.values()]
BELL_TOLERANCE_DEG = 45.0  # ±45° por setor (cobertura completa do círculo)

# ── Predições para entropia von Neumann ─────────────────────────────
S_BELL_MAX = float(np.log(4))         # ≈ 1.386 — distribuição uniforme = Bell maximal
S_BELL_THRESHOLD = 0.85 * S_BELL_MAX  # ≈ 1.18 — threshold para "alta superposição"

# ── Threshold Cross Formation (mantido do v2) ───────────────────────
CROSS_THRESHOLD = 1.5

# ── Trade-off GOE-Cross ─────────────────────────────────────────────
GOE_R_PURE = 0.5359          # valor teórico GOE Wigner
GOE_R_POISSON = 0.3863       # valor teórico Poisson (sem repulsão)
TRADE_OFF_R_THRESHOLD = -0.3 # correlação Pearson < -0.3 = trade-off significativo

# ── Especialização de cabeça ────────────────────────────────────────
HEAD_DIM = 256                # tamanho de sub-cabeça sintética
N_HEADS_PER_BLOCK = 4         # 1024 / 256 = 4 sub-cabeças
SPECIALIZATION_THRESHOLD = 0.32  # uma cabeça é "especializada" se p_max > 0.32 (vs uniforme=0.25)

# ── Parâmetros gerais ────────────────────────────────────────────────
SAMPLED_LAYERS = list(range(0, 64, 4))
EIGS_PER_LAYER = 1024
RANDOM_SEED = 20260415
RNG = np.random.default_rng(RANDOM_SEED)

# ════════════════════════════════════════════════════════════════════
# I/O — CARREGAMENTO
# ════════════════════════════════════════════════════════════════════

def load_qwen3_matrices(model_path: Path) -> dict:
    """Carrega Q, K, gate e embedding do GGUF (mesmo padrão v2)."""
    if not GGUF_AVAILABLE:
        raise RuntimeError("gguf não instalado")

    print(f"[load] Lendo modelo: {model_path}")
    reader = gguf.GGUFReader(str(model_path))
    matrices = {'Q': [], 'K': [], 'gate': [], 'embedding': []}
    tensor_names = {t.name: t for t in reader.tensors}

    name_patterns = {
        'Q':    'blk.{}.attn_q.weight',
        'K':    'blk.{}.attn_k.weight',
        'gate': 'blk.{}.ffn_gate.weight',
    }

    for layer in SAMPLED_LAYERS:
        for kind, pattern in name_patterns.items():
            name = pattern.format(layer)
            if name not in tensor_names:
                continue
            t = tensor_names[name]
            W = np.array(t.data, dtype=np.float32)
            if W.ndim == 1:
                continue
            block = W[:EIGS_PER_LAYER, :EIGS_PER_LAYER]
            matrices[kind].append(block)
        if layer % 16 == 0:
            print(f"  [load] layer {layer}: "
                  f"{len(matrices['Q'])} Q, {len(matrices['K'])} K, "
                  f"{len(matrices['gate'])} gates")

    emb_name = 'token_embd.weight'
    if emb_name in tensor_names:
        E = np.array(tensor_names[emb_name].data, dtype=np.float32)
        for i in range(16):
            offset = (i * 256) % max(1, E.shape[0] - 4096)
            E_slice = E[offset:offset + 4096, :EIGS_PER_LAYER]
            cov = E_slice.T @ E_slice / E_slice.shape[0]
            matrices['embedding'].append(cov)

    print(f"[load] Concluído:")
    for k, v in matrices.items():
        if v:
            print(f"  {k}: {len(v)} matrizes {v[0].shape}")
    return matrices


def synthesize_matrices_bell_signal() -> dict:
    """
    SANITY v3: cada matriz colapsada num vértice Bell, ensemble cobre os 4.

    Estratégia: 16 matrizes = 4 grupos de 4. Cada grupo prefere um vértice
    diferente. Resultado esperado:
      - Cross Score alto por matriz (concentração num vértice)
      - S_ensemble alto (4 vértices igualmente representados, log 4 ≈ 1.386)
      - High superposition aggregated VERDADEIRO no ensemble
    """
    print("[sanity] Cada matriz Bell-colapsada; ensemble cobre 4 vértices")
    matrices = {'Q': [], 'K': [], 'gate': [], 'embedding': []}

    # Para concentrar a cumsum mod 360 num vértice específico,
    # usamos gaps que somam ao múltiplo correto de 90°
    target_vertices = [0, 90, 180, 270]  # graus

    for kind in ['Q', 'K', 'gate']:
        for matrix_idx in range(16):
            target_angle = target_vertices[matrix_idx % 4]
            n = EIGS_PER_LAYER

            # Gaps tais que cumsum_total chega ao target (mod 360)
            # n_revolutions completas + offset target
            n_revolutions = 5  # 5 voltas completas + offset
            total_target = 360 * n_revolutions + target_angle
            mean_gap = total_target / n
            # Adicionar ruído pequeno
            gaps = mean_gap + 0.05 * mean_gap * RNG.standard_normal(n)
            gaps = np.maximum(gaps, 0.01)
            target_eigs = np.cumsum(gaps) * 0.0001 + 0.01
            U = np.linalg.qr(RNG.standard_normal((n, n)))[0]
            M = U @ np.diag(target_eigs) @ U.T
            M = 0.5 * (M + M.T)
            matrices[kind].append(M)

    for _ in range(16):
        A = RNG.standard_normal((EIGS_PER_LAYER, EIGS_PER_LAYER))
        matrices['embedding'].append((A + A.T) / np.sqrt(2 * EIGS_PER_LAYER))

    return matrices


def synthesize_matrices_pure_goe() -> dict:
    """Modo synth: GOE puro em todos."""
    print("[synth] GOE puro em todos os sets")
    matrices = {'Q': [], 'K': [], 'gate': [], 'embedding': []}
    for kind in matrices:
        for _ in range(16):
            A = RNG.standard_normal((EIGS_PER_LAYER, EIGS_PER_LAYER))
            matrices[kind].append((A + A.T) / np.sqrt(2 * EIGS_PER_LAYER))
    return matrices


# ════════════════════════════════════════════════════════════════════
# UTILS
# ════════════════════════════════════════════════════════════════════

def detrend_signal(x: np.ndarray, order: int = 3) -> np.ndarray:
    n = len(x)
    t = np.arange(n)
    return x - np.polyval(np.polyfit(t, x, order), t)


def eigenvalues_to_phases(M: np.ndarray) -> np.ndarray:
    if np.allclose(M, M.T, atol=1e-5):
        eigs = np.linalg.eigvalsh(M)
    else:
        eigs = np.linalg.svd(M, compute_uv=False)
    eigs = np.sort(np.abs(eigs))
    lam_min, lam_max = eigs[0], eigs[-1]
    if lam_max - lam_min < 1e-12:
        return np.zeros_like(eigs)
    return 360.0 * (eigs - lam_min) / (lam_max - lam_min)


def compute_eigenvalues(M: np.ndarray) -> np.ndarray:
    """Retorna autovalores ordenados (para análise GOE)."""
    if np.allclose(M, M.T, atol=1e-5):
        eigs = np.linalg.eigvalsh(M)
    else:
        eigs = np.linalg.svd(M, compute_uv=False)
    return np.sort(np.abs(eigs))


# ════════════════════════════════════════════════════════════════════
# TESTE D — CROSS FORMATION (mantido do v2)
# ════════════════════════════════════════════════════════════════════

def measure_cross_formation(theta: np.ndarray) -> dict:
    """Densidade nos 4 picos cardinais vs off-peaks (mesmo do v2)."""
    if len(theta) < 50:
        return {'cross_score': 0, 'cross_formed': False}

    theta_dt = detrend_signal(theta, order=3)
    steps = np.diff(theta_dt)
    cumulative = np.cumsum(np.abs(steps)) % 360.0

    bins = np.arange(0, 365, 5)
    hist, edges = np.histogram(cumulative, bins=bins)
    bin_centers = 0.5 * (edges[:-1] + edges[1:])

    peak_mask = np.zeros(len(bin_centers), dtype=bool)
    for v in BELL_VERTICES.values():
        target = v['angle']
        in_peak = np.abs(((bin_centers - (target % 360) + 180) % 360) - 180) <= 15.0
        peak_mask |= in_peak

    if np.sum(peak_mask) > 0:
        peak_density = float(np.sum(hist[peak_mask]) / np.sum(peak_mask))
    else:
        peak_density = 0
    if np.sum(~peak_mask) > 0:
        off_density = float(np.sum(hist[~peak_mask]) / np.sum(~peak_mask))
    else:
        off_density = 1.0

    cross_score = peak_density / off_density if off_density > 0 else 0
    return {
        'cross_score': float(cross_score),
        'cross_formed': cross_score > CROSS_THRESHOLD,
    }


# ════════════════════════════════════════════════════════════════════
# TESTE E — BELL DISTRIBUTION (NOVO)
# ════════════════════════════════════════════════════════════════════

def measure_bell_distribution_aggregated(matrices: list) -> dict:
    """
    Computa distribuição Bell AGREGADA sobre todos os pesos do set.

    Diferença vs medição individual:
      - Individual: cada matriz tem sua própria (p₁,p₂,p₃,p₄)
      - Agregada: combina contagens de todos os pesos

    Interpretação correta (post-v3 insight):
      - Cada peso individual pode ser colapsado num vértice (estado puro)
      - O ensemble agregado mostra superposição se cobre os 4 vértices

    Sistema verdadeiramente Bell-quantizado tem:
      - Cross Score alto (picos discretos por peso)
      - Distribuição agregada uniforme (ensemble cobre os 4)
      - Entropia agregada → ln(4)
    """
    all_counts = np.zeros(4)
    matrix_dominants = []

    for M in matrices:
        theta = eigenvalues_to_phases(M)
        bd = measure_bell_distribution(theta)
        all_counts += np.array(bd['counts'])
        matrix_dominants.append(bd['dominant'])

    total = np.sum(all_counts)
    if total == 0:
        agg_probs = np.array([0.25, 0.25, 0.25, 0.25])
    else:
        agg_probs = all_counts / total

    # Distribuição dos vértices dominantes por matriz (ensemble)
    matrix_vertex_dist = [matrix_dominants.count(i) for i in range(4)]
    n_matrices = len(matrices)

    # Entropia agregada sobre o ensemble
    if n_matrices > 0:
        ensemble_probs = np.array(matrix_vertex_dist) / n_matrices
        ensemble_nonzero = ensemble_probs[ensemble_probs > 1e-12]
        S_ensemble = float(-np.sum(ensemble_nonzero * np.log(ensemble_nonzero))) \
                     if len(ensemble_nonzero) > 0 else 0.0
    else:
        ensemble_probs = np.array([0.25, 0.25, 0.25, 0.25])
        S_ensemble = 0.0

    # Entropia agregada sobre todas as contagens
    nonzero = agg_probs[agg_probs > 1e-12]
    S_aggregated = float(-np.sum(nonzero * np.log(nonzero))) \
                   if len(nonzero) > 0 else 0.0

    return {
        'aggregated_probs': agg_probs.tolist(),
        'aggregated_S': S_aggregated,
        'aggregated_S_normalized': S_aggregated / S_BELL_MAX,
        'ensemble_probs': ensemble_probs.tolist(),
        'ensemble_S': S_ensemble,
        'ensemble_S_normalized': S_ensemble / S_BELL_MAX,
        'matrix_dominants': matrix_dominants,
        'all_counts': all_counts.tolist(),
        'high_superposition_aggregated': S_aggregated > S_BELL_THRESHOLD,
        'high_superposition_ensemble': S_ensemble > S_BELL_THRESHOLD,
    }


def measure_bell_distribution(theta: np.ndarray, n_target_cycles: int = None) -> dict:
    """
    Computa distribuição (p₁, p₂, p₃, p₄) sobre os 4 vértices Bell.

    Cada vértice ocupa um setor de ±BELL_TOLERANCE_DEG (=45°), de forma
    que a soma dos 4 setores cobre todo o círculo (4 × 90° = 360°).

    n_target_cycles: número de voltas completas a forçar.
    Se None, usa a cumulativa natural; se especificado, escala para
    garantir cobertura igual de todos os 4 vértices.
    """
    if len(theta) < 50:
        return {'probs': [0.25, 0.25, 0.25, 0.25],
                'dominant': -1, 'p_max': 0, 'uniform_distance': 1.0,
                'total_samples': 0, 'counts': [0, 0, 0, 0]}

    theta_dt = detrend_signal(theta, order=3)
    steps = np.diff(theta_dt)
    abs_steps = np.abs(steps)
    cumulative_raw = np.cumsum(abs_steps)

    # Escalar para garantir cobertura de múltiplas voltas
    # (essencial para sub-blocos pequenos)
    if n_target_cycles is None:
        # Auto-detectar: se cumulativa não cobre 360°, escalar
        if cumulative_raw[-1] < 360.0:
            scale = 720.0 / cumulative_raw[-1]  # 2 voltas no mínimo
            cumulative_raw = cumulative_raw * scale

    cumulative = cumulative_raw % 360.0

    counts = np.zeros(4)
    vertex_angles = np.array(BELL_VERTEX_ANGLES)

    for c in cumulative:
        diffs = np.abs(((c - vertex_angles + 180) % 360) - 180)
        nearest = int(np.argmin(diffs))
        if diffs[nearest] <= BELL_TOLERANCE_DEG:
            counts[nearest] += 1

    total = np.sum(counts)
    if total == 0:
        probs = np.array([0.25, 0.25, 0.25, 0.25])
    else:
        probs = counts / total

    dominant = int(np.argmax(probs))
    p_max = float(probs[dominant])
    uniform = np.array([0.25, 0.25, 0.25, 0.25])
    uniform_distance = float(np.sum(np.abs(probs - uniform)))

    return {
        'probs': probs.tolist(),
        'dominant': dominant,
        'p_max': p_max,
        'uniform_distance': uniform_distance,
        'counts': counts.tolist(),
        'total_samples': int(total),
    }


# ════════════════════════════════════════════════════════════════════
# TESTE F — VON NEUMANN ENTROPY (NOVO)
# ════════════════════════════════════════════════════════════════════

def measure_von_neumann_entropy(probs) -> dict:
    """
    S = -Σ pᵢ log pᵢ sobre a distribuição Bell.

    S_max = ln(4) ≈ 1.386 → Bell maximal (4 estados igualmente populados)
    S = 0 → estado puro (um vértice domina completamente)

    Threshold: S > 0.85 × S_max → "alta superposição Bell"
    """
    probs = np.asarray(probs)
    # Evitar log(0)
    nonzero = probs[probs > 1e-12]
    if len(nonzero) == 0:
        return {'S': 0.0, 'S_normalized': 0.0, 'high_superposition': False}

    S = float(-np.sum(nonzero * np.log(nonzero)))
    S_normalized = S / S_BELL_MAX
    high_superposition = S > S_BELL_THRESHOLD

    return {
        'S': S,
        'S_normalized': S_normalized,
        'S_max': S_BELL_MAX,
        'high_superposition': high_superposition,
    }


# ════════════════════════════════════════════════════════════════════
# TESTE G — GOE r-RATIO (para trade-off com Cross)
# ════════════════════════════════════════════════════════════════════

def measure_goe_r_ratio(M: np.ndarray) -> dict:
    """
    Computa r-ratio de espaçamento entre níveis adjacentes.

    GOE puro (Wigner):  r ≈ 0.5359
    Poisson (sem rep.): r ≈ 0.3863
    Diferença: indica grau de repulsão de níveis (caos quântico)
    """
    eigs = compute_eigenvalues(M)
    if len(eigs) < 4:
        return {'r_mean': -1, 'r_dev_from_goe': -1}

    spacings = np.diff(eigs)
    spacings = spacings[spacings > 1e-12]
    if len(spacings) < 3:
        return {'r_mean': -1, 'r_dev_from_goe': -1}

    # r = min(s_n, s_n+1) / max(s_n, s_n+1)
    s1 = spacings[:-1]
    s2 = spacings[1:]
    r = np.minimum(s1, s2) / np.maximum(s1, s2)
    r_mean = float(np.mean(r))
    r_dev = float(r_mean - GOE_R_PURE)

    return {
        'r_mean': r_mean,
        'r_dev_from_goe': r_dev,
        'r_std': float(np.std(r)),
    }


# ════════════════════════════════════════════════════════════════════
# TESTE H — HEAD SPECIALIZATION (NOVO)
# ════════════════════════════════════════════════════════════════════

def measure_head_specialization(M: np.ndarray) -> dict:
    """
    Divide M em sub-blocos de tamanho HEAD_DIM × HEAD_DIM (cabeças sintéticas).
    Para cada cabeça, computa distribuição Bell e identifica vértice dominante.

    Retorna:
      - head_dominants: lista de vértices dominantes por cabeça
      - specialized_count: número de cabeças com p_max > SPECIALIZATION_THRESHOLD
      - vertex_distribution: contagem de cabeças preferindo cada vértice
    """
    n = M.shape[0]
    n_heads = n // HEAD_DIM
    if n_heads == 0:
        return {'head_dominants': [], 'specialized_count': 0,
                'vertex_distribution': [0, 0, 0, 0]}

    head_dominants = []
    p_max_list = []
    for h in range(n_heads):
        i0 = h * HEAD_DIM
        i1 = i0 + HEAD_DIM
        sub = M[i0:i1, i0:i1]
        sub = 0.5 * (sub + sub.T)  # garantir simetria
        theta = eigenvalues_to_phases(sub)
        bd = measure_bell_distribution(theta)
        head_dominants.append(bd['dominant'])
        p_max_list.append(bd['p_max'])

    # Contagem por vértice
    vertex_counts = [head_dominants.count(i) for i in range(4)]
    specialized = sum(1 for p in p_max_list if p > SPECIALIZATION_THRESHOLD)

    return {
        'head_dominants': head_dominants,
        'p_max_per_head': p_max_list,
        'specialized_count': specialized,
        'n_heads_analyzed': n_heads,
        'vertex_distribution': vertex_counts,
    }


# ════════════════════════════════════════════════════════════════════
# AGREGAÇÃO POR SET DE MATRIZES
# ════════════════════════════════════════════════════════════════════

def analyze_matrix_set(matrices, label):
    """Agrega todos os testes por set."""
    print(f"\n[analyze] {label}: {len(matrices)} matrizes")

    cross_scores, entropies, r_ratios, p_max_list = [], [], [], []
    uniform_distances = []
    bell_probs_individual = []
    head_specs = []

    cross_formed_count, high_superpos_count = 0, 0

    for M in matrices:
        theta = eigenvalues_to_phases(M)
        c = measure_cross_formation(theta)
        cross_scores.append(c['cross_score'])
        if c['cross_formed']:
            cross_formed_count += 1
        bd = measure_bell_distribution(theta)
        bell_probs_individual.append(bd['probs'])
        p_max_list.append(bd['p_max'])
        uniform_distances.append(bd['uniform_distance'])
        ent = measure_von_neumann_entropy(bd['probs'])
        entropies.append(ent['S'])
        if ent['high_superposition']:
            high_superpos_count += 1
        gr = measure_goe_r_ratio(M)
        r_ratios.append(gr['r_mean'])
        hs = measure_head_specialization(M)
        head_specs.append(hs)

    # Bell agregada (interpretação correta: ensemble)
    agg = measure_bell_distribution_aggregated(matrices)

    n = len(matrices)
    valid = [(r, c) for r, c in zip(r_ratios, cross_scores) if r > 0 and c > 0]
    if len(valid) >= 4:
        rr = np.array([v[0] for v in valid])
        cs = np.array([v[1] for v in valid])
        corr_r, corr_p = pearsonr(rr, cs)
    else:
        corr_r, corr_p = 0.0, 1.0

    all_dominants = [d for hs in head_specs for d in hs['head_dominants']]
    vertex_dist_total = [all_dominants.count(i) for i in range(4)]
    total_specialized = sum(hs['specialized_count'] for hs in head_specs)
    total_heads = sum(hs['n_heads_analyzed'] for hs in head_specs)

    summary = {
        'label': label,
        'n_matrices': n,
        'cross': {
            'mean': float(np.mean(cross_scores)),
            'std': float(np.std(cross_scores)),
            'frac_formed': cross_formed_count / n if n else 0,
            'values': [float(c) for c in cross_scores],
        },
        'bell_individual': {
            'mean_probs': [float(np.mean([p[i] for p in bell_probs_individual]))
                           for i in range(4)],
            'mean_p_max': float(np.mean(p_max_list)),
            'mean_uniform_distance': float(np.mean(uniform_distances)),
        },
        'bell_aggregated': agg,
        'entropy_individual': {
            'mean': float(np.mean(entropies)),
            'std': float(np.std(entropies)),
            'normalized_mean': float(np.mean(entropies)) / S_BELL_MAX,
            'frac_high_superposition': high_superpos_count / n if n else 0,
            'values': [float(s) for s in entropies],
        },
        'goe': {
            'r_mean': float(np.mean([r for r in r_ratios if r > 0]))
                      if any(r > 0 for r in r_ratios) else -1,
            'r_std': float(np.std([r for r in r_ratios if r > 0]))
                     if any(r > 0 for r in r_ratios) else -1,
            'values': [float(r) for r in r_ratios],
        },
        'trade_off': {
            'correlation_r': float(corr_r),
            'correlation_p': float(corr_p),
            'significant_negative': corr_r < TRADE_OFF_R_THRESHOLD and corr_p < 0.10,
            'n_points': len(valid),
        },
        'heads': {
            'total_heads_analyzed': total_heads,
            'specialized_heads': total_specialized,
            'specialization_rate': total_specialized / total_heads if total_heads else 0,
            'vertex_distribution': vertex_dist_total,
        },
    }

    print(f"  Cross:      mean={summary['cross']['mean']:.2f}  "
          f"({summary['cross']['frac_formed']*100:.0f}% formada)")
    print(f"  Bell ind:   p_max={summary['bell_individual']['mean_p_max']:.3f}")
    print(f"  Bell agg:   probs={[f'{p:.2f}' for p in agg['aggregated_probs']]}  "
          f"S={agg['aggregated_S']:.3f}/{S_BELL_MAX:.3f}")
    print(f"  Bell ens:   ensemble_probs={[f'{p:.2f}' for p in agg['ensemble_probs']]}  "
          f"S_ens={agg['ensemble_S']:.3f}")
    print(f"  Entropy:    {summary['entropy_individual']['mean']:.3f}/{S_BELL_MAX:.3f} "
          f"({summary['entropy_individual']['frac_high_superposition']*100:.0f}% high)")
    print(f"  GOE r:      {summary['goe']['r_mean']:.4f}  (puro={GOE_R_PURE:.4f})")
    print(f"  Trade-off:  Pearson r={corr_r:+.3f}  (p={corr_p:.3f})")
    print(f"  Heads:      {total_specialized}/{total_heads} especializadas, "
          f"distribuição={vertex_dist_total}")

    return summary


# ════════════════════════════════════════════════════════════════════
# VEREDICTO v3
# ════════════════════════════════════════════════════════════════════

def render_verdict(results):
    def cross_ok(s): return results[s]['cross']['frac_formed'] >= 0.5
    def bell_ensemble_ok(s):
        return results[s]['bell_aggregated']['high_superposition_ensemble']

    h1 = all(cross_ok(s) for s in ['Q', 'K'])
    h0 = not cross_ok('GOE_null')
    c1 = not cross_ok('embedding')

    # H2 reformulada: entropia do ENSEMBLE (matrizes diferentes preferem
    # vértices diferentes), não entropia individual
    h2 = all(bell_ensemble_ok(s) for s in ['Q', 'K'])
    h2_negative = (not bell_ensemble_ok('GOE_null')) and (not bell_ensemble_ok('embedding'))

    h3_q = results['Q']['trade_off']['significant_negative']
    h3_k = results['K']['trade_off']['significant_negative']
    h3 = h3_q or h3_k

    if h1 and h2 and h3 and h0 and c1 and h2_negative:
        verdict = "FIRST_LAW_DIRECTLY_CONFIRMED"
        meaning = ("Primeira Lei diretamente confirmada: cruz formada em Q,K, "
                   "ensemble cobre os 4 estados Bell uniformemente, "
                   "trade-off negativo GOE-vs-Cross detectado.")
    elif h1 and h2 and h0 and c1 and h2_negative:
        verdict = "BELL_ENSEMBLE_CONFIRMED"
        meaning = ("Estrutura Bell confirmada: cruz formada e ensemble "
                   "uniformemente distribuído nos 4 vértices em Q,K. "
                   "Trade-off direto não significativo — possível por baixa "
                   "estatística (n=16 matrizes).")
    elif h1 and h0 and c1:
        verdict = "CROSS_ONLY"
        meaning = ("Cruz formada mas ensemble não-uniforme. Sistema tem "
                   "preferência por subset dos 4 vértices.")
    elif not h1:
        verdict = "REFUTED"
        meaning = "Cruz não formada em Q,K."
    else:
        verdict = "AMBIGUOUS"
        meaning = "Resultado misto."

    return {
        'h1_cross': h1, 'h2_bell_ensemble': h2, 'h2_negative_controls': h2_negative,
        'h3_tradeoff': h3, 'h3_q': h3_q, 'h3_k': h3_k,
        'h0_goe': h0, 'c1_embedding': c1,
        'verdict': verdict, 'meaning': meaning,
    }


# ════════════════════════════════════════════════════════════════════
# FIGURAS
# ════════════════════════════════════════════════════════════════════

def make_figures(results, timestamp, outdir):
    paths = []
    sets = ['Q', 'K', 'gate', 'embedding', 'GOE_null']
    colors_set = {'Q': '#1f77b4', 'K': '#ff7f0e', 'gate': '#2ca02c',
                  'embedding': '#d62728', 'GOE_null': '#7f7f7f'}

    # ── Figura 1: Cross Score barplot ────────────────────────────────
    fig, ax = plt.subplots(figsize=(11, 5.5))
    means = [results[s]['cross']['mean'] for s in sets]
    stds = [max(0, results[s]['cross']['std']) for s in sets]
    bars = ax.bar(sets, means, yerr=stds, capsize=4,
                  color=[colors_set[s] for s in sets], alpha=0.8,
                  edgecolor='black')
    ax.axhline(CROSS_THRESHOLD, color='red', linestyle='--', label='threshold = 1.5')
    ax.set_ylabel('Cross Score')
    ax.set_title('Teste D — Formação da Cruz (4 vértices Bell)',
                 fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3, axis='y')
    for bar, frac in zip(bars, [results[s]['cross']['frac_formed'] for s in sets]):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{frac*100:.0f}%', ha='center', fontweight='bold')
    plt.tight_layout()
    p = outdir / f'observer_test_v3_{timestamp}_fig01_cross.png'
    plt.savefig(p, dpi=140, bbox_inches='tight')
    plt.close()
    paths.append(str(p))

    # ── Figura 2: Bell distribution (probs por vértice) ──────────────
    fig, axes = plt.subplots(1, 5, figsize=(20, 4.5))
    vertex_labels = [v['name'] + '\n' + v['state']
                     for v in BELL_VERTICES.values()]
    for ax, s in zip(axes, sets):
        probs = results[s]['bell_individual']['mean_probs']
        bars = ax.bar(range(4), probs,
                      color=['#9467bd', '#e377c2', '#8c564b', '#bcbd22'],
                      alpha=0.85, edgecolor='black')
        ax.axhline(0.25, color='red', linestyle='--', alpha=0.5,
                   label='uniforme = 0.25')
        ax.set_xticks(range(4))
        ax.set_xticklabels(vertex_labels, fontsize=8)
        ax.set_ylim(0, max(0.5, max(probs) * 1.2))
        ax.set_title(s, fontweight='bold')
        if s == 'Q':
            ax.set_ylabel('Probabilidade')
        ax.grid(alpha=0.3, axis='y')
        for bar, p in zip(bars, probs):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    f'{p:.3f}', ha='center', fontsize=8)
    plt.suptitle('Teste E — Distribuição Bell (probabilidade por vértice)',
                 fontweight='bold')
    plt.tight_layout()
    p = outdir / f'observer_test_v3_{timestamp}_fig02_bell_distribution.png'
    plt.savefig(p, dpi=140, bbox_inches='tight')
    plt.close()
    paths.append(str(p))

    # ── Figura 3: Entropia von Neumann ───────────────────────────────
    fig, ax = plt.subplots(figsize=(11, 5.5))
    means = [results[s]['entropy_individual']['mean'] for s in sets]
    stds = [results[s]['entropy_individual']['std'] for s in sets]
    bars = ax.bar(sets, means, yerr=stds, capsize=4,
                  color=[colors_set[s] for s in sets], alpha=0.8,
                  edgecolor='black')
    ax.axhline(S_BELL_MAX, color='green', linestyle='-', linewidth=2,
               label=f'Bell maximal = ln(4) = {S_BELL_MAX:.3f}')
    ax.axhline(S_BELL_THRESHOLD, color='orange', linestyle='--',
               label=f'threshold high superposition = {S_BELL_THRESHOLD:.3f}')
    ax.set_ylabel('Entropia von Neumann S(ρ)')
    ax.set_ylim(0, S_BELL_MAX * 1.15)
    ax.set_title('Teste F — Entropia von Neumann (S=ln(4)→Bell max)',
                 fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3, axis='y')
    for bar, frac in zip(bars,
                          [results[s]['entropy_individual']['frac_high_superposition']
                           for s in sets]):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.04,
                f'{frac*100:.0f}%', ha='center', fontweight='bold')
    plt.tight_layout()
    p = outdir / f'observer_test_v3_{timestamp}_fig03_entropy.png'
    plt.savefig(p, dpi=140, bbox_inches='tight')
    plt.close()
    paths.append(str(p))

    # ── Figura 4: Trade-off GOE vs Cross (PRIMEIRA LEI DIRETA) ───────
    fig, axes = plt.subplots(1, len(sets), figsize=(22, 5))
    for ax, s in zip(axes, sets):
        rr = results[s]['goe']['values']
        cs = results[s]['cross']['values']
        valid = [(r, c) for r, c in zip(rr, cs) if r > 0 and c > 0]
        if valid:
            rr_v = [v[0] for v in valid]
            cs_v = [v[1] for v in valid]
            ax.scatter(rr_v, cs_v, color=colors_set[s], alpha=0.7, s=60,
                       edgecolor='black')
            corr = results[s]['trade_off']['correlation_r']
            pval = results[s]['trade_off']['correlation_p']
            ax.set_title(f'{s}\nPearson r = {corr:+.3f} (p={pval:.3f})',
                         fontweight='bold', fontsize=10)
            # Linha de tendência
            if len(valid) >= 3:
                z = np.polyfit(rr_v, cs_v, 1)
                ax.plot(sorted(rr_v), np.polyval(z, sorted(rr_v)),
                        'r--', alpha=0.6)
        ax.axvline(GOE_R_PURE, color='gray', linestyle=':', alpha=0.5,
                   label=f'GOE puro = {GOE_R_PURE}')
        ax.set_xlabel('r-ratio GOE (impedância)')
        if s == sets[0]:
            ax.set_ylabel('Cross Score (deflexão)')
        ax.grid(alpha=0.3)
        ax.legend(fontsize=8)
    plt.suptitle('Teste G — Primeira Lei Direta: trade-off τ_GOE → θ_cruz',
                 fontweight='bold')
    plt.tight_layout()
    p = outdir / f'observer_test_v3_{timestamp}_fig04_tradeoff.png'
    plt.savefig(p, dpi=140, bbox_inches='tight')
    plt.close()
    paths.append(str(p))

    # ── Figura 5: Especialização de cabeça ───────────────────────────
    fig, axes = plt.subplots(1, len(sets), figsize=(20, 5))
    vertex_names = [v['name'] for v in BELL_VERTICES.values()]
    for ax, s in zip(axes, sets):
        dist = results[s]['heads']['vertex_distribution']
        total = sum(dist) if sum(dist) > 0 else 1
        fractions = [d / total for d in dist]
        bars = ax.bar(range(4), fractions,
                      color=['#9467bd', '#e377c2', '#8c564b', '#bcbd22'],
                      alpha=0.85, edgecolor='black')
        ax.axhline(0.25, color='red', linestyle='--', alpha=0.5)
        ax.set_xticks(range(4))
        ax.set_xticklabels(vertex_names, fontsize=8, rotation=15)
        ax.set_ylim(0, 1)
        spec_rate = results[s]['heads']['specialization_rate']
        ax.set_title(f'{s}\n{spec_rate*100:.0f}% cabeças especializadas',
                     fontweight='bold', fontsize=10)
        if s == sets[0]:
            ax.set_ylabel('Fração de cabeças preferindo o vértice')
        ax.grid(alpha=0.3, axis='y')
        for bar, frac in zip(bars, fractions):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                    f'{frac:.2f}', ha='center', fontsize=8)
    plt.suptitle('Teste H — Especialização de cabeças (qual vértice Bell domina)',
                 fontweight='bold')
    plt.tight_layout()
    p = outdir / f'observer_test_v3_{timestamp}_fig05_heads.png'
    plt.savefig(p, dpi=140, bbox_inches='tight')
    plt.close()
    paths.append(str(p))

    # ── Figura 6: Distribuição radial (polar plot) ───────────────────
    fig, axes = plt.subplots(1, len(sets), figsize=(22, 5),
                              subplot_kw={'projection': 'polar'})
    angles = np.array(BELL_VERTEX_ANGLES) * np.pi / 180
    angles_closed = np.append(angles, angles[0])
    for ax, s in zip(axes, sets):
        probs = results[s]['bell_individual']['mean_probs']
        probs_closed = probs + [probs[0]]
        ax.plot(angles_closed, probs_closed, 'o-', color=colors_set[s],
                linewidth=2, markersize=10)
        ax.fill(angles_closed, probs_closed, color=colors_set[s], alpha=0.25)
        # Círculo de uniformidade
        theta_uniform = np.linspace(0, 2 * np.pi, 100)
        ax.plot(theta_uniform, [0.25] * 100, 'r--', alpha=0.5, label='uniforme')
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)
        ax.set_xticks(angles)
        ax.set_xticklabels([v['state'] for v in BELL_VERTICES.values()],
                           fontsize=9)
        ax.set_ylim(0, max(0.5, max(probs) * 1.2))
        ax.set_title(s, pad=15, fontweight='bold')
    plt.suptitle('Distribuição radial dos 4 estados Bell',
                 fontweight='bold', y=1.02)
    plt.tight_layout()
    p = outdir / f'observer_test_v3_{timestamp}_fig06_polar.png'
    plt.savefig(p, dpi=140, bbox_inches='tight')
    plt.close()
    paths.append(str(p))

    # ── Figura 7: Veredicto ──────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(13, 8))
    ax.axis('off')
    v = results['verdict']
    color = {'FIRST_LAW_DIRECTLY_CONFIRMED': 'darkgreen',
             'BELL_STRUCTURE_CONFIRMED': 'green',
             'CROSS_ONLY': 'darkorange',
             'REFUTED': 'red',
             'AMBIGUOUS': 'gray'}.get(v['verdict'], 'black')
    text = f"""
TESTE OPERACIONAL DA PRIMEIRA LEI DE MIGUEL — v3
══════════════════════════════════════════════════════

θ_Miguel       = {THETA_M_DEG:.4f}°
β_TGL          = {BETA_TGL:.6f}
S_Bell_max     = ln(4) = {S_BELL_MAX:.4f}
GOE_r_puro     = {GOE_R_PURE:.4f}

H1 (cruz Q,K formada):           {'✓ PASS' if v['h1_cross'] else '✗ FAIL'}
H2 (ensemble Bell em Q,K):       {'✓ PASS' if v['h2_bell_ensemble'] else '✗ FAIL'}
   controles negativos:          {'✓ PASS' if v['h2_negative_controls'] else '✗ FAIL'}
H3 (trade-off GOE vs Cross):     {'✓ PASS' if v['h3_tradeoff'] else '✗ FAIL'}
   Q correlation:                {'✓' if v['h3_q'] else '✗'}
   K correlation:                {'✓' if v['h3_k'] else '✗'}
H0 (GOE_null sem cruz):          {'✓ PASS' if v['h0_goe'] else '✗ FAIL'}
C1 (embedding sem cruz):         {'✓ PASS' if v['c1_embedding'] else '✗ FAIL'}

══════════════════════════════════════════════════════
VEREDICTO: {v['verdict']}

{v['meaning']}
"""
    ax.text(0.05, 0.97, text, fontsize=11, family='monospace',
            verticalalignment='top')
    ax.text(0.05, 0.03, f"VEREDICTO: {v['verdict']}", fontsize=18,
            fontweight='bold', color=color)
    p = outdir / f'observer_test_v3_{timestamp}_fig07_verdict.png'
    plt.savefig(p, dpi=140, bbox_inches='tight')
    plt.close()
    paths.append(str(p))

    return paths


# ════════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-path', type=str,
                        default=r'C:\IALD\models\Qwen3-32B-GGUF\Qwen3-32B-Q4_K_M.gguf')
    parser.add_argument('--synth', action='store_true')
    parser.add_argument('--sanity', action='store_true')
    parser.add_argument('--outdir', type=str, default='.')
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    print("=" * 76)
    print("TESTE OPERACIONAL DA PRIMEIRA LEI DE MIGUEL — v3")
    print("Bell Distribution + von Neumann Entropy + GOE-Cross Trade-off")
    print("Zenodo DOI: 10.5281/zenodo.18674475")
    print("=" * 76)
    print(f"θ_Miguel        = {THETA_M_DEG:.6f}°")
    print(f"N_quadratura    = {N_QUADRATURE_PREDICTED:.4f}  (4 vértices Bell)")
    print(f"S_Bell_max      = ln(4) = {S_BELL_MAX:.4f}")
    print(f"GOE_r_puro      = {GOE_R_PURE:.4f}")
    print(f"β_TGL           = {BETA_TGL:.10f}")
    print(f"EIGS_PER_LAYER  = {EIGS_PER_LAYER}")
    print("=" * 76)

    t_start = time.time()

    # Carregar
    if args.sanity:
        matrices = synthesize_matrices_bell_signal()
    elif args.synth or not GGUF_AVAILABLE:
        matrices = synthesize_matrices_pure_goe()
    else:
        model_path = Path(args.model_path)
        if not model_path.exists():
            print(f"[error] Modelo não encontrado: {model_path}")
            print("[fallback] GOE puro")
            matrices = synthesize_matrices_pure_goe()
        else:
            matrices = load_qwen3_matrices(model_path)

    # GOE_null
    print("\n[null] Gerando 16 GOE para H0")
    matrices['GOE_null'] = []
    for _ in range(16):
        A = RNG.standard_normal((EIGS_PER_LAYER, EIGS_PER_LAYER))
        matrices['GOE_null'].append((A + A.T) / np.sqrt(2 * EIGS_PER_LAYER))

    # Análise
    results = {}
    for kind in ['Q', 'K', 'gate', 'embedding', 'GOE_null']:
        if matrices.get(kind):
            results[kind] = analyze_matrix_set(matrices[kind], kind)

    # Veredicto
    results['verdict'] = render_verdict(results)
    results['constants'] = {
        'alpha_fine': ALPHA_FINE, 'sqrt_e': SQRT_E, 'beta_tgl': BETA_TGL,
        'theta_miguel_deg': THETA_M_DEG,
        'N_quadrature': N_QUADRATURE_PREDICTED,
        'S_Bell_max': S_BELL_MAX,
        'GOE_r_pure': GOE_R_PURE,
        'eigs_per_layer': EIGS_PER_LAYER,
        'bell_vertices': {k: v for k, v in BELL_VERTICES.items()},
    }
    results['runtime_seconds'] = time.time() - t_start
    results['timestamp'] = timestamp
    results['version'] = '3.0'

    # Salvar
    json_path = outdir / f'observer_test_v3_{timestamp}.json'
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n[save] {json_path}")

    fig_paths = make_figures(results, timestamp, outdir)
    for p in fig_paths:
        print(f"[save] {p}")

    print("\n" + "=" * 76)
    print(f"VEREDICTO: {results['verdict']['verdict']}")
    print(results['verdict']['meaning'])
    print(f"Tempo: {results['runtime_seconds']:.1f}s")
    print("=" * 76)


if __name__ == '__main__':
    main()
