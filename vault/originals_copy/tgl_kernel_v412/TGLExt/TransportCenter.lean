import TGLExt.WedgeHorizonObserver
import TGLExt.F1Fecho394.CanonicalFockRegularCoreR2
import TGLExt.V350SeparatingRestrictionVonNeumann

/-! The same observer acts on wedge observables and, fibrewise, on the
regular crossed product built from the transported flow on the actual net. -/
set_option autoImplicit false
set_option maxHeartbeats 800000
set_option synthInstance.maxHeartbeats 150000
noncomputable section

namespace K07.Horizon.TransportCenter
open TGL.SpecificAQFT TGLV350.Regular F1Rede.BosonicFock F1Fecho
open F1Fecho.OrbitalSpatial F1Fecho.RegularCovariantCore

abbrev Op := F →L[ℂ] F
abbrev RegOp := RegularHilbert F →L[ℂ] RegularHilbert F
abbrev frameU (L : generatedLorentz) (a : Point) := gamma (observerUnitary L a)
abbrev frameAlg (L : generatedLorentz) (a : Point) :=
  PhysicalFockNet.net (observerChart L a '' rightWedge)

theorem base_covariance (L : generatedLorentz) (a : Point) (A : Op) :
    A ∈ CanonicalFockRegular.M ↔ (frameU L a).conjStarAlgEquiv A ∈ frameAlg L a := by
  have h := (observer_and_wedge_algebra L a A).2
  rw [PhysicalFockNet.net_wedge_eq] at h
  exact h

def conjugateFlow (U : F ≃ₗᵢ[ℂ] F) (B : UnitaryFlow F) : UnitaryFlow F where
  U t := (U.symm.trans (B.U t)).trans U
  zero := by ext1 x; simp [B.zero]
  add s t := by ext1 x; simp [B.add]
  strong x := U.continuous.comp (B.strong (U.symm x))

private theorem unitary_sandwich (U : F ≃ₗᵢ[ℂ] F) (A : Op) :
    U.conjStarAlgEquiv A = (U : Op) * A * star (U : Op) := by
  rw [LinearIsometryEquiv.star_eq_symm]
  rfl

private theorem left_right_inverse (U : F ≃ₗᵢ[ℂ] F) :
    star (U : Op) * (U : Op) = 1 ∧ (U : Op) * star (U : Op) = 1 := by
  rw [LinearIsometryEquiv.star_eq_symm]
  exact ⟨by ext1 x; exact U.symm_apply_apply x, by ext1 x; exact U.apply_symm_apply x⟩

def regularFrameUnitary (U : F ≃ₗᵢ[ℂ] F) : unitary RegOp :=
  ⟨fibre (U : Op), by
    constructor
    · rw [← fibre_star, ← fibre_mul, (left_right_inverse U).1, fibre_one]
    · rw [← fibre_star, ← fibre_mul, (left_right_inverse U).2, fibre_one]⟩

def regularAd (U : F ≃ₗᵢ[ℂ] F) : RegOp ≃⋆ₐ[ℂ] RegOp :=
  Unitary.conjStarAlgAut ℂ _ (regularFrameUnitary U)

theorem regularAd_fibre (U : F ≃ₗᵢ[ℂ] F) (A : Op) :
    regularAd U (fibre A) = fibre (U.conjStarAlgEquiv A) := by
  change fibre (U : Op) * fibre A * star (fibre (U : Op)) = _
  rw [unitary_sandwich, fibre_mul, fibre_mul, fibre_star]

theorem regularAd_shift (U : F ≃ₗᵢ[ℂ] F) (t : ℝ) :
    regularAd U (shift t) = shift t := by
  change fibre (U : Op) * shift t * star (fibre (U : Op)) = shift t
  have hu : fibre (U : Op) * star (fibre (U : Op)) = 1 := (regularFrameUnitary U).property.2
  calc
    _ = (shift t * fibre (U : Op)) * star (fibre (U : Op)) :=
      congrArg (fun T : RegOp => T * star (fibre (U : Op))) (shift_commutes_fibre t (U : Op)).symm
    _ = shift t * (fibre (U : Op) * star (fibre (U : Op))) := mul_assoc _ _ _
    _ = shift t := by rw [hu, mul_one]

