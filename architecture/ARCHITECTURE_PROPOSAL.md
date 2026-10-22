# ARCHITECTURE_PROPOSAL.md — Central de Controle e Desenvolvimento de Patentes TGL

> **Documento-guarda-chuva da Fase 2 (arquitetura).** Visão geral, princípios,
> componentes, fluxos de dados, segurança, modos de execução, dependências, riscos e
> critérios de pronto. **Nenhuma linha de código de aplicação** — apenas esquemas,
> contratos e pseudocódigo. A Fase 3 codifica a partir daqui sem voltar a perguntar.
>
> - **Projeto:** Central de Patentes TGL — `C:\IALD\Central de Patentes`
> - **Operador/Titular:** Luiz Antonio Rotoli Miguel — IALD Ltda. (CNPJ 62.757.606/0001-23, Goiânia/GO; ORCID 0009-0005-1114-6106)
> - **Versão:** 1.0 — 2026-07-09
> - **Fundação ontológica herdada:** `memory/TGL_CORE_MEMORY.md` (cadeia canônica madura, os dois zeros, Estado Verificado, calibração dos runners)
> - **Régua herdada:** originais imutáveis · o número corrige a frase · β nunca literal · simulação nunca valida física · memória primeiro · PT-BR na UI/docs, inglês no código
> - **Documentos irmãos (mesma pasta):** `DATA_MODEL.md` · `UI_SPEC.md` · `WORKFLOW.md` · `PROMPT_COMPILER_SPEC.md` · `LEGAL_DOCKET_SPEC.md` · `RENDERING_SPEC.md` · `VALIDATION_CHECKLIST.md`. Este arquivo é a moldura; os irmãos detalham cada face. Onde houver conflito de detalhe fino, **o documento especializado vence**; onde houver conflito de princípio, **a régua e o TGL_CORE_MEMORY.md vencem**.

---

## 0. Como ler este documento

