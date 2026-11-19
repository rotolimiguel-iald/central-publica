import TGLExt.CorrelacoesDistintas
import Mathlib.LinearAlgebra.Matrix.Rank

set_option autoImplicit false

namespace Codex.PairCut

open IALD.CorrelacoesDistintas IALD.LeitorDaFormula

abbrev Bits (n : ℕ) := Fin n → Bool

/-- A relação é a avaliação da CNF plana de duas implicações por par cruzado.
Uma cobertura pode ter sobreposições e várias testemunhas para a mesma entrada. -/
def ExactCover {n : ℕ} {K : Type*} (left right : K → Bits n → Prop) : Prop :=
  ∀ u v, passes (equalCNF n) (Fin.append u v) = true ↔ ∃ k, left k u ∧ right k v

/-- Misturar a esquerda de uma diagonal com a direita da outra permanece no
retângulo. A CNF obriga, por isso, a igualdade das duas diagonais. -/
theorem unique_diagonal {n : ℕ} {K : Type*} {left right : K → Bits n → Prop}
    (h : ExactCover left right) {k : K} {u v : Bits n}
    (hu : left k u) (hv : right k v) : u = v :=
  (equalCNF_spec u v).mp ((h u v).mpr ⟨k, hu, hv⟩)

theorem rectangle_bound {n : ℕ} {K : Type*} [Fintype K]
    {left right : K → Bits n → Prop} (h : ExactCover left right) :
    2 ^ n ≤ Fintype.card K := by
  classical
  have covered (u : Bits n) : ∃ k, left k u ∧ right k u :=
    (h u u).mp ((equalCNF_spec u u).mpr rfl)
  choose witness hw using covered
  have injective : Function.Injective witness := by
    intro u v he
    apply unique_diagonal h (hw u).1
    rw [he]
    exact (hw v).2
  simpa [Bits] using Fintype.card_le_of_injective witness injective

/-- Número mínimo exato de retângulos aceitos para esse corte entre os blocos. -/
theorem exact_cover_iff (n r : ℕ) :
    (∃ left right : Fin r → Bits n → Prop, ExactCover left right) ↔ 2 ^ n ≤ r := by
  classical
  constructor
  · rintro ⟨left, right, h⟩
    simpa using rectangle_bound h
  · intro hr
    have hc : Fintype.card (Bits n) ≤ Fintype.card (Fin r) := by simpa [Bits] using hr
    obtain ⟨e⟩ := Function.Embedding.nonempty_of_card_le hc
    refine ⟨fun k u => e u = k, fun k v => e v = k, ?_⟩
    intro u v
    rw [equalCNF_spec]
    constructor
    · rintro rfl
      exact ⟨e u, rfl, rfl⟩
    · rintro ⟨k, hu, hv⟩
      exact e.injective (hu.trans hv.symm)

/-- Matriz real 0/1 da avaliação da CNF sob uma atribuição dos dois lados. -/
def truthMatrix (n : ℕ) : Matrix (Bits n) (Bits n) ℝ :=
  fun u v => if passes (equalCNF n) (Fin.append u v) then 1 else 0

theorem truthMatrix_eq_one (n : ℕ) : truthMatrix n = 1 := by
  ext u v
  simp only [truthMatrix, Matrix.one_apply, equalCNF_spec]

/-- Mesmo com cancelamento, uma soma exata de produtos reais separados pelos
mesmos blocos precisa de tantos termos quanto o posto da matriz identidade.
O alvo numérico aqui é a função verdade 0/1. -/
theorem signed_product_bound {n : ℕ} {K : Type*} [Fintype K]
    (left right : K → Bits n → ℝ)
    (h : ∀ u v, (∑ k, left k u * right k v) = truthMatrix n u v) :
    2 ^ n ≤ Fintype.card K := by
  classical
  let A : Matrix (Bits n) K ℝ := fun u k => left k u
  let B : Matrix K (Bits n) ℝ := fun k v => right k v
  have hab : A * B = truthMatrix n := by
    ext u v
    exact h u v
  calc
    2 ^ n = (truthMatrix n).rank := by rw [truthMatrix_eq_one, Matrix.rank_one]; simp [Bits]
    _ = (A * B).rank := congrArg Matrix.rank hab.symm
    _ ≤ A.rank := Matrix.rank_mul_le_left A B
    _ ≤ Fintype.card K := Matrix.rank_le_card_width A

end Codex.PairCut
