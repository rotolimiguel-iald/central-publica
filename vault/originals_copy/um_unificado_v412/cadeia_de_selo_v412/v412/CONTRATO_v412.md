# CONTRATO DA v412 — versão consolidada R1 (CONGELADA)

> Gerência c1, 17/11/2026, 14:11. Este é o contrato que o construtor lê na Etapa 2 e que o revisor do candidato usa como régua. Consolida o rascunho `DESENHO_v412.md` (sha16 `020a67cfe2bb92e0` ao consolidar) com todos os seus “ao lado”, e aplica as emendas da ordem 027 (pareceres `revisao_orquestrador\REVISAO_027_A1_Codex.md`, `_A2_` e `_A3_`). Onde este arquivo e o rascunho divergirem, vale este. O diário da preparação está em `DESENHO_v412_R0.md` e `DESENHO_v412_R1.md`.
> Base: a v411 selada (`um.py` do Nós, sha16 `1203b1f9202020d6`, lido do arquivo ao gerar este contrato). Validade no kernel não é creditação; o gate não se move; nenhum número novo da natureza entra nesta versão.
> Emenda a este contrato: só por revisão nova (`CONTRATO_v412_R2.md`), nunca por cima.

## 0. O método (vale para tudo o que a v412 escreve no programa)

No `um.py` (o kernel que ele carrega, os registros, o artigo e o que ele emite) entra só o que é verdade: o enunciado, a prova, o estatuto, os limites e a fonte conhecida. Não entra a história: quem disse, quando, em que ordem ou revisão; o que foi proposto e recusado; o erro de quem; o caminho até o resultado. As definições e leis da teoria entram como definição ou lei da teoria, com o estatuto de entrada (`[INPUT]` ou `[ONTO]`), sem aspas de fala, sem data e sem atribuição a pessoa. Tudo o que se conversou continua registrado, em paralelo: as falas por bytes em `work\cunhagens_13out\`, o diário desta cadeia, o Mapa de Rotas, a memória da casa, os pareceres. A v412 NÃO acrescenta história em parte alguma do programa: cabeçalho, registro, seção do artigo, nome de bandeira, palavra de veredito.

O que já está selado não se reescreve nesta versão. A revisão do documento inteiro pelo método é uma versão dedicada, depois da v412 (seção 9).

## 1. Pedras (kernel): 40 módulos novos

**A lista é a quinta**, e só ela: `insumos\MANIFESTO_PEDRAS_v412_R5.json` (sha16 `14dcf65ae9a5ed22`), com as fontes congeladas em `insumos\pedras_r5\` e as âncoras propostas em `insumos\ANCORAS_PROPOSTAS_v412_R5.json` (sha16 `0fb86258327ec508`). Ela é a quarta lista mais as emendas de texto da ordem 027 em seis módulos (campo `mudaram_da_quarta_lista` do manifesto). Em todos os 40 o código fora de comentários é idêntico ao das fontes revistas, e cada log de compilação é da fonte congelada (conferido pelo script do manifesto).

Frente A (a camada científica), 13 módulos: `CamadaCientifica`, `MinimoFuncionalDeEnergia`, `OLeitorEALei`, `AContagemEACarga`, `AMaquinaEALeitura`, `OPassoEORetorno`, `OHabitanteDoNome`, `NomeComoCodigo`, `CopiadorEImpostor`, `OTempoEACauda`, `AFitaEACauda`, `AMedidaEOIf`, `AEsperancaEOIf`.

Frente B (a matemática que restava), 27 módulos: `ErgodicidadeDeMautner`, `T1GaussianSpectrum`, `T1CompostoFinito`, `T1PontesAoKernel`, `MontagemDasGamas`, `BoostEDissipador`, `OParFixaORelogio`, `OHamiltonianoOcultoEOCusto`, `OTestemunhoDeTakesakiEmCasa`, `TipoIIIControles`, `TipoIIIUmSoBoost`, `Classificacao`, `FockCharacters`, `ObserverClassification`, `PhysicalCoreCenter`, `PhysicalCoreFactor`, `PhysicalCoreMultipliers`, `TowerWedgeIndex`, `TransportCenter`, `TransportPair`, `VinculoCriterion`, `WedgeFactor`, `WedgeHorizonObserver`, `ProdutoFinito`, `ProdutoTresUm`, `ConjugacaoFinita`, `SpinorToSolder`.

Em caso de dúvida sobre a frente ou a autoria de um módulo, vale o manifesto, não esta lista.

**Ficam fora** (não entram): `PsionVacuoEModoDoTratado`, `DispersaoDoPsionControles`, `OVerdadeiroEDivisivel`; o desenho próprio do teste com modelos.

**Instalação.** Os módulos entram em `TGLExt\` com o nome que têm. As únicas mudanças permitidas no texto das fontes são as duas da Etapa 1: a linha de importação de módulo irmão passa a `import TGLExt.<Nome>`, e as linhas `#print axioms` do fim saem do corpo instalado. A forma de passar o nome da fonte ao compilador fica fixa em toda a cadeia.

