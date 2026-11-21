# Ordem da Etapa 3 da v413: preparar a instalação, o rito e o pós-rito (gerência c1, 20/11/2026)

Você é o **construtor da Etapa 3 da v413**, agente da gerência c1. Português na prosa; inglês no código. Windows; Python em
`C:\Python314\python.exe -B -X utf8 arquivo.py`, scripts pela ferramenta Write e rodados com `< /dev/null`; nunca `python -c`,
nunca heredoc, nada interativo.

## O que é

A Etapa 2 (o candidato, outro agente, em curso) gera o `um.py` candidato da v413 e fecha em `PREPARACAO_v413_PRONTA.json`.
Esta ordem prepara TUDO o que vem depois do candidato, para a gerência executar: a instalação no Nós, a reversão, o rito, o
conferidor pós-rito, a regeneração de todos os textos derivados com o rótulo v413, o handoff à custódia. **Você NÃO instala,
NÃO roda o rito e NÃO toca o Nós.** Você deriva e ensaia; a gerência executa.

## Leia primeiro

1. `C:\IALD\Central de Patentes\work\custodia_v413_preparo_20nov\HANDOFF_DA_CUSTODIA_A_GERENCIA_ENTREGA_DO_UM_PY_v413.md`,
   inteiro: é o que a custódia exige da entrega (as três marcas, o compositor R2 do handoff, os marcadores, os diffs, o par
   `_V413_FONTES`/`_V413_VERBATINS2`, o `kh_n1_cobertura_v413`, a guarda privada, as superfícies, a entrega).
2. `...\cadeia_de_selo\v413\CONTRATO_v413_R1.md` (congelado) e `...\v413\INVENTARIO_CADEIA_v413.json` (o inventário que a Etapa 1
   fez dos 36 scripts da cadeia que a v413 precisa, com o que muda em cada um).
