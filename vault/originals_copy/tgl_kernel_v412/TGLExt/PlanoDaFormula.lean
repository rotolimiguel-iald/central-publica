import TGLExt.LeitorGlobal

/-! Construct a sufficient plan from the flat clauses themselves. A variable
selected by several clauses receives a single shared decision in the plan. -/
set_option autoImplicit false
namespace Codex.FormulaPlan
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula
open Codex.HornResidual Codex.CrossSelectors Codex.SharedBranch Codex.SharedReader
variable {n : Nat}

def pivots (p : CNF n) : List (Fin n) :=
  (p.flatMap (fun c => (names c true).tail)).dedup

def remaining (is : List (Fin n)) (c : Clausula n) : List (Fin n) :=
  names (c.filter (fun l => decide (l.var ∉ is))) true

theorem remaining_restrict (i : Fin n) (is : List (Fin n)) (c : Clausula n) :
    remaining is (c.filter (fun l => l.var != i)) = remaining (i::is) c := by
  unfold remaining
  rw [List.filter_filter]
  congr 2
  funext l
  by_cases h : l.var = i <;> simp [h]

theorem covered_ready (is : List (Fin n)) (p : CNF n)
    (hc : ∀ c ∈ p, (remaining is c).length ≤ 1) : ready is p := by
  induction is generalizing p with
  | nil =>
    apply (parse_iff p).2
    simpa [remaining] using hc
  | cons i is ih =>
    have branch (b : Bool) : ready is (restrictVar i b p) := by
      apply ih
      intro r hr
      obtain ⟨c,hc',e⟩ := List.mem_filterMap.mp hr
      unfold restrictClause at e
      split at e
      · simp at e
      · obtain rfl := Option.some.inj e
        rw [remaining_restrict]
        exact hc c hc'
    exact ⟨branch false,branch true⟩

private theorem remaining_names (is : List (Fin n)) (c : Clausula n) :
    remaining is c = (names c true).filter (fun i => decide (i ∉ is)) := by
  induction c with
  | nil => rfl
  | cons l c ih =>
    cases h : l.pos <;> by_cases h' : l.var ∈ is <;>
      simp [remaining,names,h,h'] at ih ⊢ <;> exact ih

theorem pivots_cover (p : CNF n) (c : Clausula n) (hc : c ∈ p) :
    (remaining (pivots p) c).length ≤ 1 := by
  rw [remaining_names]
  have picked : ∀ i ∈ (names c true).tail, i ∈ pivots p := by
    intro i hi
    exact List.mem_dedup.mpr (List.mem_flatMap.mpr ⟨c,hc,hi⟩)
  cases h : names c true with
  | nil => simp
  | cons j js =>
    have zero : js.filter (fun i => decide (i ∉ pivots p)) = [] := by
      apply List.filter_eq_nil_iff.mpr
      intro i hi
      have hm := picked i (by simpa [h] using hi)
      simp [hm]
    rw [List.filter_cons]
    split <;> rw [zero] <;> simp

theorem decided_from_formula (p : CNF n) :
    readPlan (pivots p) p = some (palavraDaFormula p) :=
  (reader_spec _ _).1 (covered_ready _ _ (pivots_cover p))

theorem no_duplicate_pivots (p : CNF n) : (pivots p).Nodup := List.nodup_dedup _

theorem horn_moves_from_formula (p : CNF n) :
    ∃ m ≤ 2^(pivots p).length * (2*Codex.PolinomioPorEscolha.budget
      (Codex.PolinomioPorEscolha.original p).length),
      Trace (pivots p) p (palavraDaFormula p) m :=
  cost_on_horn_tapes _ _ _ (Nat.le_refl _) (covered_ready _ _ (pivots_cover p))

end Codex.FormulaPlan
