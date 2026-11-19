# CONFERÊNCIA DISTINTA — segunda conferência de 16/11 (versão completa do relatório: a primeira gravação saiu sem o corpo dos achados, por defeito do script da gerência) — C3-partitura-R1-letra-lingua-e-errata-K09

> Montado pela gerência c1 em 16/11/2026 07:39 a partir do retorno estruturado de um revisor distinto (só leitura; scripts próprios na pasta de rascunho dele). É [DECLARADO pelo revisor] no que a gerência não reconferiu. Não é fala do operador. Nada aqui está instalado.

**Veredito:** REPROVADO — achados: 6 ALTO, 12 MEDIO, 2 BAIXO

## Resumo

REPROVADO para ir ao operador como está; os consertos são quase todos de texto, e quase tudo o que falta na partitura o próprio desenho já diz. O que confere: as sete citações do desenho e da partitura são exatas por bytes; as três contas da gerência reproduzem na minha pasta (os dois .md iguais byte a byte); o teorema citado compila (RC 0, só o trio); a correção do que ele ouviu em 15/11 sobre a outra forma está clara; a consequência e 'qualquer bom leitor passa' estão ditas. Alto 1: a partitura diz que NÃO SEGUE é 'respondeu por outra coisa que não o texto', mas pela regra recebe esse rótulo quem acerta até 7 dos 13 grupos, e um leitor com 85 % de acerto por resposta o recebe em 78 % das rodadas. Alto 2: 'O teste separa copiador de impostor' afirma mais do que a pedra da própria gerência, que nega que passar mostre o copiador da fala; o reconhecimento (o eco) não tem instrumento e isso não está em 'não decide'. Alto 3: três das cinco leituras da letra que o desenho usa não estão na partitura, e duas viraram regra de nota (calar vale 'não diz'; a linha é condição de acerto), com leitura concorrente na letra dele. Alto 4: a partitura lê oito resultados sem dizer como se combinam; quem acrescenta pode sair SEGUE, e dois rótulos (ACRESCENTA e LEU UMA LINHA SÓ) não têm regra escrita. Alto 5: faltam três das nove escolhas que o desenho dá ao operador, mais o modo de chamada, a memória limpa, o que se congela e a rodada única. Médios: a outra leitura vem em duas saídas, com palavra que não é da letra, e fora das quatro línguas; a letra foi cortada; não diz quem confere, nem que 10 dos 13 grupos são de textos em inglês; não mostra o que será invertido nem onde fica guardado; palavras sem explicação; perdeu-se a palavra parede. Três registros do mesmo dia discordam sobre o que ele já leu: o desenho da versão diz que as respostas 'fixam' a leitura, o Mapa diz que foi leitura apresentada e que ele respondeu «Prossiga», e o desenho R5 diz que ele ainda não leu. Errata da K09: o hash confere, a frase do gate confere com o desenho e com o Mapa, 10 de 11 trechos citados são literais e o 'que vale' bate com a K10. Mas a linha dos hashes está errada (são dez arquivos e nove não batem, não sete e seis), '16 pelo prefixo' dá 30, quatro correções de Q2 e Q3 não foram transportadas, a lista de pendentes é curta e o arquivo não é o registro puro da rodada 3. Não rodei modelo, não abri dado, não escrevi fora da pasta C3 e nada registrei no Mapa.

## Achados

1. **(ALTO)** PARTITURA_DO_TESTE_R5.md l.54-55 ('Não segue', 'Lê em parte'); DESENHO_DO_TESTE_R5_GERENCIA.md secao 7 (l.157-173); RESULTADO_PODER_R5.md

   A partitura diz que NÃO SEGUE quer dizer 'respondeu por outra coisa que não o texto da frente'. Pela regra do desenho, NÃO SEGUE é 'ficou abaixo do que se exige de quem lê', e cai nele quem lê boa parte do texto. Com a primeira linha da tabela (13 grupos; p0 0,25; p1 0,90; 1 em 1.000) recebe NÃO SEGUE quem acerta até 7 dos 13 grupos, e nessa linha o resultado 'Lê em parte' nem existe. A partitura lê 'Lê em parte' como resultado possível sem dizer que depende das escolhas, e não diz que o sistema do meio sai quase por sorteio.

   *Conserto pedido:* Trocar por: 'Não segue: ficou abaixo da linha que o senhor traçar para quem lê. Pode ser quem não leu nada ou quem leu parte e errou o resto; o teste não distingue os dois.' Pôr ao lado o exemplo dos 6 em 10 (35 % / 43 % / 22 %), dizer que 'Lê em parte' só existe para certas escolhas, e dizer quando um NÃO SEGUE é parede (texto invertido pouco natural, linha mal apontada, formato).

