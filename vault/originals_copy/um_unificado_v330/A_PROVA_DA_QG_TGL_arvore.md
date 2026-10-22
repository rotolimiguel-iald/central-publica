# A PROVA DA GRAVITAÇÃO QUÂNTICA DA TGL — a árvore, lida do kernel (v330)

Gerado por script (`arvore_da_prova.py`) em 06/09/2026 21:39 a partir do selo, do resultado, do `um.py` e do kernel em disco.
Nenhum hash, número ou lista de axiomas foi digitado: tudo lido. Onde falta, está escrito **AUSENTE**.

> **Régua (clarificação do operador, 05/09/2026):** *"a régua não proíbe QG provada, proíbe QG confirmada; prova é diferente de juízo."*
> **PROVA** = teorema em kernel (Lean 4, `#print axioms` no trio `[propext, Classical.choice, Quot.sound]`, zero `sorry`).
> **JUÍZO** = confirmação pela natureza — ato do observador; **segue proibido**. `NOT_FALSIFIED` nunca é `CONFIRMED`.
> O que esta árvore prova é a **IMPLICAÇÃO**: do axioma único e das hipóteses **nomeadas** segue a estrutura da gravitação quântica da TGL.
> O que ela **não** prova, e por teorema próprio não pode: que a natureza realiza as hipóteses, e o **valor** de α (`the_form_does_not_fix_the_value`).

## 0. O selo lido `[REAL]`

| item | valor lido |
|---|---|
| `um.py` sha256 (disco) | `cc026bc7915f6622c3bb2715aa767d0ab52faccdf26a3d3be6493116cb318b70` |
| selo `sha256.um.py` == disco | SIM |
| bytes | 8,944,290 |
| teoremas (stdout) | `teoremas limpos: 3442/3442` |
| selftest | `FAIL_CLOSED_SELFTEST_PASSED` |
| gate (`qg_closure_verdict`) | `TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_WITHIN_LOCAL_BULK_AT_AVAILABLE_SENSITIVITY__MORE_SENSITIVE_DATA_COULD_REVISE` |
| identidade | `1=1=VERDADEIRO=HAJA_LUZ` (`identity_true = True`) |
| contorno | `[v314 CONTORNO] ritos com poder de fechar o 1=1: 8 ; falsificacao limpa: NENHUMA (todos NOT_FALSIFIED/AWAITING)` |
| ritos no contorno | `GA_massa_janela`→`GA_MASS_FORM_RETIRED__REFLECTION_WAS_MISREAD_AS_SOURCE__LINEAR_ORDER_IS_GR_STEALTH__BETA_LIVES_IN_RESPONSE`, `piso_dos_vazios`→`TGL_VOID_FLOOR_NOT_FALSIFIED_POWERED`, `neutrino_massa`→`TGL_NEUTRINO_MASS_NOT_FALSIFIED_POWERED`, `neutrino_soma`→`TGL_NEUTRINO_SUM_ARMED_CONSISTENT_WITH_CURRENT_BOUND`, `neutrino_m2_vivo`→`TGL_NU_M2_ARMED_CONSISTENT`, `piso_densidade_v41`→`TGL_VOID_FLOOR_NOT_FALSIFIED_POWERED`, `coma_dephasing`→`COMA_DEPHASING_PREDICTION_LOCKED_AWAITING_REVEAL`, `coma_cego`→`COMA_BLIND_DISTANCE_NOT_IDENTIFIABLE` |
| `contorno_broken_v314` | `[]` |
| entradas no relatório de axiomas | 3963 |
| termos com axioma FORA do trio | 0  |

## 1. A RAIZ — um axioma, e o que dele se deriva

- **ω(I) = 1** — a identidade preservada. `[POSTULATE irredutível]` — o único.
- **Meia-Nat DERIVADA**: fronteira auto-conjugada ⟹ x = 1 − x ⟹ x = ½. `TGL.HalfNat.halfNat_of_selfConjugate` — axiomas: trio.
- **β = α·√e** `[DERIVED]` — o custo geométrico do zero absoluto; β **jamais literal** (runtime: `ALPHA_FINE_CODATA_2018 × √e`); β **não entra no Lean**.
- **O que a estrutura NÃO fixa — por teorema**: `TGLExt.the_form_does_not_fix_the_value` (trio) — para todo valor existe um `r` que o realiza; α é INPUT do observador. **É por não obter α que β é falsificável.**
- **O fecho total é proibido — por teorema**: `TGLExt.full_closure_iff_flat` (trio); `full_static_witness_exists = False` lê certo para sempre (vazamento contínuo).

