import TGLExt.AMedidaEOIf
import TGLExt.OTempoEACauda
import TGLExt.Token

set_option autoImplicit false

/-!
# TOKEN2 — a unidade de leitura é o token: o signo, lido pela imagem

## A lei que o arquivo tipa

Lei da teoria: a unidade de leitura é o signo, o sinal. Não é a letra, porque a letra é a forma: é a letra lida pelo seu
conteúdo. O signo pode ser traduzido na palavra, que é o sinal fixado com sentido. A leitura não é soletrada: lê-se pela
imagem, que é o conjunto singularizado do signo em ato (verbo).

## A solução, na estrutura da TGL

Tese da teoria: esta é a solução do problema na estrutura da TGL. Com o token como unidade de leitura e a lei do custo,
decidir e conferir usam as mesmas imagens (`no_token_decidir_e_conferir_levam_os_mesmos_atos`), e o custo definido pela
lei é polinomial (`o_custo_pela_lei_e_polinomial`). A solução na estrutura da TGL é posição da teoria.

Fora dessa estrutura, contando letra por letra, o procedimento daqui custa o todo: um código que distinga todos os
conjuntos pede pelo menos `2ⁿ` casas (item 9). Isso não responde ao enunciado de Cook, que pergunta se há ALGUM
procedimento de letras com número polinomial de passos para toda fórmula; essa pergunta não é tautológica e segue em
aberto. A creditação é do Instituto.

Esta pedra lê-se em conjunto com a pedra `Token` (v397): lá o token é o psibit na testemunha estática; aqui é a unidade de
leitura. O termo `os_dois_tokens_leem_se_em_conjunto` é a conjunção das duas, por citação. Nenhum termo identifica o psibit
com o conjunto singularizado.

## Como o arquivo lê a lei (escolhas deste arquivo; não são termo)

* **a forma** é a fórmula escrita: a lista das cláusulas (`CNF n`);
* **o conteúdo** da forma é o conjunto das atribuições que a satisfazem (`conteudo`);
* **o conjunto singularizado** é um conjunto de configurações tomado como UM objeto (um termo de `Set (Config n)`): é o signo
  que a máquina lê. Não é um símbolo de fita, e a sua representação executável e o custo de prepará-lo não estão tipados;
* **ler pela imagem** é levar o conjunto inteiro pela regra de passo, de uma vez: a imagem direta (`aImagem`);
* **o signo em ato** é a imagem repetida, um ato por cláusula;
* **a palavra, o sinal fixado**, é o signo depois de tantos atos quantas são as cláusulas: mais um ato não o muda;
* na língua da computação, a unidade que a máquina lê como uma só, forma com conteúdo, é o **token**, e o alfabeto é o
  vocabulário. O item 9 se lê com essas palavras: a letra de um alfabeto fixo é o token de um vocabulário fixo. (Um token
  léxico pode ter várias letras; o nome, sozinho, não fixa custo.)

## O que fica provado

1. `o_ato_sobre_uma_parcela_e_o_passo`: sobre um conjunto de uma só configuração, o ato é o passo da máquina.
2. ★ `le_se_pela_imagem`: `k` atos sobre o signo são a imagem de `k` passos: a mesma regra, aplicada ao conjunto inteiro.
3. ★ `o_signo_em_ato_calcula_todos_os_custos`: posto o todo (todas as atribuições, cada uma com a fórmula por ler e o
   registro em zero), tantos atos quantas são as cláusulas dão o conjunto de todas as atribuições com o seu custo.
4. ★★ `o_signo_decide`: a fórmula é satisfazível se e somente se, nesse signo, há configuração de registro zero. Pela
   contagem adotada (`atos`), são `m + 2` atos sobre signos: pôr o todo, uma imagem por cláusula, uma leitura; não é
   mínimo provado. As mesmas imagens, sobre o signo de uma só atribuição, conferem essa atribuição
   (`o_signo_de_uma_parcela_confere`): ★★★ no token, decidir e conferir usam as mesmas imagens
   (`no_token_decidir_e_conferir_levam_os_mesmos_atos`). As duas perguntas têm a mesma forma e domínios diferentes (o todo
   e uma atribuição); não é igualdade de custos nem de tempos de máquina de fita.