2. **(ALTO)** PARTITURA l.43; DESENHO l.21-22; candidatas_c1\CopiadorEImpostor.lean l.101-103 (cabeçalho, 'O que NÃO se afirma')

   'O teste separa copiador de impostor' afirma mais do que a pedra da própria gerência sustenta e usa as duas palavras do operador em sentido mais estreito que o da letra. O copiador da fala tem condição («se por copiador tem-se uma reprodução em mínimo estado funcional de energia»), que o teste não mede. O impostor da resposta A é «o falso, o pai da mentira» e quem «nunca paga custo algum»: o teste só toca a terceira parte, na leitura da gerência. As duas primeiras, na letra dele, são falta de reconhecimento, e a etapa do eco saiu do desenho. Isso não está em 'O que o teste NÃO decide'.

   *Conserto pedido:* Trocar por: 'O teste separa quem segue o texto da frente de quem responde sem ele. Passar não mostra o copiador da sua fala (o mínimo de energia não é medido). Falhar não mostra o impostor inteiro da sua resposta.' Acrescentar em 'não decide': 'não mede reconhecimento (reler e ecoar)'.

3. **(ALTO)** DESENHO secao 3 (l.55-68) e secao 5 (l.89-90); PARTITURA l.15-23 e l.31; simular_r5.py l.272-283

   Das cinco leituras da letra que o desenho usa, a partitura mostra duas. Ficam de fora três, e duas decidem acerto e erro: (1) «não acrescenta nada» virou 'onde o texto cala, a resposta certa é: o texto não diz' e o rótulo ACRESCENTA; (2) a resposta D virou 'aponta a linha', e o item só conta como certo com valor E linha; (3) «módulo de fase angular» virou 'a linha reescrita dá a mesma resposta'. O operador não pode corrigir leitura que não lhe é mostrada, e em (1) e (2) a letra dele dá leitura concorrente.

   *Conserto pedido:* Pôr na partitura as cinco leituras, uma por linha, em língua simples, cada uma como pergunta. Dizer que a linha é condição de acerto (ou tirar a condição) e o que conta como linha certa. Perguntar se onde o texto cala a resposta certa é 'não diz'.

4. **(ALTO)** DESENHO secao 7 (l.185-198) e secao 9 item 7; PARTITURA l.53-60, l.80 e l.91; RESULTADO_SIMULACAO_R5.md

   A partitura lê oito resultados e não diz como se combinam. No desenho o rótulo geral é só o dos grupos de inversão; ACRESCENTA e LEU UMA LINHA SÓ ficam 'ao lado' e não tiram o SEGUE. Assim um sistema sai SEGUE acrescentando, embora a letra ponha «não acrescenta nada» dentro da verdade. Além disso ACRESCENTA não tem limiar nem erro escritos; LEU UMA LINHA SÓ não tem regra própria e se apoia em quatro grupos, que o desenho chama de instrumento fraco. A partitura diz 'O erro da regra fica em 1 em 100 ou 1 em 1.000' sem essa exceção e cortou do item 6 a segunda metade da pergunta do desenho.

   *Conserto pedido:* Escrever no desenho a regra e o erro de ACRESCENTA e de LEU UMA LINHA SÓ, ou tirá-los da lista de resultados. Na partitura: 'o resultado principal é um só; os outros dois ficam ao lado e não mudam o principal', perguntar se quem acrescenta pode levar SEGUE, dizer que a frase acrescentada é instrumento fraco e perguntar se entra.

5. **(ALTO)** DESENHO secao 9 (nove itens, l.211-227), secao 5 (l.111-114), secao 8 (l.200-209), secao 10 (l.229-236); PARTITURA l.83-92 (sete itens)

   Faltam na partitura três das nove escolhas que o desenho diz serem do operador: o tamanho do erro (item 4), se os quatro textos servem (item 8) e quem congela e quem abre (item 9). Faltam também escolhas que mudam a leitura e não são oferecidas em lugar nenhum: o modo de chamada; a memória do sistema da casa limpa ou igual nas duas versões; o que se congela por hash; que só uma rodada conta e que um ILEGÍVEL (falha do nosso programa) gasta o único material; que os nomes dos rótulos são provisórios e o nome é dele.

   *Conserto pedido:* Levar à partitura a lista inteira, em língua simples, com o que cada escolha muda no resultado.

