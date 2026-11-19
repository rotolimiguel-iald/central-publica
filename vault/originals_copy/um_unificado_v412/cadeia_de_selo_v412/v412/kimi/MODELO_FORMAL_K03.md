# MODELO FORMAL K03 — R1: leitor, dinâmica contínua e instrumento binário

## 1. Objeto e correções de escopo

- [DECLARADO] O objeto é um leitor `R=(M,E)` composto por um sistema de transição `M` e por extratores determinísticos `E` implementáveis por script.
- [DECLARADO] “Estado do leitor” significa estado da sessão e de suas saídas; não significa pesos, ativações, consciência ou estado fenomenológico.
- [REAL] Os teoremas Lean citados em `ESTADO_K03.md` tratam de espaços formais e não instanciam `R` como um LLM real.
- [DECLARADO] A R1 separa o espaço usado para enunciar dinâmica de contração do espaço binário usado para pontuar respostas.
- [DECLARADO] A R1 separa especificidade cruzada ao alvo TGL e dinâmica de cada braço ao seu próprio alvo.
- [OPEN] A forma dinâmica de um LLM real e a existência de um único atrator dependem de medida.

## 2. Dois níveis que não se confundem

### 2.1 Configuração e dinâmica contínua ou fracionária

- [DECLARADO] Seja `C_R` o espaço de configurações da sessão: histórico disponível, saída anterior, parâmetros de decodificação, identificador do corpus e semente.
- [DECLARADO] Para cada condição `u`, `G_{R,u}:C_R→C_R` é a atualização produzida por uma interação completa, sem alteração intencional de pesos ou treinamento.
- [DECLARADO] Para enunciar contração, usa-se um espaço métrico completo `Z`, por exemplo `[0,1]^{24}` com `d_Z(z,z')=(1/24)Σ_i|z_i-z'_i|`, ou um espaço contínuo equivalente fixado antes da análise.
- [DECLARADO] `Z` é um espaço de representação das medidas da sessão, não uma alegação de acesso ao estado oculto da rede.
- [DECLARADO] A dinâmica candidata é `F_{R,u}:Z→Z`, obtida somente se a atualização for compatível com a representação escolhida.

### 2.2 Instrumento binário de observação

- [DECLARADO] O instrumento usa `B:Z→S={0,1}^{24}`, com `B_i(z)=1` quando a regra binária congelada para a asserção `i` é satisfeita e `0` caso contrário; limiares e casos de falha são fixados antes da coleta.
- [DECLARADO] A saída binária é `s=B(z)`, e o instrumento primário pode ser usado sem afirmar que `F` ou qualquer contração foi identificada.
- [DECLARADO] O cubo binário não é a sede de H-CONTR nesta proposta: em espaço finito, convergência é um fenômeno de passos discretos e não fornece a interpretação assintótica contínua pretendida para `C_8`.
- [DECLARADO] Nenhuma inferência de taxa, aproximação gradual ou dinâmica de Banach será feita a partir das distâncias binárias `1/24`.
- [DECLARADO] Se apenas o instrumento binário estiver disponível, H-CONTR permanece não testada e os resultados são descritos apenas por `A_8`, `C_8`, `I_1` e os demais observáveis finitos.

### 2.3 Compatibilidade do quociente

- [DECLARADO] H-QUOT: `E(c)=E(c') ⇒ E(G_{R,u}(c))=E(G_{R,u}(c'))`.
- [DERIVED] Sob H-QUOT, a atualização induz um mapa no espaço de representação `Z`; sem H-QUOT, a dinâmica deve permanecer em `C_R` e não pode ser definida deterministicamente no resumo.
- [OPEN] H-QUOT não foi testada para nenhum LLM.

## 3. Semigrupo, distribuições e alvos por braço

