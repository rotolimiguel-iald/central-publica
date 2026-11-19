import Mathlib

/-!
Candidata K05/τ★ R2. Prova somente dimensão e álgebra explícitas.
Não deriva uma âncora física, não escolhe `c★`, não identifica a Meia-Nat
com entropia de Bekenstein–Hawking e não identifica `τ` com `tempoDoRetido`.
-/

namespace K05.Tau

/-- Em dimensões `(M,L,T)`, `ħ` tem `(1,2,-1)` e `c` tem `(0,1,-1)`.
As três equações pedem que `ħ^a c^b` seja um tempo; são incompatíveis. -/
theorem no_time_from_hbar_c (a b : ℚ)
    (hM : a = 0) (hL : 2 * a + b = 0) (hT : -a - b = 1) : False := by
  linarith

/-- `G` tem `(-1,3,-2)`. Os expoentes de `ħ^a G^b c^d` com dimensão
 de tempo são unicamente `(1/2,1/2,-5/2)`. -/
theorem unique_planck_exponents (a b d : ℚ)
    (hM : a - b = 0) (hL : 2 * a + 3 * b + d = 0)
    (hT : -a - 2 * b - d = 1) :
    a = 1 / 2 ∧ b = 1 / 2 ∧ d = -5 / 2 := by
  refine ⟨?_, ?_, ?_⟩ <;> linarith

noncomputable def planckEnergy (ħ c G : ℝ) : ℝ := Real.sqrt (ħ * c ^ 5 / G)
noncomputable def planckTime (ħ c G : ℝ) : ℝ := ħ / planckEnergy ħ c G

theorem planckEnergy_pos {ħ c G : ℝ} (hħ : 0 < ħ) (hc : 0 < c) (hG : 0 < G) :
    0 < planckEnergy ħ c G := by
  unfold planckEnergy
  positivity

theorem planckEnergy_ne {ħ c G : ℝ} (hħ : 0 < ħ) (hc : 0 < c) (hG : 0 < G) :
    planckEnergy ħ c G ≠ 0 := (planckEnergy_pos hħ hc hG).ne'

theorem planckEnergy_sq {ħ c G : ℝ} (hħ : 0 < ħ) (hc : 0 < c) (hG : 0 < G) :
    (planckEnergy ħ c G) ^ 2 = ħ * c ^ 5 / G := by
  unfold planckEnergy
  rw [Real.sq_sqrt]
  positivity

theorem planckTime_mul_planckEnergy {ħ c G : ℝ}
    (hħ : 0 < ħ) (hc : 0 < c) (hG : 0 < G) :
    planckTime ħ c G * planckEnergy ħ c G = ħ := by
  unfold planckTime
  field_simp [planckEnergy_ne hħ hc hG]

