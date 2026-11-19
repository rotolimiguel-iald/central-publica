import TGLExt.RedesDeCadeias
import Mathlib.Tactic.Linarith

set_option autoImplicit false
namespace PsiNetworks.Tape
open PsiNetworks

abbrev Pair := Bool × Bool
abbrev Quad := Pair × Pair
abbrev Mask := Quad × Quad

def pack (f : Table) : Mask :=
  (((f false false false, f false false true), (f false true false, f false true true)),
   ((f true false false, f true false true), (f true true false, f true true true)))

def pick {A : Type} (p : A × A) (b : Bool) : A := if b then p.2 else p.1
def unpack (s : Mask) (a b z : Bool) : Bool := pick (pick (pick s a) b) z

@[simp] theorem unpack_pack (f : Table) : unpack (pack f) = f := by
  funext a b z
  cases a <;> cases b <;> cases z <;> rfl

inductive Letter where
  | first (lit : Lit)
  | second (lit : Lit)
  | join (serial : Bool)
  deriving DecidableEq, Fintype

inductive Cell where
  | input (s : Letter)
  | gap
  | mark (v : Mask)
  deriving DecidableEq, Fintype

inductive Mode where
  | scan (last : Mask)
  | nextLit (p : Lit)
  | saveAtom (v : Mask)
  | seekRight (serial : Bool)
  | seekLeft (serial : Bool) (right : Mask)
  | done (word verb : Bool)
  | invalid
  deriving DecidableEq, Fintype

/-- One tape. The first list is the cells strictly to the left, in reverse order.
    The second starts under the head. Its end is the physical end marker. -/
structure Config where
  mode : Mode
  before : List Cell
  afterHead : List Cell

def left (q : Mode) : List Cell → List Cell → Config
  | h::t, s => ⟨q,t,h::s⟩
  | [], s => ⟨.invalid,[],s⟩

/-- A transition reads the current cell, writes one finite symbol, moves at most
    one place, and changes finite control. No address arithmetic or head jumps. -/
def step : Config → Config
  | ⟨.scan v, p, []⟩ => ⟨.done (result (unpack v) true) (result (unpack v) false),p,[]⟩
  | ⟨.scan v, p, .gap::s⟩ => ⟨.scan v,.gap::p,s⟩
  | ⟨.scan _, p, .input (.first a)::s⟩ => ⟨.nextLit a,.gap::p,s⟩
  | ⟨.nextLit a, p, .input (.second b)::s⟩ => left (.saveAtom (pack (atom a b))) p (.gap::s)
  | ⟨.saveAtom v, p, .gap::s⟩ => ⟨.scan v,.mark v::p,s⟩
  | ⟨.scan _, p, .input (.join k)::s⟩ => left (.seekRight k) p (.gap::s)
  | ⟨.seekRight k, p, .gap::s⟩ => left (.seekRight k) p (.gap::s)
  | ⟨.seekRight k, p, .mark r::s⟩ => left (.seekLeft k r) p (.gap::s)
  | ⟨.seekLeft k r, p, .gap::s⟩ => left (.seekLeft k r) p (.gap::s)
  | ⟨.seekLeft k r, p, .mark l::s⟩ =>
    let v := pack (combine k (unpack l) (unpack r))
    ⟨.scan v,.mark v::p,s⟩
  | ⟨.done w v,p,s⟩ => ⟨.done w v,p,s⟩
  | ⟨_,p,s⟩ => ⟨.invalid,p,s⟩

def run : Nat → Config → Config
  | 0,c => c
  | n+1,c => run n (step c)

theorem run_add (m n : Nat) (c : Config) : run (m+n) c = run n (run m c) := by
  induction m generalizing c with
  | zero => simp [run]
  | succ m ih => rw [Nat.succ_add]; exact ih _

def gaps : Nat → List Cell → List Cell
  | 0,p => p
  | n+1,p => .gap :: gaps n p

theorem gaps_push (n : Nat) (p : List Cell) : gaps n (.gap::p) = .gap::gaps n p := by
  induction n with
  | zero => rfl
  | succ n ih => simp [gaps, ih]

theorem gaps_add (m n : Nat) (p : List Cell) : gaps m (gaps n p) = gaps (m+n) p := by
  induction m with
  | zero => simp [gaps]
  | succ m ih => simp [gaps, Nat.succ_add,ih]

theorem forward (n : Nat) (v : Mask) (p s : List Cell) :
    run n ⟨.scan v,p,gaps n s⟩ = ⟨.scan v,gaps n p,s⟩ := by
  induction n generalizing p with
  | zero => rfl
  | succ n ih => exact (ih (.gap::p)).trans (by rw [gaps_push]; rfl)

theorem back_right (n : Nat) (k : Bool) (p s : List Cell) :
    run n (left (.seekRight k) (gaps n p) s) = left (.seekRight k) p (gaps n s) := by
  induction n generalizing s with
  | zero => rfl
  | succ n ih => exact (ih (.gap::s)).trans (by rw [gaps_push]; rfl)

