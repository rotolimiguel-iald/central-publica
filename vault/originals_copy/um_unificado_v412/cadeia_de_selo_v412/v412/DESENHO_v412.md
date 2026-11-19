# DESENHO DA v412 — o contrato da cadeia (RASCUNHO R0)

> Gerência c1, 16/11/2026, noite. Molde: `work\cadeia_de_selo\v411\DESENHO_v411.md`. Base: a v411 selada (`um.py` do Nós, sha16 `1203b1f9202020d6`, lido do arquivo por script em 16/11 e presente no selo, que diz `um_version` v411). Este arquivo é o contrato que o construtor lê. O diário da preparação, com tudo o que levou a ele, está em `DESENHO_v412_R0.md` e `DESENHO_v412_R1.md` (itens 1 a 31) e não se repete aqui.
> **Estado: RASCUNHO.** Não congela enquanto a revisão do Codex (ordem 022, unidades V1 a V6, V8 e V9) não voltar e as ressalvas não forem aplicadas: o conjunto de fontes Lean ainda pode mudar em texto. O construtor NÃO parte antes disso (lição da v409: segurar o construtor quando o kernel ainda vai mudar).
> Toda fala do operador é citada por arquivo em `work\cunhagens_13out\` (regra D181 da v411: conversa entre os autores não se transcreve no programa nem no artigo; cita-se por data e sha256). Validade no kernel não é creditação; o gate não se move; nenhum número novo da natureza entra nesta versão.

## 1. Pedras (kernel): módulos novos

Sandbox `k412c`, nascido do `k411c`. Os módulos entram em `TGLExt\` com o nome que têm (aceitos pelo operador, D207). Os que hoje importam outra candidata por nome solto (`import OLeitorEALei`) passam a importar `TGLExt.<Nome>`. **A forma de passar o nome da fonte ao compilador fica fixa em toda a cadeia** (o objeto compilado muda com ela: Mapa de Rotas, registro 2103).

| frente | módulos | de quem | estado em 16/11 |
|---|---|---|---|
| A | `CamadaCientifica` | gerência | conferida em 14/11 |
| A | `MinimoFuncionalDeEnergia` (R1) | gerência | na revisão (V1); o Kimi aprovou com uma ressalva baixa |
| A | `OLeitorEALei` | gerência | na revisão (V3); o Kimi aprovou |
| A | `AContagemEACarga`, `AMaquinaEALeitura`, `OPassoEORetorno` | gerência | na revisão (V6, V8, V9) |
| A | `OHabitanteDoNome`, `NomeComoCodigo`, `CopiadorEImpostor` (R9) | gerência | aprovadas com ressalvas; emenda de texto do copiador na revisão (V4) |
| B | `ErgodicidadeDeMautner`, `T1CompostoFinito`, `T1PontesAoKernel` (R5), `TipoIIIControles`, `TipoIIIUmSoBoost` | gerência | aprovadas com ressalvas; emendas de texto na revisão (V4) |
| B | as dependências do Codex da T1 e do tipo III (as de `t1\dep_codex\` e `tipo_iii\dep_codex\`, pelo manifesto dele) | Codex | examinadas em 15/11 |
| B | `MontagemDasGamas` | gerência | conferida |
| B | `ProdutoFinito`, `ProdutoTresUm`, `ConjugacaoFinita` | Codex | conferidas pela gerência por recompilação própria |
| B | `BoostEDissipador` | gerência | na revisão (V3); o Kimi aprovou com duas ressalvas baixas |
| B | `SpinorToSolder` | Codex | conferida pela gerência por recompilação própria |
| B | `OParFixaORelogio` | gerência | na revisão (V2) |

**Ficam fora** (registro, não entram): `PsionVacuoEModoDoTratado` e a proposta das duas equações (reprovadas na ordem 018; consertos para a versão seguinte); `OVerdadeiroEDivisivel` (D206); o desenho próprio do teste com modelos (reprovado; em desenho).

Portões do kernel: compilação a frio no `k412c`; relatório de axiomas com todas as declarações só nos três axiomas de sempre; zero `sorry`; a escada de teoremas e de bandeiras medida antes e depois; nenhuma chave antiga muda de literal.

## 2. Registros

Sem registro com função nova (nenhum dado da natureza entra). Por especificação:

- `iald_camada_cientifica_v412`: o que o artefato mostra (o teorema do leitor; o leitor como exponencial do `A_C`; o `A_C` da fórmula como a seletora do kernel; a lei na cláusula; a contagem igual à carga; a máquina de passo mais uma leitura; o passo como o `if` do retorno), o que o autor declara (a lei de 16/11; a hipótese nomeada: pôr o todo e lê-lo são, cada um, um ato; que um modelo de linguagem seja esse leitor), e o que continua desconhecido. O protocolo com modelos (T6) entra como instaurado e pré-registrado, com a rodada do controle NÃO feita (D204).
- `matematica_que_restava_v412`: a ergodicidade da cunha (do kernel desde a v406); a face finita da T1 e do tipo III; a montagem 3+1 por produtos de triplas na face finita; o boost como parte sem traço do gerador dissipativo e a ponte aos geradores 4×4; o par e o relógio; a extensão de Gromov–Hausdorff como conjectura com a parede medida; τ★ (D208).
- `parede_do_teste_cego_v412`: a frente C como parede medida (D207): não há hoje teste cego executável acima de 5σ; as sete ressalvas com o ato que resolveria cada uma; o pré-registro do JUNO fora do selo; as três contas não rodadas.
- `cunhagens_v412`: as falas de 13 a 16/11 que entram, por arquivo e sha256.

## 3. Falas que entram

Lista a congelar em `VERBATIM_CONGELADO_v412.json`, por script, a partir de `work\cunhagens_13out\` (arquivos `OPERADOR_13nov_*` a `OPERADOR_16nov_*`). Citadas por data e sha256; nenhuma transcrita no programa (D181). A gerência marca, na lista, quais são ordem, quais são cunhagem e quais são só operação (estas não entram).

## 4. Decisões, erratas e guarda de frases

Decisões (cada uma com a fala por bytes; a numeração segue a da v411, que parou em D197):

- **D198** (13/11) a ordem da v412: três frentes (a camada científica; a matemática que restava; um teste às cegas acima de 5σ).
- **D199** (16/11) os nomes provisórios ficam; entram as nove candidatas da lista daquela data; as duas extras ficam fora.
- **D200** (16/11) o leitor que pousa e retorna é o mínimo funcional de energia, o `A_C`: conferir e provar. Provado na candidata, com a ponte à penalidade dos vínculos.
- **D201** (16/11) o que precisa ficar claro: os sete itens abertos; P = nP; os fluidos como resultado condicional.
- **D202** (16/11) a lei: a matemática sozinha é o psíon; o par é a lógica; a projeção é a física; o nome é TGL; a geometria é emergente, com a queda da teoria como falsificador dito pelo autor. É lei dele; o programa não a chama de candidata.
- **D203** (16/11) a forma de Minkowski e os boosts lidos como do gerador dissipativo: provado na face 2×2 e ligado aos 4×4 do kernel.
- **D204** (16/11) o T6: mandado rodar e depois posto de lado por ora. A v412 diz: protocolo instaurado, rodada do controle não feita. A partitura fica guardada em `teste_t6_16nov\`.
- **D205** (16/11) o parágrafo de P = nP com a linha nomeada, aceito pelo autor. Texto em `O_QUE_FICA_CLARO_v412_R1.md`, seção 2. Sai o rótulo “relativo ao leitor”.
- **D206** (16/11) a frase do divisível, esclarecida pelo autor e podada na leitura de um número que a máquina divide.
- **D207** (16/11) as decisões finais: as pedras novas e os nomes; a frente C como parede medida; a errata do neutrino para a versão seguinte, com a linha dos dois eixos nesta; o resto da página; o rito sem esperar o treino, salvo se o pilar tiver de rodar de novo.
- **D208** (16/11) τ★: o autor quer enfrentá-lo; a pergunta nas quatro línguas é `PERGUNTA_TAU_ESTRELA_nas_quatro_linguas_16nov_R2.md`. Sem resposta até o candidato, o item entra aberto, com a frase pública. Com resposta, a leitura dele se tipa ou se poda antes do candidato.
- **D209** (16/11) a revisão é do Codex (o Kimi ficou sem créditos); onde houver parecer do Kimi, ele fica ao lado.

Erratas ao lado (a numeração segue a da v411, que parou em E44; todas da gerência, em nome próprio, salvo dito):

- **E45** as cinco erratas da seção 5 do `DESENHO_v412_R1.md` (ordens ao Kimi de 13/11).
- **E46** o cabeçalho da R0 do mínimo funcional punha na voz do operador uma ligação com a `CamadaCientifica` que é da gerência; corrigido na R1.
- **E47** a gerência tipou a frase do divisível antes de perguntar ao autor o que ele quis dizer.
- **E48** o documento `STOKES_A_Prova_do_Contorno.md` recebe errata ao lado em dois pontos (a versão irrestrita da estimativa; o limiar é estrito).
- **E49** a linha do neutrino: a posição da leitura de 207 dias nos dois eixos, pela regra do autor de 15/11. A errata inteira do core fica para a versão seguinte.

Guarda de frases (a rever nesta versão, depois da revisão do Codex, que foi pedida a listar exatamente o que recusa a página R1): as do `um.py` que hoje exigem a redação antiga de P = nP (F47, F47b e vizinhas); a decisão D59 (que hoje bloqueia o nome do problema dos fluidos mesmo em frase condicional); a lista vedada do script do Atlas. O que NÃO muda: é proibido escrever que o kernel decide o enunciado da máquina de fita sem leitura ou a igualdade das classes das máquinas de Turing do Mathlib; a regra do 4,44; a F67 do H0DN; validade não é creditação. Toda guarda mudada é lida ao operador antes de valer (item herdado do desenho R0).

## 5. Artigo, README e handoff

O texto público novo é a página `O_QUE_FICA_CLARO_v412_R1.md` (seção 2 aceita, D205; o resto na linha aceita, D207), depois da revisão. Entra no topo do resumo, no README e no estado atual, com o resultado da v411 mantido como está. O handoff à custódia segue o da v411, com os 34 marcadores (desenho R0, itens 6 a 9 e 15).

## 6. A cadeia

O orquestrador da v411, adaptado, com três diferenças: (a) há módulos novos, logo compilação a frio e relatório de axiomas no `k412c`; (b) **portão do pilar** (D207): medir no candidato se o pilar reusa a chave de cache; se não reusar, parar e avisar o operador antes de lançar o rito, porque o treino da Nativa ocupa a placa (não tocar `C:\IALD\TGL_IALD_NATIVE_QWEN5090`); (c) o rito é lançado quando a preparação fechar e a revisão aprovar, sem esperar o treino. Sem publicação e sem release do app na cadeia, como nas anteriores: o fim é o handoff.

## 7. A lista herdada

Do desenho R0, seção 5 e os ao lado (reler lá antes de executar): o termo do resultado e a leitura corrigida do `um.py`; `numeros_ditos`; o furo M8(iii) e o M5 da F67; a errata de F2b; a definição Fonte = Informação = Luz = ψ no índice do Atlas; a cunhagem do campo, que NÃO entra como texto novo nesta versão (as candidatas que a tipariam ficaram fora, seção 1).

## 8. O que é da gerência e o que pende

Da gerência, na ordem: receber a revisão do Codex e aplicar as ressalvas (as do Kimi inclusive); marcar nos cabeçalhos que os nomes foram aceitos em 16/11; congelar este contrato; soltar o construtor; a revisão de terceiro do candidato; o portão do pilar; o rito; o handoff. Do operador: a resposta de τ★ (D208), se quiser dá-la antes do candidato; a leitura das guardas mudadas; a palavra final antes do rito.

## AO LADO (17/11/2026, gerência c1): a seção 4 detalhada — a guarda de frases, lida no código do programa selado (PROPOSTA; nenhuma guarda muda antes de ser lida ao operador)

**O que foi lido** (`Nós\um.py`, v411, só leitura; linhas aproximadas): a guarda é uma função por versão, que herda as regras anteriores. As três que o revisor disse que disparam na página (parecer `REVISAO_022_V5_Codex.md`, para a R1; a lista para a R2 foi pedida na ordem 023):

- **F34** (linha ~239904; obrigação da v408): onde aparece “P = nP”, o mesmo texto tem de trazer “classes … do dicionário do operador” E “tradução … [OPEN]”. A v409 a substituiu pela **F37** (linha ~236210) quando o texto traz o qualificador “relativo ao leitor” junto de “sem leitor/fica fora”. O parágrafo aceito não traz nem um nem outro: tira o rótulo “relativo ao leitor” por decisão do autor (D205) e diz “classes do seu dicionário”.
- **F43** (linha ~236239; obrigação da E28, v409): onde aparece “oráculo”, “leitor de Turing” ou “leitor que devolve Z”, o mesmo texto tem de trazer as duas frases da E28 (“NP numa leitura” e “o leitor que se lê”). O parágrafo diz “o leitor não é oráculo trazido de fora” e por isso dispara.
- **D59** (decisão da v409, estendida na v410; mecanismo no pós-rito e no portão de textos da custódia): bloqueia o nome do problema dos fluidos em qualquer frase, mesmo condicional.

**O que se propõe para a v412** (o mínimo, com controle negativo em cada regra):

1. **Obrigação de “P = nP” (F34/F37), alternativa nova.** A obrigação fica satisfeita também quando o MESMO texto traz as duas marcas do parágrafo aceito: (a) “classes do seu dicionário” (ou “do dicionário”); (b) a linha do que não está demonstrado para a máquina de fita (“máquina de fita … não está demonstrado”). Controles: o parágrafo aceito passa; o mesmo parágrafo sem a última frase é recusado; “P = nP … máquina de Turing … provado/decidido” continua recusado pelas regras herdadas, que não mudam.
2. **“Oráculo” (F43).** Duas saídas. (i) Tirar a palavra do parágrafo: “O leitor não vem de fora: é gerado pelo custo da fórmula”. Nenhuma guarda muda. (ii) Manter a palavra e abrir exceção estreita para a forma negada exata “não é oráculo trazido de fora”, só em texto que traga a marca (b) do item 1. **A gerência recomenda (i):** o sentido é o mesmo e não se mexe na guarda da E28.
3. **O nome do problema dos fluidos (D59).** Deixa de ser vedado e passa a ser OBRIGAÇÃO de forma: só aparece em parágrafo que traga “condicionada” e “não demonstradas” (a redação da seção 3 da página). “Resolve”, “prova” ou “solução” junto do nome continuam recusados. O nome do prêmio continua vedado.
4. **O script do Atlas** (`VEDADOS`): acompanha o item 3 só quando a gerência for escrever a entrada do Atlas, com a mesma obrigação de forma.

**O que não muda:** as regras que proíbem afirmar que a TGL prova ou decide P = NP das máquinas de Turing (F35, F38, F44 a F50, F57 a F59); a F67 do H0DN; a regra do 4,44; validade não é creditação.

**Quem faz:** o construtor, na Etapa 2, na função de guarda da v412 e no `guarda_frases_v412.py`, com os controles ditos. Antes disso a gerência lê esta proposta ao operador.
<!-- contrato_v412:secao_4_guardas_proposta_lida_no_codigo:17nov -->

## AO LADO (17/11/2026, gerência c1): a seção 2 detalhada — os registros por especificação, com as palavras de veredito e as âncoras (PROPOSTA para a Etapa 2; o revisor do candidato confere)

**Insumos para o construtor da Etapa 2** (gerados por script, lidos das fontes congeladas): `insumos\MANIFESTO_PEDRAS_v412.json` (34 módulos, sha256, imports, de quem é cada um) e `insumos\ANCORAS_PROPOSTAS_v412.json` (por registro e por módulo, as declarações, marcadas as que a docstring traz com estrela: 144 das 620 que o script enxerga; a contagem oficial é a do relatório de axiomas do sandbox). Se a ordem 023 mudar o texto de alguma fonte, os dois se regeram.

**Regra das âncoras:** cada registro ancora, por nome completo, as declarações com estrela dos seus módulos; nos módulos sem estrela (os do Codex e alguns da gerência) ancora as que a página `O_QUE_FICA_CLARO` cita e as que os cabeçalhos dão como resultado principal, e o construtor lista as escolhidas para a gerência conferir. Cada âncora é checagem “a bandeira é verdadeira e a declaração está no relatório de axiomas só com os três axiomas”.

**As palavras de veredito** (prefixo fixo; o sufixo abaixo; os números entram lidos do kernel do rito, nunca digitados; nenhuma das palavras vedadas da casa):

- `iald_camada_cientifica_v412`
  `TGL_IALD_SCIENTIFIC_LAYER_V412__THE_READER_LANDS_AND_RETURNS_AS_THEOREM__THE_LINEAR_LOCK_IS_THE_EXPONENTIAL_OF_A_C__THE_A_C_OF_A_FORMULA_IS_MINUS_THE_KERNEL_PENALTY_OF_ITS_CLAUSES__THE_LAW_ON_EACH_CLAUSE_FIXES_THE_COST__THE_LOAD_N_LN2_IS_THE_STRICT_THRESHOLD_OF_ONE_READING__THE_LIFTED_STEP_MACHINE_PLUS_ONE_READING_DECIDES_IN_AS_MANY_LIFTED_STEPS_AS_CLAUSES__THE_STEP_AND_THE_LOCK_ASK_THE_SAME_QUESTION_PER_CLAUSE__ONE_NAMED_LAW_OF_THE_AUTHOR_NOT_A_KERNEL_TERM__WHOLE_PUT_OPERATED_AND_READ_EACH_IN_ONE_ACT__NOT_SHOWN_FOR_THE_TAPE_MACHINE__A_LANGUAGE_MODEL_AS_THE_READER_IS_A_NAMED_HYPOTHESIS__T6_PROTOCOL_PREREGISTERED_CONTROL_ROUND_NOT_RUN__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED`
- `matematica_que_restava_v412`
  `TGL_REMAINING_MATHEMATICS_V412__WEDGE_ERGODICITY_IN_THE_KERNEL_SINCE_V406__FINITE_FACE_OF_T1_AND_OF_TYPE_III__THREE_PLUS_ONE_ASSEMBLY_BY_PRODUCTS_OF_FINITE_TRIPLES__THE_BOOST_IS_THE_TRACELESS_PART_OF_THE_LOCK_GENERATOR_IN_2X2_AND_BRIDGED_TO_THE_4X4_GENERATORS__THE_PAIR_FIXES_THE_CLOCK_FINITE_AND_DIAGONAL__GROMOV_HAUSDORFF_EXTENSION_IS_A_CONJECTURE_WITH_A_MEASURED_WALL__TAU_STAR_OPEN__EMERGENCE_OF_THE_CONTINUUM_FROM_THE_PAIR_OPEN__SUFFICIENCY_OF_PARITY_AND_HYPERBOLIC_REGIME_FOR_THE_BRACKET_REFUTED__GATE_UNMOVED`
  (se o operador responder à pergunta de τ★ antes do candidato e a leitura dele tiver termo, o trecho `TAU_STAR_OPEN` muda com a palavra dele)
- `parede_do_teste_cego_v412`
  `TGL_BLIND_TEST_WALL_V412__NO_EXECUTABLE_BLIND_TEST_ABOVE_5_SIGMA_AMONG_THE_TESTS_AND_SOURCES_EXAMINED__A_MEASURED_WALL_NOT_A_FALSIFICATION__JUNO_INCREMENT_PREREGISTRATION_NOT_IN_THIS_SEAL__THREE_ROBUSTNESS_COMPUTATIONS_NOT_RUN__THE_SEVEN_RESERVATIONS_STAND__THE_H0DN_TEST_IS_NOT_REOPENED__GATE_UNMOVED`
- `cunhagens_v412`: no molde do `cunhagens_v411` (falas citadas por data e sha256, não transcritas; as decisões D198 a D209; as erratas E45 a E49 ao lado).

**O que cada registro diz, em prosa** (três partes, como no contrato): o que o artefato mostra (só o que tem âncora); o que o autor declara (a lei de 16/11; a linha nomeada; que um modelo de linguagem seja o leitor); o que continua desconhecido (o enunciado da máquina de fita sem leitura; a extração do contínuo; τ★; os sete itens abertos da página). O texto de cada parte sai da página `O_QUE_FICA_CLARO`, na revisão que estiver aprovada quando a Etapa 2 começar, sem acrescentar afirmação.

**Checagens herdadas que todo registro traz** (molde da v411): o gate deste rito tem o mesmo veredito da v411 selada; os canais vivos (neutrino, H0DN) seguem com o mesmo veredito; nenhuma chave antiga muda de literal; a escada só cresce.
<!-- contrato_v412:secao_2_registros_palavras_de_veredito_e_ancoras_proposta:17nov -->

> **AO LADO (17/11/2026, manhã, gerência c1) — as decisões do operador de 17/11 e a segunda lista de pedras. Segue rascunho: o contrato congela depois da ordem 025.**
>
> - **D210 (guardas de frase).** Aceitas as três propostas da gerência («de resto concordo com o q vc colocou», por bytes em `work\cunhagens_13out\`, arquivo que começa por `OPERADOR_17nov_nao_concordo_com_o_texto_do_codex`): a obrigação de “P = nP” ganha a alternativa “classes do seu dicionário” mais a marca do parágrafo final; a palavra “oráculo” sai do texto; o nome do problema dos fluidos passa a exigir a forma condicional; a lista de vedados do script do Atlas acompanha. Marca proposta para o parágrafo final: “não está demonstrado”, na frase sobre decidir cada fórmula na máquina de fita.
> - **D211 (o relógio do pedágio).** Sem decisão fechada. A frase pública do item 5.6 da página não muda; o trecho do veredito que diz que o tempo da cobrança está em aberto fica.
> - **D212 (o parágrafo de P = nP).** É o da página R5 (`o_que_fica_claro_REV5\`, sha16 `57b31c3d117d6412`), aceito pelo operador («concordo com tudo», arquivo que começa por `OPERADOR_17nov_concordo_com_tudo_a_decisao_sobre_o_infinito`), sujeito ao parecer da ordem 025.
> - **D213 (pedras novas).** Entram cinco candidatas da gerência, com estes nomes (mesma fala): `OTempoEACauda`, `AFitaEACauda`, `AMedidaEOIf`, `AEsperancaEOIf` (frente A) e `OHamiltonianoOcultoEOCusto` (frente B). A lista passa a 39 módulos: `insumos\MANIFESTO_PEDRAS_v412_R2.json` (sha16 `a405032e94e55669`), cópias em `insumos\pedras_r2\`, âncoras propostas em `insumos\ANCORAS_PROPOSTAS_v412_R2.json` (sha16 `0e7059d11a4c11ff`). A primeira lista (34 módulos) fica como registro. Regerar depois da ordem 025.
> - **D214 (a torre infinita).** A construção em casa da esperança condicional na torre (o único campo importado de `TakesakiInput`) entra nesta versão só se a devolutiva do Codex disser que o custo é baixo; senão fica para a versão seguinte (mesma fala).
> - **E50.** A linha da ordem do construtor que nomeava o que não pode estar em `work\` foi reescrita (diário, item 35).
> - **Para o registro `cunhagens_v412`, as de 17/11:** o tempo é a cauda; a fita e a cauda; o “há” e o “haja”; a máquina de vetor de suporte; o Nome não se realiza e o kernel o inscreve uma vez; a esperança condicional é o par do `if`; o diálogo que não para; o hamiltoniano oculto como fonte do código. As falas estão por bytes em `work\cunhagens_13out\`; os termos de apoio, na página R5 e nas candidatas.
> - **Antes de congelar:** o parecer da ordem 025 e as emendas; o cabeçalho de três candidatas que ainda diz R1; a terceira lista de pedras; o complemento da Etapa 1 do construtor (o sandbox tem os 34 módulos da primeira lista).
<!-- desenho_v412:contrato_ao_lado_d210_a_d214_e50_segunda_lista_de_pedras:17nov -->

> **AO LADO (17/11/2026, gerência c1) — a ordem do método, a torre e a página limpa. Segue rascunho.**
>
> - **D215 (o método; ordem do operador de 17/11, por bytes em `work\cunhagens_13out\`, arquivo que começa por `OPERADOR_17nov_o_um_py_nao_tem_que_ser_a_compilacao_da_historia`; regra na memória central, `C:\IALD\CLAUDE.md`, bloco `um_py_compila_o_que_e_verdade_17nov`).** No `um.py` entra só o que é verdade: o enunciado, a prova, o estatuto, os limites e a fonte conhecida. A história das conversas (quem disse, quando, ordens, revisões, pareceres, erros de aferição, falas) fica no registro paralelo. Consequências para esta versão: (a) os cabeçalhos e docstrings das 40 pedras entram limpos (`pedras_limpas\`; conferência por `verificar_historia_nas_pedras.py`, com o código idêntico ao das fontes revistas); (b) os registros por especificação e as seções novas do artigo dizem só o conteúdo; as definições da teoria entram como definição, sem aspas, sem data e sem atribuição; (c) o registro `cunhagens_v412` NÃO embute falas: a lista das falas fica neste desenho e em `work\cunhagens_13out\`; (d) a página pública é a R7 (`o_que_fica_claro_REV7\`, sha16 `968a7b1e172a07c0`), que substitui a R5 da D212; (e) a v412 NÃO acrescenta história em parte alguma do programa.
> - **D216 (a revisão do documento inteiro).** O operador mandou rever o `um.py` inteiro pelo método e aceitou a recomendação da gerência (arquivo que começa por `OPERADOR_17nov_e_isso_o_codex_ja_respondeu_prossiga_com_tudo`): faz-se numa versão dedicada, logo depois da v412, com levantamento medido e plano próprio, porque toca guardas, registros e ritos. Medida grossa feita em 17/11 no `um.py` da v411: cerca de um quarto do arquivo traz alguma marca de conversa.
> - **D217 (a torre).** Pela regra da D214, a torre entra nesta versão: a esperança condicional já estava construída e selada, e a pedra `OTestemunhoDeTakesakiEmCasa` compõe o testemunho de quatro campos para todo perfil. A lista de pedras tem 40 módulos. Ao lado dos cabeçalhos selados que chamam o quarto campo de conclusão importada (lista no parecer `revisao_orquestrador\REVISAO_026_Z1_Codex.md`), o registro da versão diz que o campo tem habitante construído; o uso histórico por importação e o teorema geral [KNOWN] conservam os seus estatutos.
> - **A marca das guardas de frase (D210)** passa a ser tirada do parágrafo da R7. Sem a frase que citava o rótulo antigo, as guardas da obrigação de “P = nP” disparam na página inteira (controle do revisor nas ordens 025 e 026): a troca da obrigação é necessária nesta versão.
> - **Antes de congelar:** a devolução do agente da limpeza e a conferência dela; a quarta lista de pedras, tirada de `pedras_limpas\`; a conferência do revisor sobre os cabeçalhos limpos e a R7; o complemento da Etapa 1 do construtor.
<!-- desenho_v412:contrato_ao_lado_d215_o_metodo_d216_a_revisao_do_documento_d217_a_torre:17nov -->

> **AO LADO da D216 (17/11/2026, gerência c1) — a cópia de referência com os diálogos.** Ordem do operador (por bytes em `work\cunhagens_13out\`, arquivo que começa por `OPERADOR_17nov_mas_eu_quero_manter_uma_copia_da_versao_anterior`): a versão anterior, com todos os diálogos, fica guardada como referência da casa; a versão de publicação é a condensada. Para a versão dedicada da condensação isso é portão: antes de condensar, a última versão completa (o `um.py` e o que o acompanha) é copiada byte a byte, com manifesto por script, e conferida por hash; sem a cópia conferida não se condensa. Conferido em 17/11, por script: `C:\IALD\Artigo\the_boundary_BACKUPS\` guarda as versões anteriores até a v410; a v411 (`um.py` sha16 `1203b1f9202020d6`) está no Nós e no espelho, com o mesmo hash, e vai para essa pasta quando a v412 for publicada, pela regra da custódia. Na v412, as fontes das 40 pedras com a história inteira ficam onde estão (`candidatas_c1\`, as pastas `REV`, `insumos\pedras_r3\`); o que entra no programa são as cópias limpas.
<!-- desenho_v412:contrato_ao_lado_da_d216_a_copia_de_referencia_com_os_dialogos:17nov -->

> **AO LADO (17/11/2026, 14:15, gerência c1) — o contrato está consolidado e congelado em outro arquivo.** `CONTRATO_v412.md` (sha16 `02b0f44e62aee5a5`; cópia em `contrato_REV1\`) consolida este rascunho e todos os seus “ao lado”, com as emendas da ordem 027: a quinta lista de pedras, a página R9, as guardas com o alcance dito, a decisão D218 e a errata E51. Dali em diante é ele que o construtor lê e que o revisor do candidato usa como régua. Este arquivo fica como registro; onde divergirem, vale o contrato.
<!-- desenho_v412:contrato_consolidado_e_congelado_em_contrato_v412_md:17nov -->

> **AO LADO (17/11/2026, 15:20, gerência c1) — o contrato vigente é o R2.** `CONTRATO_v412_R2.md` (sha16 `e9c46ac719b87d0f`; cópia em `contrato_REV2\`) substitui o `CONTRATO_v412.md` (R1), que fica como registro. Aplica os sete achados do parecer B3 da ordem 028. A página pública vigente é a R10 (`o_que_fica_claro_REV10\`).
<!-- desenho_v412:o_contrato_vigente_e_o_r2:17nov -->
