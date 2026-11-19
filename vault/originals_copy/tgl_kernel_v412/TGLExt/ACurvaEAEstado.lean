import TGLExt.OPsiBitDaFormula

set_option autoImplicit false
set_option maxHeartbeats 800000

/-!
# A curva e o estado: a curva é a projeção do resumo; o estado é o par

## A obstrução que este arquivo responde

Os prefixos `x` e `¬x` têm o mesmo PsiBit e a mesma curva inteira da soma lida (a mesma partição para todo tempo), e
acrescentar a MESMA cláusula `x` produz fórmulas com Palavras opostas (`PalavrasResiduais`). Logo nem a curva
completa substitui a informação de qual valor sobreviveu: um estado de leitura que precise continuar pede distinção
(pelo menos n bits).

## A leitura que este arquivo tipa

A curva não substitui o estado porque a curva é a leitura (o ângulo de Miguel); não é dada de graça; seria a
releitura (o token ao quadrado), que não acrescenta nada [INPUT/ONTO: definição da teoria, entrada, não teorema].

Este arquivo prova a parte dela que cabe nos termos do kernel: **a curva é a projeção do resumo — a soma das células
da fronteira — e a projeção identifica o que o resumo distingue. O estado é o par (a tabela da fronteira).** Chamar a
curva de releitura, que não acrescenta, é a leitura acima [INPUT/ONTO].

## O que fica provado

1. `a_curva_e_a_soma_das_celulas`: a curva de um prefixo é a soma das células do resumo na fronteira (perda zero
   sobre o total; não sobre as células).
2. ★ `mesma_curva_para_todo_tempo`: os dois prefixos têm a mesma curva inteira, para todo tempo (a obstrução de
   `PalavrasResiduais`, nos termos de `OResumoEPsiBit`).
3. ★ `palavras_opostas_depois_da_mesma_clausula`: acrescentada a mesma cláusula, as Palavras ficam opostas.
4. ★★ `a_fronteira_distingue_os_prefixos`: os RESUMOS dos dois prefixos diferem (na célula do valor que sobrevive) —
   o estado é a tabela, não a curva.
5. ★ `a_curva_identifica_o_que_o_resumo_distingue`: a projeção (a soma) identifica os dois prefixos; a tabela não.
   (Que a curva seja a releitura do resumo é a leitura acima [INPUT/ONTO].)

Os itens 1 a 5 são provados no exemplo de uma variável (`CNF 1`); as células dos dois resumos diferem para `t ≠ 0`
(em `t = 0` todos os fatores valem 1). A projeção do prefixo em qualquer número de variáveis é
`Codex.FrontierProjection.total_projection` (arquivo `ProjecaoDaFronteira`).

(Auxiliares, marcados como tais: `sat_clausula_true_em_1`, `sat_clausula_false_em_1`, `flip1`,
`flip1_involutive`, `custo_flip1`.)

## O que NÃO se afirma

* Que a obstrução esteja errada: ela está certa — e é exatamente o que distingue o escalar (a curva) do par (o
  resumo). Este arquivo responde a ela mostrando que o estado da leitura é o resumo, que passa na obstrução.
* O "token ao quadrado" e o "ângulo de Miguel" são nomes da teoria [INPUT/ONTO]; o termo é a projeção do item 1, e a
  pedra `Psibit` do kernel tem outro portador — citação por nome.
* Nenhuma cota polinomial uniforme para toda CNF plana: essa cota continua a pergunta do Instituto, aberta e
  localizada (uma fronteira de largura `w` indexa `2^w` células).
* Nada sobre a natureza. Validade no kernel não é creditação.
-/

namespace TGLExt.ACurvaEAEstado

open TGLExt TGLExt.TraducaoTuring TGLExt.OResumoEPsiBit TGLExt.OPsiBitDaFormula

/-! ## 1. Os dois prefixos e as duas continuações -/

/-- [DEF] O prefixo positivo: a cláusula `x₀ = true`. -/
def prefixoPos : CNF 1 := [[⟨0, true⟩]]

/-- [DEF] O prefixo negativo: a cláusula `x₀ = false`. -/
def prefixoNeg : CNF 1 := [[⟨0, false⟩]]

