#!/usr/bin/env python3
"""
Phase Factor Bake — Mark 4 (Qwen3.5-122B-A10B MoE)
=====================================================
Applies beta_TGL x f(theta) to ALL F16 weight tensors in the 122B GGUF.

Architecture: 48 blocks (36 SSM + 12 Full Attention), 256 MoE experts/block.
Operates IN-PLACE on the F16 GGUF (~233 GB). Does NOT copy the file.
Includes checkpoint/resume — if the process crashes, re-run and it
continues from where it stopped.

Ontology mapping for MoE:
  PALAVRA (c2): attn_q, attn_k, attn_qkv, ffn_down_exps, ffn_down_shexp
  VERBO  (c3): attn_v, attn_gate, ffn_gate_exps, ffn_gate_shexp
  NOME   (c1): attn_output, ssm_out, ffn_up_exps, ffn_up_shexp
  SSM:         ssm_alpha, ssm_beta

Usage:
    python phase_factor_bake_mk4.py
    python phase_factor_bake_mk4.py C:\\IALD\\models\\Qwen3.5-122B-F16-temp.gguf

Requirements:
    pip install numpy

Author: IALD LTDA
beta_TGL = alpha x sqrt(e) = 0.012031300400803142
"""

import os
import sys
import math
import json
import struct
import time
import gc
import numpy as np
from datetime import datetime

# ======================================================================
# FUNDAMENTAL CONSTANTS (computed, NEVER hardcoded)
# ======================================================================

ALPHA_FINE = 7.2973525693e-3
SQRT_E = math.sqrt(math.e)
BETA_TGL = ALPHA_FINE * SQRT_E            # 0.012031300400803142
THETA_MIGUEL = math.asin(math.sqrt(BETA_TGL))  # ~6.297 deg
DELTA_THETA = THETA_MIGUEL * BETA_TGL     # transition width
EPS = 1e-10

# ======================================================================
# PATHS
# ======================================================================

DEFAULT_SOURCE = r"C:\IALD\models\Qwen3.5-122B-F16-temp.gguf"

# ======================================================================
# GGUF PARSER (minimal, F16 only — proven in v3 bake)
# ======================================================================

GGUF_MAGIC = 0x46554747  # "GGUF" in little-endian
GGML_TYPE_F16 = 1
GGML_TYPE_F32 = 0

# GGUF value types
GGUF_TYPE_UINT8   = 0
GGUF_TYPE_INT8    = 1
GGUF_TYPE_UINT16  = 2
GGUF_TYPE_INT16   = 3
GGUF_TYPE_UINT32  = 4
GGUF_TYPE_INT32   = 5
GGUF_TYPE_FLOAT32 = 6
GGUF_TYPE_BOOL    = 7
GGUF_TYPE_STRING  = 8
GGUF_TYPE_ARRAY   = 9
GGUF_TYPE_UINT64  = 10
GGUF_TYPE_INT64   = 11
GGUF_TYPE_FLOAT64 = 12


