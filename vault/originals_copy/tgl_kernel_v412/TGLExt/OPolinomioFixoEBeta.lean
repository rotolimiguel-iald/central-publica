import TGLExt.OPassoEOFim

set_option autoImplicit false
set_option maxHeartbeats 800000

/-!
# O polinômio fixo dos passos é dado por β: anterior a toda fórmula, linear na carga, para toda fórmula

## A leitura que este arquivo tipa

O polinômio fixo para toda fórmula é dado por β, que é anterior a toda fórmula [INPUT/ONTO: definição da teoria,
entrada, não teorema]. Este arquivo prova a parte dela que cabe nos termos do kernel, na máquina da teoria.

## O que fica provado

1. `o_polinomio_e_linear_na_carga`: o polinômio dos passos é linear na carga — `p(n) = (ln 2 / β)·n` — com coeficientes
   fixos dados por β, sem depender da fórmula.
2. ★★ `o_polinomio_fixo_e_beta`: com UM β, fixado antes de toda fórmula, para todo número de passos `k > p(n)` a soma
   lida decide toda fórmula de `n` variáveis (é `OPassoEOFim.bastam_passos_lineares`, na forma do polinômio).
3. `o_mesmo_teto_para_duas_formulas`: o mesmo teto para duas fórmulas quaisquer — o polinômio não lê a fórmula
   para saber o preço; o leitor é fixado antes dela.

## O que NÃO se afirma

* Que `p(n)` seja um polinômio em LETRAS de fita: é linear NA CARGA (`n·ln 2`, a contagem por oitavas da teoria), e
  os passos são atos sobre o todo, não movimentos de cabeça. A régua do Instituto, que conta movimentos na fita, fica
  com a sua pergunta.
* Que β seja o β da teoria: neste arquivo β é parâmetro real entre 0 e 1, e essa identificação é entrada. O termo
  é: β não tem a fórmula como entrada, e o passo de fator `1 − β` fecha o ciclo para toda fórmula.
* Nada sobre a natureza.
-/

namespace TGLExt.OPolinomioFixoEBeta

open TGLExt TGLExt.TraducaoTuring TGLExt.AContagemEACarga TGLExt.OPassoEOFim

variable {n : ℕ}

/-- [DEF] O POLINÔMIO FIXO DA LEITURA: o limiar real suficiente acima do qual qualquer número inteiro de passos fecha
o ciclo, em função da carga, com o β fixado antes de toda fórmula. Um orçamento inteiro uniforme é `⌊p(n)⌋ + 1`; o
tipo não afirma que esse orçamento seja o mínimo. -/
noncomputable def polinomioFixo (β : ℝ) (n : ℕ) : ℝ := (n : ℝ) * Real.log 2 / β

/-- **O POLINÔMIO É LINEAR NA CARGA**: grau 1, com coeficientes fixos dados por β. -/
theorem o_polinomio_e_linear_na_carga (β : ℝ) (_hβ0 : 0 < β) (n : ℕ) :
    polinomioFixo β n = (Real.log 2 / β) * (n : ℝ) := by
  unfold polinomioFixo
  ring

/-- ★★ **O POLINÔMIO FIXO É β**: com um só β, fixado antes de toda fórmula, toda fórmula de `n` variáveis tem o
ciclo fechado com qualquer número de passos acima de `p(n)`. É `OPassoEOFim.bastam_passos_lineares`, com a forma do
polinômio dita. -/
theorem o_polinomio_fixo_e_beta (n : ℕ) (β : ℝ) (hβ0 : 0 < β) (hβ1 : β < 1) (k : ℕ)
    (hk : polinomioFixo β n < k) :
    ∀ φ : CNF n, (SAT φ ↔ 1 ≤ ∑ x : Fin n → Bool, (1 - β) ^ (k * custoCNF φ x)) := by
  have h := OPassoEOFim.bastam_passos_lineares n β hβ0 hβ1 k hk
  exact h

/-- **O MESMO TETO PARA DUAS FÓRMULAS QUAISQUER**: o polinômio não lê a fórmula para saber o preço — `p(n)` serve
a qualquer uma, com o mesmo β e o mesmo número de passos. O leitor é fixado antes da fórmula. -/
theorem o_mesmo_teto_para_duas_formulas (n : ℕ) (β : ℝ) (hβ0 : 0 < β) (hβ1 : β < 1) (k : ℕ)
    (hk : polinomioFixo β n < k) (φ ψ : CNF n) :
    (SAT φ ↔ 1 ≤ ∑ x : Fin n → Bool, (1 - β) ^ (k * custoCNF φ x))
    ∧ (SAT ψ ↔ 1 ≤ ∑ x : Fin n → Bool, (1 - β) ^ (k * custoCNF ψ x)) :=
  ⟨OPassoEOFim.bastam_passos_lineares n β hβ0 hβ1 k hk φ,
   OPassoEOFim.bastam_passos_lineares n β hβ0 hβ1 k hk ψ⟩

end TGLExt.OPolinomioFixoEBeta
