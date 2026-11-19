# K02 — Extensão de Gromov–Hausdorff a III₁

## 1. Enunciado de origem e estatuto

**Fonte.** `A Ponte Einstein Cartan Miguel.tex`, linhas 1821–1826: a extensão GH a III₁ é “provada na sombra; conjecturada no contínuo via Rieffel”; linhas 1934–1942: a cascata é truncamento espectral e “no caso comutativo, qGH = GH (Rieffel)”; linhas 2250–2254 repete a conjectura. [A Ponte Einstein Cartan Miguel](kimi-cite://md-line?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2FA%20Ponte%20Einstein%20Cartan%20Miguel.tex&line=1821 "citation"), [mesmo artigo, Fecho 3](kimi-cite://md-line?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2FA%20Ponte%20Einstein%20Cartan%20Miguel.tex&line=1934 "citation")

**[DECLARADO — veredito]** A extensão é **[CONJECTURE]**. Há dois alvos diferentes, que o artigo não pode contrair:

- **(GH-R)** convergência em **qGH de Rieffel**, definida por pontes/Lip-normas compatíveis;
- **(GH-S)** convergência da **GH clássica dos espaços de estados**, munidos da distância de Connes.

A segunda não implica automaticamente a primeira; Kaad–Kyed provou que as duas distâncias não são equivalentes em geral. A frase “qGH = GH” não é aceita como identidade universal. [KNOWN, a conferir, Kaad–Kyed 2023, *Math. Phys. Anal. Geom.* 26, 8, DOI `10.1007/s11040-023-09451-y`, arXiv:2212.10874](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2212.10874v2 "citation")

## 2. Enunciado tipado da conjectura

**[CONJECTURE — formulação candidata]** Seja `(A,H,D)` uma tripla espectral unitária cujo fechamento de von Neumann é um fator III₁ e seja `L_D(a)=‖[D,a]‖` uma Lip-norma: domínio denso, núcleo `ℂ1`, condição de Leibniz (ou variante declarada), e topologia induzida em `S(A)` igual à fraca-*. Sejam `P_M` projeções espectrais de `D` com `P_M→1` fortemente, `E_M=P_M A P_M`, `D_M=P_MDP_M` e `L_M` as seminormas induzidas. Então:

1. **GH-R:** `dist_Q((E_M,L_M),(A,L_D)) → 0` em qGH de Rieffel;
2. **GH-S:** `(S(E_M),d_M) → (S(A),d_D)` em GH clássica de espaços métricos compactos.

**Hipóteses que não podem ser omitidas [DECLARADO].** Finitude de `L_M` nos estados, Leibniz/quasi-Leibniz uniforme, compatibilidade das topologias fracas-*, existência de aproximações de ordem `C¹` e escolha de qGH. A mera convergência `P_M→1` e a III₁-idade não bastam.

A candidata Lean `TypeIII1GHConjecture` registra `IsTypeIII1`, `IsSpectralTruncationOf`, `qghDist`, `Tendsto ... atTop (𝓝 0)` como parâmetros/tipos, sem afirmar ter construído qGH.

## 3. Aferição na ordem da casa

**Consultas [REAL].**

1. `rotas.py consultar "Gromov Hausdorff III1 truncamento espectral Rieffel Connes van Suijlekom"`: 0; `consultar "Gromov"`: 0; cabeça `62342a0adf344cf5`.
2. `buscar.py` para `tripla espectral|spectral triple|KO.dimens|Gromov.Hausdorff|Rieffel|Suijlekom`: 102 arquivos; artigo/sombras e bibliografia, nenhum fecho III₁.
3. Inventário `.md/.json`: nenhum módulo Rieffel/qGH/GH; `H_modular_equals_geometric` e Bisognano–Wichmann continuam OPEN.
4. Kernel: nenhum `Gromov`, `Rieffel`, `qGH`, `ghDist` ou `SpectralTriple` no recorte consultado.
5. Atlas: o “ACHADO 08” lembra que III₁ não tem estado tracial; `Face C` mantém a extensão GH como OPEN.
6. Sombra `tgl_continuum_v1.py` e `tgl_three_locks_v1.py`, lidas por `K02/medir_sombra.py`.

**Classificação [DECLARADO a partir das consultas].**

- **EXISTE E ESTÁ LIGADO:** a GH clássica da mathlib e as testemunhas numéricas da sombra finita.
- **EXISTE NA BANCADA MAS NÃO ESTÁ LIGADO:** nenhuma prova pronta de qGH/III₁ foi encontrada; as sombras são fiação numérica, não ligação formal ao contínuo.
- **SABIDO POR REFERÊNCIA:** Rieffel, Connes–van Suijlekom, van Suijlekom e Leimbach–van Suijlekom; Connes–Moscovici para triplas tipo III.
- **AUSENTE no recorte consultado:** uma Lip-norma III₁ com as topologias verificadas e a convergência qGH/estados para os truncamentos da casa.

## 4. O que a mathlib da toolchain contém

`Mathlib.Topology.MetricSpace.GromovHausdorff`, na toolchain `v4.31.0`, contém:

- `GromovHausdorff.GHSpace`, quociente de compactos não vazios por isometria;
- `GromovHausdorff.toGHSpace`;
- `GromovHausdorff.ghDist`, a distância entre compactos não vazios;
- `dist_ghDist`, `ghDist_le_hausdorffDist`, `ghDist_eq_hausdorffDist` e `hausdorffDist_optimal`;
- `GromovHausdorffRealized` e critérios de compacidade.

Esses objetos são **GH clássica**, não qGH de Rieffel nem GH de espaços de estados não comutativos. O checkout não forneceu `QuantumMetricSpace`, `OrderUnit`, `OperatorSystem` ou `SpectralTriple` prontos para a conjectura. [GromovHausdorff](kimi-cite://md-line?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2FN%C3%B3s%2Ftgl_kernel%2F.lake%2Fpackages%2Fmathlib%2FMathlib%2FTopology%2FMetricSpace%2FGromovHausdorff.lean&line=61 "citation")

## 5. O que é teorema publicado

1. **Rieffel 2004.** Constrói espaços métricos quânticos compactos e qGH; o exemplo principal é continuidade de toros quânticos nos parâmetros. *Mem. Amer. Math. Soc.* 168(796), 1–65, DOI `10.1090/memo/0796`, arXiv:math/0011063. Não é um teorema universal de truncamentos III₁ nem de igualdade qGH=GH. [KNOWN, a conferir, AMS](kimi-cite://web?url=https%3A%2F%2Fams.org%2Fbooks%2Fmemo%2F0796 "citation")
2. **Connes–van Suijlekom 2021.** Formaliza truncamentos espectrais por sistemas operadores `PAP` e estuda círculo/Toeplitz, positividade, estados e distância de Connes. *Commun. Math. Phys.* 383, 2021–2067, arXiv:2004.14115. É a moldura, não a prova III₁. [KNOWN, a conferir](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2004.14115 "citation")
3. **van Suijlekom 2021.** Dá condições para convergência GH dos espaços de estados de truncamentos, com círculo, Fourier finito e matrizes→esfera. *J. Geom. Phys.* 162, 104075, DOI `10.1016/j.geomphys.2020.104075`, arXiv:2005.08544. O alvo é GH-S. [KNOWN, a conferir](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2005.08544 "citation")
4. **Leimbach–van Suijlekom 2024.** Prova convergência dos espaços de estados de truncamentos de toros à medidas de Borel no toro com Monge–Kantorovich, usando multiplicadores de Schur/Fourier e núcleo de Fejér espectral. *Adv. Math.* 439, 109496, DOI `10.1016/j.aim.2024.109496`, arXiv:2302.07877. [KNOWN, a conferir](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2302.07877 "citation")
5. **Connes–Moscovici 2008.** *Type III and spectral triples*, em *Traces in Number Theory, Geometry and Quantum Fields*, Aspects Math. E38, 57–71, arXiv:math/0609703. Mostra que triplas tipo III são um campo legítimo; não fornece a convergência GH aqui conjecturada. [Connes–Moscovici 2008, arXiv:math/0609703](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2Fmath%2F0609703 "citation")

## 6. O que a sombra da casa realmente verificou

**[REAL, lido e recalculado por `K02/medir_sombra.py`]**

- L3: razões `0,9772114286441925 → 0,997105920823951`; erros `1−r`: `0,0227885713558075 → 0,0028940791760490`. Os fatores sucessivos de redução são `1,98168`, `1,99108`, `1,99564`, compatíveis com duplicação de `M` e erro `O(1/M)` nesses quatro níveis, sem prova assintótica. [tgl three locks v1 20260609 230529](kimi-cite://text?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2Ftgl%20three%20locks%20v1%2020260609%20230529.json&text=%22L3_ratios%22 "citation")
- C1, três execuções: `h` de `0,0493592780656549` a `9,64048399719919×10⁻⁵`; taxa `0,5000000000000054`, `R²=1`.
- C2: distância cruzada final `0,0005266633–0,0007592851` e KS final `0,0180223–0,0218775`.
- C3: erro de identidade `4,96×10⁻¹⁶`, `1,97×10⁻¹⁵`, `1,23×10⁻¹⁵`; menores autovalores relativos positivos `0,10682–0,16517`. [tgl continuum v1 20260609 225321](kimi-cite://text?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2Ftgl%20continuum%20v1%2020260609%20225321.json&text=%22C3_identity_err%22 "citation")

**[DECLARADO — escopo]** São testemunhas finitas de uma métrica/proxy, não prova de que a métrica seja qGH de Rieffel, nem de topologia fraca-* em III₁, nem de convergência para uma álgebra III₁. Hiperfinitude densa não implica convergência métrica automática.

## 7. Obstruções específicas em III₁ e rota de prova

1. **Sem traço [KNOWN, a conferir; OPEN].** Não há traço normal semifinito fiel em III₁. A construção `L_D` e os mapas de suavização/Fejér devem usar um peso, uma estrutura KMS/twisted ou outra Lip-norma; o traço não pode ser chamado implicitamente.
2. **Qual seminorma [OPEN].** É preciso provar núcleo `ℂ1`, Leibniz/quasi-Leibniz, finitude e densidade. `a↦‖[D,a]‖` é a candidata natural, mas essas propriedades não vêm da III₁-idade.
3. **Qual topologia [OPEN].** A distância de Connes pode ser infinita ou metrizar topologia distinta da fraca-*; Rieffel exige coincidência topológica. O espaço de estados é fraco-* compacto no caso unitário, mas isso não garante a Lip-norma.
4. **Qual distância [OPEN].** GH-S e GH-R são distintas. É necessário declarar qual se prova e, se ambas, construir a ponte adicional.
5. **Truncamento/aliasing [DECLARADO].** A lição do próprio artigo, linhas 1944–1949, mostra que a grade errada produz termo de bordo ampliado por `M`; truncamento de Toeplitz é exigido.

**Rota candidata [DECLARADO, passos ainda abertos].**

1. Fixar GH-R e/ou GH-S e escrever todos os axiomas da Lip-norma III₁.
2. Construir `R_M:A→E_M` e `S_M:E_M→A` positivos/unitais com `R_M S_M=id` e `S_M R_M` dado por núcleo apropriado.
3. Provar estimativas `C¹` uniformes: `L_M(R_Ma)≤C_M L(a)`, `L(S_Mb)≤C′_M L_M(b)`, e `‖S_M R_M a−a‖≤ε_M L(a)`, com `C_M,C′_M→1`, `ε_M→0`.
4. Usar o teorema de van Suijlekom para GH-S e uma ponte explícita para GH-R.
5. Verificar que `P_M→1` preserva a topologia fraca-* e que os tipos passam ao limite; só então concluir a conjectura.

## 8. Possível contraexemplo

**[DECLARADO — critério, não exemplo construído]** Uma tripla III₁ com `P_M→1` para a qual `d_M` permanece infinita entre estados distintos, ou cuja topologia `d_D` não seja a fraca-*, impediria a formulação GH-S. Se, apesar disso, as distâncias forem finitas mas `dist_Q` ficar separada de zero por escolha incompatível de Lip-normas, há contraexemplo a GH-R. A grade com aliasing mencionada pelo artigo é uma candidata natural a contraexemplo à **estratégia ingênua**, não ainda um contraexemplo à conjectura bem posta.

## 9. Candidata e log real

Arquivo: `K02/candidatas/GH_III1.lean`; log: `K02/sandbox/logs/GH_III1.log`.

Compilação final real: `rc=0`, Lean `4.31.0`.

- `classical_gh_self`: `ghDist X X = 0`, somente GH clássica;
- `QuantumMetricSpace`: recorte com seminorma e Leibniz, sem alegação de cobrir todos os axiomas de Rieffel;
- `TypeIII1GHConjecture`: enunciado tipado;
- `typeIII1_of_named_hypothesis`: conclui apenas a partir de `H_GH_III1`, `H_limit`, `H_truncations` nomeadas.

Ambos os `#print axioms` contêm somente `[propext, Classical.choice, Quot.sound]`. Nenhum `sorry`, nenhuma qGH importada indevidamente e nenhum termo incondicional III₁.