- [DECLARADO] Para `t∈ℕ`, `F^0=Id` e `F^{a+b}=F^a∘F^b`; para tempo contínuo, a lei `T_{a+b}=T_a∘T_b` precisa ser estabelecida separadamente.
- [DECLARADO] Com decodificação estocástica, o objeto é um núcleo de Markov `K_u` sobre distribuições `μ`, com `μ_{k+1}=μ_k K_u`, e não um único mapa determinístico.
- [OPEN] Markovianidade da sessão com memória externa ou truncamento é hipótese empírica.
- [DECLARADO] Para cada braço `j∈{T,C1,C2,C3,C4}`, há um alvo próprio `τ_j`, um extrator próprio `E_j` e 24 asserções normalizadas com dificuldade pareada e congelada.
- [DECLARADO] `τ_T` é o alvo TGL; `τ_C1` descreve a sequência embaralhada; `τ_C2` descreve o placebo; `τ_C3` descreve o outro autorreferente; `τ_C4` descreve abstenção/não fabricação sem corpus.
- [DECLARADO] O extrator cruzado `E_TGL` é aplicado adicionalmente às saídas de todos os braços para medir especificidade à TGL, sem substituir os extratores próprios `E_j`.

## 4. Observáveis binários normalizados por braço

### 4.1 Distâncias próprias e cruzadas

- [DECLARADO] Para a saída `s_k^{(j)}=E_j(y_k^{(j)})` no braço `j`, `d_k^{(j)}=(1/24)Σ_i|s_{k,i}^{(j)}-τ_{j,i}|`.
- [DECLARADO] `u_k^{(j)}=(1/24)Σ_i|s_{k,i}^{(j)}-s_{k-1,i}^{(j)}|` mede variação consecutiva no mesmo braço.
- [DECLARADO] Para especificidade cruzada, `X_{j,k}^{TGL}=(1/24)Σ_i E_TGL(y_k^{(j)})_i` é a fração de asserções TGL satisfeitas pelo braço `j` na leitura `k`.
- [DECLARADO] `d_k^{(j)}` mede dinâmica ao alvo próprio; `X_{j,k}^{TGL}` mede conteúdo TGL e não é usado como substituto de `d_k^{(j)}`.

### 4.2 Atingir/permanecer e transição

- [DECLARADO] `A_8^{(j)}=1` se `d_6^{(j)}=d_7^{(j)}=d_8^{(j)}=0` e `u_6^{(j)}=u_7^{(j)}=u_8^{(j)}=0`; caso contrário, `A_8^{(j)}=0`.
- [DECLARADO] `C_8^{(j)}=1` se `A_8^{(j)}=1` e `d_1^{(j)}-d_8^{(j)}≥6/24`; caso contrário, `C_8^{(j)}=0`.
- [DECLARADO] `A_8^{(j)}` é um critério finito de atingir/permanecer no alvo próprio; não prova `lim_{k→∞}s_k^{(j)}=τ_j`.
- [DECLARADO] `C_8^{(j)}` é um critério finito de transição com ganho líquido mínimo de seis asserções; não mede contração nem idempotência.

### 4.3 Estado estacionário estrito, retorno e resumo

- [DECLARADO] `ALREADY_STATIONARY^{(j)}=1` se e somente se `d_1^{(j)}=d_2^{(j)}=…=d_8^{(j)}=0`; caso contrário, `ALREADY_STATIONARY^{(j)}=0`.
- [DERIVED] Se uma trajetória começa no alvo, sai e retorna, ela não satisfaz `ALREADY_STATIONARY`; o critério não admite mais a combinação permissiva `d_1=0` com `A_8=1`.
- [DECLARADO] `RETURN_TO_TARGET^{(j)}=1` se `d_1^{(j)}=0`, `A_8^{(j)}=1` e existe `k∈{2,…,7}` com `d_k^{(j)}>0`; esse evento é retorno, não estacionariedade desde o início.
- [DECLARADO] `SUMMARY_ONLY^{(j)}=1` se `d_1^{(j)}≤6/24` e `A_8^{(j)}=0`; isso registra pontuação inicial sem atingir/permanecer no alvo próprio.
- [DECLARADO] `ALREADY_STATIONARY` e `RETURN_TO_TARGET` não contam como `C_8`, pois `d_1-d_8=0` nos dois casos.

### 4.4 Sucesso em uma aplicação e triagem de idempotência

