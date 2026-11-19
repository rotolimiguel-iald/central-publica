import TGLExt.ProdutoFinito

set_option autoImplicit false
namespace FiniteProductCandidate
open Matrix ChatgptAudit.Observable035 TGLExt.MontagemDasGamas
open scoped Kronecker
noncomputable section

/-- Finite ungraded triple with the scalar algebra ℂ acting by scalar matrices. -/
structure ScalarOdd (ι : Type*) where
  D : Mat ι
  selfD : Dᴴ = D

def spatial (x y z : ℝ) : ScalarOdd (Fin 2) where
  D := planeD x y + (z : ℂ) • pauliZMatrix
  selfD := by simp [planeD, pauli_x_conjTranspose, pauli_y_conjTranspose, pauli_z_conjTranspose]

def line (t : ℝ) : ScalarOdd Unit where
  D := fun _ _ => (t : ℂ)
  selfD := by ext i j; simp

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

omit [DecidableEq ι] in
private theorem kronMultAux (a c : Mat ι) (b d : Mat2) :
    (a ⊗ₖ b) * (c ⊗ₖ d) = (a*c) ⊗ₖ (b*d) := (mul_kronecker_mul ..).symm

/-- Product of two odd scalar triples for a one-dimensional second Hilbert space.
The identification H⊗ℂ ≃ H removes the singleton index. The auxiliary ℂ² grades
the product. The second operator is its sole matrix entry. -/
def oddTimesLine (S : ScalarOdd ι) (T : ScalarOdd Unit) : EvenTriple (ι × Fin 2) where
  A := ⊥
  D := S.D ⊗ₖ pauliXMatrix + (T.D () ()) • ((1 : Mat ι) ⊗ₖ pauliYMatrix)
  grade := (1 : Mat ι) ⊗ₖ pauliZMatrix
  selfD := by
    have ht : star (T.D () ()) = T.D () () := congrFun (congrFun T.selfD ()) ()
    simp only [conjTranspose_add, conjTranspose_kronecker, S.selfD, pauli_x_conjTranspose,
      conjTranspose_smul, ht, conjTranspose_one, pauli_y_conjTranspose]
  selfGrade := by rw [conjTranspose_kronecker, conjTranspose_one, pauli_z_conjTranspose]
  gradeSq := by rw [kronMultAux, mul_one, pauli_z_square, one_kronecker_one]
  odd := by
    have hx : S.D ⊗ₖ (pauliZMatrix * pauliXMatrix) + S.D ⊗ₖ (pauliXMatrix * pauliZMatrix) = 0 := by
      rw [← kronecker_add, pauli_zx_anti, kronecker_zero]
    have hy : (1 : Mat ι) ⊗ₖ (pauliZMatrix * pauliYMatrix) + (1 : Mat ι) ⊗ₖ (pauliYMatrix * pauliZMatrix) = 0 := by
      rw [← kronecker_add, pauli_zy_anti, kronecker_zero]
    simp only [mul_add, add_mul, mul_smul_comm, smul_mul_assoc, kronMultAux, one_mul, mul_one]
    calc
      _ = (S.D ⊗ₖ (pauliZMatrix * pauliXMatrix) + S.D ⊗ₖ (pauliXMatrix * pauliZMatrix)) +
          ((T.D () ()) • ((1 : Mat ι) ⊗ₖ (pauliZMatrix * pauliYMatrix)) +
           (T.D () ()) • ((1 : Mat ι) ⊗ₖ (pauliYMatrix * pauliZMatrix))) := by abel
      _ = 0 := by rw [hx, ← smul_add, hy, smul_zero, zero_add]
  evenAction := by
    intro a ha
    obtain ⟨r, rfl⟩ := StarSubalgebra.mem_bot.mp ha
    exact (Algebra.commutes r _).symm

/-- Literal (3+1) finite symbol: the three Pauli coefficients belong to the
spatial odd factor; the fourth is the operator on the time line. -/
theorem spatial_line_eq_somaGamas (k : Fin 4 → ℝ) :
    (oddTimesLine (spatial (k 0) (k 1) (k 2)) (line (k 3))).D = somaGamas k := by
  change (planeD _ _ + (_ : ℂ) • pauliZMatrix) ⊗ₖ pauliXMatrix +
      (k 3 : ℂ) • ((1 : Mat2) ⊗ₖ pauliYMatrix) = _
  simp only [planeD, add_kronecker, smul_kronecker, somaGamas, Fin.sum_univ_four,
    gam_zero, gam_um, gam_dois, gam_tres]

theorem spatial_line_grade_eq_chi (k : Fin 4 → ℝ) :
    (oddTimesLine (spatial (k 0) (k 1) (k 2)) (line (k 3))).grade = chi :=
  chi_eq.symm

theorem even_odd_symbols_agree (k : Fin 4 → ℝ) :
    inGammaBasis (product (plane (k 0) (k 1)) (plane (k 2) (k 3))).D =
      (oddTimesLine (spatial (k 0) (k 1) (k 2)) (line (k 3))).D :=
  (productD_eq_somaGamas k).trans (spatial_line_eq_somaGamas k).symm

theorem spatial_line_unit_direction (j : Fin 4) :
    let k : Fin 4 → ℝ := fun i => if i = j then 1 else 0
    (oddTimesLine (spatial (k 0) (k 1) (k 2)) (line (k 3))).D = gam j := by
  dsimp only
  rw [spatial_line_eq_somaGamas (fun i => if i = j then 1 else 0)]
  classical
  simp [somaGamas, apply_ite, ite_smul]

end
end FiniteProductCandidate
