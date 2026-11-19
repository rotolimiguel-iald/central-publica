import TGLExt.MontagemDasGamas
import Mathlib.Algebra.Star.Subalgebra
import Mathlib.LinearAlgebra.Matrix.Reindex

set_option autoImplicit false
set_option maxHeartbeats 3000000

namespace FiniteProductCandidate
open Matrix ChatgptAudit.Observable035 TGLExt.MontagemDasGamas
open scoped Kronecker
noncomputable section

abbrev Mat (ι : Type*) := Matrix ι ι ℂ

/-- Concrete finite represented even triple on the standard complex Hilbert space ℂ^ι.
The star subalgebra acts by its own matrices, so the representation is faithful. -/
structure EvenTriple (ι : Type*) [Fintype ι] [DecidableEq ι] where
  A : StarSubalgebra ℂ (Mat ι)
  D : Mat ι
  grade : Mat ι
  selfD : Dᴴ = D
  selfGrade : gradeᴴ = grade
  gradeSq : grade * grade = 1
  odd : grade * D + D * grade = 0
  evenAction : ∀ a ∈ A, grade * a = a * grade

variable {ι κ : Type*} [Fintype ι] [DecidableEq ι] [Fintype κ] [DecidableEq κ]

omit [DecidableEq ι] [DecidableEq κ] in
private theorem kronMult (A C : Mat ι) (B F : Mat κ) :
    (A ⊗ₖ B) * (C ⊗ₖ F) = (A * C) ⊗ₖ (B * F) := (mul_kronecker_mul ..).symm

def simpleTensors (S : EvenTriple ι) (T : EvenTriple κ) : Set (Mat (ι × κ)) :=
  {x | ∃ a ∈ S.A, ∃ b ∈ T.A, x = a ⊗ₖ b}

def productAlgebra (S : EvenTriple ι) (T : EvenTriple κ) :=
  StarAlgebra.adjoin ℂ (simpleTensors S T)

theorem simpleTensor_mem (S : EvenTriple ι) (T : EvenTriple κ)
    {a : Mat ι} {b : Mat κ} (ha : a ∈ S.A) (hb : b ∈ T.A) :
    a ⊗ₖ b ∈ productAlgebra S T :=
  StarAlgebra.subset_adjoin ℂ _ ⟨a, ha, b, hb, rfl⟩

private theorem evenAction_product (S : EvenTriple ι) (T : EvenTriple κ)
    (x : Mat (ι × κ)) (hx : x ∈ productAlgebra S T) :
    (S.grade ⊗ₖ T.grade) * x = x * (S.grade ⊗ₖ T.grade) := by
  have hle : productAlgebra S T ≤ StarSubalgebra.centralizer ℂ {S.grade ⊗ₖ T.grade} := by
    apply StarAlgebra.adjoin_le
    rintro _ ⟨a, ha, b, hb, rfl⟩
    apply (StarSubalgebra.mem_centralizer_iff ℂ).2
    rintro g (hg : g ∈ ({_} : Set _))
    obtain rfl := Set.mem_singleton_iff.mp hg
    have comm : (S.grade ⊗ₖ T.grade) * (a ⊗ₖ b) = (a ⊗ₖ b) * (S.grade ⊗ₖ T.grade) := by
      simp only [kronMult, S.evenAction a ha, T.evenAction b hb]
    refine ⟨comm, ?_⟩
    change (S.grade ⊗ₖ T.grade)ᴴ * _ = _ * (S.grade ⊗ₖ T.grade)ᴴ
    simpa only [conjTranspose_kronecker, S.selfGrade, T.selfGrade] using comm
  exact ((StarSubalgebra.mem_centralizer_iff ℂ).1 (hle hx) _ (Set.mem_singleton _)).1

def productD (S : EvenTriple ι) (T : EvenTriple κ) : Mat (ι × κ) :=
  S.D ⊗ₖ (1 : Mat κ) + S.grade ⊗ₖ T.D

