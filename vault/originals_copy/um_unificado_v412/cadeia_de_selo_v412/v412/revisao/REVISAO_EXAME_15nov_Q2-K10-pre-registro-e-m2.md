# CONFERÊNCIA DISTINTA — as entregas do Codex (unidade do tipo III) e do Kimi (K10), examinadas por ordem do operador — Q2-K10-pre-registro-e-m2

> Montado pela gerência c1 em 15/11/2026 19:34 a partir do retorno estruturado de um revisor distinto (só leitura; scripts próprios na pasta de rascunho dele). É [DECLARADO pelo revisor] no que a gerência não reconferiu. Não é fala do operador. Nada aqui está instalado.

**Veredito:** APROVADO_COM_RESSALVAS — achados: 1 ALTO, 6 MEDIO, 5 BAIXO

## Resumo

1. As contas reproduzem com script meu (Q2\conta_q2.py, scan_c.py, datas_q2.py; beta so por ALPHA_FINE_CODATA_2018 x raiz de e): Tabela 6 = 64,788 % (centro publico) e 99,730 % (previsao verdadeira); com piso 3,58 / 6,36 / 7,81 % e D 2,21 / 2,47 / 2,58, teto delta/s0 = 2,86; NuFIT 2,953 contra 3,024 e 3,044; as seis datas de brinquedo e o SK-Gd (17/10/2027). Nenhum erro de aritmetica.
2. Situacao dos achados. Pre-registro: 1 ALTO PARCIAL, 2 ALTO SIM (no K10; NAO no ENTREGA_K09), 3 ALTO SIM, 4 ALTO PARCIAL, 5 a 10 MEDIO SIM (7 e 10 com ressalva). M2: 1 ALTO PARCIAL, 2 a 7 MEDIO SIM. Os BAIXO estao sanados salvo os que listo abaixo.
3. ALTO restante: o ENTREGA_K09.md, que a K10 declara "corrigido ao lado" e cujo hash ela pina, ainda diz "pronto para a gerencia ler ao operador", define o observavel pela chave antiga, diz que o negativo nao atinge "nem o gate" nem "beta isolado" e que "revisor independente abre". Sao exatamente os defeitos dos achados 1, 2, 4, 7 e 9.
4. As duas camadas do negativo (bandeiras nao se movem; contorno v314 cai) estao ditas no pre-registro K10, nos insumos, na errata e na ENTREGA_K10 (confere com um.py l.299841-299869, l.4702). Falham a ENTREGA_K09 e a definicao de "gate", que mistura as 18 bandeiras do fecho com o 1=1.
5. A frase nova (conjuncao beta x sen 45 x u com m1 perto de zero; ajustar u ou o angulo depois nao reverte) esta certa no conteudo e nao e atribuida ao operador: e redacao do revisor, adotada pelo Kimi. Mas a ENTREGA_K10 a rotula "[REAL, lido no um.py]", a clausula de resgate e compromisso e nao fato, nao esta na tabela de escolhas, e o par 5.1 omite o ordenamento normal e o [ONTO] do sen 45.
6. Chave da cegueira: escrita sem ambiguidade em 1.1 (primeira aparicao publica do numero, depois da previsao de 17/02/2026 E do selo, com carimbo externo; S tambem pos-selo; registro datado da busca). Restam frases de um eixo so (0.1, 1.2, 2.4, 8; 59,1 d em 1.1, F11 e M2 par 5) e uma parentese ambigua no M2 e no ENTREGA_K09 ("antes de qualquer acesso do selo").
7. Nenhuma frase diz ou sugere que o autor viu dado de neutrino antes (varredura por grep nos arquivos da rodada). A clausula repetida "nao diz o que o autor leu ou deixou de ler" nao viola, mas e ruido.
8. Gatilho, prazo-limite e plano B estao como PENDENTES do operador, com alternativas, e "uma regra so, ou duas com precedencia antes do selo" esta em 4, D2 e E2. Faltam na tabela E1-E15: a clausula de resgate, a abertura unica com "estresse nao consome", a convencao de erro assimetrico, o centro H1, e o acoplamento de E12 (contorno) com E10/E14 (escada).
9. A primeira pagina diz o que decide, o que nao decide e o que o negativo significa, e promete parede medida, mas NAO esta em lingua de leigo (r, D, delta/s0, identity_true, v314); a versao leiga esta no par 8, no fim.
10. O poder aparece sem a hipotese do mundo: "4 a 8 %" (par 0.2 e bloco leigo dos INSUMOS) omite "se o valor verdadeiro for o centro publico"; sob a previsao verdadeira e ~0. O "65 %" da ENTREGA_K10 e do REGISTRO_MAPA_K10 e para sigma = 0,024, inalcancavel com o piso, e o "99,7 %" e P(r<3) do primario, nao o veredito do canal.
11. JSON em dados: os artigos de 2025 sem formula e sem valor (conferi: zero ocorrencias nos dois .tex do acervo); nada instalado (um.py de 12/11 e core de 13/11 intocados). Estatuto em quase toda data; faltam no pino de 08/08 (so mtime local, rotulado REAL) e em tres linhas da tabela do M2 par 5.
12. Veredito APROVADO_COM_RESSALVAS: o ALTO e residuo em arquivo antigo pinado (conserto mecanico). Antes de a gerencia registrar no Mapa (livro so-acrescimo) e antes de ler ao operador, corrigir os itens 3, 9 e 10.

