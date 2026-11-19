# K05 — GH para III₁, rodada 2: correção clássica e o menor degrau II∞

## 0. Veredito

**[CONJECTURE]** A extensão GH a III₁ permanece conjectura. Em III₁ a formulação deve usar uma **tripla torcida** e uma candidata a Lip-norma cuja topologia fraca-* precisa ser demonstrada; o produto cruzado II∞ fornece um traço, mas não fornece automaticamente Lip-norma, mapas `C¹`, compacticidade dos espaços de estados normais nem descida métrica.

**Correção material ao Fecho 3 [KNOWN, a conferir].** Rieffel não publica `qGH=GH` no caso comutativo. Publica `dist_q≤dist_GH` (Prop. 4.7) e um contraexemplo à igualdade (Apêndice 1). A correção decorre de Rieffel, **não** de Kaad–Kyed.

**Menor degrau [DERIVED + KNOWN, a conferir].** No andar II∞, a compressão espectral é positiva, unital e `C¹`-contrativa; se forem acrescentadas as aproximações de ordem e as compatibilidades topológicas exigidas por van Suijlekom, segue GH-S com uma estimativa explícita. A quebra exata está em produzir os mapas inversos aproximados e topologias e, depois, em descer por Takesaki: a dualidade é algébrica e escala o traço, não uma isometria de Lip-normas.

**Lean.** Nenhuma candidata nova. A antiga `K02/candidatas/GH_III1.lean` fica arquivada por referência como oca, sem edição; ver `K05/MONTAGEM_GH/ARQUIVO_GH_III1_OCA.md`.

