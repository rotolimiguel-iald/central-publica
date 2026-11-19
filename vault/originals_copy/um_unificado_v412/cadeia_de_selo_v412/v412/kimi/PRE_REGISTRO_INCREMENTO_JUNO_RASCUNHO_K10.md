# PRÉ-REGISTRO — INCREMENTO JUNO — RASCUNHO K10 (rodada 4 da v412)

**Linhagem.** Este arquivo reconstrói, AO LADO, o `PRE_REGISTRO_INCREMENTO_JUNO_RASCUNHO_K09.md` (que fica intacto), aplicando os 12 achados da conferência distinta (`..\revisao\REVISAO_K09_PRE_REGISTRO_DO_INCREMENTO.md`, sha16 `3b1d8a2fabc7467b`; 4 ALTO, 6 MEDIO, 2 BAIXO). A tabela achado → conserto está em `ERRATA_K10_PRE_REGISTRO.md`. Nenhum vetor de dados foi lido, nenhuma likelihood foi aberta, nenhum teste observado foi executado, nenhum modelo de linguagem foi rodado. As contas citadas são de planejamento com agregados públicos; as da conferência reproduzem (o revisor refez com script próprio), e as que são só do revisor vêm marcadas [DERIVED pelo revisor; a gerência não reconferiu].

---

## 0. Primeira página

### 0.1 A partitura em língua de leigo

**O que o teste decide.** Se um número novo do JUNO — publicado pela primeira vez depois de este pré-registro estar selado e carimbado fora desta casa, e calculado só com dados tomados depois do fim da janela de 207,2 dias — fica a 5 desvios-padrão ou mais da massa que a TGL publicou em 17/02/2026: m₂ = β × sen 45° × 1 eV = 8,5074 meV (no ordenamento normal, com m₁ ≈ 0).

**O que o teste não decide.** Não mede β sozinho, não separa os fatores do produto β·sen 45°·u, não confirma a TGL, e — ponto central desta rodada — um resultado SEM negativo não é evidência a favor, porque o teste quase não tem força para dar negativo (a conta está em 0.2). Nenhum desfecho positivo vira CONFIRMED: está no objeto congelado (`forbidden_verdicts`, um.py l.4627).

**O que um negativo significaria — as DUAS camadas.** (a) Um negativo válido falsifica a conjunção β·sen 45°·u com m₁ ≈ 0; este teste não separa os fatores. As **bandeiras do gate da gravidade quântica não se movem** — no rito m₂ o campo `does_not_gate_core` é `True` (um.py l.4702). ("Gate", primeira ocorrência: nesta nota, "gate" é o conjunto de checagens do `um.py` que autorizam o veredito nuclear do programa, o 1 = 1.) (b) Mas o `um.py` selado tem a **regra do contorno** (v314, l.299841–299869): o rito `neutrino_m2_vivo` está no rol de oito ritos (l.299856), e um veredito que contém FALSIFIED sem NOT_FALSIFIED ("FALSIFIED limpo", l.299846–299848) põe `identity_true` em `False` e escreve o 1 = 1 como `1=1=FALSO_NO_CONTORNO[neutrino_m2_vivo]` (l.299864–299866). O comentário do código atribui a regra a uma decisão do operador de 05/09/2026 [DECLARADO no código; esta frente não abriu os bytes dessa fala]. **Se essa regra do contorno vale também para o veredito do incremento é decisão do operador** (manter o rol como está, ou emendá-lo antes do selo). E vale a cláusula de resgate: ajustar u ou o ângulo DEPOIS do negativo não reverte o veredito.

Esta partitura é leitura da gerência, montada da conferência; o operador ainda não a leu.

### 0.2 A conta de poder realista

- **Com o piso** [DERIVED pelo revisor da conferência; hipótese dita: piso por bloco, s² = s0² + a/T, com s0 = 0,052588 vindo do ajuste de dois pontos 59,1 → 207,2 — piso com zero grau de liberdade, e a análise mudou entre os pontos; o próprio K04 diz que não é piso medido]: a chance de 5σ é **3,58 % em 1 ano, 6,36 % em 2 anos, 7,81 % em 3 anos com uma testemunha** (D = 2,21 / 2,47 / 2,58) — leia-se **~4–8 % em 1–3 anos** —, e **perto de zero com duas testemunhas** (a segunda, S, teria de chegar a 5σ também, o que pediria σ_S ≲ 0,03 × 10⁻⁵ eV², que nenhuma entrada de hoje demonstra). Com o piso, a distância de planejamento tem teto δ/s0 ≈ **2,86**: não só 5σ e D90 ficam inalcançáveis, **também a marca planejada r = 3 fica fora de alcance**; o que sobra é só a flutuação estatística, que é o que os 3,58–7,81 % medem.
- **Sem piso** (o brinquedo da seção 3): só 3 anos chegam a **~42 %** de chance de 5σ sob o posterior público de hoje.
- **Portanto, o que este pré-registro promete é uma PAREDE MEDIDA, não um teste decisivo.** Na faixa realista, um resultado sem negativo carrega quase nenhuma informação: é parede medida, não evidência a favor. Com a regra de duas testemunhas e sem S, o máximo que o canal devolve é TENSION — que não é FALSIFIED.

