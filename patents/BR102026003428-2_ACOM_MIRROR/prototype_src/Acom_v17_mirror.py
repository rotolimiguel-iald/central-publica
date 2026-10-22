#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    ACOM v17.0 — MIRROR                                       ║
║                                                                              ║
║              "Teletransporte de Informação Espelhada"                        ║
║                                                                              ║
║                 Teoria da Gravitação Luminodinâmica                          ║
║                    Luiz Antonio Rotoli Miguel                                ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  PARADIGMA:                                                                  ║
║                                                                              ║
║      ACOM não é compressão — é REFLEXÃO DIMENSIONAL                         ║
║                                                                              ║
║      O dado não "viaja" — o REFLEXO viaja                                   ║
║      O dado RE-EMERGE através da DOBRA                                      ║
║                                                                              ║
║  OS CINCO PILARES:                                                           ║
║                                                                              ║
║      1. ψ é NOMINADO em ℋ (Espaço de Hilbert), não quantizado              ║
║      2. F_exp é DERIVADA de ψ, não armazenada                               ║
║      3. θ (ponto angular) é INFORMAÇÃO DE RETORNO                           ║
║      4. DOBRA = ×2 = Boundary→Bulk = Reflexão Especular                     ║
║      5. Modos são REFLEXÕES PSIÔNICAS (espelhos dos dados)                  ║
║                                                                              ║
║  OPERAÇÕES:                                                                  ║
║                                                                              ║
║      REFLECT: L → (ψ, θ)     Projetar no espelho                           ║
║      MANIFEST: (ψ, θ) → L'   Desdobrar de volta                            ║
║                                                                              ║
║  CONSTANTES:                                                                 ║
║                                                                              ║
║      α² = 0.012              Imperfeição do espelho cósmico                 ║
║      θ_Miguel = 6.29°        Ponto angular fundamental                      ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import numpy as np
import torch
import torch.nn.functional as F
from dataclasses import dataclass
from typing import Tuple, Dict, Any, List, Optional
from enum import IntEnum
import time
import math
import warnings
warnings.filterwarnings('ignore')

try:
    import zstandard as zstd
    HAS_ZSTD = True
except ImportError:
    HAS_ZSTD = False

import zlib

# ══════════════════════════════════════════════════════════════════════════════
# CONSTANTES FUNDAMENTAIS
# ══════════════════════════════════════════════════════════════════════════════

ALPHA2 = 0.012                          # Imperfeição do espelho cósmico
ALPHA = math.sqrt(ALPHA2)               # √α²
THETA_MIGUEL = math.asin(ALPHA)         # Ponto angular fundamental ≈ 6.29°
PHI_GOLDEN = (1 + math.sqrt(5)) / 2     # Proporção áurea
EPSILON = 1e-10

# A DOBRA: fator de desdobramento dimensional
FOLD_FACTOR = 2.0  # ×2 = Boundary→Bulk = Reflexão

print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    ACOM v17.0 — MIRROR                                       ║
║              "Teletransporte de Informação Espelhada"                        ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  O dado não viaja — o REFLEXO viaja                                         ║
║  O dado RE-EMERGE através da DOBRA                                          ║
║                                                                              ║
║  α² = {ALPHA2:.6f}  (imperfeição do espelho)                                  ║
║  θ_Miguel = {math.degrees(THETA_MIGUEL):.4f}°  (ponto angular fundamental)                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")


# ══════════════════════════════════════════════════════════════════════════════
# ESTADOS PSIÔNICOS NO ESPAÇO DE HILBERT ℋ₄
# ══════════════════════════════════════════════════════════════════════════════

class PsionicState(IntEnum):
    """
    Estados nominados no Espaço de Hilbert ℋ₄.
    
    Não são números — são ESTADOS.
    Cada estado é um vetor base em ℋ₄.
    """
    COLLAPSE_PLUS = 0   # |COLAPSO⁺⟩  — Positivo, Colapsando (paridade inversa)
    ASCEND_PLUS = 1     # |ASCENSÃO⁺⟩ — Positivo, Ascendendo (paridade normal)
    EMERGE_MINUS = 2    # |EMERGÊNCIA⁻⟩ — Negativo, Emergindo (paridade normal)
    FALL_MINUS = 3      # |QUEDA⁻⟩    — Negativo, Afundando (paridade inversa)


