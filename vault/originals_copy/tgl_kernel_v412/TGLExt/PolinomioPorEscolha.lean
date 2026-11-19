import TGLExt.EscolhasGlobais
import TGLExt.FechoNaFita

/- Uma entrada plana unária: tick repetido i vezes e uma letra de sinal por
   literal de índice i, mais um terminador por cláusula. O programa Horn
   fornecido como escolha cabe no comprimento desta entrada. Verificá-lo
   tem custo de fita delimitado. Obter/verificar a seleção a partir das duas
   fitas (a fórmula e um candidato), ou buscar uma boa escolha, é outra etapa. -/
set_option autoImplicit false
namespace Codex.PolinomioPorEscolha
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula Codex.CrossSelectors Codex.HornCross
open Codex.SparseHornTape
variable {n : Nat}

inductive Letter where
  | tick | sign (positive : Bool) | delimiter
deriving DecidableEq, Repr

def spell (l : Literal n) : List Letter := List.replicate l.var.val .tick ++ [.sign l.pos]
def spellClause (c : Clausula n) := c.flatMap spell ++ [.delimiter]
def original (p : CNF n) := p.flatMap spellClause

def weight (xs : List (Fin n)) : Nat := (xs.map (fun i => i.val+1)).sum

theorem arg_length (i : Fin n) (s : Sym) : (arg i s).length = i.val+1 := by simp [arg]

theorem args_length (xs : List (Fin n)) : (args xs).length = weight xs := by
  induction xs with
  | nil => rfl
  | cons i xs ih =>
    change (arg i .need ++ args xs).length = (i.val+1)+weight xs
    rw [List.length_append,arg_length,ih]

theorem weight_member (xs : List (Fin n)) (i : Fin n) (h : i ∈ xs) :
    i.val+1 ≤ weight xs := by
  induction xs with
  | nil => simp at h
  | cons x xs ih =>
    change _ ≤ (x.val+1) + weight xs
    rcases List.mem_cons.mp h with h|h
    · subst x; omega
    · have := ih h; omega

theorem sign_partition (c : Clausula n) :
    weight (names c false)+weight (names c true) = (c.flatMap spell).length := by
  induction c with
  | nil => rfl
  | cons l c ih =>
    obtain ⟨i,b⟩ := l
    cases b <;>
      simp [names,weight,spell] at ih ⊢ <;> omega

theorem alternative_length (c : Clausula n) (r : Rule n) (hr : r ∈ alternatives c) :
    (line r).length ≤ (spellClause c).length := by
  have part := sign_partition c
  unfold alternatives at hr
  cases h : names c true with
  | nil =>
    simp [h] at hr
    subst r
    have empty : weight (names c true) = 0 := by rw [h]; rfl
    change (args (names c false) ++ [Sym.deny]).length ≤ (c.flatMap spell ++ [Letter.delimiter]).length
    simp only [List.length_append,args_length,List.length_cons,List.length_nil]
    omega
  | cons i is =>
    simp only [h,List.mem_map] at hr
    obtain ⟨j,hj,rfl⟩ := hr
    have hw := weight_member (names c true) j (by simpa only [h] using hj)
    change (args (names c false) ++ arg j .setBit).length ≤ (c.flatMap spell ++ [Letter.delimiter]).length
    simp only [List.length_append,args_length,arg_length,List.length_cons,List.length_nil]
    omega

theorem selected_length (p : CNF n) (q : List (Rule n)) (hq : q ∈ programs p) :
    (program q).length ≤ (original p).length := by
  induction p generalizing q with
  | nil => simp [programs] at hq; subst q; rfl
  | cons c p ih =>
    simp only [programs,List.mem_flatMap,List.mem_map] at hq
    obtain ⟨r,hr,v,hv,rfl⟩ := hq
    change (line r ++ program v).length ≤ (spellClause c ++ original p).length
    simp only [List.length_append]
    exact Nat.add_le_add (alternative_length _ _ hr) (ih _ hv)

theorem halt_persists (c : Cfg) (b : Bool) (h : c.mode = .halt b) (k : Nat) :
    run k c = c := by
  have fixed : step c = c := by simp [step,h]
  induction k with
  | zero => rfl
  | succ k ih => simp [run,fixed,ih]

theorem halt_unique (c : Cfg) (k j : Nat) (a b : Bool) (ha : (run k c).mode = .halt a)
    (hb : (run j c).mode = .halt b) : a = b := by
  have h₁ : (run (k+j) c).mode = .halt a := by rw [run_add,halt_persists _ _ ha,ha]
  have h₂ : (run (j+k) c).mode = .halt b := by rw [run_add,halt_persists _ _ hb,hb]
  rw [Nat.add_comm k j] at h₁
  exact Mode.halt.inj (h₁.symm.trans h₂)

def budget (L : Nat) := (L+1)*(3*L+2)

theorem budget_le (u v : Nat) (h : u ≤ v) : budget u ≤ budget v :=
  Nat.mul_le_mul (by omega) (by omega)

/-- O limite vale para TODAS as escolhas: a máquina responde
    sim ou não em função da Palavra de cada programa selecionado. -/
theorem every_candidate (p : CNF n) (q : List (Rule n)) (hq : q ∈ programs p) :
    ∃ T ≤ budget (original p).length,
      travel T (start q ∅) ≤ 2 * budget (original p).length ∧
      (run T (start q ∅)).mode = .halt (checkProgram q) := by
  obtain ⟨T,ht,move,answer⟩ := sparse_horn_tape q
  have bound := budget_le _ _ (selected_length p q hq)
  exact ⟨T,ht.trans bound,move.trans (Nat.mul_le_mul_left _ bound),
    answer.trans (congrArg Mode.halt (horn_word q).symm)⟩

/-- Exatidão existencial para CADA CNF. A máquina determinista aqui verificada
    parte da fita do candidato q. A condição q ∈ programs p pertence à relação
    matemática entre a entrada e a escolha; não é uma checagem gratuita da máquina. -/
theorem word_iff_bounded_selection (p : CNF n) :
    palavraDaFormula p = true ↔
      ∃ q ∈ programs p, (program q).length ≤ (original p).length ∧
        ∃ T ≤ budget (original p).length,
          travel T (start q ∅) ≤ 2*budget (original p).length ∧
          (run T (start q ∅)).mode = .halt true := by
  rw [← selector_word,scan_spec,List.any_eq_true]
  constructor
  · rintro ⟨q,hq,yes⟩
    obtain ⟨T,hT,hv,h⟩ := every_candidate p q hq
    exact ⟨q,hq,selected_length _ _ hq,T,hT,hv,by simpa only [yes] using h⟩
  · rintro ⟨q,hq,_,T,_,_,h⟩
    obtain ⟨S,_,_,ans⟩ := every_candidate p q hq
    exact ⟨q,hq,halt_unique _ S T _ _ ans h⟩

end Codex.PolinomioPorEscolha
