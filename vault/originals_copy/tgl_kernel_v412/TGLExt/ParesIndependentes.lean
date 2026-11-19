import TGLExt.OPsiBitDaFormula
import TGLExt.LeitorDaFormula

/-! A product of local binary relations. Each flat clause is assigned to one
of the predefined disjoint pairs (Xᵢ,Yᵢ); the clause stream may interleave
different pairs arbitrarily. The two rows of a relation are two sign pairs.
Existential decoding examines four bits per pair, never a global truth table. -/
namespace IALD.ParesIndependentes
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula IALD.LeitorDaFormula TGLExt.Psibit

structure FlagPair where
  word : Bool
  verb : Bool
deriving Repr, DecidableEq

structure Mask where
  low : FlagPair
  high : FlagPair
deriving Repr, DecidableEq

def row (r : Mask) (a : Bool) := if a then r.high else r.low
def read (r : Mask) (a b : Bool) : Bool := if b then (row r a).verb else (row r a).word
def table (f : Bool → Bool → Bool) : Mask :=
  ⟨⟨f false false, f false true⟩,⟨f true false, f true true⟩⟩

@[simp] theorem read_table (f : Bool → Bool → Bool) (a b : Bool) :
    read (table f) a b = f a b := by cases a <;> cases b <;> rfl

theorem two_psibits (r : Mask) (a : Bool) :
    ∃ θ : ℝ, (codeAmp θ).word = bitSign (read r a false) ∧
      (codeAmp θ).verb = bitSign (read r a true) ∧ decodeAmp (codeAmp θ) = v θ := by
  have nz (b : Bool) : bitSign b ≠ 0 := by cases b <;> decide
  obtain ⟨θ,hw,hv⟩ := the_orbit_visits_all_four_states _ _ (nz _) (nz _)
  exact ⟨θ,hw,hv,decodeAmp_codeAmp θ⟩

structure LocalLit where
  right : Bool
  pos : Bool
deriving Repr, DecidableEq

def literal (l : LocalLit) (a b : Bool) := (if l.right then b else a) == l.pos
def localPass (c : List LocalLit) (a b : Bool) := c.any (fun l => literal l a b)
def meet (u r : Mask) := table (fun a b => read u a b && read r a b)
def rule (c : List LocalLit) := table (localPass c)

/-- Short-circuit scan under one local valuation, with actual literal visits. -/
def probe : List LocalLit → Bool → Bool → Bool × Nat
  | [],_,_ => (false,0)
  | l::c,a,b =>
    if literal l a b then (true,1) else
      let tail := probe c a b
      (tail.1,tail.2+1)

theorem probe_answer (c : List LocalLit) (a b : Bool) :
    (probe c a b).1 = localPass c a b := by
  induction c with
  | nil => rfl
  | cons l c ih => cases h : literal l a b <;> simp_all [probe,localPass]

theorem probe_visits (c : List LocalLit) (a b : Bool) : (probe c a b).2 ≤ c.length := by
  induction c with
  | nil => rfl
  | cons l c ih =>
    cases h : literal l a b
    · simpa [probe,h] using Nat.succ_le_succ ih
    · simp [probe,h]

def probeMask (c : List LocalLit) : Mask × Nat :=
  let ff := probe c false false
  let ft := probe c false true
  let tf := probe c true false
  let tt := probe c true true
  (⟨⟨ff.1,ft.1⟩,⟨tf.1,tt.1⟩⟩,ff.2+ft.2+tf.2+tt.2)

theorem probed_mask (c : List LocalLit) : (probeMask c).1 = rule c := by
  simp [probeMask,probe_answer,rule,table]

theorem probed_visits (c : List LocalLit) : (probeMask c).2 ≤ 4*c.length := by
  have h₀ := probe_visits c false false
  have h₁ := probe_visits c false true
  have h₂ := probe_visits c true false
  have h₃ := probe_visits c true true
  dsimp [probeMask]
  omega

structure LocalClause (n : Nat) where
  addr : Fin n
  lits : List LocalLit

inductive State : Nat → Type where
  | nil : State 0
  | cons {n} (head : Mask) (tail : State n) : State (n+1)

def full : (n : Nat) → State n
  | 0 => .nil
  | n+1 => .cons (table (fun _ _ => true)) (full n)

