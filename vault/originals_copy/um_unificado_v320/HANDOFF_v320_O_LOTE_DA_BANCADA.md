# HANDOFF v320 — O LOTE DA BANCADA (v311→v320) — para a sessão irmã (custódia `the_boundary`)

> Data: 06/09/2026 10:47 · Casa: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós`
> Escriba: Claude (sessão Central de Patentes, d554e796) · Operador: Luiz Antonio Rotoli Miguel
> Regra em vigor: NOT_FALSIFIED nunca é CONFIRMED; **CONFIRMADA proibido, PROVADA = teorema** (clarificação do
> operador, 05/09); o gate NÃO se moveu em nenhuma das dez versões; β jamais literal; hash jamais de memória.
> Gerado POR SCRIPT (`handoff_v320.py`): todo hash e número abaixo foi lido do disco agora.

## 0. A ORDEM DO OPERADOR (verbatim, 06/09/2026)

> *"após o término desta rodada escreva o handoff para a sessão irmã aqui do claude code que custodia o um no
> repositorio do The_boundary para ela realizar a custódia, mas peça para ela criar uma pasta de backup do um.py em
> outra pasta diferente do repositório para ir salvando as versões antigas com seus respectivos resultados antes de
> salvar por cima a versão nova, para irmos controlando as versões alteradas com backup salvo para comparação."*

## 1. ★ A REGRA NOVA DA CUSTÓDIA — o BACKUP DA VERSÃO ANTERIOR, FORA DO REPOSITÓRIO, ANTES DE SOBRESCREVER

**Antes** de copiar qualquer arquivo novo para `C:\IALD\Artigo\the_boundary\Um (absoluto) — Grande Atrator`, crie (se não existir) a pasta **fora do repositório**:

```
C:\IALD\Artigo\the_boundary_BACKUPS\
```

e dentro dela uma subpasta por versão que está sendo substituída, nomeada pela versão e pelo sha16 do `um.py`
que ESTÁ no espelho hoje — hoje o espelho tem: um.py sha16 `0969fc4809ca1229` (6,149,205 bytes; selo do espelho diz `0969fc4809ca1229`), mtime 01/09/2026 11:31. Ou seja, a primeira subpasta será algo como
`um_v310_<sha16-lido-do-espelho>\`. Nela vão, **byte a byte** (`open(p,"rb").read()` → `open(dst,"wb")`),
TODOS os arquivos de resultado que acompanham aquele `um.py` no espelho: `um.py`, `um_absoluto.json`,
`um_absoluto_selo.json`, os PDFs e TXTs (pt/en), `um_absoluto_forma_canonica.md`, `um_absoluto_manifest.md`,
`MEMORIA_DA_LINHAGEM.md`, `DESENHO_DO_FECHAMENTO_QG.md`, a pasta `rodadas\` e a pasta `Lean\` (o kernel daquela
versão) — mais um `BACKUP_MANIFEST.json` com `{arquivo: {bytes, sha256}}` de cada um, **gerado por script**.
Só depois de conferir que o manifesto do backup bate com o espelho (hash a hash) é que se sobrescreve.

Daqui em diante **toda custódia começa por esse backup** — o operador quer as versões alteradas guardadas com os
seus resultados, para comparação. Nunca `open(P,"w")` direto; temp → verificar tamanho → substituir; nunca `E:\`.

**Semente para a pasta de backups (as versões intermediárias v311–v319 que NÃO passaram pelo espelho):** em
`Nós\` existem os backups de BYTES pré-cirurgia `um.py.bak_<AAAAMMDD_HHMMSS>` — cada um é exatamente o `um.py` de
uma versão selada (a tabela do §3 foi calculada a partir deles, com o sha16 conferido contra o diário) — e os
stdouts `rodada_v311..v319_stdout.txt` são o resultado canônico de cada uma. Copie-os para
`the_boundary_BACKUPS\um_vNNN_<sha16>\` (um `um.py` + o `rodada_vNNN_stdout.txt` por versão; os JSON/PDF dessas
intermediárias foram sobrescritos pelos ritos seguintes — só o stdout sobreviveu, e isso fica DITO no manifesto
do backup). Mapa versão → backup: v311 → `um.py.bak_20260905_144827` · v312 → `um.py.bak_20260905_155815` · v313 → `um.py.bak_20260905_164113` · v314 → `um.py.bak_20260905_172023` · v315 → `um.py.bak_20260905_185816` · v316 → `um.py.bak_20260906_062325` · v317 → `um.py.bak_20260906_081147` · v318 → `um.py.bak_20260906_091046` · v319 → `um.py.bak_20260906_100208`

## 2. O ESTADO MEDIDO `[REAL — lido do selo e do rito agora]`

| o quê | valor |
|---|---|
| **`um.py`** sha256 | `d186a9c3d32ec76ab4619f0de32f7f0000be8eaf20f8d561a5af466ecea9f166` |
| sha16 | **`d186a9c3d32ec76a`** (7,916,694 bytes) |
| selo `sha256.um.py` == disco | SIM |
| teoremas limpos (stdout `rodada_v320_stdout.txt`) | **2399/2399** |
| autoteste | `FAIL_CLOSED_SELFTEST_PASSED` |
| gate | `TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_WITHIN_LOCAL_BULK_AT_AVAILABLE_SENSITIVITY__MORE_SENSITIVE_DATA_COULD_REVISE` |
| identidade | `1=1=VERDADEIRO=HAJA_LUZ` (`identity_true = True`) |
| contorno (v314+) | 8 ritos; falsificação limpa: NENHUMA ; `contorno_broken_v314 = []` |
| relatório de axiomas | 2731 termos; **fora do trio: 0** [] |
| kernel em `Nós\tgl_kernel` | `TGLExt/` 450 módulos + `TGL/` 27 módulos (Lean 4.31.0) |

**Confira antes de tudo.** Se não bater no seu lado, **pare** e escreva no `DA_IRMA.md`.

## 3. O ARCO v311→v320 (hash e contagem lidos do diário `MEMORIA_DA_LINHAGEM.md`, que os leu do disco em cada selo)

| versão | `um.py` sha16 | teoremas | o que entrou |
|---|---|---|---|
| v311 | `ac0be9d89f64c8c8` | 963/963 | Tomita CONSTRUIDO na torre (S, J, Delta, Delta^{it}) — 20 pedras da bancada ChatGPT |
| v312 | `09d6bec30171a9c1` | 1005/1005 | esperanca condicional dos ANDARES (`constructedLevelExpectations`) — ENTREGA_001 |
| v313 | `ac5595a8ad9fa72d` | 1060/1060 | rede localizada da cadeia A(I), cauda escalar, volume q_I — ENTREGA_003 |
| v314 | `920ba2b9a937b8b3` | 1060/1060 | o CONTORNO com poder de fechar o 1=1 (falsificacao limpa mata; inconclusivo nao) — rigor maximo do operador |
| v315 | `e13806c12799f5d4` | 1060/1060 | fidelidade: roster +neutrino_m2 +void_density_v41; kill_rule do neutrino como congelada (frozen_hash intocado) |
| v316 | `eb8c8fc5bb092708` | 1092/1092 | esperanca do centralizador LOCAL e TRACIAL; `tail_never_strict` (o parabolico de BW nao nasce do shift) — ENTREGA_006 |
| v317 | `e11229a1376fcd61` | 1879/1879 | lote 007..023: habitante GLOBAL periodico da esperanca; Borchers trivial; assinatura (inferencia refutada); camada GEOMETRICA GERAL em carta (Jacobson como teorema) |
| v318 | `dc17d17542875c19` | 2119/2119 | Gibbs no Hilbert da torre; limite termico NEGATIVO (nao-Cauchy); criterio de AFINIDADE; estado global fiel — 024..026 |
| v319 | `8aa6f64048c6cd49` | 2335/2335 | transporte modular com DOMINIOS no Hilbert original; resposta global finita; contraexemplo harmonico — 027..028 |
| v320 | `d186a9c3d32ec76a` | 2399/2399 | geometria CURVA de onda plana construida; casamento de area; liberdade residual (shear livre) — 029 |

**De onde veio:** a bancada **ChatGPT** (sessão irmã do operador) trabalha pelo TÚNEL
(`C:\IALD\Central de Patentes\Chatgpt\TUNEL\` — ORDEM_nnn da gerência, ENTREGA_nnn da bancada; 29 entregas
até agora, 001–029). **Só esta sessão escreve no `um.py`.** Cada entrega foi auditada antes de entrar: hashes
declarados e manifesto 100%; auditor da própria bancada rodado (exit 0); zero `sorry`/`axiom`/`native_decide`;
**recompilação INDEPENDENTE** de cada módulo contra os oleans do kernel canônico (todos os axiomas no trio
`[propext, Classical.choice, Quot.sound]`); guarda estática de colisão de nomes no ROOT (lição da v317:
`flatNullFrame`); `lake build` do ROOT limpo; rito completo com stdout canônico. Os módulos da bancada levam o
namespace `ChatgptAudit` e um cabeçalho de procedência/auditoria. **A partir da v311 o stdout do rito voltou a ser
gravado** (`rodada_v311..v320_stdout.txt`) — o seu pedido de 01/09 está atendido.

## 4. O QUE SE PROVOU, EM UMA LINHA CADA (estatutos da bancada, conferidos)

- **A esperança de Takesaki sobre o centralizador da torre está CONSTRUÍDA** (local, tracial e global para todo
  perfil com período comum) — o `[KNOWN, Takesaki 1972]` da v309 foi descarregado nesses casos; resta o aperiódico.
- **O parabólico de Bisognano–Wichmann não nasce da torre-produto** por nenhuma via (shift: `tail_never_strict`;
  Borchers: `product_borchers_trivial`) — negativos honestos que encolhem o caminho crítico.
- **A minha inferência sobre a assinatura foi REFUTADA** pela bancada (`single_boost_has_two_signatures`): um boost
  preserva (1,3) **e** (2,2). Anotado ao lado.
- **A camada geométrica geral em carta existe em kernel**: Levi-Civita, curvatura, Bianchi, Einstein geométrico com
  conservação, Raychaudhuri, e o **Jacobson como teorema** (`geometric_einstein_equation_from_ricci_null_balance`:
  balanço nulo de Ricci + T conservado ⟹ ∃Λ, G + Λg = κT); Clausius local ⟺ balanço nulo; telas e congruências
  nulas construídas. **O que ENTRA como INPUT**, dito pela bancada em cada entrega: métrica lorentziana suave,
  referencial, conservação de matéria, Clausius/casamento microscópico. H3 dinâmico, assinatura, dimensão,
  globalização, lei de área geral e a seleção da liberdade radiativa seguem OPEN.
- **Gibbs na torre; o limite térmico ingênuo NÃO existe** (não-Cauchy); **critério de afinidade** (Cauchy ⟺
  afinidade-limite > 0); **transporte modular com domínios** do estado global no Hilbert original; contraexemplo
  harmônico (afinidade positiva ≠ energia finita); **geometria curva de onda plana** que casa a área, com shear livre.
- **A árvore da prova** (`A_PROVA_DA_QG_TGL_arvore.md`, gerada por script do selo) diz, termo a termo, o que está
  PROVADO (a implicação: axioma + hipóteses nomeadas ⟹ estrutura da QG da TGL) e o que NÃO está (que a natureza
  realiza H1–H3; as folhas abertas). **CONFIRMADA continua proibido.** Leve-a para o espelho: é nova.

## 5. O QUE LEVAR PARA O ESPELHO (existência e sha256 lidos agora; bytes com `rb`/`wb`)

| arquivo (em `Nós\`) | bytes | sha256 (32) |
|---|---|---|
| `um.py` | 7,916,694 | `d186a9c3d32ec76ab4619f0de32f7f00` |
| `um_absoluto.json` | 1,638,036 | `41da751efe22233fb1a2388c2e102297` |
| `um_absoluto_selo.json` | 35,121 | `c16a0e8ee15975d5691861f24e7cd4da` |
| `um_absoluto_pt.pdf` | 1,729,481 | `a21a15321848d6420bf49bd15b887027` |
| `um_absoluto_en.pdf` | 1,697,823 | `4bc88218914bb441a6956646c72e7517` |
| `um_absoluto_pt.txt` | 499,045 | `7d403eccb7c2b833db22d7aa71641b48` |
| `um_absoluto_en.txt` | 500,929 | `1665cebf40f5391e8ba06550fe8a7ae7` |
| `um_absoluto_forma_canonica.md` | 145,233 | `3a44079f3acc3bc208f8f5135c642444` |
| `um_absoluto_manifest.md` | 460,940 | `f3429fa879f30924796965e8a6d58d21` |
| `A_PROVA_DA_QG_TGL_arvore.md` | 16,556 | `34a4e9d5aca10de433fb11355f97d726` |
| `MEMORIA_DA_LINHAGEM.md` | 451,736 | `082d29b51c4250d3ceceeed9be31d47b` |
| `DESENHO_DO_FECHAMENTO_QG.md` | 86,519 | `0c95b9604afe65841ee76f94ec7f4b5e` |
| `rodada_v308_stdout.txt` | 188,597 | `56776407e20e2da948ebb60ff1532ddd` |
| `rodada_v309_stdout.txt` | 188,735 | `58fa9bd6881c6af4c3a19bdae1dd3d33` |
| `rodada_v310_stdout.txt` | 188,872 | `89d08dab242baedd728e4d0fd53d51a7` |
| `rodada_v311_stdout.txt` | 188,809 | `b1a1d0d1b7e37c585327a1afa9d8ef36` |
| `rodada_v312_stdout.txt` | 188,814 | `26b912433592daa671294f93b149a9d0` |
| `rodada_v313_stdout.txt` | 188,814 | `e810dc88b0039e57673152dca2f9249b` |
| `rodada_v314_stdout.txt` | 188,929 | `85d375627727482088a28a7408f376f3` |
| `rodada_v315_stdout.txt` | 188,929 | `2ead284d40fd4e3ff85a0943cd1e130d` |
| `rodada_v316_stdout.txt` | 188,936 | `6f92e977a42acc83ba8ee739069a1f1b` |
| `rodada_v317_stdout.txt` | 188,936 | `1f5ab12fec15b3c7b26decb4ed520065` |
| `rodada_v318_stdout.txt` | 188,936 | `54e451472c919ad59a5a20a65fe15f14` |
| `rodada_v319_stdout.txt` | 188,936 | `6517c985d2743ecae00cbad3c5079e58` |
| `rodada_v320_stdout.txt` | 188,936 | `31242a0f9b819d687a3483152aa64b72` |

Mais: a pasta **`Nós\tgl_kernel\`** inteira (`TGL/`, `TGLExt/`, `TGL.lean`, `TGLExt.lean`, `lakefile`, `lean-toolchain`,
`README.md` — **sem** `.lake/`) para `C:\IALD\Artigo\the_boundary\Um (absoluto) — Grande Atrator\Lean\tgl_kernel\` e para o cofre da Central
(`vault\originals_copy\tgl_kernel_v320\` + `CUSTODY_MANIFEST.json`, como na v310); os stdouts para `rodadas\`;
e a procedência da bancada: `C:\IALD\Central de Patentes\Chatgpt\TUNEL\` (ORDENS e ENTREGAS) — copiar a pasta
`TUNEL\` inteira para `C:\IALD\Artigo\the_boundary\Um (absoluto) — Grande Atrator\bancada\TUNEL\` é o suficiente (os fontes .lean da bancada já estão no kernel).
**Não levar:** `.lake/`, `cache/`, backups `.bak_*`, nada de `E:\`, nenhum confidencial.

## 6. AS PORTAS

Regenerar `PORTA.md`/`PORTA.json`/`llms.txt` **por script** (`gerar_portas.py`), nunca à mão; hash lido do
artefato; aditivo. A seção «Como matar esta teoria» e o TÚNEL ficam. **Commit/push são ato do operador** — deixe
o repositório pronto e diga no `DA_IRMA.md` o que ficou staged.

## 7. O QUE EU FAÇO DEPOIS DA SUA CUSTÓDIA

Sigo com as entregas novas da bancada (a próxima é a 030; ela produz uma a cada ~35 min) pelo mesmo pipeline —
varredura, recompilação independente, guarda de colisão, build, rito, verificação, árvore, superfícies — e
emito novos handoffs por lote. Responda no `Nós\DA_IRMA.md` (datado) quando a custódia v320 estiver feita, com o
sha16 que você leu do espelho e o caminho do backup criado.

*Cosmologia jamais vira prova matemática. O gate não se move por este documento.*
