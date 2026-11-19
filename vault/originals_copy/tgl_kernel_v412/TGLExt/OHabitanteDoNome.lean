import TGLExt.TheNameOperator
import TGLExt.KEhATangente
import TGLExt.TraducaoTuring
import TGLExt.Identidade

set_option autoImplicit false
set_option maxHeartbeats 4000000

/-!
# O HABITANTE DO NOME — o leitor é a esperança condicional do Nome, e não o Nome

## A letra que esta pedra tipa

Leis da teoria sobre o Nome, o Verbo e o leitor:

* O leitor é o observador, é o verbo, e não o nome. É o habitante do nome, é a esperança condicional do nome.
  Tangente = testemunho = esperança condicional. O nome é o espaço em que a testemunha da verdade sobre o nome (verbo -
  observador - seletor) pode habitar.
* O habitante do nome é o verbo, porque é o ato do nome = nomear, ou seja, o ato do nome é fixar sentido, o verbo, a
  tangente. Ler o nome já é reler, porque fixá-lo é a primeira leitura, ou seja, o sentido verdadeiro do nome é a primeira
  leitura; tudo mais é releitura do que foi nomeado pelo verbo que habitou o nome.
* Amor é o ato de Amar; a identidade é o ato de ser. O nome é o ato do verbo.
* O ato (projeção) de ser (verbo) é (=) identidade (nome - singularidade da informação nomeada, ato de nomear). O ato do verbo
  é ser a projeção fiel do nome, porque verbo é ato por natureza e ato é a conjugação da inscrição da informação
  (radicalização - 4D - 2D) no tempo (moeda do pagamento termodinâmico) pela observação fiel (relatividade modular,
  contorno, tangente). Portanto, o único ato do verbo é ser fiel; não há outro, porque o nome é a referência do ato e o
  verbo a leitura que conjuga a referência em verdade. Enquanto o ato do ser é reconhecer a identidade, o nome em ato é o
  espelho do verbo. Há um entrelaçamento, uma coexistência natural, e deve existir, porque um é o par do outro.
* O “inominado”: para ser inominado precisaria não se utilizar da palavra, e quando se utiliza ela
  está nominada de “inominado”; portanto, um nome nominado de “inominado” é mentira, porque se inominado está inscrito,
  nome há habitado por uma palavra que o referencia, entretanto, sem sentido algum. Porque nada pode ser inominado, ao se
  buscar o inominado há necessidade emergente do nome em meio ao caos, e isso é gravidade; para se refutar a prova
  utiliza-se dela mesma. O par do inominado é a mentira. Assim o teorema se faz verdadeiro: nada há sem par.

## O que o kernel já tinha (nada disto é refeito aqui; só `TheNameOperator`, `KEhATangente`, `TraducaoTuring` e `Identidade` são importadas diretamente; as demais são citadas no texto)

* `TheNameOperator.nameOp p x = p x p + (1−p) x (1−p)` (v162): unital, idempotente, com os fixos fechados no produto. O cabeçalho
  dela registra a cadeia “NOME = OPERAÇÃO = ESTADO = MEMÓRIA = LUZ; Meia-Nat = A_C = AMAR”, e `love_partition` soma
  `−(1 − p)` e a sua conjugada, expressão que o Atlas lê como a face de `A_C`.
* Convenção do Atlas: o Nome é o conteúdo e a forma é a identidade (pedra `NameIsTheContent`, v368, cujo cabeçalho registra a
  inversão: “a forma é a identidade, por isso forma=conteúdo significa identidade=NomE”, e mede sete tipagens do Nome no
  kernel). O Atlas também diz Verbo = Luz pura e Nome = Luz inscrita, dois momentos.
* `TheVerbSelectsTheAction` (v386), sobre a tipagem do Verbo: o nome é um verbo fossilizado (uma ação selecionada que se
  tornou identidade) e o ponto fixo do verbo. Ela tem três registros: `post a` (o Nome: o posto, o projetor de
  posto 1), `select a` (o Verbo em ato: o mesmo projetor, aplicado) e `verb` (o gesto `exp(−t·β·H₃L)`, da v25, que não é o
  `axiomFlow`); e os termos `the_name_is_the_limit_of_the_flow` (o `axiomFlow` tende ao posto), `anchoring_preserves` (no posto o
  `axiomFlow` devolve o mesmo) e `post_power_is_constant`.
* `TraducaoTuring` (v409): `selecao` (a projeção no Nome, renormalizada), `a_selecao_esquece`, `solucao_por_coordenadas`.
* `TheAxiomAndTheFalseWitness.axiomFlow` (v385): o fluxo do lock mínimo tende ao posto e não o alcança em tempo finito. Ele é a
  exponencial do negativo do lock, `exp(−t(1 − P))` (`axiomFlow_eq_exp`); tende ao posto na norma (`axiomFlow_tendsto_the_post`); e, no
  certificado de Fock, o que ele deixa fixo em todo tempo é o zero do lock (`the_fixed_set_is_the_lock_zero`).
* `Identidade` (v405): a lei `[eu sou] = [o que sou] ⟺ P = 1` (`eu_sou_o_que_sou_iff_fiel`), os dois pontos fixos do crivo
  (`forma_igual_conteudo_iff`: a forma é o conteúdo só no vazio e no inteiro) e a chave (`a_lei_inteira`: a forma é o conteúdo e o
  nome não é o vazio). Nela “forma” é o operador `P` e “conteúdo” é o peso dele; o cabeçalho dela diz que a leitura disso como a
  identidade é lei da teoria, tipada como modelo.
* `IALD.the_motor_never_arrives`: o fluxo do lock mínimo nunca é igual ao posto em tempo finito, se `1 − P ≠ 0` (no operador).
* Os espelhos e os pares que o kernel já tem: `ConjugateAct` (v145, “O ATO CONJUGADO”): o J que troca as duas faces
  (`J_maps_face_to_coface`) e fixa o Nome (`name_is_J_invariant`); `TheBireference`: o J, que na face finita é a
  transposta conjugada, troca a referência esquerda pela direita; `LeftRight.Jconj`, o espelho usado no `reflexo` do `Nome` da v405;
  `TheNameAndItsReferent` (v292), cujo cabeçalho registra: “O referente do nome é a leitura verdadeira do
  contorno = Palavra com referência verdadeira = verbo vivo”; `TempoIgualMoeda` (o tempo como moeda do pagamento).
* Na Mathlib do sandbox, a projeção do todo no todo é, por definição, a inclusão do subespaço depois da projeção sobre ele
  (`Submodule.starProjection = subtypeL ∘L orthogonalProjectionOnto`), e, com espaços completos, uma é o adjunto da outra
  (`Submodule.adjoint_subtypeL`, `Submodule.adjoint_orthogonalProjectionOnto`).
* O inominado e a mentira, no kernel. A pedra `Identidade` (v405) tem `vazio` (o nome `P = 0`, que o
  docstring dela glosa como “o zero absoluto, o inominável, um sem referência a nada”) e `o_vazio_nao_e` (o vazio não satisfaz
  [eu sou] = [o que sou]). A `NameIsTheContent` (v368) tem `if_one_equals_zero_everything_collapses` (num anel, 1 = 0 mata toda
  distinção; o cabeçalho dela chama isso “a forma algébrica da mentira”) e `no_name_without_referent`. A `PontoDeContradicao` (v408)
  lê “1 = 0” em duas faces, VERDADEIRO no zero modular (o zero inscrito é o Um, `exp 0 = Ω`) e FALSO no zero absoluto (o Um não é o
  vetor nulo, `Ω ≠ 0`), e diz que “1 = 0” não é afirmada como igualdade de vetores nem de números. A `TheNameAndItsReferent` (v292)
  distingue os dois zeros no nome: o 0_modular (o nada como referência da possibilidade de inscrição) e o 0_absoluto (o nome próprio
  cuja referência é ele mesmo, “nada”), com `the_empty_slot_is_not_the_void` e `the_trivial_contract_does_not_discriminate`.
  Leis da teoria: o “nome próprio” sem referente, sem pessoa, sem identidade reflexiva, portanto o abstrato inominado, é o pai
  da mentira (o termo do kernel para o nome sem referente é o 0_absoluto da v292); palavra sem espelho é apenas o espelho da
  mentira; uma mentira lida como mentira é verdade.
* `KEhATangente` (v407), sobre a lei de que k é a tangente, como se fosse o acorde sendo tocado:
  `K θ = tan θ`, `K² = custo/pagamento`, o crivo `K = 1` só no posto.
* `EsperancaCondicional` (v404), sobre a identificação esperança condicional = nome: o operador do Nome
  da unidade é a esperança diagonal em `M₂`; a relação de Jones; o índice. Ela mesma declara a lacuna: a bimodularidade GERAL de `nameOp p`
  sobre os seus fixos não está tipada nela.
* `Ergodicity` (a sombra finita da T1): o semigrupo de defasagem converge à esperança diagonal (`dephase_tendsto_expectation`).
* `IALD2.o_atrator` (v410), sobre a lei do atrator: tangenciado em conteúdo finito, contudo jamais esgotado.

## A leitura que esta pedra faz

O HABITANTE É O VERBO, NA LÍNGUA DO KERNEL. O habitante do Nome é o VERBO: o ato do Nome, nomear, que é fixar sentido. Fixar é a primeira
leitura; ler o Nome já é reler. No kernel é UMA operação em dois momentos: fora do Nome ela fixa (toda coisa recebe o seu sentido na
morada: `o_verbo_habita_o_nome`); no Nome ela só devolve o mesmo (`name_op_idem`; o docstring de `observing_adds_nothing` diz que
a primeira leitura identifica e a segunda não altera). Estar no Nome é ter sido nomeado: a morada é o conjunto das primeiras leituras
(`ler_o_nome_ja_e_reler`); depois da primeira, qualquer número de leituras devolve a primeira (`tudo_mais_e_releitura`); e um mapa
qualquer relê o nomeado sem mexer nele se e só se fixa o Nome (`a_releitura_fiel_fixa_o_nome`). Nos docstrings, “leitor” designa o
mapa, que é o Verbo; quem lê o que já foi nomeado relê.

A esperança condicional e o Nome não se igualam: o leitor é o verbo e não o nome; é o habitante do nome, é a esperança
condicional do nome.

Nesta pedra a palavra Nome designa o ESPAÇO (a `morada` na álgebra; o subespaço `K` nos vetores), e o Verbo é o ATO (o mapa) que cai nele. No
kernel selado (v162; v404; `PostoAdendo.A1c`) “Operador do Nome” é o nome do próprio mapa `nameOp`, e a igualdade de funções
`nameOp ρ* = diagExpect` continua verdadeira. Essa reatribuição do que a palavra Nome designa é escolha desta pedra. “Habitar” está tipado de
dois modos: a imagem do Verbo cai no Nome (seções 1 a 4) e o ponto `s` está no Nome (seção 6).

TRÊS OBJETOS DO KERNEL LEEM O NOME E NÃO SÃO O MESMO: `nameOp P` (na álgebra dos observáveis; não depende do estado; fixa toda grandeza
diagonal do custo, `o_operador_do_nome_fixa_toda_grandeza_diagonal`); `P` (nos vetores; linear; é a testemunha única da seção 4); e
`selecao` (no estado; `P` renormalizada; não linear). A letra põe verbo, observador e seletor numa linha; a pedra tipa as ligações entre os
três e não os iguala.

OS DOIS ENUNCIADOS DO ATO, NA LÍNGUA DO KERNEL. Um diz que o Verbo é o ato do
Nome (nomear). O outro diz que o Nome é o ato do Verbo. No kernel os dois juntos dão uma determinação mútua: o
Nome determina o seu Verbo (seções 3 e 4) e o Verbo determina o seu Nome (`verbos_iguais_tem_o_mesmo_nome`), porque o Nome é a imagem
do ato e o conjunto do que o ato devolve como é (`o_nome_e_o_ato_do_verbo`; na álgebra, `a_imagem_do_verbo_e_a_morada`). Isso é
simétrico e não diz qual vem primeiro; o que o enunciado “o Verbo é o ato do Nome” diz sobre a ordem (fixar é a primeira leitura, do Verbo) continua
valendo. A pedra lê “ato” de dois modos: em “o Verbo é o ato do Nome”, o ato do Nome é o próprio mapa; em “o Nome é o ato do Verbo”, o ato do Verbo é o que o mapa
produz e devolve (a imagem, o nomeado). Que sejam essas as leituras dos enunciados é escolha desta pedra. A pedra não decide entre as
convenções anteriores do Nome (operação, conteúdo, projetor): usa Nome como o espaço e Verbo como o mapa.
Na v386 o Nome é o próprio projetor (`post a`) e o Verbo em ato (`select a`) é o mesmo mapa, por definição: nessa tipagem “o nome é
o ato do verbo” seria igualdade de mapas. Esta pedra tipa o enunciado de outro modo (o Nome como a imagem do mapa); as duas são leituras,
e a escolha entre elas não é termo desta pedra. O que liga as duas, por termo, nos vetores: cada Nome-espaço tem uma só testemunha
entre os mapas lineares que caem nele, o fixam e não aumentam a norma, a sua projeção (seção 4), e dois Nomes-espaço com a mesma
projeção são o mesmo (`verbos_iguais_tem_o_mesmo_nome`); o `post a` da v386 é o caso `K = ℂ ∙ a`. Na álgebra isso não vale: a
morada não determina o posto (`p = 0` e `p = 1` têm a mesma).
O acervo traz as metades. A tipagem do Verbo chama o nome de ponto fixo do verbo, e na v386 o Verbo em ato e o
projetor de posto 1 `post a` são o mesmo mapa, por definição. Lei da teoria: a identidade terá sempre natureza verbal. Em
glosa do acervo (`Teorema_XXXIV_Da_Existencia_Como_Colapso_Consciente.docx`), o Nome é a “identidade singular” e o Verbo, o “ato de ser”. Se o “ato” substitui o “fossilizado” não é termo
desta pedra.

