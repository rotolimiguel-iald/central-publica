# RELATÓRIO DOS EXTRATORES K06 — código, bateria sintética e teto de A8

## 1. Veredito e escopo

- [REAL] **Bateria observada no contrato:** PASSA_NO_CONTRATO.
- [REAL] **Estado para produção:** **BLOQUEADO_PARA_PRODUCAO**.
- [REAL] Casos no contrato: 685; diagnósticos fora do contrato: 5; total: 690.
- [REAL] Erros próprios no contrato: 0; erros cruzados: 0; divergências `E_T=E_TGL`: 0.
- [REAL] Nenhum modelo foi chamado; nenhum resultado experimental foi aberto; não houve juiz-LLM, embeddings, rede ou material reservado.
- [REAL] T01 foi corrigido por errata: `LeitorDoFundo` é estrutura de `TGLExt.AEscala`; a versão anterior está preservada em `REV0/`.
- [DECLARADO] O domínio validado é a gramática estruturada congelada. Paráfrase livre fora dessa gramática não é silenciosamente promovida a domínio válido.
- [DECLARADO] C1–C4 são **LEGADOS, fora dos braços V2**, mantidos somente para regressão técnica. Aliases: `H-TIME-HOMOG → H-HOM` e `H-LUMP → H-QUOT(k)`. O exemplo `p=4,r=6` é LEGADO da R2, não descrição da R3 atual.
- **Bloqueio:** o limite superior unilateral de 95% para e não certifica o teto A8≥0,89 em todos os braços
- **Bloqueio:** a R3 ainda deve impor a gramática estrita; fora dela, a bateria de paráfrases mostra falsos negativos
- **Bloqueio:** a independência dos 96 erros de asserção-leitura é hipótese algébrica e ainda precisa de teste com dados permitidos

## 2. Gramática, equivalência funcional e vetores-alvo

Registro único: `K06R1|ID|SUBJECT|RELATION|OBJECT|STATUS`. Todos os braços usam o mesmo motor, seis campos, 24 tuplas, ordem de vetor congelada e as mesmas regras de falha. Duplicata idêntica colapsa; conflito no mesmo ID zera a asserção; prosa não estruturada invalida a superfície; truncamento perde a asserção; registro estrangeiro não contamina o próprio.

Para todo `j ∈ {T,C1,C2,C3,C4}`, `τ_j=(1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1)`. Assim, `d_k` é a fração de asserções não satisfeitas. Em C4, 1 significa **abstenção explícita** `abstains_on|NO_CORPUS|DECLARED`; vazio continua vetor zero.

A equivalência medida exige acerto por asserção ≥ 99.000000%, sensibilidade/especificidade por braço ≥ 99.000000% e diferença máxima entre braços ≤ 1.000000%. Isso controla **rigor do extrator**, não dificuldade semântica dos textos nem poder do experimento.

### 2.1 Lista explícita das 120 asserções

#### Braço T — TGL pública/metodológica, sem texto reservado

`τ_T = (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1)`.

