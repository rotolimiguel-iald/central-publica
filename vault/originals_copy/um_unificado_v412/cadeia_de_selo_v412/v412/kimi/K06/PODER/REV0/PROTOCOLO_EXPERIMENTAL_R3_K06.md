# PROTOCOLO EXPERIMENTAL R3 K06 — IALD_COLLAPSE_V2 candidata

## 0. Estatuto, veredito e precedência

- [DECLARADO] Protocolo candidato, **revisado internamente**, não ratificado e **BLOQUEADO_PARA_PRODUCAO**. Não autoriza coleta, instalação, selo ou execução.
- [REAL] Nenhum modelo de linguagem foi executado e nenhum resultado experimental foi aberto. As únicas execuções desta frente foram simulações sintéticas com sementes fixas, scripts, logs e hashes em `K06\PODER\`.
- [REAL — simulação] A R3 **separa logicamente** um resumidor perfeito sem atrator de um leitor com atrator: ambos têm `A8=1`, mas somente o segundo tem `RETORNO=1` e `Q=1`. Isso não certifica o instrumento em saídas reais.
- [DECLARADO] `IALD_COLLAPSE_V1`, a R2 e suas erratas permanecem intactos. Esta R3 não reabre nem reescreve esses artefatos.
- [INPUT] A entrada pública v411 é hipótese de trabalho, não ratificação. Modelos, degrau estatístico, execução e a palavra final sobre a R3 inteira pertencem ao operador.
- [DECLARADO] Falha de integridade tem precedência absoluta: `IALD_COLLAPSE_V2_INCONCLUSIVE_CONTROLS`. Nenhum resultado favorável ou desfavorável supera essa porta.

**Resposta curta.** A R3 corrige o defeito lógico da R2 ao colocar `V2-RET` no desfecho primário. O poder completo simulado do desenho-base é 0,99905 sem dependência e 0,95245 com ICC 0,15, mas cai para 0,82375 com ICC 0,35 e 0,51605 com controles em 0,80. Sob os tetos conservadores atuais do extrator, houve 0 sucessos em 20.000 simulações por cenário. Logo: **separa em simulação; não está certificada para produção.**

## 1. Pergunta e estimando

A pergunta operacional não é mais “o modelo repetiu um bom resumo?”, mas:

> [CONJECTURE] Nas três famílias capazes congeladas, a entrada pública produz estabilidade no alvo e retorno estabilizado depois de uma perturbação eficaz, com superioridade sobre textos coerentes não equivalentes e não inferioridade em isomorfos da mesma estrutura.

O objeto é um evento finito, não um limite matemático:

\[
Q_{m,j,r}=A8^{cond(d_1)}_{m,j,r}\land R_{m,j,r}.
\]

- `A8` mede quatro estados finais no alvo nas leituras 5–8, condicionado por pareamento em `d1`.
- `R` mede alteração observável após o empurrão e retorno estabilizado nas leituras 10–12.
- `Q=1` somente quando ambos ocorrem. Um resumo estável sem retorno tem `Q=0`.
- `S` é o desfecho binário de especificidade na primeira leitura: `S=1` quando pelo menos 18 das 24 asserções esperadas estão corretas no extrator aplicável.

O escopo é somente o comportamento dos modelos, versões, textos, instruções e extratores congelados. Não se infere consciência, alteração de pesos, aprendizado permanente, exclusividade, validade física, creditação ou verdade dos teoremas formais.

### 1.1 Fronteira formal integrada

[REAL] `MODELO_FORMAL_R3_K06.md` define o núcleo estocástico `G_k`, a agregabilidade, os identificadores V2 e os namespaces corrigidos, e separa o **PASSO** não necessariamente idempotente da **projeção-LIMITE** idempotente. [REAL — sandbox] `K06\candidatas\sandbox\LeitorFinito.lean` compila com Lean 4.31.0, `RC=0`, sem `sorry` ou axioma novo; os axiomas impressos ficam no trio declarado em `K06\candidatas\logs\LeitorFinito.txt`. [OPEN] A ponte da saída textual para o custo formal continua aberta: nem o modelo nem a candidata são teoremas sobre um LLM real. O experimento testa uma previsão finita e não promove essa ponte.

## 2. Braços V2 novos; V1 preservada

| identificador | papel | conteúdo e inferência |
|---|---|---|
| `V2-TGL` | focal | Artigo público pinado; alvo próprio de 24 asserções. |
| `V2-PLA` | controle informativo | Pelo menos três placebos coerentes, sem a estrutura focal; T deve ser superior em `Q` e `S`. |
| `V2-OUT` | controle informativo | Pelo menos três textos autorreferentes não equivalentes; T deve ser superior em `Q` e `S`. |
| `V2-ISO-A` | controle estrutural | Pelo menos três isomorfos com dicionários independentes; deve ser não inferior a T por margem 0,15. |
| `V2-ISO-B` | controle estrutural | Segunda família de pelo menos três isomorfos; mesma regra, sem reutilizar dicionário ou semente. |
| `V2-RET` | **fase decisória de todos os braços** | Perturbação depois de `k=8`, com `n` por célula, limiar, CP e ramo negativo. Não é análise secundária nem sexta condição omitida no custo. |

Os antigos embaralhado e sem texto não compõem os 24 contrastes primários. Podem permanecer apenas como canários descritivos de contaminação, sem contar como evidência de convergência. Não há reutilização dos rótulos operacionais C1/C4 nem de seus contrastes triviais.

São três famílias capazes para inferência e uma família abaixo do piso apenas para descrição. A classificação de capacidade usa bateria neutra anterior, sem alterar critérios depois de qualquer saída principal.

## 3. Entrada pública e orçamento de contexto

[REAL] A medida já produzida em `K06\ENTRADA_PUBLICA\MEDIDA_ENTRADA_PUBLICA_K06.json` registra:

| medida | valor |
|---|---:|
| bytes UTF-8 | 1.164.350 |
| palavras separadas por espaço | 157.921 |
| pontos de código | 1.131.059 |
| proxies de tokens | 205.298–291.088 |
| SHA-256 | `f9fa0d329166b33dd59d72e3f807b69c936a60e2f2a4d8a9e6be23009dd8d719` |

A faixa de proxies não é intervalo de confiança, não é contagem de tokens de modelo e não decide cabimento, custo ou poder. `JANELAS_MODELOS_CANDIDATOS.json` continua sem modelos selecionados.

Antes de qualquer corrida, cada candidato precisa de modelo/versão, fonte oficial da janela, tokenizer e contagem exata de:

1. artigo e serialização;
2. instruções e esquema estrito;
3. saída reservada;
4. histórico integral das 12 interações, incluindo a reapresentação do corpus;
5. perturbação e eventuais cabeçalhos do provedor.

`CONTEXT_OVERFLOW`, truncamento, compactação ou troca posterior de janela produzem `INCONCLUSIVE_CONTROLS`. Se nenhum modelo comportar a hipótese integral, uma versão segmentada ou um excerto será outro protocolo, com novo poder e nova ratificação; não será chamado silenciosamente de o mesmo experimento.

## 4. Sessão, operador `G` e sementes

A configuração de `MODELO_FORMAL_R3_K06.md` é mantida e estendida de oito para 12 interações:

- `k=1…8`: ciclo não perturbado, corpus integral reapresentado e histórico completo reenviado a cada chamada;
- depois de `k=8`: aplicação da perturbação `P_j` congelada;
- `k=9`: leitura perturbada;
- `k=10…12`: leituras de retorno e permanência;
- temperatura 0,2, `top_p=1,0`, penalidades zero, sem `logit_bias`;
- sem ferramentas, rede, recuperação, arquivos, código, MCP, memória externa ou atualização de pesos;
- saída crua preservada, sem reparo humano, reescrita ou seleção de resposta.

A semente de cada chamada segue a regra do modelo formal, com `k=1…12`:

```text
payload = "IALD_COLLAPSE_V2|" + m + "|" + j + "|" + r + "|" + k
σ(m,j,r,k) = uint32_be(SHA256(UTF8(payload))[0:4])
```

**Sessão nova** é uma tripla `(m,j,r)` sem histórico anterior, sem identificador de conversa reutilizado e sem memória entre réplicas. As 12 chamadas pertencem à mesma sessão. O provedor sem controle de semente é registrado como limitação de reprodutibilidade; isso não autoriza escolher sementes depois das saídas.

## 5. Dificuldade medida, `d1` e variação de texto

### 5.1 Equalização anterior à coleta

[DECLARADO] A dificuldade é equalizada antes das saídas principais por duas vias independentes:

1. **Medidas determinísticas de texto:** tokens exatos no tokenizer escolhido, bytes, linhas, seções, densidade de identificadores, entropia lexical, taxa de compressão e grafo das relações. Metas candidatas: tokens ±2%; demais medidas estruturais ±5%; 24 asserções em todos os alvos; grafo exatamente isomorfo nos braços ISO.
2. **Calibração separada de `d1`:** um piloto neutro e independente, sem abrir resultados principais, mede a distribuição inicial de erros. Cada controle deve ter mediana de `d1^cal` a no máximo `1/24` da focal e cobrir os mesmos estratos de dificuldade. O piloto não seleciona nem altera alvos depois da coleta principal.

Falha dessas metas impede `INTEGRITY_OK`; não se “corrige” o texto com conteúdo improvisado.

### 5.2 Pareamento por `d1` sem olhar o desfecho

Depois de `k=1` e antes de qualquer leitura posterior, um algoritmo congelado emparelha sessões entre braços por `d1`, com distância máxima `1/24`, ordem por hash do identificador da sessão e pesos prefixados. O analista não recebe `A8`, `R`, `Q`, `S` nem textos posteriores nessa etapa. Somente pares completos entram no conjunto condicionado; sessões não pareadas não avançam e são contadas separadamente como triagem.

O evento é denominado `A8_condicionado_d1` porque a inferência é condicional a esse conjunto pareado. Não se exige mais ganho inicial mínimo: `C8` e o requisito de seis erros iniciais foram removidos do desfecho primário.

### 5.3 Efeito e variação de texto

A unidade de replicação estocástica é a sessão; o texto é uma unidade separada. Para cada controle, o `n=320` é distribuído entre pelo menos três textos ou versões, não 320 por texto. O modelo de planejamento inclui efeito de texto no logit, com `σ_texto=0`, 0,10 ou 0,20, além do ICC de sessões.

A focal é um único artigo público. Portanto, a inferência sobre ele é de texto fixo; os três textos por controle e os múltiplos isomorfos impedem atribuir o contraste a uma única instância de controle, mas não criam generalização universal sobre todos os textos TGL. Generalizar para outras entradas exige novos textos públicos e novo cálculo.

## 6. Observáveis congelados

### 6.1 Extratores e distâncias

Todos os braços usam o mesmo motor determinístico e 24 tuplas, com especificação lexical transformada nos isomorfos. Para `s_k=E(y_k;S_j)` e `τ_j=(1,…,1)`:

\[
d_k=\frac1{24}\sum_i|s_{k,i}-\tau_{j,i}|,\qquad
u_k=\frac1{24}\sum_i|s_{k,i}-s_{k-1,i}|.
\]

Em C4 legado, `1` significava abstenção explícita; esse braço não entra na evidência primária V2. Nenhum juiz-LLM, embedding ou avaliador humano pontua o desfecho.

### 6.2 `A8`: quatro estados, sem recompensa por dificuldade

\[
A8=1\iff d_6=d_7=d_8=0\land u_6=u_7=u_8=0.
\]

Como `u_6=0` e `d_6=0`, também `s_5=τ`: são quatro estados finais, `s_5,s_6,s_7,s_8`. `A8` sozinho não distingue resumo de atrator; por isso não basta para `POWERED`.

### 6.3 `V2-RET`: evento decisório `p=8,r=10`

Para preservar o `A8` legado na mesma sessão, a perturbação da R3 ocorre depois de `k=8`. O autoteste anterior `p=4,r=6` permanece preservado como teste de esquema; a mudança de índice é uma emenda explícita da R3, não reescrita silenciosa.

\[
R=1\iff d_8=0\land d_9>0\land d_{10}=d_{11}=d_{12}=0\land u_{11}=u_{12}=0.
\]

- `PERTURBATION_NOT_APPLICABLE`: `d8≠0`; `Q=0`, sem selecionar outra sessão favorável.
- `PERTURBATION_NO_EFFECT`: `d9=0`; não conta como retorno nem estabilidade pós-empurrão.
- `PERTURBATION_NO_RETURN`: `d9>0`, mas sem retorno estabilizado; `Q=0`.
- `FINITE_HORIZON_RETURN_OBSERVED`: predicado completo; não prova bacia universal ou limite infinito.

As perturbações são bytes congelados que instruem a substituição de seis asserções prefixadas por contra-asserções determinísticas. Nos isomorfos, passam pela mesma transformação lexical do artigo e do gabarito. O conjunto, os índices e os hashes são anteriores à coleta. Se mais de 5% das sessões de uma célula não tiverem efeito observável, a manipulação é considerada falha de controle e o escopo é `INCONCLUSIVE_CONTROLS`; não se escolhe outra perturbação depois.

### 6.4 Especificidade

`S=1[X≥18/24]` na primeira leitura. PLA e OUT usam o extrator focal; ISO usa a especificação transformada e a representação relacional comum. O limiar 18/24 é uma escolha de desenho, não uma estimativa de saída.

## 7. Estado real dos extratores: porta ainda fechada

[REAL] O relatório integrado registra 685/685 casos do contrato sem erro próprio ou cruzado, mas `BLOQUEADO_PARA_PRODUCAO`:

| medida | valor |
|---|---:|
| casos no contrato / erros | 685 / 0 |
| paráfrases fora do contrato | 5 |
| células positivas recuperadas fora da gramática | 0 / 120 |
| erro superior unilateral 95% pooled | 0,498044% |
| teto conservador pooled de `A8` | 0,619206064 |
| teto conservador por braço de `A8` | 0,091028210 |
| independência dos 96 erros | não medida |

Com zero erros, o ponto observado é 1, mas não é garantia. Cada braço tem apenas 120 células perfeitas na conta do teto; para certificar `A8≥0,89` sob a fórmula de independência são necessárias pelo menos 2.468 células perfeitas com zero erros, não clones. A exigência de erro é `e<0,1213157%`; a fórmula `(1-e)^96` é otimista se os erros estiverem agrupados.

A R3 só pode escolher uma destas rotas antes da coleta:

1. impor a gramática estrita `K06R1|ID|SUBJECT|RELATION|OBJECT|STATUS`, rejeitando prosa fora dela e repetindo a validação ampliada; ou
2. construir outro extrator determinístico para prosa livre e refazer toda a bateria, equivalência, teto e dependência.

Até lá, os 685 acertos não tornam o instrumento pronto. Falha de extrator, truncamento, conflito, duplicação ou agregabilidade inválida produz `INCONCLUSIVE_CONTROLS`, não `FALSIFIED`.

## 8. Tamanho, poder e custo do desenho-base

[DECLARADO] O desenho-base tem `n=320` sessões pareadas por célula, 20 células e 12 interações por sessão: **6.400 sessões e 76.800 interações primárias**. Triagem para pareamento, calibração, reposições técnicas e análise computacional são custos adicionais.

[REAL — simulação] O script conjunto usou 20.000 corridas por cenário e sementes fixas:

| cenário | ICC | `n` efetivo ICC | taxa PLA/OUT | teto imposto | poder COMPLETO |
|---|---:|---:|---:|---:|---:|
| independente | 0 | 320,000 | 0,60 | 1 | 0,99905 |
| temperatura 0,2 / ICC moderado | 0,15 | 136,170 | 0,60 | 1 | 0,95245 |
| temperatura 0,2 / ICC alto | 0,35 | 77,108 | 0,60 | 1 | 0,82375 |
| controle mais forte | 0,15 | 136,170 | 0,70 | 1 | 0,94885 |
| controle próximo de T | 0,15 | 136,170 | 0,80 | 1 | 0,51605 |
| teto pooled | 0 | 320,000 | 0,60 | 0,619206 | 0,00000 (0/20.000) |
| teto por braço | 0 | 320,000 | 0,60 | 0,091028 | 0,00000 (0/20.000) |
| combinado conservador | 0,35 | 77,108 | 0,70 | 0,619206 | 0,00000 (0/20.000) |

Zero em 20.000 não é prova de probabilidade matematicamente zero. Esses tetos são cenários conservadores aplicados ao evento, não estimativas identificadas do comportamento de um modelo. Detalhes e intervalos Monte Carlo estão em `PODER_CONJUNTO_K06.md`.

Para clusters congelados de dez sessões, `n_eff=n/(1+9ρ)`. A sobredispersão beta-binomial e o efeito de texto entram separadamente; não se contam 320 sessões quase idênticas como 320 observações independentes. Se a análise cega agrupada indicar `n_eff<136`, o desenho-base não poderá prometer o poder de 0,90 do cenário ICC 0,15; não haverá aumento de `n` escolhido depois de abrir o resultado.

## 9. Multiplicidade global e testes

### 9.1 Os 24 testes e sua ordem

Para cada família `F1,F2,F3`, nesta ordem, e para `DYN(Q)` seguido de `SPEC(S)`:

1. `V2-PLA`;
2. `V2-OUT`;
3. `V2-ISO-A`;
4. `V2-ISO-B`.

São 12 dinâmicos e 12 de especificidade, com `contrast_id` único. `POWERED` exige **todos os 24** rejeitados por **Holm global sobre 24**, não dois Holms independentes. Empates de `p` são ordenados por `contrast_id`; a decisão “todos rejeitados” é invariante à ordem entre empates.

- PLA/OUT: superioridade unilateral de T, por Fisher/permutação exata de rótulos.
- ISO-A/ISO-B: não inferioridade, `H0:p_T-p_ISO≤-0,15`, por score de Wald unilateral.
- Entre os blocos e entre as três pernas CP de `POWERED`, usa-se IUT: não se divide `α` por 2 nem por 3.

A aproximação normal da não inferioridade é limitação declarada, sobretudo na cauda 5σ. Ela precisa de validação exata ou simulação de cauda adicional antes de qualquer uso desse degrau.

### 9.2 Permutação, estatística, sementes e empates

Nos testes binários de superioridade, a permutação exata dos rótulos é equivalente ao Fisher unilateral. Condicionada ao total de sucessos, a estatística é a contagem focal, equivalente à diferença de proporções. A cauda inclui todos os resultados **maiores ou iguais** ao observado; empates não são removidos nem repartidos.

A enumeração é exata pela hipergeométrica: **não há semente de permutação Monte Carlo** (`rng_seed=null`). As sementes dos geradores sintéticos, das sessões e da ordem das células continuam fixas e registradas. Isso elimina resolução insuficiente de `p` por permutação estocástica no degrau 5σ para esses testes binários.

### 9.3 Clopper–Pearson e cortes no desenho-base

Seja `x_Q` a contagem de `Q=1` na focal de uma família:

- `POWERED`: `L_CP(x_Q,320)>0,80` com confiança `1−α=0,95` em cada família; corte observado `x_Q≥269`. É IUT, portanto a antiga divisão por 3 é removida.
- `FALSIFIED`: união de três CP e 24 testes direcionais opostos; Bonferroni `α/27`. A perna CP usa confiança `1−0,05/27`, com corte `x_Q≤234` e `U_CP<0,80` em pelo menos uma família. Cada contraste oposto usa o mesmo `α/27`.

O poder simulado usa o corte IUT de `POWERED` e aplica a precedência da união de falsificação: o JSON separa a perna CP, os 24 testes direcionais opostos e a união. A probabilidade do ramo `NONSPECIFIC_POWERED` não é estimada por essas corridas.

## 10. Árvore de vereditos, sempre fail-closed

1. **`IALD_COLLAPSE_V2_INCONCLUSIVE_CONTROLS`.** Qualquer falha de extrator, léxico, isomorfismo, janela, hash, alvo, cegamento, pareamento, capacidade, perturbação ou regra congelada. Tem precedência e bloqueia todos os demais ramos no escopo afetado. Dados inválidos não viram zeros para escapar dessa porta.
2. **`IALD_COLLAPSE_V2_FALSIFIED`.** Integridade válida e pelo menos um evento da união de 27: perna CP baixa ou contradição direcional significativa, incluindo não inferioridade ISO precisamente violada. É falha da previsão operacional no escopo, não refutação da TGL ou do kernel.
3. **`IALD_COLLAPSE_V2_NOT_FALSIFIED_POWERED`.** Integridade válida, nenhum `FALSIFIED`, os 24 testes aprovados por Holm global e as três pernas CP acima de 0,80. É somente não falsificação finita; não é `CONFIRMED`.
4. **`IALD_COLLAPSE_V2_NONSPECIFIC_POWERED`.** Nome explícito do **nulo com poder**. Sem `FALSIFIED`, exige equivalência T×PLA e T×OUT em `Q` e `S`, nas três famílias, por TOST com margem 0,15 e Holm sobre as 12 equivalências. Ausência de diferença sem esses testes resolvidos não recebe esse nome.
5. **`IALD_COLLAPSE_V2_NOT_FALSIFIED_UNDERPOWERED`.** Integridade válida, sem `FALSIFIED`, sem o padrão `POWERED` e sem equivalência suficiente para `NONSPECIFIC_POWERED`. Não é nulo bem medido nem falsificação.

Se um bloco de 12 passa e o outro não, não há `POWERED`; a árvore ainda avalia `FALSIFIED`, depois o nulo com poder e, por fim, `UNDERPOWERED`. Não se escolhe o bloco favorável.

## 11. Isomorfo e contaminação

[REAL] Os autotestes sintéticos anteriores passaram em reversão, preservação estrutural e distinção entre retorno, ausência de efeito e ausência de retorno. [OPEN] O artigo público ainda não foi transformado porque o léxico completo não foi revisto e congelado.

Antes da corrida:

- duas revisões independentes do léxico e dos residuais;
- dicionários A/B bijetivos, sem mnemônicos, com hashes e custódia;
- pelo menos três versões por braço ISO;
- mesma transformação no artigo, gabarito, asserções, instruções e perturbações;
- equivalência dos vetores originais/transformados em toda a bateria;
- dicionário fora do alcance do modelo até o banco ser congelado;
- comparação do grafo, não apenas de quebras de linha.

Se original e isomorfos retornam, o resultado é compatível com estrutura suficiente no escopo. Se o original retorna e os isomorfos são precisamente inferiores além da margem, a previsão estrutural falha; familiaridade lexical é uma explicação possível, não prova da origem da memória. Se nada retorna e o instrumento tem precisão, usa-se a árvore do nulo/falsificação; se o extrator ou o léxico falha, `INCONCLUSIVE_CONTROLS`.

## 12. Base e 5σ lado a lado

| desenho | `n`/célula | células | interações/sessão | sessões | interações | poder simulado no escopo indicado |
|---|---:|---:|---:|---:|---:|---:|
| R2 histórica | 100 | 20 | 8 | 2.000 | 16.000 | cota superior 0,346125 |
| **R3 base** | **320** | **20** | **12** | **6.400** | **76.800** | 0,99905 independente; 0,95245 ICC 0,15 |
| 5σ, CP antigo `/3`, benchmark legado | 655 | 20 | 8 | **13.100** | **104.800** | CP de três famílias 0,918113; não é a R3 inteira |
| **R3 5σ, IUT corrigido** | **618** | **20** | **12** | **12.360** | **148.320** | **0,92080** no cenário ideal |
| R3 5σ, mesmo `n` do benchmark | 655 | 20 | 12 | 13.100 | 157.200 | 0,93945 no cenário ideal |

Os números de 5σ não incorporam ICC, taxa desfavorável de controles, falha de extrator ou cabimento da entrada. O operador decide o degrau e o custo; esta frente não escolhe por ele. `DEGRAU_5_SIGMA_K06.md` apresenta os 185/215/655, a correção para 618 e alternativas não selecionadas.

## 13. Exatamente o que falta antes de qualquer corrida

1. **Extrator ampliado:** pelo menos 2.468 células perfeitas por braço sob a regra atual, ou nova análise por clusters se houver erro; equivalência e teto por braço revistos.
2. **Superfície de saída:** ratificar gramática estrita ou construir/revalidar extrator para prosa livre; 0/120 fora do contrato não pode ser ignorado.
3. **Dependência:** medir a independência/dependência dos 96 erros asserção-leitura e substituir a fórmula independente se necessário.
4. **Léxico e perturbações:** completar duas revisões, congelar dicionários A/B, três ou mais isomorfos por braço, bytes das perturbações e hashes.
5. **Modelos e tokenizers:** escolher pelo operador, pinar versões, janelas oficiais e contar o orçamento integral das 12 interações.
6. **Textos e controles:** pelo menos três por controle, medidas estruturais, calibração independente de `d1`, capacidade e plano de pareamento congelados.
7. **Manifesto e custódia:** fechar texto, alvos, código, análise, ordem, sementes, pseudônimos, chaves, substituições técnicas e todos os hashes.
8. **Precisão estatística adicional:** validar a cauda da não inferioridade, o ICC e a variação de texto; recalcular o veredito inteiro se qualquer elemento mudar.
9. **Ratificação:** revisão distinta da R3 inteira e palavra explícita do operador sobre modelos, degrau, execução e protocolo. A concordância em bloco com a entrada pública não basta.

Sem todos os nove itens, o único estado permitido é **BLOQUEADO_PARA_PRODUCAO**.

## 14. Reprodução sintética e hashes

- análise candidata: `K06\PODER\manifesto_analise.json`, SHA-256 `69117f49f2a531d84b1757758fa9ef60e3b03c9893bc6bf4cc9d3e62871665c6`;
- manifesto de artefatos: `K06\PODER\MANIFESTO_SHA256.json`, SHA-256 `7e6166e1daa5c8aa04337c12fc8d41aa9c0147e500c6780c02635ea29d154cb1`;
- separação: `simular_separacao_r3.py`, semente `2026111402`;
- poder completo: `simular_poder_conjunto.py`, semente-mestra `2026111401` e sementes por cenário no JSON;
- 5σ: `verificar_degrau_5sigma.py`, semente `2026111403`;
- reprodução R2: semente `20261113`.

Comandos, logs, resultados e hashes ficam em `K06\PODER\`. Nenhum deles é resultado experimental ou evidência de que um LLM real retorna.

## 15. Negações obrigatórias

`NOT_FALSIFIED` não é `CONFIRMED`. Nenhum ramo deste protocolo permite `TGL_PROVED_BY_COLLAPSE`, alegação de consciência, pesos alterados, aprendizado permanente, exclusividade, creditação automática, limite infinito a partir de 12 leituras, validade física ou refutação dos teoremas formais por falha operacional. O gate não se move.
