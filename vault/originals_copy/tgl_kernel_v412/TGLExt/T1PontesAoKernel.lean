import TGLExt.T1CompostoFinito
import TGLExt.Ergodicity
import TGLExt.EquivariantSection
import TGLExt.CondExpect

set_option autoImplicit false
noncomputable section

/-!
# A T1 na face finita: as pontes aos objetos que o kernel já tem

## O que as pontes ligam

`T1CompostoFinito` define, com nomes próprios, objetos que o kernel selado já tem. As pontes abaixo ligam cada
definição ao objeto do kernel, na saída (itens 1 e 3) e na entrada (item 2).

## Nota sobre a palavra estado

O kernel define `rhoD d = diag(d)`, sem normalizar o traço. O que as pontes de entrada usam é a matriz positiva
diagonal `D` de pesos `e^{√k}`; o logaritmo de `D` é a matriz das frequências. Em dimensão positiva, a densidade do
estado é `D/Tr(D)`. A normalização subtrai `log Tr(D)` vezes a identidade ao gerador e conserva o fluxo, as médias e
os fixos (na fórmula do kernel entram só diferenças de logaritmos). Exemplo: em dimensão dois com os dois
níveis zero, `D = I` tem traço 2; o estado é `I/2`, com logaritmo `−log 2 · I`, e a matriz das frequências é zero.
Onde as docstrings abaixo dizem estado de pesos, leia-se a matriz `D` desses pesos, antes de normalizar.

## O que fica provado

1. **A ligação ao kernel, na saída.** A média gaussiana é o `TGLExt.dephase` do kernel com taxa `(√kᵢ − √kⱼ)²/2` e
   tempo `v` (`media_e_dephase`); a `esperanca` é a `TGLExt.specExpect` nas frequências (`esperanca_e_specExpect`), nos
   níveis quando são não negativos (`esperanca_e_specExpect_nivel`) e, no espectro simples, a `TGLExt.diagExpect`
   (`esperanca_e_diagExpect`). O `dephase` do kernel é genérico na taxa; a taxa que ele nomeia (`modularGap`,
   `|log dᵢ − log dⱼ|`) não é a da média gaussiana (metade do quadrado dessa diferença): mesma família, mesmo fixo,
   mesmo limite.
2. **A ligação ao kernel, na entrada.** A conjugação pelas fases é o fluxo modular `TGLExt.sigma` do estado diagonal de
   pesos `e^{√k}` (`conjugacao_e_sigma`), e a própria média é a média gaussiana desse fluxo, entrada por entrada
   (`media_e_a_media_do_sigma`); o sinal dos pesos é escolha: com `e^{−√k}` o fluxo é o mesmo com o tempo invertido
   (`sinal_dos_pesos_e_inversao_do_tempo`), e a média e o fixo não mudam; a matriz das frequências é `logRho D`, para a
   diagonal positiva `D = diag(e^{√k})`, antes de normalizar o traço
   (`frequencias_e_logRho`); a média gaussiana do fluxo modular do kernel é o dephasing do kernel, para pesos
   positivos quaisquer (`media_gaussiana_do_sigma_e_dephase`); e ★ ser fixo por UMA média gaussiana de variância não
   nula é ser fixo por TODO o fluxo modular (`fixo_da_media_sse_fixo_do_fluxo`, sobre a estrela do kernel
   `sigma_fixed_iff_specExpect`).
3. **Repetições, ditas:** `media_compoe_pelo_kernel`, `idempotente_pelo_kernel` e `cai_no_comutante_pelo_kernel` têm o
   mesmo enunciado de três teoremas de `T1CompostoFinito`, com a prova pelo kernel; `esperanca_um` e
   `esperanca_e_diagExpect` são instâncias de `specExpect_one` e `specExpect_of_injective`, provadas à mão;
   `esperanca_positiva_pelo_kernel` é caso de `esperanca_posSemidef`; `fixo_sse_specExpect` é `fixo_sse_esperanca` com
   o objeto do kernel; `media_zero` é instância de `dephase_zero`, provada à mão.
