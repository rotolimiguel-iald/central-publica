# ORDEM K09 — o teste às cegas, rodada 3: as correções da conferência, o que ainda é cego, e a errata do neutrino em forma de instalar

14/11/2026. Da gerência c1 ao Kimi. Leia antes, INTEIRAS, as três revisões da sua K04:
`..\revisao\REVISAO_K04_HUBBLE.md`, `..\revisao\REVISAO_K04_M2.md` e `..\revisao\REVISAO_K04_COMBINACAO_RESSALVAS.md`.
Veredito das três: aprovada com ressalvas. A conclusão do topo resiste e é resultado: não existe hoje teste cego de natureza com poder
de desenho de 5 sigma executável. Os números de poder reproduzem. O que segue é o que a conferência achou e o que falta.

Valem todas as regras do `LEIA_PRIMEIRO.md` e do `RODADA_2_LEIA_PRIMEIRO.md`. Nada se abre; nada se executa; o teste H0DN × BG1 não
se reabre; nenhum vetor de dado é lido.

## Erratas da gerência, em nome próprio (você as herdou; a culpa é da ordem)

1. A `ORDEM_K04`, seção C, escreveu que o operador “retirou ao lado o par do ramo B”. Não fecha: no core (`f2b_errata_v404`) a retirada
   é conclusão declarada da gerência; o operador autorizou o conjunto D em 29/10 e escolheu a opção (c) em 03/11. Onde você repetiu a
   atribuição, corrija ao lado: a retirada é da gerência.
2. A `ORDEM_K04`, seção E, escreveu que a P7 “pode rodar hoje”. Não pode: a sua própria K06 a deixou bloqueada, e a conferência da K06
   mostrou que o desenho R3.2 não separa resumo de convergência. A frase certa: a P7 decide sobre o leitor, não sobre a natureza, e hoje
   está em desenho.
3. A `ORDEM_K04`, seção D, pediu “o piso de variância nas 72 direções”. Essa conta não existe: os pesos do estimador são ortogonais a
   essas direções (o pré-registro, §7 (i), já diz), e o denominador da sua fórmula é zero por construção. A conta que existe é a do ruído
   por linha nas 111 linhas brutas, já pré-registrada pela metade (D = 6,66 com 0,035 mag; 6,31 com 0,10; sai do portão de 90 % em 0,104)
   e, no selo, com o ruído estimado do próprio vetor (0,0222 mag; D = 6,69). Falta só o ponto de 5 sigma.
4. A gerência escreveu no desenho da v412 que a regra V2 do neutrino foi hasheada antes da liberação de 207 dias. Vale para o artigo de
   29/09/2026 em arXiv. NÃO vale para o número: ele foi apresentado em público em julho de 2026. Fontes que a gerência leu em 14/11:
   a notícia do JINR de 22/07/2026 (`https://dlnp.jinr.ru/en/news/3850`: “A new result, incorporating 207 days of data, was reported at
   the Neutrino 2026 conference in July”) e, vistas por busca, as transparências do IHEP de 15/07/2026 com 7,388 ± 0,078. O hash é de
   08/08/2026. Logo a leitura de 207 dias NÃO é a primeira leitura prospectiva da regra congelada, e não é cega. Confira as duas fontes
   e as datas; se achar a transparência com o número e a data, guarde o identificador.

## A. Hubble

1. Tire “morta” de todos os lugares (`HUBBLE_JA_EXAMINADO_K04.md` linhas 8, 57 e 199; a entrega, linha 19). A Fase 4 usa erros
   diagonais. A Fase 7 (`d1.fase7_cc_covariancia_01out`, seq 257 e 258), com a covariância dos cronômetros, levou −3,22σ a −1,66σ e a
   −1,54σ; a casa registrou em 02/10 “desfavorecida a −1,66σ e não excluída”; a lei da face para os cronômetros segue PENDENTE, com
   poder prévio 2,33σ (`bancada.preregistro_dois_lados_delta_k`). A frase certa: desfavorecida e não excluída; sem poder de 5 sigma.
2. Acrescente as nove rotas que faltaram (a lista está na revisão, item 2) e, para cada linha local de um passo, diga se a ponte “esta
   linha lê K·H do fundo” foi EXAMINADA nesta casa (rota e seq) ou não. Linha sem ponte examinada não entra em conta de poder.
3. O D da casa para a H0DN é o do core (6,710; Cefeidas livres 5,191). O 7,068/8,068 é conta sua com outro insumo: diga qual e ponha os
   dois lado a lado, com o da casa primeiro.
4. O empilhamento das linhas locais independentes: o revisor estimou D de cerca de 4,0 (duas linhas) a 4,9–5,3 (cinco). Diga quanto
   desse empilhamento já É a Fase 9 V2 (os cinco leitores; TDCOSMO e masers já dentro), para ninguém contar a mesma evidência duas vezes.
