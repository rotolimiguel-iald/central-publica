import TGLExt.DuasPassagens

/-! A general CNF on the original unary input tape; a finite, read-only bit
tape supplied by the caller. The second head starts on its first bit. Its
left boundary is the empty left stack. Reuse the local one-cell rewind.
A move is one head moving by one cell; a tick moves both heads. -/
set_option autoImplicit false
namespace Codex.EcoDaAtribuicao
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula IALD.LeitorDaFormula
open Codex.PolinomioPorEscolha (Letter spell spellClause original)
open Codex.BranchCircuit (rewind rewind_trace)

private def charge (k : Nat) (r : Bool × Nat) : Bool × Nat := (r.1,k+r.2)

/-- The output pairs the decision with the measured head movements.
An exhausted echo at a required cell rejects. The left stack consists of
the very bits traversed, in reverse order, and the right starts at the head. -/
def scan : List Letter → List Bool → List Bool → Bool → Bool → Bool × Nat
  | [], _, _, ok, _ => (ok, 0)
  | .tick :: _, _, [], _, _ => (false, 1)
  | .tick :: w, left, b :: right, ok, hit =>
    charge 2 (scan w (b :: left) right ok hit)
  | .sign _ :: _, _, [], _, _ => (false, 1)
  | .sign s :: w, left, b :: right, ok, hit =>
    let home := rewind left (b :: right)
    charge (1 + home.2) (scan w [] home.1 ok (hit || (b == s)))
  | .delimiter :: w, left, right, ok, hit =>
    charge 1 (scan w left right (ok && hit) false)

def verify (w : List Letter) (bits : List Bool) : Bool × Nat :=
  scan w [] bits true false

private theorem ticks (pre right left : List Bool) (w : List Letter) (ok hit : Bool) :
    (scan (List.replicate pre.length .tick ++ w) left (pre ++ right) ok hit).1 =
      (scan w (pre.reverse ++ left) right ok hit).1 := by
  induction pre generalizing left with
  | nil => simp
  | cons b pre ih =>
    simp only [List.length_cons,List.replicate_succ,List.cons_append,scan,charge,
      List.reverse_cons,List.append_assoc]
    exact ih (b :: left)

private theorem at_literal {n : Nat} (l : Literal n) (x : Fin n → Bool)
    (w : List Letter) (ok hit : Bool) :
    (scan (spell l ++ w) [] (List.ofFn x) ok hit).1 =
      (scan w [] (List.ofFn x) ok (hit || l.vale x)).1 := by
  let bits := List.ofFn x
  let i := l.var.val
  let pre := bits.take i
  let tail := bits.drop (i+1)
  have hi : i < bits.length := by simp [i,bits]
  have len : pre.length = i := List.length_take_of_le (Nat.le_of_lt hi)
  have decomp : pre ++ x l.var :: tail = bits := by
    have cut := List.drop_eq_getElem_cons hi
    have bit : bits[i] = x l.var := by simp [bits,i]
    rw [bit] at cut
    change bits.take i ++ x l.var :: bits.drop (i+1) = bits
    rw [← cut,List.take_append_drop]
  change (scan ((List.replicate i .tick ++ [.sign l.pos]) ++ w) [] bits ok hit).1 = _
  rw [List.append_assoc,List.singleton_append]
  conv_lhs => rw [← len,← decomp]
  rw [ticks]
  simp only [List.append_nil,scan,charge,rewind_trace,List.reverse_reverse,decomp,Literal.vale]
  rfl

private theorem clause {n : Nat} (c : Clausula n) (x : Fin n → Bool)
    (w : List Letter) (ok hit : Bool) :
    (scan (c.flatMap spell ++ w) [] (List.ofFn x) ok hit).1 =
      (scan w [] (List.ofFn x) ok (hit || satisfeita c x)).1 := by
  induction c generalizing hit with
  | nil => simp [satisfeita]
  | cons l c ih =>
    rw [List.flatMap_cons,List.append_assoc,at_literal,ih]
    simp [satisfeita,Bool.or_assoc]

private theorem formula {n : Nat} (p : CNF n) (x : Fin n → Bool) (ok : Bool) :
    (scan (original p) [] (List.ofFn x) ok false).1 = (ok && passes p x) := by
  induction p generalizing ok with
  | nil => simp [original,scan,passes]
  | cons c p ih =>
    change (scan ((c.flatMap spell ++ [.delimiter]) ++ original p) [] (List.ofFn x) ok false).1 = _
    rw [List.append_assoc,List.singleton_append,clause]
    change (scan (original p) [] (List.ofFn x) (ok && (false || satisfeita c x)) false).1 = _
    simp [ih,passes,Bool.and_assoc]

/-- Valid for every CNF, including n = 0, empty formulas and empty clauses. -/
theorem verify_assignment {n : Nat} (p : CNF n) (x : Fin n → Bool) :
    (verify (original p) (List.ofFn x)).1 = passes p x := by
  simpa [verify] using formula p x true

private theorem travel (w : List Letter) (left right : List Bool) (ok hit : Bool) :
    (scan w left right ok hit).2 ≤ 3 * w.length + left.length := by
  induction w generalizing left right ok hit with
  | nil => simp [scan]
  | cons a w ih =>
    cases a with
    | delimiter =>
      have h := ih left right (ok && hit) false
      simp only [scan,charge,List.length_cons] at *
      omega
    | tick =>
      cases right with
      | nil => simp [scan]; omega
      | cons b right =>
        have h := ih (b :: left) right ok hit
        simp only [scan,charge,List.length_cons] at *
        omega
    | sign s =>
      cases right with
      | nil => simp [scan]; omega
      | cons b right =>
        have h := ih [] (left.reverse ++ b :: right) ok (hit || (b == s))
        simp only [scan,charge,rewind_trace,List.length_cons,List.length_nil] at *
        omega

/-- On either answer, at most three movements per original input symbol.
The echo is already on the second tape; its production is outside this bound. -/
theorem at_most_three (w : List Letter) (bits : List Bool) :
    (verify w bits).2 ≤ 3*w.length := by
  simpa [verify] using travel w [] bits true false

/-- Existence of a length-n bit string accepted by this verifier. -/
theorem word_iff_echo {n : Nat} (p : CNF n) :
    palavraDaFormula p = true ↔
      ∃ bits : List Bool, bits.length = n ∧ (verify (original p) bits).1 = true := by
  rw [a_palavra_e_o_sat,sat_iff]
  constructor
  · rintro ⟨x,h⟩
    exact ⟨List.ofFn x,List.length_ofFn, (verify_assignment p x).trans h⟩
  · rintro ⟨bits,rfl,h⟩
    let x : Fin bits.length → Bool := fun i => bits[i.val]
    have rep : List.ofFn x = bits := List.ofFn_getElem
    exact ⟨x,by rwa [← verify_assignment,rep]⟩

end Codex.EcoDaAtribuicao
