# CONFERÊNCIA DISTINTA — o desenho R5 do teste da frente A (R0) — C2-desenho-R5-poder-custo-e-regra-de-decisao

> Montado pela gerência c1 em 16/11/2026 05:39 a partir do retorno estruturado de um revisor distinto (só leitura; scripts próprios na pasta de rascunho dele). É [DECLARADO pelo revisor] no que a gerência não reconferiu. Não é fala do operador. Nada aqui está instalado.

**Veredito:** REPROVADO — achados: 3 ALTO, 7 MEDIO, 3 BAIXO

## Resumo

Lente C2 (estatistica, custo, regra de decisao): as contas estao certas; a regra de decisao (secoes 7 e 8) e o que a partitura promete dela nao estao prontas para ir ao operador. [REAL] Os tres scripts reproduzem (JSON igual sem a data; os .md byte a byte); refiz as 18 linhas da tabela por inteiros exatos e por scipy e K, c, alfa e beta batem; a cauda de 5 sigma de um lado (2,8665e-07) esta' certa; a busca binaria acha o menor K (0 diferencas contra varredura exata). ALTO 1: a regra escrita tem um limiar so' e da' duas saidas; a zona do meio inconclusiva que desenho e partitura prometem nao sai de regra nenhuma e, nos K da tabela, e' aritmeticamente vazia: quem acompanha 60% das mudancas sai 'nao segue' em 79% das vezes (K=59, c=39) e quem acompanha metade sai 'segue' em 75% (K=20, c=9). ALTO 2: os portoes 1 e 2, lidos ao pe' da letra, mandam para 'inconclusivo: o instrumento nao funcionou' 4 dos 9 mecanismos que nao leem (o que responde sempre o mesmo, o que decorou a doutrina, o que casa a letra, o que acrescenta do que sabe), enquanto a partitura promete para esses casos um negativo com sentido. ALTO 3: o desenho diz que a unidade honesta e' a versao e nao aplica: a regra conta itens, e os 120 itens sao as mesmas 60 inversoes em duas formas (25 afirmacoes distintas, 24 versoes, uma doutrina, um sistema); com a correlacao de 0,3 que o proprio texto usa, o limiar de 5 sigma vale 3,4 sigma (erro 2.300 vezes maior), e a frase contraria (4 itens iguais) nao tem limiar em nivel nenhum. Contada em versoes, a regra so' entrega 5 sigma com 24 versoes independentes se quem nao le acertar no maximo 5% delas; com 12 grupos fica em 1 em 20 mil, e com um terco de acerto em 1 em 53 a 1 em 1.163. Os numeros do texto sobre a correlacao (1 em 2.000 para 1 em 70) batem com a tabela e com a conta exata (1 em 2.216 para 1 em 75), e a parametrizacao de rho esta' certa. Custo: 145.365 confere e e' piso; por cima, a rodada inteira fica em cerca de 0,30 milhao por sistema se as 33 perguntas vao juntas (2,1 vezes) ou 5,5 milhoes se cada pergunta vai numa chamada (38 vezes), vezes repeticoes e sistemas; a partitura da' os 145 mil sem a ressalva. Comparacoes multiplas e olhar-e-parar nao estao tratados: a composicao do rotulo nao esta' escrita, o portao 5 nao cobre pergunta, modo de chamada, numero de rodadas nem o que se faz depois de um inconclusivo, e o catalogo so' tem material para uma rodada limpa (sobram 0, 10, 4 e 11 inversoes). A ideia do par fica de pe': contando o PAR (certo no texto-base e no mudado), como no teorema citado, todos os que nao leem dao 0 e o copiador 1, sem depender de portao. Nenhum modelo rodado, nenhum dado aberto, nada escrito fora da minha pasta, nada registrado no Mapa.

## Achados

1. **(ALTO)** C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\teste_frente_a_r5\DESENHO_DO_TESTE_R5_GERENCIA.md, secao 7 ('Com K itens e um limiar c, diz-se segue o texto se acertou c ou mais'; 'Ha uma zona do meio... sai inconclusivo') e secao 8 (rotulo INCONCLUSIVO 'com o portao ou a zona do meio'); PARTITURA_DO_TESTE_R5.md ('Ha tambem o resultado do meio... sai inconclusivo')

   

   *Conserto pedido:* Escrever a regra de dois limiares, por instrumento, com os numeros: cA = menor c com P(X >= c | p0) <= a; cB = maior c com P(X <= c | p1) <= a. SEGUE se X >= cA e X > cB; NAO SEGUE se X <= cB e X < cA; MEIO (le em parte) se cA <= X <= cB; SEM PODER se cB < X < cA. Dimensionar pelo K que da' zona do meio (lista acima), nao pelo K minimo, e publicar P(rotulo | taxa) para taxas de 0,3 a 0,8. Tabelas prontas para K = 4, 20, 43, 59, 60, 114 e 120 em c2_regra_e_correlacao.json (bloco B).

