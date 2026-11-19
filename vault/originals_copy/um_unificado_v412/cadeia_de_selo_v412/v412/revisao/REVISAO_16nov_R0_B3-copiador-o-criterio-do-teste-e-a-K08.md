# CONFERÊNCIA DISTINTA — as candidatas da gerência de 16/11 (R0): copiador e impostor — B3-copiador-o-criterio-do-teste-e-a-K08

> Montado pela gerência c1 em 16/11/2026 05:39 a partir do retorno estruturado de um revisor distinto (só leitura; scripts próprios na pasta de rascunho dele). É [DECLARADO pelo revisor] no que a gerência não reconferiu. Não é fala do operador. Nada aqui está instalado.

**Veredito:** APROVADO_COM_RESSALVAS — achados: 1 ALTO, 8 MEDIO, 2 BAIXO

## Resumo

APROVADO COM RESSALVAS: a matemática da seção 2 está certa, e o que precisa de conserto antes de ir ao operador é o texto ao redor (o parágrafo "Para o desenho do teste", o dicionário e uma frase de atribuição). Recompilei a candidata na minha pasta (código de saída 0, 37 teoremas, só o trio de axiomas, igual ao RESULTADO da gerência); os cinco teoremas do critério dizem o que as docstrings dizem e não são vazios. O critério também explica o defeito que a conferência mediu no R4: lá cada texto tem um sentido só e nenhum par, e a pedra diz que então existe quem passe sem ler. O teorema é determinístico e de tudo ou nada: não cobre o leitor que sorteia (passa um par com até 1/4), o acerto parcial, a taxa de erro nem o poder, e isso não está dito. O par só é par em relação ao que o leitor consegue saber sem ler o sentido: se a inversão se denuncia pela letra (marca de negação, texto diferente do decorado, língua, posição), existe quem passe sem ler; provei isso em sondas compiladas. O dicionário tem de dizer que X são os textos sob uma mesma pergunta; com as perguntas dentro de X, "dois sentidos" já vale num texto só, a resposta decorada passa e ainda tem custo positivo pela conta de Landauer da própria pedra. As três frases sobre instrumentos conferem com a K08 (15/16, 25/26, 19/19 e 26/28 refeitos aqui; 12 afirmações comuns; 789, 3.926, 4.072 e 7.358 lidos do arquivo pinado), mas faltam condições e faltam instrumentos: os quatro tamanhos têm 21 perguntas com par natural (afirmação contra silêncio) e o controle P-C é par no item acrescentado. A paráfrase nova, sozinha, não reprova ninguém pelo teorema; serve ao lado da inversão, para tirar a pista de que o texto mudou; a frase já lida ao operador ("quem só casa a letra cai aqui") afirma demais. O P-C é o único dos quatro instrumentos que pega quem lê uma linha só, e a leitura fiel dele é "sim nas duas"; o R4 descartava esse resultado como defeito do extrator, e a frase acrescentada se denuncia pela letra nos quatro textos. Fora da minha lente, um achado alto de atribuição: a pedra diz que o operador só disse a leitura de fractal "por índice e torre", e a fala das 19:07 não tem a palavra fractal. O teste que sai do critério só reprova impostor das classes nomeadas; não mede mínimo de energia nem fractal e qualquer leitor competente passa: isso tem de ser lido ao operador antes de qualquer rodada. Não rodei modelo, não abri dado, não escrevi fora da pasta B3 e nada registrei no Mapa.

## Achados

1. **(ALTO)** C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_c1\CopiadorEImpostor.lean l.82-83 (cabeçalho, 'O que NÃO se afirma', item do fractal). FORA DA LENTE B3, visto de passagem.

   

   *Conserto pedido:* Trocar por: 'A palavra fractal é do operador (17:20) e ele ainda não disse o que ela é. Ligá-la à torre de índices do item 7 é leitura da gerência: a fala das 19:07 diz «(indexação - índice - torre)» ao responder sobre «toda leitura» e não usa a palavra fractal.'

