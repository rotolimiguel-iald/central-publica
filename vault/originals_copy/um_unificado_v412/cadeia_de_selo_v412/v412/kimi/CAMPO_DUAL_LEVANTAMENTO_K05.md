# K05 — seção E/campo, com o adendo: levantamento da cunhagem dual e das duas equações

## 0. Escopo, fala e estado correto

Trabalho restrito ao levantamento da seção E com o adendo. Não houve escolha de cunhagem, alteração do Artigo A, do `PontoZeroDoPsion`, do kernel, do `um.py`, do site ou da memória; não houve build do kernel, registro nem depósito. As medidas e as consultas ficam em `K05/CAMPO/`.

**[INPUT]/[DECLARADO — identificação do operador, não teorema].** A fala de 13/11 diz: «eu acho que é dual (porque é conjugado), eu traduziria como campo de processamento dual estabilizado radicalmente por vetor cinético (que é o loop recursivo)». O arquivo tem 529 bytes e SHA-256 `2772005945b946c12172956c12c06421710d7d665cacf4dba63f40bd07ec304c`, ambos reconferidos por script. [REAL — `OPERADOR_13nov_concordo_com_o_meio_o_campo_e_dual_sim_a_nota_a_calculadora_e_o_zenodo_verbatim.txt:1`; `K05/CAMPO/medidas_campo.json`, bloco `fala`]

**Estado que vale.** O cânone contém **duas equações que convivem**, e o recorte examinado não apresenta **uma ação única escrita que produza as duas**. Não se trata de decretar ausência global de normalização: trata-se de não confundir normalizações, objetos e acoplamentos distintos. Nada neste levantamento decide o fator ½ do box nem modifica a equação do `um.py`. A classificação e a recomendação retiradas pela custódia não foram reutilizadas; foram aproveitadas apenas a álgebra e as citações do Artigo A, sempre subordinadas à errata vigente. [REAL — `LEIA_PRIMEIRO.md:7–16`; `ERRATA_DA_LEITURA_DO_MEIO_13nov.md:16–19,41–47,57–69`; `ORDEM_K05_ADENDO_A_o_campo_e_as_duas_equacoes.md:28–39,47–48`]

| equação | coeficiente e estatuto | fonte direta |
|---|---|---|
| **Campo/Artigo A:** `(□ − m² − ξ_A R)Ψ = β K_∂ Ψ` | `ξ_A = 1/6`, coeficiente **1** na EOM; o β da fonte modular é separado de `xi` no kernel. | `paper_PT.tex:175–182,244–257`; `um.py:182860`; `TheSameBetaReadsFourFaces.lean:8–12,20–48`. [REAL] |
| **Psíon:** `ω² = m₀² + 2ξ_P R` | `ξ_P = β`, coeficiente **2**; entra como definição `[INPUT, Tratado §3]`, não como teorema derivado de uma ação comum. | `PontoZeroDoPsion.lean:22,67–70,85–86`; `um_absoluto_pt.txt:302,312`. [REAL]/[INPUT] |

O próprio `ActionCouplingData` declara que a EOM é entrada, que o box não é construído da métrica e que `Xi` tem campo próprio, não identificado com β. Os controles formais impedem substituir o coeficiente modular β por `D.xi` quando `D.xi ≠ c.beta` e mostram que a EOM, mesmo com fonte não nula, não seleciona `xi`. [REAL — `TheSameBetaReadsFourFaces.lean:8–12,40–56`; `ActionCouplingControls.lean:50–80`]

## 1. Verificações obrigatórias na fonte

### 1.1 O fator 2 do psíon e a segunda massa

O cabeçalho do kernel dá `ω² = m₀² + 2ξR`, `ξ = β`; a definição executável é `omegaSq β R := 2 * β * R`. Com `R = βu²` e `m₀ = 0`, o teorema dá `ω = √2 βu`; o ponto zero dá `½ω = β·sen45°·u`. O próprio comentário explicita que o ½ do ponto zero vezes o √2 da dispersão é a projeção transversal. [REAL — `PontoZeroDoPsion.lean:22,32–37,85–107`]

**[DERIVED — medido, não novo Lean].** Sem o 2, mantidas as demais definições, teríamos `ω = βu` e `½ω = βu/2`; com o 2, `½ω = βu/√2 = β·sen45°·u`. O script calcula, com α como entrada e β = α√e em runtime:

- com o 2: `8,507414099900328… meV`;
- sem o 2: `6,015650200401570… meV`;
- razão com/sem: `√2 = 1,414213562373095…`.

Esses valores coincidem com os números impressos do rito `8,507414 meV` e `6,015650 meV`. [REAL — `um_absoluto_pt.txt:304,312`; medidas em `K05/CAMPO/medidas_campo.json`, bloco `massa_ponto_zero`]