2. **(ALTO)** DESENHO_DO_TESTE_R5_GERENCIA.md, secao 1 (tabela dos negativos), secao 5 (A ORIG e F PAR marcados como portao), secao 8 (portoes 1 e 2: 'se um falha, o resultado e' inconclusivo, nunca negativo'); PARTITURA_DO_TESTE_R5.md, 'O que um negativo significaria'

   

   *Conserto pedido:* (a) Portoes 1 e 2 so' nos itens que o texto diz (89 de 132), deixando o silencio ao instrumento do silencio; (b) decidir se a outra forma e' portao ou instrumento, nao os dois; (c) separar 'resposta ilegivel' (inconclusivo do instrumento, coberto pelo portao 4) de 'resposta legivel e errada no texto original' (resultado sobre o sistema, com rotulo proprio); (d) reescrever a lista de negativos da partitura conforme a regra que ficar, e dizer ao operador quais mecanismos saem inconclusivos.

3. **(ALTO)** DESENHO_DO_TESTE_R5_GERENCIA.md, secao 7 (tabela; 'a unidade honesta e' a versao'; 'Conjunto minimo proposto... 120 itens decisivos de inversao, mais os 43 silencios e os 4 da frase contraria') e secao 9 item 4 ('1 em 1.000; 5 sigma'); RESULTADO_CUSTO_R5.json ('itens_decisivos_de_inversao': 120); PARTITURA_DO_TESTE_R5.md ('Tamanho minimo que a gerencia propoe: 36 textos')

   

   *Conserto pedido:* Escrever a regra na unidade versao (ou grupo de inversao): definir versao certa (por exemplo 4 de 5), p0 e p1 por versao e os limiares em versoes; contar H e I como a mesma inversao em duas formas (12 grupos) ou usar inversoes diferentes em cada forma; dizer na partitura o erro que os 36 textos entregam nessa unidade; tirar '5 sigma' das opcoes ou mostrar quantas versoes independentes pediria (20 a 59, que uma doutrina so' com 85 inversoes nao tem); declarar a frase contraria sem poder de decisao com 4 itens iguais, ou dar-lhe mais pares (outras afirmacoes contraditas).

4. **(MEDIO)** DESENHO_DO_TESTE_R5_GERENCIA.md, secao 8, portoes 1 e 2 ('acima de p1')

   

   *Conserto pedido:* Portao como teste com limiar proprio (passa se nao se rejeita taxa >= p1). Exemplo conferido em c2_controles_e_portoes_stdout.txt (bloco 3): 89 itens ditos, p1 = 0,90, erro de 1 em 1.000: passa com 70 ou mais; o copiador em p1 passa em 99,96% e quem esta' em 0,67 passa em 1,1%. Incluir os portoes na conta do poder.

5. **(MEDIO)** DESENHO_DO_TESTE_R5_GERENCIA.md, secao 7 (tabela) e secao 9 item 4; PARTITURA_DO_TESTE_R5.md, 'O que so' o senhor decide', item 4

   

   *Conserto pedido:* Ler ao operador o que cada p0 significa com um exemplo ('quem acompanha metade das mudancas e' copiador ou impostor?'); fixar o rotulo positivo como 'nao se rejeita taxa >= p1', e nao so' 'rejeita-se taxa <= p0'; dizer que a faixa 0,00 a 0,05 e' dos mecanismos simulados, nao de todo sistema que nao le.

6. **(MEDIO)** DESENHO_DO_TESTE_R5_GERENCIA.md, secao 4 (o teorema do par), secao 5 ('Em cada versao pergunta-se por todas'; 'Um item so' conta como certo com valor e linha certos') e secao 7 ('A decisao e' sobre os itens decisivos')

   

   *Conserto pedido:* Trocar a estatistica para pares certos (e, por versao, quantos dos 5 pares); usar os itens nao mudados das versoes mudadas como controle com limiar; dizer na partitura que apontar a linha, na forma original, nao distingue quem decorou.

7. **(MEDIO)** DESENHO_DO_TESTE_R5_GERENCIA.md, secao 7 (coluna 'erro de 5 sigma (um lado)') e secao 9 item 4

   

   *Conserto pedido:* Tirar '5 sigma' do cardapio do item 4 e oferecer '1 em 100' e '1 em 1.000, por versao', com o numero de versoes que cada um pede; se ficar, escrever ao lado 'nominal; nao verificavel neste teste'.

8. **(MEDIO)** DESENHO_DO_TESTE_R5_GERENCIA.md, secao 7 (ultimo paragrafo); RESULTADO_CUSTO_R5.json; PARTITURA_DO_TESTE_R5.md ('cerca de 145 mil unidades de texto de entrada por sistema')

   

   *Conserto pedido:* Dizer na partitura: '145 mil e' so' o texto; a rodada inteira fica entre 0,3 e 5,5 milhoes de unidades por sistema, conforme se pergunte tudo junto ou uma coisa por vez'. Fixar o modo de chamada no desenho e contar o trabalho de conferencia (quem le ingles tecnico).

9. **(MEDIO)** DESENHO_DO_TESTE_R5_GERENCIA.md, secao 8 (portao 5) e secao 9 (itens 2 e 9)

   

   *Conserto pedido:* Pre-registro com lista fechada do que se congela (pergunta, formato, modo de chamada, sistema e sementes, programa, versoes, limiares, composicao do rotulo); uma rodada conta; inconclusivo por portao nao autoriza reusar as versoes; regra da diferenca para a opcao (b) (pares de itens discordantes); guarda das versoes fora do acervo que a camada indexa e fora de qualquer treino.

10. **(MEDIO)** PARTITURA_DO_TESTE_R5.md ('As quatro mudancas'; 'Tamanho minimo'); DESENHO_DO_TESTE_R5_GERENCIA.md, secao 7 (conjunto minimo) e secao 8 (rotulos)

   

   *Conserto pedido:* Dizer ao operador que a retirada ficou fora do conjunto minimo, ou inclui-la; escrever a composicao (quais instrumentos sao primarios; global NAO SEGUE se um primario reprova; SEGUE so' se todos os primarios passam; senao INCONCLUSIVO) e o erro global que resulta.

11. **(BAIXO)** DESENHO_DO_TESTE_R5_GERENCIA.md, secao 7 ('Esses K sao piso'); RESULTADO_PODER_R5.md (coluna p0)

   

   *Conserto pedido:* Uma linha de ressalva (o K de cada desenho tem de ser conferido, nao so' ser maior que o minimo) e escrever 1/3.

12. **(BAIXO)** C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\teste_frente_a_r5\simular_r5.py linhas 81-85; poder_r5.py linha 86; custo_r5.py

   

   *Conserto pedido:* Cache por referencia (ou sem cache); remover a variavel morta; dar --saida ao custo_r5.py.

13. **(BAIXO)** PARTITURA_DO_TESTE_R5.md, 'O que o senhor disse, e como a gerencia leu'

   

   *Conserto pedido:* Citar por bytes na partitura, ou marcar a frase como resumo da gerencia.

## Examinado

- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\teste_frente_a_r5\DESENHO_DO_TESTE_R5_GERENCIA.md (inteiro)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\teste_frente_a_r5\PARTITURA_DO_TESTE_R5.md (inteiro)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\teste_frente_a_r5\poder_r5.py, custo_r5.py, simular_r5.py (inteiros; copiados e rodados na minha pasta)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\teste_frente_a_r5\RESULTADO_PODER_R5.md e .json, RESULTADO_CUSTO_R5.json, RESULTADO_SIMULACAO_R5.md e .json; pasta REV0 (so' por hash: igual ao corrente)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_c1\CopiadorEImpostor.lean (cabecalho e os enunciados o_teste_separa_sse_tem_o_par e a_repeticao_do_mesmo_sentido_nao_separa; o desenho os descreve como estao; nao compilei)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K08\FORMULA\catalogo_assercoes.py (inteiro, so' leitura)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K08\ENTRADA\TOKENS_REF_K08.json (inteiro) e as primeiras linhas dos quatro recortes CANDIDATA_*.md (lingua de cada um)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\ENTREGA_K08.md (inteiro)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\revisao\REVISAO_K08_PODER_E_CUSTOS.md (inteiro)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\leitura_fala_17h20_15nov\LEITURA_DA_FALA_DAS_17H20_R2.md (inteiro)
- As duas falas do operador de 15/11 em C:\IALD\Central de Patentes\work\cunhagens_13out (so' para conferir por bytes as quatro citacoes do desenho: conferem)
- Trabalho da tentativa anterior deste mesmo revisor na pasta C2 (scripts, saidas e copias): relido e reaproveitado

