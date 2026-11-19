import TGLExt.TheSingularityReadsTheAttractorAdendo1
import TGLExt.LightRhoStar
import TGLExt.F1Fecho394.BosonicFockGroupActions
import TGLExt.F1Fecho394.BosonicFockContinuity
import TGLExt.F1Fecho394.PhysicalWedgeNullGeometryR3
import TGLExt.F1Fecho394.CanonicalWedgeFlowR2
import TGLExt.F1Fecho394.WedgeCyclicR3
import TGLExt.F1Fecho394.CanonicalFockModularCoreInputR1
import TGLExt.F1Fecho394.PhysicalCanonicalWedgeEqualityR3

/-!
# ERGODICIDADE POR MAUTNER (a T1)

## A T1 e o que este arquivo formaliza

A T1 do Artigo vale, na caixa, para ESTADO normal fiel e depende de duas hipóteses nomeadas: `H_K̂` e
`H_erg` (o centralizador do estado é trivial; é propriedade do estado, não do tipo). Ela usa dois lemas de padrão de
redação (o domínio multiplicativo e a convergência no predual). Os passos: o Lema C (o comutante relativo no produto
cruzado), o Lema A (os fixos da mistura são o comutante), o Lema B (o traço, a esperança e a convergência), a proposição
da cunha (`H_erg` para a cunha de Minkowski, pelo argumento de Mautner) e o resíduo que o Artigo nomeia
(Bisognano–Wichmann para horizontes que não são de Killing). A identificação desta frente com a T1 de mesmo nome no
Artigo é rótulo deste arquivo.

Este arquivo formaliza o argumento de Mautner num Hilbert abstrato, com a fiação na luz.

## O que a pedra acrescenta ao kernel

1. **Mautner solto do contrato (seções 1 e 2).** Se o boost preserva o produto interno e reescala as
   duas translações (por `exp s` e por `exp (-s)`), todo vetor fixo pelo boost é fixo pelas duas
   translações; e basta UMA só dilatação que encolha. O kernel tinha o passo para a translação ao
   longo de `nullDir`, com fase, dentro do contrato (`ContratoH2.no_point_spectrum` e
   `eigen_null_correlation_dilation`, em `ContratoQG_v31_Teoremas.lean`).
2. **O que comuta com o boost é escalar, dado o vácuo único (seção 3), e a média (seção 4).** O vácuo
   único é hipótese NOMEADA; a seção 4 usa a leitura que o kernel já tem
   (`TheSingularityReadsTheAttractor.A1_cesaro`, o teorema ergódico médio do Mathlib).
3. **Um só boost na luz (8.5).** Para `s₀ ≠ 0`: o único `VF s₀` fixa só a reta do vácuo; o que comuta
   com ele na álgebra da cunha é escalar; e as médias dele convergem, em todo vetor, à projeção sobre
   a reta do vácuo. O kernel tem os dois primeiros para o GRUPO inteiro de boosts e não para um boost
   isolado; as médias de um boost da luz não estão no kernel (só `A1_cesaro`, genérico). É aqui que
   Mautner é usado.
4. **O domínio multiplicativo, a álgebra dos fixos e o Lema A para misturas finitas (seções 5 a 7).**
   Sem equivalente no kernel nem no Mathlib (busca recursiva nos dois).
5. **A outra direção nula em quatro dimensões (8.1)** e a covariância da translação ao longo de
   `nullMinus` sob o mesmo boost. A forma 2×2 já era do kernel (`boost_null_contract`).

## O que NÃO é novo, e está aqui só trazido à forma

- **A ergodicidade da cunha da luz livre JÁ É teorema do kernel, sem condição:**
  `LightRhoStar.centralizer_is_trivial` no certificado habitado `physicalFockCertificate`
  (`F1Fecho394\CanonicalFockModularCoreInputR1.lean`; o core e o selo da v411 trazem
  `certificate_inhabited` verdadeiro no registro `fechamento_v406`). A subseção 8.4 a reexporta
  (`a_ergodicidade_na_luz_e_do_kernel`) e dá uma segunda rota, pela translação nula, que só serve
  para mostrar que as hipóteses da seção 3 são cumpridas pela luz.
- O vácuo como único fixo da translação nula: `light_null_ergodic` no mesmo certificado.
- A unicidade do vácuo sob o grupo de boosts: `gamma_no_fixed` e `OUmInscrito.o_um_e_o_unico_fixo_da_luz`.
- A separação pelo vácuo: `canonical_wedge_separating`. A álgebra `M` como a da cunha direita física:
  sai de `physical_right_wedge_eq_KWR`, que é sobre os subespaços reais, por reescrita.
- Na torre (outro modelo), a esperança sobre o centralizador como limite de médias:
  `ChatgptAudit.Aperiodic046.aperiodicExpectationInput` (em `AperiodicCentralizerExpectation.lean`).

