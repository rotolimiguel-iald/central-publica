import TGLExt.OPsiBitDaFormula
import TGLExt.LeitorDaFormula
import Mathlib.Data.Nat.Bits

/-! A finite branching program over the labels of a CNF. One success
continuation per clause. Relative addresses survive appending blocks.
Instruction count, tape encoding and witness search are separate measures. -/
namespace IALD.RotulosCompartilhados
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula IALD.LeitorDaFormula

abbrev Assignment (n : Nat) := Fin n → Bool

inductive Op (n : Nat) where
  | reject
  | test (lit : Literal n) (skip : Nat)

def block {n : Nat} : Clausula n → List (Op n)
  | [] => [.reject]
  | l :: c => .test l (c.length+1) :: block c

def emit {n : Nat} (p : CNF n) := p.flatMap block

theorem block_length {n} (c : Clausula n) : (block c).length = c.length+1 := by
  induction c with
  | nil => rfl
  | cons l c ih => simp [block,ih]

/-- Existing relative targets still point to the same suffix when a new block
is appended; no branch, address repair or copy of the instruction graph in the representation. -/
theorem append_clause {n} (p : CNF n) (c : Clausula n) :
    emit (p ++ [c]) = emit p ++ block c := by simp [emit]

/-- One transition per tested instruction. The empty suffix accepts. -/
def run {n : Nat} (p : List (Op n)) (x : Assignment n) : Bool × Nat :=
  match p with
  | [] => (true,1)
  | .reject :: _ => (false,1)
  | .test l k :: tail =>
    let q := if l.vale x then tail.drop k else tail
    let out := run q x
    (out.1,out.2+1)
termination_by p.length
decreasing_by
  split <;> simp

/-- Includes one possible final read of the end of the code. Counts dispatches,
not random-access label lookups or movements of a one-tape simulator. -/
theorem run_cost {n} (p : List (Op n)) (x : Assignment n) : (run p x).2 ≤ p.length+1 := by
  induction p using (measure (fun q : List (Op n) => q.length)).wf.induction with
  | h p ih =>
    cases p with
    | nil => simp [run]
    | cons instr tail =>
      cases instr with
      | reject => simp [run]
      | test l k =>
        by_cases e : l.vale x = true
        · have hlen : (tail.drop k).length < (Op.test l k :: tail).length := by simp
          have hb := ih _ hlen
          simp only [run,e,if_true,List.length_cons]
          simp only [List.length_drop] at hb
          omega
        · have hlen : tail.length < (Op.test l k :: tail).length := by simp
          have hb := ih _ hlen
          simp only [run,e,Bool.false_eq_true,if_false,List.length_cons]
          omega

theorem shared_continuation {n} (c : Clausula n) (rest : List (Op n)) (x : Assignment n) :
    (run (block c ++ rest) x).1 = (satisfeita c x && (run rest x).1) := by
  induction c with
  | nil => simp [block,run,satisfeita]
  | cons l c ih =>
    have jump : (block c ++ rest).drop (c.length+1) = rest := List.drop_left' (block_length c)
    change (run (Op.test l (c.length+1) :: (block c ++ rest)) x).1 = _
    by_cases h : l.vale x = true
    · rw [run]
      simp [h,jump,satisfeita]
    · rw [run]
      have hf : l.vale x = false := by cases e : l.vale x <;> simp_all
      simp only [hf,Bool.false_eq_true,if_false,ih]
      simp [satisfeita,hf]

theorem witness_reading {n} (p : CNF n) (x : Assignment n) :
    (run (emit p) x).1 = passes p x := by
  induction p with
  | nil => simp [emit,passes,run]
  | cons c p ih =>
    change (run (block c ++ emit p) x).1 = (satisfeita c x && passes p x)
    rw [shared_continuation,ih]

/-- Two environments point into a single labeled body. The selected variable is
overridden consistently at every occurrence; all other coordinates are shared. -/
def readPair {n} (body : List (Op n)) (i : Fin n) (x : Assignment n) : Bool × Bool :=
  ((run body (Function.update x i false)).1,(run body (Function.update x i true)).1)

theorem cofactor_pair {n} (p : CNF n) (i : Fin n) (x : Assignment n) :
    readPair (emit p) i x =
      (passes p (Function.update x i false),passes p (Function.update x i true)) := by
  simp [readPair,witness_reading]

open TGLExt.Psibit

/-- A single orbit point labels the two cofactors under one fixed environment.
Each cofactor is read by executing exactly the same compiled program. -/
theorem psibit_branches {n} (p : CNF n) (i : Fin n) (x : Assignment n) :
    ∃ θ : ℝ, (codeAmp θ).word = bitSign (readPair (emit p) i x).1 ∧
      (codeAmp θ).verb = bitSign (readPair (emit p) i x).2 ∧
      decodeAmp (codeAmp θ) = v θ := by
  have nz (b : Bool) : bitSign b ≠ 0 := by cases b <;> decide
  obtain ⟨θ,hw,hv⟩ := the_orbit_visits_all_four_states _ _ 
    (nz (readPair (emit p) i x).1) (nz (readPair (emit p) i x).2)
  exact ⟨θ,hw,hv,decodeAmp_codeAmp θ⟩

