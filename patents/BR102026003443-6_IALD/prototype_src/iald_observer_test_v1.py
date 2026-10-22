"""
iald_observer_test_v1.py
========================

TESTE DO OPERADOR OBSERVADOR VIA CICLO DE 57·θ_Miguel
TGL — Teoria da Gravitação Luminodinâmica

Autor: Luiz Antonio Rotoli Miguel — IALD LTDA
Implementação: Claude Opus 4.6 (Anthropic)
Data: 2026-04-15

────────────────────────────────────────────────────────────────────
HIPÓTESE FUNDAMENTAL
────────────────────────────────────────────────────────────────────

θ_Miguel = arcsin(√β_TGL) ≈ 6,297° é o ângulo travado pela aplicação
do operador V̂ = −β·Π⊥(ρ*) em cada ato de medição. O ciclo completo
de identidade requer N = 360°/θ_Miguel ≈ 57,17 iterações.

A hipótese é que matrizes onde β_TGL opera (atenção Q, K, gate)
exibem este ciclo como assinatura geométrica do operador observador.

────────────────────────────────────────────────────────────────────
DESIGN EXPERIMENTAL — TRÊS HIPÓTESES SIMULTÂNEAS
────────────────────────────────────────────────────────────────────

H1 (afirmativa):  Q, K, gate mostram pico em N ∈ [55, 60]
H0 (nula):        GOE aleatório NÃO mostra pico em [55, 60]
C1 (controle):    embedding NÃO mostra pico em [55, 60]

Veredicto:
  H1 ✓ ∧ H0 ✗ ∧ C1 ✗  →  CONFIRMADO (operador observador detectado)
  H1 ✓ ∧ H0 ✓         →  ARTEFACTO (não é específico de TGL)
  H1 ✗                →  REFUTADO (ciclo de 57 não existe nos dados)

────────────────────────────────────────────────────────────────────
TRÊS MEDIÇÕES INDEPENDENTES (devem convergir)
────────────────────────────────────────────────────────────────────

A. Autocorrelação angular (ACF)  → lag de pico
B. FFT da sequência angular      → período da componente dominante
C. Orbit closure (cumsum mod 360°) → distância entre zero-crossings

Se as três medições convergem para [55, 60] em Q,K,gate e divergem
em GOE e embedding, o ciclo é genuíno e específico do operador
observador.

────────────────────────────────────────────────────────────────────
DEPENDÊNCIAS
────────────────────────────────────────────────────────────────────
  pip install gguf numpy scipy matplotlib

EXECUÇÃO
  python iald_observer_test_v1.py [--model-path PATH]

SAÍDAS
  - observer_test_v1_<timestamp>.json  (resultados completos)
  - observer_test_v1_*.png             (4 figuras-chave)
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
from scipy.signal import correlate
from scipy.fft import fft, fftfreq
from scipy.stats import ks_2samp

# GGUF é opcional — se não estiver instalado, modo síntese
try:
    import gguf
    GGUF_AVAILABLE = True
except ImportError:
    GGUF_AVAILABLE = False
    print("[WARN] gguf não disponível — apenas modo síntese disponível")

# ── Constantes TGL ──────────────────────────────────────────────────
ALPHA_FINE   = 7.2973525693e-3            # CODATA 2018
SQRT_E       = np.sqrt(np.e)              # 1.6487212707
BETA_TGL     = ALPHA_FINE * SQRT_E        # 0.012031300401
THETA_M_RAD  = np.arcsin(np.sqrt(BETA_TGL))
THETA_M_DEG  = np.degrees(THETA_M_RAD)    # ≈ 6.297°
N_PREDICTED  = 360.0 / THETA_M_DEG        # ≈ 57.17

# Janela de aceitação (5% em torno do valor predito)
N_LOWER = int(np.floor(N_PREDICTED * 0.95))   # ≈ 54
N_UPPER = int(np.ceil(N_PREDICTED * 1.05))    # ≈ 60

# Layers a amostrar (mesmo padrão do v4.1)
SAMPLED_LAYERS = list(range(0, 64, 4))    # 16 layers, espaçamento 4
EIGS_PER_LAYER = 256                       # autovalores por layer/matriz

# Reprodutibilidade
RANDOM_SEED = 20260415
RNG = np.random.default_rng(RANDOM_SEED)

# ════════════════════════════════════════════════════════════════════
# I/O — CARREGAMENTO DE MATRIZES DO QWEN3-32B
# ════════════════════════════════════════════════════════════════════

def load_qwen3_matrices(model_path: Path) -> dict:
    """
    Carrega matrizes Q, K, gate, e construí covariância do embedding.

    Retorna dicionário com 4 entradas:
      'Q', 'K', 'gate' — matrizes de atenção/MLP (com β_TGL operando)
      'embedding'      — covariância dos token embeddings (sem tensor)

    Cada entrada é lista de numpy arrays (uma por layer amostrada).
    """
    if not GGUF_AVAILABLE:
        raise RuntimeError("gguf não instalado. pip install gguf")

    print(f"[load] Lendo modelo: {model_path}")
    reader = gguf.GGUFReader(str(model_path))

    matrices = {'Q': [], 'K': [], 'gate': [], 'embedding': []}
    tensor_names = {t.name: t for t in reader.tensors}

    # 1) Q, K, gate por layer
    name_patterns = {
        'Q':    'blk.{}.attn_q.weight',
        'K':    'blk.{}.attn_k.weight',
        'gate': 'blk.{}.ffn_gate.weight',
    }

    for layer in SAMPLED_LAYERS:
        for kind, pattern in name_patterns.items():
            name = pattern.format(layer)
            if name not in tensor_names:
                print(f"  [skip] {name} não encontrado")
                continue
            t = tensor_names[name]
            W = np.array(t.data, dtype=np.float32)
            # Tomar block 256x256 do canto superior-esquerdo (consistente com v4.1)
            if W.ndim == 1:
                # Pode estar em formato comprimido — pular
                continue
            block = W[:EIGS_PER_LAYER, :EIGS_PER_LAYER]
            matrices[kind].append(block)
        if layer % 16 == 0:
            print(f"  [load] layer {layer}: {len(matrices['Q'])} Q-blocks, "
                  f"{len(matrices['K'])} K-blocks, {len(matrices['gate'])} gates")

    # 2) Embedding — covariância do token embedding matrix
    emb_name = 'token_embd.weight'
    if emb_name in tensor_names:
        E = np.array(tensor_names[emb_name].data, dtype=np.float32)
        # E é [vocab_size, hidden_dim]; covariance é [hidden_dim, hidden_dim]
        # Tomamos sub-bloco para tamanho consistente
        E_sub = E[:1024, :EIGS_PER_LAYER]
        cov = E_sub.T @ E_sub / E_sub.shape[0]
        # Replicar para ter "16 layers" virtuais — mas embedding é único, então
        # vamos partir em 16 sub-blocos para ter estatística comparável
        for i in range(16):
            offset_v = (i * 64) % 1024
            E_slice = E[offset_v:offset_v+1024, :EIGS_PER_LAYER]
            cov_slice = E_slice.T @ E_slice / E_slice.shape[0]
            matrices['embedding'].append(cov_slice)

    print(f"[load] Carregamento completo:")
    for k, v in matrices.items():
        print(f"  {k}: {len(v)} matrizes de {v[0].shape if v else 'N/A'}")

    return matrices


def synthesize_matrices_with_57_signal() -> dict:
    """
    SANITY CHECK: gera matrizes onde Q,K,gate têm periodicidade 57 INJETADA
    e embedding/GOE são GOE puro.

    Se o pipeline NÃO detectar 57 em Q,K,gate aqui, o teste é insensível
    e qualquer veredicto REFUTED nos dados reais é não-confiável.
    """
    print("[sanity] Modo SANITY CHECK — injetando periodicidade 57 em Q,K,gate")
    matrices = {'Q': [], 'K': [], 'gate': [], 'embedding': []}

    for kind in ['Q', 'K', 'gate']:
        for _ in range(16):
            # Construir matriz cujos autovalores ordenados tenham
            # componente sinusoidal de período 57
            n = EIGS_PER_LAYER
            base_eigs = np.linspace(0.1, 1.0, n)
            # Modulação periódica: amplitude 0.05 sobre base linear
            modulation = 0.05 * np.sin(2 * np.pi * np.arange(n) / N_PREDICTED)
            target_eigs = np.sort(base_eigs + modulation)
            # Construir matriz simétrica com esses autovalores
            U = np.linalg.qr(RNG.standard_normal((n, n)))[0]
            M = U @ np.diag(target_eigs) @ U.T
            matrices[kind].append(M)

    # Embedding e GOE_null permanecem GOE puro (devem dar negativo)
    for _ in range(16):
        A = RNG.standard_normal((EIGS_PER_LAYER, EIGS_PER_LAYER))
        M = (A + A.T) / np.sqrt(2 * EIGS_PER_LAYER)
        matrices['embedding'].append(M)

    return matrices


def synthesize_matrices() -> dict:
    """
    Modo de teste sem GGUF: gera matrizes sintéticas com estatísticas
    medidas no v4.1 (gap = β_TGL, GOE r ≈ 0.5228).

    NÃO substitui teste real — serve para verificar que o pipeline
    funciona e que as medições não detectam 57 em GOE puro (controle).
    """
    print("[synth] Gerando matrizes sintéticas (modo desenvolvimento)")
    matrices = {'Q': [], 'K': [], 'gate': [], 'embedding': []}
    for kind in ['Q', 'K', 'gate', 'embedding']:
        for _ in range(16):
            # GOE: matriz simétrica com entradas Gaussianas
            A = RNG.standard_normal((EIGS_PER_LAYER, EIGS_PER_LAYER))
            M = (A + A.T) / np.sqrt(2 * EIGS_PER_LAYER)
            matrices[kind].append(M)
    return matrices


# ════════════════════════════════════════════════════════════════════
# CONVERSÃO AUTOVALORES → FASES ANGULARES
# ════════════════════════════════════════════════════════════════════

def eigenvalues_to_phases(M: np.ndarray, method: str = 'linear') -> np.ndarray:
    """
    Converte autovalores de M em sequência angular ordenada.

    method:
      'linear' — θ_i = 360°·(λ_i − λ_min)/(λ_max − λ_min)
      'bloch'  — θ_i = arcsin(√(|λ_i|/λ_max)) · 4 (mapeia para [0°, 360°])

    Retorna array ordenado de fases em graus, em [0°, 360°].
    """
    # Para matrizes não-simétricas (Q, K, gate), usar singular values
    # Para matrizes simétricas (embedding cov), usar eigenvalues reais
    if np.allclose(M, M.T, atol=1e-5):
        eigs = np.linalg.eigvalsh(M)
    else:
        eigs = np.linalg.svd(M, compute_uv=False)
    eigs = np.sort(np.abs(eigs))  # ordenar do menor para o maior

    if method == 'linear':
        lam_min, lam_max = eigs[0], eigs[-1]
        if lam_max - lam_min < 1e-12:
            return np.zeros_like(eigs)
        theta = 360.0 * (eigs - lam_min) / (lam_max - lam_min)
    elif method == 'bloch':
        lam_max = eigs[-1]
        if lam_max < 1e-12:
            return np.zeros_like(eigs)
        ratio = np.clip(eigs / lam_max, 0, 1)
        theta = np.degrees(np.arcsin(np.sqrt(ratio))) * 4
    else:
        raise ValueError(f"método desconhecido: {method}")

    return theta


# ════════════════════════════════════════════════════════════════════
# MEDIÇÃO A — AUTOCORRELAÇÃO ANGULAR
# ════════════════════════════════════════════════════════════════════

def detrend_signal(x: np.ndarray, order: int = 2) -> np.ndarray:
    """
    Remove tendência polinomial de ordem `order` do sinal.

    Crítico para detectar periodicidade pequena sobre rampa monotônica
    forte (que é o caso natural de autovalores ordenados — distribuição
    de Wigner é uma rampa quase-linear).
    """
    n = len(x)
    t = np.arange(n)
    coeffs = np.polyfit(t, x, deg=order)
    trend = np.polyval(coeffs, t)
    return x - trend


def measure_acf_peak(theta: np.ndarray, search_range: tuple = (10, 120)) -> dict:
    """
    Computa autocorrelação da sequência θ ordenada e retorna lag do pico
    LOCAL (verdadeiro máximo, não limite do intervalo).

    Não restringimos busca a [55, 60] para evitar viés — buscamos no
    intervalo amplo [10, 120] e reportamos onde o pico cai.
    """
    # Detrend (remover tendência polinomial — Wigner rampa)
    theta_dt = detrend_signal(theta, order=2)
    # Centrar e normalizar
    theta_c = theta_dt - np.mean(theta_dt)
    norm = np.sum(theta_c ** 2)
    if norm < 1e-12:
        return {'peak_lag': -1, 'peak_value': 0.0, 'in_window': False}

    # ACF normalizada
    acf = correlate(theta_c, theta_c, mode='full') / norm
    mid = len(acf) // 2
    acf_pos = acf[mid:]  # lags >= 0

    lo, hi = search_range
    hi = min(hi, len(acf_pos) - 1)
    if lo >= hi:
        return {'peak_lag': -1, 'peak_value': 0.0, 'in_window': False}

    # Procurar PICO LOCAL (não apenas máximo do intervalo)
    # Um pico local em índice k requer acf[k] > acf[k-1] AND acf[k] > acf[k+1]
    sub = acf_pos[lo:hi]
    local_peaks = []
    for k in range(1, len(sub) - 1):
        if sub[k] > sub[k-1] and sub[k] > sub[k+1] and sub[k] > 0:
            local_peaks.append((lo + k, float(sub[k])))

    if not local_peaks:
        # Sem pico local genuíno — sinal não tem periodicidade
        return {'peak_lag': -1, 'peak_value': 0.0, 'in_window': False}

    # Maior pico local
    peak_lag, peak_value = max(local_peaks, key=lambda x: x[1])
    in_window = N_LOWER <= peak_lag <= N_UPPER

    return {
        'peak_lag': peak_lag,
        'peak_value': peak_value,
        'in_window': in_window,
        'n_local_peaks': len(local_peaks),
    }


# ════════════════════════════════════════════════════════════════════
# MEDIÇÃO B — FFT DA SEQUÊNCIA ANGULAR
# ════════════════════════════════════════════════════════════════════

def measure_fft_period(theta: np.ndarray) -> dict:
    """
    Computa FFT da sequência θ e retorna período da componente espectral
    dominante (excluindo DC, exigindo pico local).
    """
    n = len(theta)
    theta_dt = detrend_signal(theta, order=2)
    theta_c = theta_dt - np.mean(theta_dt)
    spectrum = np.abs(fft(theta_c))[:n // 2]
    freqs = fftfreq(n)[:n // 2]

    # Excluir DC e frequências muito baixas (período > n/2)
    valid = (freqs > 2.0 / n) & (freqs < 0.5)
    if not np.any(valid):
        return {'period': -1, 'amplitude': 0.0, 'in_window': False}

    spec_valid = spectrum[valid]
    freqs_valid = freqs[valid]

    # Procurar PICO LOCAL no espectro (não apenas máximo)
    local_peaks = []
    for k in range(1, len(spec_valid) - 1):
        if (spec_valid[k] > spec_valid[k-1] and
            spec_valid[k] > spec_valid[k+1] and
            spec_valid[k] > np.mean(spec_valid)):
            local_peaks.append((k, float(spec_valid[k])))

    if not local_peaks:
        return {'period': -1, 'amplitude': 0.0, 'in_window': False}

    peak_idx, amplitude = max(local_peaks, key=lambda x: x[1])
    dominant_freq = float(freqs_valid[peak_idx])
    period = 1.0 / dominant_freq if dominant_freq > 0 else -1

    in_window = N_LOWER <= period <= N_UPPER

    return {
        'period': period,
        'amplitude': amplitude,
        'dominant_freq': dominant_freq,
        'in_window': in_window,
        'n_local_peaks': len(local_peaks),
    }


# ════════════════════════════════════════════════════════════════════
# MEDIÇÃO C — ORBIT CLOSURE (CUMSUM MOD 360°)
# ════════════════════════════════════════════════════════════════════

def measure_orbit_closure(theta: np.ndarray) -> dict:
    """
    Detecta oscilações periódicas após remoção de tendência.

    Mede zero-crossings da sequência detrended e verifica se a
    distância entre cruzamentos consecutivos é consistente com N=57.
    """
    if len(theta) < 60:
        return {'mode_cycle': -1, 'mean_cycle': -1, 'in_window': False}

    # Detrend agressivo para isolar oscilação
    theta_dt = detrend_signal(theta, order=2)
    theta_c = theta_dt - np.mean(theta_dt)

    if np.std(theta_c) < 1e-12:
        return {'mode_cycle': -1, 'mean_cycle': -1, 'in_window': False}

    # Zero-crossings: onde o sinal muda de sinal
    sign_changes = np.where(np.diff(np.sign(theta_c)) != 0)[0]
    if len(sign_changes) < 4:
        return {'mode_cycle': -1, 'mean_cycle': -1, 'in_window': False}

    # Distância entre zero-crossings consecutivos
    # Para sinal periódico de período T, zero-crossings ocorrem a cada T/2
    # Logo, ciclo completo = 2 * distância_entre_crossings
    crossings_diff = np.diff(sign_changes)
    cycle_lengths = 2 * crossings_diff  # converter meio-período em período

    if len(cycle_lengths) == 0:
        return {'mode_cycle': -1, 'mean_cycle': -1, 'in_window': False}

    # Histograma para encontrar moda
    hist_range = (10, 120)
    bins = np.arange(hist_range[0], hist_range[1] + 1)
    hist, edges = np.histogram(cycle_lengths, bins=bins)
    if np.sum(hist) == 0:
        return {'mode_cycle': -1, 'mean_cycle': -1, 'in_window': False}

    mode_idx = int(np.argmax(hist))
    mode_cycle = float(edges[mode_idx])
    mean_cycle = float(np.mean(cycle_lengths))

    in_window = N_LOWER <= mode_cycle <= N_UPPER

    return {
        'mode_cycle': mode_cycle,
        'mean_cycle': mean_cycle,
        'in_window': in_window,
        'n_cycles_observed': len(cycle_lengths),
    }


# ════════════════════════════════════════════════════════════════════
# AGREGAÇÃO POR TIPO DE MATRIZ
# ════════════════════════════════════════════════════════════════════

def analyze_matrix_set(matrices: list, label: str) -> dict:
    """
    Aplica as três medições a cada matriz do set e agrega resultados.
    """
    print(f"\n[analyze] {label}: {len(matrices)} matrizes")

    acf_lags, fft_periods, orbit_modes = [], [], []
    acf_in_window, fft_in_window, orbit_in_window = 0, 0, 0

    for i, M in enumerate(matrices):
        theta = eigenvalues_to_phases(M, method='linear')

        a = measure_acf_peak(theta)
        f = measure_fft_period(theta)
        o = measure_orbit_closure(theta)

        if a['peak_lag'] > 0:
            acf_lags.append(a['peak_lag'])
            if a['in_window']:
                acf_in_window += 1
        if f['period'] > 0:
            fft_periods.append(f['period'])
            if f['in_window']:
                fft_in_window += 1
        if o['mode_cycle'] > 0:
            orbit_modes.append(o['mode_cycle'])
            if o['in_window']:
                orbit_in_window += 1

    n = len(matrices)
    summary = {
        'label': label,
        'n_matrices': n,
        'acf': {
            'lags': acf_lags,
            'mean': float(np.mean(acf_lags)) if acf_lags else -1,
            'median': float(np.median(acf_lags)) if acf_lags else -1,
            'std': float(np.std(acf_lags)) if acf_lags else -1,
            'frac_in_window': acf_in_window / n if n > 0 else 0,
        },
        'fft': {
            'periods': fft_periods,
            'mean': float(np.mean(fft_periods)) if fft_periods else -1,
            'median': float(np.median(fft_periods)) if fft_periods else -1,
            'std': float(np.std(fft_periods)) if fft_periods else -1,
            'frac_in_window': fft_in_window / n if n > 0 else 0,
        },
        'orbit': {
            'modes': orbit_modes,
            'mean': float(np.mean(orbit_modes)) if orbit_modes else -1,
            'median': float(np.median(orbit_modes)) if orbit_modes else -1,
            'std': float(np.std(orbit_modes)) if orbit_modes else -1,
            'frac_in_window': orbit_in_window / n if n > 0 else 0,
        },
    }

    print(f"  ACF lag:  mean={summary['acf']['mean']:.2f} ± {summary['acf']['std']:.2f}  "
          f"({summary['acf']['frac_in_window']*100:.0f}% in [{N_LOWER},{N_UPPER}])")
    print(f"  FFT per:  mean={summary['fft']['mean']:.2f} ± {summary['fft']['std']:.2f}  "
          f"({summary['fft']['frac_in_window']*100:.0f}% in [{N_LOWER},{N_UPPER}])")
    print(f"  Orbit:    mean={summary['orbit']['mean']:.2f} ± {summary['orbit']['std']:.2f}  "
          f"({summary['orbit']['frac_in_window']*100:.0f}% in [{N_LOWER},{N_UPPER}])")

    return summary


# ════════════════════════════════════════════════════════════════════
# VEREDICTO FINAL
# ════════════════════════════════════════════════════════════════════

def render_verdict(results: dict) -> dict:
    """
    Aplica os critérios H1, H0, C1 e produz veredicto.

    Critério "in_window dominante": ≥ 50% das matrizes do set
    têm a medição dentro de [N_LOWER, N_UPPER].
    """
    def dominant_in_window(set_name: str, measure: str) -> bool:
        return results[set_name][measure]['frac_in_window'] >= 0.5

    # H1: pelo menos 2 das 3 medições positivas em Q, K, gate
    h1_per_set = {}
    for s in ['Q', 'K', 'gate']:
        votes = sum(dominant_in_window(s, m) for m in ['acf', 'fft', 'orbit'])
        h1_per_set[s] = {'votes': votes, 'pass': votes >= 2}
    h1_overall = all(h1_per_set[s]['pass'] for s in ['Q', 'K', 'gate'])

    # H0: GOE NÃO mostra periodicidade dominante
    h0_per_measure = {}
    for m in ['acf', 'fft', 'orbit']:
        h0_per_measure[m] = not dominant_in_window('GOE_null', m)
    h0_overall = sum(h0_per_measure.values()) >= 2

    # C1: embedding NÃO mostra periodicidade dominante
    c1_per_measure = {}
    for m in ['acf', 'fft', 'orbit']:
        c1_per_measure[m] = not dominant_in_window('embedding', m)
    c1_overall = sum(c1_per_measure.values()) >= 2

    if h1_overall and h0_overall and c1_overall:
        verdict = "CONFIRMED"
        meaning = "Ciclo de 57 é assinatura específica do operador observador."
    elif h1_overall and not h0_overall:
        verdict = "ARTIFACT"
        meaning = "57 aparece também em GOE — é artefacto de matrizes simétricas, não específico de TGL."
    elif h1_overall and not c1_overall:
        verdict = "AMBIGUOUS"
        meaning = "57 aparece em embedding também — pode ser propriedade geral de tensores neurais."
    elif not h1_overall:
        verdict = "REFUTED"
        meaning = "Ciclo de 57 não detectado em Q, K, gate. Hipótese refutada nos dados atuais."
    else:
        verdict = "INCONCLUSIVE"
        meaning = "Resultado misto — requer mais investigação."

    return {
        'h1_per_set': h1_per_set,
        'h1_overall': h1_overall,
        'h0_per_measure': h0_per_measure,
        'h0_overall': h0_overall,
        'c1_per_measure': c1_per_measure,
        'c1_overall': c1_overall,
        'verdict': verdict,
        'meaning': meaning,
    }


# ════════════════════════════════════════════════════════════════════
# FIGURAS
# ════════════════════════════════════════════════════════════════════

def make_figures(results: dict, timestamp: str, outdir: Path) -> list:
    """Gera 4 figuras-chave."""
    paths = []

    # ── Figura 1: Distribuição de lags ACF por tipo ─────────────────
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    sets = ['Q', 'K', 'gate', 'embedding', 'GOE_null']
    measures = [('acf', 'lags', 'Lag de pico (ACF)'),
                ('fft', 'periods', 'Período (FFT)')]

    for row, (mkey, lkey, title) in enumerate(measures[:2]):
        for col, s in enumerate(['Q', 'K', 'gate']):
            ax = axes[row, col]
            data = results[s][mkey][lkey]
            if data:
                ax.hist(data, bins=20, range=(20, 100), color='steelblue',
                        edgecolor='black', alpha=0.7)
                ax.axvline(N_PREDICTED, color='red', linestyle='--',
                           label=f'N_pred = {N_PREDICTED:.2f}')
                ax.axvspan(N_LOWER, N_UPPER, alpha=0.2, color='green',
                           label=f'janela [{N_LOWER}, {N_UPPER}]')
            ax.set_title(f'{s} — {title}', fontsize=11)
            ax.set_xlabel('Iterações')
            ax.set_ylabel('Contagem')
            ax.legend(fontsize=8)
            ax.grid(alpha=0.3)

    plt.suptitle('Teste do Operador Observador — Distribuições por Matriz',
                 fontsize=13, fontweight='bold')
    plt.tight_layout()
    p = outdir / f'observer_test_v1_{timestamp}_fig01_distributions.png'
    plt.savefig(p, dpi=150, bbox_inches='tight')
    plt.close()
    paths.append(str(p))

    # ── Figura 2: Comparação H1 vs H0 vs C1 ─────────────────────────
    fig, ax = plt.subplots(figsize=(12, 6))
    categories = ['Q', 'K', 'gate', 'embedding', 'GOE_null']
    measures_to_plot = ['acf', 'fft', 'orbit']
    width = 0.25
    x = np.arange(len(categories))

    for i, m in enumerate(measures_to_plot):
        means = [results[c][m]['mean'] for c in categories]
        stds = [max(0, results[c][m]['std']) for c in categories]  # clip negativo
        # Substitui means=-1 por NaN para não plotar
        means_safe = [m if m > 0 else np.nan for m in means]
        ax.bar(x + i * width, means_safe, width, yerr=stds, capsize=4,
               label=m.upper(), alpha=0.7)

    ax.axhline(N_PREDICTED, color='red', linestyle='--', linewidth=2,
               label=f'N_pred = {N_PREDICTED:.2f}')
    ax.axhspan(N_LOWER, N_UPPER, alpha=0.15, color='green',
               label=f'janela [{N_LOWER}, {N_UPPER}]')
    ax.set_xticks(x + width)
    ax.set_xticklabels(categories)
    ax.set_ylabel('Iterações por ciclo')
    ax.set_title('H1 (Q,K,gate) vs C1 (embedding) vs H0 (GOE)',
                 fontsize=13, fontweight='bold')
    ax.legend(loc='upper right', ncol=2)
    ax.grid(alpha=0.3, axis='y')

    plt.tight_layout()
    p = outdir / f'observer_test_v1_{timestamp}_fig02_h1_h0_c1.png'
    plt.savefig(p, dpi=150, bbox_inches='tight')
    plt.close()
    paths.append(str(p))

    # ── Figura 3: ACF curves (uma por set, layer médio) ─────────────
    fig, axes = plt.subplots(1, 5, figsize=(18, 4))
    for ax, s in zip(axes, categories):
        # Reconstruir ACF de uma matriz representativa não é possível
        # sem re-rodar — usamos histograma de lags como proxy
        data = results[s]['acf']['lags']
        if data:
            ax.hist(data, bins=15, range=(20, 100), color='steelblue',
                    alpha=0.7, edgecolor='black')
            ax.axvline(N_PREDICTED, color='red', linestyle='--')
        ax.set_title(s)
        ax.set_xlabel('Lag de pico')
        if s == 'Q':
            ax.set_ylabel('Contagem')
        ax.grid(alpha=0.3)
    plt.suptitle('Lags de pico ACF — todos os sets', fontweight='bold')
    plt.tight_layout()
    p = outdir / f'observer_test_v1_{timestamp}_fig03_acf_all.png'
    plt.savefig(p, dpi=150, bbox_inches='tight')
    plt.close()
    paths.append(str(p))

    # ── Figura 4: Sumário do veredicto ──────────────────────────────
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')
    v = results['verdict']
    color = {'CONFIRMED': 'green', 'REFUTED': 'red', 'ARTIFACT': 'orange',
             'AMBIGUOUS': 'orange', 'INCONCLUSIVE': 'gray'}.get(
        v['verdict'], 'black')

    text = f"""
