# 00 — INVENTÁRIO GERAL DA CENTRAL DE PATENTES TGL

**Documento de apresentação ao operador — GATE de validação (Fases 0–2)**
**Operador:** Luiz Antonio Rotoli Miguel — **IALD Ltda.** (CNPJ 62.757.606/0001-23, Goiânia/GO · ORCID 0009-0005-1114-6106)
**Pasta de trabalho:** `C:\IALD\Central de Patentes`
**Data:** 09/07/2026 · **Estado:** aguardando sua validação expressa (nenhuma linha de código de aplicação foi escrita; nenhum arquivo original foi modificado)

> **Para que serve esta página.** É o panorama do que a Central contém **hoje**: a
> estrutura de pastas criada, a contagem exata dos arquivos originais, o resultado do
> Estado Verificado (Fase 0), o resultado da auditoria adversarial, as provas de
> integridade e a lista completa dos artefatos produzidos nesta rodada. É leitura
> humana. Os números vieram dos arquivos — não de memória de modelo.

---

## 1. O que a Central protege — em uma frase

**16 patentes de invenção (PI) depositadas no INPI**, em **10 classes temáticas**,
todas de titularidade da **IALD Ltda.**, inventor **Luiz Antonio Rotoli Miguel**.
A raiz de tudo é o **ACOM** (BR102025026951-1, 05/12/2025); a agregadora é o
**SkyGrid** (BR102026004850-0). Este projeto é o cockpit de controle e desenvolvimento
delas — construído **memória primeiro, arquitetura segundo, código por último**.

**Regra ePCT (sua palavra, 09/07/2026):** [LEGAL]
- **SÓ o ACOM raiz** tem ePCT **vivo, depositado e pago** — **PCT/BR2025/050558**, de **05/12/2025**.
- As **15 demais** patentes = **somente registro INPI hoje**; o ePCT **ainda não foi depositado** — é o **próximo passo** planejado pelo operador (novo processo originário, **sem vínculo**). Status = **A_DEPOSITAR / PENDENTE**, não "perdido". [OPEN — ação a fazer]
- Os **10 recibos ePCT de 17/02/2026** (família PCT/BR2026/050068–050076) no Acervo = **tentativa de protocolo abandonada de propósito**: o operador não pagou as demais taxas, preferiu **deixar precluir** por ser "defeituosa na forma", e vai iniciar um depósito **novo e desvinculado**. É **rascunho preclusso a ser substituído**, não proteção que se perdeu por descuido.

---

## 2. Estrutura de pastas criada

