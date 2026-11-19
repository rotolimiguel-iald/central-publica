#!/usr/bin/env python3
"""Extrai, sem recomputar estatística, os registros de relógio já selados."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(r"C:\IALD")
CORE = ROOT / "Artigo" / "Haja_Luz" / "A Ponte e o Um" / "Nós" / "um_absoluto.json"
OUT = ROOT / "Central de Patentes" / "work" / "cadeia_de_selo" / "v412" / "kimi" / "K05" / "TAU" / "medidas" / "clock_selado_extraido.json"
WANTED = {"clock_test_result_v369", "clock_test_protocol_v369"}


def walk(value: Any, path: tuple[str, ...] = ()):
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = path + (key,)
            if key in WANTED:
                yield child_path, child
            yield from walk(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk(child, path + (str(index),))


def main() -> None:
    raw = CORE.read_bytes()
    document = json.loads(raw.decode("utf-8"))
    found = list(walk(document))
    missing = WANTED.difference(path[-1] for path, _ in found)
    if missing:
        raise SystemExit(f"Chaves ausentes: {sorted(missing)}")
    payload = {
        "status": "REAL_READ_OF_SEALED_RECORD_NO_NEW_OBSERVED_STATISTIC",
        "source": str(CORE),
        "source_bytes": len(raw),
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "records": [
            {"key": path[-1], "json_path": list(path), "value": value}
            for path, value in found
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUT),
        "source_sha256": payload["source_sha256"],
        "records": [{"key": value["key"], "json_path": value["json_path"]} for value in payload["records"]],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
