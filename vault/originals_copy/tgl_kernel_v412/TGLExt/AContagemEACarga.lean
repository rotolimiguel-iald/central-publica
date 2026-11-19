import TGLExt.AEscala

set_option autoImplicit false

/-!
# A carga da instância é a fronteira estrita da leitura: o critério de uma leitura vale quando, e só quando, o tempo pago passa da carga

## A identificação que o arquivo prova em parte

A contagem da leitura em passos de uma máquina clássica é a sua própria carga, a própria isometria; matemática, lógica e
física medem o mesmo porque são isotrópicas. Uma identificação se prova no kernel ou se poda: este arquivo prova a parte
dela que é da LEITURA. A passagem para a carga logarítmica e para o se-e-somente-se abaixo é a realização escolhida neste
arquivo.

O ponto de partida (`TGLExt.AEscala`): `os_passos_sao_o_ciclo_ate_o_tetelestai` dá, para tempo pago
`s > n·ln 2`, que uma leitura da soma `Z(s) = Σ e^{−s·c(x)}` separa o sim do não; a docstring dele diz, como conta à
mão e não como termo, que no limiar exato a leitura não separa. Este arquivo dá o nome carga e a recíproca.

## O que fica provado

1. `a_carga_de_n_variaveis`: a carga de `n` variáveis de sim ou não (o logaritmo do número de configurações, em nats)
   é `n·ln 2`: `ln 2` por variável.
2. ★ `na_carga_ou_abaixo_a_leitura_nao_distingue`: com tempo pago até a carga, o custo que vale 1 em toda configuração
   (não tem solução) já dá soma lida pelo menos 1: o critério de uma leitura falha.
3. ★ `a_contagem_e_a_carga`: o critério de uma leitura (há configuração de custo zero se e somente se `1 ≤ Z(s)`) vale
   para TODO custo se e somente se o tempo pago PASSA da carga. A carga é a fronteira estrita desse critério uniforme:
   é o ínfimo dos tempos que bastam para todo custo, e não é atingida (na carga exata o critério falha; não existe
   menor tempo suficiente). Depende só de quantas configurações há. Para uma fórmula específica o critério pode valer
   antes.
4. ★ `a_contagem_e_a_carga_para_formulas`: o mesmo para fórmulas: uma leitura decide SAT para toda fórmula de `n`
   variáveis se e somente se o tempo pago passa de `n·ln 2`. A fórmula que engana abaixo da carga é a de uma cláusula
   vazia.
5. `o_limiar_da_leitura_normalizada_e_e_a_menos_carga`: a identidade `1/|X| = e^{−carga}`. Na leitura normalizada (a
   média, `Z/|X|`; a separação vem do termo de `AEscala`) o limiar que separa o sim do não é esse número: a carga
   aparece duas vezes, como o tempo que se paga e como o limiar da média, `1/|X|`. Limiar não é tolerância a erro: com
   tempo `carga + δ`, a instância sem solução dá média no máximo `e^{−δ}/|X|` e a que tem solução dá pelo menos
   `1/|X|`, de modo que a separação garantida é `(1 − e^{−δ})/|X|`; com `δ = ln 2` é `1/(2|X|)`, que pede da ordem de
   `n` casas binárias depois da vírgula [conta aproximada; não é termo]. Avaliar a soma com essa precisão e representar o tempo são custos
   distintos, e este arquivo não trata de nenhum dos dois.

## O que NÃO se afirma

* Nada sobre a máquina de Turing do Mathlib (`Turing.TM2ComputableInPolyTime`): este arquivo não tem termo que ligue o
  tempo pago da leitura aos movimentos de uma cabeça sobre uma fita. Que os dois sejam a mesma contagem é a tradução
  do dicionário (v409) e é lei da teoria, não termo deste arquivo; não é igualdade tipada aqui.
* Quanto custa, a quem não lê de uma vez, obter um número com a finura `e^{−carga}` (item 5). O arquivo diz onde essa
  finura mora; não diz quem a paga.
* Nada sobre a natureza. Validade no kernel não é creditação; o gate não se move.

Sem sorry, sem axioma novo.
-/

namespace TGLExt.AContagemEACarga

open TGLExt TGLExt.TraducaoTuring TGLExt.AEscala

/-- [DEF] **A CARGA DA INSTÂNCIA**: o logaritmo do número de configurações, em nats. -/
noncomputable def carga (X : Type) [Fintype X] : ℝ := Real.log (Fintype.card X)

/-- **A CARGA DE `n` VARIÁVEIS DE SIM OU NÃO É `n·ln 2`**: `ln 2` por variável. -/
theorem a_carga_de_n_variaveis (n : ℕ) : carga (Fin n → Bool) = (n : ℝ) * Real.log 2 := by
  unfold carga
  rw [Fintype.card_fun, Fintype.card_bool, Fintype.card_fin]
  push_cast
  rw [Real.log_pow]

