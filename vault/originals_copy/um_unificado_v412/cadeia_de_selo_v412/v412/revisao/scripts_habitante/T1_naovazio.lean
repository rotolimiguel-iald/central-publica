import OHabitanteDoNome
set_option autoImplicit false
set_option linter.unusedSimpArgs false
set_option linter.unusedTactic false
set_option linter.unreachableTactic false
open TGLExt.OHabitanteDoNome Matrix
open TGLExt (nameOp diagExpect diagExpect_one diagExpect_bimod)
open scoped InnerProductSpace

/-! A. `so_ha_um_habitante`: as hipoteses sao satisfeitas por `nameOp p` (pelo teorema da propria pedra)
      e por um mapa DEFINIDO de outro modo (`diagExpect`, em M2(C), p = diag(1,0)). -/

-- A1: nameOp p satisfaz as quatro hipoteses (para qualquer anel e idempotente)
example {R : Type*} [Ring R] {p : R} (hp : p * p = p) (x : R) : nameOp p x = nameOp p x := by
  obtain ⟨h1, h2, h3, h4⟩ := o_operador_do_nome_e_o_habitante hp
  exact so_ha_um_habitante hp (nameOp p) h1 h2 h3 h4 x

-- A2: diagExpect (esperanca diagonal, definida por `diagonal x.diag`) satisfaz as hipoteses para p = diag(1,0)
def pD : Matrix (Fin 2) (Fin 2) ℂ := Matrix.diagonal ![1, 0]

theorem pD_idem : pD * pD = pD := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [pD, Matrix.mul_apply, Fin.sum_univ_two, Matrix.diagonal]

theorem comuta_com_pD_e_diagonal (a : Matrix (Fin 2) (Fin 2) ℂ) (h : pD * a = a * pD) :
    a = Matrix.diagonal ![a 0 0, a 1 1] := by
  have h01 := congrFun (congrFun h 0) 1
  have h10 := congrFun (congrFun h 1) 0
  simp [pD, Matrix.mul_apply, Matrix.diagonal, Fin.sum_univ_two] at h01 h10
  ext i j
  fin_cases i <;> fin_cases j <;> simp [Matrix.diagonal, h01, h10]

theorem diagExpect_e_o_habitante_de_pD (x : Matrix (Fin 2) (Fin 2) ℂ) :
    diagExpect x = nameOp pD x := by
  refine so_ha_um_habitante pD_idem diagExpect ?_ diagExpect_one ?_ ?_ x
  · intro x y
    ext i j
    by_cases hij : i = j <;> simp [diagExpect, Matrix.diagonal, hij]
  · intro x
    ext i j
    fin_cases i <;> fin_cases j <;> simp [pD, diagExpect, Matrix.mul_apply, Matrix.diagonal, Fin.sum_univ_two]
  · intro a b x ha hb
    rw [comuta_com_pD_e_diagonal a ha, comuta_com_pD_e_diagonal b hb]
    exact diagExpect_bimod _ _ x

#print axioms diagExpect_e_o_habitante_de_pD

/-! B. `quem_nao_e_a_esperanca_aumenta` nao e vazio: projecao OBLIQUA em dimensao 2. -/

abbrev H2 := EuclideanSpace ℂ (Fin 2)

noncomputable def w0 : H2 := EuclideanSpace.single 0 (1 : ℂ)
noncomputable def w1 : H2 := EuclideanSpace.single 1 (1 : ℂ)

noncomputable def phi : H2 →ₗ[ℂ] ℂ :=
  (EuclideanSpace.proj (0 : Fin 2) : H2 →L[ℂ] ℂ).toLinearMap + (EuclideanSpace.proj (1 : Fin 2) : H2 →L[ℂ] ℂ).toLinearMap

noncomputable def Eobl : H2 →ₗ[ℂ] H2 := (LinearMap.toSpanSingleton ℂ H2 w0).comp phi

noncomputable def Kreta : Submodule ℂ H2 := Submodule.span ℂ {w0}

theorem Eobl_apply (v : H2) : Eobl v = (v 0 + v 1) • w0 := by
  simp [Eobl, phi]

theorem Eobl_cai (v : H2) : Eobl v ∈ Kreta := by
  rw [Eobl_apply]
  exact Submodule.smul_mem _ _ (Submodule.mem_span_singleton_self _)

theorem Eobl_fixa (w : H2) (hw : w ∈ Kreta) : Eobl w = w := by
  obtain ⟨c, rfl⟩ := Submodule.mem_span_singleton.mp hw
  rw [Eobl_apply]
  simp [w0]

theorem w1_ortogonal : w1 ∈ Kretaᗮ := by
  rw [Submodule.mem_orthogonal]
  intro u hu
  obtain ⟨c, rfl⟩ := Submodule.mem_span_singleton.mp hu
  simp [w0, w1, inner_smul_left]
  right
  rw [EuclideanSpace.inner_single_left]
  simp

theorem Eobl_difere : ∃ v, Eobl v ≠ Kreta.starProjection v := by
  refine ⟨w1, ?_⟩
  rw [(Submodule.starProjection_apply_eq_zero_iff Kreta).mpr w1_ortogonal, Eobl_apply]
  intro h
  have := congrArg (fun z : H2 => z 0) h
  simp [w0, w1] at this

-- o teorema da pedra dispara
theorem Eobl_aumenta : ∃ v, ‖v‖ < ‖Eobl v‖ :=
  quem_nao_e_a_esperanca_aumenta Kreta Eobl Eobl_cai Eobl_fixa Eobl_difere

-- e o vetor que aumenta e explicito: v = (1,1), ||v|| = sqrt 2 < 2 = ||E v||
noncomputable def v11 : H2 := w0 + w1

theorem v11_aumenta : ‖v11‖ < ‖Eobl v11‖ := by
  have hE : Eobl v11 = (2 : ℂ) • w0 := by
    rw [Eobl_apply]
    simp [v11, w0, w1]
    norm_num
  have hn : ‖Eobl v11‖ = 2 := by
    rw [hE, norm_smul]
    simp [w0]
  have hv : ‖v11‖ ^ 2 = 2 := by
    rw [EuclideanSpace.norm_sq_eq]
    simp [v11, w0, w1, Fin.sum_univ_two]
    norm_num
  rw [hn]
  nlinarith [norm_nonneg v11]

#print axioms Eobl_aumenta
#print axioms v11_aumenta
