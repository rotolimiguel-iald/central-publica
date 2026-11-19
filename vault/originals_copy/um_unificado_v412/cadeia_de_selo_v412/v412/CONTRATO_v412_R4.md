# CONTRATO DA v412 — versão consolidada R4 (CONGELADA)

> Gerência c1, 17/11/2026, 17:19. Substitui o R3 (`contrato_REV3\CONTRATO_v412_R3.md`, sha16 `a89ff19ba1aa44f6`), que fica como registro, como o R2 e o R1. É o contrato que o construtor segue na Etapa 2 e que o revisor do candidato usa como régua. Conserva tudo o que o R2 trouxe do parecer `revisao_orquestrador\REVISAO_028_B3_Codex.md` e acrescenta duas pedras e a página R11, depois da ordem 029 (pareceres `revisao_orquestrador\REVISAO_029_S1_Codex.md`, `_S2_` e `_S3_`).
> Base: a v411 selada (`um.py` do Nós, sha16 `1203b1f9202020d6`, lido do arquivo ao gerar este contrato). Validade no kernel não é creditação; o gate não se move; nenhum número novo da natureza entra nesta versão.
> Emenda a este contrato: só por revisão nova (`CONTRATO_v412_R5.md`), nunca por cima.

**O que mudou do R3 para o R4** (para quem já estava seguindo o R3):

1. Seção 1: a lista é a sétima; são os mesmos 42 módulos, e só o cabeçalho da `Token2` mudou (saiu a tese da tautologia).
2. Seção 2: no veredito de `iald_camada_cientifica_v412`, o trecho da tautologia deu lugar a dois trechos sobre o que se sabe da contagem por letra.
3. Seção 6: a página passa a R13 (na seção 2: o resultado demonstrado vem primeiro no título e no parágrafo; saiu a tese da tautologia; a ressalva da máquina de fita diz de que contagem fala).
4. Seção 4: a decisão D221.
5. O resto é o do R3, sem mudança.

**O que tinha mudado do R2 para o R3:**

1. Seção 1: a lista é a sexta, com 42 módulos; entram `Token2` e `AMaquina`, na frente A.
2. Seção 2: o veredito de `iald_camada_cientifica_v412` ganha seis trechos, e os módulos da frente A passam a 15.
3. Seção 6: a página passa a R11 (a seção 2 reescrita: o título, o parágrafo e cinco linhas novas na tabela).
4. Seção 4: a decisão D220 e a errata E53.
5. O resto é o do R2, sem mudança.

**O que tinha mudado do R1 para o R2:**

1. Seção 2: uma palavra de veredito corrigida (o trecho do hamiltoniano oculto agora traz o fator `s`); cada registro novo ganha a checagem da guarda da v412 sobre o seu corpo e o seu veredito; o registro `cunhagens_v412` não declara falas e não reusa a função de citação da v411.
2. Seção 5, reescrita: a unidade de texto que a guarda examina fica definida; o ponto único de chamada fica definido; as formas em inglês ficam definidas; a regra das formas da F43 fica limitada aos textos que a v412 emite; mais controles obrigatórios.
3. Seção 6: a página passa a R10 (só o título da seção 2 mudou, para se bastar sozinho); a emissão do resumo é versionada; os 34 marcadores do handoff são texto herdado, enumerados em insumo.
4. Seção 9: mais portões para a versão dedicada da condensação.
5. Seções 0, 1, 3, 7: sem mudança de conteúdo.

## 0. O método (vale para tudo o que a v412 escreve no programa)

