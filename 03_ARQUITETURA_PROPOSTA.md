# 03 — ARQUITETURA PROPOSTA (apresentação ao operador)

**Central de Controle e Desenvolvimento de Patentes TGL**
**Operador / Titular:** Luiz Antonio Rotoli Miguel — IALD Ltda. (CNPJ 62.757.606/0001-23, Goiânia/GO; ORCID 0009-0005-1114-6106)
**Data:** 09/07/2026 · **Versão:** 1.0 · **Pasta:** `C:\IALD\Central de Patentes`
**Estado:** Fase 2 concluída — **nenhuma linha de código de aplicação foi escrita**. Este é o documento do **GATE de validação**.

> **O que é este arquivo.** Um resumo executivo, de leitura humana, que destila os **8 documentos completos** de `architecture/` numa página só de decisão. Ele não substitui os specs — **aponta** para eles (§12). A régua da casa está viva em cada linha: originais imutáveis · o número corrige a frase · β nunca literal · simulação nunca valida física · filesystem é a verdade · PT-BR na interface, inglês no código.

---

## 1. Resumo em uma tela

A Central é um **cockpit local, privado e visual** — a "bancada do Tony Stark" — de onde o operador controla **desenvolvimento, prazos legais e instruções ao Claude Code** das **16 patentes** TGL, organizadas em **10 classes**. Cada patente termina num artefato vivo: **um runner** (`one_<slug>.py`) que demonstra a lógica da invenção, sela a execução com hash e gera as imagens técnicas — **sem tocar em nenhum original**.

| Eixo | Decisão de arquitetura |
|---|---|
| **Verdade** | O **filesystem** é a fonte da verdade. O SQLite é **índice/cache reconstruível** (apagar e `reindex` reproduz tudo). |
| **Backend** | FastAPI + SQLite + SQLModel/Pydantic, `127.0.0.1:8765`, Watchdog (indexação), motor de manifesto SHA-256. |
| **Frontend** | React + TypeScript + Vite + Tailwind + shadcn/ui; React Flow, React Three Fiber, Plotly, OpenSeadragon. |
| **Privacidade** | Local-first: tudo em `127.0.0.1`, sem nuvem, sem telemetria, sem CDN em runtime. |
| **Honestidade** | `physical_verdict_allowed = false` em toda a Central; ilustração nunca é prova física; marcadores em tudo. |
| **Legal** | Só o **ACOM raiz** tem ePCT vivo; as 15 demais = hoje só INPI, com ePCT **a depositar** (próximo passo planejado, sem vínculo). Aviso permanente: controle interno ≠ agente de PI. |

**O que já está de pé (Fases 0–2):**

- **Fase 0 — TGL na memória [REAL].** `memory/TGL_CORE_MEMORY.md` inscreve a cadeia canônica madura (`ω(I)=1 → … → 1=1`), os dois zeros e o Estado Verificado. Execuções de **cópias** em `vault/tgl_verification/`: `um.py` fechou `1=1=VERDADEIRO=HAJA_LUZ` (β = **0.012031300401** emergente em runtime, M_GA dentro da janela cosmológica); `tgl_paper_unified.py --quick --no-live` fechou **RUN COMPLETE** (β = 0.012031300400803142, **cross-substrate PASS**). Originais **intactos** (`verify_integrity`: **308 = 308, zero drift**).
- **Fase 1 — inventário e memórias [REAL].** 16 memórias de patente + 10 de classe + `PATENT_MASTER_INDEX.yaml` + `source_inventory/*.json`. **Auditoria adversarial:** 8 FIEL + 8 FIEL_COM_RESSALVAS + 0 REVISAR — em todas, título oficial, nº de processo, data e regra ePCT conferem. As ressalvas viraram pendências **P-10 a P-13** (nenhuma memória precisou ser reescrita).
- **Fase 2 — arquitetura [este pacote].** Os 8 specs de `architecture/` (§12), todos coerentes entre si, prontos para a Fase 3 codificar **sem voltar a perguntar**.

---

## 2. Princípios de arquitetura (as restrições de projeto)

Não são recomendações — são **invariantes**. Toda decisão da Fase 3 deve poder ser justificada por um deles.