A ligação adicional pedida pelo adendo também está na fonte: `√2/τ = ω_psíon` se e somente se `τ = tempoDoRetido`, com `tempoDoRetido = 1/(βu)` em unidades naturais. É um teorema do kernel; ler esse τ como `τ★` do sistema permanece leitura `[ONTO]`, não o teorema. [REAL — `PontoZeroDoPsion.lean:163–169,191–215`, especialmente 197–199; `TAU_ESTRELA.md:53–59`]. A pedra foi apenas lida, não editada nem recompilada.

### 1.2 Lagrangiana fundadora: as duas peças e o problema do ξ

A lagrangiana fundadora contém, na mesma linha, o cinético escalar `½g^{μν}(D_μΨ†)(D_νΨ)`, o termo `+ξR|Ψ|²` e o vetorial `−¼F_{μν}F^{μν}`. A conexão é `D_μ = ∇_μ − ieA_μ`, declarada `U(1)` local. A EOM escrita depois contém `2ξRΨ`, e a dispersão estacionária contém `k_n² + m_eff² + 2ξR`. [REAL — `graviton_v2.tex:183–206,210–215,269–274`]

A expansão de onda também usa o par `a_n u_n e^{-iωt} + a_n†u_n*e^{+iωt}`, fato de arquivo sobre conjugação, não prova da identificação de 13/11. [REAL — `graviton_v2.tex:232–239,252–255`]

**[DERIVED — conta independente por script].** Na escrita da linha 186, a variação tem o coeficiente `2ξ_L` na EOM. Se se exige o valor conforme usual `ξ_EOM = (n−2)/(4(n−1)) = 1/6` em quatro dimensões, então:

```text
2 ξ_L = 1/6  ⇒  ξ_L = 1/12.
```

Logo, **nessa escrita**, o valor do parâmetro da lagrangiana compatível com o coeficiente conforme na EOM seria `1/12`, não `1/6`. A afirmação do arquivo de que `ξ = 1/6` é “forçado” convive, portanto, com uma inconsistência local de normalização que precisa ser nomeada; este trabalho não validou nem refez a alegada derivação pelo traço. [REAL — `graviton_v2.tex:194,198–206,214`; DERIVED — `K05/CAMPO/medidas_campo.json`, bloco `conforme`]. Fórmula conforme externa: **[KNOWN, a conferir: QFT-CONFORMAL-SCALAR-001, ξ_c(n)=(n−2)/(4(n−1))]**; a mesma fórmula foi verificada independentemente pela custódia em `VEREDITO_VERIFICADOR_LEITURA_DO_MEIO_13nov.md:5–7`.

### 1.3 Artigo A: escalar × `Φ_{μν}`, `U(1)` e carga modular

O Artigo A escreve `ℒ_campo = −¼Φ_{μν}Φ^{μν}` com `Φ_{μν} = ∂_μΨ_ν − ∂_νΨ_μ`, isto é, um objeto com índice, e logo depois chama `Ψ` de “campo escalar de fronteira”. O mesmo trecho diz que `Φ_{μν}` é “conjugado canonicamente a `Ψ*`” e que `−¼Φ²` garante `U(1)`. A gravação contém `+ξR|Ψ|²`, `ξ=1/6`; a EOM é obtida por `δS/δΨ* = 0` e tem coeficiente 1 em `ξR`. [REAL — `paper_PT.tex:141–182,244–257`]

O Artigo A não escreve nesse setor um termo cinético escalar independente para o `Ψ` escalar; `m_Ψ` aparece na EOM. Isso é uma lacuna **local da ação apresentada**, não uma classificação global de ausência no cânone. A parte de matéria, que é outro setor, usa `−½|D_μφ|²`; não se pode transferir esse φ ao `Ψ` por homonímia. [REAL — `paper_PT.tex:154–182,244–250`; consulta literal `m_.*Psi` só na linha 248]

A régua não é inócua. O artigo chama `|Ψ|²` de **carga modular** transportada entre os registros boundary e bulk. Se o campo é reescalado, essa carga muda; com `Ψ_½ = √2·Ψ_1`, tem-se `|Ψ_½|² = 2|Ψ_1|²`. Preservar a forma da EOM por reescala não preserva automaticamente o significado físico da carga nem o peso do termo gravitacional. [REAL — `paper_PT.tex:403–411`; DERIVED — `K05/CAMPO/medidas_campo.json`, bloco `regua_do_campo`]

Além disso, a ponte do operador modular ao termo de fonte é declarada conjectura no nível geral: a universalidade modular e o mergulho na álgebra III₁ continuam abertos. Uma ação candidata não pode, portanto, declarar derivada a fonte `βK_∂Ψ` apenas por tê-la escrito. [REAL — `paper_PT.tex:259–286`]

