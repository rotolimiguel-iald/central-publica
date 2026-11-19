import TGLExt.TheSameBetaReadsFourFaces
import TGLExt.PontoZeroDoPsion

open TGLExt TGLExt.PontoZeroDoPsion

namespace ReviewU2

/-- Exact modal reduction on one nonzero complex section. Both operators and the mode are inputs. -/
theorem modal_reduction {X : Type*} (D : ActionCouplingData X) (c : TGLCoupling)
    (ψ : X → ℂ) (hψ : ψ ≠ 0) (a k : ℝ)
    (hm : D.mass = 0) (hR : D.curvatureTerm ψ = 0)
    (hbox : D.boxOperator ψ = a • ψ) (hk : D.K_boundary ψ = k • ψ) :
    D.EOM c ψ ↔ a = c.beta * k := by
  change (D.boxOperator ψ - D.mass ^ 2 • ψ - D.xi • D.curvatureTerm ψ = c.beta • D.K_boundary ψ) ↔ _
  rw [hbox, hk, hm, hR, smul_smul]
  simp only [ne_eq, OfNat.ofNat_ne_zero, not_false_eq_true, zero_pow, zero_smul, smul_zero, sub_zero]
  exact ⟨fun h => smul_left_injective ℝ hψ h, fun h => congrArg (fun q : ℝ => q • ψ) h⟩

/-- At fixed unit, the missing eigenvalue is necessary and sufficient in that sector. -/
theorem psion_iff {a k u : ℝ} (c : TGLCoupling) (h : a = c.beta * k) :
    a = omegaSq c.beta (pagamentoComoCurvatura c.beta u) ↔ k = 2 * pagamentoComoCurvatura c.beta u := by
  rw [h]
  unfold omegaSq
  constructor
  · intro e
    apply mul_left_cancel₀ c.beta_pos.ne'
    calc c.beta * k = 2 * c.beta * pagamentoComoCurvatura c.beta u := e
         _ = c.beta * (2 * pagamentoComoCurvatura c.beta u) := by ring
  · intro e
    rw [e]
    ring

end ReviewU2

#print axioms ReviewU2.modal_reduction
#print axioms ReviewU2.psion_iff

