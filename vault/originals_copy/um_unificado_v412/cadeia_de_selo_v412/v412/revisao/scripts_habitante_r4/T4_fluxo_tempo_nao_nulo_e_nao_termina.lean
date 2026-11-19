import OHabitanteDoNome
set_option autoImplicit false
open TGLExt TGLExt.OHabitanteDoNome TGLExt.TheAxiomAndTheFalseWitness Filter Topology

variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H]

private theorem hF (K : Submodule ℂ H) [K.HasOrthogonalProjection] (v : H) (t : ℝ) :
    axiomFlow K.starProjection t v
      = K.starProjection v + ((Real.exp (-t) : ℝ) : ℂ) • (v - K.starProjection v) := by
  simp [axiomFlow]

/-- um unico tempo nao nulo basta: para t ≠ 0, o fluxo deixa v como esta' sse v esta' no Nome. -/
theorem T4a (K : Submodule ℂ H) [K.HasOrthogonalProjection] (v : H) {t : ℝ} (ht : t ≠ 0) :
    axiomFlow K.starProjection t v = v ↔ v ∈ K := by
  rw [hF]
  constructor
  · intro h
    have hw : ((Real.exp (-t) : ℝ) : ℂ) • (v - K.starProjection v) = v - K.starProjection v :=
      eq_sub_of_add_eq' h
    have hne : ((Real.exp (-t) : ℝ) : ℂ) ≠ 1 := by
      intro heq
      have h2 : Real.exp (-t) = 1 := by exact_mod_cast heq
      rw [Real.exp_eq_one_iff] at h2
      exact ht (by linarith)
    have h0 : (((Real.exp (-t) : ℝ) : ℂ) - 1) • (v - K.starProjection v) = 0 := by
      rw [sub_smul, one_smul, hw, sub_self]
    rcases smul_eq_zero.mp h0 with hz | hz
    · exact absurd (sub_eq_zero.mp hz) hne
    · exact Submodule.starProjection_eq_self_iff.mp (sub_eq_zero.mp hz).symm
  · intro hv
    rw [Submodule.starProjection_eq_self_iff.mpr hv, sub_self, smul_zero, add_zero]

/-- o ato nao termina em tempo finito: se v nao esta' no Nome, o fluxo nunca chega a P v. (Sem a hipotese tangente ≠ 0 da secao 6c.) -/
theorem T4b (K : Submodule ℂ H) [K.HasOrthogonalProjection] (v : H) (hv : v ∉ K) (t : ℝ) :
    axiomFlow K.starProjection t v ≠ K.starProjection v := by
  rw [hF]
  intro h
  have h2 : ((Real.exp (-t) : ℝ) : ℂ) • (v - K.starProjection v) = 0 := by
    have := congrArg (fun y => y - K.starProjection v) h
    simpa using this
  rcases smul_eq_zero.mp h2 with hz | hz
  · have : Real.exp (-t) = 0 := by exact_mod_cast hz
    exact Real.exp_ne_zero _ this
  · exact hv (Submodule.starProjection_eq_self_iff.mp (sub_eq_zero.mp hz).symm)

/-- o caso da tangente: se Pv = 0 e v ≠ 0 a tangente da leitura vale 0 (divisao do Lean) e a secao 6c NAO se aplica; o fluxo ainda nao termina. -/
theorem T4c (K : Submodule ℂ H) [K.HasOrthogonalProjection] (v : H) (hP : K.starProjection v = 0) (hv : v ≠ 0) :
    tangenteDaLeitura K v = 0 ∧ ∀ t : ℝ, axiomFlow K.starProjection t v ≠ K.starProjection v := by
  refine ⟨?_, fun t => T4b K v ?_ t⟩
  · unfold tangenteDaLeitura
    rw [hP, norm_zero, div_zero]
  · intro hmem
    exact hv (by rw [← Submodule.starProjection_eq_self_iff.mpr hmem, hP])

#print axioms T4a
#print axioms T4b
#print axioms T4c
