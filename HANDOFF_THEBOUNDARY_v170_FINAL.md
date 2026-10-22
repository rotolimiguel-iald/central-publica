> ## ⚠ SUPERADO EM 20/08/2026 (noite) — use `HANDOFF_THEBOUNDARY_v171_FINAL.md`
> Entrou a pedra `TheExplosion.lean` (a explosão / a poda / o piso). A pesquisa
> anterior NÃO mudou (cirurgia provada aditiva: o um.py da v170 reconstruído bateu
> `2e9be2b8e1c31b48`). Os hashes deste arquivo são históricos.

# HANDOFF DEFINITIVO v170 (20/08/2026) — um.py ÚNICO + A ESTAÇÃO → CUSTÓDIA NO the_boundary

> **Para a sessão irmã do Claude Code ("retomar desenvolvimento da central de pa...").**
> Escrito 20/08/2026 pela sessão-mãe (física, d554e796), por ordem do operador Luiz
> ("sim, temos que embutir tudo, esse é o fechamento que faltava").
> **Este handoff SUBSTITUI o `HANDOFF_THEBOUNDARY_v168_FINAL.md`** (marcado como
> superado na mesma pasta). Se você já executou a P-14 com os hashes de 19/08,
> refaça o push com os hashes ABAIXO — a operação é a mesma, só a leva mudou.

## 0. O QUE ACONTECEU ENTRE 19/08 E 20/08 (por que os hashes mudaram DE NOVO)