/-- [DEF] A continuação comum sobre o prefixo positivo: a mesma cláusula `x₀ = true` acrescentada. -/
def continuacaoPos : CNF 1 := [[⟨0, true⟩], [⟨0, true⟩]]

/-- [DEF] A continuação comum sobre o prefixo negativo. -/
def continuacaoNeg : CNF 1 := [[⟨0, false⟩], [⟨0, true⟩]]

/-- [DEF] O levantamento de uma célula da fronteira a uma atribuição inteira (falso fora dela). -/
def levanta (F : Finset (Fin 1)) (v : ↥F → Bool) : Fin 1 → Bool :=
  fun i => if h : i ∈ F then v ⟨i, h⟩ else false

/-! ## 2. Auxiliares: a leitura das cláusulas unitárias e o flip -/

/-- A leitura da cláusula unitária `x₀ = true`, em uma variável. -/
theorem sat_clausula_true_em_1 (x : Fin 1 → Bool) :
    satisfeita ([⟨0, true⟩] : Clausula 1) x = (x 0 == true) :=
  Bool.or_false _

/-- A leitura da cláusula unitária `x₀ = false`, em uma variável. -/
theorem sat_clausula_false_em_1 (x : Fin 1 → Bool) :
    satisfeita ([⟨0, false⟩] : Clausula 1) x = (x 0 == false) :=
  Bool.or_false _

/-- [DEF] O FLIP de sinal em uma variável (auxiliar). -/
def flip1 : (Fin 1 → Bool) → (Fin 1 → Bool) := fun x i => !(x i)

/-- O flip é involução. -/
theorem flip1_involutive : Function.Involutive flip1 := fun x => by
  funext i
  simp only [flip1, Bool.not_not]

/-- O custo troca de sinal com o flip, literal a literal: `Literal.vale` é `==`. -/
theorem custo_flip1 (x : Fin 1 → Bool) :
    custoCNF prefixoNeg x = custoCNF prefixoPos (flip1 x) := by
  have hbool : ∀ b : Bool, (b == false) = ((Bool.not b) == true) := fun b => by cases b <;> rfl
  have hs : satisfeita ([⟨0, false⟩] : Clausula 1) x
      = satisfeita ([⟨0, true⟩] : Clausula 1) (flip1 x) := by
    rw [sat_clausula_false_em_1, sat_clausula_true_em_1]
    show (x 0 == false) = ((Bool.not (x 0)) == true)
    exact hbool (x 0)
  show custoCNF ([⟨0, false⟩] :: ([] : CNF 1)) x
    = custoCNF ([⟨0, true⟩] :: ([] : CNF 1)) (flip1 x)
  rw [custoCNF_cons, custoCNF_cons,
    show custoCNF ([] : CNF 1) x = 0 from rfl,
    show custoCNF ([] : CNF 1) (flip1 x) = 0 from rfl,
    zero_add, zero_add, hs]

/-! ## 3. Os cinco teoremas -/

/-- ★ **A CURVA É A SOMA DAS CÉLULAS**: a partição da parte lida é a soma dos valores do resumo sobre as células da
fronteira. (A curva é a projeção do resumo: perda zero sobre o total.) -/
theorem a_curva_e_a_soma_das_celulas (φ : CNF 1) (t : ℝ) (j : ℕ) :
    particao (custoCNF (φ.take j)) t
      = ∑ v : (↥(fronteira φ j) → Bool), resumo φ t j (levanta (fronteira φ j) v) := by
  classical
  rw [OResumoEPsiBit.particao_e_a_soma_dos_pesos, ← Finset.sum_fiberwise Finset.univ
    (leituraDaFronteira φ j) (fun x => pesoDas (φ.take j) t x)]
  refine Finset.sum_congr rfl fun v _ => ?_
  unfold resumo
  refine Finset.sum_congr ?_ fun x _ => rfl
  ext x
  simp only [Finset.mem_filter, Finset.mem_univ, true_and]
  constructor
  · -- a restrição de x é v → x coincide com o levantamento de v na fronteira
    intro hx i hi
    have h2 := congrFun hx ⟨i, hi⟩
    show x i = (if h : i ∈ fronteira φ j then v ⟨i, h⟩ else false)
    rw [dif_pos hi]
    exact h2
  · -- x coincide com o levantamento de v na fronteira → a restrição de x é v
    intro hx
    funext ⟨i, hi⟩
    have hxi : x i = (if h : i ∈ fronteira φ j then v ⟨i, h⟩ else false) := hx i hi
    rw [dif_pos hi] at hxi
    show x i = v ⟨i, hi⟩
    exact hxi

