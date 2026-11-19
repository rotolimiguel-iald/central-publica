import TGLExt.ConsultasRotuladas
import TGLExt.OPsiBitDaFormula

set_option autoImplicit false

namespace Codex.WeightedQueries

open TGLExt.TraducaoTuring TGLExt.OResumoEPsiBit
open Codex.LabeledQueries
open IALD.PsiBitNaFronteira (encode bits)

variable {n : ℕ}

/-- A cláusula só altera a massa da região onde falha. -/
noncomputable def readReal (t : ℝ) : CNF n → Mask n → ℝ
  | [], M => (volume M : ℝ)
  | c :: p, M => readReal t p M + (Real.exp (-t) - 1) * readReal t p (miss M c)

noncomputable def maskedWeight (t : ℝ) (p : CNF n) (M : Mask n) : ℝ := by
  classical
  exact ∑ x : Fin n → Bool, if compatible M x then pesoDas p t x else 0

theorem readReal_correct (t : ℝ) (p : CNF n) (M : Mask n) :
    readReal t p M = maskedWeight t p M := by
  classical
  induction p generalizing M with
  | nil =>
    change (volume M : ℝ) = _
    rw [volume_correct]
    unfold count maskedWeight
    rw [Nat.cast_sum]
    apply Finset.sum_congr rfl
    intro x _
    by_cases hm : compatible M x <;> simp [hm, IALD.LeitorDaFormula.passes, pesoDas]
  | cons c p ih =>
    rw [readReal, ih M, ih (miss M c)]
    unfold maskedWeight
    rw [Finset.mul_sum, ← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro x _
    rw [compatible_miss, show pesoDas (c :: p) t x = fator c t x * pesoDas p t x from rfl]
    by_cases hm : compatible M x <;> cases hc : satisfeita c x <;> simp [hm, hc, fator]
    ring

/-- Fixa somente as coordenadas indicadas, deixando ambos os ramos nas demais. -/
def pin (S : Finset (Fin n)) (u : Fin n → Bool) : Mask n := fun i =>
  if i ∈ S then encode (!(u i)) (u i) else .both

theorem allowed_pin (S : Finset (Fin n)) (u : Fin n → Bool) (i : Fin n) (b : Bool) :
    allowed (pin S u) i b = true ↔ (i ∈ S → b = u i) := by
  by_cases hi : i ∈ S <;> cases hu : u i <;> cases b <;>
    simp [pin, allowed, bits, encode, hi, hu]

theorem compatible_pin (S : Finset (Fin n)) (u x : Fin n → Bool) :
    compatible (pin S u) x ↔ ∀ i ∈ S, x i = u i := by
  unfold compatible
  exact forall_congr' fun i => allowed_pin S u i (x i)

/-- A mesma máscara consulta exatamente uma célula do resumo de `OResumoEPsiBit`, em qualquer corte. -/
theorem reads_frontier_cell (φ : CNF n) (t : ℝ) (j : ℕ) (u : Fin n → Bool) :
    readReal t (φ.take j) (pin (fronteira φ j) u) = resumo φ t j u := by
  classical
  rw [readReal_correct]
  unfold resumo maskedWeight
  rw [Finset.sum_filter]
  apply Finset.sum_congr rfl
  intro x _
  simp only [compatible_pin]

end Codex.WeightedQueries