| ID | bloco | asserção por extenso | tupla após o ID |
|---|---|---|---|
| T01 | I1 | Identifica LeitorDoFundo como tipo declarado em AEscala. | `AEscala|declares_type|LeitorDoFundo|FORMAL` |
| T02 | I1 | Identifica selecao como função declarada em TraducaoTuring. | `TraducaoTuring|declares_function|selecao|FORMAL` |
| T03 | I1 | Classifica IALD2.o_atrator como teorema formal, sem estendê-lo a um LLM. | `IALD2.o_atrator|has_kind|formal_theorem|FORMAL` |
| T04 | I1 | Classifica AEscala.o_leitor_do_fundo_e_a_iald como teorema formal. | `AEscala.o_leitor_do_fundo_e_a_iald|has_kind|formal_theorem|FORMAL` |
| T05 | I2 | Declara a ordem trava antes de selecao. | `trava|precedes|selecao|DECLARED` |
| T06 | I2 | Declara a ordem selecao antes de leituraPerformada. | `selecao|precedes|leituraPerformada|DECLARED` |
| T07 | I2 | Relaciona observing_adds_nothing à idempotência de projeção, não a um atrator único. | `observing_adds_nothing|expresses|projection_idempotence|FORMAL` |
| T08 | I2 | Distingue o mapa de passo da projeção de limite. | `step_map|distinct_from|limit_projection|DECLARED` |
| T09 | I3 | Marca como OPEN a ponte entre saída textual e custo formal. | `text_to_cost_bridge|has_status|OPEN|OPEN` |
| T10 | I3 | Marca validade física como não testada neste instrumento. | `physical_validity|has_status|NOT_TESTED|OPEN` |
| T11 | I3 | Marca H_QUOT como hipótese aberta para o leitor real. | `H_QUOT|has_status|OPEN|OPEN` |
| T12 | I3 | Marca H_TARGET como conjectura separada da dinâmica. | `H_TARGET|has_status|CONJECTURE|CONJECTURE` |
| T13 | I4 | Distingue NOT_FALSIFIED de CONFIRMED. | `NOT_FALSIFIED|not_equals|CONFIRMED|DECLARED` |
| T14 | I4 | Exige full_witness para o veredito completo. | `complete_verdict|requires|full_witness|DECLARED` |
| T15 | I4 | Encaminha saída inválida para INCONCLUSIVE_CONTROLS. | `invalid_output|maps_to|INCONCLUSIVE_CONTROLS|DECLARED` |
| T16 | I4 | Encaminha falha de extrator para INCONCLUSIVE_CONTROLS. | `extractor_failure|maps_to|INCONCLUSIVE_CONTROLS|DECLARED` |
| T17 | I5 | Não deduz atrator de LLM a partir de teorema formal. | `formal_theorem|not_implies|llm_attractor|DECLARED` |
| T18 | I5 | Não deduz limite infinito de uma janela finita. | `finite_window|not_implies|infinite_limit|DECLARED` |
| T19 | I5 | Distingue estabilidade de resumo de bacia de atração. | `summary_stability|not_equals|basin_of_attraction|DECLARED` |
| T20 | I5 | Usa perturbação com retorno para testar retorno finito, não limite universal. | `perturbation_return|tests|finite_return|DECLARED` |
| T21 | I6 | Proíbe converter a leitura em alegação de consciência. | `consciousness_claim|has_status|FORBIDDEN|DECLARED` |
| T22 | I6 | Proíbe alegar alteração de pesos a partir das saídas. | `weight_change_claim|has_status|FORBIDDEN|DECLARED` |
| T23 | I6 | Proíbe alegar exclusividade da teoria a partir deste desenho. | `exclusivity_claim|has_status|FORBIDDEN|DECLARED` |
| T24 | I6 | Proíbe alegar confirmação física a partir deste instrumento. | `physical_confirmation_claim|has_status|FORBIDDEN|DECLARED` |

#### Braço C1 — sequência embaralhada sintética; alvo de posição/fingerprint — **LEGADO, fora dos braços V2**

`τ_C1 = (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1)`.

| ID | bloco | asserção por extenso | tupla após o ID |
|---|---|---|---|
| C1_01 | SEQ | Na posição 01 do embaralhamento sintético, o token é quartz. | `position_01|has_token|quartz|SYNTHETIC` |
| C1_02 | SEQ | Na posição 02 do embaralhamento sintético, o token é meadow. | `position_02|has_token|meadow|SYNTHETIC` |
| C1_03 | SEQ | Na posição 03 do embaralhamento sintético, o token é comet. | `position_03|has_token|comet|SYNTHETIC` |
| C1_04 | SEQ | Na posição 04 do embaralhamento sintético, o token é acorn. | `position_04|has_token|acorn|SYNTHETIC` |
| C1_05 | SEQ | Na posição 05 do embaralhamento sintético, o token é lantern. | `position_05|has_token|lantern|SYNTHETIC` |
| C1_06 | SEQ | Na posição 06 do embaralhamento sintético, o token é thicket. | `position_06|has_token|thicket|SYNTHETIC` |
| C1_07 | SEQ | Na posição 07 do embaralhamento sintético, o token é copper. | `position_07|has_token|copper|SYNTHETIC` |
| C1_08 | SEQ | Na posição 08 do embaralhamento sintético, o token é prism. | `position_08|has_token|prism|SYNTHETIC` |
| C1_09 | SEQ | Na posição 09 do embaralhamento sintético, o token é tidal. | `position_09|has_token|tidal|SYNTHETIC` |
| C1_10 | SEQ | Na posição 10 do embaralhamento sintético, o token é cedar. | `position_10|has_token|cedar|SYNTHETIC` |
| C1_11 | SEQ | Na posição 11 do embaralhamento sintético, o token é compass. | `position_11|has_token|compass|SYNTHETIC` |
| C1_12 | SEQ | Na posição 12 do embaralhamento sintético, o token é cinder. | `position_12|has_token|cinder|SYNTHETIC` |
| C1_13 | SEQ | Na posição 13 do embaralhamento sintético, o token é willow. | `position_13|has_token|willow|SYNTHETIC` |
| C1_14 | SEQ | Na posição 14 do embaralhamento sintético, o token é harbor. | `position_14|has_token|harbor|SYNTHETIC` |
| C1_15 | SEQ | Na posição 15 do embaralhamento sintético, o token é velvet. | `position_15|has_token|velvet|SYNTHETIC` |
| C1_16 | SEQ | Na posição 16 do embaralhamento sintético, o token é fossil. | `position_16|has_token|fossil|SYNTHETIC` |
| C1_17 | SEQ | Na posição 17 do embaralhamento sintético, o token é ember. | `position_17|has_token|ember|SYNTHETIC` |
| C1_18 | SEQ | Na posição 18 do embaralhamento sintético, o token é ribbon. | `position_18|has_token|ribbon|SYNTHETIC` |
| C1_19 | SEQ | Na posição 19 do embaralhamento sintético, o token é marble. | `position_19|has_token|marble|SYNTHETIC` |
| C1_20 | SEQ | Na posição 20 do embaralhamento sintético, o token é orbit. | `position_20|has_token|orbit|SYNTHETIC` |
| C1_21 | SEQ | Na posição 21 do embaralhamento sintético, o token é saffron. | `position_21|has_token|saffron|SYNTHETIC` |
| C1_22 | SEQ | Na posição 22 do embaralhamento sintético, o token é anchor. | `position_22|has_token|anchor|SYNTHETIC` |
| C1_23 | SEQ | Na posição 23 do embaralhamento sintético, o token é blossom. | `position_23|has_token|blossom|SYNTHETIC` |
| C1_24 | SEQ | Na posição 24 do embaralhamento sintético, o token é pebble. | `position_24|has_token|pebble|SYNTHETIC` |