/-- ★ **A MESMA CURVA PARA TODO TEMPO**: os dois prefixos têm a mesma partição inteira, para todo tempo. (A
obstrução de `PalavrasResiduais`, nos termos de `OResumoEPsiBit`.) -/
theorem mesma_curva_para_todo_tempo (t : ℝ) :
    particao (custoCNF prefixoPos) t = particao (custoCNF prefixoNeg) t := by
  classical
  unfold particao
  exact Fintype.sum_equiv ⟨flip1, flip1, flip1_involutive, flip1_involutive⟩
    (fun x => Real.exp (-(t * (custoCNF prefixoPos x : ℝ))))
    (fun x => Real.exp (-(t * (custoCNF prefixoNeg x : ℝ))))
    (fun x => by
      show Real.exp (-(t * (custoCNF prefixoPos x : ℝ)))
        = Real.exp (-(t * (custoCNF prefixoNeg (flip1 x) : ℝ)))
      rw [custo_flip1 (flip1 x), flip1_involutive x])

/-- ★ **PALAVRAS OPOSTAS DEPOIS DA MESMA CLÁUSULA**: a continuação sobre o prefixo positivo satisfaz; sobre o
negativo, não. -/
theorem palavras_opostas_depois_da_mesma_clausula :
    palavraDaFormula continuacaoPos = true ∧ palavraDaFormula continuacaoNeg = false := by
  constructor
  · exact (a_palavra_e_o_sat _).mpr ⟨fun _ => true, by
      intro C hC
      have hC2 : C ∈ ([[⟨0, true⟩], [⟨0, true⟩]] : CNF 1) := hC
      simp only [List.mem_cons, List.not_mem_nil, or_false, or_self_iff] at hC2
      rw [hC2, sat_clausula_true_em_1]
      decide⟩
  · unfold palavraDaFormula
    rw [decide_eq_false_iff_not]
    rintro ⟨x, hx⟩
    have h0 := (custoCNF_zero_sse continuacaoNeg x).mp hx
    have hN : satisfeita ([⟨0, false⟩] : Clausula 1) x = true := h0 _ (by
      show ([⟨0, false⟩] : Clausula 1) ∈ ([[⟨0, false⟩], [⟨0, true⟩]] : CNF 1)
      exact List.mem_cons_self)
    have hP : satisfeita ([⟨0, true⟩] : Clausula 1) x = true := h0 _ (by
      show ([⟨0, true⟩] : Clausula 1) ∈ ([[⟨0, false⟩], [⟨0, true⟩]] : CNF 1)
      exact List.mem_cons_of_mem _ List.mem_cons_self)
    rw [sat_clausula_false_em_1] at hN
    rw [sat_clausula_true_em_1] at hP
    cases h : x 0 <;> simp [h] at hN hP

