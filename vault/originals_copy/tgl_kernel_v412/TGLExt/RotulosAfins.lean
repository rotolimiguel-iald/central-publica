import TGLExt.PontePalavraVerbo
import TGLExt.CorrelacoesDistintas

/- Um rótulo preserva as equações afins da fronteira sobre o corpo de dois
   elementos. A leitura de um ramo pode depender de TODOS os bits restantes.
   Cada coluna guarda no máximo um pivô e a sua cauda de coeficientes.
   Nomes locais de construção. Nenhuma escolha de nome canônico. -/
namespace IALD.RotulosAfins

open TGLExt.TraducaoTuring TGLExt.OPsibitEACompressao IALD.LeitorDaFormula

abbrev Assignment (n : Nat) := Fin n → Bool

/-- Forma afim d xor Σ cᵢxᵢ. Uma equação exige seu valor falso (= zero). -/
inductive Row : Nat → Type where
  | offset (d : Bool) : Row 0
  | col {n} (coeff : Bool) (tail : Row n) : Row (n+1)
deriving Repr

def value : {n : Nat} → Row n → Assignment n → Bool
  | _, .offset b, _ => b
  | _, .col c r, x => Bool.xor (c && x 0) (value r (fun i => x i.succ))

/-- XOR bit a bit. Contam-se duas leituras e uma escrita por posição,
    inclusive o termo constante. -/
def xorRows : {n : Nat} → Row n → Row n → Row n × Nat
  | _, .offset a,.offset b => (.offset (Bool.xor a b),3)
  | _, .col a r,.col b s =>
    let result := xorRows r s
    (.col (Bool.xor a b) result.1,result.2+3)

theorem xor_value {n} (r s : Row n) (x : Assignment n) :
    value (xorRows r s).1 x = Bool.xor (value r x) (value s x) := by
  induction r with
  | offset b => cases s; rfl
  | col a r ih =>
    cases s with
    | col b s =>
      simp only [xorRows,value,ih]
      cases a <;> cases b <;> cases x 0 <;> cases value r (fun i => x i.succ) <;>
        cases value s (fun i => x i.succ) <;> rfl

theorem xor_work {n} (r s : Row n) : (xorRows r s).2 = 3*(n+1) := by
  induction r with
  | offset b => cases s; rfl
  | col a r ih => cases s with
    | col b s => simp [xorRows,ih]; omega

/-- done true conserva uma contradição 1=0. No slot de índice i, some tail
    representa Xᵢ = valor(tail); none deixa esse bit livre. -/
inductive Label : Nat → Type where
  | done (inconsistent : Bool) : Label 0
  | slot {n} (pivot : Option (Row n)) (lower : Label n) : Label (n+1)
deriving Repr

def fits : {n : Nat} → Label n → Assignment n → Bool
  | _, .done b,_ => !b
  | _, .slot p l,x =>
    (p.elim true (fun row => x 0 == value row (fun i => x i.succ))) &&
      fits l (fun i => x i.succ)

def blank : (n : Nat) → Label n
  | 0 => .done false
  | k+1 => .slot none (blank k)

theorem blank_fits (n : Nat) (x : Assignment n) : fits (blank n) x = true := by
  induction n with
  | zero => rfl
  | succ k ih => exact ih _

/-- Medidor de trabalho sobre linhas densas. Quatro unidades por inspeção
    de slot/coefficient e reconstrução do controle; uma cópia da cauda
    custa duas operações por bit. A soma de linhas também cobra cada bit. -/
def insertRow : {n : Nat} → Row n → Label n → Label n × Nat
  | _, .offset a,.done b => (.done (a || b),3)
  | _, .col false r,.slot p l =>
    let v := insertRow r l
    (.slot p v.1, v.2+4)
  | _+1, .col true r,.slot none l =>
    (.slot (some r) l,4+2*((fun {m} (_ : Row m) => m+1) r))
  | _, .col true r,.slot (some p) l =>
    let add := xorRows r p
    let v := insertRow add.1 l
    (.slot (some p) v.1,v.2+add.2+4)

theorem insert_spec {n} (eqn : Row n) (s : Label n) (x : Assignment n) :
    fits (insertRow eqn s).1 x = (fits s x && !(value eqn x)) := by
  induction n with
  | zero =>
    cases eqn with | offset a =>
      cases s with | done b =>
        cases a <;> cases b <;> rfl
  | succ k ih =>
    cases eqn with | col c r =>
      cases s with | slot p l =>
        cases c
        · simp [insertRow,fits,value,ih,Bool.and_assoc]
        · cases p with
          | none =>
            simp only [insertRow,fits,value,Option.elim_some,Option.elim_none,
              Bool.true_and]
            cases x 0 <;> cases value r (fun i => x i.succ) <;>
              cases fits l (fun i => x i.succ) <;> rfl
          | some p =>
            simp only [insertRow,fits,value,Option.elim_some,Bool.true_and,ih,xor_value]
            cases x 0 <;> cases value r (fun i => x i.succ) <;>
              cases value p (fun i => x i.succ) <;> cases fits l (fun i => x i.succ) <;> rfl