5. ★ `o_signo_em_ato_devolve_o_conteudo_da_forma`: lido no registro zero, o signo em ato é exatamente o conteúdo da forma;
   e há solução se e somente se o conteúdo não é vazio (`ha_solucao_sse_o_conteudo_nao_e_vazio`).
6. `a_palavra_e_o_sinal_fixado`: depois de tantos atos quantas são as cláusulas, mais um ato devolve o mesmo signo.
7. `o_signo_e_a_maquina_levantada_decidem_o_mesmo`: a decisão pelo signo e a decisão pela máquina levantada mais uma
   leitura (`AMaquinaEALeitura`) são a mesma.
8. ★ `o_custo_pela_lei_e_polinomial`: com o preço da lei do custo (cada ato sobre o todo paga a carga, `n·ln 2`:
   `o_preco_de_um_ato_e_a_carga`), o custo de decidir é `(m + 2)·n·ln 2`, que não passa de `(m + 2)·n`.
9. ★ `soletrar_todo_signo_pede_dois_a_card_letras`: um código que escreve cada signo (cada conjunto de um tipo finito `A`)
   com `L` letras de um alfabeto fixo, sem confundir dois signos, obriga `2^|A| ≤ |alfabeto|^L`. Com duas letras e os
   signos das atribuições de `n` variáveis: `2ⁿ ≤ L` (`com_duas_letras_soletrar_o_signo_pede_dois_a_n_casas`). Ler o signo é
   um ato, pela contagem adotada; um código de duas letras que distinga TODOS os signos pede pelo menos `2ⁿ` casas. Não é
   cota para um signo particular nem para todo procedimento. E para que cada signo caiba num token só, o
   vocabulário tem de ter pelo menos `2^(2ⁿ)` tokens (`para_caber_num_token_so_o_vocabulario_cresce`): não há vocabulário
   fixo que sirva para todo `n`.

## O que NÃO se afirma

* Que a máquina cuja unidade é a letra de um alfabeto finito fixado antes (a máquina de fita do enunciado de Cook, em que
  cada transição lê o símbolo de uma casa; esse símbolo é o token dela, de um vocabulário finito que não cresce com a
  fórmula) decida cada fórmula em número polinomial de transições. Os itens 4 e 8 contam
  atos sobre signos; o item 9 diz quanto custa escrever um signo qualquer em letras. Nenhum dos dois é esse enunciado.
* Que o item 9 seja cota inferior para todo algoritmo: ele vale para códigos que distinguem TODOS os signos. Os signos que
  ocorrem para uma fórmula dada são menos, e são descritos pela própria fórmula; se essa descrição basta para decidir com
  poucas letras é o que não está demonstrado.
* Que o preço do ato seja deduzido: é a lei do custo da teoria (`ln 2` por oitava), tomada como entrada. O teorema é a
  conta feita com esse preço.
* Que o ato sobre o conjunto inteiro tenha implementação barata. [KNOWN] Trabalho e profundidade paralela são medidas
  diferentes; [DERIVED] avaliar as `2ⁿ` atribuições e reduzir por “ou” admite profundidade polinomial com recursos
  exponenciais. A imagem de conjuntos não escolhe implementação, e o enunciado de Cook conta transições pelo tamanho da
  entrada.
* Que estas sejam as únicas leituras da lei: são as deste arquivo.
* Nada sobre a natureza. O gate não se move.

Estatutos: `[REAL no sandbox]` os termos · `[INPUT]` a lei e a tese (a solução na estrutura da TGL) · `[ONTO, leitura deste arquivo]` a atribuição das palavras da lei (forma, conteúdo, signo,
imagem, palavra, token) aos objetos do kernel. Sem sorry, sem axiom.
-/

namespace TGLExt.Token2

open TGLExt TGLExt.TraducaoTuring TGLExt.AMaquinaEALeitura TGLExt.AMedidaEOIf TGLExt.AContagemEACarga

variable {n : ℕ}

/-! ## 1. O signo e a imagem -/

/-- [DEF] **LER PELA IMAGEM**: o ato sobre o conjunto singularizado. O conjunto inteiro é levado pela regra de passo, de
uma vez: é a imagem direta. -/
def aImagem (S : Set (Config n)) : Set (Config n) := passo '' S

