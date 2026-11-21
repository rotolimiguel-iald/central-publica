# Revisão independente do molde do B(n) da v413 (o salto v411 → v413) — 20/11/2026

Revisor independente único, a serviço da gerência c1. Não construí nada do molde. Escopo: só leitura e testes numa pasta
minha (o scratchpad da sessão). Nada foi ligado, parado ou escrito na Bancada, no Nós, na v412, em `C:\t\k41*`, no quadro
ou nos arquivos do molde; nenhum GET nem POST na porta 18777; o pré-selo, o pós-selo e o APLICAR não rodaram. Não inscrevi
referência na memória ACOM (o `init` grava fora da minha pasta); o registro é da gerência.

Estatutos: [REAL] = lido ou medido agora, por script; [DERIVADO] = conclusão da leitura do código; [OPEN] = não se sabe.

**Objeto conferido [REAL]:** os 26 scripts do `PRONTO_BN_v413.json` (sha16 `e7f457baffcd868a`) têm, no disco, o sha16 e os
bytes que o fecho declara (26 de 26, todos com fim de linha LF); os 6 artefatos do pré-selo (cadeia, pino da cadeia,
bateria da v412 e seus pinos) também conferem. O ensaio hermético (76/76) e o controle negativo (13/13) foram gerados com
esses mesmos scripts (sha16 do conferidor `df19601a074ea6e5`, do mutador `10a98c65d4feff28`). Nenhum script que o ensaio
exercita mudou depois das 21:28; o ensaio é das 21:34, e só o gerador do PRONTO é posterior (21:36).

---

## Veredito: APROVADO_COM_RESSALVAS

- **Nenhum achado ALTO.** Não achei caminho em que o molde grave na produção fora do APLICAR autorizado, nem em que dê
  «ok» falso: toda recusa que achei é visível e do lado seguro.
- **Quatro MÉDIOS:** dois operacionais (M1, o sandbox `vb24` compartilhado com a Etapa 2; M2, o tempo contra o limite da
  ferramenta), um de cobertura de teste (M3) e um de custódia dos insumos do salto (M4).
- **O pré-selo pode rodar** assim que M1 e M2 estiverem resolvidos (as duas são regra de execução, sem mudar código). Os
  consertos BAIXOS B1 a B3 são baratos e podem entrar antes. Se entrarem, rode de novo o ensaio hermético e o controle
  negativo, porque eles leem esses scripts.
- **Prazo [DERIVADO]:** o pré-selo continua preso ao Nós na v412 (N1). A bateria da v412 roda ali pela primeira vez (M3),
  então convém rodá-lo com folga antes da instalação da v413.

---

## 1. O pré-selo do salto

