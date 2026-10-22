# DATA_MODEL.md — Central de Controle e Desenvolvimento de Patentes TGL

**Fase 2 · Especificação · nenhum código de aplicação.** Este documento define o
modelo de dados canônico da Central: entidades, campos tipados, chaves, relações,
formatos de arquivo (a fonte da verdade), mapeamento arquivo↔tabela com regras de
parse, o comando `reindex`, a estratégia de migração e as consultas do dashboard.
A Fase 3 codifica a partir daqui **sem voltar a perguntar**.

> **Régua herdada (inviolável):** originais READ-ONLY; o número corrige a frase;
> `β_TGL` nunca literal em código (`ALPHA_FINE_CODATA_2018 * sqrt(e)`); simulação
> nunca valida física (`physical_verdict_allowed=false`); marcadores em tudo;
> controle interno não substitui agente de propriedade industrial.

---

## 0. Princípio arquitetural do dado — o eixo que rege TODO este documento

**O FILESYSTEM É A FONTE DA VERDADE. O SQLite é ÍNDICE/CACHE, 100% reconstruível.**

```
                 ┌──────────────────────────────────────────┐
   VERDADE  →    │  Arquivos dentro de C:\IALD\Central...\   │
 (imutável       │  memory\*.md / *.yaml · docket.yaml ·     │
  ou versionada  │  notes\*.md · seals\*.json · results\ ·   │
  pelo operador) │  renders\ · PENDENCIAS.md · source_inv\   │
                 └───────────────┬──────────────────────────┘
                                 │  parse + hash (reindex, Watchdog)
                                 ▼
                 ┌──────────────────────────────────────────┐
   ÍNDICE   →    │  backend\data\central.db  (SQLite)        │
 (descartável,   │  espelha os arquivos; guarda content_hash │
  regenerável)   │  de cada fonte p/ detectar DRIFT          │
                 └───────────────┬──────────────────────────┘
                                 │  SELECT (read-only p/ o dado canônico)
                                 ▼
                 Backend FastAPI :8765  →  Frontend React :5173
```

Consequências de projeto, obrigatórias:

1. **Nenhum dado nasce no SQLite.** Toda escrita de dado canônico (uma nota nova, uma
   instrução, um prazo customizado) é escrita PRIMEIRO no arquivo `.md`/`.yaml`
   correspondente; o SQLite só é atualizado por `reindex` (ou pelo job Watchdog que
   chama `reindex` incremental daquele arquivo). O banco nunca é o dono do dado.
2. **`central.db` pode ser apagado a qualquer momento.** `reindex` reconstrói tudo.
   Isso é o teste de sanidade permanente: `rm central.db && reindex` ⇒ estado idêntico.
3. **Cada linha do índice carrega `source_path` + `source_sha256`** (o hash do arquivo
   que a originou). É assim que o `reindex` é idempotente e detecta drift (§7).
4. **Campos derivados de "hoje"** (dias restantes, bucket de urgência) **não são
   persistidos como verdade** — são calculados na consulta (`as_of = date('now')`),
   ou cacheados com o carimbo `as_of` explícito. O prazo (a data) é verdade; a
   urgência é uma leitura datada dela.

---

## 1. Mapa de entidades e relações (visão geral)

Entidades canônicas (10) + 2 tabelas de sistema (`index_meta`, `reindex_run`):

```
PatentClass 1 ─────< Patent >───────────────────────────┐
 (CLASS_01..10)        │  (16 patentes; PK = processo)   │
                       │                                 │
        ┌──────────────┼───────────────┬─────────────┬───┴────────┐
        │              │               │             │            │
     Document      DocketEntry      Note/Instr    RunnerRun     Render
   (por arquivo;    (1:1 c/         (nota|sugest  (results.json  (desenho|
    hash SHA-256;    docket.yaml)    instr|tarefa  + seal.json)   diagrama|3D)
    N por patente     │              bloqueio|                    │
    ou avulso)        │              pergunta)                    │
                      ▼                                           │
                   Deadline (N; derivada do docket.yaml)          │
                                                                  │
CompiledPrompt >───(inclui Notes active=true de N patentes)───────┘
Pendencia  M ──< relacionada a >── N Patent   (P-01..P-09; PENDENCIAS.md)
```

Cardinalidades:

| Relação | Card. | Chave |
|---|---|---|
| PatentClass → Patent | 1 : N | `patent.class_id → patent_class.id` |
| Patent → Document | 1 : N (Document pode ser avulso, `patent_id` nulo p/ Acervo) | `document.patent_id` |
| Patent → DocketEntry | 1 : 1 | `docket_entry.patent_id` (PK) |
| Patent → Deadline | 1 : N | `deadline.patent_id` |
| Patent → Note | 1 : N | `note.patent_id` |
| Patent → RunnerRun | 1 : N | `runner_run.patent_id` |
| Patent → Render | 1 : N | `render.patent_id` |
| Patent ↔ Pendencia | M : N | tabela ponte `pendencia_patent` |
| CompiledPrompt ↔ Note | M : N (snapshot) | tabela ponte `compiled_prompt_note` |

---

## 2. Camada de arquivos — a fonte da verdade (arquivo → entidade)

Toda tabela do índice tem UM arquivo (ou conjunto) que a origina. O `reindex` lê
somente daqui; nunca inventa.

| Entidade (tabela SQLite) | Arquivo(s) fonte (verdade) | Regra de parse (resumo) | Precedência em conflito |
|---|---|---|---|
| `patent_class` | `memory\classes\CLASS_01..10.md` | headers `##` + bloco de metadados | md manda |
| `patent` | `memory\PATENT_MASTER_INDEX.yaml` (catálogo) + `memory\patents\<ID>_<SLUG>.md` (narrativa) | YAML: 1 item de `patentes:` = 1 patente; md enriquece campos textuais | **catálogo YAML** manda em id/datas; docket manda no estado legal |
| `document` | `source_inventory\original_hashes.json` ⋈ `discovered_files.json` ⋈ `extraction_report.json` (join por `rel_path`) | JSON; classificar `doc_role` pelo nome | hashes.json manda no SHA |
| `docket_entry` | `patents\<ID>_<SLUG>\docket.yaml` | YAML load direto | **docket.yaml é autoridade legal** |
| `deadline` | derivada de `docket.yaml` (campos de data) + `notes` custom | computar 1 linha por campo de prazo presente | docket manda |
| `note` | `patents\<ID>_<SLUG>\notes\*.md` | parser de seções (§5.7) | md manda |
| `runner_run` | `patents\<ID>_<SLUG>\seals\<run>\seal.json` + `results\<run>\results.json` (SkyGrid: `SKYGRID_*_SELO.json`) | JSON | seal.json manda |
| `render` | `patents\<ID>_<SLUG>\renders\*` + `prototype\component_specs.json` + desenhos extraídos | varredura + JSON | arquivo manda |
| `compiled_prompt` | `compiled_prompts\YYYY-MM-DD_HHMM_CLAUDE_CODE_TASK.md` | nome do arquivo + header YAML embutido | arquivo manda |
| `pendencia` | `PENDENCIAS.md` (raiz da Central) | parser de headings `## P-NN [STATUS]` | md manda |
| `index_meta`, `reindex_run` | (sistema) gerado pelo `reindex` | — | — |