### 0.3 Estado

**Rascunho com bloqueios.** Não selado, sem hash novo, sem abertura autorizada, sem gatilho, sem prazo-limite e sem plano B fixados. Nunca escrever "pronto" sobre este texto. Os bloqueios estão na seção 7; as escolhas que são do operador, na seção 9.

---

## 1. Observável, cegueira e os marcos

### 1.1 Os três marcos e a chave da cegueira

**Motivo (os dois eixos na mesma frase).** A função de veredito foi congelada em 08/08/2026, **depois** de o número JUNO de 207,2 dias ser público, e a previsão foi publicada em 17/02/2026 (valor no acervo em 22/01/2026), **antes** desse número: em relação ao hash da regra, o número de 207,2 dias não é cego; em relação à previsão publicada, ele é posterior. A tese do neutrino é de 2025, sem o valor; o JUNO de 59,1 dias (18/11/2025) é anterior ao valor público e conta como retrodição sem ajuste (novidade de uso), não como leitura prospectiva do valor. Esta nota fala só de datas e das entradas da fórmula (β, sen 45°, 1 eV; nenhuma usa dado de neutrino); não diz o que o autor leu ou deixou de ler.

**Os três marcos.** (i) a previsão publicada, 17/02/2026; (ii) o pino da regra antiga, o hash da função de veredito, 08/08/2026; (iii) **o selo DESTE pré-registro**, que ainda não existe e só nasce com carimbo externo. Os dois primeiros marcos independem do selo; o selo acrescenta o terceiro.

**A chave da cegueira, corrigida.** O que blinda o teste não é a data em que o dado foi tomado: é a **PRIMEIRA APARIÇÃO PÚBLICA do número**, que tem de ser posterior à previsão publicada (17/02/2026) **E** ao selo deste pré-registro, com **carimbo externo** (push ou depósito público, como no precedente H0DN, rota do Mapa `infra.github.publicacao_fora_da_cadeia_h0dn_12nov`). Dado tomado entre 18/05/2026 e 08/08/2026 foi tomado antes do pino antigo e nem por isso deixaria de ser desconhecido; número já público não cega nada, seja qual for a data de tomada.

**O que é falso na redação anterior, corrigido.** Não é verdade que exista "um único dado posterior aos dois marcos": o artigo JUNO de 207,2 dias (29/09/2026, arXiv:2609.37895v1) e o SK-Gd reator (02/10/2026, arXiv:2610.03143v1) já são posteriores aos dois marcos e já são públicos. O correto: **só um NÚMERO do JUNO tornado público pela primeira vez depois do selo é posterior à previsão publicada e ao selo.** Pela mesma razão, o cenário SK-Gd já foi visto: uma segunda testemunha **S só é cega se for liberação nova pós-selo**, e isso passa a estar escrito.

**Registro datado da busca.** No dia do selo, anexa-se a este pré-registro o registro datado da busca: as consultas feitas, a data e o resultado (o que estava público naquele dia sobre o incremento). Sem esse anexo, "ainda não mostrado" seria afirmação de ausência sem busca datada.

**Datas com o seu estatuto.** O fim da janela, 18/05/2026, é **[DECLARADO, sem resposta crua guardada]**: o resumo do arXiv só diz "207.2 live days" e a data veio da ordem da gerência. O início da janela, 26/08/2025 — usado no duty cycle de 78,19 % — também é **[DECLARADO, sem resposta crua guardada]**.

### 1.2 O observável

Estimador de `Δm²₂₁` baseado **exclusivamente em eventos posteriores ao fim da janela de 207,2 dias** (18/05/2026 [DECLARADO, sem resposta crua guardada]), cujo número tenha **primeira aparição pública posterior ao selo deste pré-registro**, lido do **TEXTO** do artigo (não de figura, não de notícia), com:

- janela temporal explícita e disjunta da amostra anterior;
- centro, erro total e, se houver assimetria, os dois lados (convenção na seção 2.3);
- versão da seleção, volume fiducial, calibração, fundos, fluxo/ânconas TAO/Daya Bay e modelo de resposta;
- tratamento dos nuisances compartilhados com a análise de 207,2 dias;
- matriz de covariância ou ajuste conjunto/condicional suficiente para ligar o estimador novo aos cumulativos já públicos.

