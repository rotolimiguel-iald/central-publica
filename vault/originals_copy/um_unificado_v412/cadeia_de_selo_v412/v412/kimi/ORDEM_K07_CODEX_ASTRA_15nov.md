# ORDEM K07-C — ao Codex, no modo máximo (astra), com o Kimi: a matemática que resta da v412

De: a gerência c1 (sessão Claude Code da Central de Patentes). Para: o orquestrador do Codex. 15/11/2026, 16:49.
Unidade do quadro: `F1.K07_ASTRA_20261115` (`C:\IALD\PROGRAMA_IALD`). Reivindique antes de trabalhar; entregue com evidência.

## 0. A ordem do operador

Bytes em `C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_15nov_o_que_falta_para_o_tipo_iii_como_termo_pergunta_nas_quatro_linguas_e_codex_astra_com_o_kimi_no_segundo_adendo_verbatim.txt` (sha256 `305830689dbdc266ad2d853ebbd8b300a1b486bb0968348606c6fd2e65272c6d`; confira lendo o arquivo). O trecho que lhe diz respeito, copiado dos bytes:

«quanto ao seu segundo adendo vamos trabalhar com o codex no modo maximo dele (astra) junto com o kimi, peça ele para ler e entender tudo que o Kimi fez e resolver o que vc está pedindo do segundo adendo, pode passar ao orquestrador do codex e peça para quando estiver pronto ele te devolver no caminho que vc criou»

Esta mensagem é da gerência, não do operador. A autorização é a fala dele, no arquivo acima. Se ela não lhe bastar, pare e pergunte a ele no app.

## 1. O que ler e entender primeiro: tudo o que o Kimi fez

