import TGLExt.AtalhosNaFita
import TGLExt.CustoDoPlano

/-! The total reader first scans the raw tape. Its fallback selects global pivots
from the formula and visits both branches. Count only visits to the Horn leaf reader
in the second coordinate; the first scan has its own physical movement theorem. -/
set_option autoImplicit false
namespace Codex.IntegratedRead
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula IALD.LeitorDaFormula
open Codex.CaudaDisjunta Codex.PlanCounter Codex.FormulaPlan Codex.PolinomioPorEscolha
variable {n : Nat}

def read (p : CNF n) : Option Bool × Nat :=
  match FastScan.answer (original p) with
  | some b => (some b,0)
  | none => counted (pivots p) p

theorem exact_read (p : CNF n) : (read p).1 = some (palavraDaFormula p) := by
  cases h : FastScan.answer (original p) with
  | none => simp [read,h,counted_spec,decided_from_formula]
  | some b => simp [read,h,FastScan.fast_sound p b h]

def coupling (m : Nat) : Clausula (m+m) :=
  (List.finRange m).map (fun i => ⟨left i,false⟩)
def coupled (m : Nat) : CNF (m+m) := coupling m :: disjointCNF m

theorem common_label {m} (i : Fin m) : (⟨left i,false⟩ : Literal _) ∈ coupling m ∧
    (⟨left i,true⟩ : Literal _) ∈ pairClause i := by
  exact ⟨List.mem_map.mpr ⟨i,List.mem_finRange _,rfl⟩,List.mem_cons_self⟩

private theorem no_pivot_added (m : Nat) : pivots (coupled m) = pivots (disjointCNF m) := by
  have h : Codex.CrossSelectors.names (coupling m) true = [] := by
    simp [coupling,Codex.CrossSelectors.names,List.filter_map]
  simp only [pivots,coupled,List.flatMap_cons,h,List.tail_nil,List.nil_append]

theorem mixed_witness (m : Nat) : palavraDaFormula (coupled (m+1)) = true := by
  let x : Fin ((m+1)+(m+1)) → Bool := fun j => decide (m+1 ≤ j.val)
  apply (a_palavra_e_o_sat _).mpr
  apply (sat_iff _).mpr
  refine ⟨x,List.all_eq_true.mpr ?_⟩
  intro c hc
  rcases List.mem_cons.mp hc with rfl|tail
  · apply List.any_eq_true.mpr
    refine ⟨⟨left (0 : Fin (m+1)),false⟩,(common_label (0 : Fin (m+1))).1,?_⟩
    simp [x,left,Literal.vale]
  · obtain ⟨i,_,rfl⟩ := List.mem_map.mp tail
    apply List.any_eq_true.mpr
    refine ⟨⟨right i,true⟩,by simp [pairClause],?_⟩
    simp [right,x,Literal.vale]
    omega

theorem first_pass_undecided (m : Nat) : FastScan.answer (original (coupled (m+1))) = none := by
  let p := coupled (m+1)
  have no : IALD.GuardasNaFita.detects p = false := by
    apply Bool.eq_false_iff.mpr
    exact fun hit => IALD.GuardasNaFita.detection_safe p hit ((a_palavra_e_o_sat _).mp (mixed_witness m))
  have missed : passes p (fun _ => true) = false := by
    simp [p,coupled,coupling,passes,satisfeita,Literal.vale]
  rw [FastScan.fast_spec,no,missed]
  rfl

theorem coupled_visits (m : Nat) :
    (read (coupled (m+1))).1 = some true ∧ 2^(m+1) ≤ (read (coupled (m+1))).2 := by
  refine ⟨(exact_read _).trans (congrArg some (mixed_witness m)),?_⟩
  have lower := (many_visits (m+1)).2
  rw [counted_spec] at lower
  simpa only [read,first_pass_undecided,counted_spec,no_pivot_added] using lower

theorem coupled_size (k : Nat) : (original (coupled k)).length ≤ k*(5*k+4)+1 := by
  have negSize (xs : List (Fin k)) :
      ((xs.map (fun i => (⟨left i,false⟩ : Literal (k+k)))).flatMap spell).length ≤ xs.length*(k+1) := by
    induction xs with
    | nil => simp
    | cons i xs ih =>
      simp only [List.map_cons,List.flatMap_cons,List.length_append,spell,List.length_replicate,
        List.length_cons,List.length_nil,Nat.add_mul,Nat.one_mul] at ⊢
      have hi : (left i).val < k := i.isLt
      omega
  have neg := negSize (List.finRange k)
  rw [List.length_finRange] at neg
  have pairs := disjoint_input_size k
  change (spellClause (coupling k) ++ original (disjointCNF k)).length ≤ _
  simp only [List.length_append,spellClause,coupling,List.length_cons,List.length_nil]
  nlinarith

end Codex.IntegratedRead
