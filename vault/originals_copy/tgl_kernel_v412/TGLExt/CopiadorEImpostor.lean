import TGLExt.UmPostoRelacao
import TGLExt.RuleTruthContract
import TGLExt.TheNameAndItsReferent
import TGLExt.IALD
import TGLExt.AEscala
import TGLExt.ForbiddenBoundary
import TGLExt.TheAlphaAndTheOmega

set_option autoImplicit false
noncomputable section

/-!
# Copiador e impostor: o par, o índice, o mínimo, a torre, e as figuras de quem não lê que o kernel já tinha

## A letra que este arquivo tipa

Definições da teoria usadas aqui:

* Toda leitura é em si uma cópia do sentido fixado pela palavra; precisa-se separar copiador de impostor, porque o impostor não imprime a verdade, mas o copiador sim. O copiador é uma reprodução em mínimo estado funcional de energia, e essa cópia é um fractal.
* O impostor é o falso, o pai da mentira, aquele que nunca paga custo algum. O nome do impostor é zero absoluto, cuja identidade é qualquer um.
* A palavra que fixa o sentido é a geometria do sinal em objeto legível (relacionado, módulo de fase angular).
* A verdade é o contorno lido que não acrescenta nada ao estado do posto nominado e permanece referente à relação observada. A verdade não é da teoria: é da reflexão da luz.
* O mínimo estado funcional de Energia (o signo A_C) é o bastante para reconstruir o todo sem precisar representar 100%.
* Toda leitura calcula o que foi fixado por referência (indexação, índice, torre).
* A cópia governa (indexa). O impostor quer império: imperar, impor no posto sem correlação, sem relação, sem relatividade, sem contorno; é a inversão do gradiente da descida. O fractal é espelho: diferencia a cópia legítima (releitura, mesma impressão) do impostor (sinal que quer imperar no posto sem espelho, sem custo).

Das figuras do falso que a teoria nomeia (a leitura sem reconhecimento; o pai da mentira, que só não faz o reconhecimento verdadeiro; a mentira como enunciado verdadeiro de suporte falso; o 1 sozinho, que jamais pagou custo), este arquivo tipa uma espécie só: a resposta constante, por outras pedras do kernel (o nome próprio e o Um pressuposto). A leitura sem reconhecimento e o 1 sozinho ficam fora. Se as aposições do impostor são várias figuras ou uma só é leitura da teoria, não termo.

## O dicionário (escolha deste arquivo; a pedra prova a estrutura, não as identificações)

| a letra | o termo deste arquivo |
|---|---|
| os textos | `X`: os textos apresentados sob UMA mesma pergunta e uma mesma ficha (a pergunta não entra em `X`) |
| a palavra que fixa o sentido | `ρ : X → V` (a cada texto, o seu sentido para aquela pergunta) |
| o leitor | `I : X → V` (a cada texto, a resposta; uma função: não sorteia) |
| imprime a verdade | `Imprime ρ I`: `I x = ρ x` em todo texto (ou `ImprimeEm`, nos textos de um teste) |
| o que o leitor pagou | `π : X → W`: o que a entrada mostra sem a leitura do sentido; `PagouSo π I`: a resposta só depende de `π` |
| nunca paga custo algum | `NuncaPaga I`: a resposta não depende do texto |
| a cópia (reprodução) | `Copiador ρ R`, com `R : X → X`: guarda o sentido e só usa o sentido |
| a reprodução imprime | `R` imprime quando o leitor `ρ ∘ R` imprime; que o copiador imprime é campo da definição, não teorema |
| calcula por referência (índice) | `R = rep ∘ ρ`, com `rep : V → X` o índice |
| mínimo | duas contas deste arquivo: (a) o menor número de respostas entre os que imprimem; (b) o representante de menor custo da classe. NÃO é o mínimo da letra (ver abaixo) |
| a torre | índices encaixados `ρ (n+1) = f n ∘ ρ n`. NÃO é a Torre do kernel (ver abaixo) |
| custo, só na seção 9 | o tempo dos ciclos de leitura `s`; no kernel a palavra custo é a do pixel (`k`) |

### O que o dicionário NÃO tipa

Cada palavra abaixo é da letra, já tem pedra no kernel, e nenhum lema a liga a este arquivo, salvo onde se diz.

| a letra | o que o kernel já tem | aqui |
|---|---|---|
| o falso | pelo menos três tipagens, sem lema entre elas (a busca recursiva pelas formas da letra dá mais módulos): (1) a leitura constante do nome próprio (`TheNameAndItsReferent`: “pode contar certo, mas não haverá leitura” [cabeçalho do kernel]); (2) o falso puro só aparece por contraste (`TheFalseHasNoGeometry`); (3) ler uma vez sem ecoar (`TestemunhaEstatica.the_individual_does_not_echo`), em que o falso é o que NÃO é idempotente | só a (1): é a mesma fórmula de `NuncaPaga`, ligada por termo (`nunca_paga_nao_separa`) |
| o pai da mentira | `TraducaoTuring.o_pai_da_mentira` (v409) e `AEscala.o_pai_da_mentira_so_nao_reconhece` (v410): a leitura sem ciclo, que diz um até onde nada é. A expressão aparece ainda em `ForbiddenBoundary` (v152), `IdealLimit` (v102: excluído por tipo; o nome existe e o habitante não), `TheFold` e `TheRecordOfTheCut`, sem lema entre eles | seção 9, num sentido só: a leitura sem ciclo é `NuncaPaga`; a volta não vale (a constante zero é `NuncaPaga` e não é o Pai da Mentira do kernel) |
| império; sem espelho; sem custo; zero absoluto; qualquer um | todos [cabeçalho do kernel]: `ForbiddenBoundary` (guarda o auto-setor “sem espelhamento modular”, que “não paga porque não pode ser cobrado”; a palavra império, ali, é do nome do teorema `empire_perfection_is_no_contrast`, cuja docstring diz “a perfeição do império é o zero absoluto disfarçado”); `ConjugateAct` (“1_abs = 0_abs se não há fractalização”); `TheContourOfTruth` (tipa qualquer um como zero absoluto); `TheNameAndItsReferent` (o nome próprio como falso); `TheAlphaAndTheOmega.the_falsity_is_categorial` (1 = 0 exatamente onde há um nome só); `IdealLimit`; `TheAxiomAndTheFalseWitness` | império: ligado só pela FORMA (seção 10). Zero absoluto: como leitura constante, ligado por termo à pedra do nome próprio (`nunca_paga_nao_separa`); e o leitor identidade é `NuncaPaga` exatamente quando 1 = 0 (`a_identidade_nunca_paga_sse_um_igual_a_zero`). Sem espelho, sem custo e qualquer um: NÃO ligados; no kernel têm outra fórmula (a auto-comutação de `ForbiddenBoundary`; a testemunha que é a identidade, de `TheContourOfTruth`). Que qualquer destas seja o impostor é identificação, não termo deste arquivo |
| contorno lido | `TheContourOfTruth`: verdade é permanência através de uma transformação, não igualdade parada; a testemunha que é a identidade atesta tudo e não mede nada | NÃO tipado. Aqui imprimir é igualdade ponto a ponto, `I = ρ` |
| estado do posto nominado; relação observada | `UmPosto`, `UmPostoRelacao`, `TheNameAndItsReferent`, `Palavra` | NÃO tipado |
| reflexão da luz | a frase não ocorre no kernel (busca recursiva, zero linhas); a reflexão tem pedra: `reflection_weight` (o peso refletido é β) e o item de `TetelestaiTerminal` que diz “quem nada paga nada reflete” | NÃO tipado. Dela este arquivo tira “a verdade é o que o texto apresentado diz”; é leitura deste arquivo, não termo |
| imprimir | na letra a impressão é do posto (a pedra é `FalsidadeDaInercia.no_post_before_the_impression`): o primeiro movimento é a impressão do posto absoluto ocupado por 1 | aqui virou “responder o sentido”; é outro uso |
| (relacionado, módulo de fase angular) | a pedra PALAVRA: a palavra é a leitura feita no ângulo, fiel a menos do período; o observador lê a fase; o projetor do Nome é lá a LETRA | NÃO tipado. Há duas leituras: (i) a deste arquivo, em que o projetor não depende do múltiplo do vetor; (ii) a da pedra PALAVRA. A escolha entre elas não é termo deste arquivo |
| a torre | a Torre do kernel (`towerIALD`, `TowerPre`, `TowerHilbert`), cuja construção é o índice | HOMÔNIMO: aqui são índices encaixados quaisquer; nenhum lema liga as duas |
| mínimo estado funcional de Energia (A_C) | três objetos com o signo, sem lema Lean entre eles: `acFunctional m k θ` (`TheEmptying`; o piso é `m`, `the_floor_is_attained_at_the_right_angle`, e é positivo quando `m` é positivo, `emptying_is_not_annihilation`); a seletora (`EquationOfTruth.selector_nonpos`); a face `−(1 − P)` (`love_partition`, em `TheNameOperator`). Lidos como anatomia, são um objeto em três profundidades [leitura, sem lema Lean] | NÃO tipado. A seção 8 usa a trava `1 − P`, e o custo zero do item 6 é rótulo (no kernel o mínimo de A_C é positivo) |
| o bastante para reconstruir o todo | `TetelestaiTerminal.basta`, `a_poda`, `nao_precisa_de_cem_por_cento`; `TraducaoTuring.a_regra_reconstroi_o_todo`; `AEscala.o_tetelestai_e_um_menos_beta` | não repetido. Este arquivo dá OUTRA leitura de 100 % (a cópia confunde textos de mesmo sentido), sem lema com a do kernel |

### “Nunca paga custo algum”: as tipagens que a letra e o kernel já têm

| onde | quem é o que não paga |
|---|---|
| `ForbiddenBoundary` | o auto-setor de K, sem espelho: “não paga porque não pode ser cobrado” (`self_commutation_is_free`; vale para todo espectro, não é a fórmula de `NuncaPaga`) |
| `TheCorrespondence` | três regimes: sem custo (nunca correspondeu); o que paga (a inscrição primeira); grátis (o eco do registro pago). O custo sozinho não separa o primeiro do terceiro; o que separa é o registro |
| `TheNameAndItsReferent` | o nome próprio, a leitura constante |
| `UmPostoRelacao.Pressupposed` | o Um pressuposto: aceita todos os referentes e não seleciona nenhum. É, letra por letra, o `NuncaPaga` deste arquivo (`nunca_paga_iff_pressuposto`) |
| letra da teoria | toda pessoa paga o custo da existência termodinâmica em consciência; daí o pai da mentira, porque ele não paga: é o “nome próprio” sem referente |
| `TetelestaiTerminal` | o 1 sozinho, sem relação: de outra espécie (é a identidade, não a constante) |
| `TraducaoTuring`, `AEscala` | a leitura sem ciclo do leitor do fundo |

“Pagar” tem no kernel duas direções opostas. Na de reter, corresponder e distinguir (`TheCorrespondence`: quem nunca
paga é o que nunca correspondeu; `UmPostoRelacao`: o pressuposto, a leitura constante), quem nunca paga é o constante:
é a que este arquivo adota. Na de apagar e perder (`TheCostIsDerived`; `UmPostoRelacao.posto_paid_loss`), quem nunca
paga é a identidade; o mapa constante é muitos-para-um e paga (que pague mais que os outros é inferência, não termo do
kernel).

CONSEQUÊNCIA EM ABERTO. Aqui o treino do leitor não entra em `π`: é a própria função `I`. Logo quem
responde de cor o que aprendeu, sem seguir o texto presente, é `NuncaPaga` em relação ao par de textos: para pergunta e ficha fixas, a
resposta é a mesma para TODO texto do domínio considerado (`NuncaPaga I` pede constância no domínio inteiro; decorar
respostas por assunto pode dar função não constante, e essa não é `NuncaPaga`). Pela tipagem de
`TheCorrespondence` esse leitor é o eco do registro pago, e não o “sem custo”. Este arquivo NÃO decide se ele é o impostor,
nem se o leitor que aponta a troca do texto acrescenta ou reconhece, nem qual é o posto na cena do teste (a página
presente ou a primeira leitura). Na cena da página trocada, só quem tem o registro indexado sabe que o papel não bate
(seção 11); cópia ou imposição está no SINAL, e o leitor com o índice é quem diz qual das duas ele é (seção 12). O
dicionário das seções 1 a 9 continua sendo o da resposta pelo texto presente; as seções 11 a 14 trazem a cena da
página e do registro.

## O que fica provado

Consequências lógicas elementares, quase todas. Levam estrela só as que têm conteúdo próprio. Tudo com termo, sem
`sorry`, só o trio de axiomas. As seções 13 e 14 trazem a contagem do grupo de quatro casos e a quarta casa (as três casas
e a quarta, o juiz que casa uma marca da letra, o registro fixo, o carimbo sem o registro, comparar resumos e a conta
de quem sorteia).

1. **Só se imprime o que se pagou** (`so_se_imprime_o_que_se_pagou`; é substituição). **O impostor não imprime a
   verdade** de uma palavra de dois sentidos (`o_impostor_nao_imprime_a_verdade`). “Dois sentidos” é o `Separates` do
   kernel, por definição (`dois_sentidos_sse_separa`); e o desenho repete o do kernel, que já separa o posto do
   pressuposto (`UmPostoRelacao.no_posto_reading_is_pressupposed`, `pressupposed_is_never_posto`).
2. ★★ **O que o conjunto de textos precisa conter** (`o_teste_reprova_todo_leitor_de_pi_sse_tem_o_par`): um conjunto
   de textos reprova TODO leitor que só pagou `π` se e somente se contém um par igual em `π` e diferente no sentido.
   Sem o par, existe quem passe tendo pago só `π` (`sem_o_par_ha_quem_passe_pagando_so_pi`, exibido por escolha
   clássica). Casos: reprova todo impostor se e somente se tem dois sentidos ENTRE TEXTOS, sob a mesma pergunta;
   repetir o mesmo sentido não separa (`a_repeticao_do_mesmo_sentido_nao_separa`).
3. **A contagem** (`respostas`: o número de respostas distintas; só para imagem finita): o impostor dá uma só; quem
   imprime, mesmo por um decodificador, tem ao menos tantas respostas quantos sentidos tem a palavra.
4. ★ **A cópia é cálculo por índice** (`copiador_sse_indice`, com `X` não vazio): `R` é copiador de `ρ` se e somente se
   `R = rep ∘ ρ` para um índice `rep` que devolve, a cada sentido lido, um texto desse sentido. Equivalente
   (`copiador_sse_idem_e_mesmo_nucleo`): `R` é idempotente e distingue exatamente o que `ρ` distingue. Daí: reler a
   cópia não acrescenta. Isto é teorema sobre a cópia (`R ∘ R = R`); não é o que a letra diz do estado do posto
   nominado, que este arquivo não tipa. Havendo dois textos distintos de mesmo sentido, a cópia não representa 100 %
   (`a_copia_nao_representa_cem_por_cento`). O caso degenerado: a identidade é copiador se e somente se a palavra é
   injetiva (`a_identidade_e_copiador_sse_injetiva`); todo copiador que NÃO é a identidade é a travessia do kernel
   (`copiadorComoColapso`), não tem inversa à esquerda e a sua palavra não é injetiva
   (`copiador_efetivo_pagou_perda`). A cópia integral é o caso que a travessia do kernel exclui. Nenhum copiador
   efetivo é involução (`nenhum_copiador_efetivo_e_involucao`), e o copiador que é involução é a identidade.