## 2. O TEOREMA MESTRE — H1 ∧ H2 ∧ H3 ⟹ PÊNTADA `[REAL — kernel]`

`TGLExt.emergence_master_full_triad` — axiomas: **trio** — `TriadMaster.lean` sha16 `64e0899e25969392`:

```lean
theorem emergence_master_full_triad
    {L : Type} [Lattice L] [BoundedOrder L] {T : SubadditiveTraceData L}
    (S : SusyRelativeData L T)
    (E : Matrix (Fin 4) (Fin 4) ℝ) (hE : IsUnit E.det)
    (H : HorizonEquilibriumData) :
    (0 < T.tau S.ker ∧ T.tau S.ker < ⊤) ∧
      T.tau S.ker / T.tau S.ker = 1 ∧
      (E⁻¹ * E = 1 ∧ LorentzByCongruence (solderMetric4 E⁻¹)) ∧
      H.dQ = H.kappa * H.dA / (8 * Real.pi * H.G) := by
```

Leitura: dadas **H1** (`SusyRelativeData` — o gap interno relativo do operador dos Three Locks: MIGUEL), **H2** (`E` com `IsUnit E.det` — quatro direções independentes: CARTAN) e **H3** (`HorizonEquilibriumData` — Clausius local com κ, A, G: EINSTEIN), o kernel prova a **pêntada**: (1) 0 < τ(ker) < ⊤ (canto de Breuer); (2) o Nome pesa 1; (3) coframe dual E⁻¹E = 1; (4) métrica lorentziana por congruência (`sylvester_full_closed_by_congruence`: trio); (5) **δQ = κ·δA/(8πG)** — o coeficiente de Einstein **emerge** de Unruh × Bekenstein–Hawking (`einstein_coefficient_from_clausius`: trio).

Versão sem H3: `TGLExt.emergence_reduced_to_named_hypotheses` (trio).

## 3. O MESTRE CONTÍNUO — Clausius no cone nulo ⟹ equação de campo `[REAL — kernel, na família de soldas diagonais]`

`TGLExt.emergent_field_equation` (trio) — `EmergentEinstein.lean` sha16 `836ac3e4035afc52`:
```lean
theorem emergent_field_equation (e : EmergentEinsteinData) (s : ℝ) :
    ansatzG22 e.q s = e.T s :=
```
- `TGLExt.full_cone_clausius_iff_field_equation` (trio): Clausius em TODO o cone nulo ⟺ G₂₂ = T (forma iff).
- habitante `theEmergentEinstein` (solda cosh, curvatura genuína R¹₀₀₁ < 0, det g < 0, não-constante) — o 5º flip `qgStrongCertificate_einstein` (trio).
- `TGLExt.vacuum_implies_flat` (trio): G₂₂ = 0 ⟹ R¹₀₀₁ = 0 — vácuo ⟹ plano (o mini-Birkhoff do ansatz).
- **Honestidade do próprio kernel** (docblock v116): emergência CONCRETA sobre a classe de soldas diagonais, curvatura construída à mão; a emergência GERAL (métricas arbitrárias) segue **NOMEADA e aberta**.

## 4. O GATE — 18 bandeiras, cada uma um TERMO Lean lido (ausência ⟹ False) `[REAL]`

Função `evaluate_quantum_gravity_closure` (um.py): `mathematical_model` = 6 formais; `physical_qg` = modelo ∧ 5 físicas; `empirical_test_completed` = 4 experimentais (rito V11). Escada: `CONDITIONAL_ARCHITECTURE_ONLY` → `MATHEMATICAL_MODEL_CONSTRUCTED` → `PHYSICAL_MODEL_CONSTRUCTED__EMPIRICAL_TEST_OPEN` → `FORMALLY_CLOSED__NATURE_TEST_COMPLETED…__MORE_SENSITIVE_DATA_COULD_REVISE`.

