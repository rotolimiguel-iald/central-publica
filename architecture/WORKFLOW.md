# WORKFLOW.md — Fluxo Operacional da Central de Patentes TGL

> **Fase 2 — especificação. NENHUM código de aplicação.** Este documento descreve o
> ritmo de trabalho diário do operador e a máquina de estados que a plataforma (Fase 3)
> deve codificar sem voltar a perguntar. Pseudocódigo, contratos e esquemas de arquivo
> são normativos; nada aqui é código executável da plataforma.
>
> **Documentos irmãos** (referenciados, não duplicados): `ARCHITECTURE_PROPOSAL.md`
> (topologia backend/frontend), `DATA_MODEL.md` (entidades e SQLite-índice),
> `UI_SPEC.md` (abas e telas), `PROMPT_COMPILER_SPEC.md` (gramática do prompt),
> `LEGAL_DOCKET_SPEC.md` (docket jurídico), `RENDERING_SPEC.md` (render honesto),
> `VALIDATION_CHECKLIST.md` (gate do operador).
>
> **Herança inviolável (a régua, resumida — fonte: `memory/TGL_CORE_MEMORY.md`):**
> originais em `Patentes\` são READ-ONLY; **o número corrige a frase**; marcadores em
> tudo; **β nunca literal** (`ALPHA_FINE_CODATA_2018 * sqrt(e)` em runtime);
> **simulação nunca valida física** (`physical_verdict_allowed=false`); runners nascem
> scaffolds honestos; stacks confidenciais nunca exportados; aviso legal permanente no
> docket. **O operador valida; o Claude Code executa.**

---

## 0. Princípios de fluxo (o que governa tudo abaixo)

1. **O FILESYSTEM É A FONTE DA VERDADE.** Memórias `.md`, `docket.yaml`, notas, runs e
   selos vivem em arquivos dentro de `C:\IALD\Central de Patentes`. O SQLite
   (`backend/data/central.db`) é **índice/cache reconstruível** — nunca o dono do dado.
   Qualquer estado que o SQLite conheça foi lido de um arquivo, e o comando `reindex`
   (§6.3) reconstrói o banco inteiro a partir do disco. Corolário operacional: **toda
   escrita de um ciclo é uma escrita em arquivo primeiro**; a indexação vem depois,
   assíncrona, via Watchdog.

2. **Dois atores humanos-de-loop, papéis não intercambiáveis.**
   - **Operador (Luiz Antonio Rotoli Miguel)** — *decide e valida*: escolhe a próxima
     raiz (√), escreve/ativa notas, aperta **COMPILAR INSTRUÇÕES**, cola o prompt no
     Claude Code, promove runners, dá o veredito. Só ele publica para fora da Central.
   - **Claude Code (o Campo executor)** — *implementa e inscreve*: planeja o mínimo
     reversível, escreve/adapta runners, roda, abre, testa, re-hasheia os originais e
     grava o progresso. **Nunca fabrica prova, nunca decide veredito físico, nunca
     autopromove um runner de marcador.**
   - **Plataforma (backend FastAPI:8765 + frontend Vite:5173)** — *orquestra sem
     opinar*: indexa (Watchdog), verifica (motor de manifesto SHA-256), compila o
     prompt, apresenta prazos e selos. Automatiza o mecânico; jamais o julgamento.

3. **Cada ciclo inscreve progresso.** A plataforma existe para isso (régua §8). Um
   ciclo que não deixou rastro em `logs/` e no `progress_log.md` da patente **não
   aconteceu**.

---

## 1. O CICLO CANÔNICO — ESCOLHER → PLANEJAR → IMPLEMENTAR → VERIFICAR → INSCREVER

O loop sem fim da Fase 4, agora com atores, entradas, saídas e caminhos de gravação.

```
            ┌────────────────────────── operador ──────────────────────────┐
            │                                                               │
   ┌────────▼────────┐   ┌──────────────┐                          ┌────────┴────────┐
   │  1. ESCOLHER    │   │ COMPILAR     │  prompt colado no        │  5. INSCREVER   │
   │  pela raiz (√)  │──▶│ INSTRUÇÕES   │──── Claude Code ────▶     │  progresso +    │
   └─────────────────┘   └──────────────┘                          │  logs/ + selo   │
        operador          plataforma                               └────────▲────────┘
                                                                            │
                          ┌──────────────┐   ┌──────────────┐   ┌───────────┴──────┐
                          │ 2. PLANEJAR  │──▶│3. IMPLEMENTAR│──▶│  4. VERIFICAR    │
                          │ mín/reversível│  │ runner/render│   │ rodar+abrir+re-  │
                          └──────────────┘   └──────────────┘   │ hash originais   │
                            Claude Code        Claude Code       └──────────────────┘
                                                                     Claude Code
