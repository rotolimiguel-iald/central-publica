import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Algebra.Algebra.Subalgebra.Basic

/-! Revisor V_B1_a: contraexemplos compilados as hipoteses das secoes abstratas da candidata
ErgodicidadeDeMautner (enunciados COPIADOS; nada importado da candidata). So Mathlib. -/

set_option autoImplicit false
set_option maxHeartbeats 1000000

open scoped InnerProductSpace ComplexConjugate

namespace TesteV

/-! ## CE2: com peso zero a mistura nao fixa cada ato (nivel vetorial, o passo que usa `hp`) -/

theorem peso_zero_quebra_a_mistura :
    ∃ (S : Finset (Fin 2)) (p : Fin 2 → ℝ) (w : Fin 2 → ℂ) (v : ℂ),
      (∀ i ∈ S, 0 ≤ p i) ∧ ∑ i ∈ S, p i = 1 ∧ (∀ i ∈ S, ‖w i‖ = ‖v‖) ∧
      ∑ i ∈ S, (p i : ℂ) • w i = v ∧ ¬ (∀ i ∈ S, w i = v) := by
  refine ⟨Finset.univ, ![1, 0], ![1, -1], 1, ?_, ?_, ?_, ?_, ?_⟩
  · intro i _; fin_cases i <;> simp
  · simp [Fin.sum_univ_two]
  · intro i _; fin_cases i <;> simp
  · simp [Fin.sum_univ_two]
  · intro h
    have := h 1 (Finset.mem_univ _)
    simp at this
    -- this : (-1 : ℂ) = 1
    norm_num at this

/-! ## CE3: sem a saturacao o dominio multiplicativo falha -/

noncomputable def Phi : ℂ × ℂ →ₗ[ℂ] (ℂ →L[ℂ] ℂ) :=
  LinearMap.smulRight ((1 / 2 : ℂ) • (LinearMap.fst ℂ ℂ ℂ + LinearMap.snd ℂ ℂ ℂ))
    (1 : ℂ →L[ℂ] ℂ)

theorem Phi_apply (p : ℂ × ℂ) : Phi p = ((1 / 2 : ℂ) * (p.1 + p.2)) • (1 : ℂ →L[ℂ] ℂ) := rfl

theorem Phi_estrela (x : ℂ × ℂ) : Phi (star x) = star (Phi x) := by
  rw [Phi_apply, Phi_apply, star_smul, star_one]
  congr 1
  simp

theorem Phi_schwarz (x : ℂ × ℂ) (v : ℂ) :
    ‖Phi x v‖ ^ 2 ≤ RCLike.re ⟪v, Phi (star x * x) v⟫_ℂ := by
  rw [Phi_apply, Phi_apply]
  simp only [smul_apply, one_apply_eq_self, norm_smul,
    mul_pow, inner_smul_right, RCLike.re_to_complex, Prod.fst_mul, Prod.snd_mul,
    Prod.fst_star, Prod.snd_star]
  have hv : ⟪v, v⟫_ℂ = ((‖v‖ ^ 2 : ℝ) : ℂ) := by
    rw [inner_self_eq_norm_sq_to_K]; simp
  rw [hv]
  generalize hr : ‖v‖ ^ 2 = r
  have hn : 0 ≤ r := by rw [← hr]; exact sq_nonneg _
  have e1 : ‖(1 / 2 : ℂ) * (x.1 + x.2)‖ ^ 2
      = ((x.1.re + x.2.re) ^ 2 + (x.1.im + x.2.im) ^ 2) / 4 := by
    rw [Complex.sq_norm, Complex.normSq_apply]
    simp; ring
  have e2 : ((1 / 2 : ℂ) * (star x.1 * x.1 + star x.2 * x.2) * (r : ℂ)).re
      = ((x.1.re ^ 2 + x.1.im ^ 2 + (x.2.re ^ 2 + x.2.im ^ 2)) / 2) * r := by
    rw [Complex.re_mul_ofReal]
    congr 1
    simp [Complex.mul_re, Complex.mul_im, Complex.conj_re, Complex.conj_im] <;> ring
  rw [e1, e2]
  have key : ((x.1.re + x.2.re) ^ 2 + (x.1.im + x.2.im) ^ 2) / 4
      ≤ (x.1.re ^ 2 + x.1.im ^ 2 + (x.2.re ^ 2 + x.2.im ^ 2)) / 2 := by
    nlinarith [sq_nonneg (x.1.re - x.2.re), sq_nonneg (x.1.im - x.2.im)]
  exact mul_le_mul_of_nonneg_right key hn

theorem sem_saturacao_o_dominio_multiplicativo_falha :
    (∀ x, Phi (star x) = star (Phi x)) ∧
    (∀ x v, ‖Phi x v‖ ^ 2 ≤ RCLike.re ⟪v, Phi (star x * x) v⟫_ℂ) ∧
    ∃ a b : ℂ × ℂ, Phi (b * a) ≠ Phi b * Phi a ∧
      ¬ (Phi (star a * a) = star (Phi a) * Phi a) := by
  refine ⟨Phi_estrela, fun x v => Phi_schwarz x v, ((1, 0) : ℂ × ℂ), ((0, 1) : ℂ × ℂ), ?_, ?_⟩
  · intro h
    have h1 := congrArg (fun f : ℂ →L[ℂ] ℂ => f 1) h
    simp [Phi_apply] at h1
  · intro h
    have h1 := congrArg (fun f : ℂ →L[ℂ] ℂ => f 1) h
    simp [Phi_apply, Complex.star_def] at h1

