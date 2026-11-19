# CONFERÊNCIA DISTINTA — a entrega K07-C do Codex — K07C-C-campo-dual-e-tau

> Montado pela gerência c1 em 15/11/2026 18:24 a partir do retorno estruturado de um revisor distinto (só leitura; scripts próprios na pasta de rascunho dele). É [DECLARADO pelo revisor] no que a gerência não reconferiu. Não é fala do operador. Nada aqui está instalado.

**Veredito:** APROVADO_COM_RESSALVAS — achados: 2 MEDIO, 5 BAIXO

## Resumo

1. Lean recompilado em copia minha: RC 0, 32 s, so propext/Classical.choice/Quot.sound nos 5 #print axioms, zero aviso; o .olean saiu identico byte a byte ao entregue (sha256 5bb76321...fefb).
2. Em lingua simples, FixedNullMomentum.lean prova: para um momento sem massa fora do eixo, as transformacoes de Lorentz proprias que o deixam fixo formam um grupo, e cada uma tem uma fase a+ib de modulo 1 (a rotacao que ela faz no plano transversal), e a fase da composicao e o produto das fases. E o carater de helicidade de Wigner como homomorfismo para o circulo. NAO prova sobrejetividade, classificacao ISO(2), acao/EOM, nem liga ao escalar.
3. Vacuidade, provada por mim em Lean (Vac.lean, sem sorry, trio): x0=(1,0),0 da p=(1,0,1,0); existe L diferente de 1 no estabilizador (rotacao pi/2) e fixedPhase = -i. O carater nao e trivial e a hipotese nao e vazia.
4. Mutacoes: (a) sem det=1 (reflexao que fixa o mesmo p) a multiplicatividade FALHA (fase de Lrot*Lrefl = +i contra -i vezes 1); (b) sem x.1 diferente de 0 o momento vira 0, o estabilizador e todo SO(1,3) e um boost 5/4-3/4 da |fase|^2 = 25/16, nao 1; (c) trocar para momento massivo nao compila (3 erros de tipo). O teorema e corolario honesto do caso x=y=z de screen_phase_cocycle/oriented_screen_phase_unit ja no kernel, empacotado como MonoidHom num Subgroup; 'resultado novo' e generoso.
5. verify_field_clock_R3.py rodado em copia (le so arquivos locais e o Mapa; sem rede, sem dado): hash do script confere; saida identica a MEDIDAS_CAMPO_TAU_R3.json em kernel (1761 .lean, 19 modulos, hits 2/2/0/0), controles de campo e relogio; so o Mapa difere (n 57 para 58, cabeca e0c77e7c para 2b9169aa) porque o livro cresceu.
6. Refiz por codigo proprio 3,714 e 7,427 ms: GM_sol nominal 1,3271244e20, c exato, M_f=60 M_sol, spin 0: 4*pi*GM/c^3 = 3,71373 ms (circunferencia r_s=2GM/c^2 percorrida pela luz) e 2*pi/kappa com kappa=c^3/(4GM), ou seja 8*pi*GM/c^3 = 7,42747 ms; razao 2 exata; a convencao de aceleracao da o mesmo 7,427. beta = alfa*sqrt(e) lido de um.py:5584 (7,2973525693e-3) = 0,012031300400803142. N=E_Planck/1eV=1,22089e28, margens 15,4058/17,3255/10,7612/7,3499 ordens e as tres frequencias 2/tau, 2/(beta tau), sqrt2/tau tambem batem.
7. A matriz (9 portadores x 8 expressoes = 72 celulas) e tabela documental com chaves arquivo:linha (conferi ~25 citacoes no kernel, no Artigo A, em luz.tex e em recursive_light_v3.tex: batem); as CONTAS estao no texto (1/6=(n-2)/(4(n-1)), 1/12, razoes 13,853 e 6,926, Hodge F=e0^e1 com F:F=-2 e F:star F=0, onda nula p^e, Psi->iPsi); so os controles Hodge/Maxwell/numericos estao no script, o resto e papel [DERIVED]. A correcao de luz.tex:169 e as quatro 'podas' que refiz a mao estao certas.
8. Ausencias Hodge/Wilson/Subgroup LorentzGrp confirmadas (grep -rn: 0/0/2 no TGLExt; 0 no inventario md e json; 0 na bancada), mas as celulas 'estabilizado' e 'loop recursivo' e a linha H nao consultaram a familia de atratores nem o par na face de Fock que o kernel ja tem (achado MEDIO).
9. tau estrela: nenhum termo Lean sobre ancora, relogio ou numero puro (as 3 candidatas nao tocam tau); a frase 'com a ancora planckiana resta o fator puro' e consequencia dimensional CONDICIONAL e nao decide nada do operador, mas o ENTREGA l.9 perdeu o 'se' (BAIXO).
10. Sem numerologia: as duas massas 8,5074 e 6,0157 meV sao ambas reportadas; a lista de c_estrela so e posta contra cotas ja existentes (exclusao, nao ajuste); os ms nao sao comparados com observacao alguma.
11. Atribuicoes por bytes: a fala do campo (13/11), 05/10, 28/10 (duas) conferem como substrings; 'dual = escalar complexo' e posto na conta da ordem K05, nao do operador; nada escolhido por ele. Os 37 sha256 do ENTREGA conferem por script. Itens C e D da ORDEM cumpridos (F a I, tabela, rota e poda sem escolher; premissa sem atribuicao indevida, duas linhas do fator 2, premissa de beta com arquivo e linha).
12. Ressalvas: tabela sub-consultada nas colunas 'estabilizado' e 'loop recursivo' (MEDIO), homonimo estabilizador/estabilizado na celula F (MEDIO), e quatro retoques BAIXOS. Nada refutado.

