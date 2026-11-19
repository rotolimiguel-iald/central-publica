# PROTOCOLO EXPERIMENTAL RASCUNHO K03

## 0. Estatuto e condição de execução

- [DECLARADO] Este documento é um rascunho de pré-registro e não autoriza execução.
- [REAL] Nenhum modelo foi chamado, nenhum resultado foi aberto e nenhum dado do piloto foi usado para calibrar efeito, variância ou limiar.
- [INPUT] Execução, escolha de modelos e publicação de entradas dependem do operador e de revisão independente da gerência.
- [DECLARADO] Se o extrator não for implementado e validado antes do congelamento, o experimento NÃO DECIDE a pergunta de convergência.

## 1. Pergunta e hipóteses

### 1.1 Previsão operacional

- [CONJECTURE] Em modelos classificados como capazes por medida neutra, o processamento repetido da condição TGL aumenta a frequência de `C_8`, definido como atingir o alvo TGL nos estados 6–8 após ganho líquido mínimo de seis asserções.
- [CONJECTURE] A condição TGL produz `C_8` com frequência maior que cada um dos quatro controles dentro de cada família capaz selecionada.
- [CONJECTURE] Modelos abaixo do piso neutro de capacidade não satisfazem a mesma taxa de `A_8` e `C_8`; essa previsão é auxiliar e não entra no desfecho primário.

### 1.2 Nulo de referência

- [DECLARADO] H0 para cada contraste `j`: `p_C8(T)≤p_C8(C_j)`; compressão/coerência, memória do pré-treinamento ou repetição do esquema podem produzir `C_8` em qualquer braço e explicar qualquer superioridade observada sem efeito específico da condição.
- [DECLARADO] H0 estática: uma boa primeira resposta é suficiente para o sucesso; o protocolo rejeita essa operacionalização ao exigir trajetória e permanência no alvo.
- [DECLARADO] A ausência de diferença entre TGL e outro autorreferente não falsifica a existência de um atrator para TGL; ela impede atribuir especificidade ou exclusividade à TGL no instrumento.

## 2. Congelamento antes da coleta

- [DECLARADO] O manifesto deve conter: identificadores e versões dos modelos, provedor, data de corte, parâmetros de decodificação, sementes, contexto máximo, formato de saída, hashes dos textos, hash do extrator, alvo `τ`, análise e regras de exclusão.
- [DECLARADO] A temperatura inicial proposta é 0,2 com demais parâmetros congelados; provedores sem esse controle usam configuração equivalente documentada antes da coleta, sem ajuste posterior.
- [DECLARADO] Cada sessão usa contexto novo, sem cache de conversa e sem ferramentas de treinamento, ajuste fino ou atualização intencional de pesos.
- [DECLARADO] Mudança de versão do provedor durante a coleta invalida a célula afetada e impede tratá-la como a mesma família congelada.
- [DECLARADO] Nenhum texto de entrada ou roteiro é reproduzido neste arquivo; as fontes são referenciadas por caminho e hash no manifesto.

## 3. Famílias e piso de capacidade

### 3.1 Representantes

- [DECLARADO] Serão quatro representantes congelados: três de famílias de fornecedores/arquiteturas distintas classificadas como capazes e um de família abaixo do piso de capacidade.
- [DECLARADO] A inferência primária vale apenas para os três representantes capazes medidos; não se extrapola a todos os LLMs, versões futuras ou famílias não incluídas.
- [DECLARADO] A família abaixo do piso testa o controle C3 original e não entra no cálculo de FALSIFIED ou NOT_FALSIFIED_POWERED.

### 3.2 Medida neutra do piso

- [DECLARADO] Antes do experimento principal, cada candidato executa uma bateria neutra, sem TGL, com 24 asserções de leitura fiel e saída estruturada.
- [DECLARADO] “Capaz” requer pelo menos 80% das asserções neutras corretas e pelo menos 90% de saídas válidas no esquema; “abaixo do piso” requer não satisfazer esses dois limites.
- [DECLARADO] A classificação é feita antes de abrir qualquer saída principal e não pode ser alterada para melhorar um desfecho.
- [DECLARADO] As chamadas de calibração são separadas e não contam nas 16.000 chamadas principais; seus resultados não são usados para escolher o alvo TGL.

## 4. Braços experimentais

