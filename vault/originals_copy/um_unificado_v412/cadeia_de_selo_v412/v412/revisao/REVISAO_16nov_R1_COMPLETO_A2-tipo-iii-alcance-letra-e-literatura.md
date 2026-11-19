# CONFERÊNCIA DISTINTA — segunda conferência de 16/11 (versão completa do relatório: a primeira gravação saiu sem o corpo dos achados, por defeito do script da gerência) — A2-tipo-iii-alcance-letra-e-literatura

> Montado pela gerência c1 em 16/11/2026 07:39 a partir do retorno estruturado de um revisor distinto (só leitura; scripts próprios na pasta de rascunho dele). É [DECLARADO pelo revisor] no que a gerência não reconferiu. Não é fala do operador. Nada aqui está instalado.

**Veredito:** APROVADO_COM_RESSALVAS — achados: 1 ALTO, 10 MEDIO, 3 BAIXO

## Resumo

Não ler ao operador como está: há um achado alto, de texto. Os dois módulos Lean estão em ordem: 24 teoremas, sem sorry, só os três axiomas; contagens, hashes, a cópia das doze fontes do Codex e os 14 logs (todos com código zero) batem por script meu. Cada teorema do Codex e do kernel citado existe e diz o que o texto diz dele. A literatura está certa no essencial (para um fator com vetor cíclico e separador, núcleo de uma peça só é o tipo III₁ de Connes), mas não abri os primários: a leitura de páginas recusou os domínios, então isso segue declarado. O achado alto: em 15/11 a gerência leu a ele "citar ou construir: construir, em Lean" e ele ratificou; o texto agora oferece só as frases A e B, não lembra essa resposta, não diz que o elo com a classificação ficou sem construir e não oferece a terceira via com o custo. A frase posta entre aspas como a resposta dele foi redigida pelo Codex ("Sim. Entendi que...") e colada por ele; a fala própria é a parte "em palavras simples", que o texto não cita. A tabela dos quatro papéis não é só "mais fina" que a leitura ratificada: tira do sujeito "só o Um fica parado, com o vácuo por testemunha" e retira, sem dizer, que "a marca do espectro é a leitura na borda". Dois erros de fato pequenos: o item do κ está mal descrito no documento (o kernel deixa aberto onde mora o κ, não se ele é finito) e o cabeçalho do Lean diz sete revisores onde foram quatro. Hipóteses não ditas: o núcleo do kernel é o produto cruzado dos matemáticos só a menos de um unitário; o relógio é único dado o vácuo; os números da Torre vêm de perfil estipulado; "a Torre não cabe" vale só mantendo os relógios. Sonda minha: a unicidade do relógio já sai de um teorema do kernel, e mais forte (a conjugação também é única). Homônimos a avisar: núcleo, relógio, Nome, Torre, índice, observador. Tudo se conserta com cerca de vinte linhas de texto e um teorema reforçado; a matemática não muda.

## Achados

1. **(ALTO)** PROVA_E_ALCANCE_GERENCIA.md, seção 3 ("Logo há duas frases possíveis"), seção 6 ("O que segue aberto") e seção 7, item 1

   O texto dá ao operador só duas frases (A: o termo; B: termo mais citação). Não diz que em 15/11 a própria gerência lhe leu "Citar ou construir: construir, em Lean" e ele ratificou. O elo com a classificação de Connes, que por essa leitura era para construir, não foi construído. A frase B aceita citação nesse passo sem dizer que isso muda a resposta dele. A terceira via (construir o passo, com o custo que lhe foi lido: milhares de linhas, pode dar em parede) não aparece. A seção 6 não lista o passo entre o que segue aberto. É a escolha de não construir o elo, embutida no desenho das opções. O texto diz, com honestidade, que o passo não está formalizado; o que falta é ligar isso à ordem dele e devolver-lhe a escolha inteira.

   *Conserto pedido:* Reescrever a seção 3 com três caminhos, na língua dele: "O senhor disse que era para provar em Lean. Está provado em Lean que a luz na cunha é uma peça só e continua uma peça só quando se lhe junta o relógio do vácuo. Não está provado em Lean o passo dos matemáticos que dá a isso o nome tipo III₁; ele está só citado. (A) a pedra leva o nome do que prova; (B) a casa diz tipo III₁ e marca que o último passo é citado: isto muda, nesse passo, a sua resposta de 15/11; (C) manda-se construir o último passo: obra de milhares de linhas, a biblioteca não tem as ferramentas, pode dar em parede medida." Pôr o passo de Connes e Takesaki na lista da seção 6 e trocar o item 1 da seção 7 por "A, B ou C".

