import TGLExt.FatoresIndependentes

/-! Join along a still-free Boolean. A crossing clause uses one extra bit
per side, recording whether a local witness can satisfy its share of the
clause while using the same boundary value. -/
set_option autoImplicit false
namespace Codex.FreeSeparator
open TGLExt.TraducaoTuring IALD.LeitorDaFormula Codex.BranchPresence Codex.IndependentFactors
variable {n : Nat}

def slice (p : CNF n) (c : Clausula n) (owner : Bool) : Clausula n :=
  c.filter (fun l => appears p l.var == owner)

private theorem hit (p : CNF n) (c : Clausula n) (owner : Bool) (x : Fin n → Bool) :
    satisfeita (slice p c owner) x = true ↔
      ∃ l ∈ c, appears p l.var = owner ∧ x l.var = l.pos := by
  simp only [satisfeita,List.any_eq_true,slice,List.mem_filter,beq_iff_eq,Literal.vale]
  constructor
  · rintro ⟨l,⟨m,a⟩,v⟩
    exact ⟨l,m,a,v⟩
  · rintro ⟨l,m,a,v⟩
    exact ⟨l,⟨m,a⟩,v⟩

private theorem append_pass (p q : CNF n) (x : Fin n → Bool) :
    passes (p++q) x = true ↔ passes p x = true ∧ passes q x = true := by simp [passes]

private theorem last_pass (p : CNF n) (c : Clausula n) (x : Fin n → Bool) :
    passes (p++[c]) x = true ↔ passes p x = true ∧ satisfeita c x = true := by
  simp [passes]

/-- This formula is valid for any known separator assignment contained in
ms. The entering clause may mention both blocks and entirely new variables.
Every literal is assigned to the left if it occurs in p, to the right
otherwise, matching the definition of the pasted assignment. -/
theorem conditional_join (p q : CNF n) (c : Clausula n) (ms : List (Literal n))
    (cut : splitAtLabels p q ms) :
    Compatible ((p++q)++[c]) ms ↔
      (Compatible (p++[slice p c true]) ms ∧ Compatible q ms) ∨
      (Compatible p ms ∧ Compatible (q++[slice p c false]) ms) := by
  constructor
  · rintro ⟨x,ok,marks⟩
    obtain ⟨pq,whole⟩ := (last_pass _ _ _).mp ok
    obtain ⟨px,qx⟩ := (append_pass _ _ _).mp pq
    obtain ⟨l,m,v⟩ := List.any_eq_true.mp whole
    have value : x l.var = l.pos := by simpa [Literal.vale] using v
    cases e : appears p l.var with
    | false =>
      exact Or.inr ⟨⟨x,px,marks⟩,x,(last_pass _ _ _).mpr
        ⟨qx,(hit p c false x).mpr ⟨l,m,e,value⟩⟩,marks⟩
    | true =>
      exact Or.inl ⟨⟨x,(last_pass _ _ _).mpr
        ⟨px,(hit p c true x).mpr ⟨l,m,e,value⟩⟩,marks⟩,x,qx,marks⟩
  · rintro (⟨⟨x,ph,xm⟩,⟨y,qy,ym⟩⟩ | ⟨⟨x,px,xm⟩,⟨y,qh,ym⟩⟩)
    · obtain ⟨px,hx⟩ := (last_pass _ _ _).mp ph
      obtain ⟨l,m,own,v⟩ := (hit p c true x).mp hx
      obtain ⟨pq,marks⟩ := glue p q ms cut x y px qy xm ym
      exact ⟨paste p x y,(last_pass _ _ _).mpr ⟨pq,List.any_eq_true.mpr
        ⟨l,m,by simp [Literal.vale,paste,own,v]⟩⟩,marks⟩
    · obtain ⟨qy,hy⟩ := (last_pass _ _ _).mp qh
      obtain ⟨l,m,own,v⟩ := (hit p c false y).mp hy
      obtain ⟨pq,marks⟩ := glue p q ms cut x y px qy xm ym
      exact ⟨paste p x y,(last_pass _ _ _).mpr ⟨pq,List.any_eq_true.mpr
        ⟨l,m,by simp [Literal.vale,paste,own,v]⟩⟩,marks⟩

def oneFree (p q : CNF n) (ms : List (Literal n)) (s : Fin n) : Prop :=
  ∀ i, appears p i = true → appears q i = true → i=s ∨ ∃ l ∈ ms, l.var=i

