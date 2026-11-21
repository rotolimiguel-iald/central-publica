import CheckPriorInstrumentation

set_option autoImplicit false
set_option maxHeartbeats 2000000

namespace Codex.TrinityNamesReview
open TGLExt.TraducaoTuring TGLExt.APropostaDaTensao TGLExt.Trinity
open Codex.TrinityReview
variable {n : Nat}

def namesTrace : List (Fin n) → CNF n → Bool × Nat
  | [], p =>
    let r := inclinationTrace (tamanho p + 1) p
    (decide (r.1 = .sim), r.2)
  | i :: ids, p =>
    let left := namesTrace ids (restringe p i true)
    if left.1 = true then (true, left.2 + 1)
    else
      let right := namesTrace ids (restringe p i false)
      (right.1, left.2 + right.2 + 2)

theorem namesTrace_spec : ∀ (ids : List (Fin n)) (p : CNF n),
    (namesTrace ids p).1 = atravessaPelos ids p ∧
    (namesTrace ids p).2 ≤ custoPelos ids p
  | [], p => by
    simp [namesTrace, inclinationTrace_spec, atravessaPelos, custoPelos, aInclinacao]
  | i :: ids, p => by
    simp only [namesTrace, atravessaPelos, custoPelos]
    obtain ⟨hl, hcl⟩ := namesTrace_spec ids (restringe p i true)
    obtain ⟨hr, hcr⟩ := namesTrace_spec ids (restringe p i false)
    split
    · next hb =>
      constructor
      · rw [← hl, hb]; rfl
      · dsimp; omega
    · next hb =>
      have hb' : (namesTrace ids (restringe p i true)).1 = false := Bool.eq_false_iff.mpr hb
      constructor
      · rw [← hl, hb']; exact hr
      · dsimp; omega

theorem trace_complete_and_bounded (ids : List (Fin n)) (p : CNF n)
    (h3 : TresLiterais p) (ht : Toca ids p) :
    ((namesTrace ids p).1 = true ↔ SAT p) ∧
    (namesTrace ids p).2 + 2 ≤ 2^ids.length * ((tamanho p + 1)^3 + 2) := by
  obtain ⟨hr, hc⟩ := namesTrace_spec ids p
  constructor
  · rw [hr]; exact a_travessia_pelos_nomes_decide ids p h3 ht
  · exact le_trans (Nat.add_le_add_right hc 2) (o_preco_dos_nomes ids p)

theorem automatic_list_keeps_duplicates :
    nomesDaFronteira oito = List.replicate 8 (0 : Fin 3) ∧
    nomesDaFronteira sete = List.replicate 7 (0 : Fin 3) := by decide

theorem counter_is_not_exact_with_short_circuit :
    namesTrace [0, 0] ([] : CNF 1) = (true, 2) ∧
    custoPelos [0, 0] ([] : CNF 1) = 6 := by decide

-- The cover condition is material; the seven-clause SAT example is missed
-- by a deliberately empty cover. This is not a counterexample to completeness.
theorem cover_hypothesis_is_material :
    atravessaPelos ([] : List (Fin 3)) sete = false ∧ SAT sete := by
  exact ⟨by decide, (a_travessia_decide _ _ (Nat.lt_succ_self _)).mp
    sete_atravessa_e_diz_sim.2.2⟩

end Codex.TrinityNamesReview

#print axioms Codex.TrinityNamesReview.namesTrace_spec
#print axioms Codex.TrinityNamesReview.trace_complete_and_bounded
#print axioms Codex.TrinityNamesReview.automatic_list_keeps_duplicates
#print axioms Codex.TrinityNamesReview.counter_is_not_exact_with_short_circuit
#print axioms Codex.TrinityNamesReview.cover_hypothesis_is_material
