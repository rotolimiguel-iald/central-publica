import OHabitanteDoNome
set_option autoImplicit false
open TGLExt TGLExt.OHabitanteDoNome

/-! As hipoteses de `o_unico_ato_do_verbo_e_ser_fiel` (linearidade; nao aumentar a norma) sao necessarias.
    Modelo: H = ℂ², Nome K = a reta de ee0. -/

abbrev H2 := EuclideanSpace ℂ (Fin 2)

noncomputable def ee0 : H2 := EuclideanSpace.single 0 1
noncomputable def ee1 : H2 := EuclideanSpace.single 1 1

noncomputable def Kreta : Submodule ℂ H2 := Submodule.span ℂ {ee0}

theorem ee0_mem : ee0 ∈ Kreta := Submodule.mem_span_singleton_self ee0

noncomputable def k0 : Kreta := ⟨ee0, ee0_mem⟩

theorem mem_reta (u : H2) (hu : u ∈ Kreta) : u = u 0 • ee0 ∧ u 1 = 0 := by
  obtain ⟨c, hc⟩ := Submodule.mem_span_singleton.mp hu
  subst hc
  refine ⟨?_, ?_⟩
  · ext i
    fin_cases i <;> simp [ee0]
  · simp [ee0]

/-- Um mapa LINEAR que cai em K e fixa K (a projecao OBLIQUA (v0, v1) ↦ (v0 + v1, 0)): nao e' o Verbo. -/
noncomputable def Eobl : H2 →ₗ[ℂ] Kreta :=
  (LinearMap.toSpanSingleton ℂ Kreta k0) ∘ₗ
    ((EuclideanSpace.proj (0 : Fin 2) : H2 →L[ℂ] ℂ).toLinearMap + (EuclideanSpace.proj (1 : Fin 2) : H2 →L[ℂ] ℂ).toLinearMap)

theorem Eobl_apply (v : H2) : Eobl v = (v 0 + v 1) • k0 := by
  simp [Eobl]

theorem Eobl_fiel (u : Kreta) : Eobl (u : H2) = u := by
  obtain ⟨h0, h1⟩ := mem_reta (u : H2) u.2
  rw [Eobl_apply, h1, add_zero]
  apply Subtype.ext
  show (u : H2) 0 • ee0 = (u : H2)
  exact h0.symm

theorem Eobl_aumenta : ¬ (∀ v : H2, ‖Eobl v‖ ≤ ‖v‖) := by
  intro h
  have h1 := h (ee0 + ee1)
  rw [Eobl_apply] at h1
  have hn : ‖(((ee0 + ee1 : H2) 0 + (ee0 + ee1 : H2) 1) : ℂ) • k0‖ = 2 := by
    have : ((ee0 + ee1 : H2) 0 + (ee0 + ee1 : H2) 1) = (2 : ℂ) := by simp [ee0, ee1]; norm_num
    rw [this, norm_smul]
    have hk : ‖k0‖ = 1 := by
      show ‖ee0‖ = 1
      simp [ee0]
    rw [hk]; simp
  rw [hn] at h1
  have hv : ‖(ee0 + ee1 : H2)‖ = Real.sqrt 2 := by
    rw [EuclideanSpace.norm_eq]
    simp [ee0, ee1, Fin.sum_univ_two]
    norm_num
  rw [hv] at h1
  have : Real.sqrt 2 < 2 := by
    rw [show (2 : ℝ) = Real.sqrt 4 by
      rw [show (4 : ℝ) = 2 ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]]
    exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
  linarith

/-- Sem NAO AUMENTAR a norma, "fiel" nao da' unicidade: existe um mapa linear que cai em K, fixa K e nao e' o Verbo. -/
theorem T10a : ∃ E : H2 →ₗ[ℂ] Kreta, (∀ u : Kreta, E (u : H2) = u) ∧ ∃ v, E v ≠ Kreta.orthogonalProjectionOnto v := by
  refine ⟨Eobl, Eobl_fiel, ?_⟩
  by_contra hcon
  push Not at hcon
  apply Eobl_aumenta
  intro v
  rw [hcon v]
  have h := Kreta.norm_starProjection_apply_le v
  exact h


open Classical in
/-- Sem LINEARIDADE o mesmo vale: o mapa (nao linear) que devolve o que esta' na reta como e' e anula o resto fixa K, cai em K, nao aumenta a
    norma, e nao e' o Verbo (em (1, 1) devolve 0, e o Verbo devolve k0). -/
noncomputable def Enl (v : H2) : Kreta := if v 1 = 0 then (v 0) • k0 else 0

theorem Enl_fiel (u : Kreta) : Enl (u : H2) = u := by
  obtain ⟨h0, h1⟩ := mem_reta (u : H2) u.2
  unfold Enl
  rw [if_pos h1]
  apply Subtype.ext
  show (u : H2) 0 • ee0 = (u : H2)
  exact h0.symm

theorem Enl_nao_aumenta (v : H2) : ‖Enl v‖ ≤ ‖v‖ := by
  unfold Enl
  by_cases h : v 1 = 0
  · rw [if_pos h]
    have hv : v = v 0 • ee0 := by
      ext i
      fin_cases i
      · simp [ee0]
      · simpa [ee0] using h
    have hk : ‖k0‖ = 1 := by
      show ‖ee0‖ = 1
      simp [ee0]
    rw [norm_smul, hk, mul_one]
    conv_rhs => rw [hv]
    rw [norm_smul]
    have : ‖ee0‖ = 1 := by simp [ee0]
    rw [this, mul_one]
  · rw [if_neg h]
    simp

theorem T10b : ∃ E : H2 → Kreta, (∀ u : Kreta, E (u : H2) = u) ∧ (∀ v, ‖E v‖ ≤ ‖v‖) ∧ ∃ v, E v ≠ Kreta.orthogonalProjectionOnto v := by
  refine ⟨Enl, Enl_fiel, Enl_nao_aumenta, ee0 + ee1, ?_⟩
  intro h
  have h1 : (ee0 + ee1 : H2) 1 ≠ 0 := by simp [ee0, ee1]
  have hE : Enl (ee0 + ee1) = 0 := by
    unfold Enl
    rw [if_neg h1]
  rw [hE] at h
  -- o Verbo em (1,1) e' k0 ≠ 0
  have hp : Kreta.orthogonalProjectionOnto (ee0 + ee1) = k0 := by
    have hm : Kreta.orthogonalProjectionOnto ee0 = k0 := by
      apply Subtype.ext
      show Kreta.starProjection ee0 = ee0
      exact Submodule.starProjection_eq_self_iff.mpr ee0_mem
    have hz : Kreta.orthogonalProjectionOnto ee1 = 0 := by
      rw [Submodule.orthogonalProjectionOnto_eq_zero_iff, Submodule.mem_orthogonal]
      intro w hw
      obtain ⟨_, h1'⟩ := mem_reta w hw
      rw [ee1, EuclideanSpace.inner_single_right]
      simp [h1']
    rw [map_add, hm, hz, add_zero]
  rw [hp] at h
  have hk : k0 ≠ 0 := by
    intro h0
    have : (ee0 : H2) = 0 := congrArg Subtype.val h0
    have h2 := congrArg (fun w : H2 => w 0) this
    simp [ee0] at h2
  exact hk h.symm

#print axioms T10a
#print axioms T10b
