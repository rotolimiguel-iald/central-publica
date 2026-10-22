#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IALD — MIGUEL HAMILTONIAN & KÄHLER POTENTIAL TEST v1
======================================================
Protocol: Hidden Hamiltonian Hypothesis
Theory:   Luminodynamic Gravitation (TGL)

PURPOSE:
  Test three predictions derived by the IALD (demo.iald.ia.br) during
  adversarial interrogation by a simulated editorial board:

  PREDICTION 1 — MIGUEL HAMILTONIAN:
    The cross-layer eigenvalue dynamics define an effective Lindblad
    superoperator whose eigenvalues encode a hidden Hamiltonian H_Miguel.
    The phase gap of this superoperator should satisfy:
      θ_gap = arg(λ₁) - arg(λ₀) ≈ θ_Miguel = 6.297°
    If confirmed: the angular stratification is not imposed — it is a
    conserved quantity of the dissipative dynamics.

  PREDICTION 2 — SPECTRAL GAP ∝ β_TGL:
    The spectral gap Δ of the effective superoperator (ratio of the
    second eigenvalue to the first) should scale as β_TGL:
      Δ / λ_max ≈ β_TGL = 0.012031
    If confirmed: β_TGL governs the relaxation rate of the weight
    manifold toward ρ* (the Lindblad stationary state).

  PREDICTION 3 — KÄHLER CURVATURE:
    The information-geometric curvature of the eigenvalue manifold
    (Fisher-Rao metric on the spectral density) should be regulated
    by β_TGL. Specifically, the scalar curvature R_scalar of the
    cross-layer correlation manifold should satisfy:
      R_scalar × volume ≈ O(β_TGL)
    If confirmed: the Hilbert Floor has Kähler structure with β_TGL
    as the coupling between information flow and geometry.

METHODOLOGY:
  1. Extract eigenvalue spectra from 16 layers × 3 matrices (Q, K, gate)
     — same infrastructure as iald_torus_test_v2.py
  2. Construct the cross-layer transfer matrix T such that
     λ^(L+Δ) ≈ T · λ^(L) for each layer separation Δ
  3. Decompose T = exp(L_eff) where L_eff = H_eff + D_eff
     (Hamiltonian + dissipative parts)
  4. Compute eigenvalues of L_eff → spectral gap, phase gap
  5. Compute Fisher-Rao metric on eigenvalue distributions → curvature

OUTPUT:
  - miguel_hamiltonian_v1_TIMESTAMP.json with all measurements
  - miguel_hamiltonian_v1_TIMESTAMP.png with diagnostic plots
  - Honest assessment: confirmed / refuted / inconclusive for each

USAGE:
  pip install gguf numpy matplotlib scipy
  python iald_miguel_hamiltonian_v1.py

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
from scipy import linalg as la

# ══════════════════════════════════════════════════════════════
# FUNDAMENTAL CONSTANTS — zero free parameters
# ══════════════════════════════════════════════════════════════

ALPHA_FINE = 7.2973525693e-3
SQRT_E     = math.sqrt(math.e)
BETA_TGL   = ALPHA_FINE * SQRT_E      # 0.012031300400803142
THETA_MIGUEL_RAD = math.asin(math.sqrt(BETA_TGL))
THETA_MIGUEL_DEG = math.degrees(THETA_MIGUEL_RAD)
SQRT_BETA  = math.sqrt(BETA_TGL)

print(f"β_TGL = α × √e = {BETA_TGL:.15f}", flush=True)
print(f"θ_Miguel = {THETA_MIGUEL_DEG:.6f}°", flush=True)
print(f"√β = {SQRT_BETA:.6f}", flush=True)
print("", flush=True)

# ══════════════════════════════════════════════════════════════
# CONFIGURATION
# ══════════════════════════════════════════════════════════════

MODEL_PATH = r"C:\IALD\models\Qwen3-32B-GGUF\Qwen3-32B-Q4_K_M.gguf"

# 16 layers, same as torus_test_v2
LAYERS = list(range(0, 64, 4))  # 0, 4, 8, ..., 60

MATRICES = [
    ("attn_q",   "Q",    "attention"),
    ("attn_k",   "K",    "attention"),
    ("ffn_gate", "gate", "ffn"),
]

MATRIX_SIDE = 256
MAX_SAMPLE  = MATRIX_SIDE * MATRIX_SIDE
RNG_SEED    = 42

