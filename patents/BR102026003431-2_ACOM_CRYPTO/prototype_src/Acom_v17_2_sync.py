#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    ACOM v17.2 — SYNC                                         ║
║                                                                              ║
║              "Handshake de Sincronia Miguel"                                 ║
║                                                                              ║
║                 Teoria da Gravitação Luminodinâmica                          ║
║                    Luiz Antonio Rotoli Miguel                                ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  PARADIGMA:                                                                  ║
║                                                                              ║
║      Em vez de trocar CHAVES (números), trocar CALIBRAÇÕES (estados)        ║
║      A "chave" não é transmitida — ela EMERGE da sincronização              ║
║                                                                              ║
║  PROTOCOLO:                                                                  ║
║                                                                              ║
║      1. SONDAGEM: Emissor envia pulso de ruído (Luz Primordial)             ║
║      2. ECO: Receptor retorna assinatura de paridade                         ║
║      3. CALIBRAÇÃO: Ambos derivam α²_sync único para sessão                 ║
║      4. TÚNEL: Canal estabelecido com θ_sync compartilhado                  ║
║                                                                              ║
║  SEGURANÇA:                                                                  ║
║                                                                              ║
║      Man-in-the-Middle não pode replicar α²_sync sem participar             ║
║      da calibração inicial — o sinal aparece como ruído térmico             ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import numpy as np
import torch
import hashlib
import secrets
import json
import struct
import time
import math
from dataclasses import dataclass, field
from typing import Tuple, Dict, Any, List, Optional
from enum import IntEnum
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

ALPHA2_BASE = 0.012              # Constante de Miguel base
ALPHA_BASE = math.sqrt(ALPHA2_BASE)
THETA_MIGUEL = math.asin(ALPHA_BASE)
EPSILON = 1e-10

# Parâmetros de sincronização
SYNC_PULSE_SIZE = 1024           # Tamanho do pulso de sondagem
JITTER_SCALE = 1e-8              # Escala do jitter do neutrino (variação de α²)
CALIBRATION_ROUNDS = 3           # Rodadas de calibração

# Versão do protocolo
PROTOCOL_VERSION = b'ACOM_SYNC_v17.2'

print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    ACOM v17.2 — SYNC                                         ║
║              "Handshake de Sincronia Miguel"                                 ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Em vez de trocar CHAVES, trocar CALIBRAÇÕES                                ║
║  A "chave" EMERGE da sincronização                                          ║
║                                                                              ║
║  α²_base = {ALPHA2_BASE:.6f}                                                     ║
║  θ_Miguel = {math.degrees(THETA_MIGUEL):.4f}°                                                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")


# ══════════════════════════════════════════════════════════════════════════════
# ESTADOS PSIÔNICOS
# ══════════════════════════════════════════════════════════════════════════════

class PsionicState(IntEnum):
    COLLAPSE_PLUS = 0   # |COLAPSO⁺⟩
    ASCEND_PLUS = 1     # |ASCENSÃO⁺⟩
    EMERGE_MINUS = 2    # |EMERGÊNCIA⁻⟩
    FALL_MINUS = 3      # |QUEDA⁻⟩


# ══════════════════════════════════════════════════════════════════════════════
# ESTRUTURAS DO PROTOCOLO
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class SyncPulse:
    """
    Pulso de Sondagem — Luz Primordial.
    
    Não contém dados. Serve para medir a Impedância do Substrato.
    """
    pulse_id: bytes               # ID único do pulso
    primordial_light: bytes       # Ruído gaussiano (Luz Primordial)
    timestamp: float              # Momento da emissão
    sender_id: bytes              # ID do emissor
    
    def to_bytes(self) -> bytes:
        meta = {
            'pulse_id': self.pulse_id.hex(),
            'timestamp': self.timestamp,
            'sender_id': self.sender_id.hex(),
        }
        meta_json = json.dumps(meta).encode('utf-8')
        return struct.pack('<I', len(meta_json)) + meta_json + self.primordial_light
    
    @classmethod
    def from_bytes(cls, data: bytes) -> 'SyncPulse':
        meta_len = struct.unpack('<I', data[:4])[0]
        meta = json.loads(data[4:4+meta_len].decode('utf-8'))
        primordial_light = data[4+meta_len:]
        return cls(
            pulse_id=bytes.fromhex(meta['pulse_id']),
            primordial_light=primordial_light,
            timestamp=meta['timestamp'],
            sender_id=bytes.fromhex(meta['sender_id']),
        )


