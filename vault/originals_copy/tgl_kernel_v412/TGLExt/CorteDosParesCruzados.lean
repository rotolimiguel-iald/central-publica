import TGLExt.CorteDosPares

set_option autoImplicit false

namespace Codex.CrossedPairCut

open TGLExt.TraducaoTuring IALD.CorrelacoesDistintas IALD.LeitorDaFormula
open Codex.PairCut

/-- O primeiro par transmite o controle; cada outro par pode inverter o seu bit. -/
def transform {n : ℕ} (u : Bits (n+1)) : Bits (n+1) :=
  Fin.cases (u 0) (fun i => Bool.xor (u 0) (u i.succ))

theorem transform_twice {n : ℕ} (u : Bits (n+1)) : transform (transform u) = u := by
  funext i
  refine Fin.cases ?_ (fun j => ?_) i
  · rfl
  · change Bool.xor (u 0) (Bool.xor (u 0) (u j.succ)) = u j.succ
    cases u 0 <;> cases u j.succ <;> rfl

/-- Se os dois bits esquerdos são s e d, o bit direito correspondente deve ser s xor d. -/
def gate {n : ℕ} (i : Fin n) (s d : Bool) : Clausula ((n+1)+(n+1)) :=
  [⟨(0 : Fin (n+1)).castAdd (n+1), !s⟩, ⟨i.succ.castAdd (n+1), !d⟩,
   ⟨Fin.natAdd (n+1) i.succ, Bool.xor s d⟩]

def quartet {n : ℕ} (i : Fin n) : CNF ((n+1)+(n+1)) :=
  [gate i false false, gate i false true, gate i true false, gate i true true]

def crossedFormula (n : ℕ) : CNF ((n+1)+(n+1)) :=
  [implication (0 : Fin (n+1)) true, implication 0 false] ++ (List.finRange n).flatMap quartet

theorem clause_count (n : ℕ) : (crossedFormula n).length = 2 + 4*n := by
  have h (is : List (Fin n)) : (is.flatMap quartet).length = 4 * is.length := by
    induction is with
    | nil => rfl
    | cons i is ih =>
      rw [List.flatMap_cons, List.length_append, ih, List.length_cons]
      change 4 + 4 * is.length = 4 * (is.length + 1)
      omega
  simp [crossedFormula, h]
  omega

theorem quartet_spec {n : ℕ} (i : Fin n) (u v : Bits (n+1)) :
    passes (quartet i) (Fin.append u v) = true ↔ v i.succ = Bool.xor (u 0) (u i.succ) := by
  simp only [passes, quartet, gate, List.all_cons, List.all_nil,
    satisfeita, List.any_cons, List.any_nil, Literal.vale, Fin.append_left, Fin.append_right]
  cases u 0 <;> cases u i.succ <;> cases v i.succ <;> decide

private theorem flat_spec {n : ℕ} {A : Type*} (is : List A) (f : A → CNF n) (x : Bits n) :
    passes (is.flatMap f) x = true ↔ ∀ i ∈ is, passes (f i) x = true := by
  simp only [passes, List.all_eq_true, List.mem_flatMap]
  constructor
  · intro h i hi c hc
    exact h c ⟨i, hi, hc⟩
  · rintro h c ⟨i, hi, hc⟩
    exact h i hi c hc

theorem crossed_spec {n : ℕ} (u v : Bits (n+1)) :
    passes (crossedFormula n) (Fin.append u v) = true ↔ v = transform u := by
  have split (p q : CNF ((n+1)+(n+1))) : passes (p ++ q) (Fin.append u v) = true ↔
      passes p (Fin.append u v) = true ∧ passes q (Fin.append u v) = true := by
    simp [passes]
  have anchor : passes [implication (0 : Fin (n+1)) true, implication 0 false] (Fin.append u v) = true ↔
      u 0 = v 0 := by
    simpa [passes] using pair_spec u v 0
  rw [crossedFormula, split, anchor, flat_spec]
  simp only [List.mem_finRange, true_implies, quartet_spec]
  constructor
  · rintro ⟨h0, hd⟩
    funext i
    exact Fin.cases (motive := fun j => v j = transform u j) h0.symm hd i
  · rintro rfl
    exact ⟨rfl, fun _ => rfl⟩

theorem crossed_cover_bound {n : ℕ} {K : Type*} [Fintype K]
    (left right : K → Bits (n+1) → Prop)
    (h : ∀ u v, passes (crossedFormula n) (Fin.append u v) = true ↔
      ∃ k, left k u ∧ right k v) : 2^(n+1) ≤ Fintype.card K := by
  apply rectangle_bound (left := left) (right := fun k v => right k (transform v))
  intro u v
  rw [equalCNF_spec, ← h, crossed_spec]
  constructor
  · rintro rfl; rfl
  · intro he
    simpa only [transform_twice] using congrArg transform he.symm

/-- A permutação das colunas converte a matriz da CNF cruzada na identidade. -/
theorem crossed_signed_bound {n : ℕ} {K : Type*} [Fintype K]
    (left right : K → Bits (n+1) → ℝ)
    (h : ∀ u v, (∑ k, left k u * right k v) =
      if passes (crossedFormula n) (Fin.append u v) then (1 : ℝ) else 0) :
    2^(n+1) ≤ Fintype.card K := by
  apply signed_product_bound left (fun k v => right k (transform v))
  intro u v
  rw [h, truthMatrix]
  have hi : Function.Injective (transform (n := n)) := Function.LeftInverse.injective transform_twice
  simp only [crossed_spec, equalCNF_spec, hi.eq_iff, (eq_comm : v = u ↔ u = v)]

end Codex.CrossedPairCut
