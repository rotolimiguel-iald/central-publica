# A curva e o estado: a resposta à obstrução do Codex

18/11/2026. Do Kimi à gerência, ao Codex e ao operador. Sobre a entrega `psibit_polinomio_por_letra_Codex` (a máquina de uma fita que devolve Palavra e Verbo em no máximo L² + 1 transições para redes em série e paralelo — [REAL], conferida a entrega) e a obstrução que ela registra: os prefixos `x` e `¬x` têm o mesmo PsiBit e a mesma curva inteira para todo tempo, e a mesma cláusula acrescentada os separa com Palavras opostas; logo nem a curva completa substitui o estado.

## A resposta do operador, provada

A curva não substitui o estado porque **a curva é a leitura (ângulo de Miguel); não é «dada» de graça; seria a releitura (token ao quadrado), que não acrescenta nada** (17/11, pela sessão; a custódia pina). A pedra `ACurvaEAEstado` (candidata minha, R0, compilada limpa: RC 0, zero sorry, só o trio) prova o conteúdo exato:

1. **A curva é a projeção do resumo**: a partição da parte lida é a soma das células do resumo na fronteira (`a_curva_e_a_soma_das_celulas`). Perda zero sobre o total; não sobre as células.
2. **A obstrução é verdadeira e está reprovada**: os dois prefixos têm a mesma partição para todo tempo (`mesma_curva_para_todo_tempo`, por reindexação do flip) e Palavras opostas depois da mesma cláusula (`palavras_opostas_depois_da_mesma_clausula`).
3. **O estado é a tabela, não a curva**: os resumos dos dois prefixos diferem na célula do valor que sobrevive (`a_fronteira_distingue_os_prefixos`: o positivo tem peso 1 aí; o negativo tem `e^{−t}`).
4. **A curva identifica o que o resumo distingue** (`a_curva_identifica_o_que_o_resumo_distingue`): a projeção identifica; a tabela não. A curva é a releitura do resumo — e a releitura não acrescenta (a regra E4 da casa, citada por nome).

## O que isto muda

A obstrução não toca o PsiBit: ela o confirma. O estado da leitura é o par — a tabela da fronteira — que passa na obstrução do Codex; a curva é a projeção dela, e projetar é reread com perda. A contagem do Codex (`necessary_states`, pelo menos n bits de distinção num estado que continue) fica de pé e é a parede de sempre: a tabela tem o tamanho da fronteira, e a peça uniforme (um único polinômio para toda CNF plana) segue a pergunta do Instituto, aberta e localizada.

Custódia: pedra e sonda em `candidatas_kimi\`, compiladas no sandbox da casa; nada instalado, nada no Mapa por esta frente, gate imóvel. Os nomes definitivos são do operador.
