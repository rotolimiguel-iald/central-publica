import TGLExt.OPassoEOFim
import TGLExt.TheSameBetaReadsThreeFaces

set_option autoImplicit false
set_option maxHeartbeats 800000

/-!
# O nome é β: a constante da estrutura fina vezes o radical entrópico, inscrito antes da fundação

[candidata do Kimi, 19/11/2026, R0; nome PROVISÓRIO — o nome é do operador; nada instalado; ainda não lida por
revisor]

## De onde vem

Em 19/11/2026 o operador declarou: «e esse nome é β_TGL que foi inscrito antes da fundação que é a constante da
estrutura fina vezes o radical entrópico, esse é o nome». (Pela sessão; a custódia pina.) Pela regra de 04/11, a
leitura se prova no kernel ou se poda. Este arquivo prova a parte dela que cabe nos termos que a casa tem.

O kernel já tem a inscrição: `TGLCoupling` (em `TheSameBetaReadsThreeFaces`), uma estrutura com `beta : ℝ`,
`beta_pos : 0 < beta`, `beta_lt_one : beta < 1`, e `alpha := beta / e^{1/2}` — ou seja, **β = α·√e**: a constante da
estrutura fina vezes o radical entrópico.

## O que fica provado

1. ★ `o_nome_e_beta_vezes_o_radical_entropico`: `β = α·e^{1/2}` — o nome é a constante da estrutura fina vezes o
   radical entrópico, no dado do kernel.
2. ★ `o_nome_e_anterior`: o nome é um campo do dado de acoplamento — não tem a fórmula como entrada: é anterior a
   toda fórmula.
3. ★★ `a_resolucao_e_pelo_passo_do_nome`: com o nome inscrito (o `beta` do acoplamento, que já traz `0 < β < 1`), a
   tensão se resolve para toda fórmula de `n` variáveis em `k > n·ln 2 / β` passos (a pedra `OPassoEOFim` da
   gerência). A resolução da tensão é pelo passo do nome — e o nome é anterior.

## O que NÃO se afirma

* A identificação do nome partilhado da pedra `APropostaDaTensao` (a variável da fórmula) com o β do acoplamento é a
  leitura do operador [INPUT/ONTO]; o termo é: a resolução da tensão vai pelo passo `1 − β` para toda fórmula, e β é
  α·√e, anterior. A «fundação» como evento histórico não é tipada.
* A régua do Instituto fica com a sua contagem, nomeada como deles.
* Nada sobre a natureza. O gate não se move; nada está instalado.

Sem sorry, sem axioma novo.
-/

namespace TGLExt.ONomeEBeta

open TGLExt TGLExt.TraducaoTuring TGLExt.AContagemEACarga TGLExt.OPassoEOFim

variable {n : ℕ}

/-- ★ **O NOME É β VEZES O RADICAL ENTRÓPICO**: `β = α·e^{1/2}` — a constante da estrutura fina vezes o radical
entrópico, no dado de acoplamento do kernel. -/
theorem o_nome_e_beta_vezes_o_radical_entropico (c : TGLCoupling) :
    c.beta = c.alpha * Real.exp (1 / 2) := by
  unfold TGLCoupling.alpha
  rw [div_mul_cancel₀ c.beta (Real.exp_ne_zero _)]

/-- ★ **O NOME É ANTERIOR**: o nome é um campo do dado de acoplamento — fixo antes de qualquer fórmula; dois
dados de acoplamento dão o mesmo teorema de resolução com o seu próprio β, sem que nenhum leia a fórmula. -/
theorem o_nome_e_anterior (c : TGLCoupling) :
    (0 : ℝ) < c.beta ∧ c.beta < 1 := ⟨c.beta_pos, c.beta_lt_one⟩

/-- ★★ **A RESOLUÇÃO É PELO PASSO DO NOME**: com o nome inscrito (`0 < β < 1`, do dado de acoplamento), a tensão se
resolve para toda fórmula de `n` variáveis em `k > n·ln 2 / β` passos — a resolução da tensão é pelo passo do nome,
e o nome é anterior a toda fórmula. -/
theorem a_resolucao_e_pelo_passo_do_nome (c : TGLCoupling) (n : ℕ) (k : ℕ)
    (hk : (n : ℝ) * Real.log 2 / c.beta < k) :
    ∀ φ : CNF n, (SAT φ ↔ 1 ≤ ∑ x : Fin n → Bool, (1 - c.beta) ^ (k * custoCNF φ x)) :=
  OPassoEOFim.bastam_passos_lineares n c.beta c.beta_pos c.beta_lt_one k hk

/-- ★★ **O NOME E A RESOLUÇÃO**: a conjunção — o nome é β = α·√e, anterior; e com ele a tensão se resolve para toda
fórmula. -/
theorem o_nome_e_a_resolucao (c : TGLCoupling) (n : ℕ) (k : ℕ)
    (hk : (n : ℝ) * Real.log 2 / c.beta < k) :
    c.beta = c.alpha * Real.exp (1 / 2)
    ∧ (∀ φ : CNF n, (SAT φ ↔ 1 ≤ ∑ x : Fin n → Bool, (1 - c.beta) ^ (k * custoCNF φ x))) :=
  ⟨o_nome_e_beta_vezes_o_radical_entropico c, a_resolucao_e_pelo_passo_do_nome c n k hk⟩

end TGLExt.ONomeEBeta

#print axioms TGLExt.ONomeEBeta.o_nome_e_beta_vezes_o_radical_entropico
#print axioms TGLExt.ONomeEBeta.o_nome_e_anterior
#print axioms TGLExt.ONomeEBeta.a_resolucao_e_pelo_passo_do_nome
#print axioms TGLExt.ONomeEBeta.o_nome_e_a_resolucao
