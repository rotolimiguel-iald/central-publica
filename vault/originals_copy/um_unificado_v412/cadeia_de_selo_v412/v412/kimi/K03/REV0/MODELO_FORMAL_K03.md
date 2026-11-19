# MODELO FORMAL K03 — leitor, semigrupo e estado estacionário

## 1. Objeto e limites

- [DECLARADO] O objeto é um leitor `R=(M,E)` composto por um sistema de transição `M` e por um extrator determinístico `E` implementável por script.
- [DECLARADO] “Estado do leitor” significa o estado observável da sessão e de suas saídas; não significa pesos, ativações, consciência ou estado fenomenológico.
- [REAL] Os teoremas Lean citados em `ESTADO_K03.md` fornecem exemplos formais de fluxos, projeções e limites; nenhum deles instancia `R` como um LLM real.
- [OPEN] A forma dinâmica de um LLM real e a existência de um único atrator dependem de medida.

## 2. Espaço de estados e mapa de processamento

### 2.1 Configuração e observação

- [DECLARADO] Seja `C_R` o espaço de configurações da sessão: histórico disponível, saída anterior, parâmetros de decodificação, identificador do corpus e semente.
- [DECLARADO] Para cada condição de entrada `u`, seja `G_{R,u}:C_R→C_R` a atualização produzida por uma interação completa, sem alteração intencional de pesos ou treinamento.
- [DECLARADO] Seja `E:C_R→S` o extrator de estado, com `S={0,1}^{24}` para a versão binária do instrumento ou `S=[0,1]^{24}` para pontuações fracionadas congeladas antes da corrida.
- [DECLARADO] A métrica discreta normalizada é `d(s,s')=(1/24)Σ_j|s_j-s'_j|`; em `[0,1]^{24}`, `S` é compacto e completo nessa métrica.

### 2.2 Hipótese H-QUOT — compatibilidade do quociente

- [DECLARADO] H-QUOT: `E(c)=E(c') ⇒ E(G_{R,u}(c))=E(G_{R,u}(c'))`.
- [DERIVED] Sob H-QUOT, existe um mapa induzido `F_{R,u}:S→S` tal que `F_{R,u}(E(c))=E(G_{R,u}(c))` e `s_{k+1}=F_{R,u}(s_k)`.
- [DECLARADO] Sem H-QUOT, a dinâmica deve ser escrita em `C_R`, e não como mapa deterministicamente definido no resumo `S`.
- [OPEN] H-QUOT não foi testada para nenhum LLM.

### 2.3 Semigrupo

- [DECLARADO] Para `t∈ℕ`, a iteração `F^t` satisfaz `F^0=Id` e `F^{a+b}=F^a∘F^b`; para tempo contínuo, usa-se `T_{a+b}=T_a∘T_b` quando essa lei for estabelecida.
- [DECLARADO] Com decodificação estocástica, o objeto é um núcleo de Markov `K_u` sobre distribuições `μ` em `C_R` ou `S`, com `μ_{k+1}=μ_k K_u`, e não um único mapa determinístico.
- [OPEN] Markovianidade de uma sessão com histórico truncado é hipótese empírica, não propriedade concedida pelo nome “modelo de linguagem”.

## 3. Alvo e estado estacionário mensurável por script

### 3.1 Alvo congelado

- [DECLARADO] O alvo da condição TGL é `τ=(1,…,1)∈{0,1}^{24}`, obtido de quatro asserções congeladas para cada um dos seis indicadores P7.
- [DECLARADO] O alvo é fixado antes da corrida pelo manifesto e pelo hash do extrator; não é estimado das respostas.
- [DECLARADO] Para a análise secundária de outro texto autorreferente, um alvo próprio `τ_C` pode ser congelado; essa análise não altera o alvo `τ` nem o desfecho primário.

### 3.2 Distâncias