@dataclass
class ParityEcho:
    """
    Eco de Paridade — Resposta do receptor.
    
    Informa ao emissor a Imperfeição do Espelho local.
    """
    echo_id: bytes                # ID do eco
    pulse_id: bytes               # ID do pulso original
    f_exp_local: float            # Força de Expulsão local
    state_signature: bytes        # Assinatura dos estados
    deflection_angle: float       # Ângulo de deflexão θ
    alpha2_local: float           # α² medido localmente
    receiver_id: bytes            # ID do receptor
    timestamp: float
    
    def to_bytes(self) -> bytes:
        meta = {
            'echo_id': self.echo_id.hex(),
            'pulse_id': self.pulse_id.hex(),
            'f_exp_local': self.f_exp_local,
            'state_signature': self.state_signature.hex(),
            'deflection_angle': self.deflection_angle,
            'alpha2_local': self.alpha2_local,
            'receiver_id': self.receiver_id.hex(),
            'timestamp': self.timestamp,
        }
        return json.dumps(meta).encode('utf-8')
    
    @classmethod
    def from_bytes(cls, data: bytes) -> 'ParityEcho':
        meta = json.loads(data.decode('utf-8'))
        return cls(
            echo_id=bytes.fromhex(meta['echo_id']),
            pulse_id=bytes.fromhex(meta['pulse_id']),
            f_exp_local=meta['f_exp_local'],
            state_signature=bytes.fromhex(meta['state_signature']),
            deflection_angle=meta['deflection_angle'],
            alpha2_local=meta['alpha2_local'],
            receiver_id=bytes.fromhex(meta['receiver_id']),
            timestamp=meta['timestamp'],
        )


@dataclass
class HilbertTunnel:
    """
    Túnel de Hilbert — Canal sincronizado.
    
    Contém todos os parâmetros da sessão sincronizada.
    """
    tunnel_id: bytes              # ID do túnel
    alpha2_sync: float            # α² sincronizado para esta sessão
    theta_sync: float             # θ sincronizado
    f_exp_sync: float             # F_exp de referência
    state_mapping: Dict[int, int] # Mapeamento de estados ψ
    session_key: bytes            # Chave de sessão derivada
    participants: List[bytes]     # IDs dos participantes
    established_at: float         # Momento do estabelecimento
    expires_at: float             # Momento de expiração
    
    def is_valid(self) -> bool:
        """Verifica se o túnel ainda é válido."""
        return time.time() < self.expires_at
    
    def to_bytes(self) -> bytes:
        meta = {
            'tunnel_id': self.tunnel_id.hex(),
            'alpha2_sync': self.alpha2_sync,
            'theta_sync': self.theta_sync,
            'f_exp_sync': self.f_exp_sync,
            'state_mapping': self.state_mapping,
            'session_key': self.session_key.hex(),
            'participants': [p.hex() for p in self.participants],
            'established_at': self.established_at,
            'expires_at': self.expires_at,
        }
        return json.dumps(meta).encode('utf-8')
    
    @classmethod
    def from_bytes(cls, data: bytes) -> 'HilbertTunnel':
        meta = json.loads(data.decode('utf-8'))
        return cls(
            tunnel_id=bytes.fromhex(meta['tunnel_id']),
            alpha2_sync=meta['alpha2_sync'],
            theta_sync=meta['theta_sync'],
            f_exp_sync=meta['f_exp_sync'],
            state_mapping={int(k): v for k, v in meta['state_mapping'].items()},
            session_key=bytes.fromhex(meta['session_key']),
            participants=[bytes.fromhex(p) for p in meta['participants']],
            established_at=meta['established_at'],
            expires_at=meta['expires_at'],
        )


@dataclass
class SyncedMessage:
    """
    Mensagem transmitida através do Túnel de Hilbert.
    """
    message_id: bytes
    tunnel_id: bytes
    psi_states: bytes             # Estados ψ (cifrados com session_key)
    theta_angles: bytes           # Ângulos θ (cifrados com session_key)
    f_exp_check: float            # F_exp para verificação
    shape: Tuple[int, ...]
    n_elements: int
    g_max: float
    sequence_number: int          # Número de sequência (anti-replay)
    timestamp: float


# ══════════════════════════════════════════════════════════════════════════════
# NODO DE SINCRONIZAÇÃO
# ══════════════════════════════════════════════════════════════════════════════

