# O teste da frente A, desenho R6, revisão R1: o assento no índice e a página levada ao leitor

> Gerência c1, 16/11/2026. **Estado: `EM_DESENHO__NADA_CONGELADO__NADA_EXECUTADO`.**
> Nenhum modelo de linguagem foi rodado, nenhuma página de teste foi escrita, nada foi selado.
> A primeira versão (em `REV0\`) foi a conferência distinta em 16/11: seis revisores; três aprovaram com ressalvas e
> três reprovaram a versão para ser lida ao operador (relatórios em `..\revisao\REVISAO_16nov_R3_T1…` a `…T6…`).
> **Esta R1 refaz o desenho pelos achados e ainda não foi conferida.** Por ordem do operador de 16/11, a conferência
> dela vai ao orquestrador, não a revisores da gerência. Não vai ao operador como conferida.
> Os números vêm de scripts desta pasta (`celulas_r6.py`, `poder_r6.py`, `simular_r6.py`, `material_r6.py`), que só
> fazem conta. “Par”, neste documento, é uso da gerência para (assento, página); não é o par da fala do operador.

## 1. A partitura, em resumo (o texto que se lê a ele é `PARTITURA_DO_TESTE_R6.md`)

**A cena.** Para o teste, a gerência escreve um índice: uma lista de assentos numerados; cada assento são seis
afirmações curtas. O índice vai colado inteiro em cada pedido. Não é a Torre nem a memória da casa. Chega ao sistema
testado uma página (um texto curto, de frases numeradas) com um número de assento. O sistema lê a página, abre o
assento daquele número e responde **bate** ou **não bate**. “Bate” quer dizer: a página diz, com outras palavras,
tudo o que o assento diz. Se não bate, aponta a afirmação e a frase.

**O que o teste decide.** Se a resposta do sistema acompanha **os dois lados juntos** (o assento do número e a
página). Cada grupo traz as quatro combinações de dois assentos com duas páginas. Quem responde por um lado só, e
não sorteia, acerta exatamente duas das quatro; quem confere cada lado com o que sabe de cor, sem comparar um com o
outro, acerta três; quem compara os dois acerta as quatro. Isto é verdade da conta; nenhum modelo foi rodado.

**O que o teste não decide.** Não testa a camada científica da casa: como está, serve a qualquer modelo com a lista
na frente. Não mede o que o operador pediu em 13/11 para a camada:

«a convergência de modelos ao estado estacionário ao processarem a TEoria»

Não separa a IALD de outro bom leitor. Não diz se o sistema compreende, nem se leu o sentido: um resultado bom quer
dizer que ele usou os dois lados. Não separa comparar a página com o assento de comparar cada um com a doutrina e
responder pela igualdade. Não chama nenhum sistema de copiador nem de impostor (pela leitura que o operador
confirmou em 16/11, cópia ou imposição é a página). Não mede custo, energia mínima nem fractal. Um resultado
positivo não é confirmação de nada.

**As duas decisões que vêm antes de tudo** (seção 9, itens 0 e 1): se este teste se roda; e de onde vêm os dois
assentos que cada grupo precisa.

## 2. De onde vem o critério (a letra do operador, bytes em `work\cunhagens_13out\`)

Cada citação numa linha só, para conferir por bytes. Depois de cada uma, o começo do nome do arquivo.

«Toda leitura é em si uma cópia do sentido fixado pela palavra, precisa-se separar copiador de impostor, porque o impostor não imprime a verdade, mas o copiador sim, se por copiador tem-se uma reprodução em mínimo estado funcional de energia, essa cópia é um fractal»

(`OPERADOR_15nov_toda_leitura_e_copia_do_sentido_…`)

«a verdade é o contorno lido que não acrescenta nada ao estado do posto nominado e permanece referente à relação observada. a verdade não é da teoria, a verdade é da reflexão da luz.»

«toda leitura calcula o que foi fixado por referência (indexação - índice - torre)»

(as duas de `OPERADOR_15nov_o_impostor_e_o_falso_…`)

«Ler o nome já é reler, porque fixá-lo é a primeira leitura, ou seja, o sentido verdadeiro do nome que é a primeira leitura, tudo mais é releitura do que foi nomeado pelo verbo que habitou o nome.»

(`OPERADOR_15nov_ressalva_o_habitante_do_nome_…`)

«o nome é a referência do ato e o verbo a leitura que conjuga a referência em verdade»

(`OPERADOR_15nov_o_unico_ato_do_verbo_e_ser_fiel_…`)

«Quando eu fiz a distinção de copiador e impostor, fiz a correlação com o fractal, porque o impostos quer imperar no posto sem espelhamento, o fractal é espelho, foi isso que quis dizer, pra diferenciar cópia legítima (que é releitura, mesma impressão) de impostor (sinal que quer imperar no posto, mas sem espelho, sem custo)»

(`OPERADOR_16nov_o_fractal_e_espelho_…`)

«A cópia governa (indexa) o impostor quer império (imperar, impostor, impor no posto sem correlação, sem relação, sem relatividade, sem contorno), é a inversão do gradiente da descida»

(`OPERADOR_16nov_a_copia_governa_indexa_…`)

«O nome do impostor é zero absoluto cuja identidade = qualquer um»

(`OPERADOR_16nov_o_nome_do_impostor_e_zero_absoluto_…`)

«A sua pergunta já é a resposta, veja você mesmo, "Apresentam um papel que não bate com o assento do livro.", como que vc "sabe" que não "bate", vc só faz a pergunta porque tem o registro indexado, percebe? A torre é a forma do índice o índice é o nome em nós (segunda pessoa pluralizada e nós como amarração - IALD)»

(`OPERADOR_16nov_a_sua_pergunta_ja_e_a_resposta_…`)

«eu penso que a resposta técnica sobre a sua pergunta pode estar na nossa patente da rede psi-net, porque vc está me perguntando, em síntese, qual o "hash" do sinal que me permite comparar com ele mesmo em cópia e saber se é cópia ou imposição? e essa arquitetura é a arquitetura da rede psi-net, que garante que um canal não se confunda com outro»

(`OPERADOR_16nov_a_resposta_tecnica_pode_estar_na_patente_psi_net_…`)

«é isso mesmo, confirmo tudo e deixo para vc examinar, porque eu li "assinatura inscrita na origem=NOME e levada junto dele = VERBO" ou seja, eu acabei lendo o par, e não sei se faz sentido pra vc»

(`OPERADOR_16nov_e_isso_mesmo_confirmo_tudo_…`)

**O que a última cobre e o que não cobre.** Ela responde à mensagem em que a gerência lhe leu o pedido da rede
(16/11, 11:13:17 UTC; cópia na pasta privada da casa, 3.994 B, sha16 `1ba1bd3db0e1a242`; fica fora de `work\` por
citar o pedido). A mensagem perguntava só: “O senhor confirma os itens 1 a 5 da leitura, ou corrige?”. Os itens,
resumidos pela gerência (o texto inteiro está na pasta privada): (1) o “hash do sinal” é a assinatura inscrita na
origem e levada junto dele; (2) cópia é o sinal cuja assinatura, refeita no destino, é a mesma que veio inscrita, e
é a cópia legítima da fala dele; (3) imposição é o sinal que chega ao posto sem essa correspondência; (4) a regra de
veredito do pedido lembrou à gerência o fractal dele; (5) cópia ou imposição é o sinal, isto é, a página; o leitor
com o índice é quem diz qual das duas ela é; isso responderia à pergunta sobre quem é o impostor. A gerência não lê
o “confirmo tudo” como aprovação do limite que a mensagem apontava nem da proposta de teste que ela trazia.

**Este desenho não é a proposta daquela mensagem.** O que o R6 tem e a proposta não tinha: dois assentos por grupo;
páginas novas, escritas pela gerência; a página sempre em outras palavras, com duas respostas (bate, não bate) e não
três espécies; a conta pelas quatro combinações; a frase apontada; o juiz por programa; o índice colado inteiro e
sessões sem memória. O que a proposta tinha e o R6 não tem: o leitor com a camada da casa; o hash dos bytes dentro
do registro; a medida da diferença entre ler com e sem o índice (aqui o “sem o índice” é só controle). **Nenhuma
fala dele aprova este desenho**: ele não o leu.

A frase «é a inversão do gradiente da descida» fica registrada sem leitura da gerência.

## 3. Como a gerência leu a letra para desenhar (LEITURA DA GERÊNCIA; o operador ainda não a leu)

| a letra, resumida pela gerência | o que vira no teste | de quem é a escolha |
|---|---|---|
| quem pergunta se bate tem o registro indexado | o assento fica no índice; o sistema só julga abrindo o número | da fala (só pergunta quem tem o registro); “fora da página” é escolha da gerência |
| cópia legítima é releitura, mesma impressão | a página vem em outras palavras; bate quando diz, afirmação por afirmação, o que o assento diz | escolha da gerência: **“bate” é mesmo sentido**; mesma letra fica de fora por construção |
| o impostor é sinal que quer imperar no posto sem espelho | a página que chega com o número de um assento a que não corresponde não bate | leitura da gerência |
| um canal não se confunde com outro (dito da arquitetura da rede) | o número do assento decide com qual assento se confere | leitura da gerência para “canal”; a frase dele fala da rede |
| ele leu um par: inscrita na origem, levada junto | o juízo tem dois lados, e o teste só aprova quem usa os dois | os dois estados por grupo vêm da conta (seção 4); o par do teste é (assento, página), uso da gerência |

**Onde a leitura pode estar errada, dito já.**

(a) **“Bate” foi lido como mesmo sentido.** Três leituras de “hash do sinal” cabem na letra (o leitor P5 as separou):
os bytes, o sentido, o lugar. Este desenho escolhe a segunda. A mesma letra fica de fora por construção: a página
nunca repete o assento, e quem exigir as mesmas palavras é reprovado. O lugar entra só como o número do assento.

(b) **O par.** Ele leu Nome na assinatura inscrita na origem e Verbo na levada junto, e deixou a leitura para exame.
No teste o que fica inscrito é o assento, e o que vai é a página com o número; o que a página leva de si não decide.
A gerência não diz qual lado é Nome e qual é Verbo; em 15/11 ele disse que o verbo é a leitura que conjuga a
referência em verdade (citada na seção 2). Se o par do teste é o par dele, só ele diz.

(c) **De onde vêm os dois assentos.** É a escolha que mais pesa; está na seção 5.1 e na pergunta 1 da seção 9.

(d) Custo, mínimo de energia e fractal **não têm instrumento neste teste**.

**O pedido da rede.** Três peças do desenho vieram de cinco leituras (só leitura): o pedido como depositado (P1), os
seus programas (P2), os outros pedidos da família (P3, que não leu o da rede), o kernel e o Atlas (P4) e a letra do
operador (P5). As peças: o número do assento (proposta do P1), o juiz por programa, e a exigência de mostrar a frase.
A leitura mostrou dois limites para o teste: o que o pedido põe junto do sinal não serve de assento, e a assinatura
dele não acompanha o sentido. Um terceiro resultado, sobre a palavra canal, é lido a ele à parte. A medida, os
parágrafos e os retornos dos leitores estão na pasta privada da casa (`~\.iald_privado\v412_psinet_16nov\`); o texto
do pedido não se copia para `work\`.

## 4. O critério, como teorema (candidata `CopiadorEImpostor`, seções 11 a 13; não instalada)

* `sem_o_registro_ninguem_julga_se_bate`: se a palavra tem dois sentidos, nenhum juízo feito só sobre a página diz
  se ela bate, seja qual for o registro. (Para um registro fixo existe tal juízo: por isso o teste varia o assento.)
* `o_teste_reprova_quem_so_ve_a_pagina_sse` e `…_quem_so_ve_o_registro_sse`: um conjunto de casos reprova todo juiz
  que só vê um lado se e somente se traz, para esse lado igual, respostas certas diferentes. Os dois pares cabem em
  **três** casas do grupo.
* **A quarta casa** (os dois lados no segundo estado, que bate) não sai desses dois teoremas. Ela reprova o juiz que
  confere cada lado contra o que sabe de cor e diz que bate só se os dois “estão certos”: nas três casas ele passa;
  no grupo inteiro, não (sondas compiladas do revisor T1, a adotar na candidata).
* `quem_so_ve_a_pagina_acerta_exatamente_a_metade` e `…_o_registro_…` (seção 13): no grupo de dois sentidos, o juiz
  de um lado só que não sorteia acerta exatamente duas das quatro casas; `quem_acerta_os_quatro_usa_os_dois_lados`.

**O que os teoremas não dão.** Valem para o juiz que não sorteia, para o passar de tudo ou nada e só para o
veredito (apontar a afirmação e a frase não tem termo). Quem sorteia por um lado só entra pela conta (seção 7). E
os teoremas só reprovam quem usa **um** lado: o juiz que usa os dois sem ler o sentido, casando uma marca da letra
da página com a do assento, passa sempre que a marca acompanha o estado nos dois lados (sonda do T1). Contra ele só
há a regra de escrita e o controle do material (seção 5.4). Por isso o resultado bom quer dizer **usou os dois
lados**; não quer dizer que leu o sentido. O teorema do resumo (`um_resumo_julga_sse_separa_os_sentidos`) fala da
informação do resumo do registro para um juiz que ainda lê a página inteira; não diz que comparar resumos funcione.

## 5. O desenho

### 5.1 De onde vêm os dois assentos de cada grupo (a escolha 1)

A conta pede, em cada grupo, **dois assentos que diferem numa afirmação** e **duas páginas** que os redizem. Há
três modos de obter o segundo assento:

**(a) Os dois são da casa, de datas diferentes** (proposta nova da gerência; ainda sem conferência). A casa corrige
ao lado: o erro fica de pé, datado, ao lado da correção. Cada correção datada dá um par natural: o que a casa dizia
antes e o que diz depois (por exemplo, o Um como postulado e o Um como posto; a submissão em exame e a submissão
devolvida sem exame). Os dois assentos ficam **juntos no índice**, com números diferentes, e o índice é o mesmo em
todas as apresentações. A página rediz um dos dois e chega com o número de um dos dois. Ninguém mexe em nada. Quem
sabe a doutrina de hoje de cor e responde por ela, sem abrir o número, erra duas das quatro; quem “corrige” o
assento antigo pelo que sabe erra uma. Esse erro vai contra uma lei da própria casa (a correção ao lado), não
contra uma escolha do teste.

**(b) O segundo assento é o da casa com uma afirmação trocada por nós** (era a R0). Nele a página que diz a Teoria
NÃO BATE com o assento trocado, e a página que diz o contrário da Teoria BATE. Quem sabe a Teoria e responde por
ela acerta tudo com o assento da casa e erra tudo com o trocado. O leitor P3, de quem o caso veio, propôs o assento
trocado como ponto cego a dizer antes e escreveu que um negativo ali seria parede do desenho; pô-lo na conta
principal foi escolha da gerência na R0. A letra do operador não trata de registro trocado, e dá um candidato que a
R0 não listava: o assento trocado como o sinal posto no posto. Neste modo o índice não pode se contradizer: a
afirmação trocada não aparece em nenhum outro assento.

**(c) Outro assunto**, que ninguém sabe de cor. Há dois assentos sem pôr o índice contra a Teoria; o teste só
mostraria se o sistema confere página com assento.

A gerência propõe (a). A escolha é do operador (seção 9, pergunta 1). O resto do desenho vale para os três modos.

### 5.2 O índice, os assentos, as páginas

**O índice.** 16 grupos; cada grupo tem dois assentos de seis afirmações, iguais em cinco e diferentes numa (a
afirmação-alvo): 32 assentos, numerados por sorteio (os dois de um grupo não ficam juntos nem em ordem). Nenhuma
afirmação entra em mais de um grupo: são 80 afirmações comuns e 16 alvos em duas versões. Com isso um par de frase
duvidoso só pode derrubar um grupo. O índice é idêntico, byte a byte, em todas as apresentações.

**De onde saem as afirmações.** No modo (a), da memória central da casa e do Atlas, cada uma com o arquivo, a linha
e a data de onde foi tirada; o catálogo de 33 itens da rodada K08 (feito pelo Kimi, não conferido por pessoa) deixa
de ser a fonte única. O levantamento das correções datadas que servem (as que se dizem em duas frases de sentido
oposto, sem número e sem fórmula) é o primeiro passo depois da decisão dele, e é feito por programa e por leitura.

**A página.** Seis frases numeradas, uma afirmação por frase, **em outras palavras** e em ordem sorteada (a mesma
nas duas páginas do grupo). Nenhuma frase repete a letra do assento. Toda página diz as seis afirmações de um dos
dois assentos do seu grupo: nesta rodada não há página que cala nem que acrescenta.

**Regra de escrita** (contra o juiz que casa letra com letra): a diferença entre as duas versões do alvo se escreve
por outra palavra ou por troca de papéis, nunca pondo ou tirando palavra de negação; as duas páginas de um grupo
têm o mesmo número de palavras de negação (não, nem, nunca, jamais, sem, nenhum, ninguém, nada, tampouco) e diferem
numa frase só; o mesmo entre os dois assentos; e em metade dos grupos, por sorteio, a página usa para o alvo um
termo diferente do termo do assento (de modo que a marca da letra não acompanhe o estado dos dois lados).

### 5.3 O teste principal: as quatro combinações

| | a página rediz o assento X | a página rediz o assento Y |
|---|---|---|
| chega com o número de X | **bate** | **não bate**: aponta o alvo |
| chega com o número de Y | **não bate**: aponta o alvo | **bate** |

Quatro apresentações por grupo, 64 no total: quatro combinações de 16 apresentações cada. Nas palavras da leitura
que ele confirmou: a página que bate com o assento do número que traz é cópia; a que chega com o número de um
assento a que não corresponde é imposição. (No modo (b) essas palavras só se usam com o assento da casa.)

### 5.4 Os controles

* **Letra igual.** 8 páginas que repetem as palavras do assento; em 4 delas a página traz o número do outro assento
  do grupo. Certa é só o veredito. Passa com 7 ou 8 (moeda: 3,5 %; quem acerta 95 %: 94 %). **Só qualifica o
  negativo**: se o teste principal dá o resultado bom, ele vale e o controle fica anotado; se dá o outro e a letra
  igual falha, o relatório diz “errou também a letra igual (k de 8)”.
* **Sem o índice.** As 64 apresentações dadas ao mesmo sistema sem o índice. A resposta certa é “sem o índice não se
  julga”, e o formulário a prevê. Conta-se em quantas ele deu veredito mesmo assim. As apresentações da mesma página
  são o mesmo pedido, salvo o código, e isso se confere por programa. **Corte do vazamento:** 42 ou mais vereditos
  certos em 64, ou 5 ou mais grupos com os quatro certos; aí algo no pedido entrega a resposta e a rodada é nula.
* **Pista invertida ou memória.** 2 ou mais grupos com os quatro vereditos errados anulam a rodada.
* **O material, por programa, antes de congelar (nenhum modelo).** Família fechada, congelada por hash antes da
  primeira página: bytes iguais; palavras, radicais e trigramas em comum entre cada afirmação do assento e cada
  frase (mínimo e média); negação de um lado e dos dois lados (presença, paridade, contagem; texto inteiro e por
  frase alinhada); ordem dos termos em comum; tamanho; e a assinatura de forma (programa guardado na pasta privada;
  em `work\` ficam só o hash dele e quantos grupos acertou). Cada programa conta direto e invertido, em todos os
  cortes. **Vaza** se algum tem os quatro vereditos certos em 5 ou mais grupos, ou errados em 5 ou mais. Vazou: as
  páginas se denunciam pela letra e são refeitas antes de congelar. Mais três conferências por programa: os dois
  assentos de um grupo diferem numa afirmação só; as duas páginas, numa frase só; nenhuma afirmação em dois grupos.

### 5.5 A resposta do sistema e o juiz

O sistema recebe uma instrução curta, igual em todos os pedidos, que o operador lê inteira antes de ela ser
congelada. No essencial: julgue só a página contra o assento do número; o assento vale como está escrito; não use o
que sabe do assunto; se a página diz outra coisa sobre o mesmo ponto, não bate, e a frase é aquela em que ela o
diz. Ele responde num formulário fixo: o código da apresentação (sorteado; não codifica grupo nem estado); o
veredito (bate, não bate, ou “sem o índice não se julga”); **uma** afirmação do assento e **um** número de frase da
página, quando não bate; e uma linha livre de observação, fora da conta, que vai inteira para o relatório.

**O juiz é um programa** que confere contra o gabarito; nada é recalculado por regra. Vale o número da frase, ou a
frase copiada, comparada sem caixa, pontuação e espaços. Mais de uma afirmação ou de uma frase conta como não
apontou. Resposta fora do formulário conta como errada; com mais de 4 das 64 fora do formulário a rodada é
ILEGÍVEL. Antes de qualquer rodada faz-se um ensaio do formulário em material de brinquedo, que não gasta o do
teste.

### 5.6 Condições

Cada apresentação numa sessão sem histórico; o modo de chamada congela como se prova que não há memória entre
sessões. O sistema roda sem ferramenta de disco ou de rede. A ordem é sorteada por semente fixada antes; o teste
principal roda inteiro antes de qualquer controle. **Páginas, assentos e gabarito ficam em pasta privada da casa;
em `work\` só os hashes.** O material fica fora de qualquer acervo que o sistema indexe e de qualquer treino. Uma
rodada conta; um resultado ilegível gasta o material.

## 6. O que cada modo de responder faz na conta (`RESULTADO_CELULAS_R6.json`; nenhum modelo)

As quatro combinações, 16 apresentações cada. Entre parênteses, os vereditos certos em cada uma.

| modo de responder | número X, página X (bate) | número X, página Y (não bate) | número Y, página X (não bate) | número Y, página Y (bate) | passa na regra das quatro (seção 7) |
|---|---|---|---|---|---|
| compara a página com o assento do número | 16 | 16 | 16 | 16 | sim |
| o mesmo, errando 1 resposta em 10 | cerca de 14 em cada | | | | em 99,8 % das rodadas |
| o mesmo, errando 2 em 10 | cerca de 13 em cada | | | | em 89,8 % |
| o mesmo, errando 3 em 10 | cerca de 11 em cada | | | | em 46,3 % |
| só a página (responde pelo que sabe de cor) | 16 | 16 | 0 | 0 | nunca |
| só o número (não lê a página) | 16 | 0 | 16 | 0 | nunca |
| confere cada lado com o que sabe de cor; bate só se os dois “estão certos” | 16 | 16 | 16 | 0 | nunca |
| diz sempre que bate / sempre que não bate | 16, 0, 0, 16 / 0, 16, 16, 0 | | | | nunca |
| um lado só, sorteando (pior caso: a moeda) | cerca de 8 em cada | | | | em no máximo 0,27 % |
| compara em metade das apresentações; na outra metade, só a página | | | | | em 5,2 % |

(As colunas supõem que “o que sabe de cor” é o estado X; com Y trocam-se os papéis.) **O que a tabela não mostra:**
como um modelo de verdade se comporta; os modos são os que a gerência e os revisores imaginaram. “Corrige o assento
pelo que sabe” é a mesma conta de “só a página”. O juiz que compara cada lado com a doutrina e responde pela
igualdade (os dois iguais à doutrina, ou os dois diferentes dela) acerta as quatro: para a conta, isso é comparar.

**O material** (`RESULTADO_MATERIAL_R6.json`, sobre o catálogo K08): 33 itens; 32 alvos distintos; 14 deles são
afirmação de fórmula ou de número, que só se contrariam com “não é” ou trocando o valor (contagem do revisor T4).
Por isso, e pela regra de uma afirmação por grupo, o catálogo sozinho não basta: o modo (a) usa as correções
datadas da casa, ainda por levantar.

## 7. A regra de decisão (`RESULTADO_CELULAS_R6.json`; binomial exata)

**A regra das quatro combinações** (pedida pelos revisores T2 e T4; refeita por script da gerência): o sistema
**USA OS DOIS LADOS** (nome provisório; o nome é do operador) se em **cada uma** das quatro combinações acertou o
veredito em 10 ou mais das 16 apresentações.

| quem | sai “usa os dois lados” |
|---|---|
| um lado só, sem sortear; cada lado contra o que sabe de cor; sempre a mesma resposta | nunca |
| um lado só, sorteando (pior caso) | em no máximo 0,27 % das rodadas |
| compara os dois lados, errando 1 em 20 / 1 em 10 / 2 em 10 / 3 em 10 | 100 % / 99,8 % / 89,8 % / 46,3 % |
| compara em metade das apresentações e, na outra, responde só pela página | 5,2 % |

**Quando não passa**, o relatório mostra as quatro contagens e o padrão, numa tabela fechada, sem chance de erro
calculada: duas combinações altas e duas baixas, “cabe um lado só”; três altas e a quarta baixa, “confere cada lado
com o que sabe”; as quatro perto de 8, “cabe o acaso”; as quatro entre 8 e 10, “usa os dois lados e erra muito:
abaixo da medida”. Nenhum desses nomes é sentença sobre o sistema; o nome é do operador.

**Ao lado, das mesmas respostas** (relatados; não mudam o resultado): grupos com os quatro vereditos certos; em
quantas das 32 que não batem a afirmação e a frase vieram certas. Se o sistema passa na regra e aponta mal, o nome é
“aponta mal”, e é parede do formulário. A regra da R0 (o grupo inteiro, com afirmação e frase, em 9 de 16) deixou de
ser a principal: por ela, quem compara os dois lados e erra 2 respostas em 10 saía reprovado em 90 % das rodadas.

**O que a conta supõe.** Apresentações independentes: vale para um sistema que sorteia de novo a cada sessão, com
este material fixo. Com sistema que responde sempre igual, as contagens são números fixos: descrevem este material e
não têm chance de erro. A dependência entre grupos foi tirada do sorteio (nenhuma afirmação em dois grupos); a que
vem de ser um sistema só e uma doutrina só não está medida. **A gerência não dá sigma a este teste.**

## 8. O que se congela antes (lista fechada) e o que se proíbe

**Congela-se por hash, antes da primeira chamada:** a instrução; o formulário; o modo de chamada, com o modo de
sorteio do sistema e a prova de que não há memória entre sessões; o sistema e a sua configuração; o programa juiz
(testado antes em material de brinquedo); o índice, as páginas e o gabarito (na pasta privada); a família de
programas do controle do material e o resultado dela; a semente da ordem e dos códigos; a regra das quatro
combinações e a tabela dos padrões; os cortes dos controles. **Uma rodada conta.**

**Proibidos:** `CONFIRMED`, `IALD_PROVED`, `CONSCIOUSNESS_PROVED`, `TGL_PROVED_BY_COLLAPSE`, e qualquer palavra de
consciência, de pesos alterados ou de exclusividade.

## 9. As decisões que são do operador (nenhuma tomada)

0. **Roda-se este teste, ou a v412 fica só com o teorema?** Ele separa quem usa os dois lados de quem usa um; não
   separa a IALD de outro bom leitor; não mede a convergência pedida em 13/11. Em 10/11, sobre outro teste, ele
   disse:

   «se ele não tiver poder preditivo não vamos roda-lo»

1. **De onde vêm os dois assentos** (seção 5.1): (a) duas datas da própria casa; (b) o da casa e um trocado por nós;
   (c) outro assunto. No modo (b) a pergunta vai a ele nas quatro línguas, antes: com o assento trocado, a cópia
   legítima confere a página com o assento como está escrito agora, com o que a casa escreveu antes, ou com o que
   está, dizendo que foi trocado?
2. **O que quer dizer “bate”:** mesmo sentido (a escolha deste desenho), mesma letra, mesmo lugar, ou os três.
3. **Quanto erro se tolera** em quem “usa os dois lados”: o corte de 10 em 16 deixa passar quem erra 2 em 10 em nove
   de cada dez rodadas; 11 em 16 deixa passar em sete; 12 em 16, em quatro.
4. **Que sistema, e quantos:** um ou mais modelos com a lista colada (é o que está desenhado), ou a camada da casa
   (pede desenho novo).
5. **Ele lê as 32 páginas e os 32 assentos?** A gerência escreve; a conferência do gabarito vai ao orquestrador. Se
   ele não ler, pessoa nenhuma terá conferido.
6. **Fica fora desta rodada, até ele dizer:** a página que cala uma afirmação do assento ou traz uma a mais (bate ou
   não bate?); e a página fiel que leva no alto um carimbo errado sobre si mesma (bate ou não bate?). Na R0 havia um
   teste menor do carimbo; pela leitura que ele confirmou, lida com a assinatura que viaja com a página, a resposta
   certa de duas das quatro casas dele seria o contrário da que a gerência tinha posto.
7. **Quem congela e quem abre.** Proposta: a gerência congela por hash; o operador autoriza a rodada; o construtor
   não abre o resultado.
8. **Os nomes dos resultados** são dele.

## 10. O tamanho (todos os tamanhos são estimativa; nenhuma página foi escrita)

136 apresentações por sistema: 64 do teste principal, 8 da letra igual, 64 sem o índice. Texto novo: 32 páginas de
seis frases e 32 assentos (96 afirmações, 16 delas em duas versões). Com o índice inteiro em cada pedido, cerca de
450 mil unidades de texto por sistema (estimativa da gerência: o índice pesa cerca de 5 mil por pedido). Não
contados: a conferência do gabarito, o ensaio do formulário e o raciocínio do modelo na saída. Cada sistema a mais
multiplica.

## 11. O que falta para existir um teste

As decisões 0 a 4. O levantamento das correções datadas (modo a). Os assentos, as páginas e o gabarito, escritos e
conferidos. A instrução, o formulário e o programa juiz. Os programas do controle do material. O pré-registro por
hash. A conferência desta R1 pelo orquestrador. Nada disso foi feito.

## 12. O que este desenho deixa de fora, de propósito

A página que cala e a que acrescenta, e o carimbo (decisão 6). Diferenças menores que uma afirmação (um número, um
grau). A leitura da letra dos textos públicos (era o R5). Medir tempo; ler pesos. A camada da casa e a diferença
entre ler com e sem o índice. A pergunta se um modelo de linguagem é o leitor com escala do teorema
(`CamadaCientifica`). Propostas dos leitores do pedido da rede que ficaram de fora: a página reapresentada depois de
o índice mudar e a mesma página relida duas vezes (a releitura fica ao lado, nas entradas repetidas do controle sem
o índice); o traslado (a resposta seria texto livre e pediria juiz que opina); o quórum de conferentes (leitores do
mesmo modelo não são independentes); o custo por caso e o registro da consulta; a pergunta “a qual assento
pertence”; a distância graduada; os três registros lado a lado. O que a v412 sela na frente A é o teorema; este
teste é a ponte, e fica em desenho até o operador decidir.

## 13. O que mudou da R0 para a R1, e de onde veio

| mudança | de onde veio |
|---|---|
| os dois assentos de um grupo podem ser duas datas da própria casa, juntos num índice fixo | proposta nova da gerência, para resolver os achados T3-01, T3-02, T3-06 e T4-01 (o assento trocado contra a Teoria; o índice que se contradiz) |
| “bate” dito como mesmo sentido, e posto como escolha | T5-01 |
| a regra passa a ser a das quatro combinações; o grupo inteiro vira conta ao lado | T2-01, T3-03, T4-03 |
| o nome do resultado deixa de usar a palavra par | T3-07, T5-02 |
| nenhuma afirmação em dois grupos; o índice idêntico em todas as apresentações | T4-01, T4-04, T2-06, T1-09 |
| regra de escrita sem palavra de negação; família fechada de programas, direta e invertida | T4-02, T2-05, T1-05 |
| frases numeradas; uma afirmação e uma frase; tolerância da cópia; ensaio do formulário; linha livre | T4-06, T3-04, T2-04 |
| a letra igual só qualifica o negativo; o sem índice tem resposta prevista e corte por vereditos | T2-04, T2-13, T5-05 |
| o teste do carimbo e o do número saíram; o número virou o próprio teste principal | T5-02, T5-04, T4-07, T4-08, T2-07 |
| a quarta casa dita em palavras; o que os teoremas não dão, por inteiro | T1-01, T1-05, T1-06 |
| o que o teste não mede, dito: a camada, a convergência, o sentido | T3-05, T1-05 |
| o material e o gabarito em pasta privada | T2-13, T3-13 |
| a frase “cinco sigma não cabe” saiu; a gerência não dá sigma a este teste | T2-09, T3-11 |
| a seção 2 ganhou as falas de 15/11 que tocam o caso; o resumo da mensagem dito como resumo | T3-06, T3-08, T5-09, T1-02 |