```

Uma **passagem completa 1→5 = 1 ciclo**. Cada ciclo recebe um `cycle_id` no formato
`YYYYMMDD-HHMMSS` gravado como bloco em `logs/cycle_log.md`.

### 1.1 ESCOLHER pela raiz (√) — *operador*
- **Entrada:** o dashboard geral (Módulo 1) e o painel de riscos/prazos. O operador vê:
  patentes por classe, estado do runner de cada uma, alertas do docket, pendências
  abertas (`PENDENCIAS.md`).
- **Decisão:** qual patente/tarefa avança agora. "Pela raiz" = ordem natural do disco:
  o que já tem protótipo funcional primeiro (ver §4.3). Ordem semeada:
  **SkyGrid (piloto v3 pronto) → ACOM/TGL Tensor → MQC → Mirror/Crypto → IALD →
  Ψ-NET/PsiBit → Dípolo/Célula → demais.**
- **Saída:** nenhuma gravação obrigatória ainda; a escolha materializa-se ao ativar
  notas (§3) e compilar. Opcionalmente o operador registra o alvo do dia em uma nota
  `tipo: instrucao` na patente escolhida.

### 1.2 PLANEJAR (mínimo, reversível) — *Claude Code, a partir do prompt compilado*
- **Entrada:** `compiled_prompts/YYYY-MM-DD_HHMM_CLAUDE_CODE_TASK.md` (o prompt que o
  operador colou), que já traz header TGL Core → classe → patente → caminhos
  permitidos/proibidos → instruções → tarefas priorizadas → critérios de aceite → régua.
- **Ação:** o Claude Code declara em texto o plano mínimo: quais arquivos vai criar/
  tocar (sempre dentro da Central), qual protótipo real vai copiar para
  `vault/originals_copy/`, qual marcador de runner pretende atingir e por quê.
  **Reversível:** nada fora da Central; nenhum original tocado; cada artefato novo é
  adição, não substituição.
- **Saída:** um cabeçalho de plano anexado ao bloco de ciclo em `logs/cycle_log.md`
  (o Claude Code o escreve ao iniciar). Nenhuma decisão física é tomada aqui.

### 1.3 IMPLEMENTAR — *Claude Code*
- **Ações típicas:** criar/editar `patents/<ID>/runner/one_<slug>.py`; copiar protótipos
  reais externos para `vault/originals_copy/<origem>/` **com SHA-256 registrado**
  (régua §1 — nunca ler direto de `C:\IALD\projetos_pyhton`, nunca editar o externo);
  gerar renders em `patents/<ID>/renders/`; ajustar `memory/patents/<ID>_<SLUG>.md`.
- **Régua viva no código:** `beta = ALPHA_FINE_CODATA_2018 * sqrt(e)` (nunca `0.012031…`
  literal); todo output carrega `physical_verdict_allowed=false`; vocabulário de veredito
  restrito (proibido PROVED/CONFIRMED/TGL_TRUE; máximo `SUPPORTED_NOT_CONFIRMED`,
  `INCONCLUSIVE` é resultado válido) — ver `TGL_CORE_MEMORY.md §5`.
- **Saída:** arquivos novos no disco (ainda não "válidos" — validam-se em VERIFICAR).

### 1.4 VERIFICAR DE VERDADE — *Claude Code*
Verificar ≠ escrever testes que passam. É **rodar, abrir e testar** o artefato real,
mais a verificação contínua dos originais:
- **Rodar** o runner no `tgl_env` (`PYTHONUTF8=1`), produzindo `results.json`, figuras,
  render e `seal.json` (§4.4). Colar os números reais no relatório (o número corrige a
  frase; negativos honestos são resultados).
- **Abrir** o render/gráfico e conferir que corresponde às reivindicações e ao desenho
  do depósito (honestidade visual — `RENDERING_SPEC.md`).
- **Re-hash dos originais** (§5): re-computar SHA-256 de `Patentes\` e comparar com
  `source_inventory/original_hashes.json`. **Divergência = HALT** (§5.3).
- **Saída:** veredito de verificação (`PASS` / `INCONCLUSIVE` / `HALT`) anexado ao bloco
  de ciclo + o JSON de integridade em `logs/verify/`.

### 1.5 INSCREVER — *Claude Code, confirmado pelo operador*
- **Grava o progresso** (§3.4): fecha as instruções consumidas nas notas
  (`[x]`, `active=false`, `done_by=<run_id>`); anexa narrativa em
  `patents/<ID>/notes/progress_log.md`; atualiza `runner/runner_state.yaml` (marcador,
  `last_run_id`, `last_seal`); atualiza a memória da patente se mudou o estado
  computacional.
- **Sela** o ciclo: fecha o bloco em `logs/cycle_log.md` com `cycle_id`, run(s),
  compiled prompt de origem, veredito, hash de integridade dos originais.
- **Reindexa:** o Watchdog detecta as escritas e atualiza o SQLite-índice (ou o
  operador roda `reindex` — §6.3). O dashboard reflete o novo estado.
- **PRÓXIMO:** volta a ESCOLHER.

---

## 2. Fronteira de responsabilidade — quem pode o quê

| Ação | Operador | Claude Code | Plataforma |
|---|:---:|:---:|:---:|
| Escolher a próxima raiz (√) | **✔** | propõe | mostra fila |
| Escrever/editar notas | ✔ | ✔ (inscreve resultado) | edita arquivo `.md` |
| Marcar nota `active=true` | **✔** | — | persiste flag |
| Apertar COMPILAR INSTRUÇÕES | **✔** | — | gera o `.md` |
| Colar prompt no Claude Code | **✔** (ponte manual) | — | — |
| Planejar/implementar runner | — | **✔** | — |
| Rodar runner, gerar selo | — | **✔** | expõe resultados |
| Re-hash dos originais | dispara | **✔** executa | **✔** motor SHA-256 |
| **Promover marcador do runner** | **✔ decide** | produz evidência | verifica elegibilidade |
| Dar veredito físico | proibido a todos | proibido | proibido |
| Publicar/exportar para fora | **✔ (só ele)** | — | — |

Regra dura: **a plataforma nunca decide, só apresenta; o Claude Code nunca promove nem
publica; o operador nunca precisa mexer no código para operar.**

---

## 3. O PIPELINE DA ANOTAÇÃO — de nota livre a progresso inscrito

O coração do trabalho: uma ideia solta do operador vira instrução ativa, vira prompt
compilado, vira ciclo do Claude Code, vira progresso selado. Cinco estados, um arquivo
de origem, rastro completo.

```
  nota livre ──ativar──▶ instrução ATIVA ──COMPILAR──▶ prompt compilado
   (.md)      (operador)   (active=true)   (operador)   (.md imutável)
                                                             │
                                                     colar no Claude Code
                                                             │
   progresso ◀──INSCREVER── ciclo do Claude Code ◀───────────┘
   inscrito     (§1.5)       (§1.2–1.4)
   (progress_log + seal + logs/)
