import TGLExt.PolinomioPorEscolha
import TGLExt.BuscaEmCruzamentos
import Mathlib.Tactic.DeriveFintype

/- Leitor de uma passagem sobre a codificação unária original. Guarda somente
   quatro sinais de contradição, o estado da cláusula atual e um contador
   saturado de zeros. A ordem interna 0,1 OU 1,0 é admitida. -/
namespace IALD.GuardasNaFita
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula IALD.LeitorDaFormula
open Codex.PolinomioPorEscolha (Letter spell spellClause original)
open IALD.CruzamentosUniversais (guardClause guards)

inductive Rank where | zero | one | many
deriving DecidableEq, Fintype, Repr

def rank : Nat → Rank
  | 0 => .zero | 1 => .one | _+2 => .many

def inc : Rank → Rank | .zero => .one | _ => .many

theorem inc_rank (n : Nat) : inc (rank n) = rank (n+1) := by
  cases n with | zero => rfl | succ n => cases n <;> rfl

inductive Phase where
  | empty | firstZero (p : Bool) | firstOne (q : Bool)
  | both (p q : Bool) | other
deriving DecidableEq, Fintype, Repr

def addLit : Phase → Rank → Bool → Phase
  | .empty,.zero,b => .firstZero b
  | .empty,.one,b => .firstOne b
  | .firstZero p,.one,q => .both p q
  | .firstOne q,.zero,p => .both p q
  | _,_,_ => .other

structure Marks where
  ff : Bool
  ft : Bool
  tf : Bool
  tt : Bool
deriving DecidableEq, Fintype, Repr

def blank : Marks := ⟨false,false,false,false⟩
def seen (m : Marks) : Bool → Bool → Bool
  | false,false => m.ff | false,true => m.ft | true,false => m.tf | true,true => m.tt

def flag (m : Marks) : Option (Bool × Bool) → Marks
  | some (false,false) => {m with ff:=true}
  | some (false,true) => {m with ft:=true}
  | some (true,false) => {m with tf:=true}
  | some (true,true) => {m with tt:=true}
  | none => m

def extract : Phase → Option (Bool × Bool) | .both a b => some (a,b) | _ => none

structure Registers where
  phase : Phase
  count : Rank
  marks : Marks
deriving DecidableEq, Fintype, Repr

def init (m : Marks) : Registers := ⟨.empty,.zero,m⟩

def next (s : Registers) : Letter → Registers
  | .tick => {s with count := inc s.count}
  | .sign b => ⟨addLit s.phase s.count b,.zero,s.marks⟩
  | .delimiter => init (flag s.marks (if s.count = .zero then extract s.phase else none))

theorem finite_control : Fintype.card Registers = 480 := by
  let e : Registers ≃ Phase × Rank × Marks :=
    ⟨fun s => (s.phase,s.count,s.marks),fun s => ⟨s.1,s.2.1,s.2.2⟩,
      fun _ => rfl,fun _ => rfl⟩
  have hp : Fintype.card Phase = 10 := by decide
  have hr : Fintype.card Rank = 3 := by decide
  have hm : Fintype.card Marks = 16 := by decide
  rw [Fintype.card_congr e,Fintype.card_prod,Fintype.card_prod,hp,hr,hm]

def finish (m : Marks) := m.ff && m.ft && m.tf && m.tt

inductive Machine where | walk (s : Registers) (unread : List Letter) | halt (detected : Bool)

def step : Machine → Machine
  | .walk s (c::cs) => .walk (next s c) cs
  | .walk s [] => .halt (finish s.marks)
  | .halt b => .halt b

theorem exact_steps (w : List Letter) (s : Registers) :
    step^[w.length+1] (.walk s w) = .halt (finish (w.foldl next s).marks) := by
  induction w generalizing s with
  | nil => rfl
  | cons a w ih =>
    change step^[w.length+1+1] _ = _
    rw [Function.iterate_succ_apply]
    exact ih _

def addName {n} (s : Phase) (l : Literal n) := addLit s (rank l.var.val) l.pos

