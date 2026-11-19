import TGLExt.LightRhoStar
import TGLExt.F1Fecho394.CanonicalFockModularCoreInputR1
import TGLExt.F1Fecho394.CanonicalWedgeFlowR2
import TGLExt.F1Fecho394.BosonicFockGroupActions
import TGLExt.OUmInscrito
import TGLExt.F1Fecho394.PhysicalCanonicalWedgeEqualityR3

set_option autoImplicit false

open TGLExt.ImportedSQ F1Fecho.CanonicalFockModularCoreInputR1
open F1Rede.BosonicFock F1Rede.BosonicFockGroupActions
open TGLExt.ContratoQGv31 (nullDir)

/-- T4 pelo que o kernel ja tinha: light_null_ergodic no certificado fisico. -/
theorem t4_pelo_que_o_kernel_ja_tinha (ψ : F)
    (hψ : ∀ l : ℝ, UF (l • nullDir) ψ = ψ) : ψ ∈ (ℂ ∙ vacuum) :=
  TGLExt.ImportedSQ.light_null_ergodic physicalFockCertificate ψ hψ

#print axioms t4_pelo_que_o_kernel_ja_tinha

/-- A algebra M nao e escalar (nao-abeliana): campo do certificado fisico. -/
theorem M_nao_abeliana :
    ∃ a ∈ F1Fecho.CanonicalWedgeFlow.M, ∃ b ∈ F1Fecho.CanonicalWedgeFlow.M, a * b ≠ b * a := by
  obtain ⟨a, ha, b, hb, h⟩ := physicalFockCertificate.wedge_nonabelian
  refine ⟨a, ?_, b, ?_, h⟩
  · have e : physicalFockCertificate.R
      (F1Fecho.MaxwellLocalization.physicalCanonicalNet.toLightNetData.toLightOneParticle.K
        TGL.SpecificAQFT.rightWedge) = F1Fecho.CanonicalWedgeFlow.M := by
      show F1Fecho.FieldWeyl.R (F1Fecho.MaxwellLocalization.physicalCanonicalNet.K TGL.SpecificAQFT.rightWedge)
          = F1Fecho.FieldWeyl.R F1Rede.CanonicalWedge.KWR.toClosedSubmodule.toSubmodule
      rw [F1Fecho.MaxwellLocalization.physicalCanonicalNet.wedge_glue]
      rfl
    rw [← e]; exact ha
  · have e : physicalFockCertificate.R
      (F1Fecho.MaxwellLocalization.physicalCanonicalNet.toLightNetData.toLightOneParticle.K
        TGL.SpecificAQFT.rightWedge) = F1Fecho.CanonicalWedgeFlow.M := by
      show F1Fecho.FieldWeyl.R (F1Fecho.MaxwellLocalization.physicalCanonicalNet.K TGL.SpecificAQFT.rightWedge)
          = F1Fecho.FieldWeyl.R F1Rede.CanonicalWedge.KWR.toClosedSubmodule.toSubmodule
      rw [F1Fecho.MaxwellLocalization.physicalCanonicalNet.wedge_glue]
      rfl
    rw [← e]; exact hb

#print axioms M_nao_abeliana

/-- M e a algebra de Weyl da cunha direita FISICA (suporte localizado). -/
theorem M_e_a_cunha_fisica :
    F1Fecho.CanonicalWedgeFlow.M = F1Fecho.FieldWeyl.R
      (F1Fecho.MaxwellLocalization.localized F1Fecho.MaxwellLocalization.physicalRightWedge) := by
  show F1Fecho.FieldWeyl.R _ = _
  rw [F1Fecho.MaxwellLocalization.physical_right_wedge_eq_KWR]

#print axioms M_e_a_cunha_fisica
