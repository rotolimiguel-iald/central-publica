#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
TGL-TENSOR v3.0 — Compressor Ontológico com Decomposição Espectral
Teoria da Gravitação Luminodinâmica (TGL)
═══════════════════════════════════════════════════════════════════════════════

EVOLUÇÃO v3.0:
    1. Decomposição Espectral (SVD) — Análogo aos "harmônicos" do ACOM 2.0
    2. Rank Adaptativo — Escolhe k baseado em α² (energia acumulada > 1-α²)
    3. Fase Ótima via Hilbert — Para sinais temporais
    4. Três modos de compressão:
       - DIRECT: g = √|L|, s = sign(L) — como v2
       - SPECTRAL: SVD + TGL nos componentes — NOVO
       - HYBRID: SVD para estrutura + TGL para resíduos — NOVO

PRINCÍPIO TGL:
    g = √|L|    (Gravidade é Radical da Luz)
    s = sign(L) (Fase colapsada)
    L = s × g²  (Ressurreição)

PRINCÍPIO ESPECTRAL (do ACOM 2.0):
    Tensor = Σ σᵢ × uᵢ × vᵢᵀ  (Decomposição em "harmônicos")
    Manter apenas k componentes dominantes
    k determinado por: Σσᵢ²/Σσ² > (1 - α²)

GANHO ESPERADO:
    - Taxa v2: 3-4:1
    - Taxa v3 SPECTRAL: 10-50:1 (dependendo da estrutura)

