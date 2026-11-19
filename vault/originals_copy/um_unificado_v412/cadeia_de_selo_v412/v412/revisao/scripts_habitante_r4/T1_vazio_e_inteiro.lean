import OHabitanteDoNome
set_option autoImplicit false
open TGLExt TGLExt.OHabitanteDoNome

/-! (i) O Verbo do vazio (posto 0) e o do inteiro (posto 1) sao o mesmo mapa, a identidade, em todo anel. -/
section
variable {R : Type*} [Ring R]

theorem T1a (x : R) : nameOp (0 : R) x = x := by
  show (0 : R) * x * 0 + (1 - 0) * x * (1 - 0) = x
  simp

theorem T1b (x : R) : nameOp (1 : R) x = x := o_ato_do_um_e_ser x

theorem T1c (x : R) : nameOp (0 : R) x = nameOp (1 : R) x := by
  rw [T1a, T1b]

/-- a instancia pedida: o_verbo_nao_distingue_a_face_do_resto em p = 1 -/
theorem T1d (x : R) : nameOp (0 : R) x = nameOp (1 : R) x := by
  have h := o_verbo_nao_distingue_a_face_do_resto (1 : R) x
  rwa [sub_self] at h
end

#print axioms T1a
#print axioms T1b
#print axioms T1c
#print axioms T1d
