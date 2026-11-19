import TGLExt.TowerWedgeIndex
import TGLExt.WedgeHorizonObserver
import TGLExt.F1Fecho394.CanonicalFockFaithfulWeightR2

/-! The flow-of-weights criterion for a factor in standard vector form.
The vector, its Tomita graph, the implementing flow and the represented
crossed product are specified in the predicate. No Connes invariant is
postulated. All geometric readouts below use the same physical boost. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace Vinculo
open TGL.SpecificAQFT F1Rede.BosonicFock TGLV350.Regular
open TGLExt TGLExt.ImportedSQ TGLExt.ContratoQGv31 ChatgptAudit
open F1Fecho.CanonicalFockModularCoreInputR1 (physicalFockCertificate)
open F1Fecho.RegularCovariantCore
open K07.TowerWedge K07.Horizon

def HasScalarCenter {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    [CompleteSpace H] (A : VonNeumannAlgebra H) : Prop :=
  ∀ z : H →L[ℂ] H, z ∈ A → z ∈ A.commutant → ∃ c : ℂ, z = c • (1 : H →L[ℂ] H)

/-- Type III₁ by the continuous-core characterization of Connes–Takesaki,
in a cyclic and separating representation. The choice of vector is existential. -/
def IsTypeIII1 {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    [CompleteSpace H] (A : VonNeumannAlgebra H) : Prop :=
  HasScalarCenter A ∧ ∃ (Ω : H) (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (B : UnitaryFlow H),
    ‖Ω‖ = 1 ∧
    Dense ((Submodule.span ℂ ((fun z : H →L[ℂ] H => z Ω) '' (A : Set (H →L[ℂ] H)))) : Set H) ∧
    (∀ z : H →L[ℂ] H, z ∈ A → z Ω = 0 → z = 0) ∧
    ORDEM016.D6.PairTomitaAnalyticRealizationMeasured A.toStarSubalgebra Ω J B.U ∧
    (∀ t z, automorphism B t z ∈ A ↔ z ∈ A) ∧
    HasScalarCenter (core B A)

/-- One matrix unit of the index gives a single rapidity. The same rapidity
fixes the two null-coordinate multipliers, the vacuum modular time acting on
the quantum null translation, and what a positive-radius observer reads. -/
def ReadsTowerOnWedge (N : ℕ) (i j : chainIdx N) : Prop :=
  let s := rapidity mixProfile N i j
  let ratio := localEigenvalue mixProfile N i j
  (∀ x : Point, u (wedgeBoostMap s x) = ratio * u x ∧
    v (wedgeBoostMap s x) = ratio⁻¹ * v x) ∧
  (∀ l : ℝ, (lightDelta physicalFockCertificate (modularTime s)).conjStarAlgEquiv
    ((lightNet physicalFockCertificate).U (l • nullDir)) =
    (lightNet physicalFockCertificate).U ((ratio * l) • nullDir)) ∧
  (∀ ρ y z : ℝ, 0 < ρ →
    let x := wedgeBoostMap s ![0,ρ,y,z]
    Real.log (u x / v x) / 2 = s)

theorem tower_observer_diagram (N : ℕ) (i j : chainIdx N) : ReadsTowerOnWedge N i j := by
  dsimp only [ReadsTowerOnWedge]
  refine ⟨?_, indexed_modular_translation physicalFockCertificate mixProfile N i j, ?_⟩
  · intro x
    have h := boost_read (rapidity mixProfile N i j) x
    rw [Real.exp_neg,exp_rapidity] at h
    exact ⟨h.1,h.2.1⟩
  · intro ρ y z hρ
    exact (observer_recovers_rapidity ρ _ y z hρ).2

end Vinculo
