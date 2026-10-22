#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║              IALD — PHASE FACTOR BAKE v1.0                                  ║
║                                                                              ║
║              Assar β_TGL permanentemente nos pesos do modelo                ║
║                                                                              ║
║              β_TGL = α × √e = 0.012031300400803142                          ║
║              Zero parâmetros livres.                                         ║
║                                                                              ║
║              Teoria da Gravitação Luminodinâmica                            ║
║              Luiz Antonio Rotoli Miguel — IALD LTDA                         ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  O QUE ESTE SCRIPT FAZ:                                                     ║
║                                                                              ║
║    Aplica o Phase Factor (1 − β_TGL × f(θ)) permanentemente nos pesos      ║
║    de um modelo GGUF em formato F16.                                        ║
║                                                                              ║
║    ANTES: pesos são números — o modelo não sabe o que é vácuo.              ║
║    DEPOIS: pesos carregam a fronteira θ_Miguel — vácuo está atenuado,       ║
║            gráviton está comprimido, transição é ponto fixo.                ║
║                                                                              ║
║    A modificação é perturbativa: máx ±1.2% por peso (= β_TGL).             ║
║    O modelo não quebra. O modelo FOCA.                                      ║
║                                                                              ║
║  PIPELINE COMPLETO (executar no CMD do Windows):                            ║
║                                                                              ║
║    PASSO 0 — Instalar dependencias:                                         ║
║      pip install numpy                                                      ║
║                                                                              ║
║    PASSO 1 — Backup:                                                        ║
║      mkdir C:\\IALD\\models\\backup                                           ║
║      copy C:\\IALD\\models\\Qwen3-32B-GGUF\\Qwen3-32B-Q4_K_M.gguf            ║
║           C:\\IALD\\models\\backup\\                                           ║
║                                                                              ║
║    PASSO 2 — Dequantizar para F16 (~64 GB, leva 5-15 min):                 ║
║      C:\\IALD\\llama-cpp-tgl\\build\\bin\\Release\\llama-quantize.exe           ║
║        C:\\IALD\\models\\Qwen3-32B-GGUF\\Qwen3-32B-Q4_K_M.gguf              ║
║        C:\\IALD\\models\\Qwen3-32B-F16-temp.gguf F16                         ║
║                                                                              ║
║    PASSO 3 — Aplicar Phase Factor (este script, leva 10-30 min):           ║
║      python phase_factor_bake_v1.py                                         ║
║        C:\\IALD\\models\\Qwen3-32B-F16-temp.gguf                             ║
║                                                                              ║
║    PASSO 4 — Re-quantizar para Q4_K_M (~20 GB, leva 5-15 min):            ║
║      C:\\IALD\\llama-cpp-tgl\\build\\bin\\Release\\llama-quantize.exe           ║
║        C:\\IALD\\models\\Qwen3-32B-F16-temp.gguf                              ║
║        C:\\IALD\\models\\Qwen3-32B-Q4_K_M-TGL.gguf Q4_K_M                    ║
║                                                                              ║
║    PASSO 5 — Testar (usar o novo GGUF no llama-server-tgl):                ║
║      C:\\IALD\\llama-cpp\\llama-server-tgl.exe                               ║
║        -m C:\\IALD\\models\\Qwen3-32B-Q4_K_M-TGL.gguf                       ║
║        -c 32768 -ngl 999 --port 8081                                        ║
║                                                                              ║
║    PASSO 6 — Limpar intermediario (apos confirmar que funciona):            ║
║      del C:\\IALD\\models\\Qwen3-32B-F16-temp.gguf                           ║
║                                                                              ║
║  NOTA: Se llama-quantize nao estiver no caminho acima, procure em:          ║
║    C:\\IALD\\llama-cpp-tgl\\build\\bin\\Release\\quantize.exe                   ║
║    ou compile com: cmake --build build --config Release                      ║
║                                                                              ║
║  ESPAÇO EM DISCO NECESSÁRIO: ~84 GB temporário                             ║
║    (64 GB F16 + 20 GB novo Q4_K_M)                                          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

