import TGLExt.FatoresIndependentes
import TGLExt.LeitorDaFamilia

/-! A read-only one-head machine for the pair-probe promise. It remembers the
most recent literal result, and resets its three-way address class at every
sign and separator. Membership in the promise is a hypothesis. -/
set_option autoImplicit false
namespace Codex.PairTape
open TGLExt.TraducaoTuring IALD.LeitorDaFormula
open Codex.PolinomioPorEscolha Codex.ExplicitCache Codex.BranchPresence
open Codex.IndependentFactors
open Codex.FamilyHead (Addr bump classOf)

def decoded : Addr → Bool → Bool × Bool
  | .zero,s => (!s,s)
  | .one,s => (s,!s)
  | .large,_ => (true,true)

structure Reg where
  address : Addr
  bits : Bool × Bool

def start : Reg := ⟨.zero,(true,true)⟩
def see (s : Reg) : Letter → Reg
  | .tick => ⟨bump s.address,s.bits⟩
  | .sign b => ⟨.zero,decoded s.address b⟩
  | .delimiter => ⟨.zero,s.bits⟩
def read (w : List Letter) := (w.foldl see start).bits

inductive Machine where
  | walk (r : Reg) (unread : List Letter)
  | halt (out : Bool × Bool)

def step : Machine → Machine
  | .walk r (a::w) => .walk (see r a) w
  | .walk r [] => .halt r.bits
  | .halt out => .halt out

def moved : Machine → Nat
  | .walk _ (_::_) => 1
  | _ => 0
def travel : Nat → Machine → Nat
  | 0,_ => 0
  | k+1,s => moved s + travel k (step s)

theorem one_head (w : List Letter) (r : Reg) :
    step^[w.length+1] (.walk r w) = .halt (w.foldl see r).bits ∧
    travel (w.length+1) (.walk r w) = w.length := by
  induction w generalizing r with
  | nil => exact ⟨rfl,rfl⟩
  | cons a w ih =>
    obtain ⟨halted,moves⟩ := ih (see r a)
    constructor
    · change step^[w.length+1+1] _ = _
      rw [Function.iterate_succ_apply]
      exact halted
    · change 1 + travel (w.length+1) (.walk (see r a) w) = w.length+1
      omega

private theorem ticks (j : Nat) (out : Bool × Bool) :
    (List.replicate j Letter.tick).foldl see ⟨.zero,out⟩ = ⟨classOf j,out⟩ := by
  induction j with
  | zero => rfl
  | succ j ih =>
    rw [List.replicate_succ',List.foldl_append,ih]
    cases j with | zero => rfl | succ j => cases j <;> rfl

private theorem zero_at_boundary {n : Nat} (p : CNF n) (r : Reg) (z : r.address=.zero) :
    ((original p).foldl see r).address = .zero := by
  induction p generalizing r with
  | nil => exact z
  | cons c p ih =>
    change ((spellClause c ++ original p).foldl see r).address = _
    rw [List.foldl_append]
    apply ih
    simp [spellClause,List.foldl_append,see]

private theorem unit_reads {n : Nat} (l : Literal n) (r : Reg) (z : r.address=.zero) :
    ((spellClause [l]).foldl see r).bits = decoded (classOf l.var.val) l.pos := by
  obtain ⟨a,bits⟩ := r
  change a=.zero at z
  subst a
  simp [spellClause,spell,List.foldl_append,ticks,see]

theorem last_unit {n : Nat} (p : CNF n) (l : Literal n) :
    read (original (p++[[l]])) = decoded (classOf l.var.val) l.pos := by
  have split : original (p++[[l]]) = original p ++ spellClause [l] := by simp [original]
  unfold read
  rw [split,List.foldl_append]
  exact unit_reads l _ (zero_at_boundary p start rfl)

def program {k : Nat} (i : Fin (k+1)) (b : Bool) := pairs (k+1) true ++ continuation i b

private theorem pair_address {k : Nat} (i : Fin (k+1)) (b v : Bool) :
    (if v then (decoded (classOf (addr i b).val) true).2
          else (decoded (classOf (addr i b).val) true).1) =
      pairBit i b 0 false v := by
  by_cases eq : i=0
  · subst i
    have oneMod : 1 % (2*(k+1)) = 1 := Nat.mod_eq_of_lt (by omega)
    cases b <;> cases v <;> simp [addr,classOf,pairBit,decoded,oneMod]
  · have positive : 0 < i.val := by
      apply Nat.pos_of_ne_zero
      intro z
      exact eq (Fin.ext z)
    have large : 2 ≤ (addr i b).val := by
      cases b <;> simp [addr] <;> omega
    have cls : classOf (addr i b).val = .large := by
      cases e : (addr i b).val with
      | zero => omega
      | succ j => cases j with | zero => omega | succ j => rfl
    simp [cls,decoded,pairBit,Ne.symm eq]

theorem pair_bits {k : Nat} (i : Fin (k+1)) (b v : Bool) :
    let out := read (original (program i b))
    (if v then out.2 else out.1) = pairBit i b 0 false v := by
  have split : program i b = (pairs (k+1) true ++ pairs (k+1) false) ++ [[label i b true]] := by
    simp [program,continuation]
  dsimp only
  rw [split,last_unit]
  exact pair_address i b v

/-- The public theorem takes the raw input; the equation states its promise
and is used in the proof, never to skip reading any part of the input. -/
theorem pair_on_tape {k : Nat} (w : List Letter) (i : Fin (k+1)) (b : Bool)
    (promise : w = original (program i b)) :
    step^[w.length+1] (.walk start w) = .halt (read w) ∧
    travel (w.length+1) (.walk start w) = w.length ∧
    ∀ v : Bool, (if v then (read w).2 else (read w).1) = true ↔
      Compatible (program i b) [⟨addr (0 : Fin (k+1)) false,v⟩] := by
  obtain ⟨stop,moves⟩ := one_head w start
  refine ⟨stop,moves,?_⟩
  intro v
  rw [promise,pair_bits i b v]
  exact exact_pair_query i b 0 false v

theorem pivot_is_zero (k : Nat) : (addr (0 : Fin (k+1)) false).val = 0 := by simp [addr]

end Codex.PairTape
