import OHabitanteDoNome
set_option autoImplicit false
open TGLExt TGLExt.OHabitanteDoNome

/-- Sem idempotencia: p = -1 em ℂ da' compressao = identidade e p ≠ 1. -/
theorem T3a : (∀ x : ℂ, compressOp (-1 : ℂ) x = x) ∧ (-1 : ℂ) ≠ 1 ∧ ¬ ((-1 : ℂ) * (-1) = -1) := by
  refine ⟨fun x => ?_, ?_, ?_⟩
  · show (-1 : ℂ) * x * (-1) = x
    ring
  · norm_num
  · norm_num

/-- A caracterizacao exata sem hp: compressao = identidade <-> p*p = 1 e p central. Com hp (p*p = p) isto da' p = 1. -/
theorem T3b {R : Type*} [Ring R] (p : R) :
    (∀ x, compressOp p x = x) ↔ (p * p = 1 ∧ ∀ x, p * x = x * p) := by
  constructor
  · intro h
    have h1 : p * p = 1 := by
      have := h 1
      simpa [compressOp] using this
    refine ⟨h1, fun x => ?_⟩
    have hx := h x
    simp only [compressOp] at hx
    calc p * x = p * (p * x * p) := by rw [hx]
      _ = (p * p) * x * p := by simp only [mul_assoc]
      _ = x * p := by rw [h1, one_mul]
  · rintro ⟨h1, hc⟩ x
    show p * x * p = x
    rw [hc x, mul_assoc, h1, mul_one]

#print axioms T3a
#print axioms T3b
