> ## ⚠ SUPERADO por v179 — use `HANDOFF_THEBOUNDARY_v179_FINAL.md`
> (o nome do veredito foi ESCOPADO; a escada nao se moveu)

# HANDOFF DEFINITIVO v178 (20/08/2026) — A DOBRA, O REGISTRO E O OBSERVADOR

> **Para a sessão irmã do Claude Code.** Escrito 20/08/2026 pela sessão-mãe (física,
> d554e796). **SUBSTITUI todos os anteriores**, inclusive o v176.

## O QUE ENTROU (a última onda de 20/08)

**Três pedras novas em kernel**, todas verdes, sem avisos próprios, axiomas ⊆ {propext,
choice, quot} — o kernel embutido passou de 166 para **169 arquivos**:

- `TGLExt/TheBandNet.lean` (`ce91de5490bcdb40`) — **as caudas são totalmente ordenadas**
  (`tails_are_totally_ordered`): não há par independente ali, e por isso uma obrigação de
  localidade seria VAZIA — não por falta de campo no tipo, mas por falta de objetos
  disjuntos. E as **bandas** de intervalos disjuntos são **ortogonais**
  (`bandSub_orthogonal`): a independência espectral, com o par independente exibido
  (`adjacent_bands_disjoint`, sem depender de axioma algum).
- `TGLExt/TheFold.lean` (`e4546410da663f73`) — **o contador de cortes é invisível ao habitante**
  (`the_cut_count_is_invisible`), com testemunha não-nula explícita
  (`the_fold_has_witnesses`), enquanto **os espaços se distinguem**
  (`the_index_does_distinguish_the_spaces`): a perda é do lado do habitante, não da
  família. E `the_fold_the_two_faces`: a cauda é submódulo (aspecto) **e** o seu contador
  é invisível (natureza). *A sobra veste a totalidade.*
- `TGLExt/TheRecordOfTheCut.lean` (`dfcdd551fd1b04fb`) — **o registro cresce enquanto o resíduo
  encolhe**; encontram-se só no zero e são ortogonais; **um passo no índice é um passo de
  poda com a direção exibida** (`each_step_removes_exactly_one_witnessed`);
  **`⋂ₙ Tₙ = ⊥`** — cortar não revela núcleo escondido; e **`the_identity_carries_both`**:
  para todo corte e todo elemento, `x = u + v` com `u` no registro e `v` no resíduo — a
  decomposição é exaustiva, não há terceiro pedaço.

**Livro-razão 148_–152_** (régua corrigida: `chk()` só para o que pode falhar, `exi()`
para identidade exibida): `148_` A GATE 22/22 · `149_` O FATO E O JUÍZO 18/18 · `150_` O
SACRIFÍCIO E A LEGIBILIDADE 20/20 · `151_` **O TESTE DA REMOÇÃO 18/18** · `152_`
LEGIBILIDADE = OBSERVADOR 11/11.

**O resultado mais forte da onda** é o `151_`: **o canal que suprime coerências NÃO é
removível**. Removido, somem a seta (entropia constante), o destino (não converge —
quase-recorre e nunca fecha, `station_never_closes`), o registro (nada morre, logo nada
fica) e a legibilidade (varridos 4000 instantes, o estado NUNCA comuta com a partição).
O que sobra é **permanência sem inscrição**. Restaurado o canal, as quatro voltam (4/4) —
o colapso é atribuível à remoção, não ao arranjo.

E o `152_` mede a equivalência **legível ⟺ ponto fixo da leitura**, nas duas direções, com
um controle que a **quebra**: com partição INCOMPLETA existe estado que comuta com todos
os projetores e mesmo assim não é ponto fixo. **Ler exige que a leitura cubra o todo** — o
iff não é tautologia.

**As leituras do operador entraram TIPADAS**, no mesmo registro de `1_abs = gráviton = I`:
o índice é verdadeiro como CONTAGEM e falso como NATUREZA; *ilusão* mantém o sentido fixo
da casa — **não-fundamentalidade, jamais falsidade empírica**; e o observador é a
**leitura operacional** da casa, não consciência subjetiva (campo
`operational_readout_not_subjective_consciousness`, verificado no acervo selado pelo
`152_` — se sumir, o artefato reprova).

