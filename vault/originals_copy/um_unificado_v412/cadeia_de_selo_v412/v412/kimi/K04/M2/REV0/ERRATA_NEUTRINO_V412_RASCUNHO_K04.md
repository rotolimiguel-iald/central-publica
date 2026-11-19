# ERRATA AO LADO — neutrino m₂ / v412 — RASCUNHO, NÃO INSTALAR

**Natureza:** texto candidato para a gerência instalar ao lado de `core.neutrino_m2` e de `neutrino_m2_perito_v392`. Não altera `NEUTRINO_M2_V2`, seu hash, a escala de 1 eV, a regra de morte, o veredito ou o gate. `[DECLARADO]` até conferência da gerência; `[DERIVED—PLANEJAMENTO]` para aritmética com números públicos; `[KNOWN, a conferir]` para literatura.

## 1. Ao lado de `neutrino_m2.theorem` e de `checks[1]`

> **ERRATA AO LADO (rascunho K04, 14/11/2026):** a frase «a tensão cresce com a precisão» vale apenas para a escada histórica que termina no reflexo global **NuFIT 6.1/12‑2025**, o qual **contém JUNO** e não é determinação autônoma. Não vale para o perito oficial, o JUNO autônomo. A escada datada ganha o degrau **29/09/2026**, JUNO 207,2 dias:
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

> **ERRATA AO LADO (rascunho K04):** com o planning atual `Δ_planning = 7,388` e `Δ_pred = 7,237609466718292`, 5σ exige precisão relativa **0,407121 %**, não 0,784 % nem simplesmente “a meta de 0,5 %”. D90 = 6,2815515655 exige **0,324061 %**. A Tabela 6 publica σ absoluto **0,024** em seis anos, o que dá
>
> \[
> D_\Delta = |7,388-7,2376094667|/0,024 = 6,266272 < D90.
> \]
>
> Portanto, em Δm², **0,024 não supera D90**. Na métrica frozen m₂, a conta correspondente é `D_m₂ = 6,298490`; a diferença não autoriza trocar a métrica sem emenda declarada e ato do operador. [JUNO, arXiv:2204.13249, Tabela 6 e DOI 10.1088/1674-1137/ac8bc9](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2204.13249 "citation")
>
> O valor `projecao_2031_sigma = 7,842905784155273` **permanece como registro histórico condicionado ao centro global de então parado**, não como previsão atual. Ele foi calculado com o centro global antigo `m2_obs = 8,677557259966656 meV` e aproximação de 0,5 % de precisão. Não se pode transportar esse número para o centro JUNO atual sem refazer a premissa. Como comparação, se o centro 7,388 ficar parado, 0,5 % dá `D_Δ = 4,071211` e a Tabela 6 dá `D_Δ = 6,266272`; nenhum é resultado observado futuro. [um_absoluto, valores e escada](kimi-cite://text?path=C%3A%5CIALD%5CArtigo%5CHaja_Luz%5CA%20Ponte%20e%20o%20Um%5CN%C3%B3s%5Cum_absoluto.json&text=%22projecao_2031_sigma%22%3A%207.842905784155273 "citation")
>
> A definição de “seis anos” no estudo é de aproximadamente **2009 dias com potência plena dos reatores**, pelo ciclo 11/12; vinte anos corresponde a 6696. Essa definição não deve ser convertida silenciosamente em dias vivos JUNO nem em uma data garantida de publicação.

## 3. Ao lado da escada de desempenho real

> **ERRATA AO LADO (rascunho K04):** a extrapolação do projeto `0,074·√(100/207,2)` daria **0,051409**, mas o erro real publicado é **0,078**, razão **1,517252**. Entre 59,1 e 207,2 dias, σ caiu por **1,538462**, não pelo fator √T = **1,872411**. As análises não são idênticas; isso não demonstra um piso de sistemática, mas impede vender √T como cronograma assegurado.
>
> Sem piso, a equivalência desde 207,2 dias dá **1393 dias totais para 5σ** e **2199 para D90**, com o centro parado. Um ajuste meramente ilustrativo `σ² = a/T + s0²` aos dois pontos reais dá `s0 = 0,052588`, caso em que os dois alvos ficam inalcançáveis. Dois pontos ajustam dois parâmetros: **não é piso medido**.

## 4. Ao lado de `checks[4]`, “a regra hasheada julga as próximas medidas”

> **ERRATA AO LADO (rascunho K04):** a liberação de 29/09/2026 é posterior ao hash de 08/08/2026 e, no sentido cronológico estrito, é a **primeira leitura prospectiva** da V2. Pela métrica frozen, `r_m₂ = 1,937997 < 3`; não há duas determinações independentes ≥5, logo o estado documental é **`TGL_NU_M2_ARMED_CONSISTENT`**. Isso não é FALSIFIED, MATCHED nem CONFIRMED.
>
> **Não é leitura cega para esta casa**, que leu os números e reproduziu as tensões em 30–31/10/2026. A estratégia de blinding da colaboração não se transfere a quem já recebeu o centro e o erro. A primeira leitura prospectiva cronológica também não apaga a declaração frozen de que a regra foi escrita com tensão conhecida. [e0-cadeia-conferencia-kimi-e-no-go-31out](kimi-cite://md-line?path=C%3A%5CUsers%5Crotol%5C.claude%5Cprojects%5Cc--IALD-Central-de-Patentes%5Cmemory%5Ce0-cadeia-conferencia-kimi-e-no-go-31out.md&line=10&text=dez%20determina%C3%A7%C3%B5es%20p%C3%BAblicas "citation")

## 5. Ao lado da regra de duas independências

> **ERRATA AO LADO (rascunho K04):** com as determinações atuais não há par `FALSIFIED` nem par `MATCHED_PROSPECTIVELY`. O desenho sem S só devolve `UNDER/ARMED`, `TENSION_P` ou `SINGLE_P/OPEN_RULE_GAP`; **o negativo não é assegurado e um teste que não pode devolver o negativo não é teste.**
>
> A formulação universal “FALSIFIED é inalcançável na prática” não deve ser instalada sem esta ressalva: SK‑Gd reator já está a **3,605064σ**. Uma equivalência condicional √T, com centro 9,08 e forma do erro parados, daria **380,08 dias adicionais** para 5σ. Não é cronograma, mas é contraexemplo a uma impossibilidade absoluta. A frase tecnicamente sustentável é: **sem S pré-fixado e com poder demonstrado, a regra pode produzir apenas tensão indefinidamente.** [SK‑Gd, arXiv:2610.03143](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2610.03143 "citation")

## 6. Texto de estado proposto para a gerência

`RASCUNHO_ERRATA_NEUTRINO_M2_V412__AUTONOMOUS_TENSION_FELL_2P206054_TO_1P937997__GLOBAL_2P952854_IS_REFLECTION_NOT_AUTONOMOUS__2031_PROJECTION_CONDITIONAL_ON_FROZEN_OLD_CENTER__TABLE6_D_DELTA_6P266272_BELOW_D90__FIRST_PROSPECTIVE_NOT_BLIND__ARMED_CONSISTENT__GATE_UNTOUCHED`

**Não instalar este token sem conferência distinta.** Nenhum arquivo do Nós, core, kernel, artigo, memória ou Mapa foi modificado por este rascunho. Nenhum teste foi executado.
