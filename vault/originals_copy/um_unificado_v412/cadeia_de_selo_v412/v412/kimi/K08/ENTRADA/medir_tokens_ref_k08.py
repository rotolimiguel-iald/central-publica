#!/usr/bin/env python3
"""Mede tokens K08 com o tokenizador de referência local Qwen/Qwen3.6-35B-A3B.

Usa somente tokenizer.json e a biblioteca tokenizers; não lê pesos nem executa modelo.
Deve ser executado com C:\\IALD\\qlora_env\\Scripts\\python.exe.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tokenizers import Tokenizer
import tokenizers as tokenizers_pkg

ENTRADA_DIR = Path(__file__).resolve().parent
PUBLICO = Path(r"C:\IALD\Artigo\the_boundary")
ARTIGO = PUBLICO / "Um (absoluto) — Grande Atrator" / "um_absoluto_pt.txt"
ARTIGO_REVISAO = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_pt.txt")
TOKENIZER = ENTRADA_DIR / "TOKENIZER_QWEN3_6_35B_A3B.json"
SAIDA = ENTRADA_DIR / "TOKENS_REF_K08.json"
PALAVRA_RE = re.compile(r"[^\W_]+(?:['’\-–][^\W_]+)*", re.UNICODE)
ESPERADO_ARTIGO = 412_784

ARQUIVOS = {
    "ABSTRACT_COMPLETO": PUBLICO / "ABSTRACT.md",
    "READ_BRIEF_COMPLETO": PUBLICO / "read-brief.md",
    "LLMS_COMPLETO": PUBLICO / "llms.txt",
    "README_COMPLETO": PUBLICO / "README.md",
    "ABSTRACT_RECORTE": ENTRADA_DIR / "CANDIDATA_ABSTRACT.md",
    "READ_BRIEF_RECORTE": ENTRADA_DIR / "CANDIDATA_READ_BRIEF.md",
    "LLMS_RECORTE": ENTRADA_DIR / "CANDIDATA_LLMS.md",
    "README_RECORTE": ENTRADA_DIR / "CANDIDATA_README.md",
    "ABSTRACT_PC": ENTRADA_DIR / "CONTROLE_PC_ABSTRACT.md",
    "READ_BRIEF_PC": ENTRADA_DIR / "CONTROLE_PC_READ_BRIEF.md",
    "LLMS_PC": ENTRADA_DIR / "CONTROLE_PC_LLMS.md",
    "README_PC": ENTRADA_DIR / "CONTROLE_PC_README.md",
    "ARTIGO_INTEIRO_CONTROLE": ARTIGO,
}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def medir(tok, path):
    data = path.read_bytes()
    texto = data.decode("utf-8")
    palavras = len(PALAVRA_RE.findall(texto))
    tokens = len(tok.encode(texto).ids)
    return {
        "arquivo": path.name,
        "bytes": len(data),
        "palavras": palavras,
        "tokens_ref": tokens,
        "bytes_por_token": len(data) / tokens,
        "tokens_por_palavra": tokens / palavras,
        "sha256": sha256(path),
    }


def main():
    if not TOKENIZER.exists():
        raise FileNotFoundError(f"copie tokenizer.json para {TOKENIZER}")
    tok = Tokenizer.from_file(str(TOKENIZER))
    doc = {
        "tokenizador": {
            "nome": "Qwen/Qwen3.6-35B-A3B",
            "metodo": "tokenizers.Tokenizer.from_file; somente tokenizer.json; add_special_tokens padrão da revisão",
            "biblioteca_tokenizers": tokenizers_pkg.__version__,
            "arquivo_local": TOKENIZER.name,
            "bytes_tokenizer": TOKENIZER.stat().st_size,
            "sha256_tokenizer": sha256(TOKENIZER),
            "snapshot_referencia": "995ad96eacd98c81ed38be0c5b274b04031597b0",
            "pesos_ou_modelo_lidos": False,
        },
        "fallback_bytes_v1": "histórico; não é proxy válido de tokens e não orienta o desenho",
        "arquivos": {},
    }
    for nome, path in ARQUIVOS.items():
        if not path.exists():
            raise FileNotFoundError(path)
        doc["arquivos"][nome] = medir(tok, path)
    artigo = doc["arquivos"]["ARTIGO_INTEIRO_CONTROLE"]
    artigo["tokens_esperados_revisao"] = ESPERADO_ARTIGO
    artigo["confere_revisao"] = artigo["tokens_ref"] == ESPERADO_ARTIGO
    artigo["sha256_artigo_usado_na_revisao"] = sha256(ARTIGO_REVISAO)
    artigo["artigo_publico_byte_identico_ao_da_revisao"] = artigo["sha256"] == artigo["sha256_artigo_usado_na_revisao"]
    if not artigo["confere_revisao"] or not artigo["artigo_publico_byte_identico_ao_da_revisao"]:
        raise RuntimeError(
            f"controle divergiu: {artigo['tokens_ref']} tokens, esperado {ESPERADO_ARTIGO}; "
            f"hash público={artigo['sha256']}, revisão={artigo['sha256_artigo_usado_na_revisao']}"
        )
    SAIDA.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({k: v["tokens_ref"] for k, v in doc["arquivos"].items()}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
