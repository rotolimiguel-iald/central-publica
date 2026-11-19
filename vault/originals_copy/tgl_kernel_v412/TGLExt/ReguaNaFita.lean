import TGLExt.ConteudoNaFita
import TGLExt.LeitorDeReuso

/-! Four fixed read-only-input scans, using the unary-address work head of
TwoSweeps. A work cell stores two bits: occupied and required value. The
shared names never become an input mask. A branch retains its first
contradiction. Four initially blank work tracks avoid a reset of a used
track; input rewinds between the four branch passes are charged. -/
set_option autoImplicit false
namespace Codex.NamedBank
open TGLExt.TraducaoTuring IALD.LeitorDaFormula Codex.PolinomioPorEscolha
open Codex.NamedTape (Row pivot forced clause formula)
open Codex.TwoSweeps Codex.SignProfile

abbrev Control := Option Bool × Bool
def stored (c : Cell) (v : Bool) := {c with seenPos := true, seenNeg := v}
def agrees (c : Cell) (v : Bool) := !c.seenPos || (c.seenNeg == v)
def program (u v : Bool) : Op Control :=
  ⟨fun zero sign _ c st => match st.1 with
    | none => (c,some ((if zero then u else v) != sign),st.2)
    | some hot => if hot then (stored c sign,none,st.2 && agrees c sign)
                  else (c,none,st.2),
    fun st => (none,st.2)⟩

def fits (t : Bank) (f : Nat → Bool) := ∀ j, (t j).seenPos=true → f j = (t j).seenNeg
def admits (t : Bank) (ok : Bool) (f : Nat → Bool) := ok=true ∧ fits t f

private theorem insert_spec (t : Bank) (ok : Bool) (j : Nat) (bit : Bool) (f : Nat → Bool) :
    admits (Function.update t j (stored (t j) bit)) (ok && agrees (t j) bit) f ↔
      admits t ok f ∧ f j=bit := by
  simp only [admits,Bool.and_eq_true]
  constructor
  · rintro ⟨⟨yes,matchOld⟩,newFits⟩
    have now := newFits j (by simp [stored])
    simp [stored] at now
    refine ⟨⟨yes,?_⟩,now⟩
    intro k occ
    by_cases eq : k=j
    · subst k
      have was : (t j).seenNeg=bit := by simpa [agrees,occ] using matchOld
      exact now.trans was.symm
    · simpa [Function.update_of_ne eq] using
        newFits k (by simpa [Function.update_of_ne eq] using occ)
  · rintro ⟨⟨yes,oldFits⟩,value⟩
    refine ⟨⟨yes,?_⟩,?_⟩
    · cases occ : (t j).seenPos with
      | false => simp [agrees,occ]
      | true => simp [agrees,occ,(oldFits j occ).symm.trans value]
    · intro k hk
      by_cases eq : k=j
      · subst k; simpa [stored] using value
      · rw [Function.update_of_ne eq] at hk ⊢
        exact oldFits k hk

variable {n : Nat}
private def endRow (u v : Bool) (t : Bank) (ok : Bool) (r : Row n) : St Control :=
  if forced u v r then
    ⟨Function.update t r.name.val (stored (t r.name.val) r.sign),
      (none,ok && agrees (t r.name.val) r.sign),true,0⟩
  else ⟨t,(none,ok),true,0⟩

private theorem one (a b : Fin n) (ha : a.val=0) (hb : 0<b.val) (u v : Bool)
    (s : St Control) (hs : s.control.1=none) (r : Row n) :
    finish (program u v) (lits (program u v) (clause a b r) s) =
      endRow u v s.bank s.control.2 r := by
  have eq : ((pivot a b r).val == 0) = !r.secondPivot := by
    cases side : r.secondPivot <;> simp [pivot,side,ha,Nat.ne_of_gt hb]
  cases side : r.secondPivot <;> cases hp : r.pivotSign <;> cases u <;> cases v <;>
    simp [endRow,finish,lits,applyLit,clause,ChainTape.edge,program,hs,eq,forced,side,hp]

private theorem end_none (u v : Bool) (t : Bank) (ok : Bool) (r : Row n) :
    (endRow u v t ok r).control.1 = none := by
  unfold endRow
  split <;> rfl

private theorem end_spec (u v : Bool) (t : Bank) (ok : Bool) (r : Row n) (f : Nat → Bool) :
    let s := endRow u v t ok r
    admits s.bank s.control.2 f ↔ admits t ok f ∧ (forced u v r=true → f r.name.val=r.sign) := by
  cases h : forced u v r <;> simp [endRow,h,insert_spec]

private theorem accumulated (a b : Fin n) (ha : a.val=0) (hb : 0<b.val) (u v : Bool)
    (rs : List (Row n)) (s : St Control) (hs : s.control.1=none) (f : Nat → Bool) :
    admits (clauses (program u v) (formula a b rs) s).bank
      (clauses (program u v) (formula a b rs) s).control.2 f ↔ admits s.bank s.control.2 f ∧
      ∀ r ∈ rs, forced u v r=true → f r.name.val=r.sign := by
  induction rs generalizing s with
  | nil => simp [formula,clauses]
  | cons r rs ih =>
    simp only [formula,List.map_cons,clauses,one a b ha hb u v s hs]
    let next := endRow u v s.bank s.control.2 r
    exact (ih next (end_none u v s.bank s.control.2 r)).trans (by
      change (admits (endRow u v s.bank s.control.2 r).bank
        (endRow u v s.bank s.control.2 r).control.2 f ∧ _) ↔ _
      have ef := end_spec u v s.bank s.control.2 r f
      dsimp only at ef
      rw [ef,List.forall_mem_cons,and_assoc])

