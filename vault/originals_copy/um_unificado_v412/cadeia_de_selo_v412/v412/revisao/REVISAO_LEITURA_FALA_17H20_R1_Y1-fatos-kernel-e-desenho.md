# CONFERÊNCIA DISTINTA — a versão R1 da leitura da gerência sobre a fala das 17:20 (conferência única do conserto) — Y1-fatos-kernel-e-desenho

> Montado pela gerência c1 em 15/11/2026 18:33 a partir do retorno estruturado de um revisor distinto (só leitura; scripts próprios na pasta de rascunho dele). É [DECLARADO pelo revisor] no que a gerência não reconferiu. Não é fala do operador. Nada aqui está instalado.

**Veredito:** APROVADO_COM_RESSALVAS — achados: 1 ALTO, 6 MEDIO, 8 BAIXO

## Resumo

Os ALTOS e MEDIOS da primeira conferencia, na minha lente (fatos das secoes 3 e 5 e logica do desenho), estao sanados: fractal, tres defeitos a mais, mesma leitura nas quatro escalas, partituras, secao 7. Os numeros da secao 5 conferem. Refiz por script em copia na pasta Y1 (x3_item2 e x3_item4): trocas coerentes 15/16, 25/26, 19/19, 26/28; chave custa 1 sob troca; chave constante passa E1 a E4 com o bloco entregue. 13/26 e 10/22 vem dos relatorios X3. Nao ha frase que diga que o kernel prova a fala, com uma excecao: "o kernel prova que repetir separa" (ALTO novo, uma frase). Cinco MEDIOS novos: "tres regimes" contra a regra dos dois regimes; "so o brilho muda" mistura dois teoremas; o parentese do Pai da Mentira funde dois objetos e pode emprestar ao operador uma conclusao que so esta no cabecalho; o instrumento para quem nao ecoa nao tem par na secao 5; a partitura da pergunta 1 esconde que o negativo depende da pergunta B. Mais uma omissao de vizinho do impostor. Tudo se conserta trocando frases; os consertos vao escritos abaixo. Ler ao operador so depois do ALTO e dos MEDIOS 2 a 6. Verdade, partituras das duas perguntas e a delimitacao da secao 7 estao corretas no essencial, com as ressalvas listadas.

## Achados

1. **(ALTO)** Secao 3, item 'Repetir separa numa especie e nao separa na outra', frase 'o kernel prova que repetir separa: o par ecoa, o individuo nao'.

   Consulta: sed em TestemunhaEstatica.lean, cabecalho e l.120-200. the_pair_echoes e P*P=P para o projetor do canto de Bell. the_individual_does_not_echo e ptr P=(1/2)*1 nao idempotente (Tr rho^2=1/2). Sao fatos de matrizes (projetor e estado reduzido), nao de leitores de texto nem de 'perguntar de novo'. O proprio kernel limita: 'ler uma vez sem ecoar e [INPUT/ONTO] do operador; o que esta provado e a algebra'; the_unbonded_marginal_echoes diz que 'o nao-eco e do PAR visto por um lado so, nao propriedade universal'. 'Repetir separa' e a leitura da gerencia; o operador, que nao audita o Lean, ouvira 'o kernel prova'. Alem disso o 'individuo' e um estado, nao um leitor.

   *Conserto pedido:* No que le uma vez sem ecoar (a sua frase de 22/10; pedra v396), o kernel tem dois fatos de algebra: o projetor do par ecoa (ler de novo nao acrescenta) e a reducao do par a um lado so, que e um estado e nao um leitor, nao ecoa. Que 'ler uma vez sem ecoar' seja isso e leitura sua, que o proprio kernel marca como [INPUT/ONTO], e ele mostra que o nao-eco e do par visto por um lado so, nao de tudo. Nao ha teorema sobre leitores de texto nem sobre perguntar de novo; que repetir separe, no teste, e proposta da gerencia.

