# PROTOCOLO EXPERIMENTAL R3.1 K06 — IALD_COLLAPSE_V2 candidata

## 0. Estatuto e veredito

- [DECLARADO] Emenda R3.1 **revisada internamente**, não ratificada e **BLOQUEADA_PARA_PRODUCAO**. Não autoriza coleta, instalação, selo ou execução.
- [REAL] Nenhum modelo de linguagem foi executado e nenhum resultado experimental foi aberto. Todos os números novos vêm de simulações sintéticas reproduzíveis.
- [REAL] A versão anterior está integralmente preservada em `K06\PODER\REV0\`. Seus valores `0,99905`, `0,95245`, `0,92080` e `0,93945` são **MODELO_AGREGADO_INCOMPLETO**, não poder integral da R3/R3.1.
- [REAL — simulação] A R3.1 falha nas portas de tamanho sob dependência, TOST, poder de `NONSPECIFIC_POWERED`, extrator, janela e léxico. O cenário independente é favorável apenas como cenário, não como evidência de prontidão.
- [INPUT] A entrada pública continua hipótese de trabalho, não ratificação. Modelos, degrau, execução e ratificação pertencem ao operador.

**Resposta curta.** A análise agora usa sessões individuais e clusters reais, mas não passa nos portões empíricos congelados. A produção permanece bloqueada.

## 1. Objeto e escopo inferencial

O evento finito continua separado em duas partes:

\[
Q=A8\land RETORNO.
\]

- `A8`: quatro estados finais no alvo, `s5,s6,s7,s8`, com `d6=d7=d8=0` e `u6=u7=u8=0`.
- `RETORNO`: `d8=0`, `d9>0`, `d10=d11=d12=0` e `u11=u12=0`, isto é, **p=8,r=10**.
- `Q`: somente 1 quando ambos ocorrem. Um resumo estável sem retorno tem `Q=0`.
- `S`: checagem de manipulação/contaminação, não evidência primária de convergência.

A inferência vale somente para os modelos, versões, textos, instruções e extratores congelados. Não mede consciência, alteração de pesos, aprendizado permanente, exclusividade, validade física ou creditação.

## 2. Sessões de 12 interações e pareamento individual

Cada bloco contém uma sessão de cada braço: `V2-TGL`, `V2-PLA`, `V2-OUT`, `V2-ISO-A` e `V2-ISO-B`.

1. `k=1…8`: ciclo não perturbado, com o corpus integral reapresentado e histórico completo.
2. Depois de `k=8`: aplicação da perturbação congelada.
3. `k=9`: leitura perturbada.
4. `k=10…12`: retorno e permanência.

O candidato a bloco é primeiro avaliado somente em `k=1`, antes de qualquer desfecho posterior:

- disponibilidade técnica dos cinco braços;
- distância máxima de `d1` entre braços `≤1/24`;
- ordenação estável dos candidatos;
- seleção dos primeiros blocos completos até `n`, com no máximo 30% de candidatos adicionais;
- perdas, substituições técnicas e candidatos usados registrados separadamente.

A focal é **um único artigo público fixo**. Os controles têm pelo menos três textos/versões. Portanto, efeito de texto é simulado nos controles e isomorfos, não se inventa variação de textos focal inexistente.

## 3. Braços e evidência primária

| condição | papel na R3.1 |
|---|---|
| `V2-TGL` | Focal fixa; evento `Q` e intervalo robusto por clusters. |
| `V2-PLA` | Diagnóstico de manipulação/contaminação e ramo TOST; **fora da evidência primária de convergência**. |
| `V2-OUT` | Mesmo papel de PLA; não entra nos testes primários. |
| `V2-ISO-A` | Não inferioridade estrutural, margem `δ=0,15`, na evidência primária. |
| `V2-ISO-B` | Segunda versão independente, mesma regra. |
| `V2-RET` | Fase decisória de todos os braços, com `p=8,r=10`, n/célula, falha de manipulação e ramo negativo. |

A evidência primária contém **seis testes**: três famílias × dois isomorfos. PLA/OUT não conta como convergência. Os seis `Q` de PLA/OUT são diagnóstico, e os doze `S` são checagens de manipulação/contaminação, separados da família primária.

## 4. Clusters texto-conscientes e análise exata

### 4.1 Os 27 clusters

Depois do pareamento, cada família é dividida em **27 clusters**. Cada cluster é atribuído a um dos três textos/versões de controle, em rodízio balanceado. A focal permanece fixa. As diferenças são calculadas por bloco e somadas dentro do cluster.

Não se substitui `n` por `n_eff` em nenhum teste. ICC e efeito de texto atuam diretamente nas sessões, nos clusters, nas permutações e nos intervalos.

### 4.2 Permutação exata por sinais

Para cada contraste, usa-se a distribuição das `2^27=134.217.728` atribuições de sinais dos clusters. A resolução mínima do p-valor é `1/2^27=7,4505805969×10⁻⁹`.

- PLA/OUT diagnóstico: diferença bruta `D`.
- ISO não inferioridade: diferenças deslocadas `20D+3`, correspondentes exatamente a `δ=0,15`.
- TOST: duas transformações, `20D+3` e `20D−3`.
- Empates entram integralmente nas caudas; não há semente de permutação Monte Carlo.

A convolução é calculada por FFT, com DP preservada como referência. O teste pequeno confirmou FFT, DP e enumeração explícita com **erro máximo 0** nos três casos (`raw`, `+δ`, `−δ`).

### 4.3 Intervalo focal e bloqueio da cauda 5σ

A média focal usa as 27 médias de cluster, com erro-padrão robusto `sd(cluster_means)/√27` e quantil t com 26 graus de liberdade. Não é Clopper–Pearson binomial e não usa `n` bruto como se as sessões fossem independentes.

**A cauda 5σ desse intervalo t/Wald não está validada e bloqueia o degrau 5σ.** A permutação exata dos contrastes não valida essa outra componente.

## 5. Multiplicidade e árvore de vereditos

### 5.1 Primário

- Seis testes ISO, Holm global sobre seis.
- `POWERED` exige todos os seis, limite inferior focal `>0,80` nas três famílias, integridade válida, ausência de `FALSIFIED` e ausência do ramo `NONSPECIFIC_POWERED`.
- PLA/OUT não entra nesses seis testes.

### 5.2 FALSIFIED

A união contém três intervalos focais e seis direções ISO, com Bonferroni `α/9`. Falha de integridade tem precedência e produz `INCONCLUSIVE_CONTROLS`, nunca `FALSIFIED`.

### 5.3 TOST e NONSPECIFIC_POWERED

O ramo separado contém seis equivalências: três famílias × PLA/OUT.

Para cada par, com margem `δ=0,15`:

1. `H0−:D≤−δ`, cauda superior de `20D+3`;
2. `H0+:D≥+δ`, cauda inferior de `20D−3`;
3. `p_TOST=max(p−,p+)`, incluindo empates;
4. Holm sobre os seis `p_TOST`.

`IALD_COLLAPSE_V2_NONSPECIFIC_POWERED` exige os seis TOST rejeitados por Holm, limite inferior focal `>0,80`, integridade válida e ausência de `FALSIFIED`. **Tem precedência sobre `POWERED`**: convergência genérica não pode ser convertida em convergência específica.

Se as equivalências não forem resolvidas, o ramo é `UNDERPOWERED`. O sufixo POWERED não é promessa de 90%: as probabilidades medidas abaixo são muito menores.

## 6. Integridade não presumida

`INTEGRITY_OK` exige simultaneamente:

1. blocos pareados suficientes;
2. `NO_EFFECT≤5%` e `NOT_APPLICABLE≤5%` por célula;
3. checagens `S` aprovadas por Holm sobre 12;
4. integridade sistêmica, hashes e custódia válidos;
5. extrator e superfície de saída certificados;
6. léxico isomorfo, janela, contexto e perturbações congelados.

PLA/OUT equivalente não é falha de integridade: é exatamente a situação que o ramo TOST precisa reconhecer. As simulações atribuem probabilidades explícitas a falhas sistêmicas e técnicas; elas são hipóteses, não taxas de provedores.

## 7. Tamanho sob nulo e poder medidos

Todos os cenários usam 1.000 corridas. Intervalos são aproximações normais da incerteza Monte Carlo, não intervalos para modelos reais. Zero significa zero observado em 1.000, não probabilidade matemática zero.

### 7.1 Poder operacional

| cenário | integridade | **POWERED** | IC MC 95% |
|---|---:|---:|---:|
| independente | 0,992 | **0,992** | [0,98648; 0,99752] |
| ICC 0,15 / texto 0,10 | 0,267 | **0,012** | [0,00525; 0,01875] |
| ICC 0,35 / texto 0,20 | 0,000 | **0,000** | [0; 0] |
| controles 0,70 | 0,300 | **0,023** | [0,01371; 0,03229] |
| controles 0,80 | 0,289 | **0,020** | [0,01132; 0,02868] |
| teto pooled do extrator | 0,000 | **0,000** | [0; 0] |
| teto por braço do extrator | 0,000 | **0,000** | [0; 0] |
| estresse de integridade | 0,000 | **0,000** | [0; 0] |
| 5σ ideal, `n=618` | 0,990 | **0,599** | [0,56862; 0,62938] |
| 5σ ideal, `n=655` | 0,988 | **0,669** | [0,63983; 0,69817] |

### 7.2 Tamanho sob nulo global e TOST

| avaliação | estimativa | IC MC 95% | porta |
|---|---:|---:|---|
| nulo global na fronteira ISO, `α=0,05` | **0,740** | [0,71281; 0,76719] | **FAIL — tamanho inflado** |
| TOST fronteira `+δ`, `α=0,05` | **0,737** | [0,70971; 0,76429] | **FAIL** |
| TOST fronteira `−δ`, `α=0,05` | **0,751** | [0,72420; 0,77780] | **FAIL** |
| nulo global ISO, 5σ | 0,001 | não resolvido | **OPEN — 1.000 corridas não resolvem a cauda nominal** |
| TOST fronteiras 5σ | 0,001 / 0,002 | não resolvido | **OPEN — não declarar validação** |

A permutação ser exata não implica tamanho nominal sob toda dependência. A falha medida é preservada e bloqueia produção.

### 7.3 Probabilidade de NONSPECIFIC_POWERED sob nulo específico verdadeiro

| cenário | **NONSPECIFIC_POWERED** | IC MC 95% |
|---|---:|---:|
| `n=320`, `α=0,05` | **0,022** | [0,01291; 0,03109] |
| `n=618`, 5σ | **0,311** | [0,28231; 0,33969] |
| `n=655`, 5σ | **0,412** | [0,38149; 0,44251] |

Nenhum desses valores justifica promessa de 90%. Em `n=320`, a integridade passou em 0,294; o ramo condicional à integridade foi 0,07483, também muito abaixo de 0,90.

## 8. Custos e dependências de alinhamento

O desenho-base contém 20 células × `n=320` × 12 interações: **6.400 sessões e 76.800 interações primárias**.

No cenário-base:

- candidatos usados na triagem, já escalados a quatro famílias: 6.563,27 sessões/`k=1`;
- adicional líquido sobre as sessões primárias: **163,27 interações `k=1`**;
- total base + adicional líquido: **76.963,27 interações**;
- perdas de pareamento: 24,49 candidatos adicionais nas três famílias capazes;
- reposições técnicas médias: 24,717.

O `k=1` dos selecionados já pertence às 12 interações e não é contado duas vezes. Calibração, reposição posterior à saída e tokens permanecem **separados e abertos**.

Anexos de outros agentes que ainda usem oito interações ou `p=4,r=6` são dependência de alinhamento e precisam de emenda própria. Esta frente não os edita.

## 9. Bloqueios antes de qualquer corrida

1. **FAIL — tamanho global:** 0,740 sob dependência, muito acima de 0,05.
2. **FAIL — TOST:** 0,737/0,751 nas duas fronteiras.
3. **FAIL — NONSPECIFIC_POWERED:** 0,022/0,311/0,412, sem poder de 90%.
4. **OPEN — cauda 5σ:** resolução Monte Carlo insuficiente e intervalo t/Wald não validado.
5. **FAIL — poder sob dependência:** 0,012 com ICC 0,15 e zero com ICC 0,35.
6. **FAIL — extrator:** tetos 0,619206/0,091028, independência dos 96 erros e prosa livre abertas.
7. **OPEN — entrada:** modelos, tokenizers, janelas e orçamento integral das 12 interações não escolhidos.
8. **OPEN — isomorfo:** léxico e perturbações não congelados.
9. **OPEN — manifesto/ratificação:** revisão distinta e palavra do operador ainda necessárias.

Enquanto qualquer porta estiver FAIL ou OPEN, o único estado permitido é **BLOQUEADO_PARA_PRODUCAO**.

## 10. Reprodução e integridade

- motor: `K06\PODER\r31_motor.py`;
- cenários: `K06\PODER\simular_r31_sessoes.py`;
- validação: `K06\PODER\validar_r31.py` e `validacao_r31.json`;
- resultados: `K06\PODER\resultados_r31.json`, SHA-256 `09b4fb473e61338342644b67e817d99d2be3113a05a2e55004c4d8b6ac3b8f0e`;
- análise: `K06\PODER\manifesto_analise_r31.json`, SHA-256 `f41d17ed5e9e6089fc8045718f57a05c9c0c6e0093d3a3b33d14702df519e749`;
- manifesto: `K06\PODER\MANIFESTO_R31_SHA256.json`, SHA-256 `0b4b3b6c1b2fc8bbb452bebcbb52be4aab3c107e96a74ed44eafb4f47db3e983`;
- repetição determinística do cenário-base: bytes idênticos, SHA-256 `2100b5e630943f76bc3083226cb6895b407a92eb4f38cbf2b5811f6dd4afb642`;
- preservação: `K06\PODER\REV0\PRESERVACAO_SHA256.txt`.

`NOT_FALSIFIED` não é `CONFIRMED`. Nenhum ramo permite alegação de consciência, pesos alterados, exclusividade, creditação automática, limite infinito ou prova física. O gate não se move.