**Regra da casa aplicada ao parse:** se `docket.yaml` e `PATENT_MASTER_INDEX.yaml`
divergirem num campo legal (ex.: `epct.numero`), o `reindex` **não escolhe em
silêncio**: grava o valor do docket, marca `patent.conflict_flag = true` e emite uma
linha no `reindex_report.json` (→ o operador materializa em `PENDENCIAS.md`).

Convenções de tipo (SQLite tem afinidade fraca; padronizamos):

- **Datas:** `TEXT` ISO-8601 `YYYY-MM-DD` (nunca `DD/MM/YYYY` no índice — o parser
  converte). Datas+hora: `YYYY-MM-DDTHH:MM:SS`.
- **Listas / mapas:** `TEXT` contendo JSON (SQLite JSON1: `json_extract`, `json_each`).
- **Booleanos:** `INTEGER` 0/1.
- **`<ID>`** = `processo` INPI canônico com hífen do dígito verificador,
  ex. `BR102025026951-1`. **`dir_name`** = `<processo>_<SLUG>`,
  ex. `BR102026004850-0_SKYGRID`.

---

## 3. Vocabulários controlados (enums) — válidos em todas as tabelas

> [nota operacional do operador — omitida no retrato público]

**Regra de urgência (função pura `urgency(due_date, as_of)`):**

| dias = due − as_of | urgência |
|---|---|
| dias < 0 | `vencido` |
| 0 ≤ dias ≤ 30 | `vermelho` |
| 31 ≤ dias ≤ 90 | `laranja` |
| 91 ≤ dias ≤ 180 | `amarelo` |
| dias > 180 | `verde` |

`deadline.status ∈ {cumprido, prescrito, na}` sempre exibe cinza (fora do funil de
urgência), independentemente da data.

---

## 4. Esquema SQLite (DDL — contrato do índice)

DDL é contrato de esquema, não código de aplicação. Tipos SQLite; JSON em `TEXT`.
`PRAGMA user_version` carrega o `SCHEMA_VERSION` (§9).

