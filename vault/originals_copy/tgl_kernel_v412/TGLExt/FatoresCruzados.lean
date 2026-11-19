import TGLExt.ParesIndependentes
import TGLExt.RotulosCompartilhados

/-! Boolean sum-product factors with a shared physical variable per label.
In a clause the running bond is a Bool: at least one literal has passed.
Different clauses need not have disjoint scopes. -/
namespace IALD.FatoresCruzados
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula IALD.LeitorDaFormula

abbrev Env (n : Nat) := Fin n → Bool

/-- Boolean tensor contraction over exactly two values of the shared bond. -/
def join (a b : ParesIndependentes.Mask) : ParesIndependentes.Mask := ParesIndependentes.table fun i j =>
  (ParesIndependentes.read a i false && ParesIndependentes.read b false j) || (ParesIndependentes.read a i true && ParesIndependentes.read b true j)

/-- The two-by-two transition matrix for updating the "seen true" flag. -/
def flag (hit : Bool) : ParesIndependentes.Mask := ParesIndependentes.table (fun i j => j == (i || hit))

theorem flag_product (a b : Bool) : join (flag a) (flag b) = flag (a || b) := by
  cases a <;> cases b <;> rfl

structure Core (n : Nat) where
  label : Fin n
  onFalse : ParesIndependentes.Mask
  onTrue : ParesIndependentes.Mask

def compileLit {n} (l : Literal n) : Core n :=
  ⟨l.var,flag (false == l.pos),flag (true == l.pos)⟩
def evaluate {n} (g : Core n) (x : Env n) := if x g.label then g.onTrue else g.onFalse

theorem core_spec {n} (l : Literal n) (x : Env n) :
    evaluate (compileLit l) x = flag (l.vale x) := by
  cases h : x l.var <;> simp [evaluate,compileLit,Literal.vale,h]

theorem core_psibit {n} (l : Literal n) (x : Env n) (incoming : Bool) :
    ∃ θ : ℝ, (TGLExt.Psibit.codeAmp θ).word =
      bitSign (ParesIndependentes.read (evaluate (compileLit l) x) incoming false) ∧
      (TGLExt.Psibit.codeAmp θ).verb =
      bitSign (ParesIndependentes.read (evaluate (compileLit l) x) incoming true) ∧
      TGLExt.Psibit.decodeAmp (TGLExt.Psibit.codeAmp θ) = TGLExt.Psibit.v θ :=
  ParesIndependentes.two_psibits _ _

def contract {n} (gs : List (Core n)) (x : Env n) :=
  gs.foldr (fun g acc => join (evaluate g x) acc) (flag false)

theorem contract_clause {n} (c : Clausula n) (x : Env n) :
    contract (c.map compileLit) x = flag (satisfeita c x) := by
  induction c with
  | nil => rfl
  | cons l c ih =>
    change join (evaluate (compileLit l) x) (contract (c.map compileLit) x) =
      flag (l.vale x || satisfeita c x)
    rw [core_spec,ih,flag_product]

/-- Literals from any number of pairs, grouped into segments, may be
contracted separately under the same x. Each segment still has a two-state bond. -/
theorem contract_segments {n} (chunks : List (Clausula n)) (x : Env n) :
    chunks.foldr (fun c tail => join (contract (c.map compileLit) x) tail) (flag false) =
      flag (satisfeita chunks.flatten x) := by
  induction chunks with
  | nil => rfl
  | cons c chunks ih =>
    rw [List.foldr_cons,ih,contract_clause,flag_product]
    simp [satisfeita]

theorem regroup {n} (p q : Clausula n) (h : p.Perm q) (x : Env n) :
    contract (p.map compileLit) x = contract (q.map compileLit) x := by
  rw [contract_clause,contract_clause]
  apply congrArg flag
  exact h.any_eq

def factorize {n} (p : CNF n) := p.map (List.map compileLit)
def output {n} (g : List (Core n)) (x : Env n) := ParesIndependentes.read (contract g x) false true
def accept {n} (p : List (List (Core n))) (x : Env n) := p.all (fun g => output g x)

theorem output_clause {n} (c : Clausula n) (x : Env n) :
    output (c.map compileLit) x = satisfeita c x := by
  rw [output,contract_clause]
  cases h : satisfeita c x <;> rfl

theorem flat_exact {n} (p : CNF n) (x : Env n) :
    accept (factorize p) x = passes p x := by
  induction p with
  | nil => rfl
  | cons c p ih =>
    change (output (c.map compileLit) x && accept (factorize p) x) =
      (satisfeita c x && passes p x)
    rw [output_clause,ih]

