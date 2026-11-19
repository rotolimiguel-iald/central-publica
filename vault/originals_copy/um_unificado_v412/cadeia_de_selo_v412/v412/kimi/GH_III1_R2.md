# K05 — GH para III₁, rodada 2: correção clássica e o menor degrau II∞

## 0. Veredito

**[CONJECTURE]** A extensão GH a III₁ permanece conjectura. Em III₁ a formulação deve usar uma **tripla torcida** e uma candidata a Lip-norma cuja topologia fraca-* precisa ser demonstrada; o produto cruzado II∞ fornece um traço, mas não fornece automaticamente Lip-norma, mapas `C¹`, compacticidade dos espaços de estados normais nem descida métrica.

**Correção material ao Fecho 3 [KNOWN, a conferir].** Rieffel não publica `qGH=GH` no caso comutativo. Publica `dist_q≤dist_GH` (Prop. 4.7) e um contraexemplo à igualdade (Apêndice 1). A correção decorre de Rieffel, **não** de Kaad–Kyed.

**Menor degrau [DERIVED + KNOWN, a conferir].** No andar II∞, a compressão espectral é positiva, unital e `C¹`-contrativa; se forem acrescentadas as aproximações de ordem e as compatibilidades topológicas exigidas por van Suijlekom, seguem **GH-S e GH-R**, com estimativas explícitas e independentes: `d_GH≤γ_M+γ′_M` e `dist_Q≤max{γ_M,γ′_M}`. A quebra exata está em produzir os mapas inversos aproximados e topologias e, depois, em descer por Takesaki: a dualidade é algébrica e escala o traço, não uma isometria de Lip-normas.

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
| **van Suijlekom 2021 + Kaad–Kyed Obs. 3.7** | Teorema 5: `C¹`-aproximações + topologias fracas-* ⇒ GH-S; pela Obs. 3.7 e Kaad–Kyed 2022 Prop. 2.14, o mesmo pacote também ⇒ GH-R. A aproximação `C¹` do círculo dá ambas as convergências. | As hipóteses `C¹`/Lip-norma continuam indispensáveis; isso não diz que GH-R e GH-S sejam universalmente equivalentes. |
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
2. **No círculo [KNOWN, a conferir].** Van Suijlekom constrói a aproximação `C¹` que prova GH-S (Prop. 13). Pela Obs. 3.7 de Kaad–Kyed e pela Prop. 2.14 de Kaad–Kyed 2022, essa mesma aproximação também prova GH-R: os truncamentos de Toeplitz do círculo convergem tanto em qGH de Rieffel como em GH-S. Hekkelman reforça o resultado para os estados puros truncados no sentido GH clássico. Não se deve mais dizer que GH-R do círculo precise de uma ponte nova.
3. **Kaad–Kyed.** O Teorema A confirma que GH-S e GH-R não são universalmente equivalentes, mas seus objetos não são `C(X)` clássicos. Isso não contradiz a convergência simultânea sob as mesmas hipóteses `C¹`, nem decide a identidade clássica; Rieffel já a havia decidido pela desigualdade e pelo exemplo. A correção `qGH≤GH`, e não `qGH=GH`, permanece intacta.
4. **O que fica OPEN.** A versão GH-R/GH-S para os truncamentos III₁ da casa continua dependendo de Lip-norma, topologias e dados `C¹` efetivamente construídos. O resultado do círculo não preenche esses dados em III₁.

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

### Lema II∞-2 — Critérios GH-S e GH-R no núcleo, com estimativas e fronteira entre estados

**Estatuto: [KNOWN, a conferir, condicional; hipóteses para a TGL OPEN].**

Suponha que, além do Lema 1:

- `(E_M,H_M,D_M)` e `(E,H,D)` sejam triplas de sistemas de operadores cujas distâncias metrizem as topologias fracas-* de `S(E_M)` e `S(E)`;
- existam mapas positivos unitais `S_M:E_M→E`, `C¹`-contrativos, tais que `(R_M,S_M)` seja uma `C¹`-aproximação de isomorfismo de ordem, com constantes `γ_M,γ′_M→0`.

Então valem, simultaneamente,

`d_GH((S(E_M),d_M),(S(E),d)) ≤ γ_M+γ′_M → 0`

e

`dist_Q((E_M,L_M),(E,L)) ≤ max{γ_M,γ′_M} → 0`.

**Prova de GH-S.** A Proposição 4 de van Suijlekom dá as duas comparações bilaterais de distâncias com erros `2γ_M` e `2γ′_M`; o Teorema 5 limita a distorção da correspondência por `2γ_M+2γ′_M`, e `d_GH≤(1/2)dis`. ∎ [van Suijlekom 2021, arXiv:2005.08544, Prop. 4 e Teo. 5, KNOWN, a conferir](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2005.08544v2 "citation")

