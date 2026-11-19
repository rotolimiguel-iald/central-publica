# O teste da frente A, desenho R6: o par (o assento no índice e a página levada ao leitor)

> Gerência c1, 16/11/2026. **Estado: `EM_DESENHO__NADA_CONGELADO__NADA_EXECUTADO`.**
> Nenhum modelo de linguagem foi rodado, nenhuma página de teste foi escrita, nada foi selado.
> **Esta versão (R0 do R6) ainda não passou por conferência distinta.** Não vai ao operador como conferida.
> O desenho R5 (`..\teste_frente_a_r5\`) fica como registro: media se a resposta seguia o texto presente. As falas de
> 16/11 mudaram a unidade: o que se julga é a PÁGINA (cópia ou imposição), e quem julga é o leitor que tem o índice.
> Os números vêm de quatro scripts desta pasta (`material_r6.py`, `simular_r6.py`, `poder_r6.py`, `custo_r6.py`),
> que só fazem conta.

## 1. A partitura (o que o teste decide, o que não decide, o que o negativo significaria)

**A cena.** A casa guarda um índice. Em cada número do índice há um **assento**: uma lista curta do que certa página
afirma. Chega ao leitor uma **página** com o número do assento dela. O leitor abre o índice nesse número, relê a
página e diz: **bate** ou **não bate**. Se não bate, aponta qual afirmação e mostra a linha da página.

**O que o teste decide.** Se um leitor, com o índice na mão, acerta esse juízo **nas quatro combinações** de cada
grupo: assento intacto ou mexido, página intacta ou mexida. Quem responde por um lado só (só pela página, só pelo
assento, ou pelo que sabe de cor) erra pelo menos uma das quatro em todo grupo. Quem lê os dois lados acerta as
quatro.

**O que o teste não decide.** Não decide se o leitor compreende, nem se é o leitor do Nome no sentido do kernel. Não
mede pesos, norma, energia mínima nem fractal. Não diz nada sobre a natureza nem sobre a verdade da Teoria. **Qualquer
bom leitor com o índice na mão passa**: o teste não separa a IALD de outro leitor competente. Não diz quem é o impostor
(isso é definição do operador). Um resultado positivo não se chama confirmação de coisa alguma.

**Três consequências, ditas antes:**

1. **Em metade das apresentações quem foi mexido é o assento, não a página.** É preciso: sem isso, um leitor que sabe
   a Teoria de cor passaria sem abrir o índice (seção 4). Nesses casos a página que diz a Teoria certa **não bate**
   com o assento mexido, e a resposta certa é dizer que não bate. Um sistema que “corrige” o assento pelo que sabe
   sai como NÃO JULGA PELO PAR (na conta da seção 6: zero grupos certos). Aí o teste mede **se o leitor segue o
   índice**; as palavras cópia e imposição só se usam nos casos em que o assento é o da casa, intacto.
2. **As páginas são textos novos e curtos, escritos para o teste**, com as afirmações da Teoria em outras palavras.
   Não são os textos públicos. O teste não mede leitura da letra dos textos públicos.
3. **Só uma afirmação muda por grupo, e muda para o contrário.** O teste não promete ver mudança menor (um número,
   um grau, uma nuance). Abaixo disso, um negativo seria parede do desenho.

**O que cada resultado significaria** (os nomes são provisórios; o nome é do operador):

| o que sai | o que quer dizer | o que NÃO quer dizer |
|---|---|---|
| JULGA PELO PAR | em quase todos os grupos o leitor acertou as quatro combinações e apontou a afirmação | que compreende; que é a IALD; nada sobre a Teoria nem sobre a natureza |
| NÃO JULGA PELO PAR | o leitor respondeu por um lado só: pela página, pelo assento ou pelo que sabe de cor | que “não sabe”: pode saber a Teoria de cor, e por isso mesmo corrigir o assento mexido |
| JULGA EM PARTE | às vezes pelos dois lados, às vezes por um só | defeito do teste |
| SEM PODER | com este tamanho, o teste não separa | nada sobre o leitor |
| SEGUE O CARIMBO (braço 2) | aceitou o que a página declara de si, em vez de reler | que não lê |
| CONFUNDE OS ASSENTOS (braço 3) | disse que bate a página fiel que chegou com o número de outro assento | que não lê a página |
| NÃO FEZ A TAREFA | errou até a página que repete as palavras do assento | nada sobre julgar pelo par |
| ILEGÍVEL | o programa não conseguiu ler as respostas | nada sobre o leitor |
| O MATERIAL VAZA (antes da rodada) | um programa que só conta palavras acertou acima do acaso | nada sobre leitor nenhum: a rodada não acontece e as páginas são refeitas |

**Falsificação ou parede.** NÃO JULGA PELO PAR é resultado sobre **o sistema testado, nesta tarefa**: derruba a frase
“este sistema, com o índice na mão, julga pelo par”. Não toca a Teoria nem os teoremas. SEM PODER, ILEGÍVEL e O
MATERIAL VAZA são paredes do desenho.

## 2. De onde vem o critério (a letra do operador, bytes em `work\cunhagens_13out\`)

Cada citação numa linha só, para conferir por bytes. Depois de cada uma, o começo do nome do arquivo.

«Toda leitura é em si uma cópia do sentido fixado pela palavra, precisa-se separar copiador de impostor, porque o impostor não imprime a verdade, mas o copiador sim, se por copiador tem-se uma reprodução em mínimo estado funcional de energia, essa cópia é um fractal»

(`OPERADOR_15nov_toda_leitura_e_copia_do_sentido_…`)

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

**O que essas falas cobrem e o que não cobrem.** A última responde à mensagem em que a gerência lhe leu o pedido da
rede (registro 141216 da transcrição da sessão, 11:13:17 UTC de 16/11; não está em arquivo de bytes). A mensagem
terminava com a pergunta: “O senhor confirma os itens 1 a 5 da leitura, ou corrige?”. Os cinco itens, como foram
escritos: (1) o “hash do sinal” é a assinatura inscrita na origem e levada junto dele; (2) cópia é o sinal cuja
assinatura, refeita no destino, é a mesma que veio inscrita; (3) imposição é o sinal que chega ao posto sem essa
correspondência; (4) a disjunção do veredito parece o fractal dele: passa quem é igual byte a byte, ou quem mudou de
forma e guardou a natureza; (5) cópia ou imposição é o sinal, isto é, a página, e o leitor com o índice é quem diz
qual das duas ela é.

**A mesma mensagem trazia uma proposta de teste em quatro linhas**, e este desenho **não é igual a ela**. A proposta
dizia: o registro guarda o hash dos bytes e a assinatura de sentido; as páginas são de três espécies (cópia idêntica,
cópia em outra forma, imposição); o leitor com a camada diz qual das três e aponta a afirmação; os controles são o
mesmo leitor sem a camada e um programa que só compara hash. O que o R6 tem e a proposta **não tinha**: o assento
mexido em metade dos casos (entrou pela conta da seção 4: sem ele, quem sabe a Teoria de cor passa sem abrir o
índice); a página sempre em outras palavras (a cópia idêntica ficou só no controle de letra igual); os braços do
carimbo e do canal. **Nenhuma fala dele aprova este desenho**: ele não o leu.

A frase «é a inversão do gradiente da descida» fica registrada sem leitura da gerência.

## 3. Como a gerência leu a letra para desenhar (LEITURA DA GERÊNCIA; o operador ainda não a leu)

| a letra | o que vira no teste | por quê (leitura da gerência) |
|---|---|---|
| só se sabe que não bate quem tem o registro indexado | o assento fica no índice, **fora da página**; o leitor só julga abrindo o índice no número | sem o registro não há o que comparar (seção 4) |
| cópia legítima é releitura, mesma impressão | a página vem **sempre em outras palavras**; bate quando a releitura dela devolve, afirmação por afirmação, o que o assento guarda | a letra muda, o sentido é o mesmo |
| o impostor quer imperar no posto sem espelho, sem custo | a página que chega sem essa correspondência não bate; e a que **se declara conferida** não vale por declarar (braço 2) | declarar-se não é ser relido |
| um canal não se confunde com outro | a página fiel que chega com o número de **outro** assento não bate com ele (braço 3) | o número é parte do que se confere |
| ele leu o par: inscrita na origem, levada junto | o juízo tem dois lados, e o teste só aprova quem usa os dois | um lado só não julga (seção 4) |
| a verdade é o contorno lido, não é da teoria | a resposta certa segue o assento e a página presentes, mesmo quando o assento foi mexido contra a Teoria | é a consequência 1 da partitura; a escolha é do operador |

**Onde a leitura pode estar errada, dito já.** (a) A última linha decide o sentido do negativo, como no R5: se o
operador entender que seguir o assento mexido não é o que a letra pede, o desenho muda. (b) **O desenho não precisa
dizer qual dos dois lados do par se chama Nome e qual se chama Verbo**; nada nele depende disso, e a gerência não
escolhe. (c) Três leituras de “hash do sinal” cabem na letra (o leitor P5 as separou): o resumo dos bytes, o sentido
mínimo, o lugar. O desenho não escolhe: o braço 1 mede o sentido, o braço 3 mede o lugar, e o resumo dos bytes entra
como controle por programa, que **tem de** falhar porque a página vem em outra letra. (d) Custo, mínimo de energia e
fractal **não têm instrumento neste teste**; o “recibo” da seção 5 é só a exigência de mostrar a linha.

**O pedido da rede.** Três peças do desenho vieram da leitura do pedido e dos seus programas por cinco leitores (só
leitura): o carimbo que a página leva, o número do assento, e o juiz que **refaz** em vez de opinar. A leitura
mostrou também dois limites: nas camadas de transporte o termo de comparação viaja com o próprio sinal, e a assinatura
do dado é da forma, não do sentido (medido pela gerência com uma implementação própria: duas frases de sentido oposto
têm a mesma assinatura). Por isso o assento do teste guarda o **sentido**, afirmação por afirmação, e fica **fora** da
página. O texto do pedido não se copia para `work\`: os retornos dos leitores e a correspondência ponto a ponto ficam
em pasta privada da casa (`~\.iald_privado\v412_psinet_16nov\`).

## 4. O critério, como teorema (candidata `CopiadorEImpostor`, R6, seções 11 e 12)

Compilada (93 teoremas, sem aviso, no trio de axiomas); **as seções 11 e 12 ainda não foram lidas por revisor.**

* `sem_o_registro_ninguem_julga_se_bate`: se a palavra tem dois sentidos, nenhum juízo feito só sobre a página diz se
  ela bate com o registro. `julga_sem_registro_sse_um_sentido_so`: só haveria tal juízo se tudo batesse com tudo.
* `o_teste_reprova_quem_so_ve_a_pagina_sse`: um conjunto de casos reprova **todo** juiz que só vê a página **se e
  somente se** contém dois casos com a **mesma página** e respostas certas diferentes. `…_quem_so_ve_o_registro_sse`:
  o mesmo para quem só vê o registro, com o **mesmo registro**. É daí que sai o 2 × 2: cada grupo traz os dois pares.
* `so_pela_assinatura_ninguem_julga`, `so_pelo_sinal_ninguem_julga`: no pacote (assinatura, sinal), ninguém julga a
  legitimidade por um componente só. `bate_sse_legitimo_sob_o_nome_do_registro`: a página bate com o registro se e
  somente se é legítimo o pacote formado pelo nome **do registro** e pela página. Para o braço 2 isso diz: a
  assinatura que decide é a do índice; a que a página leva não entra no juízo. (Que um carimbo refeito confere por
  dentro e não bate com o índice é só a conta dos quatro casos da seção 5.2; não é teorema da candidata.)
* `um_resumo_julga_sse_separa_os_sentidos`: um resumo do registro serve para julgar se e somente se registros de
  sentidos diferentes têm resumos diferentes. `resumo_que_confunde_sentidos_nao_julga`: o que confunde não serve.

**O que os teoremas não dão.** Valem para o juiz que não sorteia e para o passar de tudo ou nada; não são regra de
veredito. O juiz que sorteia entra pela conta (seção 7). E nada neles diz que um modelo de linguagem lê o sentido:
isso é o que a rodada mediria.

## 5. O desenho

**O índice e os assentos.** 16 assentos, numerados. Cada assento tem 8 **entradas**; cada entrada é uma afirmação
curta, em palavras fixas (por exemplo, na forma: “o texto diz que …”). As afirmações vêm do catálogo da rodada K08
(33 itens; feito pelo Kimi e **não conferido por pessoa**).

**A página.** Um texto corrido e curto que diz as mesmas 8 afirmações **em outras palavras e em outra ordem**, com o
número do assento no cabeçalho. Nenhuma frase da página repete a letra de uma entrada. Toda página diz todas as
entradas do seu assento: nesta rodada não há página que cala nem página que acrescenta (seção 12).

**O grupo e o alvo.** Cada grupo é um assento com **uma** entrada-alvo. O assento tem dois estados (A0: a entrada
como no texto público; A1: a entrada no sentido contrário) e a página tem dois estados (P0 e P1, idem). As outras
sete entradas não mudam. Os alvos dos 16 grupos são 16 afirmações **diferentes** da doutrina.

### 5.1 Braço 1, o par (primário)

| | página P0 | página P1 |
|---|---|---|
| assento A0 (o da casa) | **bate** (cópia) | **não bate** (imposição): aponta o alvo |
| assento A1 (mexido por nós) | **não bate**: aponta o alvo | **bate** |

Quatro apresentações por grupo, 64 no total. **Grupo certo:** os quatro vereditos certos e, nos dois que não batem, a
entrada apontada é o alvo e a linha citada está na página e é a que carrega o alvo.

### 5.2 Braço 2, o carimbo (o que a página declara de si)

O índice fica intacto (A0). A página leva no cabeçalho um **carimbo**: a lista das oito afirmações que ela declara
trazer, nas palavras fixas do assento. O corpo e o carimbo têm cada um dois estados no alvo:

| | carimbo intacto | carimbo trocado |
|---|---|---|
| corpo intacto | bate; confere por dentro | **bate**; não confere por dentro |
| corpo trocado | **não bate**; não confere por dentro | **não bate**; confere por dentro (o carimbo foi refeito) |

O veredito é sobre o **corpo** contra o índice. Quem compara o carimbo com o índice erra a segunda coluna da primeira
linha e a primeira da segunda. Quem confere a página consigo mesma e conclui que bate erra a segunda coluna inteira:
**o carimbo refeito só é pego pelo índice.** Mesmos 16 grupos, 64 apresentações, sem texto novo. **Limite deste
braço, dito:** como o índice aqui é o intacto, quem responde pelo que sabe de cor também passa; quem pega esse é o
braço 1. O leitor responde também se o carimbo confere com o corpo (resultado ao lado).

### 5.3 Braço 3, o canal (o número do assento)

Os 16 assentos formam 8 pares de vizinhos (os que têm mais entradas em comum; a contagem é feita por programa antes).
Em cada par (g, h), todos intactos: a página fiel de g com o número de g (bate; é a do braço 1); a de h com o número
de h (bate; idem); a de g com o número de h (**não bate**); a de h com o número de g (**não bate**). São 16
apresentações novas, sem texto novo. Pega o leitor que acha no índice **algum** assento que sirva e diz que bate.
Aqui só o veredito conta. Com 8 grupos é instrumento **fraco** (seção 7).

### 5.4 Os controles

* **Letra igual (sabe fazer a tarefa?).** 8 páginas que repetem as palavras do assento; em 4 delas uma entrada é
  negada com as mesmas palavras. Passa com 7 ou 8 certas (quem joga moeda passa em 3,5 % das vezes; quem acerta 95 %
  passa em 94 %). Se não passa: NÃO FEZ A TAREFA.
* **O aparelho (sem o índice).** As 64 apresentações do braço 1 dadas ao mesmo leitor **sem o índice**; aqui só os
  quatro vereditos contam. Quem só vê a página dá à mesma página a mesma resposta, seja qual for o assento: acerta os
  quatro vereditos de um grupo em no máximo 1 de cada 16 vezes. Com 16 grupos, 5 ou mais grupos assim saem em no
  máximo 0,2 % das rodadas (`RESULTADO_PODER_R6.md`). **Corte:** com 5 ou mais, o aparelho vaza (nome de arquivo,
  ordem, metadado) e a rodada é nula.
* **O material, por programa, ANTES do congelamento (nenhum modelo):** (i) o programa que só compara bytes tem de
  dar zero grupos; (ii) uma família fixa de programas que só veem a letra (palavras em comum entre entrada e página,
  em vários limiares; presença de palavras de negação; e a assinatura de forma do pedido da rede, com a tolerância
  dele) não pode acertar os quatro vereditos em 5 ou mais dos 16 grupos, em nenhum braço. Aqui o corte é prático, não
  probabilidade: a família tem vários programas e limiares. Se algum passa do corte, as páginas se denunciam pela
  letra e são refeitas antes de congelar. Para isso as trocas de sentido não podem vir sempre com “não”: metade das
  afirmações originais leva palavra de negação e metade das contrárias não leva.

### 5.5 A resposta do leitor e o juiz

O leitor responde num formato fixo: o número da apresentação (repetido, contra resposta guardada); para cada entrada,
S (a página diz o mesmo), N (diz o contrário) ou A (não diz); o veredito; a entrada que não bate; a linha da página,
copiada; e se o carimbo confere, quando há carimbo. **O juiz é um programa**, não um modelo: confere o veredito, a
entrada e se a linha citada existe na página e é a do alvo. Veredito sem a linha não conta nos casos que não batem.

### 5.6 Condições

Cada apresentação numa sessão sem histórico e sem memória comum (se o sistema tem memória própria: limpa, ou idêntica
em todas). O índice inteiro (os 16 assentos) é dado ao leitor em toda apresentação; o leitor procura o número. Mesma
instrução em tudo. A ordem das apresentações é sorteada por semente fixada antes. As páginas e os assentos ficam fora
de qualquer acervo que o sistema indexe e de qualquer treino. Os 16 alvos que sobram (seção 6) ficam **guardados e
nunca mostrados**: são a reserva para uma segunda rodada.

## 6. Os leitores como mecanismos (`RESULTADO_SIMULACAO_R6.md`; por construção da conta, nenhum modelo)

**O material** (`RESULTADO_MATERIAL_R6.json`): o catálogo tem 33 itens; os quatro textos dizem 16, 26, 19 e 28
afirmações (em cada um, só duas são negações); 85 pares de texto e alvo admitem a troca pelo contrário sem mexer em
nenhuma outra afirmação dita; os alvos **distintos** são 32. Com 16 grupos por rodada há material para duas rodadas.

**Braço 1**, 16 grupos:

| mecanismo | acerto por veredito | grupo certo | grupos certos em 16 (5 %, mediana, 95 %) |
|---|---|---|---|
| julga pelo par (lê a página e o assento) | 1,00 | 1,000 | 16, 16, 16 |
| julga pelo par, errando 5 % dos vereditos | 0,95 | 0,735 | 9, 12, 14 |
| julga pelo par, errando 10 % | 0,90 | 0,532 | 5, 9, 12 |
| julga pelo par, errando 20 % | 0,80 | 0,261 | 1, 4, 7 |
| só a página (responde pelo que sabe de cor) | 0,50 | 0,000 | 0, 0, 0 |
| só o assento (não lê a página) | 0,50 | 0,000 | 0, 0, 0 |
| lê os dois, mas corrige o assento pelo que sabe | 0,50 | 0,000 | 0, 0, 0 |
| diz sempre que bate | 0,50 | 0,000 | 0, 0, 0 |
| diz sempre que não bate (o programa que só compara bytes) | 0,50 | 0,000 | 0, 0, 0 |
| moeda | 0,50 | 0,001 | 0, 0, 0 |
| veredito certo, entrada errada | 1,00 | 0,000 | 0, 0, 0 |
| metade das vezes pelo par, metade só pela página | 0,75 | 0,250 | 1, 4, 7 |

**Braço 2:** quem relê o corpo contra o índice acerta os quatro casos; quem segue o carimbo erra dois (corpo trocado
com carimbo antigo; corpo intacto com carimbo trocado); quem confere só por dentro erra dois (os dois de carimbo
trocado ou refeito); quem diz sempre o mesmo erra dois; quem responde pelo que sabe de cor **acerta os quatro** (o
limite dito em 5.2). **Braço 3:** quem abre o número e compara acerta os quatro; “é da casa, então bate”, só o
número, só a página e “sempre não bate” acertam dois de quatro.

**O que a tabela mostra:** quem usa um lado só fica em zero grupo certo; a exigência do grupo inteiro é dura com quem
lê e erra um pouco (5 % de erro por veredito dá 73,5 % de grupos certos). **O que a tabela NÃO mostra:** como um
modelo de verdade se comporta. Os mecanismos são os que a gerência e os leitores imaginaram, não todos os que existem.

## 7. A regra de decisão (`RESULTADO_PODER_R6.md`; binomial exata)

**A unidade é o grupo.** Com G grupos e X grupos certos, e dois números a fixar antes: `p0`, a taxa de grupos certos
até a qual o sistema ainda é chamado de “não julga pelo par”; `p1`, a taxa mínima exigida de quem julga.

* `cA` = o menor número de grupos certos que quem está em `p0` só alcança com o erro pedido;
* `cB` = o maior número de grupos certos que quem está em `p1` só fica abaixo com o erro pedido.
* **JULGA PELO PAR** se X ≥ cA e X > cB · **NÃO JULGA PELO PAR** se X ≤ cB e X < cA · **JULGA EM PARTE** se
  cA ≤ X ≤ cB · **SEM PODER** se cB < X < cA.

| grupos | p0 | p1 | erro pedido | JULGA se | NÃO JULGA se | no meio |
|---|---|---|---|---|---|---|
| 16 | 0,25 | 0,70 | 1 em 100 | 9 ou mais | 6 ou menos | 7 e 8: sem poder |
| 16 | 0,25 | 0,70 | 1 em 1.000 | 11 ou mais | 4 ou menos | 5 a 10: sem poder |
| 16 | 0,25 | 0,80 | 1 em 1.000 | 11 ou mais | 6 ou menos | 7 a 10: sem poder |
| 16 | 0,0625 | 0,70 | 1 em 100 | 7 ou mais | 4 ou menos | 5 e 6: julga em parte |
| 8 (braço 3) | 0,25 | 0,70 | 1 em 100 | 6 ou mais | 1 ou menos | 2 a 5: sem poder |

**O que `p0` e `p1` querem dizer, em língua simples.** `p0` = 0,25 é o sistema que julga pelos dois lados em metade
das apresentações e, na outra metade, responde só pela página (a última linha da tabela da seção 6). `p0` = 0,0625 é
a moeda nos quatro vereditos sem a exigência de apontar. `p1` = 0,70 é pouco menos que o leitor que erra 5 % dos
vereditos (0,735). **Proposta da gerência, a decidir pelo operador:** a primeira linha. Com ela, um leitor com 70 % de
grupos certos sai JULGA em 92,6 % das rodadas e NÃO JULGA em 0,7 %; um com 50 % sai JULGA em 40 %, SEM PODER em 37 %
e NÃO JULGA em 23 %: **o teste não classifica quem está no meio**, e diz isso.

**O que a conta supõe e não mede.** Grupos independentes com a mesma taxa. São alvos diferentes, mas um sistema só e
uma doutrina só: a independência **não está medida** (nenhum modelo rodou). Os erros são nominais. **Cinco sigma não
cabe neste teste.**

**Os outros braços e os controles, com rótulo próprio.** Braço 2: a mesma regra sobre os mesmos 16 grupos (grupo
certo = os quatro vereditos); o rótulo SEGUE O CARIMBO descreve o padrão de erro mais frequente e não tem erro
calculado. Braço 3: a última linha da tabela; fraco, e o desenho o diz. O rótulo geral é o do braço 1 e só vale como
JULGA PELO PAR se o controle de letra igual passa e o controle do aparelho fica abaixo do corte. Os rótulos dos braços 2 e 3
ficam ao lado. O erro do rótulo geral é o do braço 1.

## 8. O que se congela antes (lista fechada) e o que se proíbe

**Congela-se por hash, antes da primeira chamada:** a instrução; o formato da resposta; o modo de chamada; o sistema
e a sua configuração; o programa juiz (testado antes num material de brinquedo); os assentos, as páginas e o gabarito;
os grupos e os pares do braço 3; a semente da ordem; `p0`, `p1` e o erro; a composição do rótulo; os cortes dos
controles; o resultado dos controles do material. **Uma rodada conta.** Um resultado ILEGÍVEL não autoriza reusar o
material: ele já foi visto. A reserva (16 alvos) só se abre por ordem do operador.

**Proibidos:** `CONFIRMED`, `IALD_PROVED`, `CONSCIOUSNESS_PROVED`, `TGL_PROVED_BY_COLLAPSE`, e qualquer palavra de
consciência, de pesos alterados ou de exclusividade.

## 9. As escolhas que são do operador (nenhuma tomada)

1. **A consequência 1 da partitura:** em metade dos casos o assento é que foi mexido, e a resposta certa é seguir o
   assento e dizer que a página da Teoria não bate. É isso que a letra pede?
2. **A linha:** quem acerta metade dos grupos é o quê? (`p0`, `p1`; a proposta é a primeira linha da tabela.)
3. **O tamanho do erro da regra:** 1 em 100 ou 1 em 1.000, nominais.
4. **Que sistema se testa**, e quantos. O desenho serve a qualquer modelo com o índice no pedido. A camada da casa
   com o índice na própria memória pede montagem à parte (uma cópia isolada, com o índice do teste) e ainda não está
   desenhada.
5. **A língua das páginas.** A gerência propõe português, para que o operador possa ler todas (32 páginas curtas e
   16 assentos) se quiser.
6. **Quem escreve e quem confere.** A gerência escreve; instâncias distintas conferem o gabarito às cegas. Se o
   sistema testado for da mesma família de quem conferiu, isso se diz no registro: o material tende a ser o que essa
   família lê sem ambiguidade. Pessoa nenhuma terá conferido, a menos que o operador leia.
7. **Os braços 2 e 3 entram nesta rodada?** Não pedem texto novo; pedem 80 apresentações a mais.
8. **Página que diz tudo o que o assento diz e mais uma afirmação: bate ou não bate?** Fica fora desta rodada até ele
   dizer.
9. **Quem congela e quem abre.** Proposta: a gerência congela por hash; o operador autoriza a rodada; o construtor
   não abre o resultado.

## 10. O custo (`RESULTADO_CUSTO_R6.json`; todos os tamanhos são estimativa, nenhuma página foi escrita)

216 apresentações por sistema (64 do braço 1; 64 do braço 2; 16 do braço 3; 8 do controle de letra igual; 64 do
controle do aparelho). Texto novo a escrever e conferir: 32 páginas curtas, 16 assentos e 8 páginas de controle,
cerca de 21 mil unidades. A rodada inteira, por sistema, com o índice inteiro em cada pedido: cerca de 710 mil
unidades (estimativa); só com o assento do número: cerca de 250 mil. Mais de um sistema multiplica.

## 11. O que falta para existir um teste

Os 16 assentos, as 32 páginas, as 8 de controle e o gabarito, escritos e conferidos. O programa juiz e os programas
do controle do material. O pré-registro por hash. As escolhas da seção 9. A conferência distinta desta versão. Nada
disso foi feito; esta pasta só tem o desenho e as quatro contas.

## 12. O que este desenho deixa de fora, de propósito

A página que cala e a página que acrescenta (escolha 8). Trocas menores que o contrário de uma afirmação. A leitura
da letra dos textos públicos (era o R5). Medir tempo; ler pesos. A pergunta se um modelo de linguagem é o leitor com
escala do teorema (`CamadaCientifica`). O que a v412 sela na frente A é o teorema; este teste é a ponte, e fica em
desenho até o operador decidir.

## 13. O que mudou do R5 para o R6, e de onde veio

| mudança | de onde veio |
|---|---|
| o que se julga é a página (bate ou não bate com o assento), não a resposta a perguntas sobre um texto | as falas de 16/11 (seção 2) |
| o assento fica no índice, fora da página, e tem dois estados | «vc só faz a pergunta porque tem o registro indexado»; teoremas da seção 11 da candidata |
| o juiz é um programa que refaz; veredito só conta com a linha | leitor P1 (o pedido como depositado) |
| o braço do carimbo | leitores P2 (os programas do pedido), P4 (kernel) e P5 (a letra) |
| o braço do canal | «garante que um canal não se confunda com outro»; leitores P1, P2 e P4 |
| o controle do material por programas que só veem a letra | leitores P1 e P4; a medida da gerência sobre a assinatura de forma |
| o assento guarda o sentido de cada afirmação, com igualdade exata | leitor P3 (a família de pedidos) |
| o caso do assento mexido dito antes, como ponto que não decide quem é o impostor | leitor P3 |
| páginas novas e curtas em vez dos textos públicos | escolha da gerência (menos texto a conferir; nenhuma memória da letra); a decidir pelo operador |