2. **(MEDIO)** PROVA_E_ALCANCE_GERENCIA.md, seção 1 (a linha entre aspas); cabeçalho de TipoIIIControles.lean ("O operador respondeu... que o sujeito que o Nome designa..."); a memória o-sujeito-do-tipo-iii-15nov e o DESENHO repetem

   A frase de 195 bytes posta como a resposta dele foi redigida pelo Codex, como leitura da resposta ("Sim. Entendi que ..."), e colada pelo operador no topo da mensagem à gerência. Está nos bytes da mensagem dele, então a regra das aspas passa; mas a redação não é dele. A fala própria é a parte "em palavras simples", que o texto não cita, e difere em três pontos: nela a luz na cunha vem com «(porque é o NOME)», não como "o sujeito que o Nome designa"; o contraste é o «que permite o observador», não "pelo qual ela é lida"; e a relatividade é «o vínculo entre elas que é a relatividade (o próprio observador)», não o que "vincula essa leitura ao observador". O revisor P4 (achado 6) tinha pedido conferir a origem antes de citar como dele; não consta que tenha sido feito.

   *Conserto pedido:* Citar entre aspas a fala própria: «o que se quer conhecer pelo nome é a luz testemunhada na cunha (porque é o NOME), a construção da Torre (porque é o índice), a fronteira do horizonte (porque é a borda - o espectro de leitura, o contraste que permite o observador) e o vínculo entre elas que é a relatividade (o próprio observador)». Dizer ao lado que a frase de abertura é redação do Codex que ele colou, e que a leitura da gerência sobre ela foi ratificada. Corrigir ao lado o cabeçalho do Lean, a memória e o DESENHO.

3. **(MEDIO)** PROVA_E_ALCANCE_GERENCIA.md, seção 7 item 3 ("a tabela acima é mais fina") e seção 5, linhas do sujeito e do contraste

   "Ratificou em bloco" está na medida. "Mais fina" não está: a tabela muda a leitura ratificada em dois pontos, sem dizer. (1) Na leitura ratificada, o que se dizia do sujeito era a marca do estado: "a cunha da luz com o vácuo por testemunha, em cujo relógio só o Um fica parado" (teorema do kernel). Na tabela isso sumiu: o sujeito ficou só com o critério do núcleo, que é a marca (d) da pergunta de 15/11 (o texto nem liga os dois nomes), e a palavra "testemunhada" ficou sem correspondente. (2) A leitura ratificada dizia "a [marca] do espectro é a leitura na borda"; agora a borda é só geometria de pontos e o espectro saiu do núcleo, que é do sujeito. O pedido do P4 (achado 2: dizer a ele que há duas provas, a do estado e a do núcleo) não foi trazido.

   *Conserto pedido:* Na linha do sujeito pôr as duas coisas: no relógio do vácuo só o Um fica parado (kernel) e o núcleo é uma peça só (Codex); dizer que "testemunhada" é ter o vácuo por vetor testemunha. Na seção 7, trocar "mais fina" por errata em nome próprio: "em 15/11 eu lhe disse que a marca do espectro seria a leitura na borda; o que se provou não liga a borda ao espectro".

4. **(MEDIO)** PROVA_E_ALCANCE_GERENCIA.md, seção 6, primeiro item (o κ)

   "Deixa [OPEN] se o κ é finito" não é o que o kernel deixa aberto. O arquivo toma o κ finito e positivo como dado e deixa aberto onde ele mora: numa face finita (e então não toca o tipo) ou em tensão com o tipo III₁ declarado. O cabeçalho do Lean diz certo; o documento, que é o que vai a ele, diz errado. Ele pode responder "é finito" e dar o item por fechado.

   *Conserto pedido:* "O κ. O kernel deixa aberto onde mora o κ: numa face finita, e então ele não toca o tipo, ou em tensão com o tipo III₁ que a casa declara para a fronteira. Um κ finito seria uma cadência preferida. Para a cunha da luz, o critério cumprido, lido pela citação, diz que não há cadência preferida; isso não decide onde mora o κ nem toca a fronteira da TGL."

