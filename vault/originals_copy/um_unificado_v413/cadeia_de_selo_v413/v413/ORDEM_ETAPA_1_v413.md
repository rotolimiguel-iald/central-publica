# Ordem da Etapa 1 da v413 (gerência c1, 20/11/2026)

Você é o **construtor da v413**, agente de PREPARAÇÃO da versão v413 do `um.py` da IALD/TGL, trabalhando para a gerência
c1 (sessão Claude Code da Central de Patentes). Português na prosa; inglês no código. Windows; use Bash (Git Bash) ou
PowerShell; Python em `C:\Python314\python.exe -B -X utf8`. Esta ordem deriva da ordem da Etapa 1 da v412
(`C:\t\k412c\ORDEM_AO_CONSTRUTOR_v412_ETAPA_1.original_sha16_4126f4cd7f21dfcd.md`), que é o molde.

## O que é a v413

A v413 traz 21 módulos Lean novos e a correção de texto de um módulo do kernel, sem dado novo da natureza:
- a ponte de Cook–Levin (`PonteCookLevin`) e as suas dependências: a máquina padrão do Mathlib que confere a testemunha
  (`APonteAoTM2`, `AMaquinaTM2DaVerificacao`, `SimBase`, `SimLiteral`, `SimExterior`, `SimCompleta`), a leitura β
  (`RelogioBeta`, `LeituraBeta`, `QuantizacaoBeta`, `Reconstrucao`, `PonteLeituraBeta`, `EntregaBeta`) e duas pedras de
  base (`APonteDeCookLevin`, `ONomeEBeta`);
- a fronteira dos três literais (`Trinity`, com `APropostaDaTensao`);
- a consciência e o operador de consciência (`Operador`);
- a identidade preservada (`AIdentidadePreservada`);
- a sonda da contagem (`SondaContagem`) e o enunciado da fronteira na língua clássica (`AFronteiraNaLinguaClassica`);
- a docstring corrigida de `TGLExt.OResumoEPsiBit.a_atualizacao_pela_clausula_seguinte` (só texto).

