# Em qual ramo o Nome ficou inteiro

**[REAL]** Para uma variável marcada, o leitor conserva os rótulos falso e verdadeiro. Quando entra uma cláusula, cada ramo sobrevive se ao menos uma atribuição daquele ramo satisfaz tanto o prefixo quanto a cláusula. Um literal de cada trecho pode usar o mesmo rótulo muitas vezes. A compatibilidade exige que ele receba o mesmo valor em todas as ocorrências.

## A regra de atualização

Escreva `E(P,M)` quando existe uma atribuição que satisfaz o prefixo P e todas as marcas M. Para toda cláusula C, inclusive vazia, o Lean verifica

```text
E(P ∧ C, M)  ↔  existe ℓ em C tal que E(P, M ∪ {ℓ}).
```

Aqui a união significa acrescentar o literal à lista de marcas. Com M composto de `xᵢ=b`, essa igualdade dá o bit do ramo b. A disjunção dos bits devolve a Palavra. Para k positivo e 0 < β < 1, esse mesmo bit equivale a existir no ramo uma atribuição de peso exatamente um, pois o peso é (1−β) elevado a k vezes o número de cláusulas violadas. A existência do ângulo PsiBit que representa o par está em `decode_updated_pair`. A computação das marcas usa bits.

A função executável `search` escolhe um literal por cláusula, transportando os rótulos e conferindo sua consistência. Ela dispensa a tabela de máscaras e decide corretamente qualquer fórmula finita. Se as compatibilidades já estão calculadas e dispostas na fita na ordem dos literais, os dois acumuladores consomem um avanço por literal, seguido de uma transição de término. A produção dessas compatibilidades precisa entrar na conta da fita original. O teorema `diagonal_reads_prefix` mostra que consultar apenas as duas entradas diagonais de uma linha correta já decide a Palavra do prefixo.

## Custos na fita original

L conta cada marca de endereço unário, cada sinal e cada terminador de cláusula no formato `PolinomioPorEscolha.original`. A medida soma deslocamentos de cabeças, incluindo os retornos. «Plana» designa a lista de cláusulas e literais da fonte, com incidências arbitrárias. Os enunciados de custo usam o pivô no endereço zero. A regra lógica acima admite qualquer endereço dentro da fórmula.

| Entradas | Resposta verificada | Movimentos |
|---|---|---|
| Família `coupled k` da revisão anterior, k ≥ 1 | Determina a existência de solução em cada ramo. Com um par, sobrevive só o ramo falso. Com pelo menos dois, ambos. | Exatamente L avanços. Há ainda uma transição final parada. |
| Cada variável diferente do pivô que aparece nos dois sinais ocorre também numa cláusula unitária | Determina a existência nos dois ramos e, portanto, a Palavra. A largura das cláusulas e o número de variáveis podem crescer. | No máximo 7L, em duas passagens, contando a volta do cabeçote de entrada e o trajeto no banco de trabalho. |

A primeira passagem do segundo leitor registra quatro indicadores por endereço visitado. Eles dizem quais sinais ocorreram e quais foram exigidos por cláusulas unitárias. Na segunda passagem cada ramo fixa o pivô no seu valor. Os outros endereços recebem o sinal exigido por uma unitária, quando houver, e o sinal presente quando forem puros. Com unitárias contraditórias, a verificação dos dois candidatos falha, como deve ocorrer. A cabeça de trabalho alcança o endereço lendo os traços da própria fita. A cláusula vê os valores das mesmas variáveis em todas as suas ocorrências.

Para uma fórmula arbitrária, um bit positivo dessa segunda leitura continua fornecendo uma testemunha válida. Um bit negativo informa apenas que a testemunha escolhida falhou, a menos que se saiba que vale a condição da classe. O controle finito encontrou 48 fórmulas satisfatíveis com os dois candidatos falsos entre 624 fórmulas fora da classe. A fórmula (x₁ ∨ x₂) ∧ (¬x₁ ∨ ¬x₂) admite os dois valores do pivô x₀. O leitor das testemunhas escolhe x₁=x₂=verdadeiro e perde ambas. A cota de movimentos desse leitor vale também nessa entrada.

