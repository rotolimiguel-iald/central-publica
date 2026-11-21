import TGLExt.APonteDeCookLevin
import Mathlib.Computability.Primrec.Basic
import Mathlib.Computability.Primrec.List
import Mathlib.Computability.Partrec
import Mathlib.Computability.TuringMachine.Computable

set_option autoImplicit false
set_option maxHeartbeats 800000

/-!
# Ponte ao TM2, com codificações fixas

Verificação semântica e recursividade; alfabeto e gramática da fita; o decodificador, a cota de tamanho e a
especificação concreta da saída.
-/

namespace TGLExt.APonteAoTM2

open TGLExt TGLExt.TraducaoTuring TGLExt.AContagemEACarga TGLExt.AMaquinaEALeitura TGLExt.APonteDeCookLevin

/-- [DEF] A verificação lida da fita: toda cláusula tem um literal cujo bit na testemunha bate com a polaridade.
(O `getElem?` devolve `none` fora da fita — e `none ≠ some`: quem não está na fita não satisfaz. É a leitura da
borda da irmã `AFitaEOIndice`: quem não visita não lê.) -/
def verificaNaFita (φf : List (List (ℕ × Bool))) (bits : List Bool) : Bool :=
  φf.all fun C => C.any fun p => (bits[p.1]? == some p.2)

variable {n : ℕ}

/-- [DEF] A fórmula na fita: cada cláusula vira a lista dos seus literais, e cada literal o par
(índice da variável, polaridade) — o que se escreve na fita. -/
def aFormulaNaFita (φ : CNF n) : List (List (ℕ × Bool)) :=
  φ.map fun C => C.map fun l => (l.var.val, l.pos)

/-- [DEF] A atribuição na fita: os bits da testemunha, na ordem das variáveis. -/
def aAtribuicaoNaFita (x : Fin n → Bool) : List Bool :=
  List.ofFn x

/-- O bit da fita na posição de um literal é o valor da variável: a leitura da fita bate com a leitura da casa.
(Auxiliar do enraizamento.) -/
theorem o_bit_da_fita_e_o_da_casa (x : Fin n → Bool) (l : Literal n) :
    ((List.ofFn x)[l.var.val]? == some l.pos) = l.vale x := by
  rw [List.getElem?_ofFn, dif_pos l.var.isLt]
  rfl

/-- O custo zero é o sim: nenhuma cláusula violada se, e só se, todas satisfeitas. (Auxiliar do enraizamento.) -/
theorem custo_zero_sse_toda_satisfeita (φ : CNF n) (x : Fin n → Bool) :
    custoCNF φ x = 0 ↔ ∀ C ∈ φ, satisfeita C x = true := by
  induction φ with
  | nil => simp [custoCNF]
  | cons C ψ ih =>
    have hdef : custoCNF (C :: ψ) x = (if satisfeita C x then 0 else 1) + custoCNF ψ x := by
      unfold custoCNF
      rw [List.countP_cons]
      by_cases h : satisfeita C x <;> simp [h, Nat.add_comm]
    rw [hdef]
    constructor
    · intro h
      rw [List.forall_mem_cons]
      refine ⟨?_, ih.mp ?_⟩
      · by_cases hC : satisfeita C x
        · exact hC
        · simp [hC] at h
      · by_cases hC : satisfeita C x
        · simpa [hC] using h
        · simp [hC] at h
    · intro h
      rw [List.forall_mem_cons] at h
      have hψ := ih.mpr h.2
      simp [h.1, hψ]

