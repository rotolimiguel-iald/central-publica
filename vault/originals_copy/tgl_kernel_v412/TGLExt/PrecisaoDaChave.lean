import TGLExt.ObrigacoesJaSatisfeitas

/-! Cost of one specific proposal: sending the dense truth word as a
terminating binary fraction of a turn. Both source formulas have the same
unary spelling length. The discrimination bound is for this sequential
wire, without access to a separate source or a seek oracle. -/
set_option autoImplicit false
namespace Codex.DenseAngle
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula IALD.LeitorDaFormula
open Codex.PolinomioPorEscolha

abbrev Val (w : Nat) := Fin w → Bool

def top (w : Nat) : Val w := fun _ => true
def unitPos {w : Nat} (i : Fin w) : Clausula w := [⟨i,true⟩]
def units (w : Nat) : CNF w := (List.finRange w).map unitPos
def source (n : Nat) (b : Bool) : CNF (n+1) := units (n+1) ++ [[⟨0,b⟩]]

theorem units_force {w : Nat} (x : Val w) : passes (units w) x = true ↔ x = top w := by
  constructor
  · intro h
    apply funext
    intro i
    have hi : unitPos i ∈ units w := List.mem_map.mpr ⟨i,by simp,rfl⟩
    have := List.all_eq_true.mp h _ hi
    simpa [unitPos,satisfeita,Literal.vale,top] using this
  · rintro rfl
    simp [units,unitPos,passes,satisfeita,Literal.vale,top,List.all_eq_true]

theorem source_accepts (n : Nat) (b : Bool) (x : Val (n+1)) :
    passes (source n b) x = true ↔ x=top _ ∧ b=true := by
  have h : passes (source n b) x = (passes (units _) x && (x 0 == b)) := by
    simp [source,passes,satisfeita,Literal.vale]
  rw [h,Bool.and_eq_true,units_force]
  constructor
  · rintro ⟨rfl,hb⟩
    exact ⟨rfl,by simpa [top,eq_comm] using hb⟩
  · rintro ⟨rfl,rfl⟩
    exact ⟨rfl,rfl⟩

theorem source_word (n : Nat) (b : Bool) : palavraDaFormula (source n b) = b := by
  apply Bool.eq_iff_iff.mpr
  rw [a_palavra_e_o_sat,sat_iff]
  constructor
  · rintro ⟨x,h⟩
    exact ((source_accepts n b x).mp h).2
  · intro h
    exact ⟨top _,(source_accepts _ _ _).mpr ⟨rfl,h⟩⟩

private theorem unit_size {w : Nat} (xs : List (Fin w)) :
    (original (xs.map unitPos)).length ≤ xs.length*(w+1) := by
  induction xs with
  | nil => simp [original]
  | cons i xs ih =>
    change (spellClause (unitPos i) ++ original (xs.map unitPos)).length ≤ _
    rw [List.length_append]
    have z : (spellClause (unitPos i)).length = i.val+2 := by
      simp [spellClause,unitPos,spell]
    have hi := i.isLt
    rw [z,List.length_cons,Nat.succ_mul]
    omega

theorem source_size (n : Nat) (b : Bool) :
    (original (source n b)).length = (original (units (n+1))).length+2 ∧
    (original (source n b)).length ≤ (n+1)*(n+2)+2 := by
  have h : (original (source n b)).length = (original (units (n+1))).length+2 := by
    simp [source,original,spellClause,spell]
  refine ⟨h,?_⟩
  rw [h]
  have base := unit_size (List.finRange (n+1))
  simpa [units] using Nat.add_le_add_right base 2

noncomputable def other (w : Nat) : List (Val w) := (Finset.univ.erase (top w)).toList
noncomputable def wire {w : Nat} (p : CNF w) : List Bool :=
  (other w ++ [top w]).map (passes p)

theorem payload (n : Nat) (b : Bool) :
    wire (source n b) = List.replicate ((other (n+1)).length) false ++ [b] := by
  classical
  have lemma1 (xs : List (Val (n+1))) (none : top _ ∉ xs) :
      xs.map (passes (source n b)) = List.replicate xs.length false := by
    induction xs with
    | nil => rfl
    | cons x xs ih =>
      have ne : x ≠ top _ := by
        intro e
        exact none (by simp [e])
      have off : passes (source n b) x = false := by
        cases h : passes (source n b) x with
        | false => rfl
        | true => exact (ne ((source_accepts _ _ _).mp h).1).elim
      have tail : top _ ∉ xs := fun hm => none (List.mem_cons_of_mem _ hm)
      simp [off,ih tail,List.replicate_succ]
  have excluded : top (n+1) ∉ other (n+1) := by simp [other]
  have last : passes (source n b) (top _) = b := by
    apply Bool.eq_iff_iff.mpr
    simp [source_accepts]
  simp [wire,List.map_append,lemma1 _ excluded,last]

theorem digit_count (n : Nat) : (other (n+1)).length+1 = 2^(n+1) := by
  classical
  have := Finset.card_erase_add_one (s := (Finset.univ : Finset (Val (n+1))))
    (a := top (n+1)) (by simp)
  simpa [other,Val,Fintype.card_fun] using this

/-- A rational turn in the terminating expansion at the public word length. -/
def turn : List Bool → ℚ
  | [] => 0
  | b::bs => ((if b then 1 else 0) + turn bs)/2

private theorem turn_pad (m : Nat) (b : Bool) :
    turn (List.replicate m false ++ [b]) = (if b then 1 else 0)*(1/2:ℚ)^(m+1) := by
  induction m with
  | zero => cases b <;> norm_num [turn]
  | succ m ih =>
    rw [List.replicate_succ,List.cons_append]
    change (0 + turn (List.replicate m false ++ [b]))/2 = _
    rw [ih,pow_succ _ (m+1)]
    ring

theorem transmitted_angle (n : Nat) (b : Bool) :
    turn (wire (source n b)) = (if b then 1 else 0)*(1/2:ℚ)^(2^(n+1)) := by
  rw [payload,turn_pad,digit_count]

/-- Even given the common length, the observed prefixes coincide. -/
theorem same_prefix (n t : Nat) (bound : t < 2^(n+1)) :
    (wire (source n false)).take t = (wire (source n true)).take t := by
  have h : t ≤ (other (n+1)).length := by have := digit_count n; omega
  have cut (b : Bool) :
      (wire (source n b)).take t = (List.replicate (other (n+1)).length false).take t := by
    rw [payload]
    apply List.take_append_of_le_length
    simpa using h
  rw [cut false,cut true]

theorem prefix_reader_fails (n t : Nat) (bound : t < 2^(n+1))
    (decode : List Bool → Bool) :
    ¬ ∀ b, decode ((wire (source n b)).take t) = palavraDaFormula (source n b) := by
  intro ok
  have a := ok false
  have d := ok true
  rw [same_prefix n t bound,source_word] at a
  rw [source_word] at d
  simp_all

end Codex.DenseAngle