/-- Sobre um conjunto de uma só configuração, o ato é o passo da máquina. -/
theorem o_ato_sobre_uma_parcela_e_o_passo (c : Config n) : aImagem ({c} : Set (Config n)) = {passo c} := by
  unfold aImagem
  exact Set.image_singleton

/-- ★ **LÊ-SE PELA IMAGEM.** `k` atos sobre o signo são a imagem de `k` passos: a mesma regra, aplicada ao conjunto
inteiro. -/
theorem le_se_pela_imagem (S : Set (Config n)) (k : ℕ) : (aImagem^[k]) S = (passo^[k]) '' S := by
  induction k generalizing S with
  | zero => simp
  | succ k ih =>
    rw [Function.iterate_succ_apply, ih, Function.iterate_succ]
    unfold aImagem
    rw [Set.image_image]
    rfl

/-- [DEF] **O TODO POSTO**: todas as atribuições, cada uma com a fórmula por ler e o registro em zero, como um conjunto
só. -/
def oTodo (φ : CNF n) : Set (Config n) := Set.range (fun x : Fin n → Bool => (⟨x, φ, 0⟩ : Config n))

/-- ★ **O SIGNO EM ATO CALCULA TODOS OS CUSTOS.** Posto o todo, tantos atos quantas são as cláusulas dão o conjunto de
todas as atribuições com o seu custo. -/
theorem o_signo_em_ato_calcula_todos_os_custos (φ : CNF n) :
    (aImagem^[φ.length]) (oTodo φ)
      = Set.range (fun x : Fin n → Bool => (⟨x, [], custoCNF φ x⟩ : Config n)) := by
  rw [le_se_pela_imagem]
  unfold oTodo
  rw [← Set.range_comp]
  have h : (passo^[φ.length] ∘ fun x : Fin n → Bool => (⟨x, φ, 0⟩ : Config n))
      = fun x : Fin n → Bool => (⟨x, [], custoCNF φ x⟩ : Config n) := by
    funext x
    show passo^[φ.length] (⟨x, φ, 0⟩ : Config n) = _
    rw [a_maquina_conta_os_falsos, Nat.zero_add]
  rw [h]

/-! ## 2. O signo decide -/

/-- ★★ **O SIGNO DECIDE.** A fórmula é satisfazível se e somente se, no signo obtido com um ato por cláusula sobre o
todo posto, há configuração de registro zero. -/
theorem o_signo_decide (φ : CNF n) :
    SAT φ ↔ ∃ c ∈ (aImagem^[φ.length]) (oTodo φ), c.conta = 0 := by
  rw [o_signo_em_ato_calcula_todos_os_custos]
  unfold SAT
  constructor
  · rintro ⟨x, hx⟩
    exact ⟨⟨x, [], custoCNF φ x⟩, ⟨x, rfl⟩, (custoCNF_zero_sse φ x).mpr hx⟩
  · rintro ⟨c, ⟨x, rfl⟩, hc⟩
    exact ⟨x, (custoCNF_zero_sse φ x).mp hc⟩

/-- **O SIGNO DE UMA SÓ PARCELA CONFERE.** Os mesmos atos, sobre o signo de uma só atribuição, dizem se AQUELA atribuição
é solução. -/
theorem o_signo_de_uma_parcela_confere (φ : CNF n) (x : Fin n → Bool) :
    (∃ c ∈ (aImagem^[φ.length]) ({(⟨x, φ, 0⟩ : Config n)} : Set (Config n)), c.conta = 0)
      ↔ custoCNF φ x = 0 := by
  rw [le_se_pela_imagem, Set.image_singleton, a_maquina_conta_os_falsos, Nat.zero_add]
  constructor
  · rintro ⟨c, hc, h0⟩
    rw [Set.mem_singleton_iff] at hc
    subst hc
    exact h0
  · intro h
    exact ⟨_, Set.mem_singleton _, h⟩