def allows : {n : Nat} → State n → (Fin n → Bool) → (Fin n → Bool) → Bool
  | _, .nil, _, _ => true
  | _, .cons m s, x, y =>
    read m (x 0) (y 0) && allows s (fun i => x i.succ) (fun i => y i.succ)

theorem full_allows (n : Nat) (x y : Fin n → Bool) : allows (full n) x y = true := by
  induction n with
  | zero => rfl
  | succ n ih => simp [full,allows,ih]

/-- The counter records every state-list row visited, including the target row. -/
def insert : {n : Nat} → State n → Fin n → Mask → State n × Nat
  | 0,.nil,i,_ => i.elim0
  | _+1,.cons m s,i,r =>
    Fin.cases (.cons (meet m r) s,1) (fun j =>
      let next := insert s j r
      (.cons m next.1,next.2+1)) i

theorem insert_spec {n} (s : State n) (i : Fin n) (r : Mask) (x y : Fin n → Bool) :
    allows (insert s i r).1 x y = (allows s x y && read r (x i) (y i)) := by
  induction s with
  | nil => exact i.elim0
  | cons m s ih =>
    cases i using Fin.cases with
    | zero => simp [insert,allows,meet,Bool.and_assoc,Bool.and_comm]
    | succ i => simp [insert,allows,ih,Bool.and_assoc]

theorem address_visits {n} (s : State n) (i : Fin n) (r : Mask) :
    (insert s i r).2 = i.val+1 := by
  induction s with
  | nil => exact i.elim0
  | cons m s ih => cases i using Fin.cases <;> simp [insert,ih]

def run {n} : List (LocalClause n) → State n → State n × Nat × Nat
  | [],s => (s,0,0)
  | c::p,s =>
    let mask := probeMask c.lits
    let step := insert s c.addr mask.1
    let tail := run p step.1
    (tail.1,step.2 + tail.2.1,mask.2 + tail.2.2)

def inputPass {n} (p : List (LocalClause n)) (x y : Fin n → Bool) :=
  p.all (fun c => localPass c.lits (x c.addr) (y c.addr))

theorem stream_spec {n} (p : List (LocalClause n)) (s : State n) (x y : Fin n → Bool) :
    allows (run p s).1 x y = (allows s x y && inputPass p x y) := by
  induction p generalizing s with
  | nil => simp [run,inputPass]
  | cons c p ih =>
    simp [run,ih,insert_spec,probed_mask,rule,inputPass,Bool.and_assoc]

def live (m : Mask) := (m.low.word || m.low.verb) || (m.high.word || m.high.verb)

theorem live_spec (m : Mask) : live m = true ↔ ∃ a b, read m a b = true := by
  simp [live,read,row,Bool.exists_bool]

def decode : {n : Nat} → State n → Bool
  | _,.nil => true
  | _,.cons m s => live m && decode s

theorem decode_spec {n} (s : State n) :
    decode s = true ↔ ∃ x y, allows s x y = true := by
  induction s with
  | nil => exact ⟨fun _ => ⟨Fin.elim0,Fin.elim0,rfl⟩,fun _ => rfl⟩
  | cons m s ih =>
    rw [decode,Bool.and_eq_true,live_spec,ih]
    constructor
    · rintro ⟨⟨a,b,hm⟩,⟨x,y,hs⟩⟩
      exact ⟨Fin.cases a x,Fin.cases b y,by simp [allows,hm,hs]⟩
    · rintro ⟨x,y,h⟩
      simp only [allows,Bool.and_eq_true] at h
      obtain ⟨hm,hs⟩ := h
      exact ⟨⟨x 0,y 0,hm⟩,⟨_,_,hs⟩⟩

def toLit {n} (i : Fin n) (l : LocalLit) : Literal (n+n) :=
  ⟨if l.right then Fin.natAdd n i else i.castAdd n,l.pos⟩

def flatten {n} (p : List (LocalClause n)) : CNF (n+n) :=
  p.map (fun c => c.lits.map (toLit c.addr))

theorem flat_pass {n} (p : List (LocalClause n)) (z : Fin (n+n) → Bool) :
    passes (flatten p) z = inputPass p (fun i => z (i.castAdd n)) (fun i => z (Fin.natAdd n i)) := by
  have he (i : Fin n) (l : LocalLit) : (toLit i l).vale z =
      literal l (z (i.castAdd n)) (z (Fin.natAdd n i)) := by
    cases l with | mk side sign => cases side <;> rfl
  simp [passes,flatten,inputPass,satisfeita,localPass,List.all_map,List.any_map,
    Function.comp_def,he]