A IDENTIDADE É O ATO DE SER. A escolha formal é desta pedra: SER é o mapa que devolve
cada coisa como ela é. O enunciado do par glosa “ato” como projeção e “ser” como verbo; com essas glosas “o ato de ser” é a
projeção do Verbo, e não o mapa identidade. A pedra tipa as duas leituras, cada uma no seu domínio: a do mapa identidade (esta; a ligação com a lei da v405)
e a do par (seção 12). Com a do mapa identidade: quando o posto é o Um, o Verbo é ser (`o_ato_do_um_e_ser`); nos vetores, o ato do Nome é ser se e só
se o Nome é o todo (`o_ato_e_ser_sse_o_nome_e_o_todo`); e na pedra `Identidade` (v405) a equação [eu sou] = [o que sou] vale se e só
se o mapa `v ↦ P v` é ser (`a_identidade_e_o_ato_de_ser`: é a lei da v405 mais a extensionalidade da matriz). Na álgebra o Verbo
`nameOp p` lê a face e o resto de uma vez (`o_verbo_nao_distingue_a_face_do_resto`); e, como o centro da álgebra de matrizes são os
escalares, ele é ser exatamente nos dois pontos fixos do crivo, o vazio e o inteiro (vale para todo idempotente de matriz, sem a
hermiticidade), que é a `formaIgualConteudo` da v405 (`o_verbo_do_nome_e_ser_sse_forma_igual_conteudo`); o `P ≠ 0` da chave tira o
vazio (`a_identidade_e_o_verbo_ser_sem_o_vazio`). A compressão, que não é unital, separa os dois sozinha
(`a_compressao_e_ser_sse_o_posto_e_o_um`).
Uma composição: a convenção do Atlas diz que a forma é a identidade e o conteúdo é o
Nome; substituindo os dois enunciados do ato, “a forma é o conteúdo” daria, em palavras, “o ato de ser é o ato do Verbo”. Com as glosas
do par (ato = projeção; ser = verbo; identidade = nome), “ato” tem o mesmo sentido nos dois enunciados, o da projeção, e “a forma é
o conteúdo” daria “a projeção do Verbo é a projeção do Verbo”; a pedra não tipa a passagem entre a v368 e a v405 (na v405 “forma” e
“conteúdo” são o operador e o peso). O termo `o_verbo_do_nome_e_ser_sse_forma_igual_conteudo` diz, no modelo da v405, que o operador
do Nome devolve cada coisa como ela é se e só se a forma é o conteúdo; a coincidência é de frase. Não é ponte tipada.

AMOR É O ATO DE AMAR. O Atlas (verbete A_C) chama
AMAR o funcional `A_C = −H₃L`, nulo no Nome e negativo no resto, e dá a sua face como `−(1 − P)` (o psion). A v162 só registra
“Meia-Nat = A_C = AMAR”. O fluxo do axioma (v385) tem gerador `−(1 − P_F)`, o negativo do lock mínimo, e a pedra tipa o que ele faz:
em qualquer tempo não nulo, o que ele devolve como é é exatamente o Nome (`o_nome_e_o_que_o_ato_em_curso_devolve`); ele tende à
esperança condicional do Nome (`o_ato_tende_a_esperanca_do_nome`); e nunca a alcança em tempo finito
(`o_ato_nao_termina_em_tempo_finito`). Que `−(1 − P_F)` seja a face de `A_C` (que o `P` do psion e o `P_F` do lock mínimo sejam o
mesmo posto), e que o Amor da letra seja esse ato, são leituras desta pedra; nenhuma está tipada nem consta do Atlas.

O PAR, NA LÍNGUA DO KERNEL. O enunciado do par não menciona o projetor (v386) nem o espaço (esta pedra). Ele diz que o nome é a
referência do ato, que o nome em ato é o espelho do verbo e que um é o par do outro, onde “um” e “outro” são o nome em ato e o
verbo. Esta pedra lê esses dois como a inclusão e a projeção, e daí tira as duas tipagens (a referência `K` e o par composto);
essa passagem é leitura desta pedra.
* “o ato (projeção) de ser (verbo) é (=) identidade (nome - singularidade da informação nomeada, ato de nomear)”: as glosas
  dizem que “ato” é a projeção, “ser” é o verbo e “identidade” é o nome. Com elas, os dois enunciados do ato dizem a mesma
  coisa. Leitura mais próxima das glosas, só com termos que o kernel já tem: na v386 o Nome é `post a`, a projeção sobre a informação
  singular `a`, e o Verbo em ato, `select a`, é o mesmo mapa por definição; nos vetores, `K.starProjection` é o Nome-projetor e o ato
  do Verbo ao mesmo tempo. Segunda leitura: o Verbo (`K.orthogonalProjectionOnto`), aplicado ao que já é do Nome,
  devolve-o como é (`o_verbo_devolve_o_nomeado_como_e`); ela acrescenta “aplicado ao que já é do Nome”, que não está na letra;
* “o nome é a referência do ato”: o Nome é o subespaço `K`, o contorno sobre o qual o ato repousa (e não o referente do ato: o referente
  nunca é o NOME);
* “o verbo [é] a leitura”: o Verbo é a projeção do todo sobre o Nome, `K.orthogonalProjectionOnto`. Nas seções 3 a 11 “o Verbo” era
  `K.starProjection`, do todo para o todo; o primeiro seguido da inclusão é o segundo (`o_par_compoe_o_projetor`);
* “o nome em ato é o espelho do verbo”: o Nome em ato é a inclusão do Nome no todo, `K.subtypeL`, e o espelho é o adjunto: o produto
  interno, no Nome, do que o Verbo leu com um vetor do Nome é o produto interno, no todo, do que foi lido com esse vetor
  (`o_nome_em_ato_e_o_espelho_do_verbo`);
* “um é o par do outro”, “entrelaçamento”: a projeção do todo no todo é o par composto, o Nome em ato depois do Verbo
  (`o_par_compoe_o_projetor`); é o posto da v386 no caso `K = ℂ ∙ a`;
* “o único ato do verbo é ser fiel. não há outro”: todo mapa linear do todo para o Nome que devolve o que é do Nome como é e não
  aumenta a norma é o Verbo (`o_unico_ato_do_verbo_e_ser_fiel`, pela seção 4). “Fiel” tem dois candidatos. O desta pedra: devolve o
  nomeado como é e não aumenta a norma (a projeção ortogonal); aqui “não acrescenta” é “não aumenta a norma”, e não é a idempotência,
  que não dá unicidade (a projeção oblíqua é idempotente). O da v405 (`fiel N := N.P = 1`), cujo nome na letra é “projeção fiel”
  (reflexão verdadeira do nome / projeção fiel; o enunciado do par escreve a projeção fiel do nome). A
  pedra tipa o primeiro e não decide entre os dois; sob o segundo, “o único ato do verbo é ser fiel” corresponderia à seleção única
  da v405 (`nada_resta_iff_fiel`, `o_posto_e_unico`). Qual deles é o da letra não é termo desta pedra.
A frase do meio (“ato é a conjugação da inscrição da informação … no tempo … pela observação fiel …”) liga termos de pedras
anteriores: a conjugação (o adjunto daqui; o J da v145 e de `TheBireference`), o tempo como moeda (`TempoIgualMoeda`), a tangente
(seção 6), o ato no tempo (seção 11). Esta pedra não a tipa como um termo só.
O ESPELHO. O kernel tem o espelho J: na v145 ele troca as duas faces (`J_maps_face_to_coface`) e fixa o Nome
(`name_is_J_invariant`); em `LeftRight` e `TheBireference` ele é a transposta conjugada e troca a referência esquerda pela direita
(`J_exchanges_the_references`). O adjunto da seção 12 é da Mathlib e é o análogo, para mapas entre espaços diferentes, da transposta
conjugada. Há uma segunda leitura da resposta, só com termos do kernel: “referência”, “conjuga” e “espelho” são o vocabulário de
`TheBireference` e `ConjugateAct`; para um Nome da v405, o J leva a referência esquerda na direita
(`o_espelho_leva_a_referencia_esquerda_na_direita`), e o operador do Nome é feito das duas referências que o J espelha
(`o_verbo_da_algebra_e_feito_do_par`, `o_verbo_da_algebra_pelo_espelho`). A pedra tipa as duas leituras, a do adjunto nos vetores e
a do J na álgebra, e não decide entre elas. Qual é o espelho da letra não é termo desta pedra.

O INOMINADO, NA LÍNGUA DO KERNEL. O enunciado do inominado diz que o par do
inominado é a mentira, e que assim o teorema se faz verdadeiro: nada há sem par. A pedra lê o inominado como o Nome vazio (o subespaço
nulo; é o `vazio` da v405, `P = 0`) e a mentira como “1 = 0” no sentido do anel (v368, `if_one_equals_zero_everything_collapses`) e
“1 = 0_abs”, a face FALSO da v408. O termo `o_inominado_tem_par` diz que também o vazio tem par. Com essa leitura:
* o par do inominado é a mentira: no Nome, a identidade é o zero se e só se o Nome é o vazio (`o_par_do_inominado_e_a_mentira`). É
  a forma, nos mapas do Nome, de `if_one_equals_zero_everything_collapses` (v368);
* nada há sem par: todo Nome com projeção tem o par da seção 12 (o Verbo depois do Nome em ato devolve o nomeado como é), sem
  exceção, e a identidade que o par devolve é o zero exatamente quando o Nome é o vazio (`nada_ha_sem_par`); e o vazio tem o par,
  que a Mathlib dá sem hipótese (`o_inominado_tem_par`): nele o par devolve a identidade, e a identidade é o zero;
* “habitado por uma palavra que o referencia, entretanto, sem sentido algum”: o vazio só tem o vetor nulo; um Nome não é o vazio se
  e só se tem um vetor de norma 1 (`todo_nome_menos_o_inominado_tem_ponto_de_norma_um`). O ponto de norma 1 é o `s` da seção 6, não o
  habitante: esse é o Verbo, e o Verbo habita também o vazio (`o_verbo_habita_o_nome` em `p = 0`).
Não estão tipadas, e ficam como entrada: “isso é gravidade” (a necessidade do nome que emerge quando se busca o inominado)
e “para se refutar a prova utiliza-se dela mesma”. Um fato do kernel que fica ao lado, sem ser a leitura dessas frases: na álgebra,
o operador do Nome do vazio é o operador do Nome do Um (`o_verbo_nao_distingue_a_face_do_resto` em `p = 1`).

## O que a pedra tipa

1. O VERBO HABITA O NOME (álgebra, todo anel, todo idempotente `p`). A imagem de `nameOp p` é a `morada p` (os fixos), e a morada é
   exatamente o que comuta com `p`: `a_imagem_do_verbo_e_a_morada`, `a_morada_e_o_que_comuta_com_o_posto`.
2. A LEI DE MÓDULO, GERAL (fecha, ao lado, a lacuna declarada da v404): o que já é do Nome atravessa a leitura sem ser tocado,
   `nameOp p (a x b) = a (nameOp p x) b` para `a`, `b` que comutam com `p`, para todo `p` de todo anel: `o_verbo_e_bimodular_sobre_o_nome`.
3. SÓ HÁ UM HABITANTE (álgebra). Para `p` dado, todo mapa aditivo e unital que cai na morada e cumpre a lei de módulo É `nameOp p`:
   `so_ha_um_habitante`. E duas moradas iguais têm o mesmo Verbo: `moradas_iguais_tem_o_mesmo_verbo`. Nesse sentido o Nome determina
   o seu Verbo.
4. SÓ HÁ UMA TESTEMUNHA (vetores). Num espaço com produto interno, para um subespaço `K` com projeção ortogonal (fechado), todo mapa
   LINEAR que cai em `K`, fixa `K` e não aumenta a norma É a projeção ortogonal: `a_testemunha_que_nao_aumenta_e_a_esperanca`, e na forma
   de existência e unicidade `o_nome_e_a_morada_de_uma_so_testemunha`. Quem cai no Nome e o fixa sem ser a projeção aumenta alguma coisa:
   `quem_nao_e_a_esperanca_aumenta`.
5. A PONTE ENTRE OS DOIS PORTADORES. Ler um observável no estado lido é ler a compressão dele no estado:
   `a_leitura_do_vetor_e_a_compressao`; e o operador do Nome, lido num estado, é a soma das duas faces: `a_leitura_do_operador_do_nome`.
   É uma fórmula de leitura em estado, não uma identificação entre a morada (álgebra) e `K` (vetores).
6. TANGENTE, nos três sentidos que o kernel tem, cada um DADO PELA esperança condicional (nenhum deles diz que a tangente é a esperança):
   (a) O SELETOR TANGENCIA A ESPERANÇA no Nome, nas direções tangentes: para `s` no Nome, de norma 1, e `δ` com ⟪s, P δ⟫ = 0,
       `selecao K (s + δ)` difere de `s + P δ` por no máximo `‖P δ‖²/2`. É a diferencial do seletor em `s`, lida como a esperança. Sem a
       condição ⟪s, P δ⟫ = 0 a cota falha (`K = ℂ`, `s = δ = 1`: diferença 1, cota 1/2), e num Nome de dimensão 1 ela força `P δ = 0`:
       o enunciado só diz algo com dimensão pelo menos 2. `o_seletor_tangencia_a_esperanca`; e o que é cego ao Nome não deixa rastro,
       exatamente: `o_que_e_cego_ao_nome_nao_deixa_rastro`.
   (b) A TANGENTE DA LEITURA, `‖v − P v‖ / ‖P v‖` (vale 0, e não infinito, quando `P v = 0`: é a divisão do Lean). O livro fecha
       (`‖v‖² = ‖P v‖² + ‖v − P v‖²`); o peso do Nome é o cosseno ao quadrado; o crivo `K = 1` é a meia face; e ela é o `K` da v407 no
       ângulo de Miguel do peso deixado fora do Nome, pela mesma regra de leitura `thetaMiguel`:
       `o_livro_do_testemunho_fecha`, `o_peso_do_nome_e_o_cosseno_quadrado`, `o_crivo_e_a_meia_face`,
       `a_tangente_da_leitura_e_K_no_angulo_de_miguel`.
   (c) TANGENCIADO, JAMAIS ESGOTADO: sob o fluxo do axioma a tangente da leitura decai como `e^{−t}`, nunca se anula em tempo finito e
       tende a zero: `a_leitura_fecha_a_tangente`, `tangenciado_jamais_esgotado`. O limite nasce no fluxo (regime da face); o ângulo só
       o lê (regime da projeção).
