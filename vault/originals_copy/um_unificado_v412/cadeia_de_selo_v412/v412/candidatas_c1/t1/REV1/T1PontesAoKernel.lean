import T1CompostoFinito
import TGLExt.Ergodicity
import TGLExt.ErgodicMeanSection
import TGLExt.TheSingularExpectation

set_option autoImplicit false
noncomputable section

/-!
# A T1 na face finita: as pontes da candidata aos objetos que o kernel já tem
[candidata da gerência c1, 16/11/2026; nome provisório; nada instalado; o nome é do operador]

## De onde vem

A conferência distinta de 16/11 (revisor C4) achou que `T1CompostoFinito` redefinia, com nomes novos, objetos que o
kernel selado já tem, sem citar nem ligar. O revisor escreveu e compilou as pontes como sondas (S3 e S5); a gerência
as adota aqui, recompiladas, com os nomes do revisor. Nenhum teorema deste arquivo é da gerência.

## O que fica provado

1. **A ligação ao kernel.** A média gaussiana é o `TGLExt.dephase` do kernel com taxa `(√kᵢ − √kⱼ)²/2` e tempo `v`
   (`media_e_dephase`); a matriz das frequências é o `TGLExt.rhoD` nas frequências (`gerador_e_rhoD`, por `rfl`); a
   `esperanca` é a `TGLExt.specExpect` nas frequências (`esperanca_e_specExpect`) e, no espectro simples, a
   `TGLExt.diagExpect` (`esperanca_e_diagExpect`). Três teoremas da candidata saem inteiros do kernel
   (`media_compoe_pelo_kernel`, `idempotente_pelo_kernel`, `cai_no_comutante_pelo_kernel`), e o limite, no espectro
   simples, sai de `TGLExt.dephase_tendsto_expectation` já para a matriz inteira (`media_tende_pelo_kernel`).
2. **O composto num termo só** (`fixo_sse_polinomio`): com variância não nula e frequências distintas, uma matriz é
   fixa pela média se e somente se é um polinômio na matriz das frequências (`polinomio_e_fixo` é a volta).
3. **A ponte das frequências para os níveis**, com níveis não negativos: comutar com `diag √k` é comutar com `diag k`
   (`comuta_freq_sse_comuta_nivel`); o fixo da média é o comutante do gerador de níveis
   (`fixo_da_media_sse_comuta_nivel`); todo fixo é polinômio no gerador de níveis se e somente se os níveis são
   distintos (`o_fixo_e_gerado_pelo_nivel_sse`).
4. **A projeção como esperança:** unidade, traço, estrela e lei de bimódulo sobre o comutante (`esperanca_um`,
   `esperanca_traco`, `esperanca_estrela`, `esperanca_bimodulo`). A positividade não é termo aqui (o kernel a tem para
   a `diagExpect`).
5. **O limite da matriz inteira** (`a_media_tende_matriz`), na topologia produto.

## O que NÃO se afirma

O mesmo que em `T1CompostoFinito`: nada sobre o caso contínuo, nem sobre as hipóteses valerem no objeto da teoria. As
pontes ao kernel estão em `Type` (o universo em que o kernel enuncia).

Estatutos: `[REAL no sandbox]` os termos · escritos pelo revisor C4, adotados pela gerência.
-/

namespace TGLExt.T1CompostoFinito

open MeasureTheory ProbabilityTheory Matrix Polynomial Filter
open scoped NNReal Topology
open K07.T1

section geral

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- Todo polinômio na matriz das frequências é fixo pela média. -/
theorem polinomio_e_fixo (k : n → ℝ) (v : ℝ≥0) (p : Polynomial ℂ) :
    mediaGaussiana k v (aeval (Matrix.diagonal (freq k)) p) = aeval (Matrix.diagonal (freq k)) p := by
  rw [aeval_diagonal]
  ext i j
  rw [media_entrada]
  by_cases hij : i = j
  · subst hij
    simp [mult]
  · simp [Matrix.diagonal_apply_ne _ hij]

/-- **O COMPOSTO NUM TERMO SÓ.** Com variância não nula e frequências distintas, fixo = polinômio na matriz das
frequências. -/
theorem fixo_sse_polinomio (k : n → ℝ) {v : ℝ≥0} (hv : v ≠ 0)
    (hinj : Function.Injective (freq k)) (x : Matrix n n ℂ) :
    mediaGaussiana k v x = x ↔ ∃ p : Polynomial ℂ, aeval (Matrix.diagonal (freq k)) p = x := by
  constructor
  · exact (o_fixo_e_gerado_sse_espectro_simples k hv).mpr hinj x
  · rintro ⟨p, rfl⟩
    exact polinomio_e_fixo k v p