def readWord {n} (p : List (LocalClause n)) := decode (run p (full n)).1

theorem word_eq {n} (p : List (LocalClause n)) : readWord p = palavraDaFormula (flatten p) := by
  apply Bool.eq_iff_iff.mpr
  rw [readWord,decode_spec,a_palavra_e_o_sat,sat_iff]
  simp only [stream_spec,full_allows,Bool.true_and,flat_pass]
  constructor
  · rintro ⟨x,y,h⟩
    exact ⟨Fin.append x y,by simpa only [Fin.append_left,Fin.append_right] using h⟩
  · rintro ⟨z,h⟩
    exact ⟨_,_,h⟩

/-- Recognizer for an ordinary flat CNF when at least one pair is available.
Only an empty clause uses the fallback pair, where it correctly erases all four bits. -/
def splitLit {n} (l : Literal (n+n)) : Fin n × LocalLit :=
  Fin.addCases (fun i => (i,⟨false,l.pos⟩)) (fun i => (i,⟨true,l.pos⟩)) l.var

theorem split_roundtrip {n} (l : Literal (n+n)) :
    toLit (splitLit l).1 (splitLit l).2 = l := by
  obtain ⟨j,b⟩ := l
  cases j using Fin.addCases <;> simp [splitLit,toLit,-Fin.natAdd_eq_addNat]

theorem split_toLit {n} (i : Fin n) (l : LocalLit) : splitLit (toLit i l) = (i,l) := by
  cases l with
  | mk b sign => cases b <;> simp [splitLit,toLit,-Fin.natAdd_eq_addNat]

def groupAddr {n} (fallback : Fin n) : Clausula (n+n) → Fin n
  | [] => fallback
  | l::_ => (splitLit l).1
def group {n} (fallback : Fin n) (c : Clausula (n+n)) : LocalClause n :=
  ⟨groupAddr fallback c,c.map (fun l => (splitLit l).2)⟩
def withinPair {n} (fallback : Fin n) (c : Clausula (n+n)) :=
  let addr := groupAddr fallback c
  c.all (fun l => (splitLit l).1 == addr)

theorem group_back {n} (fallback : Fin n) (c : Clausula (n+n)) (h : withinPair fallback c) :
    (group fallback c).lits.map (toLit (group fallback c).addr) = c := by
  let i := (group fallback c).addr
  change (c.map (fun l => (splitLit l).2)).map (toLit i) = c
  rw [List.map_map]
  calc
    _ = c.map id := List.map_congr_left (fun l hl => by
      have he : (splitLit l).1 = i := beq_iff_eq.mp (List.all_eq_true.mp h _ hl)
      exact he ▸ split_roundtrip l)
    _ = c := List.map_id c

theorem every_emitted_clause_passes {n} (fallback : Fin n) (c : LocalClause n) :
    withinPair fallback (c.lits.map (toLit c.addr)) = true := by
  obtain ⟨i,ls⟩ := c
  cases ls with
  | nil => rfl
  | cons l ls => simp [withinPair,groupAddr,split_toLit,List.all_map,Function.comp_def]

def checkedWord {n} (fallback : Fin n) (p : CNF (n+n)) : Option Bool :=
  if p.all (withinPair fallback) then some (readWord (p.map (group fallback))) else none

theorem checked_sound {n} (fallback : Fin n) (p : CNF (n+n)) (b : Bool)
    (hb : checkedWord fallback p = some b) : b = palavraDaFormula p := by
  unfold checkedWord at hb
  split at hb
  next hall =>
    have eqn : flatten (p.map (group fallback)) = p := by
      rw [flatten,List.map_map]
      calc
        _ = p.map id := List.map_congr_left (fun c hc =>
          group_back fallback c (List.all_eq_true.mp hall c hc))
        _ = p := List.map_id p
    cases hb
    rw [word_eq,eqn]
  next => contradiction