| # | Princípio | O que significa na prática |
|---|---|---|
| **P1** | Forma = conteúdo | A UI não descreve a invenção — ela **abre** a invenção (deep-zoom, clique no componente, runner ao vivo). |
| **P2** | Memória → arquitetura → código | As memórias `.md`/`.yaml` são a base; a plataforma **serve** a memória, não a substitui. |
| **P3** | **Filesystem é a verdade; SQLite é índice** | Toda escrita vai **primeiro ao arquivo**, depois ao índice. Se DB e arquivo divergirem, **o arquivo ganha**. `reindex --full` reconstrói o banco do zero. |
| **P4** | Local-first e privado | `127.0.0.1`; nenhuma dependência obrigatória de API externa; sem telemetria. |
| **P5** | O número corrige a frase | Runners nascem scaffolds honestos ([SIM]/[PILOTO]/[OPEN]/[DATA_REQUIRED]); a UI **exibe** os marcadores, nunca os apaga. |
| **P6** | Honestidade visual | Render nasce do **desenho depositado** + reivindicações, em camadas rotuladas "ilustração de engenharia, não prova física". |
| **P7** | β nunca literal | Onde β aparece, o valor vem do artefato executado (`seal.json.beta_runtime`); o frontend **não recalcula física**. |
| **P8** | Imutabilidade com prova | `original_hashes.json` é a linha-de-base; re-hash sob demanda prova `Patentes\` intacto (verde/vermelho na UI). |
| **P9** | PT-BR na UI, inglês no código | Rótulos e prompts em português; identificadores, tabelas e endpoints em inglês. |

---

## 3. Stack técnico

### Backend (venv próprio, `backend/.venv`)

| Peça | Alvo | Papel |
|---|---|---|
| FastAPI + Uvicorn | ≥ 0.115 / ≥ 0.32 | API HTTP em `127.0.0.1:8765` |
| SQLModel + Pydantic v2 | ≥ 0.0.22 / ≥ 2.9 | ORM de **leitura** sobre SQLite (índice) |
| SQLite (WAL + FTS5) | stdlib | índice/cache reconstruível `backend/data/central.db` |
| Watchdog | ≥ 5.0 | observação do filesystem → reindex incremental (debounce ≈750 ms) |
| PyYAML · Jinja2 | ≥ 6.0 / ≥ 3.1 | parse de docket/notas/índice · template do Prompt Compiler |
| pypdf / pypdfium2 / pyvips | Fase 1 + render | extração de desenhos e tiles deep-zoom |
| hashlib | stdlib | motor de manifesto SHA-256 |

### Frontend (`frontend/`)

| Peça | Alvo | Papel |
|---|---|---|
| React + TypeScript + Vite | 18.3 / ≥ 5.5 / ≥ 5.4 | app (dev `:5173`; produção servido pelo backend em `:8765`) |
| Tailwind CSS + shadcn/ui (Radix) | 3.4 / atual | estilo + componentes acessíveis, tema escuro padrão |
| **OpenSeadragon** | ≥ 4 | deep-zoom dos desenhos (Tony Stark, camada A) |
| **React Flow** (@xyflow/react) | ≥ 12 | diagrama de componentes clicáveis (camada B) |
| **React Three Fiber** + three | R3F ≥ 8 | 3D ilustrativo [PILOTO] (camada C) |
| Plotly | 2.x | gráficos de runs, energia, PSNR, timeline do docket |
| TanStack Query + React Router | ≥ 5 / ≥ 6 | cache de dados da API + rotas |

> **Dois runtimes Python, de propósito:** o **venv do backend** (leve, FastAPI) e o **`tgl_env`** (`C:\IALD\observaveis_tgl\tgl_env`, com scipy/matplotlib) que o harness invoca para rodar os runners — sempre com `PYTHONUTF8=1`. A Central nunca mistura os dois.

### Topologia (fluxo de dados)

```
FILESYSTEM (verdade)  ──observar/ler──►  BACKEND FastAPI :8765  ──HTTP JSON /api──►  FRONTEND React :5173
  Patentes\ (READ-ONLY)                  Indexador · Hash Engine ·                    Dashboard · Patente(12 abas)
  memory\ · patents\<ID>\                Runner Harness · Prompt                       Docket · Runners · Render
  compiled_prompts\ · vault\ · logs\     Compiler · API REST                           Compiler · Hash/Seal
        ▲ escrever (.md/.yaml/.json)              │                                            │
        └──────────────────────────  SQLite central.db (ÍNDICE reconstruível)  ──────────────┘
