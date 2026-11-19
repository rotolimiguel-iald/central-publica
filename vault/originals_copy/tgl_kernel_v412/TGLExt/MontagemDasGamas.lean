-- ---------------------------------------------------------------------
-- A ALGEBRA FINITA DAS QUATRO GAMAS da montagem 3+1.
-- O QUE E: a algebra finita das quatro gamas 4x4 sobre C (gam 0 = Gamma_1 = sigma_x x tau_1,
--   gam 1 = Gamma_2 = sigma_y x tau_1, gam 2 = Gamma_3 = sigma_z x tau_1, gam 3 = Gamma_4 = 1 x tau_2,
--   na ordem do documento da montagem) e os sinais KO 4 NO NIVEL DAS GAMAS.
-- O QUE NAO E: nao e a tripla espectral do toro, nao e o operador de Dirac em L2, nao e a montagem
--   formalizada, nao e nada de III_1 nem de assinatura (1,3). O kernel nao tem o tipo tripla espectral:
--   sem ele, isto e algebra finita sem consumidor.
-- DOIS LIMITES DITOS: (1) dos tres sinais KO 4, epsilon = -1 e epsilon'' = +1 saem inteiros; de
--   epsilon' = +1 so sai a metade das gamas, que vale -1 (C conj(D(k)) C = D(-k)); o +1 final e o
--   produto desse -1 pelo -1 da reflexao de modos k -> -k do fator -i d em L2, que NAO esta aqui.
--   (2) a secao G5 e uma identidade finita sobre as 24 permutacoes; o ciclo de Hochschild e o
--   emparelhamento com D nao sao construidos.
-- As identidades com C sao identidades de matrizes; J = C composta com a conjugacao e antilinear e
--   nao e construido.
-- Reusa do kernel: pauliXMatrix/Y/Z e os teoremas pauli_*_square, pauli_xy, pauli_yx,
--   pauli_*_conjTranspose (TGLExt.SitePauliObservables) e o produto de Kronecker.
-- ---------------------------------------------------------------------
import TGLExt.SitePauliObservables
import Mathlib.LinearAlgebra.Matrix.Kronecker
import Mathlib.GroupTheory.Perm.Sign
import Mathlib.GroupTheory.Perm.Fin

set_option autoImplicit false

namespace TGLExt.MontagemDasGamas

open Matrix ChatgptAudit.Observable035
open scoped Kronecker

noncomputable section

/-- Matrizes 2x2 complexas. -/
abbrev Mat2 := Matrix (Fin 2) (Fin 2) ℂ

/-- Matrizes 4x4 complexas, indexadas por `Fin 2 × Fin 2`. -/
abbrev Mat4 := Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ

/-! ## 0. Complementos de Pauli e de Kronecker -/

/-- `σx σz + σz σx = 0`. -/
theorem pauli_xz_anti : pauliXMatrix * pauliZMatrix + pauliZMatrix * pauliXMatrix = 0 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [pauliXMatrix, pauliZMatrix, Matrix.mul_apply, Fin.sum_univ_two]

/-- `σy σz + σz σy = 0`. -/
theorem pauli_yz_anti : pauliYMatrix * pauliZMatrix + pauliZMatrix * pauliYMatrix = 0 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [pauliYMatrix, pauliZMatrix, Matrix.mul_apply, Fin.sum_univ_two]

/-- `σx σy + σy σx = 0`, a partir de `pauli_xy` e `pauli_yx` do kernel. -/
theorem pauli_xy_anti : pauliXMatrix * pauliYMatrix + pauliYMatrix * pauliXMatrix = 0 := by
  rw [pauli_xy, pauli_yx, ← add_smul]
  simp

/-- `σz σx + σx σz = 0`. -/
theorem pauli_zx_anti : pauliZMatrix * pauliXMatrix + pauliXMatrix * pauliZMatrix = 0 :=
  (add_comm _ _).trans pauli_xz_anti

/-- `σz σy + σy σz = 0`. -/
theorem pauli_zy_anti : pauliZMatrix * pauliYMatrix + pauliYMatrix * pauliZMatrix = 0 :=
  (add_comm _ _).trans pauli_yz_anti

