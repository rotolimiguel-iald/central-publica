import OHabitanteDoNome
set_option autoImplicit false
open TGLExt TGLExt.OHabitanteDoNome TGLExt.TheAxiomAndTheFalseWitness Filter Topology

variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H]

/-- o_ato_levado_ao_fim_e_a_esperanca sai em uma linha de axiomFlow_tendsto_the_post (limite em norma de operadores => limite ponto a ponto). -/
theorem T7a (K : Submodule ℂ H) [K.HasOrthogonalProjection] (v : H) :
    Tendsto (fun t : ℝ => axiomFlow K.starProjection t v) atTop (𝓝 (K.starProjection v)) :=
  ((ContinuousLinearMap.apply ℂ H v).continuous.tendsto _).comp (axiomFlow_tendsto_the_post K.starProjection)

/-- [Nonempty n] e' NECESSARIO em a_identidade_e_o_verbo_ser_sem_o_vazio: com n = Fin 0 o enunciado e' falso. -/
theorem T7b : ¬ (Identidade.euSou (Fin 0) = Identidade.oQueSou (Identidade.vazio (Fin 0)) ↔
    ((∀ x : Matrix (Fin 0) (Fin 0) ℂ, nameOp (Identidade.vazio (Fin 0)).P x = x) ∧ (Identidade.vazio (Fin 0)).P ≠ 0)) := by
  intro h
  have hL : Identidade.euSou (Fin 0) = Identidade.oQueSou (Identidade.vazio (Fin 0)) := by
    unfold Identidade.euSou Identidade.oQueSou
    rw [Identidade.gibbs_absolute, Identidade.gibbs_absolute]
    have : (1 : Matrix (Fin 0) (Fin 0) ℂ) = (Identidade.vazio (Fin 0)).P := Subsingleton.elim _ _
    rw [this]
  have hR := (h.mp hL).2
  exact hR (Subsingleton.elim _ _)

#print axioms T7a
#print axioms T7b
