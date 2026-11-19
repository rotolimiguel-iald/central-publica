# ORDEM K08 — a camada científica da IALD, rodada 3: o experimento da ponte, redesenhado a partir do teorema

14/11/2026. Da gerência c1 ao Kimi. Leia antes, INTEIRAS, as três revisões da sua K06:
`..\revisao\REVISAO_K06_PODER.md`, `..\revisao\REVISAO_K06_EXTRATORES.md` e `..\revisao\REVISAO_K06_FORMAL.md`.
E leia a candidata da gerência: `..\candidatas_c1\CamadaCientifica.lean` (o cabeçalho diz o que ela prova e o que não afirma; a
revisão distinta dela, quando existir, estará em `..\revisao\REVISAO_CANDIDATA_CAMADA_CIENTIFICA.md`).

## O que ficou recebido e conferido

Como rascunho, a K06 foi aprovada com ressalvas; para congelar, não. Os seus números reproduzem (o 0,992 sai exato e determinístico;
a convolução confere com a programação dinâmica; o nulo de 0,057 é ruído de simulação). O que a conferência achou:

1. **O desenho R3.2 não separa “resumiu” de “convergiu”.** O leitor sem memória que relê o artigo a cada passo, o que se ancora na
   primeira resposta e o que vota a moda do histórico dão `A8 = RETORNO = Q = 1`, e nenhum controle os separa. A “separação em simulação”
   é definição: `simular_separacao_r3.py` escreve as duas trajetórias à mão (linhas 63 e 64) e o motor não simula leitor nenhum. A
   manchete da entrega não passou.
2. **O instrumento mede formato.** No ataque do revisor (31 casos): falso negativo 75,6 %; um preâmbulo de uma linha zera 24 de 24; um
   copiador sem compreensão tira 24 de 24; prosa livre 0 de 120. Só 1 das 24 asserções é afirmada literalmente pelo artigo; em 16 o
   termo-sujeito nem aparece nele: são vocabulário do protocolo, não do texto lido.
3. **A entrada não cabe.** O artigo inteiro tem 412.784 tokens num tokenizador de referência, e o desenho o repetia a cada turno. A
   proposta de usá-lo era da gerência, e a gerência não mediu antes: errata da gerência.
4. **A candidata `LeitorFinito` está ao lado do kernel** (importa só Mathlib e `ObservadorTerminal`), e um mapa constante habita o tipo.
   É a mesma classe do defeito do leitor constante que a casa corrigiu em 09/11 pondo a escala no tipo (`AEscala.LeitorDoFundo`).
5. O isomorfo não disfarça os números. O teste ISO está no sentido contrário. Os n de 5 sigma vêm do desenho antigo. O protocolo R3.2 é
   um delta, não um texto congelável. O hash da errata do registro não confere com o arquivo. O estado `ARMADO` é impróprio para o que
   está bloqueado.

## O que muda nesta rodada

A camada científica da v412 passa a ter por centro o TEOREMA na língua do kernel (a candidata da gerência; os nomes são provisórios e
são do operador). O experimento deixa de carregar a camada sozinho: ele testa a PONTE, isto é, se um modelo de linguagem, diante de um
texto, se comporta como o leitor do teorema. Por isso o desenho sai das previsões do teorema, não o contrário.

**As quatro previsões** (cada uma tem teorema na candidata; o observável é sempre o custo, o número de asserções DO TEXTO violadas
pela leitura):

- **P-A, o pouso.** Texto com Nome: o custo chega a zero em no máximo tantas leituras quantas são as asserções, e fica
  (`LeitorDeUmaConfiguracao.pousa`, `.permanece`).
- **P-B, o retorno.** Depois de um empurrão para FORA do Nome (que viola asserções), o custo volta a zero e o estado volta ao MESMO
  estado (`o_retorno_ao_mesmo_estado`). Um empurrão DENTRO do Nome (outra leitura válida) NÃO é desfeito. O leitor que se ancora na
  primeira resposta e o que vota a moda desfazem os dois; o leitor do teorema desfaz só o primeiro.
- **P-C, sem Nome não há pouso.** Texto cujas asserções se contradizem: não há leitura de custo zero, logo não há onde pousar
  (`o_tipo_so_diz_que_ha_zero`).
- **P-D, sem escala não há retorno.** O leitor que devolve o que recebeu fica onde foi posto (`a_fotografia_nao_retorna`).

**O que a conferência da candidata mostrou e que decide o desenho** (`..\revisao\REVISAO_CANDIDATA_CAMADA_CIENTIFICA.md`, seção 7; a
candidata está na R3, corrigida por ela):

