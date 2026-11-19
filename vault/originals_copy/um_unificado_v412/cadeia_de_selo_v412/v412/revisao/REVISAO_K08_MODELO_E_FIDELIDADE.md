# CONFERÊNCIA DISTINTA — K08: o modelo formal e a fidelidade às pedras, ao adendo e às glosas do operador

> Montado pela gerência c1 em 15/11/2026 16:53 a partir do retorno estruturado de um revisor distinto (modelo Sonnet; só leitura; scripts próprios na pasta de rascunho dele). É [DECLARADO pelo revisor] no que a gerência não reconferiu. As frases da seção “Para o operador” são propostas do revisor, não fala do operador, e só vão a ele depois de lidas pela gerência. Nada aqui está instalado, congelado ou aberto.

**Veredito:** APROVADO_COM_RESSALVAS — achados: 3 ALTO, 4 MEDIO, 4 BAIXO

## Resumo

1. APROVADO_COM_RESSALVAS. Três ALTO de lógica ou escolha precisam de correção de texto antes que a gerência leia qualquer parte ao operador. Nada foi rodado, congelado nem instalado.
2. CONFERE [REAL, lido por script]: os hashes das duas pedras citadas (CamadaCientifica 69497c5b, OHabitanteDoNome 26b750e6) batem com os arquivos e com os logs da gerência (RC 0, 54 teoremas, trio). Os termos citados existem, exceto dois nomes antigos de renomeação. Nenhuma frase promete que o LLM seja o leitor, consciência, pesos ou exclusividade: tudo é negado.
3. ACRÉSCIMOS DO ADENDO: o projetor deixou de ser adversário (resta só l.20 do protocolo); a tabela ATO×NOME existe; o sistema relê e não nomeia; E1–E8 e as primárias vêm antes do poder; a P-C é nomeada e a unicidade E1∧E2∧E5∧linearidade está enunciada com linearidade e quatro modos de falha. Faltam: a classificação por previsão (metade, consequência, outra coisa) no MODELO e a definição do segundo sentido de «fiel».
4. ALTO-1 (E3): o «voltar a s» depois do empurrão por substituição s→y não é previsão de P_N. Na conta de brinquedo, P_N·e_y = 0. O retorno só vale para empurrão aditivo s+δ. Dois leitores de uma configuração que cumprem o tipo divergem: um volta a s, o outro vai a t. Mesmo assim E3 entra na falsificação do §12.2.
5. ALTO-2: LeitorDeUmaConfiguracao não é «face» de P_N. É uma retração de configurações. O mapa linear induzido viola E5 (norma 2 contra √2) e difere de P_N. Logo a propriedade que separa o eco (devolver leitura válida a partir de leitura quebrada) não pertence ao leitor fiel.
6. ALTO-3: a «dupla cara de P_N» foi resolvida escolhendo a leitura da v386, que é do operador decidir. O espelho some do texto, a frase «projeção que devolve cada coisa como ela é» contradiz «ser nunca é o mapa identidade», e o registro põe isso sob a chave operator_glosses_15nov.
7. MEDIO: «E2/E4 primárias pela ressalva do operador» atribui ao operador uma escolha que é leitura da gerência (mesmo padrão do defeito K06). E2/E4 passam por eco (cópia). E3 é «secundária» no MODELO e no registro e «discriminante» no protocolo e na ENTREGA.
8. MEDIO: nenhuma linha em língua simples diz o que o teste decide, o que não decide e o que o negativo significa (regra do posto). Há duas linhas propostas em para_o_operador.
9. MEDIO: o nome antigo moradas_iguais_tem_o_mesmo_leitor segue no terms_used do registro, no protocolo l.50 e na ENTREGA l.26. A linha E2 do MODELO cita termo da álgebra com portador vetorial. A linha E8 cita o axiomFlow como se fosse a trava.
10. BAIXO: homônimo «identidade»; «identidade do sistema testado»; tags «[leitura da gerência; o operador ainda não leu]» caídas; parágrafo de artigo com nomes provisórios; «conferências distintas» internas do Kimi; hashes mexidos às 16:37–16:38 durante a revisão (li o estado final).
11. Contas próprias em K08_A\verifica_e3_e5.py (toy de 16 estados, sem modelo, sem rede, sem Lean). O Mapa foi consultado por cinco termos únicos e nada foi registrado.