/-- `σy σx σy = -σx`. -/
theorem pauli_yxy : pauliYMatrix * pauliXMatrix * pauliYMatrix = (-1 : ℂ) • pauliXMatrix := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [pauliXMatrix, pauliYMatrix, Matrix.mul_apply, Fin.sum_univ_two]

/-- `σy σz σy = -σz`. -/
theorem pauli_yzy : pauliYMatrix * pauliZMatrix * pauliYMatrix = (-1 : ℂ) • pauliZMatrix := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [pauliZMatrix, pauliYMatrix, Matrix.mul_apply, Fin.sum_univ_two]

/-- A conjugacao complexa entrada a entrada fixa `σx`. -/
theorem pauli_x_map_star : pauliXMatrix.map star = pauliXMatrix := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [pauliXMatrix]

/-- A conjugacao complexa entrada a entrada fixa `σz`. -/
theorem pauli_z_map_star : pauliZMatrix.map star = pauliZMatrix := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [pauliZMatrix]

/-- A conjugacao complexa entrada a entrada leva `σy` em `-σy`. -/
theorem pauli_y_map_star : pauliYMatrix.map star = (-1 : ℂ) • pauliYMatrix := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [pauliYMatrix]

/-- A conjugacao complexa entrada a entrada fixa a identidade 2x2. -/
theorem one_map_star : (1 : Mat2).map star = 1 :=
  Matrix.map_one star (star_zero ℂ) (star_one ℂ)

/-- O produto de dois Kronecker e o Kronecker dos produtos (forma de reescrita). -/
theorem kron_mul_kron (A A' B B' : Mat2) : (A ⊗ₖ B) * (A' ⊗ₖ B') = (A * A') ⊗ₖ (B * B') :=
  (mul_kronecker_mul A A' B B').symm

/-- A conjugacao entrada a entrada passa ao Kronecker. -/
theorem kron_map_star (A B : Mat2) : (A ⊗ₖ B).map star = A.map star ⊗ₖ B.map star := by
  ext ⟨a, b⟩ ⟨c, d⟩
  simp

/-- O sinal sai do fator da esquerda de um Kronecker. -/
theorem neg_kron (A B : Mat2) : (-A) ⊗ₖ B = -(A ⊗ₖ B) := by
  ext ⟨a, b⟩ ⟨c, d⟩
  simp

/-- O sinal sai do fator da direita de um Kronecker. -/
theorem kron_neg (A B : Mat2) : A ⊗ₖ (-B) = -(A ⊗ₖ B) := by
  ext ⟨a, b⟩ ⟨c, d⟩
  simp

/-- Anticomutacao de dois Kronecker quando os fatores da esquerda anticomutam e os da direita
comutam. -/
theorem anti_kron_esq (A A' B B' : Mat2) (hA : A * A' + A' * A = 0) (hB : B * B' = B' * B) :
    (A ⊗ₖ B) * (A' ⊗ₖ B') + (A' ⊗ₖ B') * (A ⊗ₖ B) = 0 := by
  rw [kron_mul_kron, kron_mul_kron, ← hB, ← add_kronecker, hA, zero_kronecker]

/-- Anticomutacao de dois Kronecker quando os fatores da esquerda comutam e os da direita
anticomutam. -/
theorem anti_kron_dir (A A' B B' : Mat2) (hA : A * A' = A' * A) (hB : B * B' + B' * B = 0) :
    (A ⊗ₖ B) * (A' ⊗ₖ B') + (A' ⊗ₖ B') * (A ⊗ₖ B) = 0 := by
  rw [kron_mul_kron, kron_mul_kron, ← hA, ← kronecker_add, hB, kronecker_zero]

/-! ## G1. As quatro gamas -/

/-- As quatro gamas 4x4: `gam 0 = Γ₁ = σx⊗σx`, `gam 1 = Γ₂ = σy⊗σx`, `gam 2 = Γ₃ = σz⊗σx`,
`gam 3 = Γ₄ = 1⊗σy` (o indice do Lean vai de 0 a 3; o do documento, de 1 a 4)
(a ordem dos fatores e a do documento da montagem: primeiro o fator auxiliar `σ`, depois `τ`). -/
def gam : Fin 4 → Mat4
  | 0 => pauliXMatrix ⊗ₖ pauliXMatrix
  | 1 => pauliYMatrix ⊗ₖ pauliXMatrix
  | 2 => pauliZMatrix ⊗ₖ pauliXMatrix
  | 3 => (1 : Mat2) ⊗ₖ pauliYMatrix

