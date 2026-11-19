import TGLExt.LightRhoStar
import TGLExt.F1Fecho394.CanonicalFockModularCoreInputR1
import TGLExt.F1Fecho394.CanonicalWedgeFlowR2
import TGLExt.F1Fecho394.BosonicFockGroupActions
import TGLExt.OUmInscrito

set_option autoImplicit false

open TGLExt.ImportedSQ F1Fecho.CanonicalFockModularCoreInputR1
open F1Rede.BosonicFock F1Rede.BosonicFockGroupActions

/-- O kernel ja instancia o centralizador trivial no certificado fisico (sem hipotese de certificado). -/
theorem instancia_no_certificado_fisico
    (a : (physicalFockCertificate.R
      (F1Fecho.MaxwellLocalization.physicalCanonicalNet.toLightNetData.toLightOneParticle.K
        TGL.SpecificAQFT.rightWedge)).toStarSubalgebra)
    (ha : ∀ t : ℝ, physicalFockCertificate.flow t a = a) :
    ∃ c : ℂ, a.val = c • (1 : F →L[ℂ] F) :=
  TGLExt.LightRhoStar.centralizer_is_trivial physicalFockCertificate a ha

#print axioms instancia_no_certificado_fisico

theorem a_algebra_fisica_e_M :
    (physicalFockCertificate.R
      (F1Fecho.MaxwellLocalization.physicalCanonicalNet.toLightNetData.toLightOneParticle.K
        TGL.SpecificAQFT.rightWedge))
    = F1Fecho.CanonicalWedgeFlow.M := by
  show F1Fecho.FieldWeyl.R (F1Fecho.MaxwellLocalization.physicalCanonicalNet.K TGL.SpecificAQFT.rightWedge)
      = F1Fecho.FieldWeyl.R F1Rede.CanonicalWedge.KWR.toClosedSubmodule.toSubmodule
  rw [F1Fecho.MaxwellLocalization.physicalCanonicalNet.wedge_glue]
  rfl

#print axioms a_algebra_fisica_e_M

/-- A ergodicidade na luz da candidata (T5), derivada SO do que o kernel ja tinha. -/
theorem t5_pelo_que_o_kernel_ja_tinha (x : F →L[ℂ] F)
    (hx : x ∈ F1Fecho.CanonicalWedgeFlow.M)
    (hxδ : ∀ (s : ℝ) (v : F), VF s (x v) = x (VF s v)) :
    ∃ c : ℂ, x = c • (1 : F →L[ℂ] F) := by
  have hx' : x ∈ physicalFockCertificate.R
      (F1Fecho.MaxwellLocalization.physicalCanonicalNet.toLightNetData.toLightOneParticle.K
        TGL.SpecificAQFT.rightWedge) := by
    rw [a_algebra_fisica_e_M]; exact hx
  let a : (physicalFockCertificate.R
      (F1Fecho.MaxwellLocalization.physicalCanonicalNet.toLightNetData.toLightOneParticle.K
        TGL.SpecificAQFT.rightWedge)).toStarSubalgebra := ⟨x, hx'⟩
  have ha : ∀ t : ℝ, physicalFockCertificate.flow t a = a := by
    intro t
    apply Subtype.ext
    have h := physicalFockCertificate.flow_is_Ad t a
    rw [h]
    ext v
    simp only [LinearIsometryEquiv.conjStarAlgEquiv_apply_apply]
    have := hxδ (-(2 * Real.pi * t)) ((gamma (B0 (-(2 * Real.pi * t)))).symm v)
    change (gamma (B0 (-(2 * Real.pi * t)))) (x ((gamma (B0 (-(2 * Real.pi * t)))).symm v)) = x v
    have h2 : VF (-(2 * Real.pi * t)) ((gamma (B0 (-(2 * Real.pi * t)))).symm v) = v :=
      LinearIsometryEquiv.apply_symm_apply _ _
    rw [h2] at this
    exact this
  exact TGLExt.LightRhoStar.centralizer_is_trivial physicalFockCertificate a ha

#print axioms t5_pelo_que_o_kernel_ja_tinha
