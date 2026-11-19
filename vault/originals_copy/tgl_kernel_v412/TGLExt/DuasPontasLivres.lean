import TGLExt.UmaChaveAngular

/-! A fresh last clause can constrain both old free endpoints. A delayed
finite register remembers the relation before the current clause without
requiring a boundary marker or a rewind of the original flat tape. -/
set_option autoImplicit false
namespace Codex.ClosingEdge
open TGLExt.TraducaoTuring IALD.LeitorDaFormula Codex.PolinomioPorEscolha
open Codex.ChainTape Codex.OrthantRelation

structure Buffer where
  walk : ChainTape.Reg
  base : Table
  signs : Row
  last : Table

def initial : Buffer := ⟨clean freshKey,idTable,(false,false),idTable⟩

def push (s : Buffer) (a : Letter) : Buffer :=
  let next := see s.walk a
  match a with
  | .tick => {s with walk := next}
  | .sign b => {s with walk := next, signs := (s.signs.2,b)}
  | .delimiter => ⟨next,committed next.acc,(false,false),both s.base (clauseTable s.signs)⟩

/-- Advancing the head consumes exactly its current cell. All registers
have constant finite size, including the saved pre-clause table. -/
def run (s : Buffer) : List Letter → Table × Nat
  | [] => (s.last,0)
  | a::w => let (out,k) := run (push s a) w; (out,k+1)

theorem movement (w : List Letter) (s : Buffer) :
    run s w = ((w.foldl push s).last,w.length) := by
  induction w generalizing s with
  | nil => rfl
  | cons a w ih => simp [run,ih]

private theorem walking (w : List Letter) (s : Buffer) :
    (w.foldl push s).walk = w.foldl see s.walk := by
  induction w generalizing s with
  | nil => rfl
  | cons a w ih =>
    change (w.foldl push (push s a)).walk = w.foldl see (see s.walk a)
    rw [ih]
    cases a <;> rfl

private theorem boundary {n : Nat} (p : CNF n) (s : Buffer) (base : s.base = committed s.walk.acc) :
    ((original p).foldl push s).base = committed ((original p).foldl push s).walk.acc := by
  induction p generalizing s with
  | nil => exact base
  | cons c p ih =>
    change ((spellClause c ++ original p).foldl push s).base = _
    simp only [original,List.flatMap_cons,List.foldl_append] at *
    apply ih
    simp [spellClause,List.foldl_append,push]

private theorem ticks (n : Nat) (s : Buffer) :
    ((List.replicate n Letter.tick).foldl push s).base = s.base ∧
    ((List.replicate n Letter.tick).foldl push s).signs = s.signs := by
  induction n generalizing s with
  | zero => exact ⟨rfl,rfl⟩
  | succ n ih =>
    rw [List.replicate_succ]
    exact ih (push s .tick)

private theorem end_clause {n : Nat} (i j : Fin n) (b : Row) (s : Buffer) :
    ((spellClause (edge i j b)).foldl push s).last = both s.base (clauseTable b) := by
  obtain ⟨u,v⟩ := b
  simp only [spellClause,edge,List.flatMap_cons,List.flatMap_nil,List.append_nil,
    spell,List.foldl_append,List.foldl_cons,List.foldl_nil,push,ticks]

private theorem closed_visible {n : Nat} (p : CNF n) (i j : Fin n) (u v : Bool) (signs : Row) :
    visible (p++[edge i j signs]) i j u v ↔
      visible p i j u v ∧ ((u == signs.1) || (v == signs.2)) = true := by
  constructor
  · rintro ⟨x,xi,xj,h⟩
    have hp := List.all_eq_true.mp h
    have hc := hp (edge i j signs) (by simp)
    refine ⟨⟨x,xi,xj,List.all_eq_true.mpr (fun c hc => hp c (by simp [hc]))⟩,?_⟩
    simpa [satisfeita,edge,Literal.vale,xi,xj] using hc
  · rintro ⟨⟨x,xi,xj,h⟩,cl⟩
    refine ⟨x,xi,xj,?_⟩
    have he : satisfeita (edge i j signs) x = true := by
      simpa [satisfeita,edge,Literal.vale,xi,xj] using cl
    apply List.all_eq_true.mpr
    intro c hc
    rcases List.mem_append.mp hc with hp|last
    · exact List.all_eq_true.mp h _ hp
    · simpa only [List.mem_singleton.mp last] using he

theorem closed_path {n : Nat} {i j : Fin n} {p : CNF n} (h : Path i p j) (signs : Row) :
    let q := p ++ [edge i j signs]
    let wire := original q
    (run initial wire).2 = wire.length ∧ ∀ u v,
      getBit (run initial wire).1 u v = true ↔ visible q i j u v := by
  obtain ⟨a,walk,_,ok⟩ := path_table h
  have hb := boundary p initial rfl
  rw [walking] at hb
  change _ = committed ((original p).foldl see (clean freshKey)).acc at hb
  rw [walk] at hb
  dsimp only
  rw [movement]
  refine ⟨rfl,?_⟩
  intro u v
  have split : original (p++[edge i j signs]) = original p ++ spellClause (edge i j signs) := by
    simp [original]
  rw [split,List.foldl_append,end_clause,hb,closed_visible]
  simp only [both,get_tab,clauseTable,Bool.and_eq_true]
  exact and_congr (ok u v) Iff.rfl

theorem closed_reception {n : Nat} {i j : Fin n} {p : CNF n} (h : Path i p j) (signs : Row)
    (z : ℚ) (k : ℤ) :
    let q := p ++ [edge i j signs]
    let table := (run initial (original q)).1
    |z-(turn (phaseTag table)+k)| < 1/32 → ∀ u v,
      atBit (fromPhase (Codex.SinglePhase.slice z)) u v = true ↔ visible q i j u v := by
  dsimp only
  intro noise u v
  rw [Codex.SinglePhase.receives _ _ _ noise,phase_roundtrip]
  exact (closed_path h signs).2 u v

theorem closing_example :
    let signs := fun (i : Nat) =>
      if i=0 then ((false,true),[(true,false)]) else ((true,true),[(false,false)])
    let path := ladder (n:=3) signs 2 (by decide)
    let last := edge (0:Fin 3) (2:Fin 3) (true,false)
    run initial (original (path++[last])) = (((false,false),(true,false)),25) := by decide

end Codex.ClosingEdge
