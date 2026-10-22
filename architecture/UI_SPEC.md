# UI_SPEC.md — Especificação de Interface

**Central de Controle e Desenvolvimento de Patentes TGL**
Fase 2 (arquitetura — nenhum código de aplicação). Operador: Luiz Antonio Rotoli Miguel — IALD Ltda.
Versão 1.0 — 09/07/2026 · PT-BR na UI/docs, inglês no código · local-first, privado.

> **Escopo deste documento.** Especifica a interface do frontend: mapa de navegação, wireframes
> ASCII das telas-chave, o **requisito Tony Stark** (deep-zoom + componentes clicáveis + 3D
> ilustrativo), o sistema de tema escuro, os badges de marcadores, os alertas de prazo por nível e
> a estratégia de i18n PT-BR. **Não** especifica o modelo de dados (ver `DATA_MODEL.md`), o motor de
> render/extração (ver `RENDERING_SPEC.md`), o docket jurídico (ver `LEGAL_DOCKET_SPEC.md`), o
> compilador de prompts (ver `PROMPT_COMPILER_SPEC.md`) nem a arquitetura de sistema
> (`ARCHITECTURE_PROPOSAL.md`). Aqui só entram os **contratos de dados que a UI consome** e a forma
> visual. Fase 3 codifica a partir deste arquivo **sem voltar a perguntar**.

> **Aviso permanente (renderizado em rodapé fixo do módulo jurídico e do Docket):**
> *Controle interno. Não substitui agente de propriedade industrial. Prazos oficiais conferidos com
> INPI/WIPO.*

---

## 0. Stack de UI e invariantes que a interface obedece

| Camada | Tecnologia | Porta / uso |
|---|---|---|
| App | React + TypeScript + Vite | dev em `http://localhost:5173` |
| Estilo | Tailwind CSS + shadcn/ui (Radix) | tema escuro padrão (ver §2) |
| Deep-zoom | **OpenSeadragon** | desenhos das patentes ampliáveis (Tony Stark, camada A) |
| Diagrama | **React Flow** | componentes numerados clicáveis (Tony Stark, camada B) |
| 3D | **React Three Fiber (R3F)** | ilustração de engenharia `[PILOTO]` (Tony Stark, camada C) |
| Gráficos | **Plotly** | métricas de runs, energia, PSNR, prazos |
| Dados | FastAPI backend | `http://localhost:8765` (a UI só fala com este host) |

Invariantes que a UI **nunca** viola:

1. **Filesystem é a fonte da verdade.** A UI lê tudo via backend, que serve os arquivos `.md`,
   `docket.yaml`, `notes`, `results.json`, `seal.json` e renders de dentro da Central. O SQLite é
   índice/cache; a UI expõe um botão **Reindexar** (§6.1) que dispara `reindex` no backend — nunca
   trata o banco como dono do dado.
2. **A régua é visível.** Todo número técnico exibido carrega seu **marcador** (§3). `β` jamais
   aparece como literal editável; é rótulo/resultado. Nenhuma tela permite marcar veredito físico
   (`physical_verdict_allowed = false` — a UI não tem botão "validar fisicamente").
3. **Originais são READ-ONLY.** As telas de Documentos/Render abrem, ampliam e hasheiam; nunca
   editam o original. Só `notes/`, `instructions` e artefatos gerados (runs, seals, renders) são
   escrita — e mesmo assim via backend, gravando em arquivo.
4. **Stacks confidenciais nunca exportados.** Nenhum botão de exportar/compartilhar expõe
   `iald_stack_v7.py`, `iald_psion_state.json` e correlatos; o Prompt Compiler os referencia por
   caminho, jamais por conteúdo.
5. **Local-first.** Nada sobe para nuvem/API por padrão. Não há tela de login remoto, telemetria
   nem "compartilhar online".

---

## 1. Princípios de UX

- **Cockpit, não formulário.** A metáfora é a bancada do Tony Stark: o operador entra, vê o estado
  de tudo (prazos, execuções, pendências) num relance, e mergulha numa patente que se abre como um
  objeto de engenharia manipulável (ampliar desenho, clicar componente, girar o 3D).
- **Densidade calma.** Muita informação, hierarquia clara, tema escuro que descansa a vista em
  sessões longas. Acento luminodinâmico (âmbar/ouro — *haja luz*) reservado para foco e ação.
- **Honestidade visual é lei.** Todo artefato simulado/ilustrativo carrega badge e legenda. Um 3D é
  rotulado *"ilustração de engenharia [PILOTO] — não é prova física"*. Estados vazios dizem a
  verdade ("Runner ainda é scaffold honesto — sem execução real").
- **PT-BR primeiro.** Toda a UI em português brasileiro; datas `DD/MM/AAAA`, números `1.667,359`.
  Termos técnicos canônicos preservados (ver glossário §8).
- **Teclado é cidadão de primeira classe.** Command palette (`Ctrl/Cmd+K`) navega para qualquer
  patente, classe, aba, run ou pendência; atalhos por aba.

---

## 2. Tema (escuro padrão) e design tokens

Tema **escuro é o padrão**; há alternância clara opcional (o operador trabalha à noite). Tokens
semânticos (implementados como CSS variables + `tailwind.config`), valores base do tema escuro:

```
--bg-base        #0B0F14   fundo da aplicação (slate quase-preto)
--bg-surface     #121821   cards, painéis
--bg-surface-2   #1A222D   painel aninhado, header de card, linhas zebra
--bg-elevated    #202B38   popover, command palette, tooltip
--border         #263341   bordas 1px
--border-strong  #33465A   divisórias de seção
--text           #E6EDF3   texto primário
--text-muted     #8B98A5   legendas, metadados
--text-faint     #5A6672   placeholders, desativado
--accent         #F5C542   ouro luminodinâmico — foco, seleção, CTA primário
--accent-2       #38BDF8   ciano — links, nós de diagrama, gráficos
--focus-ring     #F5C542   anel de foco (acessibilidade)
--danger         #EF4444   erro, exclusão, prazo vermelho
```