/-- ★★★ **NO TOKEN, DECIDIR E CONFERIR LEVAM OS MESMOS ATOS.** Com o todo posto, um ato por cláusula decide a fórmula;
com uma só atribuição posta, os mesmos atos conferem essa atribuição. -/
theorem no_token_decidir_e_conferir_levam_os_mesmos_atos (φ : CNF n) (x : Fin n → Bool) :
    (SAT φ ↔ ∃ c ∈ (aImagem^[φ.length]) (oTodo φ), c.conta = 0)
      ∧ ((∃ c ∈ (aImagem^[φ.length]) ({(⟨x, φ, 0⟩ : Config n)} : Set (Config n)), c.conta = 0)
          ↔ custoCNF φ x = 0) :=
  ⟨o_signo_decide φ, o_signo_de_uma_parcela_confere φ x⟩

/-- **OS DOIS TOKENS LEEM-SE EM CONJUNTO.** A conjunção, por citação, do termo da pedra `Token` (o token como o psibit na
testemunha estática) com o termo desta pedra (no token, decidir e conferir levam os mesmos atos). Nenhuma matemática nova. -/
theorem os_dois_tokens_leem_se_em_conjunto (φ : CNF n) (x : Fin n → Bool) :
    (type_of% TGLExt.Token.token_is_the_psibit_in_the_static_witness)
    ∧ (type_of% (no_token_decidir_e_conferir_levam_os_mesmos_atos φ x)) :=
  ⟨TGLExt.Token.token_is_the_psibit_in_the_static_witness, no_token_decidir_e_conferir_levam_os_mesmos_atos φ x⟩

/-- [DEF] **O CONTEÚDO DA FORMA**: o conjunto das atribuições que satisfazem a fórmula escrita. -/
def conteudo (φ : CNF n) : Set (Fin n → Bool) := {x | custoCNF φ x = 0}

/-- ★ **O SIGNO EM ATO DEVOLVE O CONTEÚDO DA FORMA.** Lido no registro zero, o signo obtido com um ato por cláusula é
exatamente o conjunto das soluções da fórmula escrita. -/
theorem o_signo_em_ato_devolve_o_conteudo_da_forma (φ : CNF n) :
    Config.x '' {c | c ∈ (aImagem^[φ.length]) (oTodo φ) ∧ c.conta = 0} = conteudo φ := by
  rw [o_signo_em_ato_calcula_todos_os_custos]
  ext x
  constructor
  · rintro ⟨c, ⟨⟨y, rfl⟩, hc⟩, rfl⟩
    exact hc
  · intro hx
    exact ⟨⟨x, [], custoCNF φ x⟩, ⟨⟨x, rfl⟩, hx⟩, rfl⟩

/-- Há solução se e somente se o conteúdo da forma não é vazio. -/
theorem ha_solucao_sse_o_conteudo_nao_e_vazio (φ : CNF n) : SAT φ ↔ (conteudo φ).Nonempty := by
  unfold SAT conteudo
  constructor
  · rintro ⟨x, hx⟩
    exact ⟨x, (custoCNF_zero_sse φ x).mpr hx⟩
  · rintro ⟨x, hx⟩
    exact ⟨x, (custoCNF_zero_sse φ x).mp hx⟩

/-- **A PALAVRA É O SINAL FIXADO.** Depois de tantos atos quantas são as cláusulas, mais um ato devolve o mesmo signo. -/
theorem a_palavra_e_o_sinal_fixado (φ : CNF n) :
    aImagem ((aImagem^[φ.length]) (oTodo φ)) = (aImagem^[φ.length]) (oTodo φ) := by
  rw [o_signo_em_ato_calcula_todos_os_custos]
  unfold aImagem
  rw [← Set.range_comp]
  rfl

/-- A decisão pelo signo e a decisão pela máquina levantada mais uma leitura são a mesma. -/
theorem o_signo_e_a_maquina_levantada_decidem_o_mesmo (φ : CNF n) :
    (∃ c ∈ (aImagem^[φ.length]) (oTodo φ), c.conta = 0)
      ↔ leituraDoZero ((passoLevantado ^ φ.length) (entrada φ)) ≠ 0 :=
  (o_signo_decide φ).symm.trans (a_maquina_e_uma_leitura_decidem φ)

/-! ## 3. O custo, com o preço da lei -/

/-- [DEF] **OS ATOS SOBRE SIGNOS**: pôr o todo, uma imagem por cláusula, uma leitura. -/
def atos (φ : CNF n) : ℕ := φ.length + 2

