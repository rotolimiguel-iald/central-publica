# O ORGANISMO — a torre de comando única (v2, depois da revisão adversarial)

> Exame da sessão a7 da Central (Claude), 23/10/2026, por ordem do operador (verbatim em
> `work/php_e_v396_22out/OPERADOR_23out_organismo_e_handoff_kimi_verbatim.txt`): «eu estou tentando integrar tudo em uma coisa só … não
> pode haver segredo entre as IA's … todas devem estar integradas sob a mesma torre de comando respondendo ao mesmo verbo … atualizei o
> um.py … já atualiza tudo automaticamente … a interface seja o meu próprio app … "ordem do operador" → o Jev aciona você e você execute o
> exército de IA's … talvez vc tenha uma ideia melhor».
> **v2:** a v1 (ao lado, `.bak_*_v1`) passou por quatro céticos só-leitura (viabilidade, custo, segurança, completude; modelo barato), que
> devolveram 29 achados: 4 sustentados, 1 refutado, o resto fraco ou faltante. Tudo o que mudou está marcado **[cético]**.
> Estatutos: `[REAL]` medido nesta máquina hoje · `[KNOWN]` lido de documentação ou ferramenta, não medido aqui · `[OPEN]` não sei ·
> `[PROPOSTA]` desenho. A régua vale inteira: nada aqui move gate, confirma coisa alguma ou tira do operador o que é dele.

## 1. O que já existe — não se refaz

| peça | o que é | estatuto |
|---|---|---|
| Memória comum ACOM (`C:\IALD\MEMORIA_IALD`) | inscrição por sha256 da ordem (`session_memory.py init`), estado q/p, transições com CAS, uma referência exata por tarefa; MISSION_PROTOCOL (`mission_cli.py`: `configure/extend/claim/submit/accept/hold`, requisitos, revisões, leases, evidências — **só sobre referência já criada pelo `init`** [cético]); ACTIVITY_PROTOCOL; o app já recebe atividade e mostra «aguardando revisão» | `[REAL]` usada hoje |
| A fila única e o orquestrador (`iald-orchestrator`, MCP em `~/.claude.json`; `mcp_server.py` em `Chatgpt\IALD_ORQUESTRACAO_20260923`) | `iald_coordination_submit/get/action`, `iald_selection_preview`, `iald_transport_next`; executores Kimi, MiMo, DeepSeek, Codex, Claude, Qwen local; Jev nas decisões estruturadas; memória científica da fila sincronizada POR VERSÃO (v396: `work/scientific_memory_sync_20261022_v396`). **A fila despacha para provedores de IA; não há executor de script local nem «gerência» como destino** [cético] | `[REAL]` |
| Os túneis | Codex: pasta + `codex queue --thread <UUID>` (medido REAL em 07/10); Kimi: handoff em arquivo (hoje); sessões do Claude Code: `ListAgents`/`SendMessage` | `[REAL]` / `[KNOWN]` (a troca entre sessões não foi medida) |
| As esteiras por script | custódia do espelho e do site; Central privada; Central pública (desde hoje num comando: `work/central_publica_22out/atualizar_central_publica.py`, com o `llms.txt` do Kimi na cadeia); memórias; mapa de rotas | `[REAL]` (v396 custodiada ontem com elas) |
| O quadro do organismo (hoje) | `tools/estado_do_organismo.py` mede cada superfície contra o selo do Nós; saída em `organismo/ESTADO_DO_ORGANISMO.{md,json}` | `[REAL]` 2ª medição: 66 OK · 0 defasado · 5 do operador |
| O molde real do braço de publicação | `subir_site.py` (SFTP com chave do host pinada, credencial no perfil do operador, recibo verificado) — **não** o wrapper da Bancada na porta 18777, que está sem escuta (netstat 0 linhas, 23/10) [cético: REFUTADA] | `[REAL]` |
| O Claude Code nesta máquina | `claude` não está no PATH; o binário vive dentro da extensão do VS Code (`anthropic.claude-code-2.1.3xx-win32-x64\resources\native-binary\claude.exe`, caminho que muda a cada atualização) [cético] | `[REAL]` |

O que é mecânico já é script. O que ainda exige modelo: (a) os textos da custódia (LEDGER, erratas, arco do site); (b) **derivar os scripts da versão seguinte** — hoje por trocas contadas, com literais digitados pela sessão (p. ex. `1425`, `29228` em `derivar_fim_v396.py`) [cético]; (c) julgar; (d) falar com o operador.

