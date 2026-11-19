import TGLExt.LeituraCertificada
import TGLExt.LeitorDeReuso
import TGLExt.CacheDeRamos

/-! Preserve the certificates from the first physical scanner. Rewind the
same original input for a second physical scanner only if needed. An
unresolved pair requests a shared reached-key layer. The movement bound
ends at the interface to that last, finite-set computation. -/
set_option autoImplicit false
namespace Codex.ReuseDispatch
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula IALD.LeitorDaFormula
open Codex.PolinomioPorEscolha Codex.SignProfile Codex.TwoSweeps
open Codex.SecondRead (lane)
open Codex.CertifiedRead (classify readTape)
open Codex.LiteralSearchCost (delayed every_branch_possible)

abbrev PartialPair := Option Bool × Option Bool

def pickLane (p : PartialPair) (b : Bool) := if b then p.2 else p.1
def complete (p : PartialPair) := p.1.isSome && p.2.isSome
def originalAnswers (w : List Letter) : PartialPair :=
  let tape := readTape w
  (classify tape false, classify tape true)

def upgrade (answer : Option Bool) (positive : Bool) : Option Bool :=
  match answer with
  | some v => some v
  | none => if positive then some true else none

def overlay (old : PartialPair) (more : Unit → Bool × Bool) : PartialPair :=
  if complete old then old else
    let q := more ()
    (upgrade old.1 q.1,upgrade old.2 q.2)

def physical (w : List Letter) : PartialPair :=
  overlay (originalAnswers w) (fun _ => ReuseReader.read (returned w).1)

private theorem overlay_lane (old : PartialPair) (more : Unit → Bool × Bool) (b : Bool) :
    pickLane (overlay old more) b = upgrade (pickLane old b) (lane (more ()) b) := by
  obtain ⟨a,d⟩ := old
  cases a <;> cases d <;> cases b <;> rfl

theorem physical_lane (w : List Letter) (b : Bool) :
    pickLane (physical w) b =
      upgrade (classify (readTape w) b) (lane (ReuseReader.read w) b) := by
  rw [physical,overlay_lane,returned_spec]
  cases b <;> rfl

theorem old_answer_preserved (w : List Letter) (b v : Bool)
    (h : classify (readTape w) b = some v) : pickLane (physical w) b = some v := by
  rw [physical_lane,h]; rfl

private def Valid (answer : Option Bool) (goal : Prop) :=
  ∀ v, answer = some v → (v=true ↔ goal)

private theorem old_valid {n : Nat} (p : CNF (n+1)) (b : Bool) :
    Valid (classify (readTape (original p)) b) (present p b) := by
  intro v h
  cases v with
  | true => simp [CertifiedRead.positive_sound p b h]
  | false => simp [CertifiedRead.negative_sound p b h]

private theorem upgrade_valid {answer : Option Bool} {bit : Bool} {goal : Prop}
    (old : Valid answer goal) (good : bit=true → goal) : Valid (upgrade answer bit) goal := by
  intro v h
  cases e : answer with
  | some d =>
    have eq : some d = some v := by simpa only [e,upgrade] using h
    exact old v (e.trans eq)
  | none =>
    cases k : bit with
    | false => simp [e,k,upgrade] at h
    | true =>
      have hv : v=true := by simpa [e,k,upgrade,eq_comm] using h
      simp [hv,good k]

theorem physical_valid {n : Nat} (p : CNF (n+1)) (b v : Bool)
    (cert : pickLane (physical (original p)) b = some v) : v=true ↔ present p b := by
  rw [physical_lane] at cert
  exact upgrade_valid (old_valid p b) (ReuseReader.positive_sound p b) v cert

/-- Distinct branches are matched before evaluating the typed fallback.
In the double miss there is one shared run, provided by BranchCache.read. -/
def finish {n : Nat} (p : CNF (n+1)) : PartialPair → Bool × Bool
  | (some a,some b) => (a,b)
  | (some a,none) => (a,BranchCache.branch (BranchCache.run p (BranchCache.initial _)) 0 true)
  | (none,some b) => (BranchCache.branch (BranchCache.run p (BranchCache.initial _)) 0 false,b)
  | (none,none) => BranchCache.read p 0

def branches {n : Nat} (p : CNF (n+1)) := finish p (physical (original p))

private theorem finish_lane {n : Nat} (p : CNF (n+1)) (q : PartialPair) (b : Bool) :
    lane (finish p q) b = (pickLane q b).getD
      (BranchCache.branch (BranchCache.run p (BranchCache.initial _)) 0 b) := by
  obtain ⟨a,d⟩ := q
  cases a <;> cases d <;> cases b <;> rfl

theorem branch_exact {n : Nat} (p : CNF (n+1)) (b : Bool) :
    lane (branches p) b = true ↔ present p b := by
  rw [branches,finish_lane]
  cases e : pickLane (physical (original p)) b with
  | none => exact BranchCache.branch_correct p 0 b
  | some v => exact physical_valid p b v e

def decision : {n : Nat} → CNF n → Bool
  | 0,p => (original p).isEmpty
  | _+1,p => let q := branches p; q.1 || q.2

private theorem word_zero (p : CNF 0) : (original p).isEmpty = palavraDaFormula p := by
  apply Bool.eq_iff_iff.mpr
  rw [a_palavra_e_o_sat,sat_iff]
  cases p with
  | nil => simp [original,passes]
  | cons c p =>
    have empty : c = [] := by
      cases c with
      | nil => rfl
      | cons l _ => exact Fin.elim0 l.var
    simp [empty,original,spellClause,passes,satisfeita]

theorem decision_exact {n : Nat} (p : CNF n) : decision p = palavraDaFormula p := by
  cases n with
  | zero => exact word_zero p
  | succ k =>
    apply Bool.eq_iff_iff.mpr
    rw [word_from_pair]
    change ((branches p).1 || (branches p).2) = true ↔ _
    rw [Bool.or_eq_true]
    exact or_congr (branch_exact p false) (branch_exact p true)

/-- Displacement of the physical portion only. The second reader starts on
its own fresh work tapes after rewinding the original input head. -/
def physicalMoves (w : List Letter) :=
  if complete (originalAnswers w) then CertifiedRead.headMovements w else
    CertifiedRead.headMovements w + (returned w).2 + ReuseReader.movements (returned w).1

theorem before_cache_bound (w : List Letter) : physicalMoves w ≤ 23*w.length+4 := by
  have a := CertifiedRead.at_most_seven_per_letter w
  have b := ReuseReader.linear_travel w
  simp only [physicalMoves,returned_spec]
  split <;> omega

theorem delayed_avoids_cache (k : Nat) :
    physical (original (delayed k)) = (some true,some true) := by
  have both (b : Bool) : pickLane (physical (original (delayed k))) b = some true := by
    rw [physical_lane,(ReuseReader.delayed_result k).1]
    cases e : classify (readTape (original (delayed k))) b with
    | none => cases b <;> rfl
    | some v =>
      have hv := ((old_valid _ b) v e).mpr (every_branch_possible k b)
      subst v
      rfl
  exact Prod.ext (both false) (both true)

theorem delayed_cost (k : Nat) :
    physicalMoves (original (delayed k)) ≤ 23*(6*k+14)+4 := by
  simpa only [LiteralSearchCost.delayed_letters] using before_cache_bound (original (delayed k))

end Codex.ReuseDispatch
