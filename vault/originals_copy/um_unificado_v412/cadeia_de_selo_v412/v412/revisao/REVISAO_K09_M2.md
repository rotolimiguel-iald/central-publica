# CONFERÊNCIA DISTINTA — K09: o neutrino m₂

> Montado pela gerência c1 em 15/11/2026 16:53 a partir do retorno estruturado de um revisor distinto (modelo Sonnet; só leitura; scripts próprios na pasta de rascunho dele). É [DECLARADO pelo revisor] no que a gerência não reconferiu. As frases da seção “Para o operador” são propostas do revisor, não fala do operador, e só vão a ele depois de lidas pela gerência. Nada aqui está instalado, congelado ou aberto.

**Veredito:** APROVADO_COM_RESSALVAS — achados: 1 ALTO, 6 MEDIO, 4 BAIXO

## Resumo

As contas do m2 reproduzem com script próprio e a descrição do ramo de decisão do código confere com o um.py selado. Há um ALTO, seis MEDIO e alguns BAIXO, todos de redação, escolha escondida ou escopo, nenhum de aritmética.
1. Contas: r em m2 e em Delta m2 de 59,1 d, 207,2 d, NuFIT (tabela, eq. 11 e simétrico do core), SK-Gd, Capozzi, SNO+, KamLAND, solares e PDG batem com o JSON (diferença menor que 1e-9). As quatro tabelas (a1, a2, b1, b2) batem célula a célula, até 2e-5 pp, por forma fechada e por integração direta. Também batem a Tabela 6 (64,788004 % e 66,145584 %), o incremento 59 para 207 (1,228176 sigma), SK-Gd (3,101149 sigma; 380,0785536 d; 17/10/2027), o piso s0 = 0,052587652, o MATCHED (7,348108 %) e o calendário nas duas métricas, que bate nas 12 datas.
2. Código (um.py L4589 a L4720): o ramo TENSION, a regra das duas testemunhas, a ausência de ramo MATCHED, o campo tensao_global_5sigma_sem_2a_determinacao e os quatro vereditos permitidos conferem.
3. Hashes: .py, .resultado.json e frozen_hash 4bdae22a conferem; o do dicionário portado (e24877) confere com o core. Os dez artefatos da tabela da entrega têm sha256 igual ao declarado.
4. ALTO: ENTREGA_K09:20 diz que o m2 mais provavelmente devolve tensão do primário. Isso vale só no mundo em que o valor verdadeiro é o centro público 7,388 (modelos a1 e b1). No mundo em que a previsão é verdadeira (a2 e b2) o resultado é ARMED_CONSISTENT em 99,7 %. A condição foi perdida e é uma escolha de hipótese não lida pelo operador.
5. As dez passagens da leitura da manhã foram corrigidas em substância. Restam três defeitos de redação. O primeiro é a negação "nenhuma data sugere que o autor tenha visto o dado antes", sem âncora no "antes" e inclusive para o degrau de 59,1 d. O segundo é "o dado tomado depois de 18/05/2026 é posterior aos dois marcos", quando o pino é de 08/08/2026. O terceiro é "toda superfície/todos os textos", falso para seis arquivos K01/K04 ainda vivos.
6. A errata em dados não diz que os artigos de 2025 também não têm a fórmula (conferi 12 padrões nos dois .tex), não separa a data do dicionário portado (L4618 cita 10/08/2026) e traz datas sem marca de estatuto.
7. A amostra de 207,2 d acumula a de 59,1 d e isso não entra na cronologia; "subconjunto de P" é mais forte do que se sabe. O estado ARMED_CONSISTENT não vem do perito JUNO 207: no core ele vem da linha NuFIT 2,9529, que só fica abaixo de 3 porque 0,097 foi arredondado para 0,10.
8. Fora do meu foco, não revisados: Hubble, combinação e as sete ressalvas. Não rodei scripts do Kimi, não usei rede nem dado observado.

## Achados