A métrica do veredito é m₂ (seção 2.1). Nenhum centro cumulativo posterior pode ser renomeado "incremento" sem demonstrar a extração.

### 1.3 Forma A — publicado pela colaboração como incremento

Conta quando a própria JUNO publicar o estimador do período disjunto, com incerteza total e a covariância/ligação com os estimadores anteriores. Pode ser um ajuste condicional ao estado anterior ou um ajuste conjunto completo; a publicação deve permitir reproduzir o erro do incremento, não apenas do cumulativo.

**Base de precedência, sem força de mais.** O único precedente real (59,1 → 207,2 dias) foi **cumulativo**, com volume, seleção, fundos e âncora mudados e sem covariância publicada — ou seja, não foi Forma A. Pelo precedente, **o caso mais provável é SEM veredito** (a fonte da Forma A pode nunca vir); é por isso que o plano B e o prazo-limite da seção 6 precisam estar escritos antes do selo.

### 1.4 Forma B — diferença entre liberações cumulativas

Sejam `X0` o estimador de 207,2 dias, `Xc` o cumulativo posterior, `V0`, `Vc` e `C = Cov(X0, Xc)`. Defina

\[
\lambda=\frac{C}{V_0},\qquad
Y=\frac{X_c-\lambda X_0}{1-\lambda},
\qquad
\operatorname{Var}(Y)=\frac{V_c+\lambda^2V_0-2\lambda C}{(1-\lambda)^2}.
\]

A escolha de `λ` torna `Y` não correlacionado com `X0` no modelo linear. No aninhamento de variância inversa com informação nova independente, `C = Vc`; isso recupera, para 59,1 → 207,2 dias, o centro ilustrativo 7,306061 e o erro ilustrativo 0,102640. **Esse caso não é uma covariância atribuída ao JUNO.**

**Identificabilidade (achado da conferência, com conta do revisor).** Sem a covariância publicada, `λ`, o centro incremental e sua variância **não são identificáveis**, e a escolha de `C` troca o veredito. Exemplo hipotético do revisor (X0 = 7,388 ± 0,078; Xc = 7,35 ± 0,06): o r_Δ do estimador por diferença vale 1,87 com C = 0; 0,61 com C = Vc; 0,32 no limite de C positivo; e chega a 8,28 com C negativo admissível por positividade. Além disso, C = Vc só vale no limite de Hausman (estimador eficiente e sem sistemática compartilhada), e o piso de dois pontos sugere sistemática grande. Fixar `C = 0` ou `C = Vc` sem fonte é apenas um brinquedo e não habilita veredito.

**O que se exige:** covariância entre liberações, resposta conjunta dos nuisances, compatibilidade da seleção e demonstração de que o estimador resultante representa apenas a informação posterior ao corte.

## 2. Métrica congelada, D_P, erros assimétricos e fonte elegível

### 2.1 Métrica do veredito

Com `μ` e `σ_μ` em `10⁻⁵ eV²`,

\[
m_2=\sqrt{10\mu}\ {\rm meV},\qquad
\sigma_{m_2}=\frac{m_2\sigma_\mu}{2\mu},\qquad
r_{m_2}=\frac{m_2\,|m_2-m_{2,\rm TGL}|}{5\sigma_\mu}.
\]

`m₂,TGL = 8,507414099900329 meV` e `Δpred = 7,237609466718292 × 10⁻⁵ eV²`, no pacote `E0 = 1 eV`, `m₁ ≈ 0` (a escala 1 eV é "DECLARADA, NAO DERIVADA" no objeto congelado, um.py l.4621, que também registra que 1,0200 eV zeraria a tensão). A razão `r_Δ = |μ − Δpred| / σ_μ` pode ser mostrada ao lado **somente como comparação**. Trocar a métrica do veredito é emenda com nova versão e hash anterior ao centro novo.

### 2.2 D_P — definição e métrica

**D_P é a distância de planejamento**, computada no centro de planejamento fixado no selo (hoje o posterior público 7,388 × 10⁻⁵ eV²), **na métrica do veredito (m₂)**:

\[
D_P=\frac{|\,m_{2,\rm plano}-m_{2,\rm TGL}\,|}{\sigma_{m_2}\ {\rm do\ incremento}}.
\]

D_P **não** é o r observado: a exigência de poder é sobre o desenho, não sobre o resultado. Na variante de poder da regra B, exige-se `D_P ≥ 6,281552` (= 5 + z90, z90 = 1,2815516) — se adotada, consta no selo; lida como r observado, viraria `r_P ≥ 6,28`, o que não é a mesma regra. Com o piso (seção 3.3), D_P tem teto δ/s0 ≈ 2,86 no centro de planejamento de hoje: a variante D90 é inalcançável nesse cenário.

