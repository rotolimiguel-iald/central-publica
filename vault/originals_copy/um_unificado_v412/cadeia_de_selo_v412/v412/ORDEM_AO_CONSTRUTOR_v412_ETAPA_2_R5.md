Você é o **claude-construtor-v412**, agente de PREPARAÇÃO da versão v412 do `um.py` da IALD/TGL, trabalhando para a gerência c1 (sessão Claude Code da Central de Patentes). Português na prosa; inglês no código. Windows; Bash (Git Bash) ou PowerShell; Python sempre como `C:\Python314\python.exe -B -X utf8 arquivo.py`, com o `.py` gravado pela ferramenta Write (NUNCA `python -c`, `python -` nem heredoc).

## O que é esta ordem: refazer a Etapa 2 pelo contrato R5 (do kernel ao candidato) e PARAR

Ordem escrita em 18/11/2026, 18:05. A Etapa 2 foi fechada pelo contrato R4 em 17/11 (candidato `8b9a02e51650b11c`, 42 módulos). Depois disso o autor mandou entrar tudo o que se provou em 17 e 18/11 sobre o leitor da fórmula, e a lista de pedras passou de 42 para **153 módulos**. O contrato vigente é o **R5**, CONGELADO: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\CONTRATO_v412_R5.md` (sha16 `d2eaac8ca77e7f51`; cópia em `contrato_REV5\`). Confira por script, antes de começar, este sha16 e os três que o contrato dá: o manifesto `insumos\MANIFESTO_PEDRAS_v412_R10.json` (`518b593bfbf759b0`), as âncoras `insumos\ANCORAS_PROPOSTAS_v412_R10.json` (`a287f91f884982bc`) e a página `o_que_fica_claro_REV18\O_QUE_FICA_CLARO_v412_R18.md` (`c58564d29275ee75`). Se algum não bater, PARE.

**As regras invioláveis, o método e a lista do que é da gerência são os da ordem anterior, `ORDEM_AO_CONSTRUTOR_v412_ETAPA_2.md`: leia-a inteira antes de tudo; valem todas, sem exceção.** Esta ordem só diz o que mudou.

## Leia primeiro (nesta ordem)

1. `ORDEM_AO_CONSTRUTOR_v412_ETAPA_2.md` (as regras e o método).
2. `CONTRATO_v412_R5.md`, inteiro; o topo dele diz o que mudou do R4.
3. O seu fecho anterior `PREPARACAO_v412_PRONTA.json` e `ETAPA_2_ESTADO_v412.json` (LEIA como arquivo; NÃO rode os scripts `e2_*_estado_*` para ler estado: eles regravam o arquivo). O que você construiu pelo R4 (o gerador, o delta, os registros, a guarda, a travessia, os scripts `e2_*` e `*_c4`) é o seu ponto de partida: derive cópias novas com sufixo `_r5`; não edite as antigas.
4. `insumos\MANIFESTO_PEDRAS_v412_R10.json` (campos `frente`, `de_quem`, `namespaces`, `novas_em_relacao_a_oitava_lista`, `mudaram_da_nona_lista`, `tudo_junto`) e `insumos\ANCORAS_PROPOSTAS_v412_R10.json` (campo novo por módulo: `listadas_em_print_axioms`).
5. A página R18 e os pareceres `revisao_orquestrador\REVISAO_031_U3_Codex.md` e `REVISAO_032_V3_Codex.md` (só para saber o que cada linha da tabela quer dizer).

## O que fazer

0. **Confira os quatro sha16** e grave o recibo.
1. **O kernel.** Reconstrua no sandbox `C:\t\k412c\final` com os 153 módulos de `insumos\pedras_r10\` (hoje ele tem os 42 da sétima lista): as duas transformações permitidas da seção 1 do contrato e mais nenhuma; compilação a frio; relatório de axiomas; os portões do kernel da seção 1; escada de teoremas e de bandeiras antes e depois. Guarde a árvore anterior fora de `work\`, como antes. Feche em `PRONTO_PARA_CANDIDATO_v412_R5.json`.
   **Três pontos novos, que os seus scripts do R4 podem não cobrir:**
   - **Os nomes completos das declarações.** Dos 109 módulos da frente C, só 8 abrem `TGLExt.*`; os outros abrem `Codex.*` (70), `IALD.*` (27), `PsiNetworks.*` (3) e os das duas sondas, e há módulo que abre dois espaços de nome. NÃO monte nome de declaração por prefixo do módulo. O nome completo de cada âncora sai do relatório de axiomas do sandbox (ou das linhas `#print axioms` da fonte, que trazem o nome completo), e a checagem confere que ele existe lá.
   - **Dois arquivos têm nome em minúsculas** (`sonda_n0_contraexemplo`, `sonda_cadeia_caminho`): entram com o nome que têm.
   - **Nenhum identificador se renomeia** (decisão do autor; seção 1 e D223). Se a compilação a frio acusar nome repetido, PARE e diga qual: a gerência compilou uma raiz que importa o kernel inteiro e os 153 com os nomes soltos, sem erro (`pedras_novas\build\TUDO_JUNTO.json`), mas a instalação muda as linhas de importação.
