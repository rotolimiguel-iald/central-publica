import OHabitanteDoNome
set_option autoImplicit false
open TGLExt TGLExt.OHabitanteDoNome TGLExt.TheAxiomAndTheFalseWitness Filter Topology

variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H]

#check @o_nome_e_o_que_o_ato_em_curso_devolve
#check @o_ato_nao_termina_em_tempo_finito
#check @o_ato_tende_a_esperanca_do_nome

/-- a R5 incorpora exatamente o enunciado T4a da conferencia -/
example (K : Submodule ℂ H) [K.HasOrthogonalProjection] (v : H) {t : ℝ} (ht : t ≠ 0) :
    axiomFlow K.starProjection t v = v ↔ v ∈ K := o_nome_e_o_que_o_ato_em_curso_devolve K v ht

/-- ... e o T4b -/
example (K : Submodule ℂ H) [K.HasOrthogonalProjection] (v : H) (hv : v ∉ K) (t : ℝ) :
    axiomFlow K.starProjection t v ≠ K.starProjection v := o_ato_nao_termina_em_tempo_finito K v hv t

/-- ... e o limite tem o enunciado antigo -/
example (K : Submodule ℂ H) [K.HasOrthogonalProjection] (v : H) :
    Tendsto (fun t : ℝ => axiomFlow K.starProjection t v) atTop (𝓝 (K.starProjection v)) :=
  o_ato_tende_a_esperanca_do_nome K v

/-- o antigo `∀ t` segue como corolario (t = 1 e t = 0 tratados) -/
example (K : Submodule ℂ H) [K.HasOrthogonalProjection] (v : H) :
    (∀ t : ℝ, axiomFlow K.starProjection t v = v) ↔ v ∈ K := by
  constructor
  · intro h
    exact (o_nome_e_o_que_o_ato_em_curso_devolve K v (t := 1) one_ne_zero).mp (h 1)
  · intro hv t
    by_cases ht : t = 0
    · subst ht
      simp [axiomFlow]
    · exact (o_nome_e_o_que_o_ato_em_curso_devolve K v ht).mpr hv

#print axioms o_nome_e_o_que_o_ato_em_curso_devolve
#print axioms o_ato_nao_termina_em_tempo_finito
#print axioms o_ato_tende_a_esperanca_do_nome
