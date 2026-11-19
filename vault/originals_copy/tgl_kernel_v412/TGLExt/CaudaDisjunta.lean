import TGLExt.ChecagemHorn
import TGLExt.RestricaoGlobal

/-! A disjoint family with an explicit satisfying assignment. A set of labels
that makes its all-false residual syntactically Horn must meet each pair. -/
set_option autoImplicit false
namespace Codex.CaudaDisjunta
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula IALD.LeitorDaFormula
open Codex.HornResidual Codex.SharedBranch Codex.HornCross Codex.CrossSelectors

def left {m : Nat} (i : Fin m) : Fin (m+m) := i.castAdd m
def right {m : Nat} (i : Fin m) : Fin (m+m) := Fin.natAdd m i
def pairIndex {m : Nat} : Fin (m+m) → Fin m := Fin.addCases id id
def pairClause {m : Nat} (i : Fin m) : Clausula (m+m) :=
  [⟨left i,true⟩,⟨right i,true⟩]
def disjointCNF (m : Nat) : CNF (m+m) := (List.finRange m).map pairClause

theorem simple_witness (m : Nat) : palavraDaFormula (disjointCNF m) = true := by
  apply (a_palavra_e_o_sat _).mpr
  apply (sat_iff _).mpr
  refine ⟨fun _ => true,List.all_eq_true.mpr ?_⟩
  intro c hc
  obtain ⟨i,_,rfl⟩ := List.mem_map.mp hc
  simp [pairClause,satisfeita,Literal.vale]

private theorem hits_bound {m : Nat} (is : List (Fin (m+m)))
    (hits : ∀ i : Fin m, left i ∈ is ∨ right i ∈ is) :
    m ≤ is.toFinset.card := by
  have sub : (Finset.univ : Finset (Fin m)) ⊆ is.toFinset.image pairIndex := by
    intro i _
    rcases hits i with hl | hr
    · exact Finset.mem_image.mpr ⟨left i,by simpa using hl,by simp [pairIndex,left]⟩
    · exact Finset.mem_image.mpr ⟨right i,by simpa using hr,Fin.addCases_right i⟩
  calc
    m = (Finset.univ : Finset (Fin m)).card := by simp
    _ ≤ (is.toFinset.image pairIndex).card := Finset.card_le_card sub
    _ ≤ is.toFinset.card := Finset.card_image_le

private theorem untouched {m : Nat} (i : Fin m) (is : List (Fin (m+m)))
    (p : CNF (m+m)) (hc : pairClause i ∈ p)
    (hl : left i ∉ is) (hr : right i ∉ is) :
    pairClause i ∈ restrictMany is (fun _ => false) p := by
  induction is generalizing p with
  | nil => exact hc
  | cons j is ih =>
    have hlj : left i ≠ j := fun he => hl (List.mem_cons.mpr (Or.inl he))
    have hrj : right i ≠ j := fun he => hr (List.mem_cons.mpr (Or.inl he))
    apply ih (restrictVar j false p) _ (fun h => hl (List.mem_cons_of_mem _ h))
      (fun h => hr (List.mem_cons_of_mem _ h))
    apply List.mem_filterMap.mpr
    refine ⟨pairClause i,hc,?_⟩
    simp [Codex.SharedBranch.restrictClause,pairClause,hlj,hrj]

/-- One assignment on the chosen labels already forces them to hit every pair.
The count is of distinct labels even if the conditioning list repeats labels. -/
theorem all_false_requires {m : Nat} (is : List (Fin (m+m)))
    (accepted : ∃ q, parseProgram (restrictMany is (fun _ => false) (disjointCNF m)) = some q) :
    m ≤ is.toFinset.card := by
  apply hits_bound
  intro i
  by_contra! missed
  have source : pairClause i ∈ disjointCNF m :=
    List.mem_map.mpr ⟨i,List.mem_finRange _,rfl⟩
  have mem := untouched i is _ source missed.1 missed.2
  have impossible := (parse_iff _).mp accepted _ mem
  change 2 ≤ 1 at impossible
  omega

theorem every_residual_requires {m : Nat} (is : List (Fin (m+m)))
    (accepted : ∀ x : Fin (m+m) → Bool,
      ∃ q, parseProgram (restrictMany is x (disjointCNF m)) = some q) :
    m ≤ is.toFinset.card := all_false_requires is (accepted (fun _ => false))

end Codex.CaudaDisjunta
