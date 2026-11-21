# Diagnóstico da Bancada Um e plano do B(n) da v413 (20/11/2026)

Agente de diagnóstico a serviço da gerência c1. Pedido do operador, por bytes:
`work\cunhagens_13out\OPERADOR_20nov_colei_no_codex_prossiga_concordo_com_tudo_veja_a_questao_da_bancada_verbatim.txt`
(sha16 `29c5cffc50a2f8bf`): «veja a questão da bancada para que não tenhamos problema mais».

**Escopo.** Só leitura. Nenhum serviço foi ligado ou parado, não houve POST nem GET na Bancada (a porta está fechada), e nada
foi escrito fora desta pasta. A placa de vídeo e o treino em `C:\IALD\TGL_IALD_NATIVE_QWEN5090` não foram medidos nem
tocados: o que digo sobre a placa vem da leitura do código. Não inscrevi referência na memória ACOM, porque o `init` grava
fora desta pasta; a referência da missão fica com a gerência.

**Evidência lida por script, nesta pasta** (hash sempre lido do arquivo, nunca de memória):

| script | saída | o que mede |
|---|---|---|
| `ler_eventos_bancada.py` (sha16 `1dde3f4c58684fd0`) | `saida_ler_eventos_bancada.txt` (`eac684b5c94179ee`) | eventos 1617, 1686, 1687, 1689 e cadeia de hash do quadro (1709 elos, nenhuma quebra; `eventos.jsonl` sha16 `d79cc3c1ec600c76` na leitura) |
| `medir_evidencias_bancada_v413.py` (`7d6d3c7d00c91c62`) | `saida_medir_evidencias_bancada_v413.txt` (`a054982f998a7504`) | sha16 de 45 artefatos, o estado da Bancada e do Nós, as cópias de bytes, a seleção da cadeia de selos refeita sem gravar, os recibos |
| `ler_sistema_bancada.py` (`0c4b9a02f33c2dda`) | `saida_ler_sistema_bancada.txt` (`90e5ee3baa457d07`) | último boot, eventos de reinício, falhas de python, processos, porta 18777, início automático |

Estatutos: [REAL] = lido ou medido agora; [DERIVADO] = conclusão da leitura do código, sem executar; [DECLARADO] = dito na
memória ou num recibo, sem remedir; [OPEN] = não se sabe.

---

## Resumo

1. **Por que está desligada** [REAL]: o último início registrado foi o religamento do B20, em 13/11 às 03:55:53, PID 23688.
   A máquina reiniciou em 16/11 entre 13:48 e 13:57: primeiro um reinício pedido pelo usuário, depois um do Windows Update.
   Não existe início automático da Bancada (nenhuma tarefa agendada, nenhuma entrada na pasta Inicializar ou na chave Run).
   Ninguém a religou. Os religamentos feitos desde 04/11 não deixaram log, por isso não há como dizer se ele caiu antes de
   16/11 [OPEN].
2. **Ligar agora não a devolve ao uso** [DERIVADO]. Desde a instalação da v412 no Nós (18/11 às 23:51), o contrato dela pina
   o `um.py` v411 no caminho do Nós, e o `canonical.py` recusa com PIN_CHANGED. Ela subiria em modo degradado, recusando toda
   conta científica com 409, até o B(n) da v413 regravar o manifesto.
3. **A placa** [DERIVADO]: no modo normal, a Bancada usa a placa ao subir (cria o contexto CUDA e põe o motor na GPU) e
   carrega o lago na RAM, até 60% da RAM livre (~24 GiB [DECLARADO]). No modo degradado, cada leitura de `/api/estado` cria o
   contexto CUDA. O B(n) em si (o esboço e a bateria) não usa a placa.
4. **O salto** exige uma cadeia de selos v411→v412 conferida por hash e um **pré-selo rodado com o Nós ainda na v412, antes da
   instalação da v413**. O recibo do salto só serve à versão seguinte. Medi que a cadeia é viável hoje: as cópias de bytes,
   o registro do instalador e os backups existem e conferem.
5. **Pendências:** são 15 itens na lista. 5 já estão feitos no molde e 10 seguem abertos. Proponho conserto para os 10
   (arquivo, linha e mudança na seção 3). Achei mais 9 pontos que a lista não tem.
6. **O que o Codex espera:** o evento c1 `SINCRONIZACAO_BANCADA` (F0.6) da v413, os três recibos com revisão distinta,
   devolvidos na pasta `bench`, e a Bancada servindo a v413 no `/api/contratos`.

---

## 1. Por que está desligada, como sobe, placa e RAM

### 1.1 Linha do tempo [REAL, salvo quando marcado]

| quando | o quê | fonte |
|---|---|---|
| 04/11 07:32:44 | última escrita do `servidor.log` (13 linhas «Bancada Um no ar») e, às 07:32:50, do `servidor_erros.log` (9 tracebacks `ConnectionAbortedError` de cliente que fechou a conexão; nenhum erro de subida) | `estado\servidor.log` `8d56ce61f1bd814c`; `estado\servidor_erros.log` `c5ccac6f465f8d04` |
| 05/11, 06/11, 11/11, 13/11 | religamentos dos B17 a B20, que não escreveram no `servidor.log` (o recibo do religamento da v411 guarda só o comando, sem redirecionamento) | recibos `RECIBO_SINCRONIZACAO_v408..v411` em `estado\sincronizacao`; mtime do log |
| 13/11 03:53:48 | parada do PID 68292 (no ar desde 11/11 02:24:18) para o B20 | `v411\bancada_B3_servico\RECIBO_PARADA_v411.json` `0a08cb1dd411f0f6` |
| 13/11 03:53:53 | evento c1 1617 `SINCRONIZACAO_BANCADA` v411 (hash16 `8b7301134714332b`) | `eventos.jsonl` l.1617 |
| 13/11 03:53:59–03:55:52 | APLICAR do B20: `REPINADA_B20__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO` | `Bancada_Um\estado\sincronizacao\RECIBO_SINCRONIZACAO_v411_20261113_035359.json` `50989b5e353fa7ab` |
| 13/11 03:55:53 | **último início**: PID 23688, `"C:\Python314\pythonw.exe" -X utf8 C:\IALD\Bancada_Um\um_bancada.py`; `pronta: false` às 03:56:08 | `v411\bancada_B3_servico\RECIBO_RELIGAMENTO_v411.json` `c97da059f477d3cc` |
| 13/11 03:55:52 | o arquivo mais novo da pasta da Bancada, fora `__pycache__` | saída de `medir_evidencias`, seção (5) |
| 16/11 13:09 | falha de um `python.exe` **3.12** (outro interpretador; a Bancada roda no `pythonw` do Python 3.14) | Application 1000/1001, `saida_ler_sistema_bancada.txt` |
| 16/11 13:48:56 | reinício pedido pelo usuário IALD\rotol pelo menu Iniciar (Id 1074, «Outro (não planejado)») | System 1074 |
| 16/11 13:52:48 | reinício do Windows Update (TrustedInstaller, «atualização (planejada)»); desligamento por winlogon às 13:54:12 | System 1074/6006 |
| 16/11 13:57:46 | boot atual | `LastBootUpTime` |
| 16/11 13:59:54–17:18:26 | 5 adaptadores `mcp_um.py` renascem com as sessões; nenhum `um_bancada.py` | `saida_ler_sistema_bancada.txt` |
| 18/11 23:51:46 | v412 instalada no Nós (backups `*.bak_20261118_235146`): daqui em diante o contrato da Bancada fica velho (PIN_CHANGED) | `v412\APLICADO_AO_CANONICO_20261118_235146.json` `0baf3bc1aeffd20a` |
| 19/11 00:46:31 | selo da v412 | `v412\bateria_pre_selo\MOMENTO_DO_PRE_SELO.json` l.14 |
| 19/11 11:01:46 e 14:01:32 | o Codex encontra a porta recusando conexão e zero processos | `iald_v412_20261119\bench\VERIFICACAO_BANCADA_R1.json` `d4c7ec39b1e41a02`; `C1_RETURN_VERIFIED.json` `380d94e5dd12c48a` |
| 20/11 20:26 | segue desligada: nenhuma escuta na 18777, nenhum `um_bancada.py`, nenhum início automático | `saida_ler_sistema_bancada.txt` |