/-! ## CE1: sem o vacuo unico a conclusao de `o_que_comuta_com_o_boost_e_escalar` falha -/

abbrev H := EuclideanSpace ℂ (Fin 2)

noncomputable def e0 : H := EuclideanSpace.single (0 : Fin 2) (1 : ℂ)
noncomputable def e1 : H := EuclideanSpace.single (1 : Fin 2) (1 : ℂ)

noncomputable def P : H →L[ℂ] H := (EuclideanSpace.proj (0 : Fin 2)).smulRight e0

theorem P_apply (v : H) : P v = (v 0) • e0 := rfl

theorem P_e0 : P e0 = e0 := by simp [P_apply, e0]
theorem P_e1 : P e1 = 0 := by simp [P_apply, e1]

theorem sem_vacuo_unico_a_conclusao_falha :
    ¬ (∀ (δ Tp Tm : ℝ → H →L[ℂ] H)
        (_hδ : ∀ s v w, ⟪δ s v, δ s w⟫_ℂ = ⟪v, w⟫_ℂ)
        (_hTp : ∀ a v, ‖Tp a v‖ = ‖v‖) (_hTm : ∀ a v, ‖Tm a v‖ = ‖v‖)
        (_hp0 : ∀ v, Tp 0 v = v) (_hm0 : ∀ v, Tm 0 v = v)
        (_hpc : ∀ v, ContinuousAt (fun a => Tp a v) 0)
        (_hmc : ∀ v, ContinuousAt (fun a => Tm a v) 0)
        (_hcp : ∀ s a v, δ s (Tp a v) = Tp (Real.exp s * a) (δ s v))
        (_hcm : ∀ s a v, δ s (Tm a v) = Tm (Real.exp (-s) * a) (δ s v))
        (M : Subalgebra ℂ (H →L[ℂ] H)) (Ω : H)
        (_hsep : ∀ x ∈ M, x Ω = 0 → x = 0)
        (_hΩ : ∀ s, δ s Ω = Ω)
        (x : H →L[ℂ] H) (_hx : x ∈ M) (_hxδ : ∀ s v, δ s (x v) = x (δ s v)),
        ∃ c : ℂ, x = c • (1 : H →L[ℂ] H)) := by
  intro h
  have hM : ∀ y ∈ Subalgebra.centralizer ℂ ({P} : Set (H →L[ℂ] H)), y (e0 + e1) = 0 → y = 0 := by
    intro y hy hΩ
    have hc : P * y = y * P := ((Subalgebra.mem_centralizer_iff ℂ).mp hy) P rfl
    have hPΩ : P (e0 + e1) = e0 := by rw [map_add, P_e0, P_e1, add_zero]
    have h0 : y e0 = 0 := by
      have h1 : y (P (e0 + e1)) = P (y (e0 + e1)) := by
        have := congrArg (fun f : H →L[ℂ] H => f (e0 + e1)) hc
        simpa using this.symm
      rw [hPΩ, hΩ, map_zero] at h1
      exact h1
    have h1 : y e1 = 0 := by
      have := hΩ
      rw [map_add, h0, zero_add] at this
      exact this
    apply ContinuousLinearMap.coe_injective
    apply (EuclideanSpace.basisFun (Fin 2) ℂ).toBasis.ext
    intro i
    fin_cases i
    · simpa [OrthonormalBasis.coe_toBasis, EuclideanSpace.basisFun_apply, e0] using h0
    · simpa [OrthonormalBasis.coe_toBasis, EuclideanSpace.basisFun_apply, e1] using h1
  obtain ⟨c, hc⟩ := h (fun _ => 1) (fun _ => 1) (fun _ => 1)
    (by intros; rfl) (by intros; rfl) (by intros; rfl) (by intros; rfl) (by intros; rfl)
    (fun v => continuousAt_const) (fun v => continuousAt_const)
    (by intros; rfl) (by intros; rfl)
    (Subalgebra.centralizer ℂ ({P} : Set (H →L[ℂ] H))) (e0 + e1) hM
    (by intros; rfl) P
    ((Subalgebra.mem_centralizer_iff ℂ).mpr (fun g hg => by rw [Set.mem_singleton_iff] at hg; rw [hg]))
    (by intros; rfl)
  have a1 := congrArg (fun f : H →L[ℂ] H => (f e0) 0) hc
  have a2 := congrArg (fun f : H →L[ℂ] H => (f e1) 1) hc
  simp [P_apply, e0, e1] at a1 a2
  rw [← a1] at a2
  norm_num at a2

end TesteV

#print axioms TesteV.peso_zero_quebra_a_mistura
#print axioms TesteV.sem_saturacao_o_dominio_multiplicativo_falha
#print axioms TesteV.sem_vacuo_unico_a_conclusao_falha
