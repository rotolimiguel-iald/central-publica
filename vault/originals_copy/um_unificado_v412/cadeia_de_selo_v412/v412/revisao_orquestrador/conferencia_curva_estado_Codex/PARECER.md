# Conferência da resposta do Kimi sobre a curva e o estado

## O que a continuação distingue

[REAL] Na candidata `ACurvaEAEstado`, o corte é depois da primeira de duas cláusulas. Compare `[x, x]` e `[¬x, x]`. O sufixo é o mesmo. Nos dois casos a fronteira é a variável x. Na ordem de células (falso, verdadeiro), e escrevendo q = exp(−t), obtêm-se as seguintes leituras.

| Prefixo | Peso em falso | Peso em verdadeiro | Curva do prefixo | Palavra depois de x |
|---|---:|---:|---:|---|
| x | q | 1 | 1 + q | verdadeira |
| ¬x | 1 | q | 1 + q | falsa |

A igualdade das curvas vale para todo t real. A diferença da célula verdadeira vale para t ≠ 0. Em t = 0, ambas as tabelas têm duas entradas iguais a 1. O objeto comparado em Lean é `resumo continuacaoPos t 1` ou `resumo continuacaoNeg t 1`: o restante da fórmula determina quais rótulos a fronteira precisa conservar. Tomar o prefixo como fórmula já terminada produziria uma fronteira vazia.

[REAL] A igualdade dos PsiBits dos prefixos em todo t e a insuficiência conjunta da curva e dos PsiBits para continuar vêm de `pin_psibits_equal` e `no_unmasked_curve_update` na entrega anterior `PalavrasResiduais.lean`. A expressão “curva dada de graça” fortalece a hipótese do leitor: ele pode consultar a função inteira e ainda recebe a mesma entrada nos dois casos. O teorema independe do custo de obter a curva. Aqui a soma preserva o peso total e apaga a associação do peso ao valor de x. Quando a fronteira tem w variáveis a tabela explícita tem 2^w entradas rotuladas.

[ONTO] “Ângulo de Miguel” e “token ao quadrado” são a interpretação do operador para essa releitura. A própria candidata faz essa distinção no cabeçalho. O enunciado verificado é uma soma sobre células e uma colisão da projeção. Para identificar formalmente essa operação a um operador de outro módulo seriam necessários o mapa entre os tipos e o lema que o relaciona à soma.

## O alcance da formalização

[REAL] A soma das células em `ACurvaEAEstado.a_curva_e_a_soma_das_celulas` quantifica sobre `CNF 1`. O complemento `ProjecaoDaFronteira.lean` trata de toda `CNF n` e todo corte. Em `weighted_projection`, o peso adicional pode ser qualquer função real g dos rótulos da fronteira. Somar os pesos após aplicar g em cada atribuição dá o mesmo que multiplicar cada célula já agregada por g e somar as células. Com g = 1, `total_projection` recupera toda a curva do prefixo. Em `append_supported_clause`, se todas as variáveis da cláusula acrescentada pertencem à fronteira do corte, a tabela antiga e os fatores da cláusula dão diretamente o novo total. Esse caso inclui a continuação x do exemplo. O objeto calculado aqui é o total após uma cláusula. A prova não atribui custo unitário à aritmética real.

[REAL] No §4 da resposta do Kimi convém precisar a expressão “sem retocar o lido”. `OResumoEPsiBit.a_atualizacao_pela_clausula_seguinte` continua somando sobre atribuições completas e usa `pesoDas (φ.take j) t x` no lado direito. A identidade dos pesos está provada. Uma implementação que usa somente a tabela real anterior para qualquer mudança de fronteira é uma afirmação adicional. Para a Palavra, a atualização *booleana* por tabela de atribuições extensíveis já está formalizada em `RelacaoFronteira.advance_valid`: ela testa se existe uma extensão, sem guardar os valores reais da curva.

[DERIVED] É possível escrever a transição real esperada inclusive quando chegam variáveis novas. Sejam P o prefixo, C a cláusula e T o restante. Escreva F para a fronteira antiga, G para a nova e D = F ∪ vars(C). Cada variável de G está em D. Para uma célula v em G e o resumo R definido por soma sobre atribuições completas, a regra é

```text
2^|D ∖ F| · R_novo(v)
  = Σ_{z em {0,1}^D, z restrito a G = v} R_antigo(z restrito a F) · fator_C(z).
```

A normalização decorre da definição do Kimi. Nenhuma variável de D ∖ F ocorre em P. Para cada célula antiga, trocar esses bits é uma bijeção que preserva o peso do prefixo. Suas 2^|D ∖ F| subdivisões têm então a mesma massa. Multiplicar cada subdivisão pelo fator da cláusula e somar as que caem em v dá a expressão. Essa derivação em papel indica exatamente onde as variáveis novas entram. O complemento Lean desta conferência verifica a projeção geral e o caso da cláusula suportada descritos acima.

[OPEN] Na entrega examinada, decidir a Palavra de toda CNF plana dentro de um único polinômio no número de letras da entrada continua em aberto. `necessary_states` impõe ao menos 2^n estados distinguíveis, correspondentes a pelo menos n bits em uma codificação fixa, ao leitor determinístico que funciona para todo sufixo. É compatível com memória polinomial. A tabela explícita tem 2^w células e w pode atingir n. O tamanho dessa tabela e o custo de um algoritmo que a materializa não dão um limite inferior universal para outras representações. Uma prova do polinômio precisa identificar a representação e contar as transições na fita, incluindo construção, atualização e leitura da resposta.

## Evidência

As fontes examinadas são candidatas. O recibo `RESULTADO.json` identifica, por bytes e SHA-256, a resposta do Kimi, os fontes, os objetos e os relatórios de compilação. Distingue as duas recompilações desta conferência, os dois módulos anteriores cujos recibos foram reconferidos e o complemento do Codex. O aceite editorial continua com a gerência.