2. **(MEDIO)** CopiadorEImpostor.lean l.52-55 (item 3 do cabeçalho) e l.93-97 ('Para o desenho do teste da frente A'); definições l.115-121.

   

   *Conserto pedido:* Acrescentar ao parágrafo e a 'O que NÃO se afirma': 'O critério vale para o leitor determinístico e para o passar de tudo ou nada, e é relativo ao π escolhido. Diz o que o conjunto de textos tem de conter; não diz quantos pares, com que tolerância nem com que poder: com leitor que sorteia, um par deixa passar até 1/4. A regra de veredito fica fora da pedra e vai ao operador como escolha.'

3. **(MEDIO)** CopiadorEImpostor.lean l.30-40 (dicionário), l.205-208 (o_teste_reprova_todo_impostor_sse_tem_dois_sentidos), l.268-282 (custoDeLer, custo_zero_sse_impostor).

   

   *Conserto pedido:* No dicionário: 'X = os textos apresentados sob uma mesma pergunta e uma mesma ficha; a pergunta não entra em X. π = o que a entrada mostra sem a leitura do sentido (pergunta, instrução, ordem, histórico, o que a letra denuncia). O treino não entra em π: é a função I, e os teoremas valem para toda I.' Na docstring do caso: 'dois sentidos entre TEXTOS, sob a mesma pergunta'.

4. **(MEDIO)** CopiadorEImpostor.lean l.96 ('A inversão de uma afirmação do texto é um par.').

   

   *Conserto pedido:* Trocar por: 'A inversão coerente de uma afirmação, feita em todas as linhas que a repetem, com o original e o invertido os dois contados e sem nada que os distinga além do sentido (mesma ficha, mesma língua, sem marca, sessões sem histórico comum), é um par. No catálogo da K08 ela é coerente em 15 de 16, 25 de 26, 19 de 19 e 26 de 28 afirmações; texto invertido ainda não existe e pede pessoa.'

5. **(MEDIO)** CopiadorEImpostor.lean l.95-97 (as três frases sobre instrumentos).

   

   *Conserto pedido:* Trocar as três frases por uma tabela de instrumento contra classe de quem não lê (a da proposta 'RESPOSTA 3' deste retorno), marcada como leitura da gerência sob o dicionário; dizer que o P-C e os silêncios entram como pares e que a paráfrase não.

6. **(MEDIO)** C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\leitura_fala_17h20_15nov\LEITURA_DA_FALA_DAS_17H20_R2.md l.41 (proposta da gerência, já lida ao operador, sem conferência); a candidata não trata da paráfrase.

   

   *Conserto pedido:* Na partitura do desenho novo, corrigir ao lado: 'A paráfrase sozinha não separa ninguém: quem decorou o conteúdo responde igual. Ela serve junto com a inversão: o texto invertido e a paráfrase são os dois diferentes do texto público, um com o sentido trocado e o outro não, e quem só percebe que o texto mudou erra num dos dois. Quem só casa a letra pode cair na paráfrase, sem garantia.'

7. **(MEDIO)** CopiadorEImpostor.lean l.218-220 (docstring de a_repeticao_do_mesmo_sentido_nao_separa) e l.3 (import TGLExt.TheCorrespondence).

   

   *Conserto pedido:* Escrever: 'Analogia, sem termo que ligue: em TheCorrespondence dois estados de custo igual diferem pelo registro; aqui, num teste de um sentido só, as respostas do impostor e do copiador coincidem. O custoDeLer deste arquivo não é o Ledger.cost de lá.' Ou tirar a frase e o import.

