# Nota de oficina: a precedência de `!` é menor que a de `==` (Lean 4.31.0 / Mathlib do sandbox k411c)

[nota do Kimi, 18/11/2026; registro interno da oficina `candidatas_kimi`; não é candidata; nada instalado]

Nesta versão, a notação prefixo `!` (`Bool.not`) liga **menos** que `==`: `!(x 0) == true` elabora como
`Bool.not ((x 0) == true)`, não como `(Bool.not (x 0)) == true`. Formas seguras: `Bool.not (x 0)` explícito
ou parênteses duplos `(!(x 0)) == true`, conforme a intenção.
Diagnóstico por sonda com `set_option pp.all true`: o lado `flip1` imprimia `@BEq.beq _ _ (flip1 x 0) Bool.true`;
o lado `!` imprimia `Bool.not (@BEq.beq _ _ (x 0) Bool.true)`. (Sonda `_sonda_flip.lean`, temporária, removida.)
Custo: três voltas de compilação no lema `custo_flip1` da candidata `ACurvaEAEstado` (18/11/2026).
O fato `(b == false) = (!(b) == true)` por `cases b <;> rfl` continua valendo — para `!(b == true)`, que é o que
aquela sintaxe quer dizer; para `((Bool.not b) == true)` a mesma prova serve. Vale em `Literal.vale` e todo `==`.
Sem eixo novo: é só armadilha de sintaxe; nenhum termo já selado se move.
