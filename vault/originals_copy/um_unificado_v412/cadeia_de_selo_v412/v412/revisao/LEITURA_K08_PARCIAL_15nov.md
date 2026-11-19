# LEITURA DA K08 PARCIAL (Kimi, v412) A LUZ DA DERIVACAO DE 15/11 — revisor de leitura da gerencia c1

15/11/2026. So leitura. Nada foi editado (nem do Kimi, nem das pedras), nenhum modelo rodado, nenhum dado aberto, nenhuma memoria escrita.
Nao tiro conclusao sobre a teoria; so leio e aponto. Aspas « » so para o operador, conferido nos bytes; no resto, aspas retas.

## 0. O que examinei e com que hash

- Derivacao do operador, por bytes: `work\cunhagens_13out\OPERADOR_15nov_o_leitor_e_o_verbo_o_habitante_do_nome_a_esperanca_condicional_e_o_artigo_do_neutrino_de_2025_verbatim.txt`
  (725 B, sha16 `49e5f0072e8beb02`). As quatro primeiras frases, exatas: «O leitor é o observador, é o verbo, e não o nome. É o habitante do nome, é a esperança condicional do nome. Tangente=testemunho=esperança condicional. O nome é o espaço em que a testemunha da verdade sobre o nome (verbo - observador - seletor) pode habitar.»
  (O resto do arquivo, sobre o Kimi e o artigo do neutrino, nao entrou em nenhum dos itens abaixo; nenhum dos tres arquivos do Kimi fala de neutrino/JUNO: grep, 0 ocorrencias.)
