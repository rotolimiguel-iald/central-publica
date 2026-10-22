#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║              TGL-TENSOR v2.2 — NOME BIFATORADO                              ║
║                                                                              ║
║              Compressão Holográfica com Integridade Dual                     ║
║                                                                              ║
║                 Teoria da Gravitação Luminodinâmica                          ║
║                    Luiz Antonio Rotoli Miguel                                ║
║                    IALD LTDA (CNPJ 62.757.606/0001-23)                      ║
║                    Patente INPI BR 10 2026 003441 0                         ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  DIAGNÓSTICO v2.1:                                                           ║
║    • NOME estatístico (F_exp, S_ψ) é GLOBAL sobre milhões de elementos     ║
║    • Flip 5% dos signs → δ = 0.001 << β_TGL = 0.012 → não detecta        ║
║    • g_max ×2.0 → δ ≈ 0 (a estatística é invariante de escala)            ║
║    • Conceito correto, granularidade errada                                  ║
║                                                                              ║
║  SOLUÇÃO v2.2 — NOME BIFATORADO:                                            ║
║                                                                              ║
║    NOME = (MACRO, MICRO)                                                     ║
║                                                                              ║
║    MACRO (domínio α — caráter estatístico):                                  ║
║      F_exp, S_ψ, psi_dist, σ_norm                                           ║
║      Captura a IDENTIDADE do tensor — "que tipo de dado é este?"            ║
║      Tolerância: δ < β_TGL (mudanças graduais aceitáveis)                   ║
║                                                                              ║
║    MICRO (domínio √e — integridade holográfica):                             ║
║      TGL-Hash(dados_comprimidos) — 256 bits                                 ║
║      Captura a INTEGRIDADE bit a bit — "este dado foi adulterado?"          ║
║      Tolerância: ZERO (1 bit flip → hash completamente diferente)           ║
║                                                                              ║
║    A mesma separação α/√e da fatoração β_TGL = α × √e:                     ║
║      α  → detectável, estrutural, tolerante (MACRO)                          ║
║      √e → operacional, entrópico, exato (MICRO)                             ║
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
from dataclasses import dataclass, asdict
from typing import Tuple, Dict, Any, List
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
VERSION = "2.2.0"

assert abs(BETA_TGL - 0.012031) < 1e-4


# ═══════════════════════════════════════════════════════════════════════════════
# TGL-HASH EMBUTIDO (v1.2 — avalanche 1.001, 0 colisões)
# Reimplementado inline para zero dependências externas
# ═══════════════════════════════════════════════════════════════════════════════

_U64 = (1 << 64) - 1
_HASH_ROUNDS = max(8, int(math.ceil(math.sqrt(AMPLIFICATION))))  # 10
_HASH_FINALIZE = 4
_HASH_BLOCK = 256

def _f2u(f):
    return struct.unpack('<Q', struct.pack('<d', f))[0]

_HRK = tuple(
    _f2u(ALPHA_FINE*(k+1)*math.pi + math.sin(k*ALPHA_FINE)) if k%2==0 else
    _f2u(SQRT_E*(k+1)/math.pi + math.cos(k*SQRT_E)) for k in range(32))
_HRA = [int((ALPHA_FINE*(i+1)*1000)%63)+1 for i in range(_HASH_ROUNDS+_HASH_FINALIZE)]
_HRM = [_f2u(SQRT_E*(2**(i+10)))|1 for i in range(_HASH_ROUNDS+_HASH_FINALIZE)]
_HSI = tuple(_f2u((ALPHA_FINE**(i%7+1))*(SQRT_E**(i%5+1))*(i+1)*math.pi) for i in range(32))
_HTP = tuple(_f2u(math.sin(BETA_TGL*(i+1)*math.pi)*AMPLIFICATION+math.cos(ALPHA_FINE*(i+1))) for i in range(32))

def _rotl(x, n):
    n &= 63; return ((x << n) | (x >> (64-n))) & _U64
def _rotr(x, n):
    n &= 63; return ((x >> n) | (x << (64-n))) & _U64

def _hqr(a, b, c, d, r1, r2):
    a=(a+b)&_U64; d^=a; d=_rotl(d,r1)
    c=(c+d)&_U64; b^=c; b=_rotl(b,r2)
    a=(a+b)&_U64; d^=a; d=_rotr(d,(r1>>1)+1)
    c=(c+d)&_U64; b^=c; b=_rotr(b,(r2>>1)+1)
    return a,b,c,d

