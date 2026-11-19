# CONFERÊNCIA DISTINTA — K09: Hubble, a combinação e as ressalvas

> Montado pela gerência c1 em 15/11/2026 16:53 a partir do retorno estruturado de um revisor distinto (modelo Sonnet; só leitura; scripts próprios na pasta de rascunho dele). É [DECLARADO pelo revisor] no que a gerência não reconferiu. As frases da seção “Para o operador” são propostas do revisor, não fala do operador, e só vão a ele depois de lidas pela gerência. Nada aqui está instalado, congelado ou aberto.

**Veredito:** APROVADO_COM_RESSALVAS — achados: 1 ALTO, 6 MEDIO, 7 BAIXO

## Resumo

1. Todas as contas do meu foco reproduzem por script meu (contas_k09c.py): Stouffer de pesos iguais sigma_J<=0,024145 / 2.162 dias vivos / poder 90,5 %; pesos proporcionais a D 0,0264169 / 1.806 d / 96,4 %; JUNO sozinho 0,023942 / 2.199 d; SN II EPM 3,256 e 2,319 (sys=stat); H0DN 7,068/8,068; as 26 linhas da tabela de D; empilhamento 4,04/3,36/5,34/4,88; ringdown 25,487/25,687 eventos, saturacao 5,805, taxas O4b 16,2 e 11,2/ano, 8,7 e 16,6 meses; Fase 7 (-3,22 -> -1,66 -> -1,54; lnB 5,35 -> 1,62 -> 1,46) confere no Mapa (seq 247, 257, 258).
2. Aplicado: a palavra "morta" saiu; as nove rotas entraram com rota e seq corretos (conferi todas por rotas.py ver); D da casa (6,710/5,191) vem antes do de bolso (exceto uma celula de tabela); DESI DR3 respondido; Stouffer, 2034, O4b, viés 0,0686, P7 bloqueada, R5 por linha (reproduz 6,6571/6,3109/0,104/6,6886 com um unico parametro), R3/R4 com particao e duas bases, F2b.
3. Nada foi aberto: scripts do Kimi so leem JSON/Mapa/core selado e nomes em factors.json; nenhum npz; H0DN nao reaberto; o hash do Mapa no manifesto do censo (558d49b9...) reproduz como prefixo das primeiras 2066 linhas.
4. Bytes do operador abertos por mim e conferidos por sha256: 29/10 (47 B, 9e54b477...), 03/11 (1091 B, 73466598...), 28/10 calibrar (1091 B, 56703faa...) e 28/10 pedagio (587 B, 597fff4a...): as citacoes sao literais e o core (f2b_errata_v404) confirma que a retirada do par F2b e conclusao da gerencia.
5. ALTO (1): o "poder previo 2,33 sigma" esta colado na lei da face PENDENTE; pela fonte (Perguntas:119; V1.4 linhas 26 e 55) e o poder da cobranca F1 ja lida (-1,66 sigma), nao da lei do lado transmitido, que nem foi escrita. Entraria permanente no Mapa (REGISTRO).
6. MEDIO: "16 rotas Hubble" nao e teto (e contagem por prefixo; ha pelo menos 5 rotas fora do prefixo que a propria tabela do Kimi lista); combinacao dada sem o piso s0 que a mesma entrega usa no m2 (com o piso, lambda maximo 3,90 nas duas regras); achado C3 da K04 (poder = chance de 5 sigma contra o pacote; fiduciais assimetricos; tres rotas do Mapa) nao aplicado; particao 3+9/92 e o p do R7 sao escolhas que podem produzir o negativo e estao entregues a "gerencia", nao lidas ao operador; R7 ainda listado como "resolvido"; portao D90 vs 5,0 (fala dele: "poder preditivo acima de 5 sigma") nao mostrado ao lado no ringdown e na combinacao.
7. BAIXO: varias redacoes (combinacao "nao antecipa nada", "ratificada pelo operador" no REGISTRO, DESI "adotado", "conferencias distintas", celula invertida, 0,022 vs 0,023, pinos).
8. REGISTRO e DEPOSITO: sem a raiz confirm, sem aspas angulares; _valida (copia) passa com 13 artefatos; nomes nao reservados. Antes de registrar, consertar o ALTO 1 (o livro e so-acrescimo).

## Achados

