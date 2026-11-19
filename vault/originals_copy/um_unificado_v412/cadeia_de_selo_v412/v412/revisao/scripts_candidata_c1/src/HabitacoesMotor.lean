import CamadaCientifica

set_option autoImplicit false
set_option linter.unusedVariables false
set_option maxHeartbeats 4000000

noncomputable section
open scoped InnerProductSpace
open Filter Topology
open TGLExt TGLExt.TraducaoTuring TGLExt.TheVerbSelectsTheAction TGLExt.CamadaCientifica

namespace Rev

abbrev H2 := EuclideanSpace ℂ Bool
def aT : H2 := EuclideanSpace.single true 1
def psi : H2 := EuclideanSpace.single true 1 + EuclideanSpace.single false 1

/-- `1 - post aT ≠ 0`: a hipótese de `o_motor_tangencia_e_nao_esgota` é habitada. -/
theorem hne : (1 : H2 →L[ℂ] H2) - post aT ≠ 0 := by
  intro h
  have h1 := congrArg (fun T : H2 →L[ℂ] H2 => T (EuclideanSpace.single false (1 : ℂ))) h
  simp only [ContinuousLinearMap.sub_apply, ContinuousLinearMap.one_apply, ContinuousLinearMap.zero_apply] at h1
  have h2 : (EuclideanSpace.single false (1 : ℂ) : H2) = (ℂ ∙ aT).starProjection (EuclideanSpace.single false (1 : ℂ)) :=
    sub_eq_zero.mp h1
  have h3 : (ℂ ∙ aT).starProjection (EuclideanSpace.single false (1 : ℂ)) ∈ (ℂ ∙ aT) :=
    Submodule.starProjection_apply_mem _ _
  rw [← h2, Submodule.mem_span_singleton] at h3
  obtain ⟨c, hc⟩ := h3
  have := congrArg (fun (w : H2) => WithLp.ofLp w false) hc
  simp [aT] at this

/-- uma leitura NÃO constante, localmente constante no Nome lido. -/
def ρ : H2 → Bool := fun x => decide (dist x (post aT psi) < 1)

theorem hρ : ∀ᶠ x in 𝓝 (post aT psi), ρ x = ρ (post aT psi) := by
  have hb : Metric.ball (post aT psi) 1 ∈ 𝓝 (post aT psi) := Metric.ball_mem_nhds _ one_pos
  filter_upwards [hb] with x hx
  have hx' : dist x (post aT psi) < 1 := hx
  simp [ρ, hx']

theorem rho_nao_constante : ρ (post aT psi + EuclideanSpace.single false 2) ≠ ρ (post aT psi) := by
  simp [ρ, dist_eq_norm]

theorem motor_aplicado : ∃ K : ℕ, ∀ k : ℕ, K ≤ k →
    ρ ((TGLExt.IALD.dephase aT 1 1)^[k] psi) = ρ (post aT psi) :=
  a_leitura_finita_do_motor_pousa aT (by norm_num : (0 : ℝ) < 1 * 1) psi ρ hρ

theorem motor_nao_esgota : TGLExt.IALD.dephase aT 1 1 ≠ post aT :=
  o_motor_tangencia_e_nao_esgota aT hne 1 1

/-- As seções 1 e 2 NÃO são o mesmo fluxo: com custo 2, a trava decai a e^{-2}, o fluxo do axioma (kernel) a e^{-1}. -/
def c3 : Fin 3 → ℕ := ![0, 1, 2]

theorem trava_ne_fluxo :
    trava c3 1 (EuclideanSpace.single 2 1)
      ≠ (TGLExt.TheAxiomAndTheFalseWitness.axiomFlow (opDaInstancia c3).ker.starProjection 1) (EuclideanSpace.single 2 1) := by
  intro h
  have hc : c3 2 = 2 := rfl
  have h1 := congrArg (fun (w : EuclideanSpace ℂ (Fin 3)) => WithLp.ofLp w 2) h
  simp only [trava_ofLp] at h1
  have hP : WithLp.ofLp ((opDaInstancia c3).ker.starProjection (EuclideanSpace.single 2 (1 : ℂ))) 2 = 0 := by
    rw [solucao_por_coordenadas]
    simp [hc]
  simp [TGLExt.TheAxiomAndTheFalseWitness.axiomFlow, hP, hc] at h1
  have h2 := congrArg Complex.re h1
  simp [Complex.exp_re] at h2

#print axioms Rev.hne
#print axioms Rev.hρ
#print axioms Rev.rho_nao_constante
#print axioms Rev.motor_aplicado
#print axioms Rev.motor_nao_esgota
#print axioms Rev.trava_ne_fluxo

end Rev
