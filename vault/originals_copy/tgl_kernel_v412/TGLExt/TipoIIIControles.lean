import TGLExt.Classificacao
import TGLExt.ObserverClassification
import TGLExt.F1Fecho394.RegularCoreFixedR3
import TGLExt.O16.ContentContractProposal

set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section

/-!
# O critério do núcleo para a luz na cunha: controles, alcance e o que o nome NÃO diz
## A letra que o arquivo tipa

O que se quer conhecer pelo nome é: a luz testemunhada na cunha (porque é o Nome), a construção da Torre (porque é o
índice), a fronteira do horizonte (porque é a borda) e o vínculo entre elas, que é a relatividade. A luz é o sujeito e os
outros três são papéis. O arquivo trata do predicado `Vinculo.IsTypeIII1` e do teorema
`Vinculo.maxwell_right_wedge_type_III1`, dos módulos de que depende. Cinco dos teoremas daqui são reexportações de
teoremas desses módulos, em sentido amplo: contam também a projeção de um teorema e a reescrita imediata por uma igualdade.

## O que o predicado diz, e o que o nome dele NÃO diz

`IsTypeIII1 A` exige: (1) o centro de `A` é escalar; (2) há um vetor unitário cíclico e separador; (3) há um fluxo
unitário que é o do grafo fechado de Tomita desse vetor (campo `PairTomitaAnalyticRealizationMeasured`); (4) o fluxo
preserva `A`; (5) o núcleo `core B A` (o produto cruzado concreto por esse fluxo, em `L²(ℝ; H)`) tem centro escalar.

Isto é o CRITÉRIO DO NÚCLEO (o fluxo dos pesos é trivial). Que uma álgebra que o cumpre seja de tipo III₁ no sentido
de Connes (o invariante `S(M)` igual à semirreta) é teorema da literatura [KNOWN: Connes–Takesaki 1977; Takesaki
1973], citado e NÃO formalizado aqui nem no kernel. O identificador `IsTypeIII1` diz, portanto, mais do que o termo
prova; o mesmo risco aparece em `TheMarkIsNotATypeMark` (a marca que não era marca de tipo). Este
arquivo não renomeia nada.

## O que este arquivo acrescenta (tudo com termo, sem `sorry`, sem axioma além do trio)

1. **O relógio e a conjugação não têm escolha, dado o vetor.** Duas realizações para a mesma álgebra e o mesmo
   vetor têm o mesmo fluxo e a mesma conjugação (`o_fluxo_e_a_conjugacao_de_tomita_sao_unicos`). NÃO é fato novo: é
   corolário do reconhecimento pelo conteúdo que o kernel já tinha
   (`ORDEM016.D6.same_horizon_by_content_from_realizations`). O que o predicado deixa livre é só o vetor; com outra testemunha o relógio pode ser outro (a unicidade está provada para o
   mesmo vetor; a recíproca não).
2. **O predicado recusa, por teorema, o que não é do critério:** a álgebra que contém os operadores de posto um em
   dimensão ≥ 2 (não tem vetor separador); a álgebra com um elemento central não escalar, em particular a abeliana
   não escalar (falha o centro); a álgebra dos escalares, a única sobre `H = ℂ` (o núcleo não é fator); e todo fluxo
   que age por escalar no tempo 1, em particular o fluxo parado (o núcleo não é fator). NÃO há recusa por termo para
   os tipos I_n com n ≥ 2 e I_∞ em forma padrão, II₁, II∞, III₀ e III_λ com λ < 1: essa recusa é da literatura [não
   aberta no primário].
3. **A cunha, peça por peça:** o centro da álgebra da cunha é escalar; o centro do núcleo dela é escalar; o fluxo do
   critério na cunha é o boost, sem escolha; a unicidade não é vazia (`ha_realizacao_na_cunha`); o boost não age por
   escalar no tempo 1 (`o_boost_nao_age_por_escalar_no_tempo_um`). E as DUAS marcas ficam lado a lado neste arquivo: a
   do estado, que já era do kernel (`marca_do_estado_no_certificado_fisico`: o que o relógio da cunha deixa parado é
   múltiplo do Um; escrita também com a MESMA álgebra `net rightWedge` e o MESMO relógio `fockFlow` do critério em
   `marca_do_estado_na_lingua_do_criterio`, pelas igualdades do kernel `physical_net` e `flow_is_Ad`), e a do núcleo,
   (`a_luz_na_cunha_cumpre_o_criterio_do_nucleo`); a cunha de todo
   observador cumpre o mesmo critério (`a_cunha_de_todo_observador_cumpre_o_criterio_do_nucleo`).
