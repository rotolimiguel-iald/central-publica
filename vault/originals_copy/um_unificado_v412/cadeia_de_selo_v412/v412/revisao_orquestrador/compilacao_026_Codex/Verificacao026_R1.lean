import TGLExt.F1Fecho394.CanonicalFockModularCoreInputR1
import TGLExt.ContratoQG_v31_Teoremas
import TGLExt.TraducaoTuring
import TGLExt.ModularFlowSpectrum
import TGLExt.MixedLadder
import TGLExt.TheRootOfTheProofTree
namespace Revisao026
open TGLExt.ImportedSQ TGLExt.ContratoQGv31 F1Fecho.CanonicalFockModularCoreInputR1
theorem setorFisico (N : KillingNormalization) :
    NoEigenOutsideVacuum (lightNet physicalFockCertificate) (lightDelta physicalFockCertificate) :=
  (lightH2 physicalFockCertificate N).no_point_spectrum
theorem vacuoFixo (N : KillingNormalization) (t : ℝ) :
    lightDelta physicalFockCertificate t physicalFockCertificate.Ω = physicalFockCertificate.Ω :=
  (lightH2 physicalFockCertificate N).Δit_vac t
#print axioms setorFisico
#print axioms vacuoFixo
#print axioms ChatgptAudit.modularFlow_eigenvector
#print axioms ChatgptAudit.localEigenvectors_total
#print axioms TGLExt.mixed_log_dense
#print axioms TGLExt.the_aperiodic_antecedent_is_now_a_term
end Revisao026