No `um.py` (o kernel que ele carrega, os registros, o artigo e o que ele emite) entra só o que é verdade: o enunciado, a prova, o estatuto, os limites e a fonte conhecida. Não entra a história: quem disse, quando, em que ordem ou revisão; o que foi proposto e recusado; o erro de quem; o caminho até o resultado. As definições e leis da teoria entram como definição ou lei da teoria, com o estatuto de entrada (`[INPUT]` ou `[ONTO]`), sem aspas de fala, sem data e sem atribuição a pessoa. Tudo o que se conversou continua registrado, em paralelo: as falas por bytes em `work\cunhagens_13out\`, o diário desta cadeia, o Mapa de Rotas, a memória da casa, os pareceres. A v412 NÃO acrescenta história em parte alguma do programa: cabeçalho, registro, seção do artigo, nome de bandeira, palavra de veredito.

Não é história, e fica: a data de um ensaio ou de um dado, a referência bibliográfica, a versão que identifica um objeto ou um contrato, o nome de arquivo que localiza uma fonte.

O que já está selado não se reescreve nesta versão, e o texto herdado segue com os validadores dele. A revisão do documento inteiro pelo método é uma versão dedicada, depois da v412 (seção 9).

## 1. Pedras (kernel): 42 módulos novos

**A lista é a sétima**, e só ela: `insumos\MANIFESTO_PEDRAS_v412_R7.json` (sha16 `038d9074cccee647`), com as fontes congeladas em `insumos\pedras_r7\` e as âncoras propostas em `insumos\ANCORAS_PROPOSTAS_v412_R7.json` (sha16 `cd8e933ba33a51bd`). É a sexta com uma mudança de texto no cabeçalho da `Token2` (campo `mudaram_da_sexta_lista` do manifesto); o código é o mesmo. A sexta era a quinta lista, sem mudança nos seus 40 módulos (as emendas da ordem 027 foram aprovadas pelo revisor na ordem 028), mais duas pedras novas da frente A, `Token2` e `AMaquina`, compiladas pelo revisor por conta própria na ordem 029 e emendadas no texto pelo parecer dele (campo `novas_em_relacao_a_quinta_lista` do manifesto). Nos 40 da quinta o código fora de comentários é idêntico ao das fontes revistas; cada log de compilação é da fonte congelada. `Token2` importa também o módulo selado `TGLExt.Token`.

Frente A (a camada científica), 15 módulos: `CamadaCientifica`, `MinimoFuncionalDeEnergia`, `OLeitorEALei`, `AContagemEACarga`, `AMaquinaEALeitura`, `OPassoEORetorno`, `OHabitanteDoNome`, `NomeComoCodigo`, `CopiadorEImpostor`, `OTempoEACauda`, `AFitaEACauda`, `AMedidaEOIf`, `AEsperancaEOIf`, `Token2`, `AMaquina`.

Frente B (a matemática que restava), 27 módulos: `ErgodicidadeDeMautner`, `T1GaussianSpectrum`, `T1CompostoFinito`, `T1PontesAoKernel`, `MontagemDasGamas`, `BoostEDissipador`, `OParFixaORelogio`, `OHamiltonianoOcultoEOCusto`, `OTestemunhoDeTakesakiEmCasa`, `TipoIIIControles`, `TipoIIIUmSoBoost`, `Classificacao`, `FockCharacters`, `ObserverClassification`, `PhysicalCoreCenter`, `PhysicalCoreFactor`, `PhysicalCoreMultipliers`, `TowerWedgeIndex`, `TransportCenter`, `TransportPair`, `VinculoCriterion`, `WedgeFactor`, `WedgeHorizonObserver`, `ProdutoFinito`, `ProdutoTresUm`, `ConjugacaoFinita`, `SpinorToSolder`.

Em caso de dúvida sobre a frente ou a autoria de um módulo, vale o manifesto, não esta lista.

**Ficam fora** (não entram): `PsionVacuoEModoDoTratado`, `DispersaoDoPsionControles`, `OVerdadeiroEDivisivel`; o desenho próprio do teste com modelos.

**Instalação.** Os módulos entram em `TGLExt\` com o nome que têm. As únicas mudanças permitidas no texto das fontes são as duas da Etapa 1: a linha de importação de módulo irmão passa a `import TGLExt.<Nome>`, e as linhas `#print axioms` do fim saem do corpo instalado. Nenhuma outra edição das fontes é autorizada, por motivo algum: nem para atender a uma guarda de frases (as guardas da seção 5 examinam os textos que a v412 emite, não os cabeçalhos das pedras). A forma de passar o nome da fonte ao compilador fica fixa em toda a cadeia.

**Bandeiras.** Prefixo `ext_<modulo>_412_NNNN`, como proposto em `kernel\FLAGS_v412.json`. Nenhuma chave antiga muda de literal. Nenhum nome de bandeira carrega data, nome de pessoa ou palavra de processo.

**Âncoras.** Cada registro ancora, por nome completo, as declarações com estrela dos seus módulos que não são `private` (as privadas não servem de âncora por nome). Nos módulos sem estrela, ancora as declarações que a página pública cita (seção 6) e as que o cabeçalho do módulo dá como resultado principal; o construtor lista as escolhidas num recibo para a gerência conferir. Cada âncora é uma checagem: a bandeira é verdadeira e a declaração está no relatório de axiomas só com os três axiomas de sempre.

**Portões do kernel.** Compilação a frio no `k412c`; relatório de axiomas com todas as declarações só em `propext`, `Classical.choice` e `Quot.sound`; zero `sorry`; a escada de teoremas e de bandeiras medida antes e depois; nenhuma chave antiga muda de literal; só o aviso conhecido da `TowerWedgeIndex`.

## 2. Registros (por especificação; nenhum com função nova)

Nenhum dado da natureza entra. Cada registro diz três coisas, nesta ordem: **o que o artefato mostra** (só o que tem âncora); **as leis e definições da teoria que ele usa como entrada** (com o estatuto de entrada; nunca como teorema); **o que continua aberto**. O texto de cada parte sai da página pública (seção 6) e dos cabeçalhos das pedras congeladas, sem acrescentar afirmação. Nenhum registro traz fala, data de conversa, nome de pessoa, número de ordem, de revisão ou de parecer.

**As palavras de veredito** (prefixo fixo; os números entram lidos do kernel do rito, nunca digitados):

