import TGLExt.PerfilDeSinais
import TGLExt.CircuitoNaFita

/-! Read-only input, one work tape, two sweeps. At a sign the input head has
advanced, so the delimiter test uses the symbol it is now on. A work head
moves right once per tick and returns to its left marker at each sign. -/
set_option autoImplicit false
namespace Codex.TwoSweeps
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula IALD.LeitorDaFormula
open Codex.PolinomioPorEscolha Codex.SignProfile

abbrev Bank := Nat → Cell
structure Op (Q : Type) where
  literal : Bool → Bool → Bool → Cell → Q → Cell × Q -- zero address, sign, unit
  boundary : Q → Q

structure St (Q : Type) where
  bank : Bank
  control : Q
  first : Bool
  head : Nat

/-- Each recursive call moves the work head exactly one cell left. -/
def home : Nat → Nat × Nat
  | 0 => (0,0)
  | k+1 => let r := home k; (r.1,r.2+1)
@[simp] theorem home_trace (j : Nat) : home j = (0,j) := by
  induction j with | zero => rfl | succ j ih => simp [home,ih]

def delimiterNext : List Letter → Bool
  | .delimiter :: _ => true
  | _ => false

def atSign {Q} (o : Op Q) (st : St Q) (s last : Bool) : St Q :=
  let v := o.literal (st.head == 0) s (st.first && last) (st.bank st.head) st.control
  ⟨Function.update st.bank st.head v.1,v.2,false,(home st.head).1⟩

def update {Q} (o : Op Q) (a : Letter) (next : List Letter) (st : St Q) : St Q :=
  match a with
  | .tick => {st with head := st.head+1}
  | .sign s => atSign o st s (delimiterNext next)
  | .delimiter => {st with first := true, control := o.boundary st.control}

/-- Input advances one on every letter. Ticks also advance the work head;
signs also rewind it. The length of the unread tail is never consulted. -/
def workMoves (j : Nat) : Letter → Nat
  | .tick => 1 | .sign _ => (home j).2 | .delimiter => 0

def scan {Q} (o : Op Q) : List Letter → St Q → St Q
  | [],st => st
  | a::w,st => scan o w (update o a w st)
def travel {Q} (o : Op Q) : List Letter → St Q → Nat
  | [],_ => 0
  | a::w,st => (1+workMoves st.head a) + travel o w (update o a w st)

/-- Bookkeeping of the past of the SAME read-only input head during scan.
The zipper is an observation. Returning to the left uses rewind, cell by cell. -/
def past : List Letter → List Letter → List Letter
  | [],left => left
  | a::w,left => past w (a::left)
theorem past_spec (w left : List Letter) : past w left = w.reverse ++ left := by
  induction w generalizing left with
  | nil => rfl
  | cons a w ih => simp [past,ih,List.append_assoc]
def returned (w : List Letter) := Codex.BranchCircuit.rewind (past w []) []
theorem returned_spec (w : List Letter) : returned w = (w,w.length) := by
  simp [returned,Codex.BranchCircuit.rewind_trace,past_spec]

theorem count_le {Q} (o : Op Q) (w : List Letter) (s : St Q) :
    travel o w s ≤ 3*w.length+s.head := by
  induction w generalizing s with
  | nil => simp [travel]
  | cons a w ih =>
    have h := ih (update o a w s)
    cases a <;> simp [travel,update,atSign,workMoves,Nat.mul_add] at h ⊢ <;> omega

/-- Macro at a literal boundary. Its index is used only to prove what raw scan
computes. The executable scanner reaches it using the ticks of the input. -/
def applyLit {Q n} (o : Op Q) (l : Literal n) (unit : Bool) (s : St Q) : St Q :=
  let r := o.literal (l.var.val == 0) l.pos unit (s.bank l.var.val) s.control
  ⟨Function.update s.bank l.var.val r.1,r.2,false,0⟩
def lits {Q n} (o : Op Q) : Clausula n → St Q → St Q
  | [],s => s
  | l::ls,s => lits o ls (applyLit o l (s.first && ls.isEmpty) s)
def finish {Q} (o : Op Q) (s : St Q) : St Q := {s with first:=true,control:=o.boundary s.control}
def clauses {Q n} (o : Op Q) : CNF n → St Q → St Q
  | [],s => s
  | c::p,s => clauses o p (finish o (lits o c s))

