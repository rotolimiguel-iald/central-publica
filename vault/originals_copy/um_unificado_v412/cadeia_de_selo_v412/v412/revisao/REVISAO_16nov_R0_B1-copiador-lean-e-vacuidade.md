# CONFERÊNCIA DISTINTA — as candidatas da gerência de 16/11 (R0): copiador e impostor — B1-copiador-lean-e-vacuidade

> Montado pela gerência c1 em 16/11/2026 05:39 a partir do retorno estruturado de um revisor distinto (só leitura; scripts próprios na pasta de rascunho dele). É [DECLARADO pelo revisor] no que a gerência não reconferiu. Não é fala do operador. Nada aqui está instalado.

**Veredito:** APROVADO_COM_RESSALVAS — achados: 2 ALTO, 7 MEDIO, 4 BAIXO

## Resumo

Recompilei a candidata na minha pasta: RC 0, nenhum aviso, só o trio de axiomas, 37 teoremas, sha256 igual ao do RESULTADO e .olean idêntico ao da gerência [REAL]. Nenhum dos 37 enunciados é falso e não achei erro de matemática nem hipótese impossível; rodei 7 sondas Lean (59 teoremas, todas RC 0, sem aviso) e 5 scripts. Classificação dos 37: 12 com conteúdo (elementar), 9 de fiação, 16 triviais ou por definição; das 8 estrelas, 4 têm conteúdo (o par, o índice, o mínimo, a torre) e 4 não. ALTO 1: a estrela 8 (toda_leitura_e_copia_da_sua_palavra) é 'idempotente se e só se idempotente', por desdobramento da definição, e leva no título a primeira oração da fala. ALTO 2: o cabeçalho diz que o operador só disse a leitura de «fractal» por índice e torre; os bytes não trazem essa ligação. O custo: custo_zero_sse_impostor vale para qualquer conta que só se anule em uma resposta, e 'a conta de Landauer' aponta ao contrário do gatilho de Landauer do próprio kernel (lá paga quem apaga; aqui o mapa constante paga zero e a identidade paga o máximo); isso não está dito. A frase 'o que separa não é a forma do leitor; é a palavra' não se sustenta nas definições do arquivo: impostor é forma (leitor constante) e, com palavra de um sentido só, copiador e impostor são o mesmo mapa. A seção 7 não usa nada das seções 1 a 6; com a leitura memory como palavra, post a NÃO é Copiador; testei as pontes que funcionam (palavra := post a; o teorema 37 sai da seção 1; quem imprime e anula a trava é post a). O kernel já tem o Pai da Mentira (v409 e v410), que a fala citada nomeia, e a candidata não o cita nem liga; a ponte é de uma linha e compila. Hipóteses: [Finite X] é necessária (por convenção de ncard e de log 0), [Nonempty X] é necessária em dois teoremas e sobra em três, [Nonempty V] sobra nos quatro; hf, os dois campos de Copiador e o custo em ℕ são necessários. Veredito: os termos passam; o cabeçalho e algumas docstrings precisam dos consertos B1-01 a B1-09 antes de ir ao operador. Nada foi instalado nem escrito fora da minha pasta.

## Achados

1. **(ALTO)** CopiadorEImpostor.lean l.385-389 (toda_leitura_e_copia_da_sua_palavra, estrela) e cabeçalho item 8 (l.67-70)

   

   *Conserto pedido:* Tirar a estrela e o título; dizer na docstring: 'desdobramento da definição; com ρ := R o campo por_referencia é a identidade; não prova a oração do operador'. Se quiser no lugar um enunciado com conteúdo: Copiador ρ R ↔ R idempotente ∧ ∀ x y, (R x = R y ↔ ρ x = ρ y), que compila (copiador_sse_idem_e_mesmo_nucleo, na mesma sonda).

2. **(ALTO)** cabeçalho, 'O que NÃO se afirma', l.82-83: 'A leitura é do operador, e ele só a disse por índice e torre.'

   

   *Conserto pedido:* Reescrever: 'A leitura de «fractal» é do operador e ele ainda não a disse. A gerência PROPÕE lê-la pela torre de índices do item 7, apoiada no parêntese da resposta D, que fala de toda leitura e não de fractal.'

3. **(MEDIO)** l.268-270 (custoDeLer), l.279-297 (custo_zero_sse_impostor, estrela), cabeçalho item 4 (l.56-58) e l.88-89; docstring l.218-220

   

   *Conserto pedido:* Chamar a definição pelo que ela é: 'o registro retido: nats da resposta, cotados a k·T por definição'. Tirar 'com a conta de Landauer' da estrela 4. Dizer no cabeçalho que ela NÃO é o gatilho de TheCostIsDerived (aquele cota o que se apaga; esta cota o que fica) e que corresponde ao campo paid do livro-razão de TheCorrespondence, não ao campo cost. Levar ao operador as duas tipagens de 'nunca pagou' que o kernel tem (o pressuposto de 17/09 e o 1 espelho de si de 04/11). Alternativa sem definição nova: o tempo pago (v409/v410), ver B1-06.