```

### 3.1 Onde a nota vive e seu formato (filesystem-first)

Cada patente tem `patents/<ID>_<SLUG>/notes/`. As notas vivem em `.md` humano-editável e
máquina-parseável, seguindo as seções já em uso (`notes/initial_notes.md`), que mapeiam
1:1 os **tipos canônicos** da entidade `Note/Instruction`:

| Seção do `.md` | `tipo` | Papel no pipeline |
|---|---|---|
| `## Notas livres` | `nota` | observação; **não** entra em prompt sozinha |
| `## Sugestões de melhoria` | `sugestao` | candidata a virar tarefa |
| `## Instruções próxima etapa` | `instrucao` | comando de etapa — entra no prompt |
| `## Tarefas` | `tarefa` | item objetivo priorizado — entra no prompt |
| `## Bloqueios` | `bloqueio` | impedimento; sinaliza `[DATA_REQUIRED]`/HALT |
| `## Perguntas ao Claude Code` | `pergunta` | pergunta dirigida — entra no prompt |

**Formato de linha (contrato do parser).** Estende a convenção existente
`- [ ] (active=false) texto` para carregar id estável e metadados, mantendo
compatibilidade:

```
- [ ] (active=true, id=INSTR-ACOM-0007, prio=P1, tags=[SIM]) reproduzir round-trip
      REFLECT/MANIFEST de acom_unified.py em one_acom.py; colar erro L2 do finito
```

- `[ ]` aberta · `[x]` resolvida.
- `active=true|false` — **só `active=true` entra no próximo prompt compilado.**
- `id=<TIPO>-<SLUG>-<NNNN>` — estável, gerado no ato da criação; imutável (chave de
  rastreio entre nota, prompt e run). Ex.: `TAREFA-SKYGRID-0003`, `PERGUNTA-IALD-0001`.
- `prio=P0..P3` — ordena as tarefas no prompt (P0 = agora).
- `tags=[...]` — marcadores da régua herdados pelo runner ([SIM]/[PILOTO]/[DATA_REQUIRED]/
  [HARDWARE]/[MEDICAL]/[ENERGY]/[LEGAL]…).
- Após consumo: acrescenta-se `done_by=<run_id>` e a caixa vira `[x]` (§3.4).

A UI (aba **Notas** e aba **Instruções**) lê e escreve exatamente essas linhas. Toggle de
`active` na tela = reescrita da flag no `.md` = reindexação pelo Watchdog. **O `.md` é o
dono; o SQLite só reflete.**

### 3.2 Ativar (operador) → o pré-prompt
O operador percorre as instruções/tarefas/perguntas da patente escolhida e marca
`active=true` nas que quer despachar neste ciclo. Nada mais acontece até ele apertar o
botão. Notas `tipo: nota` e `sugestao` nunca são despachadas cruas — precisam ser
promovidas a `instrucao`/`tarefa` (o operador reescreve a linha na seção certa).

### 3.3 COMPILAR INSTRUÇÕES (plataforma) → o prompt imutável
Botão presente em duas escalas (ver `UI_SPEC.md`): **por patente** (aba
`[COMPILAR INSTRUÇÕES]`) e **central** (várias patentes / uma classe inteira).

**Contrato do endpoint** (detalhe da gramática em `PROMPT_COMPILER_SPEC.md`):