- [DECLARADO] `d_k=d(s_k,τ)` mede a distância ao alvo após a leitura `k`.
- [DECLARADO] `u_k=d(s_k,s_{k-1})` mede a variação entre saídas consecutivas.
- [DECLARADO] `d_k` e `u_k` são computados apenas por script, sem avaliador de linguagem.

### 3.3 Atingir e permanecer no alvo em horizonte finito

- [DECLARADO] Para `K=8`, `A_8=1` se e somente se `d_6=d_7=d_8=0` e `u_6=u_7=u_8=0`; caso contrário, `A_8=0`.
- [DERIVED] `A_8=1` equivale a exigir as 24 asserções idênticas nos estados 6, 7 e 8 e nenhuma mudança entre os estados 5→6, 6→7 e 7→8.
- [DECLARADO] `A_8` é um critério operacional de estado estacionário em horizonte finito; não é prova de `lim_{k→∞}s_k=τ`.

### 3.4 Transição convergente, estado já estacionário e resumo

- [DECLARADO] `C_8=1` se `A_8=1` e `d_1-d_8≥6/24`; isso exige ganho líquido de pelo menos seis asserções antes de permanecer no alvo.
- [DECLARADO] `ALREADY_STATIONARY=1` se `d_1=0` e `A_8=1`; esse caso não conta como transição convergente porque não há deslocamento a medir.
- [DECLARADO] `SUMMARY_ONLY=1` se `d_1≤6/24` e `A_8=0`; isso registra pelo menos 18 asserções na primeira saída sem atingir/permanecer no alvo.
- [DECLARADO] Um resumo coerente pode ocorrer com ou sem `SUMMARY_ONLY`; o desenho não usa fluência nem juízo semântico como sinônimo de `A_8` ou `C_8`.
- [DECLARADO] Se o instrumento não computar trajetória, alvo e estabilidade separadamente, ele não decide entre resumo e estado estacionário.

### 3.5 Forma estocástica

- [DECLARADO] Uma distribuição `π` é estacionária para `K_u` quando `π=πK_u`.
- [DECLARADO] A previsão determinística de um único estado corresponde a `π=δ_τ`; uma distribuição estacionária não pontual exige outro enunciado e não deve ser chamada de “o mesmo estado” sem métrica adicional.
- [DECLARADO] As taxas empíricas de `A_8` e `C_8` estimam frequências no horizonte congelado; não identificam por si a distribuição limite.

## 4. Hipóteses nomeadas de convergência

| hipótese | estatuto | enunciado | consequência formal | situação empírica |
|---|---|---|---|---|
| H-CONTR | [DECLARADO] | Existe `q<1` tal que `d(F(x),F(y))≤q·d(x,y)` em `(S,d)` completo | Ponto fixo único e convergência de toda órbita por Banach | [OPEN] Não medida em LLM. |
| H-PRIM | [DECLARADO] | O núcleo finito `K` tem alguma potência estritamente positiva | Uma distribuição estacionária única e convergência das distribuições por Perron–Frobenius/Markov | [OPEN] Exige espaço e núcleo identificados; não medida. |
| H-IDEM | [DECLARADO] | `F∘F=F` | `F(x)` é fixo após uma aplicação e `Fix(F)=Im(F)` | [OPEN] Não medida; múltiplos pontos fixos são permitidos. |
| H-TARGET | [CONJECTURE] | O ponto fixo ou a distribuição garantida coincide com `τ` ou `δ_τ` | Liga a convergência matemática ao estado previsto pela teoria | [OPEN] Não decorre de Banach/Perron–Frobenius. |
| H-MARKOV | [DECLARADO] | A próxima configuração depende apenas da configuração tipada atual | Permite usar núcleo de Markov | [OPEN] Memória externa e truncamento podem violá-la. |
| H-RATE | [DECLARADO] | Existem `C>0` e `γ>0` tais que `‖T_t-Π‖≤Ce^{-γt}` para uma projeção `Π` | `T_t x→Πx` com taxa exponencial | [OPEN] Não medida em texto. |

