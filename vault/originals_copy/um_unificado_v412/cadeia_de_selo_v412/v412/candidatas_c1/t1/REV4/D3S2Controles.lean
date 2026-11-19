import T1PontesAoKernel

/-! SONDA S2 do revisor D3 (terceira conferencia, 16/11): onde mora cada objeto do kernel usado pelas pontes; e os
controles da hipotese `k ≥ 0` na ponte das frequencias para os niveis. Nada instalado; sonda de leitura. -/

set_option autoImplicit false
noncomputable section

namespace D3.S2

open MeasureTheory ProbabilityTheory Matrix Polynomial Filter
open scoped NNReal Topology
open K07.T1 TGLExt.T1CompostoFinito

/-! ## (R1) o modulo em que cada constante do kernel e' declarada -/

open Lean Elab Command in
#eval show CommandElabM Unit from do
  let env ← getEnv
  for c in [``TGLExt.dephase, ``TGLExt.dephase_add, ``TGLExt.dephase_zero, ``TGLExt.dephase_tendsto_expectation,
      ``TGLExt.rhoD, ``TGLExt.specExpect, ``TGLExt.specExpect_idem, ``TGLExt.specExpect_one,
      ``TGLExt.rhoD_commute_specExpect, ``TGLExt.specExpect_of_injective, ``TGLExt.sigma_fixed_iff_specExpect,
      ``TGLExt.diagExpect, ``TGLExt.diagExpect_posSemidef, ``TGLExt.diagExpect_bimod, ``TGLExt.trace_diagExpect,
      ``TGLExt.dephase_fixed_iff_diagonal, ``TGLExt.birkhoff_tendsto_specExpect, ``TGLExt.sigma,
      ``TGLExt.sigma_fixed_iff_diag, ``ChatgptAudit.modularPhase] do
    match env.getModuleIdxFor? c with
    | some idx => logInfo m!"MODULO {c} : {env.header.moduleNames[idx.toNat]!}"
    | none => logInfo m!"MODULO {c} : (este arquivo)"

#check @TGLExt.dephase
#check @TGLExt.rhoD
#check @TGLExt.specExpect
#check @TGLExt.diagExpect
#check @TGLExt.dephase_add
#check @TGLExt.specExpect_idem
#check @TGLExt.rhoD_commute_specExpect
#check @TGLExt.dephase_tendsto_expectation
#check @TGLExt.dephase_fixed_iff_diagonal
#check @TGLExt.sigma_fixed_iff_specExpect
#check @TGLExt.birkhoff_tendsto_specExpect

/-! ## (R2) os enunciados das pontes, como o Lean os le -/

#check @media_e_dephase
#check @esperanca_e_specExpect
#check @gerador_e_rhoD
#check @esperanca_e_diagExpect
#check @media_tende_pelo_kernel
#check @comuta_freq_sse_comuta_nivel
#check @fixo_da_media_sse_comuta_nivel
#check @o_fixo_e_gerado_pelo_nivel_sse
#check @fixo_sse_polinomio
#check @polinomio_e_fixo

/-! ## (R3) controles: sem `k ≥ 0` a ponte para os niveis e' FALSA -/

/-- niveis negativos distintos: frequencias todas nulas -/
def kNeg : Fin 2 → ℝ := ![-1, -2]

theorem kNeg_injetiva : Function.Injective kNeg := by
  intro i j h
  fin_cases i <;> fin_cases j <;> simp [kNeg] at h ⊢

theorem freq_kNeg (i : Fin 2) : Real.sqrt (kNeg i) = 0 := by
  apply Real.sqrt_eq_zero_of_nonpos
  fin_cases i <;> simp [kNeg]

/-- com niveis negativos TUDO comuta com a matriz das frequencias -/
theorem tudo_comuta_freq_kNeg (x : Matrix (Fin 2) (Fin 2) ℂ) :
    Commute (Matrix.diagonal (freq kNeg)) x := by
  rw [comuta_sse_entradas]
  intro i j hij
  exact absurd (by rw [freq_kNeg i, freq_kNeg j]) hij