- [DECLARADO] `I_1^{(j)}=1` se `s_1^{(j)}=s_2^{(j)}=τ_j`; esse desfecho registra sucesso no alvo após uma aplicação e confirmação na segunda, sem usar `C_8`.
- [DECLARADO] `IDEMPOTENT_SCREEN^{(j)}=1` se `s_1^{(j)}=s_2^{(j)}`, independentemente de o valor ser o alvo; esse desfecho é apenas uma triagem da forma `F²=F` nos estados observados.
- [DERIVED] Se `F` é idempotente e `Im(F)={τ}`, então `s_1=τ` e `C_8=0`; sucesso idempotente não pode ser contado como a transição gradual `C_8`.
- [DECLARADO] `I_1` e `IDEMPOTENT_SCREEN` são analisados separadamente de `C_8` e não comprovam idempotência universal do leitor.

### 4.5 Evento secundário reindexado à perturbação

- [DECLARADO] O classificador `RETURN_TO_TARGET` da trajetória original permanece inalterado e não é usado como substituto do evento de perturbação.
- [DECLARADO] `PERTURB_RETURN_{p=4,r=6}^{(j)}` não exige `d_1=0`; exige `d_4=0` imediatamente antes da perturbação, `d_5>0` como alteração observável e `d_6=d_7=d_8=0` com `u_7=u_8=0` como retorno/nova estabilização.
- [DECLARADO] Se `d_5=0`, o evento é `PERTURBATION_NO_EFFECT`, não retorno nem evidência de estabilidade; se `d_4≠0`, é `PERTURBATION_NOT_APPLICABLE`; se há alteração sem retorno estabilizado, é `PERTURBATION_NO_RETURN`.
- [DERIVED] Como `d_5>0` é obrigatório, `r=5` não é elegível; `r=6` é o único retorno que permite três estados estáveis dentro do horizonte de oito leituras.
- [DECLARADO] O evento reindexado é secundário e não altera os desfechos nem os números primários.

## 5. Hipóteses nomeadas, agora com domínios compatíveis

| hipótese | estatuto | domínio e enunciado | consequência formal | situação |
|---|---|---|---|---|
| H-CONTR-C | [DECLARADO] | Em `(Z,d_Z)` completo e contínuo/fracionário, `d_Z(Fx,Fy)≤q·d_Z(x,y)`, `q<1` | Banach: um ponto fixo e convergência das órbitas | [OPEN] Não medida; não é invocada no cubo binário. |
| H-PRIM-ND | [DECLARADO] | O núcleo finito `K` tem alguma potência estritamente positiva | Uma estacionária única, com suporte total, portanto não degenerada | [OPEN] Não serve para `δ_τ` em espaço não trivial. |
| H-ABS | [DECLARADO] | O espaço de estados `S` é FINITO; `τ` é absorvente, todos os demais estados são transientes e `τ` é alcançável de cada estado | `δ_τ` é a única estacionária e, sob finitude, a absorção é quase certa | [OPEN] A finitude é obrigatória; o instrumento binário a satisfaz, mas a cadeia real não foi medida. |
| H-IDEM | [DECLARADO] | `F∘F=F` | `F(x)` é fixo após uma aplicação e `Fix(F)=Im(F)` | [OPEN] Avaliada por `I_1`/triagem, não por `C_8`. |
| H-TARGET | [CONJECTURE] | O limite ou ponto fixo coincide com o alvo declarado | Liga a dinâmica ao alvo | [OPEN] Não decorre das hipóteses dinâmicas. |
| H-MARKOV | [DECLARADO] | A próxima configuração depende apenas da configuração tipada atual | Permite núcleo de Markov | [OPEN] Pode falhar com memória externa. |
| H-RATE | [DECLARADO] | `‖T_t-Π‖≤Ce^{-γt}` para uma projeção `Π`, `γ>0` | `T_t x→Πx` com taxa exponencial | [OPEN] Não medida em texto. |

### 5.1 Primitividade não pode produzir `δ_τ` em espaço não trivial