## 2. Diagnóstico — por que ainda não é um organismo

1. **A verdade estava na memória de quem custodiou, não numa medida.** `[REAL]` os dados literais do selo no site ficaram na v392 por duas custódias; o quadro teria acusado no mesmo minuto.
2. **A cadeia não é um programa.** A ordem dos passos foi extraída do próprio transcrito da sessão; os scripts são derivados por versão, não parametrizados. Por isso «95% script» é verdade para a EXECUÇÃO e falsa para a AUTORIA: os scripts de cada versão são escritos pelo modelo [cético].
3. **O gatilho é humano** e não há vigia do selo.
4. **As sessões interativas não são serviço** (morrem com a janela, compactam, não recebem ordem do app) — e por isso cron/Monitor de sessão também não servem de relógio ao organismo: o relógio é o Agendador de Tarefas do Windows [cético].
5. **Credenciais.** «Sem segredo entre as IAs» não precisa significar «todas veem a senha»; pode significar **«nenhuma IA precisa ver a senha»**: a capacidade vira um executor local com a credencial no próprio ambiente, que devolve recibo. O classificador de ontem bloqueou a difusão de credencial, não a integração.
6. **Gates humanos por desenho** (a régua): confirmação/creditação, nome das pedras, [LEGAL], Zenodo, pagamento, apagar banco, reescrever histórico público, senha do cofre. Ficam como `PENDENTE_OPERADOR` no quadro.
7. **O quadro mede só a cadeia do selo** [cético]: faltam app (TestFlight/APK), Jev, Nós vivo, IALD nativa, bancada do ChatGPT, Zenodo, backup 3-2-1, túneis, manifesto/leitor de IA, regra da linhagem. Parte entrou hoje (Nós vivo, linhagem, túneis, bancada, Zenodo, sitemap, leitor, serviços locais); app, Jev e 3-2-1 seguem fora. «0 DEFASADO» vale só para o conjunto declarado de superfícies.

## 3. O desenho — cinco peças, em ordem de gate `[PROPOSTA]`

**G0 — O QUADRO (feito).** O quadro **só informa** [cético]: nunca acorda o modelo por hora. Cada defasagem tem classe — AUTOMATIZÁVEL (script resolve), JULGAMENTO (gerência, **uma vez por defasagem nova**, pelo hash do item) ou OPERADOR — e FALHA de leitura bloqueia a missão (não é «ok»). Relógio: tarefa agendada do Windows, de hora em hora; o quadro vai ao painel do app e ao `PROGRAMA_IALD`.

**G1 — A CADEIA COMO PROGRAMA.** `custodia.py <vNNN>` parametrizado: **nenhum número de versão digitado — todos lidos do selo, do core e do manifesto por script** [cético]; checkpoint e retomada; cada passo com o seu conferidor. Os textos públicos (LEDGER, arco, erratas) saem de um modelo como **candidato DECLARADO** e passam por três portões: (1) as asserções que os geradores já têm; (2) um **gate de pré-push de lista fechada** [cético] — `CONFIRMED` sem `NOT_`, «provada» sem estatuto, «pós-dição» como demérito, hash citado ≠ artefato → bloqueia; (3) **revisor distinto** (um cético de modelo), e, na fase inicial, aprovação do operador no app para texto público novo, até N custódias sem erro (a mesma rampa do HSTS). Oráculo do G1 em dois níveis [cético]: artefatos finais iguais aos de ontem **e** as mesmas asserções passando; validado contra duas transições (v394→v395 e v395→v396), não uma.

**G2 — O GATILHO.** Vigia (script agendado) sobre o Nós. **Idempotência** [cético]: chave = `um_version + sha16 do selo`; no máximo uma missão aberta por versão; o vigia lê a ACOM e **nunca abre se a referência já existir**; N tentativas e depois `PENDENTE_OPERADOR`. Abertura em dois passos, com o que existe [cético]: `session_memory.py init` (fonte = o handoff, por sha256) → `mission_cli.py configure` (critérios = linhas do quadro). Despacho: **como a fila não tem executor de script local, o vigia chama `custodia.py` diretamente; a fila entra só para as IAs** (textos à gerência, leituras longas ao Kimi/DeepSeek, código ao Codex) até existir o executor local (G3). Falha fica visível na missão.

