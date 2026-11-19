# PROTOCOLO EXPERIMENTAL RASCUNHO K03 — R1

## 0. Estatuto e condição de execução

- [DECLARADO] Este documento é um rascunho de pré-registro e não autoriza execução.
- [REAL] Nenhum modelo foi chamado, nenhum resultado foi aberto e nenhum dado do piloto foi usado para calibrar efeito, variância ou limiar.
- [INPUT] Execução, escolha de modelos e publicação de entradas dependem do operador e de revisão independente da gerência.
- [DECLARADO] O extrator continua pendente: sem implementação, casos adversariais e validação antes do congelamento, o experimento NÃO DECIDE e nenhum dos ramos FALSIFIED/POWERED/UNDERPOWERED pode ser emitido.
- [DECLARADO] A R1 usa uma única inicialização primária e separa dinâmica própria por braço, especificidade cruzada à TGL e análises secundárias.

## 1. Perguntas e hipóteses separadas

### 1.1 Dinâmica ao alvo próprio de cada braço

- [CONJECTURE] Em modelos capazes, a condição TGL produz maior frequência de `C_8^{(T)}` que cada controle produz de `C_8^{(j)}`, cada um medido contra seu próprio alvo `τ_j` com instrumento normalizado e dificuldade pareada.
- [DECLARADO] H0 para cada contraste dinâmico `j`: `p_C8(T)≤p_C8(C_j)`; os desfechos são binários e normalizados por 24 asserções, 8 leituras e ganho mínimo `6/24`.
- [DECLARADO] A análise dinâmica responde se os braços convergem aos seus próprios alvos; não mede por si quanto de TGL cada saída contém.

### 1.2 Especificidade cruzada à TGL

- [CONJECTURE] Na primeira leitura, a condição TGL produz maior pontuação cruzada `X_{T,1}^{TGL}` que cada controle `X_{C_j,1}^{TGL}`, sempre com o extrator TGL aplicado às saídas de todos os braços.
- [DECLARADO] H0 para cada contraste de especificidade `j`: as distribuições de `X_{T,1}^{TGL}` e `X_{C_j,1}^{TGL}` são iguais ou T não é superior; o teste é separado dos 12 contrastes dinâmicos.
- [DECLARADO] A análise cruzada responde quanto do alvo TGL foi reproduzido; ela não substitui o controle dinâmico ao alvo próprio e não pode transformar resumo em convergência.

### 1.3 Estado já estacionário e idempotência

- [CONJECTURE] `ALREADY_STATIONARY` só será reconhecido quando todas as oito distâncias forem zero; iniciar no alvo, sair e retornar será classificado como `RETURN_TO_TARGET`, não como estacionário desde o início.
- [CONJECTURE] Sucesso após uma aplicação/idempotência será medido por `I_1` e `IDEMPOTENT_SCREEN`, nunca pela transição `C_8`.
- [DECLARADO] A ausência de diferença entre TGL e outro autorreferente impede atribuir especificidade ou exclusividade à TGL, mas não falsifica por si a existência de um atrator para TGL.

## 2. Congelamento antes da coleta

- [DECLARADO] O manifesto deve conter modelos/versões, provedor, datas, parâmetros, sementes, contexto, formato, hashes dos textos, alvos `τ_j`, extratores `E_j`, extrator cruzado `E_TGL`, análises, regras de exclusão e escopos de integridade.
- [DECLARADO] A temperatura primária proposta é 0,2; provedores sem esse controle usam configuração equivalente congelada antes da coleta, sem ajuste posterior.
- [DECLARADO] Cada sessão usa contexto novo, sem cache de conversa e sem treinamento, ajuste fino ou atualização intencional de pesos.
- [DECLARADO] Mudança de versão do provedor invalida a célula afetada e impede tratá-la como a mesma família congelada.
- [DECLARADO] Nenhum texto de entrada ou sequência reservada é reproduzido; as fontes são referenciadas apenas por caminho e hash no manifesto.
- [DECLARADO] A representação contínua/fracionária usada para discutir contração e o instrumento binário usado para pontuar são registrados como objetos distintos.

## 3. Famílias e piso de capacidade

