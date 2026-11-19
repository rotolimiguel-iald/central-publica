import TGLExt.FitaDoResiduo
import TGLExt.CompilaHornNaFita

set_option autoImplicit false

namespace Codex.BranchCircuit
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula
open PolinomioPorEscolha (Letter original budget)
open SharedBranch (restrictVar)
open IALD

/-- A read-only head going left over its own tape, one cell per recursive step.
The component counting steps is an observer, not a machine register. -/
def rewind {α : Type} : List α → List α → List α × Nat
  | [], right => (right, 0)
  | x :: left, right =>
    let result := rewind left (x :: right)
    (result.1, result.2 + 1)

theorem rewind_trace {α : Type} (left right : List α) :
    rewind left right = (left.reverse ++ right, left.length) := by
  induction left generalizing right with
  | nil => rfl
  | cons x left ih => simp [rewind, ih, List.append_assoc]

/-- Left side of the shared input head. Reconstruction for the second branch
uses this tape in place. This zipper is accounting data, not a copied input. -/
def cross (c : ResidualTape.Cfg) (left : List Letter) : List Letter :=
  match c.mode, c.input with
  | .scan _ _, x :: _ => x :: left
  | _, _ => left

def past (b : Bool) : Nat → ResidualTape.Cfg → List Letter → List Letter
  | 0, _, left => left
  | k+1, c, left => past b k (ResidualTape.step b c) (cross c left)

private theorem conserve_step (b : Bool) (c : ResidualTape.Cfg) (left : List Letter) :
    (cross c left).reverse ++ (ResidualTape.step b c).input = left.reverse ++ c.input := by
  rcases c with ⟨m, ip, out⟩
  cases m with
  | halt => rfl
  | erase =>
    cases out with
    | nil => rfl
    | cons x out => cases x <;> rfl
  | scan seen hit =>
    cases ip with
    | nil => rfl
    | cons x ip =>
      cases x <;> cases seen <;> cases hit <;>
        simp [cross, ResidualTape.step, ResidualTape.reading, List.append_assoc]

theorem conserve (b : Bool) (t : Nat) (c : ResidualTape.Cfg) (left : List Letter) :
    (past b t c left).reverse ++ (ResidualTape.run b t c).input = left.reverse ++ c.input := by
  induction t generalizing c left with
  | zero => rfl
  | succ t ih => exact (ih (ResidualTape.step b c) (cross c left)).trans (conserve_step b c left)

/-- Stopping times of four finite-control phases, as trace witnesses. Each
phase stops at its own marker. Solving starts on the actual output of compiling. -/
structure Clocks where
  cut : Nat
  compile : Nat
  back : Nat
  solve : Nat

def cutStart (raw : List Letter) := ResidualTape.reading false raw []

def cutEnd (b : Bool) (raw : List Letter) (k : Clocks) :=
  ResidualTape.run b k.cut (cutStart raw)

def compileStart (b : Bool) (raw : List Letter) (k : Clocks) :=
  CompilaHornNaFita.ready (rewind (cutEnd b raw k).output []).1 [] none

def compileEnd (b : Bool) (raw : List Letter) (k : Clocks) :=
  CompilaHornNaFita.run k.compile (compileStart b raw k)

def checkerStart (b : Bool) (raw : List Letter) (k : Clocks) :=
  CompilaHornNaFita.dock (compileEnd b raw k)

def checkerEnd (b : Bool) (raw : List Letter) (k : Clocks) :=
  SparseHornTape.run (k.back+k.solve) (checkerStart b raw k)

def finished (b : Bool) (raw : List Letter) (k : Clocks) (answer : Bool) : Prop :=
  (cutEnd b raw k).mode = .halt ∧ (cutEnd b raw k).input = [] ∧
  (compileEnd b raw k).mode = .halt ∧ (checkerEnd b raw k).mode = .halt answer

def leafTravel (b : Bool) (raw : List Letter) (k : Clocks) : Nat :=
  ResidualTape.travel b k.cut (cutStart raw) + (rewind (cutEnd b raw k).output []).2 +
  (CompilaHornNaFita.travel k.compile (compileStart b raw k) +
   SparseHornTape.travel (k.back+k.solve) (checkerStart b raw k))