# Vetores base no Espaço de Hilbert ℋ₄
# Cada estado é um vetor ortonormal
HILBERT_BASIS = {
    PsionicState.COLLAPSE_PLUS: torch.tensor([1., 0., 0., 0.]),   # |0⟩
    PsionicState.ASCEND_PLUS:   torch.tensor([0., 1., 0., 0.]),   # |1⟩
    PsionicState.EMERGE_MINUS:  torch.tensor([0., 0., 1., 0.]),   # |2⟩
    PsionicState.FALL_MINUS:    torch.tensor([0., 0., 0., 1.]),   # |3⟩
}

# Paridade de cada estado
# NORMAL: sign(L) e sign(∂L) concordam na "direção"
# INVERSA: sign(L) e sign(∂L) discordam — FORÇA DE EXPULSÃO
PARITY = {
    PsionicState.COLLAPSE_PLUS: -1,  # (+,-) Inversa — F_exp ativo
    PsionicState.ASCEND_PLUS:   +1,  # (+,+) Normal
    PsionicState.EMERGE_MINUS:  +1,  # (-,+) Normal  
    PsionicState.FALL_MINUS:    -1,  # (-,-) Inversa — F_exp ativo
}

# Sinal de L para cada estado (para reconstrução)
SIGN_L = {
    PsionicState.COLLAPSE_PLUS: +1,
    PsionicState.ASCEND_PLUS:   +1,
    PsionicState.EMERGE_MINUS:  -1,
    PsionicState.FALL_MINUS:    -1,
}


# ══════════════════════════════════════════════════════════════════════════════
# ESTRUTURAS DE DADOS
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class MirrorReflection:
    """
    Reflexo no espelho dimensional.
    
    Não contém os dados — contém o REFLEXO.
    Os dados re-emergem através da dobra.
    """
    psi_states: bytes           # Estados ψ nominados (comprimidos)
    theta_angles: bytes         # Pontos angulares θ (informação de retorno)
    metadata: Dict[str, Any]    # Informações para manifestação


# ══════════════════════════════════════════════════════════════════════════════
# O ESPELHO DIMENSIONAL
# ══════════════════════════════════════════════════════════════════════════════