1. **(ALTO)** ENTREGA_K09.md:20 (origem em ENTREGA_K04.md:4; a conferência da gerência, REVISAO_K04_M2.md:9, dizia 'com a precisão da Tabela 6')

   'O que o m₂ mais provavelmente devolve segue sendo tensão do primário, não falsificação.' É probabilidade condicional a (a1)/(b1), isto é, ao mundo em que o valor verdadeiro é o centro público 7,388 e a previsão é falsa. Recalculado por mim: P(r≥5) = 64,79 % (a1) e 66,15 % (b1) na Tabela 6, mas 0,000058 % (a2) e 0,000202 % (b2); sob (a2)/(b2) o resultado é ARMED_CONSISTENT em 99,73 % e 99,41 %. Mesmo sob H1, P(r≥3) é 40,0 %, 61,8 % e 71,9 % com 1, 2 e 3 anos de dado novo, então 'mais provavelmente tensão' só vale a partir de cerca de 2 anos. A K04 dizia 'com precisão alta'; a K09 tirou a condição. Na língua do operador: a frase o induz a esperar negativo e esconde que isso depende de a previsão dele ser falsa, o que ele não leu.

   *Conserto pedido:* Trocar por: 'Sem segunda testemunha elegível, o canal só devolve ARMED_CONSISTENT ou TENSION; nenhum dos dois falsifica (parede medida). Se o valor verdadeiro for o centro público de hoje (a1/b1), o primário passa de r=5 com P≈65 % no desenho da Tabela 6; se a previsão for verdadeira (a2/b2), devolve ARMED_CONSISTENT com P≈99,7 %.' Dizer qual hipótese o texto adota (nenhuma).

2. **(MEDIO)** ENTREGA_K09.md:3; M2_DESFECHOS...K04.md:12 e :213; ERRATA_M2_K09.md:14; ERRATA_M2_K09_15nov.md:12; PRE_REGISTRO...K09.md:5; INSUMOS_PARA_A_PERGUNTA_K09.md (F11); REGISTRO_MAPA_K09.json (resultado)

   'Nenhuma data/superfície sugere que o autor tenha visto o dado antes.' (a) O 'antes' não tem âncora nem os dois eixos. (b) No M2:213 e no ERRATA:14 a frase fecha parágrafos que tratam também do degrau de 59,1 d, que já era público (18/11/2025) quando o valor 8,51 foi escrito (22/01/2026; o docx traz 8,67 meV na mesma parêntese): as datas não excluem nada, e é por isso que é retrodição sem ajuste. (c) No ERRATA:14 vem logo depois de 'hasheada depois de o número ser público' e a razão dada (artigos de 2025 sem o valor; entradas sem dado de neutrino) não responde ao eixo do pino. (d) Os bytes do operador de 15/11 (sha256 49e5f007…, abertos por mim) cobrem o artigo de 2025, não o valor. (e) A errata da gerência (R1 §7) e o Mapa seq 2063 adotam 'não diz o que o autor leu'. O texto passa a falar do estado de conhecimento do autor, o que a regra de 15/11 manda não fazer.

   *Conserto pedido:* Em todos os sítios: 'Esta nota fala só de datas e das entradas da fórmula; não diz o que o autor leu ou deixou de ler.' Para o valor: 'o degrau de 59,1 d era público quando o valor foi escrito (retrodição sem ajuste); o número de 207,2 d é posterior à previsão publicada e anterior ao hash da regra.'

3. **(MEDIO)** ENTREGA_K09.md:3, :10 e :18 ('em toda tabela de datas'); ERRATA_M2_K09_15nov.md:7 e :12; REGISTRO_MAPA_K09.json ('em toda superfície'). Resíduos: ENTREGA_K04.md:8; ERRATA_NEUTRINO_V412_RASCUNHO_K04.md:49 e :51; ERRATA_K01.md:39; ENTREGA_K01.md:79-81; PRE_REGISTRO_CEGO_RASCUNHO_K01.md:9, :49, :53, :61; ORDEM_K04:66-68. Um eixo só: M2:215; ERRATA_M2_K09.md:16; ERRATA_M2_K09_15nov.md:12 e :34; PRE_REGISTRO:5; ENTREGA:18

   'Todos os textos carregam os dois eixos' e 'em toda superfície' é falso. Varredura por script (207, 59, cega, prospectiv, antes, depois, anterior, posterior): seis arquivos K01/K04 ainda vivos na mesma pasta trazem formulações de um eixo só, p.ex. ENTREGA_K04:8 'primeira nova determinação JUNO posterior ao hash V2 … não é cega para a casa', que é errada para o número (público em jun/jul; só o artigo de 29/09 é posterior ao hash). A tabela de cronologia do M2 §5 não tem colunas de posição nos dois eixos, ao contrário do que a entrega diz. Há frases de um eixo só: 'também anterior ao pino' (M2:215); '59,1 d veio antes do valor público' sem 'e antes do pino' (ERRATA:16, 15nov:12 e :34, PRE_REGISTRO:5). O REGISTRO_MAPA, que entra no livro só-acréscimo, herdaria o excesso.

   *Conserto pedido:* Restringir a afirmação a 'nos arquivos desta rodada'; pôr 'SUPERADA neste ponto pela K09/15nov' ao lado de cada resíduo (ou pedir à gerência que o faça); acrescentar o segundo eixo às frases listadas; tirar 'em toda tabela de datas' ou pôr as duas colunas de posição na tabela §5.

