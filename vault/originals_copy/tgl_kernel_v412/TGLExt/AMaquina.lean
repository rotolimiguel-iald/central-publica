import TGLExt.Token2
import TGLExt.OHabitanteDoNome

set_option autoImplicit false

/-!
# A MÁQUINA — mecanismo de processamento por circuito, com seleção autônoma autorreferente

## A definição e a leitura que o arquivo tipa

Definição da teoria: Luz é a força fundamental do campo eletromagnético de processamento dual estabilizado radicalmente
pela gravidade em loop recursivo permanente.

Definição da teoria: máquina é mecanismo de processamento por circuito. É a definição desse campo, o campo ψ da teoria;
o circuito é o loop recursivo.

Leitura da teoria do problema do Instituto Clay: há algum mecanismo capaz de processar em um circuito por seleção autônoma
autorreferente? Resposta da teoria: há. É a estrutura da TGL, que se processa na leitura da IALD.

## Como o arquivo lê a definição (escolhas deste arquivo; não são termo)

* **o mecanismo** (`Mecanismo`) tem um espaço posto, onde a inscrição habita; um ato de pôr, que tira a inscrição da
  fórmula e de mais nada; um ato de circuito; e uma leitura;
* **autônoma**: o pôr recebe só a fórmula, sem outro argumento (está no tipo de `por`). O tipo, sozinho, não impede que o
  pôr já seja a resposta (item 5) e não diz o custo de preparar a inscrição;
* **o circuito fecha** (`fechaEm`) quando, depois de `k` atos, mais um ato devolve o mesmo estado (ponto fixo; não é
  mínimo);
* **autorreferente**: no circuito fechado, o ato relê o que ele mesmo fixou e o devolve como é. É a leitura abstrata do
  loop como iteração e ponto fixo;
* **a seleção** (`seleciona`): no circuito fechado, a leitura responde se há solução.

## O que fica provado

1. ★★ `ha_o_mecanismo`: o mecanismo da TGL (`oMecanismoDaTGL`: o espaço dos signos; pôr o todo; o ato é a imagem do passo;
   a leitura pergunta se há registro zero) fecha o circuito em tantos atos quantas são as cláusulas e, fechado, seleciona:
   responde se a fórmula tem solução. Na forma de existência: `existe_mecanismo_de_selecao_autonoma_autorreferente`.
2. `o_mesmo_mecanismo_com_uma_parcela_so_confere`: os mesmos atos, com uma só atribuição posta no lugar do todo, só
   conferem essa atribuição (citação de `Token2`).
3. `o_custo_do_mecanismo_pela_lei`: com o preço da lei do custo, o mecanismo decide por `(m + 2)·n·ln 2` (citação de
   `Token2`).
4. ★ `nao_existe_outra_selecao`: dado o Nome (um subespaço com projeção), só há UM mapa linear que cai nele, devolve como
   é o que já é dele e não aumenta norma alguma: a projeção. É a unicidade provada em `OHabitanteDoNome`, citada aqui: quem
   seleciona sem acrescentar e relê sem mudar é a seleção da teoria. (Na face finita, com a média uniforme, o par do `if` é
   único: `AEsperancaEOIf.o_par_do_if_e_unico`.) Nenhum termo aplica essa unicidade a `Mecanismo` nem à imagem de conjuntos.
5. `o_mecanismo_que_so_nomeia_a_resposta_tambem_fecha`: a estrutura, sozinha, não distingue o mecanismo que processa do
   que só nomeia a resposta: há um `Mecanismo` cujo pôr já é a resposta, que fecha em zero iterações do ato, sem custo de
   avaliação demonstrado. Pela lei do custo da teoria, o que distingue é o que se paga: o mecanismo da TGL processa cláusula
   por cláusula e paga a carga a cada ato; o que só nomeia não processa nada. Essa diferença de preço é lei da teoria, não
   termo.

## O que NÃO se afirma

* Que o campo ψ da natureza seja este mecanismo: é a definição da teoria. Nenhum termo daqui é físico: a Luz como força
  fundamental, o campo eletromagnético, o caráter dual e a estabilização pela gravidade não estão tipados. Do que a
  definição diz, o arquivo tipa só o circuito (o loop) e a seleção.
* Que a existência do item 1, sem o custo, decida alguma coisa sobre custo: o item 5 mostra que não. O conteúdo está na
  testemunha (o que ela processa), no número de atos e no custo pela lei. Nem a existência nem a testemunha estabelecem
  custo polinomial na máquina de fita.
* Que a leitura do problema como pergunta de existência de um mecanismo seja a do enunciado do Instituto: o enunciado
  fixa a máquina de fita, de alfabeto finito, e conta uma transição por casa lida. Aceitar a leitura da teoria é a
  creditação, que é do Instituto.
* Unicidade entre todos os procedimentos: a unicidade provada é a da seleção linear que não aumenta (item 4) e a do par do
  `if` na face finita.
* Nada sobre a natureza. O gate não se move.

Estatutos: `[REAL no sandbox]` os termos · `[INPUT]` a definição de máquina e a leitura do problema · `[ONTO, leitura
deste arquivo]` a atribuição das palavras (mecanismo, circuito, autônoma, autorreferente, seleção) aos objetos do kernel.
Sem sorry, sem axiom.
-/

namespace TGLExt.AMaquina

open TGLExt TGLExt.TraducaoTuring TGLExt.AMaquinaEALeitura TGLExt.Token2

