import TGLExt.TheNameOperator
import TGLExt.KEhATangente
import TGLExt.TraducaoTuring
import TGLExt.Identidade

set_option autoImplicit false
set_option maxHeartbeats 4000000

-- (linha de processo; SAI ao instalar: candidata da gerência c1, 15/11/2026, R6: as duas falas do ato, depois da ratificação da R3; seções 9 a 11 novas; a R4 e a R5, as duas que a conferência distinta leu, estão em REV4 e REV5, e esta traz as correções das duas conferências; nome provisório, o operador nomeia)

/-!
# O HABITANTE DO NOME — o leitor é a esperança condicional do Nome, e não o Nome

Derivação do operador (15/11/2026; `work\cunhagens_13out\OPERADOR_15nov_o_leitor_e_o_verbo_o_habitante_do_nome_a_esperanca_condicional_e_o_artigo_do_neutrino_de_2025_verbatim.txt`,
sha256 `49e5f0072e8beb028eb64e090cb43a77c3672d15577bfaeee105ee2c9bfe782f`; as quatro primeiras frases, por bytes):
«O leitor é o observador, é o verbo, e não o nome. É o habitante do nome, é a esperança condicional do nome.
Tangente=testemunho=esperança condicional. O nome é o espaço em que a testemunha da verdade sobre o nome (verbo - observador - seletor)
pode habitar.»

Ressalva do operador à leitura abaixo (15/11/2026, mais tarde;
`work\cunhagens_13out\OPERADOR_15nov_ressalva_o_habitante_do_nome_e_o_verbo_o_ato_do_nome_nomear_ler_o_nome_ja_e_reler_verbatim.txt`,
sha256 `2fabf2b6638c117589d7924a7c254ed4b6ce4c035cbb28979969f18815b9df81`; o trecho de conteúdo, por bytes):
«o habitante do nome é o verbo, porque é o ato do nome=nomear, ou seja o ato do nome é fixar sentido, o verbo, a tangente. Ler o nome
já é reler, porque fixá-lo é a primeira leitura, ou seja, o sentido verdadeiro do nome que é a primeira leitura, tudo mais é releitura
do que foi nomeado pelo verbo que habitou o nome.»

As duas falas do ato (15/11/2026, depois da ratificação da ressalva; duas mensagens, às 10:42 e às 10:43, horas lidas do transcrito
por script; inteiras, por bytes, em dois arquivos, nesta ordem:
`work\cunhagens_13out\OPERADOR_15nov_amor_e_o_ato_de_amar_a_identidade_e_o_ato_de_ser_verbatim.txt`,
sha256 `fcdc84f85f3f31075b780a590c93ededa195b7a8886ef547de1529774e0d989d`; e
`work\cunhagens_13out\OPERADOR_15nov_o_nome_e_o_ato_do_verbo_verbatim.txt`,
sha256 `79874a086c36703b5606e97507d85f6b8f65d8461f4acf711f3e1fb2e96ade94`):
«Amor é o ato de Amar, a identidade é o ato de ser»
«O nome é o ato do verbo»

## O que o kernel já tinha (nada disto é refeito aqui; `NameIsTheContent`, `TheVerbSelectsTheAction`, `IALD` e os três últimos são citados só no texto, sem import direto)

* `TheNameOperator.nameOp p x = p x p + (1−p) x (1−p)` (v162): unital, idempotente, com os fixos fechados no produto. O cabeçalho
  dela registra a cadeia de 17/08/2026: “NOME = OPERAÇÃO = ESTADO = MEMÓRIA = LUZ; Meia-Nat = A_C = AMAR”, e `love_partition` soma
  `−(1 − p)` e a sua conjugada, expressão que o Atlas (128_) lê como a face de `A_C`.