private theorem fixed (p q : CNF n) (ms : List (Literal n)) (s : Fin n) (b : Bool)
    (cut : oneFree p q ms s) : splitAtLabels p q (⟨s,b⟩::ms) := by
  intro i hp hq
  rcases cut i hp hq with eq | ⟨l,mem,rfl⟩
  · exact ⟨⟨s,b⟩,List.mem_cons_self,eq.symm⟩
  · exact ⟨l,List.mem_cons_of_mem _ mem,rfl⟩

private theorem split_value (p : CNF n) (ms : List (Literal n)) (s : Fin n) :
    Compatible p ms ↔ Compatible p (⟨s,false⟩::ms) ∨ Compatible p (⟨s,true⟩::ms) := by
  constructor
  · rintro ⟨x,h,m⟩
    have marked : Agrees x (⟨s,x s⟩::ms) := by simpa [Agrees] using m
    cases e : x s with
    | false => exact Or.inl ⟨x,h,e ▸ marked⟩
    | true => exact Or.inr ⟨x,h,e ▸ marked⟩
  · rintro (⟨x,h,m⟩|⟨x,h,m⟩) <;> exact ⟨x,h,fun l hl => m l (List.mem_cons_of_mem _ hl)⟩

/-- For fixed marks the first bit tells if the block has a witness at all.
The second requires that witness to satisfy a literal of its clause slice. -/
abbrev Flags := Bool × Bool
def flags (p : CNF n) (c : Clausula n) (ms : List (Literal n)) : Flags :=
  (search p ms,search (p++[c]) ms)

def joinFlags (left right : Flags) := (left.2 && right.1) || (left.1 && right.2)

def row (p q : CNF n) (c : Clausula n) (ms : List (Literal n)) :=
  joinFlags (flags p (slice p c true) ms) (flags q (slice p c false) ms)

theorem row_exact (p q : CNF n) (c : Clausula n) (ms : List (Literal n))
    (cut : splitAtLabels p q ms) : row p q c ms = true ↔ Compatible ((p++q)++[c]) ms := by
  simpa only [row,flags,joinFlags,Bool.or_eq_true,Bool.and_eq_true,search_correct]
    using (conditional_join p q c ms cut).symm

def update (p q : CNF n) (c : Clausula n) (ms : List (Literal n)) (s : Fin n) :=
  row p q c (⟨s,false⟩::ms) || row p q c (⟨s,true⟩::ms)

theorem update_exact (p q : CNF n) (c : Clausula n) (ms : List (Literal n)) (s : Fin n)
    (cut : oneFree p q ms s) : update p q c ms s = true ↔ Compatible ((p++q)++[c]) ms := by
  rw [update,Bool.or_eq_true,row_exact _ _ _ _ (fixed p q ms s false cut),
    row_exact _ _ _ _ (fixed p q ms s true cut),←split_value]

/-- A branch label uses a pivot mark in addition to the shared live value.
They may be the same variable. -/
theorem branch_exact (p q : CNF n) (c : Clausula n) (pivot s : Fin n) (v : Bool)
    (cut : oneFree p q [⟨pivot,v⟩] s) :
    update p q c [⟨pivot,v⟩] s = true ↔
      ∃ x : Fin n → Bool, x pivot = v ∧ passes ((p++q)++[c]) x = true := by
  rw [update_exact _ _ _ _ _ cut]
  constructor
  · rintro ⟨x,h,m⟩
    exact ⟨x,m ⟨pivot,v⟩ (by simp),h⟩
  · rintro ⟨x,vx,h⟩
    exact ⟨x,h,by simpa [Agrees] using vx⟩

/-! Eight flag bits suffice for one queried branch after the two local tables
are available. Each emitted bit advances one read-only head. The prefixed
tables are charged separately from this finite-control receiver. -/
inductive Stage where
  | start
  | leftLive (a : Bool)
  | leftBoth (a h : Bool)
  | beforeHit (a h r : Bool)
  deriving DecidableEq

abbrev Reg := Bool × Stage

def receive (s : Reg) (bit : Bool) : Reg :=
  match s.2 with
  | .start => (s.1,.leftLive bit)
  | .leftLive a => (s.1,.leftBoth a bit)
  | .leftBoth a h => (s.1,.beforeHit a h bit)
  | .beforeHit a h r => (s.1 || joinFlags (a,h) (r,bit),.start)

def packet (l r : Flags) : List Bool := [l.1,l.2,r.1,r.2]

