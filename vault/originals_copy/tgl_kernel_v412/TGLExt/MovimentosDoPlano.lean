import TGLExt.LeituraIntegrada

/-! A lower bound in *physical head movements*, for the defined eager pivot
reader and its unary Horn leaf machine. Every residual keeps a real clause. -/
set_option autoImplicit false
namespace Codex.PlanTravel
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula
open Codex.SharedBranch Codex.SharedReader Codex.CaudaDisjunta Codex.HornResidual
open Codex.CrossSelectors Codex.FormulaPlan Codex.IntegratedRead Codex.PolinomioPorEscolha
open Codex.SparseHornTape Codex.HornCross
variable {n : Nat}

private theorem untouched (c : Clausula n) (i : Fin n) (b : Bool)
    (h : ∀ l ∈ c, l.var ≠ i) : restrictClause i b c = some c := by
  have skip : c.any (fun l => l.var == i && l.pos == b) = false := by
    apply List.any_eq_false.mpr
    intro l hl
    have e : (l.var == i) = false := beq_eq_false_iff_ne.mpr (h l hl)
    simp [e]
  have keep : c.filter (fun l => l.var != i) = c := by
    apply List.filter_eq_self.mpr
    intro l hl
    simpa using h l hl
  simp only [restrictClause,skip,Bool.false_eq_true,if_false,keep]

private theorem parsed_nonempty {p : CNF n} {q : List (Rule n)}
    (hp : p ≠ []) (h : parseProgram p = some q) : q ≠ [] := by
  cases p with
  | nil => contradiction
  | cons c cs =>
    cases hc : parseClause c <;> cases hs : parseProgram cs <;> simp [parseProgram,hc,hs] at h
    subst q
    simp

private theorem leaf_moves {q : List (Rule n)} {a : Bool} {t : Nat}
    (hn : q ≠ []) (hh : (run t (start q ∅)).mode = .halt a) :
    1 ≤ travel t (start q ∅) := by
  have positive : 0 < (program q).length :=
    lt_of_lt_of_le (List.length_pos_iff.mpr hn) (clauses_length q)
  cases t with
  | zero => contradiction
  | succ k =>
    cases h : program q with
    | nil => simp [h] at positive
    | cons sym rest =>
      rw [travel]
      have moved : 1 ≤ moves (start q ∅) (step (start q ∅)) := by
        cases sym <;> simp [start,readCfg,h,step,moves,Nat.dist]
      omega

theorem trace_moves_of_surviving_clause {is : List (Fin n)} {p : CNF n} {ans : Bool} {m : Nat}
    (trace : Trace is p ans m) (c : Clausula n) (hc : c ∈ p)
    (outside : ∀ l ∈ c, l.var ∉ is) : 2^is.length ≤ m := by
  induction trace with
  | leaf h halted =>
    have nonempty := parsed_nonempty (List.ne_nil_of_mem hc) h
    simpa only [List.length_nil,pow_zero] using leaf_moves nonempty halted
  | @fork i is p _ _ _ _ tl tr ihl ihr =>
    have stay (b : Bool) : c ∈ restrictVar i b p := by
      apply List.mem_filterMap.mpr
      exact ⟨c,hc,untouched c i b (fun l hl e => outside l hl (List.mem_cons.mpr (Or.inl e)))⟩
    have tail : ∀ l ∈ c, l.var ∉ is :=
      fun l hl hmem => outside l hl (List.mem_cons_of_mem _ hmem)
    have a := ihl (stay false) tail
    have b := ihr (stay true) tail
    simp only [List.length_cons,pow_succ,Nat.mul_two]
    exact Nat.add_le_add a b

private theorem only_right {k} {v : Fin (k+k)} (hv : v ∈ pivots (coupled k)) :
    ∃ i : Fin k, v = right i := by
  unfold pivots at hv
  obtain ⟨c,hc,h⟩ := List.mem_flatMap.mp (List.mem_dedup.mp hv)
  rcases List.mem_cons.mp hc with rfl|hm
  · have hneg : names (coupling k) true = [] := by
      simp [coupling,names,List.filter_map]
    simp [hneg] at h
  · obtain ⟨i,_,rfl⟩ := List.mem_map.mp hm
    exact ⟨i,by simpa [pairClause,names] using h⟩

/-- A trace exists by horn_moves_from_formula. This lower bound holds for *every*
successful complete trace, so changing the stopping clocks cannot erase the cost. -/
theorem coupled_physical_lower (m : Nat) {moves : Nat} {answer : Bool}
    (t : Trace (pivots (coupled (m+1))) (coupled (m+1)) answer moves) :
    2^(m+1) ≤ moves := by
  let p := coupled (m+1)
  have leaves : 2^(m+1) ≤ 2^(pivots p).length := by
    have h := (coupled_visits m).2
    simpa only [Codex.IntegratedRead.read,first_pass_undecided,PlanCounter.counted_spec] using h
  apply leaves.trans
  apply trace_moves_of_surviving_clause t (coupling (m+1)) List.mem_cons_self
  intro l hl picked
  obtain ⟨a,_,rfl⟩ := List.mem_map.mp hl
  obtain ⟨b,e⟩ := only_right picked
  have eq := congrArg Fin.val e
  change (left a).val = (right b).val at eq
  simp only [left,right,Fin.val_castAdd,Fin.val_natAdd] at eq
  have lt := a.isLt
  omega

end Codex.PlanTravel