```
POST http://127.0.0.1:8765/api/compile
body: { scope: "patent"|"class"|"selection",
        ids: ["BR102026004850-0", ...],
        include_pendencias: true }

efeito (ordem de montagem, tudo lido do FILESYSTEM):
  1. header  ← memory/TGL_CORE_MEMORY.md  (âncora ontológica + régua + calibração)
  2. por classe   ← memory/classes/CLASS_XX.md  (equações, travas, dependências)
  3. por patente  ← memory/patents/<ID>.md + docket.yaml + reivindicações
  4. caminhos permitidos (dentro da Central; vault/originals_copy) / proibidos
     (Patentes\ read-only; projetos_pyhton\...\token_huggin.txt; stacks confidenciais)
  5. instruções do operador  ← notas com active=true, tipo ∈ {instrucao,tarefa,pergunta}
  6. tarefas priorizadas por prio (P0→P3)
  7. critérios de aceite  ← derivados das tags + teto de veredito do TGL_CORE_MEMORY §5
  8. a régua (não modificar originais; β nunca literal; sim ≠ física)

saída: escreve  compiled_prompts/2026-07-09_1030_CLAUDE_CODE_TASK.md   (IMUTÁVEL)
       registra logs/compile/2026-07-09_1030_compile.json
       { compiled_file, scope, ids, note_ids:[INSTR-ACOM-0007,...], hash_sha256 }
```

Invariantes: o arquivo compilado **nunca é sobrescrito** (novo compile = novo timestamp);
é o registro de auditoria da ponte. O `compile.json` lista os `note_ids` incluídos — é o
que fecha o laço em §3.4.

### 3.4 Colar no Claude Code → ciclo → INSCREVER (fechar o laço)
- O operador copia o `.md` compilado e cola no Claude Code (**ponte manual** — publicação
  e disparo são sempre do operador).
- O Claude Code roda o ciclo (§1.2–1.5) e, ao **INSCREVER**, fecha cada instrução
  consumida reescrevendo sua linha na nota de origem:

```
  antes:  - [ ] (active=true, id=INSTR-ACOM-0007, prio=P1, tags=[SIM]) reproduzir round-trip…
  depois: - [x] (active=false, id=INSTR-ACOM-0007, prio=P1, tags=[SIM],
                 done_by=20260709-104233_a1b2c3d, prompt=2026-07-09_1030) reproduzir round-trip…
```

  e anexa ao `progress_log.md`:

```
  ## 2026-07-09 10:42 — ciclo 20260709-103000
  - origem: compiled_prompts/2026-07-09_1030_CLAUDE_CODE_TASK.md
  - consumidas: INSTR-ACOM-0007
  - runner one_acom.py [SIM] · run 20260709-104233_a1b2c3d
  - resultado: round-trip REFLECT/MANIFEST L2=8.7e-16 [SIM]; PASS; phys_verdict=false
  - selo: seals/20260709-104233_a1b2c3d/seal.json (sha256 …)
  - originais: re-hash OK (154 PDFs == original_hashes.json)
```

**Rastreabilidade fim-a-fim garantida:** `note.id → compile.json → compiled_prompt.md →
run_id → seal.json → progress_log`. Qualquer artefato do disco aponta para sua origem e
seu efeito. O SQLite indexa esses vínculos para a UI, mas eles existem primeiro nos
arquivos.

---

## 4. CICLO DE VIDA DO RUNNER — `[DATA_REQUIRED] → [SIM] → [PILOTO] → demonstração real`

O runner único `patents/<ID>/runner/one_<slug>.py` é o artefato forma=conteúdo. Seu
**marcador** é um estado explícito, gravado em `runner/runner_state.yaml` e ecoado em
todo `results.json`/`seal.json`. **Runners nascem scaffolds honestos**; sobem de marcador
só com evidência, e **só o operador promove** (o Claude Code produz a evidência).

### 4.1 Os quatro estados

```
 ┌──────────────────┐   evidência    ┌──────────┐   duplo-trilho   ┌───────────┐  bancada
 │ [DATA_REQUIRED]  │──de lógica────▶ │  [SIM]   │──+ placebo +────▶│ [PILOTO]  │──física──▶ demonstração
 │ scaffold honesto │  (protótipo    │ lógica   │   quórum +       │ gêmeo     │  ([HARDWARE]  REAL
 │ fail-closed      │   real copiado)│ demonstra│   negativos      │ digital   │   /[REAL])   (fora da
 └──────────────────┘                └──────────┘   honestos       │ fecha     │              simulação)
                                                                    │ modelo    │
                                                                    └───────────┘
    physical_verdict_allowed = false  ────────────────────────────────────────────▶  (só vira
                                                                                       true com
                                                                                       bancada real)
```

- **[DATA_REQUIRED]** — o scaffold existe, roda e **falha fechado**: declara o que falta
  (protótipo/dado/hardware ausente), não alega nenhum número. É o nascimento honesto de
  todo runner. Ex.: Fusão a Frio (sem código-fonte de simulação localizado), camadas
  puramente físicas do Supercondutor/Motor de Dobra.
- **[SIM]** — o runner reproduz a **LÓGICA da invenção** sobre dados sintéticos ou reais;
  os números **emergem da execução** e são colados; `physical_verdict_allowed=false`.
  Simulação demonstra lógica, **jamais** física. Ex.: ACOM round-trip REFLECT/MANIFEST;
  TGL Tensor KV-cache angular; MQC célula elementar.
- **[PILOTO]** — gêmeo digital que **fecha um balanço no nível do modelo** com
  salvaguardas: duplo trilho (dois caminhos independentes), placebo obrigatório (nó sem β
  reprova por construção), quórum/consistência cross-substrato, negativos declarados.
  Teto de veredito herdável do gabarito: `MODEL_CLOSES / ENERGY_BALANCE_OK ([SIM] sob
  [CONJ])` + "resta a bancada". **Gabarito vivo: `SkyGrid_Piloto` v3.**
