# REVISÃO DISTINTA DA ENTREGA K05 (v412) — MONTAGEM 3+1 e GROMOV–HAUSDORFF a III₁

Revisor distinto (quem constrói não aprova). 14/11/2026. Só leitura fora desta pasta; nada registrado no Mapa, nada depositado na fila, nada instalado, nenhum `lake`, nenhum arquivo do Kimi tocado.
Estatutos: **[REAL]** conferido por mim com a consulta/script citado · **[KNOWN]** literatura conferida na fonte, com identificador · **[DERIVED]** derivado por mim aqui · **[DECLARADO]** do Kimi, não conferido · **[OPEN]**.
Escopo: `MONTAGEM_3MAIS1_R2.md` (sha256 `3eeb6c56…`), `GH_III1_R2.md` (sha256 `0f5e367d…`), erratas `K05\MONTAGEM_GH\ERRATA_GH_III1_R2.md`, `ERRATA_GH_III1_R3.md`, `REV0\`, `REV1\`, `ARQUIVO_GH_III1_OCA.md`, contra `ORDEM_K05_matematica_rodada_2.md` (seções B e C), `REVISAO_K02.md` e o artigo `A Ponte Einstein Cartan Miguel.tex` (sha256 `98ec3d80…`).

## 0. Veredito

| frente | veredito |
|---|---|
| **A. Montagem 3+1** | **APROVADA COM RESSALVAS.** O (4,0) está identificado de fato: Dirac, `J`, `χ`, sinais KO 4 e o rótulo `T³×S¹` conferem por cálculo explícito (script). **Um erro numérico material**: a constante do ciclo de orientação (`−1/18`) está errada; o certo, com as fórmulas do próprio documento, é `−1/24`. A lista L1–L10 de axiomas lorentzianos tem três omissões (§A6). O estatuto de (1,3), «(H) com moldura publicada para definição e sinais», está certo, nem mais nem menos. |
| **B. GH–III₁** | **APROVADA COM RESSALVAS.** Nenhuma promoção indevida: a conjectura segue `[CONJECTURE]` do começo ao fim. Todas as citações que consegui abrir dizem o que o documento diz (Rieffel, van Suijlekom, Kaad–Kyed, Haagerup–Musat, Hekkelman, Connes–Moscovici); a direção de Sakai–Tomiyama está certa; as erratas R2/R3 e os hashes REV0/REV1 conferem. Ressalva de enquadramento: o «degrau II∞» não tem conteúdo específico de II∞ (os Lemas 1 e 2 valem em qualquer tipo; a metade condicional do Lema 3 é tautológica); só a obstrução negativa usa II∞. Blackadar Cor. III.2.1.10 não consegui abrir. |

## 1. Aferição antes de afirmar ausência ou novidade

- **Mapa de Rotas** (termos únicos; a consulta por frase devolve zero por construção, logo a do Kimi, §1 de ambos os documentos, não prova nada): `rotas.py consultar Rieffel`, `triplas`, `Hausdorff`, `Krein`, `Dossena`, `Suijlekom`, `Tomiyama`, `Toeplitz` → 0 rotas cada (2059 registros, cabeça `cab386c822ca5a3e`); `toro` → só `cadeia.preparacao_v412` (EM_CURSO, rota geral da preparação). Nada refeito, nada registrado. [REAL]
- **Kernel** (`...\tgl_kernel\TGLExt`, só leitura; `grep -rIl`): `SpectralTriple`, `TriplaEspectral`, `Gromov`, `Rieffel`, `qGH`, `ghDist`, `Krein`, `Sakai`, `Hausdorff`, `Toeplitz`, `KO_dim`, `Dixmier` → **0 arquivos**. `Tomiyama` → 2 (`CondExpect.lean` l.6/103 e `EsperancaCondicional.lean` l.38/89/97), todos o **Tomiyama finito** (esperança condicional de dimensão finita, relação de Jones); não tocam a obstrução Sakai–Tomiyama de tipo III. Bancada (`BANCADA_TOE\kernel_bancada`): `Krein`, `SpectralTriple`, `Gromov|Rieffel`, `Sakai|Tomiyama` → 0. [REAL] A afirmação do Kimi («nenhuma ocorrência geométrica no recorte consultado») confere.
- **Inventário da bancada** (`INVENTARIO_BANCADA_CHATGPT.md`, `grep -c`): `SpectralTriple|tripla espectral`, `Gromov|Rieffel|qGH`, `Krein`, `Sakai|Tomiyama`, `Hekkelman|Kaad|Suijlekom` → 0 linhas. [REAL]
- **Acervo** (`C:\IALD\INDICE_DO_ACERVO\buscar.py`): `Rieffel` e `Krein` só aparecem no próprio artigo e em JSON de sombra (`tgl continuum v1`, `tgl three locks v1`, `tgl krein signature v1`); nenhum trabalho prévio de GH/Rieffel além do que o artigo já cita. A busca por `tripla espectral|spectral triple` passou de 180 s e foi para segundo plano sem uso. [REAL, parcial]
- **Identificadores** (`scripts_k05_mgh\arxiv_meta.py`, `crossref_meta.py`; saídas `.json`): todos os arXiv e DOIs citados nas duas frentes existem e batem com autor/título/periódico declarados (Rieffel Mem. AMS 168(796); CvS CMP 383, 2021–2067; vS J. Geom. Phys. 162, 104075; Leimbach–vS Adv. Math. 439, 109496; Hekkelman Lett. Math. Phys. 112, art. 20; Kaad–Kyed MPAG 26, art. 8; D–D IJGMMP 8, 1833–1848; vdD MPAG 19, art. 4; **BBB J. Math. Phys. 59, 062303**; Takesaki Acta Math. 131, 249–310; Connes–Takesaki Tohoku 29, 473–575). Não conferível por metadados: Connes–Moscovici (Aspects Math. E38, 57–71) e o conteúdo dos livros (GVF 2001; Blackadar 2006). [KNOWN, metadados]

## 2. FRENTE A — Montagem 3+1 (`MONTAGEM_3MAIS1_R2.md`)

Script: `scripts_k05_mgh\revisor_montagem.py` → `revisor_montagem_saida.json`. Fontes lidas por mim: D–D (arXiv:1011.4456, texto e páginas 12, 14–16 como imagem), van den Dungen (1505.01939), BBB (1611.07062), Connes 1996 (hep-th/9603053), Connes 2008 (0810.2088, resumo e sumário).

### A1. §3: «quatro triplas do círculo = tripla canônica do toro plano T⁴ com spin trivial»

| afirmação | veredito | razão |
|---|---|---|
| Fórmulas de produto: ímpar×ímpar `H=(H₁⊗H₂)⊗ℂ²`, `D=D₁⊗1⊗σ₁+1⊗D₂⊗σ₂`, `χ=1⊗1⊗σ₃`; par×ímpar `D=D_par⊗1+χ_par⊗D_ímpar` (l.57–61) | **certo** [KNOWN+REAL] | D–D (25) e §4.2/(18); reproduzidas por mim passo a passo (S¹×S¹ → T² → T³ → T⁴). |
| «escolha-se M₊ da Tabela 6, compatível com a seleção de Connes» (l.61) | **certo** [REAL] | D–D (26) dá `M₊(1,1)=σ₂` e `M₊(3,1)=σ₀` (identidade); Tabela 6 (página 12, lida como imagem) confere. Com `J⁺` os sinais dos passos saem (−,+,−) em KO 2, (−,+) em KO 3, (−,+,+) em KO 4 = seleção de Connes (script, bloco `c_sinais_passos`). |
| `Γ₁=σ₁⊗τ₁, Γ₂=σ₂⊗τ₁, Γ₃=σ₃⊗τ₁, Γ₄=1⊗τ₂`: autoadjuntas, quadrado 1, anticomutam; `χ=−Γ₁Γ₂Γ₃Γ₄` (l.75–77) | **certo** [REAL] | script bloco `a_gamas`: as quatro verdadeiras. |
| `D_λ^{prod}` e o operador intermediário de T³ (l.63–65) | **certo** [REAL] | script bloco `c_iterado_igual_ao_doc`: a iteração de D–D devolve exatamente `Γ_j`, `χ` e `C=σ₂⊗1`. |
| `J=(σ₂⊗1)K`, `J²=−1, JD=DJ, Jχ=χJ` ⇒ KO 4 (l.69, 79) | **certo** [REAL] | script bloco `b_sinais_J_doc` = (−1,+1,+1), igual a Connes n=4. **Lacuna de exposição (menor):** o `J` final é afirmado, não derivado; a cadeia é `J_{T³}=σ₂K` (de `M₊(1,1)=σ₂` e do passo par×ímpar) e `M₊(3,1)=σ₀`; escrevi-a no script. |
| «`U₄` é literalmente a identificação de bases» (l.73) | **certo** | em `L²(T⁴)⊗ℂ²⊗ℂ²≅L²(T⁴,ℂ⁴)` o `D` já é `−iλΣΓ_j∂_j`; o spin é o trivial (D–D §6: «flat torus with the trivial spin structure»; o círculo canônico tem autovalores inteiros = periódico). |
| **Orientação (§3.3, l.85–93):** `c_{(4,λ)}=−(1/18)×_{j}c^j_{1,λ}`, «a constante resulta de `r₂=i, r₃=3, r₄=6i` de D–D (35)–(36)», `π_{D_λ}(c_{(4,λ)})=χ` | **ERRADO (a constante)** [REAL] | Ver abaixo. O ciclo de orientação existe e realiza `χ`; mas com a constante do documento `π_D(c)=(4/3)χ`, não `χ`. O certo é `−1/24`. |
| Ciclo de orientação coincide com o do toro plano (l.93) | **certo na substância** | o shuffle iterado dos quatro 1-ciclos É o ciclo de volume padrão de T⁴ (ordem `dx₁∧…∧dx₄`); só a normalização está errada. |

**O erro da constante (item que a ordem pedia para caçar: «algo só afirmado e chamado de identificado?»).** O Kimi copiou D–D (35)–(36), onde `r = ν_{n₁+n₂}` (ou `iν`), `ν_n=½(n−1)n`, justificado por «a sum of ½(n₁+n₂−1)(n₁+n₂) identical terms» (D–D p.15, (39); (43) p.16, lidas como imagem). Mas a soma do produto shuffle tem `C(n₁+n₂, n₁)` termos, não `ν_n`. Os dois coincidem só quando `n₁=2` ou `n₂=2` (`C(n,2)=½(n−1)n`). Contagem pelo script (`d_contagem_shuffles_vs_nu_DD`): (1,1) → 2 shuffles contra ν₂=1; (2,1) → 3 contra 3; **(3,1) → 4 contra ν₄=6**; (2,2) → 6 contra 6.
Cálculo direto com as matrizes do documento (cada termo vale `sgn(τ)·λ⁴·Γ_{τ(1)}…Γ_{τ(4)}=λ⁴Γ₁Γ₂Γ₃Γ₄`, pois as `Γ` anticomutam e o fator `ΠU_j^{-1}ΠU_j=1`): `Σ_{τ∈S₄}=24λ⁴Γ₁Γ₂Γ₃Γ₄=−24λ⁴χ`. Logo o ciclo normalizado é `c_{(4,λ)}=−(1/24)×_{j}c^j_{1,λ}`; as constantes sucessivas corretas são `r₂=2i` (verificado direto: `π_D(c₁×c₂)=2σ₁σ₂=2iσ₃`, e D–D (43) daria `iσ₃`), `r₃=3`, `r₄=4i`, produto −24 (D–D literal: `i·3·6i=−18`). [REAL: script blocos `d_orientacao`, `d_passo_1_1`, `d_produto_r`]. O erro é da fórmula publicada de D–D, herdado sem conferência; não procurei errata publicada de D–D (limite). A regra de escala da §5 (`c_λ=λ⁻⁴c`) não depende da constante e segue certa.

### A2. §4: finitude e dualidade de Poincaré no caso comutativo

- **Finitude:** `H^∞=C^∞(T⁴)⊗ℂ⁴=C^∞(T⁴)⁴` livre de posto 4 ⇒ finito projetivo: **certo** [DERIVED, trivial]. «A medida de Lebesgue e a lei de Weyl dão a continuidade absoluta»: **certo e padrão**, mas **lacuna de citação**: nenhum teorema é nomeado (a fonte natural é o teorema da traça de Connes / Dixmier; não aparece).
- **Poincaré:** «o Dirac do spin trivial é a classe fundamental; por Künneth `K⁰(C(T⁴))`, `K¹` livres de posto 8; emparelhamento unimodular; cap = isomorfismo de Poincaré»: **certo na substância, citação insuficiente.** `K⁰(T⁴)=ℤ⁸` ✓. Conferi a unimodularidade por conta própria: `ch` identifica `K⁰(T⁴)` com `Λ^{par}(ℤ⁴)` (fato padrão para toros, não derivado aqui), `Â=1` no toro plano, e a forma de interseção é a forma de cunha `Λ^{par}×Λ^{par}→Λ⁴=ℤ`, de **determinante +1** (script bloco `e_forma_intersecao_T4`, matriz 8×8). [DERIVED sobre KNOWN]
- **Qual teorema é citado e ele diz isso?** Connes 1996 (hep-th/9603053, lido): o Axioma 5 (finitude) e o Axioma 6 (Poincaré, forma de interseção invertível) são **definições**; o Teorema/d) diz que a representação é `L²(M,S)` com o Dirac de Levi-Civita; a Observação 4 diz «When M is a Spin manifold the map ρ↦g(ρ) is surjective … (This amounts to checking that all axioms are fulfilled)». Ou seja, **afirma** e não demonstra. Gracia-Bondía–Várilly–Figueroa 2001: o próprio documento diz «ficha e sumário editorial consultados»; o livro não foi aberto. Conclusão: nenhum dos dois textos citados **prova** finitude/Poincaré para a tripla canônica de T⁴; a frase «estas fontes sustentam o caso comutativo» (l.109) deve passar a «Connes 1996 afirma (Obs. 4), GVF 2001 trata (capítulos, não lidos), conferido para T⁴ por Künneth+cunha». Estatuto da §4 `[DERIVED + KNOWN, a conferir]` é aceitável.

### A3. §5: o escalonamento `λ=β^{-1/2}` — refiz a conta

- `D_λ=λD₁` ⇒ `[D_λ,a]=λ[D₁,a]`; `d_λ=sup{|a(x)−a(y)|:‖[D_λ,a]‖≤1}=λ⁻¹d₁=β^{1/2}d₁`: **certo**. Tensor métrico por `λ⁻²=β`: **certo**. Concorda com o artigo (l.1941: «distância verdadeira √β·π»).
- Integral de Dixmier `Tr_ω(T|D_λ|⁻⁴)=λ⁻⁴Tr_ω(T|D₁|⁻⁴)`: **certo**; `λ⁻⁴=β²`: **certo** (script bloco `f_escala`).
- Orientação: `π_{D_λ}(c)=J(a₀)[D_λ,a₁]…[D_λ,a₄]=λ⁴π_{D₁}(c)` ⇒ `c_λ=λ⁻⁴c`: **certo** (e é o que `λ^{-4}` incorporado em `c^j_{1,λ}` já faz, l.87). A exigência `c_λ=λ⁻⁴c` está certa; a constante numérica que a acompanha (−1/18) não (A1).
- `J` e primeira ordem não mudam (λ real); regularidade (domínios iguais, `δ_{|D_λ|}=λδ_{|D₁|}`); Poincaré por `D|D|⁻¹` e por homotopia `t↦λ_tD₁`: **certo**. Hermitiana `(ξ,η)_λ=λ⁴(ξ,η)₁` consistente com a integral: **certo**.

### A4. §2: o rótulo (`T³×S¹` é ímpar×ímpar)

**Certo.** A citação do texto antigo é fiel (`MONTAGEM_3MAIS1.md` l.82: «`T³×S¹`: par×ímpar; resultado par, métrica 4, KO 4»). `T³` tem KO 3 (ímpar) e `S¹` KO 1 (ímpar); a cadeia (ímpar×ímpar→par KO 2; par×ímpar→ímpar KO 3; ímpar×ímpar→par KO 4) e `2·1·2=4` conferem (script `c_sinais_passos`). O erro era só de rótulo.

### A5. §6: o que van den Dungen e BBB cobrem para assinatura (1,3)

- **van den Dungen** (1505.01939): Def. 2.2 = tripla de Krein par: espaço de Krein ℤ₂-graduado, *-álgebra, simetria fundamental `𝒥`, `D` fechado ímpar com (1) `E=Dom D∩𝒥Dom D` denso, (2) Krein-autoadjunto, (3) comutadores limitados em `E`, (4) `π(a)ι` compacto — **analítica, como o Kimi diz** [KNOWN]. Eq. (1) §3 = condição de ordem um (`[π(a),[D,π^{op}(b)]]=0`) ✓. Def. 4.2/Prop. 4.3 = só `F×M` (F finito, M pseudo-Riemanniana spin) ✓. Obs. 6.4 = «there is no Krein version of K-homology», sinais dependeriam da assinatura ✓. Nada de finitude, orientação, Poincaré lorentzianos ✓.
- **BBB** (1611.07062): `(m,n)=(p+q,p−q)` mod 8, aditivo no produto tensorial graduado (resumo) ✓; Tabela 3, linha m=4, coluna n=6: `(t,s)=(1,3)` ✓; convenção West coast `(p,q)=(1,3)`, `n=1−3≡6` ✓ (texto, p.3); tripla indefinida **par** (§5: «The extension of this tensor product to odd-dimensional indefinite spectral triples seems difficult»), definição sem finitude/orientação/Poincaré ✓. Consequência que o documento não explicita: o círculo é ímpar, logo o produto de quatro círculos NÃO está coberto por BBB (teria de agrupar em fatores pares).
- **Estatuto «(H) COM MOLDURA PUBLICADA PARA DEFINIÇÃO/SINAIS; o restante [OPEN]»: certo, nem mais nem menos** [KNOWN + julgamento]. Limite honesto: BBB [30,33,38,57–61] e vdD [PS06, Str06] citam literatura lorentziana (Strohmaier 2006; Paschke–Sitarz 2006; Franco–Eckstein 2013–2015; Moretti 2003) que **nem o Kimi nem eu** consultamos; se algum contiver estrutura causal ou reconstrução, L9/L10 podem ter moldura publicada adicional. Não conferido.

### A6. §7: a lista L1–L10 está completa em relação ao que o artigo usa?

Mapeamento dos «primos» (Connes 1996, texto lido): Axioma 1 dimensão; 2′ `[[D,a],b°]=0`; 3 regularidade; 4′ ciclo de Hochschild `π(c)=γ`; 5 finitude; 6′ cup por `μ∈KR_n(A⊗A°)` é isomorfismo; 7′ `[a,b°]=0` e tabela de sinais. **A atribuição de origem de L2–L8 está certa.** O que o artigo `ax:lorentz` (l.523–530) nomeia: regularidade, dimensão espectral 4, orientabilidade, realidade, causalidade via Π_irr; o Kimi acerta que faltam primeira ordem, finitude e Poincaré. Omissões que encontrei:

1. **Falta o item do TIPO (III₁/sem traço).** O artigo diz (l.642–650) que «a reconstrução de Connes exige traço e projetores finitos — que III₁ não tem» e leva o ônus ao produto cruzado II∞ (l.2224–2227: «obstáculo central»). L2 (somabilidade), L7 (finitude, `∫a ds⁴` via traço de Dixmier) e L8 (Poincaré) pressupõem um traço; a lista só trata a obstrução da **assinatura**. Falta um item L0 («tipo da álgebra: traço de Dixmier em II∞ via produto cruzado, ou tripla torcida de Connes–Moscovici»), que o próprio `GH_III1_R2.md` §2.1 já usa.
2. **Falta o elo Euclides→Lorentz** que o artigo afirma: (C-5) Osterwalder–Schrader e (C-6) «a continuação lorentziana herda (1,3)» (l.1803–1816). O §6.3 diz que KO 4 não vira (1,3), mas a lista não tem item que exija o teorema de continuação/Wick entre a tripla (4,0) da §3 e a de Krein.
3. **L10 cita a fonte errada para a reconstrução.** O artigo usa «Connes 2008 (reconstrução)» (l.1798, arXiv:0810.2088). O resumo desse artigo (lido) diz: «the **first five** of the axioms … suffice (in a slightly stronger form) to characterize the spectral triples associated to smooth compact manifolds; the algebra, which is assumed to be **commutative**». Em ordem de Connes 1996, os cinco primeiros são dimensão, primeira ordem, regularidade, orientabilidade e finitude. Logo, para a reconstrução riemanniana, **Poincaré (L8) e realidade (L4) não entram**, e o caso não comutativo (o da TGL) é o §12.6 «The Noncommutative case» do sumário. O documento cita Connes 1996/GVF para L10 e declara L5–L8 «bloqueios centrais»; para a seta de reconstrução do artigo os bloqueios são L2, L3, L5, L6, L7 (+ o item de tipo), e Poincaré cabe ao enunciado de spin. [KNOWN: resumo e sumário; o teorema em si não foi lido]

## 3. FRENTE B — GH–III₁ (`GH_III1_R2.md`)

Fontes baixadas e lidas por mim (`scripts_k05_mgh\refs_dl\`, dados não confiáveis, lidos com `pdftotext`): Rieffel math/0011063v4; van Suijlekom 2005.08544v2; Kaad–Kyed 2212.10874v2 e 2205.06043v1 (v3 também); Haagerup–Musat 0706.3463v2; Hekkelman 2111.13865v2; Leimbach–vS 2302.07877v2 (resumo e sumário); Connes–Moscovici math/0609703v2.

### B7. §4: «Rieffel publica qGH ≤ GH, com exemplo de desigualdade estrita»

**Certo** [KNOWN, na fonte]. Rieffel arXiv:math/0011063v4, **Prop. 4.7** (l.887 do texto): `dist_q(A₁,A₂) ≤ dist_GH(X₁,X₂)`, seguida de «But the above inequality can fail to be an equality. A specific example, found by Hanfeng Li, is presented in Appendix 1». **Apêndice 1 (por Hanfeng Li)** (l.3779–3880): `Y={y₁,y₂,y₃}` com `ρ(y₁,y₂)=ρ(y₂,y₃)=1`, `ρ(y₁,y₃)=2`; `Z={z₁,z₂}` com `ρ=3`; `dist_GH(Y,Z)=1` e `dist_q(C(Y),C(Z))=1/2`. O Kimi o descreve fielmente (`{0,1,2}` e `{0,3}` são as imersões isométricas que o próprio Li usa). Detalhe: o exemplo é do Li, publicado dentro da memória de Rieffel; as funções são reais (espaços de unidade de ordem); Kaad–Kyed (§2) confirma que a `dist_QGH` de operador-sistemas coincide com a de Rieffel nos espaços de unidade de ordem. A errata ao artigo (l.1937–1939, «no caso comutativo, qGH = GH (Rieffel)») está **justificada**: Rieffel dá só `≤`, e há contraexemplo comutativo.

### B8. §6: os três lemas do degrau II∞

**Lema 1 (compressão).** **Certo** [DERIVED por mim + REAL]. `[D_M,R_M a]=P_M[D,a]P_M` (usa só `P_M` comutar com `D`); contratividade em norma e em `L`; positividade; `R_M(1)=P_M`; `P_MaP_M−a=P_Ma(P_M−1)+(P_M−1)a`. Sanidade numérica em dimensão finita (200 sorteios): `scripts_k05_mgh\revisor_lema1.py` → `revisor_lema1_saida.txt`, todas as identidades e desigualdades verdadeiras. O «o que não segue» está certo e honesto (nem inversa aproximada, nem uniformidade; resolvente compacto exigido por van Suijlekom Def. 1).

**Lema 2 (GH-S e GH-R).** **As estimativas seguem do que está escrito, e as hipóteses estão NOMEADAS (não escondidas)** [KNOWN, conferido nas fontes].
- van Suijlekom (2005.08544): Def. 2 («approximate order isomorphism»: `R_n,S_n` positivos unitais, `‖S_nR_n(a)−a‖≤ε_n‖a‖₁`, `‖R_nS_n(h)−h‖≤ε'_n‖h‖₁`), «C¹-contrativo» (contrativo na norma e na seminorma de Lipschitz), Prop. 4 (comparações bilaterais com erros `2ε`), Teo. 5 (hipótese: topologias de `d` = fraca-* em `S(E_n)`, `S(E)`), e a prova: `d_GH ≤ ½·dis(R_n)`, `dis ≤ 2ε_n+2ε'_n` ⇒ `d_GH ≤ ε_n+ε'_n` ✓.
- Kaad–Kyed 2212.10874, **Remark 3.7** (a «Obs. 3.7» do Kimi): «van Suijlekom's main convergence result [Theorem 5] holds true also when dist_GH is replaced by dist_QGH, … by an application of [9, Proposition 2.14]» ✓. A Prop. 2.14 de Kaad–Kyed 2205.06043**v1** (l.677 do texto): `φ,ψ` positivos unitais, `L'(φ(x))≤C·L(x)`, `L(ψ(y))≤C'·L'(y)`, `‖ψφ(x)−x‖≤ε L(x)`, `‖φψ(y)−y‖≤ε' L'(y)` ⇒ `dist_Q ≤ max{diam·|1−1/C|+ε/C, diam'·|1−1/C'|+ε'/C'}`; com `C=C'=1` os termos de diâmetro somem e sobra **`max{ε,ε'}`** ✓ [DERIVED sobre KNOWN, conferido]. Citar a **v1** é o certo (a v3, de 2025, é a versão do Memoirs EMS e pode renumerar).
- Hipóteses nomeadas no enunciado: distâncias que metrizam a fraca-* (vS Teo. 5); mapas `S_M` positivos, unitais, `C¹`-contrativos, constantes `γ_M,γ'_M→0`; resolvente compacto (nota do Lema 1). **Nada escondido.**
- **Duas observações que não são erros:** (i) o limite `d_GH≤γ+γ'` é implicado pelo de GH-R: Kaad–Kyed §2, logo após (2.2), «dist_GQH dominates dist_GH», então `d_GH ≤ dist_Q ≤ max{γ,γ'}` (melhoria, não correção); (ii) **os Lemas 1 e 2 não usam II∞**: valem para qualquer tripla de sistema de operadores, em qualquer tipo; o traço de `M̂` nunca entra (o próprio texto diz «o traço de M̂ não altera esta conta»). O título «o andar II∞» e o rótulo «menor degrau publicável» (§0, §8) prometem mais do que os lemas entregam: nenhuma tripla `(E,H,D)` concreta em `M̂` é exibida e os «truncamentos que a casa usa» (a cascata `P_MDP_M`, artigo l.1936–1941 e a lição de debug l.1944–1950) não são ligados a `M̂`.