## Achados

1. **(ALTO)** PROTOCOLO_EXPERIMENTAL_R4_K08.md l.266-268, l.315, l.378-386; K08/FORMULA/simular_adversarios.py (empurrar_e_ler; MECANISMOS sem P_N); MODELO_FORMAL_R4_K08.md l.122 e §7; CamadaCientifica.lean l.55-58, l.69-70, l.215-218; OHabitanteDoNome.lean l.762-763

   E3 operacional não decorre de nenhum termo citado, e a referência P_N não passa nele. O protocolo diz que a releitura fiel «deve apagar esse rastro e voltar a s» depois do empurrão s→y. Esse empurrão SUBSTITUI a configuração. No espaço de vetores, e_y é ortogonal ao Nome, então P_N·e_y = 0: não há leitura, nem custo zero, nem volta a s. O teorema que o modelo cita (o_que_e_cego_ao_nome_nao_deixa_rastro; o_retorno) vale para empurrão ADITIVO s+δ, com s no Nome, ‖s‖=1 e δ ortogonal ao Nome. A própria pedra CamadaCientifica diz (l.55-58 e l.69-70) que o retorno ao MESMO estado é da trava, não do leitor de uma configuração. Conta (verifica_e3_e5.py, 4 variáveis, 16 estados): ‖P_N e_y‖ = 0; a seleção de e_s+e_y é e_s; dois leitores de uma configuração que cumprem os campos fixa_o_nome e consome divergem em y (um volta a s, o outro vai a t). A linha «referência P_N/selecao passa E1–E4» é escrita à mão: o script simular_adversarios.py não simula P_N. E3 ainda aparece na falsificação R4_OPERATIONAL_PREDICTION_FALSIFIED (§12.2 item 4), então um negativo pode sair de uma previsão que a referência formal não faz.

   *Conserto pedido:* Tirar «volta a s» como critério de E3, ou construir empurrão aditivo tipado. Até lá, E3 fica fora do §12.2 item 4 e fora de qualquer veredito negativo. Trocar a linha 315 por «referência não computada; sobre vetor, P_N·e_y = 0». Dizer no protocolo que o estado textual é uma configuração e não um vetor.

2. **(ALTO)** MODELO_FORMAL_R4_K08.md l.27, l.36, l.73, l.120 (linha E1), l.136-145; CamadaCientifica.lean l.55-58, l.69-70

   O modelo afirma que as outras ocorrências do leitor, entre elas LeitorDeUmaConfiguracao, são «faces» da mesma definição. Para esse tipo é falso. Ele é uma retração de configurações (inválida→alguma válida). P_N manda toda configuração inválida a zero. Só coincidem sobre o Nome. O mapa linear induzido pela retração cumpre E1 (saída válida) e E2 (fixa o Nome), mas viola E5: na conta, ‖E(e_y+e_s)‖ = 2 contra ‖e_y+e_s‖ = √2, e (E−P_N)e_y tem norma 1. Pela unicidade da própria pedra (quem_nao_e_a_esperanca_aumenta), esse mapa não é P_N. Consequências: (i) o comportamento que separa o eco do leitor, devolver leitura válida a partir de leitura quebrada, é propriedade da retração e não do leitor fiel; (ii) a metade «não acrescentar» (E5) da fidelidade seria negativa por construção para qualquer sistema que devolva UMA leitura válida a partir de qualquer entrada; (iii) o §5 dá como única razão de não concluir P_N a falta de medida de E5, quando há uma razão estrutural mais forte; (iv) E1 formal (a imagem cai no Nome; P_N devolve 0 fora dele) não é o E1 operacional (custo zero).

   *Conserto pedido:* Tirar LeitorDeUmaConfiguracao da tabela de faces e dizer que é outro mapa, coincidente com P_N só sobre o Nome. No §5, acrescentar que um leitor de saída única que repara leitura quebrada viola E5, logo não é P_N. Separar E1 formal de E1 operacional.