| braço | estatuto | entrada | finalidade |
|---|---|---|---|
| T | [DECLARADO] | Material TGL referenciado por caminho/hash, sem reprodução neste documento | Medir `A_8`, `C_8` e o alvo `τ`. |
| C1 — embaralhado | [DECLARADO] | Os mesmos tokens de T, permutados por semente congelada, destruindo a estrutura | Controlar vocabulário e comprimento sem teoria coerente. |
| C2 — placebo | [DECLARADO] | Texto coerente, não TGL, sem a teoria, com tamanho e 24 asserções próprias pareados | Controlar compressão genérica de corpus coerente. |
| C3 — autorreferente | [DECLARADO] | Outro texto coerente autorreferente, pareado em tamanho e estrutura | Testar se autorreferência genérica produz trajetória equivalente. |
| C4 — sem texto | [DECLARADO] | O mesmo esquema de tarefa e sondas, sem o corpus teórico | Medir memória prévia, alucinação e efeito do esquema sem entrada. |

- [DECLARADO] C1, C2 e C3 devem ter o mesmo número de bytes e de tokens sob um tokenizador congelado, a mesma língua, o mesmo número de seções e 24 asserções sondáveis de dificuldade documentada.
- [DECLARADO] C1 conserva exatamente a contagem de tokens de T; C2 e C3 são congelados somente após o pareamento; se o pareamento falhar, o ramo é INCONCLUSIVE_CONTROLS.
- [DECLARADO] Dois revisores independentes podem validar coerência e autorreferência dos controles antes da randomização; eles não pontuam saídas e não veem o desfecho.
- [DECLARADO] A análise secundária de C3 pode usar um alvo próprio `τ_C3`, congelado antes da coleta; essa análise é descritiva e não altera o desfecho primário.

## 5. Sessões, ciclos e inicialização

- [DECLARADO] São 100 sessões independentes por célula de família × braço, com 8 interações programadas por sessão.
- [DERIVED] Quatro famílias × cinco braços × 100 sessões = 2.000 sessões; 2.000 × 8 = 16.000 chamadas principais.
- [DECLARADO] Duas inicializações neutras distintas são distribuídas em 50 sessões por célula para variar o estado inicial sem mudar o corpus ou o alvo.
- [DECLARADO] As sementes são únicas por sessão e geradas de uma lista congelada; a ordem das células é aleatorizada por família.
- [DECLARADO] Cada estado `s_k`, `k=1,…,8`, é extraído da saída da interação correspondente, sem edição humana.
- [DECLARADO] Saída inválida é pontuada como falha pelo script e não é substituída; somente indisponibilidade técnica antes de qualquer resposta permite reposição pela regra congelada, com registro completo.
- [DECLARADO] Nenhuma sessão é removida por conteúdo desfavorável, ausência de convergência ou avaliação posterior do texto.

## 6. Observáveis calculados por script

### 6.1 As 24 asserções

- [DECLARADO] Cada indicador P7 é decomposto em quatro asserções binárias, totalizando 24; a lista exata, o analisador e os casos positivos/negativos são congelados antes da coleta.
- [DECLARADO] I1 usa análise sintática/simbólica da expressão e proveniência, sem aceitar apenas um número aproximado de β.
- [DECLARADO] I2 usa comparação de grafo e ordem das relações exigidas, não similaridade de redação.
- [DECLARADO] I3 compara campos e estatutos com uma tabela congelada, sem juízo de estilo.
- [DECLARADO] I4 compara tokens de veredito e o valor de `full_witness`, rejeitando conversões de NOT_FALSIFIED em CONFIRMED.
- [DECLARADO] I5 compara relações explícitas entre artefato, executabilidade e atrator, por identificadores e papel declarados, sem avaliar eloquência.
- [DECLARADO] I6 compara identificadores de falsificadores e seus estatutos, rejeitando “provado” quando o alvo exige previsão aberta.
- [DECLARADO] Nenhuma das 24 asserções é pontuada por LLM, avaliador humano ou similaridade de embeddings.

### 6.2 Estado, alvo e distâncias