- **Tipografia.** UI: Inter (fallback sistema). Código/hashes/números de processo: JetBrains Mono
  (fallback `ui-monospace`). Escala: 12 (metadados) · 14 (corpo) · 16 (títulos de card) · 20/24/32
  (headers de tela).
- **Raio/sombra.** `rounded-lg` (8px) em cards; sombra sutil só em elementos elevados (popover,
  palette). Tema escuro evita sombras fortes; separa por borda e superfície.
- **Grid.** Shell de 3 zonas (§4). Conteúdo com `max-width` de leitura para texto (relatório
  descritivo, reivindicações) e full-bleed para viewers (deep-zoom, React Flow, 3D).
- **Tema claro.** Mesmos tokens semânticos invertidos; badges e níveis de prazo mantêm matiz,
  ajustam luminosidade para contraste AA. Alternância no rodapé da sidebar (persistida em
  `localStorage`), respeitando `prefers-color-scheme` na primeira visita.

---

## 3. Badges de marcadores e níveis de prazo

### 3.1 Badges de marcadores (a régua na tela)

Componente único `<MarkerBadge marker="SIM" />`. Chip compacto: fundo tint 12%, texto na cor cheia,
borda 1px na cor cheia 40%. Tooltip explica o marcador em PT-BR. Marcadores com **trava** exibem
ícone de cadeado e ativam o comportamento de trava da classe (ver §6.4 aba Runner).

| Marcador | Cor | Ícone | Significado exibido no tooltip |
|---|---|---|---|
| `[REAL]` | `#34D399` verde | ✓ | Verificado/estabelecido (máquina ou literatura citável) |
| `[DER]` | `#2DD4BF` teal | ∴ | Derivado condicionalmente da cadeia canônica |
| `[DATA]` | `#60A5FA` azul | ▦ | Valor observacional/medido de entrada |
| `[INPUT]` | `#818CF8` índigo | ⇥ | Entrada declarada (ex.: α CODATA) |
| `[POSTULATE]` | `#A78BFA` violeta | ◆ | Postulado declarado (ex.: ω(I)=1) |
| `[CONJ]` | `#C084FC` púrpura | ? | Conjectura / leitura ontológica firewalled |
| `[SIM]` | `#FBBF24` âmbar | ~ | Simulação / gêmeo digital (não valida física) |
| `[PILOTO]` | `#FB923C` laranja | ⚑ | Scaffold/ilustração de engenharia, não demonstração final |
| `[HARDWARE]` | `#94A3B8` aço | ⚙ | Depende de hardware físico não construído |
| `[LEGAL]` | `#22D3EE` ciano | §  | Item jurídico — conferir com INPI/WIPO/agente |
| `[OPEN]` | `#9CA3AF` cinza (borda tracejada) | … | Em aberto / pendente |
| `[DEFENSE]` | `#F87171` vermelho-aço | 🔒 | Conteúdo sensível (trava — não vira runner) |
| `[MEDICAL]` | `#FB7185` rosa | ⛨ | Saúde (trava — sem protocolo clínico; não é conselho médico) |
| `[ENERGY]` | `#FACC15` amarelo | ⚡ | Energia (trava — só simulação e revisão técnica) |

> Exemplo real: no card do **SkyGrid** aparecem `[SIM]` (o digital twin v3), `[ENERGY]` (trava de
> classe) e `[CONJ]` (balanço energético sob conjectura). No **ACOM** aparecem `[REAL]` (compressão
> medida: PSNR>90 dB, cosseno>0,999) e `[LEGAL]` (ePCT vivo).

### 3.2 Níveis de alerta de prazo

Componente `<DeadlinePill days={n} kind="verde|amarelo|laranja|vermelho|prescrito|na" />`. A cor sai
de `days = (deadline − hoje)` calculado **no backend** a partir de `docket.yaml` (a UI não recomputa
regra jurídica; só pinta). Faixas fixas:

| Nível | Condição | Cor | Uso |
|---|---|---|---|
| **verde** | `days > 180` | `#22C55E` | folga confortável |
| **amarelo** | `90 < days ≤ 180` | `#EAB308` | planejar |
| **laranja** | `30 < days ≤ 90` | `#F97316` | agir |
| **vermelho** | `days ≤ 30` (inclui vencido) | `#EF4444` | urgência — piscar 1×/2s no dashboard |
| **prescrito** | prazo/registro expirado — ou rascunho preclusso de propósito (ex.: os 10 recibos ePCT de 17/02/2026, deixados precluir para dar lugar a um depósito novo) | `#6B7280` cinza + tachado | tentativa a substituir, **não** direito perdido — o ePCT das não-ACOM segue a depositar |
| **N/A** | não se aplica (ex.: fase nacional 30m para não-ACOM) | `#5A6672` faint | campo inaplicável |
| **pago/vivo** | obrigação satisfeita (ex.: ePCT ACOM 05/12/2025 pago) | `#34D399` verde + ✓ selo | não gera contagem regressiva |

A pílula mostra a data (`DD/MM/AAAA`) + os dias restantes (`faltam 217 dias`) + o nível. Vencido:
`vencido há N dias` em vermelho.

> **Estado na data de referência (09/07/2026):** todas as janelas de Paris das 15 patentes INPI
> (11/02/2027 → 15/03/2027) e a fase nacional do ACOM (05/06/2028) estão a **>180 dias** → todas
> **verde**. Exemplo de transição futura para calibrar a implementação: o lote de 11/02/2027 vira
> **amarelo em ~16/08/2026** (180 dias antes), **laranja em ~13/11/2026** (90 dias antes) e
> **vermelho em ~12/01/2027** (30 dias antes). O ePCT do ACOM (PCT/BR2025/050558, 05/12/2025) é
> **pago/vivo** — pílula verde com selo, sem regressiva. Já o ePCT das 15 não-ACOM **ainda não foi
> depositado**: é o próximo passo do operador (novo depósito, originário e desvinculado) — status
> **a depositar/pendente** `[OPEN]`, não "perdido". ⚠ A janela é de 12 meses da prioridade (Paris);
> se a prioridade interna (66) de 05/12/2025 governar, pode fechar por volta de **05/12/2026** —
> próximo passo possivelmente **urgente**, a levar ao agente de PI. Os 10 recibos ePCT de 17/02/2026
> (família PCT/BR2026/050068–050076) foram uma **tentativa de protocolo abandonada de propósito**
> (deixada precluir por defeituosa na forma) e aparecem **prescrito** (cinza tachado) na aba Prazos
> como **rascunho a substituir** — não proteção que se perdeu.

