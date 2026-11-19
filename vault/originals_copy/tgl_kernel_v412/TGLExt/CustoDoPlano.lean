import TGLExt.PlanoDaFormula
import TGLExt.CaudaDisjunta

set_option autoImplicit false
namespace Codex.PlanCounter
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula
open Codex.SharedBranch Codex.SharedReader Codex.FormulaPlan Codex.HornResidual
open Codex.CrossSelectors Codex.CaudaDisjunta Codex.PolinomioPorEscolha
variable {n : Nat}

/-- Count a visit at the syntactic recognizer, even if the residual is empty.
Both sides are evaluated. This count is distinct from head displacements. -/
def counted : List (Fin n) → CNF n → Option Bool × Nat
  | [],p => ((parseProgram p).map checkProgram,1)
  | i::is,p =>
    let l := counted is (restrictVar i false p)
    let r := counted is (restrictVar i true p)
    (both l.1 r.1,l.2+r.2)

theorem counted_spec (is : List (Fin n)) (p : CNF n) :
    counted is p = (readPlan is p,2^is.length) := by
  induction is generalizing p with
  | nil => rfl
  | cons i is ih => simp only [counted,ih,readPlan,List.length_cons,pow_succ,Nat.mul_two]

theorem ready_all (is : List (Fin n)) (p : CNF n) (h : ready is p) (x : Fin n → Bool) :
    ∃ q, parseProgram (restrictMany is x p) = some q := by
  induction is generalizing p with
  | nil => exact h
  | cons i is ih =>
    change ∃ q, parseProgram (restrictMany is x (restrictVar i (x i) p)) = some q
    cases e : x i
    · exact ih _ h.1
    · exact ih _ h.2

theorem many_visits (m : Nat) :
    let p := disjointCNF m
    (counted (pivots p) p).1 = some true ∧ 2^m ≤ (counted (pivots p) p).2 := by
  dsimp only
  let p := disjointCNF m
  have ready' : ready (pivots p) p := covered_ready _ _ (pivots_cover p)
  have enough := every_residual_requires (pivots p) (ready_all _ _ ready')
  have length' : m ≤ (pivots p).length := enough.trans (List.toFinset_card_le _)
  rw [counted_spec,decided_from_formula,simple_witness]
  exact ⟨rfl,Nat.pow_le_pow_right (by decide) length'⟩

theorem disjoint_input_size (m : Nat) :
    (original (disjointCNF m)).length ≤ m*(4*m+3) := by
  have bound (xs : List (Fin m)) :
      (original (xs.map pairClause)).length ≤ xs.length*(4*m+3) := by
    induction xs with
    | nil => simp [original]
    | cons i xs ih =>
      have each : (spellClause (pairClause i)).length ≤ 4*m+3 := by
        have a := (left i).isLt
        have b := (right i).isLt
        simp only [pairClause,spellClause,spell,List.flatMap_cons,List.flatMap_nil,
          List.length_append,List.length_replicate,List.length_cons,List.length_nil]
        omega
      change (spellClause (pairClause i) ++ original (xs.map pairClause)).length ≤
        (xs.length+1)*(4*m+3)
      rw [List.length_append,Nat.add_mul,Nat.one_mul]
      omega
  simpa [disjointCNF] using bound (List.finRange m)

end Codex.PlanCounter
