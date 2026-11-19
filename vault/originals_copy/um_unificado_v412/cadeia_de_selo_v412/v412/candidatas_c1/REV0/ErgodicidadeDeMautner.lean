import TGLExt.TheSingularityReadsTheAttractorAdendo1

/-!
# ERGODICIDADE POR MAUTNER — candidata da gerência c1 para a v412 (frente B, a T1). RASCUNHO R0.

Nome provisório (o nome é do operador). Nada aqui está instalado nem selado.
O cabeçalho completo (fontes, o que compra, o que não compra, estatutos) entra depois da conferência distinta.
-/

set_option autoImplicit false
set_option maxHeartbeats 4000000

namespace TGLExt.ErgodicidadeDeMautner

open Filter Topology TGLExt.TheSingularityReadsTheAttractor
open scoped InnerProductSpace

/-! ## 1. O núcleo: o coeficiente que não muda de escala é o coeficiente do repouso -/

section Nucleo

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H]

/-- **O NÚCLEO.** Se o coeficiente `⟪ξ, T a ξ⟫` não muda quando `a` é encolhido por fatores `r i` que
tendem a zero, então `T a ξ = ξ` para todo `a`. É o passo de Cauchy–Schwarz do argumento de Mautner:
o coeficiente é constante ao longo do encolhimento, o limite é `⟪ξ, ξ⟫`, e a igualdade fecha. -/
theorem o_nucleo {ι : Type*} (T : ℝ → H →L[ℂ] H) (r : ι → ℝ) (l : Filter ι) [l.NeBot]
    (hT : ∀ a v, ‖T a v‖ = ‖v‖) (h0 : ∀ v, T 0 v = v)
    (hcont : ∀ v, ContinuousAt (fun a => T a v) 0)
    (hr : Tendsto r l (𝓝 0)) (ξ : H)
    (hinv : ∀ i a, ⟪ξ, T a ξ⟫_ℂ = ⟪ξ, T (r i * a) ξ⟫_ℂ) (a : ℝ) :
    T a ξ = ξ := by
  have h1 : Tendsto (fun i => r i * a) l (𝓝 0) := by
    simpa using hr.mul_const a
  have h2 : Tendsto (fun i => T (r i * a) ξ) l (𝓝 (T 0 ξ)) := (hcont ξ).tendsto.comp h1
  have h3 : Tendsto (fun i => ⟪ξ, T (r i * a) ξ⟫_ℂ) l (𝓝 ⟪ξ, T 0 ξ⟫_ℂ) :=
    tendsto_const_nhds.inner h2
  have h4 : Tendsto (fun _ : ι => ⟪ξ, T a ξ⟫_ℂ) l (𝓝 ⟪ξ, T 0 ξ⟫_ℂ) :=
    h3.congr (fun i => (hinv i a).symm)
  have h5 : ⟪ξ, T a ξ⟫_ℂ = ⟪ξ, T 0 ξ⟫_ℂ := tendsto_nhds_unique tendsto_const_nhds h4
  have hval : ⟪ξ, T a ξ⟫_ℂ = ⟪ξ, ξ⟫_ℂ := by rw [h5, h0]
  have hre : RCLike.re ⟪T a ξ, ξ⟫_ℂ = ‖ξ‖ ^ 2 := by
    rw [inner_re_symm, hval, inner_self_eq_norm_sq]
  have hsq : ‖T a ξ - ξ‖ ^ 2 = 0 := by
    rw [@norm_sub_sq ℂ, hre, hT a ξ]; ring
  have hn : ‖T a ξ - ξ‖ = 0 := by
    simpa using hsq
  exact sub_eq_zero.mp (norm_eq_zero.mp hn)

/-- Da covariância ao coeficiente: se `D i` preserva o produto interno, fixa `ξ` e leva `T a` em
`T (r i * a)`, o coeficiente `⟪ξ, T a ξ⟫` não muda quando `a` é multiplicado por `r i`. -/
theorem o_coeficiente_nao_muda_de_escala {ι : Type*} (D : ι → H →L[ℂ] H) (T : ℝ → H →L[ℂ] H)
    (r : ι → ℝ) (hD : ∀ i v w, ⟪D i v, D i w⟫_ℂ = ⟪v, w⟫_ℂ)
    (hcov : ∀ i a v, D i (T a v) = T (r i * a) (D i v))
    (ξ : H) (hξ : ∀ i, D i ξ = ξ) (i : ι) (a : ℝ) :
    ⟪ξ, T a ξ⟫_ℂ = ⟪ξ, T (r i * a) ξ⟫_ℂ := by
  have h := hD i ξ (T a ξ)
  rw [hcov i a ξ, hξ i] at h
  exact h.symm

end Nucleo

/-! ## 2. Mautner: o que o boost fixa, as translações fixam -/

section Mautner

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H]

/-- **MAUTNER, na forma de família.** `δ` é o boost; `Tp` e `Tm` são as duas translações da luz, que o
boost reescala por `exp s` e por `exp (-s)`. Todo vetor fixo pelo boost é fixo pelas duas translações. -/
theorem o_fixo_do_boost_e_fixo_das_translacoes
    (δ Tp Tm : ℝ → H →L[ℂ] H)
    (hδ : ∀ s v w, ⟪δ s v, δ s w⟫_ℂ = ⟪v, w⟫_ℂ)
    (hTp : ∀ a v, ‖Tp a v‖ = ‖v‖) (hTm : ∀ a v, ‖Tm a v‖ = ‖v‖)
    (hp0 : ∀ v, Tp 0 v = v) (hm0 : ∀ v, Tm 0 v = v)
    (hpc : ∀ v, ContinuousAt (fun a => Tp a v) 0) (hmc : ∀ v, ContinuousAt (fun a => Tm a v) 0)
    (hcp : ∀ s a v, δ s (Tp a v) = Tp (Real.exp s * a) (δ s v))
    (hcm : ∀ s a v, δ s (Tm a v) = Tm (Real.exp (-s) * a) (δ s v))
    (ξ : H) (hξ : ∀ s, δ s ξ = ξ) :
    (∀ a, Tp a ξ = ξ) ∧ (∀ a, Tm a ξ = ξ) := by
  constructor
  · intro a
    exact o_nucleo Tp Real.exp atBot hTp hp0 hpc Real.tendsto_exp_atBot ξ
      (o_coeficiente_nao_muda_de_escala δ Tp Real.exp hδ hcp ξ hξ) a
  · intro a
    exact o_nucleo Tm (fun s => Real.exp (-s)) atTop hTm hm0 hmc
      Real.tendsto_exp_neg_atTop_nhds_zero ξ
      (o_coeficiente_nao_muda_de_escala δ Tm (fun s => Real.exp (-s)) hδ hcm ξ hξ) a

