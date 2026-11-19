import TGLExt.PontePalavraVerbo
import Mathlib.Tactic.DeriveFintype
import TGLExt.FitaComCusto

/-
A largura k conta as variáveis compartilhadas. Uma bolsa contém k+1 variáveis
consecutivas e qualquer número de cláusulas, de qualquer comprimento, inclusive
vazias. A entrada usa índices relativos, sinal, fim de cláusula e deslocamento.
A máquina varre as bolsas da última para a primeira. Para k fixo, o alfabeto
e a tabela de transições são finitos e independem do comprimento da fita.
-/
namespace IALD.CadeiasDeBolsas
open TGLExt.TraducaoTuring TGLExt.OPsibitEACompressao IALD.LeitorDaFormula

abbrev Row (k : Nat) := Fin k → Bool
abbrev Bag (k : Nat) := CNF (k+1)

def rows : (k : Nat) → List (Row k)
  | 0 => [Fin.elim0]
  | k+1 => (rows k).flatMap fun u => [Fin.cases false u, Fin.cases true u]

theorem complete_rows {k : Nat} (u : Row k) : u ∈ rows k := by
  induction k with
  | zero =>
    have e : u = Fin.elim0 := funext (fun i => Fin.elim0 i)
    simp [rows,e]
  | succ k ih =>
    have e : u = Fin.cases (u 0) (fun i => u i.succ) := by
      funext j
      cases j using Fin.cases <;> rfl
    apply List.mem_flatMap.mpr
    refine ⟨fun i => u i.succ,ih _,?_⟩
    cases h : u 0
    · exact List.mem_cons.mpr (Or.inl (by simpa [h] using e))
    · exact List.mem_cons.mpr (Or.inr (List.mem_cons.mpr (Or.inl (by simpa only [h] using e))))

def prefixRow {k : Nat} (w : Row (k+1)) : Row k := fun i => w i.castSucc
def suffixRow {k : Nat} (w : Row (k+1)) : Row k := fun i => w i.succ

def agree {k : Nat} (u v : Row k) : Bool := (List.finRange k).all (fun i => u i == v i)
theorem agree_spec {k : Nat} (u v : Row k) : agree u v = true ↔ u = v := by
  simp [agree,List.all_eq_true,List.mem_finRange,funext_iff]

def feasibleStep {k : Nat} (valid : Row (k+1) → Bool) (old : Row k → Bool) (v : Row k) : Bool :=
  (rows (k+1)).any fun w => agree (prefixRow w) v && valid w && old (suffixRow w)

theorem feasibleStep_spec {k : Nat} (valid : Row (k+1) → Bool) (old : Row k → Bool) (v : Row k) :
    feasibleStep valid old v = true ↔ ∃ w, prefixRow w = v ∧ valid w = true ∧
      old (suffixRow w) = true := by
  simp [feasibleStep,List.any_eq_true,complete_rows,agree_spec,and_assoc]

def relation {k : Nat} (bags : List (Bag k)) : Row k → Bool :=
  bags.foldr (fun f old => feasibleStep (passes f) old) (fun _ => true)

def clip (k : Nat) (x : Nat → Bool) : Row k := fun i => x i.val

def validChain {k : Nat} : List (Bag k) → (Nat → Bool) → Bool
  | [], _ => true
  | f :: rest, x => passes f (clip (k+1) x) && validChain rest (fun i => x (i+1))

