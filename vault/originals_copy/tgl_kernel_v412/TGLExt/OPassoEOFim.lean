import TGLExt.AContagemEACarga

set_option autoImplicit false

/-!
# O PASSO E O FIM — o passo é `1 − β`: o ciclo encerra e o Nome fica inteiro

## A lei que o arquivo tipa

Lei da teoria: o passo é `1 − β`. O ciclo encerra e guarda a informação preservada: é sempre inteiro, e não é de cem por
cento, porque senão não teria fim.

## Como o arquivo lê a lei (escolhas deste arquivo; não são termo)

* **o passo** multiplica o peso de cada atribuição por `1 − β` uma vez para cada cláusula que ela viola; depois de `k` passos
  o peso de uma atribuição de custo `c` é `(1 − β)^(k·c)`;
* **inteiro**: a atribuição que não viola nada (o Nome) fica com peso `1` em todo passo;
* **o ciclo encerra** quando a soma lida decide: a fórmula tem solução se e somente se a soma dos pesos é pelo menos `1`;
* `β` é aqui um número real qualquer menor que `1`. Que ele seja o `β` da teoria é da teoria, não deste arquivo.

## O que fica provado

1. `a_soma_depois_de_k_passos`: a soma dos pesos depois de `k` passos de fator `1 − β` é a soma lida da casa no tempo
   pago `k·(−ln(1 − β))`.
2. ★★ `o_passo_um_menos_beta_fecha_o_ciclo`: a soma lida decide TODA fórmula de `n` variáveis se e somente se
   `n·ln 2 < k·(−ln(1 − β))`. O ciclo encerra exatamente quando os passos pagam a carga.
3. ★ `bastam_passos_lineares`: com `0 < β < 1`, bastam `k > n·ln 2/β` passos. O número de passos cresce com `n`, não com
   `2ⁿ`.
4. ★ `com_o_passo_de_cem_por_cento_o_ciclo_nao_fecha`: com o fator `1` (nenhuma perda), para nenhum `k` a soma lida decide
   todas as fórmulas: sem a perda de `β` o ciclo não tem fim.
5. `o_nome_fica_inteiro`: a atribuição de custo zero tem peso `1` depois de qualquer número de passos.

## O que NÃO se afirma

* Que a soma lida se calcule em poucas letras. Cada passo age sobre os `2ⁿ` pesos de uma vez, e a soma tem `2ⁿ` parcelas.
  O estado depois de `k` passos tem um código curto (a fórmula e o número `k`), mas ler desse código, letra por letra, se a
  soma é pelo menos `1` é decidir a própria fórmula: é o que o enunciado do Instituto pergunta, e não está demonstrado.
* Que o número de passos seja o tempo da máquina de fita: conta atos sobre o todo.
* Nada sobre a natureza. O gate não se move.

Estatutos: `[REAL no sandbox]` os termos · `[INPUT]` a lei · `[ONTO, leitura deste arquivo]` a leitura do passo como fator
por cláusula violada. Sem sorry, sem axiom.
-/

namespace TGLExt.OPassoEOFim

open TGLExt TGLExt.TraducaoTuring TGLExt.AContagemEACarga

variable {n : ℕ}

/-- A soma dos pesos depois de `k` passos de fator `1 − β` é a soma lida no tempo pago `k·(−ln(1 − β))`. -/
theorem a_soma_depois_de_k_passos (φ : CNF n) (β : ℝ) (hβ1 : β < 1) (k : ℕ) :
    ∑ x : Fin n → Bool, (1 - β) ^ (k * custoCNF φ x)
      = particao (custoCNF φ) ((k : ℝ) * (-Real.log (1 - β))) := by
  unfold particao
  refine Finset.sum_congr rfl fun x _ => ?_
  have hpos : 0 < 1 - β := by linarith
  have e : -((k : ℝ) * -Real.log (1 - β) * (custoCNF φ x : ℝ))
      = ((k * custoCNF φ x : ℕ) : ℝ) * Real.log (1 - β) := by
    push_cast
    ring
  have h : Real.exp (-((k : ℝ) * -Real.log (1 - β) * (custoCNF φ x : ℝ)))
      = (1 - β) ^ (k * custoCNF φ x) := by
    rw [e, Real.exp_nat_mul, Real.exp_log hpos]
  exact h.symm