**Lema 3 (Takesaki).** **Certo na parte negativa; tautológico na parte condicional.**
- (a) bidualidade `M̂⋊_θℝ≅M⊗B(L²ℝ)` e pontos fixos de `θ` = `π(M)`: padrão [KNOWN, Takesaki 1973; **não abri**]. Mas «se `H_Tak` fornecer `R_M,S_M` equivariantes que já sejam `C¹`-aproximações nos sistemas de pontos fixos, o Lema 2 aplica-se ali»: os pontos fixos SÃO `π(M)` (III₁); `H_Tak` é então a hipótese `C¹` do Lema 2 aplicada diretamente a `π(M)`. A «descida por Takesaki» não traz nada; o II∞ é irrelevante para a implicação condicional. O Kimi quase diz («modus ponens oco», l.150) e a tabela §8 registra `descida OPEN`, mas o enquadramento como «degrau» fica generoso.
- (b) **Sakai–Tomiyama.** Haagerup–Musat 0706.3463v2, **Lemma 2.11** (l.633, lido com a prova): «Let N be a semifinite von Neumann algebra and let M⊆N be a von Neumann subalgebra of type III. Then there is no **normal** conditional expectation from N onto M» (atribuído a Sakai [36] e Tomiyama [43, Thm 3]). **Direção:** da álgebra ambiente semifinita `N` **sobre** a subálgebra de tipo III `M`. **Aplica-se ao caso:** `N=M̂` (II∞, semifinita, Takesaki/Connes–Takesaki) e `π(M)≅M` (III₁) é subálgebra de von Neumann unital ⇒ não há `E` normal de `M̂` sobre `π(M)`. O qualificador «normal» é essencial: para `M` injetiva (hiperfinita) existe esperança condicional **não normal** (norma um); o documento mantém «normal» ✓. A prova do Lema 2.11 (e do REV0 refutada na R2) não usa `τ∘E=τ`: a R2 acertou em removê-la.
- (c) **Direção dos estados / extensões individuais.** R3: «todo estado normal numa subálgebra de von Neumann admite extensão normal à ambiente (Blackadar Cor. III.2.1.10); o obstáculo é o esquema coerente por UMA esperança condicional normal, positiva, unital, `π(M)`-bimodular». O **conteúdo é correto e a correção da R2→R3 é boa** (a redação da R2, «a obstrução é à extensão normal dos estados», era larga demais). **Não consegui abrir o Cor. III.2.1.10** (livro, DOI 10.1007/3-540-28517-2): marcado não conferido. O resultado é padrão e coerente com Sakai–Tomiyama (extensões individuais não precisam ser lineares nem bimodulares); um esquema linear, positivo e normal que seja inverso à direita da restrição daria, pelo teorema de Tomiyama (projeção de norma um), justamente a esperança condicional excluída.