class DimensionalMirror:
    """
    Espelho Dimensional para reflexão de dados.
    
    Projeta dados 3D (L) no espelho (boundary 2D),
    nomina estados ψ em ℋ₄, e registra pontos angulares θ.
    """
    
    def __init__(self, device: torch.device = None, angular_bits: int = 8):
        """
        Args:
            device: Dispositivo de computação
            angular_bits: Bits para quantização angular de θ
        """
        self.device = device or torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.angular_bits = angular_bits
        self.use_zstd = HAS_ZSTD
        
        # Número de níveis angulares
        self.n_angles = (1 << angular_bits)  # 2^bits níveis
        
        # Pré-computar tabela de senos para reconstrução rápida
        angles = torch.linspace(0, math.pi/2, self.n_angles, device=self.device)
        self.sin_table = torch.sin(angles)
    
    def _nominate_state(self, sign_L: torch.Tensor, sign_dL: torch.Tensor) -> torch.Tensor:
        """
        Nomina estados ψ no Espaço de Hilbert ℋ₄.
        
        Não é codificação — é NOMINAÇÃO.
        Cada ponto de dados recebe um NOME (estado).
        """
        # Construir índice de estado a partir dos sinais
        # bit_high = 1 se L < 0, senão 0
        # bit_low = 1 se dL > 0, senão 0
        bit_high = (sign_L < 0).long()
        bit_low = (sign_dL > 0).long()
        
        # Estado = bit_high * 2 + bit_low
        # 0 = (+,-) COLLAPSE_PLUS
        # 1 = (+,+) ASCEND_PLUS
        # 2 = (-,+) EMERGE_MINUS
        # 3 = (-,-) FALL_MINUS
        states = bit_high * 2 + bit_low
        
        return states.to(torch.uint8)
    
    def _compute_angular_point(self, g: torch.Tensor, g_max: float) -> torch.Tensor:
        """
        Computa o ponto angular θ — a INFORMAÇÃO DE RETORNO.
        
        θ = arcsin(g / g_max)
        
        Este é o "endereço de retorno" para a manifestação.
        """
        # Normalizar g para [0, 1]
        g_normalized = g / (g_max + EPSILON)
        g_normalized = torch.clamp(g_normalized, 0, 1)
        
        # θ = arcsin(g_normalized) em [0, π/2]
        theta = torch.asin(g_normalized)
        
        return theta
    
    def _quantize_angular(self, theta: torch.Tensor) -> torch.Tensor:
        """
        Quantiza θ em níveis angulares.
        
        A quantização angular dá mais resolução perto de θ=0
        (valores pequenos de g) e menos perto de θ=π/2
        (valores grandes de g).
        
        Isso é NATURAL — a função sin(θ) tem derivada máxima em θ=0.
        """
        # Normalizar para [0, 1]
        theta_normalized = theta / (math.pi / 2)
        
        # Quantizar
        max_level = self.n_angles - 1
        quantized = torch.round(theta_normalized * max_level).to(torch.int32)
        quantized = torch.clamp(quantized, 0, max_level)
        
        return quantized
    
    def _dequantize_angular(self, quantized: torch.Tensor) -> torch.Tensor:
        """
        Dequantiza níveis angulares de volta para θ.
        """
        max_level = self.n_angles - 1
        theta_normalized = quantized.float() / max_level
        theta = theta_normalized * (math.pi / 2)
        return theta
    
    def reflect(self, L: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, Dict]:
        """
        REFLECT: Projeta dados no espelho dimensional.
        
        L → (ψ, θ)
        
        O dado não é comprimido — é REFLETIDO.
        O reflexo (ψ, θ) captura a FORMA do dado.
        
        Returns:
            (psi_states, theta_quantized, metadata)
        """
        L = L.to(self.device).flatten().float()
        n = len(L)
        
        # ══════════════════════════════════════════════════════════════════════
        # PASSO 1: Computar o gráviton g = √|L|
        # ══════════════════════════════════════════════════════════════════════
        g = torch.sqrt(torch.abs(L) + EPSILON)
        g_max = g.max().item()
        g_min = g.min().item()
        
        # ══════════════════════════════════════════════════════════════════════
        # PASSO 2: Computar derivada temporal ∂L
        # ══════════════════════════════════════════════════════════════════════
        dL = torch.zeros_like(L)
        dL[1:] = L[1:] - L[:-1]
        dL[0] = dL[1] if n > 1 else 0
        
        # ══════════════════════════════════════════════════════════════════════
        # PASSO 3: Determinar sinais
        # ══════════════════════════════════════════════════════════════════════
        sign_L = torch.sign(L)
        sign_dL = torch.sign(dL)
        
        # Tratar zeros (convenção: zero → positivo)
        sign_L = torch.where(sign_L == 0, torch.ones_like(sign_L), sign_L)
        sign_dL = torch.where(sign_dL == 0, torch.ones_like(sign_dL), sign_dL)
        
        # ══════════════════════════════════════════════════════════════════════
        # PASSO 4: NOMINAR estados ψ no Espaço de Hilbert ℋ₄
        # ══════════════════════════════════════════════════════════════════════
        psi_states = self._nominate_state(sign_L, sign_dL)
        
        # ══════════════════════════════════════════════════════════════════════
        # PASSO 5: Computar pontos angulares θ (INFORMAÇÃO DE RETORNO)
        # ══════════════════════════════════════════════════════════════════════
        theta = self._compute_angular_point(g, g_max)
        theta_quantized = self._quantize_angular(theta)
        
        # ══════════════════════════════════════════════════════════════════════
        # PASSO 6: Calcular Força de Expulsão (DERIVADA de ψ)
        # ══════════════════════════════════════════════════════════════════════
        # F_exp emerge automaticamente da distribuição de paridades
        parities = torch.tensor([PARITY[PsionicState(s.item())] for s in psi_states], 
                               device=self.device, dtype=torch.float32)
        f_exp = parities.mean().item()  # Força de expulsão média
        
        # Contagem de estados
        state_counts = {}
        for state in PsionicState:
            count = (psi_states == state.value).sum().item()
            state_counts[state.name] = count
        
        # Calcular entropia de estados (complexidade da forma refletida)
        state_probs = torch.bincount(psi_states.long(), minlength=4).float() / n
        state_probs = state_probs[state_probs > 0]
        state_entropy = -torch.sum(state_probs * torch.log2(state_probs)).item()
        
        metadata = {
            'n_elements': n,
            'g_max': g_max,
            'g_min': g_min,
            'angular_bits': self.angular_bits,
            'f_exp': f_exp,  # Força de expulsão (emerge de ψ)
            'state_counts': state_counts,
            'state_entropy': state_entropy,
            'theta_miguel': THETA_MIGUEL,
        }
        
        return psi_states, theta_quantized, metadata
    
    def manifest(self, psi_states: torch.Tensor, theta_quantized: torch.Tensor, 
                 metadata: Dict) -> torch.Tensor:
        """
        MANIFEST: Desdobra o reflexo de volta para dados.
        
        (ψ, θ) → L'
        
        O dado RE-EMERGE através da DOBRA.
        Não é decodificação — é MANIFESTAÇÃO.
        """
        n = metadata['n_elements']
        g_max = metadata['g_max']
        
        psi_states = psi_states.to(self.device)
        theta_quantized = theta_quantized.to(self.device)
        
        # ══════════════════════════════════════════════════════════════════════
        # PASSO 1: RETURN — Recuperar θ do ponto angular
        # ══════════════════════════════════════════════════════════════════════
        theta = self._dequantize_angular(theta_quantized)
        
        # ══════════════════════════════════════════════════════════════════════
        # PASSO 2: Reconstruir g via sin(θ)
        # ══════════════════════════════════════════════════════════════════════
        g = g_max * torch.sin(theta)
        
        # ══════════════════════════════════════════════════════════════════════
        # PASSO 3: Recuperar sinal de L a partir de ψ
        # ══════════════════════════════════════════════════════════════════════
        sign_L = torch.zeros(n, device=self.device, dtype=torch.float32)
        for state in PsionicState:
            mask = (psi_states == state.value)
            sign_L[mask] = SIGN_L[state]
        
        # ══════════════════════════════════════════════════════════════════════
        # PASSO 4: DOBRA — L = s × g²
        # ══════════════════════════════════════════════════════════════════════
        # A dobra é a multiplicação g × g (geométrica)
        # que é equivalente ao desdobramento dimensional
        L = sign_L * (g ** 2)
        
        return L.to(torch.float64)


