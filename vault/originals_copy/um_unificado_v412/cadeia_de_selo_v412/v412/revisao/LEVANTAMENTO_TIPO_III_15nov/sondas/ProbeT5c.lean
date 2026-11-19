import TGLExt.LightRhoStar
import TGLExt.F1Fecho394.CanonicalFockModularCoreInputR1
import TGLExt.F1Fecho394.CanonicalFockActualPositiveTracePackageR2
import TGLExt.F1Fecho394.CanonicalFockFaithfulWeightR2

set_option autoImplicit false
open scoped ENNReal NNReal

/-! SONDA T5c: (1) o teorema do kernel instancia em physicalFockCertificate; (2) as quatro definicoes tipam. -/

namespace T5Probe

open F1Fecho.CanonicalFockModularCoreInputR1 TGLExt.LightRhoStar

section defs
variable {F : Type} [NormedAddCommGroup F] [InnerProductSpace ℂ F] [CompleteSpace F]

/-- fator: o centro de M e' escalar -/
def IsFactor (M : VonNeumannAlgebra F) : Prop :=
  ∀ z ∈ M, (∀ a ∈ M, a * z = z * a) → ∃ c : ℂ, z = c • (1 : F →L[ℂ] F)

/-- nao-trivial: M nao e' so escalares (existe par nao comutativo) -/
def NonComm (M : VonNeumannAlgebra F) : Prop := ∃ a ∈ M, ∃ b ∈ M, a * b ≠ b * a

/-- p ~ 1 em M (Murray-von Neumann): isometria de M com projecao de imagem p -/
def EquivOne (M : VonNeumannAlgebra F) (p : F →L[ℂ] F) : Prop :=
  ∃ v ∈ M, star v * v = 1 ∧ v * star v = p

/-- (A) por projecoes: fator infinito puro (tipo III, qualquer lambda) -/
def PurelyInfiniteFactor (M : VonNeumannAlgebra F) : Prop :=
  IsFactor M ∧ NonComm M ∧ ∀ p ∈ M, IsStarProjection p → p ≠ 0 → EquivOne M p

/-- (B) peso tracial normal fiel semifinito em M, valorado em ENNReal -/
structure NFSTrace (M : VonNeumannAlgebra F) where
  τ : (F →L[ℂ] F) → ℝ≥0∞
  zero : τ 0 = 0
  add : ∀ a ∈ M, ∀ b ∈ M, 0 ≤ a → 0 ≤ b → τ (a + b) = τ a + τ b
  smul : ∀ (r : ℝ≥0) (a : F →L[ℂ] F), a ∈ M → 0 ≤ a → τ (((r : ℝ) : ℂ) • a) = (r : ℝ≥0∞) * τ a
  tracial : ∀ x ∈ M, τ (star x * x) = τ (x * star x)
  faithful : ∀ a ∈ M, 0 ≤ a → τ a = 0 → a = 0
  normal : ∀ {ι : Type} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (a : ι → F →L[ℂ] F) (s : F →L[ℂ] F),
    (∀ i, a i ∈ M ∧ 0 ≤ a i) → Monotone a → IsLUB (Set.range a) s → s ∈ M →
    τ s = ⨆ i, τ (a i)
  semifinite : ∀ p ∈ M, IsStarProjection p → p ≠ 0 →
    ∃ q ∈ M, IsStarProjection q ∧ q ≠ 0 ∧ q ≤ p ∧ τ q < ⊤

/-- (B) sem traco normal fiel semifinito -/
def NoNFSTrace (M : VonNeumannAlgebra F) : Prop := IsEmpty (NFSTrace M)

/-- (D) por estado vetorial ergodico: Omega separador, grupo unitario sigma que e' KMS a beta = 1 para Omega,
    pontos fixos de Ad sigma_t em M so escalares, M nao comutativa -/
def ErgodicVectorState (M : VonNeumannAlgebra F) : Prop :=
  ∃ (Ω : F) (σ : ℝ → (F ≃ₗᵢ[ℂ] F)),
    ‖Ω‖ = 1 ∧
    Dense ((Submodule.span ℂ ((fun T : F →L[ℂ] F => T Ω) '' (M : Set (F →L[ℂ] F))) : Submodule ℂ F) : Set F) ∧
    (∀ a ∈ M, a Ω = 0 → a = 0) ∧
    TGLExt.ImportedSQ.KMSBody M Ω σ 1 ∧
    (∀ a ∈ M, (∀ t : ℝ, (σ t).conjStarAlgEquiv a = a) → ∃ c : ℂ, a = c • (1 : F →L[ℂ] F)) ∧
    NonComm M


