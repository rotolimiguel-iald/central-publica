import TGLExt.SegundaLeitura
import TGLExt.GuardaDoPerfil
import TGLExt.AtualizaONome

/-! The second traversal updates the two witness bits and the coverage check
in one finite control. Each transition reads the very same work-tape cell. -/
set_option autoImplicit false
namespace Codex.CertifiedRead
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula IALD.LeitorDaFormula
open Codex.PolinomioPorEscolha Codex.SignProfile Codex.TwoSweeps
open Codex.SecondRead Codex.ProfileGuard

def combinedOp : Op (Bits × Bool) where
  literal zero pos unit cell q :=
    (cell, (evalOp.literal zero pos unit cell q.1).2,
           (guardOp.literal zero pos unit cell q.2).2)
  boundary q := (evalOp.boundary q.1, guardOp.boundary q.2)

private def witnessState (st : St (Bits × Bool)) : St Bits :=
  ⟨st.bank,st.control.1,st.first,st.head⟩

private def guardState (st : St (Bits × Bool)) : St Bool :=
  ⟨st.bank,st.control.2,st.first,st.head⟩

private theorem witnessStep (a : Letter) (next : List Letter) (st : St (Bits × Bool)) :
    witnessState (TwoSweeps.update combinedOp a next st) =
      TwoSweeps.update evalOp a next (witnessState st) := by
  cases a <;> rfl

private theorem guardStep (a : Letter) (next : List Letter) (st : St (Bits × Bool)) :
    guardState (TwoSweeps.update combinedOp a next st) =
      TwoSweeps.update guardOp a next (guardState st) := by
  cases a <;> rfl

private theorem projectWitness (w : List Letter) (st : St (Bits × Bool)) :
    witnessState (scan combinedOp w st) = scan evalOp w (witnessState st) := by
  induction w generalizing st with
  | nil => rfl
  | cons a w ih => simp only [scan,ih,witnessStep]

private theorem projectGuard (w : List Letter) (st : St (Bits × Bool)) :
    guardState (scan combinedOp w st) = scan guardOp w (guardState st) := by
  induction w generalizing st with
  | nil => rfl
  | cons a w ih => simp only [scan,ih,guardStep]

def resumeTogether (st : St Unit) : St (Bits × Bool) :=
  ⟨st.bank,(beginBits,true),true,(home st.head).1⟩

/-- Computed bits and guard after the second sweep of the original spelling. -/
def readTape (w : List Letter) : (Bool × Bool) × Bool :=
  let q := (scan combinedOp (returned w).1 (resumeTogether (firstSweep w))).control
  (q.1.passed, q.2)

theorem witness_projection (w : List Letter) : (readTape w).1 = SecondRead.read w :=
  congrArg (fun st : St Bits => st.control.passed)
    (projectWitness (returned w).1 (resumeTogether (firstSweep w)))

theorem guard_projection {n : Nat} (p : CNF (n+1)) :
    (readTape (original p)).2 = true ↔ covered p := by
  have h := congrArg (fun st : St Bool => st.control)
    (projectGuard (returned (original p)).1 (resumeTogether (firstSweep (original p))))
  change (readTape (original p)).2 = _ at h
  rw [h,returned_spec]
  have bank : (firstSweep (original p)).bank = profile p := builds_from_letters p
  simpa only [guardState,resumeTogether,home_trace,bank,start] using guard_exact p

def headMovements (w : List Letter) : Nat :=
  travel profileOp w (start emptyBank ()) + (home (firstSweep w).head).2 +
    (returned w).2 + travel combinedOp (returned w).1 (resumeTogether (firstSweep w))

theorem at_most_seven_per_letter (w : List Letter) : headMovements w ≤ 7*w.length := by
  have first := cost_with_position profileOp w (start emptyBank ())
  have second := cost_with_position combinedOp w (resumeTogether (firstSweep w))
  change travel profileOp w (start emptyBank ()) + (firstSweep w).head ≤ 3*w.length+0 at first
  simp only [resumeTogether,home_trace,Nat.add_zero] at second
  unfold headMovements
  rw [returned_spec,home_trace]
  dsimp only [Prod.fst,Prod.snd]
  simp only [resumeTogether,home_trace] at *
  omega

/-- A witnessed branch stays positive even if coverage is false. -/
def classify (observed : (Bool × Bool) × Bool) (b : Bool) : Option Bool :=
  if lane observed.1 b then some true else if observed.2 then some false else none

theorem positive_iff (observed : (Bool × Bool) × Bool) (b : Bool) :
    classify observed b = some true ↔ lane observed.1 b = true := by
  unfold classify
  cases lane observed.1 b <;> cases observed.2 <;> decide

