import TGLExt.ConsultasRotuladas

set_option autoImplicit false

namespace Codex.QueryWidth

open TGLExt.TraducaoTuring
open Codex.LabeledQueries

variable {n : ℕ}

def unit (i : Fin n) : Clausula n := [⟨i,true⟩]

/-- An actual path of the two subqueries in run. A true choice takes the clause-miss branch. -/
def follow (M : Mask n) (choices : Fin n → Bool) : List (Fin n) → Mask n
  | [] => M
  | i :: tail =>
    follow (if choices i then miss M (unit i) else M) choices tail

theorem allow_true_after_miss (M : Mask n) (i k : Fin n) :
    allowed (miss M (unit i)) k true = (allowed M k true && !decide (k=i)) := by
  change allowed (ban M ⟨i,true⟩) k true = _
  simp [allowed_ban]

theorem label_on_path (M : Mask n) (choices : Fin n → Bool) (is : List (Fin n)) (k : Fin n) :
    allowed (follow M choices is) k true = true ↔
      allowed M k true = true ∧ (k ∈ is → choices k = false) := by
  induction is generalizing M with
  | nil => simp [follow]
  | cons i is ih =>
    simp only [follow, ih, List.mem_cons]
    by_cases he : k = i
    · subst i
      cases choices k <;> simp [allow_true_after_miss]
    · cases choices i <;> simp [he,allow_true_after_miss]

def finalMask (choices : Fin n → Bool) : Mask n := follow free choices (List.finRange n)

/-- Trace of terminal queries of run, used only for the complexity proof. -/
def terminalMasks : CNF n → Mask n → List (Mask n)
  | [], M => [M]
  | c :: p, M => terminalMasks p M ++ terminalMasks p (miss M c)

theorem follow_is_terminal (M : Mask n) (choices : Fin n → Bool) (is : List (Fin n)) :
    follow M choices is ∈ terminalMasks (is.map unit) M := by
  induction is generalizing M with
  | nil => simp [follow, terminalMasks]
  | cons i is ih =>
    simp only [follow, List.map_cons, terminalMasks, List.mem_append]
    cases h : choices i
    · exact Or.inl (ih M)
    · exact Or.inr (ih (miss M (unit i)))

theorem retained_choice (choices : Fin n → Bool) (k : Fin n) :
    allowed (finalMask choices) k true = true ↔ choices k = false := by
  unfold finalMask
  rw [label_on_path]
  have all : allowed (free : Mask n) k true = true := rfl
  simp [all]

theorem finalMask_injective (n : ℕ) : Function.Injective (@finalMask n) := by
  intro a b hab
  funext k
  have h : (a k = false ↔ b k = false) := by
    rw [← retained_choice a k, ← retained_choice b k, hab]
  cases ha : a k <;> cases hb : b k <;> simp_all

/-- Each sequence of choices is an actual branch of run on the list of all distinct positive
unit clauses, even if every pair of identical terminal queries is merged. -/
theorem distinct_terminal_masks (n : ℕ) :
    Fintype.card (Set.range (@finalMask n)) = 2^n := by
  classical
  rw [Fintype.card_congr (Equiv.ofInjective _ (finalMask_injective n)).symm]
  simp

end Codex.QueryWidth
