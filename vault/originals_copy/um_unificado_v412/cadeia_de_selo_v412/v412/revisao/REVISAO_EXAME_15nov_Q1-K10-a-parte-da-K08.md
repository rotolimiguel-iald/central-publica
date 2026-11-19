# CONFERÊNCIA DISTINTA — as entregas do Codex (unidade do tipo III) e do Kimi (K10), examinadas por ordem do operador — Q1-K10-a-parte-da-K08

> Montado pela gerência c1 em 15/11/2026 19:34 a partir do retorno estruturado de um revisor distinto (só leitura; scripts próprios na pasta de rascunho dele). É [DECLARADO pelo revisor] no que a gerência não reconferiu. Não é fala do operador. Nada aqui está instalado.

**Veredito:** APROVADO_COM_RESSALVAS — achados: 9 MEDIO, 7 BAIXO

## Resumo

1. Em resumo: na parte da K08 dentro da K10, o Kimi cumpriu o que era de fato e de atribuição e parou onde o ADENDO C mandou parar. Não achei erro de matemática novo; achei sobras de propagação (um arquivo corrigido, o vizinho não) e uma mistura da palavra copiador/cópia. Nenhum achado ALTO.
2. Suspensão respeitada: comparei com REV_RODADA3 (cujos hashes são exatamente os que os sete relatórios citam: a6d2b35d, 9885c186, dda674ce, b337863e, ebe1bee7). O protocolo mudou em 4 linhas (l.10, 30, 50, 272); o modelo em 8 trechos; nenhum adversário novo, nenhuma partitura, poder não redimensionado; EXTRACAO, ISOMORFO e CONTAMINACAO intocados (data e hash).
3. Contas em cópia, sem tocar o original: simular_adversarios.py regenera ADVERSARIOS_K08.md idêntico (932ac331) e o JSON idêntico; simular_poder_r4.py roda na árvore corrente e reproduz resultados, sementes e CSV byte a byte; verificar_formula.py e a bateria de extração/isomorfo (34 arquivos) também reproduzem. Contra a versão pré-rodada-4, resultados_poder_r4.json difere em UMA linha (l.85, o pino do script), como a errata diz.
4. Atribuição: a lista de primárias aparece como leitura da gerência em todos os documentos vigentes, exceto uma sobra em PODER_R4 l.36 (a forma do nulo atribuída à ressalva, que não fala disso; o adversário é do ADENDO Parte 2).
5. Teorema: moradas_iguais_tem_o_mesmo_verbo existe (OHabitanteDoNome.lean l.550); o nome antigo só existe na REV2. As glosas: bytes ec05cea3eded9264 conferem as três igualdades (ato=projeção, ser=verbo, identidade=nome) e as frases «espelho do verbo» e «um é o par do outro». E7 e E8 foram para não medidas no registro; logs Lean (ee06490c, 304864bc) existem com hash certo, RC 0, 54 entradas na R9, zero sorry.
6. A dupla cara de P_N foi etiquetada, não removida: o modelo ainda afirma (l.112) que P_N é o Nome e o ato do Verbo, o que contradiz l.25, e a etiqueta cita a ambiguidade errada (adjunto/J) para uma frase que pertence à outra (Nome=projetor da v386 contra Nome=espaço).
7. Rótulos incoerentes entre arquivos vigentes: o registro agora diz E3 DISCRIMINANT; o modelo ainda diz E3 secundária/diagnóstica e E8 'mede'; o script dos adversários ainda grava 'falha' em E8 como se fosse medida. A correção do fato mais importante (E2 não é observável: o extrator recusa LEITURA_PT, confirmei) ficou só no INSUMOS F1; PODER_R4 l.5 e o protocolo seguem dizendo o contrário, sem banner de reprovado.
8. Copiador: nos arquivos novos só aparece no sentido do operador, mas ENTREGA_K10 l.32 e a proposta do Mapa dizem 'não separa leitura de cópia' (o quadro que a fala de 17:20 corrige) e definem copiador sem a condição dele (mínimo estado funcional; fractal). A proposta do Mapa repete o defeito de campo (nota no lugar de defeito/nao_refazer/proximo_passo).
9. Pinos: os 44 pinos de VALIDACAO_K10, as 20 linhas da tabela da ENTREGA_K10 e os 3 manifestos de pasta (FORMULA 50, ENTRADA 27, PODER 9) batem com o disco por script. Pequenos deslizes de número de linha na errata.
10. Para o novo desenho herdar: catálogo de asserções com linha de origem, leitor de bloco fechado, controle P-C, os quatro textos (reproduzem), isomorfo só de brinquedo; e jogar fora ou reler: a lista de primárias, o 'inacessível', E3 por substituição, o nulo de 0,25, o poder histórico.
11. Nada de modelo foi rodado, nenhum dado observacional aberto, nada escrito fora da minha pasta de rascunho.