/-- Concatena testemunhas compatíveis exatamente nas k variáveis comuns. -/
theorem relation_spec {k : Nat} (bags : List (Bag k)) (v : Row k) :
    relation bags v = true ↔ ∃ x : Nat → Bool, clip k x = v ∧ validChain bags x = true := by
  induction bags generalizing v with
  | nil =>
    constructor
    · intro _
      refine ⟨fun j => if h : j < k then v ⟨j,h⟩ else false,?_,rfl⟩
      funext i; simp [clip,i.isLt]
    · intro _; rfl
  | cons f rest ih =>
    change feasibleStep (passes f) (relation rest) v = true ↔ _
    rw [feasibleStep_spec]
    constructor
    · rintro ⟨w,hw,hf,hr⟩
      obtain ⟨tail,ht,htail⟩ := (ih _).mp hr
      let x : Nat → Bool := fun j => Nat.casesOn j (w 0) tail
      have xw : clip (k+1) x = w := by
        funext j
        cases j using Fin.cases with
        | zero => rfl
        | succ i => exact congrFun ht i
      refine ⟨x,?_,?_⟩
      · exact (congrArg prefixRow xw).trans hw
      · change (passes f (clip (k+1) x) && validChain rest tail) = true
        simp [xw,hf,htail]
    · rintro ⟨x,hx,h⟩
      change (passes f _ && validChain rest _) = true at h
      rw [Bool.and_eq_true] at h
      obtain ⟨h₁,h₂⟩ := h
      exact ⟨clip (k+1) x,hx,h₁,(ih _).mpr ⟨fun i => x (i+1),rfl,h₂⟩⟩

def raiseLit {k n : Nat} (h : k ≤ n) (l : Literal k) : Literal n := ⟨l.var.castLE h,l.pos⟩
def raiseCNF {k n : Nat} (h : k ≤ n) (f : CNF k) : CNF n := f.map (fun c => c.map (raiseLit h))

def formula {k : Nat} : (bags : List (Bag k)) → CNF (k+bags.length)
  | [] => []
  | f :: rest => raiseCNF (by simp) f ++ IALD.FitaComCusto.liftCNF (formula rest)

theorem formula_spec {k : Nat} (bags : List (Bag k)) (x : Nat → Bool) :
    passes (formula bags) (clip _ x) = validChain bags x := by
  induction bags generalizing x with
  | nil => rfl
  | cons f rest ih =>
    have re (h : k+1 ≤ k+(f::rest).length) :
        passes (raiseCNF h f) (clip _ x) = passes f (clip _ x) := by
      simp [passes,raiseCNF,satisfeita,List.all_map,List.any_map,Function.comp_def,Literal.vale,
        raiseLit,clip]
    have ap (g h : CNF (k+(f::rest).length)) :
        passes (g++h) (clip _ x) = (passes g (clip _ x) && passes h (clip _ x)) := List.all_append
    rw [formula,ap,re,IALD.FitaComCusto.lift_spec]
    exact congrArg (fun b => passes f (clip (k+1) x) && b) (ih (fun i => x (i+1)))

theorem sat_spec {k : Nat} (bags : List (Bag k)) :
    (rows k).any (relation bags) = true ↔ SAT (formula bags) := by
  rw [sat_iff]
  simp only [List.any_eq_true,complete_rows,true_and,relation_spec]
  constructor
  · rintro ⟨_,x,_,h⟩
    exact ⟨clip _ x,(formula_spec bags x).trans h⟩
  · rintro ⟨v,h⟩
    let x : Nat → Bool := fun j => if h : j < k+bags.length then v ⟨j,h⟩ else false
    have hx : clip (k+bags.length) x = v := by funext i; simp [clip,x,i.isLt]
    exact ⟨clip k x,x,rfl,by rw [← formula_spec,hx]; exact h⟩

def allGood {k : Nat} (bags : List (Bag k)) : Bool :=
  bags.all (fun f => (rows (k+1)).all (passes f))

theorem allGood_spec {k : Nat} (bags : List (Bag k)) :
    allGood bags = true ↔ ∀ x : Nat → Bool, validChain bags x = true := by
  induction bags with
  | nil => simp [allGood,validChain]
  | cons f rest ih =>
    change (((rows (k+1)).all (passes f)) && allGood rest) = true ↔ _
    simp only [Bool.and_eq_true,List.all_eq_true,complete_rows,true_implies,ih,validChain]
    constructor
    · rintro ⟨hf,hr⟩ x
      exact ⟨hf _,hr _⟩
    · intro h
      constructor
      · intro w
        let x : Nat → Bool := fun j => if hj : j < k+1 then w ⟨j,hj⟩ else false
        have hx : clip (k+1) x = w := by
          funext i
          simp only [clip,x,dif_pos i.isLt]
        simpa [hx] using (h x).1
      · intro y
        exact (h (Nat.casesOn · false y)).2

