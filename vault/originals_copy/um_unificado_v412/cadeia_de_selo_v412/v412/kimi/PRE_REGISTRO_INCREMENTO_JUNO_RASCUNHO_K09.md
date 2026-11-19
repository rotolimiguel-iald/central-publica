# PRÉ-REGISTRO — INCREMENTO JUNO APÓS 18/05/2026 — RASCUNHO K09

**Estado:** rascunho para leitura da gerência e do operador; **não selado, sem hash novo e sem abertura autorizada**. Nenhum vetor de dados foi lido, nenhuma likelihood foi aberta e nenhum teste observado foi executado. As contas abaixo são somente planejamento com agregados públicos.

**Motivo:** a função de veredito foi hasheada em 08/08/2026, depois de o número JUNO de 207,2 dias ser público; por isso a regra não é cega em relação a esse número. Em relação à previsão publicada — valor no acervo em 22/01/2026 e publicação Zenodo em 17/02/2026 — o número veio depois. A tese do neutrino é de 2025, mas sem o valor; JUNO 59,1 dias é anterior ao valor público e conta como retrodição sem ajuste/use-novelty, não como leitura prospectiva do valor. O observável aqui é o dado tomado **depois de 18/05/2026**, ainda não mostrado: o único dado posterior à previsão publicada e ao pino da regra. Nada disto sugere que o autor tenha visto o dado antes.

## 1. Observável e formas admissíveis de obtê-lo

### 1.1 Observável

Estimador de `Δm²₂₁` baseado **exclusivamente em eventos posteriores a 18/05/2026**, com:

- janela temporal explícita e disjunta da amostra anterior;
- centro, erro total e, se houver assimetria, os dois lados;
- versão da seleção, volume fiducial, calibração, fundos, fluxo/ânconas TAO/Daya Bay e modelo de resposta;
- tratamento dos nuisances compartilhados com a análise de 207,2 dias;
- matriz de covariância ou ajuste conjunto/condicional suficiente para ligar o estimador novo aos cumulativos já públicos.

A métrica do veredito será calculada depois, em m₂. Nenhum centro cumulativo posterior pode ser renomeado “incremento” sem demonstrar a extração.

### 1.2 Forma A — publicado pela colaboração como incremento

Conta quando a própria JUNO publicar o estimador do período disjunto, com incerteza total e a covariância/ligação com os estimadores anteriores. Pode ser um ajuste condicional ao estado anterior ou um ajuste conjunto completo; a publicação deve permitir reproduzir o erro do incremento, não apenas do cumulativo.

### 1.3 Forma B — diferença entre liberações cumulativas

Sejam `X0` o estimador de 207,2 dias, `Xc` o cumulativo posterior, `V0`, `Vc` e `C=Cov(X0,Xc)`. Defina

\[
\lambda=\frac{C}{V_0},\qquad
Y=\frac{X_c-\lambda X_0}{1-\lambda},
\]

com

\[
\operatorname{Var}(Y)=
\frac{V_c+\lambda^2V_0-2\lambda C}{(1-\lambda)^2}.
\]

A escolha de `λ` torna `Y` não correlacionado com `X0` no modelo linear. No aninhamento de variância inversa com informação nova independente, `C=Vc`; isso recupera, para 59,1 → 207,2 dias, o centro ilustrativo 7,306061 e o erro ilustrativo 0,102640. **Esse caso não é uma covariância atribuída ao JUNO.**

**O que se exige:** covariância entre liberações, resposta conjunta dos nuisances, compatibilidade da seleção e demonstração de que o estimador resultante representa apenas a informação posterior ao corte.

**O que se perde sem covariância:** `λ`, o centro incremental e sua variância deixam de ser identificáveis; perde-se a validade de `r`, da alegação de independência, da comparação de tensões e da abertura cega. Fixar `C=0` ou `C=Vc` sem fonte é apenas um brinquedo e não habilita veredito.

## 2. Métrica congelada e fonte elegível

### 2.1 Métrica obrigatória

Com `μ` e `σ_μ` em `10⁻⁵ eV²`,

\[
m_2=\sqrt{10\mu}\ {\rm meV},\qquad
\sigma_{m_2}=\frac{m_2\sigma_\mu}{2\mu},\qquad
r_{m_2}=\frac{m_2|m_2-m_{2,\rm TGL}|}{5\sigma_\mu}.
\]

`m₂,TGL = 8,507414099900329 meV` e `Δpred = 7,237609466718292 × 10⁻⁵ eV²`, no pacote `E0=1 eV`, `m₁≈0`. A razão `r_Δ = |μ−Δpred|/σ_μ` pode ser mostrada ao lado **somente como comparação**. Trocar a métrica do veredito é emenda com nova versão e hash anterior ao centro novo.

### 2.2 Publicação que conta