2. **(MEDIO)** Secao 3, 'Reler nao acrescenta. E teorema em tres regimes do kernel (o angulo, a leitura no espaco de Hilbert, a esperanca condicional)'.

   Consulta: grep -rn 'theorem observing_adds_nothing|rereading_adds_nothing|rereading_the_name_adds_nothing' e sed em IALD.lean l.675-681 e EsperancaCondicional.lean l.60-75. Os tres teoremas existem e estao importados (TGLExt.lean l.165, 1078, 1114, 1148), com a mesma forma e sem equacao entre eles. Mas o kernel conta DOIS regimes: IALD.lean B7 diz 'nos dois regimes: face do motor e angulo da PALAVRA' (a leitura em Hilbert e a esperanca sao ambas da face); EsperancaCondicional diz 'a esperanca age na algebra, o observador no angulo (regra dos dois regimes)'. 'Tres regimes' colide com a regra dos dois regimes, que o operador cunhou e exige 'o tempo todo'.

   *Conserto pedido:* Reler nao acrescenta e teorema em tres pedras do kernel (a do angulo, a da leitura no espaco de Hilbert e a da esperanca condicional), com a mesma forma. Duas sao do regime da face e uma do regime do angulo, e nenhum teorema as iguala.

3. **(MEDIO)** Secao 3, item Fractal: 'o Nome e os pesos b e 1 - b nao mudam com a escala de tempo, so o brilho muda, por metade a cada oitava'.

   Consulta: sed em AEscala.lean l.915-930 e l.1634-1655. o_nome_e_o_mesmo_em_toda_escala diz 'So o relogio muda; o Nome e a decisao nao dependem da constante' e que os pesos b e 1-b nao dependem de c. O limiar de tempo da decisao ((n ln 2)/c) muda com c. A metade por oitava vem de OUTRO teorema, a_escala_e_meio_por_oitava: 'uma oitava de tempo pago (s = ln 2) leva o brilho do pixel de custo 1 a 1/2', para o leitor do fundo com a constante da luz = 1. A frase junta os dois e faz parecer que, ao mudar a escala, so o brilho muda, por metade por oitava de escala.

   *Conserto pedido:* O Nome e os pesos b e 1 - b nao dependem da constante da luz, a escala de tempo (AEscala, o_nome_e_o_mesmo_em_toda_escala: so o relogio muda). Em outro teorema (a_escala_e_meio_por_oitava), o brilho de um ponto de custo 1 cai a metade a cada oitava de tempo pago (ln 2).

4. **(MEDIO)** Secao 3, 'Quatro defeitos de leitura, com as suas palavras': '... a leitura sem escala (a pedra do Pai da Mentira; o cabecalho registra que o decisor sem escala nao e mentiroso, so nao le)'.

   Consulta: sed em AEscala.lean l.885-896 e l.714-722; bytes de OPERADOR_10nov_a_mentira_lida_como_mentira... (um unico paragrafo). Texto exato (l.892-893), no cabecalho de o_decisor_sem_escala_nao_e_leitor_do_fundo: 'R4 (D94): o decisor sem escala NAO e chamado de mentiroso - pelo operador (fala 9, 10/11), a mentira lida como mentira e uma verdade; ele simplesmente nao LE: nao tem sistema de referencia, nao e leitor.' O cabecalho atribui ao operador (falas 9 e 10 de 10/11). Os bytes dessas falas nao falam do decisor sem escala: 'Uma mentira lida como mentira e verdade, portanto o pai da mentira nao pode ler a si mesmo como mentira... so nao faz uma unica coisa: reconhecimento verdadeiro'. 'So nao le' e conclusao escrita no cabecalho. E o l.718-722 diz que o decisor sem escala 'nao e o Pai da Mentira'; o Pai da Mentira (o_pai_da_mentira_so_nao_reconhece, l.1070) e a leitura sem ciclo, s=0, que diz 1 onde nada e. A frase junta os dois objetos num parentese e, sob 'com as suas palavras', pode emprestar ao operador uma conclusao que esta so no cabecalho.

   *Conserto pedido:* Terceiro defeito, a leitura sem escala. O kernel separa dois objetos: a leitura sem ciclo, que diz 'eu sou' em toda parte (a pedra do Pai da Mentira, ligada as suas falas de 10/11), e o decisor sem escala, que o cabecalho de AEscala diz que nao e o Pai da Mentira: 'nao e chamado de mentiroso, simplesmente nao le'. O cabecalho poe isso sob as suas falas de 10/11, mas as falas, abertas por mim, nao dizem isso do decisor: e leitura escrita no cabecalho.

