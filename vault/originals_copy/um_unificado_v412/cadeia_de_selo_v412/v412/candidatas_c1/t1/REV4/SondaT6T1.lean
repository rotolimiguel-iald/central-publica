import T1PontesAoKernel

/-! Sonda T6 (revisor da conferencia de conserto, 16/11/2026). So' leitura do kernel e das candidatas; nada instalado.
(1) o modulo em que mora cada constante do kernel e do Codex usada pelos doze termos novos da R2;
(2) a ponte de entrada sobre a PROPRIA definicao: a media gaussiana da candidata e' a media gaussiana do `sigma`;
(3) as duas pontes (entrada e saida) fecham uma na outra;
(4) repeticoes nao ditas: a positividade pelo kernel e' caso da geral; a unidade sai do kernel;
(5) nao vacuidade: ha' matriz que NAO e' fixa (frequencias diferentes) e matriz fixa. -/

set_option autoImplicit false
noncomputable section
namespace SondaT6T1

open MeasureTheory ProbabilityTheory Matrix Polynomial Filter
open scoped NNReal Topology ComplexOrder
open K07.T1 TGLExt.T1CompostoFinito ChatgptAudit

/-! ## (1) onde mora cada constante -/

open Lean Elab Command in
#eval show CommandElabM Unit from do
  let env ← getEnv
  for c in [``TGLExt.sigma, ``TGLExt.logRho, ``TGLExt.rhoD, ``TGLExt.dephase, ``TGLExt.dephase_zero,
      ``TGLExt.specExpect, ``TGLExt.diagExpect, ``TGLExt.sigma_fixed_iff_specExpect, ``TGLExt.sigma_diagonal_apply,
      ``TGLExt.logRho_diagonal, ``TGLExt.diagExpect_posSemidef, ``TGLExt.modularGap, ``ChatgptAudit.modularPhase,
      ``K07.T1.gaussian_phase_integral, ``K07.T1.phaseMatrix_conjugation_entry, ``K07.T1.phaseMatrix,
      ``K07.T1.aeval_diagonal, ``K07.T1.commutant_generated_iff_injective] do
    match env.getModuleIdxFor? c with
    | some idx => logInfo m!"MODULO {c} : {env.header.moduleNames[idx.toNat]!}"
    | none => logInfo m!"MODULO {c} : (este arquivo)"

#check @TGLExt.sigma
#check @TGLExt.logRho
#check @TGLExt.sigma_fixed_iff_specExpect
#check @conjugacao_e_sigma
#check @frequencias_e_logRho
#check @media_gaussiana_do_sigma_e_dephase
#check @fixo_da_media_sse_fixo_do_fluxo
#check @esperanca_posSemidef
#check @fixo_sse_polinomio_nivel
#check @media_zero
#check @K07.T1.phaseMatrix

section kernel

variable {m : Type} [Fintype m] [DecidableEq m]

/-! ## (2) a ponte de entrada sobre a propria definicao -/