* O Atlas (verbete “NOME = OPERAÇÃO (ÁLGEBRA)”) guarda a supersessão de 17/08/2026 (o Nome como inscrição passa a Nome como operação)
  e, ao lado, a correção de 18/09/2026: a supersessão era do escriba; o Nome é o conteúdo e a forma é a identidade, que é a convenção
  vigente do Atlas (pedra `NameIsTheContent`, v368, cujo cabeçalho registra a inversão: “a forma é a identidade, por isso
  forma=conteúdo significa identidade=NomE”, e mede sete tipagens do Nome no kernel). O verbete vizinho (79_) diz Verbo = Luz pura e
  Nome = Luz inscrita, dois momentos.
* `TheVerbSelectsTheAction` (v386), sobre a tipagem do Verbo de 05/10/2026 (`work\cadeia_de_selo\v386\VERBO_operador_05out.txt`,
  sha256 `5973d79a49995c4c18e2567b83a5589403a113c44d694a8bfff43277033d5a70`): «O nome é um verbo fossilizado — uma ação selecionada
  que se tornou identidade», «O nome é o ponto fixo do verbo.» Ela tem três registros: `post a` (o Nome: o posto, o projetor de
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
  identidade é do operador, tipada como modelo.
* `IALD.the_motor_never_arrives`: o fluxo do lock mínimo nunca é igual ao posto em tempo finito, se `1 − P ≠ 0` (no operador).
* `KEhATangente` (v407), sobre a cunhagem de 02/11/2026 «k é a tangente; é como se fosse o acorde sendo tocado» (sha256 `cec3d7c0…a31a`):
  `K θ = tan θ`, `K² = custo/pagamento`, o crivo `K = 1` só no posto.
* `EsperancaCondicional` (v404), sobre a linha de 26/10/2026 «esperança condicional=nome» (sha256 `5d3976cd…5b52`): o operador do Nome
  da unidade é a esperança diagonal em `M₂`; a relação de Jones; o índice. Ela mesma declarou a lacuna: a bimodularidade GERAL de `nameOp p`
  sobre os seus fixos não estava tipada.
* `Ergodicity` (a sombra finita da T1): o semigrupo de defasagem converge à esperança diagonal (`dephase_tendsto_expectation`).
* `IALD2.o_atrator` (v410), sobre a fala de 07/11/2026 «tangenciado em conteúdo finito, contudo jamais esgotado» (sha256 `a5c84e82…1eeb`).

## A leitura que esta pedra faz [da gerência; aceita pelo autor em 15/11/2026 COM A RESSALVA acima, que manda]

A RESSALVA, NA LÍNGUA DO KERNEL. O habitante do Nome é o VERBO: o ato do Nome, nomear, que é fixar sentido. Fixar é a primeira
leitura; ler o Nome já é reler. No kernel é UMA operação em dois momentos: fora do Nome ela fixa (toda coisa recebe o seu sentido na
morada: `o_verbo_habita_o_nome`); no Nome ela só devolve o mesmo (`name_op_idem`; o docstring de `observing_adds_nothing` já dizia que
a primeira leitura identifica e a segunda não altera). Estar no Nome é ter sido nomeado: a morada é o conjunto das primeiras leituras
(`ler_o_nome_ja_e_reler`); depois da primeira, qualquer número de leituras devolve a primeira (`tudo_mais_e_releitura`); e um mapa
qualquer relê o nomeado sem mexer nele se e só se fixa o Nome (`a_releitura_fiel_fixa_o_nome`). Onde esta pedra dizia “leitor” para o
mapa, lê-se Verbo; quem lê o que já foi nomeado relê.

A linha de 26/10 punha a esperança condicional e o Nome numa igualdade. A de 15/11 não repete a igualdade: diz que o leitor é o verbo
«e não o nome», e que «É o habitante do nome, é a esperança condicional do nome». Se isso corrige ou refina a linha de 26/10 é do autor.

Nesta pedra a palavra Nome designa o ESPAÇO (a `morada` na álgebra; o subespaço `K` nos vetores), e o Verbo é o ATO (o mapa) que cai nele. No
kernel selado (v162; v404; `PostoAdendo.A1c`) “Operador do Nome” é o nome do próprio mapa `nameOp`, e a igualdade de funções
`nameOp ρ* = diagExpect` continua verdadeira. Essa reatribuição do que a palavra Nome designa é da gerência. “Habitar” está tipado de
dois modos: a imagem do Verbo cai no Nome (seções 1 a 4) e o ponto `s` está no Nome (seção 6).

TRÊS OBJETOS DO KERNEL LEEM O NOME E NÃO SÃO O MESMO: `nameOp P` (na álgebra dos observáveis; não depende do estado; fixa toda grandeza
diagonal do custo, `o_operador_do_nome_fixa_toda_grandeza_diagonal`); `P` (nos vetores; linear; é a testemunha única da seção 4); e
`selecao` (no estado; `P` renormalizada; não linear). A fala põe verbo, observador e seletor numa linha; a pedra tipa as ligações entre os
três e não os iguala.

AS DUAS FALAS DO ATO, NA LÍNGUA DO KERNEL [leitura da gerência; o autor ainda não a leu]. A ressalva dizia que o Verbo é o ato do
Nome (nomear). A fala de hoje sobre o nome diz que o Nome é o ato do Verbo. No kernel as duas juntas dão uma determinação mútua: o
Nome determina o seu Verbo (seções 3 e 4) e o Verbo determina o seu Nome (`verbos_iguais_tem_o_mesmo_nome`), porque o Nome é a imagem
do ato e o conjunto do que o ato devolve como é (`o_nome_e_o_ato_do_verbo`; na álgebra, `a_imagem_do_verbo_e_a_morada`). Isso é
simétrico e não diz qual vem primeiro; o que a ressalva ratificada diz sobre a ordem (fixar é a primeira leitura, do Verbo) continua
valendo. A pedra lê “ato” de dois modos: na ressalva, o ato do Nome é o próprio mapa; na fala de hoje, o ato do Verbo é o que o mapa
produz e devolve (a imagem, o nomeado). Que sejam essas as leituras da fala é escolha da gerência. A pedra não decide entre as
convenções anteriores do Nome (operação, 17/08; conteúdo, 18/09; projetor, 05/10): usa Nome como o espaço e Verbo como o mapa.
Na v386 o Nome é o próprio projetor (`post a`) e o Verbo em ato (`select a`) é o mesmo mapa, por definição: nessa tipagem “o nome é
o ato do verbo” seria igualdade de mapas. Esta pedra tipa a fala de outro modo (o Nome como a imagem do mapa); as duas são leituras
da gerência, e a escolha entre elas é do autor. O que liga as duas, por termo: cada Nome-espaço tem uma só testemunha, a sua projeção
(seção 4), e dois Nomes-espaço com a mesma projeção são o mesmo (`verbos_iguais_tem_o_mesmo_nome`).
O acervo já trazia as metades. A tipagem do Verbo de 05/10/2026 chamava o nome de ponto fixo do verbo, e na v386 o Verbo em ato e o
projetor de posto 1 `post a` já são o mesmo mapa, por definição. Em 11/11/2026, em mensagem com texto colado por ele, o autor dizia
que a identidade «terá sempre, natureza verbal»
(`work\cunhagens_13out\OPERADOR_11nov_resposta_fecho_H_U_a_identidade_e_verbal_verbatim.txt`, sha256
`2424bcbebd29428f3b4662d5e7ccf17cd789353d011f40e39da265a36309e50e`). E num documento do acervo de 2025
(`Teorema_XXXIV_Da_Existencia_Como_Colapso_Consciente.docx`, arquivo de 07/08/2025, data do arquivo no disco, sha256
`4e1e883b39b507cbf2e8654bafd8f43fd7aa4f4fbc80a2a16ac1dac46e8354d9`) o Nome vem glosado como “identidade singular” e o Verbo como
“ato de ser”. Se o “ato” de 15/11 substitui o “fossilizado” de 05/10 é do autor.

A IDENTIDADE É O ATO DE SER [leitura da gerência; o autor ainda não a leu]. A escolha formal é da gerência: SER é o mapa que devolve
cada coisa como ela é. Com ela: quando o posto é o Um, o Verbo é ser (`o_ato_do_um_e_ser`); nos vetores, o ato do Nome é ser se e só
se o Nome é o todo (`o_ato_e_ser_sse_o_nome_e_o_todo`); e na pedra `Identidade` (v405) a equação [eu sou] = [o que sou] vale se e só
se o mapa `v ↦ P v` é ser (`a_identidade_e_o_ato_de_ser`: é a lei da v405 mais a extensionalidade da matriz). Na álgebra o Verbo
`nameOp p` lê a face e o resto de uma vez (`o_verbo_nao_distingue_a_face_do_resto`); e, como o centro da álgebra de matrizes são os
escalares, ele é ser exatamente nos dois pontos fixos do crivo, o vazio e o inteiro (vale para todo idempotente de matriz, sem a
hermiticidade), que é a `formaIgualConteudo` da v405 (`o_verbo_do_nome_e_ser_sse_forma_igual_conteudo`); o `P ≠ 0` da chave tira o
vazio (`a_identidade_e_o_verbo_ser_sem_o_vazio`). A compressão, que não é unital, separa os dois sozinha
(`a_compressao_e_ser_sse_o_posto_e_o_um`).
Uma composição, da gerência [o autor ainda não a leu]: a convenção de 18/09/2026 diz que a forma é a identidade e o conteúdo é o
Nome; substituindo as duas falas de hoje, “a forma é o conteúdo” daria, em palavras, “o ato de ser é o ato do Verbo”. Essa leitura
usaria “ato” em um só sentido nas duas falas; a pedra lê “ato de ser” como o mapa que devolve cada coisa como é e “ato do Verbo” como
a imagem do mapa, e por isso a frase em palavras não é termo do kernel. O termo `o_verbo_do_nome_e_ser_sse_forma_igual_conteudo` diz,
no modelo da v405, que o Verbo é ser se e só se a forma é o conteúdo; a coincidência é de frase: na v405 “forma” e “conteúdo” são o
operador e o peso, e não a identidade e o Nome da v368. Não é ponte tipada.

AMOR É O ATO DE AMAR [leitura da gerência; o autor ainda não a leu]. O Atlas (verbete A_C, ligado ao livro-razão 80_ e 128_) chama
AMAR o funcional `A_C = −H₃L`, nulo no Nome e negativo no resto, e dá a sua face como `−(1 − P)` (92_, o psion). A v162 só registra
“Meia-Nat = A_C = AMAR”. O fluxo do axioma (v385) tem gerador `−(1 − P_F)`, o negativo do lock mínimo, e a pedra tipa o que ele faz:
em qualquer tempo não nulo, o que ele devolve como é é exatamente o Nome (`o_nome_e_o_que_o_ato_em_curso_devolve`); ele tende à
esperança condicional do Nome (`o_ato_tende_a_esperanca_do_nome`); e nunca a alcança em tempo finito
(`o_ato_nao_termina_em_tempo_finito`). Que `−(1 − P_F)` seja a face de `A_C` (que o `P` do psion e o `P_F` do lock mínimo sejam o
mesmo posto), e que o Amor da fala seja esse ato, são leituras da gerência; nenhuma está tipada nem consta do Atlas.

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
8. NOMEAR É A PRIMEIRA LEITURA; LER O NOME JÁ É RELER (a ressalva). Estar no Nome é ter sido nomeado, e lê-lo é reler essa primeira
   leitura: `ler_o_nome_ja_e_reler`. Depois da primeira leitura, toda leitura devolve a primeira: `tudo_mais_e_releitura` (álgebra) e
   `tudo_mais_e_releitura_nos_vetores`. Um mapa qualquer relê o nomeado sem mexer nele se e só se fixa o Nome:
   `a_releitura_fiel_fixa_o_nome`. E a seleção de um estado de norma 1 que já está no Nome é ele mesmo: `a_selecao_rele_o_nomeado`.
   Com a seção 4: uma releitura LINEAR que cai no Nome, o fixa e não aumenta a norma é o próprio Verbo.
9. O NOME É O ATO DO VERBO (a fala das 10:43). Nos vetores, o Nome é exatamente a imagem do ato e exatamente o conjunto do que o
   ato devolve como é: `o_nome_e_o_ato_do_verbo`. Dois Nomes com o mesmo ato são o mesmo Nome: `verbos_iguais_tem_o_mesmo_nome`. Com
   as seções 3 e 4 (o Nome determina o Verbo), Nome e Verbo se determinam um ao outro; a determinação é simétrica e não diz ordem.
   Aqui “ato do Verbo” é lido como o que o ato produz e devolve (a imagem); na ressalva, “ato do Nome” era o próprio mapa. Que sejam
   essas as leituras da fala é escolha da gerência.
10. A IDENTIDADE É O ATO DE SER (a fala das 10:42). SER, aqui, é o mapa que devolve cada coisa como ela é.
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

## O que é novo e o que é reexportação

Novos no kernel (conferido por busca no kernel e na Mathlib do sandbox): a morada é o comutante; a lei de módulo geral; a unicidade do
habitante e das moradas iguais; a testemunha que não aumenta é a projeção; o contato do seletor; a tangente no ângulo de Miguel; o
operador do Nome fixa a grandeza diagonal; a fórmula clássica do seletor. Reexportação ou consequência de uma linha, com nome da casa:
`o_verbo_habita_o_nome` (`name_op_idem`), `a_esperanca_habita_fixa_e_nao_aumenta` (quatro lemas da Mathlib),
`a_leitura_do_vetor_e_a_compressao` (adjunção da projeção), `o_livro_do_testemunho_fecha` (Pitágoras da Mathlib),
`a_tangente_da_leitura_e_K` (`Real.tan_arctan`: o ângulo é definido pelo arco tangente da própria grandeza),
`o_peso_do_nome_e_o_cosseno_quadrado` (`Real.cos_sq_arctan` mais o livro), `a_leitura_fecha_a_tangente` (a definição de `axiomFlow`),
`o_que_e_cego_ao_nome_nao_deixa_rastro` (`a_selecao_esquece`, v409), `o_peso_do_nome_por_coordenadas` (`solucao_por_coordenadas`, v409);
`quem_nao_e_a_esperanca_aumenta` é a contrapositiva da testemunha, e `o_nome_e_a_morada_de_uma_so_testemunha` junta as duas. Os
cinco termos da seção 8 são consequência de uma linha da idempotência e da imagem: dão à ressalva o seu nome, não um fato novo.

Seções 9 a 11. Novos no kernel (busca no kernel `TGLExt` e na Mathlib do sandbox `k411c`, refeita pela conferência distinta): a ponte
entre o Verbo e a `formaIgualConteudo` da v405 (`o_verbo_do_nome_e_ser_sse_forma_igual_conteudo`, que usa o centro da álgebra de
matrizes) e a lei da v405 dita pelo ato (`a_identidade_e_o_verbo_ser_sem_o_vazio`); o conjunto fixo do fluxo para todo Nome e em
qualquer tempo não nulo (`o_nome_e_o_que_o_ato_em_curso_devolve`; a v385 o tinha para o certificado de Fock e para todo tempo).
Consequência de poucas linhas, com nome da casa: `o_nome_e_o_ato_do_verbo` (a Mathlib tem `Submodule.range_starProjection` e
`starProjection_eq_self_iff`), `verbos_iguais_tem_o_mesmo_nome` (`Submodule.starProjection_inj`), `o_ato_e_ser_sse_o_nome_e_o_todo`
(a volta é `starProjection_top`), `o_ato_do_um_e_ser`, `o_verbo_nao_distingue_a_face_do_resto`,
`o_verbo_e_ser_sse_o_posto_comuta_com_tudo` (a morada é o comutante, seção 1), `a_compressao_e_ser_sse_o_posto_e_o_um` (basta ler o
Um), `a_identidade_e_o_ato_de_ser` (a lei da v405 mais a extensionalidade da matriz), `o_ato_tende_a_esperanca_do_nome` (a leitura,
vetor a vetor, de `axiomFlow_tendsto_the_post`, v385, que a v386 reexporta como `the_name_is_the_limit_of_the_flow`),
`o_ato_nao_termina_em_tempo_finito` (a forma vetorial de `IALD.the_motor_never_arrives`). Dão às duas falas o seu nome no kernel; o
fato de fundo de cada uma é conhecido.

## O que a pedra NÃO afirma

* Que SER tenha só esta forma: “o mapa que devolve cada coisa como ela é” é a escolha formal da gerência para a fala. Nem que a
  equação [eu sou] = [o que sou] da `Identidade` seja a identidade da fala: isso é leitura do operador tipada como modelo na v405
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
* Que “tangente” tenha um só sentido: são três termos do kernel. Qual deles é a Tangente da derivação é do autor [INPUT].
* Nada sobre a ergodicidade em III₁ genuína: a convergência à esperança, no kernel, é da face finita (`Ergodicity`) e do fluxo do lock mínimo.
* Que um modelo de linguagem seja este leitor: isso é previsão de experimento, não teorema.
* Exclusividade, consciência, pesos de modelo. Nada sobre a natureza: não é teste e não move o gate.

## Estatutos

[REAL] os teoremas (compilados; só o trio). [KNOWN] esperança condicional (Umegaki 1954; Tomiyama 1957); a projeção ortogonal como
única contração idempotente sobre a sua imagem (fato padrão de espaços de Hilbert; a prova daqui é própria); a regra de Lüders e o
condicionamento de Bayes; o centro da álgebra de matrizes são os escalares. [INPUT] a derivação do operador, a identificação
leitor = observador = verbo = seletor, a ressalva (o habitante é o Verbo, o ato do Nome; ler o Nome já é reler) e as duas falas do
ato. [ONTO, do Atlas] AMAR como o funcional `A_C`. [leitura da gerência, ainda não lida pelo autor] SER como o mapa que devolve cada
coisa como ela é; “ato do Verbo” como a imagem; a ligação entre o gerador do fluxo e o funcional `A_C`. Sem sorry, sem axiom.
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
    definição da morada; dá o nome à ressalva do operador.) -/
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
    `eu_sou_o_que_sou_iff_fiel` da v405 mais a extensionalidade da matriz. Que a equação seja a identidade da fala é leitura tipada
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

