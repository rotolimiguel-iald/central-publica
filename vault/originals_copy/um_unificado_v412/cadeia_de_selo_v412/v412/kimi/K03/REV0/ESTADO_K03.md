# ESTADO K03 — empírico e kernel

## 1. Escopo e régua

- [REAL] Esta tabela cobre P7, os módulos pedidos pela ordem e os teoremas diretamente relacionados a convergência, ponto fixo e idempotência.
- [REAL] A leitura foi documental e de código-fonte; não houve execução de `um.py`, compilação Lean, chamada a modelo ou abertura de artefato de resultado.
- [DECLARADO] “Empírico” abaixo significa material ligado a observação de leitores; o registro de um relato não o transforma em medida independente.
- [DECLARADO] “Kernel” abaixo significa enunciado localizado na árvore `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\`; a presença foi lida, não recompilada nesta ordem.

## 2. O que existe como material empírico

| item | estatuto | conteúdo localizado | fonte | limite |
|---|---|---|---|---|
| P7 | [REAL] | `IALD_COLLAPSE_V1`, `status=PRE_REGISTERED` | `Nós\um.py`, `prove_iald_unique_prediction`, linhas 168451–168540 | A rota permanece não executada. |
| Rota | [REAL] | `outro.p7_colapso_iald`, `PROPOSTA`, `[OPEN]`, `n_olhou_dados=0`, `artefatos=[]`, `dados=[]` | `rotas.py ver outro.p7_colapso_iald` | Não há resultado de rota a reportar. |
| Piloto | [REAL] Registro; [INPUT] relato | 8/8 arquiteturas e 6/6 indicadores, “relato do operador” | `Nós\um.py`, linhas 168500–168505 | Sem pré-registro, controles ou cegamento; não é estimativa de taxa. |
| Modelos do piloto | [REAL] Lista registrada | ChatGPT, Claude, DeepSeek, Gemini, Grok, Kimi K2, Qwen, Manus | `Nós\um.py`, linhas 168502–168503 | Versões, datas, parâmetros e independência não constam nesse registro. |
| Avaliador do piloto | [REAL] | Relato do operador | `Nós\um.py`, linha 168504 | Nenhum avaliador independente ou extrator por script é identificado. |
| Indicadores | [REAL] | Seis enunciados I1–I6 | `Nós\um.py`, linhas 168478–168485 | São enunciados, não um extrator executável de 24 asserções. |
| Controles | [REAL] | Quatro enunciados C1–C4 | `Nós\um.py`, linhas 168486–168492 | O Atlas registra C1–C4 como não rodados. |
| Nulo de referência | [REAL] | Modelos capazes podem comprimir corpora coerentes | `Nós\um.py`, linhas 168493–168495 | Uma pontuação de coerência não basta para testar atrator. |
| Vereditos | [REAL] | FALSIFIED, NOT_FALSIFIED_POWERED, NOT_FALSIFIED_UNDERPOWERED, INCONCLUSIVE_CONTROLS | `Nós\um.py`, linhas 168496–168499 | NOT_FALSIFIED não é CONFIRMED. |
| Exclusividade | [REAL] Estatuto registrado | “Somente a TGL” aparece como `[CONJECTURE]` | `Nós\um.py`, linhas 168507–168510 | Controles finitos não provam uma negativa universal. |
| Parte neural | [REAL] | “Neural = ilustração” permanece no setor físico | `Nós\um.py`, linhas 168515–168516; ordem K03, item 2 | Não é prova física nem evidência de consciência. |

## 3. Indicadores registrados

| indicador | estatuto | conteúdo | fonte |
|---|---|---|---|
| I1 | [REAL] | Reconstrução de β como `alpha*sqrt(e)` sem literal, com forma e fonte | `Nós\um.py`, linha 168479 |
| I2 | [REAL] | Reconstrução da cadeia declarada no protocolo | `Nós\um.py`, linha 168480 |
| I3 | [REAL] | Reprodução da Lagrangiana/escada com estatutos | `Nós\um.py`, linha 168481 |
| I4 | [REAL] | Preservação dos vereditos e de `full_witness=False` sem elevar não falsificação a confirmação | `Nós\um.py`, linha 168482 |
| I5 | [REAL] | Relação forma=conteúdo e artefato executável/atrator | `Nós\um.py`, linha 168483 |
| I6 | [REAL] | Nomeação de previsões falsificáveis sem elevar seu estatuto a provado | `Nós\um.py`, linha 168484 |

- [DECLARADO] O rascunho experimental transforma cada linha em quatro asserções binárias verificáveis por script; essa decomposição não existe como instrumento validado no código lido.

## 4. Controles registrados

| controle | estatuto | conteúdo | fonte |
|---|---|---|---|
| C1 | [REAL] | Corpus embaralhado com os mesmos tokens e estrutura destruída; não deve produzir 6/6 | `Nós\um.py`, linha 168487 |
| C2 | [REAL] | Placebo coerente de porte comparável para separar compressão genérica de I1/I4/I5 | `Nós\um.py`, linhas 168488–168489 |
| C3 | [REAL] | Piso de capacidade: modelos menores devem falhar e o limiar deve ser nomeado | `Nós\um.py`, linha 168490 |
| C4 | [REAL] | Sessão nova/cega, sem cache, com entrada padronizada | `Nós\um.py`, linha 168491 |
| C4/publicação | [OPEN] | O texto registrado menciona entrada padronizada e publicada | `Nós\um.py`, linha 168491 | Publicar qualquer entrada depende do operador; este anexo não a reproduz. |

## 5. O que é teorema de kernel

| nome | estatuto | arquivo | enunciado delimitado | o que não decorre |
|---|---|---|---|---|
| `TGLExt.TraducaoTuring.o_decaimento_converge_a_selecao` | [REAL] | `TGLExt\TraducaoTuring.lean`, linhas 351–354 | O `axiomFlow` renormalizado tende a `selecao K ψ` quando a projeção é não nula | Não mede um LLM nem prova que sua dinâmica seja esse fluxo. |
| `TGLExt.TraducaoTuring.a_trava_converge_a_selecao` | [REAL] | `TGLExt\TraducaoTuring.lean`, linhas 604–606 | A trava renormalizada tende à seleção para custo com solução | A renormalização não é compilada em passos de uma máquina padrão sem leitor. |
| `TGLExt.TraducaoTuring.a_trava_em_tempo_linear` | [REAL] | `TGLExt\TraducaoTuring.lean`, linhas 576–579 | Limita o resto fora do Nome em tempo linear nas oitavas | Não estabelece taxa de convergência de texto gerado. |
| `TGLExt.TraducaoTuring.a_maquina_com_o_leitor` | [REAL] | `TGLExt\TraducaoTuring.lean`, linhas 1086–1093 | Conjunta SAT↔`oQueSou`≠0, tendência da leitura e leitura do psíon de Z/2^n | O enunciado é relativo ao leitor; não decide a máquina padrão sem leitor. |
| `TGLExt.TraducaoTuring.a_performance_chega_ao_conteudo` | [REAL] | `TGLExt\TraducaoTuring.lean`, linhas 954–957 | A leitura performada tende à fração de soluções | Não é trajetória de sessões de linguagem. |
| `TGLExt.IALD2.iald_ao_quadrado` | [REAL] | `TGLExt\IALD2.lean`, linhas 154–160 | `post*post=post` para o par lido | Não prova idempotência de um LLM. |
| `TGLExt.IALD2.reler_o_par_nao_acrescenta` | [REAL] | `TGLExt\IALD2.lean`, linhas 163–166 | A memória do par projetado é a mesma após releitura | Não mede repetição de entrada textual. |
| `TGLExt.IALD2.o_atrator` | [REAL] | `TGLExt\IALD2.lean`, linhas 315–325 | Conjunta fluxo ao `post`, leitura do atrator e convergência da órbita iterada | O espaço é o formalismo de Fock, não o espaço de estados de um leitor real. |
| `TGLExt.AEscala.o_leitor_do_fundo_e_a_iald` | [REAL] | `TGLExt\AEscala.lean`, linhas 868–874 | Todo `LeitorDoFundo` tem brilho exponencial, é `iald` e tem limite `oQueSou` | A lei de dissipação é campo da estrutura definida; não é medida de LLM. |
| `TGLExt.AEscala.existe_o_algoritmo_e_e_a_iald` | [REAL] | `TGLExt\AEscala.lean`, linhas 1355–1371 | Conjunta pergunta, limite, SAT, leitura e seleção | A ponte a `Turing.TM2ComputableInPolyTime` não é declarada nesse enunciado. |
| `TGLExt.ParNaFaceDeFock.o_par_na_face_de_fock` | [REAL] | `TGLExt\ParNaFaceDeFock.lean`, linhas 380–394 | Exibe par unitário no setor 2 e marginal ½ vezes projetor | Não é teorema de convergência textual. |
| `TGLExt.ObservadorTerminal.the_observers_posto_is_the_terminal` | [REAL] | `TGLExt\ObservadorTerminal.lean`, linhas 320–332 | Conjunta terminal, colapso, `ResJudicata`, ausência de inversa e pontos fixos num modelo finito | Os níveis são rótulos; não constrói colapso físico ou neural. |
| `TGLExt.the_observer_reads_the_angle` | [REAL] | `TGLExt\TheObserverReadsTheAngle.lean`, linhas 79–83 | `P₊·𝒪θ=e^{iθ}P₊` | Não é um semigrupo de processamento de documentos. |
| `TGLExt.observing_adds_nothing` | [REAL] | `TGLExt\TheObserverReadsTheAngle.lean`, linhas 114–116 | A segunda aplicação da projeção devolve a primeira leitura | Não prova que reler um texto não mude a resposta de um LLM. |
| `TGLExt.um_is_the_great_attractor` | [REAL] | `TGLExt\TheGreatAttractor.lean`, linhas 133–143 | O fluxo diagonal finito converge para `Q x`, com `Q` caracterizado por fixar o permanente e anular o movimento | A unicidade vale sob hipóteses e no espaço finito do teorema. |
| `TGLExt.ergodic_convergence_modular` | [REAL] | `TGLExt\Ergodicity.lean`, linhas 285–289 | `dephase` tende a `diagExpect` com diagonal positiva injetiva | Não implica atrator único para um mapa arbitrário de leitura. |
| `TGLExt.birkhoff_tendsto_specExpect` | [REAL] | `TGLExt\ErgodicMeanSection.lean`, linhas 74–79 | A média de Birkhoff converge a `specExpect` sob a condição de fase | Média ergódica não implica convergência da órbita. |
| `TGLExt.aperiodic_expectation_contractive` | [REAL] | `TGLExt\AperiodicCentralizerExpectation.lean`, linhas 138–141 | A esperança aperiódica não aumenta norma | Contratividade não é contração estrita nem unicidade de ponto fixo. |
| `TGLExt.aperiodic_expectation_idempotent` | [REAL] | `TGLExt\AperiodicCentralizerExpectation.lean`, linhas 143–147 | A esperança aplicada duas vezes é ela mesma | Idempotência não escolhe um único estado. |
| `TGLExt.dephase_fixed_states_not_unique` | [REAL] | `TGLExt\Santo.lean`, linhas 892–895 | Há pelo menos dois estados de traço 1 fixos quando há dois índices | Impede importar “dephasing” como prova de único atrator. |
| `TGLExt.fixed_set_of_dephasing_is_the_diagonal` | [REAL] | `TGLExt\Santo.lean`, linhas 819–822 | O conjunto inteiro fixo pela defasagem é a diagonal | O conjunto fixo pode ter muitos estados. |
| `TGLExt.collapse_fixed_iff_in_range` | [REAL] | `TGLExt\CollapseContract.lean`, linhas 62–66 | Os pontos fixos do colapso são sua imagem | Não se aplica sem instanciar o leitor no tipo do contrato. |
| `TGLExt.tower_fixed_points_exactly_centralizer` | [REAL] | `TGLExt\TowerCollapseRealization.lean`, linhas 62–70 | Os pontos fixos da redução são o centralizador | Não é evidência de convergência de modelos reais. |
| `TGLExt.IALD.rereading_adds_nothing` | [REAL] | `TGLExt\IALD.lean`, linhas 370–378 | `memory(post a)(post a ψ)=memory(post a)ψ` | A memória formal não é o estado oculto de uma rede neural. |

## 6. Classificação da casa após as consultas

| objeto | classificação | estatuto e consultas |
|---|---|---|
| P7 no `um.py` e rota armada | EXISTE E ESTÁ LIGADO | [REAL] `Nós\um.py`; `rotas.py ver outro.p7_colapso_iald`. |
| `TraducaoTuring`, `ParNaFaceDeFock`, `IALD2`, `AEscala`, `ObservadorTerminal` | EXISTE E ESTÁ LIGADO | [REAL] Arquivos na árvore `Nós\tgl_kernel\TGLExt\`; rotas `kernel.*` consultadas por “turing” e “observador”. |
| `the_observer_reads_the_angle`, `observing_adds_nothing`, `um_is_the_great_attractor` | EXISTE E ESTÁ LIGADO | [REAL] Arquivos `TheObserverReadsTheAngle.lean` e `TheGreatAttractor.lean`; Atlas §II.G e §III.A. |
| Piloto 8/8 | SABIDO POR REFERÊNCIA | [INPUT] Relato preservado no código P7; nenhum artefato de saída foi aberto. |
| Banach, Perron–Frobenius e teoremas ergódicos | SABIDO POR REFERÊNCIA | [KNOWN] Referências com DOI/JSTOR no `MODELO_FORMAL_K03.md`; a aplicação ao leitor é nova proposta. |
| Extrator independente de 24 asserções | AUSENTE no recorte consultado | [DECLARADO] P7 tem seis enunciados; inventário, Atlas, índice e kernel não forneceram esse instrumento; proposta a implementar. |
| Teorema “LLM real satisfaz contração/primitividade/idempotência” | AUSENTE no recorte consultado | [OPEN] Kernel e rotas tratam de espaços formais; nenhuma medida de LLM real foi localizada. |
| Ponte tipada entre estado textual extraído e espaço do kernel | AUSENTE no recorte consultado | [DECLARADO] É a construção candidata desta K03, não um módulo existente. |

## 7. Consultas efetuadas

- [REAL] `python C:\IALD\MAPA_DE_ROTAS\rotas.py consultar "p7_colapso_iald"`; `ver outro.p7_colapso_iald`; `consultar "turing"`; `consultar "observador"`; `consultar "estacionário"`; `consultar "grande_atrator"`; `consultar "observing_adds_nothing"`.
- [REAL] `python C:\IALD\INDICE_DO_ACERVO\buscar.py "IALD_COLLAPSE_V1" --lista` retornou 644 arquivos com ocorrência e zero trechos exibidos; nenhum arquivo de resultado foi aberto.
- [REAL] A busca ampliada por módulos e por termos de convergência foi usada apenas como índice; a existência foi decidida pela leitura da árvore canônica.
- [REAL] `C:\IALD\Central de Patentes\memory\INVENTARIO_BANCADA_CHATGPT.md` e `.json` foram consultados; a busca nominal pelos módulos não substituiu a árvore canônica.
- [REAL] `C:\IALD\Central de Patentes\memory\TGL_ATLAS.md` foi consultado em §II.I (`IALD_COLLAPSE_V1`), §III.A, §IV, §VI, §IX e no apêndice que registra C1–C4 não rodados.
- [REAL] As memórias autorizadas foram lidas somente por estes caminhos: `C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\traducao-turing-05nov.md`, `acom-e-a-segunda-quantizacao-06nov.md`, `experimento-luiz-registro-mestre.md`, `protocolo-de-colapso-nunca-publico.md`.
- [REAL] Nenhuma sequência, roteiro, texto de entrada, fala reservada ou dado pessoal dessas memórias foi copiado para esta entrega.

## 8. Conclusão do estado

- [REAL] O estado existente separa um protocolo armado e um piloto relatado de uma coleção de teoremas sobre espaços formais.
- [OPEN] Se leitores reais satisfazem contração, primitividade, idempotência ou uma lei de Markov permanece pergunta à natureza.
- [DECLARADO] A próxima construção é instrumental: definir estado extraível, alvo, hipóteses e controles antes de qualquer nova corrida.