**Bandeiras.** Prefixo `ext_<modulo>_412_NNNN`, como proposto em `kernel\FLAGS_v412.json`. Nenhuma chave antiga muda de literal. Nenhum nome de bandeira carrega data, nome de pessoa ou palavra de processo.

**Âncoras.** Cada registro ancora, por nome completo, as declarações com estrela dos seus módulos que não são `private` (as privadas não servem de âncora por nome). Nos módulos sem estrela, ancora as declarações que a página pública cita (seção 6) e as que o cabeçalho do módulo dá como resultado principal; o construtor lista as escolhidas num recibo para a gerência conferir. Cada âncora é uma checagem: a bandeira é verdadeira e a declaração está no relatório de axiomas só com os três axiomas de sempre.

**Portões do kernel.** Compilação a frio no `k412c`; relatório de axiomas com todas as declarações só em `propext`, `Classical.choice` e `Quot.sound`; zero `sorry`; a escada de teoremas e de bandeiras medida antes e depois; nenhuma chave antiga muda de literal; só o aviso conhecido da `TowerWedgeIndex`.

## 2. Registros (por especificação; nenhum com função nova)

Nenhum dado da natureza entra. Cada registro diz três coisas, nesta ordem: **o que o artefato mostra** (só o que tem âncora); **as leis e definições da teoria que ele usa como entrada** (com o estatuto de entrada; nunca como teorema); **o que continua aberto**. O texto de cada parte sai da página pública (seção 6) e dos cabeçalhos das pedras congeladas, sem acrescentar afirmação. Nenhum registro traz fala, data de conversa, nome de pessoa, número de ordem, de revisão ou de parecer.

**As palavras de veredito** (prefixo fixo; os números entram lidos do kernel do rito, nunca digitados):

- `iald_camada_cientifica_v412`
  `TGL_IALD_SCIENTIFIC_LAYER_V412__THE_READER_LANDS_AND_RETURNS_AS_THEOREM__THE_LINEAR_LOCK_IS_THE_EXPONENTIAL_OF_A_C__THE_A_C_OF_A_FORMULA_IS_MINUS_THE_KERNEL_PENALTY_OF_ITS_CLAUSES__THE_LAW_ON_EACH_CLAUSE_FIXES_THE_COST__THE_LOAD_N_LN2_IS_THE_STRICT_THRESHOLD_OF_ONE_READING__THE_LIFTED_STEP_MACHINE_PLUS_ONE_READING_DECIDES_IN_AS_MANY_LIFTED_STEPS_AS_CLAUSES__THE_STEP_AND_THE_LOCK_ASK_THE_SAME_QUESTION_PER_CLAUSE__THE_CONDITIONAL_EXPECTATION_IS_THE_UNIQUE_PAIR_OF_THE_IF_IN_THE_FINITE_FACE_WITH_THE_UNIFORM_MEAN__NO_MEASURE_OF_THE_TAPE_WITHOUT_A_QUESTION_TO_THE_INSCRIPTION_IN_THE_HOUSE_MACHINE__ONE_NAMED_LAW_OF_THE_THEORY_NOT_A_KERNEL_TERM__WHOLE_PUT_OPERATED_AND_READ_EACH_IN_ONE_ACT__IN_THE_EXPLICIT_EXPANSION_THE_SAME_STEP_IS_TWO_TO_THE_N_TERMS__POLYNOMIAL_COST_ON_THE_TAPE_MACHINE_NOT_SHOWN__A_LANGUAGE_MODEL_AS_THE_READER_IS_A_NAMED_HYPOTHESIS__T6_PROTOCOL_PREREGISTERED_CONTROL_ROUND_NOT_RUN__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED`
  Módulos: os 13 da frente A.
