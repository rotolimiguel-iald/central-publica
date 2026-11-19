# Nota de oficina: nomear `(0 : Fin L)` numa assinatura pede `[NeZero L]` (Lean 4.31.0 / sandbox k411c)

[nota do Kimi, 18/11/2026; registro interno da oficina `candidatas_kimi`; não é candidata; nada instalado]

A `instOfNat` do núcleo exige `[NeZero n]`: o numeral `(0 : Fin L)` com `L` livre **não elabora** — qualquer
assinatura que nomeie a posição `0` (literal `⟨0, b⟩`, `f 0`) precisa da instância `[NeZero L]` no enunciado.
Não confundir com a hipótese: `hp : p ≠ 0` só é **habitada** com `L ≥ 2`, mas quem tipa o termo é a instância —
a hipótese não alcança a elaboração do `0`. (E em `L = 1`, `Fin 1` tem um único elemento: `p ≠ 0` é vazio.)
Foi o laço da pedra `AFitaEOIndice` (18/11/2026): cinco assinaturas ganharam `[NeZero L]`, com NOTA DO LAÇO
no cabeçalho dela; enunciados preservados na forma, a instância é o dado de tipo.
Irmã de `NOTA_PRECEDENCIA_NOT_EQQ_18nov.md` (a precedência de `!` menor que `==`): as duas são armadilhas de
elaboração desta versão, não eixos novos — nenhum termo já selado se move.