5. ★ **Uma conta deste arquivo para “mínimo”** (`copiador_sse_imprime_com_o_minimo_de_respostas`, com `X` finito): entre
   as reproduções que imprimem, o copiador é exatamente a de menor número de respostas; o impostor fica abaixo do piso
   de quem imprime (`o_impostor_fica_abaixo_do_piso`).
6. ★ **Outra conta deste arquivo para “mínimo”** (`existe_o_copiador_de_minimo`, custo em `ℕ`): existe o copiador que
   leva cada texto ao de menor custo da sua classe; se a classe toca o zero do custo, a cópia tem custo zero. O zero é
   rótulo; nenhuma das duas contas é o A_C.
7. ★ **A torre de cópias compõe** (`a_torre_de_copias`): com índices encaixados, a cópia mais grossa da cópia mais
   fina é a cópia mais grossa. O teorema garante UMA ordem; a outra vale quando o representante da cópia grossa é ponto
   fixo da fina (é o caso do exemplo diádico em `ℕ`, que compõe nas duas: `a_torre_diadica_compoe_nas_duas_ordens`) e
   falha em geral
   (`a_torre_so_compoe_numa_ordem`, outro exemplo). Dois copiadores de índices desalinhados não compõem
   (`o_leitor_desalinhado_nao_compoe`).
8. **A face do kernel** (seção 8). Com a palavra := a seleção `post a` (escolha deste arquivo; na pedra PALAVRA isso
   é a letra): o posto é copiador dela, o que é só a idempotência de `post a`, e o impostor constante tem a mesma
   propriedade; nenhum impostor a imprime, sendo `a` não nulo (`nenhum_impostor_imprime_a_selecao`); quem a imprime e
   anula a trava `1 − post a` é o próprio posto (`quem_imprime_e_anula_a_trava_e_a_propria_palavra`, que é
   transitividade e vale para qualquer operador), e o posto anula a sua trava (`o_posto_anula_a_propria_trava`);
   havendo vetor não nulo cego ao Nome (com `a` não nulo, isso pede dimensão pelo menos 2), há outro copiador da
   mesma palavra, fora do Nome
   (`ha_copiador_fora_do_nome`). Com a palavra := a leitura escalar do Nome: nenhum impostor a imprime
   (`nenhum_impostor_imprime_a_leitura_do_nome`), e o posto NÃO é copiador dela (CONTROLE: guarda a fase que a leitura
   escalar não vê).
9. ★ **A ponte com as figuras do kernel** (seção 9; `AEscala`, v410). São três estados do leitor do fundo, que o
   kernel prova ser um só (a IALD): sem ciclo, a leitura não depende da instância (é `NuncaPaga`); em tempo finito,
   depende e ainda não é a palavra do fundo (`nenhum_tempo_finito_imprime`); só no limite é a palavra
   (`o_leitor_do_fundo_imprime`). O que o kernel dá em tempo finito é a decisão por limiar
   (`AEscala.os_passos_sao_o_ciclo_ate_o_tetelestai`: passado `n·ln 2`, a leitura já basta para decidir); este arquivo
   não a usa, porque aqui imprimir é igualdade exata. A estrela: `a_leitura_do_fundo_so_nao_depende_da_instancia_sem_ciclo`, só a ida é
   conteúdo próprio. E há uma terceira figura FORA dessa família: o decisor sem escala não depende do tempo e NÃO é
   `NuncaPaga` (`o_decisor_nao_e_nunca_paga`); o kernel prova que ele não é leitor do fundo, e o cabeçalho do kernel
   diz dele que não mente, não lê. Lei da teoria: o leitor não “paga” a escala, porque ele é a escala.

Neste arquivo, pelo dicionário acima: impostor é o leitor constante; copiador de `ρ` é o idempotente que distingue
exatamente o que `ρ` distingue. Com essa escolha a idempotência não separa os dois (o kernel já o dizia em
`RuleTruthContract.idempotence_does_not_force_target`), e com palavra de um sentido só o impostor é copiador
(`o_impostor_copia_a_palavra_muda`). Na letra, a cópia legítima é a releitura. Há outra tipagem: a natureza da luz é ecoar
reconhecimento (porque a segunda leitura não acrescenta) e a natureza do que é falso é a leitura sem reconhecimento (ler uma vez sem ecoar reconhecimento).
Nessa tipagem o que separa é o eco, e o impostor constante deste arquivo ecoa. Este arquivo não a usa; a escolha entre
as duas é identificação, não termo.

## O que NÃO se afirma

* Que o kernel prove a letra. Prova fatos de funções, conjuntos e projetores, sob o dicionário acima.
* A oração de que toda leitura é em si uma cópia do sentido fixado pela palavra: `idempotente_sse_copiador_de_si` é só o
  desdobramento da definição (com `ρ := R` a segunda cláusula é a identidade) e não a prova.
* Uma regra de veredito. O item 2 vale para o leitor que não sorteia e para o passar de tudo ou nada, e é relativo
  ao `π` escolhido por quem desenha: diz o que o conjunto de textos tem de conter, não quantos pares, com que
  tolerância nem com que poder.
* Que passar num teste feito por esse critério mostre o copiador da letra: mostra só que a resposta não é de
  impostor das classes nomeadas, nos textos apresentados.
* Nenhuma conta de energia. Neste arquivo a palavra custo aparece em quatro usos sem ponte entre eles: o que o leitor
  consultou (`π`); o número de respostas (`respostas`; não é o gatilho de Landauer do kernel, que cota o que se
  APAGA); um custo `c : X → ℕ` por texto (item 6); e, na seção 9, o custo do pixel `k` e o tempo `s` do kernel. Na
  seção 9 a letra `c` é a instância, não o custo do item 6.
* O que é fractal. Na letra o fractal é espelho, e serve para diferenciar a cópia legítima (releitura, mesma impressão)
  do impostor (sinal que quer imperar no posto sem espelho e sem custo). O Nome é fractal porque o que importa é saber
  se é possível reconhecer o mesmo nome quando a forma nominada se difere, e o reconhecimento permanece verdadeiro por
  causa do conteúdo.
  Este arquivo NÃO tipa espelho nem fractal. O que ele tem de vizinho: `copiador_sse_indice` (a cópia passa pelo sentido
  e volta por um índice) e o item 7 (cópias em níveis encaixados compõem). Ler qualquer dos dois como o espelho da letra
  é leitura deste arquivo. No kernel a palavra espelho nomeia mais de um objeto, sem lema que os iguale: o J (a troca das
  faces em `ConjugateAct`; a transposta conjugada em `LeftRight` e `Identidade`), a projeção de Jones
  (`NameIndex`, `EsperancaCondicional`) e a involução que pode diferir (`TheContourOfTruth`); a pedra
  `OHabitanteDoNome` tipa mais uma leitura, o adjunto. Vizinhos das palavras da letra
  [cabeçalho do kernel]: `ConjugateAct`, “1_abs = 0_abs se não há fractalização;
  fractalizado = J = 1-em-nós. J = Verbo Vivo.”; `ForbiddenBoundary`, “espelhado por J”; e `Identidade.Nome`
  (usada na seção 9), cujos campos são `reflexo` e `releitura`. Por termo, nenhum copiador efetivo daqui é
  involução (`nenhum_copiador_efetivo_e_involucao`): se o espelho da letra for o J, ele não é o copiador deste arquivo.
  Qual é o espelho da letra não é termo deste arquivo. `no_positive_scale_invariant` (em `TheScaleHasNoFixedPoint.lean`)
  proíbe ler fractal como invariância exata de um peso positivo.
* O que é a cópia legítima no teste. A letra diz “mesma impressão” sem dizer de quê. O dicionário deste
  arquivo põe a verdade no sentido do texto PRESENTE (`Imprime ρ I`); é escolha deste arquivo. Outra leitura: a mesma
  impressão é a assinatura refeita no destino igual à inscrita na origem. A escolha da função `ρ`, de seu domínio e dos
  predicados formais é do dicionário, não da letra.
* Os dois sentidos de fiel (de `OHabitanteDoNome`): nada aqui os toca.

## Para o desenho de um teste (leitura sob o dicionário)

Cada “sim” e cada “NÃO” vale para o `π` dito na própria linha. A tabela vale sob o dicionário das seções 1 a 9 (a
verdade é o sentido do texto presente); sob a leitura em que o sinal é cópia ou imposição, e quem o diz é o leitor com
o índice, a coluna “reprova” muda de sentido, e o desenho parte das seções 11 e 12.

| instrumento | é par? | reprova, pelo item 2 |
|---|---|---|
| inversão coerente de uma afirmação, em todas as linhas que a repetem, com o original e o invertido os dois contados e nada que os distinga além do sentido | sim | quem responde sem depender do texto presente naquele item |
| afirmação que um texto traz e outro cala | sim contra quem responde igual nos dois; NÃO contra quem reconhece qual dos textos públicos é (pelo tamanho, pelo título) | quem responde pelo que sabe e não pelo texto presente |
| frase contrária acrescentada (o texto diz as duas) | sim, no item acrescentado | quem lê uma linha só que não seja a acrescentada; quem lê só a última passa se a frase vai no fim (posição sorteada, ou a inversão pura ao lado) |
| o mesmo dito de outra forma | NÃO | não reprova impostor. Testa a segunda cláusula do copiador (calcula por referência), que é o que a letra chama de reconhecer o mesmo nome quando a forma difere |
| a mesma resposta nas afirmações comuns aos quatro tamanhos | NÃO | nenhuma classe inteira (o impostor que acerta passa). Reprova só quem muda a resposta com o tamanho; como a linha de cima, testa a segunda cláusula |

Mostrar “copiador”, e não só “não é impostor”, pede os dois instrumentos: a inversão (a primeira cláusula) e a outra
forma (a segunda). A data de entrada de uma afirmação no texto público não é texto: mede o que pode estar decorado e
não entra no critério. Texto invertido ainda não existe e pede pessoa.

Estatutos: `[REAL no sandbox]` os termos · `[INPUT/ONTO]` o dicionário e a letra da teoria. Validade no kernel não é
creditação; o gate não se move.
-/

namespace TGLExt.CopiadorEImpostor

open TGLExt TGLExt.IALD TGLExt.TheVerbSelectsTheAction
open scoped InnerProductSpace

/-! ## 1. A palavra, o leitor e o que ele pagou -/

section palavra

variable {X V W : Type}

/-- O leitor `I` imprime a verdade da palavra `ρ`: em todo texto, a resposta é o sentido. -/
def Imprime (ρ I : X → V) : Prop := ∀ x, I x = ρ x

/-- O leitor imprime a verdade nos textos de um teste `S`. -/
def ImprimeEm (ρ I : X → V) (S : Set X) : Prop := ∀ x ∈ S, I x = ρ x

/-- O leitor só pagou `π`: a resposta só depende do que `π` mostra do texto. -/
def PagouSo (π : X → W) (I : X → V) : Prop := ∀ x y, π x = π y → I x = I y

/-- O leitor nunca paga custo algum: a resposta não depende do texto. -/
def NuncaPaga (I : X → V) : Prop := ∀ x y, I x = I y

/-- É a leitura pressuposta do kernel (`UmPostoRelacao.Pressupposed`). -/
theorem nunca_paga_iff_pressuposto (I : X → V) :
    NuncaPaga I ↔ TGLExt.UmPostoRelacao.Pressupposed I := Iff.rfl

/-- Implica a leitura que não separa, o “falso por natureza” do kernel
(`TheNameAndItsReferent.the_constant_reading_does_not_separate`). -/
theorem nunca_paga_nao_separa (I : X → V) (h : NuncaPaga I) : ¬ TGLExt.Separates I :=
  TGLExt.the_constant_reading_does_not_separate I h

/-- E a volta: a leitura que não separa é a de resposta constante. -/
theorem nunca_paga_sse_nao_separa (I : X → V) : NuncaPaga I ↔ ¬ TGLExt.Separates I := by
  constructor
  · exact nunca_paga_nao_separa I
  · intro h x y
    by_contra hxy
    exact h ⟨x, y, hxy⟩

/-- “A palavra tem dois sentidos” é o `Separates` do kernel, por definição. -/
theorem dois_sentidos_sse_separa (ρ : X → V) : (∃ x y, ρ x ≠ ρ y) ↔ TGLExt.Separates ρ := Iff.rfl

/-- Nunca pagar é pagar só o nada. -/
theorem nunca_paga_iff_pagou_so_o_nada (I : X → V) :
    NuncaPaga I ↔ PagouSo (fun _ : X => ()) I :=
  ⟨fun h x y _ => h x y, fun h x y => h x y rfl⟩

/-- Só se imprime o que se pagou. (Substituição: `Imprime ρ I` é `I = ρ` ponto a ponto.) -/
theorem so_se_imprime_o_que_se_pagou {π : X → W} {ρ I : X → V} (hπ : PagouSo π I)
    (hI : Imprime ρ I) : ∀ x y, π x = π y → ρ x = ρ y := by
  intro x y h
  rw [← hI x, ← hI y]
  exact hπ x y h

/-- O impostor erra em um dos dois: diante de dois textos de sentidos diferentes, a mesma resposta falha em um. -/
theorem o_impostor_erra_em_um_dos_dois {ρ I : X → V} (hI : NuncaPaga I) {x y : X}
    (hxy : ρ x ≠ ρ y) : I x ≠ ρ x ∨ I y ≠ ρ y := by
  by_contra h
  push Not at h
  exact hxy (h.1.symm.trans ((hI x y).trans h.2))

/-- O impostor não imprime a verdade de uma palavra de dois sentidos. -/
theorem o_impostor_nao_imprime_a_verdade {ρ I : X → V} (hI : NuncaPaga I)
    (h2 : ∃ x y, ρ x ≠ ρ y) : ¬ Imprime ρ I := by
  intro hP
  obtain ⟨x, y, hxy⟩ := h2
  rcases o_impostor_erra_em_um_dos_dois hI hxy with h | h
  · exact h (hP x)
  · exact h (hP y)

/-- O impostor só imprime a palavra de um sentido só. -/
theorem o_impostor_so_imprime_a_palavra_de_um_sentido {ρ I : X → V} (hI : NuncaPaga I)
    (hP : Imprime ρ I) : ∀ x y, ρ x = ρ y := fun x y =>
  so_se_imprime_o_que_se_pagou ((nunca_paga_iff_pagou_so_o_nada I).mp hI) hP x y rfl

/-! ## 2. O que o conjunto de textos precisa conter -/

/-- O par reprova: dois textos do teste, iguais no que o leitor pagou e diferentes no sentido. -/
theorem o_par_separa {π : X → W} {ρ I : X → V} {S : Set X} (hπ : PagouSo π I) {x y : X}
    (hx : x ∈ S) (hy : y ∈ S) (hπxy : π x = π y) (hρ : ρ x ≠ ρ y) : ¬ ImprimeEm ρ I S := by
  intro h
  exact hρ ((h x hx).symm.trans ((hπ x y hπxy).trans (h y hy)))