### 1.2 O motivo

- [REAL] A Bancada não tem início automático: não há tarefa agendada, entrada na pasta Inicializar ou chave Run que a cite.
  O processo de 13/11 não sobreviveu ao reinício de 16/11, e o rito só a religa no passo 10-ter do B(n) seguinte, que na
  v412 não houve.
- [REAL] Ninguém percebeu por três dias (16/11 → 19/11), porque nenhuma etapa da casa confere a Bancada fora do B(n).
- [OPEN] Não há log de 13/11 a 16/11. O `pythonw` foi lançado sem redirecionar stdout e stderr (o `servidor.log` parou em
  04/11), então não se pode excluir uma queda anterior. O log de aplicações não tem falha do `pythonw` 3.14 entre 13/11 03:50
  e 16/11 14:00.
- [DERIVADO] Mesmo no ar, ela estaria cientificamente inutilizável desde 18/11 23:51 (seção 1.5).

### 1.3 Como sobe

- **Comando do rito**: `"C:\Python314\pythonw.exe" -X utf8 C:\IALD\Bancada_Um\um_bancada.py` (`RECIBO_PARADA_v411.json`,
  campo `religar`; `RECIBO_RELIGAMENTO_v411.json`, campo `comando`). É um processo `pythonw`, sem console.
- **Atalho do operador**: `abrir_bancada.pyw` l.31-47 (`83349b1423e8bcf0`). Lança o `pythonw` destacado
  (`DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP`), com stdout e stderr em `estado\servidor.log` e
  `estado\servidor_erros.log` (l.35-39), e espera até 90 s. A ferramenta `ferramentas\reiniciar_servidor.py` l.26-63
  (`1960ead8c3cf06c4`) encerra pelo PID achado na linha de comando, sobe destacado com os mesmos logs e espera `pronta` até 120 s.
- **Sequência de subida** (`um_bancada.py`, `1e5eef094f8a6019`):
  1. `main` (l.433-436) constrói `Bancada()` e abre a porta 127.0.0.1:18777.
  2. `__init__` chama `require_current("server_startup")` (l.40-44). Se o contrato não está em dia, grava `erro` e retorna
     cedo, sem lago, sem banco GW e sem motor.
  3. Com o contrato em dia, cria `Lago` e `GWResidente` e dispara três threads (l.45-51).
  4. `_carrega` (l.53-65) cria `Motor`, `Livro` e `Evidencia`, confere o contrato de novo, marca `pronta = True` e dispara o
     lago inteiro na RAM, «e fica» (l.63).
- **Tempo**: «motor pronto ~1 s; lago residente 23,68 GiB em 34 s (481 arquivos)» [DECLARADO: memória `bancada-um.md` l.15,
  medição de 28/09]. Em 13/11 o recibo do religamento registrou `pronta: false` 15 s depois da subida [REAL].
- **RAM do lago**: o orçamento é 60% da RAM livre. O que não cabe fica listado como `nao_carregado` (`bancada\lago.py` l.9,
  l.118-120, l.243-258, `dff321cbe1da102b`). As quatro raízes do lago estão em `um_bancada.py` l.24-25. Cerca de 24 GiB
  [DECLARADO, `bancada-um.md` l.3 e l.15].

### 1.4 A placa de vídeo ao subir [DERIVADO, nada medido]

- **Modo normal (contrato em dia): sim, na subida.** A thread `_carrega` cria o `Motor`, que escolhe `cuda` se houver
  (`bancada\motor.py` l.131-133, `dc8bdc0da972a4b5`). Na construção, o motor põe na GPU a tabela CAMB
  (`camb_tabela.py` l.19, l.29-34), as grades do fundo (`fundo_gpu.py` l.63-83) e as Cholesky e covariâncias, inclusive dois
  `PantheonCov` (`motor.py` l.158, l.165-189). Isso cria um contexto CUDA e aloca tensores pequenos (a tabela CAMB tem 224 KB
  em disco, a covariância Pantheon 23 MB). O tamanho do contexto não foi medido.
- **Sob demanda**: as colunas do lago vão para a VRAM com cache LRU até min(8 GiB; 40% da VRAM livre) e **ficam lá**
  (`lago.py` l.310-333). Os lotes do MCMC usam até 50% da VRAM livre (`motor.py` l.192-198). O próprio código avisa que
  «a GPU é compartilhada com o llama-server» (l.193).
- **Modo degradado (o de hoje)**: o motor não sobe. Mas `/api/estado` importa `torch` e chama `torch.cuda.is_available()` e
  `torch.cuda.mem_get_info()` (`um_bancada.py` l.91, l.105-108): a primeira leitura de estado cria o contexto CUDA no processo
  do servidor. Chamam `/api/estado` o `um_bancada.py --check` (l.424-431) e o recibo do religamento
  (`recibo_religamento_v412.py` l.79). `/api/contratos` não toca a placa: só lê o contrato (l.264-265).
- **O B(n) não usa a placa.** O esboço só lê arquivos e o `canonical.py`. Os testes da bateria que usam `torch` forçam CPU
  (`F0.3.B2\tests_motor\test_motor_synthetic.py` l.17, l.21, l.66, l.145; `bateria\t10_t11_canais.py` l.54;
  `neff_canal.controle_anti_dupla_contagem`, padrão `cpu` em l.205-206). T01, T09 e T15 só usam o `canonical`. Os runners do
  T12–T14 (`F1.ATRATOR`) e as fontes de T02, T07, T08 e T16 não citam `torch` nem `cuda` (grep). A bateria não foi executada.
- **Atenuação sem mudar código**: lançar o servidor com `CUDA_VISIBLE_DEVICES=-1`. No Windows, uma variável vazia é apagada,
  por isso o valor tem de ser `-1`. Assim `torch.cuda.is_available()` dá False e o motor roda em CPU (`motor.py` l.131-132).
  Não remove o custo de RAM do lago. Não medido.