### 2.3 Convenção de erros assimétricos

Quando a fonte publicar erro assimétrico (σ⁺ ≠ σ⁻), o veredito usa **o erro do lado que aponta para a previsão** m₂,TGL (convenção trazida da M2 §7 e aqui declarada no próprio pré-registro). Os dois lados são sempre registrados. Esta convenção entra no objeto hasheado do novo pré-registro.

### 2.4 Publicação que conta

- artigo ou preprint da colaboração JUNO com identificador, versão e data;
- transparências oficiais da colaboração **podem contar como resultado preliminar de conferência**, desde que identifiquem evento, contribuição, anexo e data e contenham janela, centro, erro total, seleção e a covariância/ligação exigidas para o incremento;
- se faltar qualquer elemento necessário ao cálculo, a transparência entra apenas como **estresse preliminar** e **não abre veredito nem consome a abertura** (seção 6);
- notícia secundária, resumo jornalístico ou menção sem o agregado completo não conta;
- a classe "preliminar" e sua aceitação são ratificadas **pelo operador**, com proposta técnica preparada pela gerência, **antes** do selo; não se muda a fonte depois de ver o centro.

A elegibilidade temporal e a cegueira são independentes da forma: mesmo um artigo completo não conta se reutilizar apenas dados até o fim da janela de 207,2 dias, ou se o seu número já era público antes do selo.

## 3. Hipóteses de planejamento e as tabelas

Seja `s` o erro do incremento sozinho.

**(H1) Posterior público de hoje, prior plano declarado:**

\[
\mu\sim N(7,388,\,0,078^2),\qquad X\mid\mu\sim N(\mu,s^2)
\quad\Rightarrow\quad X\sim N(7,388,\,0,078^2+s^2).
\]

**(H2) Verdade = previsão:** `X ~ N(Δpred, s²)`.

### 3.1 e 3.2 — BRINQUEDO SEM PISO (rótulo obrigatório)

Para cenários sem piso, usa-se `s(T) = 0,078√(207,2/T)`. **Isto é uma extrapolação de brinquedo, não uma previsão da colaboração.** As duas tabelas abaixo são as do rascunho K09, mantidas porque reproduzem (a conferência as refez e batem), e valem **só** como brinquedo sem piso. Arquivo-fonte das células: `K04/M2/K09/medidas/incremento_1a3_anos_k09.md`.

**H1 — posterior público (brinquedo sem piso):**

| Dado novo | s | DΔ | D_m₂ | P(r≤1) | P(1<r<3) | P(r<3) | P(3≤r<5) | P(r≥5), m₂ | PΔ(r≥5) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 ano = 365,25 d | 0,058748 | 2,559918 | 2,573080 | 15,762854 % | 44,224261 % | 59,987115 % | 32,500487 % | 7,512398 % | 7,105281 % |
| 2 anos = 730,50 d | 0,041541 | 3,620271 | 3,638885 | 9,399527 % | 28,812218 % | 38,211745 % | 35,422244 % | 26,366011 % | 25,833369 % |
| 3 anos = 1095,75 d | 0,033918 | 4,433909 | 4,456706 | 7,026722 % | 21,055952 % | 28,082674 % | 30,394820 % | 41,522506 % | 41,078430 % |

**H2 — verdade = previsão (brinquedo sem piso; REFERÊNCIA, sem informação de desenho):** a tabela mostra os mesmos benchmarks 68,27 % / 31,46 % / 99,73 % em qualquer exposição, como tem de ser quando a verdade é a previsão; não carrega informação de desenho.

| Dado novo | s | DΔ | D_m₂ | P(r≤1) | P(1<r<3) | P(r<3) | P(3≤r<5) | P(r≥5), m₂ | PΔ(r≥5) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 ano = 365,25 d | 0,058748 | 2,559918 | 2,573080 | 68,269647 % | 31,460324 % | 99,729971 % | 0,269970 % | 0,000059 % | 0,000057 % |
| 2 anos = 730,50 d | 0,041541 | 3,620271 | 3,638885 | 68,269298 % | 31,460698 % | 99,729996 % | 0,269946 % | 0,000058 % | 0,000057 % |
| 3 anos = 1095,75 d | 0,033918 | 4,433909 | 4,456706 | 68,269182 % | 31,460822 % | 99,730004 % | 0,269938 % | 0,000058 % | 0,000057 % |

As duas caudas foram implementadas com o módulo: na cauda inferior, `r ≥ t` é intervalo entre raízes, não `m ≤ L_t`.

### 3.3 A faixa COM PISO — a que se aplica

