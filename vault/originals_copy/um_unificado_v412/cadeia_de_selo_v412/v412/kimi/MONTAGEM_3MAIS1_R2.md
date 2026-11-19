# K05 — Montagem 3+1, rodada 2: o caso (4,0) identificado; (1,3) continua (H)

## 0. Veredito e limites

**[DERIVED + KNOWN, a conferir]** A montagem euclidiana de quatro triplas canônicas do círculo é unitariamente equivalente, com `J`, orientação e estrutura spin produto/trivial explícitos, à tripla de Dirac do toro plano `T⁴`. Assim, finitude/continuidade absoluta e dualidade de Poincaré fecham no caso comutativo, **sem** atribuir a Dąbrowski–Dossena §5 dois axiomas que essa seção não trata.

**[INPUT (H)/OPEN]** A assinatura `(1,3)` tem moldura publicada para a análise de Krein e para os sinais/dimensões mod 8, mas não para toda a lista de axiomas nem para a reconstrução. Ela continua **(H) COM MOLDURA PUBLICADA PARA DEFINIÇÃO/SINAIS**, não “sabida”.

**[DECLARADO — etiqueta da casa]** Todas as referências bibliográficas abaixo ficam marcadas `[KNOWN, a conferir]` e foram efetivamente consultadas no escopo indicado nesta rodada; a conferência distinta continua necessária. Nenhuma candidata Lean nova é necessária.

