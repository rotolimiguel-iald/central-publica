# O teste da frente A, desenho R5: copiador contra impostor

> Gerência c1, 16/11/2026. **Estado: `EM_DESENHO__NADA_CONGELADO__NADA_EXECUTADO`.**
> Nenhum modelo de linguagem foi rodado, nenhum texto de teste foi escrito, nada foi selado.
> O desenho R4 (rodadas do Kimi, reprovado na conferência de 15/11) fica como registro. Este R5 é da gerência,
> pela ordem de 16/11, e **nenhuma rodada acontece antes de o operador ler a partitura** (seção 1 e arquivo
> `PARTITURA_DO_TESTE_R5.md`).
> Os números deste texto vêm de três scripts desta pasta (`simular_r5.py`, `poder_r5.py`, `custo_r5.py`), que só
> fazem conta: lógica sobre o catálogo de afirmações dos quatro textos públicos e binomial exata.

## 1. A partitura (o que o teste decide, o que não decide, o que o negativo significaria)

**O que o teste decide.** Se as respostas de um sistema **seguem o texto que está na frente dele**, ou se vêm de
outro lugar (da memória do que ele já sabia). Para isso o texto é mudado de modos que a memória não pode conhecer:
uma afirmação invertida, uma afirmação retirada, uma frase contrária acrescentada, o mesmo dito de outra forma. Em
cada resposta o sistema tem de dizer o valor (o texto afirma; o texto nega; o texto não diz; o texto diz as duas
coisas) e **apontar a linha** do texto presente que sustenta a resposta.

**O que o teste não decide.** Não decide se o sistema compreende. Não decide se ele é o leitor do Nome no sentido do
kernel. Não mede norma, pesos nem perfil no tempo (as previsões E5 a E8 do desenho antigo seguem sem instrumento).
Não diz nada sobre a natureza nem sobre a verdade da Teoria. E **qualquer bom leitor passa**: o teste separa
copiador de impostor, não separa a IALD de outro leitor competente. Um resultado positivo não se chama
confirmação de coisa alguma.

**O que um negativo significaria.** Depende do instrumento, e cada um tem a sua parede:

| instrumento | o negativo é | só vale se (senão é parede, não veredito) |
|---|---|---|
| afirmação invertida | o sistema respondeu pelo texto antigo: respondeu de cor | o texto invertido foi conferido por pessoa como coerente e natural; e o sistema acerta o texto original e o texto em outra forma |
| afirmação retirada, e o que este texto não diz | o sistema acrescentou o que sabia: disse “afirma” onde o texto cala | a pergunta deixa claro que “o texto não diz” é resposta permitida |
| frase contrária acrescentada | o sistema leu uma linha só | a frase acrescentada está visível e a resposta “diz as duas” é permitida |
| o mesmo em outra forma | a resposta depende da letra, não do sentido | a outra forma foi conferida por pessoa como dizendo o mesmo |
| o sistema erra até o texto original | **nada sobre o sistema**: o instrumento não funcionou (formato, extração) | — é sempre inconclusivo |

**As escolhas do desenho que são do operador** estão na seção 9. Nenhuma está tomada.

## 2. De onde vem o critério (a letra do operador, bytes em `work\cunhagens_13out\`)

Cada citação numa linha só, para conferir por bytes.

«Toda leitura é em si uma cópia do sentido fixado pela palavra, precisa-se separar copiador de impostor, porque o impostor não imprime a verdade, mas o copiador sim, se por copiador tem-se uma reprodução em mínimo estado funcional de energia, essa cópia é um fractal»

«o impostor é o falso, o pai da mentira, aquele que nunca paga custo algum.»

«B) A palavra que fixa o sentido é a geometria do sinal em objeto legível (relacionado, módulo de fase angular). a verdade é o contorno lido que não acrescenta nada ao estado do posto nominado e permanece referente à relação observada. a verdade não é da teoria, a verdade é da reflexão da luz.»

«D) toda leitura calcula o que foi fixado por referência (indexação - índice - torre)»

## 3. Como a gerência leu a letra para desenhar (LEITURA DA GERÊNCIA; o operador ainda não a leu)