4. **O composto num termo só**, nas frequências (`fixo_sse_polinomio`; `polinomio_e_fixo` é a volta) e nos níveis não
   negativos e distintos (`fixo_sse_polinomio_nivel`; `polinomio_nivel_e_fixo`).
5. **A ponte das frequências para os níveis**, com níveis não negativos: comutar com `diag √k` é comutar com `diag k`
   (`comuta_freq_sse_comuta_nivel`); o fixo da média é o comutante do gerador de níveis
   (`fixo_da_media_sse_comuta_nivel`); todo fixo é polinômio no gerador de níveis se e somente se os níveis são
   distintos (`o_fixo_e_gerado_pelo_nivel_sse`).
6. **A projeção como esperança:** unidade, traço, estrela, lei de bimódulo sobre o comutante e positividade, também
   com frequências repetidas (`esperanca_um`, `esperanca_traco`, `esperanca_estrela`, `esperanca_bimodulo`,
   `esperanca_posSemidef`).
7. **O limite da matriz inteira** (`a_media_tende_matriz`), na topologia produto; e a unidade do semigrupo
   (`media_zero`).

## O que NÃO se afirma

O mesmo que em `T1CompostoFinito`: nada sobre o caso contínuo, nem sobre as hipóteses valerem no objeto da teoria. As
pontes ao kernel estão em `Type` (o universo em que o kernel enuncia).

Estatutos: `[REAL no sandbox]` os termos.
-/

namespace TGLExt.T1CompostoFinito

open MeasureTheory ProbabilityTheory Matrix Polynomial Filter
open scoped NNReal Topology ComplexOrder
open K07.T1 ChatgptAudit

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

/-- Comutar com uma matriz diagonal: as entradas que ligam valores diferentes da diagonal são nulas. -/
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
/-- A projeção leva a unidade na unidade. -/
theorem esperanca_um (k : n → ℝ) : esperanca k (1 : Matrix n n ℂ) = 1 := by
  ext i j
  unfold esperanca
  simp only [Matrix.of_apply]
  by_cases hij : i = j
  · subst hij
    simp
  · simp [Matrix.one_apply_ne hij]

omit [DecidableEq n] in
/-- A projeção preserva o traço. -/
theorem esperanca_traco (k : n → ℝ) (x : Matrix n n ℂ) : (esperanca k x).trace = x.trace := by
  simp [Matrix.trace, esperanca]

omit [Fintype n] [DecidableEq n] in
/-- A projeção comuta com a estrela. -/
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
/-- Mesma matriz, outro papel. Esta igualdade identifica, por definição, `diag(√k)` com `rhoD (√k)`: no kernel `rhoD`
é só a matriz diagonal dos números dados, e aqui os números são as frequências `√k` (a matriz pode ter traço zero, e é
a matriz nula quando todo `kᵢ = 0`). O gerador do fluxo é outra coisa: `logRho D`, para a diagonal
estritamente positiva `D = diag(e^{√k})` (`frequencias_e_logRho`). A igualdade por `rfl` vale para a álgebra
(comutante, seção). O nome do teorema diz menos que esta docstring: a igualdade é só de matrizes. -/
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


/-! ## As pontes de ENTRADA

A conjugação pelas fases é o `TGLExt.sigma` do kernel no estado diagonal de pesos `e^{√k}`; a matriz das frequências
é o `logRho` desse estado (e não o estado `rhoD`); a média gaussiana do fluxo modular do kernel é o dephasing do
kernel; ser fixo por UMA média é ser fixo por TODO o fluxo; a projeção é positiva também com frequências repetidas;
e o composto num termo só nos NÍVEIS. -/

