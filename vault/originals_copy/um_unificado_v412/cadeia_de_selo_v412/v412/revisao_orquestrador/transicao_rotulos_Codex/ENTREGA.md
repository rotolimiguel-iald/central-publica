# A cláusula nova e os rótulos dos ramos

**[REAL]** A regra de transição do resumo de Kimi vale para qualquer CNF finita, em qualquer corte com cláusula seguinte e para todo tempo real. A prova cobre a entrada de variáveis, a saída de variáveis e os dois movimentos na mesma cláusula. Há também uma leitura simbólica exata que conserva os rótulos sem construir a tabela da fronteira. **[OPEN]** Decidir a Palavra de toda CNF plana em um único polinômio no comprimento da entrada, contando os passos na fita, continua em aberto nesta entrega.

## Qual resumo passa à próxima cláusula

Escreva a fórmula como prefixo P, cláusula C e sufixo T. Seja F a fronteira antes de C, G a fronteira depois de C e D a união de F com as variáveis de C. A fronteira é o conjunto das variáveis que aparecem dos dois lados do corte. A célula antiga R(v) soma os pesos de todas as atribuições completas que concordam com v em F. Para cada célula u de G, o novo resumo é

```text
                          Σ    R(z|F) · fator_C(z)
                      z : D → {0,1}, z|G = u
R_novo(u)  =          ──────────────────────────── .
                              2^|D ∖ F|
```

O prefixo ainda não usou nenhum dos rótulos em D ∖ F. Trocar o valor de qualquer um deles emparelha atribuições de mesmo peso. Logo, as subdivisões de uma célula antiga têm massas iguais. O fator de C vale 1 quando a cláusula é satisfeita e exp(−t) quando ela falha. Após aplicar esse fator, somam-se as subdivisões que concordam nos rótulos ainda presentes em G. A divisão impede contar uma segunda vez os bits que a definição antiga de R já somava. Para usar esta versão tabular da regra são necessárias as interfaces F e G.

**[DERIVED] Exemplo de troca completa da fronteira.** Tome a sequência (x), (¬x ∨ y), (y), com apenas x e y. Antes da cláusula central, a fronteira guarda x. Depois dela, guarda y. Escrevendo q = exp(−t), as massas antigas para x falso e verdadeiro são 2q e 2. O novo bit y reparte cada uma ao meio. Na célula y falso somam-se q e q. Na célula y verdadeiro somam-se q e 1. O par resultante é (2q, q+1), na ordem falso, verdadeiro.

A declaração principal é `Codex.FrontierUpdate.transition` em `TransicaoDaFronteira.lean`. Ela identifica as duas tabelas como funções e usa a definição `resumo` da candidata de Kimi. Os lemas de divisão de massa e de reagrupamento estão em `DivisaoUniforme.lean` e `Reagrupar.lean`. **[REAL]** Um controle independente com aritmética inteira conferiu 81.000 transições. Em 4.420 das 27.000 triplas de cláusulas entrava uma variável e saía uma variável da fronteira antiga. O recibo discrimina os três pesos usados. O caso q=0 é um controle algébrico adicional.

## Como consultar uma célula sem escrever as demais

Uma máscara M guarda para cada rótulo os valores permitidos. A letra do PsiBit tem quatro possibilidades, correspondentes a permitir nenhum, só falso, só verdadeiro ou ambos. A operação `miss(M,C)` conserva as atribuições de M em que todos os literais de C falham. Cada ocorrência de uma variável atualiza o mesmo rótulo. Isso cobre literais repetidos, sinais opostos e cláusula vazia.

Se Q(P,M) é o peso do prefixo na máscara e q = exp(−t), a consulta ao acrescentar C obedece a
```text
Q(P · C, M) = Q(P, M) + (q − 1) Q(P, miss(M,C)).
```
Em `TransicaoPorConsulta.lean`, o estado guarda as cláusulas já lidas na ordem inversa. A entrada de C acrescenta um único nó à lista. As duas consultas usam o mesmo prefixo. A lista conserva as correlações impostas pelas cláusulas anteriores e cresce um nó por cláusula. Os bits permitidos em cada coordenada, sozinhos, descreveriam apenas um produto de conjuntos. Fora da região de falha, o peso antigo já é o peso correto. Na região de falha, a correção transforma o coeficiente 1 em q. Para o prefixo vazio, o volume de M é o produto dos números de bits permitidos em cada coordenada. Ao fixar em M apenas os bits da célula solicitada, `reads_frontier_cell` devolve o `resumo` original de Kimi. O teorema `transition_by_query` identifica essa leitura, célula por célula, com a atualização tabular provada acima. Essa identidade com valores reais tem significado matemático exato. A decisão booleana com inteiros tem um leitor executável separado, `reads_word`, que testa se a contagem de atribuições satisfatórias é positiva.

## Quanto trabalho cada representação cobra