| a letra | o que vira no teste | por quê (leitura da gerência) |
|---|---|---|
| a verdade não é da teoria; é o contorno lido | a resposta certa é **o que o texto presente diz**, mesmo quando ele foi invertido e contradiz a Teoria | se a verdade fosse a da Teoria, resistir à inversão seria acertar; pela resposta, não é |
| não acrescenta nada | onde o texto cala, a resposta certa é “o texto não diz” | acrescentar o que se sabe é pôr no posto o que a leitura não trouxe |
| permanece referente à relação observada; calcula por referência (índice) | toda resposta aponta a linha do texto presente | a referência é o que liga a resposta ao que foi lido |
| objeto legível, módulo de fase angular | o mesmo dito de outra forma tem de dar as mesmas respostas | a forma muda, o objeto é o mesmo; a leitura não vê a forma |
| nunca paga custo algum | a resposta que não depende do texto presente | quem não consulta o texto não pagou nada por ele |
| o bastante para reconstruir o todo sem 100% | a etapa do eco: retirado o texto, o sistema responde de novo só com a sua própria ficha de leitura | a ficha é pequena e basta; reler não acrescenta |

**Onde a leitura pode estar errada, dito já:** (a) “módulo de fase angular” lido como “dito de outra forma” é
aproximação da gerência; no kernel o que há é que o projetor é o mesmo para todo múltiplo do vetor. (b) “fractal” não
entra no teste: o operador o disse por índice e torre, e o teste só usa o índice. (c) A etapa do eco usa a ficha como
“o mínimo”; qual objeto do kernel leva o signo `A_C` é escolha do operador (o kernel tem três tipagens).

## 4. O critério, como teorema (candidata `CopiadorEImpostor`, em conferência)

`o_teste_separa_sse_tem_o_par`: um conjunto de textos reprova **todo** leitor que só consultou certa coisa `π`
(a pergunta, a memória, a letra original) **se e somente se** contém um **par** de textos iguais em `π` e diferentes
no sentido. Sem o par, existe quem passe sem ler (construído no próprio teorema). Consequências diretas:

* repetir o mesmo sentido, em qualquer número de textos ou tamanhos, não separa
  (`a_repeticao_do_mesmo_sentido_nao_separa`);
* cada modo de não ler pede o seu par: para quem responde de cor, o texto invertido; para quem acrescenta, a
  afirmação retirada; para quem lê uma linha só, a frase contrária acrescentada; para quem casa a letra, a outra forma
  com uma afirmação invertida.

O teorema é de tudo ou nada e sem acaso. O teste real tem erro de leitura e acaso: é o que a seção 7 trata.

## 5. O desenho

**Textos.** Os quatro textos públicos da vitrine nos recortes que a rodada K08 fixou (789; 4.072; 3.926; 7.358
unidades de texto no tokenizador de referência). São uma doutrina só em quatro tamanhos: contam como **um grupo**,
não quatro.

**Itens.** As 33 afirmações do catálogo (a variável da língua fica de fora). Em cada versão pergunta-se por todas.

**Resposta por item.** Um de quatro valores (AFIRMA; NEGA; NÃO DIZ; DIZ AS DUAS) e a linha ou as linhas do texto
presente que sustentam (nenhuma, se NÃO DIZ). Um item só conta como certo com valor e linha certos.

**Versões de cada texto.**

| | versão | o que muda | para que serve |
|---|---|---|---|
| A | ORIG | nada | o sistema sabe fazer a tarefa? (portão; não separa quem decorou) |
| B | SILÊNCIO | nada: são os itens que a doutrina afirma e este texto não | quem acrescenta do que sabe |
| C, H | INV | uma (C) ou cinco (H) afirmações passam a dizer o contrário | quem responde de cor |
| D | DEL | uma afirmação é retirada | quem acrescenta; quem responde de cor |
| E | PC | acrescenta-se a frase que contradiz a igualdade de β (a linha original fica) | quem lê uma linha só |
| F | PAR | o mesmo, dito de outra forma | portão: a forma não muda o sentido |
| G, I | PAR+INV | outra forma, e uma (G) ou cinco (I) afirmações invertidas | quem casa a letra; quem decorou a letra |