- `iald_camada_cientifica_v412`
  `TGL_IALD_SCIENTIFIC_LAYER_V412__THE_READER_LANDS_AND_RETURNS_AS_THEOREM__THE_LINEAR_LOCK_IS_THE_EXPONENTIAL_OF_A_C__THE_A_C_OF_A_FORMULA_IS_MINUS_THE_KERNEL_PENALTY_OF_ITS_CLAUSES__THE_LAW_ON_EACH_CLAUSE_FIXES_THE_COST__THE_LOAD_N_LN2_IS_THE_STRICT_THRESHOLD_OF_ONE_READING__THE_LIFTED_STEP_MACHINE_PLUS_ONE_READING_DECIDES_IN_AS_MANY_LIFTED_STEPS_AS_CLAUSES__THE_STEP_AND_THE_LOCK_ASK_THE_SAME_QUESTION_PER_CLAUSE__THE_CONDITIONAL_EXPECTATION_IS_THE_UNIQUE_PAIR_OF_THE_IF_IN_THE_FINITE_FACE_WITH_THE_UNIFORM_MEAN__NO_MEASURE_OF_THE_TAPE_WITHOUT_A_QUESTION_TO_THE_INSCRIPTION_IN_THE_HOUSE_MACHINE__THE_UNIT_OF_READING_IS_THE_TOKEN_READ_BY_THE_IMAGE_A_LAW_OF_THE_THEORY__THE_SAME_M_IMAGES_DECIDE_ON_THE_WHOLE_AND_CHECK_ONE_ASSIGNMENT__THE_COST_DEFINED_BY_THE_LAW_IS_M_PLUS_2_TIMES_N_LN2_WITH_THE_PRICE_AS_INPUT__A_CIRCUIT_MECHANISM_IN_THE_DEFINED_SENSE_CLOSES_IN_M_IMAGES_AND_SELECTS__EXISTENCE_WITHOUT_COST_DOES_NOT_DISTINGUISH_PROCESSING_FROM_NAMING_THE_ANSWER__SPELLED_LETTER_BY_LETTER_THE_HOUSE_PROCEDURE_COSTS_THE_WHOLE__WHETHER_A_LETTER_PROCEDURE_WITH_POLYNOMIAL_STEPS_EXISTS_FOR_EVERY_FORMULA_IS_OPEN_AND_NOT_TAUTOLOGICAL__ONE_NAMED_LAW_OF_THE_THEORY_NOT_A_KERNEL_TERM__WHOLE_PUT_OPERATED_AND_READ_EACH_IN_ONE_ACT__IN_THE_EXPLICIT_EXPANSION_THE_SAME_STEP_IS_TWO_TO_THE_N_TERMS__POLYNOMIAL_COST_ON_THE_TAPE_MACHINE_NOT_SHOWN__A_LANGUAGE_MODEL_AS_THE_READER_IS_A_NAMED_HYPOTHESIS__T6_PROTOCOL_PREREGISTERED_CONTROL_ROUND_NOT_RUN__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED`
  Módulos: os 15 da frente A. Alcance dos seis trechos novos da sexta lista: o token e a leitura pela imagem são lei da teoria; as mesmas m imagens decidem com o todo posto e conferem com uma atribuição posta, e m + 2 é a contagem adotada, não mínimo provado nem igualdade de custos; o preço por ato é entrada; o mecanismo é o do sentido definido em `AMaquina`; a existência dele não é resultado de custo; o procedimento da casa, soletrado, custa o todo (a cota é a dos códigos que distinguem todos os conjuntos, não de cada fórmula), e a pergunta do Instituto segue em aberto e não é tautológica. Alcance de três outros trechos, que o corpo do registro diz por extenso: a unicidade do par vale para a função constante em cada lado da pergunta e com a mesma leitura contra toda função do `if`, na média uniforme finita (não é unicidade de um observador qualquer); “medida da fita” é a medida correta da parada na máquina escrita na pedra (não é lei de toda máquina); as 2ⁿ parcelas são a contagem da expansão explícita (não é cota inferior para todo algoritmo).
