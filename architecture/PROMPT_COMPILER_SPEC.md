# PROMPT_COMPILER_SPEC.md — O Prompt Compiler da Central de Patentes TGL

**Central de Controle e Desenvolvimento de Patentes TGL · `C:\IALD\Central de Patentes`**
**Fase 2 — ARQUITETURA (especificação; NENHUM código de aplicação escrito).**
**Operador: Luiz Antonio Rotoli Miguel — IALD Ltda. (CNPJ 62.757.606/0001-23, Goiânia/GO).**
**Versão 1.0 — 09/07/2026. PT-BR na doc; inglês nos identificadores de código.**

> **Posição na cadeia do projeto.**
> `TGL Core → Classes → Patentes → Memória Técnica → Runner Único → Hash/Selo → Dashboard Visual → **Prompt Compiler (esta spec)**`.
> O Prompt Compiler é a **ponte manual** entre a Central e o Claude Code. Ele não
> executa nada nas patentes: ele **coleta** as notas/instruções vivas que o operador
> deixou pela UI, **agrupa e prioriza** por classe→patente, **prefixa** o header
> ontológico do TGL Core + a régua + os caminhos permitidos/proibidos, e **emite** um
> único arquivo `compiled_prompts/YYYY-MM-DD_HHMM_CLAUDE_CODE_TASK.md` que o operador
> **copia e cola** numa nova sessão do Claude Code. Fase 3 codifica a partir deste
> documento sem voltar a perguntar.

> **Documentos irmãos** (coerência obrigatória): `DATA_MODEL.md` (entidades canônicas),
> `LEGAL_DOCKET_SPEC.md` (prazos que alimentam a urgência), `WORKFLOW.md` (o loop),
> `UI_SPEC.md` (abas por patente, incluindo a aba **[COMPILAR INSTRUÇÕES]**).

---

## 0. Invariantes herdados (esta spec obedece a todos)

1. **Local-first, privado.** A compilação é 100% local; nenhuma API externa é chamada.
2. **FILESYSTEM É A FONTE DA VERDADE.** Cada nota/instrução é **um arquivo `.md` com
   YAML frontmatter** dentro de `patents/<ID>_<SLUG>/notes/`. Cada prompt compilado é
   **um arquivo `.md` + um sidecar `.manifest.json`** em `compiled_prompts/`. O SQLite
   (`backend/data/central.db`) é **índice/cache reconstruível** (`reindex`), nunca o
   dono do dado. Apagar o `.db` e reindexar reproduz o estado byte-a-byte a partir dos
   arquivos.
