import TGLExt.ONomeEBeta
/-!
# Relógio inteiro fixado pelo acoplamento

A especialização do relógio real de `OPolinomioFixoEBeta` usa uma constante
natural m, fixada antes da fórmula.
`clock m n` é computável por aritmética natural; a existência de m é provada.
A escolha a partir de um real arbitrário não é apresentada como algoritmo.
Isto conta passos do fator 1-beta, não passos de uma máquina de fita.
-/

namespace Codex.RelogioBeta

open TGLExt TGLExt.TraducaoTuring

def clock (m n : ℕ) : ℕ := m * (n + 2)

theorem fixed_slope_exists (c : TGLCoupling) :
    ∃ m : ℕ, Real.log 2 / c.beta < (m : ℝ) :=
  exists_nat_gt _

theorem clock_sufficient (c : TGLCoupling) (m : ℕ)
    (hm : Real.log 2 / c.beta < (m : ℝ)) (n : ℕ) :
    ((n : ℝ) + 2) * Real.log 2 / c.beta < (clock m n : ℝ) := by
  have h := mul_lt_mul_of_pos_left hm (by positivity : (0 : ℝ) < (n : ℝ) + 2)
  calc
    _ = ((n : ℝ) + 2) * (Real.log 2 / c.beta) := by ring
    _ < ((n : ℝ) + 2) * (m : ℝ) := h
    _ = (clock m n : ℝ) := by simp [clock]; ring

theorem clock_affine (m n : ℕ) : clock m n = m * n + 2 * m := by
  unfold clock
  ring

theorem clock_succ (m n : ℕ) : clock m (n + 1) = clock m n + m := by
  unfold clock
  ring

theorem clock_polynomial_bound (m n : ℕ) : clock m n ≤ (2 * m) * (n + 1) := by
  unfold clock
  nlinarith

theorem one_clock_all_formulas (c : TGLCoupling) (m : ℕ)
    (hm : Real.log 2 / c.beta < (m : ℝ)) (n : ℕ) :
    ∀ φ : CNF n, (SAT φ ↔ 1 ≤ ∑ x : Fin n → Bool,
      (1 - c.beta) ^ (clock m n * custoCNF φ x)) := by
  apply TGLExt.ONomeEBeta.a_resolucao_e_pelo_passo_do_nome c n (clock m n)
  have hk := clock_sufficient c m hm n
  have hl : 0 < Real.log (2 : ℝ) := Real.log_pos (by norm_num)
  have hb := c.beta_pos
  have hh : (n : ℝ) * Real.log 2 / c.beta <
      ((n : ℝ) + 2) * Real.log 2 / c.beta := by
    apply (div_lt_div_iff_of_pos_right hb).2
    nlinarith
  exact hh.trans hk

end Codex.RelogioBeta