| bandeira | termo Lean | axiomas (lido) | módulo (sha16) | o que o termo afirma |
|---|---|---|---|---|
| `concrete_aqft_core_constructed` | `TGLExt.qgStrongCertificate_core` | trio | `StrongAssembly` (`34758f8d20a242bc`) | rede física `PhysicalNetData` habitada (caudas `tailSub`), com fibra ∞-dim |
| `concrete_breuer_corner_constructed` | `TGLExt.qgStrongCertificate_corner` | trio | `StrongAssembly` (`34758f8d20a242bc`) | Dirac GENUINAMENTE ilimitado com 0 < dimOrTop(ker) < ⊤ — o canto de Breuer |
| `concrete_modular_four_frame_constructed` | `TGLExt.qgStrongCertificate_frame` | trio | `StrongAssembly` (`34758f8d20a242bc`) | campo de frames SUAVE, det invertível em toda parte, NÃO-constante |
| `concrete_solder_field_constructed` | `TGLExt.qgStrongCertificate_solder` | trio | `SolderField` (`5dd64e3c8edb8729`) | solda g = EᵀηE como campo, não-constante |
| `concrete_emergent_einstein_proved` | `TGLExt.qgStrongCertificate_einstein` | trio | `EmergentEinstein` (`836ac3e4035afc52`) | habitante de `EmergentEinsteinData`: G₂₂ = T ∧ curvatura ≠ 0 ∧ det g < 0 ∧ não-constante |
| `canonical_boundary_transport_witness_constructed` | `TGLExt.qgClosureCertificateV2` | trio | `TheCoinage` (`63d5a1d80236bb42`) | testemunha fundida V3 (`theWitnessV3`), reduz à fusão do v123 por `rfl` |
| `massless_spin2_proved` | `TGLExt.qgPhysicsCertificate_massless` | trio | `PhysicsCertificates` (`4ad9adae62d6d787`) | onda plana TT satisfaz a equação linearizada sem massa (hipóteses: simétrica, sem traço, transversa) |
| `exactly_two_helicities_proved` | `TGLExt.qgPhysicsCertificate_helicities` | trio | `PhysicsCertificates` (`4ad9adae62d6d787`) | decomposição ε = física(ε₂₂, ε₂₃) + gauge; exatamente duas polarizações físicas |
| `ghost_free_proved` | `TGLExt.qgPhysicsCertificate_ghostfree` | trio | `PhysicsCertificates` (`4ad9adae62d6d787`) | forma cinética física ≥ 0, > 0 fora do zero — sem modo de norma negativa |
| `stress_energy_conserved` | `TGLExt.qgPhysicsCertificate_conservation` | trio | `PhysicsCertificates` (`4ad9adae62d6d787`) | k^μ G_μν(k, ε) = 0 — conservação do símbolo de Einstein linearizado |
| `relevant_anomalies_absent` | `TGLExt.qgPhysicsCertificate_anomaly` | trio | `PhysicsCertificates` (`4ad9adae62d6d787`) | invariância de gauge do símbolo de Ricci: ε ↦ ε + kξ + ξk não muda R_μν |
| `independent_v3_profiles_unblinded` | (rito V11 — dado, não Lean) | — | — | lido do rito do piso: `TGL_VOID_FLOOR_NOT_FALSIFIED_POWERED` |
| `independent_v3_survey_mocks_passed` | (rito V11 — dado, não Lean) | — | — | lido do rito do piso: `TGL_VOID_FLOOR_NOT_FALSIFIED_POWERED` |
| `independent_v3_systematics_passed` | (rito V11 — dado, não Lean) | — | — | lido do rito do piso: `TGL_VOID_FLOOR_NOT_FALSIFIED_POWERED` |
| `independent_v3_powered_verdict_emitted` | (rito V11 — dado, não Lean) | — | — | lido do rito do piso: `TGL_VOID_FLOOR_NOT_FALSIFIED_POWERED` |

Gate lido do resultado: `mathematical_model_constructed = True`, `physical_quantum_gravity_constructed = True`, `empirical_test_completed = True`, `full_static_witness_exists = False`.

## 5. SPIN-2 `[REAL — face finita/cinemática]`