| o que | conferido | onde |
|---|---|---|
| cadeia v411→v412 | 2 elos. v411: cópias de `v412\base_v411`, mais o registro do instalador `v412\APLICADO_AO_CANONICO_20261118_235146.json` e os dois `.bak_20261118_235146` do Nós. v412: cópias de `v413\base_v412`, sem instalação. Pinada por sha256. Conferida pelas funções do esboço R3.6 pinado (carregar, início = Bancada B20, fim = Nós v412) | `gerar_e_pinar_cadeia_v413.py:45-62`; `PINO_CADEIA_DE_SELOS_v411_v412.json` [REAL] |
| runner do ensaio | `--versao v412 --fase pre_selo --modo ensaio`, a bateria da v412 em `v413\bateria_v412_pre_selo` (não é ancestral da `--saida`), a cadeia com o sha, `--saida v413\bateria_pre_selo\ensaio_1` (raiz admitida pelo esboço: `raizes_saida(v412, pre_selo)` = `cadeia_de_selo\v413`, esboço l.220-230) | `rodar_ensaio_1_pre_selo_v413.sh:17-35`. **Medido** com uma cópia em que só a chamada do esboço virou eco: todos os argumentos saem com os valores reais (o caminho do Nós com acento e espaço passa inteiro pelo `sh`) [REAL] |
| sandbox | `C:\t\vb24`, lido do `delta_bn` e conferido na forma `C:\t\vb<dígitos>`; o runner recusa se a pasta já existe; hoje ela não existe [REAL] | `delta_bn_v413.py:45`; `rodar_bn_pre_selo_v413.sh:35-42` |
| conferir do salto (C.1) | pela função do esboço, com `ja_sincronizada=False`, a cadeia pinada e o selo e o kernel anteriores de `v413\base_v412` (no salto, o anterior do um.py é o fim da cadeia: esboço l.1079-1080, 1135-1140); 26 condições e 9 controles com o código de recusa esperado | `conferir_recibo_pre_selo_salto_v413.py:77-211` |
| gerar_pino | aceita só `REPINADA_B<GER+1>__SALTO_v411_v412__ENSAIO__NADA_GRAVADO_NA_BANCADA`, com GER lido do `manifesto_anterior` do recibo e igual a `DBN.VEREDITO_PRE_SELO`; sai com rc 1 se o pino não serve ou se a produção mudou; o `inicio_utc` tem de cair entre as fotos | `gerar_pino_recibo_pre_selo_v413.py:64-67, 128-134, 179-185, 230` |
| nada grava na Bancada nem no Nós | [DERIVADO] passo a passo: as fotos, o conferir e o pino gravam no sandbox, em `OUTB` e em `v413\`; o esboço em ensaio grava só em `--saida` (`guarda_servico` só age no aplicar, l.2686); o `canonical.py` da Bancada é importado sem bytecode (`-B`, `sys.dont_write_bytecode`, esboço l.531). Os passos 8 e 9 rodam depois da foto final e só leem a produção | — |
| recusa com o Nós fora da v412 | o runner (`:20-24`) e os dois geradores param com PRAZO_DO_PRE_SELO_PERDIDO; o próprio esboço recusaria (`ler_nos`, l.562-566); o teste E6 mostra o rc 9 | — |

## 2. O pós-selo

- **Ordem 10 → 10a → evento → 10b → 10c → 11 [DERIVADO, imposta].** O evento exige o stdout do ENSAIO e o `b3_recibo`
  dele com rc 0 (`evento_c1_b3_v413.py:21-25`). O 10b exige `B3_AUTORIZADO`, `EVENTO`, `EVENTO_HASH`, o recibo da
  parada, o ENSAIO conferido de novo, o evento conferido no livro inteiro e posterior ao ensaio, e a porta fechada
  (`bn_v413.sh:104-112`). O religamento exige exatamente 1 APLICAR do salto cujo manifesto novo é o do disco
  (`recibo_religamento_v413.py:70-84`). O 11 exige os três recibos e o PID vivo (`bn_v413.sh:134-142`;
  `fechar_bn_v413.py:31-92`).
- **APLICAR:** só com o serviço parado. O bn testa a porta e o esboço sonda de novo antes de cada gravação. O evento é
  conferido por hash na cadeia do livro pelo próprio esboço (l.673-752).
- **Parada `ja_fora_do_ar`** (`recibo_parada_v413.py:77-96`). Exige:
  - a conferência A de hoje, pinada pelo sha256 passado, com veredito FORA_DO_AR ou FORA_DO_AR_APOS_REINICIO, porta
    fechada e nenhum processo;
  - o último PID conhecido (o da v411) ausente, ou de outro programa;
  - e recusa PID parado no ambiente.
- **Religamento** (`recibo_religamento_v413.py`):
  - AGUARDA (rc 20) sem a fala do modo da placa (`:55-58`);
  - lança `pythonw` destacado, com stdout e stderr anexados aos logs de `estado\` (`:97-103`);
  - no modo `cpu`, `CUDA_VISIBLE_DEVICES=-1` no processo lançado; no `normal`, a variável sai do ambiente (`:92-96`);
  - lê a identidade só de `/api/contratos` (`:110`).
  As chaves que ele espera (`ok`, `canonical_version`, `deployment_id`, `canonical_manifest_sha256`, `um_py_sha256`,
  `seal_sha256`) são as que `canonical.py` devolve em `check()` (Bancada `bancada\canonical.py:91-99`; a rota está em
  `um_bancada.py:264-265`; o Host `127.0.0.1:18777` é aceito, l.21). O `pythonw.exe` de `C:\Python314` é o interpretador
  real, não um lançador de venv (não há `pyvenv.cfg`), e por isso o PID lançado é o PID da porta [REAL].
- **Fechamento:** os três recibos juntos e o salto exigido; o pino conjunto com o seq e o hash do evento, conferido de
  novo depois de gravado, com rc 2 sem gravar nada se faltar recibo; a cópia na pasta `bench` do evento 1687, conferida por
  sha. As chaves de `aplicacao.pos_conferencia` que o `b3_recibo`, o religamento e o fechar leem existem no retorno de
  `conferir_repinagem` (esboço l.1294-1295, 2530).
- **Evento F0.6:** as chaves dos dados estão no conjunto fechado do esboço (`versao, acao, bancada, um_py, selo,
  unidade`). O `iald.py anotar` real grava `dados + {unidade}` e imprime o hash com 16 hex (`PROGRAMA_IALD\iald.py:332-341`),
  que é exatamente o que `evento_c1_b3_v413.py:39-43` exige; a unidade F0.6 existe em `PROGRAMA.json` [REAL].
- **Autorização [REAL, contra o quadro real e só por leitura]:**
  - `livro_conferido` aceita o livro inteiro: 1710 elos, CRLF, nenhum separador que o `str.splitlines` corte fora do CRLF;
  - o 1687 nomeia `BENCH_AND_QUEUE_OPERATOR_APPROVAL.json`, e o sha256 dele confere;
  - o 1689 é da claude-c1, em resposta ao 1687; a fala dele confere pelo sha16, e a decisão «Salto na v413» está na fala;
  - a fala de 20/11 tem sha16 `29c5cffc50a2f8bf` e 106 caracteres numa linha.
  O texto da autorização teria cerca de 550 caracteres, longe do limite de uma variável de ambiente.

## 3. As 15 pendências e N1–N9

Cada uma foi feita como o plano propôs. As exceções: N3 está parcial (o que falta está em M4). N7 é ato da gerência e já
está no `CONTRATO_v413_R1.md`, §7, l.141-142. As guardas estáticas do 1.4(c) são da Etapa 2. As âncoras de linha do
PRONTO conferem com os arquivos (conferidas uma a uma).

| item | estado conferido |
|---|---|
| 1.1, 1.2, 1.3, 1.5, C.2 | feitos. Ressalvas no 1.2: o rc do p00 não entra no veredito do runner (B1, herdado da v412) e a guarda de restos tem uma falha (B2) |
| 1.4 | o PINOS_BN pina o delta principal, o `delta_bn` e o `util` (`diff_e_pinos_bn_v413.py:107-123`); o `b3_prepara` confere os três (`bn_v413.sh:39-46`); vb24 vem do delta |
| 2.1–2.7 | feitos como propostos (seção 2). No 2.7, o PINOS_BN final é exigido já no passo 10, e não só no 10b: mais estrito, coerente |
| 2.8 | M7, M8, M9, M10a/b/c e M11, cada um pego pela condição certa; o controle sem mutação passa (48/48) [REAL, no resultado] |
| C.1 | feito, com 9 controles |
| N1, N2, N4, N5, N6, N8, N9 | feitos |

**Algum conserto quebrou outra coisa?**

1. **N8/1.4(c)** — unificar o sandbox em `DBN.SANDBOX_CURTO` desfez uma separação que existia na v412 sem querer (as
   guardas usavam vb22 e o pré-selo vb23). Agora o pré-selo, as guardas estáticas da Etapa 2 (o `delta_v413.py:50` faz
   `SANDBOX_CURTO = DBN.SANDBOX_CURTO`) e o `mutar_conferidor` usam todos `C:\t\vb24`. Ver M1.
2. **2.2** — o livro passou a ser conferido inteiro. É mais estrito, e o livro real passa [REAL].
3. **N5** — o conserto vale para a v413, mas empurra o problema para a v414, com uma indireção a mais (B12).
4. **Uma condição nova do conferidor de exigências** dá falso negativo depois do passo 10 (B3).

## 4. Testes herméticos (76) e mutações (13): código real ou substituto?

**Real:** cópias byte a byte dos scripts do B(n), num mundo falso, com o `delta_bn` reapontado (`mundo_falso_bn_v413.py:196-208`).
Também reais:
- o esboço R3.6, o gerador da cadeia e o da bateria;
- o `canonical.py` da Bancada, copiado;
- o `pythonw` real lançando um servidor falso (o B5 provou o log e o `CUDA_VISIBLE_DEVICES=-1`);
- a conferência A contra a porta real fechada;
- o `delta_bn` lendo a produção;
- o conferidor real sobre cópias mutadas.

**Substituto** (`ensaio_hermetico_bn_v413.py`):
- **(a) Bateria e T12 forjados.** O esboço rodou só com `--sandbox --sem-bateria` (l.117-118). O `bateria_resultado` foi
  trocado por um PASSA de mentira (l.124-125), e o recibo do T12 foi forjado (l.129).
- **(b) Saída do ensaio forjada.** O `etapa1_stdout.txt` foi escrito à mão (l.130). Por isso o
  `rodar_ensaio_1_pre_selo_v413.sh` nunca rodou, e o corpo do `rodar_bn_pre_selo_v413.sh` só rodou até o portão N1 (E6).
- **(c) Recibos do pós-selo sintetizados.** Os recibos de ENSAIO e APLICAR que o B1, o B2, o B3 e o B6 conferem saíram de
  `recibo_pos` (l.234-245), não do esboço.
- **(d) `iald.py` falso.** Ele grava `unidade` também no topo do elo (`mundo_falso_bn_v413.py:93`); o real grava só dentro
  de `dados`. O teste passa nos dois casos.
- **(e) `bn_v413.sh` só nos portões.** Ele rodou só até o primeiro portão de cada passo (E1–E5).
- **(f) Mutações estáticas.** As 13 mutações testam o conferidor, que é estático (AST e texto), e não o comportamento dos
  recibos. O comportamento ficou com os negativos dinâmicos de parada e religamento.

**Caminhos reais sem teste.** Eles são a primeira execução na rodada real, e eu os conferi só pela leitura e pelas
medições da seção 6:
1. a bateria da v412 pelo esboço (T01–T16);
2. o runner do pré-selo inteiro;
3. o esboço no pós-selo (ENSAIO e APLICAR com salto, `--kernel-recibo` e `--criterios`);
4. o `b3_prepara` depois do portão dos pinos: a geração da bateria da v413 com `--pinos-bn PINOS_BN_v413.json`, o
   `gravar_pino_bateria_v413.py` e a árvore do kernel;
5. o `diff_e_pinos_bn_v413.py --delta` (o diff do embutido e o `diff -u`);
6. o `iald.py anotar` real, que também grava `PROGRAMA.json`;
7. o modo `pelo_pid` da parada.

## 5. O que pode falhar na rodada real e não falhou no hermético

| risco | estado | efeito |
|---|---|---|
| tempo | o pré-selo da v411 levou 2 min 10 s (`v411\bateria_pre_selo\bn_pre_selo_out_v411.txt`: 22:33:47 → 22:35:57); o da v413 roda a bateria inteira e fotografa um Nós de cerca de 161 mil entradas (a foto segue a junção de `packages`) | passa do limite padrão de 120 s da ferramenta Bash; idem os passos 10 e 10b (M2) |
| escrita alheia no Nós ou no kernel irmão durante as fotos | o Nós não muda desde 19/11 11:14 [REAL]; há 1 junção: `Nós\tgl_kernel\.lake\packages → A Ponte e o Um\tgl_kernel\.lake\packages` [REAL]; as Etapas constroem em `C:\t\k404c\final\.lake\packages`, outro alvo [REAL] | prova «produção alterada», do lado seguro. Congelar a linhagem, o desenho, a memória e qualquer servidor Lean nesses dois kernels durante o pré-selo |
| sandbox compartilhado | M1 | recusa no início ou falha no passo 7 |
| bateria da v412 | nunca rodou nesta versão | BATERIA_FALHOU (rc 3), nada gravado; refazer exige tirar as saídas e o vb24 (B2) |
| serviço morrer com a sessão que o lançou | [OPEN]: `Popen` com DETACHED_PROCESS e CREATE_NEW_PROCESS_GROUP, sem breakaway de Job (B9) | o portão C do 11 pega depois |
| meia-noite | a conferência A e o portão C usam a data local | rodar outra conferência A |
| porta 18777 | hoje fora das faixas excluídas do Windows [REAL] (as faixas mudam a cada boot) | religamento recusa, e agora com o erro no log (N9) |
| livro em escrita alheia | linha final parcial = EVENTOS_JSONL_ILEGIVEL | transitório; repetir (cuidado com B6) |
| Git Bash, fim de linha, PID | [REAL] Medido: o caminho com acento ida e volta pelo `sh`; `diff`, `cygpath` e `powershell` no PATH; TZ −03:00 coerente entre `time.strftime` e `datetime`; nenhuma variável de proxy nem `PYTHON*` no ambiente; scripts em LF, livro em CRLF (tratado), stdout do rito com `RITO_RC=` | sem risco medido |

---

## 6. Achados

### MÉDIO

**M1 — O sandbox `C:\t\vb24` é compartilhado com trabalho que corre ao mesmo tempo (efeito do conserto N8/1.4c).**

Quem o usa:
- `delta_bn_v413.py:45`;
- `delta_v413.py:50`, da Etapa 2, que está em curso;
- `controle_negativo\mutar_conferidor_v413.py:41`, cujo padrão é `DBN.SANDBOX_CURTO`;
- as guardas estáticas que a Etapa 2 vai derivar. O molde dela, `v412\guardas_estaticas_bancada_v412_r7.py`, cria
  `SANDBOX_CURTO\gate` e apaga o sandbox se o criou.

Os efeitos:
- o pré-selo recusa se a pasta existe (`rodar_bn_pre_selo_v413.sh:42`);
- o `limpar_sandbox_vb24.py:48` apaga a pasta inteira;
- uma guarda ou mutação em curso faz o pré-selo recusar no início, ou falhar no passo 7. Pior: a limpeza pode apagar a
  pasta de trabalho da guarda.

Conserto:
- **(a)**, regra para hoje: rodar o pré-selo com a Etapa 2 parada (nenhuma guarda estática nem `mutar_conferidor` em
  curso) e conferir, imediatamente antes, que `C:\t\vb24` não existe.
- **(b)**, se a gerência preferir código: em `delta_bn_v413.py`, depois da l.45, acrescentar
  `SANDBOX_GUARDAS = os.path.join(C, "t", "vb25")   # guardas estaticas e controle negativo; nunca o do pre-selo (o limpar apaga vb24 inteiro)`.
  Em `mutar_conferidor_v413.py:41`, trocar por
  `TEMP_DIR = os.environ.get("V413_MUTAR_TEMP") or DBN.SANDBOX_GUARDAS`.
  Pedir à Etapa 2 que as guardas usem `DBN.SANDBOX_GUARDAS`; o `e7_01_conferir_delta_v413.py` também cita o sandbox e tem
  de acompanhar. Conferir antes que `vb25` não existe.

