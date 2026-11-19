# CONFERÊNCIA DISTINTA — a entrega K07-C do Codex — K07C-B-montagem-e-GH

> Montado pela gerência c1 em 15/11/2026 18:24 a partir do retorno estruturado de um revisor distinto (só leitura; scripts próprios na pasta de rascunho dele). É [DECLARADO pelo revisor] no que a gerência não reconferiu. Não é fala do operador. Nada aqui está instalado.

**Veredito:** APROVADO_COM_RESSALVAS — achados: 2 MEDIO, 6 BAIXO

## Resumo

1. Constante (numpy 4x4 proprio, b1_montagem.py): os 24 termos sgn(pi)*G_pi1 G_pi2 G_pi3 G_pi4 valem todos G1G2G3G4 = -chi; a soma e -24chi; o coeficiente que devolve chi e -1/24. Refiz a cadeia iterada: constantes 2i, 3, 4i, produto -24; a leitura i*3*6i = -18 daria 4chi/3. Confere o Codex.
2. O sinal -1/24 e convencao: com chi=+G1G2G3G4, ou coordenadas 1 e 2 trocadas, o coeficiente vira +1/24. A R3 diz "orientacao de coordenadas escolhida"; o resumo da ENTREGA diz so "a orientacao e -1/24" (achado 4).
3. Realidade em L2 truncado (81 modos x C^4, J antilinear): com a reflexao k->-k, (J^2, JD, Jchi) = (-1,+1,+1) = KO 4; sem a reflexao, (-1,-1,+1). J^2 e Jchi nao dependem da reflexao; so o sinal de JD. O texto esta certo; uma frase mistura as causas (achado 5).
4. GH reconstruido: corte e_i=1_[-i,i](h-chapeu); q_i=e_{i+1}-e_i; Lipschitz L(a)=||[h-chapeu,a]||; estimativa de van Suijlekom Def. 2 (||S_nR_n a - a|| <= eps_n ||a||_1, com ||a||_1=||[D,a]||, lido no texto do arXiv 2005.08544) e Kaad-Kyed Prop. 2.14. Em q_i: norma 1, L=0, R_i(q_i)=0, logo 1 <= gamma*0. Analogo finito (b2_gh.py): ||S(Rq)-q||=1 para S linear qualquer. E no-go de UMA realizacao (observaveis N, D=h-chapeu), nao de GH em III1; o texto nao o vende como mais. "Outra realizacao segue em aberto" e honesto.
5. Mas o negativo era previsivel: vale para todo D afiliado a N e nao escalar, porque as projecoes espectrais de D estao na algebra e comutam com D. O texto diz menos do que prova e nao diz que o teste nao podia dar outro resultado (achado 1, regra do posto).
6. Assinatura: a R3 nao afirma nada novo sobre (1,3); L0 a L11 estao [OPEN]. Tabela KO: n=4 (-,+,+); n=6, o (1,3) na convencao de Bizi-Brouder-Besnard, (+,+,-). A advertencia da R2 sobre isso se perdeu na R3 (achado 7).
7. Literatura lida no primario por mim: Blackadar Cor. III.2.1.10 (Cycr.pdf de 2017, enunciado exato); Haagerup-Junge-Xu arXiv 0806.3635v2 (1.2),(1.4)-(1.6),(1.10)-(1.12) (tau o theta_t = e^-t tau; lambda(t)=D^it), coerentes com tau(e_i)=2 sinh i; van Suijlekom Def. 1-2 e Teo. 5; Haagerup-Musat Lema 2.11; Connes 2008 Teo. 1.1/1.2; Connes 1996 Obs. 4 (afirma, nao prova). Dixmier c_lambda=4 vol(B4)/lambda^4 conferido (razao 0,998); pareamento de K-teoria em T4 tem det +1 nas duas paridades.
8. Candidata das gamas: sha16 41de0a594e4b551c confere; linhas 236, 258, 266, 292, 435 citadas existem; log com so os tres axiomas. O Codex cita como identidade de matrizes, como o adendo B manda. Kernel (grep -rI em TGLExt): SpectralTriple, Gromov, Rieffel, Krein, Dixmier, Hochschild, Clifford = 0 arquivos; confere a errata.
9. Os 37 sha256 da ENTREGA: 0 divergencia (b3_hashes.py); R2 intactos (3eeb6c56, 0f5e367d); o pin do deposito na fila confere com a ENTREGA.
10. Ordem: 3a (seis itens) e 3b cumpridos; errata de montagem incompleta (achado 3). Nenhuma fala atribuida ao operador nas pecas desta lente; nenhuma palavra proibida; sem ALTO. Ressalvas: 2 MEDIO e 6 BAIXO.