## De que passo da T1 cada seção é a face de kernel

- Seções 1 a 3 e 8: a proposição da cunha (`H_erg` para a cunha de Minkowski).
- Seção 7: um pedaço do Lema A (a conta da variância), para mistura FINITA e um só vetor separador.
- Seções 5 e 6: a frase do Artigo sobre o domínio multiplicativo. As provas da T1 não usam esse lema; as duas seções ficam fora do caminho crítico da T1.
- Seção 4 e a média da 8.5: só análogas ao passo de vetores (L²) do Lema B.

## O que a pedra NÃO afirma

- Não afirma o tipo III₁ de nada: o tipo não é termo do kernel. O que há é o centralizador do estado
  do vácuo na álgebra da cunha do campo LIVRE.
- Não toca o horizonte da TGL: a passagem da cunha ao horizonte é o resíduo que o Artigo nomeia e
  segue [OPEN].
- Não prova `H_K̂` nem decide se ela é o Axioma E transcrito.
- Não prova o Lema C (o produto cruzado e o comutante relativo), nem o Lema B (o traço canônico, a
  mistura gaussiana, a passagem de L² a L¹ e à topologia σ-fraca, a esperança de Takesaki), nem o
  Lema A na forma contínua (a mistura gaussiana de suporte total).
- Não formaliza a condição espectral nem Bisognano–Wichmann nas seções 1 a 4: o vácuo único nomeado
  e o boost abstrato as absorvem (na luz, a identificação do boost com o fluxo modular é do kernel). E
  não deriva a desigualdade de Schwarz da 2-positividade: a seção 5 a toma como hipótese.
- Não é a esperança condicional da álgebra: as médias das seções 4 e 8.5 são de vetores.
- O vácuo único é hipótese nas seções 3 e 4. Na luz livre ele é teorema do kernel para a translação
  ao longo de `nullDir`, e só para ela o vácuo único é pedido de 8.4 em diante; a de `nullMinus` entra
  em Mautner na luz (8.3) e, como a translação que encolhe quando `s₀ > 0`, na 8.5. No caso geral de energia positiva o vácuo único pede as duas direções nulas, e por isso a
  seção 3 as tem.
- Em dimensão finita as seções 2 a 4 são triviais: as hipóteses de covariância (na forma de uma só
  dilatação) forçam a translação a ser a identidade [DECLARADO: compilado num teste à parte, `TesteDimFinita.lean`; não é termo desta pedra]. O conteúdo
  mora em dimensão infinita; o modelo não trivial é o Fock da luz, e a álgebra `M` não é abeliana (8.4).
- O que o kernel cita como [KNOWN] na construção do boost de uma partícula e da rede da luz continua
  citado lá; esta pedra o herda e não o paga. As limitações do próprio certificado físico (o que ele
  cita e os limites que o seu registro declara) também se herdam.
- Nada sobre a natureza. O gate não se move.

## Estatutos

[REAL] o que compila aqui. [KNOWN, não conferidos no primário] o argumento de Mautner e Moore (lido
em fonte secundária); Choi 1974; Reeh–Schlieder; Bisognano–Wichmann. [KNOWN] o teorema ergódico médio
de von Neumann, na forma do Mathlib. [DECLARADO] a T1 no papel (`T1_FECHADO.md`). [OPEN] o resíduo do horizonte; `H_K̂`; o caso contínuo do
Lema A; os Lemas B e C; o tipo como termo.
-/

set_option autoImplicit false

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

/-- A mesma conclusão quando a relação vem escrita na outra ordem, `T a (U v) = U (T (q * a) v)`, com
`|q| < 1`. -/
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

/-! ## 3. O que comuta com o boost é escalar, dado o vácuo único -/

section Ergodicidade

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H]

/-- **O QUE COMUTA COM O BOOST É ESCALAR, DADO O VÁCUO ÚNICO.** `M` é uma subálgebra com unidade, `Ω` é
separador para `M` e fixo pelo boost, e vale a hipótese NOMEADA do vácuo único (todo vetor fixo pelas
duas translações é múltiplo de `Ω`). Então todo `x` de `M` que comuta com o boost é escalar. Na T1 do
papel isto é `H_erg` para a cunha; aqui o vácuo único é hipótese. -/
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

/-- **O MESMO COM UMA SÓ DILATAÇÃO.** Todo `x` de `M` que comuta com uma dilatação que fixa o vácuo
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

/-! ## 4. A média do boost converge à projeção sobre a reta do vácuo -/

