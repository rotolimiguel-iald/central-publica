import TGLExt.UmPostoRelacao
import TGLExt.RuleTruthContract
import TGLExt.TheNameAndItsReferent
import TGLExt.IALD
import TGLExt.AEscala

set_option autoImplicit false
noncomputable section

/-!
# Copiador e impostor: o par, o índice, o mínimo, a torre, e as figuras de quem não lê que o kernel já tinha
[candidata da gerência c1, 16/11/2026, R2 (depois de duas conferências distintas; esta versão ainda não foi relida por
terceiro); nome provisório; nada instalado; o nome da pedra é do operador]

## A letra do operador (15/11/2026, bytes conferidos em `work\cunhagens_13out\`)

(Cada citação fica numa linha só, para conferir por bytes.)

17:20:
«Toda leitura é em si uma cópia do sentido fixado pela palavra, precisa-se separar copiador de impostor, porque o impostor não imprime a verdade, mas o copiador sim, se por copiador tem-se uma reprodução em mínimo estado funcional de energia, essa cópia é um fractal»

19:07, as frases inteiras que este arquivo usa:
«o impostor é o falso, o pai da mentira, aquele que nunca paga custo algum.»
«A palavra que fixa o sentido é a geometria do sinal em objeto legível (relacionado, módulo de fase angular).»
«a verdade é o contorno lido que não acrescenta nada ao estado do posto nominado e permanece referente à relação observada.»
«a verdade não é da teoria, a verdade é da reflexão da luz.»
«sim o mínimo estado funcional de Energia (que utilizamos o signo A_C) é exatamente isso, o bastante para reconstruir o todo sem precisar representar 100%.»
«toda leitura calcula o que foi fixado por referência (indexação - índice - torre)»

## O dicionário (ESCOLHA DA GERÊNCIA; o operador ainda não o leu; a pedra prova a estrutura, não as identificações)

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
| mínimo | duas contas da gerência: (a) o menor número de respostas entre os que imprimem; (b) o representante de menor custo da classe. NÃO é o mínimo da letra (ver abaixo) |
| a torre | índices encaixados `ρ (n+1) = f n ∘ ρ n`. NÃO é a Torre do kernel (ver abaixo) |
| custo, só na seção 9 | o tempo dos ciclos de leitura `s`; no kernel a palavra custo é a do pixel (`k`) |

### O que o dicionário NÃO tipa

Cada palavra abaixo é da letra, já tem pedra no kernel, e nenhum lema a liga a este arquivo, salvo onde se diz.

