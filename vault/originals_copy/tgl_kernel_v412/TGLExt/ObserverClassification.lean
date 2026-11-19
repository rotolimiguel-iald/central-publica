import TGLExt.TransportPair
import TGLExt.Classificacao

/-! Type III₁ and the two concrete scalar centres in every observer chart of
the proper generated Lorentz and spacetime translation orbit of the wedge. -/
set_option autoImplicit false
noncomputable section
namespace K07.Horizon.TransportCenter
open TGL.SpecificAQFT F1Fecho F1Fecho.OrbitalSpatial
open F1Rede.BosonicFock F1Fecho.Antilinear

theorem observer_vacuum_pair_tomita (L : generatedLorentz) (a : Point) :
    ORDEM016.D6.PairTomitaAnalyticRealizationMeasured (frameAlg L a).toStarSubalgebra vacuum
      (((frameU L a).symm.trans canonicalFockJ).trans (frameU L a))
      (conjugateFlow (frameU L a) CanonicalFockRegular.fockFlow).U := by
  have hp := measured_pair_transport (PhysicalFockNet.net rightWedge) (frameAlg L a)
    vacuum (frameU L a) canonicalFockJ CanonicalFockRegular.fockFlow
    (fun z => (observer_and_wedge_algebra L a z).2) PhysicalFockNet.pair_tomita
  simpa only [frameU, gamma_vacuum] using hp

theorem observer_base_center_scalar (L : generatedLorentz) (a : Point) :
    Vinculo.HasScalarCenter (frameAlg L a) :=
  scalar_center_transport _ _ _ (base_covariance L a) Vinculo.WedgeFactor.wedge_center_scalar

theorem observer_core_center_scalar (L : generatedLorentz) (a : Point) :
    Vinculo.HasScalarCenter (frameCore L a) :=
  scalar_center_transport _ _ _ (core_covariance L a) K07.PhysicalCoreCenter.physical_core_is_factor

theorem maxwell_observer_wedge_type_III1 (L : generatedLorentz) (a : Point) :
    Vinculo.IsTypeIII1 (PhysicalFockNet.net (observerChart L a '' rightWedge)) :=
  observer_wedge_typeIII1 L a Vinculo.maxwell_right_wedge_type_III1

end K07.Horizon.TransportCenter