theorem gam_zero : gam 0 = pauliXMatrix ⊗ₖ pauliXMatrix := rfl
theorem gam_um : gam 1 = pauliYMatrix ⊗ₖ pauliXMatrix := rfl
theorem gam_dois : gam 2 = pauliZMatrix ⊗ₖ pauliXMatrix := rfl
theorem gam_tres : gam 3 = (1 : Mat2) ⊗ₖ pauliYMatrix := rfl

/-- Cada gama ao quadrado e a identidade. -/
theorem gam_sq (j : Fin 4) : gam j * gam j = 1 := by
  fin_cases j <;>
    simp [gam, kron_mul_kron, pauli_x_square, pauli_y_square, pauli_z_square]

theorem gam_anti_01 : gam 0 * gam 1 + gam 1 * gam 0 = 0 :=
  anti_kron_esq _ _ _ _ pauli_xy_anti rfl

theorem gam_anti_02 : gam 0 * gam 2 + gam 2 * gam 0 = 0 :=
  anti_kron_esq _ _ _ _ pauli_xz_anti rfl

theorem gam_anti_12 : gam 1 * gam 2 + gam 2 * gam 1 = 0 :=
  anti_kron_esq _ _ _ _ pauli_yz_anti rfl

theorem gam_anti_03 : gam 0 * gam 3 + gam 3 * gam 0 = 0 :=
  anti_kron_dir _ _ _ _ (by simp) pauli_xy_anti

theorem gam_anti_13 : gam 1 * gam 3 + gam 3 * gam 1 = 0 :=
  anti_kron_dir _ _ _ _ (by simp) pauli_xy_anti

theorem gam_anti_23 : gam 2 * gam 3 + gam 3 * gam 2 = 0 :=
  anti_kron_dir _ _ _ _ (by simp) pauli_xy_anti

/-- Gamas distintas anticomutam. -/
theorem gam_anti (i j : Fin 4) (h : i ≠ j) : gam i * gam j + gam j * gam i = 0 := by
  fin_cases i <;> fin_cases j <;>
    first
    | exact absurd rfl h
    | exact gam_anti_01
    | exact (add_comm _ _).trans gam_anti_01
    | exact gam_anti_02
    | exact (add_comm _ _).trans gam_anti_02
    | exact gam_anti_12
    | exact (add_comm _ _).trans gam_anti_12
    | exact gam_anti_03
    | exact (add_comm _ _).trans gam_anti_03
    | exact gam_anti_13
    | exact (add_comm _ _).trans gam_anti_13
    | exact gam_anti_23
    | exact (add_comm _ _).trans gam_anti_23

/-- Cada gama e autoadjunta. -/
theorem gam_selfadjoint (j : Fin 4) : (gam j)ᴴ = gam j := by
  fin_cases j <;>
    simp [gam, conjTranspose_kronecker, pauli_x_conjTranspose, pauli_y_conjTranspose,
      pauli_z_conjTranspose]

/-! ## G3. A quiralidade -/

/-- A quiralidade `χ = -(Γ₁Γ₂Γ₃Γ₄)`. -/
def chi : Mat4 := -(gam 0 * gam 1 * gam 2 * gam 3)

/-- A conta explicita: `χ = 1 ⊗ σz`. -/
theorem chi_eq : chi = (1 : Mat2) ⊗ₖ pauliZMatrix := by
  have h1 : pauliXMatrix * pauliYMatrix * pauliZMatrix = Complex.I • (1 : Mat2) := by
    rw [pauli_xy, smul_mul_assoc, pauli_z_square]
  have h2 : pauliXMatrix * pauliXMatrix * pauliXMatrix * pauliYMatrix =
      Complex.I • pauliZMatrix := by
    rw [pauli_x_square, one_mul, pauli_xy]
  unfold chi
  rw [gam_zero, gam_um, gam_dois, gam_tres]
  simp only [kron_mul_kron]
  rw [mul_one, h1, h2, smul_kronecker, kronecker_smul, smul_smul, Complex.I_mul_I]
  simp