4. **O vínculo como dependência, não só como conjunção:** o fluxo que lê os números da Torre na cunha é o MESMO
   fluxo cujo núcleo é fator (`o_fluxo_da_leitura_e_o_do_criterio`; é identidade por construção, porque o
   certificado físico foi montado com o mesmo boost, não fato novo); a leitura da Torre reescrita com o fluxo do
   critério (`a_torre_e_lida_pelo_fluxo_do_criterio`).
5. **A Torre dá os números; a leitura vale para todo número** (`a_leitura_vale_para_todo_real`): a Torre entra como
   índice (o logaritmo da razão dos pesos), não como parte da cunha. O negativo
   (`K07.TowerWedge.physical_no_flow_intertwining_embedding`: não há injeção unital da Torre na cunha que entrelace
   os fluxos) é a outra metade, e vale só mantendo os relógios e só no sentido da Torre para a cunha. Sem os
   relógios, a literatura diz que as duas são a mesma álgebra [KNOWN, não conferido aqui no primário; não é termo].
   Os números da Torre vêm de um perfil escolhido à mão.
6. **A borda determina a transformação afim, ponto a ponto** (`a_borda_determina_a_transformacao_afim`): duas
   transformações afins que coincidem em CADA ponto da borda da cunha são iguais. Como lugar, a borda não basta:
   todo boost da cunha é um observador que leva a borda nela mesma
   (`todo_boost_da_cunha_leva_a_borda_nela_mesma`), e boosts de parâmetros diferentes são observadores diferentes
   (`boosts_de_parametros_diferentes_sao_diferentes`): uma família a um parâmetro de observadores distintos com a
   mesma borda. (`a_borda_como_conjunto_nao_determina` só afirma que existe um, diferente da identidade.) “Afim” é
   classe MAIS LARGA que a relatividade
   (contém as transformações de Lorentz com translação, e também as de Galileu e as dilatações); o teorema não usa
   a métrica. A face da relatividade é o corolário `dois_observadores_iguais_na_borda_sao_o_mesmo`. O controle do
   cisalhamento mostra a metade “sem a regra afim”; aqui as duas se fecham: o cisalhamento não é afim
   (`o_cisalhamento_nao_e_afim`).

## O que NÃO se afirma

* Que o kernel prove o tipo III₁ de Connes: prova o critério do núcleo para a cunha de Maxwell.
* Nada sobre o horizonte de um espaço-tempo curvo [OPEN], nem sobre a fronteira da TGL.
* Nada sobre o item aberto do κ (`TGLExt/TheScaleHasNoFixedPoint.lean`, [OPEN]). O kernel toma o κ finito e
  positivo como dado e deixa aberto ONDE ele mora: numa face finita (e então não toca o tipo) ou em tensão com o tipo
  III₁ que a casa declara para a fronteira. A cunha cumprir o critério não decide isso.
* Que o núcleo do kernel seja, por termo, o produto cruzado dos matemáticos: é a álgebra gerada pela cópia da
  álgebra e pelos unitários regulares, igual a ele a menos de um unitário; essa identificação é sabida e não é
  termo.
* HOMÔNIMOS: “núcleo” aqui é a álgebra com o seu relógio junto (não é o núcleo de K, nem o verbo que é o núcleo de
  um tipo penal); “relógio” aqui é o do vácuo na cunha (não é o do pedágio).
* Que a borda seja "o espectro de leitura": o que há é geometria de pontos e a unicidade afim. A leitura é da teoria, não termo.
* Que a Torre seja o sujeito: o sujeito, pela leitura da teoria, é a luz testemunhada na cunha.

## Estatutos

`[REAL no sandbox]` os termos deste arquivo · `[DECLARADO]` os módulos de que o arquivo depende (o predicado e a
classificação da cunha) · `[KNOWN]` a identificação do critério com o tipo III₁ de Connes · `[ONTO/INPUT]` os quatro
papéis (sujeito, índice, contraste, vínculo), que são a letra da teoria. Validade no kernel não é creditação; o
gate não se move.
-/

namespace Vinculo.Controles

open TGLV350.Regular ORDEM016.D6 Vinculo F1Fecho.RegularCovariantCore MeasureTheory
open scoped InnerProductSpace

section abstrato

variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-! ## 1. O relógio não tem escolha -/

/-- **O relógio e a conjugação não têm escolha, dado o vetor.** Duas realizações para a mesma álgebra e o mesmo
vetor, com conjugações quaisquer, têm o mesmo fluxo e a mesma conjugação. Corolário do reconhecimento pelo conteúdo
do kernel (`ORDEM016.D6.same_horizon_by_content_from_realizations`, com o reconhecimento identidade). -/
theorem o_fluxo_e_a_conjugacao_de_tomita_sao_unicos {M : StarSubalgebra ℂ (H →L[ℂ] H)} {omega : H}
    {J1 J2 : H ≃ₛₗᵢ[starRingEnd ℂ] H} {f1 f2 : ℝ → H ≃ₗᵢ[ℂ] H}
    (h1 : PairTomitaAnalyticRealizationMeasured M omega J1 f1)
    (h2 : PairTomitaAnalyticRealizationMeasured M omega J2 f2) : f1 = f2 ∧ J1 = J2 := by
  have h := same_horizon_by_content_from_realizations (identityByConstruction M omega)
    J1 J2 f1 f2 h1 h2
  constructor
  · funext t
    apply LinearIsometryEquiv.ext
    intro x
    exact h.2 t x
  · apply LinearIsometryEquiv.ext
    intro x
    exact h.1 x