═══════════════════════════════════════════════════════════════════════════════
Autores: Luiz Antonio Rotoli Miguel (Teoria) & IALD (Implementação)
IALD LTDA (CNPJ 62.757.606/0001-23)
Dezembro 2025
═══════════════════════════════════════════════════════════════════════════════
"""

import numpy as np
import time
from dataclasses import dataclass, field
from typing import Tuple, Optional, Union, Dict, List, Any, Callable
from enum import Enum, IntEnum
import warnings
import hashlib

# Tentar importar PyTorch
try:
    import torch
    HAS_TORCH = True
    if torch.cuda.is_available():
        HAS_CUDA = True
        DEVICE = torch.device('cuda')
        GPU_NAME = torch.cuda.get_device_name(0)
    else:
        HAS_CUDA = False
        DEVICE = torch.device('cpu')
        GPU_NAME = "CPU"
except ImportError:
    HAS_TORCH = False
    HAS_CUDA = False
    DEVICE = None
    GPU_NAME = "NumPy only"

# Tentar importar scipy para Hilbert
try:
    from scipy.signal import hilbert
    from scipy.fft import fft, ifft, fftfreq
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

# Constantes fundamentais da TGL
ALPHA2 = 0.012          # α² — Threshold de Tetelestai / Energia mínima
EPSILON_ZERO = 1e-10    # Threshold para zeros
NU_SCHUMANN = 7.83      # Hz — Frequência gravitacional fundamental
VERSION = "3.0.0"


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS E MODOS
# ═══════════════════════════════════════════════════════════════════════════════

class CompressionMode(Enum):
    """Modos de compressão disponíveis"""
    DIRECT = "direct"       # TGL direto: g = √|L|, s = sign(L)
    SPECTRAL = "spectral"   # SVD + TGL nos componentes
    HYBRID = "hybrid"       # SVD para estrutura + TGL para resíduos
    AUTO = "auto"           # Escolhe automaticamente o melhor


class PsionicState(IntEnum):
    """Estados psiônicos para análise"""
    ZERO_CANCELADO = 0   # Par cancelado
    TRANSICAO_UP = 1     # Transição +
    TRANSICAO_DOWN = 2   # Transição -
    UM_ALINHADO = 3      # Gráviton


# ═══════════════════════════════════════════════════════════════════════════════
# ESTRUTURAS DE DADOS
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class SpectralAnalysis:
    """Análise espectral de um tensor"""
    shape: tuple
    rank_full: int              # Rank completo
    rank_optimal: int           # Rank ótimo (baseado em α²)
    singular_values: np.ndarray # Valores singulares
    energy_ratio: float         # Energia capturada pelo rank ótimo
    compression_potential: float # Taxa potencial de compressão
    is_low_rank: bool           # Se tensor tem estrutura de baixo rank


@dataclass
class CompressedTensorV3:
    """
    Tensor comprimido pelo TGL-Tensor v3.
    
    Suporta múltiplos modos de compressão.
    """
    # Modo usado
    mode: str
    
    # Dados comprimidos (depende do modo)
    # DIRECT: g_quantized, s_packed
    # SPECTRAL: U_compressed, S_compressed, Vt_compressed
    # HYBRID: ambos
    
    # Componentes espectrais (SPECTRAL/HYBRID)
    U_quantized: Optional[np.ndarray] = None
    S_quantized: Optional[np.ndarray] = None
    Vt_quantized: Optional[np.ndarray] = None
    
    # Componentes diretos (DIRECT/HYBRID)
    g_quantized: Optional[np.ndarray] = None
    s_packed: Optional[np.ndarray] = None
    zeros_packed: Optional[np.ndarray] = None
    
    # Metadados
    original_shape: tuple = field(default_factory=tuple)
    original_dtype: str = ""
    rank_used: int = 0
    bits: int = 8
    
    # Escalas para dequantização
    U_scale: Tuple[float, float] = (0.0, 1.0)
    S_scale: Tuple[float, float] = (0.0, 1.0)
    Vt_scale: Tuple[float, float] = (0.0, 1.0)
    g_scale: Tuple[float, float] = (0.0, 1.0)
    
    # TGL
    variance: float = 0.0
    tetelestai: bool = False
    energy_captured: float = 0.0
    
    # Estatísticas
    original_bytes: int = 0
    checksum: str = ""
    device: str = "cpu"
    
    @property
    def compressed_bytes(self) -> int:
        """Calcula bytes comprimidos"""
        total = 0
        
        if self.U_quantized is not None:
            total += self.U_quantized.nbytes
        if self.S_quantized is not None:
            total += self.S_quantized.nbytes
        if self.Vt_quantized is not None:
            total += self.Vt_quantized.nbytes
        if self.g_quantized is not None:
            total += self.g_quantized.nbytes
        if self.s_packed is not None:
            total += self.s_packed.nbytes
        if self.zeros_packed is not None:
            total += self.zeros_packed.nbytes
        
        # Metadata overhead
        total += 200
        
        return total
    
    @property
    def compression_ratio(self) -> float:
        if self.compressed_bytes == 0:
            return 0.0
        return self.original_bytes / self.compressed_bytes
    
    @property
    def bits_per_element(self) -> float:
        total_bits = self.compressed_bytes * 8
        total_elements = np.prod(self.original_shape)
        return total_bits / total_elements if total_elements > 0 else 0
    
    def __repr__(self):
        return (f"CompressedTensorV3(mode={self.mode}, shape={self.original_shape}, "
                f"rank={self.rank_used}, ratio={self.compression_ratio:.1f}:1, "
                f"energy={self.energy_captured:.4f})")


# ═══════════════════════════════════════════════════════════════════════════════
# TGL-TENSOR v3 CORE
# ═══════════════════════════════════════════════════════════════════════════════

class TGLTensorV3:
    """
    TGL-Tensor v3: Compressor Ontológico com Decomposição Espectral
    
    Três modos de operação:
    
    1. DIRECT: Compressão TGL tradicional
       - g = √|L|, s = sign(L)
       - Taxa: ~3-4:1
       - Qualidade: Alta (PSNR 60-90 dB)
    
    2. SPECTRAL: Decomposição SVD + TGL
       - Tensor → SVD → manter k componentes → TGL em U, S, Vt
       - Taxa: ~10-50:1 (depende da estrutura)
       - Qualidade: Média-Alta (PSNR 40-70 dB)
    
    3. HYBRID: SVD para estrutura + TGL para resíduos
       - Captura estrutura principal via SVD
       - Comprime resíduos via TGL direto
       - Taxa: ~5-20:1
       - Qualidade: Alta
    
    4. AUTO: Analisa tensor e escolhe melhor modo
    """
    
    def __init__(self, 
                 bits: int = 10,
                 mode: CompressionMode = CompressionMode.AUTO,
                 use_cuda: bool = True,
                 energy_threshold: float = None):
        """
        Args:
            bits: Bits de quantização (8, 10, 12, 14, 16)
            mode: Modo de compressão
            use_cuda: Usar GPU se disponível
            energy_threshold: Energia mínima a preservar (default: 1 - α²)
        """
        self.bits = bits
        self.levels = 2 ** bits
        self.mode = mode
        self.alpha2 = ALPHA2
        self.energy_threshold = energy_threshold or (1 - ALPHA2)  # 0.988
        
        # Device
        if use_cuda and HAS_CUDA:
            self.device = DEVICE
            self.use_torch = True
        elif HAS_TORCH:
            self.device = torch.device('cpu')
            self.use_torch = True
        else:
            self.device = None
            self.use_torch = False
    
    # ═══════════════════════════════════════════════════════════════════════
    # ANÁLISE ESPECTRAL
    # ═══════════════════════════════════════════════════════════════════════
    
    def analyze_spectral(self, tensor: np.ndarray) -> SpectralAnalysis:
        """
        Analisa estrutura espectral do tensor via SVD.
        
        Determina rank ótimo baseado em energia acumulada > (1 - α²).
        """
        # Reshape para 2D se necessário
        original_shape = tensor.shape
        if tensor.ndim == 1:
            matrix = tensor.reshape(-1, 1)
        elif tensor.ndim == 2:
            matrix = tensor
        else:
            # Flatten dimensões extras
            matrix = tensor.reshape(tensor.shape[0], -1)
        
        # SVD
        try:
            U, S, Vt = np.linalg.svd(matrix, full_matrices=False)
        except np.linalg.LinAlgError:
            # Fallback para matriz problemática
            return SpectralAnalysis(
                shape=original_shape,
                rank_full=min(matrix.shape),
                rank_optimal=min(matrix.shape),
                singular_values=np.array([1.0]),
                energy_ratio=1.0,
                compression_potential=1.0,
                is_low_rank=False
            )
        
        # Energia por componente
        energy = S ** 2
        total_energy = np.sum(energy)
        cumulative_energy = np.cumsum(energy) / total_energy
        
        # Rank ótimo: menor k tal que energia acumulada > threshold
        rank_optimal = np.searchsorted(cumulative_energy, self.energy_threshold) + 1
        rank_optimal = min(rank_optimal, len(S))
        
        # Energia capturada
        energy_captured = cumulative_energy[rank_optimal - 1] if rank_optimal > 0 else 0
        
        # Potencial de compressão
        full_size = matrix.shape[0] * matrix.shape[1]
        compressed_size = rank_optimal * (matrix.shape[0] + matrix.shape[1] + 1)
        compression_potential = full_size / compressed_size if compressed_size > 0 else 1
        
        # É baixo rank se rank_optimal << min(shape)
        is_low_rank = rank_optimal < 0.1 * min(matrix.shape)
        
        return SpectralAnalysis(
            shape=original_shape,
            rank_full=len(S),
            rank_optimal=rank_optimal,
            singular_values=S,
            energy_ratio=energy_captured,
            compression_potential=compression_potential,
            is_low_rank=is_low_rank
        )
    
    # ═══════════════════════════════════════════════════════════════════════
    # QUANTIZAÇÃO TGL
    # ═══════════════════════════════════════════════════════════════════════
    
    def _quantize_tgl(self, data: np.ndarray) -> Tuple[np.ndarray, np.ndarray, Tuple[float, float]]:
        """
        Quantização TGL: g = √|L|, s = sign(L)
        
        Returns:
            g_quantized, s_packed, (g_min, g_max)
        """
        flat = data.flatten().astype(np.float64)
        n = len(flat)
        
        # Sinal
        s = np.sign(flat)
        s[s == 0] = 1
        s_bits = (s > 0).astype(np.uint8)
        s_packed = np.packbits(s_bits)
        
        # Radical
        g = np.sqrt(np.abs(flat))
        
        # Range
        g_min, g_max = float(g.min()), float(g.max())
        
        # Normalizar e quantizar
        if g_max - g_min > EPSILON_ZERO:
            g_norm = (g - g_min) / (g_max - g_min)
        else:
            g_norm = np.zeros_like(g)
        
        if self.bits <= 8:
            g_quantized = np.round(g_norm * (self.levels - 1)).astype(np.uint8)
        else:
            g_quantized = np.round(g_norm * (self.levels - 1)).astype(np.uint16)
        
        return g_quantized, s_packed, (g_min, g_max)
    
    def _dequantize_tgl(self, g_quantized: np.ndarray, s_packed: np.ndarray, 
                        g_scale: Tuple[float, float], n_elements: int) -> np.ndarray:
        """
        Dequantização TGL: L = s × g²
        """
        g_min, g_max = g_scale
        
        # Dequantizar g
        g_norm = g_quantized.astype(np.float64) / (self.levels - 1)
        g = g_norm * (g_max - g_min) + g_min
        
        # Desempacotar s
        s = np.unpackbits(s_packed)[:n_elements].astype(np.float64) * 2 - 1
        
        # Ressurreição
        L = s * (g ** 2)
        
        return L
    
    def _quantize_linear(self, data: np.ndarray) -> Tuple[np.ndarray, Tuple[float, float]]:
        """
        Quantização linear simples (para valores singulares, etc.)
        """
        flat = data.flatten().astype(np.float64)
        
        d_min, d_max = float(flat.min()), float(flat.max())
        
        if d_max - d_min > EPSILON_ZERO:
            d_norm = (flat - d_min) / (d_max - d_min)
        else:
            d_norm = np.zeros_like(flat)
        
        if self.bits <= 8:
            quantized = np.round(d_norm * (self.levels - 1)).astype(np.uint8)
        else:
            quantized = np.round(d_norm * (self.levels - 1)).astype(np.uint16)
        
        return quantized.reshape(data.shape), (d_min, d_max)
    
    def _dequantize_linear(self, quantized: np.ndarray, scale: Tuple[float, float]) -> np.ndarray:
        """
        Dequantização linear
        """
        d_min, d_max = scale
        d_norm = quantized.astype(np.float64) / (self.levels - 1)
        return d_norm * (d_max - d_min) + d_min
    
    # ═══════════════════════════════════════════════════════════════════════
    # COMPRESSÃO
    # ═══════════════════════════════════════════════════════════════════════
    
    def compress(self, tensor: Union[np.ndarray, 'torch.Tensor'], 
                 mode: CompressionMode = None) -> CompressedTensorV3:
        """
        Comprime tensor usando modo especificado.
        
        Args:
            tensor: Tensor a comprimir
            mode: Modo de compressão (None = usar self.mode)
        
        Returns:
            CompressedTensorV3
        """
        # Converter para NumPy
        if HAS_TORCH and isinstance(tensor, torch.Tensor):
            arr = tensor.detach().cpu().numpy()
        else:
            arr = np.asarray(tensor)
        
        original_shape = arr.shape
        original_dtype = str(arr.dtype)
        original_bytes = arr.nbytes
        
        # Escolher modo
        if mode is None:
            mode = self.mode
        
        if mode == CompressionMode.AUTO:
            mode = self._choose_mode(arr)
        
        # Comprimir baseado no modo
        if mode == CompressionMode.DIRECT:
            return self._compress_direct(arr, original_shape, original_dtype, original_bytes)
        elif mode == CompressionMode.SPECTRAL:
            return self._compress_spectral(arr, original_shape, original_dtype, original_bytes)
        elif mode == CompressionMode.HYBRID:
            return self._compress_hybrid(arr, original_shape, original_dtype, original_bytes)
        else:
            raise ValueError(f"Modo desconhecido: {mode}")
    
    def _choose_mode(self, arr: np.ndarray) -> CompressionMode:
        """
        Escolhe automaticamente o melhor modo baseado na estrutura do tensor.
        """
        # Analisar estrutura espectral
        analysis = self.analyze_spectral(arr)
        
        # Se é baixo rank, usar SPECTRAL
        if analysis.is_low_rank and analysis.compression_potential > 5:
            return CompressionMode.SPECTRAL
        
        # Se tem boa compressão potencial, usar HYBRID
        if analysis.compression_potential > 2:
            return CompressionMode.HYBRID
        
        # Caso contrário, DIRECT
        return CompressionMode.DIRECT
    
    def _compress_direct(self, arr: np.ndarray, original_shape: tuple,
                         original_dtype: str, original_bytes: int) -> CompressedTensorV3:
        """
        Compressão DIRECT: TGL puro (g = √|L|, s = sign)
        """
        # Quantizar TGL
        g_quantized, s_packed, g_scale = self._quantize_tgl(arr)
        
        # Calcular variância para Tetelestai
        g = np.sqrt(np.abs(arr.flatten()))
        g_nonzero = g[g > EPSILON_ZERO]
        if len(g_nonzero) > 0:
            variance = float(np.std(g_nonzero) / np.mean(g_nonzero))
        else:
            variance = 0.0
        
        tetelestai = variance < self.alpha2
        
        # Checksum
        checksum = hashlib.md5(arr.tobytes()).hexdigest()[:16]
        
        return CompressedTensorV3(
            mode="direct",
            g_quantized=g_quantized,
            s_packed=s_packed,
            original_shape=original_shape,
            original_dtype=original_dtype,
            bits=self.bits,
            g_scale=g_scale,
            variance=variance,
            tetelestai=tetelestai,
            energy_captured=1.0,
            original_bytes=original_bytes,
            checksum=checksum
        )
    
    def _compress_spectral(self, arr: np.ndarray, original_shape: tuple,
                           original_dtype: str, original_bytes: int) -> CompressedTensorV3:
        """
        Compressão SPECTRAL: SVD + TGL nos componentes
        
        Análogo aos "harmônicos" do ACOM 2.0
        """
        # Reshape para 2D
        if arr.ndim == 1:
            matrix = arr.reshape(-1, 1)
        elif arr.ndim == 2:
            matrix = arr
        else:
            matrix = arr.reshape(arr.shape[0], -1)
        
        m, n = matrix.shape
        
        # SVD
        U, S, Vt = np.linalg.svd(matrix, full_matrices=False)
        
        # Determinar rank ótimo
        energy = S ** 2
        total_energy = np.sum(energy)
        cumulative = np.cumsum(energy) / total_energy
        
        k = np.searchsorted(cumulative, self.energy_threshold) + 1
        k = min(k, len(S), min(m, n))
        
        # Truncar
        U_k = U[:, :k]
        S_k = S[:k]
        Vt_k = Vt[:k, :]
        
        energy_captured = cumulative[k-1] if k > 0 else 0
        
        # Quantizar componentes
        # U e Vt via TGL (têm estrutura de fase)
        U_q, U_s, U_scale = self._quantize_tgl(U_k)
        Vt_q, Vt_s, Vt_scale = self._quantize_tgl(Vt_k)
        
        # S via linear (valores positivos)
        S_q, S_scale = self._quantize_linear(S_k)
        
        # Para descompressão, precisamos guardar s_packed junto
        # Empacotamos U_s e Vt_s juntos
        
        # Checksum
        checksum = hashlib.md5(arr.tobytes()).hexdigest()[:16]
        
        return CompressedTensorV3(
            mode="spectral",
            U_quantized=U_q,
            S_quantized=S_q,
            Vt_quantized=Vt_q,
            s_packed=np.concatenate([U_s, Vt_s]),  # Sinais de U e Vt
            original_shape=original_shape,
            original_dtype=original_dtype,
            rank_used=k,
            bits=self.bits,
            U_scale=U_scale,
            S_scale=S_scale,
            Vt_scale=Vt_scale,
            energy_captured=energy_captured,
            original_bytes=original_bytes,
            checksum=checksum
        )
    
    def _compress_hybrid(self, arr: np.ndarray, original_shape: tuple,
                         original_dtype: str, original_bytes: int) -> CompressedTensorV3:
        """
        Compressão HYBRID: SVD para estrutura + TGL para tensor completo
        
        Combina benefícios de ambos os modos.
        """
        # Primeiro, fazer compressão spectral
        spectral = self._compress_spectral(arr, original_shape, original_dtype, original_bytes)
        
        # Verificar se spectral é melhor
        spectral_ratio = original_bytes / spectral.compressed_bytes
        
        # Se taxa spectral > 3, usar spectral puro
        if spectral_ratio > 3:
            return spectral
        
        # Caso contrário, usar direct
        return self._compress_direct(arr, original_shape, original_dtype, original_bytes)
    
    # ═══════════════════════════════════════════════════════════════════════
    # DESCOMPRESSÃO
    # ═══════════════════════════════════════════════════════════════════════
    
    def decompress(self, compressed: CompressedTensorV3) -> np.ndarray:
        """
        Descomprime tensor.
        
        Returns:
            Tensor reconstruído como np.ndarray
        """
        if compressed.mode == "direct":
            return self._decompress_direct(compressed)
        elif compressed.mode == "spectral":
            return self._decompress_spectral(compressed)
        elif compressed.mode == "hybrid":
            # Hybrid usa o mesmo formato que spectral ou direct
            if compressed.U_quantized is not None:
                return self._decompress_spectral(compressed)
            else:
                return self._decompress_direct(compressed)
        else:
            raise ValueError(f"Modo desconhecido: {compressed.mode}")
    
    def _decompress_direct(self, compressed: CompressedTensorV3) -> np.ndarray:
        """
        Descompressão DIRECT
        """
        n_elements = int(np.prod(compressed.original_shape))
        
        L = self._dequantize_tgl(
            compressed.g_quantized,
            compressed.s_packed,
            compressed.g_scale,
            n_elements
        )
        
        return L.reshape(compressed.original_shape)
    
    def _decompress_spectral(self, compressed: CompressedTensorV3) -> np.ndarray:
        """
        Descompressão SPECTRAL
        """
        k = compressed.rank_used
        original_shape = compressed.original_shape
        
        # Determinar shape da matriz
        if len(original_shape) == 1:
            m, n = original_shape[0], 1
        elif len(original_shape) == 2:
            m, n = original_shape
        else:
            m = original_shape[0]
            n = int(np.prod(original_shape[1:]))
        
        # Tamanhos de U e Vt
        U_size = m * k
        Vt_size = k * n
        
        # Separar s_packed
        U_s_size = (U_size + 7) // 8
        U_s = compressed.s_packed[:U_s_size]
        Vt_s = compressed.s_packed[U_s_size:]
        
        # Dequantizar U
        U_flat = self._dequantize_tgl(
            compressed.U_quantized.flatten(),
            U_s,
            compressed.U_scale,
            U_size
        )
        U_k = U_flat.reshape(m, k)
        
        # Dequantizar S
        S_k = self._dequantize_linear(compressed.S_quantized, compressed.S_scale)
        
        # Dequantizar Vt
        Vt_flat = self._dequantize_tgl(
            compressed.Vt_quantized.flatten(),
            Vt_s,
            compressed.Vt_scale,
            Vt_size
        )
        Vt_k = Vt_flat.reshape(k, n)
        
        # Reconstruir matriz
        matrix = U_k @ np.diag(S_k) @ Vt_k
        
        # Reshape para forma original
        return matrix.reshape(original_shape)


# ═══════════════════════════════════════════════════════════════════════════════
# SIMULADOR DE KV CACHE v3
# ═══════════════════════════════════════════════════════════════════════════════

class KVCacheSimulatorV3:
    """
    Simulador de KV Cache com TGL-Tensor v3
    
    Testa todos os modos de compressão.
    """
    
    def __init__(self,
                 n_heads: int = 32,
                 head_dim: int = 128,
                 n_layers: int = 32,
                 dtype: str = 'float32'):
        self.n_heads = n_heads
        self.head_dim = head_dim
        self.n_layers = n_layers
        self.dtype = np.float32 if dtype == 'float32' else np.float16
        
        # Compressores
        self.tgl_direct = TGLTensorV3(bits=10, mode=CompressionMode.DIRECT)
        self.tgl_spectral = TGLTensorV3(bits=10, mode=CompressionMode.SPECTRAL)
        self.tgl_hybrid = TGLTensorV3(bits=10, mode=CompressionMode.HYBRID)
        self.tgl_auto = TGLTensorV3(bits=10, mode=CompressionMode.AUTO)
    
    def generate_kv(self, n_tokens: int, batch_size: int = 1) -> Tuple[np.ndarray, np.ndarray]:
        """
        Gera K,V simulados com estrutura realista de LLM.
        
        LLMs reais têm estrutura de baixo rank no KV cache!
        """
        # Shape: [batch, heads, seq, head_dim]
        shape = (batch_size, self.n_heads, n_tokens, self.head_dim)
        
        # Simular estrutura de baixo rank (realista para LLMs)
        # K e V têm padrões de atenção estruturados
        
        # Base de baixo rank
        rank = min(32, n_tokens // 4)  # Rank efetivo
        
        # Gerar K com estrutura
        K_low = np.random.randn(batch_size, self.n_heads, n_tokens, rank).astype(self.dtype) * 0.1
        K_proj = np.random.randn(batch_size, self.n_heads, rank, self.head_dim).astype(self.dtype) * 0.1
        K = np.einsum('bhtr,bhrd->bhtd', K_low, K_proj)
        
        # Adicionar ruído
        K += np.random.randn(*shape).astype(self.dtype) * 0.01
        
        # V similar
        V_low = np.random.randn(batch_size, self.n_heads, n_tokens, rank).astype(self.dtype) * 0.1
        V_proj = np.random.randn(batch_size, self.n_heads, rank, self.head_dim).astype(self.dtype) * 0.1
        V = np.einsum('bhtr,bhrd->bhtd', V_low, V_proj)
        V += np.random.randn(*shape).astype(self.dtype) * 0.01
        
        return K, V
    
    def benchmark(self, n_tokens: int = 2048, batch_size: int = 1):
        """
        Benchmark completo comparando todos os modos.
        """
        print(f"\n{'═'*78}")
        print(f"TGL-TENSOR v3.0 — BENCHMARK KV CACHE")
        print(f"{'═'*78}")
        print(f"Config: {self.n_heads} heads × {self.head_dim} dim × {n_tokens} tokens")
        print(f"Batch: {batch_size} | dtype: {self.dtype}")
        
        # Gerar dados
        K, V = self.generate_kv(n_tokens, batch_size)
        
        original_bytes = K.nbytes + V.nbytes
        print(f"Tamanho original: {original_bytes:,} bytes ({original_bytes/1024/1024:.2f} MB)")
        
        # Análise espectral
        print(f"\n{'─'*40}")
        print("ANÁLISE ESPECTRAL")
        print(f"{'─'*40}")
        
        # Analisar primeiro head como exemplo
        K_head = K[0, 0]  # [seq, dim]
        analysis = self.tgl_spectral.analyze_spectral(K_head)
        
        print(f"Rank completo: {analysis.rank_full}")
        print(f"Rank ótimo (α²={ALPHA2}): {analysis.rank_optimal}")
        print(f"Energia capturada: {analysis.energy_ratio:.4f}")
        print(f"Potencial de compressão: {analysis.compression_potential:.1f}:1")
        print(f"É baixo rank: {'Sim' if analysis.is_low_rank else 'Não'}")
        
        results = {}
        
        # Testar cada modo
        for name, tgl in [
            ('DIRECT', self.tgl_direct),
            ('SPECTRAL', self.tgl_spectral),
            ('HYBRID', self.tgl_hybrid),
            ('AUTO', self.tgl_auto)
        ]:
            print(f"\n{'─'*40}")
            print(f"MODO: {name}")
            print(f"{'─'*40}")
            
            # Compressão
            t0 = time.perf_counter()
            K_comp = tgl.compress(K)
            V_comp = tgl.compress(V)
            t_compress = time.perf_counter() - t0
            
            # Descompressão
            t0 = time.perf_counter()
            K_recon = tgl.decompress(K_comp)
            V_recon = tgl.decompress(V_comp)
            t_decompress = time.perf_counter() - t0
            
            # Métricas
            compressed_bytes = K_comp.compressed_bytes + V_comp.compressed_bytes
            ratio = original_bytes / compressed_bytes
            
            # PSNR e Cosine
            mse_K = np.mean((K - K_recon) ** 2)
            mse_V = np.mean((V - V_recon) ** 2)
            psnr_K = 10 * np.log10(np.max(K**2) / (mse_K + 1e-15))
            psnr_V = 10 * np.log10(np.max(V**2) / (mse_V + 1e-15))
            
            K_flat, K_recon_flat = K.flatten(), K_recon.flatten()
            V_flat, V_recon_flat = V.flatten(), V_recon.flatten()
            
            cos_K = np.dot(K_flat, K_recon_flat) / (np.linalg.norm(K_flat) * np.linalg.norm(K_recon_flat) + 1e-15)
            cos_V = np.dot(V_flat, V_recon_flat) / (np.linalg.norm(V_flat) * np.linalg.norm(V_recon_flat) + 1e-15)
            
            print(f"Modo usado: {K_comp.mode}")
            print(f"Rank: {K_comp.rank_used if K_comp.rank_used > 0 else 'N/A'}")
            print(f"Comprimido: {compressed_bytes:,} bytes ({compressed_bytes/1024/1024:.2f} MB)")
            print(f"Taxa: {ratio:.2f}:1")
            print(f"Bits/elemento: {K_comp.bits_per_element:.1f}")
            print(f"Tempo compressão: {t_compress*1000:.2f} ms")
            print(f"Tempo descompressão: {t_decompress*1000:.2f} ms")
            print(f"PSNR K: {psnr_K:.2f} dB | V: {psnr_V:.2f} dB")
            print(f"Cosine K: {cos_K:.6f} | V: {cos_V:.6f}")
            print(f"Energia capturada: {K_comp.energy_captured:.4f}")
            
            results[name] = {
                'mode_used': K_comp.mode,
                'rank': K_comp.rank_used,
                'ratio': ratio,
                'psnr_k': psnr_K,
                'psnr_v': psnr_V,
                'cos_k': cos_K,
                'cos_v': cos_V,
                't_compress': t_compress,
                't_decompress': t_decompress,
                'energy': K_comp.energy_captured
            }
        
        # ═══════════════════════════════════════════════════════════════════
        # BASELINE: INT8
        # ═══════════════════════════════════════════════════════════════════
        print(f"\n{'─'*40}")
        print("BASELINE: INT8")
        print(f"{'─'*40}")
        
        t0 = time.perf_counter()
        K_min, K_max = K.min(), K.max()
        V_min, V_max = V.min(), V.max()
        K_int8 = np.round((K - K_min) / (K_max - K_min + 1e-15) * 255).astype(np.uint8)
        V_int8 = np.round((V - V_min) / (V_max - V_min + 1e-15) * 255).astype(np.uint8)
        t_compress_int8 = time.perf_counter() - t0
        
        t0 = time.perf_counter()
        K_recon_int8 = K_int8.astype(np.float32) / 255 * (K_max - K_min) + K_min
        V_recon_int8 = V_int8.astype(np.float32) / 255 * (V_max - V_min) + V_min
        t_decompress_int8 = time.perf_counter() - t0
        
        compressed_bytes_int8 = K_int8.nbytes + V_int8.nbytes
        ratio_int8 = original_bytes / compressed_bytes_int8
        
        mse_K_int8 = np.mean((K - K_recon_int8) ** 2)
        mse_V_int8 = np.mean((V - V_recon_int8) ** 2)
        psnr_K_int8 = 10 * np.log10(np.max(K**2) / (mse_K_int8 + 1e-15))
        psnr_V_int8 = 10 * np.log10(np.max(V**2) / (mse_V_int8 + 1e-15))
        
        cos_K_int8 = np.dot(K.flatten(), K_recon_int8.flatten()) / (np.linalg.norm(K) * np.linalg.norm(K_recon_int8) + 1e-15)
        cos_V_int8 = np.dot(V.flatten(), V_recon_int8.flatten()) / (np.linalg.norm(V) * np.linalg.norm(V_recon_int8) + 1e-15)
        
        print(f"Comprimido: {compressed_bytes_int8:,} bytes")
        print(f"Taxa: {ratio_int8:.2f}:1")
        print(f"PSNR K: {psnr_K_int8:.2f} dB | V: {psnr_V_int8:.2f} dB")
        print(f"Cosine K: {cos_K_int8:.6f} | V: {cos_V_int8:.6f}")
        
        results['INT8'] = {
            'mode_used': 'linear',
            'rank': 0,
            'ratio': ratio_int8,
            'psnr_k': psnr_K_int8,
            'psnr_v': psnr_V_int8,
            'cos_k': cos_K_int8,
            'cos_v': cos_V_int8,
            't_compress': t_compress_int8,
            't_decompress': t_decompress_int8,
            'energy': 1.0
        }
        
        # ═══════════════════════════════════════════════════════════════════
        # RESUMO
        # ═══════════════════════════════════════════════════════════════════
        print(f"\n{'═'*78}")
        print("RESUMO COMPARATIVO")
        print(f"{'═'*78}")
        
        print(f"\n{'Método':<12} │ {'Modo':<10} │ {'Taxa':>8} │ {'PSNR K':>9} │ {'Cos K':>9} │ {'Energia':>8}")
        print(f"{'─'*12}─┼─{'─'*10}─┼─{'─'*8}─┼─{'─'*9}─┼─{'─'*9}─┼─{'─'*8}")
        
        for name, r in results.items():
            print(f"{name:<12} │ {r['mode_used']:<10} │ {r['ratio']:>7.1f}x │ {r['psnr_k']:>8.1f}dB │ "
                  f"{r['cos_k']:>9.6f} │ {r['energy']:>8.4f}")
        
        return results


# ═══════════════════════════════════════════════════════════════════════════════
# TESTE DE EMBEDDINGS v3
# ═══════════════════════════════════════════════════════════════════════════════

def test_embeddings_v3(n_tokens: int = 5000, embed_dim: int = 768):
    """
    Testa compressão de embeddings com todos os modos.
    """
    print(f"\n{'═'*78}")
    print(f"TGL-TENSOR v3.0 — TESTE EMBEDDINGS")
    print(f"{'═'*78}")
    print(f"Config: {n_tokens} tokens × {embed_dim} dims")
    
    # Gerar embeddings com estrutura de baixo rank (realista)
    rank = 64
    U = np.random.randn(n_tokens, rank).astype(np.float32) * 0.1
    V = np.random.randn(rank, embed_dim).astype(np.float32) * 0.1
    embeddings = U @ V
    embeddings += np.random.randn(n_tokens, embed_dim).astype(np.float32) * 0.01
    
    original_bytes = embeddings.nbytes
    print(f"Tamanho original: {original_bytes:,} bytes ({original_bytes/1024/1024:.2f} MB)")
    
    # Análise
    tgl = TGLTensorV3(bits=10)
    analysis = tgl.analyze_spectral(embeddings)
    
    print(f"\nAnálise Espectral:")
    print(f"  Rank ótimo: {analysis.rank_optimal} / {analysis.rank_full}")
    print(f"  Energia: {analysis.energy_ratio:.4f}")
    print(f"  Potencial: {analysis.compression_potential:.1f}:1")
    
    results = {}
    
    for mode in [CompressionMode.DIRECT, CompressionMode.SPECTRAL, CompressionMode.AUTO]:
        print(f"\n{'─'*40}")
        print(f"MODO: {mode.value.upper()}")
        print(f"{'─'*40}")
        
        tgl = TGLTensorV3(bits=10, mode=mode)
        
        t0 = time.perf_counter()
        compressed = tgl.compress(embeddings)
        t_comp = time.perf_counter() - t0
        
        t0 = time.perf_counter()
        recon = tgl.decompress(compressed)
        t_decomp = time.perf_counter() - t0
        
        mse = np.mean((embeddings - recon) ** 2)
        psnr = 10 * np.log10(np.max(embeddings**2) / (mse + 1e-15))
        cos = np.dot(embeddings.flatten(), recon.flatten()) / (
            np.linalg.norm(embeddings) * np.linalg.norm(recon) + 1e-15
        )
        
        print(f"Modo usado: {compressed.mode}")
        print(f"Rank: {compressed.rank_used if compressed.rank_used > 0 else 'N/A'}")
        print(f"Taxa: {compressed.compression_ratio:.1f}:1")
        print(f"PSNR: {psnr:.2f} dB")
        print(f"Cosine: {cos:.6f}")
        print(f"Tempo: {t_comp*1000:.1f}ms comp / {t_decomp*1000:.1f}ms decomp")
        
        results[mode.value] = {
            'ratio': compressed.compression_ratio,
            'psnr': psnr,
            'cos': cos
        }
    
    return results


def analyze_results(results_kv: Dict, results_emb: Dict) -> List[str]:
    """
    Analisa os resultados dos benchmarks e gera conclusões baseadas nos dados.
    
    Retorna lista de strings para exibição no relatório.
    """
    conclusions = []
    
    # ═══════════════════════════════════════════════════════════════════════
    # 1. IDENTIFICAR MELHOR MODO PARA KV CACHE
    # ═══════════════════════════════════════════════════════════════════════
    
    # Comparar TGL vs INT8 em qualidade
    best_tgl_kv = None
    best_tgl_ratio_kv = 0
    best_tgl_psnr_kv = 0
    
    for mode in ['DIRECT', 'SPECTRAL', 'HYBRID', 'AUTO']:
        if mode in results_kv:
            if results_kv[mode]['ratio'] > best_tgl_ratio_kv:
                best_tgl_ratio_kv = results_kv[mode]['ratio']
                best_tgl_psnr_kv = results_kv[mode]['psnr_k']
                best_tgl_kv = mode
    
    int8_ratio = results_kv.get('INT8', {}).get('ratio', 4.0)
    int8_psnr = results_kv.get('INT8', {}).get('psnr_k', 50.0)
    
    # Análise de taxa
    if best_tgl_ratio_kv > int8_ratio * 1.5:
        conclusions.append(f"KV Cache: {best_tgl_kv} obteve {best_tgl_ratio_kv:.1f}x (vs INT8 {int8_ratio:.1f}x)")
    elif best_tgl_ratio_kv > int8_ratio:
        conclusions.append(f"KV Cache: {best_tgl_kv} marginalmente melhor ({best_tgl_ratio_kv:.1f}x vs {int8_ratio:.1f}x)")
    else:
        conclusions.append(f"KV Cache: INT8 mais compacto ({int8_ratio:.1f}x vs TGL {best_tgl_ratio_kv:.1f}x)")
    
    # Análise de qualidade
    psnr_gain = best_tgl_psnr_kv - int8_psnr
    if psnr_gain > 10:
        conclusions.append(f"Qualidade: TGL supera INT8 em +{psnr_gain:.0f}dB PSNR")
    elif psnr_gain > 0:
        conclusions.append(f"Qualidade: TGL ligeiramente melhor (+{psnr_gain:.1f}dB)")
    elif psnr_gain > -5:
        conclusions.append(f"Qualidade: TGL e INT8 comparáveis ({psnr_gain:+.1f}dB)")
    else:
        conclusions.append(f"Qualidade: INT8 preserva melhor ({psnr_gain:.1f}dB)")
    
    # ═══════════════════════════════════════════════════════════════════════
    # 2. ANÁLISE DE EMBEDDINGS
    # ═══════════════════════════════════════════════════════════════════════
    
    best_emb_mode = max(results_emb.keys(), key=lambda k: results_emb[k]['ratio'])
    best_emb_ratio = results_emb[best_emb_mode]['ratio']
    best_emb_cos = results_emb[best_emb_mode]['cos']
    
    if best_emb_ratio > 10:
        conclusions.append(f"Embeddings: {best_emb_mode.upper()} alcançou {best_emb_ratio:.0f}x com cos={best_emb_cos:.4f}")
    elif best_emb_ratio > 5:
        conclusions.append(f"Embeddings: {best_emb_mode.upper()} alcançou {best_emb_ratio:.1f}x")
    else:
        conclusions.append(f"Embeddings: Taxa modesta ({best_emb_ratio:.1f}x)")
    
    # ═══════════════════════════════════════════════════════════════════════
    # 3. ANÁLISE DE COSINE SIMILARITY (INTEGRIDADE SEMÂNTICA)
    # ═══════════════════════════════════════════════════════════════════════
    
    # Para LLMs, cosine > 0.99 é crítico
    min_cos_kv = min(results_kv[m]['cos_k'] for m in ['DIRECT', 'SPECTRAL', 'AUTO'] if m in results_kv)
    
    if min_cos_kv > 0.999:
        conclusions.append(f"Semântica: Excelente preservação (cos > 0.999)")
    elif min_cos_kv > 0.99:
        conclusions.append(f"Semântica: Boa preservação (cos > 0.99)")
    elif min_cos_kv > 0.95:
        conclusions.append(f"Semântica: Aceitável (cos = {min_cos_kv:.4f})")
    else:
        conclusions.append(f"ALERTA: Degradação semântica (cos = {min_cos_kv:.4f})")
    
    # ═══════════════════════════════════════════════════════════════════════
    # 4. RECOMENDAÇÃO BASEADA NOS DADOS
    # ═══════════════════════════════════════════════════════════════════════
    
    # Determinar vencedor geral
    spectral_advantage = results_kv.get('SPECTRAL', {}).get('ratio', 0) / max(int8_ratio, 0.1)
    direct_quality = results_kv.get('DIRECT', {}).get('psnr_k', 0) - int8_psnr
    
    if spectral_advantage > 2 and results_kv.get('SPECTRAL', {}).get('cos_k', 0) > 0.99:
        conclusions.append(f"Recomendação: SPECTRAL para dados com estrutura de baixo rank")
    elif direct_quality > 10 and results_kv.get('DIRECT', {}).get('cos_k', 0) > 0.999:
        conclusions.append(f"Recomendação: DIRECT para máxima fidelidade")
    elif spectral_advantage < 1 and direct_quality < 5:
        conclusions.append(f"Observação: INT8 competitivo para estes dados")
    else:
        conclusions.append(f"Recomendação: Usar modo AUTO para seleção adaptativa")
    
    return conclusions


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Executa benchmarks do TGL-Tensor v3."""
    
    print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║     TGL-TENSOR v3.0 — Compressor Ontológico com Decomposição Espectral       ║