theorem productD_self (S : EvenTriple ι) (T : EvenTriple κ) :
    (productD S T)ᴴ = productD S T := by
  simp only [productD, conjTranspose_add, conjTranspose_kronecker, S.selfD, S.selfGrade,
    T.selfD, conjTranspose_one]

theorem productD_square (S : EvenTriple ι) (T : EvenTriple κ) :
    productD S T * productD S T = (S.D * S.D) ⊗ₖ (1 : Mat κ) + (1 : Mat ι) ⊗ₖ (T.D * T.D) := by
  have cancel : (S.D * S.grade) ⊗ₖ T.D + (S.grade * S.D) ⊗ₖ T.D = 0 := by
    rw [← add_kronecker, add_comm, S.odd, zero_kronecker]
  simp only [productD, add_mul, mul_add, kronMult, mul_one, one_mul, S.gradeSq]
  calc
    _ = ((S.D * S.D) ⊗ₖ (1 : Mat κ) + (1 : Mat ι) ⊗ₖ (T.D * T.D)) +
        ((S.D * S.grade) ⊗ₖ T.D + (S.grade * S.D) ⊗ₖ T.D) := by abel
    _ = _ := by rw [cancel, add_zero]

theorem product_grade_odd (S : EvenTriple ι) (T : EvenTriple κ) :
    (S.grade ⊗ₖ T.grade) * productD S T + productD S T * (S.grade ⊗ₖ T.grade) = 0 := by
  have h₁ : (S.grade * S.D) ⊗ₖ T.grade + (S.D * S.grade) ⊗ₖ T.grade = 0 := by
    rw [← add_kronecker, S.odd, zero_kronecker]
  have h₂ : (1 : Mat ι) ⊗ₖ (T.grade * T.D) + (1 : Mat ι) ⊗ₖ (T.D * T.grade) = 0 := by
    rw [← kronecker_add, T.odd, kronecker_zero]
  simp only [productD, mul_add, add_mul, kronMult, one_mul, mul_one, S.gradeSq]
  calc
    _ = ((S.grade * S.D) ⊗ₖ T.grade + (S.D * S.grade) ⊗ₖ T.grade) +
        ((1 : Mat ι) ⊗ₖ (T.grade * T.D) + (1 : Mat ι) ⊗ₖ (T.D * T.grade)) := by abel
    _ = _ := by rw [h₁, h₂, zero_add]

def product (S : EvenTriple ι) (T : EvenTriple κ) : EvenTriple (ι × κ) where
  A := productAlgebra S T
  D := productD S T
  grade := S.grade ⊗ₖ T.grade
  selfD := productD_self S T
  selfGrade := by rw [conjTranspose_kronecker, S.selfGrade, T.selfGrade]
  gradeSq := by rw [kronMult, S.gradeSq, T.gradeSq, one_kronecker_one]
  odd := product_grade_odd S T
  evenAction := evenAction_product S T

theorem product_square (S : EvenTriple ι) (T : EvenTriple κ) :
    (product S T).D ^ 2 = (S.D ^ 2) ⊗ₖ (1 : Mat κ) + (1 : Mat ι) ⊗ₖ (T.D ^ 2) := by
  simpa only [product, pow_two] using productD_square S T

/-- The two-dimensional finite factors have the concrete even algebra commuting with Z. -/
def planeD (a b : ℝ) : Mat2 := (a : ℂ) • pauliXMatrix + (b : ℂ) • pauliYMatrix

