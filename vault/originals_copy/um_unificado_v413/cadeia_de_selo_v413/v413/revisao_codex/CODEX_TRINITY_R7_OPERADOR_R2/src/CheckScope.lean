import Trinity

set_option autoImplicit false
namespace Codex.TrinityR7Review
open TGLExt TGLExt.TraducaoTuring TGLExt.Trinity

-- Synthetic real parameters below are boundary controls, not values of beta_TGL.
theorem flat_weight {n : ℕ} (β : ℝ) (k : ℕ) (φ : CNF n)
    (h : ∀ x, custoCNF φ x = 1) :
    peso β k φ = (2 : ℝ) ^ n * (1 - β) ^ k := by
  unfold peso
  simp only [h, Nat.mul_one]
  rw [Finset.sum_const, Finset.card_univ, Fintype.card_fun,
    Fintype.card_bool, Fintype.card_fin, nsmul_eq_mul]
  push_cast
  ring

theorem flat_has_no_solution {n : ℕ} (φ : CNF n)
    (h : ∀ x, custoCNF φ x = 1) : ¬ SAT φ := by
  rw [AContagemEACarga.sat_e_existir_custo_zero]
  rintro ⟨x, hx⟩
  rw [h x] at hx
  exact Nat.one_ne_zero hx

theorem zero_parameter_does_not_decay (k : ℕ) :
    peso 0 k oito = 8 ∧ solucoes oito = 0 := by
  constructor
  · rw [flat_weight 0 k oito oito_patamar_plano]
    norm_num
  · simp [solucoes, oito_patamar_plano]

theorem threshold_equality_is_still_wrong :
    peso (1 / 2) 3 oito = 1 ∧ peso (1 / 2) 4 oito = 1 / 2 ∧ ¬ SAT oito := by
  rw [flat_weight _ 3 oito oito_patamar_plano, flat_weight _ 4 oito oito_patamar_plano]
  norm_num [oito_sem_solucao]

theorem at_most_one_step_is_sharp :
    (∃ k : ℕ, (1 : ℝ) < k ∧ (k : ℝ) ≤ 2) ∧
    ¬ ∃ k : ℕ, (1 : ℝ) < k ∧ (k : ℝ) < 2 := by
  constructor
  · exact ⟨2, by norm_num, by norm_num⟩
  · rintro ⟨k, hk, hk2⟩
    have hn : 1 < k := by exact_mod_cast hk
    have hn2 : k < 2 := by exact_mod_cast hk2
    omega

theorem zero_load_requires_a_whole_step {c : ℝ} (hc : 0 < c) :
    ∀ k : ℕ, (0 : ℝ) < k * c → (k : ℝ) * c ≤ 0 + c → (k : ℝ) * c = c := by
  intro k hp hle
  have hk : k ≠ 0 := by intro h; subst k; simp at hp
  have hn : 1 ≤ k := Nat.one_le_iff_ne_zero.mpr hk
  have hr : (1 : ℝ) ≤ k := by exact_mod_cast hn
  have hl : c ≤ (k : ℝ) * c := by nlinarith
  linarith

theorem no_extra_hypotheses_on_the_flat_threshold {n : ℕ} {β : ℝ}
    (hβ : β < 1) (k : ℕ) (φ : CNF n) (hφ : ∀ x, custoCNF φ x = 1) :
    (peso β k φ < 1 ↔ (n : ℝ) * Real.log 2 < k * (-Real.log (1 - β))) := by
  have h := no_patamar_plano_a_carga_e_exata hβ k hφ
  simpa only [not_le] using not_congr h

theorem distinct_names_decide_the_examples :
    (nomesDaFronteira oito).dedup = [0] ∧
    (nomesDaFronteira sete).dedup = [0] ∧
    atravessaPelos (nomesDaFronteira oito).dedup oito = false ∧
    atravessaPelos (nomesDaFronteira sete).dedup sete = true := by decide

theorem no_forced_energy_account_without_hLandauer (m : ℕ) {kB T : ℝ}
    (hk : 0 < kB) (hT : 0 < T) :
    ¬ ((2 : ℝ) ^ (m + 1) * (kB * T * Real.log 2) ≤ (0 : ℝ)) := by
  exact not_le.mpr (mul_pos (pow_pos (by norm_num) _) (TGLExt.landauer_floor_pos kB T hk hT))

end Codex.TrinityR7Review

#print axioms Codex.TrinityR7Review.flat_weight
#print axioms Codex.TrinityR7Review.flat_has_no_solution
#print axioms Codex.TrinityR7Review.zero_parameter_does_not_decay
#print axioms Codex.TrinityR7Review.threshold_equality_is_still_wrong
#print axioms Codex.TrinityR7Review.at_most_one_step_is_sharp
#print axioms Codex.TrinityR7Review.zero_load_requires_a_whole_step
#print axioms Codex.TrinityR7Review.no_extra_hypotheses_on_the_flat_threshold
#print axioms Codex.TrinityR7Review.distinct_names_decide_the_examples
#print axioms Codex.TrinityR7Review.no_forced_energy_account_without_hLandauer
