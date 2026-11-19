import TGLExt.ParesIndependentes

/-! Linear padding from every flat CNF to one whose every clause crosses two
predefined pairs. The pair convention is exactly the two-block numbering of
ParesIndependentes. Two fresh left coordinates (0 and 1) lie in different
pairs. The remaining original labels are shifted by two; the right copy
provides the partners and is unconstrained. -/
namespace IALD.CruzamentosUniversais
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula IALD.LeitorDaFormula

abbrev width (n : Nat) := (n+2)+(n+2)
abbrev Env (n : Nat) := Fin n → Bool

def a (n : Nat) : Fin (width n) := (0 : Fin (n+2)).castAdd (n+2)
def b (n : Nat) : Fin (width n) := (0 : Fin (n+1)).succ.castAdd (n+2)
def shift {n} (i : Fin n) : Fin (width n) := i.succ.succ.castAdd (n+2)
def liftLit {n} (l : Literal n) : Literal (width n) := ⟨shift l.var,l.pos⟩

def pad {n} (c : Clausula n) : Clausula (width n) :=
  ⟨a n,true⟩ :: ⟨b n,true⟩ :: c.map liftLit
def guardClause (n : Nat) (p q : Bool) : Clausula (width n) :=
  [⟨a n,p⟩,⟨b n,q⟩]
def guards (n : Nat) : CNF (width n) :=
  [guardClause n false false,guardClause n false true,guardClause n true false]
def translate {n} (p : CNF n) : CNF (width n) := p.map pad ++ guards n

/-- A literal's pair index ignores which side it uses. Both halves use the
same numbering, as in the flat recognizer of ParesIndependentes. -/
def pair {k} (l : Literal (k+k)) := (ParesIndependentes.splitLit l).1
def crosses {k} (c : Clausula (k+k)) :=
  ∃ l ∈ c, ∃ r ∈ c, pair l ≠ pair r

private theorem distinct_pairs (n : Nat) (p q : Bool) :
    pair (⟨a n,p⟩ : Literal (width n)) ≠ pair (⟨b n,q⟩ : Literal (width n)) := by
  simp [pair,ParesIndependentes.splitLit,a,b]

private theorem first_two {n} (p q : Bool) (rest : Clausula (width n)) :
    crosses (⟨a n,p⟩ :: ⟨b n,q⟩ :: rest) := by
  exact ⟨_,List.mem_cons_self,_,List.mem_cons_of_mem _ List.mem_cons_self,distinct_pairs n p q⟩

theorem every_clause_crosses {n} (p : CNF n) (c : Clausula (width n)) (hc : c ∈ translate p) :
    crosses c := by
  rcases List.mem_append.mp hc with hp | hg
  · obtain ⟨d,_,rfl⟩ := List.mem_map.mp hp
    exact first_two _ _ _
  · simp [guards] at hg
    rcases hg with rfl | rfl | rfl <;> exact first_two _ _ _

def projectEnv {n} (z : Env (width n)) : Env n := fun i => z (shift i)
def extendEnv {n} (x : Env n) : Env (width n) :=
  Fin.append (Fin.cases false (Fin.cases false x)) (fun _ => false)

@[simp] theorem extend_a {n} (x : Env n) : extendEnv x (a n) = false := by
  simp [extendEnv,a]
@[simp] theorem extend_b {n} (x : Env n) : extendEnv x (b n) = false := by
  simp only [extendEnv,b,Fin.append_left,Fin.cases_succ,Fin.cases_zero]
@[simp] theorem project_extend {n} (x : Env n) : projectEnv (extendEnv x) = x := by
  funext i; simp [projectEnv,extendEnv,shift]

theorem guarded {n} (z : Env (width n)) :
    passes (guards n) z = true ↔ z (a n) = false ∧ z (b n) = false := by
  cases ha : z (a n) <;> cases hb : z (b n) <;>
    simp [passes,guards,guardClause,satisfeita,Literal.vale,ha,hb]

theorem pad_boolean {n} (c : Clausula n) (z : Env (width n))
    (ha : z (a n) = false) (hb : z (b n) = false) :
    satisfeita (pad c) z = satisfeita c (projectEnv z) := by
  simp [pad,satisfeita,Literal.vale,ha,hb,liftLit,projectEnv,Function.comp_def]

private theorem all_padded {n} (p : CNF n) (z : Env (width n))
    (ha : z (a n) = false) (hb : z (b n) = false) :
    passes (p.map pad) z = passes p (projectEnv z) := by
  induction p with
  | nil => rfl
  | cons c p ih =>
    change (satisfeita (pad c) z && passes (p.map pad) z) =
      (satisfeita c (projectEnv z) && passes p (projectEnv z))
    rw [pad_boolean _ _ ha hb,ih]