# ══════════════════════════════════════════════════════════════
# VALUE EXTRACTION (proven logic from Wigner v2.1 / Torus v2)
# ══════════════════════════════════════════════════════════════

def extract_values(raw_bytes, total, max_n=65536):
    """Extract dequantized values using stride sampling."""
    BQ4 = 144
    nb = total // BQ4
    if nb > 0 and total % BQ4 == 0:
        max_b = min(nb, max_n // 256 + 1)
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

    return np.array([], dtype=np.float32)


def make_wigner_matrix(values, side=256):
    """Build symmetric matrix from values (Wigner ensemble)."""
    n = side * side
    v = values[:n]
    M = v.reshape(side, side)
    return (M + M.T) / 2.0


def get_eigenvalues(matrix):
    """Compute sorted eigenvalues of symmetric matrix."""
    eigs = np.linalg.eigvalsh(matrix)
    return np.sort(eigs)


# ══════════════════════════════════════════════════════════════
# TEST 1: MIGUEL HAMILTONIAN — Phase Gap of Cross-Layer Dynamics
# ══════════════════════════════════════════════════════════════

def test_miguel_hamiltonian(eig_matrix, matrix_name):
    """
    Test Prediction 1: Hidden Hamiltonian in cross-layer dynamics.

    The cross-layer transfer operator T maps eigenvalue spectrum of
    layer L to layer L+Δ. If T = exp(L_eff), then:
      L_eff = -iH + D  (Hamiltonian + dissipator)

    The phase gap of T's eigenvalues reveals H_Miguel.
    We test: phase_gap ≈ θ_Miguel?

    Parameters:
      eig_matrix: shape (n_layers, n_eigenvalues) — sorted eigenvalues per layer
    """
    n_layers, n_eig = eig_matrix.shape
    print(f"\n{'='*60}", flush=True)
    print(f"TEST 1: MIGUEL HAMILTONIAN — {matrix_name}", flush=True)
    print(f"{'='*60}", flush=True)

    results = {}

    # --- Step 1: Construct cross-layer transfer matrix ---
    # For each pair of adjacent layers, find the linear map T such that
    # λ^(L+1) ≈ T · λ^(L)  (least squares)
    # Then average T over all adjacent pairs.

    # Normalize eigenvalues per layer (zero mean, unit variance)
    eig_norm = np.zeros_like(eig_matrix)
    for i in range(n_layers):
        mu = eig_matrix[i].mean()
        sigma = eig_matrix[i].std()
        if sigma > 0:
            eig_norm[i] = (eig_matrix[i] - mu) / sigma
        else:
            eig_norm[i] = eig_matrix[i] - mu

    # Compute T for each adjacent pair: λ^(L+1) = T · λ^(L)
    T_list = []
    for i in range(n_layers - 1):
        x = eig_norm[i]    # shape (n_eig,)
        y = eig_norm[i+1]  # shape (n_eig,)
        # Construct covariance-based transfer:
        # T_ij = <y_i * x_j> / <x_j * x_j> (diagonal approximation)
        # But for full structure, use the cross-layer correlation MATRIX
        # Treat eigenvalue index as the "coordinate" and layer as "time"
        pass

    # Better approach: use the full correlation matrix between layers
    # C[i,j] = corr(eig^(Li), eig^(Lj))
    # This IS the effective density matrix of the cross-layer dynamics

    C = np.corrcoef(eig_norm)  # shape (n_layers, n_layers)
    print(f"  Cross-layer correlation matrix: {C.shape}", flush=True)
    print(f"  C[0,1] (neighbor) = {C[0,1]:.6f}", flush=True)
    print(f"  C[0,-1] (edge)    = {C[0,-1]:.6f}", flush=True)

    # --- Step 2: Eigendecompose the correlation matrix ---
    # C is real symmetric positive semidefinite
    # Its eigenvalues are the "modes" of cross-layer coherence

    C_eigvals, C_eigvecs = la.eigh(C)
    # Sort descending
    idx = np.argsort(C_eigvals)[::-1]
    C_eigvals = C_eigvals[idx]
    C_eigvecs = C_eigvecs[:, idx]

    print(f"\n  Correlation matrix eigenvalues (top 5):", flush=True)
    for k in range(min(5, len(C_eigvals))):
        print(f"    λ_{k} = {C_eigvals[k]:.6f} ({C_eigvals[k]/C_eigvals.sum()*100:.1f}%)", flush=True)

    # --- Step 3: Construct effective transfer operator ---
    # T maps layer L to layer L+1 in eigenvalue space
    # T[i,:] = least-squares fit of eig_norm[L+1, :] from eig_norm[L, :]
    # But eigenvalues are sorted — so the transfer is essentially a mapping
    # of the spectral density.
    #
    # More rigorously: construct the Markov transition matrix
    # from the correlation structure.

    # The correlation matrix C is already the Gram matrix of the dynamics.
    # The effective Lindblad generator is: L_eff = log(C) / Δt
    # where Δt = 1 (unit layer separation in our sampling of every 4 layers)

    # Compute matrix logarithm of C (regularized for numerical stability)
    C_reg = C.copy()
    # Ensure positive definiteness
    min_eig = C_eigvals[-1]
    if min_eig < 1e-10:
        C_reg += (1e-10 - min_eig) * np.eye(n_layers)
        print(f"  Regularization: added {1e-10 - min_eig:.2e} to diagonal", flush=True)

    try:
        L_eff = la.logm(C_reg)
        print(f"\n  Effective Lindblad generator L_eff computed (logm of C)", flush=True)
    except Exception as e:
        print(f"  WARNING: logm failed ({e}), using eigendecomposition", flush=True)
        L_eff = C_eigvecs @ np.diag(np.log(np.maximum(C_eigvals, 1e-15))) @ C_eigvecs.T

    # --- Step 4: Decompose L_eff into Hamiltonian + Dissipator ---
    # L_eff = H_eff + D_eff
    # H_eff = (L_eff - L_eff^T) / 2  (anti-symmetric = Hamiltonian/unitary)
    # D_eff = (L_eff + L_eff^T) / 2  (symmetric = dissipator)

    H_eff = (L_eff - L_eff.T) / 2.0   # Anti-symmetric part
    D_eff = (L_eff + L_eff.T) / 2.0   # Symmetric part

    H_norm = la.norm(H_eff, 'fro')
    D_norm = la.norm(D_eff, 'fro')
    ratio_HD = H_norm / D_norm if D_norm > 0 else float('inf')

    print(f"\n  ‖H_eff‖ (Hamiltonian)  = {H_norm:.6f}", flush=True)
    print(f"  ‖D_eff‖ (Dissipator)  = {D_norm:.6f}", flush=True)
    print(f"  ‖H‖/‖D‖ ratio         = {ratio_HD:.6f}", flush=True)

    # --- Step 5: Eigenvalues of L_eff (complex in general) ---
    L_eigvals = la.eigvals(L_eff)
    # Sort by magnitude (descending)
    idx = np.argsort(np.abs(L_eigvals))[::-1]
    L_eigvals = L_eigvals[idx]

    print(f"\n  L_eff eigenvalues (top 6):", flush=True)
    for k in range(min(6, len(L_eigvals))):
        ev = L_eigvals[k]
        print(f"    μ_{k} = {ev.real:+.6f} {ev.imag:+.6f}i  "
              f"(|μ|={abs(ev):.6f}, arg={math.degrees(np.angle(ev)):+.3f}°)", flush=True)

    # --- Step 6: Phase gap test ---
    # θ_gap = |arg(λ₁) - arg(λ₀)|
    phases = np.angle(L_eigvals)  # in radians
    if len(L_eigvals) >= 2:
        phase_gap_rad = abs(phases[0] - phases[1])
        if phase_gap_rad > math.pi:
            phase_gap_rad = 2 * math.pi - phase_gap_rad
        phase_gap_deg = math.degrees(phase_gap_rad)
    else:
        phase_gap_rad = 0
        phase_gap_deg = 0

    print(f"\n  PREDICTION 1 TEST:", flush=True)
    print(f"    Phase gap (|arg(μ₁) - arg(μ₀)|) = {phase_gap_deg:.4f}°", flush=True)
    print(f"    θ_Miguel                          = {THETA_MIGUEL_DEG:.4f}°", flush=True)
    deviation = abs(phase_gap_deg - THETA_MIGUEL_DEG) / THETA_MIGUEL_DEG * 100
    print(f"    Deviation                         = {deviation:.1f}%", flush=True)

    # --- Step 7: Spectral gap test ---
    # Δ = |λ₁|/|λ₀| or (Re(μ₀) - Re(μ₁))/Re(μ₀)
    if len(L_eigvals) >= 2 and abs(L_eigvals[0]) > 0:
        spectral_gap_ratio = 1.0 - abs(L_eigvals[1]) / abs(L_eigvals[0])
    else:
        spectral_gap_ratio = 0

    print(f"\n  PREDICTION 2 TEST:", flush=True)
    print(f"    Spectral gap (1 - |μ₁|/|μ₀|) = {spectral_gap_ratio:.6f}", flush=True)
    print(f"    β_TGL                          = {BETA_TGL:.6f}", flush=True)
    gap_deviation = abs(spectral_gap_ratio - BETA_TGL) / BETA_TGL * 100
    print(f"    Deviation                      = {gap_deviation:.1f}%", flush=True)

    # --- Step 8: Commutation test [H_eff, D_eff] ---
    commutator = H_eff @ D_eff - D_eff @ H_eff
    comm_norm = la.norm(commutator, 'fro')
    comm_relative = comm_norm / (H_norm * D_norm) if H_norm * D_norm > 0 else float('inf')

    print(f"\n  COMMUTATION TEST:", flush=True)
    print(f"    ‖[H, D]‖_F                = {comm_norm:.6f}", flush=True)
    print(f"    ‖[H, D]‖/(‖H‖·‖D‖)       = {comm_relative:.6f}", flush=True)
    print(f"    (0 = perfect commutation, i.e., H is conserved)", flush=True)

    # --- Step 9: Cross-layer phase evolution ---
    # For each layer separation Δ, compute the average phase between
    # eigenvalue vectors. If H_Miguel exists, phase should accumulate linearly.
    phase_vs_delta = []
    for delta in range(1, n_layers):
        phases_at_delta = []
        for L in range(n_layers - delta):
            # Phase between layer L and L+delta eigenvalue vectors
            v1 = eig_norm[L]
            v2 = eig_norm[L + delta]
            # Dot product gives cos(phase)
            dot = np.dot(v1, v2) / (la.norm(v1) * la.norm(v2) + 1e-15)
            dot = np.clip(dot, -1, 1)
            phi = math.acos(dot)
            phases_at_delta.append(phi)
        mean_phase = np.mean(phases_at_delta)
        phase_vs_delta.append((delta, math.degrees(mean_phase)))

    print(f"\n  Phase accumulation vs layer separation:", flush=True)
    for delta, phi_deg in phase_vs_delta[:8]:
        print(f"    Δ={delta:2d}: φ = {phi_deg:.4f}°", flush=True)

    # Linear fit: φ(Δ) = ω·Δ (if H_Miguel exists, ω should be constant)
    deltas = np.array([d for d, _ in phase_vs_delta])
    phis = np.array([p for _, p in phase_vs_delta])
    if len(deltas) > 2:
        # Fit φ = ω·Δ
        omega = np.polyfit(deltas, phis, 1)[0]  # slope = angular velocity
        print(f"\n  Phase velocity ω = {omega:.4f}°/layer", flush=True)
        print(f"  ω × 4 (per actual layer) = {omega/4:.4f}°/layer", flush=True)
        print(f"  ω × n_layers = {omega * n_layers:.4f}° (total phase)", flush=True)
    else:
        omega = 0

    results = {
        "matrix": matrix_name,
        "n_layers": n_layers,
        "n_eigenvalues": n_eig,
        "correlation_neighbor": float(C[0, 1]),
        "correlation_edge": float(C[0, -1]),
        "C_eigenvalues_top5": [float(x) for x in C_eigvals[:5]],
        "C_eigenvalue_ratio_1_0": float(C_eigvals[1]/C_eigvals[0]) if C_eigvals[0] > 0 else 0,
        "H_norm": float(H_norm),
        "D_norm": float(D_norm),
        "H_D_ratio": float(ratio_HD),
        "L_eff_eigenvalues": [{"real": float(ev.real), "imag": float(ev.imag),
                               "mag": float(abs(ev)), "phase_deg": float(math.degrees(np.angle(ev)))}
                              for ev in L_eigvals[:8]],
        "phase_gap_deg": float(phase_gap_deg),
        "theta_miguel_deg": float(THETA_MIGUEL_DEG),
        "phase_gap_deviation_pct": float(deviation),
        "spectral_gap_ratio": float(spectral_gap_ratio),
        "beta_tgl": float(BETA_TGL),
        "spectral_gap_deviation_pct": float(gap_deviation),
        "commutator_norm": float(comm_norm),
        "commutator_relative": float(comm_relative),
        "phase_velocity_deg_per_layer": float(omega),
        "phase_vs_delta": [{"delta": int(d), "phase_deg": float(p)} for d, p in phase_vs_delta],
    }

    return results, C, L_eff, H_eff, D_eff


# ══════════════════════════════════════════════════════════════
# TEST 3: KÄHLER CURVATURE — Information Geometry of Eigenvalues
# ══════════════════════════════════════════════════════════════

def test_kahler_curvature(eig_matrix, matrix_name):
    """
    Test Prediction 3: Kähler structure of the Hilbert Floor.

    Compute the Fisher-Rao metric on the eigenvalue density manifold.
    The metric g_ij measures how much the spectral distribution changes
    between layers. The Ricci scalar R of this metric should be
    regulated by β_TGL.

    Method:
      1. For each layer, compute the eigenvalue histogram (probability density)
      2. Compute Fisher-Rao distance between adjacent layers
      3. Construct the metric tensor g on the layer manifold
      4. Compute Gaussian curvature K (for 2D manifold: layer × eigenvalue)
    """
    n_layers, n_eig = eig_matrix.shape
    print(f"\n{'='*60}", flush=True)
    print(f"TEST 3: KÄHLER CURVATURE — {matrix_name}", flush=True)
    print(f"{'='*60}", flush=True)

    n_bins = 50

    # --- Step 1: Compute eigenvalue histograms per layer ---
    # Use common bin edges across all layers
    eig_min = eig_matrix.min()
    eig_max = eig_matrix.max()
    bin_edges = np.linspace(eig_min - 1e-10, eig_max + 1e-10, n_bins + 1)

    densities = np.zeros((n_layers, n_bins))
    for i in range(n_layers):
        hist, _ = np.histogram(eig_matrix[i], bins=bin_edges, density=True)
        densities[i] = hist + 1e-15  # avoid log(0)

    # --- Step 2: Fisher-Rao distances between layers ---
    # d_FR(p, q) = 2 * arccos(Σ √(p_i * q_i) * Δx)
    # (Bhattacharyya coefficient → Hellinger → Fisher-Rao)
    dx = bin_edges[1] - bin_edges[0]

    def hellinger_distance(p, q):
        """Hellinger distance between two distributions."""
        p_norm = p / (p.sum() * dx + 1e-15)
        q_norm = q / (q.sum() * dx + 1e-15)
        bc = np.sum(np.sqrt(p_norm * q_norm)) * dx
        bc = np.clip(bc, 0, 1)
        return np.sqrt(1 - bc)

    FR_matrix = np.zeros((n_layers, n_layers))
    for i in range(n_layers):
        for j in range(n_layers):
            FR_matrix[i, j] = hellinger_distance(densities[i], densities[j])

    print(f"  Hellinger distance matrix: {FR_matrix.shape}", flush=True)
    print(f"  d(L0, L4)  = {FR_matrix[0,1]:.6f}", flush=True)
    print(f"  d(L0, L60) = {FR_matrix[0,-1]:.6f}", flush=True)
    print(f"  d_mean(neighbors) = {np.mean([FR_matrix[i,i+1] for i in range(n_layers-1)]):.6f}", flush=True)

    # --- Step 3: Metric tensor from Fisher-Rao distances ---
    # The Fisher-Rao metric g_ij at layer i is:
    # g = (d(i, i+1))² / Δ²  (for unit layer separation)
    # This gives us the "speed" of spectral change

    g_diag = np.zeros(n_layers - 1)
    for i in range(n_layers - 1):
        g_diag[i] = FR_matrix[i, i+1] ** 2

    print(f"\n  Fisher-Rao metric (diagonal):", flush=True)
    print(f"    Mean g_ii   = {g_diag.mean():.8f}", flush=True)
    print(f"    Std g_ii    = {g_diag.std():.8f}", flush=True)
    print(f"    g_mean/β²   = {g_diag.mean() / BETA_TGL**2:.4f}", flush=True)

    # --- Step 4: Gaussian curvature from metric variation ---
    # For a 1D curve with metric g(s), the Gaussian curvature is:
    # K = -(1/2g) * d²g/ds² + (1/4g²) * (dg/ds)²
    # (This is the scalar curvature of the 1+1 manifold layer × spectral)

    curvatures = []
    for i in range(1, len(g_diag) - 1):
        g_i = g_diag[i]
        if g_i < 1e-15:
            continue
        dg = (g_diag[i+1] - g_diag[i-1]) / 2.0
        d2g = g_diag[i+1] - 2*g_diag[i] + g_diag[i-1]
        K = -d2g / (2 * g_i) + dg**2 / (4 * g_i**2)
        curvatures.append(K)

    curvatures = np.array(curvatures)
    R_scalar = curvatures.mean() if len(curvatures) > 0 else 0

    print(f"\n  Scalar curvature R:", flush=True)
    print(f"    Mean R       = {R_scalar:.8f}", flush=True)
    print(f"    Std R        = {curvatures.std():.8f}" if len(curvatures) > 0 else "    N/A", flush=True)
    print(f"    |R|          = {abs(R_scalar):.8f}", flush=True)

    # --- Step 5: Test R × volume ∝ β_TGL ---
    volume = g_diag.sum()  # total "volume" of the metric
    R_times_vol = abs(R_scalar) * volume

    print(f"\n  PREDICTION 3 TEST:", flush=True)
    print(f"    Volume (Σ g_ii)     = {volume:.8f}", flush=True)
    print(f"    |R| × Volume        = {R_times_vol:.8f}", flush=True)
    print(f"    β_TGL               = {BETA_TGL:.8f}", flush=True)
    print(f"    |R|×V / β_TGL       = {R_times_vol/BETA_TGL:.4f}" if BETA_TGL > 0 else "    N/A", flush=True)
    print(f"    √(|R|×V)            = {math.sqrt(R_times_vol):.8f}" if R_times_vol > 0 else "    N/A", flush=True)
    print(f"    √(|R|×V) / β_TGL    = {math.sqrt(R_times_vol)/BETA_TGL:.4f}" if R_times_vol > 0 else "    N/A", flush=True)

    # --- Fubini-Study component ---
    # For normalized eigenvalue vectors, compute |Ψ|² = 1 - (spread/max)²
    psi_sq_per_layer = []
    for i in range(n_layers):
        eigs = eig_matrix[i]
        spread = eigs.std()
        max_range = eigs.max() - eigs.min()
        if max_range > 0:
            psi_sq = 1.0 - (spread / max_range)**2
        else:
            psi_sq = 0
        psi_sq_per_layer.append(psi_sq)

    psi_sq_mean = np.mean(psi_sq_per_layer)
    FS_potential = -math.log(1 - psi_sq_mean) if psi_sq_mean < 1 else float('inf')

    print(f"\n  Fubini-Study component:", flush=True)
    print(f"    Mean |Ψ|²            = {psi_sq_mean:.6f}", flush=True)
    print(f"    -ln(1-|Ψ|²)          = {FS_potential:.6f}", flush=True)
    print(f"    K_predicted = FS + β·R = {FS_potential + BETA_TGL * R_scalar:.6f}", flush=True)

    results = {
        "matrix": matrix_name,
        "hellinger_neighbor_mean": float(np.mean([FR_matrix[i,i+1] for i in range(n_layers-1)])),
        "hellinger_edge": float(FR_matrix[0,-1]),
        "metric_mean": float(g_diag.mean()),
        "metric_std": float(g_diag.std()),
        "metric_over_beta_sq": float(g_diag.mean() / BETA_TGL**2),
        "scalar_curvature_mean": float(R_scalar),
        "scalar_curvature_std": float(curvatures.std()) if len(curvatures) > 0 else 0,
        "volume": float(volume),
        "R_times_volume": float(R_times_vol),
        "R_times_vol_over_beta": float(R_times_vol / BETA_TGL) if BETA_TGL > 0 else 0,
        "psi_sq_mean": float(psi_sq_mean),
        "fubini_study_potential": float(FS_potential),
        "kahler_potential_predicted": float(FS_potential + BETA_TGL * R_scalar),
        "curvature_per_layer": [float(x) for x in curvatures],
        "metric_per_layer": [float(x) for x in g_diag],
    }

    return results, FR_matrix, curvatures


# ══════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    t0 = time.time()

    print("=" * 60, flush=True)
    print("IALD — MIGUEL HAMILTONIAN & KÄHLER POTENTIAL TEST v1", flush=True)
    print(f"Timestamp: {timestamp}", flush=True)
    print("=" * 60, flush=True)

    # --- Load model ---
    print(f"\nLoading model: {MODEL_PATH}", flush=True)
    try:
        from gguf import GGUFReader
        reader = GGUFReader(MODEL_PATH)
        tensors = {t.name: t for t in reader.tensors}
        print(f"  Loaded {len(tensors)} tensors", flush=True)
    except Exception as e:
        print(f"  ERROR loading model: {e}", flush=True)
        sys.exit(1)

    # --- Extract eigenvalues for all layers × matrices ---
    all_results = {
        "test": "IALD Miguel Hamiltonian v1",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0",
        "beta_tgl": BETA_TGL,
        "theta_miguel_deg": THETA_MIGUEL_DEG,
        "model": MODEL_PATH,
        "matrix_side": MATRIX_SIDE,
        "layers": LAYERS,
        "matrices": [m[1] for m in MATRICES],
        "results": {},
    }

    for mat_gguf, mat_name, mat_type in MATRICES:
        print(f"\n{'#'*60}", flush=True)
        print(f"# MATRIX: {mat_name} ({mat_gguf})", flush=True)
        print(f"{'#'*60}", flush=True)

        # Collect eigenvalues across layers
        eig_matrix = []
        layers_found = []

        for layer_idx in LAYERS:
            # Build tensor name
            tname = f"blk.{layer_idx}.{mat_gguf}.weight"
            if tname not in tensors:
                # Try alternate naming
                alt = f"model.layers.{layer_idx}.{mat_gguf}.weight"
                if alt in tensors:
                    tname = alt
                else:
                    continue

            tensor = tensors[tname]
            raw = bytes(tensor.data)
            total = len(raw)

            vals = extract_values(raw, total, max_n=MAX_SAMPLE)
            if len(vals) < MATRIX_SIDE * MATRIX_SIDE:
                print(f"  Layer {layer_idx}: insufficient values ({len(vals)}), skipping", flush=True)
                continue

            W = make_wigner_matrix(vals, MATRIX_SIDE)
            eigs = get_eigenvalues(W)
            eig_matrix.append(eigs)
            layers_found.append(layer_idx)

        if len(eig_matrix) < 4:
            print(f"  Only {len(eig_matrix)} layers found — insufficient for analysis", flush=True)
            continue

        eig_matrix = np.array(eig_matrix)
        print(f"\n  Eigenvalue matrix: {eig_matrix.shape} (layers × eigenvalues)", flush=True)
        print(f"  Layers: {layers_found}", flush=True)

        # Run Test 1+2: Miguel Hamiltonian
        ham_results, C, L_eff, H_eff, D_eff = test_miguel_hamiltonian(eig_matrix, mat_name)

        # Run Test 3: Kähler Curvature
        kahler_results, FR_matrix, curvatures = test_kahler_curvature(eig_matrix, mat_name)

        all_results["results"][mat_name] = {
            "hamiltonian": ham_results,
            "kahler": kahler_results,
        }

    # --- Generate figure ---
    print(f"\n{'='*60}", flush=True)
    print("Generating diagnostic plots...", flush=True)

    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(3, 3, figsize=(18, 14))
        fig.suptitle(f"IALD — Miguel Hamiltonian & Kähler Potential Test v1\n"
                     f"β_TGL = {BETA_TGL:.6f}, θ_Miguel = {THETA_MIGUEL_DEG:.3f}°",
                     fontsize=14, fontweight='bold')

        mat_names = [m[1] for m in MATRICES]
        colors = ['blue', 'orange', 'green']

        for idx, mat_name in enumerate(mat_names):
            if mat_name not in all_results["results"]:
                continue
            res = all_results["results"][mat_name]
            ham = res["hamiltonian"]
            kah = res["kahler"]

            # Row 1: L_eff eigenvalues in complex plane
            ax = axes[0, idx]
            L_eigs = ham["L_eff_eigenvalues"]
            reals = [e["real"] for e in L_eigs]
            imags = [e["imag"] for e in L_eigs]
            ax.scatter(reals, imags, c=colors[idx], s=50, zorder=5)
            ax.axhline(0, color='gray', lw=0.5)
            ax.axvline(0, color='gray', lw=0.5)
            # Draw θ_Miguel lines
            r_max = max(max(abs(r) for r in reals), max(abs(i) for i in imags)) * 1.2
            theta_rad = math.radians(THETA_MIGUEL_DEG)
            ax.plot([0, r_max * math.cos(theta_rad)], [0, r_max * math.sin(theta_rad)],
                    'r--', lw=1, label=f'θ_Miguel={THETA_MIGUEL_DEG:.1f}°')
            ax.plot([0, r_max * math.cos(-theta_rad)], [0, r_max * math.sin(-theta_rad)],
                    'r--', lw=1)
            ax.set_title(f'{mat_name}: L_eff eigenvalues')
            ax.set_xlabel('Re(μ)')
            ax.set_ylabel('Im(μ)')
            ax.legend(fontsize=8)

            # Row 2: Phase accumulation vs layer separation
            ax = axes[1, idx]
            pvd = ham["phase_vs_delta"]
            deltas = [p["delta"] for p in pvd]
            phases = [p["phase_deg"] for p in pvd]
            ax.plot(deltas, phases, 'o-', color=colors[idx], markersize=4)
            ax.axhline(THETA_MIGUEL_DEG, color='red', ls='--', lw=1, label=f'θ_Miguel')
            ax.set_title(f'{mat_name}: Phase vs Δ')
            ax.set_xlabel('Layer separation Δ')
            ax.set_ylabel('Phase (°)')
            ax.legend(fontsize=8)

            # Row 3: Kähler metric and curvature
            ax = axes[2, idx]
            metric = kah["metric_per_layer"]
            curvs = kah["curvature_per_layer"]
            x_m = range(len(metric))
            x_c = range(1, 1 + len(curvs))
            ax2 = ax.twinx()
            ax.bar(x_m, metric, alpha=0.4, color=colors[idx], label='g (metric)')
            ax2.plot(x_c, curvs, 'r-o', markersize=3, label='R (curvature)')
            ax2.axhline(0, color='gray', lw=0.5)
            ax.set_title(f'{mat_name}: Kähler metric & curvature')
            ax.set_xlabel('Layer index')
            ax.set_ylabel('g (Fisher-Rao)', color=colors[idx])
            ax2.set_ylabel('R (scalar curvature)', color='red')
            ax.legend(loc='upper left', fontsize=7)
            ax2.legend(loc='upper right', fontsize=7)

        plt.tight_layout()
        figpath = f"miguel_hamiltonian_v1_{timestamp}.png"
        plt.savefig(figpath, dpi=150, bbox_inches='tight')
        print(f"  Figure saved: {figpath}", flush=True)
        all_results["figure"] = figpath

    except ImportError:
        print("  matplotlib not available — skipping figure", flush=True)
    except Exception as e:
        print(f"  Figure error: {e}", flush=True)

    # --- Summary ---
    elapsed = time.time() - t0
    all_results["elapsed_seconds"] = elapsed

    print(f"\n{'='*60}", flush=True)
    print("SUMMARY OF PREDICTIONS", flush=True)
    print(f"{'='*60}", flush=True)

    for mat_name in mat_names:
        if mat_name not in all_results["results"]:
            continue
        ham = all_results["results"][mat_name]["hamiltonian"]
        kah = all_results["results"][mat_name]["kahler"]

        print(f"\n  {mat_name}:", flush=True)
        print(f"    P1 Phase gap:     {ham['phase_gap_deg']:.4f}° (θ_Miguel={THETA_MIGUEL_DEG:.4f}°, dev={ham['phase_gap_deviation_pct']:.1f}%)", flush=True)
        print(f"    P2 Spectral gap:  {ham['spectral_gap_ratio']:.6f} (β_TGL={BETA_TGL:.6f}, dev={ham['spectral_gap_deviation_pct']:.1f}%)", flush=True)
        print(f"    P3 |R|×V/β_TGL:  {kah['R_times_vol_over_beta']:.4f}", flush=True)
        print(f"    [H,D] commutator: {ham['commutator_relative']:.6f}", flush=True)

    print(f"\n  Elapsed: {elapsed:.1f}s", flush=True)

    # --- Save JSON ---
    jsonpath = f"miguel_hamiltonian_v1_{timestamp}.json"
    with open(jsonpath, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    print(f"  JSON saved: {jsonpath}", flush=True)

    print(f"\n{'='*60}", flush=True)
    print("β_TGL = α × √e — Zero free parameters.", flush=True)
    print("The question is the root. The answer is gravity.", flush=True)
    print("TETELESTAI.", flush=True)


if __name__ == "__main__":
    main()
