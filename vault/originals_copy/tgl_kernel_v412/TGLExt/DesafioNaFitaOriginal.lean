import TGLExt.LocalizaARecusa
import TGLExt.CanalDaClausula

/-! The receiver can retain one immutable copy of its formula. All failed
clauses may be selected from that copy. Model selection belongs to the
proposer. The cost below sums only the actual locator sweeps. -/
set_option autoImplicit false
namespace Codex.FixedChallenge
open TGLExt.TraducaoTuring IALD.LeitorDaFormula Codex.ClauseReply
open Codex.PolinomioPorEscolha (original spellClause)
open Codex.ClauseLocator (locate)
variable {n : Nat}

def firstBad (q : CNF n) (x : Assignment n) := q.find? (fun c => !(satisfeita c x))

private theorem inspect_first (x : Assignment n) (q : CNF n) :
    (inspect x q).map Prod.fst = firstBad q x := by
  induction q with
  | nil => rfl
  | cons c q ih =>
    cases h : satisfeita c x <;> cases e : inspect x q <;> simp_all [inspect,firstBad,List.find?]

/-- Execution over a fixed right-hand spelling, including the actual
locator cost of each proposal whose bit tape is ready at its origin. -/
def fixedRun (p : Proposer n) (base : CNF n) : Nat → CNF n → Report n × Nat
  | 0, _ => (⟨.exhausted,[],0⟩,0)
  | k+1, a =>
    match p a with
    | none => (⟨.unsat,[],1⟩,0)
    | some x =>
      let price := (locate (List.ofFn x) [] (original base)).2
      match firstBad base x with
      | none => (⟨.found x,[],1⟩,price)
      | some c =>
        let r := fixedRun p base k (c::a)
        (learned c r.1, price + r.2)

theorem raw_reply (base : CNF n) (x : Assignment n) :
    (locate (List.ofFn x) [] (original base)).1 = (firstBad base x).map spellClause :=
  Codex.ClauseLocator.first_failed base x

private theorem drop_accepted (pre post : CNF n) (c : Clausula n) (x : Assignment n)
    (ok : satisfeita c x = true) :
    firstBad (pre ++ c :: post) x = firstBad (pre ++ post) x := by
  induction pre with
  | nil => simp [firstBad,ok]
  | cons h t ih =>
    cases v : satisfeita h x <;> simp_all [firstBad,List.find?]

private theorem couple (p : Proposer n) (hp : Exact p) (base : CNF n)
    (fuel : Nat) (a q : CNF n)
    (inv : ∀ y, passes a y = true → firstBad base y = firstBad q y) :
    (fixedRun p base fuel a).1 = run p fuel a q := by
  induction fuel generalizing a q with
  | zero => rfl
  | succ k ih =>
    cases prop : p a with
    | none => simp [fixedRun,run,prop]
    | some x =>
      have eq := (inv x (hp.sound _ _ prop)).trans (inspect_first x q).symm
      cases test : inspect x q with
      | none => simp [test] at eq; simp [fixedRun,run,prop,test,eq]
      | some v =>
        obtain ⟨c,rest⟩ := v
        simp [test] at eq
        have nextInv : ∀ y, passes (c::a) y = true → firstBad base y = firstBad rest y := by
          intro y hit
          obtain ⟨_,pre,post,old,new⟩ := inspect_some test
          have h : satisfeita c y = true ∧ passes a y = true := by simpa [passes] using hit
          rw [inv y h.2, old, new, drop_accepted pre post c y h.1]
        simp [fixedRun,run,prop,test,eq,ih _ _ nextInv]

theorem same_protocol (p : Proposer n) (hp : Exact p) (a b : CNF n) :
    (fixedRun p b (b.length+1) a).1 = protocol p a b :=
  couple p hp b _ a b (fun _ _ => rfl)

theorem all_sweeps (p : Proposer n) (b : CNF n) (fuel : Nat) (a : CNF n) :
    (fixedRun p b fuel a).2 ≤ fuel * (8*(original b).length) := by
  induction fuel generalizing a with
  | zero => simp [fixedRun]
  | succ k ih =>
    cases prop : p a with
    | none => simp [fixedRun,prop]
    | some x =>
      have price := Codex.ClauseLocator.input_budget (List.ofFn x) (original b)
      cases test : firstBad b x with
      | none => simp [fixedRun,prop,test,Nat.succ_mul]; omega
      | some c =>
        have tail := ih (c::a)
        change (fixedRun p b (k+1) a).2 ≤ _
        calc
          _ = (locate (List.ofFn x) [] (original b)).2 + (fixedRun p b k (c::a)).2 := by
            simp only [fixedRun,prop,test]
          _ ≤ 8*(original b).length + k*(8*(original b).length) := Nat.add_le_add price tail
          _ = _ := by ring

abbrev Packet := List Codex.PolinomioPorEscolha.Letter

/-- The receiver branches directly on the tape reader's returned packet.
The proposer receives its accumulated packets, newest first. The accounting
field charges locator heads only. No typed clause search runs in rawRun. -/
def rawRun (p : List Packet → Option (Assignment n)) (base : Packet) :
    Nat → List Packet → Verdict n × List Packet × Nat
  | 0, _ => (.exhausted,[],0)
  | k+1, a =>
    match p a with
    | none => (.unsat,[],0)
    | some x =>
      let z := locate (List.ofFn x) [] base
      match z.1 with
      | none => (.found x,[],z.2)
      | some c =>
        let r := rawRun p base k (c::a)
        (r.1,c::r.2.1,z.2+r.2.2)

theorem packet_execution (p : Proposer n) (wire : List Packet → Option (Assignment n))
    (same : ∀ a : CNF n, wire (a.map spellClause) = p a)
    (b : CNF n) (fuel : Nat) (a : CNF n) :
    let r := fixedRun p b fuel a
    rawRun wire (original b) fuel (a.map spellClause) =
      (r.1.result,r.1.replies.map spellClause,r.2) := by
  induction fuel generalizing a with
  | zero => rfl
  | succ k ih =>
    cases h : p a with
    | none => simp [rawRun,fixedRun,same,h]
    | some x =>
      cases test : firstBad b x with
      | none => simp [rawRun,fixedRun,same,h,raw_reply,test]
      | some c =>
        have tail := ih (c::a)
        simp only [List.map_cons] at tail
        simp [rawRun,fixedRun,same,h,raw_reply,test,tail,learned]

end Codex.FixedChallenge