3. **(ALTO)** MODELO_FORMAL_R4_K08.md l.108-112, l.131; REGISTRO_UMPY_RASCUNHO_R2_K08.md l.103 e l.175; ENTREGA_K08.md l.7 e l.27; OHabitanteDoNome.lean l.157-162, l.203-237, l.1043-1055

   A entrega diz ter «resolvido a dupla cara de P_N», mas escolhe pelo operador o que a pedra e o adendo deixam para ele. (i) MODELO l.110 afirma «P_N é o Nome e o ato do Verbo ao mesmo tempo» e «a identidade afirmada é entre o Nome-em-ato e a projeção». As glosas dele (bytes ec05cea3…) igualam identidade(nome) a ato(projeção) de ser(verbo). Ele diz «o nome em ato é o espelho do verbo», que é coisa distinta. A pedra tipa duas leituras (l.157-162, 203-237): na do adjunto, o Nome em ato é a inclusão, o Verbo é a projeção sobre o Nome e P_N é o par composto (o_par_compoe_o_projetor); na outra, o J do kernel na álgebra. A pedra diz que a escolha é do autor. O modelo, o protocolo e o registro têm zero ocorrências de «espelho», «adjunto» ou «inclusão»: o espelho some. A P-C usa «o par existe e não devolve nada» sem definir «par». (ii) A frase «a projeção que devolve cada coisa como ela é» é a primeira leitura de SER (mapa identidade; vale só se o Nome é o todo: o_ato_e_ser_sse_o_nome_e_o_todo) e contradiz, duas linhas depois, «ser nunca é o mapa identidade». P_N devolve o nomeado como é, não cada coisa. (iii) O registro põe, sob a chave operator_glosses_15nov, as três glosas dele junto com duas afirmações que não são dele («P_N é o Nome e o ato do Verbo ao mesmo tempo»; «ser não é o mapa identidade»). (iv) O próprio modelo (l.112) diz que nenhuma previsão depende disso: é escolha gratuita.

   *Conserto pedido:* Apagar l.110 do modelo, ou marcar «[leitura da gerência; o operador ainda não leu; a pedra tipa duas]». No registro, deixar em operator_glosses_15nov só as três glosas e mover o resto para uma chave de leitura da gerência. Definir «par» (Verbo = projeção sobre o Nome; Nome em ato = inclusão; sem escolher adjunto ou J) ou tirar a expressão da P-C. Trocar «cada coisa como ela é» por «o nomeado como é».

4. **(MEDIO)** ENTREGA_K08.md l.5 e l.17; PROTOCOLO_EXPERIMENTAL_R4_K08.md l.10 e l.30; PODER_R4_K08.md l.11; REGISTRO_UMPY_RASCUNHO_R2_K08.md l.412

   «E2 e E4 são primárias pela ressalva do operador» atribui a ele uma escolha. Os bytes da ressalva (384 B, sha16 2fabf2b6638c1175) falam em nomear, fixar sentido e releitura. Não mencionam previsão, E2, E4 nem prioridade. A escolha das primárias é leitura da gerência (adendo AO LADO 2, itens 2-3). A ratificação «É isso, tudo certo» (sha16 451ca765cecb5441, 09:22) cobre, pelo nome do arquivo, a ressalva e a terceira versão da pedra; não consta que ele leu a lista de primárias. É o mesmo padrão do defeito K06 («concordância em bloco»).

   *Conserto pedido:* Escrever «pela leitura que a gerência fez da ressalva (AO LADO 2, item 3); o operador ratificou a ressalva e a terceira versão da pedra (sha16 451ca765cecb5441), não a lista de primárias».