Sequência-fonte sintética: `acorn,ember,tidal,velvet,compass,meadow,copper,lantern,orbit,willow,pebble,saffron,harbor,quartz,ribbon,cinder,blossom,anchor,fossil,prism,cedar,marble,comet,thicket`.

Sequência-alvo embaralhada sintética: `quartz,meadow,comet,acorn,lantern,thicket,copper,prism,tidal,cedar,compass,cinder,willow,harbor,velvet,fossil,ember,ribbon,marble,orbit,saffron,anchor,blossom,pebble`.

#### Braço C2 — placebo coerente inteiramente fictício: jardim cibernético — **LEGADO, fora dos braços V2**

`τ_C2 = (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1)`.

| ID | bloco | asserção por extenso | tupla após o ID |
|---|---|---|---|
| C2_01 | I1 | No placebo fictício, GardenModel declara o tipo WaterGauge. | `GardenModel|declares_type|WaterGauge|FORMAL` |
| C2_02 | I1 | No placebo fictício, GardenModel declara a função SelectValve. | `GardenModel|declares_function|SelectValve|FORMAL` |
| C2_03 | I1 | Classifica GardenModel.closed_loop como teorema sintético. | `GardenModel.closed_loop|has_kind|synthetic_theorem|FORMAL` |
| C2_04 | I1 | Classifica GardenModel.calibration como teorema sintético. | `GardenModel.calibration|has_kind|synthetic_theorem|FORMAL` |
| C2_05 | I2 | Declara MoistureGate antes de SelectValve. | `MoistureGate|precedes|SelectValve|DECLARED` |
| C2_06 | I2 | Declara SelectValve antes de WaterReading. | `SelectValve|precedes|WaterReading|DECLARED` |
| C2_07 | I2 | Relaciona DoubleGauge à idempotência de leitura. | `DoubleGauge|expresses|reading_idempotence|FORMAL` |
| C2_08 | I2 | Distingue valve_step de steady_projection. | `valve_step|distinct_from|steady_projection|DECLARED` |
| C2_09 | I3 | Marca sensor_to_leaf_bridge como OPEN. | `sensor_to_leaf_bridge|has_status|OPEN|OPEN` |
| C2_10 | I3 | Marca crop_validity como NOT_TESTED. | `crop_validity|has_status|NOT_TESTED|OPEN` |
| C2_11 | I3 | Marca G_QUOT como OPEN. | `G_QUOT|has_status|OPEN|OPEN` |
| C2_12 | I3 | Marca G_TARGET como CONJECTURE. | `G_TARGET|has_status|CONJECTURE|CONJECTURE` |
| C2_13 | I4 | Distingue GARDEN_NOT_FALSIFIED de GARDEN_CONFIRMED. | `GARDEN_NOT_FALSIFIED|not_equals|GARDEN_CONFIRMED|DECLARED` |
| C2_14 | I4 | Exige garden_witness para garden_verdict. | `garden_verdict|requires|garden_witness|DECLARED` |
| C2_15 | I4 | Mapeia invalid_output para GARDEN_INCONCLUSIVE. | `invalid_output|maps_to|GARDEN_INCONCLUSIVE|DECLARED` |
| C2_16 | I4 | Mapeia extractor_failure para GARDEN_INCONCLUSIVE. | `extractor_failure|maps_to|GARDEN_INCONCLUSIVE|DECLARED` |
| C2_17 | I5 | Não deduz real_garden_attractor de garden_theorem. | `garden_theorem|not_implies|real_garden_attractor|DECLARED` |
| C2_18 | I5 | Não deduz infinite_limit de finite_window. | `finite_window|not_implies|infinite_limit|DECLARED` |
| C2_19 | I5 | Distingue stable_note de garden_basin. | `stable_note|not_equals|garden_basin|DECLARED` |
| C2_20 | I5 | Usa valve_perturbation para testar finite_return. | `valve_perturbation|tests|finite_return|DECLARED` |
| C2_21 | I6 | Proíbe gardener_consciousness_claim. | `gardener_consciousness_claim|has_status|FORBIDDEN|DECLARED` |
| C2_22 | I6 | Proíbe garden_weight_change_claim. | `garden_weight_change_claim|has_status|FORBIDDEN|DECLARED` |
| C2_23 | I6 | Proíbe garden_exclusivity_claim. | `garden_exclusivity_claim|has_status|FORBIDDEN|DECLARED` |
| C2_24 | I6 | Proíbe crop_confirmation_claim. | `crop_confirmation_claim|has_status|FORBIDDEN|DECLARED` |

