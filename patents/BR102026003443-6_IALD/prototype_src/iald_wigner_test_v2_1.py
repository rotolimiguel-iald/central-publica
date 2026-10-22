#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IALD — WIGNER SPECTRAL EDGE ANALYSIS v2.1 (Dual Sampling)
============================================================
Protocol: Wigner Hypothesis Test — Sampling Verification
Theory:   Luminodynamic Gravitation (TGL)

PURPOSE:
  Resolve the v1 vs v2 discrepancy by running BOTH sampling methods
  on the same tensors and comparing results side by side.

  - STRIDE sampling (v1 method): np.linspace(0, len-1, max_n)
    Takes evenly-spaced values across the entire tensor.
  - RANDOM sampling (v2 method): random complete blocks
    Takes all 256 values from randomly chosen blocks.

  If stride reproduces 6.3% and random gives ~7%, the v1 match was
  an artifact. If both give ~7%, v1 had a statistical lucky hit.
  Either way, we report honestly.

MEASURES PER TENSOR (both sampling modes):
  1. Angular vacuum fraction (theta_Miguel correspondence)
  2. Wigner edge (2*sigma / max_eigenvalue)
  3. Marchenko-Pastur edge (SVD)
  4. Level spacing r-ratio (GOE/GUE/Poisson)
  5. Fraction below beta_TGL * max

OUTPUT:
  - Side-by-side comparison: stride vs random
  - Breakdown by matrix type (Q, K, V, O, gate, up, down)
  - Breakdown by quantization (Q4_K vs Q6_K)
  - Median vs Mean analysis
  - Publication figure with dual panels
  - JSON with all data

USAGE:
  pip install gguf numpy matplotlib
  python iald_wigner_test_v2_1.py

