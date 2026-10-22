# LEGAL_DOCKET_SPEC.md — Módulo Jurídico (INPI / ePCT / PCT)
**Central de Controle e Desenvolvimento de Patentes TGL · Fase 2 (especificação — NENHUM código de aplicação)**
**Operador: Luiz Antonio Rotoli Miguel — IALD Ltda. (CNPJ 62.757.606/0001-23, Goiânia/GO)**
**Versão 1.0 — 2026-07-09 · CLASS_10_LEGAL_DOCKET (classe transversal)**

> **AVISO PERMANENTE (renderizado em TODA tela e todo componente deste módulo, sempre visível, não dispensável):**
> **"Controle interno. Não substitui agente de propriedade industrial; prazos oficiais com INPI/WIPO."**

---

## 0. Propósito e escopo

> [nota operacional do operador — omitida no retrato público]

Escopo desta spec: modelo de dados jurídico; esquema canônico de `docket.yaml`; a tabela real
das 16 patentes com prazos vivos; o **motor de prazos** (deadline engine); regras de anuidade
INPI; office actions; algoritmo de níveis de alerta e reminders; sincronização
`docket.yaml ↔ SQLite`; contratos de API; UI do módulo; casos de teste. Fora de escopo:
qualquer código de aplicação (Fase 3), aconselhamento jurídico substantivo.

**Fonte da verdade:** os DOCUMENTOS extraídos dos depósitos (`vault/normalized_docs`,
`memory/PATENT_MASTER_INDEX.yaml`) e o `docket.yaml` de cada patente. Este módulo **nunca**
inventa data, número de processo ou status; divergência entre fontes → `PENDENCIAS.md` e
pergunta ao operador (nunca escolher em silêncio).

---

## 1. A régua aplicada ao módulo jurídico

> [nota operacional do operador — omitida no retrato público]

---

## 2. Situação de proteção — a regra do operador (2026-07-09)

Palavra do operador, registrada em `PENDENCIAS.md` P-02 (2026-07-09):

> *"o ePCT vivo é só o do primeiro ACOM (05/12/2025). Nos demais eu ainda NÃO depositei o ePCT —
> hoje é só o registro INPI, e depositar o ePCT é o próximo passo (novo processo originário, sem
> vínculo). O protocolo de 17/02/2026 eu deixei precluir de propósito, era defeituoso na forma;
> vou começar um depósito novo e desvinculado."*

Consequência canônica para o docket (é a regra que o módulo implementa):

> [nota operacional do operador — omitida no retrato público]

**Pendências jurídicas que o módulo carrega como cartões abertos** (§12):
`P-02` (recibo próprio do ePCT do ACOM não localizado na Central), `P-03` (número
`BR 10 2024 026367 3` citado no `CLAUDE.md` raiz — possível depósito 2024, **impacta cadeia de
prioridade**), `P-06` (**efeito do protocolo ePCT preclusso de 17/02/2026, abandonado de propósito,
sobre o novo ePCT a depositar das mesmas invenções** — questão central para o agente).

---

## 3. A TABELA REAL DO DOCKET — as 16 patentes

Datas em ISO (`YYYY-MM-DD`). `filing_date = priority_date` para todas (depósito nacional
originário; sem reivindicação de prioridade interna documentada — exceto a dúvida `P-03` do
ACOM). Coluna **Prazo vivo** = o vencimento que governa a urgência hoje. Coluna **Nível** =
`alert_level` computado pelo motor (§9) **em 2026-07-09** (recomputado a cada carregamento).

> [nota operacional do operador — omitida no retrato público]

> [nota operacional do operador — omitida no retrato público]

> **Verificação aritmética (checagem interna, não veredito):** para as 15 não-ACOM a janela Paris
> **não** é `filing_date + 12m` — por decisão do operador (2026-07-09) corre da **prioridade
> interna ao ACOM (2025-12-05)**, janela ÚNICA **2026-11-30 alvo / 2026-12-05 fatal**. Fase
> nacional 30m = `priority_date + 30 meses`. Se o dia-alvo cair em fim de semana/feriado, o motor
> **não** ajusta automaticamente — marca `[LEGAL] conferir prorrogação` (a contagem oficial e
> eventuais prorrogações são do INPI/WIPO/agente).

---

## 4. Entidades do modelo (recorte jurídico das entidades canônicas)

