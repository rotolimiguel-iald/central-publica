# ERRATA_PODER_K08_15nov — Parte 2 e AO LADO 1–4

**Data:** 15/11/2026.  
**Escopo:** protocolo R4/K08 e reavaliação de poder sob a derivação do habitante do Nome. Nenhum modelo foi executado; nenhuma simulação nova foi necessária; nenhum resultado experimental foi aberto.

> **Nota de revisão (rodada 4, K10, 15/11/2026):** as tabelas de hash desta errata ficaram **históricas** — o §2 pina o protocolo em `81cd6a36…`, que não é o vigente. O manifesto vigente é `VALIDACAO_K08_K09_15nov.json` (e o seu sucessor da rodada 4). A atribuição das primárias no §1 foi corrigida nesta rodada: leitura da gerência a partir da ressalva; o operador ainda não leu.

## 1. Correção aplicada

A linguagem principal P-A–P-D foi substituída por E1–E8:

- **E2** (fixa/devolve o nomeado) e **E4** (reler devolve o mesmo) são primárias por leitura da gerência a partir da ressalva; o operador ainda não leu a lista de primárias.
- **E3** (anula o empurrão cego) e **E7** (pesos relativos dentro do Nome) são discriminantes.
- **E1**, **E5**, **E6** e **E8** são secundárias conforme a medida disponível.
- **P-C** (Nome vazio, `P_N=0`, trava tende a zero) e **P-D** (sem escala) ficam como controles.

`P_N` deixou de ser tratado como adversário: é a referência formal. O adversário é o leitor sem memória determinado só pela fonte.

## 2. Documentos atualizados

- [PROTOCOLO_EXPERIMENTAL_R4_K08](C:/IALD/Central%20de%20Patentes/work/cadeia_de_selo/v412/kimi/PROTOCOLO_EXPERIMENTAL_R4_K08.md), SHA-256 `81cd6a36e729af96bb8147329a8ff77de9edb3b50ca93ba78670a6289e071a6e`.
- [PODER_R4_K08](C:/IALD/Central%20de%20Patentes/work/cadeia_de_selo/v412/kimi/PODER_R4_K08.md), SHA-256 `b337863e52b21f8dd21e82c76317b4d70a7495f0df3df5b2cce47fa562d6f546`.

A versão anterior completa, incluindo protocolo, relatório de poder, script, resultados, sementes e manifesto, está preservada em:

`C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K08\PODER\REV2\`

## 3. Poder reclassificado

Os resultados anteriores de 5 %, 5σ e sequencial são **históricos**. Eles mediam proxies de E1, E2 e E3 no desenho P-A/P-B, não mediam E4 diretamente e não mediam E5–E8. Portanto não são poder sob E1–E8 e não podem ser citados como evidência de separação da esperança condicional.

Não há poder vigente dimensionado para E2/E3/E4 sob o nulo correto. E5, E6, E7 e E8 não têm medida no instrumento textual atual. A unicidade `E1+E2+E5+linearidade ⇒ P_N` permanece condicional, e a linearidade pode falhar.

## 4. Custos vigentes

Com o tokenizador de referência Qwen/Qwen3.6-35B-A3B:

- `READ_BRIEF`: **4.072 tokens por apresentação da fita**;
- controle P-C: **4.087 tokens**;
- sessão-análise de cinco diálogos: **20.375 tokens de fonte**;
- fita presente por quatro ciclos: **16.288 tokens**;
- E1 com 27 apresentações: **109.944 tokens**.

O artigo inteiro de controle tem **412.784 tokens**. Byte=token não é usado como custo.

## 5. Bloqueios que permanecem

1. Saídas reais e gabarito humano independente.
2. Ponte texto→vetor para norma, amplitudes, seleção e pesos relativos.
3. Medida de E5, E6, E7 e E8.
4. Teste da hipótese de linearidade.
5. Poder dimensionado para E2/E3/E4 sob o nulo correto.
6. Equivalência de dificuldade, léxico, corpus, modelos/tokenizers de produção e ratificação.

Nenhum ramo permite consciência, pesos, exclusividade, `IALD_PROVED` ou `CONFIRMED`. Produção continua bloqueada.