section Media

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- **A MÉDIA DO BOOST CONVERGE AO VÁCUO.** Com o vácuo único e de norma 1, as médias de Cesàro de uma
dilatação convergem, em todo vetor `v`, a `⟪Ω, v⟫ • Ω`, a projeção ortogonal de `v` sobre a reta do
vácuo. É convergência de vetores; não é a esperança condicional da álgebra. -/
theorem a_media_do_boost_converge_ao_vacuo
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

/-! ## 7. A mistura de atos só deixa parado o que cada ato deixa parado (o Lema A, para misturas finitas) -/

section Mistura

variable {K : Type*} [NormedAddCommGroup K] [InnerProductSpace ℂ K]

/-- Convexidade estrita, na forma que o Lema A usa: se uma média de vetores de mesma norma que `v`
(pesos positivos, soma 1) é o próprio `v`, cada um deles é `v`. Sai também da convexidade estrita do
Mathlib (`norm_sum_lt_of_strictConvexSpace`); a conta direta foi mantida. -/
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
/-- **O LEMA A, PARA MISTURAS FINITAS.** `α i` são atos que respeitam a estrela e o produto, o estado de `Ω` é
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


/-! ## 8. Na luz: a pedra no Fock canônico da luz

Os objetos (`F`, `vacuum`, `VF`, `UF`, `nullDir`, `nullMinus`, a álgebra da cunha
`F1Fecho.CanonicalWedgeFlow.M`) e os fatos de base (a covariância do boost com as translações, a
continuidade forte, a separação pelo vácuo) são do kernel. O kernel JÁ TEM, sem condição, a
ergodicidade da cunha da luz livre: `LightRhoStar.centralizer_is_trivial` no certificado habitado
`physicalFockCertificate`. O que esta seção acrescenta: a outra direção nula em quatro dimensões
(8.1), Mautner na luz (8.3) e os teoremas de UM só boost (8.5). A subseção 8.4 traz o que é do kernel
para a forma usada aqui, e é reexportação. De 8.4 em diante o vácuo único só é pedido para a
translação ao longo de `nullDir`; a de `nullMinus` entra na 8.3 e, como a translação que encolhe
quando `s₀ > 0`, nos teoremas de um só boost da 8.5. -/

section NaLuz

open F1Rede.BosonicFock F1Rede.BosonicFockGroupActions
open TGLExt.ImportedSQ (U1 B0)
open TGLExt.ContratoQGv31 (wedgeBoostMap nullDir wedgeBoostMap_smul wedgeBoostMap_nullDir
  wedgeBoostMap_apply0 wedgeBoostMap_apply1)
open F1Fecho.MaxwellLocalization (nullMinus)
open F1Fecho.CanonicalFockModularCoreInputR1 (physicalFockCertificate)

/-! ### 8.1. A outra direção nula -/

/-- A outra direção nula, `nullMinus = (1, -1, 0, 0)`, é autodireção do boost da cunha, com fator
`exp (-s)`. É a forma em quatro dimensões; a forma 2×2 já é do kernel (`boost_null_contract`, em
`BisognanoWichmann.lean`). -/
theorem o_boost_encolhe_a_outra_direcao_nula (s : ℝ) :
    wedgeBoostMap s nullMinus = Real.exp (-s) • nullMinus := by
  have h := Real.cosh_sub_sinh s
  have e0 : nullMinus 0 = 1 := rfl
  have e1 : nullMinus 1 = -1 := rfl
  funext i
  fin_cases i
  · show wedgeBoostMap s nullMinus 0 = Real.exp (-s) * nullMinus 0
    rw [wedgeBoostMap_apply0, e0, e1, ← h]
    ring
  · show wedgeBoostMap s nullMinus 1 = Real.exp (-s) * nullMinus 1
    rw [wedgeBoostMap_apply1, e0, e1, ← h]
    ring
  · simp [nullMinus, wedgeBoostMap, TGLExt.boostMat, Matrix.mulVec, dotProduct, Fin.sum_univ_four]
  · simp [nullMinus, wedgeBoostMap, TGLExt.boostMat, Matrix.mulVec, dotProduct, Fin.sum_univ_four]

/-! ### 8.2. As três famílias como mapas lineares contínuos -/

/-- O boost da luz no Fock, `VF s`, como mapa linear contínuo. -/
noncomputable def boostNaLuz (s : ℝ) : F →L[ℂ] F :=
  (VF s).toLinearIsometry.toContinuousLinearMap

/-- A translação ao longo de `nullDir`, `UF (a • nullDir)`, como mapa linear contínuo. -/
noncomputable def translacaoNulaMais (a : ℝ) : F →L[ℂ] F :=
  (UF (a • nullDir)).toLinearIsometry.toContinuousLinearMap

/-- A translação ao longo de `nullMinus`, `UF (a • nullMinus)`, como mapa linear contínuo. -/
noncomputable def translacaoNulaMenos (a : ℝ) : F →L[ℂ] F :=
  (UF (a • nullMinus)).toLinearIsometry.toContinuousLinearMap