theorem chi_sq : chi * chi = 1 := by
  rw [chi_eq, kron_mul_kron, mul_one, pauli_z_square, one_kronecker_one]

/-- `χ` anticomuta com cada gama. -/
theorem chi_anti (j : Fin 4) : chi * gam j + gam j * chi = 0 := by
  rw [chi_eq]
  fin_cases j
  · exact anti_kron_dir _ _ _ _ (by simp) pauli_zx_anti
  · exact anti_kron_dir _ _ _ _ (by simp) pauli_zx_anti
  · exact anti_kron_dir _ _ _ _ (by simp) pauli_zx_anti
  · exact anti_kron_dir _ _ _ _ (by simp) pauli_zy_anti

theorem chi_selfadjoint : chiᴴ = chi := by
  rw [chi_eq]
  simp [conjTranspose_kronecker, pauli_z_conjTranspose]

/-! ## G4. Os sinais KO 4 das gamas (`J = C ∘ conjugacao`, com `C = σy ⊗ 1`) -/

/-- A matriz `C = σy ⊗ 1`. (`J = C ∘ conjugacao` seria antilinear e nao e construido aqui.) -/
def matC : Mat4 := pauliYMatrix ⊗ₖ (1 : Mat2)

theorem matC_sq : matC * matC = 1 := by
  unfold matC
  rw [kron_mul_kron, pauli_y_square, mul_one, one_kronecker_one]

/-- `C · conj(C) = -1` (o sinal `ε = -1` de `J² = -1`). -/
theorem matC_conj_matC : matC * matC.map star = -1 := by
  unfold matC
  rw [kron_map_star, pauli_y_map_star, one_map_star, kron_mul_kron, mul_smul_comm,
    pauli_y_square, mul_one, smul_kronecker, one_kronecker_one, neg_one_smul]

theorem matC_inverte_gam_0 : matC * (gam 0).map star * matC = -gam 0 := by
  simp only [matC, gam_zero, kron_map_star, pauli_x_map_star, kron_mul_kron, pauli_yxy,
    one_mul, mul_one, neg_one_smul, neg_kron]

theorem matC_inverte_gam_1 : matC * (gam 1).map star * matC = -gam 1 := by
  simp only [matC, gam_um, kron_map_star, pauli_x_map_star, pauli_y_map_star, kron_mul_kron,
    neg_one_smul, mul_neg, neg_mul, pauli_y_square, one_mul, mul_one, neg_kron]

theorem matC_inverte_gam_2 : matC * (gam 2).map star * matC = -gam 2 := by
  simp only [matC, gam_dois, kron_map_star, pauli_x_map_star, pauli_z_map_star,
    kron_mul_kron, pauli_yzy, one_mul, mul_one, neg_one_smul, neg_kron]

theorem matC_inverte_gam_3 : matC * (gam 3).map star * matC = -gam 3 := by
  simp only [matC, gam_tres, kron_map_star, pauli_y_map_star, one_map_star, kron_mul_kron,
    neg_one_smul, mul_neg, neg_mul, pauli_y_square, one_mul, mul_one, kron_neg]

/-- `C · conj(Γⱼ) · C = -Γⱼ` (o sinal de `J Γⱼ J⁻¹ = -Γⱼ`, com `C⁻¹ = C`). -/
theorem matC_inverte_gam (j : Fin 4) : matC * (gam j).map star * matC = -gam j := by
  fin_cases j
  · exact matC_inverte_gam_0
  · exact matC_inverte_gam_1
  · exact matC_inverte_gam_2
  · exact matC_inverte_gam_3

/-- `C · conj(χ) · C = χ` (o sinal `ε'' = +1` de `Jχ = χJ`). -/
theorem matC_fixa_chi : matC * chi.map star * matC = chi := by
  simp only [matC, chi_eq, kron_map_star, one_map_star, pauli_z_map_star, kron_mul_kron,
    mul_one, one_mul, pauli_y_square]