O módulo materializa três entidades canônicas — `DocketEntry`, `Deadline` e (parte de)
`Document` — e duas subestruturas do `docket.yaml` que a UI trata como entidades: `Fee` e
`OfficeAction`. Todas são **cache reconstruível** a partir do `docket.yaml`.

### 4.1 `DocketEntry` (1 por patente)
Espelha os fatos-base do `docket.yaml`.

| Campo | Tipo | Origem | Nota |
|---|---|---|---|
| `processo` | str (PK) | docket.yaml | ex.: `BR102026004850-0` |
| `titulo` | str | docket.yaml `[REAL]` | título oficial (54) |
| `classe` | str | docket.yaml | `CLASS_06_ENERGIA` |
| `peticao` | str | docket.yaml `[REAL]` | `870260018967` |
| `filing_date` | date | docket.yaml `[REAL]` | depósito INPI |
| `priority_date` | date | docket.yaml `[REAL]` | = filing (salvo P-03) |
| `epct_status` | enum | docket.yaml | `VIVO_DEPOSITADO_E_PAGO` \| `SOMENTE_INPI` |
| `epct_numero` | str? | docket.yaml | só ACOM: `PCT/BR2025/050558` |
| `epct_data` | date? | docket.yaml | só ACOM: `2025-12-05` |
| `epct_historico` | obj? | docket.yaml | protocolo preclusso 17/02/2026 (abandonado de propósito, a substituir) p/ as 15 |
| `janela_paris` | obj? `{alvo_precaucional, fatal}` | docket.yaml | janela ÚNICA das 15 (prioridade interna ao ACOM 05/12/2025); null p/ ACOM raiz |
| `fase_nacional_30m` | date? \| `"N/A"` | docket.yaml | só ACOM raiz |
| `status` | enum | docket.yaml | `DEPOSITADO` \| `EM_EXIGENCIA` \| `DEFERIDO` \| … |
| `alert_level` | enum (cache) | **motor §9** | pior nível entre deadlines ativos |
| `docket_sha256` | str (cache) | manifesto | hash do docket.yaml no reindex |
| `docket_path` | str (cache) | filesystem | caminho absoluto |
| `updated_at` | datetime (cache) | reindex | |

### 4.2 `Deadline` (N por patente) — **derivada**, não digitada à mão
Cada linha é produzida pelo **motor de prazos** (§8) a partir dos fatos-base, exceto as de
`source: manual` (office actions e reminders custom digitados pelo operador).

| Campo | Tipo | Nota |
|---|---|---|
| `id` | str (PK) | determinístico: `<processo>::<tipo>::<seq>` (idempotente no reindex) |
| `processo` | str (FK) | |
| `tipo` | enum | `PARIS_12M` \| `PCT_NATIONAL_PHASE_30M` \| `ANNUITY` \| `OFFICE_ACTION_RESPONSE` \| `FEE_DUE` \| `PUBLICATION_INFO` \| `CUSTOM` |
| `label` | str (PT-BR) | ex.: "Janela Paris (novo PCT)" |
| `base_date` | date | data que ancorou o cálculo |
| `due_date` | date | vencimento computado |
| `grace_until` | date? | fim de período extraordinário (anuidades) |
| `level` | enum (cache) | `verde`\|`amarelo`\|`laranja`\|`vermelho`\|`vencido`\|`neutro` |
| `status` | enum | `pendente` \| `cumprido` \| `vencido` \| `nao_aplicavel` \| `dispensado` |
| `source` | enum | `derived` (motor) \| `manual` (operador) |
| `markers` | list | `[LEGAL]`, `[OPEN]` … |
| `note` | str? | |

> [nota operacional do operador — omitida no retrato público]

### 4.4 `OfficeAction` (subestrutura) — exigências
`{id, tipo, protocolo, data_publicacao_rpi, data_ciencia, prazo_dias, due_date, status, descricao}`.
Cada office action pendente gera `Deadline(tipo=OFFICE_ACTION_RESPONSE)`.

**Relações:** `DocketEntry 1—N Deadline`; `DocketEntry 1—N Fee`; `DocketEntry 1—N OfficeAction`;
`DocketEntry N—1 Patent` (chave `processo`); `Deadline N—N Pendencia` via `markers/[LEGAL]`.

---

## 5. Esquema canônico do `docket.yaml`