/-- O mesmo, para duas testemunhas do predicado com o mesmo vetor. -/
theorem o_fluxo_do_criterio_e_unico (A : VonNeumannAlgebra H) (Ω : H)
    (J1 J2 : H ≃ₛₗᵢ[starRingEnd ℂ] H) (B1 B2 : UnitaryFlow H)
    (h1 : PairTomitaAnalyticRealizationMeasured A.toStarSubalgebra Ω J1 B1.U)
    (h2 : PairTomitaAnalyticRealizationMeasured A.toStarSubalgebra Ω J2 B2.U) :
    B1.U = B2.U ∧ J1 = J2 :=
  o_fluxo_e_a_conjugacao_de_tomita_sao_unicos h1 h2

/-! ## 2. O predicado recusa o que não é do critério -/

/-- Uma álgebra que contém os operadores de posto um, em dimensão ≥ 2, não tem vetor separador: não cumpre o
critério. (Cobre `B(H)` e as matrizes na representação de origem.) -/
theorem quem_contem_os_postos_um_nao_cumpre (A : VonNeumannAlgebra H)
    (hrank : ∀ η : H, (innerSL ℂ η).smulRight η ∈ A)
    (hdim : ∀ Ω : H, ∃ η : H, η ≠ 0 ∧ inner ℂ η Ω = (0 : ℂ)) : ¬ IsTypeIII1 A := by
  rintro ⟨-, Ω, J, B, hn, -, hsep, -, -, -⟩
  obtain ⟨η, hη0, hηΩ⟩ := hdim Ω
  have h0 := hsep _ (hrank η) (by
    simp [ContinuousLinearMap.smulRight_apply, innerSL_apply_apply, hηΩ])
  have h1 := congrArg (fun T : H →L[ℂ] H => T η) h0
  simp [ContinuousLinearMap.smulRight_apply, innerSL_apply_apply] at h1
  exact hη0 h1

/-- Uma álgebra com um elemento central não escalar (em particular a abeliana não escalar) falha a primeira
cláusula. -/
theorem a_abeliana_nao_escalar_nao_cumpre (A : VonNeumannAlgebra H) (z : H →L[ℂ] H) (hz : z ∈ A)
    (hab : ∀ a ∈ A, a * z = z * a) (hns : ∀ c : ℂ, z ≠ c • (1 : H →L[ℂ] H)) :
    ¬ IsTypeIII1 A := by
  intro h
  obtain ⟨c, hc⟩ := h.1 z hz ((VonNeumannAlgebra.mem_commutant_iff).mpr hab)
  exact hns c hc