def traverse : Reg → List Bool → Reg × Nat
  | s,[] => (s,0)
  | s,v::vs => let result := traverse (receive s v) vs; (result.1,result.2+1)

theorem traverse_spec (s : Reg) (vs : List Bool) :
    traverse s vs = (vs.foldl receive s,vs.length) := by
  induction vs generalizing s with
  | nil => rfl
  | cons v vs ih => simp [traverse,ih]

def packets (p q : CNF n) (c : Clausula n) (ms : List (Literal n)) (s : Fin n) :=
  let atValue := fun (v : Bool) =>
    let marks := (⟨s,v⟩ : Literal n)::ms
    packet (flags p (slice p c true) marks) (flags q (slice p c false) marks)
  atValue false ++ atValue true

theorem eight_moves (p q : CNF n) (c : Clausula n) (ms : List (Literal n)) (s : Fin n) :
    traverse (false,.start) (packets p q c ms s) = ((update p q c ms s,.start),8) := by
  rw [traverse_spec]
  simp [packets,packet,receive,row,update]

theorem packet_decides (p q : CNF n) (c : Clausula n) (ms : List (Literal n)) (s : Fin n)
    (cut : oneFree p q ms s) :
    let r := traverse (false,.start) (packets p q c ms s)
    (r.1.1 = true ↔ Compatible ((p++q)++[c]) ms) ∧ r.2 = 8 := by
  simpa only [eight_moves,and_true] using update_exact p q c ms s cut

/-! Appending a genuine shared-variable bridge can encode an arbitrary input
formula inside the left block. The source transformation is a one-pass
transducer: copy input tokens, emit three extra ticks at each sign, append a
fixed fifteen-letter gadget. Both its input and output motion are measured. -/
open Codex.PolinomioPorEscolha

def shifted (l : Literal n) : Literal (n+3) := ⟨l.var.succ.succ.succ,l.pos⟩
def renamed (p : CNF n) : CNF (n+3) := p.map (List.map shifted)

def sepVar (n : Nat) : Fin (n+3) := ⟨0,by omega⟩
def leftVar (n : Nat) : Fin (n+3) := ⟨1,by omega⟩
def rightVar (n : Nat) : Fin (n+3) := ⟨2,by omega⟩
def leftEdge (n : Nat) : Clausula (n+3) := [⟨sepVar n,true⟩,⟨leftVar n,true⟩]
def rightEdge (n : Nat) : Clausula (n+3) := [⟨sepVar n,true⟩,⟨rightVar n,true⟩]
def bridge (n : Nat) : Clausula (n+3) := [⟨leftVar n,false⟩,⟨rightVar n,false⟩]
def wrapped (p : CNF n) : CNF (n+3) := renamed p ++ [leftEdge n,rightEdge n,bridge n]

private theorem renamed_eval (p : CNF n) (y : Fin (n+3) → Bool) :
    passes (renamed p) y = passes p (fun i => y i.succ.succ.succ) := by
  simp [renamed,passes,satisfeita,Literal.vale,shifted,List.all_map,List.any_map,Function.comp_def]

def witness (x : Fin n → Bool) : Fin (n+3) → Bool :=
  Fin.cases true (Fin.cases false (Fin.cases false x))

private theorem witness_bits (x : Fin n → Bool) :
    witness x (sepVar n) = true ∧ witness x (leftVar n) = false ∧
      witness x (rightVar n) = false := by
  change witness x 0 = true ∧ witness x (Fin.succ 0) = false ∧ witness x (Fin.succ (Fin.succ 0)) = false
  simp only [witness,Fin.cases_zero,Fin.cases_succ,and_self]

theorem wrapped_compatible (p : CNF n) : Compatible (wrapped p) [] ↔ Compatible p [] := by
  constructor
  · rintro ⟨y,good,_⟩
    have yy := ((append_pass _ _ _).mp good).1
    exact ⟨fun i => y i.succ.succ.succ,(renamed_eval p y) ▸ yy,by simp [Agrees]⟩
  · rintro ⟨x,ok,_⟩
    have hx : passes (renamed p) (witness x) = true := by
      simpa [renamed_eval,witness] using ok
    obtain ⟨a,b,c⟩ := witness_bits x
    exact ⟨witness x,(append_pass _ _ _).mpr ⟨hx,by
      simp [passes,leftEdge,rightEdge,bridge,satisfeita,Literal.vale,a,b,c]⟩,by simp [Agrees]⟩