theorem negative_iff (observed : (Bool × Bool) × Bool) (b : Bool) :
    classify observed b = some false ↔ lane observed.1 b = false ∧ observed.2 = true := by
  unfold classify
  cases lane observed.1 b <;> cases observed.2 <;> decide

theorem unknown_iff (observed : (Bool × Bool) × Bool) (b : Bool) :
    classify observed b = none ↔ lane observed.1 b = false ∧ observed.2 = false := by
  unfold classify
  cases lane observed.1 b <;> cases observed.2 <;> decide

theorem positive_sound {n : Nat} (p : CNF (n+1)) (b : Bool)
    (h : classify (readTape (original p)) b = some true) : present p b := by
  have hit := (positive_iff _ _).mp h
  rw [witness_projection] at hit
  exact positive_is_sound p b hit

theorem negative_sound {n : Nat} (p : CNF (n+1)) (b : Bool)
    (h : classify (readTape (original p)) b = some false) : ¬present p b := by
  obtain ⟨miss,guarded⟩ := (negative_iff _ _).mp h
  rw [witness_projection] at miss
  intro hx
  have hit := (branches_exact ((guard_projection p).mp guarded) b).mpr hx
  simp [miss] at hit

theorem classified_when_covered {n : Nat} {p : CNF (n+1)} (g : covered p) (b : Bool) :
    classify (readTape (original p)) b =
      some (lane (SecondRead.read (original p)) b) := by
  simp only [classify,witness_projection,(guard_projection p).mpr g]
  cases lane (SecondRead.read (original p)) b <;> rfl

open Codex.BranchPresence (Compatible search search_correct) in
theorem branch_search_exact {n : Nat} (p : CNF (n+1)) (b : Bool) :
    search p [⟨0,b⟩] = true ↔ present p b := by
  rw [search_correct]
  simp [Compatible,BranchPresence.Agrees,present,and_comm]

/-- The continuation is evaluated only on an unresolved branch. -/
def resolve {n : Nat} (p : CNF (n+1)) (b : Bool) (answer : Option Bool) : Bool :=
  match answer with
  | some v => v
  | none => BranchPresence.search p [⟨0,b⟩]

theorem resolve_exact {n : Nat} (p : CNF (n+1)) (b : Bool) :
    resolve p b (classify (readTape (original p)) b) = true ↔ present p b := by
  cases h : classify (readTape (original p)) b with
  | none => exact branch_search_exact p b
  | some v =>
    cases v with
    | false => simp [resolve,negative_sound p b h]
    | true => simp [resolve,positive_sound p b h]

def exactWord {n : Nat} (p : CNF (n+1)) : Bool :=
  let observed := readTape (original p)
  resolve p false (classify observed false) || resolve p true (classify observed true)

theorem whole_word_exact {n : Nat} (p : CNF (n+1)) :
    exactWord p = palavraDaFormula p := by
  apply Bool.eq_iff_iff.mpr
  simp only [exactWord,Bool.or_eq_true,resolve_exact,word_from_pair]

/-- With no address, there is no pivot to label. The unmarked decision has
the same Word semantics as the branch classifier and its continuation. -/
def decision : {n : Nat} → CNF n → Bool
  | 0,p => BranchPresence.search p []
  | _+1,p => exactWord p

theorem decision_exact {n : Nat} (p : CNF n) : decision p = palavraDaFormula p := by
  cases n with
  | zero =>
    apply Bool.eq_iff_iff.mpr
    change BranchPresence.search p [] = true ↔ _
    rw [BranchPresence.search_correct,a_palavra_e_o_sat,sat_iff]
    simp [BranchPresence.Compatible,BranchPresence.Agrees]
  | succ k => exact whole_word_exact p

/-- Pivot true has a witnessed branch. Pivot false remains open, even though
the two branches receive the identical coverage result. -/
def mixedExample : CNF 3 :=
  [[⟨0,true⟩,⟨1,true⟩,⟨2,true⟩],[⟨0,true⟩,⟨1,false⟩,⟨2,false⟩]]

theorem mixed_outcomes :
    classify (readTape (original mixedExample)) false = none ∧
    classify (readTape (original mixedExample)) true = some true := by decide

def linked (equal : Bool) : CNF 2 :=
  [[⟨0,false⟩,⟨1,equal⟩],[⟨0,true⟩,⟨1,!equal⟩]]

def forceSecond : Clausula 2 := [⟨1,true⟩]

theorem before_unit_both_branches (equal b : Bool) : present (linked equal) b := by
  refine ⟨fun i => if i.val = 0 then b else (b == equal),?_,?_⟩
  · simp
  · cases equal <;> cases b <;> rfl

theorem unit_selects_opposite_branches :
    readTape (original (linked true ++ [forceSecond])) = ((false,true),true) ∧
    readTape (original (linked false ++ [forceSecond])) = ((true,false),true) := by decide

end Codex.CertifiedRead