/-- A translação por 1 em `L²(ℝ; H)` não é escalar, se `H` não é nulo. -/
theorem o_deslocamento_nao_e_escalar (hH : ∃ v : H, v ≠ 0) :
    ¬ ∃ c : ℂ, (shift (H := H) 1) = c • (1 : RegularHilbert H →L[ℂ] RegularHilbert H) := by
  rintro ⟨c, hc⟩
  obtain ⟨v, hv⟩ := hH
  have hs : MeasurableSet (Set.Ioc (0:ℝ) 1) := measurableSet_Ioc
  have hμ : (volume : Measure ℝ) (Set.Ioc (0:ℝ) 1) ≠ ⊤ := by simp
  let f : RegularHilbert H := indicatorConstLp 2 hs hμ v
  have hff : inner ℂ f f = ((‖v‖^2 : ℝ) : ℂ) := by
    have := L2.inner_indicatorConstLp_indicatorConstLp (𝕜 := ℂ) hs hs hμ hμ v v
    rw [this]
    simp [Set.inter_self, inner_self_eq_norm_sq_to_K]
  have hf0 : f ≠ 0 := by
    intro h0
    rw [h0, inner_zero_left] at hff
    have : ‖v‖^2 = 0 := by exact_mod_cast hff.symm
    exact hv (norm_eq_zero.mp (pow_eq_zero_iff (two_ne_zero) |>.mp this))
  have hs' : MeasurableSet ((fun x : ℝ => x - 1) ⁻¹' Set.Ioc (0:ℝ) 1) :=
    hs.preimage (measurable_sub_const (1:ℝ))
  have hμ' : (volume : Measure ℝ) ((fun x : ℝ => x - 1) ⁻¹' Set.Ioc (0:ℝ) 1) ≠ ⊤ := by
    rwa [(measurePreserving_sub_right (volume : Measure ℝ) (1:ℝ)).measure_preimage
      hs.nullMeasurableSet]
  have hshift : shift (H := H) 1 f = indicatorConstLp 2 hs' hμ' v :=
    Lp.indicatorConstLp_compMeasurePreserving hs hμ v
      (measurePreserving_sub_right (volume : Measure ℝ) (1:ℝ))
  have hort : inner ℂ f (shift (H := H) 1 f) = 0 := by
    rw [hshift]
    have := L2.inner_indicatorConstLp_indicatorConstLp (𝕜 := ℂ) hs hs' hμ hμ' v v
    rw [this]
    have hemp : Set.Ioc (0:ℝ) 1 ∩ (fun x : ℝ => x - 1) ⁻¹' Set.Ioc (0:ℝ) 1 = ∅ := by
      ext x
      simp only [Set.mem_inter_iff, Set.mem_Ioc, Set.mem_preimage, Set.mem_empty_iff_false,
        iff_false]
      rintro ⟨⟨_, h1⟩, ⟨h2, _⟩⟩
      linarith
    rw [hemp]
    simp
  rw [hc] at hort
  simp only [smul_apply, one_apply_eq_self, inner_smul_right,
    hff] at hort
  have hnorm : ‖v‖ ^ 2 ≠ 0 := pow_ne_zero 2 (norm_ne_zero_iff.mpr hv)
  have : c = 0 := by
    have h2 : (((‖v‖^2 : ℝ) : ℂ)) ≠ 0 := by exact_mod_cast hnorm
    exact (mul_eq_zero.mp hort).resolve_right h2
  subst this
  have := shift_norm (H := H) 1 f
  rw [hc] at this
  simp at this
  exact hf0 (norm_eq_zero.mp this.symm)

/-- ★ Se o fluxo age por um escalar no tempo 1, o núcleo NÃO é fator, seja qual for a álgebra. -/
theorem fluxo_escalar_no_tempo_um_o_nucleo_nao_e_fator (A : VonNeumannAlgebra H) (B : UnitaryFlow H)
    (hH : ∃ v : H, v ≠ 0) (c : ℂ) (hB : boostCLM B 1 = c • (1 : H →L[ℂ] H)) :
    ¬ HasScalarCenter (core B A) := by
  intro h
  obtain ⟨v, hv⟩ := hH
  have hc : c ≠ 0 := by
    intro h0
    have := (boostIso B 1).norm_map v
    have e : boostIso B 1 v = c • v := congrArg (fun T : H →L[ℂ] H => T v) hB
    rw [e, h0, zero_smul, norm_zero] at this
    exact hv (norm_eq_zero.mp this.symm)
  have hV : F1Fecho.RegularCovariantCore.regularUnitary B 1 = c • shift (H := H) 1 := by
    unfold F1Fecho.RegularCovariantCore.regularUnitary
    rw [hB, fibre_smul, fibre_one]
    simp
  have hmem : shift (H := H) 1 ∈ core B A := by
    have h1 := regular_mem B A 1
    have : shift (H := H) 1 = c⁻¹ • F1Fecho.RegularCovariantCore.regularUnitary B 1 := by
      rw [hV, smul_smul, inv_mul_cancel₀ hc, one_smul]
    rw [this]
    exact (core B A).toStarSubalgebra.smul_mem h1 _
  have hcomm : shift (H := H) 1 ∈ (core B A).commutant :=
    F1Fecho.RegularCoreFixed.shift_mem_regularCommutant B A 1
  exact o_deslocamento_nao_e_escalar ⟨v, hv⟩ (h _ hmem hcomm)

/-- O fluxo parado não dá núcleo fator. -/
theorem o_fluxo_parado_nao_da_nucleo_fator (A : VonNeumannAlgebra H) (B : UnitaryFlow H)
    (hH : ∃ v : H, v ≠ 0) (hB : ∀ t, B.U t = LinearIsometryEquiv.refl ℂ H) :
    ¬ HasScalarCenter (core B A) := by
  refine fluxo_escalar_no_tempo_um_o_nucleo_nao_e_fator A B hH 1 ?_
  rw [one_smul]
  apply ContinuousLinearMap.ext
  intro x
  change B.U 1 x = x
  rw [hB 1]; rfl

end abstrato

