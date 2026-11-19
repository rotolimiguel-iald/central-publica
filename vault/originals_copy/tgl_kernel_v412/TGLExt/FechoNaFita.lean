import TGLExt.FitaHornEsparsa
import Mathlib.Data.Nat.Dist

set_option autoImplicit false
namespace Codex.SparseHornTape
open Codex.HornCross TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula

variable {n : Nat}
theorem changed_iff (r : Rule n) (s : Mem n) :
    changeBit r s = decide (stepRule s r ≠ s) := by
  cases r with
  | mk xs h =>
    cases h with
    | none => simp [changeBit, stepRule]
    | some i =>
      by_cases ha : active s (Rule.mk xs (some i)) = true <;> by_cases hi : i ∈ s <;>
        simp [changeBit,stepRule,ha,hi,Finset.insert_eq_self]

theorem fail_when_stable (r : Rule n) (s : Mem n) (hs : stepRule s r = s) :
    failure r s = !ok s r := by
  cases r with
  | mk xs h =>
    cases h with
    | none => simp [failure,ok,hit]
    | some i =>
      by_cases ha : active s (Rule.mk xs (some i)) = true
      · have hi : i ∈ s := by
          have h : i ∈ stepRule s (Rule.mk xs (some i)) := by simp [stepRule,ha]
          rwa [hs] at h
        simp [failure,ok,hit,ha,hi]
      · simp [failure,ok,ha]

theorem trace_mem (p : List (Rule n)) (s : Mem n) (h b : Bool) :
    (traceResult p s h b).1 = sweep p s := by
  induction p generalizing s h b with
  | nil => rfl
  | cons r p ih => exact ih _ _ _

theorem trace_changed (p : List (Rule n)) (s : Mem n) (h b : Bool) :
    (traceResult p s h b).2.1 = (h || decide (sweep p s ≠ s)) := by
  induction p generalizing s h b with
  | nil => simp [traceResult,sweep]
  | cons r p ih =>
    simp only [traceResult,ih,changed_iff]
    change _ = (h || decide (sweep p (stepRule s r) ≠ s))
    by_cases hr : stepRule s r = s
    · simp [hr]
    · have hne : sweep p (stepRule s r) ≠ s := by
        intro hh
        have hs := sweep_extends p (stepRule s r)
        rw [hh] at hs
        exact hr (Finset.Subset.antisymm hs (step_extends _ _))
      simp [hr,hne]

theorem trace_bad_fixed (p : List (Rule n)) (s : Mem n) (h b : Bool) (hs : sweep p s = s) :
    (traceResult p s h b).2.2 = (b || !valid p s) := by
  induction p generalizing h b with
  | nil => simp [traceResult,valid]
  | cons r p ih =>
    have hr := each_stable (r::p) s hs r List.mem_cons_self
    change sweep p (stepRule s r) = s at hs
    rw [hr] at hs
    simp only [traceResult, hr, ih _ _ hs, fail_when_stable _ _ hr, valid,List.all_cons]
    cases b <;> cases ok s r <;> cases p.all (ok s) <;> rfl

theorem pass_length (p : List (Rule n)) : costPass p ≤ 2*(program p).length := by
  have line_bound (r : Rule n) : costLine r ≤ 2*(line r).length := by
    cases r with
    | mk xs h => cases h <;> simp [costLine,line,Nat.mul_add]
  induction p with
  | nil => simp [costPass,program]
  | cons r p ih =>
    have h := line_bound r
    change costLine r + costPass p ≤ 2*(line r ++ program p).length
    rw [List.length_append,Nat.mul_add]
    exact Nat.add_le_add h ih

theorem clauses_length (p : List (Rule n)) : p.length ≤ (program p).length := by
  have one (r : Rule n) : 1 ≤ (line r).length := by
    cases r with
    | mk xs h => cases h <;> simp [line,arg]; omega
  induction p with
  | nil => rfl
  | cons r p ih =>
    change p.length+1 ≤ (line r ++ program p).length
    rw [List.length_append]
    have := one r
    omega

theorem back_trace (l r : List Sym) (s : Finset Nat) (a h b : Bool) :
    run (l.length+1) ⟨.back,a,h,b,l,r,0,s⟩ = readCfg [] (l.reverse++r) s true false false := by
  induction l generalizing r with
  | nil => rfl
  | cons c l ih =>
    change run (l.length+1) ⟨.back,a,h,b,l,c::r,0,s⟩ = _
    simpa [List.reverse_cons,List.append_assoc] using ih (c::r)

