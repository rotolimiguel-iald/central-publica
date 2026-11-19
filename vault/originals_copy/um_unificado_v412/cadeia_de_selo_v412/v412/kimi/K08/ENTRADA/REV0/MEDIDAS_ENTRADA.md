# Medidas das entradas — K08

## 1. Método exato, sem modelo

Não havia `tiktoken`, `tokenizers`, `transformers` ou `sentencepiece` no Python gerenciado. O executável local de tokenização do llama.cpp exige um modelo/pesos e por isso não foi usado. Em vez de baixar pesos ou apresentar uma estimativa como contagem de referência, adoto **`fallback_bytes_v1`: cada byte UTF-8 é exatamente um token**. Assim, nesta tabela, tokens = bytes por definição. É um tokenizador determinístico de 256 símbolos, sem modelo; **não é cl100k/o200k nem uma previsão do custo de um modelo específico**.

Palavras são contadas pelo regex Unicode `[^\W_]+(?:['’\-–][^\W_]+)*`. Apóstrofo, hífen ou travessão internos não separam; pontos e vírgulas separam. Bytes e SHA-256 são lidos do arquivo, nunca copiados de memória.

## 2. Arquivos públicos completos

| candidata | arquivo completo | bytes | palavras | tokens fallback | SHA-256 |
|---|---|---:|---:|---:|---|
| ABSTRACT | `ABSTRACT.md` | 3.308 | 487 | 3.308 | `4465ab5de23cba859a948be04ad9643a7eabfd891ac31b7c38ddefaf3cf78e24` |
| READ_BRIEF | `read-brief.md` | 24.533 | 3.688 | 24.533 | `4390ecab7cab98839a80494822b3cb2a368c4742692a812127567c2cf4c401ac` |
| LLMS | `llms.txt` | 26.444 | 4.173 | 26.444 | `b83098531201d5797416cfa6074b18419844c78d9964bdc316acfa4c38ec0002` |
| README | `README.md` | 40.695 | 6.253 | 40.695 | `d741c9933c05a23f1fbb8070d2a44ac7d9bc224bfcf7abe62eb5ca8d2a12f98c` |

## 3. Recortes compactos e asserções sustentadas

Os recortes são verbatim em caracteres e contêm todas as linhas usadas pelo catálogo nuclear; usam LF e uma linha em branco entre faixas, não identidade de bytes com um corte da origem. A contagem de asserções é a da fórmula validada, não uma alegação de que toda frase navegacional do arquivo seja uma asserção científica.

| candidata | asserções | cláusulas | bytes | palavras | tokens fallback | tokens/completo | SHA-256 |
|---|---:|---:|---:|---:|---:|---:|---|
| ABSTRACT | 16 | 17 | 2.958 | 429 | 2.958 | 89.42% | `4db59a9f839958607de1ce6ed8e60f6930e41eae1b40d4cb00d1aa2358d14313` |
| READ_BRIEF | 26 | 27 | 13.555 | 2.073 | 13.555 | 55.25% | `21cc74147bf6cc1a5bf1bc019f19903d6a0c28da36587ed4569044b4603bf633` |
| LLMS | 19 | 19 | 11.760 | 1.877 | 11.760 | 44.47% | `5c2eb5cf57f236a6025ac78926bf58b6a2a5a2605e456531241d3429da96a8b0` |
| README | 28 | 31 | 23.544 | 3.764 | 23.544 | 57.85% | `45526d4c7b0c145f68b716fe7bd74be30c526920af9b079136b4769bbd765fb4` |

**Escolha de trabalho: `READ_BRIEF`.** Ela separa as oito partes da teoria e escreve hipóteses, estatutos e limites com mais clareza que o sumário denso de `llms`; sustenta mais asserções do catálogo que `ABSTRACT` e `llms`. `README` tem a maior contagem, mas mistura núcleo, painel de resultado, P=nP, selo e navegação. O custo entra só como desempate. A escolha não usa nenhuma expectativa de desfecho.

## 4. Custo de texto por sessão, em tokens

Seja `T` o número de tokens do recorte e `r` o número de vezes que a fita entra. **C(r) = r × T**; interações sem a fita acrescentam zero token de texto-fonte. Pela regra deste desenho, a fonte não volta depois do primeiro passo, logo **r = 1 por sessão**. O número `m` de cláusulas pode limitar passos discretos, mas não multiplica o custo de fita. P-C usa o texto contraditório uma vez. Não se atribui à trava um pouso exato em tempo finito.

Esses valores cobrem **somente o texto-fonte**. Tokens de estado/histórico, perguntas e saídas não têm serialização fixada nesta tarefa e não são inventados. O JSON conserva, apenas como contrafactual explicitamente não usado, quanto custaria devolver a fita em cada um dos `m` passos de P-A.

| candidata | P-A: uma fita | P-B: uma fita | P-C: controle uma fita | P-D: uma fita | fonte completa: uma fita |
|---|---:|---:|---:|---:|---:|
| ABSTRACT | 2.958 | 2.958 | 2.999 | 2.958 | 3.308 |
| READ_BRIEF | 13.555 | 13.555 | 13.596 | 13.555 | 24.533 |
| LLMS | 11.760 | 11.760 | 11.801 | 11.760 | 26.444 |
| README | 23.544 | 23.544 | 23.585 | 23.544 | 40.695 |

P-C tem dois custos diferentes que não se confundem: o **custo lógico mínimo de violação** é calculado em `RESULTADOS_FORMULA.json` e é maior que zero; o **custo de entrada** acima é o número de tokens para apresentar o controle uma vez.

## 5. Reprodução

Executar primeiro `python -B ../FORMULA/verificar_formula.py` e depois `python -B medir_entradas.py`. O segundo script não escolhe automaticamente outro tokenizador se uma biblioteca aparecer: ele falha para que a mudança de método seja explícita. Nenhum modelo foi executado; nada foi congelado.