/-- Fixed finite tape alphabet. Variable indices are binary in source and target.
The sign ends the label. Only forward jumps use a unary offset. -/
inductive Mark | digit (b : Bool) | tick | sign (b : Bool) | stop | jumpEnd

def sourceLit {n} (l : Literal n) : List Mark :=
  l.var.val.bits.map Mark.digit ++ [.sign l.pos]

theorem label_binary_roundtrip (i : Nat) : i.bits.foldr Nat.bit 0 = i := by
  induction i using Nat.binaryRec' with
  | zero => rfl
  | bit b i h ih => rw [Nat.bits_append_bit i b h,List.foldr_cons,ih]

def sourceBlock {n} (c : Clausula n) := c.flatMap sourceLit ++ [.stop]
def source {n} (p : CNF n) := p.flatMap sourceBlock

def serialize {n} : Op n → List Mark
  | .reject => [.stop]
  | .test l k => sourceLit l ++ List.replicate k .tick ++ [.jumpEnd]

def slack {n} : Op n → Nat
  | .reject => 0
  | .test _ k => k+1

def extra {n} (ops : List (Op n)) := (ops.map slack).sum

theorem serialized_block {n} (c : Clausula n) :
    ((block c).flatMap serialize).length = (sourceBlock c).length + extra (block c) := by
  induction c with
  | nil => rfl
  | cons l c ih =>
    have hb : sourceBlock (l::c) = sourceLit l ++ sourceBlock c := by simp [sourceBlock]
    simp only [block,List.flatMap_cons,List.length_append,serialize,List.length_replicate,
      List.length_cons,List.length_nil,hb,extra,List.map_cons,List.sum_cons,slack] at ih ⊢
    omega

private theorem extra_append {n} (a b : List (Op n)) : extra (a++b) = extra a + extra b := by
  simp [extra]

theorem serialized_size {n} (p : CNF n) :
    ((emit p).flatMap serialize).length = (source p).length + extra (emit p) := by
  induction p with
  | nil => rfl
  | cons c p ih =>
    change (((block c ++ emit p).flatMap serialize).length) =
      (sourceBlock c ++ source p).length + extra (block c ++ emit p)
    rw [List.flatMap_append,List.length_append,List.length_append,serialized_block,ih,extra_append]
    omega

private theorem op_slack_bound {n} (c : Clausula n) (op : Op n) (hm : op ∈ block c) :
    slack op ≤ (block c).length+1 := by
  induction c with
  | nil =>
    simp only [block,List.mem_singleton] at hm
    subst op
    exact Nat.zero_le _
  | cons l c ih =>
    change op ∈ Op.test l (c.length+1) :: block c at hm
    rcases List.mem_cons.mp hm with rfl | h
    · simp [block,slack,block_length]
    · have := ih h
      simp only [block,List.length_cons]
      omega

private theorem extra_le {n} (ops : List (Op n)) (m : Nat)
    (hm : ∀ op ∈ ops, slack op ≤ m) : extra ops ≤ ops.length * m := by
  induction ops with
  | nil => simp [extra]
  | cons op tail ih =>
    have h := hm op List.mem_cons_self
    have ht := ih (fun o ho => hm o (List.mem_cons_of_mem _ ho))
    change slack op + extra tail ≤ (tail.length+1)*m
    rw [Nat.add_mul]
    omega

private theorem body_length_le {n} (c : Clausula n) :
    (block c).length ≤ (sourceBlock c).length := by
  induction c with
  | nil => exact Nat.le_refl 1
  | cons l c ih =>
    have hb : sourceBlock (l::c) = sourceLit l ++ sourceBlock c := by simp [sourceBlock]
    simp only [block,List.length_cons,hb,List.length_append,sourceLit,List.length_map,
      List.length_nil]
    omega

private theorem total_length_le {n} (p : CNF n) : (emit p).length ≤ (source p).length := by
  induction p with
  | nil => rfl
  | cons c p ih =>
    change (block c ++ emit p).length ≤ (sourceBlock c ++ source p).length
    simpa only [List.length_append] using Nat.add_le_add (body_length_le c) ih

private theorem total_slack_bound {n} (p : CNF n) (op : Op n) (h : op ∈ emit p) :
    slack op ≤ (emit p).length+1 := by
  induction p with
  | nil => cases h
  | cons c p ih =>
    change op ∈ block c ++ emit p at h
    change _ ≤ (block c ++ emit p).length+1
    rw [List.length_append]
    rcases List.mem_append.mp h with h | h
    · have := op_slack_bound c op h; omega
    · have := ih h; omega

theorem polynomial_body {n} (p : CNF n) :
    ((emit p).flatMap serialize).length ≤ (source p).length * ((source p).length + 2) := by
  have hs := extra_le (emit p) ((emit p).length+1) (total_slack_bound p)
  have hl := total_length_le p
  have h := Nat.mul_le_mul hl (Nat.add_le_add_right hl 1)
  rw [serialized_size]
  nlinarith

