# O PsiBit como leitor do par que sai da fórmula

Candidata do Codex para revisão da gerência, em pasta isolada da v412. A identificação da leitura do par como compressão originária é a indicação do autor [INPUT]. A escolha de manter dois resíduos sintáticos e de representar os seus resultados pelos sinais da órbita é a construção examinada aqui.

## As duas respostas ao autor

**O que fica depois de uma cláusula?** Escolha uma variável x. Guarde duas fórmulas sobre as variáveis restantes. A primeira diz o que ainda é preciso cumprir se x vale 0. A segunda diz o mesmo se x vale 1. Inicialmente ambas são a conjunção vazia, que vale verdadeiro. O par se obtém da escrita da fórmula. Nenhuma lista de atribuições ou de pesos serve de entrada.

**Como entra a próxima cláusula?** Em cada ramo, se o valor escolhido para x satisfaz um dos seus literais, a cláusula já está paga. Caso contrário, retire os literais de x, que agora são falsos, e acrescente ao ramo o que sobrou. Se sobra uma cláusula vazia, esse ramo é impossível. Para qualquer atribuição comum das demais variáveis, ler um ramo devolve exatamente o valor do prefixo original na opção correspondente de x.

[REAL no Lean] A soma dos tamanhos dos dois resíduos do prefixo é no máximo **duas vezes** o tamanho desse prefixo, contando uma unidade por ocorrência de literal e uma por cláusula. É uma cota para o resumo de uma variável. O índice e o sinal de cada literal continuam representados. Ver `summarize_spec` e `prefix_size`.

## O que o PsiBit recupera

[REAL no Lean] Há dois vínculos com o kernel. Para os bits lógicos, a convenção verdadeiro ↦ +1 e falso ↦ −1 realiza o par nos sinais Palavra e Verbo de uma amplitude da órbita. O ângulo atesta que o par é representável. Para os pesos efetivos de um ramo e do outro, com a mesma atribuição restante, normalizamos o vetor, conservamos a sua norma e usamos o código canônico da amplitude normalizada. Decodificar e repor a norma recupera os dois pesos. A cláusula seguinte multiplica cada peso por 1 se satisfeita e por r se violada, onde r = (1 − β)ᵏ no ciclo. A escala conservada é explícita. Ver `leitura_psibit`, `round_trip` e `update_spec`.

[REAL no Lean] A Palavra e o Verbo *da candidata REV65 da gerência* têm uma segunda realização. Para a Palavra, o algoritmo elimina uma variável por vez e decide a fórmula. Para o Verbo calado, verifica em cada cláusula se nela aparecem um literal e seu oposto. Uma cláusula que carece de tal par admite uma atribuição que falsifica todos os seus literais; a prova constrói essa atribuição. O Verbo do prefixo atualizado é o Verbo anterior em conjunção com o resultado da nova cláusula. A busca ingênua faz no máximo o quadrado do comprimento de cada cláusula em comparações de literais. No tempo pago s > n·ln 2, `bits_spec` identifica os dois resultados com os predicados da REV65. A representação dos resultados como sinais em `bits_on_orbit` estabelece uma codificação. A identificação das duas derivadas físicas ou analíticas precisaria de outro termo.

## Onde aparece o custo global

[REAL no Lean] Para eliminar x, o algoritmo reúne as possibilidades dos dois ramos sob a mesma atribuição restante. Se os resíduos são A e B, o resultado é A ∨ B. Em forma de conjunção de cláusulas, a distribuição utilizada produz C ∨ D para todo C de A e todo D de B. Preserva satisfazibilidade para qualquer fórmula. O número de cláusulas que esta implementação escreve é exatamente |A|·|B|. O exemplo compilado no arquivo vai de duas cláusulas sobre a última variável para quatro e depois dezesseis nas duas primeiras eliminações. Trata-se da distribuição implementada, antes de qualquer simplificação. Ver `merge_size`, `eliminate_spec` e `solve_spec`.

[REAL no Lean] Há um critério geral para a atualização por cláusula. Se dois prefixos deixam o mesmo estado de um atualizador determinístico exato, têm de aceitar as mesmas atribuições. A demonstração escolhe uma atribuição em que poderiam diferir e acrescenta uma cláusula unitária para cada variável, fixando essa atribuição. A continuação daria duas respostas diferentes a partir do mesmo estado. Isso caracteriza o que um estado tem de distinguir, sem exigir que o estado armazene uma tabela-verdade. Ver `all_continuations_iff` e `same_state_preserves_assignments`.

[REAL no Lean] Exemplo mínimo para os dois bits da REV65. Os prefixos y e ¬y admitem solução e têm Verbo ativo, portanto emitem o mesmo par de respostas. Acrescentar y deixa y ∧ y satisfazível e torna ¬y ∧ y insatisfazível. Os dois bits emitidos não bastam como *única* memória da etapa seguinte. O fenômeno também alcança uma agregação ponderada específica. Após somar sobre y em cada ramo de outra variável x, os dois prefixos têm o mesmo par (1+r, 1+r). Depois da mesma cláusula y, os valores por ramo são 1+r² e 2r, distintos para 0 < r < 1. Mesmo guardar a escala e o código inteiro **dessas marginais** não recupera a correlação perdida com y. Ver `bits_alone_not_updatable` e `no_marginal_update`.

## Margem finita e solução única

[REAL no Lean] Escreva q = 2ⁿr, com 0 ≤ r ≤ 1. Para qualquer máscara de atribuições, a soma é pelo menos 1 se a máscara contém uma solução. Sem solução nela, a soma é no máximo q. Quando q < 1, o limiar (1+q)/2 separa os casos até com erro absoluto estritamente menor que (1−q)/2. Para 0 < β < 1, tomar kβ ≥ (n+2)·ln 2 garante q ≤ 1/4. A demonstração usa β como parâmetro e não fixa uma medição física. Ver `leitura_com_folga`, `sinal_do_passo` e `cauda_uniforme`.

[REAL no Lean] Havendo exatamente uma solução, uma leitura do todo verifica existência e n leituras das máscaras «a coordenada i vale 1» recuperam todos os seus bits sob a mesma margem. O argumento inclui n = 0. Há também uma reconstrução diretamente da sintaxe: o decisor recebe a fórmula original e, para cada i, a fórmula acrescida da unidade que exige i = 1. Retorna os mesmos bits sob a hipótese de unicidade. Essa segunda construção dispensa obter numericamente as somas. Ver `n_mais_uma_leituras` e `syntax_recovers_unique`.

**[OPEN]** Permanece aberta a cota polinomial uniforme, em operações de fita, para obter a Palavra em toda CNF. A nova prova dá atualização direta com tamanho controlado no primeiro par, leitura fiel, critério de equivalência de estados e reconstrução. A etapa sem essa cota é manter as correlações e eliminar todas as variáveis com custo total polinomial. A colisão demonstrada decide a insuficiência dos dois resumos explícitos examinados e preserva a possibilidade de outras representações.

Os arquivos `*.verificado.json` trazem os hashes da fonte, do executável Lean, dos imports diretos e do objeto, a saída de compilação e os axiomas das declarações auditadas. Os diagnósticos intermediários pertencem às versões em elaboração. A revisão da ORDEM 030 sobre as fontes da gerência está em recibo próprio.