### 1.5 Ligar agora adiantaria? Não [DERIVADO]

O manifesto pina o `um.py` pelo **caminho do Nós**. O `canonical_contracts.json` (`f2ed66a8a6ce96f4`) traz `B20-v411-20261113-R1`,
com `script.path` igual a `...\Nós\um.py` e sha16 `1203b1f9202020d6`, enquanto o Nós tem `3e741dcaa58ef2b8` (v412) [REAL].

O `CanonicalRegistry` confere o contrato ao ser construído (`bancada\canonical.py` l.24-47) e recusa com `PIN_CHANGED`
(l.53-60). Em consequência:

- o servidor sobe com `erro` (`um_bancada.py` l.40-44);
- só respondem `/`, `/ui/*`, `/api/estado`, `/api/atividades` e `/api/contratos` (l.256-265);
- todo outro GET passa por `require_current` (l.266-267) e devolve 409 `CANONICAL_REVALIDATION_REQUIRED` (l.321-322);
- todo POST também devolve 409 (l.357-360).

É o desenho: «uma versão nova do um.py invalida o contrato instalado: o canonical.py recusa toda operação científica
(PIN_CHANGED) até que o passo B(n) da cadeia regenere o manifesto» (`R3_6\sincronizar_bancada.py` l.1168-1169). Ligar antes
do B(n) também obriga a parar pelo PID antes do APLICAR (`guarda_servico`, l.2684-2692).

### 1.6 O que não verifiquei

O tempo e a memória reais da subida, o tamanho do contexto CUDA, se a bateria realmente não toca a placa ao rodar, o
comportamento dos adaptadores `mcp_um.py` quando o servidor voltar e se o processo de 13/11 viveu até 16/11.

---

## 2. O B(n) pelo R3.6 e o caminho do salto

Esboço: `bancada_vinculo_12out\R3_6\sincronizar_bancada.py` (sha16 `bf5ad5c99d05fa57`, o pinado em `PINOS_BN_v411.json`
como `esboco_R3_6`). A R3.6 é a R3.5 mais um contrato de recibo do kernel. Só `verificar_kernel_recibo` difere
(`R3_6\RESULTADO_R3_6.md` l.9, `a4de6e5fdac3aeec`).

### 2.1 Os passos e quem faz

| passo | o que faz | onde | quem |
|---|---|---|---|
| P1–P9 pré-selo | foto da produção; ensaio `--fase pre_selo --modo ensaio` (só lê a Bancada e o Nós, grava só em `--saida`); fotos depois e final; conferência do recibo pelo esboço; pino do recibo e prova de produção intacta; limpeza do sandbox curto; `diff_e_pinos` (o `PINOS_BN`); `p00` | `v412\bateria_pre_selo\rodar_bn_pre_selo_v412.sh` l.43-55 (`88e46f2eea0bdd5a`) | gerência ou construtor sob ordem dela; gerar o `PINOS_BN` é «ato da gerência» (`diff_e_pinos_v412.py` l.13) |
| 10 | ensaio pós-selo | `v412\pos_rito\bn_v412.sh` l.87-100 (`4020186d13166667`) | gerência |
| 10a | recibo da parada; se o serviço estava no ar, a parada é pelo PID, «nunca por nome», sob ordem do operador | bn l.101-112; `recibo_parada_v412.py` (`58a8d6b06bf3d940`) | o operador ou a gerência sob a ordem dele; recibo pela gerência |
| evento | `SINCRONIZACAO_BANCADA`, quem `claude-c1`, unidade F0.6, pelo `iald.py anotar` | `evento_c1_b3_v412.py` l.11-22 (`69652343ddad72cd`) | gerência |
| 10b | APLICAR: `B3_AUTORIZADO=sim`, `EVENTO`, `EVENTO_HASH`, serviço parado; backup de bytes, troca atômica, rollback | bn l.113-131 | gerência, com autorização do operador |
| 10c | religar o serviço e gravar o recibo do religamento; reconectar os MCP em cada sessão | bn l.132-137; `recibo_religamento_v412.py` (`01036552a690a9a1`) | o operador ou a gerência sob a ordem dele (na v411 foi a gerência); o MCP é do operador |
| 11 | fechar: confere juntos os três recibos; sem eles, rc 2 | molde: `v410\pos_rito\chain_pos_rito_v410.sh` l.308-311 (`5ece9c315369b920`) e `fechar_v410.py` l.89-127 (`29afc4537f7bafb6`); **ausente na v412** (bn l.12) | gerência |

**Os três recibos** (`fechar_v410.py` l.15, l.93-118):

- `RECIBO_SINCRONIZACAO_vNNN_<stamp>.json` do APLICAR (esboço l.2678; a cópia em `estado\sincronizacao` sai de l.2904-2928);
- `RECIBO_PARADA_vNNN.json`;
- `RECIBO_RELIGAMENTO_vNNN.json`.

**O evento**, conferido pelo esboço:

- conferido pela cadeia de hash do livro (l.693-707) e pelo `--evento-hash` (l.742-748);
- tipo `SINCRONIZACAO_BANCADA` e autor `claude-c1`, por convenção, não por autenticação (l.234-235, l.713-716);
- `dados` só com as chaves fechadas `versao, bancada, acao, um_py, selo, reparo, gravacoes, unidade, nota` (l.250, l.723-725);
- `versao` igual à versão alvo e `acao` igual a `sincronizacao` (l.726-729);
- `um_py` e `selo` como prefixos (16 hex ou mais) dos sha do Nós (l.732-736).

### 2.2 O caminho do salto (`--cadeia-de-selos`)

**O que exige, no pré-selo:**

- **A Bancada atrasada**: a versão dela é diferente de `--versao` e ela não está sincronizada (l.2820). Se estiver à frente
  do Nós, recusa (l.2822-2823).
- **`--cadeia-de-selos` e `--cadeia-de-selos-sha256`**: sem eles, `BANCADA_ATRASADA_SEM_CADEIA_DE_SELOS` (l.2824-2826). O
  arquivo é pinado por sha (l.957-964), tem chaves fechadas (l.971-972) e o contrato `CADEIA_DE_SELOS_R3_4` (l.973-974).
- **De 2 a 64 elos**, de versões consecutivas (l.976-981).
- **Cada elo** traz cópias de bytes pinadas (caminho absoluto, sha e bytes; nunca link) do `um.py`, do selo e do manifesto do
  kernel. O selo pina os dois, e `UM_VERSION` e `ALPHA` são linhas únicas (l.864-915).
- **Cada elo menos o último** traz o registro do instalador (`APLICADO_AO_CANONICO`), cujos backups de bytes têm de ser as
  cópias do elo e cujo `um_py_novo` tem de ser o do elo seguinte (l.918-950). O último elo não pode trazer instalação (l.982-983).
- **O início da cadeia é a Bancada** (versão, `um.py`, selo e o manifesto do kernel registrado, l.988-998). **O fim é o Nós
  lido agora** (l.1001-1007, l.2827-2828).

**O que devolve:**