### B9. Sakai–Tomiyama: enunciado exato, direção, aplicação — ver B8(b). **Certo.**

### B10. Hekkelman (arXiv:2111.13865)

**Usado corretamente, mas só como citação** (tabela §3 l.57; §4(2) l.78; §10 l.180); não entra em nenhuma prova. O resumo (lido): «the pure state space on the n×n complex Toeplitz matrices converges in the Gromov–Hausdorff sense to the state space on C(S¹)»; **Teorema 3.8**; §4 «Recovering S¹». O Kimi diz que o limite é `S(C(S¹))` e não `S¹`/estados puros clássicos ✓ e que não é teorema III₁ ✓.

### B11. Nada foi promovido?

**Confere.** `[CONJECTURE]` na §0 (l.5), na §2.2 (l.48, versão tipada), na tabela §8 (l.166), no bloqueio final (l.190); os Lemas 1–3 têm estatuto condicional explícito; `H_Tak` fica `[OPEN]`; «nenhum contraexemplo construído» não é tomado como prova (l.157). Frases a ajustar (não são promoções): (i) «o andar II∞» e «menor degrau publicável» (ver B8); (ii) §0 l.5 «**deve** usar uma tripla torcida»: Connes–Moscovici (lido; Def. 3.1: `Da−σ(a)D` limitado, σ∈Aut(A); exemplos tipo III da geometria transversa de folheações, Lemas 2.1–2.2) mostra que a torção **permite** exemplos tipo III; que seja a única formulação é escolha do Kimi, `[DECLARADO]`; (iii) «em exemplos modulares ela está ligada ao peso» (§2.1): o que Connes–Moscovici dizem (Obs. 2.4) é que o estado canônico é uma `σ⁻¹`-traço cujo grupo modular tem σ como continuação analítica em `t=−i`; «peso» é leitura do Kimi `[DECLARADO]`.

