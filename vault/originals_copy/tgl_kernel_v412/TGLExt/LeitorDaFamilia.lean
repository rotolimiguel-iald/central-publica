import TGLExt.LeituraIntegrada

/-! A single read head, fixed finite control, and no supplied assignment.
    Address 0 is read on both polarities. The first occurrence of address 1
    fixes its common value; larger addresses are always true. -/
set_option autoImplicit false
namespace Codex.FamilyHead
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula IALD.LeitorDaFormula
open Codex.PolinomioPorEscolha Codex.CaudaDisjunta Codex.IntegratedRead

inductive Addr where | zero | one | large
deriving DecidableEq
def bump : Addr → Addr | .zero => .one | _ => .large
def classOf : Nat → Addr | 0 => .zero | 1 => .one | _+2 => .large

def assign (b v : Bool) (i : Nat) := match classOf i with
  | .zero => b | .one => v | .large => true
def valAt (b v : Bool) (a : Addr) := match a with
  | .zero => b | .one => v | .large => true

structure Core where
  addr : Addr
  passed : Bool × Bool
  clause : Bool × Bool

def fixedStep (v : Bool) (s : Core) : Letter → Core
  | .tick => {s with addr := bump s.addr}
  | .sign p => ⟨.zero,s.passed,
      (s.clause.1 || (valAt false v s.addr == p),s.clause.2 || (valAt true v s.addr == p))⟩
  | .delimiter => ⟨.zero,(s.passed.1 && s.clause.1,s.passed.2 && s.clause.2),(false,false)⟩

structure Reg where
  core : Core
  pin : Option Bool

def remember (old : Option Bool) (a : Addr) (l : Letter) : Option Bool :=
  match old,a,l with
  | none,.one,.sign p => some p
  | _,_,_ => old

def readLetter (s : Reg) (l : Letter) : Reg :=
  let v := remember s.pin s.core.addr l
  ⟨fixedStep (v.getD true) s.core l,v⟩

def start : Reg := ⟨⟨.zero,(true,true),(false,false)⟩,none⟩
def scanned (w : List Letter) := w.foldl readLetter start
def answer (w : List Letter) := (scanned w).core.passed

private def Compatible (v : Bool) : Option Bool → Prop
  | none => True | some a => v = a
private theorem step_compatible (v : Bool) (s : Reg) (a : Letter)
    (h : Compatible v (readLetter s a).pin) :
    Compatible v s.pin ∧ (readLetter s a).core = fixedStep v s.core a := by
  obtain ⟨⟨d,f,c⟩,o⟩ := s
  cases o <;> cases d <;> cases a <;> simp_all [readLetter,remember,fixedStep,Compatible,valAt]

private theorem stream_compatible (v : Bool) (w : List Letter) (s : Reg)
    (h : Compatible v (w.foldl readLetter s).pin) :
    Compatible v s.pin ∧ (w.foldl readLetter s).core = w.foldl (fixedStep v) s.core := by
  induction w generalizing s with
  | nil => exact ⟨h,rfl⟩
  | cons a w ih =>
    obtain ⟨tail,eq⟩ := ih (readLetter s a) h
    obtain ⟨prev,head⟩ := step_compatible v s a tail
    exact ⟨prev,eq.trans (congrArg (List.foldl (fixedStep v) · w) head)⟩