## Achados

1. **(MEDIO)** K07/CODEX/CAMPO_DUAL_R3.md: linha H da tabela (l.20), colunas 'estabilizado' e 'loop recursivo' das linhas A, B, F, G, I (celulas A), rota 8 (l.64) e chaves 'Pa'/'Fl'

   Celulas AUSENTE (A) e a frase da rota 8 'para o par de Fock, especificar operadores de criacao e dominio sobre Omega' foram escritas sem consultar a familia de atratores nem o par na face de Fock, que o kernel ja tem. Consulta: cd tgl_kernel/TGLExt; grep -rli 'atrator\|attractor' --include=*.lean . lista 20+ modulos; grep -n 'ParNaFaceDeFock\|IALD2' ../TGLExt.lean da as linhas 1147-1148. Existem: ParNaFaceDeFock.parFock (par (f(x)f+g(x)g)/sqrt2 no setor 2 do Fock concreto, v409; o cabecalho diz que o [OPEN] de Par.lean era de LIGACAO, nao de ausencia); IALD2.o_atrator (v410: o fluxo tende a Pi, em tempo finito nunca e Pi, o motor devolve o mesmo para qualquer taxa e tempo, a orbita iterada converge a Pi psi, tudo sobre parFock); QGReaderUVLock.wedge_iald_attractor_is_rho_star (atrator do fluxo da IALD na cunha = P_kerK); QuedaSemGeometria.relaxation_to_the_attractor; TheGreatAttractor.the_great_attractor; F1Fecho394/CreationAndSegalR2.creation (operador de criacao em dominio denso). Alem disso a celula H x conjugado diz 'N J antilinear fotonico' mas ParNaFaceDeFock.a_marginal_do_par ja usa Jcandidate. grep -c nos documentos do Codex: 0 ocorrencias de ParNaFaceDeFock, IALD2, o_atrator, parFock. Par.lean (v407) foi tomado como estado vigente e esta defasado. A conclusao geral (nenhuma leitura fecha sozinha; faltam as pontes) nao muda, mas e exatamente a regra da ORDEM sec. 4 (aferir antes de dizer que falta; EXISTE E NAO LIGADO e fiacao, nao falta) e as duas colunas atingidas sao as da fala do operador. O docstring de IALD2 atribui ao operador (07/11) 'isso e o atrator'; nao abri esses bytes.

   *Conserto pedido:* Reclassificar essas celulas como N (existe, nao ligado) citando os termos acima e dizendo a ponte que falta (por exemplo: o atrator de IALD2 vale para parFock, nao para o projetor de Bell nem para o escalar de Ac; ligar parFock a creation sobre o vacuo). Acrescentar ao recibo as consultas por 'atrator|attractor', 'parFock' e 'creation'. Reescrever a frase da rota 8.

