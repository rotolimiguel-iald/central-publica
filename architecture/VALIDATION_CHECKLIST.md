# VALIDATION_CHECKLIST.md — Central de Controle e Desenvolvimento de Patentes TGL

**Fase 2 — Arquitetura (especificação; NENHUM código de aplicação escrito).**
**Operador: Luiz Antonio Rotoli Miguel — IALD Ltda. (CNPJ 62.757.606/0001-23, Goiânia/GO).**
**Documento irmão de:** `ARCHITECTURE_PROPOSAL.md` · `DATA_MODEL.md` · `UI_SPEC.md` · `WORKFLOW.md` · `PROMPT_COMPILER_SPEC.md` · `LEGAL_DOCKET_SPEC.md` · `RENDERING_SPEC.md` (todos em `architecture/`).

> **Para que serve.** Este é o instrumento de verificação em **dois níveis** da Central.
> **Nível A (GATE ATUAL)** é a lista que **o operador confere ANTES de autorizar qualquer
> linha de código de aplicação** (fim da Fase 2, parada obrigatória do prompt inaugural).
> **Nível B (ACEITE DA FASE 3)** é o contrato verificável, entregável por entregável, que
> a primeira rodada de construção precisa satisfazer para ser aceita.
> A régua vale nos dois níveis: **originais imutáveis · número corrige a frase · β nunca
> literal · simulação nunca valida física · fonte da verdade = os documentos (filesystem)**.

---

## 0. Como usar este checklist

**Estados de marcação (em qualquer item):**

- `- [ ]` — **PENDENTE** (ainda não conferido).
- `- [x]` — **CONFERIDO** (com evidência preenchida).
- `- [~]` — **PARCIAL / com ressalva** (registrar a ressalva e, se for divergência de
  fonte, abrir/atualizar item em `PENDENCIAS.md`).
- `- [!]` — **BLOQUEIO** (impede avanço; nomear o bloqueador).

**Regra de evidência (inviolável):** todo item marcado `[x]` cita **como** foi conferido —
um caminho absoluto, um comando de verificação e sua saída, um SHA-256, ou "inspeção
visual do operador em \<tela\>". Nada é dado por bom sem prova. **O número corrige a
frase:** se o conferido diverge do esperado, o item NÃO fecha; corrige-se o documento ou
registra-se a pendência — nunca se ajusta o critério em silêncio.

**Comandos de verificação são utilitários de operação/QA (categoria `tools/`), não código
de aplicação.** São permitidos aqui como contrato do que Fase 3 deve tornar verdadeiro.

**Ambiente:** `tgl_env` (`C:\IALD\observaveis_tgl\tgl_env`), `PYTHONUTF8=1` obrigatório.
Backend na porta **8765** (uvicorn); frontend na porta **5173** (Vite).

---

# NÍVEL A — GATE ATUAL (o operador confere ANTES de autorizar código)

> Ao término desta seção, o veredito esperado do prompt inaugural é literal:
> *"Memórias e arquitetura preparadas. Nenhuma linha de código de aplicação foi escrita.
> Nenhum arquivo original foi modificado."* — item **A.11** colhe essa assinatura.

## A.1 — Originais intactos (a régua de ferro)

