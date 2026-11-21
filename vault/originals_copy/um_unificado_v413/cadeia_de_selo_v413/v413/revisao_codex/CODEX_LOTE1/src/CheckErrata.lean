import TGLExt.OResumoEPsiBit

set_option autoImplicit false

namespace Codex.V413Review

open TGLExt.TraducaoTuring TGLExt.OResumoEPsiBit

/-- The frontier after the last clause is empty, regardless of the formula. -/
theorem final_frontier_empty {n : ℕ} (φ : CNF n) :
    fronteira φ φ.length = ∅ := by
  simp [fronteira, varsDas]

/-- An empty frontier has one cell whose fiber is the whole assignment space. -/
theorem final_fiber_is_universe {n : ℕ} (φ : CNF n) (u : Fin n → Bool) :
    Finset.univ.filter (fun x : Fin n → Bool =>
      ∀ i ∈ fronteira φ φ.length, x i = u i) = Finset.univ := by
  classical
  simp [final_frontier_empty]

/-- This is a transition allowed by the original hypothesis j < length. -/
theorem one_clause_fiber_is_universe {n : ℕ} (C : Clausula n) (u : Fin n → Bool) :
    0 < ([C] : CNF n).length ∧
    Finset.univ.filter (fun x : Fin n → Bool =>
      ∀ i ∈ fronteira [C] (0 + 1), x i = u i) = Finset.univ := by
  classical
  exact ⟨by simp, final_fiber_is_universe [C] u⟩

/-- The old summary aggregates weights; it is not the old weight of one assignment. -/
theorem summary_is_not_individual_weight (u : Fin 1 → Bool) :
    resumo ([[]] : CNF 1) 0 0 u = 2 ∧ pesoDas ([] : CNF 1) 0 u = 1 := by
  classical
  constructor
  · simp [resumo, fronteira, varsDas, pesoDas]
  · simp [pesoDas]

end Codex.V413Review

#print axioms Codex.V413Review.final_frontier_empty
#print axioms Codex.V413Review.final_fiber_is_universe
#print axioms Codex.V413Review.one_clause_fiber_is_universe
#print axioms Codex.V413Review.summary_is_not_individual_weight
