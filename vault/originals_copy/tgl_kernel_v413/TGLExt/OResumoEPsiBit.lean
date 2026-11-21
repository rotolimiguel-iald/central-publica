import TGLExt.TraducaoTuring

set_option autoImplicit false
set_option maxHeartbeats 800000

/-!
# O resumo e a fronteira: a compressão sai da fórmula, e a parede fica de pé

## A pergunta que este arquivo responde

**De onde sai a compressão?** Se o leitor comprime o sinal já estendido, leu o todo, e a contagem por letra continua
2ⁿ. Se comprime direto da fórmula, cláusula por cláusula, guardando um resumo que baste para reconstruir a resposta,
o que decide é o tamanho desse resumo.

## A leitura que este arquivo tipa

A compressão sai direto da fórmula; é o PsiBit; a leitura do par binário pelo PsiBit é a compressão originária, o
próprio leitor [INPUT/ONTO: definição da teoria, entrada, não teorema]. Este arquivo prova a parte dela que cabe nos
termos do kernel, e diz exatamente onde a parede fica.

Termos em que este arquivo se apoia: o fator da cláusula como a lei dos dois valores (`OPassoEORetorno.o_retorno_e_o_if`), o custo
da fórmula como a soma dos `if`s, o leitor como o produto dos fatores, e a carga da instância como `n·ln 2`
(`AContagemEACarga`). O termo deste arquivo: a forma do resumo que a leitura carrega entre uma cláusula e a seguinte.

## O que fica provado

1. `peso_e_o_produto_dos_fatores` e `particao_e_a_soma_dos_pesos`: a trava escrita como o produto dos fatores das
   cláusulas (a conta de `OPassoEORetorno`, aqui só com o kernel).
2. `satisfeita_so_ve_as_suas_variaveis` e `peso_so_ve_as_variaveis_lidas`: a cláusula não vê o que ela não menciona;
   a parte lida não vê o que as suas cláusulas não mencionam.
3. ★ `o_resumo_so_ve_a_fronteira` e `a_fronteira_basta_ao_resumo`: o resumo depois de `j` cláusulas é uma função da
   célula da fronteira — as variáveis que ligam o lido ao não lido — e de mais nada.
4. `a_fronteira_tem_duas_elevado_as_celulas`: a tabela do resumo tem `2^{|fronteira|}` células; com a fronteira plena
   são `2ⁿ` (item 7).
5. ★★ `a_leitura_pela_fronteira_e_exata`: a soma lida inteira é a soma, célula a célula da fronteira, dos produtos do
   peso lido pelo peso por ler das atribuições que caem na célula — agrupar pela fronteira não perde nada da soma. (A
   soma simples das células do resumo dá a partição do prefixo: `Codex.FrontierProjection.total_projection` (arquivo `ProjecaoDaFronteira`).)
6. ★ `a_atualizacao_pela_clausula_seguinte`: o resumo depois da cláusula seguinte é a soma, sobre as atribuições que
   caem na célula nova, do peso lido antes multiplicado pelo fator da cláusula (1 ou `e^{−t}`). A identidade é escrita
   sobre atribuições completas: expande o peso pelo fator novo. A recorrência de tabela a tabela (estender às variáveis
   novas e contrair as que saíram da fronteira) é `Codex.FrontierUpdate.transition` (arquivo `TransicaoDaFronteira`).
7. ★ `a_parede_de_todas_as_variaveis`: duas ocorrências da cláusula de todas as variáveis põem a fronteira igual ao
   universo depois da primeira leitura — aí o resumo é o todo, com `2ⁿ` células. A pergunta do Instituto não é tocada.

## Como ler

**O que é o resumo depois de ler uma cláusula?** A tabela sobre a fronteira: as variáveis que as cláusulas já
lidas ainda partilham com as por ler. Em cada célula, a soma dos pesos lidos de todas as atribuições que nela
caem. É o estado do leitor; é a compressão.