[DERIVED pelo revisor da conferência; a gerência não reconferiu. **Hipótese dita:** o piso s0 = 0,052587652 do ajuste de dois pontos vale em cada bloco, s² = s0² + a/T. O piso tem zero grau de liberdade e a análise mudou entre os pontos; o próprio K04 diz que não é piso medido.]

| Horizonte | P(r ≥ 5 \| H1), com piso | D, com piso |
|---|---:|---:|
| 1 ano | **3,58 %** | 2,21 |
| 2 anos | **6,36 %** | 2,47 |
| 3 anos | **7,81 %** | 2,58 |

Com o piso: a distância de planejamento tem teto δ/s0 ≈ 2,86 no centro 7,388; **5σ, D90 e a marca planejada r = 3 são todos inalcançáveis** como alcance de desenho (r continua variável aleatória: a flutuação pode cruzar 3 ou 5 — é exatamente o que a tabela acima mede), e **nenhuma das datas de brinquedo da seção 4 vale**. Em uma linha: **na faixa realista, um resultado sem negativo é parede medida, não evidência a favor.**

## 4. As duas regras, sem ordem de padrão

Nenhuma das duas regras está escolhida, e a ordem de apresentação não é padrão. É fato sobre o código — não escolha prospectiva — que o `um.py` de hoje descreve a lógica da regra A. Manter A ou adotar B exige ato futuro do operador, com texto, limiar, fonte, escada e implementação selados antes da única abertura. **Eliminado o "A/B para comparação" depois do dado:** ou se sela uma regra só, ou se selam as duas **com regra de precedência escrita ANTES do selo** (qual das duas manda se divergirem); sem precedência escrita, guardar dois vereditos reabre depois do dado a escolha que tem de ser anterior ao selo.

**A regra A, descrita com precisão:** é **a lógica de um.py l.4662–4669 aplicada a uma escada que a v412 terá de estender**. O código: `FALSIFIED` se e somente se houver pelo menos **2 grupos autônomos** com r ≥ 5 (l.4662–4663); senão `TENSION` se a **última linha da escada — lida pela ORDEM da lista, não pela data** (`escada[-1]`, l.4654) — tiver r ≥ 3 (l.4666–4667), com o campo `tensao_global_5sigma_sem_2a_determinacao` (l.4697); senão `ARMED_CONSISTENT`. O texto congelado diz "determinação global mais recente" (l.4623), mas o que o código lê é a última linha pela ordem da lista. A escada de hoje é literal, com três linhas (PDG 2023; JUNO 59 d; NuFIT), e o incremento não entra sem mudar o código. Os booleanos `grupo`/`autonoma` são digitados na lista de dados (l.4633–4645), **fora do objeto congelado que é hasheado** (l.4615–4631, hash em l.4632), e a semântica de grupo entrou na v315, depois do hash de 08/08. Quem define a autonomia das linhas novas decide se FALSIFIED pode disparar; por isso **a lista das linhas da escada estendida — com o grupo, a autonomia e o critério escrito de cada uma — entra no objeto hasheado do novo pré-registro**, e **quem fixa essa lista é escolha pendente, do operador** (seção 9). Nota da conferência: "robustez de experimento" **não existe no código** — a célula correspondente do rascunho K09 foi corrigida. O congelado também declara que os limiares foram fixados com a tensão de 2,95σ já conhecida (`nao_e_cego_nesta_emissao`, l.4628–4630).