### B12. Erratas R2, R3, REV0, REV1 e hashes

Script `scripts_k05_mgh\hashes_k05_mgh.py` → `hashes_k05_mgh_saida.json`. **Todos os hashes declarados conferem** [REAL]:

| arquivo | sha256 calculado | declarado |
|---|---|---|
| `K05\MONTAGEM_GH\REV0\GH_III1_R2.md` | `08d43701e8e843b76ff7b88fb3ba20573f56f3327a6706737c6f7b83f68e62e6` | R2: «GH anterior, em REV0» ✓ |
| `K05\MONTAGEM_GH\REV1\GH_III1_R2.md` | `dff5a66c167fab789a8781f53429faab44600218bae82616fd130a1e0bda5b59` | R2: «GH corrigido»; R3: «GH anterior, em REV1» ✓ |
| `GH_III1_R2.md` (atual) | `0f5e367db38f68c3aa3ac15e19cb10ea8d557a5f7c2d24ac88b0bf25edff9745` | R3 ✓; também em `VALIDACAO_K05.json` ✓ |
| `MONTAGEM_3MAIS1_R2.md` | `3eeb6c56ffc8ad336505e1adc908292b6d0305e90512bf602910650baa692dbb` | R2 e R3 («inalterado») ✓; `VALIDACAO_K05.json` ✓ |
| `K02\candidatas\GH_III1.lean` | `8b56968adeaeaeef6a373ed2f0ddd53ada78ced5aebec35f63a001df653e4a10` | R2, R3, §9 e `ARQUIVO_GH_III1_OCA.md` ✓ |
| `ERRATA_GH_III1_R2.md` / `_R3.md` | `52d61dd0…` / `c71dd5b8…` | `VALIDACAO_K05.json` ✓ |

