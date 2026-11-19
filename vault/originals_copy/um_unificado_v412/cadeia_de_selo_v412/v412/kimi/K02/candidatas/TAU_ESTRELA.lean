import Mathlib

/-!
Candidata K02/τ★: somente álgebra dimensional da lei de dephasing.
Nenhuma escala física é derivada; `ħ`, `u` e `τ` são entradas.
-/

namespace K02.Tau

/-- Lei declarada Γω = ½ β τ ω². -/
noncomputable def Gamma (β τ ω : ℝ) : ℝ := (1 / 2) * β * τ * ω ^ 2

/-- [REAL no sandbox] Rescala de τ rescala Γ; a forma não escolhe τ★. -/
theorem gamma_rescales (β τ ω r : ℝ) :
    Gamma β (r * τ) ω = r * Gamma β τ ω := by
  unfold Gamma
  all_goals ring

/-- [DERIVED sob entradas não nulas] A leitura autoconsistente fixa a
FREQUÊNCIA em função de τ★, não τ★ nem a unidade. -/
theorem self_consistent_readout_fixes_frequency (ħ τ ω : ℝ)
    (H_hbar_ne : ħ ≠ 0) (H_tau_ne : τ ≠ 0) (H_omega_ne : ω ≠ 0)
    (H : ħ * ω = ħ * ((1 / 2) * τ * ω ^ 2)) : ω = 2 / τ := by
  have h1 : ω = (1 / 2) * τ * ω ^ 2 := mul_left_cancel₀ H_hbar_ne H
  have h2 : ω * (1 - (1 / 2) * τ * ω) = 0 := by linear_combination h1
  rcases mul_eq_zero.mp h2 with h0 | h0
  · exact absurd h0 H_omega_ne
  · rw [eq_div_iff H_tau_ne]
    linear_combination (-2 : ℝ) * h0

/-- [DERIVED algébrico] Para τ = ħ/u e ω = u/ħ, resta Γ = βu/(2ħ). -/
theorem gamma_of_gap_time (β ħ u : ℝ) (H_hbar_ne : ħ ≠ 0) (H_u_ne : u ≠ 0) :
    Gamma β (ħ / u) (u / ħ) = β * u / (2 * ħ) := by
  unfold Gamma
  field_simp [H_hbar_ne, H_u_ne]
  all_goals ring

/-- [DERIVED algébrico] Para τ = ħ/(βu) e ω = u/ħ, β cancela:
Γ = u/(2ħ) = ω/2. Isto não deriva u nem identifica τ★. -/
theorem gamma_of_retained_time (β ħ u : ℝ)
    (H_beta_ne : β ≠ 0) (H_hbar_ne : ħ ≠ 0) (H_u_ne : u ≠ 0) :
    Gamma β (ħ / (β * u)) (u / ħ) = u / (2 * ħ) := by
  unfold Gamma
  field_simp [H_beta_ne, H_hbar_ne, H_u_ne]
  all_goals ring

#print axioms K02.Tau.gamma_rescales
#print axioms K02.Tau.self_consistent_readout_fixes_frequency
#print axioms K02.Tau.gamma_of_gap_time
#print axioms K02.Tau.gamma_of_retained_time

end K02.Tau