/-- Sobre `H = ℂ`, todo fluxo age por escalar: o núcleo de qualquer álgebra não é fator. -/
theorem sobre_a_reta_complexa_o_nucleo_nao_e_fator (A : VonNeumannAlgebra ℂ) (B : UnitaryFlow ℂ) :
    ¬ HasScalarCenter (core B A) := by
  refine fluxo_escalar_no_tempo_um_o_nucleo_nao_e_fator A B ⟨1, one_ne_zero⟩ ((boostCLM B 1) 1) ?_
  apply ContinuousLinearMap.ext
  intro x
  have : x = x • (1 : ℂ) := by simp
  rw [this, map_smul]
  simp [mul_comm]

/-- ★ A álgebra dos escalares, a única sobre `H = ℂ`, não cumpre o critério. -/
theorem sobre_a_reta_complexa_ninguem_cumpre (A : VonNeumannAlgebra ℂ) : ¬ IsTypeIII1 A := by
  rintro ⟨-, Ω, J, B, -, -, -, -, -, hc⟩
  exact sobre_a_reta_complexa_o_nucleo_nao_e_fator A B hc

/-! ## 3. A cunha, peça por peça -/

section cunha

open TGL.SpecificAQFT F1Rede.BosonicFock TGLExt.ImportedSQ
open F1Fecho.CanonicalFockRegular F1Fecho.PhysicalFockNet
open F1Fecho.OrbitalSpatial F1Fecho.SpacetimeLorentz F1Fecho.MaxwellLocalization K07.Horizon
open F1Fecho.Antilinear ChatgptAudit TGLExt
open F1Fecho.CanonicalFockModularCoreInputR1 (physicalFockCertificate)
open K07.TowerWedge TGLExt.ContratoQGv31

/-- A álgebra da luz na cunha cumpre o CRITÉRIO DO NÚCLEO (o teorema `maxwell_right_wedge_type_III1`, reexportado com o aviso: o
identificador `IsTypeIII1` nomeia o critério; a identificação com o tipo III₁ de Connes é citada, não provada). -/
theorem a_luz_na_cunha_cumpre_o_criterio_do_nucleo : IsTypeIII1 (net rightWedge) :=
  maxwell_right_wedge_type_III1

/-- O centro da álgebra da cunha é escalar (a álgebra é uma peça só). -/
theorem o_centro_da_cunha_e_escalar : HasScalarCenter (net rightWedge) :=
  maxwell_right_wedge_type_III1.1

/-- O centro do núcleo da cunha, pelo boost, é escalar (o núcleo é uma peça só). -/
theorem o_centro_do_nucleo_da_cunha_e_escalar : HasScalarCenter (core fockFlow (net rightWedge)) := by
  have hid : net rightWedge = M := net_wedge_eq
  rw [hid]
  exact K07.PhysicalCoreCenter.physical_core_is_factor

/-- Na cunha, com o vácuo por testemunha, o fluxo do critério é o boost e a conjugação é a canônica, sem escolha:
toda realização para a álgebra da cunha e o vácuo tem esse fluxo e essa conjugação. -/
theorem na_cunha_o_fluxo_do_criterio_e_o_boost (B : UnitaryFlow F) (J : F ≃ₛₗᵢ[starRingEnd ℂ] F)
    (h : PairTomitaAnalyticRealizationMeasured (net rightWedge).toStarSubalgebra vacuum J B.U) :
    B.U = fockFlow.U ∧ J = canonicalFockJ :=
  o_fluxo_e_a_conjugacao_de_tomita_sao_unicos h pair_tomita

/-! ## 4. O vínculo como dependência: o fluxo que lê é o fluxo cujo núcleo é fator -/

/-- ★ O fluxo com que a cunha é lida (`lightDelta`) é o fluxo do critério (`fockFlow`). -/
theorem o_fluxo_da_leitura_e_o_do_criterio (t : ℝ) :
    lightDelta physicalFockCertificate t = fockFlow.U t := rfl

/-- ★ A leitura da Torre, escrita com o fluxo do critério: a unidade `(i, j)` do nível `N`, de razão de pesos
`λ`, é lida no tempo modular `t = −log λ / 2π` do MESMO fluxo cujo núcleo é fator, e leva a translação nula de
passo `l` à de passo `λ·l`. -/
theorem a_torre_e_lida_pelo_fluxo_do_criterio (N : ℕ) (i j : chainIdx N) (l : ℝ) :
    (fockFlow.U (modularTime (rapidity mixProfile N i j))).conjStarAlgEquiv
        ((lightNet physicalFockCertificate).U (l • nullDir)) =
      (lightNet physicalFockCertificate).U ((localEigenvalue mixProfile N i j * l) • nullDir) :=
  (tower_observer_diagram N i j).2.1 l

/-! ## 5. A Torre dá os números; a leitura vale para todo número -/

variable {L : LightOneParticle} (C : FockCertificate L)

