import TGLExt.ONomeEBeta
set_option autoImplicit false
set_option maxHeartbeats 1000000

/-!
Leitura com folga finita, condicionada a uma aproximação racional dada.
Esta pedra não implementa a aproximação nem afirma custo polinomial de obtê-la.
A folga real está demonstrada em `TGLExt.LeiturasComFolga` (`IALD.LeiturasComFolga.leitura_com_folga`). Este
módulo traz a folga real especializada ao β fixo, o comparador racional executável
e o transporte da precisão pela normalização.
-/
namespace Codex.LeituraBeta

open TGLExt TGLExt.TraducaoTuring TGLExt.AContagemEACarga TGLExt.OPassoEOFim

noncomputable def weightedSum {n : ℕ} (c : TGLCoupling) (k : ℕ) (φ : CNF n) : ℝ :=
  ∑ x : Fin n → Bool, (1 - c.beta) ^ (k * custoCNF φ x)

theorem sat_lower {n : ℕ} (c : TGLCoupling) (k : ℕ) (φ : CNF n)
    (h : SAT φ) : 1 ≤ weightedSum c k φ := by
  obtain ⟨x, hx⟩ := (sat_e_existir_custo_zero φ).mp h
  unfold weightedSum
  calc
    1 = (1 - c.beta) ^ (k * custoCNF φ x) := (o_nome_fica_inteiro φ c.beta k x hx).symm
    _ ≤ ∑ y : Fin n → Bool, (1 - c.beta) ^ (k * custoCNF φ y) := by
      exact Finset.single_le_sum (fun y _ => pow_nonneg
        (sub_nonneg.mpr c.beta_lt_one.le) (k * custoCNF φ y)) (Finset.mem_univ x)

theorem effective_time_gt (c : TGLCoupling) (n k : ℕ)
    (hk : ((n : ℝ) + 2) * Real.log 2 / c.beta < k) :
    ((n : ℝ) + 2) * Real.log 2 < (k : ℝ) * (-Real.log (1 - c.beta)) := by
  have hlog : c.beta ≤ -Real.log (1 - c.beta) := by
    have := Real.log_le_sub_one_of_pos (by linarith [c.beta_lt_one] : 0 < 1 - c.beta)
    linarith
  have hk' : ((n : ℝ) + 2) * Real.log 2 < (k : ℝ) * c.beta := by
    rwa [div_lt_iff₀ c.beta_pos] at hk
  exact lt_of_lt_of_le hk' (mul_le_mul_of_nonneg_left hlog (Nat.cast_nonneg k))

theorem unsat_upper {n : ℕ} (c : TGLCoupling) (k : ℕ) (φ : CNF n)
    (hk : ((n : ℝ) + 2) * Real.log 2 / c.beta < k) (h : ¬ SAT φ) :
    weightedSum c k φ < 1 / 4 := by
  classical
  let s : ℝ := (k : ℝ) * (-Real.log (1 - c.beta))
  have hs : ((n : ℝ) + 2) * Real.log 2 < s := effective_time_gt c n k hk
  have hs0 : 0 ≤ s := le_of_lt (lt_of_le_of_lt
    (mul_nonneg (by positivity) (Real.log_nonneg one_le_two)) hs)
  have hno : ¬ ∃ x, custoCNF φ x = 0 := fun hx => h ((sat_e_existir_custo_zero φ).mpr hx)
  have hvazio : Finset.univ.filter (fun x => custoCNF φ x = 0) = ∅ := by
    apply Finset.filter_eq_empty_iff.mpr
    intro x _ hx
    exact hno ⟨x, hx⟩
  have hsum := TGLExt.AEscala.a_flutuacao_do_fundo_e_cotada (custoCNF φ) hs0
  rw [hvazio] at hsum
  simp only [Finset.card_empty, Nat.cast_zero, zero_add] at hsum
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
  unfold weightedSum
  rw [a_soma_depois_de_k_passos φ c.beta c.beta_lt_one k]
  exact lt_of_le_of_lt hsum htail

/-- O comparador é executável; seu argumento racional não é produzido aqui. -/
def readBit (r : ℚ) : Bool := decide ((1 / 2 : ℚ) ≤ r)

