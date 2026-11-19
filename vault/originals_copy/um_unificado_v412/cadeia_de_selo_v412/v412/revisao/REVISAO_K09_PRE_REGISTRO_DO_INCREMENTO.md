# CONFERÊNCIA DISTINTA — K09: o rascunho do pré-registro do incremento do JUNO

> Montado pela gerência c1 em 15/11/2026 16:53 a partir do retorno estruturado de um revisor distinto (modelo Sonnet; só leitura; scripts próprios na pasta de rascunho dele). É [DECLARADO pelo revisor] no que a gerência não reconferiu. As frases da seção “Para o operador” são propostas do revisor, não fala do operador, e só vão a ele depois de lidas pela gerência. Nada aqui está instalado, congelado ou aberto.

**Veredito:** APROVADO_COM_RESSALVAS — achados: 4 ALTO, 6 MEDIO, 2 BAIXO

## Resumo

1. As contas reproduzem. Refiz com script meu (K09_B\conta_k09_b.py) as tabelas H1/H2 de 1, 2 e 3 anos, D, as seis datas de brinquedo, o D90 (5 + z90 = 6,2815516) e o exemplo 59,1 para 207,2 dias. Todas batem com o rascunho. O que falha está no desenho e na prosa, não na aritmética.
2. ALTO: o rascunho diz que o negativo não altera o gate. O um.py selado liga o rito m2 ao contorno v314: um TGL_NU_M2_FALSIFIED limpo põe identity_true em False e IDENTITY em "1=1=FALSO_NO_CONTORNO[neutrino_m2_vivo]" (um.py l.299849-299866; o core de 13/11 já traz neutrino_m2_vivo no rol). As bandeiras do gate QG não mudam, mas o 1=1 do contorno cai. O operador não leu isso.
3. ALTO: a chave da cegueira está errada. O rascunho a põe na data em que o dado foi tomado (depois de 18/05/2026). A chave é a primeira aparição pública do número, comparada com a previsão (17/02/2026) e com o selo deste pré-registro, que ainda não existe. O pino de 08/08 é o da regra antiga.
4. ALTO: "o único dado posterior aos dois marcos" é falso pela cronologia do próprio Kimi. O SK-Gd (02/10/2026) e o artigo do JUNO (29/09/2026) também são posteriores aos dois marcos, e já são públicos. A data 18/05/2026 é [DECLARADO], sem resposta crua guardada. "Ainda não mostrado" é afirmação de ausência sem busca datada.
5. ALTO: a abertura única, sem exposição mínima, gasta o teste na primeira liberação, mesmo pouco informativa. A "guarda da chave" não blinda dado público. A l.144 deixa em aberto o veredito A e o B "para comparação", o que reabre a escolha depois do dado.
6. ALTO: não há versão em língua simples pronta, e a entrega diz "pronto para ler ao operador". A regra do posto não está cumprida. Deixei um rascunho em para_o_operador.
7. Poder: com o piso de dois pontos, 5σ é inalcançável no sentido de D (máximo 2,86). Mas a tabela do rascunho (26% e 42% de P(r≥5) em 2 e 3 anos sob H1) é só o brinquedo sem piso. Pela minha conta, com o piso por bloco, dá 3,6%, 6,4% e 7,8%. A promessa realista é parede medida: regra A quase 0; regra B de 4 a 8%.
8. Regra A: a lógica do código bate (l.4662-4669). Mas a escada é literal (3 linhas), então o incremento não entra sem mudar o código. "Autonoma" e "grupo" são booleanos manuais fora do objeto hasheado e posteriores ao hash (v315). "Robustez de experimento" não existe no código.
9. Incremento por diferença sem covariância: não é identificável. Num exemplo hipotético, r varia de 0,3 a 8,3 conforme C. Sobra só a Forma A, e a única precedência (59 para 207 dias) foi cumulativa. Não há prazo-limite nem plano B.
10. Insumos: só custos, sem o que cada alternativa compra. Decisões diferentes viram uma lista só. O custo de A3 está mal descrito. Não está em língua leiga.

