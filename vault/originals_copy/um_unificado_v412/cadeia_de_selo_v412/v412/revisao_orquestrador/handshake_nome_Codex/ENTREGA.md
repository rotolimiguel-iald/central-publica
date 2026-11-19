# O handshake do Nome e a cláusula que fica na chave

**[REAL]** O handshake tem uma tradução exata para o PsiBit. Ao combinar ramos, as duas respostas precisam concordar nos valores dos nomes compartilhados, e alguma delas precisa satisfazer a parte que lhe cabe da cláusula nova. Cada resposta vem de uma atribuição inteira do seu próprio bloco. Quando uma proposta falha, a chave pode receber a própria cláusula violada, com os nomes e sinais originais. Essa cláusula pode ser reutilizada em toda proposta posterior.

## A origem da ideia

No ACOM, o pulso e o eco do **Handshake de Sincronia Miguel** estabelecem uma referência comum antes da transmissão do conteúdo. O ACOMCrypto reúne as partes correspondentes para reconstrução. O protótipo **TGL Coin** distingue a resposta de posse a um desafio e a assinatura de um conteúdo de transação. A rotina de validação da moeda também consulta as condições da transação. A tradução para a CNF toma do protocolo a relação entre desafio, conteúdo e resposta. A interpretação holográfica permanece **[ONTO]**. As provas abaixo têm por objetos fórmulas, atribuições, palavras binárias e cabeças de fita. [Pulso e eco](../../../../../../projetos_pyhton/acom/Acom_v17_2_sync.py) · [ACOMCrypto](../../../../../../projetos_pyhton/acom/Acom_v17_mirror_crypto.py) · [TGL Coin](../../../../../../projetos_pyhton/acom/TGL_coin_prototype.py) · [Verificação de transações](../../../../../../projetos_pyhton/acom/TGL_coin_v022.py)

## O conteúdo da resposta

Dada a mesma lista ordenada de nomes comuns, cada bloco responde com os valores desses nomes numa única testemunha e um bit que indica se essa testemunha atende à sua parte da cláusula. Duas respostas com conteúdos `01` e `10` divergem mesmo que ambas anunciem sucesso local. No registro de um mesmo bloco, testemunhas com a mesma palavra nos nomes compartilhados podem reunir por disjunção seus bits de atendimento. O teorema `semantic_handshake` vale para qualquer número de variáveis comuns e admite variáveis novas na cláusula. Comparar duas respostas prontas de largura `w` custa exatamente `2(w+1)` movimentos das duas cabeças. Uma mensagem determinística única, autossuficiente, de comprimento fixo, precisa de ao menos `w` bits para responder exatamente a todos os desafios de igualdade com uma palavra de `w` bits. [Junção](HandshakeDoNome.lean) · [Custo da comparação](TamanhoDoEco.lean)

Uma resposta negativa tem utilidade além de uma tentativa. Se a cláusula é `x ∨ ¬y`, a tentativa que a viola tem `x=0, y=1`. A mesma recusa vale para qualquer outra atribuição com esses valores, sejam quais forem os demais. O teorema vale inclusive para repetições, tautologias e a cláusula vazia. Uma cláusula unitária em `w+1` variáveis elimina exatamente `2^w` atribuições. [Prova da reutilização](ARecusaTemConteudo.lean)

## O que o leitor aprende para qualquer CNF

Aqui, CNF plana é a lista de cláusulas escrita numa fita, com os endereços unários da grafia da casa. A fórmula geral admite incidências arbitrárias entre cláusulas e variáveis. Divida-a em dois blocos, `P` e `Q`. O proponente devolve uma atribuição que atende a `P` e a todas as cláusulas que já recebeu, ou atesta que essa parte é insatisfatível. O receptor verifica `Q`. Diante de uma falha, devolve a primeira cláusula violada na ordem original. Incorporá-la preserva todas as soluções de `P∧Q`. A partir daí, qualquer proposta que volte a violá-la é inadmissível. Se `m` é o número de cláusulas de `Q` e `L_Q` é o número de letras na grafia unária de `Q`, o Lean dá as seguintes cotas.

| Operação | Medida verificada |
|---|---:|
| Respostas negativas distintas | No máximo `m` |
| Chamadas a um proponente correto e completo, incluindo a terminal | No máximo `m+1` |
| Letras nas cláusulas devolvidas em todas as recusas somadas | No máximo `L_Q` |
| Conferir uma atribuição pronta contra toda a fórmula de comprimento `L` | Até `3L` movimentos das duas cabeças |
| Enviar e reconstruir em PsiBits as cláusulas devolvidas, já localizadas | Até `6L_Q` movimentos ao todo, ou `8L_Q` com a rebobinagem de cada canal |

