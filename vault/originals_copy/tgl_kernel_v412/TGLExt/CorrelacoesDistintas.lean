import TGLExt.LeitorDaFormula

namespace IALD.CorrelacoesDistintas

open TGLExt.TraducaoTuring IALD.LeitorDaFormula

/-- Each bit pair contributes one implication in each direction. -/
def implication {n : ℕ} (i : Fin n) (b : Bool) : Clausula (n+n) :=
  [⟨i.castAdd n, !b⟩, ⟨Fin.natAdd n i, b⟩]

def equalCNF (n : ℕ) : CNF (n+n) :=
  List.ofFn (fun i => implication i true) ++ List.ofFn (fun i => implication i false)

theorem syntax_size (n : ℕ) :
    (equalCNF n).length = 2*n ∧ ∀ c ∈ equalCNF n, c.length = 2 := by
  constructor
  · simp [equalCNF, two_mul]
  · intro c hc
    simp only [equalCNF, List.mem_append, List.mem_ofFn] at hc
    rcases hc with ⟨i,rfl⟩ | ⟨i,rfl⟩ <;> rfl

theorem pair_spec {n : ℕ} (u v : Fin n → Bool) (i : Fin n) :
    (satisfeita (implication i true) (Fin.append u v) = true ∧
    satisfeita (implication i false) (Fin.append u v) = true) ↔ u i = v i := by
  simp only [implication, satisfeita, List.any_cons, List.any_nil, Literal.vale,
    Fin.append_left, Fin.append_right]
  cases hu : u i <;> cases hv : v i <;> decide

theorem equalCNF_spec {n : ℕ} (u v : Fin n → Bool) :
    passes (equalCNF n) (Fin.append u v) = true ↔ u = v := by
  simp only [passes, equalCNF, List.all_eq_true, List.mem_append, List.mem_ofFn]
  constructor
  · intro h
    funext i
    apply (pair_spec u v i).1
    exact ⟨h _ (.inl ⟨i,rfl⟩), h _ (.inr ⟨i,rfl⟩)⟩
  · rintro rfl c (⟨i,rfl⟩ | ⟨i,rfl⟩)
    · exact ((pair_spec u u i).2 rfl).1
    · exact ((pair_spec u u i).2 rfl).2

/-- A residual is the function of the unassigned right half. -/
def residual {n : ℕ} (u : Fin n → Bool) (v : Fin n → Bool) : Bool :=
  passes (equalCNF n) (Fin.append u v)

theorem residual_injective (n : ℕ) :
    Function.Injective (residual (n := n)) := by
  intro u v he
  apply (equalCNF_spec u v).1
  have hh := congrFun he v
  exact hh.trans ((equalCNF_spec v v).2 rfl)

/-- Applies even if states are shared by every prefix with the same residual. -/
theorem fixed_order_width {n : ℕ} {S : Type*} [Fintype S]
    (afterLeft : (Fin n → Bool) → S) (finish : S → (Fin n → Bool) → Bool)
    (correct : ∀ u v, finish (afterLeft u) v = residual u v) :
    2 ^ n ≤ Fintype.card S := by
  have inj : Function.Injective afterLeft := by
    intro u v h
    apply residual_injective n
    funext z
    rw [← correct, ← correct, h]
  simpa using Fintype.card_le_of_injective afterLeft inj

/-- A left/right pair can instead be presented consecutively on a binary stream. -/
inductive State where
  | ready | expectFalse | expectTrue | dead
  deriving DecidableEq, Fintype

def tick : State → Bool → State
  | .ready, false => .expectFalse
  | .ready, true => .expectTrue
  | .expectFalse, false => .ready
  | .expectTrue, true => .ready
  | _, _ => .dead

def pairStream {n : ℕ} (u v : Fin n → Bool) (is : List (Fin n)) :=
  is.flatMap fun i => [u i, v i]

theorem pairStream_length {n : ℕ} (u v : Fin n → Bool) (is : List (Fin n)) :
    (pairStream u v is).length = 2 * is.length := by
  induction is with
  | nil => simp [pairStream]
  | cons i is ih =>
    change ([u i,v i] ++ pairStream u v is).length = 2 * (i :: is).length
    simp [ih, Nat.mul_add]

theorem interleaved_fold {n : ℕ} (u v : Fin n → Bool) (is : List (Fin n)) (ok : Bool) :
    (pairStream u v is).foldl tick (if ok then .ready else .dead) =
      if ok && is.all (fun i => u i == v i) then .ready else .dead := by
  induction is generalizing ok with
  | nil => simp [pairStream]
  | cons i is ih =>
    change (pairStream u v is).foldl tick (tick (tick (if ok then .ready else .dead) (u i)) (v i)) = _
    have hp := ih (ok && (u i == v i))
    cases ok <;> cases h₁ : u i <;> cases h₂ : v i <;> simpa [h₁, h₂, tick] using hp

theorem interleaved_reader {n : ℕ} (u v : Fin n → Bool) :
    ((pairStream u v (List.finRange n)).foldl tick .ready = .ready ↔
        passes (equalCNF n) (Fin.append u v) = true) ∧
    (pairStream u v (List.finRange n)).length = 2*n ∧ Fintype.card State = 4 := by
  refine ⟨?_, by simpa using pairStream_length u v (List.finRange n), by decide⟩
  rw [equalCNF_spec]
  have h := interleaved_fold u v (List.finRange n) true
  simp only [Bool.true_and, if_true] at h
  rw [h]
  by_cases e : u = v
  · subst v
    simp
  · have hn : (List.finRange n).all (fun i => u i == v i) = false := by
      by_contra! h
      apply e
      funext i
      have ht : (List.finRange n).all (fun j => u j == v j) = true := by
        cases hh : (List.finRange n).all (fun j => u j == v j) <;> simp_all
      have ha := List.all_eq_true.mp ht i (List.mem_finRange i)
      simpa using ha
    simp [hn,e]

end IALD.CorrelacoesDistintas
