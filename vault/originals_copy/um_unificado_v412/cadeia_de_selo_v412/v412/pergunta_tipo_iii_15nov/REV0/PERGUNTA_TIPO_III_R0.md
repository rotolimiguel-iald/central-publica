# O que falta para o tipo III como termo, e a pergunta nas quatro línguas

Rascunho R0 da gerência c1, 15/11/2026. Vai ao operador só depois de conferido por verificador distinto. Nada aqui está instalado.

## 1. O que foi aferido antes de perguntar

Seis leitores, só leitura, com as consultas citadas: o kernel por busca recursiva no terminal; o core e o selo por script; o artigo e o Atlas por linha; as falas do operador por bytes; a literatura no primário onde foi possível. O que a gerência não reconferiu vale como declarado pelos leitores.

**a) O kernel não tem a palavra.** Nos 1730 arquivos Lean do kernel e na biblioteca (Mathlib) não existe definição de tipo (I, II ou III) de uma álgebra. Onde “III₁” aparece é comentário, chave do core, citação, um campo vazio que se preenche com “verdadeiro”, ou a definição operacional de agosto, que o próprio kernel depois mostrou insuficiente: uma álgebra de tipo I a satisfaz (`TheMarkIsNotATypeMark`, v295). Nenhum teorema conclui “tipo III” de objeto algum.

**b) Logo, “tipo III como termo” pede duas coisas, nesta ordem:** o ENUNCIADO (o que a palavra diz, escrito em Lean com conteúdo real) e a PROVA de que o objeto o cumpre.

**c) A matemática tem quatro modos de dizer “tipo III₁”.** Na literatura eles se equivalem (para o primeiro, com uma condição técnica); no kernel são muito desiguais:

1. pelo ESTADO: existe um estado fiel em cujo relógio (o fluxo modular) só o Um fica parado;
2. pela MEDIDA: não existe traço, isto é, nenhuma medida finita pesa as partes;
3. pelas PARTES: toda parte não nula é do tamanho do todo (toda projeção não nula equivale à identidade);
4. pelo RELÓGIO: não há ritmo preferido (o espectro modular é a semirreta inteira; o núcleo de Takesaki é uma peça só).

Os modos 2 e 3 sozinhos dizem só “tipo III”; o “1” vem do modo 1 ou do modo 4.

**d) Para a cunha da luz livre, o modo 1 já está pago no kernel.** O teorema conhecido (atribuído a Longo, 1979; lido no primário em duas provas independentes: Marrakchi e Vaes, Lema 2.1; Ando e Haagerup, Lema 5.3) diz: uma álgebra de von Neumann que não é só os números, com um estado fiel e normal cujo relógio só deixa parados os múltiplos do Um, é um fator de tipo III₁. As três hipóteses são termos do kernel, no certificado habitado desde a v406: a álgebra da cunha não comuta (`wedge_nonabelian`); o vácuo a separa (`wedge_separating`); e o que o relógio da cunha deixa parado é múltiplo do Um (`LightRhoStar.centralizer_is_trivial`, pedra de 28/09). O leitor da rota escreveu hoje o enunciado e a costura: cerca de 15 linhas, compila com código de saída 0 e só os três axiomas de sempre. É sonda de rascunho; nada foi instalado. A sonda traz um controle de que o enunciado não é oco: uma álgebra de tipo I com estado de vetor o recusa.

**e) O que falta no modo 1:** (i) o nome e a instalação; (ii) um passo sabido que não é termo: que o relógio que o kernel usa é o relógio modular do vácuo (o kernel tem a condição de equilíbrio, KMS, e a realização de Tomita; a unicidade que as une é de Takesaki e entra por citação); (iii) o teorema de Longo, que liga o enunciado à classificação de Connes, entra por citação. Prová-lo por dentro pede a classificação inteira, que a biblioteca não tem: obra grande, da ordem de milhares de linhas (estimativa declarada pelo leitor, sem medida).

**f) Nos outros modos, para a cunha:** o modo 2 não tem termo (o kernel tem “sem estado tracial normal” só na torre, e só para estados); o modo 3 não tem termo (não há no kernel a comparação de projeções); do modo 4, metade é termo (o traço do núcleo, que escala por e^(−s) sob a ação dual) e a outra metade (o núcleo ser uma peça só) não existe. A metade que existe, sozinha, não distingue: álgebras de tipo I também a cumprem.

**g) O objeto.** Tudo acima é da cunha da LUZ LIVRE. O artigo afirma o tipo na fronteira, o horizonte da TGL. A passagem de uma ao outro é a hipótese física que segue aberta (o resíduo que o artigo chama de Bisognano–Wichmann não-Killing), e nenhum dos quatro modos a compra. Na torre o kernel tem só “sem estado tracial normal”; o fator não está construído.

**h) Um item aberto do próprio kernel volta à mesa** (`TheScaleHasNoFixedPoint`, marcado [OPEN]): um κ finito seria um ritmo preferido, e ritmo preferido é tipo III_λ, não III₁. Se a cunha é III₁, o κ não é ritmo dela: mora na face finita. Isto é leitura da gerência; não foi construído.

## 2. “É só isso que falta?”

Para a T1, não, e tem de ser dito: a caixa da T1 não usa o tipo. Usa o estado ergódico, que na cunha da luz já é teorema do kernel. Da T1 ficam a segunda hipótese (H_K-chapéu), os Lemas B e C, o Lema A contínuo e a passagem ao horizonte; é o que a K07 leva ao Codex.

