import TipoIIIControles

/-! Sonda T6 (revisor da conferencia de conserto, 16/11/2026). So' leitura do kernel e das candidatas; nada instalado.
(1) os tipos dos objetos do kernel e do Codex que os cinco termos novos da R2 usam, como o Lean os imprime;
(2) o parametro `s` de `a_borda_como_conjunto_nao_determina` e' mudo: o enunciado equivale ao existencial sem `s`;
(3) a forma que diz o que a docstring e o documento dizem: TODO boost da cunha leva a borda nela mesma, e boosts de
    parametros diferentes sao observadores diferentes;
(4) a marca do estado na MESMA lingua do criterio (algebra `net rightWedge`, relogio `fockFlow`). -/

set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace SondaT6

open TGLV350.Regular ORDEM016.D6 Vinculo F1Fecho.RegularCovariantCore MeasureTheory
open TGL.SpecificAQFT F1Rede.BosonicFock TGLExt.ImportedSQ
open F1Fecho.CanonicalFockRegular F1Fecho.PhysicalFockNet
open F1Fecho.OrbitalSpatial F1Fecho.SpacetimeLorentz F1Fecho.MaxwellLocalization K07.Horizon
open F1Fecho.Antilinear ChatgptAudit TGLExt
open F1Fecho.CanonicalFockModularCoreInputR1 (physicalFockCertificate)
open K07.TowerWedge TGLExt.ContratoQGv31
open Vinculo.Controles

/-! ## (1) tipos -/

#check @pair_tomita
#check @TGLExt.LightRhoStar.centralizer_is_trivial
#check @K07.Horizon.TransportCenter.maxwell_observer_wedge_type_III1
#check @FlagNet.boost_image_rightWedge
#check @F1Fecho.CanonicalFockModularCoreInputR1.physical_net
#check @ha_realizacao_na_cunha
#check @o_boost_nao_age_por_escalar_no_tempo_um
#check @marca_do_estado_no_certificado_fisico
#check @a_cunha_de_todo_observador_cumpre_o_criterio_do_nucleo
#check @a_borda_como_conjunto_nao_determina
#check @theBoost
#check @wedgeBoostMap_nullDir
#check @fockFlow
#check @net_wedge_eq

open Lean Elab Command in
#eval show CommandElabM Unit from do
  let env ← getEnv
  for c in [``TGLExt.LightRhoStar.centralizer_is_trivial, ``F1Fecho.PhysicalFockNet.pair_tomita,
      ``K07.Horizon.TransportCenter.maxwell_observer_wedge_type_III1, ``FlagNet.boost_image_rightWedge,
      ``F1Fecho.CanonicalFockModularCoreInputR1.physicalFockCertificate,
      ``K07.PhysicalCoreCenter.physical_core_is_factor, ``Vinculo.maxwell_right_wedge_type_III1,
      ``ORDEM016.D6.same_horizon_by_content_from_realizations, ``K07.TowerWedge.wedgeAlgebra] do
    match env.getModuleIdxFor? c with
    | some idx => logInfo m!"MODULO {c} : {env.header.moduleNames[idx.toNat]!}"
    | none => logInfo m!"MODULO {c} : (este arquivo)"

/-! ## (2) o `s` do enunciado adotado e' mudo -/

/-- O enunciado adotado (`∀ s ≠ 0, ∃ L ≠ 1, ...`) equivale ao existencial sem `s`: a conclusao nao fala de `s`. -/
theorem enunciado_adotado_equivale_ao_sem_s :
    (∀ s : ℝ, s ≠ 0 → ∃ L : generatedLorentz, L ≠ 1 ∧
        observerChart L 0 '' frontier rightWedge = frontier rightWedge) ↔
      (∃ L : generatedLorentz, L ≠ 1 ∧
        observerChart L 0 '' frontier rightWedge = frontier rightWedge) :=
  ⟨fun h => h 1 one_ne_zero, fun h _ _ => h⟩

/-! ## (3) a forma que diz o que a docstring diz -/

/-- TODO boost da cunha e' um observador do Codex que leva a borda nela mesma. -/
theorem todo_boost_da_cunha_leva_a_borda_nela_mesma (s : ℝ) :
    ∃ h : theBoost s ∈ generatedLorentz,
      observerChart ⟨theBoost s, h⟩ 0 '' frontier rightWedge = frontier rightWedge := by
  have hmem : theBoost s ∈ generatedLorentz := Subgroup.subset_closure (Or.inr ⟨s, rfl⟩)
  have hfun : (⇑(observerChart ⟨theBoost s, hmem⟩ 0) : Point → Point) = wedgeBoostMap s := by
    funext x
    change (theBoost s).val.mulVec x + 0 = wedgeBoostMap s x
    rw [add_zero]
    rfl
  refine ⟨hmem, ?_⟩
  rw [(observerChart ⟨theBoost s, hmem⟩ 0).image_frontier, hfun, FlagNet.boost_image_rightWedge]

/-- Boosts de parametros diferentes sao transformacoes de Lorentz diferentes (em particular, so' o de parametro
zero e' a identidade): ha' uma familia a um parametro de observadores distintos com a mesma borda. -/
theorem boosts_de_parametros_diferentes_sao_diferentes (s t : ℝ) (h : theBoost s = theBoost t) : s = t := by
  have h3 : (theBoost s).val.mulVec nullDir = (theBoost t).val.mulVec nullDir := by rw [h]
  have h2 : wedgeBoostMap s nullDir = wedgeBoostMap t nullDir := h3
  rw [wedgeBoostMap_nullDir, wedgeBoostMap_nullDir] at h2
  have hcoord := congrFun h2 (0 : Fin 4)
  apply Real.exp_injective
  simpa [nullDir] using hcoord

/-! ## (4) a marca do estado na lingua do criterio -/

/-- A marca do ESTADO escrita com os MESMOS objetos do criterio do nucleo: a algebra e' `net rightWedge` e o
relogio e' `fockFlow` (o fluxo do predicado). O que a conjugacao pelo relogio deixa parado, na algebra da cunha,
e' multiplo do Um. Sai do teorema do kernel pelas igualdades por construcao do certificado fisico. -/
theorem marca_do_estado_na_lingua_do_criterio (a : F →L[ℂ] F) (ha : a ∈ net rightWedge)
    (hfix : ∀ t : ℝ, (fockFlow.U t).conjStarAlgEquiv a = a) :
    ∃ c : ℂ, a = c • (1 : F →L[ℂ] F) := by
  have ha' : a ∈ (wedgeAlgebra physicalFockCertificate) := ha
  exact marca_do_estado_no_certificado_fisico ⟨a, ha'⟩ (fun t => by
    apply Subtype.ext
    rw [physicalFockCertificate.flow_is_Ad t ⟨a, ha'⟩]
    exact hfix t)

#print axioms enunciado_adotado_equivale_ao_sem_s
#print axioms todo_boost_da_cunha_leva_a_borda_nela_mesma
#print axioms boosts_de_parametros_diferentes_sao_diferentes
#print axioms marca_do_estado_na_lingua_do_criterio

end SondaT6
