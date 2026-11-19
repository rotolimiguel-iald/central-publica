import TGLExt.GuardasNaFita
import TGLExt.CaudaDisjunta

/-! A sound three-way scan of the original flat input: a positive witness, a
contradictory quartet, or unknown. In the last case the formula is still needed. -/
set_option autoImplicit false
namespace Codex.FastScan
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula
open Codex.PolinomioPorEscolha IALD.LeitorDaFormula
open IALD.GuardasNaFita (Registers blank init next)

structure State where
  guards : Registers
  clausesOK : Bool
  hasPositive : Bool

def consume (s : State) (a : Letter) : State :=
  match a with
  | .tick => ⟨next s.guards a,s.clausesOK,s.hasPositive⟩
  | .sign b => ⟨next s.guards a,s.clausesOK,s.hasPositive || b⟩
  | .delimiter => ⟨next s.guards a,s.clausesOK && s.hasPositive,false⟩

def start : State := ⟨init blank,true,false⟩
def finish (s : State) : Option Bool :=
  if IALD.GuardasNaFita.finish s.guards.marks then some false
  else if s.clausesOK then some true else none

def guards_proj (w : List Letter) (s : State) :
    (w.foldl consume s).guards = w.foldl next s.guards := by
  induction w generalizing s with
  | nil => rfl
  | cons a w ih =>
    simp only [List.foldl_cons,ih]
    cases a <;> rfl

def pairStep (s : Bool × Bool) : Letter → Bool × Bool
  | .tick => s
  | .sign b => (s.1,s.2 || b)
  | .delimiter => (s.1 && s.2,false)

theorem witness_proj (w : List Letter) (s : State) :
    ((w.foldl consume s).clausesOK,(w.foldl consume s).hasPositive) =
      w.foldl pairStep (s.clausesOK,s.hasPositive) := by
  induction w generalizing s with
  | nil => rfl
  | cons a w ih =>
    simp only [List.foldl_cons,ih]
    cases a <;> rfl

private theorem ticks (k : Nat) (s : Bool × Bool) :
    (List.replicate k Letter.tick).foldl pairStep s = s := by
  induction k with
  | zero => rfl
  | succ k ih => simp [List.replicate_succ,pairStep,ih]

private theorem lits {n} (c : Clausula n) (a b : Bool) :
    (c.flatMap spell).foldl pairStep (a,b) =
      (a,b || satisfeita c (fun _ => true)) := by
  induction c generalizing b with
  | nil => simp [satisfeita]
  | cons l c ih =>
    simp only [List.flatMap_cons,spell,List.foldl_append,ticks,List.foldl_cons,List.foldl_nil,pairStep]
    rw [ih]
    cases h : l.pos <;> simp [satisfeita,Literal.vale,h]

private theorem encoded {n} (p : CNF n) (a : Bool) :
    (original p).foldl pairStep (a,false) = (a && passes p (fun _ => true),false) := by
  induction p generalizing a with
  | nil => simp [original,passes]
  | cons c p ih =>
    change ((c.flatMap spell ++ [Letter.delimiter]) ++ original p).foldl pairStep _ = _
    simp only [List.foldl_append,lits,List.foldl_cons,List.foldl_nil,pairStep,Bool.false_or,ih]
    simp [passes,Bool.and_assoc]

def answer (w : List Letter) := finish (w.foldl consume start)
inductive Machine where
  | walk (state : State) (input : List Letter)
  | halt (out : Option Bool)

def step : Machine → Machine
  | .walk s (a::as) => .walk (consume s a) as
  | .walk s [] => .halt (finish s)
  | .halt v => .halt v

theorem one_pass (w : List Letter) (s : State) :
    step^[w.length+1] (.walk s w) = .halt (finish (w.foldl consume s)) := by
  induction w generalizing s with
  | nil => rfl
  | cons a w ih =>
    change step^[w.length+1+1] _ = _
    rw [Function.iterate_succ_apply]
    exact ih _

theorem fast_spec {n} (p : CNF n) :
    answer (original p) = if IALD.GuardasNaFita.detects p then some false else
      if passes p (fun _ => true) then some true else none := by
  have h := congrArg Prod.fst (witness_proj (original p) start)
  change ((original p).foldl consume start).clausesOK =
    ((original p).foldl pairStep (true,false)).1 at h
  rw [encoded] at h
  simp only [Bool.true_and] at h
  unfold answer finish
  rw [guards_proj,h]
  rw [show start.guards = init blank from rfl,IALD.GuardasNaFita.tape_read]
  rfl

theorem fast_sound {n} (p : CNF n) (b : Bool) (h : answer (original p) = some b) :
    palavraDaFormula p = b := by
  rw [fast_spec] at h
  split at h
  next det =>
    cases Option.some.inj h
    apply Bool.eq_false_iff.mpr
    exact fun yes => IALD.GuardasNaFita.detection_safe p det ((a_palavra_e_o_sat _).mp yes)
  next no =>
    split at h
    next witness =>
      cases Option.some.inj h
      exact (a_palavra_e_o_sat _).mpr ((sat_iff _).mpr ⟨_,witness⟩)
    next => contradiction

theorem guarded_family (m : Nat) :
    answer (original (IALD.BuscaEmCruzamentos.family m)) = some false := by
  rw [fast_spec,IALD.GuardasNaFita.detects_family]
  rfl

theorem disjoint_family (m : Nat) :
    answer (original (Codex.CaudaDisjunta.disjointCNF m)) = some true := by
  let p := Codex.CaudaDisjunta.disjointCNF m
  have yes : passes p (fun _ => true) = true := by
    apply List.all_eq_true.mpr
    intro c hc
    obtain ⟨i,_,rfl⟩ := List.mem_map.mp hc
    simp [Codex.CaudaDisjunta.pairClause,satisfeita,Literal.vale]
  have no : IALD.GuardasNaFita.detects p = false := by
    apply Bool.eq_false_iff.mpr
    exact fun hit => IALD.GuardasNaFita.detection_safe p hit ((sat_iff _).mpr ⟨_,yes⟩)
  change answer (original p) = some true
  rw [fast_spec,no,yes]
  rfl

end Codex.FastScan