Fontes do artigo: a tripla escalada e a montagem aparecem nas linhas 1922–1932; `ax:lorentz`, já marcado ABERTO, está nas linhas 523–530. [A Ponte Einstein Cartan Miguel](kimi-cite://md-line?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2FA%20Ponte%20Einstein%20Cartan%20Miguel.tex&line=1922 "citation"), [A Ponte Einstein Cartan Miguel](kimi-cite://md-line?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2FA%20Ponte%20Einstein%20Cartan%20Miguel.tex&line=523 "citation")

## 1. Aferição local antes de qualquer alegação de ausência

**[REAL — consultas executadas em 13/11/2026]**

- `rotas.py consultar "montagem 3+1 produto triplas espectrais KO dimensao"`: 0 rota; 2056 registros, cabeça `03042aca2e30e8cf`. Não há rota pronta a reabrir.
- O índice do acervo foi consultado por `tripla espectral|spectral triple|KO.dimens|Gromov.Hausdorff|Rieffel|Suijlekom|Hekkelman|Kaad|Kyed`; a saída ampla excedeu 120 s e foi interrompida. Ela não é usada como prova de ausência.
- Inventário da bancada: aparecem módulos modulares/Takesaki, mas nenhum módulo de produto de triplas, GH quântico ou convergência métrica que feche esta montagem.
- Kernel canônico, só leitura: nenhuma ocorrência geométrica de `SpectralTriple`, `TriplaEspectral`, `KO.dim`, `Gromov`, `Rieffel`, `qGH` ou `ghDist` no recorte `.lean` consultado. Nada foi compilado ou alterado.
- Atlas, §IX e os verbetes `ACHADO 08`, `Face C` e `Takesaki (produto cruzado)`: o Atlas conserva a ausência de traço em III₁ e o estatuto condicional; não fornece a montagem explícita nem uma ponte GH.

Classificação: a identificação algébrica e as fórmulas são **SABIDO POR REFERÊNCIA + DERIVED aqui**; uma formalização Lean da geometria está **AUSENTE no recorte efetivamente consultado**. Não se conclui ausência universal a partir da busca interrompida do índice.

## 2. Correção AO LADO do rótulo anterior

O texto anterior de `MONTAGEM_3MAIS1.md`, §6, passo 4, dizia:

> “`T³×S¹`: par×ímpar; resultado par, métrica 4, KO 4.”

**Esse rótulo está errado e permanece citado acima, sem apagá-lo.** A correção é:

> **`T³×S¹` é ÍMPAR×ÍMPAR, com duplicação auxiliar `ℂ²`; o resultado é par, de dimensão métrica 4 e KO-dimensão 4.**

A sequência correta é:

| etapa | paridade da operação | resultado |
|---|---|---|
| `S¹×S¹` | ímpar×ímpar, duplicação | par, KO 2 |
| `T²×S¹` | par×ímpar | ímpar, KO 3 |
| `T³×S¹` | **ímpar×ímpar, duplicação** | **par, KO 4** |

Em KO 4, `(ε,ε′,ε″)=(−1,+,+)`. Os sinais foram conferidos por matrizes gama na revisão independente e também pela realização explícita da §3 abaixo. A dimensão do fibrado de espinores é `2·1·2=4`: já estava correta; o erro era somente a paridade atribuída ao último produto. D–D §4.3 contém a duplicação ímpar×ímpar; §5 não contém finitude nem Poincaré. [Dąbrowski–Dossena 2011, arXiv:1011.4456, KNOWN, a conferir](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F1011.4456 "citation")

## 3. Identificação explícita: quatro círculos = toro spin trivial `T⁴`

### 3.1 Entrada e convenções

Seja `λ=β_TGL^(−1/2)>0`, e para cada coordenada `x_j` em `S¹=R/2πZ`,

`T_j=(C∞(S¹), L²(S¹), D_j),   D_j=−iλ d/dx_j,   J_j=K`,

onde `K` é a conjugação complexa. A tripla tem `c_1=U^(−1)⊗U`, `U(x)=e^(ix)`, com normalização `c_{1,λ}=λ^(−1)c_1`, de modo que `π_{D_j}(c_{1,λ})=1`. Cada fibrado spinor é o trivial `S¹×ℂ`; a estrutura spin produto é, portanto, a trivial.

### 3.2 As duas duplicações e o Dirac resultante

Use a construção D–D:

- ímpar×ímpar: `H=(H_1⊗H_2)⊗ℂ²`, `D=D_1⊗1⊗σ_1+1⊗D_2⊗σ_2`, `χ=1⊗1⊗σ_3`;
- par×ímpar: `D=D_par⊗1+χ_par⊗D_ímpar`;
- em cada ímpar×ímpar escolha-se o sinal `M_+` da Tabela 6 de D–D, compatível com a seleção de Connes.

Após `S¹×S¹`, o operador intermediário em `T³` é simplesmente `-iλ∑_{j=1}³ σ_j ∂_j`. A última duplicação dá, em `L²(T⁴)⊗ℂ²_a⊗ℂ²_τ`,

`D_λ^(prod)=−iλ[σ_1^a⊗τ_1 ∂_1 + σ_2^a⊗τ_1 ∂_2 + σ_3^a⊗τ_1 ∂_3 + 1^a⊗τ_2 ∂_4]`,

`χ_λ^(prod)=1^a⊗τ_3`,

`J_λ^(prod)=(σ_2^a⊗1_τ)K_(4,a,τ)`,

onde `K_(4,a,τ)` conjuga tanto as funções como os dois fatores auxiliares. A álgebra é `C∞(T⁴)`, por multiplicação, trivial nos fatores auxiliares.

Defina `U_4` como a unitária de Fourier/base constante que identifica esse espaço com `L²(T⁴,ℂ⁴)`. Nas fórmulas acima ela é literalmente a identificação de bases, não uma equivalência existencial. Então:

1. as quatro matrizes `Γ_1=σ_1⊗τ_1`, `Γ_2=σ_2⊗τ_1`, `Γ_3=σ_3⊗τ_1`, `Γ_4=1⊗τ_2` são autoadjointas, têm quadrado `1` e anticomutam;
2. `U_4 D_λ^(prod) U_4* = −iλ∑ Γ_j∂_j = D_{T⁴,λ}`, o Dirac plano autoadjunto;
3. `χ=−Γ_1Γ_2Γ_3Γ_4`, a quiralidade de volume na convenção autoadjunta;
4. `U_4 J^(prod)U_4* = J_{T⁴}` é a conjugação de carga do spin trivial;
5. cálculo direto dá `J²=−1`, `JD=DJ`, `Jχ=χJ`, exatamente KO 4.

A trivialidade dos dois frames constantes `σ` e `τ` mostra que a estrutura spin é a **produto/trivial**, não uma estrutura exótica de `T⁴`. D–D §2.4 fornece a decomposição do Dirac em produtos cartesianos e §6 recomenda precisamente o toro plano com spin trivial e condições periódicas. [Dąbrowski–Dossena 2011, arXiv:1011.4456, KNOWN, a conferir](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F1011.4456 "citation")

### 3.3 Orientação: o ciclo também coincide

Sejam `U_j(x_j)=e^(ix_j)` e `c_{1,λ}^j=λ^(−1)U_j^(−1)⊗U_j`. Tome o shuffle iterado de D–D,

`c_(4,λ)=−(1/18) ×_{j=1}⁴ c_{1,λ}^j`.

A constante resulta das normalizações sucessivas `r_2=i`, `r_3=3`, `r_4=6i` de D–D (35)–(36). Pela fórmula de orientação de D–D §5, e sem usá-la para finitude/Poincaré,

`π_{D_λ}(c_(4,λ))=χ_λ^(prod)`.

Depois de `U_4`, este é o ciclo de volume do toro plano, com a orientação fixada pela ordem `dx_1∧dx_2∧dx_3∧dx_4`. Logo a equivalência unitária transporta **Dirac, realidade, quiralidade e orientação**, não apenas os espaços de Hilbert.

## 4. Finitude e dualidade de Poincaré no caso comutativo

**Estatuto dos sete itens [DERIVED a partir da identificação + KNOWN, a conferir]:**

| axioma | fecho para `T⁴` |
|---|---|
| dimensão/somabilidade | Autovalores de `D_λ²`: `λ²‖k‖²`, `k∈Z⁴`. A lei de Weyl dá dimensão 4; a duplicação altera multiplicidades, não a dimensão. |
| regularidade | `Dom(D_λ^m)=Dom(D_1^m)` e `δ_|D_λ|=λδ_|D_1|`; o domínio suave é `C∞(T⁴)⊗ℂ⁴`. |
| realidade e primeira ordem | As fórmulas explícitas de `J` valem; `Jb*J` age à direita e comuta com funções e comutadores. |
| orientação | O ciclo shuffle explícito da §3.3 realiza a quiralidade de volume. |
| **finitude/continuidade absoluta** | `H∞=C∞(T⁴)⊗ℂ⁴=C∞(T⁴)^4` é **livre de posto 4**, logo finito projetivo. A medida de Lebesgue e a lei de Weyl dão a continuidade absoluta; a estrutura hermitiana pode ser escolhida com a normalização da §5. |
| **dualidade de Poincaré** | O Dirac do spin trivial é a classe fundamental de K-homologia de `T⁴`. Por Künneth, `K⁰(C(T⁴))` e `K¹(C(T⁴))` são livres de posto 8 e o emparelhamento de interseção com essa classe é unimodular; o produto de cap é o isomorfismo de Poincaré. |
| equivalência | Todos os dados são transportados por `U_4`, inclusive o módulo livre e a classe de Fredholm. |

Connes 1996 formula finitude como Axioma 5 e Poincaré como Axioma 6, e também apresenta a tripla spin como o caso geométrico; Gracia-Bondía–Várilly–Figueroa 2001 sistematiza a tripla comutativa e o teorema de variedade spin. Estas fontes sustentam o **caso comutativo identificado**, não um teorema geral de preservação por produtos arbitrários. [Connes 1996, hep-th/9603053, KNOWN, a conferir](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2Fhep-th%2F9603053 "citation"), [Gracia-Bondía–Várilly–Figueroa 2001, DOI 10.1007/978-1-4612-0005-5, KNOWN, a conferir](kimi-cite://web?url=https%3A%2F%2Fdoi.org%2F10.1007%2F978-1-4612-0005-5 "citation")

## 5. O que muda ao multiplicar `D` por `λ=β^(−1/2)`?

**Resposta curta [DERIVED]: nenhum axioma é destruído, desde que orientação e a normalização hermitiana sejam reescaladas; a distância muda por `λ^(−1)=β^(1/2)`.**

| objeto | efeito exato de `D_λ=λD_1` | veredito |
|---|---|---|
| distância de Connes | `[D_λ,a]=λ[D_1,a]`, logo `d_λ=λ^(−1)d_1=β^(1/2)d_1`; a métrica riemanniana escala por `λ^(−2)=β`. | **muda**, mas de forma controlada |
| dimensão/somabilidade | valores singulares de `|D_λ|^(−1)` são `λ^(−1)` vezes os anteriores; a integral de Dixmier em dimensão 4 escala por `λ^(−4)=β²`. | preservado |
| regularidade | domínios inalterados; derivações escalam por `λ`. | preservado |
| `J` e primeira ordem | `λ` é real escalar; os sinais KO 4 e os comutadores não mudam. | preservado |
| orientação | `π_{D_λ}(c_4)=λ⁴π_{D_1}(c_4)=λ⁴χ`; deve-se usar `c_(4,λ)=λ^(−4)c_4=β²c_4`. | **preservado somente com o ciclo reescalado** |
| finitude | `H∞` e o posto livre não mudam. Para manter `⟨aξ,η⟩=∫a(ξ,η)ds_λ⁴`, pode-se tomar `(ξ,η)_λ=λ⁴(ξ,η)_1`. | preservado; normalização explícita |
| Poincaré | fora do núcleo, `D_λ|D_λ|^(−1)=D_1|D_1|^(−1)`; a fase e a classe de K-homologia são as mesmas (também por homotopia `t↦λ_tD_1`). | preservado |

Portanto, seria incorreto tanto dizer “a distância não muda” como dizer “a orientação vale com exatamente o mesmo ciclo sem reescala”.

## 6. Assinatura (1,3): o que as fontes realmente cobrem

### 6.1 van den Dungen

A Definição 2.2 de tripla de Krein par exige dados de Krein, simetria fundamental, domínio denso, Krein-autoadjointness, comutadores limitados e compacidade de `π(a)ι`. É uma definição **analítica**. O produto construído na Definição 4.2/Proposição 4.3 é `F×M`, com `F` finito e `M` pseudo-Riemanniana spin, não um produto geral de quatro fatores. A Obs. 6.4 registra a falta de uma K-homologia de Krein. Não há, nessa referência, os axiomas de finitude, orientação e Poincaré nem o fecho lorentziano pedido. [van den Dungen 2016, arXiv:1505.01939, DOI 10.1007/s11040-016-9207-z, KNOWN, a conferir](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F1505.01939v2 "citation")

### 6.2 Bizi–Brouder–Besnard

O par `(m,n)` de dimensões de espaço/tempo é aditivo mod 8 sob produto tensorial graduado. A Tabela 3 dá `(t,s)=(1,3)` quando `n=6`, `m=4`; na convenção West coast, `n=p−q=1−3=−2≡6 (mod 8)`. O produto de triplas indefinidas é tratado no caso **par**, e a extensão ao caso ímpar é declarada difícil. Isso fornece sinais e contabilidade, não os sete axiomas nem reconstrução. [Bizi–Brouder–Besnard 2018, arXiv:1611.07062, J. Math. Phys. 59, 062303, DOI 10.1063/1.5010424, KNOWN, a conferir](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F1611.07062v2 "citation")

### 6.3 Estatuto resultante

> **(H) COM MOLDURA PUBLICADA para (i) definição analítica de Krein e (ii) sinais/dimensões mod 8; o restante de (H) continua [OPEN].**

KO 4 euclidiano não se transforma em assinatura lorentziana; `(1,3)↔(m,n)=(4,6)` também não prova que o produto concreto do artigo satisfaça os axiomas restantes.

## 7. LISTA mínima de axiomas que `ax:lorentz` deve nomear

A lista abaixo separa origem e estatuto. `𝒥` denota a simetria fundamental de Krein e `J` a realidade de Connes; confundi-las invalida a contabilidade.

| item que o artigo deve nomear | origem efetivamente consultada | o que fica OPEN para a montagem (1,3) |
|---|---|---|
| **L1. Dados de Krein e análise** | van den Dungen, Def. 2.2: `H`, `𝒥`, grading, `D` fechado/Krein-autoadjointo, domínio e comutadores limitados, compacidade de `π(a)ι`. | Escolha explícita de `𝒥`, domínios e compacidade para o produto concreto. |
| **L2. Dimensão espectral 4 e somabilidade** | Connes 1996, Axioma 1, como molde; van den Dungen fornece apenas a compacidade analítica. | Definir a noção indefinida de dimensão/somabilidade e provar que vale 4. |
| **L3. Regularidade** | Connes 1996, Axioma 3; os requisitos de domínio de van den Dungen. | Forma lorentziana de `δ_|D|`/domínios e sua preservação pelo produto. |
| **L4. Realidade e sinais, incluindo ordem zero** | Connes 1996, Axioma 7′; BBB 2018 para `(m,n)` e os sinais de `J`, `χ`, `𝒥`. | Compatibilidade completa com a realidade escolhida e ordem zero no produto. |
| **L5. Primeira ordem** | Connes 1996, Axioma 2′: `[[D,a],Jb*J⁻¹]=0`; van den Dungen §3, eq. (1), oferece uma versão de ordem um. | A condição e sua preservação em `(1,3)`; **omitida em `ax:lorentz`**. |
| **L6. Orientação e quiralidade** | Connes 1996, Axioma 4′: ciclo de Hochschild realizando `χ`; D–D §5 só no caso euclidiano. | Ciclo indefinido, normalização e prova de que realiza a quiralidade. |
| **L7. Finitude e continuidade absoluta** | Connes 1996, Axioma 5: `H∞` finito projetivo e estrutura hermitiana compatível. | Módulo e forma indefinida apropriados; **omitida em `ax:lorentz`**. |
| **L8. Dualidade de Poincaré** | Connes 1996, Axioma 6′: isomorfismo por cap com a classe fundamental; van den Dungen Obs. 6.4 adverte que não há K-homologia de Krein pronta. | Formular a dualidade sem uma K-homologia de Krein disponível e prová-la; **omitida em `ax:lorentz`**. |
| **L9. Causalidade e orientação temporal** | O próprio `ax:lorentz`, linhas 523–530, via `Π_irr`; é dado adicional, não consequência de KO. | Provar que `Π_irr` define a causalidade pretendida e recuperar a métrica além do fator conforme sem circularidade. |
| **L10. Reconstrução e regra de produto** | Connes 1996/GVF 2001 no caso riemanniano; van den Dungen só `F×M`; BBB só sinais e caso par. | Equivalência unitária com uma variedade `(1,3)` e o teorema de produto para L1–L9. |

**[OPEN]** Não se afirma que L1–L10 seja uma axiomatização lorentziana completa aceita. É a lista mínima que a hipótese do artigo precisa tornar explícita para que a seta de reconstrução tenha conteúdo verificável. Os bloqueios centrais são L5–L8, a K-homologia de Krein, a orientação e a regra de produto; não apenas a causalidade já mencionada por `ax:lorentz`.

## 8. Texto curto pronto para substituir a alegação, sem alterar o artigo nesta rodada

> **(4,0) [DERIVED + KNOWN].** O produto de quatro triplas canônicas do círculo, com as duplicações ímpar×ímpar e as escolhas de realidade de D–D, é unitariamente equivalente à tripla de Dirac do toro plano `T⁴` com estrutura spin produto/trivial, inclusive `J`, quiralidade e ciclo de volume. O módulo suave é livre de posto 4 e a classe de Dirac realiza Poincaré. Assim, finitude e dualidade de Poincaré seguem no caso comutativo, não de D–D §5. Se `D↦λD`, então `d↦λ⁻¹d`, `J` e Poincaré não mudam, e a orientação se preserva usando `c↦λ⁻⁴c`.
>
> **(1,3) [INPUT (H)/OPEN].** Existe moldura publicada para a análise de Krein e para os sinais mod 8. Permanece como hipótese a existência de uma realização que satisfaça a lista L1–L10, incluindo primeira ordem, finitude e Poincaré, e a regra de produto correspondente.

## 9. Referências consultadas

- Ludwik Dąbrowski e Giacomo Dossena (2011), *Product of real spectral triples*, IJGMMP 8, 1833–1848, DOI `10.1142/S021988781100597X`, arXiv:`1011.4456`, §§2.4, 4.3, 5, 6. **[KNOWN, a conferir]** [arXiv](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F1011.4456 "citation")
- Alain Connes (1996), *Gravity coupled with matter and the foundation of non commutative geometry*, CMP 182, 155–176, arXiv:`hep-th/9603053`, axiomas 1–7 e 1′–7′. **[KNOWN, a conferir]** [arXiv](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2Fhep-th%2F9603053 "citation")
- José M. Gracia-Bondía, Joseph C. Várilly e Héctor Figueroa (2001), *Elements of Noncommutative Geometry*, Birkhäuser, DOI `10.1007/978-1-4612-0005-5`, capítulos *Spectral Triples* e *Connes’ Spin Manifold Theorem*; ficha e sumário editorial consultados. **[KNOWN, a conferir]** [Springer](kimi-cite://web?url=https%3A%2F%2Fdoi.org%2F10.1007%2F978-1-4612-0005-5 "citation")
- Koen van den Dungen (2016), *Krein spectral triples and the fermionic action*, Math. Phys. Anal. Geom. 19, art. 4, DOI `10.1007/s11040-016-9207-z`, arXiv:`1505.01939`, Def. 2.2, §3, Def. 4.2, Prop. 4.3, Obs. 6.4. **[KNOWN, a conferir]** [arXiv](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F1505.01939v2 "citation")
- Nadir Bizi, Christian Brouder e Fabien Besnard (2018), *Space and time dimensions of algebras with applications to Lorentzian noncommutative geometry and quantum electrodynamics*, J. Math. Phys. 59, 062303, DOI `10.1063/1.5010424`, arXiv:`1611.07062`, Tabela 3 e §§3, 5. **[KNOWN, a conferir]** [arXiv](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F1611.07062v2 "citation")

**Bloqueio restante:** nenhum para `(4,0)` no nível desta ordem; para `(1,3)`, a definição e verificação de L5–L8, a K-homologia de Krein e a regra de produto continuam abertas.