4. **(MEDIO)** ENTREGA_K09.md:4 e :24; M2:219; ERRATA_M2_K09.md:14; ERRATA_M2_K09_15nov.md:12; PRE_REGISTRO:1, :5, :11, :69; INSUMOS F2; REGISTRO_MAPA_K09.json

   'O único dado posterior aos dois marcos é o dado tomado depois de 18/05/2026.' O pino é de 08/08/2026, 82 dias depois de 18/05, então parte desse dado foi tomada antes do pino; o que é posterior ao pino e à previsão é o NÚMERO tornado público pela primeira vez depois de 08/08/2026 (mesma chave trocada que a conferência da gerência achou no rascunho R0, F11). O observável do pré-registro fica ancorado na data de tomada, não na de primeira publicação. 'Ainda não mostrado' é [DECLARADO] (leitura da gerência de 14/11, não reconferida; o revisor da K04 achou o negativo fraco) e vem sem marca. 18/05/2026 e 26/08/2025 (base do duty cycle de 265 d) não têm resposta crua guardada: o ERRATA_NEUTRINO_V412_DADOS_K09.json traz 'janela_dados_fim' sem estatuto.

   *Conserto pedido:* Reescrever: 'só um número do JUNO tornado público pela primeira vez depois de 08/08/2026 (e antes de qualquer acesso do selo) é posterior à previsão publicada e ao hash da regra'. Marcar [DECLARADO] 18/05/2026, 26/08/2025 e a ausência de número posterior; guardar a fonte da janela antes de selar.

5. **(MEDIO)** ENTREGA_K09.md:18; M2:12 e :201-202 (linhas 16/10/2025 e 04/11/2025 da tabela §5); ERRATA_NEUTRINO_V412_DADOS_K09.json (tese_neutrino_2025: só valor_8_51_presente=false)

   Os dois artigos de 2025 são descritos como 'a tese do neutrino … sem o valor 8,51'. Medi: nos .tex dos dois (neutrino_nmc_revised e lie_of_light) há zero ocorrências de 8,5x, 0,0085, sin 45, 45°, π/4, √e, '1 eV', JUNO, β_TGL, α√e; o único meV é um intervalo genérico (meV a PeV). Ou seja, não têm a fórmula nem o valor. A K09 diz só 'sem o valor', e o JSON, que é a errata em dados, não tem campo para a fórmula. O um.py selado diz em L4222-4225, L4241, L4243 e L4620 que a derivação foi 'publicada 2025, Zenodo 17526619', e L2944-2950 (v182) já a retirou; a K09 não menciona essa contradição (a descrição do código cobre só o ramo de decisão). A palavra 'tese' fica sem definição.

   *Conserto pedido:* Acrescentar ao JSON formula_presente=false (com a contagem e as cadeias buscadas) e à prosa: 'os dois artigos não contêm a fórmula nem o valor'. Listar L4222-4225, L4241, L4243 e L4620 como itens para a gerência (C1 a C3 do rascunho R1). Definir ou trocar 'tese' por 'o que o título e o resumo afirmam'.

