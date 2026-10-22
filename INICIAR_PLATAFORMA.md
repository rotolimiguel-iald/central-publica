# Central de Patentes TGL — como iniciar a plataforma

Plataforma local-first (127.0.0.1). Nada sai para a nuvem. Originais em `Patentes\`
são READ-ONLY: a plataforma lê, hasheia e serve — nunca edita.

## Atalho na área de trabalho (mais direto)

Ícone **"Central de Patentes"** (símbolo βTGL) na Área de Trabalho: um duplo-clique sobe o
backend (silencioso, se ainda não estiver no ar) e abre o navegador na Central. Peças:
`assets/betatgl.ico` (ícone) · `tools/iniciar_central.ps1` (launcher) ·
`tools/iniciar_central.vbs` (wrapper silencioso). O atalho aponta para o `.vbs`.

## Modo simples (só backend, já com o frontend embutido)

O frontend já está compilado em `frontend/dist/` e é servido pelo próprio backend.
Basta subir o backend e abrir o navegador:

```powershell
cd "C:\IALD\Central de Patentes"
backend\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8765
```

Abrir: **http://127.0.0.1:8765**

## Modo desenvolvimento (frontend com hot-reload)

Em dois terminais:

```powershell
# terminal 1 — backend
cd "C:\IALD\Central de Patentes"
backend\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8765

