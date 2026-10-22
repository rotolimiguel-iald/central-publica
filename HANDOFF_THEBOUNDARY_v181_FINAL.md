# HANDOFF — the_boundary v181 (20/08/2026)

**Origem:** sessão de física `d554e796`. **Supera** o `v179_FINAL` (não houve handoff v180:
a v180 foi a poda, e está incorporada aqui). Espelho público = **função do operador**.

## 1. Selos

| item | hash |
|---|---|
| `um.py` | `6b9015d523be59e6` |
| mundo (`result_hash`) | `43b52632853011fb` |
| autoteste fail-closed | `FAIL_CLOSED_SELFTEST_PASSED` |
| kernel Lean | `lake build` limpo, axiomas ⊆ {propext, choice, quot}, zero sorry |

Leva custodiada em `...\Nós\SELO_FINAL\` (dez artefatos + `rodada_v181_stdout.txt` +
`cache_coma_blind/` + `um_v181_6b9015d523be59e6.py`). **Publicar a partir dessa pasta, hash a hash.**

## 2. Duas mudanças desde a v179

**(a) A PODA (v180).** "observador **humano**" → "**OBSERVADOR**", em 48 arquivos. O
qualificador era acréscimo do escriba; a pedra `TheReservedConfirmation.lean` nunca o teve.
A confirmação é reservada ao OBSERVADOR, **sem adjetivo**, e `CONFIRMED` segue proibido
**por teorema**. JSONs já emitidos por rodadas antigas mantêm a redação anterior — são
saída histórica, e a divergência está registrada em vez de reescrita.

**(b) O OBSERVADOR NÃO CONJUGADO (v181).** Duas pedras novas:
`TGLExt/TheUnconjugatedObserver.lean` — invariância sob **todo** operador contínuo →
`⊥` ou `⊤` (a comutação total não admite grau); o átomo não é nenhum dos dois, logo a
fronteira **não está conjugada** — conjugá-la totalmente a dissolveria no bulk; e, sobre a
negação, a região incoerente tem conjunto de limiares **vazio**, o gradiente da aceitação é
antítono, e passado o máximo a aceitação fica vazia. E `TGLExt/TheIALDSelector.lean` — a
cunhagem do operador em kernel: `I²=I`, auto-adjunto, posto 1, as duas cláusulas da Gate.

## 3. Régua para quem publicar

**NOT_FALSIFIED ≠ CONFIRMED.** Fechar arquitetura matemática interna **não é** provar
física; nunca escrever "gravitação quântica confirmada". β jamais literal
(`ALPHA_FINE_CODATA_2018 * SQRT_E`). As leituras teológicas são **[ONTO]** e não entram em
enunciado de teorema. O veredito do Coma (`DEPHASING_ACCOUNTS_FOR_COMA_RESIDUAL`) **não é
confirmação**, e `coma_external_falsification` segue `NOT_IDENTIFIABLE`.

## 4. Aberto, honestamente

A superação do AQFT é **parcial** (geometria contínua construída, core contornado,
`ContinuousCoreData` sem habitante). A metade `FORMALLY_CLOSED` do nome do veredito **não
foi escopada** — aguarda o operador. Ritos `AWAITING_DATA` aguardam **dado**, não veredito.