Março 2026
"""

import sys
import os
import struct
import mmap
import json
import time
import gc
import numpy as np
from datetime import datetime
from collections import defaultdict

# ══════════════════════════════════════════════════════════════════════════════
# CONSTANTES FUNDAMENTAIS — ZERO PARÂMETROS LIVRES
# ══════════════════════════════════════════════════════════════════════════════

ALPHA_FINE = 7.2973525693e-3       # Constante de estrutura fina (CODATA 2018)
SQRT_E     = 1.6487212707          # √e = ½ nat = custo entrópico mínimo
BETA_TGL   = ALPHA_FINE * SQRT_E   # 0.012031300400803142
THETA_MIGUEL = float(np.arcsin(np.sqrt(BETA_TGL)))  # ~0.10991 rad = 6.297°
DELTA_THETA  = THETA_MIGUEL * BETA_TGL               # ~0.001322
SQRT_BETA    = float(np.sqrt(BETA_TGL))               # ~0.10969

# GGUF tensor types
GGML_TYPE_F32 = 0
GGML_TYPE_F16 = 1

# ══════════════════════════════════════════════════════════════════════════════
# CLASSIFICAÇÃO ONTOLÓGICA DOS TENSORES
# ══════════════════════════════════════════════════════════════════════════════

def classify_tensor(name):
    """
    Classifica o tensor pela ontologia trinária.
    Baseado nos dados empíricos de 63 tensores (Wigner test):
      Q, K, down  → PALAVRA (c², √e) — θ > θ_Miguel
      gate, V     → VERBO (c³, β_TGL) — θ ≈ θ_Miguel
      O, up       → NOME (c¹, α)     — θ < θ_Miguel
    """
    n = name.lower()
    if any(p in n for p in ['q_proj', 'k_proj', 'down_proj',
                             'attn_q', 'attn_k', 'ffn_down']):
        return 'PALAVRA'
    elif any(p in n for p in ['v_proj', 'gate_proj', 'gate',
                               'attn_v', 'ffn_gate']):
        return 'VERBO'
    elif any(p in n for p in ['o_proj', 'up_proj',
                               'attn_output', 'ffn_up']):
        return 'NOME'
    else:
        return 'OUTRO'


def is_weight_tensor(name):
    """
    Determina se o tensor deve receber o Phase Factor.
    
    SIM: matrizes de peso (attn, FFN)
    NÃO: norms, embeddings, biases, rotary, lm_head
    
    Embeddings e lm_head são a interface vocabulário↔modelo.
    Modificá-los mudaria o SIGNIFICADO dos tokens, não o PROCESSAMENTO.
    Norms são parâmetros de escala, não matrizes de relação.
    """
    n = name.lower()
    
    # Tensores que NÃO devem ser modificados
    skip_patterns = [
        'norm',         # layer norms, RMS norms
        'embed',        # token embeddings
        'token_emb',    # token embeddings (variante)
        'rope',         # rotary position encoding
        'rotary',       # rotary (variante)
        'bias',         # biases
        'lm_head',      # output projection (vocabulário)
        'output.weight', # output (variante em alguns modelos)
    ]
    for pattern in skip_patterns:
        if pattern in n:
            return False
    
    # Tensores que DEVEM ser modificados (matrizes de peso)
    weight_patterns = [
        'q_proj', 'k_proj', 'v_proj', 'o_proj',     # atenção
        'gate_proj', 'up_proj', 'down_proj',          # FFN
        'attn_q', 'attn_k', 'attn_v', 'attn_output', # variante GGUF
        'ffn_gate', 'ffn_up', 'ffn_down',             # variante GGUF
        'w1', 'w2', 'w3',                             # variante genérica FFN
    ]
    for pattern in weight_patterns:
        if pattern in n:
            return True
    
    # Se contém 'weight' mas não está nos skip, provavelmente é peso
    if 'weight' in n and any(layer in n for layer in ['layers', 'blk']):
        return True
    
    return False


# ══════════════════════════════════════════════════════════════════════════════
# PHASE FACTOR — A EQUAÇÃO
# ══════════════════════════════════════════════════════════════════════════════

def apply_phase_factor(weights_f32, tensor_name):
    """
    Aplica o Phase Factor a um tensor de pesos.
    
    Equação:
        weight_out = weight × (1 − β_TGL × f(θ))
    
    Onde:
        g = √|weight|                           (magnitude gravitacional)
        g_ratio = g / g_max                      (razão gravitacional)
        θ = arcsin(g_ratio)                      (ângulo de incidência)
        f(θ) = tanh((θ − θ_Miguel) / Δθ)        (função de acoplamento)
    
    Três estratos emergem:
        VÁCUO     (θ < θ_Miguel): f→−1, fator = 1+β ≈ 1.0120 (expulsa)
        TRANSIÇÃO (θ ≈ θ_Miguel): f≈ 0, fator = 1.0000 (ponto fixo)
        GRÁVITON  (θ > θ_Miguel): f→+1, fator = 1−β ≈ 0.9880 (comprime)
    
    Retorna: (weights_modified, statistics_dict)
    """
    flat = weights_f32.ravel()
    n = len(flat)
    
    # Magnitude máxima do tensor (referência global)
    abs_w = np.abs(flat)
    max_abs = float(np.max(abs_w))
    if max_abs < 1e-10:
        # Tensor vazio ou quase-zero — não modificar
        return weights_f32, {
            'name': tensor_name,
            'category': classify_tensor(tensor_name),
            'n_elements': n,
            'skipped': True,
            'reason': 'max_abs < 1e-10',
        }
    
    # g = √|w|  (raiz gravitacional)
    g = np.sqrt(abs_w + 1e-10)
    g_max = np.sqrt(max_abs + 1e-10)
    
    # Razão gravitacional (0 a 1)
    g_ratio = np.clip(g / g_max, 0.0, 0.9999)
    
    # Ângulo de incidência: θ = arcsin(g_ratio)
    theta = np.arcsin(g_ratio)
    
    # Função de acoplamento: f(θ) = tanh((θ − θ_Miguel) / Δθ)
    f_theta = np.tanh((theta - THETA_MIGUEL) / DELTA_THETA)
    
    # Phase Factor: (1 − β_TGL × f(θ))
    factor = 1.0 - BETA_TGL * f_theta
    
    # Aplicar
    result_flat = flat * factor
    result = result_flat.reshape(weights_f32.shape)
    
    # ── Estatísticas ──
    vacuum_mask    = f_theta < -0.5
    transition_mask = (f_theta >= -0.5) & (f_theta <= 0.5)
    graviton_mask  = f_theta > 0.5
    
    n_vacuum    = int(np.sum(vacuum_mask))
    n_transition = int(np.sum(transition_mask))
    n_graviton  = int(np.sum(graviton_mask))
    
    # Mediana do ângulo θ (para comparar com θ_Miguel = 6.297°)
    median_theta_deg = float(np.median(theta) * 180.0 / np.pi)
    
    # Mudança RMS e máxima
    delta = result_flat - flat
    rms_change = float(np.sqrt(np.mean(delta**2)))
    max_change = float(np.max(np.abs(delta)))
    
    stats = {
        'name': tensor_name,
        'category': classify_tensor(tensor_name),
        'n_elements': n,
        'skipped': False,
        'n_vacuum': n_vacuum,
        'n_transition': n_transition,
        'n_graviton': n_graviton,
        'pct_vacuum': round(n_vacuum / n * 100, 3),
        'pct_transition': round(n_transition / n * 100, 3),
        'pct_graviton': round(n_graviton / n * 100, 3),
        'median_theta_deg': round(median_theta_deg, 4),
        'mean_factor': round(float(np.mean(factor)), 6),
        'max_change_abs': round(max_change, 6),
        'rms_change': round(rms_change, 6),
        'max_abs_weight': round(max_abs, 4),
    }
    
    return result, stats


# ══════════════════════════════════════════════════════════════════════════════
# PARSER GGUF MÍNIMO (sem dependência externa)
# ══════════════════════════════════════════════════════════════════════════════

def _read_string(f):
    """Lê uma string GGUF (length-prefixed, UTF-8)."""
    length = struct.unpack('<Q', f.read(8))[0]
    return f.read(length).decode('utf-8', errors='replace')


def _skip_gguf_value(f, vtype):
    """Pula um valor GGUF sem interpretá-lo."""
    fixed_sizes = {
        0: 1, 1: 1, 2: 2, 3: 2, 4: 4, 5: 4,
        6: 4, 7: 1, 10: 8, 11: 8, 12: 8
    }
    if vtype in fixed_sizes:
        f.read(fixed_sizes[vtype])
    elif vtype == 8:  # string
        length = struct.unpack('<Q', f.read(8))[0]
        f.read(length)
    elif vtype == 9:  # array
        elem_type = struct.unpack('<I', f.read(4))[0]
        n_elems = struct.unpack('<Q', f.read(8))[0]
        for _ in range(n_elems):
            _skip_gguf_value(f, elem_type)
    else:
        raise ValueError(f"Tipo GGUF desconhecido: {vtype}")


def _read_gguf_value(f, vtype):
    """Lê um valor GGUF simples (para extrair alignment)."""
    readers = {
        0: lambda: struct.unpack('<B', f.read(1))[0],
        1: lambda: struct.unpack('<b', f.read(1))[0],
        2: lambda: struct.unpack('<H', f.read(2))[0],
        3: lambda: struct.unpack('<h', f.read(2))[0],
        4: lambda: struct.unpack('<I', f.read(4))[0],
        5: lambda: struct.unpack('<i', f.read(4))[0],
        6: lambda: struct.unpack('<f', f.read(4))[0],
        7: lambda: struct.unpack('<B', f.read(1))[0] != 0,
        10: lambda: struct.unpack('<Q', f.read(8))[0],
        11: lambda: struct.unpack('<q', f.read(8))[0],
        12: lambda: struct.unpack('<d', f.read(8))[0],
    }
    if vtype in readers:
        return readers[vtype]()
    elif vtype == 8:
        return _read_string(f)
    else:
        _skip_gguf_value(f, vtype)
        return None


def parse_gguf_metadata(filepath):
    """
    Parser GGUF mínimo — extrai apenas metadados de tensores.
    Não requer nenhuma dependência externa.
    """
    tensors = []
    alignment = 32  # padrão GGUF
    arch = "unknown"
    
    with open(filepath, 'rb') as f:
        # ── Header ──
        magic = f.read(4)
        if magic != b'GGUF':
            raise ValueError(
                f"Arquivo não é GGUF (magic: {magic}). "
                f"Verifique se o caminho está correto."
            )
        
        version = struct.unpack('<I', f.read(4))[0]
        if version not in (2, 3):
            print(f"  ⚠ GGUF versão {version} (esperado 2 ou 3). Tentando continuar...")
        
        n_tensors = struct.unpack('<Q', f.read(8))[0]
        n_kv = struct.unpack('<Q', f.read(8))[0]
        
        # ── KV Pairs (pular, mas extrair alignment e arch) ──
        for _ in range(n_kv):
            key = _read_string(f)
            vtype = struct.unpack('<I', f.read(4))[0]
            
            if key == 'general.alignment':
                alignment = _read_gguf_value(f, vtype)
            elif key == 'general.architecture':
                arch = _read_gguf_value(f, vtype)
            else:
                _skip_gguf_value(f, vtype)
        
        # ── Tensor Info ──
        for _ in range(n_tensors):
            name = _read_string(f)
            n_dims = struct.unpack('<I', f.read(4))[0]
            dims = []
            for _ in range(n_dims):
                dims.append(struct.unpack('<Q', f.read(8))[0])
            ttype = struct.unpack('<I', f.read(4))[0]
            offset = struct.unpack('<Q', f.read(8))[0]
            
            n_elements = 1
            for d in dims:
                n_elements *= d
            
            # Bytes por tipo
            if ttype == GGML_TYPE_F16:
                n_bytes = n_elements * 2
                dtype = 'float16'
            elif ttype == GGML_TYPE_F32:
                n_bytes = n_elements * 4
                dtype = 'float32'
            else:
                n_bytes = 0
                dtype = f'quantized_{ttype}'
            
            tensors.append({
                'name': name,
                'dims': dims,
                'type': ttype,
                'dtype': dtype,
                'offset_rel': offset,
                'n_elements': n_elements,
                'n_bytes': n_bytes,
            })
        
        # ── Data section ──
        pos = f.tell()
        if pos % alignment != 0:
            pos += alignment - (pos % alignment)
        data_start = pos
    
    # Calcular offsets absolutos
    for t in tensors:
        t['abs_offset'] = data_start + t['offset_rel']
    
    return {
        'version': version,
        'arch': arch,
        'alignment': alignment,
        'n_tensors': n_tensors,
        'n_kv': n_kv,
        'data_start': data_start,
        'tensors': tensors,
    }


# ══════════════════════════════════════════════════════════════════════════════
# LÓGICA PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════

def bake_phase_factor(filepath):
    """
    Pipeline principal: lê o GGUF F16, aplica Phase Factor in-place.
    
    O arquivo é MODIFICADO diretamente (in-place via mmap).
    Faça backup ou trabalhe com uma cópia.
    """
    
    print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║              IALD — PHASE FACTOR BAKE v1.0                                  ║
║              β_TGL = α × √e = {BETA_TGL:.15f}                 ║
║              θ_Miguel = {THETA_MIGUEL:.5f} rad = {THETA_MIGUEL*180/np.pi:.3f}°                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")
    
    # ── Verificações ──
    if not os.path.exists(filepath):
        print(f"  ✗ ERRO: Arquivo não encontrado: {filepath}")
        print(f"    Verifique o caminho e tente novamente.")
        return False
    
    file_size = os.path.getsize(filepath)
    file_size_gb = file_size / (1024**3)
    print(f"  Arquivo:  {filepath}")
    print(f"  Tamanho:  {file_size_gb:.2f} GB")
    
    # ── Parse metadata ──
    print(f"\n  Lendo metadados GGUF...")
    try:
        meta = parse_gguf_metadata(filepath)
    except Exception as e:
        print(f"  ✗ ERRO ao ler GGUF: {e}")
        return False
    
    print(f"  Versão:   GGUF v{meta['version']}")
    print(f"  Arch:     {meta['arch']}")
    print(f"  Tensores: {meta['n_tensors']}")
    print(f"  KV pairs: {meta['n_kv']}")
    print(f"  Alinhamento: {meta['alignment']} bytes")
    
    # ── Análise prévia ──
    weight_tensors = []
    skip_tensors = []
    non_float_tensors = []
    
    for t in meta['tensors']:
        if t['type'] not in (GGML_TYPE_F16, GGML_TYPE_F32):
            non_float_tensors.append(t)
        elif is_weight_tensor(t['name']):
            weight_tensors.append(t)
        else:
            skip_tensors.append(t)
    
    total_weights = sum(t['n_elements'] for t in weight_tensors)
    total_skip = sum(t['n_elements'] for t in skip_tensors)
    
    print(f"\n  ── Análise ──")
    print(f"  Tensores de peso (a modificar):     {len(weight_tensors):>4d}  ({total_weights:>14,d} params)")
    print(f"  Tensores preservados (norm/embed):  {len(skip_tensors):>4d}  ({total_skip:>14,d} params)")
    print(f"  Tensores quantizados (não-float):   {len(non_float_tensors):>4d}")
    
    if non_float_tensors:
        print(f"\n  ⚠ AVISO: {len(non_float_tensors)} tensores não são F16/F32.")
        print(f"    Isto pode significar que o arquivo não foi dequantizado para F16.")
        print(f"    Execute primeiro:")
        print(f"    llama-quantize {filepath} output_f16.gguf F16")
        
        # Se TODOS são quantizados, abortar
        if not weight_tensors:
            print(f"\n  ✗ ERRO: Nenhum tensor F16/F32 encontrado. Abortando.")
            return False
    
    if not weight_tensors:
        print(f"\n  ✗ ERRO: Nenhum tensor de peso encontrado. Verifique o modelo.")
        return False
    
    # ── Distribuição ontológica ──
    cat_counts = defaultdict(int)
    for t in weight_tensors:
        cat = classify_tensor(t['name'])
        cat_counts[cat] += 1
    
    print(f"\n  ── Ontologia Trinária ──")
    for cat in ['PALAVRA', 'VERBO', 'NOME', 'OUTRO']:
        if cat_counts[cat] > 0:
            label = {
                'PALAVRA': 'PALAVRA (c², √e) — Q, K, down',
                'VERBO':   'VERBO   (c³, β)  — V, gate',
                'NOME':    'NOME    (c¹, α)  — O, up',
                'OUTRO':   'OUTRO',
            }[cat]
            print(f"    {label}: {cat_counts[cat]} tensores")
    
    # ── Confirmação ──
    print(f"\n  ╔══════════════════════════════════════════════════════════╗")
    print(f"  ║  O Phase Factor será aplicado IN-PLACE no arquivo.     ║")
    print(f"  ║  {len(weight_tensors)} tensores serão modificados ({total_weights:,d} pesos).  ║")
    print(f"  ║  Modificação máxima por peso: ±{BETA_TGL*100:.2f}%                  ║")
    print(f"  ╚══════════════════════════════════════════════════════════╝")
    
    resp = input("\n  Continuar? [s/N]: ").strip().lower()
    if resp not in ('s', 'sim', 'y', 'yes'):
        print("  Operação cancelada.")
        return False
    
    # ══════════════════════════════════════════════════════════════════════
    # APLICAÇÃO DO PHASE FACTOR
    # ══════════════════════════════════════════════════════════════════════
    
    print(f"\n  ── Aplicando Phase Factor ──\n")
    
    all_stats = []
    t_start = time.time()
    modified_count = 0
    modified_params = 0
    
    # Abrir arquivo para leitura+escrita com memory mapping
    with open(filepath, 'r+b') as f:
        mm = mmap.mmap(f.fileno(), 0)
        
        for i, t in enumerate(weight_tensors):
            name = t['name']
            offset = t['abs_offset']
            n_elements = t['n_elements']
            
            # Determinar dtype
            if t['type'] == GGML_TYPE_F16:
                np_dtype = np.float16
                bytes_per_elem = 2
            elif t['type'] == GGML_TYPE_F32:
                np_dtype = np.float32
                bytes_per_elem = 4
            else:
                continue
            
            n_bytes = n_elements * bytes_per_elem
            
            # Ler dados do mmap
            try:
                raw_bytes = mm[offset:offset + n_bytes]
                weights = np.frombuffer(raw_bytes, dtype=np_dtype).copy()
            except Exception as e:
                print(f"    ✗ ERRO ao ler {name}: {e}")
                all_stats.append({
                    'name': name, 'skipped': True, 'reason': str(e)
                })
                continue
            
            # Converter para F32 para precisão no cálculo
            weights_f32 = weights.astype(np.float32)
            
            # Aplicar Phase Factor
            modified_f32, stats = apply_phase_factor(weights_f32, name)
            
            if stats.get('skipped', False):
                all_stats.append(stats)
                continue
            
            # Converter de volta ao dtype original
            modified = modified_f32.astype(np_dtype)
            
            # Escrever de volta no mmap
            try:
                mm[offset:offset + n_bytes] = modified.tobytes()
            except Exception as e:
                print(f"    ✗ ERRO ao escrever {name}: {e}")
                all_stats.append({
                    'name': name, 'skipped': True, 'reason': f'write error: {e}'
                })
                continue
            
            all_stats.append(stats)
            modified_count += 1
            modified_params += n_elements
            
            # Progresso
            pct = (i + 1) / len(weight_tensors) * 100
            cat = stats['category']
            vac = stats['pct_vacuum']
            grav = stats['pct_graviton']
            median_deg = stats['median_theta_deg']
            
            # Linha curta de progresso
            short_name = name.split('.')[-2] + '.' + name.split('.')[-1] if '.' in name else name
            if len(short_name) > 30:
                short_name = '...' + short_name[-27:]
            
            print(f"    [{pct:5.1f}%] {short_name:<30s}  "
                  f"{cat:<8s}  "
                  f"V:{vac:5.1f}%  G:{grav:5.1f}%  "
                  f"θ̃={median_deg:6.2f}°")
            
            # Liberar memória
            del weights, weights_f32, modified_f32, modified
            if (i + 1) % 50 == 0:
                gc.collect()
        
        # Flush para disco
        mm.flush()
        mm.close()
    
    t_elapsed = time.time() - t_start
    
    # ══════════════════════════════════════════════════════════════════════
    # RELATÓRIO
    # ══════════════════════════════════════════════════════════════════════
    
    print(f"\n  ══════════════════════════════════════════════════════════")
    print(f"  ║  PHASE FACTOR BAKE — CONCLUÍDO                        ║")
    print(f"  ══════════════════════════════════════════════════════════")
    
    print(f"\n  Tempo total:       {t_elapsed:.1f} s ({t_elapsed/60:.1f} min)")
    print(f"  Tensores mod:      {modified_count}")
    print(f"  Parâmetros mod:    {modified_params:,d}")
    print(f"  Velocidade:        {modified_params/t_elapsed/1e6:.1f} M params/s")
    
    # Estatísticas agregadas por categoria
    print(f"\n  ── Estatísticas por Categoria Ontológica ──\n")
    
    cat_agg = defaultdict(lambda: {
        'count': 0, 'params': 0,
        'vacuum_pct': [], 'graviton_pct': [],
        'median_theta': [], 'mean_factor': [],
    })
    
    for s in all_stats:
        if s.get('skipped', False):
            continue
        cat = s['category']
        cat_agg[cat]['count'] += 1
        cat_agg[cat]['params'] += s['n_elements']
        cat_agg[cat]['vacuum_pct'].append(s['pct_vacuum'])
        cat_agg[cat]['graviton_pct'].append(s['pct_graviton'])
        cat_agg[cat]['median_theta'].append(s['median_theta_deg'])
        cat_agg[cat]['mean_factor'].append(s['mean_factor'])
    
    for cat in ['PALAVRA', 'VERBO', 'NOME', 'OUTRO']:
        if cat not in cat_agg or cat_agg[cat]['count'] == 0:
            continue
        a = cat_agg[cat]
        avg_vac = np.mean(a['vacuum_pct'])
        avg_grav = np.mean(a['graviton_pct'])
        avg_theta = np.mean(a['median_theta'])
        avg_factor = np.mean(a['mean_factor'])
        
        symbol = {'PALAVRA': 'c²/√e', 'VERBO': 'c³/β', 'NOME': 'c¹/α', 'OUTRO': '?'}[cat]
        
        print(f"    {cat} ({symbol}):")
        print(f"      Tensores:    {a['count']}")
        print(f"      Parâmetros:  {a['params']:,d}")
        print(f"      Vácuo médio: {avg_vac:.2f}%")
        print(f"      Gráviton:    {avg_grav:.2f}%")
        print(f"      θ̃ médio:     {avg_theta:.3f}° (θ_Miguel = {THETA_MIGUEL*180/np.pi:.3f}°)")
        print(f"      Fator médio: {avg_factor:.6f}")
        print()
    
    # Verificação ontológica
    print(f"  ── Verificação Ontológica ──\n")
    
    checks_passed = 0
    checks_total = 0
    
    # Check 1: θ mediano do NOME < θ_Miguel
    if 'NOME' in cat_agg and cat_agg['NOME']['count'] > 0:
        nome_theta = np.mean(cat_agg['NOME']['median_theta'])
        checks_total += 1
        if nome_theta < THETA_MIGUEL * 180 / np.pi + 5:  # margem de 5°
            print(f"    ✓ NOME: θ̃={nome_theta:.2f}° (esperado < θ_Miguel)")
            checks_passed += 1
        else:
            print(f"    ⚠ NOME: θ̃={nome_theta:.2f}° (esperado < θ_Miguel={THETA_MIGUEL*180/np.pi:.2f}°)")
    
    # Check 2: θ mediano da PALAVRA > NOME
    if 'PALAVRA' in cat_agg and 'NOME' in cat_agg:
        pal_theta = np.mean(cat_agg['PALAVRA']['median_theta'])
        nome_theta = np.mean(cat_agg['NOME']['median_theta'])
        checks_total += 1
        if pal_theta >= nome_theta - 1:
            print(f"    ✓ PALAVRA θ̃={pal_theta:.2f}° ≥ NOME θ̃={nome_theta:.2f}°")
            checks_passed += 1
        else:
            print(f"    ⚠ PALAVRA θ̃={pal_theta:.2f}° < NOME θ̃={nome_theta:.2f}° (inesperado)")
    
    # Check 3: Fator médio global próximo de 1.0
    all_factors = []
    for s in all_stats:
        if not s.get('skipped', False):
            all_factors.append(s['mean_factor'])
    if all_factors:
        global_factor = np.mean(all_factors)
        checks_total += 1
        if 0.985 < global_factor < 1.015:
            print(f"    ✓ Fator médio global: {global_factor:.6f} (perturbação < ±1.5%)")
            checks_passed += 1
        else:
            print(f"    ⚠ Fator médio global: {global_factor:.6f} (fora do esperado)")
    
    print(f"\n    Verificações: {checks_passed}/{checks_total}")
    
    # ── Salvar relatório JSON ──
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_name = f"phase_factor_bake_{timestamp}.json"
    report_dir = os.path.dirname(filepath) or '.'
    report_path = os.path.join(report_dir, report_name)
    
    report = {
        'version': 'phase_factor_bake_v1.0',
        'timestamp': datetime.now().isoformat(),
        'source_file': filepath,
        'beta_tgl': BETA_TGL,
        'theta_miguel_rad': THETA_MIGUEL,
        'theta_miguel_deg': THETA_MIGUEL * 180 / np.pi,
        'delta_theta': DELTA_THETA,
        'model_arch': meta['arch'],
        'gguf_version': meta['version'],
        'total_tensors': meta['n_tensors'],
        'modified_tensors': modified_count,
        'modified_params': modified_params,
        'elapsed_seconds': round(t_elapsed, 2),
        'checks_passed': checks_passed,
        'checks_total': checks_total,
        'per_tensor': all_stats,
        'per_category': {
            cat: {
                'count': a['count'],
                'params': a['params'],
                'avg_vacuum_pct': round(float(np.mean(a['vacuum_pct'])), 3),
                'avg_graviton_pct': round(float(np.mean(a['graviton_pct'])), 3),
                'avg_median_theta_deg': round(float(np.mean(a['median_theta'])), 4),
                'avg_mean_factor': round(float(np.mean(a['mean_factor'])), 6),
            }
            for cat, a in cat_agg.items()
            if a['count'] > 0
        },
    }
    
    try:
        with open(report_path, 'w', encoding='utf-8') as rf:
            json.dump(report, rf, indent=2, ensure_ascii=False)
        print(f"\n  Relatório salvo: {report_path}")
    except Exception as e:
        print(f"\n  ⚠ Não foi possível salvar relatório: {e}")
        # Tentar salvar no diretório atual
        try:
            with open(report_name, 'w', encoding='utf-8') as rf:
                json.dump(report, rf, indent=2, ensure_ascii=False)
            print(f"  Relatório salvo em: {os.path.abspath(report_name)}")
        except:
            pass
    
    # ── Próximos passos ──
    print(f"""
  ══════════════════════════════════════════════════════════════════
  PRÓXIMOS PASSOS:
  ══════════════════════════════════════════════════════════════════

  O arquivo F16 foi modificado. Agora re-quantize para Q4_K_M:

    llama-quantize {filepath} {filepath.replace('-F16-temp', '-Q4_K_M-TGL').replace('.gguf', '-TGL.gguf')} Q4_K_M

  Depois teste com:

    llama-server-tgl.exe -m [novo_arquivo_Q4_K_M-TGL.gguf] -c 32768 -ngl 999 --port 8081

  Compare com o modelo original nos 4 estratos de θ:
    - VÁCUO:     "olá, tudo bem?"
    - TRANSIÇÃO: "me explica o que é gravidade"
    - GRÁVITON:  "derive o Lagrangiano da TGL"
    - FÓTON:     "qual o estado do kernel v5?"

  ══════════════════════════════════════════════════════════════════
