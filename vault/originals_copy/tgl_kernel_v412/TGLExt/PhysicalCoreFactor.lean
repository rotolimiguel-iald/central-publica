import TGLExt.PhysicalCoreMultipliers
import TGLExt.FockCharacters

/-! Strong limits of physical boost coefficients determine the scalar centre
of the actual regular core. The only geometric input of the final implication
is an independently meaningful approximation of real characters. -/
set_option autoImplicit false
set_option maxHeartbeats 900000
set_option synthInstance.maxHeartbeats 160000
noncomputable section
open MeasureTheory Filter
open scoped Topology
namespace K07.PhysicalCoreCenter
open TGLV350.Regular F1Rede.BosonicFock
open F1Fecho.CanonicalFockRegular

/-- Rephase by the inverse character and apply dominated convergence in L². -/
theorem coefficientOp_tendsto_character (s : ℝ) (v : ℕ → F)
    (hn : ∀ n, ‖v n‖ ≤ 1)
    (hv : ∀ x, Tendsto (fun n => coefficient (v n) (v n) x) atTop
      (𝓝 (characterPhase s x))) (f : Reg) :
    Tendsto (fun n => coefficientOp (v n) (v n) f) atTop (𝓝 (characterMultiplier s f)) := by
  let w (n : ℕ) (x : ℝ) := characterPhase (-s) x * coefficient (v n) (v n) x
  have hc (n) : Continuous (w n) :=
    (characterPhase_continuous (-s)).mul (coefficient_continuous (v n) (v n))
  have hb (n x) : ‖w n x‖ ≤ 1 := by
    change ‖characterPhase (-s) x * coefficient (v n) (v n) x‖ ≤ 1
    rw [norm_mul, characterPhase_norm, one_mul]
    exact (coefficient_bound _ _ _).trans
      ((mul_le_mul (hn n) (hn n) (norm_nonneg _) zero_le_one).trans_eq (one_mul _))
  have hl (x) : Tendsto (fun n => w n x) atTop (𝓝 1) := by
    have h := (tendsto_const_nhds (x := characterPhase (-s) x)).mul (hv x)
    simpa only [characterPhase_add, neg_add_cancel, characterPhase_zero] using h
  let W (n) : RegOp := F1Fecho.BoundedScalarL2.multiply (w n) (hc n) 1 zero_le_one (hb n)
  have hW : Tendsto (fun n => W n f) atTop (𝓝 f) :=
    F1Fecho.BoundedScalarL2.multiply_tendsto w hc 1 zero_le_one hb hl f
  have he (n) : characterMultiplier s (W n f) = coefficientOp (v n) (v n) f := by
    apply Lp.ext
    filter_upwards [characterMultiplier_ae s (W n f),
      F1Fecho.BoundedScalarL2.multiply_ae (w n) (hc n) 1 zero_le_one (hb n) f,
      coefficientOp_ae (v n) (v n) f] with x h1 h2 h3
    change (W n f) x = _ at h2
    rw [h1,h2,h3,smul_smul]
    change (characterPhase s x * (characterPhase (-s) x * _)) • f x = _
    rw [← mul_assoc,characterPhase_add,add_neg_cancel,characterPhase_zero,one_mul]
  exact (((characterMultiplier (H := F) s).continuous.tendsto f).comp hW).congr
    (fun n => he n)

/-- A single character in the pointwise closure is enough to force central
    operators to commute with that dual character. -/