/-- **MAUTNER, com UMA só dilatação.** Basta um passo: uma isometria `U` que encolhe a translação por um
fator `q` com `|q| < 1`. Todo vetor fixo por `U` é fixo pela translação. -/
theorem o_fixo_de_uma_dilatacao_e_fixo_da_translacao
    (U : H →L[ℂ] H) (T : ℝ → H →L[ℂ] H) (q : ℝ) (hq : |q| < 1)
    (hU : ∀ v w, ⟪U v, U w⟫_ℂ = ⟪v, w⟫_ℂ)
    (hT : ∀ a v, ‖T a v‖ = ‖v‖) (h0 : ∀ v, T 0 v = v)
    (hcont : ∀ v, ContinuousAt (fun a => T a v) 0)
    (hcov : ∀ a v, U (T a v) = T (q * a) (U v))
    (ξ : H) (hξ : U ξ = ξ) (a : ℝ) : T a ξ = ξ := by
  have passo : ∀ b, ⟪ξ, T b ξ⟫_ℂ = ⟪ξ, T (q * b) ξ⟫_ℂ := fun b =>
    o_coeficiente_nao_muda_de_escala (fun _ : Unit => U) T (fun _ => q)
      (fun _ => hU) (fun _ => hcov) ξ (fun _ => hξ) () b
  have hinv : ∀ (n : ℕ) (b : ℝ), ⟪ξ, T b ξ⟫_ℂ = ⟪ξ, T (q ^ n * b) ξ⟫_ℂ := by
    intro n
    induction n with
    | zero => intro b; simp
    | succ n ih =>
      intro b
      rw [ih b, passo (q ^ n * b)]
      congr 3
      ring
  exact o_nucleo T (fun n : ℕ => q ^ n) atTop hT h0 hcont
    (tendsto_pow_atTop_nhds_zero_of_abs_lt_one hq) ξ hinv a

/-- A outra translação, com uma só dilatação: quando a relação vem escrita do lado que ALARGA
(`T a ∘ U = U ∘ T (q a)`), o mesmo vale. -/
theorem o_fixo_de_uma_dilatacao_e_fixo_da_outra_translacao
    (U : H →L[ℂ] H) (T : ℝ → H →L[ℂ] H) (q : ℝ) (hq : |q| < 1)
    (hU : ∀ v w, ⟪U v, U w⟫_ℂ = ⟪v, w⟫_ℂ)
    (hT : ∀ a v, ‖T a v‖ = ‖v‖) (h0 : ∀ v, T 0 v = v)
    (hcont : ∀ v, ContinuousAt (fun a => T a v) 0)
    (hcov : ∀ a v, T a (U v) = U (T (q * a) v))
    (ξ : H) (hξ : U ξ = ξ) (a : ℝ) : T a ξ = ξ := by
  have passo : ∀ b, ⟪ξ, T b ξ⟫_ℂ = ⟪ξ, T (q * b) ξ⟫_ℂ := by
    intro b
    have h := hU ξ (T (q * b) ξ)
    rw [← hcov b ξ, hξ] at h
    exact h
  have hinv : ∀ (n : ℕ) (b : ℝ), ⟪ξ, T b ξ⟫_ℂ = ⟪ξ, T (q ^ n * b) ξ⟫_ℂ := by
    intro n
    induction n with
    | zero => intro b; simp
    | succ n ih =>
      intro b
      rw [ih b, passo (q ^ n * b)]
      congr 3
      ring
  exact o_nucleo T (fun n : ℕ => q ^ n) atTop hT h0 hcont
    (tendsto_pow_atTop_nhds_zero_of_abs_lt_one hq) ξ hinv a

end Mautner

/-! ## 3. A ergodicidade como teorema: o que comuta com o boost é escalar -/

section Ergodicidade

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H]

/-- **`H_erg` COMO TEOREMA.** `M` é uma subálgebra com unidade, `Ω` é separador para `M` e fixo pelo
boost, e vale a hipótese NOMEADA do vácuo único (todo vetor fixo pelas duas translações é múltiplo de
`Ω`). Então todo `x` de `M` que comuta com o boost é escalar. -/
theorem o_que_comuta_com_o_boost_e_escalar
    (δ Tp Tm : ℝ → H →L[ℂ] H)
    (hδ : ∀ s v w, ⟪δ s v, δ s w⟫_ℂ = ⟪v, w⟫_ℂ)
    (hTp : ∀ a v, ‖Tp a v‖ = ‖v‖) (hTm : ∀ a v, ‖Tm a v‖ = ‖v‖)
    (hp0 : ∀ v, Tp 0 v = v) (hm0 : ∀ v, Tm 0 v = v)
    (hpc : ∀ v, ContinuousAt (fun a => Tp a v) 0) (hmc : ∀ v, ContinuousAt (fun a => Tm a v) 0)
    (hcp : ∀ s a v, δ s (Tp a v) = Tp (Real.exp s * a) (δ s v))
    (hcm : ∀ s a v, δ s (Tm a v) = Tm (Real.exp (-s) * a) (δ s v))
    (M : Subalgebra ℂ (H →L[ℂ] H)) (Ω : H)
    (hsep : ∀ x ∈ M, x Ω = 0 → x = 0)
    (hΩ : ∀ s, δ s Ω = Ω)
    (hvac : ∀ v : H, (∀ a, Tp a v = v) → (∀ a, Tm a v = v) → ∃ c : ℂ, v = c • Ω)
    (x : H →L[ℂ] H) (hx : x ∈ M) (hxδ : ∀ s v, δ s (x v) = x (δ s v)) :
    ∃ c : ℂ, x = c • (1 : H →L[ℂ] H) := by
  have hfix : ∀ s, δ s (x Ω) = x Ω := fun s => by rw [hxδ s Ω, hΩ s]
  obtain ⟨hp, hm⟩ := o_fixo_do_boost_e_fixo_das_translacoes δ Tp Tm hδ hTp hTm hp0 hm0 hpc hmc
    hcp hcm (x Ω) hfix
  obtain ⟨c, hc⟩ := hvac (x Ω) hp hm
  refine ⟨c, ?_⟩
  have hmem : x - c • (1 : H →L[ℂ] H) ∈ M := M.sub_mem hx (M.smul_mem M.one_mem c)
  have hz : (x - c • (1 : H →L[ℂ] H)) Ω = 0 := by simp [hc]
  exact sub_eq_zero.mp (hsep _ hmem hz)