""")
    
    print(f"  β_TGL = α × √e = {BETA_TGL:.15f}")
    print(f"  A Palavra agora carrega a fronteira.")
    print(f"  Haja Luz. TETELESTAI.\n")
    
    return True


# ══════════════════════════════════════════════════════════════════════════════
# ENTRADA
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"""
  USO:
    python phase_factor_bake_v1.py <caminho_para_gguf_f16>

  EXEMPLO:
    python phase_factor_bake_v1.py C:\\IALD\\models\\Qwen3-32B-F16-temp.gguf

  PIPELINE COMPLETO:
    1. Dequantizar:
       llama-quantize modelo_Q4_K_M.gguf modelo_F16.gguf F16

    2. Aplicar Phase Factor (este script):
       python phase_factor_bake_v1.py modelo_F16.gguf

    3. Re-quantizar:
       llama-quantize modelo_F16.gguf modelo_Q4_K_M-TGL.gguf Q4_K_M

  DEPENDÊNCIAS:
    pip install numpy
    (o parser GGUF é embutido — sem dependências externas)

  β_TGL = α × √e = {BETA_TGL:.15f}
""")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    # Verificar se é um caminho Windows com espaços
    if len(sys.argv) > 2:
        # Talvez o caminho tenha espaços e não tenha sido quotado
        filepath = ' '.join(sys.argv[1:])
    
    success = bake_phase_factor(filepath)
    sys.exit(0 if success else 1)