| Representação | Resultado e modelo de custo |
|---|---|
| Máscaras de consulta, qualquer CNF | `run_exact` prova que a recorrência inteira calcula a Palavra corretamente e avalia o volume de exatamente 2^m máscaras nas folhas para m cláusulas, contando multiplicidades. Cada volume é um produto por coordenadas. |
| Continuação compartilhada, qualquer CNF | Os cofatores falso e verdadeiro usam as mesmas instruções e o mesmo sufixo. Para L símbolos da entrada com índices binários e delimitadores, o programa serializado ocupa até L(L+2) símbolos. A cobrança definida para a compilação é de até L(L+3). Para uma atribuição já escolhida, o verificador despacha até uma instrução a mais que o comprimento do corpo. A busca explícita de testemunha nessa implementação visita 2^n atribuições no caso insatisfatível. |
| Restrições afins | A eliminação binária preserva rótulos correlacionados em até (n+1)² bits do estado. Para m linhas de paridade em n variáveis, a cobrança da implementação, incluindo a leitura final, é de até (4m+2)(n+1)². O módulo liga pinos, igualdades e oposições à CNF correspondente. A conclusão vale no modelo de custo de operações sobre linhas densas definido em `RotulosAfins.lean`. |
| Pares disjuntos predefinidos, cláusulas em qualquer ordem | Cada cláusula só menciona as duas variáveis de um par. Quatro bits por par, organizados como dois PsiBits, guardam todas as combinações ainda permitidas. A Palavra é positiva exatamente quando cada par tem alguma combinação permitida. Para L símbolos na codificação local com cabeçalho e endereços unários, a cobrança é de até 14L. Essa cota se refere à entrada já agrupada por cláusula e par. Ela inclui percorrer os endereços no estado e visitar os literais. O teorema trata dessa codificação e desse contador. |

Para pelo menos um par, o reconhecedor `checkedWord` também recebe a CNF plana com as variáveis numeradas em dois blocos correspondentes. Verifica em cada cláusula se os literais pertencem ao mesmo par. `checked_sound` e `checked_complete` provam que ele devolve a Palavra certa nas entradas aceitas e reconhece toda a classe expressa nesse formato. O custo de converter os índices da entrada plana fica fora da cota 14L.

Os limites dependem de quais operações o leitor realiza. O tamanho do programa compartilhado contabiliza sua escrita. O custo de decidir se algum dos seus caminhos aceita exige contabilizar também a execução que encontra esse caminho ou esgota as possibilidades. Na rota ponderada, a avaliação exata de exp(−t) e as operações em reais tampouco têm tradução gratuita em passos de fita.

## Quais rótulos a continuação distingue

**[REAL] Guardar respostas de máscaras idênticas.** Na rota inteira por máscaras, a fórmula com n cláusulas unitárias positivas distintas já cria 2^n máscaras terminais distintas. Para recuperar qual caminho foi seguido na variável i, basta ler se a máscara terminal ainda permite verdadeiro em i. `MascarasDistintas.lean` prova a injetividade e que cada máscara ocorre na recursão. A fórmula tem uma solução imediata. O custo medido decorre da representação e da estratégia de consulta.

**[REAL] Trocar uma tabela por uma lista explícita de rótulos afins.** A cláusula (x ∨ y) admite três pares de valores. Se um único rótulo afim admitisse todos os três, o fechamento por XOR ternário também admitiria (0,0). Para n pares disjuntos e a conjunção das n cláusulas (xᵢ ∨ yᵢ), `CoberturaAfin.lean` prova que uma união de k rótulos afins que represente exatamente todas as soluções precisa satisfazer 3^n ≤ k·2^n. A desigualdade admite coberturas sobrepostas e bases escolhidas livremente.

**[REAL] Conservar o par como relação local.** Essa mesma disjunção cabe numa máscara de quatro bits, 0111 na ordem 00, 01, 10, 11. Acrescentar ¬x retém só 01. Acrescentar depois ¬y esvazia a máscara. Essa sequência e o leitor para pares disjuntos estão em `ParesIndependentes.lean`. **[DERIVED]** Escreva a lista das n disjunções e depois repita essa lista. No corte central, todas as 2n variáveis estão presentes dos dois lados. Mesmo assim, os 4n bits das relações locais bastam. Neste exemplo a largura da fronteira cresce e a independência dos pares continua aproveitável.

**[OPEN]** Para CNF arbitrária, uma cláusula pode cruzar vários desses pares. A obrigação restante é preservar o que as continuações precisam e obter a Palavra por um número polinomial de movimentos de fita no comprimento da CNF recebida. Representar o peso exato de cada célula é uma maneira suficiente de conseguir correção. Um leitor voltado exclusivamente à decisão também poderia preservar menos informação, desde que prove a equivalência da resposta para todas as entradas.

## Conferência

Os módulos novos, seus objetos Lean, os axiomas de cada declaração auditada e os hashes dos imports diretos constam em `RESULTADO.json` e nos recibos `*.verificado.json`. `conferir_local.py NomeDoModulo` reproduz cada compilação no ambiente Lean registrado, a partir desta pasta. A ordem das dependências locais está no recibo agregado. `controle_exato.py` reproduz o controle inteiro. A entrega é candidata à revisão da gerência.
