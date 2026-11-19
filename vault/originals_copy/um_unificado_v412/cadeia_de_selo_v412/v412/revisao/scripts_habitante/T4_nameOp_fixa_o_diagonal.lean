import OHabitanteDoNome
set_option autoImplicit false
set_option linter.unusedSimpArgs false
open TGLExt.OHabitanteDoNome
open TGLExt.TraducaoTuring (opDaInstancia opDaInstancia_ofLp solucao_por_coordenadas selecao)
open scoped InnerProductSpace

/-- Na instancia de custo (v409), o operador do Nome do projetor no Nome FIXA toda grandeza diagonal `opDaInstancia d`
    (ela comuta com o projetor): nao e' a media classica de g dado o Nome (ela mexe nos pesos, esta nao mexe em nada). -/
theorem nameOp_fixa_o_diagonal {X : Type} [Fintype X] [DecidableEq X] (c d : X → ℕ) :
    TGLExt.nameOp (opDaInstancia c).ker.starProjection (opDaInstancia d) = opDaInstancia d := by
  have hp : (opDaInstancia c).ker.starProjection * (opDaInstancia c).ker.starProjection
      = (opDaInstancia c).ker.starProjection :=
    (Submodule.isIdempotentElem_starProjection (opDaInstancia c).ker).eq
  have hmor := (a_morada_e_o_que_comuta_com_o_posto hp (opDaInstancia d)).mpr
  have hcomm : (opDaInstancia c).ker.starProjection * opDaInstancia d
      = opDaInstancia d * (opDaInstancia c).ker.starProjection := by
    ext ψ y
    simp only [ContinuousLinearMap.mul_apply]
    rw [solucao_por_coordenadas, opDaInstancia_ofLp, solucao_por_coordenadas]
    simp only [opDaInstancia_ofLp]
    by_cases hy : c y = 0 <;> simp [hy, mul_comm]
  exact hmor hcomm

#print axioms nameOp_fixa_o_diagonal

/-- Contraste: o Nome de dois estados (X = Fin 2, c = 0, ou seja Nome = tudo): a seleção = estado normalizado; o ponto: com Nome = ⊤,
    `selecao` e' ψ/‖ψ‖ (a esperanca classica dado o evento certo e' a media de Born), e `nameOp 1` = identidade. -/
example : True := trivial