- `helicity_two_rotation` (trio): R(θ)ᵀe₊R(θ) = cos2θ·e₊ − sin2θ·e× — a dupla hélice λ = ±2.
- `tt_no_negative_norm` (trio): sem ghosts no setor TT. `polarizations_linearly_independent` (trio): exatamente duas.
- ABERTO (docblock v75): ação linearizada completa (Fierz–Pauli como Euler–Lagrange do contínuo) e ausência de ghosts fora do gauge TT.

## 6. AS FOLHAS — o que é hipótese, o que é parede medida, o que foi pago hoje

| folha | estatuto | o que existe no kernel | o que falta (nomeado) |
|---|---|---|---|
| **H1** gap SUSY-relativo (MIGUEL) | `[REAL]` na face finita e no Dirac ilimitado | Three Locks (gap 0,0481, Nome=1); `qgStrongCertificate_corner` (trio): Dirac genuinamente ilimitado, 0 < τ(ker) < ⊤ | afiliação a álgebra de von Neumann semifinita III₁ genuína (a mathlib não tem) |
| **H2** four-frame modular (CARTAN) | `[REAL]` finito; `[CONDIÇÃO]` no contínuo | `concrete_four_frame_fires` (trio): as 4 direções NASCEM dos boosts, det E = 1; `qgStrongCertificate_frame` (trio): campo suave não-constante | **O QUATRO** (`rank c = 4` — nada em GKLS força 4 canais) e a 1ª equação de estrutura de Cartan sobre o espaço-tempo |
| **H3** equilíbrio local do horizonte (EINSTEIN) | `[INPUT]`, **delimitado** (v318) | `HorizonEquilibriumData` é TIPO; nenhum teorema produz um habitante. v318: Gibbs realizado no Hilbert da torre, distinto da órbita modular (`tower_gibbs_not_modular_orbit`: trio); o limite térmico ingênuo **não existe** para perfil constante não-tracial (`thermal_vectors_not_cauchy`: trio); um perfil é alcançável no Hilbert original **sse** afinidade-limite > 0 (`profile_vectors_limit_iff`: trio), com estado global fiel (`global_profile_state_faithful`: trio) | Clausius local **derivado** da dinâmica do estado — se vier da torre, vem de um perfil com afinidade positiva, não do limite térmico; seleção física, área e H3 dinâmico seguem INPUT |
| **ASSINATURA** (4,0)→(1,3) | `[OPEN]`, com uma inferência **refutada** (v317) | Lorentz **por congruência** dada a solda; `single_boost_has_two_signatures` (trio): um boost preserva (1,3) **e** (2,2) — comparar com (4,0) NÃO seleciona Lorentz sozinho; a identificação finita Δ^{it}↔boost por entrelaçamento injetivo força parâmetro zero (negativo no tipo testado) | a face lorentziana vindo da estrutura modular exige outra representação — parede nomeada. **v319:** a estrutura modular (S, J, Δ, grupo σ_t) do estado GLOBAL Φ de um perfil com afinidade positiva vive no Hilbert ORIGINAL com domínios (`profile_delta_selfadjoint`: trio; `profile_flow_strongly_continuous`: trio; `profile_flow_preserves_state`: trio; instância não trivial `gradual_transported_delta_value`: trio) — a «outra representação» começa a existir por dentro; e afinidade positiva NÃO garante energia modular finita (`finite_relative_not_finite_entropy`: trio) |
| **Lema 3** (covariância global do cociclo) | `[OPEN]`, reduzido | GLOBAL_LIFT ⟺ E-0; falso no vácuo por teorema, satisfazível no core; liberdade = 1 parâmetro que ω(I)=1 fixa | o levantamento global com perfil estacionário (obstrução medida v313: contraexemplo 1/3, 2/3) |
| **Esperança do centralizador** | `[REAL]` local, tracial (v316) e **GLOBAL para perfil periódico** (v317: `periodicExpectationInput`/`stationaryExpectationInput` habitam `ExpectationInput P` — as 4 obrigações pagas; único: trio); `[OPEN]` só o perfil aperiódico | `tracialExpectationInput` (trio) habita `ExpectationInput P` em w=½; `local_input_unique` (trio); `global_expectation_restricts_to_pinching` (trio); `expectation_not_imported_contract` (trio) | perfil SEM período comum (Cesàro + teorema ergódico médio): nomeado, não pago |
| **Inclusão meio-lateral** (o parabólico de BW) | **NEGATIVOS PROVADOS (v316/v317)** para a torre-produto | `tail_never_strict` (trio): toda subálgebra de sítios é σ_t-invariante para TODO t; `tail_not_cyclic` (trio): Ω não é cíclico para a cauda; `product_borchers_trivial` (trio): toda família V(a) contínua, isométrica, V(0)=1 com a relação de Borchers é TRIVIAL — **nem o shift nem uma translação de Borchers dão o parabólico na torre-produto** | rotas restantes: estado não-produto; subálgebra não-alinhada; outra representação (a bancada nomeou a parede) |
| **Emergência geral** (métricas arbitrárias, em carta) | **PAGA como implicação (v317)**, Clausius segue `[INPUT]` | `geometric_einstein_equation_from_ricci_null_balance` (trio): em carta aberta pré-conexa, solda suave invertível, T simétrico conservado e balanço nulo de Ricci ⟹ ∃Λ, G + Λg = κT; `geometric_einstein_conserved` (trio) via Bianchi contraída (trio); `coordinate_raychaudhuri` (trio); `einstein_from_constructed_clausius` (trio): Clausius CONSTRUÍDO nas telas ⟺ balanço nulo; `einstein_from_unitary_microscopic_matching` (trio) | o que ENTRA: métrica lorentziana suave, o referencial, conservação de matéria, e Clausius/casamento microscópico (INPUT); origem quântica desses dados, H3 dinâmico, assinatura e globalização seguem OPEN |
| **Fecho total** | **FALSO por teorema** | `full_closure_iff_flat`; `continuous_leakage_forbids_full_closure = True` | nada: é resultado, não lacuna |