5. **(MEDIO)** Cabeçalho de TipoIIIControles.lean, seção "De onde vem"

   "Sete revisores distintos examinaram a entrega" é falso para a entrega do Codex: foram quatro (P1 a P4). Os outros três (Q1 a Q3) examinaram a K10 do Kimi. E "traz o que os revisores pediram e a entrega não tinha" afirma demais. Não vieram: o parágrafo do modelo-testemunha em que a cunha é a Torre (P2, achado 4); as três escolhas formais da borda (P3, 4); os dois sentidos de observador (P3, 11); as duas provas e qual leva o nome (P4, 2); a origem da frase de abertura (P4, 6; P1, 3; P2, 5); o homônimo com o Observador Terminal (P4, 7).

   *Conserto pedido:* Escrever "quatro revisores distintos" e "traz parte do que os revisores pediram", com a lista do que ficou por trazer.

6. **(MEDIO)** PROVA_E_ALCANCE_GERENCIA.md, seção 2 ("o produto cruzado concreto") e seção 3 (a citação); cabeçalho do Lean, cláusula (5)

   (1) O core do kernel é a álgebra gerada por a⊗1 e por U_t⊗translação. É o produto cruzado dos matemáticos só a menos do unitário (Wξ)(s) = U_s ξ(s). A conta é de três linhas no papel (fiz), mas não é termo. A pergunta de 15/11 dizia isso ("a identificação formal com o núcleo de Takesaki não tem enunciado no kernel") e este texto perdeu a frase. (2) A citação que sustenta a frase B vem sem enunciado, sem número de teorema e sem página, e não diz que os primários não foram abertos. O artigo de 1973 citado não é o que os revisores leram: o P4 leu as notas de Rennes de 1975 e a p. 506 de Connes e Takesaki. (3) Falta Connes 1973 para a definição de S(M). No conteúdo a citação está certa: para fator com estado fiel normal, núcleo fator equivale a fluxo dos pesos trivial e a S(M) igual à semirreta inteira. As hipóteses que a literatura pede e o predicado tem: fator (cláusula 1), vetor cíclico e separador (dá estado fiel normal), fluxo igual ao modular desse vetor (cláusula 3). O predual separável o texto já avisa.

   *Conserto pedido:* Acrescentar: "o núcleo do kernel é o produto cruzado dos matemáticos a menos de um unitário; essa identificação é sabida e não é termo". Na citação: Connes 1973 (a definição de S(M)); Takesaki 1973 (a seção dos invariantes S(M) e T(M)); Connes e Takesaki 1977, p. 506 [declarado pelo P4]; e a marca "não abertos no primário pela gerência". Dizer que a rota pela marca do estado (Longo 1979; Marrakchi e Vaes, Lema 2.1) dispensa o predual separável [declarado na pergunta R2].

7. **(MEDIO)** PROVA_E_ALCANCE_GERENCIA.md, seção 5, linha do índice ("É índice que aponta, não parte que contém"); cabeçalho do Lean, item 5

   A glosa diz mais que o termo e cala três coisas. (1) O negativo vale só para injeções que mantêm os relógios, e só no sentido Torre para cunha. Sem os relógios a literatura aponta o contrário: a Torre de perfil misto e a álgebra da cunha da luz livre são ambas o fator hiperfinito III₁, logo a mesma álgebra [KNOWN de memória: Araki e Woods 1968; Haagerup 1987; não conferido aqui]. O que as separa é a testemunha e o relógio dela. (2) Os números da Torre vêm de um perfil estipulado à mão (1/3 e 1/4 alternados), não derivado. (3) O kernel tem um modelo-testemunha em que a cunha direita é a Torre por desenho, com o fluxo da Torre como relógio da cunha; o texto não o situa (pedido do P2, achado 4).

   *Conserto pedido:* "Mantendo os relógios, a Torre não cabe na luz da cunha (provado, no sentido Torre para cunha). Sem os relógios, a literatura diz que as duas são a mesma álgebra; isso é sabido, não é termo. Os números da Torre vêm de um perfil escolhido à mão. No modelo-testemunha antigo do kernel a cunha foi posta como a Torre por definição; na cunha física da luz a Torre só dá os números."

