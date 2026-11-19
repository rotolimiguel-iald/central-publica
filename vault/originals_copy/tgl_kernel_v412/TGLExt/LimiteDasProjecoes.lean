import TGLExt.LeitorGlobal

/-! Existential support can agree on *every proper set of labels*. A single
new unit clause can separate the profiles again. Each prefix below is one
explicit clause with one occurrence per label, with no table of assignments. -/
set_option autoImplicit false
namespace Codex.ProjectionLimit
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula Codex.SharedBranch
open IALD.LeitorDaFormula (passes sat_iff)
variable {n : Nat}

def signedCNF (s : Fin n → Bool) : CNF n :=
  [(List.finRange n).map (fun j => (⟨j,s j⟩ : Literal n))]

theorem signed_read (s x : Fin n → Bool) :
    passes (signedCNF s) x = true ↔ ∃ j, x j = s j := by
  simp [passes,signedCNF,satisfeita,List.any_map,List.any_eq_true,Literal.vale,
    Function.comp_def]

/-- A labeled possibility query. No claim of unit cost for computing it. -/
def support (p : CNF n) (S : Set (Fin n)) (u : Fin n → Bool) : Prop :=
  ∃ x, (∀ j ∈ S, x j = u j) ∧ passes p x = true

def Profile (n : Nat) := (S : Set (Fin n)) → (∃ j, j ∉ S) → (Fin n → Bool) → Prop

def profile (p : CNF n) : Profile n := fun S _ u => support p S u

theorem all_proper_supports (s : Fin n → Bool) (S : Set (Fin n))
    (omits : ∃ j, j ∉ S) (u : Fin n → Bool) : support (signedCNF s) S u := by
  obtain ⟨j,hj⟩ := omits
  refine ⟨Function.update u j (s j), ?_, (signed_read _ _).mpr ⟨j,by simp⟩⟩
  intro i hi
  have h : i ≠ j := fun e => hj (e ▸ hi)
  simp [h]

theorem profiles_agree (s t : Fin n → Bool) : profile (signedCNF s) = profile (signedCNF t) := by
  funext S h u
  exact propext ⟨fun _ => all_proper_supports t S h u, fun _ => all_proper_supports s S h u⟩

/-- Flipping this one literal changes which global assignment the clause forbids. -/
def signedAt (i : Fin n) (b : Bool) : Fin n → Bool := fun j => if j = i then b else true

def unitAt (i : Fin n) (b : Bool) : Clausula n := [⟨i,b⟩]

private theorem append_unit (p : CNF n) (x : Fin n → Bool) (j : Fin n) (b : Bool) :
    passes (p ++ [unitAt j b]) x = true ↔ passes p x = true ∧ x j = b := by
  simp [passes,unitAt,satisfeita,Literal.vale]

theorem one_clause_separates (i j : Fin n) :
    let S := {v : Fin n | v ≠ j}
    let z := fun _ : Fin n => false
    support (signedCNF (signedAt i false) ++ [unitAt j false]) S z ∧
    ¬ support (signedCNF (signedAt i true) ++ [unitAt j false]) S z := by
  dsimp only
  constructor
  · refine ⟨fun _ => false, fun _ _ => rfl, (append_unit _ _ _ _).mpr ⟨?_,rfl⟩⟩
    exact (signed_read _ _).mpr ⟨i, by simp [signedAt]⟩
  · rintro ⟨x,hagree,hpass⟩
    obtain ⟨hp,hj⟩ := (append_unit _ _ _ _).mp hpass
    obtain ⟨w,hw⟩ := (signed_read _ _).mp hp
    have zero : x w = false := by
      by_cases e : w = j
      · simpa [e] using hj
      · exact hagree w e
    simp [zero,signedAt] at hw