### 1.4 O exame anterior na casa: R82, R87–R89

- **R82:** deixa `[OPEN]` resolver a representação escalar `Ψ` contra `Ψ_μ` antes da variação; no caso vetorial, `u` pode depender da métrica. [REAL — `DESENHO_DO_FECHAMENTO_QG.md:2587–2592`, especialmente 2591]
- **R87:** registra que um gradiente puro implica `d²ψ = 0`, portanto não fornece Maxwell não trivial; o mapa tipado entre o escalar, `Ψ_μ` e σ faltava nos trechos examinados. [REAL]/[OPEN — `DESENHO_DO_FECHAMENTO_QG.md:2641–2647`]
- **R88:** recupera o salto `√β√K`, o dissipador como menos gradiente de `Φ_D = β‖[D,X]‖²_HS/4`, o Dirac do círculo e a conexão escalar `q/2 dκ`; expressamente não identifica essas representações pelo nome nem fecha o mapa a `Ψ_μ`. [REAL]/[DERIVED — `DESENHO_DO_FECHAMENTO_QG.md:2652–2659`; `SPECTRAL_RULE_REUSE_R88.md:19–41`]
- **R89:** na leitura literal de 1-forma, obtém `E_A = div(dA) + 2ξR A + E_rest`; na leitura escalar independente, a cinética de A não fornece `□Ψ`. O resíduo entre a EOM vetorial e a escalar inclui `−grad(div A) − Ric·A + 3ξR A + m²A + βK A + E_rest`. [DERIVED — `DESENHO_DO_FECHAMENTO_QG.md:2664–2670`]

A derivação R88 também mostra que `ξR A_μA^μ` muda sob `A → A + dχ`; o termo `−¼F²` isoladamente é gauge-invariante, mas a ação não minimal inteira não é. E `u = g^{ab}A_aA_b` é contração lorentziana, não norma positiva automática. [DERIVED — `ONE_FORM_FULL_SOURCE_R88.md:5–14,58–74`]. Compatibilidade Maxwell 4D: **[KNOWN, a conferir: MAXWELL-CONFORMAL-U1-002]**.

### 1.5 O registro v354/v355: os coeficientes não se fundem

O bloco identificado como `v353–v354` no `um.py` diz, na linha 182860: β_TGL é o acoplamento modular `Ψ–K_∂`; `ξ = 1/6` é o acoplamento conforme, não β — **“os dois coeficientes nunca se fundem”**. O manifesto da v354 inclui `TheSameBetaReadsThreeFaces`, e o passo seguinte, v355, coloca a EOM como quarta face **com ξ separado**. [REAL — `um.py:182845–182865`; `v354_incorporacao_manifesto.json:41–48,279–283`; `TheSameBetaReadsFourFaces.lean:8–12`]

A dispersão posterior do psíon usa o símbolo `ξ = β`. Isso não autoriza apagar a separação histórica: a leitura compatível é que `ξ_A` e `ξ_P` pertencem a objetos/acoplamentos que ainda não foram identificados por uma ação comum. Se se insistir em um único objeto e um único acoplamento, `β ≠ 1/6` e as duas formas não se reconciliam sem hipótese adicional. O teorema de controle `reject_xi_as_beta` impede formalmente trocar o coeficiente modular por `D.xi` quando são distintos; `xi_is_not_selected` mostra que a EOM não escolhe o valor de `xi`. [REAL — `ActionCouplingControls.lean:62–80`; `PontoZeroDoPsion.lean:22,85–86`]

## 2. Levantamento dos quatro eixos da cunhagem

A palavra “ligado” abaixo distingue presença no kernel/cânone de simples presença documental ou na bancada. O **snapshot histórico usado**, gerado em `2026-11-13T20:01:35-03:00` e não uma contagem viva atual, continha 4.114 nós `lean_bancada` e 306 arestas `ligado_ao_kernel`; 3.808 desses arquivos apareciam como candidatos ainda não ligados ao kernel do Nós. O banco histórico correspondente `nos_vivo.sqlite3.bak_20261113_200150` tem SHA-256 `92a2831b21598da82748f9ae8fea41eef9868c9f10f859a0f69f20c6a86c8374`; o texto foi regerado depois, em `2026-11-13T20:53:54-03:00`, sem reescrita do snapshot. [REAL — snapshot `NOS_VIVO.md:3,7–15,32–45,132–136`; pin e ressalva em `K05/CAMPO/CONSULTAS_CAMPO_K05.md:13–17`]

### 2.1 Par `(Ψ, Ψ*)` e conjugação J