theorem comuta_diag_sse (d : n → ℂ) (x : Matrix n n ℂ) :
    Commute (Matrix.diagonal d) x ↔ ∀ i j, d i ≠ d j → x i j = 0 := by
  constructor
  · intro h i j hij
    have he := congrArg (fun a : Matrix n n ℂ => a i j) h.eq
    change (Matrix.diagonal d * x) i j = (x * Matrix.diagonal d) i j at he
    rw [Matrix.diagonal_mul, Matrix.mul_diagonal] at he
    have h2 : (d i - d j) * x i j = 0 := by
      rw [sub_mul, he]
      ring
    rcases mul_eq_zero.mp h2 with h0 | h0
    · exact absurd (sub_eq_zero.mp h0) hij
    · exact h0
  · intro h
    show Matrix.diagonal d * x = x * Matrix.diagonal d
    ext i j
    rw [Matrix.diagonal_mul, Matrix.mul_diagonal]
    by_cases hij : d i = d j
    · rw [hij]
      ring
    · rw [h i j hij]
      ring

/-- **A PONTE DAS FREQUÊNCIAS PARA OS NÍVEIS.** Com níveis não negativos, comutar com `diag √k` é comutar com
`diag k`. -/
theorem comuta_freq_sse_comuta_nivel (k : n → ℝ) (hk : ∀ i, 0 ≤ k i) (x : Matrix n n ℂ) :
    Commute (Matrix.diagonal (freq k)) x ↔
      Commute (Matrix.diagonal (fun i => ((k i : ℝ) : ℂ))) x := by
  rw [comuta_sse_entradas, comuta_diag_sse]
  constructor
  · intro h i j hij
    refine h i j (fun hs => hij ?_)
    have hkk : k i = k j := (Real.sqrt_inj (hk i) (hk j)).mp hs
    simp only [hkk]
  · intro h i j hij
    refine h i j (fun hc => hij ?_)
    have hc' : ((k i : ℝ) : ℂ) = ((k j : ℝ) : ℂ) := hc
    have hkk : k i = k j := by exact_mod_cast hc'
    rw [hkk]

/-- O fixo da média é o comutante do gerador de NÍVEIS (com `k ≥ 0` dito no enunciado). -/
theorem fixo_da_media_sse_comuta_nivel (k : n → ℝ) (hk : ∀ i, 0 ≤ k i) {v : ℝ≥0} (hv : v ≠ 0)
    (x : Matrix n n ℂ) :
    mediaGaussiana k v x = x ↔ Commute (Matrix.diagonal (fun i => ((k i : ℝ) : ℂ))) x :=
  (fixo_da_media_sse_comuta k hv x).trans (comuta_freq_sse_comuta_nivel k hk x)