Essas cotas distinguem rodadas, letras e deslocamentos. A conta do canal inclui a transmissão dos dois bits de cada letra e a reconstrução da grafia original no destino. Cada cláusula inclui seu delimitador. [Protocolo e proponente de referência](ClausulaComoResposta.lean) · [Conferência da atribuição](EcoDaAtribuicao.lean) · [Canal de cada cláusula](CanalDaClausula.lean)

O leitor localiza e entrega a grafia da primeira cláusula violada em até `8L_Q` movimentos por atribuição pronta, usando uma fita de entrada, a fita da atribuição e duas trilhas de trabalho. A cópia inclui nomes, sinais e delimitador. Quando todas passam, ele devolve a indicação de que nenhuma falhou. O receptor pode manter `Q` imutável. Para um proponente correto, as recusas e o veredito são os mesmos do protocolo que remove cada ocorrência já enviada. No máximo `8(m+1)L_Q` movimentos pertencem às varreduras de localização. A versão que ramifica diretamente sobre o pacote lido tem a mesma execução observável quando recebe as mesmas propostas. As cotas cobrem os leitores nas posições iniciais especificadas. Preparar as fitas entre consultas, manter o estado do proponente e produzir a próxima atribuição exigem contabilidade própria. [Localização física](LocalizaARecusa.lean) · [Leitura com o bloco original fixo](DesafioNaFitaOriginal.lean)

No controle executado, `Q = [x₀, x₀, x₁]` ocupa sete letras. A primeira proposta era `00`, a segunda era `10` e a terceira era `11`, na ordem dos nomes `x₀,x₁`. As recusas devolveram primeiro `x₀` e depois `x₁`. A repetição de `x₀` na entrada custou leitura, mas dispensou uma nova recusa. As buscas na fita original custaram 12, 40 e 37 movimentos, totalizando 89. As duas cláusulas devolvidas somaram cinco letras e seu transporte custou 30 movimentos, ou 40 com as rebobinagens dos canais. A versão que opera diretamente sobre os pacotes entregou as mesmas cláusulas, aceitou o mesmo modelo e reproduziu os 89 movimentos de localização. [Controle e resultado](CONTROLES.json)

## Duas variáveis-pivô e muitos nomes em comum

Na classe de cláusulas binárias estudada, o primeiro literal traz um de dois pivôs fixos, um deles no endereço zero. O segundo literal traz qualquer variável fora desses dois pivôs. Os nomes podem se repetir em ambos os blocos e as cláusulas podem chegar intercaladas, em qualquer ordem. Para cada escolha dos dois pivôs, se o primeiro literal falha, sua cláusula obriga o valor do segundo. Duas exigências contrárias para o mesmo nome recusam o ramo. As demais exigências coexistem numa atribuição.

**[REAL]** Em quatro passagens, uma por par de valores dos pivôs, o leitor guarda em cada célula se o nome já foi exigido e com qual valor. A codificação unária leva a cabeça ao nome e a traz de volta. Para entrada de `L` letras com `T` marcas de endereço, o custo dos quatro ramos é exatamente **`7L + 8T ≤ 15L`**. A soma inclui a cabeça de entrada, quatro trilhas inicialmente brancas e as três rebobinagens da entrada. Nenhuma lista de atribuições é recebida ou percorrida. O primeiro leitor, que visita repetidamente os endereços, tem recibo separado e só conta a cabeça de entrada. [Leitor das quatro passagens](ReguaNaFita.lean) · [Especificação e leitor por endereço](ConteudoNaFita.lean)

No controle com dois nomes comuns, uma fórmula de 48 letras preservou precisamente os ramos `00` e `11`. Inverter uma das correlações mantendo o comprimento fez com que os dois nomes impusessem paridades contraditórias aos mesmos pivôs. Todos os quatro ramos caíram. O leitor percorreu exatamente 528 movimentos em cada instância. [Controle e resultado](CONTROLES.json)

## Onde termina a prova geral

**[OPEN]** Produzir a próxima atribuição compatível, ou decidir que ela inexiste, com custo polinomial fixo em movimentos de fita para toda CNF plana. O código traz um proponente executável correto cuja lista de referência contém `2^n` atribuições. Com `Q` vazio, o canal recebe zero cláusulas e a primeira chamada ao proponente já deve decidir `P`, que pode ser uma CNF arbitrária. Uma regra nova para produzir essa resposta com custo uniforme daria a cota que o operador procura. A quantidade de rodadas, a fidelidade da transmissão e o custo de conferir cada tentativa já têm provas próprias. A formulação pública da pergunta sobre busca e verificação continua aberta. [Clay Mathematics Institute](https://www.claymath.org/millennium/p-vs-np/)

Candidatas locais para revisão da gerência. O manifesto identifica os fontes, os objetos, o compilador, os imports diretos e os axiomas de cada declaração auditada. [Controles reproduzíveis](CONTROLES.json) · [Manifesto e hashes](RESULTADO.json)