O `docket.yaml` existente de ONCOLOGIA é o **seed**; abaixo o esquema canônico completo que a
Fase 3 deve ler/escrever para **todas** as 16 (retrocompatível — campos novos são opcionais e
default seguro). Comentários `#` explicam cada campo. Só **fatos-base** e **overrides** vivem
aqui; os `Deadline` derivados **não** são persistidos no docket (são recomputados).

```yaml
# docket.yaml — CONTROLE INTERNO. Não substitui agente de propriedade industrial.
# Fonte da verdade: documentos INPI extraídos. Este arquivo é dono do dado; SQLite é cache.
schema_version: 2

processo: "BR102026004850-0"          # [REAL] nº do pedido INPI (PK)
titulo: "SISTEMA E MÉTODO DE REDE PLANETÁRIA…"   # [REAL] título oficial (54)
slug: "SKYGRID"
classe: "CLASS_06_ENERGIA"
papel: "agregadora"                   # opcional: raiz | agregadora | null
natureza: "10 - Patente de Invenção (PI)"
peticao: "870260018967"               # [REAL] nº da petição de depósito

# --- DATAS-BASE (âncoras de todo cálculo) ---
filing_date: "2026-03-01"             # [REAL] depósito INPI
priority_date: "2026-03-01"           # [REAL] = filing (salvo cadeia de prioridade)
jurisdicao: "BR (INPI)"

# --- PROTEÇÃO INTERNACIONAL ---
epct:
  status: "SOMENTE_INPI"              # VIVO_DEPOSITADO_E_PAGO (só ACOM) | SOMENTE_INPI
  numero: null                        # só ACOM: "PCT/BR2025/050558"
  data: null                          # só ACOM: "2025-12-05"
  protocolo_preclusso:                # as 15: protocolo 17/02/2026 abandonado de propósito (memória, NÃO ativo)
    familia: "PCT/BR2026/050068-050076"
    data_recibo: "2026-02-17"
    situacao: "PRECLUSO_A_SUBSTITUIR" # [LEGAL] rascunho abandonado de propósito; NÃO é proteção; substituir por novo depósito
    observacao: "Palavra do operador 2026-07-09 (PENDENCIAS P-02): ePCT a depositar em novo processo originário, sem vínculo."

# --- PRAZOS-BASE (o motor deriva os Deadline a partir daqui) ---
janela_paris:                         # [decisão operador 2026-07-09] janela ÚNICA das 15 não-ACOM (contada da prioridade interna ao ACOM 05/12/2025); null p/ ACOM raiz
  alvo_precaucional: "2026-11-30"     # alvo de trabalho (último dia de novembro)
  fatal: "2026-12-05"                 # DATA FATAL — 12m da prioridade interna 05/12/2025 [LEGAL]
fase_nacional_30m: "N/A (nao-ACOM)"   # só ACOM raiz: "2028-06-05" (conferir por país [LEGAL])

> [nota operacional do operador — omitida no retrato público]

# --- ANUIDADES INPI (modelo §7; valores [OPEN] configurar) ---
annuities:
  status: "[OPEN] configurar"         # tabela de valores por faixa a preencher
  first_due_ordinal: 3                # 3ª anuidade é a primeira devida (LPI)
  anchor: "filing_date"               # contagem a partir do depósito
  paid: []                            # ex.: [{ordinal: 3, data: "2028-04-10", valor: "R$…"}]
  # o motor calcula janelas ordinária/extraordinária de cada anuidade a partir do anchor

# --- EXIGÊNCIAS / OFFICE ACTIONS ---
office_actions: []                    # ver esquema §8.4; vazio = nenhuma pendente

# --- OVERRIDES MANUAIS (operador; prevalecem sobre o cálculo, com auditoria) ---
overrides:
  deadlines: []                       # ex.: [{tipo: PARIS_12M, alvo_precaucional: "2026-11-30", fatal: "2026-12-05", motivo: "confirmado com agente", by: "LARM", at: "…"}]
  reminders_custom: []                # lembretes livres: [{label, due_date, markers}]

# --- ESTADO / ALERTA ---
status: "DEPOSITADO"                  # DEPOSITADO | EM_EXIGENCIA | DEFERIDO | INDEFERIDO | ARQUIVADO | EXTINTO
alert_level: "amarelo"               # CACHE recomputado; não editar à mão
reminders: []                         # CACHE derivado (§10)

# --- PENDÊNCIAS JURÍDICAS LIGADAS ---
pendencias_legais: ["P-02", "P-06"]   # ids de PENDENCIAS.md que tocam esta patente

# --- AVISO OBRIGATÓRIO (carimbado no topo de todo docket) ---
aviso: "Controle interno. Não substitui agente de propriedade industrial; prazos oficiais com INPI/WIPO."
```