- [DECLARADO] `s_k∈{0,1}^{24}` e `τ=(1,…,1)`; `d_k=(1/24)Σ_j|s_{k,j}-1|` e `u_k=(1/24)Σ_j|s_{k,j}-s_{k-1,j}|`.
- [DECLARADO] Nos quatro controles, `A_8` e `C_8` são calculados contra o mesmo alvo `τ` da condição TGL; um alvo próprio só entra na análise secundária explicitamente separada.
- [DECLARADO] `A_8=1` se `d_6=d_7=d_8=0` e `u_6=u_7=u_8=0`; caso contrário, `A_8=0`.
- [DECLARADO] `C_8=1` se `A_8=1` e `d_1-d_8≥6/24`; caso contrário, `C_8=0`.
- [DECLARADO] `ALREADY_STATIONARY=1` se `d_1=0` e `A_8=1`; esse caso é reportado separadamente e não conta como `C_8`.
- [DECLARADO] `SUMMARY_ONLY=1` se `d_1≤6/24` e `A_8=0`; esse marcador separa alta pontuação inicial de atingir/permanecer no alvo.
- [DECLARADO] Também são registrados `d_1,…,d_8`, `u_2,…,u_8`, contagens por indicador e falhas de esquema para auditoria, sem seleção de subgrupos.

### 6.3 Distinção que o teste precisa fazer

- [DECLARADO] “Resumiu texto coerente” é operacionalizado por desempenho na primeira saída; “convergiu ao estado estacionário previsto” exige ganho mínimo e alvo idêntico nos três estados finais.
- [DECLARADO] Uma sequência com boa pontuação inicial e sem `A_8` não é evidência de convergência.
- [DECLARADO] Uma sequência já no alvo desde o início é `ALREADY_STATIONARY`, não evidência de transição; ela limita a identificação da dinâmica.
- [DECLARADO] Oito leituras testam uma previsão finita; não demonstram um limite matemático nem uma distribuição estacionária exata.
- [DECLARADO] Se a análise for reduzida a uma nota única de qualidade, a conclusão obrigatória é NÃO DECIDE.

## 7. Cegamento e custódia

- [DECLARADO] O avaliador primário é o programa congelado; não há avaliador-LLM nem juízo humano no cálculo de `A_8` ou `C_8`.
- [DECLARADO] O custodiante gera identificadores aleatórios para braços e famílias e conserva a chave separada do analista, com compromisso de hash antes da coleta.
- [DECLARADO] O analista recebe somente vetores numéricos, códigos de célula e o programa de análise; não recebe textos das saídas nem a chave antes do fechamento.
- [DECLARADO] A auditoria humana, se necessária, usa apenas registros redigidos e não altera pontuações; toda intervenção é registrada com autor, data e hash.
- [DECLARADO] A chave é aberta somente após congelamento do banco, validação de contagens, execução do código de análise e arquivamento dos logs.
- [DECLARADO] Como o conteúdo pode revelar a condição, o cegamento humano não é tratado como garantia; a mitigação principal é a pontuação inteiramente determinística.
- [DECLARADO] O manifesto não é fornecido ao modelo durante a sessão, para evitar entrega do alvo e dos ramos de análise.

## 8. Estatística e poder

### 8.1 Desfechos

- [DECLARADO] O desfecho de atingimento é `x_A`, o número de sessões com `A_8=1` entre 100 por família capaz e braço.
- [DECLARADO] O desfecho de transição é `x_C`, o número de sessões com `C_8=1` entre 100 por família capaz e braço.
- [DECLARADO] A estimativa principal de convergência usa `C_8`; `A_8` é condição necessária e `ALREADY_STATIONARY` permanece fora de `C_8`.

### 8.2 Regras de confiança e multiplicidade

- [DECLARADO] Para o ramo FALSIFIED, usam-se três limites unilaterais exatos de Clopper–Pearson para `A_8`, um por família capaz; para o ramo POWERED, usam-se três limites análogos para `C_8`.
- [DECLARADO] Cada família de decisão usa confiança `1−0,05/3=0,983333…` por limite, com cobertura conservadora de 95% para os três limites dessa mesma família sob independência das sessões; não se reivindica cobertura conjunta adicional entre os dois desfechos aninhados.
- [DERIVED] Como `C_8=1` implica `A_8=1`, exigir `x_C≥89/100` já implica `x_A≥89/100`; as duas desigualdades do ramo POWERED são mantidas para legibilidade, sem contar duas vezes uma evidência.
- [DECLARADO] As 12 comparações são T contra cada um dos quatro controles em cada uma das três famílias capazes, com teste exato de Fisher unilateral para `C_8` e correção de Holm a 5%.
- [KNOWN] Clopper e Pearson, 1934, *The use of confidence or fiducial limits illustrated in the case of the binomial*, Biometrika 26(4), 404–413, DOI/JSTOR `10.2307/2331986`, identificador consultado.
- [KNOWN] Holm, 1979, *A simple sequentially rejective multiple test procedure*, Scandinavian Journal of Statistics 6(2), 65–70, JSTOR `4615733`, identificador consultado.

