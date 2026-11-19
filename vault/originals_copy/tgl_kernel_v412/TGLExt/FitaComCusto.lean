import TGLExt.PontePalavraVerbo
import TGLExt.OResumoEPsiBit

/- Uma fita de alfabeto fixo para cadeias de relações booleanas com uma
   cláusula global positiva em cada ponta. Cada símbolo contém a máscara de
   quatro bits de uma relação dada; nenhum símbolo contém a resposta da cadeia. -/
namespace IALD.FitaComCusto
open TGLExt.TraducaoTuring IALD.LeitorDaFormula

/-- Os quatro bits são as quatro entradas de uma tabela binária. -/
structure Mask where
  ff : Bool
  ft : Bool
  tf : Bool
  tt : Bool
deriving DecidableEq, Repr

def Mask.read (m : Mask) : Bool → Bool → Bool
  | false, false => m.ff
  | false, true => m.ft
  | true, false => m.tf
  | true, true => m.tt

def Mask.tab (f : Bool → Bool → Bool) : Mask :=
  ⟨f false false, f false true, f true false, f true true⟩

@[simp] theorem read_tab (f : Bool → Bool → Bool) (a b : Bool) :
    (Mask.tab f).read a b = f a b := by cases a <;> cases b <;> rfl

/-- Se a atribuição toma precisamente (a,b), a cláusula que proíbe (a,b) é falsa. -/
def ban {k : Nat} (a b : Bool) : Clausula (k+2) := [⟨0,!a⟩, ⟨1,!b⟩]

def look (r : Mask) : List (Bool × Bool) :=
  [(false,false),(false,true),(true,false),(true,true)].filter
    (fun p => !(r.read p.1 p.2))

def edgeCNF {k : Nat} (r : Mask) : CNF (k+2) :=
  (look r).map (fun p => ban p.1 p.2)

theorem edge_spec {k : Nat} (r : Mask) (x : Fin (k+2) → Bool) :
    passes (edgeCNF r) x = r.read (x 0) (x 1) := by
  obtain ⟨a,b,c,d⟩ := r
  cases a <;> cases b <;> cases c <;> cases d <;>
    cases hx : x 0 <;> cases hy : x 1 <;>
    simp [passes, edgeCNF, look, ban, Mask.read, satisfeita, Literal.vale, hx, hy]

def liftLit {n : Nat} (l : Literal n) : Literal (n+1) := ⟨l.var.succ,l.pos⟩

def liftCNF {n : Nat} (f : CNF n) : CNF (n+1) :=
  f.map (fun c => c.map liftLit)

@[simp] theorem lift_spec {n : Nat} (f : CNF n) (x : Fin (n+1) → Bool) :
    passes (liftCNF f) x = passes f (fun i => x i.succ) := by
  simp [passes, liftCNF, List.all_map, Function.comp_def, satisfeita, List.any_map,
    Literal.vale, liftLit]

def chain : (es : List Mask) → CNF (es.length+1)
  | [] => []
  | e :: es => edgeCNF e ++ liftCNF (chain es)

def someTrue {n : Nat} : Clausula n := (List.finRange n).map (fun i => ⟨i,true⟩)

theorem global_spec {n : Nat} (x : Fin n → Bool) :
    satisfeita someTrue x = true ↔ ∃ i, x i = true := by
  simp [satisfeita, someTrue, List.any_eq_true, Literal.vale, List.mem_finRange]

def formula (es : List Mask) : CNF (es.length+1) :=
  [someTrue] ++ chain es ++ [someTrue]

/-- Com as duas cláusulas globais, até a primeira fronteira contém toda variável. -/
theorem full_frontier (es : List Mask) :
    TGLExt.OResumoEPsiBit.fronteira (formula es) 1 = Finset.univ := by
  classical
  have hv : TGLExt.OResumoEPsiBit.varsClausula (@someTrue (es.length+1)) = Finset.univ := by
    ext i
    simp [TGLExt.OResumoEPsiBit.varsClausula, someTrue, List.mem_finRange]
  have hp : (formula es).take 1 = [someTrue] := rfl
  have ht : (formula es).drop 1 = chain es ++ [someTrue] := rfl
  unfold TGLExt.OResumoEPsiBit.fronteira
  rw [hp, ht]
  ext i
  have hs : i ∈ TGLExt.OResumoEPsiBit.varsClausula (@someTrue (es.length+1)) := by simp [hv]
  simp only [Finset.mem_inter, Finset.mem_univ, iff_true]
  exact ⟨TGLExt.OResumoEPsiBit.mem_varsDas_of_mem (by simp) hs,
    TGLExt.OResumoEPsiBit.mem_varsDas_of_mem (by simp) hs⟩

/-- Invariante de sufixo: a é o valor da primeira variável, seen registra
    se o prefixo anterior já continha um valor verdadeiro. -/
