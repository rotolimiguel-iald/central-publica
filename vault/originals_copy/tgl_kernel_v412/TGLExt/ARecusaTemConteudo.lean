import TGLExt.ClausulaNoSeparador

/-! A failed challenge may return one actual clause. Its literal names and
polarities specify exactly which other replies are invalidated as well. -/
set_option autoImplicit false
namespace Codex.FailedChallenge
open TGLExt.TraducaoTuring IALD.LeitorDaFormula Codex.BranchPresence
variable {n : Nat}

def inverted (c : Clausula n) : List (Literal n) :=
  c.map (fun l => ⟨l.var,!l.pos⟩)

theorem rejects_exactly (c : Clausula n) (x : Fin n → Bool) :
    satisfeita c x = false ↔ Agrees x (inverted c) := by
  induction c with
  | nil => simp [satisfeita,Agrees,inverted]
  | cons l c ih =>
    change (l.vale x || satisfeita c x) = false ↔ _
    rw [Bool.or_eq_false_iff,ih]
    have rel : l.vale x = false ↔ x l.var = !l.pos := by
      unfold Literal.vale
      cases x l.var <;> cases l.pos <;> decide
    rw [rel]
    simp [inverted,Agrees]

/-- Any witness with the same values on the clause names shares the refutation. -/
theorem reuses_clause (c : Clausula n) (x y : Fin n → Bool)
    (failed : satisfeita c x = false) (same : ∀ l ∈ c, x l.var = y l.var) :
    satisfeita c y = false := by
  apply (rejects_exactly _ _).mpr
  intro l mem
  obtain ⟨k,hk,rfl⟩ := List.mem_map.mp mem
  have hx := (rejects_exactly _ _).mp failed ⟨k.var,!k.pos⟩ (List.mem_map.mpr ⟨k,hk,rfl⟩)
  exact (same k hk).symm.trans hx

def positiveUnit (w : Nat) : Clausula (w+1) := [⟨0,true⟩]

private theorem unit_refuses (w : Nat) (x : Fin (w+1) → Bool) :
    satisfeita (positiveUnit w) x = false ↔ x 0 = false := by
  simp [positiveUnit,satisfeita,Literal.vale]

/-- The free coordinates parametrize ALL rejected complete words exactly once. -/
def refusedWords (w : Nat) :
    (Fin w → Bool) ≃ { x : Fin (w+1) → Bool // satisfeita (positiveUnit w) x = false } where
  toFun tail := ⟨Fin.cases false tail,(unit_refuses w _).mpr rfl⟩
  invFun x j := x.val j.succ
  left_inv tail := by funext j; simp
  right_inv x := by
    apply Subtype.ext
    funext i
    refine Fin.cases ?_ (fun j => ?_) i
    · exact ((unit_refuses w _).mp x.property).symm
    · rfl

theorem rejected_count (w : Nat) :
    Fintype.card { x : Fin (w+1) → Bool // satisfeita (positiveUnit w) x = false } = 2^w := by
  simpa [Fintype.card_fun] using (Fintype.card_congr (refusedWords w)).symm

end Codex.FailedChallenge
