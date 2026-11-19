import TGLExt.PhysicalCoreCenter
import TGLExt.F1Fecho394.BoundedScalarL2LimitR3

/-! Matrix coefficients of the physical boost give centralizing multiplication
operators on the same regular Hilbert space. -/
set_option autoImplicit false
set_option maxHeartbeats 900000
set_option synthInstance.maxHeartbeats 160000
noncomputable section
open MeasureTheory Filter
open scoped Topology
namespace K07.PhysicalCoreCenter
open TGLV350.Regular F1Rede.BosonicFock
open F1Fecho.CanonicalFockRegular
open F1Fecho.RegularCovariantCore (boostCLM)
open F1Fecho.RegularCoreFixed (twistedCommutantField)

def coefficient (u v : F) (x : ℝ) : ℂ := inner ℂ u (boostCLM fockFlow x v)

theorem coefficient_continuous (u v : F) : Continuous (coefficient u v) :=
  continuous_const.inner (fockFlow.strong v)

theorem coefficient_bound (u v : F) (x : ℝ) :
    ‖coefficient u v x‖ ≤ ‖u‖ * ‖v‖ :=
  (norm_inner_le_norm _ _).trans_eq
    (congrArg (fun t : ℝ => ‖u‖ * t) ((fockFlow.U x).norm_map v))

def coefficientOp (u v : F) : RegOp :=
  F1Fecho.BoundedScalarL2.multiply (coefficient u v) (coefficient_continuous u v)
    (‖u‖*‖v‖) (mul_nonneg (norm_nonneg _) (norm_nonneg _)) (coefficient_bound u v)

theorem coefficientOp_ae (u v : F) (f : Reg) :
    coefficientOp u v f =ᵐ[volume] fun x => coefficient u v x • f x :=
  F1Fecho.BoundedScalarL2.multiply_ae _ _ _ _ _ _

/-- Applying the multiplier to any test vector gives a bounded linear map
in the second physical vector. The bound is uniform on the unit ball of tests. -/
def coefficientCLM (u : F) (f : Reg) : F →L[ℂ] Reg := by
  let L : F →ₗ[ℂ] Reg :=
    { toFun := fun v => coefficientOp u v f
      map_add' := by
        intro v w
        apply Lp.ext
        filter_upwards [coefficientOp_ae u (v+w) f, coefficientOp_ae u v f,
          coefficientOp_ae u w f, Lp.coeFn_add (coefficientOp u v f) (coefficientOp u w f)]
            with x h1 h2 h3 h4
        change (coefficientOp u (v+w) f) x =
          (coefficientOp u v f + coefficientOp u w f) x
        rw [h1,h4]
        simp only [Pi.add_apply,h2,h3,coefficient,map_add,inner_add_right,add_smul]
      map_smul' := by
        intro c v
        apply Lp.ext
        filter_upwards [coefficientOp_ae u (c • v) f, coefficientOp_ae u v f,
          Lp.coeFn_smul c (coefficientOp u v f)] with x h1 h2 h3
        change (coefficientOp u (c • v) f) x = (c • coefficientOp u v f) x
        rw [h1,h3]
        simp only [Pi.smul_apply,h2,coefficient,map_smul,inner_smul_right,smul_smul] }
  have bound (v : F) : ‖L v‖ ≤ (‖u‖ * ‖f‖) * ‖v‖ := by
    have hop : ‖coefficientOp u v‖ ≤ ‖u‖ * ‖v‖ :=
      operatorFieldLift_norm_le (F1Fecho.BoundedScalarL2.field (H := F)
        (coefficient u v) (coefficient_continuous u v) (‖u‖*‖v‖)
        (mul_nonneg (norm_nonneg u) (norm_nonneg v)) (coefficient_bound u v))
    exact ((coefficientOp u v).le_of_opNorm_le hop f).trans_eq (by ring)
  refine { toLinearMap := L, cont := ?_ }
  have hlip : LipschitzWith (‖u‖₊ * ‖f‖₊) L := by
    apply LipschitzWith.of_dist_le_mul
    intro v w
    simpa only [dist_eq_norm, ← map_sub, NNReal.coe_mul, coe_nnnorm] using bound (v-w)
  exact hlip.continuous

private def ketBra (a b : F) : Op := (innerSL ℂ b).smulRight a

private theorem ketBra_apply (a b v : F) : ketBra a b v = inner ℂ b v • a := rfl

/-- A rank-one compression of the twisted commutant field extracts a
    boost coefficient, pointwise on L². -/
