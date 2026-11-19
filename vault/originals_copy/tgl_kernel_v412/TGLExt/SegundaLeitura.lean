import TGLExt.DuasPassagens

/-! One physical work tape. The signs and the unit-clause obligations observed
on the original input fix a common assignment away from the pivot. -/
set_option autoImplicit false
namespace Codex.SecondRead
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula IALD.LeitorDaFormula
open Codex.PolinomioPorEscolha Codex.SignProfile Codex.TwoSweeps

structure Bits where
  passed : Bool × Bool
  clause : Bool × Bool
  deriving DecidableEq, Repr

def beginBits : Bits := ⟨(true,true),(false,false)⟩

def choose (zero b : Bool) (cell : Cell) := if zero then b else pick cell

def readSign (zero pos : Bool) (cell : Cell) (bits : Bits) : Bits :=
  ⟨bits.passed,
   (bits.clause.1 || (choose zero false cell == pos),
    bits.clause.2 || (choose zero true cell == pos))⟩

def endClause (bits : Bits) : Bits :=
  ⟨(bits.passed.1 && bits.clause.1,bits.passed.2 && bits.clause.2),(false,false)⟩

def evalOp : Op Bits :=
  ⟨fun zero pos _ cell bits => (cell,readSign zero pos cell bits),endClause⟩

def bankValue {n : Nat} (bank : Bank) (b : Bool) (i : Fin n) : Bool :=
  choose (i.val == 0) b (bank i.val)

private theorem literalState {n : Nat} (l : Literal n) (u : Bool) (st : St Bits) :
    applyLit evalOp l u st =
    ⟨st.bank,readSign (l.var.val == 0) l.pos (st.bank l.var.val) st.control,false,0⟩ := by
  simp [applyLit,evalOp]

private theorem literalList {n : Nat} (ls : Clausula n) (st : St Bits) :
    (lits evalOp ls st).bank = st.bank ∧
    (lits evalOp ls st).control = ⟨st.control.passed,
      (st.control.clause.1 || satisfeita ls (bankValue st.bank false),
       st.control.clause.2 || satisfeita ls (bankValue st.bank true))⟩ := by
  induction ls generalizing st with
  | nil =>
    cases st with | mk t q f j => cases q; simp [lits,satisfeita]
  | cons l ls ih =>
    rw [lits,literalState]
    obtain ⟨t,q⟩ := ih ⟨st.bank,readSign (l.var.val == 0) l.pos (st.bank l.var.val) st.control,false,0⟩
    refine ⟨t,?_⟩
    rw [q]
    simp [readSign,satisfeita,Literal.vale,bankValue,Bool.or_assoc]

private theorem evalClauses {n : Nat} (p : CNF n) (st : St Bits)
    (fresh : st.control.clause = (false,false)) :
    (clauses evalOp p st).control.passed =
      (st.control.passed.1 && passes p (bankValue st.bank false),
       st.control.passed.2 && passes p (bankValue st.bank true)) := by
  induction p generalizing st with
  | nil => simp [clauses,passes]
  | cons c p ih =>
    rw [clauses,ih _ rfl]
    obtain ⟨t,q⟩ := literalList c st
    change ((endClause (lits evalOp c st).control).passed.1 &&
        passes p (bankValue (lits evalOp c st).bank false),
      (endClause (lits evalOp c st).control).passed.2 &&
        passes p (bankValue (lits evalOp c st).bank true)) = _
    rw [t,q]
    simp [endClause,fresh,passes,Bool.and_assoc]

def firstSweep (w : List Letter) := scan profileOp w (start emptyBank ())

/-- The two components of home are the final position and its charged distance.
The input head returns on the original, immutable tape. -/
def resume (st : St Unit) : St Bits :=
  ⟨st.bank,beginBits,true,(home st.head).1⟩

def read (w : List Letter) := (scan evalOp (returned w).1 (resume (firstSweep w))).control.passed

def movements (w : List Letter) :=
  travel profileOp w (start emptyBank ()) + (home (firstSweep w).head).2 +
    (returned w).2 + travel evalOp (returned w).1 (resume (firstSweep w))