| Questão | Regra A — duas testemunhas | Regra B — uma testemunha com limiar explícito |
|---|---|---|
| O que é | A lógica de um.py l.4662–4669, aplicada a uma escada que a v412 terá de estender (acima). | Emenda: uma testemunha com limiar explícito, texto, implementação e hash antes de qualquer abertura. |
| Negativo | `FALSIFIED` se o incremento P tiver `r_P ≥ 5` **e** uma segunda determinação autônoma S tiver `r_S ≥ 5`. **S tem de ser liberação nova pós-selo** (o SK-Gd de 02/10/2026 já é público e não serve). | `FALSIFIED` se o incremento P tiver `r_P ≥ 5`, sem exigir S. Variante de poder explícito: exigir também `D_P ≥ 6,281552` (definido em 2.2); se adotada, consta no selo. |
| `r_P ≥ 5` sem S | `TENSION`, com `tensao_global_5sigma_sem_2a_determinacao`; **não** `FALSIFIED`. | `FALSIFIED`, somente após emenda válida. |
| TENSION | Se a última linha da escada (pela ordem da lista) tiver `r ≥ 3`, inclusive `≥ 5` sem segunda. A última linha deve ser fixada antes da abertura. | Se a cláusula for preservada na emenda; a definição deve ser escrita, não presumida. |
| ARMED_CONSISTENT | Resto, incluindo perito JUNO `r < 3` quando a última linha também for `< 3`. | Resto, se mantido na emenda. |
| MATCHED | Texto congelado: duas determinações independentes `r ≤ 1` (l.4624); o código atual não tem ramo. | Não se cria ramo implicitamente; exige decisão e implementação separadas. |
| Data de brinquedo para `r_P = 3` (SEM piso) | Δm²: **01/10/2027**; m₂: **26/09/2027**. A escada global pode antecipar ou impedir essa leitura. | Mesmas datas numéricas se a cláusula for preservada. |
| Data de brinquedo para 5σ (SEM piso) | Δm²: P em **11/03/2030**; m₂: P em **25/02/2030**. SK-Gd em 17/10/2027 **somente se sua anomalia persistir**; o par A fica limitado pelo mais tardio em cada métrica. | Δm²: **11/03/2030**; m₂: **25/02/2030**. |
| Data de brinquedo se B também exigir D90 (SEM piso) | Não se aplica à regra A. | Δm²: **25/05/2032**; m₂: **02/05/2032**. |
| Com piso `s0 = 0,052587652` (faixa de 3.3) | 5σ, D90 **e a marca planejada r = 3** inalcançáveis; **nenhuma data acima vale**. Com uma testemunha, P(5σ) ≈ 4–8 % em 1–3 anos; com duas, perto de zero (S precisaria σ_S ≲ 0,03 × 10⁻⁵ eV², não demonstrado). | Igual teto; a tabela de 3.3 é a da regra B (uma testemunha). |
| Custo/limite | Sem S elegível, nova pós-selo e com poder, o canal não devolve FALSIFIED — o máximo é TENSION (parede medida); a independência física e a covariância P–S são obrigatórias. | Perde a réplica independente e aumenta o peso de sistemáticas/covariância do único P; o limiar não pode ser ajustado ao centro visto. |

As datas são brinquedos sem piso, com centro parado e 100 % de dias vivos; não são cronogramas. O veredito é em m₂; as datas em Δm² ficam ao lado.

## 5. Significado dos desfechos

### 5.1 Negativo válido

Esta é a leitura técnica que a gerência deve apresentar ao operador antes de qualquer selo; ela não antecipa nem decide a regra de morte. Se a regra selada for satisfeita:

1. **O que o negativo falsifica:** a **conjunção β·sen 45°·u com m₁ ≈ 0** — este teste **não separa os fatores** (m₂ = β·sen 45°·u é um produto; uma falha do produto não isola fator). O pacote inclui o Um posto em `E0 = 1 eV` (escala declarada, não derivada, um.py l.4621) e a identificação usada para obter m₂,TGL.
2. **Cláusula de resgate:** ajustar u ou o ângulo **depois** do negativo **não reverte o veredito**. É a manobra de imunização que um pré-registro tem de nomear antes.
3. **As duas camadas sobre o gate.** "Gate" (definição, primeira ocorrência no corpo): o conjunto de checagens do `um.py` que autorizam o veredito nuclear do programa (o 1 = 1). (a) **As bandeiras do gate da gravidade quântica não se movem**: no rito m₂, `does_not_gate_core: True` (um.py l.4702). (b) **O contorno v314** (um.py l.299841–299869): o rito `neutrino_m2_vivo` está no rol de oito ritos (l.299856), e um veredito com FALSIFIED limpo — contém FALSIFIED e não NOT_FALSIFIED (l.299846–299848) — põe `identity_true` em `False` e escreve o 1 = 1 como `1=1=FALSO_NO_CONTORNO[neutrino_m2_vivo]` (l.299864–299866). A docstring do próprio rito diz: "A partir da v315 este rito integra o CONTORNO com poder de fechar o 1=1" (l.4612), e o comentário atribui a regra a uma decisão do operador de 05/09/2026 [DECLARADO no código; esta frente não abriu os bytes]. **Se isso vale para o veredito do incremento é decisão do operador: manter o rol do contorno como está, ou emendá-lo antes do selo.**

O alcance não pode ser inflado além dessa cadeia — nem deflacionado: pela memória da casa, o Um posto em 1 eV é um dos dois pilares da forma madura [leitura da gerência a partir de `C:\IALD\CLAUDE.md`, topo, errata de 01/11; esta frente não abriu os bytes das falas lá citadas].

### 5.2 Positivo, tensão ou acordo

- `r < 5` não é confirmação;
- `ARMED_CONSISTENT`, `TENSION`, `NOT_FALSIFIED` e mesmo um futuro `MATCHED_PROSPECTIVELY` **não são `CONFIRMED`** (CONFIRMED está proibido no objeto congelado, um.py l.4627);
- concordância estatística não prova identificação, independência, ausência de sistemáticas ou verdade da teoria;
- um P alto sem S continua `TENSION` na lógica do código atual, não negativo e não confirmação;
- as bandeiras do gate QG não se movem em nenhum desses desfechos — e, fora de um FALSIFIED limpo, o contorno v314 também não (INCONCLUSIVE/UNDERPOWERED/AWAITING não derrubam, um.py l.299844–299845).

