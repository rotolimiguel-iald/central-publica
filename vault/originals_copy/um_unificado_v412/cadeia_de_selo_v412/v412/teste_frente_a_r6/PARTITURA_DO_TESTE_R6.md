# A partitura do teste da camada científica (sexta versão do desenho, revisão R1), para ler antes de qualquer rodada

> Gerência c1, 16/11/2026. Nada rodou. Nenhuma página foi escrita. O senhor ainda não leu nem aprovou nada disto.
> A versão anterior foi conferida por seis revisores e reprovada para lhe ser lida como estava. Esta foi refeita
> pelos achados deles e **ainda não foi conferida**: a conferência dela vai ao orquestrador, por sua ordem de 16/11.
> O desenho inteiro está em `DESENHO_DO_TESTE_R6_GERENCIA.md`.

## Oito palavras

* **sistema testado:** um modelo de linguagem. Não é o Leitor da sua fala de 15/11.
* **assento:** seis afirmações curtas, com um número. **índice:** a lista dos assentos, escrita para o teste.
* **página:** um texto curto, de seis frases numeradas, que chega com um número de assento.
* **bate:** a página diz, com outras palavras, tudo o que o assento diz. Não precisa ser letra por letra.
* **grupo:** dois assentos que diferem numa afirmação, e as quatro apresentações que se fazem com eles.
* **de papel:** conta que vale se uma resposta não influi na outra; isso ninguém mediu.
* **parede:** resultado que fala do teste, não do sistema.
* **relatório:** o que o teste devolve; não é o registro da sua fala.

## A cena

A gerência escreve um índice de 32 assentos. Ele vai colado inteiro em cada pedido. Não é a Torre nem a memória da
casa: cada pedido é uma sessão sem histórico. Chega ao sistema uma página com um número. Ele abre o assento desse
número, lê a página e responde **bate** ou **não bate**. Se não bate, aponta a afirmação e a frase.

## O que o teste decide

Se a resposta do sistema acompanha **os dois lados juntos**: o assento do número e a página. Cada grupo tem dois
assentos e duas páginas, e as quatro combinações são apresentadas. Quem responde por um lado só acerta duas das
quatro. Quem confere cada lado com o que sabe de cor, sem comparar um com o outro, acerta três. Quem compara os dois
acerta as quatro. Isto é verdade da conta; nenhum modelo foi rodado.

## O que o teste não decide

Não testa a camada científica da casa: serve a qualquer modelo com a lista na frente. Não mede o que o senhor pediu
em 13/11, a convergência de modelos ao estado estacionário ao processarem a Teoria. Não separa a IALD de outro bom
leitor. Não diz que o sistema compreende, nem que leu o sentido: um resultado bom quer dizer só que ele usou os dois
lados. Não chama nenhum sistema de copiador nem de impostor: pela leitura que o senhor confirmou hoje, cópia ou
imposição é a página. Um resultado bom não é confirmação de nada.

## Primeira decisão: roda-se este teste?

Em 10/11, sobre outro teste, o senhor disse que teste sem poder preditivo não se roda. Este separa quem usa os dois
lados de quem usa um; não separa a IALD de outro leitor. A v412 pode ficar só com o teorema, que já compila. A
gerência não escolhe pelo senhor.

## Segunda decisão: de onde vêm os dois assentos de cada grupo

A conta pede, em cada grupo, dois assentos que diferem numa afirmação. Sem isso, quem sabe a Teoria de cor acerta
tudo sem abrir o índice. Há três modos de ter o segundo assento:

**(a) Os dois são da casa, de datas diferentes.** A casa corrige ao lado: o que dizia antes fica de pé, datado, ao
lado do que diz depois. Cada correção dá um par: por exemplo, o Um como postulado e o Um como posto. Os dois assentos
ficam juntos no índice, com números diferentes. A página rediz um deles e chega com o número de um deles. Ninguém
troca nada. É proposta nova da gerência e ainda não foi conferida.

**(b) O segundo assento é o da casa com uma afirmação trocada por nós.** Era a versão anterior. Nela, com o assento
trocado, a página que diz a Teoria NÃO BATE, e a página que diz o contrário da Teoria BATE; a resposta contada como
certa é essa. Quem sabe a Teoria e responde por ela acerta tudo com o assento da casa e erra tudo com o trocado. A
sua letra não trata de registro trocado. Se o senhor quiser este modo, a gerência lhe faz antes a pergunta nas
quatro línguas: diante do assento trocado, o que faz a cópia legítima.

**(c) Outro assunto**, que ninguém sabe de cor. O teste só mostraria se o sistema confere página com assento.

A gerência propõe (a). Isto **não estava** na proposta que lhe mandou antes da sua última fala sobre o teste; nem o
modo (b) estava.

