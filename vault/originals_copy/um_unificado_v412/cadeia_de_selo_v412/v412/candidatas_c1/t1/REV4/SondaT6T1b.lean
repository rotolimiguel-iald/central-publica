import T1PontesAoKernel

/-! Sonda T6-b (revisor da conferencia de conserto, 16/11/2026). Nada instalado.
A ponte de entrada escolhe o estado de pesos `e^{+√k}` (o que pesa MAIS os niveis altos). Com os pesos `e^{-√k}`
(o que pesa mais os niveis baixos) o fluxo e' o mesmo com o tempo invertido; o que fica parado nao muda. -/

set_option autoImplicit false
noncomputable section
namespace SondaT6T1b

open MeasureTheory ProbabilityTheory Matrix Polynomial Filter
open scoped NNReal Topology ComplexOrder
open K07.T1 TGLExt.T1CompostoFinito ChatgptAudit

variable {m : Type} [Fintype m] [DecidableEq m]

/-- O sinal dos pesos e' a inversao do tempo: o fluxo do estado de pesos `e^{-√k}` no tempo `t` e' o do estado de
pesos `e^{√k}` no tempo `-t`. -/
theorem sinal_dos_pesos_e_inversao_do_tempo (k : m → ℝ) (t : ℝ) (x : Matrix m m ℂ) :
    TGLExt.sigma (TGLExt.rhoD (fun i => Real.exp (-Real.sqrt (k i)))) t x =
      TGLExt.sigma (TGLExt.rhoD (fun i => Real.exp (Real.sqrt (k i)))) (-t) x := by
  ext i j
  rw [TGLExt.sigma_diagonal_apply _ (fun i => Real.exp_pos _) t x i j,
    TGLExt.sigma_diagonal_apply _ (fun i => Real.exp_pos _) (-t) x i j]
  simp only [Real.log_exp]
  congr 2
  push_cast
  ring

/-- Logo o fixo de UMA media gaussiana e' tambem o fixo de TODO o fluxo do estado de pesos `e^{-√k}`. -/
theorem fixo_da_media_sse_fixo_do_fluxo_pesos_decrescentes (k : m → ℝ) {v : ℝ≥0} (hv : v ≠ 0)
    (x : Matrix m m ℂ) :
    mediaGaussiana k v x = x ↔
      ∀ t : ℝ, TGLExt.sigma (TGLExt.rhoD (fun i => Real.exp (-Real.sqrt (k i)))) t x = x := by
  rw [fixo_da_media_sse_fixo_do_fluxo k hv x]
  constructor
  · intro h t
    rw [sinal_dos_pesos_e_inversao_do_tempo]
    exact h (-t)
  · intro h t
    have := h (-t)
    rw [sinal_dos_pesos_e_inversao_do_tempo, neg_neg] at this
    exact this

#print axioms sinal_dos_pesos_e_inversao_do_tempo
#print axioms fixo_da_media_sse_fixo_do_fluxo_pesos_decrescentes

end SondaT6T1b