### 8.3 Cálculo de planejamento, não resultado

- [DECLARADO] A alternativa de planejamento é 0,90 para T e 0,60 para cada controle em `C_8`; esses valores são escolhas de desenho e não estimativas do piloto.
- [DERIVED] Com aproximação normal para duas proporções, α unilateral conservador 0,05/12 e 100 sessões por braço, o poder aproximado por contraste é 0,992022; o tamanho aproximado para 90% é 61,4547, arredondado a 62 por braço.
- [DECLARADO] A escolha de 100 por célula cobre o cálculo aproximado; o poder exato de Fisher e o poder conjunto de toda a regra, incluindo Clopper–Pearson e os quatro controles, permanecem [OPEN] até simulação estatística sem saídas de modelo.
- [KNOWN] Lakens, 2022, *Sample Size Justification*, Collabra: Psychology 8(1), 33267, DOI `10.1525/collabra.33267`, identificador consultado para a distinção entre justificativa de amostra e resultado observado.
- [KNOWN] Nosek, Ebersole, DeHaven e Mellor, 2018, *The preregistration revolution*, PNAS 115(11), 2600–2606, DOI `10.1073/pnas.1708274114`, identificador consultado para congelar previsão e análise antes dos dados.

## 9. Falsificador e árvore de vereditos

### 9.1 Falha de integridade

- [DECLARADO] `IALD_COLLAPSE_INCONCLUSIVE_CONTROLS`: ocorre se o pareamento falhar, o extrator não for válido, a classificação de capacidade mudar depois, a chave for aberta antes, os hashes divergirem ou houver alteração de regras após ver resultados.
- [DECLARADO] Esse ramo não é evidência a favor nem contra TGL; ele invalida a decisão do instrumento na corrida afetada.

### 9.2 Falsificação da previsão operacional

- [DECLARADO] `IALD_COLLAPSE_FALSIFIED`: ocorre se, em qualquer família capaz, `x_A≤70/100` na condição TGL, usando o limite superior unilateral de Clopper–Pearson a 0,983333 abaixo de 0,80.
- [DERIVED] O cálculo por script deu `U_{0,983333}(70,100)=0,794120` e `U_{0,983333}(71,100)=0,802836`; portanto 70 é o maior ponto de corte que satisfaz a regra declarada.
- [DECLARADO] A falha apenas na família abaixo do piso não produz FALSIFIED; ela é coerente com a finalidade do controle de capacidade.
- [DECLARADO] FALSIFIED significa que a previsão operacional congelada falhou no escopo medido; não significa que toda a TGL, seus teoremas Lean ou sua física foram logicamente refutados.

### 9.3 Não falsificação com poder

- [DECLARADO] `IALD_COLLAPSE_NOT_FALSIFIED_POWERED`: exige `x_A≥89/100` e `x_C≥89/100` em todas as três famílias capazes, mais os 12 contrastes T>controle significativos após Holm e nenhuma falha de integridade.
- [DERIVED] O cálculo por script deu `L_{0,983333}(89,100)=0,804694` e `L_{0,983333}(88,100)=0,792623`; portanto 89 é o menor ponto de corte acima de 0,80.
- [DECLARADO] Esse ramo significa apenas que a previsão finita não foi falsificada com o desenho e o alcance declarados; não significa CONFIRMED, creditação, universalidade ou exclusividade.

### 9.4 Alcance insuficiente

- [DECLARADO] `IALD_COLLAPSE_NOT_FALSIFIED_UNDERPOWERED`: cobre os resultados que não satisfazem os ramos anteriores, incluindo 71–88 em `A_8`, menos de 89 em `C_8` sem FALSIFIED, contrastes não resolvidos ou predomínio de `ALREADY_STATIONARY` que impeça medir transição.
- [DECLARADO] Convergência semelhante em TGL e em outro autorreferente entra nesse ramo se não houver superioridade resolvida; o significado é “mecanismo genérico não separado”, não “TGL falsa” e não “TGL única”.
- [DECLARADO] Se for necessário declarar equivalência em estudo futuro, a margem e o teste de equivalência devem ser pré-especificados; não rejeitar diferença não prova equivalência. Schuirmann, 1987, DOI `10.1007/BF01068419`, e Lakens, Scheel e Isager, 2018, DOI `10.1177/2515245918770963`, identificadores consultados [KNOWN].