/-- O boost da luz preserva o produto interno. -/
theorem o_boost_na_luz_preserva_o_produto_interno (s : ℝ) (v w : F) :
    ⟪boostNaLuz s v, boostNaLuz s w⟫_ℂ = ⟪v, w⟫_ℂ :=
  (VF s).inner_map_map v w

/-- A translação ao longo de `nullDir` preserva a norma. -/
theorem a_translacao_mais_preserva_a_norma (a : ℝ) (v : F) : ‖translacaoNulaMais a v‖ = ‖v‖ :=
  (UF (a • nullDir)).norm_map v

/-- A translação ao longo de `nullMinus` preserva a norma. -/
theorem a_translacao_menos_preserva_a_norma (a : ℝ) (v : F) : ‖translacaoNulaMenos a v‖ = ‖v‖ :=
  (UF (a • nullMinus)).norm_map v

/-- Em `a = 0` a translação ao longo de `nullDir` é a identidade. -/
theorem a_translacao_mais_em_zero_e_a_identidade (v : F) : translacaoNulaMais 0 v = v := by
  show UF ((0 : ℝ) • nullDir) v = v
  rw [zero_smul, UF_zero]
  rfl

/-- Em `a = 0` a translação ao longo de `nullMinus` é a identidade. -/
theorem a_translacao_menos_em_zero_e_a_identidade (v : F) : translacaoNulaMenos 0 v = v := by
  show UF ((0 : ℝ) • nullMinus) v = v
  rw [zero_smul, UF_zero]
  rfl

/-- A translação ao longo de `nullDir` é contínua em `a = 0`, vetor a vetor. -/
theorem a_translacao_mais_e_continua_em_zero (v : F) :
    ContinuousAt (fun a : ℝ => translacaoNulaMais a v) 0 := by
  have h : Continuous (fun a : ℝ => gamma (U1 (a • nullDir)) v) :=
    (translations_strong v).comp (continuous_id.smul continuous_const)
  exact h.continuousAt

/-- A translação ao longo de `nullMinus` é contínua em `a = 0`, vetor a vetor. -/
theorem a_translacao_menos_e_continua_em_zero (v : F) :
    ContinuousAt (fun a : ℝ => translacaoNulaMenos a v) 0 := by
  have h : Continuous (fun a : ℝ => gamma (U1 (a • nullMinus)) v) :=
    (translations_strong v).comp (continuous_id.smul continuous_const)
  exact h.continuousAt

/-- A covariância na forma do kernel: o boost `VF s` leva a translação ao longo de `nullDir` de
parâmetro `a` na de parâmetro `exp s * a`. -/
theorem a_covariancia_do_boost_com_a_translacao_mais (s a : ℝ) (v : F) :
    VF s (UF (a • nullDir) v) = UF ((Real.exp s * a) • nullDir) (VF s v) := by
  have h := VF_UF_VF_symm s (a • nullDir) (VF s v)
  rw [LinearIsometryEquiv.symm_apply_apply, wedgeBoostMap_smul, wedgeBoostMap_nullDir, smul_smul,
    mul_comm a (Real.exp s)] at h
  exact h

/-- A covariância para a outra direção: o boost `VF s` leva a translação ao longo de `nullMinus` de
parâmetro `a` na de parâmetro `exp (-s) * a`. -/
theorem a_covariancia_do_boost_com_a_translacao_menos (s a : ℝ) (v : F) :
    VF s (UF (a • nullMinus) v) = UF ((Real.exp (-s) * a) • nullMinus) (VF s v) := by
  have h := VF_UF_VF_symm s (a • nullMinus) (VF s v)
  rw [LinearIsometryEquiv.symm_apply_apply, wedgeBoostMap_smul,
    o_boost_encolhe_a_outra_direcao_nula, smul_smul, mul_comm a (Real.exp (-s))] at h
  exact h

/-- O boost alarga a translação ao longo de `nullDir` por `exp s` (a forma que a seção 2 pede). -/
theorem o_boost_alarga_a_translacao_mais (s a : ℝ) (v : F) :
    boostNaLuz s (translacaoNulaMais a v) = translacaoNulaMais (Real.exp s * a) (boostNaLuz s v) :=
  a_covariancia_do_boost_com_a_translacao_mais s a v

/-- O boost encolhe a translação ao longo de `nullMinus` por `exp (-s)` (a forma que a seção 2
pede). -/
theorem o_boost_encolhe_a_translacao_menos (s a : ℝ) (v : F) :
    boostNaLuz s (translacaoNulaMenos a v)
      = translacaoNulaMenos (Real.exp (-s) * a) (boostNaLuz s v) :=
  a_covariancia_do_boost_com_a_translacao_menos s a v