**Como a cláusula seguinte o atualiza?** Pelo fator dela: 1 se a cláusula é satisfeita, `e^{−t}` se não (a lei dos
dois valores). Neste arquivo a identidade é escrita sobre atribuições completas. A regra que leva a tabela de uma
fronteira à tabela da seguinte, estendendo às variáveis novas e contraindo as que nenhuma cláusula futura toca, é
`Codex.FrontierUpdate.transition` (arquivo `TransicaoDaFronteira`).

**De onde sai a compressão?** Direto da fórmula — mas a tabela do resumo tem `2^w` células, com `w` a largura
da fronteira. E há fórmula cuja fronteira é o universo (item 7): aí são `2ⁿ` células.

## O que NÃO se afirma

* Que o resumo seja pequeno para TODA fórmula: uma fronteira de largura `w` indexa `2^w` células; a parede do item 7
  mostra o caso pior. O termo conta células; a escolha da melhor ordem de leitura (na literatura, a eliminação por
  balde e a largura de árvore da fórmula [KNOWN; Dechter e a decomposição em árvore; não é termo deste arquivo]) e o
  tempo de execução são outras questões.
* Que da fronteira pequena saia o tempo polinomial na máquina de fita: é a pergunta do Instituto, intocada.
* Que a compressão SEJA o PsiBit por termo: essa identidade é definição da teoria [INPUT/ONTO]. O que está em
  termo é: a leitura por cláusula é a lei dos dois valores (o par), o resumo é exato e mora na fronteira. A pedra
  `Psibit` do kernel (a leitura do par é necessária, suficiente e sem perda) tem outro portador (a órbita da
  matriz-S); nenhuma ponte nova entre ela e este arquivo é construída aqui — a citação é por nome.
* Nada sobre a natureza. Validade no kernel não é creditação.
-/

namespace TGLExt.OResumoEPsiBit

open TGLExt TGLExt.TraducaoTuring

variable {n : ℕ}

/-! ## 1. Variáveis, fronteira, fator e peso -/

/-- [DEF] As variáveis de uma cláusula. -/
def varsClausula (C : Clausula n) : Finset (Fin n) := (C.map Literal.var).toFinset

/-- [DEF] As variáveis de uma lista de cláusulas. -/
def varsDas (φ : CNF n) : Finset (Fin n) := (φ.map varsClausula).foldr (· ∪ ·) ∅

/-- [DEF] A FRONTEIRA depois de `j` cláusulas lidas: as variáveis que ligam o lido ao que falta. -/
def fronteira (φ : CNF n) (j : ℕ) : Finset (Fin n) := varsDas (φ.take j) ∩ varsDas (φ.drop j)

/-- [DEF] O FATOR da cláusula no tempo `t` (a lei dos dois valores: 1 se ela vale, `e^{−t}` se está violada). -/
noncomputable def fator (C : Clausula n) (t : ℝ) (x : Fin n → Bool) : ℝ := if satisfeita C x then 1 else Real.exp (-t)

/-- [DEF] O PESO de uma atribuição sobre uma lista de cláusulas: o produto dos fatores. -/
noncomputable def pesoDas (φ : CNF n) (t : ℝ) (x : Fin n → Bool) : ℝ := (φ.map fun C => fator C t x).prod

/-- O fator é a exponencial do `if` da cláusula. -/
theorem fator_eq_exp (C : Clausula n) (t : ℝ) (x : Fin n → Bool) :
    fator C t x = Real.exp (-(t * (if satisfeita C x then (0 : ℝ) else 1))) := by
  unfold fator
  cases satisfeita C x <;> simp

/-- O peso é a exponencial de menos `t` vezes o custo parcial. -/
theorem pesoDas_eq_exp (φ : CNF n) (t : ℝ) (x : Fin n → Bool) :
    pesoDas φ t x = Real.exp (-(t * (φ.countP fun C => !(satisfeita C x) : ℕ))) := by
  induction φ with
  | nil => simp [pesoDas]
  | cons C ψ ih =>
      have hstep : pesoDas (C :: ψ) t x = fator C t x * pesoDas ψ t x := rfl
      rw [hstep, ih, fator_eq_exp, ← Real.exp_add, List.countP_cons]
      congr 1
      cases satisfeita C x <;> simp
      ring