/-- Intersect even an arbitrary previously correlated relation, pointwise.
The old relation and the new clause see the same external variable x[i] at
every occurrence; only the internal clause flag is existentially contracted. -/
theorem intersect_any {n} (r : Env n → Bool) (c : Clausula n) (x : Env n) :
    (r x && output (c.map compileLit) x) = (r x && satisfeita c x) := by rw [output_clause]

section OneCrossing
open ParesIndependentes (Mask table read)

def existsPair (f : Bool → Bool → Bool) :=
  (f false false || f false true) || (f true false || f true true)

private theorem existsPair_spec (f : Bool → Bool → Bool) :
    existsPair f = true ↔ ∃ a b, f a b = true := by simp [existsPair,Bool.exists_bool]

private theorem join_spec (a b : Mask) (i j : Bool) :
    read (join a b) i j = true ↔ ∃ k, read a i k = true ∧ read b k j = true := by
  simp [join,Bool.exists_bool]

/-- The first row data is any local correlation. The second says which of
its four valuations satisfies the literals of the crossing clause at this pair. -/
abbrev PairData := Mask × Mask

def eliminatePair (d : PairData) : Mask := table fun i j =>
  existsPair (fun a b => read d.1 a b && (j == (i || read d.2 a b)))

private theorem eliminatePair_spec (d : PairData) (i j : Bool) :
    read (eliminatePair d) i j = true ↔
      ∃ a b, read d.1 a b = true ∧ j = (i || read d.2 a b) := by
  simp [eliminatePair,existsPair_spec]

def closePairs : List PairData → Mask × Nat
  | [] => (flag false,0)
  | d::ds =>
    let t := closePairs ds
    (join (eliminatePair d) t.1,t.2+1)

def trace : List PairData → List (Bool × Bool) → Bool → Bool → Bool
  | [],[],i,j => j == i
  | d::ds,(a,b)::cs,i,j =>
    read d.1 a b && trace ds cs (i || read d.2 a b) j
  | _,_,_,_ => false

theorem closePairs_spec (ds : List PairData) (i j : Bool) :
    read (closePairs ds).1 i j = true ↔ ∃ cs, trace ds cs i j = true := by
  induction ds generalizing i j with
  | nil =>
    constructor
    · intro h; exact ⟨[],by simpa [closePairs,flag,trace] using h⟩
    · rintro ⟨cs,h⟩; cases cs <;> simp_all [trace,closePairs,flag]
  | cons d ds ih =>
    change read (join (eliminatePair d) (closePairs ds).1) i j = true ↔ _
    rw [join_spec]
    constructor
    · rintro ⟨k,hl,hr⟩
      obtain ⟨a,b,ha,hk⟩ := (eliminatePair_spec d i k).mp hl
      obtain ⟨cs,hs⟩ := (ih k j).mp hr
      exact ⟨(a,b)::cs,by simpa [trace,ha,← hk] using hs⟩
    · rintro ⟨cs,hs⟩
      cases cs with
      | nil => simp [trace] at hs
      | cons ab cs =>
        obtain ⟨a,b⟩ := ab
        simp only [trace,Bool.and_eq_true] at hs
        exact ⟨_,(eliminatePair_spec _ _ _).mpr ⟨a,b,hs.1,rfl⟩,
          (ih _ _).mpr ⟨cs,hs.2⟩⟩

/-- Exactly one constant-size pair elimination and one two-by-two matrix
contraction at each step. Label axes have already been grouped by pair. -/
theorem closePairs_steps (ds : List PairData) : (closePairs ds).2 = ds.length := by
  induction ds with
  | nil => rfl
  | cons d ds ih => simp [closePairs,ih]

end OneCrossing

section FlatCrossing
open ParesIndependentes (State LocalClause splitLit insert rule decode allows flatten)

private theorem shared_lit {n} (l : Literal (n+n)) (x y : Env n) :
    ParesIndependentes.literal (splitLit l).2 (x (splitLit l).1) (y (splitLit l).1) =
      l.vale (Fin.append x y) := by
  obtain ⟨i,b⟩ := l
  cases i using Fin.addCases <;>
    simp [splitLit,ParesIndependentes.literal,Literal.vale,-Fin.natAdd_eq_addNat]

