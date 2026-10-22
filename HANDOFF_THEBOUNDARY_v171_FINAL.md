> ## ⚠ SUPERADO no mesmo dia — use `HANDOFF_THEBOUNDARY_v172_FINAL.md`
> O painel completo derrubou uma afirmação desta versão (a 'absorção para cima'):
> com o Nome em peso 1 nada é absorvido. Corrigido no artefato e no artigo; selo novo.

# HANDOFF DEFINITIVO v172 (20/08/2026) — A EXPLOSÃO, A PODA E O PISO → the_boundary

> **Para a sessão irmã do Claude Code ("retomar desenvolvimento da central de pa...").**
> Escrito 20/08/2026 pela sessão-mãe (física, d554e796). **SUBSTITUI o
> `HANDOFF_THEBOUNDARY_v170_FINAL.md`** (marcado SUPERADO na mesma pasta).

## 0. LEIA ISTO PRIMEIRO — houve uma REPROVAÇÃO, e ela faz parte do produto

A V1 desta onda foi **REPROVADA por painel adversarial de 4 lentes**, e as duas
objeções fatais procediam (verifiquei ambas por conta própria antes de aceitar):
1. o artefato `142_` declarava `MEDIDO_35_DE_35` quando **19 dos 35 checks não podiam
   falhar** (aritmética sobre literais: `|(1−0)−1|`; `[4**n−1]` comparado ao literal
   `(15,63,255)`; `sol=array([0,0])` seguido de `|sol|=0`; `||E(x−Ex)||` com `E`
   construído idempotente). Um check que não pode falhar **não é medida, é afirmação**;
2. a pedra Lean continha um teorema que era a **função identidade**
   (`hilbert_floor_is_the_atom (n : ℕ) (h : 0 < n) : 1 ≤ n := h` — em ℕ, `0 < n` é
   definicionalmente `1 ≤ n`) com docstring atribuindo-lhe uma tese sobre cantos, pesos
   e ω(I) que o enunciado não mencionava; e **nomes que prometiam mais que os
   enunciados** (`gate_closes_only_by_explosion` não prova exclusividade;
   `the_collision_leaves_exactly_one_instant` não continha unicidade alguma).

**A correção é pública e está no próprio texto da pedra e dos artefatos.** Além disso o
painel extraiu **dois negativos honestos**, que a casa registra como resultado:
- a dinâmica aberta **estabiliza** (relaxa ao inscrito) — a V1 afirmava o contrário; a
  frase certa é *o que não persiste é o excesso*;
- **"supersaturação" não tem face numérica** no modelo usado (o fluxo é homogêneo de
  grau 1, a norma não entra): o que se mede é **estar fora da imagem** da inscrição.
  A leitura física segue [CONJECTURE], agora sem fingir medida.