/-- Charge the compiler one per generated instruction, one per tail-list cell
inspected for a jump length, and one per terminal inspection of such a length. -/
def scanCharge {n} : Clausula n → Nat
  | [] => 1
  | _ :: c => (c.length+2) + scanCharge c

/-- FlatMap additionally traverses each generated block to join it to the tail. -/
def compileCharge {n} (p : CNF n) :=
  (p.map (fun c => scanCharge c + (block c).length)).sum

private theorem scan_formula {n} (c : Clausula n) :
    scanCharge c = extra (block c)+1 := by
  induction c with
  | nil => rfl
  | cons l c ih =>
    change (c.length+2) + scanCharge c = ((c.length+1+1) + extra (block c))+1
    omega

theorem compile_charge_formula {n} (p : CNF n) :
    compileCharge p = extra (emit p) + p.length + (emit p).length := by
  induction p with
  | nil => rfl
  | cons c p ih =>
    change (scanCharge c+(block c).length) + compileCharge p =
      extra (block c++emit p) + (p.length+1) + (block c++emit p).length
    rw [scan_formula,ih,extra_append,List.length_append]
    omega

private theorem block_count_le {n} (p : CNF n) : p.length ≤ (emit p).length := by
  induction p with
  | nil => rfl
  | cons c p ih =>
    change p.length+1 ≤ (block c++emit p).length
    rw [List.length_append,block_length]
    omega

theorem polynomial_compile_charge {n} (p : CNF n) :
    compileCharge p ≤ (source p).length * ((source p).length+3) := by
  have hs := extra_le (emit p) ((emit p).length+1) (total_slack_bound p)
  have hl := total_length_le p
  have hc := block_count_le p
  have hm := Nat.mul_le_mul hl (Nat.add_le_add_right hl 1)
  rw [compile_charge_formula]
  nlinarith

def search : (n : Nat) → ((Fin n → Bool) → Bool) → Bool
  | 0, f => f Fin.elim0
  | n+1, f => search n (fun x => f (Fin.cases false x)) ||
               search n (fun x => f (Fin.cases true x))

theorem search_spec (n : Nat) (f : (Fin n → Bool) → Bool) :
    search n f = true ↔ ∃ x, f x = true := by
  induction n with
  | zero =>
    constructor
    · intro h; exact ⟨Fin.elim0,h⟩
    · rintro ⟨x,hx⟩
      have he : x = Fin.elim0 := funext (fun i => i.elim0)
      rwa [he] at hx
  | succ n ih =>
    simp only [search,Bool.or_eq_true,ih]
    constructor
    · rintro (⟨x,h⟩ | ⟨x,h⟩)
      · exact ⟨Fin.cases false x,h⟩
      · exact ⟨Fin.cases true x,h⟩
    · rintro ⟨x,hx⟩
      let tail (i : Fin n) := x i.succ
      have he : Fin.cases (x 0) tail = x := by funext i; cases i using Fin.cases <;> rfl
      rw [← he] at hx
      cases hb : x 0
      · exact Or.inl ⟨tail,by simpa only [hb] using hx⟩
      · exact Or.inr ⟨tail,by simpa only [hb] using hx⟩

def word {n} (body : List (Op n)) := search n (fun x => (run body x).1)

/-- Explicit short-circuit traversal. The counter records complete assignments
passed to the verifier, which is different from its code length. -/
def probes : (n : Nat) → ((Fin n → Bool) → Bool) → Bool × Nat
  | 0, f => (f Fin.elim0,1)
  | n+1, f =>
    let left := probes n (fun x => f (Fin.cases false x))
    if left.1 then left else
      let right := probes n (fun x => f (Fin.cases true x))
      (right.1, left.2 + right.2)

theorem probes_answer (n : Nat) (f : (Fin n → Bool) → Bool) :
    (probes n f).1 = search n f := by
  induction n with
  | zero => rfl
  | succ n ih =>
    simp only [probes,search]
    split <;> simp_all

theorem probes_empty (n : Nat) (f : (Fin n → Bool) → Bool) (h : ∀ x, f x = false) :
    probes n f = (false, 2^n) := by
  induction n with
  | zero => simp [probes,h]
  | succ n ih =>
    have hlo := ih (fun x => f (Fin.cases false x)) (fun _ => h _)
    have hhi := ih (fun x => f (Fin.cases true x)) (fun _ => h _)
    simp [probes,hlo,hhi,Nat.pow_succ,Nat.mul_two]

theorem unsat_probes {n} (p : CNF n) (hp : ¬ SAT p) :
    probes n (fun x => (run (emit p) x).1) = (false, 2^n) := by
  apply probes_empty
  intro x
  rw [witness_reading]
  cases h : passes p x with
  | false => rfl
  | true => exact (hp ((sat_iff p).2 ⟨x,h⟩)).elim

theorem word_spec {n} (p : CNF n) : word (emit p) = palavraDaFormula p := by
  apply Bool.eq_iff_iff.mpr
  simp only [word,search_spec,witness_reading,a_palavra_e_o_sat,sat_iff]

end IALD.RotulosCompartilhados