/-- **A PARTIÇÃO É A SOMA DOS PESOS**: a soma lida sobre o custo da fórmula é a soma dos pesos. -/
theorem particao_e_a_soma_dos_pesos (φ : CNF n) (t : ℝ) :
    particao (custoCNF φ) t = ∑ x : Fin n → Bool, pesoDas φ t x := by
  unfold particao
  refine Finset.sum_congr rfl fun x _ => ?_
  rw [pesoDas_eq_exp]
  rfl

/-- **O PESO É O PRODUTO DOS FATORES** (forma registrada; a mesma conta de `OPassoEORetorno`). -/
theorem peso_e_o_produto_dos_fatores (φ : CNF n) (t : ℝ) (x : Fin n → Bool) :
    Real.exp (-(t * (custoCNF φ x : ℝ))) = pesoDas φ t x := by
  rw [pesoDas_eq_exp]
  rfl

/-! ## 2. A cláusula não vê o que ela não menciona -/

/-- A variável de um literal de uma cláusula está nas variáveis dela. -/
theorem var_mem_varsClausula {C : Clausula n} {l : Literal n} (hl : l ∈ C) : l.var ∈ varsClausula C := by
  unfold varsClausula
  rw [List.mem_toFinset]
  exact List.mem_map.mpr ⟨l, hl, rfl⟩

/-- ★ **A CLÁUSULA NÃO VÊ O QUE ELA NÃO MENCIONA**: duas atribuições que concordam nas variáveis da cláusula dão o
mesmo veredito. -/
theorem satisfeita_so_ve_as_suas_variaveis (C : Clausula n) {x y : Fin n → Bool}
    (h : ∀ i ∈ varsClausula C, x i = y i) : satisfeita C x = satisfeita C y := by
  induction C with
  | nil => rfl
  | cons l ψ ih =>
      have hsub : ∀ i ∈ varsClausula ψ, x i = y i := by
        intro i hi
        apply h i
        unfold varsClausula at hi ⊢
        rw [List.map_cons, List.toFinset_cons]
        exact Finset.mem_insert_of_mem hi
      have hl : l.vale x = l.vale y := by
        have hmem : l.var ∈ varsClausula (l :: ψ) := by
          unfold varsClausula
          rw [List.map_cons, List.toFinset_cons]
          exact Finset.mem_insert_self _ _
        unfold Literal.vale
        rw [h l.var hmem]
      show (l.vale x || satisfeita ψ x) = (l.vale y || satisfeita ψ y)
      rw [hl, ih hsub]

/-- Uma variável das variáveis de uma cláusula da lista está nas variáveis da lista. -/
theorem mem_varsDas_of_mem {φ : CNF n} {C : Clausula n} (hC : C ∈ φ) {i : Fin n}
    (hi : i ∈ varsClausula C) : i ∈ varsDas φ := by
  induction φ with
  | nil => exact absurd hC List.not_mem_nil
  | cons D ψ ih =>
      unfold varsDas
      rw [List.map_cons, List.foldr_cons]
      simp only [List.mem_cons] at hC
      rcases hC with rfl | hC
      · exact Finset.mem_union_left _ hi
      · exact Finset.mem_union_right _ (ih hC)

/-- ★ **A PARTE LIDA NÃO VÊ O QUE AS SUAS CLÁUSULAS NÃO MENCIONAM.** -/
theorem peso_so_ve_as_variaveis_lidas (φ : CNF n) (t : ℝ) {x y : Fin n → Bool}
    (h : ∀ i ∈ varsDas φ, x i = y i) : pesoDas φ t x = pesoDas φ t y := by
  induction φ with
  | nil => rfl
  | cons C ψ ih =>
      have hsub : ∀ i ∈ varsDas ψ, x i = y i := by
        intro i hi
        apply h i
        unfold varsDas
        rw [List.map_cons, List.foldr_cons]
        exact Finset.mem_union_right _ hi
      have hC : satisfeita C x = satisfeita C y :=
        satisfeita_so_ve_as_suas_variaveis C (fun i hi =>
          h i (mem_varsDas_of_mem List.mem_cons_self hi))
      have hf : fator C t x = fator C t y := by
        unfold fator
        rw [hC]
      show fator C t x * pesoDas ψ t x = fator C t y * pesoDas ψ t y
      rw [hf, ih hsub]