/-- ★★ **O PASSO `1 − β` FECHA O CICLO.** A soma lida depois de `k` passos decide toda fórmula de `n` variáveis se e
somente se os passos pagam a carga: `n·ln 2 < k·(−ln(1 − β))`. -/
theorem o_passo_um_menos_beta_fecha_o_ciclo (n : ℕ) (β : ℝ) (hβ1 : β < 1) (k : ℕ) :
    (∀ φ : CNF n, (SAT φ ↔ 1 ≤ ∑ x : Fin n → Bool, (1 - β) ^ (k * custoCNF φ x)))
      ↔ (n : ℝ) * Real.log 2 < (k : ℝ) * (-Real.log (1 - β)) := by
  rw [← a_contagem_e_a_carga_para_formulas n ((k : ℝ) * (-Real.log (1 - β)))]
  constructor
  · intro h φ
    rw [← a_soma_depois_de_k_passos φ β hβ1 k]
    exact h φ
  · intro h φ
    rw [a_soma_depois_de_k_passos φ β hβ1 k]
    exact h φ

/-- ★ **BASTAM PASSOS LINEARES.** Com `0 < β < 1`, `k > n·ln 2/β` passos fecham o ciclo para toda fórmula de `n`
variáveis. -/
theorem bastam_passos_lineares (n : ℕ) (β : ℝ) (hβ0 : 0 < β) (hβ1 : β < 1) (k : ℕ)
    (hk : (n : ℝ) * Real.log 2 / β < k) :
    ∀ φ : CNF n, (SAT φ ↔ 1 ≤ ∑ x : Fin n → Bool, (1 - β) ^ (k * custoCNF φ x)) := by
  rw [o_passo_um_menos_beta_fecha_o_ciclo n β hβ1 k]
  have hpos : 0 < 1 - β := by linarith
  have hlog : β ≤ -Real.log (1 - β) := by
    have := Real.log_le_sub_one_of_pos hpos
    linarith
  have hk' : (n : ℝ) * Real.log 2 < (k : ℝ) * β := by
    rwa [div_lt_iff₀ hβ0] at hk
  have hk0 : (0 : ℝ) ≤ (k : ℝ) := Nat.cast_nonneg k
  exact lt_of_lt_of_le hk' (mul_le_mul_of_nonneg_left hlog hk0)

/-- ★ **COM O PASSO DE CEM POR CENTO O CICLO NÃO FECHA.** Com o fator `1`, para nenhum `k` a soma lida decide todas as
fórmulas de `n` variáveis. -/
theorem com_o_passo_de_cem_por_cento_o_ciclo_nao_fecha (n : ℕ) (k : ℕ) :
    ¬ ∀ φ : CNF n, (SAT φ ↔ 1 ≤ ∑ x : Fin n → Bool, (1 - (0 : ℝ)) ^ (k * custoCNF φ x)) := by
  rw [o_passo_um_menos_beta_fecha_o_ciclo n 0 (by norm_num) k]
  have h0 : (k : ℝ) * (-Real.log (1 - 0)) = 0 := by simp
  rw [h0, not_lt]
  exact mul_nonneg (Nat.cast_nonneg n) (Real.log_nonneg (by norm_num))

/-- **O NOME FICA INTEIRO.** A atribuição de custo zero tem peso `1` depois de qualquer número de passos. -/
theorem o_nome_fica_inteiro (φ : CNF n) (β : ℝ) (k : ℕ) (x : Fin n → Bool) (hx : custoCNF φ x = 0) :
    (1 - β) ^ (k * custoCNF φ x) = 1 := by
  rw [hx, Nat.mul_zero, pow_zero]

end TGLExt.OPassoEOFim