/-- ★ **A VERIFICAÇÃO NA FITA É A DA CASA**: verificar a fórmula na fita com a testemunha na fita é decidir o
mesmo sim da casa — custo zero. -/
theorem a_verificacao_na_fita_e_a_da_casa (φ : CNF n) (x : Fin n → Bool) :
    verificaNaFita (aFormulaNaFita φ) (aAtribuicaoNaFita x) = decide (custoCNF φ x = 0) := by
  have hcel : ∀ C : Clausula n,
      ((C.map fun l => (l.var.val, l.pos)).any fun p => ((List.ofFn x)[p.1]? == some p.2))
        = satisfeita C x := by
    intro C
    rw [List.any_map]
    show C.any ((fun p => ((List.ofFn x)[p.1]? == some p.2)) ∘ fun l => (↑l.var, l.pos))
        = C.any fun l => l.vale x
    congr 1
    funext l
    show ((List.ofFn x)[l.var.val]? == some l.pos) = l.vale x
    exact o_bit_da_fita_e_o_da_casa x l
  have hiff : (verificaNaFita (aFormulaNaFita φ) (aAtribuicaoNaFita x) = true)
      ↔ ∀ C ∈ φ, satisfeita C x = true := by
    unfold verificaNaFita aFormulaNaFita aAtribuicaoNaFita
    rw [List.all_eq_true, List.forall_mem_map]
    constructor
    · intro h C hC
      rw [← hcel C]
      exact h C hC
    · intro h C hC
      rw [hcel C]
      exact h C hC
  rw [decide_eq_decide.mpr (custo_zero_sse_toda_satisfeita φ x)]
  by_cases hP : ∀ C ∈ φ, satisfeita C x = true
  · rw [decide_eq_true_eq.mpr hP]
    exact hiff.mpr hP
  · rw [decide_eq_false_iff_not.mpr hP]
    exact Bool.eq_false_iff.mpr fun hXt => hP (hiff.mp hXt)

/-- ★ **A FITA TEM AS LETRAS**: o comprimento da fórmula na fita (os literais) mais um terminador por cláusula é
exatamente `letras φ`, a contagem definida em `APonteDeCookLevin`. -/
theorem a_fita_tem_as_letras (φ : CNF n) :
    (aFormulaNaFita φ).flatten.length + φ.length = letras φ := by
  induction φ with
  | nil => rfl
  | cons C ψ ih =>
    show (((C.map fun l => (l.var.val, l.pos)) :: ψ.map fun C' => C'.map fun l => (l.var.val, l.pos)).flatten).length
        + (C :: ψ).length = letras (C :: ψ)
    rw [List.flatten_cons, List.length_append, List.length_map, List.length_cons,
      show letras (C :: ψ) = C.length + letras ψ + 1 from by
        unfold letras
        rw [List.map_cons, List.sum_cons, List.length_cons]
        ring]
    unfold aFormulaNaFita at ih
    omega

/-- As duas instâncias de `BEq (Option Bool)` concordam ponto a ponto. (Auxiliar do laço: a notação `==` dos
enunciados elabora com `Option.instBEq`; o lema `Primrec.beq` da biblioteca carrega `instBEqOfDecidableEq`.) -/
theorem beq_option_agree : ∀ a b : Option Bool,
    @BEq.beq _ instBEqOfDecidableEq a b = @BEq.beq _ Option.instBEq a b := by
  intro a b
  cases a <;> cases b
  · rfl
  · rfl
  · rfl
  · show decide (some _ = some _) = decide (_ = _)
    simp only [Option.some.injEq]

/-- O passo do literal é primitivo recursivo: ler o bit da posição e conferir a polaridade. (Auxiliar.) -/
private theorem passoLiteral_primrec :
    Primrec fun q : List Bool × (ℕ × Bool) => (q.1[q.2.1]? == some q.2.2) :=
  (Primrec.beq.comp
    ((Primrec.list_getElem? (α := Bool)).comp Primrec.fst (Primrec.fst.comp Primrec.snd))
    (Primrec.option_some.comp (Primrec.snd.comp Primrec.snd))).of_eq fun q =>
    beq_option_agree (q.1[q.2.1]?) (some q.2.2)

/-- O passo da cláusula é primitivo recursivo: algum literal bate. (Auxiliar.) -/
private theorem passoClausula_primrec :
    Primrec fun q : List Bool × List (ℕ × Bool) => q.2.any fun p => (q.1[p.1]? == some p.2) := by
  have hpasso : Primrec₂ fun (q : List Bool × List (ℕ × Bool)) (ps : (ℕ × Bool) × Bool) =>
      ((q.1[ps.1.1]? == some ps.1.2) || ps.2) := by
    show Primrec fun r : (List Bool × List (ℕ × Bool)) × ((ℕ × Bool) × Bool) =>
      ((r.1.1[r.2.1.1]? == some r.2.1.2) || r.2.2)
    exact Primrec.or.comp
      (passoLiteral_primrec.comp
        (Primrec.pair (Primrec.fst.comp Primrec.fst) (Primrec.fst.comp Primrec.snd)))
      (Primrec.snd.comp Primrec.snd)
  have hfold : Primrec fun q : List Bool × List (ℕ × Bool) =>
      q.2.foldr (fun p s => ((q.1[p.1]? == some p.2) || s)) false :=
    Primrec.list_foldr Primrec.snd (Primrec.const false) hpasso
  exact hfold.of_eq fun q => by
    induction q.2 with
    | nil => rfl
    | cons p l ih => simp only [List.any_cons, List.foldr_cons, ih]

