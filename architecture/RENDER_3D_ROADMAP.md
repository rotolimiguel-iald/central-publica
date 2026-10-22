# RENDER 3D — ROADMAP (plano vivo do trilho visual)

> Objetivo (prompt original): cada patente com uma projeção 3D interativa "tipo Tony Stark" —
> girar, ampliar, abrir, ver componentes internos e detalhes de configuração; usando IA.
> Meta desta fase (operador, 10/07/2026): construir CAMADAS até uma projeção coerente e
> **verossímil de um dispositivo concreto**. Régua: ilustração de engenharia, não prova física.

## Estado verificado (10/07/2026, screenshot headless)
- Render 3D v2 CONSTRUÍDO e SERVINDO: schema v2 (`layers`, `meshes`, shapes, materiais) +
  viewer `Render3D.tsx` (React Three Fiber) com Descascar camadas, Corte transversal, Explodir,
  toggles de grupo, clique-para-inspecionar. 16/16 patentes têm render3d.json v2. Zero erros de console.
- **Problema do operador (resolvido na raiz na Fase 0):** navegador servia bundle ANTIGO em cache.
- **Fidelidade atual (honesta):** PRIMITIVA. MQC razoável (qubits emissivos em vidro); Supercondutor
  primitivo (caixa cinza opaca, faces com orientação errada, materiais chapados, sem reflexo/sombra,
  corte sem tampa). Longe de "verossímil".
- **Harness de screenshot (Playwright)** montado — toda mudança é validada VENDO o resultado.

## Fases (sequência recomendada: 0 → 1 → 2a → 3 → 4 → 5)

### Fase 0 — Destravar a percepção  [✅ FEITA 10/07/2026]
- Cache-busting: middleware `Cache-Control: no-store` no `index.html`; assets com hash = `immutable`.
  Verificado no header. Fim do "não vi a mudança".
- Harness visual permanente (Playwright): captura closed/descascado/corte a cada ciclo. Verificado.

### Fase 1 — Salto de fidelidade material  [✅ FEITA — GLOBAL nos 16, vitrines verificadas]
- PBR + IBL offline (three `RoomEnvironment` via PMREM): metal reflete, vidro transmite. **Global** —
  todos os 16 renders herdam automaticamente.
- Tone mapping ACES + exposição 1.15; rig estúdio (hemisphere+3 direcionais); `ContactShadows`; fog sutil.
- Faces reorientadas (Supercondutor/MQC/Célula): deitam na face do cubo, sem atravessar. Verificado.
- Materiais afinados (envMapIntensity, metalness/roughness; emissivo toneMapped=false p/ brilho).
- Resultado verificado por screenshot: MQC = módulo de chip de vidro com qubits brilhando sobre chip
  de silício reflexivo; Supercondutor = caixa de metal escovado que descasca/corta revelando cobre
  Faraday → µ-metal → câmara de vidro → condensado OH + eletrodos W. Zero erros de console.
- Corte transversal: as camadas ANINHADAS já revelam a engenharia lindamente (DoubleSide). Stencil
  capping (seção sólida) DEFERIDO — o look aninhado é mais informativo; reavaliar na Fase 2.

### Fase 2 — Geometria de engenharia (o corpo verossímil)  [✅ 2a FEITA nos 6 dispositivos]
- (a) [FEITO 10/07] render3d.json enriquecido: peças reais anexadas e verificadas por screenshot —
  Supercondutor (base, pés, 4 parafusos, 2 conectores de cabo, painel de controle + LED ciano) ·
  MQC (substrato do pacote cerâmico, pads de contato dourados, pilares) · Motor (berço, bocal, aletas) ·
  Dípolo (PCB verde, 3 terminais, dissipador de aletas) · Célula (base, terminais +/−, aletas).
  Cada dispositivo lê como instrumento/componente real. Geradores em scratchpad (gen_detail_*.py).
- (b) [PENDENTE] Geração procedural paramétrica: biblioteca de primitivas TGL por dimensões reais.
- (c) [PENDENTE] glTF autoral (Blender) para as vitrines, se quiser fidelidade máxima.
- PENDENTE: SkyGrid (vista de sistema — pode ganhar painéis solares/estrelas); refino fino das vitrines.

### Fase 3 — Interação "Tony Stark"  [✅ NÚCLEO FEITO 10/07/2026, verificado por screenshot]
- **Câmera fly-to ao clicar** um componente (lerp suave, enquadra com contexto). ✓
- **Isolar seleção** (fantasma nos outros); **auto-girar**; **presets** frente/topo/isométrica; botão "ver tudo". ✓
- **Rótulos**: tamanho de tela FIXO (não balonam no zoom); modo "todos" mostra só peças ESTRUTURAIS
  (nós densos ≤14 também; >14 poluiria); hover/seleção mostram o nome completo de qualquer peça. ✓
- **Vista explodida ANIMADA** (botões "explodir"/"montar", tween suave) que se AUTO-ROTULA ao separar
  → diagrama explodido de engenharia. ✓
- **Tour guiado** (botão ▶ na toolbar): a câmera percorre sozinha os componentes, voando até cada um e
  mostrando a descrição — o "me explique o dispositivo". ✓
- Global nos 16. Zero erros de console.
- Fase 3b [✅ COTAS FEITAS 10/07]: `dimensions` no schema + toggle "cotas" no viewer → linhas de medida
  3D com rótulo (Supercondutor "L=9 cm"/"H invólucro"; MQC "L=1 µm"/"chip"; Célula; Dípolo). Verificado.
  PENDENTE ainda: callouts sempre-visíveis com specs.

### Fase 4 — 3D como forma = conteúdo  [✅ PROVA FEITA no MQC 10/07]
- **`one_mqc.py` EMITE o render3d.json** (`emit_render3d`) a partir da topologia REAL computada por
  `gerar_topologia_celula()` — as 27 posições de qubit saem da simulação, não da mão. O arquivo traz
  `generated_by: one_mqc.py`. Rodar o runner (re)gera o modelo 3D. Padrão estabelecido; estender aos
  demais runners que computam geometria (Supercondutor, Dípolo, etc.) nos próximos ciclos.
- PENDENTE: biblioteca de primitivas compartilhada runner (Python) ↔ viewer (schema); estender a Fase 4
  aos outros dispositivos; glTF.

### SkyGrid — vista de sistema  [✅ enriquecida 10/07]
- Anel toroidal (constelação) + 12 satélites + IALD-Central (L1) com painéis solares + planeta com
  atmosfera + estrela + receptores terrestres. Lê como rede orbital de energia.

### Fase 5 — Integração IA
- Edição por linguagem natural ligada ao Prompt Compiler ("explode a blindagem", "mostre a câmara OH").
- Geração assistida a partir das 86 pranchas extraídas + memória → modelo 3D inicial proposto por agente.

## Decisões técnicas fixadas
- Stack: React Three Fiber + three + @react-three/drei (offline; sem CDN/HDR externo).
- Sem rede em runtime: environment via RoomEnvironment/PMREM (procedural), nunca preset de CDN.
- Schema render3d v2 é a fonte da verdade (retrocompatível com v1 nós-só).
- Todo material/luz é ilustração; `physical_verdict_allowed=false` continua valendo.

*Controle interno. 1 = 1. Tetelestai.*