Tudo abaixo de `C:\IALD\Central de Patentes`. A pasta `Patentes\` é o acervo original
**READ-ONLY** (ler, hashear, copiar — nunca editar). Todo o resto foi produzido nesta rodada.

```
C:\IALD\Central de Patentes\
├── Patentes\                    [READ-ONLY]  os 308 depósitos originais (17 subpastas)
├── PROMPT_INAUGURAL_CENTRAL_DE_PATENTES.md   a constituição do projeto (a régua)
├── PENDENCIAS.md                             P-01 … P-13 (o que perguntar ao operador/agente)
├── memory\
│   ├── TGL_CORE_MEMORY.md                    header ontológico — a TGL na memória da Central
│   ├── PATENT_MASTER_INDEX.yaml              índice-mestre das 16 patentes (extraído dos PDFs)
│   ├── classes\   CLASS_01 … CLASS_10 (.md)  as 10 linhas de pesquisa
│   └── patents\   16 memórias técnicas (.md) uma por patente
├── patents\        16 pastas <ID>_<SLUG>\
│   └── <cada uma>\ docket.yaml + notes\initial_notes.md
├── architecture\   8 especificações (.md)    a arquitetura da plataforma (Fase 2)
├── tools\          3 utilitários (.py)        inventário, índice e verificação de integridade
├── source_inventory\  3 JSONs                 a prova imutável do acervo (hashes + extração)
├── vault\
│   ├── originals_copy\zips\                   cópias de leitura dos 3 zips do acervo
│   ├── normalized_docs\Patentes\             154 textos extraídos dos PDFs
│   └── tgl_verification\                      cópias executadas de um.py e do paper + saídas
├── compiled_prompts\   (vazia — preenchida na Fase 3 pelo Prompt Compiler)
└── logs\               (vazia — preenchida na operação)
```

**O que cada pasta guarda:**

> [nota operacional do operador — omitida no retrato público]

---

## 3. Contagem dos arquivos originais (reconciliada)

Os três números do acervo, e como se encaixam:

| Nº | Significado | Fonte |
|---|---|---|
| **336** | Total de arquivos hasheados = **308 originais** de `Patentes\` **+ 28** extraídos dos 3 zips do acervo | `original_hashes.json` |
| **308** | Os **originais READ-ONLY** sob `Patentes\` — o conjunto coberto pela garantia de imutabilidade | `verify_integrity.py` |
| **154 de 178** | PDFs cujo **texto foi extraído com sucesso** (24 falharam — em geral digitalizações/imagens) | `extraction_report.json` |

**Os 28 dos zips** (dentro de `vault\originals_copy\zips\`, só leitura): *Acervos de Patentes INPI* (13) · *Depósito 1 no epct* (10) · *Informações sobre o Depósito Internacional PCT* (5).

**Composição dos 308 originais** (por extensão): 154 `.pdf` · 43 `.pyc` · 40 `.py` · 14 `.md` · 14 `.json` · 12 `.tex` · 12 `.png` · 8 `.docx` · 3 `.zip` · 2 `.jsonl` · 2 `.html` · 2 `.mp4` · 1 `.jsx` · 1 sem extensão. O grosso (134 arquivos) é o **piloto SkyGrid** — o gêmeo digital já funcional.

**Extração de texto:** os 154 PDFs lidos com sucesso viraram 154 textos normalizados em `vault\normalized_docs\Patentes\`, base de onde o índice-mestre e as memórias foram construídos.

---

## 4. Estado Verificado — Fase 0 (o chão factual de hoje) [REAL]

Rodados como **cópias** dentro de `vault\tgl_verification\` (originais jamais editados),
em `tgl_env`, `PYTHONUTF8=1`. Os números abaixo saíram da máquina, não de memória.

### 4.1 `um.py` — o Um inscrito
- **VEREDITO:** `1=1=VERDADEIRO=HAJA_LUZ`
- Identidade de Lagrange `1 = q² + α²` → resíduo **0.0e+00**
- **β_TGL = 0.012031300401** — **emergiu em runtime** (`α·√e`), nunca literal
- **M_GA (Grande Atrator):** Modo A = 2.744e16 M☉ · Modo B = 1.986e16 M☉ — **ambos na janela cosmológica pré-registrada** [1e15, 1e17] M☉; sensibilidade 300/300 (100%) na banda
- Selo `um_grande_atrator_selo.json`, timestamp **2026-07-09 10:27:14**
- Auditoria: `geometry_only=true`, `beta_hardcoded=false`, `free_parameter_used=false`, `only_runtime_input="1"`

### 4.2 `tgl_paper_unified.py --quick --no-live`
- **RUN COMPLETE** em 26,81 s · `results.json` (118 KB) + **16 figuras** geradas
- **β = 0.012031300400803142** · **Cross-substrate consistency = PASS** (mesmo β em 4 substratos) · BBN PASS · H0 PASS
- Honestidades gravadas no próprio resultado (negativos declarados, não escondidos): torus ~10× DECLARADO · eco GW como predição falsificável · Qwen assado = ilustração
- Observação registrada em **P-07:** o SHA-256 da cópia (`29c92b66…`) **diverge** do selo pinado na memória raiz (`dea07d8e…`) — o arquivo evoluiu após o selo; é pendência para o operador atualizar o selo, não erro da Central. [DATA]

---

## 5. Auditoria adversarial das 16 memórias [REAL]

Cada memória técnica foi conferida, uma a uma, **contra os documentos extraídos**:

| Resultado | Quantidade |
|---|---|
| **FIEL** | 8 |
| **FIEL_COM_RESSALVAS** | 8 |
| **REVISAR** | **0** |

Em **todas as 16**: título oficial (campo 54) confere · número de processo confere ·
data confere · regra ePCT correta. **Nenhuma memória precisou ser reescrita.** As
ressalvas viraram as pendências P-10 a P-13 (correções de fidelidade e questões legais),
nenhuma delas alterando fato, número ou situação jurídica.

---

## 6. Provas de integridade — os originais estão intactos [REAL]

`tools\verify_integrity.py` re-hasheia todo o `Patentes\` e compara com a linha de base:

```
baseline=308  current=308
added=0  removed=0  changed=0
VERDICT: ORIGINALS_INTACT
```

**308 = 308, zero drift.** Nenhum arquivo original foi escrito, movido, renomeado ou
apagado. Toda leitura/execução ocorreu em cópias sob `vault\`. Selos das cópias em
`vault\tgl_verification\COPIES_SHA256.txt` (um.py `cc24dd9d…`, paper `29c92b66…`).

---

## 7. Achado material para o agente de PI — P-10 [LEGAL][OPEN]

**Prioridade Interna (66) ao ACOM (05/12/2025).** Os depósitos reivindicam prioridade
interna (LPI art. 17) apontando para **BR102025026951-1** — **confirmado por extração
limpa em ACOM Mirror, ACOM Crypto e TGL Tensor**; nas demais, conferir uma a uma no rosto
do PDF. **Consequência:** se a prioridade de 05/12/2025 governar a Convenção de Paris, a
janela de 12 meses para depósito PCT de **toda a família** venceria por volta de
**05/12/2026** — antes das datas de fev–mar/2027 calculadas pela data de depósito, o que torna
**o próximo passo (o novo ePCT desvinculado) possivelmente urgente**. **Ação: levar ao agente de PI com urgência.**
Controle interno não substitui agente de propriedade industrial.

---

## 8. Artefatos produzidos nesta rodada (com contagem)

| # | Artefato | Contagem | Local |
|---|---|---|---|
| 1 | Prompt inaugural (a constituição/régua) | **1** | `PROMPT_INAUGURAL_CENTRAL_DE_PATENTES.md` |
| 2 | Núcleo ontológico TGL | **1** | `memory\TGL_CORE_MEMORY.md` |
| 3 | Índice-mestre das patentes | **1** | `memory\PATENT_MASTER_INDEX.yaml` |
| 4 | Memórias de classe | **10** | `memory\classes\CLASS_01…10.md` |
| 5 | Memórias técnicas de patente | **16** | `memory\patents\*.md` |
| 6 | Dockets jurídicos | **16** | `patents\*\docket.yaml` |
| 7 | Cadernos de notas iniciais | **16** | `patents\*\notes\initial_notes.md` |
| 8 | Especificações de arquitetura | **8** | `architecture\*.md` |
| 9 | Registro de pendências | **1** (P-01…P-13) | `PENDENCIAS.md` |
| 10 | Ferramentas utilitárias | **3** | `tools\*.py` |
| 11 | Inventário-fonte (provas) | **3** JSONs | `source_inventory\*.json` |
| 12 | Verificação TGL (cópias executadas + saídas) | um.py + paper + 16 figuras + selos | `vault\tgl_verification\` |

**As 8 especificações de arquitetura (Fase 2):** `ARCHITECTURE_PROPOSAL` ·
`DATA_MODEL` · `UI_SPEC` · `WORKFLOW` · `PROMPT_COMPILER_SPEC` · `LEGAL_DOCKET_SPEC` ·
`RENDERING_SPEC` · `VALIDATION_CHECKLIST`. Todas marcadas "nenhum código de aplicação".

**As 3 ferramentas:** `inventory_and_extract.py` (varredura + hash + extração de texto) ·
`build_master_index.py` (monta o índice a partir dos textos) · `verify_integrity.py`
(prova que os originais não mudaram). Os scripts de verificação da TGL (`um.py`,
`tgl_paper_unified.py`) rodaram como **cópias** em `vault\tgl_verification\`.

---

## 9. As 16 patentes por classe (mapa de uma olhada)

| Classe | Patentes depositadas | Nº |
|---|---|---|
| **01 · ACOM/Tensor** | ACOM ★raiz, TGL Tensor | 2 |
| **02 · Mirror/Crypto** | ACOM Mirror, ACOM Crypto | 2 |
| **03 · IALD/Cognição** | IALD, Aprendizado Contínuo, Kernel Ontológico | 3 |
| **04 · Ψ-NET** | Ψ-NET / TGL Net Protocol | 1 |
| **05 · Hardware Holográfico** [HARDWARE] | Supercondutor, MQC, Dípolo Transistor | 3 |
| **06 · Energia** [ENERGY] | SkyGrid ★agregadora, Fusão a Frio, Célula de Reversão | 3 |
| **07 · Propulsão** [SIM] | Motor de Dobra | 1 |
| **08 · Saúde** [MEDICAL] | Oncologia Luminodinâmica | 1 |
| **09 · PCT/Legacy/Drafts** | (rascunhos não depositados — pipeline) | 0 |
| **10 · Legal/Docket** | (classe transversal jurídica) | 0 |
| | **Total depositadas** | **16** |

---

## 10. Tabela resumo — o estado da Central hoje

| Item | Valor | Estado |
|---|---|---|
| Patentes depositadas (INPI, PI) | 16 em 10 classes | [REAL] |
| Titular / inventor | IALD Ltda. / Luiz Antonio Rotoli Miguel | [REAL] |
| ePCT vivo | 1 — só ACOM raiz (PCT/BR2025/050558, 05/12/2025) | [LEGAL] |
| Demais patentes | somente registro INPI; ePCT **a depositar** (próximo passo, novo e desvinculado); recibos de 17/02/2026 = tentativa preclusa a substituir | [LEGAL][OPEN] |
| Arquivos hasheados (total) | 336 (308 originais + 28 de zips) | [REAL] |
| Originais READ-ONLY | 308 | [REAL] |
| PDFs com texto extraído | 154 de 178 | [REAL] |
| Estado Verificado — `um.py` | `1=1=VERDADEIRO=HAJA_LUZ`; β=0.012031300401; M_GA na janela | [REAL] |
| Estado Verificado — paper | RUN COMPLETE; cross-substrate β **PASS**; 16 figuras | [REAL] |
| Auditoria das 16 memórias | 8 FIEL + 8 FIEL_COM_RESSALVAS + 0 REVISAR | [REAL] |
| Integridade dos originais | 308 = 308, **zero drift** (ORIGINALS_INTACT) | [REAL] |
| Achado material | P-10 — prioridade interna (66) ao ACOM → levar ao agente de PI | [LEGAL][OPEN] |
| Pendências registradas | P-01 … P-13 | — |
| Código de aplicação escrito | **nenhum** | [REAL] |

---

## 11. Rodapé — a régua e o próximo passo

> **A régua (inviolável):** o número corrige a frase · β nunca literal (`α·√e` em
> runtime) · simulação nunca valida física (`physical_verdict_allowed=false`) ·
> não modificar nenhum original · memória primeiro, arquitetura segundo, código por
> último. Aviso permanente [LEGAL]: o controle interno **não substitui** agente de
> propriedade industrial; prazos oficiais conferidos com INPI/WIPO.

**Veredito da rodada:** *"Memórias e arquitetura preparadas. Nenhuma linha de código de
aplicação foi escrita. Nenhum arquivo original foi modificado."*

**Próximo passo:** sua validação expressa deste GATE. Este documento acompanha
`01_MAPA_DE_CLASSES.md`, `02_MAPA_DE_PATENTES.md`, `03_ARQUITETURA_PROPOSTA.md`,
`04_PLANO_DE_CONSTRUCAO.md`, `05_CHECKLIST_VALIDACAO_USUARIO.md` e `PENDENCIAS.md`.
**A Fase 3 (construção) só começa após seu aval.**

**TGL = haja luz. Tetelestai. 1 = 1.**
