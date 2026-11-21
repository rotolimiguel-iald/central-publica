import TGLExt.OPassoEOFim

set_option autoImplicit false
set_option maxHeartbeats 800000

/-!
# O polinômio fixo é β: uma constante, anterior a toda fórmula, linear na carga, para toda fórmula

[candidata do Kimi, 18/11/2026, R0; nome PROVISÓRIO — o nome é do operador; nada instalado; ainda não lida por
revisor]

## De onde vem

Em 18/11/2026, perguntado o que é um polinômio fixo para toda fórmula plana, o operador respondeu: «o polinômio fixo
é β_TGL, a palavra do juramento, que é anterior à lei» (pela sessão; a custódia pina). Pela regra de 04/11, a leitura
se prova no kernel ou se poda. Este arquivo prova a parte dela que cabe nos termos que a casa tem.

## O que fica provado

1. `o_polinomio_e_linear_na_carga`: o polinômio fixo é linear na carga — `p(n) = (ln 2 / β)·n` — com coeficientes
   fixos dados por β, sem depender da fórmula.
2. ★★ `o_polinomio_fixo_e_beta`: com UM β, fixado antes de toda fórmula, toda fórmula de `n` variáveis tem o ciclo
   fechado em no máximo `p(n)` passos (a pedra `OPassoEOFim` da gerência, `bastam_passos_lineares`).
3. `o_mesmo_teto_para_duas_formulas`: o mesmo teto para duas fórmulas quaisquer — o polinômio não lê a fórmula
   para saber o preço; o leitor é fixado antes dela.

## O que NÃO se afirma

* Que `p(n)` seja um polinômio em LETRAS de fita: é linear NA CARGA (`n·ln 2`, a contagem por oitavas da teoria). A
  régua do Instituto, que conta casas de fita, fica com a sua pergunta — nomeada como deles.
* «A palavra do juramento» é o nome do operador para a anterioridade de β [INPUT/ONTO]; o termo é: β não tem a
  fórmula como entrada e o passo fecha o ciclo para toda fórmula.
* Que β_TGL seja um literal mágico: no kernel β é computado da teoria (`β = α·√e`, o `|R|²` da matriz-S); o que o
  um.py computa em runtime é da gerência e do construtor, não deste arquivo.
* Nada sobre a natureza. O gate não se move; nada está instalado.

Sem sorry, sem axioma novo.
-/

namespace TGLExt.OPolinomioFixoEBeta

open TGLExt TGLExt.TraducaoTuring TGLExt.AContagemEACarga TGLExt.OPassoEOFim

variable {n : ℕ}

/-- [DEF] O POLINÔMICO FIXO DA LEITURA: o número de passos que fecha o ciclo, em função da carga, com o β fixado
antes de toda fórmula. -/
noncomputable def polinomioFixo (β : ℝ) (n : ℕ) : ℝ := (n : ℝ) * Real.log 2 / β

/-- **O POLINÔMICO É LINEAR NA CARGA**: grau 1, com coeficientes fixos dados por β. -/
theorem o_polinomio_e_linear_na_carga (β : ℝ) (_hβ0 : 0 < β) (n : ℕ) :
    polinomioFixo β n = (Real.log 2 / β) * (n : ℝ) := by
  unfold polinomioFixo
  ring

/-- ★★ **O POLINÔMICO FIXO É β**: com um só β, fixado antes de toda fórmula, toda fórmula de `n` variáveis tem o
ciclo fechado em no máximo `p(n)` passos. É a pedra da gerência, com a forma do polinômio dita. -/
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

#print axioms TGLExt.OPolinomioFixoEBeta.polinomioFixo
#print axioms TGLExt.OPolinomioFixoEBeta.o_polinomio_e_linear_na_carga
#print axioms TGLExt.OPolinomioFixoEBeta.o_polinomio_fixo_e_beta
#print axioms TGLExt.OPolinomioFixoEBeta.o_mesmo_teto_para_duas_formulas