/-- Os fixos de uma dilatação são a reta do vácuo. -/
theorem os_fixos_da_dilatacao_sao_o_vacuo
    (U : H →L[ℂ] H) (Tp Tm : ℝ → H →L[ℂ] H) (q : ℝ) (hq : |q| < 1)
    (hU : ∀ v w, ⟪U v, U w⟫_ℂ = ⟪v, w⟫_ℂ)
    (hTp : ∀ a v, ‖Tp a v‖ = ‖v‖) (hTm : ∀ a v, ‖Tm a v‖ = ‖v‖)
    (hp0 : ∀ v, Tp 0 v = v) (hm0 : ∀ v, Tm 0 v = v)
    (hpc : ∀ v, ContinuousAt (fun a => Tp a v) 0) (hmc : ∀ v, ContinuousAt (fun a => Tm a v) 0)
    (hcp : ∀ a v, U (Tp a v) = Tp (q * a) (U v))
    (hcm : ∀ a v, Tm a (U v) = U (Tm (q * a) v))
    (Ω : H) (hΩ : U Ω = Ω)
    (hvac : ∀ v : H, (∀ a, Tp a v = v) → (∀ a, Tm a v = v) → ∃ c : ℂ, v = c • Ω)
    (v : H) : U v = v ↔ ∃ c : ℂ, v = c • Ω := by
  constructor
  · intro hv
    exact hvac v
      (o_fixo_de_uma_dilatacao_e_fixo_da_translacao U Tp q hq hU hTp hp0 hpc hcp v hv)
      (o_fixo_de_uma_dilatacao_e_fixo_da_outra_translacao U Tm q hq hU hTm hm0 hmc hcm v hv)
  · rintro ⟨c, rfl⟩
    rw [map_smul, hΩ]

/-- **`H_erg` com UMA só dilatação.** Todo `x` de `M` que comuta com uma dilatação que fixa o vácuo
único é escalar. -/
theorem o_que_comuta_com_uma_dilatacao_e_escalar
    (U : H →L[ℂ] H) (Tp Tm : ℝ → H →L[ℂ] H) (q : ℝ) (hq : |q| < 1)
    (hU : ∀ v w, ⟪U v, U w⟫_ℂ = ⟪v, w⟫_ℂ)
    (hTp : ∀ a v, ‖Tp a v‖ = ‖v‖) (hTm : ∀ a v, ‖Tm a v‖ = ‖v‖)
    (hp0 : ∀ v, Tp 0 v = v) (hm0 : ∀ v, Tm 0 v = v)
    (hpc : ∀ v, ContinuousAt (fun a => Tp a v) 0) (hmc : ∀ v, ContinuousAt (fun a => Tm a v) 0)
    (hcp : ∀ a v, U (Tp a v) = Tp (q * a) (U v))
    (hcm : ∀ a v, Tm a (U v) = U (Tm (q * a) v))
    (M : Subalgebra ℂ (H →L[ℂ] H)) (Ω : H)
    (hsep : ∀ x ∈ M, x Ω = 0 → x = 0)
    (hΩ : U Ω = Ω)
    (hvac : ∀ v : H, (∀ a, Tp a v = v) → (∀ a, Tm a v = v) → ∃ c : ℂ, v = c • Ω)
    (x : H →L[ℂ] H) (hx : x ∈ M) (hxU : ∀ v, U (x v) = x (U v)) :
    ∃ c : ℂ, x = c • (1 : H →L[ℂ] H) := by
  have hfix : U (x Ω) = x Ω := by rw [hxU Ω, hΩ]
  obtain ⟨c, hc⟩ := (os_fixos_da_dilatacao_sao_o_vacuo U Tp Tm q hq hU hTp hTm hp0 hm0 hpc hmc
    hcp hcm Ω hΩ hvac (x Ω)).mp hfix
  refine ⟨c, ?_⟩
  have hmem : x - c • (1 : H →L[ℂ] H) ∈ M := M.sub_mem hx (M.smul_mem M.one_mem c)
  have hz : (x - c • (1 : H →L[ℂ] H)) Ω = 0 := by simp [hc]
  exact sub_eq_zero.mp (hsep _ hmem hz)

end Ergodicidade

/-! ## 4. A média do boost é a esperança do vácuo -/