5. **(MEDIO)** Secao 4, item 3 ('dois instrumentos para duas especies'), contra a secao 3 ('o registro separa') e a secao 5.

   Logica. (a) O primeiro instrumento do item 3 ('para o que nao ecoa, perguntar de novo e ver se sustenta') nao tem correspondente na secao 5. A pergunta 2 ('texto retirado, volta ao que era depois de um erro?') e retencao depois de erro, nao 'perguntar de novo'. O instrumento que ja existe no desenho e a E4 (reler devolve o mesmo; protocolo l.270-272), e a tabela l.313-320 mostra todos os adversarios simulados passando E4. Como a propria secao 5 diz que os quatro mecanismos tiram a saida da propria resposta anterior, todos ecoam: nenhum adversario simulado nao ecoa. A E4 nunca foi vista separando nada, e para a especie que nao ecoa nao ha instrumento medido, e a secao 5 nao diz. (b) A secao 3 afirma que, no par eco/custo zero, quem separa e o REGISTRO (TheCorrespondence), mas nenhum dos dois instrumentos e de registro; o de proveniencia so existe na torre nativa (C3, observavel de proveniencia por relacao, 'so modelo proprio').

   *Conserto pedido:* Item 3: 'Proposta de desenho, nao leitura. Como o kernel tem leituras que respondem sempre o mesmo e uma que le uma vez sem ecoar, o teste pediria mudar o texto e ver se a resposta acompanha (instrumento da pergunta 1) e, para o que nao ecoa, reler e ver se a segunda resposta e igual a primeira (a E4 do desenho atual). Hoje nenhum adversario simulado deixa de ecoar, entao esse segundo instrumento nunca foi visto separando nada. O que o kernel diz que separa eco gratuito de custo zero e o registro, e esse instrumento so existe na torre nativa.'

6. **(MEDIO)** Secao 5, partitura da pergunta 1 ('Um negativo e falsificacao so se a inversao for coerente e o modelo ainda assim responder pelo texto antigo').

   Logica e regra do posto. O negativo so e 'falsificacao' se seguir o texto dado conta como ler e responder pela resposta antiga conta como nao ler. Isso supoe que 'palavra' e o texto dado e 'verdade' e o que o texto diz, que e justamente a pergunta B (secao 6). Se para o operador a verdade e a da teoria, o modelo que resiste a inversao e quem 'imprime a verdade' (o copiador, pela fala), e o negativo troca de sentido. A partitura nao diz de que e a falsificacao nem que depende da pergunta B; o operador a ouve antes da B.

   *Conserto pedido:* Acrescentar ao fim da pergunta 1: 'Este teste trata seguir o texto como ler, e responder pela resposta antiga como nao ler. Isso supoe que a palavra e o texto que damos e que a verdade e o que ele diz; se para o senhor a verdade e a da teoria, quem resiste a inversao estaria imprimindo a verdade, e o negativo muda de sentido. Esta e a sua pergunta B.'