- **No pré-selo**:
  - o bloco `salto` (l.1010-1019): `de` (com o sha do manifesto da Bancada e o `deployment_id`), `ate`, `versoes_puladas`,
    `proxima_a_selar` e o resumo da cadeia;
  - o veredito `REPINADA_B<n>__SALTO_<de>_<ate>__ENSAIO__NADA_GRAVADO_NA_BANCADA` (l.2875-2877, l.2953).
- **No pós-selo**, o recibo pré-selo do salto entra com a **mesma** cadeia (`RECIBO_PRE_SELO_SALTO_SEM_CADEIA` sem ela,
  l.1071-1073). O bloco declarado tem de ser byte a byte o recalculado (l.1074-1078), e o veredito do recibo tem de ser
  exato, com `n` igual à geração mais 1 (l.1090-1095). O selo anterior passa a ser o do **fim** da cadeia (l.1079-1080 e
  l.1125-1140). O salto só vale para a versão seguinte: `SALTO_VERSAO_NAO_CONSECUTIVA` (l.2839-2841).
- **No APLICAR**:
  - veredito `REPINADA_B<n>__SALTO_<de>_<versao>__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO` (l.2876-2877, l.2924);
  - o manifesto novo registra `sincronizacao.salto` (l.1241-1242) e, em `anterior.kernel_manifesto_sha256`, o kernel da
    Bancada que sai (l.1233);
  - o contrato ganha a seção «Salto (R3.4)» (l.1177-1183).

**Precedente que funcionou** [REAL]: v394, `REPINADA_B4__SALTO_v392_v394__APLICADA__...` (`RECIBO_SINCRONIZACAO_v394_20261019_174116.json`),
com a parada no modo «o processo já não existe» (`v394\bancada_B3_servico\RECIBO_PARADA_v394.json`). A cadeia foi a
`R3_5\CADEIA_DE_SELOS_v394.json` (`0f96cebd7c2135c1`), gerada por `R3_5\gerar_cadeia_de_selos.py` (`de838fd0cfb50e45`).

### 2.3 A v413: o que roda antes do selo e o que roda depois

Estado medido [REAL]:

- o Nós está na v412: `um.py` `3e741dcaa58ef2b8`, selo `60f00e9818f71b73`, kernel `1ef88a6bb8c1971b`, e o selo pina os dois;
- a Bancada está na B20-v411: `um.py` `1203b1f9202020d6`, selo `d52de88162106768`, kernel registrado `4047eb456795ae86`;
- `v412\base_v411` confere com o que a Bancada pina (3 de 3) e `v413\base_v412` confere com o Nós de hoje (3 de 3).

**Prazo duro.** O pré-selo do salto lê o Nós com `--versao v412` (`ler_nos`, l.550-637). Quando a v413 for instalada no Nós
(o `APLICADO_AO_CANONICO` da v413, antes do rito), `ler_nos` recusa com `SELO_NAO_PINA_O_UM_PY_DO_DISCO` (l.564-566) e,
depois do selo, com `SELO_VERSAO_DIFERENTE` (l.562-563). Aí o salto só poderia ser refeito para a v414 (`proxima_a_selar`,
l.1017). A janela da v412 se perdeu exatamente assim (`p00_precondicoes_v412.py` l.136).

**Antes da instalação da v413** (Nós ainda na v412):

- **a.** A cadeia v411→v412: `python -I -B -X utf8 R3_5\gerar_cadeia_de_selos.py --cadeia work\cadeia_de_selo --de v411 --ate v412 --saida <novo>`.
  Medi a seleção que ele faria (l.48-69, refeita sem gravar): há **exatamente 1** registro que confere,
  `v412\APLICADO_AO_CANONICO_20261118_235146.json` (backup `1203b1f9202020d6`, novo `3e741dcaa58ef2b8`). Os backups
  `Nós\um.py.bak_20261118_235146`, `Nós\um_absoluto_selo.json.bak_20261118_235146` e
  `Nós\tgl_kernel_proof_manifest.json.bak_20261118_235146` existem e são, byte a byte, as cópias de `v412\base_v411`.
- **b.** A bateria da v412, com `pinos_da_versao` v412. **Não existe**: não há `v412\bateria_pos_selo` nem
  `v412\PINOS_BN_v412.json` [REAL]. Veja N2.
- **c.** O ensaio pré-selo do salto:
  `--producao --nos <Nós> --versao v412 --fase pre_selo --modo ensaio --bateria <v412> --bateria-sha256 ... --cadeia-de-selos <a> --cadeia-de-selos-sha256 ... --saida work\cadeia_de_selo\v413\bateria_pre_selo\ensaio_1`
  (as raízes admitidas para `--saida` estão em l.220-230). Veredito esperado: `REPINADA_B21__SALTO_v411_v412__ENSAIO__NADA_GRAVADO_NA_BANCADA`.
  Não precisa do serviço (`guarda_servico` só age no APLICAR, l.2686) e não grava na Bancada.
- **d.** Conferência do recibo de salto, pino, prova de produção intacta, limpeza; `PINOS_BN_v413` final (recibo pré-selo,
  cadeia, selo e kernel anteriores da v412, delta); `p00` da v413.

**Depois do selo da v413:**

- **e.** A bateria da v413, com pinos da v413.
- **f.** O passo 10, ensaio pós-selo:
  `--versao v413 --fase pos_selo --modo ensaio --recibo-pre-selo (+sha) --cadeia-de-selos (+sha) --selo-anterior v413\base_v412\um_absoluto_selo.json --kernel-manifesto-anterior v413\base_v412\tgl_kernel_proof_manifest.json --kernel-recibo KERNEL_RECIBO_v413 (+sha) --criterios CRITERIOS_v413 (+sha)`.
  Veredito esperado: `REPINADA_B21__SALTO_v411_v413__ENSAIO__NADA_GRAVADO_NA_BANCADA`.
- **g.** O passo 10a: recibo da parada, no modo `ja_fora_do_ar` se ela seguir desligada (como na v394).
- **h.** O evento c1 da v413.
- **i.** O passo 10b, APLICAR. Veredito esperado: `REPINADA_B21__SALTO_v411_v413__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO`,
  manifesto `B21-v413-<data>-R1` (l.1219).
- **j.** O passo 10c: religar e gravar o recibo.
- **k.** O passo 11: fechar.

O manifesto da Bancada não pode mudar entre `c` e `i`, porque `montar_salto` embute o sha dele e o `deployment_id`
(l.1014-1015, conferidos em l.1074-1078). Ligar e desligar o servidor não o muda.

### 2.4 Onde o molde herdado recusa o salto por desenho [DERIVADO, lido no código]