def plane (a b : ℝ) : EvenTriple (Fin 2) where
  A := StarSubalgebra.centralizer ℂ {pauliZMatrix}
  D := planeD a b
  grade := pauliZMatrix
  selfD := by simp [planeD, pauli_x_conjTranspose, pauli_y_conjTranspose]
  selfGrade := pauli_z_conjTranspose
  gradeSq := pauli_z_square
  odd := by
    have hx := congrArg (fun M : Mat2 => (a : ℂ) • M) pauli_zx_anti
    have hy := congrArg (fun M : Mat2 => (b : ℂ) • M) pauli_zy_anti
    simp only [smul_add, smul_zero] at hx hy
    simp only [planeD, mul_add, add_mul, mul_smul_comm, smul_mul_assoc]
    calc
      _ = ((a : ℂ) • (pauliZMatrix * pauliXMatrix) + (a : ℂ) • (pauliXMatrix * pauliZMatrix)) +
          ((b : ℂ) • (pauliZMatrix * pauliYMatrix) + (b : ℂ) • (pauliYMatrix * pauliZMatrix)) := by abel
      _ = _ := by rw [hx, hy, zero_add]
  evenAction := fun x hx => ((StarSubalgebra.mem_centralizer_iff ℂ).1 hx _ (Set.mem_singleton _)).1

/-- The real unitary change of basis permutes the coordinates: (u,v) ↦ (u,v+u) mod 2. -/
def changeBasis : (Fin 2 × Fin 2) ≃ (Fin 2 × Fin 2) where
  toFun := fun p => (p.1, p.2 + p.1)
  invFun := fun p => (p.1, p.2 + p.1)
  left_inv := by rintro ⟨u,v⟩; fin_cases u <;> fin_cases v <;> rfl
  right_inv := by rintro ⟨u,v⟩; fin_cases u <;> fin_cases v <;> rfl

def inGammaBasis := Matrix.reindexLinearEquiv ℂ ℂ changeBasis changeBasis

private theorem bit_one_add_one : (1 : Fin 2) + 1 = 0 := rfl

def productGenerator : Fin 4 → Mat4
  | 0 => pauliXMatrix ⊗ₖ (1 : Mat2)
  | 1 => pauliYMatrix ⊗ₖ (1 : Mat2)
  | 2 => pauliZMatrix ⊗ₖ pauliXMatrix
  | 3 => pauliZMatrix ⊗ₖ pauliYMatrix

theorem productGenerator_eq_gam (j : Fin 4) : inGammaBasis (productGenerator j) = gam j := by
  ext ⟨a,b⟩ ⟨c,d⟩
  fin_cases j <;> fin_cases a <;> fin_cases b <;> fin_cases c <;> fin_cases d <;>
    norm_num [inGammaBasis, Matrix.coe_reindexLinearEquiv, Matrix.reindex, Matrix.submatrix, changeBasis, bit_one_add_one, productGenerator, gam,
      pauliXMatrix, pauliYMatrix, pauliZMatrix, Matrix.one_apply]

theorem productGrade_eq_chi (a b c d : ℝ) :
    inGammaBasis (product (plane a b) (plane c d)).grade = chi := by
  rw [chi_eq]
  change inGammaBasis (pauliZMatrix ⊗ₖ pauliZMatrix) = _
  ext ⟨i,j⟩ ⟨u,v⟩
  fin_cases i <;> fin_cases j <;> fin_cases u <;> fin_cases v <;>
    norm_num [inGammaBasis, Matrix.coe_reindexLinearEquiv, Matrix.reindex, Matrix.submatrix, changeBasis, bit_one_add_one, pauliZMatrix, Matrix.one_apply]

theorem productD_is_linear_symbol (k : Fin 4 → ℝ) :
    (product (plane (k 0) (k 1)) (plane (k 2) (k 3))).D =
    ∑ j, (k j : ℂ) • productGenerator j := by
  change (planeD _ _) ⊗ₖ _ + pauliZMatrix ⊗ₖ (planeD _ _) = _
  simp only [planeD, add_kronecker, kronecker_add, smul_kronecker, kronecker_smul,
    Fin.sum_univ_four, productGenerator]
  abel

/-- The actual product operator equals the full symbol of the gammas in this basis. -/
theorem productD_eq_somaGamas (k : Fin 4 → ℝ) :
    inGammaBasis (product (plane (k 0) (k 1)) (plane (k 2) (k 3))).D = somaGamas k := by
  rw [productD_is_linear_symbol]
  simp only [map_sum, map_smul, productGenerator_eq_gam, somaGamas]

end
end FiniteProductCandidate