private theorem right_absent (p : CNF n) : appears (renamed p) (rightVar n) = false := by
  apply Bool.eq_false_iff.mpr
  intro ok
  obtain ⟨c,hc,l,hl,eq⟩ : ∃ c ∈ renamed p, ∃ l ∈ c, l.var = rightVar n := by
    simpa [appears,List.any_eq_true] using ok
  obtain ⟨d,_,rfl⟩ := List.mem_map.mp hc
  obtain ⟨t,_,rfl⟩ := List.mem_map.mp hl
  have bad := congrArg Fin.val eq
  simp [shifted,rightVar] at bad

theorem genuinely_shared (p : CNF n) :
    oneFree (renamed p ++ [leftEdge n]) [rightEdge n] [] (sepVar n) ∧
    appears (renamed p ++ [leftEdge n]) (sepVar n) = true ∧
    appears [rightEdge n] (sepVar n) = true := by
  have d0 : sepVar n ≠ rightVar n := fun h => by have e := congrArg Fin.val h; simp [sepVar,rightVar] at e
  have d1 : leftVar n ≠ rightVar n := fun h => by have e := congrArg Fin.val h; simp [leftVar,rightVar] at e
  refine ⟨?_,by simp [appears,leftEdge],by simp [appears,rightEdge]⟩
  intro i hl hr
  have r : sepVar n = i ∨ rightVar n = i := by simpa [appears,rightEdge] using hr
  rcases r with e | rfl
  · exact Or.inl e.symm
  · have noRight := right_absent p
    simp [appears] at noRight
    simp [appears,leftEdge,d0,d1] at hl
    obtain ⟨c,hc,l,hm,e⟩ := hl
    exact ((noRight c hc l hm) e).elim

def emit : Letter → List Letter
  | .sign v => [.tick,.tick,.tick,.sign v]
  | l => [l]

private theorem emit_lit (l : Literal n) : (spell l).flatMap emit = spell (shifted l) := by
  have copied (i : Nat) : (List.replicate i Letter.tick).flatMap emit = List.replicate i .tick := by
    induction i with
    | zero => rfl
    | succ k ih => simp [List.replicate_succ,emit,ih]
  simp [spell,shifted,Fin.val_succ,List.flatMap_append,copied,emit,List.replicate_add,List.append_assoc]

private theorem emit_clause (c : Clausula n) :
    (spellClause c).flatMap emit = spellClause (c.map shifted) := by
  have many (ls : Clausula n) : (ls.flatMap spell).flatMap emit = (ls.map shifted).flatMap spell := by
    induction ls with
    | nil => rfl
    | cons l ls ih => simp [List.flatMap_append,emit_lit,ih]
  simp [spellClause,List.flatMap_append,many,emit]

private theorem emit_formula (p : CNF n) : (original p).flatMap emit = original (renamed p) := by
  induction p with
  | nil => rfl
  | cons c p ih =>
    change (spellClause c ++ original p).flatMap emit = spellClause (List.map shifted c) ++ original (renamed p)
    rw [List.flatMap_append,emit_clause,ih]

def trailer := original [leftEdge 0,rightEdge 0,bridge 0]

theorem emitted (p : CNF n) :
    (original p).flatMap emit ++ trailer = original (wrapped p) := by
  rw [emit_formula]
  have constant : original [leftEdge n,rightEdge n,bridge n] = trailer := by rfl
  simpa only [wrapped,original,List.flatMap_append] using congrArg (original (renamed p) ++ ·) constant.symm

/-- A letter written consumes one rightward output-head move; a consumed
input letter consumes one rightward input-head move. No search or random
access is part of this representation change. -/
def writeMoves : List Letter → Nat
  | [] => 0
  | _::rest => writeMoves rest + 1

def copyMoves : List Letter → Nat
  | [] => writeMoves trailer
  | l::rest => 1 + writeMoves (emit l) + copyMoves rest

theorem copy_bound (w : List Letter) :
    copyMoves w ≤ 5*w.length+15 := by
  induction w with
  | nil => decide
  | cons l w ih =>
    have small : writeMoves (emit l) ≤ 4 := by cases l <;> simp [writeMoves,emit]
    simp only [copyMoves,List.length_cons]
    omega