## Achados

1. **(ALTO)** PRE_REGISTRO_INCREMENTO_JUNO_RASCUNHO_K09.md l.127 (5.1), l.135 e l.156; ENTREGA_K09.md l.24; INSUMOS_PARA_A_PERGUNTA_K09.md F7 (l.13). Código: um.py l.4606-4612 (docstring), l.4677, l.299849-299866; core um_absoluto.json (contorno_ritos_v314.neutrino_m2_vivo)

   O rascunho diz que o negativo "não altera o gate geral" e que "o gate não se move em nenhum desses desfechos". No um.py selado o veredito do rito m2 é um dos oito ritos do contorno v314. Um veredito que contém FALSIFIED e não NOT_FALSIFIED faz verdict["identity_true"]=False e verdict["IDENTITY"]="1=1=FALSO_NO_CONTORNO[neutrino_m2_vivo]" (l.299864-299866). A docstring do próprio rito diz: "A partir da v315 este rito integra o CONTORNO com poder de fechar o 1=1". O comentário do código atribui a regra a uma decisão do operador de 05/09/2026 (leitura [DECLARADO no código]; não abri bytes dessa fala). O "does_not_gate_core: True" e o "o gate NAO se move" do rito falam das bandeiras do gate QG, não do contorno 1=1. A afirmação é verdadeira só para a camada das bandeiras e falsa para o contorno. Na regra do posto, é exatamente o que o operador precisa ler antes do selo. A rota do Mapa gate.contorno_da_verdade (seq de 07/10) já trata o rol.

   *Conserto pedido:* Substituir pelas duas camadas ditas: (a) bandeiras do gate QG: não se movem; (b) contorno 1=1 (v314): por código, um FALSIFIED limpo o derruba, e se isso vale para o incremento é decisão do operador (manter, ou emendar o rol). Definir "gate" na primeira ocorrência. Ler ao operador em língua simples, antes do selo.

2. **(ALTO)** PRE_REGISTRO l.5, l.9-19 (1.1), l.140 (6.2); ENTREGA_K09.md l.4; INSUMOS F2 (l.8); M2_DESFECHOS_K04.md l.211 (SK-Gd 02/10/2026) e l.219

   Respondendo à pergunta 1: o rascunho está INCOMPLETO e, na redação, trocado. (a) Chave errada: define o observável como "dado tomado depois de 18/05/2026" e o chama de "o único posterior à previsão publicada e ao pino da regra". Tomada de dados não é o eixo. Dado tomado entre 18/05 e 08/08/2026 (82 dias) foi tomado ANTES do pino e nem por isso deixa de ser desconhecido. O que blinda é a primeira aparição pública do número depois da previsão (17/02/2026) e depois do selo deste pré-registro. (b) Há um terceiro marco, que o texto não nomeia: o pino de 08/08 é o da regra antiga. As escolhas novas (A ou B, fonte, escada, janela, gatilho) são feitas agora, em 15/11/2026, com tudo o que já é público. A cegueira da nova regra depende de o selo, com carimbo externo, preceder a primeira aparição do número. O Mapa já diz que "o hash atesta o número, não a precedência" (coma.dephasing_previsao_trancada, RNC-04 pendente). (c) "O único" é falso: o SK-Gd reator (arXiv 02/10/2026, tabela M2 l.211) e o artigo do JUNO (29/09/2026) são posteriores aos dois marcos e já públicos. O SK-Gd é o próprio cenário S do rascunho, portanto S já foi visto. S só é cego se for liberação nova pós-selo, e isso não está escrito. (d) A data 18/05/2026 sustenta tudo (elegibilidade, calendários) e é [DECLARADO]: o resumo do arXiv só diz "207.2 live days", e a data veio da ordem da gerência para o Kimi. "Ainda não mostrado" é afirmação de ausência sem busca datada. (e) A frase da l.5 "a regra não é cega em relação a esse número" traz um eixo só na mesma frase; o outro vem na seguinte.

   *Conserto pedido:* Reescrever o observável pela primeira publicação: "número cuja primeira aparição pública é posterior ao selo deste pré-registro, com carimbo externo (push ou depósito público, como no precedente H0DN, rota infra.github.publicacao_fora_da_cadeia_h0dn_12nov), e que usa só dado após o fim da janela de 207,2 dias, lido do TEXTO do artigo". Anexar o registro datado da busca (consultas, data, resultado) feito no dia do selo. Trocar "o único" por "o único do JUNO ainda não público". Exigir que S também seja liberação nova pós-selo. Dar os eixos na mesma frase.