/-- A media gaussiana DA CANDIDATA e', entrada a entrada, a media gaussiana do fluxo modular do kernel no estado
diagonal de pesos `e^{√k}`. (As tres pontes da R2 dao isto em dois passos; aqui num termo so'.) -/
theorem media_e_a_media_do_sigma (k : m → ℝ) (v : ℝ≥0) (x : Matrix m m ℂ) (i j : m) :
    mediaGaussiana k v x i j =
      ∫ s : ℝ, TGLExt.sigma (TGLExt.rhoD (fun i => Real.exp (Real.sqrt (k i)))) s x i j ∂gaussianReal 0 v := by
  unfold mediaGaussiana
  rw [Matrix.of_apply]
  simp only [conjugacao_e_sigma]

/-! ## (3) entrada e saida fecham -/

/-- A taxa que sai da ponte de entrada (metade do quadrado da diferenca dos logaritmos dos pesos `e^{√k}`) e' a da
ponte de saida (`media_e_dephase`). -/
theorem as_duas_pontes_fecham (k : m → ℝ) (v : ℝ≥0) (x : Matrix m m ℂ) (i j : m) :
    TGLExt.dephase (fun i j => (Real.log (Real.exp (Real.sqrt (k i))) -
        Real.log (Real.exp (Real.sqrt (k j)))) ^ 2 / 2) (v : ℝ) x i j =
      TGLExt.dephase (fun i j => (Real.sqrt (k i) - Real.sqrt (k j)) ^ 2 / 2) (v : ℝ) x i j := by
  rw [← media_gaussiana_do_sigma_e_dephase (fun i => Real.exp (Real.sqrt (k i))) (fun i => Real.exp_pos _) v x i j,
    ← media_e_a_media_do_sigma, media_e_dephase]

/-! ## (4) repeticoes nao ditas no cabecalho -/

/-- `esperanca_positiva_pelo_kernel` tem a conclusao de `esperanca_posSemidef` com uma hipotese a mais. -/
theorem positiva_pelo_kernel_e_caso_da_geral (k : m → ℝ) (_hinj : Function.Injective (freq k))
    {x : Matrix m m ℂ} (hx : x.PosSemidef) : (esperanca k x).PosSemidef :=
  esperanca_posSemidef k hx

/-- `media_zero` sai do kernel (`dephase_zero`) pela ponte de saida. -/
theorem media_zero_pelo_kernel (k : m → ℝ) (x : Matrix m m ℂ) : mediaGaussiana k 0 x = x := by
  rw [media_e_dephase, NNReal.coe_zero, TGLExt.dephase_zero]

/-- `fixo_sse_specExpect` e' `fixo_sse_esperanca` reescrito por `esperanca_e_specExpect`. -/
theorem fixo_sse_specExpect_e_reescrita (k : m → ℝ) {v : ℝ≥0} (hv : v ≠ 0) (x : Matrix m m ℂ) :
    (mediaGaussiana k v x = x ↔ x = TGLExt.specExpect (fun i => Real.sqrt (k i)) x) ↔
      (mediaGaussiana k v x = x ↔ x = esperanca k x) := by
  rw [esperanca_e_specExpect]

end kernel

/-! ## (5) nao vacuidade em `Fin 2` -/

/-- niveis 0 e 1: frequencias 0 e 1, distintas -/
def k01 : Fin 2 → ℝ := ![0, 1]

theorem freq01_distintas : Real.sqrt (k01 0) ≠ Real.sqrt (k01 1) := by
  simp [k01]

/-- a unidade de matriz `E₀₁` NAO e' fixa pela media de variancia 1 -/
theorem ha_quem_nao_e_fixo :
    mediaGaussiana k01 1 (Matrix.single (0 : Fin 2) (1 : Fin 2) (1 : ℂ)) ≠ Matrix.single 0 1 1 := by
  intro h
  have h01 := (fixo_sse_entradas k01 one_ne_zero _).mp h 0 1 freq01_distintas
  simp at h01

/-- e, pela ponte nova, NAO e' fixa por todo o fluxo modular do kernel -/
theorem ha_quem_o_fluxo_do_kernel_move :
    ¬ ∀ t : ℝ, TGLExt.sigma (TGLExt.rhoD (fun i => Real.exp (Real.sqrt (k01 i)))) t
        (Matrix.single (0 : Fin 2) (1 : Fin 2) (1 : ℂ)) = Matrix.single 0 1 1 :=
  fun h => ha_quem_nao_e_fixo ((fixo_da_media_sse_fixo_do_fluxo k01 one_ne_zero _).mpr h)

/-- a identidade e' fixa -/
theorem a_unidade_e_fixa : mediaGaussiana k01 1 (1 : Matrix (Fin 2) (Fin 2) ℂ) = 1 := by
  have h := polinomio_e_fixo k01 1 (Polynomial.C (1 : ℂ))
  simpa using h

#print axioms media_e_a_media_do_sigma
#print axioms as_duas_pontes_fecham
#print axioms positiva_pelo_kernel_e_caso_da_geral
#print axioms media_zero_pelo_kernel
#print axioms fixo_sse_specExpect_e_reescrita
#print axioms ha_quem_nao_e_fixo
#print axioms ha_quem_o_fluxo_do_kernel_move
#print axioms a_unidade_e_fixa

end SondaT6T1
