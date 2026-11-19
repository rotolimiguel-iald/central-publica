# K04/B — m₂: desfechos, calendário, incremento e segunda testemunha — R3

**Estatuto geral:** `[DECLARADO]` para o desenho; `[DERIVED—PLANEJAMENTO]` para contas com números públicos agregados; `[KNOWN, a conferir]` para literatura; `[OPEN]` para covariância ou informação não publicada. Nenhum vetor de dados foi baixado ou lido, nenhuma likelihood foi aberta, nenhuma estatística observada nova foi calculada, nada de H0DN foi executado e nenhum teste observado foi realizado. As fórmulas foram avaliadas analiticamente, sem simulação e sem semente. REV0 permanece intacto; R2 e seus hashes estão preservados em `K04/M2/REV1/`; as duas novas correções estão resumidas em [ERRATA_M2_K04_R3](ERRATA_M2_K04_R3.md).

## Conclusão antes das contas

1. **D de desenho não muda quando a hipótese é “verdade = previsão”.** Ele é sempre calculado com o centro de planejamento já público, 7,388, e com a precisão futura. Em `r_P < 3`, 0,7 % e 0,5 % devolvem `UNDER`; desde 0,407121 % devolvem `ARMED_CONSISTENT`, inclusive sob verdade = previsão.
2. **O modelo \(N(7,388,0,078^2+s^2)\) vale somente para medida/incremento independente.** Não vale para liberação JUNO cumulativa nem liga suas probabilidades às datas cumulativas. O modelo cumulativo exige `Cov(X0,X)=C`; o exemplo `C=s²` é apenas um brinquedo de sensibilidade, pois a covariância real permanece `[OPEN]`.
3. **Hoje não há par publicado que satisfaça `FALSIFIED` nem par que satisfaça `MATCHED_PROSPECTIVELY`.** Com S realmente `ABSENT`, só são alcançáveis `UNDER/ARMED`, `TENSION_P` e `SINGLE_P/OPEN_RULE_GAP`; a probabilidade conjunta de MATCHED é zero **somente nesse estado**. O desfecho negativo não está assegurado pelo desenho: **condicionalmente à regra e ao desenho, um teste que não pode devolver o negativo não é teste.**
4. **Isso não autoriza o universal falso “FALSIFIED é inalcançável na prática”.** SK‑Gd reator está a **3,605064σ**. Com centro 9,08 e forma do erro parados, a equivalência \(\sigma\propto T^{-1/2}\) fornece **380,0785536 dias adicionais** para 5σ. É cenário, não agenda nem prova de independência. A frase sustentável é: sem S pré-fixado e com poder demonstrado, a regra pode produzir apenas tensão indefinidamente.
5. **Vale a métrica congelada em m₂ até emenda do operador:** `r_m₂ = 1,937997`; em Δm², `r_Δ = 1,928084`. Para o D de planejamento em Δm², a Tabela 6 dá **6,266272 < 6,281552 = D90**. Não houve troca de métrica, escala ou regra.
6. A liberação JUNO de 207,2 dias, de **29/09/2026**, é a **primeira nova determinação JUNO posterior ao hash da V2 de 08/08/2026**, não a primeira medida mundial irrestrita. SNO+ v4 foi depositado em **04/09/2026**, antes do JUNO, mas é revisão do mesmo conjunto de dados. O estado documental JUNO é `TGL_NU_M2_ARMED_CONSISTENT`, pois `r_m₂ < 3` e não há duas independências ≥5. **Não é leitura cega para esta casa**, que leu centro e tensão em 30–31/10/2026. [SNO+ v4](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2511.11856v4 "citation"), [JUNO 207,2 d](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2609.37895 "citation"), [e0-cadeia-conferencia-kimi-e-no-go-31out](kimi-cite://md-line?path=C%3A%5CUsers%5Crotol%5C.claude%5Cprojects%5Cc--IALD-Central-de-Patentes%5Cmemory%5Ce0-cadeia-conferencia-kimi-e-no-go-31out.md&line=10&text=dez%20determina%C3%A7%C3%B5es%20p%C3%BAblicas "citation")
7. **Q1 para o operador, sem escolha feita aqui:** manter duas independências ≥5 e declarar que o canal devolve só tensão até haver par; emendar para uma testemunha com limiar explícito; ou pré-fixar S, inclusive possível SK‑Gd, com covariância e robustez? Toda mudança de fórmula, fonte, métrica ou limiar é **emenda declarada e ato do operador**, nunca ajuste ao centro.

### Alternativas e custos

| Alternativa | O que preserva | Custo e condição |
|---|---|---|
| **A — manter duas independências ≥5 e anunciar “somente tensão” até haver par** | Regra frozen integral; nenhuma emenda de fórmula | Pode nunca produzir FALSIFIED nem MATCHED; um P alto continua `SINGLE_P/OPEN_RULE_GAP`. Exige declarar que não é teste decisivo enquanto S não tiver poder. |
| **B — uma testemunha com limiar explícito** | Restaura a possibilidade lógica de negativo | É emenda. Candidatos: `r_P ≥ 5` em m₂, ou `D_P ≥ 6,281552` junto de `r_P ≥ 5`, com incremento disjunto, covariância publicada, tentativas e estresses visíveis. Custa perda da réplica independente e aumenta a assimetria. O limiar não foi escolhido aqui. |
| **C — manter a dupla exigência e pré-fixar SK‑Gd como S, sem exigir σ_S ≤ 0,0301** | A fórmula de duas independências pode permanecer | Nomeação/versão da fonte também deve ser emenda se não tiver sido fixada antes. Exige covariância, análise congelada e aceitação de erro grande e centro móvel. O corte 0,0301 é suficiente para S perto de 7,388, **não necessário** para S distante como 9,08. |

`MATCHED_PROSPECTIVELY` exige **duas determinações independentes a ≤1σ** e, mesmo se alcançado, não significa `CONFIRMED`.

---

## 1. D, hipóteses e os três modelos que não podem ser misturados

Em unidades de \(10^{-5}\,\mathrm{eV}^2\),

\[
\Delta_{\rm pred}=7,237609466718292,\qquad
\Delta_0=7,388,\qquad
\delta=\Delta_0-\Delta_{\rm pred}=0,150390533281708 .
\]

Para qualquer hipótese,

\[
D_\Delta(s)=\frac{\delta}{s},\qquad
D_{m_2}(s)=\frac{m_2(\Delta_0)\,|m_2(\Delta_0)-m_{2,\rm TGL}|}{5s}.
\]

**D mede a distância da previsão ao centro público de planejamento, não à verdade hipotética.** Por isso `D = 0` seria um erro de implementação, não uma consequência de “verdade = previsão”.

A razão de veredito congelada é

\[
m_2=\sqrt{10\mu}\ {\rm meV},\qquad
\sigma_{m_2}=\frac{5\sigma_\mu}{m_2}
=\frac{m_2\sigma_\mu}{2\mu},\qquad
r_{m_2}=\frac{m_2|m_2-m_{2,\rm TGL}|}{5\sigma_\mu}.
\]

O rascunho K01 passou a Δm² sem declarar emenda; a correção fica ao lado. [PRE_REGISTRO_CEGO_RASCUNHO_K01](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Ccadeia_de_selo%5Cv412%5Ckimi%5CPRE_REGISTRO_CEGO_RASCUNHO_K01.md&line=36&text=propaga%C3%A7%C3%A3o%20%CF%83_m%E2%82%82%20%E2%89%88%20%CF%83(%CE%94m%C2%B2%E2%82%82%E2%82%81)/(2m%E2%82%82) "citation")

### 1.1 Medida ou incremento independente

**(a1) Posterior público de planejamento, com prior plano declarado:**

\[
\mu\sim N(7,388,0,078^2),\qquad X\mid\mu\sim N(\mu,s^2)
\quad\Rightarrow\quad X\sim N(7,388,0,078^2+s^2).
\]

O erro atual entra uma única vez. Esse “posterior” é construção de planejamento, não publicado pela colaboração.

**(a2) Verdade = previsão:** \(X\sim N(\Delta_{\rm pred},s^2)\), sem erro atual adicional.

### 1.2 Liberação cumulativa com covariância

Seja `X0` o estimador atual e `X` o cumulativo futuro, com `Cov(X0,X)=C`:

\[
\operatorname{Var}(X)=0,078^2+s^2-2C.
\]

**(b1) Posterior público cumulativo:** usa média 7,388 e essa variância.

**(b2) Verdade = previsão condicionada ao valor atual observado \(X_0=x_0\):**

\[
E[X\mid X_0=x_0]
=\Delta_{\rm pred}+\frac{C}{0,078^2}(x_0-\Delta_{\rm pred}),
\]

\[
\operatorname{Var}(X\mid X_0=x_0)
=s^2-\frac{C^2}{0,078^2}.
\]

Com `C = 0`, essa distribuição condicional reduz exatamente a (a2): média \(\Delta_{\rm pred}\) e variância \(s^2\). Não se usa simples \(N(\Delta_{\rm pred},s^2)\) no cenário cumulativo com covariância não nula.

**Brinquedo aninhado de informação nova independente:** `C = s²`, logo

\[
\operatorname{Var}(X)=0,078^2-s^2,
\qquad
\operatorname{Var}(X\mid X_0=x_0)
=s^2(1-s^2/0,078^2).
\]

Esse `C=s²` **não é uma covariância atribuída ao JUNO**. A covariância real é `[OPEN]` e deve ser fornecida pela colaboração ou por ajuste conjunto com nuisances.

### 1.3 Caudas na métrica frozen

Para Δm², as caudas são normais. Para m₂, defino \(Y=\sqrt{10X}\) e \(r=Y|Y-m_{2,\rm TGL}|/(5s)\); as raízes usadas na CDF são

\[
Y_+=\frac{m_{2,\rm TGL}+\sqrt{m_{2,\rm TGL}^2+20ts}}2,
\qquad
Y_-=\frac{m_{2,\rm TGL}-\sqrt{m_{2,\rm TGL}^2-20ts}}2 .
\]

O script devolve separadamente `P(r≤1)`, `P(1<r<3)`, `P(3≤r<5)` e `P(r≥5)`. [resultados_planejamento](K04/M2/medidas/resultados_planejamento.json)

---

## 2. Tabelas independentes — somente medida/incremento independente

### (a1) Posterior público

| Precisão | σ | DΔ | D_m₂ | P(r≤1) | P(1<r<3) | P(3≤r<5) | P(r≥5), frozen | PΔ(r≥5) | Ramo r<3 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0,7 % | 0,051716 | 2,908008 | 2,922959 | 14,563479 % | 37,117002 % | 35,441905 % | 12,877614 % | 12,384071 % | UNDER |
| 0,5 % | 0,036940 | 4,071211 | 4,092143 | 9,424274 % | 22,731850 % | 32,803157 % | 35,040719 % | 34,553737 % | UNDER |
| 0,407121 % | 0,030078 | 5,000001 | 5,025709 | 7,499826 % | 15,986966 % | 26,147929 % | 50,365280 % | 50,016055 % | ARMED |
| 0,324061 % | 0,023942 | 6,281550 | 6,313847 | 6,056849 % | 10,668509 % | 18,397100 % | 64,877542 % | 64,702532 % | ARMED |
| 0,3 % | 0,022164 | 6,785352 | 6,820238 | 5,687768 % | 9,310023 % | 16,097589 % | 68,904620 % | 68,786155 % | ARMED |
| Tabela 6, σ = 0,024 | 0,024000 | 6,266272 | 6,298490 | 6,069337 % | 10,714638 % | 18,473119 % | 64,742906 % | 64,566086 % | ARMED |

### (a2) Verdade = previsão

| Precisão | σ | DΔ | D_m₂ | P(r≤1) | P(1<r<3) | P(3≤r<5) | P(r≥5), frozen | PΔ(r≥5) | Ramo r<3 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0,7 % | 0,051716 | 2,908008 | 2,922959 | 84,091518 % | 15,766349 % | 0,142097 % | 0,000036 % | 0,000057 % | UNDER |
| 0,5 % | 0,036940 | 4,071211 | 4,092143 | 84,103737 % | 15,756174 % | 0,140055 % | 0,000034 % | 0,000057 % | UNDER |
| 0,407121 % | 0,030078 | 5,000001 | 5,025709 | 84,109426 % | 15,751434 % | 0,139107 % | 0,000033 % | 0,000057 % | ARMED |
| 0,324061 % | 0,023942 | 6,281550 | 6,313847 | 84,114522 % | 15,747186 % | 0,138261 % | 0,000032 % | 0,000057 % | ARMED |
| 0,3 % | 0,022164 | 6,785352 | 6,820238 | 84,115999 % | 15,745954 % | 0,138015 % | 0,000032 % | 0,000057 % | ARMED |
| Tabela 6, σ = 0,024 | 0,024000 | 6,266272 | 6,298490 | 84,114473 % | 15,747226 % | 0,138269 % | 0,000032 % | 0,000057 % | ARMED |

**D é idêntico ao da tabela (a1), inclusive a coluna de ramo.** A hipótese não zera nem redefine o planning.

---

## 3. Tabelas cumulativas — somente o brinquedo `C = s²`

### (b1) Posterior público cumulativo

| Precisão | σ | DΔ | D_m₂ | P(r≤1) | P(1<r<3) | P(3≤r<5) | P(r≥5), frozen | PΔ(r≥5) | Ramo r<3 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0,7 % | 0,051716 | 2,908008 | 2,922959 | 4,537286 % | 48,154903 % | 43,828989 % | **3,478822 %** | 3,195125 % | UNDER |
| 0,5 % | 0,036940 | 4,071211 | 4,092143 | 4,925529 % | 23,099842 % | 40,509010 % | 31,465619 % | 30,874110 % | UNDER |
| 0,407121 % | 0,030078 | 5,000001 | 5,025709 | 4,724292 % | 15,328371 % | 29,523025 % | 50,424312 % | 50,001481 % | ARMED |
| 0,324061 % | 0,023942 | 6,281550 | 6,313847 | 4,422500 % | 10,018415 % | 19,287900 % | 66,271184 % | 66,044954 % | ARMED |
| 0,3 % | 0,022164 | 6,785352 | 6,820238 | 4,318779 % | 8,734194 % | 16,589445 % | 70,357583 % | 70,187987 % | ARMED |
| Tabela 6, σ = 0,024 | 0,024000 | 6,266272 | 6,298490 | 4,425796 % | 10,062417 % | 19,379309 % | **66,132478 %** | 65,904386 % | ARMED |

Os benchmarks pedidos ficam assim confirmados por script: **12,88 % → 3,48 %** a 0,7 % e **64,74 % → 66,13 %** na Tabela 6, aproximadamente.

### (b2) Verdade = previsão condicionada ao valor atual observado

| Precisão | σ_condicional | DΔ | D_m₂ | P(r≤1) | P(1<r<3) | P(3≤r<5) | P(r≥5), frozen | PΔ(r≥5) | Ramo r<3 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0,7 % | 0,038714426 | 2,908008 | 2,922959 | 35,411892 % | 63,454110 % | 1,133954 % | **0,000044650 %** | **0,000033222 %** | UNDER |
| 0,5 % | 0,032534742 | 4,071211 | 4,092143 | 53,871682 % | 45,206172 % | 0,921940 % | 0,000206305 % | 0,000173995 % | UNDER |
| 0,407121 % | 0,027751832 | 5,000001 | 5,025709 | 60,906316 % | 38,350405 % | 0,743053 % | 0,000226218 % | 0,000198191 % | ARMED |
| 0,324061 % | 0,022785907 | 6,281550 | 6,313847 | 66,568313 % | 32,849213 % | 0,582273 % | 0,000200946 % | 0,000181484 % | ARMED |
| 0,3 % | 0,021250371 | 6,785352 | 6,820238 | 68,109754 % | 31,352299 % | 0,537759 % | 0,000188316 % | 0,000171604 % | ARMED |
| Tabela 6, σ = 0,024 | 0,022835662 | 6,266272 | 6,298490 | 66,516974 % | 32,899068 % | 0,583756 % | **0,000201329 %** | **0,000181779 %** | ARMED |

A variância condicional correta é \(s^2-C^2/0,078^2\), não a variância total cumulativa. Com `C = 0`, (b2) reduz exatamente a (a2). As linhas continuam sendo brinquedo condicional, não probabilidade publicada pelo JUNO.

### 3.1 Ramos e ausência real de S

| Faixa | Ramo |
|---|---|
| `r_P ≤ 1` | Com S realmente `ABSENT`, segue `UNDER` se `D_P < 5` e `ARMED_CONSISTENT` se `D_P ≥ 5`. Só há `MATCHED` se existir S independente com `r_S ≤ 1`; sem esse S, a probabilidade conjunta é zero. |
| `1 < r_P < 3` | `UNDER` se `D_P < 5`; `ARMED_CONSISTENT` se `D_P ≥ 5`. O D é o mesmo em todas as hipóteses. |
| `3 ≤ r_P < 5` | `TGL_NU_M2_TENSION__P`. |
| `r_P ≥ 5` | `T_SINGLE(P)_AWAITING_S` se ratificado; caso contrário `OPEN_RULE_GAP`. Não é FALSIFIED. |
| `FALSIFIED` | Depende de S independente com `r_S ≥ 5`; zero somente quando S é realmente `ABSENT`. |
| `MATCHED` | Depende de S independente com `r_S ≤ 1`; zero somente quando S é realmente `ABSENT`; nunca `CONFIRMED`. |

---

## 4. Desempenho real e exposições: nominal não é full‑reactor

A Tabela 6 publica σ = 0,074 em 100 dias, 0,024 em seis anos e 0,017 em vinte. A fonte converte esses tempos, pelo ciclo 11/12, em aproximadamente **92, 2009 e 6696 dias com potência plena dos reatores**. Portanto:

- 100 dias **nominais** ≈ 92 dias full‑reactor;
- seis anos ≈ 2009 dias full‑reactor;
- vinte anos ≈ 6696 dias full‑reactor.

Não se deve usar o coeficiente de 100 nominais numa variável T medida em full‑reactor. [JUNO, arXiv:2204.13249](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2204.13249&text=will%20be%20determined%20to%20better%20than%200.5%25%20precision%20in%20six%20years "citation")

\[
D_\Delta(0,024)=6,266272<6,281552=D90,
\qquad D_{m_2}(0,024)=6,298490 .
\]

### 4.1 Comparação real de 59,1/207,2 dias com o projeto

| Quantidade | Conta | Resultado |
|---|---|---:|
| σ de projeto escalado para 207,2 d | `0,074 × √(100/207,2)` | **0,051409** |
| σ real publicado | fonte JUNO | **0,078** |
| razão real/projeto | `0,078/0,051409` | **1,517252** |
| redução real 59,1 → 207,2 d | `0,12/0,078` | **1,538462** |
| redução √T ingênua | `√(207,2/59,1)` | **1,872411** |

As análises mudaram volume fiducial, seleção, fundos e âncoras de espectro. Isso não mede um piso de sistemática. O orçamento publicado informa volume fiducial 0,96 %, prótons‑alvo 1,0 %, eficiência combinada 1,4 %, espectro de referência 1,2 %, potência térmica 0,5 %, fração de fissão 0,6 %, combustível gasto 0,3 %, não equilíbrio 0,3 % e diferença entre frações 0,1 %. Bi–Po e eficiência são significativos e redutíveis; a decomposição numérica σ_stat/σ_sys de Δm²₂₁ permanece `[OPEN]`. [JUNO 207,2 d, Tabelas II–III](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fpdf%2F2609.37895&text=Detection%20efficiency "citation")

### 4.2 Cenários próprios desde 207,2 dias — sem ligação com (a1)

**Sem piso**, \(\sigma(T)=0,078\sqrt{207,2/T}\):

| Alvo | σ alvo | T total | Adicional cumulativo | Data ideal cumulativa* | Dias novos no incremento | Data ideal incremento* |
|---|---:|---:|---:|---|---:|---|
| 5σ | 0,030078 | 1393,41 d | 1186,21 d | 16/08/2029 | 1393,41 d | 11/03/2030 |
| D90 | 0,023942 | 2199,24 d | 1992,04 d | 31/10/2031 | 2199,24 d | 25/05/2032 |

\* Aritmética desde 18/05/2026, com 100 % de dias vivos e centro parado; não é cronograma nem liberação anunciada. **Essas datas não herdam as probabilidades do modelo independente (a1).**

**Piso ilustrativo dos dois pontos reais:** \(\sigma^2=a/T+s_0^2\) dá `a = 0,687601` e `s0 = 0,052588`, tornando 5σ/D90 inalcançáveis nesse brinquedo. Dois pontos ajustam dois parâmetros e as análises mudaram: não é piso medido.

### 4.3 Brinquedo decomposição do projeto — full‑reactor versus inteiramente nominal

Defino, separadamente,

\[
a_{\rm full}=92\times0,074^2,\qquad
a_{\rm nom}=100\times0,074^2,
\]

\[
{\rm floor\_full\_sq}=0,024^2-a_{\rm full}/2009,
\qquad
{\rm floor\_nominal\_sq}=0,024^2-a_{\rm nom}/2191 .
\]

Assim `s0_full = 0,018034202` e **`s0_nominal = 0,018057366`**. Para cada alvo,

\[
T_{\rm full}=a_{\rm full}/(target^2-{\rm floor\_full\_sq}),
\qquad
T_{\rm nom}=a_{\rm nom}/(target^2-{\rm floor\_nominal\_sq}) .
\]

| Alvo | Dias full‑reactor | Data convertida por 2009 dias em 6 anos | Dias inteiramente nominais | Data inteiramente nominal |
|---|---:|---|---:|---|
| 5σ | 869,416 | **31/03/2028** | 946,383 | **29/03/2028** |
| D90 | 2031,675 | **19/09/2031** | 2215,813 | **19/09/2031** |

Os benchmarks pedidos ficam confirmados por script. As datas anteriores 15/05/2028 e 18/09/2031, e a data nominal R2 12/09/2031, ficam históricas em REV0/REV1.

Tudo nesta subseção é **brinquedo decomposição em quadratura**, não curva publicada nem cronograma. Nenhuma precisão nova foi inventada para ajustar datas.

---

## 5. Métrica, datas e prospectividade

**Vale `NEUTRINO_M2_V2`, em m₂.** A `kill_rule` exige `|m2_obs−m2_TGL|/σ_obs ≥ 5` em duas determinações independentes, com hash `e24877751ad810225412cc294c06b83eefeaedc67e4c5cabc7779ac01e4b19c3` e porte de 08/08/2026. [um_absoluto, frozen](kimi-cite://text?path=C%3A%5CIALD%5CArtigo%5CHaja_Luz%5CA%20Ponte%20e%20o%20Um%5CN%C3%B3s%5Cum_absoluto.json&text=FALSIFIED%20sse%20%7Cm2_obs%20-%20m2_TGL%7C%2Fsigma_obs%20%3E%3D%205 "citation")

| Forma | Resultado em 207,2 dias |
|---|---:|
| frozen, m₂, primeira ordem | **1,937997** |
| Δm² | **1,928084** |

Se se propuser Δm², deve-se declarar **EMENDA DE MÉTRICA**, com versão nova, hash e ato do operador anterior ao próximo centro. A Tabela 6 fica abaixo de D90 em Δm² e acima em m₂: a escolha altera a fronteira.

Cronologia:

- **08/08/2026:** V2 hasheada; a emissão inicial declara tensão conhecida e cegueira apenas prospectiva.
- **04/09/2026:** SNO+ v4 depositado; revisão do mesmo conjunto, não uma medida mundial nova irrestrita.
- **29/09/2026:** liberação JUNO 207,2 dias; primeira nova determinação **JUNO** posterior ao hash.
- **30–31/10/2026:** esta casa leu e reproduziu as tensões, inclusive 1,938σ. [determinacoes_m2_30out](kimi-cite://text?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Cneutrino_E0_autonomia_30out%5Cdeterminacoes_m2_30out.json&text=%22z_sigma%22%3A%201.9379969609289271 "citation")

A função documental devolve **`TGL_NU_M2_ARMED_CONSISTENT`**, não TENSION/FALSIFIED/MATCHED. Eu não a executei agora. A liberação é prospectiva no calendário da regra, mas **não cega para a casa**, pois centro e erro já foram comunicados e lidos.

---

## 6. Incremento 59,1 → 207,2 e desenho com dados novos

Com \(w_1=1/0,12^2\) e \(w_2=1/0,078^2\),

\[
\mu_\Delta=\frac{w_2(7,388)-w_1(7,50)}{w_2-w_1}
=7,306061,\qquad
\sigma_\Delta=(w_2-w_1)^{-1/2}=0,102640 .
\]

| Quantidade | Resultado |
|---|---:|
| centro ilustrativo | **7,306061** |
| σ ilustrativo | **0,102640** |
| r contra previsão, Δm² | **0,666902** |
| r contra previsão, frozen m₂ | **0,668472** |
| distância ao centro 7,50 | **1,889502σ_incremento** |

Não é determinação independente: a liberação é cumulativa e muda seleção, volume fiducial, fundos e âncora TAO/Daya Bay. A conta também trata erros totais como pesos estatísticos separáveis.

Não localizei coeficiente de correlação ou matriz de covariância entre os estimadores 59,1 e 207,2 dias. O erro correto do incremento é **[OPEN]**; 0,102640 é só a ilustração de variância inversa.

### 6.1 Estimador e covariância futuros

O desenho precisa de amostra posterior a 18/05/2026, temporalmente disjunta, e de ajuste conjunto/condicional que entregue

\[
\Sigma=
\begin{pmatrix}
V_{\rm old} & C_{\rm old,new}\\
C_{\rm old,new} & V_{\rm new}
\end{pmatrix},
\]

com nuisances compartilhados de escala/não linearidade de energia, fluxo, eficiência, fundos e resposta do detector. Uma diferença de estimadores cumulativos tem `V(d)=V_cum+V_old−2C`; sem `C` e sem a resposta conjunta, a precisão incremental não é identificável.

O estimador candidato é `μ̂_new` da likelihood dos eventos novos condicionada ao estado anterior, ou ajuste conjunto completo. Seleção, nuisances, versão e cortes precisam ser congelados antes do novo centro.

Sem piso, o incremento sozinho exige **1393 dias novos para 5σ** e **2199 para D90**, sem subtrair 207,2. Datas ideais: 11/03/2030 e 25/05/2032. Com o piso ilustrativo 0,052588, ambos são inalcançáveis. Poder real continua condicionado a covariância, centro e sistemáticas.

---

## 7. Segunda testemunha sem JUNO: determinações e independência real

A convenção de r é frozen. Em assimetrias usa‑se o erro do lado da previsão; `σ5` é o erro que bastaria para 5σ com centro parado. Números públicos: `[KNOWN, a conferir]`; r/σ5: `[DERIVED—PLANEJAMENTO]`.

| Entrada | Centro e erro | σ usado | r frozen | σ5 | Experimento, ano e ID consultado | Papel/independência |
|---|---|---:|---:|---:|---|---|---|
| JUNO 207,2 d | 7,388 ± 0,078 | 0,078 | **1,937997** | 0,030233 | JUNO, 2026, [arXiv:2609.37895v1](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2609.37895 "citation") | P; não S |
| SNO+ | 7,91 (+0,22/−0,25) | 0,250 | **2,749285** | 0,137464 | SNO+, 2026, [PRL 137, 101807; DOI 10.1103/mv5z-pfb7](kimi-cite://web?url=https%3A%2F%2Fdoi.org%2F10.1103%2Fmv5z-pfb7 "citation"), arXiv:2511.11856v4 | Direta, sem JUNO; covariância de fluxo/nuisances OPEN |
| SK‑Gd reator | 9,08 (+0,55/−0,54) | 0,540 | **3,605064** | 0,389347 | SK, 2026, [arXiv:2610.03143v1](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2610.03143 "citation") | Direta, sem JUNO; cenário, não agenda/prova |
| KamLAND‑only | 7,54 (+0,19/−0,18) | 0,180 | **1,697137** | 0,061097 | KamLAND, 2013, [PRD 88, 033001; arXiv:1303.4667v2, Tabela 3](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F1303.4667v2 "citation"), DOI 10.1103/PhysRevD.88.033001 | Direta, sem JUNO; covariância OPEN |
| Solares sem KamLAND | 6,10 (+0,95/−0,81) | 0,950 | **1,146322** | 0,217801 | SK + solares, 2024, [PRD 109, 092001; arXiv:2312.12907v2](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2312.12907 "citation"), DOI 10.1103/PhysRevD.109.092001 | Uma família; covariância OPEN |
| JUNO 59,1 d | 7,50 ± 0,12 | 0,120 | **2,206054** | 0,052945 | JUNO, 2025/2026, [arXiv:2511.14593v1](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2511.14593 "citation"), DOI 10.1038/s41586-026-10538-z | Subconjunto de P |
| NuFIT 6.1 | 7,537 (+0,100/−0,094) | 0,094 | **3,217279** | 0,060485 | NuFIT, 2025, [release notes 6.1](kimi-cite://web?url=http%3A%2F%2Fwww.nu-fit.org%2Fsites%2Fdefault%2Ffiles%2Fv61.release-notes.pdf "citation"); [arXiv:2601.09791 associado](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2601.09791 "citation") | Global com JUNO 59 d; conjunto OPEN |
| Capozzi et al. | 7,48 ± 0,10 | 0,100 | **2,443867** | 0,048877 | Capozzi et al., 2025/2026, [arXiv:2511.21650](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2511.21650 "citation"), DOI 10.1103/cxqw-1bty | Global com JUNO/SNO+; conjunto OPEN |
| Bari 2026.a NO | 7,465 (+0,072/−0,080) | 0,080 | **2,864363** | 0,045830 | Bari, 2026, [Global‑nu release 2026.a](kimi-cite://web?url=https%3A%2F%2Fglobal-nu.org%2Fresults.html "citation") | **Preliminar, paper in preparation; não artigo primário publicado; conjunto OPEN** |
| SK‑Gd solar+reator | 8,94 (+0,46/−0,47) | 0,470 | **3,813218** | 0,358442 | SK, 2026, [arXiv:2610.03143v1](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2610.03143 "citation") | Mesma colaboração; conjunto OPEN |
| SNO+ reator+solar, final | 7,59 ± 0,17 | 0,170 | **2,097521** | 0,071316 | SNO+, 2026, [PRL 137, 101807, Tabela 3](kimi-cite://web?url=https%3A%2F%2Fdoi.org%2F10.1103%2Fmv5z-pfb7 "citation") | Sem JUNO; não somar SNO+ duas vezes; conjunto OPEN |

**Errata de versões:** SNO+ v1/v2 trazia 7,93 e 7,63; a versão final PRL/v4 traz 7,91 e 7,59. KamLAND‑only 7,54 vem da Tabela 3, não do ajuste solar+KamLAND 7,53 do resumo. [SNO+ v2](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2511.11856v2 "citation")

### 7.1 Alguma chega a σ_S ≤ 0,0301?

**Nenhuma das dez entradas, combinação citada ou previsão consultada demonstra essa precisão.** O alvo Δm² é 0,030078; o alvo frozen no centro JUNO é 0,030233. Mas o corte não é necessário para 5σ, pois σ5 depende do centro:

- SK‑Gd: `σ5 = 0,389347`; 411,52 dias atuais → 791,5985536 totais e **380,0785536 adicionais** no cenário √T.
- SNO+: `σ5 = 0,137464`; 685 dias → 2265,6402185 totais e 1580,6402185 adicionais.
- KamLAND: `σ5 = 0,061097`; o fator de informação não é plano operacional.
- Solares: `σ5 = 0,217801`, sem exposição única.

Essas equivalências não são datas, não provam independência e não são estatística observada nova. [determinacoes_m2_30out](kimi-cite://text?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Cneutrino_E0_autonomia_30out%5Cdeterminacoes_m2_30out.json&text=%22exposicao_adicional_dias%22%3A%20380.07855357458413 "citation")

---

## 8. MATCHED: avaliação conjunta P+S, sem independência fingida

O modelo usado apenas como **brinquedo identificável** é

\[
P\sim N(7,388,0,078^2),\qquad
S\sim N(\mu_S,\sigma_S^2),\qquad C_{PS}=0 .
\]

`C_PS = 0` permite calcular o produto das probabilidades marginais frozen de `r_P≤1` e `r_S≤1`, mas **não é prova de independência física**: fluxos de reator, modelo espectral, calibração e nuisances podem correlacionar-se e não têm covariância pública completa.

| S | P(r_P≤1) | P(r_S≤1) | P(MATCHED), brinquedo C=0 | Avaliação real |
|---|---:|---:|---:|---|
| SNO+ | 17,599161 % | 4,476223 % | **0,787778 %** | Só brinquedo; C real OPEN |
| SK‑Gd reator | 17,599161 % | 0,756582 % | **0,133152 %** | Só brinquedo; C real OPEN |
| KamLAND | 17,599161 % | 24,635184 % | **4,335586 %** | Só brinquedo; C real OPEN |
| Solares sem KamLAND | 17,599161 % | 98,493504 % | **17,334031 %** | Só brinquedo; C real OPEN |
| JUNO 59,1 d | 17,599161 % | OPEN | OPEN | Subconjunto de P; não S |
| NuFIT 6.1 | 17,599161 % | OPEN | OPEN | Contém JUNO; conjunto não identificável |
| Capozzi et al. | 17,599161 % | OPEN | OPEN | Contém JUNO/SNO+; conjunto não identificável |
| Bari 2026.a NO | 17,599161 % | OPEN | OPEN | Preliminar e contém JUNO/SK‑Gd; conjunto não identificável |
| SK‑Gd solar+reator | 17,599161 % | OPEN | OPEN | Mesma colaboração; covariância não publicada |
| SNO+ reator+solar | 17,599161 % | OPEN | OPEN | Compartilha dados/fluxos com componentes; não identificável |

Essas probabilidades são modelos de planejamento, não frequências de veredito observado. Para Hyper‑K/DUNE não há centro medido nem covariância P+S: **MATCHED = OPEN**, não zero presumido.

---

## 9. Previsões e classe das fontes

| Fonte | Classe e previsão | Consequência para S |
|---|---|---|
| Hyper‑Kamiokande | O documento de status da colaboração descreve construção do tanque em 2026, instalação de PMTs em 2027 e **commissioning antes dos primeiros dados em 2028**. O estudo de cinco anos do arXiv:1309.0184 fala em amplitude zênite ≈0,5 % e precisão Δm²₂₁ comparável à dos reatores então vigentes, não 0,407 %. Cinco anos é tentativa posterior ao início, não data de precisão assegurada. [Status of the Hyper‑Kamiokande experiment, colaboração, 2026](kimi-cite://web?url=https%3A%2F%2Findico.cern.ch%2Fevent%2F1568942%2Fcontributions%2F6841210%2F "citation"), [Hyper‑K, arXiv:1309.0184](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F1309.0184 "citation") | Não fornece σ ≤ 0,0301 nem calendário que o demonstre. |
| DUNE solar | **5,9 % em Δm²₂₁ por 100 kton·ano é previsão de Capozzi et al., teóricos, não da DUNE Collaboration.** Requer investimentos e não traz orçamento completo de sistemáticas. [Capozzi et al., arXiv:1808.08232v3](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F1808.08232v3 "citation") | Muito longe de 0,407 %. |
| DUNE com NC | A via dia–noite de Capozzi continua melhor para Δm²₂₁; NC melhora sobretudo θ₁₂ e fluxo. O texto situa o programa em torno de 2030, não uma medida a 0,407 %. [Meighen‑Berger et al., arXiv:2410.00330](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2410.00330v1 "citation") | Não altera a conclusão. |
| JUNO solar | Previsão de 20 % em Δm²₂₁ em dez anos, modelo‑independente. [JUNO, arXiv:2210.08437](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2210.08437 "citation") | Não serve ao corte e não é independente do P JUNO. |
| SNO+ continuado | A previsão de três anos para superar a precisão global então vigente é **antiga**; o calendário atual e a precisão correspondente ficam `[OPEN]`, não uma promessa atual. [SNO+ Results](kimi-cite://web?url=https%3A%2F%2Fsnoplus.phy.queensu.ca%2Fresults.html "citation") | Não há previsão atual suficiente para o corte. |
| Bari 2026.a | **Preliminary version, paper in preparation; não fonte primária publicada.** | Pode ficar como estresse preliminar, nunca como independência publicada. |

**Leitura probatória:** não há segunda testemunha com σ ≤ 0,0301 demonstrada. SK‑Gd continua sendo cenário condicional, não agenda nem prova de independência. A conclusão “sem negativo não é teste” permanece condicional à regra e ao desenho, sem universal falso.

---

## 10. Correções menores K01, apenas propostas

Não editei `CANAIS_K01.json`, `PRE_REGISTRO_CEGO_RASCUNHO_K01.md` nem `K01_validar.py`.

1. **UNDER nunca exercido / D padrão 6.** O padrão `d_p = d_s = 6,0` força ARMED. Uma revisão futura deve incluir `d_p = 4` para UNDER e `d_p = None` para `AWAIT_SOURCE`, usando o D documental. [K01_validar](kimi-cite://text?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Ccadeia_de_selo%5Cv412%5Ckimi%5CK01_validar.py&text=def%20veredito_sintetico "citation")
2. **Sub‑rótulos colapsados.** Proposta: devolver token principal com campos `reason`, `P_band`, `S_band`, `S_state`, `D_P`, `D_S`, `awaiting`.
3. **S INVALID não esconde P ≥ 5.** O ramo continua `INCONCLUSIVE_SYSTEMATICS__INTEGRITY_S`, com estresse obrigatório `stress_P = {r_P, band: "≥5", D_P}` ao lado. [REVISAO_K01, B3](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Ccadeia_de_selo%5Cv412%5Crevisao%5CREVISAO_K01.md&line=47&text=S%20INVALID%20esconde%20um%20P%20%E2%89%A5%205%CF%83 "citation")

Nenhum desses casos foi executado.

---

## 11. Reprodutibilidade, REV0/REV1 e bloqueios

- `K04/M2/REV0/`: versão original e `hashes_REV0.txt`, preservada sem alterações.
- `K04/M2/REV1/`: versão R2 e `hashes_REV1.txt`, preservada antes desta R3.
- `K04/M2/scripts/medidas_planejamento.py`: modelos independente, cumulativo, condicional, exposições e MATCHED; biblioteca padrão.
- `K04/M2/scripts/extrair_contexto_juno.py`: leitura bibliográfica em memória, sem salvar PDF nem dados de eventos.
- `K04/M2/medidas/resultados_planejamento.json`: valores completos.
- `K04/M2/medidas/tabelas_planejamento.md`: tabelas geradas pelo script.
- `K04/M2/medidas/execucao_planejamento.txt`: saída das contas, não de teste empírico.
- `K04/M2/medidas/hashes_R3.txt`: hashes desta revisão.
- [ERRATA_M2_K04_R3](ERRATA_M2_K04_R3.md): duas novas correções ao lado, sem instalação no core; [ERRATA_M2_K04_R2](ERRATA_M2_K04_R2.md) também foi atualizada para não repetir a fórmula inválida.

**Bloqueios:** covariância inter-liberações e P–S não publicada; decomposição σ_stat/σ_sys de Δm²₂₁ em 207,2 dias ausente; covariância real de fluxos/nuisances compartilhados ausente; próxima liberação desconhecida; Bari preliminar; decisão de métrica/limiar/fonte é do operador. Nenhum bloqueio foi resolvido por ajuste de escala ou regra.