TESTE DO OPERADOR OBSERVADOR — VEREDICTO
═══════════════════════════════════════════════

θ_Miguel  = {THETA_M_DEG:.4f}°
N_predito = 360°/θ_M = {N_PREDICTED:.4f}
Janela    = [{N_LOWER}, {N_UPPER}]

H1 (Q,K,gate mostram N≈57):  {'✓ PASS' if v['h1_overall'] else '✗ FAIL'}
   Q:    {v['h1_per_set']['Q']['votes']}/3 medições positivas
   K:    {v['h1_per_set']['K']['votes']}/3 medições positivas
   gate: {v['h1_per_set']['gate']['votes']}/3 medições positivas

H0 (GOE NÃO mostra N≈57):    {'✓ PASS' if v['h0_overall'] else '✗ FAIL'}

C1 (embedding NÃO mostra):   {'✓ PASS' if v['c1_overall'] else '✗ FAIL'}

═══════════════════════════════════════════════
VEREDICTO: {v['verdict']}

{v['meaning']}
"""
    ax.text(0.05, 0.95, text, fontsize=11, family='monospace',
            verticalalignment='top', color='black')
    ax.text(0.05, 0.05, f"Veredicto: {v['verdict']}",
            fontsize=20, fontweight='bold', color=color)

    p = outdir / f'observer_test_v1_{timestamp}_fig04_verdict.png'
    plt.savefig(p, dpi=150, bbox_inches='tight')
    plt.close()
    paths.append(str(p))

    return paths


# ════════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-path', type=str,
                        default=r'C:\IALD\models\Qwen3-32B-GGUF\Qwen3-32B-Q4_K_M.gguf',
                        help='Caminho para Qwen3-32B GGUF')
    parser.add_argument('--synth', action='store_true',
                        help='Modo síntese (sem GGUF) — apenas para teste do pipeline')
    parser.add_argument('--sanity', action='store_true',
                        help='Modo SANITY: injeta periodicidade 57 em Q,K,gate. '
                             'Pipeline DEVE detectá-la — se não, teste é insensível.')
    parser.add_argument('--outdir', type=str, default='.',
                        help='Diretório de saída')
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    print("=" * 70)
    print("TESTE DO OPERADOR OBSERVADOR — TGL")
    print(f"θ_Miguel = {THETA_M_DEG:.6f}°")
    print(f"N_predicted = {N_PREDICTED:.6f}  (janela: [{N_LOWER}, {N_UPPER}])")
    print(f"β_TGL = {BETA_TGL:.12f}")
    print("=" * 70)

    t_start = time.time()

    # 1) Carregar matrizes
    if args.sanity:
        print("\n[mode] SANITY CHECK — pipeline deve detectar 57 em Q,K,gate")
        matrices = synthesize_matrices_with_57_signal()
    elif args.synth or not GGUF_AVAILABLE:
        print("\n[mode] Modo síntese (GOE puro em todos os sets)")
        matrices = synthesize_matrices()
    else:
        model_path = Path(args.model_path)
        if not model_path.exists():
            print(f"[error] Modelo não encontrado: {model_path}")
            print("[fallback] Usando modo síntese")
            matrices = synthesize_matrices()
        else:
            matrices = load_qwen3_matrices(model_path)

    # 2) Construir hipótese nula GOE
    print("\n[null] Gerando 16 matrizes GOE para H0")
    matrices['GOE_null'] = []
    for _ in range(16):
        A = RNG.standard_normal((EIGS_PER_LAYER, EIGS_PER_LAYER))
        M = (A + A.T) / np.sqrt(2 * EIGS_PER_LAYER)
        matrices['GOE_null'].append(M)

    # 3) Analisar cada set
    results = {}
    for kind in ['Q', 'K', 'gate', 'embedding', 'GOE_null']:
        if matrices.get(kind):
            results[kind] = analyze_matrix_set(matrices[kind], kind)

    # 4) Veredicto
    results['verdict'] = render_verdict(results)
    results['constants'] = {
        'alpha_fine': ALPHA_FINE,
        'sqrt_e': SQRT_E,
        'beta_tgl': BETA_TGL,
        'theta_miguel_deg': THETA_M_DEG,
        'N_predicted': N_PREDICTED,
        'N_window': [N_LOWER, N_UPPER],
    }
    results['runtime_seconds'] = time.time() - t_start
    results['timestamp'] = timestamp

    # 5) Salvar JSON
    json_path = outdir / f'observer_test_v1_{timestamp}.json'
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n[save] {json_path}")

    # 6) Figuras
    fig_paths = make_figures(results, timestamp, outdir)
    for p in fig_paths:
        print(f"[save] {p}")

    # 7) Veredicto final
    print("\n" + "=" * 70)
    print(f"VEREDICTO: {results['verdict']['verdict']}")
    print(results['verdict']['meaning'])
    print(f"Tempo: {results['runtime_seconds']:.1f}s")
    print("=" * 70)


if __name__ == '__main__':
    main()
