"""Gera hashes da REV2; nao executa contas nem abre dados externos."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

AQUI = Path(__file__).resolve().parent
SAIDA = AQUI / "SHA256SUMS_K09.json"


def main() -> None:
    entradas = []
    for caminho in sorted(AQUI.iterdir(), key=lambda p: p.name.casefold()):
        if not caminho.is_file() or caminho == SAIDA:
            continue
        dados = caminho.read_bytes()
        entradas.append({
            "arquivo": caminho.name,
            "bytes": len(dados),
            "sha256": hashlib.sha256(dados).hexdigest(),
        })
    objeto = {
        "estatuto": "HASHES_DOCUMENTAIS_REV2__SEM_EXECUCAO_DE_CONTAS",
        "escopo": "todos os arquivos regulares da REV2, exceto SHA256SUMS_K09.json",
        "arquivos": entradas,
    }
    SAIDA.write_text(json.dumps(objeto, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"arquivos_hasheados": len(entradas), "saida": str(SAIDA)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