- `matematica_que_restava_v412`
  `TGL_REMAINING_MATHEMATICS_V412__WEDGE_ERGODICITY_IN_THE_KERNEL_SINCE_V406__FINITE_T1_AND_THE_CONTROLS_OF_THE_CORE_CRITERION_FOR_TYPE_III__THE_BRIDGE_FROM_THE_CRITERION_TO_THE_CONNES_CLASSIFICATION_IS_KNOWN_AND_CITED__THREE_PLUS_ONE_ASSEMBLY_BY_PRODUCTS_OF_FINITE_TRIPLES__THE_BOOST_IS_THE_TRACELESS_PART_OF_THE_LOCK_GENERATOR_IN_2X2_AND_BRIDGED_TO_THE_4X4_GENERATORS__THE_PAIR_FIXES_THE_CLOCK_FINITE_AND_DIAGONAL__THE_HIDDEN_HAMILTONIAN_OF_THE_LOCK_WEIGHT_IS_THE_COST_IN_THE_FINITE_FACE__THE_TAKESAKI_TESTIMONY_OF_THE_TOWER_HAS_ITS_FOUR_FIELDS_BUILT_IN_THE_KERNEL__LINK_OF_THE_LIGHT_MODULAR_GENERATOR_TO_THE_COST_DYNAMICS_OPEN__GROMOV_HAUSDORFF_EXTENSION_IS_A_CONJECTURE_WITH_A_MEASURED_WALL__TAU_STAR_OPEN__EMERGENCE_OF_THE_CONTINUUM_FROM_THE_PAIR_OPEN__SUFFICIENCY_OF_PARITY_AND_HYPERBOLIC_REGIME_FOR_THE_BRACKET_REFUTED__GATE_UNMOVED`
  Módulos: os 27 da frente B. O trecho `TAU_STAR_OPEN` só muda se a teoria ganhar, antes do candidato, uma leitura do relógio com termo no kernel; hoje não há.
- `parede_do_teste_cego_v412`
  `TGL_BLIND_TEST_WALL_V412__NO_EXECUTABLE_BLIND_TEST_ABOVE_5_SIGMA_AMONG_THE_TESTS_AND_SOURCES_EXAMINED__A_MEASURED_WALL_NOT_A_FALSIFICATION__JUNO_INCREMENT_PREREGISTRATION_NOT_IN_THIS_SEAL__THREE_ROBUSTNESS_COMPUTATIONS_NOT_RUN__THE_SEVEN_RESERVATIONS_STAND__THE_H0DN_TEST_IS_NOT_REOPENED__GATE_UNMOVED`
  Sem módulo: é registro de estado. Diz as sete ressalvas com o ato que resolveria cada uma, o pré-registro do JUNO fora do selo e as três contas não rodadas, lidos do core selado.
