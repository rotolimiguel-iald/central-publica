# K05/A/T1 — fechamento condicionado do produto cruzado e face finita

**Escopo.** Somente a seção A/T1 da K05/v412. Nada aqui registra, deposita, instala ou altera o kernel canônico.
**Veredito.** O remark do artigo vira UM teorema condicionado a `H_K̂`, `H_erg` e, para a aplicação à TGL, à hipótese física nomeada `H_TGL-horizon`. Não se afirma que III₁ tenha centralizador trivial, nem que `Fix = W*(K̂)` valha sem injetividade essencial.
**Estatutos.** `[REAL]` = compilado/consultado aqui; `[DERIVED]` = prova escrita aqui; `[KNOWN, a conferir]` = literatura consultada com identificador; `[OPEN]` = não fechado.

## 1. Ponto de partida e aferição

O artigo define `Φ_t = ∫ Ad(e^{is√K})dN(0,βt)(s)` e depois afirma, no produto cruzado, `Fix = W*(K̂)` e `Φ_t → E` σ-fracamente, mas não define `K̂` nem prova essas duas afirmações. [A Ponte Einstein Cartan Miguel](kimi-cite://md-line?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2FA%20Ponte%20Einstein%20Cartan%20Miguel.tex&line=1888&text=e%5Et%7B%5Cmathcal%20L%7D "citation"), [A Ponte Einstein Cartan Miguel](kimi-cite://md-line?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2FA%20Ponte%20Einstein%20Cartan%20Miguel.tex&line=1903 "citation")

Consultas efetivamente feitas antes de declarar ausência `[REAL]`:

- `python C:\IALD\MAPA_DE_ROTAS\rotas.py consultar "T1 produto cruzado comutante relativo ergodicidade cunha"`: 0 rotas, 2056 registros, cabeça `03042aca2e30e8cf`.
- Inventário da bancada: há `specExpect`, pinching finito, `V351AverageFixedPair` e `ModularGeneratorControl`; não há o teorema UCP normal contínuo desta T1.
- Kernel, somente leitura: `AperiodicPhaseAverage.flow_average_limit` prova pinching para média de fases; `EquivariantSection` trata degenerescências. A média gaussiana `Φ_t` desta K05 não estava provada.
- Atlas: os verbetes “Ergodicidade (T1)” e “Takesaki (produto cruzado, 1973)” foram lidos como remissões, não como fonte primária.
- `python C:\IALD\INDICE_DO_ACERVO\buscar.py "Digernes|Borchers|Mautner|Choi|Kadison" --lista`: executado; saída preservada em `K05/sandbox_t1/logs/acervo_T1.log`.
- A K02 antiga foi lida inteira, com a errata e a revisão K02 inteira, especialmente §4. A candidata antiga não foi alterada; a nota de arquivamento está em `K05/T1/ARQUIVAMENTO_T1_K02.md`.

## 2. Convenções e hipóteses nomeadas

Seja `M` uma álgebra de von Neumann σ-finita e `φ` um peso normal fiel semifinito; quando um argumento usar diretamente o vetor GNS sem localização, `φ` será um estado normal fiel. Escreva `σ = σ^φ` e `M_φ = {x∈M : σ_t(x)=x ∀t}`.

No produto cruzado modular `M̂ = M ⋊_σ ℝ`, uso

`(π(a)ξ)(s) = σ_{-s}(a)ξ(s)`, `λ(t)ξ(s)=ξ(s-t)`, `ρ(t)ξ(s)=ξ(s+t)`.

O gerador de Stone é escrito de duas formas equivalentes: `λ(t)=h^{it}=e^{itĥ}`, com `h>0` e `ĥ=log h` autoadjunto. Trocar o sinal dessa convenção troca apenas os sinais nas fórmulas. Ponho `L(ℝ)=λ(ℝ)″ = W*(ĥ)`. A notação `M_φ ⊗̄ L(ℝ)` é entendida dentro de `M̂`, após o flip tensorial evidente.

**H_K̂ (estrutura espectral).** `K̂=F(ĥ)≥0` é afiliado a `L(ℝ)`, `F:ℝ→[0,∞)` é boreliana e essencialmente injetiva para a medida de Lebesgue. Ponho `G=√F` e `u_s=e^{is√K̂}=e^{isG(ĥ)}`.

**H_erg (ergodicidade).** `M_φ=ℂ1`, para o mesmo `φ` usado no produto cruzado.

**H_TGL-horizon [OPEN — hipótese física].** Existe uma identificação normal *-isomórfica da álgebra de horizonte da TGL com o modelo de cunha usado em §7, transportando o peso, o fluxo modular, os boosts, a condição espectral, a unicidade do vácuo e a realização de `K̂`. Este passo Minkowski→TGL não é deduzido de III₁ nem de BW; é uma hipótese física separada.

## 3. Lema C — o comutante relativo no produto cruzado

**Enunciado `[DERIVED sobre Digernes–Takesaki e a fatia de Tomita]`.**

`λ(ℝ)′ ∩ M̂ = M_φ ⊗̄ L(ℝ) = (π(M_φ) ∪ λ(ℝ))″`.

Além disso, `L(ℝ)` é maximal abeliana em `M̂` **se e somente se** `M_φ=ℂ1`.

**Entrada por citação.** O teorema de Digernes–Takesaki realiza

`M̂ = (M ⊗̄ B(L²(ℝ)))^{σ⊗Adρ}`.

Takesaki, 2003, *Theory of Operator Algebras II*, cap. X, Cor. 1.22, DOI do volume `10.1007/978-3-662-10451-4`; Andreou, 2020, arXiv:2004.07169, p. 14, reproduz exatamente essa referência. [KNOWN, a conferir]. [Andreou 2020](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fpdf%2F2004.07169&text=According%20to%20the%20Digernes-Takesaki%20theorem%20(see%20for%20example%20%5B32%2C%20Chapter%20X%2C%20Corollary%201.22%5D) "citation")

**Prova `[DERIVED]`.**

1. Como a representação regular de ℝ é abeliana e maximal abeliana, `λ(ℝ)′=λ(ℝ)″=L(ℝ)` em `B(L²(ℝ))`. O teorema de comutação tensorial dá, após o flip,

   `(1⊗λ(ℝ))′ ∩ (B(L²(ℝ)) ⊗̄ M) = L(ℝ) ⊗̄ M`.

2. Se `x∈M̂` comuta com `1⊗λ(ℝ)`, então `x∈L(ℝ)⊗̄M`. Como `ρ_t∈L(ℝ)` e esta álgebra é abeliana, `Adρ_t` age trivialmente sobre `x`. A condição de ponto fixo de Digernes–Takesaki reduz-se a `(id⊗σ_t)(x)=x` para todo `t`.
3. A fatia de Tomita para a ação tensorizada `id⊗σ` dá

   `(L(ℝ)⊗̄M)^{id⊗σ}=L(ℝ)⊗̄M_φ`.

   Essa é a mesma hipótese de fatia usada na revisão K02; ela entra por citação a Takesaki, 2003, não por uma nova prova de Tomita.
4. Como `L(ℝ)` já está contida no comutante relativo, ela é maximal abeliana exatamente quando o comutante relativo não contém nenhum fator adicional, isto é, `M_φ=ℂ1`. ∎

**Consequência.** Centralizador trivial e maximalidade de `L(ℝ)` são equivalentes neste produto cruzado. O tipo III₁ sozinho não aparece nessa equivalência e não fornece `M_φ=ℂ1`.

## 4. Lema A — pontos fixos da mistura, sem hipóteses supérfluas

**Enunciado `[DERIVED]`.** Seja `N` uma álgebra de von Neumann, `α_s=Ad(u_s)` um grupo fortemente contínuo de automorfismos e

`Φ_t(x)=∫_ℝ α_s(x)dν_t(s)`, `ν_t=N(0,βt)`, `β>0`, `t>0`,

como integral UCP normal. Suponha uma família fiel `{ω_ι}` de estados normais, isto é, `ω_ι(x*x)=0 ∀ι ⇒ x=0`, tal que `ω_ι∘α_s=ω_ι` para todos `ι,s`. Então, para cada `t>0`,

`Fix(Φ_t) = {u_s : s∈ℝ}′ ∩ N`.

Em particular, o setor fixo é um comutante relativo; nenhuma maximalidade abeliana está incluída no Lema A.

**Prova.** A inclusão `{u_s}′∩N⊂Fix(Φ_t)` é imediata porque `ν_t` é probabilidade. Reciprocamente, se `Φ_t(x)=x`, ponha `y_s=α_s(x)-x`. Pela invariância de cada estado,

`ω_ι(y_s*y_s)=2ω_ι(x*x)-ω_ι(x*α_s(x))-ω_ι(α_s(x*)x)`.

Integrando em `ν_t` e usando `Φ_t(x)=x`, obtém-se `∫ω_ι(y_s*y_s)dν_t(s)=0`. O integrando é não negativo e contínuo; `ν_t` tem suporte total em ℝ. Logo `y_s=0` para todo `s`, primeiro quase certamente e depois por continuidade. A fidelidade da família conclui. ∎

**A igualdade correta de Kadison–Schwarz.** Para `x∈Fix(Φ_t)`, a invariância dá

`ω_ι(Φ_t(x*x)-Φ_t(x)*Φ_t(x))=0`,

e analogamente para `xx*`. Os dois defeitos são positivos por Kadison–Schwarz e anulam-se pela família fiel. Para um mapa unital 2-positivo `Φ`, Choi prova que as duas igualdades

`Φ(x*x)=Φ(x*)Φ(x)`, `Φ(xx*)=Φ(x)Φ(x*)`

caracterizam o domínio multiplicativo bilateral; em uma única direção, `Φ(x*x)=Φ(x*)Φ(x)` já implica `Φ(ax)=Φ(a)Φ(x)` para todo `a`. Choi, 1974, *Illinois J. Math.* 18(4), 565–574, Theorem 3.1 e Corollary 2.8, DOI `10.1215/ijm/1256051007`. [KNOWN, a conferir]. [Choi 1974](kimi-cite://web?url=https%3A%2F%2Fprojecteuclid.org%2Fjournals%2Fillinois-journal-of-mathematics%2Fvolume-18%2Fissue-4%2FA-schwarz-inequality-for-positive-linear-maps-on-Cast-algebras%2F10.1215%2Fijm%2F1256051007.pdf "citation")

Esse passo multiplicativo é compatível com a prova, mas não substitui a família fiel nem o argumento de suporte total.

**Testemunha no produto cruzado, sem exigir estado tracial.** Com o traço canônico `τ`, seja `d=f(ĥ)>0` uma densidade boreliana de suporte 1 com `τ(d)<∞` e normalize

`ω_d(x)=τ(d^{1/2}xd^{1/2})/τ(d)`.

Então `ω_d` é normal fiel. Como `d` comuta com toda função boreliana de `ĥ`, em particular com `u_s`, a tracialidade de `τ` dá `ω_d∘Ad(u_s)=ω_d`. Uma testemunha explícita, na normalização de §6, é `d=e^{-\hat h^2-\hat h}`, com `τ(d)=c_φ∫_ℝe^{-p²-2p}dp<∞`. A forma sugerida `d=f(K̂)` também serve quando `f∘F>0` q.c. e `τ(f(K̂))<∞`; não imponho essa integrabilidade adicional porque `f(ĥ)` já fornece a família fiel invariante.

## 5. H_K̂, a fórmula exata do setor fixo e o caso não injetivo

### 5.1 Sob injetividade essencial

`[DERIVED]` Como `F` é essencialmente injetiva, `G=√F` também o é. Pelo cfc boreliano e pela recuperação das projeções espectrais pelo grupo de Stone,

`W*(u_s:s∈ℝ)=W*(G(ĥ))=L(ℝ)`,

e, por positividade,

`W*(√K̂)=W*(K̂)=L(ℝ)`.

Lemas A e C implicam, para cada `t>0`,

`Fix(Φ_t)={u_s}′∩M̂=λ(ℝ)′∩M̂=M_φ⊗̄L(ℝ)`.

Portanto:

- **Sob H_K̂**, `Fix=M_φ⊗̄L(ℝ)` sempre.
- **Sob H_K̂**, `Fix=W*(K̂)` **se e somente se** `M_φ=ℂ1`, pois `W*(K̂)=L(ℝ)`.
- Sem injetividade essencial, mas mantendo `K̂` afiliado a `L(ℝ)` — ou supondo explicitamente as hipóteses do Lema A —, a identidade geral que permanece é `Fix=W*(√K̂)′∩M̂`. Ela coincide com `M_φ⊗̄L(ℝ)` exatamente quando esse comutante coincide com `λ(ℝ)′∩M̂`; a condição `W*(√K̂)=L(ℝ)` é a hipótese espectral suficiente usada aqui, não uma afirmação de que seja necessária em todos os modelos.

### 5.2 O argumento de paridade: fechado sob hipóteses explícitas

**H_paridade.** `K̂=ĥ²`, `G(ĥ)=|ĥ|`; `φ` é um estado normal fiel e o espaço Hilbert standard de `M` é separável.

Defina o espectro pontual algébrico

`D={ω∈ℝ : ∃x≠0 em M com σ_t(x)=e^{iωt}x ∀t}`.

`D` é contável: se `x` é um autooperador, `xΩ` é um autovetor do grupo modular no Hilbert standard; é não nulo por separação, e autovetores de frequências distintas são ortogonais. Separabilidade limita `D` a um conjunto contável.

`[DERIVED sob H_paridade]` Também aqui `Fix(Φ_t)=M_φ⊗̄L(ℝ)`:

1. Todo ponto fixo comuta com `e^{is|ĥ|}` e decompõe-se, para `g>0`, nas fibras de dois pontos `{-g,+g}` como uma matriz `2×2` com entradas limitadas em `M`.
2. A condição de ponto fixo de Digernes–Takesaki dá, às entradas fora da diagonal, a lei `σ_t(a_g)=e^{±2igt}a_g`; às diagonais dá `σ_t(a_g)=a_g`. O sinal depende da convenção de `ρ`, sem efeito no argumento.
3. Se `2g∉D`, as entradas fora da diagonal anulam-se. Como `D` é contável, isso vale para quase todo `g>0`. As entradas diagonais pertencem a `M_φ`. O caso `g=0` tem fibra de um só ponto e é imediato.
4. Logo o ponto fixo é decomponível diagonalmente com valores em `M_φ`, isto é, pertence a `M_φ⊗̄L(ℝ)`. A inclusão reversa é imediata. ∎

**Contraexemplo `ĥ²/|ĥ|`.** `W*(K̂)=W*(ĥ²)` é a álgebra das funções pares, enquanto `W*(√K̂)=W*(|ĥ|)` também é própria em `L(ℝ)`. Sob `H_paridade` e `H_erg`, `Fix=L(ℝ)` contém a projeção sobre a parte ímpar, que não pertence a `W*(K̂)`. Assim `W*(K̂)⊊Fix`, apesar de `M_φ=ℂ1`.

### 5.3 O que NÃO se pode afirmar para toda F não injetiva

`[OPEN para F boreliana arbitrária]` A contabilidade de `D` usa, na prova acima, entradas limitadas nas fibras de dois pontos. Ela não autoriza uma conclusão universal para fibras mensuráveis infinitas nem para uma `F` qualquer. A forma universal “não injetividade implica `Fix=M_φ⊗̄L(ℝ)`” é falsa já em `F≡0`: nesse caso `u_s=1` e `Fix=M̂`, não necessariamente `M_φ⊗̄L(ℝ)`.

O argumento da gerência fica, portanto, **provado para paridade sob H_paridade**, e **aberto para F não injetiva arbitrária**. Não o transformo em decreto geral.

## 6. Lema B — traço canônico, expectativa e convergência

### 6.1 O que é automático e o que não é

Seja `τ` o traço normal fiel semifinito canônico de `M̂`.

- **Invariância automática.** Todo `Ad(u_s)` preserva `τ`; logo toda mistura `Φ_t` preserva `τ`.
- **Predual automático.** Para o traço semifinito, `M̂_* = L¹(M̂,τ)` pela realização de Segal–Dixmier; não é necessária a teoria de Haagerup–Terp. [KNOWN, a conferir]. [Realização Lp, 2016, §2.3](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F1603.01735v1&text=Thus%2C%20L1(%E2%84%B3%2C%CF%84)%20is%20the%20predual%20of%20%E2%84%B3 "citation")
- **Modular trivial.** `σ^τ=id`; portanto toda subálgebra de von Neumann é invariante pelo grupo modular de `τ`.
- **Semifinitude da restrição NÃO automática.** Se `R` é II₁ com traço finito `τ_R`, `A₀⊂R` é uma masa e `N=A₀⊗1 ⊂ R⊗B(ℓ²)`, então `τ=τ_R⊗Tr` é trivialmente modular, mas toda projeção não nula de `N` tem traço `τ_R(q)·∞=∞`. A restrição não é semifinita.

Takesaki, 1972, *J. Funct. Anal.* 9, 306–321, DOI `10.1016/0022-1236(72)90004-3`, exige as duas condições para a expectativa que preserva o peso: invariância modular da subálgebra **e** semifinitude da restrição do peso. [KNOWN, a conferir]. [Takesaki 1972](kimi-cite://web?url=https%3A%2F%2Fwww.sciencedirect.com%2Fscience%2Farticle%2Fpii%2F0022123672900043 "citation")

### 6.2 Por que H_K̂ fornece cantos finitos

Na normalização `λ(t)=h^{it}`, o traço canônico restringe-se a `L(ℝ)` por uma medida equivalente à de Lebesgue:

`τ(f(ĥ))=c_φ∫_ℝ f(p)e^{-p}dp` para `f≥0` boreliana,

com `0<c_φ<∞`; multiplicando o traço por uma constante positiva, escolho `c_φ=1`. Para um estado normal fiel, a normalização usual dá `c_φ=φ(1)=1`. Para um peso geral, `c_φ` denota a constante finita da normalização escolhida, não se escreve `φ(1)` como se fosse necessariamente finito. A convenção oposta troca `e^{-p}` por `e^{p}`. A existência do traço canônico, sua dualidade e essa normalização entram por Takesaki, 1973, *Acta Math.* 131, 249–310, DOI `10.1007/BF02392041`, e Connes–Takesaki, 1977, *Tohoku Math. J.* 29, 473–575, DOI `10.2748/tmj/1178240493`. [KNOWN, a conferir]. [Takesaki 1973](kimi-cite://web?url=https%3A%2F%2Fprojecteuclid.org%2Fjournals%2Facta-mathematica%2Fvolume-131%2Fissue-none%2FDuality-for-crossed-products-and-the-structure-of-von-Neumann%2F10.1007%2FBF02392041.full "citation"), [Connes–Takesaki 1977](kimi-cite://web?url=https%3A%2F%2Fprojecteuclid.org%2Fjournals%2Ftohoku-mathematical-journal%2Fvolume-29%2Fissue-4%2FThe-flow-of-weights-on-factors-of-type-rm-III%2F10.2748%2Ftmj%2F1178240493.full "citation")

Se `K̂` é afiliado a `L(ℝ)` — já mais fraco que H_K̂ — então `L(ℝ)⊂Fix(Φ_t)=:N`, pois todas as funções de `ĥ` comutam com `u_s`. Ponha

`e_i=1_{[-i,i]}(ĥ)`.

Então `e_i∈L(ℝ)⊂N`, `e_i↑1`, `τ(e_i)<∞`, e cada `e_i` comuta com `u_s`. Para `x∈N_+`, ponha `y_i=x^{1/2}e_i x^{1/2}`. Então `y_i∈N_+`, `0≤y_i≤x` e `τ(y_i)=τ(e_i x e_i)≤‖x‖τ(e_i)<∞`. Se `x≠0`, algum `y_i≠0`, pois `e_i→1` fortemente. Assim, todo elemento positivo não nulo de `N` domina um elemento positivo não nulo de traço finito; logo `τ|_N` é semifinito. Takesaki 1972 fornece a única expectativa condicional normal `E_τ:M̂→N` com `τ∘E_τ=τ`. Não é preciso supor separadamente `H_E` nem `H_Lp`.

### 6.3 A função gaussiana e o indicador da diagonal

`[DERIVED]` Fixe `e=e_i` e `H=G(ĥ)=√K̂`. Em `eM̂e`, `eHe` é afiliado ao canto e pode ser não limitado, pois `F` é apenas boreliana; isso não exige hipótese adicional de limitação local. Sobre `L²(eM̂e,τ)`, a implementação standard de `Ad(e^{isH})` é `U_s=e^{isA_e}`, com o gerador autoadjunto

`A_e = L_{eHe}-R_{eHe}`

(multiplicação à esquerda menos à direita, em seu domínio natural). Pela função característica gaussiana e pelo cfc desse gerador,

`T_t^{(e)} := ∫U_s dν_t(s) = e^{-\frac12βt A_e²}`.

Na resolução espectral conjunta das multiplicações à esquerda e à direita, o integrando é exatamente

`e^{-\frac12βt(a-b)²}`,

e seu limite pontual é `1_Δ(a,b)`, onde `Δ={(a,b):a=b}` é o indicador da diagonal. Convergência dominada espectral dá

`T_t^{(e)}ξ → P_{\ker A_e}ξ` em `L²`.

Mas `P_{\ker A_e}` é a projeção sobre `L²(eNe)`, que é a extensão ortogonal de `E_τ` no canto. Logo `Φ_t(x)→E_τ(x)` em `L²` para `x∈eM̂e`.

### 6.4 De L² a L¹ e à topologia σ-fraca

Como `τ(e)<∞`, Hölder dá

`‖Φ_t(x)-E_τ(x)‖₁ ≤ τ(e)^{1/2}‖Φ_t(x)-E_τ(x)‖₂ → 0`.

Além disso `‖Φ_t(x)-E_τ(x)‖∞≤2‖x‖`. Para um funcional normal qualquer no canto, aproxime sua densidade `L¹` por uma densidade limitada `b` e use

`|ψ(z)| ≤ ‖ψ-ψ_b‖₁‖z‖∞ + ‖b‖∞‖z‖₁`.

Resulta `ψ(Φ_t(x))→ψ(E_τ(x))` para todo `ψ` normal no canto.

Para `x∈M̂` e `ψ∈M̂_*=L¹(M̂,τ)`, use `e_i↑1` e a convergência `e_i a e_i→a` em `L¹` para a densidade `a` de `ψ`. Como `e_i∈N`,

`e_iΦ_t(x)e_i=Φ_t(e_ixe_i)`, `e_iE_τ(x)e_i=E_τ(e_ixe_i)`.

O canto já dá a convergência para `ψ_i(y)=ψ(e_iye_i)`. Por contratividade uniforme,

`|(ψ-ψ_i)(Φ_t(x)-E_τ(x))| ≤ 2‖ψ-ψ_i‖‖x‖`.

Logo `ψ(Φ_t(x))→ψ(E_τ(x))`, isto é, `Φ_t→E_τ` σ-fracamente. ∎

**Onde a prova falha sem as hipóteses.** Sem `τ|_N` semifinito, Takesaki 1972 não fornece `E_τ` e pode não haver cantos finitos de `N` cobrindo `1`. Sem afiliação de `K̂` a `L(ℝ)`, a sequência `e_i` acima não está garantida em `N`. Sem invariância de `τ`, a implementação unitária e a contratividade usadas na passagem global falham. No modelo externo `L∞(ℝ)` com translações e medida de Lebesgue, `Fix=ℂ1`, `τ(1)=∞` e não existe expectativa normal τ-preservante sobre as constantes; ele ilustra a obstrução, embora não se apresente como exemplo de automorfismos internos.

## 7. H_erg na cunha — prova Borchers–Mautner com hipóteses

**Entrada por citação.** Bisognano–Wichmann identifica o grupo modular da álgebra da cunha com os boosts, nas hipóteses Wightman/AQFT: Bisognano–Wichmann, 1975, *J. Math. Phys.* 16, 985–1007, DOI `10.1063/1.522605`; 1976, *J. Math. Phys.* 17, 303–321, DOI `10.1063/1.522898`. Ver também Guido, 2008/2011, arXiv:0812.1511, *Contemp. Math.* 534, 97–120. [KNOWN, a conferir]. [Bisognano–Wichmann 1976](kimi-cite://web?url=http%3A%2F%2Fdenebola.if.usp.br%2F~jbarata%2Fleituras-recomendadas%2FBisognanoWichmann-02-DualityConditionQuantumFields_303_1_online.pdf "citation"), [Guido 2008](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F0812.1511 "citation")

**Hipóteses do argumento.** Representação fortemente contínua e Poincaré-covariante, espectro das translações em `\bar V_+`, vácuo `Ω` único a menos de escalar, Reeh–Schlieder para a cunha e BW.

**Prova `[DERIVED]`.** Seja `x∈M_Ω` e `ξ=xΩ`. Como `x` é modular-fixo e `Δ^{it}Ω=Ω`, `ξ` é invariante pelos boosts. Escolha vetores nulos `a_+=(1,1,0,0)` e `a_-=(1,-1,0,0)`. O boost satisfaz `Λ(s)a_±=e^{±s}a_±`. Para `f(r)=⟨ξ,U(ra_+)ξ⟩`, covariância e invariância dão

`f(r)=f(e^{-s}r)→f(0)=‖ξ‖²` quando `s→∞`.

Pela continuidade forte, `f(r)=‖ξ‖²` para todo `r`. Daí `‖U(ra_+)ξ-ξ‖²=0`, logo `U(ra_+)ξ=ξ`; o mesmo vale para `a_-`. Assim os dois geradores nulos anulam `ξ` no sentido espectral, e portanto `P⁰ξ=0`. Pela condição espectral `\bar V_+∩{p⁰=0}={0}`, `ξ` é invariante por todas as translações. Unicidade do vácuo implica `ξ=cΩ`. Finalmente `(x-c1)Ω=0` e, como `Ω` é separador, `x=c1`. Logo `M_Ω=ℂ1`. ∎

**Referência primária específica pendente.** Não localizei, com teorema e página, uma fonte primária de Minkowski que enuncie precisamente “a ergodicidade da cunha” nesta forma. A prova acima está completa sob as hipóteses declaradas e não depende da referência pendente. O argumento é de tipo Borchers–Mautner; Speranza, 2025, arXiv:2504.07630 §4 registra a conclusão como exemplo, sem fornecer essa prova. [KNOWN, a conferir]. [Speranza 2025](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2504.07630v1&text=there%20also%20exist%20ergodic%20states%20with%20trivial%20centralizer%2C%20such%20as%20the%20Minkowski%20vacuum%20for%20a%20Rindler%20wedge "citation")

**Limite físico.** Esta prova trata da cunha de Minkowski. Transportá-la à álgebra de horizonte da TGL é exatamente `H_TGL-horizon` e permanece `[OPEN]`.

## 8. Caixa pronta para o artigo

> **TEOREMA T1 CONDICIONADO.** Sejam `M̂=M⋊_{σ^φ}ℝ`, `τ` seu traço canônico, `β>0` e `Φ_t=∫Ad(e^{is√K̂})dN(0,βt)(s)`. Suponha **H_K̂** (`K̂=F(ĥ)≥0` afiliado a `L(ℝ)` e `F` essencialmente injetiva), **H_erg** (`M_φ=ℂ1`) e, para a aplicação à TGL, **H_TGL-horizon [OPEN]**. Então, para cada `t>0`,
>
> `Fix_{M̂}(Φ_t)={u_s:s∈ℝ}′∩M̂=L(ℝ)=W*(√K̂)=W*(K̂)`.
>
> Existe uma única expectativa condicional normal `E_τ:M̂→L(ℝ)` com `τ∘E_τ=τ`, e `Φ_t(x)→E_τ(x)` σ-fracamente para todo `x∈M̂`. Nos cantos `e_i`, a prova em `L²` usa o multiplicador `e^{-½βt(a-b)²}` e seu limite, o indicador da diagonal.

**O que entra por citação.** Digernes–Takesaki e a fatia de Tomita (Lema C); existência e normalização do traço canônico; Takesaki 1972 para `E_τ`; Choi 1974 apenas para a caracterização do domínio multiplicativo; Bisognano–Wichmann para a geometria modular da cunha.

**O que está provado aqui.** Lema A por família fiel e suporte total; Lema C a partir das duas entradas citadas; a análise de H_K̂ e da paridade; os cantos e toda a passagem `L²→L¹→σ-fraca`; o argumento de Borchers–Mautner para `M_Ω=ℂ1`; a montagem do teorema.

**O que permanece hipótese/aberto.** A definição física de `F` e H_K̂; H_TGL-horizon; a fórmula para `F` não injetiva arbitrária; uma referência primária específica, com teorema/página, para a formulação usual da ergodicidade da cunha. III₁ sozinho não é invocado como centralizador trivial.

## 9. Face finita Lean — substituição do alvo antigo

**Enunciado formalizado `[REAL no sandbox]`.** Em `M_n(ℂ)`, numa base espectral com `K=diag(k_i)` e `k_i≥0`, defina

`Φ_t(x)_{ij}=e^{-βt(√k_i-√k_j)²/2}x_{ij}`.

Para `β>0` e `t>0`, `Φ_t(x)=x` se e somente se `Kx=xK`; quando `t→∞`, `Φ_t(x)` converge ao pinching que conserva `x_{ij}` quando `k_i=k_j` e zera as demais entradas. Também são provados `K` hermitiana/positiva, a fórmula exata do multiplicador e a idempotência do pinching.

Nomes principais: `gaussianFlow_entry_formula`, `diagonalK_isHermitian`, `diagonalK_posSemidef`, `fixed_gaussianFlow_iff`, `fixed_gaussianFlow_iff_pinching`, `tendsto_gaussianFlow`, `pinching_idem`.

**Espectro simples `[DERIVED, ainda não formalizado]`.** Em dimensão finita, `Fix={K}′=W*(K)` se e somente se `K` tem espectro simples. Se todos os `k_i` são distintos, o comutante é diagonal e interpolação polinomial produz toda matriz diagonal a partir de `K`. Se `k_i=k_j` para `i≠j`, `W*(K)` permanece diagonal nessa base, mas o comutante contém a matriz unitária fora da diagonal `E_{ij}`. Esse bicondicional não foi incluído como teorema Lean; nenhuma hipótese oca foi usada para supri-lo.

**Escopo deliberado.** A candidata trabalha na base espectral diagonal. A embalagem unitariamente covariante para um `K` hermitiano arbitrário e o bicondicional de espectro simples ficam fora do termo Lean atual. Isso não afeta os teoremas finitos efetivamente compilados nem se apresenta como prova do caso contínuo.

**Arquivos e compilação `[REAL]`.**

- Candidata: `K05/candidatas/T1_R2.lean`.
- Cópia compilada: `K05/sandbox_t1/sources/T1_R2.lean`.
- Objeto: `K05/sandbox_t1/build/T1_R2.olean`.
- Script: `K05/sandbox_t1/compilar_t1.sh`.
- Log: `K05/sandbox_t1/logs/T1_R2.log`.
- Auditoria independente de consistência: `K05/sandbox_t1/logs/T1_R2_audit.log`.

O comando registra Lean `4.31.0`, commit `68218e876d2a38b1985b8590fff244a83c321783`, e `RC: 0`. Os 11 registros `#print axioms` finais contêm somente `propext`, `Classical.choice` e `Quot.sound`. Busca na fonte não encontra `sorry`, `admit`, declaração `axiom` ou `sorryAx`; restam apenas avisos de estilo/linter. A auditoria confirma candidata=cópia compilada, objeto presente e `RC: 0`. Não houve `lake` nem build do kernel canônico.

## 10. Fechado × aberto

**Fechado.** Comutante relativo geral; equivalência masa↔centralizador trivial; setor fixo sob H_K̂ e bicondicional `Fix=W*(K̂)↔M_φ=ℂ1`; paridade sob H_paridade; família fiel invariante explícita; semifinitude sob afiliação a `L(ℝ)`; expectativa e convergência σ-fraca; ergodicidade da cunha por prova própria sob BW/espectro/vácuo; face finita gaussiana compilada.

**Aberto.** H_TGL-horizon; escolha física de `F`; F não injetiva arbitrária; referência primária específica da ergodicidade da cunha com teorema/página; embalagem Lean para `K` não diagonal e formalização do bicondicional de espectro simples.
