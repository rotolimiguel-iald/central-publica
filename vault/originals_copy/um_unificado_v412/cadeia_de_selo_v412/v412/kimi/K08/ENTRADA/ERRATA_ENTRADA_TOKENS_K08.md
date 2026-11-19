# Errata — tokens das entradas K08

## Correção

A REV0 apresentou `fallback_bytes_v1` (um token por byte UTF-8) como método exato disponível. Isso foi insuficiente para a ordem K08: **o fallback byte=token fica como histórico, não é proxy válido de tokens e não orienta o desenho**. Os números que orientam o desenho são os do tokenizador de referência local **Qwen/Qwen3.6-35B-A3B**, medidos somente a partir de `tokenizer.json`.

## Por que a REV0 errou

A REV0 verificou `tiktoken`, `tokenizers`, `transformers` e `sentencepiece` apenas no Python gerenciado e concluiu indevidamente que não havia referência local. O ambiente do projeto `C:\IALD\qlora_env` contém `tokenizers` 0.21.4, e o cache local contém o `tokenizer.json` usado pela revisão. Nenhum peso ou modelo foi necessário ou executado.

| tokenizador | arquivo | bytes | SHA-256 | biblioteca |
|---|---|---:|---|---|
| Qwen/Qwen3.6-35B-A3B | `TOKENIZER_QWEN3_6_35B_A3B.json` | 12.807.982 | `5f9e4d4901a92b997e463c1f46055088b6cca5ca61a6522d1b9f64c4bb81cb42` | tokenizers 0.21.4 |

## Controle do artigo inteiro

O artigo inteiro usado pela revisão é byte-idêntico ao espelho público (`sha256` igual nos dois caminhos). A contagem reproduz a referência:

| arquivo | bytes | palavras | tokens de referência | esperado pela revisão | confere | SHA-256 |
|---|---:|---:|---:|---:|---|---|
| `um_absoluto_pt.txt` | 1.164.350 | 189.851 | 412.784 | 412.784 | true | `f9fa0d329166b33dd59d72e3f807b69c936a60e2f2a4d8a9e6be23009dd8d719` |

## Substituição das medidas

| candidata | recorte REV0: byte=token histórico | recorte: tokens de referência | completo REV0: byte=token histórico | completo: tokens de referência |
|---|---:|---:|---:|---:|
| ABSTRACT | 2.958 | 789 | 3.308 | 877 |
| READ_BRIEF | 13.555 | 4.072 | 24.533 | 7.915 |
| LLMS | 11.760 | 3.926 | 26.444 | 8.946 |
| README | 23.544 | 7.358 | 40.695 | 13.434 |

Como a fonte entra uma única vez por sessão, os custos de texto correntes por sessão são:

| candidata | P-A | P-B | P-C | P-D | fonte completa, comparação |
|---|---:|---:|---:|---:|---:|
| ABSTRACT | 789 | 789 | 804 | 789 | 877 |
| READ_BRIEF | 4.072 | 4.072 | 4.087 | 4.072 | 7.915 |
| LLMS | 3.926 | 3.926 | 3.941 | 3.926 | 8.946 |
| README | 7.358 | 7.358 | 7.373 | 7.358 | 13.434 |

## O que não muda

Não muda nenhuma cláusula, leitura, empurrão, prova SAT/UNSAT, redundância, tabela adversarial ou a escolha `READ_BRIEF`. A escolha foi por clareza e completude e não foi reescolhida pelo novo custo. Os hashes dos textos recortados e dos controles são os mesmos da REV0; só a coluna de tokens deixou de ser byte=token.

A versão anterior completa da pasta `ENTRADA` está preservada em `REV0/`.

## Reprodução

1. `python -B ../FORMULA/verificar_formula.py` (fórmula e arquivos; Python gerenciado).
2. `C:\IALD\qlora_env\Scripts\python.exe -B medir_tokens_ref_k08.py` (só `tokenizer.json`; sem pesos/modelo).
3. `python -B medir_entradas.py` (consolida medidas).
4. `python -B gerar_errata_tokens.py` (esta errata).

O hash corrente desta errata consta do manifesto de entrada, não dentro do próprio texto.