theorem quiet_spec {k : Nat} (bags : List (Bag k)) (t : ℝ) :
    allGood bags = true ↔ verboCalado (custoCNF (formula bags)) t := by
  rw [o_verbo_cala_sse_tudo_e_nome,allGood_spec]
  have eqz (f : CNF (k+bags.length)) (u : Row (k+bags.length)) :
      custoCNF f u = 0 ↔ passes f u = true := by
    simp [custoCNF_zero_sse,passes,List.all_eq_true]
  constructor
  · intro h u
    let x : Nat → Bool := fun j => if hj : j < k+bags.length then u ⟨j,hj⟩ else false
    have hx : clip (k+bags.length) x = u := by funext i; simp [clip,x,i.isLt]
    exact (eqz _ u).mpr (by rw [← hx,formula_spec]; exact h x)
  · intro h x
    exact (formula_spec bags x).symm.trans ((eqz _ _).mp (h _))


inductive Mark (k : Nat) where
  | lit (i : Fin (k+1)) (sign : Bool)
  | close
  | slide
deriving Fintype

structure Registers (k : Nat) where
  suffix : Row k → Bool
  bag : Row (k+1) → Bool
  clause : Row (k+1) → Bool
  quiet : Bool
deriving Fintype

def ready {k : Nat} (r : Row k → Bool) (q : Bool) : Registers k :=
  ⟨r,fun _ => true,fun _ => false,q⟩

/-- A semântica é de uma tabela de transição de controle finito para k fixo.
    Uma avaliação recursiva de closures Lean é uma implementação diferente. -/
def readMark {k : Nat} (r : Registers k) : Mark k → Registers k
  | .lit i sign => {r with clause := fun w => r.clause w || (w i == sign)}
  | .close => {r with bag := fun w => r.bag w && r.clause w, clause := fun _ => false}
  | .slide => ready (feasibleStep r.bag r.suffix) (r.quiet && (rows (k+1)).all r.bag)

def literals {k : Nat} (c : Clausula (k+1)) : List (Mark k) :=
  c.map (fun l => Mark.lit l.var l.pos)
def clauseTokens {k : Nat} (c : Clausula (k+1)) : List (Mark k) := literals c ++ [.close]
def bagTokens {k : Nat} (f : Bag k) : List (Mark k) := f.flatMap clauseTokens ++ [.slide]
def tape {k : Nat} (bags : List (Bag k)) := bags.reverse.flatMap bagTokens

theorem read_literals {k : Nat} (c : Clausula (k+1)) (r : Registers k) :
    (literals c).foldl readMark r = {r with clause := fun w => r.clause w || satisfeita c w} := by
  induction c generalizing r with
  | nil => simp [literals,satisfeita]
  | cons l c ih =>
    change (literals c).foldl readMark (readMark r (.lit l.var l.pos)) = _
    rw [ih]
    simp [readMark,satisfeita,Literal.vale,Bool.or_assoc]

theorem read_clauses {k : Nat} (f : Bag k) (r : Row k → Bool)
    (b : Row (k+1) → Bool) (q : Bool) :
    (f.flatMap clauseTokens).foldl readMark ⟨r,b,fun _ => false,q⟩ =
    ⟨r,fun w => b w && passes f w,fun _ => false,q⟩ := by
  induction f generalizing b with
  | nil => simp [passes]
  | cons c f ih =>
    rw [List.flatMap_cons,List.foldl_append]
    simp only [clauseTokens,List.foldl_append,read_literals,List.foldl_cons,List.foldl_nil,
      readMark,Bool.false_or]
    rw [ih]
    simp [passes,Bool.and_assoc]

theorem read_bag {k : Nat} (f : Bag k) (r : Row k → Bool) (q : Bool) :
    (bagTokens f).foldl readMark (ready r q) =
    ready (feasibleStep (passes f) r) (q && (rows (k+1)).all (passes f)) := by
  simp [bagTokens,List.foldl_append,ready,read_clauses,readMark]