**Prova de GH-R.** A Obs. 3.7 de Kaad–Kyed afirma que o Teorema 5 também vale com GH-S substituída pela qGH de Rieffel, por aplicação da Prop. 2.14 do trabalho anterior dos mesmos autores. Nessa proposição, os mapas positivos unitais têm `C=C′=1`, pois são `C¹`-contrativos. Logo os termos com diâmetro desaparecem e a cota é `max{γ_M,γ′_M}`. ∎ [Kaad–Kyed 2023, arXiv:2212.10874v2, Obs. 3.7, KNOWN, a conferir](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2212.10874v2 "citation"), [Kaad–Kyed 2022, arXiv:2205.06043v1, Prop. 2.14, KNOWN, a conferir](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2205.06043v1 "citation")

**Fronteira precisa.** GH-S usa os **espaços de estados das hipóteses**; para GH-Sₙ, com somente estados normais, é necessário provar separadamente a compacticidade/cobertura e refazer as correspondências. GH-R já está incluído pelo mesmo pacote `C¹`/Lip-norma, sem ponte adicional, e sua convergência simultânea com GH-S não implica equivalência universal entre as duas distâncias. O enunciado **não fecha** sem a construção de `S_M`, `γ_M`, `γ′_M` e as topologias.

### Lema II∞-3 — Takesaki: o que desce e a obstrução à descida ingênua

**Estatuto: [KNOWN, a conferir para a obstrução por Sakai–Tomiyama/Haagerup–Musat e para dualidade; DERIVED apenas para a formulação condicional de H_Tak; descida métrica OPEN].**

**(a) O que desce.** A bidualidade dá um isomorfismo equivariante

`\widehat M⋊_θ R ≅ M⊗B(L²(R))`,

e os pontos fixos de `θ` em `\widehat M` são `π(M)`. Restrições de dados `θ`-equivariantes — representações, projeções, seminormas efetivamente invariantes — podem ser escritas nos pontos fixos. Se uma hipótese nomeada `H_Tak` fornecer mapas `R_M,S_M` equivariantes que já sejam `C¹`-aproximações nos sistemas de pontos fixos e as topologias exigidas, o Lema 2 aplica-se ali, tanto para GH-S como para GH-R. Isso é uma implicação condicional explícita, não uma prova de `H_Tak`.

**(b) O que não desce.** `τ∘θ_s=e^(−s)τ` não é invariância métrica; a dualidade não afirma preservação de Lip-norma, de `C¹`-constantes, de qGH ou de GH-S. Em particular, **não existe esperança condicional normal** `E:\widehat M→π(M)`.

**Prova por referência, não derivação autônoma.** Sakai–Tomiyama, reproduzido por Haagerup–Musat no Lema 2.11, afirma: se `N` é uma álgebra de von Neumann semifinita e `M⊆N` é uma subálgebra de von Neumann de tipo III, então não existe esperança condicional normal de `N` sobre `M`. Aplique `N=\widehat M`, que é II∞, e a subálgebra `π(M)`, que é III₁. A conclusão segue diretamente, sem supor `τ∘E=τ` e sem exigir fidelidade de `E`. [Haagerup–Musat 2007, arXiv:0706.3463v2, Lema 2.11, KNOWN, a conferir](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F0706.3463v2 "citation")

