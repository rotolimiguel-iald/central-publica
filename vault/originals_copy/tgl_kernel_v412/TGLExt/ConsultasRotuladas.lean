import TGLExt.PsiBitNaFronteira
import TGLExt.OPsiBitDaFormula

set_option autoImplicit false

namespace Codex.LabeledQueries

open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula
open IALD.PsiBitNaFronteira (Letter encode bits bits_encode)
open IALD.LeitorDaFormula (passes sat_iff)

variable {n : ℕ}
abbrev Mask (n : ℕ) := Fin n → Letter

def allowed (M : Mask n) (i : Fin n) (b : Bool) : Bool :=
  if b then (bits (M i)).2 else (bits (M i)).1

def compatible (M : Mask n) (x : Fin n → Bool) : Prop :=
  ∀ i, allowed M i (x i) = true

def ban (M : Mask n) (l : Literal n) : Mask n := fun i =>
  encode (allowed M i false && !(decide (i = l.var) && (false == l.pos)))
         (allowed M i true  && !(decide (i = l.var) && (true == l.pos)))

theorem allowed_ban (M : Mask n) (l : Literal n) (i : Fin n) (b : Bool) :
    allowed (ban M l) i b =
      (allowed M i b && !(decide (i = l.var) && (b == l.pos))) := by
  cases b <;> simp [allowed, ban, bits_encode]

theorem compatible_ban (M : Mask n) (l : Literal n) (x : Fin n → Bool) :
    compatible (ban M l) x ↔ compatible M x ∧ l.vale x = false := by
  constructor
  · intro h
    have keep (i : Fin n) : allowed M i (x i) = true ∧
        (!(decide (i = l.var) && (x i == l.pos))) = true := by
      simpa only [allowed_ban, Bool.and_eq_true] using h i
    refine ⟨fun i => (keep i).1, ?_⟩
    simpa [Literal.vale] using (keep l.var).2
  · rintro ⟨hold,hl⟩ i
    rw [allowed_ban, hold i]
    by_cases hi : i = l.var
    · subst i
      simpa [Literal.vale] using hl
    · simp [hi]

/-- A single labeled rectangle specifying exactly the assignments where the clause fails. -/
def miss (M : Mask n) (c : Clausula n) := c.foldl ban M

theorem compatible_miss (M : Mask n) (c : Clausula n) (x : Fin n → Bool) :
    compatible (miss M c) x ↔ compatible M x ∧ satisfeita c x = false := by
  induction c generalizing M with
  | nil => simp [miss, satisfeita]
  | cons l c ih =>
    change compatible (miss (ban M l) c) x ↔ compatible M x ∧ (l.vale x || satisfeita c x) = false
    rw [ih, compatible_ban, Bool.or_eq_false_iff]
    exact and_assoc

def volume (M : Mask n) : ℕ :=
  ∏ i, (∑ b : Bool, if allowed M i b then 1 else 0)

/-- Executable query route. The second component counts base-volume evaluations of this recursion. -/
def run : CNF n → Mask n → ℕ × ℕ
  | [], M => (volume M, 1)
  | c :: p, M =>
    let a := run p M
    let b := run p (miss M c)
    (a.1 - b.1, a.2 + b.2)

noncomputable def count (M : Mask n) (p : CNF n) : ℕ := by
  classical
  exact ∑ x : Fin n → Bool, if compatible M x ∧ passes p x = true then 1 else 0

theorem volume_correct (M : Mask n) : volume M = count M [] := by
  classical
  unfold volume count
  rw [Fintype.prod_sum]
  apply Finset.sum_congr rfl
  intro x _
  by_cases h : compatible M x
  · simp [h, passes, h _]
  · have h' : ¬ ∀ i, allowed M i (x i) = true := h
    obtain ⟨i, hi⟩ := not_forall.mp h'
    have hz : (∏ j, (if allowed M j (x j) then 1 else 0 : ℕ)) = 0 :=
      Finset.prod_eq_zero (Finset.mem_univ i) (if_neg hi)
    simp [hz, h]

theorem count_split (M : Mask n) (c : Clausula n) (p : CNF n) :
    count M (c :: p) + count (miss M c) p = count M p := by
  classical
  unfold count
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro x _
  rw [compatible_miss]
  have hcons : passes (c :: p) x = (satisfeita c x && passes p x) := by simp [passes]
  rw [hcons]
  by_cases h : compatible M x <;> cases satisfeita c x <;> cases passes p x <;> simp [h]

theorem run_exact (p : CNF n) (M : Mask n) :
    (run p M).1 = count M p ∧ (run p M).2 = 2 ^ p.length := by
  induction p generalizing M with
  | nil => exact ⟨volume_correct M, rfl⟩
  | cons c p ih =>
    have ha := ih M
    have hb := ih (miss M c)
    have hs := count_split M c p
    constructor
    · change (run p M).1 - (run p (miss M c)).1 = _
      rw [ha.1, hb.1, ← hs, Nat.add_sub_cancel]
    · change (run p M).2 + (run p (miss M c)).2 = _
      rw [ha.2, hb.2, List.length_cons, pow_succ, Nat.mul_two]

def free : Mask n := fun _ => .both

theorem reads_word (p : CNF n) :
    decide (0 < (run p free).1) = palavraDaFormula p := by
  classical
  rw [(run_exact p free).1]
  apply Bool.eq_iff_iff.mpr
  rw [decide_eq_true_eq, a_palavra_e_o_sat, sat_iff]
  unfold count
  rw [Finset.sum_pos_iff_of_nonneg (fun _ _ => Nat.zero_le _)]
  simp [compatible, free, allowed, bits]
  apply exists_congr
  intro x
  cases h : passes p x <;> simp

end Codex.LabeledQueries
