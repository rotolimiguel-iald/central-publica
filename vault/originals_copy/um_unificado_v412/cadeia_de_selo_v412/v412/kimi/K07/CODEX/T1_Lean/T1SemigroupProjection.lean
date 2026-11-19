import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Analysis.InnerProductSpace.Projection.Basic
import Mathlib.Topology.Instances.NNReal.Lemmas
import Mathlib.Tactic

/-! Strong convergence of a self-adjoint contraction semigroup. The midpoint
identity makes every orbit Cauchy without spectral calculus or time regularity. -/

set_option autoImplicit false
noncomputable section

namespace K07.T1

open Filter
open scoped Topology NNReal InnerProductSpace

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- The fixed subspace of the operators in the semigroup is the range of
the strong limit. No norm convergence of the operators is asserted. -/
theorem selfadjoint_semigroup_projection
    (T : ℝ≥0 → (H →L[ℂ] H)) (hcontract : ∀ t, ‖T t‖ ≤ 1)
    (hsa : ∀ t, IsSelfAdjoint (T t)) (hadd : ∀ s t, T (s + t) = T s * T t)
    (F : Submodule ℂ H) [F.HasOrthogonalProjection]
    (hF : ∀ y, y ∈ F ↔ ∀ t, T t y = y) (x : H) :
    Tendsto (fun t => T t x) atTop (𝓝 (F.starProjection x)) := by
  have comp (s t : ℝ≥0) (y : H) : T (s + t) y = T s (T t y) := by
    rw [hadd]
    rfl
  let energy (s : ℝ≥0) := ‖T s x‖ ^ 2
  have hanti : Antitone energy := by
    intro s t hst
    have hnorm : ‖T t x‖ ≤ ‖T s x‖ := by
      calc
        ‖T t x‖ = ‖T (t - s) (T s x)‖ := by
          rw [← comp, tsub_add_cancel_of_le hst]
        _ ≤ ‖T (t - s)‖ * ‖T s x‖ := (T (t - s)).le_opNorm _
        _ ≤ 1 * ‖T s x‖ := mul_le_mul_of_nonneg_right (hcontract _) (norm_nonneg _)
        _ = _ := one_mul _
    exact pow_le_pow_left₀ (norm_nonneg _) hnorm 2
  have lower : BddBelow (Set.range energy) :=
    ⟨0, fun _ ⟨t, ht⟩ => ht ▸ sq_nonneg ‖T t x‖⟩
  have midpoint (s t : ℝ≥0) :
      RCLike.re (inner ℂ (T s x) (T t x)) = energy ((s + t) / 2) := by
    let m := (s + t) / 2
    have hdouble : s + t = m + m := by dsimp [m]; ring
    calc
      RCLike.re (inner ℂ (T s x) (T t x)) = RCLike.re (inner ℂ x (T s (T t x))) :=
        congrArg (RCLike.re : ℂ → ℝ) ((hsa s).isSymmetric _ _)
      _ = RCLike.re (inner ℂ x (T m (T m x))) := by rw [← comp, hdouble, comp]
      _ = RCLike.re (inner ℂ (T m x) (T m x)) :=
        congrArg (RCLike.re : ℂ → ℝ) ((hsa m).isSymmetric _ _).symm
      _ = _ := inner_self_eq_norm_sq (𝕜 := ℂ) (T m x)
  have cauchy : CauchySeq (fun t => T t x) := by
    apply Metric.cauchySeq_iff.mpr
    intro ε hε
    have hnear : (⨅ t, energy t) < (⨅ t, energy t) + ε ^ 2 / 2 :=
      lt_add_of_pos_right _ (by positivity)
    have tail := (tendsto_atTop_ciInf hanti lower).eventually (gt_mem_nhds hnear)
    obtain ⟨N, hN⟩ := eventually_atTop.mp tail
    refine ⟨N, fun s hs t ht => ?_⟩
    rw [dist_eq_norm]
    apply (sq_lt_sq₀ (norm_nonneg _) hε.le).mp
    rw [norm_sub_sq (𝕜 := ℂ), midpoint]
    change energy s - 2 * energy ((s + t) / 2) + energy t < ε ^ 2
    have hs' : energy s < (⨅ u, energy u) + ε ^ 2 / 2 := hN s hs
    have ht' : energy t < (⨅ u, energy u) + ε ^ 2 / 2 := hN t ht
    linarith [ciInf_le lower ((s + t) / 2)]
  obtain ⟨z, hz⟩ := cauchySeq_tendsto_of_complete cauchy
  have fixed (r : ℝ≥0) : T r z = z := by
    have ht : Tendsto (fun t : ℝ≥0 => r + t) atTop atTop :=
      tendsto_atTop_mono (fun t => le_add_self) tendsto_id
    apply tendsto_nhds_unique ((T r).continuous.tendsto z |>.comp hz)
    simpa only [Function.comp_def, ← comp] using hz.comp ht
  have proj : F.starProjection x = z := by
    apply Submodule.eq_starProjection_of_mem_of_inner_eq_zero ((hF z).mpr fixed)
    intro y hy
    have hyFix := (hF y).mp hy
    have eqt (t : ℝ≥0) : inner ℂ (T t x) y = inner ℂ x y := by
      calc
        inner ℂ (T t x) y = inner ℂ x (T t y) := (hsa t).isSymmetric _ _
        _ = inner ℂ x y := by rw [hyFix t]
    have limEq : inner ℂ z y = inner ℂ x y := by
      apply tendsto_nhds_unique (hz.inner (tendsto_const_nhds (x := y)))
      simpa only [eqt] using (tendsto_const_nhds (f := (atTop : Filter ℝ≥0))
        (x := inner ℂ x y))
    rw [inner_sub_left, limEq, sub_self]
  rwa [proj]