section entradaGeral

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- Ser fixo por UMA média de variância não nula é ser ponto fixo da projeção. -/
theorem fixo_sse_esperanca (k : n → ℝ) {v : ℝ≥0} (hv : v ≠ 0) (x : Matrix n n ℂ) :
    mediaGaussiana k v x = x ↔ x = esperanca k x := by
  rw [fixo_da_media_sse_comuta k hv x]
  constructor
  · intro h
    exact (esperanca_fixa_o_comutante k x h).symm
  · intro h
    rw [h]
    exact esperanca_cai_no_comutante k x

/-- Todo polinômio na matriz dos NÍVEIS é fixo (sem hipótese sobre o sinal dos níveis). -/
theorem polinomio_nivel_e_fixo (k : n → ℝ) (v : ℝ≥0) (p : Polynomial ℂ) :
    mediaGaussiana k v (aeval (Matrix.diagonal (fun i => ((k i : ℝ) : ℂ))) p) =
      aeval (Matrix.diagonal (fun i => ((k i : ℝ) : ℂ))) p := by
  rw [aeval_diagonal]
  ext i j
  rw [media_entrada]
  by_cases hij : i = j
  · subst hij
    simp [mult]
  · simp [Matrix.diagonal_apply_ne _ hij]

/-- **O COMPOSTO NUM TERMO SÓ, NOS NÍVEIS.** Com níveis não negativos e distintos e variância não nula, ser fixo é ser
polinômio na matriz dos níveis. -/
theorem fixo_sse_polinomio_nivel (k : n → ℝ) (hk : ∀ i, 0 ≤ k i) {v : ℝ≥0} (hv : v ≠ 0)
    (hinj : Function.Injective k) (x : Matrix n n ℂ) :
    mediaGaussiana k v x = x ↔
      ∃ p : Polynomial ℂ, aeval (Matrix.diagonal (fun i => ((k i : ℝ) : ℂ))) p = x := by
  constructor
  · exact (o_fixo_e_gerado_pelo_nivel_sse k hk hv).mpr hinj x
  · rintro ⟨p, rfl⟩
    exact polinomio_nivel_e_fixo k v p

end entradaGeral

section entradaKernel

variable {m : Type} [Fintype m] [DecidableEq m]

/-- A mesma, com o objeto do kernel. -/
theorem fixo_sse_specExpect (k : m → ℝ) {v : ℝ≥0} (hv : v ≠ 0) (x : Matrix m m ℂ) :
    mediaGaussiana k v x = x ↔ x = TGLExt.specExpect (fun i => Real.sqrt (k i)) x := by
  rw [← esperanca_e_specExpect]
  exact fixo_sse_esperanca k hv x

omit [Fintype m] [DecidableEq m] in
/-- Com níveis não negativos, a `esperanca` é a seção espectral do kernel nos NÍVEIS. -/
theorem esperanca_e_specExpect_nivel (k : m → ℝ) (hk : ∀ i, 0 ≤ k i) (x : Matrix m m ℂ) :
    esperanca k x = TGLExt.specExpect k x := by
  ext i j
  by_cases h : k i = k j
  · simp [esperanca, h]
  · have hs : Real.sqrt (k i) ≠ Real.sqrt (k j) :=
      fun hs => h ((Real.sqrt_inj (hk i) (hk j)).mp hs)
    simp [esperanca, h, hs]

/-- A conjugação pelas fases É o fluxo modular do kernel na matriz positiva diagonal de pesos `e^{√k}` (o estado é ela
dividida pelo traço; o fluxo é o mesmo: nota do cabeçalho). -/
theorem conjugacao_e_sigma (k : m → ℝ) (s : ℝ) (x : Matrix m m ℂ) :
    phaseMatrix k s * x * (phaseMatrix k s).conjTranspose =
      TGLExt.sigma (TGLExt.rhoD (fun i => Real.exp (Real.sqrt (k i)))) s x := by
  ext i j
  rw [phaseMatrix_conjugation_entry,
    TGLExt.sigma_diagonal_apply _ (fun i => Real.exp_pos _) s x i j]
  congr 1
  unfold modularPhase
  congr 1
  simp only [Real.log_exp]
  push_cast
  ring

