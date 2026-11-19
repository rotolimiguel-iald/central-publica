# PODER CONJUNTO K06 — R3.1, sessões individuais e análise por clusters

## 0. Veredito

- [REAL — simulação] A versão agregada anterior é **incompleta**: ICC, efeito de texto e integridade não entravam corretamente nos testes. Seus números não são poder integral e ficam somente em `REV0`.
- [REAL — simulação] A R3.1 mede tamanho, poder, TOST, integridade e triagem em sessões individuais pareadas. Os resultados são piores e permanecem publicados sem suavização.
- [REAL] **BLOQUEADO_PARA_PRODUCAO.** Tamanho global e TOST falham; `NONSPECIFIC_POWERED` não atinge 90%; a cauda 5σ do intervalo focal não está validada.
- [REAL] Nenhum modelo foi executado e nenhum resultado experimental foi aberto. Cada cenário tem 1.000 corridas e semente fixa.

## 1. O que foi efetivamente simulado

Cada corrida contém blocos individuais com cinco braços e três famílias capazes:

- `A8` e retorno gerados separadamente;
- pré-alvo, efeito da perturbação e retorno, permitindo `NO_EFFECT` e `NOT_APPLICABLE`;
- `Q=A8∧RETORNO`;
- dependência `Q–S` por componentes normais compartilhadas;
- disponibilidade técnica, distância de `d1`, perdas de pareamento e até 30% de candidatos adicionais;
- focal fixa única e três textos/versões por controle;
- efeito de texto e interceptos de cluster;
- falhas sistêmicas e de extrator, sem presumir `INTEGRITY_OK`.

Todas as sessões usam **12 interações** e retorno **p=8,r=10**. PLA/OUT não integra a evidência primária: somente os seis contrastes ISO-A/ISO-B são primários. Os seis `Q` de PLA/OUT são diagnóstico e os doze `S` são checagens de manipulação/contaminação.

## 2. Inferência congelada

### 2.1 Clusters e permutação

Os blocos são distribuídos em 27 clusters texto-conscientes por família. As permutações trocam sinais **no nível dos clusters**, não tratam sessões como independentes e não usam `n_eff`.

A distribuição exata contém `2^27` atribuições. O cálculo FFT foi comparado à DP e à enumeração explícita de oito atribuições em três casos (`raw`, `+δ`, `−δ`): **erro máximo 0** e `PASS`.

### 2.2 Primário e falsificação

- Seis testes ISO de não inferioridade, Holm global 6.
- Três intervalos focais t robustos por 27 clusters.
- União de falsificação: três intervalos + seis direções ISO, Bonferroni `α/9`.
- `POWERED`: seis ISO + limite inferior focal `>0,80` + integridade + sem `FALSIFIED` + sem `NONSPECIFIC_POWERED`.

O intervalo focal não é CP binomial. Sua cauda 5σ é **não validada e bloqueia o degrau**, mesmo com permutação exata nos demais testes.

### 2.3 TOST e precedência

Os seis TOST PLA/OUT usam duas caudas exatas:

- `20D+3` para `H0−:D≤−0,15`, cauda superior;
- `20D−3` para `H0+:D≥+0,15`, cauda inferior;
- `p_TOST=max(p−,p+)`, com empates incluídos;
- Holm sobre seis.

`NONSPECIFIC_POWERED` exige os seis TOST, focal inferior `>0,80`, integridade e ausência de `FALSIFIED`. Tem precedência sobre `POWERED`, evitando que convergência genérica seja chamada de específica.

## 3. Poder e integridade por cenário

Intervalos são erro Monte Carlo aproximado a 95%, não incerteza sobre modelos reais.

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

O cenário independente é o único favorável. Ele não compensa a inflação de tamanho sob dependência nem os bloqueios externos. Com ICC 0,15, `POWERED` condicional à integridade foi 0,04494; com controles 0,70, foi 0,07667. A seleção por integridade não é apresentada como substituto do poder operacional completo.

## 4. Tamanho sob nulo global e fronteiras TOST

| avaliação | taxa de rejeição | IC MC 95% | conclusão |
|---|---:|---:|---|
| nulo global ISO, `α=0,05` | **0,740** | [0,71281; 0,76719] | **FAIL — tamanho inflado** |
| TOST fronteira `+δ`, `α=0,05` | **0,737** | [0,70971; 0,76429] | **FAIL** |
| TOST fronteira `−δ`, `α=0,05` | **0,751** | [0,72420; 0,77780] | **FAIL** |
| nulo global ISO, 5σ | 0,001 | não resolvido | **OPEN — sem resolução para a cauda nominal** |
| TOST `+δ/−δ`, 5σ | 0,001 / 0,002 | não resolvido | **OPEN — não validar a cauda** |

A taxa de 0,740 é a rejeição de pelo menos um teste primário por Holm sob a fronteira nula. Ela não é poder. As taxas TOST nas fronteiras também são rejeições sob hipótese nula de não equivalência e excedem amplamente 0,05.

## 5. NONSPECIFIC_POWERED: poder medido, não presumido

