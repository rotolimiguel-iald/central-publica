import OHabitanteDoNome
set_option autoImplicit false
open TGLExt TGLExt.OHabitanteDoNome Matrix

#check @o_ato_de_ser_e_a_identidade_do_nome
#check @o_nome_em_ato_e_o_espelho_do_verbo
#check @o_par_compoe_o_projetor
#check @o_unico_ato_do_verbo_e_ser_fiel

section J
variable {n : Type} [Fintype n] [DecidableEq n]

/-- Leitura alternativa, so' com termos que o kernel ja tem: para um Nome da v405 (reflexo: Jconj P = P), o espelho J (LeftRight.Jconj,
    TheBireference.J_exchanges_the_references) leva a referencia esquerda `Lmul P` na direita `Rmul P`. -/
theorem T9a (N : Identidade.Nome n) (z : Matrix n n ℂ) :
    Jconj (Lmul N.P (Jconj z)) = Rmul N.P z := by
  rw [Jconj_Lmul_Jconj]
  have h : N.Pᴴ = N.P := N.reflexo
  rw [h]

/-- ... e o operador do Nome (o Verbo da algebra) e' feito das duas referencias: nameOp p = L_p R_p + L_{1-p} R_{1-p}. -/
theorem T9b (p z : Matrix n n ℂ) :
    nameOp p z = Lmul p (Rmul p z) + Lmul (1 - p) (Rmul (1 - p) z) := by
  simp [nameOp, Lmul, Rmul, mul_assoc]

/-- ... e as duas referencias de um Nome se espelham: R_P = J L_P J, com o par (L_P, R_P) compondo o Verbo. -/
theorem T9c (N : Identidade.Nome n) (z : Matrix n n ℂ) :
    nameOp N.P z = Lmul N.P (Jconj (Lmul N.P (Jconj z))) + Lmul (1 - N.P) (Jconj (Lmul (1 - N.P) (Jconj z))) := by
  have h1 : N.Pᴴ = N.P := N.reflexo
  have h2 : (1 - N.P)ᴴ = 1 - N.P := by
    rw [Matrix.conjTranspose_sub, Matrix.conjTranspose_one, h1]
  rw [T9b, Jconj_Lmul_Jconj, Jconj_Lmul_Jconj, h1, h2]
end J

#print axioms T9a
#print axioms T9b
#print axioms T9c