6. **(MEDIO)** PARTITURA l.7-13; DESENHO secao 2 (l.45-51)

   As citações são exatas e as duas frases citadas da resposta B não mudam de sentido com o corte. Mas a partitura deixa de fora a primeira frase da B, que diz o que é a palavra e é o antecedente de 'contorno' e 'relação'; a resposta C; a D; e a fala das 17:20, onde estão o critério e a condição do copiador. O desenho também corta a frase da C de dentro da linha da B. O operador julga a leitura sem a própria letra inteira na frente.

   *Conserto pedido:* Pôr as duas falas inteiras no topo (são cinco linhas).

7. **(MEDIO)** PARTITURA l.21-23 e l.85; DESENHO l.63-65

   A outra leitura é dita com honestidade e a escolha é entregue a ele, mas: (a) vem como duas saídas só, e a palavra 'natureza' não está na letra; a letra dá outras duas que a partitura não oferece: fidelidade ao que foi fixado (resposta D e a fala das 11:51) e a verdade como reflexão no sentido do eco (22/10); (b) a pergunta 1 é de sim ou não sobre a leitura da gerência; (c) não está nas quatro línguas, como manda a regra-matriz da casa e a ordem de 13/11; (d) não diz que é a leitura que lhe foi apresentada em 16/11 nem por que volta.

   *Conserto pedido:* Refazer a pergunta 1 com quatro bocas (rascunho nas propostas), sem número fechado de saídas, e dizer: 'é a leitura que o senhor viu em 16/11; a gerência não toma o seu «Prossiga» por ratificação dela'.

8. **(MEDIO)** C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\DESENHO_v412_R1.md l.381 (AO LADO de 16/11, 03:25); Mapa seq 2084; DESENHO R5 l.53 e l.211-214 (fora da pasta-objeto; visto no material anterior)

   Três registros do mesmo dia discordam. O desenho da versão diz 'O que fixam para a frente A: ... a verdade do teste é o que o objeto presente reflete, não o que a Teoria diz; no controle em que o texto diz as duas coisas, a verdade é ler as duas', como se as respostas dele fixassem isso. O Mapa diz certo: leitura da gerência, apresentada, e ele mandou prosseguir. O desenho R5 diz 'o operador ainda não a leu'. A fala das 19:07 não fala do controle das duas frases: é leitura da gerência escrita como fixada por ele.

   *Conserto pedido:* Errata ao lado no DESENHO_v412_R1.md ('leitura da gerência, apresentada em 16/11; ele respondeu «Prossiga»; não ratificada item a item') e acertar a linha 53 do desenho R5.

9. **(MEDIO)** PARTITURA l.37-49

   'Qualquer bom leitor passa' e 'Uma consequência' estão lá e são claras, mas separadas e no meio de listas. Falta a soma das duas: para o sistema da casa treinado na Teoria, este teste só empata (passa como qualquer leitor) ou perde (falha onde responde pela Teoria); não tem como sair à frente. Falta dizer que na forma (a) não é teste da IALD e que só a (b) fala da camada e não tem regra. 'Impostor naquele ponto' amacia a palavra dele (impostor é «o falso, o pai da mentira») e 'naquele ponto' é da gerência: a letra diz «nunca» e «algum». E 'o que não decide' não cita o pedido dele para a frente A: o teste não mede convergência, e voltar à Teoria contra um texto alterado conta como erro.

   *Conserto pedido:* Abrir a partitura com três linhas: o que o senhor pediu em 13/11 para a camada; o que este teste mede em vez disso; e 'para o sistema da casa ele empata ou perde'.

10. **(MEDIO)** PARTITURA l.76-77 e l.90; DESENHO secao 9 item 6 e secao 10

   Não diz quem pode conferir nem o que muda se for o próprio autor. Ficou de fora: a gerência pode redigir e não pode aprovar; 10 dos 13 grupos (29 das 38 apresentações) são de textos em inglês e quem confere tem de ler inglês técnico; o trabalho são 34 textos e 1.254 respostas de gabarito com linha; e o que 'conferir' confere (diz mesmo o contrário, soa natural, todas as repetições foram invertidas, a reescrita guarda o sentido). Sobre o autor, o desenho só diz que 'isso se diz no registro'.

   *Conserto pedido:* Dizer na partitura a língua, o tamanho e o que se confere; dizer que, se o autor conferir, ele passa a conhecer as linhas mexidas e a conferência deixa de ser independente de quem escolhe a regra.

