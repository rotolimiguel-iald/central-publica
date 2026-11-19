import TGLExt.MovimentosDoPlano

/-! Quantified failure of every fixed polynomial bound for this particular
two-branch traversal. The witness is an input on which complete traces exist. -/
set_option autoImplicit false
namespace Codex.ReaderBound
open Codex.IntegratedRead Codex.FormulaPlan Codex.SharedReader Codex.PolinomioPorEscolha

private theorem square_le_exp (a : Nat) : (a+4)^2 ≤ 2^(a+4) := by
  induction a with
  | zero => decide
  | succ a ih =>
    calc
      (a+1+4)^2 ≤ (a+1+4)^2+(a^2+6*a+7) := Nat.le_add_right _ _
      _ = 2*(a+4)^2 := by ring
      _ ≤ 2*2^(a+4) := Nat.mul_le_mul_left 2 ih
      _ = 2^(a+4)*2 := Nat.mul_comm _ _
      _ = 2^(a+1+4) := (pow_succ (2:Nat) (a+4)).symm

private theorem encoding_bound (k : Nat) (h : 1 ≤ k) :
    (original (coupled k)).length+1 ≤ 16*k^2 := by
  have sq : k ≤ k^2 := by
    simpa only [Nat.mul_one,pow_two] using (Nat.mul_le_mul_left k h)
  have raw := coupled_size k
  calc
    _ ≤ k*(5*k+4)+2 := by omega
    _ ≤ 16*k^2 := by nlinarith

private theorem coeff_pow (s : Nat) : 16*((2:Nat)^s)^2 = 2^(4+2*s) := by
  rw [Nat.mul_comm 2 s, pow_add (2:Nat) 4 (s*2), pow_mul (2:Nat) s 2]
  norm_num

set_option maxHeartbeats 700000 in
theorem exceeds_each_polynomial (C d : Nat) :
    ∃ m : Nat, ∃ t : Nat,
      Trace (pivots (coupled (m+1))) (coupled (m+1)) true t ∧
      ∀ (moves : Nat) (answer : Bool), Trace (pivots (coupled (m+1))) (coupled (m+1)) answer moves →
        C*((original (coupled (m+1))).length+1)^d < moves := by
  let a := 8*(C+d+1)
  let s := a+4
  let m := 2^s-1
  have pos : 0 < (2:Nat)^s := by positivity
  have size : m+1 = 2^s := by dsimp [m]; omega
  have letterBound : (original (coupled (m+1))).length+1 ≤ 2^(4+2*s) := by
    apply (encoding_bound (m+1) (Nat.succ_pos _)).trans
    rw [size, coeff_pow]
  have small : C+(4+2*s)*d < s^2 := by dsimp [s,a]; nlinarith
  have expo := lt_of_lt_of_le small (square_le_exp a)
  obtain ⟨t,_,trace⟩ := horn_moves_from_formula (coupled (m+1))
  rw [mixed_witness] at trace
  refine ⟨m,t,trace,?_⟩
  intro moves answer h
  calc
    C*((original (coupled (m+1))).length+1)^d ≤ 2^C*(2^(4+2*s))^d :=
      Nat.mul_le_mul C.lt_two_pow_self.le (Nat.pow_le_pow_left letterBound _)
    _ = 2^C*2^((4+2*s)*d) :=
      congrArg (fun z : Nat => 2^C*z) (pow_mul (2:Nat) (4+2*s) d).symm
    _ = 2^(C+(4+2*s)*d) := (pow_add (2:Nat) C ((4+2*s)*d)).symm
    _ < 2^(2^s) := pow_lt_pow_right₀ (by decide : 1 < (2:Nat)) expo
    _ = 2^(m+1) := by rw [size]
    _ ≤ moves := Codex.PlanTravel.coupled_physical_lower m h

end Codex.ReaderBound
