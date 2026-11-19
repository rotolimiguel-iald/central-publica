#!/usr/bin/env python3
"""Mede a entrada pública K06 sem executar modelo nem alterar a fonte.

Os três contadores de tokens são HEURÍSTICAS transparentes, não contagens de
tokenizer. A porta de janela só admite comparação exata depois que modelo,
versão, tokenizer, janela oficial e orçamento completo forem pinados.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any

DEFAULT_INPUT = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_pt.txt")
DEFAULT_WINDOWS = Path(__file__).with_name("JANELAS_MODELOS_CANDIDATOS.json")
PUBLICATION = {
    "doi": "10.5281/zenodo.24196546",
    "zenodo_record": "24196546",
    "version": "411",
    "file_key": "um_absoluto_pt.txt",
    "bytes": 1164350,
    "md5": "b7f69478a608347a1d59b8ce6c81e751",
}


def canonical_json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def measure_text(data: bytes) -> dict[str, Any]:
    text = data.decode("utf-8", errors="strict")
    words = re.findall(r"\S+", text, flags=re.UNICODE)
    proxies = {
        "utf8_bytes_div_4": math.ceil(len(data) / 4),
        "unicode_codepoints_div_4": math.ceil(len(text) / 4),
        "whitespace_words_x_1_30": math.ceil(len(words) * 1.30),
    }
    values = list(proxies.values())
    return {
        "encoding": "UTF-8 estrito",
        "bytes": len(data),
        "sha256": sha256_bytes(data),
        "md5": hashlib.md5(data).hexdigest(),
        "unicode_codepoints": len(text),
        "whitespace_words": len(words),
        "lines_splitlines": len(text.splitlines()),
        "empty_lines": sum(1 for line in text.splitlines() if not line.strip()),
        "crlf_count": data.count(b"\r\n"),
        "lf_count": data.count(b"\n"),
        "nul_count": data.count(b"\x00"),
        "token_proxies": proxies,
        "token_proxy_range_not_confidence_interval": [min(values), max(values)],
        "token_proxy_warning": (
            "Heurísticas de planejamento; não são tokens de nenhum modelo e não "
            "autorizam decidir cabimento, truncamento ou poder."
        ),
    }


def compare_windows(windows: dict[str, Any]) -> list[dict[str, Any]]:
    comparisons: list[dict[str, Any]] = []
    for model in windows.get("models", []):
        base = {
            "model_id": model.get("model_id"),
            "model_version": model.get("model_version"),
            "official_context_window_tokens": model.get("official_context_window_tokens"),
            "tokenizer_id": model.get("tokenizer_id"),
        }
        required = [
            "model_id", "model_version", "official_window_source_url",
            "official_context_window_tokens", "tokenizer_id",
            "measured_input_tokens", "protocol_overhead_tokens",
            "reserved_output_tokens", "history_tokens_per_additional_step",
            "additional_steps",
        ]
        missing = [key for key in required if model.get(key) is None]
        if missing:
            comparisons.append({**base, "status": "PENDING_EXACT_INPUTS", "missing": missing})
            continue
        total = (
            model["measured_input_tokens"]
            + model["protocol_overhead_tokens"]
            + model["reserved_output_tokens"]
            + model["history_tokens_per_additional_step"] * model["additional_steps"]
        )
        window = model["official_context_window_tokens"]
        comparisons.append({
            **base,
            "status": "EXACT_BUDGET_COMPUTED",
            "measured_input_tokens": model["measured_input_tokens"],
            "required_total_tokens": total,
            "remaining_tokens": window - total,
            "fits_without_truncation": total <= window,
            "note": "Só vale para a versão, tokenizer e orçamento pinados nesta entrada.",
        })
    return comparisons


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--windows", type=Path, default=DEFAULT_WINDOWS)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    data = args.input.read_bytes()  # somente leitura
    measurement = measure_text(data)
    windows = json.loads(args.windows.read_text(encoding="utf-8"))
    comparisons = compare_windows(windows)
    report = {
        "schema": "k06.entrada-publica.medida.v1",
        "estatuto": "HIPOTESE_DE_TRABALHO_NAO_RATIFICACAO_R3",
        "source_path_read_only": str(args.input),
        "publication": PUBLICATION,
        "publication_match": {
            "bytes": measurement["bytes"] == PUBLICATION["bytes"],
            "md5": measurement["md5"] == PUBLICATION["md5"],
        },
        "measurement": measurement,
        "candidate_windows_status": windows.get("status"),
        "candidate_window_comparisons": comparisons,
        "window_gate": {
            "models_chosen": bool(windows.get("models")),
            "numeric_window_comparison_available": bool(comparisons),
            "decision": (
                "Não escolher modelo nem truncar o artigo antes de tokenização exata "
                "e orçamento de contexto completo, tudo congelado antes de saídas."
            ),
        },
        "no_model_executed": True,
        "no_result_opened": True,
        "source_modified": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(canonical_json(report))


if __name__ == "__main__":
    main()