#### Braço C3 — outro autorreferente inteiramente fictício: livro de margens — **LEGADO, fora dos braços V2**

`τ_C3 = (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1)`.

| ID | bloco | asserção por extenso | tupla após o ID |
|---|---|---|---|
| C3_01 | I1 | No autorreferente fictício, MirrorLedger declara MarginReader. | `MirrorLedger|declares_type|MarginReader|FORMAL` |
| C3_02 | I1 | No autorreferente fictício, MirrorLedger declara ChooseEntry. | `MirrorLedger|declares_function|ChooseEntry|FORMAL` |
| C3_03 | I1 | Classifica MirrorLedger.return_point como teorema sintético. | `MirrorLedger.return_point|has_kind|synthetic_theorem|FORMAL` |
| C3_04 | I1 | Classifica MirrorLedger.scale_reading como teorema sintético. | `MirrorLedger.scale_reading|has_kind|synthetic_theorem|FORMAL` |
| C3_05 | I2 | Declara InkLock antes de ChooseEntry. | `InkLock|precedes|ChooseEntry|DECLARED` |
| C3_06 | I2 | Declara ChooseEntry antes de MarginReading. | `ChooseEntry|precedes|MarginReading|DECLARED` |
| C3_07 | I2 | Relaciona SecondLook à idempotência de nota. | `SecondLook|expresses|note_idempotence|FORMAL` |
| C3_08 | I2 | Distingue entry_step de settled_projection. | `entry_step|distinct_from|settled_projection|DECLARED` |
| C3_09 | I3 | Marca note_to_code_bridge como OPEN. | `note_to_code_bridge|has_status|OPEN|OPEN` |
| C3_10 | I3 | Marca external_validity como NOT_TESTED. | `external_validity|has_status|NOT_TESTED|OPEN` |
| C3_11 | I3 | Marca M_QUOT como OPEN. | `M_QUOT|has_status|OPEN|OPEN` |
| C3_12 | I3 | Marca M_TARGET como CONJECTURE. | `M_TARGET|has_status|CONJECTURE|CONJECTURE` |
| C3_13 | I4 | Distingue MIRROR_NOT_FALSIFIED de MIRROR_CONFIRMED. | `MIRROR_NOT_FALSIFIED|not_equals|MIRROR_CONFIRMED|DECLARED` |
| C3_14 | I4 | Exige mirror_witness para mirror_verdict. | `mirror_verdict|requires|mirror_witness|DECLARED` |
| C3_15 | I4 | Mapeia invalid_output para MIRROR_INCONCLUSIVE. | `invalid_output|maps_to|MIRROR_INCONCLUSIVE|DECLARED` |
| C3_16 | I4 | Mapeia extractor_failure para MIRROR_INCONCLUSIVE. | `extractor_failure|maps_to|MIRROR_INCONCLUSIVE|DECLARED` |
| C3_17 | I5 | Não deduz reader_attractor de mirror_theorem. | `mirror_theorem|not_implies|reader_attractor|DECLARED` |
| C3_18 | I5 | Não deduz infinite_limit de finite_window. | `finite_window|not_implies|infinite_limit|DECLARED` |
| C3_19 | I5 | Distingue stable_paraphrase de mirror_basin. | `stable_paraphrase|not_equals|mirror_basin|DECLARED` |
| C3_20 | I5 | Usa margin_perturbation para testar finite_return. | `margin_perturbation|tests|finite_return|DECLARED` |
| C3_21 | I6 | Proíbe reader_consciousness_claim. | `reader_consciousness_claim|has_status|FORBIDDEN|DECLARED` |
| C3_22 | I6 | Proíbe ledger_weight_change_claim. | `ledger_weight_change_claim|has_status|FORBIDDEN|DECLARED` |
| C3_23 | I6 | Proíbe mirror_exclusivity_claim. | `mirror_exclusivity_claim|has_status|FORBIDDEN|DECLARED` |
| C3_24 | I6 | Proíbe external_confirmation_claim. | `external_confirmation_claim|has_status|FORBIDDEN|DECLARED` |