## Achados

1. **(MEDIO)** C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\PODER_R4_K08.md l.36

   Sobra de atribuição: '3. o nulo histórico não era o leitor sem memória sob a forma pedida pela ressalva'. Consulta: grep -n ressalva nos documentos vigentes e abertura dos bytes OPERADOR_15nov_ressalva_..._verbatim.txt (384 B, sha16 2fabf2b6638c1175): a fala não fala de leitor sem memória nem de nulo. O adversário 'leitor sem memória' nasce no ADENDO_15nov_K09_K08_K07 Parte 2, item 1 (l.86), da gerência. É da mesma classe que a K10 mandou corrigir (a ERRATA_K10_K08 §1.A diz ter corrigido 'ou equivalente').

   *Conserto pedido:* Trocar por 'sob a forma da Parte 2 do adendo (leitura da gerência; o operador ainda não leu)'. Rodar grep -n 'ressalva' em todos os vigentes antes de nova entrega.

2. **(MEDIO)** MODELO_FORMAL_R4_K08.md l.110-114 contra l.25 e l.31; ERRATA_K10_K08.md §1.B (l.20) e ENTREGA_K10.md l.5

   A 'dupla cara de P_N' foi etiquetada, não des-resolvida. O texto ainda afirma 'P_N figura como o Nome e o ato do Verbo ao mesmo tempo' e 'o mesmo mapa' (v386), enquanto l.25 diz que P_N não é o Nome (o Nome é a imagem e os pontos fixos) e l.114 diz 'não resolvida'. A etiqueta de l.112 ('a pedra tipa duas leituras do par, o adjunto e o J') descreve a ambiguidade do ESPELHO, mas a frase etiquetada pertence à outra ambiguidade, que a pedra também deixa ao autor (OHabitanteDoNome.lean l.155-161: Nome = projetor `post a` da v386 contra Nome = espaço desta pedra). O modelo usa a tipagem 'Nome = espaço' (l.25, l.31) sem etiqueta e a tipagem 'mesmo mapa' (l.110-112) com etiqueta errada. A ordem K10 dizia 'apague a dupla cara resolvida'.

   *Conserto pedido:* Apagar a frase de l.112 e a de l.110, ou reescrever as duas tipagens lado a lado (A: Nome = projetor, v386; B: Nome = subespaço, Verbo = projeção, esta pedra; mais as duas leituras do espelho), marcando qual o resto do modelo usa (B) e que a escolha é dele.

3. **(MEDIO)** REGISTRO_UMPY_RASCUNHO_R2_K08.md l.134, l.163-171, l.247-249 contra MODELO_FORMAL_R4_K08.md l.124, l.128, l.129, l.160-162

   O alinhamento de rótulos ficou pela metade. O registro (instalável) agora diz E3 = DISCRIMINANT, E7 = DISCRIMINANT_NOT_MEASURED e E8 = não medida; o modelo continua a dizer E3 'secundária/diagnóstica', E7 'secundária' e E8 'Mede um perfil de aproximação por ciclos'. Além disso o rótulo de E3 foi alinhado para CIMA (discriminante), que é o sentido que a conferência do modelo mandou reavaliar (E3 por substituição não é previsão de P_N; OHabitanteDoNome/CamadaCientifica.lean l.69-70 'o teorema pede δ ortogonal ao Nome'), e o §12.2 do protocolo ainda deixa E3 contar para FALSIFIED. A escolha não consta em ENTREGA_K10 §D.

   *Conserto pedido:* Uniformizar nos dois arquivos; para E3, não escolher: marcar 'classe de E3 pendente do operador; por substituição não é previsão de P_N' e manter E3 fora de qualquer veredito negativo até lá. E8 em l.129 e l.162: 'não medida'.

