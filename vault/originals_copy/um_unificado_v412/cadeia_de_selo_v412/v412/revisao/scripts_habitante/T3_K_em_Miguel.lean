import OHabitanteDoNome
set_option autoImplicit false
set_option linter.unusedSimpArgs false
open TGLExt.OHabitanteDoNome
open scoped InnerProductSpace

#check @TGLExt.thetaMiguel
#check @TGLExt.KEhATangente.K_sq_no_angulo_de_miguel

/-- PROPOSTA: a tangente da leitura e' o `K` da v407 no ANGULO DE MIGUEL do peso deixado fora do Nome, `β_v = ‖v − P v‖²/‖v‖²`
    (a mesma regra de leitura `thetaMiguel = arcsin √·`); nao usa `arctan` da propria grandeza. -/
theorem tangente_da_leitura_e_K_no_angulo_de_Miguel {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (N : Submodule ℂ H) [N.HasOrthogonalProjection] (v : H) (hP : N.starProjection v ≠ 0) :
    TGLExt.KEhATangente.K (TGLExt.thetaMiguel (‖v - N.starProjection v‖ ^ 2 / ‖v‖ ^ 2)) = tangenteDaLeitura N v := by
  have hpos : 0 < ‖N.starProjection v‖ := norm_pos_iff.mpr hP
  have hb := o_livro_do_testemunho_fecha N v
  have hvpos : 0 < ‖v‖ := by
    refine norm_pos_iff.mpr ?_
    intro h0
    apply hP
    rw [h0]
    simp
  obtain ⟨β, hβ⟩ : ∃ β : ℝ, β = ‖v - N.starProjection v‖ ^ 2 / ‖v‖ ^ 2 := ⟨_, rfl⟩
  rw [← hβ]
  have h0 : 0 ≤ β := by rw [hβ]; positivity
  have h1b : 1 - β = ‖N.starProjection v‖ ^ 2 / ‖v‖ ^ 2 := by
    rw [hβ]
    have hv2 : ‖v‖ ^ 2 ≠ 0 := by positivity
    field_simp
    linarith
  have h1 : β < 1 := by
    have : 0 < ‖N.starProjection v‖ ^ 2 / ‖v‖ ^ 2 := by positivity
    linarith
  have hsq := TGLExt.KEhATangente.K_sq_no_angulo_de_miguel h0 h1
  have hrhs : β / (1 - β) = (‖v - N.starProjection v‖ / ‖N.starProjection v‖) ^ 2 := by
    rw [h1b, hβ]
    have hv2 : ‖v‖ ^ 2 ≠ 0 := by positivity
    have hp2 : ‖N.starProjection v‖ ^ 2 ≠ 0 := by positivity
    rw [div_pow]
    field_simp
  have hK0 : 0 ≤ TGLExt.KEhATangente.K (TGLExt.thetaMiguel β) := by
    unfold TGLExt.KEhATangente.K TGLExt.thetaMiguel
    exact Real.tan_nonneg_of_nonneg_of_le_pi_div_two (Real.arcsin_nonneg.mpr (Real.sqrt_nonneg _)) (Real.arcsin_le_pi_div_two _)
  have ht0 : 0 ≤ tangenteDaLeitura N v := by unfold tangenteDaLeitura; positivity
  exact (sq_eq_sq₀ hK0 ht0).mp (hsq.trans hrhs)

#print axioms tangente_da_leitura_e_K_no_angulo_de_Miguel