theorem cost_with_position {Q : Type} (o : Op Q) (w : List Letter) (st : St Q) :
    travel o w st + (scan o w st).head ≤ 3*w.length+st.head := by
  induction w generalizing st with
  | nil => simp [travel,scan]
  | cons a w ih =>
    have h := ih (TwoSweeps.update o a w st)
    cases a <;> simp only [travel,scan,List.length_cons,workMoves,TwoSweeps.update,atSign,home_trace,
      Nat.mul_add,Nat.mul_one] at h ⊢ <;> omega

theorem seven_movements_per_letter (w : List Letter) : movements w ≤ 7*w.length := by
  have a := cost_with_position profileOp w (start emptyBank ())
  have b := cost_with_position evalOp w (resume (firstSweep w))
  change travel profileOp w (start emptyBank ()) + (firstSweep w).head ≤ 3*w.length+0 at a
  simp only [resume,home_trace,Nat.add_zero] at b
  unfold movements
  rw [returned_spec,home_trace]
  dsimp only [Prod.fst,Prod.snd]
  simp only [resume,home_trace] at *
  omega

theorem values_from_tape {n : Nat} (p : CNF (n+1)) :
    read (original p) = (passes p (value p false), passes p (value p true)) := by
  unfold read
  rw [returned_spec]
  have homeZero : (resume (firstSweep (original p))).head = 0 := by simp [resume]
  rw [raw_clauses _ _ _ homeZero,evalClauses _ _ rfl]
  have v (b : Bool) : bankValue (firstSweep (original p)).bank b = value p b := by
    funext i
    simp [bankValue,value,choose,firstSweep,builds_from_letters]
  change (true && passes p (bankValue (firstSweep (original p)).bank false),
          true && passes p (bankValue (firstSweep (original p)).bank true)) = _
  rw [v,v]
  simp

def lane (bits : Bool × Bool) (b : Bool) : Bool := if b then bits.2 else bits.1

theorem lane_is_witness {n : Nat} (p : CNF (n+1)) (b : Bool) :
    lane (read (original p)) b = passes p (value p b) := by
  cases b <;> simp [values_from_tape,lane]

theorem positive_is_sound {n : Nat} (p : CNF (n+1)) (b : Bool)
    (h : lane (read (original p)) b = true) : present p b :=
  witness_sound p b ((lane_is_witness p b).symm.trans h)

theorem branches_exact {n : Nat} {p : CNF (n+1)} (h : covered p) (b : Bool) :
    lane (read (original p)) b = true ↔ present p b := by
  rw [lane_is_witness,witness_complete h b]

theorem word_exact {n : Nat} {p : CNF (n+1)} (h : covered p) :
    ((read (original p)).1 || (read (original p)).2) = palavraDaFormula p := by
  apply Bool.eq_iff_iff.mpr
  rw [Bool.or_eq_true,word_from_pair]
  exact or_congr (branches_exact h false) (branches_exact h true)

/-- A positive output on an arbitrary formula witnesses the Word. -/
theorem word_positive {n : Nat} (p : CNF (n+1))
    (hit : ((read (original p)).1 || (read (original p)).2) = true) :
    palavraDaFormula p = true := by
  apply (word_from_pair p).mpr
  exact (Bool.or_eq_true_iff.mp hit).imp (positive_is_sound p false) (positive_is_sound p true)

theorem certified {n : Nat} {p : CNF (n+1)} (h : covered p) :
    (∀ b : Bool, lane (read (original p)) b = true ↔ present p b) ∧
    (((read (original p)).1 || (read (original p)).2) = palavraDaFormula p) ∧
    movements (original p) ≤ 7 * (original p).length :=
  ⟨branches_exact h,word_exact h,seven_movements_per_letter _⟩

/-- The unit obligation at address 2 is learned from the original letters. -/
example : read [.tick,.tick,.sign false,.delimiter] = (true,true) := by decide

/-- A malformed input ending away from home is charged for returning there. -/
example : movements [.tick,.tick,.tick] = 18 := by decide

def crossed : CNF 3 :=
  [[⟨1,true⟩,⟨2,true⟩],[⟨1,false⟩,⟨2,false⟩]]

theorem opposite_values_missing :
    read (original crossed) = (false,false) ∧ (∀ b : Bool, present crossed b) := by
  constructor
  · decide
  · intro b
    refine ⟨fun i => if i.val = 0 then b else i.val == 1,?_,?_⟩
    · simp
    · rfl

end Codex.SecondRead