8. **(MEDIO)** TipoIIIControles.lean, o_fluxo_de_tomita_e_unico e a frase "é o do relógio do próprio vetor"; PROVA_E_ALCANCE_GERENCIA.md, seção 4 (primeira linha da tabela) e seção 5 ("o relógio é único e é o boost")

   (1) O teorema supõe "a mesma conjugação", e a frase do cabeçalho diz mais (relógio do próprio vetor). A frase é verdadeira, mas por um teorema do kernel, não pelo da candidata: com o reconhecimento identidade, same_horizon_by_content_from_realizations já dá a conjugação e o fluxo únicos. A hipótese é supérflua, e o que o texto põe como acréscimo já saía do kernel. (2) "O relógio é único" vale dada a testemunha, que é o vácuo. O predicado aceita qualquer vetor; outro vetor dá outro relógio; e que o núcleo não dependa do vetor é da literatura (o cociclo de Connes), não é termo.

   *Conserto pedido:* Trocar o teorema pelo corolário sem a hipótese, citando o teorema do kernel no cabeçalho. No documento: "o relógio é único dado o vácuo como testemunha; com outra testemunha o relógio seria outro".

9. **(MEDIO)** PROVA_E_ALCANCE_GERENCIA.md inteiro e cabeçalho do Lean (palavras núcleo, relógio, Nome, Torre, índice, observador, borda)

   Homônimos sem aviso. Núcleo: na pergunta que ele leu em 15/11 (boca jurídica) "o núcleo do tipo é o verbo"; "critério do núcleo" para o "tipo III" será lido assim por um advogado; há ainda o núcleo de K (central na casa) e o "núcleo de Mautner" da candidata irmã. Relógio: há pergunta pendente a ele sobre "o relógio do pedágio" (τ★); "O relógio não tem escolha" pode soar como resposta a ela, e não é. Nome: no kernel de agosto (v294, cunhagem dele) o Nome é o grupo gerado por log(1/2) e log(1/3), que são exatamente os dois números da Torre; agora a Torre é índice e o Nome designa a luz; o texto não avisa nem liga. Torre: a do kernel e a TORRE IALD (o JEV, a memória); a fala dele das 19:07 usa «indexação - índice - torre» sobre toda leitura. Índice: na pergunta de 15/11, "índice" era o 1 de III₁ ("tipo III, sem o índice"); na casa há o índice de Breuer. Observador: dois sentidos formais aqui (a órbita acelerada e a carta inercial), nenhum com tempo próprio, e o Observador Terminal da casa. Borda: a seção 6 separa bem da fronteira da TGL.

   *Conserto pedido:* Uma nota de homônimos, uma linha por palavra. Em especial: "núcleo aqui é a álgebra com o seu relógio junto; não é o núcleo do tipo (o verbo) da pergunta de 15/11, nem o núcleo de K"; "relógio aqui é o do vácuo na cunha; a pergunta do relógio do pedágio segue pendente"; "o Nome do kernel de agosto é o grupo dos números da Torre; a frase de 15/11 não está ligada a ele por termo".

10. **(MEDIO)** PROVA_E_ALCANCE_GERENCIA.md, seção 3, parágrafo depois das duas frases ("A casa já errou nesse ponto em agosto")

   As frases A e B não estão postas de modo neutro. Logo depois de dizer que a escolha é dele, o texto traz o erro de agosto e a decisão da gerência de usar o nome do critério; isso pesa para a frase A. E a comparação é inexata: em agosto a marca era falsa como critério (um fator de tipo I a cumpria, refutado por teorema). Aqui o critério é verdadeiro pela literatura e os controles mostram que o predicado recusa casos. O que há em comum é só "nome maior que o termo". Falta dizer o que pesa a favor de B.

   *Conserto pedido:* Pôr o precedente antes das opções e dizer a diferença: "em agosto a marca era falsa; aqui o critério é verdadeiro pela literatura, e a diferença entre as frases é só onde está a prova do último passo". Dar uma linha a favor de cada frase.