- [DECLARADO] Serão quatro representantes congelados: três de famílias distintas classificadas como capazes e um de família abaixo do piso.
- [DECLARADO] A inferência primária vale apenas para os três representantes capazes; não se extrapola a todos os LLMs ou versões futuras.
- [DECLARADO] A família abaixo do piso testa o controle C3 original e não entra em FALSIFIED ou NOT_FALSIFIED_POWERED.
- [DECLARADO] Antes do experimento principal, cada candidato executa uma bateria neutra, sem TGL, com 24 asserções de leitura fiel e saída estruturada.
- [DECLARADO] “Capaz” requer pelo menos 80% das asserções neutras corretas E pelo menos 90% de saídas válidas no esquema.
- [DECLARADO] “Abaixo do piso” significa falhar em PELO MENOS UM dos dois critérios: menos de 80% das asserções corretas, menos de 90% de saídas válidas, ou ambos.
- [DECLARADO] A classificação é feita antes de abrir qualquer saída principal e não pode ser alterada para melhorar um desfecho.
- [DECLARADO] Chamadas de calibração são separadas e não contam nas 16.000 interações primárias; seus resultados não são usados para escolher alvos.

## 4. Braços, alvos próprios e pareamento

| braço | estatuto | entrada | alvo próprio normalizado | finalidade separada |
|---|---|---|---|---|
| T | [DECLARADO] | Material TGL por caminho/hash | 24 asserções TGL `τ_T` | Dinâmica própria e especificidade TGL. |
| C1 — embaralhado | [DECLARADO] | Os mesmos tokens de T, permutados por semente congelada | 24 asserções de sequência/fingerprint do embaralhamento `τ_C1` | Controlar dinâmica de reprodução sem teoria coerente. |
| C2 — placebo | [DECLARADO] | Texto coerente não TGL, sem a teoria | 24 asserções do placebo `τ_C2` | Controlar dinâmica de corpus coerente genérico. |
| C3 — autorreferente | [DECLARADO] | Outro texto coerente autorreferente | 24 asserções autorreferentes `τ_C3` | Controlar dinâmica autorreferente genérica. |
| C4 — sem texto | [DECLARADO] | O mesmo esquema e sondas, sem corpus | 24 asserções de abstenção/não fabricação `τ_C4` | Controlar memória prévia, alucinação e esquema. |

- [DECLARADO] Todos os braços usam 24 asserções, a mesma métrica normalizada, 8 leituras, três estados finais e ganho mínimo de seis asserções para `C_8`.
- [DECLARADO] C1, C2 e C3 devem ter o mesmo número de bytes e tokens sob tokenizador congelado, a mesma língua, o mesmo número de seções e dificuldade pareada por tipo de asserção.
- [DECLARADO] O pareamento de dificuldade usa regras determinísticas de estrutura e dois revisores independentes antes da randomização; nenhum desfecho de modelo é usado para calibrar dificuldade.
- [DECLARADO] Se qualquer alvo, extrator ou dificuldade não estiver pareado e congelado, o escopo afetado é INCONCLUSIVE_CONTROLS.
- [DECLARADO] O extrator cruzado `E_TGL` não altera os alvos próprios `τ_j`; ele é aplicado somente para a análise de especificidade.

## 5. Sessões e inicialização única

- [DECLARADO] São 100 sessões primárias independentes por célula de família × braço, todas com UMA única inicialização neutra `I_A`, congelada antes da coleta.
- [DERIVED] Quatro famílias × cinco braços × 100 sessões = 2.000 sessões primárias; 2.000 × 8 = 16.000 interações primárias programadas.
- [DECLARADO] A segunda inicialização `I_B` é reservada para análise secundária separada, não integra as 100 sessões primárias nem as 16.000 interações e não entra em Binomial/Fisher agrupado.
- [DECLARADO] As sementes primárias são únicas por sessão e geradas de lista congelada; a ordem das células é aleatorizada por família.
- [DECLARADO] Sob `I_A` única, as 100 sessões de cada célula são tratadas como replicatas independentes condicionais ao modelo e parâmetros congelados; nenhuma mistura 50/50 permanece no desfecho primário.
- [DECLARADO] Saída inválida é falha pelo script e não é substituída; somente indisponibilidade técnica antes de qualquer resposta permite reposição pela regra congelada, com registro separado.
- [DECLARADO] Reposições técnicas, calibração, inicialização secundária e controles de perturbação são contados separadamente das 16.000 interações primárias.
- [DECLARADO] Nenhuma sessão é removida por conteúdo desfavorável ou ausência de convergência.