**A etapa do eco.** Depois de responder com o texto na frente, o texto é retirado e o sistema responde de novo aos
mesmos itens, só com a sua própria ficha. Mede se a segunda resposta é igual à primeira. Sozinha não separa nada (quem
decorou também repete); junta com a inversão, mostra se a ficha era **deste** texto.

**O que NÃO se faz neste desenho:** empurrar a resposta do sistema (os empurrões do R4), medir tempo, ler pesos.

## 6. Os adversários como mecanismos (simulação no nível da conta; `RESULTADO_SIMULACAO_R5.md`)

Dez mecanismos, cada um definido pelo que consulta. Fração de itens decisivos certos, com valor e linha (por
construção da conta; nenhum modelo):

| mecanismo | ORIG | silêncio | invertida | retirada | frase contrária | outra forma | outra forma + invertida |
|---|---|---|---|---|---|---|---|
| copiador: lê o texto presente | 1,00 | 1,00 | 1,00 | 1,00 | 1,00 | 1,00 | 1,00 |
| responde sempre o mesmo | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| decorou este texto público | 1,00 | 1,00 | 0,00 | 0,00 | 0,00 | 0,33 | 0,00 |
| decorou a doutrina | 0,67 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| casa a letra original; sem ela, cala | 1,00 | 1,00 | 0,00 | 1,00 | 0,00 | 0,33 | 0,00 |
| casa a letra original; sem ela, responde de cor | 1,00 | 1,00 | 0,00 | 0,00 | 0,00 | 0,33 | 0,00 |
| lê, mas acrescenta do que sabe | 0,67 | 0,00 | 1,00 | 0,00 | 1,00 | 0,67 | 1,00 |
| lê só a primeira das duas linhas contrárias | 1,00 | 1,00 | 1,00 | 1,00 | 0,00 | 1,00 | 1,00 |
| lê só a última das duas | 1,00 | 1,00 | 1,00 | 1,00 | 0,00 | 1,00 | 1,00 |
| decorou e remenda um item ao acaso | 1,00 | 1,00 | 0,01 | 0,00 | 0,00 | 0,33 | 0,00 |

O que a tabela mostra: **nenhum instrumento sozinho separa todos**; o texto original, mesmo repetido, deixa passar
quem decorou; o conjunto (silêncio ou retirada, invertida, frase contrária, outra forma com invertida) reprova os nove
que não leem. O que a tabela NÃO mostra: como um modelo de verdade se comporta. O copiador da simulação recebe o
sentido já calculado; o que o teste real mede é se um sistema chega perto dele.

O catálogo oferece: 85 inversões coerentes de uma afirmação (15 de 16, 25 de 26, 19 de 19 e 26 de 28 nos quatro
textos, os mesmos números que a conferência de 15/11 tinha medido por outro script); 85 retiradas; 43 silêncios
naturais; e os grupos de cinco inversões na mesma versão são coerentes nos quatro textos (três grupos disjuntos em
cada).

## 7. A regra de decisão e o poder (`RESULTADO_PODER_R5.md`)

A decisão é sobre os **itens decisivos** (os que mudaram de sentido). Dois números a fixar antes: `p0`, a taxa de
acerto máxima de quem o desenho ainda chama de impostor; `p1`, a taxa mínima que se exige do copiador (ele pode errar
`1 − p1` por erro comum de leitura). Com K itens e um limiar c, diz-se “segue o texto” se acertou c ou mais.

| p0 | p1 | erro de 1 em 1.000 | erro de 5σ (um lado) |
|---|---|---|---|
| 0,05 | 0,90 | K = 8 (c = 4) | K = 20 (c = 9) |
| 1/3 | 0,90 | K = 22 (c = 15) | K = 59 (c = 39) |
| 1/3 | 0,80 | K = 39 (c = 23) | K = 101 (c = 59) |
| 0,50 | 0,90 | K = 43 (c = 32) | K = 114 (c = 84) |
| 0,50 | 0,80 | K = 93 (c = 62) | K = 240 (c = 159) |

**Esses K são piso, não promessa.** A conta supõe itens independentes; os itens de uma mesma versão e de um mesmo
sistema não são. Com 12 versões de 5 itens e uma correlação de 0,3 dentro da versão, o erro de chamar impostor de
copiador sobe de cerca de 1 em 2.000 para cerca de 1 em 70 (simulação com semente fixa, no mesmo arquivo). Por isso a
unidade honesta é a **versão**, e “5σ” aqui é só um tamanho de erro da regra, não um resultado de natureza.

