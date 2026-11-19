import TGLExt.BoostEDissipador
import TGLExt.Solder4D
import TGLExt.HermitianLocalCoordinates
import TGLExt.TensorNullCone
import Mathlib.Analysis.Calculus.Deriv.Mul

set_option autoImplicit false
set_option maxHeartbeats 2500000

namespace SpinorToSolder

open Matrix TGLExt TGLExt.BoostEDissipador ChatgptAudit.Observable035
noncomputable section

abbrev Four := Fin 4 → ℝ

/-- The exact Hermitian embedding used here, in (t,x,y,z) order. -/
def embed (v : Four) : M2 := herm4 (v 0) (v 1) (v 2) (v 3)

theorem embed_eq_existing (v : Four) :
    embed v = ChatgptAudit.Cone039.hermitianMatrix (v 0) (v 1) (v 2) (v 3) := by
  unfold embed herm4 ChatgptAudit.Cone039.hermitianMatrix
  push_cast
  rw [mul_comm (v 2 : ℂ) Complex.I]

theorem coordinates_embed (v : Four) :
    ChatgptAudit.Cone039.matrixCoordinates (embed v) = v := by
  rw [embed_eq_existing, ChatgptAudit.Cone039.coords_of_hermitian]
  funext i
  fin_cases i <;> rfl

theorem embed_injective : Function.Injective embed := by
  intro u v h
  simpa only [coordinates_embed] using congrArg ChatgptAudit.Cone039.matrixCoordinates h

/-- The determinant and the v63 quadratic form agree on every vector. -/
theorem determinant_eq_solder_form (v : Four) :
    (embed v).det = (ChatgptAudit.tensorQuad eta4 v : ℂ) := by
  have coord : ![v 0, v 1, v 2, v 3] = v := by funext i; fin_cases i <;> rfl
  have quad := ChatgptAudit.tensorQuad_eta (v 0) (v 1) (v 2) (v 3)
  rw [coord] at quad
  rw [quad]
  exact a_forma_de_minkowski_e_o_determinante ..

/-- Tangent to the left-right congruence, with the ordinary (unnormalized) Hermitian matrix. -/
def tangent (A X : M2) : M2 := A * X + X * Aᴴ

/-- Commutators of two infinitesimal actions are the action of the matrix commutator. -/
theorem tangent_bracket (A B X : M2) :
    tangent A (tangent B X) - tangent B (tangent A X) = tangent (A * B - B * A) X := by
  simp only [tangent, conjTranspose_sub, conjTranspose_mul]
  noncomm_ring

/-- Exact identity for the straight path through the identity with velocity A. -/
theorem congruence_expansion (s : ℝ) (A X : M2) :
    ((1 : M2) + s • A) * X * ((1 : M2) + s • A)ᴴ =
      X + s • tangent A X + (s*s) • (A * X * Aᴴ) := by
  simp only [conjTranspose_add, conjTranspose_one, conjTranspose_smul, star_trivial,
    add_mul, mul_add, one_mul, mul_one, smul_mul_assoc, mul_smul_comm, smul_smul,
    tangent, smul_add]
  abel

/-- A genuine real derivative, stated entrywise to avoid choosing a matrix norm. -/
theorem congruence_derivative (A X : M2) (i j : Fin 2) :
    HasDerivAt (fun s : ℝ => (((1 : M2) + s • A) * X * ((1 : M2) + s • A)ᴴ) i j)
      (tangent A X i j) 0 := by
  simp_rw [congruence_expansion, Matrix.add_apply, Matrix.smul_apply]
  have linear := (hasDerivAt_id (0 : ℝ)).smul_const (tangent A X i j)
  have quadratic := ((hasDerivAt_id (0 : ℝ)).mul (hasDerivAt_id (0 : ℝ))).smul_const ((A * X * Aᴴ) i j)
  simpa [Pi.add_def, Pi.mul_def, id]
    using ((hasDerivAt_const (0 : ℝ) (X i j)).add linear).add quadratic

/-- Order shared by the two bases: three boosts followed by three rotations. -/
def spinAxis : Fin 6 → M2 := ![Kx, Ky, Kz, Jx, Jy, Jz]
def solderAxis : Fin 6 → Matrix (Fin 4) (Fin 4) ℝ := ![K1, K2, K3, J1, J2, J3]

