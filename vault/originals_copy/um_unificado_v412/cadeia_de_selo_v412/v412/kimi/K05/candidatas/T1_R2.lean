import Mathlib

/-!
Candidata K05/T1, rodada 2: face finita espectral da média gaussiana.

Trabalhamos em `M_n(ℂ)`, numa base na qual `K = diagonal k`, com `k i ≥ 0`.
A fórmula provada é a da função característica gaussiana:
`Φ_t(x)ᵢⱼ = exp(-β t (√kᵢ - √kⱼ)²/2) xᵢⱼ`.
O pinching conserva blocos de autovalores repetidos. Nenhum enunciado sobre
produtos cruzados, álgebras de von Neumann infinitas ou ergodicidade da cunha
é feito aqui.
-/

namespace K05.T1

open Filter Matrix
open scoped Topology ComplexOrder

noncomputable section

set_option autoImplicit false

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- O gerador positivo na base espectral escolhida. -/
def diagonalK (k : n → ℝ) : Matrix n n ℂ :=
  Matrix.diagonal (fun i => (k i : ℂ))

/-- O multiplicador escalar da função característica de `N(0, βt)`. -/
noncomputable def modalDecay (β δ t : ℝ) : ℝ :=
  Real.exp ((-β * δ ^ 2 / 2) * t)

/-- A face finita da mistura gaussiana, escrita entrada a entrada. -/
noncomputable def gaussianFlow (β t : ℝ) (k : n → ℝ)
    (x : Matrix n n ℂ) : Matrix n n ℂ :=
  fun i j => (modalDecay β (Real.sqrt (k i) - Real.sqrt (k j)) t : ℂ) * x i j

/-- O pinching nos autoespaços: blocos inteiros sobrevivem à degenerescência. -/
def pinching (k : n → ℝ) (x : Matrix n n ℂ) : Matrix n n ℂ :=
  fun i j => if k i = k j then x i j else 0

@[simp] theorem gaussianFlow_apply (β t : ℝ) (k : n → ℝ)
    (x : Matrix n n ℂ) (i j : n) :
    gaussianFlow β t k x i j =
      (modalDecay β (Real.sqrt (k i) - Real.sqrt (k j)) t : ℂ) * x i j := rfl

@[simp] theorem pinching_apply (k : n → ℝ) (x : Matrix n n ℂ) (i j : n) :
    pinching k x i j = if k i = k j then x i j else 0 := rfl

/-- A fórmula é exatamente a taxa pedida, com `t` dentro do expoente. -/
theorem gaussianFlow_entry_formula (β t : ℝ) (k : n → ℝ)
    (x : Matrix n n ℂ) (i j : n) :
    gaussianFlow β t k x i j =
      (Real.exp (-β * t * (Real.sqrt (k i) - Real.sqrt (k j)) ^ 2 / 2) : ℂ) *
        x i j := by
  simp only [gaussianFlow_apply, modalDecay]
  congr 3
  ring

theorem diagonalK_isHermitian (k : n → ℝ) : (diagonalK k).IsHermitian := by
  apply Matrix.isHermitian_diagonal_of_self_adjoint
  funext i
  simp

theorem diagonalK_posSemidef (k : n → ℝ) (H_K_nonneg : ∀ i, 0 ≤ k i) :
    (diagonalK k).PosSemidef := by
  apply Matrix.PosSemidef.diagonal
  intro i
  change (0 : ℂ) ≤ (k i : ℂ)
  exact_mod_cast H_K_nonneg i

/-- Comutar com a diagonal é precisamente anular entradas entre autovalores
 diferentes. -/
theorem diagonalK_commute_iff (k : n → ℝ) (x : Matrix n n ℂ) :
    Commute (diagonalK k) x ↔ ∀ i j, k i ≠ k j → x i j = 0 := by
  constructor
  · intro h i j H_kij
    have he : ((k i : ℂ) - (k j : ℂ)) * x i j = 0 := by
      calc
        ((k i : ℂ) - (k j : ℂ)) * x i j =
            (diagonalK k * x) i j - (x * diagonalK k) i j := by
              simp [diagonalK, Matrix.diagonal_mul, Matrix.mul_diagonal, sub_mul, mul_sub, mul_comm]
        _ = 0 := sub_eq_zero.mpr (Matrix.ext_iff.mpr h.eq i j)
    exact (mul_eq_zero.mp he).resolve_left
      (sub_ne_zero.mpr (fun hc => H_kij (Complex.ofReal_injective hc)))
  · intro h
    show diagonalK k * x = x * diagonalK k
    ext i j
    by_cases H_kij : k i = k j
    · simp [diagonalK, Matrix.diagonal_mul, Matrix.mul_diagonal, H_kij, mul_comm]
    · simp [diagonalK, Matrix.diagonal_mul, Matrix.mul_diagonal, h i j H_kij]