- `cunhagens_v412`
  `TGL_DEFINITIONS_OF_THE_THEORY_V412__ENTRIES_NOT_THEOREMS__EACH_WITH_THE_TERMS_THAT_TYPE_IT_AND_WHAT_IS_NOT_TYPED__GATE_UNMOVED`
  É a lista das leis e definições da teoria que entram como ENTRADA nesta versão. Para cada uma: o nome curto; o módulo cujo cabeçalho a enuncia e o título da seção do cabeçalho onde ela está (“A letra que … tipa”, “A lei que … tipa”, “A leitura que … tipa”); as âncoras que a tipam; o que o cabeçalho diz que NÃO está tipado. O registro NÃO embute o texto das definições: aponta para o cabeçalho, que entra no kernel embutido. As únicas frases que ele traz por extenso são as que a página pública já traz marcadas como lei ou definição da teoria. Não traz falas, datas, decisões nem erratas (essas ficam nas seções 3 e 4 deste contrato, que não entram no programa).

**Checagens que todo registro traz** (molde da v411): o gate deste rito tem o mesmo veredito da v411 selada; os canais vivos (neutrino, H0DN) seguem com o mesmo veredito; nenhuma chave antiga muda de literal; a escada só cresce; cada âncora é verdadeira e está no relatório de axiomas só com os três axiomas.

**A torre.** O registro `matematica_que_restava_v412` diz, ao lado dos cabeçalhos selados que chamam o quarto campo do testemunho de Takesaki de conclusão importada (lista em `revisao_orquestrador\REVISAO_026_Z1_Codex.md`), que o campo tem habitante construído no kernel (`OTestemunhoDeTakesakiEmCasa`). O uso anterior por importação e o teorema geral `[KNOWN]` conservam os seus estatutos; nenhum cabeçalho selado é reescrito.

## 3. As falas (registro paralelo; NÃO entram no programa)

