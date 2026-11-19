import TGLExt.TraducaoTuring

set_option autoImplicit false

/-! PONTE SUGERIDA (revisor, 14/11/2026): o teste que o leitor dos vizinhos aplica a uma leitura y (`c y = 0`) é o mesmo que a trava aplica:
    a trava deixa intacta a leitura y (o vetor da base em y) se e só se c y = 0, para todo tempo t > 0. -/

namespace TGLExt.NomeComoCodigo.Revisao
open TGLExt.TraducaoTuring

theorem a_trava_deixa_intacta_sse_o_custo_e_zero {X : Type} [Fintype X] [DecidableEq X] (c : X → ℕ) {t : ℝ} (ht : 0 < t) (y : X) :
    trava c t (EuclideanSpace.single y (1 : ℂ)) = EuclideanSpace.single y (1 : ℂ) ↔ c y = 0 := by
  constructor
  · intro h
    have h1 := congrArg (fun v : EuclideanSpace ℂ X => WithLp.ofLp v y) h
    simp only [trava_ofLp, PiLp.single_apply, if_true, mul_one] at h1
    by_contra hc
    have hpos : (0 : ℝ) < t * (c y : ℝ) := by
      have : (1 : ℝ) ≤ (c y : ℝ) := by exact_mod_cast Nat.one_le_iff_ne_zero.mpr hc
      nlinarith
    have hlt : Real.exp (-(t * (c y : ℝ))) < 1 := by
      have h0 := Real.exp_lt_exp.mpr (show -(t * (c y : ℝ)) < 0 by linarith)
      rwa [Real.exp_zero] at h0
    have h2 : Real.exp (-(t * (c y : ℝ))) = 1 := by exact_mod_cast h1
    linarith
  · intro h
    ext x
    rw [trava_ofLp]
    by_cases hx : x = y
    · subst hx; simp [h]
    · simp [hx]

end TGLExt.NomeComoCodigo.Revisao

#print axioms TGLExt.NomeComoCodigo.Revisao.a_trava_deixa_intacta_sse_o_custo_e_zero