/-- **A MÉDIA GAUSSIANA DO FLUXO MODULAR DO KERNEL É O DEPHASING DO KERNEL**, para pesos positivos quaisquer: a taxa é
metade do quadrado da diferença dos logaritmos. -/
theorem media_gaussiana_do_sigma_e_dephase (d : m → ℝ) (hd : ∀ i, 0 < d i) (v : ℝ≥0)
    (x : Matrix m m ℂ) (i j : m) :
    ∫ s : ℝ, TGLExt.sigma (TGLExt.rhoD d) s x i j ∂gaussianReal 0 v =
      TGLExt.dephase (fun i j => (Real.log (d i) - Real.log (d j)) ^ 2 / 2) (v : ℝ) x i j := by
  have hpt : ∀ s : ℝ, TGLExt.sigma (TGLExt.rhoD d) s x i j =
      modularPhase s (Real.log (d i) - Real.log (d j)) * x i j := by
    intro s
    rw [TGLExt.sigma_diagonal_apply d hd s x i j]
    congr 1
    unfold modularPhase
    congr 1
    push_cast
    ring
  simp only [hpt, integral_mul_const, gaussian_phase_integral, TGLExt.dephase, Matrix.of_apply]
  congr 3
  ring

/-- **A T1 FINITA NA LÍNGUA DO KERNEL.** Ser fixo por UMA média gaussiana de variância não nula é ser fixo por TODO o
fluxo modular do estado diagonal de pesos `e^{√k}`. Usa a estrela do kernel `sigma_fixed_iff_specExpect`. -/
theorem fixo_da_media_sse_fixo_do_fluxo (k : m → ℝ) {v : ℝ≥0} (hv : v ≠ 0) (x : Matrix m m ℂ) :
    mediaGaussiana k v x = x ↔
      ∀ t : ℝ, TGLExt.sigma (TGLExt.rhoD (fun i => Real.exp (Real.sqrt (k i)))) t x = x := by
  rw [fixo_sse_specExpect k hv x,
    TGLExt.sigma_fixed_iff_specExpect (fun i => Real.exp (Real.sqrt (k i))) (fun i => Real.exp_pos _) x]
  have h : TGLExt.specExpect (fun i => Real.exp (Real.sqrt (k i))) x =
      TGLExt.specExpect (fun i => Real.sqrt (k i)) x := by
    ext i j
    simp [Real.exp_eq_exp]
  rw [h]

/-- A matriz das frequências é o `logRho` do kernel aplicado à matriz positiva diagonal de pesos `e^{√k}`, antes de
normalizar o traço (e não à matriz `rhoD` de pesos `√k`, que é só a mesma matriz com outro papel). O gerador do estado
normalizado difere deste por um múltiplo da identidade: nota do cabeçalho. -/
theorem frequencias_e_logRho (k : m → ℝ) :
    Matrix.diagonal (freq k) =
      TGLExt.logRho (TGLExt.rhoD (fun i => Real.exp (Real.sqrt (k i)))) := by
  rw [TGLExt.logRho_diagonal _ (fun i => Real.exp_pos _)]
  simp only [Real.log_exp]
  rfl

omit [Fintype m] in
/-- No espectro simples a positividade sai do kernel (`diagExpect_posSemidef`). É caso de `esperanca_posSemidef`. -/
theorem esperanca_positiva_pelo_kernel (k : m → ℝ) (hinj : Function.Injective (freq k))
    {x : Matrix m m ℂ} (hx : x.PosSemidef) : (esperanca k x).PosSemidef := by
  rw [esperanca_e_diagExpect k hinj x]
  exact TGLExt.diagExpect_posSemidef hx