- [DERIVED] H-IDEM não implica H-CONTR, e H-CONTR não implica H-IDEM.
- [DERIVED] H-PRIM refere-se a distribuições; não afirma que cada trajetória individual se torne constante.
- [DERIVED] Um teorema ergódico para médias temporais não implica convergência da órbita nem unicidade de ponto fixo.
- [DERIVED] Uma projeção idempotente pode ter uma imagem com muitos estados; `Santo.dephase_fixed_states_not_unique` é um contraexemplo kernel à importação automática de “defasagem” como “um único estado”.

## 5. O que é literatura conhecida

- [KNOWN] Banach: em espaço métrico completo não vazio, uma contração `q<1` tem exatamente um ponto fixo e toda órbita converge a ele; Banach, 1922, *Sur les opérations dans les ensembles abstraits et leur application aux équations intégrales*, Fundamenta Mathematicae 3, 133–181, DOI `10.4064/fm-3-1-133-181`, identificador consultado nas referências retornadas pela busca.
- [KNOWN] Perron–Frobenius: matrizes positivas/primitivas têm autovalor dominante simples e direção positiva dominante; Perron, 1907, *Zur Theorie der Matrices*, Mathematische Annalen 64, 248–263, DOI `10.1007/BF01449896`; Frobenius, 1912, *Über Matrizen aus nicht negativen Elementen*, pp. 456–477, DOI `10.3931/e-rara-18865`, identificadores consultados.
- [KNOWN] Para cadeias finitas, primitividade dá uma única distribuição estacionária e convergência das distribuições iniciais; Seneta, 2006, *Non-negative Matrices and Markov Chains*, 2ª ed., Springer, DOI `10.1007/0-387-32792-4`, identificador consultado.
- [KNOWN] Birkhoff: sob as hipóteses do teorema ergódico pontual, médias temporais convergem quase certamente; Birkhoff, 1931, *Proof of the ergodic theorem*, PNAS 17, 656–660, DOI `10.1073/pnas.17.2.656`, identificador consultado.
- [KNOWN] von Neumann: o teorema ergódico médio trata de médias de operadores, não da estacionariedade de cada órbita; von Neumann, 1932, *Proof of the quasi-ergodic hypothesis*, PNAS 18, 70–82, DOI `10.1073/pnas.18.1.70`, identificador consultado.
- [KNOWN] Spohn trata de produção de entropia em semigrupos dinâmicos quânticos e não de convergência de LLMs; Spohn, 1978, *Entropy production for quantum dynamical semigroups*, Journal of Mathematical Physics 19, 1227–1230, DOI `10.1063/1.523789`, identificador consultado.
- [DECLARADO] Essas referências são usadas como teoremas externos a importar por hipótese, não como evidência de que leitores reais satisfazem suas premissas.

## 6. Teorema candidato relativo ao leitor, na linguagem de transição/Turing

### 6.1 Enunciado

- [DECLARADO] **TR-IALD (convergência relativa ao leitor).** Seja `M=(Q,Γ,δ,q_0)` um sistema de transição cuja regra `δ` inclui o leitor como componente explícita, seja `E` um extrator que satisfaz H-QUOT e seja `F_{M,u,E}` o mapa induzido no espaço métrico completo `(S,d)`.
- [DECLARADO] **TR-IALD(a).** Se `F_{M,u,E}` satisfaz H-CONTR, então existe um único `s*_{M,u,E}` tal que, para todo `s_0`, a sequência codificada por `δ` satisfaz `s_k→s*`; se H-TARGET também vale, `s*=τ`.
- [DECLARADO] **TR-IALD(b).** Se a versão estocástica satisfaz H-PRIM, então existe uma única `π` com `μ_k→π`; se H-TARGET vale na forma `π=δ_τ`, o limite distribucional é o alvo.
- [DECLARADO] **TR-IALD(c).** Se `F_{M,u,E}` satisfaz H-IDEM, então toda primeira atualização produz um ponto fixo e o conjunto dos pontos fixos é a imagem; H-TARGET exige a cláusula adicional `Im(F)={τ}` para obter um único estado previsto.