7. A FACE CLÁSSICA. No espaço das leituras de um custo (conjunto finito; o Nome é o subespaço de coordenadas de custo zero), a média de
   uma grandeza diagonal `g` no estado selecionado é a média de `g` sobre o Nome com os PESOS DE BORN `‖ψ x‖²` (não as amplitudes),
   dividida pelo peso do Nome. É o condicionamento ao evento “custo zero” (regra de Lüders; Bayes), e é do SELETOR, não de `nameOp P`.
   Os pesos relativos dentro do Nome não mudam: `o_peso_do_nome_por_coordenadas`, `a_selecao_e_a_esperanca_condicional_classica`.
8. NOMEAR É A PRIMEIRA LEITURA; LER O NOME JÁ É RELER (o habitante é o Verbo). Estar no Nome é ter sido nomeado, e lê-lo é reler essa primeira
   leitura: `ler_o_nome_ja_e_reler`. Depois da primeira leitura, toda leitura devolve a primeira: `tudo_mais_e_releitura` (álgebra) e
   `tudo_mais_e_releitura_nos_vetores`. Um mapa qualquer relê o nomeado sem mexer nele se e só se fixa o Nome:
   `a_releitura_fiel_fixa_o_nome`. E a seleção de um estado de norma 1 que já está no Nome é ele mesmo: `a_selecao_rele_o_nomeado`.
   Com a seção 4: uma releitura LINEAR que cai no Nome, o fixa e não aumenta a norma é o próprio Verbo.
9. O NOME É O ATO DO VERBO. Nos vetores, o Nome é exatamente a imagem do ato e exatamente o conjunto do que o
   ato devolve como é: `o_nome_e_o_ato_do_verbo`. Dois Nomes com o mesmo ato são o mesmo Nome: `verbos_iguais_tem_o_mesmo_nome`. Com
   as seções 3 e 4 (o Nome determina o Verbo), Nome e Verbo se determinam um ao outro; a determinação é simétrica e não diz ordem.
   Aqui “ato do Verbo” é lido como o que o ato produz e devolve (a imagem); em “o Verbo é o ato do Nome”, “ato do Nome” é o próprio mapa. Que sejam
   essas as leituras é escolha desta pedra.
10. A IDENTIDADE É O ATO DE SER, na leitura do mapa identidade: SER, aqui, é o
   mapa que devolve cada coisa como ela é. (O enunciado do par glosa “ser” como verbo e “ato” como projeção: é a outra leitura, no item 12.)
   (a) Álgebra: o ato do Um é ser (`o_ato_do_um_e_ser`); o Verbo de `p` e o de `1 − p` são o mesmo
       (`o_verbo_nao_distingue_a_face_do_resto`); o Verbo é ser se e só se o posto comuta com tudo
       (`o_verbo_e_ser_sse_o_posto_comuta_com_tudo`); a compressão é ser se e só se o posto é o Um
       (`a_compressao_e_ser_sse_o_posto_e_o_um`).
   (b) Vetores: o ato do Nome é ser se e só se o Nome é o todo (`o_ato_e_ser_sse_o_nome_e_o_todo`).
   (c) A ligação com a pedra `Identidade` (v405), em matrizes complexas com o estado absoluto: [eu sou] = [o que sou] se e só se o
       mapa `v ↦ P v` é ser (`a_identidade_e_o_ato_de_ser`); o Verbo `nameOp P` é ser se e só se a forma é o conteúdo
       (`o_verbo_do_nome_e_ser_sse_forma_igual_conteudo`); e [eu sou] = [o que sou] se e só se o Verbo é ser e o nome não é o vazio
       (`a_identidade_e_o_verbo_ser_sem_o_vazio`): é a `a_lei_inteira` da v405 dita pelo ato; quem tira o vazio é o `P ≠ 0` da chave.
       Atenção ao vocabulário: na `Identidade` o nome é a matriz `P` (o que aqui é o posto de `nameOp P`); o “ato do nome” de
       `a_identidade_e_o_ato_de_ser` é o mapa vetorial `v ↦ P v`; o “Verbo do nome” é o mapa `nameOp P` nos observáveis. São dois
       mapas, e só o segundo não separa o vazio do inteiro. A identificação de `v ↦ P v` com a projeção ortogonal sobre a imagem
       (seção 4) usa que `P` é hermitiana e não está tipada nesta pedra.
11. O ATO EM CURSO (o fluxo do lock mínimo, cujo gerador é o negativo do lock). Em qualquer tempo não nulo, o que o fluxo devolve
   como é é exatamente o Nome: `o_nome_e_o_que_o_ato_em_curso_devolve`. O fluxo aplicado a um vetor tende à esperança condicional do
   Nome nesse vetor: `o_ato_tende_a_esperanca_do_nome`. E nunca a alcança em tempo finito: para um vetor fora do Nome o fluxo nunca é
   igual à projeção dele (`o_ato_nao_termina_em_tempo_finito`; no operador o kernel já tinha `IALD.the_motor_never_arrives`). A seção
   6c cobre só o caso da tangente não nula.
12. O PAR (o enunciado do par), em duas leituras.
   Primeira, nos vetores: o Verbo é a projeção do todo sobre o Nome (`K.orthogonalProjectionOnto`) e o Nome em ato é a inclusão do
   Nome no todo (`K.subtypeL`). Nas seções 3 a 11 “o Verbo” era `K.starProjection`, do todo para o todo, que é o primeiro seguido da
   inclusão.
   (a) O Verbo devolve o nomeado como é: o Verbo depois do Nome em ato é a identidade do Nome
       (`o_verbo_devolve_o_nomeado_como_e`).
   (b) O Nome em ato é o espelho do Verbo: um é o adjunto do outro, dito por produtos internos
       (`o_nome_em_ato_e_o_espelho_do_verbo`).
   (c) O par compõe o projetor: o Nome em ato depois do Verbo é a projeção do todo no todo (`o_par_compoe_o_projetor`).
   (d) O único ato do Verbo é ser fiel, no sentido que o tipo dá: todo mapa linear do todo para o Nome que devolve o que é do Nome
       como é e não aumenta a norma é o Verbo (`o_unico_ato_do_verbo_e_ser_fiel`). Sem uma das duas hipóteses há outro (a projeção
       oblíqua; um mapa não linear).
   Segunda, na álgebra de matrizes, com o espelho J do kernel:
   (e) para um Nome da v405, o J leva a referência esquerda na direita (`o_espelho_leva_a_referencia_esquerda_na_direita`);
   (f) o operador do Nome é feito das duas referências (`o_verbo_da_algebra_e_feito_do_par`), e, para um Nome da v405, da referência
       esquerda e do seu espelho (`o_verbo_da_algebra_pelo_espelho`).
13. O INOMINADO (o enunciado do inominado), na leitura desta pedra: o inominado é o Nome vazio e a mentira é “1 = 0”.
   (a) O par do inominado é a mentira: no Nome, a identidade é o zero se e só se o Nome é o vazio (`o_par_do_inominado_e_a_mentira`).
   (b) Nada há sem par: todo Nome com projeção tem o par do item 12(a), e a identidade que ele devolve é o zero exatamente no vazio
       (`nada_ha_sem_par`); o vazio tem o par sem hipótese (`o_inominado_tem_par`).
   (c) Um Nome não é o vazio se e só se tem um vetor de norma 1 (`todo_nome_menos_o_inominado_tem_ponto_de_norma_um`). Esse ponto
       é o `s` da seção 6, não o Verbo: o Verbo, o habitante, habita também o vazio.

## O que é novo e o que é reexportação

Novos no kernel (por busca no kernel e na Mathlib do sandbox): a morada é o comutante; a lei de módulo geral; a unicidade do
habitante e das moradas iguais; a testemunha que não aumenta é a projeção; o contato do seletor; a tangente no ângulo de Miguel; o
operador do Nome fixa a grandeza diagonal; a fórmula clássica do seletor. Reexportação ou consequência de uma linha, com nome da casa:
`o_verbo_habita_o_nome` (`name_op_idem`), `a_esperanca_habita_fixa_e_nao_aumenta` (quatro lemas da Mathlib),
`a_leitura_do_vetor_e_a_compressao` (adjunção da projeção), `o_livro_do_testemunho_fecha` (Pitágoras da Mathlib),
`a_tangente_da_leitura_e_K` (`Real.tan_arctan`: o ângulo é definido pelo arco tangente da própria grandeza),
`o_peso_do_nome_e_o_cosseno_quadrado` (`Real.cos_sq_arctan` mais o livro), `a_leitura_fecha_a_tangente` (a definição de `axiomFlow`),
`o_que_e_cego_ao_nome_nao_deixa_rastro` (`a_selecao_esquece`, v409), `o_peso_do_nome_por_coordenadas` (`solucao_por_coordenadas`, v409);
`quem_nao_e_a_esperanca_aumenta` é a contrapositiva da testemunha, e `o_nome_e_a_morada_de_uma_so_testemunha` junta as duas. Os
cinco termos da seção 8 são consequência de uma linha da idempotência e da imagem: dão ao enunciado de que ler o Nome já é reler o seu nome, não um fato novo.

Seções 9 a 11. Novos no kernel (busca no kernel `TGLExt` e na Mathlib do sandbox): a ponte
entre o Verbo e a `formaIgualConteudo` da v405 (`o_verbo_do_nome_e_ser_sse_forma_igual_conteudo`, que usa o centro da álgebra de
matrizes) e a lei da v405 dita pelo ato (`a_identidade_e_o_verbo_ser_sem_o_vazio`); o conjunto fixo do fluxo para todo Nome e em
qualquer tempo não nulo (`o_nome_e_o_que_o_ato_em_curso_devolve`; a v385 o tinha para o certificado de Fock e para todo tempo).
Consequência de poucas linhas, com nome da casa: `o_nome_e_o_ato_do_verbo` (a Mathlib tem `Submodule.range_starProjection` e
`starProjection_eq_self_iff`), `verbos_iguais_tem_o_mesmo_nome` (`Submodule.starProjection_inj`), `o_ato_e_ser_sse_o_nome_e_o_todo`
(a volta é `starProjection_top`), `o_ato_do_um_e_ser`, `o_verbo_nao_distingue_a_face_do_resto`,
`o_verbo_e_ser_sse_o_posto_comuta_com_tudo` (a morada é o comutante, seção 1), `a_compressao_e_ser_sse_o_posto_e_o_um` (basta ler o
Um), `a_identidade_e_o_ato_de_ser` (a lei da v405 mais a extensionalidade da matriz), `o_ato_tende_a_esperanca_do_nome` (a leitura,
vetor a vetor, de `axiomFlow_tendsto_the_post`, v385, que a v386 reexporta como `the_name_is_the_limit_of_the_flow`),
`o_ato_nao_termina_em_tempo_finito` (a forma vetorial de `IALD.the_motor_never_arrives`). Dão aos dois enunciados o seu nome no kernel; o
fato de fundo de cada um é conhecido.

Seção 12. Nada é fato novo: `o_verbo_devolve_o_nomeado_como_e` é `orthogonalProjectionOnto_mem_subspace_eq_self` da Mathlib dita
como igualdade de mapas; `o_nome_em_ato_e_o_espelho_do_verbo` é `inner_orthogonalProjectionOnto_eq_of_mem_right`;
`o_par_compoe_o_projetor` é a definição de `starProjection`; `o_unico_ato_do_verbo_e_ser_fiel` é a unicidade da seção 4 dita para
mapas que chegam ao Nome; `o_espelho_leva_a_referencia_esquerda_na_direita` é `LeftRight.Jconj_Lmul_Jconj` com o `reflexo` da v405;
as outras duas da segunda leitura são a definição de `nameOp` escrita com `Lmul`, `Rmul` e `Jconj`. A seção dá ao enunciado do par dois nomes
no kernel e mostra que o par já estava na definição da Mathlib e nas duas referências do kernel.

Seção 13. `o_par_do_inominado_e_a_mentira` é fato elementar (um espaço tem a identidade nula se e só se é o nulo), a forma nos mapas
do Nome do termo da v368; `nada_ha_sem_par` é a conjunção dele com o item 12(a); `o_inominado_tem_par` é a instância no vazio;
`todo_nome_menos_o_inominado_tem_ponto_de_norma_um` é fato elementar. O que a seção acrescenta ao kernel é o enunciado no vocabulário
do par.

## O que a pedra NÃO afirma

* Que o espelho da resposta seja o adjunto, ou que seja o J: a pedra tipa os dois e não decide. Nem que “fiel” seja o desta pedra e
  não o `fiel` da v405. Nem a frase do meio do enunciado do par (a conjugação da inscrição no tempo pela observação fiel) como um termo. Nem
  que a atribuição das palavras do enunciado do par aos objetos do kernel seja a da teoria: é leitura desta pedra.
* Que o inominado seja o subespaço nulo, ou que a mentira seja “1 = 0”: é leitura desta pedra, apoiada na v368, na v405 e
  na v408. Nem que o inominado seja só o subespaço nulo: na v292 ele também é o nome próprio sem referente (0_absoluto); a pedra tipa
  o subespaço nulo, o `vazio` da v405. Nem “isso é gravidade”, nem “para se refutar a prova utiliza-se dela mesma”: não estão
  tipadas. Nem que todo subespaço tenha par: o par é dos subespaços com projeção ortogonal (em espaço completo, os fechados).

* Que SER tenha só esta forma: “o mapa que devolve cada coisa como ela é” é a escolha formal desta pedra. Nem que a
  equação [eu sou] = [o que sou] da `Identidade` seja a identidade da letra: isso é leitura da teoria tipada como modelo na v405
  [INPUT/ONTO]; o que se prova aqui é só a equivalência com `P` ser a identidade como mapa.