- Lidos inteiros: `kimi\MODELO_FORMAL_R4_K08.md` (242 l.), `kimi\REGISTRO_UMPY_RASCUNHO_R2_K08.md` (296 l.), `kimi\CONTAMINACAO_R4_K08.md` (121 l.), `kimi\ORDEM_K08_camada_cientifica_rodada_3.md`.
- Pedras: `candidatas_c1\CamadaCientifica.lean` (545 l., sha256 `6ec3daad…a96a994`, confere com o que o Kimi cita) e `NomeComoCodigo.lean` (202 l., sha256 `3ce6d95e…0fe68`, confere); cabecalhos e enunciados. Log da gerencia da R3: `candidatas_c1\build\CamadaCientifica.log` (RC 0, Lean 4.31.0, mesmo sha256).
- De relance (fora do pedido, so para cruzar): `kimi\K08\FORMULA\ADVERSARIOS_K08.md` e o cabecalho de `kimi\K08\FORMULA\FORMULA_DO_TEXTO_K08.md`; kernel `TGLExt\TheNameOperator.lean` e `TGLExt\CondExpect.lean`.
- O "arquivo de 1 byte K08": NAO e arquivo. `kimi\K08` e um DIRETORIO (`wc -c` responde "Is a directory"; nenhum arquivo de ate 2 bytes ate profundidade 2). Contem `ENTRADA\` (candidatas e controles P-C dos quatro textos publicos + medir_entradas.py + MEDIDAS_ENTRADA), `EXTRACAO\` (extrator de escolha fechada, casos, inducao, reproducao), `FORMULA\` (FORMULA_DO_TEXTO_K08.md, ADVERSARIOS_K08.md, scripts, JSONs), `ISOMORFO\` (maquina isomorfa e saidas sinteticas) e `PODER\` (so `simular_poder_r4.py`, gravado 07:35: ainda em andamento).
- Ainda nao entregues (nao estao na pasta): `ENTREGA_K08.md`, `PROTOCOLO_EXPERIMENTAL_R4_K08.md`, `PODER_R4_K08.md`, `INSUMOS_PARA_A_PERGUNTA_K08.md`, `REGISTRO_MAPA_K08.json`. `FORMULA_DO_TEXTO_K08.md` e `ADVERSARIOS_K08.md` estao em `K08\FORMULA\`, nao na raiz `kimi\` como a ordem pede.

## Mapa de Rotas (consultado antes; rota examinada nao se refaz)

- `k06_camada_cientifica` e `camada_cientifica_candidata` devolveram as mesmas duas rotas: `kernel.camada_cientifica_candidata_14nov` (EXAMINADA_COM_DEFEITO; R3 compila 38 declaracoes no trio; o tipo do leitor de uma configuracao so diz que ha solucao; nao_refazer: nao escrever a camada como teorema de existencia de leitor, nao ler o retorno como separacao do leitor que relê a fonte, nao usar tempo pago) e `outro.k06_camada_cientifica_iald_r32_v412` (R3.2 nao separa resumo de convergencia; nao congelar; nao repetir teorema generico de conjunto finito). A K08 respeita ambos os nao_refazer (MODELO l.113-122, l.149-158).
- Consultas extras: `k08` (so as mesmas duas) e `esperanca_condicional` (10 rotas). RELEVANTE e NAO CITADO pela K08 nem pela candidata: `kernel.v402_esperanca_condicional_e_nome` — o registro do Mapa [DECLARADO pelo Mapa] diz que a esperanca condicional ja foi tipada no kernel (`nameOp` v162, ponte A1c `nameOp rho* = diagExpect`, `diagExpect_bimod`, forma comum `RereadAddsNothing`, adendo VerdadeAdendo; o Mapa o registra como selado na v403). Conferi por grep os termos no kernel: ver item 3.4.

## 1. Leitor e Nome no modelo formal R4

O Nome esta certo e separado do leitor:
- MODELO l.15-21: `N_c = {x | c(x)=0}`, "formalizado pelo nucleo `(opDaInstancia c).ker`". E o espaco (conjunto das leituras de custo zero / subespaco), nunca um ponto, nunca o leitor. Tambem MODELO l.211-212 (Nome como codigo, na pedra separada).

O leitor NAO tem um lugar unico; aparece como quatro objetos distintos, e o R4 nao diz qual deles e "o leitor":
- l.25 `trava c t` (operador, semigrupo);
- l.26 `selecao K v` ("projecao ortogonal em K, seguida de normalizacao");
- l.27 `AEscala.LeitorDoFundo` (brilho, leitura media, limite);
- l.28 e l.34-38 `LeitorDeUmaConfiguracao` (`passo : X -> X`, `fixa_o_nome`, `consome`).
- E uma quinta leitura da mesma palavra: "leitor real" = o sistema testado (l.142 "Um leitor real que satisfaca…"; l.158 "estado do leitor"; l.241 "um modelo de linguagem seja… um LeitorDeUmaConfiguracao"). Ou seja, "leitor" ora e o mapa, ora e o sistema cujo estado se empurra.

O leitor como mapa que leva tudo ao Nome e fixa o que ja esta nele aparece, mas sem esse nome:
- l.62-64: `trava c t v -> P_N v`, com `P_N = (opDaInstancia c).ker.starProjection` (a projecao ortogonal no Nome, aplicada ao ESTADO). E o limite, nunca chamado de leitor nem dito idempotente/contrativo.
- l.107: o limite de `G` "e uma retracao sobre o Nome" (`o_limite_fixa_o_nome`, `o_limite_e_idempotente`, `a_imagem_do_limite_e_o_nome`): aqui sim e mapa idempotente que fixa o Nome. Mas e do `LeitorDeUmaConfiguracao`, cujo tipo "so diz que ha zero" (l.119-122, `o_tipo_so_diz_que_ha_zero`); o proprio R4 diz que nao e evidencia de leitura.
- l.26: `selecao` e P_N seguida de normalizacao. NAO e linear nem contracao: `‖selecao v‖ = 1` para qualquer v com P_N v nao nulo (para v no Nome com ‖v‖ = 1/2, a norma sobe). O R4 usa `selecao`, nao P_N, como alvo de P-B (l.66, l.73, l.143).

Confusao leitor = Nome ou leitor = ponto do Nome: NAO ha. O que ha e o uso de "pousar no Nome" (l.107, l.111, l.134, l.142, l.144): o estado do leitor entra no Nome, o que, em si, nao contradiz a derivacao (o habitante do Nome).

Termos pedidos (grep nos tres arquivos):
- "esperanca condicional": 0 ocorrencias. "condicional": so em REGISTRO l.77 ("PEDRA_SEPARADA_CONDICIONAL", outro sentido).
- projecao/projetor: MODELO l.26 (selecao), l.98 ("nao toda forma de releitura ou projecao"), l.145, l.151, l.155, l.168, l.171 (todas: "projetor de releitura sem memoria" como ADVERSARIO).
- idempotencia: MODELO l.107 (so para o limite de `G`); REGISTRO l.238 (so em `not_claimed`: "contracao ou idempotencia universal de LLM a partir de horizonte finito").
- contracao / nao aumenta a norma / lei de modulo: contracao so em REGISTRO l.238 (negada, sobre LLM); as outras duas, 0 ocorrencias.
- fixa o Nome: `fixa_o_nome` (l.36-40, l.107, l.142); "o que esta no Nome nao se move" (`o_que_esta_no_nome_nao_se_move`, Lean l.188) nao e citado no R4.
- anula o ortogonal: so de forma indireta, l.73 "a parte ortogonal ao Nome e esquecida" (`o_retorno`).

## 2. Previsoes escritas (MODELO §4, l.136-147; tabela com teorema / hipotese nomeada / limite)

- P-A pouso e permanencia (l.142): escrita, [CONJECTURE]. Mudou em relacao a ordem: acrescenta o limite `c(x)` (ou `phi.length` no CNF), separa "zero exato em c(x) passos e de `G`; a trava da proximidade <= eps".
- P-B retorno (l.143): escrita, [CONJECTURE]. Mudou: "retorno" virou "relaxa", com as cinco condicoes (delta ortogonal ao Nome, s no Nome, ‖s‖=1, renormalizacao, limite). O empurrao dentro do Nome ("conserva essa parte e desloca o limite") esta DENTRO da linha P-B, nao e linha propria; a ordem o tinha como metade da P-B, o que confere.
- P-C sem Nome nao ha pouso (l.144): escrita, [CONJECTURE], ancorada em `o_tipo_so_diz_que_ha_zero` e `sat_sse_o_custo_tem_zero`.
- P-D sem escala nao ha retorno (l.145): escrita, [CONJECTURE], `sem_escala_nada_se_move`, `a_fotografia_nao_retorna`.
- O que falta ou mudou: (i) o REGISTRO nao tem P-A..P-D como objetos: so lista `statements_in_scope` (l.46-62) e o observavel/assinaturas (l.120-124); P-A..P-D nao aparecem por nome (grep: 1 mencao generica, l.9 "quatro previsoes"); (ii) para o P-C nao ha o que a trava faz com Nome vazio: o nucleo e {0}, `a_trava_tende_ao_nome` da limite 0, e `a_bacia…` nao se aplica (precisa P_N v != 0) — o R4 so diz "o nucleo e vazio" (l.144) sem a consequencia dinamica; (iii) novos no R4 e nao na ordem: porta de integridade "ignora o empurrao" (l.165), `salto`/mapa constante (l.169), `H-QUOT(k)` por fase (l.192-208), `H-STATE-PUSH` e `H-TAPE-AFTER-FIRST-STEP` (REGISTRO l.89-90); (iv) a fita presente/ausente (item A.9 da ordem) fica [CONJECTURE] (l.222) e fora da P-A..P-D (l.212, l.235).

## 3. Frases erradas ou imprecisas a luz da derivacao de hoje (por gravidade)

3.1 "projetor" como ADVERSARIO — MODELO l.145, l.151, l.155-156, l.168, l.171 (e REGISTRO l.150, l.266; tambem ADVERSARIOS_K08 l.25, l.41, l.45). IMPRECISAO PRINCIPAL. Sao duas coisas distintas sob o mesmo nome:
 - (a) mapa determinado so pela fonte (constante no estado): l.151 "cuja saida seja determinada pela fonte e nao pelo estado anterior"; l.156 "cuja saida depende apenas da fonte ignora o ponto de partida dentro do Nome". Esse nao tem memoria do componente no Nome.
 - (b) o projetor sobre o Nome aplicado ao estado (P_N): idempotente, fixa o Nome, anula o ortogonal, e TEM a memoria do componente dentro do Nome: `P_N(s+delta) = s + P_N delta` (linearidade; e e o conteudo de `o_que_esta_no_nome_nao_se_move` + `a_selecao_esquece`/`o_componente_no_nome_fica`, Lean l.188, l.237-247). Para (b), l.168 "ausencia de memoria do componente inicial" nao vale; so o PERFIL (instantaneo contra e^{-tau c}) o separa da trava.
 - Leitura a luz da derivacao: se o leitor e a esperanca condicional do Nome (o mapa), o projetor sobre o Nome nao e adversario do leitor: e a forma de chegada dele; a trava e o caminho (a tangente que nao chega: `jamais_esgotado`, `o_motor_tangencia_e_nao_esgota`). O adversario real da memoria seria o item (a). A mesma mistura esta herdada da pedra (CamadaCientifica.lean l.47-48, "o projetor sobre o Nome cumpre as mesmas cotas") e da revisao distinta (REVISAO_CANDIDATA l.171-175); nao e so do Kimi. Decisao de nome e da gerencia/operador.

3.2 "memoria do componente no Nome" como assinatura "da trava" — MODELO l.92, l.156, l.143, REGISTRO l.266. Pela derivacao, preservar o componente no Nome e propriedade do proprio mapa-leitor (fixa o Nome + linearidade), nao so da trava. O kernel ja chama isso de memoria: `name_op_fix_mul` ("A MEMORIA E SUBALGEBRA", TheNameOperator.lean l.101-102). Nao e erro; e nomenclatura a alinhar, e e a razao do 3.1.

3.3 P-A (MODELO l.142) e teorema condicional, nao conjectura: dados `fixa_o_nome` e `consome`, o pouso em <= c(x) passos e o teorema `pousa` (Lean l.362). O conteudo empirico e a HIPOTESE (o leitor real baixa estritamente o custo a cada passo e fixa o que resolve), nao o pouso. Como escrito ("Um leitor real que satisfaca… chega a custo zero"), a [CONJECTURE] cai sobre o que e consequencia. O proprio R4 diz (l.113-122) que habitar o tipo nao e evidencia; a previsao deveria ser escrita sobre a hipotese.

3.4 Propriedades de esperanca condicional ausentes do R4 e da candidata (nao do kernel):
 - Idempotencia de P_N e "reler nao acrescenta": no R4 so como `permanece`/`o_limite_e_idempotente` de `G` (l.106-107), nao do limite da trava. No kernel existe: `name_op_idem` ("O QUE FOI LIDO NAO PODE SER DESLIDO", TheNameOperator.lean l.93), `name_op_unital` (l.67), `name_op_fix_mul` (l.102), `diagExpect_idem` (CondExpect.lean l.94), `diagExpect_bimod` (l.105, a lei de modulo/D-bimodular). Os termos existem no kernel (grep; so li os enunciados citados).
 - Contracao (nao aumenta a norma): nao achei teorema com esse nome em `TheNameOperator.lean`/`CondExpect.lean` (grep limitado a `norm|contract`; pode estar em outro modulo ou so em Mathlib via `starProjection`; nao verifiquei).
 - ATENCAO, dois portadores: a candidata trabalha em VETORES (`P_N` em `EuclideanSpace ℂ X`, estado); o kernel prova idempotencia/modulo em OPERADORES (`nameOp`, `diagExpect` em `M_n(ℂ)`). A ponte entre os dois portadores nao esta no R4 nem na candidata; se ha ponte no kernel, nao verifiquei. Nao identifico um com o outro.
 - `selecao` (nao linear, norma 1) nao e a esperanca condicional; P_N e. O R4 liga P-B a `selecao` (l.66, l.73, l.143); ficar claro qual dos dois e "o leitor/seletor" da derivacao e da gerencia.

3.5 P-C (MODELO l.144): ancorado na inabitabilidade do tipo (`o_tipo_so_diz_que_ha_zero`), que a propria pedra diz que "nao diz nada alem de ha solucao" (Lean l.433-436). A previsao dinamica do P-C e P_N = 0 (nucleo {0}, trava -> 0, sem estado renormalizavel): derivacao de hoje, "o espaco onde a testemunha pode habitar" e vazio. Falta nomear.

3.6 "tangencia" (MODELO l.179): lida so como "a defasagem nao se torna exatamente o Nome". A derivacao da a palavra um segundo conteudo (tangente = testemunho = esperanca condicional). O R4 nao a toca; nao e erro, e termo a reconciliar com o operador. Pelo mesmo motivo, "habitado" no R4 (l.119-122, l.169: "habitacao do tipo", `Nonempty`) e o sentido de teoria de tipos, nao o "habitar o nome" do operador; risco de homonimo se os dois usos coexistirem num texto.

3.7 Cabecalho da pedra (fora dos tres arquivos, para a gerencia): CamadaCientifica.lean l.16-17, "o leitor nao paga a escala, ele e a escala" (e o `nao_refazer` do Mapa, "o leitor e a escala"). Pela derivacao o leitor e o observador/verbo/o habitante, nao o Nome; a escala e o parametro do semigrupo. Nao e erro do Kimi (o R4 nao repete a frase); a gerencia pode querer reconciliar.

3.8 Precisoes menores:
 - MODELO l.7, l.237 e REGISTRO l.13 (B13), l.36-37, l.263: dizem que a R3 corrente nao tem recibo; correto quanto ao recibo INDEPENDENTE (REV2 recompilou o hash 77641aa…, confere), mas existe o log da gerencia para o hash da R3 (build\CamadaCientifica.log, RC 0, trio, 18:22), que o R4 nao cita.
 - CONTAMINACAO l.3, "nenhum artigo publico foi usado como insumo": verdadeiro para EXTRACAO/ISOMORFO sinteticos, mas `K08\ENTRADA\` (06:13, depois de 05:47) tem recortes verbatim dos quatro arquivos publicos (FORMULA_DO_TEXTO l.3); a frase pode induzir erro se lida pela pasta inteira.
 - REGISTRO l.283-289 (paragrafos de artigo, PT/EN) levam estado de processo ("EM_DESENHO_BLOQUEADO, sem congelamento, execucao ou leitura de resultado"); a regra de 12/11 (processo e conversa fora do programa) foi aplicada pela revisao distinta a K06 e a candidata (REVISAO_CANDIDATA l.163). Possivel o mesmo reparo, se esse paragrafo for para o artigo que o um.py emite.
 - MODELO l.166 (ancora: "pouso e retorno ao estado anterior") contra ADVERSARIOS_K08 l.21 (ancora: "nao pousa; custo 24 -> 24" no P-A): dois arquivos dizem coisas diferentes do mesmo adversario.

## 4. Matematica, exclusividade, consciencia, atribuicao ao operador

- Erro de matematica visivel: NENHUM nos tres arquivos. Conferi contra a pedra: semigrupo e k leituras (l.46-55, Lean l.126-157); limite P_N, bacia renormalizada exigindo P_N v != 0, resolucao `t >= max(0, ln(‖v‖/eps))` com `0 <= t` (l.59-67, Lean l.163-185, l.280-316); `o_retorno`, `o_retorno_ao_mesmo_estado`, `o_componente_no_nome_fica` (l.73-92, Lean l.213-247); `trava c 0 = id` (l.96-98); retracao do limite de `G`, `salto`, equivalencia `Nonempty <-> exists zero` com X nao vazio (l.104-122, Lean l.362-443); densidade (l.129-134, Lean l.450-457); ponte binaria e falha com custo > 1 (l.183-190, Lean l.252-267); *strong lumpability* `K_k(c,Q^{-1}(B)) = Kbar_k(Qc,B)` (l.205, forma padrao). CONTAMINACAO: 8/15 = 53,3 %, 6/15 = 40,0 %, 25/27 = 92,6 %, 25/55 = 45,5 %, 2x3x5 = 30 respostas, SHA do dicionario `76f63bd9…c3d8` confere com o arquivo (recalculado). Os hashes das duas pedras no REGISTRO conferem.
- Exclusividade: nenhuma afirmada. Tudo e negacao ou veto: MODELO l.27 ("nao unicidade de modelos"), l.171, l.241; REGISTRO l.225-229 (vereditos proibidos), l.237.
- "E consciente": nenhuma frase. So negacoes: MODELO l.171, l.241; REGISTRO l.212 (`CONSCIOUSNESS_PROVED` proibido, herdado da P7 selada), l.235.
- Atribuicao de fala ou ato ao operador sem bytes: nenhuma. REGISTRO diz "a ratificar" (l.5, l.19), "nao ha ratificacao" (l.195) e "decisao externa" (l.200); "herdados da P7 selada" (l.275) e a fonte, nao fala dele. "operador" nao aparece nos tres arquivos como autor de ato.
- Desvio de escopo: o R4 nao escreveu pedra Lean (MODELO l.237, REGISTRO l.9, l.71-72); justificativa consistente com a ordem (B.2 pede so se faltar teorema). Com a derivacao de hoje, a lista de propriedades do 3.4 pode virar candidata Lean; decisao da gerencia.

## 5. CONTAMINACAO_R4_K08.md em tres linhas

- Decide (so sobre material sintetico): contrato de escolha fechada SIM/NAO/O TEXTO NAO DIZ, pontuacao determinista por ID sem modelo juiz, 15 casos sem falha de contrato, reproducao byte a byte (34 arquivos); e o isomorfo sintetico com duas alternativas (contrafactual factual coerente; sem numeros) mais o sem-Nome pela mesma maquina (base 0 / sem Nome 1), 34/34 verificacoes, sem escolher bracos (`selected_arm=null`).
- Nao decide (l.42-48, l.120): inducao pela pergunta em modelo real, cobertura de cada estrategia de copia, validacao semantica com gabarito humano independente, convergencia ou qualquer coisa temporal; os 100 % de fiacao sao construcao e formato, nao desempenho.
- Em aberto (l.120): saidas reais com gabarito humano, efeito real de inducao, curadoria contrafactual e dificuldade equivalente, escopo dos textos com numeros, formula completa de texto real. Nao certifica producao.