## Achados

1. **(MEDIO)** kimi/K07/CODEX/GH_III1_R3.md l.3 e §2 (tabela, ultima linha); ENTREGA_K07_CODEX.md l.7

   O negativo de D=h-chapeu nao podia dar outro resultado e o texto nao o diz. Todo D auto-adjunto afiliado a N e nao escalar tem as projecoes 1_Delta(D) em N, comutando com D: L=0 em elementos nao escalares, e resolvente compacto comum e impossivel num fator difuso (o texto so diz o segundo, e como aparte). Reproduzi isso em dimensao finita: b2_gh.py, ||q||=1, L(q)=0, R(q)=0, ||S(Rq)-q||=1 para S linear qualquer. O texto limita o escopo a esse operador (honesto), mas nao diz que a escolha do operador mais simples fixa o negativo de antemao, nem que a cascata do circulo do artigo (Fecho 3, P_M D P_M com o Dirac do circulo, l.1936-1941) nao e posta a prova aqui. Pela regra do posto, quem le a R3 pode tomar o negativo por parede medida da conjectura.

   *Conserto pedido:* Acrescentar ao paragrafo inicial: 'o negativo vale para todo D afiliado a N com observaveis contendo W*(D); nao toca a conjectura nem o truncamento do circulo do artigo; a conjectura pede D fora de N'. A gerencia le isto ao operador antes de usar a frase.

2. **(MEDIO)** kimi/K07/CODEX/MONTAGEM_3MAIS1_R3.md l.46 (tabela §4, linha L11, ultima frase)

   'A matriz positiva de Gram estabelece a positividade especificada no artigo.' Frase solta, sem estatuto, dentro de uma linha [OPEN]; a matriz nao e definida na R3. No artigo (l.1806-1813, C-5) e M_ij=<a_i Omega, J a_j* Omega> >= 0, positividade modular no vacuo (verdadeira, e igual a ||Delta^(1/4) a Omega||^2), nao positividade de reflexao de Osterwalder-Schrader do produto de circulos. Lida ao lado do pedido de identificar reflexao e espaco reconstruido, pode parecer que fecha parte de L11.

   *Conserto pedido:* Apagar a frase, ou marcar: '[KNOWN, Tomita-Takesaki; artigo C-5] positividade do Gram modular; nao e a positividade de reflexao do produto, que continua [OPEN]'.

3. **(BAIXO)** kimi/K07/CODEX/ERRATA_MONTAGEM_GH_CODEX_R3.md l.7 (item 1) e ERRATA_MONTAGEM_GH_K07_CODEX.md

   A errata corrige so R2 §3.3 l.87-91. A ressalva 1 da revisao K05 lista tambem R2 §0 l.5, e a mesma 'orientacao identificada' esta em R2 §4 (tabela, l.104) e em ENTREGA_K05.md l.5 (conferido por grep). O diagnostico da revisao (D-D (36) conta nu_n termos, nao C(n1+n2,n1)) tambem nao aparece; a R3 diz so 'a leitura de (35)-(36) que levou a i,3,6i' (prudente, mas nao fecha a causa).

   *Conserto pedido:* Listar na errata os quatro pontos que dependem da constante; manter a frase neutra sobre D-D, dizendo que a causa nao foi conferida no artigo publicado.