theorem scan_spec {k : Nat} (bags : List (Bag k)) :
    (tape bags).foldl readMark (ready (fun _ => true) true) =
     ready (relation bags) (allGood bags) := by
  induction bags with
  | nil => rfl
  | cons f rest ih =>
    change ((f::rest).reverse.flatMap bagTokens).foldl readMark _ = _
    simp only [List.reverse_cons,List.flatMap_append,List.flatMap_cons,List.flatMap_nil,
      List.append_nil,List.foldl_append]
    change (bagTokens f).foldl readMark ((tape rest).foldl readMark _) = _
    rw [ih, read_bag]
    simp [relation,allGood,Bool.and_comm]

inductive Machine (k : Nat) where
  | reading (state : Registers k) (unread : List (Mark k))
  | stopped (word quiet : Bool)

def step {k : Nat} : Machine k → Machine k
  | .reading r (m :: ms) => .reading (readMark r m) ms
  | .reading r [] => .stopped ((rows k).any r.suffix) r.quiet
  | .stopped w q => .stopped w q

theorem prefix_steps {k : Nat} (pre rest : List (Mark k)) (r : Registers k) :
    step^[pre.length] (.reading r (pre ++ rest)) = .reading (pre.foldl readMark r) rest := by
  induction pre generalizing r with
  | nil => rfl
  | cons m ms ih =>
    change step^[ms.length+1] _ = _
    rw [Function.iterate_succ_apply]
    exact ih _

theorem exact_steps {k : Nat} (ms : List (Mark k)) (r : Registers k) :
    step^[ms.length+1] (.reading r ms) =
      .stopped ((rows k).any (ms.foldl readMark r).suffix) (ms.foldl readMark r).quiet := by
  induction ms generalizing r with
  | nil => rfl
  | cons m ms ih =>
    change step^[ms.length+1+1] _ = _
    rw [Function.iterate_succ_apply]
    exact ih _

/-- SIM e NÃO integram o mesmo teorema, para qualquer número de bolsas e
    qualquer lista de cláusulas na bolsa. A hipótese em t é a de `OPsibitEACompressao`. -/
theorem tape_reads_both {k : Nat} (bags : List (Bag k)) (t : ℝ)
    (ht : ((k+bags.length : Nat) : ℝ) * Real.log 2 < t) :
    ∃ w q, step^[(tape bags).length+1] (.reading (ready (fun _ => true) true) (tape bags)) =
      .stopped w q ∧ (w = true ↔ palavra (custoCNF (formula bags)) t) ∧
      (q = true ↔ verboCalado (custoCNF (formula bags)) t) := by
  refine ⟨(rows k).any (relation bags),allGood bags,?_,(sat_spec bags).trans
    (a_palavra_decide _ ht _),quiet_spec bags t⟩
  rw [exact_steps,scan_spec]; rfl

/-- k fica fixo na construção da máquina. As células da tabela verdade de
    cada registrador não podem passar por armazenamento de custo constante
    quando se deixa k crescer com a entrada. -/
theorem finite_control (k : Nat) : Finite (Registers k) ∧ Finite (Mark k) :=
  ⟨inferInstance,inferInstance⟩

def stateComponents (k : Nat) : Registers k ≃
    ((Row k → Bool) × (Row (k+1) → Bool) × (Row (k+1) → Bool) × Bool) where
  toFun s := (s.suffix,s.bag,s.clause,s.quiet)
  invFun p := ⟨p.1,p.2.1,p.2.2.1,p.2.2.2⟩
  left_inv _ := rfl
  right_inv _ := rfl

/-- A finitude tem um preço explícito: esta tabela usa esse conjunto de
    estados possíveis, ainda que parte deles seja inalcançável. -/
theorem state_space (k : Nat) :
    Fintype.card (Registers k) =
      2^(2^k) * (2^(2^(k+1)) * (2^(2^(k+1)) * 2)) := by
  rw [Fintype.card_congr (stateComponents k)]
  simp [Row]