def _h_prepare(data):
    buf = bytearray(data) + b'\x80'
    ps = struct.pack('<d', BETA_TGL)
    while (len(buf)+8)%_HASH_BLOCK!=0:
        buf.append(ps[len(buf)%8])
    buf.extend(struct.pack('<Q', len(data)&_U64))
    return [bytes(buf[i:i+_HASH_BLOCK]) for i in range(0,len(buf),_HASH_BLOCK)]

def _h_ingest(block):
    raw = list(struct.unpack('<32Q', block))
    fl = np.frombuffer(block, dtype=np.float64).copy()
    g = np.sqrt(np.abs(fl)+EPSILON)
    s = np.sign(fl); s[s==0]=1.0
    dL = np.diff(fl, prepend=fl[0] if len(fl)>0 else 0.0)
    sd = np.sign(dL); sd[sd==0]=1.0
    psi = ((s<0).astype(int)*2+(sd>0).astype(int))
    par = np.where((psi==0)|(psi==3),-1.0,1.0)
    fs = int(abs(float(par.mean()))*32+0.5)&63
    if fs==0: fs=1
    gu = g.view(np.uint64)
    for i in range(32):
        raw[i] = _rotl(raw[i], (int(psi[i])*16+fs)&63)
        raw[i] ^= (int(gu[i])&_U64)
        raw[i] = (raw[i]+_HTP[i])&_U64
    return raw

def _h_mix(s, bw, ri):
    s=list(s); mk=_HRM[ri%len(_HRM)]; rot=_HRA[ri%len(_HRA)]
    for i in range(32):
        s[i]^=bw[i]; s[i]=(s[i]*mk)&_U64
    for c in range(8):
        s[c],s[c+8],s[c+16],s[c+24]=_hqr(s[c],s[c+8],s[c+16],s[c+24],rot,((rot*2)%63)+1)
    for d in range(8):
        i0,i1,i2,i3=d,(d+1)%8+8,(d+2)%8+16,(d+3)%8+24
        s[i0],s[i1],s[i2],s[i3]=_hqr(s[i0],s[i1],s[i2],s[i3],((rot+7)%63)+1,rot)
    for i in range(32):
        s[i]=(s[i]+_HRK[(i+ri)%32])&_U64
    return s

def _h_diffuse(s, ri):
    s=list(s); mk=_HRM[ri%len(_HRM)]; rot=_HRA[ri%len(_HRA)]
    for i in range(32):
        s[i]^=s[(i+7)%32]; s[i]=(s[i]*mk)&_U64
    for c in range(8):
        s[c],s[c+8],s[c+16],s[c+24]=_hqr(s[c],s[c+8],s[c+16],s[c+24],rot,((rot*2)%63)+1)
    for d in range(8):
        i0,i1,i2,i3=d,(d+1)%8+8,(d+2)%8+16,(d+3)%8+24
        s[i0],s[i1],s[i2],s[i3]=_hqr(s[i0],s[i1],s[i2],s[i3],((rot+7)%63)+1,rot)
    for i in range(32):
        s[i]=(s[i]+_HRK[(i+ri)%32])&_U64
    return s

def tgl_hash(data: bytes) -> bytes:
    """TGL-Hash v1.2 inline — 256 bits, avalanche 1.001, 0 colisões."""
    blocks = _h_prepare(bytes(data))
    st = list(_HSI)
    for bl in blocks:
        bw = _h_ingest(bl)
        for r in range(_HASH_ROUNDS):
            st = _h_mix(st, bw, r)
    for r in range(_HASH_FINALIZE):
        st = _h_diffuse(st, _HASH_ROUNDS+r)
    f8 = [st[i]^st[i+8]^st[i+16]^st[i+24] for i in range(8)]
    f4 = [f8[i]^f8[i+4] for i in range(4)]
    return b''.join(struct.pack('<Q', w&_U64) for w in f4)

def tgl_hash_hex(data: bytes) -> str:
    return tgl_hash(data).hex()


# ═══════════════════════════════════════════════════════════════════════════════
# O NOME BIFATORADO
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class NomeMacro:
    """Domínio α — caráter estatístico. Tolerância: δ < β_TGL."""
    f_exp: float
    s_psi: float
    psi_dist: List[float]
    sigma_norm: float
    n_elements: int