/-- A própria média é a média gaussiana do fluxo modular do kernel, entrada por entrada: é a ligação de entrada sobre a
definição `mediaGaussiana`, e não só sobre o integrando. -/
theorem media_e_a_media_do_sigma (k : m → ℝ) (v : ℝ≥0) (x : Matrix m m ℂ) (i j : m) :
    mediaGaussiana k v x i j =
      ∫ s : ℝ, TGLExt.sigma (TGLExt.rhoD (fun i => Real.exp (Real.sqrt (k i)))) s x i j ∂gaussianReal 0 v := by
  unfold mediaGaussiana
  rw [Matrix.of_apply]
  simp only [conjugacao_e_sigma]

/-- O sinal dos pesos é a inversão do tempo: o fluxo da matriz de pesos `e^{-√k}` no tempo `t` é o da matriz de pesos
`e^{√k}` no tempo `-t`. A escolha de `e^{√k}` nas pontes de entrada não muda a média nem o fixo. -/
theorem sinal_dos_pesos_e_inversao_do_tempo (k : m → ℝ) (t : ℝ) (x : Matrix m m ℂ) :
    TGLExt.sigma (TGLExt.rhoD (fun i => Real.exp (-Real.sqrt (k i)))) t x =
      TGLExt.sigma (TGLExt.rhoD (fun i => Real.exp (Real.sqrt (k i)))) (-t) x := by
  ext i j
  rw [TGLExt.sigma_diagonal_apply _ (fun i => Real.exp_pos _) t x i j,
    TGLExt.sigma_diagonal_apply _ (fun i => Real.exp_pos _) (-t) x i j]
  simp only [Real.log_exp]
  congr 2
  push_cast
  ring

end entradaKernel

section positividade

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- A projeção é POSITIVA também com frequências repetidas: `E(x) = Σ_λ P_λ x P_λ`, com `P_λ` a projeção diagonal do
conjunto de nível da frequência `λ`. -/
theorem esperanca_posSemidef (k : n → ℝ) {x : Matrix n n ℂ} (hx : x.PosSemidef) :
    (esperanca k x).PosSemidef := by
  classical
  let P : ℝ → Matrix n n ℂ := fun l =>
    Matrix.diagonal (fun i => if Real.sqrt (k i) = l then (1 : ℂ) else 0)
  have hterm : ∀ (l : ℝ) (i j : n), ((P l)ᴴ * x * P l) i j =
      (if Real.sqrt (k i) = l then (1 : ℂ) else 0) * x i j *
        (if Real.sqrt (k j) = l then (1 : ℂ) else 0) := by
    intro l i j
    simp only [P, Matrix.diagonal_conjTranspose, Matrix.diagonal_mul, Matrix.mul_diagonal,
      Pi.star_apply]
    split_ifs <;> simp
  have hsum : esperanca k x =
      ∑ l ∈ Finset.univ.image (fun i => Real.sqrt (k i)), (P l)ᴴ * x * P l := by
    ext i j
    rw [Matrix.sum_apply]
    simp only [hterm]
    rw [Finset.sum_eq_single (Real.sqrt (k i))]
    · by_cases hij : Real.sqrt (k i) = Real.sqrt (k j)
      · simp [esperanca, hij]
      · have hji : ¬ Real.sqrt (k j) = Real.sqrt (k i) := fun h => hij h.symm
        simp [esperanca, hij, hji]
    · intro l _ hl
      have hl' : ¬ Real.sqrt (k i) = l := fun h => hl h.symm
      simp [hl']
    · intro h
      exact absurd (Finset.mem_image_of_mem _ (Finset.mem_univ i)) h
  rw [hsum]
  exact Matrix.posSemidef_sum _ (fun l _ => hx.conjTranspose_mul_mul_same (P l))

end positividade

section unidade

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- A média de variância zero é a identidade (a unidade do semigrupo). -/
theorem media_zero (k : n → ℝ) (x : Matrix n n ℂ) : mediaGaussiana k 0 x = x := by
  ext i j
  rw [media_entrada]
  simp [mult]

end unidade


end TGLExt.T1CompostoFinito