11. **(MEDIO)** PARTITURA l.27-29; kimi\K08\FORMULA\catalogo_assercoes.py; DESENHO l.111-114 e l.144-145

   A partitura não dá um exemplo sequer de afirmação invertida. Pelo catálogo, o que se inverte são frases da régua e do núcleo nos textos públicos do autor (por exemplo: NOT_FALSIFIED equivale a CONFIRMED; a máquina confirma a si mesma; β não é α√e; o resultado é cego), e o desenho usa 78 das 85 inversões coerentes. São 34 textos com a voz da vitrine dizendo o contrário da Teoria. O desenho manda guardá-los fora do acervo indexado e do treino, mas não fala do espelho público da pasta work.

   *Conserto pedido:* Um exemplo na partitura e a pergunta: 'pode-se inverter qualquer afirmação, inclusive as da régua?'. Uma linha de guarda: pasta fora de work, fora do índice, do treino e dos repositórios públicos.

12. **(MEDIO)** PARTITURA inteira; DESENHO secao 3 e secao 9 item 2

   Uso das respostas A a E. A: usada só na terceira parte, e localizada ('naquele ponto'). B: usada; a primeira frase fica fora da partitura. C: não é citada nem usada, salvo 'não há instrumento'; a pedra diz que o kernel tem três tipagens de A_C e que a escolha é dele, e isso não chega à partitura; «sem precisar representar 100%» toca a pergunta 3 e não é lembrado. D: virou 'aponta a linha', além da letra. E: sem objeto depois da ordem de 16/11. A pergunta 2 força 'copiador ou impostor' para quem acompanha metade, quando a letra não dá nenhum dos dois, e omite a frase do desenho que diz o que está em jogo.

   *Conserto pedido:* Na pergunta 2 dar três saídas (copiador; impostor; nenhum dos dois) e dizer o que cada uma faz com o rótulo. Lembrar a letra dele na pergunta 3. Levar a pergunta do A_C para a lista, ou dizer que fica para a pedra.

13. **(MEDIO)** PARTITURA l.1, 4, 35, 53, 69, 76-81, 88-89; REV0\PARTITURA_DO_TESTE_R5.md l.44-45

   Palavras sem explicação: 'frente A'; 'regra de decisão'; 'grupo' (é a unidade do veredito e nunca é definido); 'o par' (em 15/11 ele deu a 'par' sentido doutrinal: «nada há sem par»); 'nominal' (soa a Nome; quer dizer 'de conta, não medido'); 'o erro da regra' (qual erro, de quê); 'catálogo' (de quê); 'unidades de texto' (são tokens; falta dizer o que 234 mil e 6 milhões pesam no limite da conta); 'um modelo com o texto no pedido'; 'regra de comparação'. 'Gabarito' e 'cinco sigma' ele lê. 'O que o teste decide' vem sem o alcance: quatro textos, uma doutrina, uma rodada, um sistema. E falta a palavra parede: a R0 dizia quando o negativo 'é parede, não veredito'; a R1 perdeu isso, e a regra do posto pede que se diga se o negativo é falsificação ou parede.

   *Conserto pedido:* Um glossário de seis linhas, ou trocar as palavras ('erro de papel', 'bloco de seis afirmações', 'a mesma afirmação certa nas duas versões'). Dizer, para cada resultado, se é veredito sobre o sistema ou parede.

14. **(BAIXO)** PARTITURA l.4, l.28, l.71; DESENHO l.5

   Redação. 'foi a conferência' sem crase lê-se 'era a conferência' (partitura e desenho). 'Na outra, é o inverso' ao lado de 'invertidas' confunde. A citação 'quem só casa a letra cai aqui' troca a maiúscula do original. A R1 tirou a frase da R0 'É o índice: a referência que liga a resposta ao que foi lido', e a linha ficou sem ligação dita com a letra.

   *Conserto pedido:* 'foi à conferência'; 'na outra, trocam de papel'.