6. **(MEDIO)** M2:12, :213, :219, :242 (§6) e :268 (tabela §7, 'subconjunto de P'); ENTREGA_K09.md:3 e :18

   A cronologia diz que o número de 207,2 d veio depois da previsão publicada, mas não diz que a amostra de 207,2 d acumula a de 59,1 d, cujo número já era público antes do valor. A cegueira dita é a do número, não a dos dados (a conferência da gerência achou o mesmo defeito no R0, F6/F8). §6 diz que a liberação é cumulativa e não é independente, mas fora do texto cronológico. A tabela §7 chama o 59,1 d de 'subconjunto de P', mais forte do que se sabe: a conferência da K04 registra [DECLARADO] que a análise de 207 d mudou o volume fiducial e o corte de acidentais. A queda 2,206 para 1,938 é de uma amostra que acumula e não é série independente.

   *Conserto pedido:* Em cada frase de dois eixos: 'a amostra de 207,2 dias acumula a de 59,1; não são determinações independentes; a cegueira dita é a do número, não a dos dados'. Trocar 'subconjunto de P' por 'acumula P (seleção e volume fiducial mudaram) [DECLARADO]'.

7. **(MEDIO)** ENTREGA_K09.md:18 e REGISTRO_MAPA_K09.json (resultado); M2:9 (Conclusão 1) e §8.2 (:320)

   Item 5 da tarefa. A frase 'pela letra da regra congelada, o ajuste global fica na borda de TENSION' confere em números: 2,952854 (core, 7,530±0,100), 3,024242 (tabela NuFIT 7,537+0,094/−0,100), 3,044179 (eq. 11, 7,530+0,096/−0,097), ≈2,99 pelo perfil de Δχ² [DECLARADO, Mapa seq 93]; e o M2 diz os três primeiros sem escolher. Mas: (a) o resumo da entrega e o registro do Mapa cortam os números e não dizem em que lado o código selado está (abaixo de 3, ARMED_CONSISTENT) nem que o que o põe abaixo é arredondar 0,097 para 0,10; (b) 'pela letra' atribui à regra o que ela não fixa (a letra não diz qual ajuste global nem qual lado do erro; Mapa seq 93: 'a regra hoje não é unívoca'); (c) 'pelo perito autônomo JUNO de 207,2 dias o estado é ARMED_CONSISTENT' não é o que o código emite: o ARMED_CONSISTENT do core vem da linha NuFIT 2,9529 (última da escada), o perito v392 do core carrega o JUNO de 59,1 d (2,206) e diz 'CHANNEL VERDICT UNCHANGED'; o JUNO de 207,2 d nem está no core; (d) §8.2 põe 'Fonte global' sob 'para a gerência decidir', mas qual erro do NuFIT vale para a regra é decisão do operador (R1 D2).

   *Conserto pedido:* Dizer com números e lado: 'o core selado lê 2,953 e devolve ARMED_CONSISTENT; com o erro publicado do lado da previsão seria 3,024 (tabela) ou 3,044 (eq. 11) e o rótulo seria TENSION; a letra não escolhe; escolher é do operador; TENSION não é falsificação.' Trocar 'pelo perito, o estado é' por 'se o perito (R3) fosse atualizado para 207,2 d, a razão seria 1,938 (<3)'. Reetiquetar §8.2: o que é do operador sai de 'para a gerência'.

8. **(BAIXO)** ERRATA_NEUTRINO_V412_DADOS_K09.json ('pinos', 'degraus_juno', 'ajustes_globais'); M2:206-208 e :215

   O bloco 'pinos' tem um só 'data_do_congelamento: 2026-08-08' para o hash do objeto original e para o do dicionário portado (e24877…), que cita em L4618 uma decisão de 10/08/2026, logo é de 10/08 ou posterior (D7 do rascunho R1). As posições relativas não mudam (nenhum fato cai entre as duas datas), mas a data do bloco é inexata. Só 22/06 tem campo de estatuto; ficam sem marca 19/11/2025 (coletiva), Nature 654 343–348 com DOI e 10/06/2026, 18/05/2026, arXiv:2601.09791 v1 14/01 e v2 12/04/2026, SK-Gd 02/10/2026, 15/07 e 22/07/2026, apesar de nenhuma ter resposta crua na pasta v412; a entrega diz 'só números com fonte'. 'A data que comprova o valor público é 15/07' (M2:215) vale como indício, não como prova, pois ninguém abriu a página de Indico. O 'primeira ocorrência guardada' de 22/01/2026 não diz 'sem carimbo externo' (a data é do corpo, do docProps e do mtime).

   *Conserto pedido:* Separar data_objeto_original=2026-08-08 de data_dicionario_portado='≥2026-08-10 (L4618), data da portagem não estabelecida'; pôr 'estatuto' (REAL/DECLARADO) em cada data; trocar 'comprova' por 'indica [DECLARADO]'; acrescentar 'sem carimbo externo' ao 22/01/2026.