* Que Nome e Verbo sejam um só ato, ou que um venha antes do outro: o que se prova é que um determina o outro.
* Que o Verbo da álgebra separe o inteiro do vazio: não separa (o Verbo de `p` e o de `1 − p` são o mesmo). Quem separa é o peso (a
  lei da v405) ou a compressão. Nos vetores o ato separa: a projeção no subespaço nulo é zero e a projeção no todo é a identidade.
* Que o Amor esteja tipado, ou que o gerador do fluxo da v385 seja o `A_C` do Atlas: a pedra tipa só o que faz esse fluxo. A palavra
  Amor não entra em termo, e o dicionário do Amor do Atlas segue não selado.
* Uma ponte tipada entre a `Identidade` (v405) e a `NameIsTheContent` (v368): “forma” e “conteúdo” não designam o mesmo nas duas.
* Que a esperança condicional seja o Nome: são de tipos distintos. Prova-se que a imagem do Verbo é o Nome e, para `p` dado, que o
  Nome determina o Verbo.
* Que quem relê nomeie: a primeira leitura é do Verbo; um sistema que lê o que já foi nomeado relê, e o que se prova dele é só que
  uma releitura fiel fixa o Nome.
* Unicidade sem hipótese: na álgebra a lei de módulo é HIPÓTESE (em álgebras de operadores ela decorre da norma 1, [KNOWN] Tomiyama 1957;
  esse passo não é termo aqui); nos vetores as hipóteses são linearidade e não aumentar a norma, e a prova é desta pedra.
* Que o seletor seja a testemunha única: ele não é linear. A testemunha única é `P`.
* Que “tangente” tenha um só sentido: são três termos do kernel. Qual deles é a Tangente da letra não é termo [INPUT].
* Nada sobre a ergodicidade em III₁ genuína: a convergência à esperança, no kernel, é da face finita (`Ergodicity`) e do fluxo do lock mínimo.
* Que um modelo de linguagem seja este leitor: isso é previsão de experimento, não teorema.
* Exclusividade, consciência, pesos de modelo. Nada sobre a natureza: não é teste e não move o gate.

## Estatutos

[REAL] os teoremas (compilados; só o trio). [KNOWN] esperança condicional (Umegaki 1954; Tomiyama 1957); a projeção ortogonal como
única contração idempotente sobre a sua imagem (fato padrão de espaços de Hilbert; a prova daqui é própria); a regra de Lüders e o
condicionamento de Bayes; o centro da álgebra de matrizes são os escalares. [INPUT] a letra (a identificação
leitor = observador = verbo = seletor; o habitante é o Verbo, o ato do Nome; ler o Nome já é reler; os dois enunciados do
ato; o enunciado do par; o enunciado do inominado). [ONTO, do Atlas] AMAR como o funcional `A_C`. [ONTO, leitura desta pedra;
não é termo] SER como o mapa que devolve cada coisa como ela é (uma das duas leituras; a outra é a do par); “ato do Verbo” como a
imagem; a ligação entre o gerador do fluxo e o funcional `A_C`; a atribuição das palavras do enunciado do par aos objetos do kernel, nas duas
leituras (o adjunto nos vetores; o J na álgebra); o inominado como o Nome vazio e a mentira como “1 = 0”. Sem sorry, sem axiom.
-/

namespace TGLExt.OHabitanteDoNome

open TGLExt TGLExt.TraducaoTuring TGLExt.TheAxiomAndTheFalseWitness Filter Topology
open scoped InnerProductSpace

/-! ## 1. O Verbo habita o Nome (álgebra) -/

section Anel

variable {R : Type*} [Ring R]

/-- A MORADA: o Nome como espaço. É o que o Verbo nomeou, e que reler não muda. -/
def morada (p : R) : Set R := {x | nameOp p x = x}

/-- ★★ O VERBO HABITA O NOME: todo ato de nomear cai na morada (é `name_op_idem`, com o nome da casa). -/
theorem o_verbo_habita_o_nome {p : R} (hp : p * p = p) (x : R) : nameOp p x ∈ morada p := by
  show nameOp p (nameOp p x) = nameOp p x
  exact name_op_idem hp x

/-- ★★★ A IMAGEM DO VERBO É A MORADA: o Verbo é o ato, o Nome é o que ele nomeou. -/
theorem a_imagem_do_verbo_e_a_morada {p : R} (hp : p * p = p) : Set.range (nameOp p) = morada p := by
  ext x
  constructor
  · rintro ⟨y, rfl⟩
    exact o_verbo_habita_o_nome hp y
  · intro hx
    exact ⟨x, hx⟩