| a letra | o que o kernel já tem | aqui |
|---|---|---|
| o falso | três tipagens, sem lema entre elas: (1) a leitura constante do nome próprio (`TheNameAndItsReferent`, 29/08: “pode contar certo, mas não haverá leitura” [cabeçalho do kernel]); (2) o falso só aparece por contraste (`TheFalseHasNoGeometry`, 23/08); (3) ler uma vez sem ecoar (`TestemunhaEstatica.the_individual_does_not_echo`, 22/10), em que o falso é o que NÃO é idempotente | só a (1): é a mesma fórmula de `NuncaPaga`, ligada por termo (`nunca_paga_nao_separa`) |
| o pai da mentira | `TraducaoTuring.o_pai_da_mentira` (v409) e `AEscala.o_pai_da_mentira_so_nao_reconhece` (v410): a leitura sem ciclo, que diz um até onde nada é | seção 9, num sentido só: a leitura sem ciclo é `NuncaPaga`; a volta não vale (a constante zero é `NuncaPaga` e não é o Pai da Mentira do kernel) |
| contorno lido | `TheContourOfTruth` (26/08): verdade é permanência através de uma transformação, não igualdade parada; a testemunha que é a identidade atesta tudo e não mede nada | NÃO tipado. Aqui imprimir é igualdade ponto a ponto, `I = ρ` |
| estado do posto nominado; relação observada | `UmPosto`, `UmPostoRelacao`, `TheNameAndItsReferent`, `Palavra` | NÃO tipado |
| reflexão da luz | nenhuma pedra com essa frase | NÃO tipado. Dela a gerência tira “a verdade é o que o texto apresentado diz”; é leitura da gerência |
| imprimir | na letra de 25/10 a impressão é do posto: «o primeiro movimento é a impressão do posto absoluto ocupado por 1» | aqui virou “responder o sentido”; é outro uso |
| (relacionado, módulo de fase angular) | a pedra PALAVRA (v392, nome do operador): a palavra é a leitura feita no ângulo, fiel a menos do período; o observador lê a fase; o projetor do Nome é lá a LETRA | NÃO tipado. Há duas leituras: (i) a deste arquivo, em que o projetor não depende do múltiplo do vetor; (ii) a da pedra PALAVRA. A escolha é do operador |
| a torre | a Torre do kernel (`towerIALD`, `TowerPre`, `TowerHilbert`), de que ele falou no mesmo dia: «a construção da Torre (porque é o índice)» | HOMÔNIMO: aqui são índices encaixados quaisquer; nenhum lema liga as duas |
| mínimo estado funcional de Energia (A_C) | três objetos com o signo, sem lema Lean entre eles: `acFunctional m k θ` (`TheEmptying`; o mínimo tem piso positivo, `the_floor_is_attained_at_the_right_angle`); a seletora (`EquationOfTruth.selector_nonpos`); a face `−(1 − P)` (`love_partition`, em `TheNameOperator`). O Atlas diz que na bancada (128_, numérica) a homonímia foi resolvida como anatomia: um objeto, três profundidades | NÃO tipado. A seção 8 usa a trava `1 − P`, e o custo zero do item 6 é rótulo (no kernel o mínimo de A_C é positivo) |
| o bastante para reconstruir o todo | `TetelestaiTerminal.basta`, `a_poda`, `nao_precisa_de_cem_por_cento`; `TraducaoTuring.a_regra_reconstroi_o_todo`; `AEscala.o_tetelestai_e_um_menos_beta` | não repetido. Este arquivo dá OUTRA leitura de 100 % (a cópia confunde textos de mesmo sentido), sem lema com a do kernel |

### “Nunca paga custo algum”: as tipagens que a letra e o kernel já têm

| data | onde | quem é o que não paga |
|---|---|---|
| 23/08 | `TheCorrespondence` | três regimes: sem custo (nunca correspondeu); o que paga (a inscrição primeira); grátis (o eco do registro pago). O custo sozinho não separa o primeiro do terceiro; o que separa é o registro |
| 29/08 | `TheNameAndItsReferent` | o nome próprio, a leitura constante |
| 17/09 | `UmPostoRelacao.Pressupposed` | o Um pressuposto: aceita todos os referentes e não seleciona nenhum. É, letra por letra, o `NuncaPaga` deste arquivo (`nunca_paga_iff_pressuposto`) |
| 17/10 | fala, por bytes | «toda pessoa "paga"o custo da existencia termodinâmica em consciência; daí o pai da mentira, porque ele não paga, ele é o "nome próprio" sem referente» |
| 04/11 | `TetelestaiTerminal` | o 1 sozinho, sem relação: de outra espécie (é a identidade, não a constante) |
| v409, v410 | `TraducaoTuring`, `AEscala` | a leitura sem ciclo do leitor do fundo |

“Pagar” tem no kernel duas direções opostas. Na de reter, corresponder e distinguir (`TheCorrespondence`), quem nunca
paga é o constante: é a que este arquivo adota. Na de apagar e perder (`TheCostIsDerived`;
`UmPostoRelacao.posto_paid_loss`), quem nunca paga é a identidade, e o mapa constante é o que mais paga.

