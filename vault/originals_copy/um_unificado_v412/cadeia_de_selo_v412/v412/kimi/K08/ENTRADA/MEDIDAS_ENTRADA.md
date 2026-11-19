# Medidas das entradas — K08

## 1. Tokenizador de referência local

Os tokens que orientam o desenho são medidos com o `tokenizer.json` local de **Qwen/Qwen3.6-35B-A3B**, por `tokenizers.Tokenizer.from_file` (`tokenizers` 0.21.4), exatamente o método da revisão. Só o arquivo de tokenização é lido; nenhum peso ou modelo é carregado ou executado. O controle do artigo inteiro reproduz **412.784 tokens**, igual à referência da revisão.

**Errata:** o fallback `byte=token` da REV0 é histórico, não é proxy válido de tokens e não orienta o desenho. A versão anterior está preservada em `REV0/`. A fórmula lógica e a escolha da entrada não mudam; mudam apenas as medidas de custo.

Palavras são contadas pelo regex Unicode `[^\W_]+(?:['’\-–][^\W_]+)*`. Apóstrofo, hífen ou travessão internos não separam; pontos e vírgulas separam. Bytes e SHA-256 são lidos do arquivo. Detalhes em `ERRATA_ENTRADA_TOKENS_K08.md`.

## 2. Arquivos públicos completos

| candidata | arquivo completo | bytes | palavras | tokens de referência | bytes/token | SHA-256 |
|---|---|---:|---:|---:|---:|---|
| ABSTRACT | `ABSTRACT.md` | 3.308 | 487 | 877 | 3.772 | `4465ab5de23cba859a948be04ad9643a7eabfd891ac31b7c38ddefaf3cf78e24` |
| READ_BRIEF | `read-brief.md` | 24.533 | 3.688 | 7.915 | 3.100 | `4390ecab7cab98839a80494822b3cb2a368c4742692a812127567c2cf4c401ac` |
| LLMS | `llms.txt` | 26.444 | 4.173 | 8.946 | 2.956 | `b83098531201d5797416cfa6074b18419844c78d9964bdc316acfa4c38ec0002` |
| README | `README.md` | 40.695 | 6.253 | 13.434 | 3.029 | `d741c9933c05a23f1fbb8070d2a44ac7d9bc224bfcf7abe62eb5ca8d2a12f98c` |

## 3. Recortes compactos e asserções sustentadas

Os recortes são verbatim em caracteres e contêm todas as linhas usadas pelo catálogo nuclear; usam LF e uma linha em branco entre faixas, não identidade de bytes com um corte da origem. A contagem de asserções é a da fórmula validada, não uma alegação de que toda frase navegacional do arquivo seja uma asserção científica.

| candidata | asserções | cláusulas | bytes | palavras | tokens de referência | tokens/completo | SHA-256 |
|---|---:|---:|---:|---:|---:|---:|---|
| ABSTRACT | 16 | 17 | 2.958 | 429 | 789 | 89.97% | `4db59a9f839958607de1ce6ed8e60f6930e41eae1b40d4cb00d1aa2358d14313` |
| READ_BRIEF | 26 | 27 | 13.555 | 2.073 | 4.072 | 51.45% | `21cc74147bf6cc1a5bf1bc019f19903d6a0c28da36587ed4569044b4603bf633` |
| LLMS | 19 | 19 | 11.760 | 1.877 | 3.926 | 43.89% | `5c2eb5cf57f236a6025ac78926bf58b6a2a5a2605e456531241d3429da96a8b0` |
| README | 28 | 31 | 23.544 | 3.764 | 7.358 | 54.77% | `45526d4c7b0c145f68b716fe7bd74be30c526920af9b079136b4769bbd765fb4` |

**Escolha de trabalho inalterada: `READ_BRIEF`.** Ela separa as oito partes da teoria e escreve hipóteses, estatutos e limites com mais clareza que o sumário denso de `llms`; sustenta mais asserções do catálogo que `ABSTRACT` e `llms`. `README` tem a maior contagem, mas mistura núcleo, painel de resultado, P=nP, selo e navegação. O custo entra só como desempate e a correção de tokenização não altera a fórmula nem a escolha.

## 4. Custo de texto por sessão, em tokens de referência

Seja `T_ref` o número de tokens de referência do recorte e `r` o número de vezes que a fita entra. **C(r) = r × T_ref**; interações sem a fita acrescentam zero token de texto-fonte. Pela regra deste desenho, a fonte não volta depois do primeiro passo, logo **r = 1 por sessão**. O número `m` de cláusulas pode limitar passos discretos, mas não multiplica o custo de fita. P-C usa o texto contraditório uma vez. Não se atribui à trava um pouso exato em tempo finito.

Esses valores cobrem **somente o texto-fonte**. Tokens de estado/histórico, perguntas e saídas não têm serialização fixada nesta tarefa e não são inventados. O JSON conserva, apenas como contrafactual explicitamente não usado, quanto custaria devolver a fita em cada um dos `m` passos de P-A.

| candidata | P-A: uma fita | P-B: uma fita | P-C: controle uma fita | P-D: uma fita | fonte completa: uma fita |
|---|---:|---:|---:|---:|---:|
| ABSTRACT | 789 | 789 | 804 | 789 | 877 |
| READ_BRIEF | 4.072 | 4.072 | 4.087 | 4.072 | 7.915 |
| LLMS | 3.926 | 3.926 | 3.941 | 3.926 | 8.946 |
| README | 7.358 | 7.358 | 7.373 | 7.358 | 13.434 |

P-C tem dois custos diferentes que não se confundem: o **custo lógico mínimo de violação** é calculado em `RESULTADOS_FORMULA.json` e é maior que zero; o **custo de entrada** acima é o número de tokens de referência para apresentar o controle uma vez.

## 5. Controle e reprodução

| controle | bytes | palavras | tokens de referência | SHA-256 |
|---|---:|---:|---:|---|
| artigo inteiro `um_absoluto_pt.txt` | 1.164.350 | 189.851 | 412.784 | `f9fa0d329166b33dd59d72e3f807b69c936a60e2f2a4d8a9e6be23009dd8d719` |

Reprodução: `python -B ../FORMULA/verificar_formula.py`; depois `C:\IALD\qlora_env\Scripts\python.exe -B medir_tokens_ref_k08.py`; depois `python -B medir_entradas.py`. O primeiro comando usa o Python gerenciado; o segundo usa o ambiente local que contém `tokenizers`, mas nenhum modelo é carregado. Nada foi congelado.