2. **Os cinco registros** da seção 2 do contrato, com as palavras de veredito copiadas do R5 POR SCRIPT (a de `iald_camada_cientifica_v412` mudou; `leitor_da_formula_v412` é novo; as outras três não mudaram). O registro novo traz, só com o que tem âncora, o que a tabela da seção 2 da página diz, linha a linha, e não usa a expressão “P = nP”.
3. **As respostas da gerência aos seus sete pontos** estão na D224 do contrato: aplique-as (em especial: os identificadores `r1`, `r2`, `r3` de `cunhagens_v412` trocam de nome; o patch de dado no literal `escada` fica; o artefato das falas vai até `OPERADOR_18nov_*`).
4. **O texto público** pela página R18: a seção do artigo em português e em inglês (o bloco novo “O leitor da fórmula” tem uma tabela de 30 linhas; tradução fiel, com os nomes dos termos e dos módulos intactos), o resumo, os blocos do README, do estado atual e do handoff, os 34 marcadores herdados. A travessia da guarda sobre tudo o que é novo, com o recibo das unidades.
5. **O gerador e o CANDIDATO regerado** (o candidato do R4 fica guardado com outro nome, fora de `work\`), o ensaio a seco, o portão do pilar no candidato, a guarda de material privado sobre os insumos pinados, o verificador de história sobre os textos novos.
6. **Feche** em `PREPARACAO_v412_PRONTA_R5.json` (o do R4 fica como está), com tudo medido e os sha16 lidos por script, e **PARE**. A Etapa 3 (os scripts de rito, instalação, custódia e pós-rito marcados `[A ADAPTAR v412]`, e a bateria pré-selo) é OUTRA ordem, depois da revisão de terceiro do candidato: não a comece.

## Estado em disco

Depois de cada bloco (0 a 6), grave `ETAPA_2_R5_ESTADO_v412.json` (arquivo NOVO; o que está feito, com arquivos e sha16; o que falta; o próximo comando), por temporário e troca, guardando o anterior com `.bak_<data>`. Se o seu contexto acabar, uma continuação parte desse arquivo. Memória ACOM: a SUA referência (`SESSION_REFERENCE_construtor_v412.json`). Mapa de Rotas: consultar antes (`rotas.py consultar "v412"`), registrar a rota desta etapa ao fim. Depósito de memória na sua pasta da fila.

## Entrega (até 15 linhas)

Se fechou e o caminho do fecho com sha16; onde está o candidato, o tamanho e o sha16; a escada de teoremas e de bandeiras no candidato contra a do kernel (antes e depois); quantos módulos, quantas âncoras por registro e quantas checagens; como resolveu os nomes completos das âncoras da frente C e quantas ficaram sem nome no relatório de axiomas (tem de ser zero); os controles da guarda e o verificador de história; o portão do pilar; o ensaio a seco; cada ponto em que divergiu do molde ou desta ordem e por quê; o que criou em disco e o tamanho; o número do registro no Mapa e o caminho do depósito. Se algo bloquear, deixe o estado legível em disco e diga o ponto exato.