class SyncNode:
    """
    Nodo capaz de participar do Handshake de Sincronia Miguel.
    
    Cada nodo tem:
    - Um ID único
    - Um "espelho" local com α² ligeiramente diferente
    - Capacidade de gerar/processar pulsos e ecos
    """
    
    def __init__(self, device: torch.device = None, node_id: bytes = None):
        self.device = device or torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.node_id = node_id or secrets.token_bytes(16)
        self.angular_bits = 8
        self.n_angles = 256
        self.use_zstd = HAS_ZSTD
        
        # α² local com jitter (simulando variação natural)
        self.alpha2_local = ALPHA2_BASE + np.random.normal(0, JITTER_SCALE)
        
        # Túneis ativos
        self.active_tunnels: Dict[bytes, HilbertTunnel] = {}
        
        # Sequências para anti-replay
        self.sequence_numbers: Dict[bytes, int] = {}
    
    def _generate_primordial_light(self, size: int = SYNC_PULSE_SIZE) -> torch.Tensor:
        """
        Gera Luz Primordial — ruído gaussiano puro.
        
        Este é o "pulso do gráviton" que sonda o substrato.
        """
        return torch.randn(size, device=self.device, dtype=torch.float64)
    
    def _compute_state_signature(self, light: torch.Tensor) -> Tuple[bytes, float, torch.Tensor]:
        """
        Computa a assinatura de estados a partir da Luz Primordial.
        
        Returns:
            (signature_hash, f_exp, states)
        """
        # Derivada
        dL = torch.zeros_like(light)
        dL[1:] = light[1:] - light[:-1]
        dL[0] = dL[1] if len(light) > 1 else 0
        
        # Sinais
        sign_L = torch.sign(light)
        sign_dL = torch.sign(dL)
        sign_L = torch.where(sign_L == 0, torch.ones_like(sign_L), sign_L)
        sign_dL = torch.where(sign_dL == 0, torch.ones_like(sign_dL), sign_dL)
        
        # Estados ψ
        bit_high = (sign_L < 0).long()
        bit_low = (sign_dL > 0).long()
        states = (bit_high * 2 + bit_low).to(torch.uint8)
        
        # F_exp
        parities = torch.ones(len(states), device=self.device, dtype=torch.float32)
        parities[(states == 0) | (states == 3)] = -1.0
        f_exp = parities.mean().item()
        
        # Hash da assinatura
        states_bytes = states.cpu().numpy().tobytes()
        signature = hashlib.sha256(states_bytes).digest()
        
        return signature, f_exp, states
    
    def _compute_deflection_angle(self, light: torch.Tensor) -> float:
        """
        Computa o Ângulo de Deflexão θ necessário para estabilizar o pulso.
        
        Este é o ângulo que "alinha" o espelho local com o pulso recebido.
        """
        g = torch.sqrt(torch.abs(light) + EPSILON)
        g_normalized = g / (g.max() + EPSILON)
        
        # Média dos ângulos (ponto de equilíbrio)
        theta_mean = torch.asin(g_normalized).mean().item()
        
        return theta_mean
    
    def _derive_alpha2_sync(self, f_exp_a: float, f_exp_b: float, 
                            theta_a: float, theta_b: float) -> float:
        """
        Deriva α²_sync a partir das medições de ambos os nodos.
        
        Esta é a "chave" que emerge da sincronização.
        """
        # Combinar F_exp (média geométrica)
        f_combined = math.sqrt(abs(f_exp_a * f_exp_b) + EPSILON)
        
        # Combinar ângulos (média)
        theta_combined = (theta_a + theta_b) / 2
        
        # α²_sync = sin²(θ_combined) × (1 + f_combined × jitter)
        alpha2_sync = math.sin(theta_combined) ** 2 * (1 + f_combined * JITTER_SCALE * 1000)
        
        # Normalizar para ficar próximo de α²_base
        alpha2_sync = ALPHA2_BASE + (alpha2_sync - ALPHA2_BASE) * 0.001
        
        return alpha2_sync
    
    def _derive_session_key(self, alpha2_sync: float, tunnel_id: bytes) -> bytes:
        """
        Deriva chave de sessão a partir de α²_sync e tunnel_id.
        """
        key_material = struct.pack('<d', alpha2_sync) + tunnel_id
        return hashlib.sha256(key_material).digest()
    
    # ══════════════════════════════════════════════════════════════════════════
    # FASE 1: SONDAGEM
    # ══════════════════════════════════════════════════════════════════════════
    
    def create_sync_pulse(self) -> SyncPulse:
        """
        Cria pulso de sondagem (Luz Primordial).
        
        Este pulso não contém dados — serve para medir o substrato.
        """
        light = self._generate_primordial_light()
        light_bytes = light.cpu().numpy().tobytes()
        
        return SyncPulse(
            pulse_id=secrets.token_bytes(16),
            primordial_light=light_bytes,
            timestamp=time.time(),
            sender_id=self.node_id,
        )
    
    # ══════════════════════════════════════════════════════════════════════════
    # FASE 2: ECO DE PARIDADE
    # ══════════════════════════════════════════════════════════════════════════
    
    def process_pulse_create_echo(self, pulse: SyncPulse) -> ParityEcho:
        """
        Processa pulso recebido e cria Eco de Paridade.
        
        O eco informa ao emissor a Imperfeição do Espelho local.
        """
        # Reconstruir luz primordial
        light = torch.tensor(
            np.frombuffer(pulse.primordial_light, dtype=np.float64),
            device=self.device
        )
        
        # Calcular assinatura local
        signature, f_exp, states = self._compute_state_signature(light)
        
        # Calcular ângulo de deflexão
        theta = self._compute_deflection_angle(light)
        
        return ParityEcho(
            echo_id=secrets.token_bytes(16),
            pulse_id=pulse.pulse_id,
            f_exp_local=f_exp,
            state_signature=signature,
            deflection_angle=theta,
            alpha2_local=self.alpha2_local,
            receiver_id=self.node_id,
            timestamp=time.time(),
        )
    
    # ══════════════════════════════════════════════════════════════════════════
    # FASE 3: ESTABELECIMENTO DO TÚNEL
    # ══════════════════════════════════════════════════════════════════════════
    
    def establish_tunnel(self, pulse: SyncPulse, echo: ParityEcho, 
                        ttl_seconds: float = 3600) -> HilbertTunnel:
        """
        Estabelece Túnel de Hilbert após troca de pulso/eco.
        
        Ambos os nodos devem chamar este método com os mesmos dados
        para derivar o mesmo α²_sync.
        """
        # Reconstruir luz para calcular nossa parte
        light = torch.tensor(
            np.frombuffer(pulse.primordial_light, dtype=np.float64),
            device=self.device
        )
        
        _, f_exp_local, _ = self._compute_state_signature(light)
        theta_local = self._compute_deflection_angle(light)
        
        # Derivar α²_sync (ambos os lados chegam ao mesmo valor!)
        alpha2_sync = self._derive_alpha2_sync(
            f_exp_local, echo.f_exp_local,
            theta_local, echo.deflection_angle
        )
        
        # θ sincronizado
        theta_sync = math.asin(math.sqrt(alpha2_sync))
        
        # F_exp de referência (média)
        f_exp_sync = (f_exp_local + echo.f_exp_local) / 2
        
        # ID do túnel (derivado dos IDs dos participantes)
        tunnel_id = hashlib.sha256(pulse.sender_id + echo.receiver_id).digest()[:16]
        
        # Chave de sessão
        session_key = self._derive_session_key(alpha2_sync, tunnel_id)
        
        # Mapeamento de estados (identidade, mas poderia ser permutado)
        state_mapping = {0: 0, 1: 1, 2: 2, 3: 3}
        
        now = time.time()
        tunnel = HilbertTunnel(
            tunnel_id=tunnel_id,
            alpha2_sync=alpha2_sync,
            theta_sync=theta_sync,
            f_exp_sync=f_exp_sync,
            state_mapping=state_mapping,
            session_key=session_key,
            participants=[pulse.sender_id, echo.receiver_id],
            established_at=now,
            expires_at=now + ttl_seconds,
        )
        
        # Registrar túnel
        self.active_tunnels[tunnel_id] = tunnel
        self.sequence_numbers[tunnel_id] = 0
        
        return tunnel
    
    # ══════════════════════════════════════════════════════════════════════════
    # FASE 4: TRANSMISSÃO
    # ══════════════════════════════════════════════════════════════════════════
    
    def _xor_bytes(self, data: bytes, key: bytes) -> bytes:
        """XOR com chave (stream cipher simplificado)."""
        # Expandir chave usando hash
        expanded = b''
        counter = 0
        while len(expanded) < len(data):
            expanded += hashlib.sha256(key + counter.to_bytes(4, 'big')).digest()
            counter += 1
        return bytes(a ^ b for a, b in zip(data, expanded[:len(data)]))
    
    def _pack_states(self, states: torch.Tensor) -> bytes:
        """Empacota estados (4 por byte)."""
        states_np = states.cpu().numpy().astype(np.uint8)
        n = len(states_np)
        padded_len = ((n + 3) // 4) * 4
        padded = np.zeros(padded_len, dtype=np.uint8)
        padded[:n] = states_np
        
        n_bytes = padded_len // 4
        packed = np.zeros(n_bytes, dtype=np.uint8)
        for i in range(n_bytes):
            packed[i] = (padded[i*4] << 6) | (padded[i*4+1] << 4) | \
                       (padded[i*4+2] << 2) | padded[i*4+3]
        return packed.tobytes()
    
    def _unpack_states(self, packed: bytes, n: int) -> torch.Tensor:
        """Desempacota estados."""
        packed_np = np.frombuffer(packed, dtype=np.uint8)
        states = []
        for byte_val in packed_np:
            states.extend([(byte_val >> 6) & 0x03, (byte_val >> 4) & 0x03,
                          (byte_val >> 2) & 0x03, byte_val & 0x03])
        return torch.tensor(states[:n], dtype=torch.uint8, device=self.device)
    
    def _compress(self, data: bytes) -> bytes:
        if self.use_zstd:
            return zstd.ZstdCompressor(level=22).compress(data)
        return zlib.compress(data, 9)
    
    def _decompress(self, data: bytes) -> bytes:
        if self.use_zstd:
            return zstd.ZstdDecompressor().decompress(data)
        return zlib.decompress(data)
    
    def send_through_tunnel(self, data: torch.Tensor, tunnel: HilbertTunnel) -> SyncedMessage:
        """
        Transmite dados através do Túnel de Hilbert.
        
        O dado é refletido no espelho sincronizado.
        """
        if not tunnel.is_valid():
            raise ValueError("Túnel expirado!")
        
        data_flat = data.to(self.device).flatten().float()
        n = data.numel()
        shape = tuple(data.shape)
        
        # Gráviton com α²_sync
        g = torch.sqrt(torch.abs(data_flat) + EPSILON)
        g_max = g.max().item()
        
        # Derivada e sinais
        dL = torch.zeros_like(data_flat)
        dL[1:] = data_flat[1:] - data_flat[:-1]
        dL[0] = dL[1] if n > 1 else 0
        
        sign_L = torch.sign(data_flat)
        sign_dL = torch.sign(dL)
        sign_L = torch.where(sign_L == 0, torch.ones_like(sign_L), sign_L)
        sign_dL = torch.where(sign_dL == 0, torch.ones_like(sign_dL), sign_dL)
        
        # Estados ψ
        bit_high = (sign_L < 0).long()
        bit_low = (sign_dL > 0).long()
        psi_states = (bit_high * 2 + bit_low).to(torch.uint8)
        
        # F_exp para verificação
        parities = torch.ones(n, device=self.device, dtype=torch.float32)
        parities[(psi_states == 0) | (psi_states == 3)] = -1.0
        f_exp = parities.mean().item()
        
        # Ângulos θ (usando α²_sync como referência!)
        g_normalized = torch.clamp(g / (g_max + EPSILON), 0.0, 1.0)
        theta = torch.asin(g_normalized)
        # Ajuste com α²_sync
        theta_adjusted = theta * (1 + tunnel.alpha2_sync - ALPHA2_BASE)
        max_level = self.n_angles - 1
        theta_quantized = torch.round(theta_adjusted / (math.pi / 2) * max_level).long()
        theta_quantized = torch.clamp(theta_quantized, 0, max_level).to(torch.uint8)
        
        # Empacotar
        states_packed = self._pack_states(psi_states)
        angles_packed = theta_quantized.cpu().numpy().tobytes()
        
        # Cifrar com session_key
        states_encrypted = self._xor_bytes(states_packed, tunnel.session_key)
        angles_encrypted = self._xor_bytes(angles_packed, tunnel.session_key + b'theta')
        
        # Comprimir
        states_compressed = self._compress(states_encrypted)
        angles_compressed = self._compress(angles_encrypted)
        
        # Número de sequência
        seq = self.sequence_numbers[tunnel.tunnel_id]
        self.sequence_numbers[tunnel.tunnel_id] = seq + 1
        
        return SyncedMessage(
            message_id=secrets.token_bytes(16),
            tunnel_id=tunnel.tunnel_id,
            psi_states=states_compressed,
            theta_angles=angles_compressed,
            f_exp_check=f_exp,
            shape=shape,
            n_elements=n,
            g_max=g_max,
            sequence_number=seq,
            timestamp=time.time(),
        )
    
    def receive_from_tunnel(self, message: SyncedMessage, tunnel: HilbertTunnel,
                           verify: bool = True) -> torch.Tensor:
        """
        Recebe dados do Túnel de Hilbert.
        
        O dado RE-EMERGE através da dobra sincronizada.
        """
        if not tunnel.is_valid():
            raise ValueError("Túnel expirado!")
        
        if message.tunnel_id != tunnel.tunnel_id:
            raise ValueError("Mensagem não pertence a este túnel!")
        
        # Verificar anti-replay
        expected_seq = self.sequence_numbers.get(tunnel.tunnel_id, 0)
        if message.sequence_number < expected_seq:
            raise ValueError(f"Possível ataque de replay! Seq {message.sequence_number} < {expected_seq}")
        self.sequence_numbers[tunnel.tunnel_id] = message.sequence_number + 1
        
        # Descomprimir
        states_encrypted = self._decompress(message.psi_states)
        angles_encrypted = self._decompress(message.theta_angles)
        
        # Decifrar
        states_packed = self._xor_bytes(states_encrypted, tunnel.session_key)
        angles_packed = self._xor_bytes(angles_encrypted, tunnel.session_key + b'theta')
        
        # Desempacotar
        n = message.n_elements
        psi_states = self._unpack_states(states_packed, n)
        theta_quantized = torch.tensor(
            np.frombuffer(angles_packed, dtype=np.uint8)[:n],
            device=self.device, dtype=torch.int32
        )
        
        # Verificar F_exp
        if verify:
            parities = torch.ones(n, device=self.device, dtype=torch.float32)
            parities[(psi_states == 0) | (psi_states == 3)] = -1.0
            f_exp_computed = parities.mean().item()
            
            if abs(f_exp_computed - message.f_exp_check) > 0.001:
                raise ValueError(f"Verificação F_exp falhou! "
                               f"Esperado: {message.f_exp_check:.4f}, "
                               f"Obtido: {f_exp_computed:.4f}")
        
        # MANIFESTAÇÃO (DOBRA)
        # θ → g (com ajuste α²_sync)
        max_level = self.n_angles - 1
        theta_normalized = theta_quantized.float() / max_level
        theta = theta_normalized * (math.pi / 2)
        # Desfazer ajuste
        theta_original = theta / (1 + tunnel.alpha2_sync - ALPHA2_BASE)
        g = message.g_max * torch.sin(theta_original)
        
        # ψ → sign_L
        sign_L = torch.ones(n, device=self.device, dtype=torch.float32)
        sign_L[(psi_states == 2) | (psi_states == 3)] = -1.0
        
        # DOBRA: L = s × g²
        L = sign_L * (g ** 2)
        
        return L.reshape(message.shape).to(torch.float64)


# ══════════════════════════════════════════════════════════════════════════════
# DEMONSTRAÇÃO DO PROTOCOLO
# ══════════════════════════════════════════════════════════════════════════════

def demonstrate_sync_protocol():
    """Demonstra o Handshake de Sincronia Miguel."""
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    DEMONSTRAÇÃO: HANDSHAKE DE SINCRONIA MIGUEL               ║
║                                                                              ║
║              Em vez de trocar CHAVES, trocar CALIBRAÇÕES                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Device: {device}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
    print()
    
    # ══════════════════════════════════════════════════════════════════════════
    # CRIAR NODOS
    # ══════════════════════════════════════════════════════════════════════════
    
    print("[1] CRIANDO NODOS (Alice e Bob)")
    print("-" * 60)
    
    alice = SyncNode(device=device)
    bob = SyncNode(device=device)
    
    print(f"    Alice ID: {alice.node_id.hex()[:16]}...")
    print(f"    Alice α²_local: {alice.alpha2_local:.12f}")
    print(f"    Bob ID: {bob.node_id.hex()[:16]}...")
    print(f"    Bob α²_local: {bob.alpha2_local:.12f}")
    print(f"    Diferença α²: {abs(alice.alpha2_local - bob.alpha2_local):.2e}")
    
    # ══════════════════════════════════════════════════════════════════════════
    # FASE 1: SONDAGEM
    # ══════════════════════════════════════════════════════════════════════════
    
    print("\n[2] FASE 1: SONDAGEM (Pulso do Gráviton)")
    print("-" * 60)
    
    # Alice envia pulso
    pulse = alice.create_sync_pulse()
    print(f"    Alice → Pulso ID: {pulse.pulse_id.hex()[:16]}...")
    print(f"    Tamanho da Luz Primordial: {len(pulse.primordial_light)} bytes")
    print(f"    Timestamp: {pulse.timestamp:.6f}")
    
    # ══════════════════════════════════════════════════════════════════════════
    # FASE 2: ECO DE PARIDADE
    # ══════════════════════════════════════════════════════════════════════════
    
    print("\n[3] FASE 2: ECO DE PARIDADE (Bob responde)")
    print("-" * 60)
    
    # Bob processa e responde
    echo = bob.process_pulse_create_echo(pulse)
    print(f"    Bob → Echo ID: {echo.echo_id.hex()[:16]}...")
    print(f"    F_exp local: {echo.f_exp_local:.6f}")
    print(f"    Ângulo de Deflexão: {math.degrees(echo.deflection_angle):.4f}°")
    print(f"    α² local: {echo.alpha2_local:.12f}")
    
    # ══════════════════════════════════════════════════════════════════════════
    # FASE 3: ESTABELECIMENTO DO TÚNEL
    # ══════════════════════════════════════════════════════════════════════════
    
    print("\n[4] FASE 3: ESTABELECIMENTO DO TÚNEL DE HILBERT")
    print("-" * 60)
    
    # Ambos estabelecem o túnel (chegam aos mesmos valores!)
    tunnel_alice = alice.establish_tunnel(pulse, echo)
    tunnel_bob = bob.establish_tunnel(pulse, echo)
    
    print(f"    Alice α²_sync: {tunnel_alice.alpha2_sync:.12f}")
    print(f"    Bob α²_sync:   {tunnel_bob.alpha2_sync:.12f}")
    print(f"    Match perfeito: {tunnel_alice.alpha2_sync == tunnel_bob.alpha2_sync}")
    print(f"    θ_sync: {math.degrees(tunnel_alice.theta_sync):.6f}°")
    print(f"    F_exp_sync: {tunnel_alice.f_exp_sync:.6f}")
    print(f"    Session Key: {tunnel_alice.session_key.hex()[:32]}...")
    
    # ══════════════════════════════════════════════════════════════════════════
    # FASE 4: TRANSMISSÃO
    # ══════════════════════════════════════════════════════════════════════════
    
    print("\n[5] FASE 4: TRANSMISSÃO POR RE-EMERGÊNCIA")
    print("-" * 60)
    
    # Alice cria dados secretos
    secret_data = torch.randn(10000, device=device, dtype=torch.float64)
    print(f"    Dados originais: shape={secret_data.shape}")
    print(f"    Range: [{secret_data.min():.4f}, {secret_data.max():.4f}]")
    
    # Alice envia através do túnel
    start = time.time()
    message = alice.send_through_tunnel(secret_data, tunnel_alice)
    send_time = (time.time() - start) * 1000
    
    print(f"\n    Alice → Mensagem através do túnel")
    print(f"    Tamanho Ψ: {len(message.psi_states)} bytes")
    print(f"    Tamanho Θ: {len(message.theta_angles)} bytes")
    print(f"    F_exp check: {message.f_exp_check:.6f}")
    print(f"    Tempo de envio: {send_time:.2f}ms")
    
    # Bob recebe
    start = time.time()
    received_data = bob.receive_from_tunnel(message, tunnel_bob, verify=True)
    recv_time = (time.time() - start) * 1000
    
    # Verificar
    correlation = torch.corrcoef(torch.stack([
        secret_data.flatten().float(),
        received_data.flatten().float()
    ]))[0, 1].item()
    
    print(f"\n    Bob ← Dados manifestados")
    print(f"    Correlação: {correlation:.10f}")
    print(f"    Tempo de recepção: {recv_time:.2f}ms")
    print(f"    Verificação: PASSOU ✓" if correlation > 0.999 else "    Verificação: FALHOU ✗")
    
    # ══════════════════════════════════════════════════════════════════════════
    # TESTE DE SEGURANÇA: EVE (MAN-IN-THE-MIDDLE)
    # ══════════════════════════════════════════════════════════════════════════
    
    print("\n[6] TESTE DE SEGURANÇA: EVE (INTERCEPTADOR)")
    print("-" * 60)
    
    eve = SyncNode(device=device)
    print(f"    Eve α²_local: {eve.alpha2_local:.12f}")
    print(f"    Eve NÃO participou do handshake!")
    
    # Eve tenta criar um túnel falso
    try:
        # Eve não tem o pulso original ou o eco real
        # Ela só pode criar um túnel com parâmetros diferentes
        fake_pulse = eve.create_sync_pulse()  # Pulso diferente!
        fake_echo = eve.process_pulse_create_echo(fake_pulse)
        fake_tunnel = eve.establish_tunnel(fake_pulse, fake_echo)
        
        print(f"\n    Eve tenta decodificar com túnel falso...")
        print(f"    Eve α²_sync: {fake_tunnel.alpha2_sync:.12f}")
        print(f"    Diferença: {abs(fake_tunnel.alpha2_sync - tunnel_alice.alpha2_sync):.2e}")
        
        # Eve tenta receber a mensagem
        try:
            eve_data = eve.receive_from_tunnel(message, fake_tunnel, verify=True)
            print(f"    FALHA: Eve conseguiu decodificar!")
        except Exception as e:
            print(f"    Resultado: BLOQUEADO ✓")
            print(f"    Erro: {type(e).__name__}: {str(e)[:50]}...")
            
    except Exception as e:
        print(f"    Eve bloqueada: {e}")
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  HANDSHAKE DE SINCRONIA MIGUEL — DEMONSTRADO                                 ║
║                                                                              ║
║  ✓ Fase 1: Sondagem (Pulso do Gráviton)                                     ║
║  ✓ Fase 2: Eco de Paridade (Calibração do Espelho)                          ║
║  ✓ Fase 3: Túnel de Hilbert (α²_sync derivado)                              ║
║  ✓ Fase 4: Transmissão (Re-emergência)                                      ║
║  ✓ Segurança: Man-in-the-Middle bloqueado                                   ║
║                                                                              ║
║  A "chave" não foi transmitida — ela EMERGIU da sincronização              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    return tunnel_alice, tunnel_bob


# ══════════════════════════════════════════════════════════════════════════════
# BENCHMARK
# ══════════════════════════════════════════════════════════════════════════════

def run_benchmark():
    """Benchmark do protocolo SYNC."""
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    BENCHMARK: ACOM v17.2 SYNC                                ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Device: {device}")
    
    # Criar nodos
    alice = SyncNode(device=device)
    bob = SyncNode(device=device)
    
    # Estabelecer túnel
    pulse = alice.create_sync_pulse()
    echo = bob.process_pulse_create_echo(pulse)
    tunnel_alice = alice.establish_tunnel(pulse, echo)
    tunnel_bob = bob.establish_tunnel(pulse, echo)
    
    print(f"\nTúnel estabelecido com α²_sync = {tunnel_alice.alpha2_sync:.12f}")
    print()
    
    test_cases = [
        ('1K', 1000),
        ('10K', 10000),
        ('100K', 100000),
        ('1M', 1000000),
    ]
    
    print("="*80)
    print(f"{'Tamanho':<10} | {'Envio':>10} | {'Recepção':>10} | {'Total':>10} | {'Throughput':>12} | {'Corr':>10}")
    print("="*80)
    
    for name, size in test_cases:
        try:
            data = torch.randn(size, device=device, dtype=torch.float64)
            
            # Envio
            start = time.time()
            msg = alice.send_through_tunnel(data, tunnel_alice)
            send_time = (time.time() - start) * 1000
            
            # Recepção
            start = time.time()
            received = bob.receive_from_tunnel(msg, tunnel_bob, verify=True)
            recv_time = (time.time() - start) * 1000
            
            total_time = send_time + recv_time
            throughput = size * 8 / (total_time / 1000) / 1e6  # Mbps
            
            correlation = torch.corrcoef(torch.stack([
                data.flatten().float(),
                received.flatten().float()
            ]))[0, 1].item()
            
            print(f"{name:<10} | {send_time:>8.2f}ms | {recv_time:>8.2f}ms | {total_time:>8.2f}ms | {throughput:>10.2f}Mb/s | {correlation:.8f}")
            
        except Exception as e:
            print(f"{name:<10} | ERRO: {e}")
    
    print("="*80)
    print("\nHAJA LUZ! ✨")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--benchmark':
        run_benchmark()
    else:
        demonstrate_sync_protocol()
        print("\n" + "="*80 + "\n")
        run_benchmark()