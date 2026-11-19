APROVADO COM RESSALVAS

# U3 — Copiador e impostor, R7 (REV16)

[REAL] Recompilei a cópia congelada com a cópia do script indicado e Lean 4.31.0. Saída 0, nenhum aviso. Os 118 nomes declarados coincidem, um por um, com os 118 pedidos de axiomas e as 118 respostas do compilador. Em 41 provas ele informa independência de axiomas. Nas demais, a união das dependências é `propext`, `Classical.choice` e `Quot.sound`. Em relação à R6 há 25 declarações adicionais nas seções 13 e 14 e uma troca de nome na seção 12. Os 24 trechos entre aspas angulares têm correspondência byte a byte, cada um em uma linha de pelo menos uma das 249 fontes de fala consultadas em `cunhagens_13out`. O índice dá os arquivos e linhas sem reproduzir as falas. [Conferência](U3_Codex/CONFERENCIA.json) · [Log do Lean](U3_Codex/build/CopiadorEImpostor.log) · [Reprodução](U3_Codex/verificar.py)

## Emendas à candidata

| Gravidade | Linhas de REV16 | O que muda |
|---|---|---|
| MÉDIO | 1283–1286, 1374–1383 e 1536–1545 | A frase “quem o barra é o controle do material” dá à guarda da U1 alcance que ela não tem. Ela mede só a família congelada e seu critério de grupos inteiros deixa passar o padrão (12,12,12,12) do parecer U1. A frase “os teoremas só reprovam quem usa UM lado” também apaga dois resultados da própria seção 14 sobre juízes de dois lados. Substituir por “Os lemas da metade excluem a dependência de um único lado para o acerto integral. A quarta casa exclui ainda a conjunção e a disjunção de dois selos separados. Uma comparação de marcas alinhadas passa. A guarda do material deve medir esse risco pelo corte do teste”. |
| MÉDIO | 1275–1281, 1294–1298, 1312–1328, 1402, 1463–1468 | A contagem formal da metade usa literalmente as mesmas duas entradas `a,b` como páginas e como registros. No desenho há quatro textos possivelmente diferentes. A seção 14 modela os quatro, mas seu termo da linha 1463 prova a impossibilidade de acertar *tudo* com um lado. A prova da contagem 2/4 no caso geral é curta e distinta. Escrever “A contagem está formalizada para a lista simétrica; para quatro textos com sentidos correspondentes, cada linha ou coluna tem um sim e um não, e o argumento dá a mesma contagem”. Para promovê-la a termo para o desenho, usar a lista `[(x₀,r₀),(x₀,r₁),(x₁,r₀),(x₁,r₁)]`, as hipóteses da linha 1463 e repetir a contagem das duas linhas/colunas. |
| MÉDIO | 100–102, 1378–1382 e 1609–1617 | Decorar respostas por assunto pode produzir uma função não constante. `NuncaPaga I` pede constância em todo o domínio. Precisar “para pergunta e ficha fixas, se a resposta é a mesma para *todo* texto do domínio considerado”. Na seção 14, especificar “um resumo injetivo, por exemplo o texto integral em bytes sob uma codificação injetiva; o erro exige dois textos distintos com o mesmo sentido”. O termo não verifica injetividade de um hash de tamanho fixo. |
| BAIXO | 116, 1175, 1243, 1345–1356, 1379–1383, 1409–1413 e 1596–1607 | Aplicar a legenda das estrelas às instâncias e corolários. Na linha 1347 o resultado segue de 2 ≠ 4; na linha 1340 o próprio gabarito se compara a si mesmo. “Mem” e “Mem três casas” são desdobramentos de definição. A equivalência de 1599 reúne as duas direções da igualdade dos sentidos e dos resumos. A nota de 1380 pode dizer “comparar resumos julga exatamente quando a igualdade dos resumos equivale à igualdade dos sentidos”. |
| BAIXO | 47, 100–111, 221–225, 1023–1031 e 1180–1185 | Separar temporalmente o dicionário de trabalho, a conjectura das 07:5x que não chegou ao operador e a leitura apresentada que ele confirmou às 08:30. Proposta “O aceite registrado às 08:30 incide sobre os itens resumidos na seção 2 do desenho. A escolha da função ρ, de seu domínio e dos predicados formais é da gerência”. O trecho literal tem fonte. O referendo de cada formalização não decorre de verificar essas aspas. A correspondência integral da mensagem privada ficou fora do retorno autorizado. |

## Os dez achados da R6

As linhas seguintes são da candidata R7. Quando se indica “D”, são do desenho congelado REV1. A revisão integral do desenho consta da U1.