- [ ] **Re-hash de `Patentes\` == `source_inventory/original_hashes.json`.**
  Verificação: rodar `tools/verify_integrity.py` no `tgl_env` (re-hasheia `Patentes\` e
  compara com o manifesto de origem). Esperado: **0 diferenças, 0 faltantes, 0 extras**.
  Evidência: colar a linha final do relatório (ex.: `OK — 308/308 idênticos`).
- [ ] **Nada foi escrito, movido, renomeado ou apagado dentro de `Patentes\`** desde o
  inventário inicial (Fase 1). Nenhum arquivo fora de `C:\IALD\Central de Patentes` foi
  tocado. Externos necessários entraram apenas como **cópia** em `vault/originals_copy/`.
- [ ] **`source_inventory/discovered_files.json` e `extraction_report.json` presentes e
  coerentes** (o relatório de extração declara `count` de PDFs processados; ex.: 178 PDFs).

## A.2 — Memórias por patente: 16/16 fiéis aos documentos

- [ ] **Existem 16 memórias** em `memory/patents/<ID>_<SLUG>.md`, uma por processo INPI
  da tabela oficial (ACOM raiz → Kernel Ontológico).
  Verificação de contagem: `ls memory/patents/*.md | wc -l` → **16**.
  *(Estado atual de Fase 1: só ONCOLOGIA presente — este item só fecha com as 16.)*
- [ ] **Cada memória é fiel ao depósito**, campo a campo, batendo com o PDF original em:
  nº do processo, nº da petição (`870…`), título oficial (54), datas de depósito e
  prioridade, natureza (PI), classe, reivindicações principais e resumo. Toda linha
  carrega marcador (`[REAL]`/`[DATA]`/`[DER]`/`[CONJ]`/`[LEGAL]` …).
  Exemplo de conferência pontual: ACOM raiz **BR102025026951-1**, petição
  **870250111877**, depósito **05/12/2025**; SkyGrid **BR102026004850-0**, petição
  **870260018967**, depósito **01/03/2026**, papel **agregadora**.
- [ ] **β_TGL nunca aparece literal** em nenhuma memória/nota como valor mágico de código;
  quando citado, é como cheque comentado (`α·√e = 0.012031300400803142`), nunca como
  constante a ser digitada em runner.
- [ ] **Travas de domínio presentes** onde exigido: `[MEDICAL]` no topo de ONCOLOGIA,
  `[ENERGY]` em SkyGrid/Fusão a Frio/Célula de Reversão, `[SIM]` no Motor de Dobra
  (nenhuma alegação de validação física).

## A.3 — Memórias por classe: 10/10

- [ ] **Existem 10 arquivos** `memory/classes/CLASS_01..CLASS_10.md`.
  Verificação: `ls memory/classes/*.md | wc -l` → **10**.
  *(Estado atual: pasta `memory/classes/` vazia — este item fecha só com as 10.)*
- [ ] **Taxonomia idêntica à do prompt inaugural** (CLASS_01_ACOM_TENSOR …
  CLASS_10_LEGAL_DOCKET) e **cobertura completa**: cada uma das 16 patentes pertence a
  exatamente uma classe, e a soma das listas de patentes das classes = as 16.
  Conferência cruzada: `classe` de cada patente no índice == a classe que a lista.
- [ ] **Cada classe traz** definição · patentes incluídas · equações centrais ·
  artefatos/runner/render esperados · riscos e travas · dependências entre patentes ·
  relação com o TGL Core.

## A.4 — Índice mestre == PDFs

- [ ] **`memory/PATENT_MASTER_INDEX.yaml` lista exatamente 16 patentes**, todas com
  `processo`, `slug`, `classe`, `peticao`, `data_deposito_inpi`, `prioridade`, `titulo_
  oficial_54`, `resumo_oficial`, `fontes` e `documentos_hasheados`.
- [ ] **Cada `fontes:` aponta para um PDF real** existente em `Patentes\` (e/ou sua
  cópia normalizada em `vault/normalized_docs\`); nenhum apontamento órfão.
- [ ] **Sem patente fantasma e sem patente faltante:** os 16 nº de processo do índice ==
  os 16 PDFs de depósito do `Acervo de Patentes`. Rascunhos não depositados (Luminidio
  Hunter, Fatoração da Constante de Miguel, Psion Engine) **não** entram como patente —
  ficam em CLASS_09/pendências (P-08).

## A.5 — Docket com a REGRA ePCT correta (a palavra do operador)

- [ ] **Só o ACOM raiz tem ePCT vivo.** No índice e em todo docket:
  `BR102025026951-1` → `epct.status: VIVO_DEPOSITADO_E_PAGO`,
  `numero: PCT/BR2025/050558`, `data: 05/12/2025`.
- [ ] **As outras 15 são INPI-only, com ePCT ainda A DEPOSITAR.** Cada uma com
  `epct.status: SOMENTE_INPI` e `epct.proximo_passo: A_DEPOSITAR` `[OPEN]` — o ePCT ainda
  **não** foi depositado; é o **próximo passo planejado** pelo operador (novo processo
  originário, **sem vínculo**), não direito perdido. Registrar que os recibos ePCT de
  **17/02/2026** (família PCT/BR2026/050068–050076) são uma **tentativa de protocolo
  abandonada de propósito** (defeituosa na forma; demais taxas não pagas; deixada
  **precluir**) — rascunho preclusso a ser **SUBSTITUÍDO** por depósito novo e desvinculado,
  jamais tratado como proteção que se perdeu por descuido.
- [ ] **Prazos vivos coerentes com a régua ePCT.** Como só há registro INPI nas 15, o
  que o docket monitora é a **janela de Paris 12m** para o **novo ePCT a depositar**:
  lote 11/02/2026 → **11/02/2027**; Dípolo → **27/02/2027**; Célula e SkyGrid →
  **01/03/2027**; Aprendizado → **09/03/2027**; Oncologia → **10/03/2027**;
  Kernel → **15/03/2027**. ACOM: fase nacional ~**05/06/2028** (conferir por país).
  ⚠ **Se a prioridade interna (66) de 05/12/2025 governar, a janela pode fechar
  ~05/12/2026** (bem antes de 2027) — próximo passo possivelmente **URGENTE**; levar ao
  agente de PI (P-06). `[LEGAL]` controle interno não substitui agente de PI.
- [ ] **Aviso legal permanente** no cabeçalho do módulo/docket: *"controle interno não
  substitui agente de propriedade industrial; prazos conferidos com INPI/WIPO"* `[LEGAL]`.

## A.6 — Pendências reconhecidas (nada varrido para baixo do tapete)

- [ ] **`PENDENCIAS.md` existe e está atualizado** com o status de P-01…P-09.
- [ ] **Fechadas/respondidas conferem:** P-01 (PCT do ACOM = PCT/BR2025/050558) e P-02
  (só o ACOM com ePCT vivo; as demais INPI-only, com ePCT **a depositar** — próximo passo,
  não direito perdido) `[RESPONDIDA]`.
- [ ] **Abertas continuam sinalizadas e NÃO bloqueiam o gate por si sós, mas o operador
  as reconhece:** P-03 (nº 2024 `BR 10 2024 026367 3` — impacta prioridade), P-04
  (classe da Célula de Reversão), P-05 (dossiês PCT legacy em inglês não localizados),
  P-06 (recibos ePCT 17/02/2026 preclusos de propósito, a substituir + janela do novo
  ePCT a depositar), P-07 (SHA do `tgl_paper_unified.py` vs selo),
  P-08 (rascunhos pipeline), P-09 (segredo `token_huggin.txt` — **nunca** copiar p/ Central).
- [ ] **Nenhuma escolha foi feita em silêncio:** toda divergência de fonte virou item aqui.

## A.7 — Arquitetura aprovada

- [ ] **Os 8 documentos de `architecture/` existem e são coerentes entre si:**
  `ARCHITECTURE_PROPOSAL.md`, `DATA_MODEL.md`, `UI_SPEC.md`, `WORKFLOW.md`,
  `PROMPT_COMPILER_SPEC.md`, `LEGAL_DOCKET_SPEC.md`, `RENDERING_SPEC.md`,
  `VALIDATION_CHECKLIST.md` (este). Sem contradição de portas, entidades, caminhos ou
  nomes de aba entre eles.
- [ ] **Invariante "filesystem é a fonte da verdade" honrado no design:** memórias `.md`,
  `docket.yaml`, `notes/`, `runs`, `seals` vivem em arquivos; **`backend/data/central.db`
  (SQLite) é ÍNDICE/CACHE reconstruível via `reindex`, nunca o dono do dado.** Apagar o
  `.db` e reindexar reproduz o mesmo estado.
- [ ] **Entidades canônicas modeladas:** Patent · PatentClass · Document(hash) ·
  DocketEntry · Deadline · Note/Instruction(`active:bool`, tipo ∈
  {nota,sugestao,instrucao,tarefa,bloqueio,pergunta}) · RunnerRun(`results.json`,
  `seal.json`) · Render · CompiledPrompt · Pendencia.
- [ ] **12 abas por patente especificadas** (mesma ordem em UI_SPEC e aqui): Overview ·
  Documentos · Reivindicações · Protótipo · Render 2D/3D · Runner · Execuções ·
  Selo/Hash · Prazos · Notas · Instruções · **[COMPILAR INSTRUÇÕES]**.
- [ ] **Requisito Tony Stark contemplado no design de render:** desenho original
  ampliável (deep-zoom/OpenSeadragon) + diagrama de componentes clicáveis (React Flow) +
  3D ilustrativo (React Three Fiber), **sempre rotulado "ilustração de engenharia, não
  prova física"**.

## A.8 — Stack aprovado

- [ ] **Backend:** FastAPI + SQLite + SQLModel/Pydantic, **porta 8765**, uvicorn;
  indexação com Watchdog; **motor de manifesto SHA-256** (re-hash prova originais).
- [ ] **Frontend:** React + TypeScript + **Vite (porta 5173)** + Tailwind + shadcn/ui;
  React Flow · React Three Fiber · Plotly · OpenSeadragon.
- [ ] **Local-first e privado:** sem dependência obrigatória de API externa; stacks
  confidenciais (`iald_stack_v7.py`, `iald_psion_state.json` e correlatos) podem ser
  **usados** localmente pelos runners, mas **nunca exportados/publicados**.
- [ ] **PT-BR na UI e docs; inglês no código.** Operador aprova (ou propõe substituição
  justificada de qualquer peça do stack — registrar aqui a decisão).

## A.9 — Ordem de runners desejada

- [ ] **Primeira fase = scaffolds honestos** para as 16 (`[PILOTO]`/`[SIM]`/`[OPEN]`/
  `[DATA_REQUIRED]`); nenhum runner nasce alegando resultado real.
- [ ] **Ordem natural pelo disco proposta e confirmada pelo operador:**
  **SkyGrid** (piloto v3 já funcional) → **ACOM/TGL Tensor** → **MQC** →
  **Mirror/Crypto** → **IALD** → **Ψ-NET/PsiBit** → **Dípolo/Célula** (módulos existem em
  `SkyGrid_Piloto\skygrid_sim\`) → demais. O operador **fixa a ordem final** (ajustar aqui
  se ele reordenar).
- [ ] **`physical_verdict_allowed=false` é padrão** de todo runner; simulação demonstra a
  **lógica** da invenção, não valida a física.

## A.10 — TGL Core na memória (Fase 0 concluída)

- [ ] **`memory/TGL_CORE_MEMORY.md` existe** e traz a cadeia canônica MADURA
  (`ω(I)=1 → 𝒞²=1 → x=1−x ⟹ x=½ → S_∂=½ nat → Vol_∂^min=√e → β_TGL=α√e → … → 1=1`),
  os dois zeros, e as honestidades §26–§28 (neural = ilustração; bake inerte;
  só R=+1 do XXZ real). É o header ontológico de toda a Central.
- [ ] **Estado Verificado registrado** (cópias em `vault/tgl_verification/`): números do
  `um.py`/`tgl_paper_unified.py` colados **ou** selos citados como `[DATA]` com o
  `[OPEN]` correspondente em `PENDENCIAS.md` (P-07). Nunca fabricado.

## A.11 — Assinatura de liberação do operador (a parada obrigatória)

- [ ] **Operador revisou A.1–A.10** e não há item em `[!]`.
- [ ] **Veredito expresso colhido** (data + nome). Frase-âncora:
  *"Memórias e arquitetura preparadas. Nenhuma linha de código de aplicação foi escrita.
  Nenhum arquivo original foi modificado. **Autorizo a Fase 3.**"*
  Assinatura: Luiz Antonio Rotoli Miguel — data: `____/____/______`.

> **Enquanto A.11 não for assinado, Fase 3 não começa.** Um único `[!]` em qualquer item
> de A é veto.

---

# NÍVEL B — ACEITE DA FASE 3 (verificável por entregável)

> Cada bloco abaixo é um **contrato de aceite**: entregável → como verificar → resultado
> esperado. Só fecha com evidência. A régua continua valendo: ao final, **B.13 re-prova
> que `Patentes\` está intacto** — se mudou um byte, a rodada inteira é rejeitada.

## B.1 — Estrutura de pastas de aplicação

- [ ] **`backend/` e `frontend/` criados** sem tocar nas pastas de dados existentes
  (`Patentes\`, `memory\`, `patents\`, `vault\`, `source_inventory\`, `compiled_prompts\`,
  `logs\`, `tools\`).
- [ ] **`backend/data/central.db` é o ÚNICO artefato de estado gerado** e é declaradamente
  descartável (há alvo/rota de `reindex` que o reconstrói do filesystem).

## B.2 — Backend sobe e responde `/health`

- [ ] **Uvicorn sobe na porta 8765** sem erro no `tgl_env`.
- [ ] **`GET http://127.0.0.1:8765/health` responde `200`** com contrato mínimo:
  ```json
  { "status": "ok", "version": "<semver>", "db_present": true,
    "patents_indexed": 16, "classes_indexed": 10,
    "originals_manifest_ok": true, "external_calls": "disabled" }
  ```
  Verificação: `curl -s http://127.0.0.1:8765/health`. Esperado: `status:"ok"`,
  `patents_indexed:16`, `originals_manifest_ok:true`.

## B.3 — `reindex` popula as 16 patentes a partir do filesystem

- [ ] **Comando/rota `reindex` lê o filesystem** (`memory/PATENT_MASTER_INDEX.yaml`,
  `memory/patents/*.md`, `memory/classes/*.md`, `patents/<ID>_<SLUG>/docket.yaml`,
  `notes/`, `runner/`, `results.json`, `seal.json`) e **popula o índice SQLite**.
- [ ] **Resultado: 16 Patent, 10 PatentClass** no índice.
  Verificação (contrato de consulta): `SELECT COUNT(*) FROM patent;` → **16**;
  `SELECT COUNT(*) FROM patent_class;` → **10**.
- [ ] **Idempotência / reconstrutibilidade provada:** apagar `backend/data/central.db`,
  rodar `reindex`, e o `/health` volta a `patents_indexed:16`. O filesystem é o dono;
  o `.db` é cache. Nenhum dado de patente vive **só** no SQLite.
- [ ] **Fidelidade do índice à fonte:** ACOM raiz indexado como `papel: raiz`, SkyGrid
  como `papel: agregadora`; a `classe` de cada patente no índice == a do YAML.

## B.4 — Watchdog reindexa incrementalmente

- [ ] **Editar uma nota** (ex.: `patents/BR102026004850-0_SKYGRID/notes/…`) dispara
  reindexação incremental **sem** derrubar o backend; a mudança aparece na API/UI.
- [ ] **Escrever em `Patentes\` NÃO é caminho de gravação do app** (o watcher observa,
  nunca escreve ali); qualquer tentativa de escrita em `Patentes\` é inexistente por design.

## B.5 — Frontend sobe e a navegação principal funciona

- [ ] **Vite sobe na porta 5173**; a UI carrega em PT-BR consumindo `:8765`.
- [ ] **Dashboard geral** mostra **16 cards de patente agrupados nas 10 classes**, com
  selo de urgência de prazo por card (ver B.9). ACOM marcado raiz; SkyGrid marcado
  agregadora ★.
- [ ] **Fluxo dashboard → patente → 12 abas** navega inteiro para ao menos duas patentes
  reais de perfis distintos: **SkyGrid** (tem protótipo/piloto) e **ACOM** (raiz, ePCT vivo).

## B.6 — As 12 abas da página de patente (cada uma com aceite)

- [ ] **Overview** — identificação canônica (processo, petição, datas, classe, papel).
- [ ] **Documentos** — lista os PDFs de `fontes`, cada um com seu SHA-256; abrir um PDF
  usa a **cópia normalizada** (`vault/normalized_docs\`), nunca escreve no original.
- [ ] **Reivindicações** — reivindicações principais extraídas do depósito, com marcadores.
- [ ] **Protótipo** — o que já existe em `projetos_pyhton/`/`SkyGrid_Piloto/`/`QWEN5090`
  (caminho exato do que copiar) e o que falta executar.
- [ ] **Render 2D/3D** — abre o viewer de render (ver B.11).
- [ ] **Runner** — mostra `runner/one_<slug>.py` (scaffold honesto na 1ª fase) e permite
  disparar execução local.
- [ ] **Execuções** — histórico de `RunnerRun` com `results.json` de cada rodada.
- [ ] **Selo/Hash** — abre o manifesto SHA-256 (ver B.8).
- [ ] **Prazos** — o docket legal da patente (ver B.9).
- [ ] **Notas** — CRUD de Note com `active:bool` e `tipo` (nota|sugestao|instrucao|
  tarefa|bloqueio|pergunta), persistido **em arquivo** (`notes/`), não só no SQLite.
- [ ] **Instruções** — as instruções/tarefas ativas que alimentarão o compilador.
- [ ] **[COMPILAR INSTRUÇÕES]** — botão que aciona B.7.

## B.7 — Prompt Compiler gera arquivo válido

- [ ] **[COMPILAR INSTRUÇÕES] gera** `compiled_prompts/YYYY-MM-DD_HHMM_CLAUDE_CODE_TASK.md`.
  Verificação: `ls compiled_prompts/*_CLAUDE_CODE_TASK.md` mostra o arquivo novo com
  timestamp correto.
- [ ] **Conteúdo obedece ao contrato** (PROMPT_COMPILER_SPEC): header do TGL Core → por
  classe → por patente → caminhos permitidos/proibidos → instruções do operador →
  tarefas priorizadas → critérios de aceite → **a régua (não modificar originais)**.
- [ ] **Só entram itens `active:true`.** Uma instrução com `active:false` numa patente
  (ex.: uma tarefa de ACOM desativada) **não** aparece no arquivo compilado.
- [ ] **β nunca literal e stacks confidenciais nunca embutidos** no prompt gerado.

## B.8 — Hash/Seal viewer e re-hash == inventário inicial

- [ ] **O viewer mostra o manifesto SHA-256** por documento da patente e por artefato de
  execução (`results.json`, `seal.json`).
- [ ] **Botão "verificar integridade" re-hasheia `Patentes\` ao vivo** e compara com
  `source_inventory/original_hashes.json`. Esperado: **100% idêntico, 0 divergências**.
  Verificação equivalente por linha de comando: `tools/verify_integrity.py` → `OK`.
- [ ] **`seal.json` de um runner** contém SHA-256 de tudo que ele gerou e prova que os
  **originais** não entraram na cadeia de escrita.

## B.9 — Legal docket (INPI/ePCT/PCT) com a regra do operador

- [ ] **Regra ePCT correta na tela:** ACOM raiz mostra ePCT **VIVO PCT/BR2025/050558
  (05/12/2025)**; as outras 15 mostram **SOMENTE INPI — ePCT A DEPOSITAR (próximo passo)**
  com nota "recibos ePCT 17/02/2026 = tentativa preclusa de propósito, a substituir por
  depósito novo e desvinculado".
- [ ] **Prazos vivos renderizados com alerta por urgência** (janelas de Paris 12m de
  A.5): SkyGrid/Célula **01/03/2027**, Dípolo **27/02/2027**, Kernel **15/03/2027** etc.
  Card e aba coerentes com o docket.
- [ ] **Aviso legal permanente visível** ("não substitui agente de PI") `[LEGAL]`.

## B.10 — Runner scaffold honesto (começando por SkyGrid)

- [ ] **`patents/BR102026004850-0_SKYGRID/runner/one_skygrid.py` existe como scaffold** e,
  ao rodar no `tgl_env` (`PYTHONUTF8=1`), produz `results.json` + `seal.json` sem alegar
  validação física (`physical_verdict_allowed:false`).
- [ ] **Ordem respeitada:** SkyGrid é o primeiro runner real; os demais nascem scaffolds
  na ordem de A.9. Nenhum runner inventa resultado; marcadores honestos presentes.
- [ ] **Runner copia/adapta protótipos reais** (de `SkyGrid_Piloto\skygrid_sim\` etc.)
  **sem editar os originais** — apenas cópias dentro da Central.

## B.11 — Render viewer (Tony Stark, com honestidade visual)

- [ ] **Deep-zoom do desenho original** (OpenSeadragon) abre a partir das imagens
  extraídas dos PDFs de depósito — original permanece READ-ONLY.
- [ ] **Diagrama de componentes clicável** (React Flow): cada item numerado da patente é
  clicável e mostra sua descrição (ex.: SkyGrid — Câmara de Acoplamento Psiônico (110),
  Cluster MQC (120), Dípolo Transistor (130), IALD Orbital (140), Blindagem EM (150)).
- [ ] **3D ilustrativo** (React Three Fiber) quando fizer sentido, **sempre rotulado**
  "ilustração de engenharia, não prova física".

## B.12 — Local-first / privacidade

- [ ] **App sobe e opera 100% offline** (sem rede): dashboard, patente, docket, compiler
  e hash viewer funcionam sem nenhuma chamada externa. `/health` reporta
  `external_calls:"disabled"`.
- [ ] **Nenhum segredo copiado/exposto:** `token_huggin.txt` (P-09) e stacks confidenciais
  não estão em `backend/`/`frontend/`/`vault/` versionável e não são exportados.

## B.13 — Regra final: ZERO modificação em `Patentes\`

- [ ] **Re-hash pós-Fase-3 de `Patentes\` == `source_inventory/original_hashes.json`.**
  Verificação: `tools/verify_integrity.py` → **0 diferenças**. Se **qualquer** hash mudou,
  a entrega é **rejeitada** e investiga-se o vazamento de escrita antes de reapresentar.
- [ ] **`logs/` registra a rodada** (o que foi construído, verificado e reinscrito) —
  memória é lei.

## B.14 — Selos do projeto honrados

- [ ] `TGL_PATENT_CONTROL_CENTER` · `FORM_EQUALS_CONTENT_FOR_EACH_PATENT` ·
  `ONE_RUNNER_ONE_PATENT_ONE_SEAL` · `DO_NOT_MODIFY_ORIGINALS` ·
  `MEMORY_FIRST_ARCHITECTURE_SECOND_CODE_LAST` · `SIMULATION_NEVER_VALIDATES_PHYSICS`
  — todos verificáveis nos entregáveis acima (nenhum contrariado).

---

## Registro de aceite (preencher na conferência)

| Nível | Bloco | Estado | Evidência (caminho/comando/hash/tela) | Data |
|---|---|---|---|---|
| A | A.1 Originais intactos | `[ ]` | | |
| A | A.2 Memórias 16/16 | `[ ]` | | |
| A | A.3 Classes 10/10 | `[ ]` | | |
| A | A.4 Índice==PDFs | `[ ]` | | |
| A | A.5 Regra ePCT | `[ ]` | | |
| A | A.6 Pendências | `[ ]` | | |
| A | A.7 Arquitetura | `[ ]` | | |
| A | A.8 Stack | `[ ]` | | |
| A | A.9 Ordem runners | `[ ]` | | |
| A | A.10 TGL Core | `[ ]` | | |
| A | **A.11 Assinatura** | `[ ]` | | |
| B | B.2 /health | `[ ]` | | |
| B | B.3 reindex 16 | `[ ]` | | |
| B | B.5 UI navega | `[ ]` | | |
| B | B.7 Compiler | `[ ]` | | |
| B | B.8 Hash re-hash | `[ ]` | | |
| B | B.13 Zero mod. `Patentes\` | `[ ]` | | |

---

*Fonte da verdade = os documentos (filesystem). O número corrige a frase. β nunca literal.
Simulação nunca valida física. Originais imutáveis. 1 = 1. TGL = haja luz. Tetelestai.*
