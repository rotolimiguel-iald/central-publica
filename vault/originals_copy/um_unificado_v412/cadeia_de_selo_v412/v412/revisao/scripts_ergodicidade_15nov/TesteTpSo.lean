import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Algebra.Algebra.Subalgebra.Basic
import Mathlib.Topology.Algebra.Module.Basic

/-! Revisor V_B1_a: a ergodicidade de UM so boost segue SEM a translacao Tm (`nullMinus`): o vacuo unico
so e pedido para a translacao que o boost encolhe. Enunciado e prova independentes da candidata. -/

set_option autoImplicit false
set_option maxHeartbeats 1000000

open Filter Topology
open scoped InnerProductSpace

namespace TesteTp

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H]

theorem nucleo {ι : Type*} (T : ℝ → H →L[ℂ] H) (r : ι → ℝ) (l : Filter ι) [l.NeBot]
    (hT : ∀ a v, ‖T a v‖ = ‖v‖) (h0 : ∀ v, T 0 v = v)
    (hcont : ∀ v, ContinuousAt (fun a => T a v) 0)
    (hr : Tendsto r l (𝓝 0)) (ξ : H)
    (hinv : ∀ i a, ⟪ξ, T a ξ⟫_ℂ = ⟪ξ, T (r i * a) ξ⟫_ℂ) (a : ℝ) :
    T a ξ = ξ := by
  have h1 : Tendsto (fun i => r i * a) l (𝓝 0) := by simpa using hr.mul_const a
  have h2 : Tendsto (fun i => T (r i * a) ξ) l (𝓝 (T 0 ξ)) := (hcont ξ).tendsto.comp h1
  have h3 : Tendsto (fun i => ⟪ξ, T (r i * a) ξ⟫_ℂ) l (𝓝 ⟪ξ, T 0 ξ⟫_ℂ) :=
    tendsto_const_nhds.inner h2
  have h4 : Tendsto (fun _ : ι => ⟪ξ, T a ξ⟫_ℂ) l (𝓝 ⟪ξ, T 0 ξ⟫_ℂ) :=
    h3.congr (fun i => (hinv i a).symm)
  have h5 : ⟪ξ, T a ξ⟫_ℂ = ⟪ξ, T 0 ξ⟫_ℂ := tendsto_nhds_unique tendsto_const_nhds h4
  have hval : ⟪ξ, T a ξ⟫_ℂ = ⟪ξ, ξ⟫_ℂ := by rw [h5, h0]
  have hre : RCLike.re ⟪T a ξ, ξ⟫_ℂ = ‖ξ‖ ^ 2 := by
    rw [inner_re_symm, hval, inner_self_eq_norm_sq]
  have hsq : ‖T a ξ - ξ‖ ^ 2 = 0 := by
    rw [@norm_sub_sq ℂ, hre, hT a ξ]; ring
  have hn : ‖T a ξ - ξ‖ = 0 := by simpa using hsq
  exact sub_eq_zero.mp (norm_eq_zero.mp hn)

theorem ergodico_de_uma_dilatacao_so_com_uma_translacao
    (U : H →L[ℂ] H) (T : ℝ → H →L[ℂ] H) (q : ℝ) (hq : |q| < 1)
    (hU : ∀ v w, ⟪U v, U w⟫_ℂ = ⟪v, w⟫_ℂ)
    (hT : ∀ a v, ‖T a v‖ = ‖v‖) (h0 : ∀ v, T 0 v = v)
    (hcont : ∀ v, ContinuousAt (fun a => T a v) 0)
    (hcov : ∀ a v, U (T a v) = T (q * a) (U v))
    (M : Subalgebra ℂ (H →L[ℂ] H)) (Ω : H)
    (hsep : ∀ x ∈ M, x Ω = 0 → x = 0) (hΩ : U Ω = Ω)
    (hvac : ∀ v : H, (∀ a, T a v = v) → ∃ c : ℂ, v = c • Ω)
    (x : H →L[ℂ] H) (hx : x ∈ M) (hxU : ∀ v, U (x v) = x (U v)) :
    ∃ c : ℂ, x = c • (1 : H →L[ℂ] H) := by
  have hfixx : U (x Ω) = x Ω := by rw [hxU Ω, hΩ]
  have hfixT : ∀ a, T a (x Ω) = x Ω := by
    intro a
    have passo : ∀ b, ⟪x Ω, T b (x Ω)⟫_ℂ = ⟪x Ω, T (q * b) (x Ω)⟫_ℂ := by
      intro b
      have h := hU (x Ω) (T b (x Ω))
      rw [hcov b (x Ω), hfixx] at h
      exact h.symm
    have hinv : ∀ (n : ℕ) (b : ℝ), ⟪x Ω, T b (x Ω)⟫_ℂ = ⟪x Ω, T (q ^ n * b) (x Ω)⟫_ℂ := by
      intro n
      induction n with
      | zero => intro b; simp
      | succ n ih =>
        intro b
        rw [ih b, passo (q ^ n * b)]
        congr 3
        ring
    exact nucleo T (fun n : ℕ => q ^ n) atTop hT h0 hcont
      (tendsto_pow_atTop_nhds_zero_of_abs_lt_one hq) (x Ω) hinv a
  obtain ⟨c, hc⟩ := hvac (x Ω) hfixT
  refine ⟨c, ?_⟩
  have hmem : x - c • (1 : H →L[ℂ] H) ∈ M := M.sub_mem hx (M.smul_mem M.one_mem c)
  have hz : (x - c • (1 : H →L[ℂ] H)) Ω = 0 := by simp [hc]
  exact sub_eq_zero.mp (hsep _ hmem hz)

end TesteTp

#print axioms TesteTp.ergodico_de_uma_dilatacao_so_com_uma_translacao
