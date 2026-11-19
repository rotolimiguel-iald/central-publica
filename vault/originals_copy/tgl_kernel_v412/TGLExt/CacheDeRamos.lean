import TGLExt.CustoDaBuscaLiteral

/-! Keys record signed literals on a single choice path. A layer contains
only distinct keys reached by that prefix. The counter below charges one
extension attempt per (reached key, occurrence in the next clause). -/
set_option autoImplicit false

namespace Codex.BranchCache
open TGLExt.TraducaoTuring IALD.LeitorDaFormula
open Codex.LiteralSearchCost
variable {n : Nat}

abbrev Key (n : Nat) := Finset (Fin n × Bool)
abbrev Layer (n : Nat) := Finset (Key n)

def fits (s : Key n) (x : Fin n → Bool) : Prop := ∀ a ∈ s, x a.1 = a.2
def models (rows : Layer n) (x : Fin n → Bool) : Prop := ∃ s ∈ rows, fits s x
def initial (n : Nat) : Layer n := {∅}

def extend (s : Key n) (l : Literal n) : Layer n :=
  if (l.var,!l.pos) ∈ s then ∅ else {insert (l.var,l.pos) s}

def children (s : Key n) : Clausula n → Layer n
  | [] => ∅
  | l::rest => extend s l ∪ children s rest

def advance (rows : Layer n) (c : Clausula n) : Layer n :=
  rows.biUnion (fun s => children s c)

def run : CNF n → Layer n → Layer n
  | [],rows => rows
  | c::p,rows => run p (advance rows c)

private theorem fits_insert (s : Key n) (l : Literal n) (x : Fin n → Bool) :
    fits (insert (l.var,l.pos) s) x ↔ x l.var = l.pos ∧ fits s x := by
  simp [fits]

private theorem extend_models (s : Key n) (l : Literal n) (x : Fin n → Bool) :
    models (extend s l) x ↔ fits s x ∧ x l.var = l.pos := by
  by_cases opp : (l.var,!l.pos) ∈ s
  · simp only [extend,if_pos opp,models,Finset.notMem_empty,false_and,exists_false,false_iff]
    rintro ⟨hs,hit⟩
    have incompatible := hs (l.var,!l.pos) opp
    change x l.var = !l.pos at incompatible
    rw [hit] at incompatible
    cases sign : l.pos <;> simp [sign] at incompatible
  · simp [extend,opp,models,fits_insert,and_comm]

private theorem models_union (a b : Layer n) (x : Fin n → Bool) :
    models (a ∪ b) x ↔ models a x ∨ models b x := by
  simp only [models,Finset.mem_union,or_and_right,exists_or]

private theorem children_models (s : Key n) (c : Clausula n) (x : Fin n → Bool) :
    models (children s c) x ↔ fits s x ∧ satisfeita c x = true := by
  induction c with
  | nil => simp [children,models,satisfeita]
  | cons l c ih =>
    rw [children,models_union,extend_models,ih]
    simp [satisfeita,Literal.vale,and_or_left]

theorem advance_models (rows : Layer n) (c : Clausula n) (x : Fin n → Bool) :
    models (advance rows c) x ↔ models rows x ∧ satisfeita c x = true := by
  constructor
  · rintro ⟨t,ht,fit⟩
    obtain ⟨s,hs,ht⟩ := Finset.mem_biUnion.mp ht
    obtain ⟨old,hit⟩ := (children_models s c x).mp ⟨t,ht,fit⟩
    exact ⟨⟨s,hs,old⟩,hit⟩
  · rintro ⟨⟨s,hs,old⟩,hit⟩
    obtain ⟨t,ht,fit⟩ := (children_models s c x).mpr ⟨old,hit⟩
    exact ⟨t,Finset.mem_biUnion.mpr ⟨s,hs,ht⟩,fit⟩

theorem run_models (p : CNF n) (rows : Layer n) (x : Fin n → Bool) :
    models (run p rows) x ↔ models rows x ∧ passes p x = true := by
  induction p generalizing rows with
  | nil => simp [run,passes]
  | cons c p ih =>
    rw [run,ih,advance_models]
    simp [passes,and_assoc]

theorem initial_models (p : CNF n) (x : Fin n → Bool) :
    models (run p (initial n)) x ↔ passes p x = true := by
  rw [run_models]
  simp [initial,models,fits]

def build (s : Key n) (i : Fin n) (b : Bool) (j : Fin n) : Bool :=
  if j = i then b else decide ((j,true) ∈ s)