/-- ★ **A VERIFICAÇÃO É RECURSIVA PRIMITIVA**: a leitura do certificado está nas funções primitivas recursivas —
total, sem busca, só dobradura sobre a fita. É o piso de Hilbert: a verificação não é apenas
computável, é das funções mais simples que a computação clássica conhece acima das básicas. -/
theorem a_verificacao_e_recursiva_primitiva : Primrec₂ verificaNaFita := by
  have hpasso : Primrec₂ fun (q : List (List (ℕ × Bool)) × List Bool) (ps : List (ℕ × Bool) × Bool) =>
      ((ps.1.any fun p => (q.2[p.1]? == some p.2)) && ps.2) := by
    show Primrec fun r : (List (List (ℕ × Bool)) × List Bool) × (List (ℕ × Bool) × Bool) =>
      ((r.2.1.any fun p => (r.1.2[p.1]? == some p.2)) && r.2.2)
    exact Primrec.and.comp
      (passoClausula_primrec.comp
        (Primrec.pair (Primrec.snd.comp Primrec.fst) (Primrec.fst.comp Primrec.snd)))
      (Primrec.snd.comp Primrec.snd)
  have hfold : Primrec fun q : List (List (ℕ × Bool)) × List Bool =>
      q.1.foldr (fun C s => ((C.any fun p => (q.2[p.1]? == some p.2)) && s)) true :=
    Primrec.list_foldr Primrec.fst (Primrec.const true) hpasso
  exact hfold.of_eq fun q => by
    induction q.1 with
    | nil => simp only [List.foldr_nil, verificaNaFita, List.all_nil]
    | cons C l ih => simp only [List.all_cons, List.foldr_cons, ih, verificaNaFita]

/-- ★ **A VERIFICAÇÃO É TURING-COMPUTÁVEL NA LÍNGUA CLÁSSICA**: toda recursiva primitiva é computável
(`Primrec₂.to_comp`). A verificação da casa entra na hierarquia clássica pelo piso mais alto. -/
theorem a_verificacao_e_computavel : Computable₂ verificaNaFita :=
  a_verificacao_e_recursiva_primitiva.to_comp

/-- [DEF] O alfabeto da fita: oito letras. -/
inductive Simbolo where
  | tick | litT | litF | fimC | fimF | sep | um | zero
  deriving DecidableEq, Fintype

/-- [DEF] O literal na fita: o marcador com a polaridade, e o índice em unário (ticks). -/
def codificaLiteral (p : ℕ × Bool) : List Simbolo :=
  (if p.2 then Simbolo.litT else Simbolo.litF) :: List.replicate p.1 Simbolo.tick

/-- [DEF] A cláusula na fita: os literais em sequência, fechados pelo terminador. -/
def codificaClausula (C : List (ℕ × Bool)) : List Simbolo :=
  C.flatMap codificaLiteral ++ [Simbolo.fimC]

/-- [DEF] A fórmula na fita: as cláusulas em sequência, fechadas pelo terminador. -/
def codificaFormula (φf : List (List (ℕ × Bool))) : List Simbolo :=
  φf.flatMap codificaClausula ++ [Simbolo.fimF]

/-- [DEF] A testemunha na fita: os bits, em ordem. -/
def codificaBits (bits : List Bool) : List Simbolo :=
  bits.map fun b => if b then Simbolo.um else Simbolo.zero

/-- [DEF] A entrada na fita: a fórmula, a divisória, a testemunha. -/
def codificaEntrada (p : List (List (ℕ × Bool)) × List Bool) : List Simbolo :=
  codificaFormula p.1 ++ [Simbolo.sep] ++ codificaBits p.2


