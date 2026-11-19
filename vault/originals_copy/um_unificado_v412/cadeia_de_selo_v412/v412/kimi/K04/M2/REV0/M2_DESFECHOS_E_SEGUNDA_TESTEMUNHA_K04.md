# K04/B — m₂: desfechos, calendário, incremento e segunda testemunha

**Estatuto geral:** `[DECLARADO]` para o desenho; `[DERIVED—PLANEJAMENTO]` para toda conta feita com números públicos agregados; `[KNOWN, a conferir]` para literatura; `[OPEN]` para o que a fonte não fornece. Nenhum vetor de dados foi baixado ou lido, nenhuma likelihood foi aberta, nenhuma estatística observada nova foi calculada, nada de H0DN foi executado e nenhum teste foi realizado. As fórmulas foram avaliadas analiticamente, sem simulação e sem semente.

## Conclusão antes das contas

1. **Hoje não há par publicado que satisfaça `FALSIFIED` nem par que satisfaça `MATCHED_PROSPECTIVELY`.** Com S ausente, a regra só devolve `UNDER/ARMED`, `TENSION_P` ou `SINGLE_P/OPEN_RULE_GAP`; `FALSIFIED` e `MATCHED` ficam formalmente dependentes de S. O desfecho negativo **não está assegurado pelo desenho**: um teste que não pode devolver o negativo não é teste.
2. **A afirmação universal “FALSIFIED é inalcançável na prática” seria forte demais e deve ser corrigida aqui.** O próprio inventário traz SK‑Gd reator a **3,605σ**. Se o centro 9,08 e a forma do erro persistirem, uma equivalência meramente condicional \(\sigma\propto T^{-1/2}\) leva a 5σ com **380 dias adicionais**, antes do JUNO atingir 5σ nos cenários abaixo. Isso não é cronograma nem resultado futuro, mas é um contraexemplo à impossibilidade prática absoluta. O correto é: **a regra atual não garante morte; sem uma segunda fonte pré-fixada e com poder demonstrado, pode devolver apenas tensão para sempre.**
3. **Vale a métrica congelada em m₂ até emenda do operador:** `r_m₂ = 1,937997 ≈ 1,9380`; em Δm², `r_Δ = 1,928084`. Não troquei a regra. Para o D de planejamento em Δm², a Tabela 6 dá **6,266272 < 6,281552 = D90**; a frase anterior “0,3 % supera D90” veio de substituir o σ absoluto publicado por uma porcentagem arredondada.
4. A liberação de 207,2 dias, de **29/09/2026**, é a primeira nova determinação JUNO posterior ao hash da V2 de **08/08/2026** e, nesse sentido cronológico estrito, a primeira leitura prospectiva da regra. Ela devolve `TGL_NU_M2_ARMED_CONSISTENT`, pois `r_m₂ < 3` e nenhuma segunda independência ≥5 existe. **Não é leitura cega para esta casa**, que leu centro e tensão em 30–31/10/2026; a cegueira experimental da colaboração não é herdada por quem já conhece o resultado. [um_absoluto](kimi-cite://text?path=C%3A%5CIALD%5CArtigo%5CHaja_Luz%5CA%20Ponte%20e%20o%20Um%5CN%C3%B3s%5Cum_absoluto.json&text=%22nao_e_cego_nesta_emissao%22 "citation"), [e0-cadeia-conferencia-kimi-e-no-go-31out](kimi-cite://md-line?path=C%3A%5CUsers%5Crotol%5C.claude%5Cprojects%5Cc--IALD-Central-de-Patentes%5Cmemory%5Ce0-cadeia-conferencia-kimi-e-no-go-31out.md&line=10&text=dez%20determina%C3%A7%C3%B5es%20p%C3%BAblicas "citation")
5. **Q1 para o operador, sem escolha feita aqui:** a regra de morte congelada em agosto não dispara com as determinações atuais e não tem negativo assegurado; manter e assumir que o canal devolve só tensão, emendar para uma testemunha com limiar explícito, ou pré-fixar uma segunda linha como SK‑Gd com covariância e regras de robustez? Toda mudança de fórmula, fonte, métrica ou limiar é **emenda declarada e ato do operador**, nunca ajuste ao centro observado.

### Três alternativas e seus custos

| Alternativa | O que preserva | Custo e condição |
|---|---|---|
| **A — manter duas independências ≥5 e anunciar “somente tensão” até haver par** | Regra frozen integral; nenhuma emenda de fórmula | Pode nunca produzir FALSIFIED nem MATCHED; o resultado mais provável de um P alto continua `SINGLE_P/OPEN_RULE_GAP`. Exige dizer que não é teste decisivo enquanto S não tiver poder. |
| **B — uma testemunha com limiar explícito** | Pode restaurar a possibilidade lógica de negativo | É emenda. Candidatos a declarar antes do centro novo: `r_P ≥ 5` em m₂, ou poder de desenho `D_P ≥ 6,281552` junto de `r_P ≥ 5`, com incremento disjunto, covariância publicada, todas as tentativas e estresses visíveis. Custa a perda da réplica independente e aumenta a assimetria entre morte e concordância. O limiar exato não foi escolhido aqui. |
| **C — manter a dupla exigência, mas pré-fixar SK‑Gd como S admissível, sem exigir σ_S ≤ 0,0301** | A fórmula de duas independências pode permanecer inalterada | Só muda a nomeação/versão da fonte, que também deve ser emenda se o rascunho K01 ainda não a tiver fixado. Exige covariância, congelamento da análise, tolerância a erro grande e aceitação de que o centro pode se mover. O limiar 0,0301 é suficiente para S perto de 7,388, **não necessário** para um S distante como 9,08. |

`MATCHED` continua sem par atual a ≤1σ nas duas linhas e, mesmo se futuramente alcançado, não significa `CONFIRMED`.

---

## 1. O que é D e qual é o nulo de planejamento

Em unidades de \(10^{-5}\,\mathrm{eV}^2\),

\[
\Delta_{\rm pred}=7,237609466718292,\qquad
\Delta_0=7,388,\qquad
\delta=\Delta_0-\Delta_{\rm pred}=0,150390533281708 .
\]

O D usado no planejamento em Δm² é

\[
D_\Delta(s)=\frac{\delta}{s},
\]

onde \(s\) é o erro futuro. **D mede a distância da previsão ao centro que o JUNO já mediu; o nulo fiducial é “o centro de hoje é a verdade”.** Não é um Z observado nem uma nova tensão calculada nesta K04. Os centros e erros públicos são de 59,1 e 207,2 dias. [JUNO 59,1 d](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2511.14593 "citation"), [JUNO 207,2 d](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2609.37895 "citation")

A razão de veredito congelada é distinta do D de planejamento:

\[
m_2=\sqrt{10\mu}\ {\rm meV},\qquad
\sigma_{m_2}=\frac{5\sigma_\mu}{m_2}
=\frac{m_2\sigma_\mu}{2\mu},\qquad
r_{m_2}=\frac{|m_2-m_{2,\rm TGL}|}{\sigma_{m_2}}
=\frac{m_2|m_2-m_{2,\rm TGL}|}{5\sigma_\mu}.
\]

O rascunho K01 passou a Δm² sem declarar emenda; isso fica corrigido ao lado, não por cima. [PRE_REGISTRO_CEGO_RASCUNHO_K01](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Ccadeia_de_selo%5Cv412%5Ckimi%5CPRE_REGISTRO_CEGO_RASCUNHO_K01.md&line=36&text=propaga%C3%A7%C3%A3o%20%CF%83_m%E2%82%82%20%E2%89%88%20%CF%83(%CE%94m%C2%B2%E2%82%82%E2%82%81)/(2m%E2%82%82) "citation")

### 1.1 Modelo preditivo explícito, sem dupla contagem

**(a) Posterior público de planejamento.** Adoto, apenas como modelo de planejamento e com prior plano declarado,

\[
\mu\sim N(7,388,0,078^2),\qquad
X\mid\mu\sim N(\mu,s^2).
\]

Logo \(X\sim N(7,388,0,078^2+s^2)\). O erro de 207,2 dias entra **uma única vez**, na incerteza sobre a verdade atual; não é somado novamente ao deslocamento central. Esse “posterior” é construção minha de planejamento, não um posterior publicado pela colaboração.

**(b) Verdade = previsão.** Adoto \(\mu=\Delta_{\rm pred}\) e \(X\sim N(\Delta_{\rm pred},s^2)\), novamente sem erro atual adicional.

Para Δm², as caudas são normais. Para a métrica frozen, defino \(Y=\sqrt{10X}\) e \(r=Y|Y-m_{2,\rm TGL}|/(5s)\); as raízes usadas na CDF são

\[
Y_+=\frac{m_{2,\rm TGL}+\sqrt{m_{2,\rm TGL}^2+20ts}}2,
\qquad
Y_-=\frac{m_{2,\rm TGL}-\sqrt{m_{2,\rm TGL}^2-20ts}}2 .
\]

O script calcula as três faixas por CDF, sem aproximação Monte Carlo. [resultados_planejamento](K04/M2/medidas/resultados_planejamento.json)

### 1.2 Tabela principal de desfechos prováveis

As probabilidades abaixo usam **a métrica frozen m₂**. A última coluna repete `P(r≥5)` em Δm² para rastrear os números 0,35/0,69 da revisão. Todas as linhas somam 100 %. `D_m₂` é o análogo frozen de D; o D90 citado pela ordem permanece em Δm².

#### (a) Posterior público de planejamento

| Precisão futura | σ | DΔ | D_m₂ | P(r<3) | P(3≤r<5) | P(r≥5), frozen | PΔ(r≥5) |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0,7 % | 0,051716 | 2,908008 | 2,922959 | 51,680481 % | 35,441905 % | 12,877614 % | 12,384071 % |
| 0,5 % | 0,036940 | 4,071211 | 4,092143 | 32,156124 % | 32,803157 % | 35,040719 % | 34,553737 % |
| 0,407121 % | 0,030078 | 5,000001 | 5,025709 | 23,486791 % | 26,147929 % | 50,365280 % | 50,016055 % |
| 0,324061 % | 0,023942 | 6,281550 | 6,313847 | 16,725358 % | 18,397100 % | 64,877542 % | 64,702532 % |
| 0,3 % | 0,022164 | 6,785352 | 6,820238 | 14,997791 % | 16,097589 % | 68,904620 % | 68,786155 % |
| Tabela 6, σ = 0,024 | 0,024000 | 6,266272 | 6,298490 | 16,783975 % | 18,473119 % | 64,742906 % | 64,566086 % |

#### (b) Verdade = previsão

| Precisão futura | σ | DΔ | D_m₂ | P(r<3) | P(3≤r<5) | P(r≥5), frozen | PΔ(r≥5) |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0,7 % | 0,051716 | 2,908008 | 2,922959 | 99,857867 % | 0,142097 % | 0,000036 % | 0,000057 % |
| 0,5 % | 0,036940 | 4,071211 | 4,092143 | 99,859911 % | 0,140055 % | 0,000034 % | 0,000057 % |
| 0,407121 % | 0,030078 | 5,000001 | 5,025709 | 99,860860 % | 0,139107 % | 0,000033 % | 0,000057 % |
| 0,324061 % | 0,023942 | 6,281550 | 6,313847 | 99,861708 % | 0,138261 % | 0,000032 % | 0,000057 % |
| 0,3 % | 0,022164 | 6,785352 | 6,820238 | 99,861953 % | 0,138015 % | 0,000032 % | 0,000057 % |
| Tabela 6, σ = 0,024 | 0,024000 | 6,266272 | 6,298490 | 99,861700 % | 0,138269 % | 0,000032 % | 0,000057 % |

### 1.3 Como essas probabilidades caem na regra com S ausente

| Faixa de P | Ramo alcançável com S `ABSENT` |
|---|---|
| `r_P < 3` | `NOT_FALSIFIED_UNDERPOWERED` se `D_P < 5`; `ARMED_CONSISTENT` se `D_P ≥ 5`. Na hipótese (a), os dois primeiros D estão abaixo de 5 e os demais acima; na (b), `D = 0`, sempre UNDER. |
| `3 ≤ r_P < 5` | `TGL_NU_M2_TENSION__P`. |
| `r_P ≥ 5` | `T_SINGLE(P)_AWAITING_S` se ratificado; caso contrário `OPEN_RULE_GAP`. Não é FALSIFIED. |
| `FALSIFIED` | **Depende de S independente com `r_S ≥ 5`; não alcançável com S ausente.** |
| `MATCHED_PROSPECTIVELY` | **Depende de S independente com `r_S ≤ 1`; não alcançável com S ausente e não é confirmação.** |

A tabela mostra o problema operacional: sob o posterior de hoje, o desfecho `r_P ≥ 5` é o mais provável já a 0,407121 %, mas sem S ele não recebe o nome de falsificação.

---

## 2. Correção de arredondamento e desempenho real contra projeto

A Tabela 6 do estudo de sensibilidade publica, para Δm²₂₁, **σ = 0,024** em seis anos e 0,017 em vinte, contra 0,074 em 100 dias. O mesmo texto informa 92, 2009 e 6696 dias com potência plena dos reatores, respectivamente, ao aplicar o ciclo 11/12. Portanto **2009 dias full‑reactor é a definição publicada de seis anos; não a inventei como dias vivos JUNO nem como dias de calendário.** [JUNO, arXiv:2204.13249](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2204.13249&text=will%20be%20determined%20to%20better%20than%200.5%25%20precision%20in%20six%20years "citation")

\[
D_\Delta(0,024)=6,266272<6,281552=D90.
\]

A margem é pequena e negativa; não há “superação” em Δm². Na métrica frozen, `D_m₂ = 6,298490`, ligeiramente acima: a diferença é mais um motivo para não trocar a regra sem emenda.

### 2.1 Comparação entre os dois pontos reais e o projeto

| Quantidade | Conta | Resultado |
|---|---|---:|
| σ de projeto escalado para 207,2 d | `0,074 × √(100/207,2)` | **0,051409** |
| σ real publicado em 207,2 d | fonte JUNO | **0,078** |
| razão real/projeto | `0,078/0,051409` | **1,517252** |
| redução real 59,1 → 207,2 d | `0,12/0,078` | **1,538462** |
| redução √T ingênua | `√(207,2/59,1)` | **1,872411** |

As análises mudaram volume fiducial, seleção, tratamento de fundos e âncoras de espectro. Esses fatores **não medem um piso de sistemática**; apenas impedem apresentar √T como desempenho garantido.

O orçamento de 207,2 dias informa: volume fiducial 0,96 %, prótons‑alvo 1,0 %, eficiência combinada 1,4 %, espectro de referência 1,2 %, potência térmica 0,5 %, fração de fissão 0,6 %, combustível gasto 0,3 %, não equilíbrio 0,3 % e diferença entre frações 0,1 %. O artigo diz que a estatística ainda domina, mas que **Bi–Po e eficiência de detecção já são significativos e redutíveis**. Não atribuo a esses números uma decomposição σ_stat/σ_sys de Δm²₂₁ que o artigo não fornece. [JUNO 207,2 d, Tabelas II–III](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fpdf%2F2609.37895&text=Detection%20efficiency "citation")

### 2.2 Projeções desde o desempenho real de 207,2 dias

**Sem piso**, apenas como cenário \(\sigma(T)=0,078\sqrt{207,2/T}\):

| Alvo | σ alvo | T total | Adicional cumulativo | Data ideal cumulativa* | Dias novos só no incremento | Data ideal do incremento* |
|---|---:|---:|---:|---|---:|---|
| 5σ | 0,030078 | 1393,41 d | 1186,21 d | 16/08/2029 | 1393,41 d | 11/03/2030 |
| D90 | 0,023942 | 2199,24 d | 1992,04 d | 31/10/2031 | 2199,24 d | 25/05/2032 |

\* Datas aritméticas a partir do fim da amostra em 18/05/2026, com 100 % de dias vivos e centro parado; **não são cronograma da colaboração nem datas de publicação.**

**Com piso ilustrativo ajustado aos dois pontos reais**, \(\sigma^2=a/T+s_0^2\) dá `a = 0,687601` e `s0 = 0,052588`. Como esse piso supera os dois σ alvo, **5σ e D90 são inalcançáveis nesse cenário**. Dois pontos ajustam exatamente dois parâmetros e as análises mudaram: isso é um estresse de planejamento, **não um piso medido**.

**Com decomposição aproximada do projeto**, usando `a = 100×0,074²` e `s0² = 0,024²−a/2009`, obtém‑se `s0 = 0,017419`:

| Alvo | T full‑reactor no modelo | Excesso sobre 2009 d | Data ideal com ciclo 11/12* |
|---|---:|---:|---|
| 5σ | 910,75 d | −1098,25 d | 15/05/2028 |
| D90 | 2029,84 d | +20,84 d | 18/09/2031 |

\* Também é apenas uma projeção de planejamento, não uma curva publicada nem promessa de liberação. A Tabela 6 sozinha deixa D90 ligeiramente fora de alcance em Δm²; a decomposição aproximada mostra a sensibilidade dessa fronteira a poucos dias.

---

## 3. Qual métrica vale até emenda

**Vale `NEUTRINO_M2_V2`, em m₂.** A `kill_rule` congelada exige `|m2_obs−m2_TGL|/σ_obs ≥ 5` em duas determinações independentes, com hash `e24877751ad810225412cc294c06b83eefeaedc67e4c5cabc7779ac01e4b19c3` e porte de 08/08/2026. [um_absoluto, frozen](kimi-cite://text?path=C%3A%5CIALD%5CArtigo%5CHaja_Luz%5CA%20Ponte%20e%20o%20Um%5CN%C3%B3s%5Cum_absoluto.json&text=FALSIFIED%20sse%20%7Cm2_obs%20-%20m2_TGL%7C%2Fsigma_obs%20%3E%3D%205 "citation")

| Forma | Resultado em 207,2 dias |
|---|---:|
| frozen, m₂, primeira ordem | **1,937997** |
| Δm² | **1,928084** |

Se se propuser Δm², a proposta deve ser chamada **EMENDA DE MÉTRICA**, com versão nova, hash, data anterior ao próximo centro, e ato explícito do operador. Não há emenda nesta entrega. O mesmo cuidado vale para D90: 0,024 fica abaixo em Δm² e acima em m₂, de modo que uma troca silenciosa também altera a fronteira de poder.

---

## 4. Datas, prospectividade e cegueira

- **08/08/2026:** V2 hasheada; o próprio frozen declara que a emissão inicial conhecia a tensão e que a cegueira vale prospectivamente.
- **29/09/2026:** liberação pública de 207,2 dias. É posterior ao hash e é, cronologicamente, a primeira nova medida JUNO elegível à aplicação prospectiva da regra.
- **30–31/10/2026:** esta casa leu e reproduziu as dez tensões, inclusive 1,938σ para 207,2 dias. [determinacoes_m2_30out](kimi-cite://text?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Cneutrino_E0_autonomia_30out%5Cdeterminacoes_m2_30out.json&text=%22z_sigma%22%3A%201.9379969609289271 "citation")

A função, aplicada documentalmente, devolve **`TGL_NU_M2_ARMED_CONSISTENT`**, não `TENSION`, não `FALSIFIED` e não `MATCHED`, pois `r_m₂ ≈ 1,94 < 3` e não há duas independências ≥5. Eu **não executei** essa função agora; estou relatando o estado já público e congelado.

A liberação é prospectiva no calendário da regra, mas **não é cega para a casa**: o centro já foi comunicado e lido. Além disso, a regra inicial foi escrita com tensão conhecida. Custódia anterior à liberação/abertura/comunicação é necessária para uma futura leitura verdadeiramente cega; guardar bytes não basta.

---

## 5. O incremento 59,1 → 207,2 dias e o desenho só com dados novos

### 5.1 A conta de variância inversa: o que ela é e o que não é

Com \(w_1=1/0,12^2\) e \(w_2=1/0,078^2\), a subtração ingênua de pesos dá

\[
\mu_\Delta=\frac{w_2(7,388)-w_1(7,50)}{w_2-w_1}
=7,306061,\qquad
\sigma_\Delta=(w_2-w_1)^{-1/2}=0,102640 .
\]

Os valores derivados são:

| Quantidade | Resultado |
|---|---:|
| centro ilustrativo do incremento | **7,306061** |
| σ ilustrativo | **0,102640** |
| r contra previsão, Δm² | **0,666902** |
| r contra previsão, frozen m₂ | **0,668472** |
| distância ao centro anterior 7,50 | **1,889502σ_incremento** |

Isso reproduz “≈7,31 e ≈0,10”, mas **não é uma determinação independente**. A conta pressupõe informação gaussiana independente e trata erros totais como se fossem pesos estatísticos destacáveis. A liberação nova é cumulativa, contém os 59 dias e muda seleção, volume fiducial, fundos e âncora TAO/Daya Bay.

Não localizei na liberação um coeficiente de correlação ou uma matriz de covariância **entre os estimadores de 59,1 e 207,2 dias**. Covariâncias internas de Daya Bay e entre parâmetros de outros ajustes não respondem a essa pergunta. O erro correto do incremento, portanto, é **[OPEN]**: 0,102640 é só uma ilustração de variância inversa.

### 5.2 Estimador e covariância necessários para um futuro incremento

O desenho aceitável deve usar uma amostra temporalmente disjunta, posterior a 18/05/2026, e um ajuste conjunto/condicional que entregue

\[
\Sigma=
\begin{pmatrix}
V_{\rm old} & C_{\rm old,new}\\
C_{\rm old,new} & V_{\rm new}
\end{pmatrix},
\]

incluindo nuisances compartilhados de escala/não linearidade de energia, fluxo, eficiência, fundos e resposta do detector. Uma diferença de estimadores cumulativos tem `V(d) = V_cum + V_old − 2C`; sem `C` e sem a resposta conjunta, a precisão incremental não é identificável a partir dos dois resumos públicos.

O estimador candidato é `μ̂_new` da likelihood dos eventos novos condicionada ao estado anterior, ou o ajuste conjunto completo com a covariância acima. Seleção, nuisances, versão e cortes precisam ser congelados antes da comunicação do novo centro; não se pode chamar a subtração de duas liberações de “independência”.

### 5.3 Exposição e limites do cenário √T

Com a taxa observada de 207,2 dias e **sem piso**, o incremento sozinho exige **1393 dias novos para 5σ** e **2199 para D90**, não a subtração desses valores por 207,2. As datas ideais são 11/03/2030 e 25/05/2032, respectivamente. Com o piso ilustrativo de 0,052588, ambos são inalcançáveis. O poder real permanece condicionado a covariância, estabilidade do centro e orçamento de sistemáticas; nenhum desses números autoriza pré‑registrar um resultado.

---

## 6. Segunda testemunha sem JUNO: as dez determinações e as previsões

A convenção de r é a frozen. Em entradas assimétricas usa‑se o erro do lado que aponta para a previsão; `σ5` é o erro que bastaria para 5σ **se o centro ficasse parado**, não uma precisão atual. Todas as linhas são `[KNOWN, a conferir]` para os números públicos e `[DERIVED—PLANEJAMENTO]` para r/σ5.

| Entrada | Centro e erro público | σ usado | r frozen | σ5 | Experimento, ano e ID primário consultado | Papel |
|---|---|---:|---:|---:|---|---|---|
| JUNO 207,2 d | 7,388 ± 0,078 | 0,078 | **1,937997** | 0,030233 | JUNO, 2026, [arXiv:2609.37895v1](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2609.37895 "citation") | P; não S |
| SNO+ | 7,91 (+0,22/−0,25) | 0,250 | **2,749285** | 0,137464 | SNO+, 2026, [PRL 137, 101807; DOI 10.1103/mv5z-pfb7](kimi-cite://web?url=https%3A%2F%2Fdoi.org%2F10.1103%2Fmv5z-pfb7 "citation"), arXiv:2511.11856v4 | Direta, sem JUNO |
| SK‑Gd reator | 9,08 (+0,55/−0,54) | 0,540 | **3,605064** | 0,389347 | SK, 2026, [arXiv:2610.03143v1](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2610.03143 "citation") | Direta, sem JUNO |
| KamLAND‑only | 7,54 (+0,19/−0,18) | 0,180 | **1,697137** | 0,061097 | KamLAND, 2013, [PRD 88, 033001; arXiv:1303.4667v2, Tabela 3](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F1303.4667v2 "citation"), DOI 10.1103/PhysRevD.88.033001 | Direta, sem JUNO |
| Solares sem KamLAND | 6,10 (+0,95/−0,81) | 0,950 | **1,146322** | 0,217801 | SK + solares, 2024, [PRD 109, 092001; arXiv:2312.12907v2](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2312.12907 "citation"), DOI 10.1103/PhysRevD.109.092001 | Uma família; não multiplicar subconjuntos |
| JUNO 59,1 d | 7,50 ± 0,12 | 0,120 | **2,206054** | 0,052945 | JUNO, 2025/2026, [arXiv:2511.14593v1](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2511.14593 "citation"), DOI 10.1038/s41586-026-10538-z | Subconjunto de P |
| NuFIT 6.1 | 7,537 (+0,100/−0,094) | 0,094 | **3,217279** | 0,060485 | NuFIT, 2025, [release notes 6.1](kimi-cite://web?url=http%3A%2F%2Fwww.nu-fit.org%2Fsites%2Fdefault%2Ffiles%2Fv61.release-notes.pdf "citation"); [análise associada arXiv:2601.09791](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2601.09791 "citation") | Global com JUNO 59 d; não independente |
| Capozzi et al. | 7,48 ± 0,10 | 0,100 | **2,443867** | 0,048877 | Capozzi et al., 2025/2026, [arXiv:2511.21650](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2511.21650 "citation"), DOI 10.1103/cxqw-1bty | Global com JUNO/SNO+; não independente |
| Bari 2026.a NO | 7,465 (+0,072/−0,080) | 0,080 | **2,864363** | 0,045830 | Bari, 2026, [Global‑nu release 2026.a, 15/10/2026](kimi-cite://web?url=https%3A%2F%2Fglobal-nu.org%2Fresults.html "citation") | Preliminar, com JUNO 207 d/SK‑Gd; não independente |
| SK‑Gd solar+reator | 8,94 (+0,46/−0,47) | 0,470 | **3,813218** | 0,358442 | SK, 2026, [arXiv:2610.03143v1](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2610.03143 "citation") | Combinação na mesma colaboração; não adicional |
| **SNO+ reator+solar, final** | **7,59 ± 0,17** | 0,170 | **2,097521** | 0,071316 | SNO+, 2026, [PRL 137, 101807, Tabela 3](kimi-cite://web?url=https%3A%2F%2Fdoi.org%2F10.1103%2Fmv5z-pfb7 "citation") | Sem JUNO, mas não somar SNO+ duas vezes |

**Errata de versões, ao lado:** os preprints v1/v2 do SNO+ traziam 7,93 (+0,21/−0,24) e o combinado 7,63 ± 0,17; a versão final PRL e o HTML v4 trazem 7,91 (+0,22/−0,25) e 7,59 ± 0,17. Usei a versão final. KamLAND‑only 7,54 é da Tabela 3, não o ajuste solar+KamLAND 7,53 do resumo. [SNO+ v2](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2511.11856v2 "citation")

### 6.1 Alguma chega a σ_S ≤ 0,0301 (0,407121 %)?

**Nenhuma das dez, nenhuma combinação citada e nenhum forecast primário consultado demonstra essa precisão.** O alvo exato em Δm² é 0,030078; o alvo frozen no centro JUNO é 0,030233. A resposta é não nos dois.

Mais importante: **esse corte não é condição necessária para 5σ.** Os valores de σ5 acima dependem do centro. Em particular:

- SK‑Gd: `σ5 = 0,389347`; com 411,52 dias atuais, o cenário condicional dá 791,60 dias totais e **380,08 dias adicionais** para 5σ.
- SNO+: `σ5 = 0,137464`; com 685 dias atuais, o cenário dá 2265,64 totais e **1580,64 adicionais**.
- KamLAND: `σ5 = 0,061097`; o fator de informação seria grande e não constitui plano operacional.
- Solares: `σ5 = 0,217801`, sem exposição única bem definida.

Esses números são equivalências \(\sigma\propto T^{-1/2}\) com centro e forma do erro parados. Não são datas prometidas, não provam independência de sistemáticas e não são uma nova estatística observada. [determinacoes_m2_30out](kimi-cite://text?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Cneutrino_E0_autonomia_30out%5Cdeterminacoes_m2_30out.json&text=%22exposicao_adicional_dias%22%3A%20380.07855357458413 "citation")

### 6.2 Previsões Hyper‑K, DUNE solar e outras

| Fonte | Previsão primária | Consequência para S |
|---|---|---|
| Hyper‑Kamiokande | Em cinco anos, amplitude da variação zênite ≈0,5 % e Δm²₂₁ com precisão **comparável à dos experimentos de reator então vigentes**, não 0,407 %. [Hyper‑K, arXiv:1309.0184](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F1309.0184 "citation") | Não fornece σ ≤ 0,0301 nem calendário que o demonstre. |
| DUNE solar | Para 100 kton·ano, incerteza projetada de **5,9 % em Δm²₂₁**, com necessidade de investimentos e sem um orçamento completo de sistemáticas; dois módulos iniciais equivaleriam a cerca de cinco anos. [Capozzi et al., arXiv:1808.08232v3](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F1808.08232v3 "citation") | Muito longe de 0,407 %. |
| DUNE com NC | A via dia–noite de Capozzi permanece a melhor para Δm²₂₁; NC melhora sobretudo θ₁₂ e o fluxo. O texto contextualiza início do programa em torno de 2030, não uma medida a 0,407 %. [Meighen‑Berger et al., arXiv:2410.00330](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2410.00330v1 "citation") | Não altera a conclusão. |
| JUNO solar | Previsão de **20 % em Δm²₂₁** em dez anos, modelo‑independente. [JUNO, arXiv:2210.08437](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2210.08437 "citation") | Não serve ao corte e, de todo modo, não é independente do P JUNO. |
| SNO+ continuado | A página institucional diz que três anos devem superar a precisão global então vigente, não 0,407 %. [SNO+ Results](kimi-cite://web?url=https%3A%2F%2Fsnoplus.phy.queensu.ca%2Fresults.html "citation") | Não há previsão de precisão suficiente para o corte. |

**Leitura probatória final:** não há segunda testemunha com σ ≤ 0,0301 demonstrada. Contudo, SK‑Gd impede transformar essa ausência em prova de que `FALSIFIED` seja impossível para sempre. A decisão correta é pré‑registrar a fonte e a covariância antes de qualquer novo centro, não criar um requisito de precisão que a regra frozen não contém.

---

## 7. Correções menores no validador K01, somente propostas

Não editei `CANAIS_K01.json`, `PRE_REGISTRO_CEGO_RASCUNHO_K01.md` nem `K01_validar.py`.

1. **UNDER nunca exercido / D padrão 6.** O padrão `d_p = d_s = 6,0` força ARMED. Uma revisão futura deve incluir `d_p = 4` para exercer `NOT_FALSIFIED_UNDERPOWERED` e `d_p = None` para `AWAIT_SOURCE`, além de usar o D documental do canal em vez do padrão. Isso é cobertura de código, não teste físico. [K01_validar](kimi-cite://text?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Ccadeia_de_selo%5Cv412%5Ckimi%5CK01_validar.py&text=def%20veredito_sintetico "citation")
2. **Sub‑rótulos colapsados.** `SINGLE_P/S` e `BOTH_NONINDEPENDENT` colapsam situações diferentes. Proposta: devolver o token principal **com campos estruturados** `reason`, `P_band`, `S_band`, `S_state`, `D_P`, `D_S`, `awaiting`, em vez de criar ambiguidade nova no token.
3. **S INVALID não pode esconder P ≥ 5.** O ramo principal continua `INCONCLUSIVE_SYSTEMATICS__INTEGRITY_S`, mas a saída deve mostrar ao lado, como estresse obrigatório: `stress_P = {r_P, band: "≥5", D_P}`. Falha de integridade não apaga evidência desfavorável nem a transforma em FALSIFIED. [REVISAO_K01, B3](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Ccadeia_de_selo%5Cv412%5Crevisao%5CREVISAO_K01.md&line=47&text=S%20INVALID%20esconde%20um%20P%20%E2%89%A5%205%CF%83 "citation")

Nenhum desses casos foi executado nesta seção.

---

## 8. Reprodutibilidade e bloqueios restantes

Scripts em `K04/M2/scripts/` e saídas em `K04/M2/medidas/`:

- `medidas_planejamento.py`: todas as contas de desfechos, projeções, incremento e testemunhas; apenas biblioteca padrão.
- `extrair_contexto_juno.py`: leitura bibliográfica de artigos em memória, sem salvar PDF e sem dados de eventos.
- `resultados_planejamento.json`: valores completos em precisão de máquina.
- `tabelas_planejamento.md`: tabelas principais geradas pelo script.
- `execucao_planejamento.txt`: saída da última execução das contas, não de teste empírico.

**Bloqueios:** covariância inter-liberações ausente; decomposição numérica σ_stat/σ_sys de Δm²₂₁ em 207,2 dias não publicada; calendário de próxima liberação desconhecido; segunda fonte e sua análise não congeladas; decisão de métrica/limiar/fonte é do operador. Nenhum bloqueio foi resolvido por ajuste de escala ou regra.