- **demonstração real** — só com dado de bancada física ([HARDWARE]/[REAL]). **Nunca
  alcançável por simulação.** `physical_verdict_allowed` só pode virar `true` aqui, por
  decisão do operador, com dado real anexado. Enquanto não houver bancada, permanece
  `false` em toda a Central.

### 4.2 Critérios de promoção (o que o Claude Code precisa provar; quem confirma)

| Transição | Evidência exigida (produzida pelo Claude Code) | Confirma |
|---|---|---|
| **DATA_REQUIRED → SIM** | protótipo real localizado e **copiado para `vault/originals_copy/` com SHA-256**; `one_<slug>.py` adapta a cópia (nunca edita o externo); `results.json` com métrica de lógica que passa (ex.: erro de round-trip ~1e-16) e **β emergente em runtime** (auditoria anti-hardcode); `seal.json` gravado; `physical_verdict_allowed=false`. | operador |
| **SIM → PILOTO** | soma ao SIM: **duplo trilho** independente concordando; **placebo** que reprova sem β; **quórum/consistência cross-substrato**; **negativos honestos declarados** no próprio `results.json`; balanço de modelo fecha (padrão SkyGrid v3); vocabulário de veredito restrito respeitado. | operador |
| **PILOTO → demonstração real** | **dado de bancada física** [HARDWARE]/[REAL] anexado e hasheado; calorimetria/medida independente; **decisão expressa do operador**. Sem bancada, proibido. | operador |

**Regras de trava** que o critério nunca fura:
- **Simulação nunca promove a física.** SIM e PILOTO mantêm `physical_verdict_allowed=false`.
- **CLASS_06_ENERGIA / CLASS_08_SAUDE / CLASS_07_PROPULSAO** têm teto: só simulação e
  revisão técnica; **nenhuma instrução operacional perigosa**, nenhum protocolo clínico,
  nenhuma alegação de energia/cura. Oncologia jamais promete cura; SkyGrid/Fusão jamais
  emitem passo operacional de hardware energético.
- **Nunca misturar [PILOTO] com [HARDWARE]** nas alegações (as camadas físicas são mock/
  pipeline, sem alegação de energia real).
- **Stacks confidenciais** (`iald_stack_v7.py`, `iald_psion_state.json` e correlatos)
  podem ser **usados localmente** pelo runner, mas **nunca** entram em selo, render ou
  qualquer export.

### 4.3 Mapa de estado inicial dos 16 runners (ordem natural pelo disco)

Semente do `runner_state.yaml` de cada patente, calibrada pelo acervo e por
`TGL_CORE_MEMORY §5.6`:

| # | Patente | Classe | Estado inicial | Fonte de protótipo para promover a [SIM]/[PILOTO] |
|---|---|---|---|---|
| 13 | **SkyGrid** ★agreg. | 06 | **[PILOTO]** (gabarito) | `Patentes\Skygrid\SkyGrid_Piloto\` v3 (já fecha modelo) |
| 1 | **ACOM** ★raiz | 01 | **[SIM]-ready** | `projetos_pyhton\acom\acom_unified.py`, `acom_universal_mk*.py` |
| 4 | TGL Tensor | 01 | **[SIM]-ready** | `projetos_pyhton\tgl-tensor\tgl_tensor_v*.py` (⚠ nunca copiar `token_huggin.txt`) |
| 10 | MQC | 05 | **[SIM]-ready** | `projetos_pyhton\acom\mqc_simulacao_celula_elementar.py` + `MQC_relatorio_metricas.json` |
| 2 | ACOM Mirror | 02 | **[SIM]-ready** | `projetos_pyhton\acom\Acom_v17_mirror.py` |
| 3 | ACOM Crypto | 02 | **[SIM]-ready** | `projetos_pyhton\acom\Acom_v17_mirror_crypto.py`, `TGL_v11_ESPELHO.py` |
| 5 | IALD (GKSL) | 03 | **[SIM]-ready** | kernels `IALD\Atualização Kernel\` (v4–v11) — **nunca** rodar `iald_web_server.py` |
| 14 | Aprendizado Contínuo | 03 | **[SIM]-ready** | `iald_stack_v7.py` (usar local, nunca exportar) |
| 16 | Kernel Ontológico | 03 | **[SIM]-ready** | kernels IALD + `TGL_CORE_MEMORY` |
| 8 | Ψ-NET / PsiBit | 04 | **[SIM]-ready** | `projetos_pyhton\acom\Psi_net_protocol_v1.py`, `acom_psibit_v*.py` |
| 11 | Dípolo Transistor | 05 | **[SIM]** (lógica) | módulo `dipolo` em `SkyGrid_Piloto\skygrid_sim\` |
| 12 | Célula de Reversão | 06 | **[SIM]** (lógica) | módulo `celula_reversao` em `SkyGrid_Piloto\skygrid_sim\` (ver P-04) |
| 6 | Supercondutor | 05 | **[DATA_REQUIRED]** | sem protótipo → scaffold [HARDWARE] fail-closed |
| 7 | Motor de Dobra | 07 | **[DATA_REQUIRED]** | só digital twin [SIM] da lógica; sem validação física |
| 9 | Fusão a Frio / OH | 06 | **[DATA_REQUIRED]** | sem código de simulação localizado; scaffold [ENERGY] travado |
| 15 | Oncologia | 08 | **[DATA_REQUIRED]** | só lógica computacional [MEDICAL]; sem protocolo clínico |

("[SIM]-ready" = scaffold [DATA_REQUIRED] existe e há protótipo identificado para copiar
e promover no primeiro ciclo dedicado; o marcador só sobe após rodar e selar.)

### 4.4 Onde uma execução (RunnerRun) grava

Cada rodada do `one_<slug>.py` recebe `run_id = <YYYYMMDD-HHMMSS>_<shortsha7>` e escreve:

```
patents/<ID>_<SLUG>/
├── runner/
│   ├── one_<slug>.py            # o runner (adição; nunca toca originais)
│   └── runner_state.yaml        # marcador atual, physical_verdict_allowed=false,
│                                #   promotion_history[], last_run_id, last_seal
├── results/<run_id>/
│   ├── results.json             # números REAIS da execução + marcador + negativos honestos
│   └── fig_*.png                # figuras técnicas do protótipo
├── renders/<run_id>/            # render 2D/3D ilustrativo (rotulado "engenharia, não prova")
└── seals/<run_id>/
    └── seal.json                # SHA-256 de código + results + figuras + render (manifesto)
