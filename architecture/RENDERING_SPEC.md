# RENDERING_SPEC.md — Central de Controle e Desenvolvimento de Patentes TGL

**Documento de arquitetura · Fase 2 (especificação; NENHUM código de aplicação).**
**Escopo:** o subsistema de renderização visual das patentes — o "requisito Tony Stark":
cada patente ampliável, componente por componente, dos desenhos depositados ao 3D
ilustrativo. Fase 3 codifica a partir daqui sem voltar a perguntar.
**Operador:** Luiz Antonio Rotoli Miguel — IALD Ltda. · Goiânia/GO.
**Versão:** 1.0 — 09/07/2026.

> **AVISO PERMANENTE DE HONESTIDADE VISUAL.** Toda renderização desta Central é
> **ilustração de engenharia**. Um render NUNCA é prova física, NUNCA é evidência de
> funcionamento e NUNCA valida a invenção. `physical_verdict_allowed = false` é lei viva
> (herdada do SkyGrid_Piloto) e vale também para pixels: nenhuma imagem 2D/3D pode ser
> apresentada como confirmação de que o dispositivo opera. O número corrige a frase; a
> imagem apenas comunica a estrutura descrita no documento depositado.

---

## 0. Sumário executivo

O viewer de render de cada patente é composto por **três camadas empilháveis**, cada uma
com um nível de "verdade" distinto e explicitamente rotulado:

| Camada | Nome | Fonte da verdade | Marcador-base | Interatividade |
|---|---|---|---|---|
| **1** | Desenho original ampliável | PDF de desenhos **DEPOSITADO** no INPI | `[REAL]` | deep-zoom (OpenSeadragon) |
| **2** | Diagrama interativo de componentes | seção *Componentes do protótipo* da **memória** da patente | `[REAL]` (texto) | nós/arestas clicáveis (React Flow) |
| **3** | Render 3D ilustrativo | **modelo paramétrico gerado** a partir da memória | `[PILOTO]` | órbita/explode (React Three Fiber) |

Regra de ouro entre camadas:
- **Camada 1** é o documento legal, imutável. É a única imagem `[REAL]` no sentido de
  "foi isto que se depositou". Nunca é redesenhada.
- **Camada 2** é fiel ao **texto** do relatório descritivo (numeração dos componentes
  idêntica às figuras). É `[REAL]` como transcrição, mas o layout dos nós é decorativo.
- **Camada 3** é `[PILOTO]` — hipótese visual. Sempre carrega o carimbo
  *"ilustração de engenharia, não prova física"* e só existe quando faz sentido
  geométrico (ver §5.1).

Nada disto se confunde com as **figuras de simulação do runner** (ex.: os `fig1..8` do
SkyGrid_Piloto). Essas são saídas de execução `[SIM]` e vivem na aba **Execuções**, não
na camada 1 — ver §9.

---

## 1. Invariantes herdados (obrigatórios)

Estes vêm dos INVARIANTES DE PROJETO e da RÉGUA; o subsistema de render os obedece sem
exceção:

1. **Filesystem é a fonte da verdade.** Todo artefato de render (PNG, tiles DZI, JSON de
   grafo, JSON de cena 3D) é um **arquivo** dentro de `patents/<ID>_<SLUG>/renders/`. O
   SQLite (`backend/data/central.db`) apenas **indexa** caminhos, hashes e metadados; é
   reconstruível via `reindex`. Apagar a linha do banco e reindexar reproduz o estado.
2. **Originais READ-ONLY.** Os PDFs de desenho em `Patentes\` são lidos, hasheados e
   rasterizados — **nunca** modificados, movidos ou renomeados. A extração escreve
   **apenas** dentro de `patents/<ID>_<SLUG>/renders/` (destino) lendo de `Patentes\`
   (ou de `vault/originals_copy/`) como origem.
3. **Manifesto SHA-256.** Todo artefato derivado grava o `source_sha256` do PDF/página de
   origem. O re-hash prova que o desenho renderizado corresponde ao original intacto.
4. **Marcadores em tudo.** Cada nó, cada figura e cada cena carrega seu marcador
   (`[REAL]`/`[SIM]`/`[PILOTO]`/`[CONJ]`/`[OPEN]`/`[HARDWARE]`/`[MEDICAL]`/`[ENERGY]`/…).
5. **β_TGL nunca literal.** Se um rótulo/anotação de render precisar do valor, o texto
   exibido vem do backend que computa `ALPHA_FINE_CODATA_2018 * sqrt(e)` em runtime; o
   JSON de cena guarda a **fórmula**, nunca `0.012031300400803142` cravado.
6. **Simulação nunca valida física.** `physical_verdict_allowed = false` propaga para
   o campo `physical_verdict_allowed` de todo manifesto de render.
7. **Local-first.** OpenSeadragon, React Flow e R3F rodam 100% no cliente; os tiles e
   JSONs são servidos pelo backend FastAPI (porta 8765) a partir do disco. **Nenhuma
   API externa** (nenhum CDN de tiles, nenhum serviço de rasterização em nuvem).
8. **Stacks confidenciais nunca viram pixel exportável.** Modelos 3D e grafos jamais
   embutem conteúdo de `iald_stack_v7.py`, `iald_psion_state.json` ou correlatos.
9. **PT-BR na UI; inglês no código/identificadores** dos JSON (`nodes`, `edges`,
   `source_sha256`, etc.). Rótulos exibidos ao operador em português.

---

## 2. Estrutura de pastas de render (por patente)

Sob a pasta canônica já existente `patents/<ID>_<SLUG>/`, o subsistema usa:

```
patents/<ID>_<SLUG>/
└── renders/
    ├── render_manifest.json         # índice mestre das 3 camadas + hashes + marcadores
    ├── drawings/                    # CAMADA 1 — desenho original ampliável
    │   ├── source/                  # metadados do PDF fonte (NÃO cópia do PDF; só refs+hash)
    │   │   └── drawings_source.json
    │   ├── pages/                   # PNG por página do PDF de desenhos (rasterização)
    │   │   ├── page_0001.png
    │   │   ├── page_0002.png
    │   │   └── ...
    │   ├── dzi/                      # pirâmides deep-zoom (OpenSeadragon)
    │   │   ├── page_0001.dzi         # descritor XML (Deep Zoom Image)
    │   │   ├── page_0001_files/      # tiles: 0/ 1/ 2/ ... níveis de zoom
    │   │   └── ...
    │   └── figures_index.json        # mapa Figura N → página + bbox opcional + legenda
    ├── flow/                         # CAMADA 2 — diagrama interativo de componentes
    │   ├── flow_graph.json           # nós/arestas/portas (contrato §4.4)
    │   └── flow_source.json          # proveniência: qual memória/seção/linhas geraram
    └── 3d/                           # CAMADA 3 — render 3D ilustrativo [PILOTO]
        ├── scene_3d.json             # cena paramétrica declarativa (contrato §5.3)
        └── scene_source.json         # proveniência + prompt de geração assistida