- `matematica_que_restava_v412`
  `TGL_REMAINING_MATHEMATICS_V412__WEDGE_ERGODICITY_IN_THE_KERNEL_SINCE_V406__FINITE_T1_AND_THE_CONTROLS_OF_THE_CORE_CRITERION_FOR_TYPE_III__THE_BRIDGE_FROM_THE_CRITERION_TO_THE_CONNES_CLASSIFICATION_IS_KNOWN_AND_CITED__THREE_PLUS_ONE_ASSEMBLY_BY_PRODUCTS_OF_FINITE_TRIPLES__THE_BOOST_IS_THE_TRACELESS_PART_OF_THE_LOCK_GENERATOR_IN_2X2_AND_BRIDGED_TO_THE_4X4_GENERATORS__THE_PAIR_FIXES_THE_CLOCK_FINITE_AND_DIAGONAL__THE_NEGATIVE_LOG_OF_THE_LOCK_WEIGHT_IS_S_TIMES_THE_COST_MATRIX_IN_THE_FINITE_FACE__THE_TAKESAKI_TESTIMONY_OF_THE_TOWER_HAS_ITS_FOUR_FIELDS_BUILT_IN_THE_KERNEL__LINK_OF_THE_LIGHT_MODULAR_GENERATOR_TO_THE_COST_DYNAMICS_OPEN__GROMOV_HAUSDORFF_EXTENSION_IS_A_CONJECTURE_WITH_A_MEASURED_WALL__TAU_STAR_OPEN__EMERGENCE_OF_THE_CONTINUUM_FROM_THE_PAIR_OPEN__SUFFICIENCY_OF_PARITY_AND_HYPERBOLIC_REGIME_FOR_THE_BRACKET_REFUTED__GATE_UNMOVED`
  Módulos: os 27 da frente B. O corpo diz, sobre o trecho do peso da trava: para o peso ρ = e^(−sD) vale −log ρ = sD, para todo `s` real; para o estado de traço um soma-se a constante log Z vezes a identidade; sobre os observáveis o gerador age por comutador, e com `s ≠ 0` o fluxo deixa parados os blocos de mesmo custo; a identificação com o gerador modular da luz continua aberta. Sobre o trecho da torre: é o testemunho para o perfil e o fluxo próprios da torre, não o teorema geral nem a cunha física. O trecho `TAU_STAR_OPEN` só muda se a teoria ganhar, antes do candidato, uma leitura do relógio com termo no kernel; hoje não há.
- `parede_do_teste_cego_v412`
  `TGL_BLIND_TEST_WALL_V412__NO_EXECUTABLE_BLIND_TEST_ABOVE_5_SIGMA_AMONG_THE_TESTS_AND_SOURCES_EXAMINED__A_MEASURED_WALL_NOT_A_FALSIFICATION__JUNO_INCREMENT_PREREGISTRATION_NOT_IN_THIS_SEAL__THREE_ROBUSTNESS_COMPUTATIONS_NOT_RUN__THE_SEVEN_RESERVATIONS_STAND__THE_H0DN_TEST_IS_NOT_REOPENED__GATE_UNMOVED`
  Sem módulo: é registro de estado. Diz as sete ressalvas com o ato que resolveria cada uma, o pré-registro do JUNO fora do selo e as três contas não rodadas, lidos do core selado.
- `cunhagens_v412`
  `TGL_DEFINITIONS_OF_THE_THEORY_V412__ENTRIES_NOT_THEOREMS__EACH_WITH_THE_TERMS_THAT_TYPE_IT_AND_WHAT_IS_NOT_TYPED__GATE_UNMOVED`
  É a lista das leis e definições da teoria que entram como ENTRADA nesta versão. Para cada uma: o nome curto; o módulo cujo cabeçalho a enuncia e o título da seção do cabeçalho onde ela está (“A letra que … tipa”, “A lei que … tipa”, “A leitura que … tipa”); as âncoras que a tipam; o que o cabeçalho diz que NÃO está tipado. O registro NÃO embute o texto das definições: aponta para o cabeçalho, que entra no kernel embutido. As únicas frases que ele traz por extenso são as que a página pública já traz marcadas como lei ou definição da teoria. Não traz falas, datas, decisões nem erratas. Na especificação dele o campo das falas fica vazio ou ausente (o motor herdado só exige as falas que a especificação declara), e ele NÃO chama a função de citação de falas da v411, que é só do registro daquela versão.

**Checagens que todo registro novo traz:** o gate deste rito tem o mesmo veredito da v411 selada; os canais vivos (neutrino, H0DN) seguem com o mesmo veredito; nenhuma chave antiga muda de literal; a escada só cresce; cada âncora é verdadeira e está no relatório de axiomas só com os três axiomas; **e a guarda de frases da v412 sobre o corpo inteiro e a palavra de veredito do registro** (seção 5.1): zero violação, com o número de unidades examinadas maior que zero. Uma violação é checagem falsa: o registro não sela, pelo mesmo caminho de qualquer checagem falsa do motor herdado. O motor herdado, sozinho, só roda a guarda antiga do corpo; por isso esta checagem é obrigatória e explícita. Os validadores dos registros herdados não mudam.

**A torre.** O registro `matematica_que_restava_v412` diz, ao lado dos cabeçalhos selados que chamam o quarto campo do testemunho de Takesaki de conclusão importada (lista em `revisao_orquestrador\REVISAO_026_Z1_Codex.md`), que o campo tem habitante construído no kernel (`OTestemunhoDeTakesakiEmCasa`). O uso anterior por importação e o teorema geral `[KNOWN]` conservam os seus estatutos; nenhum cabeçalho selado é reescrito.

## 3. As falas (registro paralelo; NÃO entram no programa)