- artigo ou preprint da colaboração JUNO com identificador, versão e data;
- transparências oficiais da colaboração **podem contar como resultado preliminar de conferência**, desde que identifiquem evento, contribuição, anexo e data e contenham janela, centro, erro total, seleção e a covariância/ligação exigidas para o incremento;
- se faltar qualquer elemento necessário ao cálculo, a transparência entra apenas como estresse preliminar e **não abre veredito**;
- notícia secundária, resumo jornalístico ou menção sem o agregado completo não conta;
- a classe “preliminar” e sua aceitação são ratificadas **pelo operador**, com proposta técnica preparada pela gerência, **antes** do selo; não se muda a fonte depois de ver o centro.

A elegibilidade temporal é independente da forma: mesmo um artigo completo não conta se reutilizar apenas dados até 18/05/2026.

## 3. Hipóteses de planejamento

Seja `s` o erro do incremento sozinho.

**(H1) Posterior público de hoje, prior plano declarado:**

\[
\mu\sim N(7,388,0,078^2),\qquad X\mid\mu\sim N(\mu,s^2)
\quad\Rightarrow\quad X\sim N(7,388,0,078^2+s^2).
\]

**(H2) Verdade = previsão:** `X ~ N(Δpred,s²)`.

Para cenários sem piso, usa-se `s(T)=0,078√(207,2/T)`. Isso é uma extrapolação de brinquedo, não uma previsão da colaboração. Com o piso ajustado `s0=0,052587652`, 5σ e D90 são inalcançáveis; as tabelas abaixo não se aplicam a esse caso.

### 3.1 H1 — posterior público

| Dado novo | s | DΔ | D_m₂ | P(r≤1) | P(1<r<3) | P(r<3) | P(3≤r<5) | P(r≥5), m₂ | PΔ(r≥5) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 ano = 365,25 d | 0,058748 | 2,559918 | 2,573080 | 15,762854 % | 44,224261 % | 59,987115 % | 32,500487 % | 7,512398 % | 7,105281 % |
| 2 anos = 730,50 d | 0,041541 | 3,620271 | 3,638885 | 9,399527 % | 28,812218 % | 38,211745 % | 35,422244 % | 26,366011 % | 25,833369 % |
| 3 anos = 1095,75 d | 0,033918 | 4,433909 | 4,456706 | 7,026722 % | 21,055952 % | 28,082674 % | 30,394820 % | 41,522506 % | 41,078430 % |

### 3.2 H2 — verdade = previsão

| Dado novo | s | DΔ | D_m₂ | P(r≤1) | P(1<r<3) | P(r<3) | P(3≤r<5) | P(r≥5), m₂ | PΔ(r≥5) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 ano = 365,25 d | 0,058748 | 2,559918 | 2,573080 | 68,269647 % | 31,460324 % | 99,729971 % | 0,269970 % | 0,000059 % | 0,000057 % |
| 2 anos = 730,50 d | 0,041541 | 3,620271 | 3,638885 | 68,269298 % | 31,460698 % | 99,729996 % | 0,269946 % | 0,000058 % | 0,000057 % |
| 3 anos = 1095,75 d | 0,033918 | 4,433909 | 4,456706 | 68,269182 % | 31,460822 % | 99,730004 % | 0,269938 % | 0,000058 % | 0,000057 % |

As duas caudas foram implementadas com o módulo: na cauda inferior, `r≥t` é intervalo entre raízes, não `m≤L_t`. Em H2, os benchmarks são 68,27 %, 31,46 % e 99,73 % na precisão pedida. Arquivo-fonte das células: `K04/M2/K09/medidas/incremento_1a3_anos_k09.md`.

## 4. Duas regras lado a lado — SEM escolher

A regra A corresponde ao comportamento hoje descrito pelo código: duas testemunhas independentes. A regra B seria **emenda**: uma testemunha com limiar explícito. As datas são brinquedos sem piso, com centro parado e 100 % de dias vivos; não são cronogramas. O veredito é em m₂; as datas em Δm² ficam ao lado.

