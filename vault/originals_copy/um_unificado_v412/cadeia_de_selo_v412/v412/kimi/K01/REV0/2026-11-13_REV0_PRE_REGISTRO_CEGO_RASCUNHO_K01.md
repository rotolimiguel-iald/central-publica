# PRÉ-REGISTRO CEGO — RASCUNHO K01, SOMENTE DESENHO, NÃO EXECUTAR

[DECLARADO] Documento candidato para o canal `neutrino_m2_juno`, preparado em 13/11/2026. Não é uma emenda ratificada ao `NEUTRINO_M2_V2`, não autoriza abertura e não altera o frozen, o core, o kernel ou o gate. Quem constrói não aprova: gerência e operador precisam revisar antes de qualquer uso.

[REAL] Nenhum vetor de dados foi lido, nenhuma likelihood foi aberta e nenhum Z, H0 ou veredito observado foi calculado nesta K01. As contas abaixo são somente de desenho, com β = `ALPHA_FINE_CODATA_2018 × √e` em runtime.

## 1. Por que este é o único canal deste rascunho

[DERIVED] O m₂ foi escolhido porque é o único canal levantado com tranca prospectiva existente e D futuro ≥ 6,28 sob forecast publicado, não porque o resultado esperado seja favorável. A tensão corrente contra a previsão está declarada no core e a tabela `CANAIS_K01.json` conserva todos os canais desfavoráveis. [um_absoluto](kimi-cite://text?path=C%3A%5CIALD%5CArtigo%5CHaja_Luz%5CA%20Ponte%20e%20o%20Um%5CN%C3%B3s%5Cum_absoluto.json&text=%22m2_pred_meV%22%3A%208.507414099900329 "citation")

[DERIVED] O segundo candidato de cegueira, ringdown D, não foi escolhido porque seu planejamento mais recente dá D10 = 3,9346 no melhor caso e D14 = 4,6374 sem sistemática, abaixo de 5 e de D90. [PODER_RAMO_B_ANTES_DE_ABRIR](kimi-cite://text?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Cconjunto_D_20261029%5Cparametrizacao_03nov%5CPODER_RAMO_B_ANTES_DE_ABRIR.json&text=%22poder%22%3A%203.9346337577944936 "citation")

[DECLARADO] Não se abre um segundo pré-registro para ringdown nesta entrega. O V1 e o congelamento de 03/11/2026 já existem; esta K01 não os substitui nem recomenda abrir D sem poder e sem a palavra do operador.

## 2. Hipótese, escala e objeto de morte

[DERIVED] A forma condicional é

\[
m_2=\sqrt{\Delta m^2_{21}}=\beta\,\sen(45^\circ)\,E_0,
\qquad \beta=\alpha_{\rm CODATA\ 2018}\sqrt e,
\qquad E_0=1\ {\rm eV}.
\]

[REAL] O valor lido no core é m₂ = 8,507414099900329 meV. [um_absoluto](kimi-cite://text?path=C%3A%5CIALD%5CArtigo%5CHaja_Luz%5CA%20Ponte%20e%20o%20Um%5CN%C3%B3s%5Cum_absoluto.json&text=%22predicao%22%3A%20%22m_2%20%3D%20beta_TGL*sin(45)*1eV "citation")

[INPUT] E0 = 1 eV é declarado, não derivado; m₁ ≈ 0 e o ordenamento normal fazem parte do pacote de identificação. [DERIVED] O sen45 tem suporte formal condicional à identificação ONTO registrada, mas isso não deriva E0 nem transforma a identificação física em teorema independente.

[DECLARADO] O objeto de `FALSIFIED` é o pacote `m₂ = β·sen45°·E0` com E0 = 1 eV e m₁ ≈ 0, testado no setor de oscilação. Um negativo atinge a escala/identificação; não falsifica β isoladamente, não falsifica toda a TGL e não move o gate.

## 3. Dados permitidos e tranca de cegueira

[DECLARADO] **Primário P:** a próxima determinação autônoma `JUNO-only` de Δm²₂₁, com centro, σ total, versão de análise, covariância/nuisances e data pública identificados. O resultado não pode ser uma combinação que já contenha KamLAND, solar ou outro ajuste global usado como segunda testemunha.

[DECLARADO] **Secundário S:** uma determinação independente de P, com JUNO explicitamente excluído, centro, σ total, versão e covariância/sistemática públicos. A equipe, a versão e o conjunto exato de dados de S precisam ser fixados pelo operador antes da abertura de P; se isso não ocorrer, `S = AWAITING_SOURCE` e a regra de duas determinações não pode disparar.

[REAL] Um ajuste global que contenha JUNO não é independente de P. NuFIT/Capozzi ou outro ajuste só entram em S se a exclusão de JUNO estiver explícita; a escolha entre equipes não pode ser feita pelo centro, pelo erro ou pelo sinal obtido depois da leitura.

[REAL] O frozen anterior declara que sua emissão inicial não foi cega, pois a tensão corrente já era conhecida, e que a cegueira vale prospectivamente a partir de 08/08/2026. [DECLARADO] Essa contaminação histórica permanece escrita; ela não é apagada por este rascunho.

[DECLARADO] Um terceiro custodiante deve receber P e S sem os comunicar à casa. A abertura ocorre uma única vez, depois da conferência dos hashes e dos controles. Nenhuma análise preliminar de P/S pode orientar cortes, fonte, pesos, limiar ou ramos.

## 4. Poder de desenho, sem usar um resultado futuro

[DERIVED] Defina `r = σ(Δm²₂₁)/Δm²₂₁`. Para o planning público já conhecido, usado somente como ponto fiducial e não como evidência nova,

\[
D(r)=\frac{2\,[1-m_{2,\rm pred}/m_{2,\rm planning}]}{r},
\qquad m_{2,\rm planning}=8,677557259966656\ {\rm meV}.
\]

[DERIVED] Os números calculados por `K01_validar.py desenho` são:

- [DERIVED] linha de 5σ: `r ≤ 0,007842905784 = 0,7842905784 %`;
- [DERIVED] portão de 90 %, D90 = 5 + z0,90 = 6,2815515655: `r ≤ 0,006242809362 = 0,6242809362 %`;
- [DERIVED] forecast conservador `r = 0,005 = 0,5 %`: `D = 7,842905784`;
- [DERIVED] tabela de sensibilidade `r = 0,003 = 0,3 %`: `D = 13,071509640`.

[DERIVED] O planning direto JUNO-only, que é o primário do protocolo e não deve ser substituído pelo planning global mais favorável, dá: linha de 5σ `r ≤ 0,007059374345 = 0,7059374345 %`; D90 `r ≤ 0,005619132687 = 0,5619132687 %`; `D = 7,059374345` com 0,5 % e `D = 11,765623909` com 0,3 %. Os dois plannings permanecem visíveis, e a seleção não usa o maior D como justificativa.

[KNOWN, a conferir] O estudo de sensibilidade do JUNO publica precisão melhor que 0,5 % em seis anos para os parâmetros de oscilação, e a tabela pública associada dá 0,3 % para Δm²₂₁; são forecasts com o modelo de sistemáticas do projeto, não garantia de realização nem de independência. [JUNO Collaboration](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2204.13249&text=will%20be%20determined%20to%20better%20than%200.5%25%20precision%20in%20six%20years%20of%20data%20collection "citation"), [JUNO/ICHEP](kimi-cite://web?url=https%3A%2F%2Findico.cern.ch%2Fevent%2F1291157%2Fcontributions%2F5888133%2Fattachments%2F2899170%2F5083623%2Fjuno_ichep2024_calvez.pdf "citation")

[REAL] A coleta física começou em 26/08/2025. [JINR](kimi-cite://web?url=https%3A%2F%2Fwww.jinr.ru%2Fposts%2Fjuno-experiment-begins-taking-data%2F&text=On%2026%20August%202025%2C%20a%20physics%20experiment%20started "citation")

[DERIVED] Seis anos nominais após essa data terminam em **26/08/2031**. [DECLARADO] Essa é a data de exposição de referência, não uma data prometida de publicação nem uma autorização para esperar por um centro favorável. A data pública de liberação permanece [OPEN].

[DECLARADO] O cálculo de D deve ser refeito documentalmente antes da abertura somente com σ publicado e covariância declarada. Se a precisão não incluir sistema de referência, covariância com θ₁₂, fluxo de reator, não-linearidade e fundos, o estado é `AWAITING_SOURCE`, não uma precisão presumida.

## 5. Pesos e contabilidade de independência

[DECLARADO] **Sem média inversa-da-variância para matar.** P e S recebem peso lógico 1 cada e são avaliados separadamente; combinar os dois por 1/σ² poderia diluir uma discordância e está proibido para o ramo `FALSIFIED`.

[DECLARADO] A regra de independência é binária e fail-closed: `independente(P,S) = true` somente se S excluir todos os dados de P e houver declaração de sistemáticas compartilhadas/covariância. Se a independência for apenas alegada pelo nome do ajuste, vale `false`.

[DECLARADO] Ajustes adicionais, inclusive KamLAND+solar, NuFIT ou Capozzi, aparecem sempre como linhas de estresse, nunca como um menu do qual se escolhe a determinação mais conveniente. Não se contam duas vezes JUNO, um global com JUNO e outro global com os mesmos dados.

[DECLARADO] Para `MATCHED_PROSPECTIVELY`, mantém-se a regra frozen: duas determinações independentes precisam cair a 1σ de m₂_pred. Mesmo nesse caso, o ramo não significa `CONFIRMED`.

## 6. Função de veredito proposta

[DECLARADO] A primeira condição satisfeita decide; nenhuma regra posterior pode ser usada para salvar um ramo anterior. `r_P` e `r_S` são `|m₂_obs−m₂_pred|/σ_obs` de cada determinação, calculados somente na abertura autorizada, nunca nesta K01.

0. [DECLARADO] `AWAITING_SOURCE` — falta P ou S elegível, versão, centro, σ total, covariância, hash, data ou definição de independência; ou o relógio externo não é anterior ao dado.
1. [DECLARADO] `INCONCLUSIVE_SYSTEMATICS` — falha de integridade, covariância ou controle; P e S compartilham dados sem correção; primary e stress discordam de modo não resolvido; ou a versão mudou depois da tranca.
2. [DECLARADO] `TGL_NU_M2_FALSIFIED` — `independente(P,S) = true` e `r_P ≥ 5` e `r_S ≥ 5`. Não há média, compensação nem escolha do sinal.
3. [DECLARADO] `TGL_NU_M2_TENSION` — não ocorre o ramo 2 e pelo menos uma determinação elegível tem `r ≥ 3`. O sufixo obrigatório é `SINGLE_OR_GLOBAL_NOT_INDEPENDENT` quando uma determinação tem `r ≥ 5` mas a outra não satisfaz independência ou `r ≥ 5`.
4. [DECLARADO] `TGL_NU_M2_MATCHED_PROSPECTIVELY` — não ocorrem os ramos 2–3 e as duas determinações independentes estão a 1σ de m₂_pred.
5. [DECLARADO] `TGL_NU_M2_NOT_FALSIFIED_UNDERPOWERED` — não ocorrem os ramos 2–4 e o D de desenho da determinação disponível é `< 5`; o sufixo registra `POWER_<D>_OF_5_SIGMA`.
6. [DECLARADO] `TGL_NU_M2_ARMED_CONSISTENT` — demais casos elegíveis; é um estado de não decisão, nunca uma confirmação.

[OPEN] O frozen atual explicita `TENSION` em [3,5) e `FALSIFIED` com duas determinações ≥5, mas não diz com clareza o ramo de uma única determinação ≥5 sem a segunda. O ramo 3 acima fecha essa lacuna por proposta, sem criar `FALSIFIED`; precisa de ratificação antes de uso. Se o operador não ratificar uma redação para esse caso, o estado deve ser `OPEN_RULE_GAP`, não `ARMED_CONSISTENT` e nunca `FALSIFIED` por uma só determinação.

[DECLARADO] O ramo de poder não pode vetar o ramo 2: um D subestimado não impede uma falsificação observada sob a regra. Por outro lado, D ≥ 5 no desenho não autoriza antecipar qualquer resultado.

## 7. Significado de cada ramo

- [DECLARADO] `FALSIFIED`: o pacote E0 = 1 eV × sen45° × identificação m₁≈0 é rejeitado pelo desenho; β sozinho, a TGL inteira e o gate não são rejeitados por esse token.
- [DECLARADO] `TENSION`: há pressão contra a escala/pacote, mas a condição dupla de morte não foi cumprida; uma única determinação ≥5 permanece tensão e/ou parede de independência.
- [DECLARADO] `MATCHED_PROSPECTIVELY`: há concordância prospectiva dentro de 1σ nas duas linhas; não é `CONFIRMED`, creditação nem fechamento de outros setores.
- [DECLARADO] `NOT_FALSIFIED_UNDERPOWERED`: a natureza não foi alcançada com poder suficiente; é parede medida de desenho, não evidência a favor.
- [DECLARADO] `INCONCLUSIVE_SYSTEMATICS`: o instrumento, a covariância ou a independência falhou; não é veredito sobre a lei.
- [DECLARADO] `AWAITING_SOURCE`/`OPEN_RULE_GAP`: o protocolo não está completo; nenhuma inferência física é permitida.

[DECLARADO] Em todos os ramos: `NOT_FALSIFIED ≠ CONFIRMED`; o gate permanece imóvel; retrodição sem ajuste continua evidência legítima, mas não é rotulada como teste cego; o termo de linguagem pública, quando cabível, é «descoberta autoevidente em dados públicos, carente de creditação acadêmica», nunca autocrédito da máquina.

## 8. Guarda contra emenda posterior

1. [DECLARADO] Antes de qualquer nova leitura, gerência publica um manifesto com timestamp externo e sha256 deste rascunho ratificado, do `CANAIS_K01.json`, do frozen de origem, da função de veredito, das fontes P/S e do código de execução.
2. [DECLARADO] Qualquer mudança de fórmula, E0, ordenamento, P/S, pesos, independência, limiar, ramo, código ou hash invalida a abertura e devolve `AWAITING_SOURCE`.
3. [DECLARADO] Uma versão nova só pode ser escrita antes de um dado/estimador realmente novo e deve apresentar toda a tabela de tentativas; nenhuma emenda posterior a centro, σ, D ou resultado pode trocar TENSION por FALSIFIED ou UNDERPOWERED por POWERED.
4. [DECLARADO] A abertura é única e vinculada ao manifesto. Repetição técnica só é permitida por falha documentada que não envolva ler centro ou significância; depois de lido qualquer resultado, não há reabertura para “melhorar” o desenho.
5. [DECLARADO] Testes sintéticos futuros devem incluir ambos os lados de m₂_pred, duas determinações discordantes, uma única ≥5, covariância quebrada e fonte com JUNO incluído indevidamente. Eles validam a função, não a física; nenhum teste foi executado aqui.
6. [DECLARADO] O calendário não pode ser movido para aguardar uma precisão ou um centro conveniente. Toda liberação elegível e toda tentativa entram num registro append-only, inclusive as que forem contra a previsão.
7. [DECLARADO] A revisão científica e a aprovação são de pessoas diferentes do redator; a palavra final de abertura é ato separado do operador.

## 9. As sete ressalvas, uma a uma

| Ressalva V411 | Tratamento proposto e limite remanescente |
|---|---|
| R1 — emenda pós-guarda/não cegueira | [DECLARADO] **PARCIAL.** Há tranca prospectiva desde 08/08/2026, mas a regra inicial foi escrita com tensão conhecida. Este rascunho só vale depois de ratificação e timestamp anteriores ao novo dado; a história não é reescrita. |
| R2 — primário previsível por agregados | [DECLARADO] **RESPOSTA FUTURA.** P deve ser uma determinação JUNO nova, custodiada por terceiro; o planning atual é apenas fiducial e não entra como evidência. Reabrir os agregados atuais continua proibido como “teste cego”. |
| R3 — Cefeidas livres/linha de estresse | [DECLARADO] **SUBSTITUIÇÃO EXPLÍCITA.** P = JUNO-only e S = global-sem-JUNO ficam sempre lado a lado; KamLAND+solar e demais ajustes são estresse, nunca escondidos nem usados como menu. |
| R4 — poder só de desenho | [DECLARADO] **PARCIAL.** D usa forecast publicado e é apresentado com 0,5 % e 0,3 %; sistemáticas, covariância, realização e segunda determinação ficam abertas. Não se afirma 5σ de resultado. |
| R5 — 72 direções de variância zero/covariância | [DECLARADO] **NÃO SE APLICA LITERALMENTE, MAS SEGUE ABERTA.** Exige-se covariância de oscilação, nuisances e sistemáticas compartilhadas; precisão sem modelo completo devolve `AWAITING_SOURCE`. |
| R6 — escolhas com tabela de poder à vista | [DECLARADO] **PARCIAL.** O canal foi selecionado por tranca e D, com todos os 20 canais publicados nesta entrega, inclusive os contrários. A escolha de S e o fechamento da lacuna ≥5 ficam para o operador antes de qualquer centro novo. |
| R7 — tentativas/sobreposição | [DECLARADO] **PARCIAL.** P e S só contam se independentes; globals com JUNO são excluídos da segunda testemunha. Todas as tentativas e versões entram no look-elsewhere e no registro append-only. |

[DERIVED] Consequência honesta: o desenho responde melhor a R2–R5 do que a R1, R6 e R7; não “resolve as sete ressalvas” por decreto. A independência da segunda determinação e a lacuna de veredito são os dois bloqueios principais.

## 10. Decisões necessárias antes de transformar o rascunho em protocolo

- [DECLARADO] **Operador:** manter ou alterar a exigência de duas determinações independentes ≥5; recomenda-se manter. Se mantiver, nomear S com JUNO excluído e ratificar o ramo `TENSION` para uma única ≥5 ou o estado `OPEN_RULE_GAP`.
- [DECLARADO] **Operador:** ratificar que o negativo atinge E0/identificação e não β isoladamente nem a TGL inteira, preservando o gate imóvel.
- [DECLARADO] **Gerência:** conferir as fontes, os hashes, o cálculo de D, a lista completa de tentativas e a versão final da função; preparar custódia e revisão independente, sem executar P/S.
- [DECLARADO] **Operador, em ato futuro separado:** autorizar ou recusar a abertura depois de o estágio cego documentar poder e independência. Este arquivo não é essa autorização.

[OPEN] As perguntas operacionais estão separadas em `PERGUNTA_K01.md`. O restante do levantamento foi concluído sem depender dessas respostas.
