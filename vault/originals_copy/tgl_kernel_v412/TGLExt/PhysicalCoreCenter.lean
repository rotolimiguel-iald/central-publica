import TGLExt.F1Fecho394.CanonicalFockModularCoreInputR1
import TGLExt.F1Fecho394.CanonicalFockFaithfulWeightR2
import TGLExt.LightRhoStar
import TGLExt.V350FibreSlices

/-! Central operators of the represented continuous core of the physical Maxwell wedge. -/
set_option autoImplicit false
set_option maxHeartbeats 1100000
noncomputable section
namespace K07.PhysicalCoreCenter
open TGLV350.Regular F1Rede.BosonicFock
open F1Fecho.CanonicalFockRegular
open F1Fecho.RegularCovariantCore (boostCLM)
open F1Fecho.CanonicalFockModularCoreInputR1 (physicalFockCertificate)

abbrev Op := F →L[ℂ] F
abbrev Reg := RegularHilbert F
abbrev RegOp := Reg →L[ℂ] Reg

/-- Commutation on the cyclic vacuum orbit separates the commutant. -/
theorem commute_wedge_boost_scalar (A : Op)
    (hM : ∀ b ∈ M, A*b = b*A)
    (hB : ∀ t : ℝ, A * boostCLM fockFlow t = boostCLM fockFlow t * A) :
    ∃ c : ℂ, A = c • (1 : Op) := by
  have fixed (t : ℝ) : TGLExt.ImportedSQ.lightDelta physicalFockCertificate t
      (A vacuum) = A vacuum := by
    have h := congrArg (fun X : Op => X vacuum) (hB t).symm
    change boostCLM fockFlow t (A vacuum) = A (boostCLM fockFlow t vacuum) at h
    have hv : boostCLM fockFlow t vacuum = vacuum :=
      F1Rede.BosonicFock.gamma_vacuum _
    exact h.trans (congrArg A hv)
  have hl := (TGLExt.QGReaderUVLock.light_modular_fixed_iff_vacuum
    physicalFockCertificate (A vacuum)).mp fixed
  obtain ⟨c,hc⟩ := Submodule.mem_span_singleton.mp hl
  change c • vacuum = A vacuum at hc
  refine ⟨c, ContinuousLinearMap.ext_on F1Fecho.WedgeCyclic.canonical_wedge_cyclic ?_⟩
  rintro _ ⟨b,hb,rfl⟩
  calc
    A (b vacuum) = b (A vacuum) := congrArg (fun X : Op => X vacuum) (hM b hb)
    _ = _ := by rw [← hc, map_smul]; rfl

/-- A central element commutes separately with the boost acting in the fibre:
    the ordinary shift is already in the commutant of the regular model. -/
theorem central_commutes_boost (Z : RegOp) (hZ : Z ∈ core) (hZ' : Z ∈ core.commutant)
    (t : ℝ) : Z * fibre (boostCLM fockFlow t) = fibre (boostCLM fockFlow t) * Z := by
  have hreg := (VonNeumannAlgebra.mem_commutant_iff.mp hZ') _ (regular_mem t)
  have hsh := (VonNeumannAlgebra.mem_commutant_iff.mp
    (F1Fecho.RegularCoreFixed.shift_mem_regularCommutant fockFlow M (-t))) _ hZ
  have hab : regularUnitary t * shift (-t) = fibre (boostCLM fockFlow t) := by
    change (fibre (boostCLM fockFlow t) * shift t) * shift (-t) = _
    rw [mul_assoc, shift_mul, add_neg_cancel, shift_zero, mul_one]
  rw [← hab]
  exact (show Commute Z (regularUnitary t) from hreg.symm).mul_right
    (show Commute Z (shift (-t)) from hsh)

/-- Every two-sided finite-set matrix coefficient of an actual central element
    is scalar on the physical Fock space. -/
theorem central_fibre_slice_scalar (Z : RegOp) (hZ : Z ∈ core)
    (hZ' : Z ∈ core.commutant) (s t : FiniteFibreSet) :
    ∃ c : ℂ, fibreSlice Z s t = c • (1 : Op) := by
  apply commute_wedge_boost_scalar
  · intro b hb
    have h := congrArg (fun T : RegOp => fibreSlice T s t)
      ((VonNeumannAlgebra.mem_commutant_iff.mp hZ') _ (fibre_mem b hb)).symm
    simpa only [fibreSlice_left, fibreSlice_right] using h
  · intro r
    have h := congrArg (fun T : RegOp => fibreSlice T s t)
      (central_commutes_boost Z hZ hZ' r)
    simpa only [fibreSlice_left, fibreSlice_right] using h

/-- The central operator commutes with *every* constant Fock operator,
    including operators outside the represented wedge. -/
theorem central_commutes_all_fibres (Z : RegOp) (hZ : Z ∈ core)
    (hZ' : Z ∈ core.commutant) (B : Op) : Z * fibre B = fibre B * Z := by
  apply sub_eq_zero.mp
  apply fibreSlice_zero
  intro s t
  rw [fibreSlice_sub, fibreSlice_left, fibreSlice_right]
  obtain ⟨c,hc⟩ := central_fibre_slice_scalar Z hZ hZ' s t
  rw [hc, smul_mul_assoc, mul_smul_comm, mul_one, one_mul, sub_self]

end K07.PhysicalCoreCenter