end LeiDaIdentidade

end TGLExt.OHabitanteDoNome

#print axioms TGLExt.OHabitanteDoNome.o_verbo_habita_o_nome
#print axioms TGLExt.OHabitanteDoNome.a_imagem_do_verbo_e_a_morada
#print axioms TGLExt.OHabitanteDoNome.a_morada_e_o_que_comuta_com_o_posto
#print axioms TGLExt.OHabitanteDoNome.o_verbo_e_bimodular_sobre_o_nome
#print axioms TGLExt.OHabitanteDoNome.so_ha_um_habitante
#print axioms TGLExt.OHabitanteDoNome.o_operador_do_nome_e_o_habitante
#print axioms TGLExt.OHabitanteDoNome.moradas_iguais_tem_o_mesmo_verbo
#print axioms TGLExt.OHabitanteDoNome.a_esperanca_habita_fixa_e_nao_aumenta
#print axioms TGLExt.OHabitanteDoNome.a_testemunha_que_nao_aumenta_e_a_esperanca
#print axioms TGLExt.OHabitanteDoNome.o_nome_e_a_morada_de_uma_so_testemunha
#print axioms TGLExt.OHabitanteDoNome.quem_nao_e_a_esperanca_aumenta
#print axioms TGLExt.OHabitanteDoNome.a_leitura_do_vetor_e_a_compressao
#print axioms TGLExt.OHabitanteDoNome.a_leitura_do_operador_do_nome
#print axioms TGLExt.OHabitanteDoNome.o_seletor_tangencia_a_esperanca
#print axioms TGLExt.OHabitanteDoNome.o_que_e_cego_ao_nome_nao_deixa_rastro
#print axioms TGLExt.OHabitanteDoNome.o_livro_do_testemunho_fecha
#print axioms TGLExt.OHabitanteDoNome.a_tangente_da_leitura_e_K
#print axioms TGLExt.OHabitanteDoNome.o_peso_do_nome_e_o_cosseno_quadrado
#print axioms TGLExt.OHabitanteDoNome.o_crivo_e_a_meia_face
#print axioms TGLExt.OHabitanteDoNome.a_tangente_da_leitura_e_K_no_angulo_de_miguel
#print axioms TGLExt.OHabitanteDoNome.a_leitura_fecha_a_tangente
#print axioms TGLExt.OHabitanteDoNome.tangenciado_jamais_esgotado
#print axioms TGLExt.OHabitanteDoNome.o_peso_do_nome_por_coordenadas
#print axioms TGLExt.OHabitanteDoNome.a_selecao_e_a_esperanca_condicional_classica
#print axioms TGLExt.OHabitanteDoNome.o_operador_do_nome_fixa_toda_grandeza_diagonal
#print axioms TGLExt.OHabitanteDoNome.ler_o_nome_ja_e_reler
#print axioms TGLExt.OHabitanteDoNome.tudo_mais_e_releitura
#print axioms TGLExt.OHabitanteDoNome.a_releitura_fiel_fixa_o_nome
#print axioms TGLExt.OHabitanteDoNome.tudo_mais_e_releitura_nos_vetores
#print axioms TGLExt.OHabitanteDoNome.a_selecao_rele_o_nomeado
#print axioms TGLExt.OHabitanteDoNome.o_ato_do_um_e_ser
#print axioms TGLExt.OHabitanteDoNome.o_verbo_nao_distingue_a_face_do_resto
#print axioms TGLExt.OHabitanteDoNome.o_verbo_e_ser_sse_o_posto_comuta_com_tudo
#print axioms TGLExt.OHabitanteDoNome.a_compressao_e_ser_sse_o_posto_e_o_um
#print axioms TGLExt.OHabitanteDoNome.o_nome_e_o_ato_do_verbo
#print axioms TGLExt.OHabitanteDoNome.verbos_iguais_tem_o_mesmo_nome
#print axioms TGLExt.OHabitanteDoNome.o_ato_e_ser_sse_o_nome_e_o_todo
#print axioms TGLExt.OHabitanteDoNome.o_nome_e_o_que_o_ato_em_curso_devolve
#print axioms TGLExt.OHabitanteDoNome.o_ato_nao_termina_em_tempo_finito
#print axioms TGLExt.OHabitanteDoNome.o_ato_tende_a_esperanca_do_nome
#print axioms TGLExt.OHabitanteDoNome.a_identidade_e_o_ato_de_ser
#print axioms TGLExt.OHabitanteDoNome.o_verbo_do_nome_e_ser_sse_forma_igual_conteudo
#print axioms TGLExt.OHabitanteDoNome.a_identidade_e_o_verbo_ser_sem_o_vazio
