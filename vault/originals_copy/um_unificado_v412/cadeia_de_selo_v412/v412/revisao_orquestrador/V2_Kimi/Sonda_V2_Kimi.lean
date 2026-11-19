import TGLExt.Ergodicity

set_option autoImplicit false

/-!
# Sonda V2 (controle negativo) — revisor Kimi, ORDEM 022, unidade V2

Dois controles negativos sobre `OParFixaORelogio.lean` (REV25, sha16 267019b19fb5a22c):

* SONDA A: nenhuma matriz diagonal distingue dois relógios. A sonda `uns` (todas as entradas 1) de
  `o_mesmo_relogio_da_as_mesmas_razoes` é necessária: quem lê só a diagonal é cego ao fluxo.
* SONDA B: um único instante NÃO basta. Há `t > 0` e pesos normalizados NÃO proporcionais cujos
  fluxos coincidem em `t` para toda matriz — o «em todo tempo» dos teoremas `o_par_fixa_o_relogio`
  e `dois_estados_com_o_mesmo_relogio_sao_o_mesmo_estado` é essencial (periodicidade das fases).

Sem sorry. Só leitura do kernel já selado (`TGLExt.sigma_diagonal_apply`).
-/

namespace TGLExt.SondaV2Kimi

open TGLExt Matrix

variable {n : Type} [Fintype n] [DecidableEq n]

/-- SONDA A (cegueira da diagonal): para `x` diagonal, quaisquer dois estados diagonais dão o mesmo
fluxo. Logo a leitura fora da diagonal (a sonda `uns`) é necessária para comparar relógios. -/
theorem sonda_diagonal_cega (d d' : n → ℝ) (hd : ∀ i, 0 < d i) (hd' : ∀ i, 0 < d' i)
    (f : n → ℂ) (t : ℝ) :
    sigma (rhoD d) t (diagonal f) = sigma (rhoD d') t (diagonal f) := by
  ext i j
  rw [sigma_diagonal_apply d hd, sigma_diagonal_apply d' hd']
  by_cases hij : i = j
  · subst hij
    simp
  · simp [hij]

/-- SONDA B (um instante não basta): existem `t > 0` e pesos normalizados não proporcionais cujos
fluxos coincidem em `t` para toda matriz. Controle negativo do quantificador «para todo tempo». -/
theorem sonda_um_instante_nao_basta :
    ∃ t : ℝ, 0 < t ∧ ∃ d d' : Fin 2 → ℝ, (∀ i, 0 < d i) ∧ (∀ i, 0 < d' i) ∧
      ∑ i, d i = 1 ∧ ∑ i, d' i = 1 ∧ ¬ (∃ c : ℝ, ∀ i, d' i = c * d i) ∧
      ∀ x : Matrix (Fin 2) (Fin 2) ℂ, sigma (rhoD d) t x = sigma (rhoD d') t x := by
  have hL : (0 : ℝ) < Real.log 2 := Real.log_pos (by norm_num)
  have hLC : ((Real.log 2 : ℝ) : ℂ) ≠ 0 := by exact_mod_cast hL.ne'
  have hd : ∀ i : Fin 2, 0 < (fun _ : Fin 2 => (1 / 2 : ℝ)) i := fun _ => by norm_num
  have hd' : ∀ i : Fin 2, 0 < (![1 / 3, 2 / 3] : Fin 2 → ℝ) i :=
    Fin.forall_fin_two.mpr ⟨by norm_num, by norm_num⟩
  have hlog : Real.log (1 / 3 : ℝ) - Real.log (2 / 3 : ℝ) = -Real.log 2 := by
    rw [Real.log_div (by norm_num) (by norm_num), Real.log_div (by norm_num) (by norm_num),
      Real.log_one, zero_sub]
    ring
  have hlog' : Real.log (2 / 3 : ℝ) - Real.log (1 / 3 : ℝ) = Real.log 2 := by
    rw [Real.log_div (by norm_num) (by norm_num), Real.log_div (by norm_num) (by norm_num),
      Real.log_one, zero_sub]
    ring
  have hexp_neg : Complex.exp (-(2 * (Real.pi : ℂ) * Complex.I)) = 1 := by
    rw [Complex.exp_neg, Complex.exp_two_pi_mul_I, inv_one]
  have hphase : ∀ i j : Fin 2,
      Complex.exp (((2 * Real.pi / Real.log 2 : ℝ) : ℂ) * Complex.I *
          ((Real.log (![1 / 3, 2 / 3] i) : ℂ) - (Real.log (![1 / 3, 2 / 3] j) : ℂ))) = 1 := by
    refine Fin.forall_fin_two.mpr ⟨?_, ?_⟩ <;> refine Fin.forall_fin_two.mpr ⟨?_, ?_⟩
    · simp
    · simp only [Matrix.cons_val_zero, Matrix.cons_val_one]
      rw [← Complex.ofReal_sub, hlog, Complex.ofReal_neg]
      rw [show ((2 * Real.pi / Real.log 2 : ℝ) : ℂ) * Complex.I * (-(Real.log 2 : ℂ))
          = -(2 * (Real.pi : ℂ) * Complex.I) by
        push_cast
        field_simp [hLC]]
      exact hexp_neg
    · simp only [Matrix.cons_val_zero, Matrix.cons_val_one]
      rw [← Complex.ofReal_sub, hlog']
      rw [show ((2 * Real.pi / Real.log 2 : ℝ) : ℂ) * Complex.I * ((Real.log 2 : ℂ))
          = 2 * (Real.pi : ℂ) * Complex.I by
        push_cast
        field_simp [hLC]]
      exact Complex.exp_two_pi_mul_I
    · simp
  refine ⟨2 * Real.pi / Real.log 2, div_pos (mul_pos two_pos Real.pi_pos) hL,
    (fun _ : Fin 2 => (1 / 2 : ℝ)), ![1 / 3, 2 / 3], hd, hd', ?_, ?_, ?_, ?_⟩
  · rw [Fin.sum_univ_two]
    show (1 / 2 : ℝ) + 1 / 2 = 1
    norm_num
  · rw [Fin.sum_univ_two]
    norm_num
  · rintro ⟨c, hc⟩
    have h0 := hc 0
    have h1 := hc 1
    simp only [Matrix.cons_val_zero, Matrix.cons_val_one] at h0 h1
    linarith
  · intro x
    have hxid : sigma (rhoD (fun _ : Fin 2 => (1 / 2 : ℝ))) (2 * Real.pi / Real.log 2) x = x := by
      ext i j
      rw [sigma_diagonal_apply _ hd]
      simp
    have hxx : sigma (rhoD (![1 / 3, 2 / 3] : Fin 2 → ℝ)) (2 * Real.pi / Real.log 2) x = x := by
      ext i j
      rw [sigma_diagonal_apply _ hd']
      rw [hphase i j, one_mul]
    rw [hxid, hxx]

end TGLExt.SondaV2Kimi

#print axioms TGLExt.SondaV2Kimi.sonda_diagonal_cega
#print axioms TGLExt.SondaV2Kimi.sonda_um_instante_nao_basta
