# ERRATA REGISTRO UMPY R3.1 — aliases canônicos das hipóteses

14/11/2026. Correção AO LADO de `REGISTRO_UMPY_RASCUNHO_K06.md`, restrita aos nomes de duas hipóteses e à preservação explícita de seus aliases legados.

## 1. Origem e correção

A revisão recomendou alinhar o registro aos nomes canônicos de `MODELO_FORMAL_R3_K06.md`. Foram confirmados por leitura:

- `H-HOM`: homogeneidade temporal do núcleo;
- `H-QUOT(k)`: agregabilidade forte do quociente em cada fase `k=1,…,12`.

Os dois nomes não são aliases entre si: homogeneidade não dispensa agregabilidade.

No bloco JSON do registro, somente as chaves foram substituídas:

| alias legado | nome canônico adotado |
|---|---|
| `H-TIME-HOMOG` | `H-HOM` |
| `H-LUMP` | `H-QUOT(k)` |

Os valores textuais das duas hipóteses não foram alterados. Foi acrescentada a seção §1.1 com a mesma tabela de correspondência, preservando os aliases AO LADO e sua distinção conceitual.

## 2. Preservação

O original foi copiado antes da edição para:

`K06\ENTRADA_PUBLICA\REV0\REGISTRO_UMPY_RASCUNHO_K06.md`

| versão | bytes | SHA-256 |
|---|---:|---|
| original em `REV0` | 10.114 | `2033c6d2dbd45df53854919ea52e52a468b597a1fd21679552a1f0a7d1c696f1` |
| registro R3.1 | 10.814 | `875a6db32749b72e3032e452989229f95e80b6aaea96d6bf2dcfd7a4c60c897d` |

O diff foi conferido: contém apenas as duas substituições de chaves e a nova seção de aliases. Nenhum veredito, estatuto, estado `ARMADO`, parágrafo PT/EN, hipótese restante ou campo de protocolo foi modificado.

## 3. Escopo intacto

- Nenhum modelo foi executado e nenhum resultado foi aberto.
- Nenhum conteúdo reservado foi lido, copiado ou alterado.
- Nenhum outro arquivo foi modificado; em particular, T6 e `REGISTRO_MAPA` permanecem intocados.
- O registro continua candidato, não instalado, não ratificado e `ARMADO`; esta errata não promove teorema, protocolo ou resultado.