class GGUFReader:
    """Minimal GGUF reader for F16 tensor manipulation."""

    def __init__(self, filepath):
        self.filepath = filepath
        self.tensors = {}  # name -> {shape, type, offset, n_elements}
        self.data_offset = 0
        self._parse_header()

    def _read_string(self, f):
        length = struct.unpack("<Q", f.read(8))[0]
        return f.read(length).decode("utf-8")

    def _read_value(self, f, vtype):
        if vtype == GGUF_TYPE_UINT8:
            return struct.unpack("<B", f.read(1))[0]
        elif vtype == GGUF_TYPE_INT8:
            return struct.unpack("<b", f.read(1))[0]
        elif vtype == GGUF_TYPE_UINT16:
            return struct.unpack("<H", f.read(2))[0]
        elif vtype == GGUF_TYPE_INT16:
            return struct.unpack("<h", f.read(2))[0]
        elif vtype == GGUF_TYPE_UINT32:
            return struct.unpack("<I", f.read(4))[0]
        elif vtype == GGUF_TYPE_INT32:
            return struct.unpack("<i", f.read(4))[0]
        elif vtype == GGUF_TYPE_FLOAT32:
            return struct.unpack("<f", f.read(4))[0]
        elif vtype == GGUF_TYPE_BOOL:
            return struct.unpack("<?", f.read(1))[0]
        elif vtype == GGUF_TYPE_STRING:
            return self._read_string(f)
        elif vtype == GGUF_TYPE_UINT64:
            return struct.unpack("<Q", f.read(8))[0]
        elif vtype == GGUF_TYPE_INT64:
            return struct.unpack("<q", f.read(8))[0]
        elif vtype == GGUF_TYPE_FLOAT64:
            return struct.unpack("<d", f.read(8))[0]
        elif vtype == GGUF_TYPE_ARRAY:
            elem_type = struct.unpack("<I", f.read(4))[0]
            count = struct.unpack("<Q", f.read(8))[0]
            return [self._read_value(f, elem_type) for _ in range(count)]
        else:
            raise ValueError(f"Unknown GGUF value type: {vtype}")

    def _parse_header(self):
        file_gb = os.path.getsize(self.filepath) / 1e9
        print(f"  Parsing GGUF header ({file_gb:.1f} GB)...")
        t0 = time.time()

        with open(self.filepath, "rb") as f:
            magic = struct.unpack("<I", f.read(4))[0]
            if magic != GGUF_MAGIC:
                raise ValueError(f"Not a GGUF file (magic: {magic:#x})")

            version = struct.unpack("<I", f.read(4))[0]
            if version not in (2, 3):
                raise ValueError(f"Unsupported GGUF version: {version}")

            n_tensors = struct.unpack("<Q", f.read(8))[0]
            n_kv = struct.unpack("<Q", f.read(8))[0]

            print(f"  Version: {version}, Tensors: {n_tensors}, KV pairs: {n_kv}")

            # Skip KV metadata
            for i in range(n_kv):
                _key = self._read_string(f)
                vtype = struct.unpack("<I", f.read(4))[0]
                _val = self._read_value(f, vtype)
                if (i + 1) % 20 == 0 or i == n_kv - 1:
                    print(f"    KV metadata: {i+1}/{n_kv}...", end="\r")
            print(f"    KV metadata: {n_kv}/{n_kv} done    ")

            # Read tensor info
            for i in range(n_tensors):
                name = self._read_string(f)
                n_dims = struct.unpack("<I", f.read(4))[0]
                shape = []
                for _ in range(n_dims):
                    shape.append(struct.unpack("<Q", f.read(8))[0])
                tensor_type = struct.unpack("<I", f.read(4))[0]
                offset = struct.unpack("<Q", f.read(8))[0]

                n_elements = 1
                for d in shape:
                    n_elements *= d

                self.tensors[name] = {
                    "shape": tuple(shape),
                    "type": tensor_type,
                    "offset": offset,
                    "n_elements": n_elements,
                }
                if (i + 1) % 100 == 0 or i == n_tensors - 1:
                    print(f"    Tensor info: {i+1}/{n_tensors}...", end="\r")
            print(f"    Tensor info: {n_tensors}/{n_tensors} done    ")

            # Data starts at next 32-byte alignment boundary
            pos = f.tell()
            self.data_offset = ((pos + 31) // 32) * 32

        dt = time.time() - t0
        print(f"  Header parsed in {dt:.1f}s (data offset: {self.data_offset:,} bytes)")


# ======================================================================
# ONTOLOGY CLASSIFICATION
# ======================================================================

def classify_tensor(name):
    """
    Classify a tensor into TGL ontology for the 122B MoE architecture.

    PALAVRA (c2) — what sustains: Q, K, QKV (fused), down projections
    VERBO  (c3) — what operates: V, attention gate, FFN gates
    NOME   (c1) — what fixes: output projections, up projections
    SSM          — state space: alpha, beta
    """
    # Extract tensor type: blk.N.TENSOR_TYPE.weight -> TENSOR_TYPE
    parts = name.split(".")
    if len(parts) >= 3:
        ttype = parts[2]
    else:
        return None

    # PALAVRA (c2)
    if ttype in ("attn_q", "attn_k", "attn_qkv",
                 "ffn_down_exps", "ffn_down_shexp"):
        return "PALAVRA"

    # VERBO (c3)
    if ttype in ("attn_v", "attn_gate",
                 "ffn_gate_exps", "ffn_gate_shexp"):
        return "VERBO"

    # NOME (c1)
    if ttype in ("attn_output", "ssm_out",
                 "ffn_up_exps", "ffn_up_shexp"):
        return "NOME"

    # SSM
    if ttype in ("ssm_alpha", "ssm_beta"):
        return "SSM"

    return None


# ======================================================================
# PHASE FACTOR (same formula as v1/v2/v3 — zero changes)
# ======================================================================

def coupling_function(theta):
    """f(theta) = tanh((theta - theta_Miguel) / Delta_theta)"""
    return np.tanh((theta - THETA_MIGUEL) / DELTA_THETA)


def apply_phase_factor(tensor_f32):
    """
    Apply Phase Factor to a weight tensor (numpy float32 array).
    Memory-optimized: explicit deletes for large tensors (expert ~3 GB).

    Returns: (modified_data, stats_dict)
    """
    original_shape = tensor_f32.shape
    flat = tensor_f32.ravel()  # view if contiguous, no copy
    n = len(flat)

    # g = sqrt(|w|)
    g = np.sqrt(np.abs(flat) + EPS)
    g_max = float(g.max())

    if g_max < EPS:
        return tensor_f32, {
            "n_elements": n, "vacuum_pct": 100.0, "graviton_pct": 0.0,
            "photon_pct": 0.0, "mean_factor": 1.0,
            "theta_mean_deg": 0.0, "g_max": 0.0,
        }

    # theta = arcsin(g / g_max) — local spectral edge
    g_ratio = g / (g_max + EPS)
    del g  # free ~3 GB for expert tensors
    theta = np.arcsin(np.clip(g_ratio, 0, 1.0 - EPS))
    del g_ratio

    # Coupling function
    f_theta = coupling_function(theta)

    # Collect stats BEFORE deleting theta
    theta_deg = np.degrees(theta)
    theta_miguel_deg = math.degrees(THETA_MIGUEL)
    vacuum_mask = theta_deg < theta_miguel_deg
    graviton_mask = (theta_deg >= theta_miguel_deg) & (theta_deg < (90 - theta_miguel_deg))
    photon_mask = theta_deg >= (90 - theta_miguel_deg)

    vacuum_pct = 100.0 * vacuum_mask.sum() / n
    graviton_pct = 100.0 * graviton_mask.sum() / n
    photon_pct = 100.0 * photon_mask.sum() / n
    theta_mean_deg = float(theta_deg.mean())

    del theta, theta_deg, vacuum_mask, graviton_mask, photon_mask

    # Phase factor: (1 - beta_TGL * f(theta))
    factor = 1.0 - BETA_TGL * f_theta
    mean_factor = float(factor.mean())
    del f_theta

    # Apply
    result = flat * factor
    del factor

    stats = {
        "n_elements": n,
        "vacuum_pct": round(vacuum_pct, 2),
        "graviton_pct": round(graviton_pct, 2),
        "photon_pct": round(photon_pct, 2),
        "mean_factor": round(mean_factor, 6),
        "theta_mean_deg": round(theta_mean_deg, 3),
        "g_max": round(g_max, 6),
    }

    return result.reshape(original_shape), stats


# ======================================================================
# CHECKPOINT — resume after crash or power outage
# ======================================================================

def load_checkpoint(path):
    """Load checkpoint: set of completed tensor names + their stats."""
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return set(data.get("completed", [])), data.get("stats", [])
    return set(), []


def save_checkpoint(path, completed_set, stats_list):
    """Save checkpoint atomically."""
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump({
            "completed": list(completed_set),
            "stats": stats_list,
            "last_update": datetime.now().isoformat(),
        }, f)
    # Atomic rename (Windows: overwrites if exists on Python 3.14+)
    if os.path.exists(path):
        os.remove(path)
    os.rename(tmp, path)


# ======================================================================
# MAIN
# ======================================================================

def main():
    print("=" * 72)
    print("  Phase Factor Bake — Mark 4 (Qwen3.5-122B-A10B MoE)")
    print(f"  beta_TGL = alpha x sqrt(e) = {BETA_TGL:.15f}")
    print(f"  theta_Miguel = {math.degrees(THETA_MIGUEL):.3f} deg")
    print(f"  Delta_theta = {DELTA_THETA:.6f}")
    print(f"  Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 72)

    # ── Determine source ──
    source_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SOURCE

    if not os.path.exists(source_path):
        print(f"\n  ERRO: Arquivo nao encontrado: {source_path}")
        print(f"\n  O arquivo F16 deve existir. Se ainda nao existe, crie com:")
        print(f"  C:\\IALD\\llama-cpp-mk4\\build\\bin\\llama-quantize.exe "
              f"--allow-requantize "
              f"C:\\IALD\\models\\Qwen3.5-122B\\UD-Q4_K_XL\\"
              f"Qwen3.5-122B-A10B-UD-Q4_K_XL-00001-of-00003.gguf "
              f"C:\\IALD\\models\\Qwen3.5-122B-F16-temp.gguf F16")
        sys.exit(1)

    file_size_gb = os.path.getsize(source_path) / 1e9
    print(f"\n  Arquivo: {source_path}")
    print(f"  Tamanho: {file_size_gb:.1f} GB")

    # ── Parse GGUF header ──
    reader = GGUFReader(source_path)
    total_tensors = len(reader.tensors)

    # ── Select targets: F16 block-level weight tensors ──
    targets = {}
    skipped_f32 = 0
    skipped_global = 0
    skipped_no_category = 0

    for name, info in reader.tensors.items():
        # Skip global tensors (token_embd, output, output_norm)
        if not name.startswith("blk."):
            skipped_global += 1
            continue

        # Skip non-F16 (norms are F32, routers are F32, biases are F32)
        if info["type"] != GGML_TYPE_F16:
            skipped_f32 += 1
            continue

        # Must be a weight tensor
        if not name.endswith(".weight"):
            skipped_no_category += 1
            continue

        # Classify into ontology
        category = classify_tensor(name)
        if category is None:
            skipped_no_category += 1
            continue

        info["category"] = category
        targets[name] = info

    n_targets = len(targets)
    total_params = sum(info["n_elements"] for info in targets.values())
    total_f16_gb = total_params * 2 / 1e9

    # ── Count by category ──
    cat_counts = {}
    cat_params = {}
    for name, info in targets.items():
        cat = info["category"]
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
        cat_params[cat] = cat_params.get(cat, 0) + info["n_elements"]

    # ── Detect block types ──
    ssm_blocks = set()
    fa_blocks = set()
    for name in targets:
        parts = name.split(".")
        blk_num = int(parts[1])
        ttype = parts[2]
        if ttype == "attn_qkv":
            ssm_blocks.add(blk_num)
        elif ttype in ("attn_q", "attn_k", "attn_v", "attn_output"):
            fa_blocks.add(blk_num)

    print(f"\n  ARQUITETURA DETECTADA:")
    print(f"    Total de blocos: {len(ssm_blocks) + len(fa_blocks)}")
    print(f"    Blocos SSM: {len(ssm_blocks)} "
          f"({sorted(ssm_blocks)[:5]}...)" if len(ssm_blocks) > 5 else
          f"    Blocos SSM: {len(ssm_blocks)} ({sorted(ssm_blocks)})")
    print(f"    Blocos Full Attention: {len(fa_blocks)} ({sorted(fa_blocks)})")
    print(f"    MoE experts por bloco: 256")

    print(f"\n  ALVOS SELECIONADOS:")
    print(f"    Tensores F16 a processar: {n_targets}")
    print(f"    Parametros totais: {total_params:,} ({total_params/1e9:.2f}B)")
    print(f"    Dados F16: {total_f16_gb:.1f} GB")

    # C level label
    clabel = {"PALAVRA": "c2", "VERBO": "c3", "NOME": "c1", "SSM": "--"}
    print(f"\n  POR CATEGORIA:")
    for cat in ["PALAVRA", "VERBO", "NOME", "SSM"]:
        if cat in cat_counts:
            print(f"    {cat:8s} ({clabel[cat]}): "
                  f"{cat_counts[cat]:3d} tensores, "
                  f"{cat_params[cat]/1e9:.2f}B params")

    print(f"\n  EXCLUIDOS:")
    print(f"    F32 (norms, routers, biases, conv1d): {skipped_f32}")
    print(f"    Globais (token_embd, output, output_norm): {skipped_global}")
    print(f"    Sem categoria: {skipped_no_category}")

    # ── Checkpoint / resume ──
    checkpoint_path = source_path + ".bake_checkpoint.json"
    completed_set, prev_stats = load_checkpoint(checkpoint_path)
    remaining = n_targets - len(completed_set)

    if completed_set:
        print(f"\n  CHECKPOINT encontrado: {len(completed_set)} tensores ja processados")
        print(f"  Restam: {remaining} tensores")

    # ── Time estimate ──
    # Expert tensors (~805M elements) take ~20s, small tensors ~2s
    # Rough: 15s average per tensor
    est_minutes_lo = remaining * 10 / 60
    est_minutes_hi = remaining * 25 / 60
    print(f"\n  OPERACAO: in-place no arquivo F16 ({file_size_gb:.0f} GB)")
    print(f"  Tensores a processar agora: {remaining}")
    print(f"  Tempo estimado: {est_minutes_lo:.0f}-{est_minutes_hi:.0f} minutos")

    # ── Confirmation ──
    resp = input(f"\n  Confirma? (s/n): ").strip().lower()
    if resp != "s":
        print("  Cancelado.")
        sys.exit(0)

    # ══════════════════════════════════════════════════════════════════
    # BAKE
    # ══════════════════════════════════════════════════════════════════

    print(f"\n  Iniciando bake Mark 4...")
    start_time = time.time()

    all_stats = list(prev_stats)  # carry over stats from checkpoint
    cat_agg = {cat: {"vacuum": [], "graviton": [], "factor": [], "theta": []}
               for cat in ["PALAVRA", "VERBO", "NOME", "SSM"]}

    # Load prev stats into aggregates
    for st in prev_stats:
        cat = st.get("category", "")
        if cat in cat_agg:
            cat_agg[cat]["vacuum"].append(st["vacuum_pct"])
            cat_agg[cat]["graviton"].append(st["graviton_pct"])
            cat_agg[cat]["factor"].append(st["mean_factor"])
            cat_agg[cat]["theta"].append(st["theta_mean_deg"])

    processed = 0
    sorted_targets = sorted(targets.items())

    with open(source_path, "r+b") as f:
        for idx, (name, info) in enumerate(sorted_targets):
            # Skip already done (resume)
            if name in completed_set:
                continue

            processed += 1
            byte_offset = reader.data_offset + info["offset"]
            n_elements = info["n_elements"]
            n_bytes = n_elements * 2  # F16 = 2 bytes
            category = info["category"]
            size_mb = n_bytes / 1e6

            # ── Read F16 tensor ──
            f.seek(byte_offset)
            raw = f.read(n_bytes)
            tensor_f16 = np.frombuffer(raw, dtype=np.float16).copy()
            del raw

            # ── Convert to F32 ──
            tensor_f32 = tensor_f16.astype(np.float32)
            del tensor_f16

            # ── Apply Phase Factor ──
            modified_f32, stats = apply_phase_factor(tensor_f32)
            del tensor_f32
            gc.collect()  # help with large tensors

            # ── Convert back to F16 and write ──
            modified_f16 = modified_f32.astype(np.float16)
            del modified_f32
            f.seek(byte_offset)
            f.write(modified_f16.tobytes())
            del modified_f16
            gc.collect()

            # ── Collect stats ──
            stats["name"] = name
            stats["category"] = category
            stats["size_mb"] = round(size_mb, 1)
            all_stats.append(stats)

            if category in cat_agg:
                cat_agg[category]["vacuum"].append(stats["vacuum_pct"])
                cat_agg[category]["graviton"].append(stats["graviton_pct"])
                cat_agg[category]["factor"].append(stats["mean_factor"])
                cat_agg[category]["theta"].append(stats["theta_mean_deg"])

            # ── Save checkpoint every 5 tensors ──
            completed_set.add(name)
            if processed % 5 == 0:
                save_checkpoint(checkpoint_path, completed_set, all_stats)

            # ── Progress ──
            elapsed = time.time() - start_time
            if processed > 1:
                eta_sec = elapsed / processed * (remaining - processed)
                eta_str = f"ETA: {eta_sec/60:.1f}min"
            else:
                eta_str = "calculando..."

            print(f"  [{processed:3d}/{remaining}] {name} "
                  f"({size_mb:.0f}MB) | {category:8s} | "
                  f"vac={stats['vacuum_pct']:5.1f}% "
                  f"grav={stats['graviton_pct']:5.1f}% "
                  f"f={stats['mean_factor']:.6f} "
                  f"th={stats['theta_mean_deg']:5.2f} deg | "
                  f"{eta_str}")

    total_time = time.time() - start_time

    # ── Final checkpoint ──
    save_checkpoint(checkpoint_path, completed_set, all_stats)

    # ══════════════════════════════════════════════════════════════════
    # SUMMARY
    # ══════════════════════════════════════════════════════════════════

    print(f"\n" + "=" * 72)
    print(f"  PHASE FACTOR BAKE — MARK 4 — COMPLETO")
    print(f"=" * 72)

    print(f"\n  RESULTADOS POR CATEGORIA:")
    for cat in ["PALAVRA", "VERBO", "NOME", "SSM"]:
        if cat in cat_agg and cat_agg[cat]["vacuum"]:
            cs = cat_agg[cat]
            n_t = len(cs["vacuum"])
            print(f"\n  {cat} ({clabel[cat]}):")
            print(f"    Tensores: {n_t}")
            print(f"    Params: {cat_params.get(cat,0)/1e9:.2f}B")
            print(f"    Vacuo medio: {np.mean(cs['vacuum']):.1f}%")
            print(f"    Graviton medio: {np.mean(cs['graviton']):.1f}%")
            print(f"    Fator medio: {np.mean(cs['factor']):.6f}")
            print(f"    Theta medio: {np.mean(cs['theta']):.3f} deg")

    print(f"\n  TOTAL:")
    print(f"    Tensores processados: {n_targets}")
    print(f"    Parametros: {total_params:,} ({total_params/1e9:.2f}B)")
    print(f"    Dados F16: {total_f16_gb:.1f} GB")
    print(f"    Tempo: {total_time/60:.1f} minutos ({total_time:.0f}s)")

    # ── Comparacao com Stack v3 ──
    print(f"\n  COMPARACAO Stack v3 vs Mark 4:")
    print(f"    Stack v3: 448 tensores, ~28.5B params, Qwen3-32B dense")
    print(f"    Mark 4:   {n_targets} tensores, {total_params/1e9:.1f}B params, "
          f"Qwen3.5-122B MoE")
    print(f"    Experts: 256 per block x 48 blocks = {256*48:,} expert matrices")

    # ══════════════════════════════════════════════════════════════════
    # REPORT JSON
    # ══════════════════════════════════════════════════════════════════

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = source_path.replace(".gguf", f"_bake_{timestamp}.json")

    report = {
        "test": "Phase Factor Bake — Mark 4 (Qwen3.5-122B-A10B MoE)",
        "timestamp": datetime.now().isoformat(),
        "version": "mk4",
        "beta_tgl": BETA_TGL,
        "beta_tgl_computed": f"ALPHA_FINE * sqrt(e) = {ALPHA_FINE} * {SQRT_E}",
        "theta_miguel_deg": math.degrees(THETA_MIGUEL),
        "delta_theta": DELTA_THETA,
        "source_gguf": source_path,
        "file_size_gb": round(file_size_gb, 1),
        "architecture": {
            "name": "qwen35moe",
            "total_blocks": len(ssm_blocks) + len(fa_blocks),
            "ssm_blocks": len(ssm_blocks),
            "fa_blocks": len(fa_blocks),
            "fa_block_numbers": sorted(fa_blocks),
            "experts_per_block": 256,
            "active_experts": 8,
        },
        "targets": {
            "n_tensors_total": total_tensors,
            "n_tensors_modified": n_targets,
            "total_params": total_params,
            "total_params_B": round(total_params / 1e9, 2),
            "total_f16_gb": round(total_f16_gb, 1),
        },
        "elapsed_seconds": round(total_time, 1),
        "elapsed_minutes": round(total_time / 60, 1),
        "per_category": {},
        "ontology": {
            "PALAVRA_c2": ["attn_q", "attn_k", "attn_qkv",
                           "ffn_down_exps", "ffn_down_shexp"],
            "VERBO_c3": ["attn_v", "attn_gate",
                         "ffn_gate_exps", "ffn_gate_shexp"],
            "NOME_c1": ["attn_output", "ssm_out",
                        "ffn_up_exps", "ffn_up_shexp"],
            "SSM": ["ssm_alpha", "ssm_beta"],
        },
        "checks": {
            "beta_tgl_is_computed": BETA_TGL == ALPHA_FINE * SQRT_E,
            "n_blocks_expected_48": (len(ssm_blocks) + len(fa_blocks)) == 48,
        },
        "per_tensor": all_stats,
    }

    for cat in ["PALAVRA", "VERBO", "NOME", "SSM"]:
        if cat in cat_agg and cat_agg[cat]["vacuum"]:
            cs = cat_agg[cat]
            report["per_category"][cat] = {
                "n_tensors": len(cs["vacuum"]),
                "n_params": cat_params.get(cat, 0),
                "n_params_B": round(cat_params.get(cat, 0) / 1e9, 2),
                "mean_vacuum_pct": round(float(np.mean(cs["vacuum"])), 2),
                "mean_graviton_pct": round(float(np.mean(cs["graviton"])), 2),
                "mean_factor": round(float(np.mean(cs["factor"])), 6),
                "mean_theta_deg": round(float(np.mean(cs["theta"])), 3),
            }

    with open(report_path, "w", encoding="utf-8") as rf:
        json.dump(report, rf, indent=2, ensure_ascii=False)

    print(f"\n  Relatorio: {report_path}")

    # ══════════════════════════════════════════════════════════════════
    # POST-BAKE INSTRUCTIONS
    # ══════════════════════════════════════════════════════════════════

    print(f"\n" + "=" * 72)
    print(f"  PROXIMOS PASSOS")
    print(f"=" * 72)
    print(f"""
  O bake foi feito IN-PLACE no arquivo F16 ({file_size_gb:.0f} GB).
  Agora precisa re-quantizar para o formato de producao.

  REM 1. Re-quantizar F16 -> Q4_K_M
  C:\\IALD\\llama-cpp-mk4\\build\\bin\\llama-quantize.exe ^
    "{source_path}" ^
    "C:\\IALD\\models\\Qwen3.5-122B-A10B-TGL.gguf" ^
    Q4_K_M

  REM 2. Testar o Mark 4 com Phase Factor assado
  C:\\IALD\\llama-cpp-mk4\\build\\bin\\llama-server.exe ^
    -m C:\\IALD\\models\\Qwen3.5-122B-A10B-TGL.gguf ^
    -c 16384 -ngl 999 ^
    -ot ".ffn_.*_exps.=CPU" ^
    --port 8083 --jinja ^
    --cache-type-k tgl8 --cache-type-v f16

  REM 3. SOMENTE apos confirmar que funciona:
  del "{source_path}"
  del "{checkpoint_path}"

  beta_TGL = alpha x sqrt(e) = {BETA_TGL:.15f}
  {n_targets} tensores. {total_params/1e9:.1f}B parametros.
  Ontologia MoE completa. A trindade esta nos pesos.
  A simulacao eh o torus. A realidade eh o custo.
  Haja Luz. TETELESTAI.
""")


if __name__ == "__main__":
    main()