#print axioms selfadjoint_semigroup_projection

/-- The same limit with real time on the half-line, as in the analytic statement. -/
theorem selfadjoint_semigroup_real_tendsto
    (T : ℝ → (H →L[ℂ] H)) (hcontract : ∀ t, 0 ≤ t → ‖T t‖ ≤ 1)
    (hsa : ∀ t, 0 ≤ t → IsSelfAdjoint (T t))
    (hadd : ∀ s t, 0 ≤ s → 0 ≤ t → T (s + t) = T s * T t)
    (F : Submodule ℂ H) [F.HasOrthogonalProjection]
    (hF : ∀ y, y ∈ F ↔ ∀ t, 0 ≤ t → T t y = y) (x : H) :
    Tendsto (fun t => T t x) atTop (𝓝 (F.starProjection x)) := by
  have hnn := selfadjoint_semigroup_projection (fun t : ℝ≥0 => T t)
    (fun t => hcontract t t.2) (fun t => hsa t t.2)
    (fun s t => hadd s t s.2 t.2) F (fun y => by
      rw [hF]
      exact ⟨fun h t => h t t.2, fun h t ht => h ⟨t, ht⟩⟩) x
  apply (hnn.comp Real.tendsto_toNNReal_atTop).congr'
  filter_upwards [eventually_ge_atTop (0 : ℝ)] with t ht
  dsimp only [Function.comp_apply]
  rw [Real.coe_toNNReal _ ht]

#print axioms selfadjoint_semigroup_real_tendsto

/-- Intrinsically constructed common fixed space, as an intersection of closed
equalizers. It exists for every family of bounded operators. -/
def fixedSubspace (T : ℝ≥0 → (H →L[ℂ] H)) : ClosedSubmodule ℂ H :=
  ⨅ t, (⟨(T t).toLinearMap.eqLocus (1 : H →ₗ[ℂ] H),
    isClosed_eq (T t).continuous continuous_id⟩ : ClosedSubmodule ℂ H)

/-- The intrinsic form has only contractivity, self-adjointness and the
semigroup law as assumptions on the operators. -/
theorem selfadjoint_semigroup_tendsto_fixedSubspace
    (T : ℝ≥0 → (H →L[ℂ] H)) (hcontract : ∀ t, ‖T t‖ ≤ 1)
    (hsa : ∀ t, IsSelfAdjoint (T t)) (hadd : ∀ s t, T (s + t) = T s * T t)
    (x : H) :
    Tendsto (fun t => T t x) atTop (𝓝 ((fixedSubspace T).toSubmodule.starProjection x)) := by
  apply selfadjoint_semigroup_projection T hcontract hsa hadd
  intro y
  change y ∈ fixedSubspace T ↔ _
  rw [fixedSubspace, ClosedSubmodule.mem_iInf]
  rfl

#print axioms selfadjoint_semigroup_tendsto_fixedSubspace

end K07.T1
