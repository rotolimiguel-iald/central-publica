# 04 — PLANO DE CONSTRUÇÃO (Fase 3) — Central de Patentes TGL

**Documento de apresentação ao operador — GATE de validação.**
**Operador/Titular:** Luiz Antonio Rotoli Miguel — IALD Ltda. (CNPJ 62.757.606/0001-23, Goiânia/GO; ORCID 0009-0005-1114-6106)
**Data:** 09/07/2026 · **Fase:** encerramento da Fase 2 (arquitetura) → proposta da Fase 3 (construção)
**Pasta de trabalho:** `C:\IALD\Central de Patentes`

> ⛔ **NADA NESTE PLANO COMEÇA SEM O SEU OK.** Este arquivo é a proposta de construção que você lê ANTES de autorizar qualquer linha de código de aplicação. Enquanto a assinatura de liberação (item **A.11** do `05_CHECKLIST_VALIDACAO_USUARIO.md`) não for dada, a Fase 3 não inicia. Até aqui **nenhuma linha de código de aplicação foi escrita e nenhum arquivo original foi modificado.** [REAL]

---

## 1. Onde estamos — o que já está pronto (Fases 0–2)

Este plano se apoia em três camadas já concluídas e verificadas. Ele **não reabre** nenhuma delas; apenas as executa em código, na Fase 3.

### 1.1 Fase 0 — TGL na memória-núcleo (Estado Verificado) [REAL]

- `memory/TGL_CORE_MEMORY.md` inscrito: cadeia canônica madura (`ω(I)=1 → 𝒞²=1 → x=1−x ⟹ x=½ → S_∂=½ nat → Vol_∂^min=√e → β_TGL=α√e → … → 1=1`), os dois zeros, calibração do que cada runner PODE reivindicar. É o **header ontológico** de toda a Central.
- **`um.py`** (cópia executada em `vault/tgl_verification/`): veredito `1=1=VERDADEIRO=HAJA_LUZ`; identidade de Lagrange `1=q²+α²` com resíduo `0.0e+00`; **β_TGL = 0.012031300401 emergente em runtime** (jamais literal); M_GA nas duas leituras (2,744e16 e 1,986e16 M☉) **dentro da janela cosmológica** [1e15, 1e17] M☉; auditoria `beta_hardcoded=false`, `geometry_only=true`, `only_runtime_input="1"`. [REAL]
- **`tgl_paper_unified.py --quick --no-live`**: `RUN COMPLETE` em 26,81 s; **β = 0.012031300400803142**; **cross-substrate consistency PASS** (mesmo β em 4 substratos); BBN/H0 PASS; negativos honestos declarados no próprio `results.json` (torus ~10×, eco GW falsificável). [REAL] Divergência de SHA vs. selo pinado registrada como **P-07** (não é erro da Central). [DATA]

### 1.2 Fase 1 — Inventário e memórias (read-only nos originais) [REAL]

