import TGLExt.VinculoCriterion
import TGLExt.WedgeFactor
import TGLExt.PhysicalCoreFactor

/-! Classification and observer readout for the same Maxwell Weyl wedge. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace Vinculo
open TGL.SpecificAQFT F1Rede.BosonicFock TGLExt.ImportedSQ
open F1Fecho.CanonicalFockRegular F1Fecho.PhysicalFockNet
open F1Fecho.OrbitalSpatial F1Fecho.SpacetimeLorentz F1Fecho.MaxwellLocalization K07.Horizon
open F1Fecho.Antilinear ChatgptAudit TGLExt

theorem maxwell_right_wedge_type_III1 : IsTypeIII1 (net rightWedge) := by
  have hid : net rightWedge = M := net_wedge_eq
  refine ⟨?_,vacuum,canonicalFockJ,fockFlow,vacuum_norm,vacuum_cyclic,
    vacuum_separating,pair_tomita,?_,?_⟩
  · rw [hid]
    exact WedgeFactor.wedge_center_scalar
  · rw [hid]
    exact F1Fecho.CanonicalFockFaithfulWeight.boost_normalizes
  · rw [hid]
    exact K07.PhysicalCoreCenter.physical_core_is_factor

/-- A single statement names the classified algebra, every index readout,
the geometrical boundary in the observer's chart and a transported field. -/
theorem light_tower_horizon_observer (L : generatedLorentz) (a : Point) :
    IsTypeIII1 (net rightWedge) ∧
    (∀ (N : ℕ) (i j : chainIdx N), ReadsTowerOnWedge N i j) ∧
    frontier (observerChart L a '' rightWedge) =
      (observerChart L a '' futureSheet) ∪ (observerChart L a '' pastSheet) ∧
    (∀ A : F →L[ℂ] F, A ∈ net rightWedge ↔
      (gamma (observerUnitary L a)).conjStarAlgEquiv A ∈ net (observerChart L a '' rightWedge)) ∧
    ∃ f : H1, f ≠ 0 ∧ f ∈ physicalCanonicalNet.K rightWedge ∧ observerUnitary L a f ≠ 0 ∧
      F1Fecho.FieldWeyl.W (observerUnitary L a f) ∈ net (observerChart L a '' rightWedge) :=
  ⟨maxwell_right_wedge_type_III1,tower_observer_diagram,
    (observer_and_wedge_algebra L a 0).1,fun A => (observer_and_wedge_algebra L a A).2,
    transported_light_witness L a⟩

end Vinculo