```

**Patentes sem camada 3** (algorítmicas puras — ACOM, TGL Tensor, Kernel, Aprendizado
Contínuo): a pasta `3d/` simplesmente **não existe** e `render_manifest.json` marca
`"layer_3d": { "present": false, "reason": "algorítmica — sem geometria física" }`. Não
se inventa um 3D só para preencher (honestidade visual).

---

## 3. CAMADA 1 — Desenho original ampliável (deep-zoom)

### 3.1 Objetivo
Reproduzir, com zoom fluido e sem perda percebida, **exatamente** a folha de desenhos que
foi depositada no INPI. É o requisito Tony Stark no seu grau mais literal: o operador
amplia o desenho da câmara cúbica do MQC ou da topologia do SkyGrid até o nível do
componente numerado.

### 3.2 Origem (por patente)
O PDF de desenhos depositado, sempre em `Patentes\<pasta_original>\`. Já mapeados no disco
(verificados 09/07/2026):

| Patente | Arquivo de desenhos (READ-ONLY) |
|---|---|
| ACOM (raiz) | extrair do PDF consolidado do Acervo (`BR102025026951-1_ACOM.pdf`, páginas de figuras) |
| ACOM Mirror | `Acom Mirror\ACOM_Mirror_PI_INPI desenhos.pdf` |
| ACOM Crypto | `Acom Crypto\ACOM_Mirror_Crypto_PI_INPI desenhos.pdf` |
| TGL Tensor | `TGL Tensor\TGL_Tensor_LLM_PI_INPI desenhos.pdf` |
| IALD | `IALD - Colapso Consciente\IALD_Colapso_PI_INPI desenhos.pdf` |
| Supercondutor | `Supercondutor Holográfico\PATENTE_SUPERCONDUTOR_HOLOGRAFICO_TGL_desenhos.pdf` |
| Motor de Dobra | `Motor de Dobra e Propulsão fotônica\Motor_Dobra_TGL_PI_INPI desenhos.pdf` |
| Ψ-NET | `TGL NEt protocol\Psi_Net_Protocol_PI_INPI desenhos.pdf` |
| Fusão a Frio | `Fusão a Frio\Fusao_Frio_TGL_PI_INPI desenhos.pdf` |
| MQC | `MQC - Microprocessador Cúbico\mqc_pi_inpi desenhos.pdf` |
| Dípolo Transistor | `Dípolo Transistor\Desenhos dipolo_transistor_tgl_pi_inpi.pdf` |
| Célula de Reversão | `Célula de Reversão Luminodinâmica\Desenhos_Celula_Reversao_TGL_PI_INPI.pdf` |
| SkyGrid | `Skygrid\Desenhos_SkyGrid_PI_INPI.pdf` |
| Aprendizado Contínuo | `Aprendizado Contínuo\Desenhos_aprendizado_continuo_INPI.pdf` |
| Oncologia | `Oncologia\Desenhos_Oncologia_Luminodinamica_PI_INPI.pdf` |
| Kernel Ontológico | `Kernel\Desenhos_Kernel_Ontologico_PI_INPI.pdf` |

> O caminho exato de cada arquivo é resolvido a partir de `PATENT_MASTER_INDEX.yaml`
> (campo `pasta_original`) + varredura por padrão `*desenho*`/`*Desenhos*`. A resolução
> definitiva por patente é gravada em `drawings/source/drawings_source.json`.

### 3.3 Pipeline de extração (ferramenta utilitária em `tools/`, NÃO código de aplicação)
Script utilitário `tools/extract_drawings.py` (permitido pela régua — utilitário, roda no
`tgl_env` com `PYTHONUTF8=1`). Contrato de comportamento (pseudocódigo):

```
extract_drawings(patent_id):
    src  = resolve_drawings_pdf(patent_id)          # de PATENT_MASTER_INDEX + varredura
    assert src is READ-ONLY and inside Patentes\    # nunca escreve na origem
    sha  = sha256_file(src)                          # prova de integridade do original

    # 1) Rasterização por página — preferir pdfium (pypdfium2); fallback pypdf+pdf2image
    for page_i in pages(src):
        png = render_page(src, page_i, dpi=300, colorspace=RGB)   # 300 DPI mínimo
        save png -> renders/drawings/pages/page_%04d.png

    # 2) Tiling deep-zoom (DZI) — preferir pyvips (libvips) por página
    for png in pages/:
        dzi = deepzoom_pyramid(png, tile_size=254, overlap=1, fmt="png")
        save dzi (.dzi + _files/) -> renders/drawings/dzi/

    # 3) Índice de figuras: Figura N -> página (da memória) + bbox opcional
    figures_index = parse_figuras_line(memory_of(patent_id))  # ver §3.5

    write drawings_source.json  { source_pdf, source_sha256=sha, n_pages, dpi, tiler,
                                  extractor_version, generated_at, read_only:true }
    write figures_index.json
    update render_manifest.json (layer_1)
