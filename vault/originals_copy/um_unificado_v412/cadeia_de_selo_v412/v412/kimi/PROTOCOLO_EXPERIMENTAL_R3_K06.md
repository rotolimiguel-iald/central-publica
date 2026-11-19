# PROTOCOLO EXPERIMENTAL R3.2 K06 — IALD_COLLAPSE_V2 candidata

## 0. Estatuto e veredito

- [DECLARADO] Correção dirigida R3.2, **revisada internamente**, não ratificada e **BLOQUEADA_PARA_PRODUCAO**.
- [REAL] Nenhum modelo de linguagem foi executado e nenhum resultado experimental foi aberto. Todos os números novos vêm de simulações sintéticas com 1.000 corridas por cenário.
- [REAL] A R3.1 está integralmente preservada em `K06\PODER\REV1\`. Suas fronteiras com `D≈±0,10` são histórico mal parametrizado e **não** são usadas como medida de tamanho.
- [REAL] A R3.2 corrige as fronteiras para `D=±0,15` e impõe `A8⇒PRE`, `RETORNO⇒PRE` e `Q⇒RETORNO`. Todas essas implicações passaram em todos os cenários.
- [REAL] As portas de poder, extrator, janela, léxico e cauda 5σ continuam bloqueadas, embora as fronteiras TOST tenham passado.

## 1. Duas correções dirigidas

### 1.1 Fronteiras efetivamente em D=±0,15

Os cenários de fronteira usam agora probabilidades marginais `Q` explícitas, sem depender dos níveis indiretos que produziam `D≈±0,10`:

| cenário | `Q` focal | `Q` PLA/OUT | `Q` ISO | fronteira pretendida |
|---|---:|---:|---:|---|
| TOST positiva | 0,75 | 0,60 | 0,75 | `D=+0,15` |
| TOST negativa | 0,60 | 0,75 | 0,75 | `D=−0,15` |
| nulo global ISO | 0,60 | 0,60 | 0,75 | `D=−0,15` |

Para cada família e comparador, a tolerância prefixada é `|D_observado−D_alvo|≤0,005`. A geração condiciona `A8` à probabilidade de retorno para atingir a marginal `Q` alvo sob ICC e efeito de texto.

Todas as fronteiras passaram. Exemplos de desvio máximo: 0,001506 na TOST positiva, 0,002269 na negativa e 0,003325 no nulo global ISO.

### 1.2 A8 nunca ocorre com NOT_APPLICABLE

A sequência lógica agora é explícita:

\[
PRE\Rightarrow EFFECT\Rightarrow RETORNO,\qquad A8\Rightarrow PRE,\qquad Q=A8\land RETORNO.
\]

- `PRE`: `d8=0`;
- `NO_EFFECT`: `PRE=1` e `EFFECT=0`;
- `NOT_APPLICABLE`: `PRE=0`;
- `RETORNO`: `PRE=1`, `EFFECT=1` e retorno estabilizado;
- `A8`: somente gerado quando `PRE=1`;
- `Q`: somente quando `A8=1` e `RETORNO=1`.

A validação confirmou `A8≤PRE`, `RETORNO≤PRE` e `Q≤RETORNO` em todos os cenários. Integridade, poder e custos foram recalculados, não apenas as fronteiras.

## 2. Desenho experimental mantido

Não houve redesenho conceitual. Permanecem:

- **12 interações**: `k=1…8`, perturbação depois de `k=8`, leitura perturbada `k=9` e retorno `k=10…12`;
- **p=8,r=10**: `d8=0`, `d9>0`, `d10=d11=d12=0`, `u11=u12=0`;
- blocos individuais com cinco braços, três famílias capazes, focal fixa única e três textos/versões por controle;
- 27 clusters texto-conscientes, sem substituir `n` por `n_eff`;
- dependência `Q–S`, falhas de manipulação, perdas de pareamento e integridade não presumida;
- PLA/OUT fora da evidência primária; somente seis testes ISO-A/ISO-B;
- seis `Q` PLA/OUT como diagnóstico e doze `S` como checagens de manipulação/contaminação.

Os anexos foram alinhados por erratas próprias a 12 interações e `p=8,r=10`.

## 3. Inferência congelada

### 3.1 Permutação e intervalos

A análise usa `2^27` atribuições de sinais por cluster. A resolução mínima é `1/2^27=7,4505805969×10⁻⁹`; empates entram integralmente.

A convolução FFT foi validada contra DP e enumeração explícita, com erro máximo 0. O intervalo focal continua t robusto por 27 clusters, não CP binomial. **A cauda 5σ do intervalo t/Wald não está validada e bloqueia o degrau.**

### 3.2 Primário e falsificação

- Seis testes ISO de não inferioridade, Holm global 6.
- União de falsificação: três intervalos focais + seis direções ISO, Bonferroni `α/9`.
- `POWERED`: seis ISO + focal inferior `>0,80` + integridade + sem `FALSIFIED` + sem `NONSPECIFIC_POWERED`.

### 3.3 TOST e NONSPECIFIC

Os seis TOST PLA/OUT usam duas caudas exatas `20D+3` e `20D−3`, `p=max(p−,p+)`, Holm 6 e empates incluídos.

`NONSPECIFIC_POWERED` exige os seis TOST, focal inferior `>0,80`, integridade e ausência de `FALSIFIED`. Tem precedência sobre `POWERED`. Sua probabilidade é poder sob equivalência verdadeira, não tamanho sob nulo de fronteira.

## 4. Tamanho sob nulo verdadeiro versus poder

### 4.1 Tamanho nas fronteiras corrigidas

| avaliação | estimativa | IC MC 95% | porta |
|---|---:|---:|---|
| nulo global ISO, `D=−0,15`, `α=0,05` | **0,057** | [0,04263; 0,07137] | **OPEN/BORDERLINE — ponto acima, IC inclui 0,05** |
| TOST `D=+0,15`, `α=0,05` | **0,044** | [0,03129; 0,05671] | **PASS** |
| TOST `D=−0,15`, `α=0,05` | **0,040** | [0,02785; 0,05215] | **PASS** |
| nulo global ISO, 5σ | 0,000 | não resolvido | **OPEN — resolução insuficiente** |
| TOST fronteiras 5σ | 0,000 / 0,000 | não resolvido | **OPEN — não validar a cauda** |

As antigas taxas `0,740` e `0,737/0,751` não são mais portões de tamanho: pertencem a cenários mal parametrizados preservados em `REV1`.

### 4.2 Poder sob alternativa e equivalência

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

Poder de `NONSPECIFIC_POWERED` sob equivalência verdadeira:

| cenário | **NONSPECIFIC_POWERED** | IC MC 95% | porta de poder |
|---|---:|---:|---|
| `n=320`, `α=0,05` | **0,022** | [0,01291; 0,03109] | **FAIL** |
| `n=618`, 5σ | **0,311** | [0,28231; 0,33969] | **FAIL** |
| `n=655`, 5σ | **0,412** | [0,38149; 0,44251] | **FAIL** |

Essas taxas não são tamanho: são poder do ramo sob equivalência verdadeira e continuam abaixo de 0,90.

## 5. Integridade e custos recalculados

`INTEGRITY_OK` continua exigindo pares suficientes, `NO_EFFECT≤5%`, `NOT_APPLICABLE≤5%`, checagens `S`, hashes/custódia, extrator, léxico, contexto e perturbações válidos.

O custo primário permanece 20 células × `n` × 12:

| desenho | sessões primárias | interações primárias | adicional líquido `k=1` | base + adicional |
|---|---:|---:|---:|---:|
| base, `n=320` | 6.400 | 76.800 | **163,27** | **76.963,27** |
| 5σ, `n=618` | 12.360 | 148.320 | **312,09** | **148.632,09** |
| 5σ, `n=655` | 13.100 | 157.200 | **335,03** | **157.535,03** |
| estresse, `n=320` | 6.400 | 76.800 | **1.920,00** | **78.720,00** |

O adicional é `candidatos_usados − sessões_primárias`; o `k=1` dos selecionados não é duplicado. Calibração, reposições posteriores e tokens ficam separados e abertos.

## 6. Portões e bloqueios

| portão | resultado |
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

## 7. Reprodução e hashes

- `K06\PODER\r32_motor.py`: SHA-256 `3a1cac5e5255a3606b1180f3122c5eb5fd7c9bbcc207a8e98f07d7baeb5362fa`;
- `K06\PODER\simular_r32_sessoes.py`: SHA-256 `8ebecc1b0a2e29645a22267cf8ebd32f36a272cbd85f03c3c7ab0d91da111d62`;
- `K06\PODER\validar_r32.py`: SHA-256 `d058eda6cd48496ff9387ecba172763687cda9bf3ac5856e3d08d7ff7077f617`;
- `K06\PODER\validacao_r32.json`: SHA-256 `506e1f6805c28b1b835b5fcfd7de4f0e8a48f2595585387e2c26017e4ef21cb3`;
- `K06\PODER\resultados_r32.json`: SHA-256 `228e1d99e0a815a62d4ea55a156e3fe45ab5bf091f619bfce496458690105eb2`;
- `K06\PODER\manifesto_analise_r32.json`: SHA-256 `8b20323937488f7c0c77a22d2bb169d3883d5de81efdfed11e2448478ac192ce`;
- `K06\PODER\MANIFESTO_R32_SHA256.json`: SHA-256 `2dd32a68ac5b31177a3f0f6683cd4bb980928e41b611ba64c89dda9dd81e1804`;
- repetição determinística: bytes idênticos, SHA-256 `455911a61eba5536ed77e73809068394acebfe180a67e66f4317c86c4f8ec07e`.

O padrão do script é `--nsim 1000`. Todos os `resultados_r32_part_*.json` necessários à consolidação estão incluídos no manifesto. `NOT_FALSIFIED` não é `CONFIRMED`; o gate não se move.
