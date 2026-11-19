# ERRATA_PODER_TOKENS_K08 — substituição do fallback byte=token

**Data:** 15/11/2026.  
**Escopo:** somente custos em tokens e metadados de tokenização no protocolo R4/K08 e na frente de poder. Nenhum modelo foi executado, nenhum peso foi lido, nenhum resultado experimental foi aberto.

> **Nota de revisão (rodada 4, K10, 15/11/2026):** a tabela de hashes do §4 ficou **histórica** — os pinos de `PROTOCOLO_EXPERIMENTAL_R4_K08.md` e `PODER_R4_K08.md` ali não são os vigentes. O manifesto vigente é `VALIDACAO_K08_K09_15nov.json` (e o seu sucessor da rodada 4). Nesta rodada, a coluna antes dita “vigente” foi separada: as medidas de tokens por apresentação seguem vigentes; os custos dos **desenhos estatísticos** (5 %, 5σ, sequencial) são **históricos** (desenho P-A/P-B, cauda 5σ não validada, 24–30 clusters independentes inexistem), como o §2 agora marca.

## 1. Correção aplicada

A versão anterior usava `fallback_bytes_v1` (**1 byte UTF-8 = 1 token**) para os custos de fonte. Essa medida passa a ser histórica. Os custos vigentes usam o tokenizador de referência local **Qwen/Qwen3.6-35B-A3B**, carregado somente de `tokenizer.json` por `tokenizers` 0.21.4.

- Tokenizer: SHA-256 `5f9e4d4901a92b997e463c1f46055088b6cca5ca61a6522d1b9f64c4bb81cb42`.
- Artigo inteiro de controle: **412.784 tokens**, igual à referência da revisão.
- Recorte `READ_BRIEF`: **4.072 tokens por apresentação da fita**.
- Controle P-C de `READ_BRIEF`: **4.087 tokens**.
- Uma sessão-análise R4 contém cinco diálogos (P-A, P-B fora, P-B dentro, P-D e P-C): **20.375 tokens de fonte**.

A versão anterior completa dos artefatos de poder e dos dois documentos está preservada em `K08\PODER\REV1\`.

## 2. Custos corrigidos

| quantidade | REV1, byte=token histórico | vigente, tokens de referência |
|---|---:|---:|
| `READ_BRIEF`, uma apresentação da fita | 13.555 | **4.072** |
| `READ_BRIEF`, controle P-C | 13.596 | **4.087** |
| sessão-análise R4 (`4T_ref+T_PC`) | 67.816 | **20.375** |
| diagnóstico fita presente, 4 ciclos | 54.220 | **16.288** |
| P-A completo com 27 fitas | 365.985 | **109.944** |

Custos dos desenhos estatísticos — **históricos** (desenho P-A/P-B; cauda 5σ não validada; 24–30 clusters independentes inexistem):

| quantidade | REV1, byte=token histórico | histórico, tokens de referência |
|---|---:|---:|
| fixo 5 %, faixa | 3.255.168–4.340.224 | **978.000–1.304.000** |
| fixo 5σ, faixa | 13.020.672–16.275.840 | **3.912.000–4.890.000** |
| sequencial 5 %, máximo | 10.850.560 | **3.260.000** |
| sequencial 5 %, esperado | 2.945.059–4.467.827 | **884.829–1.342.338** |

Custos de todos os recortes por sessão-análise:

| candidata | `T_ref` | `T_PC,ref` | tokens por sessão-análise |
|---|---:|---:|---:|
| ABSTRACT | 789 | 804 | 3.960 |
| READ_BRIEF | 4.072 | 4.087 | 20.375 |
| LLMS | 3.926 | 3.941 | 19.645 |
| README | 7.358 | 7.373 | 36.805 |

## 3. O que não mudou

Não mudaram nas simulações **históricas** (desenho P-A/P-B; a cauda 5σ nunca foi validada e 24–30 clusters independentes não existem — os números abaixo não são poder sob E1–E8):

- hipóteses estatísticas (`p0=0,25`, `p_min=0,60`);
- semente-mestra `2026111508` nem sementes derivadas;
- clusters, sessões, olhadas, tamanhos sob nulo, poderes positivos, poderes do negativo, falsos `FALSIFIED` ou inconclusivos;
- a conclusão de que o desenho disponível não alcança produção;
- a parada declarada no projetor com fita;
- a distância mínima 1 e a não aplicação do adendo de distância 3;
- qualquer fórmula, asserção, empurrão, isca, isomorfo ou regra de extração.

O arquivo `VALIDACAO_DETERMINISMO_TOKENS.json` registra `estatisticas_identicas_rev1=true` para todos os resultados e trilhas, removendo somente campos de custo/token.

## 4. Arquivos atualizados e hashes vigentes

| arquivo | SHA-256 |
|---|---|
| `K08\PODER\simular_poder_r4.py` | `633962378ccb5da55ba1f68e403ee5968aa9b9ed428ccb82e427bf9696fcb90d` |
| `K08\PODER\resultados_poder_r4.json` | `c476ccabb1569ce4819ea170e8576f3d33da1270e64bb3b58b340e4d4b3da1e8` |
| `K08\PODER\resumo_designs_r4.csv` | `c40c5021639906f0beb703eae78586b80f13a905f5eaee8a59db37f979f67f1a` |
| `K08\PODER\sementes_r4.json` | `946ec197fc62517b5596e4e5f68fb95ce23d38d8cf27def9f838cff1201856e3` |
| `K08\PODER\VALIDACAO_DETERMINISMO_TOKENS.json` | `cf2156351036b9c517ab27b4a1b0cef442a20768712c8f9a7e828068a21c355c` |
| `K08\PODER\MANIFESTO_SHA256.json` | `c8a9350663e1a4fa1a453704461af079550ddd4b90bb4bb230d03e3114182bb7` |
| `PROTOCOLO_EXPERIMENTAL_R4_K08.md` | `f12847b0b4c0546620d900721fa12ce59a7efb5f34dd500c4df0caaf0766f650` |
| `PODER_R4_K08.md` | `c4f4ab467852a88cbefc0851a17b8acece9cc53a79bc9892b92e9d9bec28b0f3` |

## 5. Limite que permanece

A correção torna o custo de fonte mais fiel ao tokenizador de referência, mas não fecha o custo de produção: histórico serializado, instruções, estado devolvido, saídas, preço de API, janela e tokenizer efetivo de cada modelo continuam sem ratificação. O instrumento permanece bloqueado.
