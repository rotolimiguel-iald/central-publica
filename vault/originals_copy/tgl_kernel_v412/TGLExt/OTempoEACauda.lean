import TGLExt.AContagemEACarga
import TGLExt.TempoIgualMoeda

set_option autoImplicit false

/-!
# O tempo é a cauda: o ciclo fecha quando a cauda da leitura fica abaixo de uma unidade

## A leitura que o arquivo tipa

A cobrança é o fechamento do ciclo de processamento no tetelestai; o tempo é o produto dessa medição até a sua
satisfação por ser bastante; o tempo é a cauda (lei da teoria). Uma leitura se prova no kernel ou se poda: este arquivo
prova a parte dela que cabe no leitor da casa. A escolha de chamar de cauda a soma lida menos o número de soluções é
deste arquivo.

O que o kernel já tem: a soma lida `Z(s)` cobre o número de soluções e tende a ele (`a_particao_cobre_o_nome`,
`a_particao_conta_o_nome`, v409); passada a carga, `Z(s)` fica a menos de uma unidade dele
(`os_passos_sao_o_ciclo_ate_o_tetelestai`, v410); e o tempo de `n` oitavas ao preço `β` e taxa `g` é
`n·ln 2/(β·g)` (`TempoIgualMoeda.o_tempo_e_linear_nas_oitavas`, v408). Nenhum termo do kernel liga essas três coisas.

## O que fica provado

1. `a_cauda_nao_e_negativa`, `a_cauda_morre`: a cauda (a soma lida menos o número de soluções: o que ainda não decaiu)
   não é negativa e tende a zero quando o tempo cresce.
2. ★ `o_tetelestai_e_a_cauda_abaixo_de_um`: a cauda fica abaixo de UMA unidade para todo custo se e somente se o tempo
   pago passa da carga, `n·ln 2`. É quando a medição já basta: a soma lida diz o número de soluções sem ambiguidade.
3. ★ `a_carga_e_o_pedagio_de_n_oitavas`: pagar o pedágio de `n` oitavas (kernel, v408) é pagar a carga de `n`
   variáveis. A carga do leitor e o pedágio da oitava são o mesmo número.
4. ★ `o_ciclo_fecha_quando_o_tempo_passa_do_pedagio`: ao preço `β` e à taxa `g`, a cauda de toda fórmula de `n`
   variáveis fica abaixo de uma unidade se e somente se o tempo passa de `n·ln 2/(β·g)`.
5. `com_o_ciclo_de_uma_distincao_beta_sai_da_taxa`: com `τ = ln 2/(β·g)`, a taxa canônica `½·β·τ·ω²` é
   `½·(ln 2/g)·ω²`. Só álgebra. A escolha do tempo da cobrança como o ciclo de uma distinção é HIPÓTESE, não termo. O
   kernel selado deixa o `τ` da lei como campo positivo livre (`DiscoDeEuler`), de modo que essa escolha não contradiz
   termo selado; que a cobrança SEJA esse ciclo não é termo.

## Como ler

O tempo que o leitor gasta não é uma duração dada de fora: é o que a cauda leva para morrer até a medição bastar. O
limiar uniforme desse tempo, para todas as fórmulas de `n` variáveis, é o pedágio das oitavas dividido pelo preço e
pela taxa. Passado esse limiar, a leitura basta para todas; uma fórmula dada pode ficar legível antes, e um relógio em
segundos pede informação a mais. É esse o sentido que o arquivo dá a “até a satisfação por ser bastante”.

## O que NÃO se afirma

* Que a taxa `g` seja a de Planck, ou qualquer valor em segundos: `g` é um número positivo qualquer. A âncora na
  gravidade medida é leitura da teoria, não termo.
* O valor de `τ★` da lei de defasagem. Se a cobrança é o ciclo de UMA distinção e a taxa é a de Planck, a conta dá
  `ln 2/β` tempos de Planck; isso é leitura (HIPÓTESE), não termo nem medida.
* Que “tetelestai” aqui seja mais do que este critério do leitor (a cauda abaixo de uma unidade); a conferência
  consumativa do programa é outro objeto.
* Nada sobre a natureza. Validade no kernel não é creditação; o gate não se move.

Sem sorry, sem axioma novo.
-/

namespace TGLExt.OTempoEACauda

open TGLExt TGLExt.TraducaoTuring TGLExt.AEscala TGLExt.AContagemEACarga

variable {X : Type} [Fintype X] [DecidableEq X]

