import TipoIIIControles

/-! Sonda D1 (revisor da terceira conferencia, 16/11/2026). So' leitura do kernel e das candidatas; nada instalado.
(1) os tipos, como o Lean os imprime; (2) nao vacuidade da unicidade; (3) a recusa do fluxo escalar junta com o
nucleo fator diz que o boost nao e' escalar no tempo 1; (4) a marca do estado no certificado fisico;
(5) a borda COMO CONJUNTO nao determina o observador (so' ponto a ponto). -/

set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace SondaD1

open TGLV350.Regular ORDEM016.D6 Vinculo F1Fecho.RegularCovariantCore MeasureTheory
open TGL.SpecificAQFT F1Rede.BosonicFock TGLExt.ImportedSQ
open F1Fecho.CanonicalFockRegular F1Fecho.PhysicalFockNet
open F1Fecho.OrbitalSpatial F1Fecho.SpacetimeLorentz F1Fecho.MaxwellLocalization K07.Horizon
open F1Fecho.Antilinear ChatgptAudit TGLExt
open F1Fecho.CanonicalFockModularCoreInputR1 (physicalFockCertificate)
open K07.TowerWedge TGLExt.ContratoQGv31
open Vinculo.Controles

#check @ORDEM016.D6.same_horizon_by_content_from_realizations
#check @ORDEM016.D6.identityByConstruction
#check @o_fluxo_e_a_conjugacao_de_tomita_sao_unicos
#check @o_fluxo_do_criterio_e_unico
#check @na_cunha_o_fluxo_do_criterio_e_o_boost
#check @dois_observadores_iguais_na_borda_sao_o_mesmo
#check @pair_tomita
#check @TGLExt.LightRhoStar.centralizer_is_trivial
#check @K07.TowerWedge.physical_no_flow_intertwining_embedding
#check @K07.Horizon.TransportCenter.maxwell_observer_wedge_type_III1
#print axioms ORDEM016.D6.same_horizon_by_content_from_realizations
#print axioms TGLExt.LightRhoStar.centralizer_is_trivial
#print axioms K07.TowerWedge.physical_no_flow_intertwining_embedding
#print axioms K07.Horizon.TransportCenter.maxwell_observer_wedge_type_III1

/-- (1) o reconhecimento identidade tem U = refl por definicao. -/
theorem identidade_tem_U_refl {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (M : StarSubalgebra ℂ (H →L[ℂ] H)) (omega : H) :
    (identityByConstruction M omega).U = LinearIsometryEquiv.refl ℂ H := rfl

/-- (2) nao vacuidade: ha' realizacao para a cunha e o vacuo (as hipoteses da unicidade sao habitadas). -/
theorem ha_realizacao_na_cunha : ∃ (J : F ≃ₛₗᵢ[starRingEnd ℂ] F) (B : UnitaryFlow F),
    PairTomitaAnalyticRealizationMeasured (net rightWedge).toStarSubalgebra vacuum J B.U :=
  ⟨canonicalFockJ, fockFlow, pair_tomita⟩

/-- (3) o boost nao age por escalar no tempo 1: a recusa do fluxo escalar e o nucleo fator, juntos. -/
theorem o_boost_nao_age_por_escalar_no_tempo_um (c : ℂ) :
    boostCLM fockFlow 1 ≠ c • (1 : F →L[ℂ] F) := by
  intro h
  refine fluxo_escalar_no_tempo_um_o_nucleo_nao_e_fator (net rightWedge) fockFlow
    ⟨vacuum, ?_⟩ c h o_centro_do_nucleo_da_cunha_e_escalar
  intro h0
  have hn := vacuum_norm
  rw [h0, norm_zero] at hn
  exact zero_ne_one hn

/-- (4a) a marca do estado, como o kernel a tem, no certificado fisico. -/
theorem marca_do_estado_no_certificado_fisico
    (a : wedgeAlgebra physicalFockCertificate)
    (ha : ∀ t : ℝ, physicalFockCertificate.flow t a = a) :
    ∃ c : ℂ, (a : physicalFockCertificate.F →L[ℂ] physicalFockCertificate.F) = c • 1 :=
  TGLExt.LightRhoStar.centralizer_is_trivial physicalFockCertificate a ha

/-- (5) a borda COMO CONJUNTO nao determina o observador: o boost da cunha (nao trivial) e' um observador do
Codex que leva a borda nela mesma. A unicidade vale so' ponto a ponto. -/
theorem a_borda_como_conjunto_nao_determina (s : ℝ) (hs : s ≠ 0) :
    ∃ L : generatedLorentz, L ≠ 1 ∧
      observerChart L 0 '' frontier rightWedge = frontier rightWedge := by
  have hmem : theBoost s ∈ generatedLorentz := Subgroup.subset_closure (Or.inr ⟨s, rfl⟩)
  have hfun : (⇑(observerChart ⟨theBoost s, hmem⟩ 0) : Point → Point) = wedgeBoostMap s := by
    funext x
    change (theBoost s).val.mulVec x + 0 = wedgeBoostMap s x
    rw [add_zero]
    rfl
  refine ⟨⟨theBoost s, hmem⟩, ?_, ?_⟩
  · intro h
    have h1 : (theBoost s) = (1 : LorentzGrp) := congrArg Subtype.val h
    have h2 : wedgeBoostMap s nullDir = nullDir := by
      have h3 : (theBoost s).val.mulVec nullDir = (1 : LorentzGrp).val.mulVec nullDir := by rw [h1]
      have h4 : (1 : LorentzGrp).val.mulVec nullDir = nullDir := by
        rw [lorentzGrp_one_val, Matrix.one_mulVec]
      exact h3.trans h4
    rw [wedgeBoostMap_nullDir] at h2
    have hcoord := congrFun h2 (0 : Fin 4)
    apply hs
    apply Real.exp_injective
    simpa [nullDir] using hcoord
  · rw [(observerChart ⟨theBoost s, hmem⟩ 0).image_frontier, hfun, FlagNet.boost_image_rightWedge]

#print axioms identidade_tem_U_refl
#print axioms ha_realizacao_na_cunha
#print axioms o_boost_nao_age_por_escalar_no_tempo_um
#print axioms marca_do_estado_no_certificado_fisico
#print axioms a_borda_como_conjunto_nao_determina

end SondaD1