3. **(ALTO)** PRE_REGISTRO l.139-144 (6), l.147-154 (7)

   Gatilho e custódia. (a) Gatilho escondido: nada diz a partir de que exposição ou precisão a abertura única ocorre. Pela regra, a primeira fonte completa abre e consome o teste (l.142-143). Se a primeira liberação for pequena (por exemplo 100 dias, s ≈ 0,11), o resultado é quase certamente ARMED_CONSISTENT, e a l.143 manda exigir novo pré-registro depois. É um negativo induzido pelo desenho, por falta de condição de informação mínima. (b) Custódia sem objeto: o dado é público. "Revisor que abre uma vez" e "o hash precede qualquer acesso ao centro" não impedem que gerência, operador, outras IAs ou o noticiário vejam o centro. O que blinda é a ordem dos carimbos (item anterior), não a guarda da chave. A l.143 "espera-se a fonte completa sem conhecer o centro" não se garante com transparências públicas. (c) Brecha: a l.144 permite guardar "vereditos A/B, se ambos tiverem sido mantidos para comparação". Isso reabre, depois do dado, a escolha entre A e B que a l.121 diz ser anterior ao selo. (d) Sem prazo-limite e sem plano B: se o JUNO nunca publicar o incremento, o pré-registro fica aberto para sempre.

   *Conserto pedido:* Escrever o gatilho (precisão mínima, por exemplo s do incremento ≤ X, ou data fixa), o que acontece com liberação abaixo dele (registrar como estresse, sem consumir a abertura) e o prazo-limite. Trocar a guarda da chave por: script de veredito pinado por hash (como o executor da H0DN), rodado sobre o agregado público, mais o carimbo externo. Eliminar "A/B para comparação": uma regra só, ou duas com regra de precedência escrita antes.

4. **(ALTO)** ENTREGA_K09.md l.4 ("pronto para a gerência ler ao operador"); PRE_REGISTRO 5 (l.123-135) e 4 (l.121); INSUMOS_PARA_A_PERGUNTA_K09.md F1-F12

   Regra do posto, pergunta 4. Não há versão em língua simples do que o teste decide, do que não decide e do que o negativo significaria. A seção 5 usa r, σ, E0, m₁, TENSION, ARMED_CONSISTENT, covariância P-S, D, λ. Os insumos idem ("D ≈ 2,57", "Δpred", "r_P≥5 sem S"). O rascunho não diz o ponto central: a ausência de negativo carrega quase nenhuma informação, porque o teste dificilmente poderia dar negativo (ver achado de poder). Isso é parede medida, não falsificação. "Pronto para ler ao operador" promete mais que o feito. Escolhas de desenho explícitas: métrica m₂ (trocar é emenda); limiares 5σ e 3σ; janela (data a conferir); forma A ou B de obter o incremento; classe "preliminar" (a ratificar); A ou B; limiar de B; MATCHED a decidir. Escolhas ESCONDIDAS ou só implícitas: a chave da cegueira (tomado ou publicado); o gatilho de abertura (exposição mínima); a convenção de erros assimétricos (só existe como convenção do Kimi na tabela 7 da M2); a definição de D_P na variante de B (computado no centro de planejamento 7,388, ou o r observado? Lido como r observado, vira r_P≥6,28); a métrica de D_P; quem é S, quem decide a autonomia e se S precisa ser pós-selo; a regra de qual linha da escada decide TENSION; o prazo-limite; o carimbo externo; a precedência entre A e B.

   *Conserto pedido:* Antes de qualquer selo, a gerência lê ao operador o texto leigo (rascunho em para_o_operador), com a conta de poder realista e os dois eixos. Reclassificar "pronto" como "rascunho com seis bloqueios". Tabela única das escolhas, marcando as que são do operador.