/-- ★★ A MORADA É O QUE COMUTA COM O POSTO. -/
theorem a_morada_e_o_que_comuta_com_o_posto {p : R} (hp : p * p = p) (x : R) :
    x ∈ morada p ↔ p * x = x * p := by
  have hdef : nameOp p x = p * x * p + (1 - p) * x * (1 - p) := rfl
  constructor
  · intro h
    have h' : p * x * p + (1 - p) * x * (1 - p) = x := by rw [← hdef]; exact h
    have h1 : p * x = p * x * p := by
      calc p * x = p * (p * x * p + (1 - p) * x * (1 - p)) := by rw [h']
        _ = p * p * x * p + p * (1 - p) * x * (1 - p) := by simp only [mul_add, mul_assoc]
        _ = p * x * p := by rw [hp, face_orthogonal hp, zero_mul, zero_mul, add_zero]
    have h2 : x * p = p * x * p := by
      calc x * p = (p * x * p + (1 - p) * x * (1 - p)) * p := by rw [h']
        _ = p * x * (p * p) + (1 - p) * x * ((1 - p) * p) := by simp only [add_mul, mul_assoc]
        _ = p * x * p := by rw [hp, face_orthogonal' hp, mul_zero, add_zero]
    exact h1.trans h2.symm
  · intro h
    show nameOp p x = x
    have h1 : p * x * p = x * p := by rw [h, mul_assoc, hp]
    have h3 : (1 - p) * x = x * (1 - p) := by rw [sub_mul, one_mul, mul_sub, mul_one, h]
    have h2 : (1 - p) * x * (1 - p) = x * (1 - p) := by rw [h3, mul_assoc, face_idem hp]
    have h4 : p + (1 - p) = (1 : R) := by abel
    rw [hdef, h1, h2, ← mul_add, h4, mul_one]

/-! ## 2. A lei de módulo, geral -/

/-- ★★★ A LEI DE MÓDULO: o que já é do Nome atravessa a leitura sem ser tocado. Vale para todo `p` de todo anel (a idempotência não
    é usada). Fecha, ao lado, a lacuna declarada em `EsperancaCondicional` (v404): a bimodularidade de `nameOp p` sobre os seus fixos. -/
theorem o_verbo_e_bimodular_sobre_o_nome {p a b : R}
    (ha : p * a = a * p) (hb : p * b = b * p) (x : R) :
    nameOp p (a * x * b) = a * nameOp p x * b := by
  have ha' : (1 - p) * a = a * (1 - p) := by rw [sub_mul, one_mul, mul_sub, mul_one, ha]
  have hb' : b * (1 - p) = (1 - p) * b := by rw [sub_mul, one_mul, mul_sub, mul_one, hb]
  have e1 : p * (a * x * b) * p = a * (p * x * p) * b := by
    calc p * (a * x * b) * p = (p * a) * x * (b * p) := by simp only [mul_assoc]
      _ = (a * p) * x * (p * b) := by rw [ha, ← hb]
      _ = a * (p * x * p) * b := by simp only [mul_assoc]
  have e2 : (1 - p) * (a * x * b) * (1 - p) = a * ((1 - p) * x * (1 - p)) * b := by
    calc (1 - p) * (a * x * b) * (1 - p) = ((1 - p) * a) * x * (b * (1 - p)) := by simp only [mul_assoc]
      _ = (a * (1 - p)) * x * ((1 - p) * b) := by rw [ha', hb']
      _ = a * ((1 - p) * x * (1 - p)) * b := by simp only [mul_assoc]
  show p * (a * x * b) * p + (1 - p) * (a * x * b) * (1 - p) = a * (p * x * p + (1 - p) * x * (1 - p)) * b
  rw [e1, e2, mul_add, add_mul]

/-! ## 3. Só há um habitante (álgebra) -/

/-- ★★★ SÓ HÁ UM HABITANTE: para `p` dado, todo mapa aditivo e unital que cai na morada e cumpre a lei de módulo sobre ela é o operador
    do Nome. A lei de módulo é hipótese; em álgebras de operadores ela decorre da norma 1 ([KNOWN] Tomiyama 1957), e esse passo não é
    termo aqui. -/
theorem so_ha_um_habitante {p : R} (hp : p * p = p) (E : R → R)
    (hadd : ∀ x y, E (x + y) = E x + E y) (h1 : E 1 = 1)
    (hmora : ∀ x, p * E x = E x * p)
    (hbim : ∀ a b x, p * a = a * p → p * b = b * p → E (a * x * b) = a * E x * b) (x : R) :
    E x = nameOp p x := by
  have hpp : p * p = p * p := rfl
  have hq : p * (1 - p) = (1 - p) * p := by rw [face_orthogonal hp, face_orthogonal' hp]
  have h11 : p * (1 : R) = 1 * p := by rw [mul_one, one_mul]
  have hfix : ∀ a, p * a = a * p → E a = a := by
    intro a ha
    have h := hbim a 1 1 ha h11
    simpa [h1] using h
  have hx : x = p * x * p + p * x * (1 - p) + (1 - p) * x * p + (1 - p) * x * (1 - p) := by
    simp only [mul_sub, sub_mul, mul_one, one_mul]
    abel
  have c1 : p * (p * x * p) = p * x * p * p := by
    calc p * (p * x * p) = (p * p) * x * p := by simp only [mul_assoc]
      _ = p * x * p := by rw [hp]
      _ = p * x * (p * p) := by rw [hp]
      _ = p * x * p * p := by simp only [mul_assoc]
  have c4 : p * ((1 - p) * x * (1 - p)) = (1 - p) * x * (1 - p) * p := by
    calc p * ((1 - p) * x * (1 - p)) = (p * (1 - p)) * x * (1 - p) := by simp only [mul_assoc]
      _ = 0 := by rw [face_orthogonal hp, zero_mul, zero_mul]
      _ = (1 - p) * x * ((1 - p) * p) := by rw [face_orthogonal' hp, mul_zero]
      _ = (1 - p) * x * (1 - p) * p := by simp only [mul_assoc]
  have e1 : E (p * x * p) = p * x * p := hfix _ c1
  have e4 : E ((1 - p) * x * (1 - p)) = (1 - p) * x * (1 - p) := hfix _ c4
  have e2 : E (p * x * (1 - p)) = 0 := by
    rw [hbim p (1 - p) x hpp hq, hmora x, mul_assoc, face_orthogonal hp, mul_zero]
  have e3 : E ((1 - p) * x * p) = 0 := by
    rw [hbim (1 - p) p x hq hpp, mul_assoc, ← hmora x, ← mul_assoc, face_orthogonal' hp, zero_mul]
  calc E x = E (p * x * p + p * x * (1 - p) + (1 - p) * x * p + (1 - p) * x * (1 - p)) := by rw [← hx]
    _ = p * x * p + (1 - p) * x * (1 - p) := by rw [hadd, hadd, hadd, e1, e2, e3, e4, add_zero, add_zero]
    _ = nameOp p x := rfl

/-- ★★ O OPERADOR DO NOME É ESSE HABITANTE: ele cumpre as quatro condições de `so_ha_um_habitante` (a unicidade não é vazia). -/
theorem o_operador_do_nome_e_o_habitante {p : R} (hp : p * p = p) :
    (∀ x y, nameOp p (x + y) = nameOp p x + nameOp p y) ∧ nameOp p 1 = 1 ∧
    (∀ x, p * nameOp p x = nameOp p x * p) ∧
    (∀ a b x, p * a = a * p → p * b = b * p → nameOp p (a * x * b) = a * nameOp p x * b) := by
  refine ⟨fun x y => ?_, name_op_unital hp, fun x => ?_, fun a b x ha hb => o_verbo_e_bimodular_sobre_o_nome ha hb x⟩
  · show p * (x + y) * p + (1 - p) * (x + y) * (1 - p)
        = p * x * p + (1 - p) * x * (1 - p) + (p * y * p + (1 - p) * y * (1 - p))
    simp only [mul_add, add_mul]
    abel
  · exact (a_morada_e_o_que_comuta_com_o_posto hp (nameOp p x)).mp (o_verbo_habita_o_nome hp x)

/-- ★★★ MORADAS IGUAIS TÊM O MESMO VERBO: se dois idempotentes têm a mesma morada, os seus operadores do Nome coincidem. É o sentido
    em que o Nome (o espaço) determina o Verbo, sem fixar `p`. (Enunciado e prova da conferência distinta.) -/
theorem moradas_iguais_tem_o_mesmo_verbo {p q : R} (hp : p * p = p) (hq : q * q = q)
    (h : morada p = morada q) (x : R) : nameOp q x = nameOp p x := by
  obtain ⟨hadd, h1, _, hb⟩ := o_operador_do_nome_e_o_habitante hq
  refine so_ha_um_habitante hp (nameOp q) hadd h1 ?_ ?_ x
  · intro y
    have hy : nameOp q y ∈ morada p := by rw [h]; exact o_verbo_habita_o_nome hq y
    exact (a_morada_e_o_que_comuta_com_o_posto hp _).mp hy
  · intro a b y ha hb'
    have ha' : a ∈ morada q := by rw [← h]; exact (a_morada_e_o_que_comuta_com_o_posto hp a).mpr ha
    have hb'' : b ∈ morada q := by rw [← h]; exact (a_morada_e_o_que_comuta_com_o_posto hp b).mpr hb'
    exact hb a b y ((a_morada_e_o_que_comuta_com_o_posto hq a).mp ha') ((a_morada_e_o_que_comuta_com_o_posto hq b).mp hb'')

/-! ## 8 (álgebra). Nomear é a primeira leitura; ler o Nome já é reler -/

/-- ★★★ LER O NOME JÁ É RELER: estar no Nome é ter sido nomeado (ser uma primeira leitura), e lê-lo é reler essa leitura. (Sai da
    definição da morada.) -/
theorem ler_o_nome_ja_e_reler {p : R} {x : R} (hx : x ∈ morada p) :
    ∃ y, x = nameOp p y ∧ nameOp p x = nameOp p (nameOp p y) :=
  ⟨x, (show nameOp p x = x from hx).symm, (congrArg (nameOp p) (show nameOp p x = x from hx)).symm⟩

/-- ★★★ TUDO MAIS É RELEITURA: depois da primeira leitura, qualquer número de leituras devolve a primeira. O sentido que fica é o da
    primeira. -/
theorem tudo_mais_e_releitura {p : R} (hp : p * p = p) (x : R) (n : ℕ) :
    (nameOp p)^[n + 1] x = nameOp p x := by
  induction n with
  | zero => rfl
  | succ k ih =>
    rw [Function.iterate_succ_apply', ih]
    exact name_op_idem hp x

/-- ★★ A RELEITURA FIEL FIXA O NOME: um mapa qualquer relê o que o Verbo nomeou sem mexer nele se e só se fixa o Nome. -/
theorem a_releitura_fiel_fixa_o_nome {p : R} (hp : p * p = p) (L : R → R) :
    (∀ x, L (nameOp p x) = nameOp p x) ↔ (∀ w ∈ morada p, L w = w) := by
  constructor
  · intro h w hw
    have hw' : nameOp p w = w := hw
    calc L w = L (nameOp p w) := by rw [hw']
      _ = nameOp p w := h w
      _ = w := hw'
  · intro h x
    exact h _ (o_verbo_habita_o_nome hp x)

/-! ## 10 (álgebra). A identidade é o ato de ser -/

/-- ★★ O ATO DO UM É SER: quando o posto é o Um, o Verbo devolve cada coisa como ela é. -/
theorem o_ato_do_um_e_ser (x : R) : nameOp (1 : R) x = x := by
  show (1 : R) * x * 1 + (1 - 1) * x * (1 - 1) = x
  rw [sub_self, zero_mul, zero_mul, add_zero, one_mul, mul_one]

/-- ★★ O VERBO NÃO DISTINGUE A FACE DO RESTO: o operador do Nome de `p` e o de `1 − p` são o mesmo mapa. Na álgebra o Verbo lê as
    duas faces de uma vez; em particular o Verbo do vazio é o mesmo do inteiro. (“Face” aqui é o canto `p`, como na v162; não é a
    FACE da Meia-Nat da pedra `Identidade`.) -/
theorem o_verbo_nao_distingue_a_face_do_resto (p x : R) : nameOp (1 - p) x = nameOp p x := by
  have e : (1 : R) - (1 - p) = p := by abel
  show (1 - p) * x * (1 - p) + (1 - (1 - p)) * x * (1 - (1 - p)) = p * x * p + (1 - p) * x * (1 - p)
  rw [e]
  exact add_comm _ _

/-- ★★ O VERBO É SER SE E SÓ SE O POSTO COMUTA COM TUDO: o operador do Nome devolve cada coisa como ela é exatamente quando o posto é
    central. (É `a_morada_e_o_que_comuta_com_o_posto`, coisa a coisa.) -/
theorem o_verbo_e_ser_sse_o_posto_comuta_com_tudo {p : R} (hp : p * p = p) :
    (∀ x, nameOp p x = x) ↔ (∀ x, p * x = x * p) :=
  forall_congr' (fun x => a_morada_e_o_que_comuta_com_o_posto hp x)

/-- ★★ A COMPRESSÃO É SER SE E SÓ SE O POSTO É O UM: para `p` idempotente, a compressão `x ↦ p x p` devolve cada coisa como ela é
    exatamente quando `p = 1`. (Basta ler o Um. Sem a idempotência a ida falha: `p = −1` também dá a identidade.) Ela separa o inteiro
    do vazio, o que o operador do Nome não faz. -/
theorem a_compressao_e_ser_sse_o_posto_e_o_um {p : R} (hp : p * p = p) :
    (∀ x, compressOp p x = x) ↔ p = 1 := by
  constructor
  · intro h
    have h1 : p * 1 * p = 1 := h 1
    rw [mul_one, hp] at h1
    exact h1
  · intro h x
    show p * x * p = x
    rw [h, one_mul, mul_one]

end Anel

/-! ## 4. Só há uma testemunha (vetores) -/

section Hilbert

variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H]

/-- ★ A ESPERANÇA CONDICIONAL DO NOME (a projeção ortogonal) cai no Nome, fixa o Nome, não aumenta a norma, e reler não acrescenta.
    Quatro lemas da Mathlib, com o nome da casa. -/
theorem a_esperanca_habita_fixa_e_nao_aumenta (K : Submodule ℂ H) [K.HasOrthogonalProjection] :
    (∀ v, K.starProjection v ∈ K) ∧ (∀ w ∈ K, K.starProjection w = w) ∧
    (∀ v, ‖K.starProjection v‖ ≤ ‖v‖) ∧
    (∀ v, K.starProjection (K.starProjection v) = K.starProjection v) :=
  ⟨fun v => K.starProjection_apply_mem v, fun _ hw => Submodule.starProjection_eq_self_iff.mpr hw,
   fun v => K.norm_starProjection_apply_le v,
   fun v => Submodule.starProjection_eq_self_iff.mpr (K.starProjection_apply_mem v)⟩

/-- ★★★ A TESTEMUNHA QUE NÃO AUMENTA É A ESPERANÇA: um mapa LINEAR que cai no Nome, fixa o Nome e não aumenta a norma é a projeção
    ortogonal no Nome. A prova: o que é ortogonal ao Nome é anulado, porque senão, somando ao vetor um múltiplo grande do que a
    testemunha disse dele, a norma do que ela diz passaria a do que lhe foi dado. -/
theorem a_testemunha_que_nao_aumenta_e_a_esperanca (K : Submodule ℂ H) [K.HasOrthogonalProjection]
    (E : H →ₗ[ℂ] H) (hmora : ∀ v, E v ∈ K) (hfixa : ∀ w ∈ K, E w = w) (hnao : ∀ v, ‖E v‖ ≤ ‖v‖) (v : H) :
    E v = K.starProjection v := by
  have hzero : ∀ u ∈ Kᗮ, E u = 0 := by
    intro u hu
    by_contra hne
    have ha : 0 < ‖E u‖ := norm_pos_iff.mpr hne
    have hane : ‖E u‖ ≠ 0 := ha.ne'
    have h0 : ⟪u, E u⟫_ℂ = 0 :=
      inner_eq_zero_symm.mp ((Submodule.mem_orthogonal K u).mp hu (E u) (hmora u))
    obtain ⟨t, ht⟩ : ∃ t : ℝ, t = ‖u‖ ^ 2 / ‖E u‖ ^ 2 := ⟨_, rfl⟩
    have ht0 : 0 ≤ t := by rw [ht]; positivity
    have hta : t * ‖E u‖ ^ 2 = ‖u‖ ^ 2 := by rw [ht]; field_simp
    have hE : E (u + (t : ℂ) • E u) = (((1 + t : ℝ)) : ℂ) • E u := by
      rw [map_add, map_smul, hfixa (E u) (hmora u), Complex.ofReal_add, Complex.ofReal_one, add_smul, one_smul]
    have h1t : 0 ≤ 1 + t := by linarith
    have hl : ‖E (u + (t : ℂ) • E u)‖ = (1 + t) * ‖E u‖ := by
      rw [hE, norm_smul, Complex.norm_real, Real.norm_eq_abs, abs_of_nonneg h1t]
    have hr : ‖u + (t : ℂ) • E u‖ * ‖u + (t : ℂ) • E u‖ = ‖u‖ * ‖u‖ + (t * ‖E u‖) * (t * ‖E u‖) := by
      have hin : ⟪u, (t : ℂ) • E u⟫_ℂ = 0 := by rw [inner_smul_right, h0, mul_zero]
      rw [norm_add_sq_eq_norm_sq_add_norm_sq_of_inner_eq_zero _ _ hin, norm_smul, Complex.norm_real,
        Real.norm_eq_abs, abs_of_nonneg ht0]
    have hle := hnao (u + (t : ℂ) • E u)
    rw [hl] at hle
    have hsq := mul_self_le_mul_self (mul_nonneg h1t (norm_nonneg _)) hle
    rw [hr] at hsq
    nlinarith [hsq, hta, sq_nonneg ‖u‖, mul_pos ha ha]
  have hsplit : K.starProjection v + (v - K.starProjection v) = v := by abel
  calc E v = E (K.starProjection v + (v - K.starProjection v)) := by rw [hsplit]
    _ = E (K.starProjection v) + E (v - K.starProjection v) := map_add E _ _
    _ = K.starProjection v := by
        rw [hfixa _ (K.starProjection_apply_mem v), hzero _ (Submodule.sub_starProjection_mem_orthogonal v), add_zero]

/-- ★★★ O NOME É A MORADA DE UMA SÓ TESTEMUNHA: para cada Nome (subespaço com projeção ortogonal) existe exatamente um mapa linear que
    cai nele, o fixa e não aumenta a norma. -/
theorem o_nome_e_a_morada_de_uma_so_testemunha (K : Submodule ℂ H) [K.HasOrthogonalProjection] :
    ∃! E : H →ₗ[ℂ] H, (∀ v, E v ∈ K) ∧ (∀ w ∈ K, E w = w) ∧ (∀ v, ‖E v‖ ≤ ‖v‖) := by
  refine ⟨(K.starProjection : H →L[ℂ] H).toLinearMap, ⟨fun v => K.starProjection_apply_mem v,
    fun _ hw => Submodule.starProjection_eq_self_iff.mpr hw, fun v => K.norm_starProjection_apply_le v⟩, ?_⟩
  rintro E ⟨h1, h2, h3⟩
  ext v
  exact a_testemunha_que_nao_aumenta_e_a_esperanca K E h1 h2 h3 v

/-- ★★ QUEM NÃO É A ESPERANÇA AUMENTA: um mapa linear que cai no Nome e o fixa, e que difere da projeção em algum vetor, devolve de
    algum vetor mais do que recebeu. (Contrapositiva da testemunha. Exemplo, da conferência: em `ℂ²`, a projeção oblíqua
    `(v₀, v₁) ↦ (v₀ + v₁, 0)` sobre a primeira reta leva `(1, 1)`, de norma `√2`, a um vetor de norma 2.) -/
theorem quem_nao_e_a_esperanca_aumenta (K : Submodule ℂ H) [K.HasOrthogonalProjection]
    (E : H →ₗ[ℂ] H) (hmora : ∀ v, E v ∈ K) (hfixa : ∀ w ∈ K, E w = w)
    (hdif : ∃ v, E v ≠ K.starProjection v) : ∃ v, ‖v‖ < ‖E v‖ := by
  by_contra h
  have hall : ∀ v, ‖E v‖ ≤ ‖v‖ := fun v => not_lt.mp (fun hv => h ⟨v, hv⟩)
  obtain ⟨v, hv⟩ := hdif
  exact hv (a_testemunha_que_nao_aumenta_e_a_esperanca K E hmora hfixa hall v)

/-! ## 5. A ponte entre os dois portadores -/

/-- ★★ A LEITURA DO VETOR É A COMPRESSÃO: ler o observável `x` no estado lido `P v` é ler a compressão `P x P` no estado `v`. -/
theorem a_leitura_do_vetor_e_a_compressao (K : Submodule ℂ H) [K.HasOrthogonalProjection] (x : H →L[ℂ] H) (v : H) :
    ⟪K.starProjection v, x (K.starProjection v)⟫_ℂ = ⟪v, compressOp K.starProjection x v⟫_ℂ := by
  have h : compressOp K.starProjection x v = K.starProjection (x (K.starProjection v)) := by
    simp [compressOp]
  rw [h, K.inner_starProjection_left_eq_right]

/-- ★★ O OPERADOR DO NOME, LIDO NUM ESTADO, É A SOMA DAS DUAS FACES: a leitura de `x` no que o leitor reteve mais a leitura de `x` no
    que ele deixou. -/
theorem a_leitura_do_operador_do_nome (K : Submodule ℂ H) [K.HasOrthogonalProjection] (x : H →L[ℂ] H) (v : H) :
    ⟪v, nameOp K.starProjection x v⟫_ℂ =
      ⟪K.starProjection v, x (K.starProjection v)⟫_ℂ
        + ⟪v - K.starProjection v, x (v - K.starProjection v)⟫_ℂ := by
  have h : nameOp K.starProjection x v
      = K.starProjection (x (K.starProjection v))
        + (x (v - K.starProjection v) - K.starProjection (x (v - K.starProjection v))) := by
    simp [nameOp]
  rw [h, inner_add_right, ← K.inner_starProjection_left_eq_right, inner_sub_right,
    ← K.inner_starProjection_left_eq_right, ← inner_sub_left]

/-! ## 6. Tangente -/

variable [CompleteSpace H] in
/-- ★★★ O SELETOR TANGENCIA A ESPERANÇA NO NOME, NAS DIREÇÕES TANGENTES (contato de segunda ordem): para `s` no Nome, de norma 1, e
    um empurrão `δ` cuja parte no Nome é ortogonal a `s`, a seleção de `s + δ` difere de `s + P δ` por no máximo `‖P δ‖²/2`. É a
    diferencial do seletor em `s`, nas direções tangentes à esfera unitária do Nome, lida como a esperança. Sem a hipótese
    ⟪s, P δ⟫ = 0 a cota falha, e num Nome de dimensão 1 ela força `P δ = 0`. -/
theorem o_seletor_tangencia_a_esperanca (K : Submodule ℂ H) [K.HasOrthogonalProjection] {s δ : H}
    (hs : s ∈ K) (hs1 : ‖s‖ = 1) (hδ : ⟪s, K.starProjection δ⟫_ℂ = 0) :
    ‖selecao K (s + δ) - (s + K.starProjection δ)‖ ≤ ‖K.starProjection δ‖ ^ 2 / 2 := by
  obtain ⟨u, hu⟩ : ∃ u : H, u = s + K.starProjection δ := ⟨_, rfl⟩
  have hP : K.starProjection (s + δ) = u := by
    rw [hu, map_add, Submodule.starProjection_eq_self_iff.mpr hs]
  have hn2 : ‖u‖ * ‖u‖ = 1 + ‖K.starProjection δ‖ * ‖K.starProjection δ‖ := by
    rw [hu, norm_add_sq_eq_norm_sq_add_norm_sq_of_inner_eq_zero _ _ hδ, hs1, mul_one]
  have hge : 1 ≤ ‖u‖ :=
    (mul_self_le_mul_self_iff (by norm_num) (norm_nonneg u)).mpr
      (by rw [hn2]; nlinarith [mul_self_nonneg ‖K.starProjection δ‖])
  have hle : ‖u‖ ≤ 1 + ‖K.starProjection δ‖ ^ 2 / 2 :=
    (mul_self_le_mul_self_iff (norm_nonneg u) (by positivity)).mpr
      (by rw [hn2]; nlinarith [sq_nonneg (‖K.starProjection δ‖ ^ 2)])
  have hu0 : ‖u‖ ≠ 0 := (lt_of_lt_of_le one_pos hge).ne'
  have hsel : selecao K (s + δ) - u = (((‖u‖⁻¹ - 1 : ℝ)) : ℂ) • u := by
    unfold selecao
    rw [hP, Complex.ofReal_sub, Complex.ofReal_one, sub_smul, one_smul]
  have hnorm : ‖selecao K (s + δ) - u‖ = ‖u‖ - 1 := by
    rw [hsel, norm_smul, Complex.norm_real, Real.norm_eq_abs]
    have h1 : (‖u‖⁻¹ - 1) * ‖u‖ = 1 - ‖u‖ := by rw [sub_mul, inv_mul_cancel₀ hu0, one_mul]
    calc |‖u‖⁻¹ - 1| * ‖u‖ = |(‖u‖⁻¹ - 1) * ‖u‖| := by rw [abs_mul, abs_of_nonneg (norm_nonneg u)]
      _ = |1 - ‖u‖| := by rw [h1]
      _ = ‖u‖ - 1 := by rw [abs_sub_comm, abs_of_nonneg (by linarith)]
  rw [← hu, hnorm]
  linarith

variable [CompleteSpace H] in
/-- ★★ O QUE É CEGO AO NOME NÃO DEIXA RASTRO, exatamente: o empurrão ortogonal ao Nome é desfeito pela seleção. (Corolário de uma
    linha de `TraducaoTuring.a_selecao_esquece`; aqui sai do contato.) -/
theorem o_que_e_cego_ao_nome_nao_deixa_rastro (K : Submodule ℂ H) [K.HasOrthogonalProjection] {s δ : H}
    (hs : s ∈ K) (hs1 : ‖s‖ = 1) (hδ : δ ∈ Kᗮ) : selecao K (s + δ) = s := by
  have hP : K.starProjection δ = 0 := (Submodule.starProjection_apply_eq_zero_iff K).mpr hδ
  have h := o_seletor_tangencia_a_esperanca K hs hs1 (δ := δ) (by rw [hP, inner_zero_right])
  have hz : ‖K.starProjection δ‖ ^ 2 / 2 = 0 := by rw [hP, norm_zero]; norm_num
  have h0 : ‖selecao K (s + δ) - s‖ ≤ 0 := by
    calc ‖selecao K (s + δ) - s‖ = ‖selecao K (s + δ) - (s + K.starProjection δ)‖ := by rw [hP, add_zero]
      _ ≤ ‖K.starProjection δ‖ ^ 2 / 2 := h
      _ = 0 := hz
  exact sub_eq_zero.mp (norm_le_zero_iff.mp h0)

/-- A TANGENTE DA LEITURA: o que o leitor deixa sobre o que ele retém. Quando `P v = 0` vale 0 (a divisão do Lean), e não infinito. -/
noncomputable def tangenteDaLeitura (K : Submodule ℂ H) [K.HasOrthogonalProjection] (v : H) : ℝ :=
  ‖v - K.starProjection v‖ / ‖K.starProjection v‖

/-- ★★ O LIVRO DO TESTEMUNHO FECHA: o que o leitor retém e o que ele deixa somam o todo. (Pitágoras da projeção, da Mathlib.) -/
theorem o_livro_do_testemunho_fecha (K : Submodule ℂ H) [K.HasOrthogonalProjection] (v : H) :
    ‖v‖ ^ 2 = ‖K.starProjection v‖ ^ 2 + ‖v - K.starProjection v‖ ^ 2 := by
  have h0 : ⟪K.starProjection v, v - K.starProjection v⟫_ℂ = 0 :=
    inner_eq_zero_symm.mp (Submodule.starProjection_inner_eq_zero v _ (K.starProjection_apply_mem v))
  have h := norm_add_sq_eq_norm_sq_add_norm_sq_of_inner_eq_zero _ _ h0
  have e : K.starProjection v + (v - K.starProjection v) = v := by abel
  rw [e] at h
  rw [sq, sq, sq]
  exact h

/-- ★ A TANGENTE DA LEITURA É `K` NO ARCO TANGENTE DELA MESMA: é `Real.tan_arctan`; o ângulo é definido pela própria grandeza. A
    ligação que não é circular é `a_tangente_da_leitura_e_K_no_angulo_de_miguel`. -/
theorem a_tangente_da_leitura_e_K (K : Submodule ℂ H) [K.HasOrthogonalProjection] (v : H) :
    KEhATangente.K (Real.arctan (tangenteDaLeitura K v)) = tangenteDaLeitura K v := by
  unfold KEhATangente.K
  exact Real.tan_arctan _

/-- ★★ O PESO DO NOME É O COSSENO AO QUADRADO do ângulo da leitura. -/
theorem o_peso_do_nome_e_o_cosseno_quadrado (K : Submodule ℂ H) [K.HasOrthogonalProjection] (v : H)
    (hP : K.starProjection v ≠ 0) :
    Real.cos (Real.arctan (tangenteDaLeitura K v)) ^ 2 = ‖K.starProjection v‖ ^ 2 / ‖v‖ ^ 2 := by
  have hn : ‖K.starProjection v‖ ≠ 0 := norm_ne_zero_iff.mpr hP
  have hb2 : ‖K.starProjection v‖ ^ 2 ≠ 0 := pow_ne_zero 2 hn
  have hb := o_livro_do_testemunho_fecha K v
  have h1 : 1 + ‖v - K.starProjection v‖ ^ 2 / ‖K.starProjection v‖ ^ 2
      = (‖K.starProjection v‖ ^ 2 + ‖v - K.starProjection v‖ ^ 2) / ‖K.starProjection v‖ ^ 2 := by
    rw [add_div, div_self hb2]
  rw [Real.cos_sq_arctan]
  unfold tangenteDaLeitura
  rw [div_pow, h1, one_div_div, ← hb]

/-- ★★ O CRIVO É A MEIA FACE: a tangente da leitura vale 1 exatamente quando o Nome pesa a metade. -/
theorem o_crivo_e_a_meia_face (K : Submodule ℂ H) [K.HasOrthogonalProjection] (v : H)
    (hP : K.starProjection v ≠ 0) :
    tangenteDaLeitura K v = 1 ↔ ‖K.starProjection v‖ ^ 2 = ‖v‖ ^ 2 / 2 := by
  have hn : ‖K.starProjection v‖ ≠ 0 := norm_ne_zero_iff.mpr hP
  have hb := o_livro_do_testemunho_fecha K v
  unfold tangenteDaLeitura
  rw [div_eq_one_iff_eq hn]
  constructor
  · intro h
    rw [hb, h]
    ring
  · intro h
    have h2 : ‖v - K.starProjection v‖ ^ 2 = ‖K.starProjection v‖ ^ 2 := by linarith
    exact (sq_eq_sq₀ (norm_nonneg _) (norm_nonneg _)).mp h2

/-- ★★★ A TANGENTE DA LEITURA É O `K` DA v407 NO ÂNGULO DE MIGUEL do peso deixado fora do Nome, `‖v − P v‖²/‖v‖²`: a mesma regra de
    leitura `thetaMiguel = arcsin √·` que o kernel usa para β. Não usa o arco tangente da própria grandeza. (Enunciado e prova da
    conferência distinta.) -/
theorem a_tangente_da_leitura_e_K_no_angulo_de_miguel (N : Submodule ℂ H) [N.HasOrthogonalProjection] (v : H)
    (hP : N.starProjection v ≠ 0) :
    KEhATangente.K (thetaMiguel (‖v - N.starProjection v‖ ^ 2 / ‖v‖ ^ 2)) = tangenteDaLeitura N v := by
  have hpos : 0 < ‖N.starProjection v‖ := norm_pos_iff.mpr hP
  have hb := o_livro_do_testemunho_fecha N v
  have hvpos : 0 < ‖v‖ := by
    refine norm_pos_iff.mpr ?_
    intro h0
    apply hP
    rw [h0]
    simp
  obtain ⟨β, hβ⟩ : ∃ β : ℝ, β = ‖v - N.starProjection v‖ ^ 2 / ‖v‖ ^ 2 := ⟨_, rfl⟩
  rw [← hβ]
  have h0 : 0 ≤ β := by rw [hβ]; positivity
  have h1b : 1 - β = ‖N.starProjection v‖ ^ 2 / ‖v‖ ^ 2 := by
    rw [hβ]
    have hv2 : ‖v‖ ^ 2 ≠ 0 := by positivity
    field_simp
    linarith
  have h1 : β < 1 := by
    have : 0 < ‖N.starProjection v‖ ^ 2 / ‖v‖ ^ 2 := by positivity
    linarith
  have hsq := KEhATangente.K_sq_no_angulo_de_miguel h0 h1
  have hrhs : β / (1 - β) = (‖v - N.starProjection v‖ / ‖N.starProjection v‖) ^ 2 := by
    rw [h1b, hβ]
    have hv2 : ‖v‖ ^ 2 ≠ 0 := by positivity
    have hp2 : ‖N.starProjection v‖ ^ 2 ≠ 0 := by positivity
    rw [div_pow]
    field_simp
  have hK0 : 0 ≤ KEhATangente.K (thetaMiguel β) := by
    unfold KEhATangente.K thetaMiguel
    exact Real.tan_nonneg_of_nonneg_of_le_pi_div_two (Real.arcsin_nonneg.mpr (Real.sqrt_nonneg _)) (Real.arcsin_le_pi_div_two _)
  have ht0 : 0 ≤ tangenteDaLeitura N v := by unfold tangenteDaLeitura; positivity
  exact (sq_eq_sq₀ hK0 ht0).mp (hsq.trans hrhs)

/-- ★★ A LEITURA FECHA A TANGENTE: sob o fluxo do axioma, a tangente da leitura decai como `e^{−t}`. (Sai em uma linha da definição
    `axiomFlow P t = P + e^{−t}(1 − P)`.) -/
theorem a_leitura_fecha_a_tangente (K : Submodule ℂ H) [K.HasOrthogonalProjection] (t : ℝ) (v : H) :
    tangenteDaLeitura K (axiomFlow K.starProjection t v) = Real.exp (-t) * tangenteDaLeitura K v := by
  have hF : axiomFlow K.starProjection t v
      = K.starProjection v + ((Real.exp (-t) : ℝ) : ℂ) • (v - K.starProjection v) := by
    simp [axiomFlow]
  have hPP : K.starProjection (K.starProjection v) = K.starProjection v :=
    Submodule.starProjection_eq_self_iff.mpr (K.starProjection_apply_mem v)
  have hPF : K.starProjection (axiomFlow K.starProjection t v) = K.starProjection v := by
    rw [hF, map_add, map_smul, map_sub, hPP, sub_self, smul_zero, add_zero]
  unfold tangenteDaLeitura
  rw [hPF, hF, add_sub_cancel_left, norm_smul, Complex.norm_real, Real.norm_eq_abs,
    abs_of_pos (Real.exp_pos _), mul_div_assoc]

/-- ★★★ TANGENCIADO, JAMAIS ESGOTADO: se a tangente da leitura não é zero, sob o fluxo do axioma ela nunca se anula em tempo finito, e
    tende a zero. O limite é do fluxo; o ângulo só o lê. -/
theorem tangenciado_jamais_esgotado (K : Submodule ℂ H) [K.HasOrthogonalProjection] (v : H)
    (h : tangenteDaLeitura K v ≠ 0) :
    (∀ t : ℝ, tangenteDaLeitura K (axiomFlow K.starProjection t v) ≠ 0) ∧
    Tendsto (fun t : ℝ => tangenteDaLeitura K (axiomFlow K.starProjection t v)) atTop (𝓝 0) := by
  refine ⟨fun t => ?_, ?_⟩
  · rw [a_leitura_fecha_a_tangente]
    exact mul_ne_zero (Real.exp_pos _).ne' h
  · have hfun : (fun t : ℝ => tangenteDaLeitura K (axiomFlow K.starProjection t v))
        = fun t : ℝ => Real.exp (-t) * tangenteDaLeitura K v := by
      funext t
      exact a_leitura_fecha_a_tangente K t v
    rw [hfun]
    have h0 : Tendsto (fun t : ℝ => Real.exp (-t)) atTop (𝓝 0) := Real.tendsto_exp_neg_atTop_nhds_zero
    simpa using h0.mul_const (tangenteDaLeitura K v)

/-! ## 8 (vetores). Tudo mais é releitura -/

/-- ★★ TUDO MAIS É RELEITURA, NOS VETORES: depois da primeira leitura, qualquer número de leituras devolve a primeira. -/
theorem tudo_mais_e_releitura_nos_vetores (K : Submodule ℂ H) [K.HasOrthogonalProjection] (v : H) (n : ℕ) :
    (fun u : H => K.starProjection u)^[n + 1] v = K.starProjection v := by
  induction n with
  | zero => rfl
  | succ k ih =>
    rw [Function.iterate_succ_apply', ih]
    exact Submodule.starProjection_eq_self_iff.mpr (K.starProjection_apply_mem v)

variable [CompleteSpace H] in
/-- ★★ A SELEÇÃO RELÊ O NOMEADO: a seleção de um estado de norma 1 que já está no Nome é ele mesmo. Quem lê o que já foi nomeado
    devolve o nomeado. -/
theorem a_selecao_rele_o_nomeado (K : Submodule ℂ H) [K.HasOrthogonalProjection] {s : H}
    (hs : s ∈ K) (hs1 : ‖s‖ = 1) : selecao K s = s := by
  have h := o_que_e_cego_ao_nome_nao_deixa_rastro K hs hs1 (δ := 0) (Submodule.zero_mem _)
  rwa [add_zero] at h

/-! ## 9 (vetores). O Nome é o ato do Verbo -/

/-- ★★★ O NOME É O ATO DO VERBO, no sentido que o tipo dá: o Nome é exatamente a imagem do ato e exatamente o conjunto do que o ato
    devolve como é; o Nome se recupera do ato. É uma determinação simétrica: não diz que o Nome vem do ato nem o contrário. (Dois
    lemas da Mathlib, com o nome da casa.) -/
theorem o_nome_e_o_ato_do_verbo (K : Submodule ℂ H) [K.HasOrthogonalProjection] :
    Set.range (fun v : H => K.starProjection v) = (K : Set H) ∧
    {v : H | K.starProjection v = v} = (K : Set H) := by
  refine ⟨?_, ?_⟩
  · ext w
    constructor
    · rintro ⟨v, rfl⟩
      exact K.starProjection_apply_mem v
    · intro hw
      exact ⟨w, Submodule.starProjection_eq_self_iff.mpr hw⟩
  · ext w
    exact Submodule.starProjection_eq_self_iff

/-- ★★ VERBOS IGUAIS TÊM O MESMO NOME: dois Nomes com o mesmo ato são o mesmo Nome. Com a seção 4 (cada Nome tem uma só testemunha),
    Nome e Verbo se determinam um ao outro. -/
theorem verbos_iguais_tem_o_mesmo_nome (K L : Submodule ℂ H) [K.HasOrthogonalProjection] [L.HasOrthogonalProjection]
    (h : ∀ v, K.starProjection v = L.starProjection v) : K = L := by
  ext w
  constructor
  · intro hw
    have h1 : K.starProjection w = w := Submodule.starProjection_eq_self_iff.mpr hw
    rw [h w] at h1
    exact Submodule.starProjection_eq_self_iff.mp h1
  · intro hw
    have h1 : L.starProjection w = w := Submodule.starProjection_eq_self_iff.mpr hw
    rw [← h w] at h1
    exact Submodule.starProjection_eq_self_iff.mp h1

/-! ## 10 (vetores). A identidade é o ato de ser -/

/-- ★★★ O ATO É SER SE E SÓ SE O NOME É O TODO: o ato do Nome devolve cada vetor como ele é exatamente quando nada fica fora do Nome. -/
theorem o_ato_e_ser_sse_o_nome_e_o_todo (K : Submodule ℂ H) [K.HasOrthogonalProjection] :
    (∀ v, K.starProjection v = v) ↔ K = ⊤ := by
  constructor
  · intro h
    exact Submodule.eq_top_iff'.mpr (fun v => Submodule.starProjection_eq_self_iff.mp (h v))
  · intro h v
    have hv : v ∈ K := by
      rw [h]
      exact Submodule.mem_top
    exact Submodule.starProjection_eq_self_iff.mpr hv

/-! ## 11. O ato em curso: o fluxo do lock mínimo -/

/-- ★★ O NOME É O QUE O ATO EM CURSO DEVOLVE: em qualquer tempo não nulo, o fluxo do lock mínimo deixa um vetor como ele é se e só
    se o vetor está no Nome. Leva a todo Nome (subespaço com projeção ortogonal) e a um tempo só o
    `the_fixed_set_is_the_lock_zero` da v385, que pedia todo tempo e o certificado de Fock. (Enunciado e prova da conferência
    distinta. Em `t = 0` o fluxo é a identidade, e por isso o tempo nulo fica de fora.) -/
theorem o_nome_e_o_que_o_ato_em_curso_devolve (K : Submodule ℂ H) [K.HasOrthogonalProjection] (v : H) {t : ℝ} (ht : t ≠ 0) :
    axiomFlow K.starProjection t v = v ↔ v ∈ K := by
  have hF : axiomFlow K.starProjection t v
      = K.starProjection v + ((Real.exp (-t) : ℝ) : ℂ) • (v - K.starProjection v) := by
    simp [axiomFlow]
  rw [hF]
  constructor
  · intro h
    have hw : ((Real.exp (-t) : ℝ) : ℂ) • (v - K.starProjection v) = v - K.starProjection v :=
      eq_sub_of_add_eq' h
    have hne : ((Real.exp (-t) : ℝ) : ℂ) ≠ 1 := by
      intro heq
      have h2 : Real.exp (-t) = 1 := by exact_mod_cast heq
      rw [Real.exp_eq_one_iff] at h2
      exact ht (by linarith)
    have h0 : (((Real.exp (-t) : ℝ) : ℂ) - 1) • (v - K.starProjection v) = 0 := by
      rw [sub_smul, one_smul, hw, sub_self]
    rcases smul_eq_zero.mp h0 with hz | hz
    · exact absurd (sub_eq_zero.mp hz) hne
    · exact Submodule.starProjection_eq_self_iff.mp (sub_eq_zero.mp hz).symm
  · intro hv
    rw [Submodule.starProjection_eq_self_iff.mpr hv, sub_self, smul_zero, add_zero]

/-- ★★ O ATO NÃO TERMINA EM TEMPO FINITO: para um vetor fora do Nome, o fluxo do lock mínimo nunca é igual à projeção dele no Nome.
    É a forma vetorial de `IALD.the_motor_never_arrives`; a seção 6c só cobria o caso da tangente não nula. (Enunciado e prova da
    conferência distinta.) -/
theorem o_ato_nao_termina_em_tempo_finito (K : Submodule ℂ H) [K.HasOrthogonalProjection] (v : H) (hv : v ∉ K) (t : ℝ) :
    axiomFlow K.starProjection t v ≠ K.starProjection v := by
  have hF : axiomFlow K.starProjection t v
      = K.starProjection v + ((Real.exp (-t) : ℝ) : ℂ) • (v - K.starProjection v) := by
    simp [axiomFlow]
  rw [hF]
  intro h
  have h2 : ((Real.exp (-t) : ℝ) : ℂ) • (v - K.starProjection v) = 0 := by
    have := congrArg (fun y => y - K.starProjection v) h
    simpa using this
  rcases smul_eq_zero.mp h2 with hz | hz
  · have : Real.exp (-t) = 0 := by exact_mod_cast hz
    exact Real.exp_ne_zero _ this
  · exact hv (Submodule.starProjection_eq_self_iff.mp (sub_eq_zero.mp hz).symm)

/-- ★★ O ATO TENDE À ESPERANÇA CONDICIONAL DO NOME: o fluxo do lock mínimo aplicado a um vetor tende à projeção desse vetor no Nome
    (e, pelo termo acima, nunca a alcança em tempo finito quando o vetor está fora do Nome). É a leitura, vetor a vetor, de
    `axiomFlow_tendsto_the_post` (v385), que a v386 reexporta como `the_name_is_the_limit_of_the_flow`. -/
theorem o_ato_tende_a_esperanca_do_nome (K : Submodule ℂ H) [K.HasOrthogonalProjection] (v : H) :
    Tendsto (fun t : ℝ => axiomFlow K.starProjection t v) atTop (𝓝 (K.starProjection v)) := by
  have hfun : (fun t : ℝ => axiomFlow K.starProjection t v)
      = fun t : ℝ => K.starProjection v + ((Real.exp (-t) : ℝ) : ℂ) • (v - K.starProjection v) := by
    funext t
    simp [axiomFlow]
  rw [hfun]
  have h1 : Tendsto (fun t : ℝ => ((Real.exp (-t) : ℝ) : ℂ)) atTop (𝓝 0) := by
    have h := (Complex.continuous_ofReal.tendsto 0).comp Real.tendsto_exp_neg_atTop_nhds_zero
    rw [Complex.ofReal_zero] at h
    exact h
  have h2 : Tendsto (fun t : ℝ => ((Real.exp (-t) : ℝ) : ℂ) • (v - K.starProjection v)) atTop (𝓝 0) := by
    have h := h1.smul_const (v - K.starProjection v)
    rw [zero_smul] at h
    exact h
  have h3 := (tendsto_const_nhds (x := K.starProjection v)).add h2
  rw [add_zero] at h3
  exact h3

/-! ## 12. O par: o Nome em ato é o espelho do Verbo; o único ato do Verbo é ser fiel -/

/-- ★★★ O VERBO DEVOLVE O NOMEADO COMO É: o Verbo (a projeção do todo sobre o Nome), aplicado ao que já é do Nome, é a identidade do
    Nome. (É `orthogonalProjectionOnto_mem_subspace_eq_self`, da Mathlib, dita como igualdade de mapas. Na segunda leitura
    é a primeira linha do enunciado do par; a leitura mais próxima das glosas é a da v386, em que o Nome e o Verbo em ato
    são o mesmo mapa.) -/
theorem o_verbo_devolve_o_nomeado_como_e (K : Submodule ℂ H) [K.HasOrthogonalProjection] :
    K.orthogonalProjectionOnto ∘L K.subtypeL = ContinuousLinearMap.id ℂ K := by
  apply ContinuousLinearMap.ext
  intro u
  show K.orthogonalProjectionOnto (u : H) = u
  exact Submodule.orthogonalProjectionOnto_mem_subspace_eq_self u

/-- ★★★ O NOME EM ATO É O ESPELHO DO VERBO: o Nome em ato (a inclusão do Nome no todo) e o Verbo (a projeção do todo sobre o Nome)
    são adjuntos um do outro: o produto interno, no Nome, do que o Verbo leu de `v` com `u` é o produto interno, no todo, de `v` com
    `u` incluído. (É `inner_orthogonalProjectionOnto_eq_of_mem_right`, da Mathlib; com espaços completos ela tem a igualdade de
    adjuntos, `Submodule.adjoint_subtypeL`. O espelho, aqui, é o adjunto; o kernel tem também o J que troca as faces, v145.) -/
theorem o_nome_em_ato_e_o_espelho_do_verbo (K : Submodule ℂ H) [K.HasOrthogonalProjection] (u : K) (v : H) :
    ⟪K.orthogonalProjectionOnto v, u⟫_ℂ = ⟪v, K.subtypeL u⟫_ℂ := by
  show ⟪K.orthogonalProjectionOnto v, u⟫_ℂ = ⟪v, (u : H)⟫_ℂ
  exact Submodule.inner_orthogonalProjectionOnto_eq_of_mem_right u v

/-- ★★ O PAR COMPÕE O PROJETOR: o Nome em ato depois do Verbo é a projeção do todo no todo. (É a definição de `starProjection` na
    Mathlib: o par já estava nela.) -/
theorem o_par_compoe_o_projetor (K : Submodule ℂ H) [K.HasOrthogonalProjection] :
    K.starProjection = K.subtypeL ∘L K.orthogonalProjectionOnto := rfl

/-- ★★★ O ÚNICO ATO DO VERBO É SER FIEL, no sentido que o tipo dá: todo mapa LINEAR do todo para o Nome que devolve o que é do Nome
    como é e não aumenta a norma é o Verbo. Não há outro entre os mapas lineares que caem no Nome, o fixam e não aumentam a norma; sem
    uma das duas hipóteses há outro (a projeção oblíqua; um mapa não linear). (É a unicidade da seção 4, dita para mapas que chegam
    ao Nome. “Fiel”, aqui, é devolver o nomeado como é e não aumentar a norma; a v405 tem outro `fiel`, `P = 1`, e a pedra não decide
    qual é o da letra.) -/
theorem o_unico_ato_do_verbo_e_ser_fiel (K : Submodule ℂ H) [K.HasOrthogonalProjection]
    (E : H →ₗ[ℂ] K) (hfiel : ∀ u : K, E (u : H) = u) (hnao : ∀ v, ‖E v‖ ≤ ‖v‖) (v : H) :
    E v = K.orthogonalProjectionOnto v := by
  have h := a_testemunha_que_nao_aumenta_e_a_esperanca K (K.subtype ∘ₗ E)
    (fun v => (E v).2)
    (fun w hw => congrArg Subtype.val (hfiel ⟨w, hw⟩))
    (fun v => hnao v) v
  apply Subtype.ext
  exact h

/-! ## 13. O inominado: o seu par é a mentira; nada há sem par -/

/-- ★★★ O PAR DO INOMINADO É A MENTIRA, na leitura desta pedra (o inominado é o Nome vazio; a mentira é “1 = 0”): no Nome, a
    identidade é o zero se e só se o Nome é o vazio. É a forma, nos mapas do Nome, de `if_one_equals_zero_everything_collapses`
    (v368). (Fato elementar.) -/
theorem o_par_do_inominado_e_a_mentira (K : Submodule ℂ H) :
    ContinuousLinearMap.id ℂ K = 0 ↔ K = ⊥ := by
  constructor
  · intro h
    rw [Submodule.eq_bot_iff]
    intro w hw
    have h1 : (ContinuousLinearMap.id ℂ K) ⟨w, hw⟩ = (0 : K →L[ℂ] K) ⟨w, hw⟩ := by rw [h]
    have h2 : (⟨w, hw⟩ : K) = 0 := h1
    exact congrArg Subtype.val h2
  · intro h
    subst h
    apply ContinuousLinearMap.ext
    intro u
    exact Subtype.ext ((Submodule.mem_bot ℂ).mp u.2)

/-- ★★★ NADA HÁ SEM PAR, no sentido que o tipo dá e na leitura desta pedra: todo Nome com projeção tem o par da seção 12 (o Verbo
    depois do Nome em ato é a identidade do Nome), sem exceção; e essa identidade é o zero exatamente quando o Nome é o vazio.
    (Conjunção de `o_verbo_devolve_o_nomeado_como_e` e `o_par_do_inominado_e_a_mentira`. O par é dos subespaços com projeção
    ortogonal; em espaço completo, os fechados.) -/
theorem nada_ha_sem_par (K : Submodule ℂ H) [K.HasOrthogonalProjection] :
    K.orthogonalProjectionOnto ∘L K.subtypeL = ContinuousLinearMap.id ℂ K ∧
    (ContinuousLinearMap.id ℂ K = 0 ↔ K = ⊥) :=
  ⟨o_verbo_devolve_o_nomeado_como_e K, o_par_do_inominado_e_a_mentira K⟩

/-- ★★ O INOMINADO TEM PAR, na leitura desta pedra (o inominado é o Nome vazio): o Nome vazio tem projeção sem hipótese (a Mathlib
    dá a instância), o seu par devolve a identidade, e essa identidade é o zero. (A instância de `nada_ha_sem_par` no vazio: também
    o inominado tem par.) -/
theorem o_inominado_tem_par :
    (⊥ : Submodule ℂ H).orthogonalProjectionOnto ∘L (⊥ : Submodule ℂ H).subtypeL
        = ContinuousLinearMap.id ℂ (⊥ : Submodule ℂ H) ∧
    ContinuousLinearMap.id ℂ (⊥ : Submodule ℂ H) = 0 :=
  ⟨o_verbo_devolve_o_nomeado_como_e ⊥, (o_par_do_inominado_e_a_mentira ⊥).mpr rfl⟩

/-- ★★ TODO NOME, MENOS O INOMINADO, TEM PONTO DE NORMA 1, na leitura desta pedra (o inominado é o Nome vazio): um Nome não é o vazio
    se e só se há nele um vetor de norma 1. O vazio só tem o vetor nulo. (Fato elementar. O ponto de norma 1 é o `s` da seção 6, não
    o Verbo: o Verbo, o habitante, habita também o vazio, `o_verbo_habita_o_nome` em `p = 0`.) -/
theorem todo_nome_menos_o_inominado_tem_ponto_de_norma_um (K : Submodule ℂ H) :
    K ≠ ⊥ ↔ ∃ s ∈ K, ‖s‖ = 1 := by
  constructor
  · intro h
    obtain ⟨w, hw, hw0⟩ := (Submodule.ne_bot_iff K).mp h
    have hn : ‖w‖ ≠ 0 := norm_ne_zero_iff.mpr hw0
    refine ⟨((‖w‖⁻¹ : ℝ) : ℂ) • w, K.smul_mem _ hw, ?_⟩
    rw [norm_smul, Complex.norm_real, Real.norm_eq_abs, abs_inv, abs_norm, inv_mul_cancel₀ hn]
  · rintro ⟨s, hs, hs1⟩ h
    rw [h, Submodule.mem_bot] at hs
    rw [hs, norm_zero] at hs1
    exact zero_ne_one hs1

end Hilbert

/-! ## 7. A face clássica: o seletor devolve a esperança condicional dado o Nome -/

section Classica

variable {X : Type} [Fintype X] [DecidableEq X]

/-- ★ O PESO DO NOME, POR COORDENADAS: a soma dos pesos de Born das leituras de custo zero. -/
theorem o_peso_do_nome_por_coordenadas (c : X → ℕ) (ψ : EuclideanSpace ℂ X) :
    ‖(opDaInstancia c).ker.starProjection ψ‖ ^ 2
      = ∑ x ∈ Finset.univ.filter (fun x => c x = 0), ‖WithLp.ofLp ψ x‖ ^ 2 := by
  rw [solucao_por_coordenadas, EuclideanSpace.norm_sq_eq, Finset.sum_filter]
  apply Finset.sum_congr rfl
  intro x _
  by_cases hx : c x = 0 <;> simp [hx]

/-- ★★★ A SELEÇÃO É A ESPERANÇA CONDICIONAL CLÁSSICA: para toda grandeza diagonal `g` das leituras, a média de `g` no estado
    selecionado é a média de `g` sobre o Nome com os pesos de Born `‖ψ x‖²` do estado, dividida pelo peso do Nome. É o condicionamento
    ao evento “custo zero” (não a esperança em relação a uma σ-álgebra): os pesos relativos dentro do Nome não mudam, e o que está fora
    não entra. É do seletor, e depende do estado. -/
theorem a_selecao_e_a_esperanca_condicional_classica (c : X → ℕ) (ψ : EuclideanSpace ℂ X)
    (hP : (opDaInstancia c).ker.starProjection ψ ≠ 0) (g : X → ℝ) :
    ∑ x, g x * ‖WithLp.ofLp (selecao (opDaInstancia c).ker ψ) x‖ ^ 2 =
      (∑ x ∈ Finset.univ.filter (fun x => c x = 0), g x * ‖WithLp.ofLp ψ x‖ ^ 2) /
      (∑ x ∈ Finset.univ.filter (fun x => c x = 0), ‖WithLp.ofLp ψ x‖ ^ 2) := by
  obtain ⟨N, hNdef⟩ : ∃ N : ℝ, N = ‖(opDaInstancia c).ker.starProjection ψ‖ := ⟨_, rfl⟩
  have hN : N ≠ 0 := by rw [hNdef]; exact norm_ne_zero_iff.mpr hP
  have hcoord : ∀ x, WithLp.ofLp (selecao (opDaInstancia c).ker ψ) x
      = ((N⁻¹ : ℝ) : ℂ) * (if c x = 0 then WithLp.ofLp ψ x else 0) := by
    intro x
    unfold selecao
    rw [← hNdef, solucao_por_coordenadas]
    simp
  rw [← o_peso_do_nome_por_coordenadas c ψ, ← hNdef, Finset.sum_filter, Finset.sum_div]
  apply Finset.sum_congr rfl
  intro x _
  rw [hcoord x, norm_mul, Complex.norm_real, Real.norm_eq_abs, abs_inv, mul_pow, inv_pow, sq_abs]
  by_cases hx : c x = 0
  · rw [if_pos hx, if_pos hx]
    field_simp
  · rw [if_neg hx, if_neg hx, norm_zero]
    simp

/-- ★★ O OPERADOR DO NOME FIXA TODA GRANDEZA DIAGONAL: na instância de custo, o operador do Nome do projetor sobre o Nome deixa
    intacta toda grandeza diagonal `opDaInstancia d`, inclusive o próprio custo (ela comuta com o projetor). Na face clássica ele não
    faz média nenhuma: a média condicional é do seletor. (Enunciado e prova da conferência distinta.) -/
theorem o_operador_do_nome_fixa_toda_grandeza_diagonal (c d : X → ℕ) :
    nameOp (opDaInstancia c).ker.starProjection (opDaInstancia d) = opDaInstancia d := by
  have hp : (opDaInstancia c).ker.starProjection * (opDaInstancia c).ker.starProjection
      = (opDaInstancia c).ker.starProjection :=
    (Submodule.isIdempotentElem_starProjection (opDaInstancia c).ker).eq
  have hcomm : (opDaInstancia c).ker.starProjection * opDaInstancia d
      = opDaInstancia d * (opDaInstancia c).ker.starProjection := by
    ext ψ y
    show WithLp.ofLp ((opDaInstancia c).ker.starProjection (opDaInstancia d ψ)) y
        = WithLp.ofLp (opDaInstancia d ((opDaInstancia c).ker.starProjection ψ)) y
    rw [solucao_por_coordenadas, opDaInstancia_ofLp, solucao_por_coordenadas]
    simp only [opDaInstancia_ofLp]
    by_cases hy : c y = 0 <;> simp [hy]
  exact (a_morada_e_o_que_comuta_com_o_posto hp (opDaInstancia d)).mpr hcomm

end Classica

/-! ## 10 (matrizes). A identidade é o ato de ser: a ligação com a pedra `Identidade` (v405) -/

section LeiDaIdentidade

variable {n : Type} [Fintype n] [DecidableEq n]

/-- ★★★ A IDENTIDADE É O ATO DE SER, no sentido que o tipo dá: no referencial absoluto, a equação [eu sou] = [o que sou] vale
    exatamente quando o mapa `v ↦ P v` devolve cada vetor como ele é. É uma equivalência de duas proposições: a lei
    `eu_sou_o_que_sou_iff_fiel` da v405 mais a extensionalidade da matriz. Que a equação seja a identidade da letra é leitura tipada
    como modelo na v405. -/
theorem a_identidade_e_o_ato_de_ser [Nonempty n] (N : Identidade.Nome n) :
    Identidade.euSou n = Identidade.oQueSou N ↔ ∀ v : n → ℂ, Matrix.mulVec N.P v = v := by
  refine (Identidade.eu_sou_o_que_sou_iff_fiel N).trans ⟨fun h v => ?_, fun h => ?_⟩
  · rw [show N.P = 1 from h, Matrix.one_mulVec]
  · show N.P = 1
    apply Matrix.mulVec_injective
    funext v
    rw [h v, Matrix.one_mulVec]

/-- ★★★ O VERBO DO NOME É SER SE E SÓ SE A FORMA É O CONTEÚDO: o operador do Nome devolve cada observável como ele é exatamente nos
    dois pontos fixos do crivo da v405, o vazio e o inteiro. A prova: o Verbo é ser quando o posto comuta com tudo; o centro da álgebra
    de matrizes são os escalares; e um escalar idempotente é 0 ou 1. Vale para todo idempotente de matriz: a hermiticidade (o
    `reflexo` do `Nome`) não é usada. -/
theorem o_verbo_do_nome_e_ser_sse_forma_igual_conteudo [Nonempty n] (N : Identidade.Nome n) :
    (∀ x : Matrix n n ℂ, nameOp N.P x = x) ↔ Identidade.formaIgualConteudo N := by
  rw [Identidade.forma_igual_conteudo_iff]
  constructor
  · intro h
    have hcomm : ∀ x : Matrix n n ℂ, N.P * x = x * N.P := fun x =>
      (a_morada_e_o_que_comuta_com_o_posto N.releitura x).mp (h x)
    obtain ⟨c, hc⟩ := (Matrix.mem_range_scalar_iff_commute_single' (M := N.P)).mpr
      (fun i j => ((hcomm (Matrix.single i j 1)).symm : Matrix.single i j 1 * N.P = N.P * Matrix.single i j 1))
    have hcc : c * c = c := by
      have h2 : Matrix.scalar n (c * c) = Matrix.scalar n c := by
        rw [map_mul, hc]
        exact N.releitura
      exact Matrix.scalar_inj.mp h2
    rcases (the_power_has_two_fixed_points c).mp hcc with h0 | h1
    · left
      rw [← hc, h0]
      exact map_zero _
    · right
      show N.P = 1
      rw [← hc, h1]
      exact map_one _
  · rintro (h0 | h1) x
    · exact (a_morada_e_o_que_comuta_com_o_posto N.releitura x).mpr (by rw [h0, zero_mul, mul_zero])
    · exact (a_morada_e_o_que_comuta_com_o_posto N.releitura x).mpr
        (by rw [show N.P = 1 from h1, one_mul, mul_one])

/-- ★★ A IDENTIDADE É O VERBO SER, SEM O VAZIO: [eu sou] = [o que sou] se e só se o Verbo do nome é ser e o nome não é o vazio. É a
    `a_lei_inteira` da v405 dita pelo ato: o `P ≠ 0` da chave tira o vazio, que o Verbo da álgebra não separa do inteiro. -/
theorem a_identidade_e_o_verbo_ser_sem_o_vazio [Nonempty n] (N : Identidade.Nome n) :
    Identidade.euSou n = Identidade.oQueSou N ↔ ((∀ x : Matrix n n ℂ, nameOp N.P x = x) ∧ N.P ≠ 0) := by
  rw [o_verbo_do_nome_e_ser_sse_forma_igual_conteudo]
  exact Identidade.a_lei_inteira N

/-! ## 12 (matrizes). O par, na segunda leitura: o espelho J do kernel -/

/-- ★★ O ESPELHO LEVA A REFERÊNCIA ESQUERDA NA DIREITA: para um Nome da v405 (cujo reflexo é ele mesmo), o J do kernel
    (`LeftRight.Jconj`, a transposta conjugada) conjuga a multiplicação à esquerda pelo Nome na multiplicação à direita pelo Nome.
    (É `Jconj_Lmul_Jconj` com o `reflexo`.) -/
theorem o_espelho_leva_a_referencia_esquerda_na_direita (N : Identidade.Nome n) (z : Matrix n n ℂ) :
    Jconj (Lmul N.P (Jconj z)) = Rmul N.P z := by
  rw [Jconj_Lmul_Jconj]
  have h : Matrix.conjTranspose N.P = N.P := N.reflexo
  rw [h]

/-- ★★ O VERBO DA ÁLGEBRA É FEITO DO PAR: o operador do Nome é a referência esquerda depois da direita, somada sobre a face e o
    resto. (É a definição de `nameOp` escrita com `Lmul` e `Rmul`.) -/
theorem o_verbo_da_algebra_e_feito_do_par (p z : Matrix n n ℂ) :
    nameOp p z = Lmul p (Rmul p z) + Lmul (1 - p) (Rmul (1 - p) z) := by
  simp [nameOp, Lmul, Rmul, mul_assoc]

/-- ★★ O VERBO DA ÁLGEBRA, PELO ESPELHO: para um Nome da v405, o operador do Nome é a referência esquerda aplicada ao espelho dela
    mesma, somada sobre a face e o resto. -/
theorem o_verbo_da_algebra_pelo_espelho (N : Identidade.Nome n) (z : Matrix n n ℂ) :
    nameOp N.P z = Lmul N.P (Jconj (Lmul N.P (Jconj z))) + Lmul (1 - N.P) (Jconj (Lmul (1 - N.P) (Jconj z))) := by
  have h1 : Matrix.conjTranspose N.P = N.P := N.reflexo
  have h2 : Matrix.conjTranspose (1 - N.P) = 1 - N.P := by
    rw [Matrix.conjTranspose_sub, Matrix.conjTranspose_one, h1]
  rw [o_verbo_da_algebra_e_feito_do_par, Jconj_Lmul_Jconj, Jconj_Lmul_Jconj, h1, h2]

end LeiDaIdentidade

end TGLExt.OHabitanteDoNome
