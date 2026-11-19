# PRÉ-REGISTRO CEGO — RASCUNHO K01, SOMENTE DESENHO, NÃO EXECUTAR

[DECLARADO] Documento candidato para o canal `neutrino_m2_juno`, preparado em 13/11/2026. Não é uma emenda ratificada ao `NEUTRINO_M2_V2`, não autoriza abertura e não altera o frozen, o core, o kernel ou o gate. Quem constrói não aprova: gerência e operador precisam revisar antes de qualquer uso.

[REAL] Nenhum vetor de dados foi lido, nenhuma likelihood foi aberta e nenhum Z, H0 ou veredito observado foi calculado nesta K01. As contas abaixo são somente de desenho, com β = `ALPHA_FINE_CODATA_2018 × √e` em runtime.

## 1. Por que este é o único canal deste rascunho

[DERIVED] O m₂ permanece como único rascunho porque tem tranca prospectiva e um cenário publicado de sensibilidade que ainda cruza D90, não porque o resultado esperado seja favorável. A determinação pública mais recente muda o planning: com 207,2 dias, D de desenho com o σ publicado é 1,9281; com 0,5 %, D = 4,0712 e não basta; somente a tabela de 0,3 % dá D = 6,7854 e supera D90. O poder conjunto das duas testemunhas permanece [OPEN].

[REAL] A determinação de 29/09/2026 já é pública e não será tratada como futura. [JUNO Collaboration, 2026](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2609.37895&text=207.2%20live%20days%20of%20data "citation")