```sql
PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;
PRAGMA user_version = 1;   -- SCHEMA_VERSION

-- 4.1 CLASSES ------------------------------------------------------------
CREATE TABLE patent_class (
  id            TEXT PRIMARY KEY,          -- 'CLASS_06_ENERGIA'
  ordinal       INTEGER NOT NULL,          -- 6
  name          TEXT NOT NULL,             -- 'Energia / Infraestrutura / Materiais'
  slug          TEXT NOT NULL,             -- 'energia'
  description   TEXT,
  markers       TEXT DEFAULT '[]',         -- JSON: ["[ENERGY]"]
  lock_note     TEXT,                      -- trava textual (ex.: só simulação)
  memory_md_path TEXT NOT NULL,            -- 'memory/classes/CLASS_06_ENERGIA.md'
  source_sha256 TEXT NOT NULL,
  indexed_at    TEXT NOT NULL
);

-- 4.2 PATENTS ------------------------------------------------------------
CREATE TABLE patent (
  id             TEXT PRIMARY KEY,         -- processo: 'BR102025026951-1'
  slug           TEXT NOT NULL UNIQUE,     -- 'ACOM'
  dir_name       TEXT NOT NULL UNIQUE,     -- 'BR102025026951-1_ACOM'
  class_id       TEXT NOT NULL REFERENCES patent_class(id),
  role           TEXT,                     -- 'raiz' | 'agregadora' | NULL
  title_54       TEXT NOT NULL,
  nature         TEXT,                     -- '10 - Patente de Invenção (PI)'
  peticao        TEXT,                     -- '870250111877'
  filing_date    TEXT,                     -- ISO 'YYYY-MM-DD'
  priority_date  TEXT,
  jurisdiction   TEXT DEFAULT 'BR (INPI)',
  epct_status    TEXT NOT NULL,            -- enum epct_status
  epct_number    TEXT,                     -- 'PCT/BR2025/050558' | NULL
  epct_date      TEXT,
  abstract       TEXT,                     -- resumo_oficial
  markers        TEXT DEFAULT '[]',        -- JSON list
  prototype_status TEXT DEFAULT 'VER_MEMORIA',
  pasta_original TEXT,                     -- original READ-ONLY
  memory_md_path TEXT,                     -- memory/patents/<ID>_<SLUG>.md
  docket_path    TEXT,                     -- patents/<ID>_<SLUG>/docket.yaml
  doc_count      INTEGER DEFAULT 0,        -- documentos_hasheados
  claims_total   INTEGER,                  -- do md (ex.: 23)
  claims_independent INTEGER,              -- ex.: 5
  figures_count  INTEGER,
  conflict_flag  INTEGER DEFAULT 0,        -- 1 = divergência entre fontes (→ PENDENCIAS)
  source_sha256  TEXT NOT NULL,            -- hash do item do master index
  memory_sha256  TEXT,                     -- hash do md de patente
  indexed_at     TEXT NOT NULL
);
CREATE INDEX ix_patent_class ON patent(class_id);
CREATE INDEX ix_patent_epct  ON patent(epct_status);

-- 4.3 DOCUMENTS ----------------------------------------------------------
CREATE TABLE document (
  id             INTEGER PRIMARY KEY AUTOINCREMENT,
  patent_id      TEXT REFERENCES patent(id),   -- NULL p/ docs de Acervo/avulsos
  rel_path       TEXT NOT NULL UNIQUE,         -- 'Patentes\...\BR..._ACOM.pdf'
  sha256         TEXT NOT NULL,
  size_bytes     INTEGER,
  mtime          TEXT,                         -- ISO datetime
  ext            TEXT,                         -- '.pdf'
  doc_role       TEXT,                         -- enum doc_role
  pages          INTEGER,                      -- de extraction_report
  chars          INTEGER,
  extract_ok     INTEGER,                      -- 0/1
  extract_error  TEXT,
  is_original    INTEGER NOT NULL DEFAULT 1,   -- 1 = sob Patentes\ (READ-ONLY)
  normalized_path TEXT,                        -- vault/normalized_docs/...
  indexed_at     TEXT NOT NULL
);
CREATE INDEX ix_document_patent ON document(patent_id);
CREATE INDEX ix_document_sha    ON document(sha256);

-- 4.4 DOCKET (1:1 com patent) -------------------------------------------
CREATE TABLE docket_entry (
  patent_id      TEXT PRIMARY KEY REFERENCES patent(id),
  status         TEXT,                     -- 'DEPOSITADO'
  alert_level    TEXT,                     -- enum alert_level
  epct_status    TEXT,
  epct_number    TEXT,
  epct_date      TEXT,
  janela_paris_12m TEXT,                   -- ISO date | NULL
  fase_nacional_30m TEXT,                  -- ISO date | 'N/A (nao-ACOM)'
  gru_arquivo    TEXT,
  gru_servico    TEXT,
  gru_nosso_numero TEXT,
  gru_valor      TEXT,                     -- 'R$ 130,00'
  gru_vencimento TEXT,                     -- ISO date
  pix_arquivo    TEXT,
  pix_data       TEXT,
  pix_valor      TEXT,
  annuities_note TEXT,
  office_actions TEXT DEFAULT '[]',        -- JSON list
  reminders      TEXT DEFAULT '[]',        -- JSON list
  aviso          TEXT,                     -- disclaimer legal permanente
  source_sha256  TEXT NOT NULL,            -- hash do docket.yaml
  indexed_at     TEXT NOT NULL
);

-- 4.5 DEADLINES (N; derivadas) ------------------------------------------
CREATE TABLE deadline (
  id             INTEGER PRIMARY KEY AUTOINCREMENT,
  patent_id      TEXT NOT NULL REFERENCES patent(id),
  kind           TEXT NOT NULL,            -- enum deadline_kind
  label          TEXT NOT NULL,            -- PT-BR p/ UI
  due_date       TEXT,                     -- ISO date | NULL (p/ 'na')
  status         TEXT NOT NULL,            -- enum deadline_status
  basis          TEXT,                     -- de que campo/regra saiu
  source_field   TEXT,                     -- 'janela_paris_12m'
  legal_note     TEXT,                     -- [LEGAL] consultar agente...
  indexed_at     TEXT NOT NULL
);
CREATE INDEX ix_deadline_patent ON deadline(patent_id);
CREATE INDEX ix_deadline_due    ON deadline(due_date);
CREATE INDEX ix_deadline_status ON deadline(status);

-- 4.6 NOTES / INSTRUCTIONS ----------------------------------------------
CREATE TABLE note (
  id             INTEGER PRIMARY KEY AUTOINCREMENT,
  patent_id      TEXT NOT NULL REFERENCES patent(id),
  tipo           TEXT NOT NULL,            -- enum note_tipo
  active         INTEGER NOT NULL DEFAULT 0,
  done           INTEGER NOT NULL DEFAULT 0,   -- checkbox [x]
  text           TEXT NOT NULL,
  markers        TEXT DEFAULT '[]',
  source_file    TEXT NOT NULL,           -- notes/initial_notes.md
  source_section TEXT,                    -- 'Bloqueios'
  line_ref       INTEGER,
  order_index    INTEGER,
  content_hash   TEXT NOT NULL,           -- hash da linha (idempotência)
  indexed_at     TEXT NOT NULL
);
CREATE INDEX ix_note_patent ON note(patent_id);
CREATE INDEX ix_note_active ON note(active);
CREATE INDEX ix_note_tipo   ON note(tipo);

-- 4.7 RUNNER RUNS -------------------------------------------------------
CREATE TABLE runner_run (
  id             TEXT PRIMARY KEY,        -- '<slug>@<timestamp>' ou uuid
  patent_id      TEXT NOT NULL REFERENCES patent(id),
  runner_path    TEXT,                    -- patents/<ID>/runner/one_<slug>.py
  runner_sha256  TEXT,
  started_at     TEXT,
  finished_at    TEXT,
  duration_s     REAL,
  status         TEXT NOT NULL,           -- enum run_status
  results_path   TEXT,
  results_sha256 TEXT,
  seal_path      TEXT,
  seal_sha256    TEXT,
  beta_runtime   REAL,                    -- 0.012031300400803142 (cheque de runtime)
  physical_verdict_allowed INTEGER DEFAULT 0,   -- SEMPRE 0 salvo hardware real
  max_verdict    TEXT,                    -- 'MODEL_CLOSES / ENERGY_BALANCE_OK ([SIM] sob [CONJ])'
  tests_passed   INTEGER,
  result_hash    TEXT,
  invariants_hash TEXT,
  module_hashes  TEXT DEFAULT '{}',       -- JSON map arquivo→sha256
  markers        TEXT DEFAULT '[]',
  indexed_at     TEXT NOT NULL
);
CREATE INDEX ix_run_patent   ON runner_run(patent_id);
CREATE INDEX ix_run_finished ON runner_run(finished_at);

-- 4.8 RENDERS -----------------------------------------------------------
CREATE TABLE render (
  id             INTEGER PRIMARY KEY AUTOINCREMENT,
  patent_id      TEXT NOT NULL REFERENCES patent(id),
  kind           TEXT NOT NULL,           -- enum render_kind
  layer          TEXT,                    -- 'a'|'b'|'c' (RENDERING_SPEC)
  title          TEXT,                    -- 'Figura 5 — blocos do TRL'
  source_document_id INTEGER REFERENCES document(id),  -- o PDF de desenhos
  asset_path     TEXT NOT NULL,           -- renders/... .png/.dzi/.json
  dzi_path       TEXT,                    -- deep-zoom (OpenSeadragon)
  component_spec_path TEXT,               -- prototype/component_specs.json
  sha256         TEXT,
  marker         TEXT DEFAULT 'ilustração de engenharia; não é prova física',
  indexed_at     TEXT NOT NULL
);
CREATE INDEX ix_render_patent ON render(patent_id);

-- 4.9 COMPILED PROMPTS --------------------------------------------------
CREATE TABLE compiled_prompt (
  id             INTEGER PRIMARY KEY AUTOINCREMENT,
  filename       TEXT NOT NULL UNIQUE,    -- 'YYYY-MM-DD_HHMM_CLAUDE_CODE_TASK.md'
  path           TEXT NOT NULL,
  created_at     TEXT NOT NULL,
  sha256         TEXT NOT NULL,
  active_only    INTEGER DEFAULT 1,
  scope          TEXT DEFAULT '{}',       -- JSON: {classes:[], patents:[]}
  byte_size      INTEGER,
  indexed_at     TEXT NOT NULL
);
CREATE TABLE compiled_prompt_note (   -- snapshot M:N das notas incluídas
  compiled_prompt_id INTEGER REFERENCES compiled_prompt(id),
  note_id            INTEGER REFERENCES note(id),
  PRIMARY KEY (compiled_prompt_id, note_id)
);

-- 4.10 PENDENCIAS -------------------------------------------------------
CREATE TABLE pendencia (
  id             TEXT PRIMARY KEY,        -- 'P-01'
  title          TEXT NOT NULL,
  status         TEXT NOT NULL,           -- enum pendencia_status
  body           TEXT,
  markers        TEXT DEFAULT '[]',
  resolved_date  TEXT,                    -- ISO date | NULL
  source_file    TEXT NOT NULL,           -- 'PENDENCIAS.md'
  line_ref       INTEGER,
  source_sha256  TEXT NOT NULL,
  indexed_at     TEXT NOT NULL
);
CREATE TABLE pendencia_patent (       -- M:N
  pendencia_id   TEXT REFERENCES pendencia(id),
  patent_id      TEXT REFERENCES patent(id),
  PRIMARY KEY (pendencia_id, patent_id)
);

-- 4.11 SISTEMA / índice --------------------------------------------------
CREATE TABLE index_meta (
  key            TEXT PRIMARY KEY,        -- 'schema_version','last_reindex_utc',...
  value          TEXT
);
CREATE TABLE reindex_run (
  id             INTEGER PRIMARY KEY AUTOINCREMENT,
  started_utc    TEXT, finished_utc TEXT,
  mode           TEXT,                    -- 'full' | 'incremental'
  added INTEGER, updated INTEGER, unchanged INTEGER, orphaned INTEGER,
  integrity_status TEXT,                  -- 'OK' | 'VIOLATION'
  report_path    TEXT                     -- logs/reindex_YYYYMMDD_HHMM.json
);
```