1. **(ALTO)** HUBBLE_JA_EXAMINADO_K04.md:8, :42, :250; ERRATA_HUBBLE_K09.md:13; ENTREGA_K09.md:3 e :14; REGISTRO_MAPA_K09.json:5; INSUMOS_PARA_A_PERGUNTA_K09.md:7 (F1); K04\HUBBLE\K09\NOTAS_ROTAS_PONTES_K09.md (secao 3, 3o marcador, e linha da rota bancada.preregistro); NOTAS_EMPILHAMENTO_DESI_K09.md secao 3. Fonte: C:\IALD\Central de Patentes\work\v381_perguntas\PERGUNTAS_QUE_FALTAM_QUATRO_LINGUAS_20261002.md:119 e C:\IALD\Bancada_Um\investigacao\preregistro_dois_lados_02out\PREREGISTRO_DOIS_LADOS_DELTA_K_20261002_V1_4.md:26 e :55.

   O "poder previo 2,33 sigma" e atribuido a "lei da face dos cronometros PENDENTE". Pela fonte, 2,33 sigma e o poder previo da cobranca F1 (fundo nu contra a lei D1b nos cronometros, fase7.poder_previo.moresco2020), que JA foi lida na Fase 7 (-1,66 sigma): pela regua da Fase 4 (>1 sigma) tem poder, pela da Fase 6 (<5) e UNDERPOWERED. A lei do lado transmitido (1-beta por travessia) esta PENDENTE, nao escrita, sem cobranca e com o poder "a dizer antes de abrir"; nada se sabe do poder dela. Nos registros seq 282 e 291 que o Kimi cita nao ha 2,33 (conferi o ver da rota; a V1.4, seq 290, e que traz o numero). A frase "nao ha teste de 5 sigma nesse canal" tambem fica sem lastro para a lei pendente. O erro vem da ordem/revisao da gerencia (aparece no seq 2063), mas o Kimi o replicou em varias superficies e o REGISTRO o poria permanentemente no livro so-acrescimo. A conclusao do topo (parede) nao muda.

   *Conserto pedido:* Separar em duas frases: (a) "a leitura intermediaria (lei D1b nos cronometros, F1) foi lida na Fase 7: -1,66 sigma (Moresco 2020) e -1,54 (todos); poder previo dessa leitura 2,33 sigma (V1.4, fase7.poder_previo.moresco2020), abaixo de 5"; (b) "a lei do lado transmitido (1-beta por travessia) esta pendente: nao escrita, sem cobranca, sem poder dito". Citar seq 290 (V1.4) alem de 282. Corrigir a frase antes do REGISTRO; a gerencia deve por errata ao lado do seq 2063, que traz a mesma mistura.

2. **(MEDIO)** ERRATA_COMBINACAO_K09.md:55; RESSALVAS_UMA_A_UMA_K04.md (bloco K09 de R7, item 2, ~l.301); ENTREGA_K09.md:28; K04\COMBINACAO\K09\CENSO_R7_MAPA_K09.json (campos rotas_hubble e filtro_hubble) e mapear_metadados_k09.py (filtro startswith d1./hubble. ou h0dn).

   "16 rotas Hubble" e chamado de TETO, mas e uma contagem por prefixo de nome (d1., hubble., h0dn). Reproduzi: 2.062 registros, 505 rotas, 285 registros e 123 rotas que olharam dado, 16 por prefixo; porem ha pelo menos 5 rotas FORA do prefixo, com olhou_dados=true, que a propria tabela do Kimi lista como leituras de Hubble (linhas 1, 8, 10, 11, 25): supernovas.pantheon_errata_cosmologica, um_py.v378.o_que_faltou_contraste_fase4, discriminante.ordem018.f1b.fase45_conjunta, discriminante.ordem018.f2.r_d, um_py.v380.fases_5_6_7_por_hash (18 rotas fora do prefixo citam termos de Hubble/H0). Logo 16 nao limita nada; so 123 e teto. Uma diluicao feita com 16 seria branda demais.

   *Conserto pedido:* Dizer "16 = contagem pelo prefixo d1./hubble./h0dn; ha rotas de Hubble fora do prefixo; o unico teto e 123", ou trocar o filtro por lista documentada de rotas de Hubble; manter "nao e N independente".