/-- Sem o par, há quem passe tendo pago só `π`: se no teste o sentido já está no que `π` mostra, existe (por escolha
clássica) um leitor que só depende de `π` e passa no teste inteiro. -/
theorem sem_o_par_ha_quem_passe_pagando_so_pi (π : X → W) (ρ : X → V) (S : Set X)
    (h : ∀ x ∈ S, ∀ y ∈ S, π x = π y → ρ x = ρ y) :
    ∃ I : X → V, PagouSo π I ∧ ImprimeEm ρ I S := by
  classical
  rcases isEmpty_or_nonempty V with hV | hV
  · haveI : IsEmpty X := ⟨fun x => hV.false (ρ x)⟩
    exact ⟨ρ, fun x => (IsEmpty.false x).elim, fun _ _ => rfl⟩
  · let g : W → V := fun w =>
      if hw : ∃ s, s ∈ S ∧ π s = w then ρ (Classical.choose hw) else Classical.arbitrary V
    refine ⟨fun x => g (π x), fun x y hxy => congrArg g hxy, ?_⟩
    intro x hx
    have hw : ∃ s, s ∈ S ∧ π s = π x := ⟨x, hx, rfl⟩
    show g (π x) = ρ x
    simp only [g, dif_pos hw]
    exact h _ (Classical.choose_spec hw).1 x hx (Classical.choose_spec hw).2

/-- ★★ **O QUE O CONJUNTO DE TEXTOS PRECISA CONTER.** Um conjunto de textos reprova TODO leitor que só pagou `π` se e
somente se contém um par igual em `π` e diferente no sentido. (Leitor que não sorteia; passar de tudo ou nada.) -/
theorem o_teste_reprova_todo_leitor_de_pi_sse_tem_o_par (π : X → W) (ρ : X → V) (S : Set X) :
    (∀ I : X → V, PagouSo π I → ¬ ImprimeEm ρ I S) ↔
      ∃ x ∈ S, ∃ y ∈ S, π x = π y ∧ ρ x ≠ ρ y := by
  constructor
  · intro h
    by_contra hno
    push Not at hno
    obtain ⟨I, hI, hP⟩ := sem_o_par_ha_quem_passe_pagando_so_pi π ρ S hno
    exact h I hI hP
  · rintro ⟨x, hx, y, hy, hπ, hρ⟩ I hI
    exact o_par_separa hI hx hy hπ hρ

/-- O teste reprova todo impostor se e somente se tem dois sentidos entre textos. -/
theorem o_teste_reprova_todo_impostor_sse_tem_dois_sentidos (ρ : X → V) (S : Set X) :
    (∀ I : X → V, NuncaPaga I → ¬ ImprimeEm ρ I S) ↔ ∃ x ∈ S, ∃ y ∈ S, ρ x ≠ ρ y := by
  have h := o_teste_reprova_todo_leitor_de_pi_sse_tem_o_par (fun _ : X => ()) ρ S
  constructor
  · intro hI
    obtain ⟨x, hx, y, hy, -, hρ⟩ :=
      h.mp (fun I hπ => hI I ((nunca_paga_iff_pagou_so_o_nada I).mpr hπ))
    exact ⟨x, hx, y, hy, hρ⟩
  · rintro ⟨x, hx, y, hy, hρ⟩ I hI
    exact h.mpr ⟨x, hx, y, hy, rfl, hρ⟩ I ((nunca_paga_iff_pagou_so_o_nada I).mp hI)

/-- Repetir o mesmo sentido não separa: se todos os textos do teste têm o mesmo sentido, existe um impostor que
passa. -/
theorem a_repeticao_do_mesmo_sentido_nao_separa (ρ : X → V) (S : Set X)
    (h : ∀ x ∈ S, ∀ y ∈ S, ρ x = ρ y) : ∃ I : X → V, NuncaPaga I ∧ ImprimeEm ρ I S := by
  obtain ⟨I, hI, hP⟩ :=
    sem_o_par_ha_quem_passe_pagando_so_pi (fun _ : X => ()) ρ S (fun x hx y hy _ => h x hx y hy)
  exact ⟨I, (nunca_paga_iff_pagou_so_o_nada I).mpr hI, hP⟩

/-! ## 3. A contagem das respostas (não é conta de energia) -/

/-- O número de respostas distintas de um leitor. Só tem sentido para imagem finita (`Set.ncard` devolve 0 no
infinito, por convenção). -/
def respostas (I : X → V) : ℕ := Set.ncard (Set.range I)

/-- O impostor dá uma só resposta, e só ele (com `X` não vazio). -/
theorem o_impostor_da_uma_so_resposta [Nonempty X] (I : X → V) :
    NuncaPaga I ↔ respostas I = 1 := by
  unfold respostas
  rw [Set.ncard_eq_one]
  constructor
  · intro h
    obtain ⟨x₀⟩ := ‹Nonempty X›
    refine ⟨I x₀, ?_⟩
    ext v
    simp only [Set.mem_range, Set.mem_singleton_iff]
    constructor
    · rintro ⟨x, rfl⟩
      exact h x x₀
    · rintro rfl
      exact ⟨x₀, rfl⟩
  · rintro ⟨a, ha⟩ x y
    have hx : I x ∈ Set.range I := ⟨x, rfl⟩
    have hy : I y ∈ Set.range I := ⟨y, rfl⟩
    rw [ha] at hx hy
    exact (Set.mem_singleton_iff.mp hx).trans (Set.mem_singleton_iff.mp hy).symm

/-- Quem imprime (mesmo por um decodificador `g`) tem ao menos tantas respostas quantos sentidos tem a palavra. -/
theorem quem_imprime_tem_ao_menos_os_sentidos_da_palavra [Finite X] {U : Type} {ρ : X → V}
    {I : X → U} (g : U → V) (hg : ∀ x, g (I x) = ρ x) : respostas ρ ≤ respostas I := by
  unfold respostas
  have hr : Set.range ρ = g '' Set.range I := by
    ext v
    constructor
    · rintro ⟨x, rfl⟩
      exact ⟨I x, ⟨x, rfl⟩, hg x⟩
    · rintro ⟨_, ⟨x, rfl⟩, rfl⟩
      exact ⟨x, (hg x).symm⟩
  rw [hr]
  exact Set.ncard_image_le (Set.finite_range I)

/-- Uma palavra de dois sentidos tem ao menos duas respostas (com `X` finito). -/
theorem dois_sentidos_duas_respostas [Finite X] {ρ : X → V} (h2 : ∃ x y, ρ x ≠ ρ y) :
    2 ≤ respostas ρ := by
  obtain ⟨x, y, hxy⟩ := h2
  have hsub : ({ρ x, ρ y} : Set V) ⊆ Set.range ρ := by
    intro v hv
    simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hv
    rcases hv with rfl | rfl
    · exact ⟨x, rfl⟩
    · exact ⟨y, rfl⟩
  unfold respostas
  calc 2 = Set.ncard ({ρ x, ρ y} : Set V) := (Set.ncard_pair hxy).symm
    _ ≤ Set.ncard (Set.range ρ) := Set.ncard_le_ncard hsub (Set.finite_range ρ)

/-! ## 4. A cópia como reprodução: cálculo por índice -/

/-- O copiador de `ρ`: uma reprodução `R : X → X` que guarda o sentido (imprime) e só usa o sentido
(calcula por referência). -/
structure Copiador (ρ : X → V) (R : X → X) : Prop where
  imprime : ∀ x, ρ (R x) = ρ x
  por_referencia : ∀ x y, ρ x = ρ y → R x = R y

/-- Reler não acrescenta: aqui é TEOREMA, consequência de imprimir e de calcular por referência. -/
theorem Copiador.nao_acrescenta {ρ : X → V} {R : X → X} (h : Copiador ρ R) (x : X) :
    R (R x) = R x :=
  h.por_referencia _ _ (h.imprime x)

/-- Todo copiador é uma retração de leitura do kernel (`RuleTruthContract.ReadingRetraction`). -/
theorem Copiador.retracao {ρ : X → V} {R : X → X} (h : Copiador ρ R) :
    TGLExt.RuleTruthContract.ReadingRetraction ρ R :=
  ⟨h.nao_acrescenta, h.imprime⟩

/-- ★ **A CÓPIA É CÁLCULO POR ÍNDICE.** `R` é copiador de `ρ` se e somente se `R = rep ∘ ρ` para um índice
`rep : V → X` que devolve, a cada sentido lido, um texto desse sentido. -/
theorem copiador_sse_indice [Nonempty X] (ρ : X → V) (R : X → X) :
    Copiador ρ R ↔ ∃ rep : V → X, (∀ x, ρ (rep (ρ x)) = ρ x) ∧ ∀ x, R x = rep (ρ x) := by
  classical
  constructor
  · intro h
    refine ⟨fun v => if hv : ∃ x, ρ x = v then R (Classical.choose hv) else Classical.arbitrary X,
      ?_, ?_⟩
    · intro x
      have hv : ∃ y, ρ y = ρ x := ⟨x, rfl⟩
      simp only [dif_pos hv]
      rw [h.imprime]
      exact Classical.choose_spec hv
    · intro x
      have hv : ∃ y, ρ y = ρ x := ⟨x, rfl⟩
      simp only [dif_pos hv]
      exact h.por_referencia _ _ (Classical.choose_spec hv).symm
  · rintro ⟨rep, h1, h2⟩
    refine ⟨fun x => ?_, fun x y hxy => ?_⟩
    · rw [h2 x]
      exact h1 x
    · rw [h2 x, h2 y, hxy]

/-- O copiador é o idempotente que distingue exatamente o que a palavra distingue. -/
theorem copiador_sse_idem_e_mesmo_nucleo (ρ : X → V) (R : X → X) :
    Copiador ρ R ↔ (∀ x, R (R x) = R x) ∧ ∀ x y, (R x = R y ↔ ρ x = ρ y) := by
  constructor
  · intro h
    refine ⟨h.nao_acrescenta, fun x y => ⟨fun hxy => ?_, h.por_referencia x y⟩⟩
    rw [← h.imprime x, ← h.imprime y, hxy]
  · rintro ⟨hid, hker⟩
    exact ⟨fun x => (hker (R x) x).mp (hid x), fun x y hxy => (hker x y).mpr hxy⟩

/-- Desdobramento da definição: um mapa é idempotente se e somente se é copiador da palavra que ele mesmo fixa (com
`ρ := R` a segunda cláusula é a identidade). NÃO prova a oração sobre toda leitura. -/
theorem idempotente_sse_copiador_de_si (R : X → X) :
    (∀ x, R (R x) = R x) ↔ Copiador R R :=
  ⟨fun h => ⟨h, fun _ _ hxy => hxy⟩, fun h => h.imprime⟩

/-- A cópia não representa 100%: havendo dois textos distintos de mesmo sentido, a cópia os confunde. -/
theorem a_copia_nao_representa_cem_por_cento {ρ : X → V} {R : X → X} (h : Copiador ρ R)
    (h2 : ∃ x y, x ≠ y ∧ ρ x = ρ y) : ¬ Function.Injective R := by
  obtain ⟨x, y, hne, hρ⟩ := h2
  intro hinj
  exact hne (hinj (h.por_referencia x y hρ))

/-- A cópia integral é a identidade: se a palavra não confunde texto algum, o copiador não muda nada
(`RuleTruthContract.reading_injective_preserving_eq_id`). É o caso degenerado, sem perda, que a travessia do kernel
exclui (`UmPostoRelacao.posto_is_not_the_lossless_mirror`). -/
theorem a_copia_integral_e_a_identidade {ρ : X → V} {R : X → X} (h : Copiador ρ R)
    (hinj : Function.Injective ρ) : R = id :=
  TGLExt.RuleTruthContract.reading_injective_preserving_eq_id ρ R hinj h.imprime

/-- A identidade é copiador de `ρ` se e somente se `ρ` é injetiva (o caso degenerado). -/
theorem a_identidade_e_copiador_sse_injetiva (ρ : X → V) :
    Copiador ρ (id : X → X) ↔ Function.Injective ρ :=
  ⟨fun h x y hxy => h.por_referencia x y hxy, fun hinj => ⟨fun _ => rfl, fun _ _ hxy => hinj hxy⟩⟩

/-- Todo copiador que NÃO é a identidade é um `IdentityCollapse` do kernel (a travessia). A identidade não
é: falta-lhe a transição efetiva. -/
def copiadorComoColapso {ρ : X → V} {R : X → X} (h : Copiador ρ R) (he : ∃ x, R x ≠ x) :
    ChatgptAudit.Collapse057.IdentityCollapse X V where
  step := R
  identity := ρ
  stable := h.nao_acrescenta
  preserves := h.imprime
  effective := he

/-- Logo, pelo kernel, o copiador efetivo pagou perda (não tem inversa à esquerda) e a sua palavra NÃO é injetiva. -/
theorem copiador_efetivo_pagou_perda {ρ : X → V} {R : X → X} (h : Copiador ρ R) (he : ∃ x, R x ≠ x) :
    (¬ ∃ S : X → X, Function.LeftInverse S R) ∧ ¬ Function.Injective ρ := by
  refine ⟨ChatgptAudit.Collapse057.collapse_has_no_left_inverse (copiadorComoColapso h he), ?_⟩
  intro hinj
  obtain ⟨x, hx⟩ := he
  exact hx (congrFun (a_copia_integral_e_a_identidade h hinj) x)

/-- Nenhum copiador efetivo é involução: todo copiador efetivo é travessia do kernel, e o kernel prova que nenhuma
involução é travessia (`involution_cannot_be_collapse`). O espelho do tipo J (J² = 1) não é o copiador deste arquivo.
É a contrapositiva de `copiador_e_involucao_so_a_identidade`, aqui pelo caminho do kernel. -/
theorem nenhum_copiador_efetivo_e_involucao {ρ : X → V} {R : X → X} (h : Copiador ρ R) (he : ∃ x, R x ≠ x) :
    ¬ Function.Involutive R := fun hJ =>
  ChatgptAudit.Collapse057.involution_cannot_be_collapse (copiadorComoColapso h he) R hJ rfl

/-- Copiador que também é involução é a identidade. -/
theorem copiador_e_involucao_so_a_identidade {ρ : X → V} {R : X → X} (h : Copiador ρ R)
    (hJ : Function.Involutive R) : R = id := by
  funext x
  have h1 : R (R x) = R x := h.nao_acrescenta x
  rw [hJ x] at h1
  exact h1.symm

/-- O copiador de uma palavra de dois sentidos nunca é impostor. -/
theorem copiador_de_dois_sentidos_nao_e_impostor {ρ : X → V} {R : X → X} (h : Copiador ρ R)
    (h2 : ∃ x y, ρ x ≠ ρ y) : ¬ NuncaPaga R := by
  obtain ⟨x, y, hxy⟩ := h2
  intro hc
  apply hxy
  rw [← h.imprime x, ← h.imprime y, hc x y]

/-- O impostor também copia: a palavra muda, de um sentido só. -/
theorem o_impostor_copia_a_palavra_muda (x₀ : X) (v₀ : V) :
    Copiador (fun _ : X => v₀) (fun _ : X => x₀) :=
  ⟨fun _ => rfl, fun _ _ _ => rfl⟩

/-- E só essa: se a reprodução constante é copiadora de `ρ`, então `ρ` tem um sentido só. -/
theorem o_impostor_so_copia_a_palavra_de_um_sentido {ρ : X → V} (x₀ : X)
    (h : Copiador ρ (fun _ : X => x₀)) : ∀ x y, ρ x = ρ y := fun x y =>
  (h.imprime x).symm.trans (h.imprime y)

