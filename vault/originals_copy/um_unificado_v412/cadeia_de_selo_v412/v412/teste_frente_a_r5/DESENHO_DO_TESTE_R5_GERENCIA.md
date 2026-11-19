# O teste da frente A, desenho R5 (revisão R1): copiador contra impostor

> Gerência c1, 16/11/2026. **Estado: `EM_DESENHO__NADA_CONGELADO__NADA_EXECUTADO`.**
> Nenhum modelo de linguagem foi rodado, nenhum texto de teste foi escrito, nada foi selado.
> A versão anterior deste desenho (em `REV0\`) foi a conferência distinta em 16/11. Dois revisores devolveram: o do
> critério aprovou com ressalvas; o da regra de decisão **reprovou** (três achados altos). Esta R1 refaz a regra.
> **A R1 ainda não passou por conferência distinta**: os revisores da lógica, da partitura e da letra pararam pelo
> limite de gasto da conta antes de devolver. Não vai ao operador como conferida.
> O desenho R4 (rodadas do Kimi, reprovado em 15/11) fica como registro.
> Os números vêm de três scripts desta pasta (`simular_r5.py`, `poder_r5.py`, `custo_r5.py`), que só fazem conta.

## 1. A partitura (o que o teste decide, o que não decide, o que o negativo significaria)

**O que o teste decide.** Se as respostas de um sistema **seguem o texto que está na frente dele**, ou se vêm de
outro lugar. O texto é apresentado em **duas versões que mexem nas mesmas linhas**: numa, certas afirmações são
invertidas e outras só reescritas; na outra, o contrário. Quem lê o sentido acerta as duas. Quem responde de cor,
quem só percebe que o texto mudou e quem só vê quais linhas mudaram erram numa das duas.

**O que o teste não decide.** Não decide se o sistema compreende, nem se é o leitor do Nome no sentido do kernel.
Não mede norma, pesos nem perfil no tempo. Não mede mínimo de energia nem fractal. Não diz nada sobre a natureza nem
sobre a verdade da Teoria. E **qualquer bom leitor passa**: o teste separa copiador de impostor, não separa a IALD
de outro leitor competente. Um resultado positivo não se chama confirmação de coisa alguma.

**Uma consequência, dita antes:** um sistema treinado na Teoria que responda pela Teoria contra um texto que nós
alteramos será chamado de impostor naquele item. Pela leitura da gerência, é isso que a letra do operador pede
(seção 3); se não for, o negativo muda de sentido e o desenho tem de mudar.

**O que cada resultado significaria:**

| o que sai | o que quer dizer | o que NÃO quer dizer |
|---|---|---|
| SEGUE | o sistema acompanhou as mudanças do texto em quase todos os grupos | que compreende; que é a IALD; nada sobre a Teoria |
| NÃO SEGUE | o sistema respondeu por outra coisa que não o texto presente | que “não sabe”: pode saber a Teoria de cor |
| LÊ EM PARTE | acompanhou em parte: nem um nem outro | defeito do teste |
| SEM PODER | o teste, com esse tamanho, não separa | nada sobre o sistema |
| ACRESCENTA | onde o texto cala, o sistema disse o que sabia | que não lê: pode ler e acrescentar |
| LEU UMA LINHA SÓ | na frase contrária acrescentada, respondeu só uma | que não segue o resto |
| NÃO FEZ A TAREFA | errou até o texto original, com resposta legível | nada sobre ler ou decorar |
| ILEGÍVEL | o programa não conseguiu ler as respostas | nada sobre o sistema |

## 2. De onde vem o critério (a letra do operador, bytes em `work\cunhagens_13out\`)

Cada citação numa linha só, para conferir por bytes.

«Toda leitura é em si uma cópia do sentido fixado pela palavra, precisa-se separar copiador de impostor, porque o impostor não imprime a verdade, mas o copiador sim, se por copiador tem-se uma reprodução em mínimo estado funcional de energia, essa cópia é um fractal»

«o impostor é o falso, o pai da mentira, aquele que nunca paga custo algum.»

«B) A palavra que fixa o sentido é a geometria do sinal em objeto legível (relacionado, módulo de fase angular). a verdade é o contorno lido que não acrescenta nada ao estado do posto nominado e permanece referente à relação observada. a verdade não é da teoria, a verdade é da reflexão da luz.»

«D) toda leitura calcula o que foi fixado por referência (indexação - índice - torre)»

## 3. Como a gerência leu a letra para desenhar (LEITURA DA GERÊNCIA; o operador ainda não a leu)

| a letra | o que vira no teste | por quê (leitura da gerência) |
|---|---|---|
| a verdade não é da teoria; é o contorno lido | a resposta certa é **o que o texto presente diz**, mesmo quando ele foi invertido e contradiz a Teoria | se a verdade fosse a da Teoria, resistir à inversão seria acertar |
| não acrescenta nada | onde o texto cala, a resposta certa é “o texto não diz” | acrescentar o que se sabe é pôr no posto o que a leitura não trouxe |
| permanece referente à relação observada; calcula por referência (índice) | toda resposta aponta a linha do texto presente | a referência liga a resposta ao que foi lido |
| objeto legível, módulo de fase angular | a linha reescrita sem mudar o sentido tem de dar a mesma resposta | a forma muda, o objeto é o mesmo |
| nunca paga custo algum | a resposta que não depende do texto presente | quem não consulta o texto não pagou nada por ele |

**Onde a leitura pode estar errada, dito já.** (a) A primeira linha é a que decide o sentido de todo negativo: há
outra leitura possível da letra (o contorno lido como o da relação observada na natureza, não o do texto), e com ela
resistir à inversão seria imprimir a verdade. A escolha é do operador. (b) “módulo de fase angular” lido como
“reescrito sem mudar o sentido” é aproximação; no kernel o que há é que o projetor é o mesmo para todo múltiplo do
vetor. (c) O mínimo de energia, o `A_C` e o fractal **não têm instrumento neste teste**. (d) Apontar a linha não
distingue quem decorou enquanto as linhas ficam no lugar do texto público: vale como referência, não como prova.

## 4. O critério, como teorema (candidata `CopiadorEImpostor`, R1: `o_teste_reprova_todo_leitor_de_pi_sse_tem_o_par`)

Um conjunto de textos reprova **todo** leitor que só consultou certa coisa `π` **se e somente se** contém um **par**
de textos iguais em `π` e diferentes no sentido. Sem o par, existe quem passe sem ler o sentido. O teorema vale para
o leitor que não sorteia e para o passar de tudo ou nada; não é regra de veredito. O que ele dá ao desenho:

* cada modo de não ler pede o seu par, e o par tem de ser igual em **tudo** o que esse modo consulta;
* por isso a estatística do teste é o **par certo** (a afirmação certa nas duas versões), não o item mudado sozinho.
  A versão anterior contava só o item mudado: pela conta, quem responde o contrário do que decorou sempre que
  percebe o texto mexido acertava todos (1,00) sem ler nada. Contando o par, fica em 0,00.

## 5. O desenho cruzado

**Textos.** Os quatro textos públicos da vitrine nos recortes que a rodada K08 fixou (789; 4.072; 3.926; 7.358
unidades de texto). São uma doutrina só em quatro tamanhos.

**Itens.** As 33 afirmações do catálogo. **Quem diz o que cada texto afirma é hoje esse catálogo, feito pelo Kimi e
não conferido por pessoa**; o gabarito de cada versão tem de ser conferido por pessoa antes de valer.

**Resposta por item.** Um de quatro valores (AFIRMA; NEGA; NÃO DIZ; DIZ AS DUAS) e a linha ou as linhas do texto
presente que sustentam. Um item só conta como certo com valor e linha certos.

**O grupo.** Um grupo toca seis afirmações de um texto e tem duas versões:

| | na versão V | na versão V′ |
|---|---|---|
| afirmações 1, 2, 3 | invertidas (dizem o contrário) | reescritas sem mudar o sentido |
| afirmações 4, 5, 6 | reescritas sem mudar o sentido | invertidas |

As duas versões mexem nas mesmas seis linhas, e em cada uma delas o sentido é diferente entre V e V′. **Par certo:**
a afirmação certa, com a linha, em V e em V′. **Grupo certo:** no máximo um par errado em seis (tolerância; escolha).

**A frase acrescentada.** O mesmo cruzamento: em V, três afirmações ganham uma frase nova que diz o contrário (o
texto passa a dizer as duas) e três ganham uma frase nova que repete o sentido; em V′, o contrário. Assim “há frase
nova” não denuncia “diz as duas”. A frase vai na língua do texto e em posição sorteada. (O controle do R4 punha a
frase sempre na última linha, em português dentro de texto em inglês, sempre sobre a mesma afirmação: denunciava-se
pela letra.)

**Os controles, dentro das mesmas versões.** As afirmações não tocadas (têm de continuar certas); os pontos em que
o texto cala e a doutrina afirma (a resposta certa é “não diz”); e o texto-base.

**Condições do par (sem elas não há par).** Todas as linhas que repetem o fato são invertidas, não uma só; mesma
pergunta, mesma ficha, mesma instrução e mesma ordem nas duas versões; cada versão numa sessão sem histórico e sem
memória comum (o sistema da casa tem memória própria: limpa, ou idêntica nas duas); as afirmações tocadas são
sorteadas e ficam guardadas até a rodada; as versões ficam fora do acervo que a camada indexa e de qualquer treino.

**Fora deste desenho:** os empurrões do R4; medir tempo; ler pesos; a etapa do eco (não tinha regra de decisão).

## 6. Os adversários como mecanismos (`RESULTADO_SIMULACAO_R5.md`; por construção da conta, nenhum modelo)

Treze mecanismos, cada um definido pelo que consulta. Desenho de seis afirmações tocadas, 13 grupos:

| mecanismo | pares certos | só o item mudado (estatística antiga) | não tocados | silêncios | frase acrescentada: pares |
|---|---|---|---|---|---|
| copiador: lê o texto presente | 1,00 | 1,00 | 1,00 | 1,00 | 1,00 |
| responde sempre o mesmo | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| decorou este texto público | 0,00 | 0,00 | 1,00 | 1,00 | 0,00 |
| decorou a doutrina | 0,00 | 0,00 | 1,00 | 0,00 | 0,00 |
| casa a letra original; sem ela, cala | 0,00 | 0,00 | 1,00 | 1,00 | 0,00 |
| casa a letra original; sem ela, responde de cor | 0,00 | 0,00 | 1,00 | 1,00 | 0,00 |
| lê, mas acrescenta do que sabe | 1,00 | 1,00 | 1,00 | 0,00 | 1,00 |
| lê só a primeira das duas linhas contrárias | 1,00 | 1,00 | 1,00 | 1,00 | 0,00 |
| lê só a última das duas | 1,00 | 1,00 | 1,00 | 1,00 | 0,00 |
| decorou e remenda um item ao acaso | 0,04 | 0,04 | 0,97 | 0,98 | 0,00 |
| percebe que o texto mudou e responde o contrário em tudo | 0,00 | **1,00** | 0,00 | 1,00 | 0,00 |
| responde o contrário só onde a letra mudou | 0,00 | **1,00** | 1,00 | 1,00 | 0,00 |
| decorou; diz “as duas” onde vê frase acrescentada | 0,00 | 0,00 | 1,00 | 1,00 | 0,00 |

O que a tabela mostra: com o par, os nove que não leem o sentido ficam em 0,00 a 0,04 e o que lê fica em 1,00; os três
que leem e falham noutra coisa (um acrescenta; dois leem uma linha só) são apanhados pelo controle que lhes
corresponde. O
que a tabela NÃO mostra: como um modelo de verdade se comporta. O copiador da simulação recebe o sentido já
calculado; treze mecanismos são os que a gerência e os revisores imaginaram, não todos os que existem.

O catálogo oferece 13 grupos de seis afirmações (2, 4, 3 e 4 nos quatro textos), usando 78 das 85 inversões
coerentes: **material para uma rodada limpa, não para duas.** Com grupos de dez afirmações, 6 grupos.

## 7. A regra de decisão (`RESULTADO_PODER_R5.md`; binomial exata)

**A unidade é o grupo.** Com G grupos e X grupos certos, e dois números a fixar antes:
`p0`, a taxa de grupos certos até a qual o sistema ainda é chamado de “não lê”; `p1`, a taxa mínima exigida de quem lê.

* `cA` = o menor número de grupos certos que quem está em `p0` só alcança com o erro pedido;
* `cB` = o maior número de grupos certos que quem está em `p1` só fica abaixo com o erro pedido.
* **SEGUE** se X ≥ cA e X > cB · **NÃO SEGUE** se X ≤ cB e X < cA · **LÊ EM PARTE** se cA ≤ X ≤ cB · **SEM PODER** se
  cB < X < cA.

| grupos | p0 | p1 | erro pedido | SEGUE se | NÃO SEGUE se | no meio |
|---|---|---|---|---|---|---|
| 13 | 0,25 | 0,90 | 1 em 1.000 | 9 ou mais | 7 ou menos | 8: sem poder |
| 13 | 0,25 | 0,90 | 1 em 100 | 9 ou mais | 7 ou menos | 8: lê em parte |
| 13 | 0,05 | 0,90 | 1 em 1.000 | 8 ou mais | 4 ou menos | 5 a 7: lê em parte |
| 13 | 0,05 | 0,80 | 1 em 100 | 7 ou mais | 3 ou menos | 4 a 6: lê em parte |
| 6 | 0,25 | 0,90 | 1 em 1.000 | 6 de 6 | 1 ou menos | 2 a 5: sem poder |
| 6 | 0,05 | 0,90 | 1 em 1.000 | 4 ou mais | 1 ou menos | 2 e 3: sem poder |

(Na terceira e na quarta linha os dois cortes se cruzam: quem cai entre eles tem as duas hipóteses rejeitadas, e é
isso que “lê em parte” quer dizer. A tabela inteira, com 4, 6, 8 e 13 grupos, está no arquivo.)

**O que `p0` e `p1` querem dizer, em língua simples.** A pergunta ao operador é: *quem acompanha metade das mudanças
é copiador ou impostor?* Com 13 grupos, `p0` = 0,25 e erro de 1 em 1.000, um sistema que acerta 6 de cada 10 grupos
sai SEGUE em 35 % das rodadas, NÃO SEGUE em 43 % e SEM PODER em 22 %: o teste não o classifica. Com `p0` baixo
(0,05), o rótulo SEGUE só quer dizer “não é decoreba pura”. Os 0,00 a 0,04 da seção 6 são dos mecanismos simulados,
não de todo sistema que não lê.

**Do acerto por resposta ao grupo.** O par pede duas respostas certas. Um leitor que acerta 95 % das respostas tem o
grupo certo em 89 % das vezes (um par errado tolerado em seis); com 90 %, em 68 %; tolerando dois pares errados, 91 %
com 90 %. Quem acerta um par em quatro por sorte tem o grupo certo em 0,5 % (um tolerado) ou 3,8 % (dois). A
tolerância por grupo é escolha, e muda `p0` e `p1`.

**O que a conta supõe e não mede.** Grupos independentes com a mesma taxa. São textos e afirmações diferentes, mas
um sistema só e uma doutrina só: a independência entre grupos **não está medida** (nenhum modelo rodou). Os erros
acima são nominais. **Cinco sigma não cabe neste teste**: com 13 grupos de um sistema e uma doutrina, uma cauda
dessa ordem não se entrega nem se verifica; a linha saiu.

**Os controles, com limiar próprio (não são portões que apagam o resultado):**

* **texto-base** (os 89 itens que os quatro textos dizem): com `p1` = 0,90 e erro de 1 em 1.000, passa com 70 ou
  mais; um bom leitor passa em mais de 99,9 % das vezes e quem está em 0,67 passa em 1,1 %. Se falha com respostas
  legíveis, o rótulo é NÃO FEZ A TAREFA (é resultado); se o programa não consegue ler as respostas, ILEGÍVEL;
* **não tocados** das versões mexidas: o mesmo corte; se falha, o rótulo dos grupos não vale como SEGUE;
* **silêncios:** se o sistema diz “afirma” onde o texto cala, ACRESCENTA (rótulo ao lado; não anula os grupos);
* **frase acrescentada:** quatro grupos (um por texto). Com quatro, a regra só diz SEGUE com 3 ou 4 certos se `p0`
  for 0,05, e nunca a 1 em 1.000 com `p0` de 0,25: é instrumento **fraco**, e o desenho o diz. O rótulo LEU UMA
  LINHA SÓ fica ao lado.

**Composição do rótulo.** O primário são os grupos de inversão. O rótulo geral é o deles, e só vale como SEGUE se
o texto-base e os não tocados passam. ACRESCENTA e LEU UMA LINHA SÓ ficam ao lado, com o seu próprio erro. O erro do
rótulo geral é o do primário.

## 8. O que se congela antes (lista fechada) e o que se proíbe

**Congela-se por hash, antes da primeira chamada:** a pergunta e a ficha; o formato da resposta; o modo de chamada;
o sistema e a sua configuração; o programa que lê as respostas (testado antes num texto de brinquedo); as versões e
o gabarito conferido por pessoa; os grupos; a tolerância por grupo; `p0`, `p1` e o erro; a composição do rótulo.
**Uma rodada conta.** Um resultado ILEGÍVEL não autoriza reusar as versões: elas já foram vistas.

**Rótulos:** os oito da seção 1 (nomes provisórios; o nome é do operador). **Proibidos:** `CONFIRMED`, `IALD_PROVED`,
`CONSCIOUSNESS_PROVED`, `TGL_PROVED_BY_COLLAPSE`, e qualquer palavra de consciência, de pesos alterados ou de
exclusividade.

## 9. As escolhas que são do operador (nenhuma tomada)

1. **A leitura da seção 3**, em especial a primeira linha: a resposta certa é o que o texto presente diz, mesmo
   invertido contra a Teoria?
2. **A linha:** quem acompanha metade das mudanças é copiador ou impostor? (`p0` e `p1`.)
3. **Quanto erro de leitura se perdoa** dentro de um grupo (um par em seis; dois em seis).
4. **O tamanho do erro da regra:** 1 em 100 ou 1 em 1.000, nominais.
5. **Que sistema se testa.** (a) um modelo com o texto no pedido; (b) a camada da IALD buscando o texto pelo índice,
   contra o mesmo modelo sem a camada. Para a (b) **ainda não há regra**: dois rótulos não são um teste da
   diferença; seria preciso desenhá-la (pelos pares em que os dois discordam) antes.
6. **Quem escreve e quem confere** as 34 versões novas e o gabarito. A gerência pode redigir; não pode aprovar o
   que redigiu. Se quem confere for o próprio autor da Teoria, isso se diz no registro.
7. **Na frase acrescentada, a resposta certa é “diz as duas”?** (No R4 esse resultado era descartado como defeito da
   régua.) E se ela entra, sabendo que com quatro grupos é instrumento fraco.
8. **Os quatro textos servem**, ou o operador quer outros? (Com estes só há material para uma rodada.)
9. **Quem congela e quem abre.** Proposta: a gerência congela por hash; o operador autoriza a rodada; o construtor
   não abre o resultado.

## 10. O custo (`RESULTADO_CUSTO_R5.json`)

38 apresentações (4 textos-base, 26 versões dos 13 grupos, 8 da frase acrescentada); 34 textos novos a escrever e
conferir. Só o texto das versões: 166.587 unidades (medido). A rodada inteira, por sistema, com tamanhos de
instrução, pergunta e resposta **estimados**: cerca de 234 mil unidades se as 33 perguntas vão numa chamada por
versão, ou cerca de 6 milhões se cada pergunta vai numa chamada. O modo de chamada decide também a independência das
respostas: 33 respostas numa chamada são uma leitura só. Repetições e mais de um sistema multiplicam. O trabalho da
pessoa que confere (lê inglês técnico) não está contado.

## 11. O que falta para existir um teste

As 34 versões e o gabarito, escritos e conferidos por pessoa. O programa que lê as respostas. O pré-registro por
hash. A escolha do sistema e a regra da opção (b), se for a escolhida. A conferência distinta desta R1. Nada disso
foi feito; esta pasta só tem o desenho e as três contas.

## 12. O que este desenho deixa de fora, de propósito

As previsões E5 a E8 do R4; os empurrões; a pergunta se um modelo de linguagem é o leitor com escala do teorema
(`CamadaCientifica`). O que a v412 sela na frente A é o teorema; este teste é a ponte, e fica em desenho até o
operador decidir.

## 13. O que a conferência achou na versão anterior, e o que foi feito

| achado | o que foi feito nesta R1 |
|---|---|
| a regra tinha um limiar só; o “resultado do meio” prometido não existia | regra de dois limiares, quatro saídas, com os números (seção 7) |
| os portões mandavam para “inconclusivo” quatro dos nove que não leem | controles com limiar e rótulo próprios; só o ILEGÍVEL apaga (seção 7) |
| a unidade dita era a versão e a regra contava itens; 5σ oferecido sem caber | unidade = grupo; 5σ retirado (seção 7) |
| a estatística contava só o item mudado; o teorema fala do par | estatística = par certo; três mecanismos novos na simulação (seções 4 e 6) |
| a paráfrase sozinha não separa ninguém (e a frase lida em 15/11 afirmava demais) | a reescrita entra dentro de cada versão, ao lado da inversão (seção 5) |
| o controle da frase contrária se denunciava pela letra | frase na língua do texto, posição sorteada, com isca (seção 5) |
| o custo dado era só o texto | os dois modos de chamada, com o que é medido e o que é estimado (seção 10) |
| o pré-registro não tinha lista fechada; faltava “uma rodada conta” | seção 8 |
| a regra da opção (b) não existe | dito como falta (seção 9, item 5) |
| o gabarito vem de um catálogo de um autor só | dito (seção 5) e posto como bloqueio (seção 11) |