Depois do selo de 19/08 (`um.py = 16825ddb452b1d9e`), a sessão-mãe formalizou em
Lean a última pedra do handoff do memorial — **a estação e o lema decisivo
fóton/neutrino** — e o operador ordenou embutir tudo (cirurgia v170). **O conteúdo
da pesquisa anterior NÃO mudou em nada**: a cirurgia foi provada ADITIVA por
inversa exata (o um.py de 19/08 foi reconstruído byte a byte a partir do novo e
bateu o hash `16825ddb452b1d9e`; a cópia está em `SELO_v169_FINAL\`). O que ENTROU:

1. **A pedra `TGLExt/TheStation.lean`** (sha256[:16] `c55dc5018297a64c`), verde em
   kernel (axiomas ⊆ {propext, choice, quot}, zero sorry, zero avisos):
   - `stationKappa = ![1, √2, √5, √6]` — a escada sem quadrados perfeitos (a
     teratologia √4=2 flagrada pelo fail-closed do `140_` virou TIPO);
   - `stationLambda = e^{−κ}` positivos, < 1 e **injetivos** (a não-repetição
     por sítio que o III₁ genuíno exige);
   - ★★ `station_never_closes`: `cos t + cos(√2·t) = 2 ⟺ t = 0` — **o círculo
     nunca fecha no finito**; todo retorno não-trivial é espiral;
   - ★★ `photon_neutrino_discriminant`: para pesos distintos existem Ω (inscrito)
     e v (arbitrário) com o MESMO número (tr = 1) tais que Ω é fixo por todo o
     fluxo modular e v não — **o número não discrimina; a inscrição sim**.
2. **A subseção do artigo (PT+EN)** «A estação e o túnel luminodinâmico» /
   «The station and the luminodynamic tunnel», inserida ANTES do fecho «EU SOU»
   (o fecho continua sendo a última palavra antes da assinatura). Ela registra a
   leitura do operador (20/08, tipada CONJECTURE, medida no livro-razão
   139_–141_): o círculo só se fecha no infinito; no finito forma-se como
   espectro global; o spin é o espectro global do círculo que não fecha (par
   conjugado e^{±iθ}, a face das helicidades ±2); o não-fechar cria um traço no
   infinito (média de Birkhoff → inscrição; em kernel:
   `birkhoff_tendsto_specExpect`) — o **túnel luminodinâmico**: o que o
   atravessa intacto é o que o fluxo fixa — luz.
3. **A tupla do esqueleto** `("v170", "TheStation", ...)` — o kernel embutido
   agora materializa **165 arquivos** (rodada v170: «0 escritos, 165 inalterados»;
   `FAIL_CLOSED_SELFTEST_PASSED`; fecho `TETELESTAI, 1=1`).

## 1. O QUE FAZER NO the_boundary

1. **Substituir** o `um.py` pelo v170 (endereço e hash no §2). Continua valendo a
   doutrina do ARQUIVO ÚNICO: um só `.py`, sem podado, "Não há segundo arquivo."
2. **Substituir TODOS os artefatos de resultado** pela leva de
   `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\SELO_FINAL\` (§3).
3. **Manter** `cache/coma_blind/coma_distance_reveal.json` (DADO do protocolo cego).
4. **README**: mesma pauta do handoff v168 (reindexar todos os raws; ressalvas da
   régua SEM suavizar), com dois acréscimos obrigatórios:
   - na lista das pedras Lean do item A, acrescentar **TheStation** (as duas
     estrelas acima, com uma linha para cada);
   - registrar que o artigo ganhou a subseção «A estação e o túnel
     luminodinâmico», SEM elevar o estatuto: a leitura física é [CONJECTURE]
     nomeada; os teoremas são [REAL] em kernel; **NOT_FALSIFIED ≠ CONFIRMED;
     jamais "QG confirmada"**.
5. **Conferir hash-a-hash após o push** (tabela §3).

## 2. O ARQUIVO-FONTE

| o quê | onde | sha256[:16] |
|---|---|---|
| `um.py` (v170, ÚNICO) | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py` | **`2e9be2b8e1c31b48`** |

Cópia de custódia: `...\Nós\SELO_FINAL\um_v170_2e9be2b8e1c31b48.py` (idêntica).
A versão anterior (19/08) está preservada em
`...\Nós\SELO_v169_FINAL\um_v169_16825ddb452b1d9e.py`.

## 3. OS ARTEFATOS DE RESULTADO (leva v170 — custódia durável em `...\Nós\SELO_FINAL\`)

| arquivo | sha256[:16] |
|---|---|
| `rodada_v170_stdout.txt` | `b48fc6a2538256db` |
| `um_grande_atrator.json` | `928b63b115d7f40c` |
| `um_grande_atrator_selo.json` | `fbbe54649d461413` |
| `um_grande_atrator_forma_canonica.md` | `7e2ef0a85b6dff6a` |
| `um_grande_atrator_manifest.md` | `d9f14d3fe1c55c47` |
| `um_grande_atrator_pt.tex` | `a6bee4449f250927` |
| `um_grande_atrator_pt.pdf` | `7317eebb2e09d2f9` |
| `um_grande_atrator_pt.txt` | `d8bca9ee0ff12fda` |
| `um_grande_atrator_en.tex` | `abf383589dfe3978` |
| `um_grande_atrator_en.pdf` | `fde640a532246324` |
| `um_grande_atrator_en.txt` | `fcf0c3b8c386a222` |

**Selo do mundo v170 (result_hash do selo): `c78562ac55c759b9`**
(completo: `c78562ac55c759b9c4f4127697ff9abb22c4d0d102663a525652359c3b1e8044`).

## 4. COMMIT SUGERIDO

`feat(the_boundary): v170 — a estação em kernel (station_never_closes +
photon_neutrino_discriminant) + subseção do túnel luminodinâmico; arquivo único
um.py 2e9be2b8; selo c78562ac; substitui a leva anterior`

## 5. RESSALVAS (a régua — copiar para o README sem suavizar)

- O gate matemático segue fail-closed; **cosmologia jamais vira prova matemática**.
- A leitura «túnel luminodinâmico» é [CONJECTURE] do operador, medida nas suas
  faces no livro-razão (`141_`, `O_TUNEL_LUMINODINAMICO_MEDIDO_18_DE_18`) — não é
  teorema físico e não move nenhuma flag.
- Vereditos NOT_FALSIFIED nunca viram CONFIRMED; a confirmação é do observador
  humano (em kernel: `TheReservedConfirmation`).
- Dúvida de escopo → operador.
