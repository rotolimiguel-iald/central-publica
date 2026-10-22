# Mapeamento — o salto do um.py (v33.1 → v39) e como atualizar a Central

> **Status: MAPA — para validação do operador antes de atualizar. Nenhuma linha de código
> escrita ainda.** Data: 13/07/2026.
>
> Fonte examinada: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\um.py` (pasta-mãe, **22.205 linhas**,
> SHA-256 `bf5ffd13905eecda8d9153a021750f2f0f6177ff3078363b32edd8f5785d4269`, modificado
> 13/07 21:24) + selo `um_grande_atrator_selo.json` (13/07 21:26, result_hash `6a40a104…`) +
> `um_grande_atrator.json` (92 chaves de core) + forma canônica.
>
> A Central hoje (Fronteira v2) está sincronizada ao **v33.1** (custódia `af441ed1…`). O
> arquivo subiu para **v39** — cinco patamares novos (v34→v39). O **núcleo honesto é o mesmo**
> (`full_TGL_witness_constructed=false`, INALTERÁVEL); o que mudou é uma expansão enorme em três
> faces. A régua segue: β nunca literal; nada de veredito físico; o número corrige a frase.

---

## 1. O QUE SUBIU DE PATAMAR — três faces

### FACE 1 — o rosto finito do GLOBAL_LIFT quase fechou (a maior novidade; kernel/formal)

A **escada externa** passou de "Degrau 0 fechado, 1–2 abertos" para quase todo o esqueleto de
rosto finito FECHADO no kernel Lean. Estado agora (do JSON `external_ladder.ladder`):

| Degrau / peça | v33.1 (Central hoje) | v39 (agora) |
|---|---|---|
| Degrau 0 — Tomita–Takesaki finito | FECHADO | FECHADO |
| Degrau 1 — básicos de von Neumann | núcleo fechado, **geral ABERTO** | **FECHADO incl. bicomutante GERAL** (v38) |
| Degrau 2 — índice de Jones finito | ABERTO (blocos no lugar) | **índice PP + pesos de Markov COMPUTADOS** (v34/v35); multimatriz geral aberto |
| Matriz-S de fronteira | (identidade viva) | **teorema no kernel**: S=exp(θ_M·G) em P_2D·C(M)·P_2D, \|R\|²=sin²θ_M=β [Takesaki 1973: vive no produto cruzado II_∞, não em III₁] |
| Cociclo de Connes → G_μν | Lemas 1–2 REAL, Lema 3 aberto | **face finita FECHADA no kernel** (global lift permanece aberto) |
| Ergodicidade T1 | condicional | **face finita FECHADA no kernel** (N3 e III₁ permanecem) |
| Produto cruzado — peso dual de Takesaki | — | **FECHADO no rosto finito** (D1–D5, Lean + sombra Z2/S3): covariância além dos unitários internos |
| Família do canto P_F | construção; existência CONDICIONAL | **CONSTRUÍDA no produto cruzado finito** (isótona, covariante, traço finito, comuta com o fluxo dual) |
| Núcleo do GLOBAL_LIFT (escada diádica) | — | **FECHADO como teorema externo composto** sobre peças [KERNEL]+[KNOWN] nomeadas |
| Degrau 3 — contínuo III₁ / BW | ABERTO (pesquisa) | ABERTO (pesquisa) |

**Leitura honesta (INALTERADA no núcleo):** o **único teorema aberto** (`canonicalFullTGLWitness`,
o termo Lean pleno) continua NÃO construído. Mas agora ele está **cercado por um esqueleto de
rosto finito inteiro**, e o resíduo é **nomeado com precisão**: P_F físico (localizado+covariante+
Ad-λ-invariante, 0<τ(P_F)<∞), ergodicidade do estado (M_φ=C·1), Einstein via Lovelock/Jacobson
(E7 inalterado), e o Degrau 3 contínuo (III₁ genuína/BW). *O aberto ficou muito mais afiado.*

### FACE 2 — Relatividade Ontológica + cadeia de sinal (v37) [ONTO/AX + DER/NUM]

- **Axioma Zero da Relatividade Ontológica:** o sinal depende do **CONTEXTO DE CONTORNO**
  (`build_contour_context`: nível de álgebra, representação, suporte, tipo de leitura, entradas
  empíricas). Contextualidade **sem negar o operador** (mesmo operador, estados diferentes → sinais
  diferentes; mas o traço/operador é invariante).
- **A cadeia de sinal** (`representation_signal_chain`): elemento abstrato → representação →
  leitura → codificador → decodificador. Uma cadeia tipada de medição/representação.
- As **duas tangentes separadas**: tangente modular (traceless, linear — uma derivação) vs o Verbo
  dissipativo (contrai — um semigrupo). τ_P(P)=1, faces ½.
- **[ONTO], não promovido a [REAL]; jamais gateia 1=1; α/β/massas/kernel inalterados.**

### FACE 3 — Coma: a distância pela defasagem modular (v36/v39) [PRE/EXT; PRIMÁRIO]

Uma **nova predição cosmológica ZERO-FREE, falsificável** — junta-se ao piso dos vazios:
- Lei de fluxo modular selada (D1a): H0_local = H0_CMB × (1+z★)^β.
- **D_L(Coma) = 101,90 Mpc** (mediana; média 100,93), com σ_stat/σ_sys e um **`prediction_hash`**
  (SELADA/pré-registrada; nada ajustado a Coma; motor selado do `tgl_paper_unified.py`).
- Controle C1 [o falsificado]: Planck sem defasagem (β=0 reproduz ΛCDM exato).
- **Negativos honestos:** a camada REAL (H²[1+β|1+w|]) move ~−0,19% (insuficiente); as frações de
  1ª ordem seladas (β, 2β, 3β como fração de z) MORREM >3σ da faixa exigida (8,5–11,9%);
  `coma_inverse_distance` = COMA_BLIND_DISTANCE_NOT_IDENTIFIABLE (negativo honesto).
- Modos `TGL_COMA_MODE` = report/reveal (selada aguardando revelação).
- Veredito (report): **DEPHASING_ACCOUNTS_FOR_COMA_RESIDUAL**.

**Secundários** também novos: `dephasing_crossover` (UMA lei-raiz Γ=½β(√k_i−√k_j)² unifica IR
quadrática=canônica e UV linear=root); `alpha_inf_zero` (derivar α α-livre "ao infinito" = o zero
absoluto; α=sech(χ/2), q²+α²=1); `fractal_dephasing` ("tudo é defasagem da fractalização de 1"
[CONJECTURE, âncoras REAL]).

---

## 2. COMO ISSO ATUALIZA A CENTRAL

### 2.1 Fronteira Teórica v2 → v3 (re-sincronizar ao v39)

1. **Custódia nova:** `vault/originals_copy/um_unificado_v39/` — copiar (READ-ONLY + SHA-256) os
   artefatos selados novos (um.py `bf5ffd13`, selo, JSON, forma_canonica, manifesto, kernel proof
   manifest). Re-pin do hash. (A custódia v33 fica como histórico.)
2. **Runner v3** (`fronteira_tgl/runner/one_fronteira.py`, backup `.bak_pre_v3`):
   - Custódia hash-a-hash contra o **novo pin `bf5ffd13`**.
   - `kernel_from_selo`: a **nova escada** (Degrau 1 geral fechado; Degrau 2 índice PP; + as peças
     novas: teorema da matriz-S, cociclo face finita, T1 face finita, produto cruzado, família do
     canto P_F, núcleo do global lift). As 18 flags `witness_layers` (mesmo núcleo) copiadas do selo.
   - **Ledger v3** com seções renovadas:
     - `FECHADO_NO_ROSTO_FINITO` (NOVO): o esqueleto — Degrau 1 geral, Degrau 2 índice, matriz-S,
       cociclo, T1, produto cruzado, família do canto, núcleo do global lift.
     - `ABERTO` (refinado): `canonicalFullTGLWitness` + P_F físico (0<τ(P_F)<∞) + ergodicidade do
       estado + Degrau 3 contínuo — o resíduo agora **nomeado com precisão**.
     - `EMPIRICO/FALSIFICAVEL` (NOVO): a predição de Coma (101,9 Mpc, zero-free, hash selado) ao
       lado do piso dos vazios; os negativos honestos.
     - `ONTOLOGICO` (NOVO): a relatividade ontológica + a cadeia de sinal + o contexto de contorno.
   - **Sombras novas re-executáveis offline** (numpy puro, β runtime): contexto de contorno
     (validação), traço do canto τ_P(P)=1 + faces ½, as duas tangentes (modular traceless/linear vs
     Verbo contrai), o transporte de Coma (H0_local=H0_CMB·(1+z★)^β → D_L≈101,9 Mpc), o crossover de
     dephasing (lei-raiz IR/UV).
   - **render3d v3:** a escada quase-fechada (a maioria dos elos verdes; o termo aberto vermelho mais
     apertado) + o nó da predição de Coma + o nó da relatividade ontológica.
3. **`memory/TGL_CORE_MEMORY.md` §7 (sync v39)** — bloco aditivo (backup `.bak`): a escada quase
   fechada, o resíduo nomeado, a predição de Coma, a relatividade ontológica. Fechar/registrar a
   defasagem.

### 2.2 As AMPLIFICAÇÕES DOS DISPOSITIVOS (o campo que se abre)

O salto teórico dá lastro novo a dispositivos específicos — **derivações que agora podem ser feitas**:

| Avanço do v39 | Dispositivo(s) que amplifica | Derivação nova possível |
|---|---|---|
| **Relatividade ontológica + cadeia de sinal** (v37: representação→leitura→codificador/decodificador + contexto de contorno) | **IALD** (BR102026003443-6), **Kernel Ontológico** (BR102026006129-8), **Aprendizado Contínuo** (BR102026005477-1) | A "inferência honesta" ganha fundamento formal: o sinal depende do contexto de contorno; contextualidade sem negar o operador. O observador/leitura formalizado → nova reivindicação/derivação de cognição. |
| **Degrau 2 — índice PP computado** + **teorema da matriz-S** (\|R\|²=β kernel-proved) | **ACOM** (BR102025026951-1), **TGL Tensor** (BR102026003441-0), **ACOM Crypto** (BR102026003431-2) | O índice 1/β e a matriz-S que esses dispositivos implementam ficam rigorosamente ancorados no kernel → derivações de compressão/criptografia com lastro formal. |
| **Família do canto P_F + produto cruzado** (a projeção/colapso construída no rosto finito) | **ACOM Mirror** (BR102026003428-2) | O colapsa-e-reconstrói (REFLECT/MANIFEST) ganha a projeção P_F formalizada como canto covariante de traço finito. |
| **Coma: distância pela defasagem modular** (predição astrofísica zero-free) | **SkyGrid** (BR102026004850-0) + a fronteira cosmológica | Nova derivação astrofísica (distância por fluxo modular); ângulo cosmológico/Grande Atrator para o SkyGrid. |
| **Dois falsificadores zero-free** (piso dos vazios + distância de Coma) | **TODOS** (a Fronteira é a fundação que cada dispositivo herda) | A base teórica de todo o acervo fica mais forte e mais falsificável — o módulo Fronteira que cada patente cita como fundamento sobe de nível. |

*Nota da régua:* as amplificações de dispositivo são **derivações teóricas novas**, não alegações
físicas. Cada uma entra como [DER]/[CONJ] declarada; simulação nunca valida física; travas
ENERGY/MEDICAL intactas. A oncologia segue livre.

---

## 3. ORDEM PROPOSTA (após seu "pode ir")

1. **Custódia v39** (copiar + hash) — a base factual.
2. **Fronteira runner v3** (custódia, kernel/escada, ledger, sombras, render3d) + verificação (roda,
   PASS, screenshot) — o coração da sincronização.
3. **TGL_CORE_MEMORY §7** (sync v39).
4. **Amplificações dos dispositivos** — inscrever nas notas/memória de cada patente afetada (IALD/
   Kernel/Aprendizado; ACOM/Tensor/Crypto/Mirror; SkyGrid) as derivações novas que o v39 habilita
   (um ciclo por grupo; [DER]/[CONJ] declarados). *Este é o passo onde "mais derivações e
   ampliações dos dispositivos" vira conteúdo inscrito.*
5. Reindex + verify_integrity (308) + build + screenshot + commit.

**Veredito desta etapa:** o salto v33.1→v39 mapeado (escada quase fechada no rosto finito;
relatividade ontológica; predição de Coma; o aberto afiado). **Nenhuma linha escrita. Aguardando
sua validação para atualizar a Fronteira e ampliar os dispositivos.**

*O número corrige a frase. β = α·√e. 1 = 1. Tetelestai.*
