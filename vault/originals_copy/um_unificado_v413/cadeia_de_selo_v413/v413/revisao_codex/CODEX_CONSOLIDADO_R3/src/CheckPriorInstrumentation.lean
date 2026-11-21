import Trinity

set_option autoImplicit false
set_option maxHeartbeats 1000000

namespace Codex.TrinityReview
open TGLExt.TraducaoTuring TGLExt.APropostaDaTensao TGLExt.Trinity
variable {n : Nat}

-- A paired evaluator counts fixation events while following the procedure.
-- This does not count tape steps, comparisons or evaluation of the cost function.
def propagationTrace : Nat → CNF n → CNF n × Nat
  | 0, p => (p, 0)
  | k + 1, p =>
    if morta p = true then (p, 0)
    else match unidade p with
      | none => (p, 0)
      | some l =>
        let r := propagationTrace k (fixa p l)
        (r.1, r.2 + 1)

theorem propagationTrace_spec : ∀ (k : Nat) (p : CNF n),
    propagationTrace k p = (propaga k p, custoPropaga k p)
  | 0, _ => rfl
  | k + 1, p => by
    simp only [propagationTrace, propaga, custoPropaga]
    split
    · rfl
    · cases hu : unidade p with
      | none => rfl
      | some l => simp only [propagationTrace_spec]

def probeTrace (p : CNF n) : List (Literal n) → Option (Lance n) × Nat
  | [] => (none, 0)
  | l :: ls =>
    let side := propagationTrace (tamanho p) (fixa p l)
    if morta side.1 = true then (some (.empurra l), side.2 + 1)
    else if contida side.1 p = true then (some (.compromete l), side.2 + 1)
    else
      let r := probeTrace p ls
      (r.1, side.2 + 1 + r.2)

theorem probeTrace_spec (p : CNF n) : ∀ ls : List (Literal n),
    probeTrace p ls = (sonda p ls, custoSonda p ls)
  | [] => rfl
  | l :: ls => by
    simp only [probeTrace, propagationTrace_spec, sonda, custoSonda, morreLogo]
    split
    · simp only [Nat.add_zero]
    · split
      · simp only [Nat.add_zero]
      · simp only [probeTrace_spec]

def inclinationTrace : Nat → CNF n → Veredito × Nat
  | 0, _ => (.indeciso, 0)
  | k + 1, p =>
    let r := propagationTrace (tamanho p) p
    if morta r.1 = true then (.nao, r.2)
    else if passaTrivial r.1 = true then (.sim, r.2)
    else
      let s := probeTrace r.1 r.1.flatten
      match s.1 with
      | none => (.indeciso, r.2 + s.2)
      | some (.empurra l) =>
        let rest := inclinationTrace k (fixa r.1 (oposto l))
        (rest.1, r.2 + (s.2 + (rest.2 + 1)))
      | some (.compromete l) =>
        let rest := inclinationTrace k (fixa r.1 l)
        (rest.1, r.2 + (s.2 + (rest.2 + 1)))

theorem inclinationTrace_spec : ∀ (k : Nat) (p : CNF n),
    inclinationTrace k p = (inclina k p, custoInclina k p)
  | 0, _ => rfl
  | k + 1, p => by
    simp only [inclinationTrace, propagationTrace_spec, probeTrace_spec, inclina, custoInclina]
    split
    · simp only [Nat.add_zero]
    · split
      · simp only [Nat.add_zero]
      · cases hs : sonda (propaga (tamanho p) p) (propaga (tamanho p) p).flatten with
        | none => simp only [Nat.add_zero]
        | some action =>
          cases action <;> simp only [inclinationTrace_spec]

theorem chain_two_rounds : inclina 1 cadeia = .indeciso ∧ inclina 2 cadeia = .sim := by decide

theorem chain_four_fixations : custoInclina (tamanho cadeia + 1) cadeia = 4 := by decide

theorem empty_cases : aInclinacao ([] : CNF 0) = .sim ∧ aInclinacao ([[]] : CNF 0) = .nao := by decide

-- The quantification of the R1 lemma imposes no occurrence condition on l.
theorem any_literal_including_absent {p : CNF n}
    (h : ∀ C ∈ p, C.length = 2) (l : Literal n) :
    morta (propaga (tamanho p) (fixa p l)) = true ∨
    contida (propaga (tamanho p) (fixa p l)) p = true :=
  todo_lado_morre_ou_nao_corta h l

end Codex.TrinityReview

#print axioms Codex.TrinityReview.propagationTrace_spec
#print axioms Codex.TrinityReview.probeTrace_spec
#print axioms Codex.TrinityReview.inclinationTrace_spec
#print axioms Codex.TrinityReview.chain_two_rounds
#print axioms Codex.TrinityReview.chain_four_fixations
#print axioms Codex.TrinityReview.empty_cases
#print axioms Codex.TrinityReview.any_literal_including_absent