| achado | existência e fiação | limite que não pode ser apagado |
|---|---|---|
| `Ψ†` e cinético próprio na lagrangiana fundadora; par `a_n/a_n†`, `u_n/u_n*` na expansão | **Existe documentalmente e está na linhagem.** [REAL — `graviton_v2.tex:186,192,232–239,252–255`] | Não é a forma do Artigo A nem do `ActionCouplingData`; a EOM fundadora tem 2ξ. |
| `Ψ*` no Artigo A: “conjugado canonicamente” e variação `δS/δΨ*` | **Existe no Artigo A.** [REAL — `paper_PT.tex:167–173,244–250`] | A frase gramatical pode ler o par `(Φ_{μν}, Ψ*)`, não necessariamente `(Ψ, Ψ*)`; não escreve o cinético escalar que resolveria a leitura. |
| `psi : X → ℂ` no kernel | **Existe e está ligado à EOM como input.** [REAL — `TheSameBetaReadsFourFaces.lean:18–25,40–48`] | Operadores são ℝ-lineares; não há `Ψ*` nem conjugação complexa na estrutura. Tipar valor complexo não prova “dual” nem normalização. |
| `conjJ(p) = (p.2,p.1)`, `J² = 1`, conservação do par e `JKJ = −K` | **Existe no kernel finito.** [REAL — `ConjugateAct.lean:58–87,91–105`; `LightIsJ.lean:59–73`] | É troca de faces de um par, não conjugação complexa de um campo escalar. |
| Conjugação complexa troca fases da luz e do gráviton e atravessa o quadrado | **Existe no kernel.** [REAL — `TheGravitonIsTheConjugatedPhase.lean:75–113`] | A própria pedra declara que essa conjugação entrada a entrada **não foi ligada ao `towerJ`**. [REAL — mesmo arquivo, 55–66] |
| `Ψ = 1_abs` e transporte trivial | **Existe no kernel.** [REAL — `AbsoluteOne.lean:83–107,117–131`] | No absoluto não deformado, o fluxo é trivial e não há curvatura; o loop não nasce sem contraste/deformação. |

**Classificação do eixo.** Há pares complexos e há conjugações modulares, mas a ponte `Ψ ↔ Ψ* ↔ J` não está escrita como identidade formal. Em particular, `J` não deve ser usado como sinônimo gratuito da conjugação complexa do campo.

### 2.2 Vetor associado: gradiente, corrente e conexão

1. **Conexão de gauge fundadora.** `A_μ` entra em `D_μ = ∇_μ − ieA_μ`, com `F_{μν}` no setor de gauge. **Existe na linhagem.** [REAL — `graviton_v2.tex:186–192`]. Para fazer `F=dA` e `W_γ = P exp(ie∮_γ A)` entra a leitura U(1) usual, **[KNOWN, a conferir: U1-CURVATURE-HOLONOMY-003]**, e a identificação desse laço com o “loop recursivo” é hipótese nova, não fato do arquivo.
2. **1-forma do Artigo A.** `Ψ_μ` e `Φ = dΨ` existem, mas a identificação com o escalar é justamente R82/OPEN. **Existe o termo; não existe a ponte de tipos.** [REAL — `paper_PT.tex:167–173`; `DESENHO_DO_FECHAMENTO_QG.md:2591,2668`]
3. **Diferencial de Connes.** A fatia tem `(C∞(S¹), L²(S¹), −iβ^{-1/2}∂_x)`; a operação `[D_circ,M_f]ψ = −iβ^{-1/2}f′ψ` é concreta. **Existe na representação da fatia, não como `Ψ_μ` identificado.** [REAL — `A Ponte Einstein Cartan Miguel.tex:1922–1932`; `um.py:6750–6769`; `SPECTRAL_RULE_REUSE_R88.md:29–35`]
4. **Conexão escalar.** `α′ = −(q/2)α`, equivalente a `(∂_κ + q/2)α = 0`, fornece conexão e seção paralela explícitas. **Existe no kernel, mas não foi renomeada como campo 3+1.** [REAL — `ContinuousModularZero.lean:203–217`; `SPECTRAL_RULE_REUSE_R88.md:13,35–39`]
5. **Corrente modular finita.** `L†L = P_0`, `LL† = P_1` implementa equivalência de faces distintas. **Existe no kernel, como matriz, não como vetor espaço-temporal.** [REAL — `ModularCurrent.lean:56–61,75–115`; `TheCurrentConnectsTheCorners.lean:132–168`]
6. **Corrente eletromagnética histórica.** O artigo recursivo escreve `j^ν_Ψ = 4g_{Ψγ}Ψ²∂_μF^{μν} + h_{Ψγ}(Ψ*∂^νΨ − Ψ∂^νΨ*)`. **Existe como documento histórico, com outra ação e outro β; não está ligado à cunhagem.** [REAL — `recursive_light_v3.tex:229–255,271–275,393–418`; `TGL_ATLAS.md:2381–2388`]