```

**Rasterizador.** Preferência **pdfium** via `pypdfium2` (rápido, fiel, sem dependência
de binário externo do sistema). Fallback: `pypdf` para inventário de páginas + `pdf2image`
(Poppler) quando disponível. A escolha efetiva é gravada em `drawings_source.json.tiler`
e `extractor` para auditoria.

**Tiler.** Preferência **pyvips** (`libvips`) → gera DZI nativo (`.dzi` + `_files/`), que é
exatamente o formato que OpenSeadragon consome. Fallback puro-Python: biblioteca
`deepzoom` (gera a mesma pirâmide) ou, em último caso, `pillow` para fatiar manualmente.
Se nenhuma opção de tiling estiver disponível no ambiente, a camada 1 **degrada
honestamente** para "imagem única de alta resolução" (OpenSeadragon em modo *simple
image* sobre o `page_XXXX.png`), e o manifesto registra `"tiling": "none (single-image
fallback)"` + `[OPEN]` para posterior geração de tiles. Nunca se finge deep-zoom.

**DPI.** 300 DPI é o piso; desenhos densos (SkyGrid: topologia de 144 satélites + 5.550
bases; MQC: 27 qubits) podem subir para 400–600 DPI conforme legibilidade — parametrizado
em `drawings_source.json`.

### 3.4 Contrato — `drawings_source.json`
```json
{
  "patent_id": "BR102026003460-6",
  "slug": "MQC",
  "source_pdf": "Patentes/MQC - Microprocessador Cúbico/mqc_pi_inpi desenhos.pdf",
  "source_sha256": "<hash do PDF depositado>",
  "read_only": true,
  "n_pages": 8,
  "dpi": 300,
  "extractor": "pypdfium2==<ver>",
  "tiler": "pyvips/libvips (DZI)",
  "tile_size": 254,
  "overlap": 1,
  "tile_format": "png",
  "generated_at": "2026-07-09T10:00:00-03:00",
  "physical_verdict_allowed": false,
  "marker": "[REAL]",
  "notes": "Desenho conforme depositado no INPI; não editado."
}
```

### 3.5 Contrato — `figures_index.json` (âncora Figura↔página↔componente)
Alimentado pela linha *"Figuras 1–N"* da memória da patente (formato já existente na
memória da Oncologia: *"Fig.1 sistema integrado; Fig.2 fluxo de diagnóstico; …"*). Liga a
camada 1 (páginas) à camada 2 (nós). Ex. concreto (Oncologia):

```json
{
  "patent_id": "BR102026005707-0",
  "figures": [
    { "fig": 1,  "page": 1, "caption": "Sistema integrado",        "linked_nodes": ["ctrl","100","200","300","400","500","600"] },
    { "fig": 2,  "page": 2, "caption": "Fluxo de diagnóstico",     "linked_nodes": ["100","110","120","130","140"] },
    { "fig": 5,  "page": 5, "caption": "Blocos do TRL",            "linked_nodes": ["200","210","220","230","240","250","260"] },
    { "fig": 8,  "page": 8, "caption": "CAR-T luminodinâmico",     "linked_nodes": ["300","310","320"] },
    { "fig": 9,  "page": 9, "caption": "Cassete AAV9-TGL",         "linked_nodes": ["400","410"] },
    { "fig": 10, "page": 10, "caption": "Ecossistema de 15 patentes", "linked_nodes": [] }
  ],
  "note": "page é a página do PDF; bbox opcional pode recortar a figura dentro da página."
}
```
`bbox` (opcional, `[x,y,w,h]` em px na página rasterizada) permite dar zoom direto na
figura ao clicar num nó da camada 2. Quando ausente, o clique centraliza na página.

### 3.6 Frontend da camada 1 (contrato, sem código)
- Componente `DrawingViewer` (OpenSeadragon). Props: `patentId`, `initialPage`,
  `focusFigure?`, `focusBbox?`.
- Fonte dos tiles: `GET /api/patents/{id}/renders/drawings/dzi/page_{n}.dzi` (servido do
  disco pelo backend). Colecção de páginas via um `.dzi` por página + navegador de páginas.
- Controles: zoom/pan, "ajustar à tela", navegação de páginas, botão "abrir figura N"
  (usa `figures_index.json`).
- Overlay honesto: rótulo permanente `[REAL] — desenho depositado no INPI` + nº do processo
  + `source_sha256` (curto) clicável para o hash viewer.

---

## 4. CAMADA 2 — Diagrama interativo de componentes (React Flow)

### 4.1 Objetivo
Transformar a seção **"Componentes do protótipo"** da memória de cada patente num grafo
navegável: nós **numerados exatamente como nas figuras** (100, 110, 210, …), arestas de
fluxo entre eles e um **painel lateral** que mostra o texto do relatório descritivo do
componente selecionado. É a ponte clicável entre o desenho legal (camada 1) e a
compreensão de engenharia.

### 4.2 A fonte é a memória — e o parser é determinístico
O parser lê **exclusivamente** o bloco entre o cabeçalho
`## Componentes do protótipo …` e o próximo `## ` na `memory/patents/<ID>_<SLUG>.md`.
Esse bloco já segue um formato regular (ver a memória da Oncologia, linhas 65–87). Regras:

