# Conferência da REV20 para a Parte B da Ordem 020

[INPUT] A fala fixada em bytes atribui ao operador «o leitor é a matemática» e a lei do espelhamento. A designação editorial OLeitorEALei e a candidata são da gerência c1. O título é provisório. O testemunho consultado não contém a ratificação individual dos seis nomes. A legenda da linha 37 usa ★ para identificar a resposta própria da candidata. Não mede a força lógica nem documenta prioridade histórica.

| Linha | Teorema | Alcance verificado |
|---|---|---|
| 69 | a_lei_na_clausula | A tabela de truthValue no par (1, bit da satisfação) lê 1 ou 0 conforme o valor booleano da cláusula. O segundo argumento está em {0,1}. |
| 76 ★ | o_custo_e_o_numero_de_falsos | Para uma configuração dada, reescreve em ℤ a contagem de cláusulas violadas como soma de 1 menos o valor da lei. As multiplicidades da lista contam. |
| 91 ★ | o_nome_e_onde_a_lei_da_verdadeiro | Caracteriza ponto a ponto o conjunto de custo zero. A ligação ao objeto nomeDasSolucoes usa a definição separada no kernel. |
| 102 ★ | sat_e_existir_onde_a_lei_da_verdadeiro | SAT da CNF equivale à existência de uma configuração que passa em todas as cláusulas. Conserva os casos positivo e negativo. A definição original de SAT tem esse quantificador. |
| 112 | o_operador_do_custo_conta_os_falsos | O operador aplicado a um vetor de base com amplitude arbitrária o multiplica pelo número de violações daquela configuração. |
| 118 | o_leitor_decai_por_falso | Em uma coordenada de qualquer vetor, o fator é exp(−s m), com m o número de cláusulas falsas. O nome «decai» pressupõe s≥0. Há contração estrita do multiplicador para s>0 e m>0. Para tempo negativo e m>0 há amplificação. |

[DERIVED] A fórmula vazia tem custo zero em toda configuração e é satisfazível, inclusive com zero variáveis. A fórmula cuja única cláusula é vazia tem custo um em toda configuração e é insatisfazível. Esses exemplos decorrem de any, countP e da definição de SAT. As ligações entre a tabela, a soma de custos e os pesos da trava têm conteúdo matemático verificável. As linhas 69, 112 e 118 explicitam as especializações das peças anteriores.

O custo local requer a fórmula, seus literais e a atribuição. Seu trabalho é percorrer as cláusulas e os literais dessa entrada. O existencial sobre as configurações é distinto da contagem global das configurações ou da avaliação de uma partição. Esta pedra, sozinha, não fornece decisor determinístico com contagem de passos polinomial, testemunha de NP do Mathlib ou identificação universal de toda a matemática com a lei. As pontas existentes são TheEquationOfTruth.lean linhas 24–26 e TraducaoTuring.lean linhas 123, 476, 1046–1068 e 1075.

O log integral e seu confronto termo a termo com o recibo da gerência estão em lean.log e CONFERENCIA.json.