**M2 — O pré-selo e os passos 10 e 10b passam do limite padrão (120 s) da ferramenta Bash.** Se a ferramenta matar a
árvore no meio:
- ficam `.tmp` e o vb24;
- o p00 acusa `.tmp` (D135), mas o p00 não decide o veredito (B1);
- refazer exige limpeza manual, contra o prazo N1.

Conserto: rodar `sh ./rodar_bn_pre_selo_v413.sh > <OUTB>\bn_pre_selo_out_v413.txt 2>&1` e os passos 10 e 10b com
`run_in_background` (ou timeout de 600000 ms), e ler o veredito no arquivo. Pôr essa linha no item «falta_para_rodar» do
PRONTO e no cabeçalho de uso do runner (`rodar_bn_pre_selo_v413.sh:9`).

**M3 — Os caminhos centrais da rodada real nunca rodaram (seção 4).** São a bateria da v412, o runner do pré-selo inteiro,
o esboço no pós-selo e no APLICAR com o salto, e o `b3_prepara` depois dos pinos. Conferi por leitura o formato que o
`b3_recibo`, o religamento e o fechar esperam do esboço, e por medição a montagem dos argumentos do ensaio. Mesmo assim, um
defeito ali só aparece na hora; no pós-selo, depois do selo.

Conserto:
- **(i)** rodar o pré-selo com margem antes da instalação da v413. A bateria da v412 só se prova ali; um negativo é parede
  medida, sem gravação, e se refaz enquanto o Nós estiver na v412.