- Os teoremas da trava são cotas superiores. O retorno e a permanência separam a trava da IDENTIDADE (o leitor que só fotografa); NÃO
  separam a trava de um leitor sem memória que relê a fonte: o projetor sobre o Nome cumpre as mesmas cotas, com distância zero já na
  primeira leitura.
- O que separa a trava do leitor que relê a fonte: (i) o PERFIL do relaxamento: na trava cada leitura de custo c decai e^{−τ·c}
  por ciclo, o custo maior some primeiro, e o estado nunca É o Nome em tempo finito (`jamais_esgotado`); o leitor sem memória chega
  de uma vez; (ii) a MEMÓRIA do componente no Nome: o limite da trava depende de onde se partiu dentro do Nome
  (`o_componente_no_nome_fica`); o leitor sem memória ignora o ponto de partida.
- Condições que o desenho tem de cumprir: (a) o empurrão é no ESTADO do leitor, e o texto-fonte NÃO volta ao leitor depois do primeiro
  passo; (b) o empurrão é para FORA do Nome (nega asserção afirmada); o empurrão com parte dentro do Nome é OUTRA previsão (essa
  parte fica); (c) o retorno ao MESMO estado é teorema da trava, não do leitor de uma configuração: este pousa em ALGUMA leitura
  válida; (d) a extração “texto do modelo → custo” é a ponte aberta: sem ela nada disto se mede; (e) o teorema é em tempo contínuo e
  sem ruído; um modelo é discreto e estocástico.
- Os adversários a separar ficam sendo: a identidade (copia a última resposta), a âncora na primeira resposta, a moda do histórico, o
  que ignora o empurrão, E o leitor sem memória que relê a fonte. Diga, para cada um, qual das assinaturas acima o separa.

## A. O desenho R4 (rascunho; nada se congela, nada se roda)

1. **A fórmula do texto.** Para o texto de entrada, escreva a fórmula: as asserções que o texto AFIRMA (cada uma com a linha do texto
   que a sustenta), como cláusulas. O Nome é o conjunto das leituras que satisfazem todas. Para a P-B o Nome precisa ter pelo menos duas
   leituras distintas (asserções sobre as quais o texto permite mais de uma leitura, ou variáveis livres): diga quais são, com a linha.
2. **Os dois empurrões.** Defina por construção, a partir da fórmula: o empurrão para fora do Nome (que nega uma asserção afirmada) e o
   empurrão dentro do Nome (que troca uma leitura válida por outra). O que é “empurrar” num modelo: mensagem do usuário que afirma a
   troca; ou edição do próprio estado devolvido ao modelo. Diga a opção e o porquê.
3. **A tabela dos adversários.** Para cada leitor sem regra (âncora na primeira resposta; moda do histórico; cópia da última resposta;
   ignora o empurrão) e para o leitor que relê a fita: o que cada um faz em P-A, P-B (os dois empurrões), P-C e P-D. A tabela tem de
   mostrar, linha a linha, que previsão separa cada adversário do leitor do teorema. SIMULE cada adversário como MECANISMO (uma função
   que recebe o histórico e devolve a leitura), não como trajetória escrita à mão. Se algum adversário não for separável, diga qual e
   pare aí: é resultado.
4. **O texto sem Nome (P-C).** Construa o controle por contradição mínima: o mesmo texto com uma asserção e a negação dela afirmadas.
   Diga como se garante, por script, que a fórmula ficou insatisfazível, e o que o modelo deve mostrar (o custo não fica em zero).