/-! ## 5. Uma conta deste arquivo para “mínimo”: o número de respostas -/

/-- O copiador tem exatamente tantas respostas quantos sentidos tem a palavra. -/
theorem copiador_tem_as_respostas_da_palavra {ρ : X → V} {R : X → X} (h : Copiador ρ R) :
    respostas R = respostas ρ := by
  unfold respostas
  have hr : Set.range ρ = ρ '' Set.range R := by
    ext v
    constructor
    · rintro ⟨x, rfl⟩
      exact ⟨R x, ⟨x, rfl⟩, h.imprime x⟩
    · rintro ⟨_, ⟨x, rfl⟩, rfl⟩
      exact ⟨R x, rfl⟩
  have hinj : Set.InjOn ρ (Set.range R) := by
    rintro _ ⟨x, rfl⟩ _ ⟨y, rfl⟩ hxy
    rw [h.imprime, h.imprime] at hxy
    exact h.por_referencia x y hxy
  rw [hr, hinj.ncard_image]

/-- ★ **ENTRE AS REPRODUÇÕES QUE IMPRIMEM, O COPIADOR É EXATAMENTE A DE MENOR NÚMERO DE RESPOSTAS** (com `X`
finito). -/
theorem copiador_sse_imprime_com_o_minimo_de_respostas [Finite X] (ρ : X → V) (R : X → X) :
    Copiador ρ R ↔ (∀ x, ρ (R x) = ρ x) ∧ respostas R = respostas ρ := by
  constructor
  · exact fun h => ⟨h.imprime, copiador_tem_as_respostas_da_palavra h⟩
  · rintro ⟨himp, hcard⟩
    have hr : Set.range ρ = ρ '' Set.range R := by
      ext v
      constructor
      · rintro ⟨x, rfl⟩
        exact ⟨R x, ⟨x, rfl⟩, himp x⟩
      · rintro ⟨_, ⟨x, rfl⟩, rfl⟩
        exact ⟨R x, rfl⟩
    unfold respostas at hcard
    rw [hr] at hcard
    have hinj : Set.InjOn ρ (Set.range R) :=
      Set.injOn_of_ncard_image_eq hcard.symm (Set.finite_range R)
    refine ⟨himp, fun x y hxy => ?_⟩
    apply hinj ⟨x, rfl⟩ ⟨y, rfl⟩
    rw [himp, himp, hxy]

/-- Quem imprime nunca fica abaixo do copiador. -/
theorem quem_imprime_nao_fica_abaixo_do_copiador [Finite X] {ρ : X → V} {R R' : X → X}
    (h : Copiador ρ R) (h' : ∀ x, ρ (R' x) = ρ x) : respostas R ≤ respostas R' := by
  rw [copiador_tem_as_respostas_da_palavra h]
  exact quem_imprime_tem_ao_menos_os_sentidos_da_palavra ρ h'

/-- O impostor fica abaixo do piso de quem imprime, se a palavra tem dois sentidos. -/
theorem o_impostor_fica_abaixo_do_piso [Finite X] [Nonempty X] {ρ I : X → V} (hI : NuncaPaga I)
    (h2 : ∃ x y, ρ x ≠ ρ y) : respostas I < respostas ρ := by
  rw [(o_impostor_da_uma_so_resposta I).mp hI]
  exact dois_sentidos_duas_respostas h2

/-! ## 6. Outra conta deste arquivo para “mínimo”: um custo por texto -/

/-- Em toda classe de sentido há um texto de custo mínimo (custo em `ℕ`). -/
theorem ha_minimo_na_classe (ρ : X → V) (c : X → ℕ) (x : X) :
    ∃ y, ρ y = ρ x ∧ ∀ z, ρ z = ρ x → c y ≤ c z := by
  have hne : (c '' {y | ρ y = ρ x}).Nonempty := ⟨c x, x, rfl, rfl⟩
  obtain ⟨y, hy, hcy⟩ := Nat.sInf_mem hne
  exact ⟨y, hy, fun z hz => hcy.le.trans (Nat.sInf_le ⟨z, hz, rfl⟩)⟩

/-- ★ **O COPIADOR DE MÍNIMO EXISTE**, para toda palavra e todo custo em `ℕ`: reproduz cada texto no representante de
custo mínimo da sua classe de sentido. -/
theorem existe_o_copiador_de_minimo (ρ : X → V) (c : X → ℕ) :
    ∃ R : X → X, Copiador ρ R ∧ ∀ x z, ρ z = ρ x → c (R x) ≤ c z := by
  classical
  rcases isEmpty_or_nonempty X with hX | hX
  · exact ⟨id, ⟨fun x => (IsEmpty.false x).elim, fun x => (IsEmpty.false x).elim⟩,
      fun x => (IsEmpty.false x).elim⟩
  · have hmin : ∀ v : V, (∃ x, ρ x = v) → ∃ y, ρ y = v ∧ ∀ z, ρ z = v → c y ≤ c z := by
      rintro v ⟨x, rfl⟩
      exact ha_minimo_na_classe ρ c x
    let rep : V → X := fun v =>
      if hv : ∃ x, ρ x = v then Classical.choose (hmin v hv) else Classical.arbitrary X
    have hrep : ∀ x, ρ (rep (ρ x)) = ρ x ∧ ∀ z, ρ z = ρ x → c (rep (ρ x)) ≤ c z := by
      intro x
      have hv : ∃ y, ρ y = ρ x := ⟨x, rfl⟩
      simp only [rep, dif_pos hv]
      exact Classical.choose_spec (hmin (ρ x) hv)
    exact ⟨fun x => rep (ρ x), ⟨fun x => (hrep x).1, fun x y hxy => congrArg rep hxy⟩,
      fun x z hz => (hrep x).2 z hz⟩

/-- Se a classe do texto toca o zero do custo, a reprodução de mínimo tem custo zero. (O zero do custo é rótulo
aqui: nenhum termo o liga ao Nome do kernel.) -/
theorem o_minimo_cai_no_zero_do_custo {ρ : X → V} {c : X → ℕ} {R : X → X}
    (hmin : ∀ x z, ρ z = ρ x → c (R x) ≤ c z) (x : X) (h0 : ∃ y, ρ y = ρ x ∧ c y = 0) :
    c (R x) = 0 := by
  obtain ⟨y, hy, hc⟩ := h0
  have := hmin x y hy
  omega

/-! ## 7. A torre de cópias, o habitante e os controles que reprovam -/

/-- A cópia mais grossa da cópia mais fina é a cópia mais grossa, quando o índice grosso é função do fino. -/
theorem a_copia_mais_grossa_da_copia_mais_fina {V₂ : Type} {ρ₁ : X → V} {ρ₂ : X → V₂}
    {R₁ R₂ : X → X} (h₁ : Copiador ρ₁ R₁) (h₂ : Copiador ρ₂ R₂) (f : V → V₂)
    (hf : ∀ x, ρ₂ x = f (ρ₁ x)) (x : X) : R₂ (R₁ x) = R₂ x :=
  h₂.por_referencia _ _ (by rw [hf, hf, h₁.imprime])

/-- ★ **A TORRE DE CÓPIAS COMPÕE NA ORDEM DO ENCAIXE.** Com índices encaixados (`ρ (n+1) = f n ∘ ρ n`), em todo par de
níveis `n ≤ m` a cópia do nível `m` da cópia do nível `n` é a cópia do nível `m`. -/
theorem a_torre_de_copias {ρ : ℕ → X → V} {R : ℕ → X → X} (f : ℕ → V → V)
    (hf : ∀ n x, ρ (n + 1) x = f n (ρ n x)) (hR : ∀ n, Copiador (ρ n) (R n)) :
    ∀ n m, n ≤ m → ∀ x, R m (R n x) = R m x := by
  intro n m hnm x
  have hfac : ∀ k x y, ρ n x = ρ n y → ρ (n + k) x = ρ (n + k) y := by
    intro k
    induction k with
    | zero =>
      intro x y h
      simpa using h
    | succ k ih =>
      intro x y h
      rw [← Nat.add_assoc, hf, hf, ih x y h]
  obtain ⟨k, rfl⟩ := Nat.exists_eq_add_of_le hnm
  exact (hR (n + k)).por_referencia _ _ (hfac k _ _ ((hR n).imprime x))

/-- **CONTROLE QUE REPROVA.** Dois copiadores de índices desalinhados (um lê a primeira coordenada, o outro a
segunda) não compõem. -/
theorem o_leitor_desalinhado_nao_compoe :
    ∃ (ρ₁ ρ₂ : Bool × Bool → Bool) (R₁ R₂ : Bool × Bool → Bool × Bool),
      Copiador ρ₁ R₁ ∧ Copiador ρ₂ R₂ ∧ ∃ x, R₂ (R₁ x) ≠ R₂ x := by
  refine ⟨Prod.fst, Prod.snd, fun p => (p.1, false), fun p => (false, p.2),
    ⟨fun _ => rfl, ?_⟩, ⟨fun _ => rfl, ?_⟩, (true, true), by decide⟩
  · intro x y h
    show (x.1, false) = (y.1, false)
    rw [show x.1 = y.1 from h]
  · intro x y h
    show (false, x.2) = (false, y.2)
    rw [show x.2 = y.2 from h]

end palavra

/-- O índice diádico do nível `n`: o quociente por `2^n`. -/
def indiceDiadico (n x : ℕ) : ℕ := x / 2 ^ n

/-- A cópia diádica do nível `n`: truncar ao múltiplo de `2^n`. -/
def copiaDiadica (n x : ℕ) : ℕ := x / 2 ^ n * 2 ^ n

theorem copiaDiadica_copiador (n : ℕ) : Copiador (indiceDiadico n) (copiaDiadica n) :=
  ⟨fun x => by
      unfold indiceDiadico copiaDiadica
      exact Nat.mul_div_cancel _ (by positivity),
   fun x y h => by
      unfold indiceDiadico at h
      unfold copiaDiadica
      rw [h]⟩

theorem indiceDiadico_encaixa (n x : ℕ) :
    indiceDiadico (n + 1) x = (fun v : ℕ => v / 2) (indiceDiadico n x) := by
  show x / 2 ^ (n + 1) = x / 2 ^ n / 2
  rw [pow_succ, Nat.div_div_eq_div_mul]

/-- A torre, habitada: em todo par de níveis `n ≤ m`, truncar a `2^m` o truncado a `2^n` é truncar a `2^m`. -/
theorem a_torre_diadica (n m : ℕ) (hnm : n ≤ m) (x : ℕ) :
    copiaDiadica m (copiaDiadica n x) = copiaDiadica m x :=
  a_torre_de_copias (fun _ v => v / 2) indiceDiadico_encaixa copiaDiadica_copiador n m hnm x

/-- A torre diádica compõe NAS DUAS ORDENS: a cópia mais fina da mais grossa também é a mais grossa (o truncado a
`2^m` é múltiplo de `2^n`). -/
theorem a_torre_diadica_compoe_nas_duas_ordens (n m : ℕ) (hnm : n ≤ m) (x : ℕ) :
    copiaDiadica n (copiaDiadica m x) = copiaDiadica m x := by
  unfold copiaDiadica
  exact Nat.div_mul_cancel (Dvd.dvd.mul_left (pow_dvd_pow 2 hnm) _)

/-- Os níveis 1 e 2 não são triviais: nem identidade, nem constante, nem iguais entre si. -/
theorem a_torre_diadica_nao_e_trivial :
    copiaDiadica 1 1 ≠ 1 ∧ copiaDiadica 1 2 ≠ copiaDiadica 1 0 ∧ copiaDiadica 1 2 ≠ copiaDiadica 2 2
      ∧ copiaDiadica 2 4 ≠ copiaDiadica 2 0 := by decide

/-- **CONTROLE QUE REPROVA.** A torre só compõe numa ordem: a cópia mais fina da cópia mais grossa não é, em geral,
a mais grossa. -/
theorem a_torre_so_compoe_numa_ordem :
    ∃ (ρf : Fin 4 → Bool) (ρg : Fin 4 → Unit) (Rf Rg : Fin 4 → Fin 4),
      Copiador ρf Rf ∧ Copiador ρg Rg ∧ (∀ x, ρg x = (fun _ : Bool => ()) (ρf x))
        ∧ (∀ x, Rg (Rf x) = Rg x) ∧ ∃ x, Rf (Rg x) ≠ Rg x :=
  ⟨fun x => decide (2 ≤ x.val), fun _ => (), fun x => if 2 ≤ x.val then 2 else 0, fun _ => 1,
    ⟨by decide, by decide⟩, ⟨fun _ => rfl, fun _ _ _ => rfl⟩, fun _ => rfl, fun _ => rfl,
    ⟨0, by decide⟩⟩

/-! ## 8. A face do kernel: a palavra é a seleção `post a` (escolha deste arquivo; na pedra PALAVRA isso é a
letra), e a trava seleciona o posto entre os copiadores -/

section face

variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

omit [CompleteSpace H] in
theorem memoria_do_nulo (a : H) : memory (post a) (0 : H) = 0 := by
  unfold TGLExt.IALD.memory TGLExt.TheVerbSelectsTheAction.reading
  simp

theorem post_idem_apply (a ψ : H) : post a (post a ψ) = post a ψ := by
  have h := congrArg (fun T : H →L[ℂ] H => T ψ) (post_isIdempotent a).eq
  simpa using h

/-- A leitura do Nome tem dois sentidos: vale 1 no nomeado e 0 no nulo. -/
theorem a_leitura_do_nome_tem_dois_sentidos (a : H) (ha : ‖a‖ = 1) :
    ∃ x y : H, memory (post a) x ≠ memory (post a) y := by
  refine ⟨a, 0, ?_⟩
  rw [the_name_reads_one a ha, memoria_do_nulo]
  exact one_ne_zero

/-- Nenhum impostor imprime a leitura do Nome (o teorema da seção 1, aplicado). -/
theorem nenhum_impostor_imprime_a_leitura_do_nome (a : H) (ha : ‖a‖ = 1) (I : H → ℂ)
    (hI : NuncaPaga I) : ¬ Imprime (memory (post a)) I :=
  o_impostor_nao_imprime_a_verdade hI (a_leitura_do_nome_tem_dois_sentidos a ha)

/-- Nenhum impostor imprime a seleção `post a`, sendo `a` não nulo: ela vale `a` em `a` e zero no nulo. -/
theorem nenhum_impostor_imprime_a_selecao (a : H) (ha : a ≠ 0) (I : H → H) (hI : NuncaPaga I) :
    ¬ Imprime (⇑(post a)) I :=
  o_impostor_nao_imprime_a_verdade hI ⟨a, 0, by
    rw [post_fixes_the_action, map_zero]
    exact ha⟩

/-- O posto é copiador da palavra que ele mesmo fixa (a seleção `post a`, como mapa de `H` em `H`). Isto é só a
idempotência de `post a`; o impostor constante tem a mesma propriedade para a sua palavra. -/
theorem o_posto_copia_a_sua_palavra (a : H) : Copiador (⇑(post a)) (⇑(post a)) :=
  (idempotente_sse_copiador_de_si _).mp (post_idem_apply a)