**Classificação do eixo.** Existem candidatos a vetor em pelo menos três tipos: conexão de gauge, 1-forma espaço-temporal e diferencial/conexão espectral. A passagem `A = Σa[D,b]` e `D_A`, ou qualquer equação que os identifique mantendo o mesmo registro, não foi localizada no recorte R88 ampliado pelas consultas desta K05. [REAL/OPEN — `SPECTRAL_RULE_REUSE_R88.md:35–45`]

### 2.3 Loop, holonomia e recursão

- **Holonomia infinitesimal no kernel:** `δ_A∘δ_B − δ_B∘δ_A = δ_[A,B]`; geradores comutantes dão holonomia zero. A reconstrução da holonomia ao tensor de Riemann completo permanece aberta. [REAL — `TransportWitness.lean:259–279`; escopo declarado em 39–45]
- **Holonomia de tríade no Artigo A:** `W = U_ki U_jk U_ij`; em geral `W ≠ I`, mas `Ad(W)` preserva os dados modulares na sombra finita. Em III₁ genuíno, provar `W ∈ Stab(𝒟)` segue conjectura. [REAL finito/CONJECTURE global — `paper_PT.tex:3226–3233`]
- **Defeito por travessia:** o defeito bruto cresce com o número de travessias; o normalizado por travessia é independente do laço, e a ida-e-volta dá `m(2−m)`. [REAL — `TheDeathOfTheSignal.lean:73–88,128–149`]
- **Recursão histórica:** `Ψ_{n+1} = 𝓕[Ψ_n]` com `𝓕 = U(Δt)∘Π_Nome∘L_GKLS`, permanência como iteração do ponto fixo. É documento `[DECLARADO]` de 2025, não teorema do cânone atual; seu `β ∼ 10^{-6}` é explicitamente distinto de β_TGL. [REAL documental — `recursive_light_v3.tex:82–136`; `TGL_ATLAS.md:2381–2388`]

**Classificação do eixo.** Há holonomia algébrica, holonomia de subespaços e recursão de processo. Nenhuma dessas três foi demonstrada ser, ao mesmo tempo, a holonomia U(1) de `A_μ` e o laço recursivo da fala. Essa identificação permanece `[OPEN]`.

### 2.4 Radical `√K` e o fluxo do Fecho 1

O Fecho 1 escreve `e^{tℒ} = ∫ V_s(·)V_s* dν_t`, `V_s = e^{is√K}`, `ν_t` gaussiana de variância `βt`, e reproduz `Γ_ij = ½β(√k_i−√k_j)²`; a distância na fatia é `ds = √β|d√k|`. [REAL na forma e na sombra declarada — `A Ponte Einstein Cartan Miguel.tex:1104–1118,1886–1901`; implementação em `um.py:6726–6747`]

O artigo **enuncia**, no produto cruzado, `u_s = e^{is√K̂}` como unitário da álgebra e `Fix = W*(K̂)`; esta seção E não trata essa igualdade como teorema independente. O fechamento condicionado emprega **H_K̂** (afiliação de `K̂=F(ĥ)≥0` a `L(ℝ)` e injetividade essencial de `F`) e **H_erg** (`M_φ=ℂ1`): sob H_K̂, `Fix=W*(K̂)` vale se e somente se `M_φ=ℂ1`; a aplicação física adicional depende de **H_TGL-horizon**, que permanece `[OPEN]`. A fonte original também classifica os dois lemas restantes como esquema de prova cuja redação completa fica pendente, e chama a não covariância de `√K̂` de ancoragem de escala, não seleção do valor de `τ★`. [REAL com escopo — `A Ponte Einstein Cartan Miguel.tex:1903–1919`; `T1_FECHADO.md:3–4,30–34,112–122,238–248`; `TAU_ESTRELA.md:61–65`]

O `um.py` implementa a raiz PSD e o salto `L = √β√K`, e também registra `V_s = e^{is√K}`, `ds = √β|d√k|`, `g = √|L|`. A reconciliação completa entre a lei-raiz e a canônica fica aberta quanto ao coeficiente, embora o mapa de expoentes seja calculado. [REAL — `um.py:1500–1516,2312–2328,2832–2840,2863–2875`]

A composição R88 dá `L_D(X) = −∇Φ_D(X)` e o limite projector por blocos `E_D`, com `E_D² = E_D` e `E_D exp(tL_D) = E_D`; porém diz expressamente que `D = √K` não é identificado com o `D` diferencial do círculo. [DERIVED na face finita — `SPECTRAL_RULE_REUSE_R88.md:19–35`]