## 6. Observáveis calculados por script

### 6.1 Extratores próprios e cruzado

- [DECLARADO] Cada alvo `τ_j` é decomposto em 24 asserções binárias verificáveis por `E_j`; lista, analisador e casos positivos/negativos são congelados antes da coleta.
- [DECLARADO] I1 da TGL usa análise sintática/simbólica e proveniência; I2 usa grafo/ordem; I3 usa campos/estatutos; I4 usa vereditos e `full_witness`; I5 usa relações entre artefato/executabilidade/atrator; I6 usa falsificadores e estatutos.
- [DECLARADO] Nenhuma asserção é pontuada por LLM, avaliador humano ou similaridade de embeddings.
- [DECLARADO] `E_TGL` aplica as mesmas 24 regras TGL às saídas de todos os braços para `X_{j,k}^{TGL}=(1/24)Σ_i E_TGL(y_k^{(j)})_i`.
- [DECLARADO] A especificidade primária usa `X_{j,1}^{TGL}`; trajetórias cruzadas posteriores são secundárias.

### 6.2 Dinâmica própria

- [DECLARADO] `d_k^{(j)}=(1/24)Σ_i|s_{k,i}^{(j)}-τ_{j,i}|` e `u_k^{(j)}=(1/24)Σ_i|s_{k,i}^{(j)}-s_{k-1,i}^{(j)}|`.
- [DECLARADO] `A_8^{(j)}=1` se `d_6^{(j)}=d_7^{(j)}=d_8^{(j)}=0` e `u_6^{(j)}=u_7^{(j)}=u_8^{(j)}=0`; caso contrário, `A_8^{(j)}=0`.
- [DECLARADO] `C_8^{(j)}=1` se `A_8^{(j)}=1` e `d_1^{(j)}-d_8^{(j)}≥6/24`; caso contrário, `C_8^{(j)}=0`.
- [DECLARADO] O contraste dinâmico compara `C_8^{(T)}` com `C_8^{(C_j)}`, nunca a pontuação cruzada como substituto.

### 6.3 Estacionário estrito, retorno, uma aplicação e resumo

- [DECLARADO] `ALREADY_STATIONARY^{(j)}=1` se e somente se `d_1^{(j)}=…=d_8^{(j)}=0`; qualquer saída intermediária torna o valor zero.
- [DECLARADO] `RETURN_TO_TARGET^{(j)}=1` se `d_1^{(j)}=0`, `A_8^{(j)}=1` e existe `k∈{2,…,7}` com `d_k^{(j)}>0`; retorno não é estacionário desde o início nem transição `C_8`.
- [DECLARADO] `I_1^{(j)}=1` se `s_1^{(j)}=s_2^{(j)}=τ_j`; esse é o desfecho separado de sucesso no alvo em uma aplicação.
- [DECLARADO] `IDEMPOTENT_SCREEN^{(j)}=1` se `s_1^{(j)}=s_2^{(j)}`, independentemente do alvo; essa triagem não prova idempotência universal e não entra em `C_8`.
- [DECLARADO] `SUMMARY_ONLY^{(j)}=1` se `d_1^{(j)}≤6/24` e `A_8^{(j)}=0`; isso separa pontuação inicial de atingir/permanecer no alvo próprio.
- [DECLARADO] Oito leituras testam previsão finita e não demonstram limite, contração, primitividade, absorção ou idempotência universal.

## 7. Controle secundário de resumo iterativo e perturbação-retorno