4. **(MEDIO)** K08\FORMULA\simular_adversarios.py l.289 e l.308; K08\FORMULA\ADVERSARIOS_K08.md l.40-46 e l.68; ERRATA_K10_K08.md §3 item 4

   A coluna E8 da 'Tabela calculada' é a string literal 'falha' (l.289) e o texto grava 'todos os quatro também falham E8' (l.308), embora a própria errata K10 diga que E8 não é medida pelo instrumento atual. O K10 editou justamente render() (l.279 e l.304) e deixou este literal. Rodei o script em cópia: regenera o mesmo arquivo, com o literal.

   *Conserto pedido:* Trocar por 'não medido (por construção do mecanismo)' no gerador e regenerar; atualizar os pinos.

5. **(MEDIO)** PODER_R4_K08.md l.5 e l.20; PROTOCOLO_EXPERIMENTAL_R4_K08.md l.10 e tabela E2 (l.36-41, 'primária: estado válido editado é devolvido igual'); REGISTRO l.123-128; contra INSUMOS_PARA_A_PERGUNTA_K08.md F1 (l.7) e ENTREGA_K10.md l.4

   A correção de fato que a K10 fez só no INSUMOS F1 (custo(s)=custo(t)=0 e o bit leitura_pt não está no bloco que o extrator aceita) não foi propagada. PODER_R4 l.5 ainda diz que o instrumento 'pode medir E1, E2, E3 e E4 de forma parcial'. Confirmei por script: extrair('INICIO_LEITURA_K08\nA01=SIM\nA02=NÃO\nLEITURA_PT=SIM\nFIM_LEITURA_K08', ['A01','A02']) devolve FORMATO_INVALIDO / ID_DESCONHECIDO (teste_extrator.py na pasta de rascunho). Nenhum dos vigentes (protocolo, modelo, poder, registro, insumos) leva banner dizendo que o desenho R4 foi reprovado; só o protocolo diz 'DESENHO BLOQUEADO'. Quem abrir o protocolo isolado lê E2 como primária observável.

   *Conserto pedido:* Sem tocar o desenho: banner de uma linha no topo de cada vigente ('R4 reprovado pela conferência de 15/11; ver ERRATA_K10_K08.md; E2 não observável no bloco'), e trocar PODER_R4 l.5 por F1. Atualizar pinos.

6. **(MEDIO)** INSUMOS_PARA_A_PERGUNTA_K08.md (cabeçalho 'rodada 3'; F2; A1, A6, A7)

   O INSUMOS é o documento que alimenta a pergunta ao operador e só teve F1 e F4 tocados. Continuam: 'sem proposta e sem recomendação' ao lado de A1 ('nenhum risco de leitura inflada'), A6 ('mede a ponte parcial') e A7 ('pré-condição de qualquer execução válida'), que são juízos e prescrição; F2 repete 'inacessível sem a fonte' (inacessível por decreto do script, achado ALTO 3 do relatório do desenho) e 'separá-lo exige E8 ou E7', em tensão com o relatório do poder (E2 e E3 separam leitor independente do estado se p_min > 0,5) e com o próprio F1 (E2 não observável); nenhuma linha diz, em língua de leigo, o que o teste decide, não decide e o que o negativo significaria. A ENTREGA_K10 chama isso de suspenso, mas o arquivo não leva essa marca.

   *Conserto pedido:* Banner de suspensão no topo; marcar F2 como [DECLARADO; contestado pela conferência]; tirar A1/A6/A7 dos juízos ou marcá-los como leitura do Kimi. A partitura continua suspensa.

