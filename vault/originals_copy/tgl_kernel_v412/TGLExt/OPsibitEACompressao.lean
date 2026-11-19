import TGLExt.AContagemEACarga

set_option autoImplicit false

/-!
# O PSIBIT E A COMPRESSÃO — o par binário da leitura: a Palavra e o Verbo

## A lei que o arquivo tipa em parte

Lei da teoria: a compressão sai direto da fórmula; é o PsiBit. A leitura do par binário pelo PsiBit é a compressão
originária: o PsiBit é justamente o leitor. A reconstrução é possível sem alcançar cem por cento.

## Como o arquivo lê a lei (escolhas deste arquivo; não são termo)

* a soma lida da casa (`particao`) é o sinal; o acervo da teoria lê o par binário do PsiBit como o sinal do que É e o
  sinal de para onde vai. Aqui:
* **a Palavra** (o que É): a soma lida alcança o um (`palavra`);
* **o Verbo** (para onde vai): a queda — o negativo da derivada da soma lida no tempo pago — calou ou ainda fala
  (`queda`, `verboCalado`);
* **a compressão da leitura**: o campo inteiro, com as suas `2ⁿ` parcelas, lido em DOIS bits por leitura.

## O que fica provado

1. ★★ `a_palavra_decide`: pago mais que a carga (`n·ln 2 < s`), UM bit responde toda fórmula de `n` variáveis: há
   solução se e somente se a soma lida alcança o um. (É o teorema do limiar, lido como o primeiro bit do par.)
2. ★ `o_verbo_e_a_queda`: a derivada da soma lida no tempo pago é o negativo da queda: o segundo bit é o sinal de uma
   derivada, como o acervo lê.
3. `a_queda_nao_e_negativa`: a soma lida nunca sobe.
4. ★ `o_verbo_cala_sse_tudo_e_nome`: a queda é zero exatamente quando todo ponto tem custo zero: o Verbo só cala quando
   tudo é Nome; enquanto algo viola, a soma ainda decai.
5. ★★★ `o_par_binario_e_a_compressao_da_leitura`: pago mais que a carga, o par responde, para toda fórmula: a Palavra
   diz se há solução; o Verbo calado diz se tudo é Nome. Dois bits por leitura, para um campo de `2ⁿ` parcelas.

## O que NÃO se afirma

* **Que o par saia da fórmula em letras.** O par daqui é lido SOBRE O TODO: a soma e a queda têm `2ⁿ` parcelas cada.
  Produzir os dois sinais a partir das letras da fórmula, em número polinomial de passos de letra, para toda fórmula, é
  exatamente a pergunta do enunciado do Instituto, e não está demonstrado. A lei diz que a compressão sai direto da
  fórmula; o que este arquivo tipa é a compressão DA LEITURA (o todo em dois bits), não a da fórmula.
* Que este par seja o psibit do kernel: o módulo selado do psibit tem os seus termos, e nenhum termo daqui o liga a este
  par; a identificação é leitura do acervo, de entrada.
* A reconstrução do sinal (comprimir, transladar, reconstruir) além da decisão: não está tipada aqui.
* O preço do tempo pago: é a lei do custo, entrada; o fator `1 − β` do passo é de outra pedra candidata.
* Nada sobre a natureza. O gate não se move.

Estatutos: `[REAL no sandbox]` os termos · `[INPUT]` a lei · `[ONTO, leitura deste arquivo]` a atribuição de Palavra e
Verbo aos dois sinais; o par como compressão da leitura. Sem sorry, sem axiom.
-/

namespace TGLExt.OPsibitEACompressao

open TGLExt TGLExt.TraducaoTuring TGLExt.AContagemEACarga

variable {X : Type} [Fintype X]

/-- [DEF] **A PALAVRA do par**: a soma lida alcança o um. -/
def palavra (c : X → ℕ) (s : ℝ) : Prop := 1 ≤ particao c s