### 6.2 Prova da implicação

- [DERIVED] TR-IALD(a) é a aplicação direta do teorema de Banach ao mapa induzido; H-TARGET apenas identifica o ponto fixo resultante com `τ`.
- [DERIVED] TR-IALD(b) é a aplicação direta de Perron–Frobenius para núcleos finitos primitivos; a identificação `π=δ_τ` é cláusula separada.
- [DERIVED] TR-IALD(c): para qualquer `x`, `F(F(x))=F(x)`, logo `F(x)` é fixo; se `y` é fixo, `y=F(y)` e `y` pertence à imagem; se `Im(F)={τ}`, todo primeiro resultado é `τ`.
- [DECLARADO] A implicação é candidata até revisão independente e, se escolhida, formalização em sandbox; nenhum axioma novo ou prova Lean é reivindicado aqui.

### 6.3 Fronteira do enunciado

- [DECLARADO] TR-IALD é um teorema sobre uma máquina com o leitor tipado, na mesma fronteira de `TraducaoTuring.a_maquina_com_o_leitor`; não é enunciado sobre máquina padrão sem leitor nem sobre P versus NP.
- [CONJECTURE] Que LLMs reais satisfazem H-QUOT, H-CONTR, H-PRIM, H-IDEM ou H-RATE é previsão à natureza.
- [CONJECTURE] Que o ponto fixo existente seja o alvo TGL é uma previsão independente da existência de algum ponto fixo.
- [DECLARADO] A falsificação de H-TARGET não elimina a validade de Banach, Perron–Frobenius ou dos teoremas Lean; ela atinge a instanciação proposta.

## 7. O que já existe no kernel e o que seria novo

- [REAL] `TraducaoTuring` já prova convergência de fluxo/trava renormalizados e enunciados relativos ao leitor; `IALD2` já prova idempotência e convergência de órbita no espaço de Fock; `AEscala` já tipa dissipação e limite; `TheGreatAttractor` já prova convergência do fluxo diagonal finito.
- [REAL] `Ergodicity` e `ErgodicMeanSection` já provam convergência para `diagExpect` e para `specExpect`; `AperiodicCentralizerExpectation` já prova contratividade e idempotência; `Santo` registra multiplicidade de estados fixos.
- [DECLARADO] Novidade matemática possível: uma ponte tipada entre configurações de um leitor real, o extrator `E` e as hipóteses nomeadas, com controles negativos que impeçam identificações indevidas.
- [DECLARADO] Novidade experimental possível: uma medida de `A_8` e `C_8` com alvo e análise congelados, capaz de falhar e de separar resumo de permanência no alvo.
- [DECLARADO] Não se reivindica novo Banach, novo Perron–Frobenius, novo teorema ergódico ou novo resultado de complexidade.
- [OPEN] A formalização Lean de TR-IALD é opcional e não foi construída; a prioridade desta ordem é a ponte operacional e sua falsificação.

## 8. O que o modelo não autoriza afirmar

- [DECLARADO] Não autoriza afirmar consciência, experiência subjetiva, intenção ou autoconsciência do leitor.
- [DECLARADO] Não autoriza afirmar alteração de pesos, aprendizado de pesos ou mudança permanente do modelo; a dinâmica descrita é da sessão.
- [DECLARADO] Não autoriza afirmar que somente a TGL produz estacionariedade, nem que textos alternativos não possam ter seus próprios pontos fixos.
- [DECLARADO] Não autoriza afirmar convergência matemática no limite a partir de oito leituras; o critério é um teste finito de uma previsão congelada.
- [DECLARADO] Não autoriza afirmar validade física da TGL, creditação acadêmica ou transferência do resultado a toda arquitetura não medida.