theorem insert_work {n} (eqn : Row n) (s : Label n) :
    (insertRow eqn s).2 ≤ 4*(n+1)^2 := by
  induction n with
  | zero => cases eqn; cases s; norm_num [insertRow]
  | succ k ih =>
    cases eqn with | col c r =>
      cases s with | slot p l =>
        cases c
        · simp only [insertRow]
          have h := ih r l
          ring_nf at h ⊢
          omega
        · cases p with
          | none => simp only [insertRow]; ring_nf; omega
          | some p =>
            simp only [insertRow,xor_work]
            have h := ih (xorRows r p).1 l
            ring_nf at h ⊢
            omega

def footprint : {n : Nat} → Label n → Nat
  | _, .done _ => 1
  | k+1, .slot p l => 1 + (p.elim 0 (fun _ => k+1)) + footprint l

theorem compact_size {n} (s : Label n) : footprint s ≤ (n+1)^2 := by
  induction s with
  | done b => simp [footprint]
  | @slot k p l ih =>
    cases p <;> simp only [footprint,Option.elim_none,Option.elim_some] <;>
      ring_nf at ih ⊢ <;> omega

/-- Um testemunho, obtido resolvendo os pivôs de trás para a frente. -/
def readWord : {n : Nat} → Label n → Bool
  | _, .done b => !b
  | _, .slot _ l => readWord l

def witness : {n : Nat} → Label n → Assignment n
  | _, .done _ => Fin.elim0
  | _, .slot p l =>
    let tail := witness l
    Fin.cases (p.elim false (fun r => value r tail)) tail

theorem witness_fits {n} (s : Label n) : fits s (witness s) = readWord s := by
  induction s with
  | done _ => rfl
  | slot p l ih => cases p <;> simp [fits,witness,readWord,ih]

theorem fits_implies_word {n} (s : Label n) (x : Assignment n) :
    fits s x = true → readWord s = true := by
  induction s with
  | done b => exact id
  | slot p l ih =>
    intro h
    apply ih (fun i => x i.succ)
    change (_ && _) = true at h
    rw [Bool.and_eq_true] at h
    exact h.2

def run {n : Nat} : List (Row n) → Label n → Label n × Nat
  | [],s => (s,0)
  | eqn :: eqns,s =>
    let first := insertRow eqn s
    let rest := run eqns first.1
    (rest.1, first.2+rest.2)

theorem run_spec {n} (eqns : List (Row n)) (s : Label n) (x : Assignment n) :
    fits (run eqns s).1 x = (fits s x && eqns.all (fun r => !(value r x))) := by
  induction eqns generalizing s with
  | nil => simp [run]
  | cons r eqns ih => simp [run,ih,insert_spec,Bool.and_assoc]

theorem run_work {n} (eqns : List (Row n)) (s : Label n) :
    (run eqns s).2 ≤ eqns.length * (4*(n+1)^2) := by
  induction eqns generalizing s with
  | nil => simp [run]
  | cons r eqns ih =>
    simp only [run,List.length_cons,Nat.add_mul,one_mul]
    exact (Nat.add_le_add (insert_work r s) (ih _)).trans_eq (Nat.add_comm _ _)

theorem affine_word {n} (eqns : List (Row n)) :
    readWord (run eqns (blank n)).1 = true ↔ ∃ x, eqns.all (fun r => !(value r x)) = true := by
  have h (x : Assignment n) : fits (run eqns (blank n)).1 x =
      eqns.all (fun r => !(value r x)) := by rw [run_spec, blank_fits,Bool.true_and]
  constructor
  · intro yes
    exact ⟨witness (run eqns (blank n)).1,by rw [← h,witness_fits,yes]⟩
  · rintro ⟨x,hx⟩
    exact fits_implies_word _ x ((h x).trans hx)

def constant : (n : Nat) → Bool → Row n
  | 0,d => .offset d
  | n+1,d => .col false (constant n d)

@[simp] theorem constant_value (n : Nat) (d : Bool) (x : Assignment n) :
    value (constant n d) x = d := by
  induction n with
  | zero => rfl
  | succ k ih => simp [constant,value,ih]