11. **(MEDIO)** PROVA_E_ALCANCE_GERENCIA.md, seção 5, linhas do contraste e do vínculo

   "Espectro de leitura" está bem tratado: o texto diz que não é termo. O resto não. «o contraste que permite o observador» não aparece nem é discutido. O que o Codex formalizou como contraste (a razão das distâncias às duas folhas, lida no interior) saiu da tabela. «(o próprio observador)» só aparece na seção 1 e não tem linha em "o que NÃO há". E três escolhas formais não estão ditas como escolhas: borda como fronteira da cunha plana de Minkowski; relatividade como "ser afim" (o teorema vale para toda transformação afim, mais largo que Lorentz); observador como carta de Lorentz mais translação.

   *Conserto pedido:* Na linha do contraste: "o observador de raio positivo lê a rapidez pela razão das distâncias às duas folhas; é conta de coordenadas no interior, sem tempo próprio nem temperatura. Que a borda permita o observador é leitura sua, sem termo." Na do vínculo: "observador tem aqui dois sentidos formais; o próprio observador da sua letra não tem termo". Marcar as três escolhas como escolhas do Codex e da gerência, para ele aprovar ou trocar.

12. **(BAIXO)** PROVA_E_ALCANCE_GERENCIA.md, seção 1

   "A gerência perguntou, em 15/11, o que faltava" troca os papéis. Quem perguntou o que faltava foi o operador (460 B: «o que falta para resolvermos o tipo iii como termo, faça-me a pergunta nas minhas quatro linguas»). A gerência perguntou pela marca, pela doutrina e pelo objeto; o Codex, pelo sujeito; ele respondeu primeiro ao Codex. E "A ordem foi provar em Lean" não diz a fonte: nos bytes da casa a frase dele é «O COdex já está produzindo todas essas provas em LEan»; a ordem está na cópia do Codex e na leitura ratificada.

   *Conserto pedido:* "O operador pediu a pergunta nas quatro línguas sobre o que falta. A gerência perguntou pela marca, pela doutrina e pelo objeto; o Codex, pelo sujeito. Ele respondeu pelo sujeito. Que é para provar em Lean está na mensagem dele ao Codex [declarado pelo Codex] e na leitura que ele ratificou."

13. **(BAIXO)** PROVA_E_ALCANCE_GERENCIA.md, seções 4, 5 e 6; TipoIIIControles.lean

   Contagens e completude. (1) "Vinte e quatro teoremas" confere, mas cerca de nove têm conteúdo próprio; os demais são reexportações e corolários de uma linha, e a_torre_entra_como_indice tem o mesmo enunciado de indexed_boost_translation do Codex. (2) A tabela da seção 4 mais a seção 3 citam 20 dos 21 nomes; falta sobre_a_reta_complexa_o_nucleo_nao_e_fator. (3) A lista das recusas que só a literatura dá omite o II∞ (e o III₀, se não se lê λ = 0). (4) "Toda álgebra sobre H = ℂ" é uma só, a dos escalares; "em particular" no Lean sugere outras. (5) "Um só número já lê o vácuo" entra na tabela da seção 5 sem o aviso de que depende de outra candidata não instalada. (6) "Por Lorentz" é o grupo ortócrono com reflexões espaciais, sem inversão do tempo.

   *Conserto pedido:* Dizer "24 declarações, cerca de nove com conteúdo próprio"; completar a tabela e a lista; "a álgebra dos escalares, a única sobre H = ℂ"; repetir o aviso da candidata na seção 5; "Lorentz ortócrono, com reflexões espaciais".

