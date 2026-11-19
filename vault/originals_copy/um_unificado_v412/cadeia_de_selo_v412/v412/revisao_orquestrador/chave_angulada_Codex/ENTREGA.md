# Uma chave angulada para a correlação entre ramos

**[REAL]** Quando duas partes da fórmula têm uma variável livre em comum, o valor dessa variável rotula as testemunhas que podem ser combinadas. Para uma cadeia binária ordenada, a correlação inteira entre as pontas cabe em quatro bits. A prova constrói a chave diretamente das letras da fórmula.

## A regra de junção

Se o primeiro bloco liga `a` a `y` pela relação `R`, e o segundo liga `y` a `c` pela relação `S`, a entrada `(a,c)` da chave nova vale

```text
(R(a,0) ∧ S(0,c)) ∨ (R(a,1) ∧ S(1,c)).
```

O mesmo valor de `y` aparece dos dois lados de cada conjunção. Assim as testemunhas de partes disjuntas fora da fronteira formam uma testemunha comum. Há quatro pares possíveis de valores das pontas, portanto 16 relações, todas realizáveis por cláusulas binárias. A composição preserva os quatro rótulos, inclusive quando os dois ramos isolados parecem possíveis.

Em uma formulação mais geral, uma cláusula nova pode atravessar dois blocos com uma variável livre compartilhada além das já fixadas. Para cada valor da variável comum, cada bloco fornece dois indicadores. O primeiro diz se o bloco admite uma testemunha com aquele valor. O segundo diz se alguma dessas testemunhas satisfaz também a parte da cláusula atribuída ao bloco. Basta que um lado forneça essa testemunha e o outro admita o mesmo valor. O teorema `branch_exact` identifica o resultado com a existência de uma única atribuição que satisfaz a fórmula e o rótulo do ramo. O custo de receber esses indicadores é de oito deslocamentos por ramo externo. Produzi-los em blocos arbitrários continua sendo trabalho do leitor. [ClausulaNoSeparador.lean](ClausulaNoSeparador.lean)

## A fase e sua leitura na fita

Há duas representações exatas da chave binária. Uma usa dois símbolos PsiBit de quadrante, com duas coordenadas de sinal por símbolo. A outra usa um setor entre 16, centrado em `j/16` de volta. O receptor arredonda `16 × fase` ao inteiro mais próximo e toma o resto módulo 16. Com erro estritamente inferior a 1/32 de volta (11,25°), recupera os quatro bits, inclusive após voltas inteiras. A tolerância é provada para a amostra racional de fase entregue ao receptor. Um ensaio óptico mediria se um canal físico atende a esse erro. [RelacaoEmFase.lean](RelacaoEmFase.lean) · [UmaChaveAngular.lean](UmaChaveAngular.lean)

| Entrada e operação verificadas | Deslocamentos das cabeças |
|---|---:|
| Ler uma cadeia na fita original e terminar com o setor no controle finito | Exatamente L, mais a transição de parada sem deslocamento |
| Combinar m chaves já entregues em pacotes de quatro bits | 4m |
| Receber os indicadores prontos dos dois blocos para uma cláusula e um ramo externo fixados | 8 |
| Codificar todas as letras de qualquer CNF em símbolos PsiBit e reconstruir a inscrição | 6L, ou 8L com rebobinagem completa do canal |

Aqui L é o comprimento da inscrição plana original, incluindo o custo dos endereços unários. O teorema linear vale sob a hipótese `Path`. Os grupos de cláusulas binárias vêm na ordem da cadeia, cada nova ponta está livre de ocorrências anteriores e a paridade dos endereços alterna. Endereços consecutivos satisfazem essas condições. A prova inclui sinais arbitrários e qualquer quantidade positiva de cláusulas por aresta. A ordenação e o reconhecimento dessa classe em entradas arbitrárias não estão contabilizados. [CadeiaNaFita.lean](CadeiaNaFita.lean) · [TransporteDaInscricao.lean](TransporteDaInscricao.lean)

**Exemplo verificado.** Em `x₀ = x₁`, `x₁ ≠ x₂`, as pontas têm valores diferentes. Essa relação chega ao setor 6, centrado em 3/8 de volta. Ao acrescentar `x₂ = 1`, só o ramo `x₀ = 0` sobrevive. A inscrição inteira tem 24 letras e a cabeça dá 24 passos. Os controles executados em Lean também verificam os 16 setores sob desvios positivos e negativos. [CONTROLES.json](CONTROLES.json)