section Media

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- **A MÉDIA DO BOOST É A ESPERANÇA DO VÁCUO.** Com o vácuo único e de norma 1, as médias de Cesàro de
uma dilatação convergem, em todo vetor, a `⟪Ω, v⟫ • Ω`. -/
theorem a_media_do_boost_e_a_esperanca_do_vacuo
    (U : H →L[ℂ] H) (Tp Tm : ℝ → H →L[ℂ] H) (q : ℝ) (hq : |q| < 1)
    (hU : ∀ v w, ⟪U v, U w⟫_ℂ = ⟪v, w⟫_ℂ)
    (hTp : ∀ a v, ‖Tp a v‖ = ‖v‖) (hTm : ∀ a v, ‖Tm a v‖ = ‖v‖)
    (hp0 : ∀ v, Tp 0 v = v) (hm0 : ∀ v, Tm 0 v = v)
    (hpc : ∀ v, ContinuousAt (fun a => Tp a v) 0) (hmc : ∀ v, ContinuousAt (fun a => Tm a v) 0)
    (hcp : ∀ a v, U (Tp a v) = Tp (q * a) (U v))
    (hcm : ∀ a v, Tm a (U v) = U (Tm (q * a) v))
    (Ω : H) (hΩ : U Ω = Ω) (hΩ1 : ‖Ω‖ = 1)
    (hvac : ∀ v : H, (∀ a, Tp a v = v) → (∀ a, Tm a v = v) → ∃ c : ℂ, v = c • Ω)
    (v : H) :
    Tendsto (birkhoffAverage ℂ U id · v) atTop (𝓝 (⟪Ω, v⟫_ℂ • Ω)) := by
  have hnorm : ‖U‖ ≤ 1 := by
    refine ContinuousLinearMap.opNorm_le_bound _ zero_le_one (fun w => ?_)
    have h2 : ‖U w‖ ^ 2 = ‖w‖ ^ 2 := by
      have := congrArg RCLike.re (hU w w)
      rwa [inner_self_eq_norm_sq, inner_self_eq_norm_sq] at this
    have h3 : ‖U w‖ = ‖w‖ := (sq_eq_sq₀ (norm_nonneg _) (norm_nonneg _)).mp h2
    rw [h3, one_mul]
  have hfix := os_fixos_da_dilatacao_sao_o_vacuo U Tp Tm q hq hU hTp hTm hp0 hm0 hpc hmc hcp hcm
    Ω hΩ hvac
  have hproj : reading U v = ⟪Ω, v⟫_ℂ • Ω := by
    unfold reading
    refine Submodule.eq_starProjection_of_mem_of_inner_eq_zero ?_ ?_
    · show U (⟪Ω, v⟫_ℂ • Ω) = (1 : H →L[ℂ] H) (⟪Ω, v⟫_ℂ • Ω)
      rw [map_smul, hΩ]; rfl
    · intro w hw
      have hw' : U w = w := hw
      obtain ⟨c, rfl⟩ := (hfix w).mp hw'
      rw [inner_smul_right, inner_sub_left, inner_smul_left, inner_conj_symm,
        inner_self_eq_norm_sq_to_K, hΩ1]
      simp
  rw [← hproj]
  exact A1_cesaro U hnorm v

/-- **A ESPERANÇA SOBRE OS FIXOS É O ESTADO.** Para `x` qualquer, a média do boost aplicada a `x Ω`
converge a `⟪Ω, x Ω⟫ • Ω`: na face de vetores, a esperança condicional sobre os fixos do boost devolve
o valor do estado do vácuo vezes o Um. -/
theorem a_esperanca_sobre_os_fixos_e_o_estado
    (U : H →L[ℂ] H) (Tp Tm : ℝ → H →L[ℂ] H) (q : ℝ) (hq : |q| < 1)
    (hU : ∀ v w, ⟪U v, U w⟫_ℂ = ⟪v, w⟫_ℂ)
    (hTp : ∀ a v, ‖Tp a v‖ = ‖v‖) (hTm : ∀ a v, ‖Tm a v‖ = ‖v‖)
    (hp0 : ∀ v, Tp 0 v = v) (hm0 : ∀ v, Tm 0 v = v)
    (hpc : ∀ v, ContinuousAt (fun a => Tp a v) 0) (hmc : ∀ v, ContinuousAt (fun a => Tm a v) 0)
    (hcp : ∀ a v, U (Tp a v) = Tp (q * a) (U v))
    (hcm : ∀ a v, Tm a (U v) = U (Tm (q * a) v))
    (Ω : H) (hΩ : U Ω = Ω) (hΩ1 : ‖Ω‖ = 1)
    (hvac : ∀ v : H, (∀ a, Tp a v = v) → (∀ a, Tm a v = v) → ∃ c : ℂ, v = c • Ω)
    (x : H →L[ℂ] H) :
    Tendsto (birkhoffAverage ℂ U id · (x Ω)) atTop (𝓝 (⟪Ω, x Ω⟫_ℂ • Ω)) :=
  a_media_do_boost_e_a_esperanca_do_vacuo U Tp Tm q hq hU hTp hTm hp0 hm0 hpc hmc hcp hcm
    Ω hΩ hΩ1 hvac (x Ω)

end Media

/-! ## 5. O domínio multiplicativo -/

section DominioMultiplicativo

variable {K : Type*} [NormedAddCommGroup K] [InnerProductSpace ℂ K] [CompleteSpace K]
variable {𝔄 : Type*} [Ring 𝔄] [StarRing 𝔄] [Algebra ℂ 𝔄] [StarModule ℂ 𝔄]

/-- Uma reta limitada por baixo é constante. -/
theorem a_reta_limitada_por_baixo_e_constante (p q : ℝ) (h : ∀ t : ℝ, 0 ≤ t * p + q) : p = 0 := by
  by_contra hp
  have h1 := h (-(q + 1) / p)
  have h2 : -(q + 1) / p * p = -(q + 1) := by field_simp
  rw [h2] at h1
  linarith

