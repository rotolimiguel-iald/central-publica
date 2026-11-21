import TGLExt.PonteLeituraBeta
import TGLExt.QuantizacaoBeta
set_option autoImplicit false

/-!
Passo finito da leitura beta.

Uma constante natural é fixada por beta; a precisão é finita; as consultas
reconstroem uma testemunha sem a hipótese de solução única. As hipóteses sobre
o produtor `reader` estão expressas. Nenhum teorema deste arquivo constrói uma
máquina de fita polinomial para calcular esse produtor.
-/

namespace Codex.EntregaBeta

open TGLExt TGLExt.TraducaoTuring Codex.RelogioBeta Codex.LeituraBeta
open Codex.PonteLeituraBeta Codex.QuantizacaoBeta
open TGLExt.APonteDeCookLevin

variable {n : ℕ}

theorem bounded_code_exists (c : TGLCoupling) (m : ℕ)
    (hm : Real.log 2 / c.beta < (m : ℝ)) (φ : CNF n) :
    ∃ j : ℕ, j < 2 ^ (n + 3) ∧
      |(dyadic n j : ℝ) - normalizedSum c (clock m n) φ| ≤
        1 / (4 * (2 : ℝ) ^ n) ∧
      (decide (2 ≤ j) = true ↔ SAT φ) := by
  obtain ⟨j, hj, he⟩ := normalizedSum_has_bounded_dyadic c (clock m n) φ
  have he' : |(dyadic n j : ℝ) - normalizedSum c (clock m n) φ| ≤
      1 / (4 * (2 : ℝ) ^ n) := by simpa [dyadic] using he
  exact ⟨j, dyadic_word_bound n j hj, he', dyadic_correct c m hm φ j he'⟩

/-- O teste inteiro usa só o numerador; o produtor é parâmetro. -/
def codeDecision (reader : CNF n → ℕ) (φ : CNF n) : Bool := decide (2 ≤ reader φ)

theorem codeDecision_correct (c : TGLCoupling) (m : ℕ)
    (hm : Real.log 2 / c.beta < (m : ℝ)) (reader : CNF n → ℕ)
    (hr : ∀ φ, |(dyadic n (reader φ) : ℝ) - normalizedSum c (clock m n) φ| ≤
      1 / (4 * (2 : ℝ) ^ n)) (φ : CNF n) :
    codeDecision reader φ = true ↔ SAT φ :=
  dyadic_correct c m hm φ (reader φ) (hr φ)

theorem all_labels_from_beta (c : TGLCoupling) (m : ℕ)
    (hm : Real.log 2 / c.beta < (m : ℝ)) (reader : CNF n → ℕ)
    (hr : ∀ φ, |(dyadic n (reader φ) : ℝ) - normalizedSum c (clock m n) φ| ≤
      1 / (4 * (2 : ℝ) ^ n)) (φ : CNF n) :
    ((Reconstrucao.solveByLetters (codeDecision reader) φ).1 = none ↔ ¬ SAT φ) ∧
    (∀ x, (Reconstrucao.solveByLetters (codeDecision reader) φ).1 = some x →
      Reconstrucao.Good φ x) ∧
    (Reconstrucao.solveByLetters (codeDecision reader) φ).2 ≤ letras φ + 1 :=
  Reconstrucao.solveByLetters_correct _ (codeDecision_correct c m hm reader hr) φ

/-- A soma dos comprimentos das consultas inclui a consulta inicial.
`letras` conta literais e terminadores. Não inclui execução do produtor,
largura dos índices, movimentação de cabeças ou construção das consultas. -/
theorem query_volume (reader : CNF n → ℕ) (φ : CNF n) :
    letras φ + ((Reconstrucao.queries (codeDecision reader) φ
      (Reconstrucao.occurrences φ)).map letras).sum ≤
      letras φ + 3 * (letras φ) ^ 2 := by
  exact Nat.add_le_add_left (Reconstrucao.queryByLetters_bound (codeDecision reader) φ).2 _

end Codex.EntregaBeta