def start (p : List (Rule n)) (s : Mem n) := readCfg [] (program p) (written s) true false false

theorem halts_from (p : List (Rule n)) (k : Nat) (s : Mem n) (hs : s ⊆ heads p)
    (hk : (heads p).card < s.card+k) :
    ∃ T ≤ k*(3*(program p).length+2),
      (run T (start p s)).mode = .halt (valid p (settle p k s)) := by
  induction k generalizing s with
  | zero => have := Finset.card_le_card hs; omega
  | succ k ih =>
    let z := traceResult p s false false
    have hp := pass_trace p [] [] s false false
    simp only [List.append_nil] at hp
    have hpass : run (costPass p) (start p s) = readCfg (program p).reverse [] (written z.1) true z.2.1 z.2.2 := hp
    have hc := trace_changed p s false false
    have hm := trace_mem p s false false
    have hlen := pass_length p
    by_cases he : sweep p s = s
    · have hb := trace_bad_fixed p s false false he
      refine ⟨costPass p+1,?_,?_⟩
      · rw [Nat.succ_mul]; omega
      · rw [run_add,hpass]
        simp [z,readCfg,run,step,hc,hb,he,settle]
    · have hu := sweep_within p s hs
      have hlt := Finset.card_lt_card (Finset.ssubset_iff_subset_ne.mpr ⟨sweep_extends p s,Ne.symm he⟩)
      obtain ⟨T,hT,halt⟩ := ih (sweep p s) hu (by omega)
      refine ⟨(costPass p+1+((program p).length+1))+T,?_,?_⟩
      · rw [Nat.succ_mul]; omega
      · rw [run_add _ T, run_add (costPass p+1) ((program p).length+1),
          run_add (costPass p) 1,hpass]
        have hh : z.2.1 = true := by simp [z,hc,he]
        change (run T (run ((program p).length+1)
          ⟨if z.2.1 then .back else .halt (!z.2.2),true,z.2.1,z.2.2,(program p).reverse,[],0,written z.1⟩)).mode = _
        have hback := back_trace (program p).reverse [] (written z.1) true true z.2.2
        simp only [List.length_reverse,List.reverse_reverse,List.append_nil] at hback
        rw [hh]
        change (run T (run ((program p).length+1)
          ⟨.back,true,true,z.2.2,(program p).reverse,[],0,written z.1⟩)).mode = _
        rw [hback]
        simpa only [z,hm,settle,if_neg he,start] using halt

/-- Physical movement of both heads between configurations, in unit cell boundaries crossed. -/
def moves (x y : Cfg) := Nat.dist x.left.length y.left.length + Nat.dist x.pos y.pos
def travel : Nat → Cfg → Nat
  | 0,_ => 0
  | k+1,c => moves c (step c) + travel k (step c)

theorem one_tick (c : Cfg) : moves c (step c) ≤ 2 := by
  rcases c with ⟨mode,a,h,b,l,r,i,t⟩
  cases mode with
  | halt _ => simp [moves,step]
  | home => cases i <;> simp [moves,step,Nat.dist]
  | back => cases l <;> simp [moves,step,Nat.dist]
  | scan =>
    cases r with
    | nil => simp [moves,step]
    | cons c r => cases c <;> simp [moves,step,Nat.dist]

theorem travel_bound (T : Nat) (c : Cfg) : travel T c ≤ 2*T := by
  induction T generalizing c with
  | zero => rfl
  | succ T ih =>
    have h := one_tick c
    have h' := ih (step c)
    simp only [travel,Nat.mul_succ]
    omega

theorem sparse_horn_tape (p : List (Rule n)) :
    let L := (program p).length
    ∃ T ≤ (L+1)*(3*L+2), travel T (start p ∅) ≤ 2*((L+1)*(3*L+2)) ∧
      (run T (start p ∅)).mode = .halt (palavraDaFormula (p.map asClause)) := by
  have h₁ := List.toFinset_card_le (p.filterMap Rule.head)
  have h₂ := List.length_filterMap_le Rule.head p
  obtain ⟨T,hT,ha⟩ := halts_from p (p.length+1) ∅ (by simp) (by simpa [heads] using Nat.lt_succ_of_le (h₁.trans h₂))
  have h := hT.trans (Nat.mul_le_mul_right _ (Nat.add_le_add_right (clauses_length p) 1))
  exact ⟨T,h,(travel_bound _ _).trans (Nat.mul_le_mul_left 2 h),ha.trans (congrArg Mode.halt (horn_word p))⟩

end Codex.SparseHornTape