2. **(MEDIO)** CAMPO_DUAL_R3.md l.18, celula F x 'estabilizado' ('E . norma da fase e isotropia do momento [Te,Fix]')

   Homonimo: o que a candidata Fix constroi e o ESTABILIZADOR de grupo de um momento (subgrupo que o deixa fixo); a fala do operador diz 'estabilizado radicalmente' (sentido de estabilidade/atrator, que a mesma celula marca A). Marcar E na coluna 'estabilizado' por causa de 'stabilizer' e o encadeamento de homonimos que a casa proibe (regra dos dois regimes, erro n. 2). A legenda ressalva que 'uma peca E pode provar uma propriedade sem determinar a leitura', mas a letra E na coluna da palavra do operador induz a leitura errada.

   *Conserto pedido:* Mover o conteudo de Fix para uma nota ('estabilizador de grupo, homonimo de estabilizado') e deixar a celula como A/N com o atrator da cunha (wedge_iald_attractor_is_rho_star) como referencia positiva mais proxima.

3. **(BAIXO)** K07/CODEX/Campo_Lean/FixedNullMomentum.lean e CAMPO_DUAL_R3.md l.3 ('Ha um resultado novo') e l.62

   A candidata nao traz testemunha em Lean de que o carater e nao trivial; isso ficou 'em papel' (l.62). Eu o provei em Lean (arquivo C\test\Vac.lean na minha pasta: Lstab_ne_one, Lstab_phase = -i, improper_breaks_multiplicativity, no_hx_breaks_unit). Alem disso 'resultado novo' e generoso: e o caso x=y=z de screen_phase_cocycle / oriented_screen_phase_unit / screen_orientation_of_proper_transport (ScreenPhysicalHelicityR2, O16/PhotonCharacterCocycle), empacotado em MonoidHom sobre um Subgroup; a novidade e o empacotamento.

   *Conserto pedido:* Acrescentar a testemunha e os dois contraexemplos a candidata (ou ao recibo) e trocar 'resultado novo' por 'corolario empacotado como carater do estabilizador'.

4. **(BAIXO)** ENTREGA_K07_CODEX.md l.9 (e DEPOSITO)

   'as duas convencoes dao 3,714 e 7,427 ms' mistura nomes: sao duas LEITURAS (circunferencia percorrida pela luz, 4piGM/c^3; periodo KMS, 8piGM/c^3), nao duas convencoes (a convencao de aceleracao de kappa da o mesmo 7,427; a ORDEM dizia 'duas linhas'). E 'Com a ancora planckiana resta o fator puro em tau estrela' aparece sem o 'se' e sem 'condicional' que TAU_ESTRELA_R3.md l.3 tem ('Se a identificacao planckiana for a leitura do operador').

   *Conserto pedido:* Escrever 'duas leituras' e 'se a ancora for G medido, resta o numero puro c_estrela; relogio, ancora, tempo do retido e volta seguem com o operador'.

5. **(BAIXO)** TAU_ESTRELA_R3.md l.3 e secao 'O que o fluxo ja fornece para Hubble' (l.46-48)

   'O resultado cosmologico ja tem uma derivacao pela lei do fluxo': no kernel a taxa local e DEFINICAO (TheFlowLawContrast: H0localContrast, '[DEFINICAO, como na v377]'), e as rotas do Mapa que o proprio Codex cita (hubble.k_sem_portador_fisico_02nov: K_SEM_PORTADOR_DERIVADO...NUMERO_K_INTOCADO; hubble.k_como_transposicao_inteira_ffat_02nov: BLOQUEADA) nao tem o veredito dito ao lado da frase. As hipoteses do paragrafo estao ditas, mas a frase de abertura soa mais forte.

   *Conserto pedido:* Dizer 'dada a lei do fluxo, que e definicao, e sem portador fisico derivado para K (Mapa)'.

