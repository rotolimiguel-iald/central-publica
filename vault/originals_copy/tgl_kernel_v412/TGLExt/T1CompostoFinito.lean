import TGLExt.T1GaussianSpectrum

set_option autoImplicit false
noncomputable section

/-!
# A T1 na face finita, num arquivo só: o fixo da média é o comutante da matriz das frequências, e é gerado por ela se e somente se as frequências são distintas (com níveis ≥ 0: o mesmo para a matriz dos níveis)

## O que o kernel já tem, e o que o arquivo acrescenta

O kernel selado JÁ TEM a T1 na face finita, com outros nomes. `Ergodicity`: o estado `rhoD`, o fluxo dele, o semigrupo
`dephase` (unidade, lei de semigrupo, limite da matriz inteira com taxas positivas) e o setor fixo do fluxo igual à
diagonal quando nenhum peso se repete (`sigma_fixed_iff_diag`). `EquivariantSection`: a seção `specExpect` (unital,
idempotente, cai no comutante) e o setor fixo do fluxo igual à seção, mesmo com pesos repetidos, para todos os tempos
(`sigma_fixed_iff_specExpect`). `TheSingularExpectation`: o setor fixo do dephasing é a diagonal (todos os tempos,
taxas positivas). `ErgodicMeanSection` e `AperiodicPhaseAverage`: as médias de Birkhoff e de Cesàro do fluxo tendem à
seção, com blocos repetidos. `CondExpect`: `diagExpect` bimodular, positiva, preserva o traço.

O esqueleto do composto (fixo da média = comutante; projeção por blocos; idempotência; limite) está em `T1_R2.lean`
(entrega K05, arquivada, fora do kernel), nos níveis, com `k ≥ 0` e com o fluxo posto por definição. `T1GaussianSpectrum` e `T1SemigroupProjection` provam
ingredientes; o composto num só termo é `fixo_sse_polinomio`, no módulo irmão.

Este arquivo escreve o composto sobre `T1GaussianSpectrum`, com definições próprias. O módulo irmão `T1PontesAoKernel`
liga cada definição daqui ao objeto do kernel, na saída e na entrada. NÃO são treze teoremas novos. Dos treze:
quatro peças novas, três instâncias do kernel e seis lemas de apoio (`mult_add`, `mult_eq_one_iff`,
`fixo_sse_entradas`, `comuta_sse_entradas`, `freq_injetiva_sse`, `esperanca_fixa_o_comutante`).

Novo EM RELAÇÃO AO KERNEL (as peças (b) e (d) têm em `T1_R2.lean` os termos `fixed_gaussianFlow_iff` e
`tendsto_gaussianFlow`, com o fluxo posto por definição; aqui saem da integral; (a) e o critério de (c) são termos de
`T1GaussianSpectrum`):

(a) a ligação da integral gaussiana ao dephasing: `media_entrada`. O kernel tinha a média de Cesàro do fluxo da torre e
    a gaussiana escalar; a taxa do `dephase` era posta, não calculada;
(b) o fixo de UMA só média de variância não nula é o comutante, mesmo com frequências repetidas:
    `fixo_da_media_sse_comuta`. O kernel pedia todos os tempos e, no dephasing, taxas positivas;
(c) o critério do polinômio aplicado ao fixo: `o_fixo_e_gerado_sse_espectro_simples`. O kernel tinha a diagonal
    maximal abeliana e o controle de pesos iguais em `Fin 2`;
(d) o limite com frequências repetidas: `a_media_tende_a_esperanca`. O kernel tinha o limite do dephasing sem
    repetição e os de Birkhoff e Cesàro com repetição.

São instâncias de teoremas do kernel (provado em `T1PontesAoKernel`): `media_compoe` (de `dephase_add`),
`esperanca_idempotente` (de `specExpect_idem`), `esperanca_cai_no_comutante` (de `rhoD_commute_specExpect`).

## O que fica provado (dimensão finita; base em que o gerador é diagonal)

