import TGLExt.Reagrupar
import TGLExt.DivisaoUniforme

set_option autoImplicit false

namespace Codex.FrontierUpdate

open TGLExt TGLExt.TraducaoTuring TGLExt.OResumoEPsiBit Codex.FrontierProjection

variable {n : ℕ}

private theorem fiber_mass (S : Finset (Fin n)) (u : Assignment n) (W : Assignment n → ℝ) :
    fiber S u W = Codex.Fresh.mass S u W := by
  classical
  unfold fiber Codex.Fresh.mass
  apply Finset.sum_congr _ fun _ _ => rfl
  ext; simp [Codex.Fresh.agree]

/-- A labeled table with one argument per actual frontier variable. -/
noncomputable def table (φ : CNF n) (t : ℝ) (j : ℕ) (v : Cells (fronteira φ j)) : ℝ :=
  resumo φ t j (extendCell _ v)

theorem table_read (φ : CNF n) (t : ℝ) (j : ℕ) (u : Assignment n) :
    table φ t j (readAt _ u) = resumo φ t j u := by
  apply o_resumo_so_ve_a_fronteira
  intro i hi
  exact restrict_extend _ (readAt _ u) ⟨i,hi⟩

/-- Numerator of one transition. Only labels on F ∪ vars(C) are summed.
The formula prefix is not an argument. G is the new interface and u selects its cell. -/
noncomputable def numerator (F G : Finset (Fin n)) (C : Clausula n) (t : ℝ)
    (old : Cells F → ℝ) (u : Assignment n) : ℝ := by
  classical
  let D := F ∪ varsClausula C
  exact ∑ z ∈ Finset.univ.filter (fun z : Cells D => readAt G (extendCell D z) = readAt G u),
    old (readAt F (extendCell D z)) * fator C t (extendCell D z)

/-- Fresh bits share the old unnormalized mass equally, including bits retiring immediately. -/
theorem transition_scaled (φ : CNF n) (t : ℝ) (j : ℕ) (hj : j < φ.length) (u : Assignment n) :
    let C := φ.get ⟨j,hj⟩
    let F := fronteira φ j
    let G := fronteira φ (j+1)
    (2 : ℝ) ^ ((F ∪ varsClausula C) \ F).card * resumo φ t (j+1) u =
      numerator F G C t (table φ t j) u := by
  classical
  let C := φ.get ⟨j,hj⟩
  let F := fronteira φ j
  let G := fronteira φ (j+1)
  let D := F ∪ varsClausula C
  let W := pesoDas (φ.take j) t
  change (2 : ℝ) ^ (D \ F).card * resumo φ t (j+1) u = _
  obtain ⟨hGD, hFresh⟩ := cut_support φ j hj
  have hW (x y : Assignment n) (h : ∀ i, i ∉ D \ F → x i = y i) : W x = W y :=
    peso_so_ve_as_variaveis_lidas _ _ (fun i hi => h i (hFresh i hi))
  have hf (x y : Assignment n) (h : ∀ i ∈ D, x i = y i) : fator C t x = fator C t y := by
    unfold fator
    rw [satisfeita_so_ve_as_suas_variaveis C (fun i hi => h i (Finset.mem_union_right _ hi))]
  have hnew : resumo φ t (j+1) u = fiber G u (fun x => W x * fator C t x) := by
    rw [← fiber_resumo]
    exact congrArg (fiber G u) (funext (peso_succ φ t hj))
  rw [hnew, regroup D G hGD u W (fator C t) hf, Finset.mul_sum]
  unfold numerator
  refine Finset.sum_congr rfl fun z _ => ?_
  rw [← mul_assoc]
  congr 1
  rw [fiber_mass, Codex.Fresh.split_mass F D Finset.subset_union_left _ W hW,
    ← fiber_mass, table_read]
  exact fiber_resumo φ t j _

noncomputable def advanceTable (F G : Finset (Fin n)) (C : Clausula n) (t : ℝ)
    (old : Cells F → ℝ) (v : Cells G) : ℝ :=
  numerator F G C t old (extendCell G v) / (2 : ℝ) ^ ((F ∪ varsClausula C) \ F).card

/-- Equality of functions, for every clause at every legal cut of every finite CNF.
On the right the only prefix information is the old labeled table and old/new interface. -/
theorem transition (φ : CNF n) (t : ℝ) (j : ℕ) (hj : j < φ.length) :
    table φ t (j+1) = advanceTable (fronteira φ j) (fronteira φ (j+1))
      (φ.get ⟨j,hj⟩) t (table φ t j) := by
  funext v
  unfold table advanceTable
  apply (eq_div_iff (by positivity)).2
  rw [mul_comm]
  exact transition_scaled φ t j hj _

end Codex.FrontierUpdate