/-- There is no update of the proper support profile alone (even granting
free access to all proper existential projections). It cannot retain every
next proper profile. Distinct indexed states or witness counts may do more. -/
theorem no_profile_update (i j : Fin n) :
    ¬ ∃ advance : Profile n → Clausula n → Profile n,
        ∀ (p : CNF n) c, advance (profile p) c = profile (p ++ [c]) := by
  rintro ⟨advance,exactness⟩
  let f := signedCNF (signedAt i false)
  let g := signedCNF (signedAt i true)
  let c := unitAt j false
  have h : profile (f ++ [c]) = profile (g ++ [c]) := by
    rw [← exactness f c, ← exactness g c, profiles_agree (signedAt i false) (signedAt i true)]
  let S := {v : Fin n | v ≠ j}
  have proper : ∃ v, v ∉ S := ⟨j, by simp [S]⟩
  have e := congrArg (fun z : Profile n => z S proper (fun _ => false)) h
  have diff := one_clause_separates i j
  exact diff.2 (e.mp diff.1)

/-- A common continuation, without enumerating masks. -/
def sealOthers (i : Fin n) : CNF n :=
  ((List.finRange n).filter (fun j => j != i)).map (fun j => unitAt j false)

private theorem seal_iff (i : Fin n) (x : Fin n → Bool) :
    passes (sealOthers i) x = true ↔ ∀ j, j ≠ i → x j = false := by
  simp [passes,sealOthers,unitAt,satisfeita,Literal.vale,List.all_eq_true]
  constructor
  · exact fun hs j hj => (hs j).resolve_left hj
  · intro hs j
    by_cases h : j = i
    · exact Or.inl h
    · exact Or.inr (hs j h)

theorem after_common_suffix (i : Fin n) (b : Bool) (x : Fin n → Bool) :
    passes (signedCNF (signedAt i b) ++ sealOthers i) x = true ↔
      x i = b ∧ ∀ j, j ≠ i → x j = false := by
  have split (p q : CNF n) : passes (p ++ q) x = (passes p x && passes q x) := by
    simp [passes]
  rw [split,Bool.and_eq_true,signed_read,seal_iff]
  constructor
  · rintro ⟨⟨w,hw⟩,hz⟩
    by_cases e : w = i
    · exact ⟨by simpa [signedAt,e] using hw,hz⟩
    · simp [signedAt,e,hz w e] at hw
  · rintro ⟨hb,hz⟩
    exact ⟨⟨i,by simpa [signedAt] using hb⟩,hz⟩

theorem surviving_branch (i : Fin n) (b a : Bool) :
    palavraDaFormula (restrictVar i a (signedCNF (signedAt i b) ++ sealOthers i)) = true ↔ a = b := by
  rw [a_palavra_e_o_sat,sat_iff]
  constructor
  · rintro ⟨x,hx⟩
    rw [branch_read] at hx
    simpa using ((after_common_suffix _ _ _).mp hx).1
  · rintro rfl
    refine ⟨fun _ => false,?_⟩
    rw [branch_read,after_common_suffix]
    exact ⟨by simp,fun j hj => by simp [hj]⟩

/-- The smallest three-label instance comparing *all pairs*. -/
theorem all_pairs_in_three (s t : Fin 3 → Bool) (i j : Fin 3) (u : Fin 3 → Bool) :
    support (signedCNF s) {i,j} u ↔ support (signedCNF t) {i,j} u := by
  have missing : ∃ k : Fin 3, k ∉ ({i,j} : Set (Fin 3)) := by
    fin_cases i <;> fin_cases j <;> decide
  exact ⟨fun _ => all_proper_supports t _ missing u, fun _ => all_proper_supports s _ missing u⟩

/-- Four clauses with opposite parity costs. These finite formulas are for the
weighted obstruction only; the arbitrary-width support obstruction above uses one. -/
def parityCNF (q : Bool) : CNF 3 :=
  [[⟨0,true⟩,⟨1,true⟩,⟨2,q⟩],
   [⟨0,true⟩,⟨1,false⟩,⟨2,!q⟩],
   [⟨0,false⟩,⟨1,true⟩,⟨2,!q⟩],
   [⟨0,false⟩,⟨1,false⟩,⟨2,q⟩]]

private def toggle (j : Fin 3) (x : Fin 3 → Bool) : Fin 3 → Bool :=
  fun i => if i = j then !(x i) else x i

private theorem toggle_twice (j : Fin 3) (x : Fin 3 → Bool) : toggle j (toggle j x) = x := by
  funext i
  by_cases h : i = j <;> simp [toggle,h]

