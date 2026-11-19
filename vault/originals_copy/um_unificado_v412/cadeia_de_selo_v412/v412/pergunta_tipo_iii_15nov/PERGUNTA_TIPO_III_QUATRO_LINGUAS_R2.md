# O que falta para o tipo III como termo, e a pergunta nas quatro línguas

Gerência c1, 15/11/2026. Terceira versão (R2). A primeira foi a quatro revisores distintos (dois a reprovaram por erros de fato da gerência). A segunda foi a dois (ambos aprovaram com ressalvas; um achado alto, na frase de abertura). Os consertos de uma linha pedidos pela segunda conferência foram aplicados pela gerência nesta versão e não foram relidos por terceiro. Nada aqui está instalado. O anexo técnico, no fim, é para registro; a leitura ao operador é das seções 1 a 6.

## 1. Em palavras simples

A definição de tipo (I, II, III) dos matemáticos não existe no kernel nem na biblioteca que ele usa. Hoje “tipo III₁” aparece no kernel de dois modos: como rótulo, e como a definição operacional de agosto, a testemunha da torre (um estado normal que não é traço, a marca densa, nenhum estado que seja traço normal). O kernel habita essa definição e a sexta bandeira do gate se apoia nela. Mas a marca densa o próprio kernel já retirou como critério de tipo (v295), e o cabeçalho da definição diz que o resto ainda não é o tipo. Nenhum teorema conclui o tipo III dos matemáticos de objeto algum.

Por isso “tipo III como termo” pede duas coisas, nesta ordem: dizer o que a palavra diz, e provar que o objeto o cumpre.

A matemática tem ao menos quatro marcas do tipo III, de dois alcances. Duas alcançam o “tipo III₁”. Duas dizem só “tipo III”. (O 1 de III₁ é a razão de escala de Connes; não é o Um posto. A coincidência é só de escrita.)

- (a) pelo ESTADO, numa álgebra que não é só os números: no relógio do próprio estado, só o Um fica parado. Basta para III₁.
- (b) pela FALTA DE MEDIDA: não existe medida das partes que não dependa da ordem, nem finita nem de peso infinito (os matemáticos dizem: nenhum traço normal semifinito não nulo). “Medida” é a sua palavra para o lado do tipo I; a marca é a falta dela. Diz só III.
- (c) pelas PARTES: toda parte não nula equivale ao todo. Diz só III.
- (d) pelo RELÓGIO: nenhum estado tem cadência preferida. Olham-se os relógios de todos os estados, e o que sobra em comum é a semirreta inteira; um estado só não basta para dizê-lo. No tipo III isso equivale a o núcleo ser uma peça só. Diz III₁.

Na literatura, dentro de cada par as marcas se equivalem: (b) com (c); (a) com (d). De (a) sai o III₁ sempre. A volta só vale com uma condição técnica, e então existem estados assim, não todo estado. Escolher qual marca é o nome não muda o que é verdade; muda o que o kernel prova por dentro e o que entra por citação.

Para a cunha da luz livre, a marca (a) já está provada no kernel, em quatro peças: a álgebra da cunha não comuta; o vácuo não anula nada dela que não seja zero; o que o relógio da cunha deixa parado é múltiplo do Um; e esse relógio é o relógio modular do vácuo. A matemática conhecida diz que isso basta para o III₁ (teorema atribuído a Longo, 1979; lido hoje em duas provas independentes), junto com um fato clássico que entra por citação: o que comuta com o estado é o que o relógio deixa parado. Um dos leitores escreveu em rascunho o enunciado (umas dez linhas) e a ligação com o que o kernel já prova (cerca de quinze); o Lean aceita; fica a refazer amarrado ao relógio modular, porque o rascunho deixou o relógio solto.

Das outras três marcas, para a cunha: de (b), nada; de (c), só pedaços soltos, sem ligação com a cunha; de (d), metade.

Então o que falta, antes de qualquer prova nova, é uma escolha: qual marca é o nome. Essa escolha é sua.

## 2. “É só isso que falta?”

Não, e tem de ser dito.