theorem rational_reader_correct {n : ℕ} (c : TGLCoupling) (k : ℕ) (φ : CNF n)
    (hk : ((n : ℝ) + 2) * Real.log 2 / c.beta < k) (r : ℚ)
    (hr : |(r : ℝ) - weightedSum c k φ| ≤ 1 / 4) :
    SAT φ ↔ (1 / 2 : ℚ) ≤ r := by
  have habs := abs_le.mp hr
  constructor
  · intro hsat
    have hlower := sat_lower c k φ hsat
    have hreal : (1 / 2 : ℝ) ≤ (r : ℝ) := by linarith
    have hc : (((1 / 2 : ℚ) : ℝ)) ≤ (r : ℝ) := by norm_num at *; exact hreal
    exact Rat.cast_le.mp hc
  · intro hread
    have hcast : (((1 / 2 : ℚ) : ℝ)) ≤ (r : ℝ) := Rat.cast_le.mpr hread
    have hreal : (1 / 2 : ℝ) ≤ (r : ℝ) := by norm_num at hcast; exact hcast
    by_contra hnot
    have hupper := unsat_upper c k φ hk hnot
    linarith

theorem readBit_correct {n : ℕ} (c : TGLCoupling) (k : ℕ) (φ : CNF n)
    (hk : ((n : ℝ) + 2) * Real.log 2 / c.beta < k) (r : ℚ)
    (hr : |(r : ℝ) - weightedSum c k φ| ≤ 1 / 4) :
    readBit r = true ↔ SAT φ := by
  simpa [readBit] using (rational_reader_correct c k φ hk r hr).symm

noncomputable def normalizedSum {n : ℕ} (c : TGLCoupling) (k : ℕ) (φ : CNF n) : ℝ :=
  weightedSum c k φ / (2 : ℝ) ^ n

def normalizedReadBit (n : ℕ) (r : ℚ) : Bool := decide (1 / (2 * (2 : ℚ) ^ n) ≤ r)

theorem normalized_rational_reader_correct {n : ℕ} (c : TGLCoupling) (k : ℕ) (φ : CNF n)
    (hk : ((n : ℝ) + 2) * Real.log 2 / c.beta < k) (r : ℚ)
    (hr : |(r : ℝ) - normalizedSum c k φ| ≤ 1 / (4 * (2 : ℝ) ^ n)) :
    SAT φ ↔ 1 / (2 * (2 : ℚ) ^ n) ≤ r := by
  let D : ℝ := (2 : ℝ) ^ n
  have hp : 0 < D := pow_pos (by norm_num) n
  have hscale : |((r * (2 : ℚ) ^ n : ℚ) : ℝ) - weightedSum c k φ| ≤ 1 / 4 := by
    push_cast
    change |(r : ℝ) * D - weightedSum c k φ| ≤ 1 / 4
    have heq : (r : ℝ) * D - weightedSum c k φ =
        ((r : ℝ) - weightedSum c k φ / D) * D := by
      field_simp
    rw [heq, abs_mul, abs_of_pos hp]
    change |(r : ℝ) - weightedSum c k φ / D| ≤ 1 / (4 * D) at hr
    have hmul := mul_le_mul_of_nonneg_right hr hp.le
    have hcancel : 1 / (4 * D) * D = (1 / 4 : ℝ) := by field_simp
    rwa [hcancel] at hmul
  rw [rational_reader_correct c k φ hk (r * (2 : ℚ) ^ n) hscale]
  have hq : (0 : ℚ) < (2 : ℚ) ^ n := pow_pos (by norm_num) n
  have heq : 1 / (2 * (2 : ℚ) ^ n) = (1 / 2 : ℚ) / (2 : ℚ) ^ n := by ring
  rw [heq, div_le_iff₀ hq]

theorem normalizedReadBit_correct {n : ℕ} (c : TGLCoupling) (k : ℕ) (φ : CNF n)
    (hk : ((n : ℝ) + 2) * Real.log 2 / c.beta < k) (r : ℚ)
    (hr : |(r : ℝ) - normalizedSum c k φ| ≤ 1 / (4 * (2 : ℝ) ^ n)) :
    normalizedReadBit n r = true ↔ SAT φ := by
  simpa [normalizedReadBit] using (normalized_rational_reader_correct c k φ hk r hr).symm

end Codex.LeituraBeta