/-- A mesma covariância escrita na outra ordem, para `nullDir`: a translação atravessa o boost com
o parâmetro multiplicado por `exp (-s)`. -/
theorem a_translacao_mais_atravessa_o_boost (s a : ℝ) (v : F) :
    translacaoNulaMais a (boostNaLuz s v)
      = boostNaLuz s (translacaoNulaMais (Real.exp (-s) * a) v) := by
  rw [o_boost_alarga_a_translacao_mais, ← mul_assoc, ← Real.exp_add, add_neg_cancel, Real.exp_zero,
    one_mul]

/-- A mesma covariância escrita na outra ordem, para `nullMinus`: a translação atravessa o boost com
o parâmetro multiplicado por `exp s`. -/
theorem a_translacao_menos_atravessa_o_boost (s a : ℝ) (v : F) :
    translacaoNulaMenos a (boostNaLuz s v)
      = boostNaLuz s (translacaoNulaMenos (Real.exp s * a) v) := by
  rw [o_boost_encolhe_a_translacao_menos, ← mul_assoc, ← Real.exp_add, neg_add_cancel,
    Real.exp_zero, one_mul]

/-! ### 8.3. Mautner na luz -/

/-- **MAUTNER NA LUZ.** No Fock canônico, todo vetor fixo por `VF s` para todo `s` é fixo pelas duas
translações nulas, `UF (a • nullDir)` e `UF (a • nullMinus)`, para todo `a`. -/
theorem o_fixo_do_boost_da_luz_e_fixo_das_translacoes_nulas (ψ : F) (hψ : ∀ s : ℝ, VF s ψ = ψ) :
    (∀ a : ℝ, UF (a • nullDir) ψ = ψ) ∧ (∀ a : ℝ, UF (a • nullMinus) ψ = ψ) :=
  o_fixo_do_boost_e_fixo_das_translacoes boostNaLuz translacaoNulaMais translacaoNulaMenos
    o_boost_na_luz_preserva_o_produto_interno
    a_translacao_mais_preserva_a_norma a_translacao_menos_preserva_a_norma
    a_translacao_mais_em_zero_e_a_identidade a_translacao_menos_em_zero_e_a_identidade
    a_translacao_mais_e_continua_em_zero a_translacao_menos_e_continua_em_zero
    o_boost_alarga_a_translacao_mais o_boost_encolhe_a_translacao_menos ψ hψ

/-! ### 8.4. O que é do kernel, na forma usada aqui (reexportação) -/

/-- A álgebra da cunha do certificado físico do kernel é a álgebra `M`. -/
theorem a_algebra_do_certificado_fisico_e_a_da_cunha :
    physicalFockCertificate.R
      (F1Fecho.MaxwellLocalization.physicalCanonicalNet.toLightNetData.toLightOneParticle.K
        TGL.SpecificAQFT.rightWedge)
    = F1Fecho.CanonicalWedgeFlow.M := by
  show F1Fecho.FieldWeyl.R
      (F1Fecho.MaxwellLocalization.physicalCanonicalNet.K TGL.SpecificAQFT.rightWedge)
    = F1Fecho.FieldWeyl.R F1Rede.CanonicalWedge.KWR.toClosedSubmodule.toSubmodule
  rw [F1Fecho.MaxwellLocalization.physicalCanonicalNet.wedge_glue]
  rfl

/-- `M` é a álgebra de Weyl da cunha direita física: reescrita por `physical_right_wedge_eq_KWR`, do
kernel, que é sobre os subespaços reais. -/
theorem a_algebra_da_cunha_e_a_da_cunha_direita_fisica :
    F1Fecho.CanonicalWedgeFlow.M = F1Fecho.FieldWeyl.R
      (F1Fecho.MaxwellLocalization.localized F1Fecho.MaxwellLocalization.physicalRightWedge) := by
  show F1Fecho.FieldWeyl.R _ = _
  rw [F1Fecho.MaxwellLocalization.physical_right_wedge_eq_KWR]

/-- `M` não é feita só de escalares: tem dois elementos que não comutam (campo do certificado
físico). Sem isso, dizer que o que comuta com o boost é escalar seria vazio. -/
theorem a_algebra_da_cunha_nao_e_abeliana :
    ∃ a ∈ F1Fecho.CanonicalWedgeFlow.M, ∃ b ∈ F1Fecho.CanonicalWedgeFlow.M, a * b ≠ b * a := by
  obtain ⟨a, ha, b, hb, h⟩ := physicalFockCertificate.wedge_nonabelian
  refine ⟨a, ?_, b, ?_, h⟩
  · rw [← a_algebra_do_certificado_fisico_e_a_da_cunha]
    exact ha
  · rw [← a_algebra_do_certificado_fisico_e_a_da_cunha]
    exact hb

