import OHabitanteDoNome
import Mathlib.Analysis.InnerProductSpace.Positive
set_option autoImplicit false
open TGLExt TGLExt.OHabitanteDoNome

variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H]

/-- verbos_iguais_tem_o_mesmo_nome e' uma linha da Mathlib: Submodule.starProjection_inj. -/
theorem T5a (K L : Submodule ℂ H) [K.HasOrthogonalProjection] [L.HasOrthogonalProjection]
    (h : ∀ v, K.starProjection v = L.starProjection v) : K = L :=
  Submodule.starProjection_inj.mp (ContinuousLinearMap.ext h)

/-- a primeira metade de o_nome_e_o_ato_do_verbo e' Submodule.range_starProjection. -/
theorem T5b (K : Submodule ℂ H) [K.HasOrthogonalProjection] :
    Set.range (fun v : H => K.starProjection v) = (K : Set H) := by
  have h := Submodule.range_starProjection K
  ext w
  constructor
  · rintro ⟨v, rfl⟩
    exact K.starProjection_apply_mem v
  · intro hw
    exact ⟨w, Submodule.starProjection_eq_self_iff.mpr hw⟩

/-- o_ato_e_ser_sse_o_nome_e_o_todo, volta: Submodule.starProjection_top. -/
theorem T5c (K : Submodule ℂ H) [K.HasOrthogonalProjection] (h : K = ⊤) (v : H) : K.starProjection v = v := by
  subst h
  rw [Submodule.starProjection_top]
  rfl

/-- reflexo de Identidade.Nome NAO e' usado em o_verbo_do_nome_e_ser_sse_forma_igual_conteudo: vale para todo idempotente de matriz. -/
theorem T5d {n : Type} [Fintype n] [DecidableEq n] [Nonempty n] {P : Matrix n n ℂ} (hP : P * P = P) :
    (∀ x : Matrix n n ℂ, nameOp P x = x) ↔ (P = 0 ∨ P = 1) := by
  constructor
  · intro h
    have hcomm : ∀ x : Matrix n n ℂ, P * x = x * P := fun x =>
      (a_morada_e_o_que_comuta_com_o_posto hP x).mp (h x)
    obtain ⟨c, hc⟩ := (Matrix.mem_range_scalar_iff_commute_single' (M := P)).mpr
      (fun i j => ((hcomm (Matrix.single i j 1)).symm : Matrix.single i j 1 * P = P * Matrix.single i j 1))
    have hcc : c * c = c := by
      have h2 : Matrix.scalar n (c * c) = Matrix.scalar n c := by
        rw [map_mul, hc]
        exact hP
      exact Matrix.scalar_inj.mp h2
    rcases (TGLExt.TheAxiomAndTheFalseWitness.the_power_has_two_fixed_points c).mp hcc with h0 | h1
    · left
      rw [← hc, h0]
      exact map_zero _
    · right
      rw [← hc, h1]
      exact map_one _
  · rintro (h0 | h1) x
    · exact (a_morada_e_o_que_comuta_com_o_posto hP x).mpr (by rw [h0, zero_mul, mul_zero])
    · exact (a_morada_e_o_que_comuta_com_o_posto hP x).mpr (by rw [h1, one_mul, mul_one])

/-- [Nonempty n] pode cair em a_identidade_e_o_ato_de_ser (n vazio: os dois lados sao verdadeiros). -/
theorem T5e {n : Type} [Fintype n] [DecidableEq n] (N : Identidade.Nome n) :
    Identidade.euSou n = Identidade.oQueSou N ↔ ∀ v : n → ℂ, Matrix.mulVec N.P v = v := by
  by_cases hn : Nonempty n
  · exact a_identidade_e_o_ato_de_ser N
  · have hE : IsEmpty n := not_nonempty_iff.mp hn
    constructor
    · intro _ v
      funext i
      exact (hE.false i).elim
    · intro _
      unfold Identidade.euSou Identidade.oQueSou
      rw [Identidade.gibbs_absolute, Identidade.gibbs_absolute]
      have : (1 : Matrix n n ℂ) = N.P := Subsingleton.elim _ _
      rw [this]

#print axioms T5a
#print axioms T5b
#print axioms T5c
#print axioms T5d
#print axioms T5e