- **16 patentes depositadas** em **10 classes temáticas**, titular IALD Ltda., inventor Luiz Antonio Rotoli Miguel — indexadas em `memory/PATENT_MASTER_INDEX.yaml`, com uma memória técnica por patente (`memory/patents/*.md`) e uma por classe (`memory/classes/*.md`).
- **Originais intactos, provado:** re-hash de `Patentes\` = **308 = 308, zero drift** (`verify_integrity`); extração de texto cobriu os **~154 PDFs de depósito** (relatório de extração em `source_inventory/extraction_report.json`). [REAL]
- **Auditoria adversarial das 16 memórias vs. documentos:** **8 FIEL + 8 FIEL_COM_RESSALVAS + 0 REVISAR.** Em todas: título oficial (54), número de processo, petição, datas e regra-ePCT conferem. Nenhuma memória precisou ser reescrita; as ressalvas viraram P-10 a P-13. [REAL]

### 1.3 Fase 2 — Arquitetura (sem código de aplicação) [REAL]

Oito documentos em `architecture/` (moldura + 7 faces), coerentes entre si: `ARCHITECTURE_PROPOSAL.md`, `DATA_MODEL.md`, `UI_SPEC.md`, `WORKFLOW.md`, `PROMPT_COMPILER_SPEC.md`, `LEGAL_DOCKET_SPEC.md`, `RENDERING_SPEC.md`, `VALIDATION_CHECKLIST.md`. Definem o cockpit local-first "bancada do Tony Stark", o invariante **filesystem = fonte da verdade / SQLite = índice reconstruível**, as 12 abas por patente e o motor de manifesto SHA-256.

### 1.4 Fatos legais fixos que a Fase 3 codifica sem reabrir [LEGAL]

- **Só o ACOM raiz** `BR102025026951-1` tem **ePCT vivo**: **PCT/BR2025/050558**, de **05/12/2025**, depositado e pago. [LEGAL]
- **As 15 demais = hoje somente registro INPI; o ePCT ainda NÃO foi depositado — é o próximo passo planejado pelo operador** (novo processo originário, sem vínculo). Status = **A_DEPOSITAR / PENDENTE**, não "perdido". Os 10 recibos ePCT de 17/02/2026 (família PCT/BR2026/050068–050076) são uma **tentativa de protocolo abandonada de propósito** — defeituosa na forma, deixada precluir sem pagar as demais taxas: **rascunho preclusso a ser substituído** por um depósito novo e desvinculado, nunca proteção que se perdeu por descuido. [LEGAL][OPEN]
- **Achado material — P-10 (levar ao agente de PI com urgência):** os depósitos reivindicam **Prioridade Interna (66) = BR102025026951-1 (ACOM), 05/12/2025** (LPI art. 17), **confirmada por extração limpa em ACOM Mirror, ACOM Crypto e TGL Tensor** (conferir uma a uma nas demais 12). Se essa prioridade interna governar a Convenção de Paris, a janela de 12 meses para **depositar o novo ePCT de toda a família** venceria por volta de **05/12/2026** — bem antes de fev–mar/2027 —, tornando o próximo passo possivelmente **urgente**. É **questão exclusiva de parecer**: o docket exibe as janelas como "depende de parecer [LEGAL]", nunca decide em silêncio. [LEGAL][OPEN]

> **Aviso permanente (imutável em todo o módulo legal):** controle interno **não substitui** agente de propriedade industrial; prazos oficiais conferidos com INPI/WIPO.

---

## 2. O que a Fase 3 constrói (escopo em uma tela)

A Central é um **cockpit local e privado** (`127.0.0.1`) onde você controla desenvolvimento, prazos legais e instruções ao Claude Code, patente por patente. Cada patente termina num artefato vivo: **UM runner** `one_<slug>.py` que demonstra a **lógica** da invenção, sela a execução com SHA-256 e gera as imagens técnicas do protótipo — **sem jamais alegar validação física**.

**Stack aprovado na Fase 2** (você pode vetar/substituir com justificativa no gate):

| Camada | Tecnologias | Porta |
|---|---|---|
| Backend | FastAPI + Uvicorn · SQLite (WAL/FTS5) + SQLModel/Pydantic v2 · Watchdog (indexação) · motor de manifesto SHA-256 | `127.0.0.1:8765` |
| Runner runtime | **`tgl_env`** (`C:\IALD\observaveis_tgl\tgl_env`, com scipy/matplotlib) · `PYTHONUTF8=1` obrigatório | subprocess |
| Frontend | React + TypeScript + Vite + Tailwind + shadcn/ui · React Flow (componentes clicáveis) · React Three Fiber (3D [PILOTO]) · Plotly (gráficos) · OpenSeadragon (deep-zoom dos desenhos) | `127.0.0.1:5173` (dev) / servido em `8765` (operador) |

**Invariantes de projeto (herdados, inegociáveis):** originais imutáveis com prova · o número corrige a frase · **β nunca literal** (`ALPHA_FINE_CODATA_2018 * sqrt(e)` em runtime) · **simulação nunca valida física** (`physical_verdict_allowed=false`) · filesystem é a verdade, SQLite é cache · PT-BR na UI/docs, inglês no código · nada sobe para nuvem.

---

## 3. Ordem de implementação — 8 passos

Sequência proposta, do alicerce ao artefato vivo. Cada passo **entrega algo demonstrável** e só avança quando o anterior fecha. Os passos 1–7 constroem o cockpit; o passo 8 acende os runners.

| # | Passo | Constrói | Depende de | Marco |
|---|---|---|---|---|
| **1** | **Scaffold + backend + reindex** | Estrutura `backend/` e `frontend/` dentro da RAIZ; SQLite `central.db`; `reindex --full` que popula **16 Patent + 10 PatentClass** a partir do filesystem; `verify-originals` (re-hash `Patentes\`); `/health`. | Fases 0–2 | **M1** |
| **2** | **Dashboard + navegação** | Tela geral: 16 cards agrupados nas 10 classes; ACOM ★raiz, SkyGrid ★agregadora; selos de urgência de prazo; busca FTS; roteamento. | M1 | **M2** |
| **3** | **Página de patente — 12 abas** | Overview · Documentos · Reivindicações · Protótipo · Render 2D/3D · Runner · Execuções · Selo/Hash · Prazos · Notas · Instruções · **[COMPILAR INSTRUÇÕES]**. | M2 | **M3** |
| **4** | **Legal docket** | Docket INPI/ePCT/PCT por patente: ACOM ePCT vivo `PCT/BR2025/050558`; as 15 SOMENTE_INPI; janelas de Paris marcadas "depende de parecer" (P-10); alerta por urgência; aviso legal permanente. | M3 | **M4** |
| **5** | **Prompt Compiler** | Botão **[COMPILAR INSTRUÇÕES]** → `compiled_prompts/<ts>_CLAUDE_CODE_TASK.md`: header TGL Core → classe → patente → caminhos permitidos/proibidos → instruções `active` → tarefas priorizadas → critérios de aceite → a régua. Blocklist-aware. | M3 | **M5** |
| **6** | **Hash/Seal viewer** | Manifesto SHA-256 por documento e por artefato de runner; botão "verificar integridade" re-hasheia `Patentes\` ao vivo (== `original_hashes.json`); revalida `seal.json`. | M1 | **M6** |
| **7** | **Render viewer (Tony Stark)** | Camada (a) desenho original ampliável (OpenSeadragon, extraído dos PDFs) · (b) diagrama de componentes clicáveis (React Flow) · (c) 3D ilustrativo [PILOTO] — **sempre rotulado "ilustração de engenharia, não prova física"**. | M3 | **M7** |
| **8** | **Runners forma=conteúdo** | Harness (subprocess `tgl_env`, sem rede, timeout, captura de `results.json`/`seal.json`/figuras, `policy.py` anti-hardcode e veredito restrito) + runners na ordem da §4. | M1, M3, M6 | **M8** |

> Ordem de dependência dura: **1 é o alicerce de tudo**; 6 (hash) e 8 (runners) dependem do motor de manifesto do passo 1; 3 (abas) é a moldura onde 4–7 aparecem. 2–7 podem paralelizar parcialmente após M1, mas a **verificação de originais (6) acompanha cada passo** — nunca é deixada para o fim.

---

## 4. Ordem sugerida dos runners

**Regra-mãe:** todo runner nasce **scaffold honesto** e só sobe de marcador com evidência gravada **+ confirmação do operador**. `physical_verdict_allowed=false` é padrão; simulação demonstra a **lógica**, jamais a física. Começamos onde o disco JÁ entrega protótipo — **SkyGrid é o gabarito vivo**.

### Onda 0 — o gabarito (já fecha o modelo)

| # | Patente | Classe | Estado inicial | Base de protótipo |
|---|---|---|---|---|
| 13 | **SkyGrid** ★agregadora | 06 | **[PILOTO]** (gabarito) | `Patentes\Skygrid\SkyGrid_Piloto\` v3 — 18 módulos, testes fail-closed, selos; `MODEL_CLOSES / ENERGY_BALANCE_OK ([SIM] sob [CONJ])`, `beta_runtime=0.012031300400803142`, `physical_verdict_allowed:false` |

SkyGrid primeiro porque o gêmeo digital v3 **já existe e já fecha balanço no nível do modelo**. `one_skygrid.py` é **consolidação** (v1+v2+v3), não invenção nova. É o teto de veredito herdável por toda a Central: `MODEL_CLOSES` + "resta a bancada". [ENERGY][SIM][CONJ]

### Onda 1 — [SIM]-ready (protótipo dedicado identificado; promove no 1º ciclo)

| # | Patente | Classe | Estado | Protótipo a copiar (READ-ONLY → `vault/originals_copy/`) |
|---|---|---|---|---|
| 1 | **ACOM** ★raiz | 01 | [SIM]-ready | `projetos_pyhton\acom\acom_unified.py`, `acom_universal_mk*.py` |
| 4 | TGL Tensor | 01 | [SIM]-ready | `projetos_pyhton\tgl-tensor\tgl_tensor_v*.py` (⚠ **nunca** copiar `token_huggin.txt` — P-09) |
| 10 | MQC | 05 | [SIM]-ready | `projetos_pyhton\acom\mqc_simulacao_celula_elementar.py` + `MQC_relatorio_metricas.json` |
| 2 | ACOM Mirror | 02 | [SIM]-ready | `projetos_pyhton\acom\Acom_v17_mirror.py` |
| 3 | ACOM Crypto | 02 | [SIM]-ready | `projetos_pyhton\acom\Acom_v17_mirror_crypto.py`, `TGL_v11_ESPELHO.py` |
| 5 | IALD (GKSL) | 03 | [SIM]-ready | kernels `IALD\Atualização Kernel\` (v4–v11) — **nunca** rodar `iald_web_server.py` (produção com usuários reais) |
| 8 | Ψ-NET / PsiBit | 04 | [SIM]-ready | `projetos_pyhton\acom\Psi_net_protocol_v1.py`, `acom_psibit_v*.py` |
| 14 | Aprendizado Contínuo | 03 | [SIM]-ready | `iald_stack_v7.py` (usar **local**, nunca exportar — confidencial) |
| 16 | Kernel Ontológico | 03 | [SIM]-ready | kernels IALD + `TGL_CORE_MEMORY.md` |

Ordem de ataque sugerida dentro da Onda 1 (a que a memória semeia): **ACOM/Tensor → MQC → Mirror/Crypto → IALD → Ψ-NET/PsiBit**, depois os dois de cognição contínua (Aprendizado, Kernel). Você fixa a ordem final.

### Onda 2 — [SIM] lógica via módulos do próprio SkyGrid_Piloto

| # | Patente | Classe | Estado | Base |
|---|---|---|---|---|
| 11 | Dípolo Transistor | 05 | [SIM] (lógica) | módulo `dipolo` em `SkyGrid_Piloto\skygrid_sim\` |
| 12 | Célula de Reversão | 06 | [SIM] (lógica) | módulo `celula_reversao` em `SkyGrid_Piloto\skygrid_sim\` (classe a confirmar — P-04) |

### Onda 3 — scaffolds honestos [DATA_REQUIRED] (fail-closed; declaram o que falta)

| # | Patente | Classe | Estado | Por quê scaffold |
|---|---|---|---|---|
| 6 | Supercondutor Holográfico | 05 | **[DATA_REQUIRED]** | sem protótipo → scaffold **[HARDWARE]** fail-closed |
| 7 | Motor de Dobra | 07 | **[DATA_REQUIRED]** | só digital twin **[SIM]** da lógica; **sem** validação física (propulsão) |
| 9 | Fusão a Frio / OH | 06 | **[DATA_REQUIRED]** | sem código de simulação localizado; scaffold **[ENERGY]** travado |
| 15 | Oncologia | 08 | **[DATA_REQUIRED]** | só lógica computacional **[MEDICAL]**; **nenhum** protocolo clínico, **nenhuma** promessa de cura |

> **Travas de domínio que nenhum critério fura:** CLASS_06 (Energia), CLASS_07 (Propulsão) e CLASS_08 (Saúde) têm teto — **só simulação e revisão técnica**, nenhuma instrução operacional perigosa, nenhum protocolo clínico, nenhuma alegação de energia/cura. Camadas físicas entram como mock/pipeline [HARDWARE], nunca misturadas com [PILOTO]. Stacks confidenciais (`iald_stack_v7.py`, `iald_psion_state.json`) podem ser **usados localmente**, mas **nunca** entram em selo, render ou export.

---

## 5. Entregáveis da 1ª rodada e critérios de PRONTO

A primeira rodada da Fase 3 está **pronta** quando **todos** os itens abaixo forem demonstráveis a você (espelham o Nível B do `05_CHECKLIST_VALIDACAO_USUARIO.md`). Cada item fecha **só com evidência** (caminho + comando + saída, ou inspeção visual sua).

### 5.1 Infra e integridade
- [ ] `backend/` e `frontend/` criados **dentro da RAIZ**, sem tocar `Patentes\`/`memory\`/`patents\`/`vault\`/`source_inventory\`/`compiled_prompts\`/`logs\`/`tools\`.
- [ ] Backend sobe em `127.0.0.1:8765`; `GET /health` → `patents_indexed:16`, `classes_indexed:10`, `originals_manifest_ok:true`, `external_calls:"disabled"`. [REAL]
- [ ] `reindex --full` popula **16 Patent + 10 PatentClass** do filesystem; **idempotência provada** (apagar `central.db`, reindexar, `/health` volta a 16). Filesystem é o dono; o `.db` é cache.
- [ ] **Originais intactos:** re-hash de `Patentes\` == `source_inventory/original_hashes.json` → **308/308, 0 diferenças**; badge verde na UI + registro em `logs/`. [REAL]

### 5.2 Navegação (a bancada)
- [ ] Dashboard geral: 16 patentes nas 10 classes, prazos vivos, status de integridade.
- [ ] Página de patente com as **12 abas** navegando inteiro para ao menos **duas** patentes de perfis distintos: **SkyGrid** (tem protótipo/piloto) e **ACOM** (raiz, ePCT vivo).
- [ ] Render viewer: deep-zoom do desenho oficial + diagrama de componentes clicáveis; 3D [PILOTO] onde aplicável, sempre rotulado.
- [ ] Legal docket com a regra ePCT correta na tela e o aviso legal permanente.

### 5.3 Funções vivas
- [ ] **Runner** disparável pela UI para ao menos **SkyGrid**: gera `results.json`/`seal.json`/figuras; `physical_verdict_allowed=false` exibido; **nenhum vocabulário de veredito proibido** escapa (PROVED/CONFIRMED/TGL_TRUE/REFUTED); máximo `SUPPORTED_NOT_CONFIRMED`/`INCONCLUSIVE`.
- [ ] **Prompt Compiler** funcional: `[COMPILAR INSTRUÇÕES]` gera o `.md` com o contrato completo; só entram itens `active:true`; **β nunca literal** e confidenciais nunca embutidos.
- [ ] **Hash/Seal viewer** funcional (manifesto de originais e de artefatos de runner).
- [ ] **Busca FTS** sobre patentes, notas, docket e memórias.

### 5.4 Disciplina (vetos)
- [ ] **Nenhum arquivo original modificado** — re-hash pós-rodada == hashes iniciais. *Se mudou um byte, a rodada inteira é rejeitada.* [REAL]
- [ ] Nenhum confidencial exportado (blocklist testada; `token_huggin.txt` jamais na Central — P-09).
- [ ] **Toda escrita da UI foi ao arquivo primeiro** — apagar `central.db` e `reindex --full` reproduz o estado exibido (prova viva de que o filesystem é a verdade).
- [ ] `logs/` registra a rodada (o que foi construído, verificado, reinscrito). Memória é lei.

---

## 6. Marcos (M0–M8) e sequência de aceite

Cada marco é uma parada natural onde você pode conferir e seguir (ou pausar). Nenhum marco "vale" sem a prova de integridade dos originais anexada.

> [nota operacional do operador — omitida no retrato público]

Após M8 fechado com o Nível B do checklist, a **primeira rodada** está aceita e a Central entra no regime permanente da Fase 4.

---

## 7. O loop sem fim (Fase 4)

Depois da 1ª rodada, cada patente avança pelo mesmo ciclo canônico. **Você decide e valida; o Claude Code implementa e inscreve; a plataforma orquestra sem opinar.**

```
ESCOLHER pela raiz (√) → PLANEJAR (mínimo, reversível) → IMPLEMENTAR
   → VERIFICAR DE VERDADE (rodar, abrir, testar; re-hash dos originais intactos)
   → INSCREVER na plataforma (progresso da patente + logs/ + selo) → PRÓXIMO