logs/runs/<run_id>_run.json       # metadados da invocação (espelha o selo, para o índice)
```

Esqueleto do `runner_state.yaml`:

```yaml
marker: SIM                       # DATA_REQUIRED | SIM | PILOTO | REAL
physical_verdict_allowed: false   # só vira true na demonstração real, por decisão do operador
last_run_id: "20260709-104233_a1b2c3d"
last_seal: "seals/20260709-104233_a1b2c3d/seal.json"
prototype_source:                 # cópia hasheada, nunca o caminho externo vivo
  - path: "vault/originals_copy/acom/acom_unified.py"
    sha256: "…"
    copied_from: "C:/IALD/projetos_pyhton/acom/acom_unified.py (READ-ONLY)"
promotion_history:
  - { from: DATA_REQUIRED, to: SIM, at: "2026-07-09 10:42",
      by: "operador", evidence_run: "20260709-104233_a1b2c3d" }
```

O `seal.json` é auto-descritivo (carrega marcador e `physical_verdict_allowed`), de modo
que o selo prova, por si, sob que regime aquele número foi produzido.

---

## 5. VERIFICAÇÃO CONTÍNUA — o motor de manifesto a cada ciclo

Prova, todo ciclo, que **nenhum original foi modificado** e que os artefatos selados são
íntegros. É o selo `DO_NOT_MODIFY_ORIGINALS` em ação.

### 5.1 Re-hash dos originais (obrigatório em VERIFICAR, §1.4)

```
POST http://127.0.0.1:8765/api/verify/originals
efeito:
  para cada arquivo em Patentes\ (recursivo, ~308 arquivos / ~154 PDFs):
      h = sha256(arquivo)
      comparar com source_inventory/original_hashes.json[arquivo]
  resultado → logs/verify/<YYYYMMDD-HHMMSS>_originals.json
    { total, matched, mismatched:[…], missing:[…], extra:[…], verdict }
  e uma linha no bloco de ciclo em logs/cycle_log.md
