#!/usr/bin/env python3
"""Roda duas vezes apenas os scripts sintéticos e compara todos os bytes da K08."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

EXTRACAO = Path(__file__).resolve().parent
K08 = EXTRACAO.parent
ISOMORFO = K08 / "ISOMORFO"
RELATORIO = EXTRACAO / "REPRODUCAO.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot():
    arquivos = {}
    for pasta in (EXTRACAO, ISOMORFO):
        for path in sorted(pasta.rglob("*"), key=lambda p: str(p.relative_to(K08))):
            if path.is_file() and path != RELATORIO and "__pycache__" not in path.parts:
                arquivos[str(path.relative_to(K08))] = sha256(path)
    combinado = hashlib.sha256(
        json.dumps(arquivos, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return {"combined_sha256": combinado, "files": arquivos}


def rodada(numero: int):
    comandos = [
        (EXTRACAO, "gerar_casos.py"),
        (EXTRACAO, "executar_casos.py"),
        (EXTRACAO, "inducao.py"),
        (ISOMORFO, "executar_isomorfo.py"),
    ]
    logs = []
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    for cwd, script in comandos:
        proc = subprocess.run(
            [sys.executable, "-B", script],
            cwd=cwd,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        logs.append({"script": script, "returncode": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr})
        if proc.returncode != 0:
            raise RuntimeError(f"Falha na rodada {numero}, {script}: {proc.stdout}\n{proc.stderr}")
    return {"run": numero, "logs": logs, "snapshot": snapshot()}


def main() -> None:
    primeira = rodada(1)
    segunda = rodada(2)
    a = primeira["snapshot"]
    b = segunda["snapshot"]
    alterados = sorted(nome for nome in set(a["files"]) | set(b["files"]) if a["files"].get(nome) != b["files"].get(nome))
    payload = {
        "schema": "k08-r4-synthetic-reproducibility-v1",
        "model_calls": 0,
        "network_used": False,
        "scope": "Somente scripts e dados sintéticos das pastas EXTRACAO e ISOMORFO.",
        "run1": primeira,
        "run2": segunda,
        "byte_identical": not alterados,
        "changed_files": alterados,
        "combined_sha256": b["combined_sha256"],
        "meaning": "Reprodutibilidade de software; não é certificação de produção nem evidência sobre modelos.",
    }
    RELATORIO.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"byte_identical": not alterados, "changed_files": alterados, "combined_sha256": b["combined_sha256"], "file_count": len(b["files"])}, ensure_ascii=False))
    if alterados:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
