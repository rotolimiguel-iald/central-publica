import TGLExt.EntregaBeta
set_option autoImplicit false

/-!
# O produtor da leitura β conta as soluções

A leitura β (`Codex.EntregaBeta`) deixa como hipótese `hr` um produtor `reader : CNF n → ℕ` cujo numerador
diádico aproxima a soma normalizada com erro ≤ 1/(4·2ⁿ), no relógio `clock m n` fixado por β. Este módulo prova
três coisas sobre essa hipótese de precisão:

1. ela é habitada: o numerador `4 · contaSolucoes φ` a cumpre;
2. ela determina o número de soluções: todo produtor que a cumpre dá `(reader φ + 1) / 4 = contaSolucoes φ`;
3. com `TGLExt.TraducaoTuring.o_que_sou_das_solucoes`, esse número dividido por 2ⁿ é a leitura
   `oQueSou (nomeDasSolucoes (custoCNF φ))`.

Logo o produtor que falta é essa leitura escrita na fita: contar as soluções de toda CNF, não só decidir se há
uma. A decisão `2 ≤ reader φ` é `0 < contaSolucoes φ`.
-/

namespace TGLExt.SondaContagem

open TGLExt TGLExt.TraducaoTuring TGLExt.AContagemEACarga TGLExt.OPassoEOFim
open Codex.RelogioBeta Codex.LeituraBeta Codex.PonteLeituraBeta

variable {n : ℕ}

/-- O número de soluções da fórmula: as atribuições de custo zero. -/
def contaSolucoes (φ : CNF n) : ℕ :=
  (Finset.univ.filter (fun x : Fin n → Bool => custoCNF φ x = 0)).card

/-- A fórmula é satisfazível exatamente quando há ao menos uma solução. -/
theorem sat_sse_ha_solucao (φ : CNF n) : SAT φ ↔ 0 < contaSolucoes φ := by
  rw [sat_e_existir_custo_zero, contaSolucoes, Finset.card_pos, Finset.filter_nonempty_iff]
  simp

/-- Cada solução pesa exatamente 1 na soma; as demais atribuições pesam ≥ 0. -/
theorem a_soma_cobre_as_solucoes (c : TGLCoupling) (k : ℕ) (φ : CNF n) :
    (contaSolucoes φ : ℝ) ≤ weightedSum c k φ := by
  unfold contaSolucoes weightedSum
  have h1 : ((Finset.univ.filter (fun x : Fin n → Bool => custoCNF φ x = 0)).card : ℝ)
      = ∑ x ∈ Finset.univ.filter (fun x : Fin n → Bool => custoCNF φ x = 0),
          (1 - c.beta) ^ (k * custoCNF φ x) := by
    rw [Finset.card_eq_sum_ones, Nat.cast_sum, Nat.cast_one]
    refine Finset.sum_congr rfl (fun x hx => ?_)
    rw [(Finset.mem_filter.mp hx).2, Nat.mul_zero, pow_zero]
  rw [h1]
  exact Finset.sum_le_sum_of_subset_of_nonneg (Finset.filter_subset _ _)
    (fun y _ _ => pow_nonneg (sub_nonneg.mpr c.beta_lt_one.le) _)