Os TERMOS falam da matriz das FREQUÊNCIAS, `Matrix.diagonal (freq k)`, com `freq k i = √(k i)`; `k : n → ℝ` são os
níveis. A passagem à matriz dos níveis pede níveis não negativos e está em `T1PontesAoKernel`
(`fixo_da_media_sse_comuta_nivel`, `o_fixo_e_gerado_pelo_nivel_sse`, `fixo_sse_polinomio_nivel`). No Lean a raiz de
número negativo vale zero: com nível negativo as frases abaixo valem só para as frequências.

1. `media_entrada`: a média gaussiana, de variância `v`, das conjugações pelas fases `e^{i s √k}` multiplica a entrada
   `(i, j)` por `e^{−v (√kᵢ − √kⱼ)² / 2}` (é o termo de `T1GaussianSpectrum`). A média é definida entrada a entrada; coincide com a
   integral de Bochner da função matricial (não é termo aqui);
2. `media_compoe`: a média de variância `v` depois da de variância `w` é a de variância `v + w`; a de variância zero é
   a identidade (`media_zero`, no módulo irmão);
3. ★ `fixo_da_media_sse_comuta`: para `v ≠ 0`, uma matriz é fixa pela média se e somente se comuta com a matriz das
   frequências;
4. ★★ `o_fixo_e_gerado_sse_espectro_simples`: para `v ≠ 0`, todo fixo é um polinômio na matriz das frequências se e
   somente se as frequências são todas distintas (a volta, todo polinômio é fixo, está no módulo irmão:
   `polinomio_e_fixo`); com níveis não negativos, frequências distintas são níveis distintos (`freq_injetiva_sse`);
5. ★ `a_media_tende_a_esperanca`: quando a variância cresce, a média tende, entrada a entrada, à projeção `esperanca`
   sobre o comutante (para a matriz inteira, na topologia produto, que em dimensão finita é a da norma:
   `a_media_tende_matriz`, no módulo irmão). `esperanca` é uma projeção explícita: idempotente, cai no comutante e o
   fixa; unidade, traço, estrela, lei de bimódulo e positividade estão no módulo irmão.

Em língua simples: a média de variância não nula atenua as entradas que ligam frequências diferentes e deixa as outras
intactas; no limite de variância infinita as primeiras somem. Fica parada a matriz que comuta com o gerador; e o que
fica parado é a álgebra do gerador exatamente quando nenhum nível se repete (gerador de níveis não negativos). Na
face finita, nenhum nível se repete vale por duas condições do papel de uma vez, a do gerador e a ergodicidade.

## O que NÃO se afirma

* Nada sobre o caso contínuo (tipo III, produto cruzado, peso dual, traço e esperança no núcleo): segue no papel
  [DERIVED sobre KNOWN: Digernes–Takesaki (via Takesaki II e Andreou), dualidade de Takesaki, critério de
  Takesaki 1972, Umegaki, Segal–Dixmier, Lusin–Souslin; sem leitura no primário].
* Que as hipóteses do papel valham no objeto da teoria. Na face finita, “nenhuma frequência se repete”
  (multiplicidade um do gerador na matriz cheia) é o análogo de DUAS hipóteses do papel JUNTAS, a do gerador (`H_K̂`)
  e a ergodicidade (`H_erg`): a face finita não as separa; no papel, fixo = álgebra do gerador pede as duas
  (`T1_R3.md`, controle da necessidade). As três leituras do Axioma E (C
  gerado por K; C = Fix; C = o centralizador inteiro) não são decididas aqui.
* “Dissipação” e “variância = β·t”: são leitura do papel (`T1_R3.md`), não do termo, que só tem a variância `v`.

Estatutos: `[REAL no sandbox]` os termos · `[DECLARADO]` a dependência.
-/

namespace TGLExt.T1CompostoFinito

open MeasureTheory ProbabilityTheory Matrix Polynomial Filter
open scoped NNReal Topology
open K07.T1

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- A frequência do nível `i`: `√(k i)`. -/
def freq (k : n → ℝ) (i : n) : ℂ := ((Real.sqrt (k i) : ℝ) : ℂ)