/-- Each column calculation uses the Pauli and the actual v63 matrices, in the same order. -/
theorem six_axes (a : Fin 6) (v : Four) :
    tangent (spinAxis a) (embed v) = embed (solderAxis a *ᵥ v) := by
  ext i j
  fin_cases a <;> fin_cases i <;> fin_cases j <;>
    apply Complex.ext <;>
    simp only [tangent, embed, herm4, spinAxis, solderAxis, Kx, Ky, Kz, Jx, Jy, Jz,
      K1, K2, K3, J1, J2, J3, pauliXMatrix, pauliYMatrix, pauliZMatrix,
      Matrix.add_apply, Matrix.mul_apply, Matrix.mulVec, dotProduct, Fin.sum_univ_two, Fin.sum_univ_four,
      Matrix.conjTranspose_apply, Matrix.of_apply, Matrix.cons_val_zero,
      Matrix.cons_val_one, Fin.isValue] <;>
    norm_num [Matrix.vecMul, dotProduct, Fin.sum_univ_two, Matrix.conjTranspose_apply, Complex.star_def,
      Complex.add_re, Complex.add_im, Complex.sub_re, Complex.sub_im, Complex.mul_re, Complex.mul_im,
      Matrix.cons_val_two, Matrix.cons_val_three, Matrix.vecHead, Matrix.vecTail, Fin.isValue] <;> ring

def spin (c : Fin 6 → ℝ) : M2 :=
  c 0 • Kx + c 1 • Ky + c 2 • Kz + c 3 • Jx + c 4 • Jy + c 5 • Jz

private theorem embed_add (u v : Four) : embed (u + v) = embed u + embed v := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [embed, herm4] <;> ring

private theorem embed_smul (r : ℝ) (v : Four) : embed (r • v) = r • embed v := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [embed, herm4, Complex.real_smul] <;> ring

private theorem tangent_add (A B X : M2) :
    tangent (A+B) X = tangent A X + tangent B X := by
  simp only [tangent, add_mul, mul_add, conjTranspose_add]
  abel

private theorem tangent_smul (r : ℝ) (A X : M2) :
    tangent (r • A) X = r • tangent A X := by
  simp only [tangent, smul_mul_assoc, conjTranspose_smul, star_trivial, mul_smul_comm, smul_add]

/-- Intertwining for arbitrary real linear combinations and arbitrary Hermitian coordinates. -/
theorem all_generators (c : Fin 6 → ℝ) (v : Four) :
    tangent (spin c) (embed v) = embed (lorentzRep c *ᵥ v) := by
  have hx : tangent Kx (embed v) = embed (K1 *ᵥ v) := six_axes 0 v
  have hy : tangent Ky (embed v) = embed (K2 *ᵥ v) := six_axes 1 v
  have hz : tangent Kz (embed v) = embed (K3 *ᵥ v) := six_axes 2 v
  have hrx : tangent Jx (embed v) = embed (J1 *ᵥ v) := six_axes 3 v
  have hry : tangent Jy (embed v) = embed (J2 *ᵥ v) := six_axes 4 v
  have hrz : tangent Jz (embed v) = embed (J3 *ᵥ v) := six_axes 5 v
  simp only [spin, lorentzRep, tangent_add, tangent_smul, hx, hy, hz, hrx, hry, hrz,
    add_mulVec, smul_mulVec, embed_add, embed_smul]

theorem coordinates_tangent (c : Fin 6 → ℝ) (v : Four) :
    ChatgptAudit.Cone039.matrixCoordinates (tangent (spin c) (embed v)) = lorentzRep c *ᵥ v := by
  rw [all_generators, coordinates_embed]

/-- The six coefficients can be recovered from the action on all Hermitian inputs. -/
theorem coefficients_unique {c d : Fin 6 → ℝ}
    (h : ∀ v : Four, tangent (spin c) (embed v) = tangent (spin d) (embed v)) : c = d := by
  apply lorentzRep_injective
  apply Matrix.ext_iff_mulVec.mpr
  intro v
  apply embed_injective
  simpa only [all_generators] using h v

theorem spin_injective : Function.Injective spin := by
  intro c d h
  apply coefficients_unique
  intro v
  rw [h]

end
end SpinorToSolder