**Classificação do eixo.** O radical e seu fluxo existem e são altamente pertinentes à palavra “radicalmente”. Não está escrito que esse fluxo seja a holonomia do vetor cinético, nem que estabilize a EOM escalar e a dispersão do psíon por uma única ação.

## 3. Candidatas de cunhagem — comparação sem escolha

Nenhuma linha abaixo é promoção. “Dá as duas?” pergunta pelas **duas equações-alvo da seção 0**, não por duas equações quaisquer. “Preserva o 2” distingue compatibilidade algébrica de derivação da segunda massa.

| candidata | Dá as duas equações? Com qual ξ? | Preserva o 2 e a segunda massa? | Escalar × `Φ_{μν}`, U(1), `|Ψ|²` e normalização | Hipótese NOMEADA e o que NÃO fecha |
|---|---|---|---|---|
| **A — Um escalar complexo dual acoplado a um vetor de gauge, na forma fundadora** | **Não com um só objeto/acoplamento.** A ação dá EOM e dispersão com `2ξ_L`. `ξ_L = β` serve ao psíon, mas não ao Artigo A; para obter coeficiente `1/6` na EOM, precisa `ξ_L = 1/12` (ou `ξ_A = 2ξ_L = 1/6` na escrita complexa de coeficiente 1). Se o psíon tem outro acoplamento, a candidata migra para B. | Com `ξ_L = β`, o 2 e a dispersão saem na forma fundadora. Com `ξ_L = 1/12`, a dispersão da mesma ação deixa de ser `2βR`. A segunda massa não sobrevive à troca silenciosa. | U(1) de fase é preservado por `D_μ` e `|Ψ|²`; a incompatibilidade escalar × vetor exige identificar `Ψ_μ = A_μ` e `Φ = F`. A reescala muda a carga `|Ψ|²`. O radical `√K` e o loop-holonomia não estão na ação. | **H_A:** `Ψ` complexo, `Ψ*` independente, `A_μ` conexão, `F=dA`, `W_γ = P exp(ie∮A)` como loop. **Não fecha:** duas equações-alvo com um só ξ, origem do `√K`, identidade loop = `W_γ`, e ação única para os dois regimes. |
| **B — Dois setores independentes: escalar complexo do Artigo A + 1-forma literal (R82/R89)** | **Formalmente, só com dois objetos e dois acoplamentos nomeados.** O setor escalar usa `ξ_A = 1/6` e coeficiente 1; o setor vetorial pode dar `2ξ_V R A`, com `ξ_V = β`. Exige uma ação conjunta e uma regra dizendo qual `|·|²` recebe cada curvatura. | O 2 aparece na EOM vetorial. A segunda massa só segue se o modo vetorial for identificado ao psíon, com `R = βu²` e `m₀ = 0`; essa identificação não é dada. | R89 mostra que a EOM vetorial não é a escalar; o resíduo não é escolhido para cancelar. `ξ_V R A²` quebra gauge na ação total, embora `−¼F²` seja invariante. `A²` é lorentziano e depende da métrica. A versão complexa muda os fatores da variação. | **H_B:** campos e acoplamentos separados, alocação dos termos de curvatura e identificação do modo vetorial com o psíon. **Não fecha:** gauge total, resíduo R89, carga modular comum, origem da dispersão como consequência e não input. |
| **C — Escalar complexo + vetor espectral/de Connes, com loop GKLS e radical `√K`** | **Não.** Há gradiente, conexão, corrente, recursão e dissipador, mas não uma variação que produza a EOM escalar e a dispersão. `ξ_A = 1/6` e `ξ_P = β` só podem ser mantidos como dados separados. | O 2 do psíon permanece intacto por não ser tocado; não é derivado desta candidata. `Γ_ij = ½β(√k_i−√k_j)²` é outra lei, não a dispersão `ω² = m₀² + 2βR`. | Gradiente puro dá `F=d²ψ=0`; a conexão escalar não é automaticamente U(1) espaço-temporal. Não há definição comum de `|Ψ|²` nem normalização da ação. | **H_C:** `d_D f` ou `q/2 dκ` é `Ψ_μ`; `D=√K` é identificado ao `D_circ`; o fluxo GKLS é o loop do vetor. **Não fecha:** justamente essas três identificações, as duas EOM e a carga absoluta. |
| **D — Dualidade modular J + holonomia de transporte/cociclo** | **Não.** Fornece dualidade e laço, não a EOM local nem a dispersão. `ξ_A` e `ξ_P` ficam externos à proposta. | Não altera o 2 nem a massa, mas também não os deduz. | `conjJ` troca faces; a conjugação complexa de fases não está ligada ao `towerJ`. `Ad(W) ∈ Stab(𝒟)` não é automaticamente fase U(1). `|Ψ|²` pode ser carga transportada, mas a ação escalar × vetor não é fornecida. | **H_D:** J é a conjugação do campo e `W` é o loop U(1); uma deformação não trivial fornece o vetor. **Não fecha:** mapa J ↔ `Ψ*`, `W` ↔ holonomia de gauge, ação e equações. No absoluto não deformado, o fluxo é trivial. |
| **E — Recursão histórica da luz + corrente eletromagnética** | **Não.** A ação histórica tem outra EOM e outro setor eletromagnético; seu `β ∼ 10^{-6}` não é β_TGL. Não recupera o `ξ_A = 1/6` canônico nem o `ξ_P = β` do psíon. | Não fornece o 2 nem a segunda massa do cânone. | Tem `Ψ` complexo, `F_{μν}` e `j^ν_Ψ`, mas a interação não é a conexão fundadora `D=∇−ieA`; U(1) e a carga modular atual não são herdados. | **H_E:** a recursão histórica é o loop da cunhagem e sua corrente é o vetor cinético. **Não fecha:** colisão de β, forma da ação, coeficientes, U(1) e as duas equações. Fica como documento, não como prova da nova leitura. |

