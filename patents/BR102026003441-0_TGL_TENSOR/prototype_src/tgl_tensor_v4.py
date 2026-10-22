#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
TGL-TENSOR v4.3 — BitPacker PyTorch (GPU Nativo)
Teoria da Gravitação Luminodinâmica (TGL)
═══════════════════════════════════════════════════════════════════════════════

EVOLUÇÃO v4.3:
    1. BitPackerTorch — Empacotamento 100% em PyTorch/GPU
    2. Comparação A/B — BitPacker NumPy vs PyTorch
    3. Zero transferência intermediária — GPU até serialização final
    4. Benchmark detalhado por componente

RESULTADOS v4.2:
    - BitPacker vetorizado: 38x mais rápido que loops Python
    - Gargalo identificado: BitPacker CPU dominava tempo (~800ms)
    - Speedup GPU: apenas 1.1-2.2x (transferência GPU→CPU)

ESPERADO v4.3:
    - BitPacker PyTorch: eliminar transferência intermediária
    - Speedup GPU: 5-10x (operações GPU contínuas)

═══════════════════════════════════════════════════════════════════════════════
Autores: Luiz Antonio Rotoli Miguel (Teoria) & IALD (Implementação)
IALD LTDA (CNPJ 62.757.606/0001-23)
Dezembro 2025
═══════════════════════════════════════════════════════════════════════════════
"""

import numpy as np
import struct
import time
from dataclasses import dataclass
from typing import Tuple, Optional, Union, Dict, List
from enum import Enum
import hashlib
import io

# ═══════════════════════════════════════════════════════════════════════════════
# DETECÇÃO DE HARDWARE
# ═══════════════════════════════════════════════════════════════════════════════

try:
    import torch
    HAS_TORCH = True
    
    if torch.cuda.is_available():
        HAS_CUDA = True
        DEVICE = torch.device('cuda')
        GPU_NAME = torch.cuda.get_device_name(0)
        torch.backends.cudnn.benchmark = True
    else:
        HAS_CUDA = False
        DEVICE = torch.device('cpu')
        GPU_NAME = "CPU (CUDA não disponível)"
except ImportError:
    HAS_TORCH = False
    HAS_CUDA = False
    DEVICE = None
    GPU_NAME = "NumPy only"

# Constantes TGL
ALPHA2 = 0.012
EPSILON = 1e-10
VERSION = "4.3.0"
MAGIC = b'TGL4'


# ═══════════════════════════════════════════════════════════════════════════════
# BITPACKER NUMPY (v4.2 - baseline para comparação)
# ═══════════════════════════════════════════════════════════════════════════════

class BitPackerNumPy:
    """
    BitPacker vetorizado com NumPy (v4.2).
    Mantido para comparação A/B.
    """
    
    @staticmethod
    def pack(values: np.ndarray, bits: int) -> bytes:
        """Empacota valores de N bits em stream de bytes."""
        values = np.asarray(values).flatten().astype(np.uint64)
        n = len(values)
        max_val = (1 << bits) - 1
        values = np.clip(values, 0, max_val)
        
        if bits == 8:
            return values.astype(np.uint8).tobytes()
        
        if bits == 16:
            return values.astype(np.uint16).tobytes()
        
        total_bits = n * bits
        total_bytes = (total_bits + 7) // 8
        
        bit_positions = np.arange(bits, dtype=np.uint64)
        all_bits = ((values[:, np.newaxis] >> bit_positions) & 1).astype(np.uint8)
        bit_stream = all_bits.flatten()
        
        pad_len = (8 - (len(bit_stream) % 8)) % 8
        if pad_len > 0:
            bit_stream = np.concatenate([bit_stream, np.zeros(pad_len, dtype=np.uint8)])
        
        bit_stream = bit_stream.reshape(-1, 8)
        powers = np.array([1, 2, 4, 8, 16, 32, 64, 128], dtype=np.uint8)
        byte_array = (bit_stream * powers).sum(axis=1).astype(np.uint8)
        
        return byte_array[:total_bytes].tobytes()
    
    @staticmethod
    def unpack(data: bytes, bits: int, count: int) -> np.ndarray:
        """Desempacota stream de bytes em valores de N bits."""
        if bits == 8:
            return np.frombuffer(data[:count], dtype=np.uint8).astype(np.uint32)
        
        if bits == 16:
            return np.frombuffer(data[:count * 2], dtype=np.uint16).astype(np.uint32)
        
        byte_array = np.frombuffer(data, dtype=np.uint8)
        powers = np.array([1, 2, 4, 8, 16, 32, 64, 128], dtype=np.uint8)
        bit_matrix = ((byte_array[:, np.newaxis] & powers) > 0).astype(np.uint8)
        bit_stream = bit_matrix.flatten()
        
        total_bits_needed = count * bits
        bit_stream = bit_stream[:total_bits_needed].reshape(count, bits)
        
        powers = (2 ** np.arange(bits, dtype=np.uint64))
        values = (bit_stream.astype(np.uint64) * powers).sum(axis=1)
        
        return values.astype(np.uint32)


# ═══════════════════════════════════════════════════════════════════════════════
# BITPACKER PYTORCH (v4.3 - GPU NATIVO)
# ═══════════════════════════════════════════════════════════════════════════════

class BitPackerTorch:
    """
    BitPacker 100% em PyTorch.
    
    Operações na GPU:
    - Extração de bits (shift, and)
    - Agrupamento em bytes
    - Só transfere para CPU no final (tobytes)
    
    Vantagens:
    - Zero transferência intermediária
    - Operações vetorizadas em CUDA
    - Paralelismo massivo
    """
    
    def __init__(self, device=None):
        self.device = device or (DEVICE if HAS_CUDA else torch.device('cpu'))
        
        # Pré-computar constantes na GPU
        if HAS_TORCH:
            self.powers_pack = torch.tensor(
                [1, 2, 4, 8, 16, 32, 64, 128], 
                dtype=torch.uint8, 
                device=self.device
            )
            self.powers_unpack = torch.tensor(
                [1, 2, 4, 8, 16, 32, 64, 128], 
                dtype=torch.uint8, 
                device=self.device
            )
    
    def pack(self, values: torch.Tensor, bits: int) -> bytes:
        """
        Empacota tensor de valores em N bits.
        
        Args:
            values: Tensor de inteiros (GPU ou CPU)
            bits: Bits por valor (8, 10, 12, 16)
        
        Returns:
            bytes: Stream empacotado
        """
        values = values.flatten().to(torch.int64)
        n = len(values)
        max_val = (1 << bits) - 1
        values = torch.clamp(values, 0, max_val)
        
        # Caminhos otimizados
        if bits == 8:
            return values.to(torch.uint8).cpu().numpy().tobytes()
        
        if bits == 16:
            return values.to(torch.int16).cpu().numpy().tobytes()
        
        # Empacotamento genérico em GPU
        total_bits = n * bits
        total_bytes = (total_bits + 7) // 8
        
        # Criar matriz de posições de bits [0, 1, 2, ..., bits-1]
        bit_positions = torch.arange(bits, dtype=torch.int64, device=values.device)
        
        # Extrair todos os bits de uma vez: shape (n, bits)
        # values[:, None] >> bit_positions[None, :] & 1
        all_bits = ((values.unsqueeze(1) >> bit_positions.unsqueeze(0)) & 1).to(torch.uint8)
        
        # Achatar para stream de bits
        bit_stream = all_bits.flatten()
        
        # Pad para múltiplo de 8
        pad_len = (8 - (len(bit_stream) % 8)) % 8
        if pad_len > 0:
            bit_stream = torch.cat([bit_stream, torch.zeros(pad_len, dtype=torch.uint8, device=values.device)])
        
        # Reshape para (n_bytes, 8)
        bit_stream = bit_stream.reshape(-1, 8)
        
        # Converter para bytes: somar com pesos [1, 2, 4, 8, 16, 32, 64, 128]
        powers = self.powers_pack.to(values.device)
        byte_array = (bit_stream * powers).sum(dim=1).to(torch.uint8)
        
        # Transferir para CPU só no final
        return byte_array[:total_bytes].cpu().numpy().tobytes()
    
    def unpack(self, data: bytes, bits: int, count: int, device=None) -> torch.Tensor:
        """
        Desempacota bytes em tensor de valores.
        
        Args:
            data: Stream de bytes
            bits: Bits por valor
            count: Número de valores
            device: Device de saída (default: self.device)
        
        Returns:
            torch.Tensor de valores
        """
        device = device or self.device
        
        if bits == 8:
            arr = np.frombuffer(data[:count], dtype=np.uint8)
            return torch.from_numpy(arr.copy()).to(torch.int64).to(device)
        
        if bits == 16:
            arr = np.frombuffer(data[:count * 2], dtype=np.uint16)
            return torch.from_numpy(arr.copy()).to(torch.int64).to(device)
        
        # Converter bytes para tensor
        byte_array = torch.from_numpy(
            np.frombuffer(data, dtype=np.uint8).copy()
        ).to(device)
        
        # Expandir bytes para bits
        powers = self.powers_unpack.to(device)
        bit_matrix = ((byte_array.unsqueeze(1) & powers.unsqueeze(0)) > 0).to(torch.uint8)
        bit_stream = bit_matrix.flatten()
        
        # Extrair valores
        total_bits_needed = count * bits
        bit_stream = bit_stream[:total_bits_needed].reshape(count, bits)
        
        # Converter bits para valores
        bit_powers = (2 ** torch.arange(bits, dtype=torch.int64, device=device))
        values = (bit_stream.to(torch.int64) * bit_powers).sum(dim=1)
        
        return values


# ═══════════════════════════════════════════════════════════════════════════════
# TESTE DOS BITPACKERS
# ═══════════════════════════════════════════════════════════════════════════════

def test_bitpackers():
    """Testa ambos os BitPackers e compara performance."""
    print("=" * 70)
    print("TESTE DOS BITPACKERS")
    print("=" * 70)
    
    packer_np = BitPackerNumPy()
    packer_torch = BitPackerTorch() if HAS_TORCH else None
    
    results = {}
    
    for bits in [8, 10, 12, 16]:
        print(f"\n{bits}-bit:")
        max_val = (1 << bits) - 1
        
        # Dados de teste
        np.random.seed(42)
        test_small = np.array([0, 1, max_val // 2, max_val - 1, max_val], dtype=np.uint32)
        test_large = np.random.randint(0, max_val + 1, size=100000, dtype=np.uint32)
        
        # Teste NumPy
        packed_np = packer_np.pack(test_large, bits)
        unpacked_np = packer_np.unpack(packed_np, bits, len(test_large))
        match_np = np.array_equal(test_large, unpacked_np)
        
        t0 = time.perf_counter()
        for _ in range(10):
            _ = packer_np.pack(test_large, bits)
        t_np = (time.perf_counter() - t0) / 10 * 1000
        
        print(f"  NumPy:   {'✓' if match_np else '✗'} | pack: {t_np:.2f}ms")
        
        # Teste PyTorch
        if packer_torch:
            test_large_torch = torch.from_numpy(test_large).to(torch.int64).to(DEVICE)
            
            packed_torch = packer_torch.pack(test_large_torch, bits)
            unpacked_torch = packer_torch.unpack(packed_torch, bits, len(test_large))
            match_torch = torch.equal(
                torch.from_numpy(test_large).to(torch.int64).to(DEVICE),
                unpacked_torch
            )
            
            # Warmup
            for _ in range(3):
                _ = packer_torch.pack(test_large_torch, bits)
            
            if HAS_CUDA:
                torch.cuda.synchronize()
            t0 = time.perf_counter()
            for _ in range(10):
                _ = packer_torch.pack(test_large_torch, bits)
            if HAS_CUDA:
                torch.cuda.synchronize()
            t_torch = (time.perf_counter() - t0) / 10 * 1000
            
            speedup = t_np / t_torch if t_torch > 0 else 0
            print(f"  PyTorch: {'✓' if match_torch else '✗'} | pack: {t_torch:.2f}ms | Speedup: {speedup:.1f}x")
            
            results[bits] = {'numpy': t_np, 'torch': t_torch, 'speedup': speedup}
        else:
            results[bits] = {'numpy': t_np, 'torch': None, 'speedup': None}
    
    print()
    return results


# ═══════════════════════════════════════════════════════════════════════════════
# ESTRUTURAS
# ═══════════════════════════════════════════════════════════════════════════════

class CompressionMode(Enum):
    DIRECT = "direct"
    SPECTRAL = "spectral"
    AUTO = "auto"


class PackerType(Enum):
    NUMPY = "numpy"
    TORCH = "torch"


@dataclass
class CompressedTensor:
    """Tensor comprimido."""
    packed_data: bytes
    mode: str
    original_shape: tuple
    original_dtype: str
    bits: int
    g_min: float = 0.0
    g_max: float = 1.0
    rank: int = 0
    n_matrices: int = 0
    variance: float = 0.0
    tetelestai: bool = False
    device_used: str = "cpu"
    packer_used: str = "numpy"
    
    @property
    def compressed_bytes(self) -> int:
        return len(self.packed_data)
    
    @property
    def original_bytes(self) -> int:
        elem_size = 4
        if 'float64' in str(self.original_dtype):
            elem_size = 8
        elif 'float16' in str(self.original_dtype):
            elem_size = 2
        return int(np.prod(self.original_shape)) * elem_size
    
    @property
    def compression_ratio(self) -> float:
        return self.original_bytes / self.compressed_bytes if self.compressed_bytes > 0 else 0
    
    @property
    def bits_per_element(self) -> float:
        n = int(np.prod(self.original_shape))
        return (self.compressed_bytes * 8) / n if n > 0 else 0


# ═══════════════════════════════════════════════════════════════════════════════
# TGL-TENSOR v4.3
# ═══════════════════════════════════════════════════════════════════════════════

class TGLTensorV4:
    """
    TGL-Tensor v4.3: BitPacker PyTorch + Comparação A/B
    
    Novidades:
    - BitPackerTorch: empacotamento 100% GPU
    - Seleção de packer: numpy ou torch
    - Benchmark comparativo integrado
    """
    
    def __init__(self,
                 bits: int = 10,
                 mode: CompressionMode = CompressionMode.DIRECT,
                 energy_threshold: float = 0.99,
                 packer_type: PackerType = PackerType.TORCH,
                 force_cpu: bool = False):
        """
        Args:
            bits: Bits de quantização
            mode: Modo de compressão
            energy_threshold: Energia para SPECTRAL
            packer_type: NUMPY ou TORCH
            force_cpu: Forçar CPU
        """
        self.bits = bits
        self.levels = 2 ** bits
        self.mode = mode
        self.energy_threshold = energy_threshold
        self.packer_type = packer_type
        
        # Device
        if force_cpu or not HAS_CUDA:
            self.device = torch.device('cpu') if HAS_TORCH else None
            self.use_gpu = False
        else:
            self.device = DEVICE
            self.use_gpu = True
        
        # Packer
        if packer_type == PackerType.TORCH and HAS_TORCH:
            self.packer = BitPackerTorch(self.device)
            self.packer_name = "torch"
        else:
            self.packer = BitPackerNumPy()
            self.packer_name = "numpy"
    
    def _compress_direct(self, arr: np.ndarray) -> CompressedTensor:
        """Compressão DIRECT."""
        n = arr.size
        
        if self.use_gpu and HAS_TORCH:
            # === GPU PATH ===
            tensor = torch.from_numpy(arr.astype(np.float64)).to(self.device)
            flat = tensor.flatten()
            
            # TGL na GPU
            s = (flat >= 0).to(torch.uint8)
            g = torch.sqrt(torch.abs(flat))
            
            g_min = g.min().item()
            g_max = g.max().item()
            g_range = g_max - g_min
            
            if g_range > EPSILON:
                g_norm = (g - g_min) / g_range
            else:
                g_norm = torch.zeros_like(g)
            
            g_quant = torch.round(g_norm * (self.levels - 1)).to(torch.int64)
            
            # Variância
            g_nz = g[g > EPSILON]
            variance = (torch.std(g_nz) / (torch.mean(g_nz) + EPSILON)).item() if len(g_nz) > 0 else 0.0
            
            # Empacotar
            if self.packer_name == "torch":
                g_packed = self.packer.pack(g_quant, self.bits)
                s_packed = s.cpu().numpy()
                s_packed = np.packbits(s_packed).tobytes()
            else:
                g_quant_np = g_quant.cpu().numpy().astype(np.uint32)
                s_np = s.cpu().numpy()
                g_packed = self.packer.pack(g_quant_np, self.bits)
                s_packed = np.packbits(s_np).tobytes()
            
            device_used = "gpu"
        else:
            # === CPU PATH ===
            flat = arr.flatten().astype(np.float64)
            
            s = (flat >= 0).astype(np.uint8)
            g = np.sqrt(np.abs(flat))
            
            g_min, g_max = float(g.min()), float(g.max())
            g_range = g_max - g_min
            
            if g_range > EPSILON:
                g_norm = (g - g_min) / g_range
            else:
                g_norm = np.zeros_like(g)
            
            g_quant = np.round(g_norm * (self.levels - 1)).astype(np.uint32)
            
            g_nz = g[g > EPSILON]
            variance = float(np.std(g_nz) / (np.mean(g_nz) + EPSILON)) if len(g_nz) > 0 else 0.0
            
            if self.packer_name == "torch" and HAS_TORCH:
                g_quant_torch = torch.from_numpy(g_quant).to(torch.int64)
                g_packed = self.packer.pack(g_quant_torch, self.bits)
            else:
                g_packed = self.packer.pack(g_quant, self.bits)
            s_packed = np.packbits(s).tobytes()
            
            device_used = "cpu"
        
        # Header
        header = io.BytesIO()
        header.write(MAGIC)
        header.write(struct.pack('B', 3))  # version 4.3
        header.write(struct.pack('B', 0))  # mode: direct
        header.write(struct.pack('B', self.bits))
        header.write(struct.pack('B', len(arr.shape)))
        for dim in arr.shape:
            header.write(struct.pack('I', dim))
        header.write(struct.pack('d', g_min))
        header.write(struct.pack('d', g_max))
        header.write(struct.pack('Q', n))
        header.write(struct.pack('I', len(g_packed)))
        
        packed_data = header.getvalue() + g_packed + s_packed
        
        return CompressedTensor(
            packed_data=packed_data,
            mode="direct",
            original_shape=arr.shape,
            original_dtype=str(arr.dtype),
            bits=self.bits,
            g_min=g_min,
            g_max=g_max,
            variance=variance,
            tetelestai=(variance < ALPHA2),
            device_used=device_used,
            packer_used=self.packer_name
        )
    
    def _decompress_direct(self, comp: CompressedTensor) -> np.ndarray:
        """Descompressão DIRECT."""
        data = comp.packed_data
        offset = 0
        
        magic = data[offset:offset+4]; offset += 4
        if magic != MAGIC:
            raise ValueError("Magic inválido")
        
        version = data[offset]; offset += 1
        mode = data[offset]; offset += 1
        bits = data[offset]; offset += 1
        n_dims = data[offset]; offset += 1
        
        shape = []
        for _ in range(n_dims):
            shape.append(struct.unpack('I', data[offset:offset+4])[0])
            offset += 4
        shape = tuple(shape)
        
        g_min = struct.unpack('d', data[offset:offset+8])[0]; offset += 8
        g_max = struct.unpack('d', data[offset:offset+8])[0]; offset += 8
        n = struct.unpack('Q', data[offset:offset+8])[0]; offset += 8
        g_packed_len = struct.unpack('I', data[offset:offset+4])[0]; offset += 4
        
        g_packed = data[offset:offset+g_packed_len]; offset += g_packed_len
        s_packed_len = (n + 7) // 8
        s_packed = data[offset:offset+s_packed_len]
        
        # Desempacotar
        if self.packer_name == "torch" and HAS_TORCH:
            g_quant = self.packer.unpack(g_packed, bits, n, device='cpu')
            g_quant = g_quant.numpy()
        else:
            g_quant = self.packer.unpack(g_packed, bits, n)
        
        g_norm = g_quant.astype(np.float64) / (self.levels - 1)
        g = g_norm * (g_max - g_min) + g_min
        
        s = np.unpackbits(np.frombuffer(s_packed, dtype=np.uint8))[:n]
        s = s.astype(np.float64) * 2 - 1
        
        L = s * (g ** 2)
        return L.reshape(shape)
    
    def _compress_spectral(self, arr: np.ndarray) -> CompressedTensor:
        """Compressão SPECTRAL."""
        original_shape = arr.shape
        
        # Preparar matrizes
        if arr.ndim <= 2:
            matrices = [arr.reshape(-1, 1)] if arr.ndim == 1 else [arr]
        elif arr.ndim == 3:
            matrices = [arr[i] for i in range(arr.shape[0])]
        elif arr.ndim == 4:
            matrices = [arr[b, h] for b in range(arr.shape[0]) for h in range(arr.shape[1])]
        else:
            raise ValueError(f"Tensor {arr.ndim}D não suportado")
        
        n_matrices = len(matrices)
        matrix_shape = matrices[0].shape
        
        # SVD
        if self.use_gpu and HAS_TORCH:
            all_U, all_S, all_Vt = [], [], []
            ranks = []
            
            for mat in matrices:
                mat_torch = torch.from_numpy(mat.astype(np.float64)).to(self.device)
                U, S, Vt = torch.linalg.svd(mat_torch, full_matrices=False)
                
                energy = S ** 2
                total = energy.sum() + EPSILON
                cumsum = torch.cumsum(energy, dim=0) / total
                k = int((cumsum < self.energy_threshold).sum().item()) + 1
                k = max(1, min(k, len(S)))
                
                ranks.append(k)
                all_U.append(U[:, :k])
                all_S.append(S[:k])
                all_Vt.append(Vt[:k, :])
            
            U_cat = torch.cat([u.flatten() for u in all_U])
            S_cat = torch.cat(all_S)
            Vt_cat = torch.cat([vt.flatten() for vt in all_Vt])
            
            device_used = "gpu"
        else:
            all_U, all_S, all_Vt = [], [], []
            ranks = []
            
            for mat in matrices:
                U, S, Vt = np.linalg.svd(mat.astype(np.float64), full_matrices=False)
                
                energy = S ** 2
                total = np.sum(energy) + EPSILON
                cumsum = np.cumsum(energy) / total
                k = np.searchsorted(cumsum, self.energy_threshold) + 1
                k = max(1, min(k, len(S)))
                
                ranks.append(k)
                all_U.append(U[:, :k])
                all_S.append(S[:k])
                all_Vt.append(Vt[:k, :])
            
            U_cat = np.concatenate([u.flatten() for u in all_U])
            S_cat = np.concatenate(all_S)
            Vt_cat = np.concatenate([vt.flatten() for vt in all_Vt])
            
            device_used = "cpu"
        
        # Comprimir componentes com TGL
        def compress_tgl(data):
            if isinstance(data, torch.Tensor):
                s = (data >= 0).to(torch.uint8)
                g = torch.sqrt(torch.abs(data))
                g_min, g_max = g.min().item(), g.max().item()
                rng = g_max - g_min + EPSILON
                g_norm = (g - g_min) / rng
                g_quant = torch.round(g_norm * (self.levels - 1)).to(torch.int64)
                
                if self.packer_name == "torch":
                    g_packed = self.packer.pack(g_quant, self.bits)
                else:
                    g_packed = self.packer.pack(g_quant.cpu().numpy().astype(np.uint32), self.bits)
                s_packed = np.packbits(s.cpu().numpy()).tobytes()
            else:
                s = (data >= 0).astype(np.uint8)
                g = np.sqrt(np.abs(data))
                g_min, g_max = float(g.min()), float(g.max())
                rng = g_max - g_min + EPSILON
                g_norm = (g - g_min) / rng
                g_quant = np.round(g_norm * (self.levels - 1)).astype(np.uint32)
                
                if self.packer_name == "torch" and HAS_TORCH:
                    g_packed = self.packer.pack(torch.from_numpy(g_quant).to(torch.int64), self.bits)
                else:
                    g_packed = self.packer.pack(g_quant, self.bits)
                s_packed = np.packbits(s).tobytes()
            
            return g_packed, s_packed, g_min, g_max, len(data) if not isinstance(data, torch.Tensor) else data.numel()
        
        U_g, U_s, U_min, U_max, U_n = compress_tgl(U_cat)
        S_g, S_s, S_min, S_max, S_n = compress_tgl(S_cat)
        Vt_g, Vt_s, Vt_min, Vt_max, Vt_n = compress_tgl(Vt_cat)
        
        # Header
        header = io.BytesIO()
        header.write(MAGIC)
        header.write(struct.pack('B', 3))
        header.write(struct.pack('B', 1))
        header.write(struct.pack('B', self.bits))
        
        header.write(struct.pack('B', len(original_shape)))
        for d in original_shape:
            header.write(struct.pack('I', d))
        
        header.write(struct.pack('I', n_matrices))
        header.write(struct.pack('HH', matrix_shape[0], matrix_shape[1]))
        for k in ranks:
            header.write(struct.pack('H', k))
        
        header.write(struct.pack('dddd', U_min, U_max, S_min, S_max))
        header.write(struct.pack('dd', Vt_min, Vt_max))
        header.write(struct.pack('QQQ', U_n, S_n, Vt_n))
        header.write(struct.pack('III', len(U_g), len(S_g), len(Vt_g)))
        
        packed = header.getvalue() + U_g + U_s + S_g + S_s + Vt_g + Vt_s
        
        return CompressedTensor(
            packed_data=packed,
            mode="spectral",
            original_shape=original_shape,
            original_dtype=str(arr.dtype),
            bits=self.bits,
            rank=int(np.mean(ranks)),
            n_matrices=n_matrices,
            device_used=device_used,
            packer_used=self.packer_name
        )
    
    def _decompress_spectral(self, comp: CompressedTensor) -> np.ndarray:
        """Descompressão SPECTRAL."""
        data = comp.packed_data
        offset = 0
        
        magic = data[offset:offset+4]; offset += 4
        version = data[offset]; offset += 1
        mode = data[offset]; offset += 1
        bits = data[offset]; offset += 1
        
        n_dims = data[offset]; offset += 1
        original_shape = tuple(struct.unpack('I', data[offset+i*4:offset+(i+1)*4])[0] for i in range(n_dims))
        offset += n_dims * 4
        
        n_matrices = struct.unpack('I', data[offset:offset+4])[0]; offset += 4
        m = struct.unpack('H', data[offset:offset+2])[0]; offset += 2
        n = struct.unpack('H', data[offset:offset+2])[0]; offset += 2
        
        ranks = [struct.unpack('H', data[offset+i*2:offset+(i+1)*2])[0] for i in range(n_matrices)]
        offset += n_matrices * 2
        
        U_min, U_max, S_min, S_max = struct.unpack('dddd', data[offset:offset+32]); offset += 32
        Vt_min, Vt_max = struct.unpack('dd', data[offset:offset+16]); offset += 16
        
        U_n, S_n, Vt_n = struct.unpack('QQQ', data[offset:offset+24]); offset += 24
        U_g_len, S_g_len, Vt_g_len = struct.unpack('III', data[offset:offset+12]); offset += 12
        
        def decompress_tgl(g_data, g_min, g_max, count):
            if self.packer_name == "torch" and HAS_TORCH:
                g_quant = self.packer.unpack(g_data, bits, count, device='cpu').numpy()
            else:
                g_quant = self.packer.unpack(g_data, bits, count)
            g_norm = g_quant.astype(np.float64) / (self.levels - 1)
            return g_norm * (g_max - g_min) + g_min
        
        # U
        U_g_data = data[offset:offset+U_g_len]; offset += U_g_len
        U_s_len = (U_n + 7) // 8
        U_s_data = data[offset:offset+U_s_len]; offset += U_s_len
        U_g = decompress_tgl(U_g_data, U_min, U_max, U_n)
        U_s = np.unpackbits(np.frombuffer(U_s_data, dtype=np.uint8))[:U_n].astype(np.float64) * 2 - 1
        U_cat = U_s * (U_g ** 2)
        
        # S
        S_g_data = data[offset:offset+S_g_len]; offset += S_g_len
        S_s_len = (S_n + 7) // 8
        S_s_data = data[offset:offset+S_s_len]; offset += S_s_len
        S_g = decompress_tgl(S_g_data, S_min, S_max, S_n)
        S_s = np.unpackbits(np.frombuffer(S_s_data, dtype=np.uint8))[:S_n].astype(np.float64) * 2 - 1
        S_cat = S_s * (S_g ** 2)
        
        # Vt
        Vt_g_data = data[offset:offset+Vt_g_len]; offset += Vt_g_len
        Vt_s_len = (Vt_n + 7) // 8
        Vt_s_data = data[offset:offset+Vt_s_len]; offset += Vt_s_len
        Vt_g = decompress_tgl(Vt_g_data, Vt_min, Vt_max, Vt_n)
        Vt_s = np.unpackbits(np.frombuffer(Vt_s_data, dtype=np.uint8))[:Vt_n].astype(np.float64) * 2 - 1
        Vt_cat = Vt_s * (Vt_g ** 2)
        
        # Reconstruir
        matrices = []
        U_off, S_off, Vt_off = 0, 0, 0
        
        for i in range(n_matrices):
            k = ranks[i]
            U_i = U_cat[U_off:U_off + m*k].reshape(m, k); U_off += m * k
            S_i = S_cat[S_off:S_off + k]; S_off += k
            Vt_i = Vt_cat[Vt_off:Vt_off + k*n].reshape(k, n); Vt_off += k * n
            matrices.append(U_i @ np.diag(S_i) @ Vt_i)
        
        if len(original_shape) == 1:
            return matrices[0].flatten()
        elif len(original_shape) == 2:
            return matrices[0]
        elif len(original_shape) == 3:
            return np.stack(matrices)
        elif len(original_shape) == 4:
            batch, heads = original_shape[0], original_shape[1]
            result = np.zeros(original_shape)
            idx = 0
            for b in range(batch):
                for h in range(heads):
                    result[b, h] = matrices[idx]
                    idx += 1
            return result
        return matrices[0]
    
    def compress(self, tensor, mode=None) -> CompressedTensor:
        """Comprime tensor."""
        if HAS_TORCH and isinstance(tensor, torch.Tensor):
            arr = tensor.detach().cpu().numpy()
        else:
            arr = np.asarray(tensor, dtype=np.float64)
        
        mode = mode or self.mode
        if mode == CompressionMode.AUTO:
            mode = CompressionMode.SPECTRAL if arr.ndim >= 2 and min(arr.shape[-2:]) >= 32 else CompressionMode.DIRECT
        
        if mode == CompressionMode.DIRECT:
            return self._compress_direct(arr)
        return self._compress_spectral(arr)
    
    def decompress(self, comp: CompressedTensor) -> np.ndarray:
        """Descomprime tensor."""
        if comp.mode == "direct":
            return self._decompress_direct(comp)
        return self._decompress_spectral(comp)


# ═══════════════════════════════════════════════════════════════════════════════
# BENCHMARK COMPARATIVO
# ═══════════════════════════════════════════════════════════════════════════════

def benchmark_comparison(n_heads=32, head_dim=128, n_tokens=2048):
    """Benchmark comparativo: NumPy vs PyTorch BitPacker."""
    print(f"\n{'═'*70}")
    print(f"BENCHMARK COMPARATIVO: NumPy vs PyTorch BitPacker")
    print(f"{'═'*70}")
    print(f"Config: {n_heads} heads × {head_dim} dim × {n_tokens} tokens")
    print(f"Device: {GPU_NAME}")
    
    # Gerar dados
    np.random.seed(42)
    rank = min(32, n_tokens // 4)
    K = np.random.randn(1, n_heads, n_tokens, rank).astype(np.float32) @ \
        np.random.randn(1, n_heads, rank, head_dim).astype(np.float32) * 0.01
    K += np.random.randn(1, n_heads, n_tokens, head_dim).astype(np.float32) * 0.001
    
    orig_bytes = K.nbytes * 2
    print(f"Original: {orig_bytes:,} bytes ({orig_bytes/1024/1024:.2f} MB)")
    
    results = {}
    
    configs = [
        ("DIRECT 8-bit", 8, CompressionMode.DIRECT),
        ("DIRECT 10-bit", 10, CompressionMode.DIRECT),
        ("DIRECT 12-bit", 12, CompressionMode.DIRECT),
        ("SPECTRAL 10-bit", 10, CompressionMode.SPECTRAL),
    ]
    
    for name, bits, mode in configs:
        print(f"\n{'─'*70}")
        print(f"{name}")
        print(f"{'─'*70}")
        
        for packer_type, packer_name in [(PackerType.NUMPY, "NumPy"), (PackerType.TORCH, "PyTorch")]:
            if packer_type == PackerType.TORCH and not HAS_TORCH:
                continue
            
            # GPU
            if HAS_CUDA:
                tgl = TGLTensorV4(bits=bits, mode=mode, packer_type=packer_type, force_cpu=False)
                
                # Warmup
                _ = tgl.compress(K[:, :1, :100, :])
                
                torch.cuda.synchronize()
                t0 = time.perf_counter()
                comp = tgl.compress(K)
                torch.cuda.synchronize()
                t_comp = time.perf_counter() - t0
                
                t0 = time.perf_counter()
                recon = tgl.decompress(comp)
                t_dec = time.perf_counter() - t0
                
                ratio = K.nbytes / comp.compressed_bytes
                mse = np.mean((K - recon) ** 2)
                psnr = 10 * np.log10(np.max(K**2) / (mse + 1e-15))
                cos = np.dot(K.flat, recon.flat) / (np.linalg.norm(K) * np.linalg.norm(recon) + 1e-15)
                
                print(f"  {packer_name} GPU: {ratio:.2f}x | {psnr:.0f}dB | cos={cos:.4f} | "
                      f"comp={t_comp*1000:.0f}ms dec={t_dec*1000:.0f}ms")
                
                results[f"{name} ({packer_name} GPU)"] = {
                    'ratio': ratio, 'psnr': psnr, 'cos': cos,
                    't_comp': t_comp, 't_dec': t_dec
                }
            
            # CPU
            tgl_cpu = TGLTensorV4(bits=bits, mode=mode, packer_type=packer_type, force_cpu=True)
            
            t0 = time.perf_counter()
            comp_cpu = tgl_cpu.compress(K)
            t_comp_cpu = time.perf_counter() - t0
            
            t0 = time.perf_counter()
            recon_cpu = tgl_cpu.decompress(comp_cpu)
            t_dec_cpu = time.perf_counter() - t0
            
            ratio_cpu = K.nbytes / comp_cpu.compressed_bytes
            mse_cpu = np.mean((K - recon_cpu) ** 2)
            psnr_cpu = 10 * np.log10(np.max(K**2) / (mse_cpu + 1e-15))
            cos_cpu = np.dot(K.flat, recon_cpu.flat) / (np.linalg.norm(K) * np.linalg.norm(recon_cpu) + 1e-15)
            
            print(f"  {packer_name} CPU: {ratio_cpu:.2f}x | {psnr_cpu:.0f}dB | cos={cos_cpu:.4f} | "
                  f"comp={t_comp_cpu*1000:.0f}ms dec={t_dec_cpu*1000:.0f}ms")
            
            results[f"{name} ({packer_name} CPU)"] = {
                'ratio': ratio_cpu, 'psnr': psnr_cpu, 'cos': cos_cpu,
                't_comp': t_comp_cpu, 't_dec': t_dec_cpu
            }
    
    # Análise de speedup
    print(f"\n{'═'*70}")
    print("ANÁLISE DE SPEEDUP")
    print(f"{'═'*70}")
    
    for config_name, bits, mode in configs:
        numpy_gpu_key = f"{config_name} (NumPy GPU)"
        torch_gpu_key = f"{config_name} (PyTorch GPU)"
        numpy_cpu_key = f"{config_name} (NumPy CPU)"
        torch_cpu_key = f"{config_name} (PyTorch CPU)"
        
        print(f"\n{config_name}:")
        
        if numpy_gpu_key in results and torch_gpu_key in results:
            speedup = results[numpy_gpu_key]['t_comp'] / results[torch_gpu_key]['t_comp']
            print(f"  PyTorch vs NumPy (GPU): {speedup:.2f}x")
        
        if numpy_cpu_key in results and torch_cpu_key in results:
            speedup = results[numpy_cpu_key]['t_comp'] / results[torch_cpu_key]['t_comp']
            print(f"  PyTorch vs NumPy (CPU): {speedup:.2f}x")
        
        if torch_cpu_key in results and torch_gpu_key in results:
            speedup = results[torch_cpu_key]['t_comp'] / results[torch_gpu_key]['t_comp']
            print(f"  GPU vs CPU (PyTorch):   {speedup:.2f}x")
    
    return results


def main():
    print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║  TGL-TENSOR v4.3 — BitPacker PyTorch (GPU Nativo)                            ║
║  Teoria da Gravitação Luminodinâmica                                         ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    print(f"NumPy: {np.__version__}")
    print(f"PyTorch: {'Sim' if HAS_TORCH else 'Não'}")
    print(f"CUDA: {'Sim' if HAS_CUDA else 'Não'}")
    print(f"Device: {GPU_NAME}")
    
    # Testar BitPackers
    bitpacker_results = test_bitpackers()
    
    # Benchmark comparativo
    comparison_results = benchmark_comparison()
    
    # Resumo final
    print(f"\n{'═'*70}")
    print("RESUMO FINAL")
    print(f"{'═'*70}")
    
    # Encontrar melhor configuração
    valid_results = {k: v for k, v in comparison_results.items() if v['cos'] > 0.99}
    if valid_results:
        fastest = min(valid_results.keys(), key=lambda k: valid_results[k]['t_comp'])
        best_ratio = max(valid_results.keys(), key=lambda k: valid_results[k]['ratio'])
        
        print(f"\nMais rápido (cos>0.99): {fastest}")
        print(f"  {valid_results[fastest]['t_comp']*1000:.0f}ms, {valid_results[fastest]['ratio']:.2f}x")
        
        print(f"\nMelhor taxa (cos>0.99): {best_ratio}")
        print(f"  {valid_results[best_ratio]['ratio']:.2f}x, {valid_results[best_ratio]['t_comp']*1000:.0f}ms")
    
    print(f"\n{'─'*70}")
    print("                         — TETELESTAI —")
    
    return bitpacker_results, comparison_results


if __name__ == "__main__":
    main()