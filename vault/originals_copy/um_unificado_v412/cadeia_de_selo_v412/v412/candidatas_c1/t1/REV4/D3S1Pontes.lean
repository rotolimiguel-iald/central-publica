import T1PontesAoKernel

/-! SONDA S1 do revisor D3 (terceira conferencia, 16/11): o que AINDA nao e' termo depois do conserto e sai em poucas
linhas. Nada instalado; sonda de leitura.
(Q1) o fixo de UMA media na forma `x = E x`, com o objeto do kernel (a forma de `sigma_fixed_iff_specExpect`).
(Q2) com niveis nao negativos, a `esperanca` e' a `TGLExt.specExpect` nos NIVEIS.
(Q3) a conjugacao pelas fases e' o `TGLExt.sigma` do kernel no estado diagonal de pesos `e^{√k}`.
(Q4) a media gaussiana do fluxo modular do kernel e' o dephasing do kernel (pesos positivos quaisquer).
(Q5) o composto num termo so' na forma dos NIVEIS (a frase em lingua simples). -/

set_option autoImplicit false
noncomputable section

namespace D3.S1

open MeasureTheory ProbabilityTheory Matrix Polynomial Filter
open scoped NNReal Topology ComplexOrder
open K07.T1 TGLExt.T1CompostoFinito ChatgptAudit

section geral

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- (Q1) fixo de UMA media de variancia nao nula = ponto fixo da projecao -/
theorem fixo_sse_esperanca (k : n → ℝ) {v : ℝ≥0} (hv : v ≠ 0) (x : Matrix n n ℂ) :
    mediaGaussiana k v x = x ↔ x = esperanca k x := by
  rw [fixo_da_media_sse_comuta k hv x]
  constructor
  · intro h
    exact (esperanca_fixa_o_comutante k x h).symm
  · intro h
    rw [h]
    exact esperanca_cai_no_comutante k x

/-- (Q5a) todo polinomio na matriz dos NIVEIS e' fixo (sem hipotese sobre o sinal dos niveis) -/
theorem polinomio_nivel_e_fixo (k : n → ℝ) (v : ℝ≥0) (p : Polynomial ℂ) :
    mediaGaussiana k v (aeval (Matrix.diagonal (fun i => ((k i : ℝ) : ℂ))) p) =
      aeval (Matrix.diagonal (fun i => ((k i : ℝ) : ℂ))) p := by
  rw [aeval_diagonal]
  ext i j
  rw [media_entrada]
  by_cases hij : i = j
  · subst hij
    simp [mult]
  · simp [Matrix.diagonal_apply_ne _ hij]

/-- (Q5b) O COMPOSTO NUM TERMO SO', NOS NIVEIS: niveis nao negativos e distintos, variancia nao nula:
fixo = polinomio na matriz dos niveis -/
theorem fixo_sse_polinomio_nivel (k : n → ℝ) (hk : ∀ i, 0 ≤ k i) {v : ℝ≥0} (hv : v ≠ 0)
    (hinj : Function.Injective k) (x : Matrix n n ℂ) :
    mediaGaussiana k v x = x ↔
      ∃ p : Polynomial ℂ, aeval (Matrix.diagonal (fun i => ((k i : ℝ) : ℂ))) p = x := by
  constructor
  · exact (o_fixo_e_gerado_pelo_nivel_sse k hk hv).mpr hinj x
  · rintro ⟨p, rfl⟩
    exact polinomio_nivel_e_fixo k v p

end geral

section kernel

variable {m : Type} [Fintype m] [DecidableEq m]