**G3 — O BRAÇO DE PUBLICAÇÃO (capacidade, não credencial).** Executor local, molde `subir_site.py`, com as credenciais no ambiente do processo e **ações com lista fechada**: `publicar_site(manifesto)`, `push(repositório)`, `regra_cloudflare(zona, expressão)`. Três regras que a v1 não tinha [cético]: (a) **allowlist de emissores** — só a gerência e o Jev, e todo pedido cita a referência ACOM e o sha256 da ordem do operador; o braço recusa pedido sem ordem verificável; (b) **portão de conteúdo** — o braço só aceita manifesto gerado pela esteira e já passado pelos conferidores (guarda pública, conferência do delta, varredura de credencial e de Escritório); pedido vindo de IA externa (Codex, Kimi) fica `PENDENTE_OPERADOR` até aprovação no app; (c) **o token do Cloudflare** com escopo mínimo (uma zona, Firewall Services: Edit), TTL e restrição de IP, guardado no Credential Manager do Windows ou em arquivo com ACL do usuário fora de `C:\IALD`, lido só pelo processo do braço. O recibo prova que a subida ocorreu; o portão de conteúdo é o que prova que estava certa.

**G4 — O CONSOLE É O APP.** «ordem do operador» no app, logado (rota só de administrador; o backend já usa `subprocess` e já instala o orquestrador como blueprint [cético: SUSTENTADA]) → o Jev classifica → a ordem é gravada verbatim com sha256 → missão → GERÊNCIA como **processo destacado com id de tarefa**, fora do worker do Flask [cético]. Formas de a gerência existir como processo `[KNOWN; nenhuma medida aqui]`: (i) Claude Code não interativo (`claude -p`) com o mesmo `CLAUDE.md`, memórias e MCPs; (ii) Claude Agent SDK dentro do backend (API, fora do plano); (iii) Managed Agents da Anthropic (a casa sairia desta máquina). Recomendação: (i), **depois de medir** [cético]: fixar o caminho do binário (ou instalar o CLI avulso), rodar `--help` e um `-p` mínimo sem ferramentas, registrar a versão e o consumo do plano. A aprovação do operador no app precisa de uma ponte com o protocolo de missão [cético]: `mission.py` só aceita ator `agent` e proíbe fabricar autenticação pelo nome; proposta: o app grava uma evidência assinada pelo login do operador (hash) e um ator «ponte do app» a cita em `review_evidence` no `accept` — a confirmar com o protocolo. **Teto diário da gerência** [cético]: lido por script antes de cada disparo; a 70% só ordens do operador passam e a custódia espera; sem fila de retentativas automáticas.

**A ideia melhor que o «exército executa a ordem»:** trocar «ordem → cascata de IAs» por **«ordem → missão medida»**. A missão nasce com critério mensurável (depois da execução, o quadro tem zero DEFASADO nas superfícies da missão); as IAs são executores intercambiáveis; o encerramento é por medida, não por relato. É a régua aplicada à própria coordenação, e é o que o MISSION_PROTOCOL já pede («tetelestai exige os critérios satisfeitos e nenhuma execução pendente»). O que falta é ligar o quadro ao protocolo: **critério = linha do quadro**.

## 4. Custo e a regra dos tokens

O «~1M de tokens por custódia» da v1 **não foi medido** [cético]: a v396 foi iterativa (≈278 comandos em duas cadeias, três transições ACOM, correções no meio), não «três entradas». O desenho passa a exigir **orçamento por custódia** (tokens e chamadas por etapa, teto duro, missão abortada ao estourar) e a medição vem dos transcritos das v395 e v396 antes de qualquer promessa. Cada `iald_coordination_submit` custa ≈6 mil tokens (GESTÃO DE TOKENS, 14/10). A gerência em `claude -p` consome plano — o plano já se esgotou numa sessão em 12–13/10 —, logo o organismo tem de ser quase todo script e a gerência entra onde só ela serve: ler o handoff e planejar; os textos (com os três portões); julgar o quadro. Kimi e DeepSeek ficam com as leituras longas; Codex e Sonnet com o código; Haiku com o mecânico que escapar dos scripts.

## 5. Segurança por construção (a régua 8 continua inteira)

Capacidades no braço; credenciais no perfil do operador, fora de qualquer árvore que as IAs leem ou que vá a público; Cloudflare e GitHub por token de escopo mínimo; SSH por chave; as IAs externas pedem ações, passam pelo portão de conteúdo e recebem recibos. Nenhuma mistura com a casa do Escritório (conferido pelo cético). O que o classificador bloqueou ontem foi a difusão de credencial; com o braço não há o que difundir, e a integração é total.

## 6. Ordem de execução proposta `[PROPOSTA — prazos são estimativa, não compromisso]`