/-! ## 3. O resumo e a fronteira -/

/-- [DEF] O RESUMO depois de `j` cláusulas, na célula `u`: a soma dos pesos lidos de todas as atribuições que caem
nessa célula da fronteira. -/
noncomputable def resumo (φ : CNF n) (t : ℝ) (j : ℕ) (u : Fin n → Bool) : ℝ :=
  ∑ x ∈ Finset.univ.filter (fun x => ∀ i ∈ fronteira φ j, x i = u i), pesoDas (φ.take j) t x

/-- ★ **O RESUMO SÓ VÊ A FRONTEIRA**: duas células que concordam na fronteira dão o mesmo resumo. -/
theorem o_resumo_so_ve_a_fronteira (φ : CNF n) (t : ℝ) (j : ℕ) {u v : Fin n → Bool}
    (h : ∀ i ∈ fronteira φ j, u i = v i) : resumo φ t j u = resumo φ t j v := by
  unfold resumo
  apply Finset.sum_congr
  · ext x
    simp only [Finset.mem_filter, Finset.mem_univ, true_and]
    constructor
    · intro hx i hi
      rw [← h i hi]
      exact hx i hi
    · intro hx i hi
      rw [h i hi]
      exact hx i hi
  · intro x _
    rfl

/-- ★ **A FRONTEIRA BASTA AO RESUMO**: o resumo fatora pela leitura da fronteira — existe uma tabela sobre as células
da fronteira que o dá. -/
theorem a_fronteira_basta_ao_resumo (φ : CNF n) (t : ℝ) (j : ℕ) :
    ∃ S : (↥(fronteira φ j) → Bool) → ℝ, ∀ u : Fin n → Bool,
      resumo φ t j u = S fun i => u i := by
  classical
  refine ⟨fun s => resumo φ t j fun i => if h : i ∈ fronteira φ j then s ⟨i, h⟩ else false, fun u => ?_⟩
  apply o_resumo_so_ve_a_fronteira
  intro i hi
  simp only [dif_pos hi]

/-- **A TABELA TEM `2^{|fronteira|}` CÉLULAS, não `2ⁿ`.** -/
theorem a_fronteira_tem_duas_elevado_as_celulas (φ : CNF n) (j : ℕ) :
    Fintype.card (↥(fronteira φ j) → Bool) = 2 ^ (fronteira φ j).card := by
  rw [Fintype.card_fun, Fintype.card_bool, Fintype.card_coe]

/-! ## 4. A leitura pela fronteira é exata -/

/-- O peso da fórmula inteira é o produto do peso da parte lida com o da parte por ler. -/
theorem peso_take_mul_peso_drop (φ : CNF n) (t : ℝ) (j : ℕ) (x : Fin n → Bool) :
    pesoDas φ t x = pesoDas (φ.take j) t x * pesoDas (φ.drop j) t x := by
  unfold pesoDas
  rw [← List.prod_append, ← List.map_append, List.take_append_drop]

/-- A restrição à fronteira. -/
def leituraDaFronteira (φ : CNF n) (j : ℕ) (x : Fin n → Bool) : ↥(fronteira φ j) → Bool :=
  fun i => x i

/-- ★★ **A LEITURA PELA FRONTEIRA É EXATA**: a soma lida inteira é a soma sobre as células da fronteira das somas das
fibras — e em cada fibra o fator lido é o resumo em construção. Perda zero: nada da resposta final se perde. -/
theorem a_leitura_pela_fronteira_e_exata (φ : CNF n) (t : ℝ) (j : ℕ) :
    particao (custoCNF φ) t
      = ∑ v : (↥(fronteira φ j) → Bool),
          ∑ x ∈ Finset.univ.filter (fun x => leituraDaFronteira φ j x = v),
            pesoDas (φ.take j) t x * pesoDas (φ.drop j) t x := by
  rw [particao_e_a_soma_dos_pesos]
  classical
  simp only [peso_take_mul_peso_drop φ t j]
  exact (Finset.sum_fiberwise Finset.univ (leituraDaFronteira φ j)
    fun x => pesoDas (φ.take j) t x * pesoDas (φ.drop j) t x).symm