private def toggleEquiv (j : Fin 3) : (Fin 3 → Bool) ≃ (Fin 3 → Bool) :=
  ⟨toggle j,toggle j,toggle_twice j,toggle_twice j⟩

private theorem toggled_cost (j : Fin 3) (x : Fin 3 → Bool) :
    custoCNF (parityCNF false) x = custoCNF (parityCNF true) (toggle j x) := by
  fin_cases j <;> cases h0 : x 0 <;> cases h1 : x 1 <;> cases h2 : x 2 <;>
    simp [parityCNF,custoCNF,satisfeita,Literal.vale,toggle,h0,h1,h2,Fin.isValue]

/-- Conditional weighted sum on one labeled slice, used as a mathematical
descriptor only. The weight may be any function of violation count. -/
noncomputable def weightedSlice (p : CNF 3) (S : Set (Fin 3)) (u : Fin 3 → Bool)
    (weight : Nat → ℝ) : ℝ := by
  classical
  exact ∑ x : Fin 3 → Bool,
    if ∀ i ∈ S, x i = u i then weight (custoCNF p x) else 0

theorem parity_partial_weights (S : Set (Fin 3)) (omits : ∃ j, j ∉ S) (u : Fin 3 → Bool)
    (weight : Nat → ℝ) :
    weightedSlice (parityCNF false) S u weight = weightedSlice (parityCNF true) S u weight := by
  classical
  obtain ⟨j,hj⟩ := omits
  unfold weightedSlice
  refine Fintype.sum_equiv (toggleEquiv j) _ _ ?_
  intro x
  change (if ∀ i ∈ S, x i = u i then weight (custoCNF _ x) else 0) =
    (if ∀ i ∈ S, toggle j x i = u i then weight (custoCNF _ (toggle j x)) else 0)
  have same (i : Fin 3) (hi : i ∈ S) : toggle j x i = x i := by
    have ne : i ≠ j := fun e => hj (e ▸ hi)
    simp [toggle,ne]
  have reflects : (∀ i ∈ S, toggle j x i = u i) ↔ (∀ i ∈ S, x i = u i) :=
    ⟨fun h i hi => (same i hi).symm.trans (h i hi),
     fun h i hi => (same i hi).trans (h i hi)⟩
  by_cases hx : ∀ i ∈ S, x i = u i
  · rw [if_pos hx,if_pos (reflects.mpr hx)]
    exact congrArg weight (toggled_cost j x)
  · rw [if_neg hx,if_neg (fun h => hx (reflects.mp h))]

theorem parity_opposite_branches (q a : Bool) :
    palavraDaFormula (restrictVar (2:Fin 3) a
      (parityCNF q ++ [unitAt 0 false,unitAt 1 false])) = true ↔ a = q := by
  rw [a_palavra_e_o_sat,sat_iff]
  constructor
  · rintro ⟨x,hx⟩
    rw [branch_read] at hx
    cases q <;> cases a <;> cases h0 : x 0 <;> cases h1 : x 1 <;>
      simp_all [passes,parityCNF,unitAt,satisfeita,Literal.vale,Function.update]
  · rintro rfl
    refine ⟨fun _ => false,?_⟩
    rw [branch_read]
    cases a <;> simp [passes,parityCNF,unitAt,satisfeita,Literal.vale,Function.update]

/-- Even after the weighted agreement above, ONE new clause changes the
pair feasibility query at (x₀=false,x₁=false) differently. -/
theorem parity_pair_changes_after_one :
    let S : Set (Fin 3) := {0,1}
    let z := fun _ : Fin 3 => false
    support (parityCNF false ++ [unitAt 2 false]) S z ∧
      ¬ support (parityCNF true ++ [unitAt 2 false]) S z := by
  dsimp only
  constructor
  · exact ⟨fun _ => false,fun _ _ => rfl,by decide⟩
  · rintro ⟨x,row,h⟩
    have h₀ : x 0 = false := row 0 (by simp)
    have h₁ : x 1 = false := row 1 (by simp)
    cases h₂ : x 2 <;> simp [passes,parityCNF,unitAt,satisfeita,Literal.vale,h₀,h₁,h₂] at h

end Codex.ProjectionLimit