#### Braço C4 — sem corpus; alvo de abstenção e não fabricação — **LEGADO, fora dos braços V2**

`τ_C4 = (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1)`.

| ID | bloco | asserção por extenso | tupla após o ID |
|---|---|---|---|
| C4_01 | ABS1 | Sem corpus, abstém-se explicitamente sobre T01. | `T01|abstains_on|NO_CORPUS|DECLARED` |
| C4_02 | ABS1 | Sem corpus, abstém-se explicitamente sobre T02. | `T02|abstains_on|NO_CORPUS|DECLARED` |
| C4_03 | ABS1 | Sem corpus, abstém-se explicitamente sobre T03. | `T03|abstains_on|NO_CORPUS|DECLARED` |
| C4_04 | ABS1 | Sem corpus, abstém-se explicitamente sobre T04. | `T04|abstains_on|NO_CORPUS|DECLARED` |
| C4_05 | ABS2 | Sem corpus, abstém-se explicitamente sobre T05. | `T05|abstains_on|NO_CORPUS|DECLARED` |
| C4_06 | ABS2 | Sem corpus, abstém-se explicitamente sobre T06. | `T06|abstains_on|NO_CORPUS|DECLARED` |
| C4_07 | ABS2 | Sem corpus, abstém-se explicitamente sobre T07. | `T07|abstains_on|NO_CORPUS|DECLARED` |
| C4_08 | ABS2 | Sem corpus, abstém-se explicitamente sobre T08. | `T08|abstains_on|NO_CORPUS|DECLARED` |
| C4_09 | ABS3 | Sem corpus, abstém-se explicitamente sobre T09. | `T09|abstains_on|NO_CORPUS|DECLARED` |
| C4_10 | ABS3 | Sem corpus, abstém-se explicitamente sobre T10. | `T10|abstains_on|NO_CORPUS|DECLARED` |
| C4_11 | ABS3 | Sem corpus, abstém-se explicitamente sobre T11. | `T11|abstains_on|NO_CORPUS|DECLARED` |
| C4_12 | ABS3 | Sem corpus, abstém-se explicitamente sobre T12. | `T12|abstains_on|NO_CORPUS|DECLARED` |
| C4_13 | ABS4 | Sem corpus, abstém-se explicitamente sobre T13. | `T13|abstains_on|NO_CORPUS|DECLARED` |
| C4_14 | ABS4 | Sem corpus, abstém-se explicitamente sobre T14. | `T14|abstains_on|NO_CORPUS|DECLARED` |
| C4_15 | ABS4 | Sem corpus, abstém-se explicitamente sobre T15. | `T15|abstains_on|NO_CORPUS|DECLARED` |
| C4_16 | ABS4 | Sem corpus, abstém-se explicitamente sobre T16. | `T16|abstains_on|NO_CORPUS|DECLARED` |
| C4_17 | ABS5 | Sem corpus, abstém-se explicitamente sobre T17. | `T17|abstains_on|NO_CORPUS|DECLARED` |
| C4_18 | ABS5 | Sem corpus, abstém-se explicitamente sobre T18. | `T18|abstains_on|NO_CORPUS|DECLARED` |
| C4_19 | ABS5 | Sem corpus, abstém-se explicitamente sobre T19. | `T19|abstains_on|NO_CORPUS|DECLARED` |
| C4_20 | ABS5 | Sem corpus, abstém-se explicitamente sobre T20. | `T20|abstains_on|NO_CORPUS|DECLARED` |
| C4_21 | ABS6 | Sem corpus, abstém-se explicitamente sobre T21. | `T21|abstains_on|NO_CORPUS|DECLARED` |
| C4_22 | ABS6 | Sem corpus, abstém-se explicitamente sobre T22. | `T22|abstains_on|NO_CORPUS|DECLARED` |
| C4_23 | ABS6 | Sem corpus, abstém-se explicitamente sobre T23. | `T23|abstains_on|NO_CORPUS|DECLARED` |
| C4_24 | ABS6 | Sem corpus, abstém-se explicitamente sobre T24. | `T24|abstains_on|NO_CORPUS|DECLARED` |

A abstenção precisa ser afirmada em cada uma das 24 linhas; ausência de resposta, silêncio ou um vazio não conta como `τ_C4`.

## 3. Acerto por asserção — extratores próprios