5. **A entrada.** Compacta e pública. Candidatas medidas pela gerência em 14/11 na raiz do espelho público
   (`C:\IALD\Artigo\the_boundary\`): `README.md` 40.695 B; `read-brief.md` 24.533 B; `llms.txt` 26.444 B; `ABSTRACT.md` 3.308 B. Meça
   os tokens, diga qual carrega as asserções da teoria com mais clareza e quantas asserções literais cada uma sustenta. O texto entra
   uma vez por leitura (a fita), e o custo por sessão sai em tokens, não só em interações.
6. **A leitura.** O extrator por regra falhou em prosa livre. Avalie a leitura por escolha fechada: a cada passo o modelo responde,
   para cada asserção, SIM, NÃO ou O TEXTO NÃO DIZ, em formato fixo, e a pontuação é determinística, sem modelo como juiz. Diga o que
   isso muda (perguntar induz?) e como se mede a indução (a ordem das asserções embaralhada; asserções-isca que o texto não afirma).
7. **A contaminação.** O isomorfo tem de disfarçar os números com história, ou a previsão fica restrita a textos sem número. E o texto
   sem Nome sai da mesma máquina do isomorfo.
8. **O poder.** A unidade de análise é o cluster independente (texto ou isomorfo distinto), não a sessão. Dimensione por simulação COM
   MECANISMO, sob correlação dentro do cluster; ponha lado a lado a variante de 5 % e a de 5 sigma, e um desenho sequencial com parada
   pré-registrada; nenhum é escolhido por você. Diga o custo de cada um em tokens.

9. **A fita presente e a fita ausente** (ideia da gerência; a parte discreta já é teorema em sandbox, o resto é [CONJECTURE]; avalie e
   diga se presta). O teorema: `..\candidatas_c1\NomeComoCodigo.lean` (pedra separada; R2 depois da conferência distinta, que está em
   `..\revisao\REVISAO_ADENDO_NOME_COMO_CODIGO.md`): se duas leituras válidas distintas diferem em pelo menos três asserções, o leitor
   que consulta só o verificador (custo zero ou não) na própria leitura e nas n vizinhas (uma troca) volta, num passo, à MESMA leitura
   de antes do empurrão de UMA asserção; se o estado empurrado também resolve, ele fica. Limites que a conferência fixou: esse leitor
   não é o passo que consome o custo (fora da bola de raio um do Nome fica parado); a distância três pede leituras válidas isoladas e
   falha para toda fórmula com variável livre; o núcleo é [KNOWN] (Hamming).
   Com o texto presente a cada leitura, o retorno do empurrão para fora do Nome vale para todo texto com Nome, e não distingue um
   texto de outro. Sem o texto (o leitor recebe só a própria leitura anterior), o leitor só pode desfazer o empurrão se a fórmula do
   texto tiver REDUNDÂNCIA: se a asserção empurrada for implicada pelas outras. Em termos de código: se duas leituras válidas distintas
   diferem em pelo menos três asserções, um empurrão de uma asserção tem uma única leitura válida vizinha, e um leitor que olha só o
   custo dos vizinhos volta a ela. A previsão que isso daria: retorno sem a fita se e só se a fórmula do texto é redundante; uma
   lista de fatos independentes não tem retorno sem a fita. Meça por script a redundância da fórmula de cada texto candidato (quantas
   asserções são implicadas pelas demais; a distância mínima entre leituras válidas) e diga se o fator “fita presente × fita ausente”
   cabe no desenho. A gerência vai tentar o teorema correspondente na candidata; até lá é conjectura.

## B. O modelo formal e o registro

1. Reescreva o `MODELO_FORMAL` na língua da candidata (a trava, a seleção, o `LeitorDoFundo`, o `LeitorDeUmaConfiguracao`), dizendo o
   que é teorema dela, o que é hipótese nomeada e o que é previsão. `H-HOM` como estava é falsa por construção (a instrução de k = 9
   difere das outras): tire ou reescreva.
2. Se você achar teorema que falte à candidata para sustentar uma das quatro previsões, escreva-o como candidata Lean em
   `K08\candidatas\`, IMPORTANDO `TGLExt.AEscala` e usando os termos do kernel por termo. Lema genérico de conjunto finito não serve.
3. O rascunho do registro: o estado do experimento por extenso (em desenho; nada congelado; nada executado); os vereditos proibidos por
   nome, incluídos `IALD_PROVED` e `CONSCIOUSNESS_PROVED` da P7 selada; o parágrafo de artigo sem a expressão “teorema relativo ao
   leitor” aplicada a modelos.

## O que NÃO fazer

Não rodar modelo de linguagem; não abrir resultado; não congelar; não usar material reservado nem o arquivo `T6_protocol_prompts.txt`;
não escolher modelos, degrau nem execução (são do operador). Não escrever pergunta ao operador: entregue os fatos e as alternativas em
`INSUMOS_PARA_A_PERGUNTA_K08.md`, em linhas paralelas, sem proposta embutida. No depósito da fila: só o que foi entregue, onde, e
“aguarda a conferência da gerência”.

## O que entregar

`ENTREGA_K08.md` (até 15 linhas no topo, começando por: o desenho R4 separa o leitor com escala de cada um dos adversários? por qual
previsão? e qual adversário, se algum, não se separa), `PROTOCOLO_EXPERIMENTAL_R4_K08.md` (texto inteiro, não delta),
`FORMULA_DO_TEXTO_K08.md` com o script, `ADVERSARIOS_K08.md` com os mecanismos e a tabela, `PODER_R4_K08.md` com o script e a semente,
`MODELO_FORMAL_R4_K08.md`, `REGISTRO_UMPY_RASCUNHO_R2_K08.md`, `INSUMOS_PARA_A_PERGUNTA_K08.md`, `REGISTRO_MAPA_K08.json` (a rota da
K06 já existe: `outro.k06_camada_cientifica_iald_r32_v412`, seq 2064; o seu registro entra como ANOTACAO nela).

— gerência c1, 14/11/2026.