theorem witness_exact {n} (p : CNF n) (z : Env (width n)) :
    passes (translate p) z = true ↔
      z (a n) = false ∧ z (b n) = false ∧ passes p (projectEnv z) = true := by
  have split : passes (translate p) z = (passes (p.map pad) z && passes (guards n) z) :=
    List.all_append
  rw [split,Bool.and_eq_true,guarded]
  constructor
  · rintro ⟨hv,ha,hb⟩
    exact ⟨ha,hb,(all_padded _ _ ha hb).symm.trans hv⟩
  · rintro ⟨ha,hb,hv⟩
    exact ⟨(all_padded _ _ ha hb).trans hv,ha,hb⟩

theorem word_preserved {n} (p : CNF n) :
    palavraDaFormula (translate p) = palavraDaFormula p := by
  apply Bool.eq_iff_iff.mpr
  rw [a_palavra_e_o_sat,a_palavra_e_o_sat,sat_iff,sat_iff]
  constructor
  · rintro ⟨z,hz⟩
    exact ⟨projectEnv z,((witness_exact p z).mp hz).2.2⟩
  · rintro ⟨x,hx⟩
    exact ⟨extendEnv x,(witness_exact p _).mpr (by simpa using hx)⟩

theorem clause_count {n} (p : CNF n) : (translate p).length = p.length+3 := by
  simp [translate,guards]

inductive Mark | tick | headerEnd | sign (b : Bool) | clauseEnd
def emitLit {n} (l : Literal n) : List Mark := List.replicate l.var.val .tick ++ [.sign l.pos]
def emitClause {n} (c : Clausula n) : List Mark := c.flatMap emitLit ++ [.clauseEnd]
def body {n} (p : CNF n) := p.flatMap emitClause
def input {n} (p : CNF n) : List Mark := List.replicate n .tick ++ [.headerEnd] ++ body p
def occ {n} (p : CNF n) := (p.map List.length).sum

private theorem shift_length {n} (l : Literal n) :
    (emitLit (liftLit l)).length = (emitLit l).length+2 := by
  simp [liftLit,shift,emitLit]

private theorem shifted_list {n} (c : Clausula n) :
    ((c.map liftLit).flatMap emitLit).length = (c.flatMap emitLit).length + 2*c.length := by
  induction c with
  | nil => rfl
  | cons l c ih =>
    simp only [List.map_cons,List.flatMap_cons,List.length_append,shift_length,ih,List.length_cons]
    omega

private theorem pad_length {n} (c : Clausula n) :
    (emitClause (pad c)).length = (emitClause c).length + 2*c.length+3 := by
  change (([Mark.sign true,Mark.tick,Mark.sign true] ++ (c.map liftLit).flatMap emitLit)
    ++ [Mark.clauseEnd]).length =
    (c.flatMap emitLit ++ [Mark.clauseEnd]).length + 2*c.length+3
  simp only [List.length_append,List.length_cons,List.length_nil,shifted_list]
  omega

private theorem map_length {n} (p : CNF n) :
    (body (p.map pad)).length = (body p).length + 2*occ p + 3*p.length := by
  induction p with
  | nil => rfl
  | cons c p ih =>
    change (emitClause (pad c) ++ body (p.map pad)).length =
      (emitClause c ++ body p).length + 2*(c.length+occ p)+3*(p.length+1)
    rw [List.length_append,List.length_append,pad_length,ih]
    omega

private theorem guards_length (n : Nat) : (body (guards n)).length = 12 := by
  rfl

theorem encoded_size {n} (p : CNF n) :
    (input (translate p)).length = (input p).length + n + 2*occ p + 3*p.length + 16 := by
  have h : body (translate p) = body (p.map pad) ++ body (guards n) := List.flatMap_append
  simp only [input,List.length_append,List.length_replicate,List.length_cons,List.length_nil,
    h,guards_length,map_length,width]
  omega

private theorem literals_fit {n} (c : Clausula n) : c.length ≤ (c.flatMap emitLit).length := by
  induction c with
  | nil => rfl
  | cons l c ih =>
    simp only [List.flatMap_cons,List.length_append,List.length_cons,emitLit,List.length_replicate,
      List.length_nil]
    omega

theorem linear_size {n} (p : CNF n) : (input (translate p)).length ≤ 4*(input p).length+16 := by
  have base : occ p + p.length ≤ (body p).length := by
    induction p with
    | nil => rfl
    | cons c p ih =>
      have h := literals_fit c
      change (c.length+occ p)+(p.length+1) ≤ ((c.flatMap emitLit ++ [Mark.clauseEnd]) ++ body p).length
      simp only [List.length_append,List.length_cons,List.length_nil]
      omega
  rw [encoded_size]
  simp only [input,List.length_append,List.length_replicate,List.length_cons,List.length_nil]
  omega

