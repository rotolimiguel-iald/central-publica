import TGLExt.ModularFlowSpectrum
import TGLExt.AffineClockAndRegion
import TGLExt.V350WedgeModularData
import TGLExt.FlagNetV31
import TGLExt.LightRhoStar
import TGLExt.F1Fecho394.CanonicalFockModularCoreInputR1

set_option autoImplicit false
set_option maxHeartbeats 1600000

/-! Vínculo entre os rótulos modulares da torre e o observador da cunha direita.
    A orientação de rapidez é fixada por `wedgeBoostMap_nullDir`. -/
noncomputable section
namespace K07.TowerWedge

open TGLExt ChatgptAudit TGLExt.ImportedSQ TGLExt.ContratoQGv31 TGL.SpecificAQFT
open F1Fecho.CanonicalFockModularCoreInputR1

/-- Rapidez que tem por fator de dilatação o autovalor modular da unidade
matricial (i,j) na representação da torre. -/
def rapidity (P : SiteProfile) (N : ℕ) (i j : chainIdx N) : ℝ :=
  Real.log (localEigenvalue P N i j)

theorem exp_rapidity (P : SiteProfile) (N : ℕ) (i j : chainIdx N) :
    Real.exp (rapidity P N i j) = localEigenvalue P N i j :=
  Real.exp_log (localEigenvalue_pos N i j)

theorem rapidity_unique (P : SiteProfile) (N : ℕ) (i j : chainIdx N) (s : ℝ) :
    Real.exp s = localEigenvalue P N i j ↔ s = rapidity P N i j := by
  rw [← exp_rapidity P N i j, Real.exp_injective.eq_iff]