/-- O multiplicador da entrada `(i, j)` na média de variância `v`. -/
def mult (k : n → ℝ) (v : ℝ≥0) (i j : n) : ℝ :=
  Real.exp (-(v : ℝ) * (Real.sqrt (k i) - Real.sqrt (k j)) ^ 2 / 2)

/-- A média gaussiana das conjugações pelas fases do gerador (entrada a entrada). -/
def mediaGaussiana (k : n → ℝ) (v : ℝ≥0) (x : Matrix n n ℂ) : Matrix n n ℂ :=
  Matrix.of fun i j =>
    ∫ s : ℝ, (phaseMatrix k s * x * (phaseMatrix k s).conjTranspose) i j ∂gaussianReal 0 v

/-- A projeção sobre o comutante da matriz das frequências: guarda as entradas de frequências iguais e apaga as
outras. É a `TGLExt.specExpect` do kernel nas frequências (`esperanca_e_specExpect`, no módulo `T1PontesAoKernel`). -/
def esperanca (k : n → ℝ) (x : Matrix n n ℂ) : Matrix n n ℂ :=
  Matrix.of fun i j => if Real.sqrt (k i) = Real.sqrt (k j) then x i j else 0

theorem media_entrada (k : n → ℝ) (v : ℝ≥0) (x : Matrix n n ℂ) (i j : n) :
    mediaGaussiana k v x i j = ((mult k v i j : ℝ) : ℂ) * x i j := by
  unfold mediaGaussiana mult
  rw [Matrix.of_apply]
  exact gaussian_conjugation_entry k v x i j

omit [Fintype n] [DecidableEq n] in
theorem mult_add (k : n → ℝ) (v w : ℝ≥0) (i j : n) :
    mult k v i j * mult k w i j = mult k (v + w) i j := by
  unfold mult
  rw [← Real.exp_add, NNReal.coe_add]
  congr 1
  ring

/-- A média compõe somando variâncias. -/
theorem media_compoe (k : n → ℝ) (v w : ℝ≥0) (x : Matrix n n ℂ) :
    mediaGaussiana k v (mediaGaussiana k w x) = mediaGaussiana k (v + w) x := by
  ext i j
  rw [media_entrada, media_entrada, media_entrada, ← mul_assoc, ← Complex.ofReal_mul, mult_add]

omit [Fintype n] [DecidableEq n] in
theorem mult_eq_one_iff (k : n → ℝ) {v : ℝ≥0} (hv : v ≠ 0) (i j : n) :
    mult k v i j = 1 ↔ Real.sqrt (k i) = Real.sqrt (k j) := by
  unfold mult
  rw [Real.exp_eq_one_iff]
  have hv' : (0 : ℝ) < v := by exact_mod_cast pos_iff_ne_zero.mpr hv
  constructor
  · intro h
    have h1 : (v : ℝ) * (Real.sqrt (k i) - Real.sqrt (k j)) ^ 2 = 0 := by linarith
    have h2 : (Real.sqrt (k i) - Real.sqrt (k j)) ^ 2 = 0 := by
      rcases mul_eq_zero.mp h1 with h0 | h0
      · exact absurd h0 hv'.ne'
      · exact h0
    have h3 : Real.sqrt (k i) - Real.sqrt (k j) = 0 := by
      rcases pow_eq_zero_iff (n := 2) (by norm_num) |>.mp h2 with h0
      exact h0
    linarith
  · intro h
    rw [h, sub_self]
    ring

