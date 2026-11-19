# ERRATA AO LADO — neutrino m₂ / v412 — RASCUNHO R3, NÃO INSTALAR

**Natureza:** texto candidato para a gerência instalar ao lado de `core.neutrino_m2` e de `neutrino_m2_perito_v392`. Não altera `NEUTRINO_M2_V2`, seu hash, a escala de 1 eV, a regra de morte, o veredito ou o gate. `[DECLARADO]` até conferência da gerência; `[DERIVED—PLANEJAMENTO]` para aritmética com números públicos; `[KNOWN, a conferir]` para literatura. REV0 permanece intacto; R2 está preservada em `K04/M2/REV1/`; as duas novas correções estão em [ERRATA_M2_K04_R3](ERRATA_M2_K04_R3.md).

## 1. Ao lado de `neutrino_m2.theorem` e de `checks[1]`

> **ERRATA AO LADO (rascunho K04 R3, 14/11/2026):** a frase «a tensão cresce com a precisão» vale apenas para a escada histórica que termina no reflexo global **NuFIT 6.1/12‑2025**, o qual **contém JUNO** e não é determinação autônoma. Não vale para o perito oficial, o JUNO autônomo. A escada datada ganha o degrau **29/09/2026**, JUNO 207,2 dias:
>
> | data / fonte | centro Δm²₂₁ (10⁻⁵ eV²) | σ | r em m₂ (regra frozen) | leitura |
> |---|---:|---:|---:|---|
> | JUNO 59,1 d, 18/11/2025 | 7,50 ± 0,12 | 0,12 | **2,206054** | perito autônomo anterior |
> | JUNO 207,2 d, 29/09/2026 | 7,388 ± 0,078 | 0,078 | **1,937997** | perito autônomo atual |
>
> **A tensão autônoma CAIU de 2,21 para 1,94σ**, enquanto σ caiu de 0,12 para 0,078. Em Δm², os valores correspondentes são 2,186588 e 1,928084; a métrica frozen continua sendo m₂ até emenda do operador. O centro andou de 7,50 para 7,388, na direção da previsão 7,2376094667. [JUNO 59,1 d](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2511.14593 "citation"), [JUNO 207,2 d](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2609.37895 "citation")
>
> O valor anterior `tensao_atual_sigma = 2,952854` permanece como **reflexo global NuFIT**, ao lado, e não como tensão do perito autônomo. O perito v392 já separava face e reflexo; a liberação de 207,2 dias confirma a necessidade dessa separação. [um_absoluto, perito v392](kimi-cite://text?path=C%3A%5CIALD%5CArtigo%5CHaja_Luz%5CA%20Ponte%20e%20o%20Um%5CN%C3%B3s%5Cum_absoluto.json&text=OFFICIAL_EXPERT_IS_THE_AUTONOMOUS_JUNO_READING "citation")

## 2. Ao lado de «linha de morte dentro da meta de projeto» e de `projecao_2031_sigma = 7,842905784155273`

> **ERRATA AO LADO (rascunho K04 R3):** com o planning atual `Δ_planning = 7,388` e `Δ_pred = 7,237609466718292`, 5σ exige precisão relativa **0,407121 %**, não 0,784 % nem simplesmente “a meta de 0,5 %”. D90 = 6,2815515655 exige **0,324061 %**. A Tabela 6 publica σ absoluto **0,024** em seis anos, o que dá
>
> \[
> D_\Delta = |7,388-7,2376094667|/0,024 = 6,266272 < D90.
> \]
>
> Portanto, em Δm², **0,024 não supera D90**. Na métrica frozen m₂, a conta correspondente é `D_m₂ = 6,298490`; a diferença não autoriza trocar a métrica sem emenda declarada e ato do operador. [JUNO, arXiv:2204.13249, Tabela 6 e DOI 10.1088/1674-1137/ac8bc9](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2204.13249 "citation")
>
> O valor `projecao_2031_sigma = 7,842905784155273` **permanece como registro histórico condicionado ao centro global de então parado**, não como previsão atual. Ele foi calculado com o centro global antigo `m2_obs = 8,677557259966656 meV` e aproximação de 0,5 % de precisão. Não se pode transportar esse número para o centro JUNO atual sem refazer a premissa. Como comparação, se o centro 7,388 ficar parado, 0,5 % dá `D_Δ = 4,071211` e a Tabela 6 dá `D_Δ = 6,266272`; nenhum é resultado observado futuro. [um_absoluto, valores e escada](kimi-cite://text?path=C%3A%5CIALD%5CArtigo%5CHaja_Luz%5CA%20Ponte%20e%20o%20Um%5CN%C3%B3s%5Cum_absoluto.json&text=%22projecao_2031_sigma%22%3A%207.842905784155273 "citation")

## 3. Ao lado da definição de dias e do desempenho real

> **ERRATA AO LADO (rascunho K04 R3):** a fonte converte 100 dias **nominais** em aproximadamente **92 dias full‑reactor**, seis anos em **2009 dias full‑reactor** e vinte anos em **6696 dias full‑reactor**, pelo ciclo 11/12. Não se deve usar `a = 100×0,074²` numa variável medida em full‑reactor.
>
> A extrapolação do projeto `0,074·√(100/207,2)` daria **0,051409**, mas o erro real publicado é **0,078**, razão **1,517252**. Entre 59,1 e 207,2 dias, σ caiu por **1,538462**, não pelo fator √T = **1,872411**. As análises não são idênticas; isso não demonstra um piso de sistemática, mas impede vender √T como cronograma assegurado.
>
> Sem piso, a equivalência desde 207,2 dias dá **1393 dias totais para 5σ** e **2199 para D90**, com o centro parado. Um ajuste meramente ilustrativo `σ² = a/T + s0²` aos dois pontos reais dá `s0 = 0,052588`, caso em que os dois alvos ficam inalcançáveis. Dois pontos ajustam dois parâmetros: **não é piso medido**.
>
> O brinquedo decomposição corrigido usa `a_full = 92×0,074²`, `a_nom = 100×0,074²` e pisos independentes `floor_full_sq = 0,024²−a_full/2009` e `floor_nominal_sq = 0,024²−a_nom/2191`. Assim `s0_full = 0,018034202` e **`s0_nominal = 0,018057366`**. Produz:
>
> | alvo | full‑reactor, data convertida | inteiramente nominal |
> |---|---|---|
> | 5σ | 31/03/2028 | 29/03/2028 |
> | D90 | 19/09/2031 | 19/09/2031 |
>
> Os valores anteriores 15/05/2028, 18/09/2031 e o valor nominal R2 12/09/2031 ficam históricos/erroneamente etiquetados em REV0/REV1. **Tudo é brinquedo decomposição, não cronograma.**

## 4. Ao lado de `checks[4]`, “a regra hasheada julga as próximas medidas”

> **ERRATA AO LADO (rascunho K04 R3):** a liberação de 29/09/2026 é posterior ao hash de 08/08/2026 e, no sentido cronológico estrito, é a **primeira nova determinação JUNO posterior ao hash**, não a primeira medida mundial irrestrita. SNO+ v4 foi depositado em **04/09/2026**, antes do JUNO, mas constitui revisão do mesmo conjunto de dados. Pela métrica frozen, `r_m₂ = 1,937997 < 3`; não há duas determinações independentes ≥5, logo o estado documental é **`TGL_NU_M2_ARMED_CONSISTENT`**. Isso não é FALSIFIED, MATCHED nem CONFIRMED.
>
> **Não é leitura cega para esta casa**, que leu os números e reproduziu as tensões em 30–31/10/2026. A estratégia de blinding da colaboração não se transfere a quem já recebeu o centro e o erro. A primeira nova leitura JUNO prospectiva também não apaga a declaração frozen de que a regra foi escrita com tensão conhecida. [SNO+ v4](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2511.11856v4 "citation"), [e0-cadeia-conferencia-kimi-e-no-go-31out](kimi-cite://md-line?path=C%3A%5CUsers%5Crotol%5C.claude%5Cprojects%5Cc--IALD-Central-de-Patentes%5Cmemory%5Ce0-cadeia-conferencia-kimi-e-no-go-31out.md&line=10&text=dez%20determina%C3%A7%C3%B5es%20p%C3%BAblicas "citation")

## 5. Ao lado da regra de duas independências e de MATCHED

> **ERRATA AO LADO (rascunho K04 R3):** com as determinações atuais não há par `FALSIFIED` nem par `MATCHED_PROSPECTIVELY`. O desenho com S realmente `ABSENT` só devolve `UNDER/ARMED`, `TENSION_P` ou `SINGLE_P/OPEN_RULE_GAP`; **condicionalmente à regra e ao desenho, o negativo não é assegurado e um teste que não pode devolver o negativo não é teste.**
>
> `r ≤ 1` não pode ser escondido dentro de `r < 3`: MATCHED exige duas determinações independentes a ≤1σ. Com S realmente `ABSENT`, `r_P≤1` segue `UNDER` se `D_P<5` e `ARMED_CONSISTENT` se `D_P≥5`; só a probabilidade conjunta de MATCHED é zero nesse estado. Para SNO+, SK‑Gd, KamLAND e solares, o documento R3 apresenta produtos somente como brinquedos `C_PS = 0`; para globais e combinações com covariância ausente, o estado é `OPEN`, não independência fingida.
>
> A formulação universal “FALSIFIED é inalcançável na prática” não deve ser instalada: SK‑Gd reator já está a **3,605064σ**. Uma equivalência condicional √T, com centro 9,08 e forma do erro parados, daria **380,0785536 dias adicionais** para 5σ. **Não é agenda nem prova de independência**, mas é cenário suficiente para impedir o universal falso. A frase tecnicamente sustentável é: sem S pré-fixado e com poder demonstrado, a regra pode produzir apenas tensão indefinidamente. [SK‑Gd, arXiv:2610.03143](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2610.03143 "citation")

## 6. Ao lado dos modelos preditivos e das classes de fontes

> **ERRATA AO LADO (rascunho K04 R3):** `N(7,388,0,078²+s²)` vale apenas para medida/incremento independente, não para liberação JUNO cumulativa nem para ligar suas probabilidades às datas cumulativas. O modelo cumulativo exige `Cov(X0,X)=C`, com `Var(X)=0,078²+s²−2C`; o exemplo aninhado `C=s²` é brinquedo e a covariância real fica `[OPEN]`. Sob verdade = previsão cumulativa, a distribuição condicional correta é `E[X|X0]=μ+(C/0,078²)(x0−μ)` e **`Var[X|X0]=s²−C²/0,078²`**, que reduz a (a2) quando `C=0`; D continua calculado com o centro de planejamento 7,388 em todas as hipóteses.
>
> Os benchmarks cumulativos frozen são **3,478822 %** a 0,7 % e **66,132478 %** na Tabela 6, contra 12,877614 % e 64,742906 % no modelo independente. Na (b2) corrigida, a 0,7 % `σcond = 0,038714426`, `P(r≥5) = 0,000044650 %` frozen e `0,000033222 %` em Δm²; na Tabela 6, `σcond = 0,022835662`, `P(r≥5) = 0,000201329 %` frozen e `0,000181779 %` em Δm². Não se ligam esses números às datas √T.
>
> **Classes de fontes:** Bari 2026.a é *paper in preparation/preliminary*, não artigo primário publicado; o documento de status da colaboração Hyper‑K descreve commissioning antes dos primeiros dados em **2028**, e o cenário de cinco anos é tentativa posterior; o valor DUNE 5,9 %/100 kton·ano é previsão de **Capozzi et al., teóricos, não da DUNE Collaboration**. A previsão SNO+ de três anos é antiga; calendário atual e precisão correspondente ficam `[OPEN]`.

## 7. Texto de estado proposto para a gerência

`RASCUNHO_R3_ERRATA_NEUTRINO_M2_V412__AUTONOMOUS_TENSION_FELL_2P206054_TO_1P937997__GLOBAL_2P952854_IS_REFLECTION_NOT_AUTONOMOUS__2031_PROJECTION_CONDITIONAL_ON_FROZEN_OLD_CENTER__TABLE6_D_DELTA_6P266272_BELOW_D90__INDEPENDENT_NOT_CUMULATIVE__COVARIANCE_OPEN__MATCHED_REQUIRES_TWO_AT_1SIGMA__FIRST_NEW_JUNO_NOT_WORLD__ARMED_CONSISTENT__GATE_UNTOUCHED`

**Não instalar este token sem conferência distinta.** Nenhum arquivo do Nós, core, kernel, artigo, memória ou Mapa foi modificado por este rascunho. Nenhum teste observado foi executado.