theorem pinching_eq_self_iff (k : n → ℝ) (x : Matrix n n ℂ) :
    pinching k x = x ↔ Commute (diagonalK k) x := by
  rw [diagonalK_commute_iff]
  constructor
  · intro h i j H_kij
    have he := Matrix.ext_iff.mpr h i j
    simpa [pinching_apply, H_kij] using he.symm
  · intro h
    ext i j
    by_cases H_kij : k i = k j
    · simp [pinching_apply, H_kij]
    · simp [pinching_apply, H_kij, h i j H_kij]

/-- Para `βt > 0`, o multiplicador só vale um quando a diferença é nula. -/
theorem modalDecay_eq_one_iff (β δ t : ℝ) (H_beta_pos : 0 < β) (H_t_pos : 0 < t) :
    modalDecay β δ t = 1 ↔ δ = 0 := by
  constructor
  · intro h
    have hz := (Real.exp_eq_one_iff _).mp h
    by_contra H_delta
    have hs : 0 < δ ^ 2 := sq_pos_of_ne_zero H_delta
    have hc : -β * δ ^ 2 / 2 < 0 := by nlinarith
    have hp : (-β * δ ^ 2 / 2) * t < 0 := mul_neg_of_neg_of_pos hc H_t_pos
    linarith
  · intro h
    subst δ
    simp [modalDecay]

/-- Todo modo não nulo decai; o modo nulo permanece. -/
theorem tendsto_modalDecay (β δ : ℝ) (H_beta_pos : 0 < β) :
    Tendsto (modalDecay β δ) atTop (𝓝 (if δ = 0 then 1 else 0)) := by
  change Tendsto (fun t : ℝ => Real.exp ((-β * δ ^ 2 / 2) * t)) atTop
    (𝓝 (if δ = 0 then 1 else 0))
  by_cases H_delta_zero : δ = 0
  · subst δ
    simpa using (tendsto_const_nhds : Tendsto (fun _ : ℝ => (1 : ℝ)) atTop (𝓝 1))
  · have H_delta_sq_pos : 0 < δ ^ 2 := sq_pos_of_ne_zero H_delta_zero
    have H_coef_neg : -β * δ ^ 2 / 2 < 0 := by nlinarith
    have H_linear : Tendsto (fun t : ℝ => (-β * δ ^ 2 / 2) * t) atTop atBot :=
      tendsto_id.const_mul_atTop_of_neg H_coef_neg
    have H_exp := Real.tendsto_exp_atBot.comp H_linear
    rw [if_neg H_delta_zero]
    change Tendsto (Real.exp ∘ fun t : ℝ => (-β * δ ^ 2 / 2) * t) atTop (𝓝 0)
    exact H_exp

