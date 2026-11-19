import TGLExt.PsiBitNaFronteira

/-! A second general route: keep one shared selector in the syntax. Join size is
additive, and reading is faithful on each branch. Projection still quantifies a bit. -/
namespace IALD.SeletorCompartilhado

open TGLExt.TraducaoTuring IALD.LeitorDaFormula IALD.PsiBitNaFronteira

def guardClause {n} (disable : Bool) (c : Clausula n) : Clausula (n+1) :=
  ⟨0,disable⟩ :: c.map (fun l => ⟨l.var.succ,l.pos⟩)

def join {n} (left right : CNF n) : CNF (n+1) :=
  left.map (guardClause true) ++ right.map (guardClause false)

theorem clause_read {n} (off b : Bool) (c : Clausula n) (z : Fin n → Bool) :
    satisfeita (guardClause off c) (Fin.cases b z) = ((b == off) || satisfeita c z) := by
  simp [guardClause,satisfeita,Literal.vale,List.any_map,Function.comp_def]

theorem branch_read {n} (left right : CNF n) (b : Bool) (z : Fin n → Bool) :
    passes (join left right) (Fin.cases b z) = (if b then passes right z else passes left z) := by
  cases b <;> simp [passes,join,List.all_map,Function.comp_def,clause_read]

theorem single_letter {n} (a b : CNF n) (z : Fin n → Bool) :
    encode (passes (join a b) (Fin.cases false z)) (passes (join a b) (Fin.cases true z)) =
      encode (passes a z) (passes b z) := by simp [branch_read]

theorem projection_exact {n} (a b : CNF n) (z : Fin n → Bool) :
    (∃ s : Bool, passes (join a b) (Fin.cases s z) = true) ↔
    accepts (encode (passes a z) (passes b z)) = true := by
  simp only [accepts_encode,Bool.or_eq_true,branch_read]
  constructor
  · rintro ⟨s,h⟩
    cases s
    · exact Or.inl h
    · exact Or.inr h
  · rintro (h | h)
    · exact ⟨false,h⟩
    · exact ⟨true,h⟩

def literals {n} (f : CNF n) := (f.map List.length).sum

private theorem guarded_size {n} (f : CNF n) (b : Bool) :
    literals (f.map (guardClause b)) = literals f + f.length := by
  induction f with
  | nil => rfl
  | cons c f ih =>
    change (guardClause b c).length + literals (f.map (guardClause b)) = c.length + literals f + (f.length+1)
    rw [ih]
    simp only [guardClause,List.length_cons,List.length_map]
    omega

theorem additive_size {n} (a b : CNF n) :
    (join a b).length = a.length + b.length ∧
    literals (join a b) = literals a + literals b + a.length + b.length := by
  constructor
  · simp [join]
  · have h (x y : CNF (n+1)) : literals (x ++ y) = literals x + literals y := by simp [literals]
    rw [join,h,guarded_size,guarded_size]
    omega

/-- If the pair came from splitting an input, the guarded join realizes the
original relation, including the bit split off, for the same common z. -/
theorem reconstruct_relation {n} (f : CNF (n+1)) (b : Bool) (z : Fin n → Bool) :
    passes (join (summarize f).1 (summarize f).2) (Fin.cases b z) =
      passes f (Fin.cases b z) := by
  rw [branch_read]
  cases b
  · exact summarize_spec false f z
  · exact summarize_spec true f z

/-- The same successful choice of selector need not work for every outside assignment. -/
theorem shared_choice_can_depend_on_context :
    let a : CNF 1 := [[⟨0,true⟩]]
    let b : CNF 1 := [[⟨0,false⟩]]
    (∀ z, ∃ s, passes (join a b) (Fin.cases s z) = true) ∧
      ¬ ∃ s, ∀ z, passes (join a b) (Fin.cases s z) = true := by decide

end IALD.SeletorCompartilhado
