import TGLExt.OPassoEOFim
import TGLExt.TheSameBetaReadsThreeFaces

set_option autoImplicit false
set_option maxHeartbeats 800000

/-!
# O nome é β: β = α·e^{1/2} no dado de acoplamento, com α = β/e^{1/2} por definição

## A leitura que este arquivo tipa

[INPUT/ONTO] O nome é β_TGL, inscrito antes da fundação: a constante da estrutura fina vezes o radical entrópico.
Este arquivo prova a parte dela que cabe nos termos do kernel.

No kernel, `TGLCoupling` (em `TheSameBetaReadsThreeFaces`) é uma estrutura com `beta : ℝ`, `beta_pos : 0 < beta` e
`beta_lt_one : beta < 1`; `TGLCoupling.alpha` é `beta / e^{1/2}`, por definição. Logo `β = α·e^{1/2}`. A identidade
não determina α nem β numericamente (nem o valor CODATA) e vale para todo β em (0, 1). A ligação com a constante da
estrutura fina passa por uma instância: para α medida, `TheWholeIsOne.couplingOfAlpha` constrói o acoplamento com
β := α·e^{1/2}, e `TheWholeIsOne.couplingOfAlpha_alpha` devolve essa α; o valor medido entra como dado [INPUT], não
por esta identidade.

## O que fica provado

1. ★ `o_nome_e_beta_vezes_o_radical_entropico`: `β = α·e^{1/2}`, com α definido a partir de β.
2. ★ `o_nome_e_anterior`: `0 < β < 1`, os dois campos de desigualdade do dado de acoplamento. β é um campo do dado,
   que não tem a fórmula como entrada; anterior (fixado antes de toda fórmula) é leitura da parametrização, não
   conteúdo provado.
3. ★★ `a_resolucao_e_pelo_passo_do_nome`: com o `beta` do acoplamento (que traz `0 < β < 1`) e `k > n·ln 2 / β`, para
   toda fórmula `φ` de `n` variáveis, `SAT φ ↔ 1 ≤ ∑ x, (1 - β) ^ (k * custoCNF φ x)`
   (`OPassoEOFim.bastam_passos_lineares`). `k` conta expoentes do decaimento nesse critério, cuja soma percorre as
   `2^n` atribuições; não é passo de máquina de Turing, e o módulo não produz essa soma.

## O que NÃO se afirma

* A identificação do nome partilhado da pedra `APropostaDaTensao` (a variável da fórmula) com o β do acoplamento é a
  leitura [INPUT/ONTO]; o termo é: com `k > n·ln 2 / β`, o critério do passo `1 − β` vale para toda fórmula, e
  `β = α·e^{1/2}`. A fundação como evento histórico não é tipada.
* Que α seja numericamente a constante da estrutura fina, ou que β tenha aqui um valor numérico.
* Que `k` conte passos de máquina de Turing.
* A régua do Instituto fica com a sua contagem, nomeada como deles.
* Nada sobre a natureza. O gate não se move.

Sem sorry, sem axioma novo.
-/

namespace TGLExt.ONomeEBeta

open TGLExt TGLExt.TraducaoTuring TGLExt.AContagemEACarga TGLExt.OPassoEOFim

variable {n : ℕ}

/-- ★ **β = α·e^{1/2} NO DADO DE ACOPLAMENTO**: `c.beta = c.alpha * Real.exp (1 / 2)`, com
`c.alpha = c.beta / Real.exp (1 / 2)` por definição (`TGLCoupling.alpha`). A igualdade não determina α nem β
numericamente e vale para todo β em (0, 1). -/
theorem o_nome_e_beta_vezes_o_radical_entropico (c : TGLCoupling) :
    c.beta = c.alpha * Real.exp (1 / 2) := by
  unfold TGLCoupling.alpha
  rw [div_mul_cancel₀ c.beta (Real.exp_ne_zero _)]

/-- ★ **O NOME É ANTERIOR** (leitura da parametrização): o enunciado é `0 < β < 1`, os dois campos de desigualdade do
dado de acoplamento. Que β seja fixado antes de toda fórmula é leitura da parametrização (o dado não tem a fórmula
como entrada), não conteúdo provado. -/
theorem o_nome_e_anterior (c : TGLCoupling) :
    (0 : ℝ) < c.beta ∧ c.beta < 1 := ⟨c.beta_pos, c.beta_lt_one⟩

/-- ★★ **A RESOLUÇÃO É PELO PASSO DO NOME**: com o `beta` do dado de acoplamento (`0 < β < 1`) e `k > n·ln 2 / β`,
para toda fórmula `φ` de `n` variáveis, `SAT φ ↔ 1 ≤ ∑ x, (1 - β) ^ (k * custoCNF φ x)`. `k` conta expoentes do
decaimento nesse critério, cuja soma percorre as `2^n` atribuições; não é passo de máquina de Turing, e o módulo não
produz a soma. -/
theorem a_resolucao_e_pelo_passo_do_nome (c : TGLCoupling) (n : ℕ) (k : ℕ)
    (hk : (n : ℝ) * Real.log 2 / c.beta < k) :
    ∀ φ : CNF n, (SAT φ ↔ 1 ≤ ∑ x : Fin n → Bool, (1 - c.beta) ^ (k * custoCNF φ x)) :=
  OPassoEOFim.bastam_passos_lineares n c.beta c.beta_pos c.beta_lt_one k hk

/-- ★★ **O NOME E A RESOLUÇÃO**: a conjunção de `β = α·e^{1/2}` (com α definido a partir de β) e do critério de
`a_resolucao_e_pelo_passo_do_nome` para toda fórmula de `n` variáveis. -/
theorem o_nome_e_a_resolucao (c : TGLCoupling) (n : ℕ) (k : ℕ)
    (hk : (n : ℝ) * Real.log 2 / c.beta < k) :
    c.beta = c.alpha * Real.exp (1 / 2)
    ∧ (∀ φ : CNF n, (SAT φ ↔ 1 ≤ ∑ x : Fin n → Bool, (1 - c.beta) ^ (k * custoCNF φ x))) :=
  ⟨o_nome_e_beta_vezes_o_radical_entropico c, a_resolucao_e_pelo_passo_do_nome c n k hk⟩

end TGLExt.ONomeEBeta