A pasta é `C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\` (o túnel do Kimi nesta versão). Leia nesta ordem:

1. `LEIA_PRIMEIRO.md` e `RODADA_2_LEIA_PRIMEIRO.md`; as ordens `ORDEM_K01` a `ORDEM_K09`; os dois adendos de 15/11 (`ADENDO_15nov_K09_K08_K07_…md`, com quatro acréscimos no fim, e o **ADENDO B**, `ADENDO_15nov_B_K07_a_gerencia_fez_a_construcao_2_e_a_ergodicidade_da_cunha_ja_era_do_kernel.md`, sha16 `0d89bf7eceeaf540`).
2. As entregas `ENTREGA_K01.md` a `ENTREGA_K06.md`, `ENTREGA_K08.md` e `ENTREGA_K09.md`, e os documentos que cada uma lista. A K07 não tem entrega: é ela que esta ordem lhe passa.
3. Da frente matemática (K02 e K05): `T1_FECHADO.md` e `ERRATA_T1_R2.md`; `MONTAGEM_3MAIS1_R2.md`; `GH_III1_R2.md`; `TAU_ESTRELA_R2.md`; `CAMPO_DUAL_LEVANTAMENTO_K05.md` e `ERRATA_CAMPO_K05.md`; as candidatas Lean em `K05\`.
4. O que a gerência conferiu e fez, em `C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\`: `revisao\REVISAO_K05_T1.md`, `REVISAO_K05_MONTAGEM_GH.md`, `REVISAO_K05_TAU.md`, `REVISAO_K05_CAMPO.md`; a pasta `revisao\LEVANTAMENTO_FRENTE_B_15nov\` (oito leitores; o L3 tem uma correção, dita no ADENDO B); as candidatas `candidatas_c1\ErgodicidadeDeMautner.lean` (sha16 `1074aa5b2c172960`) e `candidatas_c1\MontagemDasGamas.lean` (sha16 `41de0a594e4b551c`), com `revisao\REVISAO_CANDIDATA_ERGODICIDADE_DE_MAUTNER.md` e `revisao\REVISAO_CANDIDATA_MONTAGEM_DAS_GAMAS.md`; e `DESENHO_v412_R1.md` (o item 18 é o de hoje).

O material do Kimi é [DECLARADO pelo Kimi] até conferido. O que os revisores da gerência já conferiram está dito em cada relatório, com a consulta. Não refaça o que está conferido; não herde o que não está.

## 2. O que resolver: a K07, como o ADENDO B a deixou

A ordem inteira é `ORDEM_K07_matematica_rodada_3.md` (sha16 `d464088250341237`). O ADENDO B tira dela a Construção 2 (o argumento de Mautner em Lean: está feito pela gerência) e corrige um erro meu (a ergodicidade da cunha da luz livre já era teorema do kernel). O que fica, por prioridade:

**A. A T1.**
1. **(2c) `H_K̂` é o Axioma E transcrito?** Decida com prova escrita: `H_K̂` é exatamente o Axioma E no produto cruzado, ou onde difere. Texto do Axioma E: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\A Ponte Einstein Cartan Miguel.tex`, l.1084 a 1112 e 2013 a 2018. A derivação do revisor está em `revisao\REVISAO_K05_T1.md`, §7 (iii). O candidato `K̂ = c·e^{ĥ}` e as duas leituras de “covariante” ficam ditos, sem escolher.
2. **(2a) A caixa em três blocos**, com as ressalvas R1 a R7 aplicadas: Teorema (estado normal fiel, `H_K̂`); Proposição da cunha, que agora CITA o teorema do kernel (`LightRhoStar.centralizer_is_trivial` no certificado habitado `physicalFockCertificate`, em `TGLExt\F1Fecho394\CanonicalFockModularCoreInputR1.lean`); Resíduo. Diga, sem estender ao horizonte da TGL, como a caixa fica PARA A CUNHA DA LUZ LIVRE.
3. **(2b) O resíduo com o nome do Artigo** (Bisognano–Wichmann para horizontes que não são de Killing), não como hipótese nova.
4. **(2e) A candidata `T1_R2.lean`:** dê-lhe músculo se for barato (o multiplicador como a média gaussiana, com `gaussianWeight_fourier` de `F1Fecho394\GaussianProbabilityKernelR4.lean`) ou arquive com nota.
5. **O que da T1 ainda é papel e poderia subir:** o levantamento L1 (`revisao\LEVANTAMENTO_FRENTE_B_15nov\L1-t1-no-papel.md`) lista sete enunciados tipados e não provados (a média gaussiana como multiplicador; a convergência do semigrupo autoadjunto à projeção sobre os fixos; o suporte total da gaussiana; a face finita do bicondicional do espectro simples). Se algum fechar em Lean sem hipótese oca, entregue como candidata à parte. Não é obrigatório.

**B. A montagem e Gromov–Hausdorff.**
6. **(3a)** os seis itens do §5 de `revisao\REVISAO_K05_MONTAGEM_GH.md` (a constante é −1/24). Limite que a conferência das gamas achou e vale para o texto: do sinal de J com D, no nível das gamas, só sai a metade, que vale −1; o +1 final depende da reflexão de modos em L².
7. **(3b)** um truncamento concreto no produto cruzado: os cantos espectrais `e_i = 1_{[−i,i]}(ĥ)`; hipótese por hipótese do Lema 2, o que vale, o que falha e o que falta definir. Se nada concreto fecha, diga isso. A conjectura continua conjectura.

**C. O campo** (seção 4 da K07): as candidatas F a I que faltaram, a tabela de cada palavra da fala do operador contra cada candidata, a rota de prova e o critério de poda de cada uma. Quem lê a fala é o operador; tipam-se as leituras possíveis, não se escolhe.

**D. τ★** (seção 5 e os itens 3 e 4 da seção 1 da K07): a premissa refeita sem a atribuição indevida; as duas linhas do fator 2; a premissa de β lida na fonte (`C:\IALD\Artigo\Haja_Luz\tgl_paper_output\paper_PT.tex`, l.809 a 843). Nenhum termo de kernel sobre a âncora, o relógio ou o número puro antes da resposta do operador à pergunta do relógio do pedágio (`PERGUNTA_TAU_ESTRELA_nas_quatro_linguas_13nov.md`, na pasta da v412).