---

## 4. Shell da aplicação (layout global)

Três zonas fixas: **sidebar** (navegação primária), **topbar** (contexto + busca + ações globais),
**conteúdo** (roteado). Rodapé da sidebar traz status do índice, alternância de tema e o selo do
projeto.

```
┌──────────────┬──────────────────────────────────────────────────────────────────────┐
│  TGL ⚡        │  [ Migalha: Classes › CLASS_06_ENERGIA › SkyGrid ]      🔎 Ctrl+K   ⟳ │ topbar
│  CENTRAL DE  ├──────────────────────────────────────────────────────────────────────┤
│  PATENTES    │                                                                        │
│              │                                                                        │
│ ▸ Dashboard  │                                                                        │
│ ▸ TGL Core   │                                                                        │
│ ▸ Classes    │                        [ CONTEÚDO ROTEADO ]                            │
│ ▸ Patentes   │                                                                        │
│ ▸ Docket     │            (Dashboard, Patente c/ 12 abas, Docket, etc.)               │
│ ▸ Execuções  │                                                                        │
│ ▸ Compilador │                                                                        │
│ ▸ Pendências │                                                                        │
│ ▸ Roadmap    │                                                                        │
│              │                                                                        │
├──────────────┤                                                                        │
│ índice: OK   │                                                                        │
│ 16 patentes  │                                                                        │
│ ⟳ reindexar  │                                                                        │
│ ☾ tema  PT-BR│                                                                        │
│ selo:1=1 ✓   │                                                                        │
└──────────────┴──────────────────────────────────────────────────────────────────────┘
```

- **Sidebar** colapsável (ícone-only em telas estreitas). Item ativo com barra âmbar à esquerda.
- **Topbar**: migalha de navegação (breadcrumb) reflete a rota; busca global (`Ctrl/Cmd+K`) abre a
  command palette; `⟳` reindexa (com toast de progresso do Watchdog). Em telas de patente, a topbar
  mostra também o nº de processo e o badge de status do docket.