theorem planckTime_sq {ħ c G : ℝ} (hħ : 0 < ħ) (hc : 0 < c) (hG : 0 < G) :
    (planckTime ħ c G) ^ 2 = ħ * G / c ^ 5 := by
  have hE := planckEnergy_ne hħ hc hG
  have hE2 := planckEnergy_sq hħ hc hG
  unfold planckTime
  rw [div_pow, hE2]
  field_simp [hħ.ne', hc.ne', hG.ne']

/-- Com `u` posto, `N=E_P/u` é o número puro que mede a mesma razão
que a âncora de Planck: `ħ/u = N·t_P`. -/
theorem gap_time_is_dimensionless_ratio_mul_planck (ħ c G u : ℝ)
    (hħ : 0 < ħ) (hc : 0 < c) (hG : 0 < G) (hu : 0 < u) :
    ħ / u = (planckEnergy ħ c G / u) * planckTime ħ c G := by
  unfold planckTime
  field_simp [planckEnergy_ne hħ hc hG, hu.ne']

/-- O tempo do retido é outro múltiplo de Planck, `(N/β)·t_P`;
não se identifica aqui esse tempo com o `τ★` do relógio. -/
theorem retained_time_is_dimensionless_ratio_mul_planck (β ħ c G u : ℝ)
    (hβ : 0 < β) (hħ : 0 < ħ) (hc : 0 < c) (hG : 0 < G) (hu : 0 < u) :
    ħ / (β * u) = (planckEnergy ħ c G / (β * u)) * planckTime ħ c G := by
  unfold planckTime
  field_simp [planckEnergy_ne hħ hc hG, hβ.ne', hu.ne']

/-- Fixados `ħ,c,u`, medir `G` ou medir `N=E_P/u` é a mesma informação. -/
theorem newton_eq_of_dimensionless_ratio (ħ c G u N : ℝ)
    (hħ : 0 < ħ) (hc : 0 < c) (hG : 0 < G) (hu : 0 < u) (hN : 0 < N)
    (h : N * u = planckEnergy ħ c G) :
    G = ħ * c ^ 5 / (N ^ 2 * u ^ 2) := by
  have hE2 := planckEnergy_sq hħ hc hG
  have h3 : G * (N * u) ^ 2 = ħ * c ^ 5 := by
    rw [h]
    have h4 := (eq_div_iff hG.ne').mp hE2
    nlinarith
  rw [eq_div_iff (mul_ne_zero (pow_ne_zero 2 hN.ne') (pow_ne_zero 2 hu.ne'))]
  calc
    G * (N ^ 2 * u ^ 2) = G * (N * u) ^ 2 := by ring
    _ = ħ * c ^ 5 := h3

/-- A recíproca: o número puro `N` reconstrói `E_P/u` quando `G` tem
a forma acima. -/
theorem dimensionless_ratio_eq_of_newton (ħ c G u N : ℝ)
    (hħ : 0 < ħ) (hc : 0 < c) (hG : 0 < G) (hu : 0 < u) (hN : 0 < N)
    (h : G = ħ * c ^ 5 / (N ^ 2 * u ^ 2)) :
    N * u = planckEnergy ħ c G := by
  have hNu : 0 ≤ N * u := (mul_pos hN hu).le
  have hE : 0 ≤ planckEnergy ħ c G := (planckEnergy_pos hħ hc hG).le
  have hsq : (N * u) ^ 2 = (planckEnergy ħ c G) ^ 2 := by
    rw [planckEnergy_sq hħ hc hG, h]
    field_simp [hħ.ne', hc.ne', hN.ne', hu.ne']
  nlinarith [sq_nonneg (N * u - planckEnergy ħ c G),
    sq_nonneg (N * u + planckEnergy ħ c G), mul_nonneg hNu hE]

/-- A hipótese física `S=A/(4ℓ_P²)` com `S=½` fornece apenas `A=2ℓ_P²`. -/
theorem half_nat_cell_area (A ell : ℝ) (hell : ell ≠ 0)
    (h : (1 / 2 : ℝ) = A / (4 * ell ^ 2)) : A = 2 * ell ^ 2 := by
  field_simp [hell] at h
  linarith

theorem sqrt_half_nat_cell_area {ell : ℝ} (hell : 0 ≤ ell) :
    Real.sqrt (2 * ell ^ 2) = Real.sqrt 2 * ell := by
  have h2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hs : 2 * ell ^ 2 = (Real.sqrt 2 * ell) ^ 2 := by
    rw [mul_pow, h2]
  rw [hs, Real.sqrt_sq (mul_nonneg (Real.sqrt_nonneg 2) hell)]

/-- Sob a hipótese ADICIONAL de célula quadrada e travessia de luz,
`A=2ℓ_P²` dá `τ=√2·(ℓ_P/c)`. Área sozinha não fornece essa travessia. -/
theorem half_nat_square_light_crossing (A ell c : ℝ)
    (hell : 0 < ell) (hc : 0 < c) (hA : A = 2 * ell ^ 2) :
    Real.sqrt A / c = Real.sqrt 2 * (ell / c) := by
  rw [hA, sqrt_half_nat_cell_area hell.le]
  ring

/-- Se `ℓ_P/c=t_P`, a travessia acima é `√2·t_P`, não um teorema
sobre a dispersão do psíon. -/
theorem half_nat_square_light_crossing_planck (A ell c tP : ℝ)
    (hell : 0 < ell) (hc : 0 < c) (hA : A = 2 * ell ^ 2)
    (htP : tP = ell / c) : Real.sqrt A / c = Real.sqrt 2 * tP := by
  rw [half_nat_square_light_crossing A ell c hell hc hA, htP]

noncomputable def Gamma (β τ ω : ℝ) : ℝ := (1 / 2) * β * τ * ω ^ 2

/-- A leitura `Γ=ω` da lei canônica, COM β, fixa `ω=2/(βτ)`. -/
theorem canonical_readout_fixes_frequency (β ħ τ ω : ℝ)
    (hβ : β ≠ 0) (hħ : ħ ≠ 0) (hτ : τ ≠ 0) (hω : ω ≠ 0)
    (h : ħ * ω = ħ * ((1 / 2) * β * τ * ω ^ 2)) : ω = 2 / (β * τ) := by
  have h1 : ω = (1 / 2) * β * τ * ω ^ 2 := mul_left_cancel₀ hħ h
  have h2 : ω * (1 - (1 / 2) * β * τ * ω) = 0 := by linear_combination h1
  rcases mul_eq_zero.mp h2 with h0 | h0
  · exact absurd h0 hω
  · rw [eq_div_iff (mul_ne_zero hβ hτ)]
    linear_combination (-2 : ℝ) * h0

/-- No monopolo, `E=ħω` muda a lei de `ω²` para `ω³`. -/
theorem monopole_gamma_is_cubic (β G ħ c ω : ℝ) :
    Gamma β (4 * Real.pi * G * (ħ * ω) / c ^ 5) ω
      = (2 * Real.pi * β * G * ħ / c ^ 5) * ω ^ 3 := by
  unfold Gamma
  ring

/-- Candidata de seleção, não derivação: piso de Planck com horizonte próprio. -/
noncomputable def tauMax (tP tauHorizon : ℝ) : ℝ := max tP tauHorizon

theorem tauMax_local {tP tauHorizon : ℝ} (h : tauHorizon ≤ tP) :
    tauMax tP tauHorizon = tP := max_eq_left h

theorem tauMax_horizon {tP tauHorizon : ℝ} (h : tP ≤ tauHorizon) :
    tauMax tP tauHorizon = tauHorizon := max_eq_right h

#print axioms K05.Tau.no_time_from_hbar_c
#print axioms K05.Tau.unique_planck_exponents
#print axioms K05.Tau.planckTime_mul_planckEnergy
#print axioms K05.Tau.planckTime_sq
#print axioms K05.Tau.gap_time_is_dimensionless_ratio_mul_planck
#print axioms K05.Tau.retained_time_is_dimensionless_ratio_mul_planck
#print axioms K05.Tau.newton_eq_of_dimensionless_ratio
#print axioms K05.Tau.dimensionless_ratio_eq_of_newton
#print axioms K05.Tau.half_nat_cell_area
#print axioms K05.Tau.half_nat_square_light_crossing_planck
#print axioms K05.Tau.canonical_readout_fixes_frequency
#print axioms K05.Tau.monopole_gamma_is_cubic
#print axioms K05.Tau.tauMax_local
#print axioms K05.Tau.tauMax_horizon

end K05.Tau