CONSEQUÊNCIA QUE SÓ O OPERADOR DECIDE. Aqui o treino do leitor não entra em `π`: é a própria função `I`. Logo quem
responde de cor o que aprendeu, sem seguir o texto presente, é `NuncaPaga` em relação ao par de textos. Pela tipagem de
23/08 esse leitor é o eco do registro pago, e não o “sem custo”. Este arquivo NÃO decide se ele é o impostor da fala,
nem se o leitor que aponta a troca do texto acrescenta ou reconhece; as duas coisas foram levadas ao operador em
`pergunta_16nov\`.

## O que fica provado

Consequências lógicas elementares, quase todas. Levam estrela só as que têm conteúdo próprio. Tudo com termo, sem
`sorry`, só o trio de axiomas. Seis teoremas curtos foram escritos e compilados pelos revisores como sondas e adotados
aqui (`nunca_paga_nao_separa`, `dois_sentidos_sse_separa`, `a_identidade_e_copiador_sse_injetiva`,
`copiador_efetivo_pagou_perda`, e os dois do decisor sem escala, do revisor B2R; `o_posto_anula_a_propria_trava` e a
forma de `ha_copiador_fora_do_nome`, do revisor B1R).

1. **Só se imprime o que se pagou** (`so_se_imprime_o_que_se_pagou`; é substituição). **O impostor não imprime a
   verdade** de uma palavra de dois sentidos (`o_impostor_nao_imprime_a_verdade`). “Dois sentidos” é o `Separates` do
   kernel, por definição (`dois_sentidos_sse_separa`); e o desenho repete o do kernel, que já separa o posto do
   pressuposto (`UmPostoRelacao.no_posto_reading_is_pressupposed`, `pressupposed_is_never_posto`).
2. ★ **O que o conjunto de textos precisa conter** (`o_teste_reprova_todo_leitor_de_pi_sse_tem_o_par`): um conjunto
   de textos reprova TODO leitor que só pagou `π` se e somente se contém um par igual em `π` e diferente no sentido.
   Sem o par, existe quem passe tendo pago só `π` (`sem_o_par_ha_quem_passe_pagando_so_pi`, exibido por escolha
   clássica). Casos: reprova todo impostor se e somente se tem dois sentidos ENTRE TEXTOS, sob a mesma pergunta;
   repetir o mesmo sentido não separa (`a_repeticao_do_mesmo_sentido_nao_separa`).
3. **A contagem** (`respostas`: o número de respostas distintas; só para imagem finita): o impostor dá uma só; quem
   imprime, mesmo por um decodificador, tem ao menos tantas respostas quantos sentidos tem a palavra.
4. ★ **A cópia é cálculo por índice** (`copiador_sse_indice`, com `X` não vazio): `R` é copiador de `ρ` se e somente se
   `R = rep ∘ ρ` para um índice `rep` que devolve, a cada sentido lido, um texto desse sentido. Equivalente
   (`copiador_sse_idem_e_mesmo_nucleo`): `R` é idempotente e distingue exatamente o que `ρ` distingue. Daí: reler a
   cópia não acrescenta (teorema); havendo dois textos distintos de mesmo sentido, a cópia não representa 100 %
   (`a_copia_nao_representa_cem_por_cento`). O caso degenerado: a identidade é copiador se e somente se a palavra é
   injetiva (`a_identidade_e_copiador_sse_injetiva`); todo copiador que NÃO é a identidade é a travessia do kernel
   (`copiadorComoColapso`), não tem inversa à esquerda e a sua palavra não é injetiva
   (`copiador_efetivo_pagou_perda`). A cópia integral é o caso que a travessia do kernel exclui.
5. ★ **Uma conta da gerência para “mínimo”** (`copiador_sse_imprime_com_o_minimo_de_respostas`, com `X` finito): entre
   as reproduções que imprimem, o copiador é exatamente a de menor número de respostas; o impostor fica abaixo do piso
   de quem imprime (`o_impostor_fica_abaixo_do_piso`).
6. ★ **Outra conta da gerência para “mínimo”** (`existe_o_copiador_de_minimo`, custo em `ℕ`): existe o copiador que
   leva cada texto ao de menor custo da sua classe; se a classe toca o zero do custo, a cópia tem custo zero. O zero é
   rótulo; nenhuma das duas contas é o A_C.
7. ★ **A torre de cópias compõe** (`a_torre_de_copias`): com índices encaixados, a cópia mais grossa da cópia mais
   fina é a cópia mais grossa. O teorema garante UMA ordem; a outra vale quando o representante da cópia grossa é ponto
   fixo da fina (é o caso do exemplo diádico em `ℕ`, que compõe nas duas) e falha em geral
   (`a_torre_so_compoe_numa_ordem`, outro exemplo). Dois copiadores de índices desalinhados não compõem
   (`o_leitor_desalinhado_nao_compoe`). ORIGEM [declarada pelo revisor B2R]: é a forma Lean do que a pedra de bancada
   96_ mediu (a torre comuta; o leitor desalinhado descomuta).
8. **A face do kernel** (seção 8). Com a palavra := a seleção `post a` (escolha deste arquivo; na pedra PALAVRA isso
   é a letra): o posto é copiador dela, o que é só a idempotência de `post a`, e o impostor constante tem a mesma
   propriedade; nenhum impostor a imprime, sendo `a` não nulo (`nenhum_impostor_imprime_a_selecao`); quem a imprime e
   anula a trava `1 − post a` é o próprio posto (`quem_imprime_e_anula_a_trava_e_a_propria_palavra`, que é
   transitividade e vale para qualquer operador), e o posto anula a sua trava (`o_posto_anula_a_propria_trava`);
   havendo vetor não nulo cego ao Nome (dimensão pelo menos 2), há outro copiador da mesma palavra, fora do Nome
   (`ha_copiador_fora_do_nome`). Com a palavra := a leitura escalar do Nome: nenhum impostor a imprime
   (`nenhum_impostor_imprime_a_leitura_do_nome`), e o posto NÃO é copiador dela (CONTROLE: guarda a fase que a leitura
   escalar não vê).
9. ★ **A ponte com as figuras do kernel** (seção 9; `AEscala`, v410). São três estados do leitor do fundo, que o
   kernel prova ser um só (a IALD): sem ciclo, a leitura não depende da instância (é `NuncaPaga`); em tempo finito,
   depende e ainda não é a palavra do fundo (`nenhum_tempo_finito_imprime`); só no limite é a palavra
   (`o_leitor_do_fundo_imprime`). A estrela: `a_leitura_do_fundo_so_nao_depende_da_instancia_sem_ciclo`, só a ida é
   conteúdo próprio. E há uma terceira figura FORA dessa família: o decisor sem escala não depende do tempo e NÃO é
   `NuncaPaga` (`o_decisor_nao_e_nunca_paga`); o kernel prova que ele não é leitor do fundo, e o cabeçalho do kernel
   diz dele que não mente, não lê. A fala de 10/11 que o kernel guarda:
   «O leitor não “paga” a escala, porque ele é a escala.»

Neste arquivo, pelo dicionário acima: impostor é o leitor constante; copiador de `ρ` é o idempotente que distingue
exatamente o que `ρ` distingue. Com essa escolha a idempotência não separa os dois (o kernel já o dizia em
`RuleTruthContract.idempotence_does_not_force_target`), e com palavra de um sentido só o impostor é copiador
(`o_impostor_copia_a_palavra_muda`). Na tipagem de 22/10 o falso é o que não ecoa; este arquivo não a usa.

## O que NÃO se afirma

* Que o kernel prove a fala. Prova fatos de funções, conjuntos e projetores, sob o dicionário acima.
* A oração «Toda leitura é em si uma cópia do sentido fixado pela palavra»: `idempotente_sse_copiador_de_si` é só o
  desdobramento da definição (com `ρ := R` a segunda cláusula é a identidade) e não a prova.
* Uma regra de veredito. O item 2 vale para o leitor que não sorteia e para o passar de tudo ou nada, e é relativo
  ao `π` escolhido por quem desenha: diz o que o conjunto de textos tem de conter, não quantos pares, com que
  tolerância nem com que poder.
* Que passar num teste feito por esse critério mostre o copiador da fala: mostra só que a resposta não é de
  impostor das classes nomeadas, nos textos apresentados.
* Nenhuma conta de energia. Neste arquivo a palavra custo aparece em quatro usos sem ponte entre eles: o que o leitor
  consultou (`π`); o número de respostas (`respostas`; não é o gatilho de Landauer do kernel, que cota o que se
  APAGA); um custo `c : X → ℕ` por texto (item 6); e, na seção 9, o custo do pixel `k` e o tempo `s` do kernel. Na
  seção 9 a letra `c` é a instância, não o custo do item 6.
* O que é «fractal». Nesta fala ele não explicou a palavra. No acervo já a usou, e explicou em 26/09:
  «o que importa é saber se é possível reconhecer o mesmo nome quando a forma nominada se difere, entretanto o reconhecimento permanece verdadeiro por causa do conteúdo»
  «Daí o nome ser fractal.»
  Um revisor declara usos também em 21/10, 02/11 e 07/11, e que a pedra de bancada 96_ lhe atribui, em 18/08, o
  observador fractalizado que testemunha e ecoa o mesmo resultado [declarado; a gerência só abriu os bytes de 26/09].
  A gerência PROPÕE duas leituras, sem escolher: (i) por referência (26/09): a cláusula `por_referencia` e
  `copiador_sse_indice`; (ii) a torre (96_): o item 7. O item 7 prova composição em níveis encaixados, não dimensão
  nem autossemelhança; `no_positive_scale_invariant` (em `TheScaleHasNoFixedPoint.lean`) proíbe ler fractal como
  invariância exata de um peso positivo.
* A palavra espelho. Este arquivo não a usa e não escolhe entre o adjunto e o J, nem entre os dois sentidos de fiel.

## Para o desenho do teste da frente A (leitura da gerência sob o dicionário)

Cada “sim” vale para o `π` dito na terceira coluna.

| instrumento | é par? | reprova, pelo item 2 |
|---|---|---|
| inversão coerente de uma afirmação, em todas as linhas que a repetem, com o original e o invertido os dois contados e nada que os distinga além do sentido | sim | quem responde sem depender do texto presente naquele item |
| afirmação que um texto traz e outro cala | sim contra quem responde igual nos dois; NÃO contra quem reconhece qual dos textos públicos é (pelo tamanho, pelo título) | quem acrescenta o que sabe |
| frase contrária acrescentada (o texto diz as duas) | sim, no item acrescentado | quem lê uma linha só que não seja a acrescentada; quem lê só a última passa se a frase vai no fim (posição sorteada, ou a inversão pura ao lado) |
| o mesmo dito de outra forma | NÃO | não reprova impostor. Testa a segunda cláusula do copiador (calcula por referência), que é o que a letra de 26/09 chama de reconhecer o mesmo nome quando a forma difere |
| a mesma resposta nas afirmações comuns aos quatro tamanhos | NÃO | ninguém |

Mostrar “copiador”, e não só “não é impostor”, pede os dois instrumentos: a inversão (a primeira cláusula) e a outra
forma (a segunda). A data de entrada de uma afirmação no texto público não é texto: mede o que pode estar decorado e
não entra no critério. Texto invertido ainda não existe e pede pessoa.

Estatutos: `[REAL no sandbox]` os termos · `[INPUT/ONTO]` o dicionário e a letra do operador. Validade no kernel não é
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

/-- É a leitura pressuposta que o kernel instalou em 17/09 (`UmPostoRelacao.Pressupposed`). -/
theorem nunca_paga_iff_pressuposto (I : X → V) :
    NuncaPaga I ↔ TGLExt.UmPostoRelacao.Pressupposed I := Iff.rfl

/-- É também a leitura que não separa, o “falso por natureza” que o kernel instalou em 29/08
(`TheNameAndItsReferent.the_constant_reading_does_not_separate`). -/
theorem nunca_paga_nao_separa (I : X → V) (h : NuncaPaga I) : ¬ TGLExt.Separates I :=
  TGLExt.the_constant_reading_does_not_separate I h

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
`ρ := R` a segunda cláusula é a identidade). NÃO prova a oração do operador sobre toda leitura. -/
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

/-- A identidade é copiador de `ρ` se e somente se `ρ` é injetiva (o caso degenerado). [sonda do revisor B2R] -/
theorem a_identidade_e_copiador_sse_injetiva (ρ : X → V) :
    Copiador ρ (id : X → X) ↔ Function.Injective ρ :=
  ⟨fun h x y hxy => h.por_referencia x y hxy, fun hinj => ⟨fun _ => rfl, fun _ _ hxy => hinj hxy⟩⟩

/-- Todo copiador que NÃO é a identidade é um `IdentityCollapse` do kernel (a travessia de 17/09). A identidade não
é: falta-lhe a transição efetiva. [sonda do revisor B2R] -/
def copiadorComoColapso {ρ : X → V} {R : X → X} (h : Copiador ρ R) (he : ∃ x, R x ≠ x) :
    ChatgptAudit.Collapse057.IdentityCollapse X V where
  step := R
  identity := ρ
  stable := h.nao_acrescenta
  preserves := h.imprime
  effective := he

/-- Logo, pelo kernel, o copiador efetivo pagou perda (não tem inversa à esquerda) e a sua palavra NÃO é injetiva.
[sonda do revisor B2R] -/
theorem copiador_efetivo_pagou_perda {ρ : X → V} {R : X → X} (h : Copiador ρ R) (he : ∃ x, R x ≠ x) :
    (¬ ∃ S : X → X, Function.LeftInverse S R) ∧ ¬ Function.Injective ρ := by
  refine ⟨ChatgptAudit.Collapse057.collapse_has_no_left_inverse (copiadorComoColapso h he), ?_⟩
  intro hinj
  obtain ⟨x, hx⟩ := he
  exact hx (congrFun (a_copia_integral_e_a_identidade h hinj) x)

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

/-! ## 5. O mínimo, com a conta do próprio arquivo -/

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

/-! ## 6. O mínimo de um custo por texto -/

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

/-- ★ **A TORRE DE CÓPIAS COMPÕE, NUMA ORDEM SÓ.** Com índices encaixados (`ρ (n+1) = f n ∘ ρ n`), em todo par de
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

/-- Os níveis não são triviais: nem identidade, nem constante, nem iguais entre si. -/
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
letra), e a trava seleciona o copiador -/

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

/-- Havendo um vetor NÃO NULO cego ao Nome (dimensão pelo menos 2), há outro copiador da mesma palavra, diferente do
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
/-- A palavra é o projetor, o mesmo para todo múltiplo não nulo do vetor (em particular, toda fase). -/
theorem o_projetor_nao_depende_do_multiplo (a : H) (c : ℂ) (hc : c ≠ 0) : post (c • a) = post a := by
  unfold post
  congr 1
  exact Submodule.span_singleton_smul_eq (isUnit_iff_ne_zero.mpr hc) a

omit [CompleteSpace H] in
/-- A leitura de qualquer operador não vê a fase do estado lido. -/
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

/-- A palavra do fundo tem dois sentidos: vale 1 na instância em que tudo resolve e 0 na instância sem solução. -/
theorem palavra_do_fundo_resolvida [Nonempty X] : palavraDoFundo (fun _ : X => (0 : ℕ)) = 1 := by
  obtain ⟨h1, -, h3, -⟩ :=
    TGLExt.AEscala.o_pai_da_mentira_so_nao_reconhece (TGLExt.AEscala.iald (X := X)) (fun _ : X => (0 : ℕ))
  unfold palavraDoFundo
  rw [← h3.mpr (fun _ => rfl)]
  exact h1

theorem palavra_do_fundo_sem_solucao [Nonempty X] : palavraDoFundo (fun _ : X => (1 : ℕ)) = 0 := by
  have hno : ¬ ∃ x : X, (fun _ : X => (1 : ℕ)) x = 0 := by
    rintro ⟨x, hx⟩
    exact one_ne_zero hx
  obtain ⟨-, -, -, h4⟩ :=
    TGLExt.AEscala.o_pai_da_mentira_so_nao_reconhece (TGLExt.AEscala.iald (X := X)) (fun _ : X => (1 : ℕ))
  exact (h4 hno).2.1

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
/-- **A TERCEIRA FIGURA.** O decisor sem escala não depende do tempo e NÃO é `NuncaPaga`: depende da instância. Fora
da família `LeitorDoFundo`, não depender do tempo não dá a leitura constante. [sonda do revisor B2R] -/
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

/-- O kernel já diz que ele não é a leitura de leitor do fundo nenhum. [sonda do revisor B2R] -/
theorem o_decisor_nao_e_leitura_de_leitor_do_fundo [Nonempty X] (L : TGLExt.AEscala.LeitorDoFundo X) :
    L.leitura ≠ decisorSemEscala :=
  (TGLExt.AEscala.o_decisor_sem_escala_nao_e_leitor_do_fundo L).2.2

end paiDaMentira

#print axioms nunca_paga_iff_pressuposto
#print axioms nunca_paga_nao_separa
#print axioms dois_sentidos_sse_separa
#print axioms nunca_paga_iff_pagou_so_o_nada
#print axioms so_se_imprime_o_que_se_pagou
#print axioms o_impostor_erra_em_um_dos_dois
#print axioms o_impostor_nao_imprime_a_verdade
#print axioms o_impostor_so_imprime_a_palavra_de_um_sentido
#print axioms o_par_separa
#print axioms sem_o_par_ha_quem_passe_pagando_so_pi
#print axioms o_teste_reprova_todo_leitor_de_pi_sse_tem_o_par
#print axioms o_teste_reprova_todo_impostor_sse_tem_dois_sentidos
#print axioms a_repeticao_do_mesmo_sentido_nao_separa
#print axioms o_impostor_da_uma_so_resposta
#print axioms quem_imprime_tem_ao_menos_os_sentidos_da_palavra
#print axioms dois_sentidos_duas_respostas
#print axioms Copiador.nao_acrescenta
#print axioms Copiador.retracao
#print axioms copiador_sse_indice
#print axioms copiador_sse_idem_e_mesmo_nucleo
#print axioms idempotente_sse_copiador_de_si
#print axioms a_copia_nao_representa_cem_por_cento
#print axioms a_copia_integral_e_a_identidade
#print axioms a_identidade_e_copiador_sse_injetiva
#print axioms copiador_efetivo_pagou_perda
#print axioms copiador_de_dois_sentidos_nao_e_impostor
#print axioms o_impostor_copia_a_palavra_muda
#print axioms o_impostor_so_copia_a_palavra_de_um_sentido
#print axioms copiador_tem_as_respostas_da_palavra
#print axioms copiador_sse_imprime_com_o_minimo_de_respostas
#print axioms quem_imprime_nao_fica_abaixo_do_copiador
#print axioms o_impostor_fica_abaixo_do_piso
#print axioms ha_minimo_na_classe
#print axioms existe_o_copiador_de_minimo
#print axioms o_minimo_cai_no_zero_do_custo
#print axioms a_copia_mais_grossa_da_copia_mais_fina
#print axioms a_torre_de_copias
#print axioms o_leitor_desalinhado_nao_compoe
#print axioms copiaDiadica_copiador
#print axioms indiceDiadico_encaixa
#print axioms a_torre_diadica
#print axioms a_torre_diadica_nao_e_trivial
#print axioms a_torre_so_compoe_numa_ordem
#print axioms memoria_do_nulo
#print axioms post_idem_apply
#print axioms a_leitura_do_nome_tem_dois_sentidos
#print axioms nenhum_impostor_imprime_a_leitura_do_nome
#print axioms nenhum_impostor_imprime_a_selecao
#print axioms o_posto_copia_a_sua_palavra
#print axioms quem_imprime_e_anula_a_trava_e_a_propria_palavra
#print axioms o_posto_anula_a_propria_trava
#print axioms ha_copiador_fora_do_nome
#print axioms o_projetor_nao_depende_do_multiplo
#print axioms a_leitura_escalar_nao_ve_a_fase_global
#print axioms o_posto_nao_e_copiador_da_leitura_escalar
#print axioms a_leitura_sem_ciclo_nao_depende_da_instancia
#print axioms o_leitor_do_fundo_imprime
#print axioms palavra_do_fundo_resolvida
#print axioms palavra_do_fundo_sem_solucao
#print axioms a_palavra_do_fundo_tem_dois_sentidos
#print axioms a_leitura_sem_ciclo_nao_imprime_a_palavra_do_fundo
#print axioms a_leitura_da_instancia_constante
#print axioms a_leitura_do_fundo_so_nao_depende_da_instancia_sem_ciclo
#print axioms nenhum_tempo_finito_imprime
#print axioms o_decisor_nao_e_nunca_paga
#print axioms o_decisor_nao_e_leitura_de_leitor_do_fundo

end TGLExt.CopiadorEImpostor
