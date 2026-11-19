import TGLExt.F1Fecho394.WedgeNonabelianR4
import TGLExt.F1Fecho394.BosonicFockGroupActions
import TGLExt.F1Fecho394.CanonicalWedgeFlowR2
import TGLExt.F1Fecho394.WedgeCyclicR3

/-! Revisor V_B1_a: o objeto `M` da candidata nao e trivial, e o caso s0 = 0 e mesmo falso
(a hipotese `s0 != 0` carrega peso). So kernel; nada importado da candidata. -/

set_option autoImplicit false
set_option maxHeartbeats 1000000

namespace TesteLuz

open F1Rede.BosonicFock F1Rede.BosonicFockGroupActions

/-- `M` (a algebra da cunha do fluxo) nao e feita so de escalares: ha dois elementos que nao comutam. -/
theorem M_nao_e_so_escalares :
    ¬ ∀ x ∈ F1Fecho.CanonicalWedgeFlow.M, ∃ c : ℂ, x = c • (1 : F →L[ℂ] F) := by
  intro h
  obtain ⟨a, ha, b, hb, hab⟩ := F1Fecho.WedgeNonabelian.wedge_nonabelian
  obtain ⟨c, hc⟩ := h a ha
  obtain ⟨d, hd⟩ := h b hb
  apply hab
  rw [hc, hd, smul_mul_smul_comm, smul_mul_smul_comm, mul_one, mul_comm c d]

/-- Com `s0 = 0` o enunciado dos fixos de um so boost e FALSO: `VF 0` e a identidade. -/
theorem s0_zero_os_fixos_nao_sao_o_vacuo :
    ¬ ∀ v : F, VF 0 v = v → ∃ c : ℂ, v = c • vacuum := by
  intro h
  apply M_nao_e_so_escalares
  intro x hx
  obtain ⟨d, hd⟩ := h (x vacuum) (by rw [VF_zero]; rfl)
  refine ⟨d, ?_⟩
  ext v
  obtain ⟨c, hc⟩ := h v (by rw [VF_zero]; rfl)
  rw [hc, map_smul, hd, ContinuousLinearMap.smul_apply, ContinuousLinearMap.one_apply, smul_smul,
    smul_smul, mul_comm]

/-- Com `s0 = 0` a ergodicidade de um so boost tambem e FALSA (todo `x` comuta com `VF 0`). -/
theorem s0_zero_a_ergodicidade_falha :
    ¬ ∀ x : F →L[ℂ] F, x ∈ F1Fecho.CanonicalWedgeFlow.M →
      (∀ v : F, VF 0 (x v) = x (VF 0 v)) → ∃ c : ℂ, x = c • (1 : F →L[ℂ] F) := by
  intro h
  apply M_nao_e_so_escalares
  intro x hx
  exact h x hx (fun v => by rw [VF_zero]; rfl)

end TesteLuz

#print axioms TesteLuz.M_nao_e_so_escalares
#print axioms TesteLuz.s0_zero_os_fixos_nao_sao_o_vacuo
#print axioms TesteLuz.s0_zero_a_ergodicidade_falha