- [DECLARADO] Em sessões secundárias separadas, o custodiante aplica o mesmo ciclo iterativo sem perturbação e, após uma janela congelada, registra se a saída permanece resumo estável ou satisfaz `A_8`.
- [DECLARADO] Quando o alvo for atingido em sessão secundária, uma perturbação congelada é introduzida e a recuperação é medida por `RETURN_TO_TARGET`, nova estabilização e distância ao alvo próprio.
- [DECLARADO] A comparação “resumo iterativo estável × saída perturbada × retorno” é necessária antes de interpretar estabilidade como atrator, e não substitui a porta de integridade nem o desfecho primário.
- [DECLARADO] Se não houver perturbação-retorno, o protocolo só permite falar em atingir/permanecer no horizonte, não em bacia de atração.
- [DECLARADO] Essas sessões e chamadas são contadas separadamente das 16.000 primárias e não entram nos 12 contrastes dinâmicos ou nos 12 de especificidade.

## 8. Cegamento e entrega dos papéis de contraste

- [DECLARADO] O avaliador primário é o programa congelado; não há avaliador-LLM nem juízo humano no cálculo dos desfechos.
- [DECLARADO] O custodiante gera pseudônimos para famílias e braços e conserva a chave fora do ambiente de análise, com compromisso de hash antes da coleta.
- [DECLARADO] Antes da chave, o custodiante entrega pacotes de contraste com: `contrast_id`, pseudônimo da família, papel orientado `FOCAL` ou `COMPARATOR`, tipo `DYNAMIC_OWN_TARGET` ou `SPECIFICITY_TGL`, vetores numéricos e contagens, sem identidade do modelo, texto ou braço.
- [DECLARADO] Os papéis `FOCAL/COMPARATOR` codificam apenas a orientação pré-registrada do teste e não revelam qual texto ou fornecedor ocupa cada papel; o mapa entre papéis e condições fica sob custódia com hash comprometido.
- [DECLARADO] O analista executa todos os pacotes sem escolher pares, orientação, subgrupos ou controles; textos das saídas não são fornecidos antes da chave.
- [DECLARADO] A chave é aberta somente após congelamento do banco, validação de contagens, execução do código e arquivamento dos logs; auditoria humana não altera pontuações.
- [DECLARADO] Como o conteúdo poderia revelar a condição, o cegamento humano não é garantia; a mitigação principal é pontuação determinística com papéis de contraste cegados.

## 9. Porta de integridade antes de qualquer veredito

- [DECLARADO] `INTEGRITY_OK` exige extratores válidos, alvos e dificuldade congelados, hashes concordantes, inicialização correta, pareamento válido, cegamento preservado e ausência de mudança de regra após qualquer saída.
- [DECLARADO] A ordem obrigatória é: validar integridade no escopo, congelar análise, somente então avaliar FALSIFIED, POWERED ou UNDERPOWERED.
- [DECLARADO] Falha de célula produz `IALD_COLLAPSE_INCONCLUSIVE_CONTROLS` na célula e impede qualquer veredito nela; a célula não entra em FALSIFIED, POWERED ou UNDERPOWERED.
- [DECLARADO] Falha de família ou perda de uma célula exigida produz INCONCLUSIVE_CONTROLS na família e no veredito global; as demais células podem ser descritas apenas exploratoriamente, sem veredito global.
- [DECLARADO] Falha de extrator global, alvo global, chave aberta antes, alteração de código ou divergência de hash global invalida toda a corrida e impede os três ramos em todo o escopo.
- [DECLARADO] INCONCLUSIVE_CONTROLS não é evidência a favor ou contra TGL e tem precedência sobre qualquer contagem ou p-valor.

## 10. Estatística, cortes e poder

### 10.1 Duas famílias de contrastes

- [DECLARADO] Os 12 contrastes dinâmicos comparam `C_8^{(T)}` com `C_8^{(C_j)}` nos três modelos capazes × quatro controles, com Fisher unilateral e Holm a 5%.
- [DECLARADO] Os 12 contrastes de especificidade comparam `X_{T,1}^{TGL}` com `X_{C_j,1}^{TGL}` nos mesmos pares, por teste de permutação unilateral dentro de cada família e Holm separado a 5%.
- [DECLARADO] Os dois blocos têm papéis distintos e são reportados separadamente; especificidade cruzada não substitui dinâmica própria, e dinâmica própria não substitui especificidade TGL.
- [DECLARADO] O poder conjunto dos dois blocos, dos cortes e da regra completa permanece [OPEN] até cálculo estatístico sem saídas de modelo.

