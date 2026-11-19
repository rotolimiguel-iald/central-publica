import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Analysis.Normed.Module.FiniteDimension

/-! Revisor V_B1_a: em dimensao FINITA as hipoteses de `o_fixo_de_uma_dilatacao_e_fixo_da_translacao`
(covariancia com um fator `|q| < 1`, continuidade forte em 0, `T 0 = 1`) forcam `T a = 1`. -/

set_option autoImplicit false
set_option maxHeartbeats 1000000

open Filter Topology
open scoped InnerProductSpace

namespace TesteDim

theorem em_dimensao_finita_a_translacao_e_trivial
    {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [FiniteDimensional ℂ H]
    (U : H →L[ℂ] H) (T : ℝ → H →L[ℂ] H) (q : ℝ) (hq : |q| < 1)
    (hU : ∀ v w, ⟪U v, U w⟫_ℂ = ⟪v, w⟫_ℂ) (h0 : ∀ v, T 0 v = v)
    (hcont : ∀ v, ContinuousAt (fun a => T a v) 0)
    (hcov : ∀ a v, U (T a v) = T (q * a) (U v)) (a : ℝ) (v : H) :
    T a v = v := by
  have hUn : ∀ w, ‖U w‖ = ‖w‖ := by
    intro w
    have h2 : ‖U w‖ ^ 2 = ‖w‖ ^ 2 := by
      have := congrArg RCLike.re (hU w w)
      rwa [inner_self_eq_norm_sq, inner_self_eq_norm_sq] at this
    exact (sq_eq_sq₀ (norm_nonneg _) (norm_nonneg _)).mp h2
  have hUpow : ∀ (n : ℕ) w, ‖(U ^ n) w‖ = ‖w‖ := by
    intro n
    induction n with
    | zero => intro w; simp
    | succ n ih => intro w; rw [pow_succ, ContinuousLinearMap.mul_apply, ih, hUn]
  have hcovn : ∀ (n : ℕ) (b : ℝ) w, (U ^ n) (T b w) = T (q ^ n * b) ((U ^ n) w) := by
    intro n
    induction n with
    | zero => intro b w; simp
    | succ n ih =>
      intro b w
      have e : q ^ (n + 1) * b = q ^ n * (q * b) := by ring
      rw [pow_succ, ContinuousLinearMap.mul_apply, hcov, ih, e, ContinuousLinearMap.mul_apply]
  have hTc : ContinuousAt T 0 := continuousAt_clm_apply.mpr hcont
  have hT0 : T 0 = 1 := by
    ext w
    simp [h0]
  have hq' : Tendsto (fun n : ℕ => q ^ n * a) atTop (𝓝 0) := by
    simpa using (tendsto_pow_atTop_nhds_zero_of_abs_lt_one hq).mul_const a
  have hlim : Tendsto (fun n : ℕ => T (q ^ n * a)) atTop (𝓝 1) := by
    rw [← hT0]
    exact hTc.tendsto.comp hq'
  have hbound : ∀ n : ℕ, ‖T a v - v‖ ≤ ‖T (q ^ n * a) - 1‖ * ‖v‖ := by
    intro n
    have h1 : ‖T a v - v‖ = ‖(U ^ n) (T a v - v)‖ := (hUpow n _).symm
    have h2 : (U ^ n) (T a v - v) = (T (q ^ n * a) - 1) ((U ^ n) v) := by
      rw [map_sub, hcovn n a v, ContinuousLinearMap.sub_apply, ContinuousLinearMap.one_apply]
    rw [h1, h2]
    calc ‖(T (q ^ n * a) - 1) ((U ^ n) v)‖
        ≤ ‖T (q ^ n * a) - 1‖ * ‖(U ^ n) v‖ := ContinuousLinearMap.le_opNorm _ _
      _ = ‖T (q ^ n * a) - 1‖ * ‖v‖ := by rw [hUpow]
  have hnorm : Tendsto (fun n : ℕ => ‖T (q ^ n * a) - 1‖) atTop (𝓝 0) :=
    tendsto_iff_norm_sub_tendsto_zero.mp hlim
  have hlim2 : Tendsto (fun n : ℕ => ‖T (q ^ n * a) - 1‖ * ‖v‖) atTop (𝓝 0) := by
    simpa using hnorm.mul_const ‖v‖
  have hle : ‖T a v - v‖ ≤ 0 := ge_of_tendsto' hlim2 hbound
  exact sub_eq_zero.mp (norm_le_zero_iff.mp hle)

end TesteDim

#print axioms TesteDim.em_dimensao_finita_a_translacao_e_trivial