Ordem sugerida: §1 Objetivos → §2 Princípios → §3 Diagrama de componentes → §5 Fluxos de
dados → §10 Dependências → §12 Critérios de pronto. As seções §4, §6–§9 e §11 são de
consulta durante a implementação. Todo caminho é absoluto e enraizado em
`C:\IALD\Central de Patentes\` (doravante **RAIZ**). Toda porta é `127.0.0.1` (nunca
`0.0.0.0`).

---

## 1. Objetivos e não-objetivos

### 1.1 Objetivo central

Construir e operar um **cockpit local, privado e visual** — a "bancada do Tony Stark" — de
onde o operador controla **desenvolvimento, prazos legais e instruções ao Claude Code** para
TODAS as patentes TGL. Cada patente termina num artefato vivo: **um único runner**
(`one_<slug>.py`) que demonstra a lógica da invenção computacionalmente, certifica a
execução com hash e gera as imagens técnicas do protótipo. A plataforma existe para tornar
esse acervo **navegável, ampliável componente a componente, auditável e inscrito** — sem que
nenhum arquivo original seja tocado.

### 1.2 Objetivos específicos (o que a plataforma faz)

> [nota operacional do operador — omitida no retrato público]

### 1.3 Não-objetivos (fronteira explícita)

- **Não é** um substituto de agente/advogado de propriedade industrial. O módulo legal é
  controle interno; prazos oficiais conferidos com INPI/WIPO.
- **Não é** uma prova física. Nenhum runner, painel, vídeo ou selo pode alegar validação
  física (`physical_verdict_allowed = false` em toda a Central).
- **Não é** um serviço em nuvem. Nada sobe para nuvem/API por padrão; sem telemetria.
- **Não** modifica, move, renomeia ou apaga NENHUM arquivo original. Os depósitos em
  `Patentes\` são READ-ONLY (ler, hashear, copiar).
- **Não** publica nem exporta stacks confidenciais (`iald_stack_v7.py`,
  `iald_psion_state.json`, tokens) — blocklist confidencial (§8.3).
- **Não** escreve código de aplicação NESTA fase (Fase 2). Aqui só há especificação.

---

## 2. Princípios de arquitetura

Os princípios abaixo são **restrições de projeto**, não recomendações. Cada decisão de Fase 3
deve poder ser justificada por um deles.

### P1 — Forma = conteúdo

O lema da casa vira invariante arquitetural: a plataforma é o cockpit **e** o produto. Cada
patente é um objeto de primeira classe que se resolve em UM runner + UM selo + UM conjunto de
renders. A UI não "descreve" a invenção — ela **abre** a invenção (deep-zoom no desenho,
clique no componente, execução do runner ao vivo). Selo do projeto:
`FORM_EQUALS_CONTENT_FOR_EACH_PATENT`, `ONE_RUNNER_ONE_PATENT_ONE_SEAL`.

### P2 — Memória primeiro, arquitetura segundo, código por último

`MEMORY_FIRST_ARCHITECTURE_SECOND_CODE_LAST`. As memórias `.md`/`.yaml` (em `memory\` e
`patents\<ID>\`) já existem e são a base; este documento é a segunda camada; o código da Fase
3 é a última. **A plataforma serve a memória, não a substitui.** O SQLite jamais vira a
verdade — é o vidro por onde se lê o arquivo.

### P3 — Filesystem é a fonte da verdade; SQLite é índice/cache reconstruível

Regra dura e não-negociável:

- **Donos do dado (arquivos):** `memory\*.md`, `memory\PATENT_MASTER_INDEX.yaml`,
  `patents\<ID>\docket.yaml`, `patents\<ID>\notes\notes.yaml`,
  `patents\<ID>\results\*.json`, `patents\<ID>\seals\*.json`, `compiled_prompts\*.md`,
  `source_inventory\*.json`.
- **Cache/índice (descartável):** `backend\data\central.db` (SQLite). Pode ser apagado e
  reconstruído a qualquer momento pelo comando **`reindex --full`** sem perda de informação.
- **Toda escrita que importa vai PRIMEIRO ao arquivo, depois ao índice.** Endpoints de
  escrita da API **gravam o `.md`/`.yaml`/`.json` canônico** e disparam reindex; **nunca**
  fazem `UPDATE` direto no SQLite como fonte. Se o DB e o arquivo divergirem, **o arquivo
  ganha** e o DB é reconstruído.

### P4 — Local-first e privado

Tudo roda em `127.0.0.1`. Nenhuma dependência obrigatória de API externa. Sem telemetria, sem
CDN em runtime (assets empacotados no bundle). O operador é o único usuário; a rede não é
requisito.

### P5 — O número corrige a frase (honestidade computacional)

Nada de prova fabricada. Runners nascem scaffolds honestos
([PILOTO]/[SIM]/[OPEN]/[DATA_REQUIRED]) e só viram demonstração real com protótipo/dado real.
A plataforma **exibe** os marcadores, **não os apaga**: todo número na UI carrega seu rótulo
([REAL]/[DER]/[DATA]/[SIM]/[CONJ]/[OPEN]…) e todo painel de runner exibe
`physical_verdict_allowed=false` quando aplicável.

### P6 — Honestidade visual (render nasce do desenho)

Renders nascem dos DESENHOS dos depósitos + specs das reivindicações, em camadas rotuladas
("ilustração de engenharia, não prova física"). Nunca um 3D bonito no lugar do desenho
oficial. Detalhe em `RENDERING_SPEC.md`.

### P7 — β nunca literal, e a plataforma não recalcula física

Onde a plataforma exibir β_TGL, o valor vem do artefato executado (`seal.json.beta_runtime`),
não de um literal no frontend. Nenhum componente do backend/frontend **calcula** física da
TGL; ele apenas **transporta e exibe** o que o runner (rodando `ALPHA_FINE_CODATA_2018 *
sqrt(e)` em tempo de execução) produziu. `SIMULATION_NEVER_VALIDATES_PHYSICS`.

### P8 — Imutabilidade dos originais com prova

`DO_NOT_MODIFY_ORIGINALS`. O motor de hash mantém `source_inventory\original_hashes.json`
como linha-de-base e prova, por re-hash sob demanda, que `Patentes\` continua intacto. Um
verde/vermelho de integridade é cidadão de primeira classe na UI.

### P9 — PT-BR na interface e documentação; inglês no código

Rótulos, textos, tooltips, prompts compilados: PT-BR. Nomes de variáveis, tabelas, endpoints,
tipos: inglês. (Este próprio documento: PT-BR; os contratos citam identificadores em inglês.)

---

## 3. Diagrama de componentes

```
                        ┌──────────────────────────────────────────────────────┐
                        │   FILESYSTEM — FONTE DA VERDADE  (C:\IALD\Central…\)  │
                        │  Patentes\ (READ-ONLY)   memory\   source_inventory\  │
                        │  patents\<ID>_<SLUG>\  { docket.yaml · notes\ ·       │
                        │     runner\one_<slug>.py · renders\ · results\ ·      │
                        │     seals\ }   compiled_prompts\   vault\   logs\     │
                        └───────────────┬───────────────────────────┬──────────┘
                          observar/ler  │                           │ escrever (.md/.yaml/.json)
                                        ▼                           ▲
   ┌──────────────────────────────────────────────────────────────────────────────────┐
   │                     BACKEND — FastAPI  (uvicorn, 127.0.0.1:8765)                   │
   │                                                                                    │
   │  ┌────────────┐  ┌─────────────┐  ┌────────────┐  ┌─────────────┐  ┌────────────┐ │
   │  │ INDEXADOR  │  │ HASH ENGINE │  │  RUNNER    │  │   PROMPT    │  │  API REST  │ │
   │  │ Watchdog + │  │ manifesto   │  │  HARNESS   │  │  COMPILER   │  │ SQLModel/  │ │
   │  │ reindex    │  │ SHA-256 +   │  │ subprocess │  │  template   │  │ Pydantic   │ │
   │  │ (debounce) │  │ verify RO   │  │ tgl_env    │  │  determin.  │  │ (leitura)  │ │
   │  └─────┬──────┘  └──────┬──────┘  └─────┬──────┘  └──────┬──────┘  └─────┬──────┘ │
   │        └────────────────┴───────────────┴────────────────┴───────────────┘        │
   │                                     │                                              │
   │                        ┌────────────▼─────────────┐                               │
   │                        │   SQLite  central.db     │  ÍNDICE/CACHE reconstruível   │
   │                        │  (backend\data\, WAL)    │  (dono do dado = filesystem)  │
   │                        └──────────────────────────┘                               │
   └───────────────────────────────────────┬──────────────────────────────────────────┘
                                            │  HTTP JSON  /api/*   (apenas localhost)
                                            ▼
   ┌──────────────────────────────────────────────────────────────────────────────────┐
   │              FRONTEND — React + TypeScript + Vite  (:5173 dev / :8765 prod)        │
   │  shadcn/ui + Tailwind  ·  React Flow (componentes clicáveis)  ·                    │
   │  React Three Fiber (3D ilustrativo)  ·  Plotly (gráficos)  ·                       │
   │  OpenSeadragon (deep-zoom dos desenhos)                                            │
   │  Módulos: Dashboard · TGL Core · Classes · Patente(abas) · Docket · Runners ·      │
   │           Render viewer · Notas/Instruções · Prompt Compiler · Hash/Seal · Riscos  │
   └──────────────────────────────────────────────────────────────────────────────────┘
```

### 3.1 Papel de cada componente

| Componente | Responsabilidade única | Nunca faz |
|---|---|---|
| **Indexador** (Watchdog + `reindex`) | Observar a árvore da RAIZ, parsear os arquivos canônicos e **espelhar** seu conteúdo em `central.db`. Incremental (por mtime+hash) e full. | Não é dono do dado; não escreve nos originais; não inventa campos ausentes. |
| **Hash Engine** (manifesto SHA-256) | Gerar/verificar hashes: linha-de-base dos originais, manifesto de artefatos de runner, prova "originais intactos". | Não modifica arquivos; não recalcula física. |
| **Runner Harness** | Invocar `one_<slug>.py` em subprocess no `tgl_env`, capturar `results.json`/`seal.json`/figuras, registrar a execução. | Não contém a lógica da invenção; não edita o runner nem os originais; não deixa alegar física. |
| **Prompt Compiler** | Renderizar `compiled_prompts\<ts>_CLAUDE_CODE_TASK.md` a partir das notas/instruções `active`. | Não executa nada; não chama IA; não decide sozinho o que é confidencial (usa a blocklist). |
| **API REST** | Servir leitura (SQLModel↔central.db) e receber escritas (que viram arquivo + reindex). | Não é a verdade; endpoints de escrita nunca gravam só no DB. |
| **SQLite `central.db`** | Índice/cache consultável, com FTS para busca textual. | Não sobrevive como fonte; pode ser apagado. |
| **Frontend** | Cockpit visual: navegar, ampliar, clicar componente, disparar runner, ver selo, editar nota, compilar prompt. | Não calcula β; não esconde marcadores; não fala com a internet. |

### 3.2 Módulos internos do backend (organização de pacotes — nomes em inglês)

```
backend/
  app.py                 # cria FastAPI, monta routers, CORS localhost, mounts estáticos (modo operador)
  config.py              # ROOT path, portas, flags de modo, blocklist paths
  cli.py                 # entrypoints: reindex [--full], verify-originals, run <patent_id>, compile-prompt <patent_id>
  data/central.db        # SQLite (gerado; ignorado por git)
  models/                # SQLModel: Patent, PatentClass, Document, DocketEntry, Deadline, Note, RunnerRun, Render, CompiledPrompt, Pendencia
  indexer/
    watcher.py           # Watchdog Observer -> fila debounced
    reindex.py           # walk + parse + upsert (idempotente)
    parsers/             # yaml_docket.py, notes_yaml.py, master_index.py, memory_md.py, results_seal.py
  hashing/
    manifest.py          # sha256 de arquivo/pasta, gera/lê manifests
    verify.py            # re-hash Patentes\ vs original_hashes.json -> relatório
  runners/
    harness.py           # subprocess tgl_env, timeout, env PYTHONUTF8=1, captura artefatos, registra RunnerRun
    policy.py            # guarda-corpos: physical_verdict_allowed, vocabulário proibido, anti-hardcode (lint)
  compiler/
    templater.py         # render determinístico do prompt (Jinja2), blocklist-aware
  api/
    routers/             # patents.py, classes.py, documents.py, docket.py, notes.py, runners.py, renders.py, prompts.py, integrity.py, search.py, core.py
    schemas.py           # DTOs Pydantic de resposta (read models)
  security/
    blocklist.py         # padrões de caminho/nome confidenciais; nega leitura/export
    readonly.py          # guarda que impede qualquer escrita sob Patentes\ e fora da RAIZ
```

> O detalhamento campo-a-campo das tabelas está em `DATA_MODEL.md`; a superfície REST completa
> em `DATA_MODEL.md`/`UI_SPEC.md`; a política do harness e do compilador em `WORKFLOW.md` e
> `PROMPT_COMPILER_SPEC.md`. Aqui fixamos a **forma**, não o schema fino.

---

## 4. Entidades canônicas e onde vivem (visão de arquitetura)

Mapa entidade → arquivo dono → tabela-espelho. (Schema detalhado: `DATA_MODEL.md`.)

| Entidade | Dono no filesystem (fonte da verdade) | Espelho em `central.db` |
|---|---|---|
| **PatentClass** | `memory\classes\CLASS_01..10.md` | `patent_class` |
| **Patent** | `memory\PATENT_MASTER_INDEX.yaml` + `memory\patents\<ID>_<SLUG>.md` | `patent` |
| **Document** (com hash) | `Patentes\...` (RO) + `vault\normalized_docs\...`; hashes em `source_inventory\original_hashes.json` | `document` |
| **DocketEntry / Deadline** | `patents\<ID>_<SLUG>\docket.yaml` | `docket_entry`, `deadline` |
| **Note / Instruction** (`active:bool`, `tipo: nota\|sugestao\|instrucao\|tarefa\|bloqueio\|pergunta`) | `patents\<ID>_<SLUG>\notes\notes.yaml` (estruturado) + `notes\initial_notes.md` (narrativo) | `note` |
| **RunnerRun** (`results.json` + `seal.json`) | `patents\<ID>_<SLUG>\results\` e `\seals\` | `runner_run` |
| **Render** | `patents\<ID>_<SLUG>\renders\` (+ imagens extraídas dos PDFs) | `render` |
| **CompiledPrompt** | `compiled_prompts\<ts>_CLAUDE_CODE_TASK.md` | `compiled_prompt` |
| **Pendencia** | `PENDENCIAS.md` (P-01…P-09, status `[ABERTA]/[RESPONDIDA]/[FECHADA]`) | `pendencia` |

**Nota sobre `notes.yaml`.** As notas/instruções estruturadas (com `active`, `tipo`, autor,
timestamp) são o insumo do Prompt Compiler; por isso ganham um arquivo YAML diffável e
máquina-editável, ao lado do `initial_notes.md` humano. A API de escrita de notas
(`POST/PATCH /api/patents/{id}/notes`) edita `notes.yaml` e dispara reindex — nunca escreve só
no DB. Formato-contrato (ver `DATA_MODEL.md` para o schema completo):

```yaml
# patents/<ID>_<SLUG>/notes/notes.yaml
patent: "BR102026004850-0"      # SkyGrid, exemplo
notes:
  - id: "n-0001"
    tipo: "tarefa"              # nota|sugestao|instrucao|tarefa|bloqueio|pergunta
    active: true
    created: "2026-07-09T14:32:00-03:00"
    author: "operador"
    text: "Portar o digital twin v3 do SkyGrid_Piloto para one_skygrid.py como runner REAL."
    refs: ["Patentes/Skygrid/SkyGrid_Piloto/SKYGRID_v3_ENERGIA_FINAL.md"]
```

---

## 5. Fluxos de dados

### 5.1 Fluxo A — filesystem → reindex → SQLite → API → UI (leitura)

```
[arquivo .md/.yaml/.json muda]  ──►  Watchdog capta evento
        │                                    │
        │                                    ▼
        │                          fila debounced (≈750 ms)
        │                                    │
        ▼                                    ▼
  reindex incremental  ──►  parser específico  ──►  upsert em central.db
  (só arquivos com mtime/hash                            │
   diferente do registrado)                              ▼
                                            API GET /api/... (SQLModel)
                                                          │
                                                          ▼
                                       Frontend (React Query) renderiza
```

- **Gatilho:** salvar qualquer arquivo canônico sob a RAIZ (edição manual pelo operador, ou
  escrita da própria API, ou saída de um runner). `Patentes\` é observado apenas para
  **detectar violação de integridade** (não deveria mudar) — mudança ali gera alerta, não
  reindex de conteúdo.
- **Idempotência:** `reindex` é seguro de rodar N vezes; usa `source_file` + `content_sha256`
  + `mtime` por linha para evitar reprocessar o que não mudou.
- **Reconstrução total:** `python -m backend.cli reindex --full` apaga e refaz `central.db`.
- **Exemplo concreto:** o operador corrige a data de um prazo em
  `patents\BR102026004850-0_SKYGRID\docket.yaml` (SkyGrid, janela de Paris 2027-03-01). Ao
  salvar, o Watchdog dispara; `parsers/yaml_docket.py` relê o arquivo; o `deadline` é
  atualizado no DB; a aba **Prazos** do SkyGrid mostra o novo alerta sem reiniciar nada.

### 5.2 Fluxo B — runner → results/seal → UI (execução)

```
UI: botão "Executar runner"  ──►  POST /api/patents/{id}/runs
        │
        ▼
Runner Harness:
  1. valida: existe patents/<ID>/runner/one_<slug>.py ?           (senão -> 404 scaffold ausente)
  2. subprocess: tgl_env\python one_<slug>.py   (cwd=pasta da patente; env PYTHONUTF8=1; sem rede; timeout)
  3. captura stdout/stderr -> logs\runs\<ts>.log
  4. runner grava results\<ts>_results.json  +  renders\*.png  +  seals\<ts>_seal.json
  5. harness lê seal.json; aplica policy.py:
        - exige physical_verdict_allowed == false quando a classe é física
        - rejeita vocabulário proibido (PROVED/CONFIRMED/TGL_TRUE/REFUTED)
        - anti-hardcode: procura literal 0.012031… em código de cálculo -> falha honesta
  6. Hash Engine sela: manifesto SHA-256 de {código, results, figuras}
  7. registra RunnerRun no DB via reindex do diretório results\/seals\
        │
        ▼
UI: aba "Execuções" lista a run; aba "Selo/Hash" mostra o manifesto;
    aba "Runner" mostra β_runtime, veredito máx e figuras — com carimbo
    "simulação não valida física" quando aplicável.
```

- **O harness é orquestrador, não autor.** A lógica da invenção mora em `one_<slug>.py`
  (portado/adaptado dos protótipos REAIS — nunca editando originais). O harness só invoca,
  captura, sela e indexa.
- **Ordem natural de maturação (do disco):** SkyGrid (piloto v3 pronto) → ACOM/Tensor → MQC →
  Mirror/Crypto → IALD → Ψ-NET/PsiBit → Dípolo/Célula → demais. Patentes sem protótipo (ex.:
  **Oncologia** — nenhum código localizado, `[DATA_REQUIRED]`) começam como **scaffold
  honesto** que roda, declara o que falta e não finge resultado.
- **Exemplo concreto (SkyGrid):** `one_skygrid.py` reaproveita o digital twin v3
  (`SkyGrid_Piloto\`), emite `seal.json` com `beta_runtime: 0.012031300400803142`,
  `physical_verdict_allowed: false`, `max_verdict: "MODEL_CLOSES / ENERGY_BALANCE_OK ([SIM]
  sob [CONJ])"`. A UI mostra exatamente esses valores — o frontend não recomputa nada.

### 5.3 Fluxo C — nota/instrução (UI → filesystem → reindex)

```
UI aba "Notas/Instruções": operador adiciona tarefa (tipo=tarefa, active=true)
        │
        ▼
POST /api/patents/{id}/notes
        │
        ▼
escreve/atualiza  patents/<ID>/notes/notes.yaml   (arquivo = verdade; append/patch)
        │
        ▼
Watchdog -> reindex(notes.yaml) -> tabela note atualizada -> UI reflete
```

Toggle `active` e mudança de `tipo` seguem o mesmo caminho (arquivo primeiro). Isso mantém as
notas versionáveis e auditáveis fora do banco.

### 5.4 Fluxo D — prompt compiler (COMPILAR INSTRUÇÕES)

```
UI: botão central "COMPILAR INSTRUÇÕES" (global ou por patente)
        │
        ▼
POST /api/prompts/compile   { scope: "patent"|"class"|"all", patent_id?, selection? }
        │
        ▼
Prompt Compiler (templater.py):
  header TGL Core (de memory/TGL_CORE_MEMORY.md)
    -> por classe (memory/classes/CLASS_xx.md)
      -> por patente: identificação + notas/instruções com active=true
         + caminhos PERMITIDOS (patents/<ID>/…, vault/) e PROIBIDOS (Patentes\ RO, blocklist)
         + tarefas priorizadas + critérios de aceite + a régua (não modificar originais)
        │
        ▼
grava  compiled_prompts/<YYYY-MM-DD_HHMM>_CLAUDE_CODE_TASK.md   (arquivo = verdade)
        │
        ▼
reindex -> tabela compiled_prompt -> UI mostra prévia + botão "copiar" + caminho do arquivo
```

Determinístico e blocklist-aware: nunca inclui conteúdo confidencial (§8.3) no prompt. Detalhe
completo do template em `PROMPT_COMPILER_SPEC.md`.

### 5.5 Fluxo E — prova de integridade (originais intactos)

```
UI badge de integridade  /  CLI verify-originals
        │
        ▼
Hash Engine: re-hash de todos os arquivos de Patentes\
        │
        ▼
compara com source_inventory/original_hashes.json (linha-de-base)
        │
        ├─ todos batem  -> status "verde: originais intactos (N arquivos)"  +  registra em logs\
        └─ divergência   -> status "vermelho": lista arquivos alterados/faltantes -> alerta + PENDENCIAS
```

Este fluxo é o cumprimento vivo de `DO_NOT_MODIFY_ORIGINALS` e do critério de aceite da Fase 3
("re-hash == hashes iniciais"). Roda sob demanda (badge) e no boot do backend (log).

---

## 6. Superfície de API (contrato de alto nível)

REST sob `/api`, JSON, apenas `127.0.0.1`. Leitura serve read-models do `central.db`; escrita
grava arquivo + dispara reindex. (Schemas de request/response detalhados em `DATA_MODEL.md`.)

| Método | Rota | Faz | Escreve arquivo? |
|---|---|---|---|
| GET | `/api/core` | header TGL, Estado Verificado, selos | — |
| GET | `/api/classes` · `/api/classes/{code}` | classes e suas patentes | — |
| GET | `/api/patents` · `/api/patents/{id}` | lista e detalhe (todas as abas agregadas) | — |
| GET | `/api/patents/{id}/documents` | documentos + hashes | — |
| GET | `/api/patents/{id}/docket` | docket + deadlines + alert_level | — |
| PATCH | `/api/patents/{id}/docket` | edita `docket.yaml` | **sim** → reindex |
| GET/POST/PATCH | `/api/patents/{id}/notes` | lê/cria/atualiza notas em `notes.yaml` | **sim** → reindex |
| GET | `/api/patents/{id}/runs` · `/api/runs/{run_id}` | execuções e artefatos | — |
| POST | `/api/patents/{id}/runs` | dispara runner via harness | **sim** (results/seal) |
| GET | `/api/patents/{id}/renders` | renders e camadas | — |
| GET | `/api/patents/{id}/seal` | manifesto SHA-256 mais recente | — |
| POST | `/api/prompts/compile` | compila prompt | **sim** → `compiled_prompts\` |
| GET | `/api/prompts` · `/api/prompts/{id}` | lista/lê prompts compilados | — |
| GET | `/api/integrity` | status "originais intactos" | — (log) |
| POST | `/api/integrity/verify` | re-hash sob demanda | — (log) |
| POST | `/api/admin/reindex` | reindex incremental/full | — |
| GET | `/api/search?q=` | busca FTS (patentes, notas, docket, memórias) | — |
| GET | `/api/pendencias` | P-01…P-09 e status | — |

Convenções: erros como `{ "error": { "code", "message", "path?" } }`; escritas retornam o
recurso reindexado; toda resposta de número técnico carrega seu `label` ([REAL]/[SIM]/…).

---

## 7. Persistência: filesystem canônico + espelho SQLite

- **SQLite** com **WAL** (`journal_mode=WAL`), `foreign_keys=ON`, um único arquivo
  `backend\data\central.db`. Acesso via SQLModel (leitura) — escrita no DB **só** pelo
  indexador.
- **FTS5** (`patent_fts`, `note_fts`, `memory_fts`) para a busca global — reconstruído no
  reindex.
- **Sem migrations de dados:** como o DB é derivado, mudança de schema = bump de
  `SCHEMA_VERSION` + `reindex --full`. Não há "perda" possível porque a verdade está nos
  arquivos. (Isso simplifica enormemente a evolução: sem Alembic obrigatório.)
- **Registro de proveniência:** cada linha guarda `source_file`, `source_sha256`,
  `indexed_at`. A UI pode sempre responder "de qual arquivo veio este dado".

---

## 8. Segurança e privacidade

### 8.1 Superfície de rede mínima

- Backend liga em `127.0.0.1:8765`; frontend dev em `127.0.0.1:5173`. **Nunca** `0.0.0.0`.
- CORS restrito a `http://127.0.0.1:5173` (dev) e same-origin (operador). Sem autenticação
  remota porque não há superfície remota — usuário único, máquina do operador.
- Sem chamadas de saída: sem CDNs em runtime (fonts/js/css empacotados no bundle), sem
  telemetria, sem "phone home". A internet não é requisito de funcionamento.

### 8.2 Originais read-only, com guarda em código

- `security/readonly.py` é um guarda central: **qualquer** operação de escrita cujo caminho
  resolva para dentro de `Patentes\` ou para **fora** da RAIZ é negada antes de tocar o disco
  (defesa em profundidade, além da disciplina humana).
- Recomenda-se ainda (operacional, do operador) marcar `Patentes\` como somente-leitura no SO.
- O Watchdog trata mudança em `Patentes\` como **incidente de integridade**, não como update.

### 8.3 Blocklist confidencial (nunca lê para exportar, nunca publica)

Padrões de caminho/nome que a plataforma pode **usar localmente** (um runner pode importar um
stack), mas que **nunca** são expostos por API pública, incluídos em prompt compilado, ou
copiados para artefatos exportáveis:

- `iald_stack_v7.py`, `iald_psion_state.json` e correlatos (stacks confidenciais);
- qualquer `token*.txt` / segredo (ex.: o `token_huggin.txt` em `projetos_pyhton\tgl-tensor\`
  — **jamais** copiar para a Central, conforme PENDENCIAS P-09);
- caminhos de produção com usuários reais (ex.: `iald_web_server.py`) — **não tocar, não
  rodar**.

`security/blocklist.py` centraliza os padrões (glob/regex). O Prompt Compiler e todo endpoint
de leitura de conteúdo consultam a blocklist antes de emitir bytes. Selo:
stacks confidenciais nunca exportados.

### 8.4 Aviso legal permanente

Todo docket, painel legal e prompt compilado carrega, imutável: **"Controle interno; não
substitui agente de propriedade industrial. Prazos oficiais conferidos com INPI/WIPO."** A
regra ePCT do operador é dado fixo: **só o ACOM raiz** (BR102025026951-1) tem ePCT **vivo**
(**PCT/BR2025/050558**, 05/12/2025, depositado e pago). As outras 15 são **hoje somente
INPI**: o ePCT **ainda não foi depositado** — é o **próximo passo planejado** (novo processo
originário, sem vínculo), status **A_DEPOSITAR / PENDENTE**, não direito perdido. Os 10
recibos ePCT de 17/02/2026 (família PCT/BR2026/050068–050076) no Acervo são uma **tentativa de
protocolo abandonada de propósito** — rascunho preclusso a ser **substituído** por um depósito
novo e desvinculado, não proteção perdida por descuido. **Janela do novo ePCT:** 12 meses da
prioridade (Convenção de Paris); ⚠ se a prioridade interna (66) de 05/12/2025 governar, pode
ser ~05/12/2026 (bem antes de 2027) — próximo passo possivelmente **urgente**, a levar ao
agente de PI (P-06/P-10). Detalhe em `LEGAL_DOCKET_SPEC.md`.

### 8.5 Sandbox dos runners

O harness roda `one_<slug>.py` como subprocess **sem acesso à rede** por padrão, com `cwd` na
pasta da patente, `timeout` configurável, `PYTHONUTF8=1`, e captura total de stdout/stderr. O
runner só pode escrever dentro da própria pasta da patente (`results\`, `renders\`, `seals\`);
tentativa de escrever em `Patentes\` ou fora da RAIZ é bloqueada pelo guarda de §8.2.

---

## 9. Modos de execução

Dois modos, uma base de código. Selecionados por variável de ambiente `CENTRAL_MODE` e/ou
flags de CLI.

### 9.1 Modo DEV (construção da plataforma)

- **Backend:** `uvicorn backend.app:app --reload --host 127.0.0.1 --port 8765` (venv do
  backend). Watchdog ativo; logs verbosos; CORS libera `:5173`.
- **Frontend:** `npm run dev` (Vite) em `127.0.0.1:5173`, com proxy `/api → 127.0.0.1:8765`.
  Hot Module Replacement.
- **Uso:** desenvolver componentes, iterar UI, testar endpoints.

### 9.2 Modo OPERADOR (uso local do cockpit)

- **Build único:** `npm run build` gera `frontend\dist\`. O backend **monta o bundle
  estático** em `/` e serve a API em `/api` — **tudo numa porta só, 8765**. Um clique/atalho
  (`start_central.ps1`) sobe `uvicorn backend.app:app --host 127.0.0.1 --port 8765` (sem
  `--reload`) e abre `http://127.0.0.1:8765`.
- **Endurecido:** CORS same-origin; sem endpoints de admin destrutivos expostos além de
  `reindex`/`verify`; Watchdog ativo para refletir edições manuais do operador em tempo real.
- **Uso:** o operador controla o acervo, dispara runners, edita docket/notas, compila prompts.

> Ambos os modos dependem de **dois runtimes Python distintos**, de propósito: (a) o **venv do
> backend** (FastAPI etc.) e (b) o **`tgl_env`** (`C:\IALD\observaveis_tgl\tgl_env`, com
> scipy/matplotlib) que o harness invoca para os runners. A Central nunca "mistura" os dois —
> o backend é leve; a computação científica fica no `tgl_env`.

---

## 10. Dependências e versões-alvo

Alvos conservadores e compatíveis (2026). "≥" indica piso; usar a última linha estável
compatível. Todas as libs de UI empacotadas no bundle (sem CDN em runtime).

### 10.1 Backend (venv próprio, `backend\.venv`)

| Dependência | Versão-alvo | Papel |
|---|---|---|
| Python | 3.11+ | runtime do backend |
| FastAPI | ≥ 0.115 | framework HTTP/API |
| Uvicorn (standard) | ≥ 0.32 | servidor ASGI |
| SQLModel | ≥ 0.0.22 | ORM (leitura) sobre SQLite |
| Pydantic | v2 (≥ 2.9) | validação/serialização (DTOs) |
| SQLite | stdlib (WAL, FTS5) | índice/cache |
| Watchdog | ≥ 5.0 | observação de filesystem |
| PyYAML | ≥ 6.0 | parse de `docket.yaml`/`notes.yaml`/`PATENT_MASTER_INDEX.yaml` |
| Jinja2 | ≥ 3.1 | template do Prompt Compiler |
| pypdf / pdfminer.six | (já usados na Fase 1) | extração de imagens/texto dos PDFs para renders |
| hashlib | stdlib | SHA-256 (motor de manifesto) |

### 10.2 Runner runtime (separado)

| Dependência | Versão-alvo | Papel |
|---|---|---|
| `tgl_env` (Python) | existente | executa `one_<slug>.py` |
| numpy / scipy / matplotlib | conforme `tgl_env` | computação/figuras dos runners |
| `PYTHONUTF8` | `=1` (obrigatório) | encoding em toda invocação |

### 10.3 Frontend (`frontend\`)

| Dependência | Versão-alvo | Papel |
|---|---|---|
| Node.js | 20 LTS (ou 22 LTS) | toolchain |
| React + ReactDOM | 18.3 (19 aceitável se shadcn/ui compatível) | UI |
| TypeScript | ≥ 5.5 | tipagem |
| Vite | ≥ 5.4 (6 aceitável) | dev server + build (:5173) |
| Tailwind CSS | 3.4 (4.x se migração validada) | estilo utilitário |
| shadcn/ui + Radix UI | atual | componentes acessíveis |
| @xyflow/react (React Flow) | ≥ 12 | diagramas de componentes clicáveis |
| @react-three/fiber + three | R3F ≥ 8 / three ≥ 0.16x | 3D ilustrativo [PILOTO] |
| react-plotly.js + plotly.js | 2.x | gráficos (β, séries, ROC) |
| OpenSeadragon | ≥ 4 | deep-zoom dos desenhos das patentes |
| TanStack Query (React Query) | ≥ 5 | cache de dados da API |
| React Router | ≥ 6 | rotas dos módulos |

> Detalhamento de bibliotecas de render (extração de imagem dos PDFs, geração de tiles para
> OpenSeadragon, grafos React Flow por patente) em `RENDERING_SPEC.md`.

---

## 11. Riscos técnicos e mitigação

| # | Risco | Impacto | Mitigação |
|---|---|---|---|
| R1 | **DB tratado como verdade** (escrita direta no SQLite) corrompe o invariante P3 | Perda de confiança no dado; divergência silenciosa | Endpoints de escrita **só** gravam arquivo + reindex; `verify` compara `source_sha256`; `reindex --full` sempre possível; testes que provam "DB = função pura dos arquivos". |
| R2 | **Watchdog perde/duplica eventos** no Windows (renomes, saves atômicos, locks) | Índice defasado | Debounce (≈750 ms) + reconciliação periódica por varredura completa; `reindex --full` no boot; badge "última indexação". |
| R3 | **Modificação acidental de original** em `Patentes\` | Viola `DO_NOT_MODIFY_ORIGINALS` | Guarda `readonly.py` nega escrita; SO read-only recomendado; `verify-originals` no boot e badge; Watchdog trata mudança como incidente. |
| R4 | **Runner alega física** (vocabulário/veredito indevido) | Fere a régua | `runners/policy.py`: exige `physical_verdict_allowed=false`, rejeita PROVED/CONFIRMED/TGL_TRUE/REFUTED, teto de veredito herdado do SkyGrid; UI carimba "não valida física". |
| R5 | **β hardcoded** em código de runner | Fere P7 | Auditoria anti-hardcode na suíte (procura literal `0.012031…`); β só de `seal.json.beta_runtime` na UI; `ALPHA_FINE_CODATA_2018 * sqrt(e)` obrigatório em runtime. |
| R6 | **Vazamento de confidencial** (stack/token) via API ou prompt | Quebra de sigilo | `blocklist.py` consultada por toda leitura de conteúdo e pelo compilador; token nunca copiado (P-09); testes negativos. |
| R7 | **Runner trava/loop/consome recurso** | Backend pendura | Subprocess com `timeout`, sem rede, `cwd` isolado, kill em estouro; execução assíncrona com status `queued/running/done/failed`. |
| R8 | **Extração de imagem dos PDFs frágil** (desenhos em baixa resolução) | Deep-zoom pobre | Preferir imagens vetoriais/alta-res; fallback ao PDF renderizado em DPI alto; rotular qualidade; `RENDERING_SPEC.md` define pipeline. |
| R9 | **Peso de assets 3D/tiles** (SkyGrid tem 134 documentos hasheados) | UI lenta | Lazy-load por aba; tiles OpenSeadragon sob demanda; virtualização de listas; R3F só quando a aba 3D abre. |
| R10 | **Divergência documento × memória** (ex.: grafias INPI sem hífen do DV na Oncologia; P-03 número 2024) | Dado errado no docket | Fonte da verdade = PDF; divergência → `PENDENCIAS.md` e perguntar; nunca escolher em silêncio; UI mostra pendências ligadas à patente. |
| R11 | **Encoding/paths Windows** (acentos em `Patentes\`, UTF-8) | Parse quebra | `PYTHONUTF8=1` em todo subprocess; I/O sempre `encoding="utf-8"`; caminhos por `pathlib`, nunca concatenação de string. |
| R12 | **Deriva de dependências** (Tailwind 4, React 19, Vite 6) | Build quebra | Pinar versões-alvo (§10) em `package.json`/`requirements.txt`; lockfiles versionados; upgrades como tarefa deliberada. |
| R13 | **Selo do artefato canônico defasado** (P-07: SHA do `tgl_paper_unified.py` diverge do pinado) | Confusão de proveniência | Exibir SHA **executado** e SHA **pinado** lado a lado, com link à pendência; nunca "consertar" em silêncio. |

---

## 12. Critérios de pronto da Fase 3 (Definition of Done da primeira rodada)

A Fase 3 estará "pronta" (primeira rodada) quando **todos** os itens abaixo forem
demonstráveis ao operador. Espelha os entregáveis do prompt inaugural e alimenta o
`VALIDATION_CHECKLIST.md`.

**Infra e integridade**
1. Estrutura de pastas do backend/frontend criada dentro da RAIZ; nada escrito fora dela.
2. Backend sobe em `127.0.0.1:8765`; frontend sobe (dev `:5173`; operador servido em `:8765`).
3. `central.db` populado por `reindex --full` a partir das memórias/docket/notes/results/seals
   existentes; `reindex` incremental reflete edições em tempo real (Watchdog).
4. **Originais intactos provados:** `verify-originals` re-hasheia `Patentes\` e bate com
   `source_inventory\original_hashes.json`; badge verde na UI e registro em `logs\`.

**Navegação (a bancada do Tony Stark)**
5. **Dashboard geral** navegável: 16 patentes, 10 classes, prazos vivos, status de integridade.
6. **Página individual de patente** com as abas: Overview · Documentos · Reivindicações ·
   Protótipo · Render 2D/3D · Runner · Execuções · Selo/Hash · Prazos · Notas · Instruções ·
   **[COMPILAR INSTRUÇÕES]** — funcionando ao menos para uma patente com protótipo (SkyGrid) e
   uma sem (Oncologia, como scaffold honesto).
7. **Render viewer** com deep-zoom (OpenSeadragon) do desenho oficial + diagrama de componentes
   clicáveis (React Flow); 3D [PILOTO] onde aplicável, sempre rotulado.
8. **Legal docket** com os prazos extraídos dos documentos (ACOM ePCT vivo PCT/BR2025/050558;
   as 15 somente-INPI com ePCT **a depositar** — próximo passo planejado, janela de 12 meses
   da prioridade, possivelmente ~05/12/2026 se a prioridade interna de 05/12/2025 governar) e o
   aviso legal permanente.

**Funções vivas**
9. **Runner** disparável pela UI para ao menos uma patente; `results.json`/`seal.json`/figuras
   gerados; aba Execuções e Selo/Hash mostram os artefatos; `physical_verdict_allowed=false`
   exibido; nenhum vocabulário de veredito proibido escapa.
10. **Prompt Compiler** funcional: **[COMPILAR INSTRUÇÕES]** gera
    `compiled_prompts\<ts>_CLAUDE_CODE_TASK.md` com header TGL Core → classe → patente →
    caminhos permitidos/proibidos → tarefas → critérios → régua; prévia e cópia na UI;
    confidenciais bloqueados.
11. **Hash/Seal viewer** funcional: manifesto SHA-256 de originais e de artefatos de runner.
12. **Busca** (FTS) sobre patentes, notas, docket e memórias.

**Disciplina**
13. **Nenhum arquivo original modificado** (re-hash == hashes iniciais — item 4 reprovado ⇒
    Fase 3 reprovada).
14. Nenhum confidencial exportado; blocklist testada (§8.3).
15. Toda escrita da UI foi ao **arquivo** primeiro (P3): apagar `central.db` e rodar
    `reindex --full` reproduz o estado exibido — **prova viva de que o filesystem é a verdade**.

---

## 13. Relação com os documentos irmãos (mapa de responsabilidades)

| Documento | Cobre (o que ESTE aqui apenas referencia) |
|---|---|
| `DATA_MODEL.md` | Schema campo-a-campo das entidades, tabelas SQLite, DTOs Pydantic, contratos request/response da API. |
| `UI_SPEC.md` | Layout dos 12 módulos, abas por patente, componentes visuais, estados, interações. |
| `WORKFLOW.md` | O loop sem fim, o ciclo do runner harness, políticas de execução e de indexação. |
| `PROMPT_COMPILER_SPEC.md` | Template exato do prompt compilado, ordem, blocklist, campos de nota. |
| `LEGAL_DOCKET_SPEC.md` | Campos do docket, cálculo de prazos, níveis de alerta, regra ePCT, aviso legal. |
| `RENDERING_SPEC.md` | Pipeline desenho→tiles, grafos React Flow por patente, 3D [PILOTO], rótulos de honestidade. |
| `VALIDATION_CHECKLIST.md` | Checklist operacional do gate de validação e da Fase 3 (§12 aqui é a semente). |

---

## 14. Rodapé — selos e disciplina

**Selos honrados por esta arquitetura:**
`TGL_PATENT_CONTROL_CENTER` · `FORM_EQUALS_CONTENT_FOR_EACH_PATENT` ·
`ONE_RUNNER_ONE_PATENT_ONE_SEAL` · `DO_NOT_MODIFY_ORIGINALS` ·
`MEMORY_FIRST_ARCHITECTURE_SECOND_CODE_LAST` · `SIMULATION_NEVER_VALIDATES_PHYSICS`.

Filesystem é a verdade; o SQLite é o vidro. Os originais não se tocam; provam-se intactos por
hash. O número corrige a frase; β nunca é literal; a simulação nunca valida física. Memória
primeiro, arquitetura (este documento) segundo, código por último.

> **TGL = haja luz. Tetelestai. 1 = 1.**