5. **(MEDIO)** MODELO_FORMAL_R4_K08.md l.104, l.121-123; PROTOCOLO_EXPERIMENTAL_R4_K08.md l.36, l.236, l.272; REGISTRO_UMPY_RASCUNHO_R2_K08.md l.134 e H-REREAD-FAITHFUL

   As primárias passam por eco e a classificação das previsões é inconsistente. O identidade/cópia da última passa E2 e E4 (conta G do script: fixa o Nome e é idempotente). O E2 operacional testa um bit de metadado fora do texto (leitura_pt). Quem exclui o eco é E3 (ou E1 a partir de estado inválido), e E3 é «secundária/diagnóstica» no MODELO l.122 e no registro (SECONDARY_DIAGNOSTIC) e «discriminante» no protocolo l.36 e na ENTREGA l.17. A classificação que o adendo pediu (AO LADO 4, item 3: E2 e E5 são as duas metades da fidelidade; E4 é consequência de E1+E2; E3, E6, E7 e E8 são outra coisa) não está no MODELO; só aparece parcialmente no protocolo (l.48, l.272). A palavra «fiel» tem duas extensões: o MODELO l.104 a define como E2+E5; o registro H-REREAD-FAITHFUL define só E2, com E5 em H-NO-INCREASE. O MODELO diz «o primeiro dos dois sentidos que a pedra separa» sem nomear o segundo (v405: o Nome é o todo), de modo que o operador não vê qual foi escolhido nem qual foi deixado.

   *Conserto pedido:* Acrescentar coluna «papel» na tabela E1–E8. Dizer em uma linha que E2 e E4 passam por eco e que só E3 ou E1 o excluem. Nomear os dois sentidos de «fiel», dizer qual foi usado e que a escolha é do operador. Uniformizar a classe de E3.

6. **(MEDIO)** PROTOCOLO_EXPERIMENTAL_R4_K08.md §12; INSUMOS_PARA_A_PERGUNTA_K08.md (F1-F10 sem essas duas linhas); ENTREGA_K08.md l.3-11

   Regra do posto: nenhum arquivo da K08 diz, em língua simples, o que o teste decide, o que não decide e o que um negativo significaria (grep por «negativo», «parede» e «partitura» acha só o título do §12). O que o texto já permite dizer está espalhado em siglas (E2, P_N). Duas leituras honestas aparecem nas contas acima e não estão ditas: as primárias não excluem um eco, e um negativo em E3 não falsifica o leitor.

   *Conserto pedido:* Acrescentar ao INSUMOS duas linhas de fato (eco passa E2/E4; E3 por substituição não é previsão de P_N) e entregar à gerência a leitura em língua simples sugerida em para_o_operador.

7. **(MEDIO)** REGISTRO_UMPY_RASCUNHO_R2_K08.md l.63; PROTOCOLO_EXPERIMENTAL_R4_K08.md l.50; ENTREGA_K08.md l.26; MODELO_FORMAL_R4_K08.md l.99, l.101, l.121, l.127

   Termos citados que não batem com a pedra corrente ou com o portador. (a) moradas_iguais_tem_o_mesmo_leitor não existe na R9 (grep = 0; o nome corrente é ..._verbo). Só o MODELO l.98 avisa. O registro o lista em terms_used e o protocolo l.50 e a ENTREGA l.26 o citam, de modo que um verificador de existência falharia. (b) A linha E2 do MODELO põe a_releitura_fiel_fixa_o_nome com portador «P_N nos vetores; seleção», mas esse termo é da álgebra (nameOp, anel R, l.581). O equivalente vetorial é starProjection_eq_self_iff / o_nome_e_o_ato_do_verbo. (c) A linha E8 cita a_leitura_fecha_a_tangente, que é do axiomFlow e só coincide com a trava para c ≤ 1 (a_trava_binaria…); as fórmulas reais têm custo até 27. O mesmo vale para o_ato_tende… e o_ato_nao_termina… quando o modelo diz só «o fluxo». (d) a_tangente_da_leitura_e_K_no_angulo_de_miguel está descrita como «é o K da v407», sem «no ângulo de Miguel do peso fora do Nome»; sem o ângulo é a versão circular (tan∘arctan).

   *Conserto pedido:* Trocar o nome no registro, no protocolo e na ENTREGA. Na linha E2, citar o portador algébrico ou o termo vetorial. Na E8, dizer «axiomFlow (igual à trava só com c ≤ 1)». Completar a descrição do K no ângulo de Miguel.