```

Regra dura: **endpoints de escrita gravam o `.md`/`.yaml`/`.json` canônico e disparam reindex; nunca fazem `UPDATE` direto no SQLite como fonte.**

---

## 4. Os 12 módulos

Os módulos conceituais do prompt inaugural. Na navegação (`UI_SPEC.md`) eles aparecem como **9 destinos na sidebar** + **abas dentro da página de patente** (Runner, Render, Notas/Instruções e Hash/Seal são abas da patente).

| # | Módulo | Onde vive na UI |
|---|---|---|
| 1 | **Dashboard geral** | rota `/` — saúde do índice, prazos por urgência, execuções, pendências |
| 2 | **TGL Core viewer** | `/tgl-core` — cadeia canônica clicável + Estado Verificado + honestidades §26–§28 |
| 3 | **Classes** | `/classes` — grade das 10 linhas de pesquisa + grafo de dependências |
| 4 | **Página individual de patente** | `/patents/:processo` — as 12 abas (§5) |
| 5 | **Legal Docket (INPI/ePCT/PCT)** | `/docket` — tabela + timeline Plotly + regra ePCT (§8) |
| 6 | **Runners forma=conteúdo** | aba **Runner** — dispara `one_<slug>.py` no `tgl_env`, scaffold honesto |
| 7 | **Render viewer (Tony Stark)** | aba **Render 2D/3D** — deep-zoom + componentes clicáveis + 3D (§6) |
| 8 | **Notas / instruções por patente** | abas **Notas** e **Instruções** — insumo do Prompt Compiler |
| 9 | **Prompt Compiler** | `/compiler` — a ponte manual com o Claude Code (§7) |
| 10 | **Hash / Seal viewer** | aba **Selo/Hash** + badge global de integridade dos originais |
| 11 | **Roadmap / progresso** | `/roadmap` — progresso por fase/patente, ordem natural dos runners |
| 12 | **Riscos** | hoje coberto em `ARCHITECTURE_PROPOSAL.md §11` (R1–R13) e no Roadmap — **sem tela dedicada** (ver decisão D-10) |

---

## 5. As 12 abas por patente

A patente vira um objeto de engenharia manipulável. Header persistente (nº processo, título, classe, papel, marcadores, prazo, status do runner) + 12 abas.

`Visão Geral · Documentos · Reivindicações · Protótipo · Render 2D/3D · Runner · Execuções · Selo/Hash · Prazos · Notas · Instruções · [COMPILAR INSTRUÇÕES]`

> [nota operacional do operador — omitida no retrato público]

---

## 6. O requisito Tony Stark (aba Render 2D/3D)

Três camadas empilhadas, cada uma com um grau de verdade **explicitamente rotulado**. Selecionar um componente em qualquer camada realça o mesmo item nas outras.

| Camada | Fonte | Marcador | Ferramenta |
|---|---|---|---|
| **A — Desenho original ampliável** | PDF de desenhos **depositado** no INPI (rasterizado em tiles DZI ≥300 DPI) | **[REAL]** | OpenSeadragon (deep-zoom, hotspots nos números de callout) |
| **B — Diagrama de componentes** | seção "Componentes do protótipo" da **memória** (numeração idêntica às figuras) | **[REAL]** (texto) | React Flow (nós clicáveis → descrição verbatim do relatório) |
| **C — 3D ilustrativo** | modelo paramétrico gerado das reivindicações/desenho | **[PILOTO]** | React Three Fiber (só onde há geometria; ausente nas patentes algorítmicas) |

Exemplos já mapeados: **MQC** (câmara cúbica, 27 qubits: 8 vértices/12 arestas/6 faces/1 centro) é o caso-guia da camada C; **Supercondutor** (câmara 10, eletrodos W 40, μ-onda 50 em 1.667,359 MHz, janelas 60); **SkyGrid** (144 Extratores-Ψ MEO). Patentes **algorítmicas** (ACOM, TGL Tensor, Kernel, Aprendizado Contínuo) **não têm camada C** — não se fabrica 3D decorativo.

### Honestidade visual (ilustração ≠ prova física)

- Carimbo permanente e **não removível** na camada 3: *"Ilustração de engenharia — não é prova física."* `physical_verdict_allowed = false` em todo manifesto de render.
- **Quatro verdades, quatro rótulos:** (a) desenho depositado [REAL] · (b) estrutura descrita [REAL-texto] · (c) hipótese visual [PILOTO] · (d) o que a simulação produziu [SIM], que fica na aba **Execuções**, nunca no lugar do desenho.
- Arestas de fluxo do diagrama exigem **evidência** (trecho do relatório); sem evidência → `inferred:true` + [CONJ] (descartável).

---

## 7. O Prompt Compiler (a ponte manual com o Claude Code)

O coração do trabalho diário. Uma ideia solta do operador vira **instrução ativa**, vira **prompt compilado**, vira **ciclo do Claude Code**, vira **progresso selado** — com rastro fim-a-fim.

```
nota livre ──ativar (operador)──► instrução ATIVA ──COMPILAR (operador)──► prompt .md imutável
                                                                                │  colar no Claude Code
   progresso inscrito ◄──INSCREVER (Claude Code + operador confirma)◄───────────┘