def testLiteral {n} (s : State n) (l : Literal (n+n)) : Bool × Nat :=
  let localLit := splitLit l
  let updated := insert s localLit.1 (rule [localLit.2])
  (decode updated.1,updated.2+n)

theorem literal_witness {n} (s : State n) (l : Literal (n+n)) :
    (testLiteral s l).1 = true ↔
    ∃ x y, allows s x y = true ∧ l.vale (Fin.append x y) = true := by
  simp [testLiteral,ParesIndependentes.decode_spec,ParesIndependentes.insert_spec,
    rule,ParesIndependentes.localPass,shared_lit]

/-- Flat crossing clause, with no grouping supplied. Try each of its own
literals against the same independent-pair state. Short circuit on success.
The counter charges addresses actually visited and a full decode scan per try. -/
def oneCrossing {n} (s : State n) : Clausula (n+n) → Bool × Nat
  | [] => (false,0)
  | l::c =>
    let a := testLiteral s l
    if a.1 then a else
      let b := oneCrossing s c
      (b.1,a.2+b.2)

theorem one_witness {n} (s : State n) (c : Clausula (n+n)) :
    (oneCrossing s c).1 = true ↔
      ∃ x y, allows s x y = true ∧ satisfeita c (Fin.append x y) = true := by
  induction c with
  | nil => simp [oneCrossing,satisfeita]
  | cons l c ih =>
    have h₀ := literal_witness s l
    have disj : (oneCrossing s (l::c)).1 =
      ((testLiteral s l).1 || (oneCrossing s c).1) := by
      change (if (testLiteral s l).1 then testLiteral s l else
        ((oneCrossing s c).1,(testLiteral s l).2+(oneCrossing s c).2)).1 = _
      cases h : (testLiteral s l).1 <;> simp [h]
    rw [disj,Bool.or_eq_true,h₀,ih]
    simp only [satisfeita,List.any_cons,Bool.or_eq_true]
    aesop

theorem crossing_charge {n} (s : State n) (c : Clausula (n+n)) :
    (oneCrossing s c).2 ≤ 2*n*c.length := by
  induction c with
  | nil => simp [oneCrossing]
  | cons l c ih =>
    have hc : (testLiteral s l).2 ≤ 2*n := by
      simp only [testLiteral,ParesIndependentes.address_visits]
      have hi := (splitLit l).1.isLt
      omega
    rw [List.length_cons,Nat.mul_succ]
    change (if (testLiteral s l).1 then testLiteral s l else
      ((oneCrossing s c).1,(testLiteral s l).2+(oneCrossing s c).2)).2 ≤ _
    by_cases h : (testLiteral s l).1 = true
    · rw [if_pos h]; omega
    · rw [if_neg h]; change (testLiteral s l).2+(oneCrossing s c).2 ≤ _; omega

theorem one_flat_word {n} (base : List (LocalClause n)) (c : Clausula (n+n)) :
    (oneCrossing (ParesIndependentes.run base (ParesIndependentes.full n)).1 c).1 =
      palavraDaFormula (flatten base ++ [c]) := by
  apply Bool.eq_iff_iff.mpr
  rw [one_witness,a_palavra_e_o_sat,sat_iff]
  have hp (z : Env (n+n)) : passes (flatten base ++ [c]) z =
      (passes (flatten base) z && satisfeita c z) := by simp [passes]
  simp only [ParesIndependentes.stream_spec,ParesIndependentes.full_allows,Bool.true_and,
    hp,Bool.and_eq_true,ParesIndependentes.flat_pass]
  constructor
  · rintro ⟨x,y,hb,hc⟩
    exact ⟨Fin.append x y,by simpa only [Fin.append_left,Fin.append_right] using hb,hc⟩
  · rintro ⟨z,hb,hc⟩
    exact ⟨_,_,hb,by simpa only [Fin.append_castAdd_natAdd] using hc⟩

end FlatCrossing

def word {n} (p : List (List (Core n))) := RotulosCompartilhados.search n (accept p)

theorem global_word {n} (p : CNF n) : word (factorize p) = palavraDaFormula p := by
  apply Bool.eq_iff_iff.mpr
  simp only [word,RotulosCompartilhados.search_spec,flat_exact,a_palavra_e_o_sat,sat_iff]

theorem global_probes {n} (p : CNF n) (h : ¬ SAT p) :
    RotulosCompartilhados.probes n (accept (factorize p)) = (false,2^n) := by
  apply RotulosCompartilhados.probes_empty
  intro x
  rw [flat_exact]
  cases hx : passes p x with
  | false => rfl
  | true => exact (h ((sat_iff p).2 ⟨x,hx⟩)).elim