No leitor com guarda, um bit de controle percorre a segunda passagem junto com as duas testemunhas e verifica a condição de cobertura. Um ramo com testemunha recebe `sim`. Na ausência dessa testemunha ele recebe `não` se a guarda passou e `inconclusivo` nos demais casos. A distância total das cabeças continua limitada a 7L. Uma composição exata para fórmulas finitas consulta a busca por literais apenas para os ramos inconclusivos. A cota de 7L cobre o classificador em duas passagens, incluindo a guarda.

Exemplo com o mesmo próximo literal. Tome o pivô x e o segundo endereço y. Os prefixos x↔y e x↔¬y admitem originalmente ambos os valores de x. Acrescente a mesma cláusula unitária (y). No primeiro prefixo só sobrevive x=1 e no segundo só x=0. Cada equivalência escrita em duas cláusulas e acrescida de (y) ocupa 11 letras. O controle das duas cabeças contou 45 deslocamentos em cada uma.

## O que a nova cláusula pode revelar

Há duas CNFs de paridade sobre três variáveis em que, antes da nova cláusula, coincidem as somas de pesos em cada célula de cada par, para qualquer função real do custo. Ao acrescentar a mesma unitária ¬x₂, com x₀=x₁=falso uma relação ainda admite solução e a outra já a perdeu. Com as mesmas unitárias ¬x₀ e ¬x₁ como continuação dos dois prefixos originais, os valores permitidos de x₂ são opostos. As tabelas completas tinham conteúdos distintos desde o início.

Em qualquer número positivo de variáveis, a prova `no_profile_update` também dá um par de prefixos cujas projeções existenciais em **todos** os subconjuntos próprios coincidem. Uma cláusula pode separar as projeções seguintes. O exemplo de paridade tem três variáveis e já admite uma descrição simbólica curta. O resultado delimita o que uma atualização consegue obter se receber exclusivamente as projeções.

## Limite da busca por literais

A contagem instrumentada em `CustoDaBuscaLiteral` conserva a resposta de `search`, inclusive sua parada na primeira escolha que funciona. Para k cópias de (x₀ ∨ x₁) seguidas de (x₂) e (¬x₂), o texto tem 4k+8 letras e essa implementação faz exatamente 2ᵏ verificações de consistência nas folhas. Trata-se da contagem de verificações dessa busca. O exemplo admite um tratamento curto por inspeção das duas unitárias, inclusive pelo leitor em duas passagens.

Há também uma família satisfatível que chega à busca mesmo com a guarda habilitada. Para k ≥ 1, tome k cópias de (x₁ ∨ x₂) e encerre com (¬x₁ ∨ x₃) e (¬x₁ ∨ ¬x₃). As duas cláusulas finais obrigam x₁=falso, pois, se fosse verdadeiro, exigiriam os dois sinais de x₃. Em ambos os ramos do pivô x₀, basta escolher x₂=verdadeiro. O perfil devolve inconclusivo nos dois ramos. A busca que tenta x₁ antes de x₂ em cada cópia faz pelo menos 2ᵏ verificações de consistência em cada ramo, numa entrada de 6k+14 letras. No controle com k=10, foram 74 letras, 374 deslocamentos na etapa com guarda e 4.093 verificações de consistência em cada ramo consultado pela busca. Deduplicar essas cláusulas pouparia trabalho nessa família. O custo exponencial demonstrado pertence à busca implementada com essa ordem de escolhas. Uma verificação de consistência é uma operação da busca, sem equiparação automática a um deslocamento da cabeça.

**[OPEN]** Falta uma regra executável que produza e atualize a compatibilidade de cada ramo com os novos literais, preserve as correlações conjuntas e tenha, no pior caso de toda CNF plana, um único polinômio no número de letras para os movimentos totais. A regra semântica e os dois leitores de fita acima têm provas separadas. As candidatas estão disponíveis para revisão da gerência.

As fontes Lean, os objetos, o compilador, as importações diretas e os controles locais estão vinculados em `RESULTADO.json`. O controle finito usa enumeração como oráculo de conferência. Os leitores de fita recebem somente a grafia original.