- **(ii)** antes do selo, um ensaio a seco do pós-selo no mundo falso do hermético:
  1. instalar a v413 falsa no Nós falso;
  2. rodar o esboço real com `--sandbox --sem-bateria --fase pos_selo --modo ensaio`, passando o recibo pré-selo do A3b
     (com o sha dele), a cadeia, e `--selo-anterior`/`--kernel-manifesto-anterior` da `base_v412` falsa;
  3. passar o stdout no `b3_recibo_v413.py <stdout> ensaio <cadeia>`.
  Assim o salto no pós-selo, o `regenerar` com salto e o formato do recibo ficam provados; só o bloco da bateria segue
  sintético.

**M4 — A custódia dos insumos do salto cobre menos do que o salto lê.** O `CONTRATO_v413_R1.md` (§7, l.147-148) protege só
os `.bak_20261118_235146` do Nós e o registro do instalador. A cadeia pina, por caminho absoluto e sha, também:
- `v413\base_v412\{um.py, um_absoluto_selo.json, tgl_kernel_proof_manifest.json}`;
- os mesmos três em `v412\base_v411\`.

O pós-selo lê ainda:
- `v413\cadeia_de_selos_v411_v412\` (a cadeia e o pino);
- o recibo pré-selo em `v413\bateria_pre_selo\ensaio_1\`;
- a árvore `C:/t/k413c/arvore` do `KERNEL_RECIBO_v413` (`bn_v413.sh:56-57`; não há `refazer_arvore_v413` no molde, como
  houve na v412).

Depois da instalação da v413, perder qualquer um desses mata o salto ou deixa o passo 10 em AGUARDA. O
`copiar_base_v413.py` não sobrescreve bytes diferentes (l.32-33), mas o LAR e a limpeza de `C:\t` não estão cobertos.

Conserto: acrescentar ao §7 do contrato, ou ao pedido ao LAR, a frase «e, até o fechamento do B21, também
`v413\base_v412\`, `v412\base_v411\`, `v413\cadeia_de_selos_v411_v412\`, `v413\bateria_v412_pre_selo\`,
`v413\bateria_pre_selo\` e `C:\t\k413c\arvore`». No p00, seção (6), conferir `os.path.isdir(KR["arvore"])` quando o pino
`kernel_recibo` existir.

### BAIXO

**B1** — `rodar_bn_pre_selo_v413.sh:65` não lê `RC_P00` (herdado da v412). Uma FALHA do p00 (rc 1) passa calada. Trocar a
linha por:
`if [ "$RC_CONFERENCIA" != 0 ] || [ "$RC_PINO" != 0 ] || [ "$RC_LIMPAR" != 0 ] || [ "$RC_DIFF_PINOS" != 0 ] || { [ "$RC_P00" != 0 ] && [ "$RC_P00" != 3 ]; } || [ "$UTIL" != True ]; then echo "FALHOU: conferencia=$RC_CONFERENCIA pino=$RC_PINO limpar=$RC_LIMPAR diff_e_pinos=$RC_DIFF_PINOS p00=$RC_P00 utilizavel=$UTIL"; exit 1; fi`

**B2** — A guarda de restos (`rodar_bn_pre_selo_v413.sh:44`) não cobre `LIMPEZA_SANDBOX_vb24.json` nem `prova_producao`.
Numa falha antes do passo 7 (l.51, l.53) o vb24 fica. Se ele for limpo pelo `limpar_sandbox_vb24.py`, nasce o LIMPEZA que
faz o passo 7 da rodada seguinte falhar no fim (`limpar_sandbox_vb24.py:24-26`), com o pino já utilizável. Trocar a l.44 por:
`for f in "$OUTB/etapa1_stdout.txt" "$OUTB/ensaio_1" "$OUTB/conferencia_pelo_esboco_v413.json" "$OUTB/prova_producao" "$OUTB/LIMPEZA_SANDBOX_$(basename "$SB").json" "$(cygpath -u "$(UV const PINO_RECIBO_PRE_SELO_ARQ)")" "$(cygpath -u "$(UV const PROVA_PRODUCAO_ARQ)")"; do`
(`SB` já está definido na l.40).

**B3** — `conferir_exigencias_servico_v413.py:234`: o glob `bancada_B3*` casa a pasta do ENSAIO pós-selo
(`bancada_B3_ensaio_<stamp>`, `bn_v413.sh:84`). Depois do passo 10, a condição «o recibo do APLICAR ainda não existe»
falha, e com ela o controle sem mutação do `mutar_conferidor`. Trocar por:
`bn13 = sorted(glob.glob(os.path.join(DBN.V413, "bancada_B3", "RECIBO_SINCRONIZACAO_%s_*.json" % DBN.UM_VERSION_BN)) + glob.glob(os.path.join(DBN.V413, "bancada_B3_[0-9]*", "RECIBO_SINCRONIZACAO_%s_*.json" % DBN.UM_VERSION_BN)))`

**B4** — Falta o evento de aviso F0.6 que aponta os três recibos (plano §4, item 4), de que o Codex precisa para encerrar
a unidade dele. Nem o passo 11 nem o `fechar_bn_v413.py` o lembram. Acrescentar ao fim do passo 11 do `bn_v413.sh`:
`echo "FALTA (ato da gerencia): o aviso F0.6 no quadro apontando o pino conjunto (caminho e sha256) para o Codex encerrar a unidade"`
Ou fazer um `aviso_f06_v413.py` que anote por `iald.py anotar --quem claude-c1 --unidade F0.6`.

**B5** — Os recibos exigem no `V413_AUTORIZACAO_OPERADOR`:
- os hash16 dos eventos e os sha16;
- a resposta, a decisão e as falas inteiras.
(`recibo_parada_v413.py:45-46`; `recibo_religamento_v413.py:48-49, 65`.) O molde não traz o script que monta esse texto
dos arquivos; só o hermético tem um (`MF.aut`). Pela régua, hash só lido por script. Conserto: um
`montar_autorizacao_v413.py [<fala do modo> <cpu|normal>]` que grave `bancada_B3_servico\AUTORIZACAO_v413.txt` e o sha dele;
a gerência passa o texto por `$(cat …)`.

**B6** — `evento_c1_b3_v413.py:35-45`: não há guarda contra repetição. Se o `iald.py` anotou e o script caiu depois (por
exemplo, a releitura do livro durante uma escrita alheia), rodar de novo anota um segundo evento. Conserto: antes de
anotar, procurar no livro conferido um elo da claude-c1, do tipo SINCRONIZACAO_BANCADA, com `dados == dados` e `quando`
posterior ao fim do ensaio; se houver, imprimir `EVENTO=` dele e sair com rc 0 sem anotar.

**B7** — `recibo_religamento_v413.py:92`: o servidor (que não roda isolado) herda o ambiente inteiro. Hoje nenhuma variável
`PYTHON*` está definida [REAL]. Acrescentar depois da l.92:
`for v_ in ("PYTHONPATH", "PYTHONHOME", "PYTHONSTARTUP", "PYTHONUSERBASE", "PYTHONPLATLIBDIR", "PYTHONEXECUTABLE", "PYTHONINSPECT", "PYTHONOPTIMIZE"): AMB.pop(v_, None)`
E gravar a lista das retiradas em `ambiente_do_processo`.

**B8** — `recibo_religamento_v413.py:114-115`: o `U.processo()` levanta RuntimeError se a leitura do PowerShell for
ilegível. Isso acontece depois do lançamento: sai um traceback sem RECUSA gravada e sem o PID em disco. Envolver as duas
linhas num `try/except Exception as e_: PROB.append("leitura do processo falhou: %r" % (e_,)); PROC_INFO = None`.

**B9** — [OPEN] Não se sabe se o servidor sobrevive ao fim da sessão que o lança (Job com *kill-on-close*). O diagnóstico,
na seção 1.2, não exclui que o de 13/11 tenha caído assim. Conserto: tentar
`creationflags=... | subprocess.CREATE_BREAKAWAY_FROM_JOB`; se o `Popen` levantar OSError, repetir sem e registrar
`breakaway: true|false` no recibo. O PID vivo segue conferido no passo 11.

**B10** — O portão C (`util_bn_v413.py:244-252`) aceita qualquer `SAUDE_BANCADA_<hoje>_*` e qualquer veredito, inclusive
INDETERMINADO, sem ler `contrato` nem a Bancada. Exigir `contrato == "SAUDE_BANCADA"`,
`os.path.normcase(bancada) == os.path.normcase(DBN.PRODUCAO)` e `veredito != "INDETERMINADO"`.

**B11** — O 10b só confere que o recibo da parada existe (`bn_v413.sh:106`). Acrescentar a conferência de `modo` (`pelo_pid`
ou `ja_fora_do_ar`) e de `autorizacao_conferida.evento_decisao.seq == 1689`, pelo `UV json`.

**B12** — O N5 volta na v414, com uma indireção a mais. O `delta_v413.py:17-20` carrega o `delta_bn_v413.py` por caminho,
e o `_bancada_pina_hoje()` dele só admite B20-v411 e B21-v413 (`delta_bn_v413.py:112`). Depois do B22, importar o
`delta_v413` quebra. Registrar no plano da v414: fixar também a carga do `delta_bn` dentro do `delta_v413`, não só a linha
do `BANCADA_PINA_HOJE`.

**B13** — `limpar_sandbox_vb24.py:29, 49-53`: a conferência dos irmãos de `C:\t` falha se outro agente criar arquivo
direto em `C:\t` durante o `rmtree` (as Etapas gravam logs ali). O efeito é RC_LIMPAR ≠ 0 com o pino já utilizável. Basta
saber que é benigno; ou comparar só as pastas `vb*`.

---

## 7. A partitura (para a gerência ler ao autor antes do pré-selo; complementa o 5.4 do plano)

«O pré-selo confere identidade, não física. Ele decide se a Bancada pode, depois do selo, saltar da v411 para a v413. Não
decide nada sobre a teoria, o selo ou o gate. Se der negativo, o primeiro suspeito é a bateria da v412, que roda ali pela
primeira vez. É parede medida: nada é gravado na Bancada, e ele pode ser refeito enquanto o Nós estiver na v412.»

## 8. O que não verifiquei

- a bateria da v412 rodando;
- o esboço no pós-selo;
- se um Job mata o servidor lançado;
- o comportamento das guardas estáticas da Etapa 2, que ainda não existem;
- o `gerar_pronto_bn_v413.py` linha a linha (conferi o PRONTO contra o disco);
- uma nova rodada do ensaio hermético.

## Anexo para o Mapa de Rotas (a gerência registra)

- **Consultado antes:** `rotas.py consultar "salto v413"` (0 rotas) e `consultar "bn_v413"` (1 rota:
  `bancada.bn_v413.salto_v411_v413_20nov`, EM_CURSO).
- **Examinado** (`olhou_dados: false`):
  - os 26 scripts e o esboço, nos trechos do salto, do recibo pré-selo, do evento, do APLICAR e da saída;
  - o quadro real conferido inteiro, só por leitura;
  - a montagem dos argumentos do ensaio, com eco;
  - o caminho com acento ida e volta pelo `sh`;
  - as junções e as escritas recentes no Nós e na Bancada;
  - as faixas de porta excluídas e o ambiente.
- **Veredito:** `MOLDE_BN_v413__APROVADO_COM_RESSALVAS__0_ALTO_4_MEDIO_13_BAIXO__PRE_SELO_PODE_RODAR_APOS_M1_M2`.
- **Não refazer:** a conferência do formato do recibo do esboço contra o `b3_recibo`, o religamento e o fechar; a leitura
  do quadro real.
- **Scripts desta revisão** (só leitura, no scratchpad da sessão): `r01_conferir_sha_pronto.py`,
  `r02_ler_bateria_e_cadeia.py`, `r03_ambiente.py`, `r04_quadro_real_so_leitura.py`, `r05_nos_recentes_so_leitura.py`,
  `r06_eco.py`, `r06_ida_e_volta.sh`, `r07_preparar_copia_ensaio1.py` (gera `r07_ensaio1_eco.sh`), `r08_ler_resultados.py`,
  `r09_juncoes_so_leitura.py`, `r10_juncao_k413c.py`.