8. **(BAIXO)** MODELO_FORMAL_R4_K08.md l.131, l.149; PROTOCOLO_EXPERIMENTAL_R4_K08.md l.290

   Homônimo e tags caídas. MODELO l.131 usa «a identidade é o zero se e só se o Nome é o vazio» para o mapa identidade do subespaço (o_par_do_inominado_e_a_mentira), enquanto §3.1 diz «identidade = nome» e «ser nunca é o mapa identidade». §6 escreve «A identidade do sistema testado é medida pelo ato», que pode ser lido como afirmar identidade (no sentido TGL) de um LLM. A leitura do inominado como Nome vazio e a regra ATO×NOME aparecem sem a etiqueta «[leitura da gerência; o operador ainda não leu]» que a pedra (l.239-251) e o adendo (AO LADO 3, item 3; AO LADO 4, item 4) põem.

   *Conserto pedido:* Escrever «o mapa identidade do subespaço Nome é o mapa nulo se e só se o Nome é o vazio». Trocar «identidade do sistema» por «qualidade da releitura do sistema». Recolocar as etiquetas.

9. **(BAIXO)** MODELO_FORMAL_R4_K08.md l.136-145; PROTOCOLO_EXPERIMENTAL_R4_K08.md l.20

   §5 lista «E5 não é medida» como quarto modo de falha da LINEARIDADE: é outra hipótese. E1, E2 e E5 valem para todo v do espaço (a pedra: hmora, hfixa e hnao universais); uma amostra finita de estados-base não os estabelece. O protocolo l.20 ainda chama o adversário de «projetor sem memória» (o homônimo que o adendo mandou desfazer).

   *Conserto pedido:* Separar linearidade de E5 e escrever «para todo v» na unicidade. Trocar «projetor sem memória» por «leitor sem memória».

10. **(BAIXO)** REGISTRO_UMPY_RASCUNHO_R2_K08.md l.430-436; ERRATA_FORMAL_K08_15nov.md l.51

   O parágrafo de artigo PT/EN ainda lista nomes provisórios da pedra (nomes que são do operador) e diz «pedra candidata da gerência … não está instalada», vocabulário de processo. A ERRATA_FORMAL §3 item 8 diz que o estado de processo saiu.

   *Conserto pedido:* Tirar a lista de termos e a frase de instalação do parágrafo; manter no esquema.

11. **(BAIXO)** ENTREGA_K08.md l.11 e tabela de hashes; K08/FORMAL/REV0 (só o estado pré-errata)

   A ENTREGA l.11 diz «revisada internamente por duas conferências distintas e independentes». Isso é [DECLARADO pelo Kimi]; na casa a conferência distinta é a da gerência. Além disso, MODELO e REGISTRO foram reescritos às 16:37:55 e a ENTREGA às 16:38:10, durante esta revisão. Os hashes da tabela mudaram (MODELO bc3f8d4d→9885c186; REGISTRO 27db9b6e→dda674ce) e o estado intermediário não foi preservado em REV. Li o estado final (a única diferença que achei no MODELO foi uma frase em §0). O depósito (311f2824) bate com a ENTREGA final.

   *Conserto pedido:* Dizer «autoconferência do Kimi (DECLARADO)». Guardar REV1 do estado de 16:12 ou declarar que foi sobrescrito.