/-- Three finite control states. A step consumes one source symbol and writes
a bounded chunk to the separate output tape. Both heads only move right. -/
inductive Mode | header | first | inside
def openTags : List Mark := [.sign true,.tick,.sign true]
def chunk : Mark → List Mark
  | .tick => [.tick]
  | .sign b => [.tick,.tick,.sign b]
  | .clauseEnd => [.clauseEnd]
  | .headerEnd => [.headerEnd]
def nextMode : Mark → Mode
  | .clauseEnd => .first
  | _ => .inside
def step : Mode → Mark → Mode × List Mark
  | .header,.tick => (.header,[.tick,.tick])
  | .header,.headerEnd => (.first,[.tick,.tick,.tick,.tick,.headerEnd])
  | .header,_ => (.header,[])
  | .first,s => (nextMode s,openTags ++ chunk s)
  | .inside,s => (nextMode s,chunk s)

/-- At end-of-input the machine writes the fixed twelve-symbol suffix. -/
def scan : Mode → List Mark → List Mark
  | _,[] => body (guards 0)
  | m,s::xs =>
    let q := step m s
    q.2 ++ scan q.1 xs

private theorem begin_clause (xs : List Mark) (h : xs ≠ []) :
    scan .first xs = openTags ++ scan .inside xs := by
  cases xs with
  | nil => contradiction
  | cons s xs => rfl

private theorem scan_digits (k : Nat) (b₀ : Bool) (rest : List Mark) :
    scan .inside (List.replicate k .tick ++ .sign b₀ :: rest) =
      List.replicate (k+2) .tick ++ .sign b₀ :: scan .inside rest := by
  induction k with
  | zero => rfl
  | succ k ih => exact congrArg (List.cons Mark.tick) ih

private theorem scan_literal {n} (l : Literal n) (rest : List Mark) :
    scan .inside (emitLit l ++ rest) = emitLit (liftLit l) ++ scan .inside rest := by
  simpa only [emitLit,List.append_assoc,List.singleton_append,liftLit,shift,Fin.val_castAdd,
    Fin.val_succ] using scan_digits l.var.val l.pos rest

private theorem scan_inside {n} (c : Clausula n) (rest : List Mark) :
    scan .inside (c.flatMap emitLit ++ .clauseEnd :: rest) =
      (c.map liftLit).flatMap emitLit ++ .clauseEnd :: scan .first rest := by
  induction c with
  | nil => rfl
  | cons l c ih =>
    simp only [List.flatMap_cons,List.map_cons,List.append_assoc,scan_literal,ih]

private theorem scan_one {n} (c : Clausula n) (rest : List Mark) :
    scan .first (emitClause c ++ rest) = emitClause (pad c) ++ scan .first rest := by
  change scan .first ((c.flatMap emitLit ++ [Mark.clauseEnd]) ++ rest) = _
  rw [List.append_assoc]
  change scan .first (c.flatMap emitLit ++ .clauseEnd :: rest) = _
  rw [begin_clause _ (by simp),scan_inside]
  simp [emitClause,pad,emitLit,a,b,openTags,List.append_assoc]

private theorem scan_body {n} (p : CNF n) : scan .first (body p) = body (translate p) := by
  induction p with
  | nil => rfl
  | cons c p ih =>
    change scan .first (emitClause c ++ body p) = emitClause (pad c) ++ body (translate p)
    rw [scan_one,ih]

private theorem scan_header (k : Nat) (rest : List Mark) :
    scan .header (List.replicate k .tick ++ .headerEnd :: rest) =
      List.replicate (2*k+4) .tick ++ .headerEnd :: scan .first rest := by
  induction k with
  | zero => rfl
  | succ k ih =>
    change .tick :: .tick :: scan .header (List.replicate k .tick ++ .headerEnd :: rest) = _
    rw [ih,show 2*(k+1)+4 = (2*k+4)+1+1 by omega]
    rfl

theorem transduction {n} (p : CNF n) : scan .header (input p) = input (translate p) := by
  simp only [input,List.append_assoc,List.singleton_append,scan_header,scan_body]
  exact congrArg (fun k => List.replicate k Mark.tick ++ Mark.headerEnd :: body (translate p))
    (show 2*n+4 = width n by unfold width; omega)

/-- Count one right move for every symbol read or written, on the respective
tape. Finite-control steps and termination testing are separate from moves. -/
def moves : Mode → List Mark → Nat
  | _,[] => 12
  | m,s::xs =>
    let q := step m s
    1 + q.2.length + moves q.1 xs

theorem movement_identity (m : Mode) (xs : List Mark) :
    moves m xs = xs.length + (scan m xs).length := by
  induction xs generalizing m with
  | nil => rfl
  | cons s xs ih =>
    simp only [moves,scan,ih,List.length_cons,List.length_append]
    omega

theorem linear_head_moves {n} (p : CNF n) : moves .header (input p) ≤ 5*(input p).length+16 := by
  rw [movement_identity,transduction]
  have h := linear_size p
  omega

end IALD.CruzamentosUniversais
