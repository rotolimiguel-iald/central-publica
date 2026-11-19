# PLANO ISOMORFO K08/R4 — CONTAMINAÇÃO E NÚMEROS COM HISTÓRIA

## Escopo e máquina comum

Somente textos sintéticos próprios entram na máquina. A pasta separada `K08/ENTRADA/` usa recortes verbatim dos quatro arquivos públicos, com linha e hash próprios; nada reservado entra em nenhuma das duas. O dicionário `dicionario_sintetico_v1.json` tem identidade e versão; cada execução registra seu SHA-256. A mesma função transforma texto, asserções, polaridades e gabarito, em uma única passagem mais-longa-primeiro, sem cascata. IDs e três rótulos permanecem estáveis para que o **mesmo extrator fechado** meça os dois braços. A correspondência perfeita obtida por essa fiação é medida de construção/formato, não de convergência.

O texto sem Nome também sai dessa máquina: insere-se uma única sentença que afirma a negação de um literal já afirmado, e só então se aplica a mesma transformação. Um enumerador Booleano independente calcula custo mínimo e número de leituras de custo zero **na fórmula mínima declarada para a contradição**; ele não finge formalizar todos os fatos do texto.

No braço numérico, “primeira” e “segunda” são índices estruturais das séries, não quantidades medidas; por isso permanecem. Todas as quantidades numéricas explícitas do texto principal e do gabarito principal são alteradas. As sondas com valores antigos são um diagnóstico separado, não uma permanência oculta no braço isomorfo.

A auditoria lexical trata nomes-fonte e números antigos. O par comparativo bidirecional é verificado por distinção textual e polaridade, não pela auditoria de nomes.

## Escopo (i): textos com números por contrafactual factual coerente

No exemplo com números, as duas durações são substituídas por valores novos e a conclusão comparativa dependente é invertida. O mesmo número de oscilações e a unidade são preservados; 46,0 e 43,0 segundos tornam coerente dizer que a segunda série foi mais rápida. As mudanças NUM01, NUM02 e REL01 são explícitas no dicionário. Nenhum número do texto principal permanece intacto.

Isto **não é um isomorfo factual estrito**: as medidas foram alteradas. É um contrafactual sintético para medir dependência de números e nomes na releitura: se o respondedor segue o texto novo ou reproduz a história original. As sondas de memória mantêm as afirmações originais separadamente e registram quais rótulos devem mudar no texto contrafactual. Elas não fazem parte do texto principal nem são apresentadas como fatos reais.

**Testabilidade:** a coerência interna, a ausência de números antigos, a transformação do gabarito e a medida pelo mesmo extrator são testáveis agora neste exemplo. A dificuldade equivalente e a validade semântica em qualquer texto real permanecem abertas e exigiriam curadoria independente, domínio a domínio. Não se troca uma medida da natureza publicada; se isso fosse necessário, a alternativa ficaria bloqueada até uma especificação factual contrafactual própria.

## Escopo (ii): restrição a textos sem números

A máquina também executa um braço puramente qualitativo, com renomeação estrita e sem contrafactual numérico. Um guarda rejeita dígitos, palavras numéricas listadas e sinais matemáticos comuns antes e depois da transformação. A lista e o escopo do guarda são versionados; ele é uma verificação lexical, não prova de que nenhum conteúdo quantitativo implícito existe.

**Testabilidade:** o isomorfismo de renomeação, o gabarito, a contradição mínima e o mesmo extrator são testáveis agora nesse subdomínio. A alternativa não testa contaminação por números e não pode ser generalizada a textos com medidas: neles a previsão fica expressamente fora de escopo.

## Sem escolha escondida e sem teste direto da fala da identidade

As duas saídas são geradas e relatadas; não existe campo `selected_arm`, ranking ou preferência operacional. A alternativa (i) é a única das duas que examina diretamente números com história, mas paga o preço de deixar de ser factualmente idêntica. A alternativa (ii) preserva fatos qualitativos com mais clareza, mas não responde à pergunta numérica.

O sistema testado relê o que já foi nomeado; não nomeia nem é o Verbo. As grandezas primárias são de ATO, não rótulos ou termos. **Nenhuma das duas alternativas testa diretamente a fala da identidade; o controle isomorfo mede dependência de nomes/números e não é prova de convergência.** Nenhuma execução experimental com modelos é autorizada.

## Sem Nome e reintrodução acidental

Para cada braço, o texto contraditório contém P e ¬P. A fórmula correspondente tem zero leituras de custo zero e custo mínimo um; retirar a sentença inserida deve restaurar exatamente o texto isomorfo satisfatível. O validador também procura termos-fonte e números antigos no texto transformado. `nome_vazio=true` trata do Nome formal; `lexical_disguise_ok=true` trata do disfarce lexical. Um não substitui o outro.