/-- **O LIMIAR DA LEITURA NORMALIZADA É `e^{−carga}`**: o inverso do número de configurações. -/
theorem o_limiar_da_leitura_normalizada_e_e_a_menos_carga (X : Type) [Fintype X] [Nonempty X] :
    ((Fintype.card X : ℝ))⁻¹ = Real.exp (-carga X) := by
  have hc : (0 : ℝ) < Fintype.card X := by exact_mod_cast Fintype.card_pos
  unfold carga
  rw [Real.exp_neg, Real.exp_log hc]

/-- A soma lida do custo que vale 1 em toda configuração: `|X|·e^{−s}`. -/
theorem a_particao_do_custo_um (X : Type) [Fintype X] (s : ℝ) :
    particao (fun _ : X => (1 : ℕ)) s = (Fintype.card X : ℝ) * Real.exp (-s) := by
  unfold particao
  simp

/-- ★ **NA CARGA OU ABAIXO DELA, UMA LEITURA NÃO DISTINGUE**: o custo que vale 1 em toda configuração não tem solução,
e a soma lida não fica abaixo de 1. -/
theorem na_carga_ou_abaixo_a_leitura_nao_distingue (X : Type) [Fintype X] [Nonempty X] {s : ℝ}
    (hs : s ≤ carga X) :
    (¬ ∃ x : X, (fun _ : X => (1 : ℕ)) x = 0) ∧ 1 ≤ particao (fun _ : X => (1 : ℕ)) s := by
  refine ⟨fun ⟨_, h⟩ => one_ne_zero h, ?_⟩
  rw [a_particao_do_custo_um]
  have hc : (0 : ℝ) < Fintype.card X := by exact_mod_cast Fintype.card_pos
  have h1 : Real.exp (-carga X) ≤ Real.exp (-s) := Real.exp_le_exp.mpr (by linarith)
  rw [← o_limiar_da_leitura_normalizada_e_e_a_menos_carga] at h1
  calc (1 : ℝ) = (Fintype.card X : ℝ) * ((Fintype.card X : ℝ))⁻¹ := (mul_inv_cancel₀ hc.ne').symm
    _ ≤ (Fintype.card X : ℝ) * Real.exp (-s) := mul_le_mul_of_nonneg_left h1 hc.le

/-- ★ **A CARGA É A FRONTEIRA ESTRITA DA LEITURA.** O critério de uma leitura (há configuração de custo zero se e
somente se a soma lida é pelo menos 1) vale para TODO custo exatamente quando o tempo pago passa da carga da instância.
Na carga exata não vale. -/
theorem a_contagem_e_a_carga (n : ℕ) (s : ℝ) :
    (∀ c : (Fin n → Bool) → ℕ, ((∃ x, c x = 0) ↔ 1 ≤ particao c s)) ↔ carga (Fin n → Bool) < s := by
  constructor
  · intro h
    by_contra hns
    have hle : s ≤ carga (Fin n → Bool) := not_lt.mp hns
    obtain ⟨h1, h2⟩ := na_carga_ou_abaixo_a_leitura_nao_distingue (Fin n → Bool) hle
    exact h1 ((h (fun _ => 1)).mpr h2)
  · intro hs c
    rw [a_carga_de_n_variaveis] at hs
    exact (os_passos_sao_o_ciclo_ate_o_tetelestai n c hs iald).2.2.1

/-- O custo da fórmula de uma cláusula vazia vale 1 em toda atribuição. -/
theorem o_custo_da_clausula_vazia (n : ℕ) : custoCNF ([[]] : CNF n) = fun _ => 1 := by
  funext x
  simp [custoCNF, satisfeita]

/-- Uma fórmula é satisfazível se e somente se alguma atribuição tem custo zero. -/
theorem sat_e_existir_custo_zero {n : ℕ} (φ : CNF n) : SAT φ ↔ ∃ x, custoCNF φ x = 0 := by
  unfold SAT
  constructor
  · rintro ⟨x, hx⟩
    exact ⟨x, (custoCNF_zero_sse φ x).mpr hx⟩
  · rintro ⟨x, hx⟩
    exact ⟨x, (custoCNF_zero_sse φ x).mp hx⟩

/-- ★ **A CARGA É A FRONTEIRA ESTRITA, PARA FÓRMULAS**: uma leitura decide SAT para toda fórmula de `n` variáveis se e
somente se o tempo pago passa de `n·ln 2`. -/
theorem a_contagem_e_a_carga_para_formulas (n : ℕ) (s : ℝ) :
    (∀ φ : CNF n, (SAT φ ↔ 1 ≤ particao (custoCNF φ) s)) ↔ (n : ℝ) * Real.log 2 < s := by
  rw [← a_carga_de_n_variaveis]
  constructor
  · intro h
    by_contra hns
    have hle : s ≤ carga (Fin n → Bool) := not_lt.mp hns
    obtain ⟨h1, h2⟩ := na_carga_ou_abaixo_a_leitura_nao_distingue (Fin n → Bool) hle
    have h3 := (h [[]]).mpr (by rw [o_custo_da_clausula_vazia]; exact h2)
    rw [sat_e_existir_custo_zero, o_custo_da_clausula_vazia] at h3
    exact h1 h3
  · intro hs φ
    rw [sat_e_existir_custo_zero]
    exact ((a_contagem_e_a_carga n s).mpr hs) (custoCNF φ)

end TGLExt.AContagemEACarga