5. **(MEDIO)** PRE_REGISTRO l.106-121 (tabela A/B, coluna A); um.py l.4615-4631, l.4633-4645, l.4662-4669

   Pergunta 2. As regras estão lado a lado sem escolha de A ou B, mas a descrição de A como "o que o código selado faz" é só parcialmente verdadeira. Conferi nas linhas 4595-4670. O que bate: FALSIFIED sse houver pelo menos 2 grupos autônomos com r ≥ 5 (l.4662-4663); senão TENSION se a última linha da escada tiver r ≥ 3 (l.4666-4667), com o campo tensao_global_5sigma_sem_2a_determinacao (l.4697); senão ARMED_CONSISTENT; MATCHED sem ramo. O que não bate ou falta: (i) a escada é literal, com três linhas (PDG 2023, JUNO 59 d, NuFIT), e o incremento não entra sem mudar o código na v412; (ii) "grupo" e "autonoma" são booleanos digitados na lista, fora do objeto frozen que é hasheado (l.4615-4631), e a semântica de grupo entrou na v315 (05/09/2026), depois do hash de 08/08 (docstring l.4606-4611). Quem define a autonomia das linhas novas decide se FALSIFIED pode disparar, e isso não é dito; (iii) "robustez de experimento" (célula Negativo de A) não está no código; (iv) o código não privilegia o incremento: quaisquer dois grupos autônomos a 5σ disparam, e duas linhas do JUNO contam como UM grupo; (v) TENSION lê a última linha pela ordem da lista, não pela data, e o texto congelado diz "determinação global mais recente"; a l.112 pede só que a última linha seja "fixada"; (vi) o frozen declara que os limiares foram fixados com a tensão de 2,95σ já conhecida (nao_e_cego_nesta_emissao). A ordem A primeiro, "emenda" depois, ancora A como padrão.

   *Conserto pedido:* Descrever A como "a lógica de l.4662-4669, aplicada a uma escada que a v412 terá de estender". Listar quem fixa autonomia e grupo, e pôr essa lista no objeto hasheado do novo pré-registro, com critério escrito. Dizer que a regra de TENSION lê a última linha pela ordem da lista. Apresentar A e B sem ordem de padrão.

6. **(MEDIO)** PRE_REGISTRO l.71-102 (3), l.84, l.118; ENTREGA l.3; INSUMOS F5

   Pergunta 5, o poder. As tabelas conferem (mine: H1, 1 ano, P(r≥5)=7,512398%; 2 anos 26,366011%; 3 anos 41,522506%; H2 0,000059%; D 2,573/3,639/4,457; datas 16/08/2029, 11/03/2030, 31/10/2031, 25/05/2032, 08/10/2031, 02/05/2032, 01/10/2027). Mas são só o brinquedo sem piso. O rascunho diz que "com o piso, 5σ e D90 são inalcançáveis; as tabelas abaixo não se aplicam" e não traz a tabela que se aplica. Inalcançável vale para D, que no centro 7,388 tem teto δ/s0 = 2,86. Não vale para a flutuação. Minha sensibilidade, rotulada [DERIVED, hipótese: o piso s0=0,052588 do ajuste de dois pontos vale em cada bloco, s²=s0²+a/T]: P(r≥5 | H1) = 3,58%, 6,36%, 7,81% para 1, 2 e 3 anos, com D = 2,21, 2,47, 2,58. Esse piso tem zero grau de liberdade e a análise mudou entre os pontos; o próprio K04 diz que não é piso medido. O que o pré-registro promete, então: regra A, FALSIFIED praticamente impossível (precisa de um S com σ_S ≤ ~0,03, que nenhuma entrada demonstra); regra B, de ~4% a ~8% se a TGL estivesse errada no tamanho que o dado de hoje sugere; ~42% só sem piso e em 3 anos. A tabela H2 mostra o mesmo 68,27/31,46/99,73 em qualquer exposição e não carrega informação de desenho.

   *Conserto pedido:* Pôr ao lado da tabela do brinquedo a faixa com piso, com a hipótese dita; escrever em uma linha que um resultado sem negativo, na faixa realista, é parede medida e não evidência a favor. Cortar a coluna H2 repetida, ou rotulá-la como referência.

