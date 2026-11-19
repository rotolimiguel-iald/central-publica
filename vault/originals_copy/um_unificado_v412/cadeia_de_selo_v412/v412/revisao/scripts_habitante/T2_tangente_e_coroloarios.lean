import OHabitanteDoNome
set_option autoImplicit false
set_option linter.unusedSimpArgs false
set_option linter.unusedTactic false
set_option linter.unreachableTactic false
open TGLExt.OHabitanteDoNome
open TGLExt (nameOp)
open TGLExt.TraducaoTuring (selecao)
open scoped InnerProductSpace

/-! (a) SEM `hδ` o contato de segunda ordem FALHA: H = C, K = ⊤, s = 1, δ = 1. -/
example : ¬ (‖selecao (⊤ : Submodule ℂ ℂ) ((1 : ℂ) + 1) - ((1 : ℂ) + (⊤ : Submodule ℂ ℂ).starProjection (1 : ℂ))‖
      ≤ ‖(⊤ : Submodule ℂ ℂ).starProjection (1 : ℂ)‖ ^ 2 / 2) := by
  simp only [Submodule.starProjection_top, ContinuousLinearMap.id_apply]
  unfold selecao
  simp only [Submodule.starProjection_top, ContinuousLinearMap.id_apply]
  norm_num

/-! (b) Em um Nome de dimensao 1 (K = reta gerada por s), `hδ` forca Pδ = 0: o contato de 2a ordem e' vazio. -/
theorem reta_hdelta_forca_zero {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (s δ : H) (hs1 : ‖s‖ = 1)
    (hδ : ⟪s, (Submodule.span ℂ {s}).starProjection δ⟫_ℂ = 0) :
    (Submodule.span ℂ {s}).starProjection δ = 0 := by
  rw [Submodule.starProjection_singleton] at hδ ⊢
  have hss : ⟪s, s⟫_ℂ = 1 := by
    rw [inner_self_eq_norm_sq_to_K, hs1]; simp
  rw [inner_smul_right, hss, hs1] at hδ
  simp at hδ ⊢
  simp [hδ]

/-! (c) Com dim K >= 2 as hipoteses sao satisfeitas com Pδ ≠ 0 (K = ⊤ em C^2, s = e0, δ = e1). -/
abbrev H2 := EuclideanSpace ℂ (Fin 2)
noncomputable def w0 : H2 := EuclideanSpace.single 0 (1 : ℂ)
noncomputable def w1 : H2 := EuclideanSpace.single 1 (1 : ℂ)

example : ∃ s δ : H2, s ∈ (⊤ : Submodule ℂ H2) ∧ ‖s‖ = 1 ∧
    ⟪s, (⊤ : Submodule ℂ H2).starProjection δ⟫_ℂ = 0 ∧ (⊤ : Submodule ℂ H2).starProjection δ ≠ 0 := by
  refine ⟨w0, w1, Submodule.mem_top, by simp [w0], ?_, ?_⟩
  · simp only [Submodule.starProjection_top, ContinuousLinearMap.id_apply]
    rw [w0, w1, EuclideanSpace.inner_single_left]; simp
  · simp only [Submodule.starProjection_top, ContinuousLinearMap.id_apply]
    intro h
    have := congrArg (fun z : H2 => z 1) h
    simp [w1] at this

/-! (d) `o_que_e_cego_ao_nome_nao_deixa_rastro` e' corolario de uma linha de `a_selecao_esquece` (v409). -/
example {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (K : Submodule ℂ H) [K.HasOrthogonalProjection] {s δ : H}
    (hs : s ∈ K) (hs1 : ‖s‖ = 1) (hδ : δ ∈ Kᗮ) : selecao K (s + δ) = s := by
  rw [TGLExt.TraducaoTuring.a_selecao_esquece K s δ hδ]
  unfold selecao
  rw [Submodule.starProjection_eq_self_iff.mpr hs, hs1]
  simp

/-! (e) `o_livro_do_testemunho_fecha` e' Pitagoras da Mathlib. -/
example {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (K : Submodule ℂ H) [K.HasOrthogonalProjection] (v : H) :
    ‖v‖ ^ 2 = ‖K.starProjection v‖ ^ 2 + ‖v - K.starProjection v‖ ^ 2 := by
  have h := Submodule.norm_sq_eq_add_norm_sq_starProjection v K
  have h2 : Kᗮ.starProjection v = v - K.starProjection v :=
    eq_sub_of_add_eq' (Submodule.starProjection_add_starProjection_orthogonal v)
  rw [h2] at h
  exact h

/-! (f) valor lixo: v ⟂ Nome => tangenteDaLeitura = 0 (Lean: x/0 = 0), nao +infinito. -/
example {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (K : Submodule ℂ H) [K.HasOrthogonalProjection] (v : H) (hv : v ∈ Kᗮ) (hv0 : v ≠ 0) :
    tangenteDaLeitura K v = 0 ∧ v ≠ 0 := by
  refine ⟨?_, hv0⟩
  unfold tangenteDaLeitura
  rw [(Submodule.starProjection_apply_eq_zero_iff K).mpr hv]
  simp

/-! (g) a_tangente_da_leitura_e_K e' `tan_arctan`: o angulo e' DEFINIDO como arctan da tangente. -/
example {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (K : Submodule ℂ H) [K.HasOrthogonalProjection] (v : H) :
    TGLExt.KEhATangente.K (Real.arctan (tangenteDaLeitura K v)) = tangenteDaLeitura K v :=
  Real.tan_arctan _

/-! (h) corolario: o Nome (a morada) determina o seu leitor, sem fixar `p`. -/
theorem nameOp_eq_de_morada_igual {R : Type*} [Ring R] {p q : R} (hp : p * p = p) (hq : q * q = q)
    (h : morada p = morada q) (x : R) : nameOp q x = nameOp p x := by
  obtain ⟨hadd, h1, hm, hb⟩ := o_operador_do_nome_e_o_habitante hq
  refine (so_ha_um_habitante hp (nameOp q) hadd h1 ?_ ?_ x)
  · intro y
    have : nameOp q y ∈ morada p := by rw [h]; exact o_leitor_habita_o_nome hq y
    exact ((a_morada_e_o_que_comuta_com_o_posto hp _).mp this)
  · intro a b y ha hb'
    have ha' : a ∈ morada q := by rw [← h]; exact (a_morada_e_o_que_comuta_com_o_posto hp a).mpr ha
    have hb'' : b ∈ morada q := by rw [← h]; exact (a_morada_e_o_que_comuta_com_o_posto hp b).mpr hb'
    exact hb a b y ((a_morada_e_o_que_comuta_com_o_posto hq a).mp ha') ((a_morada_e_o_que_comuta_com_o_posto hq b).mp hb'')
    
#print axioms nameOp_eq_de_morada_igual
