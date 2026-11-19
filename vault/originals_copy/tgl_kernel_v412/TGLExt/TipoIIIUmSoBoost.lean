import TGLExt.TowerWedgeIndex
import TGLExt.ErgodicidadeDeMautner

set_option autoImplicit false
noncomputable section

/-!
# Um só número da Torre já lê o vácuo

`K07.TowerWedge.two_tower_boosts_read_vacuum` prova que um vetor fixo por DOIS boosts indexados pela Torre
está na reta do vácuo. `ErgodicidadeDeMautner` prova que UM boost não nulo basta.
Aqui os dois se encontram: a Torre, que é índice, não precisa de dois números para apontar o vácuo; um só,
desde que não nulo, aponta. A hipótese de dois boosts é, portanto, mais forte do que o necessário,
e a equivalência abaixo o diz por termo.

Depende de `ErgodicidadeDeMautner`, por isso fica em arquivo separado de
`TipoIIIControles`.
-/

namespace Vinculo.Controles

open TGLExt ChatgptAudit TGLExt.ImportedSQ TGLExt.ContratoQGv31 TGL.SpecificAQFT
open F1Fecho.CanonicalFockModularCoreInputR1 (physicalFockCertificate)
open K07.TowerWedge

/-- O primeiro número da Torre (nível 0, unidade (0,1)) não é zero. -/
theorem o_primeiro_numero_da_torre_nao_e_zero : rapidity mixProfile 0 0 1 ≠ 0 := by
  rw [first_mixed_rapidity]
  exact (Real.log_neg (by norm_num) (by norm_num)).ne

/-- ★ Um vetor fixo pelo boost de UM só número da Torre está na reta do vácuo. -/
theorem um_so_numero_da_torre_le_o_vacuo (v : physicalFockCertificate.F)
    (h : (lightBoost physicalFockCertificate).V (rapidity mixProfile 0 0 1) v = v) :
    v ∈ (ℂ ∙ physicalFockCertificate.Ω) := by
  obtain ⟨c, hc⟩ := (TGLExt.ErgodicidadeDeMautner.os_fixos_de_um_so_boost_da_luz_sao_a_reta_do_vacuo
    _ o_primeiro_numero_da_torre_nao_e_zero v).mp h
  exact Submodule.mem_span_singleton.mpr ⟨c, hc.symm⟩

/-- A hipótese de dois boosts equivale à de um só: o segundo número não acrescenta. -/
theorem dois_numeros_nao_acrescentam_a_um (v : physicalFockCertificate.F) :
    ((lightBoost physicalFockCertificate).V (rapidity mixProfile 0 0 1) v = v ∧
      (lightBoost physicalFockCertificate).V (rapidity mixProfile 1 (0,0) (0,1)) v = v) ↔
      (lightBoost physicalFockCertificate).V (rapidity mixProfile 0 0 1) v = v :=
  ⟨fun h => h.1, fun h =>
    (two_tower_boosts_read_vacuum physicalFockCertificate v).mpr (um_so_numero_da_torre_le_o_vacuo v h)⟩


end Vinculo.Controles
