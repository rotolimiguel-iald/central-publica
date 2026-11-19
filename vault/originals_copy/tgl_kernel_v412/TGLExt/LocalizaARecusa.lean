import TGLExt.EcoDaAtribuicao

/-! Locate and deliver the first failed clause on the raw input. While
reading a record, append its letters on two fresh scratch tracks. At its
delimiter, rewind the first scratch head and check the record against the
supplied assignment. After an accepted clause that head is at its new
blank and the assignment is back at its origin (the final literal ends
in a sign, or the clause was empty). The other writer remains at the new
blank. After a refusal, rewind the second track to present the full clause
to the sender. Rewinds stop at the previous delimiter or the left margin.
The reversed prefix is the zipper view of both identically written tracks.
Payloads include the trailing delimiter. Lists in the result describe
what is present on the output tape at its head. -/
set_option autoImplicit false
namespace Codex.ClauseLocator
open TGLExt.TraducaoTuring IALD.LeitorDaFormula Codex.PolinomioPorEscolha
open Codex.EcoDaAtribuicao (verify verify_assignment at_most_three)
open Codex.BranchCircuit (rewind rewind_trace)

abbrev Output := Option (List Letter) × Nat

def debit (k : Nat) (o : Output) : Output := (o.1,k+o.2)

def locate (bits : List Bool) (written : List Letter) : List Letter → Output
  | [] => (none,0)
  | a::w =>
    if a = .delimiter then
      let checked := rewind (a::written) []
      let v := verify checked.1 bits
      if v.1 then debit (3+checked.2+v.2) (locate bits [] w)
      else
        let output := rewind (a::written) []
        (some output.1, 3+checked.2+v.2+output.2)
    else debit 3 (locate bits (a::written) w)

private theorem travel (bits w written) :
    (locate bits written w).2 ≤ 8*w.length+5*written.length := by
  induction w generalizing written with
  | nil => simp [locate]
  | cons a w ih =>
    by_cases hd : a = .delimiter
    · subst a
      have hv := at_most_three ((Letter.delimiter::written).reverse) bits
      simp only [List.length_reverse,List.length_cons] at hv
      have next := ih []
      simp only [List.length_nil] at next
      rw [List.reverse_cons] at hv
      cases h : (verify (written.reverse++[Letter.delimiter]) bits).1 <;>
        simp [locate,debit,rewind_trace,h] <;> omega
    · have next := ih (a::written)
      simp only [List.length_cons] at next
      simp [locate,debit,hd]
      omega

theorem input_budget (bits : List Bool) (w : List Letter) :
    (locate bits [] w).2 ≤ 8*w.length := by simpa using travel bits w []

private theorem before_delimiter (bits : List Bool) (z w : List Letter)
    (clean : Letter.delimiter ∉ z) (buf : List Letter) :
    (locate bits buf (z++w)).1 = (locate bits (z.reverse++buf) w).1 := by
  induction z generalizing buf with
  | nil => simp
  | cons a zs ih =>
    have ha : a ≠ .delimiter := fun e => clean (by simp [e])
    have hc : Letter.delimiter ∉ zs := fun x => clean (List.mem_cons_of_mem _ x)
    simpa [locate,ha,debit,List.append_assoc] using ih hc (a::buf)

theorem first_failed {n : Nat} (q : CNF n) (x : Fin n → Bool) :
    (locate (List.ofFn x) [] (original q)).1 =
      (q.find? (fun c => !(satisfeita c x))).map spellClause := by
  induction q with
  | nil => rfl
  | cons c q ih =>
    let body := c.flatMap spell
    have clean : Letter.delimiter ∉ body := by simp [body,spell]
    have val : (verify (spellClause c) (List.ofFn x)).1 = satisfeita c x := by
      simpa [original,passes] using verify_assignment [c] x
    have sync : (Letter.delimiter :: body.reverse).reverse = spellClause c := by
      simp [body,spellClause]
    change (locate (List.ofFn x) [] ((body++[.delimiter])++original q)).1 = _
    rw [List.append_assoc,before_delimiter _ _ _ clean]
    cases h : satisfeita c x <;>
      simp [locate,debit,rewind_trace,sync,val,h,ih,List.find?]

end Codex.ClauseLocator