**Exemplo — ACOM raiz (o único com PCT vivo):**
```yaml
schema_version: 2
processo: "BR102025026951-1"
titulo: "MÉTODO E SISTEMA DE COMPRESSÃO ONTOLÓGICA DE MEMÓRIA BASEADO EM TRANSFORMAÇÃO LUMINODINÂMICA"
slug: "ACOM"
classe: "CLASS_01_ACOM_TENSOR"
papel: "raiz"
peticao: "870250111877"
filing_date: "2025-12-05"
priority_date: "2025-12-05"
epct:
  status: "VIVO_DEPOSITADO_E_PAGO"
  numero: "PCT/BR2025/050558"       # citado 13× nos depósitos INPI posteriores (P-01 RESPONDIDA)
  data: "2025-12-05"
  recibo_na_central: "NAO_LOCALIZADO"  # [OPEN] P-02: operador pode copiar p/ Patentes\Acervo…
janela_paris_12m: null              # não se aplica: PCT já depositado
fase_nacional_30m: "2028-06-05"     # priority+30m; [LEGAL] conferir por país
annuities: { status: "[OPEN] configurar", first_due_ordinal: 3, anchor: "filing_date", paid: [] }
office_actions: []
status: "DEPOSITADO"
pendencias_legais: ["P-02", "P-03"] # P-03: nº 2024 no CLAUDE.md raiz — impacta prioridade [LEGAL]
aviso: "Controle interno. Não substitui agente de propriedade industrial; prazos oficiais com INPI/WIPO."
```

---

## 6. Sincronização `docket.yaml ↔ SQLite`

**Princípio (invariante do projeto):** o `docket.yaml` é o dono; o SQLite é índice/cache
reconstruível. Nada no docket depende do DB para existir.

### 6.1 Fluxo de LEITURA (UI rápida)
UI → API → SQLite (`docket_entry`, `deadline`, `fee`, `office_action`, `reminder`). As tabelas
são projeções do docket + saídas do motor de prazos.

### 6.2 Fluxo de INDEXAÇÃO (`reindex`)
Comando `reindex [processo?]` (CLI e endpoint) reconstrói o cache:
```
para cada docket.yaml em patents/*/:
  1. ler + validar contra o schema (Pydantic); schema_version < 2 → migrar em memória
  2. calcular sha256(docket.yaml) → docket_entry.docket_sha256
  3. upsert docket_entry (fatos-base)
  4. rodar MOTOR DE PRAZOS (§8) → lista de Deadline derivados
  5. mesclar overrides.deadlines (prevalecem, com auditoria) + office_actions + fees vencíveis
  6. recomputar level de cada deadline (§9) e alert_level da patente = pior nível
  7. gerar reminders (§10)
  8. substituir (delete+insert idempotente por id determinístico) as linhas do processo
tudo em UMA transação por processo; se validação falhar → não toca o cache, loga em logs/legal_reindex.log e cria/atualiza pendência
```
Idempotência: rodar `reindex` N vezes sem mudar docket.yaml → cache byte-idêntico (ids
determinísticos, sem timestamps nos ids). `updated_at` só muda se o conteúdo mudou.

### 6.3 Fluxo de ESCRITA (operador edita pela UI)
A UI **nunca** escreve no SQLite direto. Escrita = mutação de fato-base → gravar `docket.yaml` →
reindexar:
```
PUT/POST → validar payload (Pydantic)
  → BACKUP: copiar docket.yaml → docket.yaml.bak_<YYYYMMDD_HHMMSS>_<motivo>   # hábito da casa
  → escrever docket.yaml (YAML estável, chaves ordenadas, aviso no topo preservado)
  → recomputar manifesto SHA-256
  → reindex(processo)  → cache atualizado
  → responder com o DocketEntry recomputado
```
Campos `alert_level`, `reminders`, e qualquer `deadline derived` são **read-only** na API de
escrita (recomputados). Só fatos-base, `overrides`, `office_actions`, `fees.pago`,
`annuities.paid`, `status` e `pendencias_legais` são editáveis.