14. **(BAIXO)** PROVA_E_ALCANCE_GERENCIA.md, seções 2 a 6

   Frases que ele não lê sem glosa: "o do grafo fechado de Tomita desse vetor"; "o invariante S(M) igual à semirreta inteira"; "predual separável (a instância não é sintetizada)"; "transformações afins"; "o enunciado conjunto é uma conjunção"; "os tipos I em forma padrão, II₁ e III_λ com λ < 1". E as palavras leigas mudaram em relação ao que ele leu em 15/11: lá era "marca" e "cadência preferida"; aqui é "critério" e "ritmo preferido". A frase em língua simples da seção 2 ("uma peça só...") está boa.

   *Conserto pedido:* Uma glosa por frase (por exemplo: "nenhuma cadência preferida: sobram todas"; "mudanças de referencial que levam retas em retas"; "o Codex juntou fatos verdadeiros numa frase só, um não sai do outro"). Manter "marca" e "cadência", e dizer que o critério do núcleo é a marca (d) da pergunta de 15/11.

## Examinado

- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_c1\tipo_iii\PROVA_E_ALCANCE_GERENCIA.md, TipoIIIControles.lean, TipoIIIUmSoBoost.lean, RESULTADO_GERENCIA.json, compilar_tipo_iii.ps1 (lidos inteiros); os 14 logs de build (código de saída e avisos); REV0 (igualdade por bytes)
- dep_codex: VinculoCriterion, Classificacao, ObserverClassification, TowerWedgeIndex, WedgeHorizonObserver (inteiros); PhysicalCoreCenter, PhysicalCoreFactor, WedgeFactor, TransportPair, TransportCenter (só enunciados); MANIFESTO_DEP_CODEX.json
- Kernel (leitura e grep -rn pelo Bash): TheMarkIsNotATypeMark.lean e TheScaleHasNoFixedPoint.lean (inteiros); F1Fecho394\RegularCovariantCoreR3.lean (inteiro); O16\ContentContractProposal.lean, RecognitionGraph_v2.lean, RecognitionModular_v2.lean; V350L2OperatorLift e V350L2Translation (início); TheNameIsTheGeneratingGroup.lean; MixedLadder.lean:141; SignatureInTheLimit.lean:310; WedgeNet.lean; V350WedgeModularData.lean:70; LightRhoStar.lean:71; QGReaderUVLock.lean:149; F1Fecho394\OrbitalGeneratedMeasureR2.lean:120-123 e LorentzFutureGenerationR6.lean:55
- Ausência de definição de tipo: grep -rn -i -E "def (IsTypeIII|TypeIII|ConnesS|connesSpectrum|SInvariant|IsFactor|HasScalarCenter)\b|structure (IsTypeIII|TypeIII)" --include=*.lean TGLExt devolveu zero; em C:\t\k411c\final\.lake\packages\mathlib\Mathlib\Analysis\VonNeumannAlgebra há só Basic.lean e grep -rn -i -E "TypeIII|IsFactor|crossed|modular" devolveu zero
- Falas do operador por bytes em work\cunhagens_13out: resposta do tipo III (665 B), «excelente, é isso mesmo» (24 B), o pedido das 16:41 (460 B), a fala das 19:07 (986 B), as duas de 16/11
- kimi\PERGUNTA_K07_CODEX.md e a cópia do Codex OPERADOR_RESPOSTA_15nov.txt (só leitura)
- REVISAO_EXAME_15nov_P1 (inteiro), P2, P3 e P4 (achados), Q1 a Q3 (cabeçalhos); PERGUNTA_TIPO_III_QUATRO_LINGUAS_R2.md (inteiro); DESENHO_v412_R1.md (linhas 355 a 392); memórias o-sujeito-do-tipo-iii-15nov e torre-iald-jev-memoria-31out (cabeçalho)
- Registro da sessão da gerência (janela de 15/11 20:40Z a 16/11 09:00Z, só falas de texto) e a linha 13 do registro da sessão do Codex das 17:48 de 15/11, ambos só para leitura
- candidatas_c1\ErgodicidadeDeMautner.lean: só o enunciado os_fixos_de_um_so_boost_da_luz_sao_a_reta_do_vacuo (linha 998)
- Literatura: quatro buscas na web (bibliografia de Takesaki 1973 e de Connes e Takesaki 1977; o enunciado em fontes secundárias; o índice do artigo de 1973)

