#!/usr/bin/env python3
"""Atualiza manifestos com bytes e SHA-256 dos artefatos atuais e da REV0."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

K08 = Path(__file__).resolve().parent.parent
FORMULA_DIR = K08 / "FORMULA"
ENTRADA_DIR = K08 / "ENTRADA"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def entrada(base, raiz):
    out = []
    for path in sorted(base.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(raiz).as_posix()
        if path.name.startswith("MANIFESTO_"):
            continue
        out.append({
            "arquivo": rel,
            "bytes": path.stat().st_size,
            "sha256": sha(path),
        })
    return out


def main():
    entrada_doc = {
        "escopo": "K08/ENTRADA; REV0 preservada; manifestos não listam a si mesmos",
        "tokenizador": "tokens_ref são Qwen/Qwen3.6-35B-A3B via tokenizer.json; fallback byte=token é histórico",
        "arquivos": entrada(ENTRADA_DIR, K08),
    }
    formula_doc = {
        "escopo": "K08/FORMULA; fórmula lógica inalterada pela errata de tokens",
        "arquivos": entrada(FORMULA_DIR, K08),
    }
    (ENTRADA_DIR / "MANIFESTO_ENTRADA_K08.json").write_text(
        json.dumps(entrada_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    (FORMULA_DIR / "MANIFESTO_FORMULA_K08.json").write_text(
        json.dumps(formula_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({
        "entrada_arquivos": len(entrada_doc["arquivos"]),
        "formula_arquivos": len(formula_doc["arquivos"]),
        "manifesto_entrada_sha256": sha(ENTRADA_DIR / "MANIFESTO_ENTRADA_K08.json"),
        "manifesto_formula_sha256": sha(FORMULA_DIR / "MANIFESTO_FORMULA_K08.json"),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