**Direção dos estados e extensões normais individuais.** Todo estado normal em `π(M)` admite uma **extensão normal individual** a `\widehat M`, independentemente de `E`, por Blackadar, Cor. III.2.1.10. Portanto, extensões normais individuais existem e **não são o obstáculo**; restringir estados de `\widehat M` a `π(M)` também é automático. Se `E` existisse, `φ↦φ∘E` forneceria, ao contrário, um **esquema coerente de extensão** por UMA esperança condicional normal, positiva, unital e `π(M)`-bimodular. [Blackadar 2006, *Operator Algebras*, Cor. III.2.1.10, DOI 10.1007/3-540-28517-2, KNOWN, a conferir](kimi-cite://web?url=https%3A%2F%2Fdoi.org%2F10.1007%2F3-540-28517-2 "citation")

**Quebra exata.** A obstrução é à existência de um **esquema coerente de extensão via UMA esperança condicional normal, positiva, unital e `π(M)`-bimodular** e, sobretudo, de **extensões equivariantes compatíveis com Lip-normas, constantes `C¹` e truncamentos**. Não é uma obstrução à existência de extensões normais individuais. A bidualidade, sozinha, entrega estabilização e pontos fixos, não esse esquema nem essas compatibilidades. Sem `H_Tak`, concluir III₁-GH a partir de II∞-GH seria modus ponens oco.

## 7. Possíveis contraexemplos — e seus alvos exatos

1. **Contraexemplo publicado à igualdade clássica [KNOWN, a conferir].** O par `Y={0,1,2}`, `Z={0,3}` de Rieffel/Li tem `dist_q=1/2<1=dist_GH`. Derruba `qGH=GH`, não a convergência GH-S do círculo.
2. **Contraexemplo publicado à ponte universal GH-S ⇒ GH-R [KNOWN, a conferir].** Kaad–Kyed constrói `p_n∈(1,2)`, `p_n→1`, e dimensões `N_n` para as quais a GH dos espaços de estados vai a 0, enquanto qGH fica `≥1/4`. Não é `C(X)` clássico nem III₁; é um contraexemplo à inferência universal, não à conjectura III₁ bem posta. [Kaad–Kyed 2023, arXiv:2212.10874, KNOWN, a conferir](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2212.10874v2 "citation")
3. **Candidata a contraexemplo à estratégia ingênua [DECLARADO/OPEN].** Uma grade com aliasing que enrola o modo `+M` em `−M`, como a lição de debug do artigo, pode impedir as estimativas `C¹` porque o comutador amplifica o termo de borda. Ela não é um contraexemplo construído à conjectura com Toeplitz e Lip-norma; é um teste que a demonstração precisa excluir explicitamente.
4. **O que continua sem contraexemplo construído [OPEN].** Não foi encontrada, nas fontes consultadas, uma tripla torcida III₁ com `L_σ` Lip-norma e truncamentos legítimos que falsifique GH-R ou GH-S. Essa ausência não é prova da conjectura.

## 8. Estatuto dos lemas e bloqueios em uma tabela

| enunciado | estatuto | o que falta |
|---|---|---|
| II∞-1: compressão positiva/unital/`C¹`-contrativa e convergência forte | **[DERIVED, fechado sob as hipóteses]** | Não produz inversa aproximada nem convergência uniforme. |
| II∞-2: `C¹` + topologias ⇒ GH-S com erro `γ+γ′` e GH-R com erro `max{γ,γ′}` | **[KNOWN, a conferir, condicional]** | Construir `S_M`, erros e topologias; GH-Sₙ exige análise separada, GH-R não exige ponte nova. |
| II∞-3: restrição equivariante condicional; nenhuma esperança condicional normal para III₁ | **[KNOWN, a conferir para Sakai–Tomiyama/Haagerup–Musat e Blackadar; descida OPEN]** | `H_Tak`: esquema coerente por UMA esperança condicional normal, positiva, unital e `π(M)`-bimodular e extensões equivariantes compatíveis com Lip-normas, `C¹` e truncamentos; extensões normais INDIVIDUAIS existem e não são o obstáculo. |
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
- Jens Kaad e David Kyed (2023), *A comparison of two quantum distances*, Math. Phys. Anal. Geom. 26, art. 8, DOI `10.1007/s11040-023-09451-y`, arXiv:`2212.10874v2`, Teorema A e Obs. 3.7. **[KNOWN, a conferir]** [arXiv](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2212.10874v2 "citation")
- Jens Kaad e David Kyed (2022), *The quantum metric structure of quantum SU(2)*, arXiv:`2205.06043v1`, Prop. 2.14: cota qGH para mapas positivos unitais e, no caso `C=C′=1`, `max{γ,γ′}`. **[KNOWN, a conferir]** [arXiv](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2205.06043v1 "citation")
- Uffe Haagerup e Magdalena Musat (2007), *Classification of hyperfinite factors up to completely bounded isomorphism of their preduals*, arXiv:`0706.3463v2`, Lema 2.11, que reproduz Sakai–Tomiyama: inexistência de esperança condicional normal de álgebra semifinita sobre subálgebra tipo III. **[KNOWN, a conferir]** [arXiv](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F0706.3463v2 "citation")
- Bruce Blackadar (2006), *Operator Algebras: Theory of C*-Algebras and von Neumann Algebras*, Encyclopaedia of Mathematical Sciences 122, Springer, DOI `10.1007/3-540-28517-2`, Cor. III.2.1.10: todo estado normal numa subálgebra de von Neumann admite extensão normal à álgebra ambiente, sem esperança condicional. **[KNOWN, a conferir]** [DOI](kimi-cite://web?url=https%3A%2F%2Fdoi.org%2F10.1007%2F3-540-28517-2 "citation")
- Masamichi Takesaki (1973), *Duality for crossed products and the structure of von Neumann algebras of type III*, Acta Math. 131, 249–310, DOI `10.1007/BF02392041`, usado para dualidade e pontos fixos. **[KNOWN, a conferir]** [DOI](kimi-cite://web?url=https%3A%2F%2Fdoi.org%2F10.1007%2FBF02392041 "citation")
- Alain Connes e Masamichi Takesaki (1977), *The flow of weights on factors of type III*, Tohoku Math. J. 29, 473–575, DOI `10.2748/tmj/1178240493`, usado para o núcleo II∞ e o escalamento do traço. **[KNOWN, a conferir]** [DOI](kimi-cite://web?url=https%3A%2F%2Fdoi.org%2F10.2748%2Ftmj%2F1178240493 "citation")

**Bloqueio principal:** o menor degrau publicável é condicional. Fecham-se a compressão e os critérios GH-S/GH-R sob o mesmo pacote `C¹`; não se fecha a construção `C¹` da casa nem qualquer descida III₁ por Takesaki. A inexistência de esperança condicional normal é citada por Sakai–Tomiyama/Haagerup–Musat, sem derivação autônoma e sem `τ∘E=τ`. A conjectura permanece viva e claramente tipada, sem Lean e sem promoção.
