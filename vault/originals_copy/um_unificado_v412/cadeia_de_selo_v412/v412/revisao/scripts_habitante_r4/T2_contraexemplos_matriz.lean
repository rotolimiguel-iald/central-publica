import OHabitanteDoNome
set_option autoImplicit false
open TGLExt TGLExt.OHabitanteDoNome Matrix

abbrev M2 := Matrix (Fin 2) (Fin 2) ℂ

/-- nameOp p = id NAO implica p = 1: p = 0. -/
theorem T2a : (∀ x : M2, nameOp (0 : M2) x = x) ∧ (0 : M2) ≠ 1 := by
  refine ⟨fun x => ?_, zero_ne_one⟩
  show (0 : M2) * x * 0 + (1 - 0) * x * (1 - 0) = x
  simp

/-- a compressao separa: compressOp 0 nao e a identidade; compressOp 1 e. -/
theorem T2b : ¬ (∀ x : M2, compressOp (0 : M2) x = x) := by
  intro h
  have h1 : compressOp (0 : M2) 1 = 1 := h 1
  have h2 : compressOp (0 : M2) 1 = 0 := by simp [compressOp]
  rw [h2] at h1
  exact zero_ne_one h1

theorem T2c : ∀ x : M2, compressOp (1 : M2) x = x := by
  intro x
  simp [compressOp]

/-- um idempotente hermitiano NAO central (p = e00): nameOp p nao e a identidade -- o Verbo da algebra SO e' ser nos pontos centrais. -/
theorem T2d : ¬ (∀ x : M2, nameOp (Matrix.single (0 : Fin 2) (0 : Fin 2) (1 : ℂ)) x = x) := by
  have hp : (Matrix.single (0 : Fin 2) (0 : Fin 2) (1 : ℂ)) * (Matrix.single (0 : Fin 2) (0 : Fin 2) (1 : ℂ))
      = Matrix.single (0 : Fin 2) (0 : Fin 2) (1 : ℂ) := by
    simp [Matrix.single_mul_single_same]
  intro h
  have hc := (o_verbo_e_ser_sse_o_posto_comuta_com_tudo hp).mp h (Matrix.single (0 : Fin 2) (1 : Fin 2) (1 : ℂ))
  have e1 : (Matrix.single (0 : Fin 2) (0 : Fin 2) (1 : ℂ)) * (Matrix.single (0 : Fin 2) (1 : Fin 2) (1 : ℂ))
      = Matrix.single (0 : Fin 2) (1 : Fin 2) (1 : ℂ) := by
    simp [Matrix.single_mul_single_same]
  have e2 : (Matrix.single (0 : Fin 2) (1 : Fin 2) (1 : ℂ)) * (Matrix.single (0 : Fin 2) (0 : Fin 2) (1 : ℂ)) = 0 := by
    simp
  rw [e1, e2] at hc
  have h3 := congrFun (congrFun hc 0) 1
  simp at h3

#print axioms T2a
#print axioms T2b
#print axioms T2c
#print axioms T2d