3. **(MEDIO)** ENTREGA_K09.md:8 (versus :3); REGISTRO_MAPA_K09.json:5; COMBINACAO_K04.md:122-125, :170-178, :277; INSUMOS_PARA_A_PERGUNTA_K09.md F5 e F12.

   As datas e poderes da combinacao (2.162 e 1.806 dias vivos; 90,5 % e 96,4 %) sao "sem piso", mas a MESMA entrega afirma no m2 que com o piso s0 = 0,052588 (ajuste de dois pontos, 59,1 d e 207,2 d; varia 0,047 a 0,058 com o arredondamento dos sigma) 5 sigma e D90 sao inalcancaveis. Por script meu, com esse piso D_J <= 2,86 e o lambda maximo e 3,90 nas duas regras de pesos: a combinacao tambem fica inalcancavel. O ENTREGA e o REGISTRO dao os 2.162 d/90,5 % sem dizer "brinquedo sem piso"; so COMBINACAO C.4 diz "sem piso", antes da correcao K09, e a ponte com o piso do m2 nao esta feita em lugar nenhum. "Horizonte 2034" fica mais forte do que a propria entrega sustenta.

   *Conserto pedido:* Na mesma frase: "sem piso: 2.162 d (pesos iguais) / 1.806 d (pesos prop. a D), poder 90,5 % / 96,4 %; com o piso s0 do m2 (ajuste de dois pontos, sem graus de liberdade) lambda <= 3,90 nas duas regras, D90 inalcancavel". Rotular os dias vivos como brinquedo.

4. **(MEDIO)** COMBINACAO_K04.md:66 e :116; ERRATA_COMBINACAO_K09.md (nao trata); K04\COMBINACAO\K09\NOTAS_C_FONTES_E_DESENHO.md; VALIDACAO_K08_K09_15nov.json:4; ENTREGA_K09.md:10.

   Achado C3 da conferencia da K04 sobre a combinacao NAO foi aplicado (regra do posto). (a) O "poder 90,5 %/96,4 %" e, em lingua simples, a chance de um 5 sigma CONTRA o pacote se o mundo ficar como esta hoje (JUNO em 7,388; N_eff no padrao 3,044); o texto so diz que nao e probabilidade de o pacote ser verdadeiro. (b) Os fiduciais sao assimetricos (JUNO: o centro de hoje persiste; N_eff: o centro migra ao padrao) e o core tem as duas convencoes (4,30 sigma persistindo; 2,65 migrando); nao e dito que e escolha. (c) As tres rotas do Mapa que a conferencia apontou (estatistica.coincidencia_conjunta, neff.frozen_v1_08ago, cmb.fisher_gates_e_prereg_so_s4_14ago) continuam sem citacao (grep nos arquivos K09 da combinacao: zero). Tambem a conferencia pediu trocar "revisores distintos" por "revisao interna": VALIDACAO ainda diz "conferencias distintas e independentes".

   *Conserto pedido:* Uma linha ao operador: "se o mundo ficar como hoje, este teste tem 90 % de chance de devolver 5 sigma contra o pacote; os dois centros de planejamento foram escolhidos assim (JUNO persiste, N_eff migra); o core tem a outra convencao". Citar as tres rotas com "nao refazer". Trocar "distintas e independentes" por "revisao interna".

5. **(MEDIO)** RESSALVAS_UMA_A_UMA_K04.md:97 e :130-156 (bloco K09 R3/R4), :295-301 (R7); ERRATA_COMBINACAO_K09.md:44-53 e :61 (bloqueios).

   Escolhas de desenho que podem PRODUZIR o negativo estao fixadas pelo Kimi e entregues a "gerencia", sem leitura ao operador. (1) Particao R3/R4: calibracao = 3 ancoras + 9 MAS, as 92 HMS ficam em V_other. Pelas contas sobre numeros selados do core (so algebra, sem dado): com calibracao perfeita o alvo 5 (base Z = 4,514) so e viavel se as 3+9 carregarem pelo menos 18,5 % da variancia total, e o alvo D90 (base D = 5,191) so se carregarem pelo menos 31,7 %; do contrario f_q < 0 por construcao da particao, nao por causa do erro publicado nem do dado. O texto "leitura de um numero ruim" (f_q < 0 = outros erros sozinhos impedem) nao foi atualizado e nao diz isso. (2) R7: o p escolhido (contra o nulo, 6,11 sigma, o mais favoravel a diluicao) e dito com razao, mas nao entra na lista "antes de R3/R4 ratificar; antes de R7 o livro": so a particao e as bases estao ali.

   *Conserto pedido:* Na partitura ao operador: o que a particao decide (viabilidade do alvo ja no desenho), o que nao decide (a lei, o dado), o que o negativo significaria (fragilidade da particao e do erro publicado, nao falsificacao), com os dois limiares 18,5 % e 31,7 %. Listar a particao, as duas bases e o p do R7 como itens a ratificar PELO OPERADOR depois da leitura.