private theorem ticks (v : Bool) (k : Nat) (f c : Bool × Bool) :
    (List.replicate k Letter.tick).foldl (fixedStep v) ⟨.zero,f,c⟩ = ⟨classOf k,f,c⟩ := by
  induction k with
  | zero => rfl
  | succ k ih =>
    rw [List.replicate_succ',List.foldl_append,ih]
    cases k with
    | zero => rfl
    | succ j => cases j <;> rfl

private theorem literals {n : Nat} (v : Bool) (cs : Clausula n) (f c : Bool × Bool) :
    (cs.flatMap spell).foldl (fixedStep v) ⟨.zero,f,c⟩ =
    ⟨.zero,f,(c.1 || satisfeita cs (fun i => assign false v i.val),
             c.2 || satisfeita cs (fun i => assign true v i.val))⟩ := by
  induction cs generalizing c with
  | nil => simp [satisfeita]
  | cons l cs ih =>
    simp only [List.flatMap_cons,spell,List.foldl_append,ticks,List.foldl_cons,List.foldl_nil,fixedStep,ih]
    simp [satisfeita,Literal.vale,Bool.or_assoc,assign,valAt]

private theorem formula {n : Nat} (v : Bool) (p : CNF n) (f : Bool × Bool) :
    (original p).foldl (fixedStep v) ⟨.zero,f,(false,false)⟩ =
    ⟨.zero,(f.1 && passes p (fun i => assign false v i.val),
            f.2 && passes p (fun i => assign true v i.val)),(false,false)⟩ := by
  induction p generalizing f with
  | nil => simp [original,passes]
  | cons c p ih =>
    change ((c.flatMap spell ++ [Letter.delimiter]) ++ original p).foldl _ _ = _
    simp only [List.foldl_append,literals,List.foldl_cons,List.foldl_nil,fixedStep,Bool.false_or,ih]
    simp [passes,Bool.and_assoc]

/-- Both bits share the same assignment to every address other than zero. -/
theorem answer_spec {n : Nat} (p : CNF n) :
    let v := (scanned (original p)).pin.getD true
    answer (original p) = (passes p (fun i => assign false v i.val),
                             passes p (fun i => assign true v i.val)) := by
  let s := scanned (original p)
  have ok : Compatible (s.pin.getD true) s.pin := by cases s.pin <;> simp [Compatible]
  have h := (stream_compatible (s.pin.getD true) (original p) start ok).2
  change (scanned (original p)).core = (original p).foldl _ ⟨.zero,(true,true),(false,false)⟩ at h
  rw [formula] at h
  simpa [answer,s] using congrArg Core.passed h

theorem scan_accepts {n : Nat} (p : CNF n) (hit : (answer (original p)).1 || (answer (original p)).2) :
    palavraDaFormula p = true := by
  rw [answer_spec] at hit
  apply (a_palavra_e_o_sat _).mpr
  apply (sat_iff _).mpr
  rcases Bool.or_eq_true_iff.mp hit with h|h
  · exact ⟨_,h⟩
  · exact ⟨_,h⟩

inductive Machine where
  | walk (state : Reg) (unread : List Letter)
  | halt (bits : Bool × Bool)

def step : Machine → Machine
  | .walk s (a::w) => .walk (readLetter s a) w
  | .walk s [] => .halt s.core.passed
  | .halt b => .halt b
def move : Machine → Nat
  | .walk _ (_::_) => 1
  | _ => 0
def travel : Nat → Machine → Nat
  | 0,_ => 0
  | k+1,s => move s + travel k (step s)

theorem exactly_one_pass (w : List Letter) (s : Reg) :
    step^[w.length+1] (.walk s w) = .halt (w.foldl readLetter s).core.passed ∧
    travel (w.length+1) (.walk s w) = w.length := by
  induction w generalizing s with
  | nil => exact ⟨rfl,rfl⟩
  | cons a w ih =>
    obtain ⟨halted,moves⟩ := ih (readLetter s a)
    constructor
    · change step^[w.length+1+1] _ = _
      rw [Function.iterate_succ_apply]
      exact halted
    · change 1 + travel (w.length+1) (.walk (readLetter s a) w) = w.length+1
      omega

private theorem latch_kept (w : List Letter) (s : Reg) (v : Bool) (h : s.pin = some v) :
    (w.foldl readLetter s).pin = some v := by
  induction w generalizing s with
  | nil => exact h
  | cons l w ih =>
    apply ih (readLetter s l)
    simp [readLetter,remember,h]

private theorem coupled_header (m : Nat) :
    ∃ tail, original (coupled (m+2)) = Letter.sign false :: .tick :: .sign false :: tail := by
  unfold coupled original coupling
  simp [List.finRange_succ,List.flatMap_cons,spellClause,spell,left]

private theorem coupled_pin (m : Nat) : (scanned (original (coupled (m+2)))).pin = some false := by
  obtain ⟨tail,h⟩ := coupled_header m
  unfold scanned
  rw [h]
  apply latch_kept tail
  rfl

private theorem coupled_large {m : Nat} (b : Bool) :
    passes (coupled (m+2)) (fun i => assign b false i.val) = true := by
  apply List.all_eq_true.mpr
  intro c hc
  rcases List.mem_cons.mp hc with rfl | hp
  · apply List.any_eq_true.mpr
    let i : Fin (m+2) := ⟨1,by omega⟩
    refine ⟨⟨left i,false⟩,(common_label i).1,?_⟩
    rfl
  · obtain ⟨i,_,rfl⟩ := List.mem_map.mp hp
    apply List.any_eq_true.mpr
    refine ⟨⟨right i,true⟩,by simp [pairClause],?_⟩
    have hg : 2 ≤ (right i).val := by simp only [right,Fin.val_natAdd]; omega
    obtain ⟨d,hd⟩ := Nat.exists_eq_add_of_le hg
    simp [Literal.vale,hd,assign,classOf,Nat.add_comm 2 d]

/-- A single pass on the `coupled` family of `LeituraIntegrada`. For a lone pair only the
false branch can satisfy; with two or more pairs both branches have a witness. -/
theorem coupled_outputs (m : Nat) :
    answer (original (coupled (m+1))) = (true,decide (0 < m)) := by
  cases m with
  | zero => rfl
  | succ m =>
    rw [answer_spec,coupled_pin m]
    simp [coupled_large]

theorem coupled_linear (m : Nat) :
    let p := coupled (m+1)
    step^[(original p).length+1] (.walk start (original p)) = .halt (true,decide (0 < m)) ∧
    travel ((original p).length+1) (.walk start (original p)) = (original p).length ∧
    palavraDaFormula p = true := by
  obtain ⟨h,t⟩ := exactly_one_pass (original (coupled (m+1))) start
  change step^[_] _ = .halt (answer _) at h
  rw [coupled_outputs] at h
  exact ⟨h,t,mixed_witness m⟩

/-- At a clause boundary the control state continues in place. -/
theorem next_clause {n : Nat} (p : CNF n) (c : Clausula n) :
    scanned (original (p ++ [c])) = (spellClause c).foldl readLetter (scanned (original p)) := by
  simp [scanned,original,List.foldl_append]

/-- When the new clause first fixes the shared value at address 1, the previous
two acceptance bits still describe the prefix at that new value. -/
theorem survivor_transition {n : Nat} (p : CNF n) (c : Clausula n) :
    let v := (scanned (original (p ++ [c]))).pin.getD true
    let before := answer (original p)
    answer (original (p ++ [c])) =
      (before.1 && satisfeita c (fun i => assign false v i.val),
       before.2 && satisfeita c (fun i => assign true v i.val)) := by
  let final := scanned (original (p ++ [c]))
  let v := final.pin.getD true
  have ok : Compatible v final.pin := by
    change Compatible (final.pin.getD true) final.pin
    cases final.pin <;> simp [Compatible]
  have continued : final = (spellClause c).foldl readLetter (scanned (original p)) := next_clause p c
  have prefixOK := (stream_compatible v (spellClause c) (scanned (original p))
    (by rw [← continued]; exact ok)).1
  have old := (stream_compatible v (original p) start prefixOK).2
  change (scanned (original p)).core = (original p).foldl _ ⟨.zero,(true,true),(false,false)⟩ at old
  rw [formula] at old
  have before : answer (original p) = (passes p (fun i => assign false v i.val),
      passes p (fun i => assign true v i.val)) := by
    simpa [answer] using congrArg Core.passed old
  dsimp only
  rw [answer_spec,before]
  simp [v,final,passes]

def lane (bs : Bool × Bool) (b : Bool) := if b then bs.2 else bs.1

def HasBranch {n : Nat} (p : CNF n) (b : Bool) : Prop :=
  ∃ x : Fin n → Bool, (∀ i, i.val = 0 → x i = b) ∧ passes p x = true

theorem branch_witness {n : Nat} (p : CNF n) (b : Bool)
    (hit : lane (answer (original p)) b = true) : HasBranch p b := by
  let v := (scanned (original p)).pin.getD true
  refine ⟨fun i => assign b v i.val,?_,?_⟩
  · intro i hi
    simp [hi,assign,classOf]
  · rw [answer_spec] at hit
    cases b <;> simpa [v,lane] using hit

/-- On this family the scan recovers the exact feasibility of each branch,
including exclusion of the positive branch for the single pair. -/
theorem coupled_exact_lanes (m : Nat) (b : Bool) :
    lane (answer (original (coupled (m+1)))) b = true ↔ HasBranch (coupled (m+1)) b := by
  constructor
  · exact branch_witness _ _
  · intro h
    rw [coupled_outputs]
    cases m with
    | zero =>
      cases b with
      | false => rfl
      | true =>
        obtain ⟨x,hx,yes⟩ := h
        have h0 : x (0 : Fin 2) = true := hx 0 rfl
        have hn := List.all_eq_true.mp yes (coupling 1) List.mem_cons_self
        rw [show coupling 1 = [⟨(0 : Fin 2),false⟩] from rfl] at hn
        simp [satisfeita,Literal.vale,h0] at hn
    | succ m => cases b <;> simp [lane]

end Codex.FamilyHead