### 6.4 Watchdog (indexação incremental)
Watchdog observa `patents/*/docket.yaml`. Ao detectar modificação externa (o operador editou o
YAML na mão), dispara `reindex(processo)` com debounce (~1 s). Assim o filesystem permanece a
fonte da verdade mesmo com edição fora da UI. Conflito UI-vs-arquivo: última escrita vence, mas
o `.bak_*` preserva o anterior; divergência estrutural → pendência.

> [nota operacional do operador — omitida no retrato público]

---

## 7. Anuidades INPI — modelo `[OPEN] configurar`

Base legal (LPI 9.279/96, arts. 84–86) — **modelado como aritmética, veredito é do agente**:

- A **1ª anuidade devida é a 3ª** (`first_due_ordinal: 3`): as anuidades incidem a partir do
  **início do 3º ano** contado da **data do depósito** (`anchor: filing_date`).
- **Período ordinário:** os 3 primeiros meses do período anual (paga-se independentemente de
  notificação). **Período extraordinário:** os 6 meses seguintes, com retribuição adicional.
- Não pagamento no extraordinário → **arquivamento** do pedido (`status → ARQUIVADO`), com
  possibilidade de restauração (art. 87) em prazo próprio — tudo `[LEGAL] → agente`.

**Cálculo por anuidade `n` (n ≥ 3):**
```
ordinary_start(n)  = filing_date + (n-1) anos            # início do enésimo período anual
ordinary_due(n)    = ordinary_start(n) + 3 meses         # fim do período ordinário
extraordinary_due(n)= ordinary_due(n)  + 6 meses         # fim do período extraordinário (com adicional)
```
**3ª anuidade das 16 (início do período ordinário = `filing_date + 2 anos`):**

| Lote | ordinary_start (3ª) | ordinary_due (3ª) | extraordinary_due (3ª) |
|---|---|---|---|
| ACOM (2025-12-05) | **2027-12-05** | 2028-03-05 | 2028-09-05 |
| Lote-B 11/02/2026 (×9) | **2028-02-11** | 2028-05-11 | 2028-11-11 |
| Dípolo (2026-02-27) | **2028-02-27** | 2028-05-27 | 2028-11-27 |
| Célula/SkyGrid (2026-03-01) | **2028-03-01** | 2028-06-01 | 2028-12-01 |
| Aprendizado (2026-03-09) | **2028-03-09** | 2028-06-09 | 2028-12-09 |
| Oncologia (2026-03-10) | **2028-03-10** | 2028-06-10 | 2028-12-10 |
| Kernel (2026-03-15) | **2028-03-15** | 2028-06-15 | 2028-12-15 |

O motor gera `Deadline(tipo=ANNUITY, base_date=ordinary_start, due_date=ordinary_due,
grace_until=extraordinary_due)`. **Valores em R$** ficam `[OPEN] configurar` num
`legal_config.yaml` (tabela por porte — a IALD é PJ; verificar enquadramento e descontos no
INPI) até o operador preencher. Enquanto `annuities.status == "[OPEN] configurar"`, a UI
mostra a **janela** (datas) mas rotula o valor como `[OPEN]`.

---

## 8. Motor de prazos (deadline engine) — contrato

Função pura, determinística, sem I/O de rede: `derive_deadlines(docket, today) -> [Deadline]`.
Pseudocódigo (não é código de aplicação — é o contrato que a Fase 3 implementa):

```
function derive_deadlines(d: Docket, today: date) -> list[Deadline]:
    out = []

> [nota operacional do operador — omitida no retrato público]

    # 8.2 Anuidades (§7) — gera pelo menos a próxima anuidade não paga
    n = próxima_anuidade_nao_paga(d.annuities)           # começa em 3
    out += Deadline(ANNUITY, base=ordinary_start(n),
                    due=ordinary_due(n), grace_until=extraordinary_due(n),
                    markers=["OPEN"] if d.annuities.status=="[OPEN] configurar" else [])

> [nota operacional do operador — omitida no retrato público]

    # 8.4 Office actions pendentes
    for oa in d.office_actions where oa.status=="pendente":
        out += Deadline(OFFICE_ACTION_RESPONSE,
                        base=oa.data_ciencia, due=oa.due_date,
                        note=oa.descricao)

    # 8.5 Overrides manuais (prevalecem por (tipo,due) com auditoria)
    out = apply_overrides(out, d.overrides.deadlines)
    out += [Deadline(CUSTOM, due=r.due_date, label=r.label) for r in d.overrides.reminders_custom]

    # 8.6 Nível + status de cada deadline
    for dl in out:
        dl.level  = compute_level(dl, today)             # §9
        dl.status = compute_status(dl, today, d)         # pendente|vencido|cumprido|na
    return out
```