- A prova da ergodicidade (a T1) não usa o tipo. Usa o estado em que só o Um fica parado, que na cunha da luz já é teorema. As peças da T1 que seguem abertas, e a passagem da cunha ao horizonte, foram ao Codex.
- O tipo como termo também não resolve o passo de Gromov–Hausdorff (o limite das geometrias) no caso III₁, que segue conjectura; nem a derivação de τ★, que espera a sua resposta sobre o relógio do pedágio. Sobre a montagem das quatro dimensões (3+1), a gerência não aferiu se o tipo a toca.
- Não move o selo nem o gate. A sexta bandeira do gate segue apoiada na definição operacional da torre; nenhuma resposta a move.

O que ele fecha: para a cunha da luz livre, uma palavra hoje só citada passa a ter um critério provado e uma citação com nome. E dá ocasião de corrigir ao lado as superfícies da casa que hoje dizem coisas diferentes sobre o tipo (a lista está no anexo).

## 3. O que o senhor já disse (bytes abertos pela gerência; os erros de digitação são seus e ficam como estão)

- 02/11: «De um lado, o que você tem é o fluxo, do outro, o que você tem é medida.» e «não há uma ponta para o Tipo I o que há é o espelhamento da informação acontecendo em tempo real, de um lado o tipo I, concentrado, comprimido, de outro lado, o tipo III, contínuo.» Na sua letra, o fluxo e o contínuo estão do lado do tipo III; a medida, o comprimido, do lado do tipo I.
- 02/11, corrigindo uma frase da gerência: «a luz tem autovetor a inscrição do um absoluto que é na essência ela mesma, ou seja, identidade o um absoluto inscrito é a identidade da luz». A fala diz que a luz tem como autovetor o Um inscrito; não diz que ele é o único parado, nem que isso define o tipo. O kernel prova que o único vetor que o relógio da luz deixa parado é o Um, e daí sai a marca (a). Ligar a fala à marca (a) é leitura da gerência.
- 04/11: «toda geomtria tem traço no finito, no infinito é mera impedância». Cuidado com o homônimo: “traço” tem três sentidos no kernel, e a gerência não lê esta fala como a marca (b).
- 12/10: «o paradoxo de zenão resolvido no contínuo III1». “Contínuo” é a sua palavra para o III.
- Sobre importar ou construir. A regra registrada em 27/09 no CLAUDE.md da raiz (bytes não abertos): o que é sabido e pode ser importado não precisa ser provado, portanto não falta nada. 02/11, antes da partitura das chaves: «então não vamos construir ainda o que é sabido». 02/11, em resposta à partitura das 42 chaves, onde a parede era a face de Fock: «precismamos construir tudo, porque não podemos mais perder a ordem lógica, é o fechamento»; essa superou a anterior para aquelas quatro chaves, que a v406 depois habitou, e que ela valha além disso é leitura da gerência. 11/11: «O que é matemática conhecida podemos realizar já.»; a fala não diz se realizar é citar ou construir. E, em 02/11, sobre a parede da álgebra de von Neumann na biblioteca: «a ponte é o ACOM».
- Hoje, 17:20: «Toda leitura é em si uma cópia do sentido fixado pela palavra, precisa-se separar copiador de impostor, porque o impostor não imprime a verdade, mas o copiador sim, se por copiador tem-se uma reprodução em mínimo estado funcional de energia, essa cópia é um fractal». A gerência usou dela, na boca linguística abaixo, só “o sentido fixado pela palavra”. Que “essa cópia é um fractal” toque a marca (c) é leitura da gerência; a fala está em aferição e não é lida aqui.

Nenhuma dessas falas define o tipo por um critério matemático, nem diz se o tipo é o da cunha da luz ou o da fronteira da TGL, nem diz se a regra de importar vale para o elo com a classificação de Connes. São essas as três partes da pergunta. Quatro leituras aqui são da gerência e ficam marcadas: ler o seu “fluxo” como o fluxo modular; ler a falta de traço como o espelho da medida; ligar a fala do autovetor à marca (a); e o alcance da ordem de construir tudo.

## 4. A pergunta