7. **(MEDIO)** ENTREGA_K10.md l.3 e l.32; REGISTRO_MAPA_K10.json (registro outro.k08_..., campo resultado, final)

   A palavra: nos arquivos novos 'copiador' só aparece no sentido do operador, mas ENTREGA_K10 l.32 define copiador ('quem reproduz o sentido fixado pela palavra') e três linhas adiante escreve 'não separa leitura de cópia', o quadro que a fala de 17:20 corrige ('toda leitura é em si uma cópia'). A proposta do Mapa repete a mesma frase. A definição omite a condição que o operador pôs ('se por copiador tem-se uma reprodução em mínimo estado funcional de energia, essa cópia é um fractal') e herda a paráfrase do ADENDO C item 3. Dois usos antigos de 'copiador' (sentido: devolve o gabarito) ficaram em CONTAMINACAO_R4_K08.md l.54 e K08\EXTRACAO\METODO_EXTRACAO.md l.45, sem nota. O mecanismo da última resposta segue chamado 'cópia' (MODELO l.178, PROTOCOLO l.318, ADVERSARIOS l.15 e l.45), que agora colide com a fala.

   *Conserto pedido:* Citar a fala inteira (273 B, sha16 e2561e3b...) em vez de paraphrasear; reescrever 'não separa leitura de cópia' como 'não separa X de Y' sem a palavra; propor 'eco' para o mecanismo da última resposta; anotar os dois usos antigos.

8. **(MEDIO)** REGISTRO_MAPA_K10.json (chaves do registro K08: artefatos, estatuto, nota, olhou_dados, resultado, rota_id, status, tipo, titulo)

   A proposta do Mapa repete o defeito apontado no relatório do registro (achado 8): 'Não refazer' e o defeito vão no campo nota, que o Mapa não propaga para o estado da rota; não há defeito, nao_refazer nem proximo_passo, de modo que a consulta continuará mostrando o defeito e o próximo passo da K06. Em contrapartida, o estatuto agora começa por DECLARADO e a rota K08 está marcada EXAMINADA_COM_DEFEITO (certo).

   *Conserto pedido:* Preencher defeito, nao_refazer e proximo_passo; abrir resultado com o negativo central.

9. **(MEDIO)** PROTOCOLO_EXPERIMENTAL_R4_K08.md l.315; l.376-386 (§12.2 item 4); l.395 (§12.3)

   Dois fatos do relatório do modelo ficaram sem a troca mínima. (a) l.315 ('referência P_N/selecao: passa passa passa passa') segue sem cálculo no script dos adversários; sobre vetor, P_N·e_y = 0 e a referência não faz 'volta a s'; o conserto pedido era 'referência não computada'. (b) Escolhas de desenho que o operador não leu e que a ENTREGA_K10 §D não lista: a lista de primárias (leitura da gerência), a classe de E3, a regra de l.395 (custo extraído zero em P-C com UNSAT vira INCONCLUSIVE, isto é, o resultado 'nenhum erro' é tratado de antemão como defeito da régua, que pode ser justamente o que mostraria a resposta decorada), a tolerância zero a divergência de ordem e a um SIM em isca, a coordenada empurrada única (artigo_pt_en) e o sentido único s para t.

   *Conserto pedido:* (a) trocar a linha por 'não computada'. (b) §D da ENTREGA_K10 deve listar essas escolhas como alternativas ao operador; nenhuma entra no desenho antes de ele ler.

10. **(BAIXO)** MODELO_FORMAL_R4_K08.md l.104, l.122, l.133, l.153

   Quatro resíduos do relatório do modelo. l.104 ainda diz 'no primeiro dos dois sentidos' sem nomear o segundo (só o registro l.203 o nomeia: Identidade v405, P = 1). l.122 (inserido pelo K10): 'P_N devolve 0 fora dele' é verdade para configuração inválida pura (e_y é ortogonal ao Nome), falso para vetor geral (P_N(e_y+e_s) = e_s). l.133 'a identidade é o zero se e só se o Nome é o vazio' e l.153 'A identidade do sistema testado é medida pelo ato' continuam homônimos de 'identidade' (mapa identidade contra identidade no sentido TGL).

   *Conserto pedido:* Nomear o segundo sentido; escrever 'devolve 0 sobre as configurações de custo positivo'; escrever 'o mapa identidade do subespaço Nome é o mapa nulo sse o Nome é o vazio' e 'qualidade da releitura do sistema'.