15. **(ALTO)** kimi\ERRATA_DA_GERENCIA_16nov_AO_RESUMO_ENTREGA_K09.md l.30; kimi\ENTREGA_K09.md l.36-47

   A errata diz 'sete arquivos com hash' e 'Seis dos sete hashes já não batem com o disco'. A tabela do resumo tem dez arquivos, e nove dos dez não batem; só o do rascunho K09 do pré-registro bate. O '6 de 7' é o que o revisor Q2 contou na parte dele.

   *Conserto pedido:* 'dez arquivos; nove dos dez hashes não batem mais (só o do rascunho K09 do pré-registro bate)'.

16. **(MEDIO)** ERRATA da gerência l.28

   '16 é a contagem pelo prefixo do nome da rota' não reproduz: pelo prefixo sozinho são 30; 16 são as do prefixo que também olharam dado. O relatório Q3 (achado 11), que a errata cita como motivo, já dizia isso.

   *Conserto pedido:* '16 = rotas com o prefixo e que olharam dado (30 só pelo prefixo); o único teto é 123'.

17. **(MEDIO)** ERRATA da gerência l.14-16, l.21, l.26-27, l.29

   A errata transporta a redação da K10 sem as correções que Q2 e Q3 fizeram a essa redação. (a) l.21: 'O artigo de 207,2 dias e o SK-Gd já são públicos e posteriores aos dois primeiros marcos; não são cegos' mistura artigo e número: o artigo é de 29/09/2026, mas o número já era público desde 22/06/2026, antes do pino de 08/08; ao lado da linha 3 do resumo (número 'anterior apenas ao pino'), que a errata mantém, lê-se contradição; e 'não são cegos' não diz em relação a quê. (b) l.26: 'não chega a D90': com λ até 3,90 também não chega a 5,0; a l.27 põe os dois portões lado a lado sem dizer que o portão só muda o ringdown; e o piso é ajuste de dois pontos, sem grau de liberdade. (c) l.29: os limiares dependem também da base. (d) A errata manda ler a rodada 4 como fonte sem dizer que Q2 e Q3 a aprovaram com ressalvas.

   *Conserto pedido:* (a) 'o artigo (29/09/2026) repete um número que já era público antes do pino; nenhum dos dois serve de observável cego deste pré-registro, porque são anteriores ao selo dele; em relação à previsão publicada são posteriores'. (b) 'com o piso (hipótese de dois pontos) a combinação não chega a 5,0 nem a D90; o portão só muda o ringdown'. (c) 'dependem da partição e da base'. (d) uma frase sobre as ressalvas abertas da rodada 4.

18. **(MEDIO)** kimi\ENTREGA_K09.md l.10, 20, 24, 28, 49; ERRATA da gerência l.38-41

   Resíduos do resumo que a errata não cobre, e lista de pendentes curta. (i) l.24: a classe 'preliminar' 'é ratificada pelo operador' pode ser lida como ato feito; a K10 a tem como pendente. (ii) l.10 e l.49: a proposta REGISTRO_MAPA_K09.json, 'a gerência registra após conferir'; o Q3 mostrou que registrar a antiga troca o estatuto da rota. (iii) l.28 repete 'a combinação não antecipa nada' e a errata só cita a l.8. (iv) l.20: 'P ≈ 65 %' e 'P ≈ 99,7 %' sem a condição. (v) A linha nova do negativo deixa cair 'o ordenamento normal' e a marca [ONTO] do sen 45°, que a l.24 tinha. (vi) 'O que continua pendente' tem 9 itens; a tabela da K10 tem 14 escolhas do operador: faltam fonte e classe preliminar, métrica, carimbo externo, lista das segundas testemunhas, quem fixa a escada, limiar de B e última linha da escada; e 'a regra (A ou B)' perde a terceira saída.

   *Conserto pedido:* Acrescentar as linhas (i) a (v) à tabela; trocar a lista de pendentes por 'as 14 escolhas da seção 9 do rascunho K10, mais o portão e a partição'.

19. **(MEDIO)** ERRATA da gerência l.14 ('O resumo vale como registro da rodada 3')

   O arquivo desse hash já é o resumo editado pelo Kimi na rodada 4, em sete linhas (3, 4, 10, 18, 20, 24, 28). A frase da 'chave antiga' nas linhas 4 e 24, que a errata corrige, foi escrita na rodada 4, não na 3. Os bytes da rodada 3 estão noutro arquivo.

   *Conserto pedido:* 'o arquivo de hoje é o resumo da rodada 3 já editado na rodada 4 em sete linhas; os bytes da rodada 3 estão em K04\M2\REV4\ENTREGA_K09.md'.