def coordinate : (n : Nat) → Fin n → Row n
  | 0,i => Fin.elim0 i
  | k+1,i => Fin.cases (.col true (constant k false)) (fun j => .col false (coordinate k j)) i

@[simp] theorem coord_value (n : Nat) (i : Fin n) (x : Assignment n) :
    value (coordinate n i) x = x i := by
  induction n with
  | zero => exact Fin.elim0 i
  | succ k ih =>
    cases i using Fin.cases with
    | zero => simp [coordinate,value]
    | succ j => simp [coordinate,value,ih]

/-- Sintaxe da classe de CNFs: pinos unitários e os pares de cláusulas que
    exprimem igualdade ou oposição, em qualquer ordem e em qualquer grafo. -/
inductive Constraint (n : Nat) where
  | pin (i : Fin n) (b : Bool)
  | link (i j : Fin n) (p : Bool)

def rowOf {n} : Constraint n → Row n
  | .pin i b => (xorRows (coordinate n i) (constant n b)).1
  | .link i j p => (xorRows (xorRows (coordinate n i) (coordinate n j)).1 (constant n p)).1

def cnfOf {n} : Constraint n → CNF n
  | .pin i b => [[⟨i,b⟩]]
  | .link i j p => [[⟨i,false⟩,⟨j,!p⟩],[⟨i,true⟩,⟨j,p⟩]]

theorem literal_translation {n} (c : Constraint n) (x : Assignment n) :
    (!(value (rowOf c) x)) = passes (cnfOf c) x := by
  cases c with
  | pin i b =>
    simp only [rowOf,xor_value,coord_value,constant_value,cnfOf,passes,List.all_cons,
      List.all_nil,satisfeita,List.any_cons,List.any_nil,Literal.vale]
    cases x i <;> cases b <;> rfl
  | link i j p =>
    simp only [rowOf,xor_value,coord_value,constant_value,cnfOf,passes,List.all_cons,
      List.all_nil,satisfeita,List.any_cons,List.any_nil,Literal.vale]
    cases x i <;> cases x j <;> cases p <;> rfl

theorem translated_support {n} (cs : List (Constraint n)) (x : Assignment n) :
    (cs.map rowOf).all (fun r => !(value r x)) = passes (cs.flatMap cnfOf) x := by
  induction cs with
  | nil => rfl
  | cons c cs ih =>
    rw [List.map_cons,List.all_cons,literal_translation c x,ih]
    simp only [List.flatMap_cons,passes,List.all_append]

theorem signed_CNF_word {n} (cs : List (Constraint n)) (t : ℝ) (ht : (n:ℝ)*Real.log 2 < t) :
    readWord (run (cs.map rowOf) (blank n)).1 = true ↔ palavra (custoCNF (cs.flatMap cnfOf)) t := by
  rw [affine_word,← a_palavra_decide n ht,sat_iff]
  simp only [translated_support]

def equalityLinks (n : Nat) : List (Constraint (n+n)) :=
  (List.finRange n).map (fun i => .link (i.castAdd n) (Fin.natAdd n i) false)

theorem equality_solutions (n : Nat) (u v : Assignment n) :
    fits (run ((equalityLinks n).map rowOf) (blank (n+n))).1 (Fin.append u v) = true ↔
      passes (IALD.CorrelacoesDistintas.equalCNF n) (Fin.append u v) = true := by
  rw [IALD.CorrelacoesDistintas.equalCNF_spec,run_spec,blank_fits,Bool.true_and]
  simp only [equalityLinks,List.map_map,List.all_map,List.all_eq_true,Function.comp_apply,
    List.mem_finRange,true_implies,rowOf,xor_value,coord_value,constant_value,
    Fin.append_left,Fin.append_right]
  rw [funext_iff]
  constructor <;> intro h i <;> have hi := h i <;>
    cases hu : u i <;> cases hv : v i <;> simp_all

/-- O resultado dos dois ramos sobre uma MESMA cauda é codificável nos dois
    sinais da órbita. O pivô torna a leitura existencial exatamente o rótulo inferior. -/
theorem join_pair {n} (p : Option (Row n)) (l : Label n) (x : Assignment n) :
    (fits (.slot p l) (Fin.cases false x) || fits (.slot p l) (Fin.cases true x)) =
      fits l x := by
  cases p with
  | none => simp [fits]
  | some p =>
    simp only [fits,Option.elim_some,Fin.cases_zero,Fin.cases_succ]
    cases value p x <;> cases fits l x <;> rfl

