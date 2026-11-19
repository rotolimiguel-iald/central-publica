import TGLExt.ConsultaPonderada
import TGLExt.TransicaoDaFronteira

set_option autoImplicit false

namespace Codex.PersistentQueries

open TGLExt.TraducaoTuring TGLExt.OResumoEPsiBit
open Codex.FrontierUpdate Codex.FrontierProjection
open Codex.LabeledQueries Codex.WeightedQueries

variable {n : ℕ}

/-- Prefixo lido, com a cláusula mais recente na cabeça. -/
def state (φ : CNF n) (j : ℕ) : CNF n := (φ.take j).reverse

def push (s : CNF n) (c : Clausula n) : CNF n := c :: s

theorem state_start (φ : CNF n) : state φ 0 = [] := by simp [state]

theorem state_step (φ : CNF n) (j : ℕ) (hj : j < φ.length) :
    state φ (j + 1) = push (state φ j) (φ.get ⟨j, hj⟩) := by
  exact (congrArg List.reverse (take_succ_eq φ hj)).trans List.reverse_append

private theorem weight_reverse (p : CNF n) (t : ℝ) (x : Assignment n) :
    pesoDas p.reverse t x = pesoDas p t x := by
  unfold pesoDas
  rw [List.map_reverse, List.prod_reverse]

theorem query_reverse (t : ℝ) (p : CNF n) (M : Mask n) :
    readReal t p.reverse M = readReal t p M := by
  classical
  simp only [readReal_correct, maskedWeight, weight_reverse]

/-- Uma função de consulta. O seu argumento escolhe as coordenadas na interface. -/
noncomputable def view (t : ℝ) (s : CNF n) (G : Finset (Fin n)) (v : Cells G) : ℝ :=
  readReal t s (pin G (extendCell G v))

theorem cell_exact (φ : CNF n) (t : ℝ) (j : ℕ) (u : Assignment n) :
    readReal t (state φ j) (pin (fronteira φ j) u) = resumo φ t j u := by
  unfold state
  rw [query_reverse]
  exact reads_frontier_cell φ t j u

theorem view_eq_table (φ : CNF n) (t : ℝ) (j : ℕ) :
    view t (state φ j) (fronteira φ j) = table φ t j := by
  funext v
  exact cell_exact φ t j (extendCell _ v)

/-- As duas consultas referem-se à mesma lista antiga; só a máscara da segunda muda. -/
noncomputable def nextView (t : ℝ) (s : CNF n) (c : Clausula n) (G : Finset (Fin n))
    (v : Cells G) : ℝ :=
  let M := pin G (extendCell G v)
  readReal t s M + (Real.exp (-t) - 1) * readReal t s (miss M c)

theorem two_queries_are_push (t : ℝ) (s : CNF n) (c : Clausula n) (G : Finset (Fin n)) :
    nextView t s c G = view t (push s c) G := rfl

/-- Para cada corte legal, consultar o novo estado e avançar a tabela dão a mesma
função em todas as células da nova interface. -/
theorem transition_by_query (φ : CNF n) (t : ℝ) (j : ℕ) (hj : j < φ.length) :
    nextView t (state φ j) (φ.get ⟨j,hj⟩) (fronteira φ (j+1)) =
      advanceTable (fronteira φ j) (fronteira φ (j+1)) (φ.get ⟨j,hj⟩) t
        (view t (state φ j) (fronteira φ j)) := by
  rw [two_queries_are_push, ← state_step φ j hj, view_eq_table, view_eq_table]
  exact transition φ t j hj

end Codex.PersistentQueries