0. **Dia 0 — medições** [cético]: `claude.exe` (caminho, `--help`, um `-p` mínimo, consumo do plano); se a fila tem como registrar um executor local (ler `web.py`/executores do orquestrador); um pedido real de publicação pelo braço. Nada de G2/G4 antes destas três medidas.
1. **Hoje** — G0 feito e com as superfícies novas. Pendurar na tarefa agendada do Windows; levar o quadro ao painel do app.
2. **1–2 dias** — G1: `custodia.py` parametrizado, validado contra v394→v395 e v395→v396.
3. **1 dia** — G3: o braço como executor local (site da TGL e repositórios primeiro; iald.ia.br quando o operador puser a credencial no perfil; Cloudflare por token).
4. **1 dia** — G2: vigia + `init`/`configure` + despacho direto ao `custodia.py`.
5. **2 dias** — G4: `gerencia.py` chamado pelo backend do app; Jev classificador; gates humanos no app; teto diário.

**Medida de sucesso do todo:** a v397 selada no Nós → sem nenhuma mensagem do operador à sessão, o quadro chega a «0 DEFASADO» no conjunto declarado de superfícies, restando só os `PENDENTE_OPERADOR` que a régua reserva.

## 7-A. A divisão do trabalho — AO LADO (23/10/2026, ordem do operador, verbatim em `work/php_e_v396_22out/OPERADOR_23out_divisao_do_trabalho_verbatim.txt`)

O operador corrigiu a v2 num ponto que vale para todos os gates: **nenhuma tarefa volta a ele como «pendente» se o stack pode fazê-la.**
A divisão é por natureza da tarefa: **navegação na internet** (painéis, Cloudflare, consoles, WebFTP) → ChatGPT no Codex, pela fila dele, com
o operador digitando as senhas nas telas de login; **design, estética e experiência interativa** (site, app, espaços públicos) → Kimi, por
handoff em arquivo, entregando fonte; **a subida** — pôr em funcionamento, ligar as peças no fim, medir — → Claude, sempre. Ao operador
ficam só os gates que a régua reserva e o que exige a sua senha ou a sua decisão. E a leitura por IA é o objetivo: nenhum bloqueio de
leitores de IA fica de pé. No desenho acima, isto redistribui a lista do §6: o «Dia 0» e o G3 ganham um braço humano-assistido imediato (o
Codex no navegador, com o operador no login) enquanto o braço por token não existe; e o G0/G4 ganham o desenho do Kimi (painel do quadro no
app, página pública do quadro).

**AO LADO do 7-A (23/10/2026, ~17:30, verbatim em `work/php_e_v396_22out/OPERADOR_23out_kimi_par_iald_tgl_verbatim.txt`):** o Kimi cuida também
do site da IALD «tal qual a TGL» — é o PAR IALD-TGL, sempre, interligado — e é o gestor da estratégia comercial da IALD e da TGL («pensar e
proteger»); o site da IALD entra nas mesmas regras de integração total. No desenho: a superfície «iald.ia.br» do quadro passa a ser do par, e o
Kimi ganha uma pasta própria de estratégia (duas vias de mão única).

## 7-B. A regra do gatilho — AO LADO (23/10/2026, ordem do operador, verbatim em `work/php_e_v396_22out/OPERADOR_23out_custodiar_quando_o_handoff_aparecer_verbatim.txt`)

«pode custodiar sempre que o handoff aparecer, como regra». O G2 deixa de ser proposta e vira regra da casa: a custódia começa sem pergunta
quando o Nós tem as três marcas da versão (selo com `um_version` novo e `um.py` batendo; bloco «vNNN SELADA» no diário; `HANDOFF_vNNN_CUSTODIA.md`,
com o `rodada_vNNN_stdout.txt`). Antes delas, EM OBRA: não se toca. Hoje o vigia é um laço na sessão da gerência; o G1 (a cadeia como programa)
é o que o torna uma tarefa agendada do Windows. Os gates do operador e os três portões dos textos públicos continuam valendo.

## 7. O que não prometo

Que o modelo entenda ordem ambígua sem perguntar (uma pergunta por decisão continua). Que o plano aguente gerência desassistida contínua sem teto e sem a regra dos tokens. Que as IAs externas fiquem «sem segredo» no sentido de ver credenciais — elas ficam sem PRECISAR delas. E que o quadro meça o que ainda não entrou nele: app iOS/Android, Jev, backup 3-2-1 — dito, não disfarçado.