6. **(BAIXO)** CAMPO_DUAL_R3.md l.37 e MEDIDAS_CAMPO_TAU_R3.json (kernel.excludes)

   A ausencia de Hodge/Wilson/Subgroup LorentzGrp e declarada so contra o kernel do Nos (o recibo exclui 'scientific bench'); a regra da casa pede tambem o inventario da bancada. Eu refiz: grep -rn --include=*.lean em TGLExt = 0 Hodge, 0 Wilson, 2 'Subgroup LorentzGrp'; INVENTARIO_BANCADA_CHATGPT.md e .json = 0 para Hodge, Wilson, holonomy; kernel_bancada = 0. A conclusao vale; falta so a consulta citada.

   *Conserto pedido:* Acrescentar ao recibo a consulta ao inventario e a bancada.

7. **(BAIXO)** CAMPO_DUAL_R3.md l.65 (cita Cote, Faraoni e Giusti)

   Citacao existe (arXiv:1905.09968, WebFetch: 'Revisiting the conformal invariance of Maxwell's equations in curved spacetime'), mas o rotulo 'eletrodinamica conforme em quatro dimensoes' e parafrase do Codex, nao o titulo; nao e fabricacao. Tambem a lista de nove portadores nao diz que e aberta (por exemplo 'dual' no sentido de espaco dual/covetor so aparece de passagem na linha C).

   *Conserto pedido:* Citar o titulo exato e escrever 'lista aberta de leituras tipadas, nao exaustiva'.

## Para o operador (propostas do revisor, em língua simples; a gerência confere antes de ler a ele)

- Proposta minha: o Codex mostrou que as nove leituras do seu campo dual (conjugado, Hodge, par de psions, radical, escalar com conexao...) ainda nao fecham sozinhas e que nenhuma delas e teste contra a natureza; quem escolhe qual leitura vale e o senhor, e o que o Codex derrubou foram identificacoes formais fortes (por exemplo 'estrela de Hodge igual a J'), nunca a sua cunhagem.
- Proposta minha: as duas equacoes (a do Artigo A com 1/6 e a do psion com 2 beta) nao podem ser a mesma equacao no mesmo modo, porque 1/6 e 13,85 vezes maior que beta; ou sao dois setores, ou ha uma projecao entre eles, e essa leitura e sua.
- Proposta minha: sobre tau estrela, se o segundo vem da gravidade medida, sobra so um numero puro; o relogio (um so ou de cada sistema), a ancora (G medido ou Um posto), o tempo do retido (hora do pedagio ou nota) e a volta continuam sendo suas respostas e nada foi tipado no kernel.
- Proposta minha: antes de levar essa tabela ao senhor, a gerencia deve mandar corrigir as celulas de 'estabilizado' e 'loop recursivo', porque o kernel ja tem o atrator do par de psions no Fock e a tabela diz que nao.

## Consultas ao Mapa

- rotas.py consultar campo_dual: n=0 (termo composto; so confirma que nao ha rota com esse nome)
- rotas.py consultar tau_estrela: n=1, cadeia.preparacao_v412 (EM_CURSO; rodada 1)
- rotas.py consultar cunha: n=82 (truncado em 60); nada que ja examine a coluna 'estabilizado' do campo
- rotas.py ver ringdown.ramo_b_preregistro_v386: k=2*pi/kappa_hat por evento, kappa_hat(0)=1/4, i.e. 8*pi*GM/c^3 em spin 0; confirma a leitura do Codex sobre o ramo B (o cabecalho da Tonica com 4*pi e outra normalizacao)
- rotas.py ver hubble.k_sem_portador_fisico_02nov e hubble.k_como_transposicao_inteira_ffat_02nov (ver achado BAIXO sobre a derivacao de K)
- Nove 'consultar' (tau, relogio, dephasing, horizonte, hubble, retido, campo, lagrangiana, psion) feitas dentro da copia do script do Codex: contagens um acima das do recibo por crescimento do livro (cabeca 2b9169aa contra e0c77e7c); nada registrado