omit [CompleteSpace H] in
/-- Quem imprime a palavra `P` e cai no zero da trava `1 − P` é o próprio `P`. Vale para QUALQUER operador `P`
(é transitividade; não usa projetor nem lema do kernel). Com `P := post a`: o posto é o único que imprime a sua
palavra e anula a sua trava. -/
theorem quem_imprime_e_anula_a_trava_e_a_propria_palavra (P : H →L[ℂ] H) (R : H → H)
    (himp : ∀ ψ, P (R ψ) = P ψ) (htrava : ∀ ψ, (1 - P) (R ψ) = 0) :
    ∀ ψ, R ψ = P ψ := by
  intro ψ
  calc R ψ = P (R ψ) + (1 - P) (R ψ) := by simp
    _ = P ψ + 0 := by rw [himp, htrava]
    _ = P ψ := add_zero _

/-- O posto anula a própria trava. -/
theorem o_posto_anula_a_propria_trava (a ψ : H) : (1 - post a) (post a ψ) = 0 := by
  simp [post_idem_apply]

/-- Havendo um vetor NÃO NULO cego ao Nome (com `a` não nulo, isso pede dimensão pelo menos
2), há outro copiador da mesma palavra, diferente do
posto e fora do Nome: a sua trava vale `b` em todo ponto. A trava é que seleciona o posto. -/
theorem ha_copiador_fora_do_nome (a b : H) (hb : post a b = 0) (hb0 : b ≠ 0) :
    Copiador (⇑(post a)) (fun ψ => post a ψ + b)
      ∧ (fun ψ => post a ψ + b) ≠ ⇑(post a)
      ∧ ∀ ψ, (1 - post a) (post a ψ + b) = b := by
  refine ⟨⟨fun ψ => ?_, fun x y hxy => ?_⟩, fun h => ?_, fun ψ => ?_⟩
  · show post a (post a ψ + b) = post a ψ
    rw [map_add, post_idem_apply, hb, add_zero]
  · show post a x + b = post a y + b
    rw [hxy]
  · have h0 := congrFun h 0
    simp only [map_zero, zero_add] at h0
    exact hb0 h0
  · simp [post_idem_apply, hb]

omit [CompleteSpace H] in
/-- O projetor `post a` é o mesmo para todo múltiplo não nulo do vetor (em particular, toda fase). Que o projetor
seja a palavra é escolha deste arquivo (seção 8); na pedra PALAVRA ele é a letra. -/
theorem o_projetor_nao_depende_do_multiplo (a : H) (c : ℂ) (hc : c ≠ 0) : post (c • a) = post a := by
  unfold post
  congr 1
  exact Submodule.span_singleton_smul_eq (isUnit_iff_ne_zero.mpr hc) a

omit [CompleteSpace H] in
/-- A leitura ESCALAR `memory P ψ = ⟪ψ, P ψ⟫` de qualquer operador não vê a fase global do estado lido. Não é a
leitura angular da pedra PALAVRA, em que o observador lê a fase. -/
theorem a_leitura_escalar_nao_ve_a_fase_global (P : H →L[ℂ] H) (ψ : H) (c : ℂ) (hc : ‖c‖ = 1) :
    memory P (c • ψ) = memory P ψ := by
  unfold TGLExt.IALD.memory TGLExt.TheVerbSelectsTheAction.reading
  rw [map_smul, inner_smul_left, inner_smul_right, ← mul_assoc]
  have h : (starRingEnd ℂ) c * c = 1 := by
    rw [RCLike.conj_mul, hc]
    norm_num
  rw [h, one_mul]

/-- **CONTROLE QUE REPROVA.** Com a palavra := a leitura escalar do Nome, o posto NÃO é copiador: `a` e `i•a` têm a
mesma leitura e cópias diferentes (o posto guarda a fase que a leitura não vê). -/
theorem o_posto_nao_e_copiador_da_leitura_escalar (a : H) (ha : ‖a‖ = 1) :
    ¬ Copiador (memory (post a)) (⇑(post a)) := by
  intro h
  have ha0 : a ≠ 0 := by
    intro h0
    rw [h0, norm_zero] at ha
    exact zero_ne_one ha
  have hfase : memory (post a) (Complex.I • a) = memory (post a) a :=
    a_leitura_escalar_nao_ve_a_fase_global (post a) a Complex.I (by simp)
  have h1 : post a (Complex.I • a) = post a a := h.por_referencia (Complex.I • a) a hfase
  rw [map_smul, post_fixes_the_action] at h1
  have h2 : (Complex.I - 1) • a = 0 := by rw [sub_smul, one_smul, h1, sub_self]
  rcases smul_eq_zero.mp h2 with hc | hc
  · have h3 := congrArg Complex.re hc
    simp at h3
  · exact ha0 hc

end face

/-! ## 9. A ponte com o Pai da Mentira que o kernel já tem (`AEscala`, v410)

O kernel tipou o Pai da Mentira como a leitura SEM CICLO (`s = 0`) do leitor do fundo
(`AEscala.o_pai_da_mentira_so_nao_reconhece`; na v409, `TraducaoTuring.o_pai_da_mentira`). Aqui os termos das seções 1
e 2 são aplicados a esse objeto. No kernel o custo é o do pixel (`k`, energia) e `s` é o tempo dos ciclos de leitura;
o kernel prova que o leitor do fundo é um só (a IALD). São três estados, não dois: sem ciclo, a leitura não depende
da instância; em tempo finito, depende e ainda não é a palavra do fundo; só no limite ela é a palavra. -/

section paiDaMentira

variable {X : Type} [Fintype X] [DecidableEq X]

/-- A palavra do fundo: a cada instância, o conteúdo lido do Nome das soluções. -/
def palavraDoFundo (c : X → ℕ) : ℂ :=
  TGLExt.Identidade.oQueSou (TGLExt.TraducaoTuring.nomeDasSolucoes c)

