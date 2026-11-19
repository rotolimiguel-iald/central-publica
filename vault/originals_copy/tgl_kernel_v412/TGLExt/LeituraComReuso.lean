import TGLExt.LimiteDoReuso

/-! On a missed lane the dispatcher now runs the clause-skipping scan.
On two misses it builds the layer once and queries it twice. -/
set_option autoImplicit false
namespace Codex.CachedDispatch

open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula IALD.LeitorDaFormula
open Codex.ReuseDispatch (PartialPair physical complete)
open Codex.PolinomioPorEscolha (original)

def finish {n : Nat} (p : CNF (n+1)) : PartialPair → Bool × Bool
  | (some a, some b) => (a,b)
  | (some a, none) => (a, BranchCache.branch (CoverCache.scan p (BranchCache.initial _)) 0 true)
  | (none, some b) => (BranchCache.branch (CoverCache.scan p (BranchCache.initial _)) 0 false,b)
  | (none, none) => CoverCache.read p 0

private theorem same_bit {n : Nat} (p : CNF (n+1)) (b : Bool) :
    BranchCache.branch (CoverCache.scan p (BranchCache.initial _)) 0 b =
      BranchCache.branch (BranchCache.run p (BranchCache.initial _)) 0 b := by
  apply Bool.eq_iff_iff.mpr
  apply Iff.trans _ (BranchCache.branch_correct p 0 b).symm
  have h := CoverCache.read_exact p 0 b
  cases b <;> exact h

theorem finish_eq {n : Nat} (p : CNF (n+1)) (q : PartialPair) :
    finish p q = ReuseDispatch.finish p q := by
  obtain ⟨a,b⟩ := q
  cases a <;> cases b <;> simp only [finish, ReuseDispatch.finish, CoverCache.read,
    BranchCache.read, same_bit]

def word : {n : Nat} → CNF n → Bool
  | 0,p => ReuseDispatch.decision p
  | _+1,p => let q := finish p (physical (original p)); q.1 || q.2

theorem word_exact {n : Nat} (p : CNF n) : word p = palavraDaFormula p := by
  cases n with
  | zero => exact ReuseDispatch.decision_exact p
  | succ n =>
    simp only [word,finish_eq]
    exact ReuseDispatch.decision_exact p

def chargedExtensions {n : Nat} (p : CNF n) : Nat :=
  if complete (physical (original p)) then 0 else CoverCache.extensions p (BranchCache.initial _)

theorem no_extension_on_first_family (k : Nat) :
    chargedExtensions (LiteralSearchCost.delayed k) = 0 := by
  simp [chargedExtensions,ReuseDispatch.delayed_avoids_cache,complete]

theorem reached_cost (k : Nat) :
    2^(k+2) ≤ chargedExtensions (ReachedLayer.gateInput k) := by
  obtain ⟨miss,bound⟩ := CubeLimit.dispatched_extensions k
  simpa [chargedExtensions,miss,complete] using bound

end Codex.CachedDispatch