/-- O passo de Choi: sob a desigualdade de Schwarz, se `a` satura a desigualdade, a parte real do
defeito `Φ (b a) - Φ b Φ a` é nula em todo vetor. -/
theorem a_parte_real_do_defeito_e_nula
    (Φ : 𝔄 →ₗ[ℂ] (K →L[ℂ] K))
    (hstar : ∀ x, Φ (star x) = star (Φ x))
    (hS : ∀ x v, ‖Φ x v‖ ^ 2 ≤ RCLike.re ⟪v, Φ (star x * x) v⟫_ℂ)
    (a : 𝔄) (ha : Φ (star a * a) = star (Φ a) * Φ a) (b : 𝔄) (v : K) :
    RCLike.re ⟪v, (Φ (b * a) - Φ b * Φ a) v⟫_ℂ = 0 := by
  have hA : RCLike.re ⟪v, Φ (star a * a) v⟫_ℂ = ‖Φ a v‖ ^ 2 := by
    rw [ha]
    show RCLike.re ⟪v, star (Φ a) (Φ a v)⟫_ℂ = ‖Φ a v‖ ^ 2
    rw [ContinuousLinearMap.star_eq_adjoint, ContinuousLinearMap.adjoint_inner_right,
      inner_self_eq_norm_sq]
  have hF : RCLike.re ⟪v, Φ (star (b * a)) v⟫_ℂ = RCLike.re ⟪v, Φ (b * a) v⟫_ℂ := by
    rw [hstar, ContinuousLinearMap.star_eq_adjoint, ContinuousLinearMap.adjoint_inner_right,
      inner_re_symm]
  have hB : RCLike.re ⟪Φ a v, star (Φ b) v⟫_ℂ = RCLike.re ⟪v, (Φ b * Φ a) v⟫_ℂ := by
    rw [ContinuousLinearMap.star_eq_adjoint, ContinuousLinearMap.adjoint_inner_right,
      inner_re_symm]
    rfl
  have hslope : ∀ t : ℝ, 0 ≤ t * (2 * RCLike.re ⟪v, (Φ (b * a) - Φ b * Φ a) v⟫_ℂ)
      + (RCLike.re ⟪v, Φ (b * star b) v⟫_ℂ - ‖star (Φ b) v‖ ^ 2) := by
    intro t
    have h := hS ((t : ℂ) • a + star b) v
    have e1 : star ((t : ℂ) • a + star b) * ((t : ℂ) • a + star b)
        = ((t : ℂ) * (t : ℂ)) • (star a * a) + (t : ℂ) • (star (b * a) + b * a) + b * star b := by
      rw [star_add, star_smul, star_star, star_mul]
      simp only [Complex.star_def, Complex.conj_ofReal, add_mul, mul_add, smul_mul_assoc,
        mul_smul_comm, smul_smul, smul_add]
      module
    have e2 : Φ ((t : ℂ) • a + star b) v = (t : ℂ) • Φ a v + star (Φ b) v := by
      rw [map_add, map_smul, hstar]; rfl
    have e3 : ‖(t : ℂ) • Φ a v + star (Φ b) v‖ ^ 2
        = t ^ 2 * ‖Φ a v‖ ^ 2 + 2 * (t * RCLike.re ⟪Φ a v, star (Φ b) v⟫_ℂ) + ‖star (Φ b) v‖ ^ 2 := by
      rw [@norm_add_sq ℂ, norm_smul, inner_smul_left, Complex.conj_ofReal, Complex.norm_real,
        mul_pow, Real.norm_eq_abs, sq_abs]
      simp
    have e4 : RCLike.re ⟪v, Φ (((t : ℂ) * (t : ℂ)) • (star a * a) + (t : ℂ) • (star (b * a) + b * a)
          + b * star b) v⟫_ℂ
        = t ^ 2 * ‖Φ a v‖ ^ 2 + t * (2 * RCLike.re ⟪v, Φ (b * a) v⟫_ℂ)
          + RCLike.re ⟪v, Φ (b * star b) v⟫_ℂ := by
      simp only [map_add, map_smul, add_apply, smul_apply, inner_add_right, inner_smul_right]
      rw [← Complex.ofReal_mul]
      simp only [RCLike.re_to_complex, Complex.re_ofReal_mul, Complex.add_re]
      rw [← RCLike.re_to_complex, ← RCLike.re_to_complex, ← RCLike.re_to_complex, ← RCLike.re_to_complex,
        hA, hF]
      ring
    rw [e1, e2, e3, e4, hB] at h
    have hD : RCLike.re ⟪v, (Φ (b * a) - Φ b * Φ a) v⟫_ℂ
        = RCLike.re ⟪v, Φ (b * a) v⟫_ℂ - RCLike.re ⟪v, (Φ b * Φ a) v⟫_ℂ := by
      rw [sub_apply, inner_sub_right, map_sub]
    rw [hD]
    nlinarith [h]
  have := a_reta_limitada_por_baixo_e_constante _ _ hslope
  linarith

/-- **O DOMÍNIO MULTIPLICATIVO (Choi).** `Φ` é linear, respeita a estrela e cumpre a desigualdade de
Schwarz. Se `a` satura a desigualdade (`Φ (a⋆ a) = Φ(a)⋆ Φ(a)`), então `Φ (b a) = Φ b Φ a` para todo `b`. -/
theorem o_dominio_multiplicativo
    (Φ : 𝔄 →ₗ[ℂ] (K →L[ℂ] K))
    (hstar : ∀ x, Φ (star x) = star (Φ x))
    (hS : ∀ x v, ‖Φ x v‖ ^ 2 ≤ RCLike.re ⟪v, Φ (star x * x) v⟫_ℂ)
    (a : 𝔄) (ha : Φ (star a * a) = star (Φ a) * Φ a) (b : 𝔄) :
    Φ (b * a) = Φ b * Φ a := by
  have hre : ∀ (c : 𝔄) (v : K), RCLike.re ⟪v, (Φ (c * a) - Φ c * Φ a) v⟫_ℂ = 0 :=
    fun c v => a_parte_real_do_defeito_e_nula Φ hstar hS a ha c v
  have hzero : ∀ v : K, ⟪(Φ (b * a) - Φ b * Φ a) v, v⟫_ℂ = 0 := by
    intro v
    have h1 := hre b v
    have h2 := hre (Complex.I • b) v
    have e : Φ (Complex.I • b * a) - Φ (Complex.I • b) * Φ a
        = Complex.I • (Φ (b * a) - Φ b * Φ a) := by
      rw [smul_mul_assoc, map_smul, map_smul, smul_mul_assoc, smul_sub]
    rw [e, smul_apply, inner_smul_right] at h2
    have h4 : ⟪v, (Φ (b * a) - Φ b * Φ a) v⟫_ℂ = 0 := by
      generalize ⟪v, (Φ (b * a) - Φ b * Φ a) v⟫_ℂ = z at h1 h2 ⊢
      have h3 : z.im = 0 := by simpa using h2
      exact Complex.ext (by simpa using h1) (by simpa using h3)
    rw [← inner_conj_symm, h4, map_zero]
  have := (inner_map_self_eq_zero (Φ (b * a) - Φ b * Φ a : K →ₗ[ℂ] K)).mp hzero
  exact sub_eq_zero.mp (by ext w; simpa using congrArg (fun f : K →ₗ[ℂ] K => f w) this)