| Questão | A — duas testemunhas independentes | B — uma testemunha com limiar explícito |
|---|---|---|
| Negativo | `FALSIFIED` se o incremento P tiver `r_P≥5` **e** uma segunda determinação autônoma S tiver `r_S≥5`, com robustez de experimento. | `FALSIFIED` se o incremento P tiver `r_P≥5`, sem exigir S. Variante de poder explícito: exigir também `D_P≥6,281552`; se adotada, deve constar no selo. |
| `r_P≥5` sem S | Código atual: `TENSION`, com `tensao_global_5sigma_sem_2a_determinacao`; **não** `FALSIFIED`. | `FALSIFIED`, somente após emenda válida. |
| TENSION | Se a última linha da escada for `r≥3`, inclusive `≥5` sem segunda. A última linha deve ser fixada antes da abertura. | Se a cláusula for preservada na emenda; a definição deve ser escrita, não presumida. |
| ARMED_CONSISTENT | Resto, incluindo perito JUNO `r<3` quando a última linha também for `<3`. | Resto, se mantido na emenda. |
| MATCHED | Texto: duas determinações independentes `r≤1`; código atual não tem ramo. | Não se cria ramo implicitamente; exige decisão e implementação separadas. |
| Data de brinquedo para `r_P=3` | Δm²: **01/10/2027**; m₂: **26/09/2027**. A escada global pode antecipar ou impedir essa leitura. | Mesmas datas numéricas se a cláusula for preservada. |
| Data de brinquedo para 5σ | Δm²: P em **11/03/2030**; m₂: P em **25/02/2030**. SK-Gd em 17/10/2027 **somente se sua anomalia persistir**; o par A fica limitado pelo mais tardio em cada métrica. | Δm²: **11/03/2030**; m₂: **25/02/2030**. |
| Data de brinquedo se B também exigir D90 | Não se aplica à regra A. | Δm²: **25/05/2032**; m₂: **02/05/2032**. |
| Com piso `s0=0,052587652` | 5σ e D90 inalcançáveis; nenhuma data acima vale. | Igual. |
| Custo/limite | Sem S elegível e com poder, não devolve o negativo; a independência física e a covariância P–S são obrigatórias. | Perde a réplica independente e aumenta o peso de sistemáticas/covariância do único P; o limiar não pode ser ajustado ao centro visto. |

**Leitura obrigatória:** a tabela não escolhe A ou B. A constatação de que o código selado descreve hoje o comportamento A não é decisão prospectiva. Manter A ou adotar B exige ato futuro do operador, com texto, limiar, fonte, escada e implementação selados antes da única abertura.

## 5. Significado dos desfechos

### 5.1 Negativo válido

Esta é a leitura técnica que a gerência deve apresentar ao operador antes de qualquer selo; ela não antecipa nem decide a regra de morte. Se a regra selada for satisfeita, um negativo atinge o **pacote da escala**: o Um posto em `E0=1 eV`, com `m₁≈0`, e a identificação usada para obter `m₂,TGL`. Não atinge `β` isoladamente, não falsifica automaticamente toda a TGL e não altera o gate geral. O alcance não pode ser inflado além dessa cadeia de premissas.

### 5.2 Positivo, tensão ou acordo

- `r<5` não é confirmação;
- `ARMED_CONSISTENT`, `TENSION`, `NOT_FALSIFIED` e mesmo um futuro `MATCHED_PROSPECTIVELY` **não são `CONFIRMED`**;
- concordância estatística não prova identificação, independência, ausência de sistemáticas ou verdade da teoria;
- um P alto sem S continua `TENSION` no código atual, não negativo e não confirmação;
- o gate não se move em nenhum desses desfechos.

## 6. Custódia e abertura única

1. **Quem guarda:** a gerência c1 guarda este rascunho, os identificadores das fontes, os scripts de planejamento e o manifesto de hashes. O construtor não guarda sozinho a chave de abertura.
2. **Quem decide e sela:** o operador decide se quer selar e, com a gerência, fixa A ou B, limiar, métrica, fonte, escada e classe de publicação. O hash deve preceder qualquer acesso ao centro/erro do incremento.
3. **Quem abre:** um revisor independente nomeado pela gerência, que não construiu este rascunho, abre o agregado elegível **uma única vez**, após conferir o hash e a completude da fonte. O construtor não abre.
4. **Uma abertura só:** centro, erro, covariância e versão entram na mesma leitura. Não há espiada preliminar, segunda abertura para “melhorar” o resultado ou troca posterior de regra/fonte/métrica.
5. **Se a fonte estiver incompleta:** não há abertura nem veredito; espera-se a fonte completa sem conhecer o centro. Se já houve abertura válida, qualquer nova liberação exige novo pré-registro e nova custódia, não reabertura deste.
6. **Registro do ato:** data, fonte, versão, hash do pré-registro, identidade do revisor e vereditos A/B — se ambos tiverem sido mantidos para comparação — são preservados pela gerência. Nada disso foi executado nesta rodada.

## 7. Bloqueios antes do selo

- covariância inter-liberações e P–S não publicada;
- independência física e robustez de S não demonstrada; o cenário SK-Gd exige persistência da anomalia a 3,101149σ do JUNO;
- decomposição estatística/sistemática do erro futuro e piso real desconhecidos;
- classe de fonte preliminar a ratificar;
- escada global e ramo MATCHED a decidir/implementar;
- uma/duas testemunhas e limiar de B a escolher sem olhar o dado;
- data e existência da próxima liberação desconhecidas.

**Nenhum teste observado foi executado. `NOT_FALSIFIED` não é `CONFIRMED`; o gate não se move.**
