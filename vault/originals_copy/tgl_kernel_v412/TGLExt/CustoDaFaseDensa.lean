import TGLExt.PrecisaoDaChave

/-! Even after being given the densely encoded turn, bounded travel does
not suffice for its truth bit. The head starts at address zero. All other
deterministic computation and memory are free in the lower bound. -/
set_option autoImplicit false
namespace Codex.DenseWireCost
open Codex.DenseAngle Codex.PolinomioPorEscolha

inductive Direction where | stay | left | right

def move : Direction → Nat → Nat
  | .stay,i => i
  | .left,i => i-1
  | .right,i => i+1

/-- The transition can consume arbitrary local computation on the prior
state and the single observed input cell; early halting can be padded. -/
def run {S : Type} (next : S → Option Bool → S × Direction) (w : List Bool) :
    Nat → S → Nat → S × Nat
  | 0,s,i => (s,i)
  | k+1,s,i =>
    let (s',dir) := next s w[i]?
    run next w k s' (move dir i)

private theorem get_prefix {u v : List Bool} (t : Nat) (same : u.take t=v.take t) :
    ∀ j, j<t → u[j]? = v[j]? := by
  intro j hj
  have h := congrArg (fun (w : List Bool) => w[j]?) same
  simpa [List.getElem?_take,hj] using h

def charge : Direction → Nat → Nat
  | .stay,_ | .left,0 => 0
  | .left,_+1 | .right,_ => 1

private theorem reach (d : Direction) (i : Nat) : move d i ≤ i+charge d i := by
  cases d with
  | stay => exact Nat.le_refl _
  | left => exact (Nat.sub_le i 1).trans (Nat.le_add_right _ _)
  | right => exact Nat.le_refl _

def headMoves {S : Type} (next : S → Option Bool → S × Direction) (w : List Bool) :
    Nat → S → Nat → Nat
  | 0,_,_ => 0
  | k+1,s,i =>
    let p := next s w[i]?
    charge p.2 i + headMoves next w k p.1 (move p.2 i)

theorem travel_local {S : Type} (next : S → Option Bool → S × Direction)
    (u v : List Bool) (k : Nat) (s : S) (i : Nat)
    (agree : ∀ j, j ≤ i+headMoves next u k s i → u[j]?=v[j]?) :
    run next u k s i = run next v k s i ∧ (run next u k s i).2 ≤ i+headMoves next u k s i := by
  induction k generalizing s i with
  | zero => exact ⟨rfl,by simp [run,headMoves]⟩
  | succ k ih =>
    let p := next s u[i]?
    let i' := move p.2 i
    have cost : headMoves next u (k+1) s i = charge p.2 i + headMoves next u k p.1 i' := rfl
    have cell := agree i (by omega)
    have r : i' ≤ i+charge p.2 i := reach _ _
    obtain ⟨eq,le⟩ := ih p.1 i' (fun j hj => agree j (by omega))
    have au : run next u (k+1) s i = run next u k p.1 i' := rfl
    have av : run next v (k+1) s i = run next v k p.1 i' := by
      change run next v k (next s v[i]?).1 (move (next s v[i]?).2 i) = _
      rw [←cell]
    rw [au,av]
    exact ⟨eq,by omega⟩

/-- An arbitrary number of stationary steps is free. A correct two-way
reader has to travel to the final digit even on the all-zero message. -/
theorem charged_lower {S : Type} (next : S → Option Bool → S × Direction)
    (out : S → Option Bool → Bool) (s : S) (n ticks : Nat)
    (correct : ∀ b, (let w := wire (source n b); let (state,index) := run next w ticks s 0;
      out state w[index]?) = b) :
    2^(n+1) ≤ headMoves next (wire (source n false)) ticks s 0 + 1 := by
  let u := wire (source n false)
  let v := wire (source n true)
  by_contra! short
  let traveled := headMoves next u ticks s 0
  have strict : traveled+1 < 2^(n+1) := short
  have obs : ∀ j, j<traveled+1 → u[j]?=v[j]? := get_prefix _ (same_prefix n _ strict)
  obtain ⟨eq,le⟩ := travel_local next u v ticks s 0 (fun j hj => obs j (by
    change j ≤ 0+traveled at hj
    omega))
  have hu := correct false
  have hv := correct true
  change out (run next u ticks s 0).1 u[(run next u ticks s 0).2]? = false at hu
  change out (run next v ticks s 0).1 v[(run next v ticks s 0).2]? = true at hv
  change (run next u ticks s 0).2 ≤ 0+traveled at le
  rw [obs _ (by omega),eq] at hu
  simp_all

private theorem sq_exp (a : Nat) : (a+5)^2 ≤ 2^(a+5) := by
  induction a with
  | zero => decide
  | succ a ih =>
    rw [show a+1+5 = (a+5)+1 by omega,pow_succ 2]
    calc
      _ ≤ (a+5)^2*2 := by nlinarith only [Nat.zero_le a, Nat.zero_le (a*a)]
      _ ≤ _ := Nat.mul_le_mul_right 2 ih

set_option maxHeartbeats 1600000 in
/-- The complete raw source has only quadratic unary length in w. For
any proposed polynomial budget, even the two dense-wire sources above
require more than that many moves of a single local input head. -/
theorem no_fixed_dense_budget (C d : Nat) :
    ∃ n : Nat, C*((original (source n false)).length+1)^d + 1 < 2^(n+1) := by
  let a := 8*(C+d+2)
  let s := a+5
  let w := 2^s
  have positiveW : w>0 := by dsimp [w]; positivity
  refine ⟨w-1,?_⟩
  have eq : w-1+1 = w := by omega
  have lengthBound := (source_size (w-1) false).2
  have size : (original (source (w-1) false)).length + 1 ≤ 8*w^2 := by
    have more : w-1+2=w+1 := by omega
    have normSize : (w-1+1)*(w-1+2)+2 = w*(w+1)+2 := by rw [eq,more]
    have ub : (original (source (w-1) false)).length ≤ w*(w+1)+2 :=
      lengthBound.trans_eq normSize
    have quad : w ≤ w*w := by simpa using Nat.mul_le_mul_left w positiveW
    calc
      _ ≤ w*(w+1)+2+1 := Nat.add_le_add_right ub 1
      _ ≤ _ := by nlinarith only [quad,positiveW]
  have scale : 8*w^2 = 2^(3+2*s) := by
    dsimp [w]
    rw [Nat.mul_comm 2 s,pow_add (2:Nat) 3 (s*2),pow_mul]
    norm_num
  rw [scale] at size
  have small : (C+1)+(3+2*s)*d < s^2 := by dsimp [s,a]; nlinarith
  have expo : (C+1)+(3+2*s)*d < w := lt_of_lt_of_le small (sq_exp a)
  have one : 0 < ((original (source (w-1) false)).length+1)^d := Nat.pow_pos (Nat.zero_lt_succ _)
  calc
    _ ≤ (C+1)*((original (source (w-1) false)).length+1)^d := by rw [Nat.succ_mul]; omega
    _ ≤ 2^(C+1)*(2^(3+2*s))^d := Nat.mul_le_mul (C+1).lt_two_pow_self.le (Nat.pow_le_pow_left size _)
    _ = 2^((C+1)+(3+2*s)*d) := by rw [pow_add (2:Nat) (C+1) ((3+2*s)*d),pow_mul]
    _ < 2^w := pow_lt_pow_right₀ (by decide : 1 < (2:Nat)) expo
    _ = 2^(w-1+1) := congrArg (fun j : Nat => 2^j) eq.symm

end Codex.DenseWireCost