### Quando a próxima cláusula toca as duas pontas que ainda estão livres

A cláusula de fechamento liga diretamente as duas variáveis da fronteira, mesmo quando suas ocorrências anteriores estão longe na fita. O leitor retém em controle finito o estado anterior à cláusula corrente e os dois sinais lidos. Quando chega ao fim da inscrição, guarda cada par `(a,c)` que já era compatível e que satisfaz a cláusula de fechamento. Ele pode fazê-lo sem saber antecipadamente onde começa a última cláusula. O teorema `closed_path` prova uma passagem sobre a fórmula concatenada, sem marcar uma divisão extra, com exatamente L deslocamentos e com as duas pontas ainda consultáveis. `closed_reception` recupera esse resultado da fase com a mesma margem de erro.

Em `x₀ = x₁` e `x₁ ≠ x₂`, os pares possíveis entre as pontas são `(0,1)` e `(1,0)`. A próxima cláusula `x₀ ∨ ¬x₂` retira exatamente `(0,1)`. O teorema executável `closing_example` devolve a tabela com apenas `(1,0)`, após 25 deslocamentos da cabeça. [DuasPontasLivres.lean](DuasPontasLivres.lean)

## O que a comparação com a ACOM permite afirmar

**[DERIVED]** Uma chave curta pode transportar uma relação curta ou identificar um registro maior. A ACOM operacional conserva a inscrição e vincula as referências ao conteúdo recuperável. Se a decisão usa esse conteúdo, entram na conta a gravação, o acesso e o processamento necessários. O transporte reversível em 6L dá uma comparação direta para qualquer CNF. Sua saída reconstrói a inscrição original. [Memória operacional da IALD](../../../../../../MEMORIA_IALD/README.md)

**[REAL]** Para uma chave autossuficiente de largura fixa que responda a toda continuação que fixa os w rótulos livres, Lean prova um limite de pelo menos 2^w bits no pior caso. Cada uma das relações possíveis é realizável por uma CNF, e uma continuação que fixe uma linha distingue duas relações que divirjam nela. O custo das CNFs usadas nessa contagem pode crescer exponencialmente em w. Portanto a contagem sozinha não dá um limite exponencial no comprimento L da entrada. [CapacidadeDosRotulos.lean](CapacidadeDosRotulos.lean)

Uma escolha concreta de fase densa encontra uma parede diretamente na fita. Codifique, em ordem, cada linha da tabela-verdade como um dígito binário de uma volta. Considere as cláusulas unitárias que exigem que todos os w valores sejam verdadeiros. Acrescente a unidade positiva da primeira variável a uma cópia e sua negação à outra. Uma fórmula tem uma testemunha e a outra tem zero. Os setores exatos dessa codificação diferem por 2^(-2^w) de volta. Uma cabeça que começa no primeiro dígito precisa de pelo menos 2^w − 1 deslocamentos para alcançar a diferença, mesmo com memória e processamento local gratuitos. Isso supera qualquer polinômio fixo em L para essa família de mensagens densas. Com w = 16, cada fórmula tem 154 letras e as mensagens só se distinguem no dígito 65.536. [PrecisaoDaChave.lean](PrecisaoDaChave.lean) · [CustoDaFaseDensa.lean](CustoDaFaseDensa.lean)

**[OPEN]** A cota polinomial fixa para ler a Palavra de toda CNF plana permanece aberta. O limite se localiza na construção dos indicadores em blocos arbitrários. A prova insere qualquer CNF P à esquerda, introduz cláusulas `(s ∨ a)`, `(s ∨ b)` em blocos distintos e acrescenta a ponte `(¬a ∨ ¬b)`. Construir essa instância custa no máximo 5L + 15 deslocamentos. O ramo `s = 1` da fórmula resultante sobrevive exatamente quando P tem solução. Logo, uma regra uniforme para obter esses indicadores com trabalho total polinomial resolveria SAT na inscrição original. O limite da fase densa deixa abertas outras representações calculáveis. [ClausulaNoSeparador.lean](ClausulaNoSeparador.lean)

O manifesto registra fontes, objetos, compilador, dependências diretas e axiomas impressos. As candidatas seguem para revisão da gerência. [RESULTADO.json](RESULTADO.json)