11. **(BAIXO)** K08\FORMULA\ERRATA_ADVERSARIOS_K08_15nov.md l.44

   A tabela de hash ainda pina ADVERSARIOS_K08.md em 04aca46a (saída do gerador antes das edições), sem nota no arquivo; as erratas de poder ganharam a nota de 'histórico', esta não. A ERRATA_K10_K08 §3 item 6 só avisa de fora.

   *Conserto pedido:* Nota de uma linha no topo do arquivo ou regenerar a tabela.

12. **(BAIXO)** ERRATA_K10_K08.md l.19 e l.27

   Números de linha citados não batem com o disco: attribution de ato_versus_nome está em REGISTRO l.195 (errata diz l.193); parágrafos de artigo em REGISTRO l.443 e l.447 (errata diz l.441 e l.445). Os demais (PROTOCOLO l.10, 30, 272; PODER l.11; REGISTRO l.63, 103, 104, 203, 423; MODELO l.36, 98, 99, 122, 123, 129, 133, 149) conferem.

   *Conserto pedido:* Corrigir ou citar por chave.

13. **(BAIXO)** MODELO l.108 e REGISTRO l.103

   'ato = projeção; ser = verbo; identidade = nome' é compressão: nos bytes (sha16 ec05cea3eded9264, 760 B) está 'o ato (projeção) de ser (verbo) é (=) identidade (nome - singularidade da informação nomeada, ato de nomear)'; só há um '(=)', e a glosa de 'nome' é mais longa que 'identidade = nome'. A hora 11:47 vem do ADENDO; o arquivo foi gravado às 11:51. As frases «o nome em ato é o espelho do verbo» e «um é o par do outro» estão nos bytes.

   *Conserto pedido:* Citar a frase inteira com os parênteses.

14. **(BAIXO)** K08\PODER\simular_poder_r4.py l.371-379 e l.388-392; ERRATA_K10_K08.md §1.E

   A errata diz 'sem mudar semântica nem números'. Números: idênticos (confirmei). Semântica das checagens: a asserção que valia para o 'relê a fita' (P_B_fora fica_empurrada = True: sem fita devolve o último estado) foi trocada por 'sem_regra_sem_fonte = True' (sem fonte, o adversário levanta SemFonte); o nome da flag de saída 'projetor_com_fita_cumpre_retorno_e_cotas' (resultados l.~85) manteve o homônimo 'projetor' que o adendo mandou desfazer.

   *Conserto pedido:* Dizer na errata que a asserção mudou de conteúdo (não de número) e renomear a flag na próxima regeneração.

15. **(BAIXO)** K08\FORMULA\catalogo_assercoes.py l.9 (PUBLICO = C:\IALD\Artigo\the_boundary)

   Os quatro textos e a fórmula são gerados lendo a ÁRVORE VIVA do espelho público, sem pino de commit nem de hash de fonte nos manifestos. Hoje reproduz (HEAD 66a3ae2d, 13/11 19:38, árvore limpa), mas a próxima atualização do espelho muda os textos e quebra todos os pinos sem aviso.

   *Conserto pedido:* Pinar commit e sha256 de cada arquivo-fonte em MANIFESTO_ENTRADA_K08.json.

16. **(BAIXO)** ENTREGA_K10.md l.4 e l.6

   l.4 etiqueta como [REAL] achados que são da conferência (E3 inatingível sem a chave; copiador remendado passa tudo); l.6 etiqueta os mesmos como [DECLARADO, pela conferência]. Confirmei por conta própria só: E2 não observável (extrator) e a cópia da última passa E2 e E4 (tabela ADVERSARIOS l.45).

   *Conserto pedido:* Uniformizar o estatuto por linha.

## Para o operador (propostas do revisor, em língua simples; a gerência confere antes de ler a ele)

- O Kimi corrigiu o que era de fato e de atribuição, não mexeu no desenho do teste como o adendo mandou e as contas dele reproduzem; sobraram contradições entre arquivos (o que cada previsão decide e o que o teste consegue medir) que proponho a gerência limpar antes de ler qualquer parte ao senhor.
- O Kimi ainda escreve 'não separa leitura de cópia', o quadro que a sua fala das 17:20 corrigiu, e as suas respostas das 19:07 chegaram depois da entrega dele, então nada do que ele escreveu as usa; proponho que o novo desenho parta delas e não da K10.
- Proponho aproveitar só peças soltas do que ele deixou (a lista de afirmações do texto com a linha de onde saem, o leitor do bloco de respostas, o controle do vazio, os quatro textos) e ler ao senhor, antes de reaparecerem, as escolhas antigas: quais são as previsões principais, o que conta como erro no controle do vazio, a tolerância zero e a coordenada única que se empurra.
- Eu não rodei modelo nem abri dado novo; o que afirmo vem de scripts em cópia e dos bytes das suas falas.