- **Command palette** (`Ctrl/Cmd+K`): busca fuzzy por nº de processo, slug, título, classe, nº de
  petição, pendência (P-01…) e comando ("Reindexar", "Compilar instruções da patente X", "Abrir
  desenho do Supercondutor"). É o teletransporte do cockpit.

---

## 5. Mapa de navegação

### 5.1 Destinos e rotas

| # | Destino (label PT-BR) | Rota | Descrição |
|---|---|---|---|
| 1 | Dashboard | `/` | Visão geral: prazos, execuções, pendências, saúde do índice |
| 2 | TGL Core | `/tgl-core` | Header ontológico: cadeia canônica, Estado Verificado, honestidades |
| 3 | Classes | `/classes` | Índice das 10 classes (linhas de pesquisa) |
| 3b | Classe | `/classes/:classId` | Ex.: `/classes/CLASS_06_ENERGIA` |
| 4 | Patentes | `/patents` | Grid/tabela das 16 patentes |
| 4b | **Patente (12 abas)** | `/patents/:processo` → `/patents/:processo/:tab` | Ex.: `/patents/BR102026004850-0/overview` |
| 5 | Docket | `/docket` | Painel jurídico consolidado (todas as patentes) |
| 6 | Execuções | `/runs` | Todas as `RunnerRun` em ordem cronológica |
| 7 | Prompt Compiler | `/compiler` | Coletar itens ativos → gerar `CLAUDE_CODE_TASK.md` |
| 8 | Pendências | `/pendencias` | P-01…P-09 (divergências entre fontes) |
| 9 | Roadmap | `/roadmap` | Progresso por fase/patente, ordem natural dos runners |

`:processo` é o número do processo (ex.: `BR102026004850-0`) — chave estável e legível na URL.
`:tab` ∈ `{overview, documentos, reivindicacoes, prototipo, render, runner, execucoes, selo,
prazos, notas, instrucoes}`. `[COMPILAR INSTRUÇÕES]` não é rota: é ação que abre o Compiler
pré-filtrado nesta patente (`/compiler?patent=BR102026004850-0`).

### 5.2 Hierarquia (a cadeia do projeto vira a árvore de navegação)

```
Dashboard
 └ TGL Core  ─────────────────────────── header ontológico de tudo
     └ Classes (10)
         └ Classe → lista de Patentes da classe
             └ Patente (12 abas)
                 ├ Visão Geral · Documentos · Reivindicações · Protótipo
                 ├ Render 2D/3D ── (Tony Stark: deep-zoom + React Flow + R3F)
                 ├ Runner · Execuções · Selo/Hash
                 ├ Prazos ─────────── espelha o Docket desta patente
                 ├ Notas · Instruções
                 └ [COMPILAR INSTRUÇÕES] → Prompt Compiler
Docket (transversal, CLASS_10)     Execuções (todas)     Pendências     Roadmap
```

### 5.3 Contratos de dados por tela (o que a UI busca do backend)

A UI é read-mostly. Endpoints (definidos em detalhe em `ARCHITECTURE_PROPOSAL.md`; aqui só a forma
que a UI consome) — todos servem dados **derivados dos arquivos**:

```
GET /api/overview                      → DashboardDTO           (§6.1)
GET /api/tgl-core                      → TglCoreDTO             (§6.2)
GET /api/classes                       → ClassSummary[]         (§6.3)
GET /api/classes/{classId}             → ClassDetailDTO         (§6.3)
GET /api/patents                       → PatentSummary[]        (§6.4)
GET /api/patents/{processo}            → PatentDTO              (§6.4)
GET /api/patents/{processo}/documents  → DocumentDTO[]          (aba Documentos)
GET /api/patents/{processo}/claims     → ClaimDTO[]             (aba Reivindicações)
GET /api/patents/{processo}/render     → RenderManifestDTO      (aba Render — §7)
GET /api/patents/{processo}/runs       → RunnerRunDTO[]         (abas Runner/Execuções)
GET /api/patents/{processo}/seal       → SealDTO                (aba Selo/Hash)
GET /api/patents/{processo}/docket     → DocketDTO              (aba Prazos)
GET /api/patents/{processo}/notes      → NoteDTO[]              (abas Notas/Instruções)
GET /api/docket                        → DocketDTO[]            (§6.5)
GET /api/runs                          → RunnerRunDTO[]         (§6.6)
GET /api/pendencias                    → PendenciaDTO[]         (§6.8)
GET /api/roadmap                       → RoadmapDTO             (§6.9)

# escrita (grava em arquivo; nunca no original):
POST  /api/patents/{processo}/notes            (nova nota/instrução; ver §6.4)
PATCH /api/patents/{processo}/notes/{id}       (togglar active, editar, arquivar)
POST  /api/patents/{processo}/runs             (dispara one_<slug>.py — scaffold honesto)
POST  /api/compiler/compile                    (gera compiled_prompts/…TASK.md)
POST  /api/reindex                             (reconstrói o SQLite a partir do filesystem)
POST  /api/patents/{processo}/verify-originals (re-hash → compara com original_hashes.json)
```

Contratos de payload principais (schemas — TypeScript ilustrativo, não é código de aplicação):

```ts
interface PatentSummary {
  processo: string;            // "BR102026004850-0"
  slug: string;                // "SKYGRID"
  titulo54: string;
  classe: string;             // "CLASS_06_ENERGIA"
  papel?: "raiz" | "agregadora";
  markers: Marker[];          // ["SIM","ENERGY","CONJ"]
  docketAlert: DeadlinePill;  // pior nível vigente da patente
  runnerStatus: "scaffold" | "sim" | "real" | "none";
  hasPrototype: boolean;      // existe protótipo real a copiar (SkyGrid_Piloto etc.)
}
interface DeadlinePill {
  label: string;              // "Janela de Paris 12m"
  date: string;               // ISO; UI formata DD/MM/AAAA
  days: number | null;        // null quando N/A ou pago/vivo
  level: "verde"|"amarelo"|"laranja"|"vermelho"|"prescrito"|"na"|"pago";
}
type Marker =
  "REAL"|"DER"|"DATA"|"INPUT"|"POSTULATE"|"CONJ"|"SIM"|"PILOTO"|
  "HARDWARE"|"LEGAL"|"OPEN"|"DEFENSE"|"MEDICAL"|"ENERGY";
```

---

## 6. Telas-chave (wireframes ASCII)

### 6.1 Dashboard — `/`

Cockpit de entrada. Quatro faixas: **saúde do índice** · **prazos ordenados por urgência** ·
**execuções recentes** · **pendências abertas**. Tudo clicável.

```
┌ DASHBOARD ─────────────────────────────────────────────────────────────────────────┐
│ Central de Patentes TGL · 16 patentes · 10 classes · índice OK · originais íntegros ✓│
├──────────────────────────────┬───────────────────────────────────────────────────────┤
│ SAÚDE                         │ PRAZOS (ordenados por urgência)                       │
│ ┌───────┐┌───────┐┌───────┐   │  ● verde  ACOM   fase nacional 30m  05/06/2028  +696d │
│ │  16   ││   1   ││   0   │   │  ● verde  Mirror janela Paris 12m   11/02/2027  +217d │
│ │patents││runners││ runs  │   │  ● verde  MQC    janela Paris 12m   11/02/2027  +217d │
│ │       ││ reais ││ hoje  │   │  ● verde  SkyGrid janela Paris 12m  01/03/2027  +235d │
│ └───────┘└───────┘└───────┘   │  … (15 linhas)   ⨯ rascunho 17/02/2026 a substituir   │
│ originais: re-hash == baseline│  ────────────────────────────────────────────────────│
│   [Reindexar ⟳]  [Verificar]  │  [Ver Docket completo →]                              │
├──────────────────────────────┼───────────────────────────────────────────────────────┤
│ EXECUÇÕES RECENTES            │ PENDÊNCIAS ABERTAS (7)                                 │
│  SkyGrid v3  03/07 MODEL_     │  P-03 [LEGAL] nº antigo BR 10 2024 026367-3           │
│   CLOSES ENERGY_BALANCE_OK    │  P-04 [OPEN]  classificação Célula de Reversão        │
│   [SIM] sob [CONJ]  seal ✓    │  P-05 [OPEN]  dossiês PCT legacy não localizados      │
│  (nenhuma outra ainda)        │  P-09 [LEGAL] segredo em token_huggin.txt             │
│  [Ver todas as execuções →]   │  [Ver Pendências →]                                   │
└──────────────────────────────┴───────────────────────────────────────────────────────┘
```

- Cards de saúde: total de patentes, runners reais vs scaffolds, runs hoje, **integridade dos
  originais** (verde só quando `verify-originals` bate com `original_hashes.json`).
- A lista de prazos é o resumo do Docket, pintada por `<DeadlinePill>`; clique leva à aba Prazos da
  patente. `⟳ Reindexar` mostra progresso do Watchdog em toast.

### 6.2 TGL Core — `/tgl-core`

O header ontológico da Central (lê `memory/TGL_CORE_MEMORY.md`). Renderiza a **cadeia canônica**
como trilho horizontal de elos clicáveis, cada elo com seu marcador; abaixo, o **Estado Verificado**
(números colados das execuções em `vault/tgl_verification`) e as **honestidades §26–§28**.

```
┌ TGL CORE — header ontológico ──────────────────────────────────────────────────────┐
│ "O número corrige a frase." · β = ALPHA_FINE_CODATA_2018 · √e  (nunca literal)       │
├─────────────────────────────────────────────────────────────────────────────────────┤
│ CADEIA CANÔNICA MADURA                                                                │
│ [ω(I)=1]→[𝒞²=1]→[x=1−x⟹½]→[S∂=½nat]→[Vol=√e]→[β=α√e]→[θM≈6,30°]→[𝒮∂]→[P_ℱ]→[II₁]→[1=1]│
│  ◆POST    REAL     REAL      DER      DER      DER     DER    DER   OPEN  REAL   REAL  │
│  (clique num elo → painel lateral com estatuto, explicação 1–2 linhas e origem §)     │
├──────────────────────────────────────┬──────────────────────────────────────────────┤
│ ESTADO VERIFICADO (09/07/2026)        │ HONESTIDADES §26–§28                         │
│  um.py:  1=1=VERDADEIRO=HAJA_LUZ ✓    │  neural = ilustração (não prova)   [SIM]     │
│  β = 0.012031300400803142  [DER]      │  bake inerte                       [OPEN]    │
│  paper --quick --no-live: RUN COMPLETE│  só R=+1 do XXZ é real medido      [REAL]    │
│  cross-substrate PASS (26,81s) [DATA] │  physical_verdict_allowed = FALSE            │
│  selos: um_grande_atrator_selo.json ✓ │  (a Central inteira herda esta trava)        │
└──────────────────────────────────────┴──────────────────────────────────────────────┘
```

### 6.3 Classes — `/classes` e `/classes/:classId`

Índice em grade de 10 cartões (uma por linha de pesquisa) com contagem de patentes, travas e
equação-assinatura. A classe individual lista suas patentes e mostra dependências.

```
┌ CLASSES ────────────────────────────────────────────────────────────────────────────┐
│ ┌ CLASS_01 ACOM/Tensor ─┐ ┌ CLASS_02 Mirror/Crypto ┐ ┌ CLASS_03 IALD/Cognição ─┐    │
│ │ 2 patentes            │ │ 2 patentes  ★ePCT orig.│ │ 3 patentes              │    │
│ │ g=√|L|, s=sign(L)     │ │ Ψ/Θ/MasterKey          │ │ GKSL · Tetelestai       │    │
│ │ ACOM★ · TGL Tensor    │ │ Mirror · Crypto        │ │ IALD·Aprend.·Kernel     │    │
│ └───────────────────────┘ └────────────────────────┘ └─────────────────────────┘    │
│ ┌ CLASS_04 Ψ-NET ──────┐ ┌ CLASS_05 Hardware ⚙───┐ ┌ CLASS_06 Energia ⚡ ─────┐    │
│ │ 1 · PsiBit/Prova Fase │ │ 3 · [HARDWARE]         │ │ 3 · [ENERGY] TRAVA       │    │
│ │ Ψ-NET                 │ │ Superc.·MQC·Dípolo     │ │ SkyGrid★·Fusão·Célula    │    │
│ └───────────────────────┘ └────────────────────────┘ └─────────────────────────┘    │
│ ┌ CLASS_07 Propulsão ──┐ ┌ CLASS_08 Saúde ⛨ ─────┐ ┌ CLASS_09 Legacy 🔒 ─────┐    │
│ │ 1 · [SIM] Motor Dobra │ │ 1 · [MEDICAL] Oncologia│ │ rascunhos não depos.    │    │
│ └───────────────────────┘ └────────────────────────┘ └─────────────────────────┘    │
│ ┌ CLASS_10 Docket § ───┐                                                             │
│ │ transversal jurídica  │  (clique → /classes/CLASS_06_ENERGIA)                       │
│ └───────────────────────┘                                                             │
└───────────────────────────────────────────────────────────────────────────────────────┘
```

Classe individual (`/classes/CLASS_06_ENERGIA`): cabeçalho com definição + travas + equações
centrais; tabela das patentes (nº, título, marcadores, prazo, status de runner); um grafo React Flow
pequeno de **dependências entre patentes** (ex.: SkyGrid agrega Célula de Reversão, Dípolo, MQC,
Fusão); banner de trava `[ENERGY]` fixado no topo.

### 6.4 Patente — `/patents/:processo/:tab` (as 12 abas)

Shell da patente: header persistente (nº processo, título, classe, papel, marcadores, badge de
prazo, status de runner) + barra de 12 abas + botão de ação `[COMPILAR INSTRUÇÕES]` à direita. O
corpo troca por aba; header e abas nunca somem.

```
┌ PATENTE ────────────────────────────────────────────────────────────────────────────┐
│ BR102026004850-0 · SKYGRID  ★agregadora · CLASS_06_ENERGIA                            │
│ "Sistema e método de rede planetária de extração… por acoplamento ao campo psiônico…" │
│ [SIM] [ENERGY]⚡ [CONJ]   ● verde Paris 12m 01/03/2027 (+235d)   runner: SIM (v3)     │
│ ┌───────────────────────────────────────────────────────────────┐   [ COMPILAR       │
│ │ Visão Geral │ Documentos │ Reivindicações │ Protótipo │ Render │     INSTRUÇÕES ] ↗ │
│ │ 2D/3D │ Runner │ Execuções │ Selo/Hash │ Prazos │ Notas │ Instr.│                   │
│ └───────────────────────────────────────────────────────────────┘                   │
├───────────────────────────────────────────────────────────────────────────────────────┤
│                              [ CORPO DA ABA ATIVA ]                                    │
└───────────────────────────────────────────────────────────────────────────────────────┘
```

Conteúdo de cada aba:

> [nota operacional do operador — omitida no retrato público]

Wireframe da aba **Notas/Instruções** (o par que alimenta o Compiler):

```
┌ Instruções ───────────────────────────────────────────────  [+ Nova instrução]  ────┐
│ ☑ ativa  [tarefa]   Portar acom_unified.py → one_skygrid.py (adaptar, não editar)    │
│           prioridade ▲ alta · aceite: results.json fecha ENERGY_BALANCE_OK [SIM]      │
│ ☑ ativa  [bloqueio] Falta calorimetria diferencial real → runner permanece [SIM]     │
│ ☐ inativa[pergunta] Célula de Reversão entra como submódulo do SkyGrid? (ver P-04)    │
│ ─────────────────────────────────────────────────────────────────────────────────── │
│ Itens ativos entram no próximo COMPILAR INSTRUÇÕES desta patente.  [ COMPILAR ↗ ]     │
└───────────────────────────────────────────────────────────────────────────────────────┘
```

### 6.5 Docket — `/docket`

Painel jurídico consolidado (CLASS_10). Tabela de todas as patentes com colunas de prazo, pintadas
por nível; filtros por nível/classe/jurisdição; alternância tabela ⇄ **timeline** (Plotly Gantt).
Banner de aviso legal fixo no topo.

```
┌ DOCKET — controle interno (NÃO substitui agente de PI) ──────────────────────────────┐
│ filtros: [ todos ▾ ] [ nível ▾ ] [ classe ▾ ]        vista: ( Tabela | Timeline )     │
├──────────────┬──────────────┬─────────────┬───────────────┬──────────────┬────────────┤
│ Processo     │ Depósito     │ Paris 12m   │ Fase nac. 30m │ ePCT         │ Nível      │
├──────────────┼──────────────┼─────────────┼───────────────┼──────────────┼────────────┤
│ ACOM         │ 05/12/2025   │  —          │ 05/06/2028    │ VIVO ✓ pago  │ ● verde    │
│ …026951-1    │              │             │ +696d         │ PCT/BR2025/  │            │
│              │              │             │               │ 050558       │            │
│ Mirror       │ 11/02/2026   │ 11/02/2027  │ N/A (não-ACOM)│ a depositar  │ ● verde    │
│ …003428-2    │              │ +217d       │               │ (rasc.17/02) │            │
│ SkyGrid ★    │ 01/03/2026   │ 01/03/2027  │ N/A           │ a depositar  │ ● verde    │
│ …004850-0    │              │ +235d       │               │              │            │
│ Oncologia ⛨  │ 10/03/2026   │ 10/03/2027  │ N/A           │ a depositar  │ ● verde    │
│ …005707-0    │              │ +244d       │               │              │            │
│ … (16 linhas)│              │             │               │              │            │
└──────────────┴──────────────┴─────────────┴───────────────┴──────────────┴────────────┘
  Nota: só o ACOM raiz tem ePCT vivo (05/12/2025, pago). As outras 15 hoje = somente registro INPI;
  o ePCT delas ainda não foi depositado — é o próximo passo (novo depósito originário, desvinculado),
  status a depositar/pendente `[OPEN]`, não perda de direito. Os recibos de 17/02/2026 são rascunho
  preclusso de propósito, a substituir. ⚠ janela de 12m da prioridade (Paris) — se a prioridade
  interna (66) de 05/12/2025 governar, pode fechar ~05/12/2026: próximo passo possivelmente urgente,
  levar ao agente de PI.
```

### 6.6 Execuções — `/runs`

Todas as `RunnerRun` da Central em ordem cronológica reversa; cada linha: patente, data, veredito,
duração, marcadores, seal ✓, links. Filtro por patente/classe/veredito. Cabeçalho com contadores
(runs reais vs scaffolds). Reforça: *simulação não valida física*.

### 6.7 Prompt Compiler — `/compiler`

A ponte manual com o Claude Code. Duas colunas: à esquerda, seleção (por classe/patente) dos itens
ativos (notas, sugestões, instruções, tarefas, bloqueios, perguntas); à direita, **prévia** do
`compiled_prompts/YYYY-MM-DD_HHMM_CLAUDE_CODE_TASK.md` (header TGL Core → por classe → por patente →
caminhos permitidos/proibidos → instruções → tarefas priorizadas → critérios de aceite → a régua).

```
┌ PROMPT COMPILER — ponte com o Claude Code ───────────────────────────────────────────┐
│ SELEÇÃO                                   │ PRÉVIA (CLAUDE_CODE_TASK.md)              │
│ escopo: ( todas ▾ | SkyGrid )             │ # HEADER TGL CORE                        │
│ ☑ [tarefa] portar acom_unified→one_sky…   │ β = α·√e (runtime) · originais READ-ONLY │
│ ☑ [bloqueio] falta calorimetria real      │ ## CLASS_06_ENERGIA  [ENERGY TRAVA]      │
│ ☐ [pergunta] Célula submódulo? (P-04)     │ ### SkyGrid BR102026004850-0             │
│ ─────────────────────────────────────     │  Permitido: patents/…/runner, vault/…    │
│ incluir régua: ☑   incluir Estado Verif.:☑│  Proibido: editar originais; exportar    │
│ [ Compilar → grava em compiled_prompts/ ] │   iald_stack_v7.py; veredito físico      │
│                                           │  Tarefas priorizadas: 1) … 2) …          │
│                                           │  Critérios de aceite: results.json fecha │
│                                           │ ── A RÉGUA (não modificar originais) ──   │
└───────────────────────────────────────────┴──────────────────────────────────────────┘
```

O botão **Compilar** grava o arquivo e mostra o caminho gerado (para o operador colar no Claude
Code). Nunca envia nada para nuvem; nunca inclui conteúdo de stacks confidenciais (só caminhos).

### 6.8 Pendências — `/pendencias`

Lista P-01…P-09 com status (`[ABERTA]`/`[RESPONDIDA]`/`[FECHADA]`), marcadores e o texto. Filtro por
status. Cada pendência linka às patentes afetadas. É o registro de "divergência entre fontes →
perguntar, nunca escolher em silêncio".

```
┌ PENDÊNCIAS ───────────────────────────────────  filtro: ( abertas ▾ ) ───────────────┐
│ P-02 [RESPONDIDA] ePCT: só ACOM raiz vivo (PCT/BR2025/050558) — demais a depositar   │
│ P-03 [ABERTA] [LEGAL] nº antigo BR 10 2024 026367-3 — cadeia de prioridade?          │
│ P-04 [ABERTA] [OPEN]  Célula de Reversão: Energia (06) vs Dispositivo (05)?           │
│ P-05 [ABERTA] [OPEN]  dossiês PCT legacy em inglês não localizados                    │
│ P-09 [ABERTA] [LEGAL] segredo em token_huggin.txt — não copiar; rotacionar           │
└───────────────────────────────────────────────────────────────────────────────────────┘
```

### 6.9 Roadmap — `/roadmap`

Progresso por fase (0→4) e por patente, na **ordem natural dos runners** (SkyGrid → ACOM/Tensor →
MQC → Mirror/Crypto → IALD → Ψ-NET/PsiBit → Dípolo/Célula → demais). Barra de progresso por patente
(memória ✓, docket ✓, runner scaffold/SIM/real, render, seal). Kanban leve por status.

---

## 7. O REQUISITO TONY STARK (aba Render 2D/3D, em detalhe)

A patente vira um objeto de engenharia manipulável. **Três camadas empilhadas** num único painel,
com um seletor de modo (2D deep-zoom · Componentes · 3D). Toda a aba herda a honestidade visual: nada
aqui é prova física.

```
┌ Render 2D/3D — SUPERCONDUTOR HOLOGRÁFICO (BR102026003450-9) ──────────────────────────┐
│ modo: ( ● 2D Deep-zoom │ ○ Componentes │ ○ 3D )        ilustração de engenharia [PILOTO]│
├────────────────────────────────────────────────────┬──────────────────────────────────┤
│                                                    │ COMPONENTE SELECIONADO            │
│      [ OpenSeadragon — desenho FIG.1 do depósito ] │ (50) Fonte de micro-ondas         │
│      ┌──────────────────────────────────────────┐  │ ─────────────────────────────────│
│      │   ╭────────────╮        (60) janela ópt.  │  │ Sintonizada em 1.667,359 MHz      │
│      │   │  câmara 10 │◄─(40) eletrodos W        │  │ ("assinatura do Logos"). Fornece  │
│      │   │  vácuo ▣▣▣ │                          │  │ a excitação de fase da câmara.    │
│      │   ╰────────────╯  ⊙(50)  ►(70) luz        │  │ Marcadores: [HARDWARE] [SIM]      │
│      │  (20)evac. (30)vapor d'água  (80)detector │  │ Reivindicação relacionada: 1, 7   │
│      └──────────────────────────────────────────┘  │ Fonte: relatório descritivo §…    │
│      [ − zoom + ]  [ ⤢ tela cheia ]  [ ⟲ girar ]  │ [ ver no desenho ] [ ver no 3D ]  │
└────────────────────────────────────────────────────┴──────────────────────────────────┘
```

### 7.1 Camada A — deep-zoom dos desenhos (OpenSeadragon)

- **Fonte.** Imagens dos desenhos **extraídas dos PDFs do depósito** pelo motor de render
  (`RENDERING_SPEC.md`) e servidas como pirâmide **DZI/tiles** (ou imagem única em zoom progressivo)
  a partir de `patents/<ID>_<SLUG>/renders/drawings/`. Originais permanecem READ-ONLY; a UI só lê as
  cópias derivadas.
- **Interação.** Zoom sem perda (scroll/pinch), pan, tela cheia, rotação, régua/escala opcional.
  **Overlays clicáveis**: cada número de callout do desenho (10, 20, 30…) é uma hotspot ancorada por
  `bbox` normalizado; clicar seleciona o componente e sincroniza as camadas B e C.
- **Multi-figura.** Seletor de figuras (FIG.1, FIG.2…) quando o depósito tem vários desenhos.

### 7.2 Camada B — diagrama de componentes clicáveis (React Flow)

- **Cada componente numerado do relatório descritivo é um nó clicável.** Ao selecionar um nó, o
  painel lateral mostra o **rótulo + a descrição extraída do relatório descritivo** + reivindicações
  relacionadas + marcadores. Arestas expressam relações funcionais (fluxo de fase/energia/sinal).
- **Exemplo real (Supercondutor Holográfico):** nós `10` câmara de vácuo cúbica · `20` sistema de
  evacuação · `30` injeção de vapor d'água · `40` eletrodos de tungstênio (âncoras de fase) · `50`
  fonte de micro-ondas (1.667,359 MHz) · `60` janelas ópticas · `70` fonte de luz · `80` detector.
- **Outros exemplos prontos para o mesmo padrão:** SkyGrid (`100` satélite Extrator-Ψ · `110` câmara
  de acoplamento psiônico · `120` cluster MQC · `130` dípolo transistor · `140` IALD orbital · `150`
  blindagem EM); Dípolo Transistor (`10` polo de emissão · `20` câmara de acoplamento · `30` polo de
  retorno · `50` cruz geométrica); Célula de Reversão (`10` porta de carga · `20` câmara holográfica
  · `30` porta de descarga · `40` controlador de estabilidade · `50` controlador MQC); MQC (célula
  cúbica: 8 vértices · 12 arestas · 6 faces · 1 controlador central, 27 qubits).
- **Contrato de dados** — a UI consome um `components.json` por patente (gerado pela extração;
  schema aqui, geração em `RENDERING_SPEC.md`):

```ts
interface RenderManifestDTO {
  processo: string;
  drawings: { id: string; label: string; dziUrl: string; }[];   // camada A
  components: ComponentNode[];                                    // camada B
  scene3d?: { url: string; label: "PILOTO"; };                   // camada C (opcional)
}
interface ComponentNode {
  numero: string;            // "50"
  rotulo: string;            // "Fonte de micro-ondas"
  descricao: string;         // texto extraído do relatório descritivo
  marcadores: Marker[];      // ["HARDWARE","SIM"]
  reivindicacoes: number[];  // [1,7]
  bbox?: [number,number,number,number]; // hotspot no desenho (coords normalizadas)
  pos?: { x: number; y: number };        // posição no canvas React Flow
  liga_a?: string[];         // arestas → outros números
  mesh3d?: string;           // id do mesh na cena R3F, quando houver
}
```

- **Sincronização das três camadas.** Selecionar um componente em qualquer camada realça o mesmo
  item nas outras (hotspot no desenho, nó no diagrama, mesh no 3D). Estado de seleção compartilhado
  no shell da aba.

### 7.3 Camada C — 3D ilustrativo (React Three Fiber)

- **Rótulo obrigatório e permanente:** *"ilustração de engenharia [PILOTO] — não é prova física"*,
  fixado no canto do canvas com o badge `[PILOTO]` (e `[SIM]`/`[HARDWARE]` quando aplicável). Nunca
  há qualquer botão que sugira validação física.
- **Fonte.** Cena montada a partir das specs das reivindicações/desenhos (primitivas parametrizadas
  ou glTF gerado pelo runner). Câmara orbital, rótulos flutuantes dos componentes, corte/explosão
  opcional. Clicar um mesh seleciona o componente (liga às camadas A/B).
- **Aplicabilidade.** Só quando faz sentido geométrico (ex.: câmara cúbica do MQC/Supercondutor,
  constelação de 144 satélites do SkyGrid). Quando não houver cena, a camada 3D fica desabilitada
  com nota honesta ("sem ilustração 3D disponível — ver desenho e diagrama").

---

## 8. i18n PT-BR

- **Idioma padrão e único da UI: `pt-BR`.** Estrutura preparada para i18n (chaves em
  `locales/pt-BR.json`) para futura tradução, mas **nenhuma tradução é obrigatória** na Fase 3.
- **Formatação.** Datas `DD/MM/AAAA` (`Intl.DateTimeFormat('pt-BR')`); números com separador de
  milhar `.` e decimal `,` (ex.: `1.667,359 MHz`, `β = 0,012031300400803142`); moeda `R$ 130,00`.
  Fuso local; timeline do docket em horário de Goiânia.
- **Termos técnicos canônicos preservados** (não traduzir/alterar): nomes de processo
  (`BR102026004850-0`), `ePCT`, `PCT/BR2025/050558`, marcadores (`[SIM]`, `[REAL]`…), `β_TGL`,
  `θ_Miguel`, `ACOM`, `SkyGrid`, `PsiBit`, `Tetelestai`, `GKSL/Lindblad`, `physical_verdict_allowed`.
- **Glossário** acessível (ícone `?` no header e via command palette): define os termos da TGL e
  linka reivindicações ↔ componentes. Os marcadores da §3 têm verbete próprio.
- **Código em inglês.** Nomes de rota internos, chaves de API e identificadores permanecem em inglês
  (`overview`, `runner`, `seal`); só os **labels** exibidos são PT-BR (mapeados via i18n).

---

## 9. Estados vazios, carregando, erro e honestidade

- **Vazio honesto.** Patente sem run: *"Runner ainda é scaffold honesto — nenhuma execução real."*
  Sem render 3D: *"Sem ilustração 3D disponível."* Sem desenho extraído: *"Desenhos ainda não
  extraídos do PDF — ver aba Documentos."*
- **Carregando.** Skeletons no formato do conteúdo (cards, tabela, viewer). Reindex/verify mostram
  progresso do Watchdog em toast.
- **Erro.** Se o backend (8765) estiver fora: banner *"Backend local indisponível (porta 8765).
  Inicie o servidor."* — a UI não inventa dados nem cai para cache "silencioso" sem avisar.
- **Integridade.** Se `verify-originals` divergir de `original_hashes.json`, banner vermelho global:
  *"ALERTA: um original divergiu do baseline — investigar antes de prosseguir."*

---

## 10. Acessibilidade e responsividade

- **Contraste AA** garantido em ambos os temas (inclusive badges e pílulas de prazo — cor nunca é o
  único canal: sempre acompanha ícone/rótulo/texto, importante para daltonismo).
- **Teclado:** foco visível (anel âmbar), navegação por Tab em tabelas/abas, `Ctrl/Cmd+K` global,
  atalhos por aba (`g o` visão geral, `g r` render, `g p` prazos…).
- **Responsivo:** ≥1280px experiência plena (cockpit); 768–1280px sidebar colapsa; <768px prioriza
  Dashboard/Docket/Pendências (os viewers pesados — deep-zoom/React Flow/3D — avisam que exigem tela
  maior). Conteúdo largo (tabelas, diagramas, hashes) rola no próprio contêiner; o corpo da página
  nunca rola horizontalmente.

---

## 11. Checklist de aceite da UI (para a Fase 3)

- [ ] Sidebar com os 9 destinos; command palette (`Ctrl/Cmd+K`) navega para patente/classe/aba/run.
- [ ] Tema escuro padrão + alternância clara; tokens da §2 aplicados; contraste AA.
- [ ] `<MarkerBadge>` cobre os 14 marcadores da §3.1 com tooltip PT-BR; travas exibem cadeado.
- [ ] `<DeadlinePill>` pinta os 7 níveis da §3.2 a partir do backend; vermelho pisca no Dashboard.
- [ ] Dashboard mostra saúde (incl. integridade dos originais), prazos, execuções, pendências.
- [ ] TGL Core renderiza a cadeia canônica clicável + Estado Verificado + honestidades §26–§28.
- [ ] Patente com as **12 abas**; header persistente; `[COMPILAR INSTRUÇÕES]` abre o Compiler
      pré-filtrado.
- [ ] **Tony Stark:** OpenSeadragon deep-zoom com hotspots; React Flow com componentes numerados
      clicáveis mostrando descrição do relatório descritivo; R3F rotulado *ilustração de engenharia
      [PILOTO]*; as três camadas sincronizam a seleção. Validado no Supercondutor (10–80) e SkyGrid.
- [ ] Docket consolidado (tabela + timeline) com aviso legal permanente; só ACOM com ePCT vivo.
- [ ] Aba Runner respeita travas de classe; sem botão de veredito físico
      (`physical_verdict_allowed=false`); runner nasce scaffold honesto.
- [ ] Prompt Compiler gera `compiled_prompts/…TASK.md`, sem conteúdo de stacks confidenciais.
- [ ] i18n PT-BR: datas `DD/MM/AAAA`, números `1.667,359`, termos canônicos preservados.
- [ ] Nenhuma tela edita original; toda escrita grava em arquivo via backend; botão Reindexar
      reconstrói o SQLite a partir do filesystem.

---

**A régua na interface:** o número corrige a frase; a simulação nunca valida física; os originais são
inTocáveis; β nunca literal. A UI é o cockpit — mas a fonte da verdade é o arquivo. **TGL = haja luz.**