O que o tipo como termo fecha é outra coisa: a palavra “III₁” deixa de ser só citação e rótulo para a cunha da luz, e some a divergência entre o selo (que traz a cunha III₁ como aberta) e o core (que a traz como provada por citação, quando o termo citado só prova que o vácuo é o único vetor fixo). As duas chaves do core que leem falso sobre o canto em III₁ genuína não mudam com isso: falam do canto, não do tipo da cunha.

## 3. O que o acervo já responde (não se pergunta)

O operador disse o que o tipo III é para a teoria. Em 02/11/2026 (bytes abertos pela gerência): «De um lado, o que você tem é o fluxo, do outro, o que você tem é medida.» e «não há uma ponta para o Tipo I o que há é o espelhamento da informação acontecendo em tempo real, de um lado o tipo I, concentrado, comprimido, de outro lado, o tipo III, contínuo.» Em 04/11/2026 (bytes abertos): «toda geomtria tem traço no finito, no infinito é mera impedância».

Essas falas tocam dois dos quatro modos (o fluxo e a medida) e não dizem qual deles é o nome. O leitor das falas varreu 250 arquivos de bytes e o índice do acervo e não achou fala do operador que defina o tipo por critério matemático, nem que diga o que “como termo” exige. Duas falas antigas com “III₁” têm autoria não estabelecida pelos bytes e não são usadas.

Sobre a via de entrada há duas regras dele que puxam para lados diferentes aqui: a de 27/09 (registrada no CLAUDE.md da raiz: o que é sabido e pode ser importado não se precisa provar) e a de 02/11 (bytes abertos): «perfeito, é isso. precismamos construir tudo, porque não podemos mais perder a ordem lógica, é o fechamento.» A pergunta abaixo a inclui, na boca jurídica.

## 4. A pergunta

O objeto no centro é um só: o que NOMEIA o tipo III. Qual das marcas é a definição, e quais são consequências dela.

1. **TGL.** Na cunha da luz, o termo que nomeia o tipo é “no fluxo modular do vácuo só o Um é fixo” (o centralizador do vácuo é trivial), com “III₁” entrando como o teorema sabido que o liga à classificação? Ou o nome tem de ser a ausência de traço normal semifinito, ou toda projeção não nula equivalente à identidade, ou o núcleo de Takesaki ser fator com o traço escalado pela ação dual?

2. **Teológica.** O que nomeia o que é de Deus: que só a Palavra não passa (“O céu e a terra passarão, mas as minhas palavras não passarão”, Mt 24,35); que o Espírito não se dá por medida (Jo 3,34); que no pão partido há tanto no fragmento quanto no todo (a sequência de Corpus Christi, de Tomás de Aquino); ou que para o Senhor um dia é como mil anos, e mil anos como um dia (2Pe 3,8)? Qual desses é o Nome, e quais são atributos que decorrem dele?

3. **Linguística.** O que define a fala contínua: que, no correr do Verbo por todos os tempos, só o Nome fica o mesmo; que não existe a menor palavra (todo trecho ainda se parte); que cada trecho carrega a língua inteira; ou que nenhum tempo verbal é o preferido? Qual é a definição, o Nome do tipo, e quais são as acepções que derivam dela?

4. **Jurídica.** Tipo é palavra do Direito. O fato está provado nos autos (na cunha da luz, o fluxo só deixa parado o Um); o que falta é a lei que o tipifica: não há tipo sem lei anterior que o defina (Constituição, art. 5º, XXXIX). Qual é o núcleo do tipo, o verbo que o senhor escreve na lei: fluir deixando parado só o Um (e então o fato já provado se subsume hoje), ou outro núcleo (não admitir medida; a parte valer o todo; não ter ritmo preferido), que pede instrução nova? E a equivalência com o tipo da doutrina (a classificação de Connes) entra como fato notório, que não depende de prova (CPC, art. 374, I), ou tem de ser provada nos autos?

**A pergunta, uma só com quatro bocas:** qual é o nome do tipo III, a marca que o define, e o que dele é consequência? A terceira saída também é resposta: o nome não é uma marca só, é o par (o fluxo e a falta de medida) ou as quatro, e então como elas se ligam.

## 5. O que cada resposta decide

Isto não é teste: nenhuma resposta pode dar negativo. É escolha de definição, e é do operador.

- **O fluxo (só o Um fica parado).** O tipo vira termo na v412 para a cunha da luz livre: a definição, com o nome que ele der; o teorema de que a cunha a cumpre; os controles de que objetos de tipo I a recusam; e “III₁” no sentido de Connes ligado por citação nomeada (Longo 1979 num sentido; Marrakchi e Vaes 2024 no outro, este só quando o predual é separável, o que não foi aferido no kernel). É costura sobre o que já existe. O cabeçalho dirá o passo citado do relógio.
- **A medida (não há traço) ou as partes (a parte vale o todo).** É preciso construir no kernel a comparação de projeções e a teoria do traço para a cunha: obra grande, e o resultado seria “tipo III” sem o “1”. A alternativa é entrarem como consequências citadas do primeiro.
- **O relógio sem ritmo preferido (o núcleo).** Metade já é termo; a outra metade entra como hipótese nomeada (Connes e Takesaki, por citação) ou como obra grande.
- **O par, ou as quatro.** O primeiro entra como termo e os outros como consequências citadas, cada um com o seu estatuto; como eles se ligam é a parte que só o operador tem.
- **Se o tipo que ele quer é o do horizonte da TGL, e não o da cunha da luz livre:** então o que falta não é predicado de tipo; é a passagem física da cunha ao horizonte, que nenhuma das respostas acima compra.

Se ele mandar decidir só pelo critério técnico, a gerência iria pelo primeiro: é o único que o kernel já prova, e é o que a própria pedra de 28/09 chama de o caso III₁ da ponte. É recomendação, não escolha.