/-- A saída usa exatamente uma célula booleana. -/
def codificaSaida (b : Bool) : List Bool := [b]

private abbrev Raw := List (List (ℕ × Bool))

/-- O leitor dobra a fita da direita para a esquerda. Na fase da fórmula, o contador
guarda os ticks do próximo marcador e a primeira cláusula é a cláusula em construção. -/
private inductive ReadState where
  | witness (bits : List Bool)
  | separator (bits : List Bool)
  | formula (ticks : ℕ) (clauses : Raw) (bits : List Bool)
  | invalid

private def readSymbol : Simbolo → ReadState → ReadState
  | .um, .witness bs => .witness (true :: bs)
  | .zero, .witness bs => .witness (false :: bs)
  | .sep, .witness bs => .separator bs
  | .fimF, .separator bs => .formula 0 [] bs
  | .fimC, .formula 0 cs bs => .formula 0 ([] :: cs) bs
  | .tick, .formula i (c :: cs) bs => .formula (i+1) (c :: cs) bs
  | .litT, .formula i (c :: cs) bs => .formula 0 (((i,true) :: c) :: cs) bs
  | .litF, .formula i (c :: cs) bs => .formula 0 (((i,false) :: c) :: cs) bs
  | _, _ => .invalid

def decodificaEntrada (word : List Simbolo) : Option (List (List (ℕ × Bool)) × List Bool) :=
  match word.foldr readSymbol (.witness []) with
  | .formula 0 cs bs => some (cs, bs)
  | _ => none

private theorem readBits (bs : List Bool) :
    (codificaBits bs).foldr readSymbol (.witness []) = .witness bs := by
  induction bs with
  | nil => rfl
  | cons b bs ih => cases b <;> simp_all [codificaBits, readSymbol]

private theorem readTicks (i : ℕ) (c : List (ℕ × Bool)) (cs : Raw) (bs : List Bool) :
    (List.replicate i Simbolo.tick).foldr readSymbol (.formula 0 (c :: cs) bs) =
      .formula i (c :: cs) bs := by
  induction i with
  | zero => rfl
  | succ i ih => simp only [List.replicate_succ, List.foldr_cons, ih, readSymbol]

private theorem readLiterals (ls c : List (ℕ × Bool)) (cs : Raw) (bs : List Bool) :
    (ls.flatMap codificaLiteral).foldr readSymbol (.formula 0 (c :: cs) bs) =
      .formula 0 ((ls ++ c) :: cs) bs := by
  induction ls with
  | nil => rfl
  | cons p ls ih =>
    rcases p with ⟨i, sign⟩
    cases sign <;> simp [codificaLiteral, List.foldr_append, ih, readTicks, readSymbol]

private theorem readClauses (cs tail : Raw) (bs : List Bool) :
    (cs.flatMap codificaClausula).foldr readSymbol (.formula 0 tail bs) =
      .formula 0 (cs ++ tail) bs := by
  induction cs with
  | nil => rfl
  | cons c cs ih =>
    simp [codificaClausula, List.foldr_append, ih, readSymbol, readLiterals]

theorem decodifica_codifica (p : List (List (ℕ × Bool)) × List Bool) :
    decodificaEntrada (codificaEntrada p) = some p := by
  rcases p with ⟨cs, bs⟩
  simp [decodificaEntrada, codificaEntrada, codificaFormula, List.foldr_append,
    readBits, readSymbol, readClauses]

theorem codificaEntrada_injetiva : Function.Injective codificaEntrada := by
  intro p q h
  simpa only [decodifica_codifica, Option.some.injEq] using congrArg decodificaEntrada h

theorem cardinal_do_alfabeto : Fintype.card Simbolo = 8 := by decide

/-- A máquina identidade tem a mesma pilha para entrada e saída. As duas equivalências
de alfabeto exigidas pela Mathlib seriam incompatíveis para essa máquina. -/
theorem identidade_incompativel {A : Type} (entrada : A ≃ Simbolo) (saida : A ≃ Bool) : False := by
  have h := Fintype.card_congr (entrada.symm.trans saida)
  rw [cardinal_do_alfabeto, Fintype.card_bool] at h
  contradiction

theorem codificaSaida_injetiva : Function.Injective codificaSaida := by
  intro a b h
  simpa [codificaSaida] using h