/-- O vácuo separa a álgebra da cunha `M` (é `canonical_wedge_separating`, do kernel). -/
theorem o_vacuo_separa_a_algebra_da_cunha (x : F →L[ℂ] F)
    (hx : x ∈ F1Fecho.CanonicalWedgeFlow.M) (h0 : x vacuum = 0) : x = 0 :=
  F1Fecho.WedgeCyclic.canonical_wedge_separating x hx h0

/-- O vácuo é o único fixo da translação nula da luz: todo vetor fixo por `UF (l • nullDir)` para
todo `l` está na reta do vácuo. É `light_null_ergodic`, do kernel, no certificado físico. -/
theorem o_vacuo_e_o_unico_fixo_da_translacao_nula_da_luz (ψ : F)
    (hψ : ∀ l : ℝ, UF (l • nullDir) ψ = ψ) : ψ ∈ (ℂ ∙ vacuum) :=
  TGLExt.ImportedSQ.light_null_ergodic physicalFockCertificate ψ hψ

/-- O mesmo, na forma em que a seção 3 pede o vácuo único. -/
theorem o_fixo_da_translacao_mais_e_multiplo_do_vacuo (v : F)
    (hv : ∀ a : ℝ, translacaoNulaMais a v = v) : ∃ c : ℂ, v = c • vacuum := by
  obtain ⟨c, hc⟩ := Submodule.mem_span_singleton.mp
    (o_vacuo_e_o_unico_fixo_da_translacao_nula_da_luz v hv)
  exact ⟨c, hc.symm⟩

/-- **A ERGODICIDADE NA LUZ É DO KERNEL.** Todo `x` da álgebra da cunha `M` que comuta com `VF s` para
todo `s` é escalar. Não é resultado desta pedra: é `LightRhoStar.centralizer_is_trivial` no
certificado físico, trazido à forma em que a subseção 8.5 enuncia os teoremas de um só boost. -/
theorem a_ergodicidade_na_luz_e_do_kernel (x : F →L[ℂ] F)
    (hx : x ∈ F1Fecho.CanonicalWedgeFlow.M)
    (hxδ : ∀ (s : ℝ) (v : F), VF s (x v) = x (VF s v)) :
    ∃ c : ℂ, x = c • (1 : F →L[ℂ] F) := by
  have hx' : x ∈ physicalFockCertificate.R
      (F1Fecho.MaxwellLocalization.physicalCanonicalNet.toLightNetData.toLightOneParticle.K
        TGL.SpecificAQFT.rightWedge) := by
    rw [a_algebra_do_certificado_fisico_e_a_da_cunha]
    exact hx
  let a : (physicalFockCertificate.R
      (F1Fecho.MaxwellLocalization.physicalCanonicalNet.toLightNetData.toLightOneParticle.K
        TGL.SpecificAQFT.rightWedge)).toStarSubalgebra := ⟨x, hx'⟩
  have ha : ∀ t : ℝ, physicalFockCertificate.flow t a = a := by
    intro t
    apply Subtype.ext
    rw [physicalFockCertificate.flow_is_Ad t a]
    ext v
    have h := hxδ (-(2 * Real.pi * t)) ((gamma (B0 (-(2 * Real.pi * t)))).symm v)
    have h2 : VF (-(2 * Real.pi * t)) ((gamma (B0 (-(2 * Real.pi * t)))).symm v) = v :=
      LinearIsometryEquiv.apply_symm_apply _ _
    rw [h2] at h
    exact h
  exact TGLExt.LightRhoStar.centralizer_is_trivial physicalFockCertificate a ha

/-- A mesma conclusão por uma segunda rota, a da translação nula: Mautner (seção 2), o vácuo único
sob a translação ao longo de `nullDir` e a separação pelo vácuo. Mostra que as hipóteses da seção 3
são todas cumpridas pela luz do kernel. -/
theorem a_ergodicidade_na_luz_pela_translacao_nula (x : F →L[ℂ] F)
    (hx : x ∈ F1Fecho.CanonicalWedgeFlow.M)
    (hxδ : ∀ (s : ℝ) (v : F), VF s (x v) = x (VF s v)) :
    ∃ c : ℂ, x = c • (1 : F →L[ℂ] F) :=
  o_que_comuta_com_o_boost_e_escalar boostNaLuz translacaoNulaMais translacaoNulaMenos
    o_boost_na_luz_preserva_o_produto_interno
    a_translacao_mais_preserva_a_norma a_translacao_menos_preserva_a_norma
    a_translacao_mais_em_zero_e_a_identidade a_translacao_menos_em_zero_e_a_identidade
    a_translacao_mais_e_continua_em_zero a_translacao_menos_e_continua_em_zero
    o_boost_alarga_a_translacao_mais o_boost_encolhe_a_translacao_menos
    F1Fecho.CanonicalWedgeFlow.M.toStarSubalgebra.toSubalgebra vacuum
    (fun y hy h0 => o_vacuo_separa_a_algebra_da_cunha y hy h0) VF_vacuum
    (fun v hp _ => o_fixo_da_translacao_mais_e_multiplo_do_vacuo v hp) x hx hxδ