### Controles negativos que impedem atalhos

1. **Um único ξ não basta.** `β`, `1/6` e `1/12` desempenham papéis diferentes; escolher um deles para todas as equações perde uma das formas canônicas ou a segunda massa.
2. **Um único símbolo `Ψ` não basta.** R82 exige resolver escalar contra `Ψ_μ`; R89 dá o resíduo explícito quando se tenta comparar as EOM.
3. **Maxwell não fornece o escalar.** Um gradiente puro tem curvatura nula; uma 1-forma independente tem operador e restrição diferentes.
4. **Gauge do termo não é gauge da ação.** `−¼F²` é invariante, mas `ξR A²` e massa vetorial não o são em geral.
5. **Reescala não é inócua.** `|Ψ|²` é carga modular transportada, e a versão vetorial depende da métrica e não é positiva automaticamente.
6. **Loop não é homonímia.** Holonomia U(1), holonomia de transporte, tríade de subespaços e recursão GKLS são objetos distintos até prova de mapa.
7. **O 2 não é errata.** Ele é definição `[INPUT]` do psíon e sustenta `½ω = β·sen45°·u`; retirá-lo produz a leitura proporcional `βu/2`, não a forma da segunda derivação.
8. **A fonte modular não é bônus derivado.** O Artigo A declara aberta a universalidade da ponte; `ActionCouplingData.EOM` é input.

## 4. Existência, fiação e bloqueios resultantes

| pergunta | classificação desta K05 |
|---|---|
| Existem duas equações no cânone? | **EXISTEM E ESTÃO LIGADAS, separadamente:** Artigo A/`um.py`/`ActionCouplingData` e `PontoZeroDoPsion`. [REAL] |
| Existe uma ação única escrita que dê as duas exatamente? | **NÃO LOCALIZADA no cânone/recorte consultado; [OPEN].** A fundadora tem as duas peças, mas sua normalização e seus coeficientes não dão as duas equações-alvo sem hipóteses adicionais. |
| Existe par complexo e conjugação? | **EXISTE na linhagem e no Artigo A; no kernel só há tipagem complexa, sem `Ψ*`.** J modular existe, mas sua ponte com a conjugação do campo não está fechada. |
| Existe vetor associado? | **EXISTE em três tipos: gauge, 1-forma e espectral.** A identificação com o escalar e com `Φ_{μν}` está aberta. |
| Existe loop/holonomia/recursão? | **EXISTE em todas as três formas.** A identificação U(1) ↔ transporte ↔ recursão é hipótese, não fiação pronta. |
| Existe radical `√K` e fluxo? | **EXISTE no Fecho 1, no runtime e na composição R88.** Não está ligado à holonomia do vetor nem a uma ação única. |
| Os coeficientes se fundem? | **NÃO, pelo registro v354/v355 e pelos controles do kernel.** A dispersão posterior com `ξ=β` exige manter explícita a distinção de objetos/acoplamentos ou nomear uma nova identificação. |
| A fala do operador tem antecedente formal? | **TEM FORMA ANTECEDENTE, não derivação.** A lagrangiana fundadora tem a mesma arquitetura escalar complexo + vetor de gauge; a identificação é do operador e o tratamento formal fica `[OPEN]`. [INPUT]/[DECLARADO] |

## 5. Conclusão do levantamento

A arquitetura mais diretamente **sugerida pelos arquivos** é o escalar complexo com derivada covariante e um vetor com curvatura; isso, porém, **não é escolha nem fechamento**. As duas equações canônicas só convivem sem perda se a diferença entre `ξ_A = 1/6` e `ξ_P = β` for tratada explicitamente — por objetos/acoplamentos distintos ou por uma hipótese ainda não escrita que os relacione. A segunda massa exige manter o 2 do psíon. O “vetor cinético” e o “loop recursivo” admitem leituras gauge, 1-forma, espectral e modular, mas suas pontes permanecem nomeadas e abertas.

