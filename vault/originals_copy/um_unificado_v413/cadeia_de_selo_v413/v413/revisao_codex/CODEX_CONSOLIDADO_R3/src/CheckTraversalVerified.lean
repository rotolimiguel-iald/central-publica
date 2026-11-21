import CheckPriorInstrumentation

set_option autoImplicit false
set_option maxHeartbeats 2000000

namespace Codex.TrinityR2Review
open TGLExt.TraducaoTuring TGLExt.APropostaDaTensao TGLExt.Trinity
open Codex.TrinityReview
variable {n : Nat}

theorem frontier_fixed (k : Nat) {p : CNF n} (h : NaFronteira p) :
    propaga k p = p := by
  cases k with
  | zero => rfl
  | succ k =>
    have hu : unidade p = none := Option.isNone_iff_eq_none.mp h.2.1
    simp [propaga, h.1, hu]

theorem frontier_undecided (k : Nat) {p : CNF n} (h : NaFronteira p) :
    inclina (k + 1) p = .indeciso := by
  have hs : sonda p p.flatten = none := Option.isNone_iff_eq_none.mp h.2.2.2
  simp [inclina, frontier_fixed (tamanho p) h, h.1, h.2.2.1, hs]

-- Every branch guard is a saturated frontier, irrespective of outer fuel.
theorem branch_is_frontier (p : CNF n)
    (hm : morta (propaga (tamanho p) p) = false)
    (ht : passaTrivial (propaga (tamanho p) p) = false)
    (hs : sonda (propaga (tamanho p) p) (propaga (tamanho p) p).flatten = none) :
    NaFronteira (propaga (tamanho p) p) := by
  have hu := (a_propagacao_para (tamanho p) p le_rfl).resolve_left
    (by rw [hm]; decide)
  exact ⟨hm, by simp [hu], ht, by simp [hs]⟩

-- Follow Boolean short-circuit evaluation, returning fixation events together
-- with the answer. This is not a tape-step or wall-clock cost semantics.
def traversalTrace : Nat → CNF n → Bool × Nat
  | 0, _ => (false, 0)
  | k + 1, p =>
    let r := propagationTrace (tamanho p) p
    if morta r.1 = true then (false, r.2)
    else if passaTrivial r.1 = true then (true, r.2)
    else
      let s := probeTrace r.1 r.1.flatten
      match s.1 with
      | some (.empurra l) =>
        let rest := traversalTrace k (fixa r.1 (oposto l))
        (rest.1, r.2 + (s.2 + (rest.2 + 1)))
      | some (.compromete l) =>
        let rest := traversalTrace k (fixa r.1 l)
        (rest.1, r.2 + (s.2 + (rest.2 + 1)))
      | none => match r.1.flatten with
        | [] => (true, r.2 + s.2)
        | l :: _ =>
          let left := traversalTrace k (fixa r.1 l)
          if left.1 = true then (true, r.2 + (s.2 + (left.2 + 1)))
          else
            let right := traversalTrace k (fixa r.1 (oposto l))
            (right.1, r.2 + (s.2 + (left.2 + right.2 + 2)))