4. **(BAIXO)** ENTREGA_K07_CODEX.md l.6; MONTAGEM_3MAIS1_R3.md §2

   'A orientacao e -1/24' sem o qualificador: o sinal depende de chi=-G1G2G3G4=1 x tau3 e da ordem das coordenadas (script: +1/24 com chi=+G1G2G3G4 ou com coordenadas 1 e 2 trocadas); a magnitude 1/24 nao depende. A R3 nomeia so metade da convencao.

   *Conserto pedido:* Escrever '-1/24, com chi=-G1G2G3G4=1 x tau3 e coordenadas na ordem 1234; a orientacao oposta da +1/24'.

5. **(BAIXO)** MONTAGEM_3MAIS1_R3.md l.13 (ultima frase do bloco [DERIVED, em L2])

   'A reflexao ... fornece o segundo sinal -1. Assim J^2=-1, JD=DJ e J chi=chi J.' J^2=-1 (C conj C=-1) e J chi=chi J saem da parte matricial; a reflexao so entra no sinal de JD. Numericamente: com e sem reflexao J^2=-1 e Jchi=+; so JD muda de sinal. Nao e erro de conta; a redacao junta tres sinais sob uma causa.

   *Conserto pedido:* Separar: 'J^2=-1 e J chi=chi J pelas matrizes; JD=DJ pelo produto (-1)(-1), este segundo -1 da reflexao k->-k'.

6. **(BAIXO)** MONTAGEM_3MAIS1_R3.md l.33 (§3, K-homologia e Poincare)

   O que se deriva e o pareamento perfeito em K-teoria complexa (conferi: det +1 em Lambda^par e Lambda^impar de Z^4). O axioma 6' de Connes e em KR; a versao real fica no 'enunciado geometrico conhecido'. O bloco inteiro leva [KNOWN + DERIVED] sem dizer qual metade e qual.

   *Conserto pedido:* Marcar: 'complexo: derivado; KR (axioma 6'): citado, nao derivado'.

7. **(BAIXO)** MONTAGEM_3MAIS1_R3.md §4 (texto de abertura da tabela) frente a MONTAGEM_3MAIS1_R2.md §6.3

   A R2 §6.3 dizia que KO 4 euclidiano nao vira assinatura lorentziana e que (1,3)<->(m,n)=(4,6) nao prova os axiomas restantes. A R3 perdeu essa advertencia. Pela tabela KO o (4,0) e (-,+,+) e o (1,3), com n=6, e (+,+,-); as tabelas de sinais diferem. A R3 nao afirma nada novo sobre a lorentziana (L0 a L11 [OPEN]); so falta a guarda.

   *Conserto pedido:* Restaurar uma frase: 'os sinais KO 4 do toro nao se transportam a (1,3), que e KO 6 na convencao de Bizi-Brouder-Besnard'.

8. **(BAIXO)** ENTREGA_K07_CODEX.md; FONTES_K07_R3.json

   A entrega pina por hash os documentos da casa, mas nao diz, fonte a fonte, o que foi lido no primario e o que so por resumo. Os textos admitem Gracia-Bondia-Varilly-Figueroa 'so pelo sumario' e Blackadar 'na versao do autor' (este eu confirmei). Para Dabrowski-Dossena, Bizi-Brouder-Besnard, van den Dungen e Connes-Moscovici a R3 herda a leitura da revisao K05 sem dizer.

   *Conserto pedido:* Acrescentar uma tabela 'lido no primario / so resumo / herdado da revisao K05' por fonte.

## Para o operador (propostas do revisor, em língua simples; a gerência confere antes de ler a ele)