3. Os moldes da v412 (a «etapa 3 enxuta»): `...\v412\PLANO_ETAPA3_ENXUTA_v412.md`, `esperados_v412_foco.py`, `instalar_v412.py`,
   `adaptar_instalar_e_reverter_v412.py`, `reverter_v412.py`, `rito_v412.sh`, `conferir_pos_rito_v412_foco.py`,
   `montar_handoff_e_linhagem_v412.py` (o compositor R2), a pasta `...\v412\pos_rito\` (cadeia do pós-rito, superfícies, textos,
   blocos da custódia, fila da memória) e o `RECIBO_HANDOFF_v412.json`.
4. A ordem do autor de 19/11 sobre os textos emitidos: a árvore da prova da QG (`Nós\A_PROVA_DA_QG_TGL_arvore.md`) subiu na v412
   com o rótulo da v411 porque o pós-rito não rodou o `arvore_da_prova.py`; na v413, o pós-rito roda o `arvore_da_prova.py` e uma
   guarda recusa todo `.md` declarado sem a versão do selo no título. A G1 da custódia já para se um documento declarado traz no
   título a versão de outro selo (commit `66671b55d` da Central: `tools\custodia_g1\`). O autor reforçou em 20/11: «regenerar
   corretamente os md's todos apontando a v413 e incorporando as novas derivações corretamente».
5. Lições: `C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\licoes-custodia-v412-g1-19nov.md`,
   `licoes-cadeia-v411-13nov.md`, `stdout-do-rito-e-canonico.md`, `licao-guarda-do-rito-e-timeout-v372.md`, `rito-checkpoints-v321.md`
   e o tópico `v384-pilar-quantico-gpu-02out.md` (só o que diz do marcador do rito e do pilar).

## O que fazer, na pasta `...\cadeia_de_selo\v413\` (subpastas `pos_rito\`, `etapa3\`)

1. **Esperados** (`esperados_v413_foco.py`): o candidato (sha16 e bytes), a origem (o `um.py` v412 selado), a escada, as bandeiras
   novas e os 21 módulos mais o corrigido com o sha256 do manifesto, a raiz e o Audit antes e depois, o pilar, o gate da v412, as
   palavras de veredito do contrato R1. Lê tudo de arquivo; parametrizado pelo caminho do candidato (o candidato pode ainda não
   existir: o script recusa com mensagem clara até ele existir).
2. **Instalador e reversão** (`instalar_v413.py`, `reverter_v413.py`): pelo molde da v412, com as travas de processo, origem,
   candidato e pilar; os 21 novos ausentes do Nós antes; e o CASO NOVO: o `TGLExt/OResumoEPsiBit.lean` que existe e é SUBSTITUÍDO (o
   instalador confere o sha antigo, guarda os bytes, e a reversão o devolve). Backups de bytes; ensaio a seco obrigatório.
3. **O rito** (`rito_v413.sh`): pelo molde da v412 (corpo genérico; cabeçalho e marca da v413), com o stdout canônico gravado em
   `Nós\rodada_v413_stdout.txt`, a guarda do rito e o tempo-limite das lições, e o portão do pilar (o ambiente da placa é o do
   cache; se não for, PARAR e avisar; há treino em curso na placa: não tocar, não medir, não parar).
4. **O conferidor pós-rito** (`conferir_pos_rito_v413_foco.py`): o núcleo pós-rito contra o núcleo selado da v412: nenhum
   veredito herdado muda salvo por desenho; todas as bandeiras herdadas e as novas de pé; o gate igual; o selo com `um_version`
   v413 e o `um.py` batendo com o pino; os 22 módulos no Nós com o sha256 do manifesto; a escada medida; sem `sorry`.
5. **O pós-rito dos textos**: a cadeia que regenera, com o rótulo v413 no título e as derivações novas, todos os textos derivados
   que o pós-rito da v412 regenera mais a árvore da prova (`arvore_da_prova.py`), e a guarda que recusa `.md` declarado com outra
   versão no título; os `DIFF_v412_v413.diff` e `DIFF_KERNEL_v413.txt` em `...\cadeia_de_selo\v413\`; o compositor R2 do handoff
   (`montar_handoff_e_linhagem_v413.py`), que grava o `Nós\HANDOFF_v413_CUSTODIA.md`, o bloco «v413 SELADA» no diário da linhagem e o
   adendo do desenho, conferindo pelas funções da própria G1 antes de gravar; os parágrafos do B(n) com o sha16 dos três recibos
   (parametrizados: os recibos só existem depois do B(n) pós-selo, que a gerência roda).
6. **A guarda privada** (`guarda_privada_v413.py`): a contagem da G1 (`EP.carregar_marcadores_privados` e `EP.guarda_conta`, sem
   imprimir padrão nenhum) sobre o candidato, o core e o kernel, contra a v412 do espelho; recibo com o número de termos novos.
7. **O roteiro** `ROTEIRO_EXECUCAO_v413.md`: a sequência exata de comandos que a gerência roda (pré-condições, instalar, rito,
   conferir, pós-rito, handoff), com o que cada um grava e como se reverte. Ensaio a seco de tudo o que puder rodar sem o
   candidato (testes sem candidato, como os `teste_*_sem_candidato_v412.py`).
8. Feche em `...\v413\PRONTO_ETAPA3_v413.json` (cada script com sha16; o que foi ensaiado; o que depende do candidato; o que depende
   do B(n)) e PARE.

## Regras invioláveis

- Nada no Nós (`C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\`): só leitura. Nada no `C:\t\k413c` (a Etapa 2 usa). Não edite os
  arquivos de outros agentes (`insumos\`, `bancada\`, o candidato, os da Etapa 2) nem as pastas da v412 (só leitura). Sem
  publicação, commit, push; sem tocar o espelho the_boundary nem a Central pública.
- Hash e número lidos de arquivo por script. Backup de bytes antes de tocar arquivo existente; escrita por temporário.
- Nunca matar processo por nome; não tocar o treino em `C:\IALD\TGL_IALD_NATIVE_QWEN5090`; não usar a placa; a Bancada só por GET
  (e você não precisa dela).
- Vereditos e textos: proibidos `CONFIRMED`, `PROVED_BY`, `P_EQUALS_NP`, `TURING_SOLVED`, `CLAY_SOLVED`, `MILLENNIUM`; nenhuma
  história de conversa nos textos que vão ao programa ou às superfícies públicas (método de 17/11).
- Confidenciais: nunca leia, copie, cite ou imprima os confidenciais da casa nem os padrões da guarda privada.
- Corrija a CAUSA, nunca relaxe um teste. Se algo for impossível como está, pare naquele item e siga com o resto.
- Memória, Atlas, ACOM e Mapa: não escreva; devolva o que examinou.

## Entrega (até 15 linhas)

O caminho do fecho com sha16; os scripts derivados; o que foi ensaiado e o resultado; o que depende do candidato e do B(n); a
lista dos textos que o pós-rito regenera; desvios e por quê.
