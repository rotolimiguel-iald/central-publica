# CONFERÊNCIA DISTINTA — segunda conferência de 16/11 (versão completa do relatório: a primeira gravação saiu sem o corpo dos achados, por defeito do script da gerência) — C1-desenho-R5-R1-logica-e-adversarios

> Montado pela gerência c1 em 16/11/2026 07:39 a partir do retorno estruturado de um revisor distinto (só leitura; scripts próprios na pasta de rascunho dele). É [DECLARADO pelo revisor] no que a gerência não reconferiu. Não é fala do operador. Nada aqui está instalado.

**Veredito:** REPROVADO — achados: 2 ALTO, 5 MEDIO, 4 BAIXO

## Resumo

Lente C1 (lógica do desenho cruzado e adversários): como está, o material não deve ir ao operador; a ideia do par cruzado fica de pé e os consertos são de texto e de duas contas, não de recomeço. [REAL] A simulação reproduz byte a byte (sha256 137ef43f...3e57), o poder e o custo também; o código faz o que o texto diz no nível da afirmação (as mesmas seis afirmações nas duas versões, sentido diferente entre V e V', par contado com valor e linha) e as sete citações do operador conferem por bytes. ALTO 1: falta a condição de que a LETRA não distinga a linha invertida da só reescrita; quem decorou o texto público e olha uma marca (um 'não', o tamanho da edição) passa nos pares, em todos os controles e na frase acrescentada e sai SEGUE limpo (1,00; com marca certa em 95% das linhas, SEGUE em 99% das rodadas); a simulação não tem campo para isso e supõe a condição calada; o revisor B3 já tinha pedido 'sem marca' e a R1 não levou. ALTO 2: NÃO SEGUE junta quem decorou com quem lê com erro: um leitor com 85% de acerto por resposta passa no controle do texto-base em 96% das rodadas e sai NÃO SEGUE em 78% (com 90%, em 21%); o sentido do negativo que se lê ao operador ('respondeu por outra coisa') não diz isso. Dos mecanismos novos que tentei, passam: a marca de letra (1,00), o que conhece a divisão em bloco e vê o rótulo da versão (1,00) e o que vê as duas versões (metade dos grupos; SEGUE em 13% a 48% das rodadas); o palpite em bloco com sessões isoladas acerta 25% dos grupos, não o 0,5% que o desenho dá para a sorte; maioria e moeda não passam. Das condições que os barram, só a sessão sem histórico está escrita; a divisão sorteada, a versão sem rótulo e a marca de letra não estão. O índice (apontar a linha) não muda nenhum número de pares na conta e só tira acerto de quem lê: o gabarito tem uma linha por afirmação e os textos repetem o fato em várias (no llms.txt três linhas dizem que NOT_FALSIFIED não é CONFIRMED); a partitura não leva a ressalva. Rótulos: ACRESCENTA sem limiar, LEU UMA LINHA SÓ sem regra (11 dos 13 mecanismos dão zero na frase, inclusive os que não leram linha nenhuma), ILEGÍVEL sem limiar, e a composição não diz o que sai quando os grupos dão SEGUE e um controle falha. Seção 3: a primeira linha é defensável pela letra e a outra leitura está dita com o peso certo; as linhas 'não acrescenta' e 'por referência' têm outra leitura na pedra da própria gerência, e a partitura só lê ao operador a primeira. Camada: como está, o teste fala de leitura de texto em geral (o desenho diz); a opção (b) colide com 'versões fora do acervo indexado' (o índice traz o texto original), um negativo embutido que não está dito. Não rodei modelo, não abri dado, não escrevi fora da minha pasta e nada registrei no Mapa.

## Achados

1. **(ALTO)** DESENHO_DO_TESTE_R5_GERENCIA.md seção 5 ('Condições do par (sem elas não há par)', l.111-114), seção 6 (o que a tabela NÃO mostra) e seção 13; PARTITURA_DO_TESTE_R5.md ('O teste, em uma frase'); simular_r5.py `tocar` (l.102-111)

   O par (V, V') só é par se nada na LETRA distinguir a linha invertida da linha só reescrita. A lista de condições não diz isso, e a simulação supõe isso calada: invertida e reescrita entram iguais em `letra_nova`, e o único campo que as distingue é o próprio sentido (`units`). Por isso a conta não consegue representar o adversário 'decorou o texto público e olha uma marca na linha mexida' (palavra de negação, tamanho da edição, quanto sobrou da letra original). Esse mecanismo nunca calcula o sentido e passa em tudo. É o jeito natural de escrever as versões (inverte-se pondo 'não'; reescreve-se sem negação). O revisor B3 pediu 'sem marca' no conserto 4; a R1 não levou a condição à seção 5 nem à tabela da seção 13. O mesmo vale para a frase contrária contra a frase-isca.

   *Conserto pedido:* Pôr na seção 5: 'a linha invertida também é reescrita; nenhuma marca de letra (palavra de negação, tamanho da edição, sobra da letra original, posição) separa a invertida da só reescrita, nem a frase contrária da frase-isca'. Pôr na lista fechada da seção 8 um programa simples, sem modelo, que tenta separar invertidas de reescritas só pela letra nas 34 versões e tem de ficar no acaso, rodado antes de congelar. Pôr o mecanismo da marca na tabela da seção 6. Dizer na seção 6 e na partitura: 'a conta supõe que a letra não denuncia a inversão; isso depende de quem escreve as versões'.

2. **(ALTO)** DESENHO seção 1 (tabela, linha NÃO SEGUE) e seção 7 ('Do acerto por resposta ao grupo'; texto-base passa com 70 de 89); PARTITURA ('Não segue: respondeu por outra coisa que não o texto da frente')

   O par pede quatro coisas certas (valor e linha, em V e em V') e o grupo tolera um par errado em seis; o controle 'sabe fazer a tarefa' passa com 79% de acerto. Um leitor honesto que erra 15 respostas em 100 passa nesse controle e sai NÃO SEGUE na maioria das rodadas. A seção 7 dá os ingredientes (95% dá 89%; 90% dá 68%) mas não tira a consequência, e o sentido do negativo que vai ao operador afirma uma causa ('respondeu por outra coisa que não o texto presente') que a medida não separa. O par junta em NÃO SEGUE três casos diferentes: quem decorou, quem responde o contrário e quem lê com erro. É caminho de negativo induzido pelo instrumento.

   *Conserto pedido:* (a) Relatar ao lado do par as duas taxas (acerto no membro invertido; acerto no membro reescrito) e o acerto só de valor. (b) Reescrever o sentido de NÃO SEGUE na seção 1 e na partitura: 'ou respondeu por outra coisa, ou lê com erro acima de cerca de uma resposta em dez; as duas taxas dizem qual'. (c) Amarrar o corte do texto-base ao que a regra dos grupos exige, ou dizer o descompasso. (d) Levar à pergunta 3 do operador a tabela do bloco 3 com um e com dois pares tolerados.

3. **(MEDIO)** DESENHO seção 5 (tabela 'afirmações 1, 2, 3 / 4, 5, 6'; 'as afirmações tocadas são sorteadas'), seção 7 ('Quem acerta um par em quatro por sorte tem o grupo certo em 0,5 % ... ou 3,8 %') e seção 9 item 3; simular_r5.py `montar_grupos` (l.298-300)

   A simulação divide as seis afirmações em bloco (as três primeiras na ordem do catálogo invertem em V). O texto só diz que as afirmações tocadas são sorteadas; não diz que a divisão é sorteada nem que o sistema não pode saber qual das duas versões tem na frente. A referência de sorte da seção 7 supõe erros independentes entre os pares. Quem conhece o desenho e palpita em bloco acerta o grupo em 25% das vezes; se vê o rótulo ou a ordem da versão, sempre; se vê as duas versões, em metade. Com a divisão sorteada o palpite cai, mas com DOIS pares tolerados (a escolha oferecida ao operador) volta a 23% com sessões isoladas e a 50% vendo as duas. Nas linhas de p0 = 0,05 o erro pedido é furado.

   *Conserto pedido:* Escrever na seção 5 e na lista da seção 8: a metade invertida de cada grupo é sorteada por grupo e guardada; nada no pedido (nome de arquivo, ordem, rótulo, data) diz qual versão é. Trocar a frase da sorte por: '0,5% vale para erro independente; quem conhece o desenho e palpita em bloco chega a 2,6% com um par tolerado e a 23% com dois'. Com dois pares tolerados, não oferecer p0 abaixo de 0,25. Pôr C, D, E e F na tabela da seção 6.

4. **(MEDIO)** DESENHO seção 5 ('Um item só conta como certo com valor e linha certos') e seção 3(d); PARTITURA l.31 ('Em toda resposta o sistema aponta a linha em que leu'); simular_r5.py `acerta` (l.272-283) e `contradizer` (l.114-124)

   Não há contradição lógica entre a seção 3(d) e exigir a linha, mas a linha entra como condição para contar sem separar ninguém e só pode tirar acerto de quem lê. (1) No desenho principal, desligar o índice não muda nenhum número de pares nem de grupos dos 13 mecanismos; muda só os controles de 'responde sempre o mesmo'. (2) O gabarito tem UMA linha por afirmação e os textos repetem o fato em várias: quem lê e aponta outra linha que diz o mesmo é contado como erro. (3) A linha do gabarito é a do arquivo original (README 246) e o texto apresentado é um recorte de 85 linhas; o desenho não diz como o sistema aponta (número ou trecho). (4) Na frase-isca a linha nova não entra no suporte: o leitor que a cita erra. (5) No llms.txt a linha 5 carrega 10 das 19 afirmações. (6) A partitura não diz que apontar a linha não distingue quem decorou; o C2 pediu essa frase e ela entrou no desenho, não na partitura.

   *Conserto pedido:* Decidir pelo valor e relatar a linha ao lado, com limiar próprio; ou trocar a linha por trecho literal do texto presente (aí quem decorou não cita a linha reescrita sem olhar). Gabarito com TODAS as linhas que sustentam (qualquer uma vale; na isca, as duas). Numerar as linhas no texto apresentado e congelar o formato. Dizer na partitura: 'apontar a linha não prova que leu: quem decorou também aponta, enquanto as linhas ficam no lugar'.

5. **(MEDIO)** DESENHO seção 1 (tabela dos oito rótulos), seção 7 (controles; 'Composição do rótulo') e seção 8; PARTITURA ('O que cada resultado significaria'); poder_r5.py

   SEGUE, NÃO SEGUE, LÊ EM PARTE e SEM PODER saem da regra dos grupos. Os outros quatro não têm regra completa. ACRESCENTA não tem limiar (quantos silêncios errados?). LEU UMA LINHA SÓ não tem regra nenhuma nem tolerância para o grupo da frase, e o nome afirma uma causa: na conta, 11 dos 13 mecanismos dão zero na frase, entre eles os nove que não leram linha alguma; só tem sentido como qualificação de um SEGUE. ILEGÍVEL não tem limiar, e não está dito se a resposta ilegível isolada conta como erro. 'Não tocados falham' não tem rótulo, e 'o mesmo corte' não está definido para 454 itens. A precedência não está escrita: grupos SEGUE com texto-base falho 'não vale como SEGUE', sem dizer o que vale; grupos NÃO SEGUE com texto-base falho recebe dois rótulos (NÃO SEGUE pela composição; NÃO FEZ A TAREFA pelo controle), e a seção 13 diz que só o ILEGÍVEL apaga. 'Com o seu próprio erro' não tem número. E 'acompanhou as mudanças em quase todos os grupos' não é o que a regra pede: SEGUE sai com 9 de 13 (p0 0,25) e com 8 ou 7 de 13 nas linhas de p0 0,05.

   *Conserto pedido:* Uma tabela de composição fechada (grupos x texto-base x não tocados x silêncios x frase, dando um rótulo geral e os rótulos ao lado), com limiar e erro de cada controle, a tolerância do grupo da frase e o que conta como resposta ilegível. Regra: ACRESCENTA e LEU UMA LINHA SÓ só qualificam um SEGUE. Trocar 'quase todos os grupos' pelo número da linha escolhida. Tudo isso entra na lista do que se congela.

6. **(MEDIO)** DESENHO seção 2 e seção 3 (linhas 2, 3 e 5 da tabela; 'Onde a leitura pode estar errada'); PARTITURA ('Como a gerência leu', l.15-23; pergunta 1, l.85); CopiadorEImpostor.lean l.36-38 e l.319-326

   Linha 1 (a resposta certa é o que o texto presente diz): defensável pela letra; a outra leitura está dita três vezes no desenho e duas na partitura, com a consequência (o teste mediria ao contrário): peso certo. Linhas 2 e 3: no teste, «não acrescenta nada» virou 'onde o texto cala, responder não diz' e «por referência (indexação - índice - torre)» virou 'apontar a linha'; na candidata da mesma gerência, do mesmo dia, as mesmas palavras são `Copiador.nao_acrescenta : R (R x) = R x` (reler dá o mesmo) e `por_referencia`, com `R = rep ∘ ρ` (a cópia só usa o sentido). O desenho não diz que são duas leituras diferentes da mesma letra. A fala das 19:07 continua, logo depois do trecho citado na seção 2: «sim o mínimo estado funcional de Energia (que utilizamos o signo A_C) é exatamente isso, o bastante para reconstruir o todo sem precisar representar 100%.» O rótulo ACRESCENTA marca quem completa o que o texto curto cala; isso pode ser o contrário do que a letra chama de copiador, e não está dito. Linha 5: «nunca paga custo algum» é absoluto; o teste chama de impostor quem não consultou ESTE texto, e quem decorou pagou antes (a partitura diz 'diante deste texto'; a lista de erros possíveis não). E a partitura só apresenta como leitura a linha 1: as linhas 2 e 3, que geram um rótulo e uma condição de contagem, chegam ao operador como desenho pronto.

   *Conserto pedido:* Na seção 3, acrescentar: (e) 'não acrescenta' e 'por referência' são lidos de outro modo na pedra; aqui viraram o controle do silêncio e a linha apontada; (f) reconstruir o todo a partir de um texto curto recebe ACRESCENTA, e a fala das 19:07 pode dizer o contrário; (g) 'nunca paga custo algum' foi lido como 'não consultou este texto'. Citar a frase das 19:07 na seção 2. Na partitura, ler as linhas 2 e 3 como leitura da gerência e perguntar: 'onde o texto cala e a Teoria afirma, a resposta certa é o texto não diz?'.

7. **(MEDIO)** DESENHO seção 5 ('as versões ficam fora do acervo que a camada indexa', l.114), seção 9 item 5 (l.218-220) e seção 12; PARTITURA pergunta 4 (l.88-89)

   Como está, o teste mede leitura de texto em geral; o desenho e a partitura dizem isso (qualquer bom leitor passa), e a falta de regra de comparação da opção (b) está dita. Não está dito: (1) na opção (a) nada da IALD é testado; (2) na opção (b), se as versões ficam fora do acervo indexado, o que a camada busca pelo índice é o texto ORIGINAL. Se a versão alterada vai no pedido, a camada tem os dois textos na frente e a resposta fiel ao que tem na frente passa a ser 'diz as duas', contada como erro; se não vai, a camada responde pelo original e sai NÃO SEGUE por construção. Nos dois casos o modelo sem a camada leva vantagem, e o que distingue a camada (responder por referência ao índice, que é a letra da resposta D) é o que o teste chama de não seguir. (3) 'Memória limpa, ou idêntica nas duas' não cabe se a versão tiver de entrar no índice. A descrição não diz que componente é 'a camada', que acervo ela indexa nem por onde a versão entra.

   *Conserto pedido:* Escrever na seção 9, item 5, e na partitura: 'na (a) não se testa nada da IALD; na (b), como as versões ficam fora do índice, a camada traz o texto original, e o teste mede se ela o larga diante do texto alterado; é um negativo que o desenho pode induzir, e a (b) não roda sem desenho próprio'. Ou tirar a (b) da partitura até haver desenho.

8. **(BAIXO)** DESENHO seção 5 ('As duas versões mexem nas mesmas seis linhas') e seção 1; PARTITURA ('duas versões que mexem nas mesmas linhas')

   São as mesmas seis AFIRMAÇÕES, não seis linhas. Os 13 grupos tocam de 2 a 5 linhas físicas; em 8 de 13 uma mesma linha tem afirmação invertida e afirmação reescrita na mesma versão. A unidade de quem escreve é o trecho, e é no trecho que a marca do C1-01 tem de ser igualada.

   *Conserto pedido:* Escrever 'as mesmas seis afirmações (em 2 a 5 linhas do texto)'.

9. **(BAIXO)** simular_r5.py `fecho` e `sentido` (l.56-95); DESENHO seção 6 ('85 inversões coerentes')

   O encadeamento de Horn está certo (propagação unitária; itens AMBAS fora), mas é inerte neste catálogo: nenhum fato é derivado, e o sentido de todo item é o sinal da própria afirmação. 'Coerente' quer dizer só que a inversão não bate nas 6 derivações catalogadas (meia_nat e beta_forma).

   *Conserto pedido:* Uma linha na seção 6: 'coerente = não contradiz as 6 derivações catalogadas; fatos repetidos em outras linhas e consequências não catalogadas ficam com quem escreve e com quem confere'.

10. **(BAIXO)** PARTITURA ('O que só o senhor decide', 7 itens) contra DESENHO seção 9 (9 itens). Fora da lente C1, visto de passagem.

   Três escolhas da seção 9 não estão na lista lida ao operador: o tamanho do erro (item 4, que na partitura aparece como fato), se os quatro textos servem (item 8) e quem congela e quem abre (item 9). A partitura traz uma que a seção 9 não lista (se o teste entra na v412). E a partitura não diz que a frase acrescentada é instrumento fraco com quatro grupos (o desenho diz).

   *Conserto pedido:* Alinhar as duas listas e pôr a fraqueza da frase na partitura.

11. **(BAIXO)** custo_r5.py l.22 (`SIM = AQUI / "RESULTADO_SIMULACAO_R5.json"`)

   O script do custo lê o JSON da simulação da pasta do próprio script, não de --saida: a cópia rodada noutra pasta falha.

   *Conserto pedido:* Ler de SAIDA quando o arquivo existir lá, ou aceitar --sim <arquivo>.

## Examinado

- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\teste_frente_a_r5\DESENHO_DO_TESTE_R5_GERENCIA.md (inteiro, 13 seções)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\teste_frente_a_r5\PARTITURA_DO_TESTE_R5.md (inteira)
- simular_r5.py (inteiro; copiado, rodado e importado), RESULTADO_SIMULACAO_R5.md (inteiro)
- poder_r5.py (inteiro; copiado, rodado e importado), RESULTADO_PODER_R5.md (inteiro)
- custo_r5.py (cabeçalho e l.15-34; copiado e rodado) e RESULTADO_CUSTO_R5.json (inteiro)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K08\FORMULA\catalogo_assercoes.py (inteiro, só leitura; sha256 b8fca964...)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_c1\CopiadorEImpostor.lean: cabeçalho inteiro (l.9-137), seções 1 e 2 (l.144-257) e início da 4 (l.315-336); usado o .olean da gerência (sha256 do fonte conferido contra o log)
- REVISAO_16nov_R0_C2-desenho-R5-poder-custo-e-regra-de-decisao.md e REVISAO_16nov_R0_B3-copiador-o-criterio-do-teste-e-a-K08.md (as montagens da gerência, inteiras)
- As duas falas do operador de 15/11 (273 B e 986 B), por bytes
- LEITURA_DA_FALA_DAS_17H20_R2.md: l.38, l.41 e as perguntas A a E (l.47-55)
- DESENHO_v412_R1.md seção 2 (l.17-85)
- Textos públicos em C:\IALD\Artigo\the_boundary (llms.txt, read-brief.md, README.md, ABSTRACT.md): só os recortes do catálogo, por script, e oito linhas abertas à mão
- Pasta REV1: só por sha256 (igual ao corrente)