/-- O setor fixo de uma mistura não trivial é o comutante de `K`. -/
theorem fixed_gaussianFlow_iff (β t : ℝ) (k : n → ℝ) (x : Matrix n n ℂ)
    (H_beta_pos : 0 < β) (H_t_pos : 0 < t) (H_K_nonneg : ∀ i, 0 ≤ k i) :
    gaussianFlow β t k x = x ↔ Commute (diagonalK k) x := by
  rw [diagonalK_commute_iff]
  constructor
  · intro h i j H_kij
    have he := Matrix.ext_iff.mpr h i j
    change (modalDecay β (Real.sqrt (k i) - Real.sqrt (k j)) t : ℂ) * x i j = x i j at he
    have hs : Real.sqrt (k i) - Real.sqrt (k j) ≠ 0 := by
      apply sub_ne_zero.mpr
      intro hs
      exact H_kij ((Real.sqrt_inj (H_K_nonneg i) (H_K_nonneg j)).mp hs)
    have hm : modalDecay β (Real.sqrt (k i) - Real.sqrt (k j)) t ≠ 1 := by
      intro hm
      exact hs ((modalDecay_eq_one_iff _ _ _ H_beta_pos H_t_pos).mp hm)
    have hc : ((modalDecay β (Real.sqrt (k i) - Real.sqrt (k j)) t : ℝ) : ℂ) ≠ 1 := by
      exact_mod_cast hm
    have hf : (((modalDecay β (Real.sqrt (k i) - Real.sqrt (k j)) t : ℝ) : ℂ) - 1) *
        x i j = 0 := by
      rw [sub_mul, one_mul, he, sub_self]
    exact (mul_eq_zero.mp hf).resolve_left (sub_ne_zero.mpr hc)
  · intro h
    ext i j
    by_cases H_kij : k i = k j
    · have hs : Real.sqrt (k i) - Real.sqrt (k j) = 0 := sub_eq_zero.mpr (congrArg _ H_kij)
      simp [gaussianFlow_apply, modalDecay, hs]
    · simp [gaussianFlow_apply, h i j H_kij]

/-- Forma equivalente do setor fixo: os elementos fixos pelo pinching. -/
theorem fixed_gaussianFlow_iff_pinching (β t : ℝ) (k : n → ℝ) (x : Matrix n n ℂ)
    (H_beta_pos : 0 < β) (H_t_pos : 0 < t) (H_K_nonneg : ∀ i, 0 ≤ k i) :
    gaussianFlow β t k x = x ↔ pinching k x = x := by
  rw [pinching_eq_self_iff, fixed_gaussianFlow_iff β t k x H_beta_pos H_t_pos H_K_nonneg]

/-- A média gaussiana converge, em toda a matriz, para o pinching espectral. -/
theorem tendsto_gaussianFlow (β : ℝ) (k : n → ℝ) (x : Matrix n n ℂ)
    (H_beta_pos : 0 < β) (H_K_nonneg : ∀ i, 0 ≤ k i) :
    Tendsto (fun t : ℝ => gaussianFlow β t k x) atTop (𝓝 (pinching k x)) := by
  apply tendsto_pi_nhds.mpr
  intro i
  apply tendsto_pi_nhds.mpr
  intro j
  have hr := tendsto_modalDecay β (Real.sqrt (k i) - Real.sqrt (k j)) H_beta_pos
  have hc := (Complex.continuous_ofReal.tendsto _).comp hr
  have hm := hc.mul_const (x i j)
  by_cases H_kij : k i = k j
  · have hs : Real.sqrt (k i) - Real.sqrt (k j) = 0 := sub_eq_zero.mpr (congrArg _ H_kij)
    rw [if_pos hs] at hm
    simpa [gaussianFlow_apply, pinching_apply, H_kij] using hm
  · have hs : Real.sqrt (k i) - Real.sqrt (k j) ≠ 0 := by
      apply sub_ne_zero.mpr
      intro hs
      exact H_kij ((Real.sqrt_inj (H_K_nonneg i) (H_K_nonneg j)).mp hs)
    rw [if_neg hs] at hm
    simpa [gaussianFlow_apply, pinching_apply, H_kij] using hm

/-- O pinching é idempotente e fixa exatamente o comutante. -/
theorem pinching_idem (k : n → ℝ) (x : Matrix n n ℂ) :
    pinching k (pinching k x) = pinching k x := by
  ext i j
  by_cases H_kij : k i = k j <;> simp [pinching_apply, H_kij]

#print axioms K05.T1.gaussianFlow_entry_formula
#print axioms K05.T1.diagonalK_isHermitian
#print axioms K05.T1.diagonalK_posSemidef
#print axioms K05.T1.diagonalK_commute_iff
#print axioms K05.T1.pinching_eq_self_iff
#print axioms K05.T1.modalDecay_eq_one_iff
#print axioms K05.T1.tendsto_modalDecay
#print axioms K05.T1.fixed_gaussianFlow_iff
#print axioms K05.T1.fixed_gaussianFlow_iff_pinching
#print axioms K05.T1.tendsto_gaussianFlow
#print axioms K05.T1.pinching_idem

end

end K05.T1