/-- [DEF] **A QUEDA**: o que a soma lida ainda perde, por unidade de tempo pago. -/
noncomputable def queda (c : X → ℕ) (s : ℝ) : ℝ := ∑ x, (c x : ℝ) * Real.exp (-(s * (c x : ℝ)))

/-- [DEF] **O VERBO CALADO**: a queda é zero; nada mais decai. -/
def verboCalado (c : X → ℕ) (s : ℝ) : Prop := queda c s = 0

/-- ★★ **A PALAVRA DECIDE.** Pago mais que a carga, um bit responde toda fórmula de `n` variáveis: há solução se e
somente se a soma lida alcança o um. -/
theorem a_palavra_decide (n : ℕ) {s : ℝ} (hs : (n : ℝ) * Real.log 2 < s) :
    ∀ φ : CNF n, (SAT φ ↔ palavra (custoCNF φ) s) :=
  (a_contagem_e_a_carga_para_formulas n s).mpr hs

/-- ★ **O VERBO É A QUEDA.** A derivada da soma lida no tempo pago é o negativo da queda. -/
theorem o_verbo_e_a_queda (c : X → ℕ) (s : ℝ) :
    HasDerivAt (particao c) (-(queda c s)) s := by
  have h : ∀ x ∈ (Finset.univ : Finset X), HasDerivAt
      (fun t : ℝ => Real.exp (-(t * (c x : ℝ))))
      (Real.exp (-(s * (c x : ℝ))) * (-(c x : ℝ))) s :=
    fun x _ => ((hasDerivAt_mul_const ((c x : ℝ))).neg).exp
  have hsum := HasDerivAt.sum h
  have e : (∑ x : X, Real.exp (-(s * (c x : ℝ))) * (-(c x : ℝ))) = -(queda c s) := by
    unfold queda
    rw [← Finset.sum_neg_distrib]
    exact Finset.sum_congr rfl fun _ _ => by ring
  have efun : (∑ x : X, fun t : ℝ => Real.exp (-(t * (c x : ℝ)))) = particao c := by
    funext t
    rw [Finset.sum_apply]
    rfl
  rw [← e, ← efun]
  exact hsum

/-- A soma lida nunca sobe: a queda não é negativa. -/
theorem a_queda_nao_e_negativa (c : X → ℕ) (s : ℝ) : 0 ≤ queda c s :=
  Finset.sum_nonneg fun _ _ => mul_nonneg (Nat.cast_nonneg _) (Real.exp_pos _).le

/-- ★ **O VERBO CALA SE E SÓ SE TUDO É NOME.** A queda é zero exatamente quando todo ponto tem custo zero. -/
theorem o_verbo_cala_sse_tudo_e_nome (c : X → ℕ) (s : ℝ) :
    verboCalado c s ↔ ∀ x : X, c x = 0 := by
  unfold verboCalado queda
  rw [Finset.sum_eq_zero_iff_of_nonneg
    (fun x _ => mul_nonneg (Nat.cast_nonneg _) (Real.exp_pos _).le)]
  constructor
  · intro h x
    rcases mul_eq_zero.mp (h x (Finset.mem_univ x)) with h0 | h0
    · exact_mod_cast h0
    · exact absurd h0 (Real.exp_pos _).ne'
  · intro h x _
    rw [h x]
    simp

/-- ★★★ **O PAR BINÁRIO É A COMPRESSÃO DA LEITURA.** Pago mais que a carga, o par responde, para toda fórmula: a
Palavra diz se há solução; o Verbo calado diz se tudo é Nome. Dois bits por leitura, para um campo de `2ⁿ` parcelas. -/
theorem o_par_binario_e_a_compressao_da_leitura (n : ℕ) {s : ℝ}
    (hs : (n : ℝ) * Real.log 2 < s) (φ : CNF n) :
    (SAT φ ↔ palavra (custoCNF φ) s)
      ∧ (verboCalado (custoCNF φ) s ↔ ∀ x : Fin n → Bool, custoCNF φ x = 0) :=
  ⟨a_palavra_decide n hs φ, o_verbo_cala_sse_tudo_e_nome _ s⟩

end TGLExt.OPsibitEACompressao