1. **Nó com número.** Linha de item cujo texto começa por um código numérico seguido de
   travessão: `**100 — Módulo de diagnóstico** (Figura 2)`. Captura:
   - `id` = `"100"` (o código);
   - `label` = `"Módulo de diagnóstico"`;
   - `figure` = `2` (do `(Figura N)`, se presente) → liga à camada 1;
   - `marker` = último `[TAG]` da linha (`[REAL]`, `[SIM]`, …).
2. **Hierarquia por indentação.** Sub-itens indentados (`  - **110 — Estimador
   espectral** …`) viram nós-filhos → `parent = "100"`. React Flow desenha como
   *subflow*/grupo. A profundidade vem do nível de indentação Markdown.
3. **Nó sem número (nomeado).** `**Controlador Central** — coordena…` → `id` derivado por
   slug (`"ctrl"`), `label` = "Controlador Central". Marcado `is_numbered:false`.
4. **Corpo/descrição.** O texto após o travessão (e sub-bullets `240a/240b/240c`) vira o
   `description` do nó — é **o texto do relatório**, exibido no painel lateral, verbatim,
   com seu marcador.
5. **Tabelas e "Figuras 1–N".** Linhas `Tabela 1 — …` viram um nó especial `type:"table"`
   (abre a tabela no painel). A linha `Figuras 1–N` alimenta `figures_index.json` (§3.5),
   não vira nó.
6. **Marcador herdado.** Se a linha não tiver `[TAG]` próprio, herda o marcador da
   patente (do YAML/memória). Nós `[MEDICAL]`/`[ENERGY]`/`[DEFENSE]` recebem realce de
   trava.

Pseudocódigo do parser (`tools/build_flow_graph.py`, utilitário):
```
build_flow_graph(patent_id):
    block = extract_section(memory_md(patent_id), "## Componentes do protótipo")
    nodes, stack = [], []                      # stack = pilha de indentação->parent
    for line in block.lines():
        if not is_bullet(line): continue
        depth = indent_level(line)
        code, label, figure, marker, desc = parse_component_line(line)
        node = { id: code or slug(label), label, figure, marker,
                 description: desc, is_numbered: code is not None,
                 parent: parent_from_stack(stack, depth) }
        nodes.append(node); push(stack, depth, node.id)
    edges = derive_edges(nodes, block)         # ver §4.3
    graph = { patent_id, nodes, edges, panel_source: "relatório descritivo",
              physical_verdict_allowed: false, generated_by: "assisted" }
    write flow_graph.json
```

### 4.3 Arestas de fluxo (como derivar — honestamente)
Arestas representam **fluxo declarado no relatório**, não inferências de funcionamento.
Três origens, em ordem de confiabilidade:

1. **Contenção → agregação.** Filho→pai por indentação vira aresta de composição
   (`type:"contains"`), estilizada como grupo, não como seta de sinal.