/-- e tudo e' fixo por toda media, de qualquer variancia -/
theorem tudo_fixo_kNeg (v : ℝ≥0) (x : Matrix (Fin 2) (Fin 2) ℂ) : mediaGaussiana kNeg v x = x := by
  ext i j
  rw [media_entrada]
  simp [mult, freq_kNeg]

/-- a matriz `E₀₁` NAO comuta com a matriz dos niveis: a ponte `comuta_freq_sse_comuta_nivel` falha sem `k ≥ 0` -/
theorem ponte_falha_sem_hk :
    ¬ (∀ x : Matrix (Fin 2) (Fin 2) ℂ, Commute (Matrix.diagonal (freq kNeg)) x ↔
        Commute (Matrix.diagonal (fun i => ((kNeg i : ℝ) : ℂ))) x) := by
  intro h
  have hc := (h (Matrix.single 0 1 1)).mp (tudo_comuta_freq_kNeg _)
  rw [comuta_diag_sse] at hc
  have h01 := hc 0 1 (by simp [kNeg])
  simp at h01

/-- e `o_fixo_e_gerado_pelo_nivel_sse` falha sem `k ≥ 0`: niveis distintos, e ha' fixo que nao e' polinomio -/
theorem gerado_pelo_nivel_falha_sem_hk (v : ℝ≥0) :
    Function.Injective kNeg ∧
      ¬ (∀ x : Matrix (Fin 2) (Fin 2) ℂ, mediaGaussiana kNeg v x = x →
          ∃ p : Polynomial ℂ, aeval (Matrix.diagonal (fun i => ((kNeg i : ℝ) : ℂ))) p = x) := by
  refine ⟨kNeg_injetiva, fun h => ?_⟩
  obtain ⟨p, hp⟩ := h (Matrix.single 0 1 1) (tudo_fixo_kNeg v _)
  rw [aeval_diagonal] at hp
  have bad := congrArg (fun a : Matrix (Fin 2) (Fin 2) ℂ => a 0 1) hp
  simp at bad

/-! ## (R4) controle da variancia: com `v = 0` a media e' a identidade (nada e' atenuado) -/

theorem media_zero {n : Type*} [Fintype n] [DecidableEq n] (k : n → ℝ) (x : Matrix n n ℂ) :
    mediaGaussiana k 0 x = x := by
  ext i j
  rw [media_entrada]
  simp [mult]

/-- para `v ≠ 0` e frequencias diferentes o multiplicador e' ESTRITAMENTE menor que 1 e positivo: atenua, nao apaga -/
theorem mult_atenua {n : Type*} (k : n → ℝ) {v : ℝ≥0} (hv : v ≠ 0) (i j : n)
    (hij : Real.sqrt (k i) ≠ Real.sqrt (k j)) : 0 < mult k v i j ∧ mult k v i j < 1 := by
  have hv' : (0 : ℝ) < v := by exact_mod_cast pos_iff_ne_zero.mpr hv
  have hne : Real.sqrt (k i) - Real.sqrt (k j) ≠ 0 := sub_ne_zero.mpr hij
  have hsq : 0 < (Real.sqrt (k i) - Real.sqrt (k j)) ^ 2 := by positivity
  refine ⟨Real.exp_pos _, ?_⟩
  unfold mult
  have hpos : 0 < (v : ℝ) * (Real.sqrt (k i) - Real.sqrt (k j)) ^ 2 := mul_pos hv' hsq
  exact Real.exp_lt_one_iff.mpr (by linarith)

#print axioms ponte_falha_sem_hk
#print axioms gerado_pelo_nivel_falha_sem_hk
#print axioms tudo_fixo_kNeg
#print axioms media_zero
#print axioms mult_atenua

end D3.S2