theorem back_left (n : Nat) (k : Bool) (r : Mask) (p s : List Cell) :
    run n (left (.seekLeft k r) (gaps n p) s) = left (.seekLeft k r) p (gaps n s) := by
  induction n generalizing s with
  | zero => rfl
  | succ n ih => exact (ih (.gap::s)).trans (by rw [gaps_push]; rfl)

def leafCode (a b : Lit) : List Cell := [.input (.first a), .input (.second b)]
def joinCode (serial : Bool) : Cell := .input (.join serial)

def code : Net → List Cell
  | .clause a b => leafCode a b
  | .series l r => code l ++ code r ++ [joinCode true]
  | .parallel l r => code l ++ code r ++ [joinCode false]

/-- Number of erasures to the right of the stored value for a completed expression. -/
def holes : Net → Nat
  | .clause _ _ => 1
  | .series l r | .parallel l r => holes l + holes r + 2

theorem size_code (e : Net) : (code e).length = holes e + 1 := by
  induction e with
  | clause => rfl
  | series l r hl hr | parallel l r hl hr => simp [code, holes,hl,hr]; omega

def joinTime (l r : Nat) := 1+r+1+l+1+(l+r+2)

theorem do_join (k : Bool) (lm rm old : Mask) (l r : Nat) (p s : List Cell) :
    run (joinTime l r) ⟨.scan old, gaps r (.mark rm :: gaps l (.mark lm :: p)), joinCode k :: s⟩ =
        let j := pack (combine k (unpack lm) (unpack rm))
        ⟨.scan j,gaps (l+r+2) (.mark j::p),s⟩ := by
  unfold joinTime
  rw [run_add (1+r+1+l+1) (l+r+2), run_add (1+r+1+l) 1,
      run_add (1+r+1) l, run_add (1+r) 1, run_add 1 r]
  change run (l+r+2) (step (run l (step (run r (left (.seekRight k)
    (gaps r (.mark rm :: gaps l (.mark lm :: p))) (.gap::s)))))) = _
  rw [back_right]
  change run (l+r+2) (step (run l (left (.seekLeft k rm)
    (gaps l (.mark lm :: p)) (.gap :: gaps r (.gap::s))))) = _
  rw [back_left]
  let j := pack (combine k (unpack lm) (unpack rm))
  change run (l+r+2) ⟨.scan j,.mark j :: p,gaps l (.gap :: gaps r (.gap :: s))⟩ = _
  have h : gaps l (.gap :: gaps r (.gap :: s)) = gaps (l+r+2) s := by
    rw [gaps_push, gaps_push, gaps_push, gaps_add]
    rfl
  rw [h]
  exact forward _ _ _ _

def cost : Net → Nat
  | .clause _ _ => 4
  | .series l r | .parallel l r => cost l + cost r + joinTime (holes l) (holes r)

theorem eval_tape (e : Net) (old : Mask) (p s : List Cell) :
    run (cost e) ⟨.scan old,p,code e ++ s⟩ =
        ⟨.scan (pack (summary e)),gaps (holes e) (.mark (pack (summary e))::p),s⟩ := by
  induction e generalizing old p s with
  | clause a b => rfl
  | series l r hl hr | parallel l r hl hr =>
    simp only [cost, code, List.append_assoc, List.singleton_append]
    rw [run_add _ (joinTime _ _),run_add (cost l) (cost r),hl,hr,do_join]
    simp [summary, holes]

theorem square_bound (e : Net) : cost e ≤ (code e).length ^ 2 := by
  rw [size_code]
  induction e with
  | clause => change 4 ≤ (1+1 : Nat)^2; decide
  | series l r hl hr | parallel l r hl hr =>
    simp only [cost, holes, joinTime]
    nlinarith [Nat.zero_le (holes l * holes r)]

def initial (e : Net) : Config := ⟨.scan (pack (fun _ _ _ => false)),[],code e⟩

theorem one_head_fixed_polynomial (e : Net) :
    cost e + 1 ≤ (code e).length ^ 2 + 1 ∧
    (run (cost e + 1) (initial e)).mode =
      .done (result (summary e) true) (result (summary e) false) := by
  refine ⟨Nat.add_le_add_right (square_bound e) 1, ?_⟩
  rw [run_add]
  unfold initial
  rw [← List.append_nil (code e), eval_tape]
  simp [run,step]

/-- The very same leaves agree or conflict depending on which terminals are shared. -/
theorem junction_control :
    let x : Net := .clause ⟨false,true⟩ ⟨false,true⟩
    let y : Net := .clause ⟨false,false⟩ ⟨false,false⟩
    let s := Net.series x y
    let p := Net.parallel x y
    cost s + 1 = 18 ∧ cost p + 1 = 18 ∧
      (run 18 (initial s)).mode = .done true true ∧
      (run 18 (initial p)).mode = .done false true := by decide

end PsiNetworks.Tape