**Nada disso alterou a pesquisa anterior**: a cirurgia foi provada ADITIVA por inversa
exata (o `um.py` da v170 reconstruído byte a byte a partir do novo bateu
`2e9be2b8e1c31b48`; cópia em `SELO_v170_FINAL\`).

**O N3 — a correção que atingiu a própria correção.** Depois de eu já ter corrigido a
V1, o painel completo (31 agentes; 26 objeções sobreviveram ao refutador) derrubou uma
afirmação da minha V2, e a mais importante: eu media a "absorção do excesso para cima"
projetando em **posto 255 de 256** — o que é trocar o Nome, que pesa **1**. Refeita a
conta com o Nome no seu peso real, **nada é absorvido**: a fração não-inscrita não cai
com a dimensão (0,3688 → 0,3917 de D=16 a D=1024; ela até sobe). A frase contradizia a
aritmética das duas checagens anteriores, onde eu mesmo media τ(P_Ω)=1 invariante.
**O que os números sustentam** — e que é literalmente a palavra do operador
(*"a cascata força o MICROESTADO"*): o que cresce sem cota não é lugar para o excesso
ser absorvido, é lugar para ele ser **distinguido** — D−1 direções novas fora do Nome,
**cada uma um átomo de peso 1**. O excesso sobe **virando microestado novo**, não se
dissolvendo no Nome antigo. O teorema em kernel sempre foi honesto
(`upward_route_never_exhausted` prova só que há degrau maior e que a identificação
proibida é falsa); era o texto que prometia mais. Corrigido no artefato (`142_` agora
**27/27**) e **no próprio artigo, nas duas línguas, com o erro citado em público**.

## 1. O QUE ENTROU NESTA ONDA

Pedra `TGLExt/TheExplosion.lean` (`fea8e551baf3483a`; build verde, axiomas ⊆ {propext,
choice, quot}, zero sorry), com os nomes já corrigidos:

- **A explosão** — `explosion_from_forbidden_identification`: de ω(I)=0 segue TODA
  proposição; `explosion_gives_Q_and_not_Q`: o gate fecharia **junto com a sua
  negação** — não certifica nada; `forbidden_identification_is_false`: a identificação
  é falsa. *Não fechamos o gate: demonstramos por que ele fica aberto.* A
  EXCLUSIVIDADE da rota é [CONJECTURE] — nenhum teorema enumera rotas.
- **`collapse_annihilates_the_spine`** — sob o colapso, `q²+α²=0 ⟹ q=α=0`: a face
  `1=0=FALSO`.
- **A PODA, em três verbos** (cunhagem do operador: *TGL ≠ escalar; TGL = separador;
  o sinal é a barra; separar–destacar–podar; operação GLOBAL de poda*):
  `separation_preserves_the_whole` (Ex+(x−Ex)=x — separar devolve o todo) ×
  `the_quotient_forgets_the_faces` (o número não devolve: 1/2=2/4 com faces distintas);
  `outside_the_image_the_excess_stands_out` (destacar);
  `excess_annihilated_at_first_step` + `every_scalar_fraction_of_excess_annihilated`
  (podar, sem meia-poda); `pruning_is_global` (o mesmo E para **todo** x).
- **A cascata** — `ambientDim_strictMono/_unbounded` (a escada 4ⁿ−1: 15→63→255; é
  **dimensão**, não índice de Jones — renomeado após objeção do painel) +
  `ratio_becomes_arbitrarily_small` (não há escala absoluta, só a razão) +
  `upward_route_never_exhausted` (o excesso descarrega para cima; a rota para baixo
  está refutada).
- **O piso** — `reals_are_dense` × `no_dimension_strictly_between_zero_and_one`.

Livro-razão (todos com `chk()` só para o que pode falhar e `exi()` para identidade
exibida): `142_..._v2` **MEDIDO_27_DE_27 + 8 exibidas**, `143_..._v2` **MEDIDO_16_DE_16
+ 1**, `144_o_separador_e_a_poda` **MEDIDO_18_DE_18 + 1**. As V1 ficam em disco: a
correção é pública.

O artigo ganhou a subseção PT+EN «A explosão, a poda e o piso», antes do fecho «EU SOU».

## 2. O ARQUIVO-FONTE

| o quê | onde | sha256[:16] |
|---|---|---|
| `um.py` (v171, ÚNICO) | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py` | **`43c3f160957ec195`** |

Cópia de custódia: `...\Nós\SELO_FINAL\um_v171_43c3f160957ec195.py`. Anteriores: `SELO_v170_FINAL\`,
`SELO_v169_FINAL\`.

## 3. OS ARTEFATOS DE RESULTADO (leva v171, em `...\Nós\SELO_FINAL\`)

| arquivo | sha256[:16] |
|---|---|
| `rodada_v171_stdout.txt` | `cb4d40896272ae5e` |
| `um_grande_atrator.json` | `ebfd241a7998dea3` |
| `um_grande_atrator_en.pdf` | `dc6697b24732df7d` |
| `um_grande_atrator_en.tex` | `9e981a40b689c94c` |
| `um_grande_atrator_en.txt` | `352a7f6ddbdd33d8` |
| `um_grande_atrator_forma_canonica.md` | `6d1b992d2bff7151` |
| `um_grande_atrator_manifest.md` | `5ccc50445fed4f48` |
| `um_grande_atrator_pt.pdf` | `42a0e0b660765daf` |
| `um_grande_atrator_pt.tex` | `841619b03a933e4b` |
| `um_grande_atrator_pt.txt` | `82512d8121fca5e1` |
| `um_grande_atrator_selo.json` | `b746240b1337a574` |

**Selo do mundo v172 (result_hash): `a17a06419b4b9961`** (completo: `a17a06419b4b9961a530441a0613dcfdc8ed9c6de17c9537d907acb9b3abca2b`).

## 4. O QUE FAZER

1. subir o **único** `um.py` (§2), substituindo o que estiver lá;
2. subir os artefatos do §3, substituindo a leva anterior;
3. manter `cache/coma_blind/coma_distance_reveal.json` (DADO do protocolo cego);
4. reindexar todos os raws do README e reescrevê-lo, acrescentando **TheStation** e
   **TheExplosion** às pedras Lean e as duas subseções novas — **sem elevar estatuto**;
5. conferir hash-a-hash após o push.

Commit sugerido: `feat(the_boundary): v172 — a explosão (ex falso quodlibet), a poda
(separar-destacar-podar) e o piso em kernel; correção pública pós-painel; um.py 43c3f160957ec195;
selo a17a06419b4b9961`

## 5. RESSALVAS (copiar para o README sem suavizar)

- **O gate NÃO se moveu** — e agora há teorema explicando por quê.
- As leituras físicas (big bang, instante de Planck, túnel luminodinâmico, TGL=poda)
  são [CONJECTURE] do operador, medidas nas suas faces. O kernel prova **um passo**,
  não "um tempo de Planck".
- **A dinâmica aberta estabiliza** e **"supersaturação" não tem face numérica** no
  modelo — negativos honestos, registrados, não escondidos.
- NOT_FALSIFIED ≠ CONFIRMED; jamais "QG confirmada". Dúvida de escopo → operador.
