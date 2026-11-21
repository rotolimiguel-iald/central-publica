import TGLExt.RelogioBeta
import TGLExt.LeituraBeta
import TGLExt.Reconstrucao
/-!
# Da leitura aproximada aos rótulos da solução

Todas as leis de aproximação permanecem hipóteses.
O produtor `reader` é parâmetro, com sua precisão expressa em `hr`; este módulo não o implementa nem demonstra seu
custo de execução, e não há hipótese escondida de tempo.
Um produtor de aproximações precisa de implementação e prova de custo próprias.
O formato diádico abaixo torna explícita uma precisão suficiente e um teste
inteiro. Tamanho da resposta e custo de produzi-la são medidas diferentes.
-/

namespace Codex.PonteLeituraBeta

open TGLExt TGLExt.TraducaoTuring Codex.RelogioBeta Codex.LeituraBeta

variable {n : ℕ}

def betaDecision (reader : CNF n → ℚ) (φ : CNF n) : Bool := readBit (reader φ)

theorem betaDecision_correct (c : TGLCoupling) (m : ℕ)
    (hm : Real.log 2 / c.beta < (m : ℝ)) (reader : CNF n → ℚ)
    (hr : ∀ φ, |(reader φ : ℝ) - weightedSum c (clock m n) φ| ≤ 1 / 4)
    (φ : CNF n) : betaDecision reader φ = true ↔ SAT φ :=
  readBit_correct c (clock m n) φ (clock_sufficient c m hm n) (reader φ) (hr φ)

theorem reconstruction_from_beta (c : TGLCoupling) (m : ℕ)
    (hm : Real.log 2 / c.beta < (m : ℝ)) (reader : CNF n → ℚ)
    (hr : ∀ φ, |(reader φ : ℝ) - weightedSum c (clock m n) φ| ≤ 1 / 4)
    (φ : CNF n) :
    ((Reconstrucao.solve (betaDecision reader) φ).1 = none ↔ ¬ SAT φ) ∧
    (∀ x, (Reconstrucao.solve (betaDecision reader) φ).1 = some x →
      Reconstrucao.Good φ x) ∧
    (Reconstrucao.solve (betaDecision reader) φ).2 ≤ n + 1 :=
  Reconstrucao.solve_correct _ (betaDecision_correct c m hm reader hr) φ

/-- n+2 posições fracionárias, mais o extremo 1, representado por 2^(n+2). -/
def dyadic (n j : ℕ) : ℚ := (j : ℚ) / (2 : ℚ) ^ (n + 2)

theorem dyadic_comparison (n j : ℕ) :
    normalizedReadBit n (dyadic n j) = decide (2 ≤ j) := by
  have hp : (0 : ℚ) < (2 : ℚ) ^ n := by positivity
  have hd : (2 : ℚ) ^ (n + 2) = 4 * (2 : ℚ) ^ n := by rw [pow_add]; ring
  have hiff : 1 / (2 * (2 : ℚ) ^ n) ≤ dyadic n j ↔ 2 ≤ j := by
    unfold dyadic
    rw [hd]
    have ha : 1 / (2 * (2 : ℚ) ^ n) = 2 / (4 * (2 : ℚ) ^ n) := by ring
    rw [ha, div_le_div_iff_of_pos_right (by positivity)]
    exact_mod_cast Iff.rfl
  simp only [normalizedReadBit, hiff]

theorem dyadic_correct (c : TGLCoupling) (m : ℕ)
    (hm : Real.log 2 / c.beta < (m : ℝ)) (φ : CNF n) (j : ℕ)
    (hj : |(dyadic n j : ℝ) - normalizedSum c (clock m n) φ| ≤
      1 / (4 * (2 : ℝ) ^ n)) :
    decide (2 ≤ j) = true ↔ SAT φ := by
  rw [← dyadic_comparison n j]
  exact normalizedReadBit_correct c (clock m n) φ
    (clock_sufficient c m hm n) (dyadic n j) hj

/-- Faixa que cabe em n+3 bits binários; isto não é um custo de geração. -/
theorem dyadic_word_bound (n j : ℕ) (hj : j ≤ 2 ^ (n + 2)) :
    j < 2 ^ (n + 3) := by
  have hp : 0 < 2 ^ (n + 2) := by positivity
  have he : 2 ^ (n + 3) = 2 ^ (n + 2) * 2 := by
    rw [show n + 3 = (n + 2) + 1 by omega, pow_succ]
  rw [he]
  omega

end Codex.PonteLeituraBeta