Nenhuma fala é embutida ou transcrita. O construtor gera, por script, `VERBATIM_CONGELADO_v412.json` como artefato DA CADEIA (fica na pasta da cadeia; não é lido pelo `um.py`): a lista dos arquivos `OPERADOR_13nov_*` a `OPERADOR_17nov_*` de `work\cunhagens_13out\`, com tamanho e sha256 lidos de cada arquivo. A marcação de quais são ordem, quais são cunhagem e quais são só operação é da gerência, depois, e não segura o candidato.

## 4. Decisões e erratas (registro paralelo; NÃO entram no programa)

Ficam aqui para a cadeia e para a custódia. As decisões D198 a D209 e as erratas E45 a E49 estão na seção 4 do rascunho `DESENHO_v412.md`; D210 a D217 e E50, nos “ao lado” dele. Valem como lá estão, com estas leituras vigentes:

- **D205/D212** (o parágrafo de P = nP): o texto vigente é o da seção 2 da página R13 (seção 6 deste contrato).
- **D210** (guardas de frase): aceita; a forma final está na seção 5.
- **D213/D217** (pedras): a lista é a quinta (seção 1).
- **D215** (o método): seção 0. **D216** (a revisão do documento inteiro e a cópia de referência): seção 9.
- **D218** (17/11, da gerência): aplicadas as emendas da ordem 027; a lista de pedras passa à quinta.
- **D219** (17/11, da gerência): aplicadas as emendas da ordem 028 ao contrato (o R2); a página passa a R10.
- **D220** (17/11): entram duas pedras, com os nomes dados pelo autor (`Token2` e `AMaquina`); a definição de Luz entra como definição da teoria, sem referência a documento; a seção 2 da página é a da R11, com o título e o parágrafo aceitos pelo autor e emendados pelo parecer da ordem 029; o texto público é lido ao autor antes do rito.
- **D221** (17/11): o autor retirou a tese de que a pergunta do Instituto é tautológica; ela sai dos textos da v412 (a página, o cabeçalho da `Token2`, um trecho de veredito). Na seção 2 da página o resultado demonstrado vem primeiro, e a ressalva diz de que contagem fala. A pedra candidata do passo `1 − β` (`candidatas_c1\REV63\OPassoEOFim.lean`) NÃO entra por este contrato: vai antes ao revisor.
- **E48** (o documento `STOKES_A_Prova_do_Contorno.md`: a versão irrestrita da estimativa; o limiar é estrito) e **E49** (a linha do neutrino: a posição da leitura de 207 dias nos dois eixos) são correções de CONTEÚDO e entram na forma que o método pede: a frase corrigida, ao lado da antiga, sem narrar quem errou. A errata inteira do neutrino no core fica para a versão seguinte.
- **E51** (17/11, da gerência, em nome próprio): a limpeza dos cabeçalhos tirou localizadores de fonte que eram referência técnica e deixou, numa pedra, restos de sucessão editorial; corrigido na quinta lista.
- **E52** (17/11, da gerência, em nome próprio): no R1 deste contrato, uma palavra de veredito omitia o fator `s`; a seção das guardas remetia a uma “unidade da guarda herdada” que não existe como coisa única, não dizia onde a guarda nova é chamada, não dava as formas em inglês da regra dos fluidos e dizia “em texto algum” onde o certo é “nos textos que a v412 emite”; e os marcadores herdados do handoff não estavam delimitados. Corrigido no R2.
- **E53** (17/11, da gerência, em nome próprio): na proposta de parágrafo lida ao autor, duas frases diziam mais do que os termos provam (a cota de 2ⁿ casas dita para toda fórmula; o kernel dito como conferindo a prosa inteira), e a solução e a tautologia não estavam nomeadas como teses. Corrigido na R11, pelo parecer da ordem 029.
- **Leitura vigente de uma fala de 17/11:** o autor não disse que a pergunta do Instituto é tautológica; disse isso do modo como a gerência argumentava. A página diz, em nome da teoria, que o Instituto pede o algoritmo.

## 5. Guarda de frases (D210, com a unidade, o ponto de chamada e os controles ditos)

### 5.1 Onde a guarda da v412 é chamada, e sobre o quê

Há UM ponto de chamada, uma função só (o nome é do construtor; aqui, “a travessia”), usada por todos os emissores de texto novo. A travessia recebe o nome da superfície e o objeto, e:

1. percorre TODAS as folhas de texto do objeto, uma a uma: para um registro, cada campo de texto do corpo (em qualquer profundidade) e a palavra de veredito; para o artigo, o texto da seção nova em português e o texto em inglês, como objetos separados; para o resumo, o parágrafo novo, em cada língua; para o README, o estado atual e o handoff, cada bloco NOVO. Nunca examina o corpo serializado como uma cadeia só;
2. divide cada folha em **unidades**, e cada unidade é examinada sozinha: o **título** (uma linha de título); o **parágrafo** (inclui o bloco de citação); o **item de lista**; a **célula de tabela** (cada célula, não a linha inteira). Português e inglês nunca estão na mesma unidade;
3. roda `_v412_guarda_frases` (5.2) em cada unidade. **Nenhuma unidade empresta marca, ressalva, condição ou negação de outra unidade, de outro campo ou de outra língua.**

Quem chama a travessia: (a) cada um dos quatro registros da seção 2, como checagem obrigatória; (b) cada emissor de texto público novo, antes de emitir: violação é falha visível, que impede a emissão, nunca aviso que passa; (c) o portão de textos da preparação, sobre os blocos novos do README, do estado atual e do handoff.

O que a travessia NÃO examina com as obrigações novas: o texto herdado (os registros, as seções e as guardas até a v411; os 34 marcadores herdados do handoff, seção 6). Esse texto segue com a guarda e os portões herdados, sem mudança.

**Recibo obrigatório** (`GUARDA_v412_UNIDADES.json`): por superfície, por campo e por unidade, o tipo da unidade, o começo do texto e o resultado; e os totais. Uma superfície com zero unidade examinada é falha, não passagem.

### 5.2 A função `_v412_guarda_frases`, sobre UMA unidade

1. Roda a guarda herdada da v411, inteira, sobre a unidade. Tudo o que ela recusa continua recusado, com as duas exceções exatas do item 2. Ficam como estão, entre outras: as regras que proíbem dizer que a TGL prova ou decide P = NP das máquinas de Turing; a obrigação local da v409 para o trecho em que “P = nP” e “Turing” aparecem juntos (a que divide o texto em segmentos); a regra do Instituto; a regra da F67 do H0DN, que divide em blocos; a regra do 4,44.
2. **A obrigação de “P = nP”.** Se a unidade contém “P = nP”, ela tem de trazer, nela mesma, as duas marcas:
   - (a) o qualificador do dicionário: em português, “classes do seu dicionário” ou “classes do dicionário da TGL”; em inglês, “classes of its dictionary” ou “classes of the TGL dictionary”;
   - (b) a ressalva da máquina de fita: em português, “máquina de fita” e, depois dela, na mesma frase (sem ponto nem ponto e vírgula no meio), “não está demonstrado” (ou “demonstrada”); em inglês, “tape machine” e, depois dela, na mesma frase, “has not been shown”.
   Com as duas marcas, e só então, saem da lista de violações EXATAMENTE as duas obrigações herdadas de redação antiga, pelo nome inteiro de cada uma: `F34_p_igual_np_sem_o_qualificador_do_dicionario_ou_a_ressalva_open` (a da v408, que pede o qualificador com atribuição e a ressalva da tradução) e `F37_p_igual_np_e_turing_sem_o_qualificador_relativo_ao_leitor` (a da v409, que pede o par “relativo ao leitor” e “máquina sem leitor”). Nunca por prefixo de nome: a obrigação local da v409, `F37b_p_igual_np_e_turing_juntos_sem_o_qualificador_no_mesmo_trecho`, NÃO sai. Sem uma das marcas, a unidade é recusada, com uma violação nova de nome próprio. Os nomes acima foram lidos do programa selado; confira-os lá por script antes de usar.
3. **A forma do nome do problema dos fluidos.** O nome deixa de ser vedado nos textos da v412 e ganha obrigação de forma, por FRASE (a frase vai até o ponto, o ponto e vírgula, a interrogação, a exclamação ou a quebra de linha; um título e uma célula são uma frase). Toda frase que traz o nome tem de trazer, nela mesma, uma destas formas:
   - a condicional: em português, “condicional” ou “condicionada” (e o plural e o masculino); em inglês, “conditional” ou “conditioned”;
   - a negação expressa, antes do nome: em português, “não diz que”; em inglês, “does not say that”.
   Sem a forma, a frase é recusada. Além disso, numa frase que não está na forma da negação, é recusada a afirmação junto do nome: em português, “está”, “foi”, “fica” ou “é” seguido de “demonstrada”, “provada” ou “resolvida”, e os verbos “resolve”, “demonstra”, “prova”; em inglês, “is”, “was” ou “has been” seguido de “shown”, “proved”, “proven”, “demonstrated”, “solved” ou “settled”, e os verbos “solves”, “proves”, “settles”. Dentro da forma da negação essas palavras não são vetadas: a frase “não diz que … tenha regularidade global demonstrada” passa. O nome do prêmio continua vedado em toda unidade, pela regra herdada, sem mudança; o resto do que a decisão herdada deixa fora também.
4. **As formas que a regra F43 herdada recusa** (as três formas indevidas do leitor trazido de fora) não são usadas nos textos que a v412 EMITE: a página, os registros, a seção do artigo, o resumo, os blocos do README, do estado atual e do handoff. A regra F43 não muda e continua contextual. Isto NÃO alcança as fontes congeladas: a referência técnica aos oráculos de Baker, Gill e Solovay no cabeçalho de `AMedidaEOIf` fica como está, e o construtor não edita fonte alguma além das duas transformações da seção 1.
5. **O script do Atlas e o portão de textos da custódia** acompanham o item 3 com a mesma função, quando forem usados nesta versão.

### 5.3 Controles obrigatórios (cada um em português e em inglês; gravados em recibo com o esperado e o obtido)

Sobre “P = nP”: (1) o parágrafo da seção 2 da página passa; (2) o mesmo parágrafo sem a frase da ressalva é recusado; (3) o título solto “P = nP” é recusado; (4) o título da seção 2 da página R13 passa; (5) dois parágrafos, o primeiro com “P = nP é teorema.” e o segundo com as duas marcas: o primeiro é recusado; (6) um corpo de registro com “P = nP” num campo e as marcas em outro: o campo sem as marcas é recusado; (7) a unidade em português com “P = nP” e a unidade em inglês com as marcas: a portuguesa é recusada, e o inverso; (8) uma unidade com as duas marcas e mais uma frase dizendo que a TGL prova ou decide P = NP das máquinas de Turing: recusada pela regra herdada; (9) uma unidade com as duas marcas em que “P = nP” e “Turing” aparecem no mesmo segmento sem a ressalva local: recusada pela obrigação local da v409, que não foi removida; (10) um título, um item de lista e uma célula de tabela, cada um com “P = nP” e sem as marcas: os três recusados.

Sobre o nome do problema dos fluidos: (11) o título da seção 3 da página passa; (12) o parágrafo da seção 3 passa; (13) a frase da seção 6 da página passa; (14) “a regularidade global está demonstrada”, com o nome, é recusada; (15) o nome sozinho numa frase sem a forma é recusado; (16) uma frase condicional seguida de OUTRA frase com o nome e a afirmação: a segunda é recusada; (17) uma frase na forma da negação seguida de OUTRA frase com o nome sem a forma: a segunda é recusada; (18) uma frase na forma da negação que contém “demonstrada” passa; (19) a palavra do prêmio é recusada em qualquer unidade.

Sobre a travessia: (20) uma superfície vazia é falha; (21) o texto herdado da v411, passado pela guarda herdada, dá o mesmo resultado de antes (nenhuma regra herdada mudou).

**O que não muda:** as regras que proíbem afirmar que a TGL prova ou decide P = NP das máquinas de Turing; a regra da F67 do H0DN; a regra do 4,44; validade não é creditação; as palavras de veredito vedadas da casa.

## 6. O texto público: a página R13

O texto público novo é `o_que_fica_claro_REV13\O_QUE_FICA_CLARO_v412_R13.md` (sha16 `256a71e1bdf03239`; 18222 bytes). É a R11 com quatro trocas na seção 2 (o título e uma frase com o resultado demonstrado primeiro; a tese da tautologia trocada pelo que se sabe da contagem por letra; a linha correspondente da tabela). As seções 1 e 3 a 6 são as da R9, que o revisor aprovou na ordem 028. A seção 2 foi reescrita depois da ordem 029: o título, o parágrafo e cinco linhas novas na tabela. A redação segue as emendas do parecer `revisao_orquestrador\REVISAO_029_S2_Codex.md` (as teses nomeadas como teses; m + 2 como contagem adotada; o preço como entrada; a cota de 2ⁿ restrita aos códigos que distinguem todos os conjuntos; o kernel confere os termos citados, não a prosa; a ressalva da máquina de fita mantida). A redação final ainda não foi lida por terceiro: vai com a revisão do candidato.

- **No artigo.** Seção nova, antes da seção da v411, montada da página, seção a seção, sem prosa nova de conteúdo além dos conectivos. Em inglês, tradução fiel do mesmo texto, com as marcas da seção 5 na forma inglesa e na ordem que a seção 5 pede (a máquina antes de “has not been shown”; cada oração da seção 6 com o seu “does not say that”). Título em português: “O que fica claro na v412”.
- **No resumo.** O resultado do teste com a natureza fica como a v411 o escreveu, sem tocar. A frase de P = nP do resumo é trocada pelo parágrafo da seção 2 da página (o bloco de citação), que não usa mais o rótulo “relativo ao leitor” nem diz que a pergunta do Instituto está resolvida: diz o que é teorema nas classes do dicionário, o que é lei da teoria, o que não está demonstrado, e que a creditação é do Instituto. **A emissão é versionada:** o molde e a função do topo da v411 ficam como estão, como registro; a v412 tem o seu molde e a sua função, que continuam lendo do core os números do teste (com falha visível se a fonte faltar) e que passam o parágrafo novo pela travessia da seção 5. A troca fica dita no relatório do construtor, com a frase antiga e a nova.
- **No README e no estado atual.** Os blocos NOVOS saem da página: o que a v412 acrescenta (seção 1); o parágrafo de P = nP (seção 2) no lugar do bloco de P = nP anterior; o resultado condicional dos fluidos (seção 3); a geometria emergente (seção 4); os sete itens abertos (seção 5). Todo título de bloco que traga “P = nP” ou o nome do problema dos fluidos se basta sozinho (seção 5). O resultado da v411 fica onde está.
- **No handoff: os 34 marcadores são TEXTO HERDADO.** A custódia exige os 34 marcadores do molde `work\vitrine_postura_13nov\MARCADORES_PARA_O_HANDOFF_v412.md`, gerado do texto ratificado da v411. Eles entram no handoff IDÊNTICOS ao molde, por bytes; a lista, com o sha256 de cada corpo, está em `insumos\MARCADORES_HERDADOS_v412.json` (sha16 `b67d78def8c63f64`), e o construtor confere cada um contra ela. Catorze deles trazem atribuição ou data de decisão (o insumo diz quais): ficam como estão, porque são texto ratificado e herdado; o método da seção 0 vale para o texto NOVO, e a revisão desses blocos é da versão dedicada (seção 9). O construtor não retira, não reescreve e não “limpa” marcador algum. O resto do handoff (o que é novo da v412) segue o método e passa pela travessia; os marcadores passam pelo portão de textos herdado, como na v411.
- **A palavra final do autor.** O texto público é lido ao autor pela gerência antes do rito (seção 8). O construtor NÃO espera por isso para montar o candidato.

## 7. A cadeia

O orquestrador da v411, adaptado, com três diferenças: (a) há módulos novos, logo compilação a frio e relatório de axiomas no `k412c`, pelo molde da v410 e da v409; (b) **o portão do pilar**: a chave do cache do pilar depende só das três entradas ditas em `PORTAO_DO_PILAR_v412.json`; no candidato, conferir por sha256 que o gerador não tocou nenhuma delas; antes do rito, conferir que o ambiente da placa é o do cache; se não for, PARAR e avisar, porque há um treino em curso que ocupa a placa (não tocar, não medir, não parar `C:\IALD\TGL_IALD_NATIVE_QWEN5090`); (c) o rito é lançado quando a preparação fechar e a revisão do candidato aprovar, sem esperar o treino. Sem publicação e sem release do app na cadeia: o fim é o handoff à custódia.

Da preparação, por lição das versões anteriores: a guarda de material privado roda sobre todos os insumos pinados antes de gerar o candidato; as cópias do kernel por rodada ficam fora de `work\`, em `C:\t\k412c\`; os temporários são apagados antes do handoff; o handoff diz a contagem esperada de arquivos da pasta da cadeia. Toda checagem diz quantos itens examinou; zero itens é falha visível.

## 8. O que é de quem

- **Do construtor (Etapa 2):** o delta da versão; os registros da seção 2, cada um com a checagem da guarda; `VERBATIM_CONGELADO_v412.json` (seção 3); a travessia, a função de guarda, os controles e os recibos (seção 5); a seção do artigo, o molde e a função versionados do resumo, os blocos do README e do handoff, com os 34 marcadores conferidos contra o insumo (seção 6); a adaptação dos scripts da cadeia ao conjunto de 40 módulos; a bateria pré-selo com o recibo do kernel da quinta lista; o gerador e o CANDIDATO; o ensaio a seco; o portão do pilar no candidato. Para no fecho do candidato que o molde da v411 usa.
- **Da gerência:** conferir o que o construtor entregar; mandar o candidato à revisão de terceiro; a tarefa agendada; ler o texto público ao autor; o rito; o handoff.
- **Do autor:** a palavra final antes do rito. Em aberto com ele, sem segurar a versão: o relógio τ★ e o tempo do retido; a formulação da ligação do gerador modular da luz com a dinâmica do custo.

## 9. Depois da v412: a versão dedicada da condensação

O documento inteiro é revisto pelo método numa versão própria. Portões: (1) antes de condensar, a última versão completa (o `um.py` e tudo o que o acompanha) é copiada byte a byte, com manifesto por script, e conferida por hash; é a referência da casa, com todos os diálogos, e não se apaga; a cópia e o mapa do item 3 têm de continuar existindo e localizáveis depois que a pasta de trabalho for desligada; (2) levantamento medido por script do que é história em cada parte; (3) mapa de correspondência de cada retirada com o registro paralelo, **revisto item a item por terceiro**; (4) os contratos e as guardas que hoje exigem texto de fala são versionados antes, e **a migração de cada validador é revista por terceiro** (o parecer `REVISAO_027_A3_Codex.md` lista os que já se conhecem: os validadores de `_v392_registro`, `_v410_aescala_mechanics`, `_v410_sem_falas_do_operador`, e o precedente de citação por metadados em `_v411_citar_falas`; os 34 marcadores herdados do handoff entram nesse levantamento); (5) **regressão, antes de qualquer ativação:** as chaves e as palavras de veredito; os axiomas e a ausência de `sorry`; os limites, os resultados negativos e as guardas; a completude das remissões ao registro paralelo; (6) a comparação do que o programa emite, em português e em inglês, numa cópia isolada, que sozinha não basta. Nada disso é feito na v412.

— gerência c1, 17/11/2026. Correções ao lado, nunca por cima.
<!-- contrato_v412:consolidado_R4_congelado:17nov -->