**Aritmética de datas:** `+ N meses` = mesmo dia no mês-alvo; se inexistente (ex.: 31→fev),
usar o último dia do mês-alvo e marcar `[LEGAL] conferir`. **Nenhum ajuste de dia útil/feriado**
é aplicado (é competência do INPI/WIPO) — quando `due_date` cai em sáb/dom, anexar nota
`[LEGAL] verificar prorrogação para o próximo dia útil`.

### 8.4-esquema `office_action`
```yaml
office_actions:
  - id: "OA-1"
    tipo: "exigencia_tecnica"        # exigencia_formal | exigencia_tecnica | parecer | ciencia_indeferimento
    protocolo: "…"                   # nº da petição/despacho
    data_publicacao_rpi: "2026-08-04" # data da RPI (início da contagem oficial)
    data_ciencia: "2026-08-04"
    prazo_dias: 90                   # típico: exig. técnica 90d; formal preliminar 30d (conferir)
    due_date: "2026-11-02"           # data_ciencia + prazo_dias (aritmético)
    status: "pendente"               # pendente | cumprido | perdido
    descricao: "Exigência sob art. 36 (…)."
    markers: ["LEGAL"]
```
> **Nota importante:** contagem de prazo de exigência é a partir da **publicação na RPI**, em
> dias (corridos, salvo regra específica). O motor calcula `due = data_ciencia + prazo_dias`
> apenas como **lembrete**; a data oficial é a da RPI/INPI → `[LEGAL]`.

---

## 9. Níveis de alerta — algoritmo

`level` de um deadline depende de `dtd = (due_date - today).days` e do **tipo** (prazos
não-recuperáveis, como Paris/PCT, alertam com muito mais antecedência que uma taxa). Limiares
`{amarelo, laranja, vermelho}` (dias) por tipo, **configuráveis em `legal_config.yaml`**:

> [nota operacional do operador — omitida no retrato público]

```
function compute_level(dl, today):
    if dl.status in {cumprido, nao_aplicavel, dispensado}: return "neutro"
    dtd = (dl.due_date - today).days
    if dtd < 0:
        if dl.tipo==ANNUITY and dl.grace_until and today <= dl.grace_until: return "vermelho"  # ainda salvável (extraordinário)
        return "vencido"
    t = thresholds[dl.tipo]        # de legal_config.yaml
    if dtd <= t.vermelho: return "vermelho"
    if dtd <= t.laranja:  return "laranja"
    if dtd <= t.amarelo:  return "amarelo"
    return "verde"

# nível da PATENTE = pior (mais urgente) entre seus deadlines ativos
ordem = [vencido > vermelho > laranja > amarelo > verde > neutro]
alert_level(patente) = max(ordem, deadlines_ativos.level)
```

**Cores/badges na UI** (Tailwind + shadcn `Badge`, com ícone e texto — nunca só cor, por
acessibilidade): `verde` (emerald / "no prazo"), `amarelo` (amber / "atenção"), `laranja`
(orange / "urgente"), `vermelho` (red / "crítico"), `vencido` (zinc-800 + ícone de alerta /
"vencido — verificar com agente"), `neutro` (slate / "cumprido/N-A"). **Modo claro e escuro.**

**Validação com a tabela §3:** em **2026-07-09**, `PARIS_12M` das 15 tem janela ÚNICA
**2026-11-30** (alvo) / **2026-12-05** (fatal), `dtd ≈ 144–149 d` → **amarelo** por decisão firme
do operador (2026-07-09): faixa 90–180 d, **o prazo mais crítico do acervo** (antes marcado
verde/2027 — corrigido para amarelo); ACOM `PCT_NATIONAL_PHASE_30M` `dtd ≈ 695 d` → **verde**;
todas as anuidades `dtd ≫ 120 d` → verde. Logo `alert_level` da carteira: 1 verde (ACOM) + 15
amarelas — coerente com a coluna "Nível" da tabela.