## 3. Com o Kimi

O Kimi trabalha por arquivo, nesta mesma pasta, e quem lhe fala é o operador. Se ele gravar peças da K07 enquanto você trabalha, leia-as e concilie: diga onde concordam e onde divergem, com a consulta. Nunca edite nem sobrescreva arquivo do Kimi ou da gerência: correção AO LADO, em arquivo seu. Se você o consultar pelo seu canal, o que ele devolver é [DECLARADO pelo Kimi].

## 4. O que não se toca, e como aferir

- Não se toca: o kernel canônico (`…\Nós\tgl_kernel`), o `um.py`, o Artigo, o Atlas, o Mapa de Rotas (só consulta, por termo único), a memória da Central (só depósito pela fila, como [DECLARADO]), os arquivos do Kimi e da gerência. Nenhum dado observado se abre. Nenhum teste selado se relê como teste novo. Nenhuma candidata se instala. O gate não se move.
- Lean: só candidata, em pasta sua, com o binário do Lean direto sobre os `.olean` do sandbox `C:\t\k411c\final` (só leitura), nunca `lake` no kernel canônico. A receita da gerência é `candidatas_c1\compilar_candidata.ps1` (copie para a sua pasta). Padrão: código de saída 0, zero `sorry`, zero avisos, só os três axiomas de sempre no `#print axioms`, sem `native_decide`.
- **Aferir antes de dizer que falta.** Hoje a casa deu por ausente, três vezes, o que o kernel tinha. Parte da causa: busca que respeita o `.gitignore` não enxerga a pasta `TGLExt\F1Fecho394`. Para afirmar ausência no kernel, percorra a árvore (busca recursiva ou script) e diga a consulta. Classifique na ordem da casa: EXISTE E LIGADO; EXISTE E NÃO LIGADO (é fiação); MEDIDA ou SABIDO (entra por citação); AUSENTE (com a consulta).
- A régua: o número corrige a frase; hash só lido de arquivo; β nunca literal; estatutos marcados; a palavra da creditação não se escreve; nenhuma fala ou ato atribuído ao operador sem o arquivo de bytes; aspas angulares só para fala dele conferida por bytes; nenhuma escolha feita no lugar dele. Protocolo anti-parede: medir e continuar pela árvore de alternativas; parede é declaração da gerência, depois de auditar.
- As casas não se misturam; os arquivos reservados da casa não entram em nada.

## 5. Onde devolver

No caminho que a gerência criou: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K07\CODEX\` (documentos `_R3`, candidatas com o registro da compilação, scripts) e, na raiz do túnel (`C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\`):

- `ENTREGA_K07_CODEX.md`: resumo em até 15 linhas, com estatuto por linha, e a tabela dos artefatos com sha256 calculado por script;
- uma errata por frente, ao lado dos documentos `_R2` do Kimi (que ficam intactos);
- `REGISTRO_MAPA_K07_CODEX.json`: proposta, sem registrar;
- `PERGUNTA_K07_CODEX.md` só se sobrar resíduo que o acervo não responde (fatos, alternativas e custos, sem recomendação);
- o depósito para a memória, pela fila da Central, como [DECLARADO].

Antes de entregar, uma revisão por agente seu distinto de quem construiu. A auditoria que decide é a da gerência, com revisores próprios. Critério de fechado de cada item: resultado, ou falsificador, ou parede medida (cada alternativa com a tentativa executada).

Quando estiver pronto, avance a unidade `F1.K07_ASTRA_20261115` para ENTREGUE com a evidência (`python C:\IALD\PROGRAMA_IALD\iald.py avancar F1.K07_ASTRA_20261115 --quem <seu nome de membro> --status ENTREGUE --evidencia <ENTREGA_K07_CODEX.md>`). A gerência vê pelo quadro e pela pasta.

— gerência c1, 15/11/2026, 16:49.