theorem psibit_on_label {n} (s : Label (n+1)) (x : Assignment n) :
    ∃ θ : ℝ, (TGLExt.Psibit.codeAmp θ).word =
      bitSign (fits s (Fin.cases false x)) ∧ (TGLExt.Psibit.codeAmp θ).verb =
      bitSign (fits s (Fin.cases true x)) := by
  have nz (b : Bool) : bitSign b ≠ 0 := by cases b <;> decide
  exact TGLExt.Psibit.the_orbit_visits_all_four_states _ _ (nz _) (nz _)

def triple {n} (x y z : Assignment n) : Assignment n :=
  fun i => Bool.xor (Bool.xor (x i) (y i)) (z i)

theorem triple_value {n} (r : Row n) (x y z : Assignment n) :
    value r (triple x y z) = Bool.xor (Bool.xor (value r x) (value r y)) (value r z) := by
  induction r with
  | offset d => cases d <;> rfl
  | col c r ih =>
    have h := ih (fun i => x i.succ) (fun i => y i.succ) (fun i => z i.succ)
    change Bool.xor (c && _) (value r (triple _ _ _)) = _
    rw [h]
    simp only [value,triple]
    cases c <;> cases x 0 <;> cases y 0 <;> cases z 0 <;>
      cases value r (fun i => x i.succ) <;> cases value r (fun i => y i.succ) <;>
      cases value r (fun i => z i.succ) <;> rfl

theorem label_closed {n} (s : Label n) (x y z : Assignment n)
    (hx : fits s x = true) (hy : fits s y = true) (hz : fits s z = true) :
    fits s (triple x y z) = true := by
  induction s with
  | done _ => exact hx
  | slot p l ih =>
    cases p with
    | none =>
      simp only [fits,Option.elim_none,Bool.true_and] at *
      exact ih _ _ _ hx hy hz
    | some p =>
      simp only [fits,Option.elim_some,Bool.and_eq_true,beq_iff_eq] at hx hy hz ⊢
      refine ⟨?_,ih _ _ _ hx.2 hy.2 hz.2⟩
      change Bool.xor (Bool.xor (x 0) (y 0)) (z 0) = value p (triple _ _ _)
      rw [triple_value,hx.1,hy.1,hz.1]

def two (a b : Bool) : Assignment 2 := Fin.cases a (fun _ => b)

/-- Esta parede diz respeito a rótulos AFINS singulares. Uma única cláusula
    comum X₀∨X₁ já exige sair dessa classe se se quer conservar todo o suporte. -/
theorem ordinary_or_not_single_label :
    ¬ ∃ s : Label 2, ∀ x, fits s x = (x 0 || x 1) := by
  rintro ⟨s,hs⟩
  have h (a b : Bool) : fits s (two a b) = (a || b) := hs _
  have bad := label_closed s (two false true) (two true false) (two true true)
    (by rw [h]; rfl) (by rw [h]; rfl) (by rw [h]; rfl)
  rw [hs] at bad
  contradiction

/-- Leitura do bit final em uma passagem pelo rótulo serializado. A cauda
    do pivô é atravessada (e cobrada) mesmo quando não é usada na resposta. -/
def scanWord : {n : Nat} → Label n → Bool × Nat
  | _, .done d => (!d,1)
  | k+1,.slot p l =>
    let z := scanWord l
    (z.1,1+(p.elim 0 (fun _ => k+1))+z.2)

theorem scan_spec {n} (s : Label n) : scanWord s = (readWord s,footprint s) := by
  induction s with
  | done d => rfl
  | slot p l ih => simp [scanWord,readWord,footprint,ih]

def decideRows {n} (eqns : List (Row n)) : Bool × Nat :=
  let out := run eqns (blank n)
  let ans := scanWord out.1
  (ans.1, (n+1)+out.2+ans.2)

theorem polynomial_affine {n} (eqns : List (Row n)) :
    ((decideRows eqns).1 = true ↔ ∃ x, eqns.all (fun r => !(value r x)) = true) ∧
    (decideRows eqns).2 ≤ (4*eqns.length+2)*(n+1)^2 := by
  constructor
  · simpa only [decideRows,scan_spec] using affine_word eqns
  · simp only [decideRows,scan_spec]
    have first := run_work eqns (blank n)
    have last := compact_size (run eqns (blank n)).1
    ring_nf at first last ⊢
    omega

/-- Depois de ligar x=y, duas continuações de pinos dão SIM e NÃO. -/
theorem conflicting_tests :
    (decideRows ([Constraint.link (0 : Fin 2) 1 false,.pin 0 false,.pin 1 false].map rowOf)).1 = true ∧
    (decideRows ([Constraint.link (0 : Fin 2) 1 false,.pin 0 false,.pin 1 true].map rowOf)).1 = false := by
  decide

end IALD.RotulosAfins