theorem regularAd_flow (U : F ≃ₗᵢ[ℂ] F) (B : UnitaryFlow F) (t : ℝ) :
    regularAd U (regularUnitary B t) = regularUnitary (conjugateFlow U B) t := by
  unfold RegularCovariantCore.regularUnitary
  rw [map_mul, regularAd_fibre, regularAd_shift]
  rfl

theorem generators_image (U : F ≃ₗᵢ[ℂ] F) (B : UnitaryFlow F)
    (M N : VonNeumannAlgebra F) (he : ∀ A : Op, A ∈ M ↔ U.conjStarAlgEquiv A ∈ N) :
    regularAd U '' generators B M = generators (conjugateFlow U B) N := by
  ext Z
  constructor
  · rintro ⟨C, (⟨b,hb,rfl⟩ | ⟨t,rfl⟩), rfl⟩
    · exact Or.inl ⟨_, (he b).mp hb, (regularAd_fibre U b).symm⟩
    · exact Or.inr ⟨t, (regularAd_flow U B t).symm⟩
  · rintro (⟨b,hb,rfl⟩ | ⟨t,rfl⟩)
    · let A := U.conjStarAlgEquiv.symm b
      have hA : A ∈ M := by
        apply (he A).mpr
        rw [show U.conjStarAlgEquiv A = b from U.conjStarAlgEquiv.apply_symm_apply b]
        exact hb
      refine ⟨fibre A, Or.inl ⟨A,hA,rfl⟩, ?_⟩
      rw [regularAd_fibre, show U.conjStarAlgEquiv A = b from U.conjStarAlgEquiv.apply_symm_apply b]
    · exact ⟨_, Or.inr ⟨t,rfl⟩, regularAd_flow U B t⟩

abbrev frameCore (L : generatedLorentz) (a : Point) : VonNeumannAlgebra (RegularHilbert F) :=
  RegularCovariantCore.core (H := F) (conjugateFlow (frameU L a) CanonicalFockRegular.fockFlow)
    (frameAlg L a)

theorem core_covariance_of (U : F ≃ₗᵢ[ℂ] F) (B : UnitaryFlow F)
    (M N : VonNeumannAlgebra F) (he : ∀ A : Op, A ∈ M ↔ U.conjStarAlgEquiv A ∈ N)
    (Z : RegOp) : Z ∈ core B M ↔ regularAd U Z ∈ core (conjugateFlow U B) N := by
  change Z ∈ generatedAlgebra (generators B M) ↔
    regularAd U Z ∈ generatedAlgebra (generators (conjugateFlow U B) N)
  rw [← generators_image U B M N he]
  exact (starEquiv_generated_transport _ _ _).symm

theorem core_covariance (L : generatedLorentz) (a : Point) (Z : RegOp) :
    Z ∈ CanonicalFockRegular.core ↔ regularAd (frameU L a) Z ∈ frameCore L a := by
  exact core_covariance_of _ _ _ _ (base_covariance L a) Z

theorem scalar_center_transport {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    [CompleteSpace H] (M N : VonNeumannAlgebra H)
    (e : (H →L[ℂ] H) ≃⋆ₐ[ℂ] (H →L[ℂ] H))
    (he : ∀ Y : H →L[ℂ] H, Y ∈ M ↔ e Y ∈ N)
    (h : ∀ Y : H →L[ℂ] H, Y ∈ M → Y ∈ M.commutant → ∃ c : ℂ, Y = c • 1)
    (Z : H →L[ℂ] H) (hz : Z ∈ N) (hz' : Z ∈ N.commutant) :
    ∃ c : ℂ, Z = c • 1 := by
  let X := e.symm Z
  have ex : e X = Z := e.apply_symm_apply Z
  have hx : X ∈ M := (he X).mpr (ex.symm ▸ hz)
  have hx' : X ∈ M.commutant := by
    apply VonNeumannAlgebra.mem_commutant_iff.mpr
    intro A hA
    apply e.injective
    change e (A*X) = e (X*A)
    simpa only [map_mul,ex] using
      (VonNeumannAlgebra.mem_commutant_iff.mp hz') (e A) ((he A).mp hA)
  obtain ⟨c,hc⟩ := h X hx hx'
  exact ⟨c, ex.symm.trans (by simp only [hc, map_smul, map_one])⟩

end K07.Horizon.TransportCenter