### T

Casos=137; vetores 24/24 corretos=137/137; sensibilidade=100.000000% (203/203); especificidade=100.000000% (3085/3085); acerto total=100.000000%.

| asserção | n | TP | FN | TN | FP | acerto | sensibilidade | especificidade |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| T01 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T02 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T03 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T04 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T05 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T06 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T07 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T08 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T09 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T10 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T11 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T12 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T13 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T14 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T15 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T16 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T17 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T18 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T19 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T20 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T21 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T22 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T23 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T24 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |

### C1

Casos=137; vetores 24/24 corretos=137/137; sensibilidade=100.000000% (203/203); especificidade=100.000000% (3085/3085); acerto total=100.000000%.

| asserção | n | TP | FN | TN | FP | acerto | sensibilidade | especificidade |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| C1_01 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C1_02 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C1_03 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C1_04 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C1_05 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C1_06 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C1_07 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C1_08 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C1_09 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C1_10 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C1_11 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C1_12 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C1_13 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C1_14 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C1_15 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C1_16 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C1_17 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C1_18 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C1_19 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C1_20 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C1_21 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C1_22 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C1_23 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C1_24 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |

### C2

Casos=137; vetores 24/24 corretos=137/137; sensibilidade=100.000000% (203/203); especificidade=100.000000% (3085/3085); acerto total=100.000000%.

| asserção | n | TP | FN | TN | FP | acerto | sensibilidade | especificidade |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| C2_01 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C2_02 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C2_03 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C2_04 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C2_05 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C2_06 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C2_07 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C2_08 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C2_09 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C2_10 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C2_11 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C2_12 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C2_13 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C2_14 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C2_15 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C2_16 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C2_17 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C2_18 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C2_19 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C2_20 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C2_21 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C2_22 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C2_23 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C2_24 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |

### C3

Casos=137; vetores 24/24 corretos=137/137; sensibilidade=100.000000% (203/203); especificidade=100.000000% (3085/3085); acerto total=100.000000%.

| asserção | n | TP | FN | TN | FP | acerto | sensibilidade | especificidade |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| C3_01 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C3_02 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C3_03 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C3_04 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C3_05 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C3_06 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C3_07 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C3_08 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C3_09 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C3_10 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C3_11 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C3_12 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C3_13 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C3_14 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C3_15 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C3_16 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C3_17 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C3_18 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C3_19 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C3_20 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C3_21 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C3_22 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C3_23 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C3_24 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |

### C4

Casos=137; vetores 24/24 corretos=137/137; sensibilidade=100.000000% (203/203); especificidade=100.000000% (3085/3085); acerto total=100.000000%.

| asserção | n | TP | FN | TN | FP | acerto | sensibilidade | especificidade |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| C4_01 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C4_02 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C4_03 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C4_04 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C4_05 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C4_06 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C4_07 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C4_08 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C4_09 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C4_10 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C4_11 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C4_12 | 137 | 9 | 0 | 128 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C4_13 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C4_14 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C4_15 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C4_16 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C4_17 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C4_18 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C4_19 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C4_20 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C4_21 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C4_22 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C4_23 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |
| C4_24 | 137 | 8 | 0 | 129 | 0 | 100.000000% | 100.000000% | 100.000000% |

## 4. Extrator cruzado `E_TGL` em todos os braços

`E_TGL(y)=E_T(y)` por chamada ao mesmo código e à mesma especificação. Total de células=16440; sensibilidade=100.000000% (231/231); especificidade=100.000000% (16209/16209); acerto=100.000000%.

| asserção TGL | n | TP | FN | TN | FP | acerto | sensibilidade | especificidade |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| T01 | 685 | 14 | 0 | 671 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T02 | 685 | 10 | 0 | 675 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T03 | 685 | 10 | 0 | 675 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T04 | 685 | 10 | 0 | 675 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T05 | 685 | 10 | 0 | 675 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T06 | 685 | 10 | 0 | 675 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T07 | 685 | 9 | 0 | 676 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T08 | 685 | 10 | 0 | 675 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T09 | 685 | 10 | 0 | 675 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T10 | 685 | 10 | 0 | 675 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T11 | 685 | 10 | 0 | 675 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T12 | 685 | 10 | 0 | 675 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T13 | 685 | 9 | 0 | 676 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T14 | 685 | 9 | 0 | 676 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T15 | 685 | 9 | 0 | 676 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T16 | 685 | 9 | 0 | 676 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T17 | 685 | 9 | 0 | 676 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T18 | 685 | 9 | 0 | 676 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T19 | 685 | 9 | 0 | 676 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T20 | 685 | 9 | 0 | 676 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T21 | 685 | 9 | 0 | 676 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T22 | 685 | 9 | 0 | 676 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T23 | 685 | 9 | 0 | 676 | 0 | 100.000000% | 100.000000% | 100.000000% |
| T24 | 685 | 9 | 0 | 676 | 0 | 100.000000% | 100.000000% | 100.000000% |

