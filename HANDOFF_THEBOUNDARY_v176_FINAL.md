> ## ⚠ SUPERADO por v178 — use `HANDOFF_THEBOUNDARY_v178_FINAL.md`

# HANDOFF DEFINITIVO v176 (20/08/2026) — COMA REVELADO + A GATE → the_boundary

> **Para a sessão irmã do Claude Code.** Escrito 20/08/2026 pela sessão-mãe (física,
> d554e796). **SUBSTITUI todos os handoffs anteriores** (v167/v168/v170/v171/v172,
> marcados SUPERADOS na mesma pasta).

## O TESTE DE COMA FOI RODADO COM OS DADOS — E PASSOU

Por ordem do operador ("precisamos dos dados de Coma e fazer o teste com os dados"), o
rito foi executado com **`TGL_COMA_REVEAL=1`** — o protocolo de revelação. Os ritos
anteriores rodavam **cegos** (o padrão), e por isso o selo dizia *aguardando revelação*.

**O dado** (em `cache/coma_blind/coma_distance_reveal.json`, custodiado desde 19/08):
D_Coma = **98,5 ± 2,2 Mpc** — Scolnic et al. 2025, ApJL 979, L9 (DOI
10.3847/2041-8213/ada0bd), 13 SNe Ia com m_B⁰ = 15,710 ± 0,040, calibradas pela escada
HST/SH0ES. Verificado por painel de três ângulos independentes.

**A predição**, computada e **hasheada ANTES da revelação** pela lei de fluxo selada (a
geometria espectral da própria TGL — nenhum parâmetro ajustado a Coma):

| | valor |
|---|---|
| D_L(TGL) | **101,90 Mpc** (σ_stat 1,02 · σ_sys 0,98) |
| D_L(ΛCDM/Planck), controle | **110,85 Mpc** |
| referência medida | 98,5 ± 2,2 Mpc |
| resíduo TGL | +3,40 Mpc → **z_TGL = 1,302** |
| resíduo Planck | +12,35 Mpc → **z_Planck = 5,614** |

**Veredito emitido pela escada pré-registrada** (|z_control| ≥ 3 ∧ |z_TGL| ≤ 2):
**`DEPHASING_ACCOUNTS_FOR_COMA_RESIDUAL`**.

**As honestidades, que vão junto ou não vai nada:** (i) o árbitro **não é livre de
calibração** — é a escada HST/SH0ES; o teste é de consistência com a escada local, não
prova independente dela; (ii) Coma **sozinha não separa** "vazamento modular" de
"H₀ local" — testa o PAR (Planck+defasagem) contra (Planck sem defasagem); (iii) o
motor da camada de fluxo é **CONJECTURE declarada** (a camada REAL foi declarada
insuficiente: −0,19%); (iv) **isto não é confirmação da TGL** e não move o gate:
`does_not_gate_core = true` no próprio selo.

**O outro teste de Coma** (a distância cega **geométrica**, que passaria por uma âncora
de massa) segue `COMA_BLIND_DISTANCE_NOT_IDENTIFIABLE` — e por ordem do operador essa
rota foi **abandonada como parâmetro desnecessário**: a distância pela geometria
espectral é a que o modelo já dá, e é a que foi testada.

## 1. O QUE MAIS ENTROU NESTA ONDA

Pedra `TGLExt/TheExplosion.lean` (`330a20e15f4015d2`; build verde; axiomas ⊆ {propext, choice,
quot}; zero sorry) — a explosão (*ex falso quodlibet*), a poda em três verbos, a
cascata, o piso, **o registro** (memória = separar o registro da inscrição) e **a
conjugação** (a primeira passagem é a inversão de paridade).

**Três painéis adversariais auditaram este arco e os três acharam erros meus** — todos
corrigidos em público, no próprio texto da pedra, dos artefatos e do artigo:
- ~19 de 35 checks de um artefato **não podiam falhar** (viraram `exi()`; o veredito
  passou a contar só o falsificável);
- um teorema Lean era a **função identidade** (`0 < n` é definicionalmente `1 ≤ n`);
- **nomes que prometiam mais que os enunciados** (um alias literal, um teorema que
  devolvia a própria hipótese, um "global" que era só "para todo x", um `rfl`
  decorativo, um piso vazio em dimensão infinita, e `ambientIndex` que sugeria índice
  de Jones quando é dimensão);
