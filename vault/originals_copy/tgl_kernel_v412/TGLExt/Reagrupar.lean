import TGLExt.ProjecaoDaFronteira

set_option autoImplicit false

namespace Codex.FrontierUpdate

open TGLExt TGLExt.TraducaoTuring TGLExt.OResumoEPsiBit Codex.FrontierProjection

variable {n : ℕ}
abbrev Assignment (n : ℕ) := Fin n → Bool
abbrev Cells {n : ℕ} (D : Finset (Fin n)) := ↥D → Bool

def readAt (D : Finset (Fin n)) (x : Assignment n) : Cells D := fun i => x i

noncomputable def fiber (D : Finset (Fin n)) (u : Assignment n) (w : Assignment n → ℝ) : ℝ := by
  classical
  exact ∑ x ∈ Finset.univ.filter (fun x => ∀ i ∈ D, x i = u i), w x

theorem fiber_resumo (φ : CNF n) (t : ℝ) (j : ℕ) (u : Assignment n) :
    fiber (fronteira φ j) u (pesoDas (φ.take j) t) = resumo φ t j u := by
  classical
  unfold fiber resumo
  apply Finset.sum_congr _ fun _ _ => rfl
  ext; simp

theorem read_extend (D : Finset (Fin n)) (v : Cells D) :
    readAt D (extendCell D v) = v :=
  funext (restrict_extend D v)

theorem readAt_eq_iff (D : Finset (Fin n)) (x y : Assignment n) :
    readAt D x = readAt D y ↔ ∀ i ∈ D, x i = y i := by
  constructor
  · intro h i hi
    exact congrFun h ⟨i, hi⟩
  · intro h
    exact funext fun i => h i i.property

/-- A weighted marginal after erasing labels outside G. All factors are constant on D-cells. -/
theorem regroup (D G : Finset (Fin n)) (hGD : G ⊆ D) (u : Assignment n)
    (w f : Assignment n → ℝ)
    (hf : ∀ x y, (∀ i ∈ D, x i = y i) → f x = f y) :
    fiber G u (fun x => w x * f x) =
      ∑ z ∈ Finset.univ.filter (fun z : Cells D => readAt G (extendCell D z) = readAt G u),
        fiber D (extendCell D z) w * f (extendCell D z) := by
  classical
  let S := Finset.univ.filter (fun x : Assignment n => ∀ i ∈ G, x i = u i)
  change (∑ x ∈ S, w x * f x) = _
  rw [← Finset.sum_fiberwise S (readAt D) (fun x => w x * f x), Finset.sum_filter]
  refine Finset.sum_congr rfl fun z _ => ?_
  by_cases hz : readAt G (extendCell D z) = readAt G u
  · rw [if_pos hz, fiber, Finset.sum_mul]
    have hm (x : Assignment n) : readAt D x = z ↔ ∀ i ∈ D, x i = extendCell D z i := by
      rw [← readAt_eq_iff, read_extend]
    apply Finset.sum_congr
    · ext x
      simp only [S, Finset.mem_filter, Finset.mem_univ, true_and]
      refine ⟨fun h => (hm x).1 h.2, fun h => ⟨?_, (hm x).2 h⟩⟩
      exact fun i hi => (h i (hGD hi)).trans ((readAt_eq_iff _ _ _).1 hz i hi)
    · intro x hx
      have hxz := (Finset.mem_filter.mp hx).2
      rw [hf x (extendCell D z) hxz]
  · rw [if_neg hz]
    apply Finset.sum_eq_zero
    intro x hx
    exfalso
    obtain ⟨hxS, hxD⟩ := Finset.mem_filter.mp hx
    have hxu := (Finset.mem_filter.mp hxS).2
    apply hz
    apply (readAt_eq_iff _ _ _).2
    intro i hi
    have hxi : x i = extendCell D z i := by
      apply (readAt_eq_iff D x (extendCell D z)).1 _ i (hGD hi)
      rw [read_extend, hxD]
    exact hxi.symm.trans (hxu i hi)

private theorem vars_append (p r : CNF n) :
    varsDas (p ++ r) = varsDas p ∪ varsDas r := by
  induction p with
  | nil => simp [varsDas]
  | cons c p ih =>
    change varsClausula c ∪ varsDas (p ++ r) = (varsClausula c ∪ varsDas p) ∪ varsDas r
    rw [ih, Finset.union_assoc]

def bag (φ : CNF n) (j : ℕ) (C : Clausula n) := fronteira φ j ∪ varsClausula C

/-- Every new frontier label comes either from the old frontier or the clause. The extra bag
labels do not occur in the prefix. These are consequences of the actual syntax of the formula. -/
theorem cut_support (φ : CNF n) (j : ℕ) (hj : j < φ.length) :
    let C := φ.get ⟨j,hj⟩
    let D := bag φ j C
    fronteira φ (j+1) ⊆ D ∧ ∀ i ∈ varsDas (φ.take j), i ∉ D \ fronteira φ j := by
  classical
  dsimp only
  let C := φ.get ⟨j,hj⟩
  have hdrop : φ.drop j = C :: φ.drop (j+1) := by
    exact List.drop_eq_getElem_cons hj
  have hv : varsDas (φ.drop j) = varsClausula C ∪ varsDas (φ.drop (j+1)) := by
    rw [hdrop]; rfl
  have hp : varsDas (φ.take (j+1)) = varsDas (φ.take j) ∪ varsClausula C := by
    rw [take_succ_eq φ hj, vars_append]
    simp [C, varsDas]
  constructor
  · intro i hi
    obtain ⟨ha,hb⟩ := Finset.mem_inter.mp hi
    rw [hp] at ha
    rcases Finset.mem_union.mp ha with hold | hc
    · apply Finset.mem_union_left
      exact Finset.mem_inter.mpr ⟨hold, hv ▸ Finset.mem_union_right _ hb⟩
    · exact Finset.mem_union_right _ hc
  · intro i hi hbad
    obtain ⟨hd,hn⟩ := Finset.mem_sdiff.mp hbad
    rcases Finset.mem_union.mp hd with h | h
    · exact hn h
    · exact hn (Finset.mem_inter.mpr ⟨hi, hv ▸ Finset.mem_union_left _ h⟩)

end Codex.FrontierUpdate
