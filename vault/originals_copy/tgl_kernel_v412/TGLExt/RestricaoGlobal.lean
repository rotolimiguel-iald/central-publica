import TGLExt.PolinomioPorEscolha

set_option autoImplicit false
namespace Codex.SharedBranch
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula Codex.PolinomioPorEscolha
open IALD.LeitorDaFormula (passes sat_iff)
variable {n : Nat}

/-- Assign a single label in all its occurrences. Surviving labels keep their addresses. -/
def restrictClause (i : Fin n) (b : Bool) (c : Clausula n) : Option (Clausula n) :=
  if c.any (fun l => l.var == i && l.pos == b) then none
  else some (c.filter (fun l => l.var != i))

def restrictVar (i : Fin n) (b : Bool) (p : CNF n) : CNF n :=
  p.filterMap (restrictClause i b)

def restrictMany (is : List (Fin n)) (x : Fin n → Bool) (p : CNF n) : CNF n :=
  is.foldl (fun q i => restrictVar i (x i) q) p

private theorem partition_read (i : Fin n) (b : Bool) (c : Clausula n) (x : Fin n → Bool) :
    satisfeita c (Function.update x i b) =
      (c.any (fun l => l.var == i && l.pos == b) ||
        satisfeita (c.filter (fun l => l.var != i)) x) := by
  induction c with
  | nil => rfl
  | cons l c ih =>
    change (l.vale (Function.update x i b) || satisfeita c (Function.update x i b)) = _
    rw [ih]
    by_cases h : l.var = i
    · have symmetry : (b == l.pos) = (l.pos == b) := by cases b <;> cases l.pos <;> rfl
      simp [h,Literal.vale,Bool.or_assoc,symmetry]
    · have no : (l.var == i) = false := beq_eq_false_iff_ne.mpr h
      simp [h,no,Literal.vale,satisfeita,Bool.or_left_comm]

theorem clause_read (i : Fin n) (b : Bool) (c : Clausula n) (x : Fin n → Bool) :
    (restrictClause i b c).elim true (fun r => satisfeita r x) =
      satisfeita c (Function.update x i b) := by
  rw [partition_read]
  unfold restrictClause
  split <;> simp_all

theorem branch_read (i : Fin n) (b : Bool) (p : CNF n) (x : Fin n → Bool) :
    passes (restrictVar i b p) x = passes p (Function.update x i b) := by
  induction p with
  | nil => rfl
  | cons c p ih =>
    have hc := clause_read i b c x
    cases h : restrictClause i b c with
    | none =>
      simp [h] at hc
      simp only [restrictVar,List.filterMap_cons,h] at ih ⊢
      change _ = (satisfeita c (Function.update x i b) && _)
      rw [hc,Bool.true_and]
      exact ih
    | some r =>
      simp [h] at hc
      simpa [restrictVar,List.filterMap_cons,h,passes,←hc] using congrArg (fun v => satisfeita r x && v) ih

theorem word_split (i : Fin n) (p : CNF n) :
    palavraDaFormula p =
    (palavraDaFormula (restrictVar i false p) || palavraDaFormula (restrictVar i true p)) := by
  apply Bool.eq_iff_iff.mpr
  simp only [Bool.or_eq_true,a_palavra_e_o_sat,sat_iff]
  constructor
  · rintro ⟨x,hx⟩
    have self : Function.update x i (x i) = x := by
      funext j
      by_cases h : j = i <;> simp [h]
    have yes : passes (restrictVar i (x i) p) x = true := by rw [branch_read,self,hx]
    cases h : x i
    · exact Or.inl ⟨x,h ▸ yes⟩
    · exact Or.inr ⟨x,h ▸ yes⟩
  · rintro (⟨x,h⟩|⟨x,h⟩)
    · exact ⟨_,(branch_read i false p x).symm.trans h⟩
    · exact ⟨_,(branch_read i true p x).symm.trans h⟩

private theorem filter_cost (i : Fin n) (c : Clausula n) :
    ((c.filter (fun l => l.var != i)).flatMap spell).length ≤ (c.flatMap spell).length := by
  induction c with
  | nil => rfl
  | cons l c ih =>
    cases hl : (l.var != i) <;>
      simp only [List.filter_cons,hl,Bool.false_eq_true,if_false,if_true,List.flatMap_cons,
        List.length_append] <;> omega

theorem restrict_size (i : Fin n) (b : Bool) (p : CNF n) :
    (original (restrictVar i b p)).length ≤ (original p).length := by
  induction p with
  | nil => rfl
  | cons c p ih =>
    have hc := filter_cost i c
    change (original ((c :: p).filterMap (restrictClause i b))).length ≤
      (spellClause c ++ original p).length
    rw [List.filterMap_cons,List.length_append]
    cases e : restrictClause i b c with
    | none => exact Nat.le_trans ih (Nat.le_add_left _ _)
    | some r =>
      have hr : r = c.filter (fun l => l.var != i) := by
        unfold restrictClause at e
        split at e <;> simp_all
      subst r
      change (spellClause _ ++ original (restrictVar i b p)).length ≤ _
      rw [List.length_append]
      apply Nat.add_le_add _ ih
      simp only [spellClause,List.length_append]
      omega

end Codex.SharedBranch