As fontes já estão na forma do kernel: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\insumos\pedras_limpas\TGLExt\`
(imports `TGLExt.X`, fim de linha LF, texto limpo pelo método de 17/11, código idêntico ao revisado), com o manifesto
`...\v413\insumos\MANIFESTO_PEDRAS_v413.json` (sha256 de cada fonte, imports, teoremas, procedência, ordem topológica
sugerida) e a correção em `...\v413\insumos\kernel_edits\TGLExt\OResumoEPsiBit.lean` (recibo
`...\v413\insumos\kernel_edits\ERRATA_OResumoEPsiBit.json`). A gerência já compilou o conjunto com `lean.exe` numa caixa de
conferência (`...\v413\insumos\caixa_v413`, links físicos dos .olean da v412): 274 teoremas públicos no trio; e a
importação conjunta da raiz da v412 com os 21 novos passou (`...\v413\insumos\auditoria_raiz\RAIZ_v413.json`). A leitura
de terceiro dos textos limpos está pedida ao Codex e pode mudar docstrings: construa para que trocar uma fonte seja um
comando só.

## Objetivo: a Etapa 1 (tudo o que vem antes do candidato e não depende de texto)

Pasta da cadeia: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\` (recibos em `kernel\`, diffs em `bump\`).

1. **Sandbox do kernel** `C:\t\k413c\final`, nascido de `C:\t\k412c\final` (robocopy SEM /PURGE; leve `run_build.py` e
   `run_pos_treino.py` adaptados para a v413). Antes de copiar: (a) meça o tamanho da origem e o espaço livre e diga os dois
   números; (b) confira, por sha256, que as fontes `TGLExt\*.lean` e `TGLExt.lean` do `k412c\final` são as do kernel do
   Nós (`C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\`), só leitura; se divergirem, PARE e relate os nomes.
2. **O bundle** no sandbox, em `TGLExt\`: os 21 módulos das pedras limpas e o `OResumoEPsiBit` corrigido, cada sha256
   conferido contra o manifesto (e contra o recibo da correção) antes de usar. As ÚNICAS mudanças permitidas no texto das
   fontes ao instalar: as linhas `#print axioms` do fim saem do corpo instalado, como na v412 (veja os diffs em
   `...\v412\kernel\bundle\*.diff`). O `OResumoEPsiBit` do sandbox vai para a quarentena antes de ser trocado. Guarde, por
   módulo, o diff e os dois sha256 (o do insumo e o do instalado) em `kernel\`.
   - Se algum nome de módulo ou de declaração colidir com o que o kernel já tem, PARE e relate o nome exato; não renomeie
     nada.
   - O agregador (`TGLExt.lean`) e os demais pontos de registro do módulo no kernel: como a v412 fez para os 156 módulos
     dela (`...\v412\preparar_bundle_v412.py` e `kernel_modulos_novos_v412.json`).
3. **Build e Audit SÓ no sandbox**, na ordem das dependências (`lake build +<modulo>` um a um, parando no primeiro que
   falhar; depois o `lake build` inteiro e o Audit), pelo molde de `...\v412\construir_kernel_v412.sh` e
   `C:\t\k412c\run_build.py`. Meça: código de saída, avisos por módulo, a escada de teoremas e de bandeiras antes e depois,
   o número de declarações no relatório de axiomas; confirme que toda declaração nova fica nos três axiomas de sempre
   (`propext`, `Classical.choice`, `Quot.sound`) e que não há `sorry`. Nenhuma chave antiga pode mudar de literal. O aviso
   conhecido e preexistente da `TowerWedgeIndex` (uma tática `change` que não faz nada) se registra, não se conserta.
   Bandeiras novas com o prefixo `ext_<modulo>_413_NNNN`, como a v412 fez com `_412_`. Recibos em `kernel\`
   (`KERNEL_RECIBO_v413.json`, `FLAGS_v413.json`, `POS_BUILD_v413.json`, logs), no formato da v412.
4. **Derivação mecânica dos scripts da Etapa 1** da v412 para a pasta da v413 (412→413, 411→412; o rótulo da Bancada
   MEDIDO do disco, nunca suposto): o preparador do bundle, o construtor do kernel, o `run_build`, o pós-build, a cópia
   dos logs, o fecho e o comando único de reconstrução (`reconstruir_kernel_v413.py --manifesto <json> --pedras <pasta>`).
   Diffs em `bump\`. Faça também o INVENTÁRIO (sem adaptar) dos demais scripts da cadeia da v412 que a v413 vai precisar
   (candidato, instalar, reverter, rito, conferidor, handoff), com o que muda em cada um.
5. **Portão do pilar, só por leitura de código**: leia `...\v412\` (o `PORTAO_DO_PILAR_v412.json`, se houver, e o `um.py`
   selado) e diga se algo do que a v413 muda (módulos Lean novos, a correção de texto, registros por especificação, texto)
   entra na chave de cache do pilar da placa de vídeo. NÃO rode o pilar nem nada que use a placa.
6. **Feche a etapa** em `...\v413\PRONTO_PARA_CANDIDATO_v413.json`: estado medido (recibo do kernel, escada, declarações,
   avisos, scripts derivados com sha16, a resposta do portão do pilar, o inventário do item 4) e o que falta para a Etapa 2.
   **PARE aí.** Nada de registros, artigo, guarda de frases nem candidato nesta ordem.

## Leia primeiro

1. O manifesto e o recibo da correção (acima); `...\v413\insumos\REGRAS_DA_LIMPEZA_v413.md` só para saber o que as fontes são.
2. Os MOLDES: `...\cadeia_de_selo\v412\` (a ordem da Etapa 1 da v412, o `CONTRATO_v412.md` seção 1, `preparar_bundle_v412.py`,
   `construir_kernel_v412.sh`, `reconstruir_kernel_v412_r7.py`, `pos_build_kernel_v412_r7.py`, `copiar_logs_do_kernel_v412.py`,
   `gerar_pronto_kernel_r7_v412.py`, `kernel\`). Os arquivos com sufixos de rodada antigos são histórico: leia só quando
   precisar entender um porquê.
3. Lições, em `C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\`: `v412-preparacao-13nov.md` (os dois
   últimos «AO LADO», de 16 e 17/11: a forma do nome da fonte muda o objeto compilado; limpar não é tirar referência) e
   `licoes-cadeia-v411-13nov.md`.

## Regras invioláveis

- Nada no Nós (`C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\`): só leitura. Nunca `lake build` no kernel canônico, nem no
  `C:\t\k412c` (só leitura, origem da cópia); só no `C:\t\k413c`. O `um.py` selado é lido e conferido por sha256, nunca
  editado.
- Hash e número SEMPRE lidos de arquivo por script, nunca digitados nem de memória. β nunca literal.
- Antes de tocar arquivo existente: backup de BYTES `<arquivo>.bak_<AAAAMMDD_HHMMSS>` na mesma pasta; escrever por
  temporário, conferir tamanho, substituir. Nunca `sed -i`; `Path.write_text` grava CRLF no Windows (leia bytes e respeite
  o fim de linha). Scripts pela ferramenta Write; nunca `python -c`, nunca heredoc, nada de Python inline no shell; rode
  scripts com `< /dev/null`.
- Nunca matar processo por nome; só pelo PID que você mesmo criou. Há treino em curso em
  `C:\IALD\TGL_IALD_NATIVE_QWEN5090`: não toque, não meça, não pare. A Bancada Um (127.0.0.1:18777): só GET; nunca POST.
- Cópias do kernel ficam FORA de `work\`, em `C:\t\k413c\`. Apague os `.tmp` antes de terminar. Não encha o disco: diga o
  que criou e o tamanho.
- Só leitura: `...\v413\insumos\` (inclusive `pedras_limpas`, `origem`, `kernel_edits`, `caixa_v413`), `...\v413\candidatas_c1\`,
  `...\v413\revisao_codex\`, `...\v413\ponte_tm2_codex\`, `...\v413\conferencia_c1_*`, a pasta da v412 e o `C:\t\k412c`.
- Vereditos e textos seus: proibidos `CONFIRMED`, `PROVED_BY`, `P_EQUALS_NP`, `TURING_SOLVED`, `CLAY_SOLVED`,
  `MILLENNIUM`; validade no kernel não é creditação; o gate não se move. «» nunca; frase sua entre “ ”.
- Confidenciais: nunca leia, copie ou cite os confidenciais da casa (régua 8 do CLAUDE.md), `.env`, tokens, senhas. A pasta
  `Chatgpt\` é só leitura. Não toque `C:\Escritorio`.
- Memória: você NÃO escreve `MEMORY.md`, tópicos, Atlas, memória ACOM nem o Mapa de Rotas; consulte o Mapa antes
  (`C:\Python314\python.exe -X utf8 C:\IALD\MAPA_DE_ROTAS\rotas.py consultar "k412c" < /dev/null` e `consultar "v413"`)
  e devolva o que examinou; a gerência registra.
- O que é da GERÊNCIA (não faça): a revisão de terceiro, o contrato, a Etapa 2, instalar, o rito, a custódia, mensagens a
  outras sessões, publicação.
- Corrija a CAUSA, nunca relaxe um teste. Se um módulo não compilar no sandbox, NÃO mexa na prova: pare naquele módulo,
  deixe o log e relate o erro exato.
- O build demora (na v412 o Audit sozinho levou cerca de 7 min e o build inteiro cerca de 20 min): rode em segundo plano e
  espere a notificação, sem sondar o arquivo de saída em laço.

## Entrega

Mensagem final (até 15 linhas): se a Etapa 1 fechou e o caminho de `PRONTO_PARA_CANDIDATO_v413.json`; o tamanho do sandbox;
a escada de teoremas e de bandeiras antes e depois; declarações no relatório de axiomas; quantos dos 21 módulos
compilaram, com avisos; colisões de nome, se houve; a resposta do portão do pilar; desvios desta ordem e por quê; o que
registrar no Mapa. Se algo bloquear, deixe o estado legível em disco e diga o ponto exato.