def Good (es : List Mask) (a seen : Bool) : Prop :=
  ∃ x : Fin (es.length+1) → Bool, x 0 = a ∧ passes (chain es) x = true ∧
    (seen = true ∨ ∃ i, x i = true)

theorem good_nil (a seen : Bool) : Good [] a seen ↔ seen = true ∨ a = true := by
  constructor
  · rintro ⟨x,h,_,h' | ⟨i,hi⟩⟩
    · exact Or.inl h'
    · have hzero : i = 0 := by
        apply Fin.ext
        have lim := i.isLt
        change i.val < 1 at lim
        change i.val = 0
        omega
      exact Or.inr (by simpa [hzero,h] using hi)
  · intro h
    refine ⟨fun _ => a, rfl,rfl,?_⟩
    exact h.imp_right (fun p => ⟨0,p⟩)

theorem passes_cons_chain (e : Mask) (es : List Mask)
    (x : Fin ((e :: es).length+1) → Bool) :
    passes (chain (e::es)) x =
      (e.read (x 0) (x 1) && passes (chain es) (fun i => x i.succ)) := by
  change passes (edgeCNF e ++ liftCNF (chain es)) x = _
  have split (g h : CNF (es.length+2)) :
      passes (g++h) x = (passes g x && passes h x) := List.all_append
  rw [split, edge_spec, lift_spec]

theorem good_cons (e : Mask) (es : List Mask) (a seen : Bool) :
    Good (e::es) a seen ↔ ∃ b, e.read a b = true ∧ Good es b (seen || a) := by
  constructor
  · rintro ⟨x,hx,hc,hs⟩
    rw [passes_cons_chain, Bool.and_eq_true, hx] at hc
    refine ⟨x 1,hc.1,fun i => x i.succ,rfl,hc.2,?_⟩
    rcases hs with hs | ⟨i,hi⟩
    · exact Or.inl (by simp [hs])
    · cases i using Fin.cases with
      | zero => exact Or.inl (by simp [← hx,hi])
      | succ j => exact Or.inr ⟨j,hi⟩
  · rintro ⟨b,hr,x,hx,hc,hs⟩
    refine ⟨Fin.cases a x,rfl,?_,?_⟩
    · rw [passes_cons_chain]
      change (e.read a (x 0) && passes (chain es) x) = true
      simp [hx,hr,hc]
    · rcases hs with hs | ⟨i,hi⟩
      · have either : seen = true ∨ a = true := by simpa using hs
        rcases either with h | h
        · exact Or.inl h
        · exact Or.inr ⟨0,h⟩
      · exact Or.inr ⟨i.succ,hi⟩

def base : Mask := Mask.tab (fun a seen => seen || a)

def advance (r s : Mask) : Mask := Mask.tab (fun a seen =>
  (r.read a false && s.read false (seen || a)) ||
  (r.read a true && s.read true (seen || a)))

def summary (es : List Mask) := es.foldr advance base

theorem summary_spec (es : List Mask) (a seen : Bool) :
    (summary es).read a seen = true ↔ Good es a seen := by
  induction es generalizing a seen with
  | nil => simp [summary,base,good_nil]
  | cons e es ih =>
    change (advance e (summary es)).read a seen = true ↔ _
    simp only [advance,read_tab,Bool.or_eq_true,Bool.and_eq_true,ih,good_cons]
    constructor
    · rintro (h | h)
      · exact ⟨false,h⟩
      · exact ⟨true,h⟩
    · rintro ⟨_ | _,h⟩
      · exact Or.inl h
      · exact Or.inr h

def finish (s : Mask) := s.read false false || s.read true false

theorem finish_spec (es : List Mask) : finish (summary es) = true ↔ SAT (formula es) := by
  rw [finish,Bool.or_eq_true,summary_spec,summary_spec,sat_iff]
  have H (x : Fin (es.length+1) → Bool) : passes (formula es) x = true ↔
      passes (chain es) x = true ∧ ∃ i, x i = true := by
    simp [formula, passes, List.all_append,Bool.and_eq_true,global_spec,and_comm]
  simp only [Good,Bool.false_eq_true,false_or,H]
  constructor
  · rintro (⟨x,_,hx⟩ | ⟨x,_,hx⟩) <;> exact ⟨x,hx⟩
  · rintro ⟨x,hx⟩
    cases h : x 0
    · exact Or.inl ⟨x,h,hx⟩
    · exact Or.inr ⟨x,h,hx⟩

/-- Semântica de pequenos passos de uma máquina de leitura unidirecional:
    a cabeça avança uma célula por passo e pára ao ler o branco. A metade
    já atravessada pode ser omitida porque a cabeça nunca retorna. -/