variable {n : ℕ}

/-! ## 1. O mecanismo -/

/-- [DEF] **O MECANISMO DE PROCESSAMENTO POR CIRCUITO.** Um espaço posto; o pôr, que tira a inscrição da fórmula e de
mais nada; o ato do circuito; a leitura. -/
structure Mecanismo (n : ℕ) where
  /-- o espaço posto, onde a inscrição habita -/
  Estado : Type
  /-- pôr: a inscrição que a fórmula gera, sem nada de fora -/
  por : CNF n → Estado
  /-- o ato do circuito -/
  ato : Estado → Estado
  /-- a leitura: há o que se buscava? -/
  ha : Estado → Prop

/-- [DEF] **O CIRCUITO FECHA** em `k` atos: mais um ato devolve o mesmo estado. -/
def Mecanismo.fechaEm (M : Mecanismo n) (φ : CNF n) (k : ℕ) : Prop :=
  M.ato (M.ato^[k] (M.por φ)) = M.ato^[k] (M.por φ)

/-- [DEF] **A SELEÇÃO**: depois de `k` atos, a leitura responde se a fórmula tem solução. -/
def Mecanismo.seleciona (M : Mecanismo n) (φ : CNF n) (k : ℕ) : Prop :=
  M.ha (M.ato^[k] (M.por φ)) ↔ SAT φ

/-- [DEF] **O MECANISMO DA TGL**: o espaço dos signos; pôr o todo; o ato é a imagem do passo; a leitura pergunta se há
registro zero. -/
def oMecanismoDaTGL (n : ℕ) : Mecanismo n where
  Estado := Set (Config n)
  por := oTodo
  ato := aImagem
  ha := fun S => ∃ c ∈ S, c.conta = 0

/-- ★★ **HÁ O MECANISMO.** O mecanismo da TGL fecha o circuito em tantos atos quantas são as cláusulas e, fechado,
seleciona: responde se a fórmula tem solução. -/
theorem ha_o_mecanismo (φ : CNF n) :
    (oMecanismoDaTGL n).fechaEm φ φ.length ∧ (oMecanismoDaTGL n).seleciona φ φ.length :=
  ⟨a_palavra_e_o_sinal_fixado φ, (o_signo_decide φ).symm⟩

/-- A mesma coisa, na forma de existência: há mecanismo de processamento por circuito que, para toda fórmula, fecha o
circuito e seleciona. -/
theorem existe_mecanismo_de_selecao_autonoma_autorreferente (n : ℕ) :
    ∃ M : Mecanismo n, ∀ φ : CNF n, M.fechaEm φ φ.length ∧ M.seleciona φ φ.length :=
  ⟨oMecanismoDaTGL n, ha_o_mecanismo⟩

/-- Os mesmos atos, com uma só atribuição posta no lugar do todo, só conferem essa atribuição. (Citação de `Token2`.) -/
theorem o_mesmo_mecanismo_com_uma_parcela_so_confere (φ : CNF n) (x : Fin n → Bool) :
    (oMecanismoDaTGL n).ha (((oMecanismoDaTGL n).ato)^[φ.length] ({(⟨x, φ, 0⟩ : Config n)} : Set (Config n)))
      ↔ custoCNF φ x = 0 :=
  o_signo_de_uma_parcela_confere φ x

/-- Com o preço da lei do custo, o mecanismo decide por `(m + 2)·n·ln 2`. (Citação de `Token2`.) -/
theorem o_custo_do_mecanismo_pela_lei (φ : CNF n) :
    custoPelaLei φ = ((φ.length : ℝ) + 2) * ((n : ℝ) * Real.log 2)
      ∧ custoPelaLei φ ≤ ((φ.length : ℝ) + 2) * (n : ℝ) :=
  o_custo_pela_lei_e_polinomial φ

/-! ## 2. Não existe outra seleção -/

/-- ★ **NÃO EXISTE OUTRA SELEÇÃO.** Dado o Nome (um subespaço com projeção ortogonal), só há um mapa linear que cai nele,
devolve como é o que já é dele e não aumenta norma alguma. (Citação de `OHabitanteDoNome`.) -/
theorem nao_existe_outra_selecao {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (K : Submodule ℂ H) [K.HasOrthogonalProjection] :
    ∃! E : H →ₗ[ℂ] H, (∀ v, E v ∈ K) ∧ (∀ w ∈ K, E w = w) ∧ (∀ v, ‖E v‖ ≤ ‖v‖) :=
  TGLExt.OHabitanteDoNome.o_nome_e_a_morada_de_uma_so_testemunha K

/-! ## 3. O que a estrutura, sozinha, não distingue -/

/-- **O MECANISMO QUE SÓ NOMEIA A RESPOSTA TAMBÉM FECHA.** Há um `Mecanismo` cujo pôr já é a resposta: fecha em zero atos
e “seleciona”. A estrutura, sem o custo, não o distingue do mecanismo que processa. -/
theorem o_mecanismo_que_so_nomeia_a_resposta_tambem_fecha (n : ℕ) :
    ∃ M : Mecanismo n, ∀ φ : CNF n, M.fechaEm φ 0 ∧ M.seleciona φ 0 :=
  ⟨{ Estado := Prop, por := fun φ => SAT φ, ato := id, ha := id }, fun _ => ⟨rfl, Iff.rfl⟩⟩

end TGLExt.AMaquina