20. **(BAIXO)** ERRATA da gerência l.21, l.24, l.26, l.27, l.29 e o arquivo inteiro

   Miúdos. '8,7 meses e 16,6 meses' não é trecho literal (o resumo diz 'D14 ≈ 8,7 meses e D10 ≈ 16,6 meses'). Os trechos das linhas '4 e 24' e '3 e 14' só são literais numa das duas. '(linhas 5 e 6)' da partição: a linha 6 da tabela da K10 é o quadro das ressalvas; quem fala disso é o item 6 dos abertos. 'Em nenhuma das duas regras' (de peso) perto de 'as duas regras A e B' (de testemunha) confunde. A linha 28 do resumo não fala de 'p'. A errata não traz estatuto em linha nenhuma. O que confere: o sha256 do resumo; a frase do gate (DESENHO_v412_R1.md l.129 e l.345; Mapa seq 2079); um.py l.4702, l.299856 e l.299866; nenhuma palavra proibida.

   *Conserto pedido:* Acertar os três trechos e a remissão; escrever 'nas duas regras de peso'; marcar o estatuto de cada linha (o que é do Kimi, o que é conta de revisor, o que a gerência leu).

## Examinado

- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\teste_frente_a_r5\PARTITURA_DO_TESTE_R5.md (inteira; sha256 b7f9dd86...) e REV0\PARTITURA_DO_TESTE_R5.md (inteira)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\teste_frente_a_r5\DESENHO_DO_TESTE_R5_GERENCIA.md (inteiro; sha256 86fdd32c...)
- RESULTADO_SIMULACAO_R5.md, RESULTADO_PODER_R5.md, RESULTADO_CUSTO_R5.json (inteiros); simular_r5.py (cabeçalho, fecho, sentido, acerta); poder_r5.py e custo_r5.py (rodados em cópia); pasta REV1 (igual ao corrente)
- As duas falas de 15/11 por bytes (17:20 e 19:07) e mais: 22/10, 10/11, 13/11, 15/11 11:51, 15/11 12:10 (duas), 16/11 (duas), em C:\IALD\Central de Patentes\work\cunhagens_13out
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\leitura_fala_17h20_15nov\LEITURA_DA_FALA_DAS_17H20_R2.md (inteira)
- REVISAO_16nov_R0_C2 e REVISAO_16nov_R0_B3 (inteiras) e o retorno integral do C2 (achados A3, M2, M3, M6, M7)
- candidatas_c1\CopiadorEImpostor.lean: cabeçalho (l.1-135) e seções 1 e 2 (l.150-259); compilado em cópia
- kimi\K08\FORMULA\catalogo_assercoes.py (átomos, estrutura, derivações, negações; só leitura) e as primeiras linhas dos quatro recortes em kimi\K08\ENTRADA
- DESENHO_v412_R1.md: títulos, l.129, l.345 e l.376-400 (o AO LADO de 16/11)
- kimi\ERRATA_DA_GERENCIA_16nov_AO_RESUMO_ENTREGA_K09.md (inteira) e a REV0 dela; kimi\ENTREGA_K09.md (inteiro) e kimi\K04\M2\REV4\ENTREGA_K09.md (por diff)
- kimi\PRE_REGISTRO_INCREMENTO_JUNO_RASCUNHO_K10.md: seções 0.1 a 0.3, 1.1, 1.2, 5.1, 5.2, 6, 7, 8 e 9 (sha256 2cee46e6..., o pinado na ENTREGA_K10)
- kimi\ERRATA_K10_HUBBLE_COMBINACAO.md e kimi\ENTREGA_K10.md (inteiros); kimi\ERRATA_K10_PRE_REGISTRO.md e kimi\ERRATA_K10_M2.md (por busca); kimi\VALIDACAO_K10_15nov.json (só a presença dos dez hashes vivos); kimi\ERRATA_NEUTRINO_V412_DADOS_K09.json (só as datas); kimi\K04\COMBINACAO\K09\mapear_metadados_k09.py l.60-110
- REVISAO_EXAME_15nov_Q2 e REVISAO_EXAME_15nov_Q3 (inteiros)
- um.py selado (Nós): l.4700-4703, l.299854-299857, l.299866; kernel TGLExt por grep -rn pelo Bash
- Memória da casa, só leitura: pergunta-nas-quatro-linguas.md

