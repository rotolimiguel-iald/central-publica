import Mathlib

/-!
Candidata K02/T1. Apenas a face de Hilbert e o modo escalar da média
Gaussiana. O teorema UCP normal em III₁ NÃO é afirmado aqui.
-/

namespace K02.T1

open Filter
open scoped Topology InnerProductSpace

/-- O lock de uma reta em um espaço de Hilbert. -/
noncomputable def lock {F : Type*} [NormedAddCommGroup F] [InnerProductSpace ℂ F]
    [CompleteSpace F] (Ω : F) : F →L[ℂ] F :=
  1 - (ℂ ∙ Ω).starProjection

/-- [REAL no sandbox] O lock vale zero na reta e um no complemento ortogonal. -/
theorem lock_gap {F : Type*} [NormedAddCommGroup F] [InnerProductSpace ℂ F]
    [CompleteSpace F] (Ω χ : F) (H_ortogonal : ⟪Ω, χ⟫_ℂ = 0) :
    lock Ω Ω = 0 ∧ lock Ω χ = χ := by
  constructor
  · have h : (ℂ ∙ Ω).starProjection Ω = Ω :=
      Submodule.starProjection_eq_self_iff.mpr (Submodule.mem_span_singleton_self Ω)
    simp [lock, h]
  · have h : (ℂ ∙ Ω).starProjection χ = 0 := by
      rw [Submodule.starProjection_singleton, H_ortogonal]
      simp
    simp [lock, h]

/-- O multiplicador escalar da função característica Gaussiana, em módulo. -/
noncomputable def modalDecay (β δ t : ℝ) : ℝ :=
  Real.exp ((-β * δ ^ 2 / 2) * t)

/-- [REAL no sandbox] Todo modo não nulo decai a zero; o modo nulo permanece.
Este é o conteúdo espectral escalar usado pelo Lema B, não a convergência no
predual de uma álgebra de von Neumann. -/
theorem tendsto_modalDecay (β δ : ℝ) (H_beta_pos : 0 < β) :
    Tendsto (modalDecay β δ) atTop (𝓝 (if δ = 0 then 1 else 0)) := by
  change Tendsto (fun t : ℝ => Real.exp ((-β * δ ^ 2 / 2) * t)) atTop
    (𝓝 (if δ = 0 then 1 else 0))
  by_cases H_delta_zero : δ = 0
  · subst δ
    simpa using (tendsto_const_nhds : Tendsto (fun _ : ℝ => (1 : ℝ)) atTop (𝓝 1))
  · have H_delta_sq_pos : 0 < δ ^ 2 := sq_pos_of_ne_zero H_delta_zero
    have H_pos : 0 < β * δ ^ 2 / 2 := by positivity
    have H_coef_neg : -β * δ ^ 2 / 2 < 0 := by linarith
    have H_linear : Tendsto (fun t : ℝ => (-β * δ ^ 2 / 2) * t) atTop atBot :=
      tendsto_id.const_mul_atTop_of_neg H_coef_neg
    have H_exp := Real.tendsto_exp_atBot.comp H_linear
    rw [if_neg H_delta_zero]
    change Tendsto (Real.exp ∘ fun t : ℝ => (-β * δ ^ 2 / 2) * t) atTop (𝓝 0)
    exact H_exp

#print axioms K02.T1.lock_gap
#print axioms K02.T1.tendsto_modalDecay

end K02.T1