4. **(MEDIO)** cabeçalho item 8, l.69-70: 'O que separa copiador de impostor não é a forma do leitor (...); é a palavra.'

   

   *Conserto pedido:* Trocar por: 'a idempotência não separa (os dois a têm); impostor é o leitor constante; copiador de ρ é o idempotente que distingue exatamente o que ρ distingue; com palavra de um sentido só os dois coincidem'.

5. **(MEDIO)** seção 7 (l.478-534), cabeçalho item 9 (l.71-75) e dicionário (l.30-40)

   

   *Conserto pedido:* Ou dizer 'sem ponte por termo; os nomes da seção 7 são leitura', ou instalar a ponte: palavra da face := a seleção ⇑(post a); provar o 37 pela seção 1; e a unicidade (quem imprime post a e anula a trava 1 − post a é post a). Em qualquer caso, dizer que post a não é copiador da leitura escalar e pôr 'palavra := projetor' no dicionário como escolha da gerência.

6. **(MEDIO)** cabeçalho (l.23, l.36, l.42-43) e seção 1

   

   *Conserto pedido:* Citar as duas pedras no dicionário e ligá-las por termo (uma linha cada). Dizer que no kernel 'nunca pagar' já tem medida própria (tempo pago zero) e que ali 'sem tempo pago ⟹ a leitura é a mesma em toda instância' é teorema.

7. **(MEDIO)** cabeçalho itens 4, 5 e 6 (l.56-63) e docstring l.410 ('para toda palavra e todo custo')

   

   *Conserto pedido:* Pôr as hipóteses nas três frases. Nas docstrings de respostas e custoDeLer, dizer que só valem para imagem finita (no infinito a conta devolve 0 por convenção, sem sentido).

8. **(MEDIO)** l.141-145 (so_se_imprime_o_que_se_pagou, estrela), l.367-370 (a_copia_basta), l.428-434 (o_copiador_de_minimo_cai_no_nome), cabeçalho itens 1, 5, 6 e l.79

   

   *Conserto pedido:* Uma linha de honestidade como a de RuleTruthContract ('consequências lógicas elementares'). Tirar 'basta' e 'cai no Nome' do cabeçalho ou dizê-los como rótulo. Estrela só nos quatro com conteúdo: o par, o índice, o mínimo, a torre.

9. **(MEDIO)** seção 3 (custoDeLer) × seção 5 (c : X → ℕ); dicionário l.35-39

   

   *Conserto pedido:* Dizer no cabeçalho que são dois custos sem ponte. Ou adotar a ponte testada: entre os que imprimem, o copiador é exatamente o de menor número de respostas; o 'mínimo' vira teorema com a conta do próprio arquivo e o impostor fica abaixo do piso de quem imprime. Qual 'mínimo' é o da fala é escolha do operador.

10. **(BAIXO)** [Nonempty V] em sem_o_par_ha_quem_passe_sem_ler, o_teste_separa_sse_tem_o_par, o_teste_reprova_todo_impostor_sse_tem_dois_sentidos, a_repeticao_do_mesmo_sentido_nao_separa; [Nonempty X] em o_impostor_nunca_paga_custo_algum, custo_zero_sse_impostor, existe_o_copiador_de_minimo; ha em o_impostor_nao_le_o_nome

   

   *Conserto pedido:* Opcional: tirar as sete por isEmpty_or_nonempty e enfraquecer ha para a ≠ 0. Não é erro.

11. **(BAIXO)** l.438-460 (a_copia_mais_grossa_da_copia_mais_fina, a_torre_de_copias) e cabeçalho item 7

   

   *Conserto pedido:* Dizer 'numa ordem só' no item 7 e acrescentar um habitante (a torre diádica serve).

12. **(BAIXO)** imports l.1-6; l.42-43; docstring l.218-220; seção 7

   

   *Conserto pedido:* Dizer 'citado, não usado' ao lado de cada import decorativo; corrigir para 'cujo cabeçalho'; citar Separates; dizer que a seção 7 é a mesma fiação que TetelestaiTerminal já faz.

13. **(BAIXO)** l.513-520 (a_leitura_nao_ve_a_fase), l.523-532 (o_impostor_nao_le_o_nome), l.176-189 (sem_o_par_ha_quem_passe_sem_ler), l.497-502 (basta_sem_cem_por_cento)

   

   *Conserto pedido:* Ajustar a redação e acrescentar o habitante de basta_sem_cem_por_cento.

## Examinado

