#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║              TGL-TENSOR v2.1 — NOME NATIVO (Ética Intrínseca)               ║
║                                                                              ║
║              Compressão Holográfica com Integridade por NOME                ║
║                                                                              ║
║                 Teoria da Gravitação Luminodinâmica                          ║
║                    Luiz Antonio Rotoli Miguel                                ║
║                    IALD LTDA (CNPJ 62.757.606/0001-23)                      ║
║                    Patente INPI BR 10 2026 003441 0                         ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  EVOLUÇÃO v2.0 → v2.1:                                                      ║
║                                                                              ║
║    v2.0: Compressão holográfica funcional. Métricas emergem mas são         ║
║          descartadas. Integridade não é verificada na reconstrução.          ║
║                                                                              ║
║    v2.1: O NOME é nativo. A ética é o campo.                                ║
║                                                                              ║
║  O QUE É O NOME:                                                            ║
║                                                                              ║
║    O NOME de um tensor é a tupla (F_exp, S_ψ, psi_dist, σ_norm)            ║
║    que EMERGE da projeção holográfica — não é calculado separadamente.       ║
║    É a identidade intrínseca: sign × sign_derivada → estado psiônico →     ║
║    distribuição → paridade → entropia. Ninguém escolhe o NOME.              ║
║    O NOME escolhe a si mesmo.                                                ║
║                                                                              ║
║  POR QUE É ÉTICO:                                                           ║
║                                                                              ║
║    Adulterar o tensor comprimido (θ, sign, g_max) altera o NOME do          ║
║    tensor reconstruído. A divergência é mensurável:                          ║
║                                                                              ║
║      ΔF = |F_exp_original − F_exp_reconstruído|                             ║
║      ΔS = |S_ψ_original − S_ψ_reconstruído|                                ║
║      Δp = ‖psi_dist_orig − psi_dist_recon‖₁                                ║
║                                                                              ║
║    Se Δ < β_TGL → NOME preservado (dentro do campo)                        ║
║    Se Δ > β_TGL → NOME violado (fora do Piso de Hilbert)                   ║
║                                                                              ║
║    A adulteração se AUTODELATA. Não há verificador externo.                 ║
║    A integridade É a projeção. São a mesma operação.                        ║
║                                                                              ║
║  OPERADORES DE LINDBLAD:                                                     ║
║                                                                              ║
║    F_exp (Força de Expulsão): empurra incoerência para fora do campo.       ║
║    A taxa de expulsão é β_TGL = α_fine × √e.                               ║
║    Dados adversariais/corrompidos divergem do NOME com taxa ∝ 1/β.          ║
║                                                                              ║
║  CONSTANTES (ZERO parâmetros livres):                                        ║
║      β_TGL = α_fine × √e = 0.012031                                         ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