| arquivo (sha16) | linhas | por quê |
|---|---|---|
| `rodar_ensaio_1_pre_selo_v412.sh` (`fdde7d09cbe68cfc`) | l.10-12, l.25-39 | `--versao v411`, pinos da v411, sem `--cadeia-de-selos`; espera `JA_SINCRONIZADA` |
| `conferir_recibo_pre_selo_v412.py` (`3bb1c19b994fc1fb`) | l.63; l.86; l.117; l.118; l.119-122; l.129-134; l.135; l.136-137; l.169 | `glob` de `RECIBO_..._v411_*`; chama a função do esboço com `cadeia=None` (com salto, dá `RECIBO_PRE_SELO_SALTO_SEM_CADEIA`); exige `JA_SINCRONIZADA`; exige salto e cadeia ausentes; versão, `um.py` e selo iguais aos da Bancada; selo anterior igual ao pinado pela Bancada; estado `OK` (com o Nós na v412 é `PIN_CHANGED`); pinos da bateria na versão da Bancada; controle com veredito sem salto |
| `gerar_pino_recibo_pre_selo_v412.py` (`7bee70b76c8cb1a4`) | l.54; l.207; l.235 | `glob` v411; `utilizavel` exige `JA_SINCRONIZADA__ENSAIO`; «sem cadeia» |
| `diff_e_pinos_v412.py` (`b319a101f9e33740`) | l.13; l.93; l.108; l.118-120 | «sem salto»; `sem_salto: True`; `assert` de que a Bancada pina a `BASE_VERSION` do `um.py` (no salto, a base da Bancada é a v411 e a do `um.py` é a v412); selo e kernel anteriores da v411 (no salto são os da v412, o fim da cadeia); nenhum pino de cadeia |
| `p00_precondicoes_v412.py` (`e7add69ffb7791ed`) | l.133; l.140 | o pino tem de dizer `JA_SINCRONIZADA`, `versao_nos` v411 |
| `pos_rito\bn_v412.sh` | l.7; l.39; l.43; l.92-95; l.122-126 | vereditos sem `__SALTO_`; **recusa** o pino `cadeia_de_selos`; `selo_anterior_v411`; comandos sem `--cadeia-de-selos` |
| `pos_rito\b3_recibo_v412.py` (`593651871b54b212`) | l.13 e l.27-28; l.60-61; l.78; l.81-82; l.85; l.92; l.98 | sem terceiro argumento (a cadeia); recusa o pino de cadeia; veredito exato sem salto; recusa `__SALTO_`, `salto` e `cadeia_de_selos`; `B<n>-v412-`; `v412` |
| `recibo_religamento_v412.py` | l.65; l.73-74; l.77; l.80 | só `bancada_B3`; `assert "__SALTO_" not in`; `B<n>-v412-`; `canonical_version == v412` |
| `fechar_v410.py` (molde do 11) | l.98 | exige `"__SALTO_" not in` e `salto` vazio |
| `delta_v412_r7.py` (`76326709aacd6a74`) + `v411\delta_v411.py` (`8746e98bafa463f9`) | `delta_v412_r7` l.16-18; `delta_v411` l.87-96 | o `delta_v411` é importado sem fixar `BANCADA_PINA_HOJE`; o `assert` exige a Bancada em v410 ou v411 (l.92). Depois do APLICAR B21-v413, todo script que importa a cadeia de deltas quebra na importação |

---

## 3. As pendências: arquivo, linha e conserto proposto (nada aplicado)

Lista: `v412\revisao_19nov\PENDENCIAS_DO_MOLDE_PARA_O_BN_DA_v413.md` (sha16 `17ac5112d58f15a9`). Nela há **15** itens: 5 da
primeira revisão (l.16-20), 8 da segunda (l.23-30) e 2 do construtor (l.37-39). Já estão feitos no molde, conferidos na
leitura: 1.1, 1.2, 1.3, 1.5 e C.2. Seguem abertos 10 itens; para todos há conserto proposto abaixo. Em todos os scripts
derivados para a v413 vale o mesmo: os rótulos `v412` viram `v413`, menos os «anteriores da Bancada», que seguem v411 (N6).

