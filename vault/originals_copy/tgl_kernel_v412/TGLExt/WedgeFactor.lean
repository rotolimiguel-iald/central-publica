import TGLExt.F1Fecho394.CanonicalFockModularCoreInputR1
import TGLExt.F1Fecho394.CanonicalFockRegularCoreR2
import TGLExt.QGReaderUVLock
import TGLExt.V351ModularFixedVectors

/-! The centre of the Maxwell wedge from the Tomita graph of its vacuum.
The half-eigenvector calculation below specializes the existing calculation
in TGLExt.V351ModularFixedVectors to the actual Weyl vacuum resolvent. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
namespace Vinculo.WedgeFactor
open TGLExt ChatgptAudit TGLV350.Regular F1Rede.BosonicFock
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockPolar ORDEM016.D6
open F1Fecho.CanonicalFockModularCoreInputR1 (physicalFockCertificate)

private theorem phase_at_half {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H]
    (T : H →L[ℂ] H) (hT : IsSelfAdjoint T) (x : H)
    (hx : T x = (1/2 : ℂ) • x) (t : ℝ) :
    resolventPhaseOperator T t x = (1/4 : ℂ) • x := by
  by_cases hz : x = 0
  · simp [hz]
  let L : H →L[ℂ] H := InnerProductSpace.rankOne ℂ x x
  let Q : H →L[ℂ] H := algebraMap ℂ (H →L[ℂ] H) (1/2)
  have hQ : IsSelfAdjoint Q := by
    change star (algebraMap ℂ (H →L[ℂ] H) (1/2)) = _
    rw [← algebraMap_star_comm]
    norm_num [Q]
  have hL : T*L = L*Q := by
    ext1 y
    change T ((inner ℂ x y) • x) =
      (inner ℂ x ((1/2 : ℂ) • y)) • x
    rw [map_smul,hx,inner_smul_right,smul_smul]
    congr 1
    ring
  have hp : resolventPhaseOperator Q t =
      algebraMap ℂ (H →L[ℂ] H) (1/4) := by
    change cfc (fun z : ℂ => resolventPhaseFunction t z.re)
      (algebraMap ℂ (H →L[ℂ] H) (1/2)) = _
    rw [cfc_algebraMap]
    congr 1
    norm_num [resolventPhaseFunction,resolventDamping,modularPhase]
  have he := congrArg (fun B : H →L[ℂ] H => B x)
    (resolventPhaseOperator_intertwines T Q L hT hQ hL t)
  rw [hp] at he
  change resolventPhaseOperator T t ((inner ℂ x x) • x) =
    (inner ℂ x ((1/4 : ℂ) • x)) • x at he
  rw [map_smul,inner_smul_right] at he
  apply smul_right_injective H (inner_self_ne_zero.mpr hz : inner ℂ x x ≠ 0)
  calc
    _ = ((1/4 : ℂ) * inner ℂ x x) • x := he
    _ = _ := by
      dsimp only
      rw [smul_smul,mul_comm]

abbrev Op := F →L[ℂ] F

/-- The vacuum trace identity for z* puts (zΩ,zΩ) in the graph of S*S. -/
theorem vacuum_square_fixed (z : Op) (hz : z ∈ M)
    (hω : ∀ a ∈ M, inner ℂ vacuum ((star z) (a vacuum)) =
      inner ℂ vacuum (a ((star z) vacuum))) :
    (z vacuum, z vacuum) ∈ antilinearSquareGraph actualGraph := by
  refine ⟨(star z) vacuum, subset_closure ⟨z, hz, rfl⟩, ?_⟩
  intro y sy hy
  let K : Set (F × F) := {p | inner ℂ (z vacuum) p.1 = inner ℂ p.2 ((star z) vacuum)}
  have hclosed : IsClosed K := isClosed_eq
    (continuous_const.inner continuous_fst) (continuous_snd.inner continuous_const)
  apply (closure_minimal (t := K) ?_ hclosed) hy
  rintro _ ⟨a, ha, rfl⟩
  change inner ℂ (z vacuum) (a vacuum) = inner ℂ ((star a) vacuum) ((star z) vacuum)
  rw [← z.adjoint_inner_right, ContinuousLinearMap.star_eq_adjoint a, a.adjoint_inner_left]
  exact hω a ha

theorem vacuum_trace_scalar (z : Op) (hz : z ∈ M)
    (hω : ∀ a ∈ M, inner ℂ vacuum ((star z) (a vacuum)) =
      inner ℂ vacuum (a ((star z) vacuum))) : ∃ c : ℂ, z = c • (1 : Op) := by
  let x := z vacuum
  have hinv := modularR_inverse x x (vacuum_square_fixed z hz hω)
  have hx : modularR x = (1/2 : ℂ) • x := by
    have hh := congrArg (fun y : F => (1/2 : ℂ) • y) hinv
    rw [map_add, ← two_smul ℂ, smul_smul] at hh
    norm_num at hh
    exact hh
  have hd : resolventDampingOperator modularR x = (1/4 : ℂ) • x := by
    change modularR (x - modularR x) = _
    rw [map_sub, hx, map_smul, hx, smul_smul, ← sub_smul]
    norm_num
  have fixed (t : ℝ) : TGLExt.ImportedSQ.lightDelta physicalFockCertificate t x = x := by
    have hp := phase_at_half modularR (IsSelfAdjoint.of_nonneg modularR_nonneg) x hx t
    have he := actualModularFlow_readout t x
    rw [hd, hp, map_smul] at he
    have hf := smul_right_injective F (by norm_num : (1/4 : ℂ) ≠ 0) he
    exact (F1Fecho.CanonicalFockBW.actualModularFlow_eq_gamma_apply t x).symm.trans hf
  obtain ⟨c,hc⟩ := Submodule.mem_span_singleton.mp
    ((TGLExt.QGReaderUVLock.light_modular_fixed_iff_vacuum physicalFockCertificate x).mp fixed)
  refine ⟨c, sub_eq_zero.mp (F1Fecho.WedgeCyclic.canonical_wedge_separating
    (z-c • (1 : Op)) (M.sub_mem hz (M.smul_mem M.one_mem c)) ?_)⟩
  change z vacuum - c • vacuum = 0
  exact sub_eq_zero.mpr hc.symm

private theorem central_state_identity {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] (A : VonNeumannAlgebra H) (Ω : H)
    (z : H →L[ℂ] H) (hz : z ∈ A.commutant) (a : H →L[ℂ] H) (ha : a ∈ A) :
    inner ℂ Ω ((star z) (a Ω)) = inner ℂ Ω (a ((star z) Ω)) := by
  have hs : star z ∈ A.commutant := A.commutant.toStarSubalgebra.star_mem' hz
  have hc : a * star z = star z * a :=
    (VonNeumannAlgebra.mem_commutant_iff (S := A) (z := star z)).mp hs a ha
  change inner ℂ Ω ((star z * a) Ω) = inner ℂ Ω ((a * star z) Ω)
  rw [hc]

theorem wedge_center_scalar (z : Op) (hz : z ∈ M) (hz' : z ∈ M.commutant) :
    ∃ c : ℂ, z = c • (1 : Op) :=
  vacuum_trace_scalar z hz (central_state_identity M vacuum z hz')

end Vinculo.WedgeFactor