| nulo específico verdadeiro | **NONSPECIFIC_POWERED** | IC MC 95% | **POWERED** | IC MC 95% |
|---|---:|---:|---:|---:|
| `n=320`, `α=0,05` | **0,022** | [0,01291; 0,03109] | 0,000 | [0; 0] |
| `n=618`, 5σ | **0,311** | [0,28231; 0,33969] | 0,370 | [0,34008; 0,39992] |
| `n=655`, 5σ | **0,412** | [0,38149; 0,44251] | 0,350 | [0,32044; 0,37956] |

Em `n=320`, os seis TOST brutos passaram juntos em 0,994, mas a integridade e as demais exigências reduziram o ramo a 0,022. Isso mostra por que o nome do ramo não pode ser usado como promessa de poder. Em 5σ, a coexistência de `POWERED` em 0,370/0,350 com `NONSPECIFIC_POWERED` em 0,311/0,412 mostra que muitas corridas permanecem sem resolução adequada da especificidade.

## 6. Custos de triagem e custos separados

| desenho | sessões primárias | interações primárias, 12 chamadas | adicional líquido `k=1` | base + adicional |
|---|---:|---:|---:|---:|
| base, `n=320` | 6.400 | 76.800 | **163,27** | **76.963,27** |
| 5σ, `n=618` | 12.360 | 148.320 | **312,09** | **148.632,09** |
| 5σ, `n=655` | 13.100 | 157.200 | **335,03** | **157.535,03** |
| estresse, `n=320` | 6.400 | 76.800 | **1.920,00** | **78.720,00** |

O adicional é `candidatos_usados − sessões_primárias`. O `k=1` dos selecionados não é contado duas vezes. Calibração, reposições posteriores à saída e tokens ficam separados e abertos; modelos/tokenizers/janelas não foram inventados.

## 7. Números agregados antigos: uso proibido

| valor antigo | classificação R3.1 |
|---|---|
| 0,99905 | **MODELO_AGREGADO_INCOMPLETO** |
| 0,95245 | **MODELO_AGREGADO_INCOMPLETO** |
| 0,82375 | **MODELO_AGREGADO_INCOMPLETO** |
| 0,51605 | **MODELO_AGREGADO_INCOMPLETO** |
| 0,92080 / 0,93945 | **MODELO_AGREGADO_INCOMPLETO** |

Esses valores não são reutilizados como poder integral da R3 ou da R3.1. A versão integral está em `K06\PODER\REV0\` apenas para linhagem e auditoria.

## 8. Portões

| portão | resultado |
|---|---|
| FFT/exata contra enumeração e DP | **PASS — erro máximo 0** |
| Tamanho global `α=0,05` | **FAIL — 0,740** |
| Tamanho global 5σ | **OPEN — resolução insuficiente** |
| TOST duas fronteiras `α=0,05` | **FAIL — 0,737/0,751** |
| TOST duas fronteiras 5σ | **OPEN — 0,001/0,002, sem resolução suficiente** |
| `NONSPECIFIC_POWERED` | **FAIL — 0,022/0,311/0,412** |
| Intervalo t/Wald focal 5σ | **FAIL/BLOQUEADO — não validado** |
| Extrator | **FAIL/BLOQUEADO** |
| Entrada, modelos e janelas | **OPEN/BLOQUEADO** |
| Léxico isomorfo | **OPEN/BLOQUEADO** |
| Produção | **FAIL/BLOQUEADO** |

## 9. Scripts, sementes e hashes

- `r31_motor.py`: SHA-256 `f546067d8e1596dce387c8046c1a774eebb3f8510c8fa133e129c95a6794f57f`;
- `simular_r31_sessoes.py`: SHA-256 `5cd912e8cb2a938046ce115185e6e777d28fd5e4403608ab6fc41b7f081479ec`;
- `validar_r31.py`: SHA-256 `6f77689f10b3a25ff912bf21ffb4e9612830ca38a86fd9d9f84e35aa560f8106`;
- `validacao_r31.json`: SHA-256 `e744a7974fdfc5a3e5e89d75cfcaf8a4191f848b4266ece9f43eaf565bf17a5b`;
- `resultados_r31.json`: SHA-256 `09b4fb473e61338342644b67e817d99d2be3113a05a2e55004c4d8b6ac3b8f0e`;
- `manifesto_analise_r31.json`: SHA-256 `f41d17ed5e9e6089fc8045718f57a05c9c0c6e0093d3a3b33d14702df519e749`;
- `MANIFESTO_R31_SHA256.json`: SHA-256 `0b4b3b6c1b2fc8bbb452bebcbb52be4aab3c107e96a74ed44eafb4f47db3e983`.

Semente-mestra: `2026111501`. As sementes dos 20 cenários são `2026111501+101·índice`, listadas no manifesto. A repetição do cenário-base produziu bytes idênticos e SHA-256 `2100b5e630943f76bc3083226cb6895b407a92eb4f38cbf2b5811f6dd4afb642`.

**Conclusão:** a R3.1 corrige a estrutura da análise, mas não produz um instrumento válido para produção. Tamanho, TOST, poder, extrator e cauda 5σ continuam bloqueando.