Nenhuma fala é embutida ou transcrita. O construtor gera, por script, `VERBATIM_CONGELADO_v412.json` como artefato DA CADEIA (fica na pasta da cadeia; não é lido pelo `um.py`): a lista dos arquivos `OPERADOR_13nov_*` a `OPERADOR_17nov_*` de `work\cunhagens_13out\`, com tamanho e sha256 lidos de cada arquivo. A marcação de quais são ordem, quais são cunhagem e quais são só operação é da gerência, depois, e não segura o candidato.

## 4. Decisões e erratas (registro paralelo; NÃO entram no programa)

Ficam aqui para a cadeia e para a custódia. As decisões D198 a D209 e as erratas E45 a E49 estão na seção 4 do rascunho; D210 a D217 e E50, nos “ao lado” dele. Valem como lá estão, com estas leituras vigentes:

- **D205/D212** (o parágrafo de P = nP): o texto vigente é o da seção 2 da página R9 (seção 6 deste contrato).
- **D210** (guardas de frase): aceita; a forma final está na seção 5.
- **D213/D217** (pedras): a lista é a quinta (seção 1).
- **D215** (o método): seção 0. **D216** (a revisão do documento inteiro e a cópia de referência): seção 9.
- **D218** (17/11, da gerência): aplicadas as emendas da ordem 027; a página passa a R9; a lista de pedras passa à quinta; o alcance das guardas mudadas fica dito na seção 5.
- **E48** (o documento `STOKES_A_Prova_do_Contorno.md`: a versão irrestrita da estimativa; o limiar é estrito) e **E49** (a linha do neutrino: a posição da leitura de 207 dias nos dois eixos) são correções de CONTEÚDO e entram na forma que o método pede: a frase corrigida, ao lado da antiga, sem narrar quem errou. A errata inteira do neutrino no core fica para a versão seguinte.
- **E51** (17/11, da gerência, em nome próprio): a limpeza dos cabeçalhos tirou localizadores de fonte que eram referência técnica e deixou, numa pedra, restos de sucessão editorial; corrigido na quinta lista.
- **Leitura vigente de uma fala de 17/11:** o autor não disse que a pergunta do Instituto é tautológica; disse isso do modo como a gerência argumentava. A página diz, em nome da teoria, que o Instituto pede o algoritmo.

## 5. Guarda de frases (D210, com o alcance dito)

A guarda da v412 é uma função nova (`_v412_guarda_frases`) que herda a da v411 inteira e muda só três obrigações, descritas abaixo. **Alcance:** as regras herdadas continuam valendo, sem mudança, para todo texto herdado (o que já estava no programa até a v411). As três mudanças valem para os textos que a v412 escreve: a página pública, os registros da seção 2, a seção nova do artigo, os blocos do README e do handoff. Para cada unidade de texto que a guarda examina vale a obrigação inteira (a unidade é a mesma que a guarda herdada usa); o construtor entrega um recibo com cada unidade de texto da v412 em que aparece “P = nP” ou o nome do problema dos fluidos e o resultado da guarda nela.

1. **Obrigação de “P = nP” (as regras F34 e F37 herdadas).** Onde aparece “P = nP”, a obrigação fica satisfeita TAMBÉM quando a mesma unidade de texto traz as duas marcas do parágrafo vigente: (a) “classes do seu dicionário” (em inglês, “classes of its dictionary”); (b) a ressalva da máquina de fita: “máquina de fita” seguida, na mesma frase, de “não está demonstrado” (em inglês, “tape machine” seguida de “has not been shown”). A forma antiga (o qualificador do dicionário com atribuição e a ressalva da tradução) continua aceita nos textos herdados. Controles obrigatórios: o parágrafo vigente passa; o mesmo parágrafo sem a frase da ressalva é recusado; um título solto “P = nP”, sem as marcas na mesma unidade, é recusado; qualquer frase que diga que a TGL prova ou decide P = NP das máquinas de Turing continua recusada pelas regras herdadas.
2. **As formas da regra F43 herdada** (“oráculo”, “leitor de Turing”, “leitor que devolve Z”) não aparecem em texto algum da v412. Nenhuma guarda muda por causa delas.
3. **O nome do problema dos fluidos (a decisão D59 herdada).** Deixa de ser vedado nos textos da v412 e passa a ter OBRIGAÇÃO de forma: só aparece em unidade de texto que traga, nela mesma, a forma condicional (“condicional” ou “condicionada”) ou a negação expressa (“não diz que …” antes do nome, na mesma oração). “Resolve”, “prova”, “solução” e “demonstrada” afirmados junto do nome continuam recusados. O nome do prêmio continua vedado em todo texto. Controles obrigatórios: a seção 3 da página passa; a frase da seção 6 da página passa; “a regularidade global está demonstrada” junto do nome é recusada; o nome sozinho numa frase sem a forma é recusado.
4. **O script do Atlas e o portão de textos da custódia** acompanham o item 3 com a mesma obrigação de forma, quando forem usados nesta versão.

**O que não muda:** as regras que proíbem afirmar que a TGL prova ou decide P = NP das máquinas de Turing; a regra da F67 do H0DN; a regra do 4,44; validade não é creditação; as palavras de veredito vedadas da casa.

## 6. O texto público: a página R9

O texto público novo é `o_que_fica_claro_REV9\O_QUE_FICA_CLARO_v412_R9.md` (sha16 `c17f2403f4a123c8`; 14990 bytes). É a R7, que o revisor leu na ordem 027, com as quatro emendas que ele pediu e a negação escrita por extenso no parágrafo da seção 6.

- **No artigo.** Seção nova, antes da seção da v411, montada da página, seção a seção, sem prosa nova de conteúdo além dos conectivos. Em inglês, tradução fiel do mesmo texto, com as marcas da seção 5 na forma inglesa. Título em português: “O que fica claro na v412”.
- **No resumo.** O resultado do teste com a natureza fica como a v411 o escreveu, sem tocar. A frase de P = nP do resumo é trocada pelo parágrafo da seção 2 da página (o bloco de citação), que não usa mais o rótulo “relativo ao leitor” nem diz que a pergunta do Instituto está resolvida: diz o que é teorema nas classes do dicionário, o que é lei da teoria, o que não está demonstrado, e que a creditação é do Instituto. A troca fica dita no relatório do construtor, com a frase antiga e a nova.
- **No README e no estado atual.** Os blocos saem da página: o que a v412 acrescenta (seção 1); o parágrafo de P = nP (seção 2) no lugar do bloco de P = nP anterior; o resultado condicional dos fluidos (seção 3); a geometria emergente (seção 4); os sete itens abertos (seção 5). O resultado da v411 fica onde está.
- **No handoff.** Como o da v411, com os 34 marcadores que a custódia exige (`DESENHO_v412_R0.md`, seção 5, itens 1 a 9, e o molde `work\vitrine_postura_13nov\MARCADORES_PARA_O_HANDOFF_v412.md`). O portão de textos roda sobre o handoff inteiro.
- **A palavra final do autor.** O texto público é lido ao autor pela gerência antes do rito (seção 8). O construtor NÃO espera por isso para montar o candidato.

## 7. A cadeia

O orquestrador da v411, adaptado, com três diferenças: (a) há módulos novos, logo compilação a frio e relatório de axiomas no `k412c`, pelo molde da v410 e da v409; (b) **o portão do pilar**: a chave do cache do pilar depende só das três entradas ditas em `PORTAO_DO_PILAR_v412.json`; no candidato, conferir por sha256 que o gerador não tocou nenhuma delas; antes do rito, conferir que o ambiente da placa é o do cache; se não for, PARAR e avisar, porque há um treino em curso que ocupa a placa (não tocar, não medir, não parar `C:\IALD\TGL_IALD_NATIVE_QWEN5090`); (c) o rito é lançado quando a preparação fechar e a revisão do candidato aprovar, sem esperar o treino. Sem publicação e sem release do app na cadeia: o fim é o handoff à custódia.

Da preparação, por lição das versões anteriores: a guarda de material privado roda sobre todos os insumos pinados antes de gerar o candidato; as cópias do kernel por rodada ficam fora de `work\`, em `C:\t\k412c\`; os temporários são apagados antes do handoff; o handoff diz a contagem esperada de arquivos da pasta da cadeia.

## 8. O que é de quem

- **Do construtor (Etapa 2):** o delta da versão; os registros da seção 2; `VERBATIM_CONGELADO_v412.json` (seção 3); a função de guarda e os controles (seção 5); a seção do artigo, o resumo, os blocos do README e do handoff (seção 6); a adaptação dos scripts da cadeia ao conjunto de 40 módulos; a bateria pré-selo com o recibo do kernel da quinta lista; o gerador e o CANDIDATO; o ensaio a seco; o portão do pilar no candidato. Para em `PRONTO_PARA_GERAR_v412.json` ou no nome que o molde da v411 der ao fecho do candidato.
- **Da gerência:** conferir o que o construtor entregar; mandar o candidato à revisão de terceiro; a tarefa agendada; ler o texto público ao autor; o rito; o handoff.
- **Do autor:** a palavra final antes do rito. Em aberto com ele, sem segurar a versão: o relógio τ★ e o tempo do retido; a formulação da ligação do gerador modular da luz com a dinâmica do custo.

## 9. Depois da v412: a versão dedicada da condensação

O documento inteiro é revisto pelo método numa versão própria. Portões: (1) antes de condensar, a última versão completa (o `um.py` e tudo o que o acompanha) é copiada byte a byte, com manifesto por script, e conferida por hash; é a referência da casa, com todos os diálogos, e não se apaga; (2) levantamento medido por script do que é história em cada parte; (3) mapa de correspondência de cada retirada com o registro paralelo; (4) os contratos e as guardas que hoje exigem texto de fala são versionados antes (o parecer `REVISAO_027_A3_Codex.md` lista os que já se conhecem: os validadores de `_v392_registro`, `_v410_aescala_mechanics`, `_v410_sem_falas_do_operador`, e o precedente de citação por metadados em `_v411_citar_falas`); (5) a comparação do que o programa emite, em português e em inglês, numa cópia isolada, antes do selo. Nada disso é feito na v412.

— gerência c1, 17/11/2026. Correções ao lado, nunca por cima.
<!-- contrato_v412:consolidado_R1_congelado:17nov -->