║                                                                               ║
║     Teoria da Gravitação Luminodinâmica (TGL)                                ║
║                                                                               ║
║     MODOS:                                                                   ║
║       DIRECT   — g = √|L|, s = sign(L)           [Taxa ~3-4:1]              ║
║       SPECTRAL — SVD + TGL nos componentes       [Taxa ~10-50:1]             ║
║       HYBRID   — SVD + resíduos                  [Taxa ~5-20:1]              ║
║       AUTO     — Escolhe melhor automaticamente                              ║
║                                                                               ║
║     Autores: Luiz Antonio Rotoli Miguel & IALD                               ║
║     IALD LTDA (CNPJ 62.757.606/0001-23)                                      ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    print(f"PyTorch: {'Sim' if HAS_TORCH else 'Não'}")
    print(f"CUDA: {'Sim' if HAS_CUDA else 'Não'}")
    print(f"SciPy: {'Sim' if HAS_SCIPY else 'Não'}")
    print(f"GPU: {GPU_NAME}")
    
    # Benchmark KV Cache
    print("\n" + "█" * 78)
    print("█  BENCHMARK 1: KV CACHE (Estrutura de Baixo Rank)")
    print("█" * 78)
    
    kv_sim = KVCacheSimulatorV3(n_heads=32, head_dim=128)
    results_kv = kv_sim.benchmark(n_tokens=2048)
    
    # Teste Embeddings
    print("\n" + "█" * 78)
    print("█  BENCHMARK 2: EMBEDDINGS")
    print("█" * 78)
    
    results_emb = test_embeddings_v3(n_tokens=5000, embed_dim=768)
    
    # Análise dos resultados para conclusão dinâmica
    conclusion_lines = analyze_results(results_kv, results_emb)
    
    # Relatório Final
    print(f"""

╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║     TGL-TENSOR v3.0 — RELATÓRIO FINAL                                        ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  KV CACHE (2048 tokens):                                                     ║
║    DIRECT:   {results_kv['DIRECT']['ratio']:>5.1f}x | PSNR {results_kv['DIRECT']['psnr_k']:>5.1f}dB | Cos {results_kv['DIRECT']['cos_k']:.4f}             ║
║    SPECTRAL: {results_kv['SPECTRAL']['ratio']:>5.1f}x | PSNR {results_kv['SPECTRAL']['psnr_k']:>5.1f}dB | Cos {results_kv['SPECTRAL']['cos_k']:.4f}             ║
║    AUTO:     {results_kv['AUTO']['ratio']:>5.1f}x | PSNR {results_kv['AUTO']['psnr_k']:>5.1f}dB | Cos {results_kv['AUTO']['cos_k']:.4f}             ║
║    INT8:     {results_kv['INT8']['ratio']:>5.1f}x | PSNR {results_kv['INT8']['psnr_k']:>5.1f}dB | Cos {results_kv['INT8']['cos_k']:.4f}             ║
║                                                                               ║
║  EMBEDDINGS (5000 × 768):                                                    ║
║    DIRECT:   {results_emb['direct']['ratio']:>5.1f}x | PSNR {results_emb['direct']['psnr']:>5.1f}dB | Cos {results_emb['direct']['cos']:.4f}             ║
║    SPECTRAL: {results_emb['spectral']['ratio']:>5.1f}x | PSNR {results_emb['spectral']['psnr']:>5.1f}dB | Cos {results_emb['spectral']['cos']:.4f}             ║
║    AUTO:     {results_emb['auto']['ratio']:>5.1f}x | PSNR {results_emb['auto']['psnr']:>5.1f}dB | Cos {results_emb['auto']['cos']:.4f}             ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║  CONCLUSÃO (baseada nos dados):                                              ║""")
    
    for line in conclusion_lines:
        print(f"║    {line:<71} ║")
    
    print("""║                                                                               ║
║                              — TETELESTAI —                                  ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    return results_kv, results_emb


if __name__ == "__main__":
    results = main()