Conteúdo das erratas (diff REV0→REV1→atual): **R2 está certa** nos dois pontos (GH-R sai do mesmo pacote `C¹`, Remark 3.7 + Prop. 2.14, `C=C'=1`; e a obstrução por Sakai–Tomiyama no lugar da «prova» do REV0 que usava `μ(E(y))=τ(y)` sem `τ∘E=τ`, conferida no REV0 l.140). **R3 está certa** (precisão sobre extensões individuais). Nit: R3 diz alterar «somente» as linhas 148–150 e 165; o `diff` mostra também uma **linha nova na §10 (l.186, Blackadar)**, não mencionada. `REV0`/`REV1` preservam as versões anteriores sem edição.

## 4. COBERTURA (seções B e C da ordem)

| pedido | veio? |
|---|---|
| B1 corrigir o rótulo ímpar×ímpar | sim (§2), certo |
| B2 identificação explícita 4 círculos = T⁴ com J e orientação; finitude e Poincaré (4,0); efeito do escalonamento | sim; **`J`, `D`, `χ`, KO certos; orientação com constante errada**; Poincaré/finitude sem teorema citado que as prove |
| B3 estatuto de (1,3) | sim, certo |
| B3 LISTA de axiomas lorentzianos, origem e o que fica aberto | sim (L1–L10), **com as três omissões de §A6** |
| C1 arquivar `GH_III1.lean` com a nota | sim (`ARQUIVO_GH_III1_OCA.md`; hash confere; arquivo original intacto) |
| C2 Hekkelman, Connes–Moscovici; Kaad–Kyed não toca o «qGH=GH comutativo» | sim, certo (Kaad–Kyed trata operador-sistemas afins sobre bolas ℓ^p, não `C(X)`) |
| C3 o degrau II∞ (convergência dos truncamentos da casa no núcleo; o que desce, o que não desce; três lemas; onde quebra) | **parcial**: três lemas com estatuto e a quebra dita; **mas** nenhum truncamento concreto da casa em `M̂` é tratado, e o conteúdo é independente do tipo (B8) |
| arquivos a entregar (`MONTAGEM_3MAIS1_R2.md`, `GH_III1_R2.md`) | presentes; hashes conferem |