private theorem sumIndices (n : ℕ) (ls : List (ℕ × Bool))
    (h : ∀ p ∈ ls, p.1 < n) : (ls.map Prod.fst).sum ≤ ls.length * n := by
  induction ls with
  | nil => simp
  | cons p ls ih =>
    have hp := (h p List.mem_cons_self).le
    have ht := ih (fun q hq => h q (List.mem_cons_of_mem _ hq))
    simp only [List.map_cons, List.sum_cons, List.length_cons, Nat.succ_mul]
    omega

/-- A fita conta explicitamente cada tick, marcador, terminador, divisória e bit. -/
theorem comprimento_exato (cs : List (List (ℕ × Bool))) (bs : List Bool) :
    (codificaEntrada (cs, bs)).length =
      (cs.flatten.map Prod.fst).sum + cs.flatten.length + cs.length + bs.length + 2 := by
  have hc (c : List (ℕ × Bool)) : (c.flatMap codificaLiteral).length =
      (c.map Prod.fst).sum + c.length := by
    induction c with
    | nil => rfl
    | cons p c ih =>
      simp only [List.flatMap_cons, List.length_append, ih, List.map_cons, List.sum_cons,
        List.length_cons, codificaLiteral, List.length_replicate]
      omega
  have hf (f : List (List (ℕ × Bool))) :
      (f.flatMap codificaClausula).length =
        (f.flatten.map Prod.fst).sum + f.flatten.length + f.length := by
    induction f with
    | nil => rfl
    | cons c f ih =>
      simp only [List.flatMap_cons, List.length_append, ih, codificaClausula, hc,
        List.length_nil, List.flatten_cons, List.map_append, List.sum_append, List.length_cons]
      omega
  simp [codificaEntrada, codificaBits, codificaFormula, hf]
  omega

/-- Um mesmo polinômio serve para toda CNF n e toda testemunha com n bits. -/
theorem comprimento_em_letras_e_bits (φ : CNF n) (x : Fin n → Bool) :
    (codificaEntrada (aFormulaNaFita φ, aAtribuicaoNaFita x)).length ≤
      (letras φ + 1) * (n + 1) + 1 := by
  let f := aFormulaNaFita φ
  have hb : ∀ p ∈ f.flatten, p.1 < n := by
    intro p hp
    obtain ⟨c, hc, hp⟩ := List.mem_flatten.mp hp
    obtain ⟨C, _, rfl⟩ := List.mem_map.mp hc
    obtain ⟨l, _, rfl⟩ := List.mem_map.mp hp
    exact l.var.isLt
  have hs := sumIndices n f.flatten hb
  have hl : f.flatten.length + φ.length = letras φ := a_fita_tem_as_letras φ
  have hm := Nat.mul_le_mul_right n (show f.flatten.length ≤ letras φ by omega)
  have hf : f.length = φ.length := by simp [f, aFormulaNaFita]
  rw [comprimento_exato]
  change (f.flatten.map Prod.fst).sum + f.flatten.length + f.length +
    (List.ofFn x).length + 2 ≤ _
  rw [List.length_ofFn, Nat.mul_succ, Nat.succ_mul]
  omega

theorem comprimento_quadratico (φ : CNF n) (x : Fin n → Bool) :
    (codificaEntrada (aFormulaNaFita φ, aAtribuicaoNaFita x)).length ≤
      (letras φ + n + 1)^2 + 1 := by
  apply (comprimento_em_letras_e_bits φ x).trans
  rw [pow_two]
  exact Nat.add_le_add_right (Nat.mul_le_mul (by omega) (by omega)) 1

/-- Em entradas cruas um índice fora da testemunha é permitido pelo verificador.
Aqui o número de literais, de cláusulas e de bits é constante enquanto a fita cresce. -/
theorem comprimento_indice_cru (i : ℕ) :
    (codificaEntrada ([[(i,true)]], [])).length = i + 4 := by simp [comprimento_exato]

/-- Especificação fixa do verificador. Construir um habitante exige a simulação geral. -/
def ObjetivoTM2Polinomial : Prop :=
  Nonempty (Turing.TM2ComputableInPolyTime codificaEntrada codificaSaida
    (fun p => verificaNaFita p.1 p.2))

end TGLExt.APonteAoTM2