theorem map_star_add (X Y : Mat4) : (X + Y).map star = X.map star + Y.map star := by
  ext i j
  simp

theorem map_star_smul (c : ℂ) (X : Mat4) : (c • X).map star = star c • X.map star := by
  ext i j
  simp

theorem conjC_add (X Y : Mat4) :
    matC * (X + Y).map star * matC = matC * X.map star * matC + matC * Y.map star * matC := by
  rw [map_star_add, mul_add, add_mul]

theorem conjC_smul (c : ℂ) (X : Mat4) :
    matC * (c • X).map star * matC = star c • (matC * X.map star * matC) := by
  rw [map_star_smul, mul_smul_comm, smul_mul_assoc]

/-- A combinacao linear `D(k) = Σⱼ kⱼ Γⱼ` das gamas, com `k` real. E so a soma; nao e o operador de
Dirac em `L²`. -/
def somaGamas (k : Fin 4 → ℝ) : Mat4 := ∑ j, ((k j : ℝ) : ℂ) • gam j

/-- `C · conj(D(k)) · C = D(-k)`. No nivel das gamas o sinal e `-1`; o `ε' = +1` de `J D = D J` e o
produto desse `-1` pelo `-1` da reflexao de modos `k ↦ -k`, que e analise em `L²` e NAO esta aqui. -/
theorem matC_conj_somaGamas (k : Fin 4 → ℝ) :
    matC * (somaGamas k).map star * matC = somaGamas (fun j => -k j) := by
  unfold somaGamas
  simp only [Fin.sum_univ_four, conjC_add, conjC_smul, matC_inverte_gam]
  simp [Complex.conj_ofReal, smul_neg, neg_smul]

/-! ## G2. O quadrado da soma das gamas -/