## Achados

1. **(ALTO)** C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\ENTREGA_K09.md l.4 e l.24 (hash 5ddb3869... pinado em ENTREGA_K10.md l.50 e declarado 'corrigida ao lado' em ENTREGA_K10.md l.14)

   grep -n 'pronto|revisor independente|antes de qualquer acesso do selo|nem o gate' ENTREGA_K09.md mostra: l.4 'pronto para a gerencia ler ao operador'; l.4 e l.24 definem o observavel por 'primeira vez depois de 08/08/2026 e antes de qualquer acesso do selo' (a chave antiga, diferente da de PRE_REGISTRO_K10 sec.1.1); l.24 'o negativo atinge o pacote da escala ... nao beta isolado nem o gate' (uma camada so e a exclusao 'nao beta isolado': achados ALTO-1 e MEDIO-7 do relatorio K09 do pre-registro, e a ordem K10 sec.1 item 2 exige as duas camadas em todo texto); l.24 'revisor independente abre uma unica vez' (MEDIO-9). Os consertos feitos nesse arquivo foram so l.3, l.10, l.18 e l.20. A tabela de hashes dentro dele esta velha: 6 de 7 arquivos (M2, JSON, COMBINACAO, HUBBLE, ERRATA_M2_K09 e K09_15nov) nao batem mais com o disco (script de sha256 meu). ERRATA_K10_PRE_REGISTRO 'O que ficou OPEN' item 1 so lembra a l.10.

   *Conserto pedido:* Reescrever l.4 e o paragrafo C (ou marcar 'SUPERADO pelo PRE_REGISTRO_K10 sec.0.1, 1.1 e 5.1' no topo), tirar 'pronto', 'nem o gate', 'nao beta isolado' e 'revisor independente'; dizer que a tabela de hashes e historica e remeter a VALIDACAO_K10.

2. **(MEDIO)** PRE_REGISTRO_INCREMENTO_JUNO_RASCUNHO_K10.md l.15 e l.197 (definicao de 'gate'); um.py l.300824

   O texto define gate como 'o conjunto de checagens do um.py que autorizam o veredito nuclear do programa, o 1 = 1' e logo diz que 'as bandeiras do gate nao se movem' enquanto o contorno derruba o 1 = 1: um leigo le contradicao. No um.py o gate e core['qg_closure']['gate'] (qg_closure_verdict e as 18 bandeiras; grep -n qg_closure_verdict um.py -> l.300824) e a identidade 1=1 e verdict['identity_true'] (l.157806, alterado so no contorno l.299864-299866). Os dois fatos do texto estao certos; o nome unico para as duas coisas e que promete errado.

   *Conserto pedido:* Dois nomes: 'gate do fecho da gravidade quantica (as 18 bandeiras): nao se move' e 'veredito 1=1 do contorno: cai com FALSIFIED limpo, se o operador mantiver o rol'.