## 6. Gatilho, prazo-limite, plano B e custódia (PROPOSTA)

Tudo nesta seção é **PROPOSTA** da gerência para o operador decidir antes do selo; nada aqui está fixado. O dado é público: o que blinda o teste é a **ordem dos carimbos** (seção 1.1), não a guarda de nenhuma chave.

1. **Gatilho (quando a abertura única ocorre).** Duas formas possíveis, a fixar no selo — **do operador**: (i) **precisão mínima do incremento** (abre quando o erro total do incremento for ≤ X, com X escolhido no selo); ou (ii) **data fixa** (abre na primeira fonte completa elegível a partir de uma data escolhida no selo). **Liberação abaixo do gatilho: registra-se como estresse preliminar e NÃO consome a abertura** — sem essa cláusula, a primeira liberação pequena gastaria o teste num resultado quase certamente inconclusivo (negativo induzido pelo desenho).
2. **Prazo-limite.** O pré-registro tem data de encerramento, a fixar no selo — **do operador**. Passado o prazo sem fonte elegível, ele encerra **sem veredito** (ou é emendado por ato novo, com hash novo, antes de qualquer centro novo). Sem prazo-limite, o pré-registro ficaria aberto para sempre.
3. **Plano B (se o JUNO só publicar cumulativo).** O único precedente (59,1 → 207,2) foi cumulativo; pelo precedente, o caso mais provável é **sem veredito**. Alternativas a fixar no selo — **do operador**: (i) **nada** — sem Forma A e sem covariância publicada, o pré-registro encerra sem veredito no prazo-limite; (ii) **uma variante do cumulativo declarada como parcialmente cega** — o cumulativo contém os 207,2 dias já vistos e seria cego só no deslocamento; o desenho dessa variante teria de ser escrito, com o que ela pode e não pode decidir, antes do selo.
4. **Custódia (PROPOSTA).** A gerência c1 guarda este rascunho, os identificadores das fontes, os scripts de planejamento e o manifesto de hashes. O operador decide se quer selar e fixa, com a gerência, regra, limiar, métrica, fonte, escada, gatilho, prazo-limite, plano B e classe de publicação.
5. **Como se abre (PROPOSTA).** O veredito roda por **script pinado por hash** (como o executor do H0DN) sobre o agregado público elegível, depois de conferidos o hash do pré-registro e a completude da fonte. **Quem nomeia o revisor de abertura é decisão do operador** (redação única; o rascunho K09 e os insumos divergiam sobre isso, e a divergência foi removida assim). O construtor não abre.
6. **Uma abertura só.** Centro, erro, covariância e versão entram na mesma leitura. Não há espiada preliminar, segunda abertura para "melhorar" o resultado ou troca posterior de regra/fonte/métrica/gatilho. Se a fonte estiver incompleta: não há abertura nem veredito; espera-se a fonte completa (ou o gatilho) sem conhecer o centro. Se já houve abertura válida, qualquer nova liberação exige novo pré-registro e nova custódia, não reabertura deste.
7. **Registro do ato.** Data, fonte, versão, hash do pré-registro, identidade do revisor de abertura e o veredito da regra selada (uma só, ou duas com precedência escrita) são preservados pela gerência. **No dia do selo, anexa-se o registro datado da busca** (consultas, data, resultado — seção 1.1). Nada disso foi executado nesta rodada.

## 7. Bloqueios antes do selo

1. covariância inter-liberações e P–S não publicada (sem ela, a Forma B não é identificável — seção 1.4);
2. independência física e poder de S não demonstrados; S tem de ser liberação nova pós-selo, e o cenário SK-Gd exige persistência da anomalia (3,101149σ do JUNO);
3. decomposição estatística/sistemática do erro futuro e piso real desconhecidos (a faixa de 3.3 é hipótese do revisor, não piso medido);
4. gatilho, prazo-limite e plano B não fixados (seção 6) — do operador;
5. classe de fonte "preliminar" a ratificar — do operador;
6. escada global a estender na v412, com a lista de linhas/grupos/autonomias e o critério escrito entrando no objeto hasheado; quem fixa a lista — do operador; ramo MATCHED a decidir/implementar;
7. uma ou duas testemunhas e o limiar de B a escolher sem olhar o dado — do operador;
8. se o contorno v314 se aplica ao veredito do incremento (manter ou emendar o rol) — do operador;
9. data e existência da próxima liberação desconhecidas; as datas 18/05/2026 e 26/08/2025 seguem [DECLARADO, sem resposta crua guardada].