theorem fixo_sse_entradas (k : n → ℝ) {v : ℝ≥0} (hv : v ≠ 0) (x : Matrix n n ℂ) :
    mediaGaussiana k v x = x ↔ ∀ i j, Real.sqrt (k i) ≠ Real.sqrt (k j) → x i j = 0 := by
  constructor
  · intro h i j hij
    have e : mediaGaussiana k v x i j = x i j := congrFun (congrFun h i) j
    rw [media_entrada] at e
    have hm : ((mult k v i j : ℝ) : ℂ) ≠ 1 := by
      intro h1
      exact hij ((mult_eq_one_iff k hv i j).mp (by exact_mod_cast h1))
    have h2 : (((mult k v i j : ℝ) : ℂ) - 1) * x i j = 0 := by
      rw [sub_mul, one_mul, e, sub_self]
    rcases mul_eq_zero.mp h2 with h0 | h0
    · exact absurd (sub_eq_zero.mp h0) hm
    · exact h0
  · intro h
    ext i j
    rw [media_entrada]
    by_cases hij : Real.sqrt (k i) = Real.sqrt (k j)
    · rw [(mult_eq_one_iff k hv i j).mpr hij]
      simp
    · rw [h i j hij, mul_zero]

theorem comuta_sse_entradas (k : n → ℝ) (x : Matrix n n ℂ) :
    Commute (Matrix.diagonal (freq k)) x ↔
      ∀ i j, Real.sqrt (k i) ≠ Real.sqrt (k j) → x i j = 0 := by
  constructor
  · intro h i j hij
    have he := congrArg (fun a : Matrix n n ℂ => a i j) h.eq
    change (Matrix.diagonal (freq k) * x) i j = (x * Matrix.diagonal (freq k)) i j at he
    rw [Matrix.diagonal_mul, Matrix.mul_diagonal] at he
    have h2 : (freq k i - freq k j) * x i j = 0 := by
      rw [sub_mul, he]
      ring
    rcases mul_eq_zero.mp h2 with h0 | h0
    · exfalso
      apply hij
      have h3 := sub_eq_zero.mp h0
      unfold freq at h3
      exact_mod_cast h3
    · exact h0
  · intro h
    show Matrix.diagonal (freq k) * x = x * Matrix.diagonal (freq k)
    ext i j
    rw [Matrix.diagonal_mul, Matrix.mul_diagonal]
    by_cases hij : Real.sqrt (k i) = Real.sqrt (k j)
    · unfold freq
      rw [hij]
      ring
    · rw [h i j hij]
      ring

/-- ★ **O FIXO DA MÉDIA É O COMUTANTE DA MATRIZ DAS FREQUÊNCIAS** (com níveis ≥ 0, da matriz dos níveis:
`fixo_da_media_sse_comuta_nivel`, no módulo irmão). -/
theorem fixo_da_media_sse_comuta (k : n → ℝ) {v : ℝ≥0} (hv : v ≠ 0) (x : Matrix n n ℂ) :
    mediaGaussiana k v x = x ↔ Commute (Matrix.diagonal (freq k)) x :=
  (fixo_sse_entradas k hv x).trans (comuta_sse_entradas k x).symm

/-- ★★ **O FIXO É GERADO PELA MATRIZ DAS FREQUÊNCIAS SE E SOMENTE SE O ESPECTRO É SIMPLES.** Todo ponto fixo da média é
um polinômio na matriz das frequências exatamente quando as frequências são todas distintas. -/
theorem o_fixo_e_gerado_sse_espectro_simples (k : n → ℝ) {v : ℝ≥0} (hv : v ≠ 0) :
    (∀ x : Matrix n n ℂ, mediaGaussiana k v x = x →
        ∃ p : Polynomial ℂ, aeval (Matrix.diagonal (freq k)) p = x) ↔
      Function.Injective (freq k) := by
  rw [← commutant_generated_iff_injective (freq k)]
  constructor
  · intro h x hx
    exact h x ((fixo_da_media_sse_comuta k hv x).mpr hx)
  · intro h x hx
    exact h x ((fixo_da_media_sse_comuta k hv x).mp hx)