theorem checked_complete {n} (fallback : Fin n) (p : List (LocalClause n)) :
    checkedWord fallback (flatten p) = some (palavraDaFormula (flatten p)) := by
  have hall : (flatten p).all (withinPair fallback) = true := by
    apply List.all_eq_true.mpr
    intro c hc
    obtain ⟨q,_,rfl⟩ := List.mem_map.mp hc
    exact every_emitted_clause_passes fallback q
  have hok : checkedWord fallback (flatten p) =
      some (readWord ((flatten p).map (group fallback))) := by simp [checkedWord,hall]
  exact hok.trans (congrArg some (checked_sound _ _ _ hok))

/-- The actual stored data bits in the state, excluding the fixed list spine. -/
def dataBits : {n : Nat} → State n → Nat
  | _,.nil => 0
  | _,.cons _ s => 4 + dataBits s

theorem storage {n} (s : State n) : dataBits s = 4*n := by
  induction s with
  | nil => rfl
  | cons m s ih => simp only [dataBits,ih,Nat.mul_succ]; omega

def scans {n} (p : List (LocalClause n)) := (p.map (fun c => c.addr.val+1)).sum
def literals {n} (p : List (LocalClause n)) := (p.map (fun c => c.lits.length)).sum

theorem actual_scans {n} (p : List (LocalClause n)) (s : State n) :
    (run p s).2.1 = scans p := by
  induction p generalizing s with
  | nil => rfl
  | cons c p ih => simp [run,address_visits,ih,scans]

theorem actual_literal_visits {n} (p : List (LocalClause n)) (s : State n) :
    (run p s).2.2 ≤ 4*literals p := by
  induction p generalizing s with
  | nil => rfl
  | cons c p ih =>
    have h := probed_visits c.lits
    have ht := ih (insert s c.addr (probeMask c.lits).1).1
    change (probeMask c.lits).2 + _ ≤ 4*(c.lits.length + literals p)
    omega

/- Fixed alphabet: n header ticks then stop; each clause starts with i ticks then
addressEnd; each literal has side and sign; one clauseEnd. Empty clauses allowed. -/
inductive Symbol where
  | tick | headerEnd | addressEnd | clauseEnd | side (b : Bool) | sign (b : Bool)

def encodeClause {n} (c : LocalClause n) : List Symbol :=
  List.replicate c.addr.val .tick ++ [.addressEnd] ++
    c.lits.flatMap (fun l => [.side l.right,.sign l.pos]) ++ [.clauseEnd]
def encode {n} (p : List (LocalClause n)) : List Symbol :=
  List.replicate n .tick ++ [.headerEnd] ++ p.flatMap encodeClause

theorem encoding_size {n} (p : List (LocalClause n)) :
    (encode p).length = n+1 + scans p + 2*literals p + p.length := by
  have hh : (p.flatMap encodeClause).length = scans p + 2*literals p + p.length := by
    induction p with
    | nil => rfl
    | cons c p ih =>
      simp [scans,literals,encodeClause] at ih ⊢
      omega
  simp [encode,hh]; omega

/-- Upper charge rather than a raw transition count of a Turing machine.
Eight operations per initialized/finally read row (filling/combining four
bits), three per state row visited (read, advance/rebuild), fourteen per
target (mask construction, intersection and control), and four full scans
of each clause counting side, sign, branch and OR (16 per literal). -/
def charge {n} (p : List (LocalClause n)) :=
  8*(n+1) + 3*(run p (full n)).2.1 + 14*p.length + 4*(run p (full n)).2.2

theorem linear_charge {n} (p : List (LocalClause n)) : charge p ≤ 14*(encode p).length := by
  have hv := actual_literal_visits p (full n)
  rw [charge,actual_scans,encoding_size]
  omega

/-- Three admissible rows in one ordinary disjunction; two later negative
units, on the same pair, eliminate every remaining assignment. -/
def orPair : LocalClause 1 := ⟨0,[⟨false,true⟩,⟨true,true⟩]⟩
def noX : LocalClause 1 := ⟨0,[⟨false,false⟩]⟩
def noY : LocalClause 1 := ⟨0,[⟨true,false⟩]⟩

theorem three_then_none :
    rule orPair.lits = ⟨⟨false,true⟩,⟨true,true⟩⟩ ∧
    readWord [orPair,noX] = true ∧ readWord [orPair,noX,noY] = false := by decide

end IALD.ParesIndependentes