| # | pendência | estado | arquivo:linha | conserto proposto |
|---|---|---|---|---|
| 1.1 | `gerar_pino`: sair ≠ 0 se o pino não for utilizável ou a produção não estiver intacta; `inicio_utc` entre as fotos | **feito** | `gerar_pino_recibo_pre_selo_v412.py` l.142-147, l.205-207, l.277-278 | Para o salto, em l.207 trocar `startswith("JA_SINCRONIZADA__ENSAIO")` pela igualdade com `"REPINADA_B%d__SALTO_v411_v412__ENSAIO__NADA_GRAVADO_NA_BANCADA" % (GER+1)`, com `GER` lido da produção; em l.54 o `glob` passa a v412; l.62-63 passam aos pinos da v413; acrescentar ao pino o sha da cadeia e o bloco `salto` |
| 1.2 | `rodar_bn_pre_selo`: rc real do `limpar`, `utilizavel` do pino, recusar `etapa1_stdout.txt` velho | **feito** | `rodar_bn_pre_selo_v412.sh` l.38-41, l.52, l.57-61 | Na v413, só trocar o sandbox literal `C:\t\vb23` (l.20, l.37, l.42) por um lido do delta (N8) |
| 1.3 | `conferir_recibo`: cabeçalho com `v412\base_v411` | **feito** | `conferir_recibo_pre_selo_v412.py` l.2 | — (o conferir do salto é o C.1) |
| 1.4 | o `PINOS_BN` com o pino do próprio delta por sha; vb22 → vb23 nas guardas estáticas | aberto | `diff_e_pinos_v412.py` l.113-123 (o dicionário `pn`); `bn_v412.sh` l.35; `guardas_estaticas_bancada_v412_r7.py` l.10, l.38-39, l.111-113 (`f784956ce8d45ea9`) com `delta_v412_r7.py` l.47 (`SANDBOX_CURTO = vb22`) | (a) Acrescentar a `pn` a chave de topo `"delta": f(<delta_v413 vigente>)`. Hoje o delta só aparece como `fonte_delta_v412_r7` (l.147-149), que nenhum runner confere. (b) Pôr `delta` na lista do `b3_prepara` (bn l.35), para o pós-selo recusar um delta trocado. (c) No `delta_v413`, `SANDBOX_CURTO = C:\t\vb24` (pasta nova; conferir antes que não existe). As guardas e os runners usam `DL.SANDBOX_CURTO`, nunca um literal; o texto das guardas (l.10, l.39) diz a pasta lida |
| 1.5 | `fim_de_cadeia_v412.sh` lê o delta obsoleto: NÃO RODAR | **feito** | `fim_de_cadeia_v412.sh.NAO_RODAR.md` (`3bbc0e58b4f3b306`) | — |
| 2.1 | volta do passo 11: pino conjunto dos três recibos com o seq do evento; reconferência depois do nascimento; tolerância a repetição; trava rc 2; entrega onde o evento pede | aberto | `bn_v412.sh` l.12 e l.24 (`ORDEM="10 10a 10b 10c"`); molde `fechar_v410.py` l.89-127 | (a) `ORDEM="10 10a 10b 10c 11"` e um bloco `quer 11` que roda o `fechar_bn_v413.py`. (b) O `fechar_bn_v413.py`, derivado de `recibos_b3()`: `glob` de `bancada_B3` e `bancada_B3_[0-9]*` (como l.93), escolhendo o APLICAR cujo sha do manifesto novo é o da produção; **exige** o salto: veredito igual a `REPINADA_B21__SALTO_v411_v413__APLICADA__...`, `salto.de.versao` v411, `ate` v412, `proxima_a_selar` v413, `cadeia.sha256` igual ao pino; confere parada e religamento como em l.103-118, com v413. (c) Grava `PINO_RECIBOS_B21_v413.json` com caminho, sha256 e bytes dos três e mais `evento_c1: {seq, hash}`, relê os três e compara os sha depois de gravar (a reconferência). (d) Sai com rc 2 sem gravar nada se faltar qualquer um (como l.122-127). (e) Copia os três recibos e o pino para a pasta que o evento 1687 nomeia (`work\iald_v412_20261119\bench`) e confere as cópias por sha |
| 2.2 | o `evento()` da parada e do religamento confere a cadeia do livro e recusa linha ilegível | aberto | `recibo_parada_v412.py` l.25-40 (pula linha não JSON em l.31-36); `recibo_religamento_v412.py` l.28-43 (l.34-39) | Trocar o corpo pelo da regra do esboço (`sincronizar_bancada.py` l.693-707): percorrer todas as linhas não vazias; `json.loads` que falha encerra com `assert`, nunca `continue`; exigir `e["anterior"]` igual ao hash anterior e `e["hash"]` igual ao `sha256(json.dumps({k: v sem "hash"}, ensure_ascii=False, sort_keys=True))`; recusar seq duplicada; devolver o elo e o número de elos conferidos |
| 2.3 | o religamento acha o recibo do APLICAR numa repetição (`bancada_B3_<k>`) | aberto | `recibo_religamento_v412.py` l.65-66; o executor cria `bancada_B3_$k` em `bn_v412.sh` l.119 | `glob` de `..\bancada_B3\RECIBO_SINCRONIZACAO_v413_*.json` mais `..\bancada_B3_[0-9]*\RECIBO_SINCRONIZACAO_v413_*.json`, filtrando os de veredito `...__APLICADA__...`; exigir exatamente 1 cujo `manifesto_novo.sha256` seja o sha atual do `canonical_contracts.json` |
| 2.4 | pino pendente (sha256 None) dá AGUARDA 20, não traceback rc 1, no `b3_prepara` | aberto | `bn_v412.sh` l.36-37 | Logo depois de `tem_pino`: `a=$(pino "$k"); p=$(pinop "$k"); if [ -z "$a" ] \|\| [ "$a" = "None" ] \|\| [ "$p" = "None" ]; then aguarda "o pino $k esta' pendente (NAO_PREPARADO) em PINOS_BN_v413.json; retomar com CHAIN_DE=$1"; fi`; só então `sha256f` |
| 2.5 | o `diff_e_pinos` põe o `DIFF_vANT_vNNN.diff` em `pendentes` se não houver `diff` no PATH | aberto | `diff_e_pinos_v412.py` l.83-84 (`pendentes` só nasce em l.88) | Mover `pendentes = []` para antes de l.77 e, no `else` de l.83-84, `pendentes.append(_NDD)`. O `p00` e o `b3_prepara` passam a tratar `pendentes` não vazio como AGUARDA |
| 2.6 | o `evento_c1_b3` confere o rc do `iald.py`; a ordem ENSAIO → evento → APLICAR imposta | aberto | `evento_c1_b3_v412.py` l.19-22 | (a) Antes de anotar, exigir `pos_rito\b3_ensaio_out.txt` e `b3_recibo_v413.py <ensaio_out> ensaio <cadeia>` com rc 0. (b) Depois de anotar, `assert r.returncode == 0`; ler do stdout o JSON `{"ok": true, "evento": N, "hash": H}` (o formato que o quadro devolveu em `bench\HANDOFF_C1.json`) e imprimir `EVENTO=N EVENTO_HASH=H`. (c) No bn l.113-118, recusar o 10b se o `quando` do evento (lido do livro pela seq) não for posterior ao `fim_utc` do recibo do ensaio |
| 2.7 | o delta da v413 fixa o `BANCADA_PINA_HOJE` anterior; o `PINOS_BN` final, com o recibo pré-selo, antes do APLICAR | aberto | `delta_v412_r7.py` l.16-18; `delta_v411.py` l.87-98; molde da fixação em `delta_v411.py` l.35-45 | No `delta_v413`, carregar o `delta_v411.py` por fonte e trocar, por regex, a linha `BANCADA_PINA_HOJE = _bancada_pina_hoje()` (l.96) por `{"version": "v411", "deployment_id": <lido de RECIBO_RELIGAMENTO_v411.json>, "n": 20}`, como l.40-42 fizeram para a v410. Fixa-se a **v411** e não a v412: a v412 não teve B(n). Expor esse módulo a quem o `delta_v412_r7` importa (l.16-18 trocadas, por fonte, para usar o módulo já fixado). Definir no `delta_v413` um `_bancada_pina_hoje()` que admite `{v411, v413}`. No bn, exigir `pendentes == []` no `PINOS_BN_v413.json` antes do 10b |
| 2.8 | controle negativo: mutações para o bloco `ja_fora_do_ar` e para as chaves do recibo (hoje 6 de 41 condições exercitadas) | aberto | `controle_negativo\mutar_conferidor_v412.py` l.92 (lista `MUTACOES`, M1–M6; `1ee8f109bb6c1a68`); 41 condições em `conferir_exigencias_servico_v412.py` (`f11a21318bce3db4`; resultado em `revisao_19nov\ENSAIO_HERMETICO_RESULTADO_CONTROLE_NEGATIVO_v412.json` l.21-32) | Acrescentar: M7, o `assert` de l.91 da parada sai (PID com `ja_fora_do_ar`); M8, a conferência do diagnóstico por sha sai (l.96-97); M9, aceitar `VIVO` com `um_bancada` (l.103); M10, uma chave do recibo sai ou é renomeada (`porta_fechada`, `religar`, `versao_servida`); M11, o `evento()` volta a pular linha ilegível (com o 2.2). Para cada uma, a condição do conferidor que deve falhar; se não houver, criá-la |
| C.1 | o `conferir_recibo_pre_selo` herdado reprova o salto | aberto | `conferir_recibo_pre_selo_v412.py` l.63, l.86, l.117-122, l.129-137, l.169 | Um `conferir_recibo_pre_selo_salto_v413.py`: carrega a cadeia por `MOD.carregar_cadeia_de_selos(CAD, CAD_SHA)` e chama `MOD.conferir_recibo_pre_selo(RP, ant, PRODUCAO, False, RSHA, SELO_V412, KM_V412, cadeia)`, com `SELO_V412` e `KM_V412` de `v413\base_v412`. Condições: veredito igual a `REPINADA_B%d__SALTO_v411_v412__ENSAIO__NADA_GRAVADO_NA_BANCADA` % (GER+1); `salto.de` igual à Bancada (v411, `um.py`, selo, `manifesto_da_bancada_sha256`); `salto.ate` igual ao Nós lido (v412); `proxima_a_selar` v413; `cadeia.sha256` igual ao pino; `versao_alvo` v412; estado `PIN_CHANGED` e `pino_velho_recusado_pelo_instalado` presente; `pinos_da_versao.versao` v412. Controles negativos: sem cadeia (`RECIBO_PRE_SELO_SALTO_SEM_CADEIA`), sha da cadeia errado (`CADEIA_DE_SELOS_SHA_DIVERGE`), selo anterior v411 (`SELO_ANTERIOR_NAO_E_O_PINADO`), veredito `JA_SINCRONIZADA` e bloco `salto` adulterado (os dois `RECIBO_PRE_SELO_NAO_CORRESPONDE`) |
| C.2 | `nos_v411_do_cofre` sem uso: NAO_USAR | **feito** | `MOMENTO_DO_PRE_SELO.json` l.2-5 (`7bf389265a0ca682`); `nos_v411_do_cofre.PODAVEL.md` | — |