3. **(MEDIO)** PRE_REGISTRO_K10 sec.0.1-0.2 (l.7-23); ENTREGA_K10.md l.9

   ENTREGA_K10 l.9 diz que a parede medida esta 'na primeira pagina, em lingua de leigo'. A pagina usa conjuncao beta.sen45.u, m1, bandeiras do gate, identity_true, 'FALSIFIED limpo', contorno v314 com numeros de linha do um.py, D = 2,21/2,47/2,58, s^2 = s0^2 + a/T, sigma_S em 1e-5 eV^2, delta/s0, D90. A versao leiga existe (sec.8, l.235-244) mas esta no fim e marcada 'proposta do revisor, a gerencia confere'. A regra do posto pede a lingua dele antes do teste.

   *Conserto pedido:* Subir a sec.8 (conferida pela gerencia) para 0.1 e deixar o tecnico como anexo; corrigir 'em lingua de leigo' na ENTREGA_K10 enquanto nao estiver.

4. **(MEDIO)** PRE_REGISTRO_K10 l.21 (sec.0.2) e INSUMOS_PARA_A_PERGUNTA_K09.md l.55 (bloco em lingua simples)

   'a chance de 5 sigma e 3,58 % ... 7,81 %' (l.21) e 'a chance de esse teste dar o veredito de morte em 1 a 3 anos e de cerca de 4 a 8 %' (INSUMOS l.55) nao dizem em que mundo: so vale se o valor verdadeiro for o centro publico de hoje (H1). Sob a previsao verdadeira (H2) minha conta da P(r>=5) = 0,000059 % em 1, 2 e 3 anos (conta_q2.py). E o mesmo defeito do ALTO-1 do M2 (a condicao some e o operador e induzido a ler probabilidade incondicional de negativo). A condicao so aparece em 3.3 ('P(r>=5 | H1)') e em 8 ('mesmo que a TGL estivesse errada no tamanho que o dado de hoje sugere').

   *Conserto pedido:* Em 0.2 e no bloco leigo: 'se o valor verdadeiro for o centro publico de hoje, 7,388; se for a previsao, a chance de negativo e praticamente zero'.

5. **(MEDIO)** ENTREGA_K10.md l.11; REGISTRO_MAPA_K10.json campo 'resultado' do 2o item; ERRATA_K10_M2.md tabela linha 1

   'P(r>=5) ~ 65 % se o valor verdadeiro e o centro publico; ARMED_CONSISTENT ~ 99,7 % se a previsao e verdadeira' aparece sem a condicao de desenho: 65 % e para sigma = 0,024 (a linha 'Tabela 6', projeto D90; 64,788 % no meu script), que M2 par 4.2 e PRE_REGISTRO 3.3 dizem inalcancavel com o piso, onde o real e 3,6 a 7,8 %. A mesma ENTREGA traz 4-8 % na l.9 sem ponte entre os dois numeros. Alem disso 99,7 % e P(r<3) do primario (a2 = 99,730 %; b2 = 99,408 %), nao o veredito do canal: o veredito le a ULTIMA linha da escada (um.py l.4654, l.4666-4669); com NuFIT da tabela (3,024) como ultima linha seria TENSION mesmo com a previsao verdadeira. O REGISTRO_MAPA entra num livro so-acrescimo.

   *Conserto pedido:* Escrever 'no desenho sigma = 0,024 (inalcancavel com o piso; real 4-8 %)' e 'se o incremento for a ultima linha da escada (E14)'; corrigir antes de a gerencia registrar.

