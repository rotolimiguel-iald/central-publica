import TGLExt.OPsiBitDaFormula
import TGLExt.LeitorDaFormula
import Mathlib.Tactic

set_option autoImplicit false
namespace Codex.HornCross
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula IALD.LeitorDaFormula
variable {n : Nat}
abbrev Mem (n : Nat) := Finset (Fin n)

structure Rule (n : Nat) where
  body : List (Fin n)
  head : Option (Fin n)
deriving DecidableEq

def active (s : Mem n) (r : Rule n) := r.body.all (fun i => decide (i ∈ s))
def hit (s : Mem n) (r : Rule n) := r.head.elim false (fun i => decide (i ∈ s))
def ok (s : Mem n) (r : Rule n) := !active s r || hit s r
def stepRule (s : Mem n) (r : Rule n) : Mem n :=
  if active s r then r.head.elim s (fun i => insert i s) else s

def sweep (p : List (Rule n)) (s : Mem n) := p.foldl stepRule s
def heads (p : List (Rule n)) := (p.filterMap Rule.head).toFinset
def valid (p : List (Rule n)) (s : Mem n) := p.all (ok s)
def asClause (r : Rule n) : Clausula n :=
  (r.body.map (fun i => ⟨i,false⟩)) ++ (r.head.toList.map (fun i => ⟨i,true⟩))
def readMem (s : Mem n) : Fin n → Bool := fun i => decide (i ∈ s)
def fromAssignment (x : Fin n → Bool) : Mem n := Finset.univ.filter fun i => x i

@[simp] theorem read_from (x : Fin n → Bool) : readMem (fromAssignment x) = x := by
  funext i
  simp [readMem,fromAssignment]

theorem active_iff (s : Mem n) (r : Rule n) : active s r = true ↔ ∀ i ∈ r.body, i ∈ s := by
  simp [active,List.all_eq_true]
theorem hit_iff (s : Mem n) (r : Rule n) : hit s r = true ↔ ∃ i ∈ r.head, i ∈ s := by
  cases r with
  | mk b h => cases h <;> simp [hit]