theorem traversalTrace_spec : ∀ (k : Nat) (p : CNF n),
    (traversalTrace k p).1 = atravessa k p ∧
    (traversalTrace k p).2 ≤ custoAtravessa k p
  | 0, _ => ⟨rfl, le_rfl⟩
  | k + 1, p => by
    simp only [traversalTrace, propagationTrace_spec, probeTrace_spec,
      atravessa, custoAtravessa]
    split
    · simp
    · split
      · simp
      · split
        · next l hs =>
          simp only [hs]
          obtain ⟨hr, hc⟩ := traversalTrace_spec k
            (fixa (propaga (tamanho p) p) (oposto l))
          exact ⟨hr, Nat.add_le_add_left (Nat.add_le_add_left (Nat.add_le_add_right hc 1) _) _⟩
        · next l hs =>
          simp only [hs]
          obtain ⟨hr, hc⟩ := traversalTrace_spec k
            (fixa (propaga (tamanho p) p) l)
          exact ⟨hr, Nat.add_le_add_left (Nat.add_le_add_left (Nat.add_le_add_right hc 1) _) _⟩
        · next hs =>
          simp only [hs]
          split
          · next hfl => simp [hfl]
          · next l ls hls =>
            simp only [hls]
            obtain ⟨hl, hcl⟩ := traversalTrace_spec k
              (fixa (propaga (tamanho p) p) l)
            obtain ⟨hr, hcr⟩ := traversalTrace_spec k
              (fixa (propaga (tamanho p) p) (oposto l))
            split
            · next hb =>
              constructor
              · rw [← hl, hb]; rfl
              · have hc : (traversalTrace k (fixa (propaga (tamanho p) p) l)).2 + 1 ≤
                    custoAtravessa k (fixa (propaga (tamanho p) p) l) +
                    custoAtravessa k (fixa (propaga (tamanho p) p) (oposto l)) + 2 := by omega
                exact Nat.add_le_add_left (Nat.add_le_add_left hc _) _
            · next hb =>
              have hb' : (traversalTrace k (fixa (propaga (tamanho p) p) l)).1 = false :=
                Bool.eq_false_iff.mpr hb
              constructor
              · rw [← hl, hb']; exact hr
              · exact Nat.add_le_add_left
                  (Nat.add_le_add_left (Nat.add_le_add_right (Nat.add_le_add hcl hcr) 2) _) _

theorem trace_complete_and_upper_bound (p : CNF n) :
    ((traversalTrace (tamanho p + 1) p).1 = true ↔ SAT p) ∧
    (traversalTrace (tamanho p + 1) p).2 + ((tamanho p + 1)^2 + 1) ≤
      2^(tamanho p + 1) * ((tamanho p + 1)^2 + 1) := by
  obtain ⟨hr, hc⟩ := traversalTrace_spec (tamanho p + 1) p
  constructor
  · rw [hr]; exact a_travessia_decide _ _ (Nat.lt_succ_self _)
  · exact le_trans (Nat.add_le_add_right hc _) (o_preco_da_travessia _ _)

-- Reorder the seven clauses so that the left branch is the satisfying side.
def sevenLeft : CNF 3 := sete.drop 3 ++ sete.take 3

#eval (traversalTrace (tamanho sevenLeft + 1) sevenLeft,
  custoAtravessa (tamanho sevenLeft + 1) sevenLeft)

theorem short_circuit_counter_is_strict :
    NaFronteira sevenLeft ∧
    (traversalTrace (tamanho sevenLeft + 1) sevenLeft).1 = true ∧
    (traversalTrace (tamanho sevenLeft + 1) sevenLeft).2 <
      custoAtravessa (tamanho sevenLeft + 1) sevenLeft := by decide

-- The existential conclusion alone does not encode execution from its input.
-- This does not contradict a_inclinacao_para_so_na_fronteira.
theorem existential_alone_is_weaker_than_reachability :
    aInclinacao ([] : CNF 3) = .sim ∧
    ∃ p : CNF 3, (SAT p ↔ SAT ([] : CNF 3)) ∧ NaFronteira p := by
  refine ⟨by decide, sete, ?_, sete_atravessa_e_diz_sim.1⟩
  have hs : SAT sete := (a_travessia_decide _ _ (Nat.lt_succ_self _)).mp
    sete_atravessa_e_diz_sim.2.2
  have he : SAT ([] : CNF 3) := ⟨fun _ => false, fun _ h => by simp at h⟩
  exact ⟨fun _ => he, fun _ => hs⟩

theorem fuel_guard_is_material :
    atravessa 0 ([] : CNF 0) = false ∧ atravessa 1 ([] : CNF 0) = true := by decide

end Codex.TrinityR2Review

#print axioms Codex.TrinityR2Review.frontier_fixed
#print axioms Codex.TrinityR2Review.frontier_undecided
#print axioms Codex.TrinityR2Review.branch_is_frontier
#print axioms Codex.TrinityR2Review.traversalTrace_spec
#print axioms Codex.TrinityR2Review.trace_complete_and_upper_bound
#print axioms Codex.TrinityR2Review.short_circuit_counter_is_strict
#print axioms Codex.TrinityR2Review.existential_alone_is_weaker_than_reachability
#print axioms Codex.TrinityR2Review.fuel_guard_is_material