/-! ### 8.5. Um só boost -/

/-- A exponencial de um número negativo tem módulo menor que 1. -/
theorem a_exponencial_de_um_negativo_encolhe {t : ℝ} (ht : t < 0) : |Real.exp t| < 1 := by
  rw [abs_of_pos (Real.exp_pos t)]
  exact Real.exp_lt_one_iff.mpr ht

/-- **UM SÓ BOOST FIXA SÓ O VÁCUO.** Para `s₀ ≠ 0`, todo vetor fixo pelo único `VF s₀` está na reta
do vácuo. Se `s₀ < 0`, o boost encolhe a translação ao longo de `nullDir`; se `s₀ > 0`, usa-se a
mesma relação escrita na outra ordem. Nos dois casos o vetor é fixo por essa translação (seção 2),
e daí está na reta do vácuo. O kernel tem este resultado para o grupo inteiro de boosts; para um
boost isolado, não. -/
theorem o_fixo_de_um_so_boost_da_luz_e_o_vacuo (s₀ : ℝ) (hs : s₀ ≠ 0) (ψ : F)
    (hψ : VF s₀ ψ = ψ) : ψ ∈ (ℂ ∙ vacuum) := by
  apply o_vacuo_e_o_unico_fixo_da_translacao_nula_da_luz
  rcases lt_or_gt_of_ne hs with h | h
  · exact o_fixo_de_uma_dilatacao_e_fixo_da_translacao (boostNaLuz s₀) translacaoNulaMais
      (Real.exp s₀) (a_exponencial_de_um_negativo_encolhe h)
      (o_boost_na_luz_preserva_o_produto_interno s₀) a_translacao_mais_preserva_a_norma
      a_translacao_mais_em_zero_e_a_identidade a_translacao_mais_e_continua_em_zero
      (o_boost_alarga_a_translacao_mais s₀) ψ hψ
  · exact o_fixo_de_uma_dilatacao_e_fixo_da_outra_translacao (boostNaLuz s₀) translacaoNulaMais
      (Real.exp (-s₀)) (a_exponencial_de_um_negativo_encolhe (neg_lt_zero.mpr h))
      (o_boost_na_luz_preserva_o_produto_interno s₀) a_translacao_mais_preserva_a_norma
      a_translacao_mais_em_zero_e_a_identidade a_translacao_mais_e_continua_em_zero
      (fun a v => a_translacao_mais_atravessa_o_boost s₀ a v) ψ hψ

/-- Os fixos de um só boost `VF s₀`, `s₀ ≠ 0`, são exatamente os múltiplos do vácuo. -/
theorem os_fixos_de_um_so_boost_da_luz_sao_a_reta_do_vacuo (s₀ : ℝ) (hs : s₀ ≠ 0) (v : F) :
    VF s₀ v = v ↔ ∃ c : ℂ, v = c • vacuum := by
  constructor
  · intro hv
    obtain ⟨c, hc⟩ := Submodule.mem_span_singleton.mp
      (o_fixo_de_um_so_boost_da_luz_e_o_vacuo s₀ hs v hv)
    exact ⟨c, hc.symm⟩
  · rintro ⟨c, rfl⟩
    rw [map_smul, VF_vacuum]