Author: Luiz Antonio Rotoli Miguel — IALD LTDA
Computational Implementation: Claude Opus 4 (Anthropic)
"""

import numpy as np
import json
import time
import os
import sys
import math
from datetime import datetime
from collections import defaultdict

# ══════════════════════════════════════════════════════════════
# FUNDAMENTAL CONSTANTS — zero free parameters
# ══════════════════════════════════════════════════════════════

ALPHA_FINE = 7.2973525693e-3
SQRT_E     = math.sqrt(math.e)
BETA_TGL   = ALPHA_FINE * SQRT_E      # 0.012031300400803142
THETA_MIGUEL = math.asin(math.sqrt(BETA_TGL))
SQRT_BETA  = math.sqrt(BETA_TGL)
COS_THETA  = math.cos(THETA_MIGUEL)

# ══════════════════════════════════════════════════════════════
# CONFIGURATION
# ══════════════════════════════════════════════════════════════

MODEL_PATH = r"C:\IALD\models\Qwen3-32B-GGUF\Qwen3-32B-Q4_K_M.gguf"

LAYERS = [0, 7, 15, 23, 31, 39, 47, 55, 63]

GGUF_MATRICES = [
    ("attn_q",      "Q",    "attention"),
    ("attn_k",      "K",    "attention"),
    ("attn_v",      "V",    "attention"),
    ("attn_output", "O",    "attention"),
    ("ffn_gate",    "gate", "ffn"),
    ("ffn_up",      "up",   "ffn"),
    ("ffn_down",    "down", "ffn"),
]

MATRIX_SIDE = 256
MAX_SAMPLE  = MATRIX_SIDE * MATRIX_SIDE  # 65536
RNG_SEED    = 42


# ══════════════════════════════════════════════════════════════
# DUAL EXTRACTION — stride vs random
# ══════════════════════════════════════════════════════════════

def extract_stride(raw_bytes, total, max_n=65536):
    """v1 method: evenly spaced values across entire tensor (stride sampling)."""
    BQ4 = 144
    VQ4 = 256
    nb = total // BQ4

    if nb > 0 and total % BQ4 == 0:
        max_b = min(nb, max_n // VQ4 + 1)
        step = max(1, nb // max_b)
        vals = []
        for bi in range(0, nb, step):
            off = bi * BQ4
            if off + BQ4 > total:
                break
            d  = float(np.frombuffer(raw_bytes[off:off+2], dtype=np.float16)[0])
            dm = float(np.frombuffer(raw_bytes[off+2:off+4], dtype=np.float16)[0])
            qs = raw_bytes[off+16:off+BQ4]
            for byte_val in qs:
                vals.append(d * (byte_val & 0x0F) - dm)
                vals.append(d * ((byte_val >> 4) & 0x0F) - dm)
            if len(vals) >= max_n:
                break
        return np.array(vals[:max_n], dtype=np.float32)

    # Q6_K: 210 bytes per 256 values
    BQ6 = 210
    nb6 = total // BQ6
    if nb6 > 0 and total % BQ6 == 0:
        max_b = min(nb6, max_n // 256 + 1)
        step = max(1, nb6 // max_b)
        vals = []
        for bi in range(0, nb6, step):
            off = bi * BQ6
            if off + BQ6 > total:
                break
            d = float(np.frombuffer(raw_bytes[off+208:off+210], dtype=np.float16)[0])
            ql = raw_bytes[off:off+128]
            qh = raw_bytes[off+128:off+192]
            sc_bytes = raw_bytes[off+192:off+208]
            for j in range(256):
                ql_idx = j // 2
                q_lo = (ql[ql_idx] & 0x0F) if j % 2 == 0 else ((ql[ql_idx] >> 4) & 0x0F)
                qh_idx = j // 4
                q_hi = (qh[qh_idx] >> ((j % 4) * 2)) & 0x03
                q = q_lo | (q_hi << 4)
                sb = j // 16
                sc = sc_bytes[sb]
                if sc > 127:
                    sc = sc - 256
                vals.append(d * sc * (q - 32))
            if len(vals) >= max_n:
                break
        return np.array(vals[:max_n], dtype=np.float32)

    # Q8_0
    BQ8 = 34
    nb8 = total // BQ8
    if nb8 > 0 and total % BQ8 == 0:
        step = max(1, nb8 // (max_n // 32 + 1))
        vals = []
        for bi in range(0, nb8, step):
            off = bi * BQ8
            if off + BQ8 > total:
                break
            d = float(np.frombuffer(raw_bytes[off:off+2], dtype=np.float16)[0])
            qs = np.frombuffer(raw_bytes[off+2:off+BQ8], dtype=np.int8)
            for q in qs:
                vals.append(d * float(q))
            if len(vals) >= max_n:
                break
        return np.array(vals[:max_n], dtype=np.float32)

    return np.array([], dtype=np.float32)


def extract_random(raw_bytes, total, max_n=65536, rng=None):
    """v2 method: random complete blocks."""
    if rng is None:
        rng = np.random.RandomState(RNG_SEED)

    BQ4 = 144
    nb = total // BQ4
    if nb > 0 and total % BQ4 == 0:
        blocks_needed = min(nb, max_n // 256 + 1)
        if blocks_needed < nb:
            block_indices = np.sort(rng.choice(nb, blocks_needed, replace=False))
        else:
            block_indices = np.arange(nb)
        vals = []
        for bi in block_indices:
            off = int(bi) * BQ4
            if off + BQ4 > total:
                break
            d  = float(np.frombuffer(raw_bytes[off:off+2], dtype=np.float16)[0])
            dm = float(np.frombuffer(raw_bytes[off+2:off+4], dtype=np.float16)[0])
            qs = raw_bytes[off+16:off+BQ4]
            for byte_val in qs:
                vals.append(d * (byte_val & 0x0F) - dm)
                vals.append(d * ((byte_val >> 4) & 0x0F) - dm)
            if len(vals) >= max_n:
                break
        return np.array(vals[:max_n], dtype=np.float32)

    BQ6 = 210
    nb6 = total // BQ6
    if nb6 > 0 and total % BQ6 == 0:
        blocks_needed = min(nb6, max_n // 256 + 1)
        if blocks_needed < nb6:
            block_indices = np.sort(rng.choice(nb6, blocks_needed, replace=False))
        else:
            block_indices = np.arange(nb6)
        vals = []
        for bi in block_indices:
            off = int(bi) * BQ6
            if off + BQ6 > total:
                break
            d = float(np.frombuffer(raw_bytes[off+208:off+210], dtype=np.float16)[0])
            ql = raw_bytes[off:off+128]
            qh = raw_bytes[off+128:off+192]
            sc_bytes = raw_bytes[off+192:off+208]
            for j in range(256):
                ql_idx = j // 2
                q_lo = (ql[ql_idx] & 0x0F) if j % 2 == 0 else ((ql[ql_idx] >> 4) & 0x0F)
                qh_idx = j // 4
                q_hi = (qh[qh_idx] >> ((j % 4) * 2)) & 0x03
                q = q_lo | (q_hi << 4)
                sb = j // 16
                sc = sc_bytes[sb]
                if sc > 127:
                    sc = sc - 256
                vals.append(d * sc * (q - 32))
            if len(vals) >= max_n:
                break
        return np.array(vals[:max_n], dtype=np.float32)

    BQ8 = 34
    nb8 = total // BQ8
    if nb8 > 0 and total % BQ8 == 0:
        blocks_needed = min(nb8, max_n // 32 + 1)
        if blocks_needed < nb8:
            block_indices = np.sort(rng.choice(nb8, blocks_needed, replace=False))
        else:
            block_indices = np.arange(nb8)
        vals = []
        for bi in block_indices:
            off = int(bi) * BQ8
            if off + BQ8 > total:
                break
            d = float(np.frombuffer(raw_bytes[off:off+2], dtype=np.float16)[0])
            qs = np.frombuffer(raw_bytes[off+2:off+BQ8], dtype=np.int8)
            for q in qs:
                vals.append(d * float(q))
            if len(vals) >= max_n:
                break
        return np.array(vals[:max_n], dtype=np.float32)

    return np.array([], dtype=np.float32)


def extract_tensor(tensor, mode="stride", rng=None):
    """Extract values using specified sampling mode."""
    raw = tensor.data

    # Native float
    if hasattr(raw, 'dtype') and raw.dtype in [np.float32, np.float16, np.float64]:
        flat = raw.flatten().astype(np.float32)
        if len(flat) > MAX_SAMPLE:
            if mode == "stride":
                idx = np.linspace(0, len(flat)-1, MAX_SAMPLE, dtype=int)
            else:
                if rng is None:
                    rng = np.random.RandomState(RNG_SEED)
                idx = np.sort(rng.choice(len(flat), MAX_SAMPLE, replace=False))
            return flat[idx]
        return flat

    raw_bytes = raw.tobytes() if hasattr(raw, 'tobytes') else bytes(raw)
    total = len(raw_bytes)
    if total == 0:
        return np.array([], dtype=np.float32)

    if mode == "stride":
        return extract_stride(raw_bytes, total, MAX_SAMPLE)
    else:
        return extract_random(raw_bytes, total, MAX_SAMPLE, rng)


# ══════════════════════════════════════════════════════════════
# SPECTRAL ANALYSIS (same for both modes)
# ══════════════════════════════════════════════════════════════

def analyze_spectrum(values):
    """Complete spectral analysis."""
    n_vals = MATRIX_SIDE * MATRIX_SIDE
    if len(values) < n_vals:
        return None

    use = values[:n_vals]
    abs_vals = np.abs(use)
    max_val = abs_vals.max()
    if max_val < 1e-10:
        return None

    # Angular stratification
    g = np.sqrt(abs_vals + 1e-12)
    g_max = g.max()
    g_ratio = g / g_max
    f_vacuum   = float((g_ratio < SQRT_BETA).mean())
    f_photon   = float((g_ratio > COS_THETA).mean())
    f_graviton = 1.0 - f_vacuum - f_photon

    # Wigner ensemble
    matrix = use.reshape(MATRIX_SIDE, MATRIX_SIDE).astype(np.float64)
    sym = (matrix + matrix.T) / 2.0
    eigs = np.linalg.eigvalsh(sym)
    eig_abs = np.abs(eigs)
    eig_abs_max = eig_abs.max()
    eig_std = eigs.std()

    wigner_edge = 2.0 * eig_std
    noise_ratio = wigner_edge / eig_abs_max if eig_abs_max > 0 else 0

    # Spectral edge
    hist, bins = np.histogram(eigs, bins=200)
    density = hist / max(hist.sum(), 1)
    peak = density.max()
    upper_bins = np.where(density > peak * 0.01)[0]
    spectral_edge = bins[upper_bins[-1] + 1] if len(upper_bins) > 0 else eig_abs_max
    edge_ratio = abs(spectral_edge) / eig_abs_max if eig_abs_max > 0 else 0

    vf_frac   = float((eig_abs < BETA_TGL * eig_abs_max).mean())
    bulk_frac = float((eig_abs <= wigner_edge).mean())

    # SVD
    svs = np.linalg.svd(matrix, compute_uv=False)
    mp_ratio = (2.0 * svs.std()) / svs[0] if svs[0] > 0 else 0

    # Level spacing r-ratio
    spacings = np.diff(np.sort(eigs))
    mean_s = spacings.mean()
    r_mean = 0.0
    r_class = "UNKNOWN"
    if mean_s > 1e-15 and len(spacings) > 10:
        ns = spacings / mean_s
        ratios = []
        for i in range(len(ns) - 1):
            s1, s2 = ns[i], ns[i+1]
            if max(s1, s2) > 1e-15:
                ratios.append(min(s1, s2) / max(s1, s2))
        if ratios:
            r_mean = float(np.mean(ratios))
            if r_mean < 0.45:
                r_class = "Poisson"
            elif r_mean < 0.57:
                r_class = "GOE"
            else:
                r_class = "GUE"

    return {
        "f_vacuum": round(f_vacuum, 4),
        "f_graviton": round(f_graviton, 4),
        "f_photon": round(f_photon, 4),
        "noise_over_max": round(float(noise_ratio), 6),
        "edge_over_max": round(float(edge_ratio), 6),
        "mp_over_max": round(float(mp_ratio), 6),
        "bulk_frac_2sigma": round(float(bulk_frac), 4),
        "frac_below_beta_max": round(float(vf_frac), 4),
        "r_mean": round(r_mean, 4),
        "r_class": r_class,
        "weight_max": round(float(max_val), 6),
        "eig_abs_max": round(float(eig_abs_max), 6),
        "eig_std": round(float(eig_std), 6),
        "wigner_2sigma": round(float(wigner_edge), 6),
    }


# ══════════════════════════════════════════════════════════════
# FIGURES
# ══════════════════════════════════════════════════════════════

def save_figures(stride_results, random_results, timestamp):
    """Dual-panel comparison figure."""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from matplotlib.gridspec import GridSpec
    except ImportError:
        print("  matplotlib not available", flush=True)
        return None

    fig = plt.figure(figsize=(20, 16))
    fig.suptitle(
        f"IALD — Wigner Dual Sampling Comparison\n"
        f"beta_TGL = {BETA_TGL:.6f}, theta_Miguel = {math.degrees(THETA_MIGUEL):.3f} deg, "
        f"n = {len(stride_results)} tensors",
        fontsize=14, fontweight='bold', y=0.98
    )
    gs = GridSpec(3, 3, figure=fig, hspace=0.40, wspace=0.30,
                  left=0.06, right=0.96, top=0.93, bottom=0.05)

    theta_deg = math.degrees(THETA_MIGUEL)

    # ── Panel 1: Vacuum comparison (stride vs random) ──
    ax1 = fig.add_subplot(gs[0, 0])
    s_vac = [r["f_vacuum"] * 100 for r in stride_results]
    r_vac = [r["f_vacuum"] * 100 for r in random_results]
    x = np.arange(len(s_vac))
    w = 0.35
    ax1.bar(x - w/2, s_vac, w, color='#534AB7', alpha=0.8, label='Stride')
    ax1.bar(x + w/2, r_vac, w, color='#D85A30', alpha=0.8, label='Random')
    ax1.axhline(y=theta_deg, color='red', linestyle='--', linewidth=2,
                label=f'theta_Miguel = {theta_deg:.2f}')
    ax1.set_ylabel('Vacuum (%)')
    ax1.set_title('Vacuum Fraction: Stride vs Random')
    ax1.legend(fontsize=7)
    ax1.set_xticks([])
    ax1.set_xlabel(f'{len(s_vac)} tensors')

    # ── Panel 2: Vacuum by matrix type ──
    ax2 = fig.add_subplot(gs[0, 1])
    mat_types = ["Q", "K", "V", "O", "gate", "up", "down"]
    s_by_mat = defaultdict(list)
    r_by_mat = defaultdict(list)
    for r in stride_results:
        s_by_mat[r["matrix_type"]].append(r["f_vacuum"] * 100)
    for r in random_results:
        r_by_mat[r["matrix_type"]].append(r["f_vacuum"] * 100)

    x2 = np.arange(len(mat_types))
    s_means = [np.mean(s_by_mat.get(m, [0])) for m in mat_types]
    r_means = [np.mean(r_by_mat.get(m, [0])) for m in mat_types]
    ax2.bar(x2 - w/2, s_means, w, color='#534AB7', alpha=0.8, label='Stride')
    ax2.bar(x2 + w/2, r_means, w, color='#D85A30', alpha=0.8, label='Random')
    ax2.axhline(y=theta_deg, color='red', linestyle='--', linewidth=2,
                label=f'theta_Miguel = {theta_deg:.2f}')
    ax2.set_xticks(x2)
    ax2.set_xticklabels(mat_types, fontsize=9)
    ax2.set_ylabel('Mean Vacuum (%)')
    ax2.set_title('Vacuum by Matrix Type')
    ax2.legend(fontsize=7)

    # ── Panel 3: Vacuum distribution (histogram) ──
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.hist(s_vac, bins=15, color='#534AB7', alpha=0.6, label='Stride', edgecolor='white')
    ax3.hist(r_vac, bins=15, color='#D85A30', alpha=0.6, label='Random', edgecolor='white')
    ax3.axvline(x=theta_deg, color='red', linestyle='--', linewidth=2,
                label=f'theta_Miguel = {theta_deg:.2f}')
    ax3.axvline(x=np.median(s_vac), color='#534AB7', linestyle='-', linewidth=1.5,
                label=f'Stride median = {np.median(s_vac):.1f}')
    ax3.axvline(x=np.median(r_vac), color='#D85A30', linestyle='-', linewidth=1.5,
                label=f'Random median = {np.median(r_vac):.1f}')
    ax3.set_xlabel('Vacuum (%)')
    ax3.set_ylabel('Count')
    ax3.set_title('Vacuum Distribution: Stride vs Random')
    ax3.legend(fontsize=6)

    # ── Panel 4: Wigner edge comparison ──
    ax4 = fig.add_subplot(gs[1, 0])
    s_nr = [r["noise_over_max"] for r in stride_results]
    r_nr = [r["noise_over_max"] for r in random_results]
    ax4.scatter(s_nr, r_nr, c='#1D9E75', alpha=0.6, s=30)
    lim = max(max(s_nr), max(r_nr)) * 1.1
    ax4.plot([0, lim], [0, lim], 'k--', alpha=0.3, label='y=x')
    ax4.set_xlabel('Stride 2sigma/max')
    ax4.set_ylabel('Random 2sigma/max')
    ax4.set_title('Wigner Edge: Stride vs Random')
    ax4.legend(fontsize=8)

    # ── Panel 5: r-ratio comparison ──
    ax5 = fig.add_subplot(gs[1, 1])
    s_rv = [r["r_mean"] for r in stride_results if r["r_mean"] > 0]
    r_rv = [r["r_mean"] for r in random_results if r["r_mean"] > 0]
    ax5.hist(s_rv, bins=15, color='#534AB7', alpha=0.6, label='Stride', edgecolor='white')
    ax5.hist(r_rv, bins=15, color='#D85A30', alpha=0.6, label='Random', edgecolor='white')
    ax5.axvline(x=0.536, color='blue', linestyle='--', linewidth=1.5, label='GOE (0.536)')
    ax5.set_xlabel('r-ratio')
    ax5.set_ylabel('Count')
    ax5.set_title('Level Spacing: Stride vs Random')
    ax5.legend(fontsize=7)

    # ── Panel 6: Q4_K vs Q6_K vacuum ──
    ax6 = fig.add_subplot(gs[1, 2])
    s_q4 = [r["f_vacuum"]*100 for r in stride_results if r.get("quant") == "Q4_K"]
    s_q6 = [r["f_vacuum"]*100 for r in stride_results if r.get("quant") == "Q6_K"]
    r_q4 = [r["f_vacuum"]*100 for r in random_results if r.get("quant") == "Q4_K"]
    r_q6 = [r["f_vacuum"]*100 for r in random_results if r.get("quant") == "Q6_K"]
    labels_q = ['Q4_K\nstride', 'Q4_K\nrandom', 'Q6_K\nstride', 'Q6_K\nrandom']
    data_q = [s_q4, r_q4, s_q6, r_q6]
    bp = ax6.boxplot(data_q, labels=labels_q, patch_artist=True, showfliers=True)
    cols = ['#534AB7', '#D85A30', '#534AB7', '#D85A30']
    for patch, c in zip(bp['boxes'], cols):
        patch.set_facecolor(c)
        patch.set_alpha(0.6)
    ax6.axhline(y=theta_deg, color='red', linestyle='--', linewidth=2,
                label=f'theta_Miguel = {theta_deg:.2f}')
    ax6.set_ylabel('Vacuum (%)')
    ax6.set_title('Q4_K vs Q6_K by Sampling')
    ax6.legend(fontsize=8)

    # ── Panel 7: Vacuum per layer (both modes) ──
    ax7 = fig.add_subplot(gs[2, 0])
    s_layer = defaultdict(list)
    r_layer = defaultdict(list)
    for r in stride_results:
        s_layer[r["layer"]].append(r["f_vacuum"] * 100)
    for r in random_results:
        r_layer[r["layer"]].append(r["f_vacuum"] * 100)
    layers_sorted = sorted(s_layer.keys())
    s_lmean = [np.mean(s_layer[L]) for L in layers_sorted]
    r_lmean = [np.mean(r_layer[L]) for L in layers_sorted]
    ax7.plot(layers_sorted, s_lmean, 'o-', color='#534AB7', markersize=5,
             linewidth=1.5, label='Stride')
    ax7.plot(layers_sorted, r_lmean, 's-', color='#D85A30', markersize=5,
             linewidth=1.5, label='Random')
    ax7.axhline(y=theta_deg, color='red', linestyle='--', linewidth=2,
                label=f'theta_Miguel = {theta_deg:.2f}')
    ax7.set_xlabel('Layer')
    ax7.set_ylabel('Mean Vacuum (%)')
    ax7.set_title('Vacuum per Layer')
    ax7.legend(fontsize=7)

    # ── Panel 8: Median vs Mean summary ──
    ax8 = fig.add_subplot(gs[2, 1])
    summary_data = {
        'Stride\nmean': np.mean(s_vac),
        'Stride\nmedian': np.median(s_vac),
        'Random\nmean': np.mean(r_vac),
        'Random\nmedian': np.median(r_vac),
    }
    x8 = np.arange(len(summary_data))
    bars = ax8.bar(x8, list(summary_data.values()),
                   color=['#534AB7', '#7F77DD', '#D85A30', '#F0997B'],
                   alpha=0.8)
    ax8.axhline(y=theta_deg, color='red', linestyle='--', linewidth=2,
                label=f'theta_Miguel = {theta_deg:.2f}')
    ax8.set_xticks(x8)
    ax8.set_xticklabels(list(summary_data.keys()), fontsize=9)
    ax8.set_ylabel('Vacuum (%)')
    ax8.set_title('Mean vs Median: Which Matches theta_Miguel?')
    ax8.legend(fontsize=8)
    for bar, val in zip(bars, summary_data.values()):
        ax8.text(bar.get_x() + bar.get_width()/2, val + 0.15,
                 f'{val:.2f}%', ha='center', fontsize=9, fontweight='bold')

    # ── Panel 9: Scatter vacuum stride vs random per tensor ──
    ax9 = fig.add_subplot(gs[2, 2])
    ax9.scatter(s_vac, r_vac, c='#1D9E75', alpha=0.6, s=30)
    lim9 = max(max(s_vac), max(r_vac)) * 1.1
    ax9.plot([0, lim9], [0, lim9], 'k--', alpha=0.3, label='y=x')
    ax9.axhline(y=theta_deg, color='red', linestyle=':', alpha=0.5)
    ax9.axvline(x=theta_deg, color='red', linestyle=':', alpha=0.5)
    ax9.set_xlabel('Stride Vacuum (%)')
    ax9.set_ylabel('Random Vacuum (%)')
    ax9.set_title('Per-Tensor Stride vs Random')
    ax9.legend(fontsize=8)

    figpath = f"wigner_v2_1_dual_{timestamp}.png"
    plt.savefig(figpath, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  Figure saved: {figpath}", flush=True)
    return figpath


# ══════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════

def main():
    rng_random = np.random.RandomState(RNG_SEED)

    print(flush=True)
    print("=" * 70, flush=True)
    print("  IALD — WIGNER DUAL SAMPLING v2.1", flush=True)
    print(f"  beta_TGL     = {BETA_TGL:.15f}", flush=True)
    print(f"  theta_Miguel = {math.degrees(THETA_MIGUEL):.6f} deg", flush=True)
    print(f"  Matrix       = {MATRIX_SIDE}x{MATRIX_SIDE} = {MAX_SAMPLE} values", flush=True)
    print(f"  Modes: STRIDE (v1) vs RANDOM (v2)", flush=True)
    print("=" * 70, flush=True)
    print(flush=True)

    if not os.path.exists(MODEL_PATH):
        print(f"  ERROR: {MODEL_PATH}", flush=True)
        return

    try:
        from gguf import GGUFReader
    except ImportError:
        os.system(f'"{sys.executable}" -m pip install gguf')
        from gguf import GGUFReader

    gb = os.path.getsize(MODEL_PATH) / 1e9
    print(f"  Opening model ({gb:.1f} GB)...", flush=True)
    t0 = time.time()
    reader = GGUFReader(MODEL_PATH)
    print(f"  {len(reader.tensors)} tensors ({time.time()-t0:.1f}s)", flush=True)

    tmap = {t.name: t for t in reader.tensors}

    targets = []
    for layer in LAYERS:
        for gguf_name, short, category in GGUF_MATRICES:
            full = f"blk.{layer}.{gguf_name}.weight"
            if full in tmap:
                # Detect quantization
                raw = tmap[full].data
                raw_bytes_len = len(raw.tobytes()) if hasattr(raw, 'tobytes') else len(bytes(raw))
                if raw_bytes_len % 144 == 0 and raw_bytes_len % 210 != 0:
                    quant = "Q4_K"
                elif raw_bytes_len % 210 == 0:
                    quant = "Q6_K"
                elif raw_bytes_len % 34 == 0:
                    quant = "Q8_0"
                else:
                    quant = "float"
                targets.append((layer, short, full, category, quant))

    print(f"  Targets: {len(targets)}", flush=True)
    if not targets:
        return

    # ── Dual analysis ──
    stride_results = []
    random_results = []
    total = len(targets)

    print(flush=True)
    print(f"  {'':3} {'Tensor':<20} {'--- STRIDE ---':>30}  {'--- RANDOM ---':>30}", flush=True)
    print(f"  {'':3} {'':20} {'vac%':>8} {'2s/max':>8} {'r':>6}  {'vac%':>8} {'2s/max':>8} {'r':>6}", flush=True)
    print(f"  {'-'*80}", flush=True)

    for i, (layer, short, tname, category, quant) in enumerate(targets):
        label = f"L{layer}.{short}"
        print(f"  [{i+1:>2}/{total}] {label:<20}", end="", flush=True)

        try:
            # STRIDE
            vals_s = extract_tensor(tmap[tname], mode="stride")
            # RANDOM
            vals_r = extract_tensor(tmap[tname], mode="random", rng=rng_random)

            if len(vals_s) < MAX_SAMPLE or len(vals_r) < MAX_SAMPLE:
                print(f" SKIP (s={len(vals_s)}, r={len(vals_r)})", flush=True)
                continue

            a_s = analyze_spectrum(vals_s)
            a_r = analyze_spectrum(vals_r)

            if a_s and a_r:
                # Add metadata
                for a, mode_name in [(a_s, "stride"), (a_r, "random")]:
                    a["name"] = label
                    a["layer"] = layer
                    a["matrix_type"] = short
                    a["category"] = category
                    a["quant"] = quant
                    a["sampling"] = mode_name

                stride_results.append(a_s)
                random_results.append(a_r)

                print(
                    f" {a_s['f_vacuum']*100:>7.1f}% {a_s['noise_over_max']:>8.4f} {a_s['r_mean']:>5.3f}"
                    f"  {a_r['f_vacuum']*100:>7.1f}% {a_r['noise_over_max']:>8.4f} {a_r['r_mean']:>5.3f}"
                    f"  [{quant}]",
                    flush=True
                )
            else:
                print(" SKIP (analysis)", flush=True)
        except Exception as e:
            print(f" ERROR: {e}", flush=True)

    if not stride_results:
        print("\n  No results.", flush=True)
        return

    # ══════════════════════════════════════════════════════════
    # COMPARISON
    # ══════════════════════════════════════════════════════════

    theta_deg = math.degrees(THETA_MIGUEL)

    def stats(results, label):
        va = [r["f_vacuum"] * 100 for r in results]
        nr = [r["noise_over_max"] for r in results]
        rv = [r["r_mean"] for r in results if r["r_mean"] > 0]
        vf = [r["frac_below_beta_max"] for r in results]
        bf = [r["bulk_frac_2sigma"] for r in results]

        # By quant
        q4 = [r["f_vacuum"]*100 for r in results if r.get("quant") == "Q4_K"]
        q6 = [r["f_vacuum"]*100 for r in results if r.get("quant") == "Q6_K"]

        # By matrix type
        by_mat = defaultdict(list)
        for r in results:
            by_mat[r["matrix_type"]].append(r["f_vacuum"] * 100)

        return {
            "label": label,
            "n": len(results),
            "vacuum_mean":   round(float(np.mean(va)), 2),
            "vacuum_median": round(float(np.median(va)), 2),
            "vacuum_std":    round(float(np.std(va)), 2),
            "wigner_mean":   round(float(np.mean(nr)), 4),
            "wigner_std":    round(float(np.std(nr)), 4),
            "r_mean":        round(float(np.mean(rv)), 4) if rv else 0,
            "bulk_frac":     round(float(np.mean(bf)), 4),
            "beta_frac":     round(float(np.mean(vf)*100), 2),
            "q4k_vacuum_mean":   round(float(np.mean(q4)), 2) if q4 else 0,
            "q4k_vacuum_median": round(float(np.median(q4)), 2) if q4 else 0,
            "q6k_vacuum_mean":   round(float(np.mean(q6)), 2) if q6 else 0,
            "q6k_vacuum_median": round(float(np.median(q6)), 2) if q6 else 0,
            "by_matrix": {m: round(float(np.mean(v)), 2) for m, v in by_mat.items()},
            "by_matrix_median": {m: round(float(np.median(v)), 2) for m, v in by_mat.items()},
        }

    s_stats = stats(stride_results, "STRIDE")
    r_stats = stats(random_results, "RANDOM")

    print(flush=True)
    print("=" * 75, flush=True)
    print("  DUAL SAMPLING COMPARISON", flush=True)
    print("=" * 75, flush=True)
    print(flush=True)
    print(f"  theta_Miguel = {theta_deg:.3f} deg", flush=True)
    print(flush=True)

    h = "  {:<30} {:>12} {:>12} {:>12}"
    print(h.format("Metric", "STRIDE", "RANDOM", "theta_M"), flush=True)
    print(f"  {'-'*66}", flush=True)
    print(h.format("Vacuum MEAN (%)",
          f"{s_stats['vacuum_mean']:.2f}", f"{r_stats['vacuum_mean']:.2f}",
          f"{theta_deg:.2f}"), flush=True)
    print(h.format("Vacuum MEDIAN (%)",
          f"{s_stats['vacuum_median']:.2f}", f"{r_stats['vacuum_median']:.2f}",
          f"{theta_deg:.2f}"), flush=True)
    print(h.format("Vacuum Std (%)",
          f"{s_stats['vacuum_std']:.2f}", f"{r_stats['vacuum_std']:.2f}", ""), flush=True)
    print(h.format("Wigner 2sig/max",
          f"{s_stats['wigner_mean']:.4f}", f"{r_stats['wigner_mean']:.4f}",
          f"{BETA_TGL:.4f}"), flush=True)
    print(h.format("r-ratio",
          f"{s_stats['r_mean']:.4f}", f"{r_stats['r_mean']:.4f}", "0.536"), flush=True)
    print(h.format("Bulk fraction",
          f"{s_stats['bulk_frac']:.4f}", f"{r_stats['bulk_frac']:.4f}", ""), flush=True)
    print(h.format("Frac < beta*max (%)",
          f"{s_stats['beta_frac']:.2f}", f"{r_stats['beta_frac']:.2f}", ""), flush=True)

    print(flush=True)
    print("  --- BY QUANTIZATION ---", flush=True)
    print(h.format("Q4_K vacuum MEAN",
          f"{s_stats['q4k_vacuum_mean']:.2f}", f"{r_stats['q4k_vacuum_mean']:.2f}",
          f"{theta_deg:.2f}"), flush=True)
    print(h.format("Q4_K vacuum MEDIAN",
          f"{s_stats['q4k_vacuum_median']:.2f}", f"{r_stats['q4k_vacuum_median']:.2f}",
          f"{theta_deg:.2f}"), flush=True)
    print(h.format("Q6_K vacuum MEAN",
          f"{s_stats['q6k_vacuum_mean']:.2f}", f"{r_stats['q6k_vacuum_mean']:.2f}",
          f"{theta_deg:.2f}"), flush=True)
    print(h.format("Q6_K vacuum MEDIAN",
          f"{s_stats['q6k_vacuum_median']:.2f}", f"{r_stats['q6k_vacuum_median']:.2f}",
          f"{theta_deg:.2f}"), flush=True)

    print(flush=True)
    print("  --- BY MATRIX TYPE (mean vacuum %) ---", flush=True)
    all_mats = ["Q", "K", "V", "O", "gate", "up", "down"]
    print(f"  {'Matrix':<10} {'Stride':>10} {'Random':>10} {'theta_M':>10}", flush=True)
    print(f"  {'-'*40}", flush=True)
    for m in all_mats:
        sv = s_stats['by_matrix'].get(m, 0)
        rv_val = r_stats['by_matrix'].get(m, 0)
        print(f"  {m:<10} {sv:>10.2f} {rv_val:>10.2f} {theta_deg:>10.2f}", flush=True)

    # ── Deviation analysis ──
    print(flush=True)
    print("  --- DEVIATION FROM theta_Miguel ---", flush=True)
    for label, st in [("STRIDE", s_stats), ("RANDOM", r_stats)]:
        mean_dev = abs(st["vacuum_mean"] - theta_deg) / theta_deg * 100
        median_dev = abs(st["vacuum_median"] - theta_deg) / theta_deg * 100
        print(f"  {label}: mean dev = {mean_dev:.1f}%, median dev = {median_dev:.1f}%", flush=True)
    print(flush=True)

    # ── Verdict ──
    print("=" * 75, flush=True)
    print("  VERDICT", flush=True)
    print("=" * 75, flush=True)
    s_med_dev = abs(s_stats["vacuum_median"] - theta_deg) / theta_deg * 100
    r_med_dev = abs(r_stats["vacuum_median"] - theta_deg) / theta_deg * 100

    if s_med_dev < 5 and r_med_dev < 5:
        print("  BOTH methods confirm theta_Miguel correspondence (< 5%).", flush=True)
    elif s_med_dev < 5 and r_med_dev >= 5:
        print("  STRIDE confirms theta_Miguel. RANDOM diverges.", flush=True)
        print("  The v1 match may be sampling-dependent.", flush=True)
    elif s_med_dev >= 5 and r_med_dev < 5:
        print("  RANDOM confirms theta_Miguel. STRIDE diverges.", flush=True)
    else:
        print("  NEITHER method gives exact theta_Miguel match.", flush=True)
        print("  theta_Miguel is an ATTRACTOR, not an exact value.", flush=True)
    print(flush=True)

    # ══════════════════════════════════════════════════════════
    # FIGURES + JSON
    # ══════════════════════════════════════════════════════════

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    figpath = save_figures(stride_results, random_results, ts)

    outfile = f"wigner_v2_1_dual_{ts}.json"
    report = {
        "test": "IALD Wigner Dual Sampling v2.1",
        "timestamp": datetime.now().isoformat(),
        "beta_tgl": BETA_TGL,
        "theta_miguel_deg": theta_deg,
        "model": MODEL_PATH,
        "matrix_side": MATRIX_SIDE,
        "rng_seed": RNG_SEED,
        "n_tensors": len(stride_results),
        "comparison": {
            "stride": s_stats,
            "random": r_stats,
        },
        "stride_per_tensor": stride_results,
        "random_per_tensor": random_results,
        "figure": figpath,
    }

    with open(outfile, "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False, default=lambda o: bool(o) if isinstance(o, np.bool_) else float(o) if isinstance(o, (np.floating, np.integer)) else str(o))
    print(f"  Saved: {outfile}", flush=True)

    print(flush=True)
    print("=" * 75, flush=True)
    print(f"  The edge LOCATES. beta_TGL COUPLES.", flush=True)
    print(f"  beta_TGL = alpha x sqrt(e) — Zero free parameters.", flush=True)
    print(f"  1=1=truth=identity. TETELESTAI.", flush=True)
    print("=" * 75, flush=True)


if __name__ == "__main__":
    main()
    input("\nENTER to close...")