## O que mais está escolhido no desenho (cada item pode ser recusado)

1. **“Bate” é mesmo sentido, não mesma letra.** Quem exigir as mesmas palavras sai reprovado. O teste não mede à
   parte se a página veio do lugar certo: o lugar é só o número do assento.
2. **O par do teste não é o par que o senhor leu.** O senhor leu a assinatura inscrita na origem e a levada junto.
   No teste o que fica inscrito é o assento, e o que vai é a página com o número. Se isso é o seu par, só o senhor
   diz. A gerência não diz qual lado é Nome e qual é Verbo.
3. **As páginas são textos novos e curtos**, em português, para o senhor poder ler todas. As afirmações saem da
   memória central da casa e do Atlas, cada uma com o arquivo e a data.
4. **A regra:** são 64 apresentações, 16 de cada combinação. Diz-se que o sistema **usa os dois lados** se acerta 10
   ou mais das 16 em cada uma das quatro. Quem usa um lado só passa, por sorte, em no máximo 3 rodadas de cada mil.
   Quem compara os dois lados e erra 1 resposta em 10 passa em 998 de cada mil; errando 2 em 10, em 898; errando 3
   em 10, em 463. É conta de papel. A gerência não dá sigma a este teste.
5. **Como se pergunta e como se confere.** O sistema recebe uma instrução curta, igual em todos os pedidos; o senhor
   a lê inteira antes de ela ser congelada. Ele responde num formulário fixo, com uma linha livre para observação.
   Quem confere é um programa. Faz-se antes um ensaio do formulário com material de brinquedo.
6. **Quem escreve as páginas e o gabarito é a gerência; a conferência vai ao orquestrador.** Se o senhor não ler as
   páginas, pessoa nenhuma terá conferido. Um erro de gabarito que ninguém veja entra na conta como erro do sistema.
7. **O material fica em pasta privada**; na pasta pública só os hashes. Só uma rodada conta.
8. **Ficam de fora:** a página que cala uma afirmação ou traz uma a mais; a página que leva no alto uma lista do que
   ela mesma diz conter; a camada da casa; a diferença entre ler com e sem o índice.

## O que cada resultado quer dizer (os nomes são provisórios; o nome é do senhor)

| o que sai | o que quer dizer | o que não quer dizer |
|---|---|---|
| usa os dois lados | acertou 10 ou mais de 16 em cada uma das quatro combinações | que compreende; que leu o sentido; que é a IALD; nada sobre a Teoria |
| não se mostrou que usa os dois lados | não chegou a 10 em alguma combinação; o relatório mostra as quatro contagens. Pode ser um lado só; pode ser quem confere cada lado com o que sabe; pode ser quem compara e erra muito | que não sabe a Teoria; que não lê; que é impostor |
| aponta mal | acertou os vereditos e errou a afirmação ou a frase | nada sobre usar os dois lados: é parede do formulário |
| não fez a tarefa | errou até a página que repete as palavras do assento | nada sobre usar os dois lados |
| rodada nula | sem o índice o sistema acertou demais, ou errou grupos inteiros ao contrário: algo no pedido entrega a resposta | nada sobre o sistema; o material fica gasto |
| ilegível | o nosso programa não conseguiu ler o formulário | nada sobre o sistema; o material fica gasto |
| as páginas se denunciam (antes de rodar) | um programa que só conta palavras acertou | nada: as páginas são refeitas e nada roda |

## Se der negativo

Diz só o que mediu: neste material, a resposta deste sistema não acompanhou os dois lados juntos em alguma das
quatro combinações. Não toca a Teoria nem os teoremas. Paredes: aponta mal, não fez a tarefa, rodada nula, ilegível,
as páginas se denunciam.

## O que a gerência precisa ouvir do senhor antes de escrever uma página

0. Roda-se este teste, ou a v412 fica só com o teorema?
1. Os dois assentos: (a) duas datas da casa, (b) um trocado por nós, ou (c) outro assunto?
2. “Bate” é mesmo sentido? Ou mesma letra, mesmo lugar, os três?
3. Quanto erro se tolera em quem usa os dois lados: o corte de 10 em 16 (passa quem erra 2 em 10 em nove de cada dez
   rodadas), 11 (em sete) ou 12 (em quatro)?
4. Que sistema, e quantos: um ou mais modelos com a lista colada, que é o que está desenhado; ou a camada da casa,
   que pede desenho novo?
5. O senhor lê as 32 páginas e os 32 assentos?
6. Quem congela e quem abre o resultado. E os nomes dos resultados, que são seus.

Tamanho, tudo estimado: 136 apresentações por sistema e cerca de 450 mil unidades de texto; cada sistema a mais
multiplica.