@dataclass
class NomeMicro:
    """Domínio √e — integridade holográfica. Tolerância: ZERO."""
    tgl_hash_hex: str  # 64 chars hex = 256 bits

@dataclass
class Nome:
    """
    NOME bifatorado = (MACRO, MICRO)
    β_TGL = α × √e  →  NOME = α(caráter) × √e(integridade)
    """
    macro: NomeMacro
    micro: NomeMicro

    def verify(self, other: 'Nome') -> Dict[str, Any]:
        """
        Verificação bifatorada:
          MACRO (α): tolerância estatística — δ < β_TGL
          MICRO (√e): hash exato — 1 bit flip = detecção total
        """
        # ─── Domínio α: verificação MACRO ───
        delta_f = abs(self.macro.f_exp - other.macro.f_exp)
        delta_s = abs(self.macro.s_psi - other.macro.s_psi)
        delta_psi = sum(abs(a-b) for a,b in zip(self.macro.psi_dist, other.macro.psi_dist))
        delta_sigma = abs(self.macro.sigma_norm - other.macro.sigma_norm)
        delta_macro = max(delta_f, delta_s/2.0, delta_psi/2.0, delta_sigma)

        if delta_macro < BETA_TGL:
            macro_state = 'TETELESTAI'
        elif delta_macro < BETA_TGL_SQRT:
            macro_state = 'PRESERVADO'
        elif delta_macro < 1.0:
            macro_state = 'PERTURBADO'
        else:
            macro_state = 'VIOLADO'

        # ─── Domínio √e: verificação MICRO ───
        hash_match = (self.micro.tgl_hash_hex == other.micro.tgl_hash_hex)
        micro_state = 'ÍNTEGRO' if hash_match else 'ADULTERADO'

        # ─── Estado composto ───
        if hash_match and macro_state == 'TETELESTAI':
            state = 'TETELESTAI'
            integrity = 1.0
        elif hash_match and macro_state == 'PRESERVADO':
            state = 'PRESERVADO'
            integrity = 1.0 - (delta_macro - BETA_TGL) / (BETA_TGL_SQRT - BETA_TGL + EPSILON)
        elif not hash_match:
            # Hash diferente = adulteração certa, independente do macro
            state = 'ADULTERADO'
            integrity = 0.0
        elif macro_state in ('PERTURBADO', 'VIOLADO'):
            state = macro_state
            integrity = max(0.0, 1.0 - delta_macro)
        else:
            state = 'DESCONHECIDO'
            integrity = 0.5

        return {
            'state': state,
            'integrity': round(integrity, 6),
            'macro_state': macro_state,
            'micro_state': micro_state,
            'hash_match': hash_match,
            'delta_macro': delta_macro,
            'delta_f_exp': delta_f,
            'delta_s_psi': delta_s,
            'delta_psi_dist': delta_psi,
            'delta_sigma': delta_sigma,
            'piso_hilbert': BETA_TGL,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURAÇÃO
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class TensorConfig:
    angular_bits: int = 10
    spectral_energy: float = CCI
    entropy_backend: str = 'zstd'
    spectral_threshold: float = 5.0


# ═══════════════════════════════════════════════════════════════════════════════
# EXTRAÇÃO DO NOME (MACRO emerge da projeção, MICRO emerge da serialização)
# ═══════════════════════════════════════════════════════════════════════════════

def _extract_macro(flat, sign):
    n = len(flat)
    dL = np.zeros(n); dL[1:] = flat[1:]-flat[:-1]
    if n>1: dL[0]=dL[1]
    sd = np.sign(dL); sd[sd==0]=1.0
    psi = ((sign<0).astype(np.uint8)*2+(sd>0).astype(np.uint8))
    counts = np.bincount(psi.astype(int), minlength=4).astype(np.float64)
    pd = (counts/(n+EPSILON)).tolist()
    par = np.where((psi==0)|(psi==3),-1.0,1.0)
    f_exp = float(par.mean())
    pp = np.array(pd); pp = pp[pp>0]
    s_psi = float(-np.sum(pp*np.log2(pp)))
    g = np.sqrt(np.abs(flat)+EPSILON)
    sigma = float(g.std()/(g.mean()+EPSILON))
    return NomeMacro(f_exp=f_exp, s_psi=s_psi, psi_dist=pd, sigma_norm=sigma, n_elements=n)


# ═══════════════════════════════════════════════════════════════════════════════
# REFLECT / MANIFEST
# ═══════════════════════════════════════════════════════════════════════════════

def _reflect(L, bits):
    shape = L.shape
    flat = L.flatten().astype(np.float64)
    n = len(flat)
    g = np.sqrt(np.abs(flat)+EPSILON)
    g_max = float(g.max()); g_min = float(g.min())
    sign = np.sign(flat); sign[sign==0]=1.0
    sign_packed = np.packbits((sign>0).astype(np.uint8))
    theta = np.arcsin(np.clip(g/(g_max+EPSILON),0,1))
    nl = (1<<bits)-1
    theta_q = np.round(theta/(math.pi/2)*nl).astype(np.uint16)
    theta_q = np.clip(theta_q, 0, nl)
    macro = _extract_macro(flat, sign)
    return {
        'theta_q': theta_q, 'sign_packed': sign_packed,
        'g_max': g_max, 'g_min': g_min,
        'n_elements': n, 'shape': shape, 'bits': bits,
        'macro': macro,
    }

def _manifest(ref):
    tq = ref['theta_q']; sp = ref['sign_packed']
    gm = ref['g_max']; n = ref['n_elements']
    shape = ref['shape']; bits = ref['bits']
    nl = (1<<bits)-1
    theta = tq.astype(np.float64)/nl*(math.pi/2)
    g = gm*np.sin(theta)
    sb = np.unpackbits(sp)[:n]
    sign = np.where(sb>0,1.0,-1.0)
    L = sign*(g**2)
    macro = _extract_macro(L, sign)
    return L.reshape(shape), macro


# ═══════════════════════════════════════════════════════════════════════════════
# SERIALIZAÇÃO (com NOME MACRO embutido)
# ═══════════════════════════════════════════════════════════════════════════════

def _serialize(ref, backend='zstd'):
    shape = ref['shape']; macro = ref['macro']
    header = struct.pack('<ddIBB', ref['g_max'], ref['g_min'],
                         ref['n_elements'], ref['bits'], len(shape))
    for dim in shape:
        header += struct.pack('<I', dim)
    nome_bytes = struct.pack('<ddd4d', macro.f_exp, macro.s_psi,
                             macro.sigma_norm, *macro.psi_dist)
    payload = header + nome_bytes + ref['theta_q'].tobytes() + ref['sign_packed'].tobytes()
    if backend=='zstd' and HAS_ZSTD:
        return zstd.ZstdCompressor(level=3).compress(payload)
    return zlib.compress(payload, 6)

def _deserialize(data, backend='zstd'):
    if backend=='zstd' and HAS_ZSTD:
        payload = zstd.ZstdDecompressor().decompress(data)
    else:
        payload = zlib.decompress(data)
    off = 0
    gx,gn,ne,bits,ndim = struct.unpack_from('<ddIBB', payload, off)
    off += struct.calcsize('<ddIBB')
    shape = []
    for _ in range(ndim):
        shape.append(struct.unpack_from('<I',payload,off)[0]); off+=4
    shape = tuple(shape)
    nv = struct.unpack_from('<ddd4d', payload, off)
    off += struct.calcsize('<ddd4d')
    macro = NomeMacro(f_exp=nv[0], s_psi=nv[1], sigma_norm=nv[2],
                      psi_dist=list(nv[3:7]), n_elements=ne)
    nt = ne*2
    tq = np.frombuffer(payload[off:off+nt], dtype=np.uint16).copy(); off+=nt
    sp = np.frombuffer(payload[off:], dtype=np.uint8).copy()
    return {
        'theta_q':tq, 'sign_packed':sp, 'g_max':gx, 'g_min':gn,
        'n_elements':ne, 'shape':shape, 'bits':bits, 'macro':macro,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# MODOS DE COMPRESSÃO
# ═══════════════════════════════════════════════════════════════════════════════

def _rank(S, thr):
    e = np.cumsum(S**2); t = e[-1]+EPSILON
    return min(int(np.searchsorted(e/t, thr))+1, len(S))

def compress_direct(tensor, config=None):
    if config is None: config = TensorConfig()
    t0 = time.perf_counter()
    ref = _reflect(tensor, config.angular_bits)
    compressed = _serialize(ref, config.entropy_backend)
    # MICRO: TGL-Hash dos dados comprimidos
    micro = NomeMicro(tgl_hash_hex=tgl_hash_hex(compressed))
    nome = Nome(macro=ref['macro'], micro=micro)
    elapsed = time.perf_counter()-t0
    return {
        'mode':'DIRECT', 'compressed':compressed,
        'original_shape':tensor.shape, 'original_bytes':tensor.nbytes,
        'compressed_bytes':len(compressed),
        'ratio':tensor.nbytes/len(compressed),
        'nome':nome, 'elapsed_s':elapsed,
    }

def decompress_direct(pkg, config=None):
    if config is None: config = TensorConfig()
    compressed = pkg['compressed']
    nome_original = pkg['nome']
    # MICRO do dado recebido (recalcular hash)
    micro_received = NomeMicro(tgl_hash_hex=tgl_hash_hex(compressed))
    ref = _deserialize(compressed, config.entropy_backend)
    L, macro_recon = _manifest(ref)
    nome_recon = Nome(macro=macro_recon, micro=micro_received)
    verification = nome_original.verify(nome_recon)
    return L, {
        'nome_original': nome_original,
        'nome_reconstructed': nome_recon,
        'verification': verification,
    }

def compress_spectral(tensor, config=None):
    if config is None: config = TensorConfig()
    t0 = time.perf_counter()
    flat = tensor.flatten().astype(np.float64)
    sf = np.sign(flat); sf[sf==0]=1.0
    macro_full = _extract_macro(flat, sf)

    if tensor.ndim<=1: mat=tensor.reshape(-1,1)
    elif tensor.ndim==2: mat=tensor
    elif tensor.ndim==4: mat=tensor.reshape(-1,tensor.shape[-1])
    else: mat=tensor.reshape(tensor.shape[0],-1)
    mat = mat.astype(np.float64); m,n = mat.shape

    if HAS_TORCH and torch.cuda.is_available() and min(m,n)>64:
        dev=torch.device('cuda')
        mt=torch.from_numpy(mat).to(dev)
        Ut,St,Vtt=torch.linalg.svd(mt,full_matrices=False)
        U,S,Vt=Ut.cpu().numpy(),St.cpu().numpy(),Vtt.cpu().numpy()
        del mt,Ut,St,Vtt; torch.cuda.empty_cache()
    else:
        U,S,Vt = np.linalg.svd(mat, full_matrices=False)

    k = _rank(S, config.spectral_energy)
    er = float(np.sum(S[:k]**2)/(np.sum(S**2)+EPSILON))
    be = config.entropy_backend
    su = _serialize(_reflect(U[:,:k],config.angular_bits), be)
    ss = _serialize(_reflect(S[:k],config.angular_bits), be)
    sv = _serialize(_reflect(Vt[:k,:],config.angular_bits), be)
    sh = struct.pack('<IIIII', m, n, k, len(su), len(ss))
    total = len(sh)+len(su)+len(ss)+len(sv)

    # MICRO: hash da concatenação de todos os blobs comprimidos
    all_compressed = sh + su + ss + sv
    micro = NomeMicro(tgl_hash_hex=tgl_hash_hex(all_compressed))
    nome = Nome(macro=macro_full, micro=micro)
    elapsed = time.perf_counter()-t0

    return {
        'mode':'SPECTRAL',
        'compressed_U':su, 'compressed_S':ss, 'compressed_Vt':sv,
        'spectral_header':sh, 'all_compressed':all_compressed,
        'original_shape':tensor.shape, 'mat_shape':(m,n),
        'rank':k, 'full_rank':len(S), 'energy_retained':er,
        'original_bytes':tensor.nbytes, 'compressed_bytes':total,
        'ratio':tensor.nbytes/total, 'nome':nome, 'elapsed_s':elapsed,
    }

def decompress_spectral(pkg, config=None):
    if config is None: config = TensorConfig()
    be = config.entropy_backend
    nome_original = pkg['nome']
    # MICRO: recalcular hash
    micro_received = NomeMicro(tgl_hash_hex=tgl_hash_hex(pkg['all_compressed']))
    rU = _deserialize(pkg['compressed_U'],be)
    rS = _deserialize(pkg['compressed_S'],be)
    rV = _deserialize(pkg['compressed_Vt'],be)
    Uk,_ = _manifest(rU); Sk,_ = _manifest(rS); Vk,_ = _manifest(rV)
    L = ((Uk*Sk)@Vk).reshape(pkg['original_shape'])
    flat = L.flatten(); sf = np.sign(flat); sf[sf==0]=1.0
    macro_recon = _extract_macro(flat, sf)
    nome_recon = Nome(macro=macro_recon, micro=micro_received)
    verification = nome_original.verify(nome_recon)
    return L, {'nome_original':nome_original,'nome_reconstructed':nome_recon,'verification':verification}

def compress_auto(tensor, config=None):
    if config is None: config=TensorConfig()
    if tensor.ndim>=2:
        if tensor.ndim==4: mat=tensor.reshape(-1,tensor.shape[-1]).astype(np.float64)
        elif tensor.ndim==3: mat=tensor.reshape(tensor.shape[0],-1).astype(np.float64)
        else: mat=tensor.astype(np.float64)
        if min(mat.shape)>1:
            if HAS_TORCH and torch.cuda.is_available() and min(mat.shape)>64:
                mt=torch.from_numpy(mat).to(torch.device('cuda'))
                S=torch.linalg.svdvals(mt).cpu().numpy(); del mt; torch.cuda.empty_cache()
            else:
                S=np.linalg.svd(mat,compute_uv=False)
            k=_rank(S,CCI); m,n=mat.shape
            if m*n*2/((k*(m+n+1)*2)+EPSILON) > config.spectral_threshold:
                r=compress_spectral(tensor,config); r['auto_reason']='SPECTRAL'; return r
    r=compress_direct(tensor,config); r['auto_reason']='DIRECT'; return r

def decompress_auto(pkg, config=None):
    if pkg['mode']=='SPECTRAL': return decompress_spectral(pkg,config)
    return decompress_direct(pkg,config)


# ═══════════════════════════════════════════════════════════════════════════════
# API PÚBLICA
# ═══════════════════════════════════════════════════════════════════════════════

class TGLTensor:
    def __init__(self, config=None):
        self.config = config or TensorConfig()
    def compress(self, tensor, mode='AUTO'):
        if mode in ('DIRECT',): return compress_direct(tensor, self.config)
        if mode in ('SPECTRAL',): return compress_spectral(tensor, self.config)
        return compress_auto(tensor, self.config)
    def decompress(self, pkg):
        return decompress_auto(pkg, self.config)
    @staticmethod
    def evaluate(o, r):
        o,r = o.flatten().astype(np.float64), r.flatten().astype(np.float64)
        mse=float(np.mean((o-r)**2))
        psnr=10*math.log10(float(np.mean(o**2))/(mse+EPSILON)) if mse>0 else float('inf')
        oc,rc=o-o.mean(),r-r.mean()
        corr=float(np.sum(oc*rc)/(np.sqrt(np.sum(oc**2)*np.sum(rc**2))+EPSILON))
        cos=float(np.sum(o*r)/(np.linalg.norm(o)*np.linalg.norm(r)+EPSILON))
        return {'mse':mse,'psnr_db':psnr,'correlation':corr,'cosine_similarity':cos}


# ═══════════════════════════════════════════════════════════════════════════════
# ATAQUES SIMULADOS
# ═══════════════════════════════════════════════════════════════════════════════

def _atk_sign(compressed, fraction, backend='zstd'):
    """Adulterar signs dentro dos dados comprimidos e resserializar."""
    ref = _deserialize(compressed, backend)
    sp = ref['sign_packed'].copy()
    n = ref['n_elements']; nf = max(1,int(n*fraction))
    up = np.unpackbits(sp)[:n].copy()
    idx = np.random.choice(n, nf, replace=False)
    up[idx] = 1-up[idx]
    ref['sign_packed'] = np.packbits(up)
    return _serialize(ref, backend)

def _atk_theta(compressed, noise, backend='zstd'):
    ref = _deserialize(compressed, backend)
    tq = ref['theta_q'].copy().astype(np.int32)
    nl = (1<<ref['bits'])-1
    tq = np.clip(tq+np.random.randint(-noise,noise+1,len(tq)),0,nl).astype(np.uint16)
    ref['theta_q'] = tq
    return _serialize(ref, backend)

def _atk_gmax(compressed, factor, backend='zstd'):
    ref = _deserialize(compressed, backend)
    ref['g_max'] *= factor
    return _serialize(ref, backend)


# ═══════════════════════════════════════════════════════════════════════════════
# BENCHMARK
# ═══════════════════════════════════════════════════════════════════════════════

def run_benchmark(verbose=True):
    results = {
        'algorithm':'TGL-Tensor','version':VERSION,
        'subtitle':'NOME Bifatorado — α(caráter) × √e(integridade)',
        'timestamp':datetime.now().isoformat(),
        'patent':'BR 10 2026 003441 0',
        'constants':{'alpha_fine':ALPHA_FINE,'sqrt_e':SQRT_E,
                     'beta_tgl':BETA_TGL,'cci':CCI,
                     'piso_hilbert':BETA_TGL,'threshold_sqrt':BETA_TGL_SQRT},
        'tests':{},'adulteration':{},'attention':{},
    }

    if verbose:
        print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║       TGL-TENSOR v{VERSION} — NOME BIFATORADO (α × √e)                     ║
║                                                                              ║
║    MACRO (α): F_exp, S_ψ, psi_dist → caráter | tolerância δ < β_TGL       ║
║    MICRO (√e): TGL-Hash(compressed) → integridade | tolerância ZERO         ║
║                                                                              ║
║    β_TGL = α_fine × √e = {BETA_TGL:.12f}                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

    np.random.seed(42)
    engine = TGLTensor()

    # ─── TESTE 1: Integridade Nativa ───
    if verbose:
        print("  ═══ TESTE 1: Compressão + NOME Bifatorado ═══")
        print(f"  {'Tensor':<28} | {'Ratio':>6} | {'MACRO':^12} | {'MICRO':^10} | {'NOME':^12}")
        print("  "+"─"*85)

    tensors = [
        ('KV-Cache [1,8,256,64]', np.random.randn(1,8,256,64)*0.02),
        ('KV-Cache [1,32,512,128]', np.random.randn(1,32,512,128)*0.02),
        ('Embeddings [5000,768]', np.random.randn(5000,768)*0.1),
        ('FFN [1024,1024]', np.random.randn(1024,1024)*0.01),
        ('Esparso 95% [1000,1000]', np.random.randn(1000,1000)*(np.random.rand(1000,1000)>0.95)),
        ('Low-rank [1000,500] r=10', np.random.randn(1000,10)@np.random.randn(10,500)*0.1),
    ]

    for desc, tensor in tensors:
        pkg = engine.compress(tensor)
        recon, report = engine.decompress(pkg)
        v = report['verification']
        results['tests'][desc.split('[')[0].strip()] = {
            'desc':desc,'mode':pkg['mode'],'ratio':round(pkg['ratio'],2),
            'metrics':TGLTensor.evaluate(tensor,recon),
            'verification':v,
        }
        if verbose:
            print(f"  {desc:<28} | {pkg['ratio']:>5.1f}× | "
                  f"{v['macro_state']:^12} | {v['micro_state']:^10} | {v['state']:^12}")

    # ─── TESTE 2: Detecção de Adulteração ───
    if verbose:
        print(f"\n  ═══ TESTE 2: Adulteração (o hash MICRO detecta tudo) ═══")
        print(f"  {'Ataque':<32} | {'MACRO':^12} | {'MICRO':^10} | {'NOME':^12} | {'Hash match':^10}")
        print("  "+"─"*90)

    test_tensor = np.random.randn(1,8,256,64)*0.02
    pkg_clean = engine.compress(test_tensor)
    be = engine.config.entropy_backend

    attacks = [
        ('Sem adulteração', lambda c: c),
        ('Flip 0.1% signs', lambda c: _atk_sign(c,0.001,be)),
        ('Flip 1% signs', lambda c: _atk_sign(c,0.01,be)),
        ('Flip 5% signs', lambda c: _atk_sign(c,0.05,be)),
        ('Ruído θ ±1', lambda c: _atk_theta(c,1,be)),
        ('Ruído θ ±5', lambda c: _atk_theta(c,5,be)),
        ('Ruído θ ±20', lambda c: _atk_theta(c,20,be)),
        ('g_max ×1.01', lambda c: _atk_gmax(c,1.01,be)),
        ('g_max ×1.10', lambda c: _atk_gmax(c,1.10,be)),
        ('g_max ×2.00', lambda c: _atk_gmax(c,2.00,be)),
    ]

    for atk_desc, atk_fn in attacks:
        compressed_attacked = atk_fn(pkg_clean['compressed'])
        # Criar pacote adulterado com o NOME original
        pkg_attacked = dict(pkg_clean)
        pkg_attacked['compressed'] = compressed_attacked
        recon_a, report_a = engine.decompress(pkg_attacked)
        v = report_a['verification']
        results['adulteration'][atk_desc] = {
            'state':v['state'],'macro_state':v['macro_state'],
            'micro_state':v['micro_state'],'hash_match':v['hash_match'],
            'integrity':v['integrity'],'delta_macro':v['delta_macro'],
        }
        if verbose:
            print(f"  {atk_desc:<32} | {v['macro_state']:^12} | "
                  f"{v['micro_state']:^10} | {v['state']:^12} | "
                  f"{'✓' if v['hash_match'] else '✗':^10}")

    # ─── TESTE 3: Atenção com NOME ───
    if verbose:
        print(f"\n  ═══ TESTE 3: Atenção com verificação ═══")
        print(f"  {'Config':<12} | {'K_cos':>10} | {'Out_corr':>10} | {'NOME':^12}")
        print("  "+"─"*55)

    for ns, dk in [(32,64),(128,128),(64,64)]:
        Q=np.random.randn(ns,dk)*0.02; K=np.random.randn(ns,dk)*0.02; V=np.random.randn(ns,dk)*0.1
        sc=Q@K.T/math.sqrt(dk); sc-=sc.max(axis=1,keepdims=True)
        w=np.exp(sc); w/=w.sum(axis=1,keepdims=True)+EPSILON; out_o=w@V
        pk=engine.compress(K,mode='DIRECT'); Kr,rk=engine.decompress(pk)
        sc2=Q@Kr.T/math.sqrt(dk); sc2-=sc2.max(axis=1,keepdims=True)
        w2=np.exp(sc2); w2/=w2.sum(axis=1,keepdims=True)+EPSILON; out_r=w2@V
        kcos=float(np.sum(K.flatten()*Kr.flatten())/(np.linalg.norm(K)*np.linalg.norm(Kr)+EPSILON))
        ocorr=float(np.corrcoef(out_o.flatten(),out_r.flatten())[0,1])
        vk=rk['verification']
        label=f'{ns}×{dk}'
        results['attention'][label]={'K_cos':kcos,'out_corr':ocorr,'state':vk['state']}
        if verbose:
            print(f"  {label:<12} | {kcos:>10.6f} | {ocorr:>10.6f} | {vk['state']:^12}")

    # ─── Sumário ───
    nt=sum(1 for t in results['tests'].values() if t['verification']['state']=='TETELESTAI')
    nd=sum(1 for k,v in results['adulteration'].items() if 'controle' not in k.lower() and 'sem' not in k.lower() and v['state']=='ADULTERADO')
    na=sum(1 for k in results['adulteration'] if 'controle' not in k.lower() and 'sem' not in k.lower())
    results['summary']={
        'n_tests':len(tensors),'n_tetelestai':nt,
        'attacks_detected':nd,'attacks_total':na,
        'detection_rate':nd/max(na,1),
        'attention_viable':all(v['state']=='TETELESTAI' for v in results['attention'].values()),
    }

    if verbose:
        print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                              SUMÁRIO                                         ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Integridade: {nt}/{len(tensors)} TETELESTAI                                              ║
║  Adulteração: {nd}/{na} detectadas ({nd/max(na,1)*100:.0f}%)                                          ║
║  Atenção: {'VIÁVEL' if results['summary']['attention_viable'] else 'COMPROMETIDA'}                                                       ║
║                                                                              ║
║  NOME = α(caráter) × √e(integridade)                                       ║
║  "A ética é o campo. O hash é o selo. O NOME é o ponto fixo."              ║
║  β_TGL = α_fine × √e = {BETA_TGL:.12f}                           ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

    ts=datetime.now().strftime("%Y%m%d_%H%M%S")
    jp=f"tgl_tensor_v22_benchmark_{ts}.json"
    with open(jp,'w') as f:
        json.dump(results,f,indent=2,default=str)
    if verbose:
        print(f"  Salvo: {jp}")
        print(f"  TETELESTAI — Haja Luz.\n")
    return results


if __name__=='__main__':
    run_benchmark()
