# ERRATA R3.2 K06 — fronteiras D=±0,15 e implicação A8⇒PRE

## 0. Estatuto e preservação

- [DECLARADO] Correção dirigida **revisada internamente**, não ratificada. **BLOQUEADO_PARA_PRODUCAO** permanece obrigatório.
- [REAL] Nenhum modelo de linguagem foi executado e nenhum resultado experimental foi aberto.
- [REAL] A R3.1 está integralmente preservada em `K06\PODER\REV1\`, com `PRESERVACAO_SHA256.txt`.
- [REAL] As antigas taxas `0,740` e `0,737/0,751` pertencem a cenários com `D≈±0,10`, não à fronteira exigida. Elas permanecem como histórico mal parametrizado e não são reutilizadas como tamanho.
- [REAL] Todos os cenários foram recalculados com as mesmas sementes, sem escolha de semente para melhorar resultados.

## 1. Problema 1 — fronteiras que não estavam em D=±0,15

**Defeito:** os níveis 60/75 produziam `Q≈0,618/0,716`, portanto `D≈±0,10`. As taxas anteriores não mediam tamanho sob o nulo correto.

**Correção:** `Q` passou a ser parametrizado diretamente nos cenários de fronteira. A geração de `A8` é condicionada à probabilidade de retorno para atingir a marginal `Q` alvo sob ICC e efeito de texto.

A tolerância prefixada é `|D_observado−D_alvo|≤0,005` por família e comparador.

| cenário | fronteira | maior desvio absoluto | porta |
|---|---:|---:|---|
| TOST positiva | `D=+0,15` | 0,001506 | **PASS** |
| TOST negativa | `D=−0,15` | 0,002269 | **PASS** |
| nulo global ISO | `D=−0,15` | 0,003325 | **PASS** |
| nulo global ISO, 5σ | `D=−0,15` | 0,003044 | **PASS** |
| TOST positiva, 5σ | `D=+0,15` | 0,001628 | **PASS** |
| TOST negativa, 5σ | `D=−0,15` | 0,003053 | **PASS** |

## 2. Problema 2 — A8=1 com NOT_APPLICABLE=1

**Defeito:** o gerador permitia `A8=1` mesmo sem `d8=0`, combinação logicamente impossível.

**Correção:** os estados agora respeitam explicitamente:

\[
PRE\Rightarrow EFFECT\Rightarrow RETORNO,\qquad A8\Rightarrow PRE,\qquad Q=A8\land RETORNO.
\]

`A8` só é gerado com `PRE=1`. `NO_EFFECT` exige `PRE=1` e ausência de efeito; `NOT_APPLICABLE` é `PRE=0`; `RETORNO` exige pré-alvo e efeito; `Q` exige ambos `A8` e `RETORNO`.

A validação confirmou `A8≤PRE`, `RETORNO≤PRE` e `Q≤RETORNO` em todos os cenários. Integridade, poder e custos foram recalculados integralmente.

## 3. Tamanho sob nulo verdadeiro versus poder

### 3.1 Tamanho nas fronteiras corrigidas

| avaliação | estimativa | IC MC 95% | porta |
|---|---:|---:|---|
| nulo global ISO, `D=−0,15`, `α=0,05` | **0,057** | [0,04263; 0,07137] | **OPEN/BORDERLINE** |
| TOST `D=+0,15`, `α=0,05` | **0,044** | [0,03129; 0,05671] | **PASS** |
| TOST `D=−0,15`, `α=0,05` | **0,040** | [0,02785; 0,05215] | **PASS** |
| nulo global ISO, 5σ | 0,000 | não resolvido | **OPEN — resolução insuficiente** |
| TOST fronteiras 5σ | 0,000 / 0,000 | não resolvido | **OPEN — não validar a cauda** |

O ponto global 0,057 excede 0,05, mas o intervalo inclui o nominal. Não se reutiliza o antigo FAIL, nem se declara PASS.

### 3.2 Poder sob alternativa

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

### 3.3 Poder de NONSPECIFIC_POWERED sob equivalência verdadeira

| cenário | **NONSPECIFIC_POWERED** | IC MC 95% | **POWERED** | IC MC 95% |
|---|---:|---:|---:|---:|
| `n=320`, `α=0,05` | **0,022** | [0,01291; 0,03109] | 0,000 | [0; 0] |
| `n=618`, 5σ | **0,311** | [0,28231; 0,33969] | 0,370 | [0,34008; 0,39992] |
| `n=655`, 5σ | **0,412** | [0,38149; 0,44251] | 0,350 | [0,32044; 0,37956] |

Essas taxas são poder sob equivalência verdadeira, não tamanho. Não atingem 0,90.

## 4. Escopos e análise mantidos

- 27 clusters texto-conscientes, sem substituição por `n_eff`.
- Seis testes ISO na evidência primária; PLA/OUT fora dela.
- Seis `Q` PLA/OUT como diagnóstico e doze `S` como checagens de manipulação/contaminação.
- TOST com duas caudas exatas `20D+3` e `20D−3`, `p=max`, Holm 6 e empates incluídos.
- `NONSPECIFIC_POWERED` tem precedência sobre `POWERED`.
- União de falsificação: três intervalos focais + seis direções ISO, Bonferroni `α/9`.
- **12 interações e p=8,r=10** em todos os documentos desta frente.
- Os anexos foram alinhados por erratas próprias a 12 interações e `p=8,r=10`.

## 5. Validação computacional e repetição

- FFT, DP e enumeração explícita: **PASS**, erro máximo **0,0 / 0,0 / 0,0**.
- `A8⇒PRE`, `RETORNO⇒PRE`, `Q⇒RETORNO`: **PASS em todos os cenários**.
- Fronteiras `D=±0,15` dentro de 0,005: **PASS**.
- Repetição do cenário-base: bytes idênticos, SHA-256 `455911a61eba5536ed77e73809068394acebfe180a67e66f4317c86c4f8ec07e`.
- O padrão do script é `--nsim 1000`; não é necessário comando adicional.
- Todos os `resultados_r32_part_*.json` necessários à consolidação estão incluídos no manifesto.

## 6. Custos recalculados

| desenho | sessões primárias | interações primárias | adicional líquido `k=1` | base + adicional |
|---|---:|---:|---:|---:|
| base, `n=320` | 6.400 | 76.800 | **163,27** | **76.963,27** |
| 5σ, `n=618` | 12.360 | 148.320 | **312,09** | **148.632,09** |
| 5σ, `n=655` | 13.100 | 157.200 | **335,03** | **157.535,03** |
| estresse, `n=320` | 6.400 | 76.800 | **1.920,00** | **78.720,00** |

O adicional é `candidatos_usados − sessões_primárias`. O `k=1` dos selecionados não é contado duas vezes. Calibração, reposições posteriores e tokens continuam separados e abertos.

## 7. Portões e bloqueios

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

## 8. Arquivos e hashes

Documentos atualizados:

- `PROTOCOLO_EXPERIMENTAL_R3_K06.md`;
- `PODER_CONJUNTO_K06.md`;
- `DEGRAU_5_SIGMA_K06.md`;
- `ERRATA_R3_2_K06.md`.

Resultados e código:

- `K06\PODER\r32_motor.py`: SHA-256 `3a1cac5e5255a3606b1180f3122c5eb5fd7c9bbcc207a8e98f07d7baeb5362fa`;
- `K06\PODER\simular_r32_sessoes.py`: SHA-256 `8ebecc1b0a2e29645a22267cf8ebd32f36a272cbd85f03c3c7ab0d91da111d62`;
- `K06\PODER\validar_r32.py`: SHA-256 `d058eda6cd48496ff9387ecba172763687cda9bf3ac5856e3d08d7ff7077f617`;
- `K06\PODER\validacao_r32.json`: SHA-256 `506e1f6805c28b1b835b5fcfd7de4f0e8a48f2595585387e2c26017e4ef21cb3`;
- `K06\PODER\resultados_r32.json`: SHA-256 `228e1d99e0a815a62d4ea55a156e3fe45ab5bf091f619bfce496458690105eb2`;
- `K06\PODER\manifesto_analise_r32.json`: SHA-256 `8b20323937488f7c0c77a22d2bb169d3883d5de81efdfed11e2448478ac192ce`;
- `K06\PODER\MANIFESTO_R32_SHA256.json`: SHA-256 `2dd32a68ac5b31177a3f0f6683cd4bb980928e41b611ba64c89dda9dd81e1804`.

**Conclusão:** as duas correções estão fechadas e validadas. O TOST passa, mas poder, extrator, janela, léxico, cauda 5σ e ratificação continuam impedindo produção.