O bloqueio científico preciso não é “falta um ½”: é **escrever, com tipos e régua explícitos, uma ação que preserve a carga modular, explique os dois acoplamentos, mantenha `2ξ_P R`, produza as duas equações e identifique o fluxo radical com o loop do vetor**. Nenhuma candidata examinada fecha todos esses itens.

## 6. Fontes e reproducibilidade

- Medidas: `K05/CAMPO/medir_campo.py` e `K05/CAMPO/medidas_campo.json`; execução final concluída com todos os pins literais e asserções aprovados.
- Consultas e classificação de cobertura: `K05/CAMPO/CONSULTAS_CAMPO_K05.md`.
- Artigo A: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\paper_PT.tex`, linhas citadas acima. [paper_PT](kimi-cite://md-line?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2Fpaper_PT.tex&line=167 "citation")
- Kernel: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\PontoZeroDoPsion.lean`, linhas citadas acima. [PontoZeroDoPsion](kimi-cite://md-line?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2FN%C3%B3s%2Ftgl_kernel%2FTGLExt%2FPontoZeroDoPsion.lean&line=85 "citation")
- Lagrangiana fundadora: `C:\IALD\Artigo\the_boundary\Genesis da Unificação\Artigos_fundadores\graviton_v2.tex`, linhas 186–214 e 269–274. [graviton_v2](kimi-cite://md-line?path=C%3A%2FIALD%2FArtigo%2Fthe_boundary%2FGenesis%20da%20Unifica%C3%A7%C3%A3o%2FArtigos_fundadores%2Fgraviton_v2.tex&line=186 "citation")
- Desenho R82–R89: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\DESENHO_DO_FECHAMENTO_QG.md`, linhas 2587–2670. [DESENHO_DO_FECHAMENTO_QG](kimi-cite://md-line?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2FN%C3%B3s%2FDESENHO_DO_FECHAMENTO_QG.md&line=2591 "citation")
- Não fusão dos coeficientes: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py`, linha 182860; `TheSameBetaReadsFourFaces.lean` e `ActionCouplingControls.lean`. [um](kimi-cite://md-line?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2FN%C3%B3s%2Fum.py&line=182860 "citation"), [ActionCouplingControls](kimi-cite://md-line?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2FN%C3%B3s%2Ftgl_kernel%2FTGLExt%2FActionCouplingControls.lean&line=62 "citation")
- Fala original: `C:\IALD\Central de Patentes\work\vitrine_postura_13nov\OPERADOR_13nov_concordo_com_o_meio_o_campo_e_dual_sim_a_nota_a_calculadora_e_o_zenodo_verbatim.txt`, linha 1, hash conferido. [OPERADOR_13nov](kimi-cite://text?path=C%3A%2FIALD%2FCentral%20de%20Patentes%2Fwork%2Fvitrine_postura_13nov%2FOPERADOR_13nov_concordo_com_o_meio_o_campo_e_dual_sim_a_nota_a_calculadora_e_o_zenodo_verbatim.txt&text=eu%20acho%20que%20%C3%A9%20dual%20%28porque%20%C3%A9%20conjugado%29 "citation")
- Fecho 1: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\A Ponte Einstein Cartan Miguel.tex`, linhas 1886–1919. [A Ponte Einstein Cartan Miguel](kimi-cite://md-line?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2FA%20Ponte%20Einstein%20Cartan%20Miguel.tex&line=1886 "citation")
- R88 espectral e 1-forma: `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015\full_source_r88\spectral_reuse\SPECTRAL_RULE_REUSE_R88.md` e `...\source\ONE_FORM_FULL_SOURCE_R88.md`. [SPECTRAL_RULE_REUSE_R88](kimi-cite://md-line?path=C%3A%2FIALD%2FCentral%20de%20Patentes%2FChatgpt%2FTUNEL%2FDO_CHATGPT%2FORDEM_019%2FF1.FECHO_20261015%2Ffull_source_r88%2Fspectral_reuse%2FSPECTRAL_RULE_REUSE_R88.md&line=19 "citation"), [ONE_FORM_FULL_SOURCE_R88](kimi-cite://md-line?path=C%3A%2FIALD%2FCentral%20de%20Patentes%2FChatgpt%2FTUNEL%2FDO_CHATGPT%2FORDEM_019%2FF1.FECHO_20261015%2Ffull_source_r88%2Fsource%2FONE_FORM_FULL_SOURCE_R88.md&line=58 "citation")