/-- ★★ **A FRONTEIRA DISTINGUE OS PREFIXOS**: os resumos diferem na célula do valor que sobrevive — o positivo tem
peso 1 aí; o negativo tem `e^{−t}`. O estado é a tabela; a curva não. -/
theorem a_fronteira_distingue_os_prefixos (t : ℝ) (ht : t ≠ 0) :
    resumo continuacaoPos t 1 (fun _ => true) ≠ resumo continuacaoNeg t 1 (fun _ => true) := by
  classical
  -- as variáveis das cláusulas unitárias são o vértice único
  have hvarsT : varsDas ([[⟨0, true⟩]] : CNF 1) = {0} := by
    ext i
    simp [varsDas, varsClausula]
  have hvarsF : varsDas ([[⟨0, false⟩]] : CNF 1) = {0} := by
    ext i
    simp [varsDas, varsClausula]
  -- as fronteiras depois de uma cláusula são o vértice único
  have hfrPos : fronteira continuacaoPos 1 = {0} := by
    show varsDas (continuacaoPos.take 1) ∩ varsDas (continuacaoPos.drop 1) = {0}
    have htake : continuacaoPos.take 1 = ([[⟨0, true⟩]] : CNF 1) := rfl
    have hdrop : continuacaoPos.drop 1 = ([[⟨0, true⟩]] : CNF 1) := rfl
    rw [htake, hdrop, hvarsT, Finset.inter_self]
  have hfrNeg : fronteira continuacaoNeg 1 = {0} := by
    show varsDas (continuacaoNeg.take 1) ∩ varsDas (continuacaoNeg.drop 1) = {0}
    have htake : continuacaoNeg.take 1 = ([[⟨0, false⟩]] : CNF 1) := rfl
    have hdrop : continuacaoNeg.drop 1 = ([[⟨0, true⟩]] : CNF 1) := rfl
    rw [htake, hdrop, hvarsF, hvarsT, Finset.inter_self]
  -- a fibra da célula `fun _ => true` é o singleton dela (em `Fin 1` só há o vértice 0)
  have hfibra : (Finset.univ.filter fun x : Fin 1 → Bool =>
        ∀ i ∈ ({0} : Finset (Fin 1)), x i = (fun _ => true) i)
      = {fun _ => true} := by
    ext x
    simp only [Finset.mem_filter, Finset.mem_univ, Finset.mem_singleton, true_and]
    constructor
    · intro hx
      funext i
      show x i = true
      rw [Fin.eq_zero i]
      exact hx 0 (by simp)
    · intro hx i _
      rw [hx]
  -- o resumo do positivo na célula que sobrevive: o fator é 1 (cláusula satisfeita)
  have hresPos : resumo continuacaoPos t 1 (fun _ => true) = 1 := by
    unfold resumo
    rw [hfrPos, hfibra, Finset.sum_singleton]
    show pesoDas ([[⟨0, true⟩]] : CNF 1) t (fun _ => true) = 1
    show (List.map (fun C => fator C t (fun _ => true)) [[⟨0, true⟩]]).prod = 1
    rw [List.map_cons, List.map_nil, List.prod_singleton]
    show (if satisfeita ([⟨0, true⟩] : Clausula 1) (fun _ => true) then 1 else Real.exp (-t)) = 1
    rw [sat_clausula_true_em_1]
    rfl
  -- o resumo do negativo na mesma célula: o fator é e^{−t} (cláusula violada)
  have hresNeg : resumo continuacaoNeg t 1 (fun _ => true) = Real.exp (-t) := by
    unfold resumo
    rw [hfrNeg, hfibra, Finset.sum_singleton]
    show pesoDas ([[⟨0, false⟩]] : CNF 1) t (fun _ => true) = Real.exp (-t)
    show (List.map (fun C => fator C t (fun _ => true)) [[⟨0, false⟩]]).prod = Real.exp (-t)
    rw [List.map_cons, List.map_nil, List.prod_singleton]
    show (if satisfeita ([⟨0, false⟩] : Clausula 1) (fun _ => true) then 1 else Real.exp (-t)) = Real.exp (-t)
    rw [sat_clausula_false_em_1]
    rfl
  -- e^{−t} ≠ 1 para t ≠ 0
  have hexp : (1 : ℝ) ≠ Real.exp (-t) := by
    rcases lt_or_gt_of_ne ht with h | h
    · have h1 : (1 : ℝ) < Real.exp (-t) := by
        rw [Real.one_lt_exp_iff]
        linarith
      exact ne_of_lt h1
    · have h2 : Real.exp (-t) < 1 := by
        rw [Real.exp_lt_one_iff]
        linarith
      exact (ne_of_lt h2).symm
  rw [hresPos, hresNeg]
  exact hexp

/-- ★ **A CURVA IDENTIFICA O QUE O RESUMO DISTINGUE**: a projeção (a soma das células) identifica os dois prefixos;
a tabela (o resumo) não. -/
theorem a_curva_identifica_o_que_o_resumo_distingue (t : ℝ) (ht : t ≠ 0) :
    particao (custoCNF prefixoPos) t = particao (custoCNF prefixoNeg) t
    ∧ resumo continuacaoPos t 1 (fun _ => true) ≠ resumo continuacaoNeg t 1 (fun _ => true) :=
  ⟨mesma_curva_para_todo_tempo t, a_fronteira_distingue_os_prefixos t ht⟩

end TGLExt.ACurvaEAEstado