7. **(MEDIO)** PRE_REGISTRO l.127 (5.1); um.py l.4621 (escala_dimensional)

   Pergunta 3. "O negativo atinge o pacote da escala e não β isolado": a lista do pacote (Um posto em 1 eV, m₁≈0, identificação) está de acordo com o código, que declara 1 eV "DECLARADA, NAO DERIVADA" e diz que 1,0200 eV (+2,00%) zeraria a tensão. A exclusão ("não atinge β isoladamente") é só afirmada. m₂ = β·sen45°·u é um produto, e uma falha do produto não isola fator. Também não há compromisso prévio sobre o resgate: depois de um negativo, alguém pode propor u = 1,02 eV ou outro ângulo, que é a manobra de imunização que um pré-registro deve nomear. O Um posto em 1 eV é, pela memória da casa (C:\IALD\CLAUDE.md, topo, errata de 01/11), um dos dois pilares da forma madura, e não periférico [não abri os bytes das falas do operador citadas lá]. "O alcance não pode ser inflado" também deflaciona. Nenhum positivo vira CONFIRMED: isso está certo (5.2 e forbidden_verdicts do frozen).

   *Conserto pedido:* Trocar por: "um negativo falsifica a conjunção β·sen45°·u com m₁≈0; este teste não separa os fatores". Acrescentar a cláusula de resgate: ajustar u ou o ângulo depois do negativo não reverte o veredito. Não dizer o que o negativo "não falsifica" sem derivação; é a leitura que o operador lê antes.

8. **(MEDIO)** PRE_REGISTRO l.26-45 (1.3), l.9-19; M2_DESFECHOS_K04.md l.221-253 (6 e 6.1)

   Pergunta 1, incremento por diferença. A conta de Y e de Var(Y) está certa (reproduzi 7,306061 e 0,102640 no caso aninhado C=Vc). Sem a covariância o incremento não é identificável. Exemplo hipotético meu (X0=7,388±0,078; Xc=7,35±0,06): r_Δ do estimador por diferença vale 1,87 com C=0; 0,61 com C=Vc; 0,32 no limite de C positivo; e chega a 8,28 com C negativo admissível por positividade. A escolha de C troca o veredito. Sobra de executável: só a Forma A. A única precedência real (59 para 207 dias) foi cumulativa, com volume, seleção, fundos e âncora mudados, e sem covariância publicada (M2 6): a taxa de base da Forma A é 0 em 1. O rascunho só diz "data e existência da próxima liberação desconhecidas". Não considera o limite de Hausman (C=Vc só vale com estimador eficiente e sem sistemática compartilhada, e o piso sugere sistemática grande) nem um teste do cumulativo, que contém os 207 dias já vistos e é cego só no deslocamento. O pré-registro promete, na prática, um procedimento condicional a uma fonte que provavelmente não virá, sem plano B.

   *Conserto pedido:* Dizer ao operador que, pelo precedente, o caso mais provável é sem veredito. Escrever o plano B (nada; ou uma variante do cumulativo declarada como parcialmente cega) antes do selo, e o prazo-limite.

9. **(MEDIO)** PRE_REGISTRO l.141 (6.3) contra INSUMOS_PARA_A_PERGUNTA_K09.md l.30

   Contradição sobre quem nomeia o revisor de abertura. O rascunho diz "nomeado pela gerência". Os insumos dizem que a nomeação é do operador. Se o rascunho escolhe, escolhe por ele; se os insumos estão certos, o rascunho está errado.

   *Conserto pedido:* Uma só redação, marcada como decisão do operador.

