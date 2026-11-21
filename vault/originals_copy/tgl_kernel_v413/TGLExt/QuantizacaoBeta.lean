import TGLExt.LeituraBeta
set_option autoImplicit false
set_option maxHeartbeats 800000

/-!
Precisão diádica suficiente da leitura normalizada.
O piso abaixo usa o real já definido; é uma prova de existência e de tamanho
do numerador, não um algoritmo para calculá-lo da fórmula nem custo de fita.
-/
namespace Codex.QuantizacaoBeta

open TGLExt TGLExt.TraducaoTuring Codex.LeituraBeta

theorem normalizedSum_nonneg {n : ℕ} (c : TGLCoupling) (k : ℕ) (φ : CNF n) :
    0 ≤ normalizedSum c k φ := by
  unfold normalizedSum weightedSum
  apply div_nonneg
  · exact Finset.sum_nonneg (fun x _ => pow_nonneg (sub_nonneg.mpr c.beta_lt_one.le) _)
  · positivity

theorem normalizedSum_le_one {n : ℕ} (c : TGLCoupling) (k : ℕ) (φ : CNF n) :
    normalizedSum c k φ ≤ 1 := by
  unfold normalizedSum
  apply (div_le_one (pow_pos (by norm_num : (0 : ℝ) < 2) n)).mpr
  unfold weightedSum
  calc
    _ ≤ ∑ _x : Fin n → Bool, (1 : ℝ) := by
      apply Finset.sum_le_sum
      intro x _
      exact pow_le_one₀ (sub_nonneg.mpr c.beta_lt_one.le) (by linarith [c.beta_pos])
    _ = (2 : ℝ) ^ n := by simp

theorem exists_bounded_dyadic (n : ℕ) (y : ℝ) (hy0 : 0 ≤ y) (hy1 : y ≤ 1) :
    ∃ j : ℕ, j ≤ 2 ^ (n + 2) ∧
      |(j : ℝ) / (2 : ℝ) ^ (n + 2) - y| ≤ 1 / (4 * (2 : ℝ) ^ n) := by
  let D : ℝ := (2 : ℝ) ^ (n + 2)
  let j : ℕ := Nat.floor (y * D)
  have hp : 0 < D := pow_pos (by norm_num) _
  have hjfloor : (j : ℝ) ≤ y * D := Nat.floor_le (mul_nonneg hy0 hp.le)
  have hjupper : y * D < (j : ℝ) + 1 := Nat.lt_floor_add_one (y * D)
  have hjbound : (j : ℝ) ≤ D := le_trans hjfloor (mul_le_of_le_one_left hp.le hy1)
  have hd : D = 4 * (2 : ℝ) ^ n := by dsimp [D]; rw [pow_add]; norm_num; ring
  refine ⟨j, ?_, ?_⟩
  · change (j : ℝ) ≤ (2 : ℝ) ^ (n + 2) at hjbound
    exact_mod_cast hjbound
  · change |(j : ℝ) / D - y| ≤ 1 / (4 * (2 : ℝ) ^ n)
    rw [← hd]
    have hneg : (j : ℝ) / D - y ≤ 0 := sub_nonpos.mpr ((div_le_iff₀ hp).mpr hjfloor)
    rw [abs_of_nonpos hneg]
    apply (le_div_iff₀ hp).mpr
    have heq : -((j : ℝ) / D - y) * D = y * D - (j : ℝ) := by field_simp; ring
    rw [heq]
    linarith

/-- A precisão suficiente pode ser representada por um numerador limitado.
Não afirma que o piso do real possa ser obtido em tempo polinomial. -/
theorem normalizedSum_has_bounded_dyadic {n : ℕ} (c : TGLCoupling) (k : ℕ) (φ : CNF n) :
    ∃ j : ℕ, j ≤ 2 ^ (n + 2) ∧
      |(j : ℝ) / (2 : ℝ) ^ (n + 2) - normalizedSum c k φ| ≤ 1 / (4 * (2 : ℝ) ^ n) :=
  exists_bounded_dyadic n (normalizedSum c k φ)
    (normalizedSum_nonneg c k φ) (normalizedSum_le_one c k φ)

end Codex.QuantizacaoBeta