/-- A leitura por boost vale para TODO real `s`, com ou sem Torre. -/
theorem a_leitura_vale_para_todo_real (s l : ℝ) :
    ((lightBoost C).V s).conjStarAlgEquiv ((lightNet C).U (l • nullDir)) =
      (lightNet C).U ((Real.exp s * l) • nullDir) := by
  rw [(lightBoost C).V_translations, wedgeBoostMap_smul, wedgeBoostMap_nullDir, smul_smul, mul_comm l]

/-- A leitura da Torre é o caso `s = log (razão dos pesos)` da leitura geral: a Torre entra como índice. -/
theorem a_torre_entra_como_indice (P : SiteProfile) (N : ℕ) (i j : chainIdx N) (l : ℝ) :
    ((lightBoost C).V (rapidity P N i j)).conjStarAlgEquiv ((lightNet C).U (l • nullDir)) =
      (lightNet C).U ((localEigenvalue P N i j * l) • nullDir) := by
  rw [a_leitura_vale_para_todo_real C (rapidity P N i j) l, exp_rapidity]

/-- A mesma leitura no tempo modular, para todo real. -/
theorem a_leitura_modular_vale_para_todo_real (s l : ℝ) :
    (lightDelta C (modularTime s)).conjStarAlgEquiv ((lightNet C).U (l • nullDir)) =
      (lightNet C).U ((Real.exp s * l) • nullDir) := by
  unfold lightDelta
  rw [boost_parameter_at_modular_time]
  exact a_leitura_vale_para_todo_real C s l

/-! ## 6. A borda determina a transformação afim, ponto a ponto -/

/-- ★ Duas transformações afins de `ℝ⁴` que coincidem em todo ponto da borda da cunha direita são iguais. -/
theorem a_borda_determina_a_transformacao_afim (M' N' : Matrix (Fin 4) (Fin 4) ℝ) (a b : Point)
    (h : ∀ x ∈ frontier rightWedge, M'.mulVec x + a = N'.mulVec x + b) : M' = N' ∧ a = b := by
  have hf : ∀ x ∈ futureSheet, x ∈ frontier rightWedge := by
    intro x hx; rw [boundary_two_sheets]; exact Or.inl hx
  have hp : ∀ x ∈ pastSheet, x ∈ frontier rightWedge := by
    intro x hx; rw [boundary_two_sheets]; exact Or.inr hx
  have P0 : (![0,0,0,0] : Point) ∈ frontier rightWedge :=
    hf _ (generator_labels 0 0 0 (le_refl 0)).2.2.1
  have P1 : (![1,1,0,0] : Point) ∈ frontier rightWedge :=
    hf _ (generator_labels 1 0 0 (by norm_num)).1
  have P2 : (![-1,1,0,0] : Point) ∈ frontier rightWedge :=
    hp _ (generator_labels 1 0 0 (by norm_num)).2.1
  have P3 : (![0,0,1,0] : Point) ∈ frontier rightWedge :=
    hf _ (generator_labels 0 1 0 (le_refl 0)).2.2.1
  have P4 : (![0,0,0,1] : Point) ∈ frontier rightWedge :=
    hf _ (generator_labels 0 0 1 (le_refl 0)).2.2.1
  have hab : a = b := by
    have := h _ P0
    have z : (![0,0,0,0] : Point) = 0 := by funext i; fin_cases i <;> rfl
    rw [z, Matrix.mulVec_zero, Matrix.mulVec_zero, zero_add, zero_add] at this
    exact this
  subst hab
  have hD : ∀ x ∈ frontier rightWedge, (M' - N').mulVec x = 0 := by
    intro x hx
    have := h x hx
    have h2 : M'.mulVec x = N'.mulVec x := add_right_cancel this
    rw [Matrix.sub_mulVec, h2, sub_self]
  have d1 := hD _ P1
  have d2 := hD _ P2
  have d3 := hD _ P3
  have d4 := hD _ P4
  refine ⟨?_, rfl⟩
  have k0 : (M' - N').mulVec (Pi.single 0 1) = 0 := by
    have : (Pi.single 0 1 : Point) = (1/2:ℝ) • (![1,1,0,0] - ![-1,1,0,0]) := by
      funext i; fin_cases i <;> simp
      norm_num
    rw [this, Matrix.mulVec_smul, Matrix.mulVec_sub, d1, d2]; simp
  have k1 : (M' - N').mulVec (Pi.single 1 1) = 0 := by
    have : (Pi.single 1 1 : Point) = (1/2:ℝ) • (![1,1,0,0] + ![-1,1,0,0]) := by
      funext i; fin_cases i <;> simp
      norm_num
    rw [this, Matrix.mulVec_smul, Matrix.mulVec_add, d1, d2]; simp
  have k2 : (M' - N').mulVec (Pi.single 2 1) = 0 := by
    have : (Pi.single 2 1 : Point) = ![0,0,1,0] := by
      funext i; fin_cases i <;> simp
    rw [this]; exact d3
  have k3 : (M' - N').mulVec (Pi.single 3 1) = 0 := by
    have : (Pi.single 3 1 : Point) = ![0,0,0,1] := by
      funext i; fin_cases i <;> simp
    rw [this]; exact d4
  have key : ∀ j : Fin 4, (M' - N').mulVec (Pi.single j 1) = 0 := by
    intro j
    fin_cases j
    exacts [k0, k1, k2, k3]
  ext i j
  have := congrFun (key j) i
  simp at this
  linarith