open F1Fecho.CanonicalFockModularCoreInputR1

/-- (D) para o certificado generico: vacuo separador (cunha), KMS (bw_kms), fixos escalares (centralizer_is_trivial), nao comutativa. -/
theorem ergodicVectorState_of_certificate {L : TGLExt.ImportedSQ.LightOneParticle}
    (C : TGLExt.ImportedSQ.FockCertificate L) :
    ErgodicVectorState (C.R (L.K TGL.SpecificAQFT.rightWedge)) := by
  refine ⟨C.Ω, fun t => C.Γ (TGLExt.ImportedSQ.B0 (2 * Real.pi * t)), C.Ω_norm, C.wedge_cyclic, C.wedge_separating,
    C.bw_kms, ?_, C.wedge_nonabelian⟩
  intro a ha hfix
  have hflow : ∀ t : ℝ, C.flow t ⟨a, ha⟩ = ⟨a, ha⟩ := by
    intro t
    apply Subtype.ext
    rw [C.flow_is_Ad t ⟨a, ha⟩]
    have h := hfix (-t)
    have e : -(2 * Real.pi * t) = 2 * Real.pi * (-t) := by ring
    rw [e]
    exact h
  exact TGLExt.LightRhoStar.centralizer_is_trivial C ⟨a, ha⟩ hflow

/-- o mesmo, no certificado fisico, escrito em M := CanonicalWedgeFlow.M (a algebra da cunha, de F1Fecho). -/
theorem ergodicVectorState_M : ErgodicVectorState F1Fecho.CanonicalWedgeFlow.M := by
  have h := ergodicVectorState_of_certificate physicalFockCertificate
  have e : (physicalFockCertificate.R
      (F1Fecho.MaxwellLocalization.physicalCanonicalNet.toLightOneParticle.K TGL.SpecificAQFT.rightWedge))
      = F1Fecho.CanonicalWedgeFlow.M :=
    F1Fecho.PhysicalFockNet.net_wedge_eq
  rw [e] at h
  exact h

/-- controle de tipagem: toda algebra que contem os operadores de posto um (B(H), M_n na representacao
    defeituosa) e vive num espaco de dimensao >= 2 NAO satisfaz (D): nenhum vetor e' separador. -/
theorem not_ergodic_of_rank_one {M : VonNeumannAlgebra F}
    (hrank : ∀ η : F, (innerSL ℂ η).smulRight η ∈ M)
    (hdim : ∀ Ω : F, ∃ η : F, η ≠ 0 ∧ inner ℂ η Ω = (0 : ℂ)) :
    ¬ ErgodicVectorState M := by
  rintro ⟨Ω, σ, hn, -, hsep, -, -, -⟩
  obtain ⟨η, hη0, hηΩ⟩ := hdim Ω
  have h0 := hsep _ (hrank η) (by
    simp [ContinuousLinearMap.smulRight_apply, innerSL_apply_apply, hηΩ])
  have h1 := congrArg (fun T : F →L[ℂ] F => T η) h0
  simp [ContinuousLinearMap.smulRight_apply, innerSL_apply_apply] at h1
  exact hη0 h1

#print axioms ergodicVectorState_of_certificate
#print axioms ergodicVectorState_M
#print axioms not_ergodic_of_rank_one


/-- (C) pelo nucleo de Takesaki: o nucleo (produto cruzado por um fluxo unitario) e' fator. O traco normal fiel
    semifinito escalado pela acao dual NAO discrimina (todo (M, estado fiel) o tem): o que discrimina e' o centro. -/
def CoreIsFactor (U : F1Fecho.RegularCovariantCore.UnitaryFlow F) (M : VonNeumannAlgebra F) : Prop :=
  IsFactor (F1Fecho.RegularCovariantCore.core U M)

end defs

-- a parte (C1) do kernel, como TERMO, para o nucleo fisico:
#check @F1Fecho.CanonicalFockActualPositiveTracePackageR2.actualPositiveTrace
#print axioms F1Fecho.CanonicalFockActualPositiveTracePackageR2.actualPositiveTrace
#check @F1Fecho.CanonicalFockActualPositiveTracePackageR2.actualPositiveTrace_unit_infinite
#print axioms F1Fecho.CanonicalFockActualPositiveTracePackageR2.actualPositiveTrace_unit_infinite
#check @F1Fecho.CanonicalFockFaithfulWeight.fixed_core_is_base
-- (C2) para o nucleo fisico: o enunciado tipa; NAO ha termo
#check (CoreIsFactor F1Fecho.CanonicalFockRegular.fockFlow F1Fecho.CanonicalWedgeFlow.M)
end T5Probe
