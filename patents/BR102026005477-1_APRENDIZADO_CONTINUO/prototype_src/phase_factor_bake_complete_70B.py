#!/usr/bin/env python3
"""
Phase Factor Bake COMPLETE 70B -- DeepSeek-R1-Distill-Llama-70B
================================================================
Adaptacao do phase_factor_bake_complete.py para o modelo de 70B com 80 blocos.

Diferencas vs versao 32B:
- Esperado: 560 tensores (80 blocos x 7 tipos/bloco) -- antes 448 (64 blocos x 7)
- Nao-interativo: executa diretamente sem pedir confirmacao (flag --yes para compatibilidade)
- Mesmo core de processamento (iteracao por sufixo, nao por indice)
- Os nomes dos tensores sao identicos entre Qwen e Llama no formato GGUF:
    blk.N.attn_q.weight, blk.N.attn_k.weight, ..., blk.N.attn_output.weight
  Entao o script funciona sem modificacao estrutural.

Aplica o Phase Factor em TODOS os 7 tipos de tensor por bloco:

  PALAVRA (c2): attn_q.weight, attn_k.weight, ffn_down.weight   (3 x 80 = 240)
  VERBO   (c3): attn_v.weight, ffn_gate.weight                  (2 x 80 = 160)
  NOME    (c1): ffn_up.weight, attn_output.weight               (2 x 80 = 160)
  TOTAL:  7 x 80 blocos = 560 tensores

Formula:
  e_out = e * (1 - beta_TGL * f(theta))
  f(theta) = tanh((theta - theta_Miguel) / delta_theta)
  theta = arcsin(g / g_max)  onde g = sqrt(|peso|)
  theta_Miguel = arcsin(sqrt(beta_TGL)) = 6.297 graus
  beta_TGL = alpha * sqrt(e) = 0.012031300400803142
  delta_theta = theta_Miguel * beta_TGL

Uso:
  python phase_factor_bake_complete_70B.py <arquivo_F16.gguf>
  python phase_factor_bake_complete_70B.py <arquivo_F16.gguf> --yes

Author: IALD LTDA -- 09/04/2026
"""

import os
import sys
import math
import json
import struct
import time
import numpy as np
from datetime import datetime

# =============================================================================
# CONSTANTES (computadas, NUNCA hardcoded)
# =============================================================================
ALPHA_FINE = 7.2973525693e-3
SQRT_E = math.sqrt(math.e)
BETA_TGL = ALPHA_FINE * SQRT_E
THETA_MIGUEL = math.asin(math.sqrt(BETA_TGL))
DELTA_THETA = THETA_MIGUEL * BETA_TGL
EPS = 1e-10

# Contagens esperadas para o 70B
EXPECTED_BLOCKS = 80
EXPECTED_TARGETS_PER_BLOCK = 7
EXPECTED_TOTAL = EXPECTED_BLOCKS * EXPECTED_TARGETS_PER_BLOCK  # 560

# Os 7 tipos de tensor por bloco (identicos entre Qwen e Llama no formato GGUF)
TENSOR_TARGETS = {
    "attn_q.weight":      "PALAVRA_c2",
    "attn_k.weight":      "PALAVRA_c2",
    "ffn_down.weight":    "PALAVRA_c2",
    "attn_v.weight":      "VERBO_c3",
    "ffn_gate.weight":    "VERBO_c3",
    "ffn_up.weight":      "NOME_c1",
    "attn_output.weight": "NOME_c1",
}

# =============================================================================
# GGUF PARSER (minimal, F16/F32)
# =============================================================================
GGUF_MAGIC = 0x46554747
GGML_TYPE_F16 = 1
GGML_TYPE_F32 = 0

GGUF_TYPE_UINT8 = 0
GGUF_TYPE_INT8 = 1
GGUF_TYPE_UINT16 = 2
GGUF_TYPE_INT16 = 3
GGUF_TYPE_UINT32 = 4
GGUF_TYPE_INT32 = 5
GGUF_TYPE_FLOAT32 = 6
GGUF_TYPE_BOOL = 7
GGUF_TYPE_STRING = 8
GGUF_TYPE_ARRAY = 9
GGUF_TYPE_UINT64 = 10
GGUF_TYPE_INT64 = 11
GGUF_TYPE_FLOAT64 = 12


