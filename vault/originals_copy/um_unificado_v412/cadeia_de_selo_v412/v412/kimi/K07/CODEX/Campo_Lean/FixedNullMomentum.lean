import TGLExt.LightHelicityWigner
import TGLExt.F1Fecho394.ScreenPhysicalHelicityR2

/-! Proper Lorentz stabilizer of a regular massless momentum and its screen character.
    The classification by the Euclidean group and a Lagrangian for the scalar action
    are separate problems. -/

set_option autoImplicit false
noncomputable section

namespace K07.Field
open TGLExt ChatgptAudit.WignerOrbit016 ChatgptAudit.WignerRapidityMeasure016
open F1Fecho.OrbitalSpatial F1Fecho.OrbitalScreen ORDEM016.D1prime

def properMomentumStabilizer (p : Fin 4 → ℝ) : Subgroup LorentzGrp where
  carrier := {L | lorentzLinear L p = p ∧ L.val.det = 1}
  one_mem' := by simp [lorentzLinear_one, lorentzGrp_one_val]
  mul_mem' := by
    intro L M hL hM
    exact ⟨by rw [lorentzLinear_mul, LinearMap.comp_apply, hM.1, hL.1],
      by rw [lorentzGrp_mul_val, Matrix.det_mul, hL.2, hM.2, one_mul]⟩
  inv_mem' := by
    intro L hL
    constructor
    · calc
        lorentzLinear L⁻¹ p = lorentzLinear L⁻¹ (lorentzLinear L p) :=
          congrArg (lorentzLinear L⁻¹) hL.1.symm
        _ = lorentzLinear (L⁻¹ * L) p := by rw [lorentzLinear_mul, LinearMap.comp_apply]
        _ = p := by rw [inv_mul_cancel, lorentzLinear_one, LinearMap.id_apply]
    · calc
        (L⁻¹).val.det = (L⁻¹).val.det * L.val.det := by rw [hL.2, mul_one]
        _ = ((L⁻¹ * L).val).det := by rw [lorentzGrp_mul_val, Matrix.det_mul]
        _ = 1 := by rw [inv_mul_cancel, lorentzGrp_one_val, Matrix.det_one]

def masslessMomentum (x : MomentumCoordinates) : Fin 4 → ℝ :=
  shellMomentum 0 (rapidityChart 0 x)

def fixedPhase (x : MomentumCoordinates) (L : properMomentumStabilizer (masslessMomentum x)) : ℂ :=
  screenPhase (lorentzLinear L.val) x x

theorem fixedScreenOriented (x : MomentumCoordinates) (hx : x.1 ≠ 0)
    (L : properMomentumStabilizer (masslessMomentum x)) :
    ScreenOrientationMeasured (lorentzLinear L.val) x x := by
  apply F1Fecho.ScreenOrientation.screen_orientation_of_proper_transport _ x x hx hx
  · exact L.property.1
  · exact orbitPairing_lorentz L.val
  · rw [lorentzLinear_toMatrix]
    exact L.property.2

theorem fixedPhase_unit (x : MomentumCoordinates) (hx : x.1 ≠ 0)
    (L : properMomentumStabilizer (masslessMomentum x)) :
    Complex.normSq (fixedPhase x L) = 1 :=
  oriented_screen_phase_unit _ x x hx hx L.property.1 (orbitPairing_lorentz L.val)
    (fixedScreenOriented x hx L)

theorem fixedPhase_mul (x : MomentumCoordinates) (hx : x.1 ≠ 0)
    (L M : properMomentumStabilizer (masslessMomentum x)) :
    fixedPhase x (L * M) = fixedPhase x L * fixedPhase x M := by
  unfold fixedPhase
  rw [Subgroup.coe_mul, lorentzLinear_mul]
  exact screen_phase_cocycle _ _ x x x hx hx hx M.property.1 L.property.1
    (orbitPairing_lorentz M.val) (fixedScreenOriented x hx M)

def fixedPhaseHom (x : MomentumCoordinates) (hx : x.1 ≠ 0) :
    properMomentumStabilizer (masslessMomentum x) →* ℂ where
  toFun := fixedPhase x
  map_mul' := fixedPhase_mul x hx
  map_one' := by
    have h := fixedPhase_mul x hx 1 1
    rw [one_mul] at h
    have hn : fixedPhase x 1 ≠ 0 := by
      intro he
      have hu := fixedPhase_unit x hx 1
      rw [he, map_zero] at hu
      exact zero_ne_one hu
    apply mul_left_cancel₀ hn
    simpa only [mul_one] using h.symm

end K07.Field

#print axioms K07.Field.properMomentumStabilizer
#print axioms K07.Field.fixedScreenOriented
#print axioms K07.Field.fixedPhase_unit
#print axioms K07.Field.fixedPhase_mul
#print axioms K07.Field.fixedPhaseHom
