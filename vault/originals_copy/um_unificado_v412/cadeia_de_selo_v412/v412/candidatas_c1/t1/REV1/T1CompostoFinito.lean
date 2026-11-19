import T1GaussianSpectrum

set_option autoImplicit false
noncomputable section

/-!
# A T1 na face finita, num arquivo só: o fixo da média é o comutante, e é gerado pelo gerador se e somente se o espectro é simples
[candidata da gerência c1, 16/11/2026, R1 (depois da conferência distinta; esta versão ainda não foi relida por
terceiro); nome provisório; nada instalado; o nome é do operador]

## De onde vem, e o que já existia

O kernel selado JÁ TEM a T1 na face finita, com outros nomes: `TGLExt.rhoD` e `TGLExt.specExpect`
(`EquivariantSection`), `TGLExt.dephase` (`Ergodicity`), `TGLExt.diagExpect` (`CondExpect`): o semigrupo de
dephasing, a seção espectral, a idempotência, o cair no comutante, a unidade e o limite da matriz inteira. O esqueleto
do composto (fixo da média = comutante; projeção por blocos; idempotência; limite) também já estava na K05 do Kimi
(`T1_R2.lean`, arquivada), com o fluxo posto por definição. A conferência de 15/11 da entrega K07-C do Codex achou que
`T1GaussianSpectrum` e `T1SemigroupProjection` provam ingredientes e que o composto não estava num arquivo só.