/-- As unidades matriciais componíveis somam suas rapidezes. -/
theorem rapidity_comp (P : SiteProfile) (N : ℕ) (i j k : chainIdx N) :
    rapidity P N i j + rapidity P N j k = rapidity P N i k := by
  simp only [rapidity, localEigenvalue, Real.log_div (towerW_pos P N _).ne'
    (towerW_pos P N _).ne']
  ring

/-- O embutimento da torre envia Eᵢⱼ a Eᵢⱼ ⊗ 1. Cada parcela diagonal
na letra acrescentada guarda exatamente a rapidez anterior. -/
theorem rapidity_refine (P : SiteProfile) (N : ℕ) (i j : chainIdx N) (a : Fin 2) :
    rapidity P (N+1) (i,a) (j,a) = rapidity P N i j := by
  have ha := (siteW_pos (P.pos (N+1)) (P.lt_one (N+1)) a).ne'
  simp only [rapidity, localEigenvalue, towerW, mul_div_mul_right _ _ ha]

theorem tower_unit_flow (P : SiteProfile) (N : ℕ) (i j : chainIdx N) (t : ℝ) :
    modularFlow P t (localEigenvector P N i j) =
      modularPhase t (rapidity P N i j) • localEigenvector P N i j :=
  modularFlow_eigenvector t N i j

variable {L : LightOneParticle} (C : FockCertificate L)

/-- O boost de rapidez lida na torre atua na translação física de Fock. -/
theorem indexed_boost_translation (P : SiteProfile) (N : ℕ) (i j : chainIdx N) (l : ℝ) :
    ((lightBoost C).V (rapidity P N i j)).conjStarAlgEquiv ((lightNet C).U (l • nullDir)) =
      (lightNet C).U ((localEigenvalue P N i j * l) • nullDir) := by
  rw [(lightBoost C).V_translations, wedgeBoostMap_smul, wedgeBoostMap_nullDir,
    smul_smul, exp_rapidity, mul_comm l]

set_option backward.isDefEq.respectTransparency false in
/-- A mesma operação é um instante do relógio modular da cunha. -/
theorem indexed_modular_translation (P : SiteProfile) (N : ℕ) (i j : chainIdx N) (l : ℝ) :
    (lightDelta C (-(rapidity P N i j)/(2*Real.pi))).conjStarAlgEquiv
      ((lightNet C).U (l • nullDir)) =
      (lightNet C).U ((localEigenvalue P N i j * l) • nullDir) := by
  have ht : -(2*Real.pi*(-(rapidity P N i j)/(2*Real.pi))) = rapidity P N i j := by
    field_simp [Real.pi_ne_zero]
  unfold lightDelta
  rw [ht]
  exact indexed_boost_translation C P N i j l

def rapidityLabels (P : SiteProfile) : Set ℝ :=
  {s | ∃ (N : ℕ) (i j : chainIdx N), s = rapidity P N i j}

theorem first_mixed_rapidity :
    rapidity mixProfile 0 0 1 = Real.log ((1:ℝ)/2) := by
  norm_num [rapidity, localEigenvalue, towerW, siteW, mixProfile]

theorem second_mixed_rapidity :
    rapidity mixProfile 1 (0,0) (0,1) = Real.log ((1:ℝ)/3) := by
  norm_num [rapidity, localEigenvalue, towerW, siteW, mixProfile]

theorem mixed_generators :
    ({Real.log ((1:ℝ)/2), Real.log ((1:ℝ)/3)} : Set ℝ) ⊆ rapidityLabels mixProfile := by
  intro s hs
  rcases hs with h | h
  · exact ⟨0,0,1,h.trans first_mixed_rapidity.symm⟩
  · exact ⟨1,(0,0),(0,1),(Set.mem_singleton_iff.mp h).trans second_mixed_rapidity.symm⟩

theorem mixed_rapidities_dense :
    Dense ((AddSubgroup.closure (rapidityLabels mixProfile) : AddSubgroup ℝ) : Set ℝ) :=
  the_mixing_mark.mono (AddSubgroup.closure_mono mixed_generators)

/-- Em cada vetor de Fock, a órbita de todos os boosts é aproximada pelas
composições dos boosts indexados. A topologia usada aqui é a norma do vetor. -/
theorem mixed_boost_orbit_dense (v : C.F) :
    Set.range (fun s : ℝ => (lightBoost C).V s v) ⊆
      closure ((fun s : ℝ => (lightBoost C).V s v) ''
        ((AddSubgroup.closure (rapidityLabels mixProfile) : AddSubgroup ℝ) : Set ℝ)) :=
  ((lightBoost C).V_continuous v).range_subset_closure_image_dense mixed_rapidities_dense

abbrev towerAlgebra (P : SiteProfile) := (theFactorObject P).toStarSubalgebra
abbrev wedgeAlgebra := (C.R (L.K rightWedge)).toStarSubalgebra

/-- Unidade matricial dentro do objeto de von Neumann da torre. -/
def towerUnit (P : SiteProfile) (N : ℕ) (i j : chainIdx N) : towerAlgebra P :=
  ⟨towerPi P (Matrix.single i j 1), towerPi_mem_factor _⟩

theorem tower_unit_character (P : SiteProfile) (N : ℕ) (i j : chainIdx N) (t : ℝ) :
    V350Continuous.factorFlow P t (towerUnit P N i j) =
      modularPhase t (rapidity P N i j) • towerUnit P N i j := by
  apply Subtype.ext
  change modularConjugation P t (towerPi P (Matrix.single i j 1)) =
    modularPhase t (rapidity P N i j) • towerPi P (Matrix.single i j 1)
  rw [modularConjugation_local, flowLevel_single, towerPi_smul]
  rfl

/-- Cunha direita deslocada no gerador nulo futuro. -/
def nullWedge (l : ℝ) : Set (Fin 4 → ℝ) :=
  TGL.SpecificAQFT.translate (l • nullDir) rightWedge

theorem boost_null_wedge (s l : ℝ) :
    wedgeBoostMap s '' nullWedge l = nullWedge (Real.exp s * l) := by
  change wedgeBoostMap s '' ((fun x => x + l • nullDir) '' rightWedge) =
    (fun x => x + (Real.exp s * l) • nullDir) '' rightWedge
  calc
    _ = (fun y => y + (Real.exp s * l) • nullDir) '' (wedgeBoostMap s '' rightWedge) := by
      rw [Set.image_image, Set.image_image]
      apply Set.image_congr
      intro x _
      change wedgeBoostMap s (x + l • nullDir) = wedgeBoostMap s x + (Real.exp s * l) • nullDir
      have hadd : wedgeBoostMap s (x + l • nullDir) =
          wedgeBoostMap s x + wedgeBoostMap s (l • nullDir) := by
        unfold wedgeBoostMap
        rw [Matrix.mulVec_add]
      rw [hadd, wedgeBoostMap_smul, wedgeBoostMap_nullDir, smul_smul, mul_comm l]
    _ = _ := by rw [FlagNet.boost_image_rightWedge]

/-- Em álgebras locais, o mesmo índice transporta a cunha inteira. -/
theorem indexed_local_covariance (P : SiteProfile) (N : ℕ) (i j : chainIdx N) (l : ℝ)
    (a : (lightNet C).H →L[ℂ] (lightNet C).H) (ha : a ∈ (lightNet C).net (nullWedge l)) :
    ((lightBoost C).V (rapidity P N i j)).conjStarAlgEquiv a ∈
      (lightNet C).net (nullWedge (localEigenvalue P N i j * l)) := by
  have h := (lightBoost C).V_net (rapidity P N i j) (nullWedge l) a ha
  rwa [boost_null_wedge, exp_rapidity] at h

private theorem translations_injective : Function.Injective (lightNet C).U := by
  intro a b hab
  have h0 : (lightNet C).U (a + -b) = 1 := by
    rw [(lightNet C).U_add, hab, ← (lightNet C).U_add, add_neg_cancel, (lightNet C).U_zero]
  exact sub_eq_zero.mp (by simpa [sub_eq_add_neg] using light_translations_faithful C _ h0)

/-- A ação em uma translação nula unitária discrimina quaisquer duas
rapidezes; a identificação da escala também é fiel na representação. -/
theorem null_translation_reads_rapidity :
    Function.Injective (fun s : ℝ =>
      ((lightBoost C).V s).conjStarAlgEquiv ((lightNet C).U nullDir)) := by
  intro s t h
  change ((lightBoost C).V s).conjStarAlgEquiv ((lightNet C).U nullDir) =
    ((lightBoost C).V t).conjStarAlgEquiv ((lightNet C).U nullDir) at h
  rw [(lightBoost C).V_translations, (lightBoost C).V_translations,
    wedgeBoostMap_nullDir, wedgeBoostMap_nullDir] at h
  have hcoord := congrFun (translations_injective C h) (0 : Fin 4)
  apply Real.exp_injective
  simpa [nullDir] using hcoord

/-- Períodos do vetor no grupo unitário do observador da cunha. -/
def boostPeriods (v : C.F) : AddSubgroup ℝ where
  carrier := {s | (lightBoost C).V s v = v}
  zero_mem' := by change (lightBoost C).V 0 v = v; rw [(lightBoost C).V_zero]; rfl
  add_mem' := by
    intro s t hs ht
    change (lightBoost C).V s v = v at hs
    change (lightBoost C).V t v = v at ht
    change (lightBoost C).V (s+t) v = v
    rw [(lightBoost C).V_add, LinearIsometryEquiv.trans_apply, ht, hs]
  neg_mem' := by
    intro s hs
    change (lightBoost C).V s v = v at hs
    change (lightBoost C).V (-s) v = v
    calc
      (lightBoost C).V (-s) v = (lightBoost C).V (-s) ((lightBoost C).V s v) := congrArg _ hs.symm
      _ = (lightBoost C).V (-s + s) v := by rw [(lightBoost C).V_add]; rfl
      _ = v := by rw [neg_add_cancel, (lightBoost C).V_zero]; rfl

/-- Duas leituras efetivas dos primeiros andares da torre recuperam a
reta do vácuo no espaço de Fock completo. -/
theorem two_tower_boosts_read_vacuum (v : C.F) :
    ((lightBoost C).V (rapidity mixProfile 0 0 1) v = v ∧
      (lightBoost C).V (rapidity mixProfile 1 (0,0) (0,1)) v = v) ↔
      v ∈ (ℂ ∙ C.Ω) := by
  rw [first_mixed_rapidity, second_mixed_rapidity]
  constructor
  · intro ⟨hh,ht⟩
    have hsub : AddSubgroup.closure
        {Real.log ((1:ℝ)/2),Real.log ((1:ℝ)/3)} ≤ boostPeriods C v :=
      (AddSubgroup.closure_le _).mpr (by
        intro s hs
        rcases hs with h | h
        · rw [h]; exact hh
        · rw [Set.mem_singleton_iff.mp h]; exact ht)
    have hclosed : IsClosed ((boostPeriods C v : AddSubgroup ℝ) : Set ℝ) :=
      isClosed_eq ((lightBoost C).V_continuous v) continuous_const
    apply (QGReaderUVLock.light_modular_fixed_iff_vacuum C v).mp
    intro t
    exact (closure_minimal (show
      ((AddSubgroup.closure {Real.log ((1:ℝ)/2),Real.log ((1:ℝ)/3)} : AddSubgroup ℝ) : Set ℝ)
        ⊆ (boostPeriods C v : Set ℝ) from hsub) hclosed) (the_mixing_mark (-(2*Real.pi*t)))
  · intro hv
    obtain ⟨c,rfl⟩ := Submodule.mem_span_singleton.mp hv
    have h (s : ℝ) : (lightBoost C).V s (c • C.Ω) = c • C.Ω := by
      change C.Γ (B0 s) (c • C.Ω) = c • C.Ω
      rw [map_smul, C.Γ_vac]
    exact ⟨h _,h _⟩

def modularTime (s : ℝ) : ℝ := -s / (2*Real.pi)

theorem boost_parameter_at_modular_time (s : ℝ) :
    -(2*Real.pi*modularTime s) = s := by
  unfold modularTime
  field_simp [Real.pi_ne_zero]

private theorem boost_vector_fixed (s : ℝ) (a : wedgeAlgebra C)
    (h : C.flow (modularTime s) a = a) :
    (lightBoost C).V s ((a : C.F →L[ℂ] C.F) C.Ω) = (a : C.F →L[ℂ] C.F) C.Ω := by
  have had := C.flow_is_Ad (modularTime s) a
  rw [h, boost_parameter_at_modular_time] at had
  have hv := congrArg (fun T : C.F →L[ℂ] C.F => T C.Ω) had
  have hsym : (C.Γ (B0 s)).symm C.Ω = C.Ω := by
    apply (C.Γ (B0 s)).injective
    rw [LinearIsometryEquiv.apply_symm_apply, C.Γ_vac]
  simp only [LinearIsometryEquiv.conjStarAlgEquiv_apply_apply,hsym] at hv
  exact hv.symm

/-- Os dois instantes determinados na torre separam os escalares de todos
os demais observáveis da cunha por dois testes exatos de fixidez. -/
theorem two_tower_times_read_scalars (a : wedgeAlgebra C) :
    (C.flow (modularTime (rapidity mixProfile 0 0 1)) a = a ∧
      C.flow (modularTime (rapidity mixProfile 1 (0,0) (0,1))) a = a) ↔
      ∃ c : ℂ, a = algebraMap ℂ (wedgeAlgebra C) c := by
  constructor
  · intro ⟨h₁,h₂⟩
    have hline := (two_tower_boosts_read_vacuum C ((a : C.F →L[ℂ] C.F) C.Ω)).mp
      ⟨boost_vector_fixed C _ a h₁, boost_vector_fixed C _ a h₂⟩
    obtain ⟨c,hc⟩ := Submodule.mem_span_singleton.mp hline
    let b := a - algebraMap ℂ (wedgeAlgebra C) c
    have hb : (b : C.F →L[ℂ] C.F) C.Ω = 0 := by
      simp [b, Algebra.algebraMap_eq_smul_one, ← hc]
    have hz := C.wedge_separating _ b.property hb
    refine ⟨c, sub_eq_zero.mp ?_⟩
    exact Subtype.ext hz
  · rintro ⟨c,rfl⟩
    exact ⟨AlgHomClass.commutes _ c,AlgHomClass.commutes _ c⟩

/-- Projeção de um sítio da torre, dentro do bicomutante. -/
def siteProjection (P : SiteProfile) (n : ℕ) : towerAlgebra P :=
  ⟨siteOperator P n (Matrix.single 0 0 1), siteOperator_mem_factor _ _⟩

theorem site_fixed (P : SiteProfile) (n : ℕ) (t : ℝ) :
    V350Continuous.factorFlow P t (siteProjection P n) = siteProjection P n :=
  Subtype.ext (Cocycle030.site_zero_modular_fixed P n t)

/-- O confronto com E₀₁, no mesmo sítio, exclui qualquer valor escalar. -/
theorem site_nonscalar (P : SiteProfile) (n : ℕ) (c : ℂ) :
    siteProjection P n ≠ algebraMap ℂ (towerAlgebra P) c := by
  intro h
  have he := congrArg (fun a : towerAlgebra P => (a : TowerHilbert P →L[ℂ] TowerHilbert P)) h
  change siteOperator P n (Matrix.single 0 0 1) =
    algebraMap ℂ (TowerHilbert P →L[ℂ] TowerHilbert P) c at he
  apply Clock040.region_site_noncommutation (P := P) n
  rw [he]
  exact Algebra.commutes c _

/-- Nenhuma injeção algébrica unital e complexa entrelaça os dois fluxos
com seus estados escolhidos, mesmo admitindo qualquer reparametrização
do tempo da torre como função do tempo da cunha. -/
theorem no_flow_intertwining_embedding (P : SiteProfile) (clock : ℝ → ℝ)
    (φ : towerAlgebra P →ₐ[ℂ] wedgeAlgebra C) (hinj : Function.Injective φ)
    (hcov : ∀ (t : ℝ) (a : towerAlgebra P),
      φ (V350Continuous.factorFlow P (clock t) a) = C.flow t (φ a)) : False := by
  let p := siteProjection P 0
  have hfix (t : ℝ) : C.flow t (φ p) = φ p := by
    rw [← hcov]
    exact congrArg φ (site_fixed P 0 (clock t))
  obtain ⟨c, hc⟩ := LightRhoStar.centralizer_is_trivial C (φ p) hfix
  apply site_nonscalar P 0 c
  apply hinj
  rw [φ.commutes]
  apply Subtype.ext
  simpa [Algebra.algebraMap_eq_smul_one] using hc

theorem physical_wedge_index (N : ℕ) (i j : chainIdx N) (l : ℝ) :
    ((lightBoost physicalFockCertificate).V (rapidity mixProfile N i j)).conjStarAlgEquiv
      ((lightNet physicalFockCertificate).U (l • nullDir)) =
      (lightNet physicalFockCertificate).U ((localEigenvalue mixProfile N i j * l) • nullDir) :=
  indexed_boost_translation physicalFockCertificate mixProfile N i j l

theorem physical_no_flow_intertwining_embedding (P : SiteProfile) (clock : ℝ → ℝ)
    (φ : towerAlgebra P →ₐ[ℂ] wedgeAlgebra physicalFockCertificate) (hinj : Function.Injective φ)
    (hcov : ∀ (t : ℝ) (a : towerAlgebra P),
      φ (V350Continuous.factorFlow P (clock t) a) = physicalFockCertificate.flow t (φ a)) : False :=
  no_flow_intertwining_embedding physicalFockCertificate P clock φ hinj hcov


end K07.TowerWedge
