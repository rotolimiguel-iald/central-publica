import OHabitanteDoNome
set_option autoImplicit false
open TGLExt TGLExt.OHabitanteDoNome

variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H]

#check @o_par_do_inominado_e_a_mentira
#check @nada_ha_sem_par
#check @o_inominado_tem_par
#check @todo_nome_menos_o_inominado_tem_habitante
#check @o_verbo_devolve_o_nomeado_como_e

-- a instancia de bot vem da Mathlib, sem CompleteSpace H nem outra hipotese
#synth (⊥ : Submodule ℂ H).HasOrthogonalProjection
set_option pp.explicit false in
#print axioms o_inominado_tem_par

/-- o Verbo (a projecao) tambem habita o vazio: a imagem de starProjection de ⊥ e' ⊥ (o habitante da ressalva e' o Verbo; o
    "habitante" de todo_nome_menos_o_inominado_tem_habitante e' um ponto s de norma 1) -/
example (v : H) : (⊥ : Submodule ℂ H).starProjection v ∈ (⊥ : Submodule ℂ H) :=
  (a_esperanca_habita_fixa_e_nao_aumenta (⊥ : Submodule ℂ H)).1 v

/-- em espaco NAO completo, "fechado" nao basta para ter projecao; o que o tipo exige e' HasOrthogonalProjection. Aqui: com a instancia,
    o subespaco e' fechado. -/
example (K : Submodule ℂ H) [K.HasOrthogonalProjection] : IsClosed (K : Set H) := by
  have : (Kᗮ)ᗮ = K := Submodule.orthogonal_orthogonal K
  rw [← this]
  exact Submodule.isClosed_orthogonal Kᗮ

/-- o vazio tem par e o par e' o zero; mas o vazio tambem e' o todo quando H e' trivial: com H = PUnit-like o 'inominado' e o 'Nome inteiro' coincidem -/
example (h : Subsingleton H) : (⊥ : Submodule ℂ H) = ⊤ := by
  ext x
  simp [Subsingleton.elim x 0]