[DERIVED] O segundo candidato de cegueira, ringdown D, não foi escolhido porque seu planejamento mais recente dá D10 = 3,9346 no melhor caso e D14 = 4,6374 sem sistemática, abaixo de 5 e de D90. [PODER_RAMO_B_ANTES_DE_ABRIR](kimi-cite://text?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Cconjunto_D_20261029%5Cparametrizacao_03nov%5CPODER_RAMO_B_ANTES_DE_ABRIR.json&text=%22poder%22%3A%203.9346337577944936 "citation")

[DECLARADO] Não se abre um segundo pré-registro para ringdown nesta entrega. O V1 e o congelamento de 03/11/2026 já existem; esta K01 não os substitui nem recomenda abrir D sem poder e sem a palavra do operador.

## 2. Hipótese, escala, conversão exata e objeto de morte

[DERIVED] A forma condicional é

\[
m_2=\beta\,\sen(45^\circ)\,E_0,
\qquad \beta=\alpha_{\rm CODATA\ 2018}\sqrt e,
\qquad E_0=1\ {\rm eV}.
\]

[REAL] O valor lido no core é m₂ = 8,507414099900329 meV. [um_absoluto](kimi-cite://text?path=C%3A%5CIALD%5CArtigo%5CHaja_Luz%5CA%20Ponte%20e%20o%20Um%5CN%C3%B3s%5Cum_absoluto.json&text=%22predicao%22%3A%20%22m_2%20%3D%20beta_TGL*sin(45)*1eV "citation")

[DERIVED] Com m₁ ≈ 0 e ordenamento normal, a conversão usada no teste é exata:

\[
\Delta m^2_{21,\rm pred}=m_{2,\rm pred}^2
=7,237609466718292\times10^{-5}\ {\rm eV}^2 .
\]

[DECLARADO] Todo o poder e toda a regra de veredito serão definidos em Δm²₂₁. Se m₂ aparecer em alguma exposição, a conversão será `m₂ = √Δm²₂₁`; propagação `σ_m₂ ≈ σ(Δm²₂₁)/(2m₂)` é apenas uma aproximação de primeira ordem e não entra no D nem no veredito.

[INPUT] E0 = 1 eV é declarado, não derivado; m₁ ≈ 0 e o ordenamento normal fazem parte do pacote de identificação. [DERIVED] O sen45 tem suporte formal condicional à identificação ONTO registrada, mas isso não deriva E0 nem transforma a identificação física em teorema independente.

[DECLARADO] O objeto de `FALSIFIED` é o pacote `Δm²₂₁,pred = (β·sen45°·E0)²` com E0 = 1 eV e m₁ ≈ 0, testado no setor de oscilação. Um negativo atinge a escala/identificação; não falsifica β isoladamente, não falsifica toda a TGL e não move o gate.

## 3. Liberações públicas, dados permitidos e tranca de cegueira

[REAL] As duas determinações JUNO relevantes já públicas são versionadas assim, sem tratá-las como futuras:

| Liberação | Centro público e precisão | Papel nesta K01 e cegueira |
|---|---|---|
| JUNO Collaboration, `arXiv:2511.14593v1`, 18/11/2025, 59,1 dias | [KNOWN, a conferir] Δm²₂₁ = (7,50 ± 0,12) × 10⁻⁵ eV²; precisão relativa aproximada de 1,6 % | [DECLARADO] **Histórico, já público e conhecido.** Serve somente à auditoria da mudança; não é P futuro nem testemunha independente da liberação de 207,2 dias. [JUNO Collaboration, 2025](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2511.14593&text=using%20the%20first%2059.1%20days%20of%20data "citation") |
| JUNO Collaboration, `arXiv:2609.37895v1`, 29/09/2026, 207,2 dias | [KNOWN, a conferir] Δm²₂₁ = (7,388 ± 0,078) × 10⁻⁵ eV²; precisão publicada de 1,1 % | [DECLARADO] **Planning público elegível mais recente, já público e conhecido.** Não é dado futuro nem uma nova abertura cega da casa. [JUNO Collaboration, 2026](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2609.37895&text=207.2%20live%20days%20of%20data "citation") |

[REAL] A liberação de 207,2 dias contém e estende a de 59,1 dias. [DERIVED] Conteúdo incremental de observação não equivale a uma determinação independente: a análise incremental exigiria covariância condicional entre as liberações cumulativas. A próxima liberação cumulativa também conterá dados anteriores e exigirá a mesma distinção entre incremento de conteúdo e independência estatística.

[KNOWN, a conferir] A colaboração descreve sua própria estratégia de blinding na análise de 207,2 dias. [DECLARADO] Essa cegueira experimental não é herdada pela casa: os centros e erros já são públicos e conhecidos aqui, portanto as duas liberações acima só entram como planning documental.

[DECLARADO] **Primário P:** uma determinação `JUNO-only` **posterior a 29/09/2026 e ainda não comunicada à casa**, com centro, σ total em eV², versão de análise, covariância/nuisances e data pública identificados. P não pode ser uma combinação que já contenha KamLAND, solar ou outro ajuste usado como segunda testemunha.

[DECLARADO] **Secundário S:** uma determinação independente de P, com JUNO explicitamente excluído, centro, σ total em eV², versão e covariância/sistemática públicos. A equipe, a versão e o conjunto exato de dados de S precisam ser fixados pelo operador antes da liberação/abertura/comunicação de P à casa. A ausência de S é um estado explícito da tabela-verdade e não é confundida com falha de integridade.

[REAL] Um ajuste global que contenha JUNO não é independente de P. NuFIT/Capozzi ou outro ajuste só entram em S se a exclusão de JUNO estiver explícita; a escolha entre equipes não pode ser feita pelo centro, pelo erro ou pelo sinal obtido depois da leitura.

[REAL] O frozen anterior declara que sua emissão inicial não foi cega, pois a tensão corrente já era conhecida, e que a cegueira vale prospectivamente a partir de 08/08/2026. [DECLARADO] Essa contaminação histórica permanece escrita; ela não é apagada por este rascunho.

[DECLARADO] Um terceiro custodiante deve receber P e S sem os comunicar à casa. A abertura ocorre uma única vez, depois da conferência dos hashes e dos controles. Nenhuma análise preliminar de P/S pode orientar cortes, fonte, pesos, limiar ou ramos.

[DECLARADO] **Marco temporal obrigatório:** o timestamp externo da guarda deve preceder **a liberação pública da determinação, a abertura pela casa e a comunicação de centro/erro à casa**, conforme o que ocorrer primeiro no protocolo. Aquisição de bytes não é o marco de cegueira: guardar o arquivo não substitui a exigência de que a tranca seja anterior à liberação/abertura/comunicação.

## 4. Poder de desenho, integralmente em Δm²₂₁

[DERIVED] Defina `r = σ(Δm²₂₁)/Δm²₂₁_planning`. O poder fiducial é calculado sem qualquer linearização em m₂:

\[
D_{\rm exato}(r)=\frac{\left|1-\Delta m^2_{21,\rm pred}/\Delta m^2_{21,\rm planning}\right|}{r}
=\frac{|\Delta m^2_{21,\rm planning}-\Delta m^2_{21,\rm pred}|}{\sigma_{\rm total}} .
\]

[DERIVED] Para o planning mais recente, Δm²₂₁,planning = 7,388 × 10⁻⁵ eV², Δm²₂₁,pred = 7,237609466718292 × 10⁻⁵ eV² e σ_total = 0,078 × 10⁻⁵ eV²:

| Insumo de precisão | Conta exata de desenho | Resultado |
|---|---|---|
| σ publicado de 207,2 dias | [DERIVED] `D = |7,388−7,2376094667|/0,078` | **D = 1,9281**, não um Z observado nem um veredito |
| precisão relativa necessária para 5σ | [DERIVED] `r₅ = |1−7,2376094667/7,388|/5` | **0,407121 %** |
| precisão relativa necessária para D90 = 6,2815515655 | [DERIVED] `r_D90 = |1−7,2376094667/7,388|/6,2815515655` | **0,324061 %** |
| forecast `r = 0,005 = 0,5 %` | [DERIVED] `D = |1−7,2376094667/7,388|/0,005` | **D = 4,0712**: abaixo de 5 e de D90 |
| tabela `r = 0,003 = 0,3 %` | [DERIVED] `D = |1−7,2376094667/7,388|/0,003` | **D = 6,7854**: acima de 5 e de D90 |

[REAL] A precisão publicada para 207,2 dias é 1,1 %; a razão aritmética 0,078/7,388 é 1,0558 %. [DERIVED] O D = 1,9281 usa diretamente os dois valores publicados em Δm²₂₁ e não é apresentado como tensão nova nem como veredito observado.

[DERIVED] **Somente como histórico, não como planning atual:** a liberação de 59,1 dias daria, com a fórmula exata, D = 6,9971 para 0,5 % e exigiria 0,55695 % para D90. Esses números confirmam a inconsistência da antiga aproximação linear, mas não são mantidos como previsão vigente.

[KNOWN, a conferir] O estudo de sensibilidade do JUNO publica precisão melhor que 0,5 % em seis anos para os parâmetros de oscilação, e a tabela pública associada dá 0,3 % para Δm²₂₁; são forecasts com o modelo de sistemáticas do projeto, não garantia de realização nem de independência. [JUNO Collaboration](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2204.13249&text=will%20be%20determined%20to%20better%20than%200.5%25%20precision%20in%20six%20years%20of%20data%20collection "citation"), [JUNO/ICHEP](kimi-cite://web?url=https%3A%2F%2Findico.cern.ch%2Fevent%2F1291157%2Fcontributions%2F5888133%2Fattachments%2F2899170%2F5083623%2Fjuno_ichep2024_calvez.pdf "citation")

[REAL] A coleta física começou em 26/08/2025. [JINR](kimi-cite://web?url=https%3A%2F%2Fwww.jinr.ru%2Fposts%2Fjuno-experiment-begins-taking-data%2F&text=On%2026%20August%202025%2C%20a%20physics%20experiment%20started "citation")

[DERIVED] Seis anos nominais após essa data terminam em **26/08/2031**. [DECLARADO] Essa é a data de exposição de referência, não uma data prometida de publicação nem uma autorização para esperar por um centro favorável. A data pública da próxima liberação permanece [OPEN].

[OPEN] **O poder conjunto de P e S permanece aberto.** D_P e D_S são relatados separadamente; não se calcula poder conjunto antes de nomear S, conhecer sua precisão, independência e covariância condicional com P.

[DECLARADO] O cálculo de D deve ser refeito documentalmente antes da abertura somente com σ publicado e covariância declarada. Se a precisão não incluir sistema de referência, covariância com θ₁₂, fluxo de reator, não-linearidade e fundos, o estado é `AWAITING_SOURCE`, não uma precisão presumida.

## 5. Pesos, elegibilidade, integridade e estresses

[DECLARADO] **Sem média inversa-da-variância para matar.** P e S recebem peso lógico 1 cada e são avaliados separadamente; combinar os dois por 1/σ² poderia diluir uma discordância e está proibido para o ramo `FALSIFIED`.

[DECLARADO] `r_X = |Δm²₂₁,X − Δm²₂₁,pred|/σ_X`, com X = P ou S, só é calculado na abertura autorizada, em eV², nunca por aproximação em m₂. D_P e D_S são quantidades de desenho separadas; o poder conjunto fica [OPEN].

[DECLARADO] **Estados de S:** `ABSENT` quando ainda não nomeado; `NONINDEPENDENT` quando contém JUNO ou compartilha dados sem covariância condicional aceita; `INDEPENDENT` quando exclui JUNO e tem independência/sistemáticas documentadas; `INVALID` quando falha uma regra objetiva de integridade. S ausente ou não independente não é automaticamente inválido, mas nunca conta para a dupla exigência de `FALSIFIED` ou `MATCHED`.

[DECLARADO] **Falhas objetivas de integridade, fail-closed:** hash ou versão divergente; unidade diferente de eV²; centro não finito; σ_total não finito ou ≤ 0; fonte/versão/data ausente; covariância/nuisances exigida ausente; timestamp posterior à liberação/abertura/comunicação; fórmula, pesos, limiar ou código alterados depois da guarda; ou r não finito. Falha em P devolve `INCONCLUSIVE_SYSTEMATICS__INTEGRITY_P`; falha em S devolve `INCONCLUSIVE_SYSTEMATICS__INTEGRITY_S`. Metadados essenciais ausentes em P podem devolver `AWAITING_SOURCE_P` somente quando ainda não houve abertura nem comunicação do centro.

[DECLARADO] Ajustes adicionais, inclusive KamLAND+solar, NuFIT ou Capozzi, aparecem sempre como linhas de estresse, nunca como um menu do qual se escolhe a determinação mais conveniente. Não se contam duas vezes JUNO, um global com JUNO e outro global com os mesmos dados.

[DECLARADO] **Estresse não é veto discricionário.** Discordância de um ajuste de estresse não altera o ramo principal por si só. Só uma falha objetiva previamente congelada no parágrafo anterior produz `INCONCLUSIVE`; todo estresse é publicado ao lado do resultado, inclusive quando contraria a previsão.

[DECLARADO] Para `MATCHED_PROSPECTIVELY`, mantém-se a regra frozen: duas determinações independentes precisam cair a 1σ de Δm²₂₁,pred. Mesmo nesse caso, o ramo não significa `CONFIRMED`.

## 6. Tabela-verdade determinística da função de veredito

[DECLARADO] Primeiro valida-se P; depois classifica-se S. Para X ∈ {P,S}, `T_SINGLE(X)` significa o token candidato `TGL_NU_M2_TENSION__SINGLE_X_AWAITING_INDEPENDENT_CONFIRMATION` ou, sem ratificação do operador, `OPEN_RULE_GAP`. O nome nunca muda o conteúdo: uma só determinação ≥5 não falsifica o pacote. A tabela cobre todos os estados de P/S e todas as faixas de r.

| Condição de P | Estado de S | Faixa de r_S | Ramo determinístico |
|---|---|---|---|
| P ausente ou com metadados essenciais antes da abertura | qualquer | qualquer | `AWAITING_SOURCE_P` |
| P com falha objetiva de integridade | qualquer | qualquer | `INCONCLUSIVE_SYSTEMATICS__INTEGRITY_P` |
| r_P ≥ 5 | `INVALID` | qualquer | `INCONCLUSIVE_SYSTEMATICS__INTEGRITY_S` |
| r_P ≥ 5 | `ABSENT` | não se aplica | `T_SINGLE(P)_AWAITING_S` ou `OPEN_RULE_GAP` |
| r_P ≥ 5 | `NONINDEPENDENT` | qualquer | `T_SINGLE(P)_NONINDEPENDENT` ou `OPEN_RULE_GAP` |
| r_P ≥ 5 | `INDEPENDENT` | r_S < 5 | `T_SINGLE(P)_SECOND_BELOW_5` ou `OPEN_RULE_GAP` |
| **r_P ≥ 5** | **`INDEPENDENT`** | **r_S ≥ 5** | **`TGL_NU_M2_FALSIFIED`** |
| 3 ≤ r_P < 5 | `INVALID` | qualquer | `INCONCLUSIVE_SYSTEMATICS__INTEGRITY_S` |
| 3 ≤ r_P < 5 | `ABSENT` ou `NONINDEPENDENT` | qualquer | `TGL_NU_M2_TENSION__P` |
| 3 ≤ r_P < 5 | `INDEPENDENT` | r_S < 3 | `TGL_NU_M2_TENSION__P` |
| 3 ≤ r_P < 5 | `INDEPENDENT` | r_S ≥ 3 | `TGL_NU_M2_TENSION__BOTH` |
| 1 < r_P < 3 | `INVALID` | qualquer | `INCONCLUSIVE_SYSTEMATICS__INTEGRITY_S` |
| 1 < r_P < 3 | `ABSENT` ou `NONINDEPENDENT` | qualquer | `UNDER/ARMED` com P apenas |
| 1 < r_P < 3 | `INDEPENDENT` | r_S < 3 | `UNDER/ARMED` com P e S separados |
| 1 < r_P < 3 | `INDEPENDENT` | 3 ≤ r_S < 5 | `TGL_NU_M2_TENSION__BOTH` |
| 1 < r_P < 3 | `INDEPENDENT` | r_S ≥ 5 | `T_SINGLE(S)_SECOND_ALONE_GE_5` ou `OPEN_RULE_GAP` |
| r_P ≤ 1 | `INVALID` | qualquer | `INCONCLUSIVE_SYSTEMATICS__INTEGRITY_S` |
| r_P ≤ 1 | `ABSENT` ou `NONINDEPENDENT` | qualquer | `UNDER/ARMED` com P apenas |
| r_P ≤ 1 | `INDEPENDENT` | r_S ≤ 1 | `TGL_NU_M2_MATCHED_PROSPECTIVELY` |
| r_P ≤ 1 | `INDEPENDENT` | 1 < r_S < 3 | `UNDER/ARMED` com P e S separados |
| r_P ≤ 1 | `INDEPENDENT` | 3 ≤ r_S < 5 | `TGL_NU_M2_TENSION__S` |
| r_P ≤ 1 | `INDEPENDENT` | r_S ≥ 5 | `T_SINGLE(S)_SECOND_ALONE_GE_5` ou `OPEN_RULE_GAP` |

[DECLARADO] `UNDER/ARMED` é uma regra auxiliar, nunca um veto a `FALSIFIED`: se todas as determinações válidas disponíveis tiverem D < 5, devolve `TGL_NU_M2_NOT_FALSIFIED_UNDERPOWERED`; se ao menos uma tiver D ≥ 5, devolve `TGL_NU_M2_ARMED_CONSISTENT`, com D_P e D_S declarados separadamente. Se D necessário a esse ramo for desconhecido, devolve `AWAITING_SOURCE`. O poder conjunto não é inferido e permanece [OPEN].

[DECLARADO] A tabela torna `TENSION_SINGLE` alcançável: P ≥ 5 com S ausente ou não independente não passa por `AWAITING_SOURCE` nem por `INCONCLUSIVE` por simples ausência/não independência; vai diretamente ao ramo ratificado `T_SINGLE(P)` ou a `OPEN_RULE_GAP`. Em contraste, uma falha objetiva de integridade de S continua fail-closed em `INCONCLUSIVE_S`.

[OPEN] O frozen atual explicita `TENSION` em [3,5) e `FALSIFIED` com duas determinações ≥5, mas não diz com clareza o ramo de uma única determinação ≥5 sem a segunda. `T_SINGLE` é proposta [DECLARADO], não uma ratificação já obtida. Sem a palavra do operador, o fallback é `OPEN_RULE_GAP`, nunca `ARMED_CONSISTENT` e nunca `FALSIFIED` por uma só determinação.

[DECLARADO] O ramo de poder não pode vetar `FALSIFIED`: um D subestimado não impede uma falsificação observada sob a regra. Por outro lado, D ≥ 5 no desenho não autoriza antecipar qualquer resultado.

## 7. Significado de cada ramo

- [DECLARADO] `FALSIFIED`: o pacote Δm²₂₁,pred = (E0·sen45°·β)² com E0 = 1 eV e m₁≈0 é rejeitado somente quando duas determinações independentes têm r ≥ 5; β sozinho, a TGL inteira e o gate não são rejeitados por esse token.
- [DECLARADO] `TENSION_SINGLE`: uma única determinação ≥5 pressiona a escala/pacote, mas a condição dupla de morte não foi cumprida; S ausente ou não independente é relatado explicitamente, sem converter a falta de segunda testemunha em FALSIFIED.
- [DECLARADO] `TENSION`/`TENSION_BOTH`: uma ou ambas as determinações têm r ≥ 3 sem satisfazer a dupla exigência de 5; é pressão, não confirmação nem morte.
- [DECLARADO] `MATCHED_PROSPECTIVELY`: há concordância prospectiva dentro de 1σ nas duas linhas independentes; não é `CONFIRMED`, creditação nem fechamento de outros setores.
- [DECLARADO] `NOT_FALSIFIED_UNDERPOWERED`: a natureza não foi alcançada com poder suficiente; é parede medida de desenho, não evidência a favor. O poder conjunto permanece [OPEN].
- [DECLARADO] `INCONCLUSIVE_SYSTEMATICS__INTEGRITY_P/S`: houve falha objetiva de integridade; não é veredito sobre a lei e não pode ser contornado por ausência de segunda fonte.
- [DECLARADO] `AWAITING_SOURCE`/`OPEN_RULE_GAP`: o protocolo ou a ratificação está incompleto; nenhuma inferência física é permitida.

[DECLARADO] Em todos os ramos: `NOT_FALSIFIED ≠ CONFIRMED`; o gate permanece imóvel; retrodição sem ajuste continua evidência legítima, mas não é rotulada como teste cego; o termo de linguagem pública, quando cabível, é «descoberta autoevidente em dados públicos, carente de creditação acadêmica», nunca autocrédito da máquina.

## 8. Guarda contra emenda posterior

1. [DECLARADO] Antes de qualquer nova liberação, abertura ou comunicação de centro/erro à casa, gerência publica um manifesto com timestamp externo e sha256 deste rascunho ratificado, do `CANAIS_K01.json`, do frozen de origem, da tabela-verdade, das fontes P/S e do código de execução. Aquisição de bytes não é o marco de cegueira.
2. [DECLARADO] Qualquer mudança de fórmula, E0, ordenamento, P/S, pesos, independência, limiar, ramo, código ou hash depois da guarda é falha objetiva e devolve `INCONCLUSIVE_SYSTEMATICS__INTEGRITY`, nunca um `AWAITING_SOURCE` incompatível com a tabela.
3. [DECLARADO] Uma versão nova só pode ser escrita antes de uma nova liberação/abertura/comunicação e deve apresentar toda a tabela de tentativas; nenhuma emenda posterior a centro, σ, D ou resultado pode trocar TENSION por FALSIFIED ou UNDERPOWERED por POWERED.
4. [DECLARADO] A abertura é única e vinculada ao manifesto. Repetição técnica só é permitida por falha documentada que não envolva ler centro ou significância; depois de lido qualquer resultado, não há reabertura para “melhorar” o desenho.
5. [DECLARADO] Testes sintéticos futuros devem exercitar todas as linhas da tabela-verdade: P/S ausentes, inválidos, não independentes e independentes; r < 1, entre 1 e 3, entre 3 e 5 e ≥5; P ≥5 com S ausente/não independente; e versão alterada. Eles validam a função, não a física; nenhum teste foi executado aqui.
6. [DECLARADO] O calendário não pode ser movido para aguardar uma precisão ou um centro conveniente. Toda liberação elegível e toda tentativa entram num registro append-only, inclusive as que forem contra a previsão. Liberações cumulativas exigem covariância condicional e não são contadas como independentes por conterem novos dias.
7. [DECLARADO] A revisão científica e a aprovação são de pessoas diferentes do redator; a palavra final de abertura é ato separado do operador.

## 9. As sete ressalvas, uma a uma

| Ressalva V411 | Tratamento proposto e limite remanescente |
|---|---|
| R1 — emenda pós-guarda/não cegueira | [DECLARADO] **PARCIAL.** Há tranca prospectiva desde 08/08/2026, mas a regra inicial foi escrita com tensão conhecida. Esta versão só vale com timestamp anterior à liberação/abertura/comunicação, não apenas à aquisição; a história e REV0 são preservados em errata. |
| R2 — primário previsível por agregados | [DECLARADO] **RESPOSTA FUTURA LIMITADA.** P deve ser posterior a 29/09/2026 e ainda não comunicado à casa. As determinações de 59,1 e 207,2 dias já são públicas e só entram como planning, nunca como dado futuro. |
| R3 — Cefeidas livres/linha de estresse | [DECLARADO] **SUBSTITUIÇÃO EXPLÍCITA.** P = JUNO-only e S = global-sem-JUNO ficam sempre lado a lado; KamLAND+solar e demais ajustes são estresse, nunca escondidos nem usados como menu. Estresse não veta a regra sem falha objetiva congelada. |
| R4 — poder só de desenho | [DECLARADO] **PARCIAL.** O planning atual dá D = 1,9281 com σ publicado, D = 4,0712 para 0,5 % e D = 6,7854 para 0,3 %; o poder conjunto de P/S permanece [OPEN]. Não se afirma 5σ de resultado. |
| R5 — 72 direções de variância zero/covariância | [DECLARADO] **NÃO SE APLICA LITERALMENTE, MAS SEGUE ABERTA.** Exige-se covariância de oscilação, nuisances e sistemáticas compartilhadas; liberações cumulativas exigem covariância condicional. Precisão sem modelo completo devolve `AWAITING_SOURCE`. |
| R6 — escolhas com tabela de poder à vista | [DECLARADO] **PARCIAL.** O canal foi mantido porque 0,3 % ainda cruza D90, enquanto 0,5 % falha; os 20 canais continuam visíveis. A escolha de S e a redação de `TENSION_SINGLE`/`OPEN_RULE_GAP` ficam para o operador antes de qualquer centro novo. |
| R7 — tentativas/sobreposição | [DECLARADO] **PARCIAL.** P e S só contam se independentes; 59,1 e 207,2 dias são cumulativos e não contam como duas testemunhas. Conteúdo incremental exige covariância condicional, e todas as tentativas ficam append-only. |

[DERIVED] Consequência honesta: o desenho responde melhor a R2–R5 do que a R1, R6 e R7; não “resolve as sete ressalvas” por decreto. A independência da segunda determinação, o poder conjunto e a ratificação do ramo de única ≥5 continuam bloqueios.

## 10. Decisões necessárias antes de transformar o rascunho em protocolo

- [DECLARADO] **Operador:** manter ou alterar a exigência de duas determinações independentes ≥5; recomenda-se manter. Se mantiver, nomear S com JUNO excluído e ratificar o token `TENSION_SINGLE` ou o fallback `OPEN_RULE_GAP` para os casos explicitados na tabela.
- [DECLARADO] **Operador:** ratificar que o negativo atinge E0/identificação e não β isoladamente nem a TGL inteira, preservando o gate imóvel.
- [DECLARADO] **Gerência:** conferir as fontes `arXiv:2511.14593v1` e `arXiv:2609.37895v1`, os hashes, o cálculo exato em Δm²₂₁, a tabela-verdade e a lista completa de tentativas; preparar custódia e revisão independente, sem executar P/S.
- [DECLARADO] **Operador, em ato futuro separado:** autorizar ou recusar a abertura depois de o estágio cego documentar poder e independência. Este arquivo não é essa autorização.

[OPEN] As perguntas operacionais estão separadas em `PERGUNTA_K01.md`. O restante do levantamento foi concluído sem depender dessas respostas.