/-- **O QUE COMUTA COM UM SÓ BOOST DA LUZ É ESCALAR.** Para `s₀ ≠ 0`, todo `x` da álgebra da cunha
`M` que comuta com o único `VF s₀` é escalar. Pela seção 3, na forma de uma só dilatação; conforme
o sinal de `s₀`, a translação que encolhe é a de `nullDir` ou a de `nullMinus`. -/
theorem o_que_comuta_com_um_so_boost_da_luz_e_escalar (s₀ : ℝ) (hs : s₀ ≠ 0) (x : F →L[ℂ] F)
    (hx : x ∈ F1Fecho.CanonicalWedgeFlow.M) (hxU : ∀ v : F, VF s₀ (x v) = x (VF s₀ v)) :
    ∃ c : ℂ, x = c • (1 : F →L[ℂ] F) := by
  rcases lt_or_gt_of_ne hs with h | h
  · exact o_que_comuta_com_uma_dilatacao_e_escalar (boostNaLuz s₀) translacaoNulaMais
      translacaoNulaMenos (Real.exp s₀) (a_exponencial_de_um_negativo_encolhe h)
      (o_boost_na_luz_preserva_o_produto_interno s₀)
      a_translacao_mais_preserva_a_norma a_translacao_menos_preserva_a_norma
      a_translacao_mais_em_zero_e_a_identidade a_translacao_menos_em_zero_e_a_identidade
      a_translacao_mais_e_continua_em_zero a_translacao_menos_e_continua_em_zero
      (o_boost_alarga_a_translacao_mais s₀)
      (fun a v => a_translacao_menos_atravessa_o_boost s₀ a v)
      F1Fecho.CanonicalWedgeFlow.M.toStarSubalgebra.toSubalgebra vacuum
      (fun y hy h0 => o_vacuo_separa_a_algebra_da_cunha y hy h0) (VF_vacuum s₀)
      (fun v hp _ => o_fixo_da_translacao_mais_e_multiplo_do_vacuo v hp) x hx hxU
  · exact o_que_comuta_com_uma_dilatacao_e_escalar (boostNaLuz s₀) translacaoNulaMenos
      translacaoNulaMais (Real.exp (-s₀))
      (a_exponencial_de_um_negativo_encolhe (neg_lt_zero.mpr h))
      (o_boost_na_luz_preserva_o_produto_interno s₀)
      a_translacao_menos_preserva_a_norma a_translacao_mais_preserva_a_norma
      a_translacao_menos_em_zero_e_a_identidade a_translacao_mais_em_zero_e_a_identidade
      a_translacao_menos_e_continua_em_zero a_translacao_mais_e_continua_em_zero
      (o_boost_encolhe_a_translacao_menos s₀)
      (fun a v => a_translacao_mais_atravessa_o_boost s₀ a v)
      F1Fecho.CanonicalWedgeFlow.M.toStarSubalgebra.toSubalgebra vacuum
      (fun y hy h0 => o_vacuo_separa_a_algebra_da_cunha y hy h0) (VF_vacuum s₀)
      (fun v _ hp => o_fixo_da_translacao_mais_e_multiplo_do_vacuo v hp) x hx hxU

/-- **A MÉDIA DE UM SÓ BOOST DA LUZ CONVERGE AO VÁCUO.** Para `s₀ ≠ 0`, as médias de Cesàro de
`VF s₀` convergem, em todo vetor `v` do Fock, a `⟪vacuum, v⟫ • vacuum`, a projeção ortogonal de `v`
sobre a reta do vácuo. É convergência de vetores; não é a esperança condicional da álgebra. -/
theorem a_media_de_um_so_boost_da_luz_converge_ao_vacuo (s₀ : ℝ) (hs : s₀ ≠ 0) (v : F) :
    Tendsto (birkhoffAverage ℂ (boostNaLuz s₀) id · v) atTop (𝓝 (⟪vacuum, v⟫_ℂ • vacuum)) := by
  rcases lt_or_gt_of_ne hs with h | h
  · exact a_media_do_boost_converge_ao_vacuo (boostNaLuz s₀) translacaoNulaMais
      translacaoNulaMenos (Real.exp s₀) (a_exponencial_de_um_negativo_encolhe h)
      (o_boost_na_luz_preserva_o_produto_interno s₀)
      a_translacao_mais_preserva_a_norma a_translacao_menos_preserva_a_norma
      a_translacao_mais_em_zero_e_a_identidade a_translacao_menos_em_zero_e_a_identidade
      a_translacao_mais_e_continua_em_zero a_translacao_menos_e_continua_em_zero
      (o_boost_alarga_a_translacao_mais s₀)
      (fun a w => a_translacao_menos_atravessa_o_boost s₀ a w)
      vacuum (VF_vacuum s₀) vacuum_norm
      (fun w hp _ => o_fixo_da_translacao_mais_e_multiplo_do_vacuo w hp) v
  · exact a_media_do_boost_converge_ao_vacuo (boostNaLuz s₀) translacaoNulaMenos
      translacaoNulaMais (Real.exp (-s₀))
      (a_exponencial_de_um_negativo_encolhe (neg_lt_zero.mpr h))
      (o_boost_na_luz_preserva_o_produto_interno s₀)
      a_translacao_menos_preserva_a_norma a_translacao_mais_preserva_a_norma
      a_translacao_menos_em_zero_e_a_identidade a_translacao_mais_em_zero_e_a_identidade
      a_translacao_menos_e_continua_em_zero a_translacao_mais_e_continua_em_zero
      (o_boost_encolhe_a_translacao_menos s₀)
      (fun a w => a_translacao_mais_atravessa_o_boost s₀ a w)
      vacuum (VF_vacuum s₀) vacuum_norm
      (fun w _ hp => o_fixo_da_translacao_mais_e_multiplo_do_vacuo w hp) v

end NaLuz


end TGLExt.ErgodicidadeDeMautner
