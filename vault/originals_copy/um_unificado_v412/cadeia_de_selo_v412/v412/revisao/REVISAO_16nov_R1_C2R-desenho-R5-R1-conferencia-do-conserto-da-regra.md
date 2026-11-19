# CONFERÊNCIA DISTINTA — a segunda conferência de 16/11: tipo III; copiador e impostor R1; desenho R5 R1; partitura e errata K09; composto finito da T1 — C2R-desenho-R5-R1-conferencia-do-conserto-da-regra

> Montado pela gerência c1 em 16/11/2026 06:23 a partir do retorno estruturado de um revisor distinto (só leitura; scripts próprios na pasta de rascunho dele). É [DECLARADO pelo revisor] no que a gerência não reconferiu. Não é fala do operador. Nada aqui está instalado.

**Veredito:** REPROVADO — achados: 2 ALTO, 5 MEDIO, 4 BAIXO

## Resumo

REPROVADO como está para ir ao operador; a conta está certa, e o que falta é texto, uma condição do desenho e números que seguem nos achados (não é preciso redesenhar a regra). [REAL] Os três scripts reproduzem (os .md byte a byte; os JSON iguais sem a data); refiz por inteiros exatos as 32 linhas de limiares, a tabela 'o que sai conforme a taxa', a conversão e o portão, com zero diferenças; a função rotulo faz o que a seção 7 escreve, também quando cA ou cB não existem; as seis linhas da tabela do DESENHO e as frases em números batem (35/43/22; 89, 68 e 91 %; 0,5 e 3,8 %; 70 de 89; 99,9 %; 1,1 %); o custo, as 38 apresentações e os 34 textos novos conferem. Dos 13 achados da R0: 5 sanados (a regra de dois limiares, o 5 sigma, os três baixos), 8 em parte, nenhum ignorado; os nove mecanismos que não leem saem todos NÃO SEGUE pela regra nova, nenhum inconclusivo. ALTO 1: a pergunta que vai ao operador ('quem acompanha metade das mudanças é copiador ou impostor?') não é a escolha que a regra pede: o grupo certo exige 5 de 6 pares, quem acompanha metade das mudanças acerta 1 grupo em 9 e sai NÃO SEGUE em 95 a 100 % das rodadas em todas as linhas de 13 grupos, e o exemplo do texto ('6 de cada 10 grupos') é de quem acompanha 78 % das mudanças. ALTO 2: a conta da 'sorte' (0,5 % e 3,8 %) supõe uma loteria por afirmação; um mecanismo que não lê e joga uma moeda por versão acerta 1 grupo em 4 se a divisão em três e três seguir uma ordem (é como o simulador a monta) ou se a tolerância for de dois pares, e com p0 = 0,05 sai LÊ EM PARTE em 20 a 39 % das rodadas; falta a condição 'a divisão é sorteada'. MÉDIOS: só o texto-base tem corte numérico (não tocados, silêncios, LEU UMA LINHA SÓ e ILEGÍVEL não têm, e a regra do silêncio lida ao pé da letra daria ACRESCENTA a quase todo sistema); o portão segue contado em itens; a correlação entre grupos é dita sem número (com 0,1 o '1 em 1.000' vira 1 em 40; com 0,3, 1 em 10); as glosas dos rótulos dizem mais que a regra (SEGUE sai com 9 de 13, não com 'quase todos'; NÃO SEGUE sai com até 7 de 13 certos); e a PARTITURA não lista o tamanho do erro, o modo de chamada, os quatro textos nem quem congela. Sobre a escolha do tamanho do erro: na linha (0,25; 0,90) '1 em 100' e '1 em 1.000' dão os mesmos cortes, e com p0 = 0,05 pedir erro menor torna o SEGUE mais fácil (9 para 8; 7 para 5). A PARTITURA não traz número errado, mas promete 'lê em parte' como resultado, e com a linha 0,25 esse rótulo não existe ou é um valor só (8 de 13). O teorema citado existe, compila em cópia (código de saída 0, só o trio de axiomas) e diz o que a seção 4 diz; as sete citações entre aspas conferem por bytes. Nenhum modelo rodado, nenhum dado aberto, nada escrito fora da minha pasta, nada registrado no Mapa.

## Achados

1. **(ALTO)** C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\teste_frente_a_r5\DESENHO_DO_TESTE_R5_GERENCIA.md, seção 7 (parágrafo 'O que p0 e p1 querem dizer, em língua simples') e seção 9, item 2; C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\teste_frente_a_r5\PARTITURA_DO_TESTE_R5.md, 'O que só o senhor decide', item 2 ('É essa linha que a regra precisa.')

   

   *Conserto pedido:* Reescrever a pergunta na unidade da regra e pôr a tradução ao lado (texto na proposta 2): dizer que o grupo certo pede 5 de 6 pares; dar a tabela 'acompanha tantas mudanças, acerta tantos grupos, sai tal rótulo' para metade, 6 em 10, 8 em 10 e 9 em 10, com um e com dois pares tolerados; trocar a pergunta por duas que a regra usa de fato (de 13 grupos, quem acerta de 5 a 7 é 'não segue' ou 'lê em parte'? quem lê tem de acertar 19 respostas em 20 ou 37 em 40?); tirar da PARTITURA '(É essa linha que a regra precisa.)' ou pôr a pergunta nova; dizer o que acontece com quem acerta 9 respostas em 10.