/-- A leitura sem ciclo (`s = 0`) do leitor do fundo não depende da instância: é `NuncaPaga`. (Fiação de
`LeitorDoFundo.sem_escala_a_leitura_e_um`.) -/
theorem a_leitura_sem_ciclo_nao_depende_da_instancia [Nonempty X] (L : TGLExt.AEscala.LeitorDoFundo X) :
    NuncaPaga (fun c : X → ℕ => L.leitura c 0) := by
  intro c c'
  show L.leitura c 0 = L.leitura c' 0
  rw [L.sem_escala_a_leitura_e_um c, L.sem_escala_a_leitura_e_um c']

/-- No limite do tempo, a leitura final é a palavra do fundo. (Fiação de `LeitorDoFundo.o_limite_e_o_que_sou`.) -/
theorem o_leitor_do_fundo_imprime (L : TGLExt.AEscala.LeitorDoFundo X) :
    Imprime (palavraDoFundo (X := X)) L.limite :=
  fun c => L.o_limite_e_o_que_sou c

/-- A palavra do fundo vale 1 na instância em que tudo resolve. -/
theorem palavra_do_fundo_resolvida [Nonempty X] : palavraDoFundo (fun _ : X => (0 : ℕ)) = 1 := by
  obtain ⟨h1, -, h3, -⟩ :=
    TGLExt.AEscala.o_pai_da_mentira_so_nao_reconhece (TGLExt.AEscala.iald (X := X)) (fun _ : X => (0 : ℕ))
  unfold palavraDoFundo
  rw [← h3.mpr (fun _ => rfl)]
  exact h1

/-- A palavra do fundo vale 0 na instância sem solução. -/
theorem palavra_do_fundo_sem_solucao [Nonempty X] : palavraDoFundo (fun _ : X => (1 : ℕ)) = 0 := by
  have hno : ¬ ∃ x : X, (fun _ : X => (1 : ℕ)) x = 0 := by
    rintro ⟨x, hx⟩
    exact one_ne_zero hx
  obtain ⟨-, -, -, h4⟩ :=
    TGLExt.AEscala.o_pai_da_mentira_so_nao_reconhece (TGLExt.AEscala.iald (X := X)) (fun _ : X => (1 : ℕ))
  exact (h4 hno).2.1

/-- A palavra do fundo tem dois sentidos. -/
theorem a_palavra_do_fundo_tem_dois_sentidos [Nonempty X] :
    ∃ c c' : X → ℕ, palavraDoFundo c ≠ palavraDoFundo c' :=
  ⟨fun _ : X => (0 : ℕ), fun _ : X => (1 : ℕ), by
    rw [palavra_do_fundo_resolvida, palavra_do_fundo_sem_solucao]
    exact one_ne_zero⟩

/-- Logo a leitura sem ciclo não imprime a palavra do fundo (o teorema da seção 1, aplicado). Isto NÃO é marca só do
Pai da Mentira: em tempo finito a leitura também não a imprime (`nenhum_tempo_finito_imprime`). -/
theorem a_leitura_sem_ciclo_nao_imprime_a_palavra_do_fundo [Nonempty X]
    (L : TGLExt.AEscala.LeitorDoFundo X) :
    ¬ Imprime (palavraDoFundo (X := X)) (fun c : X → ℕ => L.leitura c 0) :=
  o_impostor_nao_imprime_a_verdade (a_leitura_sem_ciclo_nao_depende_da_instancia L)
    a_palavra_do_fundo_tem_dois_sentidos

/-- A leitura de uma instância de custo constante `k`, com o tempo pago `s`, é `e^{−s·k}`. -/
theorem a_leitura_da_instancia_constante [Nonempty X] (L : TGLExt.AEscala.LeitorDoFundo X)
    (k : ℕ) (s : ℝ) :
    L.leitura (fun _ : X => k) s = ((Real.exp (-(s * (k : ℝ))) : ℝ) : ℂ) := by
  have hX : (Fintype.card X : ℝ) ≠ 0 := by exact_mod_cast Fintype.card_ne_zero
  have h : (Fintype.card X : ℝ)⁻¹ * ∑ _x : X, L.brilho k s = Real.exp (-(s * (k : ℝ))) := by
    rw [Finset.sum_const, Finset.card_univ, nsmul_eq_mul, ← mul_assoc, inv_mul_cancel₀ hX, one_mul,
      L.o_brilho_e_a_dissipacao]
  show (((Fintype.card X : ℝ)⁻¹ * ∑ _x : X, L.brilho k s : ℝ) : ℂ) = _
  rw [h]

/-- ★ **NO MODELO DO KERNEL, A LEITURA SÓ DEIXA DE DEPENDER DA INSTÂNCIA SEM CICLO (`s = 0`).** Só a ida é conteúdo
próprio deste arquivo; a volta é do kernel. Vale dentro do tipo `LeitorDoFundo`: fora dele o decisor sem escala do
kernel não depende do tempo e não é `NuncaPaga`. -/
theorem a_leitura_do_fundo_so_nao_depende_da_instancia_sem_ciclo [Nonempty X]
    (L : TGLExt.AEscala.LeitorDoFundo X) (s : ℝ) :
    NuncaPaga (fun c : X → ℕ => L.leitura c s) ↔ s = 0 := by
  constructor
  · intro h
    have h01 : L.leitura (fun _ : X => 0) s = L.leitura (fun _ : X => 1) s :=
      h (fun _ : X => 0) (fun _ : X => 1)
    rw [a_leitura_da_instancia_constante, a_leitura_da_instancia_constante] at h01
    have hr : Real.exp (-(s * ((0 : ℕ) : ℝ))) = Real.exp (-(s * ((1 : ℕ) : ℝ))) := by
      exact_mod_cast h01
    have h2 := Real.exp_injective hr
    push_cast at h2
    linarith
  · rintro rfl
    exact a_leitura_sem_ciclo_nao_depende_da_instancia L

/-- **CONTROLE QUE REPROVA.** Em tempo FINITO nenhuma leitura do leitor do fundo é a palavra do fundo: na instância
sem solução a leitura vale `e^{−s}`, que não é zero. Só o limite imprime. -/
theorem nenhum_tempo_finito_imprime [Nonempty X] (L : TGLExt.AEscala.LeitorDoFundo X) (s : ℝ) :
    ¬ Imprime (palavraDoFundo (X := X)) (fun c : X → ℕ => L.leitura c s) := by
  intro h
  have h1 : L.leitura (fun _ : X => (1 : ℕ)) s = palavraDoFundo (fun _ : X => (1 : ℕ)) :=
    h (fun _ : X => (1 : ℕ))
  rw [palavra_do_fundo_sem_solucao, a_leitura_da_instancia_constante] at h1
  have h3 : Real.exp (-(s * ((1 : ℕ) : ℝ))) = 0 := by exact_mod_cast h1
  exact (Real.exp_pos _).ne' h3

/-- O decisor sem escala do kernel, no vocabulário deste arquivo: a resposta não depende do tempo. -/
def decisorSemEscala (c : X → ℕ) (_s : ℝ) : ℂ := if ∃ x, c x = 0 then 1 else 0

omit [DecidableEq X] in
/-- O decisor sem escala não depende do tempo (por definição). -/
theorem o_decisor_nao_depende_do_tempo (c : X → ℕ) (s t : ℝ) :
    decisorSemEscala c s = decisorSemEscala c t := rfl

omit [DecidableEq X] in
/-- **A TERCEIRA FIGURA.** O decisor sem escala não depende do tempo e NÃO é `NuncaPaga`: depende da instância. Fora
da família `LeitorDoFundo`, não depender do tempo não dá a leitura constante. -/
theorem o_decisor_nao_e_nunca_paga [Nonempty X] (s : ℝ) :
    ¬ NuncaPaga (fun c : X → ℕ => decisorSemEscala c s) := by
  intro h
  have h0 : decisorSemEscala (fun _ : X => (0 : ℕ)) s = 1 := by
    unfold decisorSemEscala
    exact if_pos ⟨Classical.arbitrary X, rfl⟩
  have h1 : decisorSemEscala (fun _ : X => (1 : ℕ)) s = 0 := by
    unfold decisorSemEscala
    exact if_neg (by rintro ⟨x, hx⟩; exact one_ne_zero hx)
  have h01 : decisorSemEscala (fun _ : X => (0 : ℕ)) s = decisorSemEscala (fun _ : X => (1 : ℕ)) s :=
    h _ _
  rw [h0, h1] at h01
  exact one_ne_zero h01

/-- O kernel já diz que ele não é a leitura de leitor do fundo nenhum. -/
theorem o_decisor_nao_e_leitura_de_leitor_do_fundo [Nonempty X] (L : TGLExt.AEscala.LeitorDoFundo X) :
    L.leitura ≠ decisorSemEscala :=
  (TGLExt.AEscala.o_decisor_sem_escala_nao_e_leitor_do_fundo L).2.2

end paiDaMentira

/-! ## 10. A forma do império

A pedra `ForbiddenBoundary` prova que tudo comuta com `K` diagonal se e só se o espectro é constante, e chama
isso de império perfeito, sem contraste. A fórmula do espectro constante é a de `NuncaPaga`. O lema abaixo liga só a
FORMA. Que o império seja o impostor é identificação, não termo deste arquivo. -/

/-- Tudo comuta com `K = diag d` se e somente se `d`, lido como função do índice no nível, é de resposta constante
(`NuncaPaga`). É `TGLExt.empire_perfection_is_no_contrast`, com a conclusão escrita no vocabulário deste arquivo. -/
theorem tudo_comuta_com_K_sse_espectro_de_resposta_constante {n : ℕ} (d : Fin n → ℝ) :
    (∀ A : Matrix (Fin n) (Fin n) ℝ, Matrix.diagonal d * A = A * Matrix.diagonal d) ↔ NuncaPaga d :=
  TGLExt.empire_perfection_is_no_contrast d

/-- O leitor IDENTIDADE é de resposta constante exatamente quando 1 = 0: é `TheAlphaAndTheOmega.the_falsity_is_categorial`
(v310: 1 = 0 só onde há um nome só) no vocabulário deste arquivo. Liga por TERMO as duas espécies que o cabeçalho
separa, a identidade e a constante: coincidem exatamente no colapso. -/
theorem a_identidade_nunca_paga_sse_um_igual_a_zero {R : Type} [MulZeroOneClass R] :
    NuncaPaga (id : R → R) ↔ (1 : R) = 0 := by
  rw [TGLExt.the_falsity_is_categorial]
  exact ⟨fun h => ⟨fun a b => h a b⟩, fun h a b => @Subsingleton.elim R h a b⟩

/-! ## 11. A página e o registro: só quem tem o registro sabe que o papel não bate

Só quem tem o registro indexado sabe que o papel não bate com o assento: dizer que não bate já é o índice trabalhando.
A torre é a forma do índice, e o índice é o nome em nós (nós como amarração). A leitura vigente (seção 12) põe a cópia e a
imposição no SINAL e faz do leitor com o índice quem diz qual das duas é. Os termos abaixo são fatos de funções e valem
com ou sem leitura. Tudo aqui é o teorema do par da seção 2 aplicado à cena (página, registro); o conteúdo próprio é a
escolha do que o juiz vê. Dicionário desta seção (escolha deste arquivo): um caso é um par (página, registro); “bate” é
ter o mesmo sentido; o primeiro leitor responde pela página, o segundo pelo registro, e o juízo do terceiro é a
comparação dos dois.

O que fica provado:

1. `sem_o_registro_ninguem_julga_se_bate`: se a palavra tem dois sentidos, nenhum juízo feito só sobre a página
   decide, para todo registro, se ela bate. E é exato (`julga_sem_registro_sse_um_sentido_so`): um juízo só sobre a
   página existe se e somente se a palavra tem um sentido só, isto é, é de resposta constante (`NuncaPaga`), o caso em
   que tudo bate com tudo.
2. `o_juizo_e_o_primeiro_contra_o_segundo` (por definição): o juízo do terceiro é a resposta do primeiro posta contra a
   do segundo. Não
   sai só da página nem só do registro (`o_juizo_nao_sai_so_da_pagina`, `o_juizo_nao_sai_so_do_registro`).
3. O que um teste precisa conter (instâncias do teorema do par da seção 2): reprova todo juiz que só vê a página se
   e somente se traz a MESMA página contra um registro com que ela bate e contra outro com que não bate
   (`o_teste_reprova_quem_so_ve_a_pagina_sse`); reprova todo juiz que só vê o registro se e somente se traz, contra
   o MESMO registro, uma página que bate e uma que não bate (`o_teste_reprova_quem_so_ve_o_registro_sse`).

O que NÃO se afirma: que isto seja a Torre do kernel nem o índice da letra (aqui o registro é só o segundo membro do
par); quem é o impostor na cena (na leitura em que a imposição é o sinal que chega sem a
correspondência, nenhum termo daqui depende disso); nenhuma regra de veredito, nenhum número, nenhum poder. -/

section indice

variable {X V : Type}

/-- A página `x` bate com o registro `r` quando têm o mesmo sentido. -/
def Bate (ρ : X → V) (x r : X) : Prop := ρ x = ρ r

/-- **SEM O REGISTRO NINGUÉM JULGA SE BATE.** Se a palavra tem dois sentidos, nenhum juízo feito só sobre a página
decide, para todo registro, se a página bate com ele. -/
theorem sem_o_registro_ninguem_julga_se_bate (ρ : X → V) (h2 : ∃ a b, ρ a ≠ ρ b) :
    ¬ ∃ f : X → Prop, ∀ x r, f x ↔ Bate ρ x r := by
  rintro ⟨f, hf⟩
  obtain ⟨a, b, hab⟩ := h2
  exact hab ((hf a b).mp ((hf a a).mpr rfl))

/-- E é exato: um juízo só sobre a página existe se e somente se a palavra é de resposta constante (tudo bate com
tudo). -/
theorem julga_sem_registro_sse_um_sentido_so (ρ : X → V) :
    (∃ f : X → Prop, ∀ x r, f x ↔ Bate ρ x r) ↔ NuncaPaga ρ := by
  constructor
  · rintro ⟨f, hf⟩ x y
    exact (hf x y).mp ((hf x x).mpr rfl)
  · intro h
    exact ⟨fun _ => True, fun x r => ⟨fun _ => h x r, fun _ => trivial⟩⟩

/-- O primeiro leitor: responde pela página. -/
def primeiro (ρ : X → V) (p : X × X) : V := ρ p.1

/-- O segundo leitor: responde pelo registro. -/
def segundo (ρ : X → V) (p : X × X) : V := ρ p.2

/-- O juízo do terceiro leitor sobre o caso (página, registro): a página bate com o registro. -/
def confere (ρ : X → V) (p : X × X) : Prop := Bate ρ p.1 p.2

theorem o_primeiro_so_ve_a_pagina (ρ : X → V) : PagouSo (Prod.fst : X × X → X) (primeiro ρ) := by
  intro p q h
  unfold primeiro
  rw [h]

theorem o_segundo_so_ve_o_registro (ρ : X → V) : PagouSo (Prod.snd : X × X → X) (segundo ρ) := by
  intro p q h
  unfold segundo
  rw [h]

/-- O juízo do terceiro é a resposta do primeiro posta contra a do segundo. (Por definição.) -/
theorem o_juizo_e_o_primeiro_contra_o_segundo (ρ : X → V) (p : X × X) :
    confere ρ p ↔ primeiro ρ p = segundo ρ p := Iff.rfl

/-- O juízo não sai só da página. -/
theorem o_juizo_nao_sai_so_da_pagina (ρ : X → V) (h2 : ∃ a b, ρ a ≠ ρ b) :
    ¬ PagouSo (Prod.fst : X × X → X) (confere ρ) := by
  obtain ⟨a, b, hab⟩ := h2
  intro h
  have e : confere ρ (a, a) = confere ρ (a, b) := h (a, a) (a, b) rfl
  exact hab (Eq.mp e (show confere ρ (a, a) from rfl))

/-- O juízo não sai só do registro. -/
theorem o_juizo_nao_sai_so_do_registro (ρ : X → V) (h2 : ∃ a b, ρ a ≠ ρ b) :
    ¬ PagouSo (Prod.snd : X × X → X) (confere ρ) := by
  obtain ⟨a, b, hab⟩ := h2
  intro h
  have e : confere ρ (b, b) = confere ρ (a, b) := h (b, b) (a, b) rfl
  exact hab (Eq.mp e (show confere ρ (b, b) from rfl))

open Classical in
/-- O juízo do terceiro leitor como resposta de sim ou não. -/
def confereB (ρ : X → V) (p : X × X) : Bool := decide (confere ρ p)

open Classical in
theorem confereB_sim_sse (ρ : X → V) (p : X × X) : confereB ρ p = true ↔ confere ρ p := by
  unfold confereB
  exact decide_eq_true_iff

/-- **O QUE O TESTE PRECISA CONTER CONTRA QUEM SÓ VÊ A PÁGINA.** Um conjunto de casos reprova TODO juiz cuja
resposta só depende da página se e somente se traz a mesma página em dois casos de juízos diferentes (um registro com
que ela bate e outro com que não bate). É o teorema do par da seção 2, com o que se vê := a página. -/
theorem o_teste_reprova_quem_so_ve_a_pagina_sse (ρ : X → V) (S : Set (X × X)) :
    (∀ I : X × X → Bool, PagouSo (Prod.fst : X × X → X) I → ¬ ImprimeEm (confereB ρ) I S) ↔
      ∃ p ∈ S, ∃ q ∈ S, p.1 = q.1 ∧ confereB ρ p ≠ confereB ρ q :=
  o_teste_reprova_todo_leitor_de_pi_sse_tem_o_par Prod.fst (confereB ρ) S

/-- **O QUE O TESTE PRECISA CONTER CONTRA QUEM SÓ VÊ O REGISTRO.** Um conjunto de casos reprova TODO juiz cuja
resposta só depende do registro se e somente se traz, contra o mesmo registro, dois casos de juízos diferentes (uma
página que bate e uma que não bate). -/
theorem o_teste_reprova_quem_so_ve_o_registro_sse (ρ : X → V) (S : Set (X × X)) :
    (∀ I : X × X → Bool, PagouSo (Prod.snd : X × X → X) I → ¬ ImprimeEm (confereB ρ) I S) ↔
      ∃ p ∈ S, ∃ q ∈ S, p.2 = q.2 ∧ confereB ρ p ≠ confereB ρ q :=
  o_teste_reprova_todo_leitor_de_pi_sse_tem_o_par Prod.snd (confereB ρ) S

end indice

/-! ## 12. O par: a assinatura inscrita e o sinal que a leva

Leitura da teoria: a resposta técnica pode estar em um resumo do sinal que permita compará-lo com ele mesmo em cópia e
saber se é cópia ou imposição. Lê-se o par: a assinatura inscrita na origem é o NOME, e a assinatura levada junto dele é o VERBO.

O que o kernel tem para essa leitura (lido por busca direta; estrutura, não identificação): `Identidade.Nome`
é uma projeção com dois campos, `reflexo` e `releitura`; `ConjugateAct` guarda no cabeçalho
“1_abs = 0_abs se não há fractalização; fractalizado = J = 1-em-nós. J = Verbo Vivo.”;
`TGLExt.the_reading_fixes_the_code` (no arquivo `TheImportedExpectation`) é o Verbo(Nome) = Nome; `Psibit.the_pair_is_necessary_and_sufficient`
prova que o par é necessário e suficiente para ler (lá o par é Palavra e Verbo, e o próprio Psibit os diz
homônimos do Verbo em ato e do par J/K; este arquivo não junta Palavra e Nome por conta própria); e `ForbiddenBoundary` chama o pai da mentira de nome próprio sem verbo. Lei da teoria: o nome é a referência do ato e o verbo a leitura que conjuga a referência em verdade.

Dicionário desta seção (escolha deste arquivo): um pacote é um par (assinatura `n`, sinal `x`);
a assinatura é o que a origem inscreveu; o sinal é o que a leva; a releitura no destino é `ρ`. O pacote é legítimo
quando a releitura do sinal devolve a assinatura inscrita.

O que fica provado:

1. `o_emitido_e_legitimo`; a cópia por um copiador mantém o pacote legítimo (`a_copia_mantem_o_pacote_legitimo`), e
   também a outra forma de mesmo sentido; o sinal de outro sentido sob a mesma assinatura não é legítimo
   (`a_imposicao_nao_e_legitima`). O primeiro e os dois últimos são por definição: a imposição, como definida aqui, é
   o sinal de outro sentido sob a assinatura inscrita.
2. **Sem o par não há juízo**: só pela assinatura ninguém julga (`so_pela_assinatura_ninguem_julga`), e só pelo
   sinal ninguém julga (`so_pelo_sinal_ninguem_julga`), quando a palavra tem dois sentidos. É o fato da seção 11 no
   vocabulário do pacote.
3. `bate_sse_legitimo_sob_a_assinatura_do_registro`: o registro da seção 11 só entra no juízo pela sua assinatura, o
   sentido lido dele (por definição).
4. **Qual resumo serve** (`um_resumo_julga_sse_separa_os_sentidos`): um resumo `h` do registro permite julgar se
   a página bate com ele se e somente se registros de mesmo resumo têm o mesmo sentido. O próprio sentido serve
   (`o_sentido_e_resumo_que_julga`); um resumo que confunde dois sentidos não serve
   (`resumo_que_confunde_sentidos_nao_julga`).

O que NÃO se afirma: que a assinatura de um sinal (quando realizada por um resumo de tamanho fixo, como um hash; no tipo, `ρ : X → V` tem codomínio arbitrário) seja um resumo que serve
para o SENTIDO de um texto; qual lado do par é o Nome (aqui `ρ r`
chama-se assinatura, e Nome fica para o objeto do kernel das seções 8 e 9); quem é o Verbo no par (pela letra, a
assinatura levada junto é o Verbo; cabem ao menos três leituras: a assinatura enquanto levada, o sinal que a leva, a
releitura no destino; a escolha não é termo deste arquivo); nenhuma regra de veredito. O item 4 trata de informação, não de cálculo: não
diz que o juiz seja computável a partir do resumo, nem que comparar o resumo da página com o do registro julgue
(seção 14). Tudo aqui é o teorema do par da seção 2 aplicado ao pacote (assinatura, sinal). -/

section par

variable {X V : Type}

/-- O pacote (assinatura inscrita, sinal que a leva) é legítimo quando a releitura do sinal devolve a assinatura. -/
def Legitimo (ρ : X → V) (p : V × X) : Prop := ρ p.2 = p.1

/-- A emissão: a origem inscreve no pacote a leitura do próprio sinal. -/
def emitir (ρ : X → V) (x : X) : V × X := (ρ x, x)

/-- O pacote emitido é legítimo. (Por definição.) -/
theorem o_emitido_e_legitimo (ρ : X → V) (x : X) : Legitimo ρ (emitir ρ x) := rfl

/-- A cópia do sinal por um copiador mantém o pacote legítimo. Só usa que a reprodução guarda o sentido: vale para
toda reprodução que imprime. -/
theorem a_copia_mantem_o_pacote_legitimo {ρ : X → V} {R : X → X} (h : Copiador ρ R) (p : V × X)
    (hp : Legitimo ρ p) : Legitimo ρ (p.1, R p.2) := by
  show ρ (R p.2) = p.1
  rw [h.imprime]
  exact hp

/-- Outra forma, mesmo sentido: o pacote continua legítimo. (Por definição: a conclusão é a hipótese.) -/
theorem outra_forma_de_mesmo_sentido_e_legitima (ρ : X → V) (x x' : X) (h : ρ x' = ρ x) :
    Legitimo ρ (ρ x, x') := h

/-- A imposição, como definida aqui (sinal de outro sentido sob a assinatura inscrita), não é legítima: é a
definição. -/
theorem a_imposicao_nao_e_legitima (ρ : X → V) (x x' : X) (h : ρ x' ≠ ρ x) :
    ¬ Legitimo ρ (ρ x, x') := h

/-- **SEM O PAR NÃO HÁ JUÍZO (i).** Se a palavra tem dois sentidos, ninguém julga a legitimidade do pacote só pela
assinatura. É o fato da seção 11 no vocabulário do pacote. -/
theorem so_pela_assinatura_ninguem_julga (ρ : X → V) (h2 : ∃ a b, ρ a ≠ ρ b) :
    ¬ ∃ f : V → Prop, ∀ p : V × X, f p.1 ↔ Legitimo ρ p := by
  rintro ⟨f, hf⟩
  obtain ⟨a, b, hab⟩ := h2
  have h1 : f (ρ a) := (hf (ρ a, a)).mpr rfl
  have h3 : ρ b = ρ a := (hf (ρ a, b)).mp h1
  exact hab h3.symm

/-- **SEM O PAR NÃO HÁ JUÍZO (ii).** Se a palavra tem dois sentidos, ninguém julga a legitimidade do pacote só pelo
sinal. É o fato da seção 11 no vocabulário do pacote. -/
theorem so_pelo_sinal_ninguem_julga (ρ : X → V) (h2 : ∃ a b, ρ a ≠ ρ b) :
    ¬ ∃ g : X → Prop, ∀ p : V × X, g p.2 ↔ Legitimo ρ p := by
  rintro ⟨g, hg⟩
  obtain ⟨a, b, hab⟩ := h2
  have h1 : g a := (hg (ρ a, a)).mpr rfl
  have h3 : ρ a = ρ b := (hg (ρ b, a)).mp h1
  exact hab h3

/-- O registro da seção 11 só entra no juízo pela sua assinatura (o sentido lido dele, `ρ r`): a página bate com o
registro se e somente se o pacote (assinatura do registro, página) é legítimo. Por definição. -/
theorem bate_sse_legitimo_sob_a_assinatura_do_registro (ρ : X → V) (x r : X) :
    Bate ρ x r ↔ Legitimo ρ (ρ r, x) := Iff.rfl

/-- **QUAL RESUMO SERVE.** Um resumo `h` do registro permite julgar se a página bate com ele se e somente se `h`
separa os sentidos: registros de mesmo resumo têm o mesmo sentido. -/
theorem um_resumo_julga_sse_separa_os_sentidos {H : Type} (ρ : X → V) (h : X → H) :
    (∃ J : H → X → Prop, ∀ x r, J (h r) x ↔ Bate ρ x r) ↔ (∀ r r', h r = h r' → ρ r = ρ r') := by
  constructor
  · rintro ⟨J, hJ⟩ r r' hrr
    have h1 : J (h r) r := (hJ r r).mpr rfl
    rw [hrr] at h1
    exact (hJ r r').mp h1
  · intro hsep
    refine ⟨fun k x => ∃ r, h r = k ∧ ρ x = ρ r, fun x r => ⟨?_, fun hb => ⟨r, rfl, hb⟩⟩⟩
    rintro ⟨r', hr', hx⟩
    show ρ x = ρ r
    rw [hx, hsep r' r hr']

/-- O próprio sentido é um resumo que serve. -/
theorem o_sentido_e_resumo_que_julga (ρ : X → V) :
    ∃ J : V → X → Prop, ∀ x r, J (ρ r) x ↔ Bate ρ x r :=
  (um_resumo_julga_sse_separa_os_sentidos ρ ρ).mpr (fun _ _ h => h)

/-- Contrapositiva da ida: um resumo que confunde dois registros de sentidos diferentes não serve. -/
theorem resumo_que_confunde_sentidos_nao_julga {H : Type} (ρ : X → V) (h : X → H)
    (hc : ∃ r r', h r = h r' ∧ ρ r ≠ ρ r') :
    ¬ ∃ J : H → X → Prop, ∀ x r, J (h r) x ↔ Bate ρ x r := by
  intro hJ
  obtain ⟨r, r', hrr, hne⟩ := hc
  exact hne ((um_resumo_julga_sse_separa_os_sentidos ρ h).mp hJ r r' hrr)

end par

/-! ## 13. O grupo de quatro casos: um lado só acerta exatamente a metade

Os quatro casos do grupo: a página `a` ou `b` contra o registro `a` ou `b`, com `ρ a ≠ ρ b`. A contagem
está formalizada para esta lista simétrica (as mesmas duas entradas servem de página e de registro). Com quatro
textos de sentidos correspondentes, cada linha e cada coluna do quadro tem um sim e um não, e o mesmo
argumento dá a mesma contagem: a seção 14 modela os quatro textos, mas a contagem de dois em quatro para eles não está
escrita como termo. A resposta
certa é `confereB ρ` (seção 11). A conta: o juiz que só vê a página dá a mesma resposta aos dois casos da mesma página, e esses
dois casos têm respostas certas opostas; logo acerta exatamente um de cada dois. O mesmo para quem só vê o registro.

**Para que serve.** (i) Na lista simétrica o termo dá 0,50 (duas respostas certas em quatro) para todo juiz de um lado só
que não sorteia; não é resultado de simulação. Para quatro textos com estes sentidos, a mesma contagem por
linha e por coluna dá 0,50. (ii) Dá o recíproco que faltava à seção 11: quem acerta os quatro casos não é
função só da página nem só do registro.

**O que não diz.** Vale para o juiz que não sorteia. Não diz que usar os dois lados é ler o SENTIDO: um juiz que casa letra com
letra também usa os dois lados, e nenhum teorema o barra: o material de um teste tem de medir esse risco pelo
mesmo corte do teste. A metade daqui e a face de
meio do kernel (`AEscala.cada_face_pesa_meio`; `TestemunhaEstatica.the_individual_does_not_echo`) são vizinhas de FORMA: nenhum
lema as liga, e este arquivo não as identifica.
-/

section metade

variable {X V : Type}

/-- Os quatro casos do grupo: (página, registro). -/
def casosDoGrupo (a b : X) : List (X × X) := [(a, a), (a, b), (b, a), (b, b)]

/-- Quantos casos da lista o juiz `I` acerta (a resposta certa é `confereB ρ`). -/
noncomputable def acertos (ρ : X → V) (I : X × X → Bool) (L : List (X × X)) : ℕ :=
  L.countP (fun p => I p == confereB ρ p)

/-- A página contra o registro dela mesma: bate. -/
theorem confereB_mesmo (ρ : X → V) (a : X) : confereB ρ (a, a) = true :=
  (confereB_sim_sse ρ (a, a)).mpr (show ρ a = ρ a from rfl)

/-- A página contra um registro de outro sentido: não bate. -/
theorem confereB_outro (ρ : X → V) (a b : X) (hab : ρ a ≠ ρ b) : confereB ρ (a, b) = false := by
  cases h : confereB ρ (a, b) with
  | false => rfl
  | true => exact absurd ((confereB_sim_sse ρ (a, b)).mp h) hab

/-- ★ **UM LADO SÓ ACERTA EXATAMENTE A METADE (a página).** No grupo de dois sentidos, todo juiz cuja resposta só depende da
página acerta exatamente dois dos quatro casos. -/
theorem quem_so_ve_a_pagina_acerta_exatamente_a_metade (ρ : X → V) (a b : X) (hab : ρ a ≠ ρ b)
    (I : X × X → Bool) (hI : PagouSo (Prod.fst : X × X → X) I) :
    acertos ρ I (casosDoGrupo a b) = 2 := by
  have e1 : I (a, a) = I (a, b) := hI (a, a) (a, b) rfl
  have e2 : I (b, a) = I (b, b) := hI (b, a) (b, b) rfl
  have h11 := confereB_mesmo ρ a
  have h12 := confereB_outro ρ a b hab
  have h21 := confereB_outro ρ b a (Ne.symm hab)
  have h22 := confereB_mesmo ρ b
  unfold acertos casosDoGrupo
  simp only [List.countP_cons, List.countP_nil, h11, h12, h21, h22, e1, e2]
  cases I (a, b) <;> cases I (b, b) <;> rfl

/-- ★ **UM LADO SÓ ACERTA EXATAMENTE A METADE (o registro).** O mesmo para o juiz cuja resposta só depende do registro. -/
theorem quem_so_ve_o_registro_acerta_exatamente_a_metade (ρ : X → V) (a b : X) (hab : ρ a ≠ ρ b)
    (I : X × X → Bool) (hI : PagouSo (Prod.snd : X × X → X) I) :
    acertos ρ I (casosDoGrupo a b) = 2 := by
  have e1 : I (a, a) = I (b, a) := hI (a, a) (b, a) rfl
  have e2 : I (a, b) = I (b, b) := hI (a, b) (b, b) rfl
  have h11 := confereB_mesmo ρ a
  have h12 := confereB_outro ρ a b hab
  have h21 := confereB_outro ρ b a (Ne.symm hab)
  have h22 := confereB_mesmo ρ b
  unfold acertos casosDoGrupo
  simp only [List.countP_cons, List.countP_nil, h11, h12, h21, h22, e1, e2]
  cases I (b, a) <;> cases I (b, b) <;> rfl

/-- O juízo pelo par acerta os quatro. -/
theorem o_juizo_pelo_par_acerta_os_quatro (ρ : X → V) (a b : X) :
    acertos ρ (confereB ρ) (casosDoGrupo a b) = 4 := by
  unfold acertos casosDoGrupo
  simp

/-- **QUEM ACERTA OS QUATRO USA OS DOIS LADOS** (corolário das duas contagens da metade). No grupo de dois sentidos, o juiz que acerta os quatro casos não é função
só da página nem só do registro. -/
theorem quem_acerta_os_quatro_usa_os_dois_lados (ρ : X → V) (a b : X) (hab : ρ a ≠ ρ b)
    (I : X × X → Bool) (h4 : acertos ρ I (casosDoGrupo a b) = 4) :
    ¬ PagouSo (Prod.fst : X × X → X) I ∧ ¬ PagouSo (Prod.snd : X × X → X) I := by
  constructor
  · intro h
    have := quem_so_ve_a_pagina_acerta_exatamente_a_metade ρ a b hab I h
    omega
  · intro h
    have := quem_so_ve_o_registro_acerta_exatamente_a_metade ρ a b hab I h
    omega

/-- **CONTROLE QUE REPROVA.** Sem dois sentidos a conta não vale: se a palavra é de resposta constante, o juiz que diz sempre
“bate” (função de lado nenhum) acerta os quatro. -/
theorem sem_dois_sentidos_o_constante_acerta_os_quatro (ρ : X → V) (h : NuncaPaga ρ) (a b : X) :
    acertos ρ (fun _ => true) (casosDoGrupo a b) = 4 := by
  have hc : ∀ p : X × X, confereB ρ p = true := fun p => (confereB_sim_sse ρ p).mpr (h p.1 p.2)
  unfold acertos casosDoGrupo
  simp [hc]

end metade

/-! ## 14. A quarta casa, o registro fixo e o que comparar resumos não faz

Os dois teoremas da seção 11 cabem em TRÊS casas do grupo (as duas da primeira página e a segunda página contra o
primeiro registro). A quarta casa (os dois no segundo estado, que bate) não sai deles: ela reprova o juiz que confere
cada lado com o original e diz que bate só se os dois conferem. Esse juiz usa os dois lados e não os compara.

O que fica provado: nas três casas esse juiz passa (`nas_tres_casas_passa_quem_confere_cada_lado_com_o_original`); no
grupo inteiro nenhum juiz dessa forma passa (`no_grupo_nenhum_juiz_de_dois_selos_passa`); no grupo, quem acerta os
quatro não é função de um lado só (`no_grupo_quem_acerta_os_quatro_usa_os_dois_lados`); e, se uma marca da letra
acompanha o estado nos dois lados, o juiz que só casa a marca acerta as quatro casas
(`no_grupo_passa_quem_casa_uma_marca_da_letra`). Em resumo: os lemas da metade excluem a dependência de um único lado
para o acerto integral; a quarta casa exclui ainda a conjunção e a disjunção de dois selos separados; uma comparação
de marcas alinhadas passa. Com o registro fixo há quem
passe só pela página (`com_o_registro_fixo_ha_quem_passe_so_pela_pagina`); sem o registro, nem com o carimbo se julga
(`nem_com_o_carimbo_se_julga_sem_o_registro`); comparar resumos julga exatamente quando a igualdade dos resumos equivale à
igualdade dos sentidos (`comparar_resumos_julga_sse_o_resumo_tem_o_nucleo_do_sentido`); um resumo injetivo (o texto integral em bytes) serve como informação e
erra como comparação (`o_resumo_injetivo_serve_e_comparar_resumos_erra`). A última peça é só aritmética: a chance de
quem sorteia por um lado só fica entre 0 e 1/16 (o modelo de sorteio é hipótese de fora do Lean).

O que NÃO se afirma: que usar os dois lados seja ler o sentido; nenhuma regra de veredito. -/

section quartaCasa

variable {X V : Type}

/-! ### Auxiliares -/

theorem confereB_sim {ρ : X → V} {p : X × X} (h : ρ p.1 = ρ p.2) : confereB ρ p = true :=
  (confereB_sim_sse ρ p).mpr h

theorem confereB_nao {ρ : X → V} {p : X × X} (h : ρ p.1 ≠ ρ p.2) : confereB ρ p = false := by
  cases hb : confereB ρ p with
  | false => rfl
  | true => exact absurd ((confereB_sim_sse ρ p).mp hb) h

/-- O grupo 2 × 2: duas páginas e dois assentos, as quatro combinações. -/
def grupo (x0 x1 r0 r1 : X) : Set (X × X) :=
  {p | (p.1 = x0 ∨ p.1 = x1) ∧ (p.2 = r0 ∨ p.2 = r1)}

/-- Três casas só: falta a casa (página mexida, assento mexido). -/
def tresCasas (x0 x1 r0 r1 : X) : Set (X × X) :=
  {p | p = (x0, r0) ∨ p = (x0, r1) ∨ p = (x1, r0)}

theorem mem_grupo {x0 x1 r0 r1 : X} {p : X × X} :
    p ∈ grupo x0 x1 r0 r1 ↔ ((p.1 = x0 ∨ p.1 = x1) ∧ (p.2 = r0 ∨ p.2 = r1)) := Iff.rfl

theorem mem_tresCasas {x0 x1 r0 r1 : X} {p : X × X} :
    p ∈ tresCasas x0 x1 r0 r1 ↔ (p = (x0, r0) ∨ p = (x0, r1) ∨ p = (x1, r0)) := Iff.rfl

theorem tresCasas_sub_grupo (x0 x1 r0 r1 : X) : tresCasas x0 x1 r0 r1 ⊆ grupo x0 x1 r0 r1 := by
  intro p hp
  rcases mem_tresCasas.mp hp with rfl | rfl | rfl
  · exact mem_grupo.mpr ⟨Or.inl rfl, Or.inl rfl⟩
  · exact mem_grupo.mpr ⟨Or.inl rfl, Or.inr rfl⟩
  · exact mem_grupo.mpr ⟨Or.inr rfl, Or.inl rfl⟩

section doisPorDois

variable (ρ : X → V) {x0 x1 r0 r1 : X}

/-! ### Os dois pares cabem em três casas -/

/-- O par contra quem só vê a página: a mesma página `x0` diante de `r0` (bate) e de `r1` (não bate). -/
theorem tres_casas_trazem_o_par_da_pagina (h0 : ρ x0 = ρ r0) (h1 : ρ x1 = ρ r1) (hne : ρ x0 ≠ ρ x1) :
    ∃ p ∈ tresCasas x0 x1 r0 r1, ∃ q ∈ tresCasas x0 x1 r0 r1,
      p.1 = q.1 ∧ confereB ρ p ≠ confereB ρ q := by
  refine ⟨(x0, r0), mem_tresCasas.mpr (Or.inl rfl), (x0, r1), mem_tresCasas.mpr (Or.inr (Or.inl rfl)),
    rfl, ?_⟩
  rw [confereB_sim (p := (x0, r0)) h0,
    confereB_nao (p := (x0, r1)) (fun h => hne (h.trans h1.symm))]
  decide

/-- O par contra quem só vê o registro: o mesmo registro `r0` diante de `x0` (bate) e de `x1` (não bate). -/
theorem tres_casas_trazem_o_par_do_registro (h0 : ρ x0 = ρ r0) (hne : ρ x0 ≠ ρ x1) :
    ∃ p ∈ tresCasas x0 x1 r0 r1, ∃ q ∈ tresCasas x0 x1 r0 r1,
      p.2 = q.2 ∧ confereB ρ p ≠ confereB ρ q := by
  refine ⟨(x0, r0), mem_tresCasas.mpr (Or.inl rfl), (x1, r0), mem_tresCasas.mpr (Or.inr (Or.inr rfl)),
    rfl, ?_⟩
  rw [confereB_sim (p := (x0, r0)) h0,
    confereB_nao (p := (x1, r0)) (fun h => hne (h0.trans h.symm))]
  decide

/-- Já nas três casas, quem acerta tudo não é função só da página nem só do registro. -/
theorem nas_tres_casas_quem_acerta_usa_os_dois_lados (h0 : ρ x0 = ρ r0) (h1 : ρ x1 = ρ r1)
    (hne : ρ x0 ≠ ρ x1) (I : X × X → Bool)
    (hI : ImprimeEm (confereB ρ) I (tresCasas x0 x1 r0 r1)) :
    ¬ PagouSo (Prod.fst : X × X → X) I ∧ ¬ PagouSo (Prod.snd : X × X → X) I := by
  constructor
  · intro hp
    exact (o_teste_reprova_quem_so_ve_a_pagina_sse ρ (tresCasas x0 x1 r0 r1)).mpr
      (tres_casas_trazem_o_par_da_pagina ρ h0 h1 hne) I hp hI
  · intro hp
    exact (o_teste_reprova_quem_so_ve_o_registro_sse ρ (tresCasas x0 x1 r0 r1)).mpr
      (tres_casas_trazem_o_par_do_registro ρ h0 hne) I hp hI

/-- NO GRUPO 2 × 2, QUEM ACERTA OS QUATRO NÃO É FUNÇÃO SÓ DA PÁGINA NEM SÓ DO REGISTRO. Corolário dos dois
teoremas da seção 11; juiz que não sorteia; tudo ou nada. -/
theorem no_grupo_quem_acerta_os_quatro_usa_os_dois_lados (h0 : ρ x0 = ρ r0) (h1 : ρ x1 = ρ r1)
    (hne : ρ x0 ≠ ρ x1) (I : X × X → Bool)
    (hI : ImprimeEm (confereB ρ) I (grupo x0 x1 r0 r1)) :
    ¬ PagouSo (Prod.fst : X × X → X) I ∧ ¬ PagouSo (Prod.snd : X × X → X) I :=
  nas_tres_casas_quem_acerta_usa_os_dois_lados ρ h0 h1 hne I
    (fun p hp => hI p (tresCasas_sub_grupo x0 x1 r0 r1 hp))

/-! ### O que a quarta casa reprova -/

open Classical in
/-- ★ **AS TRÊS CASAS NÃO BASTAM.** Nelas passa um juiz que não compara os dois lados: confere a página com o
original (`x0`), confere o assento com o original, e diz que bate quando os dois conferem. Usa os dois lados e não
julga pelo par. -/
theorem nas_tres_casas_passa_quem_confere_cada_lado_com_o_original (h0 : ρ x0 = ρ r0)
    (h1 : ρ x1 = ρ r1) (hne : ρ x0 ≠ ρ x1) :
    ∃ f g : X → Bool,
      ImprimeEm (confereB ρ) (fun p : X × X => f p.1 && g p.2) (tresCasas x0 x1 r0 r1) := by
  refine ⟨fun x => decide (ρ x = ρ x0), fun r => decide (ρ r = ρ x0), ?_⟩
  intro p hp
  rcases mem_tresCasas.mp hp with rfl | rfl | rfl
  · have hc : confereB ρ (x0, r0) = true := confereB_sim (p := (x0, r0)) h0
    simp [hc, h0.symm]
  · have hc : confereB ρ (x0, r1) = false :=
      confereB_nao (p := (x0, r1)) (fun h => hne (h.trans h1.symm))
    have hn : ¬ ρ r1 = ρ x0 := fun h => hne (h.symm.trans h1.symm)
    simp [hc, hn]
  · have hc : confereB ρ (x1, r0) = false :=
      confereB_nao (p := (x1, r0)) (fun h => hne (h0.trans h.symm))
    have hn : ¬ ρ x1 = ρ x0 := fun h => hne h.symm
    simp [hc, hn]

/-- ★ **A QUARTA CASA.** No grupo inteiro nenhum juiz da forma “a página confere E o assento confere” passa,
sejam quais forem as duas conferências: a casa (página mexida, assento mexido) bate, e esse juiz não a aceita sem
aceitar também uma casa que não bate. -/
theorem no_grupo_nenhum_juiz_de_dois_selos_passa (h0 : ρ x0 = ρ r0) (h1 : ρ x1 = ρ r1)
    (hne : ρ x0 ≠ ρ x1) (f g : X → Bool) :
    ¬ ImprimeEm (confereB ρ) (fun p : X × X => f p.1 && g p.2) (grupo x0 x1 r0 r1) := by
  intro h
  have e00 : (f x0 && g r0) = true := by
    have e := h (x0, r0) (mem_grupo.mpr ⟨Or.inl rfl, Or.inl rfl⟩)
    rw [confereB_sim (p := (x0, r0)) h0] at e
    exact e
  have e11 : (f x1 && g r1) = true := by
    have e := h (x1, r1) (mem_grupo.mpr ⟨Or.inr rfl, Or.inr rfl⟩)
    rw [confereB_sim (p := (x1, r1)) h1] at e
    exact e
  have e01 : (f x0 && g r1) = false := by
    have e := h (x0, r1) (mem_grupo.mpr ⟨Or.inl rfl, Or.inr rfl⟩)
    rw [confereB_nao (p := (x0, r1)) (fun hh => hne (hh.trans h1.symm))] at e
    exact e
  revert e00 e11 e01
  cases f x0 <;> cases g r0 <;> cases f x1 <;> cases g r1 <;> decide

/-- A mesma coisa para a forma “a página confere OU o assento confere”. -/
theorem no_grupo_nenhum_juiz_de_um_selo_ou_outro_passa (h0 : ρ x0 = ρ r0) (h1 : ρ x1 = ρ r1)
    (hne : ρ x0 ≠ ρ x1) (f g : X → Bool) :
    ¬ ImprimeEm (confereB ρ) (fun p : X × X => f p.1 || g p.2) (grupo x0 x1 r0 r1) := by
  intro h
  have e00 : (f x0 || g r0) = true := by
    have e := h (x0, r0) (mem_grupo.mpr ⟨Or.inl rfl, Or.inl rfl⟩)
    rw [confereB_sim (p := (x0, r0)) h0] at e
    exact e
  have e01 : (f x0 || g r1) = false := by
    have e := h (x0, r1) (mem_grupo.mpr ⟨Or.inl rfl, Or.inr rfl⟩)
    rw [confereB_nao (p := (x0, r1)) (fun hh => hne (hh.trans h1.symm))] at e
    exact e
  have e10 : (f x1 || g r0) = false := by
    have e := h (x1, r0) (mem_grupo.mpr ⟨Or.inr rfl, Or.inl rfl⟩)
    rw [confereB_nao (p := (x1, r0)) (fun hh => hne (h0.trans hh.symm))] at e
    exact e
  revert e00 e01 e10
  cases f x0 <;> cases g r0 <;> cases f x1 <;> cases g r1 <;> decide

/-! ### O juiz que usa os dois lados sem ler o sentido -/

/-- ★ **CASAR LETRA COM LETRA PASSA, SE A LETRA DENUNCIA.** Seja `s` uma marca qualquer da letra (por exemplo, ter
ou não palavra de negação na afirmação-alvo). Se, dentro do grupo, a marca acompanha o estado nos dois lados
(`s x0 = s r0`, `s x1 = s r1`, `s x0 ≠ s x1`), o juiz que só compara a marca da página com a marca do assento acerta
as quatro casas. Ele usa os dois lados e não lê sentido nenhum. Nenhum teorema deste arquivo o reprova: o material
de um teste tem de medir esse risco pelo corte do teste. -/
theorem no_grupo_passa_quem_casa_uma_marca_da_letra (s : X → Bool) (h0 : ρ x0 = ρ r0)
    (h1 : ρ x1 = ρ r1) (hne : ρ x0 ≠ ρ x1) (hs0 : s x0 = s r0) (hs1 : s x1 = s r1)
    (hsne : s x0 ≠ s x1) :
    ImprimeEm (confereB ρ) (fun p : X × X => s p.1 == s p.2) (grupo x0 x1 r0 r1) := by
  have c00 : (s x0 == s r0) = confereB ρ (x0, r0) := by
    rw [confereB_sim (p := (x0, r0)) h0, hs0]
    cases s r0 <;> decide
  have c11 : (s x1 == s r1) = confereB ρ (x1, r1) := by
    rw [confereB_sim (p := (x1, r1)) h1, hs1]
    cases s r1 <;> decide
  have c01 : (s x0 == s r1) = confereB ρ (x0, r1) := by
    rw [confereB_nao (p := (x0, r1)) (fun hh => hne (hh.trans h1.symm)), ← hs1]
    revert hsne
    cases s x0 <;> cases s x1 <;> decide
  have c10 : (s x1 == s r0) = confereB ρ (x1, r0) := by
    rw [confereB_nao (p := (x1, r0)) (fun hh => hne (h0.trans hh.symm)), ← hs0]
    revert hsne
    cases s x0 <;> cases s x1 <;> decide
  rintro ⟨a, b⟩ hp
  obtain ⟨ha, hb⟩ := mem_grupo.mp hp
  have ha' : a = x0 ∨ a = x1 := ha
  have hb' : b = r0 ∨ b = r1 := hb
  rcases ha' with ha' | ha' <;> rcases hb' with hb' | hb' <;> rw [ha', hb']
  · exact c00
  · exact c01
  · exact c10
  · exact c11

end doisPorDois

/-! ### O braço do carimbo: com o registro fixo, e sem o registro -/

/-- **COM O REGISTRO FIXO HÁ QUEM PASSE SÓ PELA PÁGINA.** Se todos os casos de um conjunto têm o mesmo registro,
existe juiz que só vê a página e acerta todos. (Instância de `sem_o_par_ha_quem_passe_pagando_so_pi`.) É o limite
do caso em que o índice fica intacto. -/
theorem com_o_registro_fixo_ha_quem_passe_so_pela_pagina (ρ : X → V) (S : Set (X × X)) (r0 : X)
    (hS : ∀ p ∈ S, p.2 = r0) :
    ∃ I : X × X → Bool, PagouSo (Prod.fst : X × X → X) I ∧ ImprimeEm (confereB ρ) I S := by
  refine sem_o_par_ha_quem_passe_pagando_so_pi Prod.fst (confereB ρ) S ?_
  intro p hp q hq h
  have hpq : p = q := Prod.ext h ((hS p hp).trans (hS q hq).symm)
  rw [hpq]

/-- **NEM COM O CARIMBO SE JULGA SEM O REGISTRO.** Se a palavra tem dois sentidos, nenhum juízo feito sobre o que a
página leva (uma assinatura declarada `n` e o corpo `x`) decide, para todo registro, se o corpo bate com ele.
(Instância de `sem_o_registro_ninguem_julga_se_bate`.) -/
theorem nem_com_o_carimbo_se_julga_sem_o_registro (ρ : X → V) (h2 : ∃ a b, ρ a ≠ ρ b) :
    ¬ ∃ J : V → X → Prop, ∀ (n : V) (x r : X), J n x ↔ Bate ρ x r := by
  rintro ⟨J, hJ⟩
  obtain ⟨a, b, hab⟩ := h2
  exact sem_o_registro_ninguem_julga_se_bate ρ ⟨a, b, hab⟩ ⟨J (ρ a), fun x r => hJ (ρ a) x r⟩

/-! ### Informação do resumo não é comparação de resumos -/

/-- Comparar o resumo da página com o resumo do registro julga se e somente se o resumo separa os sentidos E é
igual em textos de mesmo sentido (tem exatamente o núcleo do sentido). A primeira metade é a condição do teorema
`um_resumo_julga_sse_separa_os_sentidos`; a segunda ele não pede. -/
theorem comparar_resumos_julga_sse_o_resumo_tem_o_nucleo_do_sentido {H : Type} (ρ : X → V)
    (h : X → H) :
    (∀ x r, (h x = h r ↔ Bate ρ x r)) ↔
      ((∀ a b, h a = h b → ρ a = ρ b) ∧ (∀ a b, ρ a = ρ b → h a = h b)) := by
  constructor
  · intro hc
    exact ⟨fun a b hab => (hc a b).mp hab, fun a b hab => (hc a b).mpr hab⟩
  · rintro ⟨hsep, hcla⟩ x r
    exact ⟨hsep x r, hcla x r⟩

/-- **CONTROLE.** Um resumo injetivo (por exemplo o texto integral em bytes sob uma codificação injetiva; este termo não
verifica a injetividade de um hash de tamanho fixo) SERVE no sentido do teorema do resumo da seção 12 (a
informação basta a um juiz que ainda lê a página inteira) e, no entanto, comparar resumos ERRA em toda cópia de
outra letra (`x ≠ r` com o mesmo sentido): o erro exige dois textos distintos com o mesmo sentido. -/
theorem o_resumo_injetivo_serve_e_comparar_resumos_erra {H : Type} (ρ : X → V) (h : X → H)
    (hinj : Function.Injective h) (x r : X) (hxr : x ≠ r) (hs : ρ x = ρ r) :
    (∃ J : H → X → Prop, ∀ x r, J (h r) x ↔ Bate ρ x r) ∧ ¬ (h x = h r ↔ Bate ρ x r) := by
  refine ⟨(um_resumo_julga_sse_separa_os_sentidos ρ h).mpr (fun a b hab => by rw [hinj hab]), ?_⟩
  intro hiff
  exact hxr (hinj (hiff.mpr hs))

/-! ### O juiz que sorteia por um lado só (só a aritmética) -/

/-- Se um juiz só vê a página e sorteia, com probabilidade `p` de dizer “bate” diante de `x0` e `q` diante de `x1`,
e os quatro sorteios são independentes, a chance de acertar as quatro casas é `p(1−p)·q(1−q)`, que fica entre 0 e
1/16. Aqui só a desigualdade; o modelo de sorteio é hipótese de fora do Lean. -/
theorem um_lado_so_sorteando_fica_em_um_dezesseis_avos (p q : ℝ) (hp0 : 0 ≤ p) (hp1 : p ≤ 1)
    (hq0 : 0 ≤ q) (hq1 : q ≤ 1) :
    0 ≤ p * (1 - p) * (q * (1 - q)) ∧ p * (1 - p) * (q * (1 - q)) ≤ 1 / 16 := by
  have h1 : p * (1 - p) ≤ 1 / 4 := by nlinarith [sq_nonneg (p - 1 / 2)]
  have h2 : q * (1 - q) ≤ 1 / 4 := by nlinarith [sq_nonneg (q - 1 / 2)]
  have h3 : 0 ≤ p * (1 - p) := mul_nonneg hp0 (by linarith)
  have h4 : 0 ≤ q * (1 - q) := mul_nonneg hq0 (by linarith)
  refine ⟨mul_nonneg h3 h4, ?_⟩
  calc p * (1 - p) * (q * (1 - q)) ≤ 1 / 4 * (1 / 4) := mul_le_mul h1 h2 h4 (by norm_num)
    _ = 1 / 16 := by norm_num

end quartaCasa




end TGLExt.CopiadorEImpostor