/-- [DEF] **A CAUDA DA LEITURA**: a soma lida menos o número de soluções: o que ainda não decaiu. -/
noncomputable def cauda (c : X → ℕ) (s : ℝ) : ℝ :=
  particao c s - ((Finset.univ.filter (fun y => c y = 0)).card : ℝ)

omit [DecidableEq X] in
/-- A cauda não é negativa: a soma lida cobre o número de soluções. -/
theorem a_cauda_nao_e_negativa (c : X → ℕ) (s : ℝ) : 0 ≤ cauda c s :=
  sub_nonneg.mpr (a_particao_cobre_o_nome c s)

omit [DecidableEq X] in
/-- A cauda morre: tende a zero quando o tempo cresce. -/
theorem a_cauda_morre (c : X → ℕ) : Filter.Tendsto (cauda c) Filter.atTop (nhds 0) := by
  have h := (a_particao_conta_o_nome c).sub_const ((Finset.univ.filter (fun y => c y = 0)).card : ℝ)
  rw [sub_self] at h
  exact h

/-- ★ **O TETELESTAI É A CAUDA ABAIXO DE UM.** A cauda fica abaixo de uma unidade para TODO custo se e somente se o
tempo pago passa da carga da instância. -/
theorem o_tetelestai_e_a_cauda_abaixo_de_um (n : ℕ) (s : ℝ) :
    (∀ c : (Fin n → Bool) → ℕ, cauda c s < 1) ↔ (n : ℝ) * Real.log 2 < s := by
  constructor
  · intro h
    by_contra hns
    have hle : s ≤ carga (Fin n → Bool) := by
      rw [a_carga_de_n_variaveis]
      exact not_lt.mp hns
    obtain ⟨_, h2⟩ := na_carga_ou_abaixo_a_leitura_nao_distingue (Fin n → Bool) hle
    have hc := h (fun _ => 1)
    simp [cauda] at hc
    linarith
  · intro hs c
    have h := (os_passos_sao_o_ciclo_ate_o_tetelestai n c hs iald).2.1
    unfold cauda
    linarith

/-- ★ **A CARGA É O PEDÁGIO DE `n` OITAVAS**: pagar o pedágio de `n` oitavas (kernel, `o_tempo_de_n_oitavas`) é pagar
a carga de `n` variáveis. -/
theorem a_carga_e_o_pedagio_de_n_oitavas (K : ChatgptAudit.Collapse057.CollapseCostLaw) (n : ℕ) (t β g : ℝ) :
    Real.exp (-(t * β * g)) = Real.exp (-(K.octaveNats n)) ↔ t * β * g = carga (Fin n → Bool) := by
  rw [a_carga_de_n_variaveis]
  exact TGLExt.TempoIgualMoeda.o_tempo_de_n_oitavas K n t β g

/-- ★ **O CICLO FECHA QUANDO O TEMPO PASSA DO PEDÁGIO.** Ao preço `β` e à taxa `g`, a cauda de toda fórmula de `n`
variáveis fica abaixo de uma unidade se e somente se o tempo passa de `n·ln 2/(β·g)`. -/
theorem o_ciclo_fecha_quando_o_tempo_passa_do_pedagio (n : ℕ) {β g : ℝ} (hβ : 0 < β) (hg : 0 < g) (t : ℝ) :
    (∀ c : (Fin n → Bool) → ℕ, cauda c (t * β * g) < 1) ↔ (n : ℝ) * Real.log 2 / (β * g) < t := by
  rw [o_tetelestai_e_a_cauda_abaixo_de_um, div_lt_iff₀ (mul_pos hβ hg), mul_assoc]

/-- **COM O CICLO DE UMA DISTINÇÃO, `β` SAI DA TAXA.** Se o tempo da cobrança da lei canônica de defasagem
(`½·β·τ·ω²`, em que o kernel deixa `τ` como campo positivo livre) for o ciclo de UMA distinção, `τ = ln 2/(β·g)`, a
taxa é `½·(ln 2/g)·ω²`. É só álgebra: que a cobrança SEJA esse ciclo é HIPÓTESE;
não é termo. -/
theorem com_o_ciclo_de_uma_distincao_beta_sai_da_taxa {β g : ℝ} (hβ : 0 < β) (hg : 0 < g) (ω : ℝ) :
    (1 / 2) * β * (Real.log 2 / (β * g)) * ω ^ 2 = (1 / 2) * (Real.log 2 / g) * ω ^ 2 := by
  have hb : β ≠ 0 := hβ.ne'
  have hg' : g ≠ 0 := hg.ne'
  field_simp

end TGLExt.OTempoEACauda