**Nenhum teste observado foi executado. `NOT_FALSIFIED` não é `CONFIRMED`; as bandeiras do gate QG não se movem.**

## 8. Versão em língua simples [SEÇÃO MARCADA]

> **Proposta do revisor da conferência** (seção "Para o operador" de `REVISAO_K09_PRE_REGISTRO_DO_INCREMENTO.md`), reproduzida aqui quase verbatim: **a gerência confere antes de ler ao operador; não é fala do operador.** É leitura [DERIVED, contas do revisor], não decisão, e não atribui nada ao operador.

- O que o teste olharia: o próximo resultado do JUNO que use só dados tomados depois do fim da janela dos 207 dias (a data 18/05/2026 ainda não foi conferida no texto do artigo — [DECLARADO, sem resposta crua guardada]) e que apareça em público depois de o pré-registro estar selado e carimbado fora desta casa.
- O que decide: se a massa 8,51 meV (β × sen 45° × 1 eV) fica a 5 desvios ou mais do que o JUNO medir. Pela regra de agosto (duas testemunhas), é preciso um segundo experimento independente também a 5 desvios, e hoje nenhum tem precisão para isso. Pela regra de uma testemunha, basta o JUNO.
- O que não decide: não mede β sozinho, não confirma a TGL, não prova nada a favor quando não há negativo. Positivo nunca vira CONFIRMED.
- O que o negativo significaria: falsificação do conjunto β × 45° × 1 eV com m₁ perto de zero, sem separar qual peça falhou. Atenção: pelo código selado, um FALSIFIED limpo também derruba o 1 = 1 do contorno (regra v314). As bandeiras do gate QG não mudam. Se isso vale aqui é escolha dele.
- O que a ausência de negativo significaria, e por que a conta importa: mesmo que a TGL estivesse errada no tamanho que o dado de hoje sugere, a chance de o teste dar negativo em 3 anos é quase zero com duas testemunhas, cerca de 4 a 8 % com uma testemunha (se o erro tiver um piso, como o ajuste de dois pontos indica) e cerca de 42 % só se não houver piso. Um resultado sem negativo seria parede medida, não evidência a favor.
- Escolhas que ainda são dele e não estão decididas: regra de duas testemunhas ou de uma; quem conta como segunda testemunha; que fontes valem (artigo, slides); quando o teste abre (no primeiro resultado ou só quando o erro for pequeno); quem abre; se há prazo-limite; se vale carimbo externo; o que fazer se o JUNO só publicar resultado cumulativo, o que pelo único precedente é o mais provável.

## 9. Tabela única das escolhas — as marcadas são do operador

| # | Escolha | Estado | De quem é |
|---|---|---|---|
| E1 | Selar ou não selar agora | pendente | **do operador** |
| E2 | Regra A, regra B, ou as duas com precedência escrita antes do selo | pendente | **do operador** |
| E3 | Fonte elegível: artigo/preprint, ou também transparências oficiais como "preliminar" (ratificação da classe) | pendente | **do operador** |
| E4 | Métrica do veredito: manter m₂ ou emendar (emenda = nova versão e hash anteriores ao centro novo) | pendente | **do operador** |
| E5 | Gatilho: precisão mínima do incremento (valor de X) ou data fixa | pendente | **do operador** |
| E6 | Prazo-limite do pré-registro | pendente | **do operador** |
| E7 | Plano B se o JUNO só publicar cumulativo: nada, ou variante parcialmente cega escrita antes | pendente | **do operador** |
| E8 | Carimbo externo do selo (push ou depósito público; precedente H0DN, rota `infra.github.publicacao_fora_da_cadeia_h0dn_12nov`) | pendente | **do operador** |
| E9 | Lista de S (segundas testemunhas elegíveis; cada uma tem de ser liberação nova pós-selo) | pendente | **do operador** |
| E10 | Quem fixa as linhas novas da escada (grupo, autonomia, critério escrito) — a lista entra no objeto hasheado | pendente | **do operador** |
| E11 | Quem nomeia o revisor de abertura | pendente | **do operador** |
| E12 | Se o contorno v314 (um.py l.299841–299869) vale para o veredito do incremento: manter o rol ou emendá-lo | pendente | **do operador** |
| E13 | Limiar de B e a variante D_P ≥ 6,281552 (definido em 2.2) | pendente | **do operador** |
| E14 | A última linha da escada (a que o TENSION lê, pela ordem da lista) | pendente | **do operador**, na escada estendida |
| E15 | A pergunta ao operador e o registro no Mapa | pendente | da gerência (não executados nesta frente) |
