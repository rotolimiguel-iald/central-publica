import TGLExt.ObrigacoesJaSatisfeitas
import TGLExt.CamadaAlcancada

/-! A union of signed conjunctions cannot compress the disjoint-pair
relation: every minimal model needs a different conjunction. The bound
is independent of how the conjunctions are selected or simplified. -/
set_option autoImplicit false
namespace Codex.CubeLimit
open TGLExt.TraducaoTuring IALD.LeitorDaFormula
open Codex.BranchCache Codex.ExplicitCache Codex.CoverCache Codex.PolinomioPorEscolha
variable {n k : Nat}

def meet (x y : Fin n → Bool) (j : Fin n) := x j && y j

theorem fits_meet (s : Key n) {x y : Fin n → Bool}
    (hx : fits s x) (hy : fits s y) : fits s (meet x y) := by
  intro a ha
  simp [meet,hx a ha,hy a ha]

theorem choice_passes (f : Fin k → Bool) : passes (pairs k true) (row f) = true := by
  apply (pair_condition _ _).mpr
  intro i
  cases h : f i <;> simp [row_value,h]

/-- The intersection of two minimal choices can satisfy the prefix only if
the two choices agree at every pair. -/
theorem meet_separates (f g : Fin k → Bool)
    (h : passes (pairs k true) (meet (row f) (row g)) = true) : f = g := by
  funext i
  have onPair := (pair_condition _ _).mp h i
  cases a : f i <;> cases b : g i <;> simp_all [meet,row_value]

/-- Every exact disjunction of cubes needs all 2^k different witnesses in
separate cubes. This also permits negative marks and overlapping cubes. -/
theorem any_exact_cube_layer (rows : Layer (2*k))
    (exactModels : ∀ x, models rows x ↔ passes (pairs k true) x = true) :
    2^k ≤ rows.card := by
  classical
  have chooseCube (f : Fin k → Bool) : ∃ s : ↥rows, fits s.val (row f) := by
    obtain ⟨s,hs,fit⟩ := (exactModels _).mpr (choice_passes f)
    exact ⟨⟨s,hs⟩,fit⟩
  choose cube contains using chooseCube
  have inj : Function.Injective cube := by
    intro f g same
    have fg : fits (cube f).val (row g) := same ▸ contains g
    exact meet_separates f g ((exactModels _).mp
      ⟨(cube f).val,(cube f).property,fits_meet _ (contains f) fg⟩)
  simpa using Fintype.card_le_of_injective cube inj

private theorem scan_initial (p : CNF n) (x : Fin n → Bool) :
    models (scan p (initial n)) x ↔ passes p x = true := by
  rw [scan_exact]
  simp [initial,models,fits]

theorem reached_after_skips (k : Nat) :
    2^k ≤ (scan (pairs k true) (initial (2*k))).card :=
  any_exact_cube_layer _ (scan_initial _)

private theorem charged_if_countermodel (rows : Layer n) (c : Clausula n)
    (x : Fin n → Bool) (already : models rows x) (violates : satisfeita c x = false) :
    covers rows c = false := by
  cases h : covers rows c with
  | false => rfl
  | true =>
    have stays : models (step rows c) x := by simpa [step,h] using already
    have ok := ((step_exact rows c x).mp stays).2
    simp [violates] at ok

theorem two_costs_append (p q : CNF n) (rows : Layer n) :
    extensions (p++q) rows = extensions p rows + extensions q (scan p rows) ∧
    membershipBudget (p++q) rows = membershipBudget p rows + membershipBudget q (scan p rows) := by
  induction p generalizing rows with
  | nil => simp [extensions,membershipBudget,scan]
  | cons c p ih =>
    obtain ⟨e,m⟩ := ih (step rows c)
    simp only [List.cons_append,extensions,membershipBudget,scan,e,m,Nat.add_assoc,and_self]

/-- On a real input whose physical classifiers both miss, the next negative
clause is not covered. Counting the actual extensions of the skipping cache
therefore still gives an exponential lower bound; checking costs are separate. -/
theorem dispatched_extensions (k : Nat) :
    Codex.ReuseDispatch.physical (original (Codex.ReachedLayer.gateInput k)) = (none,none) ∧
    2^(k+2) ≤ extensions (Codex.ReachedLayer.gateInput k) (initial _) := by
  refine ⟨(Codex.ReachedLayer.calls_shared_fallback k).1,?_⟩
  let p := pairs (k+2) true
  let rows := scan p (initial _)
  let c := Codex.ReachedLayer.probePair k false false
  let ones := fun _ : Fin (2*(k+2)) => true
  have saved : models rows ones := (scan_initial p ones).mpr ((pair_condition ones true).mpr
    (fun _ => Or.inl rfl))
  have skipOff : covers rows c = false := charged_if_countermodel _ _ ones saved (by rfl)
  have lo : 2^(k+2) ≤ rows.card := reached_after_skips _
  rw [Codex.ReachedLayer.gateInput,(two_costs_append _ _ _).1]
  change _ ≤ _ + ((if covers rows c then 0 else rows.card*c.length) + _)
  rw [skipOff]
  have two : c.length = 2 := rfl
  simp only [Bool.false_eq_true,if_false,two]
  omega

end Codex.CubeLimit