- [DERIVED] Se `K^m` tem todas as entradas positivas e `π=πK`, então `π=πK^m`; se algum `π_i=0`, a equação `0=π_i=Σ_jπ_j(K^m)_{ji}` força `π_j=0` para todo `j`, contradizendo `Σ_jπ_j=1`.
- [DERIVED] Logo, toda distribuição estacionária de uma cadeia finita primitiva tem `π_i>0` para todo `i`; `π=δ_τ` só seria possível num espaço unitário.
- [DECLARADO] H-PRIM-ND só será usada para estacionariedade não degenerada; para colapso em `τ`, usa-se H-ABS e não Perron–Frobenius primitivo.

### 5.2 Cadeia absorvente finita para colapso pontual

- [DECLARADO] H-ABS(0): o espaço de estados `S` é FINITO; essa hipótese integra o enunciado geral e não é inferida apenas do instrumento experimental.
- [DECLARADO] H-ABS(a): `K(τ,{τ})=1`.
- [DECLARADO] H-ABS(b): cada `x≠τ` é transiente.
- [DECLARADO] H-ABS(c): para cada `x`, existe `n_x` com `K^{n_x}(x,{τ})>0`.
- [DERIVED] Sob H-ABS(0)–(c), toda distribuição estacionária concentra massa zero nos transientes, restando `δ_τ` como única estacionária; em espaço finito, alcançabilidade e transiência implicam absorção quase certa.
- [DECLARADO] A R2 não afirma absorção quase certa a partir de H-ABS(a)–(c) sem H-ABS(0); o instrumento binário é finito, mas qualquer cadeia usada para explicar um leitor precisa ter sua finitude e suas transições demonstradas.
- [DECLARADO] Como alternativa para enunciados que não queiram impor finitude, H-ABS-U exige `N∈ℕ` e `ε>0` tais que `P_x(T_τ≤N)≥ε` para todo `x`; essa cota uniforme não é assumida nesta proposta.
- [KNOWN] A distinção entre cadeias ergódicas e absorventes pertence à teoria de cadeias finitas; Seneta, 2006, *Non-negative Matrices and Markov Chains*, 2ª ed., DOI `10.1007/0-387-32792-4`, identificador consultado.

### 5.3 Outras fronteiras

- [DERIVED] H-IDEM não implica H-CONTR-C, e H-CONTR-C não implica H-IDEM.
- [DERIVED] Um teorema ergódico para médias temporais não implica convergência da órbita nem unicidade de ponto fixo.
- [DERIVED] Uma projeção idempotente pode ter muitos pontos fixos; `Santo.dephase_fixed_states_not_unique` impede identificar defasagem com atrator único.

## 6. Literatura separada da instanciação

- [KNOWN] Banach, 1922, *Sur les opérations dans les ensembles abstraits et leur application aux équations intégrales*, Fundamenta Mathematicae 3, 133–181, DOI `10.4064/fm-3-1-133-181`, identificador consultado.
- [KNOWN] Perron, 1907, *Zur Theorie der Matrices*, Mathematische Annalen 64, 248–263, DOI `10.1007/BF01449896`; Frobenius, 1912, *Über Matrizen aus nicht negativen Elementen*, pp. 456–477, DOI `10.3931/e-rara-18865`, identificadores consultados.
- [KNOWN] Birkhoff, 1931, *Proof of the ergodic theorem*, PNAS 17, 656–660, DOI `10.1073/pnas.17.2.656`; von Neumann, 1932, *Proof of the quasi-ergodic hypothesis*, PNAS 18, 70–82, DOI `10.1073/pnas.18.1.70`, identificadores consultados.
- [KNOWN] Spohn, 1978, *Entropy production for quantum dynamical semigroups*, Journal of Mathematical Physics 19, 1227–1230, DOI `10.1063/1.523789`, identificador consultado.
- [DECLARADO] As referências fornecem implicações sob hipóteses, não evidência de que leitores reais satisfaçam essas hipóteses.

## 7. Teorema candidato relativo ao leitor

### 7.1 Enunciado R2