theorem charged_length {k : Nat} (bags : List (Bag k)) :
    (tape bags).length =
      (bags.map (fun f => (f.map List.length).sum + f.length + 1)).sum := by
  have h (f : Bag k) : (f.flatMap clauseTokens).length = (f.map List.length).sum + f.length := by
    induction f with
    | nil => simp
    | cons c f ih =>
      simp only [List.flatMap_cons,List.length_append,clauseTokens,literals,List.length_map,
        List.length_cons,List.length_nil,List.map_cons,List.sum_cons] at *
      omega
  induction bags with
  | nil => rfl
  | cons f rest ih =>
    change ((f::rest).reverse.flatMap bagTokens).length = _
    simp only [List.reverse_cons,List.flatMap_append,List.flatMap_cons,List.flatMap_nil,
      List.append_nil,List.length_append,List.map_cons,List.sum_cons]
    change (tape rest).length + (bagTokens f).length = _
    rw [ih]
    simp [bagTokens,h, Nat.add_comm]

def extendLast {k : Nat} (v : Row k) (b : Bool) : Row (k+1) := Fin.lastCases b v

@[simp] theorem extend_prefix {k : Nat} (v : Row k) (b : Bool) :
    prefixRow (extendLast v b) = v := by
  funext i; simp [prefixRow,extendLast]

theorem extend_self {k : Nat} (w : Row (k+1)) :
    extendLast (prefixRow w) (w (Fin.last k)) = w := by
  funext i
  cases i using Fin.lastCases <;> simp [extendLast,prefixRow]

def branch {k : Nat} (valid : Row (k+1) → Bool) (old : Row k → Bool)
    (v : Row k) (b : Bool) : Bool :=
  valid (extendLast v b) && old (suffixRow (extendLast v b))

/-- Só dois prolongamentos são candidatos por célula, com o MESMO contexto v. -/
theorem join_is_pair {k : Nat} (valid : Row (k+1) → Bool) (old : Row k → Bool)
    (v : Row k) :
    feasibleStep valid old v = (branch valid old v false || branch valid old v true) := by
  apply Bool.eq_iff_iff.mpr
  rw [feasibleStep_spec,Bool.or_eq_true]
  constructor
  · rintro ⟨w,hv,hf,hr⟩
    have he : extendLast v (w (Fin.last k)) = w := by
      rw [← hv,extend_self]
    have hb : branch valid old v (w (Fin.last k)) = true := by
      simp [branch,he,hf,hr]
    cases h : w (Fin.last k)
    · exact Or.inl (by simpa only [h] using hb)
    · exact Or.inr (by simpa only [h] using hb)
  · rintro (hb | hb)
    · refine ⟨extendLast v false,extend_prefix _ _,?_⟩
      simpa [branch] using hb
    · refine ⟨extendLast v true,extend_prefix _ _,?_⟩
      simpa [branch] using hb

theorem join_psibit {k : Nat} (valid : Row (k+1) → Bool) (old : Row k → Bool)
    (v : Row k) : ∃ θ : ℝ,
    (TGLExt.Psibit.codeAmp θ).word = bitSign (branch valid old v false) ∧
    (TGLExt.Psibit.codeAmp θ).verb = bitSign (branch valid old v true) ∧
    (feasibleStep valid old v = true ↔
      (TGLExt.Psibit.codeAmp θ).word = 1 ∨ (TGLExt.Psibit.codeAmp θ).verb = 1) := by
  have nz (b : Bool) : bitSign b ≠ 0 := by cases b <;> decide
  have bit (b : Bool) : bitSign b = 1 ↔ b = true := by cases b <;> decide
  obtain ⟨θ,h₁,h₂⟩ := TGLExt.Psibit.the_orbit_visits_all_four_states _ _
    (nz (branch valid old v false)) (nz (branch valid old v true))
  exact ⟨θ,h₁,h₂,by rw [join_is_pair,h₁,h₂,bit,bit,Bool.or_eq_true]⟩

end IALD.CadeiasDeBolsas
