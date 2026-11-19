import TGLExt.MontagemDasGamas

set_option autoImplicit false
namespace FiniteProductCandidate
open Matrix ChatgptAudit.Observable035 TGLExt.MontagemDasGamas
open scoped Kronecker
noncomputable section

abbrev Spin := (Fin 2 × Fin 2) → ℂ
abbrev Modes := Spin × Spin

/-- Charge conjugation on one finite spinor. -/
def charge (v : Spin) : Spin := matC *ᵥ star v

theorem charge_add (v w : Spin) : charge (v+w) = charge v + charge w := by
  simp only [charge, star_add, mulVec_add]

theorem charge_conjugate_linear (z : ℂ) (v : Spin) :
    charge (z • v) = star z • charge v := by
  have hs : star (z • v) = star z • star v := by ext i; simp
  rw [charge, hs, mulVec_smul, charge]

private theorem starVector (M : Mat4) (v : Spin) :
    star (M *ᵥ v) = M.map star *ᵥ star v := by
  funext i
  exact RingHom.map_mulVec (starRingEnd ℂ) M v i

theorem charge_square (v : Spin) : charge (charge v) = -v := by
  simp only [charge, starVector, star_star, mulVec_mulVec, matC_conj_matC, neg_mulVec, one_mulVec]

private theorem c_unitary : matCᴴ * matC = 1 := by
  have h : matCᴴ = matC := by
    simp only [matC, conjTranspose_kronecker, pauli_y_conjTranspose, conjTranspose_one]
  rw [h, matC_sq]

/-- The standard Hermitian form in an orthonormal basis. -/
def herm (v w : Spin) : ℂ := star v ⬝ᵥ w

theorem charge_antiunitary (v w : Spin) :
    herm (charge v) (charge w) = star (herm v w) := by
  simp only [herm, charge, star_mulVec, star_star, dotProduct_mulVec, vecMul_vecMul,
    c_unitary, vecMul_one]
  rw [dotProduct_star, dotProduct_comm w (star v)]

private theorem charge_intertwines (M N : Mat4) (h : matC * M.map star * matC = N) (v : Spin) :
    charge (M *ᵥ v) = N *ᵥ charge v := by
  have h' := congrArg (fun Q : Mat4 => Q * matC) h
  simp only [mul_assoc, matC_sq, mul_one] at h'
  simp only [charge, starVector, mulVec_mulVec, h']

theorem charge_at_fixed_mode (k : Fin 4 → ℝ) (v : Spin) :
    charge ((somaGamas k) *ᵥ v) = (somaGamas (fun j => -k j)) *ᵥ charge v :=
  charge_intertwines _ _ (matC_conj_somaGamas k) v

theorem charge_grading (v : Spin) : charge (chi *ᵥ v) = chi *ᵥ charge v :=
  charge_intertwines _ _ matC_fixa_chi v

/-- Finite direct sum of two labelled fibers k and −k. The exchange is specified explicitly. -/
def pairCharge (v : Modes) : Modes := (charge v.2, charge v.1)
def pairDirac (k : Fin 4 → ℝ) (v : Modes) : Modes :=
  (somaGamas k *ᵥ v.1, somaGamas (fun j => -k j) *ᵥ v.2)
def pairGrade (v : Modes) : Modes := (chi *ᵥ v.1, chi *ᵥ v.2)
def pairHerm (v w : Modes) : ℂ := herm v.1 w.1 + herm v.2 w.2

theorem pairCharge_antiunitary (v w : Modes) :
    pairHerm (pairCharge v) (pairCharge w) = star (pairHerm v w) := by
  simp only [pairHerm, pairCharge, charge_antiunitary, star_add]
  exact add_comm _ _

theorem pairCharge_semilinear (z : ℂ) (v w : Modes) :
    pairCharge (v+w) = pairCharge v + pairCharge w ∧
    pairCharge (z • v) = star z • pairCharge v := by
  constructor
  · exact Prod.ext (charge_add ..) (charge_add ..)
  · exact Prod.ext (charge_conjugate_linear ..) (charge_conjugate_linear ..)

/-- The KO-4 signs (-,+,+) on the explicitly doubled, finite system. -/
theorem paired_signs (k : Fin 4 → ℝ) (v : Modes) :
    pairCharge (pairCharge v) = -v ∧
    pairCharge (pairDirac k v) = pairDirac k (pairCharge v) ∧
    pairCharge (pairGrade v) = pairGrade (pairCharge v) := by
  refine ⟨Prod.ext (charge_square _) (charge_square _), ?_, Prod.ext (charge_grading _) (charge_grading _)⟩
  apply Prod.ext
  · simpa only [pairDirac, pairCharge, neg_neg] using charge_at_fixed_mode (fun j => -k j) v.2
  · exact charge_at_fixed_mode k v.1

end
end FiniteProductCandidate