theorem unary (i : Nat) (p : Phase) (m : Marks) :
    (List.replicate i Letter.tick).foldl next ⟨p,.zero,m⟩ = ⟨p,rank i,m⟩ := by
  induction i with
  | zero => rfl
  | succ i ih =>
    rw [List.replicate_succ',List.foldl_append,ih]
    change Registers.mk p (inc (rank i)) m = _
    rw [inc_rank]

theorem literal_read {n} (l : Literal n) (p : Phase) (m : Marks) :
    (spell l).foldl next ⟨p,.zero,m⟩ = ⟨addName p l,.zero,m⟩ := by
  simp only [spell,List.foldl_append,unary]; rfl

theorem read_literals {n} (c : Clausula n) (p : Phase) (m : Marks) :
    (c.flatMap spell).foldl next ⟨p,.zero,m⟩ = ⟨c.foldl addName p,.zero,m⟩ := by
  induction c generalizing p with
  | nil => rfl
  | cons l c ih => simp only [List.flatMap_cons,List.foldl_append,literal_read,ih,List.foldl_cons]

def signature {n} : Clausula n → Option (Bool × Bool)
  | [l,r] =>
    match rank l.var.val,rank r.var.val with
    | .zero,.one => some (l.pos,r.pos)
    | .one,.zero => some (r.pos,l.pos)
    | _,_ => none
  | _ => none

theorem other_absorbs {n} (cs : Clausula n) : cs.foldl addName .other = .other := by
  induction cs with
  | nil => rfl
  | cons a cs ih => exact ih

theorem parse_signature {n} (c : Clausula n) :
    extract (c.foldl addName .empty) = signature c := by
  rcases c with _ | ⟨a,as⟩
  · rfl
  rcases as with _ | ⟨b,bs⟩
  · cases e : rank a.var.val <;> simp [List.foldl,addName,e,addLit,extract,signature]
  rcases bs with _ | ⟨c,cs⟩
  · cases e : rank a.var.val <;> cases f : rank b.var.val <;>
      simp [List.foldl,addName,e,f,addLit,extract,signature]
  · cases e : rank a.var.val <;> cases f : rank b.var.val <;>
      simp [addName,e,f,addLit,other_absorbs,extract,signature]

theorem clause_read {n} (c : Clausula n) (m : Marks) :
    (spellClause c).foldl next (init m) = init (flag m (signature c)) := by
  simp only [spellClause,init,List.foldl_append,read_literals,List.foldl_cons,List.foldl_nil,next,
    if_true,parse_signature]

def collect {n} (p : CNF n) (m : Marks) := p.foldl (fun s c => flag s (signature c)) m

theorem tape_read {n} (p : CNF n) (m : Marks) :
    (original p).foldl next (init m) = init (collect p m) := by
  induction p generalizing m with
  | nil => rfl
  | cons c p ih =>
    change (spellClause c ++ original p).foldl next _ = _
    rw [List.foldl_append,clause_read,ih]; rfl

theorem flag_spec (m : Marks) (v : Option (Bool × Bool)) (a b : Bool) :
    seen (flag m v) a b = true ↔ seen m a b = true ∨ v = some (a,b) := by
  rcases v with _ | ⟨x,y⟩
  · simp [flag]
  · cases x <;> cases y <;> cases a <;> cases b <;> simp [seen,flag]

theorem collect_spec {n} (p : CNF n) (m : Marks) (a b : Bool) :
    seen (collect p m) a b = true ↔ seen m a b = true ∨ ∃ c ∈ p, signature c = some (a,b) := by
  induction p generalizing m with
  | nil => simp [collect]
  | cons c p ih =>
    change seen (collect p (flag m (signature c))) a b = true ↔ _
    rw [ih,flag_spec]
    simp only [List.mem_cons]
    grind

def detects {n} (p : CNF n) := finish (collect p blank)

theorem detect_exact {n} (p : CNF n) :
    detects p = true ↔ ∀ a b, ∃ c ∈ p, signature c = some (a,b) := by
  have test (a b : Bool) : seen (collect p blank) a b = true ↔
      ∃ c ∈ p, signature c = some (a,b) := by
    rw [collect_spec]; cases a <;> cases b <;> simp [seen,blank]
  constructor
  · intro h a b
    have hs : ((seen (collect p blank) false false = true ∧ seen (collect p blank) false true = true)
      ∧ seen (collect p blank) true false = true) ∧ seen (collect p blank) true true = true := by
      simpa only [detects,finish,Bool.and_eq_true,seen] using h
    cases a <;> cases b
    · exact (test _ _).mp hs.1.1.1
    · exact (test _ _).mp hs.1.1.2
    · exact (test _ _).mp hs.1.2
    · exact (test _ _).mp hs.2
  · intro h
    simp only [detects,finish,Bool.and_eq_true]
    exact ⟨⟨⟨(test false false).mpr (h _ _),(test false true).mpr (h _ _)⟩,
      (test true false).mpr (h _ _)⟩,(test true true).mpr (h _ _)⟩

theorem tape_detects {n} (p : CNF n) :
    step^[(original p).length+1] (.walk (init blank) (original p)) = .halt (detects p) := by
  rw [exact_steps,tape_read]; rfl

def atName {n} (x : Fin n → Bool) (k : Nat) : Bool := if h : k < n then x ⟨k,h⟩ else false

theorem at_index {n} (x : Fin n → Bool) (i : Fin n) : atName x i.val = x i := by
  simp [atName,i.isLt]

theorem coords (k : Nat) : (rank k = .zero ↔ k=0) ∧ (rank k = .one ↔ k=1) := by
  cases k with | zero => decide | succ k => cases k <;> simp [rank]

theorem signature_sat {n} (c : Clausula n) (a b : Bool) (x : Fin n → Bool)
    (hs : signature c = some (a,b)) (hx : satisfeita c x = true) :
    atName x 0 = a ∨ atName x 1 = b := by
  rcases c with _ | ⟨l,ls⟩
  · contradiction
  rcases ls with _ | ⟨r,rs⟩
  · contradiction
  rcases rs with _ | ⟨s,ss⟩
  · cases e : rank l.var.val <;> cases f : rank r.var.val <;> simp [signature,e,f] at hs
    · have hl := (coords _).1.mp e
      have hr := (coords _).2.mp f
      have h₀ : atName x 0 = x l.var := hl ▸ at_index x l.var
      have h₁ : atName x 1 = x r.var := hr ▸ at_index x r.var
      simpa [satisfeita,Literal.vale,h₀,h₁,← hs.1,← hs.2] using hx
    · have hl := (coords _).2.mp e
      have hr := (coords _).1.mp f
      have h₀ : atName x 0 = x r.var := hr ▸ at_index x r.var
      have h₁ : atName x 1 = x l.var := hl ▸ at_index x l.var
      simpa [satisfeita,Literal.vale,h₀,h₁,← hs.1,← hs.2,or_comm] using hx
  · contradiction

theorem detection_safe {n} (p : CNF n) (h : detects p = true) : ¬ SAT p := by
  rintro ⟨x,hx⟩
  obtain ⟨c,hc,hs⟩ := (detect_exact p).mp h (!(atName x 0)) (!(atName x 1))
  have bad := signature_sat c _ _ x hs (hx c hc)
  cases h₀ : atName x 0 <;> cases h₁ : atName x 1 <;> simp [h₀,h₁] at bad

theorem detects_family (n : Nat) : detects (IALD.BuscaEmCruzamentos.family n) = true := by
  apply (detect_exact _).mpr
  intro p q
  have guards_mem (c : Clausula (IALD.CruzamentosUniversais.width n)) (h : c ∈ guards n) :
      c ∈ IALD.BuscaEmCruzamentos.family n := List.mem_append_right _ h
  cases p <;> cases q
  · exact ⟨guardClause n false false,guards_mem _ (by simp [guards]),rfl⟩
  · exact ⟨guardClause n false true,guards_mem _ (by simp [guards]),rfl⟩
  · exact ⟨guardClause n true false,guards_mem _ (by simp [guards]),rfl⟩
  · refine ⟨IALD.CruzamentosUniversais.pad ([] : Clausula n),?_,rfl⟩
    apply List.mem_append_left
    exact List.mem_cons_self

theorem family_steps (n : Nat) :
    let p := IALD.BuscaEmCruzamentos.family n
    step^[(original p).length+1] (.walk (init blank) (original p)) = .halt true := by
  dsimp only
  rw [tape_detects,detects_family]

end IALD.GuardasNaFita