6. **(MEDIO)** RESSALVAS_UMA_A_UMA_K04.md:22-32 (quadro; R4 na l.29, R5 na l.30, R7 na l.32), :204 (R5, numero ruim), :247 (R7, Ato); ENTREGA_K09.md:28.

   A tabela "que ato resolve cada ressalva" esta coerente com o DESENHO 4.2 em R1, R2, R3, R6, mas: (a) R7 aparece na coluna "Ato que resolve de fato" com "futuras replicas disjuntas e funcao global" e o texto diz "Resolver exige historia declarada"; o DESENHO diz que a 7 nunca se resolve, so se declara, e a frase-resumo do DESENHO (um teste cego novo resolve 1, 2, 6 e, com calibracao e covariancia independentes, 3 a 5; a 7 so se declara) nao esta em nenhum arquivo K09; (b) R4 acrescenta "dado independente", que o DESENHO nao traz; (c) a linha R5 do quadro continua com "piso comum que levaria D=6,71 a D90" (formula das 72 direcoes, retirada) e o paragrafo "leitura de um numero ruim" de R5 ("piso grande sem efeito ... contraste nao recebe informacao") nao vale para o modelo por linha; nao ha "o que o negativo significa" para o tau por linha.

   *Conserto pedido:* Reescrever as celulas: R7 = "so se declara: historia + livro; replica disjunta cria evidencia nova mas nao apaga"; R4 = "covariancia e sistematicas independentes"; R5 = "orcamento independente; a conta que existe e o ruido por linha (tau)"; acrescentar para o tau: um tau5 pequeno mede fragilidade da tabela de erros, nao falsificacao. Pôr a frase-resumo do DESENHO no ENTREGA.

7. **(MEDIO)** ENTREGA_K09.md:8; REGISTRO_MAPA_K09.json:5; COMBINACAO_K04.md:95, :200-204, :256-262; ERRATA_COMBINACAO_K09.md:25. Insumo: C:\IALD\Central de Patentes\work\conjunto_D_20261029\parametrizacao_03nov\PODER_RAMO_B_ANTES_DE_ABRIR.json (sha256 05bc5a1f...a4935, confere; o K09 cita so o nome, sem caminho).

   Portao nao mostrado ao lado. A fala do operador de 13/11 (bytes abertos: 886 B, sha16 4698446c391f9aba) pede "poder preditivo acima de 5 sigma"; as contas de ringdown e combinacao usam so D90 = 6,28 (leitura do K01: 90 % de poder a 5 sigma). A regra da casa nos ritos (poder_min = 5,0 em PODER_RAMO_B_ANTES_DE_ABRIR.json) e outra. Isso inverte o veredito "inalcancavel": no ringdown a saturacao 5,805 (viés 0,0686, C2 ampla de 50 PE) fica ACIMA de 5; para poder 5 sao ~63 eventos (~4,7 anos a taxa O4b de 11,2/ano), e sem viés 1,61x a informacao (6,1 eventos, ~6,6 meses); na combinacao com portao 5 o requisito e sigma_J <= 0,0341 (1.087 d, pesos iguais) ou 0,0355 (1.001 d, pesos prop.) contra 0,0301 (1.393 d) do JUNO sozinho. Alem disso o ENTREGA e o REGISTRO escrevem "D10 satura ~5,8" sem dizer "C2 ampla" e dao "8,7 e 16,6 meses" sem dizer "sem viés", na mesma frase que diz que o viés impede D90: leitura contraditoria.

   *Conserto pedido:* Mostrar os dois portoes lado a lado (como o Hubble ja faz: 5 sigma e D90), dizer que a escolha entre eles e do operador e que muda "inalcancavel" para "alcancavel"; marcar 8,7/16,6 meses como "sem viés" e a saturacao como "para C2 ampla (50 PE)"; citar o caminho do PODER_RAMO_B.