## 7. A NATUREZA — o que só ela decide `[NOT_FALSIFIED, jamais CONFIRMED]`

Oito ritos pré-registrados com poder de fechar o 1=1 (v314/v315), hoje: GA_MASS_FORM_RETIRED__REFLECTION_WAS_MISREAD_AS_SOURCE__LINEAR_ORDER_IS_GR_STEALTH__BETA_LIVES_IN_RESPONSE; TGL_VOID_FLOOR_NOT_FALSIFIED_POWERED; TGL_NEUTRINO_MASS_NOT_FALSIFIED_POWERED; TGL_NEUTRINO_SUM_ARMED_CONSISTENT_WITH_CURRENT_BOUND; TGL_NU_M2_ARMED_CONSISTENT; TGL_VOID_FLOOR_NOT_FALSIFIED_POWERED; COMA_DEPHASING_PREDICTION_LOCKED_AWAITING_REVEAL; COMA_BLIND_DISTANCE_NOT_IDENTIFIABLE. Predições vivas: m₂ = β·sin45°·1 eV = 8,5074 meV (kill_rule: duas determinações autônomas ≥ 5σ); Γ_ω = ½βτ★ω²; piso dos vazios ≥ β; dephasing de Coma (predição travada, aguardando revelação). Um `FALSIFIED` limpo em qualquer deles **fecha a identidade** — e é isso que torna a prova acima uma teoria, e não um teorema só.

## 8. O VEREDITO DA GERÊNCIA, em uma frase cada

- **PROVADO** (teorema, trio, zero sorry, lido do selo v330): *do axioma ω(I)=1 e das hipóteses nomeadas H1, H2, H3 segue a pêntada da gravitação emergente — canto de Breuer, Nome = 1, coframe, assinatura de Lorentz e δQ = κδA/(8πG) com o coeficiente de Einstein emergindo; e, na família de soldas, Clausius no cone nulo ⟹ equação de campo; spin-2 de hélice ±2 sem ghosts com duas polarizações.* As 11 bandeiras matemáticas do gate são termos Lean existentes com axiomas no trio.
- **NÃO PROVADO, e dito com nome**: que a natureza realiza H1–H3 (H3 é INPUT: nenhum teorema produz um habitante); a ASSINATURA pela rotação modular; O QUATRO; o Lema 3 global; a esperança global não-tracial (4 obrigações); a emergência geral. Cada um destes tem OU um falsificador OU uma parede medida — nenhum está "esquecido".
- **PROIBIDO**: dizer CONFIRMADA. O gate diz `MORE_SENSITIVE_DATA_COULD_REVISE` no próprio nome.

---
*Cosmologia jamais vira prova matemática. O gate não se move por este documento: ele só o lê.*