inductive Machine where
  | scanning (state : Mask) (unread : List Mask)
  | halted (answer : Bool)
deriving Repr

def step : Machine → Machine
  | .scanning s (e :: es) => .scanning (advance e s) es
  | .scanning s [] => .halted (finish s)
  | .halted ans => .halted ans

theorem exact_steps (cells : List Mask) (s : Mask) :
    step^[cells.length+1] (.scanning s cells) =
      .halted (finish (cells.foldl (fun q e => advance e q) s)) := by
  induction cells generalizing s with
  | nil => rfl
  | cons e es ih =>
    change step^[es.length+1+1] _ = _
    rw [Function.iterate_succ_apply]
    exact ih _

/-- A fita tem uma máscara por aresta (da direita para a esquerda), seguida
    de branco. Uma consulta à tabela finita de transição é um passo da cabeça.
    Leitura final com t acima do limiar pago da Palavra de `OPsibitEACompressao`. -/
theorem tape_reads_word (es : List Mask) (t : ℝ)
    (ht : ((es.length+1 : Nat) : ℝ) * Real.log 2 < t) :
    ∃ ans, step^[es.length+1] (.scanning base es.reverse) = .halted ans ∧
      (ans = true ↔ TGLExt.OPsibitEACompressao.palavra (custoCNF (formula es)) t) := by
  refine ⟨finish (summary es),?_,(finish_spec es).trans
    (TGLExt.OPsibitEACompressao.a_palavra_decide _ ht _)⟩
  simpa [summary, Function.flip_def] using exact_steps es.reverse base

/-- Sintaxe de entrada por cláusula local. O símbolo ban a b é a cláusula
    binária (Xᵢ ≠ a ∨ Xᵢ₊₁ ≠ b), com índices relativos à aresta atual.
    Uma sequência de positive representa, em ordem, os literais da cláusula
    global. As garantias são sobre fitas bem formadas emitidas por rawTape. -/
inductive Mark where
  | ban (a b : Bool)
  | closeEdge
  | positive
  | closeGlobal
deriving DecidableEq, Repr

def allAllowed : Mask := ⟨true,true,true,true⟩

def forbid (a b : Bool) (m : Mask) := Mask.tab (fun x y =>
  m.read x y && !((a == x) && (b == y)))

def erasePair (m : Mask) (p : Bool × Bool) := forbid p.1 p.2 m

def edgeMask (ps : List (Bool × Bool)) := ps.foldl erasePair allAllowed

theorem erasePair_spec (ps : List (Bool × Bool)) (m : Mask) (x y : Bool) :
    (ps.foldl erasePair m).read x y = true ↔
    m.read x y = true ∧ (x,y) ∉ ps := by
  induction ps generalizing m with
  | nil => simp
  | cons p ps ih =>
    obtain ⟨a,b⟩ := p
    simp only [List.foldl_cons,ih,erasePair,forbid,read_tab,Bool.and_eq_true]
    cases a <;> cases b <;> cases x <;> cases y <;> simp

structure Registers where
  feasible : Mask
  allowed : Mask

def readMark (st : Registers) : Mark → Registers
  | .ban a b => ⟨st.feasible, forbid a b st.allowed⟩
  | .closeEdge => ⟨advance st.allowed st.feasible, allAllowed⟩
  | .positive | .closeGlobal => st

def block (ps : List (Bool × Bool)) : List Mark :=
  ps.map (fun p => Mark.ban p.1 p.2) ++ [.closeEdge]

theorem read_block (ps : List (Bool × Bool)) (s : Mask) :
    (block ps).foldl readMark ⟨s,allAllowed⟩ = ⟨advance (edgeMask ps) s,allAllowed⟩ := by
  have H (qs : List (Bool × Bool)) (z : Registers) :
      (qs.map (fun p => Mark.ban p.1 p.2)).foldl readMark z =
      ⟨z.feasible,qs.foldl erasePair z.allowed⟩ := by
    induction qs generalizing z with
    | nil => cases z; rfl
    | cons p qs ih => exact ih _
  simp only [block,List.foldl_append,H,List.foldl_cons,List.foldl_nil,edgeMask]
  rfl

def chunk (n : Nat) := List.replicate n Mark.positive ++ [.closeGlobal]

theorem read_chunk (n : Nat) (z : Registers) : (chunk n).foldl readMark z = z := by
  have h (k : Nat) : (List.replicate k Mark.positive).foldl readMark z = z := by
    induction k with
    | zero => rfl
    | succ k ih => simpa [List.replicate_succ,readMark] using ih
  simp [chunk,h,readMark]

def rawTape (edges : List (List (Bool × Bool))) : List Mark :=
  chunk (edges.length+1) ++ edges.reverse.flatMap block ++ chunk (edges.length+1)

