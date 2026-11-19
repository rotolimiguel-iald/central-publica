import PsionVacuoEModoDoTratado
import TGLExt.PontoDeContradicao
import TGLExt.NumberSelfAdjoint

namespace ReviewU6
open TGLExt TGLExt.PsionVacuoEModoDoTratado TGLExt.PontoZeroDoPsion
open F1Fecho.CanonicalFockModularCoreInputR1
open F1Rede.BosonicFock
open TGLExt.ThePsionAndTheViscosity TGLExt.ProjecaoTransversalDaMeiaNat

theorem concrete_vacuum_is_psion : psion physicalFockCertificate = vacuum := rfl

theorem concrete_vacuum_mode_level (c : TGLCoupling) (u : ℝ) (hu : 0 ≤ u) :
    osciladorDeDoisNiveis (Real.sqrt (omegaSq c.beta (pagamentoComoCurvatura c.beta u))) vacuum vacuum =
    ((neutrinoMassForm c u : ℝ) : ℂ) • vacuum :=
  no_oscilador_do_modo_o_psion_do_kernel_fica_na_forma_da_massa physicalFockCertificate c u hu

theorem exceptional_coupling_is_admissible : ∃ c : TGLCoupling, Real.sqrt 2 * c.beta = 1 := by
  have hpos : 0 < Real.sqrt 2 := Real.sqrt_pos.mpr (by norm_num)
  have hsq : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  refine ⟨⟨Real.sqrt 2 / 2, by positivity, by nlinarith⟩, ?_⟩
  change Real.sqrt 2 * (Real.sqrt 2 / 2) = 1
  nlinarith

noncomputable def shiftedNumber (ω : ℝ) (x : numberOp.domain) : ellTwo :=
  ((ω : ℂ) / 2) • (x : ellTwo) + (ω : ℂ) • numberOp x

theorem every_standard_level (ω : ℝ) (n : ℕ) :
    shiftedNumber ω ⟨inscriptions n, single_mem_numberDomain n⟩ =
      ((ω : ℂ) * ((n : ℂ) + 1/2)) • inscriptions n := by
  unfold shiftedNumber
  rw [numberOp_single, smul_smul, ← add_smul]
  congr 1
  ring

#print axioms concrete_vacuum_is_psion
#print axioms concrete_vacuum_mode_level
#print axioms exceptional_coupling_is_admissible
#print axioms every_standard_level
end ReviewU6

