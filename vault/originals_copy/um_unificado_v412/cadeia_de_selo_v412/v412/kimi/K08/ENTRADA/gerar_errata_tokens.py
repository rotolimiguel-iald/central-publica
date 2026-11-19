#!/usr/bin/env python3
"""Gera a errata de tokens a partir dos JSON medidos; nada é digitado à mão."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ENTRADA_DIR = Path(__file__).resolve().parent
REV0 = json.loads((ENTRADA_DIR / "REV0" / "MEDIDAS_ENTRADA.json").read_text(encoding="utf-8"))
REF = json.loads((ENTRADA_DIR / "TOKENS_REF_K08.json").read_text(encoding="utf-8"))
ATUAL = json.loads((ENTRADA_DIR / "MEDIDAS_ENTRADA.json").read_text(encoding="utf-8"))
SAIDA = ENTRADA_DIR / "ERRATA_ENTRADA_TOKENS_K08.md"

NOMES = ("ABSTRACT", "READ_BRIEF", "LLMS", "README")


def fmt(n):
    return f"{n:,}".replace(",", ".")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    artigo = REF["arquivos"]["ARTIGO_INTEIRO_CONTROLE"]
    tok = REF["tokenizador"]
    L = []
    add = L.append
    add("# Errata — tokens das entradas K08")
    add("")
    add("## Correção")
    add("")
    add("A REV0 apresentou `fallback_bytes_v1` (um token por byte UTF-8) como método exato disponível. Isso foi insuficiente para a ordem K08: **o fallback byte=token fica como histórico, não é proxy válido de tokens e não orienta o desenho**. Os números que orientam o desenho são os do tokenizador de referência local **Qwen/Qwen3.6-35B-A3B**, medidos somente a partir de `tokenizer.json`.")
    add("")
    add("## Por que a REV0 errou")
    add("")
    add("A REV0 verificou `tiktoken`, `tokenizers`, `transformers` e `sentencepiece` apenas no Python gerenciado e concluiu indevidamente que não havia referência local. O ambiente do projeto `C:\\IALD\\qlora_env` contém `tokenizers` 0.21.4, e o cache local contém o `tokenizer.json` usado pela revisão. Nenhum peso ou modelo foi necessário ou executado.")
    add("")
    add("| tokenizador | arquivo | bytes | SHA-256 | biblioteca |")
    add("|---|---|---:|---|---|")
    add(f"| {tok['nome']} | `{tok['arquivo_local']}` | {fmt(tok['bytes_tokenizer'])} | `{tok['sha256_tokenizer']}` | tokenizers {tok['biblioteca_tokenizers']} |")
    add("")
    add("## Controle do artigo inteiro")
    add("")
    add("O artigo inteiro usado pela revisão é byte-idêntico ao espelho público (`sha256` igual nos dois caminhos). A contagem reproduz a referência:")
    add("")
    add("| arquivo | bytes | palavras | tokens de referência | esperado pela revisão | confere | SHA-256 |")
    add("|---|---:|---:|---:|---:|---|---|")
    add(f"| `um_absoluto_pt.txt` | {fmt(artigo['bytes'])} | {fmt(artigo['palavras'])} | {fmt(artigo['tokens_ref'])} | {fmt(artigo['tokens_esperados_revisao'])} | {str(artigo['confere_revisao']).lower()} | `{artigo['sha256']}` |")
    add("")
    add("## Substituição das medidas")
    add("")
    add("| candidata | recorte REV0: byte=token histórico | recorte: tokens de referência | completo REV0: byte=token histórico | completo: tokens de referência |")
    add("|---|---:|---:|---:|---:|")
    for nome in NOMES:
        antigo = REV0["candidatas"][nome]
        add(f"| {nome} | {fmt(antigo['compacto']['tokens'])} | {fmt(REF['arquivos'][nome + '_RECORTE']['tokens_ref'])} | {fmt(antigo['completo']['tokens'])} | {fmt(REF['arquivos'][nome + '_COMPLETO']['tokens_ref'])} |")
    add("")
    add("Como a fonte entra uma única vez por sessão, os custos de texto correntes por sessão são:")
    add("")
    add("| candidata | P-A | P-B | P-C | P-D | fonte completa, comparação |")
    add("|---|---:|---:|---:|---:|---:|")
    for nome in NOMES:
        c = ATUAL["candidatas"][nome]["custo_texto"]
        add(f"| {nome} | {fmt(c['P_A_fonte_so_no_primeiro_passo'])} | {fmt(c['P_B_fonte_so_no_primeiro_passo'])} | {fmt(c['P_C_controle_so_no_primeiro_passo'])} | {fmt(c['P_D_fonte_so_no_primeiro_passo'])} | {fmt(c['fonte_completa_uma_fita_para_comparacao'])} |")
    add("")
    add("## O que não muda")
    add("")
    add("Não muda nenhuma cláusula, leitura, empurrão, prova SAT/UNSAT, redundância, tabela adversarial ou a escolha `READ_BRIEF`. A escolha foi por clareza e completude e não foi reescolhida pelo novo custo. Os hashes dos textos recortados e dos controles são os mesmos da REV0; só a coluna de tokens deixou de ser byte=token.")
    add("")
    add("A versão anterior completa da pasta `ENTRADA` está preservada em `REV0/`.")
    add("")
    add("## Reprodução")
    add("")
    add("1. `python -B ../FORMULA/verificar_formula.py` (fórmula e arquivos; Python gerenciado).")
    add("2. `C:\\IALD\\qlora_env\\Scripts\\python.exe -B medir_tokens_ref_k08.py` (só `tokenizer.json`; sem pesos/modelo).")
    add("3. `python -B medir_entradas.py` (consolida medidas).")
    add("4. `python -B gerar_errata_tokens.py` (esta errata).")
    add("")
    add("O hash corrente desta errata consta do manifesto de entrada, não dentro do próprio texto.")
    SAIDA.write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"errata": str(SAIDA), "sha256": sha(SAIDA)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
