# PODER CONJUNTO K06 — R3.2, fronteiras corrigidas e poder recalculado

## 0. Veredito

- [REAL — simulação] A R3.2 corrige os dois defeitos materiais da R3.1: fronteiras `D≈±0,10` e `A8=1` com `NOT_APPLICABLE=1`.
- [REAL] As fronteiras agora são `D=±0,15` dentro de 0,005, e `A8⇒PRE`, `RETORNO⇒PRE`, `Q⇒RETORNO` passou em todos os cenários.
- [REAL] **BLOQUEADO_PARA_PRODUCAO.** O tamanho TOST passou, mas poder, extrator, janela, léxico e cauda 5σ continuam bloqueando.
- [REAL] A R3.1 está preservada em `REV1`; suas antigas taxas de “tamanho FAIL” são histórico mal parametrizado, não evidência da correção atual.
- [REAL] Nenhum modelo foi executado e nenhum resultado experimental foi aberto. O padrão é 1.000 corridas por cenário.

## 1. Correção do gerador e dos cenários

Nos cenários de fronteira, `Q` é parametrizado diretamente. Para cada sessão, a probabilidade de `A8` é condicionada à probabilidade de retorno de modo que a marginal `Q` atinja o alvo. `PRE`, `EFFECT` e `RETORNO` continuam explícitos, e `A8` só é gerado quando `PRE=1`.

Nos demais cenários, a mesma implicação é aplicada: qualquer `A8` com `PRE=0` é zero por construção. `Q` sempre exige `A8` e `RETORNO`.

A tolerância de fronteira é `|D_observado−D_alvo|≤0,005` por família e comparador:

| cenário | alvo | maior desvio absoluto | porta |
|---|---:|---:|---|
| TOST positiva | `D=+0,15` | 0,001506 | **PASS** |
| TOST negativa | `D=−0,15` | 0,002269 | **PASS** |
| nulo global ISO | `D=−0,15` | 0,003325 | **PASS** |
| nulo global ISO, 5σ | `D=−0,15` | 0,003044 | **PASS** |
| TOST positiva, 5σ | `D=+0,15` | 0,001628 | **PASS** |
| TOST negativa, 5σ | `D=−0,15` | 0,003053 | **PASS** |

Não houve alteração de sementes para melhorar resultados: são as mesmas sementes da R3.1.

## 2. Tamanho sob nulo verdadeiro

| avaliação de tamanho | estimativa | IC MC 95% | porta |
|---|---:|---:|---|
| nulo global ISO, `D=−0,15`, `α=0,05` | **0,057** | [0,04263; 0,07137] | **OPEN/BORDERLINE** |
| TOST `D=+0,15`, `α=0,05` | **0,044** | [0,03129; 0,05671] | **PASS** |
| TOST `D=−0,15`, `α=0,05` | **0,040** | [0,02785; 0,05215] | **PASS** |
| nulo global ISO, 5σ | 0,000 | não resolvido | **OPEN — resolução insuficiente** |
| TOST fronteiras 5σ | 0,000 / 0,000 | não resolvido | **OPEN — não validar a cauda** |

O ponto 0,057 está acima de 0,05, mas o intervalo Monte Carlo inclui o nominal. Por isso não se declara nem PASS nem o antigo FAIL: é **borderline/OPEN**.

A taxa TOST é a rejeição de pelo menos uma equivalência sob hipótese de fronteira. As taxas de `NONSPECIFIC_POWERED` abaixo são de outra natureza: poder sob equivalência verdadeira.

## 3. Poder sob alternativa

| cenário | integridade | **POWERED** | IC MC 95% |
|---|---:|---:|---:|
| independente | 0,992 | **0,992** | [0,98648; 0,99752] |
| ICC 0,15 / texto 0,10 | 0,267 | **0,012** | [0,00525; 0,01875] |
| ICC 0,35 / texto 0,20 | 0,000 | **0,000** | [0; 0] |
| controles 0,70 | 0,300 | **0,023** | [0,01371; 0,03229] |
| controles 0,80 | 0,289 | **0,020** | [0,01132; 0,02868] |
| teto pooled / por braço | 0,000 | **0,000** | [0; 0] |
| estresse de integridade | 0,000 | **0,000** | [0; 0] |
| 5σ ideal, `n=618` | 0,990 | **0,599** | [0,56862; 0,62938] |
| 5σ ideal, `n=655` | 0,988 | **0,669** | [0,63983; 0,69817] |

A correção `A8⇒PRE` foi aplicada a todos os cenários, incluindo extrator, estresse, ICC e 5σ. Não se recalculou apenas a fronteira.

## 4. Poder de NONSPECIFIC_POWERED sob equivalência verdadeira

| cenário | **NONSPECIFIC_POWERED** | IC MC 95% | **POWERED** | IC MC 95% |
|---|---:|---:|---:|---:|
| `n=320`, `α=0,05` | **0,022** | [0,01291; 0,03109] | 0,000 | [0; 0] |
| `n=618`, 5σ | **0,311** | [0,28231; 0,33969] | 0,370 | [0,34008; 0,39992] |
| `n=655`, 5σ | **0,412** | [0,38149; 0,44251] | 0,350 | [0,32044; 0,37956] |