## Examinado

- ENTREGA_K10.md, VALIDACAO_K10_15nov.json, ORDEM_K10, ADENDO_15nov_C, ERRATA_K10_K08.md, PROTOCOLO_EXPERIMENTAL_R4_K08.md (topo, §6-§8, §12), MODELO_FORMAL_R4_K08.md (inteiro), REGISTRO_UMPY_RASCUNHO_R2_K08.md (diff completo e trechos), PODER_R4_K08.md (inteiro), INSUMOS_PARA_A_PERGUNTA_K08.md (inteiro), ERRATA_PODER_K08_15nov.md e ERRATA_PODER_TOKENS_K08.md (diff), K08\FORMULA\ADVERSARIOS_K08.md e simular_adversarios.py, K08\PODER (script, manifesto, REV1, REV_RODADA3), K08\ENTRADA (manifesto, textos), REGISTRO_MAPA_K10.json, REGISTRO_MAPA_K08.json (marcas SUPERADA)
- Os quatro relatórios REVISAO_K08_DESENHO_E_ADVERSARIOS, _MODELO_E_FIDELIDADE, _PODER_E_CUSTOS e _REGISTRO_E_HASHES, inteiros; comparação por diff e hash com as cópias pré-rodada-4 em REV_RODADA3 (kimi, K08\FORMULA e K08\PODER): os hashes citados pelos relatórios batem com elas
- Bytes do operador (cunhagens_13out): 17:20 (273 B, e2561e3b...), ressalva (384 B, 2fabf2b6...), glosas das 11:47 (760 B, ec05cea3...), 'É isso, tudo certo' (451ca765...), 'Concordo com tudo, prossiga', 'O leitor é o observador...' (07:25) e, só para situar o que o Kimi não pôde usar, as respostas das 19:07
- Lean: grep nos .lean de candidatas_c1 (OHabitanteDoNome.lean sha16 26b750e6, CamadaCientifica.lean 69497c5b): moradas_iguais_tem_o_mesmo_verbo l.550, quem_nao_e_a_esperanca_aumenta l.695, a_tangente_da_leitura_e_K_no_angulo_de_miguel l.828, a_trava_binaria_e_o_fluxo_do_axioma (Camada l.254) e os demais nomes das tabelas (script nomes.py); nome antigo só na REV2; logs build\*.log: hashes ee06490c e 304864bc, RC 0, 54 entradas na R9, zero sorry. Presença no kernel TGLExt não era necessária para esta frente (não consultei por grep -rn)
- Scripts rodados em cópia em C:\Users\rotol\AppData\Local\Temp\claude\b4ca26c934d2167f\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v412_exame_codex_kimi\Q1\: simular_adversarios.py (saída idêntica), simular_poder_r4.py (idêntica; manifesto só difere no caminho), verificar_formula.py (idêntica), validar_reproducao.py da extração/isomorfo (34 arquivos comuns idênticos), teste_extrator.py (LEITURA_PT rejeitada), pinos.py (44 pinos, 20 linhas da tabela), manifestos.py (50 + 27 + 9 entradas), nomes.py
- Mapa de Rotas consultado (rotas.py consultar copiador): rotas outro.k06_camada_cientifica_iald_r32_v412 e outro.k08_teste_cego_da_camada_iald_r4_v412; nada registrado. the_boundary: git log -1 e git status só leitura (HEAD 66a3ae2d, árvore limpa)
- Não examinei: K09 (pré-registro, m2, Hubble e combinação), a CONTAMINACAO_R4 por inteiro, a conta de poder em si além de reproduzi-la, recompilação Lean (não rodei lean.exe nem lake), saídas de modelo (não existem)