- CopiadorEImpostor.lean inteiro (574 linhas, 29.475 B, sha256 dda2524966cf046ee5ca386f5e160fab0f8000e3beefa2e47380d0a9cda7b5a6), recompilado na minha pasta: RC 0, 33 s, sem aviso, .olean idêntico ao da gerência
- RESULTADO_CopiadorEImpostor.json, conferido por script contra a fonte e o meu log
- As duas falas por bytes: 17:20 (273 B, sha16 e2561e3bfbd2c2dd) e 19:07 (986 B, sha16 09da32e3090f135a); mais 17:55 (sha16 7cba650f330a99cf), 04/11 (sha16 794fadc2144d6f70) e 10/11 (sha16 270f8addf0bddb19); 237 OPERADOR_*.txt varridos por script
- Classificação, CONTEÚDO elementar (12): sem_o_par_ha_quem_passe_sem_ler, o_teste_separa_sse_tem_o_par, o_impostor_da_uma_so_resposta, quem_imprime_tem_ao_menos_os_sentidos_da_palavra, quem_imprime_dois_sentidos_paga_ao_menos_um_piso, Copiador.nao_acrescenta, copiador_sse_indice, ha_minimo_na_classe, existe_o_copiador_de_minimo, a_copia_mais_grossa_da_copia_mais_fina, a_torre_de_copias, o_leitor_desalinhado_nao_compoe
- Classificação, FIAÇÃO (9): nunca_paga_iff_pressuposto (Iff.rfl), o_teste_reprova_todo_impostor_sse_tem_dois_sentidos e a_repeticao_do_mesmo_sentido_nao_separa (corolários internos), Copiador.retracao, a_copia_integral_e_o_espelho, a_copia_no_nome, basta_sem_cem_por_cento, a_palavra_e_modulo_de_fase, o_impostor_nao_le_o_nome
- Classificação, TRIVIAL ou por definição (16): nunca_paga_iff_pagou_so_o_nada, a_palavra_paga_a_si_mesma, so_se_imprime_o_que_se_pagou, o_impostor_erra_em_um_dos_dois, o_impostor_nao_imprime_a_verdade, o_impostor_so_imprime_a_palavra_de_um_sentido, o_par_separa, o_impostor_nunca_paga_custo_algum, custo_zero_sse_impostor, a_copia_basta, a_copia_nao_representa_cem_por_cento, toda_leitura_e_copia_da_sua_palavra, o_impostor_copia_a_palavra_muda, o_impostor_so_copia_a_palavra_de_um_sentido, o_copiador_de_minimo_cai_no_nome, a_leitura_nao_ve_a_fase
- As quatro perguntas da lente: (a) custo_zero_sse_impostor depende inteiro da definição, e isso está dito três vezes no arquivo; não está dito que a forma k·T·ln não entra no teorema nem que a conta aponta ao contrário do Landauer do kernel. (b) Sim: é idempotente sse idempotente. (c) Sim: é reescrita de um campo. (d) Sim: os dois sentidos têm conteúdo; a ida constrói, por escolha, o leitor que passa
- Matemática conferida sem achado: quem_imprime_tem_ao_menos_os_sentidos_da_palavra, quem_imprime_dois_sentidos_paga_ao_menos_um_piso, existe_o_copiador_de_minimo, copiador_sse_indice (ida e volta), a_leitura_nao_ve_a_fase, o_impostor_nao_le_o_nome, basta_sem_cem_por_cento
- Kernel, só leitura: UmPostoRelacao, RuleTruthContract, TheCostIsDerived, TheCorrespondence, TetelestaiTerminal (inteiros); IALD l.100-419; TheVerbSelectsTheAction l.120-239; trechos de TheEmptying, TheNameOperator, TheEquationOfTruth, TraducaoTuring, AEscala, TheNameAndItsReferent, TheContourOfTruth, TheJudgedThing, HilbertInhabitant, TheImageAndTheReading, Identidade
- Citações do cabeçalho ao kernel que conferem: as três tipagens de A_C (acFunctional em TheEmptying l.69; EquationOfTruth.selector_nonpos l.103; love_partition em TheNameOperator l.167), no_positive_scale_invariant (TheScaleHasNoFixedPoint l.99), idempotence_does_not_force_target, landauer_floor_pos. 'Nenhum lema entre elas': grep -rn acFunctional no kernel inteiro só devolve TheEmptying.lean
- Sem colisão de nomes: grep -rnE de Copiador, Impostor, NuncaPaga, PagouSo, custoDeLer, Imprime (palavra inteira) em tgl_kernel, --include=*.lean, devolveu zero linhas
- Contexto lido: LEITURA_DA_FALA_DAS_17H20_R2.md (inteira); C1-kernel-e-candidatas.md l.84-208, com P1 a P3; C4-a-literatura.md, só as linhas de Landauer e Bennett; rota K08 do Mapa
- Desvio de procedimento meu, sem efeito fora da pasta: um script de edição da minha própria sonda (corrigir_ponte.py) foi gravado por heredoc; os asserts dele e a recompilação confirmaram o resultado