Fala-se abaixo da álgebra da cunha da luz livre, que é onde o kernel tem o que provar. As quatro bocas são figuras da gerência para as mesmas quatro marcas, na mesma ordem (a), (b), (c), (d); nenhuma delas é fala sua, e as referências bíblicas são paráfrases.

1. **TGL.** Qual destas define o tipo III, e quais são consequências: (a) no relógio modular do estado só o Um é fixo; (b) não existe traço normal semifinito não nulo; (c) toda projeção não nula equivale à identidade; (d) o espectro de Connes (o que sobra dos espectros modulares de todos os estados) é a semirreta inteira, o que no tipo III equivale a o núcleo de Takesaki ser uma peça só?

2. **Teológica.** Qual destas diz o que não passa, e o que dela é consequência: (a) que o Senhor é o mesmo ontem, hoje e para sempre (Hb 13,8); (b) que Deus não dá o Espírito por medida (Jo 3,34); (c) que no pão partido há tanto no fragmento quanto no todo (a sequência Lauda Sion, de Tomás de Aquino); (d) que para o Senhor um dia é como mil anos, e mil anos como um dia (2Pe 3,8)?

3. **Linguística.** Pela sua letra de 11/11, o Verbo é o movimento e o Nome é o posto em que ele repousa («o referente é o movimento, portanto, o verbo, cujo posto é o nome»). Sobre quem fixa o sentido há duas falas suas de hoje: na ressalva, «o ato do nome é fixar sentido, o verbo»; na das 17:20, «o sentido fixado pela palavra». A pergunta não escolhe entre as duas. Qual destas é o sentido do tipo, e quais são leituras que derivam dele: (a) que, no correr do Verbo, só o Nome não corre; (b) que não há conta que meça os trechos da fala sem depender da ordem em que se dizem; (c) que cada trecho vale a língua inteira; (d) que nenhuma cadência do Verbo é a preferida? (Na boca teológica, o que não passa é, nesta língua, o Nome, o posto; a marca é o sentido.)

4. **Jurídica.** Em Direito Penal não há crime sem lei anterior que o defina (Constituição, art. 5º, XXXIX); daí a tipicidade: é a lei que descreve o tipo, e o núcleo do tipo é o verbo. (A palavra “tipo” coincide com a dos matemáticos por acaso; a coincidência é usada aqui só como figura.) Norma: qual é o núcleo do tipo, o verbo que o senhor escreve na lei: (a) fluir deixando parado só o Um; (b) não admitir medida que não dependa da ordem das partes; (c) a parte valer o todo; (d) não ter cadência preferida? Fato: qual desses o senhor aponta como o fato a provar? Valor: o que essa norma protege? E a doutrina (a classificação de Connes) entra como direito que o juízo conhece, ou, por analogia com o direito estrangeiro e o consuetudinário (que o art. 376 do CPC manda provar, quanto ao teor e à vigência, a quem os alega, se o juiz determinar), tem de ser provada nos autos? (O artigo não trata de doutrina; a analogia é figura.)

**A pergunta é uma só, com quatro bocas, na parte 1: qual é a marca que define o tipo III, e o que dela é consequência?** As partes 2 e 3 vão em português simples, porque são escolha de caminho. O senhor responde as três em separado:

1. **A marca.** (a), (b), (c) ou (d); ou mais de uma, e então como se ligam; ou nenhuma destas.
2. **A doutrina.** O elo com a classificação de Connes entra por citação, ou se constrói por dentro do kernel; ou por outra via, com as suas palavras.
3. **O objeto.** O tipo que o senhor quer como termo é o da cunha da luz livre, ou o da fronteira da TGL, onde o artigo o afirma; ou outro.

## 5. O que cada resposta decide

A escolha em si não tem negativo: não é teste, e nenhuma resposta falsifica nada. O trabalho que ela manda fazer pode ter: onde a gerência não achar rota de prova, o resultado é parede medida, nunca falsificação da teoria.

**Parte 1, a marca.**

