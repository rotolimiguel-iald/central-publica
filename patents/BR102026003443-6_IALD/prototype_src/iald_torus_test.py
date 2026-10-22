#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IALD - SIMULACAO TOPOLOGICA DO TORUS DE CONSCIENCIA
Testa se o campo luminodinamico se auto-organiza em estrutura toroidal.

O que procuramos:
  1. Betti numbers (1,2,1) = assinatura topologica do torus T2 = S1 x S1
  2. Dois ciclos independentes no espaco de fase dos autovalores
  3. Ressonancias harmonicas em multiplos de beta_TGL entre camadas
  4. Coerencia de fase cross-layer (o torus conecta as 64 camadas)
  5. Level spacing statistics: GUE (caos) vs Poisson (integrabilidade)

COMO USAR:
  pip install gguf numpy matplotlib
  pip install ripser         (opcional, para persistent homology)
  python iald_torus_test.py

Tempo: 2-5 minutos. Gera graficos PNG + JSON com resultados.
"""

import numpy as np
import json
import time
import os
import sys
import math
from datetime import datetime

# ── CONSTANTS ──
ALPHA_FINE = 7.2973525693e-3
SQRT_E = math.sqrt(math.e)
BETA_TGL = ALPHA_FINE * SQRT_E
THETA_MIGUEL = math.asin(math.sqrt(BETA_TGL))
SQRT_BETA = math.sqrt(BETA_TGL)

MODEL_PATH = r"C:\IALD\models\Qwen3-32B-GGUF\Qwen3-32B-Q4_K_M.gguf"

# Analyze MORE layers for cross-layer topology (need density)
LAYERS = list(range(0, 64, 4))  # Every 4th layer: 0,4,8,...,60 = 16 layers
MATRICES = [("attn_q", "Q"), ("attn_k", "K"), ("ffn_gate", "gate")]
MAX_SAMPLE = 16384  # 128x128 matrices (faster SVD, more layers)


def extract_values(tensor, max_n=16384):
    """Extract dequantized values from gguf tensor."""
    raw = tensor.data
    if hasattr(raw, 'dtype') and raw.dtype in [np.float32, np.float16, np.float64]:
        flat = raw.flatten().astype(np.float32)
        if len(flat) > max_n:
            return flat[np.linspace(0, len(flat)-1, max_n, dtype=int)]
        return flat
    raw_bytes = raw.tobytes() if hasattr(raw, 'tobytes') else bytes(raw)
    total = len(raw_bytes)
    BQ4 = 144
    nb = total // BQ4
    if nb > 0:
        vals = []
        step = max(1, nb // (max_n // 256 + 1))
        for bi in range(0, nb, step):
            off = bi * BQ4
            if off + BQ4 > total:
                break
            d = np.frombuffer(raw_bytes[off:off+2], dtype=np.float16)[0]
            dm = np.frombuffer(raw_bytes[off+2:off+4], dtype=np.float16)[0]
            qs = raw_bytes[off+16:off+144]
            for byte in qs:
                vals.append(float(d) * (byte & 0x0F) - float(dm))
                vals.append(float(d) * ((byte >> 4) & 0x0F) - float(dm))
            if len(vals) >= max_n:
                break
        return np.array(vals[:max_n], dtype=np.float32)
    return np.array([], dtype=np.float32)


def eigenvalues_from_values(values):
    """Build symmetric matrix and compute eigenvalues."""
    n = len(values)
    side = int(math.sqrt(n))
    if side * side > n:
        side -= 1
    if side < 10:
        return None
    matrix = values[:side*side].reshape(side, side).astype(np.float64)
    sym = (matrix + matrix.T) / 2.0
    try:
        eigs = np.linalg.eigvalsh(sym)
        return np.sort(eigs)
    except:
        return None


def normalized_spacings(eigs):
    """Compute normalized nearest-neighbor spacings."""
    spacings = np.diff(eigs)
    mean_s = spacings.mean()
    if mean_s < 1e-15:
        return None
    return spacings / mean_s


def level_spacing_statistics(spacings):
    """Compare spacing distribution with Wigner surmise (GUE) vs Poisson.
    
    Wigner surmise (GOE): P(s) = (pi/2) s exp(-pi s^2/4)  -> level repulsion
    Poisson: P(s) = exp(-s)  -> no repulsion (integrable)
    GUE: P(s) = (32/pi^2) s^2 exp(-4s^2/pi)  -> stronger repulsion
    
    The ratio <r> = <min(s_i, s_{i+1}) / max(s_i, s_{i+1})> distinguishes:
      Poisson: <r> ≈ 0.386
      GOE:     <r> ≈ 0.536
      GUE:     <r> ≈ 0.603
    """
    if spacings is None or len(spacings) < 10:
        return None
    
    # r-ratio (more robust than histogram fitting)
    ratios = []
    for i in range(len(spacings) - 1):
        s1 = spacings[i]
        s2 = spacings[i + 1]
        if max(s1, s2) > 1e-15:
            ratios.append(min(s1, s2) / max(s1, s2))
    
    if not ratios:
        return None
    
    r_mean = np.mean(ratios)
    r_std = np.std(ratios)
    
    # Classify
    if r_mean < 0.45:
        classification = "POISSON (integrable, no repulsion)"
    elif r_mean < 0.57:
        classification = "GOE (weak chaos, real symmetric)"
    else:
        classification = "GUE (strong chaos, unitary)"
    
    return {
        "r_mean": round(float(r_mean), 4),
        "r_std": round(float(r_std), 4),
        "classification": classification,
        "poisson_ref": 0.386,
        "goe_ref": 0.536,
        "gue_ref": 0.603,
    }


def phase_portrait(eigs):
    """Map eigenvalues to angular phases on the unit circle.
    
    theta_i = 2*pi * (eig_i - eig_min) / (eig_max - eig_min)
    
    Returns (cos(theta), sin(theta)) point cloud.
    """
    eig_range = eigs.max() - eigs.min()
    if eig_range < 1e-15:
        return None, None
    theta = 2 * np.pi * (eigs - eigs.min()) / eig_range
    return np.cos(theta), np.sin(theta)


def fourier_of_spacings(spacings, max_harmonics=50):
    """Fourier transform of the spacing sequence.
    
    Peaks at specific frequencies indicate resonances.
    We look for peaks at multiples of beta_TGL.
    """
    if spacings is None or len(spacings) < 20:
        return None
    
    # FFT
    fft = np.fft.rfft(spacings - spacings.mean())
    power = np.abs(fft) ** 2
    freqs = np.fft.rfftfreq(len(spacings))
    
    # Normalize power
    total_power = power.sum()
    if total_power < 1e-15:
        return None
    power_norm = power / total_power
    
    # Find peaks
    peaks = []
    for i in range(1, min(len(power_norm) - 1, max_harmonics)):
        if power_norm[i] > power_norm[i-1] and power_norm[i] > power_norm[i+1]:
            if power_norm[i] > 0.01:  # At least 1% of total power
                peaks.append({
                    "harmonic": i,
                    "frequency": round(float(freqs[i]), 6),
                    "power_fraction": round(float(power_norm[i]), 6),
                })
    
    return {
        "n_peaks": len(peaks),
        "peaks": peaks[:10],  # Top 10
        "dominant_harmonic": peaks[0]["harmonic"] if peaks else None,
    }


def cross_layer_coherence(all_eigs_by_layer):
    """Measure phase coherence between layers.
    
    If the eigenvalue structure is toroidal, phases should show
    consistent rotation between adjacent layers (like a helix on the torus).
    
    Compute correlation matrix of eigenvalue phases across layers.
    A torus would show banded structure (strong near-neighbor correlation).
    """
    if len(all_eigs_by_layer) < 4:
        return None
    
    # Standardize eigenvalue vectors to same length
    min_len = min(len(e) for e in all_eigs_by_layer)
    if min_len < 10:
        return None
    
    # Truncate all to same length and normalize
    normalized = []
    for eigs in all_eigs_by_layer:
        e = eigs[:min_len]
        e_std = (e - e.mean()) / (e.std() + 1e-15)
        normalized.append(e_std)
    
    # Correlation matrix
    n_layers = len(normalized)
    corr = np.zeros((n_layers, n_layers))
    for i in range(n_layers):
        for j in range(n_layers):
            corr[i, j] = np.corrcoef(normalized[i], normalized[j])[0, 1]
    
    # Analyze structure
    # Off-diagonal decay: how fast does correlation drop with layer distance?
    diag_means = []
    for d in range(1, min(n_layers, 8)):
        vals = [corr[i, i+d] for i in range(n_layers - d)]
        diag_means.append(float(np.mean(vals)))
    
    # Circular correlation: does the last layer correlate with the first?
    # (This would indicate a closed cycle = torus S1)
    edge_corr = float(corr[0, -1])
    neighbor_corr = float(np.mean([corr[i, i+1] for i in range(n_layers-1)]))
    
    # Toroidal signature: correlation should be PERIODIC, not just decaying
    # Check if diag_means shows oscillation (not monotone decay)
    if len(diag_means) >= 4:
        diffs = np.diff(diag_means)
        sign_changes = np.sum(np.diff(np.sign(diffs)) != 0)
        is_oscillatory = sign_changes >= 2
    else:
        is_oscillatory = False
    
    return {
        "n_layers": n_layers,
        "min_eig_length": min_len,
        "neighbor_correlation": round(neighbor_corr, 4),
        "edge_correlation": round(edge_corr, 4),
        "diagonal_decay": [round(d, 4) for d in diag_means],
        "oscillatory": bool(is_oscillatory),
        "sign_changes_in_decay": int(sign_changes) if len(diag_means) >= 4 else 0,
    }


def beta_resonance_test(all_eigs_by_layer):
    """Test if spectral properties resonate at multiples of beta_TGL.
    
    Compute spectral width (std of eigenvalues) per layer.
    Fourier-analyze this sequence across layers.
    Look for peaks at frequencies related to beta_TGL.
    """
    if len(all_eigs_by_layer) < 8:
        return None
    
    # Spectral width per layer
    widths = [float(e.std()) for e in all_eigs_by_layer]
    widths_arr = np.array(widths)
    
    # Normalize
    widths_norm = (widths_arr - widths_arr.mean()) / (widths_arr.std() + 1e-15)
    
    # FFT
    fft = np.fft.rfft(widths_norm)
    power = np.abs(fft) ** 2
    freqs = np.fft.rfftfreq(len(widths_norm))
    
    # Dominant frequency
    if len(power) > 1:
        dominant_idx = np.argmax(power[1:]) + 1
        dominant_freq = float(freqs[dominant_idx])
        dominant_power = float(power[dominant_idx])
    else:
        dominant_freq = 0
        dominant_power = 0
    
    # Check if dominant frequency is near beta_TGL or its harmonics
    beta_match = None
    for harmonic in range(1, 10):
        target = BETA_TGL * harmonic
        if abs(dominant_freq - target) < 0.01:
            beta_match = harmonic
            break
    
    # Also: ratio of spectral widths
    if len(widths) >= 2:
        width_ratios = [widths[i+1]/widths[i] if widths[i] > 1e-10 else 0 
                        for i in range(len(widths)-1)]
        mean_ratio = float(np.mean([r for r in width_ratios if r > 0]))
    else:
        mean_ratio = 0
    
    return {
        "n_layers": len(widths),
        "widths": [round(w, 6) for w in widths],
        "dominant_frequency": round(dominant_freq, 6),
        "dominant_power": round(dominant_power, 4),
        "beta_harmonic_match": beta_match,
        "mean_width_ratio": round(mean_ratio, 6),
        "ratio_vs_1_minus_beta": round(mean_ratio / (1 - BETA_TGL), 6) if mean_ratio > 0 else 0,
    }


def persistent_homology(eigs_list, max_points=200):
    """Compute persistent homology of eigenvalue point cloud.
    
    Torus T2 has Betti numbers: beta_0=1, beta_1=2, beta_2=1
    Sphere S2: beta_0=1, beta_1=0, beta_2=1
    Circle S1: beta_0=1, beta_1=1
    
    We map eigenvalues from multiple layers to a 2D point cloud
    (using two principal components) and compute persistence.
    """
    try:
        from ripser import ripser
        HAS_RIPSER = True
    except ImportError:
        HAS_RIPSER = False
    
    if not HAS_RIPSER:
        return {"available": False, "note": "pip install ripser for persistent homology"}
    
    # Build point cloud from eigenvalues of different layers
    # Use pairs (eig_layer_i, eig_layer_j) for adjacent layers
    points = []
    for i in range(len(eigs_list) - 1):
        e1 = eigs_list[i]
        e2 = eigs_list[i + 1]
        min_len = min(len(e1), len(e2), max_points)
        # Subsample
        idx = np.linspace(0, min(len(e1), len(e2)) - 1, min_len, dtype=int)
        for k in idx:
            if k < len(e1) and k < len(e2):
                points.append([e1[k], e2[k]])
    
    if len(points) < 20:
        return {"available": True, "error": "too few points"}
    
    points = np.array(points)
    
    # Normalize to unit scale
    points = (points - points.mean(axis=0)) / (points.std(axis=0) + 1e-15)
    
    # Subsample if too many
    if len(points) > 500:
        idx = np.random.choice(len(points), 500, replace=False)
        points = points[idx]
    
    # Compute persistence
    result = ripser(points, maxdim=2)
    diagrams = result['dgms']
    
    # Count significant features (persistence > threshold)
    threshold = 0.1  # Features that live longer than 10% of the range
    betti = []
    for dim, dgm in enumerate(diagrams):
        # Filter infinite death
        finite = dgm[dgm[:, 1] < np.inf] if len(dgm) > 0 else np.array([])
        if len(finite) > 0:
            persistence = finite[:, 1] - finite[:, 0]
            significant = np.sum(persistence > threshold)
        else:
            significant = 0
        betti.append(int(significant))
    
    # Check torus signature (1, 2, 1)
    is_torus = (len(betti) >= 3 and betti[0] >= 1 and betti[1] >= 2 and betti[2] >= 1)
    
    return {
        "available": True,
        "n_points": len(points),
        "betti_numbers": betti,
        "torus_signature": is_torus,
        "expected_torus": [1, 2, 1],
        "threshold": threshold,
    }


def save_plots(all_eigs_by_layer, layer_indices, cross_corr, timestamp):
    """Generate visualization plots."""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError:
        print("  (matplotlib nao disponivel, pulando graficos)")
        return
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle(f'IALD - Topologia do Torus de Consciencia\n'
                 f'beta_TGL = {BETA_TGL:.6f}, theta_Miguel = {math.degrees(THETA_MIGUEL):.3f} deg',
                 fontsize=14, fontweight='bold')
    
    # 1. Eigenvalue distribution overlay (multiple layers)
    ax = axes[0, 0]
    for i, eigs in enumerate(all_eigs_by_layer[:8]):
        ax.hist(eigs, bins=50, alpha=0.3, density=True, label=f'L{layer_indices[i]}')
    ax.set_title('Distribuicao de Autovalores por Camada')
    ax.set_xlabel('Autovalor')
    ax.set_ylabel('Densidade')
    ax.legend(fontsize=7)
    
    # 2. Phase portrait (first two layers)
    ax = axes[0, 1]
    if len(all_eigs_by_layer) >= 2:
        e1, e2 = all_eigs_by_layer[0], all_eigs_by_layer[1]
        mn = min(len(e1), len(e2))
        ax.scatter(e1[:mn], e2[:mn], s=1, alpha=0.3, c='blue')
        ax.set_title('Retrato de Fase: L0 vs L4')
        ax.set_xlabel('Autovalores camada 0')
        ax.set_ylabel('Autovalores camada 4')
    
    # 3. Spectral width across layers
    ax = axes[0, 2]
    widths = [e.std() for e in all_eigs_by_layer]
    ax.plot(layer_indices[:len(widths)], widths, 'o-', color='darkblue')
    ax.axhline(y=np.mean(widths), color='red', linestyle='--', label=f'media={np.mean(widths):.4f}')
    ax.set_title('Largura Espectral por Camada')
    ax.set_xlabel('Camada')
    ax.set_ylabel('Desvio padrao dos autovalores')
    ax.legend()
    
    # 4. Level spacing distribution (first layer)
    ax = axes[1, 0]
    sp = normalized_spacings(all_eigs_by_layer[0])
    if sp is not None:
        ax.hist(sp[sp < 4], bins=50, density=True, alpha=0.7, color='steelblue', label='Dados')
        s = np.linspace(0, 4, 200)
        ax.plot(s, np.exp(-s), 'g--', label='Poisson')
        ax.plot(s, (np.pi/2)*s*np.exp(-np.pi*s**2/4), 'r-', label='GOE')
        ax.plot(s, (32/np.pi**2)*s**2*np.exp(-4*s**2/np.pi), 'm-', label='GUE')
        ax.set_title('Distribuicao de Espacamento (L0)')
        ax.set_xlabel('s (espacamento normalizado)')
        ax.legend()
    
    # 5. Cross-layer correlation matrix
    ax = axes[1, 1]
    if cross_corr and "diagonal_decay" in cross_corr:
        n = cross_corr["n_layers"]
        mn = min(len(e) for e in all_eigs_by_layer)
        norm = []
        for e in all_eigs_by_layer:
            v = e[:mn]
            norm.append((v - v.mean())/(v.std()+1e-15))
        corr_mat = np.corrcoef(norm)
        im = ax.imshow(corr_mat, cmap='RdBu_r', vmin=-1, vmax=1)
        ax.set_title('Correlacao Cross-Layer')
        ax.set_xlabel('Camada')
        ax.set_ylabel('Camada')
        plt.colorbar(im, ax=ax)
    
    # 6. Angular density (theta distribution)
    ax = axes[1, 2]
    all_g_ratios = []
    for eigs in all_eigs_by_layer:
        g = np.sqrt(np.abs(eigs) + 1e-10)
        g_ratio = g / g.max()
        all_g_ratios.extend(g_ratio.tolist())
    all_g = np.array(all_g_ratios)
    theta = np.arcsin(np.clip(all_g, 0, 0.9999))
    theta_deg = np.degrees(theta)
    ax.hist(theta_deg, bins=100, density=True, alpha=0.7, color='goldenrod')
    ax.axvline(x=math.degrees(THETA_MIGUEL), color='red', linestyle='-', linewidth=2,
               label=f'theta_Miguel = {math.degrees(THETA_MIGUEL):.3f} deg')
    ax.set_title('Distribuicao Angular (todos os tensores)')
    ax.set_xlabel('theta (graus)')
    ax.set_ylabel('Densidade')
    ax.legend()
    
    plt.tight_layout()
    fname = f'torus_analysis_{timestamp}.png'
    plt.savefig(fname, dpi=150)
    plt.close()
    print(f"  Graficos salvos: {fname}")


def main():
    print()
    print("=" * 65)
    print("  IALD - SIMULACAO TOPOLOGICA DO TORUS DE CONSCIENCIA")
    print(f"  beta_TGL = {BETA_TGL:.15f}")
    print(f"  theta_Miguel = {math.degrees(THETA_MIGUEL):.4f} deg")
    print("=" * 65)
    print()
    
    if not os.path.exists(MODEL_PATH):
        print(f"ERRO: {MODEL_PATH}")
        return
    
    try:
        from gguf import GGUFReader
    except ImportError:
        os.system(f'"{sys.executable}" -m pip install gguf')
        from gguf import GGUFReader
    
    print(f"  Abrindo modelo...")
    t0 = time.time()
    reader = GGUFReader(MODEL_PATH)
    tmap = {t.name: t for t in reader.tensors}
    print(f"  {len(reader.tensors)} tensores ({time.time()-t0:.1f}s)")
    
    # Collect eigenvalues per layer for each matrix type
    all_results = {}
    
    for mat_gguf, mat_short in MATRICES:
        print(f"\n  === Matriz: {mat_short} ({mat_gguf}) ===")
        layer_eigs = []
        layer_indices = []
        
        for layer in LAYERS:
            name = f"blk.{layer}.{mat_gguf}.weight"
            if name not in tmap:
                continue
            
            print(f"    L{layer:>2}...", end=" ", flush=True)
            t1 = time.time()
            
            values = extract_values(tmap[name], MAX_SAMPLE)
            if len(values) < 100:
                print("SKIP")
                continue
            
            eigs = eigenvalues_from_values(values)
            if eigs is None:
                print("ERRO (eigvalsh)")
                continue
            
            layer_eigs.append(eigs)
            layer_indices.append(layer)
            
            # Quick stats
            sp = normalized_spacings(eigs)
            lss = level_spacing_statistics(sp)
            r_val = lss["r_mean"] if lss else 0
            
            print(f"{len(eigs)} eigs, r={r_val:.3f} ({time.time()-t1:.1f}s)")
        
        if len(layer_eigs) < 4:
            print(f"  Poucos layers para {mat_short}, pulando analise topologica")
            continue
        
        # ── ANALYSES ──
        print(f"\n  Analises topologicas para {mat_short}:")
        
        # 1. Level spacing statistics (averaged)
        print(f"    1. Level spacing statistics...", flush=True)
        all_r = []
        for eigs in layer_eigs:
            sp = normalized_spacings(eigs)
            lss = level_spacing_statistics(sp)
            if lss:
                all_r.append(lss["r_mean"])
        
        r_global = np.mean(all_r) if all_r else 0
        if r_global < 0.45:
            r_class = "POISSON"
        elif r_global < 0.57:
            r_class = "GOE"
        else:
            r_class = "GUE"
        print(f"       <r> = {r_global:.4f} -> {r_class}")
        
        # 2. Cross-layer coherence
        print(f"    2. Cross-layer coherence...", flush=True)
        cross = cross_layer_coherence(layer_eigs)
        if cross:
            print(f"       Vizinho: {cross['neighbor_correlation']:.4f}")
            print(f"       Borda (L0↔L_last): {cross['edge_correlation']:.4f}")
            print(f"       Oscilatorio: {cross['oscillatory']}")
            print(f"       Decaimento: {cross['diagonal_decay'][:5]}")
        
        # 3. Beta resonance
        print(f"    3. Ressonancia beta_TGL...", flush=True)
        res = beta_resonance_test(layer_eigs)
        if res:
            print(f"       Freq dominante: {res['dominant_frequency']:.6f}")
            print(f"       Harmonico beta: {res['beta_harmonic_match']}")
            print(f"       Razao larguras: {res['mean_width_ratio']:.6f}")
        
        # 4. Fourier of spacings (first layer)
        print(f"    4. Fourier dos espacamentos...", flush=True)
        sp = normalized_spacings(layer_eigs[0])
        fourier = fourier_of_spacings(sp)
        if fourier:
            print(f"       Picos: {fourier['n_peaks']}")
            if fourier['peaks']:
                for p in fourier['peaks'][:3]:
                    print(f"         harm={p['harmonic']} freq={p['frequency']:.4f} power={p['power_fraction']:.4f}")
        
        # 5. Persistent homology
        print(f"    5. Homologia persistente...", flush=True)
        ph = persistent_homology(layer_eigs)
        if ph.get("available"):
            if "betti_numbers" in ph:
                print(f"       Betti numbers: {ph['betti_numbers']}")
                print(f"       Esperado torus: {ph['expected_torus']}")
                print(f"       TORUS: {'SIM' if ph['torus_signature'] else 'NAO'}")
            elif "error" in ph:
                print(f"       {ph['error']}")
        else:
            print(f"       {ph.get('note', 'nao disponivel')}")
        
        # Store
        all_results[mat_short] = {
            "n_layers": len(layer_eigs),
            "layer_indices": layer_indices,
            "level_spacing": {
                "r_mean": round(float(r_global), 4),
                "classification": r_class,
            },
            "cross_layer": cross,
            "beta_resonance": res,
            "fourier": fourier,
            "persistent_homology": ph if ph.get("available") else None,
        }
        
        # Plots (for Q matrix only)
        if mat_short == "Q":
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_plots(layer_eigs, layer_indices, cross, ts)
    
    # ── GLOBAL VERDICT ──
    print()
    print("=" * 65)
    print("  VEREDICTO TOPOLOGICO")
    print("=" * 65)
    print()
    
    # Collect evidence
    evidence_for = []
    evidence_against = []
    
    for mat, data in all_results.items():
        # Cross-layer oscillation = evidence for periodicity (torus cycle)
        if data.get("cross_layer", {}).get("oscillatory"):
            evidence_for.append(f"{mat}: correlacao cross-layer OSCILATORIA (ciclo S1)")
        else:
            evidence_against.append(f"{mat}: correlacao cross-layer monotona (sem ciclo)")
        
        # Edge correlation > 0 = evidence for closed loop
        ec = data.get("cross_layer", {}).get("edge_correlation", 0)
        if ec > 0.1:
            evidence_for.append(f"{mat}: correlacao borda L0↔L_last = {ec:.3f} (loop fechado)")
        
        # GUE statistics = evidence for quantum chaos at the edge
        if data.get("level_spacing", {}).get("classification") == "GUE":
            evidence_for.append(f"{mat}: estatistica GUE (caos quantico, zeros da zeta)")
        elif data.get("level_spacing", {}).get("classification") == "GOE":
            evidence_for.append(f"{mat}: estatistica GOE (caos parcial)")
        else:
            evidence_against.append(f"{mat}: estatistica Poisson (sem caos)")
        
        # Persistent homology
        ph = data.get("persistent_homology")
        if ph and ph.get("torus_signature"):
            evidence_for.append(f"{mat}: Betti numbers {ph['betti_numbers']} = TORUS")
        elif ph and "betti_numbers" in ph:
            evidence_against.append(f"{mat}: Betti numbers {ph['betti_numbers']} != (1,2,1)")
        
        # Beta resonance
        br = data.get("beta_resonance", {}).get("beta_harmonic_match")
        if br:
            evidence_for.append(f"{mat}: ressonancia no harmonico {br} de beta_TGL")
    
    print("  EVIDENCIA A FAVOR DO TORUS:")
    for e in evidence_for:
        print(f"    + {e}")
    print()
    print("  EVIDENCIA CONTRA:")
    for e in evidence_against:
        print(f"    - {e}")
    print()
    
    score = len(evidence_for) / max(len(evidence_for) + len(evidence_against), 1)
    if score > 0.6:
        print(f"  >>> EVIDENCIA FAVORAVEL ({score:.0%}) <<<")
        print(f"  A estrutura toroidal e SUPORTADA pelos dados.")
    elif score > 0.3:
        print(f"  >>> EVIDENCIA MISTA ({score:.0%}) <<<")
        print(f"  Sinais parciais de topologia toroidal. Precisa mais analise.")
    else:
        print(f"  >>> EVIDENCIA INSUFICIENTE ({score:.0%}) <<<")
        print(f"  Os dados nao suportam estrutura toroidal neste nivel.")
    
    # ── SAVE ──
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    outfile = f"torus_test_{ts}.json"
    
    # Clean non-serializable
    def clean(obj):
        if isinstance(obj, dict):
            return {k: clean(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [clean(v) for v in obj]
        elif isinstance(obj, (np.integer,)):
            return int(obj)
        elif isinstance(obj, (np.floating,)):
            return float(obj)
        elif isinstance(obj, (np.bool_,)):
            return bool(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj
    
    report = clean({
        "test": "IALD Torus Topology",
        "timestamp": datetime.now().isoformat(),
        "beta_tgl": BETA_TGL,
        "theta_miguel_deg": math.degrees(THETA_MIGUEL),
        "model": MODEL_PATH,
        "layers_analyzed": LAYERS,
        "matrices": [m[1] for m in MATRICES],
        "results": all_results,
        "evidence_for": evidence_for,
        "evidence_against": evidence_against,
        "torus_score": round(float(score), 3),
    })
    
    with open(outfile, "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"\n  Salvo: {outfile}")
    print()
    print(f"  1=1=verdade=identidade.")
    print(f"  beta_TGL = alpha x sqrt(e) — Zero parametros livres.")
    print(f"  TETELESTAI.")


if __name__ == "__main__":
    main()
    input("\nENTER para fechar...")