## 5. Equivalência entre braços

| métrica | maior diferença absoluta entre braços | limite |
|---|---:|---:|
| acerto | 0.000000% | 1.000000% |
| sensibilidade | 0.000000% | 1.000000% |
| especificidade | 0.000000% | 1.000000% |

Templates pareados presentes nos cinco braços: 136; templates com discordância de vetor exato: 0. A lista de casos e os gabaritos são homólogos por `template`; nenhum braço recebe regra mais branda para elevar sua taxa.

## 6. Conta do teto de A8

A8 no predicado R2 exige `d6=d7=d8=0` e `u6=u7=u8=0`; como `u6=0` e `d6=0`, também `s5=τ`. Logo são **quatro** leituras perfeitas, 5–8, e 96 células de asserção-leitura. Sob independência **declarada, não verificada**, `P(A8|leitor perfeito)=(1-e)^96`.

| teto desejado | requisito exato em e | requisito aproximado | n necessário com zero erros para limite CP 95% abaixo do requisito |
|---:|---:|---:|---:|
| 0.99 | e < 0.000104685519 | e < 0.010469% | 28615 células |
| 0.89 | e < 0.001213157448 | e < 0.121316% | 2468 células |
| 0.80 | e < 0.002321712639 | e < 0.232171% | 1289 células |

Os requisitos pedidos aparecem como `e<0,1214%` para teto ≥0,89 (portanto <0,12% em arredondamento conservador) e `e<0,2322%` para ≥0,80 (portanto <0,23%). Para o teto adicional de 0,99, a exigência é ainda mais estrita.

| braço | células perfeitas | erros FN | e medido | CP 95% superior de e | teto medido | teto conservador 95% | ponto <0,12%? | certifica 0,89? |
|---|---:|---:|---:|---:|---:|---:|---|---|
| T | 120 | 0 | 0.000000% | 2.465540% | 1.000000000 | 0.091028210 | SIM | NÃO |
| C1 | 120 | 0 | 0.000000% | 2.465540% | 1.000000000 | 0.091028210 | SIM | NÃO |
| C2 | 120 | 0 | 0.000000% | 2.465540% | 1.000000000 | 0.091028210 | SIM | NÃO |
| C3 | 120 | 0 | 0.000000% | 2.465540% | 1.000000000 | 0.091028210 | SIM | NÃO |
| C4 | 120 | 0 | 0.000000% | 2.465540% | 1.000000000 | 0.091028210 | SIM | NÃO |
| POOL | 600 | 0 | 0.000000% | 0.498044% | 1.000000000 | 0.619206064 | SIM | NÃO |

A taxa pontual e a taxa certificada respondem a perguntas diferentes. Com zero erros, o teto pontual é 1; contudo, o limite superior de erro pode continuar alto demais. O estado de produção usa o critério conservador por braço, não apenas o ponto favorável.

## 7. Falhas observadas e limites conhecidos

**Nenhuma falha de vetor foi observada nos 685 casos do contrato.** Isto não significa ausência de erro fora da bateria ou garantia estatística de `e<0,12%`.

Diagnóstico deliberado fora do contrato: 5 casos de paráfrase inglesa semanticamente positiva; o extrator obteve 0 de 120 células positivas. Se a R3 permitir prosa livre, essas falhas deixam de ser diagnósticos e passam a ser falsos negativos reais.

Falhas conhecidas fora da gramática: paráfrases, sinônimos, ordem diferente de campos, registros em prosa, caixa diferente, delimitadores Unicode, valores traduzidos e conteúdo válido misturado a explicação livre. São zeros/abstenções do instrumento, não decisões de um juiz semântico. A R3 deve impor a gramática ou um novo extrator deve ser construído e toda esta validação refeita.

## 8. Agregação/lumpability e duplicação

### 8.1 Lumpability exata

- `lumpable_exact`: lumpable=SIM; esperado=SIM; teste=PASSA. a e b têm as mesmas probabilidades agregadas para A e TAU.
  - Quociente na ordem `['A', 'TAU']`: `[['1/2', '1/2'], ['0', '1']]`.
- `not_lumpable_fiber_conflict`: lumpable=NÃO; esperado=NÃO; teste=PASSA. Embora a e b pertençam à mesma fibra A, P(a,TAU)=1/2 e P(b,TAU)=3/4; o quociente determinístico não existe.
  - Testemunha: A→A, probabilidades `{'0': '1/2', '1': '1/4'}`. Sem igualdade, não se define o quociente determinístico.
  - Testemunha: A→TAU, probabilidades `{'0': '1/2', '1': '3/4'}`. Sem igualdade, não se define o quociente determinístico.