/-- (Q1') a mesma, com o objeto do kernel -/
theorem fixo_sse_specExpect (k : m → ℝ) {v : ℝ≥0} (hv : v ≠ 0) (x : Matrix m m ℂ) :
    mediaGaussiana k v x = x ↔ x = TGLExt.specExpect (fun i => Real.sqrt (k i)) x := by
  rw [← esperanca_e_specExpect]
  exact fixo_sse_esperanca k hv x

omit [Fintype m] [DecidableEq m] in
/-- (Q2) com niveis nao negativos, a `esperanca` e' a secao espectral do kernel nos NIVEIS -/
theorem esperanca_e_specExpect_nivel (k : m → ℝ) (hk : ∀ i, 0 ≤ k i) (x : Matrix m m ℂ) :
    esperanca k x = TGLExt.specExpect k x := by
  ext i j
  by_cases h : k i = k j
  · simp [esperanca, h]
  · have hs : Real.sqrt (k i) ≠ Real.sqrt (k j) :=
      fun hs => h ((Real.sqrt_inj (hk i) (hk j)).mp hs)
    simp [esperanca, h, hs]

/-- (Q3) a conjugacao pelas fases E' o fluxo modular do kernel no estado diagonal de pesos `e^{√k}` -/
theorem conjugacao_e_sigma (k : m → ℝ) (s : ℝ) (x : Matrix m m ℂ) :
    phaseMatrix k s * x * (phaseMatrix k s).conjTranspose =
      TGLExt.sigma (TGLExt.rhoD (fun i => Real.exp (Real.sqrt (k i)))) s x := by
  ext i j
  rw [phaseMatrix_conjugation_entry,
    TGLExt.sigma_diagonal_apply _ (fun i => Real.exp_pos _) s x i j]
  congr 1
  unfold modularPhase
  congr 1
  simp only [Real.log_exp]
  push_cast
  ring

/-- (Q4) A MEDIA GAUSSIANA DO FLUXO MODULAR DO KERNEL E' O DEPHASING DO KERNEL, para pesos positivos quaisquer:
a taxa e' metade do quadrado da diferenca dos logaritmos -/
theorem media_gaussiana_do_sigma_e_dephase (d : m → ℝ) (hd : ∀ i, 0 < d i) (v : ℝ≥0)
    (x : Matrix m m ℂ) (i j : m) :
    ∫ s : ℝ, TGLExt.sigma (TGLExt.rhoD d) s x i j ∂gaussianReal 0 v =
      TGLExt.dephase (fun i j => (Real.log (d i) - Real.log (d j)) ^ 2 / 2) (v : ℝ) x i j := by
  have hpt : ∀ s : ℝ, TGLExt.sigma (TGLExt.rhoD d) s x i j =
      modularPhase s (Real.log (d i) - Real.log (d j)) * x i j := by
    intro s
    rw [TGLExt.sigma_diagonal_apply d hd s x i j]
    congr 1
    unfold modularPhase
    congr 1
    push_cast
    ring
  simp only [hpt, integral_mul_const, gaussian_phase_integral, TGLExt.dephase, Matrix.of_apply]
  congr 3
  ring

/-- (Q7) A T1 FINITA NA LINGUA DO KERNEL: ser fixo por UMA media gaussiana (variancia nao nula) e' ser fixo por TODO o
fluxo modular do estado diagonal de pesos `e^{√k}`. Usa a estrela do kernel `sigma_fixed_iff_specExpect`. -/
theorem fixo_da_media_sse_fixo_do_fluxo (k : m → ℝ) {v : ℝ≥0} (hv : v ≠ 0) (x : Matrix m m ℂ) :
    mediaGaussiana k v x = x ↔
      ∀ t : ℝ, TGLExt.sigma (TGLExt.rhoD (fun i => Real.exp (Real.sqrt (k i)))) t x = x := by
  rw [fixo_sse_specExpect k hv x,
    TGLExt.sigma_fixed_iff_specExpect (fun i => Real.exp (Real.sqrt (k i))) (fun i => Real.exp_pos _) x]
  have h : TGLExt.specExpect (fun i => Real.exp (Real.sqrt (k i))) x =
      TGLExt.specExpect (fun i => Real.sqrt (k i)) x := by
    ext i j
    simp [Real.exp_eq_exp]
  rw [h]

/-- (Q8) a matriz das frequencias e' o GERADOR MODULAR `log ρ` do kernel, para o estado de pesos `e^{√k}`
(e nao o estado `rhoD` de pesos `√k`, que e' so' a mesma matriz com outro papel) -/
theorem frequencias_e_logRho (k : m → ℝ) :
    Matrix.diagonal (freq k) =
      TGLExt.logRho (TGLExt.rhoD (fun i => Real.exp (Real.sqrt (k i)))) := by
  rw [TGLExt.logRho_diagonal _ (fun i => Real.exp_pos _)]
  simp only [Real.log_exp]
  rfl

omit [Fintype m] in
/-- (Q6') no espectro simples a positividade sai do kernel (`diagExpect_posSemidef`) -/
theorem esperanca_positiva_pelo_kernel (k : m → ℝ) (hinj : Function.Injective (freq k))
    {x : Matrix m m ℂ} (hx : x.PosSemidef) : (esperanca k x).PosSemidef := by
  rw [esperanca_e_diagExpect k hinj x]
  exact TGLExt.diagExpect_posSemidef hx

end kernel

section positividade

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- (Q6) a projecao e' POSITIVA tambem com frequencias repetidas: `E(x) = Σ_λ P_λ x P_λ`, com `P_λ` a projecao
diagonal do conjunto de nivel da frequencia `λ` -/
theorem esperanca_posSemidef (k : n → ℝ) {x : Matrix n n ℂ} (hx : x.PosSemidef) :
    (esperanca k x).PosSemidef := by
  classical
  let P : ℝ → Matrix n n ℂ := fun l =>
    Matrix.diagonal (fun i => if Real.sqrt (k i) = l then (1 : ℂ) else 0)
  have hterm : ∀ (l : ℝ) (i j : n), ((P l)ᴴ * x * P l) i j =
      (if Real.sqrt (k i) = l then (1 : ℂ) else 0) * x i j *
        (if Real.sqrt (k j) = l then (1 : ℂ) else 0) := by
    intro l i j
    simp only [P, Matrix.diagonal_conjTranspose, Matrix.diagonal_mul, Matrix.mul_diagonal,
      Pi.star_apply]
    split_ifs <;> simp
  have hsum : esperanca k x =
      ∑ l ∈ Finset.univ.image (fun i => Real.sqrt (k i)), (P l)ᴴ * x * P l := by
    ext i j
    rw [Matrix.sum_apply]
    simp only [hterm]
    rw [Finset.sum_eq_single (Real.sqrt (k i))]
    · by_cases hij : Real.sqrt (k i) = Real.sqrt (k j)
      · simp [esperanca, hij]
      · have hji : ¬ Real.sqrt (k j) = Real.sqrt (k i) := fun h => hij h.symm
        simp [esperanca, hij, hji]
    · intro l _ hl
      have hl' : ¬ Real.sqrt (k i) = l := fun h => hl h.symm
      simp [hl']
    · intro h
      exact absurd (Finset.mem_image_of_mem _ (Finset.mem_univ i)) h
  rw [hsum]
  exact Matrix.posSemidef_sum _ (fun l _ => hx.conjTranspose_mul_mul_same (P l))

end positividade

#print axioms fixo_da_media_sse_fixo_do_fluxo
#print axioms frequencias_e_logRho
#print axioms esperanca_positiva_pelo_kernel
#print axioms esperanca_posSemidef
#print axioms fixo_sse_esperanca
#print axioms polinomio_nivel_e_fixo
#print axioms fixo_sse_polinomio_nivel
#print axioms fixo_sse_specExpect
#print axioms esperanca_e_specExpect_nivel
#print axioms conjugacao_e_sigma
#print axioms media_gaussiana_do_sigma_e_dephase

end D3.S1
