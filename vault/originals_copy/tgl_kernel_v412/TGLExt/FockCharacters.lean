import TGLExt.F1Fecho394.CanonicalFockRegularCoreR2
import TGLExt.F1Fecho394.LpIntervalTotalityR3
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus

/-! Approximate every character of the real line by unit vector coefficients
of the physical boost on the one-particle sector of the actual Fock space. -/
set_option autoImplicit false
noncomputable section

namespace Vinculo.FockCharacters
open MeasureTheory Filter TGLExt.ImportedSQ TGLV350.Regular F1Rede.BosonicFock
open F1Rede.Canonical F1Rede.CanonicalWedge F1Fecho.LpIntervalTotality
open F1Fecho.CanonicalFockRegular F1Fecho.RegularCovariantCore
open scoped Topology InnerProductSpace

private theorem fibre_unit : ∃ v : AuditF13v31.TransverseFiber, ‖v‖ = 1 := by
  haveI := AuditF13v31.H1_nontrivial
  obtain ⟨f, hf⟩ := exists_ne (0 : H1)
  have hF : Phi f ≠ 0 := fun h => hf (Phi.injective (h.trans (map_zero Phi).symm))
  have h : ∃ x : ℝ, (Phi f) x ≠ 0 := by
    by_contra! he
    apply hF
    apply Lp.ext
    filter_upwards [Lp.coeFn_zero AuditF13v31.TransverseFiber 2 (volume : Measure ℝ)] with y hy
    exact (he y).trans hy.symm
  obtain ⟨x,hx⟩ := h
  exact ⟨(‖(Phi f) x‖⁻¹ : ℂ) • (Phi f) x, norm_smul_inv_norm hx⟩

private def packet (a h : ℝ) (v : AuditF13v31.TransverseFiber) : RH :=
  (((Real.sqrt h)⁻¹ : ℝ) : ℂ) • intervalVector a (a+h) v

private theorem raw_coefficient (a h b : ℝ) (hh : 0 < h)
    (v : AuditF13v31.TransverseFiber) (hv : ‖v‖ = 1) :
    inner ℂ (intervalVector a (a+h) v) (characterMultiplier b (intervalVector a (a+h) v)) =
      ∫ y in a..a+h, characterPhase b y := by
  rw [intervalIntegral.integral_of_le (by linarith)]
  unfold intervalVector
  rw [L2.inner_indicatorConstLp_eq_setIntegral_inner]
  apply setIntegral_congr_ae measurableSet_Ioc
  have hi := indicatorConstLp_coeFn (p := (2 : ENNReal)) (hs := measurableSet_Ioc (a:=a) (b:=a+h))
    (hμs := (by simp : volume (Set.Ioc a (a+h)) ≠ ⊤)) (c := v)
  filter_upwards [characterMultiplier_ae b (intervalVector a (a+h) v), hi] with y hm hy hym
  change inner ℂ v ((characterMultiplier b (intervalVector a (a+h) v)) y) = _
  rw [hm]
  change (intervalVector a (a+h) v) y = _ at hy
  simp [hy, hym, inner_smul_right, inner_self_eq_norm_sq_to_K, hv, characterPhase]

private theorem packet_coefficient (a h b : ℝ) (hh : 0 < h)
    (v : AuditF13v31.TransverseFiber) (hv : ‖v‖ = 1) :
    inner ℂ (packet a h v) (characterMultiplier b (packet a h v)) =
      h⁻¹ • ∫ y in a..a+h, characterPhase b y := by
  unfold packet
  rw [map_smul, inner_smul_left, inner_smul_right, raw_coefficient a h b hh v hv]
  simp only [Complex.conj_ofReal, Complex.real_smul, ← mul_assoc,
    ← Complex.ofReal_mul, ← mul_inv_rev, Real.mul_self_sqrt hh.le]

private theorem packet_norm (a h : ℝ) (hh : 0 < h)
    (v : AuditF13v31.TransverseFiber) (hv : ‖v‖ = 1) : ‖packet a h v‖ = 1 := by
  have hp := packet_coefficient a h 0 hh v hv
  simp only [characterMultiplier_zero, one_apply_eq_self, characterPhase_zero,
    intervalIntegral.integral_const, add_sub_cancel_left, smul_smul, inv_mul_cancel₀ hh.ne', one_smul] at hp
  have hr : ‖packet a h v‖ ^ 2 = (1 : ℝ) :=
    (norm_sq_eq_re_inner (𝕜 := ℂ) (packet a h v)).trans (congrArg Complex.re hp)
  nlinarith [norm_nonneg (packet a h v)]

private theorem mean_tendsto (a b : ℝ) :
    Tendsto (fun h : ℝ => h⁻¹ • ∫ y in a..a+h, characterPhase b y)
      (𝓝[≠] 0) (𝓝 (characterPhase b a)) := by
  have hc := characterPhase_continuous b
  have hd := intervalIntegral.integral_hasDerivAt_right
    (hc.intervalIntegrable a a) hc.stronglyMeasurable.stronglyMeasurableAtFilter hc.continuousAt
  simpa only [intervalIntegral.integral_same, sub_zero] using hd.tendsto_slope_zero

theorem fock_character_approximation (s : ℝ) :
    ∃ ξ : ℕ → F, (∀ n, ‖ξ n‖ = 1) ∧ ∀ x : ℝ,
      Tendsto (fun n => inner ℂ (ξ n) (boostCLM fockFlow x (ξ n)))
        atTop (𝓝 (characterPhase s x)) := by
  obtain ⟨v,hv⟩ := fibre_unit
  let a := -s/(4*Real.pi^2)
  let h := fun n : ℕ => 1 / ((n:ℝ)+1)
  have hh (n : ℕ) : 0 < h n := by dsimp [h]; positivity
  have ht : Tendsto h atTop (𝓝[≠] 0) :=
    tendsto_nhdsWithin_iff.mpr ⟨tendsto_one_div_add_atTop_nhds_zero_nat,
      Eventually.of_forall (fun n => (hh n).ne')⟩
  refine ⟨fun n => oneParticle (Phi.symm (packet a (h n) v)), ?_, ?_⟩
  · intro n
    rw [oneParticle.norm_map, Phi.symm.norm_map, packet_norm a (h n) (hh n) v hv]
  · intro x
    let b := 2*Real.pi*(-(2*Real.pi*x))
    have hp : characterPhase b a = characterPhase s x := by
      unfold characterPhase
      congr 1
      dsimp [a,b]
      push_cast
      field_simp [Real.pi_ne_zero]
      ring
    rw [← hp]
    refine ((mean_tendsto a b).comp ht).congr (fun n => ?_)
    change _ = inner ℂ _ (gamma (B0 (-(2*Real.pi*x))) (oneParticle _))
    rw [gamma_oneParticle, oneParticle.inner_map_map]
    rw [← Phi.inner_map_map, canonicalPartialFourier_boost]
    simp only [LinearIsometryEquiv.apply_symm_apply]
    exact (packet_coefficient a (h n) b (hh n) v hv).symm

end Vinculo.FockCharacters