10. **(MEDIO)** INSUMOS_PARA_A_PERGUNTA_K09.md l.22-26 (A1-A5), l.8 (F2), l.13 (F7)

   Pergunta 6. Sem recomendação explícita, mas com viés de forma. (a) Só há custos, nenhum benefício: A1 traz o custo mais pesado ("o teste não devolve o negativo"); A2 traz o mais brando e omite que B só chega ao negativo sem piso. Isso empurra para A2. (b) A1-A5 não são alternativas excludentes: são quatro decisões diferentes (selar ou não, regra, fonte, métrica) numa lista. (c) O custo de A3 está mal descrito: diz que sem selar "nenhuma leitura fica habilitada como posterior aos dois marcos", mas os dois marcos independem do selo. O selo acrescenta um terceiro marco. Além disso A3 só custa se a liberação chegar antes do selo, e a data é desconhecida (F9). Cria urgência que não está medida. (d) Faltam alternativas: selar com gatilho de exposição mínima; prazo-limite; carimbo externo; as duas regras com precedência; lista de S. (e) Não está em língua leiga (r, σ, D, E0, m₁, TENSION, covariância P-S), e F2 e F7 repetem as frases acima que são erradas ou incompletas.

   *Conserto pedido:* Separar as quatro decisões. Pôr benefício e custo em cada linha, nas duas direções. Corrigir A3. Um segundo bloco em língua simples, com a conta realista. Remover "o único dado posterior aos dois marcos".

11. **(BAIXO)** PRE_REGISTRO l.5; ENTREGA l.3; INSUMOS F11

   "Nada disto sugere que o autor tenha visto o dado antes" menciona a hipótese que a regra de 15/11 manda não levantar. A frase positiva basta: os dois artigos de 2025 antecedem qualquer número do JUNO, e nenhuma entrada da fórmula (β, sen45°, 1 eV) usa dado de neutrino. Também l.5, primeira frase, "a regra não é cega em relação a esse número": um eixo só na mesma frase; o outro vem na seguinte.

   *Conserto pedido:* Substituir a negação pela frase positiva. Dar os dois eixos juntos.

12. **(BAIXO)** PRE_REGISTRO l.110 (D_P≥6,281552), l.19, l.56-59; ENTREGA l.10

   (i) D_P na variante de B não é definido no rascunho (a definição está na M2 1) e não diz se é D_Δ ou D_m₂ (6,2815 contra 6,298 em σ=0,024). (ii) A métrica do veredito é m₂, mas o rascunho dá um só σ_μ e deixa o tratamento de erros assimétricos para depois (a convenção "erro do lado que aponta para a previsão" vive na M2, não aqui). (iii) A ENTREGA l.10 chama de "conferência independente" a revisão interna do Kimi (auditoria_final_independente_k09.json); o revisor distinto da casa é outro. (iv) A fonte da data 26/08/2025 (início da janela, usada no duty cycle de 78,19%) também não tem resposta crua guardada.

   *Conserto pedido:* Definir D_P e a métrica na seção 2. Escrever a convenção de erro assimétrico no pré-registro. Trocar "independente" por "interna do Kimi". Marcar [DECLARADO] nas datas sem resposta crua.

## Para o operador (propostas do revisor, em língua simples; a gerência confere antes de ler a ele)