theorem scan_raw (edges : List (List (Bool × Bool))) :
    (rawTape edges).foldl readMark ⟨base,allAllowed⟩ =
      ⟨summary (edges.map edgeMask),allAllowed⟩ := by
  have h (ls : List (List (Bool × Bool))) (s : Mask) :
      (ls.flatMap block).foldl readMark ⟨s,allAllowed⟩ =
       ⟨(ls.map edgeMask).foldl (fun q e => advance e q) s,allAllowed⟩ := by
    induction ls generalizing s with
    | nil => rfl
    | cons p ps ih =>
      simp only [List.flatMap_cons,List.foldl_append,read_block,List.map_cons,List.foldl_cons]
      exact ih _
  simp [rawTape,read_chunk,h,List.map_reverse,summary]

inductive RawMachine where
  | scanning (state : Registers) (unread : List Mark)
  | halted (answer : Bool)

def rawStep : RawMachine → RawMachine
  | .scanning s (c :: cs) => .scanning (readMark s c) cs
  | .scanning s [] => .halted (finish s.feasible)
  | .halted b => .halted b

theorem raw_steps (cs : List Mark) (s : Registers) :
    rawStep^[cs.length+1] (.scanning s cs) =
       .halted (finish (cs.foldl readMark s).feasible) := by
  induction cs generalizing s with
  | nil => rfl
  | cons c cs ih =>
    change rawStep^[cs.length+1+1] _ = _
    rw [Function.iterate_succ_apply]
    exact ih _

/-- Custo na fita escrita em cláusulas, sem fornecer a tabela de cada aresta.
    O comprimento é contado em símbolos de um alfabeto finito fixo. -/
theorem clause_tape_reads_word (edges : List (List (Bool × Bool))) (t : ℝ)
    (ht : ((edges.length+1 : Nat) : ℝ) * Real.log 2 < t) :
    ∃ ans, rawStep^[(rawTape edges).length+1] (.scanning ⟨base,allAllowed⟩ (rawTape edges)) =
      .halted ans ∧ (ans = true ↔
        TGLExt.OPsibitEACompressao.palavra (custoCNF (formula (edges.map edgeMask))) t) := by
  refine ⟨finish (summary (edges.map edgeMask)),?_, (finish_spec _).trans
    (TGLExt.OPsibitEACompressao.a_palavra_decide _ (by simpa using ht) _)⟩
  rw [raw_steps,scan_raw]

theorem boundary_cell_count (es : List Mask) :
    Fintype.card (↥(TGLExt.OResumoEPsiBit.fronteira (formula es) 1) → Bool) =
      2 ^ (es.length+1) := by
  rw [TGLExt.OResumoEPsiBit.a_fronteira_tem_duas_elevado_as_celulas,full_frontier,
    Finset.card_univ,Fintype.card_fin]

/-- Para cada valor do indicador histórico a tabela possui exatamente o par
    de sinais realizável pelos dois canais do PsiBit. O leitor discreto da
    fita acima não exige construir ou aproximar um ângulo real. -/
theorem feasible_pair_on_orbit (es : List Mask) (seen : Bool) :
    ∃ θ : ℝ,
      ((TGLExt.Psibit.codeAmp θ).word = 1 ↔ Good es false seen) ∧
      ((TGLExt.Psibit.codeAmp θ).verb = 1 ↔ Good es true seen) := by
  have nz (b : Bool) : bitSign b ≠ 0 := by cases b <;> decide
  have sign (b : Bool) : bitSign b = 1 ↔ b = true := by cases b <;> decide
  obtain ⟨θ,h₀,h₁⟩ := TGLExt.Psibit.the_orbit_visits_all_four_states _ _
    (nz ((summary es).read false seen)) (nz ((summary es).read true seen))
  refine ⟨θ,?_,?_⟩
  · rw [h₀,sign,summary_spec]
  · rw [h₁,sign,summary_spec]

theorem raw_prefix (pre rest : List Mark) (s : Registers) :
    rawStep^[pre.length] (.scanning s (pre ++ rest)) =
      .scanning (pre.foldl readMark s) rest := by
  induction pre generalizing s with
  | nil => rfl
  | cons c cs ih =>
    change rawStep^[cs.length+1] _ = _
    rw [Function.iterate_succ_apply]
    exact ih _

/-- Mesmo comprimento, mesma fronteira cheia. Na primeira instância a aresta
    só admite (0,0) e conflita com a cláusula global. Na segunda só admite
    (0,1), o que satisfaz a cláusula global. -/
theorem mixed_examples :
    ¬ SAT (formula [⟨true,false,false,false⟩]) ∧
      SAT (formula [⟨false,true,false,false⟩]) := by
  constructor
  · rw [← finish_spec]
    decide
  · rw [← finish_spec]
    decide

end IALD.FitaComCusto