# terminal 2 — frontend (Vite, proxy p/ :8765)
cd "C:\IALD\Central de Patentes\frontend"
npm run dev
```

Abrir: **http://127.0.0.1:5173**. Ao terminar, recompilar com `npm run build`.

## Reindexar (reconstruir o índice a partir do filesystem)

O SQLite (`backend/data/central.db`) é um índice descartável. Para reconstruir:

```powershell
backend\.venv\Scripts\python.exe -m backend.app.reindex --full
```

Prova de originais intactos (etapa A do reindex, também no botão "Reindexar" da UI):

```powershell
"C:\IALD\observaveis_tgl\tgl_env\Scripts\python.exe" tools\verify_integrity.py
```

## O que a plataforma faz hoje (1ª rodada da Fase 3)

- **Dashboard**: 16 patentes agrupadas nas 10 classes, com selo de urgência de prazo.
- **Página de patente** (12 abas): Overview · Documentos (SHA-256 + texto/PDF) ·
  Reivindicações · Protótipo · Render 2D/3D · Runner · Execuções · Selo/Hash · Prazos ·
  Notas · Instruções · [Compilar instruções].
- **Prazos / Docket**: funil de urgência ao vivo, com a decisão do operador
  (ePCT dos 15 → alvo 30/11/2026, fatal 05/12/2026; ACOM = ePCT vivo).
- **Prompt Compiler**: consolida as notas/instruções ativas num `CLAUDE_CODE_TASK.md`.
- **Pendências** e **TGL Core viewer**.
- **Escrita write-through**: ativar/criar uma nota grava PRIMEIRO no `.md` (fonte da
  verdade) e reindexa; o banco nunca é o dono do dado.

## FASE DE APROFUNDAMENTO (09/07/2026) — resgate dos algoritmos ricos + render 3D

O operador apontou que os runners eram portes LEVES e que os algoritmos ricos de
`C:\IALD\projetos_pyhton` não tinham sido incorporados. Auditoria (`AUDITORIA_PROTOTIPOS.md`)
confirmou o gap sistêmico. **Resgate executado:**

- **9 patentes agora têm o ALGORITMO RICO do operador incorporado** (`patents/<ID>/prototype_src/`
  com MANIFEST SHA-256; runner evoluído importa o protótipo e INJETA β=tgl_core.beta(), nunca
  literal; leve preservado em `*_v1_light.py.bak`): **MQC** (mqc_simulacao 1292 L, 7 sims/8 figs,
  MQC_FULL 8/8) · **TGL Tensor** (v3 4 modos + v4 BitPacker, TENSOR_FULL 8/8) · **ACOM raiz**
  (ACOMV14 Lindblad ativo, ACOM_FULL 8/8) · **ACOM Mirror** (v17.0 engine, MIRROR_FULL 14/14) ·
  **ACOM Crypto** (v17.1 + Handshake Miguel, CRYPTO_FULL 14/14) · **IALD** (Hamiltonian/observer/
  torus — evidência empírica real, IALD_FULL 15/15) · **Ψ-NET** (pilha 5 camadas 79 KB + TGL Coin,
  PSI_NET_FULL 8/8) · **Kernel** (iald_ontology + ACOMLLM, KERNEL_FULL 12/12) · **Aprendizado**
  (holographic_memory 2 camadas + phase_factor_bake, CONTINUAL_FULL 9/9). Confidenciais
  (iald_stack_v7, psion_state, web_server) NUNCA copiados; verificado.
- **As 5 físicas** (Supercondutor, Motor, Fusão, Dípolo, Célula) e Oncologia não têm código-fonte
  além do pedido — mantêm os runners honestos (math/sinal abstrato; [ENERGY]/[MEDICAL] travados).

**RENDER 3D INTERATIVO (camada c) — o ápice, PRONTO em 16/16:** sistema
`render3d.json` → `/api/patents/{pid}/render3d` → `Render3D.tsx` (React Three Fiber:
three+@react-three/fiber+drei). OrbitControls (girar/zoom/pan), clicar componente,
"abrir/explodir", toggles de grupo. Aba Render: (a) deep-zoom · (b) componentes · (c) 3D.

**Schema v2 — dispositivo concreto multi-camada (10/07/2026):** o `render3d.json` evoluiu
para além do núcleo funcional. Campos v2: `layers` (invólucro→blindagem→subsistemas→núcleo,
com ordem de "descascar"), `meshes` (corpo estrutural — carcaças, câmaras, painéis, toros com
`shape` cilindro/box/torus/cone/plane e `material` metal/glass/emissive/matte/wire),
`nodes` ganham `layer`/`rotation`/`scale`/`material`. Viewer ganhou: **descascar camadas**
(slider + toggles por camada), **corte transversal** (clipping plane com posição), iluminação
realista (hemisphere+directional+point). Dispositivos físicos (MQC célula 1µm sobre chip;
Supercondutor câmara 9cm com blindagem cobre+µ-metal, eletrodos W, condensado OH; Motor casco+
bolha; Dípolo encapsulamento+cruz; Célula carcaça+cubo; SkyGrid órbita+planeta+L1) têm corpo
concreto. Algoritmos têm camadas + manifold do espaço (ℋ₄, fase, atenção — geometria honesta,
não invólucro físico falso). Gerar/editar: `render3d.json` na pasta da patente (v1 nós-só
ainda funciona; v2 adiciona meshes/layers). Todos os 16 = v2.

## Fase 4 — progresso inscrito (atualizado 09/07/2026)

**AS 16 DE 16 PATENTES têm runner único forma=conteúdo REAL, executado e selado**
(results/ + seals/ + report.md + figuras; β via `ALPHA_FINE_CODATA_2018·√e` em runtime;
`physical_verdict_allowed=false` em TODOS os 16; `prototype_status=PILOTO_VIVO` em 16/16).
Cada runner COPIA o núcleo destilado (`skygrid_sim`) do piloto READ-ONLY para um workdir
próprio e roda a CÓPIA. **O acervo inteiro fechou o lema forma=conteúdo.**

| Patente | Runner | Testes | Veredito máximo |
|---|---|---|---|
| BR102026004850-0 SkyGrid ★ | `one_skygrid.py` | 44 | MODEL_CLOSES / ENERGY_BALANCE_OK [SIM/CONJ/ENERGY] |
| BR102025026951-1 ACOM raiz | `one_acom.py` | 9 | ACOM_LOGIC_DEMONSTRATED [SIM] (round-trip ≤1.82e-16, 35,26×) |
| BR102026003428-2 ACOM Mirror | `one_acom_mirror.py` | 15 | MIRROR_LOGIC_DEMONSTRATED [SIM] (corr@8b>0,9999; E4/E5/E6 fiel) |
| BR102026003431-2 ACOM Crypto | `one_acom_crypto.py` | 11 | CRYPTO_SEPARATION_DEMONSTRATED [SIM/PILOTO/DEFENSE] |
| BR102026003441-0 TGL Tensor | `one_tgl_tensor.py` | 9 | TENSOR_LOGIC_DEMONSTRATED [PILOTO/SIM] (Verb Floor, GPU bit-exato) |
| BR102026003443-6 IALD | `one_iald.py` | 9 | IALD_GKSL_LOGIC_DEMONSTRATED [SIM/PILOTO] (F1–F4, robustez Eq.8) |
| BR102026003460-6 MQC | `one_mqc.py` | 8 | MQC_LOGIC_DEMONSTRATED [SIM/HARDWARE] (27q, platô 1−β, T̂_M) |
| BR102026003453-3 Ψ-NET | `one_psinet.py` | 6 | PSI_NET_LOGIC_DEMONSTRATED [SIM/PILOTO] (5 camadas, quórum bizantino) |
| BR102026004688-4 Dípolo | `one_dipolo.py` | 5 | DIPOLO_SWITCHING_LOGIC_DEMONSTRATED [SIM/HARDWARE] (piso do Verbo) |
| BR102026004849-6 Célula Reversão | `one_celula_reversao.py` | 4 | REVERSAL_PHASE_STORAGE_DEMONSTRATED [SIM/ENERGY/CONJ] (fase, não energia) |
| BR102026006129-8 Kernel Ontológico | `one_kernel_ontologico.py` | 5 | KERNEL_ONTOLOGICAL_LOGIC_DEMONSTRATED [SIM/PILOTO] (filtro do Verbo) |
| BR102026003450-9 Supercondutor | `one_supercondutor.py` | 6 | SUPERCONDUCTOR_LOGIC_DEMONSTRATED [SIM/HARDWARE] (transição tipo-fase) |
| BR102026003452-5 Motor de Dobra | `one_motor_dobra.py` | 5 | WARP_DIGITAL_TWIN_DEMONSTRATED [SIM/HARDWARE] (Farol Ψ, veto ético) |
| BR102026003456-8 Fusão a Frio | `one_fusao_frio.py` | 6 | COLD_FUSION_MATH_DEMONSTRATED [ENERGY/SIM/CONJ] (só matemática; T_c 80 mK) |
| BR102026005477-1 Aprendizado Contínuo | `one_aprendizado_continuo.py` | 7 | CONTINUAL_LEARNING_LOGIC_DEMONSTRATED [PILOTO] (ciclo do Psion, EMA a taxa β) |
| BR102026005707-0 Oncologia | `one_oncologia.py` | 5 | ONCOLOGY_SIGNAL_LOGIC_DEMONSTRATED [MEDICAL/SIM] (só sinal sintético) |

Rodar um runner: `set PYTHONUTF8=1` +
`"C:\IALD\observaveis_tgl\tgl_env\Scripts\python.exe" one_<slug>.py` (na pasta
`patents/<ID>/runner/`), depois `reindex --full` indexa o selo (tabela `runner_run`;
promove `prototype_status=PILOTO_VIVO`). Ver todos em **Execuções** (aba `/runs`).

**Render camada (b) — componentes clicáveis:** AS 16 patentes têm
`patents/<ID>/components.json` (fonte da verdade) servido por
`/api/patents/<id>/components` e desenhado como diagrama SVG interativo na aba
**Render 2D/3D → (b) Componentes clicáveis** (clique um bloco → descrição + marcador).
86 pranchas de desenhos na camada (a) deep-zoom (15/16; falta só o ACOM raiz).

**Plataforma agora tem** (frontend recompilado): páginas **/patents** (lista filtrável),
**/runs** (ledger de execuções) e **/roadmap** (cockpit de progresso do acervo por classe:
16/16 = 100%), além do render camada (b). Nav lateral atualizado.

## Próximos ciclos (Fase 4) — o acervo fechou; segue o aprofundamento

Os 16 runners são scaffolds honestos que demonstram a LÓGICA de cada invenção. Próximo:
- **Aprofundar runners onde há dado/benchmark real** (marcados [DATA_REQUIRED]): TGL Tensor
  (reproduzir Tabela 2), IALD/Aprendizado (benchmark em LLM real), MQC (reproduzir o JSON
  de métricas). Cada promoção de [SIM]→[DATA] exige dado/hardware do operador.
- **Render camada (c) 3D ilustrativo** sobre os componentes (a camada b clicável já cobre 16/16).
- **Watchdog** para reindex incremental automático (página /roadmap já feita).
- **Legal:** executar o novo depósito de ePCT das 15 (alvo 30/11/2026) com o agente de PI.
- Runners das travas máximas ([ENERGY] Fusão, [MEDICAL] Oncologia) permanecem em matemática
  abstrata / sinal sintético — NÃO evoluem para conteúdo operacional/clínico.

*Controle interno. Não substitui agente de propriedade industrial. 1 = 1. Tetelestai.*