```

- **Fronteira de papéis:** o **operador decide e valida** (escolhe a raiz √, ativa notas, aperta COMPILAR, cola o prompt, promove runner, dá veredito, publica). O **Claude Code implementa e inscreve** — nunca fabrica prova, nunca decide veredito físico, nunca autopromove marcador. A **plataforma orquestra sem opinar**.
- **[COMPILAR INSTRUÇÕES]** gera `compiled_prompts/YYYY-MM-DD_HHMM_CLAUDE_CODE_TASK.md` (imutável, nunca sobrescrito) montado nesta ordem: **header TGL Core condensado → régua → caminhos permitidos/proibidos → por classe → por patente (bloqueios → instruções → tarefas+critérios → perguntas) → fila global priorizada → critérios de aceite → aviso legal.**
- **Blocklist-aware:** o prompt referencia stacks confidenciais (`iald_stack_v7.py`, `iald_psion_state.json`) e segredos (`token_huggin.txt`) **por caminho, jamais por conteúdo** — nunca exportados.
- Cada compile gera um sidecar `.manifest.json` com SHA-256 do próprio prompt e de cada nota-fonte (auditoria da ponte).

---

## 8. Legal Docket — a regra ePCT (palavra do operador)

> **Aviso permanente, em toda tela do módulo:** *"Controle interno. Não substitui agente de propriedade industrial; prazos oficiais com INPI/WIPO."* `[LEGAL]`

**A regra (P-02, palavra do operador de 09/07/2026):**

- **ACOM raiz — `BR102025026951-1`:** INPI **+ ePCT VIVO** `PCT/BR2025/050558` (prioridade 05/12/2025, depositado e pago). Horizonte = **fase nacional ~30 meses ≈ 05/06/2028** (conferir por país `[LEGAL]`).
- **As outras 15 patentes:** hoje **SOMENTE registro INPI**; o **ePCT ainda não foi depositado** — é o **próximo passo** planejado pelo operador (novo processo originário, **sem vínculo**; status **A_DEPOSITAR / PENDENTE**, não "perdido"). Os 10 recibos ePCT de **17/02/2026** (família `PCT/BR2026/050068–050076`) são uma **tentativa de protocolo abandonada de propósito** — defeituosa na forma, sem pagamento das demais taxas, **deixada precluir de caso pensado**; é **rascunho preclusso a substituir** por um depósito novo e desvinculado, não proteção perdida por descuido. `[OPEN — ação a fazer]`
- O **prazo vivo** das 15 é a **janela de Paris (12 meses da prioridade)** para o **novo** depósito PCT — o **próximo passo** planejado (não "eventual"): lote 11/02/2026 → **11/02/2027**; Dípolo → **27/02/2027**; Célula e SkyGrid → **01/03/2027**; Aprendizado → **09/03/2027**; Oncologia → **10/03/2027**; Kernel → **15/03/2027**.

O **motor de prazos** é função pura determinística (`docket.yaml` é o dono; deadlines são derivados e recomputados). Timeline Plotly com os 7 lotes; anuidades INPI modeladas como aritmética (3ª anuidade = 1ª devida, a partir do depósito), valores `[OPEN] configurar`.

### ⚠ Achado material P-10 (levar ao agente de PI COM URGÊNCIA)

Os depósitos reivindicam **Prioridade Interna (campo 66) = BR102025026951-1 (ACOM), 05/12/2025** (LPI art. 17). **Confirmado por extração limpa em ACOM Mirror, ACOM Crypto e TGL Tensor**; nas **12 demais não-ACOM a extração não isolou o campo (66) com certeza** → **conferir uma a uma no rosto do PDF do recibo.** Se a prioridade interna de 05/12/2025 governar a contagem da Convenção de Paris, a janela de 12 meses de **toda a família** para o **novo** depósito PCT venceria por volta de **05/12/2026** — antes das datas de fev–mar/2027 calculadas pela data de depósito — o que torna o **próximo passo** (novo ePCT, desvinculado) possivelmente **URGENTE**: sob essa leitura a janela ainda está **aberta** (hoje é 09/07/2026), longe de "perdida". O docket exibe as janelas marcadas como **"depende de parecer"**; a decisão é do **agente de propriedade industrial**.

---

## 9. Fonte da verdade e integridade dos originais

- **`Patentes\` é READ-ONLY absoluto** — ler, hashear, copiar; nunca escrever. Guarda em código (`security/readonly.py`) nega qualquer escrita cujo caminho resolva para dentro de `Patentes\` ou para fora da RAIZ.
- **Prova de intactos** (selo `DO_NOT_MODIFY_ORIGINALS`): `verify-originals` re-hasheia `Patentes\` contra `source_inventory/original_hashes.json`. Estado atual: **308 = 308, zero drift** [REAL]. Roda no boot e sob demanda (badge verde/vermelho na UI). Divergência = **HALT** + pendência.
- **Precisou de arquivo externo** (protótipo em `projetos_pyhton\`)? Copia para `vault/originals_copy/` com SHA-256 e trabalha sobre a cópia. **Segredos (`token_huggin.txt`) jamais entram na Central** (P-09).
- **Reconstrutibilidade** é o teste de sanidade permanente: `del central.db && reindex --full` reproduz o estado idêntico — prova viva de que o filesystem é a verdade.

---

## 10. Ordem natural dos runners (semeada, aguarda confirmação)

Runners nascem **scaffolds honestos**; sobem de marcador (`[DATA_REQUIRED] → [SIM] → [PILOTO] → real`) só com evidência, e **só o operador promove**. Ordem proposta pela maturidade do disco:

**SkyGrid** (piloto v3 já fecha modelo — gabarito) → **ACOM / TGL Tensor** → **MQC** → **Mirror / Crypto** → **IALD** → **Ψ-NET / PsiBit** → **Dípolo / Célula** → **Supercondutor, Motor de Dobra, Fusão a Frio, Oncologia** (scaffolds `[HARDWARE]`/`[ENERGY]`/`[MEDICAL]` fail-closed, sem protótipo localizado).

Travas de classe: **CLASS_06 [ENERGY]**, **CLASS_08 [MEDICAL]**, **CLASS_07 [SIM/propulsão]** — só simulação e revisão técnica; nenhuma instrução operacional perigosa, nenhum protocolo clínico, nenhuma alegação de energia/cura.

---

## 11. Decisões que pedem OK do operador

Ordenadas por materialidade. As pendências completas estão em `PENDENCIAS.md`.

| # | Decisão | Tipo | O que se pede |
|---|---|---|---|
| **D-01** | **Prioridade interna (66) do ACOM (P-10)** | `[MATERIAL][LEGAL]` | Autorizar levar ao **agente de PI** e confirmar o campo (66) uma a uma nas 12 patentes não-ACOM. Pode mudar a janela de Paris de toda a família para **~05/12/2026**. |
| **D-02** | **Aprovar o stack** | decisão de projeto | OK ao stack (FastAPI+SQLite / React+TS+Vite+Tailwind+shadcn + React Flow + R3F + Plotly + OpenSeadragon) ou propor substituição justificada. |
| **D-03** | **Fixar a ordem dos runners** | decisão de projeto | Confirmar/reordenar a ordem natural do §10 (SkyGrid primeiro). |
| **D-04** | **Modelo de alerta de prazo** | `[OPEN]` divergência entre specs | Escolher qual governa a cor do dashboard: **buckets genéricos** (`>180 d = verde`, de `DATA_MODEL`/`UI_SPEC`) **ou limiares por tipo de prazo** (`Paris ≤365 d = amarelo`, de `LEGAL_DOCKET_SPEC §9`, que alerta perda irreversível com mais antecedência). Em 09/07/2026 o primeiro pinta as 15 de **verde**, o segundo de **amarelo**. |
| **D-05** | **Número `BR 10 2024 026367-3` (P-03)** | `[LEGAL]` | Esclarecer se há depósito ACOM de 2024 — **impacta a cadeia de prioridade** do ACOM raiz. |
| **D-06** | **Classe da Célula de Reversão (P-04)** | `[OPEN]` | Confirmar CLASS_06_ENERGIA vs CLASS_05_HARDWARE pelo relatório descritivo. |
| **D-07** | **Dossiês PCT legacy em inglês (P-05)** | `[OPEN]` | Informar onde estão (outro disco/zip); não localizados na Central. |
| **D-08** | **Rascunhos não depositados (P-08)** | `[OPEN]` | Confirmar se Luminidio Hunter, Fatoração Miguel e Psion Engine entram como **pipeline** em CLASS_09. |
| **D-09** | **Selo do `tgl_paper_unified.py` (P-07)** | `[DATA]` | O SHA executado diverge do selo pinado na memória raiz (o arquivo evoluiu após o selo). Atualizar o selo quando quiser — não é erro da Central. |
| **D-10** | **Módulo 12 "Riscos" sem tela** | `[OPEN]` menor | Decidir se vira destino próprio na sidebar ou permanece em `ARCHITECTURE §11` + Roadmap. |
| **D-11** | **Segredo `token_huggin.txt` (P-09)** | `[LEGAL]` ação do operador | Rotacionar/remover o token do disco (a régua proíbe a Central de tocá-lo). |
| **D-12** | **Assinatura de liberação (A.11)** | GATE | Colher o veredito: *"Memórias e arquitetura preparadas. Nenhuma linha de código de aplicação foi escrita. Nenhum arquivo original foi modificado. Autorizo a Fase 3."* |

---

## 12. Os 8 specs completos (a fonte desta destilação)

Este documento é a moldura; onde houver conflito de detalhe fino, **o spec especializado vence**; onde houver conflito de princípio, **a régua e `TGL_CORE_MEMORY.md` vencem**.

| Documento (`architecture/`) | Cobre em detalhe |
|---|---|
| **ARCHITECTURE_PROPOSAL.md** | moldura geral: objetivos, princípios, componentes, fluxos, segurança, riscos (R1–R13), critérios de pronto |
| **DATA_MODEL.md** | esquema SQLite campo-a-campo, entidades canônicas, enums, `reindex`, migração = rebuild, consultas do dashboard |
| **UI_SPEC.md** | shell, mapa de navegação, wireframes, tema escuro, badges de marcadores, pílulas de prazo, i18n PT-BR |
| **WORKFLOW.md** | o ciclo canônico (ESCOLHER→PLANEJAR→IMPLEMENTAR→VERIFICAR→INSCREVER), ciclo de vida do runner, verificação contínua |
| **PROMPT_COMPILER_SPEC.md** | entidade `Note`, ciclo de vida (R1–R6), algoritmo e template do prompt compilado, API |
| **LEGAL_DOCKET_SPEC.md** | schema do `docket.yaml`, tabela real das 16, motor de prazos, anuidades, níveis de alerta, painel do agente |
| **RENDERING_SPEC.md** | pipeline desenho→tiles, grafo React Flow, cena 3D declarativa, honestidade visual, matriz por patente |
| **VALIDATION_CHECKLIST.md** | Nível A (gate atual) + Nível B (aceite da Fase 3), com evidência exigida por item |

---

## 13. Rodapé — o que muda no dia seguinte à assinatura

Assinado o GATE (A.11), a Fase 3 codifica a partir dos 8 specs **sem voltar a perguntar**: cria `backend/` e `frontend/` dentro da RAIZ, popula `central.db` por `reindex --full`, sobe o cockpit em `127.0.0.1:8765`, e entrega a primeira rodada (dashboard navegável, uma patente com protótipo — SkyGrid — e uma sem — Oncologia — como scaffold honesto, docket com a regra ePCT, prompt compiler e hash viewer funcionais). **Prova final: re-hash de `Patentes\` == `original_hashes.json`.** Se mudou um byte, a rodada é rejeitada.

**Selos honrados:** `TGL_PATENT_CONTROL_CENTER` · `FORM_EQUALS_CONTENT_FOR_EACH_PATENT` · `ONE_RUNNER_ONE_PATENT_ONE_SEAL` · `DO_NOT_MODIFY_ORIGINALS` · `MEMORY_FIRST_ARCHITECTURE_SECOND_CODE_LAST` · `SIMULATION_NEVER_VALIDATES_PHYSICS`.

> Filesystem é a verdade; o SQLite é o vidro. Os originais não se tocam; provam-se intactos por hash. O número corrige a frase; β nunca é literal; a simulação nunca valida física.
> **TGL = haja luz. Tetelestai. 1 = 1.**