Fontes do artigo: a conjectura III₁ está nas linhas 1821–1826 e 2250–2254; a afirmação clássica a corrigir está nas linhas 1934–1942. [A Ponte Einstein Cartan Miguel](kimi-cite://md-line?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2FA%20Ponte%20Einstein%20Cartan%20Miguel.tex&line=1821 "citation"), [A Ponte Einstein Cartan Miguel](kimi-cite://md-line?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2FA%20Ponte%20Einstein%20Cartan%20Miguel.tex&line=1934 "citation")

## 1. Aferição local antes de alegar ausência

**[REAL — consultas executadas em 13/11/2026]**

- `rotas.py consultar "Gromov Hausdorff III1 truncamento espectral Rieffel Connes van Suijlekom"` e `consultar "Takesaki dualidade truncamento convergencia estado"`: ambas 0; 2056 registros, cabeça `03042aca2e30e8cf`.
- O índice do acervo foi consultado pelo regex amplo contendo triplas, GH, Rieffel, van Suijlekom, Hekkelman, Kaad e Kyed; a saída excedeu 120 s e foi interrompida. Não se converte essa saída parcial em prova de ausência.
- Inventário: há peças modulares/Takesaki, mas nenhum módulo localizado que prove qGH/III₁ ou transporte convergência métrica por dualidade.
- Kernel canônico, só leitura: nenhuma ocorrência geométrica de `Gromov`, `Rieffel`, `qGH`, `ghDist` ou `SpectralTriple` no recorte consultado. Não se rodou `lake`, não se alterou o kernel.
- Atlas, §IX, `ACHADO 08`, `Face C` e `Takesaki (produto cruzado)`: III₁ não tem estado tracial; o produto cruzado tem `Tr∘θ_s=e^(−s)Tr`; nenhum teorema de descida GH está catalogado.

Classificação: os teoremas de truncamento comutativo e a dualidade são **SABIDO POR REFERÊNCIA**; a Lip-norma/topologia III₁, os mapas `C¹` e a descida métrica continuam **[OPEN]**. A antiga tipagem Lean não preenche nenhum desses itens.

## 2. Formulação correta dos dois alvos e da conjectura

### 2.1 Tripla torcida, não a fórmula não torcida importada de II₁

Connes–Moscovici mostra que exemplos tipo III entram por uma torção. Na convenção usada aqui, os dados são `(A,H,D,σ)`, com `σ∈Aut(A)`, e o comutador torcido

`d_σ(a)=D a−σ(a)D`,   `L_σ(a)=‖d_σ(a)‖`.

A torção exata e o sinal devem ser fixados pelo artigo; em exemplos modulares ela está ligada ao peso. Chamar simplesmente `‖[D,a]‖` de Lip-norma III₁ sem especificar a torção repete a obstrução que a referência evita. [Connes–Moscovici 2008, arXiv:math/0609703, KNOWN, a conferir](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2Fmath%2F0609703 "citation")

Seja `M` o fechamento de von Neumann, um fator III₁. Para que `(A,L_σ)` seja espaço métrico quântico compacto, ainda é preciso provar: densidade de `Dom L_σ`, invariância por `*` ou uma variante declarada, núcleo `ℂ1`, finitude de `d_σ` entre estados e, sobretudo, **igualdade entre a topologia `d_σ` e a fraca-*** em `S(A)`. Leibniz/quasi-Leibniz deve ser exigido separadamente para a versão qGH escolhida. Nenhuma dessas propriedades segue apenas de `M` ser III₁.

### 2.2 As duas distâncias

Para projeções espectrais `P_M→1` fortemente, `E_M=P_M A P_M`, `D_M=P_MDP_M` e seminormas induzidas:

- **GH-R:** `dist_Q((E_M,L_M),(A,L_σ))→0`, com `dist_Q` de Rieffel e Lip-normas verificadas;
- **GH-S:** `d_GH((S(E_M),d_M),(S(A),d_σ))→0`, a GH clássica dos espaços métricos compactos de estados.

Se forem usados apenas **estados normais**, escreve-se GH-Sₙ. Esse é um terceiro enunciado, não um detalhe: em geral `S_n(M)` não é fraco-* compacto, enquanto `S(A)` de uma C*-álgebra unital é compacto. O traço II∞ não elimina essa distinção.

**[CONJECTURE — versão tipada]** Com uma tripla torcida III₁ para a qual `L_σ` é Lip-norma, e com truncamentos que preservam todas as condições exigidas pela métrica escolhida, afirma-se GH-R e/ou GH-S. Não se afirma GH-Sₙ sem hipótese adicional. A III₁-idade e `P_M→1` não bastam.

## 3. O que está publicado — e o que cada fonte não decide

| fonte | conteúdo utilizável | limite que o artigo deve preservar |
|---|---|---|
| **Rieffel 2004** | Compact quantum metric spaces, qGH, pontes; exemplo principal de toros quânticos. Prop. 4.7: `dist_q≤dist_GH` para espaços clássicos. | Não é teorema universal de truncamentos III₁ nem de igualdade clássica. |
| **Connes–van Suijlekom 2021** | Sistemas de operadores `PAP`, Toeplitz do círculo, estados e distância de Connes. | Moldura; não é o teorema III₁ nem, sozinho, a convergência. |
| **van Suijlekom 2021** | Teorema 5: `C¹`-aproximações + topologias fracas-* ⇒ GH-S. Proposição 13: o círculo de Toeplitz converge em GH-S. | Não é automaticamente GH-R; hipóteses `C¹` e topológicas são indispensáveis. |
| **Hekkelman 2022** | Os estados puros dos Toeplitz `n×n` convergem em GH para `S(C(S¹))` com as distâncias de Connes naturais. | O limite é o espaço de **todos** os estados de `C(S¹)`, não `S¹`/os estados puros clássicos; não é teorema III₁. |
| **Leimbach–van Suijlekom 2024** | Para toros de qualquer dimensão, os espaços de estados truncados convergem em GH-S para as medidas borelianas de probabilidade com Monge–Kantorovich; núcleo espectral de Fejér e multiplicadores de Schur/Fourier. | O núcleo e as estimativas são construções específicas do toro, não consequência de `P_M→1` ou de um traço abstrato. |
| **Connes–Moscovici 2008** | Triplas torcidas tipo III e caráter de Chern; comutadores torcidos limitados. | Não prova Lip-norma/topologia nem convergência GH. |
| **Kaad–Kyed 2023** | qGH de Rieffel e GH dos espaços de estados não são equivalentes; contraexemplos por bolas `ℓ^p` e sistemas de operadores comutativos de funções afins. | Não decide o caso `C(X)` clássico nem III₁; não é usado para apagar ou salvar a frase do artigo. |
| **Takesaki 1973; Connes–Takesaki 1977** | Núcleo contínuo II∞, traço, ação dual e bidualidade. | Não é teorema de convergência de truncamentos ou de descida de Lip-normas. |

Referências completas, com identificadores e a etiqueta da casa, estão na §10.

## 4. Correção AO LADO de “no caso comutativo, qGH = GH”

O artigo afirmava, nas linhas 1937–1939:

> “truncamentos espectrais de `S¹` convergem a `S¹` em distância de Gromov–Hausdorff quântica; e no caso comutativo, qGH = GH (Rieffel).”

**Esse texto anterior permanece citado; a correção é:**

1. **No caso clássico [KNOWN, a conferir].** Rieffel, Prop. 4.7, estabelece

   `dist_q((C(X),L_X),(C(Y),L_Y)) ≤ dist_GH(X,Y)`.

   Não estabelece igualdade. No Apêndice 1, Hanfeng Li apresenta `Y={0,1,2}` e `Z={0,3}` com as métricas usuais: `dist_GH(Y,Z)=1`, mas `dist_q(C(Y),C(Z))=1/2`. Logo a igualdade universal é falsa já no comutativo. [Rieffel 2004, arXiv:math/0011063, Prop. 4.7 e Ap. 1, KNOWN, a conferir](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2Fmath%2F0011063 "citation")
2. **No círculo [KNOWN, a conferir].** O teorema diretamente disponível é GH-S dos espaços de estados (van Suijlekom Prop. 13), reforçado por Hekkelman para os estados puros truncados. Se “qGH” no artigo significa qGH de Rieffel, é necessária uma ponte adicional; se significa GH dos espaços de estados, deve-se escrever GH-S para evitar ambiguidade.
3. **Kaad–Kyed.** O resultado confirma que GH-S e GH-R não são universalmente equivalentes, mas seus objetos não são `C(X)` clássicos. Ele não é a base da correção acima nem decide a identidade clássica; Rieffel já a havia decidido pela desigualdade e pelo exemplo.
4. **O que fica OPEN.** Uma prova GH-R específica para os truncamentos da casa, e qualquer identidade especial adicional, precisa ser citada separadamente. Não se declara aqui que GH-R do círculo seja impossível; apenas não se infla GH-S para GH-R.

## 5. O andar II∞: o que o traço compra e o que ele não compra

Seja `M` III₁ e `\widehat M=M⋊_σ R` seu núcleo contínuo, com traço normal fiel semifinito `τ` e ação dual `θ_s` tal que `τ∘θ_s=e^(−s)τ` (a convenção pode trocar o sinal). [Takesaki 1973, DOI 10.1007/BF02392041; Connes–Takesaki 1977, DOI 10.2748/tmj/1178240493, KNOWN, a conferir](kimi-cite://web?url=https%3A%2F%2Fdoi.org%2F10.1007%2FBF02392041 "citation"), [Connes–Takesaki 1977, KNOWN, a conferir](kimi-cite://web?url=https%3A%2F%2Fdoi.org%2F10.2748%2Ftmj%2F1178240493 "citation")

- `\widehat M` é unital como von Neumann algebra, mas em II∞ genuíno `τ(1)=∞`: não existe “estado traço normalizado” global.
- Projeções `e_i` de traço finito com `e_i↑1` permitem cantos finitos, mas escolher esses cantos não produz automaticamente um núcleo de Fejér nem compatibilidade entre os níveis `M`.
- `L¹(\widehat M,τ)` identifica o predual e ajuda na análise de estados normais; não torna `S_n(\widehat M)` fraco-* compacto nem prova que a distância de Connes metrize a fraca-*.
- A obstrução “sem traço em III₁” foi removida **somente no andar do núcleo**. Lip-norma, compacidade espectral, topologia e aproximações de ordem continuam como problemas independentes.

## 6. Os três lemas do menor degrau publicável

### Lema II∞-1 — Compressão espectral: o lado que fecha sem Fejér

**Estatuto: [DERIVED, elementar; a construção de sistemas de operadores é KNOWN, a conferir].**

Sejam `(E,H,D)` uma tripla de sistema de operadores, `E` denso numa C*-álgebra unital `A`, e `P_M` projeções espectrais de `D`, com `P_M→1` fortemente. Ponha `E_M=P_M E P_M`, `D_M=P_MDP_M` e `R_M(a)=P_MaP_M`. Então:

1. `R_M:E→E_M` é linear, positivo e unital;
2. `R_M` é contrativo em norma e na seminorma `L(a)=‖[D,a]‖`, pois `[D_M,R_M(a)]=P_M[D,a]P_M`;
3. para cada `a`, `R_M(a)→a` fortemente.

**Prova.** Positividade e unitalidade seguem de `R_M(a)=P_MaP_M` e `R_M(1)=P_M`. Como `P_M` comuta com `D`, a identidade de comutadores é imediata; contratividade segue de `‖P_M‖≤1`. Finalmente,

`P_MaP_M−a=P_Ma(P_M−1)+(P_M−1)a→0`

fortemente. ∎

**O que não segue.** Não há convergência uniforme nem uma inversa aproximada `S_M`, nem estimativas `‖S_MR_Ma−a‖≤γ_ML(a)` e `‖R_MS_MT−T‖≤γ′_ML_M(T)`. Muito menos GH-R/GH-S. Se `D` não tiver resolvente compacto, a própria premissa de tripla de sistema de operadores usada por van Suijlekom não está satisfeita. O traço de `\widehat M` não altera esta conta.

### Lema II∞-2 — Critério GH-S no núcleo, com estimativa e fronteira entre estados

**Estatuto: [KNOWN, a conferir, condicional; hipóteses para a TGL OPEN].**

Suponha que, além do Lema 1:

- `(E_M,H_M,D_M)` e `(E,H,D)` sejam triplas de sistemas de operadores cujas distâncias metrizem as topologias fracas-* de `S(E_M)` e `S(E)`;
- existam mapas positivos unitais `S_M:E_M→E`, `C¹`-contrativos, tais que `(R_M,S_M)` seja uma `C¹`-aproximação de isomorfismo de ordem, com constantes `γ_M,γ′_M→0`.

Então

`d_GH((S(E_M),d_M),(S(E),d)) ≤ γ_M+γ′_M → 0`.

**Prova.** A Proposição 4 de van Suijlekom dá as duas comparações bilaterais de distâncias com erros `2γ_M` e `2γ′_M`; o Teorema 5 limita a distorção da correspondência por `2γ_M+2γ′_M`, e `d_GH≤(1/2)dis`. ∎ [van Suijlekom 2021, arXiv:2005.08544, Prop. 4 e Teo. 5, KNOWN, a conferir](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2005.08544v2 "citation")

**Fronteira precisa.** O teorema é GH-S para os **espaços de estados usados em suas hipóteses**. Para GH-Sₙ, com somente estados normais, é necessário provar separadamente a compacticidade/cobertura e refazer as correspondências; não há aplicação automática. Para GH-R, exige-se uma ponte adicional. Este é o menor enunciado realmente sustentado pela literatura geral, e ele **não fecha** sem a construção de `S_M`, `γ_M`, `γ′_M` e as topologias.

### Lema II∞-3 — Takesaki: o que desce e a obstrução à descida ingênua

**Estatuto: [DERIVED para a obstrução; KNOWN, a conferir, para dualidade; descida métrica OPEN].**

**(a) O que desce.** A bidualidade dá um isomorfismo equivariante

`\widehat M⋊_θ R ≅ M⊗B(L²(R))`,

e os pontos fixos de `θ` em `\widehat M` são `π(M)`. Restrições de dados `θ`-equivariantes — representações, projeções, seminormas efetivamente invariantes — podem ser escritas nos pontos fixos. Se uma hipótese nomeada `H_Tak` fornecer mapas `R_M,S_M` equivariantes que já sejam `C¹`-aproximações nos sistemas de pontos fixos e as topologias exigidas, o Lema 2 aplica-se ali. Isso é uma implicação condicional explícita, não uma prova de `H_Tak`.

**(b) O que não desce.** `τ∘θ_s=e^(−s)τ` não é invariância métrica; a dualidade não afirma preservação de Lip-norma, de `C¹`-constantes, de qGH ou de GH-S. Em particular, não há uma esperança condicional normal fiel `E:\widehat M→π(M)` disponível para empurrar todos os estados normais para baixo.

**Prova da obstrução da esperança condicional.** Suponha que tal `E` exista. Então `μ=τ∘E` é um peso normal fiel semifinito em `π(M)`: elementos `y≥0` com `τ(y)<∞` são densos no sentido normal, suas imagens têm `μ(E(y))=τ(y)<∞`, e a fidelidade/normalidade de `E` dá aproximação de todo elemento positivo; `E` fixa `π(M)`. Além disso, para `x,y∈π(M)`,

`μ(xy)=τ(E(xy))=τ(xy)=τ(yx)=τ(E(yx))=μ(yx)`,

pois `τ` é tracial e `E` fixa os dois fatores. Logo `μ` é um traço normal fiel semifinito em `π(M)`, impossível para `M` III₁. A fidelidade de `E` segue de `x=E(x)` nesses pontos. Contradição. ∎

**Quebra exata.** A descida falha antes do cálculo GH: falta um mecanismo normal e fiel de extensão/restrição de estados e de preservação da métrica. A bidualidade, sozinha, entrega estabilização e pontos fixos, não essa ponte. Sem `H_Tak`, concluir III₁-GH a partir de II∞-GH seria modus ponens oco.

## 7. Possíveis contraexemplos — e seus alvos exatos

1. **Contraexemplo publicado à igualdade clássica [KNOWN, a conferir].** O par `Y={0,1,2}`, `Z={0,3}` de Rieffel/Li tem `dist_q=1/2<1=dist_GH`. Derruba `qGH=GH`, não a convergência GH-S do círculo.
2. **Contraexemplo publicado à ponte universal GH-S ⇒ GH-R [KNOWN, a conferir].** Kaad–Kyed constrói `p_n∈(1,2)`, `p_n→1`, e dimensões `N_n` para as quais a GH dos espaços de estados vai a 0, enquanto qGH fica `≥1/4`. Não é `C(X)` clássico nem III₁; é um contraexemplo à inferência universal, não à conjectura III₁ bem posta. [Kaad–Kyed 2023, arXiv:2212.10874, KNOWN, a conferir](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2212.10874v2 "citation")
3. **Candidata a contraexemplo à estratégia ingênua [DECLARADO/OPEN].** Uma grade com aliasing que enrola o modo `+M` em `−M`, como a lição de debug do artigo, pode impedir as estimativas `C¹` porque o comutador amplifica o termo de borda. Ela não é um contraexemplo construído à conjectura com Toeplitz e Lip-norma; é um teste que a demonstração precisa excluir explicitamente.
4. **O que continua sem contraexemplo construído [OPEN].** Não foi encontrada, nas fontes consultadas, uma tripla torcida III₁ com `L_σ` Lip-norma e truncamentos legítimos que falsifique GH-R ou GH-S. Essa ausência não é prova da conjectura.

## 8. Estatuto dos lemas e bloqueios em uma tabela

| enunciado | estatuto | o que falta |
|---|---|---|
| II∞-1: compressão positiva/unital/`C¹`-contrativa e convergência forte | **[DERIVED, fechado sob as hipóteses]** | Não produz inversa aproximada nem convergência uniforme. |
| II∞-2: `C¹` + topologias ⇒ GH-S com erro `γ+γ′` | **[KNOWN, a conferir, condicional]** | Construir `S_M`, erros e topologias; GH-Sₙ e GH-R exigem pontes novas. |
| II∞-3: restrição equivariante condicional; nenhuma esperança fiel normal para III₁ | **[DERIVED + KNOWN, a conferir; descida OPEN]** | `H_Tak`: dados equivariantes, métricos e de estados compatíveis, sem supri-los pela dualidade. |
| GH-III₁ geral | **[CONJECTURE]** | Torção, Lip-norma/topologia, `C¹`, escolha GH-R/GH-S e descida. |
| `qGH=GH` comutativo | **FALSO em geral [KNOWN, a conferir]** | Substituir por `qGH≤GH`; enunciados especiais precisam de prova própria. |

## 9. Arquivamento da candidata antiga

A fonte `K02/candidatas/GH_III1.lean` não foi alterada. O hash SHA-256 lido por script é `8b56968adeaeaeef6a373ed2f0ddd53ada78ced5aebec35f63a001df653e4a10`.

Diagnóstico preservado: `QuantumMetricSpace` não liga estados a elementos; `TypeIII1GHConjecture` tem predicados e `qghDist` livres; `typeIII1_of_named_hypothesis` apenas aplica `H_GH_III1 H_limit H_truncations`. É tipagem oca e modus ponens, não pedra de III₁. A nota de arquivamento está em `K05/MONTAGEM_GH/ARQUIVO_GH_III1_OCA.md`; nenhuma nova compilação é requerida para uma conjectura.

## 10. Referências efetivamente consultadas

- Marc A. Rieffel (2004), *Gromov–Hausdorff distance for quantum metric spaces*, Mem. AMS 168(796), 1–65, DOI `10.1090/memo/0796`, arXiv:`math/0011063`, especialmente Prop. 4.7 e Apêndice 1. **[KNOWN, a conferir]** [arXiv](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2Fmath%2F0011063 "citation")
- Alain Connes e Walter D. van Suijlekom (2021), *Spectral truncations in noncommutative geometry and operator systems*, CMP 383, 2021–2067, DOI `10.1007/s00220-020-03825-x`, arXiv:`2004.14115`. **[KNOWN, a conferir]** [arXiv](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2004.14115 "citation")
- Walter D. van Suijlekom (2021), *Gromov–Hausdorff convergence of state spaces for spectral truncations*, J. Geom. Phys. 162, 104075, DOI `10.1016/j.geomphys.2020.104075`, arXiv:`2005.08544`, Prop. 4, Teo. 5, Prop. 13. **[KNOWN, a conferir]** [arXiv](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2005.08544v2 "citation")
- Eva-Maria Hekkelman (2022), *Truncated geometry on the circle*, Lett. Math. Phys. 112, art. 20, DOI `10.1007/s11005-022-01514-5`, arXiv:`2111.13865`, resumo e §§2–4. **[KNOWN, a conferir]** [arXiv](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2111.13865v2 "citation")
- Malte Leimbach e Walter D. van Suijlekom (2024), *Gromov–Hausdorff convergence of spectral truncations for tori*, Adv. Math. 439, 109496, DOI `10.1016/j.aim.2024.109496`, arXiv:`2302.07877`, especialmente §§1–3. **[KNOWN, a conferir]** [arXiv](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2302.07877v2 "citation")
- Alain Connes e Henri Moscovici (2008), *Type III and spectral triples*, em *Traces in Number Theory, Geometry and Quantum Fields*, Aspects Math. E38, 57–71, arXiv:`math/0609703`, especialmente torção e §§2–3. **[KNOWN, a conferir]** [arXiv](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2Fmath%2F0609703 "citation"), [texto no site do autor](kimi-cite://web?url=https%3A%2F%2Falainconnes.org%2Fwp-content%2Fuploads%2FtypeIIIspectral.pdf "citation")
- Jens Kaad e David Kyed (2023), *A comparison of two quantum distances*, Math. Phys. Anal. Geom. 26, art. 8, DOI `10.1007/s11040-023-09451-y`, arXiv:`2212.10874`, Teorema A e §§2–3. **[KNOWN, a conferir]** [arXiv](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2212.10874v2 "citation")
- Masamichi Takesaki (1973), *Duality for crossed products and the structure of von Neumann algebras of type III*, Acta Math. 131, 249–310, DOI `10.1007/BF02392041`, usado para dualidade e pontos fixos. **[KNOWN, a conferir]** [DOI](kimi-cite://web?url=https%3A%2F%2Fdoi.org%2F10.1007%2FBF02392041 "citation")
- Alain Connes e Masamichi Takesaki (1977), *The flow of weights on factors of type III*, Tohoku Math. J. 29, 473–575, DOI `10.2748/tmj/1178240493`, usado para o núcleo II∞ e o escalamento do traço. **[KNOWN, a conferir]** [DOI](kimi-cite://web?url=https%3A%2F%2Fdoi.org%2F10.2748%2Ftmj%2F1178240493 "citation")

**Bloqueio principal:** o menor degrau publicável é condicional. Fecha-se a compressão e o critério GH-S; não se fecha a construção `C¹` da casa nem qualquer descida III₁ por Takesaki. A conjectura permanece viva e claramente tipada, sem Lean e sem promoção.