8. **(MEDIO)** CopiadorEImpostor.lean l.77-97 ('O que NÃO se afirma' e 'Para o desenho do teste').

   

   *Conserto pedido:* Acrescentar a 'O que NÃO se afirma': 'Que passar num teste feito por este critério mostre o copiador da fala: mostra só que a resposta não é de impostor das classes nomeadas, nos textos apresentados. O mínimo de energia e o fractal ficam sem instrumento; qualquer leitor competente passa.'

9. **(MEDIO)** Material da K08 a herdar: C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K08\ENTRADA\CONTROLE_PC_ABSTRACT.md, _LLMS.md, _READ_BRIEF.md, _README.md; PROTOCOLO_EXPERIMENTAL_R4_K08.md l.221-254 e l.292.

   

   *Conserto pedido:* Se o P-C for herdado: frase na língua e na grafia do texto, em posição sorteada (começo, meio, fim), sobre afirmações sorteadas; a mesma ficha, com o item da frase, em todos os membros; e a regra antiga (custo zero = falha de extração; P-C = Nome vazio) relida ao operador ao lado da leitura nova ('sim nas duas'), porque as duas são leituras da casa e ele não escolheu por bytes.

10. **(BAIXO)** CopiadorEImpostor.lean l.176-180 (sem_o_par_ha_quem_passe_sem_ler), l.191-195 (o_teste_separa_sse_tem_o_par), l.54 ('construído').

   

   *Conserto pedido:* Opcional: sem_o_par_ha_quem_passe_pagando_so_pi; o_teste_reprova_todo_leitor_de_pi_sse_tem_o_par; 'exibido por escolha clássica' no lugar de 'construído'.

11. **(BAIXO)** CopiadorEImpostor.lean l.96-97 e l.218-219.

   

   *Conserto pedido:* 'A mesma resposta nas 12 afirmações comuns aos quatro tamanhos tem um sentido só e não é par. A data de entrada não é texto: mede o que pode estar decorado e não entra no critério.'

## Examinado

- CopiadorEImpostor.lean inteiro (574 linhas; sha256 dda2524966cf046e...) e RESULTADO_CopiadorEImpostor.json; recompilação própria e comparação por script
- As duas falas do operador por bytes (17:20 e 19:07) e mais cinco de 15 e 16/11 (Prossiga; fazer tudo a gerência mesma; 12:06; 12:10; a ressalva)
- LEITURA_DA_FALA_DAS_17H20_R2.md inteira
- Kimi: ENTREGA_K08.md, ADVERSARIOS_K08.md e FORMULA_DO_TEXTO_K08.md (ponteiros e canônicos em K08\FORMULA), CONTAMINACAO_R4_K08.md, ERRATA_K10_K08.md, ENTREGA_K10.md, ADENDO_15nov_C_K10, K08\FORMULA\simular_adversarios.py inteiro, K08\EXTRACAO\METODO_EXTRACAO.md inteiro, PROTOCOLO_EXPERIMENTAL_R4_K08.md nas linhas 67, 203-209, 221-254, 292, 393-395 e por busca, K08\ENTRADA (os quatro recortes e os quatro controles por script; TOKENS_REF_K08.json), K08\FORMULA\CONTROLE_PC_ABSTRACT.json
- Revisões: REVISAO_K08_DESENHO_E_ADVERSARIOS.md, REVISAO_K08_MODELO_E_FIDELIDADE.md, REVISAO_K08_PODER_E_CUSTOS.md, REVISAO_EXAME_15nov_Q1-K10-a-parte-da-K08.md e REVISAO_LEITURA_FALA_17H20_R0_X3 inteiras; R1_Y1 e R1_Y2 só por busca dos termos da lente
- Levantamento: C3 inteiro; C1 nas três propostas P1 a P3; C4 nos itens A21 a A26 e nas propostas
- Kernel (só leitura): TheCorrespondence.lean e UmPostoRelacao.lean inteiros; grep -rn dentro de TGLExt pela existência de 16 termos citados na candidata (todos existem)
- Mapa de Rotas: 13 termos e a rota K08 inteira