6. **(MEDIO)** PRE_REGISTRO_K10 sec.5.1 itens 1-2 (l.195-196), sec.9 (l.246-264); ENTREGA_K10.md l.10; PRE_REGISTRO l.17 vs l.237

   Origem e escolhas. (a) ENTREGA_K10 l.10 poe '[REAL, lido pela gerencia no um.py selado]' sobre um item que inclui 'o negativo falsifica a conjuncao ... ajustar u ou o angulo depois nao reverte o veredito': essa frase e o conserto do revisor (REVISAO_K09_PRE_REGISTRO #7), nao leitura do um.py, e a clausula de resgate e um compromisso novo, nao um fato; nao e do operador (grep de atribuicoes: nenhuma). (b) PRE_REGISTRO l.17 chama a partitura 'leitura da gerencia' e a sec.8 'proposta do revisor': atribuicao inconsistente. (c) A clausula de resgate, a abertura unica com 'estresse nao consome' (l.213, l.218), a convencao de erro assimetrico (l.108, entra no hash) e o centro H1 de planejamento sao escolhas de desenho que nao constam da tabela E1-E15. (d) A 5.1 nao diz 'ordenamento normal' (so 0.1 e INSUMOS) nem marca o sen 45 como leitura do operador [ONTO]: o achado BAIXO-10 do M2 ficou PARCIAL (so o ENTREGA_K09 l.24 nomeava).

   *Conserto pedido:* Rotular como [DERIVED, proposta do revisor, nao conferida pela gerencia]; acrescentar E16 (clausula de resgate), E17 (abertura unica e estresse), E18 (convencao de erro); nomear ordenamento normal e [ONTO] na 5.1.

7. **(MEDIO)** PRE_REGISTRO_K10 l.15, l.197, l.171, l.261 (E12); um.py l.299856, l.4654-4669

   O contorno le so o veredito do rito neutrino_m2 do um.py (core.get('neutrino_m2').verdict, l.299856), que sai da ESCADA e da regra l.4662-4669. Um veredito de script externo pinado por hash (sec.6.5) so chega ao contorno se o incremento entrar na escada. Logo E12 ('o contorno vale para o incremento?') e a mesma decisao pratica que E10/E14 (quem entra na escada e qual e a ultima linha): o operador poderia escolher E10 sem saber que escolheu E12. O texto nao diz isso. Tambem nao diz que, sob a regra A, FALSIFIED exige dois grupos autonomos (duas linhas do JUNO contam como UM grupo, l.4662) e que o contorno so cai com FALSIFIED limpo, entao sob A com P sozinho o contorno nao cai.

   *Conserto pedido:* Acrescentar a E12 'depende de E10/E14' e a frase 'um negativo do script externo so toca o contorno se entrar na escada do um.py'; carregar 'duas linhas do JUNO = um grupo' para a coluna A da sec.4.

8. **(BAIXO)** PRE_REGISTRO_K10 l.11 (0.1), l.49 (1.2), l.118 (2.4), l.239 (8), l.35 e l.17 de INSUMOS F11 (59,1 d), M2_DESFECHOS par 5 l.215

   A regra da casa pede os dois eixos na mesma frase. 0.1, 1.2, 2.4, 8 e D1 falam de cegueira so pelo selo; as frases do JUNO 59,1 d (PRE_REGISTRO 1.1, INSUMOS F11, M2 par 5) dizem 'anterior ao valor publico' sem 'e anterior ao pino', o mesmo residuo do achado 3 do M2. Alem disso M2 par 5 e ENTREGA_K09 l.4/l.24 usam '(e antes de qualquer acesso do selo)', que nao diz de qual selo nem se e 'depois do selo' como em 1.1. Em 1.1 'o artigo JUNO (29/09) e o SK-Gd ja sao posteriores aos dois marcos' mistura artigo e numero: pela chave de 1.1 o numero de 207,2 d ja era publico em 22/06 e 15/07 [DECLARADO], antes do pino.

   *Conserto pedido:* Pôr o segundo eixo nas frases listadas; trocar a parentese por 'posterior ao selo deste pre-registro, com carimbo externo'; escrever 'o artigo repete um numero que ja era publico'.

9. **(BAIXO)** PRE_REGISTRO_K10 l.218 (6.6), l.63 e l.215

   6.6 ainda diz 'espera-se a fonte completa (ou o gatilho) sem conhecer o centro': com dado publico isso nao se garante (achado 3b do K09, que a K10 aceitou na l.211 mas nao tirou aqui). E 'o caso mais provavel e SEM veredito' (l.63, l.215) sai de UM so precedente (59,1 -> 207,2); a K10 tirou a 'taxa de base 0 em 1' mas deixou a conclusao. E E8 (carimbo externo) e pendente, mas 1.1 o poe como exigencia sem dizer que, sem ele, a cegueira nao pode ser dita.

   *Conserto pedido:* Trocar por 'sem alterar nada do desenho'; escrever 'ha um so precedente e ele foi cumulativo'; dizer em E8 'sem carimbo externo nao se afirma cegueira'.

10. **(BAIXO)** PRE_REGISTRO_K10 l.78 (identificabilidade)

   '0,32 no limite de C positivo' e '8,28 com C negativo admissivel' sao do revisor e nao estao marcados como nao reconferidos. Meu scan_c.py: r_Delta = 1,873 (C=0) e 0,610 (C=Vc) reproduzem; 8,28 reproduz em C = -0,9 raiz(V0.Vc); mas o limite de C positivo admissivel (C = raiz(V0.Vc)) da 1,185 e r cai a ~0 perto de C = 0,97 raiz(V0.Vc); o 0,32 nao corresponde a nenhum limite. A conclusao qualitativa (C troca o veredito) fica mais forte: r varre de ~0 a mais de 100.

   *Conserto pedido:* Marcar [DERIVED pelo revisor] e trocar por 'r varre de quase 0 a mais de 100 no intervalo admissivel'.

11. **(BAIXO)** ERRATA_NEUTRINO_V412_DADOS_K09.json l.5-12, l.30-38, l.55-66; M2_DESFECHOS par 5 (tabela, linhas 18/11/2025, 29/09/2026, 02/10/2026)

   (i) 'previsao.beta' = 0,012031300400803142 esta como literal numerico: se a gerencia instalar o JSON no core, viola a regua 5; manter so alpha CODATA e a formula. (ii) 'busca_formula_e_valor_nos_dois_tex' cita os arquivos por nome, sem sha256: conferi nos .tex do acervo (lie_of_light.tex 29745 B sha16 c8e14d738a55cab2; neutrino_nmc_revised.tex 36843 B sha16 265f65d90c12a753): zero ocorrencias de 8,5x, 0,0085, sin 45, 45 graus, pi/4, raiz de e, 1 eV, JUNO, beta_TGL, alfa raiz de e; meV so no intervalo 'meV to PeV'. Mas e busca no .tex, nao nos PDFs do Zenodo (sem rede). (iii) 'data_do_congelamento' foi mantido ao lado de 'data_objeto_original' sem estatuto (a ambiguidade que o achado 8 do M2 apontou); o pino de 08/08 so tem mtime local (02_frozen_neutrino_m2_v2.py, sem git) e esta rotulado REAL, enquanto o 22/01 recebeu 'sem carimbo externo'; tres linhas da tabela M2 par 5 ficaram sem estatuto.

   *Conserto pedido:* Trocar beta por campo 'formula'; pinar os sha256 dos .tex; remover 'data_do_congelamento'; rotular o 08/08 'DECLARADO, sem carimbo externo'; marcar as tres linhas.

12. **(BAIXO)** COMBINACAO_K04.md l.260 (fora da minha lente)

   'nao move o gate' sobre o par D do ringdown e dito sem a camada do contorno; o roster v314 inclui coma_dephasing e coma_cego (um.py l.299858-299859). Nao verifiquei se esse rito entra no roster, so que a frase tem uma camada.

   *Conserto pedido:* A lente de Hubble e combinacao confere e acrescenta a segunda camada se couber.

## Para o operador (propostas do revisor, em língua simples; a gerência confere antes de ler a ele)

- Proposta minha, nao fala sua: o rascunho novo do pre-registro do JUNO esta melhor, mas ainda nao esta em lingua que o senhor leia sem tradutor, e um arquivo antigo (ENTREGA_K09) ainda diz que esta 'pronto' e que o negativo nao atinge o gate.
- Antes de ler ao senhor: o numero de chance de negativo (4 a 8 %) so vale se o valor verdadeiro for o que o JUNO mede hoje; se a previsao for verdadeira, a chance e quase zero, e o '65 %' que aparece num resumo e de um projeto que o proprio erro do JUNO nao deixa alcancar.
- O que um negativo faria tem duas partes: as bandeiras da gravidade quantica nao se mexem, mas o um.py selado derruba o 1 = 1 do contorno; e essa segunda parte so vale para o incremento se ele entrar na escada do um.py, o que e decisao sua.
- Escolhas que ainda estao escondidas e deviam estar na sua tabela: a clausula de que mexer em u ou no angulo depois do negativo nao reverte o veredito, a abertura unica, e a regra de qual lado do erro vale.

## Examinado

- PRE_REGISTRO_INCREMENTO_JUNO_RASCUNHO_K10.md (265 linhas, inteiro), ERRATA_K10_PRE_REGISTRO.md, INSUMOS_PARA_A_PERGUNTA_K09.md (rodada 4), ERRATA_K10_M2.md, M2_DESFECHOS_E_SEGUNDA_TESTEMUNHA_K04.md (365 linhas), ERRATA_NEUTRINO_V412_DADOS_K09.json, ERRATA_M2_K09.md, ERRATA_M2_K09_15nov.md, ERRATA_RESIDUOS_EIXOS_K01_K04.md, ENTREGA_K09.md, ENTREGA_K10.md, REGISTRO_MAPA_K10.json, VALIDACAO_K10_15nov.json, DEPOSITO_K10.md, ORDEM_K10 e ADENDO_C, em C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi
- REVISAO_K09_PRE_REGISTRO_DO_INCREMENTO.md e REVISAO_K09_M2.md (inteiros), em ...\v412\revisao
- um.py selado: l.4600-4705 (rito neutrino_m2) e l.299841-299869 (contorno v314) com numeros de linha conferidos; grep de identity_true, qg_closure_verdict e does_not_gate_core; sha256 e mtime de um.py (12/11), um_absoluto.json (13/11) e selo (13/11): nada instalado
- 02_frozen_neutrino_m2_v2.py e _resultado.json em C:\IALD\Artigo\teste_acustico_beta_tgl_v1: sha256 por script (2564d7c9..., 6f0963a5..., frozen_hash 4bdae22a... conferem com o JSON); mtime local de 08/08/2026 16:15, sem git
- Os dois .tex de 2025 em C:\IALD\papers_latex (lie_of_light, neutrino_nmc_revised): busca por script, zero ocorrencias de formula e valor
- Hashes declarados da ENTREGA_K10 (8 arquivos da minha lente: todos batem) e tabela de hashes dentro da ENTREGA_K09 (6 de 7 nao batem mais)
- Mapa de Rotas: consultar juno, carimbo, incremento; ver coma.dephasing_previsao_trancada e infra.github.publicacao_fora_da_cadeia_h0dn_12nov (existe); nada registrado
- Scripts meus em C:\Users\rotol\AppData\Local\Temp\claude\b4ca26c934d2167f\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v412_exame_codex_kimi\Q2: conta_q2.py, scan_c.py, datas_q2.py, busca_tex.py
- Nao consultei o kernel (nao havia afirmacao de ausencia a conferir); nao abri dado observacional, nao rodei modelo, nao abri bytes da fala do operador; nao reabri H0DN x BG1