8. **(BAIXO)** ENTREGA_K09.md:8; REGISTRO_MAPA_K09.json:5.

   "A combinacao nao antecipa nada" (ENTREGA e REGISTRO) e curto demais: em dias vivos o requisito do ramo JUNO cai 1,7 % (pesos iguais) ou 17,9 % (pesos prop.): 2.162 e 1.806 contra 2.199 do JUNO sozinho. O que e verdade: a data e travada pelo produto do SO (2034); JUNO sozinho no cenario ideal chega em 25/05/2032, e com duty cycle 0,782 em 28/01/2034, ou seja, empata com o SO. A frase completa esta em COMBINACAO e INSUMOS F12, nao no topo.

   *Conserto pedido:* Repetir no topo a frase completa: "2034 e o fim do levantamento do SO; a combinacao poupa dias vivos do ramo JUNO, mas a data e travada pelo SO e o JUNO sozinho chega antes no cenario ideal".

9. **(BAIXO)** HUBBLE_JA_EXAMINADO_K04.md:117, :119, :124 (versus :73, :163, :200).

   Cosmeticos de Hubble: (a) na tabela larga a celula do H0DN baseline diz "7,068, conta de bolso; D da casa 6,710 acima" (bolso antes da casa, a ordem pedia o contrario); (b) "SH0ES JWST ... D90 falha por 0,022": 6,28155 - 6,2587 = 0,0229, arredonda 0,023; (c) a linha da reanalise MCP diz "Nao na F9" enquanto a linha 73, a 163 e a secao 5.1 dizem que sao as mesmas cinco galaxias de uma familia ja na V2.

   *Conserto pedido:* Inverter a ordem na celula; trocar por 0,023; na linha 124 escrever "familia ja na F9 (mesmas 5 galaxias MCP); o valor da reanalise nao esta na F9".

10. **(BAIXO)** HUBBLE_JA_EXAMINADO_K04.md:197-202; NOTAS_EMPILHAMENTO_DESI_K09.md secao 1.

   "Quanto do empilhamento ja e a Fase 9 V2" e respondido so em numero de linhas (1 de 2; 2 de 5). O numero existe e e barato: [DERIVED-revisor, nominal, sem ponte] TDCOSMO e masers sao 28,4 % da informacao do empilhamento de 5 linhas (36,1 % no de 2); sem elas, SN II + FRB + BBH-AGN dao D = 4,57 (3,99 com SN II sys=stat). O comparador V2 (z_disc 4,443 < 5) so esta na linha 20 da tabela, longe do empilhamento.

   *Conserto pedido:* Acrescentar uma linha com 28,4 % / 4,57 e o z_disc 4,443 da V2 ao lado de 4,04 e 5,34; manter "nao cego, nao independente, nao soma".

11. **(BAIXO)** HUBBLE_JA_EXAMINADO_K04.md:208; NOTAS_EMPILHAMENTO_DESI_K09.md secao 2; ERRATA_HUBBLE_K09.md:58; ENTREGA_K09.md:6.

   DESI DR3: o texto escreve "Criterio adotado" e "Decisao documental adotada" e o ENTREGA diz "esta respondido (fundo, nao testemunha)". E escolha entre alternativas feita por uma IA; as cinco condicoes para virar testemunha estao bem ditas, mas a escolha e da gerencia/operador.

   *Conserto pedido:* Trocar por "proposta [DECLARADO]: tratar como fundo ate cumprir as cinco condicoes; decisao da gerencia/operador".

12. **(BAIXO)** COMBINACAO_K04.md:264 e :277; ERRATA_COMBINACAO_K09.md:27; NOTAS_C_FONTES_E_DESENHO.md secao 5.

   F2b e ato do operador: os dois atos tem bytes e eu os abri (29/10, 47 B: "autorizo a realizacao do teste do conjunto D"; 03/11, 1091 B: "concordo com c, porque se o teste nao tiver poder nao vou inseri-lo no um.py"; sha256 conferem; a retirada e conclusao da gerencia no core). Falta dizer o que e a opcao (c): pelo Mapa (seq 1546, 1744) e "PE cega dos 10 ate o estagio cego e decidir a abertura ali", abertura FORA da fila, e o seq 1775 diz que o teste so roda com a palavra do operador; a autorizacao de 29/10 foi dada sobre a premissa (z_excl ~7 -> FALSIFIED) que a gerencia corrigiu no mesmo dia (poder 3,7-3,9 < 5, NOT_FALSIFIED_UNDERPOWERED), e o operador decidiu de novo em 03/11. "D esta autorizado e nao aberto" pode ser lido como autorizado a abrir.

   *Conserto pedido:* Acrescentar: "(c) = rodar ate o estagio cego; a abertura nao esta na fila; so roda com a palavra do operador (Mapa seq 1775); so entra no um.py se tiver poder".