## 5. RESSALVAS QUE EXIGEM CORREÇÃO ANTES DE USAR O TEXTO

1. **`MONTAGEM_3MAIS1_R2.md` §3.3, l.87–91 (e §0 l.5; `ENTREGA_K05.md` l.5 «com … orientação»):** trocar `−1/18` por `−1/24`; reescrever «a constante resulta de r₂=i, r₃=3, r₄=6i de D–D (35)–(36)» como «D–D (36) conta ν=½(n−1)n termos em vez de C(n₁+n₂,n₁); as constantes corretas são r₂=2i, r₃=3, r₄=4i; soma shuffle = 24λ⁴Γ₁Γ₂Γ₃Γ₄». Consulta: `revisor_montagem.py`, blocos `d_*`; D–D p.15–16 (imagens).
2. **`MONTAGEM_3MAIS1_R2.md` §7 (l.143–160):** acrescentar (i) item do tipo/traço (III₁, II∞, torção); (ii) item do elo Euclides→Lorentz (artigo l.1803–1816); (iii) em L10 citar Connes 2008 (arXiv:0810.2088: cinco primeiros axiomas, álgebra comutativa) e reordenar os «bloqueios centrais» (Poincaré e realidade não entram na reconstrução riemanniana). Consulta: `ax:lorentz` l.523–530, l.642–650, l.2224–2227; Connes 0810.2088 resumo e sumário.
3. **`MONTAGEM_3MAIS1_R2.md` §4, l.105–109:** nomear o que de fato sustenta finitude e Poincaré em T⁴ (Connes 1996 afirma na Obs. 4; GVF só por sumário; conferido aqui por Künneth + forma de cunha). Não é erro; é o estatuto `[KNOWN, a conferir]` que precisa dizer onde.
4. **`GH_III1_R2.md` §0 l.9, §6 (Lemas 1–2), §8 (l.163–164):** dizer explicitamente que os Lemas 1 e 2 são independentes do tipo e que `H_Tak` (Lema 3a) reduz-se à hipótese `C¹` aplicada a `π(M)`; o «degrau II∞» não é um teorema de convergência em `M̂`. Reescrever o rótulo «menor degrau publicável».
5. **`GH_III1_R2.md` §0 l.5:** «deve usar uma tripla torcida» → «pode usar (moldura: Connes–Moscovici)».
6. **`ERRATA_GH_III1_R3.md`:** registrar a linha nova da §10 (Blackadar).