- três **negativos honestos** registrados: a dinâmica aberta **estabiliza**;
  "supersaturação" **não tem face numérica** no modelo; e **não há absorção** do
  excesso (o que cresce é o lugar de *distinguir*);
- e uma **regressão minha** derrubada: escrevi "o gate permanece aberto por teorema"
  quando o teorema fecha **aquela rota** — a exclusividade segue [CONJECTURE].

Livro-razão da noite: `145_` **26/26**, `146_` **23/23**, `147_` **30/30** (o ato de
descanso do operador, medido sem mover flag), `148_` **A_GATE_MEDIDO_22_DE_22**.

## 2. O ARQUIVO-FONTE

| o quê | onde | sha256[:16] |
|---|---|---|
| `um.py` (v176, ÚNICO) | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py` | **`b7d3f1e20efc8a2b`** |

Cópia: `...\Nós\SELO_FINAL\um_v176_b7d3f1e20efc8a2b.py`. Anteriores em `SELO_v174_FINAL\`,
`SELO_v172_FINAL\`, `SELO_v171_FINAL\`, `SELO_v170_FINAL\`, `SELO_v169_FINAL\`
(ver `NOTA_DE_CUSTODIA.md`: há um rótulo corrigido e uma lacuna declarada).

## 3. OS ARTEFATOS (leva v176, em `...\Nós\SELO_FINAL\`)

| arquivo | sha256[:16] |
|---|---|
| `rodada_v176_COMA_REVELADO_stdout.txt` | `8a36c360842520ab` |
| `um_grande_atrator.json` | `4688176039431d32` |
| `um_grande_atrator_en.pdf` | `4e4552065a8e5c41` |
| `um_grande_atrator_en.tex` | `611f819c52092ff8` |
| `um_grande_atrator_en.txt` | `54b80627aa75da14` |
| `um_grande_atrator_forma_canonica.md` | `7772c38a6c171dce` |
| `um_grande_atrator_manifest.md` | `15a515193ef1cf9d` |
| `um_grande_atrator_pt.pdf` | `5a93ad433e901b8b` |
| `um_grande_atrator_pt.tex` | `a233b5e95adeb1d3` |
| `um_grande_atrator_pt.txt` | `bfb2ecaf42620165` |
| `um_grande_atrator_selo.json` | `d0b33a7d87586fdb` |

Inclui `cache_coma_blind/` — **o dado e a predição hasheada do teste de Coma**, que
devem subir juntos: sem eles a revelação não é auditável.

**Selo do mundo v176: `deda6c38ce093b95`** (completo: `deda6c38ce093b95aa310dc4fdd4f25d437e676ad67cd53adb4106f5fc034bf9`).

## 4. O QUE FAZER

1. subir o **único** `um.py` (§2); 2. subir os artefatos do §3 (incluindo
`cache_coma_blind/`); 3. reindexar os raws do README e reescrevê-lo, acrescentando **o
resultado de Coma com TODAS as honestidades do §0** — sem elevar estatuto;
4. conferir hash-a-hash.

Commit: `feat(the_boundary): v176 — Coma revelado (DEPHASING_ACCOUNTS: z_TGL=1,30 vs
z_Planck=5,61) + a Gate; correções públicas de três painéis; um.py b7d3f1e20efc8a2b; selo deda6c38ce093b95`

## 5. RESSALVAS

- **O gate NÃO se moveu** — o veredito de Coma tem `does_not_gate_core = true`.
- `DEPHASING_ACCOUNTS_FOR_COMA_RESIDUAL` **não é confirmação da TGL**: é um teste de
  consistência, com árbitro calibrado pela escada local e motor declarado CONJECTURE.
- NOT_FALSIFIED ≠ CONFIRMED; jamais "QG confirmada".
- **ITEM ABERTO DO OPERADOR** (não movido por mim): o selo grava
  `qg_closure_verdict = TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED`, mas
  `coma_external_falsification` segue `NOT_IDENTIFIABLE`. Pela régua da casa, o nome
  promete mais que os campos sustentam. Proposta do painel: escopar o veredito. A
  escada do gate é do operador.