theorem central_commutes_character (s : ℝ) (v : ℕ → F)
    (hn : ∀ n, ‖v n‖ ≤ 1)
    (hv : ∀ x, Tendsto (fun n => coefficient (v n) (v n) x) atTop (𝓝 (characterPhase s x)))
    (Z : RegOp) (hZ : Z ∈ core) (hZ' : Z ∈ core.commutant) :
    Commute Z (characterMultiplier s) := by
  ext1 f
  change Z (characterMultiplier s f) = characterMultiplier s (Z f)
  have left := (Z.continuous.tendsto _).comp (coefficientOp_tendsto_character s v hn hv f)
  have right := coefficientOp_tendsto_character s v hn hv (Z f)
  apply tendsto_nhds_unique left
  exact right.congr (fun n => congrArg (fun A : RegOp => A f)
    (central_commutes_coefficient Z hZ hZ' (v n) (v n)).eq.symm)

/-- The scalar-centre condition is the literal one on the concrete crossed
    product. The hypothesis concerns only the physical boost on Fock vectors. -/
theorem physical_core_center_from_boost_characters
    (h : ∀ s : ℝ, ∃ v : ℕ → F, (∀ n, ‖v n‖ ≤ 1) ∧
      ∀ x, Tendsto (fun n => coefficient (v n) (v n) x) atTop (𝓝 (characterPhase s x)))
    (Z : RegOp) (hZ : Z ∈ core) (hZ' : Z ∈ core.commutant) :
    ∃ c : ℂ, Z = c • (1 : RegOp) := by
  have hz (s : ℝ) : dualAmbient s Z = Z := by
    obtain ⟨v,hn,hv⟩ := h s
    exact (dualAmbient_fixed_iff_commutes s Z).mpr
      (central_commutes_character s v hn hv Z hZ hZ').eq.symm
  obtain ⟨C,_,rfl⟩ := (F1Fecho.CanonicalFockFaithfulWeight.fixed_core_is_base Z).mp ⟨hZ,hz⟩
  have hc (B : Op) : C*B=B*C := by
    apply fibre_injective
    rw [fibre_mul, fibre_mul]
    exact central_commutes_all_fibres (fibre C) hZ hZ' B
  obtain ⟨c,hc'⟩ := commute_wedge_boost_scalar C (fun b _ => hc b) (fun t => hc _)
  refine ⟨c,?_⟩
  rw [hc',fibre_smul,fibre_one]

/-- The actual continuous core of the physical Maxwell wedge is a factor. -/
theorem physical_core_is_factor (Z : RegOp) (hZ : Z ∈ core) (hZ' : Z ∈ core.commutant) :
    ∃ c : ℂ, Z = c • (1 : RegOp) := by
  refine physical_core_center_from_boost_characters ?_ Z hZ hZ'
  intro s
  obtain ⟨v,hn,hv⟩ := Vinculo.FockCharacters.fock_character_approximation s
  exact ⟨v,fun n => (hn n).le,hv⟩

/-- Literal equality of the centre and the scalar operators. -/
theorem physical_core_center_eq_scalars (Z : RegOp) :
    (Z ∈ core ∧ Z ∈ core.commutant) ↔ ∃ c : ℂ, Z = c • (1 : RegOp) := by
  constructor
  · rintro ⟨hZ,hZ'⟩
    exact physical_core_is_factor Z hZ hZ'
  · rintro ⟨c,rfl⟩
    exact ⟨core.toStarSubalgebra.smul_mem core.toStarSubalgebra.one_mem c,
      core.commutant.toStarSubalgebra.smul_mem core.commutant.toStarSubalgebra.one_mem c⟩

/-- Kernel of the dual action restricted to the centre of the continuous core. -/
def logPeriods : Set ℝ :=
  {s | ∀ Z : RegOp, Z ∈ core → Z ∈ core.commutant → dualAmbient s Z = Z}

theorem physical_log_periods (s : ℝ) : s ∈ logPeriods := by
  intro Z hm hc
  obtain ⟨c,rfl⟩ := physical_core_is_factor Z hm hc
  rw [map_smul, map_one]

/-- Concrete value of the Connes–Takesaki flow-of-weights formula.
The general comparison with the intersection over all modular weights is
the classification theorem, independent of this concrete computation. -/
theorem physical_flow_of_weights_spectrum :
    insert (0 : ℝ) (Real.exp '' logPeriods) = Set.Ici 0 := by
  ext r
  change (r = 0 ∨ ∃ t ∈ logPeriods, Real.exp t = r) ↔ 0 ≤ r
  constructor
  · rintro (rfl | ⟨t, _, rfl⟩)
    · exact le_rfl
    · exact (Real.exp_pos t).le
  · intro hr
    rcases eq_or_lt_of_le hr with hz | hp
    · exact Or.inl hz.symm
    · exact Or.inr ⟨Real.log r, physical_log_periods _, Real.exp_log hp⟩

end K07.PhysicalCoreCenter
