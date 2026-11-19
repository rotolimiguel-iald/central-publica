# K02 — Montagem 3+1 por produtos de triplas espectrais

## 1. Enunciado de origem e separação obrigatória

**Fonte euclidiana.** `A Ponte Einstein Cartan Miguel.tex`, linhas 1922–1932: a tripla-limite é `(C∞(S¹), L²(S¹), −iβ^(-1/2)d/dx)` e “a montagem 3+1 segue por produtos”. [A Ponte Einstein Cartan Miguel](kimi-cite://md-line?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2FA%20Ponte%20Einstein%20Cartan%20Miguel.tex&line=1922 "citation")

**Fonte lorentziana.** Linhas 523–530: `ax:lorentz` é explicitamente **ABERTO**, pedindo uma extensão lorentziana dos axiomas de Connes; linhas 533–543: a reconstrução `(M^{1,3},g,Γ_LC+K)` ocorre **se (H)**. [A Ponte Einstein Cartan Miguel](kimi-cite://md-line?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2FA%20Ponte%20Einstein%20Cartan%20Miguel.tex&line=523 "citation")

**[DECLARADO — veredito]** A montagem **euclidiana (4,0)** por quatro círculos é de livro, com as duas verificações suplementares de finitude e dualidade de Poincaré explicitadas abaixo. A assinatura **lorentziana (1,3)** não segue do teorema euclidiano de produtos e permanece **[INPUT (H)/OPEN]**. “KO-dimensão 4” não é “assinatura (1,3)”.

## 2. Aferição na ordem da casa

**Consultas [REAL].**

1. `rotas.py consultar "montagem 3+1 produto triplas espectrais KO dimensao"`: 0; `consultar "triplas"`: apenas `cadeia.preparacao_v412`, que repete que não havia rota própria; cabeça `62342a0adf344cf5`.
2. `buscar.py "tripla espectral|spectral triple|KO.dimens|Gromov.Hausdorff|Rieffel|Suijlekom" --lista`: 102 arquivos no filtro amplo; aparecem o artigo e as duas sombras, não um módulo de produto de triplas.
3. Inventário `.md/.json`: nenhuma entrada `SpectralTriple`, KO-dimensão ou produto par×ímpar.
4. Kernel e mathlib: busca por `SpectralTriple`, `TriplaEspectral`, `KO.dim`, `Gromov`, `Rieffel` no kernel só encontra menções ontológicas em `Caminho.lean` e `Vida.lean`, não tipos geométricos.
5. Sombra `tgl three locks v1 20260609 230529.json`: Weyl `0,982844…, 0,9944142161`; erros relativos de comutadores `1,13266×10⁻³ → 1,86785×10⁻⁵`; `L3_ratios` `0,9772114286 → 0,9971059208`. Lidos por `K02/medir_sombra.py`. [tgl three locks v1 20260609 230529](kimi-cite://text?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2Ftgl%20three%20locks%20v1%2020260609%20230529.json&text=%22L2b_weyl_dims%22 "citation")

**Classificação [DECLARADO a partir das consultas].**

- **EXISTE E ESTÁ LIGADO:** a testemunha numérica da tripla de `S¹` e os números da sombra; a face algébrica `ZMod`/paridade usada na candidata.
- **EXISTE NA BANCADA MAS NÃO ESTÁ LIGADO:** nenhum módulo de produto foi localizado; não se atribui fiação inexistente.
- **SABIDO POR REFERÊNCIA:** produto de triplas reais de Vanhecke e Dąbrowski–Dossena, os axiomas de Connes e a tripla canônica do círculo.
- **AUSENTE no recorte consultado:** a montagem formal completa de quatro fatores com finitude e dualidade de Poincaré, e qualquer teorema lorentziano análogo.

## 3. O que a mathlib da toolchain contém

A toolchain é `leanprover/lean4:v4.31.0`.

- `ZMod 8` e sua aritmética decidível, usados para a sombra KO mod 8.
- Infraestrutura de anéis/paridade e provas decidíveis por `decide`, usadas para os 64 pares de KO-dimensão.
- `Mathlib.Topology.MetricSpace.GromovHausdorff` existe, mas não contém triplas espectrais.

**Não localizado no checkout:** uma estrutura `SpectralTriple`, real structure `J`, grading `χ`, teorema de produto par×ímpar, KO-dimensão, axiomas de Connes ou reconstrução lorentziana. A candidata, portanto, formaliza somente a aritmética finita; a geometria entra por citação.

## 4. Produto: fórmulas, paridade e sinais

Referência principal: Dąbrowski–Dossena 2011, *Product of real spectral triples*, *Int. J. Geom. Methods Mod. Phys.* 8, 1833–1848, DOI `10.1142/S021988781100597X`, arXiv:1011.4456, §§2, 4 e 5; completa Vanhecke 1999, *Lett. Math. Phys.* 50, 157–162, arXiv:math-ph/9902029. [KNOWN, a conferir, texto integral consultado](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fpdf%2F1011.4456 "citation")

**[KNOWN, a conferir — construções]**

- **Par×par:** `H=H₁⊗H₂`, `A=A₁⊗A₂`, `D=D₁⊗1+χ₁⊗D₂`, `χ=χ₁⊗χ₂`, `J=J₁⊗J₂`. Também `D̃=D₁⊗χ₂+1⊗D₂`, unitariamente equivalente no caso sem bordo.
- **Par×ímpar (par primeiro):** a mesma fórmula `D=D₁⊗1+χ₁⊗D₂`; o produto é **ímpar**.
- **Ímpar×par (par segundo):** `D̃=D₁⊗χ₂+1⊗D₂`; o produto é **ímpar**.
- **Ímpar×ímpar:** requer duplicação: `H=(H₁⊗H₂)⊗ℂ²`, `D=D₁⊗1⊗σ₁+1⊗D₂⊗σ₂`, `χ=1⊗1⊗σ₃`, `J±=J₁⊗J₂⊗M±K`; o produto é **par**.

**[KNOWN, a conferir — sinais KO]** `J²=ε`, `JD=ε′DJ`, e, no caso par, `Jχ=ε″χJ`:

| n mod 8 | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ε | +1 | +1 | −1 | −1 | −1 | −1 | +1 | +1 |
| ε′ | +1 | −1 | +1 | +1 | +1 | −1 | +1 | +1 |
| ε″ | +1 | — | −1 | — | +1 | — | −1 | — |

**[KNOWN, a conferir]** A dimensão métrica soma em `ℤ`; a KO-dimensão soma em `ℤ/8` para as estruturas reais escolhidas. Dąbrowski–Dossena também tratam estruturas “exóticas”, de modo que a escolha de `J` deve ser registrada, não presumida.

## 5. Cada axioma de Connes para o produto

A numeração segue a apresentação usada por Dąbrowski–Dossena, que remete a Connes 1996, *Commun. Math. Phys.* 182, 155–176, e Connes–Marcolli 2008, *Noncommutative Geometry, Quantum Fields and Motives*, AMS Colloquium 55. [KNOWN, a conferir; a análise de preservação está em D–D §5](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fpdf%2F1011.4456 "citation")

| Axioma | Produto: estatuto e rota |
|---|---|
| 1. Dimensão espectral | **[KNOWN, a conferir]** `D²` tem autovalores dados pela soma dos autovalores de `D₁²` e `D₂²`; logo a dimensão métrica soma, `n=n₁+n₂`. |
| 2. Regularidade | **[KNOWN, a conferir sob as hipóteses do teorema]** o argumento por operadores diferenciais generalizados cobre par×par e se estende às outras paridades; exige regularidade dos fatores. |
| 3. Finitude/continuidade absoluta | **[OPEN como verificação separada]** D–D §5 não fecha este item. Exigir a estimativa de somabilidade e a continuidade do funcional associado; não inferir apenas da soma formal de dimensões. |
| 4. Realidade (ordem zero incluída) | **[KNOWN, a conferir]** `J=J₁⊗J₂` nos casos sem duplicação e a construção explícita em ímpar×ímpar; ordem zero segue do cálculo tensorial. |
| 5. Primeira ordem | **[KNOWN, a conferir]** o cálculo de `[[D,a],Jb*J⁻¹]=0` é feito por D–D para par×par e par×ímpar e com Pauli para ímpar×ímpar. |
| 6. Orientação | **[KNOWN, a conferir]** o ciclo de Hochschild usa o produto shuffle, com normalização dependente da paridade; a prova de D–D §5 é explícita. |
| 7. Dualidade de Poincaré | **[OPEN como verificação separada]** não é demonstrada por D–D §5. Deve vir de K-homologia/produto de Kasparov ou ser incluída como hipótese adicional. |

**[DECLARADO]** A frase “produtos de triplas satisfazem os axiomas” é correta somente depois de fixar as hipóteses dos itens 3 e 7. O teorema de produto citado não é licença para omiti-los.

## 6. Montagem euclidiana (4,0), passo a passo

**Entradas [DECLARADO]:** quatro cópias da tripla canônica do círculo, com `J` e orientação escolhidos e compatibilidade dos itens 3 e 7 verificadas.

1. **[KNOWN, a conferir]** `S¹` tem dimensão métrica 1 e KO-dimensão 1 (ímpar).
2. **[KNOWN, a conferir]** `S¹×S¹`: ímpar×ímpar exige duplicação; resultado par, métrica 2, KO 2.
3. **[KNOWN, a conferir]** `T²×S¹`: par×ímpar; resultado ímpar, métrica 3, KO 3.
4. **[KNOWN, a conferir]** `T³×S¹`: par×ímpar; resultado par, métrica 4, KO 4.
5. **[DERIVED]** Em KO 4, `(ε,ε′,ε″)=(−1,+1,+1)` pela tabela. Isso é realidade euclidiana, não assinatura lorentziana.
6. **[OPEN]** Anexar as provas de finitude e dualidade de Poincaré para o produto iterado; sem isso, a montagem fica condicionada.

**[REAL na sombra, escopo limitado]** A testemunha de Weyl final `0,9944142161` e os erros decrescentes sustentam a aproximação numérica da tripla-base de `S¹`; não são prova dos sete axiomas nem da montagem 4D. [tgl three locks v1 20260609 230529](kimi-cite://text?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2Ftgl%20three%20locks%20v1%2020260609%20230529.json&text=%22L2c_comm_rel_errs%22 "citation")

## 7. Assinatura (1,3): o que permanece hipótese

**[INPUT (H), lido nas linhas 523–543]** Deve-se fornecer uma extensão lorentziana dos axiomas com regularidade, dimensão espectral 4, orientação, realidade e causalidade via `Π_irr`, capaz de reconstruir variedade suave.

**[OPEN]** O produto euclidiano não resolve: resolvente compacta/domínios do Dirac, métrica indefinida/Krein, realidade apropriada, causalidade e reconstrução de variedade lorentziana. O próprio artigo diz que não há teoria completa aceita.

**[DECLARADO — KO]** Não se deve escrever `1+3=4` e apresentar isso como KO-dimensão lorentziana. Se uma convenção pseudo-euclidiana usar `p−q`, então `(1,3)` sugere `−2≡6 (mod 8)`, mas essa é uma escolha de convenção, não um teorema de montagem do artigo. A candidata Lean deliberadamente não atribui KO a `(1,3)`.

## 8. Candidata e log real

Arquivo: `K02/candidatas/MONTAGEM_3MAIS1.lean`; log: `K02/sandbox/logs/MONTAGEM_3MAIS1.log`.

Compilação final real: `rc=0`, Lean `4.31.0`.

- `parity_koAdd`: 64 casos de paridade da soma KO;
- `product_even_odd`, `product_odd_even`, `product_odd_odd`;
- `signs_KO4`, `signs_KO2`;
- `ko_euclidean_four_zero`, `ko_sum_mod_eight`.

O log de `parity_koAdd` contém `[propext, Classical.choice, Quot.sound]`; os demais usam subconjunto. Nenhum `sorry`, nenhum axioma extra e nenhuma afirmação formal de tripla espectral ou de assinatura lorentziana.