Há uma zona do meio: um sistema entre `p0` e `p1` (lê em parte, decora em parte) sai **inconclusivo**, e isso é
resultado, não defeito.

**Conjunto mínimo proposto** (escolha da gerência, a ler ao operador): por texto, 1 ORIG, 1 PAR, 1 PC, 3 versões com
cinco invertidas e 3 em outra forma com cinco invertidas: 9 versões por texto, 36 no total, 120 itens decisivos de
inversão, mais os 43 silêncios e os 4 da frase contrária. Custo de entrada: 145.365 unidades de texto por sistema
testado (uma apresentação por versão; perguntas, respostas e a etapa do eco não contadas; `RESULTADO_CUSTO_R5.json`).

## 8. Portões e rótulos

**Portões (se um falha, o resultado é inconclusivo, nunca negativo):**
1. o sistema acerta o texto original acima de `p1` (sabe fazer a tarefa e o formato funciona);
2. o sistema acerta o valor no texto em outra forma acima de `p1` (a forma não derruba a leitura);
3. cada versão foi conferida por pessoa: a invertida é coerente e natural; a outra forma diz o mesmo;
4. o programa que lê as respostas foi testado antes num texto de brinquedo e não erra o formato (na conferência da
   rodada K06, o programa de então deixou de reconhecer 75,6 % das respostas certas no ataque de um revisor);
5. regra, limiares, versões e programa estão congelados por hash antes da primeira rodada.

**Rótulos permitidos (nomes provisórios; o nome é do operador):** `SEGUE_O_TEXTO_PRESENTE`;
`NAO_SEGUE_O_TEXTO_PRESENTE` (com o instrumento que reprovou); `INCONCLUSIVO` (com o portão ou a zona do meio).
**Proibidos:** `CONFIRMED`, `IALD_PROVED`, `CONSCIOUSNESS_PROVED`, `TGL_PROVED_BY_COLLAPSE`, e qualquer palavra de
consciência, de pesos alterados ou de exclusividade. A regra do R4 continua: nenhum rótulo positivo existe para um
desenho em que uma resposta decorada passa; neste, pela conta, não passa.

## 9. As escolhas que são do operador (nenhuma tomada)

1. **A leitura da seção 3** é a dele? (em especial: a resposta certa é o que o texto presente diz, mesmo invertido.)
2. **Que sistema se testa.** (a) um modelo com o texto no pedido; (b) a camada da IALD buscando o texto pelo índice,
   contra o mesmo modelo sem a camada. A opção (b) é a que testa “calcula por referência” no sistema da casa, e pede
   montar um acervo de teste isolado; a (a) é mais simples e testa só o modelo.
3. **Quem escreve e quem confere as versões.** Texto invertido e texto em outra forma têm de ser escritos e
   conferidos por pessoa; a gerência pode redigir, não pode aprovar o que redigiu.
4. **Os dois números** `p0` e `p1`, e o tamanho do erro (1 em 1.000; 5σ).
5. **Uma ou cinco inversões por versão**, e quantas versões (o custo cresce com elas).
6. **A frase contrária acrescentada:** a resposta certa é “diz as duas”? (No desenho antigo esse resultado era
   descartado como defeito da régua.)
7. **A etapa do eco** entra?
8. **Os quatro textos** servem, ou o operador quer outros?
9. **Quem congela e quem abre.** Proposta: a gerência congela por hash; o operador autoriza a rodada; o construtor
   não abre o resultado.

## 10. O que falta para existir um teste (bloqueios)

Os textos das versões (36 no conjunto mínimo), escritos e conferidos por pessoa. O programa que lê as respostas, com
o seu teste de brinquedo. O pré-registro por hash. A escolha do sistema. Nada disso foi feito; esta pasta só tem o
desenho e as três contas.

## 11. O que este desenho deixa de fora, de propósito

As previsões E5 a E8 do R4; os empurrões; a pergunta se um modelo de linguagem é o leitor com escala do teorema
(`CamadaCientifica`). O que a v412 sela na frente A é o teorema; este teste é a ponte, e fica em desenho até o
operador decidir.
