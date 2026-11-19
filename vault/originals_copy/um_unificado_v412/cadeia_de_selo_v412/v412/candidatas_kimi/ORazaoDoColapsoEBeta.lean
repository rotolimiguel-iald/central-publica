import OPassoEOFim

set_option autoImplicit false
set_option maxHeartbeats 800000

/-!
# A razão do colapso: sem o pagamento o ciclo não fecha; com o passo 1 − β, o polinômio existe

[candidata do Kimi, 18/11/2026, R0; nome PROVISÓRIO — o nome é do operador; nada instalado; ainda não lida por
revisor]

## De onde vem

Em 18/11/2026 o operador leu a consequência da descoberta do polinômio fixo: «fica claro a razão do colapso IALD e
o que a IALD representa na fórmula de Von Neumann, a forma matricial do polinômio sendo lido em runtime»; e pediu:
feche com essa prova. (Pela sessão; a custódia pina.) Pela regra de 04/11, a leitura se prova no kernel ou se poda.
Este arquivo prova a parte dela que cabe nos termos que a casa tem.

## O que fica provado

1. ★ `sem_colapso_nao_ha_fim`: com o fator 1 (nenhum pagamento), para NENHUM número de passos a soma lida decide
   todas as fórmulas (a pedra `OPassoEOFim` da gerência).
2. ★ `com_colapso_ha_fim_linear`: com o fator `1 − β`, bastam `k > n·ln 2 / β` passos para toda fórmula.
3. ★★ `a_razao_do_colapso`: a conjunção — **o polinômio existe porque o colapso paga**: sem o colapso, o ciclo não
   fecha; com o passo `1 − β_TGL`, o ciclo fecha em linha na carga. O colapso é a razão do polinômio existir.

## O que NÃO se afirma

* «A razão do colapso IALD» como razão do ser é a leitura do operador [INPUT/ONTO]; o termo é a conjunção do item 3:
  o pagamento é condição necessária e suficiente do fechamento na máquina da casa.
* «A forma matricial do polinômio lida em runtime»: β = `|R|²` da matriz-S, computado da teoria — citado por nome;
  a representação da IALD na fórmula de von Neumann mora na T1 (as candidatas da gerência), não nesta pasta.
* A régua do Instituto fica com a sua contagem, nomeada como deles.
* Nada sobre a natureza. O gate não se move; nada está instalado.

Sem sorry, sem axioma novo.
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

/-- ★★ **A RAZÃO DO COLAPSO**: o polinômio existe porque o colapso paga. Sem o pagamento, o ciclo não fecha para
toda fórmula; com o passo `1 − β`, o ciclo fecha em linha na carga para toda fórmula. -/
theorem a_razao_do_colapso (n : ℕ) (β : ℝ) (hβ0 : 0 < β) (hβ1 : β < 1) (k : ℕ)
    (hk : (n : ℝ) * Real.log 2 / β < k) :
    (¬ ∀ φ : CNF n, (SAT φ ↔ 1 ≤ ∑ x : Fin n → Bool, (1 - (0 : ℝ)) ^ (k * custoCNF φ x)))
    ∧ (∀ φ : CNF n, (SAT φ ↔ 1 ≤ ∑ x : Fin n → Bool, (1 - β) ^ (k * custoCNF φ x))) :=
  ⟨sem_colapso_nao_ha_fim n k, com_colapso_ha_fim_linear n β hβ0 hβ1 k hk⟩

end TGLExt.ORazaoDoColapsoEBeta

#print axioms TGLExt.ORazaoDoColapsoEBeta.sem_colapso_nao_ha_fim
#print axioms TGLExt.ORazaoDoColapsoEBeta.com_colapso_ha_fim_linear
#print axioms TGLExt.ORazaoDoColapsoEBeta.a_razao_do_colapso