### 3.1 O que a lista não tem

- **N1. O prazo.** O pré-selo do salto só roda com o Nós na v412: antes da instalação da v413, não antes do selo (seção 2.3).
  Nada na lista nem no contrato da v413 fixa esse momento.
- **N2. A bateria da v412 não existe.** O `gerar_bateria_r3_4.py` (`02b1cce70a7b77c2`) exige `--pinos-bn` cujo
  `candidato.sha256` seja o `um.py` do Nós (l.57-63), e não há `PINOS_BN_v412.json`. São dois caminhos:
  - (a) um pino mínimo `{"candidato": f(v413\base_v412\um.py)}` gravado por script, com nota dizendo por que existe;
  - (b) rodar o `diff_e_pinos_v412.py` só para isso, que grava o `PINOS_BN_v412.json` com o recibo pré-selo pendente
    (não executado; ele escreve na pasta da v412 selada).

  Em qualquer dos dois, a bateria fica numa pasta que **não** seja ancestral da `--saida`, porque o esboço recusa
  `SAIDA_NA_PASTA_DE_FONTES` (l.2548-2562). Por exemplo, `v413\bateria_v412_pre_selo\` com saída em `v413\bateria_pre_selo\ensaio_1`.
- **N3. A cadeia depende de backups no Nós.** `um.py.bak_20261118_235146` (46,8 MB), `um_absoluto_selo.json.bak_20261118_235146`
  e o registro `v412\APLICADO_AO_CANONICO_20261118_235146.json` têm de sobreviver até o fechamento do B21. A poda do LAR não
  pode alcançá-los [OPEN: a regra do LAR não foi lida]. E nada pode escrever no Nós nem na Bancada durante o pré-selo, senão
  a prova de produção intacta reprova.
- **N4. A autorização da v413.**
  - Os dois recibos leem o evento 1687 exigindo `versao == "v412"` (parada l.45, religamento l.48) e a ordem direta que
    nomeia «v412» (parada l.59, religamento l.62).
  - O 1687 autorizou «iniciar o serviço na porta 18777, rodar essa bateria, aplicar B20→B21 e conferir a versão após o
    reinício» no ciclo da v412 (`BENCH_AND_QUEUE_OPERATOR_APPROVAL.json`, `0c09a73ee42628f7`). Depois o operador escolheu
    «Salto na v413» (`OPERADOR_19nov_B21_salto_na_v413_verbatim.txt`, `d96a96140eaa8d7f`).
  - Se esse par cobre o ciclo da v413 é leitura, não fala dele por bytes. Ou a gerência decide ler 1687 e 1689 juntos (e
    os scripts conferem os dois), ou pede uma linha nova ao operador.
- **N5. A importação dos deltas quebra depois do APLICAR** (refina o 2.7). O `assert` em `delta_v411.py` l.92 dispara
  assim que a Bancada passar a v413, porque `delta_v412_r7.py` l.16-18 importa o `delta_v411` vivo.
- **N6. Há dois «anteriores».** O da **Bancada** é v411: o `rel411` da parada (l.72), o `rb_ant` do religamento (l.69-72),
  o `BANCADA_PINA_HOJE`, o `assert` do `diff_e_pinos` (l.108) e o `b3_recibo` (l.55-56). O do **`um.py`** é v412: o selo e
  o kernel anteriores, a base e o `DIFF_v412_v413`. Uma subida mecânica de rótulo (411→412, 412→413) erra o primeiro tipo.
- **N7. O contrato da v413 condiciona o B(n) ao serviço.** `CONTRATO_v413_R0.md` l.126-127 diz: «ele roda se a Bancada
  estiver no ar com a atualização do Codex; se não estiver, a decisão volta ao autor». Mas o R3.6 não precisa do serviço no
  ensaio, e o APLICAR o exige **parado** (l.2684-2692). Como está, a condição repete a armadilha da v412.
- **N8. O sandbox curto diverge.** O `delta_v412_r7.py` l.47 diz `vb22`; os runners usam `vb23` escrito à mão
  (`rodar_bn_pre_selo_v412.sh` l.20, l.37, l.42; `conferir_recibo_pre_selo_v412.py` l.38); as guardas usam `DL.SANDBOX_CURTO`.
  Na v413, uma pasta nova (por exemplo, `vb24`) tirada do delta por todos.
- **N9. O religamento não deixa log.** Desde 04/11 o comando do rito não escreve log (seção 1.1). Na v413, religar com
  stdout e stderr em `estado\servidor.log` e `estado\servidor_erros.log`, como faz o `abrir_bancada.pyw` (l.35-39), e
  registrar isso no recibo.

---

## 4. O que o Codex do app espera da gerência (F0.6)

- **O pedido** (`eventos.jsonl`):
  - 1686, `SOLICITACAO_A_GERENCIA`, de `codex-app-v412-01a094df`, hash16 `ffafd945fb95062a`: «F0.6 requer evento c1 para
    B20/B21 … Solicita-se à gerência preparar o vínculo da ordem verdadeira e o evento próprio quando houver a decisão».
  - 1687, `AVISO_AUTORIZACAO_RECEBIDA`, hash16 `9aa0c94656828380`: «À c1 existente: emitir o evento próprio
    F0.6/SINCRONIZACAO_BANCADA, coordenar a bateria pós-selo, B20→B21 e verificação após reinício, com revisão distinta e
    os três recibos. Retorno em C:\IALD\Central de Patentes\work\iald_v412_20261119\bench».
- **Depois do 1689** (hash16 `2a6975de28ad6b85`, «Salto na v413»), o Codex encerrou a espera. `C1_RETURN_VERIFIED.json`
  diz `next_action`: «Revalidate and perform the authorized bench jump during the v413 cycle under F0.6». `ROUTE_RETURN_NOTE.json`
  diz «Acompanhar o ciclo v413 pela F0.6».
- **A forma esperada**, a mesma dos eventos 1603 (v410) e 1617 (v411) e das chaves fechadas do esboço:
  1. Um evento `tipo SINCRONIZACAO_BANCADA`, `quem claude-c1`, `unidade F0.6`, com
     `dados = {"versao": "v413", "acao": "sincronizacao", "bancada": "C:\\IALD\\Bancada_Um", "um_py": <sha256 do um.py v413>, "selo": <sha256 do selo v413>, "unidade": "F0.6"}`.
     É o mesmo que o `--evento` e o `--evento-hash` do APLICAR conferem.
  2. Os **três recibos**: o `RECIBO_SINCRONIZACAO_v413_*` do APLICAR, o `RECIBO_PARADA_v413.json` e o `RECIBO_RELIGAMENTO_v413.json`,
     com revisão independente, devolvidos na pasta `bench` que o 1687 nomeia.
  3. A **verificação ao vivo**. O Codex confere por GET em `/api/contratos` (`iald_v412_20261119\verify_c1_return.py` l.25-35)
     e espera `canonical_version` v413 e `deployment_id` `B21-v413-…`.
  4. Um evento de aviso F0.6 apontando os três, para o Codex encerrar a unidade dele.
- **O app** não depende da gerência: a atualização do app tem autorização permanente (`BENCH_AND_QUEUE_OPERATOR_APPROVAL.json`,
  bloco `queue`), e o app e a fila da v412 já foram entregues (`C1_RETURN_VERIFIED.json`). O Codex não executa o B(n): o
  esboço só aceita evento de `claude-c1` (l.713-714).

---

## 5. Proposta para a v413 e daqui em diante

### 5.1 A v413, passo a passo

0. **Agora, sem tocar em nada:**
   - a gerência corrige o `CONTRATO_v413_R0.md` l.126-127 (N7);
   - decide a autorização (N4);
   - lê ao operador a partitura (5.4);
   - pede ao LAR, ou a quem poda, que preserve os backups e o registro da N3.
1. **Antes da instalação da v413, com prazo** (N1). Adaptar só o molde do pré-selo para o salto:
   - gerar a cadeia v411→v412 (seção 2.3.a) e a bateria da v412 (N2);
   - fazer o `rodar_ensaio_1` com `--versao v412` e a cadeia;
   - fazer o conferir do salto (C.1) e o `gerar_pino` aceitando o veredito do salto (1.1);
   - usar um sandbox novo tirado do delta (1.4, N8).

   Depois, uma revisão independente única, como a gerência decidiu em 19/11 (lista, l.32-34), e rodar o pré-selo. Ele lê a
   produção e o Nós, grava só em `v413\`, não precisa do serviço e, pela leitura, não usa a placa.
2. **`PINOS_BN_v413` final** (2.7), com o recibo pré-selo, o pino da cadeia, o selo e o kernel anteriores da v412 e o
   delta (1.4); e o `p00` da v413 conferindo o pino do salto.
3. **Pós-selo adaptado**, revisado na mesma revisão única se couber: `bn_v413.sh` com os argumentos da cadeia, o `b3_prepara`
   com AGUARDA (2.4) e o passo 11 (2.1); `b3_recibo_v413.py` com terceiro argumento (a cadeia) e o veredito do salto; os
   recibos de parada e religamento com 2.2, 2.3 e N6; o evento com 2.6; o delta com 2.7; as mutações de 2.8.
4. **Depois do selo**: 10 → 10a (`ja_fora_do_ar`) → evento → 10b → 10c → 11; entrega ao Codex (seção 4).

### 5.2 Quando religar o servidor, e com que recibo

- **Não antes do APLICAR.** Até o B21-v413, ligar só traz o modo degradado (seção 1.5): nenhuma conta científica, um
  contexto CUDA na placa do treino na primeira leitura de `/api/estado`, e a obrigação de parar pelo PID antes do 10b.
- **No 10c, depois do 10b.** O recibo é o `RECIBO_RELIGAMENTO_v413.json`, pelo `recibo_religamento_v413.py`. Ele confere
  em `/api/contratos` a versão v413, o deployment `B21-v413-<data>-R1`, o sha do manifesto igual ao do APLICAR, o `um.py`
  igual ao do Nós, e o PID lido da porta. O lançamento vai com log (N9).
- **Se o treino ainda estiver na placa no 10c**, há três saídas, e a escolha é do operador:
  - (a) esperar o treino acabar;
  - (b) lançar com `CUDA_VISIBLE_DEVICES=-1` (motor em CPU, sem contexto CUDA [DERIVADO]); o lago ainda ocupa até 60% da
    RAM livre;
  - (c) lançar normal, aceitando o contexto e as alocações sob demanda.

### 5.3 A medida permanente, com os riscos

> [nota operacional do operador — omitida no retrato público]

### 5.4 A partitura, para o operador ler antes (uma linha, na língua dele)

«Ligar a Bancada agora não adianta: desde que a v412 entrou no Nós ela recusa toda conta, porque o programa mudou, e só o
B21 da v413 a devolve. O B21 é uma conferência de identidade, não de física: decide se a Bancada pode passar a servir o
programa selado; não decide nada sobre a teoria, o selo ou o gate. Se der negativo, é a ferramenta recusando, uma parede
medida, e nada é gravado na Bancada. A única janela é rodar o pré-selo antes de a v413 entrar no Nós.»

### 5.5 Recomendação

- Corrigir N7 no contrato.
- Rodar o **pré-selo do salto antes da instalação da v413**: é o único passo com prazo, e não precisa do serviço nem da placa.
- Deixar o religamento para o 10c, com log, e planejá-lo em relação ao treino.
- Adotar **A + B + C** como medida permanente (ver e avisar sem ligar).
- Deixar **D** fora até uma ordem expressa do operador.

---

## Anexo: o que foi examinado, para o Mapa de Rotas (a gerência registra)

- **Consultado antes:**
  - `rotas.py consultar "bancada"`: 140 rotas, lista truncada pela ferramenta;
  - `rotas.py ver bancada.b21_v412.revisao_e_decisao_19nov`: seq 2174, veredito `B21_V412_NAO_FEITO__SALTO_NA_V413_POR_DECISAO_DO_OPERADOR__MOLDE_REVISADO_COM_RESSALVAS`;
  - `não refazer`: o pré-selo pela cópia da v411 do cofre.
- **Examinado agora**, sem dado observado (`olhou_dados: false`):
  - a causa do desligamento: o reinício de 16/11 e a ausência de início automático;
  - o modo degradado: PIN_CHANGED desde 18/11 23:51;
  - o uso da placa e da RAM, pela leitura do código;
  - a viabilidade da cadeia v411→v412, medida: 1 registro do instalador, backups presentes e conferentes;
  - o prazo do pré-selo;
  - 10 pendências abertas com conserto proposto e 9 pontos novos (N1–N9);
  - a expectativa do Codex (F0.6).
- **Não refazer:** a leitura dos logs e do sistema, as medidas de sha e a seleção da cadeia (saídas nesta pasta).
- **Próximo passo:** a ordem de adaptar o pré-selo do salto, antes da instalação da v413.
- **Erro de procedimento, dito:** um comando meu abriu um interpretador Python interativo em segundo plano (entrada vazia).
  Ele foi parado pela própria ferramenta (TaskStop) em menos de 3 minutos; conferi que não ficou processo; nada foi gravado.