/-- Concrete fixed alphabet: binary labels, explicit sign or eight table bits,
and one end-of-clause symbol. A label's terminating marker is common to both. -/
inductive Mark | digit (b : Bool) | endLabel | bit (b : Bool) | endClause
def address (i : Nat) : List Mark := i.bits.map Mark.digit ++ [.endLabel]
def packMask (m : ParesIndependentes.Mask) : List Mark :=
  [.bit m.low.word,.bit m.low.verb,.bit m.high.word,.bit m.high.verb]
def orig {n} (l : Literal n) := address l.var.val ++ [.bit l.pos]
def serial {n} (g : Core n) := address g.label.val ++ packMask g.onFalse ++ packMask g.onTrue
def input {n} (p : CNF n) := p.flatMap (fun c => c.flatMap orig ++ [.endClause])
def encoded {n} (p : List (List (Core n))) := p.flatMap (fun c => c.flatMap serial ++ [.endClause])
def occurrences {n} (p : CNF n) := (p.map List.length).sum

theorem local_size {n} (c : Clausula n) :
    ((c.map compileLit).flatMap serial).length = (c.flatMap orig).length + 7*c.length := by
  induction c with
  | nil => rfl
  | cons l c ih =>
    simp only [List.map_cons,List.flatMap_cons,List.length_append,serial,compileLit,packMask,
      List.length_cons,List.length_nil,orig] at ih ⊢
    omega

theorem encoded_size {n} (p : CNF n) :
    (encoded (factorize p)).length = (input p).length + 7*occurrences p := by
  induction p with
  | nil => rfl
  | cons c p ih =>
    change (((c.map compileLit).flatMap serial ++ [Mark.endClause]) ++ encoded (factorize p)).length =
      ((c.flatMap orig ++ [Mark.endClause]) ++ input p).length + 7*(c.length+occurrences p)
    simp only [List.length_append,List.length_cons,List.length_nil,local_size,ih]
    omega

private theorem literals_fit {n} (c : Clausula n) : c.length ≤ (c.flatMap orig).length := by
  induction c with
  | nil => rfl
  | cons l c ih => simp only [List.flatMap_cons,List.length_append,List.length_cons,orig,List.length_nil]; omega

theorem linear_encoding {n} (p : CNF n) : (encoded (factorize p)).length ≤ 8*(input p).length := by
  have bound : occurrences p ≤ (input p).length := by
    induction p with
    | nil => rfl
    | cons c p ih =>
      have h := literals_fit c
      change c.length+occurrences p ≤ ((c.flatMap orig ++ [Mark.endClause]) ++ input p).length
      simp only [List.length_append,List.length_cons,List.length_nil]
      omega
  rw [encoded_size]
  omega

/-- For one fixed global assignment, each literal contributes exactly one
2-by-2 contraction, i.e. eight ANDs and four ORs in the dense implementation.
No head-movement or global existential cost is hidden inside this count. -/
def metered {n} : List (Core n) → Env n → ParesIndependentes.Mask × Nat
  | [],_ => (flag false,0)
  | g::gs,x =>
    let t := metered gs x
    (join (evaluate g x) t.1,t.2+12)

theorem metered_exact {n} (gs : List (Core n)) (x : Env n) :
    metered gs x = (contract gs x,12*gs.length) := by
  induction gs with
  | nil => rfl
  | cons g gs ih =>
    simp [metered,ih,contract,Nat.mul_succ]

/-- The pairs (a,b) and (c,d) are both constrained internally to equality.
Two genuinely crossing clauses force a and c to disagree, while two others
force them to agree. The two crossing blocks separately admit witnesses. -/
def xy (a b : Fin 4) (p q : Bool) : Clausula 4 := [⟨a,p⟩,⟨b,q⟩]
def equal (a b : Fin 4) : CNF 4 := [xy a b false true,xy a b true false]
def differ (a b : Fin 4) : CNF 4 := [xy a b true true,xy a b false false]
def seed : CNF 4 := equal 0 1 ++ equal 2 3

theorem crossing_contradiction :
    word (factorize (seed ++ equal 0 2)) = true ∧
    word (factorize (seed ++ differ 0 2)) = true ∧
    word (factorize (seed ++ equal 0 2 ++ differ 0 2)) = false := by decide

end IALD.FatoresCruzados