---

## 10. Reminders / timeline

Para cada `Deadline` ativo o motor gera `Reminder`s em offsets `T-minus` (dias antes de
`due_date`), configuráveis por tipo em `legal_config.yaml`:

```yaml
reminder_offsets:
  PARIS_12M:                [365, 270, 180, 120, 90, 60, 30, 14, 7, 1]
  PCT_NATIONAL_PHASE_30M:   [365, 270, 180, 120, 90, 60, 30, 14, 7, 1]
  ANNUITY:                  [120, 90, 60, 30, 14, 7, 1]   # + no início do extraordinário
  OFFICE_ACTION_RESPONSE:   [45, 30, 20, 10, 7, 3, 1]
  FEE_DUE:                  [30, 14, 7, 3, 1]
```
`Reminder = {id, deadline_id, offset_days, fire_date = due_date - offset, fired:bool,
channel: "ui"}`. **Canal padrão = `ui`** (badge/sino no dashboard; nenhum envio externo). Um
canal opcional `email_draft` (§12) **gera rascunho** que o operador dispara manualmente —
jamais automático (local-first, privado). O `fired` é marcado quando o operador reconhece o
aviso; o estado de reconhecimento vive em `overrides` (persistido no docket) para sobreviver ao
`reindex`.

**Timeline visual (Plotly):** um Gantt/timeline horizontal por patente e um agregado da
carteira — eixo X = tempo (hoje…+36 meses), uma faixa por patente, marcadores por deadline
coloridos pelo `level`, linha vertical "hoje". Zoom/hover mostra `label`, `due_date`, `dtd`,
markers. Os 7 lotes (§3) aparecem como bandas verticais (Paris — janela ÚNICA das 15 — 2026-11-30 alvo / 2026-12-05 fatal;
fase nacional ACOM 2028-06-05; anuidades 2028-02…12).

---

## 11. Contratos de API (backend FastAPI, porta 8765, local-first)

Todos os endpoints leem do cache SQLite; escrita passa pelo fluxo §6.3. Prefixo `/api/legal`.

| Método | Rota | Retorno / efeito |
|---|---|---|
| `GET` | `/api/legal/docket` | lista de `DocketEntry` (resumo) + `alert_level` + prazo vivo de cada patente |
| `GET` | `/api/legal/docket/{processo}` | docket completo: fatos-base + deadlines derivados + fees + office_actions + reminders |
| `GET` | `/api/legal/deadlines?level=&tipo=&janela_dias=&lote=` | deadlines da carteira filtrados/ordenados por urgência |
| `GET` | `/api/legal/timeline?scope=carteira|processo&processo=` | payload p/ Plotly (séries por patente) |
| `GET` | `/api/legal/questoes` | agrega pendências `[LEGAL]` abertas (P-02/P-03/P-06) p/ o painel do agente (§12) |
| `PUT` | `/api/legal/docket/{processo}` | grava fatos-base editáveis → `.bak_*` → reindex → `DocketEntry` recomputado |
| `POST` | `/api/legal/docket/{processo}/office-actions` | anexa/atualiza office action → reindex |
| `POST` | `/api/legal/docket/{processo}/annuities/pay` | registra `annuities.paid[]` (ordinal, data, valor) → reindex |
| `POST` | `/api/legal/docket/{processo}/reminders/{id}/ack` | marca reminder reconhecido (grava em overrides) |
| `POST` | `/api/legal/reindex` \| `/api/legal/reindex/{processo}` | força reindexação a partir do filesystem |
| `GET`/`PUT` | `/api/legal/config` | lê/edita `legal_config.yaml` (limiares, offsets, tabela de anuidade) |
| `POST` | `/api/legal/questoes/{id}/draft-email` | gera **rascunho** local de e-mail ao agente (não envia) |

Respostas incluem sempre o campo `aviso` (§0) e `as_of: <today>` (data de cálculo, para a UI
mostrar "computado em"). Erros de validação retornam o campo que falhou + a pendência criada.

---

## 12. A questão jurídica pendente — painel "Questões para o Agente de PI"