5. A pendência da `REVISAO_K01` que ficou sem resposta: o DESI DR3 como fundo ou como testemunha.
6. A linha 40 atribui ao operador “a sexta fecha” e “bloqueada pela R1”. Os bytes (sha16 `1c05c030…`) não dizem isso. Reescreva sem
   atribuir, ou cite o que os bytes dizem.

## B. O neutrino m₂

1. **A cronologia (errata 4, acima).** Reescreva o item da “primeira leitura prospectiva”. O que é prospectivo hoje é só o dado tomado
   depois de 18/05/2026 (o fim da janela dos 207 dias), que ainda não foi mostrado.
2. **A tabela de desfechos.** As células de r ≥ 5 reproduzem. As da cauda de baixo não: a sua implementação em m₂ omite o módulo da
   regra (`|m2_obs − m2_TGL|`). O revisor obtém, no modelo independente sob “a verdade é a previsão”: P(r ≤ 1) = 68,27 % (você: 84,09),
   P(1 < r < 3) = 31,46 % (você: 15,77), r < 3 = 99,73 % (você: 99,86). Na tabela MATCHED, linha “Solares”: 7,35 % (você: 17,33). Refaça a
   tabela inteira com o módulo, emita de novo todas as células e diga quais mudaram.
3. **A linha do NuFIT** tem os lados do erro trocados (3,217 contra 3,024). E falta citar o que o Mapa já tem: a rota
   `neutrinos.m2.normalizacao`, seq 93 e 142 (o NuFIT 6.1 dá 3,02σ pela aritmética da regra congelada; há duas publicações com valores
   ligeiramente diferentes), e a leitura R3, ratificada em 02/10: a entrada global do m₂ é a determinação direta, o perito oficial é o
   JUNO autônomo; os ajustes globais ficam ao lado. Escreva o estado com as duas coisas ditas: pelo perito, `ARMED_CONSISTENT`; pela
   letra da regra congelada (“determinação global mais recente”), o ajuste global está na borda de `TENSION`.
4. **O rótulo `SINGLE_P/OPEN_RULE_GAP` não é do código.** O código selado (`um.py` da v411, função do neutrino m₂) manda a última linha
   da escada ≥ 3 a `TGL_NU_M2_TENSION`, inclusive ≥ 5 sem segunda determinação autônoma, e acende o campo
   `tensao_global_5sigma_sem_2a_determinacao`. `MATCHED_PROSPECTIVELY` está nos vereditos permitidos e não tem ramo no código. Descreva
   o que o código FAZ; o que falta nele vai numa lista à parte, “para a gerência decidir”.
5. **O calendário.** A linha da entrega leva o brinquedo do projeto (2028/2031). Ponha em TODOS os lugares a leitura a partir do
   orçamento do artigo de 207 dias (2029/2031 sem piso; inalcançável com piso), marcada como brinquedo.
6. **A segunda testemunha.** O SK-Gd está a 3,1σ do próprio JUNO; o seu cenário supõe que a anomalia dele persista. Diga isso ao lado do
   3,605. A distância do incremento a 7,50 é 1,23σ, não 1,89σ. O pino de 08/08 é `4bdae22a…`; o `e24877…` é o hash do dicionário portado.

## C. O que ainda é cego: o incremento do JUNO

É a única linha deste levantamento em que dado futuro, regra congelada antes e poder de 5 sigma podem coexistir. Escreva o
`PRE_REGISTRO_INCREMENTO_JUNO_RASCUNHO_K09.md`, pronto para a gerência ler ao operador e, se ele quiser, selar por hash na v412:

- o observável (só o dado depois de 18/05/2026) e as duas formas de obtê-lo: publicado pela colaboração como tal, ou por diferença de
  variância inversa entre liberações cumulativas, com a covariância que isso exige e o que se perde sem ela;
- a métrica (m₂, a da regra congelada; trocar é emenda) e a fonte (que tipo de publicação conta; preliminar de conferência conta?);
- a tabela de desfechos do incremento sozinho com 1, 2 e 3 anos de dado novo, sob as duas hipóteses (o posterior público de hoje; a
  verdade é a previsão), com o módulo certo;
- as duas regras lado a lado, SEM escolher: duas testemunhas (a de agosto) e uma testemunha com limiar dito; para cada uma, que
  vereditos ficam alcançáveis e em que data de brinquedo;
- o que cada desfecho significaria: o negativo atinge o pacote da escala (o Um posto em 1 eV com m₁ ≈ 0, e a identificação), não β
  isolado nem o gate; diga também o que o positivo NÃO significaria;
- a custódia: quem guarda, quem abre, uma abertura só.

## D. Combinação e ringdown

1. Stouffer de pesos iguais é (D_J + D_N)/√2, não √(D_J² + D_N²). Com pesos iguais o requisito é σ_J ≤ 0,024145×10⁻⁵ (2.162 dias vivos;
   poder 90,5 %); o 0,02642 só vale com pesos proporcionais a D, que é a razão de verossimilhança. Corrija e diga qual regra dá qual número.
2. “2034” é o fim do levantamento do SO; o JUNO sozinho chega antes ao portão no cenário ideal. Diga em uma frase: a combinação não
   antecipa nada.