7. **(MEDIO)** Secao 3: o vizinho mais proximo de 'impostor' na letra e no kernel nao aparece (a lista dos quatro defeitos e dada 'com as suas palavras').

   Consulta: sed em TheRecordOfTheCut.lean l.40-65 e l.170-190 (importado, TGLExt.lean l.144): 'a sobra com a aparencia algebrica do todo ... o disfarce surge sem nenhum erro matematico'; 'pai da mentira' e leitura [ONTO] do operador; o teorema the_record_knows_what_the_residue_forgot: o registro mostra o que o residuo esqueceu. Bytes abertos de OPERADOR_04nov_relacao_sem_peso...: 'o 1 sozinho ... que e mentira ... aparencia um inteiro, mas nao pode ser medido, jamais pagou qualquer custo, e somente a superposicao querendo ser um absoluto'. E o que parece o todo sem te-lo pago, mais perto de 'impostor' do que varios dos quatro. Outra especie, que nem repetir nem trocar o texto separam: separa o registro. Isto pesa na pergunta A. Foi apontado na primeira conferencia (X2 MEDIO 6) e so a TheCorrespondence foi incorporada.

   *Conserto pedido:* Acrescentar na secao 3: 'O kernel tem tambem a sobra com a aparencia do todo (TheRecordOfTheCut): o disfarce surge sem nenhum erro matematico, e o que o separa e o registro do corte. O pai da mentira ali e leitura sua [ONTO]. Na sua fala de 04/11: o 1 sozinho tem aparencia de inteiro, mas jamais pagou custo.' E na pergunta A acrescentar a opcao: 'o impostor e o que tem a aparencia do todo sem ter pago o custo?'