Cartão fixo no topo do módulo (abaixo do aviso permanente), alimentado por `GET
/api/legal/questoes`, que agrega as pendências `[LEGAL]` abertas de `PENDENCIAS.md`:

> [nota operacional do operador — omitida no retrato público]

Cada questão exibe: patentes afetadas, prazo mais próximo impactado, status (`[ABERTA]`), e um
botão **"Gerar rascunho para o agente"** → `POST /api/legal/questoes/{id}/draft-email` produz um
`.md`/`.txt` **local** (em `compiled_prompts/` ou `logs/`) com o resumo factual (datas, números,
a pergunta) para o operador revisar e enviar. **Nunca envia sozinho.** Opcionalmente, a questão
pode ser injetada no **Prompt Compiler** como bloco `[LEGAL]` da próxima tarefa.

> Todo texto deste painel reafirma o **AVISO PERMANENTE**: o módulo **levanta** a questão e
> organiza os fatos; a **resposta jurídica é do agente de propriedade industrial**.

---

## 13. UI do módulo (Fase 3) — telas e componentes

Aba **Prazos** de cada patente + tela agregada **Docket Legal** no dashboard geral. Todas com o
aviso permanente carimbado no topo (componente `<LegalDisclaimer>` não-dispensável).

> [nota operacional do operador — omitida no retrato público]

Acessibilidade: nível nunca comunicado só por cor (ícone + rótulo textual); claro/escuro;
PT-BR na UI. React Flow/R3F **não** se aplicam a este módulo (é dado tabular/temporal) — só
Plotly para a timeline.

---

## 14. Casos de teste / checklist de validação

- **T1 — Regra do operador:** só ACOM raiz tem `epct.status=VIVO` e `PARIS_12M` ausente; as 15
  têm `SOMENTE_INPI` e exatamente um `PARIS_12M` vivo. (falha ⇒ regra P-02 violada)
- **T2 — Datas Paris:** `janela_paris` das 15 = janela ÚNICA derivada da **prioridade interna ao
  ACOM (2025-12-05)** — **alvo 2026-11-30 / fatal 2026-12-05** (decisão do operador 2026-07-09;
  substitui `filing_date + 12m` por-patente de fev–mar/2027). ACOM `fase_nacional_30m = 2028-06-05`.
- **T3 — Anuidades:** 3ª anuidade `ordinary_start = filing + 2 anos` (§7); valores `[OPEN]`.
- **T4 — Níveis em 2026-07-09:** 1 verde (ACOM) + 15 amarelas (§9/§3).
- **T5 — Idempotência:** dois `reindex` seguidos sem editar docket ⇒ cache byte-idêntico
  (ids determinísticos, `updated_at` estável).
- **T6 — Fonte da verdade:** apagar `central.db` + `reindex` ⇒ carteira reconstruída idêntica
  a partir dos `docket.yaml`.
- **T7 — Escrita segura:** PUT em um fato-base cria `docket.yaml.bak_*`, preserva o `aviso` no
  topo, e recomputa `alert_level` (campo não editável à mão).
- **T8 — Aviso permanente:** nenhuma tela/endpoint do módulo omite a string do §0.
- **T9 — Vencido salvável:** anuidade com `today` entre `ordinary_due` e `grace_until` ⇒
  `vermelho` (não `vencido`); após `grace_until` ⇒ `vencido` + sugestão `[LEGAL] restauração`.
- **T10 — Originais intactos:** re-hash de `Patentes\` == `original_hashes.json` (gate).

---

## 15. Referências cruzadas
`PROMPT_INAUGURAL_CENTRAL_DE_PATENTES.md` (LEGAL_DOCKET_SPEC, régua, CLASS_10) ·
`memory/PATENT_MASTER_INDEX.yaml` (fatos das 16) · `PENDENCIAS.md` (P-02/P-03/P-04/P-06) ·
`patents/BR102026005707-0_ONCOLOGIA/docket.yaml` (seed real do schema) ·
`architecture/DATA_MODEL.md` (entidades canônicas) · `architecture/UI_SPEC.md` (abas) ·
`architecture/PROMPT_COMPILER_SPEC.md` (injeção de blocos `[LEGAL]`).

> **Controle interno. Não substitui agente de propriedade industrial; prazos oficiais com
> INPI/WIPO.** — 1 = 1. Tetelestai.