/-! ## 5. A atualização pela cláusula seguinte -/

/-- A lista das `j+1` primeiras cláusulas é a das `j` primeiras mais a seguinte. -/
theorem take_succ_eq (φ : CNF n) {j : ℕ} (hj : j < φ.length) :
    φ.take (j + 1) = φ.take j ++ [φ.get ⟨j, hj⟩] := by
  rw [List.take_add_one, List.getElem?_eq_getElem hj, Option.toList_some, List.get_eq_getElem]

/-- O peso com `j+1` cláusulas é o peso com `j` vezes o fator da cláusula lida. -/
theorem peso_succ (φ : CNF n) (t : ℝ) {j : ℕ} (hj : j < φ.length) (x : Fin n → Bool) :
    pesoDas (φ.take (j + 1)) t x = pesoDas (φ.take j) t x * fator (φ.get ⟨j, hj⟩) t x := by
  rw [take_succ_eq φ hj]
  unfold pesoDas
  rw [List.map_append, List.prod_append]
  simp

/-- ★ **A ATUALIZAÇÃO PELA CLÁUSULA SEGUINTE**: o resumo novo, na célula `u`, é a soma, sobre a fibra de `u` na
fronteira nova, do peso de cada atribuição nas `j` cláusulas lidas vezes o fator da cláusula seguinte. O integrando é o
peso de cada atribuição, não o resumo anterior; a fibra é a célula da fronteira nova, e é o universo das atribuições
quando essa fronteira é vazia (por exemplo, ao fim da fórmula). -/
theorem a_atualizacao_pela_clausula_seguinte (φ : CNF n) (t : ℝ) {j : ℕ} (hj : j < φ.length)
    (u : Fin n → Bool) :
    resumo φ t (j + 1) u
      = ∑ x ∈ Finset.univ.filter (fun x => ∀ i ∈ fronteira φ (j + 1), x i = u i),
          pesoDas (φ.take j) t x * fator (φ.get ⟨j, hj⟩) t x := by
  unfold resumo
  apply Finset.sum_congr rfl
  intro x _
  exact peso_succ φ t hj x

/-! ## 6. A parede -/

/-- As variáveis da lista de duas ocorrências da mesma cláusula são as variáveis dela. -/
theorem varsDas_pair (C : Clausula n) : varsDas ([C, C] : CNF n) = varsClausula C := by
  unfold varsDas
  rw [List.map_cons, List.map_cons, List.map_nil, List.foldr_cons, List.foldr_cons, List.foldr_nil]
  rw [Finset.union_empty, Finset.union_self]

/-- ★ **A PAREDE DE TODAS AS VARIÁVEIS**: uma fórmula de duas ocorrências de uma cláusula que menciona todas as
variáveis tem, depois da primeira leitura, a fronteira igual ao universo — e a tabela do resumo tem `2ⁿ` células. A
pergunta do Instituto não é tocada: há fórmula cujo resumo é o todo. -/
theorem a_parede_de_todas_as_variaveis (C : Clausula n) (hC : varsClausula C = Finset.univ) :
    fronteira ([C, C] : CNF n) 1 = Finset.univ
    ∧ Fintype.card (↥(fronteira ([C, C] : CNF n) 1) → Bool) = 2 ^ n := by
  have h1 : ([C, C] : CNF n).take 1 = [C] := rfl
  have h2 : ([C, C] : CNF n).drop 1 = [C] := rfl
  have hfr : fronteira ([C, C] : CNF n) 1 = Finset.univ := by
    unfold fronteira
    rw [h1, h2]
    rw [show varsDas ([C] : CNF n) = varsClausula C from by
      unfold varsDas
      rw [List.map_cons, List.map_nil, List.foldr_cons, List.foldr_nil, Finset.union_empty]]
    rw [hC, Finset.inter_self]
  refine ⟨hfr, ?_⟩
  rw [hfr, Fintype.card_fun, Fintype.card_bool, Fintype.card_coe, Finset.card_univ, Fintype.card_fin]

end TGLExt.OResumoEPsiBit