private theorem ticks {Q} (o : Op Q) (k : Nat) (w : List Letter) (s : St Q) :
    scan o (List.replicate k .tick ++ w) s = scan o w {s with head:=s.head+k} := by
  induction k generalizing s with
  | zero => rfl
  | succ k ih =>
    rw [List.replicate_succ]
    simp only [List.cons_append, scan, update, ih]
    congr 1
    simp [Nat.add_comm,Nat.add_left_comm]

private theorem next_lit {n} (ls : Clausula n) (w : List Letter) :
    delimiterNext (ls.flatMap spell ++ .delimiter :: w) = ls.isEmpty := by
  cases ls with
  | nil => rfl
  | cons l ls => cases h : l.var.val <;> simp [spell,delimiterNext,h,List.replicate_succ,List.append_assoc]

private theorem raw_lits {Q n} (o : Op Q) (ls : Clausula n) (w : List Letter)
    (s : St Q) (h : s.head = 0) :
    scan o (ls.flatMap spell ++ .delimiter :: w) s =
    scan o (.delimiter :: w) (lits o ls s) := by
  induction ls generalizing s with
  | nil => rfl
  | cons l ls ih =>
    simp only [List.flatMap_cons,spell,List.append_assoc,List.singleton_append,ticks,scan]
    change scan o (ls.flatMap spell ++ .delimiter :: w)
        (atSign o {s with head:=s.head+l.var.val} l.pos (delimiterNext (ls.flatMap spell ++ .delimiter :: w))) = _
    rw [h,Nat.zero_add,next_lit]
    simp only [atSign,home_trace,lits,applyLit]
    apply ih _ rfl

private theorem lits_home {Q n} (o : Op Q) (ls : Clausula n) (s : St Q) (h : s.head=0) :
    (lits o ls s).head=0 := by
  induction ls generalizing s with | nil => exact h | cons l ls ih => exact ih _ rfl

theorem raw_clauses {Q n} (o : Op Q) (p : CNF n) (s : St Q) (h : s.head=0) :
    scan o (original p) s = clauses o p s := by
  induction p generalizing s with
  | nil => rfl
  | cons c p ih =>
    change scan o ((c.flatMap spell ++ [.delimiter]) ++ original p) s = _
    rw [List.append_assoc,List.singleton_append,raw_lits o c _ s h]
    exact ih _ (lits_home o c s h)

def profileOp : Op Unit :=
  ⟨fun _ pos unit cell _ => (join cell (mark pos unit),()),id⟩
def start {Q} (t : Bank) (q : Q) : St Q := ⟨t,q,true,0⟩
def emptyBank : Bank := fun _ => blank

private theorem profile_lits {n} (ls : Clausula n) (s : St Unit) (j : Nat) :
    (lits profileOp ls s).bank j =
      join (s.bank j) (flags ls (s.first && singleton ls) j) := by
  induction ls generalizing s with
  | nil => simp [lits,flags,occurs,join]
  | cons l ls ih =>
    rw [lits,ih,flags_cons]
    have empty_flags (u : Bool) : flags ([] : Clausula n) u j = blank := by
      simp [flags,occurs,blank]
    cases ls with
    | nil =>
      by_cases e : l.var.val = j
      · subst j
        simp [applyLit,profileOp,SignProfile.singleton,empty_flags]
      · have back := Ne.symm e
        simp [applyLit,profileOp,Function.update_of_ne back,e,empty_flags]
    | cons z zs =>
      by_cases e : l.var.val = j
      · subst j
        simp [SignProfile.singleton,applyLit,profileOp,join_assoc]
      · have back := Ne.symm e
        simp [SignProfile.singleton,applyLit,profileOp,Function.update_of_ne back,e]

private theorem builds {n} (p : CNF n) (s : St Unit) (hs : s.first=true) (j : Nat) :
    (clauses profileOp p s).bank j = join (s.bank j) (profile p j) := by
  induction p generalizing s with
  | nil => simp [clauses,profile]
  | cons c p ih =>
    rw [clauses,ih _ rfl]
    simp only [finish,profile_lits,hs,Bool.true_and,profile,join_assoc]

theorem builds_from_letters {n} (p : CNF n) :
    (scan profileOp (original p) (start emptyBank ())).bank = profile p := by
  funext j
  rw [raw_clauses _ _ _ rfl,builds _ _ rfl]
  exact blank_join _

end Codex.TwoSweeps
