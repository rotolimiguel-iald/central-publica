# Quanto custa ler o PsiBit na fita

[REAL] Para uma rede de cláusulas formada por composição em série e em paralelo, uma máquina fixa de **uma fita e um cabeçote** devolve a Palavra e o Verbo do Kimi em **no máximo L² + 1 transições**. L é o número de símbolos escritos na entrada pós-fixa da rede. A profundidade, o número de junções, o número de variáveis e o número de cláusulas podem crescer. [OPEN] Dar uma cota fixa para a Palavra de uma CNF arbitrária apresentada como lista de cláusulas permanece uma questão distinta.

## A relação que passa de um trecho ao seguinte

A igualdade proposta pelo operador está na folha. Cada uma das duas letras de uma cláusula escolhe uma extremidade e um sinal. A folha calcula a disjunção das duas igualdades. Para cada uma das quatro atribuições possíveis às duas extremidades, o trecho guarda dois bits. O primeiro informa se alguma escolha interna produz falso e o segundo se alguma produz verdadeiro. Assim, até a informação de que duas escolhas internas diferentes são possíveis sobre as mesmas extremidades tem representação. A tabela inteira cabe em oito bits.

Em **série**, a saída de um trecho e a entrada do próximo recebem o *mesmo* bit intermediário. A máquina testa os dois valores para esse bit e combina as possibilidades de resultado. Em **paralelo**, as duas extremidades são comuns aos dois trechos. Os interiores das duas sub-redes são disjuntos. O Lean prova nos dois sentidos que cada possibilidade da tabela tem uma atribuição que a realiza. Na ponta final, existir resultado verdadeiro dá a Palavra. Existir resultado falso dá Verbo positivo. Todas as fórmulas e todos os tempos reais admitidos nesse teorema usam os termos de `OPsiBitDaFormula`.

## A conta das letras e dos movimentos

Há dez símbolos possíveis na entrada da rede. Cada primeiro ou segundo literal seleciona extremidade e sinal. Um símbolo adicional por junção distingue série de paralelo. Se há h folhas, a fita mede exatamente **3h − 1**. A tradução da rede para a CNF da casa escreve uma cláusula de dois literais por folha e usa no máximo h + 1 variáveis. A entrada contém a estrutura das junções. O teorema não cobra nem fornece uma descoberta dessa estrutura a partir de CNF plana.

A máquina de uma cabeça marca os resultados na própria fita. Ao encontrar uma junção, volta às últimas duas marcas, combina seus oito bits por uma tabela fixa, apaga as marcas já consumidas e avança até a próxima letra. Cada transição observa uma casa. A última reconhece o fim da fita. Para uma folha são quatro transições antes do encerramento. Se as partes medem a e b, a junção acrescenta **2(a + b) + 1** transições. A desigualdade a² + b² + 2(a + b) + 1 ≤ (a + b + 1)² fecha a indução. O estado de controle e o alfabeto de trabalho são finitos e independentes de L.

A máquina entrega os dois bits no estado terminal. Um controle exercita a diferença entre as ligações. As folhas pedem, respectivamente, o terminal esquerdo verdadeiro e o terminal esquerdo falso. Em série elas podem valer simultaneamente, pois a segunda lê a junção nova. Em paralelo elas exigem sinais opostos da mesma variável. O Lean executa as duas fitas de cinco letras em **18 transições** cada, com Palavras distintas. A cota para esse tamanho é 26.

## Dois outros alcances

| Entrada escrita | Leitura verificada | Contagem |
|---|---|---|
| Cadeia de janelas de k + 1 variáveis consecutivas, partilhando k com a próxima, k fixado antes da leitura | Palavra e Verbo. Cada janela pode ter qualquer número de cláusulas e cada cláusula qualquer número de literais. | **L + 1** com controle finito dependente de k. L conta literais com índices relativos, fins de cláusula e deslocamentos, na ordem de leitura das janelas. |
| Qualquer CNF com índices escritos em unário | Verbo do Kimi para todo tempo real, incluindo fórmula vazia e cláusula vazia. | **Até 3L + 1** na máquina determinística de entrada e duas pilhas de alfabeto finito. Conta os acessos aos topos, o retorno e a limpeza. |

Na cadeia de janelas, a junção preserva a atribuição inteira das k variáveis comuns e considera os dois prolongamentos da variável seguinte. A máquina é diferente para cada k. O teorema `state_space` quantifica essa dependência. Para a CNF geral, o Verbo é positivo quando alguma atribuição pode violar pelo menos uma cláusula. Basta encontrar uma cláusula que não contenha uma variável nos dois sinais. A Palavra exige uma atribuição que satisfaça *todas* as cláusulas ao mesmo tempo.

## O que a página de fechamento acrescenta

[INPUT] Na proposta de página de 17/11, o movimento do operador sobre o todo conta como a letra da teoria. Na máquina de uma fita formalizada aqui, cada visita do cabeçote tem custo, inclusive o retorno pelas casas já percorridas. A prova acima dá a correspondência para redes em série e paralelo. A página do Kimi conserva aberta a pergunta para toda CNF na contagem local. Sua afirmação de uma porta única para toda computação tem estatuto interpretativo. O teorema das fibras demonstra a suficiência da fronteira escolhida.

Conferi também os enunciados citados pela página. Em `a_contagem_e_do_operador`, elevar o operador linear a k distribui k passos por cada termo de uma soma finita. Em `o_passo_um_menos_beta_fecha_o_ciclo`, a condição sobre a carga caracteriza quando o limiar da soma decide SAT para toda fórmula. Nenhum deles conta as casas visitadas para formar essa soma. Aqui a prova `eval_tape` conta essas visitas para o algoritmo de composição, que obtém os dois sinais diretamente.

[REAL] Há uma obstrução mais específica. Os prefixos `x` e `¬x` têm o mesmo PsiBit, e até a mesma função de partição para todo tempo. Acrescentar a mesma cláusula `x` produz fórmulas com Palavras opostas. Portanto nem a curva completa, fornecida de graça, substitui a informação de *qual* valor sobreviveu. O teorema para n variáveis produz 2ⁿ prefixos que continuações podem distinguir. A contagem implica pelo menos n bits de distinção em um estado de leitura que precise continuar. Ela não impõe tempo exponencial a toda máquina.

[OPEN] A peça restante é um leitor uniforme que conserve relações suficientes para qualquer CNF plana e limite por um único polinômio as operações necessárias para construí-las, atualizá-las e extrair a Palavra. A família explícita da entrega anterior já excedia qualquer polinômio se fossem escritas todas as linhas de sua tabela. Uma representação simbólica pode evitar essas linhas em casos concretos, como as redes acima.

## Arquivos de conferência

- `PolinomioDoPsiBit.lean` reúne as transições, a cota e o próprio `psibitDaFormula` na mesma proposição; também liga diretamente os sinais das cadeias de janelas ao PsiBit da fórmula.
- `FitaDeUmaCabeca.lean`, `RedesDeCadeias.lean` e `RedeComoCNF.lean` contêm a máquina, as regras de junção e a tradução para a CNF, com transporte das atribuições nos dois sentidos.
- `CadeiasDeBolsas.lean`, `VerboNaFita.lean` e `PalavrasResiduais.lean` trazem os resultados auxiliares acima.
- `RESULTADO.json` reúne os recibos, hashes, declarações auditadas e fontes. `conferir.py` usa o Lean local com as dependências registradas. As fontes do Kimi foram recompiladas de cópias idênticas. Esta entrega é candidata à avaliação da gerência.