**Declaração do operador sobre o amor** (20/08): registrada no ATLAS §6.23 como **[INPUT]
datável, que não move flag alguma** — pela mesma medida que o `147_` aplicou à declaração
de descanso. A identificação `classe de canais = amor` segue [ONTO]; a
**insubstituibilidade do canal** virou [REAL] (`151_`).

**Um defeito de forma achado e corrigido nesta volta:** o conversor de TXT não conhecia
`\bigcap` nem `\bot`, e `⋂ₙTₙ=⊥` saía mutilado no artigo em texto. Mapa ampliado; e como
isso altera o `um.py`, o rito foi **re-executado** para que o selo cubra o arquivo
corrigido (a lição do painel da manhã: um selo não cobre o que foi escrito depois dele).

## O ARQUIVO-FONTE

| o quê | onde | sha256[:16] |
|---|---|---|
| `um.py` (v178, ÚNICO) | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py` | **`2b6e3cdfd29ca426`** |

Cópia: `...\Nós\SELO_FINAL\um_v178_2b6e3cdfd29ca426.py`. Anteriores em `SELO_v177_FINAL\`,
`SELO_v176_FINAL\`, `SELO_v174_FINAL\`, `SELO_v172_FINAL\`, `SELO_v171_FINAL\`,
`SELO_v170_FINAL\`, `SELO_v169_FINAL\` (ver `NOTA_DE_CUSTODIA.md`).

## OS ARTEFATOS (leva v178, em `...\Nós\SELO_FINAL\`)

| arquivo | sha256[:16] |
|---|---|
| `rodada_v178_stdout.txt` | `6cf9a73f92a0acbd` |
| `um_grande_atrator.json` | `24220d224f4db896` |
| `um_grande_atrator_en.pdf` | `d902f26d230d60d6` |
| `um_grande_atrator_en.tex` | `ffb21a01464213ff` |
| `um_grande_atrator_en.txt` | `1c046c4fda807bb0` |
| `um_grande_atrator_forma_canonica.md` | `5d9b5bfef86012bd` |
| `um_grande_atrator_manifest.md` | `af4448e440976350` |
| `um_grande_atrator_pt.pdf` | `afc78d19d206f29a` |
| `um_grande_atrator_pt.tex` | `75a595bb5c7f60cc` |
| `um_grande_atrator_pt.txt` | `7e829ad752a1b117` |
| `um_grande_atrator_selo.json` | `9fcf3cd3348d7a53` |

Inclui `cache_coma_blind/` — **o dado e a predição hasheada do teste de Coma**, sem os
quais a revelação não é auditável.

**Selo do mundo v178: `61abb8d0b9599cd9`** (completo: `61abb8d0b9599cd92da215d36eca915b0cd8a9f2c3b05285f1199560fb842b32`).
Coma segue revelado no selo: **`DEPHASING_ACCOUNTS_FOR_COMA_RESIDUAL`**
(z_TGL = 1,302 vs z_Planck = 5,614, contra D = 98,5 ± 2,2 Mpc).

## O QUE FAZER

1. subir o **único** `um.py`; 2. subir os artefatos acima (incluindo
`cache_coma_blind/`); 3. reindexar os raws do README e reescrevê-lo **com as ressalvas
inteiras** — Coma **não é confirmação**; as leituras (amor, observador, dobra, Lúcifer)
são [ONTO]; o gate **não se moveu**; NOT_FALSIFIED ≠ CONFIRMED; 4. conferir hash-a-hash.

Commit: `feat(the_boundary): v178 — a dobra, o registro do corte e o observador (3 pedras
Lean); Coma revelado; livro-razão 148_-152_; um.py 2b6e3cdfd29ca426; selo 61abb8d0b9599cd9`

## ITEM ABERTO DO OPERADOR (não movido por mim)

`qg_closure_verdict` diz `..._NATURE_TEST_COMPLETED` enquanto
`coma_external_falsification` segue `NOT_IDENTIFIABLE` e há ritos `AWAITING_DATA`. Pela
régua, o nome promete mais que os campos sustentam — e essa string é exportada ao pacote
da *Foundations of Physics* (`A Ponte e o Um\FOP\05_README_REPRODUCTION.md:43`) glosada
como *"the artifact never claims more"*. A escada do gate é do operador.