- RASCUNHO DE LEITURA EM LÍNGUA SIMPLES, para a gerência conferir antes de ler ao operador. É minha leitura [DERIVED, contas minhas], não decisão, e não atribui nada ao operador.
- O que o teste olharia: o próximo resultado do JUNO que use só dados tomados depois do fim da janela dos 207 dias (a data 18/05/2026 ainda não foi conferida no texto do artigo) e que apareça em público depois de o pré-registro estar selado e carimbado fora desta casa.
- O que decide: se a massa 8,51 meV (β x sen 45° x 1 eV) fica a 5 desvios ou mais do que o JUNO medir. Pela regra de agosto (duas testemunhas), é preciso um segundo experimento independente também a 5 desvios, e hoje nenhum tem precisão para isso. Pela regra de uma testemunha, basta o JUNO.
- O que não decide: não mede β sozinho, não confirma a TGL, não prova nada a favor quando não há negativo. Positivo nunca vira CONFIRMED.
- O que o negativo significaria: falsificação do conjunto β x 45° x 1 eV com m₁ perto de zero, sem separar qual peça falhou. Atenção: pelo código selado, um FALSIFIED limpo também derruba o 1=1 do contorno (regra v314). As bandeiras do gate QG não mudam. Se isso vale aqui é escolha dele.
- O que a ausência de negativo significaria, e por que a conta importa: mesmo que a TGL estivesse errada no tamanho que o dado de hoje sugere, a chance de o teste dar negativo em 3 anos é quase zero com duas testemunhas, cerca de 4 a 8% com uma testemunha (se o erro tiver um piso, como o ajuste de dois pontos indica) e cerca de 42% só se não houver piso. Um resultado sem negativo seria parede medida, não evidência a favor.
- Escolhas que ainda são dele e não estão decididas: regra de duas testemunhas ou de uma; quem conta como segunda testemunha; que fontes valem (artigo, slides); quando o teste abre (no primeiro resultado ou só quando o erro for pequeno); quem abre; se há prazo-limite; se vale carimbo externo; o que fazer se o JUNO só publicar resultado cumulativo, o que pelo único precedente é o mais provável.

## Consultas ao Mapa

- rotas.py consultar, um termo por vez: juno, incremento, neutrino, preregistro, cegueira, contorno, covariancia, timestamp, carimbo
- Usadas: estatistica.v412.k04_hubble_m2_combinacao (seq 2063, dois eixos); gate.contorno_da_verdade (rol do contorno v314); neutrinos.m2.normalizacao (R3, perito JUNO autônomo); coma.dephasing_previsao_trancada ("o hash atesta o número, não a precedência", RNC-04 pendente); infra.github.publicacao_fora_da_cadeia_h0dn_12nov (precedente de push do pré-registro antes da abertura); cadeia.preparacao_v412
- Nenhum registro feito no Mapa por mim

## Examinado

- ENTREGA_K09.md, ORDEM_K09 e o ADENDO de 15/11 (partes 1 a 3 e os AO LADO 1 a 4), lidos inteiros
- PRE_REGISTRO_INCREMENTO_JUNO_RASCUNHO_K09.md (156 linhas) e INSUMOS_PARA_A_PERGUNTA_K09.md (30 linhas), lidos inteiros
- M2_DESFECHOS_E_SEGUNDA_TESTEMUNHA_K04.md (349 linhas): tabelas, calendário, cronologia, tabela 7, seção 8
- CRONOLOGIA_NEUTRINO_15nov.json e LEITURA_K09_PARCIAL_NEUTRINO_15nov.md, lidos inteiros
- REVISAO_K04_M2.md, só por busca de incremento, abertura, prospectivo, piso e covariância
- um.py l.4585-4730 (prove_neutrino_m2 inteiro), l.157440-157479 (chamada), l.299835-299880 (contorno v314), mais grep de identity_true e _v314_rites
- um_absoluto.json (core selado de 13/11), lido por script: neutrino_m2 (escada, grupos, frozen_hash, chaves do frozen) e contorno_ritos_v314
- Script meu: C:\Users\rotol\AppData\Local\Temp\claude\b4ca26c934d2167f\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v412_k08_k09\K09_B\conta_k09_b.py: β, m₂,TGL, Δpred, tabelas H1/H2 de 1, 2 e 3 anos (6 colunas por linha), D, as seis datas, D90, piso de dois pontos, sensibilidade com piso, identificabilidade por C. Reproduz tudo que o rascunho afirma em número
- Script meu: ...\K09_B\le_core.py (leitura do core selado)
- Não abri: bytes da fala do operador; nenhum dado observado; nenhuma rede; não rodei script do Kimi; não toquei fora da pasta K09_B