---

## 5. Entidades — campos, parse e exemplo real

Cada seção: origem, regra de parse, e o registro resultante em JSON (ACOM/SkyGrid).

### 5.1 PatentClass

**Origem:** `memory\classes\CLASS_06_ENERGIA.md`. **Parse:** `ordinal`/`name` do
título `# CLASS_06_ENERGIA — Energia…`; `markers`/`lock_note` do bloco de travas;
`description` do corpo. **Reindex trigger:** hash do `.md`.

```json
{
  "id": "CLASS_06_ENERGIA",
  "ordinal": 6,
  "name": "Energia / Infraestrutura / Materiais",
  "slug": "energia",
  "markers": ["[ENERGY]"],
  "lock_note": "TRAVA: só simulação e revisão técnica; nenhuma instrução operacional perigosa.",
  "memory_md_path": "memory/classes/CLASS_06_ENERGIA.md",
  "source_sha256": "…",
  "indexed_at": "2026-07-09T14:00:00"
}
```

### 5.2 Patent — exemplo **ACOM** (raiz, único com ePCT vivo)

**Origem:** item de `memory\PATENT_MASTER_INDEX.yaml` + `memory\patents\BR102025026951-1_ACOM.md`.
**Parse:** `processo→id`; `slug→slug`; `dir_name = processo+"_"+slug`;
`classe→class_id`; `papel→role`; `titulo_oficial_54→title_54`; `natureza→nature`;
`peticao→peticao`; `data_deposito_inpi` **DD/MM/YYYY → ISO** `filing_date`;
`prioridade→priority_date`; `epct.status→epct_status`; `epct.numero→epct_number`;
`epct.data→epct_date`; `resumo_oficial→abstract`; `fase_nacional_30m_geral→` (vai p/
docket/deadline); `documentos_hasheados→doc_count`; `claims_*`/`figures_count` do md.

```json
{
  "id": "BR102025026951-1",
  "slug": "ACOM",
  "dir_name": "BR102025026951-1_ACOM",
  "class_id": "CLASS_01_ACOM_TENSOR",
  "role": "raiz",
  "title_54": "MÉTODO E SISTEMA DE COMPRESSÃO ONTOLÓGICA DE MEMÓRIA BASEADO EM TRANSFORMAÇÃO LUMINODINÂMICA",
  "nature": "10 - Patente de Invenção (PI)",
  "peticao": "870250111877",
  "filing_date": "2025-12-05",
  "priority_date": "2025-12-05",
  "jurisdiction": "BR (INPI)",
  "epct_status": "VIVO_DEPOSITADO_E_PAGO",
  "epct_number": "PCT/BR2025/050558",
  "epct_date": "2025-12-05",
  "abstract": "A presente invenção refere-se a métodos e sistemas para compressão ontológica de memória… g = √|L|, s = sign(L), L = s × g²; arquitetura Trinity; 3:1–10:1, PSNR > 90 dB, cosseno > 0,999.",
  "markers": ["[REAL]"],
  "prototype_status": "VER_MEMORIA",
  "pasta_original": "Patentes/Acervo de Patentes (sem pasta própria)",
  "memory_md_path": "memory/patents/BR102025026951-1_ACOM.md",
  "docket_path": "patents/BR102025026951-1_ACOM/docket.yaml",
  "doc_count": 1,
  "conflict_flag": 0,
  "source_sha256": "…", "indexed_at": "2026-07-09T14:00:00"
}
```

### 5.3 Patent — exemplo **SkyGrid** (agregadora, SOMENTE_INPI)