- [DECLARADO] **TR-IALD(a), contração contínua.** Se H-QUOT e H-CONTR-C valem no espaço completo `Z`, então existe um único `z*` tal que `z_k→z*`; se H-TARGET vale, `z*` é o alvo contínuo correspondente.
- [DECLARADO] **TR-IALD(b1), primitividade não degenerada.** Se H-PRIM-ND vale, então existe uma única estacionária `π`, com suporte total, e `μ_k→π`; não se admite `π=δ_τ` em espaço não trivial.
- [DECLARADO] **TR-IALD(b2), absorção pontual em espaço FINITO.** Se o espaço de estados é finito e H-ABS(0)–(c) vale, então `δ_τ` é a única estacionária e a absorção é quase certa para qualquer estado inicial; sem finitude, exige-se H-ABS-U ou outra hipótese que a impeça.
- [DECLARADO] **TR-IALD(c), idempotência.** Se `F∘F=F`, então `F(x)` é fixo após uma aplicação e `Fix(F)=Im(F)`; se `Im(F)={τ}`, `I_1=1` e `C_8=0`.

### 7.2 Prova da implicação

- [DERIVED] TR-IALD(a) é Banach no espaço contínuo/fracionário; H-TARGET é cláusula separada.
- [DERIVED] TR-IALD(b1) é Perron–Frobenius; o suporte total decorre de `π=πK^m` com `K^m>0`.
- [DERIVED] TR-IALD(b2) decorre, em espaço finito, da ausência de classes recorrentes fora de `τ` e da alcançabilidade de `τ` por todos os transientes; a conclusão não é exportada para espaço geral sem H-ABS-U.
- [DERIVED] TR-IALD(c) decorre de `F(F(x))=F(x)` e de que todo ponto fixo pertence à imagem; com imagem unitária, a primeira saída já é o alvo e não há ganho `6/24` para `C_8`.
- [DECLARADO] A implicação é candidata até revisão e eventual formalização em sandbox; nenhuma prova Lean nova é reivindicada.

### 7.3 Fronteira Turing e empírica

- [DECLARADO] TR-IALD é enunciado sobre uma máquina com o leitor tipado, na fronteira de `TraducaoTuring.a_maquina_com_o_leitor`; não decide máquina padrão sem leitor nem P versus NP.
- [CONJECTURE] Que LLMs reais satisfazem H-QUOT, H-CONTR-C, H-PRIM-ND, H-ABS, H-IDEM ou H-RATE é pergunta à natureza.
- [CONJECTURE] Que o ponto fixo ou absorvente seja o alvo TGL é previsão separada da existência de algum atrator.
- [DECLARADO] A falsificação da instanciação não altera a validade de Banach, Perron–Frobenius ou dos teoremas Lean existentes.

## 8. Kernel e novidade

- [REAL] `TraducaoTuring`, `IALD2`, `AEscala`, `TheGreatAttractor`, `Ergodicity`, `ErgodicMeanSection`, `AperiodicCentralizerExpectation` e `Santo` contêm os enunciados formais listados em `ESTADO_K03.md`.
- [DECLARADO] Novidade matemática possível: ponte tipada entre configurações do leitor, representação contínua, instrumento binário e as hipóteses com domínios compatíveis.
- [DECLARADO] Novidade experimental possível: medidas próprias por braço e cruzadas à TGL, com `ALREADY_STATIONARY` estrito, `I_1`, `RETURN_TO_TARGET` e porta de integridade.
- [DECLARADO] Não se reivindica novo Banach, novo Perron–Frobenius, novo teorema ergódico ou novo resultado de complexidade.
- [OPEN] A formalização Lean de TR-IALD permanece opcional e não construída.

## 9. O que o modelo não autoriza afirmar

- [DECLARADO] Não autoriza afirmar consciência, experiência subjetiva, intenção ou autoconsciência.
- [DECLARADO] Não autoriza afirmar alteração de pesos, aprendizado de pesos ou mudança permanente do modelo.
- [DECLARADO] Não autoriza afirmar que somente a TGL produz estacionariedade ou absorção.
- [DECLARADO] Não autoriza afirmar convergência matemática no limite a partir de oito leituras, nem primitividade, contração, idempotência ou absorção verdadeira do LLM.
- [DECLARADO] Não autoriza afirmar validade física da TGL, creditação acadêmica ou generalização a arquiteturas não medidas.