## 6. O que não consegui conferir

- Blackadar, *Operator Algebras*, Cor. III.2.1.10 (livro) — conteúdo coerente e padrão, **não conferido na fonte**.
- Takesaki 1973 (Acta Math. 131) e Connes–Takesaki 1977 (Tohoku 29): só metadados (Crossref); a bidualidade, `τ∘θ_s=e^{−s}τ` e «`M̂` é II∞ fator» são padrão mas **não abertos**.
- GVF 2001 (capítulos «Spectral Triples» e «Connes' Spin Manifold Theorem»): livro, só sumário.
- Connes–van Suijlekom 2021 (arXiv:2004.14115): só metadados; Leimbach–vS 2302.07877: resumo e sumário, não as provas; Connes–Moscovici: lido, mas volume/páginas (Aspects Math. E38, 57–71) não confirmados.
- Connes 2008/2013 (0810.2088): só resumo e sumário (o teorema de reconstrução em si não foi lido; o periódico, J. Noncommut. Geom. 2013, não conferido).
- Literatura lorentziana citada por BBB/vdD (Strohmaier, Paschke–Sitarz, Franco–Eckstein, Moretti): não consultada.
- Se existe errata publicada de D–D (2011) para a constante ν; `ch` iso `K⁰(T⁴)≅Λ^{par}(ℤ⁴)` usado como fato padrão.
- Nenhum Lean foi pedido, compilado ou lido além do `grep` de ausência.

## 7. O que examinei (para o Mapa; o registro é da gerência)

- **Entrega do Kimi:** `MONTAGEM_3MAIS1_R2.md`, `GH_III1_R2.md`, `MONTAGEM_3MAIS1.md` (original, l.80–82), `ENTREGA_K05.md`, `VALIDACAO_K05.json` (hashes), `REGISTRO_MAPA_K05.json` (caminhos), `K05\MONTAGEM_GH\{ERRATA_GH_III1_R2,ERRATA_GH_III1_R3,ARQUIVO_GH_III1_OCA}.md`, `REV0\` e `REV1\GH_III1_R2.md`, `K02\candidatas\GH_III1.lean` (só hash), `ORDEM_K05_matematica_rodada_2.md` (B, C), `REVISAO_K02.md`.
- **Artigo:** `A Ponte Einstein Cartan Miguel.tex` l.515–545, 638–660, 953–962, 1006–1075, 1268–1276, 1794–1830, 1920–1950, 2218–2258.
- **Literatura (arXiv, lida em `refs_dl\`):** math/0011063 (Rieffel, Prop. 4.7, 4.8, Ap. 1), 2005.08544 (van Suijlekom, Def. 1–2, Prop. 4, Teo. 5, Lemas 9–12, Prop. 13), 2212.10874 (Kaad–Kyed, Teo. A, Remarks 3.6–3.7), 2205.06043v1 (Prop. 2.14), 0706.3463 (Haagerup–Musat, Lema 2.11), 2111.13865 (Hekkelman, resumo, Teo. 3.8), 2302.07877 (Leimbach–vS, resumo e sumário), math/0609703 (Connes–Moscovici, Def. 3.1, Lemas 2.1–2.2, Obs. 2.4), hep-th/9603053 (Connes 1996, axiomas 1–7 e primos, Teorema e Obs. 4), 0810.2088 (Connes 2008, resumo e sumário), 1011.4456 (D–D, texto integral e págs. 12, 14–16 como imagem), 1505.01939 (vdD, Def. 2.2, eq. (1), Def. 4.2, Prop. 4.3, Obs. 6.4), 1611.07062 (BBB, Tabela 3, §3, §5).
- **Consultas:** `rotas.py consultar` com `Rieffel`, `triplas`, `Hausdorff`, `Krein`, `Dossena`, `Suijlekom`, `Tomiyama`, `Toeplitz`, `toro`; `grep` do kernel `TGLExt` e do `kernel_bancada`; `grep` do inventário; `buscar.py` (`Rieffel`, `Krein`); arXiv API e Crossref API (metadados).
- **Meus scripts** em `revisao\scripts_k05_mgh\`: `revisor_montagem.py` (+ `revisor_montagem_saida.json`), `revisor_lema1.py` (+ `revisor_lema1_saida.txt`), `hashes_k05_mgh.py` (+ `hashes_k05_mgh_saida.json`), `arxiv_meta.py` (+ `arxiv_meta_saida.json`), `crossref_meta.py` (+ `crossref_meta_saida.json`), `refs_dl\` (PDFs e `.txt`, dados não confiáveis).

## 8. Limites desta revisão

O erro da constante (A1) e a unimodularidade em T⁴ (A2) são cálculos meus, sem formalização e sem terceira leitura; o primeiro é reproduzível por `revisor_montagem.py` (24 termos, matrizes 4×4) e independe de convenção, porque cada termo do shuffle iterado reduz-se a `±Γ_{τ(1)}…Γ_{τ(4)}`. A leitura de «dist_QGH domina dist_GH» (B8) vem do texto de Kaad–Kyed §2 e não foi reverificada em Rieffel. Nada foi aberto de dado observado; nenhuma estatística foi calculada.