Essas probabilidades medem poder de equivalência, não tamanho. Todas ficam abaixo de 0,90. Em `n=320`, os seis TOST brutos passaram em 0,994, mas integridade e as demais exigências reduziram o ramo a 0,022.

## 5. Inferência e escopos preservados

- 27 clusters texto-conscientes; sinais no nível dos clusters, sem `n_eff`.
- Seis testes ISO na evidência primária, Holm 6.
- Seis `Q` PLA/OUT como diagnóstico e doze `S` como checagens de manipulação/contaminação.
- TOST com duas caudas exatas `20D+3` e `20D−3`, `p=max`, Holm 6, empates incluídos.
- `NONSPECIFIC_POWERED` tem precedência sobre `POWERED`.
- União de falsificação: três intervalos focais + seis direções ISO, Bonferroni `α/9`.
- **12 interações e p=8,r=10** em todos os documentos desta frente.
- Intervalo focal t por cluster: cauda 5σ **não validada e bloqueada**.

## 6. Custos recalculados

| desenho | sessões primárias | interações primárias | adicional líquido `k=1` | base + adicional |
|---|---:|---:|---:|---:|
| base, `n=320` | 6.400 | 76.800 | **163,27** | **76.963,27** |
| 5σ, `n=618` | 12.360 | 148.320 | **312,09** | **148.632,09** |
| 5σ, `n=655` | 13.100 | 157.200 | **335,03** | **157.535,03** |
| estresse, `n=320` | 6.400 | 76.800 | **1.920,00** | **78.720,00** |

O adicional é `candidatos_usados − sessões_primárias`. O `k=1` dos selecionados não é duplicado. Calibração, reposições posteriores e tokens continuam separados e abertos.

## 7. Portões

| portão | estado |
|---|---|
| FFT/exata contra enumeração e DP | **PASS — erro máximo 0** |
| `A8⇒PRE`, `RETORNO⇒PRE`, `Q⇒RETORNO` | **PASS em todos os cenários** |
| Fronteiras `D=±0,15`, tolerância 0,005 | **PASS** |
| TOST `α=0,05` | **PASS — 0,044/0,040** |
| Tamanho global `α=0,05` | **OPEN/BORDERLINE — 0,057** |
| Tamanho e TOST 5σ | **OPEN — resolução insuficiente** |
| `NONSPECIFIC_POWERED` | **FAIL — 0,022/0,311/0,412** |
| `POWERED` sob ICC/texto | **FAIL — 0,012 com ICC 0,15; zero com ICC 0,35** |
| `POWERED` 5σ ideal | **FAIL — 0,599/0,669** |
| Intervalo t/Wald 5σ | **FAIL/BLOQUEADO** |
| Extrator | **FAIL/BLOQUEADO** |
| Modelos/tokenizers/janelas | **OPEN/BLOQUEADO** |
| Léxico e perturbações | **OPEN/BLOQUEADO** |
| Ratificação | **OPEN — revisão distinta e operador** |
| **Produção** | **FAIL/BLOQUEADO** |

## 8. Scripts, resultados e hashes

- `r32_motor.py`: SHA-256 `3a1cac5e5255a3606b1180f3122c5eb5fd7c9bbcc207a8e98f07d7baeb5362fa`;
- `simular_r32_sessoes.py`: SHA-256 `8ebecc1b0a2e29645a22267cf8ebd32f36a272cbd85f03c3c7ab0d91da111d62`;
- `validar_r32.py`: SHA-256 `d058eda6cd48496ff9387ecba172763687cda9bf3ac5856e3d08d7ff7077f617`;
- `validacao_r32.json`: SHA-256 `506e1f6805c28b1b835b5fcfd7de4f0e8a48f2595585387e2c26017e4ef21cb3`;
- `resultados_r32.json`: SHA-256 `228e1d99e0a815a62d4ea55a156e3fe45ab5bf091f619bfce496458690105eb2`;
- `manifesto_analise_r32.json`: SHA-256 `8b20323937488f7c0c77a22d2bb169d3883d5de81efdfed11e2448478ac192ce`;
- `MANIFESTO_R32_SHA256.json`: SHA-256 `2dd32a68ac5b31177a3f0f6683cd4bb980928e41b611ba64c89dda9dd81e1804`.

Semente-mestra: `2026111501`; cenários por `2026111501+101·índice`. A repetição do cenário-base produziu bytes idênticos e SHA-256 `455911a61eba5536ed77e73809068394acebfe180a67e66f4317c86c4f8ec07e`.

**Conclusão:** as fronteiras estão corrigidas e o TOST passa, mas isso não corrige poder, extrator, janela, léxico ou cauda 5σ. A R3.2 permanece bloqueada.