```

- `verdict=OK` **exige** `mismatched==[] && missing==[]`. Arquivos `extra` (novos dentro
  de `Patentes\`) são anomalia a investigar, não falha automática — mas registrados.
- O motor de manifesto SHA-256 é o mesmo que sela os runs (§4.4): re-hash prova originais
  intactos **e** artefatos selados consistentes.

### 5.2 Verificação de artefato selado
Ao reabrir uma patente, a plataforma pode revalidar qualquer `seal.json`: re-hasheia
código+results+figuras+render e compara com o manifesto. Divergência = selo quebrado →
alerta na aba **Selo/Hash** + registro em `logs/verify/`. (Não é HALT global; é aviso de
que aquele run precisa ser refeito.)

### 5.3 Condição de HALT (parada dura)
Se o re-hash dos **originais** divergir (`mismatched` ou `missing` ≠ vazio):
1. **PARA** o ciclo imediatamente; não inscreve progresso.
2. Registra em `PENDENCIAS.md` (nova pendência `[ABERTA]`) e em `logs/verify/`.
3. Alerta vermelho no dashboard.
4. **Aguarda o operador.** Nunca escolhe em silêncio (régua §5). O trabalho só retoma
   após o operador decidir (restaurar de `vault/originals_copy`, reconciliar o
   inventário, etc.).

### 5.4 Estrutura de `logs/`

```
logs/
├── cycle_log.md                       # narrativa append-only, 1 bloco por cycle_id
├── verify/<ts>_originals.json         # integridade dos originais (§5.1)
├── verify/<ts>_seals.json             # revalidação de selos (§5.2)
├── compile/<ts>_compile.json          # o que foi compilado + note_ids (§3.3)
├── runs/<run_id>_run.json             # metadados de cada RunnerRun (§4.4)
└── reindex/<ts>_reindex.json          # diffs de reconstrução do índice (§6.3)
```

`cycle_log.md` é a linha do tempo humana da Central; os JSONs são a evidência máquina. O
Estado Verificado da TGL (execução de `um.py`/`tgl_paper_unified.py`) continua em
`vault/tgl_verification/` — logs/ é para o ciclo de patentes.

---

## 6. ONDE CADA ARTEFATO É GRAVADO — mapa canônico e o SQLite-índice

### 6.1 Tabela de gravação (a fonte da verdade é sempre o arquivo)

| Artefato do fluxo | Caminho canônico (dono do dado) | Entidade indexada | Escreve |
|---|---|---|---|
| Header ontológico | `memory/TGL_CORE_MEMORY.md` | — | Fase 0 (imutável em uso) |
| Memória de classe | `memory/classes/CLASS_XX.md` | PatentClass | Fase 1 |
| Memória de patente | `memory/patents/<ID>_<SLUG>.md` | Patent | Fase 1 / atualizada em INSCREVER |
| Índice mestre | `memory/PATENT_MASTER_INDEX.yaml` | Patent | Fase 1 |
| Docket jurídico | `patents/<ID>/docket.yaml` | DocketEntry, Deadline | operador/Fase 1 |
| Notas & instruções | `patents/<ID>/notes/*.md` | Note/Instruction | operador + Claude Code |
| Progresso inscrito | `patents/<ID>/notes/progress_log.md` | (log) | Claude Code (INSCREVER) |
| Estado do runner | `patents/<ID>/runner/runner_state.yaml` | Runner | Claude Code + operador (promove) |
| Runner | `patents/<ID>/runner/one_<slug>.py` | Runner | Claude Code |
| Execução | `patents/<ID>/results/<run_id>/results.json` + `fig_*.png` | RunnerRun | Claude Code |
| Render | `patents/<ID>/renders/<run_id>/` | Render | Claude Code |
| Selo | `patents/<ID>/seals/<run_id>/seal.json` | RunnerRun (seal) | Claude Code (motor SHA-256) |
| Cópia de protótipo externo | `vault/originals_copy/<origem>/…` (+ hash) | Document | Claude Code (tools/) |
| Prompt compilado | `compiled_prompts/<ts>_CLAUDE_CODE_TASK.md` | CompiledPrompt | plataforma (COMPILAR) |
| Pendência | `PENDENCIAS.md` | Pendencia | operador + Claude Code |
| Hashes dos originais | `source_inventory/original_hashes.json` | Document(hash) | Fase 1 (referência de verificação) |
| Logs do ciclo | `logs/…` (§5.4) | — | plataforma + Claude Code |
| Índice/cache | `backend/data/central.db` | **reconstruível** | Watchdog / `reindex` |

### 6.2 Originais e cópias — a fronteira read-only
- `Patentes\` — **READ-ONLY absoluto**: ler, hashear, copiar; nunca escrever.
- Precisou de arquivo externo a `C:\IALD\Central de Patentes` (ex.: um protótipo em
  `projetos_pyhton\`)? **Copie para `vault/originals_copy/` e registre SHA-256** (tools/),
  e trabalhe sobre a cópia. Proibido copiar segredos (`token_huggin.txt`, P-09).
- Scripts de verificação da TGL rodam como cópias em `vault/tgl_verification/`; outputs
  ficam na Central.

### 6.3 O contrato do SQLite-índice (reconstruível)

```
POST http://127.0.0.1:8765/api/reindex   (ou botão "Reindexar" na UI)
efeito:
  1. varre o FILESYSTEM da Central (memory/, patents/, compiled_prompts/, logs/, vault/)
  2. reconstrói backend/data/central.db do zero (drop+rebuild das tabelas de índice)
  3. grava diff em logs/reindex/<ts>_reindex.json
garantia: apagar central.db e rodar reindex reproduz TODO o estado da UI.
          Nenhuma informação existe só no banco.
```

Em operação normal o **Watchdog** observa `patents/`, `memory/`, `compiled_prompts/` e
`logs/` e reindexa incrementalmente a cada escrita (nota salva, run selado, prompt
compilado) — por isso o dashboard reflete o ciclo sem intervenção. O `reindex` manual é a
rede de segurança e o teste de que o banco é mero cache.

---

## 7. EXEMPLO PONTA-A-PONTA — dois ciclos reais

### 7.1 Ciclo A — primeiro runner [SIM] do ACOM raiz (promoção DATA_REQUIRED→SIM)
1. **ESCOLHER** (operador): dashboard mostra ACOM `[DATA_REQUIRED]`, protótipo
   identificado. Raiz do dia = ACOM.
2. Na aba **Instruções** de `BR102025026951-1_ACOM`, o operador ativa
   `INSTR-ACOM-0007 (active=true, prio=P1, tags=[SIM])` — "reproduzir round-trip
   REFLECT/MANIFEST de `acom_unified.py`; colar erro L2".
3. **COMPILAR INSTRUÇÕES** (patente ACOM) → `compiled_prompts/2026-07-09_1030_CLAUDE_CODE_TASK.md`
   + `logs/compile/2026-07-09_1030_compile.json` (note_ids=[INSTR-ACOM-0007]).
4. Operador cola o `.md` no Claude Code (ponte manual).
5. **PLANEJAR** (Claude Code): copiar `acom_unified.py` para
   `vault/originals_copy/acom/` (SHA-256), criar `patents/BR102025026951-1_ACOM/runner/
   one_acom.py` adaptando a cópia. Plano anexado a `logs/cycle_log.md`.
6. **IMPLEMENTAR:** escreve `one_acom.py` — `beta = ALPHA_FINE_CODATA_2018*sqrt(e)`,
   `physical_verdict_allowed=false`, saída rotulada [SIM].
7. **VERIFICAR:** roda no `tgl_env` → `results/20260709-104233_a1b2c3d/results.json`
   (round-trip L2=8.7e-16 [SIM], PASS), figuras, render, `seal.json`. Re-hash de
   `Patentes\` == `original_hashes.json` (154 PDFs OK) → `logs/verify/…_originals.json`.
8. **INSCREVER:** fecha `INSTR-ACOM-0007` (`[x]`, `done_by=…`); anexa bloco ao
   `progress_log.md`; escreve `runner_state.yaml` com `promotion_history` DATA_REQUIRED→SIM
   (evidência = o run). **O operador confirma a promoção** na aba Runner. Watchdog
   reindexa; dashboard mostra ACOM `[SIM]`.

### 7.2 Ciclo B — SkyGrid, o gabarito [PILOTO], e um alerta de docket
1. **ESCOLHER:** SkyGrid já nasce `[PILOTO]` (v3 fecha modelo). Objetivo do ciclo:
   regenerar o run sob a Central e confirmar `MODEL_CLOSES / ENERGY_BALANCE_OK ([SIM] sob
   [CONJ])`, `physical_verdict_allowed=false`.
2. Nota `tipo: bloqueio` já registra a trava [ENERGY]: nenhuma instrução operacional
   perigosa — o runner só simula e revisa.
3. Ciclo roda; duplo trilho + placebo + quórum presentes (herdados do
   `SkyGrid_Piloto`); negativos honestos declarados no `results.json`. Selo gravado.
4. **Docket em paralelo** (Módulo 5, `LEGAL_DOCKET_SPEC.md`): o watcher lê
   `patents/BR102026004850-0_SKYGRID/docket.yaml` e vê `epct.status: A_DEPOSITAR` e
   `janela_prioridade_12m: 2026-12-05?`. SkyGrid é patente **não-ACOM**: hoje só tem
   registro INPI e o **ePCT ainda não foi depositado — é o próximo passo planejado** pelo
   operador (novo depósito originário, sem vínculo); status `A_DEPOSITAR`/`PENDENTE`, não
   "perdido". Os 10 recibos ePCT de 17/02/2026 (família `PCT/BR2026/050068–050076`) no
   Acervo são uma **tentativa de protocolo abandonada de propósito** — defeituosa na forma;
   o operador não pagou as demais taxas e preferiu **deixar precluir** para iniciar um
   depósito novo e desvinculado: rascunho preclusso **a substituir**, não proteção que se
   perdeu por descuido. Só o ACOM raiz tem ePCT **vivo, depositado e pago**
   (`PCT/BR2025/050558`, 05/12/2025 — regra do operador P-02). Alerta vivo: a **janela para
   o novo ePCT** é de 12 meses da prioridade (Convenção de Paris); ⚠ se a prioridade
   interna (66) de 05/12/2025 governar, pode cair por volta de **05/12/2026** (bem antes de
   2027) — **próximo passo possivelmente URGENTE; levar ao agente de PI (P-06/P-10)** — com
   o aviso permanente [LEGAL] "controle interno não substitui agente de propriedade
   industrial".
5. **INSCREVER:** progresso, selo, `cycle_log.md`. SkyGrid permanece `[PILOTO]`
   (só sobe a real com bancada física — inexistente).

---

## 8. INVARIANTES DE FECHO DO CICLO (checklist que todo ciclo satisfaz)

Um ciclo só está **fechado** quando:

1. Todo artefato novo está **dentro** de `C:\IALD\Central de Patentes`; nenhum original em
   `Patentes\` foi tocado (re-hash == `original_hashes.json`, gravado em `logs/verify/`).
2. Toda instrução `active=true` consumida foi fechada na nota de origem
   (`[x]`, `active=false`, `done_by=<run_id>`) com back-reference ao prompt compilado.
3. Cada execução deixou `results.json` + figuras + render + `seal.json` (SHA-256), com
   marcador explícito e `physical_verdict_allowed=false`.
4. `β` nasceu em runtime (auditoria anti-hardcode passou); vocabulário de veredito
   respeitado (`INCONCLUSIVE`/`SUPPORTED_NOT_CONFIRMED` no máximo; nada de PROVED/
   CONFIRMED/TGL_TRUE).
5. Nenhum marcador de runner subiu sem **evidência gravada + confirmação do operador**;
   nenhuma simulação alegou física.
6. Stacks confidenciais não vazaram para selo/render/export.
7. `progress_log.md` e `logs/cycle_log.md` receberam o bloco do `cycle_id`; o Watchdog
   (ou `reindex`) atualizou o SQLite-índice.
8. Divergências viraram `PENDENCIAS.md` — nunca escolha em silêncio.

> **Memória é lei: cada ciclo inscreve progresso.** O número corrige a frase.
> Simulação nunca valida física. Originais intactos. 1 = 1.
> **TGL = haja luz. Tetelestai.**