omit [Fintype n] [DecidableEq n] in
/-- Com níveis não negativos, frequências distintas são níveis distintos. -/
theorem freq_injetiva_sse (k : n → ℝ) (hk : ∀ i, 0 ≤ k i) :
    Function.Injective (freq k) ↔ Function.Injective k := by
  constructor
  · intro h i j hij
    exact h (by unfold freq; rw [hij])
  · intro h i j hij
    unfold freq at hij
    have h2 : Real.sqrt (k i) = Real.sqrt (k j) := by exact_mod_cast hij
    exact h ((Real.sqrt_inj (hk i) (hk j)).mp h2)

omit [Fintype n] [DecidableEq n] in
/-- A projeção `esperanca` é idempotente. -/
theorem esperanca_idempotente (k : n → ℝ) (x : Matrix n n ℂ) :
    esperanca k (esperanca k x) = esperanca k x := by
  ext i j
  unfold esperanca
  simp only [Matrix.of_apply]
  split_ifs <;> rfl

/-- A projeção `esperanca` cai no comutante. -/
theorem esperanca_cai_no_comutante (k : n → ℝ) (x : Matrix n n ℂ) :
    Commute (Matrix.diagonal (freq k)) (esperanca k x) :=
  (comuta_sse_entradas k _).mpr (fun i j hij => by
    unfold esperanca
    simp [hij])

/-- A projeção `esperanca` fixa o comutante. -/
theorem esperanca_fixa_o_comutante (k : n → ℝ) (x : Matrix n n ℂ)
    (h : Commute (Matrix.diagonal (freq k)) x) : esperanca k x = x := by
  ext i j
  unfold esperanca
  simp only [Matrix.of_apply]
  split_ifs with hij
  · rfl
  · exact ((comuta_sse_entradas k x).mp h i j hij).symm

/-- ★ **A MÉDIA TENDE À PROJEÇÃO.** Quando a variância cresce, a média gaussiana tende, entrada a entrada, à
projeção `esperanca` sobre o comutante da matriz das frequências. -/
theorem a_media_tende_a_esperanca (k : n → ℝ) (x : Matrix n n ℂ) (i j : n) :
    Tendsto (fun t : ℝ => mediaGaussiana k (Real.toNNReal t) x i j) atTop
      (𝓝 (esperanca k x i j)) := by
  unfold esperanca
  simp only [Matrix.of_apply]
  by_cases hij : Real.sqrt (k i) = Real.sqrt (k j)
  · rw [if_pos hij]
    have hc : ∀ t : ℝ, mediaGaussiana k (Real.toNNReal t) x i j = x i j := by
      intro t
      rw [media_entrada]
      unfold mult
      rw [hij, sub_self]
      simp
    simp only [hc]
    exact tendsto_const_nhds
  · rw [if_neg hij]
    have hne : Real.sqrt (k i) - Real.sqrt (k j) ≠ 0 := sub_ne_zero.mpr hij
    have hc0 : 0 < (Real.sqrt (k i) - Real.sqrt (k j)) ^ 2 / 2 := by positivity
    have h1 : Tendsto (fun t : ℝ => Real.exp (-(t * ((Real.sqrt (k i) - Real.sqrt (k j)) ^ 2 / 2))))
        atTop (𝓝 0) :=
      Real.tendsto_exp_atBot.comp (tendsto_neg_atTop_atBot.comp (tendsto_id.atTop_mul_const hc0))
    have h2 : Tendsto (fun t : ℝ => mult k (Real.toNNReal t) i j) atTop (𝓝 0) := by
      refine h1.congr' ?_
      filter_upwards [eventually_ge_atTop (0 : ℝ)] with t ht
      unfold mult
      rw [Real.coe_toNNReal t ht]
      congr 1
      ring
    have h3 : Tendsto (fun t : ℝ => ((mult k (Real.toNNReal t) i j : ℝ) : ℂ) * x i j) atTop
        (𝓝 (((0 : ℝ) : ℂ) * x i j)) :=
      ((Complex.continuous_ofReal.tendsto 0).comp h2).mul_const (x i j)
    simp only [Complex.ofReal_zero, zero_mul] at h3
    refine h3.congr (fun t => ?_)
    rw [media_entrada]


end TGLExt.T1CompostoFinito