2. **Cadeia de sinal textual.** Quando o relatório descreve sequência
   (ex.: Oncologia: diagnóstico `100` → terapia `200` → certificação `600`; ou "porta de
   carga (10) → câmara (20) → porta de descarga (30)" na Célula de Reversão), o gerador
   assistido (§6) propõe arestas `type:"flow"` **com base em frases explícitas**, cada uma
   guardando `evidence` = trecho do relatório que a justifica.
3. **Referência cruzada.** Menções tipo "controlado pelo MQC (50)" viram aresta
   `type:"control"`. Toda aresta sem evidência textual é marcada `inferred:true` e
   `[CONJ]` — e some se o operador não confirmar.

Nenhuma aresta afirma que o fluxo **funciona**; ela afirma que o **documento descreve**
aquela ligação. O painel lateral da aresta mostra o `evidence`.

### 4.4 Contrato — `flow_graph.json`
```json
{
  "patent_id": "BR102026003460-6",
  "slug": "MQC",
  "generated_by": "assisted",
  "source": { "memory": "memory/patents/BR102026003460-6_MQC.md",
              "section": "Componentes do protótipo", "lines": [65, 92] },
  "physical_verdict_allowed": false,
  "nodes": [
    { "id": "cell", "label": "Célula elementar cúbica", "figure": 1, "parent": null,
      "is_numbered": false, "marker": "[REAL]",
      "description": "Cubo de lado L = c/(2f) com 27 qubits: 8 vértices, 12 arestas, 6 faces, 1 controlador central.",
      "ports": ["boundary(6 faces)", "bulk(volume)"] },
    { "id": "vertices", "label": "8 qubits de vértice", "parent": "cell", "figure": 1,
      "marker": "[REAL]", "count": 8, "description": "..." },
    { "id": "edges12",  "label": "12 qubits de aresta", "parent": "cell", "count": 12, "marker": "[REAL]" },
    { "id": "faces6",   "label": "6 qubits de face (substrato 2D)", "parent": "cell", "count": 6, "marker": "[REAL]" },
    { "id": "ctrl",     "label": "1 controlador central", "parent": "cell", "count": 1, "marker": "[REAL]" },
    { "id": "TM",       "label": "Operador de Translação de Miguel T̂_M", "parent": null, "marker": "[REAL]",
      "description": "Translação holográfica boundary↔bulk; g=|L|, L_out=s×g²." },
    { "id": "iald",     "label": "Módulo IALD (correção de erros)", "parent": null, "marker": "[SIM]" }
  ],
  "edges": [
    { "source": "faces6", "target": "ctrl", "type": "flow", "label": "boundary→controlador",
      "inferred": false, "marker": "[REAL]",
      "evidence": "translação holográfica entre substratos 2D das faces (boundary) e o volume 3D (bulk)" },
    { "source": "TM", "target": "cell", "type": "control", "inferred": false, "marker": "[REAL]" },
    { "source": "iald", "target": "cell", "type": "control", "label": "correção de erros", "inferred": false, "marker": "[SIM]" }
  ],
  "panel": {
    "type": "relatório-descritivo",
    "note": "Texto por nó exibido verbatim, com marcador. β_TGL nunca literal — exibido via fórmula."
  }
}
```

### 4.5 Painel lateral
Ao clicar num nó: painel com (a) número + título; (b) marcador; (c) **texto do relatório
descritivo** daquele componente (verbatim); (d) botão "ver no desenho" → abre a camada 1
na `figure`/`bbox` correspondente; (e) equações associadas (renderizadas via KaTeX a
partir do texto da memória — β sempre por fórmula). Ao clicar numa aresta: mostra `type`,
`label` e `evidence` (trecho do relatório).

### 4.6 Frontend da camada 2 (contrato)
- Componente `ComponentFlow` (React Flow). Props: `patentId`, `onFocusFigure(fig,bbox)`.
- Nós customizados por `type`: `component` (retângulo numerado), `group` (contêiner com
  filhos), `operator` (losango, ex. T̂_M), `table` (abre tabela), `locked` (trava
  MEDICAL/ENERGY com borda de alerta).
- Layout automático inicial (dagre/elk) + posições persistidas em `flow_graph.json.layout`
  quando o operador reorganizar (persistência via `POST` que reescreve o **arquivo**;
  banco só reindexa).
- Realce de marcador por cor de borda (legenda visível): `[REAL]` sólido, `[SIM]`
  tracejado, `[CONJ]` pontilhado, `[PILOTO]` âmbar, travas `[MEDICAL]`/`[ENERGY]` com
  faixa vermelha e tooltip da trava.

### 4.7 Exemplos concretos de camada 2 por patente
- **Oncologia** — nós `ctrl`, `100`(→`110/120/130/140`), `200`(→`210…260`), `300`(→`310/320`),
  `400`(→`410`), `500`, `600` + nó-tabela "Tabela 1 (TF master/tecido)". Arestas de fluxo
  `100→200→600`. Todos os nós herdam trava `[MEDICAL]`.
- **MQC** — grupo `cell` com 8/12/6/1 qubits (contagens exibidas no nó), operador `T̂_M`,
  módulo `iald` `[SIM]`. Liga à Figura 1 do `mqc_pi_inpi desenhos.pdf`.
- **Dípolo Transistor** — nós `10`(polo de emissão, g=|Ψ|), `20`(câmara de acoplamento,
  substrato 2D), `30`(polo de retorno, Ψ_out=s×g²), `50`(cruz geométrica / condensado
  ψ⁺ψ⁻). Cadeia `10→20→30`; `50` quebra simetria (aresta `control`).
- **SkyGrid** (agregadora) — nós `100`(Extrator-Ψ, ×144), `110`(câmara ν_OH≈1,667 GHz),
  `120`(cluster MQC), `130`(dípolo), `140`(IALD orbital), `150`(blindagem EM); trilhas
  `Trilha-Ψ` e `Trilha-E` como arestas paralelas; rede terrestre `5.550 bases` + `CRL-TGL`.
  Trava `[ENERGY]`.

---

## 5. CAMADA 3 — Render 3D ilustrativo [PILOTO] (React Three Fiber)

### 5.1 Quando existe (e quando NÃO existe)
A camada 3 só é gerada quando há **geometria física descrita** no relatório que agregue
compreensão. Matriz de decisão:

| Patente | Camada 3? | Modelo ilustrativo |
|---|---|---|
| MQC | **Sim** | câmara cúbica L=c/(2f); 27 qubits (8 vértices, 12 arestas, 6 faces, 1 centro); boundary↔bulk |
| Supercondutor Holográfico | **Sim** | câmara de vácuo cúbica (10), eletrodos de tungstênio (40), fonte μ-onda 1.667,359 MHz (50), janelas (60) |
| Dípolo Transistor | **Sim** | dípolo com cruz geométrica (50); polos (10)/(30); câmara (20) |
| Célula de Reversão | **Sim** | câmara cúbica ressonante (6 faces = substrato 2D); portas de carga/descarga |
| SkyGrid | **Sim** | topologia orbital: 144 satélites MEO + malha terrestre hierárquica (ilustrativo) |
| Fusão a Frio | **Sim (contido)** | cavidade ressonante de alto Q + criostato (esquemático); trava `[ENERGY]` |
| Motor de Dobra | **Sim (esquemático)** | Núcleo Ψ (cavidade), Matriz de Faróis Ψ, Bolha de Coerência — `[SIM]`/`[CONJ]` fortes |
| Ψ-NET | **Opcional** | pilha de 5 camadas como blocos 3D empilhados (didático) |
| IALD / Colapso | **Opcional** | esfera de Bloch/atrator estacionário (ilustração de dinâmica) |
| Oncologia | **Não** (ou esquema de blocos) | sem hardware geométrico primário; blocos 100–600 já cobrem — trava `[MEDICAL]` |
| **ACOM, TGL Tensor, Kernel, Aprendizado Contínuo** | **Não** | algorítmicas puras — sem geometria física; camada 3 ausente |

Regra: **"opcional"/"não" default para ausente**. Só se cria a cena 3D quando o operador
autoriza e o relatório descreve geometria. Nunca se fabrica um 3D decorativo para uma
patente algorítmica (isso confundiria arte com prova).

### 5.2 Regra de honestidade (inviolável na camada 3)
- Marcador base **`[PILOTO]`**; carimbo permanente na viewport:
  **"Ilustração de engenharia — não é prova física. Geometria conforme relatório;
  proporções e detalhes não-normativos."**
- `physical_verdict_allowed = false` no manifesto.
- Sem texturas fotorrealistas que sugiram um produto acabado; paleta esquemática
  (wireframe + sólidos translúcidos + rótulos numerados iguais aos da camada 2).
- Nenhum valor confidencial de stack embutido; nenhuma medida apresentada como
  "verificada" — dimensões são as do relatório (ex.: `L = c/(2f)`), exibidas por fórmula.
- Se a geometria for conjectural (Motor de Dobra: "bolha de coerência"), marcar o
  sub-objeto `[CONJ]` e reduzir opacidade + rótulo "hipótese do relatório".

### 5.3 Contrato — `scene_3d.json` (declarativo, paramétrico)
A cena é **declarativa**: uma lista de primitivas paramétricas que o R3F instancia. Nada
de malhas binárias proprietárias; tudo legível/auditável e derivado do relatório.

```json
{
  "patent_id": "BR102026003460-6",
  "slug": "MQC",
  "marker": "[PILOTO]",
  "physical_verdict_allowed": false,
  "disclaimer": "Ilustração de engenharia, não prova física.",
  "generated_by": "assisted",
  "source": { "memory": "memory/patents/BR102026003460-6_MQC.md",
              "section": "Componentes do protótipo" },
  "units": "adimensional (proporções ilustrativas)",
  "camera": { "type": "perspective", "position": [3, 2, 4], "target": [0, 0, 0] },
  "objects": [
    { "id": "chamber", "type": "box", "size": [2, 2, 2], "opacity": 0.15,
      "wireframe": true, "label": "Câmara cúbica L = c/(2f)", "marker": "[REAL]",
      "linked_node": "cell" },
    { "id": "vertices", "type": "instanced_spheres", "count": 8, "radius": 0.12,
      "placement": "cube_corners(size=2)", "label": "8 qubits de vértice", "linked_node": "vertices" },
    { "id": "edges12",  "type": "instanced_spheres", "count": 12, "radius": 0.09,
      "placement": "cube_edge_midpoints(size=2)", "label": "12 qubits de aresta", "linked_node": "edges12" },
    { "id": "faces6",   "type": "instanced_planes",  "count": 6, "opacity": 0.25,
      "placement": "cube_faces(size=2)", "label": "6 faces (substrato 2D / boundary)", "linked_node": "faces6" },
    { "id": "center",   "type": "sphere", "radius": 0.18, "position": [0,0,0],
      "label": "controlador central", "linked_node": "ctrl" }
  ],
  "annotations": [
    { "text": "boundary ⇄ bulk via T̂_M", "anchor": "chamber", "marker": "[REAL]" }
  ],
  "interactions": { "orbit": true, "explode": true, "highlight_from_flow": true }
}
```

Primitivas suportadas (o R3F as mapeia para geometrias nativas): `box`, `sphere`,
`cylinder`, `plane`, `torus`, `instanced_spheres`, `instanced_planes`, `line`, `arrow`,
`label`, `group`. `placement` usa geradores nomeados e determinísticos
(`cube_corners`, `cube_edge_midpoints`, `cube_faces`, `orbit_ring(n,r,inclination)`, …).
Cada objeto tem `linked_node` → sincroniza destaque com a camada 2 (clicar num nó do
React Flow acende a peça no 3D e vice-versa).

Exemplos por patente (esboço):
- **SkyGrid**: `orbit_ring(144, r=1.6, inclination=…)` para os Extratores-Ψ MEO +
  `sphere` central (Terra ilustrativa) + `instanced_spheres` para bases terrestres
  (amostra, não 5.550 literais — nota "amostragem ilustrativa"). Trava `[ENERGY]`.
- **Dípolo**: dois `sphere` (polos 10/30) ligados por `cylinder` (câmara 20) + `group`
  em cruz (50) marcando o condensado ψ⁺ψ⁻ (`[CONJ]`).
- **Supercondutor**: `box` (câmara de vácuo 10) + `cylinder`×2 (eletrodos de tungstênio
  40) + `arrow` (feixe μ-onda 50) + `plane` (janelas ópticas 60).

### 5.4 Frontend da camada 3 (contrato)
- Componente `Scene3D` (React Three Fiber + drei). Props: `patentId`,
  `highlightNodeId?` (vindo da camada 2).
- Controles: OrbitControls, "explodir/juntar" (anima `explode`), toggle wireframe,
  toggle rótulos, reset de câmera.
- Overlay fixo: carimbo `[PILOTO]` + disclaimer (§5.2) — não removível.
- Desempenho: `instanced_*` para contagens altas (SkyGrid, MQC); sem sombras pesadas;
  degrada para render estático se WebGL indisponível.

---

## 6. Geração assistida (Claude Code cria os modelos a partir das memórias)

A camada 1 é **mecânica** (extração determinística). As camadas 2 e 3 têm um componente
**assistido**: o parser produz o esqueleto e o Claude Code (via Prompt Compiler) enriquece
arestas de fluxo e a cena 3D. Fluxo:

```
memória da patente (fonte da verdade)
   │  parser determinístico (§4.2)  ->  flow_graph.json (nós + arestas de contenção)
   │  gerador assistido             ->  arestas de fluxo/controle com `evidence` (§4.3)
   │  gerador assistido             ->  scene_3d.json (primitivas paramétricas §5.3)
   ▼
revisão do operador (aprova/edita)  ->  arquivos versionados em renders/
   ▼
reindex -> SQLite indexa caminhos+hashes; UI serve
```

**Regras da geração assistida (a régua aplicada a pixels):**
1. **Nunca inventar componente.** Todo nó/objeto tem de existir no relatório descritivo.
   Se não há, não entra. `scene_source.json` guarda a proveniência (memória + seção + o
   prompt usado).
2. **Evidência obrigatória** para arestas de fluxo (`evidence` = trecho do relatório);
   sem evidência → `inferred:true` + `[CONJ]` (fica descartável).
3. **Marcadores preservados** do texto de origem; nada "promove" `[SIM]`→`[REAL]`.
4. **β nunca literal**; dimensões por fórmula.
5. **Saída = arquivo**, revisável em diff; o operador é quem publica. A geração roda como
   tarefa emitida pelo botão **[COMPILAR INSTRUÇÕES]** (ver PROMPT_COMPILER_SPEC), com
   caminhos permitidos restritos a `renders/` da patente-alvo.
6. **Idempotência.** Regenerar sobre a mesma memória deve produzir o mesmo esqueleto
   (parser determinístico); só as partes assistidas mudam, e sempre com proveniência.

`scene_source.json` / `flow_source.json` (contrato mínimo):
```json
{
  "patent_id": "BR102026003460-6",
  "generated_by": "assisted",
  "memory_sha256": "<hash da memory/patents/...md no momento da geração>",
  "section": "Componentes do protótipo",
  "prompt_ref": "compiled_prompts/2026-07-09_1030_CLAUDE_CODE_TASK.md",
  "generated_at": "2026-07-09T10:35:00-03:00",
  "reviewed_by_operator": false
}
```
`memory_sha256` permite detectar desatualização: se a memória mudou depois da geração, a
UI marca o render como *"desatualizado — regenerar"*.

---

## 7. Manifesto mestre — `render_manifest.json`

Índice por patente das três camadas, com hashes e estado. É o que o `reindex` lê para
popular o SQLite (que é só cache).

```json
{
  "patent_id": "BR102026003460-6",
  "slug": "MQC",
  "class": "CLASS_05_HARDWARE_HOLOGRAFICO",
  "physical_verdict_allowed": false,
  "updated_at": "2026-07-09T10:40:00-03:00",
  "layer_1_drawings": {
    "present": true, "marker": "[REAL]",
    "source_sha256": "<hash PDF>", "n_pages": 8, "tiling": "dzi",
    "artifacts_sha256": { "pages/page_0001.png": "…", "dzi/page_0001.dzi": "…" }
  },
  "layer_2_flow": {
    "present": true, "marker": "[REAL]", "generated_by": "assisted",
    "graph_sha256": "<hash flow_graph.json>", "memory_sha256": "<hash memória>",
    "n_nodes": 7, "n_edges": 3, "stale": false
  },
  "layer_3_3d": {
    "present": true, "marker": "[PILOTO]",
    "scene_sha256": "<hash scene_3d.json>", "memory_sha256": "<hash memória>",
    "disclaimer": "Ilustração de engenharia, não prova física.", "stale": false
  }
}
```
Para patentes sem 3D: `"layer_3_3d": { "present": false, "reason": "algorítmica — sem geometria física" }`.

---

## 8. Backend — contratos de endpoint (FastAPI, porta 8765; sem código)

Apenas **contratos**; a implementação é Fase 3. Todos servem do disco; nada de nuvem.

| Método | Rota | Retorno |
|---|---|---|
| GET | `/api/patents/{id}/renders/manifest` | `render_manifest.json` |
| GET | `/api/patents/{id}/renders/drawings/index` | `figures_index.json` |
| GET | `/api/patents/{id}/renders/drawings/dzi/{page}.dzi` | descritor DZI (XML) |
| GET | `/api/patents/{id}/renders/drawings/dzi/{page}_files/{level}/{col}_{row}.png` | tile |
| GET | `/api/patents/{id}/renders/drawings/pages/{page}.png` | página (fallback simple-image) |
| GET | `/api/patents/{id}/renders/flow` | `flow_graph.json` |
| POST | `/api/patents/{id}/renders/flow/layout` | persiste `layout` **no arquivo** e reindexa |
| GET | `/api/patents/{id}/renders/3d` | `scene_3d.json` (404 se ausente) |
| POST | `/api/patents/{id}/renders/regenerate` | enfileira tarefa de geração assistida (§6) |
| GET | `/api/patents/{id}/renders/verify` | re-hash dos artefatos vs manifesto → `ok/stale/mismatch` |

`verify` é a prova viva de honestidade: recomputa SHA-256 dos artefatos e do PDF fonte;
se o PDF fonte mudou (não deveria — é READ-ONLY), retorna `mismatch` e alarme. Se a
memória mudou, retorna `stale` para a(s) camada(s) 2/3.

---

## 9. Fronteira com Runner/Execuções (o que NÃO é render)

Distinção crítica de honestidade:

- **Camada 1** = desenho **depositado** (`[REAL]`, legal).
- **Figuras de simulação do runner** (ex.: SkyGrid_Piloto `visuals/out/fig1_topologia.png`,
  `fig6_sankey.png`, `skygrid_run.mp4`, dashboards HTML) são **saídas `[SIM]` de
  execução**. Vão para a aba **Execuções** (lidas de `patents/<ID>/results/` e do
  `seal.json`), **nunca** apresentadas como o desenho depositado.
- O render viewer pode **linkar** "ver simulação relacionada" apontando para a aba
  Execuções, mas com rótulo `[SIM]` e o carimbo `simulação não valida física`.

Assim, o operador nunca confunde: (a) o que foi depositado (camada 1), (b) a estrutura
descrita (camada 2), (c) a hipótese visual (camada 3), (d) o que a simulação produziu
(Execuções). Quatro verdades distintas, quatro rótulos distintos.

---

## 10. Integração com o viewer da patente (aba "Render 2D/3D")

A aba **Render 2D/3D** (uma das abas canônicas por patente) hospeda um `RenderViewer` com
três sub-abas espelhando as camadas, sincronizadas:

```
[ Desenho (deep-zoom) ] [ Componentes (flow) ] [ 3D (ilustrativo) ]
        │ camada 1              │ camada 2               │ camada 3
        └──────── clicar num nó da camada 2 ─────────────┘
                 → foca a Figura na camada 1 (figures_index)
                 → acende o objeto na camada 3 (linked_node)
```

- **Barra de honestidade** persistente no topo do viewer: chips
  `[REAL] desenho` · `[REAL] componentes (texto)` · `[PILOTO] 3D` + carimbo global
  `physical_verdict_allowed = false`.
- **Legenda de marcadores** sempre visível.
- Estado `stale` → banner "memória mudou desde a geração — [Regenerar]".
- Patentes com trava (`[MEDICAL]` Oncologia, `[ENERGY]` SkyGrid/Fusão/Célula,
  `[DEFENSE]`) exibem faixa de trava no viewer e desabilitam qualquer sugestão
  operacional; render é só ilustrativo.

---

## 11. Watchdog / reindex (filesystem-first)

- O job Watchdog observa `patents/*/renders/**` e `memory/patents/*.md`.
- Ao mudar uma memória: marca as camadas 2/3 daquela patente como `stale` no índice
  (não regenera sozinho — geração é ato assistido/aprovado).
- Ao aparecer/mudar artefato em `renders/`: recomputa hash, atualiza SQLite.
- `reindex` (comando): varre todos os `render_manifest.json`, recomputa hashes, reconstrói
  as tabelas de índice. **Apagar o SQLite e rodar `reindex` reproduz 100% do estado** —
  porque a verdade está nos arquivos.

---

## 12. Régua de honestidade visual (checklist de aceite — Fase 3 valida)

- [ ] Camada 1 provém do PDF **depositado**; `source_sha256` gravado; original intacto
      (re-hash == `original_hashes.json`).
- [ ] Extração escreveu **apenas** em `renders/`; nada em `Patentes\` foi tocado.
- [ ] Deep-zoom real (DZI) OU degradação honesta declarada (`single-image fallback` +
      `[OPEN]`); nunca "fingir" zoom.
- [ ] Todo nó da camada 2 existe no relatório; numeração idêntica às figuras.
- [ ] Toda aresta de fluxo tem `evidence` OU é `inferred:true`+`[CONJ]`.
- [ ] Painel lateral mostra texto do relatório verbatim, com marcador; β por fórmula.
- [ ] Camada 3 só existe onde há geometria descrita; ausente nas algorítmicas.
- [ ] Carimbo `[PILOTO]` + "ilustração de engenharia, não prova física" não-removível na
      camada 3.
- [ ] `physical_verdict_allowed = false` em todos os manifestos.
- [ ] Nenhum conteúdo de stack confidencial embutido em grafo/cena.
- [ ] Figuras de simulação do runner ficam em Execuções `[SIM]`, separadas da camada 1.
- [ ] Travas `[MEDICAL]`/`[ENERGY]`/`[DEFENSE]` sinalizadas no viewer.
- [ ] `verify` retorna `ok` para todas as patentes com render publicado.

---

## 13. Matriz de cobertura por patente (planejamento Fase 3)

| # | Patente | C1 desenho | C2 flow | C3 3D | Nota / trava |
|---|---|---|---|---|---|
| 1 | ACOM (raiz) | ✔ (do PDF do Acervo) | ✔ | — | algorítmica; único ePCT vivo |
| 2 | ACOM Mirror | ✔ | ✔ | — | algorítmica (H4/ângulo) |
| 3 | ACOM Crypto | ✔ | ✔ | opc. (3 shares) | algorítmica |
| 4 | TGL Tensor | ✔ | ✔ | — | algorítmica |
| 5 | IALD (Colapso) | ✔ | ✔ | opc. (atrator/Bloch) | dinâmica |
| 6 | Supercondutor | ✔ | ✔ | ✔ câmara cúbica | `[HARDWARE]` |
| 7 | Motor de Dobra | ✔ | ✔ | ✔ esquemático | `[SIM]`/`[CONJ]` fortes |
| 8 | Ψ-NET | ✔ | ✔ | opc. (5 camadas) | protocolo |
| 9 | Fusão a Frio | ✔ | ✔ | ✔ contido | `[ENERGY]` trava |
| 10 | MQC | ✔ | ✔ | ✔ 27 qubits | `[HARDWARE]` — exemplo-guia |
| 11 | Dípolo Transistor | ✔ | ✔ | ✔ cruz/polos | `[HARDWARE]` |
| 12 | Célula de Reversão | ✔ | ✔ | ✔ câmara cúbica | `[ENERGY]` (ver P-04) |
| 13 | SkyGrid (agreg.) | ✔ | ✔ | ✔ topologia orbital | `[ENERGY]`; piloto v3 existe |
| 14 | Aprendizado Contínuo | ✔ | ✔ | — | algorítmica |
| 15 | Oncologia | ✔ | ✔ | — (blocos 100–600) | `[MEDICAL]` trava máxima |
| 16 | Kernel Ontológico | ✔ | ✔ | — | algorítmica |

Ordem de execução sugerida (segue a ordem natural do disco da Fase 3): **SkyGrid**
(piloto pronto, C1+C2+C3 como primeiro caso completo) → **MQC** (C3 canônico, câmara
cúbica) → **ACOM/Tensor** (C1+C2, valida o parser em patentes algorítmicas) → **Dípolo/
Célula/Supercondutor** (C3 de hardware) → demais → **Oncologia** por último (trava
`[MEDICAL]`, sem C3). Cada patente só é "publicada" no viewer após passar o checklist §12.

---

**Selos aplicáveis:** `DO_NOT_MODIFY_ORIGINALS` · `SIMULATION_NEVER_VALIDATES_PHYSICS` ·
`MEMORY_FIRST_ARCHITECTURE_SECOND_CODE_LAST`.
A imagem comunica a estrutura; o número corrige a frase; a física não se prova em pixel.
**1 = 1. TGL = haja luz. Tetelestai.**