theorem clause_eq (s : Mem n) (r : Rule n) : satisfeita (asClause r) (readMem s) = ok s r := by
  apply Bool.eq_iff_iff.mpr
  simp only [ok,Bool.or_eq_true, Bool.not_eq_true']
  simp only [Bool.eq_false_iff, hit_iff]
  classical
  cases r with
  | mk b h =>
    cases h <;> simp [asClause,satisfeita,List.any_append,List.any_eq_true,Literal.vale,readMem,active]

theorem valid_eq (p : List (Rule n)) (s : Mem n) :
    passes (p.map asClause) (readMem s) = valid p s := by
  simp [passes,valid,List.all_map,Function.comp_def,clause_eq]

theorem step_extends (s : Mem n) (r : Rule n) : s ⊆ stepRule s r := by
  unfold stepRule
  split <;> cases r.head <;> simp
theorem sweep_extends (p : List (Rule n)) (s : Mem n) : s ⊆ sweep p s := by
  induction p generalizing s with
  | nil => exact Finset.Subset.rfl
  | cons r p ih => exact (step_extends s r).trans (ih _)

theorem step_le_model (s t : Mem n) (r : Rule n) (hs : s ⊆ t) (hr : ok t r = true) :
    stepRule s r ⊆ t := by
  by_cases ha : active s r = true
  · have ht : active t r = true := (active_iff _ _).2 (fun i hi => hs ((active_iff _ _).1 ha i hi))
    have hh : hit t r = true := by simpa [ok,ht] using hr
    obtain ⟨i,hi,hm⟩ := (hit_iff _ _).1 hh
    have he : r.head = some i := hi
    simpa [stepRule,ha,he] using Finset.insert_subset hm hs
  · simpa [stepRule,ha] using hs

theorem sweep_le_model (p : List (Rule n)) (s t : Mem n) (hs : s ⊆ t) (ht : valid p t = true) :
    sweep p s ⊆ t := by
  induction p generalizing s with
  | nil => exact hs
  | cons r p ih =>
    have both : ok t r = true ∧ valid p t = true := by simpa [valid] using ht
    obtain ⟨hr,hp⟩ := both
    exact ih (stepRule s r) (step_le_model _ _ _ hs hr) hp

theorem step_within (p : List (Rule n)) (r : Rule n) (hr : r ∈ p) (s : Mem n)
    (hs : s ⊆ heads p) : stepRule s r ⊆ heads p := by
  by_cases ha : active s r = true
  · cases he : r.head with
    | none => simpa [stepRule,ha,he] using hs
    | some i =>
      have hi : i ∈ heads p := by simpa [heads] using (List.mem_filterMap.mpr ⟨r,hr,he⟩ : i ∈ p.filterMap Rule.head)
      simpa [stepRule,ha,he] using Finset.insert_subset hi hs
  · simpa [stepRule,ha] using hs

theorem sweep_within (p : List (Rule n)) (s : Mem n) (hs : s ⊆ heads p) : sweep p s ⊆ heads p := by
  generalize h : p = q at ⊢
  subst q
  suffices ∀ (q : List (Rule n)) (a : Mem n), (∀ r ∈ q, r ∈ p) → a ⊆ heads p → sweep q a ⊆ heads p by
    exact this p s (fun _ hi => hi) hs
  intro q
  induction q with
  | nil => intro a _ h; exact h
  | cons r q ih =>
    intro a h ha
    exact ih _ (fun i hi => h i (List.mem_cons_of_mem _ hi))
      (step_within p r (h _ List.mem_cons_self) a ha)

def settle (p : List (Rule n)) : Nat → Mem n → Mem n
  | 0, s => s
  | k+1, s => let u := sweep p s; if u = s then s else settle p k u

theorem stable (p : List (Rule n)) (k : Nat) (s : Mem n) (hs : s ⊆ heads p)
    (hk : (heads p).card < s.card+k) : sweep p (settle p k s) = settle p k s := by
  induction k generalizing s with
  | zero => have := Finset.card_le_card hs; omega
  | succ k ih =>
    by_cases he : sweep p s = s
    · simp [settle,he]
    · have hlt : s.card < (sweep p s).card := Finset.card_lt_card
          (Finset.ssubset_iff_subset_ne.mpr ⟨sweep_extends p s, Ne.symm he⟩)
      simpa only [settle,if_neg he] using ih (sweep p s) (sweep_within p s hs) (by omega)

theorem settle_le_model (p : List (Rule n)) (k : Nat) (s t : Mem n) (hs : s ⊆ t) (ht : valid p t = true) :
    settle p k s ⊆ t := by
  induction k generalizing s with
  | zero => exact hs
  | succ k ih =>
    simp only [settle]
    split
    · exact hs
    · exact ih _ (sweep_le_model _ _ _ hs ht)

def closure (p : List (Rule n)) := settle p (p.length+1) ∅
theorem closure_stable (p : List (Rule n)) : sweep p (closure p) = closure p := by
  apply stable
  · simp
  · have h := List.toFinset_card_le (p.filterMap Rule.head)
    have h' := List.length_filterMap_le Rule.head p
    simp only [Finset.card_empty,Nat.zero_add]
    unfold heads
    omega

theorem each_stable (p : List (Rule n)) (s : Mem n) (he : sweep p s = s) :
    ∀ r ∈ p, stepRule s r = s := by
  induction p with
  | nil => simp
  | cons a p ih =>
    have hsub := sweep_extends p (stepRule s a)
    change sweep p (stepRule s a) = s at he
    rw [he] at hsub
    have hu : stepRule s a = s := Finset.Subset.antisymm hsub (step_extends _ _)
    have hp : sweep p s = s := by simpa only [sweep,List.foldl_cons,hu] using he
    intro r hr
    rcases List.mem_cons.mp hr with h|h
    · simpa only [h] using hu
    · exact ih hp r h

/-- A violated clause at a closed state must have empty head. Its body already fires in every model. -/
theorem closed_complete (p : List (Rule n)) (s t : Mem n) (st : s ⊆ t)
    (he : sweep p s = s) (ht : valid p t = true) : valid p s = true := by
  apply List.all_eq_true.mpr
  intro r hr
  by_cases h : active s r = true
  · have ha : active t r = true := (active_iff _ _).2 (fun i hi => st ((active_iff _ _).1 h i hi))
    have hv := List.all_eq_true.mp ht r hr
    have hh : hit t r = true := by simpa [ok,ha] using hv
    obtain ⟨i,hi,_⟩ := (hit_iff _ _).1 hh
    have hh' : r.head = some i := hi
    have heq := each_stable p s he r hr
    have hin : i ∈ stepRule s r := by simp [stepRule,h,hh']
    rw [heq] at hin
    simp [ok,h,hit,hh',hin]
  · simp [ok,h]

theorem horn_word (p : List (Rule n)) :
    valid p (closure p) = palavraDaFormula (p.map asClause) := by
  apply Bool.eq_iff_iff.mpr
  rw [a_palavra_e_o_sat,sat_iff]
  constructor
  · intro h; exact ⟨_,(valid_eq _ _).trans h⟩
  · rintro ⟨x,hx⟩
    let t := fromAssignment x
    have ht : valid p t = true := by simpa only [← valid_eq, t, read_from] using hx
    exact closed_complete p _ t (settle_le_model _ _ _ _ (by simp) ht) (closure_stable _) ht

end Codex.HornCross