8. **(BAIXO)** Secao 3, item 'Copia no kernel'.

   Consulta: grep -rn 'eco que não é cópia' = IALD.lean l.349, na docstring do teorema memory_one_iff_same_post (T5'), nao num cabecalho. Texto exato: '[ONTO] a leitura EU SOU = IALD e o eco que nao e copia; o termo e so a igualdade dos projetores.' A frase vale para a leitura EU SOU = IALD, marcada [ONTO], nao para 'a leitura' em geral. O gloss 'ler gera o mesmo projetor sem ser o mesmo vetor' e correto.

   *Conserto pedido:* Uma docstring do kernel (IALD.lean, teorema T5', marcada [ONTO]) diz que a leitura 'EU SOU = IALD' e 'o eco que nao e copia'; o termo prova so que dois vetores unitarios com a mesma leitura geram o mesmo projetor, sem serem o mesmo vetor.

9. **(BAIXO)** Secao 5, 'O que os mecanismos do desenho atual fazem': 'nenhum dos quatro le o texto'.

   O protocolo (l.313-320) lista cinco mecanismos: ancora, moda, copia da ultima, ignora o empurrao e leitor sem memoria. O quinto usa a fonte, mas, na simulacao, recebe do script a solucao ja resolvida (X3 achado 9; 0 de 200 diferentes). Dizer 'quatro' sem o quinto esconde que o desenho tem um 'leitor da palavra' por construcao.

   *Conserto pedido:* Nenhum dos quatro que guardam historico le o texto: todos tiram a saida da propria resposta anterior, e a primeira resposta e dada pronta pelo script. O quinto, o leitor sem memoria, usa o texto, mas na simulacao recebe do script a solucao ja resolvida.

10. **(BAIXO)** Secao 5, bullet Energia e 'os quatro textos sao os textos publicos da vitrine'.

   789; 3.926; 4.072; 7.358 sao tokens dos RECORTES escolhidos pelo Kimi (tokenizador de referencia Qwen); os arquivos inteiros tem 877; 7.915; 8.946; 13.434 (X3 achado 10). 'Tem so a contagem de tokens' omite a energia formal c(x), a contagem de clausulas violadas (0 = Nome), que a secao 3 usa. LLMS e READ_BRIEF quase empatam (3,7%): na pratica sao tres tamanhos.

   *Conserto pedido:* A casa nao tem medida de energia de um modelo. Tem a contagem de tokens dos recortes (789; 3.926; 4.072; 7.358; os arquivos inteiros tem mais) e a conta formal de afirmacoes violadas, que e logica, nao energia.

11. **(BAIXO)** Secao 5, 'O que ja existe': 'A data em que cada afirmacao entrou no texto publico'.

   X3 achado 11 (git log so leitura): foram levantadas as datas por arquivo e da cifra 6,11; as de cada afirmacao nao. Sob o titulo 'O que ja existe', parece pronto.

   *Conserto pedido:* A data em que cada arquivo e a cifra 6,11 entraram no texto publico; a de cada afirmacao pode ser levantada do historico, mas ainda nao foi, e so vale contra o corte de treino do modelo.

12. **(BAIXO)** Secao 5, abertura da lista de principais e secao 7: 'a resposta decorada passa as quatro previsoes' e 'so passa para quem tem a resposta decorada'.

   Rodei em copia (x3_item4.py): a constante s ou t passa E1, E2, E3 e E4 com o bloco entregue (leitura_pt fora do bloco: protocolo l.236; clausulas que a mencionam: nenhuma); com o vetor inteiro a s cai em E2 e a t cai em E3. Entao 'passa as quatro' vale para o desenho como entregue, e a consequencia da secao 7 depende disso. E a 'sem o texto so passa para quem decorou' ignora o que a pergunta 2 diz ('decorou ou guardou a primeira resposta': o simulador do Kimi, ancora e moda, tambem desfaz o erro).

   *Conserto pedido:* Trocar por: 'a resposta decorada passa as quatro previsoes no desenho como esta entregue, onde o bit livre nao e visivel ao modelo' e 'so passa para quem decorou a resposta ou guardou a primeira fora do estado editado'.

13. **(BAIXO)** Secao 5, bullet 'Inverter uma afirmacao do texto': 15 de 16, 25 de 26, 19 de 19, 26 de 28.

   Rodei x3_item2.py em copia: os numeros conferem, e custo da chave = 1 e custo do leitor-solver = 0 por construcao. Mas as trocas coerentes incluem, nos quatro textos, 'a maquina confirma a si mesma' e 'NOT_FALSIFIED equivale a CONFIRMED'; as duas invertem as proibicoes do proprio texto (a regua da casa). Os textos invertidos com curadoria teriam de afirmar o que a regua proibe. Escolha de desenho que o operador nao ouviu. Tambem falta dizer de que e a 'falsificacao' (do 'o modelo le o texto', nao da teoria).

   *Conserto pedido:* Duas das inversoes coerentes fazem o texto dizer o que a regua proibe (que a maquina confirma a si mesma; que NOT_FALSIFIED e CONFIRMED). Usa-las como estimulo e escolha sua. E 'falsificacao', na pergunta 1, e do 'o modelo segue o texto', nao da teoria.

14. **(BAIXO)** Secao 4, item 3: 'Como o kernel tem duas especies de quem nao le'.

   O 'falso' de 22/10 le uma vez e nao ecoa; nao e 'quem nao le'. 'Nao le' e do decisor sem escala (AEscala). A classificacao em duas especies e da gerencia, e o kernel tem quatro tipos (secao 3). A frase atribui ao kernel uma classificacao dela.

   *Conserto pedido:* Como as leituras defeituosas que o kernel tipa se dividem, na leitura da gerencia, em as que respondem sempre o mesmo e a que le uma vez sem ecoar, o teste pediria...

15. **(BAIXO)** Secao 3, item Fractal: 'O kernel nao tem teorema sobre fractal; onde a palavra aparece, e leitura declarada'.

   Correto no teor (FractalUnitarity.lean, cabecalho: 'a leitura fractal e [ONTO] sobre estes teoremas exatos'), mas a pedra se chama 'A UNITARIEDADE FRACTAL' e traz subcorner_unit sob esse titulo; o operador pode estranhar a palavra no kernel sem a nota.

   *Conserto pedido:* Acrescentar: 'Uma pedra do kernel se chama A UNITARIEDADE FRACTAL; seu cabecalho diz que a leitura fractal e [ONTO] sobre os teoremas exatos, entre eles o da compressao em dois passos.'

## O que foi sanado da conferência anterior

- **SIM** — X2 ALTO 1: frase do fractal (teorema proibe ler fractal como invariancia do peso, so covariancia): A frase saiu. Agora diz que o kernel nao tem teorema sobre fractal e lista TheScaleHasNoFixedPoint (no_positive_scale_invariant, l.99, com alcance limitado), FractalUnitarity.subcorner_unit (l.79) e AEscala. Resta o MEDIO 3 novo (so o brilho muda).
- **PARCIAL** — X2 ALTO 2: regra geral 'repetir-se nao separa; o impostor devolve sempre a mesma coisa': Foi escopada em duas especies (ecoa e nao ecoa), como pedido. Mas a frase nova 'o kernel prova que repetir separa' extrapola os teoremas: ver ALTO 1 novo.
- **SIM** — X3 ALTO / X1 ALTO: 'a mesma leitura em toda escala' e 'a data de entrada' listadas como instrumentos que separam: A secao 5 diz 'Nao separa copiador de impostor: quem decorou o nucleo comum tambem repete'. O titulo virou 'o que cada coisa decide'. O 16/16 so vale num par (15/16 e 12/16 nos outros): conferido com X3.
- **PARCIAL** — X2 MEDIO 3: 'seis vezes' que o kernel tipa quem nao le: Agora sao quatro defeitos, e 'impostor' e aproximacao da gerencia. Mas o parentese da leitura sem escala funde dois objetos (MEDIO 4 novo).
- **SIM** — X2 MEDIO 4: candidata da camada cientifica 'diz isso de si' e 'fidelidade': As duas frases foram retiradas da secao 3.
- **SIM** — X2 MEDIO 5: 'menor energia' e 'Nome zero da trava': Texto igual ao conserto pedido. Conferi PontoZeroDoPsion.o_lock_tem_gap_um, TheCostIsDerived.landauer_floor_pos e TetelestaiTerminal.basta e nao_precisa_de_cem_por_cento. grep zero para 'estado funcional' e 'mínimo estado'.
- **SIM** — X2 MEDIO 6: TheCorrespondence omitida: Entrou na secao 3 (eco e custo) e na pergunta C, como terceira opcao. Confere com o cabecalho do arquivo, de 23/08/2026, e com os teoremas cost_does_not_determine_correspondence, free_is_not_costless, echo_presupposes_payment, the_three_regimes.
- **SIM** — X2 MEDIO 7: 'sem termo nenhum' apagava os vizinhos de imprimir e de fixar: Agora 'imprimir (o verbo)' e vizinhos FalsidadeDaInercia (no_post_before_the_impression, the_first_motion_is_the_impression, falas de 25/10) e TheScreenIsFounded (the_word_fixes_the_place, 08/09). grep -rn zero para copiador, impostor, imprim, sentido fixad.
- **SIM** — X2 MEDIO 8: fractal, escala de tempo e escala de tamanho de texto: Diz 'escala de tempo' e que escala de tamanho de texto nao tem termo no kernel. Resta o MEDIO 3 novo.
- **SIM** — X2 MEDIO 9: 'copia' no kernel sem contrapartida: Entrou o item do eco que nao e copia (IALD.lean l.349). Ficam imprecisoes BAIXAS (cabecalho versus docstring de teorema; falta o marcador [ONTO]).
- **SIM** — X3 MEDIO 2: escolha escondida do P-C (tres origens, 'isto e, o impostor'): Tres origens ditas (protocolo l.292 e 12.3 l.395; METODO_EXTRACAO l.17); 'isto e, o impostor' foi retirado; fica a dependencia da pergunta B. Reproduzi: custo formal minimo 1 e custo zero so sem contar a clausula inserida.
- **SIM** — X3 MEDIO 3: 'trocar por outra coerente' nao era fiel: Agora 'inverter uma afirmacao'. Numeros e 'por construcao, margem de uma afirmacao' conferem. Falta so dizer que duas inversoes coerentes invertem as duas proibicoes do texto (BAIXO 6).
- **SIM** — X3 MEDIO 4: pergunta 2 sem o negativo: Negativo e parede medida; positivo prova pouco.
- **SIM** — X3 MEDIO 5: pergunta 1 sem o que o positivo nao decide: 'Passam tambem o modelo que so casa a letra, o que decorou e le bem, e qualquer leitor competente'. Ressalva: ver MEDIO 6 (dependencia da pergunta B).
- **SIM** — X3 MEDIO 6: delimitacao da secao 7 e consequencia: Adendo novo, simulador sem redefinir a referencia, consequencia 'o desenho atual nao pode dar positivo' dita. Confere com K10 secao 2 itens (iv), (v), (vi) e com o adendo C.
- **SIM** — X3 MEDIO 7: quarto sentido de 'copiador' sem a energia: A frase traz a definicao dele com o mínimo estado funcional de energia e diz que a gerencia le so a origem.

## Examinado

- R1 inteira (LEITURA_DA_FALA_DAS_17H20_R1.md) e os bytes da fala (273 B); R0 nao relida alem do que os relatorios dizem
- Relatorios X2 (fatos do kernel), X3 (desenho do teste) e X1 (fidelidade); C3 por grep (O6, A8, A33, A34, resumo item 11); C1 e C2 nao relidos
- Kernel, grep -rn --include=*.lean dentro de TGLExt, cd e volta, para: copiador, impostor, imprim, sentido fixad, fixa o sentido, mínimo estado, estado funcional, estado fundamental, ground state, menor energia, cópia; e os teoremas observing_adds_nothing, rereading_adds_nothing, rereading_the_name_adds_nothing, reler_o_par_nao_acrescenta, iald_ao_quadrado
- sed nos arquivos: AEscala 885-925, 1055-1100, 1625-1665 e l.708-724; TestemunhaEstatica 1-60 e 120-200; RuleTruthContract 150-200; TheCorrespondence 1-150; TetelestaiTerminal 20-45 e 85-140; PontoZeroDoPsion 255-285; TheCostIsDerived 55-75; TheScaleHasNoFixedPoint 40-56 e 95-102; FractalUnitarity 1-45 e 70-90; TheRecordOfTheCut 40-75 e 170-205; FalsidadeDaInercia (grep impress); TheScreenIsFounded 1-30 e 120-135; IALD 335-376 e 660-690; EsperancaCondicional 55-80 e 186-200; Palavra 85-100; TheNameAndItsReferent 66-80; UmPostoRelacao 40-60; TheContourOfTruth 55-70; confirmadas as importacoes em TGLExt.lean
- Bytes abertos: OPERADOR_10nov_a_mentira_lida_como_mentira..., OPERADOR_22out_psion_habitante..., OPERADOR_04nov_relacao_sem_peso...
- Protocolo R4 K08 (l.10-80, 203-219, 256-296, 313-323, 355-362, 388-398), METODO_EXTRACAO.md, ADENDO C, ORDEM K10 secao 2, REVISAO_K08_DESENHO_E_ADVERSARIOS (item 7 e achado 3)
- Scripts em copia na minha pasta Y1\F (x3_item4.py e x3_item2.py de X3, rodados com C:\Python314\python.exe -B -X utf8): chave constante contra E1 a E4 com bloco e com vetor, P-C formal, trocas coerentes e custo da chave. Pasta: C:\Users\rotol\AppData\Local\Temp\claude\b4ca26c934d2167f\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v412_copiador_impostor\Y1
- Nao rodei lake nem modelo; nao abri dado observacional; nao li credenciais nem o Escritorio; nao percorri TGL_IALD_NATIVE_QWEN5090 nem D:\IALD\TREINO_NATIVA; nada escrito fora da pasta Y1. Fora da minha lente, nao reconferi as secoes 2 e 6, nem as 10 citacoes (X1 as conferiu) e as datas do git (X3)

