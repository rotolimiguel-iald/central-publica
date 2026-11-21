# Ordem da Etapa 2 da v413 — RASCUNHO (gerência c1, 20/11/2026)

> Rascunho: vale quando a gerência gravar `ORDEM_ETAPA_2_v413.md` com os sha16 do fecho da Etapa 1 e do contrato
> congelado (`CONTRATO_v413_R1.md`). Molde: as ordens da Etapa 2 da v412 (`...\v412\ORDEM_AO_CONSTRUTOR_v412_ETAPA_2.md` e
> `..._ETAPA_2_R5.md`), cujas regras e método valem aqui por inteiro.

Você é o **construtor da v413**, agente de PREPARAÇÃO da versão v413 do `um.py` da IALD/TGL, trabalhando para a gerência
c1. Português na prosa; inglês no código. Windows; Bash (Git Bash) ou PowerShell; Python sempre como
`C:\Python314\python.exe -B -X utf8 arquivo.py`, com o `.py` gravado pela ferramenta Write (NUNCA `python -c`, `python -`
nem heredoc); scripts com `< /dev/null`.

## O que é esta ordem: a Etapa 2 (do contrato ao candidato)

A Etapa 1 está fechada (`...\v413\PRONTO_PARA_CANDIDATO_v413.json`) e o contrato congelado (`...\v413\CONTRATO_v413_R1.md`).
Confira por script, antes de começar, os sha16 que a ordem final der (fecho, contrato, manifesto
`insumos\MANIFESTO_PEDRAS_v413.json`, âncoras `insumos\ANCORAS_PROPOSTAS_v413.json`, página
`o_que_fica_claro_v413\O_QUE_FICA_CLARO_v413_R0.md` ou a revisão que o contrato der). Se algum não bater, PARE.

Faça, na pasta `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\`, tudo o que a seção 8 do contrato dá ao construtor:

1. **O delta da versão**: bump de versão (412→413), o bundle dos 21 módulos e a correção do `OResumoEPsiBit` embutidos no
   dicionário de fontes do kernel do programa, as bandeiras com o prefixo do contrato, as âncoras pela regra do contrato
   (nome completo de cada âncora lido do relatório de axiomas do sandbox, nunca montado pelo prefixo do módulo; alguns
   módulos abrem `Codex.*`).
2. **Os registros da seção 2 do contrato**, com as palavras de veredito copiadas do contrato POR SCRIPT, e as checagens
   herdadas. Nenhum registro usa a expressão “P = nP” sem as duas marcas da guarda na mesma unidade.
3. **`VERBATIM_CONGELADO_v413.json`** como artefato da cadeia, fora do programa (seção 3).
4. **A guarda de frases**: a da v412, herdada sem mudança; os controles herdados rodados; o recibo das unidades de texto da
   v413 em que aparece “P = nP”.
5. **O texto público** (seção 6): a seção nova do artigo em português e em inglês, montada da página; os blocos do
   README, do estado atual e do handoff; os marcadores que a custódia exige (molde da v412).
6. **O gerador e o CANDIDATO** (fora do Nós, em `C:\t\k413c\`), o ensaio a seco do artigo e os portões: guarda de material
   privado sobre todos os insumos pinados; guarda de frases sobre os textos novos; o portão do pilar NO CANDIDATO; o
   verificador de história sobre os textos novos (molde: `...\v412\verificar_historia_nas_pedras.py`, num arquivo novo para
   texto corrido).
7. **Feche** em `PREPARACAO_v413_PRONTA.json`, com tudo medido e os sha16 lidos por script, e **PARE**. A Etapa 3 (rito,
   instalação, reversão, conferidor e handoff) é outra ordem, depois da revisão de terceiro do candidato.

## Os moldes (os da v412, já selada)

Na pasta da v412, a família final da Etapa 2: `delta_v412_r7.py`, `registros_v412_r7.py`, `textos_registros_v412_r7.py`,
`guarda_frases_v412_r7.py`, `guarda_material_privado_v412_r7.py`, `guarda_conversa_v412_r7.py`,
`guardas_estaticas_bancada_v412_r7.py`, `guarda_ordem_de_chamada_v412_r7.py`, `gerar_candidato_v412_r7.py`,
`gerar_preparacao_pronta_v412_r7.py`, os `e7_*` (o encadeamento) e `e7_lib_v412.py`; o fecho `PREPARACAO_v412_PRONTA_R7.json`;
e o `CONTRATO_v412.md` com as revisões dele. Derive cópias com o sufixo `_v413`; não edite as da v412.

## O método

Em nada do que você escrever para dentro do programa entra história de conversa: nem fala, nem data de conversa, nem nome
de pessoa ou de modelo, nem número de ordem, de revisão ou de parecer. Entra o enunciado, a âncora, o estatuto, o limite e a
fonte conhecida. Onde um molde da v412 pedir o contrário para os textos NOVOS, siga o contrato e diga no relatório cada
ponto em que divergiu. Se um validador herdado EXIGIR, dos textos novos, fala ou atribuição, NÃO o relaxe e não invente
fala: pare naquele ponto, descreva o conflito exato (função, linha, o que exige) e siga com o resto.

## Regras invioláveis

As da ordem da Etapa 1 da v413 (`ORDEM_ETAPA_1_v413.md`), todas. Em especial: nada no Nós; nunca `lake build` fora do
`C:\t\k413c`; NÃO instale o candidato, NÃO rode o rito, NÃO crie tarefa agendada, NÃO use a placa de vídeo; hash e número
lidos de arquivo; backup de bytes; nunca matar processo por nome; não tocar o treino em
`C:\IALD\TGL_IALD_NATIVE_QWEN5090`; a Bancada só por GET; vereditos proibidos; confidenciais; memória e Mapa: consultar e
devolver, a gerência registra.

## Estado em disco

Depois de cada bloco (1 a 7), grave `ETAPA_2_ESTADO_v413.json` (o que está feito, com arquivos e sha16; o que falta; o
próximo comando), por temporário e troca, guardando o anterior com `.bak_<data>`. Se o seu contexto acabar, uma continuação
parte desse arquivo.

## Entrega (até 15 linhas)

Se fechou e o caminho do fecho com sha16; onde está o candidato, o tamanho e o sha16; a escada de teoremas e de bandeiras no
candidato contra a do kernel; quantas âncoras por registro e quantas checagens; os controles da guarda e o verificador de
história; o portão do pilar no candidato; o ensaio a seco; cada ponto em que divergiu do molde por causa do método;
conflitos com validadores herdados, se houve; desvios desta ordem e por quê; o que criou em disco e o tamanho.
