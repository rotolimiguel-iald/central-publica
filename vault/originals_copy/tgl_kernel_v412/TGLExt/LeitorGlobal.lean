import TGLExt.RestricaoGlobal
import TGLExt.ChecagemHorn

/-! A fixed sequence of shared pivots is applied to every clause. The evaluator
does not build a table of models. The independent cost certificate below charges
the actual head moves of every Horn run, starting on its compiled program. -/
set_option autoImplicit false
namespace Codex.SharedReader
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula Codex.SharedBranch Codex.HornResidual
open Codex.CrossSelectors Codex.HornCross Codex.PolinomioPorEscolha Codex.SparseHornTape
variable {n : Nat}

open IALD.LeitorDaFormula (passes bitSign)
open TGLExt.Psibit

/-- Each polarity reads the prefix and the continuation with the SAME pivot value
and external assignment. The angle certifies the signs after both bits are read. -/
theorem psibit_with_continuation (i : Fin n) (p s : CNF n) (x : Fin n → Bool) :
    ∃ θ : ℝ,
      (codeAmp θ).word = bitSign (passes (restrictVar i false p ++ restrictVar i false s) x) ∧
      (codeAmp θ).verb = bitSign (passes (restrictVar i true p ++ restrictVar i true s) x) ∧
      (codeAmp θ).word = bitSign (passes (p++s) (Function.update x i false)) ∧
      (codeAmp θ).verb = bitSign (passes (p++s) (Function.update x i true)) ∧
      decodeAmp (codeAmp θ) = v θ := by
  have separate (b : Bool) : restrictVar i b (p++s) = restrictVar i b p ++ restrictVar i b s := by
    simp only [restrictVar,List.filterMap_append]
  have nz (v : Bool) : bitSign v ≠ 0 := by cases v <;> decide
  obtain ⟨θ,ha,hb⟩ := the_orbit_visits_all_four_states _ _
    (nz (passes (p++s) (Function.update x i false))) (nz (passes (p++s) (Function.update x i true)))
  exact ⟨θ,by rw [← separate, branch_read]; exact ha,
    by rw [← separate, branch_read]; exact hb,ha,hb,decodeAmp_codeAmp θ⟩

def both (left right : Option Bool) : Option Bool :=
  match left,right with
  | some a,some b => some (a || b)
  | _,_ => none

def readPlan : List (Fin n) → CNF n → Option Bool
  | [],p => (parseProgram p).map checkProgram
  | i :: is,p => both (readPlan is (restrictVar i false p)) (readPlan is (restrictVar i true p))

def ready : List (Fin n) → CNF n → Prop
  | [],p => ∃ q, parseProgram p = some q
  | i :: is,p => ready is (restrictVar i false p) ∧ ready is (restrictVar i true p)

theorem reader_spec (is : List (Fin n)) (p : CNF n) :
    (ready is p → readPlan is p = some (palavraDaFormula p)) ∧
    (¬ ready is p → readPlan is p = none) := by
  induction is generalizing p with
  | nil => cases h : parseProgram p with
    | none => simp [ready,readPlan,h]
    | some q => simp [ready,readPlan,h,parse_word h]
  | cons i is ih =>
    have l := ih (restrictVar i false p)
    have r := ih (restrictVar i true p)
    by_cases hl : ready is (restrictVar i false p) <;>
      by_cases hr : ready is (restrictVar i true p)
    · simp [ready,readPlan,hl,hr,l.1 hl,r.1 hr,both,word_split i p]
    · cases hh : readPlan is (restrictVar i false p) <;>
        simp_all [ready,readPlan,both]
    · simp [ready,readPlan,hl,both,l.2 hl]
    · simp [ready,readPlan,hl,both,l.2 hl]

/-- Every leaf starts on the compiled unary Horn tape. The final field is the sum
of physical movements of both heads, across *all* leaves visited by the plan. -/
inductive Trace : List (Fin n) → CNF n → Bool → Nat → Prop
  | leaf {p : CNF n} {q : List (Rule n)} {t : Nat} {a : Bool} :
      parseProgram p = some q → (run t (start q ∅)).mode = .halt a →
      Trace [] p a (travel t (start q ∅))
  | fork {i : Fin n} {is : List (Fin n)} {p : CNF n} {a b : Bool} {l r : Nat} :
      Trace is (restrictVar i false p) a l → Trace is (restrictVar i true p) b r →
      Trace (i :: is) p (a || b) (l+r)

theorem cost_on_horn_tapes (is : List (Fin n)) (p : CNF n) (L : Nat)
    (hsize : (original p).length ≤ L) (hready : ready is p) :
    ∃ moves ≤ 2^is.length * (2*budget L), Trace is p (palavraDaFormula p) moves := by
  induction is generalizing p with
  | nil =>
    obtain ⟨q,hq⟩ := hready
    have member : q ∈ programs p := by rw [sole_program hq]; simp
    obtain ⟨t,_,hm,he⟩ := every_candidate p q member
    refine ⟨travel t (start q ∅),?_,Trace.leaf (t := t) hq ?_⟩
    · simpa using hm.trans (Nat.mul_le_mul_left 2 (budget_le _ _ hsize))
    · simpa only [parse_word hq] using he
  | cons i is ih =>
    obtain ⟨l,hl,tl⟩ := ih _ ((restrict_size i false p).trans hsize) hready.1
    obtain ⟨r,hr,tr⟩ := ih _ ((restrict_size i true p).trans hsize) hready.2
    refine ⟨l+r,?_,?_⟩
    · simp only [List.length_cons,pow_succ]
      calc l+r ≤ 2^is.length*(2*budget L) + 2^is.length*(2*budget L) := Nat.add_le_add hl hr
           _ = _ := by ring
    · rw [word_split i p]
      exact Trace.fork tl tr

end Codex.SharedReader