/-- Versao abstrata, em qualquer anel: se `Γᵢ² = 1`, as `Γ` distintas anticomutam e os
coeficientes `kᵢ` comutam entre si e com as `Γ`, entao `(Σ kᵢΓᵢ)² = Σ kᵢ²`. -/
theorem clifford_sq {R : Type*} [Ring R] {ι : Type*} [Fintype ι] [DecidableEq ι]
    (Γ k : ι → R) (hΓ : ∀ i, Γ i * Γ i = 1)
    (hanti : ∀ i j, i ≠ j → Γ i * Γ j + Γ j * Γ i = 0)
    (hkΓ : ∀ i j, Commute (k i) (Γ j)) (hkk : ∀ i j, Commute (k i) (k j)) :
    (∑ i, k i * Γ i) * (∑ i, k i * Γ i) = ∑ i, k i * k i := by
  have hT : ∀ i j, (k i * Γ i) * (k j * Γ j) = k i * k j * (Γ i * Γ j) := by
    intro i j
    have h := (hkΓ j i).eq
    calc (k i * Γ i) * (k j * Γ j) = k i * (Γ i * k j) * Γ j := by simp only [mul_assoc]
      _ = k i * (k j * Γ i) * Γ j := by rw [h]
      _ = k i * k j * (Γ i * Γ j) := by simp only [mul_assoc]
  have hsplit : ∀ i j, k i * k j * (Γ i * Γ j) =
      (if i = j then k i * k i else 0) +
        (if i = j then 0 else k i * k j * (Γ i * Γ j)) := by
    intro i j
    by_cases h : i = j
    · subst h
      simp [hΓ]
    · simp [h]
  have hoff : ∑ i, ∑ j, (if i = j then (0 : R) else k i * k j * (Γ i * Γ j)) = 0 := by
    rw [← Finset.sum_product']
    refine Finset.sum_involution (fun p _ => p.swap) ?_ ?_ ?_ ?_
    · intro p _
      by_cases h : p.1 = p.2
      · simp [h]
      · have h' : p.2 ≠ p.1 := fun e => h e.symm
        simp only [h, h', if_false, Prod.fst_swap, Prod.snd_swap]
        rw [← (hkk p.1 p.2).eq, ← mul_add, hanti p.1 p.2 h, mul_zero]
    · intro p _ hne heq
      apply hne
      have h2 : p.2 = p.1 := congrArg Prod.fst heq
      simp [h2]
    · intro p _
      exact Finset.mem_univ _
    · intro p _
      exact Prod.swap_swap p
  rw [Finset.sum_mul_sum]
  have e : ∑ i, ∑ j, (k i * Γ i) * (k j * Γ j) =
      ∑ i, ∑ j, ((if i = j then k i * k i else 0) +
        (if i = j then 0 else k i * k j * (Γ i * Γ j))) :=
    Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => (hT i j).trans (hsplit i j)
  rw [e]
  simp only [Finset.sum_add_distrib, hoff]
  simp

/-- `D(k)² = (Σⱼ kⱼ²) · 1`, instancia concreta com as gamas 4x4. -/
theorem somaGamas_sq (k : Fin 4 → ℝ) :
    somaGamas k * somaGamas k = ((∑ j, (k j) ^ 2 : ℝ) : ℂ) • (1 : Mat4) := by
  have h := clifford_sq (R := Mat4) gam (fun j => ((k j : ℝ) : ℂ) • (1 : Mat4)) gam_sq
    (fun i j hij => gam_anti i j hij)
    (fun i j => (Commute.one_left (gam j)).smul_left _)
    (fun i j => (Commute.one_left (((k j : ℝ) : ℂ) • (1 : Mat4))).smul_left _)
  simp only [smul_mul_assoc, one_mul, mul_smul_comm, mul_one, smul_smul] at h
  unfold somaGamas
  rw [h, ← Finset.sum_smul]
  push_cast
  simp [sq]

/-! ## G5. A soma sobre as 24 permutacoes (identidade finita; o ciclo de Hochschild nao e construido) -/

/-- Sinal de uma quadrupla de posicoes pela contagem de inversoes (as seis comparacoes). -/
def invSign (a b c d : Fin 4) : ℤ :=
  (if a < b then 1 else -1) * (if a < c then 1 else -1) * (if a < d then 1 else -1) *
  (if b < c then 1 else -1) * (if b < d then 1 else -1) * (if c < d then 1 else -1)

set_option maxRecDepth 100000 in
/-- O sinal de cada uma das 24 permutacoes de `Fin 4` e a contagem de inversoes de
`(τ 0, τ 1, τ 2, τ 3)` (verificado por `decide` sobre as 24 permutacoes). -/
theorem sinal_por_inversoes :
    ∀ τ : Equiv.Perm (Fin 4),
      ((Equiv.Perm.sign τ : ℤˣ) : ℤ) = invSign (τ 0) (τ 1) (τ 2) (τ 3) := by
  decide

/-- Em qualquer anel, se os `Γ` de indices distintos anticomutam, reordenar quatro deles
distintos multiplica o produto pelo sinal da reordenacao. -/
theorem reordena_produto {R : Type*} [Ring R] (Γ : Fin 4 → R)
    (h : ∀ i j, i ≠ j → Γ i * Γ j = -(Γ j * Γ i)) (a b c d : Fin 4)
    (hab : a ≠ b) (hac : a ≠ c) (had : a ≠ d) (hbc : b ≠ c) (hbd : b ≠ d) (hcd : c ≠ d) :
    invSign a b c d • (Γ a * Γ b * Γ c * Γ d) = Γ 0 * Γ 1 * Γ 2 * Γ 3 := by
  have z : ∀ i j w, i ≠ j → Γ i * (Γ j * w) = -(Γ j * (Γ i * w)) := by
    intro i j w hij
    rw [← mul_assoc, h i j hij, neg_mul, mul_assoc]
  have r10 := h 1 0 (by decide)
  have r20 := h 2 0 (by decide)
  have r30 := h 3 0 (by decide)
  have r21 := h 2 1 (by decide)
  have r31 := h 3 1 (by decide)
  have r32 := h 3 2 (by decide)
  have z10 : ∀ w, Γ 1 * (Γ 0 * w) = -(Γ 0 * (Γ 1 * w)) := fun w => z 1 0 w (by decide)
  have z20 : ∀ w, Γ 2 * (Γ 0 * w) = -(Γ 0 * (Γ 2 * w)) := fun w => z 2 0 w (by decide)
  have z21 : ∀ w, Γ 2 * (Γ 1 * w) = -(Γ 1 * (Γ 2 * w)) := fun w => z 2 1 w (by decide)
  fin_cases a <;> fin_cases b <;> fin_cases c <;> fin_cases d <;>
    first
    | exact absurd rfl hab
    | exact absurd rfl hac
    | exact absurd rfl had
    | exact absurd rfl hbc
    | exact absurd rfl hbd
    | exact absurd rfl hcd
    | simp [invSign, mul_assoc, r10, r20, r30, r21, r31, r32, z10, z20, z21]

/-- A soma sobre as 24 permutacoes, com o sinal da permutacao, de
`Γ_{τ0} Γ_{τ1} Γ_{τ2} Γ_{τ3}` e `24 · Γ₀Γ₁Γ₂Γ₃`, em qualquer anel em que os `Γ` distintos
anticomutam (so a anticomutacao entra; `Γᵢ² = 1` nao e usado). -/
theorem soma_permutacoes_anticomutativas {R : Type*} [Ring R] (Γ : Fin 4 → R)
    (h : ∀ i j, i ≠ j → Γ i * Γ j = -(Γ j * Γ i)) :
    ∑ τ : Equiv.Perm (Fin 4), ((Equiv.Perm.sign τ : ℤˣ) : ℤ) •
        (Γ (τ 0) * Γ (τ 1) * Γ (τ 2) * Γ (τ 3)) = (24 : ℤ) • (Γ 0 * Γ 1 * Γ 2 * Γ 3) := by
  have key : ∀ τ : Equiv.Perm (Fin 4), ((Equiv.Perm.sign τ : ℤˣ) : ℤ) •
      (Γ (τ 0) * Γ (τ 1) * Γ (τ 2) * Γ (τ 3)) = Γ 0 * Γ 1 * Γ 2 * Γ 3 := by
    intro τ
    rw [sinal_por_inversoes τ]
    exact reordena_produto Γ h _ _ _ _ (τ.injective.ne (by decide)) (τ.injective.ne (by decide))
      (τ.injective.ne (by decide)) (τ.injective.ne (by decide)) (τ.injective.ne (by decide))
      (τ.injective.ne (by decide))
  rw [Finset.sum_congr rfl (fun τ _ => key τ), Finset.sum_const, Finset.card_univ,
    Fintype.card_perm, Fintype.card_fin]
  simp [Nat.factorial, ← Nat.cast_smul_eq_nsmul ℤ]

/-- As gamas distintas anticomutam, na forma `Γᵢ Γⱼ = -(Γⱼ Γᵢ)`. -/
theorem gam_anti_neg (i j : Fin 4) (hij : i ≠ j) : gam i * gam j = -(gam j * gam i) :=
  eq_neg_of_add_eq_zero_left (gam_anti i j hij)

/-- A soma sobre as 24 permutacoes das gamas vale `-24 · χ`. -/
theorem soma_orientacao :
    ∑ τ : Equiv.Perm (Fin 4), ((Equiv.Perm.sign τ : ℤˣ) : ℤ) •
        (gam (τ 0) * gam (τ 1) * gam (τ 2) * gam (τ 3)) = (-24 : ℤ) • chi := by
  rw [soma_permutacoes_anticomutativas gam gam_anti_neg]
  unfold chi
  rw [smul_neg, neg_smul, neg_neg]

/-- O somatorio sobre as 24 permutacoes de `sinal(τ) · Γ_{τ0} Γ_{τ1} Γ_{τ2} Γ_{τ3}`, normalizado por
`-1/24` (isto e, `-1` sobre o numero de permutacoes), vale `χ`. -/
theorem soma_normalizada_sobre_as_permutacoes_e_chi :
    (-(1 / 24) : ℂ) • ∑ τ : Equiv.Perm (Fin 4), ((((Equiv.Perm.sign τ : ℤˣ) : ℤ) : ℂ)) •
        (gam (τ 0) * gam (τ 1) * gam (τ 2) * gam (τ 3)) = chi := by
  simp only [Int.cast_smul_eq_zsmul ℂ]
  rw [soma_orientacao, ← Int.cast_smul_eq_zsmul ℂ, smul_smul]
  norm_num

end

end TGLExt.MontagemDasGamas