/-- Both boundary values really are possible before the entering clause,
provided the arbitrary original formula has a model. -/
theorem free_before (p : CNF n) (b : Bool) :
    Compatible (renamed p ++ [leftEdge n,rightEdge n]) [⟨sepVar n,b⟩] ↔ Compatible p [] := by
  constructor
  · rintro ⟨y,ok,_⟩
    have h := ((append_pass _ _ _).mp ok).1
    exact ⟨fun i => y i.succ.succ.succ,(renamed_eval p y) ▸ h,by simp [Agrees]⟩
  · rintro ⟨x,ok,_⟩
    let y : Fin (n+3) → Bool := Fin.cases b (Fin.cases (!b) (Fin.cases (!b) x))
    have values : y (sepVar n)=b ∧ y (leftVar n)=(!b) ∧ y (rightVar n)=(!b) := by
      change y 0 = b ∧ y (Fin.succ 0) = (!b) ∧ y (Fin.succ (Fin.succ 0)) = (!b)
      simp only [y,Fin.cases_zero,Fin.cases_succ,and_self]
    obtain ⟨s,a,z⟩ := values
    have hx : passes (renamed p) y = true := by simpa [renamed_eval,y] using ok
    exact ⟨y,(append_pass _ _ _).mpr ⟨hx,by cases b <;>
      simp [passes,leftEdge,rightEdge,satisfeita,Literal.vale,s,a,z]⟩,by simpa [Agrees] using s⟩

theorem false_closed (p : CNF n) : ¬ Compatible (wrapped p) [⟨sepVar n,false⟩] := by
  rintro ⟨y,ok,mark⟩
  have s : y (sepVar n) = false := mark ⟨sepVar n,false⟩ List.mem_cons_self
  have h := ((append_pass _ _ _).mp ok).2
  cases a : y (leftVar n) <;> cases b : y (rightVar n) <;>
    simp [passes,leftEdge,rightEdge,bridge,satisfeita,Literal.vale,s,a,b] at h

/-- The surviving boundary bit is exactly SAT of the source formula. -/
theorem true_after (p : CNF n) :
    Compatible (wrapped p) [⟨sepVar n,true⟩] ↔ Compatible p [] := by
  have h := split_value (wrapped p) [] (sepVar n)
  rw [or_iff_right (false_closed p)] at h
  exact h.symm.trans (wrapped_compatible p)

/-- Event trace of a left-to-right transducer. Each event is one charged
head move; a read moves the source head and a write moves the target head.
The output trace is produced in order from the current symbol. -/
inductive Move where
  | read (a : Letter)
  | write (a : Letter)

def transport : List Letter → List Move
  | [] => trailer.map Move.write
  | a::w => .read a :: (emit a).map Move.write ++ transport w

def written (step : Move) : Option Letter := match step with
  | .read _ => none
  | .write a => some a

def consumed (step : Move) : Option Letter := match step with
  | .read a => some a
  | .write _ => none

private theorem writes (w : List Letter) :
    (w.map Move.write).filterMap written = w ∧
    (w.map Move.write).filterMap consumed = [] ∧ writeMoves w = w.length := by
  induction w with
  | nil => simp [writeMoves]
  | cons a w ih => simp [written,consumed,writeMoves,ih.2.2]

theorem transport_spec (w : List Letter) :
    (transport w).filterMap consumed = w ∧
    (transport w).filterMap written = (w.flatMap emit ++ trailer) ∧
    (transport w).length = copyMoves w := by
  induction w with
  | nil => exact ⟨(writes trailer).2.1,(writes trailer).1,by simp [transport,copyMoves,(writes trailer).2.2]⟩
  | cons a w ih =>
    have h := writes (emit a)
    constructor
    · change a :: (((emit a).map Move.write ++ transport w).filterMap consumed) = a :: w
      rw [List.filterMap_append,h.2.1,ih.1,List.nil_append]
    constructor
    · change ((emit a).map Move.write ++ transport w).filterMap written = (emit a ++ w.flatMap emit) ++ trailer
      rw [List.filterMap_append,h.1,ih.2.1,List.append_assoc]
    · change ((emit a).map Move.write ++ transport w).length + 1 = 1 + writeMoves (emit a) + copyMoves w
      rw [List.length_append,List.length_map,ih.2.2,h.2.2]
      omega

theorem linear_embedding (p : CNF n) :
    let steps := transport (original p)
    steps.filterMap consumed = original p ∧ steps.filterMap written = original (wrapped p) ∧
    steps.length ≤ 5*(original p).length+15 ∧ (Compatible (wrapped p) [] ↔ Compatible p []) := by
  obtain ⟨source,target,moves⟩ := transport_spec (original p)
  exact ⟨source,target.trans (emitted p),moves ▸ (copy_bound _),wrapped_compatible p⟩

end Codex.FreeSeparator