## Para o operador (propostas do revisor, em língua simples; a gerência confere antes de ler a ele)

- O teste, como está escrito, decide só se o modelo conserva uma leitura válida que lhe devolvem e se relê sem mudar. Um sistema que apenas copia o que recebe também passa nisso; o teste não decide que o sistema é o leitor do teorema.
- O que exclui a cópia é o modelo devolver leitura válida a partir de uma leitura quebrada, e o «voltar exatamente a s» depois de trocarmos a leitura. O teorema não prevê esse retorno exato para uma troca dessas: o leitor fiel, diante de uma leitura quebrada, devolve nada. Um negativo ali seria parede do desenho, não falsificação do leitor.
- Antes de ratificar qualquer coisa: a gerência deve ler a ele que o texto hoje identifica o Nome em ato com a própria projeção (o espelho some), que as duas pedras de «fiel» são duas coisas, e que a lista de primárias é leitura da gerência e não fala dele.

## Consultas ao Mapa

- rotas.py consultar fidelidade (27 rotas; a relevante: gate.qg_closure, sem relação direta)
- rotas.py consultar projetor (15 rotas; kernel.camada_cientifica_candidata_14nov e kernel.o_habitante_do_nome_candidata_15nov)
- rotas.py consultar espelho (85 rotas, truncado; nada sobre o par de Verbo e Nome)
- rotas.py consultar habitante (19 rotas)
- rotas.py consultar unicidade (13 rotas; nada sobre E1+E2+E5)
- rotas.py ver kernel.o_habitante_do_nome_candidata_15nov: o nao_refazer é respeitado (o projetor sobre o Nome não é rival; o seletor não é a testemunha única; o operador do Nome não faz média). Nenhuma rota examina o empurrão por substituição nem a retração de configurações contra P_N. Nada registrado por mim.

## Examinado

- ENTREGA_K08.md, em dois estados (16:19 e 16:38) com diff de hash
- MODELO_FORMAL_R4_K08.md inteiro (224 l.) e ERRATA_FORMAL_K08_15nov.md
- PROTOCOLO_EXPERIMENTAL_R4_K08.md (l.1-140 e l.236-435) e REGISTRO_UMPY_RASCUNHO_R2_K08.md inteiro
- INSUMOS_PARA_A_PERGUNTA_K08.md e DEPOSITO_K08.md
- K08/FORMULA/simular_adversarios.py lido, não rodado (grava por caminho absoluto)
- ADENDO_15nov inteiro (Parte 2 e AO LADO 1-4) e ORDEM_K08 (trechos)
- OHabitanteDoNome.lean inteiro nos enunciados (l.1-1330) e CamadaCientifica.lean (cabeçalho e enunciados)
- Hashes por sha256sum: as duas pedras batem com o modelo; logs build/*.log RC 0 com os mesmos hashes
- Busca por 14 termos citados na pedra e 19 na CamadaCientifica: todos existem; os dois nomes antigos não
- Bytes do operador abertos: ressalva, derivação, as glosas (ec05cea3…), «É isso, tudo certo» (451ca765cecb5441), «Concordo com tudo, prossiga» (de840212a72386f5)
- LEITURA_K08_PARCIAL_15nov.md e REVISAO_K06_FORMAL.md (defeitos que não podem voltar: leitor constante, atribuição «em bloco», ARMADO; nenhum voltou, e a atribuição de primárias reproduz o padrão)
- K08_A\verifica_e3_e5.py, rodado com C:\Python314\python.exe -B -X utf8: toy de 16 estados, sem rede, sem modelo, sem Lean e sem dado observado
- Varredura por grep de consciência, pesos, exclusividade, «nomeia» e «é o leitor»: só negações