def initial : St Control := start emptyBank (none,true)
def state (u v : Bool) (w : List Letter) := scan (program u v) w initial
def branch (u v : Bool) (w : List Letter) := (state u v w).control.2

theorem obligations (a b : Fin n) (ha : a.val=0) (hb : 0<b.val) (u v : Bool) (rs : List (Row n)) :
    branch u v (original (formula a b rs))=true ↔
      ∃ f : Nat → Bool, ∀ r ∈ rs, forced u v r=true → f r.name.val=r.sign := by
  let out := state u v (original (formula a b rs))
  have acc (f : Nat → Bool) : admits out.bank out.control.2 f ↔
      ∀ r ∈ rs, forced u v r=true → f r.name.val=r.sign := by
    dsimp only [out,state]
    rw [raw_clauses _ _ _ rfl,accumulated a b ha hb u v rs initial rfl f]
    simp [admits,fits,initial,start,emptyBank,blank]
  constructor
  · intro yes
    exact ⟨fun j => (out.bank j).seenNeg,(acc _).mp ⟨yes,fun _ _ => rfl⟩⟩
  · rintro ⟨f,cert⟩
    exact ((acc f).mpr cert).1

private theorem evaluates (a b : Fin n) (rs : List (Row n)) (u v : Bool) (x : Fin n → Bool)
    (xa : x a=u) (xb : x b=v) :
    passes (formula a b rs) x=true ↔ ∀ r ∈ rs, forced u v r=true → x r.name=r.sign := by
  simp only [formula,passes,List.all_eq_true,List.forall_mem_map]
  apply forall_congr'; intro r
  apply forall_congr'; intro _
  cases h : r.secondPivot <;> cases s : r.pivotSign <;> cases u <;> cases v <;>
    simp [clause,ChainTape.edge,pivot,forced,satisfeita,Literal.vale,h,s,xa,xb]

theorem branch_exact (a b : Fin n) (ha : a.val=0) (hb : 0<b.val) (rs : List (Row n))
    (fresh : ∀ r ∈ rs, r.name≠a ∧ r.name≠b) (u v : Bool) :
    branch u v (original (formula a b rs))=true ↔
      ∃ x : Fin n → Bool, x a=u ∧ x b=v ∧ passes (formula a b rs) x=true := by
  rw [obligations a b ha hb]
  have ne : b≠a := fun eq => by have := congrArg Fin.val eq; omega
  constructor
  · rintro ⟨f,cert⟩
    let x (j : Fin n) := if j=a then u else if j=b then v else f j.val
    have xa : x a=u := by simp [x]
    have xb : x b=v := by simp [x,ne]
    refine ⟨x,xa,xb,(evaluates _ _ _ _ _ _ xa xb).mpr ?_⟩
    intro r mem hot
    exact (by simpa [x,(fresh r mem).1,(fresh r mem).2] using cert r mem hot)
  · rintro ⟨x,xa,xb,ok⟩
    refine ⟨fun j => if h : j<n then x ⟨j,h⟩ else false,?_⟩
    intro r mem hot
    simpa [r.name.isLt] using (evaluates _ _ _ _ _ _ xa xb).mp ok r mem hot

structure Output where
  table : ChainTape.Table
  moves : Nat

def cost (u v : Bool) (w : List Letter) := travel (program u v) w initial
def read (w : List Letter) : Output :=
  let a := returned w
  let b := returned a.1
  let c := returned b.1
  ⟨((branch false false w,branch false true a.1),(branch true false b.1,branch true true c.1)),
   cost false false w + a.2 + cost false true a.1 + b.2 +
     cost true false b.1 + c.2 + cost true true c.1⟩

theorem four_branch_moves (w : List Letter) : (read w).moves ≤ 15*w.length := by
  have h (u v : Bool) : cost u v w ≤ 3*w.length := count_le (program u v) w initial
  have h₀ := h false false
  have h₁ := h false true
  have h₂ := h true false
  have h₃ := h true true
  simp only [read,returned_spec]
  omega

theorem contents_and_moves (a b : Fin n) (ha : a.val=0) (hb : 0<b.val)
    (rs : List (Row n)) (fresh : ∀ r ∈ rs, r.name≠a ∧ r.name≠b) :
    let w := original (formula a b rs)
    (read w).moves ≤ 15*w.length ∧ ∀ u v, ChainTape.getBit (read w).table u v=true ↔
      ∃ x : Fin n → Bool, x a=u ∧ x b=v ∧ passes (formula a b rs) x=true := by
  refine ⟨four_branch_moves _,?_⟩
  intro u v
  cases u <;> cases v <;> simpa [read,returned_spec,ChainTape.getBit,ChainTape.select]
    using (branch_exact a b ha hb rs fresh _ _)

private theorem stays_home (u v : Bool) (a b : Fin n) (rs : List (Row n))
    (s : St Control) (h : s.head=0) :
    (clauses (program u v) (formula a b rs) s).head=0 := by
  induction rs generalizing s with
  | nil => exact h
  | cons r rs ih => exact ih _ rfl

theorem exact_movements (a b : Fin n) (rs : List (Row n)) :
    let w := original (formula a b rs)
    (read w).moves = 7*w.length + 8*ReuseReader.ticksIn w := by
  let w := original (formula a b rs)
  have oneCost (u v : Bool) : cost u v w = w.length+2*ReuseReader.ticksIn w := by
    have h := ReuseReader.travel_balance (program u v) w initial
    have finalHead : (scan (program u v) w initial).head=0 := by
      change (scan _ (original (formula a b rs)) _).head=0
      rw [raw_clauses _ _ _ rfl]
      exact stays_home _ _ _ _ _ _ rfl
    rw [finalHead] at h
    exact h
  change (read w).moves=_
  simp only [read,returned_spec,oneCost]
  ring

end Codex.NamedBank