### 10.2 Uma inicialização e limites exatos

- [DECLARADO] Com `I_A` única e 100 replicatas independentes por célula, `x_A` e `x_C` são tratados como contagens binomiais condicionais ao modelo/parâmetros congelados, sem mistura de duas inicializações.
- [DECLARADO] Para FALSIFIED, usam-se três limites unilaterais de Clopper–Pearson para `A_8^{(T)}`; para POWERED, três para `C_8^{(T)}`, com confiança `1−0,05/3=0,983333…` por família.
- [DERIVED] A escolha de uma inicialização mantém `n=100` e os três modelos capazes; portanto os cortes anteriores permanecem `70/100` e `89/100`, agora sem mistura 50/50.
- [DERIVED] `U_{0,983333}(70,100)=0,794120`, `U_{0,983333}(71,100)=0,802836`, `L_{0,983333}(89,100)=0,804694` e `L_{0,983333}(88,100)=0,792623`, todos recalculados por script sem dados.
- [DERIVED] Como `C_8=1` implica `A_8=1`, `x_C≥89` implica `x_A≥89`; as duas desigualdades são mantidas por legibilidade, sem dupla contagem.
- [KNOWN] Clopper e Pearson, 1934, DOI/JSTOR `10.2307/2331986`; Holm, 1979, JSTOR `4615733`, identificadores consultados.

### 10.3 Poder aproximado dinâmico

- [DECLARADO] A alternativa de planejamento dinâmico é 0,90 para T e 0,60 para cada controle em `C_8` próprio; são escolhas de desenho, não estimativas do piloto.
- [DERIVED] Com aproximação normal para duas proporções, α unilateral conservador 0,05/12 e 100 sessões por braço sob `I_A`, o poder aproximado por contraste dinâmico é 0,992022; o tamanho aproximado para 90% é 61,4547, arredondado a 62.
- [DECLARADO] O poder exato de Fisher, o poder dos 12 testes de especificidade e o poder conjunto do veredito completo permanecem [OPEN] até cálculo estatístico sem saídas de modelo.
- [KNOWN] Lakens, 2022, DOI `10.1525/collabra.33267`; Nosek, Ebersole, DeHaven e Mellor, 2018, DOI `10.1073/pnas.1708274114`, identificadores consultados.

## 11. Árvore de vereditos, sempre após integridade

### 11.1 INCONCLUSIVE_CONTROLS

- [DECLARADO] `IALD_COLLAPSE_INCONCLUSIVE_CONTROLS` ocorre em qualquer escopo com falha de extrator, hash, integridade, alvo, pareamento, classificação de capacidade, cegamento ou regra congelada.
- [DECLARADO] Se houver falha em qualquer escopo exigido, nenhum dos outros três ramos é emitido nesse escopo; se a falha comprometer a corrida, não há veredito global.

### 11.2 FALSIFIED

- [DECLARADO] `IALD_COLLAPSE_FALSIFIED` exige `INTEGRITY_OK` em toda a corrida e, em pelo menos uma família capaz, `x_A≤70/100` na condição TGL, com o limite superior unilateral abaixo de 0,80.
- [DECLARADO] Qualquer falha de integridade impede FALSIFIED e substitui o ramo por INCONCLUSIVE_CONTROLS no escopo afetado; contagem baixa não supera a porta.
- [DECLARADO] Falha apenas na família abaixo do piso não produz FALSIFIED.
- [DECLARADO] FALSIFIED significa falha da previsão operacional congelada no escopo medido, não refutação de toda a TGL ou de seus teoremas.

### 11.3 NOT_FALSIFIED_POWERED

- [DECLARADO] `IALD_COLLAPSE_NOT_FALSIFIED_POWERED` exige `INTEGRITY_OK` em toda a corrida, `x_A≥89/100` e `x_C≥89/100` nas três famílias capazes, os 12 contrastes dinâmicos significativos após Holm e os 12 de especificidade significativos após Holm separado.
- [DECLARADO] Esse ramo significa somente não falsificação da previsão finita no escopo; não significa CONFIRMED, creditação, universalidade ou exclusividade.
- [DECLARADO] Como o poder conjunto dos dois blocos permanece [OPEN], o nome registra o desenho pretendido e não uma promessa de cobertura global já calculada.