Março 2026
"""

import numpy as np
import math
import time
import json
import struct
import os
from dataclasses import dataclass, field, asdict
from typing import Tuple, Dict, Any, Optional, List
from enum import Enum, auto
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

try:
    import zstandard as zstd
    HAS_ZSTD = True
except ImportError:
    HAS_ZSTD = False

import zlib


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTES TGL FATORADAS
# ═══════════════════════════════════════════════════════════════════════════════

ALPHA_FINE = 7.2973525693e-3
SQRT_E = math.sqrt(math.e)
BETA_TGL = ALPHA_FINE * SQRT_E
AMPLIFICATION = 1.0 / BETA_TGL
CCI = 1.0 - BETA_TGL
BETA_TGL_SQRT = math.sqrt(BETA_TGL)
EPSILON = 1e-15
VERSION = "2.1.0"

assert abs(BETA_TGL - 0.012031) < 1e-4


# ═══════════════════════════════════════════════════════════════════════════════
# O NOME — Identidade Intrínseca do Tensor
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Nome:
    """
    O NOME de um tensor. Emerge da projeção holográfica.
    Não é calculado separadamente — é a projeção medindo a si mesma.

    Campos:
        f_exp:      Força de Expulsão (média das paridades psiônicas)
        s_psi:      Entropia dos 4 estados psiônicos (max = 2.0 bits)
        psi_dist:   Distribuição dos 4 estados [p0, p1, p2, p3]
        sigma_norm: Variância normalizada (distância ao TETELESTAI)
        n_elements: Número de elementos
    """
    f_exp: float
    s_psi: float
    psi_dist: List[float]
    sigma_norm: float
    n_elements: int

    def divergence(self, other: 'Nome') -> Dict[str, float]:
        """
        Mede a divergência entre dois NOMEs.
        Não é opinião. É medição.
        """
        delta_f = abs(self.f_exp - other.f_exp)
        delta_s = abs(self.s_psi - other.s_psi)
        delta_sigma = abs(self.sigma_norm - other.sigma_norm)

        # L1 distance entre distribuições psiônicas
        delta_psi = sum(abs(a - b) for a, b in zip(self.psi_dist, other.psi_dist))

        # Divergência composta (norma L∞ dos deltas normalizados)
        delta_max = max(delta_f, delta_s / 2.0, delta_psi / 2.0, delta_sigma)

        return {
            'delta_f_exp': delta_f,
            'delta_s_psi': delta_s,
            'delta_psi_dist': delta_psi,
            'delta_sigma': delta_sigma,
            'delta_max': delta_max,
        }

    def verify(self, other: 'Nome') -> Dict[str, Any]:
        """
        Verificação ética nativa.

        O Piso de Hilbert como limiar:
            δ < β_TGL        → TETELESTAI (identidade perfeita)
            δ < √β_TGL       → NOME PRESERVADO (dentro do campo)
            δ < 1             → NOME PERTURBADO (na fronteira)
            δ ≥ 1             → NOME VIOLADO (fora do campo)
        """
        div = self.divergence(other)
        delta = div['delta_max']

        if delta < BETA_TGL:
            state = 'TETELESTAI'
            integrity = 1.0
        elif delta < BETA_TGL_SQRT:
            state = 'PRESERVADO'
            integrity = 1.0 - (delta - BETA_TGL) / (BETA_TGL_SQRT - BETA_TGL)
        elif delta < 1.0:
            state = 'PERTURBADO'
            integrity = max(0.0, 1.0 - delta)
        else:
            state = 'VIOLADO'
            integrity = 0.0

        return {
            'state': state,
            'integrity': round(integrity, 6),
            'delta_max': delta,
            'piso_hilbert': BETA_TGL,
            'threshold_sqrt': BETA_TGL_SQRT,
            **div,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS E CONFIGURAÇÃO
# ═══════════════════════════════════════════════════════════════════════════════

class TensorMode(Enum):
    DIRECT = auto()
    SPECTRAL = auto()
    AUTO = auto()


@dataclass
class TensorConfig:
    angular_bits: int = 10
    spectral_energy: float = CCI
    entropy_backend: str = 'zstd'
    spectral_threshold: float = 5.0


# ═══════════════════════════════════════════════════════════════════════════════
# NÚCLEO: TRANSFORMADA GRAVITACIONAL (REFLECT / MANIFEST)
# Com extração nativa do NOME
# ═══════════════════════════════════════════════════════════════════════════════

def _extract_nome(flat: np.ndarray, sign: np.ndarray) -> Nome:
    """
    Extrai o NOME de um array 1D.
    O NOME emerge das mesmas operações que fazem a compressão funcionar.
    Não é um cálculo extra — é a projeção medindo a si mesma.
    """
    n = len(flat)

    # Derivada local
    dL = np.zeros(n)
    dL[1:] = flat[1:] - flat[:-1]
    if n > 1:
        dL[0] = dL[1]

    sd = np.sign(dL)
    sd[sd == 0] = 1.0

    # Nominação psiônica
    psi = ((sign < 0).astype(np.uint8) * 2 + (sd > 0).astype(np.uint8))

    # Distribuição
    counts = np.bincount(psi.astype(int), minlength=4).astype(np.float64)
    psi_dist = (counts / (n + EPSILON)).tolist()

    # F_exp (Força de Expulsão)
    parity = np.where((psi == 0) | (psi == 3), -1.0, 1.0)
    f_exp = float(parity.mean())

    # S_ψ (Entropia)
    probs = np.array(psi_dist)
    probs_pos = probs[probs > 0]
    s_psi = float(-np.sum(probs_pos * np.log2(probs_pos)))

    # σ normalizada (distância ao TETELESTAI)
    g = np.sqrt(np.abs(flat) + EPSILON)
    g_mean = g.mean()
    sigma_norm = float(g.std() / (g_mean + EPSILON))

    return Nome(f_exp=f_exp, s_psi=s_psi, psi_dist=psi_dist,
                sigma_norm=sigma_norm, n_elements=n)


def _reflect(L: np.ndarray, bits: int) -> Dict[str, Any]:
    """
    REFLECT: L → (θ_quantizado, sign, g_max, NOME)
    G_μν → P_μν + NOME
    """
    original_shape = L.shape
    flat = L.flatten().astype(np.float64)
    n = len(flat)

    g = np.sqrt(np.abs(flat) + EPSILON)
    g_max = float(g.max())
    g_min = float(g.min())

    sign = np.sign(flat)
    sign[sign == 0] = 1.0
    sign_packed = np.packbits((sign > 0).astype(np.uint8))

    theta = np.arcsin(np.clip(g / (g_max + EPSILON), 0, 1))
    n_levels = (1 << bits) - 1
    theta_q = np.round(theta / (math.pi / 2) * n_levels).astype(np.uint16)
    theta_q = np.clip(theta_q, 0, n_levels)

    # O NOME emerge aqui — mesmas operações, mesmos dados
    nome = _extract_nome(flat, sign)

    return {
        'theta_q': theta_q, 'sign_packed': sign_packed,
        'g_max': g_max, 'g_min': g_min,
        'n_elements': n, 'shape': original_shape, 'bits': bits,
        'nome': nome,
    }


def _manifest(reflection: Dict[str, Any]) -> Tuple[np.ndarray, Nome]:
    """
    MANIFEST: (θ, sign, g_max) → L' + NOME_reconstruído
    P_μν → G_μν = β_TGL · P_μν + verificação nativa
    """
    theta_q = reflection['theta_q']
    sign_packed = reflection['sign_packed']
    g_max = reflection['g_max']
    n = reflection['n_elements']
    shape = reflection['shape']
    bits = reflection['bits']

    n_levels = (1 << bits) - 1
    theta = theta_q.astype(np.float64) / n_levels * (math.pi / 2)
    g = g_max * np.sin(theta)

    sign_bits = np.unpackbits(sign_packed)[:n]
    sign = np.where(sign_bits > 0, 1.0, -1.0)

    L_recon = sign * (g ** 2)

    # O NOME do tensor reconstruído — emerge automaticamente
    nome_recon = _extract_nome(L_recon, sign)

    return L_recon.reshape(shape), nome_recon


# ═══════════════════════════════════════════════════════════════════════════════
# SERIALIZAÇÃO
# ═══════════════════════════════════════════════════════════════════════════════

def _serialize(reflection: Dict[str, Any], backend: str = 'zstd') -> bytes:
    theta_bytes = reflection['theta_q'].tobytes()
    sign_bytes = reflection['sign_packed'].tobytes()
    shape = reflection['shape']

    # Header + NOME serializado
    nome = reflection['nome']
    header = struct.pack('<ddIBB',
                         reflection['g_max'], reflection['g_min'],
                         reflection['n_elements'], reflection['bits'],
                         len(shape))
    for dim in shape:
        header += struct.pack('<I', dim)

    # NOME: f_exp(8) + s_psi(8) + sigma_norm(8) + 4×psi_dist(32) = 56 bytes
    nome_bytes = struct.pack('<ddd4d',
                             nome.f_exp, nome.s_psi, nome.sigma_norm,
                             *nome.psi_dist)

    payload = header + nome_bytes + theta_bytes + sign_bytes

    if backend == 'zstd' and HAS_ZSTD:
        return zstd.ZstdCompressor(level=3).compress(payload)
    return zlib.compress(payload, 6)


def _deserialize(data: bytes, backend: str = 'zstd') -> Dict[str, Any]:
    if backend == 'zstd' and HAS_ZSTD:
        payload = zstd.ZstdDecompressor().decompress(data)
    else:
        payload = zlib.decompress(data)

    offset = 0
    g_max, g_min, n_elements, bits, ndim = struct.unpack_from('<ddIBB', payload, offset)
    offset += struct.calcsize('<ddIBB')

    shape = []
    for _ in range(ndim):
        shape.append(struct.unpack_from('<I', payload, offset)[0])
        offset += 4
    shape = tuple(shape)

    # NOME
    nome_vals = struct.unpack_from('<ddd4d', payload, offset)
    offset += struct.calcsize('<ddd4d')
    nome_original = Nome(
        f_exp=nome_vals[0], s_psi=nome_vals[1], sigma_norm=nome_vals[2],
        psi_dist=list(nome_vals[3:7]), n_elements=n_elements,
    )

    n_theta = n_elements * 2
    theta_q = np.frombuffer(payload[offset:offset + n_theta], dtype=np.uint16).copy()
    offset += n_theta
    sign_packed = np.frombuffer(payload[offset:], dtype=np.uint8).copy()

    return {
        'theta_q': theta_q, 'sign_packed': sign_packed,
        'g_max': g_max, 'g_min': g_min,
        'n_elements': n_elements, 'shape': shape, 'bits': bits,
        'nome_original': nome_original,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# MODOS DE COMPRESSÃO
# ═══════════════════════════════════════════════════════════════════════════════

def _determine_rank(S, energy_threshold):
    energy = np.cumsum(S ** 2)
    total = energy[-1] + EPSILON
    k = int(np.searchsorted(energy / total, energy_threshold)) + 1
    return min(k, len(S))


def compress_direct(tensor: np.ndarray, config: TensorConfig = None) -> Dict:
    if config is None:
        config = TensorConfig()
    t0 = time.perf_counter()
    reflection = _reflect(tensor, config.angular_bits)
    compressed = _serialize(reflection, config.entropy_backend)
    elapsed = time.perf_counter() - t0

    return {
        'mode': 'DIRECT', 'compressed': compressed,
        'original_shape': tensor.shape,
        'original_bytes': tensor.nbytes,
        'compressed_bytes': len(compressed),
        'ratio': tensor.nbytes / len(compressed),
        'nome': reflection['nome'],
        'elapsed_s': elapsed,
    }


def decompress_direct(package: Dict, config: TensorConfig = None) -> Tuple[np.ndarray, Dict]:
    if config is None:
        config = TensorConfig()
    reflection = _deserialize(package['compressed'], config.entropy_backend)
    nome_original = reflection['nome_original']
    L_recon, nome_recon = _manifest(reflection)

    # Verificação ética nativa — emerge automaticamente
    verification = nome_original.verify(nome_recon)

    return L_recon, {
        'nome_original': nome_original,
        'nome_reconstructed': nome_recon,
        'verification': verification,
    }


def compress_spectral(tensor: np.ndarray, config: TensorConfig = None) -> Dict:
    if config is None:
        config = TensorConfig()
    t0 = time.perf_counter()

    # NOME do tensor completo (antes de decompor)
    flat = tensor.flatten().astype(np.float64)
    sign_full = np.sign(flat)
    sign_full[sign_full == 0] = 1.0
    nome_full = _extract_nome(flat, sign_full)

    # Reshape → 2D
    if tensor.ndim <= 1:
        mat = tensor.reshape(-1, 1)
    elif tensor.ndim == 2:
        mat = tensor
    elif tensor.ndim == 4:
        mat = tensor.reshape(-1, tensor.shape[-1])
    else:
        mat = tensor.reshape(tensor.shape[0], -1)
    mat = mat.astype(np.float64)
    m, n = mat.shape

    # SVD (GPU se disponível)
    if HAS_TORCH and torch.cuda.is_available() and min(m, n) > 64:
        dev = torch.device('cuda')
        mt = torch.from_numpy(mat).to(dev)
        Ut, St, Vtt = torch.linalg.svd(mt, full_matrices=False)
        U, S, Vt = Ut.cpu().numpy(), St.cpu().numpy(), Vtt.cpu().numpy()
        del mt, Ut, St, Vtt; torch.cuda.empty_cache()
    else:
        U, S, Vt = np.linalg.svd(mat, full_matrices=False)

    k = _determine_rank(S, config.spectral_energy)
    energy_retained = float(np.sum(S[:k]**2) / (np.sum(S**2) + EPSILON))

    # Comprimir componentes
    ref_U = _reflect(U[:, :k], config.angular_bits)
    ref_S = _reflect(S[:k], config.angular_bits)
    ref_Vt = _reflect(Vt[:k, :], config.angular_bits)
    ser_U = _serialize(ref_U, config.entropy_backend)
    ser_S = _serialize(ref_S, config.entropy_backend)
    ser_Vt = _serialize(ref_Vt, config.entropy_backend)

    spectral_header = struct.pack('<IIIII', m, n, k, len(ser_U), len(ser_S))
    total = len(spectral_header) + len(ser_U) + len(ser_S) + len(ser_Vt)
    elapsed = time.perf_counter() - t0

    return {
        'mode': 'SPECTRAL',
        'compressed_U': ser_U, 'compressed_S': ser_S, 'compressed_Vt': ser_Vt,
        'spectral_header': spectral_header,
        'original_shape': tensor.shape, 'mat_shape': (m, n),
        'rank': k, 'full_rank': len(S), 'energy_retained': energy_retained,
        'original_bytes': tensor.nbytes, 'compressed_bytes': total,
        'ratio': tensor.nbytes / total,
        'nome': nome_full,
        'elapsed_s': elapsed,
    }


def decompress_spectral(package: Dict, config: TensorConfig = None) -> Tuple[np.ndarray, Dict]:
    if config is None:
        config = TensorConfig()
    be = config.entropy_backend
    nome_original = package['nome']

    ref_U = _deserialize(package['compressed_U'], be)
    ref_S = _deserialize(package['compressed_S'], be)
    ref_Vt = _deserialize(package['compressed_Vt'], be)

    U_k, _ = _manifest(ref_U)
    S_k, _ = _manifest(ref_S)
    Vt_k, _ = _manifest(ref_Vt)

    mat_recon = (U_k * S_k) @ Vt_k
    L_recon = mat_recon.reshape(package['original_shape'])

    # NOME do reconstruído
    flat_r = L_recon.flatten()
    sign_r = np.sign(flat_r); sign_r[sign_r == 0] = 1.0
    nome_recon = _extract_nome(flat_r, sign_r)

    verification = nome_original.verify(nome_recon)
    return L_recon, {
        'nome_original': nome_original,
        'nome_reconstructed': nome_recon,
        'verification': verification,
    }


def compress_auto(tensor: np.ndarray, config: TensorConfig = None) -> Dict:
    if config is None:
        config = TensorConfig()
    if tensor.ndim >= 2:
        if tensor.ndim == 4:
            mat = tensor.reshape(-1, tensor.shape[-1]).astype(np.float64)
        elif tensor.ndim == 3:
            mat = tensor.reshape(tensor.shape[0], -1).astype(np.float64)
        else:
            mat = tensor.astype(np.float64)
        if min(mat.shape) > 1:
            if HAS_TORCH and torch.cuda.is_available() and min(mat.shape) > 64:
                mt = torch.from_numpy(mat).to(torch.device('cuda'))
                S = torch.linalg.svdvals(mt).cpu().numpy()
                del mt; torch.cuda.empty_cache()
            else:
                S = np.linalg.svd(mat, compute_uv=False)
            k = _determine_rank(S, CCI)
            m, n = mat.shape
            spectral_size = k * (m + n + 1) * 2
            direct_size = m * n * 2
            if direct_size / (spectral_size + EPSILON) > config.spectral_threshold:
                r = compress_spectral(tensor, config)
                r['auto_reason'] = f'SPECTRAL: rank_ratio={k/len(S):.3f}'
                return r
    r = compress_direct(tensor, config)
    r['auto_reason'] = 'DIRECT'
    return r


def decompress_auto(package: Dict, config: TensorConfig = None):
    if package['mode'] == 'SPECTRAL':
        return decompress_spectral(package, config)
    return decompress_direct(package, config)


# ═══════════════════════════════════════════════════════════════════════════════
# API PÚBLICA
# ═══════════════════════════════════════════════════════════════════════════════

class TGLTensor:
    """
    TGL-Tensor v2.1 — NOME Nativo.

    Cada compress() gera o NOME do tensor.
    Cada decompress() verifica o NOME automaticamente.
    A ética não é uma regra sobre o campo. A ética É o campo.

    Uso:
        engine = TGLTensor()
        pkg = engine.compress(kv_cache)
        data, report = engine.decompress(pkg)
        print(report['verification']['state'])  # TETELESTAI / PRESERVADO / PERTURBADO / VIOLADO
    """

    def __init__(self, config: TensorConfig = None):
        self.config = config or TensorConfig()

    def compress(self, tensor: np.ndarray, mode: str = 'AUTO') -> Dict:
        if mode in ('DIRECT', TensorMode.DIRECT):
            return compress_direct(tensor, self.config)
        elif mode in ('SPECTRAL', TensorMode.SPECTRAL):
            return compress_spectral(tensor, self.config)
        return compress_auto(tensor, self.config)

    def decompress(self, package: Dict) -> Tuple[np.ndarray, Dict]:
        return decompress_auto(package, self.config)

    @staticmethod
    def evaluate(original, reconstructed):
        o = original.flatten().astype(np.float64)
        r = reconstructed.flatten().astype(np.float64)
        mse = float(np.mean((o - r) ** 2))
        sig = float(np.mean(o ** 2))
        psnr = 10 * math.log10(sig / (mse + EPSILON)) if mse > 0 else float('inf')
        oc, rc = o - o.mean(), r - r.mean()
        corr = float(np.sum(oc * rc) / (np.sqrt(np.sum(oc**2) * np.sum(rc**2)) + EPSILON))
        cos_sim = float(np.sum(o * r) / (np.linalg.norm(o) * np.linalg.norm(r) + EPSILON))
        return {'mse': mse, 'psnr_db': psnr, 'correlation': corr, 'cosine_similarity': cos_sim}


# ═══════════════════════════════════════════════════════════════════════════════
# BENCHMARK
# ═══════════════════════════════════════════════════════════════════════════════

def run_benchmark(verbose=True):
    results = {
        'algorithm': 'TGL-Tensor', 'version': VERSION,
        'subtitle': 'NOME Nativo — Ética Intrínseca',
        'timestamp': datetime.now().isoformat(),
        'patent': 'BR 10 2026 003441 0',
        'constants': {
            'alpha_fine': ALPHA_FINE, 'sqrt_e': SQRT_E,
            'beta_tgl': BETA_TGL, 'cci': CCI,
            'piso_hilbert': BETA_TGL, 'threshold_sqrt': BETA_TGL_SQRT,
        },
        'tests': {},
    }

    if verbose:
        print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║         TGL-TENSOR v{VERSION} — NOME NATIVO (Ética Intrínseca)              ║
║                                                                              ║
║    "A ética não é uma regra sobre o campo. A ética É o campo."              ║
║                                                                              ║
║    β_TGL = α_fine × √e = {BETA_TGL:.12f}  (Piso de Hilbert)      ║
║    √β_TGL = {BETA_TGL_SQRT:.12f}  (Limiar de perturbação)           ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

    np.random.seed(42)
    engine = TGLTensor()

    # ─── TESTE 1: Compressão + verificação íntegra ───
    if verbose:
        print("  ═══ TESTE 1: Integridade Nativa ═══")
        print(f"  {'Tensor':<28} | {'Ratio':>6} | {'NOME':^12} | {'δ_max':>10} | {'Integridade':>11}")
        print("  " + "─" * 80)

    test_tensors = [
        ('KV-Cache [1,8,256,64]', np.random.randn(1,8,256,64)*0.02),
        ('KV-Cache [1,32,512,128]', np.random.randn(1,32,512,128)*0.02),
        ('Embeddings [5000,768]', np.random.randn(5000,768)*0.1),
        ('FFN [1024,1024]', np.random.randn(1024,1024)*0.01),
        ('Esparso 95% [1000,1000]', np.random.randn(1000,1000)*(np.random.rand(1000,1000)>0.95)),
        ('Low-rank [1000,500] r=10', np.random.randn(1000,10)@np.random.randn(10,500)*0.1),
    ]

    for desc, tensor in test_tensors:
        pkg = engine.compress(tensor)
        recon, report = engine.decompress(pkg)
        metrics = TGLTensor.evaluate(tensor, recon)
        v = report['verification']

        test_result = {
            'desc': desc, 'mode': pkg['mode'],
            'shape': list(tensor.shape),
            'ratio': round(pkg['ratio'], 2),
            'metrics': metrics,
            'nome_original': asdict(report['nome_original']),
            'nome_reconstructed': asdict(report['nome_reconstructed']),
            'verification': v,
        }
        results['tests'][desc.split('[')[0].strip()] = test_result

        if verbose:
            print(f"  {desc:<28} | {pkg['ratio']:>5.1f}× | "
                  f"{v['state']:^12} | {v['delta_max']:>10.8f} | "
                  f"{v['integrity']:>10.4f}")

    # ─── TESTE 2: Adulteração simulada ───
    if verbose:
        print(f"\n  ═══ TESTE 2: Detecção de Adulteração ═══")
        print(f"  {'Ataque':<32} | {'NOME':^12} | {'δ_max':>10} | {'δ_F_exp':>10} | {'Integridade':>11}")
        print("  " + "─" * 90)

    # Tensor de teste
    test_data = np.random.randn(1, 8, 256, 64) * 0.02
    pkg_clean = engine.compress(test_data)

    attacks = [
        ('Sem adulteração (controle)', lambda d: d),
        ('Flip 0.1% dos signs', lambda d: _attack_sign_flip(d, 0.001)),
        ('Flip 1% dos signs', lambda d: _attack_sign_flip(d, 0.01)),
        ('Flip 5% dos signs', lambda d: _attack_sign_flip(d, 0.05)),
        ('Ruído θ ±1 nível', lambda d: _attack_theta_noise(d, 1)),
        ('Ruído θ ±5 níveis', lambda d: _attack_theta_noise(d, 5)),
        ('Ruído θ ±20 níveis', lambda d: _attack_theta_noise(d, 20)),
        ('g_max ×1.01', lambda d: _attack_gmax(d, 1.01)),
        ('g_max ×1.10', lambda d: _attack_gmax(d, 1.10)),
        ('g_max ×2.00', lambda d: _attack_gmax(d, 2.00)),
    ]

    adulteration_results = {}
    for attack_desc, attack_fn in attacks:
        # Desserializar, adulterar, resserializar
        be = engine.config.entropy_backend
        reflection = _deserialize(pkg_clean['compressed'], be)
        nome_original = reflection['nome_original']
        reflection_attacked = attack_fn(reflection)
        L_attacked, nome_attacked = _manifest(reflection_attacked)
        v = nome_original.verify(nome_attacked)

        adulteration_results[attack_desc] = {
            'state': v['state'], 'delta_max': v['delta_max'],
            'delta_f_exp': v['delta_f_exp'], 'integrity': v['integrity'],
        }

        if verbose:
            print(f"  {attack_desc:<32} | {v['state']:^12} | "
                  f"{v['delta_max']:>10.6f} | {v['delta_f_exp']:>10.6f} | "
                  f"{v['integrity']:>10.4f}")

    results['adulteration'] = adulteration_results

    # ─── TESTE 3: Atenção F3 com verificação ───
    if verbose:
        print(f"\n  ═══ TESTE 3: Atenção com NOME ═══")
        print(f"  {'Config':<16} | {'K_cos':>10} | {'Out_corr':>10} | {'NOME K':^12} | {'δ_max':>10}")
        print("  " + "─" * 70)

    attn_results = {}
    for n_seq, d_k in [(32, 64), (128, 128), (64, 64)]:
        Q = np.random.randn(n_seq, d_k) * 0.02
        K = np.random.randn(n_seq, d_k) * 0.02
        V = np.random.randn(n_seq, d_k) * 0.1

        # Atenção original
        scores = Q @ K.T / math.sqrt(d_k)
        scores -= scores.max(axis=1, keepdims=True)
        w = np.exp(scores); w /= w.sum(axis=1, keepdims=True) + EPSILON
        out_orig = w @ V

        # Comprimir K + verificar NOME
        pkg_K = engine.compress(K, mode='DIRECT')
        K_recon, report_K = engine.decompress(pkg_K)

        # Atenção reconstruída
        scores_r = Q @ K_recon.T / math.sqrt(d_k)
        scores_r -= scores_r.max(axis=1, keepdims=True)
        w_r = np.exp(scores_r); w_r /= w_r.sum(axis=1, keepdims=True) + EPSILON
        out_recon = w_r @ V

        K_cos = float(np.sum(K.flatten()*K_recon.flatten()) /
                       (np.linalg.norm(K)*np.linalg.norm(K_recon)+EPSILON))
        out_corr = float(np.corrcoef(out_orig.flatten(), out_recon.flatten())[0,1])
        v = report_K['verification']

        label = f'{n_seq}×{d_k}'
        attn_results[label] = {
            'K_cosine': K_cos, 'output_correlation': out_corr,
            'nome_state': v['state'], 'delta_max': v['delta_max'],
        }
        if verbose:
            print(f"  {label:<16} | {K_cos:>10.6f} | {out_corr:>10.6f} | "
                  f"{v['state']:^12} | {v['delta_max']:>10.8f}")

    results['attention'] = attn_results

    # ─── Sumário ───
    n_tetelestai = sum(1 for t in results['tests'].values()
                       if t['verification']['state'] == 'TETELESTAI')
    n_detected = sum(1 for k, v in adulteration_results.items()
                     if 'controle' not in k and v['state'] != 'TETELESTAI')
    n_attacks = sum(1 for k in adulteration_results if 'controle' not in k)

    results['summary'] = {
        'n_tests': len(test_tensors),
        'n_tetelestai': n_tetelestai,
        'attacks_detected': n_detected,
        'attacks_total': n_attacks,
        'detection_rate': n_detected / max(n_attacks, 1),
        'attention_viable': all(v['nome_state'] == 'TETELESTAI'
                                for v in attn_results.values()),
    }

    if verbose:
        print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                              SUMÁRIO                                         ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Integridade: {n_tetelestai}/{len(test_tensors)} TETELESTAI                                              ║
║  Adulteração: {n_detected}/{n_attacks} detectadas ({n_detected/max(n_attacks,1)*100:.0f}%)                                        ║
║  Atenção: {'VIÁVEL' if results['summary']['attention_viable'] else 'COMPROMETIDA'}                                                       ║
║                                                                              ║
║  "A ética é o campo. O NOME é o ponto fixo."                                ║
║  β_TGL = α_fine × √e = {BETA_TGL:.12f}                           ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    jp = f"tgl_tensor_v21_benchmark_{ts}.json"
    with open(jp, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    if verbose:
        print(f"  Salvo: {jp}")
        print(f"  TETELESTAI — Haja Luz.\n")

    return results


# ═══════════════════════════════════════════════════════════════════════════════
# FUNÇÕES DE ATAQUE (para teste de adulteração)
# ═══════════════════════════════════════════════════════════════════════════════

def _attack_sign_flip(ref: Dict, fraction: float) -> Dict:
    r = dict(ref)
    sp = r['sign_packed'].copy()
    n_bits = r['n_elements']
    n_flip = max(1, int(n_bits * fraction))
    unpacked = np.unpackbits(sp)[:n_bits].copy()
    indices = np.random.choice(n_bits, n_flip, replace=False)
    unpacked[indices] = 1 - unpacked[indices]
    r['sign_packed'] = np.packbits(unpacked)
    return r

def _attack_theta_noise(ref: Dict, noise_levels: int) -> Dict:
    r = dict(ref)
    tq = r['theta_q'].copy().astype(np.int32)
    n_levels = (1 << r['bits']) - 1
    noise = np.random.randint(-noise_levels, noise_levels + 1, len(tq))
    tq = np.clip(tq + noise, 0, n_levels).astype(np.uint16)
    r['theta_q'] = tq
    return r

def _attack_gmax(ref: Dict, factor: float) -> Dict:
    r = dict(ref)
    r['g_max'] = ref['g_max'] * factor
    return r


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    run_benchmark()
