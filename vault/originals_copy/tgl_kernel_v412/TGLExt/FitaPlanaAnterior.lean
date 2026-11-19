import TGLExt.PolinomioPorEscolha
import TGLExt.VerboNaFita

set_option autoImplicit false
namespace Codex.FlatTapeBridge
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula
open Codex.PolinomioPorEscolha Codex.CrossSelectors Codex.SparseHornTape

def symbol : Letter → IALD.VerbTape.Symbol
  | .tick => .mark
  | .sign b => if b then .positive else .negative
  | .delimiter => .close

def letter : IALD.VerbTape.Symbol → Letter
  | .mark => .tick
  | .positive => .sign true
  | .negative => .sign false
  | .close => .delimiter

theorem same_alphabet : Function.LeftInverse letter symbol ∧ Function.RightInverse letter symbol := by
  constructor
  · intro s
    cases s with
    | tick => rfl
    | delimiter => rfl
    | sign b => cases b <;> rfl
  · intro s; cases s <;> rfl

variable {n : Nat}

theorem same_tape (p : CNF n) : (original p).map symbol = IALD.VerbTape.tape p := by
  have lit (l : Literal n) :
      (spell l).map symbol = IALD.VerbTape.litLetters l.var.val l.pos := by
    simp [spell,IALD.VerbTape.litLetters,symbol]
  have clause (c : Clausula n) :
      ((c.flatMap spell).map symbol) = IALD.VerbTape.letters c := by
    induction c with
    | nil => rfl
    | cons l c ih =>
      change ((spell l ++ c.flatMap spell).map symbol) = _
      rw [List.map_append,lit,ih]
      rfl
  induction p with
  | nil => rfl
  | cons c p ih =>
    change ((spellClause c ++ original p).map symbol) = _
    rw [List.map_append,ih]
    simp only [spellClause,List.map_append,clause,List.map_cons,List.map_nil,symbol]
    rfl

/-- The same length L that charges the flat tape of `VerboNaFita` for the Verb also charges
    the Word for every supplied legal choice, with no change in addresses or padding. -/
theorem word_on_previous_letters (p : CNF n) :
    let L := (IALD.VerbTape.tape p).length
    palavraDaFormula p = true ↔ ∃ q ∈ programs p, (program q).length ≤ L ∧
      ∃ T ≤ budget L, travel T (start q ∅) ≤ 2*budget L ∧ (run T (start q ∅)).mode = .halt true := by
  have len : (IALD.VerbTape.tape p).length = (original p).length := by
    rw [← same_tape,List.length_map]
  simpa only [len] using word_iff_bounded_selection p

end Codex.FlatTapeBridge
