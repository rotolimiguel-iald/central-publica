import TGLExt.OPsiBitDaFormula

set_option autoImplicit false

namespace Codex.FrontierProjection

open TGLExt TGLExt.TraducaoTuring TGLExt.OResumoEPsiBit

variable {n : ℕ}

def extendCell (F : Finset (Fin n)) (v : ↥F → Bool) : Fin n → Bool :=
  fun i => if hi : i ∈ F then v ⟨i, hi⟩ else false

theorem restrict_extend (F : Finset (Fin n)) (v : ↥F → Bool) (i : ↥F) :
    extendCell F v i = v i := by simp [extendCell, i.property]

/-- A cell in the summary of `OResumoEPsiBit` is exactly a fiber sum. -/
theorem cell_eq_fiber (φ : CNF n) (t : ℝ) (j : ℕ) (v : ↥(fronteira φ j) → Bool) :
    resumo φ t j (extendCell _ v) =
      ∑ x ∈ Finset.univ.filter (fun x => leituraDaFronteira φ j x = v),
        pesoDas (φ.take j) t x := by
  classical
  unfold resumo
  refine Finset.sum_congr ?_ fun _ _ => rfl
  ext x
  simp only [Finset.mem_filter, Finset.mem_univ, true_and]
  constructor
  · intro h
    funext i
    exact (h i i.property).trans (restrict_extend _ v i)
  · intro h i hi
    exact (congrFun h ⟨i, hi⟩).trans (restrict_extend _ v ⟨i, hi⟩).symm

/-- Read any real weight depending only on the labeled interface from the old table. -/
theorem weighted_projection (φ : CNF n) (t : ℝ) (j : ℕ)
    (g : (↥(fronteira φ j) → Bool) → ℝ) :
    (∑ x : Fin n → Bool, pesoDas (φ.take j) t x * g (leituraDaFronteira φ j x)) =
      ∑ v, resumo φ t j (extendCell _ v) * g v := by
  classical
  rw [← Finset.sum_fiberwise Finset.univ (leituraDaFronteira φ j)
    (fun x => pesoDas (φ.take j) t x * g (leituraDaFronteira φ j x))]
  refine Finset.sum_congr rfl fun v _ => ?_
  rw [cell_eq_fiber, Finset.sum_mul]
  exact Finset.sum_congr rfl fun x hx => by rw [(Finset.mem_filter.mp hx).2]

theorem total_projection (φ : CNF n) (t : ℝ) (j : ℕ) :
    particao (custoCNF (φ.take j)) t =
      ∑ v : ↥(fronteira φ j) → Bool, resumo φ t j (extendCell (fronteira φ j) v) := by
  rw [particao_e_a_soma_dos_pesos]
  simpa using weighted_projection φ t j (fun _ => 1)

/-- Total after one clause when its variables are all on the old frontier. -/
theorem append_supported_clause (φ : CNF n) (t : ℝ) (j : ℕ) (C : Clausula n)
    (h : varsClausula C ⊆ fronteira φ j) :
    particao (custoCNF (φ.take j ++ [C])) t =
      ∑ v : ↥(fronteira φ j) → Bool, resumo φ t j (extendCell (fronteira φ j) v) *
        fator C t (extendCell (fronteira φ j) v) := by
  classical
  rw [particao_e_a_soma_dos_pesos]
  calc
    _ = ∑ x : Fin n → Bool, pesoDas (φ.take j) t x *
          fator C t (extendCell _ (leituraDaFronteira φ j x)) := by
      refine Finset.sum_congr rfl fun x _ => ?_
      have hs : satisfeita C x = satisfeita C (extendCell _ (leituraDaFronteira φ j x)) :=
        satisfeita_so_ve_as_suas_variaveis C (fun i hi => by
          simp [extendCell, h hi, leituraDaFronteira])
      have hf : fator C t x = fator C t (extendCell _ (leituraDaFronteira φ j x)) := by
        unfold fator
        rw [hs]
      simpa only [pesoDas, List.map_append, List.prod_append, List.map_singleton,
        List.prod_singleton] using congrArg (fun z => pesoDas (φ.take j) t x * z) hf
    _ = _ := weighted_projection φ t j (fun v => fator C t (extendCell _ v))

end Codex.FrontierProjection