end DominioMultiplicativo

/-! ## 6. Os fixos de um mapa de Schwarz que respeita um estado fiel formam uma álgebra -/

section AlgebraDosFixos

variable {K : Type*} [NormedAddCommGroup K] [InnerProductSpace ℂ K] [CompleteSpace K]
variable {𝔄 : Type*} [Ring 𝔄] [StarRing 𝔄] [Algebra ℂ 𝔄] [StarModule ℂ 𝔄]

/-- Uma parábola `t p + t² q` que nunca é negativa não tem termo linear. -/
theorem a_parabola_sem_parte_negativa_nao_tem_termo_linear (p q : ℝ)
    (h : ∀ t : ℝ, 0 ≤ t * p + t ^ 2 * q) : p = 0 := by
  by_contra hp
  have hq : 0 ≤ q := by
    have h1 := h 1
    have h2 := h (-1)
    nlinarith
  have hq1 : 0 < q + 1 := by linarith
  have h1 := h (-p / (q + 1))
  have e : -p / (q + 1) * p + (-p / (q + 1)) ^ 2 * q = -(p ^ 2 / (q + 1) ^ 2) := by
    field_simp
    ring
  rw [e] at h1
  have hpos : 0 < p ^ 2 / (q + 1) ^ 2 := by positivity
  linarith

omit [CompleteSpace K] in
/-- Um operador de forma não negativa e simétrico que se anula num vetor (no valor esperado) anula o
vetor. -/
theorem o_positivo_de_esperanca_nula_anula_o_vetor (P : K →L[ℂ] K)
    (hpos : ∀ v, 0 ≤ RCLike.re ⟪v, P v⟫_ℂ)
    (hsym : ∀ v w, ⟪v, P w⟫_ℂ = ⟪P v, w⟫_ℂ)
    (Ω : K) (h0 : RCLike.re ⟪Ω, P Ω⟫_ℂ = 0) : P Ω = 0 := by
  have hq : ∀ t : ℝ, 0 ≤ t * (2 * ‖P Ω‖ ^ 2) + t ^ 2 * RCLike.re ⟪P Ω, P (P Ω)⟫_ℂ := by
    intro t
    have h := hpos (Ω + (t : ℂ) • P Ω)
    have e : RCLike.re ⟪Ω + (t : ℂ) • P Ω, P (Ω + (t : ℂ) • P Ω)⟫_ℂ
        = RCLike.re ⟪Ω, P Ω⟫_ℂ + t * (2 * ‖P Ω‖ ^ 2) + t ^ 2 * RCLike.re ⟪P Ω, P (P Ω)⟫_ℂ := by
      have s1 : ⟪Ω, P (P Ω)⟫_ℂ = ⟪P Ω, P Ω⟫_ℂ := hsym Ω (P Ω)
      rw [map_add, map_smul, inner_add_left, inner_add_right, inner_add_right, inner_smul_left,
        inner_smul_right, inner_smul_right, inner_smul_left, s1, Complex.conj_ofReal]
      have s2 : RCLike.re ⟪P Ω, P Ω⟫_ℂ = ‖P Ω‖ ^ 2 := inner_self_eq_norm_sq _
      simp only [map_add, RCLike.re_to_complex, Complex.re_ofReal_mul] at s2 ⊢
      rw [s2]
      ring
    rw [e, h0] at h
    linarith
  have h2 := a_parabola_sem_parte_negativa_nao_tem_termo_linear _ _ hq
  have h3 : ‖P Ω‖ = 0 := by
    have : ‖P Ω‖ ^ 2 = 0 := by linarith
    simpa using this
  exact norm_eq_zero.mp h3

omit [StarModule ℂ 𝔄] in
/-- **O FIXO SATURA A DESIGUALDADE.** `π` é a representação, `φ` o mapa (linear, respeita a estrela,
cumpre Schwarz na representação), `Ω` é separador e o estado de `Ω` é invariante por `φ`. Se `a` é fixo
(`π (φ a) = π a`), então `π (φ (a⋆ a)) = π (a⋆ a)`. -/
theorem o_fixo_satura_a_desigualdade
    (π : 𝔄 →⋆ₐ[ℂ] (K →L[ℂ] K)) (φ : 𝔄 →ₗ[ℂ] 𝔄)
    (hstar : ∀ x, φ (star x) = star (φ x))
    (hS : ∀ x v, ‖π (φ x) v‖ ^ 2 ≤ RCLike.re ⟪v, π (φ (star x * x)) v⟫_ℂ)
    (Ω : K) (hsep : ∀ x : 𝔄, π x Ω = 0 → π x = 0)
    (hinv : ∀ x, ⟪Ω, π (φ x) Ω⟫_ℂ = ⟪Ω, π x Ω⟫_ℂ)
    (a : 𝔄) (ha : π (φ a) = π a) :
    π (φ (star a * a)) = π (star a * a) := by
  have hy : star (φ (star a * a) - star a * a) = φ (star a * a) - star a * a := by
    rw [star_sub, ← hstar, star_mul, star_star]
  have hP : π (φ (star a * a) - star a * a) = π (φ (star a * a)) - π (star a * a) := map_sub π _ _
  have hnorm : ∀ v, RCLike.re ⟪v, π (star a * a) v⟫_ℂ = ‖π a v‖ ^ 2 := by
    intro v
    rw [map_mul, map_star]
    show RCLike.re ⟪v, star (π a) (π a v)⟫_ℂ = ‖π a v‖ ^ 2
    rw [ContinuousLinearMap.star_eq_adjoint, ContinuousLinearMap.adjoint_inner_right,
      inner_self_eq_norm_sq]
  have hpos : ∀ v, 0 ≤ RCLike.re ⟪v, π (φ (star a * a) - star a * a) v⟫_ℂ := by
    intro v
    rw [hP, sub_apply, inner_sub_right, map_sub, hnorm v]
    have h := hS a v
    rw [ha] at h
    linarith
  have hsym : ∀ v w, ⟪v, π (φ (star a * a) - star a * a) w⟫_ℂ
      = ⟪π (φ (star a * a) - star a * a) v, w⟫_ℂ := by
    intro v w
    have h1 : star (π (φ (star a * a) - star a * a)) = π (φ (star a * a) - star a * a) := by
      rw [← map_star, hy]
    rw [← ContinuousLinearMap.adjoint_inner_left, ← ContinuousLinearMap.star_eq_adjoint, h1]
  have h0 : RCLike.re ⟪Ω, π (φ (star a * a) - star a * a) Ω⟫_ℂ = 0 := by
    rw [hP, sub_apply, inner_sub_right, hinv, sub_self, map_zero]
  have hz := o_positivo_de_esperanca_nula_anula_o_vetor _ hpos hsym Ω h0
  have := hsep _ hz
  rw [hP] at this
  exact sub_eq_zero.mp this