/-- Todo fixo é polinômio no gerador de NÍVEIS se e somente se os níveis são distintos. -/
theorem o_fixo_e_gerado_pelo_nivel_sse (k : n → ℝ) (hk : ∀ i, 0 ≤ k i) {v : ℝ≥0} (hv : v ≠ 0) :
    (∀ x : Matrix n n ℂ, mediaGaussiana k v x = x →
        ∃ p : Polynomial ℂ, aeval (Matrix.diagonal (fun i => ((k i : ℝ) : ℂ))) p = x) ↔
      Function.Injective k := by
  have hinj : Function.Injective (fun i => ((k i : ℝ) : ℂ)) ↔ Function.Injective k := by
    constructor
    · intro h i j hij
      exact h (by simp only [hij])
    · intro h i j hij
      have hij' : ((k i : ℝ) : ℂ) = ((k j : ℝ) : ℂ) := hij
      exact h (by exact_mod_cast hij')
  rw [← hinj, ← commutant_generated_iff_injective (fun i => ((k i : ℝ) : ℂ))]
  constructor
  · intro h x hx
    exact h x ((fixo_da_media_sse_comuta_nivel k hk hv x).mpr hx)
  · intro h x hx
    exact h x ((fixo_da_media_sse_comuta_nivel k hk hv x).mp hx)

omit [Fintype n] in
theorem esperanca_um (k : n → ℝ) : esperanca k (1 : Matrix n n ℂ) = 1 := by
  ext i j
  unfold esperanca
  simp only [Matrix.of_apply]
  by_cases hij : i = j
  · subst hij
    simp
  · simp [Matrix.one_apply_ne hij]

omit [DecidableEq n] in
theorem esperanca_traco (k : n → ℝ) (x : Matrix n n ℂ) : (esperanca k x).trace = x.trace := by
  simp [Matrix.trace, esperanca]

omit [Fintype n] [DecidableEq n] in
theorem esperanca_estrela (k : n → ℝ) (x : Matrix n n ℂ) :
    esperanca k x.conjTranspose = (esperanca k x).conjTranspose := by
  ext i j
  simp only [esperanca, Matrix.of_apply, Matrix.conjTranspose_apply]
  by_cases hij : Real.sqrt (k i) = Real.sqrt (k j)
  · rw [if_pos hij, if_pos hij.symm]
  · rw [if_neg hij, if_neg (fun h => hij h.symm), star_zero]

/-- A lei de bimódulo sobre o comutante: `E(a x b) = a E(x) b`. -/
theorem esperanca_bimodulo (k : n → ℝ) (a b x : Matrix n n ℂ)
    (ha : Commute (Matrix.diagonal (freq k)) a) (hb : Commute (Matrix.diagonal (freq k)) b) :
    esperanca k (a * x * b) = a * esperanca k x * b := by
  have ha' := (comuta_sse_entradas k a).mp ha
  have hb' := (comuta_sse_entradas k b).mp hb
  ext i j
  simp only [esperanca, Matrix.of_apply, Matrix.mul_apply, Finset.sum_mul]
  by_cases hij : Real.sqrt (k i) = Real.sqrt (k j)
  · rw [if_pos hij]
    refine Finset.sum_congr rfl fun m _ => Finset.sum_congr rfl fun l _ => ?_
    by_cases hlm : Real.sqrt (k l) = Real.sqrt (k m)
    · rw [if_pos hlm]
    · rw [if_neg hlm, mul_zero, zero_mul]
      by_cases hil : Real.sqrt (k i) = Real.sqrt (k l)
      · have hmj : Real.sqrt (k m) ≠ Real.sqrt (k j) := fun h => hlm (by rw [← hil, hij, h])
        rw [hb' m j hmj, mul_zero]
      · rw [ha' i l hil, zero_mul, zero_mul]
  · rw [if_neg hij]
    symm
    refine Finset.sum_eq_zero fun m _ => Finset.sum_eq_zero fun l _ => ?_
    by_cases hlm : Real.sqrt (k l) = Real.sqrt (k m)
    · rw [if_pos hlm]
      by_cases hil : Real.sqrt (k i) = Real.sqrt (k l)
      · have hmj : Real.sqrt (k m) ≠ Real.sqrt (k j) := fun h => hij (by rw [hil, hlm, h])
        rw [hb' m j hmj, mul_zero]
      · rw [ha' i l hil, zero_mul, zero_mul]
    · rw [if_neg hlm, mul_zero, zero_mul]

/-- O limite da MATRIZ (topologia produto), a partir do termo entrada a entrada. -/
theorem a_media_tende_matriz (k : n → ℝ) (x : Matrix n n ℂ) :
    Tendsto (fun t : ℝ => mediaGaussiana k (Real.toNNReal t) x) atTop (𝓝 (esperanca k x)) :=
  tendsto_pi_nhds.mpr fun i => tendsto_pi_nhds.mpr fun j => a_media_tende_a_esperanca k x i j

end geral

/-! ## A fiação ao kernel (`Ergodicity`, `EquivariantSection`, `CondExpect`) -/

section kernel

variable {m : Type} [Fintype m] [DecidableEq m]

/-- A média gaussiana É o semigrupo de dephasing do kernel, com taxa `(√kᵢ − √kⱼ)²/2` e tempo `v`. -/
theorem media_e_dephase (k : m → ℝ) (v : ℝ≥0) (x : Matrix m m ℂ) :
    mediaGaussiana k v x =
      TGLExt.dephase (fun i j => (Real.sqrt (k i) - Real.sqrt (k j)) ^ 2 / 2) (v : ℝ) x := by
  ext i j
  rw [media_entrada]
  simp only [TGLExt.dephase, Matrix.of_apply, mult]
  congr 3
  ring

/-- `media_compoe` é instância de `TGLExt.dephase_add`. -/
theorem media_compoe_pelo_kernel (k : m → ℝ) (v w : ℝ≥0) (x : Matrix m m ℂ) :
    mediaGaussiana k v (mediaGaussiana k w x) = mediaGaussiana k (v + w) x := by
  rw [media_e_dephase, media_e_dephase, media_e_dephase, NNReal.coe_add, TGLExt.dephase_add]

omit [Fintype m] [DecidableEq m] in
/-- A `esperanca` é a seção espectral do kernel nas frequências `√k`. -/
theorem esperanca_e_specExpect (k : m → ℝ) (x : Matrix m m ℂ) :
    esperanca k x = TGLExt.specExpect (fun i => Real.sqrt (k i)) x := by
  ext i j
  by_cases h : Real.sqrt (k i) = Real.sqrt (k j) <;> simp [esperanca, h]

omit [Fintype m] in
/-- A matriz das frequências é o `rhoD` do kernel nas frequências. -/
theorem gerador_e_rhoD (k : m → ℝ) :
    Matrix.diagonal (freq k) = TGLExt.rhoD (fun i => Real.sqrt (k i)) := rfl

/-- `esperanca_idempotente` é instância de `TGLExt.specExpect_idem`. -/
theorem idempotente_pelo_kernel (k : m → ℝ) (x : Matrix m m ℂ) :
    esperanca k (esperanca k x) = esperanca k x := by
  rw [esperanca_e_specExpect, esperanca_e_specExpect, TGLExt.specExpect_idem]

/-- `esperanca_cai_no_comutante` é instância de `TGLExt.rhoD_commute_specExpect`. -/
theorem cai_no_comutante_pelo_kernel (k : m → ℝ) (x : Matrix m m ℂ) :
    Commute (Matrix.diagonal (freq k)) (esperanca k x) := by
  rw [esperanca_e_specExpect, gerador_e_rhoD]
  exact TGLExt.rhoD_commute_specExpect (fun i => Real.sqrt (k i)) x

omit [Fintype m] in
/-- No espectro simples a `esperanca` é a `diagExpect` do kernel. -/
theorem esperanca_e_diagExpect (k : m → ℝ) (hinj : Function.Injective (freq k)) (x : Matrix m m ℂ) :
    esperanca k x = TGLExt.diagExpect x := by
  ext i j
  simp only [esperanca, Matrix.of_apply, TGLExt.diagExpect]
  by_cases hij : i = j
  · subst hij
    simp
  · have hne : Real.sqrt (k i) ≠ Real.sqrt (k j) := by
      intro h
      apply hij
      apply hinj
      unfold freq
      rw [h]
    rw [if_neg hne, Matrix.diagonal_apply_ne _ hij]

/-- No espectro simples o limite sai de `TGLExt.dephase_tendsto_expectation`, já para a matriz inteira. -/
theorem media_tende_pelo_kernel (k : m → ℝ) (hinj : Function.Injective (freq k)) (x : Matrix m m ℂ) :
    Tendsto (fun t : ℝ => mediaGaussiana k (Real.toNNReal t) x) atTop (𝓝 (TGLExt.diagExpect x)) := by
  have hk := TGLExt.dephase_tendsto_expectation
    (fun i j => (Real.sqrt (k i) - Real.sqrt (k j)) ^ 2 / 2)
    (fun i => by simp)
    (fun i j hij => by
      have hne : Real.sqrt (k i) - Real.sqrt (k j) ≠ 0 := by
        intro h
        apply hij
        apply hinj
        unfold freq
        rw [sub_eq_zero.mp h]
      show 0 < (Real.sqrt (k i) - Real.sqrt (k j)) ^ 2 / 2
      positivity) x
  refine hk.congr' ?_
  filter_upwards [eventually_ge_atTop (0 : ℝ)] with t ht
  rw [media_e_dephase, Real.coe_toNNReal t ht]

end kernel

#print axioms polinomio_e_fixo
#print axioms fixo_sse_polinomio
#print axioms comuta_diag_sse
#print axioms comuta_freq_sse_comuta_nivel
#print axioms fixo_da_media_sse_comuta_nivel
#print axioms o_fixo_e_gerado_pelo_nivel_sse
#print axioms esperanca_um
#print axioms esperanca_traco
#print axioms esperanca_estrela
#print axioms esperanca_bimodulo
#print axioms a_media_tende_matriz
#print axioms media_e_dephase
#print axioms media_compoe_pelo_kernel
#print axioms esperanca_e_specExpect
#print axioms gerador_e_rhoD
#print axioms idempotente_pelo_kernel
#print axioms cai_no_comutante_pelo_kernel
#print axioms esperanca_e_diagExpect
#print axioms media_tende_pelo_kernel

end TGLExt.T1CompostoFinito