13. **(BAIXO)** REGISTRO_MAPA_K09.json:5-6 e artefatos; ENTREGA_K09.md:24; K04\COMBINACAO\K09\MANIFESTO_CENSO_R7_MAPA_K09.json.

   REGISTRO e DEPOSITO: guardas ok (sem "confirm", sem aspas angulares; a copia de _valida aceita o registro com 13 artefatos; nomes nao reservados; DEPOSITO diz so o entregue, onde e "aguarda a conferencia"; hashes de ENTREGA, REGISTRO e VALIDACAO conferem). Ressalvas: (a) "classe preliminar ratificada pelo operador antes do selo" le-se como ato feito, sem bytes; escrever "a ratificar pelo operador"; (b) estatuto "REAL (leituras e validacoes)" antes da conferencia: DECLARADO ate a gerencia conferir; (c) faltam em artefatos o CENSO_R7_MAPA_K09.json e o MANIFESTO (assim a ferramenta os hasheia); (d) o hash do Mapa no manifesto (558d49b9...) reproduz como prefixo das primeiras 2066 linhas do rotas.jsonl: gravar "2066 linhas" no manifesto.

   *Conserto pedido:* Aplicar (a)-(d) antes de registrar.

14. **(BAIXO)** COMBINACAO_K04.md:37 e :210; NOTAS_C_FONTES_E_DESENHO.md secao 1.

   Duas formulacoes sem os dois eixos e pins: (a) "Pode ser cego somente no incremento" fica sem os dois eixos (a correcao K09 nao tocou); (b) NOTAS_C pina a ORDEM_K09 por f5a9985b..., que e o .bak anterior ao AO LADO de 15/11 (a ORDEM atual e 4607f0f0...); (c) a cifra de ~390 candidatas foi retirada como sem lastro no resumo de arXiv:2608.12193 (certo), mas o Mapa seq 1482 traz 390 de arXiv:2605.27225 (API); nenhuma conta usa o numero.

   *Conserto pedido:* (a) "posterior a previsao publicada (22/01 e 17/02/2026) e ao pino de 08/08/2026, e ainda nao mostrado"; (b) dizer qual versao da ORDEM; (c) opcional: citar o seq 1482 ou manter retirada sem dizer "sem lastro".

## Para o operador (propostas do revisor, em língua simples; a gerência confere antes de ler a ele)

- A parede resiste e os numeros de poder reproduzem: nao ha hoje teste cego de natureza com poder acima de 5 sigma, e nada foi aberto nem reaberto. O H0DN continua como estava.
- Um numero esta no lugar errado: o 2,33 sigma e o poder da leitura que ja foi lida (a lei acumulada nos cronometros, que deu -1,66 sigma e ficou desfavorecida, nao excluida). A lei nova do lado transmitido ainda nem foi escrita e nao tem poder dito. Precisa ser corrigido antes de ir para o Mapa.
- Se for rodar a conta das tres ressalvas, o senhor decide antes quais fatores contam como calibracao: dependendo da divisao, o resultado pode sair "impossivel" so pela divisao (calibracao precisaria ter pelo menos 18,5 % da variancia para 5 sigma e 31,7 % para o portao de 90 %), nao pelo dado nem pela lei.
- O "poder 90 %" da combinacao significa: se o mundo ficar como hoje, 90 % de chance de um 5 sigma contra o pacote. E o portao da sua frase ("acima de 5 sigma") pode ser 5,0 ou 6,28 (90 % de poder): com 5,0 o ringdown deixa de ser inalcancavel; a escolha e sua.

## Consultas ao Mapa