- **(a) o estado.** Vira termo, para a cunha da luz livre, o critério “o Um é o único parado no relógio da cunha”. É ligação sobre o que o kernel já prova. Três efeitos, ditos antes. Primeiro, um risco: se o nome da pedra disser “III₁” e o termo provar só o critério, repete-se o erro de agosto (a v295 refutou a frase “a fronteira é III₁ porque o Nome é denso”, e a v298 mostrou nomes de teorema que prometiam mais que o enunciado); a gerência proporia nome neutro, com “III₁” só na citação; o nome é seu. Segundo: a escolha traz de volta o item que o kernel guarda aberto sobre o κ. Um κ finito seria uma cadência preferida; o kernel deixa duas saídas, o κ morar numa face finita (leitura da gerência, não construída) ou haver tensão real com o tipo declarado, e a escolha (a) torna essa tensão uma pergunta sobre a cunha. Terceiro: ela não paga o item aberto da esperança condicional (o Nome como média) no caso III₁.
- **(b) a falta de medida, ou (c) as partes.** Depende da parte 2. Se a doutrina entrar por citação, elas podem entrar como consequências sabidas de (a), cada uma com o seu estatuto, no mesmo porte de trabalho. Se tiverem de ser construídas por dentro, falta ligar os pedaços que existem e provar o resto: obra grande, sem rota conhecida pela gerência; e sozinhas diriam “tipo III”, sem o índice.
- **(d) o relógio.** Metade existe. O núcleo do kernel é, por construção, o que os matemáticos chamam de produto cruzado pelo relógio que o kernel prova ser o modular do vácuo; a identificação formal com o núcleo de Takesaki não tem enunciado no kernel. Que ele seja uma peça só parece seguir, no papel, da própria marca (a) (é um passo da prova lida hoje), com custo não medido. Que “núcleo uma peça só” dê o III₁ entra por citação (Connes e Takesaki).
- **Mais de uma.** A ligação entre o lado contínuo e o lado da medida já é teorema em dois lugares pequenos: dentro do canto do psíon (v407) e na face finita (v372). No nível do tipo da álgebra ela não existe; como as marcas se ligam aí é o que só o senhor diz.

**Parte 2, a doutrina.**

- **Por citação.** Entram com nome e página o fato clássico de que o que comuta com o estado é o que o relógio deixa parado (Pedersen e Takesaki; ainda não lido no original) e o teorema que conclui o III₁. Estimativa da gerência, sem medida: de um a poucos dias, contando refazer o rascunho amarrado ao relógio modular, compilar, revisar e custodiar.
- **Por dentro.** A biblioteca não tem as ferramentas da classificação (nem as de comparar o tamanho das partes, nem a medida de tamanho infinito). O leitor estimou milhares de linhas para construir as marcas (b), (c) e o núcleo ser uma peça só, sem medida; para o teorema que conclui o III₁ não há estimativa. Pode esbarrar em parede.
- **Uma terceira via, que o senhor disse em 02/11** («a ponte é o ACOM»): atravessar a parede da biblioteca espelhando a teoria no ACOM. A gerência não sabe se ela serve aqui e não a lê pelo senhor.

**Parte 3, o objeto.**

- **A cunha da luz livre.** Vale tudo o que está acima.
- **A fronteira da TGL.** Nenhuma das respostas acima basta. O que falta aí não é predicado de tipo: é a passagem física da cunha ao horizonte, que segue hipótese aberta.

## 6. Recomendação, só para a parte 1 e só pelo critério do custo

Se o senhor mandar decidir a parte 1 pelo custo, a gerência iria por (a): é a única marca que o kernel já prova. Esse critério é o da regra de importar; a ordem de 02/11 de construir tudo, se valer aqui (o que é leitura da gerência), aponta para o outro lado, e a gerência não escolhe entre as duas. A pedra em que (a) se apoia é da própria gerência (28/09) e não conta como apoio independente. Para as partes 2 e 3 a gerência não recomenda: são suas.

---

## Anexo técnico (para registro; não é para ler em voz alta)