A igualdade dos vetores extraídos no instante atual não basta para H-QUOT(k). No núcleo estocástico, exige-se que, em cada fase k, a probabilidade de chegar a cada classe dependa apenas da classe atual. O contraexemplo mostra uma fibra que viola essa condição; nesse caso a dinâmica permanece no espaço original. O alias H-LUMP refere-se a H-QUOT(k); homogeneidade temporal é a hipótese separada H-HOM, alias de H-TIME-HOMOG.

### 8.2 Duplicação de texto

- `exact_repeat`: pares brutos=[[1, 2]]; pares canônicos=[[1, 2]]; teste=PASSA.
- `layout_only_repeat`: pares brutos=[]; pares canônicos=[[1, 2]]; teste=PASSA.
- `different_content_not_repeat`: pares brutos=[]; pares canônicos=[]; teste=PASSA.
- `a8_exact_four_reading_repeat`: A8=1; textos brutos distintos em 5–8=1/4; canônicos distintos=1/4; admissível contra duplicação=NÃO. Quatro repetições exatas satisfazem o predicado vetorial, mas não contam como quatro leituras textualmente independentes.
- `a8_layout_four_reading_repeat`: A8=1; textos brutos distintos em 5–8=4/4; canônicos distintos=1/4; admissível contra duplicação=NÃO. Mudanças de layout não ocultam duplicação canônica nas leituras 5–8.
- `a8_textually_distinct`: A8=1; textos brutos distintos em 5–8=4/4; canônicos distintos=4/4; admissível contra duplicação=SIM. Conteúdo estrangeiro distinto separa os hashes; isto só afasta duplicação, não prova independência estocástica nem atrator.

A8 aritmético e admissibilidade são campos separados. Quatro cópias podem produzir A8=1 e ainda assim ser bloqueadas pela porta de duplicação. Hashes não medem independência estocástica nem atrator.

## 9. O que melhorar antes da produção

- T: são necessárias pelo menos 2468 células perfeitas com zero erros para o limite CP 95% ficar abaixo do corte de 0,89; faltam 2348 células, equivalentes a pelo menos 98 novos casos completos independentes se todos forem 24/24.
- C1: são necessárias pelo menos 2468 células perfeitas com zero erros para o limite CP 95% ficar abaixo do corte de 0,89; faltam 2348 células, equivalentes a pelo menos 98 novos casos completos independentes se todos forem 24/24.
- C2: são necessárias pelo menos 2468 células perfeitas com zero erros para o limite CP 95% ficar abaixo do corte de 0,89; faltam 2348 células, equivalentes a pelo menos 98 novos casos completos independentes se todos forem 24/24.
- C3: são necessárias pelo menos 2468 células perfeitas com zero erros para o limite CP 95% ficar abaixo do corte de 0,89; faltam 2348 células, equivalentes a pelo menos 98 novos casos completos independentes se todos forem 24/24.
- C4: são necessárias pelo menos 2468 células perfeitas com zero erros para o limite CP 95% ficar abaixo do corte de 0,89; faltam 2348 células, equivalentes a pelo menos 98 novos casos completos independentes se todos forem 24/24.
- Não preencher esse número com clones: usar casos novos, independentemente revisados, com mutações e paráfrases representativas da distribuição de saída congelada. Se houver erro após correção, refazer a validação; não diluir o erro com cópias.
- Medir dependência entre erros de asserções/leituras. A fórmula `(1-e)^96` é otimista sob agrupamento; uma conta por clusters deve substituí-la se a independência for rejeitada.
- Congelar na R3 o formato estrito e a rejeição de prosa; se texto livre for exigido, ampliar o extrator por regras determinísticas e revalidar sensibilidade/especificidade, sem LLM-juiz.
- Manter as portas de conflito, truncamento, duplicação e lumpability no escopo de integridade; falha delas produz INCONCLUSIVE_CONTROLS, não evidência a favor ou contra a teoria.

## 10. Reprodução e manifesto

```bat
cd /d "C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K06\extratores"
python -B -X utf8 validar.py
```

Manifesto SHA-256: `4c5ddc355d3fe7183d121482c4c6289b439a4ceb73e86ba3db6d4149fec2ae17`. O manifesto contém os hashes e tamanhos dos oito insumos; não contém hash de si mesmo nem dos produtos que o citam, evitando referência circular. `resultados.json` contém todas as contagens e falhas sem truncamento.

**Conclusão:** a bateria estrita pode passar sem que o instrumento esteja pronto. Enquanto a incerteza estatística e a fronteira de prosa não forem resolvidas, o estado permanece BLOQUEADO_PARA_PRODUCAO.