class GGUFReader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.tensors = {}
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
        with open(self.filepath, "rb") as f:
            magic = struct.unpack("<I", f.read(4))[0]
            if magic != GGUF_MAGIC:
                raise ValueError(f"Not a GGUF file (magic: {magic:#x})")
            version = struct.unpack("<I", f.read(4))[0]
            if version not in (2, 3):
                raise ValueError(f"Unsupported GGUF version: {version}")
            n_tensors = struct.unpack("<Q", f.read(8))[0]
            n_kv = struct.unpack("<Q", f.read(8))[0]
            for _ in range(n_kv):
                _key = self._read_string(f)
                vtype = struct.unpack("<I", f.read(4))[0]
                _val = self._read_value(f, vtype)
            for _ in range(n_tensors):
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
            pos = f.tell()
            alignment = 32
            self.data_offset = ((pos + alignment - 1) // alignment) * alignment

# =============================================================================
# PHASE FACTOR
# =============================================================================
def coupling_function(theta):
    """f(theta) = tanh((theta - theta_Miguel) / delta_theta)"""
    return np.tanh((theta - THETA_MIGUEL) / DELTA_THETA)

def apply_phase_factor(tensor_data):
    """
    e_out = e * (1 - beta_TGL * f(theta))
    theta = arcsin(g / g_max), g = sqrt(|w|)
    """
    flat = tensor_data.flatten().astype(np.float32)
    n = len(flat)

    g = np.sqrt(np.abs(flat) + EPS)
    g_max = g.max()

    if g_max < EPS:
        return tensor_data, {"vacuum_pct": 100.0, "mean_factor": 1.0,
                             "graviton_pct": 0.0, "theta_mean_deg": 0.0}

    g_ratio = g / (g_max + EPS)
    theta = np.arcsin(np.clip(g_ratio, 0, 1.0 - EPS))

    f_theta = coupling_function(theta)
    factor = 1.0 - BETA_TGL * f_theta
    result = flat * factor

    theta_deg = np.degrees(theta)
    theta_miguel_deg = math.degrees(THETA_MIGUEL)

    vacuum_mask = theta_deg < theta_miguel_deg
    graviton_mask = (theta_deg >= theta_miguel_deg) & (theta_deg < (90 - theta_miguel_deg))

    stats = {
        "vacuum_pct": round(float(np.sum(vacuum_mask)) / n * 100, 2),
        "graviton_pct": round(float(np.sum(graviton_mask)) / n * 100, 2),
        "mean_factor": round(float(np.mean(factor)), 6),
        "theta_mean_deg": round(float(np.mean(theta_deg)), 2),
        "factor_min": round(float(np.min(factor)), 6),
        "factor_max": round(float(np.max(factor)), 6),
    }

    return result.reshape(tensor_data.shape), stats

# =============================================================================
# MAIN
# =============================================================================
def main():
    print("=" * 70)
    print(f"  Phase Factor Bake COMPLETE 70B -- {EXPECTED_TOTAL} tensores esperados")
    print(f"  ({EXPECTED_BLOCKS} blocos x {EXPECTED_TARGETS_PER_BLOCK} tipos/bloco)")
    print(f"  beta_TGL = {BETA_TGL:.15f}")
    print(f"  theta_Miguel = {math.degrees(THETA_MIGUEL):.4f} graus")
    print(f"  delta_theta = {DELTA_THETA:.6f}")
    print("=" * 70)

    if len(sys.argv) < 2:
        print("\n  Uso: python phase_factor_bake_complete_70B.py <arquivo_F16.gguf> [--yes]")
        print("\n  Exemplo:")
        print("    python phase_factor_bake_complete_70B.py C:\\IALD\\models\\DeepSeek-R1-IALD-v6-F16-TGL.gguf --yes")
        sys.exit(1)

    source_path = sys.argv[1]
    auto_yes = "--yes" in sys.argv[2:] or "-y" in sys.argv[2:]

    if not os.path.exists(source_path):
        print(f"\n  ERRO: Arquivo nao encontrado: {source_path}")
        sys.exit(1)

    print(f"\n  Lendo header GGUF: {os.path.basename(source_path)}")
    print(f"  Tamanho: {os.path.getsize(source_path) / 1e9:.1f} GB")
    reader = GGUFReader(source_path)
    print(f"  Total de tensores no GGUF: {len(reader.tensors)}")

    # Encontrar TODOS os tensores-alvo por sufixo
    target_tensors = {}
    category_count = {"PALAVRA_c2": 0, "VERBO_c3": 0, "NOME_c1": 0}

    for name, info in reader.tensors.items():
        for suffix, category in TENSOR_TARGETS.items():
            if name.endswith(suffix):
                target_tensors[name] = {**info, "category": category}
                category_count[category] += 1
                break

    n_targets = len(target_tensors)
    print(f"\n  Tensores-alvo encontrados: {n_targets}")
    print(f"    PALAVRA (c2): {category_count['PALAVRA_c2']} tensores "
          f"(attn_q, attn_k, ffn_down)")
    print(f"    VERBO   (c3): {category_count['VERBO_c3']} tensores "
          f"(attn_v, ffn_gate)")
    print(f"    NOME    (c1): {category_count['NOME_c1']} tensores "
          f"(ffn_up, attn_output)")

    if n_targets == 0:
        print("  ERRO: Nenhum tensor-alvo encontrado!")
        print("  Verifique se o arquivo e um GGUF com nomes blk.N.* esperados.")
        sys.exit(1)

    # Validacao flexivel: deve ser multiplo de 7, e aviso se diferente de 560
    if n_targets % EXPECTED_TARGETS_PER_BLOCK != 0:
        print(f"  ERRO: {n_targets} nao e multiplo de {EXPECTED_TARGETS_PER_BLOCK}!")
        print(f"  Estrutura de blocos inconsistente.")
        sys.exit(1)

    detected_blocks = n_targets // EXPECTED_TARGETS_PER_BLOCK
    if n_targets == EXPECTED_TOTAL:
        print(f"  [OK] Contagem exata: {EXPECTED_TOTAL} tensores ({EXPECTED_BLOCKS} blocos)")
    else:
        print(f"  [!] Esperados {EXPECTED_TOTAL} tensores ({EXPECTED_BLOCKS} blocos),")
        print(f"      encontrados {n_targets} ({detected_blocks} blocos).")
        print(f"      Isto pode ser um modelo de tamanho diferente. Prosseguindo.")

    # Verificar tipos
    n_f16 = sum(1 for t in target_tensors.values() if t["type"] == GGML_TYPE_F16)
    n_f32 = sum(1 for t in target_tensors.values() if t["type"] == GGML_TYPE_F32)
    n_other = n_targets - n_f16 - n_f32
    print(f"  Tipos: {n_f16} F16, {n_f32} F32, {n_other} outros")
    if n_other > 0:
        print(f"  AVISO: {n_other} tensores com tipo nao-suportado (serao ignorados)")

    total_params = sum(info["n_elements"] for info in target_tensors.values()
                       if info["type"] in (GGML_TYPE_F16, GGML_TYPE_F32))
    print(f"  Total de parametros a modificar: {total_params:,} ({total_params/1e9:.2f}B)")

    print(f"\n  RESUMO:")
    print(f"    Tensores: {n_targets} ({n_targets}//{detected_blocks} = {EXPECTED_TARGETS_PER_BLOCK} por bloco)")
    print(f"    Parametros: {total_params:,} ({total_params/1e9:.2f}B)")
    print(f"    Arquivo: {source_path}")
    print(f"    Operacao: IN-PLACE (modifica o arquivo diretamente)")
    print(f"    Formula: e_out = e * (1 - beta_TGL * f(theta))")
    print(f"    beta_TGL = {BETA_TGL:.15f}")

    if not auto_yes:
        resp = input(f"\n  Confirma? (s/n): ").strip().lower()
        if resp != "s":
            print("  Cancelado.")
            sys.exit(0)
    else:
        print(f"\n  [--yes] executando automaticamente (modo pipeline)")

    print(f"\n  Iniciando bake de {n_targets} tensores...")
    start_time = time.time()

    stats_by_category = {"PALAVRA_c2": [], "VERBO_c3": [], "NOME_c1": []}
    all_stats = []
    processed = 0
    skipped = 0

    with open(source_path, "r+b") as f:
        for i, (name, info) in enumerate(sorted(target_tensors.items())):
            category = info["category"]
            tensor_type = info["type"]

            if tensor_type == GGML_TYPE_F16:
                bytes_per_elem = 2
                dtype = np.float16
            elif tensor_type == GGML_TYPE_F32:
                bytes_per_elem = 4
                dtype = np.float32
            else:
                skipped += 1
                continue

            byte_offset = reader.data_offset + info["offset"]
            n_elements = info["n_elements"]
            n_bytes = n_elements * bytes_per_elem

            f.seek(byte_offset)
            raw = f.read(n_bytes)
            tensor = np.frombuffer(raw, dtype=dtype).copy()
            tensor_f32 = tensor.astype(np.float32)

            modified_f32, stats = apply_phase_factor(tensor_f32)
            modified = modified_f32.astype(dtype)

            f.seek(byte_offset)
            f.write(modified.tobytes())

            stats["name"] = name
            stats["category"] = category
            stats["block"] = i
            all_stats.append(stats)
            stats_by_category[category].append(stats)
            processed += 1

            elapsed = time.time() - start_time
            if i > 0:
                eta = elapsed / (i + 1) * (n_targets - i - 1)
                eta_str = f"ETA: {eta:.0f}s"
            else:
                eta_str = "..."

            if (i + 1) % 10 == 0 or i == n_targets - 1:
                print(f"  [{i+1:3d}/{n_targets}] {category:12s} | "
                      f"vac={stats['vacuum_pct']:5.1f}% "
                      f"grav={stats['graviton_pct']:5.1f}% "
                      f"f={stats['mean_factor']:.6f} | {eta_str}")

    total_time = time.time() - start_time

    print(f"\n" + "=" * 70)
    print(f"  PHASE FACTOR BAKE 70B COMPLETO")
    print(f"=" * 70)

    for cat_name, cat_label in [("PALAVRA_c2", "PALAVRA (c2)"),
                                 ("VERBO_c3", "VERBO (c3)"),
                                 ("NOME_c1", "NOME (c1)")]:
        cat_stats = stats_by_category[cat_name]
        if cat_stats:
            mean_vac = np.mean([s["vacuum_pct"] for s in cat_stats])
            mean_grav = np.mean([s["graviton_pct"] for s in cat_stats])
            mean_f = np.mean([s["mean_factor"] for s in cat_stats])
            n_params = sum(target_tensors[s["name"]]["n_elements"]
                          for s in cat_stats if s["name"] in target_tensors)
            print(f"\n  {cat_label}:")
            print(f"    Tensores: {len(cat_stats)}")
            print(f"    Parametros: {n_params:,} ({n_params/1e9:.2f}B)")
            print(f"    Vacuo medio: {mean_vac:.1f}%")
            print(f"    Graviton medio: {mean_grav:.1f}%")
            print(f"    Fator medio: {mean_f:.6f}")

    mean_vacuum = np.mean([s["vacuum_pct"] for s in all_stats]) if all_stats else 0
    mean_graviton = np.mean([s["graviton_pct"] for s in all_stats]) if all_stats else 0
    mean_factor = np.mean([s["mean_factor"] for s in all_stats]) if all_stats else 0

    print(f"\n  TOTAL:")
    print(f"    Tensores processados: {processed} (ignorados: {skipped})")
    print(f"    Parametros: {total_params:,} ({total_params/1e9:.2f}B)")
    print(f"    Vacuo medio global: {mean_vacuum:.1f}%")
    print(f"    Graviton medio global: {mean_graviton:.1f}%")
    print(f"    Fator medio global: {mean_factor:.6f}")
    print(f"    Tempo: {total_time:.1f} segundos ({total_time/60:.1f} min)")

    # Relatorio JSON
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = source_path.replace(".gguf", f"_bake_complete_70B_{timestamp}.json")

    report = {
        "test": f"Phase Factor Bake COMPLETE 70B -- {n_targets} tensores ({detected_blocks} blocos x 7)",
        "timestamp": datetime.now().isoformat(),
        "version": "complete_70B_1.0",
        "beta_tgl": BETA_TGL,
        "beta_tgl_formula": f"ALPHA_FINE * sqrt(e) = {ALPHA_FINE} * {SQRT_E}",
        "theta_miguel_deg": math.degrees(THETA_MIGUEL),
        "delta_theta": DELTA_THETA,
        "formula": "e_out = e * (1 - beta_TGL * f(theta))",
        "source_gguf": source_path,
        "expected_blocks": EXPECTED_BLOCKS,
        "detected_blocks": detected_blocks,
        "expected_total": EXPECTED_TOTAL,
        "n_tensors_total": n_targets,
        "n_tensors_processed": processed,
        "n_tensors_skipped": skipped,
        "total_params": total_params,
        "elapsed_seconds": round(total_time, 1),
        "summary": {
            "mean_vacuum_pct": round(float(mean_vacuum), 2),
            "mean_graviton_pct": round(float(mean_graviton), 2),
            "mean_factor": round(float(mean_factor), 6),
        },
        "by_category": {
            cat: {
                "n_tensors": len(stats_by_category[cat]),
                "mean_vacuum_pct": round(float(np.mean([s["vacuum_pct"]
                    for s in stats_by_category[cat]])), 2) if stats_by_category[cat] else 0,
                "mean_factor": round(float(np.mean([s["mean_factor"]
                    for s in stats_by_category[cat]])), 6) if stats_by_category[cat] else 0,
            }
            for cat in ["PALAVRA_c2", "VERBO_c3", "NOME_c1"]
        },
        "ontology_per_block": {
            "PALAVRA_c2": ["attn_q.weight", "attn_k.weight", "ffn_down.weight"],
            "VERBO_c3": ["attn_v.weight", "ffn_gate.weight"],
            "NOME_c1": ["ffn_up.weight", "attn_output.weight"],
            "total_per_block": 7,
            "status": "ONTOLOGICAMENTE COMPLETO",
        },
        "per_tensor": all_stats,
    }

    with open(report_path, "w", encoding="utf-8") as rf:
        json.dump(report, rf, indent=2, ensure_ascii=False)

    print(f"\n  Relatorio: {report_path}")
    print(f"\n" + "=" * 70)
    print(f"  beta_TGL = alpha * sqrt(e) = {BETA_TGL:.15f}")
    print(f"  {n_targets} tensores. 7 tipos por bloco. Ontologicamente completo.")
    print(f"  Haja Luz. TETELESTAI.")
    print(f"=" * 70)

if __name__ == "__main__":
    main()