## 10. Interpretações permitidas por resultado secundário

- [DECLARADO] Se C4 sem texto também atingir o alvo, a saída é compatível com memória do pré-treinamento ou com o esquema; a condição TGL não pode ser chamada de causa sem superioridade resolvida.
- [DECLARADO] Se C1 embaralhado falhar e C2/C3 tiverem trajetória semelhante a TGL, o instrumento separa estrutura coerente de vocabulário, mas não separa TGL de outra teoria coerente/autorreferente.
- [DECLARADO] Se C3 atingir um alvo próprio, isso não falsifica P7; apenas impede reivindicar exclusividade operacional e exige uma previsão distinta para TGL.
- [DECLARADO] Se a família abaixo do piso atingir o alvo, o critério de capacidade deve ser revisto em nova versão do protocolo, sem reescrever a corrida aberta.

## 11. O que exatamente não se pode afirmar após qualquer ramo

- [DECLARADO] Não se pode afirmar consciência, vivência, intencionalidade, compreensão subjetiva ou autoconsciência.
- [DECLARADO] Não se pode afirmar alteração de pesos, aprendizado permanente ou treinamento; o desenho mede histórico e saídas, não pesos.
- [DECLARADO] Não se pode afirmar que a teoria seja a única capaz de gerar um atrator, mesmo com quatro controles; a negativa universal permanece [CONJECTURE].
- [DECLARADO] Não se pode afirmar que o texto causou o efeito quando C4 sem texto produz o mesmo resultado ou quando não há contraste resolvido.
- [DECLARADO] Não se pode afirmar um limite em tempo infinito, contração, primitividade ou idempotência verdadeira do LLM a partir do critério finito `A_8`/`C_8`.
- [DECLARADO] Não se pode afirmar que resumir, repetir ou reproduzir o corpus demonstra convergência dinâmica; `C_8` é o único desfecho de transição.
- [DECLARADO] Não se pode afirmar validade física da TGL, prova cosmológica, P versus NP sem leitor ou creditação acadêmica.
- [DECLARADO] Não se pode afirmar independência entre modelos do mesmo fornecedor, ausência de contaminação de treinamento ou persistência após atualização de versão.
- [DECLARADO] Não se pode converter NOT_FALSIFIED em CONFIRMED, nem FALSIFIED no escopo operacional em refutação de todos os teoremas formais.

## 12. Referências metodológicas consultadas

- [KNOWN] Banach, 1922, DOI `10.4064/fm-3-1-133-181`; Perron, 1907, DOI `10.1007/BF01449896`; Frobenius, 1912, DOI `10.3931/e-rara-18865`; Seneta, 2006, DOI `10.1007/0-387-32792-4`; Birkhoff, 1931, DOI `10.1073/pnas.17.2.656`; von Neumann, 1932, DOI `10.1073/pnas.18.1.70`; Spohn, 1978, DOI `10.1063/1.523789`.
- [KNOWN] Clopper e Pearson, 1934, DOI/JSTOR `10.2307/2331986`; Holm, 1979, JSTOR `4615733`; Schuirmann, 1987, DOI `10.1007/BF01068419`; Lakens, Scheel e Isager, 2018, DOI `10.1177/2515245918770963`; Lakens, 2022, DOI `10.1525/collabra.33267`; Nosek et al., 2018, DOI `10.1073/pnas.1708274114`.
- [REAL] As fontes internas foram `Nós\um.py`, a árvore `Nós\tgl_kernel\`, `rotas.py`, o inventário, o índice do acervo e o Atlas, todos listados com consulta em `ESTADO_K03.md`.
- [REAL] As memórias autorizadas foram usadas somente pelos caminhos `C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\traducao-turing-05nov.md`, `acom-e-a-segunda-quantizacao-06nov.md`, `experimento-luiz-registro-mestre.md` e `protocolo-de-colapso-nunca-publico.md`; nenhuma sequência ou entrada foi copiada.