private theorem coefficient_compression (a u : F) (D : Op) :
    coefficientOp u (D vacuum) * fibre (ketBra a vacuum) =
    (fibre (ketBra a u) * operatorFieldLift (twistedCommutantField fockFlow D)) *
      fibre (ketBra vacuum vacuum) := by
  let R := operatorFieldLift (twistedCommutantField fockFlow D)
  have hv (x : ℝ) :
      (twistedCommutantField fockFlow D).op x vacuum = boostCLM fockFlow x (D vacuum) := by
    change F1Fecho.RegularCovariantCore.automorphism fockFlow x D vacuum = _
    rw [F1Fecho.RegularCovariantCore.boostAd_sandwich,
        F1Fecho.RegularCovariantCore.boostCLM_star]
    change boostCLM fockFlow x (D (boostCLM fockFlow (-x) vacuum)) = _
    rw [show boostCLM fockFlow (-x) vacuum = vacuum from gamma_vacuum _]
  ext1 f
  apply Lp.ext
  filter_upwards [coefficientOp_ae u (D vacuum) (fibre (ketBra a vacuum) f),
    fibre_ae (ketBra a vacuum) f,
    fibre_ae (ketBra a u) (R (fibre (ketBra vacuum vacuum) f)),
    operatorFieldLift_ae (twistedCommutantField fockFlow D) (fibre (ketBra vacuum vacuum) f),
    fibre_ae (ketBra vacuum vacuum) f] with x h1 h2 h3 h4 h5
  change (coefficientOp u (D vacuum) (fibre (ketBra a vacuum) f)) x =
    (fibre (ketBra a u) (R (fibre (ketBra vacuum vacuum) f))) x
  change (R (fibre (ketBra vacuum vacuum) f)) x = _ at h4
  rw [h1,h2,h3,h4,h5]
  simp only [ketBra_apply, map_smul, hv, coefficient, smul_smul]
  rw [mul_comm]

/-- The orbits of the complementary wedge are already dense in Fock space.
    Hence bounded Weyl operators in the physical commutant have total orbit. -/
theorem right_vacuum_cyclic :
    Dense ((Submodule.span ℂ ((fun D : Op => D vacuum) '' (M.commutant : Set Op)) :
      Submodule ℂ F) : Set F) := by
  let K := F1Rede.CanonicalWedge.KWR
  apply (F1Fecho.WedgeCyclic.vacuum_cyclic K.symplComp).mono
  apply Submodule.span_mono
  rintro _ ⟨D,hD,rfl⟩
  refine ⟨D,?_,rfl⟩
  change D ∈ M.commutant
  rw [VonNeumannAlgebra.mem_commutant_iff]
  intro A hA
  exact (F1Fecho.FieldWeyl.R_local _ _
    (fun u hu v hv => ClosedSubmodule.mem_symplComp_iff.mp hv u hu) A hA D hD).eq

theorem central_commutes_orbit_coefficient (Z : RegOp) (hZ : Z ∈ core)
    (hZ' : Z ∈ core.commutant) (u : F) (D : Op) (hD : D ∈ M.commutant) :
    Commute Z (coefficientOp u (D vacuum)) := by
  let W := coefficientOp u (D vacuum)
  let R := operatorFieldLift (twistedCommutantField fockFlow D)
  have hR : Commute Z R :=
    (VonNeumannAlgebra.mem_commutant_iff.mp (F1Fecho.RegularCoreFixed.twistedCommutantLift_mem
      fockFlow M F1Fecho.CanonicalFockFaithfulWeight.boost_normalizes D hD)) _ hZ
  have hf (a b : F) : Commute Z (fibre (ketBra a b)) :=
    central_commutes_all_fibres Z hZ hZ' _
  have hzero (a : F) : (Z*W-W*Z) * fibre (ketBra a vacuum) = 0 := by
    let V := fibre (ketBra a vacuum)
    have h1 : Commute Z (W*V) := by
      rw [show W*V = _ from coefficient_compression a u D]
      exact ((hf a u).mul_right hR).mul_right (hf vacuum vacuum)
    have h2 := (hf a vacuum).eq
    change Z*V = V*Z at h2
    change (Z*W-W*Z)*V = 0
    rw [sub_mul]
    apply sub_eq_zero.mpr
    calc
      (Z*W)*V = Z*(W*V) := mul_assoc _ _ _
      _ = (W*V)*Z := h1.eq
      _ = (W*Z)*V := by simp only [mul_assoc, h2]
  apply sub_eq_zero.mp
  apply fibreSlice_zero
  intro s t
  ext1 a
  have eq := congrArg (fun T : RegOp => fibreSlice T s t) (hzero a)
  rw [fibreSlice_right] at eq
  have hz : fibreSlice (0 : RegOp) s t = 0 := by simp [fibreSlice]
  rw [hz] at eq
  have ev := congrArg (fun B : Op => B vacuum) eq
  have unit : inner ℂ vacuum vacuum = 1 := by
    rw [inner_self_eq_norm_sq_to_K, F1Rede.BosonicFock.vacuum_norm]; norm_num
  change fibreSlice (Z*W-W*Z) s t (ketBra a vacuum vacuum) = 0 at ev
  rwa [ketBra_apply, unit, one_smul] at ev

theorem central_commutes_coefficient (Z : RegOp) (hZ : Z ∈ core)
    (hZ' : Z ∈ core.commutant) (u v : F) : Commute Z (coefficientOp u v) := by
  ext1 f
  let left : F →L[ℂ] Reg := Z.comp (coefficientCLM u f)
  let right : F →L[ℂ] Reg := coefficientCLM u (Z f)
  have he : left = right := by
    apply ContinuousLinearMap.ext_on right_vacuum_cyclic
    rintro _ ⟨D,hD,rfl⟩
    exact congrArg (fun A : RegOp => A f)
      (central_commutes_orbit_coefficient Z hZ hZ' u D hD).eq
  exact congrArg (fun A : F →L[ℂ] Reg => A v) he

end K07.PhysicalCoreCenter
