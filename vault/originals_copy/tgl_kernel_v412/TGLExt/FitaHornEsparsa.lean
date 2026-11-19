import TGLExt.ImplicacoesCruzadas

set_option autoImplicit false
namespace Codex.SparseHornTape
open Codex.HornCross TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula

inductive Sym where | tick | need | setBit | deny deriving DecidableEq
inductive Mode where | scan | home | back | halt (answer : Bool) deriving DecidableEq
/-- The two half tapes are the input zipper. 'pos' denotes the physical position of the
work head. The finite set is the tape support: the control can only read or set its current cell. -/
structure Cfg where
  mode : Mode
  fire : Bool
  changed : Bool
  bad : Bool
  left : List Sym
  right : List Sym
  pos : Nat
  tape : Finset Nat

def step (a : Cfg) : Cfg := match a.mode with
  | .halt _ => a
  | .home => if a.pos = 0 then {a with mode := .scan} else {a with pos := a.pos-1}
  | .back => match a.left with
    | [] => {a with mode := .scan, fire := true, changed := false, bad := false}
    | c :: l => {a with left := l, right := c::a.right}
  | .scan => match a.right with
    | [] => {a with mode := if a.changed then .back else .halt (!a.bad)}
    | c::r =>
      let b := {a with left := c::a.left,right := r}
      match c with
      | .tick => {b with pos := a.pos+1}
      | .need => {b with mode := .home, fire := a.fire && decide (a.pos ∈ a.tape)}
      | .setBit =>
        { b with
          mode := .home
          fire := true
          changed := a.changed || (a.fire && !decide (a.pos ∈ a.tape))
          tape := if a.fire then insert a.pos a.tape else a.tape }
      | .deny => {b with fire := true, bad := a.bad || a.fire}

def run : Nat → Cfg → Cfg
  | 0,c => c
  | k+1,c => run k (step c)
theorem run_add (m k : Nat) (c : Cfg) : run (m+k) c = run k (run m c) := by
  induction m generalizing c with
  | zero => simp [run]
  | succ m ih => rw [Nat.succ_add]; exact ih _

def readCfg (l r : List Sym) (s : Finset Nat) (a h b : Bool) :=
  Cfg.mk .scan a h b l r 0 s

private theorem home_trace (i : Nat) (l r : List Sym) (s : Finset Nat) (a h b : Bool) :
    run (i+1) ⟨.home,a,h,b,l,r,i,s⟩ = readCfg l r s a h b := by
  induction i with
  | zero => rfl
  | succ i ih => exact ih

