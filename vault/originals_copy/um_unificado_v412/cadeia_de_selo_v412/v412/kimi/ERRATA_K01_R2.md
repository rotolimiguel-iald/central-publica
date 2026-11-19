# ERRATA K01 R2 — DUAS LACUNAS LÓGICAS DA SEGUNDA REVISÃO

[DECLARADO] Errata ao lado, de 13/11/2026. `REV0` e `ERRATA_K01.md` permanecem intactos. A versão R1 foi preservada em `K01\REV1\` antes destas alterações. Nenhum número JUNO aprovado foi alterado. Nenhum dado foi aberto, nenhuma estatística observada foi calculada, nada foi registrado no Mapa nem depositado na fila.

## 1. Lacuna 1 — cobertura incompleta de S ≥5 e de S NONINDEPENDENT

### O erro na R1, preservado em REV1

[REAL] A linha `3 ≤ r_P < 5` com S `INDEPENDENT` e `r_S ≥ 3` devolvia `TENSION_BOTH` mesmo quando `r_S ≥ 5`. Além disso, as linhas com S `NONINDEPENDENT` podiam cair em `UNDER/ARMED` sem avaliar `r_S`, ignorando o caso `r_S ≥ 5` com `r_P < 5`.

### Correção R2

[DECLARADO] A tabela-verdade agora aplica, sem exceção:

- [DECLARADO] `3 ≤ r_P < 5` + S `INDEPENDENT` + `r_S ≥ 5` → `T_SINGLE(S)_SECOND_ALONE_GE_5` ou `OPEN_RULE_GAP`, nunca `TENSION_BOTH`.
- [DECLARADO] `TENSION_BOTH` somente quando **ambos** estão em `[3,5)`.
- [DECLARADO] `r_P < 5` + S `NONINDEPENDENT` + `r_S ≥ 5` → `T_SINGLE(S)_NONINDEPENDENT` ou `OPEN_RULE_GAP`, em todas as faixas de P.
- [DECLARADO] `r_P ≥ 5` + S `NONINDEPENDENT` + `r_S ≥ 5` → `TENSION_BOTH_NONINDEPENDENT`, nunca `FALSIFIED`, porque a independência obrigatória falha.
- [DECLARADO] Para X ∈ {P,S} com r_X ≥5 e a outra determinação <5 ou ausente, o destino é `T_SINGLE(X)` ou `OPEN_RULE_GAP`; r_S continua calculado mesmo quando S não é independente.
- [DECLARADO] `FALSIFIED` somente com **r_P ≥5 ∧ r_S ≥5 ∧ S INDEPENDENT ∧ integridade P/S**.

[DECLARADO] Nos demais ramos, `TENSION_P`, `TENSION_S`, `MATCHED`, `UNDER` e `ARMED` continuam seguindo as faixas de r e os D separados, sem poder conjunto presumido.

## 2. Lacuna 2 — NONINDEPENDENT e INVALID se confundiam por covariância

### O erro conceitual, preservado em REV1

[REAL] A descrição anterior de `INVALID` incluía covariância/nuisances sem separar a incerteza intrínseca de σ_X da covariância condicional cruzada entre P e S ou entre liberações cumulativas. Isso permitia classificar ausência de covariância cruzada como falha de integridade em vez de falta de independência.

### Correção R2 e ordem fixa

[DECLARADO] A ordem agora é: **integridade intrínseca de P → integridade intrínseca de S → independência**.

- [DECLARADO] **`INVALID` reservado a falhas intrínsecas:** hash/versão, unidade, centro/σ/r não finitos, σ ≤0, fonte/metadados/timestamp, código alterado e covariância/nuisances **intrínseca indispensável à validade de σ_X**.
- [DECLARADO] **`NONINDEPENDENT` para falta de covariância condicional cruzada:** ausência ou não aceitação de covariância condicional P–S ou entre liberações cumulativas produz `NONINDEPENDENT`, não `INVALID` por si só.
- [DECLARADO] **Prevalência:** uma falha intrínseca separada produz `INCONCLUSIVE` antes de qualquer avaliação de independência. Uma covariância cruzada ausente não impede calcular r_S com o σ_S válido.
- [DECLARADO] **Cumulativas:** 207,2 dias contém/estende 59,1 dias; conteúdo incremental exige covariância condicional cruzada e não cria independência nem falha intrínseca por si só.

## 3. Fonte primária e números JUNO inalterados

[REAL] Os números aprovados não foram tocados: Δm²₂₁,pred = 7,237609466718292×10⁻⁵ eV²; planning = 7,388×10⁻⁵ eV²; σ_total = 0,078×10⁻⁵ eV²; D = 1,9281 com σ publicado; 5σ pede 0,407121 %; D90 pede 0,324061 %; 0,5 % dá D = 4,0712; 0,3 % dá D = 6,7854. O poder conjunto permanece [OPEN].

[REAL] A determinação de 207,2 dias permanece ancorada em **`arXiv:2609.37895v1`**, de 29/09/2026. [JUNO Collaboration, 2026](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2609.37895&text=207.2%20live%20days%20of%20data "citation")

[DECLARADO] `JUNO publications` é usado apenas como índice institucional e **não é apresentado como rol atualizado de 2026**. A fonte primária da liberação mais recente continua sendo o arXiv acima.

## 4. Casos sintéticos executáveis no validador

[DECLARADO] `K01_validar.py` contém uma implementação sintética da tabela e 24 casos, sem qualquer dado observado. As expectativas cobrem:

| Classe verificada | Resultado exigido |
|---|---|
| P ≥5 com S ausente ou r_S <5 | `SINGLE_P` |
| P <5 com S independente e r_S ≥5 | `SINGLE_S` |
| P <5 com S não independente e r_S ≥5 | `SINGLE_S` |
| P e S independentes ≥5 | `FALSIFIED` |
| P e S ≥5 com S não independente | `BOTH_NONINDEPENDENT`, nunca `FALSIFIED` |
| Ambos independentes em [3,5) | `BOTH` |
| P <3 e S em [3,5) | `TENSION_S`, não `BOTH` |
| P ou S com r não finito | `INCONCLUSIVE_P/S` |
| S `INVALID` com r_S ≥5 | `INCONCLUSIVE_S` |
| Covariância cruzada ausente | `NONINDEPENDENT`, não `INVALID` |
| Covariância intrínseca inválida | `INCONCLUSIVE_S` |
| P ausente | `AWAITING_SOURCE_P` |
| P e S ≤1 e independentes | `MATCHED` |

[DECLARADO] O validador também exige exatamente 20 canais, campos aninhados e fontes resolvidas, números JUNO inalterados, consulta real ao Mapa, resumo ≤15 linhas, REV0/REV1 íntegros e referência primária `arXiv:2609.37895v1`.

## 5. REV1 — preservação com tamanhos e hashes

[REAL] A versão R1 foi copiada antes das alterações para `K01\REV1\`. Estes valores pertencem à R1, não à versão R2.

| Arquivo REV1 | Bytes | sha256 |
|---|---:|---|
| `2026-11-13_REV1_ENTREGA_K01.md` | 28836 | `482223368239a565c3953bac3ec8e84aaecd36f33008193c714be957b4f41fcc` |
| `2026-11-13_REV1_CANAIS_K01.json` | 87641 | `8943d3fc3074c7c5f8676c2588ed6ad67aaaac9daefaac4b7daaf146b6479bab` |
| `2026-11-13_REV1_PRE_REGISTRO_CEGO_RASCUNHO_K01.md` | 24344 | `95127964bc9414ffed724ca71aae21ece40a779b95353346df740ec681006f0a` |
| `2026-11-13_REV1_REGISTRO_MAPA_K01.json` | 7653 | `7bb2dbc66636cb7a8bede51d85170cb18e0c7dc632d86ab24543cce70e64c745` |
| `2026-11-13_REV1_PERGUNTA_K01.md` | 5538 | `ebb60057ddd928e8b207d4e9d6977f453cff4ab5a214690deb2052cdddf9c9de` |
| `2026-11-13_REV1_K01_validar.py` | 14816 | `4d8f15a7526874032baedf4b61d495fb12057950f4efc2653985d6e31b7a2dcf` |
| `2026-11-13_REV1_VALIDACAO_K01.json` | 4328 | `7d82d17894696c606352aa13b89922f99bca4a3e844c759e299ded636d8f8f93` |

[REAL] Backup local: [REV1](C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K01\REV1). `VALIDACAO_K01.json` contém uma seção própria para REV1, além da seção REV0 já existente e dos novos hashes canônicos.

## 6. Estatuto após R2

[DERIVED] A conclusão de ausência de canal pronto permanece. Só a tabela-verdade e a fronteira integridade/independência foram corrigidas; não houve alteração de planning, precisão, fonte ou poder JUNO.

[DECLARADO] A nova revisão pode conferir `PRE_REGISTRO_CEGO_RASCUNHO_K01.md`, `CANAIS_K01.json → neutrino_m2_juno.funcao_veredito`, `ENTREGA_K01.md`, `PERGUNTA_K01.md`, `REGISTRO_MAPA_K01.json`, `K01_validar.py` e `VALIDACAO_K01.json`. `NOT_FALSIFIED ≠ CONFIRMED`; o gate permanece imóvel; nada foi registrado nem depositado.