- rotas.py consultar (termo unico): hubble (27 rotas), stouffer (1), ringdown (34), combinacao (5), F2b (8), h0dn, fase9, SH0ES (as quatro ultimas para checar cobertura: 75 rotas distintas, 49 nao citadas, a maioria de selo/infra)
- rotas.py ver das nove rotas omitidas: d1.fase7_cc_covariancia_01out (247,257,258), bancada.preregistro_dois_lados_delta_k (275,276,279,282,290,291,303), um_py.v380.fases_5_6_7_por_hash (262-264), discriminante.lentes_5sigma_20261019 (1225-1245), discriminante.ordem018.r_h_sirenes (401,1638), d1.fase9.auditoria_suficiencia_20261019 (1247), d1.fase9.integracao_20261019 (1248-1257), estatistica.h0dn_bg1.cov_injecoes_06nov (1867), natureza.5sigma_fora_da_cosmologia_poder_27out (1479-1482): rota e seq conferem, conteudo bate com as linhas 23 a 31 do Kimi
- rotas.py ver de discriminante.ordem018.f2.r_g (379,391,393,1637), ringdown.ramo_b_preregistro_v386 (seq 1508,1526,1545,1546,1737,1744,1775) e estatistica.v412.k04_hubble_m2_combinacao (2063,2067,2076)
- rotas.jsonl lido por script meu (2.062 registros ate seq 2062; 505 rotas; 123 rotas e 285 registros com olhou_dados; 16 por prefixo; 18 fora do prefixo citando Hubble/H0)
- Resultado: nenhuma rota do Mapa traz o 2,33 sigma ligado a lei pendente; os registros do K09 nao foram registrados por mim (nada escrito no Mapa).

## Examinado

- Lidos inteiros: ENTREGA_K09.md, HUBBLE_JA_EXAMINADO_K04.md, ERRATA_HUBBLE_K09.md, COMBINACAO_K04.md, ERRATA_COMBINACAO_K09.md, RESSALVAS_UMA_A_UMA_K04.md, REGISTRO_MAPA_K09.json, DEPOSITO_K09.md, INSUMOS_PARA_A_PERGUNTA_K09.md, ORDEM_K09 e ADENDO de 15/11, LEITURA_K09_PARCIAL_NEUTRINO_15nov.md, REVISAO_K04_HUBBLE.md, REVISAO_K04_COMBINACAO_RESSALVAS.md, DESENHO_v412_R1.md (secoes 3 a 4.5), K04\HUBBLE\K09\NOTAS_*.md, K04\COMBINACAO\K09\NOTAS_C_FONTES_E_DESENHO.md.
- Fontes abertas por mim: core um_absoluto.json (sha256 36c69fc7..., confere; f2b_errata_v404; h0dn_bg1_v411.values D 6,710150598579069 / 5,19131201002441 / z_null / p_unilateral / soma_w2); PODER_RAMO_B_ANTES_DE_ABRIR.json (05bc5a1f...a4935); PREREGISTRO_RAMO_B_RINGDOWN_V1.md (censo 14/10/8/22 e eventos O4a/O4b); PREREGISTRO_DOIS_LADOS_DELTA_K_V1_4.md; PERGUNTAS_QUE_FALTAM...:119; bytes do operador (29/10, 03/11, 28/10 x2, 13/11 x2) com sha256 conferido.
- Hashes: os 10 da tabela do ENTREGA e os 3 do DEPOSITO conferem com o disco; manifesto SHA256SUMS_K04_HUBBLE 65/65 conferem; REV2 do relatorio de Hubble preservada (37fee18c...); census 08ad355c... confere; hash do Mapa do manifesto reproduz como prefixo de 2066 linhas.
- Scripts do Kimi lidos (extrair_rotas.py, medidas_planejamento.py, verificar_relatorio.py, mapear_metadados_k09.py): so json/math/hashlib; mapear_metadados le valores selados do core, nomes e semantica de factors.json e o Mapa; nenhum npz, rede ou subprocess. Nao rodei nenhum deles.
- Meus scripts, so nesta pasta: C:\Users\rotol\AppData\Local\Temp\claude\b4ca26c934d2167f\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v412_k08_k09\K09_C\contas_k09c.py, tabela_D.py, lista_seq.py, rotas_copia.py (copia usada para o dry-run de _valida, sem gravar), ver\*.txt e cons_*.json. Nenhuma rede, nenhum modelo, nenhum dado observado, nenhum lake, nenhuma escrita fora da pasta.
- Nao conferi: literatura (arXiv/DOI) dos D de planejamento alem do que a revisao da gerencia ja conferiu; as janelas O4a/O4b nas fontes (so a aritmetica de calendario: 293 e 237 dias); as partes M2/PRE_REGISTRO/ERRATA_NEUTRINO (outro revisor); nao abri network.npz nem factors.json (so os nomes citados pelo Kimi).

