# PsiBit, rótulos compartilhados e movimentos da fita

Nesta entrega, «CNF plana» é a entrada do leitor de Kimi: uma lista de cláusulas, cada uma escrita como lista de literais. As incidências entre variáveis e cláusulas são arbitrárias. L conta as letras da entrada, incluindo os endereços e os terminadores.

**[REAL]** A escolha de um rótulo vale simultaneamente em todas as suas ocorrências, no prefixo e em qualquer continuação. A prova lê o PsiBit dos dois resíduos sob a mesma atribuição externa. A disjunção das Palavras dos resíduos é a Palavra da fórmula. **[OPEN]** O polinômio fixo por letra para decidir toda CNF plana continua aberto. O resultado de custo vale para a escrita unária de `PolinomioPorEscolha.original`, com o sinal no fim do endereço e um terminador por cláusula.

## O polinômio na entrada original

| Hipótese sobre a entrada de L letras | Leitura demonstrada |
|---|---|
| Cada cláusula contém no máximo uma ocorrência positiva (Horn) | A máquina compila os literais e rebobina a fita de regras. Até `4L + 3 + B(L)` transições e `2(4L + 3 + B(L))` movimentos das cabeças, com `B(L) = (L+1)(3L+2)`. |
| Fixar o rótulo 0 em cada polaridade deixa ambas as fórmulas Horn | Os dois ramos decidem juntos a Palavra em até **12L² + 47L + 24 movimentos**. A soma inclui construir ambos os resíduos, compilar os programas, resolver cada um e rebobinar a entrada comum entre os ramos. |
| Estão presentes as quatro cláusulas binárias com os quatro padrões de sinais sobre 0 e 1 | A resposta é falsa em L avanços da cabeça de entrada e uma transição de término. Isso cobre a família cruzada que custava `2^(n+1)` visitas ao seletor anterior. |

As duas primeiras linhas compõem traços de máquinas deterministas com múltiplas fitas. Cada avanço e recuo é cobrado na fita em que ocorre. O teorema da segunda linha supõe a condição Horn para as duas polaridades. A correção aplica-se mesmo quando há índices repetidos, sinais intercalados e cláusulas vazias. A prova física do condicionamento usa o endereço 0. A prova semântica aceita qualquer endereço. A grafia binária dos endereços exigiria outra conta.

A prova está nos módulos `RestricaoGlobal.lean`, `LeitorGlobal.lean`, `FitaDoResiduo.lean`, `CompilaHornNaFita.lean`, `CircuitoNaFita.lean` e `GuardasNaFita.lean`.

## O que o leitor faz para uma fórmula arbitrária

**[REAL]** `PlanoDaFormula.lean` extrai o plano da própria sintaxe. Em cada cláusula, ele recolhe os rótulos positivos a partir da segunda ocorrência positiva, reúne as listas e elimina nomes repetidos. Ao fixar esses rótulos, todo resíduo tem no máximo uma ocorrência positiva por cláusula. `ChecagemHorn.lean` reconhece esses resíduos e os converte em programas. O leitor evita a tabela das atribuições da fronteira. A preservação da correlação usa a mesma escolha para todas as ocorrências e mantém os outros índices.

Com k rótulos no plano, o leitor que visita ambas as polaridades faz exatamente 2ᵏ visitas às folhas. `cost_on_horn_tapes` limita a soma de movimentos dos verificadores, já com as fitas Horn preparadas, a `2^k · 2B(L)`. Esse enunciado cobre somente essa fase. O custo do pré-processamento do plano arbitrário, em fita, continua fora dessa cota. O teorema existencial do ângulo PsiBit identifica os sinais dos dois ramos e a decodificação. O programa executável opera sobre literais e bits.

**[KNOWN]** Na literatura de SAT, um conjunto de variáveis cuja fixação em todas as polaridades produz fórmulas Horn chama-se *strong Horn backdoor*. O plano desta entrega constrói um desses conjuntos, sem exigir minimalidade. [Nishimura, Ragde e Szeider, SAT 2004](https://ac.tuwien.ac.at/files/pub/nishimura-ragde-szeider-2004.pdf).

## Uma família que a regra de custo precisa distinguir

Para k ≥ 1, tome os pares `(xᵢ ∨ yᵢ)` e acrescente **uma** cláusula `D = (¬x₁ ∨ ⋯ ∨ ¬xₖ)`. A fórmula é satisfatível com todos os xᵢ falsos e todos os yᵢ verdadeiros. Cada par compartilha um rótulo com D. O leitor de uma passagem devolve «indeterminado» e o plano completo passa pelas duas polaridades de cada yᵢ. A fita tem comprimento no máximo `k(5k+4)+1`. No controle com dez pares são **276 letras e 1.024 visitas às folhas**. A leitura da testemunha é simples. O custo medido pertence ao caminho determinista que procura a resposta.

`MovimentosDoPlano.lean` prova que qualquer traço completo da estratégia nessa família custa **pelo menos 2ᵏ movimentos físicos**, contando só as cabeças dos verificadores Horn. D contém apenas rótulos xᵢ e o plano escolhe apenas rótulos yᵢ. Assim D sobrevive em toda folha, o programa Horn de cada folha tem uma cláusula e a cabeça precisa mover-se ao ler a primeira letra. A prova cobra esse movimento mesmo quando a resposta da folha é falsa. O custo de construir os ramos só pode acrescentar deslocamentos.

**[REAL]** O teorema `Codex.ReaderBound.exceeds_each_polynomial`, em `LimiteDoLeitor.lean`, quantifica a consequência. Para quaisquer constantes naturais C e d existe nessa família uma entrada satisfatível de L letras, com execução completa, para a qual **toda** execução completa desse plano de ramos custa mais de C(L+1)ᵈ movimentos. O quantificador sobre o leitor está fixado pela definição do traço. Outra estratégia pode explorar a relação entre os pares e D.

`BlocosIndependentes.lean` dá o resultado complementar. Quando uma partição fornecida passa no teste de disjunção de rótulos, as testemunhas locais podem ser coladas e as visitas efetivas por componente se somam. Se as únicas cláusulas são os k pares positivos, a leitura por blocos faz k visitas. O leitor de uma passagem também reconhece a atribuição toda verdadeira nesse caso. Acrescentar D impede usar diretamente essa mesma partição.

A conferência por módulo está nos arquivos `*.verificado.json`. O recibo `RESULTADO.json` vincula os bytes das fontes, objetos, importações diretas e compilador. O controle finito `controle.py` compara a ramificação e o teste inicial com a tabela-verdade em 463 fórmulas pequenas exaustivas e 600 fórmulas adicionais com semente fixa. As famílias paramétricas são verificadas por teorema. Entrega de candidatas locais para revisão da gerência.