9. **(BAIXO)** M2:189 (§4.2); PRE_REGISTRO:84 e :118; M2:182-183 (linhas r=3 da §4.1); PRE_REGISTRO:115

   O texto diz que com o piso s0=0,052587652 os alvos de 5σ e D90 ficam inalcançáveis. Verifiquei: o alvo de r=3 também (σ=0,050130 em Δm², 0,050388 em m₂, ambos menores que s0), mas as linhas r=3 (08/03/2027 e 01/10/2027 em Δm²; 03/03/2027 e 26/09/2027 em m₂) seguem na tabela sem a ressalva; o PRE_REGISTRO:118 diz 'nenhuma data acima vale', mas o M2:189 não.

   *Conserto pedido:* Acrescentar 'e r=3' à frase do piso em M2 §4.2 e ao PRE_REGISTRO:84.

10. **(BAIXO)** M2 §8.2 (:317-325); INSUMOS_PARA_A_PERGUNTA_K09.md (F7, F8); PRE_REGISTRO:127 e §6 (:139-144); ENTREGA_K09.md:28

   Escolhas e leituras que ainda não passaram pelo operador aparecem em tom de fato. (a) INSUMOS F7 põe sob 'Fatos' que o negativo atinge 'o pacote da escala … não β isolado', enquanto o PRE_REGISTRO:127 diz que é leitura a apresentar a ele; o pacote lista Um posto 1 eV, m₁≈0 e 'a identificação', sem nomear o sen 45° (leitura dele, [ONTO]) nem o ordenamento. (b) PRE_REGISTRO §6 descreve em indicativo quem guarda, quem abre e quem nomeia o revisor, e a l.140 faz o operador fixar A ou B 'com a gerência'; INSUMOS F8 chama de 'proposta'. (c) A tabela MATCHED só dá probabilidades no mundo em que o valor verdadeiro é o centro publicado (0,13 % a 7,35 %); o mundo H2 (68,3 % × 68,3 % ≈ 46,6 %) não aparece. (d) ENTREGA:28 repete 'o operador autorizou o conjunto D em 29/10 e a opção (c) em 03/11' sem citar bytes.

   *Conserto pedido:* Mover F7 para 'leitura a apresentar ao operador', nomear o 45° e o ordenamento, dizer que com a regra A e sem S o único negativo possível do canal é TENSION (parede medida); marcar §6 como 'proposta'; pôr a coluna H2 na tabela MATCHED ou dizer que ela só vale em H1; citar os bytes das datas 29/10 e 03/11 ou marcar [DECLARADO pela ORDEM K09].

11. **(BAIXO)** ENTREGA_K09.md:10; K04/M2/K09/scripts/fechar_auditoria_k09.py e medidas/auditoria_final_independente_k09.json; M2 §7 (linhas Capozzi e Bari 2026.a)

   'Rodada revisada internamente por conferência independente' é script do próprio construtor (a revisão distinta é esta), e o campo 'cronologia_dois_eixos: true' do validar_k09 não pegou os resíduos K01/K04. As linhas Capozzi (arXiv:2511.21650) e Bari 2026.a (7,465 +0,072/−0,080, 'preliminar', sem identificador) entram na tabela com r calculado e sem [DECLARADO]; a conferência da K04 diz não ter conferido nenhuma das duas. Recalculei só as contas (Bari 2,864363, Capozzi 2,443867); a fonte não foi conferida por ninguém.

   *Conserto pedido:* Trocar 'independente' por 'conferência própria do construtor'; marcar Capozzi e Bari [DECLARADO, fonte não conferida] e dar o identificador do Bari ou tirar a linha.

## Para o operador (propostas do revisor, em língua simples; a gerência confere antes de ler a ele)