# ══════════════════════════════════════════════════════════════════════════════
# ACOM v17.0 — MIRROR (Interface Principal)
# ══════════════════════════════════════════════════════════════════════════════

class ACOMv17Mirror:
    """
    ACOM v17.0 — MIRROR
    
    Teletransporte de Informação Espelhada.
    
    Não é compressão tradicional — é REFLEXÃO DIMENSIONAL.
    O dado não viaja — o REFLEXO viaja.
    O dado RE-EMERGE através da DOBRA.
    """
    
    def __init__(self, device: torch.device = None, angular_bits: int = 8, verbose: bool = False):
        self.device = device or torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.angular_bits = angular_bits
        self.verbose = verbose
        self.use_zstd = HAS_ZSTD
        
        self.mirror = DimensionalMirror(device=self.device, angular_bits=angular_bits)
    
    def _pack_states(self, states: torch.Tensor) -> bytes:
        """Empacota estados ψ (4 estados por byte, 2 bits cada)."""
        states_np = states.cpu().numpy().astype(np.uint8)
        n = len(states_np)
        
        # Padding para múltiplo de 4
        padded_len = ((n + 3) // 4) * 4
        padded = np.zeros(padded_len, dtype=np.uint8)
        padded[:n] = states_np
        
        # Empacotar 4 estados por byte
        n_bytes = padded_len // 4
        packed = np.zeros(n_bytes, dtype=np.uint8)
        
        for i in range(n_bytes):
            packed[i] = (padded[i*4] << 6) | (padded[i*4+1] << 4) | \
                       (padded[i*4+2] << 2) | padded[i*4+3]
        
        return packed.tobytes()
    
    def _unpack_states(self, packed: bytes, n: int) -> torch.Tensor:
        """Desempacota estados ψ."""
        packed_np = np.frombuffer(packed, dtype=np.uint8)
        
        states = []
        for byte_val in packed_np:
            states.extend([
                (byte_val >> 6) & 0x03,
                (byte_val >> 4) & 0x03,
                (byte_val >> 2) & 0x03,
                byte_val & 0x03
            ])
        
        return torch.tensor(states[:n], dtype=torch.uint8)
    
    def _pack_angles(self, angles: torch.Tensor) -> bytes:
        """Empacota ângulos θ quantizados."""
        if self.angular_bits <= 8:
            return angles.cpu().numpy().astype(np.uint8).tobytes()
        else:
            return angles.cpu().numpy().astype(np.uint16).tobytes()
    
    def _unpack_angles(self, packed: bytes, n: int) -> torch.Tensor:
        """Desempacota ângulos θ."""
        if self.angular_bits <= 8:
            return torch.tensor(np.frombuffer(packed, dtype=np.uint8)[:n], dtype=torch.int32)
        else:
            return torch.tensor(np.frombuffer(packed, dtype=np.uint16)[:n], dtype=torch.int32)
    
    def reflect(self, data: torch.Tensor) -> MirrorReflection:
        """
        REFLECT: Projeta dados no espelho dimensional.
        
        Retorna um MirrorReflection que contém o REFLEXO, não os dados.
        """
        data_flat = data.to(self.device).flatten().float()
        n = data.numel()
        original_shape = tuple(data.shape)
        original_size = n * 8  # float64
        
        # Projetar no espelho
        psi_states, theta_quantized, mirror_meta = self.mirror.reflect(data_flat)
        
        if self.verbose:
            print(f"    Reflexão no espelho dimensional...")
            print(f"    Estados ψ: {mirror_meta['state_counts']}")
            print(f"    F_exp: {mirror_meta['f_exp']:.4f}")
            print(f"    Entropia: {mirror_meta['state_entropy']:.3f} bits")
        
        # Empacotar estados e ângulos
        states_packed = self._pack_states(psi_states)
        angles_packed = self._pack_angles(theta_quantized)
        
        # Combinar
        combined = states_packed + angles_packed
        
        # Comprimir o reflexo
        if self.use_zstd:
            cctx = zstd.ZstdCompressor(level=22)
            compressed_states = cctx.compress(states_packed)
            compressed_angles = cctx.compress(angles_packed)
        else:
            compressed_states = zlib.compress(states_packed, 9)
            compressed_angles = zlib.compress(angles_packed, 9)
        
        compressed_size = len(compressed_states) + len(compressed_angles)
        ratio = original_size / compressed_size if compressed_size > 0 else float('inf')
        
        metadata = {
            'version': 'ACOM_v17.0_MIRROR',
            'paradigm': 'Dimensional Reflection',
            'shape': original_shape,
            'n_elements': n,
            'angular_bits': self.angular_bits,
            'g_max': mirror_meta['g_max'],
            'g_min': mirror_meta['g_min'],
            'f_exp': mirror_meta['f_exp'],
            'state_counts': mirror_meta['state_counts'],
            'state_entropy': mirror_meta['state_entropy'],
            'states_bytes': len(states_packed),
            'angles_bytes': len(angles_packed),
            'compressed_states_bytes': len(compressed_states),
            'compressed_angles_bytes': len(compressed_angles),
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_ratio': ratio,
            'alpha2': ALPHA2,
            'theta_miguel': THETA_MIGUEL,
        }
        
        return MirrorReflection(
            psi_states=compressed_states,
            theta_angles=compressed_angles,
            metadata=metadata
        )
    
    def manifest(self, reflection: MirrorReflection) -> torch.Tensor:
        """
        MANIFEST: Desdobra o reflexo de volta para dados.
        
        O dado RE-EMERGE — não é decodificado.
        """
        meta = reflection.metadata
        n = meta['n_elements']
        shape = tuple(meta['shape'])
        
        # Descomprimir
        if self.use_zstd:
            dctx = zstd.ZstdDecompressor()
            states_packed = dctx.decompress(reflection.psi_states)
            angles_packed = dctx.decompress(reflection.theta_angles)
        else:
            states_packed = zlib.decompress(reflection.psi_states)
            angles_packed = zlib.decompress(reflection.theta_angles)
        
        # Desempacotar
        psi_states = self._unpack_states(states_packed, n)
        theta_quantized = self._unpack_angles(angles_packed, n)
        
        # Manifestar através da dobra
        L = self.mirror.manifest(psi_states, theta_quantized, meta)
        
        return L.reshape(shape)


# ══════════════════════════════════════════════════════════════════════════════
# COMPARADOR COM v16.1
# ══════════════════════════════════════════════════════════════════════════════

class ACOMv161:
    """ACOM v16.1 para comparação (versão simplificada)."""
    
    def __init__(self, device: torch.device = None, bits_g: int = 6):
        self.device = device or torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.bits_g = bits_g
        self.use_zstd = HAS_ZSTD
    
    def compress(self, data: torch.Tensor) -> Tuple[bytes, Dict]:
        data_flat = data.to(self.device).flatten().float()
        n = data.numel()
        original_size = n * 8
        
        # Derivada
        dL = torch.zeros_like(data_flat)
        dL[1:] = data_flat[1:] - data_flat[:-1]
        dL[0] = dL[1] if n > 1 else 0
        
        # Sinais
        sign_L = torch.sign(data_flat)
        sign_dL = torch.sign(dL)
        sign_L = torch.where(sign_L == 0, torch.ones_like(sign_L), sign_L)
        sign_dL = torch.where(sign_dL == 0, torch.ones_like(sign_dL), sign_dL)
        
        # Modos (2 bits)
        modes = ((sign_L < 0).long() * 2 + (sign_dL > 0).long()).to(torch.uint8)
        
        # Magnitudes
        g = torch.sqrt(torch.abs(data_flat) + 1e-10)
        g_min, g_max = g.min().item(), g.max().item()
        g_range = g_max - g_min
        
        if g_range < 1e-10:
            g_quantized = torch.zeros(n, dtype=torch.uint8)
        else:
            max_val = (1 << self.bits_g) - 1
            g_quantized = torch.round((g - g_min) / g_range * max_val).clamp(0, max_val).to(torch.uint8)
        
        # Empacotar modos
        modes_np = modes.cpu().numpy()
        padded_len = ((n + 3) // 4) * 4
        padded = np.zeros(padded_len, dtype=np.uint8)
        padded[:n] = modes_np
        n_bytes = padded_len // 4
        modes_packed = np.zeros(n_bytes, dtype=np.uint8)
        for i in range(n_bytes):
            modes_packed[i] = (padded[i*4] << 6) | (padded[i*4+1] << 4) | (padded[i*4+2] << 2) | padded[i*4+3]
        
        combined = modes_packed.tobytes() + g_quantized.cpu().numpy().tobytes()
        
        if self.use_zstd:
            compressed = zstd.ZstdCompressor(level=22).compress(combined)
        else:
            compressed = zlib.compress(combined, 9)
        
        meta = {
            'version': 'ACOM_v16.1',
            'shape': tuple(data.shape),
            'n': n,
            'g_min': g_min,
            'g_max': g_max,
            'g_range': g_range,
            'bits_g': self.bits_g,
            'modes_bytes': len(modes_packed),
            'original_size': original_size,
            'compressed_size': len(compressed),
            'compression_ratio': original_size / len(compressed)
        }
        
        return compressed, meta
    
    def decompress(self, compressed: bytes, meta: Dict) -> torch.Tensor:
        n = meta['n']
        shape = tuple(meta['shape'])
        
        if self.use_zstd:
            combined = zstd.ZstdDecompressor().decompress(compressed)
        else:
            combined = zlib.decompress(compressed)
        
        modes_bytes = meta['modes_bytes']
        modes_packed = np.frombuffer(combined[:modes_bytes], dtype=np.uint8)
        g_quantized = np.frombuffer(combined[modes_bytes:], dtype=np.uint8)
        
        # Desempacotar modos
        modes = []
        for byte_val in modes_packed:
            modes.extend([(byte_val >> 6) & 0x03, (byte_val >> 4) & 0x03, (byte_val >> 2) & 0x03, byte_val & 0x03])
        modes = torch.tensor(modes[:n], device=self.device, dtype=torch.int64)
        
        # Dequantizar
        g_range = meta['g_range']
        if g_range < 1e-10:
            g = torch.full((n,), meta['g_min'], device=self.device)
        else:
            max_val = (1 << meta['bits_g']) - 1
            g = torch.tensor(g_quantized, device=self.device, dtype=torch.float32) / max_val * g_range + meta['g_min']
        
        # Reconstruir
        sign_L = torch.where(modes < 2, torch.ones(n, device=self.device), -torch.ones(n, device=self.device))
        L = sign_L * (g ** 2)
        
        return L.reshape(shape).to(torch.float64)


# ══════════════════════════════════════════════════════════════════════════════
# BENCHMARK COMPARATIVO
# ══════════════════════════════════════════════════════════════════════════════

def run_benchmark():
    """Executa benchmark comparando v16.1 vs v17.0 MIRROR."""
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    BENCHMARK: v16.1 vs v17.0 MIRROR                          ║
║                                                                              ║
║              "O dado não viaja — o REFLEXO viaja"                            ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Device: {device}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"Backend: {'zstd' if HAS_ZSTD else 'zlib'}")
    print()
    
    # Instanciar compressores
    acom_v161 = ACOMv161(device=device, bits_g=6)
    acom_v17 = ACOMv17Mirror(device=device, angular_bits=8, verbose=False)
    
    # Dados de teste
    np.random.seed(42)
    torch.manual_seed(42)
    
    test_cases = [
        {
            'name': 'embeddings',
            'data': torch.randn(1000, 384, device=device, dtype=torch.float64),
            'desc': 'Embeddings (randn)'
        },
        {
            'name': 'audio',
            'data': torch.sin(torch.linspace(0, 100*np.pi, 44100, device=device, dtype=torch.float64)) * 
                    torch.exp(-torch.linspace(0, 5, 44100, device=device, dtype=torch.float64)),
            'desc': 'Áudio (senoidal com decay)'
        },
        {
            'name': 'financial',
            'data': 100 * torch.cumprod(1 + torch.randn(2000, device=device, dtype=torch.float64) * 0.02, dim=0),
            'desc': 'Financial (preços, sempre > 0)'
        },
        {
            'name': 'kv_cache',
            'data': torch.randn(4, 2, 8, 64, 32, device=device, dtype=torch.float64),
            'desc': 'KV-Cache (LLM)'
        },
        {
            'name': 'sparse',
            'data': torch.zeros(50000, device=device, dtype=torch.float64).scatter_(
                0, torch.randint(0, 50000, (2500,), device=device), 
                torch.randn(2500, device=device, dtype=torch.float64)
            ),
            'desc': 'Sparse (95% zeros)'
        },
        {
            'name': 'gradients',
            'data': torch.randn(10000, device=device, dtype=torch.float64) * 0.01,
            'desc': 'Gradientes (pequenos)'
        },
    ]
    
    results = []
    
    print("="*90)
    print(f"{'Teste':<12} | {'v16.1':^20} | {'v17.0 MIRROR':^20} | {'Δ Ratio':^10} | {'F_exp':^8}")
    print("="*90)
    
    for case in test_cases:
        name = case['name']
        data = case['data']
        desc = case['desc']
        
        try:
            # v16.1
            start = time.time()
            compressed_161, meta_161 = acom_v161.compress(data)
            time_161 = time.time() - start
            
            reconstructed_161 = acom_v161.decompress(compressed_161, meta_161)
            
            orig = data.flatten().float()
            rec_161 = reconstructed_161.flatten().float()
            corr_161 = torch.corrcoef(torch.stack([orig, rec_161]))[0, 1].item()
            if np.isnan(corr_161):
                corr_161 = 0.0
            
            ratio_161 = meta_161['compression_ratio']
            
            # v17.0 MIRROR
            start = time.time()
            reflection = acom_v17.reflect(data)
            time_17 = time.time() - start
            
            manifested = acom_v17.manifest(reflection)
            
            rec_17 = manifested.flatten().float()
            corr_17 = torch.corrcoef(torch.stack([orig, rec_17]))[0, 1].item()
            if np.isnan(corr_17):
                corr_17 = 0.0
            
            ratio_17 = reflection.metadata['compression_ratio']
            f_exp = reflection.metadata['f_exp']
            
            # Delta
            delta_ratio = ratio_17 - ratio_161
            delta_pct = (ratio_17 / ratio_161 - 1) * 100
            
            # Estado
            state_161 = 'T' if corr_161 >= 0.999 else 'N' if corr_161 >= 0.99 else 'F'
            state_17 = 'T' if corr_17 >= 0.999 else 'N' if corr_17 >= 0.99 else 'F'
            
            print(f"{name:<12} | {ratio_161:>6.2f}x ({corr_161:.4f}){state_161} | {ratio_17:>6.2f}x ({corr_17:.4f}){state_17} | {delta_pct:>+8.1f}% | {f_exp:>+.4f}")
            
            results.append({
                'name': name,
                'ratio_161': ratio_161,
                'ratio_17': ratio_17,
                'corr_161': corr_161,
                'corr_17': corr_17,
                'delta_pct': delta_pct,
                'f_exp': f_exp,
                'state_counts': reflection.metadata['state_counts'],
                'state_entropy': reflection.metadata['state_entropy'],
            })
            
        except Exception as e:
            print(f"{name:<12} | ERRO: {e}")
            import traceback
            traceback.print_exc()
    
    # Sumário
    if results:
        print("="*90)
        print("\nANÁLISE DA FORÇA DE EXPULSÃO (F_exp):")
        print("-"*60)
        
        for r in results:
            f_exp = r['f_exp']
            counts = r['state_counts']
            
            # Paridade inversa vs normal
            inverse = counts.get('COLLAPSE_PLUS', 0) + counts.get('FALL_MINUS', 0)
            normal = counts.get('ASCEND_PLUS', 0) + counts.get('EMERGE_MINUS', 0)
            total = inverse + normal
            
            inv_pct = inverse / total * 100 if total > 0 else 0
            
            print(f"  {r['name']:<12}: F_exp = {f_exp:>+.4f} | Paridade Inversa: {inv_pct:>5.1f}% | Entropia: {r['state_entropy']:.3f}")
        
        print("\n" + "="*90)
        
        avg_161 = np.mean([r['ratio_161'] for r in results])
        avg_17 = np.mean([r['ratio_17'] for r in results])
        avg_corr_161 = np.mean([r['corr_161'] for r in results])
        avg_corr_17 = np.mean([r['corr_17'] for r in results])
        
        print(f"\nMÉDIAS:")
        print(f"  v16.1:      {avg_161:.2f}x  (corr: {avg_corr_161:.5f})")
        print(f"  v17.0:      {avg_17:.2f}x  (corr: {avg_corr_17:.5f})")
        print(f"  Diferença:  {(avg_17/avg_161 - 1)*100:+.1f}%")
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  Código Disponibilizado em modalidade Source Avaiable                        ║
║  Uso Comercial Disponível mediante licenciamento da IALD Ltda.               ║
║  Registro de Patente: BR 10 2026 003428 2 (11/02/2006)                       ║   
║                                                                              ║
║                                                                              ║
║          PARADIGMA MIRROR:                                                   ║
║                                                                              ║
║      REFLECT: L → (ψ, θ)    Projetar no espelho                              ║
║      MANIFEST: (ψ, θ) → L'  Desdobrar de volta                               ║
║                                                                              ║
║  O dado não viaja — o REFLEXO viaja                                          ║
║  O dado RE-EMERGE através da DOBRA                                           ║
║                                                                              ║
║  HAJA LUZ! ✨                                                                ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    return results


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    results = run_benchmark()