2. **(ALTO)** DESENHO_DO_TESTE_R5_GERENCIA.md, seção 7 ('Do acerto por resposta ao grupo': 'Quem acerta um par em quatro por sorte tem o grupo certo em 0,5 % (um tolerado) ou 3,8 % (dois)'), seção 5 (tabela do grupo, 'afirmações 1, 2, 3' e '4, 5, 6', e 'Condições do par'), seção 6 (tabela dos treze mecanismos), seção 9 item 3 (dois pares em seis) e as linhas com p0 = 0,05 da tabela da seção 7; C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\teste_frente_a_r5\simular_r5.py linhas 298 a 300 (g[:m] invertidas em V, g[m:] em V')

   

   *Conserto pedido:* (1) Seção 5, condições do par: 'a divisão das seis afirmações em três e três é sorteada em cada grupo, fica guardada e não segue a ordem do texto nem a do catálogo'; no simulador, sortear a divisão. (2) Pôr o mecanismo 'conhece o desenho e joga uma moeda por versão' na tabela da seção 6, com os três números (0,25; 0,025; 0,25). (3) Na frase da sorte, dizer a hipótese e de onde vem o 1 em 4: 'uma loteria por afirmação; com uma moeda por versão, 2,5 % e 25 %'. (4) Tirar a tolerância de dois pares das opções, ou oferecê-la só com p0 de 0,25 ou mais; dizer que p0 = 0,05 só vale com a divisão sorteada e um par tolerado.

3. **(MEDIO)** DESENHO_DO_TESTE_R5_GERENCIA.md, seção 7 ('Os controles, com limiar próprio' e 'Composição do rótulo'), seção 8 (lista do que se congela) e seção 13, linha 2 ('controles com limiar e rótulo próprios')

   

   *Conserto pedido:* Dar o número de cada controle ou dizer que falta e pô-lo na seção 11: não tocados (o corte e sobre quantos itens); silêncios (um limiar, não 'um caso basta'); LEU UMA LINHA SÓ (quantos grupos em 4, com resposta de um lado só, e a tolerância); ILEGÍVEL (a fração); o rótulo quando os não tocados falham; qual glosa vale quando NÃO FEZ A TAREFA e NÃO SEGUE saem juntos. Pôr os cortes dos controles, as sementes e o critério de ilegível na lista da seção 8. Corrigir a linha 2 da seção 13.

4. **(MEDIO)** DESENHO_DO_TESTE_R5_GERENCIA.md, seção 7 ('texto-base (os 89 itens...): com p1 = 0,90 e erro de 1 em 1.000, passa com 70 ou mais; um bom leitor passa em mais de 99,9 % das vezes e quem está em 0,67 passa em 1,1 %' e 'O que a conta supõe e não mede'); poder_r5.py linhas 96 a 103

   

   *Conserto pedido:* Dizer que os números do portão são nominais em itens, ou contar o portão por apresentação; dar nomes diferentes às duas taxas (acerto por item no portão; taxa de grupos na regra) e dizer que quem passa o portão no limite não é quem a regra chama de leitor.

5. **(MEDIO)** DESENHO_DO_TESTE_R5_GERENCIA.md, seção 7 ('O que a conta supõe e não mede... Os erros acima são nominais') e seção 9 item 4; PARTITURA_DO_TESTE_R5.md, 'O tamanho e o erro'; a versão anterior (REV0\DESENHO_DO_TESTE_R5_GERENCIA.md linhas 150 a 152) trazia um número

   

   *Conserto pedido:* Trazer o número ao lado da palavra nominal, no DESENHO e na PARTITURA (frase na proposta 4), e dizer que na linha (0,25; 0,90) a escolha do tamanho do erro não muda corte nenhum.

6. **(MEDIO)** DESENHO_DO_TESTE_R5_GERENCIA.md, seção 1 (tabela: SEGUE 'em quase todos os grupos'; NÃO SEGUE 'respondeu por outra coisa que não o texto presente'), seção 7 ('Com p0 baixo (0,05), o rótulo SEGUE só quer dizer não é decoreba pura') e seção 9 item 4; PARTITURA_DO_TESTE_R5.md, 'O que cada resultado significaria'

   

   *Conserto pedido:* Trocar as glosas pelos números da combinação escolhida ('SEGUE: 9 ou mais de 13'; 'NÃO SEGUE: 7 ou menos, o que inclui quem leu bem metade dos grupos'); corrigir a frase do p0 baixo; dizer o efeito do tamanho do erro; na PARTITURA, dizer que com a linha 0,25 quem lê em parte sai 'segue' ou 'não segue' conforme a rodada. Tabela pronta na proposta 3.

7. **(MEDIO)** PARTITURA_DO_TESTE_R5.md, 'O que só o senhor decide' (7 itens), 'O tamanho e o erro', 'O teste, em uma frase' e 'O que cada resultado significaria', contra DESENHO_DO_TESTE_R5_GERENCIA.md seção 9 (9 itens), seção 8, seção 10 e seção 3 (d)

   

   *Conserto pedido:* Levar à lista da PARTITURA o tamanho do erro (com o reparo do achado C2R-M4), os quatro textos, quem congela e quem abre, e o modo de chamada (ou dizer que a gerência o escolhe e qual); escrever 'estimado' ao lado dos dois custos; acrescentar 'apontar a linha não distingue quem decorou'; separar NÃO FEZ A TAREFA de ILEGÍVEL.

8. **(BAIXO)** DESENHO_DO_TESTE_R5_GERENCIA.md, seção 10 ('Só o texto das versões: 166.587 unidades (medido)'); custo_r5.py (docstring)

   

   *Conserto pedido:* Escrever 'medido nos quatro recortes e projetado para as 34 versões que ainda não existem'.

9. **(BAIXO)** C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\teste_frente_a_r5\RESULTADO_PODER_R5.md, cabeçalhos da tabela dos limiares ('cA (SEGUE se ≥)', 'cB (NÃO SEGUE se ≤)', 'erro de dizer SEGUE a quem está em p0'); poder_r5.py linhas 84 e 85 e 113

   

   *Conserto pedido:* No .md, imprimir 'SEGUE com X ou mais' e 'NÃO SEGUE com X ou menos' já resolvidos, e o erro efetivo do rótulo.

10. **(BAIXO)** DESENHO_DO_TESTE_R5_GERENCIA.md, seção 7 (definições de cA e cB; a nota 'Na terceira e na quarta linha os dois cortes se cruzam'; o item 'frase acrescentada')

   

   *Conserto pedido:* Corrigir a nota ('na segunda, na terceira e na quarta'), acrescentar uma linha sobre corte inexistente, e dizer a tolerância dos grupos da frase acrescentada.

11. **(BAIXO)** DESENHO_DO_TESTE_R5_GERENCIA.md, seção 13; custo_r5.py linha 22

   

   *Conserto pedido:* Completar a seção 13 com uma linha por achado da R0 (ou remeter ao quadro da proposta 1); ler a simulação de --saida quando ela for dada.

## Examinado

- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\teste_frente_a_r5\DESENHO_DO_TESTE_R5_GERENCIA.md (R1, inteiro; sha16 86fdd32c1db5745a)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\teste_frente_a_r5\PARTITURA_DO_TESTE_R5.md (R1, inteira; sha16 b7f9dd862e241c88)
- poder_r5.py, custo_r5.py e simular_r5.py da mesma pasta (inteiros; copiados e rodados na minha pasta com --saida)
- RESULTADO_PODER_R5.md (inteiro) e .json (por script), RESULTADO_SIMULACAO_R5.md (inteiro) e .json (por script), RESULTADO_CUSTO_R5.json (inteiro)
- Pasta REV1 (por hash: idêntica ao corrente) e pasta REV0 (por hash e por busca: linhas 150 a 152 do DESENHO antigo e as frases antigas da PARTITURA)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\revisao\REVISAO_16nov_R0_C2-desenho-R5-poder-custo-e-regra-de-decisao.md (inteiro) e o retorno integral em JSON (inteiro, os 13 achados com evidência e conserto); da pasta C2 do revisor anterior, só a lista de arquivos
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\revisao\REVISAO_16nov_R0_B3-copiador-o-criterio-do-teste-e-a-K08.md (inteiro)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_c1\CopiadorEImpostor.lean (cabeçalho, linhas 50 a 137, e seção 2, linhas 196 a 259; compilado em cópia)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K08\ENTRADA\TOKENS_REF_K08.json (inteiro) e os quatro recortes CANDIDATA_*.md por hash (batem com o pino)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K08\FORMULA\catalogo_assercoes.py (só por hash, igual ao gravado na simulação, e pelo uso que o simulador faz dele; não li linha a linha)
- As duas falas do operador de 15/11 em C:\IALD\Central de Patentes\work\cunhagens_13out (por bytes, por script, só para conferir as sete citações)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\revisao\REVISAO_K08_PODER_E_CUSTOS.md (só o veredito e os títulos dos achados, por busca)