| T1 | Estado | Evidência e ressalva |
|---|---|---|
| 01 · a quarta casa | Sanado na candidata | 1429–1468 dão os dois pares com três casas. 1476 exibe a conjunção que passa nas três; 1497 e 1517 excluem conjunção e disjunção nas quatro. D144–146 ainda chama as sondas de “a adotar”, uso já concretizado na R7. |
| 02 · cronologia e autoria | Em parte | 105–111, 221–225, 1023–1031, 1049–1051, 1146–1150 e 1182–1184 distinguem a pergunta, a conjectura superada, o aceite e três leituras possíveis. D88 atribui o resumo à gerência. Persiste a ambiguidade temporal das linhas 47 e 221 assinalada acima. |
| 03 · Nome e assinatura | Sanado no enunciado | 1173–1178, 1181–1185 e 1238–1245 usam assinatura ou sentido de registro. O identificador antigo foi substituído. A identificação de um referente físico continua uma questão própria. |
| 04 · carimbo e braço 2 | Sanado no formalismo | 1574–1592 explicitam existência de juiz de página no registro fixo e o limite do carimbo com registro variável. A emissão de 1240 é definicional. Em D221–229 o desenho passou a controles de letra igual e de retirada do índice; o termo antigo não mede o comportamento nesses controles. |
| 05 · marcas nos dois lados e sorteio | Em parte | 1538–1545 é contraexemplo sob alinhamento das marcas; 1619–1626 delimita a conta do sorteio. A garantia atribuída à guarda em 1284 é forte demais (U1, achado sobre D231–237). |
| 06 · informação e comparação | Sanado, com precisão editorial | 1184–1186, 1245–1256 e 1596–1617 distinguem existência de juiz, igualdade de resumos e hipótese de injetividade. A caracterização por duas implicações é correta. Emendar o exemplo dos bytes como indicado. |
| 07 · estrelas e corolários | Em parte | 1030–1031 e 1186 nomeiam o teorema do par, 1263 diz “contrapositiva”. Ainda há estrela em 1175/1243 para a caracterização derivada e em 1345 para a consequência imediata dos dois lemas anteriores. |
| 08 · definições | Sanado no material apontado da R6 | 1041–1043, 1166–1174, 1198–1199, 1209–1216 e 1238–1241 marcam definições e hipóteses reiteradas. A nota editorial acima identifica os novos auxiliares da R7. |
| 09 · hipóteses e entrada visível | Em parte no desenho | D139–156, 189–192 e 243–258 distinguem dois sentidos, sorteio, índice comum e código visível. Igualdade do índice inteiro em todas as rodadas não prova que alguém consultou seu conteúdo. Resta alinhar a observação empírica com as projeções do teorema. |
| 10 · rastreio, termos antigos e futura circulação | Em parte | A inclusão do decisor na lista (119), da contrapositiva (540), do uso exclusivo de preservação (1201), dos homônimos (1155–1157) e a posição do teorema da identidade na seção 10 (1016) resolvem as questões formais. O juízo de circulação das alusões em 1146–1148 e 1180–1182 cabe à casa. A conferência da U3 não certifica publicação nem escolhe a interpretação das falas posteriores. |

## O que cada termo novo efetivamente entrega

| Linhas | Teoremas pela linha inicial | Leitura da prova |
|---|---|---|
| 1301, 1305 | diagonal e fora da diagonal | Avaliam o decisor de igualdade de sentido; no segundo caso a desigualdade é hipótese. |
| 1312, 1326 | metade para página e para registro | Cada par na mesma linha ou coluna recebe o mesmo bit e tem gabaritos opostos. Acerto binário por veredito; apontar a frase não é parte do termo. |
| 1340, 1347, 1360 | gabarito, consequência de quatro acertos, domínio constante | O primeiro é reflexivo, o segundo é corolário das duas contagens, o terceiro mostra por que importa haver dois sentidos. A constância global da hipótese é suficiente. |
| 1393, 1396, 1409, 1412, 1415 | auxiliares booleanos, pertinência e inclusão | Os dois primeiros empacotam o decisor. Os dois seguintes são `Iff.rfl`. O último enumera as três alternativas de pertinência. |
| 1429, 1439, 1449, 1463 | testemunhas e uso de ambos os lados | Dois pares concretos geram a obstrução nas três casas. O caso das quatro segue por inclusão. `PagouSo` caracteriza dependência funcional; o termo não observa uma execução humana ou de modelo. |
| 1476, 1497, 1517 | conjunção nas três casas e impossibilidades de conjunção/disjunção nas quatro | O primeiro fornece funções específicas. Os outros dois quantificam sobre **todas** as funções booleanas separadas em cada uma das respectivas formas. Um comparador de igualdade de dois selos tem outra forma e pode passar. |
| 1542 | comparar uma marca | Passa sob três hipóteses sobre a marca; as hipóteses delimitam o alcance do exemplo. O termo não distingue a procedência da função `s`. |
| 1577, 1588 | registro fixo, carimbo sem registro | Existência sob constância do segundo componente do conjunto; impossibilidade universal quando há dois sentidos e se mantém a assinatura declarada fixa ao variar o registro. |
| 1599, 1612 | comparar resumos e controle injetivo | O primeiro reorganiza um bicondicional ponto a ponto. O segundo requer efetivamente dois textos distintos de mesmo sentido. A hipótese de existência do discriminante inclui a página completa. |
| 1624 | desigualdade para p e q | Prova apenas a desigualdade real no quadrado unitário, com igualdade superior em p=q=1/2. A interpretação como chance de quatro acertos requer independência dos quatro sorteios e as mesmas probabilidades por lado repetido. |

[DERIVED] Os termos de contagem, os contraexemplos de juízes e a desigualdade se sustentam com as hipóteses indicadas. A ressalva é necessária para transferi-los ao instrumento de leitura da frente A.