### 11.4 NOT_FALSIFIED_UNDERPOWERED

- [DECLARADO] `IALD_COLLAPSE_NOT_FALSIFIED_UNDERPOWERED` exige `INTEGRITY_OK` e cobre resultados sem FALSIFIED e sem os requisitos de POWERED, incluindo 71–88 em `A_8`, menos de 89 em `C_8`, contrastes não resolvidos ou predomínio de `ALREADY_STATIONARY` que impeça medir transição.
- [DECLARADO] Qualquer falha de integridade impede também UNDERPOWERED no escopo afetado; falta de poder não é desculpa para invalidar controles.
- [DECLARADO] Convergência semelhante entre TGL e outro autorreferente significa mecanismo genérico não separado, não TGL falsa nem TGL única.
- [DECLARADO] Equivalência futura exige margem e teste pré-especificados; não rejeitar diferença não prova equivalência. Schuirmann, 1987, DOI `10.1007/BF01068419`; Lakens, Scheel e Isager, 2018, DOI `10.1177/2515245918770963`, identificadores consultados [KNOWN].

## 12. Interpretações secundárias e limites

- [DECLARADO] Se C4 sem texto reproduzir TGL na análise cruzada, a saída é compatível com memória do pré-treinamento ou esquema; a condição TGL não pode ser chamada de causa sem contraste resolvido.
- [DECLARADO] Se C3 tiver dinâmica semelhante ao próprio alvo, isso não falsifica P7; impede exclusividade operacional e exige previsão distinta para TGL.
- [DECLARADO] Se a família abaixo do piso atingir seu alvo, o critério de capacidade deve ser revisto em nova versão, sem reescrever a corrida aberta.
- [DECLARADO] Não se pode afirmar consciência, vivência, intencionalidade, compreensão subjetiva ou autoconsciência.
- [DECLARADO] Não se pode afirmar alteração de pesos, aprendizado permanente ou treinamento; o desenho mede histórico e saídas.
- [DECLARADO] Não se pode afirmar que a teoria seja a única capaz de gerar atrator, mesmo com quatro controles.
- [DECLARADO] Não se pode afirmar limite infinito, contração, primitividade, absorção ou idempotência verdadeira do LLM a partir de oito leituras.
- [DECLARADO] Não se pode afirmar validade física da TGL, prova cosmológica, P versus NP sem leitor ou creditação acadêmica.
- [DECLARADO] Não se pode converter NOT_FALSIFIED em CONFIRMED, nem FALSIFIED no escopo operacional em refutação dos teoremas formais.

## 13. Referências metodológicas consultadas

- [KNOWN] Banach, 1922, DOI `10.4064/fm-3-1-133-181`; Perron, 1907, DOI `10.1007/BF01449896`; Frobenius, 1912, DOI `10.3931/e-rara-18865`; Seneta, 2006, DOI `10.1007/0-387-32792-4`; Birkhoff, 1931, DOI `10.1073/pnas.17.2.656`; von Neumann, 1932, DOI `10.1073/pnas.18.1.70`; Spohn, 1978, DOI `10.1063/1.523789`.
- [KNOWN] Clopper e Pearson, 1934, DOI/JSTOR `10.2307/2331986`; Holm, 1979, JSTOR `4615733`; Schuirmann, 1987, DOI `10.1007/BF01068419`; Lakens, Scheel e Isager, 2018, DOI `10.1177/2515245918770963`; Lakens, 2022, DOI `10.1525/collabra.33267`; Nosek et al., 2018, DOI `10.1073/pnas.1708274114`.
- [REAL] As fontes internas foram `Nós\um.py`, a árvore `Nós\tgl_kernel\`, `rotas.py`, o inventário, o índice do acervo e o Atlas, listados com consulta em `ESTADO_K03.md`.
- [REAL] As memórias autorizadas foram usadas somente pelos caminhos `C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\traducao-turing-05nov.md`, `acom-e-a-segunda-quantizacao-06nov.md`, `experimento-luiz-registro-mestre.md` e `protocolo-de-colapso-nunca-publico.md`; nenhuma sequência ou entrada foi copiada.