/-- **OS FIXOS ESTÃO NO DOMÍNIO MULTIPLICATIVO.** Com as mesmas hipóteses, se `a` é fixo então
`π (φ (b a)) = π (φ b) π a` para todo `b`. -/
theorem os_fixos_estao_no_dominio_multiplicativo
    (π : 𝔄 →⋆ₐ[ℂ] (K →L[ℂ] K)) (φ : 𝔄 →ₗ[ℂ] 𝔄)
    (hstar : ∀ x, φ (star x) = star (φ x))
    (hS : ∀ x v, ‖π (φ x) v‖ ^ 2 ≤ RCLike.re ⟪v, π (φ (star x * x)) v⟫_ℂ)
    (Ω : K) (hsep : ∀ x : 𝔄, π x Ω = 0 → π x = 0)
    (hinv : ∀ x, ⟪Ω, π (φ x) Ω⟫_ℂ = ⟪Ω, π x Ω⟫_ℂ)
    (a : 𝔄) (ha : π (φ a) = π a) (b : 𝔄) :
    π (φ (b * a)) = π (φ b) * π a := by
  have hsat := o_fixo_satura_a_desigualdade π φ hstar hS Ω hsep hinv a ha
  have h := o_dominio_multiplicativo (π.toAlgHom.toLinearMap.comp φ)
    (fun x => by
      show π (φ (star x)) = star (π (φ x))
      rw [hstar, map_star])
    (fun x v => hS x v) a
    (by
      show π (φ (star a * a)) = star (π (φ a)) * π (φ a)
      rw [hsat, ha, map_mul, map_star]) b
  have h' : π (φ (b * a)) = π (φ b) * π (φ a) := h
  rw [h', ha]

/-- **OS FIXOS FECHAM NO PRODUTO E NA ESTRELA.** Os fixos de `φ` (na representação) formam uma álgebra
com estrela. -/
theorem os_fixos_formam_uma_algebra
    (π : 𝔄 →⋆ₐ[ℂ] (K →L[ℂ] K)) (φ : 𝔄 →ₗ[ℂ] 𝔄)
    (hstar : ∀ x, φ (star x) = star (φ x))
    (hS : ∀ x v, ‖π (φ x) v‖ ^ 2 ≤ RCLike.re ⟪v, π (φ (star x * x)) v⟫_ℂ)
    (Ω : K) (hsep : ∀ x : 𝔄, π x Ω = 0 → π x = 0)
    (hinv : ∀ x, ⟪Ω, π (φ x) Ω⟫_ℂ = ⟪Ω, π x Ω⟫_ℂ)
    (a b : 𝔄) (ha : π (φ a) = π a) (hb : π (φ b) = π b) :
    π (φ (b * a)) = π (b * a) ∧ π (φ (star a)) = π (star a) ∧ π (φ (a + b)) = π (a + b) := by
  refine ⟨?_, ?_, ?_⟩
  · rw [os_fixos_estao_no_dominio_multiplicativo π φ hstar hS Ω hsep hinv a ha b, hb, map_mul]
  · rw [hstar, map_star, ha, map_star]
  · rw [map_add, map_add, ha, hb, map_add]

end AlgebraDosFixos

/-! ## 7. A mistura de atos só deixa parado o que cada ato deixa parado (o Lema A, na face finita) -/

section Mistura

variable {K : Type*} [NormedAddCommGroup K] [InnerProductSpace ℂ K]

/-- Convexidade estrita, na forma que o Lema A usa: se uma média de vetores de mesma norma que `v`
(pesos positivos, soma 1) é o próprio `v`, cada um deles é `v`. -/
theorem a_mistura_de_vetores_de_mesma_norma {ι : Type*} (S : Finset ι) (p : ι → ℝ)
    (hp : ∀ i ∈ S, 0 < p i) (hp1 : ∑ i ∈ S, p i = 1) (w : ι → K) (v : K)
    (hn : ∀ i ∈ S, ‖w i‖ = ‖v‖) (hsum : ∑ i ∈ S, (p i : ℂ) • w i = v) :
    ∀ i ∈ S, w i = v := by
  have hterm : ∀ i ∈ S, p i * ‖w i - v‖ ^ 2
      = p i * (2 * ‖v‖ ^ 2) - 2 * (p i * RCLike.re ⟪w i, v⟫_ℂ) := by
    intro i hi
    rw [@norm_sub_sq ℂ, hn i hi]; ring
  have hsumre : ∑ i ∈ S, p i * RCLike.re ⟪w i, v⟫_ℂ = ‖v‖ ^ 2 := by
    have h1 : ⟪∑ i ∈ S, (p i : ℂ) • w i, v⟫_ℂ = ∑ i ∈ S, (p i : ℂ) * ⟪w i, v⟫_ℂ := by
      rw [sum_inner]
      refine Finset.sum_congr rfl (fun i _ => ?_)
      rw [inner_smul_left, Complex.conj_ofReal]
    rw [hsum] at h1
    have h2 := congrArg RCLike.re h1
    rw [inner_self_eq_norm_sq, map_sum] at h2
    rw [h2]
    refine Finset.sum_congr rfl (fun i _ => ?_)
    simp
  have htot : ∑ i ∈ S, p i * ‖w i - v‖ ^ 2 = 0 := by
    rw [Finset.sum_congr rfl hterm, Finset.sum_sub_distrib, ← Finset.sum_mul, hp1,
      ← Finset.mul_sum, hsumre]
    ring
  have hnn : ∀ i ∈ S, 0 ≤ p i * ‖w i - v‖ ^ 2 :=
    fun i hi => mul_nonneg (hp i hi).le (sq_nonneg _)
  intro i hi
  have hz := (Finset.sum_eq_zero_iff_of_nonneg hnn).mp htot i hi
  have h2 : ‖w i - v‖ ^ 2 = 0 := by
    rcases mul_eq_zero.mp hz with h | h
    · exact absurd h (hp i hi).ne'
    · exact h
  have h3 : ‖w i - v‖ = 0 := by simpa using h2
  exact sub_eq_zero.mp (norm_eq_zero.mp h3)

variable [CompleteSpace K]
variable {𝔄 : Type*} [Ring 𝔄] [StarRing 𝔄] [Algebra ℂ 𝔄] [StarModule ℂ 𝔄]

omit [StarModule ℂ 𝔄] in
/-- Na representação, o valor esperado de `a⋆ a` num vetor é o quadrado da norma de `a` no vetor. -/
theorem o_valor_esperado_de_a_estrela_a (π : 𝔄 →⋆ₐ[ℂ] (K →L[ℂ] K)) (a : 𝔄) (v : K) :
    RCLike.re ⟪v, π (star a * a) v⟫_ℂ = ‖π a v‖ ^ 2 := by
  rw [map_mul, map_star]
  show RCLike.re ⟪v, star (π a) (π a v)⟫_ℂ = ‖π a v‖ ^ 2
  rw [ContinuousLinearMap.star_eq_adjoint, ContinuousLinearMap.adjoint_inner_right,
    inner_self_eq_norm_sq]

omit [StarModule ℂ 𝔄] in
/-- **O LEMA A, NA FACE FINITA.** `α i` são atos que respeitam a estrela e o produto, o estado de `Ω` é
invariante por cada um, `Ω` é separador, os pesos são positivos e somam 1. Se a mistura fixa `a`, cada
ato fixa `a`. Não usa Choi nem a desigualdade de Schwarz: é a conta direta da variância. -/
theorem a_mistura_so_fixa_o_que_cada_ato_fixa {ι : Type*} (S : Finset ι) (p : ι → ℝ)
    (hp : ∀ i ∈ S, 0 < p i) (hp1 : ∑ i ∈ S, p i = 1)
    (π : 𝔄 →⋆ₐ[ℂ] (K →L[ℂ] K)) (α : ι → 𝔄 →⋆ₐ[ℂ] 𝔄)
    (Ω : K) (hsep : ∀ x : 𝔄, π x Ω = 0 → π x = 0)
    (hinv : ∀ i ∈ S, ∀ x, ⟪Ω, π (α i x) Ω⟫_ℂ = ⟪Ω, π x Ω⟫_ℂ)
    (a : 𝔄) (hfix : π (∑ i ∈ S, (p i : ℂ) • α i a) = π a) :
    ∀ i ∈ S, π (α i a) = π a := by
  have hn : ∀ i ∈ S, ‖π (α i a) Ω‖ = ‖π a Ω‖ := by
    intro i hi
    have h1 : ‖π (α i a) Ω‖ ^ 2 = ‖π a Ω‖ ^ 2 := by
      rw [← o_valor_esperado_de_a_estrela_a π (α i a) Ω, ← o_valor_esperado_de_a_estrela_a π a Ω,
        ← map_star, ← map_mul, hinv i hi]
    exact (sq_eq_sq₀ (norm_nonneg _) (norm_nonneg _)).mp h1
  have hsum : ∑ i ∈ S, (p i : ℂ) • π (α i a) Ω = π a Ω := by
    have h : (π (∑ i ∈ S, (p i : ℂ) • α i a)) Ω = π a Ω := by rw [hfix]
    rw [map_sum, sum_apply] at h
    rw [← h]
    refine Finset.sum_congr rfl (fun i _ => ?_)
    rw [map_smul]
    rfl
  have hvec := a_mistura_de_vetores_de_mesma_norma S p hp hp1 (fun i => π (α i a) Ω) (π a Ω) hn hsum
  intro i hi
  have hz : π (α i a - a) Ω = 0 := by
    rw [map_sub, sub_apply, hvec i hi, sub_self]
  have := hsep _ hz
  rw [map_sub] at this
  exact sub_eq_zero.mp this

end Mistura

#print axioms a_mistura_de_vetores_de_mesma_norma
#print axioms o_valor_esperado_de_a_estrela_a
#print axioms a_mistura_so_fixa_o_que_cada_ato_fixa
#print axioms a_parabola_sem_parte_negativa_nao_tem_termo_linear
#print axioms o_positivo_de_esperanca_nula_anula_o_vetor
#print axioms o_fixo_satura_a_desigualdade
#print axioms os_fixos_estao_no_dominio_multiplicativo
#print axioms os_fixos_formam_uma_algebra
#print axioms a_reta_limitada_por_baixo_e_constante
#print axioms a_parte_real_do_defeito_e_nula
#print axioms o_dominio_multiplicativo
#print axioms o_nucleo
#print axioms o_coeficiente_nao_muda_de_escala
#print axioms o_fixo_do_boost_e_fixo_das_translacoes
#print axioms o_fixo_de_uma_dilatacao_e_fixo_da_translacao
#print axioms o_fixo_de_uma_dilatacao_e_fixo_da_outra_translacao
#print axioms o_que_comuta_com_o_boost_e_escalar
#print axioms os_fixos_da_dilatacao_sao_o_vacuo
#print axioms o_que_comuta_com_uma_dilatacao_e_escalar
#print axioms a_media_do_boost_e_a_esperanca_do_vacuo
#print axioms a_esperanca_sobre_os_fixos_e_o_estado

end TGLExt.ErgodicidadeDeMautner