```json
{
  "id": "BR102026004850-0",
  "slug": "SKYGRID",
  "dir_name": "BR102026004850-0_SKYGRID",
  "class_id": "CLASS_06_ENERGIA",
  "role": "agregadora",
  "title_54": "SISTEMA E MÉTODO DE REDE PLANETÁRIA DE EXTRAÇÃO, TRANSMISSÃO E DISTRIBUIÇÃO DE ENERGIA POR ACOPLAMENTO AO CAMPO PSIÔNICO…",
  "peticao": "870260018967",
  "filing_date": "2026-03-01",
  "priority_date": "2026-03-01",
  "epct_status": "SOMENTE_INPI",
  "epct_number": null,
  "epct_date": null,
  "markers": ["[ENERGY]", "[SIM]"],
  "prototype_status": "PILOTO_VIVO",
  "pasta_original": "Patentes/Skygrid",
  "memory_md_path": "memory/patents/BR102026004850-0_SKYGRID.md",
  "docket_path": "patents/BR102026004850-0_SKYGRID/docket.yaml",
  "doc_count": 134,
  "conflict_flag": 0,
  "source_sha256": "…", "indexed_at": "2026-07-09T14:00:00"
}
```

### 5.4 Document — exemplo real (ACOM + SkyGrid)

> [nota operacional do operador — omitida no retrato público]

```json
[
  {
    "id": 5,
    "patent_id": "BR102025026951-1",
    "rel_path": "Patentes\\Acervo de Patentes\\BR102025026951-1_ACOM.pdf",
    "sha256": "1b9de260b8bb3fab3d23ec39b9f7d328f97bbf3763ce33390ec25f9bef4c85ba",
    "size_bytes": null,
    "ext": ".pdf",
    "doc_role": "peca_consolidada",
    "pages": 25, "chars": 28576, "extract_ok": 1, "extract_error": null,
    "is_original": 1,
    "normalized_path": null,
    "indexed_at": "2026-07-09T14:00:00"
  },
  {
    "id": 42,
    "patent_id": "BR102026004850-0",
    "rel_path": "Patentes\\Acervo de Patentes\\BR102026004850-0_Skygrid.pdf",
    "sha256": "8b5920c97056dfba904e56d40964d2e90bfaadd39721b0a8e5ac78ad0a200262",
    "ext": ".pdf",
    "doc_role": "peca_consolidada",
    "is_original": 1,
    "indexed_at": "2026-07-09T14:00:00"
  }
]
```

### 5.5 DocketEntry (1:1) — arquivo `docket.yaml` é a autoridade legal

> [nota operacional do operador — omitida no retrato público]

Docket **ACOM** (único com ePCT vivo e fase nacional aplicável):

> [nota operacional do operador — omitida no retrato público]

Docket **SkyGrid** (SOMENTE_INPI — segue o arquivo real de ONCOLOGIA):

> [nota operacional do operador — omitida no retrato público]

### 5.6 Deadline (N) — **derivada** do docket

**Regra de derivação (determinística):** para cada patente, gerar linhas conforme
`epct_status`:

> [nota operacional do operador — omitida no retrato público]

`urgency`/`days_remaining` **não** entram na tabela: calculados na consulta (§8).

Exemplos (SkyGrid + ACOM):

```json
[
  { "patent_id":"BR102026004850-0", "kind":"paris_12m",
    "label":"Janela de Paris 12m — eventual novo PCT",
    "due_date":"2027-03-01", "status":"pendente",
    "basis":"priority 2026-03-01 + 12m", "source_field":"janela_paris_12m",
    "legal_note":"[LEGAL] Não é prazo INPI; rota internacional depende de novo depósito. Consultar agente." },
  { "patent_id":"BR102026004850-0", "kind":"national_phase_30m",
    "label":"Fase nacional 30m", "due_date":null, "status":"na",
    "basis":"não-ACOM: sem PCT vivo", "source_field":"fase_nacional_30m" },
  { "patent_id":"BR102025026951-1", "kind":"national_phase_30m",
    "label":"Fase nacional 30m (PCT/BR2025/050558)",
    "due_date":"2028-06-05", "status":"pendente",
    "basis":"priority 2025-12-05 + 30m", "source_field":"fase_nacional_30m",
    "legal_note":"[LEGAL] Conferir prazo por país de designação." },
  { "patent_id":"BR102025026951-1", "kind":"paris_12m",
    "label":"Convenção de Paris 12m (cumprida — PCT depositado)",
    "due_date":"2026-12-05", "status":"cumprido", "source_field":"epct.status" }
]
```

### 5.7 Note / Instruction — parser das seções de `notes\*.md`