Este arquivo escreve o composto sobre `T1GaussianSpectrum` (do Codex, copiada byte a byte em `dep_codex\`, sem
alteração), com definições próprias. O módulo irmão `T1PontesAoKernel` liga cada definição daqui ao objeto do kernel
(sondas do revisor C4 de 16/11, adotadas). NÃO são treze teoremas novos. Novo de fato:

(a) a ligação da integral gaussiana ao dephasing (o termo é do Codex): `media_entrada`;
(b) o fixo de UMA só média de variância não nula é o comutante, mesmo com frequências repetidas:
    `fixo_da_media_sse_comuta`;
(c) o critério do polinômio (do Codex) aplicado ao fixo: `o_fixo_e_gerado_sse_espectro_simples`;
(d) o limite com frequências repetidas: `a_media_tende_a_esperanca`.

São instâncias de teoremas do kernel (provado em `T1PontesAoKernel`): `media_compoe` (de `dephase_add`),
`esperanca_idempotente` (de `specExpect_idem`), `esperanca_cai_no_comutante` (de `rhoD_commute_specExpect`).

## O que fica provado (dimensão finita; base em que o gerador é diagonal)

Os TERMOS falam da matriz das FREQUÊNCIAS, `Matrix.diagonal (freq k)`, com `freq k i = √(k i)`; `k : n → ℝ` são os
níveis. A passagem à matriz dos níveis pede níveis não negativos e está em `T1PontesAoKernel`
(`fixo_da_media_sse_comuta_nivel`, `o_fixo_e_gerado_pelo_nivel_sse`). No Lean a raiz de número negativo vale zero: com
nível negativo as frases abaixo valem só para as frequências.

1. `media_entrada`: a média gaussiana, de variância `v`, das conjugações pelas fases `e^{i s √k}` multiplica a entrada
   `(i, j)` por `e^{−v (√kᵢ − √kⱼ)² / 2}` (é o termo do Codex);
2. `media_compoe`: a média de variância `v` depois da de variância `w` é a de variância `v + w`;
3. ★ `fixo_da_media_sse_comuta`: para `v ≠ 0`, uma matriz é fixa pela média se e somente se comuta com a matriz das
   frequências;
4. ★★ `o_fixo_e_gerado_sse_espectro_simples`: para `v ≠ 0`, todo fixo é um polinômio na matriz das frequências se e
   somente se as frequências são todas distintas (a volta, todo polinômio é fixo, está em
   `T1PontesAoKernel`: `polinomio_e_fixo`); com níveis não negativos, frequências distintas são níveis distintos
   (`freq_injetiva_sse`);
5. ★ `a_media_tende_a_esperanca`: quando a variância cresce, a média tende, entrada a entrada, à projeção `esperanca`
   sobre o comutante (para a matriz inteira, na topologia produto, que em dimensão finita é a da norma:
   `a_media_tende_matriz`, no módulo irmão). `esperanca` é uma projeção explícita: idempotente, cai no comutante e o
   fixa; unidade, traço, estrela e lei de bimódulo estão no módulo irmão; a positividade não é termo aqui.

Em língua simples: a média atenua as entradas que ligam frequências diferentes e deixa as outras intactas; no limite
de variância infinita as primeiras somem. Fica parada a matriz que comuta com o gerador; e o que fica parado é a
álgebra do gerador exatamente quando nenhum nível se repete (gerador de níveis não negativos, variância não nula).

## O que NÃO se afirma

* Nada sobre o caso contínuo (tipo III, produto cruzado, peso dual, traço e esperança no núcleo): segue no papel
  [DERIVED pelo Codex sobre KNOWN: Digernes–Takesaki (via Takesaki II e Andreou), dualidade de Takesaki, critério de
  Takesaki 1972, Umegaki, Segal–Dixmier, Lusin–Souslin; nenhuma lida no primário pela casa]. Os rótulos Lema A, B e
  C são da K05 do Kimi.
* Que as hipóteses do papel valham no objeto da teoria. Na face finita, “nenhuma frequência se repete”
  (multiplicidade um do gerador na matriz cheia) é o análogo de DUAS hipóteses do papel JUNTAS, a do gerador (`H_K̂`)
  e a ergodicidade (`H_erg`): a face finita não as separa; no papel, fixo = álgebra do gerador pede as duas
  (`T1_R3.md`, controle da necessidade). Qual das três leituras do Axioma E vale é do autor.
* “Dissipação” e “variância = β·t”: são leitura do papel (`T1_R3.md`), não do termo, que só tem a variância `v`.

Estatutos: `[REAL no sandbox]` os termos · `[DECLARADO pelo Codex, conferido por revisor distinto]` a dependência.
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
outras. É a `TGLExt.specExpect` do kernel nas frequências (`T1PontesAoKernel.esperanca_e_specExpect`). -/
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

/-- A média é semigrupo na variância. -/
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

/-- ★ **O FIXO DA MÉDIA É O COMUTANTE DO GERADOR.** -/
theorem fixo_da_media_sse_comuta (k : n → ℝ) {v : ℝ≥0} (hv : v ≠ 0) (x : Matrix n n ℂ) :
    mediaGaussiana k v x = x ↔ Commute (Matrix.diagonal (freq k)) x :=
  (fixo_sse_entradas k hv x).trans (comuta_sse_entradas k x).symm

/-- ★★ **O FIXO É GERADO PELO GERADOR SE E SOMENTE SE O ESPECTRO É SIMPLES.** Todo ponto fixo da média é um
polinômio no gerador exatamente quando as frequências são todas distintas. -/
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
/-- A esperança é idempotente. -/
theorem esperanca_idempotente (k : n → ℝ) (x : Matrix n n ℂ) :
    esperanca k (esperanca k x) = esperanca k x := by
  ext i j
  unfold esperanca
  simp only [Matrix.of_apply]
  split_ifs <;> rfl

/-- A esperança cai no comutante. -/
theorem esperanca_cai_no_comutante (k : n → ℝ) (x : Matrix n n ℂ) :
    Commute (Matrix.diagonal (freq k)) (esperanca k x) :=
  (comuta_sse_entradas k _).mpr (fun i j hij => by
    unfold esperanca
    simp [hij])

/-- A esperança fixa o comutante. -/
theorem esperanca_fixa_o_comutante (k : n → ℝ) (x : Matrix n n ℂ)
    (h : Commute (Matrix.diagonal (freq k)) x) : esperanca k x = x := by
  ext i j
  unfold esperanca
  simp only [Matrix.of_apply]
  split_ifs with hij
  · rfl
  · exact ((comuta_sse_entradas k x).mp h i j hij).symm

/-- ★ **A MÉDIA TENDE À ESPERANÇA.** Quando a variância cresce, a média gaussiana tende, entrada a entrada, à
esperança sobre o comutante do gerador. -/
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

#print axioms media_entrada
#print axioms mult_add
#print axioms media_compoe
#print axioms mult_eq_one_iff
#print axioms fixo_sse_entradas
#print axioms comuta_sse_entradas
#print axioms fixo_da_media_sse_comuta
#print axioms o_fixo_e_gerado_sse_espectro_simples
#print axioms freq_injetiva_sse
#print axioms esperanca_idempotente
#print axioms esperanca_cai_no_comutante
#print axioms esperanca_fixa_o_comutante
#print axioms a_media_tende_a_esperanca

end TGLExt.T1CompostoFinito