- O que o desenho do incremento decide: com a regra A (duas testemunhas) e sem uma segunda testemunha elegível, o canal só pode devolver ARMED_CONSISTENT ou TENSION; nenhum dos dois é falsificação. Isso é parede medida, não falsificação do pacote da escala (Um posto em 1 eV, m1 ≈ 0, a identificação com sen 45°).
- O que não decide: não move o gate, não é CONFIRMED. A frase 'mais provavelmente devolve tensão' vale só no mundo em que o valor verdadeiro é o centro público de hoje (7,388); no mundo em que a previsão é verdadeira, o resultado esperado é ARMED_CONSISTENT em 99,7 %. O texto não deve escolher entre os dois mundos por você.
- Escolha escondida a ler a você: o código selado lê 2,95σ no NuFIT porque arredonda o erro de 0,097 para 0,10; com o erro publicado do lado da previsão dá 3,02σ (tabela) ou 3,04σ (artigo) e o rótulo vira TENSION. Qual vale é decisão sua; TENSION não é falsificação.
- Em palavras de datas: o número de 207,2 dias é posterior à previsão publicada (22/01/2026 nos bytes guardados; 17/02/2026 publicada) e anterior ao hash da regra do código (08/08/2026). A amostra de 207,2 dias acumula a de 59,1, que já era pública antes do valor; a cegueira dita é a do número, não a dos dados. Nada aqui diz o que o autor leu.

## Consultas ao Mapa

- rotas.py consultar neutrino (45 rotas)
- rotas.py consultar m2 (50)
- rotas.py consultar JUNO (13)
- rotas.py consultar cronologia (8)
- rotas.py consultar degrau (16)
- rotas.py consultar retrodicao (6)
- rotas.py consultar NuFIT (4)
- rotas.py consultar SK-Gd (0)
- rotas.py ver neutrinos.m2.normalizacao (seq 59, 93, 98, 128, 142, 1095: a regra do global não é unívoca; perito = JUNO autônomo, R3)
- rotas.py ver estatistica.v412.k04_hubble_m2_combinacao (seq 2063, 2067, 2076: nao_refazer fixa a regra dos dois eixos na mesma frase)

## Examinado

- ENTREGA_K09.md (inteira) e conferência dos sha256 dos 10 artefatos da tabela (todos iguais)
- M2_DESFECHOS_E_SEGUNDA_TESTEMUNHA_K04.md (inteiro, 350 linhas)
- ERRATA_M2_K09.md, ERRATA_M2_K09_15nov.md, ERRATA_NEUTRINO_V412_DADOS_K09.json (inteiros)
- PRE_REGISTRO_INCREMENTO_JUNO_RASCUNHO_K09.md, INSUMOS_PARA_A_PERGUNTA_K09.md, REGISTRO_MAPA_K09.json, DEPOSITO_K09.md (inteiros)
- ORDEM_K09 e ADENDO_15nov (Parte 1) da gerência; LEITURA_K09_PARCIAL_NEUTRINO_15nov.md; REVISAO_K04_M2.md (itens 3 a 9); REVISAO_ERRATA_NEUTRINO_CORE.md (achados 1 a 15)
- CRONOLOGIA_NEUTRINO_15nov.json e os bytes do operador de 15/11 (725 B, sha256 49e5f007…, abertos por mim e conferidos)
- Rascunho de errata da gerência ERRATA_NEUTRINO_CORE_v412_RASCUNHO_c1_R1.md (as 422 linhas)
- um.py selado, faixas L2935-2957, L4220-4245 e L4589-4720; core um_absoluto.json (neutrino_m2 e neutrino_m2_perito_v392, leitura só)
- Regra congelada original: 02_frozen_neutrino_m2_v2.py e _resultado.json (sha256 e frozen_hash conferidos)
- docx de 22/01/2026 (sha256 83ba9e81…, texto, docProps) e .tex dos dois artigos de 2025 (12 padrões de fórmula, valor e JUNO)
- Varredura por script (207, 59, cega, prospectiv, antes, depois, anterior, posterior) em 14 arquivos do conjunto K09 e 7 arquivos antigos K01/K04
- Scripts próprios na pasta K09_A: conta_k09_A.py, diff_tabelas.py, varredura_eixos.py, conferir_fontes.py, conferir_artigos2025.py, olhar_core.py, olhar_perito.py
- NÃO examinei: Hubble, combinação/ringdown, as sete ressalvas, o PDF/Indico (sem rede), o conteúdo do Zenodo 17426652; não rodei scripts do Kimi.