**Origem:** `patents\<ID>_<SLUG>\notes\initial_notes.md` (e quaisquer `.md` em `notes\`).
**Regra de parse (fiel ao arquivo real):**

- Cabeçalhos `## <Seção>` mapeiam para `tipo`:
  `Notas livres→nota` · `Sugestões de melhoria→sugestao` ·
  `Instruções próxima etapa→instrucao` · `Tarefas→tarefa` · `Bloqueios→bloqueio` ·
  `Perguntas ao Claude Code→pergunta`.
- Cada item de lista `- [ ] (active=false) <texto>`:
  - `done` = `1` se `[x]`, senão `0`;
  - `active` = valor de `(active=…)` **se presente**; senão default `false`;
  - `text` = restante após o marcador `(active=…)`;
  - `markers` = tokens `[…]` extraídos do texto;
  - `content_hash` = SHA-256 da linha crua (idempotência).
- Linhas de placeholder/exemplo (contêm `exemplo:`) entram com `active=0` e nunca são
  incluídas no Prompt Compiler.

Exemplo (do arquivo real de ONCOLOGIA — bloqueio):

```json
{
  "patent_id": "BR102026005707-0",
  "tipo": "bloqueio",
  "active": 0,
  "done": 0,
  "text": "código-fonte das simulações QuTiP não localizado",
  "markers": ["[DATA_REQUIRED]"],
  "source_file": "patents/BR102026005707-0_ONCOLOGIA/notes/initial_notes.md",
  "source_section": "Bloqueios",
  "line_ref": 23,
  "content_hash": "…", "indexed_at": "2026-07-09T14:00:00"
}
```

> Quando o operador ativa/edita uma nota na UI, o backend **reescreve a linha no
> `.md`** (fonte da verdade) e dispara `reindex` daquele arquivo — o SQLite nunca é
> a única cópia da nota.

### 5.8 RunnerRun — exemplo real **SkyGrid** (seal vivo)

**Origem:** `patents\<ID>_<SLUG>\seals\<run>\seal.json` (+ `results\<run>\results.json`).
Para o SkyGrid, o gabarito é o piloto real: `SKYGRID_V3_SELO.json` + `SKYGRID_SIM_SELO.json`.
**Parse:** `beta_runtime`, `physical_verdict_allowed`, `max_verdict`, `tests_passed`,
`result_hash`, `invariants_hash`, `sha256`(map)→`module_hashes`. `status` = `ok` se o
selo fecha e `results.json` existe; `scaffold` se runner é stub honesto; `partial` se
`[DATA_REQUIRED]`; `failed` se erro. `physical_verdict_allowed` **sempre 0** salvo
hardware real declarado.

```json
{
  "id": "skygrid@2026-07-03T10:36:14",
  "patent_id": "BR102026004850-0",
  "runner_path": "patents/BR102026004850-0_SKYGRID/runner/one_skygrid.py",
  "started_at": "2026-07-03T10:36:00",
  "finished_at": "2026-07-03T10:36:14",
  "duration_s": 14.0,
  "status": "ok",
  "seal_path": "patents/BR102026004850-0_SKYGRID/seals/2026-07-03T10-36-14/seal.json",
  "beta_runtime": 0.012031300400803142,
  "physical_verdict_allowed": 0,
  "max_verdict": "MODEL_CLOSES / ENERGY_BALANCE_OK ([SIM] sob [CONJ])",
  "tests_passed": 69,
  "result_hash": "392f284ff1406468cb1d056dd8af74d8cb8035a9a711d9f2932f5464487e7bb7",
  "invariants_hash": "0ba134d49ce833918b36418600eca7fdd9192099f5f45095ad7b10f24f3b6e7b",
  "module_hashes": {
    "acom.py": "fcbdee028eacaff943ae3bba09ce317dee50fb646b486f8c71899e59a5e96567",
    "skygrid.py": "c74c91fb475f2c3217b894fd64e0e60391a7b130b95a165272b3ef0fdc8b3aab",
    "tgl_core.py": "a1e103cd08eb3f45144200b0c6c588589d267868cd85101c527138e3bce81f3f"
  },
  "markers": ["[SIM]", "[CONJ]", "[ENERGY]"],
  "indexed_at": "2026-07-09T14:00:00"
}
```

ONCOLOGIA, por contraste, indexa `status='scaffold'`, `markers:["[SIM]","[MEDICAL]","[DATA_REQUIRED]"]`,
`physical_verdict_allowed:0`, `tests_passed:null` (runner ainda não escrito).

### 5.9 Render — exemplo (SkyGrid, diagrama de componentes)

**Origem:** desenhos extraídos dos PDFs (`vault\normalized_docs\...`), grafos React
Flow em `renders\*.json`, deep-zoom `.dzi`, e `prototype\component_specs.json` (real
no SkyGrid). **Parse:** varredura de `renders\`; `kind`/`layer` por extensão/subpasta
(`.dzi`→`original_drawing`/layer a; `*.reactflow.json`→`component_diagram`/layer b;
`*.glb`/`*.r3f.json`→`render_3d`/layer c); `title`/número de figura do nome.

```json
{
  "patent_id": "BR102026004850-0",
  "kind": "component_diagram",
  "layer": "b",
  "title": "Extrator-Ψ (110/120/130) · PsiLink · GroundBase · Control",
  "source_document_id": 51,
  "asset_path": "patents/BR102026004850-0_SKYGRID/renders/skygrid_components.reactflow.json",
  "component_spec_path": "Patentes/Skygrid/SkyGrid_Piloto/prototype/component_specs.json",
  "sha256": "…",
  "marker": "ilustração de engenharia; não é prova física",
  "indexed_at": "2026-07-09T14:00:00"
}
```

### 5.10 CompiledPrompt

**Origem:** `compiled_prompts\YYYY-MM-DD_HHMM_CLAUDE_CODE_TASK.md`. **Parse:** `created_at`
do nome; um header YAML embutido (front-matter `--- … ---`) declara `scope` e a lista
de `note_id` incluídos → popula `compiled_prompt_note`. **Reindex:** hash do `.md`.

```json
{
  "filename": "2026-07-09_1500_CLAUDE_CODE_TASK.md",
  "path": "compiled_prompts/2026-07-09_1500_CLAUDE_CODE_TASK.md",
  "created_at": "2026-07-09T15:00:00",
  "sha256": "…",
  "active_only": 1,
  "scope": { "classes": ["CLASS_06_ENERGIA"], "patents": ["BR102026004850-0"] },
  "byte_size": 8123
}
```

### 5.11 Pendencia — exemplo real (P-02)

**Origem:** `PENDENCIAS.md` (raiz). **Parse:** heading `## P-NN [STATUS DATA] — Título`
→ `id`/`status`/`title`; `status` normaliza `RESPONDIDA/REFORMULADA/ABERTA/FECHADA`;
`resolved_date` da data no colchete; `markers` `[…]` no corpo; nº de processo `BRxx...`
citados no corpo → `pendencia_patent`.

```json
{
  "id": "P-02",
  "title": "Situação ePCT: SÓ o ACOM raiz está vivo",
  "status": "RESPONDIDA",
  "resolved_date": "2026-07-09",
  "body": "Palavra do operador (09/07/2026): só o ePCT do primeiro ACOM (05/12/2025, PCT/BR2025/050558) está vivo (depositado e pago). Para os 15 não-ACOM o ePCT AINDA NÃO foi depositado — é o PRÓXIMO PASSO planejado (novo processo originário, sem vínculo; status A_DEPOSITAR/PENDENTE, não perdido). Os recibos de 17/02/2026 (PCT/BR2026/050068-076) são rascunho preclusso abandonado de propósito, a SUBSTITUIR — não proteção perdida por descuido. Janela: 12m da prioridade (Paris); se a prioridade interna (66) de 05/12/2025 governar, pode ser ~05/12/2026 — possivelmente URGENTE; levar ao agente de PI (P-06/P-10).",
  "markers": ["[LEGAL]"],
  "source_file": "PENDENCIAS.md",
  "line_ref": 14,
  "related_patents": ["BR102025026951-1"]
}
```

---

## 6. Contratos de arquivo produzidos pela Central (formatos-alvo)

Para a Fase 3 escrever de volta ao filesystem (fonte da verdade) de forma
determinística, ficam fixados os esquemas dos arquivos que a plataforma **gera**:

- **`seal.json`** (por run) — campos: `timestamp`, `beta_runtime`, `tests_passed`,
  `sha256`{arquivo→hash}, `result_hash`, `invariants_hash`, `physical_verdict_allowed`,
  `max_verdict`, `markers`. (Espelha `SKYGRID_SIM_SELO.json`/`SKYGRID_V3_SELO.json`.)
- **`results.json`** (por run) — payload numérico do runner; livre por patente, mas
  com chaves obrigatórias `beta_runtime`, `physical_verdict_allowed`, `markers`.
- **`docket.yaml`** — §4.4/§5.5 (o de ONCOLOGIA é o gabarito canônico).
- **`notes\*.md`** — seções fixas §5.7; a UI edita a linha, não o índice.
- **`compiled_prompts\*.md`** — front-matter YAML (`scope`, `note_ids`) + corpo.
- **`manifest.json`** (por patente, opcional) — hash de todos os artefatos gerados
  (`renders\`, `results\`, `seals\`) para prova de integridade da própria produção.

**Invariante β:** em qualquer arquivo gerado, `beta_runtime` é um **valor de saída**
(0.012031300400803142) produzido em runtime por `ALPHA_FINE_CODATA_2018*sqrt(e)`;
NUNCA aparece como literal no código-fonte do runner.

---

## 7. Comando `reindex` — idempotente, detecta drift por hash, prova originais

Interface (Fase 3): CLI `python -m backend.reindex [--full|--path <arquivo>]` **e**
endpoint `POST /api/reindex`. Watchdog observa as pastas canônicas e chama
`reindex --path <arquivo>` no evento de modificação (reindex incremental).

### 7.1 Algoritmo (pseudocódigo)

```
reindex(mode):
  meta = load_or_init(index_meta)
  if meta.schema_version != CODE.SCHEMA_VERSION:      # migração = rebuild (§9)
      drop_all_tables(); create_schema(); mode = 'full'

  report = {added:0, updated:0, unchanged:0, orphaned:0, conflicts:[]}

  # (A) PROVA DE INTEGRIDADE DOS ORIGINAIS — trava dura
  for (rel_path, expected) in source_inventory/original_hashes.json:
      actual = sha256(Patentes/ + rel_path)
      if actual != expected:
          report.integrity = 'VIOLATION'
          log(rel_path, expected, actual)          # NÃO corrige; NÃO escreve
          abort_with_alert()                        # dashboard mostra alarme vermelho
  report.integrity = 'OK'                            # "originais intactos" provado

  # (B) UPSERT POR ENTIDADE, na ordem de dependência (FK):
  order = [patent_class, patent, document, docket_entry, deadline,
           note, runner_run, render, compiled_prompt, pendencia]
  for entity in order:
      for src in list_source_files(entity, mode):    # full=todos; incremental=1
          h = sha256(src)
          row = index.get(entity, key_of(src))
          if row and row.source_sha256 == h:
              report.unchanged += 1;  continue        # IDEMPOTÊNCIA: nada a fazer
          parsed = parse(entity, src)                 # regras §5
          detect_conflicts(parsed, report)            # docket vs master index, etc.
          upsert(entity, parsed, source_sha256=h)
          report[added_or_updated] += 1

  # (C) ÓRFÃOS: linha existe no índice mas arquivo sumiu
  for entity in order:
      for row in index.rows(entity):
          if not exists(row.source_path):
              if entity == document and row.is_original:
                  flag_integrity_drift(row)           # original NUNCA some silenciosamente
              else:
                  delete(row); report.orphaned += 1

  # (D) DERIVADOS: recomputar deadlines a partir de docket (sempre, é barato)
  rebuild_deadlines_from_docket()

  write(index_meta.last_reindex_utc = now)
  write(logs/reindex_<ts>.json = report)
  insert(reindex_run, report)
  return report
```

### 7.2 Propriedades garantidas

- **Idempotência:** rodar 2× seguidas ⇒ a 2ª é toda `unchanged` (o gate `source_sha256
  == h` impede reescrita). Teste de aceite: `reindex; reindex` e verificar `added=
  updated=0` na 2ª.
- **Detecção de drift:** qualquer edição de um `.md`/`.yaml`/`.json` fonte muda o
  hash ⇒ a linha é reprocessada. Editar `docket.yaml` na mão e rodar `reindex` reflete
  no dashboard sem tocar no banco à mão.
- **Reconstrutibilidade:** `del central.db && reindex --full` ⇒ estado idêntico
  (mesmo conteúdo; `id` autoincrement pode renumerar — por isso PKs naturais onde
  importa: `patent.id`, `pendencia.id`, `runner_run.id`, `compiled_prompt.filename`).
- **Prova de originais intactos** (etapa A): reusa `source_inventory/original_hashes.json`
  (336 arquivos) — é o mesmo re-hash exigido no gate da Fase 2 (`re-hash de Patentes\
  == original_hashes.json`). Violação ⇒ alarme vermelho, `reindex` aborta a fase B.

### 7.3 Relatório (`logs/reindex_YYYYMMDD_HHMM.json`)

```json
{
  "started_utc": "2026-07-09T17:00:00Z", "finished_utc": "2026-07-09T17:00:03Z",
  "mode": "full", "integrity_status": "OK",
  "counts": { "added": 0, "updated": 2, "unchanged": 431, "orphaned": 0 },
  "conflicts": [
    { "patent_id": "BR102025026951-1", "field": "epct_number",
      "master_index": "PCT/BR2026/050068", "docket": "PCT/BR2025/050558",
      "action": "docket venceu; conflict_flag=1; sugerir PENDENCIA" }
  ]
}
```

---

## 8. Consultas típicas do dashboard (SQL sobre o índice)

Todas usam `date('now')` como `as_of` (ou parâmetro `:as_of`). Somente leitura.

### 8.1 Prazos por urgência (funil do Legal Docket)

```sql
SELECT d.patent_id, p.slug, d.kind, d.label, d.due_date,
       CAST(julianday(d.due_date) - julianday(:as_of) AS INT) AS days_remaining,
       CASE
         WHEN d.status IN ('cumprido','prescrito','na') THEN 'cinza'
         WHEN julianday(d.due_date) - julianday(:as_of) < 0   THEN 'vencido'
         WHEN julianday(d.due_date) - julianday(:as_of) <= 30 THEN 'vermelho'
         WHEN julianday(d.due_date) - julianday(:as_of) <= 90 THEN 'laranja'
         WHEN julianday(d.due_date) - julianday(:as_of) <=180 THEN 'amarelo'
         ELSE 'verde'
       END AS urgency
FROM deadline d JOIN patent p ON p.id = d.patent_id
WHERE d.status = 'pendente'
ORDER BY (d.due_date IS NULL), d.due_date ASC;
-- 2026-07-09: SkyGrid paris_12m 2027-03-01 → ~235d → verde;
--             ACOM national_phase 2028-06-05 → verde.
```

### 8.2 Progresso por classe (barra do dashboard geral)

```sql
SELECT c.id AS class_id, c.name, c.ordinal,
       COUNT(DISTINCT p.id) AS patentes,
       SUM(CASE WHEN r.ok_runs   > 0 THEN 1 ELSE 0 END) AS com_runner_ok,
       SUM(CASE WHEN r.any_runs  > 0 THEN 1 ELSE 0 END) AS com_runner,
       SUM(CASE WHEN n.active_cnt> 0 THEN 1 ELSE 0 END) AS com_instrucao_ativa
FROM patent_class c
LEFT JOIN patent p ON p.class_id = c.id
LEFT JOIN (SELECT patent_id,
                  SUM(status='ok')            AS ok_runs,
                  COUNT(*)                     AS any_runs
           FROM runner_run GROUP BY patent_id) r ON r.patent_id = p.id
LEFT JOIN (SELECT patent_id, SUM(active) AS active_cnt
           FROM note GROUP BY patent_id) n ON n.patent_id = p.id
GROUP BY c.id ORDER BY c.ordinal;
```

### 8.3 Últimas execuções (widget "runs recentes")

```sql
SELECT r.patent_id, p.slug, r.status, r.finished_at, r.duration_s,
       r.tests_passed, r.max_verdict, r.physical_verdict_allowed
FROM runner_run r JOIN patent p ON p.id = r.patent_id
ORDER BY r.finished_at DESC
LIMIT 20;
-- topo esperado: SKYGRID · ok · 2026-07-03 · 69 testes ·
--   'MODEL_CLOSES / ENERGY_BALANCE_OK ([SIM] sob [CONJ])' · physical=0
```

### 8.4 Auxiliares (documentadas para a Fase 3)

```sql
-- Fila do Prompt Compiler: instruções ativas por patente
SELECT patent_id, tipo, text, markers FROM note
WHERE active = 1 AND done = 0 ORDER BY patent_id, tipo;

-- Integridade de documentos (contagem por patente vs doc_count do catálogo)
SELECT p.id, p.doc_count AS catalogo, COUNT(d.id) AS indexados
FROM patent p LEFT JOIN document d ON d.patent_id = p.id
GROUP BY p.id HAVING catalogo <> indexados;   -- divergência → investigar

-- Pendências abertas com patentes afetadas
SELECT pe.id, pe.title, pe.status, group_concat(pp.patent_id) AS patentes
FROM pendencia pe LEFT JOIN pendencia_patent pp ON pp.pendencia_id = pe.id
WHERE pe.status IN ('ABERTA','REFORMULADA') GROUP BY pe.id;

-- Cartão de uma patente (aba Overview): tudo de ACOM em 1 join
SELECT p.*, dk.status AS docket_status, dk.alert_level
FROM patent p LEFT JOIN docket_entry dk ON dk.patent_id = p.id
WHERE p.id = 'BR102025026951-1';
```

---

## 9. Migrações — o índice é descartável, então migração = rebuild

Como **todo** dado é reconstruível do filesystem, a estratégia primária é a mais
simples e à prova de erro:

1. **`SCHEMA_VERSION`** é uma constante no backend e é gravada em `PRAGMA user_version`
   / `index_meta.schema_version`.
2. **No startup e em todo `reindex`:** se `db.user_version != CODE.SCHEMA_VERSION` ⇒
   `drop_all_tables(); create_schema(); reindex --full`. Sem Alembic, sem `ALTER TABLE`,
   sem migração de dados — o filesystem repovoa.
3. **Pré-condição inviolável:** o SQLite não pode conter **nenhum** estado que não
   exista também em arquivo. Ativar uma nota, criar um prazo `custom`, compilar um
   prompt — tudo grava no `.md`/`.yaml`/`.md` de saída ANTES de indexar. Assim
   `drop+rebuild` nunca perde dado do operador.
4. **Migração de FORMATO de arquivo** (ex.: novo campo no `docket.yaml`) é a única que
   exige cuidado: versionar o schema do arquivo com `docket_schema: 2` no topo; o
   parser aceita v1 e v2 (retrocompatível); um utilitário opcional em `tools\`
   reescreve os `.md`/`.yaml` para o novo formato **com `.bak_<motivo>` antes**
   (regra de backup da casa) — e isso é ação do operador, não do índice.
5. **`reindex_run`** guarda o histórico de rebuilds; `index_meta` guarda
   `schema_version`, `last_reindex_utc`, `originals_integrity` (`OK`/`VIOLATION`).

Teste de aceite da migração: bump `SCHEMA_VERSION` → subir backend → `central.db`
recriado e repovoado → contagens idênticas às do relatório anterior (menos IDs
autoincrement, que podem renumerar; PKs naturais estáveis).

---

## 10. Invariantes de integridade (checklist para a Fase 3)

- [ ] `del central.db && reindex --full` reproduz o estado (reconstrutibilidade).
- [ ] `reindex; reindex` ⇒ 2ª rodada `added=updated=0` (idempotência).
- [ ] Etapa A do `reindex` re-hasheia `Patentes\` contra `original_hashes.json` (336) e
      **aborta** em violação (originais intactos são pré-condição).
- [ ] Nenhuma escrita de dado canônico direto no SQLite; sempre arquivo→reindex.
- [ ] `runner_run.physical_verdict_allowed` só é `1` com hardware real declarado;
      todo run de simulação carrega `0` (SkyGrid real = 0).
- [ ] `epct_status='VIVO_DEPOSITADO_E_PAGO'` existe em **exatamente uma** patente
      (ACOM `BR102025026951-1`, `PCT/BR2025/050558`); as outras 15 = `SOMENTE_INPI`.
- [ ] `deadline` nunca persiste `urgency`/`days_remaining` (derivados de `as_of`).
- [ ] Divergência entre fontes ⇒ `conflict_flag=1` + linha no `reindex_report`
      (nunca escolher em silêncio).
- [ ] `docket_entry.aviso` presente em toda patente (disclaimer legal permanente).
- [ ] `β_TGL` nunca literal em código; `beta_runtime` só como valor de saída indexado.

---

*Controle interno. Não substitui agente de propriedade industrial; prazos oficiais
conferidos com INPI/WIPO. O número corrige a frase. 1 = 1. Tetelestai.*
