import AtualizaONome
import PolinomioPorEscolha

/-! Count leaf consistency checks in the direct short-circuit search. Each
literal of an unsatisfied alternative is charged even with short-circuit. -/
set_option autoImplicit false
namespace Codex.LiteralSearchCost
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula Codex.BranchPresence
open Codex.PolinomioPorEscolha

def firstSuccess {α : Type} (visit : α → Bool × Nat) : List α → Bool × Nat
  | [] => (false,0)
  | a::ls =>
    let v := visit a
    if v.1 then v else
      let tail := firstSuccess visit ls
      (tail.1,v.2+tail.2)

theorem first_spec {α} (visit : α → Bool × Nat) (ls : List α) :
    (firstSuccess visit ls).1 = ls.any (fun l => (visit l).1) := by
  induction ls with
  | nil => rfl
  | cons a ls ih => cases e : (visit a).1 <;> simp [firstSuccess,e,ih]

def traced {n : Nat} : CNF n → List (Literal n) → Bool × Nat
  | [],ms => (consistent ms,1)
  | c::p,ms => firstSuccess (fun l => traced p (l::ms)) c

theorem traced_spec {n} (p : CNF n) (ms : List (Literal n)) :
    (traced p ms).1 = search p ms := by
  induction p generalizing ms with
  | nil => rfl
  | cons c p ih => simp [traced,first_spec,ih,search]

def pos (i : Fin 3) : Literal 3 := ⟨i,true⟩
def neg (i : Fin 3) : Literal 3 := ⟨i,false⟩
def hard : Nat → CNF 3
  | 0 => [[pos 2],[neg 2]]
  | k+1 => [pos 0,pos 1] :: hard k

private theorem contradiction (ms : List (Literal 3)) :
    consistent (neg 2 :: pos 2 :: ms) = false := by
  cases h : consistent (neg 2 :: pos 2 :: ms) with
  | false => rfl
  | true =>
    obtain ⟨x,_,hx⟩ := consistent_correct _ |>.mp h
    have h₀ := hx (neg 2) (by simp)
    have h₁ := hx (pos 2) (by simp)
    simp [neg,pos] at h₀ h₁
    simp [h₀] at h₁

/-- No masking loop and no repeated literal inside a clause. Each alternative
fails only after its recursive call. The count is of leaves of THIS search. -/
theorem visits_all_alternatives (k : Nat) (ms : List (Literal 3)) :
    traced (hard k) ms = (false,2^k) := by
  induction k generalizing ms with
  | zero => simp [hard,traced,firstSuccess,contradiction]
  | succ k ih => simp [hard,traced,firstSuccess,ih,pow_succ,Nat.mul_two]

theorem input_letters (k : Nat) : (original (hard k)).length = 4*k+8 := by
  induction k with
  | zero => decide
  | succ k ih =>
    change (spellClause [pos 0,pos 1] ++ original (hard k)).length = _
    rw [List.length_append,ih]
    have first : (spellClause [pos 0,pos 1]).length = 4 := by decide
    omega

end Codex.LiteralSearchCost
#print axioms Codex.LiteralSearchCost.traced_spec
#print axioms Codex.LiteralSearchCost.visits_all_alternatives
#print axioms Codex.LiteralSearchCost.input_letters