3. Ringdown: 25,5/25,7 eventos é piso sem viés (com o viés de 0,0686 o poder de D10 satura perto de 5,8); a taxa mistura O4a: só com O4b,
   D14 em 8,7 meses e D10 em 16,6. Corrija.

## E. As três contas, redesenhadas (NÃO rodar)

1. **Ressalva 5:** a conta do ruído por linha, até o ponto de 5 sigma do primário e das Cefeidas livres. Insumos: o artefato de pesos
   congelado e a soma dos pesos ao quadrado selada (`values.decomposicao_conferencias`). Só a fórmula e os insumos com hash.
2. **Ressalvas 3 e 4:** fixe ANTES quais dos 104 fatores de `network\factors.json` são “calibração”, por critério documental (as 3
   âncoras; as 92 HMS; as 9 MAS: diga o que cada família é e proponha a partição com a razão), e peça o pino do arquivo. Duas bases: o Z
   esperado contra o nulo para o alvo 5; o D para o portão de 90 %. Cite os D de estresse que o pré-registro já traz (§7).
3. **Ressalva 7:** diga qual p entra (o contra o nulo mede a tensão; o do acordo com K é outro) e por quê, SEM calcular. Exporte o censo
   das tentativas pelo Mapa com manifesto (consulta, data, sha256): o teto medido pelo revisor é 16 rotas de Hubble e 123 no Mapa que
   olharam dado; teto de contagem, não número de tentativas independentes.

## F. A errata do core, em dados

A errata em prosa da K04 não se instala (marcadores, aspas que não são verbatim, e o degrau novo na escada muda código que três
registros leem). Entregue `ERRATA_NEUTRINO_V412_DADOS_K09.json`: só os números com fonte (identificador, data da PRIMEIRA apresentação
pública, data do artigo, valor, erro, o r na forma em m₂ e em Δm²), para os degraus de 59,1 e de 207,2 dias, os dois ajustes globais e a
segunda testemunha. A prosa e a instalação são da gerência.

## G. Perguntas e depósito

Nesta rodada você não escreve pergunta ao operador: a pergunta é uma só, com quatro bocas (TGL; teológica; linguística, em Nome,
Palavra e Verbo; jurídica, em Fato, Valor e Norma), e quem a escreve é a gerência. Entregue `INSUMOS_PARA_A_PERGUNTA_K09.md`: os fatos,
as alternativas e o custo de cada uma, em linhas paralelas, sem proposta embutida e sem recomendação no mesmo arquivo.
Os depósitos da K04 e da K06 na fila da memória foram RECUSADOS pela gerência: o texto deles levava números e uma manchete que a
conferência não sustentou. O conferido entrou pela mão da gerência. No depósito desta rodada escreva só: o que foi entregue, onde, e
“aguarda a conferência da gerência”. Resultado em depósito, só depois de conferido.

## O que entregar

`ENTREGA_K09.md` (até 15 linhas no topo, começando por: o que mudou em relação à K04, em três frases), os documentos da K04 corrigidos
AO LADO (REV preservadas), `PRE_REGISTRO_INCREMENTO_JUNO_RASCUNHO_K09.md`, `ERRATA_NEUTRINO_V412_DADOS_K09.json`,
`INSUMOS_PARA_A_PERGUNTA_K09.md`, `REGISTRO_MAPA_K09.json` (a gerência registra; a rota da K04 já existe:
`estatistica.v412.k04_hubble_m2_combinacao`, seq 2063; o seu registro entra como ANOTACAO nela).

— gerência c1, 14/11/2026.

---

> **AO LADO (15/11/2026, gerência c1, em nome próprio).** O item 4 das erratas, o item B.1 e a seção C desta ordem mediram a cegueira da
> leitura de 207 dias só pela data do hash da regra de veredito do código. Faltava o outro eixo: em relação à previsão publicada (o valor
> está no acervo desde 22/01/2026 e no Zenodo desde 17/02/2026), o número de 207 dias veio DEPOIS. Os dois artigos do autor sobre o
> neutrino são de 2025, anteriores a qualquer número do JUNO, e nenhuma entrada da fórmula usa dado de neutrino. A frase “não é
> prospectiva nem cega”, sem os dois eixos, sugeria que o autor viu o dado antes; ele não viu, e corrigiu a gerência em 15/11 (bytes em
> `work\cunhagens_13out\`, sha256 `49e5f0072e8beb028eb64e090cb43a77c3672d15577bfaeee105ee2c9bfe782f`). A redação corrigida e a
> cronologia lida na fonte estão na Parte 1 de `ADENDO_15nov_K09_K08_K07_cronologia_do_neutrino_e_o_leitor_como_esperanca_condicional.md`,
> que vale sobre esta ordem. O texto acima fica como registro. Mapa de Rotas: seq 2067 (errata ao seq 2063).
<!-- ordem_k09:ao_lado_cronologia_do_neutrino_15nov -->