3. **A régua.** Originais em `Patentes\` READ-ONLY; nada é escrito fora de
   `C:\IALD\Central de Patentes`; o número corrige a frase; marcadores em tudo;
   **β nunca literal em código** (`ALPHA_FINE_CODATA_2018 * sqrt(e)` em runtime);
   simulação nunca valida física (`physical_verdict_allowed = false`); stacks
   confidenciais nunca exportados; aviso legal permanente no docket.
4. **Backend** FastAPI + SQLite + SQLModel/Pydantic, porta **8765**, uvicorn; indexação
   por Watchdog; motor de manifesto SHA-256. **Frontend** React+TS+Vite (5173).
5. **Escrita permitida** só em áreas da Central que a Central possui: `patents/<...>/notes/`,
   `compiled_prompts/`, `logs/`. As notas NÃO são "originais" — são dado editável da
   Central. Originais de depósito (`Patentes\`) permanecem intocados.

---

## 1. Modelo de dados das Notas/Instruções

### 1.1 A entidade canônica `Note` (= Note/Instruction do DATA_MODEL)

Uma única entidade cobre os seis tipos; o campo `tipo` discrimina a semântica e o
roteamento na compilação. É a materialização da entidade canônica
`Note/Instruction(active:bool, tipo: nota|sugestao|instrucao|tarefa|bloqueio|pergunta)`.

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `id` | string (ULID, 26 chars) | sim | Identidade global estável, ordenável no tempo. Nunca muda, nunca reusa. Ex.: `01J9Z6H8QK3M0F2T7B4RX9WYV1`. |
| `ref` | string | sim | Handle humano estável, atribuído na criação: `<SLUG>-<TIPO_ABBR>-<n>` (contador por patente por tipo). Ex.: `SKYGRID-INSTR-1`. Abreviações: `NOTA·SUG·INSTR·TAR·BLOQ·PERG`. |
| `patent_id` | string | sim | Nº de processo INPI da patente-alvo. Ex.: `BR102026004850-0`. Redundante com a pasta (o arquivo vive em `patents/<ID>_<SLUG>/notes/`), mantido para o índice. |
| `patent_slug` | string | sim | Ex.: `SKYGRID`. Derivável da pasta; persistido para robustez do índice. |
| `class_id` | string | sim | Ex.: `CLASS_06_ENERGIA`. Derivado da patente (fonte: `PATENT_MASTER_INDEX.yaml`); persistido para agrupar sem join. |
| `tipo` | enum | sim | `nota` \| `sugestao` \| `instrucao` \| `tarefa` \| `bloqueio` \| `pergunta`. Ver §1.2. |
| `title` | string (≤120) | sim | Título curto, imperativo para tarefa/instrução. |
| `body` | markdown | sim | Texto livre do operador (o conteúdo real da nota). |
| `active` | bool | sim | **A chave de seleção.** `true` = entra na PRÓXIMA compilação. Default `true` para tipos compiláveis; ver §1.3. |
| `status` | enum | sim | Ciclo de vida: `rascunho` \| `ativa` \| `compilada` \| `concluida` \| `arquivada` \| `descartada`. Ver §1.3. |
| `priority` | enum | sim | `P0` (crítica/bloqueante) \| `P1` (alta) \| `P2` (média, default) \| `P3` (baixa). |
| `author` | enum | sim | `operador` \| `claude_code` \| `sistema` \| `agente_pi`. Quem escreveu. |
| `created_at` | datetime ISO-8601 c/ tz | sim | Ex.: `2026-07-09T14:32:07-03:00`. |
| `updated_at` | datetime ISO-8601 c/ tz | sim | Toda mutação atualiza. |
| `compiled_at` | datetime \| null | não | Setado no 1º compile que a incluiu. |
| `completed_at` | datetime \| null | não | Setado quando o operador marca `concluida`. |
| `markers` | lista de string | não | Marcadores da régua aplicáveis: `[SIM]`,`[PILOTO]`,`[HARDWARE]`,`[LEGAL]`,`[OPEN]`,`[DATA]`,`[CONJ]`… Renderizados no prompt. |
| `acceptance_criteria` | lista de string | não | Critérios de aceite (para `tarefa`/`instrucao`). Cada item vira checkbox no prompt. |
| `blocks` | lista de `ref` | não | Só `bloqueio`: refs de notas que este bloqueio trava. Vazio = trava a patente inteira. |
| `blocked_by` | lista de `ref` | não | Derivado (índice): refs de bloqueios ativos que travam esta nota. |
| `answer` | markdown \| null | não | Só `pergunta`: resposta registrada depois (fecha a pergunta). |
| `related` | lista de string | não | Links: refs de outras notas, `patent_id` de outras patentes, ou IDs de `Pendencia` (ex.: `P-05`). |
| `compiled_in` | lista de string | não | Nomes dos arquivos `compiled_prompts/*.md` onde esta nota já apareceu (histórico append-only). |
| `estimate` | string \| null | não | Estimativa livre do operador (`~2h`, `1 sessão`). Opcional; informa ordenação secundária. |
| `tags` | lista de string | não | Rótulos livres (`runner`, `render-3d`, `docket`). |

> **Nota sobre `active` vs `status`.** `active` é o **gate booleano** de "entra na
> próxima compilação". `status` é o **estado do ciclo de vida**. São ortogonais mas
> acoplados por regras (§1.3): o compile lê `active`; a mutação pós-compile escreve
> `status`. Manter os dois evita ambiguidade e permite "reativar" (`compilada → ativa`)
> sem perder o histórico.

### 1.2 Os seis tipos — semântica e roteamento

Cada tipo é **compilável** (entra no prompt) ou não, e vai para uma **seção** própria
do bloco da patente. `bloqueio` e `pergunta` são compiláveis mas não são "tarefas".

| `tipo` | Compilável? | Seção no prompt | Semântica |
|---|---|---|---|
| `tarefa` | **sim** | **Tarefas priorizadas** | Trabalho acionável concreto. Carrega `acceptance_criteria`. É o núcleo do prompt. |
| `instrucao` | **sim** | **Instruções do operador** | Diretiva de como fazer / política para a próxima etapa. Precede as tarefas. |
| `sugestao` | **sim** | **Sugestões de melhoria** | Ideia de aprimoramento; não obriga; entra abaixo das tarefas. |
| `pergunta` | **sim** | **Perguntas ao Claude Code** | Dúvida que o operador quer que o Claude Code responda na sessão. Fecha via `answer`. |
| `bloqueio` | **sim** | **Bloqueios ativos** (banner ⛔ no topo do bloco da patente) | Impedimento. Ativo → **realça** e marca as tarefas dependentes como travadas. |
| `nota` | **opcional** | **Contexto** | Nota de contexto/livre. Só entra se `active=true` **e** `tags` contém `include_in_prompt`; caso contrário fica só na UI/memória. Evita poluir o prompt. |

### 1.3 Ciclo de vida (`status`) e sua relação com `active`

```
            (operador cria)
                  │
            ┌─────▼─────┐   marcar pronta          ┌──────────┐
            │ rascunho  ├─────────────────────────▶│  ativa   │  active=true
            │active=false│◀────────────────────────┤          │
            └───────────┘   voltar a rascunho      └────┬─────┘
                                                        │  COMPILAR INSTRUÇÕES
                                                        │  (nota incluída no prompt)
                                                   ┌────▼──────┐
                                    reativar       │ compilada │  active=false
                              ┌────────────────────┤(no prompt)│  compiled_at setado
                              │                     └────┬──────┘
                              │                          │ operador executou no Claude Code
                              │  (volta p/ ativa)        │ e validou o resultado
                              ▼                     ┌────▼──────┐
                        (active=true)               │ concluida │  active=false
                                                    └───────────┘  completed_at setado

  Terminais alternativos: `arquivada` (guardar sem agir) e `descartada` (abandonar).
  Ambos active=false. Nenhum status apaga o arquivo — histórico é append-only.
```

**Regras duras (invariantes de estado):**

- **R1 — Elegibilidade de compilação:** uma nota entra numa compilação **se e somente
  se** `active == true` **e** `status == "ativa"` **e** `tipo` é compilável (para `nota`,
  também exige a tag `include_in_prompt`).
- **R2 — Transição de compilação:** ao ser incluída num prompt, a nota passa
  `ativa → compilada`, `active → false`, `compiled_at := agora`, e o nome do arquivo é
  **anexado** a `compiled_in[]`. Isto evita recompilar a mesma instrução na próxima vez
  por engano.
- **R3 — Perguntas:** uma `pergunta` respondida (`answer != null`) passa a `concluida`
  automaticamente; sem resposta, segue `compilada` até o operador registrar a resposta.
- **R4 — Bloqueios:** um `bloqueio` NÃO muda para `compilada` ao aparecer no prompt —
  ele permanece **`ativa`/`active=true`** até o operador resolvê-lo (`concluida`),
  porque ele deve reaparecer em toda compilação enquanto o impedimento existir.
- **R5 — Reativação:** o operador pode `compilada → ativa` (reincluir na próxima). O
  histórico `compiled_in[]` é preservado.
- **R6 — Imutabilidade de `id`/`ref`:** nunca mudam. `patent_id`/`class_id` só mudam se
  a patente for reclassificada (evento raro, registrado em `PENDENCIAS.md`; ver P-04).

### 1.4 Prioridade e ordenação

Escala fixa: **P0 > P1 > P2 (default) > P3**. A ordenação combina prioridade da nota,
tipo, urgência de prazo legal do docket e tempo de criação (desempate estável):

```
chave_de_ordem(nota) = (
    ordem_classe(class_id),          # CLASS_01 … CLASS_10 (asc)
    -urgencia_docket(patent_id),     # patente com prazo mais próximo primeiro (§3.5)
    peso_prioridade(priority),       # P0=0, P1=1, P2=2, P3=3 (asc)
    peso_tipo(tipo),                 # bloqueio=0, instrucao=1, tarefa=2, pergunta=3, sugestao=4, nota=5
    created_at                       # mais antigo primeiro (estável)
)
```

- **Cross-patente:** o documento é agrupado por classe (asc), e dentro da classe as
  patentes vêm ordenadas pela urgência do docket (prazo mais próximo primeiro).
- **Intra-patente:** bloqueios no topo (banner), depois instruções, depois tarefas por
  prioridade, depois perguntas, sugestões, e contexto.

### 1.5 Armazenamento no filesystem (fonte da verdade)

Cada nota é **um arquivo** em `patents/<ID>_<SLUG>/notes/`:

- **Convenção de nome** (ordenável, sem `:` — compatível com Windows):
  `<YYYY-MM-DD>_<HHMM>_<tipo>_<id8>.md`, onde `<id8>` são os 8 últimos chars do ULID.
  Ex.: `2026-07-09_1432_instrucao_RX9WYV1.md`.
- **Formato:** YAML frontmatter (os campos estruturados) + corpo Markdown (`body`).
- O corpo Markdown **é** o `body`; os demais campos vivem no frontmatter. O
  `acceptance_criteria` pode ser espelhado no corpo como checklist para leitura humana,
  mas a **fonte estruturada é o frontmatter**.

**Exemplo de arquivo real** — `patents/BR102026004850-0_SKYGRID/notes/2026-07-09_1432_instrucao_RX9WYV1.md`:

```markdown
---
id: 01J9Z6H8QK3M0F2T7B4RX9WYV1
ref: SKYGRID-INSTR-1
patent_id: BR102026004850-0
patent_slug: SKYGRID
class_id: CLASS_06_ENERGIA
tipo: instrucao
title: "Criar o scaffold honesto de one_skygrid.py a partir do digital twin v3"
active: true
status: ativa
priority: P1
author: operador
created_at: 2026-07-09T14:32:07-03:00
updated_at: 2026-07-09T14:32:07-03:00
compiled_at: null
completed_at: null
markers: ["[SIM]", "[CONJ]", "[ENERGY]"]
acceptance_criteria:
  - "one_skygrid.py roda em tgl_env com PYTHONUTF8=1 sem erro"
  - "physical_verdict_allowed=false em toda saída (results.json, seal.json, painel)"
  - "beta emerge em runtime (ALPHA_FINE_CODATA_2018*sqrt(e)); auditoria anti-hardcode passa"
  - "veredito maximo herdado: MODEL_CLOSES / ENERGY_BALANCE_OK ([SIM] sob [CONJ])"
  - "duplo trilho (Trilha-Psi vs Trilha-E) com validacao cruzada; placebo (no sem beta) falha"
  - "gera results.json + seal.json com SHA-256 de codigo+manifesto+resultado"
  - "re-hash de Patentes\\ == original_hashes.json (nenhum original modificado)"
blocks: []
blocked_by: []
answer: null
related: ["CLASS_06_ENERGIA", "P-04"]
compiled_in: []
estimate: "1 sessão"
tags: ["runner", "scaffold", "duplo-trilho"]
---

Adaptar (COPIANDO, nunca editando) o digital twin v3 do SkyGrid_Piloto em
`Patentes\Skygrid\SkyGrid_Piloto\skygrid_sim\` para nascer o runner único
`patents/BR102026004850-0_SKYGRID/runner/one_skygrid.py` como **scaffold honesto**.

Herdar o teto do piloto v3 (`SKYGRID_V3_SELO.json`): veredito máximo
`MODEL_CLOSES / ENERGY_BALANCE_OK ([SIM] sob [CONJ])`, `physical_verdict_allowed=false`.
Nenhuma alegação de energia real — só a LÓGICA da rede planetária (144 Extratores-Ψ,
duplo trilho Ψ/E, calorimetria diferencial). Placebo obrigatório: nó sem β falha por
construção.
```

### 1.6 Índice SQLite (cache reconstruível)

O Watchdog observa `patents/**/notes/*.md` e mantém a tabela `note` (SQLModel). O
comando `reindex` limpa e reconstrói a tabela lendo todos os arquivos. **Nenhum campo
é canônico no DB** — o DB é derivado.

```sql
-- Tabela de ÍNDICE (backend/data/central.db). Reconstruível a partir dos .md.
CREATE TABLE note (
  id            TEXT PRIMARY KEY,          -- ULID
  ref           TEXT NOT NULL UNIQUE,
  patent_id     TEXT NOT NULL,
  patent_slug   TEXT NOT NULL,
  class_id      TEXT NOT NULL,
  tipo          TEXT NOT NULL,             -- nota|sugestao|instrucao|tarefa|bloqueio|pergunta
  title         TEXT NOT NULL,
  active        INTEGER NOT NULL,          -- 0/1
  status        TEXT NOT NULL,
  priority      TEXT NOT NULL,             -- P0..P3
  author        TEXT NOT NULL,
  created_at    TEXT NOT NULL,
  updated_at    TEXT NOT NULL,
  compiled_at   TEXT,
  completed_at  TEXT,
  markers_json  TEXT,                      -- JSON array
  criteria_json TEXT,                      -- JSON array
  blocks_json   TEXT,
  answer        TEXT,
  related_json  TEXT,
  compiled_in_json TEXT,
  file_path     TEXT NOT NULL,             -- caminho relativo do .md (a fonte)
  file_sha256   TEXT NOT NULL              -- hash do .md p/ detectar drift
);
CREATE INDEX ix_note_compile ON note(active, status, class_id, patent_id, priority);
```

`file_sha256` permite ao motor de manifesto detectar que um `.md` foi editado fora da
UI (por editor de texto): a UI mostra "índice desatualizado — reindexar".

---

## 2. Algoritmo de compilação

### 2.1 Entrada (escopo e opções)

A ação **[COMPILAR INSTRUÇÕES]** aciona `POST /compile` (§4) com:

```
CompileRequest {
  scope: {
    kind: "all" | "classes" | "patents" | "notes",
    ids?: string[]            # ids de classe, patent_id, ou ULIDs de nota
  },
  options: {
    dry_run: bool = false,        # true = preview, não muta nada, não grava arquivo
    include_types?: string[],     # default: todos os compiláveis
    min_priority?: "P0".."P3",    # default P3 (inclui tudo)
    include_context_notes: bool = false,  # tipo `nota` só entra se true
    title?: string,               # rótulo humano do prompt (senão auto)
    author: "operador"            # quem disparou
  }
}
```

### 2.2 Passos

```
1. SNAPSHOT     Ler o índice (ou o FS direto) e congelar o conjunto candidato.
2. FILTRAR      Aplicar R1 (elegibilidade) + escopo + include_types + min_priority.
                → conjunto S de notas elegíveis.
3. RESOLVER     Para cada nota, resolver bloqueios ativos que a travam (blocked_by),
                puxar identificação da patente (PATENT_MASTER_INDEX.yaml) e o prazo
                vivo do Legal Docket (docket.yaml) → urgencia_docket.
4. AGRUPAR      Particionar S por class_id → depois por patent_id.
5. ORDENAR      Ordenar classes (asc) e patentes por urgência; dentro da patente,
                ordenar por chave_de_ordem (§1.4).
6. MONTAR HEADER  Carregar o header condensado do TGL Core (memory/TGL_CORE_MEMORY.md,
                §2.5) + A RÉGUA global + caminhos globais.
7. CAMINHOS     Para cada patente, montar caminhos permitidos/proibidos (§2.6),
                estado do protótipo e fontes a copiar (do master index / memória).
8. RENDER       Emitir o Markdown pelo TEMPLATE (§3): header → por classe → por
                patente (bloqueios → instruções → tarefas+critérios → sugestões →
                perguntas → contexto) → fila global priorizada → régua/aviso/rodapé.
9. SELAR        Calcular SHA-256 do .md; montar o sidecar .manifest.json (lista de
                notas incluídas com hash de cada arquivo-fonte).
10. PERSISTIR   (se !dry_run) Gravar .md + .manifest.json em compiled_prompts/;
                aplicar R2/R3/R4 a cada nota incluída; anexar ao _index.yaml;
                logar em logs/compile.log. Watchdog reindexa.
11. RETORNAR    CompileResponse (§4) com caminho, filename, contagens, selo, incluídas.
```

### 2.3 Pseudocódigo (contrato, não implementação)

```python
def compile_prompt(req: CompileRequest) -> CompileResponse:
    S = [n for n in load_notes()               # do FS/índice
         if n.active and n.status == "ativa"
         and is_compilable(n, req.options.include_types, req.options.include_context_notes)
         and in_scope(n, req.scope)
         and prio_at_least(n.priority, req.options.min_priority)]

    if not S:
        return CompileResponse(status="empty", included=[], ...)   # nada a compilar

    docket = load_docket_urgency()             # de patents/<id>/docket.yaml (LEGAL_DOCKET_SPEC)
    for n in S:
        n.blocked_by = active_blockers_of(n, S) # bloqueios ativos que travam n

    groups = group_by(S, key=lambda n: (n.class_id, n.patent_id))
    ordered = sort_groups_and_notes(groups, docket)   # §1.4 / §3.5

    header = render_tgl_core_header() + render_regua() + render_global_paths()
    body   = render_classes_and_patents(ordered, docket, paths_resolver)
    footer = render_global_queue(ordered) + render_regua_footer() + render_legal_notice()
    md     = assemble(front_matter(req, S), header, body, footer)

    seal_sha = sha256(md)
    manifest = build_manifest(md, S, seal_sha, req)   # inclui hash de cada .md-fonte

    if req.options.dry_run:
        return CompileResponse(status="preview", markdown=md, manifest=manifest, ...)

    fname = next_filename(now())               # YYYY-MM-DD_HHMM_CLAUDE_CODE_TASK.md
    atomic_write(f"compiled_prompts/{fname}", md)
    atomic_write(f"compiled_prompts/{fname}.manifest.json", manifest)
    for n in S:
        apply_post_compile(n, fname)           # R2/R3/R4 (§5)
    append_index(fname, manifest)              # compiled_prompts/_index.yaml
    log_event("compile", fname, seal_sha, len(S))
    return CompileResponse(status="ok", path=..., filename=fname, seal_sha256=seal_sha,
                           included=[n.ref for n in S], manifest=manifest)
```

### 2.4 Regras de bloqueio

- Um `bloqueio` **ativo** cujo `blocks` está vazio trava a **patente inteira**: o bloco
  da patente ganha um banner ⛔ e **todas** as tarefas/instruções da patente são
  marcadas `⛔ BLOQUEADA` (o Claude Code é instruído a não executá-las até resolução).
- Um `bloqueio` com `blocks: [SKYGRID-TAR-1]` trava **apenas** aquelas refs; as demais
  tarefas seguem executáveis.
- Bloqueios seguem R4: **não** viram `compilada`; reaparecem em toda compilação até o
  operador marcá-los `concluida`.
- O documento sempre lista o bloqueio no topo do bloco da patente com o que ele trava.

### 2.5 Header condensado do TGL Core

O compilador **não copia** o `TGL_CORE_MEMORY.md` inteiro (grande). Ele emite um
**bloco condensado canônico** derivado das §1 (cadeia), §5 (calibração dos runners) e
"A régua" daquele arquivo, e **referencia** o arquivo completo por caminho + SHA-256.
O bloco condensado é fixo (versionado junto do backend) e contém: a cadeia canônica em
uma linha, a legenda de marcadores, e a régua de calibração dos runners
(`physical_verdict_allowed=false`, β em runtime, vocabulário de veredito restrito,
placebo/duplo trilho/quórum/selo). Ver o texto exato renderizado no §4 (exemplo real).

### 2.6 Montagem dos caminhos permitidos/proibidos por patente

Fonte: `PATENT_MASTER_INDEX.yaml` (pasta original, classe) + memória da patente
(`memory/patents/<ID>_<SLUG>.md`, seção "O que já existe em protótipos") + a régua.
Regra de montagem:

- **Permitido escrever (só dentro da Central):**
  `patents/<ID>_<SLUG>/` (`runner/`, `renders/`, `results/`, `seals/`, `notes/`),
  `compiled_prompts/`, `logs/`, e `vault/originals_copy|normalized_docs|tgl_verification/`.
- **Ler + COPIAR (nunca editar):** a pasta original da patente em `Patentes\...` (READ-ONLY),
  os protótipos algorítmicos citados na memória (ex.: `projetos_pyhton\acom\`,
  `SkyGrid_Piloto\skygrid_sim\`), e `memory/`.
- **PROIBIDO (nunca tocar/rodar/exportar):** qualquer caminho fora de
  `C:\IALD\Central de Patentes\` (para escrita); os originais de depósito; os segredos
  (`token_huggin.txt`, `iald_stack_v7.py`/`iald_psion_state.json` — uso local sim,
  export jamais); o webserver de produção `iald_web_server.py` (não rodar).

### 2.7 Integração com o Legal Docket (urgência)

`urgencia_docket(patent_id)` lê o prazo vivo do docket da patente
(`LEGAL_DOCKET_SPEC.md`): para as 15 patentes só-INPI, a `janela_paris_12m`; para o
ACOM raiz, a `fase_nacional_30m`. Converte em `dias_restantes` e mapeia para nível de
alerta (🔴 ≤90d · 🟠 ≤180d · 🟡 ≤365d · 🟢 >365d). Esse nível: (a) ordena patentes
dentro da classe (mais urgente primeiro) e (b) é **impresso** ao lado da patente no
prompt, para o Claude Code priorizar. **Aviso permanente:** controle interno não
substitui agente de PI.

---

## 3. Template completo do arquivo compilado (esqueleto anotado)

`compiled_prompts/YYYY-MM-DD_HHMM_CLAUDE_CODE_TASK.md`. Placeholders em `{{ }}`;
comentários `<!-- -->` não são renderizados no arquivo final.

```markdown
---
# FRONTMATTER DO PROMPT COMPILADO (metadados do índice)
compiled_at: {{iso8601}}
compiler_version: {{semver}}
scope_kind: {{all|classes|patents|notes}}
scope_ids: [{{...}}]
options: { include_types: [...], min_priority: {{P?}}, include_context_notes: {{bool}} }
counts: { classes: {{n}}, patents: {{n}}, instrucoes: {{n}}, tarefas: {{n}},
          perguntas: {{n}}, sugestoes: {{n}}, bloqueios_ativos: {{n}} }
included_refs: [{{SLUG-TIPO-n, ...}}]
seal_sha256: {{hash do próprio .md, preenchido pós-render}}
manifest: {{filename}}.manifest.json
tgl_core_ref: { file: "memory/TGL_CORE_MEMORY.md", sha256: {{hash}} }
---

# PROMPT PARA O CLAUDE CODE — CENTRAL DE PATENTES TGL
**Gerado:** {{data extensa}} · **Escopo:** {{descrição}} · **Selo:** `{{seal_sha256[:16]}}…`
**Como usar:** cole ESTE arquivo inteiro numa nova sessão do Claude Code aberta em
`C:\IALD\Central de Patentes`. Execute apenas o que está aqui. Ao terminar, inscreva o
progresso e devolva os selos.

## 0. HEADER ONTOLÓGICO — TGL CORE (condensado)
<!-- bloco fixo do §2.5: cadeia canônica + legenda + calibração dos runners -->

## 1. A RÉGUA (inviolável nesta e em toda sessão)
<!-- não modificar originais; número corrige a frase; β em runtime; physical_verdict=false;
     marcadores; segredos nunca exportados; fonte da verdade = documentos -->

## 2. CAMINHOS GLOBAIS
<!-- permitido escrever / ler+copiar / PROIBIDO (§2.6) -->

## 3. TRABALHO POR CLASSE
### CLASSE {{class_id}} — {{nome}}  {{travas da classe, ex.: [ENERGY]}}
<!-- definição curta + travas -->

> [nota operacional do operador — omitida no retrato público]

- **⛔ BLOQUEIOS ATIVOS:** {{cada bloqueio + o que trava}}   <!-- só se houver -->
- **Instruções do operador:** {{cada instrucao + markers + critérios}}
- **Tarefas priorizadas:**
  - `[P?]` {{ref}} — {{title}}  {{⛔ se bloqueada}}
    - Critérios de aceite: {{checkboxes}}
- **Sugestões de melhoria:** {{...}}
- **Perguntas ao Claude Code:** {{...}}
- **Contexto:** {{notas com include_in_prompt}}

## 4. FILA GLOBAL PRIORIZADA (ordem recomendada de execução)
<!-- lista achatada de todas as tarefas na ordem de §1.4, com bloqueadas no fim -->

## 5. CRITÉRIOS DE ACEITE GLOBAIS
<!-- re-hash dos originais intactos; selos gerados; nada fora da Central escrito -->

## 6. A RÉGUA (repetição de fecho) + AVISO LEGAL PERMANENTE
<!-- controle interno não substitui agente de PI -->

---
**Selo:** `{{seal_sha256}}` · **Manifesto:** `{{manifest}}` · TGL = haja luz. 1 = 1.
```

---

## 4. EXEMPLO REAL PREENCHIDO (instrução fictícia na patente SkyGrid)

Cenário: o operador, na aba **[COMPILAR INSTRUÇÕES]** da patente **SkyGrid**, deixou
quatro notas vivas e clicou COMPILAR com escopo = `CLASS_06_ENERGIA` (Fusão a Frio e
Célula de Reversão não têm nenhuma nota ativa, então só o SkyGrid aparece). Notas:

- `SKYGRID-BLOQ-1` (bloqueio, P0, ativo) — trava `SKYGRID-TAR-1`.
- `SKYGRID-INSTR-1` (instrução, P1) — o scaffold do runner (arquivo do §1.5).
- `SKYGRID-TAR-1` (tarefa, P2) — plotar a constelação de 144 Extratores-Ψ.
- `SKYGRID-PERG-1` (pergunta, P2) — qual versão do módulo copiar.

Arquivo emitido — **`compiled_prompts/2026-07-09_1432_CLAUDE_CODE_TASK.md`**:

```markdown
---
compiled_at: 2026-07-09T14:32:41-03:00
compiler_version: 1.0.0
scope_kind: classes
scope_ids: [CLASS_06_ENERGIA]
options: { include_types: [instrucao, tarefa, pergunta, bloqueio, sugestao],
           min_priority: P3, include_context_notes: false }
counts: { classes: 1, patents: 1, instrucoes: 1, tarefas: 1, perguntas: 1,
          sugestoes: 0, bloqueios_ativos: 1 }
included_refs: [SKYGRID-BLOQ-1, SKYGRID-INSTR-1, SKYGRID-TAR-1, SKYGRID-PERG-1]
seal_sha256: 9f4c1e77a0b3d2568c1af09e4477b6d2e5a1c8830b6f4419aa27de0c135b7e2a
manifest: 2026-07-09_1432_CLAUDE_CODE_TASK.md.manifest.json
tgl_core_ref:
  file: memory/TGL_CORE_MEMORY.md
  sha256: 3ac9…(hash da memória-núcleo no momento da compilação)
---

# PROMPT PARA O CLAUDE CODE — CENTRAL DE PATENTES TGL
**Gerado:** 09 de julho de 2026, 14:32 (−03:00) · **Escopo:** classe CLASS_06_ENERGIA
(1 patente: SkyGrid) · **Selo:** `9f4c1e77a0b3d256…`
**Como usar:** cole ESTE arquivo inteiro numa nova sessão do Claude Code aberta em
`C:\IALD\Central de Patentes`. Execute SOMENTE o que está aqui. Ao terminar, inscreva o
progresso na plataforma e devolva os selos SHA-256 gerados.

## 0. HEADER ONTOLÓGICO — TGL CORE (condensado)

Você herda a memória-núcleo `memory/TGL_CORE_MEMORY.md` (íntegra é a fonte; aqui vai o
condensado canônico). **Cadeia madura (uma linha):**
`ω(I)=1 → 𝒞²=1 → x=1−x⟹x=½ → S_∂=½ nat → Vol_∂^min=√e → β_TGL=α√e →
θ_M=arcsin√β≈6,30° → 𝒮_∂:|𝓡|²=β,|𝓣|²=1−β → P_ℱ=s(ker H_3L) → canto II₁ →
ergodicidade dissipativa → traço no centralizador → 1=1`.

**Marcadores (use em toda afirmação):** [POSTULATE]·[REAL]·[DER]·[DATA]·[INPUT]·[CONJ]·
[SIM]·[PILOTO]·[HARDWARE]·[LEGAL]·[OPEN]. **Veredito da física TGL hoje:** NÃO
FALSIFICADA, NÃO CONFIRMADA (evidência = convergência de β; BBN 0,0σ; CMB ~2,2σ exposto).

**Calibração dos runners (inviolável):** cada `one_<slug>.py` demonstra a LÓGICA da
invenção com números REAIS de execução rotulados [SIM]/[PILOTO], e **nunca alega
validação física**. `physical_verdict_allowed = false` em toda saída. `β` sempre
emergente em runtime: `beta = ALPHA_FINE_CODATA_2018 * sqrt(e)`
(# ≈ 0,012031300400803142 — cheque comentado, JAMAIS literal em código). Vocabulário de
veredito PROIBIDO nos harnesses: PROVED/CONFIRMED/TGL_TRUE/REFUTED; máximo permitido:
`SUPPORTED_NOT_CONFIRMED`; `INCONCLUSIVE` é resultado válido. Obrigatórios: placebo (nó
sem β falha por construção), duplo trilho, quórum em rede, selos SHA-256 de
código+manifesto+resultado, hash antes de comparação externa.

## 1. A RÉGUA (inviolável)

1. **NÃO MODIFICAR NENHUM ARQUIVO ORIGINAL.** Nada fora de
   `C:\IALD\Central de Patentes` é escrito/movido/renomeado/apagado. `Patentes\` é
   READ-ONLY (ler, hashear, COPIAR para `vault/originals_copy/` com SHA-256).
2. **O número corrige a frase.** Nunca fabricar prova. Runners nascem scaffolds honestos.
3. **Simulação NUNCA valida física** (`physical_verdict_allowed=False`).
4. **β nunca literal** em código de cálculo (runtime + auditoria anti-hardcode).
5. **Segredos nunca exportados** (`token_huggin.txt`, `iald_stack_v7.py`, `iald_psion_state.json`).
6. **Fonte da verdade = os DOCUMENTOS** dos depósitos; divergência → `PENDENCIAS.md`.

## 2. CAMINHOS GLOBAIS

- **Permitido ESCREVER (só dentro da Central):** `patents/<ID>_<SLUG>/{runner,renders,
  results,seals,notes}/`, `compiled_prompts/`, `logs/`, `vault/{originals_copy,
  normalized_docs,tgl_verification}/`.
- **Ler + COPIAR (nunca editar):** `Patentes\` (originais), protótipos em
  `C:\IALD\projetos_pyhton\`, `C:\IALD\TGL_IALD_NATIVE_QWEN5090\`, `memory/`.
- **PROIBIDO:** escrever fora da Central; editar originais; exportar segredos; RODAR
  `iald_web_server.py` (produção com usuários reais).

## 3. TRABALHO POR CLASSE

### CLASSE CLASS_06_ENERGIA — Energia / infraestrutura / materiais  [ENERGY]
**TRAVA:** só simulação e revisão técnica; NENHUMA instrução operacional perigosa.
Nenhuma alegação de energia física real — só a lógica computacional da invenção.

#### PATENTE SKYGRID — Rede Planetária de Energia por Acoplamento ao Campo Psiônico  (BR102026004850-0)  🟠 prazo 180d
- **Identificação:** classe CLASS_06_ENERGIA · papel **agregadora** · natureza PI (INPI).
  **Somente registro INPI hoje** (ePCT AINDA NÃO depositado — é o PRÓXIMO PASSO planejado
  pelo operador: novo processo originário, SEM vínculo; status A_DEPOSITAR/PENDENTE, não
  "perdido". Os recibos ePCT de 17/02/2026 = tentativa de protocolo abandonada de propósito,
  rascunho preclusso a SUBSTITUIR — palavra do operador). [OPEN]
  Prioridade 01/03/2026 → **janela Paris 12m = 01/03/2027** (🟠 ~180 dias). [LEGAL]
- **Caminhos desta patente:**
  - Escrever: `patents/BR102026004850-0_SKYGRID/{runner,renders,results,seals}/`.
  - Copiar (nunca editar): `Patentes\Skygrid\SkyGrid_Piloto\` — digital twin v3 COMPLETO,
    `skygrid_sim\` (18 módulos: tgl_core, acom, …, mqc, dipolo, celula_reversao),
    `skygrid_physics\`, selos (`SKYGRID_V3_SELO.json`).
  - Proibido: editar qualquer arquivo dentro de `Patentes\Skygrid\`.
- **Estado do protótipo:** digital twin v3 **JÁ FUNCIONAL**. Último run 03/07/2026:
  `MODEL_CLOSES / ENERGY_BALANCE_OK ([SIM] sob [CONJ])`, `physical_verdict_allowed:false`.
  **É o gabarito vivo de runner forma=conteúdo.**

- **⛔ BLOQUEIOS ATIVOS:**
  - `SKYGRID-BLOQ-1` [P0] — **As 144 posições orbitais MEO exatas ainda não foram
    confirmadas no relatório descritivo** (extração pendente do PDF de depósito).
    **Trava:** `SKYGRID-TAR-1`. Resolver antes de plotar a constelação. (rel.: P-04)

- **Instruções do operador:**
  - `SKYGRID-INSTR-1` [P1] [SIM][CONJ][ENERGY] — **Criar o scaffold honesto de
    `one_skygrid.py` a partir do digital twin v3.**
    Adaptar (COPIANDO, nunca editando) `SkyGrid_Piloto\skygrid_sim\` para nascer
    `patents/BR102026004850-0_SKYGRID/runner/one_skygrid.py` como scaffold honesto.
    Herdar o teto do piloto v3: veredito máximo `MODEL_CLOSES / ENERGY_BALANCE_OK
    ([SIM] sob [CONJ])`, `physical_verdict_allowed=false`. Placebo: nó sem β falha.
    - Critérios de aceite:
      - [ ] `one_skygrid.py` roda em `tgl_env` com `PYTHONUTF8=1` sem erro.
      - [ ] `physical_verdict_allowed=false` em results.json, seal.json e painel.
      - [ ] `beta = ALPHA_FINE_CODATA_2018*sqrt(e)` em runtime; auditoria anti-hardcode passa.
      - [ ] Duplo trilho (Trilha-Ψ vs Trilha-E) com validação cruzada; placebo reprova.
      - [ ] Gera `results.json` + `seal.json` com SHA-256 de código+manifesto+resultado.
      - [ ] Re-hash de `Patentes\` == `original_hashes.json` (nenhum original modificado).

- **Tarefas priorizadas:**
  - `[P2]` **SKYGRID-TAR-1** — Plotar a constelação de 144 Extratores-Ψ (MEO) com Plotly.
    **⛔ BLOQUEADA por `SKYGRID-BLOQ-1`** — NÃO executar até as posições serem confirmadas.
    - Critérios de aceite (para quando desbloquear):
      - [ ] Gráfico 3D em `renders/` rotulado "ilustração de engenharia, não prova física".
      - [ ] Fonte das posições citada (PDF de depósito), com marcador [DATA].

- **Perguntas ao Claude Code:**
  - `SKYGRID-PERG-1` [P2] — Qual módulo do `skygrid_sim\` é o ponto de entrada mais fiel
    ao balanço energético do v3 para o `one_skygrid.py` copiar: o agregador de topo ou o
    `tgl_core`? Justifique pela leitura do `SKYGRID_V3_SELO.json`.

## 4. FILA GLOBAL PRIORIZADA (ordem recomendada)

1. **SKYGRID-BLOQ-1** [P0] — resolver o bloqueio (extrair posições MEO do PDF). ⛔
2. **SKYGRID-INSTR-1** [P1] — scaffold honesto de `one_skygrid.py` (não depende do bloqueio).
3. **SKYGRID-PERG-1** [P2] — responder qual módulo copiar.
4. **SKYGRID-TAR-1** [P2] — constelação (só após BLOQ-1). ⛔ bloqueada.

## 5. CRITÉRIOS DE ACEITE GLOBAIS

- [ ] Re-hash de `Patentes\` idêntico a `source_inventory/original_hashes.json`.
- [ ] Todo artefato novo selado com SHA-256 (`seals/`).
- [ ] Nenhum arquivo escrito fora de `C:\IALD\Central de Patentes`.
- [ ] Nenhum segredo copiado/exportado. Nenhuma alegação de validação física.
- [ ] Progresso inscrito na plataforma + `logs/`.

## 6. A RÉGUA (fecho) + AVISO LEGAL PERMANENTE

Originais imutáveis · número corrige a frase · β em runtime · simulação não valida
física · marcadores em tudo · segredos nunca exportados.
**AVISO [LEGAL]:** este controle interno NÃO substitui agente de propriedade industrial;
prazos oficiais conferidos junto a INPI/WIPO.

---
**Selo:** `9f4c1e77a0b3d2568c1af09e4477b6d2e5a1c8830b6f4419aa27de0c135b7e2a`
**Manifesto:** `2026-07-09_1432_CLAUDE_CODE_TASK.md.manifest.json`
Quem não carrega o Um não cataloga suas sombras de engenharia. **TGL = haja luz. Tetelestai. 1 = 1.**
```

---

## 5. Pós-compilação

### 5.1 Mutação de estado das notas incluídas

Aplicada só quando `dry_run=false`, atomicamente por nota (reescreve o frontmatter do
`.md`; o corpo é preservado byte-a-byte):

- `instrucao`, `tarefa`, `sugestao`: `status ativa → compilada`, `active → false`,
  `compiled_at := now`, `updated_at := now`, `compiled_in += [filename]`. (R2)
- `pergunta`: idem, mas fica `compilada` até `answer` ser registrado → então `concluida`. (R3)
- `bloqueio`: **não muta** para `compilada`; permanece `ativa/active=true`, só
  `compiled_in += [filename]` e `updated_at := now`. Reaparece até `concluida`. (R4)

A UI da patente reflete: instruções compiladas saem da lista "ativas" e entram em
"Compiladas / histórico", com link para o arquivo que as consumiu.

### 5.2 O sidecar de manifesto (motor SHA-256)

Cada prompt gera `compiled_prompts/<filename>.manifest.json`. Ele prova quais notas e
qual header alimentaram o prompt, e sela tudo:

```json
{
  "compiled_prompt": "2026-07-09_1432_CLAUDE_CODE_TASK.md",
  "compiled_at": "2026-07-09T14:32:41-03:00",
  "compiler_version": "1.0.0",
  "seal_sha256": "9f4c1e77a0b3d2568c1af09e4477b6d2e5a1c8830b6f4419aa27de0c135b7e2a",
  "scope": { "kind": "classes", "ids": ["CLASS_06_ENERGIA"] },
  "tgl_core": { "file": "memory/TGL_CORE_MEMORY.md", "sha256": "3ac9…" },
  "included_notes": [
    { "ref": "SKYGRID-BLOQ-1", "id": "01J9…", "tipo": "bloqueio", "status_after": "ativa",
      "file": "patents/BR102026004850-0_SKYGRID/notes/2026-07-09_1420_bloqueio_….md",
      "file_sha256": "a1b2…" },
    { "ref": "SKYGRID-INSTR-1", "id": "01J9Z6H8QK3M0F2T7B4RX9WYV1", "tipo": "instrucao",
      "status_after": "compilada",
      "file": "patents/BR102026004850-0_SKYGRID/notes/2026-07-09_1432_instrucao_RX9WYV1.md",
      "file_sha256": "c3d4…" }
  ],
  "counts": { "classes": 1, "patents": 1, "instrucoes": 1, "tarefas": 1,
              "perguntas": 1, "bloqueios_ativos": 1 }
}
```

`reindex` reconstrói o índice `compiled_prompt` a partir do `.md` + `.manifest.json`;
re-hash do `.md` deve bater com `seal_sha256` (prova de integridade). Se `file_sha256`
de uma nota-fonte divergir do `.md` atual, a UI sinaliza "nota editada após a
compilação".

### 5.3 Índice e histórico

- `compiled_prompts/_index.yaml`: lista append-only (filename, data, escopo, contagens,
  seal). Reconstruível a partir dos manifests. Alimenta `GET /compiled`.
- Evento logado em `logs/compile.log` (timestamp, escopo, filename, seal, nº incluídas).
- **Nada é sobrescrito:** cada compile é um arquivo novo. Recompilar as MESMAS notas (se
  reativadas) gera um novo arquivo com novo timestamp; o `compiled_in[]` da nota vira
  lista com os dois nomes — o histórico completo fica no arquivo.

### 5.4 Nome do arquivo, idempotência e concorrência

- Nome: `YYYY-MM-DD_HHMM_CLAUDE_CODE_TASK.md`. Colisão no mesmo minuto → sufixo `-2`,
  `-3`… (`2026-07-09_1432_CLAUDE_CODE_TASK-2.md`).
- **Snapshot congelado (§2.2 passo 1):** a lista de notas é fixada no início; edições
  concorrentes na UI não entram no meio da compilação.
- **Escrita atômica:** `.md` e `.manifest.json` gravados em `.tmp` + `os.replace`.
- **Dry-run** (`dry_run=true`): renderiza e devolve o Markdown para preview na UI, **sem**
  gravar arquivo e **sem** mutar `status`/`active`. É o "Pré-visualizar" da aba.

---

## 6. Contratos de API

Backend FastAPI, base `http://127.0.0.1:8765`. Todas as respostas JSON; erros no formato
`{ "error": { "code": ..., "message": ..., "details": ... } }`.

### 6.1 `POST /compile` — compilar (ou pré-visualizar)

Request body = `CompileRequest` (§2.1). Exemplos de `scope`: `{"kind":"all"}`,
`{"kind":"classes","ids":["CLASS_06_ENERGIA"]}`, `{"kind":"patents","ids":["BR102026004850-0"]}`,
`{"kind":"notes","ids":["01J9Z6H8QK3M0F2T7B4RX9WYV1"]}`.

**Response 200 (`dry_run=false`):**
```json
{
  "status": "ok",
  "filename": "2026-07-09_1432_CLAUDE_CODE_TASK.md",
  "path": "compiled_prompts/2026-07-09_1432_CLAUDE_CODE_TASK.md",
  "seal_sha256": "9f4c1e77a0b3d256…",
  "manifest": "2026-07-09_1432_CLAUDE_CODE_TASK.md.manifest.json",
  "counts": { "classes":1, "patents":1, "instrucoes":1, "tarefas":1,
              "perguntas":1, "bloqueios_ativos":1 },
  "included": ["SKYGRID-BLOQ-1","SKYGRID-INSTR-1","SKYGRID-TAR-1","SKYGRID-PERG-1"],
  "mutated": [
    {"ref":"SKYGRID-INSTR-1","status_after":"compilada"},
    {"ref":"SKYGRID-TAR-1","status_after":"compilada"},
    {"ref":"SKYGRID-PERG-1","status_after":"compilada"},
    {"ref":"SKYGRID-BLOQ-1","status_after":"ativa"}
  ]
}
```

**Response 200 (`dry_run=true`):** mesmo shape, `status:"preview"`, **sem** `filename`/
`path`/`mutated`, **com** `"markdown": "<conteúdo completo do prompt>"` para render na UI.

**Response 200 (nada elegível):** `{ "status": "empty", "included": [], "message":
"Nenhuma nota ativa no escopo." }`.

**Erros:** `400` escopo inválido / ids inexistentes; `409` compilação concorrente em
andamento (lock); `422` validação Pydantic; `500` falha de escrita/hash (rollback: se o
`.md` não selou, nenhuma nota é mutada).

### 6.2 `GET /compiled` — listar prompts compilados

Query: `?limit=50&offset=0&scope_kind=&class_id=&since=`. Lê `_index.yaml` (ou os
manifests). **Response 200:**
```json
{
  "items": [
    { "filename": "2026-07-09_1432_CLAUDE_CODE_TASK.md",
      "compiled_at": "2026-07-09T14:32:41-03:00",
      "scope": {"kind":"classes","ids":["CLASS_06_ENERGIA"]},
      "counts": {"patents":1,"tarefas":1,"instrucoes":1,"perguntas":1,"bloqueios_ativos":1},
      "seal_sha256": "9f4c1e77a0b3d256…",
      "included": ["SKYGRID-BLOQ-1","SKYGRID-INSTR-1","SKYGRID-TAR-1","SKYGRID-PERG-1"] }
  ],
  "total": 1
}
```

### 6.3 `GET /compiled/{filename}` — obter um prompt

Retorna o conteúdo `.md` + o manifesto + verificação de selo. **Response 200:**
```json
{
  "filename": "2026-07-09_1432_CLAUDE_CODE_TASK.md",
  "markdown": "<conteúdo integral do .md>",
  "manifest": { ... },
  "seal_ok": true,
  "seal_recomputed_sha256": "9f4c1e77a0b3d256…"
}
```
`seal_ok=false` se o re-hash do `.md` divergir do `seal_sha256` do manifesto (arquivo
alterado à mão). `404` se o arquivo não existir.

### 6.4 Endpoints de apoio (contrato mínimo; CRUD completo em DATA_MODEL/WORKFLOW)

- `GET /patents/{patent_id}/notes?active=true&status=ativa` — notas de uma patente
  (alimenta a aba **Instruções/Notas** e o preview do que entraria no compile).
- `POST /notes` / `PATCH /notes/{id}` / `DELETE /notes/{id}` — CRUD das notas (grava o
  `.md` fonte; o Watchdog reindexa). `PATCH` cobre `answer` (fecha `pergunta`),
  `active`, `status`, `priority`, `acceptance_criteria`.
- `POST /reindex` — reconstrói o índice SQLite a partir do filesystem (notas +
  compiled_prompts), provando que o DB é cache.

---

## 7. Selos e checklist de conformidade

**Selos aplicáveis:** `TGL_PATENT_CONTROL_CENTER` · `MEMORY_FIRST_ARCHITECTURE_SECOND_CODE_LAST`
· `DO_NOT_MODIFY_ORIGINALS` · `SIMULATION_NEVER_VALIDATES_PHYSICS`.

**Checklist (VALIDATION_CHECKLIST.md deve verificar):**

- [ ] Toda nota é um `.md` com frontmatter; o SQLite é reconstruível por `reindex`.
- [ ] `active` é o gate de compilação; `status` é o ciclo de vida; R1–R6 respeitadas.
- [ ] Compile agrupa class→patente, prioriza por §1.4, integra urgência do docket.
- [ ] O prompt sempre traz: header TGL Core + régua + caminhos + instruções + tarefas
      priorizadas + critérios de aceite + régua de fecho + aviso legal.
- [ ] β aparece como `ALPHA_FINE_CODATA_2018*sqrt(e)` (valor só como cheque comentado);
      `physical_verdict_allowed=false` reafirmado no prompt.
- [ ] Pós-compile: instruções/tarefas/sugestões/perguntas → `compilada`; bloqueios
      permanecem `ativa` (R4); histórico em `compiled_in[]` + `_index.yaml`.
- [ ] `dry_run` não grava nada nem muta status. Escrita atômica. Selo SHA-256 verificável.
- [ ] Nenhum caminho fora da Central é escrito; segredos nunca entram no prompt.

**AVISO [LEGAL] permanente:** controle interno não substitui agente de propriedade
industrial; prazos oficiais conferidos com INPI/WIPO.

---

*Fase 2 — nenhuma linha de código de aplicação foi escrita. Esta é a especificação a
partir da qual a Fase 3 codifica o Prompt Compiler sem voltar a perguntar. 1 = 1.*