- O teste com o proprio gerador da cunha (h-chapeu) so podia dar negativo: esse operador comuta com os cortes que se fazem com ele, entao qualquer volta ao sistema inteiro falha. Isso nao derruba a conjectura de Gromov e Hausdorff em III1; so diz que esse operador, o mais simples, nao serve.
- Proponho que o texto diga isso numa frase antes de qualquer uso, e que a escolha de qual outro operador tentar fique como pergunta ao senhor, nao como decisao nossa.
- A montagem de quatro circulos no toro de quatro dimensoes ficou conferida por conta numerica independente (constante 1/24, sinais de realidade). O sinal de menos da constante e convencao de orientacao; a gerencia deve dize-lo ao senhor.
- Sobre a lorentziana (1,3) a entrega nao afirma nada novo: continua hipotese, com onze itens listados.

## Consultas ao Mapa

- rotas.py consultar montagem -> 16 rotas; so a relevante: formal.k05_t1_montagem_gh_tau_campo_v412
- rotas.py consultar Gromov -> 1 rota, a mesma
- rotas.py consultar Hausdorff -> 1 rota, a mesma
- rotas.py consultar gamas -> kernel.montagem_das_gamas_candidata_15nov (candidata da gerencia) e hubble.fase9_razao_discriminante (sem relacao)
- rotas.py consultar Rieffel, Dossena, Krein -> 0 rotas; Tomiyama -> 1 rota (kernel.o_habitante_do_nome_candidata_15nov, sem relacao com a lente)
- Kernel, grep -rI recursivo em Nos/tgl_kernel/TGLExt (inclui F1Fecho394): SpectralTriple, TriplaEspectral, LipNorm, QuantumGromovHausdorff, operatorSystemTriple, Gromov, Rieffel, Krein, Dixmier, Hochschild, Clifford, KO.dim, MontagemDasGamas -> 0 arquivos cada

## Examinado

- K07/CODEX/MONTAGEM_3MAIS1_R3.md, GH_III1_R3.md, ERRATA_MONTAGEM_GH_CODEX_R3.md, REVISAO_INDEPENDENTE_R3.md, LEITURA_DO_TUNEL_R3.md, DEPOSITO_K07_CODEX.md, conferir_entrega.py (lido, nao executado); ENTREGA_K07_CODEX.md, ERRATA_MONTAGEM_GH_K07_CODEX.md, REGISTRO_MAPA_K07_CODEX.json, PERGUNTA_K07_CODEX.md (parcial)
- ORDEM_K07_CODEX_ASTRA_15nov.md, ORDEM_K07_matematica_rodada_3.md, ADENDO B; MONTAGEM_3MAIS1_R2.md, GH_III1_R2.md; revisao/REVISAO_K05_MONTAGEM_GH.md; candidatas_c1/MontagemDasGamas.lean e revisao/REVISAO_CANDIDATA_MONTAGEM_DAS_GAMAS.md (nao recompilei: o log existente tem os tres axiomas; sha16 conferido)
- Scripts proprios na pasta de rascunho scratchpad/v412_k07_codex/B: b1_montagem.py (gamas, 24 permutacoes, cadeia iterada, J com e sem reflexao em L2 truncado, tabela KO), b2_gh.py (analogo finito do no-go e contraste do circulo, so monomios), b3_hashes.py (37 sha256), b4_kunneth.py (pareamento em T4), b5_dixmier.py (constante de Dixmier)
- Literatura no primario: Blackadar Cycr.pdf (2017), Haagerup-Junge-Xu 0806.3635v2, e copias locais da revisao K05 de van Suijlekom 2005.08544, Haagerup-Musat 0706.3463, Connes 0810.2088, Connes 1996 hep-th/9603053, Connes-Moscovici math/0609703; fila de memoria: deposito k07 so no cabecalho e no pin
- Nao li nem toquei a pasta TIPO_III1_VINCULO; nao rodei modelo, nao abri dado observacional; nada fora da pasta de rascunho foi escrito

