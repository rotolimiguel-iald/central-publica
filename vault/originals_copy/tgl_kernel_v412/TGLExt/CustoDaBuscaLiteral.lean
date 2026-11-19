import TGLExt.AtualizaONome
import TGLExt.PolinomioPorEscolha
import TGLExt.PerfilDeSinais

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

open IALD.LeitorDaFormula (passes)
def choiceClause : Clausula 4 := [⟨1,true⟩,⟨2,true⟩]
def suffix : CNF 4 := [[⟨1,false⟩,⟨3,true⟩],[⟨1,false⟩,⟨3,false⟩]]
def delayed : Nat → CNF 4
  | 0 => suffix
  | k+1 => choiceClause :: delayed k

private theorem forces_low (k : Nat) (x : Fin 4 → Bool) (h : passes (delayed k) x = true) :
    x 1 = false := by
  induction k with
  | zero =>
    cases a : x 1 <;> cases b : x 3 <;> simp_all [delayed,suffix,passes,satisfeita,Literal.vale]
  | succ k ih =>
    have both : satisfeita choiceClause x = true ∧ passes (delayed k) x = true := by
      simpa only [delayed,passes,List.all_cons,Bool.and_eq_true] using h
    exact ih both.2

theorem every_branch_possible (k : Nat) (b : Bool) : SignProfile.present (delayed k) b := by
  let x : Fin 4 → Bool := fun i => if i.val=0 then b else decide (i.val=2)
  refine ⟨x,by simp [x],?_⟩
  induction k with
  | zero => rfl
  | succ k ih => change (true && passes (delayed k) x) = true; exact ih

private theorem first_failed (k : Nat) (ms : List (Literal 4)) :
    (traced (delayed k) (⟨1,true⟩::ms)).1 = false := by
  rw [traced_spec]
  cases e : search (delayed k) (⟨1,true⟩::ms) with
  | false => rfl
  | true =>
    obtain ⟨x,hp,hm⟩ := (search_correct _ _).mp e
    have atOne := hm ⟨1,true⟩ (by simp)
    simp [forces_low k x hp] at atOne

private theorem both_visited {α} (f : α → Bool × Nat) (a b : α) (h : (f a).1=false) :
    (firstSuccess f [a,b]).2 = (f a).2 + (f b).2 := by
  cases e : (f b).1 <;> simp [firstSuccess,h,e]

private theorem first_charged {α} (f : α → Bool × Nat) (a : α) (ls : List α) :
    (f a).2 ≤ (firstSuccess f (a::ls)).2 := by
  cases h : (f a).1 <;> simp [firstSuccess,h]

theorem delayed_checks (k : Nat) (ms : List (Literal 4)) :
    2^k ≤ (traced (delayed k) ms).2 := by
  induction k generalizing ms with
  | zero =>
    change 1 ≤ (firstSuccess _ [_,_]).2
    refine Nat.le_trans ?_ (first_charged _ _ _)
    change 1 ≤ (firstSuccess _ [_,_]).2
    exact first_charged (fun l : Literal 4 => traced [] (l :: ⟨1,false⟩ :: ms)) ⟨1,false⟩ [⟨3,false⟩]
  | succ k ih =>
    change 2^(k+1) ≤ (firstSuccess (fun l => traced (delayed k) (l::ms)) [_,_]).2
    rw [both_visited (fun l : Literal 4 => traced (delayed k) (l::ms))
      ⟨1,true⟩ ⟨2,true⟩ (first_failed k ms),pow_succ,Nat.mul_two]
    exact Nat.add_le_add (ih _) (ih _)

private theorem cell_one (k : Nat) : SignProfile.profile (delayed (k+1)) 1 =
    ⟨true,true,false,false⟩ := by
  induction k with
  | zero => decide
  | succ k ih =>
    change SignProfile.join (SignProfile.flags choiceClause (SignProfile.singleton choiceClause) 1)
      (SignProfile.profile (delayed (k+1)) 1) = _
    rw [ih]
    decide

theorem delayed_inconclusive (k : Nat) (b : Bool) :
    ¬SignProfile.covered (delayed (k+1)) ∧
      passes (delayed (k+1)) (SignProfile.value (delayed (k+1)) b) = false := by
  constructor
  · intro cls
    have h := cls (1 : Fin 4) (by decide)
    change SignProfile.allowed (SignProfile.profile (delayed (k+1)) 1) = true at h
    rw [cell_one] at h
    contradiction
  · cases h : passes (delayed (k+1)) (SignProfile.value (delayed (k+1)) b) with
    | false => rfl
    | true =>
      have fail := forces_low (k+1) _ h
      change SignProfile.pick (SignProfile.profile (delayed (k+1)) 1) = false at fail
      rw [cell_one] at fail
      contradiction

theorem delayed_letters (k : Nat) : (original (delayed k)).length = 6*k+14 := by
  induction k with
  | zero => decide
  | succ k ih =>
    change (spellClause choiceClause ++ original (delayed k)).length = _
    rw [List.length_append,ih]
    have first : (spellClause choiceClause).length = 6 := by decide
    omega

end Codex.LiteralSearchCost