def sharedReturn (raw : List Letter) (k : Clocks) :=
  rewind (past false k.cut (cutStart raw) []) (cutEnd false raw k).input

theorem shared_return (raw : List Letter) (k : Clocks) (h : (cutEnd false raw k).input = []) :
    sharedReturn raw k = (raw,raw.length) := by
  have hc := conserve false k.cut (cutStart raw) []
  change (past false k.cut (cutStart raw) []).reverse ++ (cutEnd false raw k).input = raw at hc
  rw [h, List.append_nil] at hc
  have hl := congrArg List.length hc
  rw [List.length_reverse] at hl
  rw [sharedReturn,rewind_trace,h,List.append_nil,hc,hl]

variable {n : Nat}

theorem complete_leaf (b : Bool) (p : CNF (n+1)) (horn : CompilaHornNaFita.IsHorn (restrictVar 0 b p)) :
    ∃ k, finished b (original p) k (palavraDaFormula (restrictVar 0 b p)) ∧
      leafTravel b (original p) k ≤ 13*(original p).length+8+2*budget (original p).length := by
  let q := restrictVar 0 b p
  obtain ⟨i,_,moves,terminated⟩ := ResidualTape.restrict_on_tape b p
  obtain ⟨j,r,v,_,compiled,_,solved,work⟩ := CompilaHornNaFita.flat_horn_stages q horn
  let k : Clocks := ⟨i,j,r,v⟩
  have z : cutEnd b (original p) k = ⟨.halt,[],(original q).reverse⟩ := terminated
  have enter : compileStart b (original p) k = CompilaHornNaFita.ready (original q) [] none := by
    rw [compileStart,z,rewind_trace]; simp
  have leave : compileEnd b (original p) k =
      CompilaHornNaFita.run j (CompilaHornNaFita.ready (original q) [] none) := by
    rw [compileEnd,enter]
  have endMove : CompilaHornNaFita.travel k.compile (compileStart b (original p) k) +
       SparseHornTape.travel (k.back+k.solve) (checkerStart b (original p) k) ≤
       2*(4*(original q).length+3+budget (original q).length) := by
    rw [enter,checkerStart,leave]; exact work
  have started : ResidualTape.travel b k.cut (cutStart (original p)) ≤ 4*(original p).length+2 := moves
  have dist : (rewind (cutEnd b (original p) k).output []).2 = (original q).length := by
    rw [z,rewind_trace]; simp
  have small : (original q).length ≤ (original p).length := SharedBranch.restrict_size 0 b p
  have monotone := PolinomioPorEscolha.budget_le _ _ small
  refine ⟨k, ⟨by rw [z], by rw [z], ?_, ?_⟩, ?_⟩
  · rw [leave]; exact compiled
  · rw [checkerEnd,checkerStart,leave]; exact solved
  · unfold leafTravel
    rw [dist]
    omega

/-- Physical trace composition with one shared read-only input and disjoint,
initially blank work tapes for the two branches. Both Boolean answers are
held in finite control. All transfers between phases operate at the same
boundary or rewind one cell at a time. The bound counts head displacements
on these tapes and includes the return of the original input head. -/
theorem fixed_zero_two_horn (p : CNF (n+1))
    (horn : ∀ b, CompilaHornNaFita.IsHorn (restrictVar 0 b p)) :
    let raw := original p
    ∃ k₀ k₁ a₀ a₁,
      finished false raw k₀ a₀ ∧
      sharedReturn raw k₀ = (raw,raw.length) ∧
      finished true (sharedReturn raw k₀).1 k₁ a₁ ∧
      (a₀ || a₁) = palavraDaFormula p ∧
      leafTravel false raw k₀ + (sharedReturn raw k₀).2 + leafTravel true (sharedReturn raw k₀).1 k₁
        ≤ 27*raw.length+16+4*budget raw.length := by
  dsimp only
  obtain ⟨a,h₀,m₀⟩ := complete_leaf false p (horn false)
  obtain ⟨b,h₁,m₁⟩ := complete_leaf true p (horn true)
  have restore := shared_return (original p) a h₀.2.1
  refine ⟨a,b,_,_,h₀,restore,?_,(SharedBranch.word_split 0 p).symm,?_⟩
  · rw [restore]; exact h₁
  · rw [restore]; dsimp only; omega

end Codex.BranchCircuit