private theorem reconstruct {s : Key n} {x : Fin n → Bool} {i : Fin n} {b : Bool}
    (hs : fits s x) (pivot : x i = b) : fits s (build s i b) := by
  rintro ⟨j,v⟩ hj
  have seen : x j = v := hs (j,v) hj
  by_cases eq : j = i
  · subst j
    simpa [build] using pivot.symm.trans seen
  · cases v with
    | true => simp [build,eq,hj]
    | false =>
      have notPos : (j,true) ∉ s := by
        intro pos
        have conflict : x j = true := hs (j,true) pos
        simp [seen] at conflict
      simp [build,eq,notPos]

def keyFits (s : Key n) (x : Fin n → Bool) : Bool :=
  decide ((s.filter (fun a => x a.1 ≠ a.2)) = ∅)

private theorem matches_spec (s : Key n) (x : Fin n → Bool) :
    keyFits s x = true ↔ fits s x := by
  simp [keyFits,Finset.filter_eq_empty_iff,fits]

def branch (rows : Layer n) (i : Fin n) (b : Bool) : Bool :=
  decide ((rows.filter (fun s => keyFits s (build s i b) = true)).Nonempty)

/-- Both bits share the same prefix computation. Querying any branch only
inspects its stored keys and tests their signed marks. -/
def read (p : CNF n) (i : Fin n) : Bool × Bool :=
  let rows := run p (initial n)
  (branch rows i false, branch rows i true)

theorem branch_correct (p : CNF n) (i : Fin n) (b : Bool) :
    branch (run p (initial n)) i b = true ↔ ∃ x, x i = b ∧ passes p x = true := by
  unfold branch
  rw [decide_eq_true_eq]
  constructor
  · rintro ⟨s,hs⟩
    obtain ⟨mem,ok⟩ := Finset.mem_filter.mp hs
    refine ⟨build s i b,by simp [build],(initial_models _ _).mp ?_⟩
    exact ⟨s,mem,(matches_spec _ _).mp ok⟩
  · rintro ⟨x,pivot,ok⟩
    obtain ⟨s,mem,fit⟩ := (initial_models _ _).mpr ok
    exact ⟨s,Finset.mem_filter.mpr ⟨mem,(matches_spec _ _).mpr (reconstruct fit pivot)⟩⟩

theorem pair_correct (p : CNF n) (i : Fin n) (b : Bool) :
    (if b then (read p i).2 else (read p i).1) = true ↔
      ∃ x, x i = b ∧ passes p x = true := by
  cases b <;> exact branch_correct p i _

def attempts : CNF n → Layer n → Nat
  | [],_ => 0
  | c::p,rows => rows.card*c.length + attempts p (advance rows c)

theorem distinct_layers (rows : Layer n) : rows.card ≤ 2^(n*2) := by
  simpa [Key] using (Finset.card_le_univ rows)

theorem attempt_bound (p : CNF n) (rows : Layer n) :
    attempts p rows ≤ 2^(n*2) * (p.map List.length).sum := by
  induction p generalizing rows with
  | nil => simp [attempts]
  | cons c p ih =>
    simp only [attempts,List.map_cons,List.sum_cons,Nat.mul_add]
    exact Nat.add_le_add (Nat.mul_le_mul_right _ (distinct_layers rows)) (ih _)

/-- Three canonical keys survive any further copy after the first two. -/
def firstLayer := advance (initial 4) choiceClause
def stableLayer := advance firstLayer choiceClause

theorem delayed_stabilizes :
    stableLayer.card = 3 ∧ advance stableLayer choiceClause = stableLayer := by decide

private theorem delayed_stable_attempts (k : Nat) :
    attempts (delayed k) stableLayer = 6*k+14 := by
  induction k with
  | zero => decide
  | succ k ih =>
    simp only [delayed,attempts,delayed_stabilizes.1,delayed_stabilizes.2,ih]
    have width : choiceClause.length = 2 := rfl
    rw [width]
    omega

theorem delayed_exact_attempts (k : Nat) :
    attempts (delayed (k+2)) (initial 4) = 6*k+20 := by
  change (initial 4).card * choiceClause.length +
      (firstLayer.card * choiceClause.length + attempts (delayed k) stableLayer) = _
  rw [delayed_stable_attempts]
  have a : (initial 4).card = 1 := by decide
  have b : firstLayer.card = 2 := by decide
  have c : choiceClause.length = 2 := rfl
  rw [a,b,c]
  omega

theorem delayed_branches (k : Nat) : read (delayed k) 0 = (true,true) := by
  apply Prod.ext
  · exact (branch_correct _ _ false).mpr (every_branch_possible k false)
  · exact (branch_correct _ _ true).mpr (every_branch_possible k true)

end Codex.BranchCache