private theorem ticks (i j : Nat) (l r : List Sym) (s : Finset Nat) (a h b : Bool) :
    run i ⟨.scan,a,h,b,l,List.replicate i .tick ++ r,j,s⟩ =
    ⟨.scan,a,h,b,List.replicate i .tick ++ l,r,j+i,s⟩ := by
  induction i generalizing j l with
  | zero => rfl
  | succ i ih =>
    change run i ⟨.scan,a,h,b,.tick::l,List.replicate i .tick ++ r,j+1,s⟩ = _
    rw [ih]
    rw [show j+1+i=j+(i+1) by omega]
    rw [List.replicate_succ']
    simp only [List.append_assoc,List.singleton_append]

variable {n : Nat}
def written (s : Mem n) : Finset Nat := s.image Fin.val
@[simp] theorem written_read (s : Mem n) (i : Fin n) : i.val ∈ written s ↔ i ∈ s := by
  simp [written,Fin.val_inj]
@[simp] theorem written_insert (s : Mem n) (i : Fin n) :
    written (insert i s) = insert i.val (written s) := by simp [written]
def arg (i : Fin n) (op : Sym) := List.replicate i.val .tick ++ [op]
def args (is : List (Fin n)) := is.flatMap (fun i => arg i .need)
def line (r : Rule n) := args r.body ++ r.head.elim [.deny] (fun i => arg i .setBit)
def program (p : List (Rule n)) := p.flatMap line

private theorem arg_need (i : Fin n) (l r : List Sym) (s : Mem n) (a h b : Bool) :
    run (2*(arg i .need).length) (readCfg l (arg i .need ++ r) (written s) a h b) =
    readCfg ((arg i .need).reverse++l) r (written s) (a && decide (i ∈ s)) h b := by
  have ht := ticks i.val 0 l (.need::r) (written s) a h b
  simp only [Nat.zero_add] at ht
  have he : 2*(arg i .need).length=i.val+((i.val+1)+1) := by simp [arg]; omega
  rw [he,run_add]
  simp only [arg,List.append_assoc,List.singleton_append,readCfg]
  rw [ht]
  change run (i.val+1) ⟨.home,_,_,_,_,_,_,_⟩ = _
  rw [home_trace]
  simp [readCfg,List.reverse_append]

private theorem arg_set (i : Fin n) (l r : List Sym) (s : Mem n) (a h b : Bool) :
    run (2*(arg i .setBit).length) (readCfg l (arg i .setBit ++ r) (written s) a h b) =
    readCfg ((arg i .setBit).reverse++l) r (written (if a then insert i s else s)) true
      (h || (a && !decide (i ∈ s))) b := by
  have ht := ticks i.val 0 l (.setBit::r) (written s) a h b
  simp only [Nat.zero_add] at ht
  have he : 2*(arg i .setBit).length=i.val+((i.val+1)+1) := by simp [arg]; omega
  rw [he,run_add]
  simp only [arg,List.append_assoc,List.singleton_append,readCfg]
  rw [ht]
  change run (i.val+1) ⟨.home,_,_,_,_,_,_,_⟩ = _
  rw [home_trace]
  cases a <;> simp [readCfg,List.reverse_append]

private theorem args_trace (is : List (Fin n)) (l r : List Sym) (s : Mem n) (a h b : Bool) :
    run (2*(args is).length) (readCfg l (args is++r) (written s) a h b) =
    readCfg ((args is).reverse++l) r (written s) (a && is.all (fun i => decide (i ∈ s))) h b := by
  induction is generalizing l a with
  | nil => simp [args,run]
  | cons i is ih =>
    simp only [show args (i :: is) = arg i .need ++ args is from rfl,
      List.length_append,Nat.mul_add,run_add,List.append_assoc]
    rw [arg_need,ih]
    simp [List.reverse_append,List.append_assoc,Bool.and_assoc]

def changeBit (r : Rule n) (s : Mem n) := active s r && r.head.elim false (fun i => !decide (i ∈ s))
def failure (r : Rule n) (s : Mem n) := active s r && r.head.isNone
def costLine (r : Rule n) := 2*(args r.body).length+r.head.elim 1 (fun i => 2*(arg i .setBit).length)
theorem line_trace (r : Rule n) (l tail : List Sym) (s : Mem n) (h b : Bool) :
    run (costLine r) (readCfg l (line r++tail) (written s) true h b) =
      readCfg ((line r).reverse++l) tail (written (stepRule s r)) true
        (h || changeBit r s) (b || failure r s) := by
  rw [costLine,run_add,line,List.append_assoc,args_trace]
  simp only [Bool.true_and]
  cases r with
  | mk is head =>
    cases head with
    | none => simp [Option.elim,run,step,readCfg,active,stepRule,changeBit,failure,List.reverse_append]
    | some i =>
      simp only [Option.elim_some]
      rw [arg_set]
      simp [active,stepRule,changeBit,failure,List.reverse_append,List.append_assoc]

def traceResult : List (Rule n) → Mem n → Bool → Bool → Mem n × Bool × Bool
  | [],s,h,b => (s,h,b)
  | r::p,s,h,b => traceResult p (stepRule s r) (h || changeBit r s) (b || failure r s)
def costPass (p : List (Rule n)) := (p.map costLine).sum

theorem pass_trace (p : List (Rule n)) (l tail : List Sym) (s : Mem n) (h b : Bool) :
    let z := traceResult p s h b
    run (costPass p) (readCfg l (program p++tail) (written s) true h b) =
      readCfg ((program p).reverse++l) tail (written z.1) true z.2.1 z.2.2 := by
  induction p generalizing l s h b with
  | nil => rfl
  | cons r p ih =>
    simp only [show costPass (r :: p) = costLine r + costPass p from rfl,
      show program (r :: p) = line r ++ program p from rfl,run_add,List.append_assoc]
    rw [line_trace,ih]
    simp [traceResult,List.reverse_append,List.append_assoc]

end Codex.SparseHornTape