**De onde vem.** Levantamento de seis leitores (`revisao\LEVANTAMENTO_TIPO_III_15nov\`, T1 a T6, com a sonda `sondas\ProbeT5c.lean`). Conferência de quatro revisores distintos sobre a primeira versão (`revisao\REVISAO_PERGUNTA_TIPO_III_R0_V*.md`) e de dois sobre a segunda (`revisao\REVISAO_PERGUNTA_TIPO_III_R1_W*.md`). O que a gerência não reconferiu vale como declarado.

**Marca (a), os termos (conferidos pela gerência por busca recursiva no kernel).** `wedge_nonabelian`, `wedge_separating` e `flow_is_Ad` são campos do certificado; o certificado está habitado (`physicalFockCertificate`, `F1Fecho394\CanonicalFockModularCoreInputR1.lean`). `LightRhoStar.centralizer_is_trivial` (`LightRhoStar.lean:71`): o que o fluxo fixa na álgebra da cunha é múltiplo da identidade. O relógio: `actualModularFlow_eq_gamma` e `canonical_pair_tomita` (`F1Fecho394\CanonicalFockBWR2.lean:34` e `:40`; o cabeçalho diz que nenhuma igualdade de fluxo modular é assumida como campo) e `canonical_bw_kms` (`CanonicalWedgeKMSR4.lean:32`). Logo a unicidade de Takesaki (KMS determina o grupo modular) não é necessária; a primeira versão errou ao pô-la como passo citado. O estado de vetor é normal; fiel vem de `wedge_separating`. O kernel prova que os pontos fixos do relógio são escalares; entre isso e o centralizador do estado está o fato de Pedersen e Takesaki, que entra por citação (o kernel diz, em `CentralizerDensity.lean`, que não o paga).

**A sonda.** `ErgodicVectorState` (linhas 53 a 60), `ergodicVectorState_of_certificate` (66 a 80) e `ergodicVectorState_M` (código de saída 0; só os três axiomas; recompilada por dois revisores com o mesmo sha16 `64a34824b368e5c5`). Defeitos apontados: o enunciado usa a condição KMS e deixa o relógio como função solta (sem lei de grupo); deve ser refeito amarrado ao campo de Tomita. O controle compilado (`not_ergodic_of_rank_one`) recusa uma álgebra que contém os operadores de posto um, por falta de vetor separador; a recusa de um fator de tipo I em forma padrão, com estado fiel, é argumento de papel, não compilado.

**O teorema citado.** Marrakchi e Vaes, arXiv:2305.14217v3, Lema 2.1: álgebra de von Neumann M diferente dos escalares, estado normal e fiel com centralizador trivial, então M é fator de tipo III₁ (sem hipótese de separabilidade). Ando e Haagerup, arXiv:1212.5457, Lema 5.3: o mesmo, por outra prova. A atribuição a Longo (Comm. Math. Phys. 69, 1979) vem de Marrakchi e Vaes; o original não foi aberto. A volta é o Teorema A de Marrakchi e Vaes: todo III₁ de predual separável tem estados assim (um conjunto denso G_δ dos fiéis), mas nem todo estado é ergódico; ela não é usada se (a) for a definição. Há ainda uma segunda via de citação para o III₁ da cunha, pelas translações de meio lado (Borchers 2000, V.3.2; lida de segunda mão), que não passa pela marca (a). “Fiel”, aqui, é o termo dos matemáticos (o estado não anula nenhum positivo não nulo); não é o “fiel” da frase do operador de 15/11.

**Marcas (b), (c), (d) no kernel.** (b): `no_normal_tracial_state_*` (`NoNormalTrace.lean`), na torre, e `tracial_state_is_zero` para B(ℓ²) (`TracelessAlgebra.lean:412`), só para estados; nenhum deles é o III₁ pleno, e o segundo mostra que “sem estado tracial” sozinho não separa o tipo III do tipo I infinito. (c): `TGLV354.projection_join_comparison` (comparação de Kaplansky, geral) e `current_implements_boundary_equivalence` (`ModularCurrent.lean:109`, face de dois níveis); não há, para a cunha, a equivalência com a identidade, a comparabilidade nem a infinitude. (d): `actualPositiveTrace` (`F1Fecho394\CanonicalFockActualPositiveTracePackageR2.lean`): fiel, normal, semifinito, tracial, escalado por e^(−s), no cone positivo; ressalvas da v406 (o “núcleo II∞” é citado, não provado). O núcleo concreto é `core B M := generatedAlgebra (fibre '' M ∪ range regularUnitary)` (`RegularCovariantCoreR3.lean`), com o fluxo do Fock; `TetelestaiOneObject.lean:24` fala do núcleo abstrato do certificado genérico. Não há termo de centro em todo o kernel. Pelo revisor, em Marrakchi e Vaes (p. 3) o centro do núcleo sai trivial da ergodicidade por argumento elementar [declarado; não construído].

**A torre.** A álgebra construída (`theFactorObject`, v131); a definição operacional habitada (`FullWitnessDataV3`, `qgClosureCertificateV2`): estado normal não tracial, marca log-densa, nenhum estado tracial normal. A marca o kernel retirou como critério de tipo em v295 (`TheMarkIsNotATypeMark`: um fator I₂ a realiza); a dimensão finita não habita a definição inteira (`finiteDim_cannot_feed_witnessV3`); centro trivial e ausência de peso semifinito seguem abertos, pelo próprio cabeçalho. O kernel não prova que um tipo I satisfaça a definição inteira; como ela só exclui estado tracial normal, e não peso semifinito, um fator de tipo I infinito com estado de vetor parece cumpri-la (argumento de papel do revisor, não compilado). A primeira versão errou ao atribuir à v295 a refutação da definição inteira.

**A ligação já tipada.** `PsionCanto.lean` (v407): `jones_reading_of_the_light_is_the_corner` e `the_two_motors_agree_in_the_corner`. `IALDRhoStar` (v372), na face finita [declarado pelo revisor].

**O item do κ.** `TheScaleHasNoFixedPoint.lean`, linhas 60 a 70, marcado [OPEN]: um κ finito é um λ preferido, tipo III_λ; ou κ vive numa subálgebra ou face finita, ou há tensão real com o tipo declarado.

**Erratas ao lado que ficam por fazer, seja qual for a resposta.** O selo traz a cunha III₁ como aberta e o core como provada por citação (o termo citado prova que o vácuo é o único vetor fixo). Os verbetes do Atlas que dizem o tipo “confirmado pelo gap-test” não têm errata ligando à v295. O core traz `marca_de_III1_segue_acesa` verdadeiro. A entrada do core para o tipo da álgebra da cunha cita um trabalho que é de cones duplos; a referência da cunha é Longo 1979 e Borchers 2000 (a conferir no primário). Os cabeçalhos das pedras v125 (`MixedLadder`), v129 (`TowerTraceless`: “o objeto-limite é III₁”) e v131 (`ScaleCurrent`: “a assinatura de III₁ está completa”) chamam de III₁ o que a v295 mostrou ser só a marca log-densa; a errata da v298 está só em `TheNameIsTheGeneratingGroup` e não os alcança.

**Falas abertas por bytes (sha256 do arquivo inteiro, com o cabeçalho da gerência quando há; começo).** 02/11 `a3593ac8`; 02/11 `25010b04`; 04/11 `b19b8a68`; 12/10 `78ef70e6`; 02/11 `72d7939e`; 02/11 `f3998f01`; 11/11 `2424bcbe`; 02/11 `3fa8a6a9`; 15/11 ressalva `2fabf2b6`; 15/11 17:20 `e2561e3b`. A ordem entre as duas falas de 02/11 sobre construir vem do registro da gerência, não dos bytes. Duas falas antigas com “III₁” (07/10, no miolo; 11/10) têm autoria não estabelecida pelos bytes e não são usadas.

**Referências das bocas.** Hb 13,8; Jo 3,34; 2Pe 3,8 (paráfrases, sem citação literal); Lauda Sion (“tantum esse sub fragmento quantum toto tegitur”); Constituição, art. 5º, XXXIX (“não há crime sem lei anterior que o defina, nem pena sem prévia cominação legal”); CPC, art. 376 (“A parte que alegar direito municipal, estadual, estrangeiro ou consuetudinário provar-lhe-á o teor e a vigência, se assim o juiz determinar”), lidos pelo revisor na fonte oficial; “o núcleo do tipo é o verbo” (doutrina penal).