```

- **ESCOLHER (você):** o dashboard mostra a fila; "pela raiz" = o que já tem protótipo primeiro (ordem da §4). Ativa notas/instruções e aperta **[COMPILAR INSTRUÇÕES]**.
- **PLANEJAR / IMPLEMENTAR / VERIFICAR (Claude Code):** copia protótipos reais para `vault/originals_copy/` (com SHA-256), escreve `one_<slug>.py`, roda no `tgl_env`, cola os números reais, re-hasheia os originais.
- **INSCREVER:** fecha as instruções consumidas, anexa ao `progress_log.md`, sela o ciclo em `logs/cycle_log.md`, atualiza o `runner_state.yaml`. O Watchdog reindexa; a bancada reflete o novo estado.
- **Ciclo de vida do runner:** `[DATA_REQUIRED] → [SIM] → [PILOTO] → demonstração real`. A última transição **só** com dado de bancada física [HARDWARE]/[REAL] e **decisão expressa sua**. Sem bancada, `physical_verdict_allowed` permanece `false` em toda a Central.
- **HALT duro:** se o re-hash dos originais divergir, o ciclo **para**, registra pendência `[ABERTA]`, alerta vermelho no dashboard e **aguarda você** — nunca escolhe em silêncio.

---

## 8. Riscos conhecidos que a construção já mitiga

| Risco | Mitigação embutida no plano |
|---|---|
| DB tratado como verdade | Endpoints de escrita **só** gravam arquivo + reindex; `reindex --full` sempre possível; teste "DB = função pura dos arquivos". |
| Modificação acidental de original | Guarda `readonly.py` nega escrita sob `Patentes\`/fora da RAIZ; `verify-originals` no boot e em cada ciclo; Watchdog trata mudança em `Patentes\` como incidente. |
| Runner alega física | `policy.py` exige `physical_verdict_allowed=false`, rejeita vocabulário proibido, herda teto do SkyGrid; UI carimba "não valida física". |
| β hardcoded | Auditoria anti-hardcode na suíte (procura literal `0.012031…`); β só de `seal.json.beta_runtime`; `ALPHA_FINE_CODATA_2018 * sqrt(e)` em runtime. |
| Vazamento de confidencial | `blocklist.py` consultada por toda leitura de conteúdo e pelo compilador; token nunca copiado (P-09). |
| Selo do artefato canônico defasado (P-07) | Exibir SHA **executado** e SHA **pinado** lado a lado, ligados à pendência; nunca "consertar" em silêncio. |
| Janela de Paris / prioridade interna (P-10) | Docket marca "depende de parecer [LEGAL]"; achado material levado ao agente de PI; a plataforma **não** decide prazo. |

Pendências abertas relevantes para a construção: **P-03** (nº 2024 `BR 10 2024 026367 3` — impacta prioridade), **P-04** (classe da Célula de Reversão), **P-05** (dossiês PCT legacy em inglês não localizados), **P-07** (SHA do paper), **P-08** (rascunhos pipeline CLASS_09), **P-09** (segredo HuggingFace), **P-10/P-11/P-12** (prioridade interna, data 05 vs 09/12, anexo trocado no Crypto). Nenhuma delas bloqueia o gate por si só, mas todas são reconhecidas — nada varrido para baixo do tapete.

---

## 9. Selos honrados por este plano

`TGL_PATENT_CONTROL_CENTER` · `FORM_EQUALS_CONTENT_FOR_EACH_PATENT` · `ONE_RUNNER_ONE_PATENT_ONE_SEAL` · `DO_NOT_MODIFY_ORIGINALS` · `MEMORY_FIRST_ARCHITECTURE_SECOND_CODE_LAST` · `SIMULATION_NEVER_VALIDATES_PHYSICS`.

---

## 10. O que você decide neste GATE

1. **Aprovar a ordem de implementação** (§3, passos 1–8) — ou reordenar.
2. **Aprovar a ordem dos runners** (§4) — SkyGrid primeiro; depois ACOM/Tensor/MQC/Mirror/Crypto/IALD/Ψ-NET; Dípolo/Célula na Onda 2; scaffolds honestos para Supercondutor/Motor/Fusão/Oncologia — **e fixar a ordem final**.
3. **Aprovar (ou substituir com justificativa) o stack** da §2.
4. **Confirmar os critérios de PRONTO** da 1ª rodada (§5) como contrato de aceite.
5. **Assinar a liberação (M0/A.11)** — sem ela, a Fase 3 não escreve uma linha.

> **Frase-âncora esperada:** *"Memórias e arquitetura preparadas. Nenhuma linha de código de aplicação foi escrita. Nenhum arquivo original foi modificado. **Autorizo a Fase 3.**"*
>
> **TGL = haja luz. Tetelestai. 1 = 1.**
