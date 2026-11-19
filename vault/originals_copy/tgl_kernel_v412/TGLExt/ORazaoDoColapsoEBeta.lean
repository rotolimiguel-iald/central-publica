import TGLExt.OPassoEOFim

set_option autoImplicit false
set_option maxHeartbeats 800000

/-!
# A razão do colapso: sem o pagamento o ciclo não fecha; com o passo 1 − β, o polinômio existe

## A leitura que este arquivo tipa

O colapso é a razão do polinômio existir: sem o pagamento, o ciclo não fecha; com o passo `1 − β`, o ciclo fecha em
linha na carga, para toda fórmula [INPUT/ONTO: definição da teoria, entrada, não teorema]. Este arquivo prova a parte
dela que cabe nos termos do kernel, na máquina da teoria.

## O que fica provado

1. ★ `sem_colapso_nao_ha_fim`: com o fator 1 (nenhum pagamento), para NENHUM número de passos a soma lida decide
   todas as fórmulas (é `OPassoEOFim.com_o_passo_de_cem_por_cento_o_ciclo_nao_fecha`).
2. ★ `com_colapso_ha_fim_linear`: com o fator `1 − β`, bastam `k > n·ln 2 / β` passos para toda fórmula (é
   `OPassoEOFim.bastam_passos_lineares`).
3. ★★ `a_razao_do_colapso`: a conjunção dos dois, para o mesmo `n` e o mesmo número de passos: sem o pagamento, o
   ciclo não fecha para toda fórmula; com o passo `1 − β`, fecha em linha na carga.

## O que NÃO se afirma

* Que o colapso seja a razão do ser do polinômio: é definição da teoria [INPUT/ONTO]. O termo é a conjunção do item 3,
  na família de passos de fator `1 − β`: com `β = 0` (nenhum pagamento), nenhum número de passos fecha o ciclo para
  toda fórmula; com `β` entre 0 e 1, bastam `k > n·ln 2/β` passos.
* Que a IALD seja a forma matricial do polinômio lida em runtime, e o que ela representa na fórmula de von Neumann: é
  leitura da teoria [INPUT/ONTO]. Nenhum termo deste arquivo trata de matrizes, de runtime ou da fórmula de von
  Neumann; β é parâmetro real, e a identificação com o β da teoria é entrada.
* Os passos são atos sobre o todo, não movimentos de cabeça na fita: a régua do Instituto fica com a sua contagem.
* Nada sobre a natureza.
-/

namespace TGLExt.ORazaoDoColapsoEBeta

open TGLExt TGLExt.TraducaoTuring TGLExt.AContagemEACarga TGLExt.OPassoEOFim

/-- ★ **SEM O COLAPSO, NÃO HÁ FIM**: com o fator 1, para nenhum `k` a soma lida decide todas as fórmulas. -/
theorem sem_colapso_nao_ha_fim (n : ℕ) (k : ℕ) :
    ¬ ∀ φ : CNF n, (SAT φ ↔ 1 ≤ ∑ x : Fin n → Bool, (1 - (0 : ℝ)) ^ (k * custoCNF φ x)) :=
  OPassoEOFim.com_o_passo_de_cem_por_cento_o_ciclo_nao_fecha n k

/-- ★ **COM O COLAPSO, HÁ FIM LINEAR**: com o fator `1 − β`, bastam `k > n·ln 2 / β` passos para toda fórmula. -/
theorem com_colapso_ha_fim_linear (n : ℕ) (β : ℝ) (hβ0 : 0 < β) (hβ1 : β < 1) (k : ℕ)
    (hk : (n : ℝ) * Real.log 2 / β < k) :
    ∀ φ : CNF n, (SAT φ ↔ 1 ≤ ∑ x : Fin n → Bool, (1 - β) ^ (k * custoCNF φ x)) :=
  OPassoEOFim.bastam_passos_lineares n β hβ0 hβ1 k hk

/-- ★★ **A RAZÃO DO COLAPSO**: sem o pagamento, o ciclo não fecha para
toda fórmula; com o passo `1 − β`, o ciclo fecha em linha na carga para toda fórmula. -/
theorem a_razao_do_colapso (n : ℕ) (β : ℝ) (hβ0 : 0 < β) (hβ1 : β < 1) (k : ℕ)
    (hk : (n : ℝ) * Real.log 2 / β < k) :
    (¬ ∀ φ : CNF n, (SAT φ ↔ 1 ≤ ∑ x : Fin n → Bool, (1 - (0 : ℝ)) ^ (k * custoCNF φ x)))
    ∧ (∀ φ : CNF n, (SAT φ ↔ 1 ≤ ∑ x : Fin n → Bool, (1 - β) ^ (k * custoCNF φ x))) :=
  ⟨sem_colapso_nao_ha_fim n k, com_colapso_ha_fim_linear n β hβ0 hβ1 k hk⟩

end TGLExt.ORazaoDoColapsoEBeta