/-- No relógio de β, o que não é solução soma menos de 1/4. -/
theorem a_soma_passa_das_solucoes_por_menos_de_um_quarto (c : TGLCoupling) (k : ℕ) (φ : CNF n)
    (hk : ((n : ℝ) + 2) * Real.log 2 / c.beta < k) :
    weightedSum c k φ < (contaSolucoes φ : ℝ) + 1 / 4 := by
  let s : ℝ := (k : ℝ) * (-Real.log (1 - c.beta))
  have hs : ((n : ℝ) + 2) * Real.log 2 < s := effective_time_gt c n k hk
  have hs0 : 0 ≤ s := le_of_lt (lt_of_le_of_lt
    (mul_nonneg (by positivity) (Real.log_nonneg one_le_two)) hs)
  have hsum := TGLExt.AEscala.a_flutuacao_do_fundo_e_cotada (custoCNF φ) hs0
  have hN : (Fintype.card (Fin n → Bool) : ℝ) = (2 : ℝ) ^ n := by
    rw [Fintype.card_fun, Fintype.card_bool, Fintype.card_fin]
    norm_num
  rw [hN] at hsum
  have hp : (0 : ℝ) < (2 : ℝ) ^ n := pow_pos (by norm_num) n
  have hexp : Real.exp (-s) < Real.exp (-((n : ℝ) * Real.log 2)) / 4 := by
    have hlt := Real.exp_lt_exp.mpr (show -s < -((n : ℝ) * Real.log 2) - 2 * Real.log 2 by nlinarith)
    have he2 : Real.exp (2 * Real.log 2) = (4 : ℝ) := by
      rw [show (2 : ℝ) * Real.log 2 = Real.log 2 + Real.log 2 by ring,
        Real.exp_add, Real.exp_log (by norm_num : (0 : ℝ) < 2)]
      norm_num
    rw [Real.exp_sub, he2] at hlt
    exact hlt
  have he : Real.exp (-((n : ℝ) * Real.log 2)) = ((2 : ℝ) ^ n)⁻¹ := by
    rw [Real.exp_neg, Real.exp_nat_mul, Real.exp_log (by norm_num : (0 : ℝ) < 2)]
  rw [he] at hexp
  have htail : (2 : ℝ) ^ n * Real.exp (-s) < 1 / 4 := by
    calc
      _ < (2 : ℝ) ^ n * (((2 : ℝ) ^ n)⁻¹ / 4) := mul_lt_mul_of_pos_left hexp hp
      _ = 1 / 4 := by rw [← mul_div_assoc, mul_inv_cancel₀ hp.ne']
  unfold weightedSum contaSolucoes
  rw [a_soma_depois_de_k_passos φ c.beta c.beta_lt_one k]
  exact lt_of_le_of_lt hsum (by linarith)

/-- O numerador diádico em reais: `dyadic n j = (j/4)/2ⁿ`. -/
theorem dyadic_em_reais (j : ℕ) : ((dyadic n j : ℚ) : ℝ) = ((j : ℝ) / 4) / (2 : ℝ) ^ n := by
  unfold dyadic
  push_cast
  rw [pow_add]
  ring

/-- O numerador que aproxima a soma com erro ≤ 1/4 determina o número de soluções. -/
theorem o_numerador_determina (j K : ℕ) (W : ℝ) (hlo : (K : ℝ) ≤ W) (hhi : W < (K : ℝ) + 1 / 4)
    (h : |(j : ℝ) / 4 - W| ≤ 1 / 4) : (j + 1) / 4 = K := by
  have hab := abs_le.mp h
  have h1 : 4 * (K : ℝ) ≤ (j : ℝ) + 1 := by linarith [hab.1]
  have h2 : (j : ℝ) < 4 * (K : ℝ) + 2 := by linarith [hab.2]
  have h1n : 4 * K ≤ j + 1 := by exact_mod_cast h1
  have h2n : j < 4 * K + 2 := by exact_mod_cast h2
  omega

/-- ★ O CONTADOR CUMPRE A PRECISÃO: o numerador `4 · contaSolucoes φ` satisfaz a hipótese de precisão `hr`,
para toda fórmula; a hipótese é habitada. -/
theorem o_contador_cumpre_a_precisao (c : TGLCoupling) (m : ℕ)
    (hm : Real.log 2 / c.beta < (m : ℝ)) (φ : CNF n) :
    |(dyadic n (4 * contaSolucoes φ) : ℝ) - normalizedSum c (clock m n) φ| ≤ 1 / (4 * (2 : ℝ) ^ n) := by
  have hlo := a_soma_cobre_as_solucoes c (clock m n) φ
  have hhi := a_soma_passa_das_solucoes_por_menos_de_um_quarto c (clock m n) φ (clock_sufficient c m hm n)
  have hp : (0 : ℝ) < (2 : ℝ) ^ n := pow_pos (by norm_num) n
  have h4 : (0 : ℝ) < 4 * (2 : ℝ) ^ n := by positivity
  have hd : ((dyadic n (4 * contaSolucoes φ) : ℚ) : ℝ) = (contaSolucoes φ : ℝ) / (2 : ℝ) ^ n := by
    rw [dyadic_em_reais]
    push_cast
    ring
  rw [hd]
  unfold normalizedSum
  rw [← sub_div, abs_div, abs_of_pos hp, abs_sub_comm, abs_of_nonneg (sub_nonneg.mpr hlo),
    div_le_div_iff₀ hp h4]
  have hq : (weightedSum c (clock m n) φ - (contaSolucoes φ : ℝ)) * 4 ≤ 1 := by linarith
  calc (weightedSum c (clock m n) φ - (contaSolucoes φ : ℝ)) * (4 * (2 : ℝ) ^ n)
      = ((weightedSum c (clock m n) φ - (contaSolucoes φ : ℝ)) * 4) * (2 : ℝ) ^ n := by ring
    _ ≤ 1 * (2 : ℝ) ^ n := mul_le_mul_of_nonneg_right hq hp.le

/-- ★ TODO PRODUTOR COM A PRECISÃO CONTA AS SOLUÇÕES: qualquer `reader` que cumpra a hipótese de precisão `hr`
devolve, em cada fórmula, o número de soluções: `(reader φ + 1) / 4 = contaSolucoes φ`. -/
theorem todo_produtor_com_a_precisao_conta_as_solucoes (c : TGLCoupling) (m : ℕ)
    (hm : Real.log 2 / c.beta < (m : ℝ)) (reader : CNF n → ℕ)
    (hr : ∀ φ, |(dyadic n (reader φ) : ℝ) - normalizedSum c (clock m n) φ| ≤ 1 / (4 * (2 : ℝ) ^ n))
    (φ : CNF n) : (reader φ + 1) / 4 = contaSolucoes φ := by
  have hlo := a_soma_cobre_as_solucoes c (clock m n) φ
  have hhi := a_soma_passa_das_solucoes_por_menos_de_um_quarto c (clock m n) φ (clock_sufficient c m hm n)
  have hp : (0 : ℝ) < (2 : ℝ) ^ n := pow_pos (by norm_num) n
  have h4 : (0 : ℝ) < 4 * (2 : ℝ) ^ n := by positivity
  have h := hr φ
  rw [dyadic_em_reais] at h
  unfold normalizedSum at h
  rw [← sub_div, abs_div, abs_of_pos hp, div_le_div_iff₀ hp h4] at h
  have hmul : (|((reader φ : ℕ) : ℝ) / 4 - weightedSum c (clock m n) φ| * 4) * (2 : ℝ) ^ n
      ≤ 1 * (2 : ℝ) ^ n := by
    calc (|((reader φ : ℕ) : ℝ) / 4 - weightedSum c (clock m n) φ| * 4) * (2 : ℝ) ^ n
        = |((reader φ : ℕ) : ℝ) / 4 - weightedSum c (clock m n) φ| * (4 * (2 : ℝ) ^ n) := by ring
      _ ≤ 1 * (2 : ℝ) ^ n := h
  have h' : |((reader φ : ℕ) : ℝ) / 4 - weightedSum c (clock m n) φ| ≤ 1 / 4 := by
    have := le_of_mul_le_mul_right hmul hp
    linarith
  exact o_numerador_determina (reader φ) (contaSolucoes φ) _ hlo hhi h'

/-- ★ O PRODUTOR QUE FALTA É A LEITURA DA IALD ESCRITA NA FITA: todo produtor com a precisão `hr` devolve,
depois de `(· + 1) / 4` e da divisão por 2ⁿ, exatamente `oQueSou (nomeDasSolucoes (custoCNF φ))`, a leitura do
Nome das soluções (`TGLExt.TraducaoTuring.o_que_sou_das_solucoes`). -/
theorem o_produtor_e_a_leitura_da_iald (c : TGLCoupling) (m : ℕ)
    (hm : Real.log 2 / c.beta < (m : ℝ)) (reader : CNF n → ℕ)
    (hr : ∀ φ, |(dyadic n (reader φ) : ℝ) - normalizedSum c (clock m n) φ| ≤ 1 / (4 * (2 : ℝ) ^ n))
    (φ : CNF n) :
    (((((reader φ + 1) / 4 : ℕ) : ℝ) / (2 : ℝ) ^ n : ℝ) : ℂ)
      = TGLExt.Identidade.oQueSou (nomeDasSolucoes (custoCNF φ)) := by
  rw [o_que_sou_das_solucoes, todo_produtor_com_a_precisao_conta_as_solucoes c m hm reader hr φ]
  have hN : (Fintype.card (Fin n → Bool) : ℝ) = (2 : ℝ) ^ n := by
    rw [Fintype.card_fun, Fintype.card_bool, Fintype.card_fin]
    norm_num
  rw [hN]
  rfl

/-- A decisão `2 ≤ reader φ` é “há ao menos uma solução”: `2 ≤ reader φ ↔ 0 < contaSolucoes φ`. -/
theorem a_decisao_e_haver_solucao (c : TGLCoupling) (m : ℕ)
    (hm : Real.log 2 / c.beta < (m : ℝ)) (reader : CNF n → ℕ)
    (hr : ∀ φ, |(dyadic n (reader φ) : ℝ) - normalizedSum c (clock m n) φ| ≤ 1 / (4 * (2 : ℝ) ^ n))
    (φ : CNF n) : 2 ≤ reader φ ↔ 0 < contaSolucoes φ := by
  have h := todo_produtor_com_a_precisao_conta_as_solucoes c m hm reader hr φ
  have hd := Codex.EntregaBeta.codeDecision_correct c m hm reader hr φ
  rw [← sat_sse_ha_solucao, ← hd]
  simp [Codex.EntregaBeta.codeDecision]

end TGLExt.SondaContagem