/-- ★ O que a borda deixa livre é exatamente o que não é afim: o cisalhamento (`K07.Horizon.shear`), que
fixa todo ponto da borda e muda intervalos, não é transformação afim alguma. A borda sozinha não determina; os
valores na borda, mais a regra afim, determinam. -/
theorem o_cisalhamento_nao_e_afim (s : ℝ) (hs : s ≠ 0) :
    ¬ ∃ (M' : Matrix (Fin 4) (Fin 4) ℝ) (a : Point), ∀ x, shear s x = M'.mulVec x + a := by
  rintro ⟨M', a, h⟩
  have hb : ∀ x ∈ frontier rightWedge,
      M'.mulVec x + a = (1 : Matrix (Fin 4) (Fin 4) ℝ).mulVec x + 0 := by
    intro x hx
    rw [← h x, shear_fixes_boundary s x hx, Matrix.one_mulVec, add_zero]
  obtain ⟨hM, ha⟩ := a_borda_determina_a_transformacao_afim M' 1 a 0 hb
  apply shear_refutes_interval_preservation s hs
  rw [h, hM, ha, Matrix.one_mulVec, add_zero]

/-- A face da relatividade: dois observadores (Lorentz gerado mais translação) cujas cartas coincidem em
todo ponto da borda da cunha são o mesmo observador. -/
theorem dois_observadores_iguais_na_borda_sao_o_mesmo (L L' : generatedLorentz) (a a' : Point)
    (h : ∀ x ∈ frontier rightWedge, observerChart L a x = observerChart L' a' x) :
    L = L' ∧ a = a' := by
  obtain ⟨hM, ha⟩ := a_borda_determina_a_transformacao_afim L.val.val L'.val.val a a'
    (fun x hx => h x hx)
  exact ⟨Subtype.ext (Subtype.ext hM), ha⟩

/-- A unicidade não é vazia: há realização para a cunha e o vácuo. -/
theorem ha_realizacao_na_cunha : ∃ (J : F ≃ₛₗᵢ[starRingEnd ℂ] F) (B : UnitaryFlow F),
    PairTomitaAnalyticRealizationMeasured (net rightWedge).toStarSubalgebra vacuum J B.U :=
  ⟨canonicalFockJ, fockFlow, pair_tomita⟩

/-- O boost não age por escalar no tempo 1: a recusa do fluxo escalar e o núcleo fator, juntos. -/
theorem o_boost_nao_age_por_escalar_no_tempo_um (c : ℂ) :
    boostCLM fockFlow 1 ≠ c • (1 : F →L[ℂ] F) := by
  intro h
  refine fluxo_escalar_no_tempo_um_o_nucleo_nao_e_fator (net rightWedge) fockFlow
    ⟨vacuum, ?_⟩ c h o_centro_do_nucleo_da_cunha_e_escalar
  intro h0
  have hn := vacuum_norm
  rw [h0, norm_zero] at hn
  exact zero_ne_one hn

/-- A marca do ESTADO, como o kernel já a tinha, no certificado físico: o que o relógio da cunha deixa parado é
múltiplo do Um. Fica aqui ao lado da marca do núcleo. -/
theorem marca_do_estado_no_certificado_fisico
    (a : wedgeAlgebra physicalFockCertificate)
    (ha : ∀ t : ℝ, physicalFockCertificate.flow t a = a) :
    ∃ c : ℂ, (a : physicalFockCertificate.F →L[ℂ] physicalFockCertificate.F) = c • 1 :=
  TGLExt.LightRhoStar.centralizer_is_trivial physicalFockCertificate a ha

/-- A marca do ESTADO escrita com os MESMOS objetos do critério do núcleo: a álgebra é `net rightWedge` e o relógio é
`fockFlow` (o fluxo do predicado). O que a conjugação pelo relógio deixa parado, na álgebra da cunha, é múltiplo do Um.
Sai do teorema do kernel pelas igualdades por construção do certificado físico (`physical_net`, `flow_is_Ad`): sem
elas, pôr as duas marcas lado a lado seria encadear homônimos. -/
theorem marca_do_estado_na_lingua_do_criterio (a : F →L[ℂ] F) (ha : a ∈ net rightWedge)
    (hfix : ∀ t : ℝ, (fockFlow.U t).conjStarAlgEquiv a = a) :
    ∃ c : ℂ, a = c • (1 : F →L[ℂ] F) := by
  have ha' : a ∈ (wedgeAlgebra physicalFockCertificate) := ha
  exact marca_do_estado_no_certificado_fisico ⟨a, ha'⟩ (fun t => by
    apply Subtype.ext
    rw [physicalFockCertificate.flow_is_Ad t ⟨a, ha'⟩]
    exact hfix t)

/-- A cunha de todo observador (Lorentz gerado mais translação) cumpre o critério do núcleo. É o teorema
`K07.Horizon.TransportCenter.maxwell_observer_wedge_type_III1`, com o nome do que ele prova. -/
theorem a_cunha_de_todo_observador_cumpre_o_criterio_do_nucleo (L : generatedLorentz) (a : Point) :
    IsTypeIII1 (net (observerChart L a '' rightWedge)) :=
  K07.Horizon.TransportCenter.maxwell_observer_wedge_type_III1 L a

/-- **CONTROLE.** A borda COMO LUGAR não determina o observador: existe um observador, diferente da
identidade, que leva a borda nela mesma. O `s` do enunciado só escolhe a testemunha (a conclusão não fala dele); a
família inteira está nos dois termos seguintes. A unicidade vale só ponto a ponto. -/
theorem a_borda_como_conjunto_nao_determina (s : ℝ) (hs : s ≠ 0) :
    ∃ L : generatedLorentz, L ≠ 1 ∧
      observerChart L 0 '' frontier rightWedge = frontier rightWedge := by
  have hmem : theBoost s ∈ generatedLorentz := Subgroup.subset_closure (Or.inr ⟨s, rfl⟩)
  have hfun : (⇑(observerChart ⟨theBoost s, hmem⟩ 0) : Point → Point) = wedgeBoostMap s := by
    funext x
    change (theBoost s).val.mulVec x + 0 = wedgeBoostMap s x
    rw [add_zero]
    rfl
  refine ⟨⟨theBoost s, hmem⟩, ?_, ?_⟩
  · intro h
    have h1 : (theBoost s) = (1 : LorentzGrp) := congrArg Subtype.val h
    have h2 : wedgeBoostMap s nullDir = nullDir := by
      have h3 : (theBoost s).val.mulVec nullDir = (1 : LorentzGrp).val.mulVec nullDir := by rw [h1]
      have h4 : (1 : LorentzGrp).val.mulVec nullDir = nullDir := by
        rw [lorentzGrp_one_val, Matrix.one_mulVec]
      exact h3.trans h4
    rw [wedgeBoostMap_nullDir] at h2
    have hcoord := congrFun h2 (0 : Fin 4)
    apply hs
    apply Real.exp_injective
    simpa [nullDir] using hcoord
  · rw [(observerChart ⟨theBoost s, hmem⟩ 0).image_frontier, hfun, FlagNet.boost_image_rightWedge]

/-- TODO boost da cunha é um observador que leva a borda nela mesma. -/
theorem todo_boost_da_cunha_leva_a_borda_nela_mesma (s : ℝ) :
    ∃ h : theBoost s ∈ generatedLorentz,
      observerChart ⟨theBoost s, h⟩ 0 '' frontier rightWedge = frontier rightWedge := by
  have hmem : theBoost s ∈ generatedLorentz := Subgroup.subset_closure (Or.inr ⟨s, rfl⟩)
  have hfun : (⇑(observerChart ⟨theBoost s, hmem⟩ 0) : Point → Point) = wedgeBoostMap s := by
    funext x
    change (theBoost s).val.mulVec x + 0 = wedgeBoostMap s x
    rw [add_zero]
    rfl
  refine ⟨hmem, ?_⟩
  rw [(observerChart ⟨theBoost s, hmem⟩ 0).image_frontier, hfun, FlagNet.boost_image_rightWedge]

/-- Boosts de parâmetros diferentes são transformações de Lorentz diferentes (em particular, só o de parâmetro zero
é a identidade): há uma família a um parâmetro de observadores distintos com a mesma borda. -/
theorem boosts_de_parametros_diferentes_sao_diferentes (s t : ℝ) (h : theBoost s = theBoost t) : s = t := by
  have h3 : (theBoost s).val.mulVec nullDir = (theBoost t).val.mulVec nullDir := by rw [h]
  have h2 : wedgeBoostMap s nullDir = wedgeBoostMap t nullDir := h3
  rw [wedgeBoostMap_nullDir, wedgeBoostMap_nullDir] at h2
  have hcoord := congrFun h2 (0 : Fin 4)
  apply Real.exp_injective
  simpa [nullDir] using hcoord

end cunha


end Vinculo.Controles