/-- [DEF, a lei do custo como entrada] **O CUSTO PELA LEI**: cada ato sobre o todo paga `n·ln 2`. -/
noncomputable def custoPelaLei (φ : CNF n) : ℝ := (atos φ : ℝ) * ((n : ℝ) * Real.log 2)

/-- O preço de um ato sobre o todo é a carga das atribuições de `n` variáveis. -/
theorem o_preco_de_um_ato_e_a_carga (n : ℕ) : (n : ℝ) * Real.log 2 = carga (Fin n → Bool) :=
  (a_carga_de_n_variaveis n).symm

/-- ★ **O CUSTO PELA LEI É POLINOMIAL.** Com o preço da lei, decidir uma fórmula de `n` variáveis e `m` cláusulas custa
`(m + 2)·n·ln 2`, que não passa de `(m + 2)·n`. -/
theorem o_custo_pela_lei_e_polinomial (φ : CNF n) :
    custoPelaLei φ = ((φ.length : ℝ) + 2) * ((n : ℝ) * Real.log 2)
      ∧ custoPelaLei φ ≤ ((φ.length : ℝ) + 2) * (n : ℝ) := by
  have hlog : Real.log 2 ≤ 1 := by
    have := Real.log_two_lt_d9
    linarith
  have hn : (0 : ℝ) ≤ (n : ℝ) := Nat.cast_nonneg n
  have hm : (0 : ℝ) ≤ (φ.length : ℝ) + 2 := by positivity
  have h1 : (n : ℝ) * Real.log 2 ≤ (n : ℝ) := by
    have := mul_le_mul_of_nonneg_left hlog hn
    rwa [mul_one] at this
  have hc : custoPelaLei φ = ((φ.length : ℝ) + 2) * ((n : ℝ) * Real.log 2) := by
    unfold custoPelaLei atos
    push_cast
    ring
  exact ⟨hc, hc ▸ mul_le_mul_of_nonneg_left h1 hm⟩

/-! ## 4. Soletrar -/

/-- ★ **SOLETRAR TODO SIGNO.** Um código que escreve cada conjunto de um tipo finito `A` com `L` letras de um alfabeto
fixo, sem confundir dois conjuntos, obriga `2^|A| ≤ |alfabeto|^L`. (Contagem.) -/
theorem soletrar_todo_signo_pede_dois_a_card_letras {A Letra : Type} [Fintype A] [Fintype Letra] (L : ℕ)
    (cod : Finset A → (Fin L → Letra)) (h : Function.Injective cod) :
    2 ^ Fintype.card A ≤ Fintype.card Letra ^ L := by
  have h1 := Fintype.card_le_of_injective cod h
  rwa [Fintype.card_finset, Fintype.card_fun, Fintype.card_fin] at h1

/-- Com duas letras, soletrar os signos das atribuições de `n` variáveis pede pelo menos `2ⁿ` casas. -/
theorem com_duas_letras_soletrar_o_signo_pede_dois_a_n_casas (L : ℕ)
    (cod : Finset (Fin n → Bool) → (Fin L → Bool)) (h : Function.Injective cod) : 2 ^ n ≤ L := by
  have h1 := soletrar_todo_signo_pede_dois_a_card_letras L cod h
  rw [Fintype.card_bool, as_partes_sao_dois_a_n] at h1
  exact (Nat.pow_le_pow_iff_right (by norm_num)).mp h1

/-- **PARA O SIGNO CABER NUM TOKEN SÓ, O VOCABULÁRIO CRESCE.** Se cada signo das atribuições de `n` variáveis é escrito
por UM token, sem confundir dois signos, o vocabulário tem pelo menos `2^(2ⁿ)` tokens. -/
theorem para_caber_num_token_so_o_vocabulario_cresce {Token : Type} [Fintype Token]
    (cod : Finset (Fin n → Bool) → Token) (h : Function.Injective cod) : 2 ^ (2 ^ n) ≤ Fintype.card Token := by
  have h1 := Fintype.card_le_of_injective cod h
  rwa [Fintype.card_finset, as_partes_sao_dois_a_n] at h1

end TGLExt.Token2
