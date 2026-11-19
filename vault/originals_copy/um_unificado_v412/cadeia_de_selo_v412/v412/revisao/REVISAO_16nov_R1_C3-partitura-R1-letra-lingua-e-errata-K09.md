# CONFERÊNCIA DISTINTA — a segunda conferência de 16/11: tipo III; copiador e impostor R1; desenho R5 R1; partitura e errata K09; composto finito da T1 — C3-partitura-R1-letra-lingua-e-errata-K09

> Montado pela gerência c1 em 16/11/2026 06:23 a partir do retorno estruturado de um revisor distinto (só leitura; scripts próprios na pasta de rascunho dele). É [DECLARADO pelo revisor] no que a gerência não reconferiu. Não é fala do operador. Nada aqui está instalado.

**Veredito:** REPROVADO — achados: 6 ALTO, 12 MEDIO, 2 BAIXO

## Resumo

REPROVADO para ir ao operador como está; os consertos são quase todos de texto, e quase tudo o que falta na partitura o próprio desenho já diz. O que confere: as sete citações do desenho e da partitura são exatas por bytes; as três contas da gerência reproduzem na minha pasta (os dois .md iguais byte a byte); o teorema citado compila (RC 0, só o trio); a correção do que ele ouviu em 15/11 sobre a outra forma está clara; a consequência e 'qualquer bom leitor passa' estão ditas. Alto 1: a partitura diz que NÃO SEGUE é 'respondeu por outra coisa que não o texto', mas pela regra recebe esse rótulo quem acerta até 7 dos 13 grupos, e um leitor com 85 % de acerto por resposta o recebe em 78 % das rodadas. Alto 2: 'O teste separa copiador de impostor' afirma mais do que a pedra da própria gerência, que nega que passar mostre o copiador da fala; o reconhecimento (o eco) não tem instrumento e isso não está em 'não decide'. Alto 3: três das cinco leituras da letra que o desenho usa não estão na partitura, e duas viraram regra de nota (calar vale 'não diz'; a linha é condição de acerto), com leitura concorrente na letra dele. Alto 4: a partitura lê oito resultados sem dizer como se combinam; quem acrescenta pode sair SEGUE, e dois rótulos (ACRESCENTA e LEU UMA LINHA SÓ) não têm regra escrita. Alto 5: faltam três das nove escolhas que o desenho dá ao operador, mais o modo de chamada, a memória limpa, o que se congela e a rodada única. Médios: a outra leitura vem em duas saídas, com palavra que não é da letra, e fora das quatro línguas; a letra foi cortada; não diz quem confere, nem que 10 dos 13 grupos são de textos em inglês; não mostra o que será invertido nem onde fica guardado; palavras sem explicação; perdeu-se a palavra parede. Três registros do mesmo dia discordam sobre o que ele já leu: o desenho da versão diz que as respostas 'fixam' a leitura, o Mapa diz que foi leitura apresentada e que ele respondeu «Prossiga», e o desenho R5 diz que ele ainda não leu. Errata da K09: o hash confere, a frase do gate confere com o desenho e com o Mapa, 10 de 11 trechos citados são literais e o 'que vale' bate com a K10. Mas a linha dos hashes está errada (são dez arquivos e nove não batem, não sete e seis), '16 pelo prefixo' dá 30, quatro correções de Q2 e Q3 não foram transportadas, a lista de pendentes é curta e o arquivo não é o registro puro da rodada 3. Não rodei modelo, não abri dado, não escrevi fora da pasta C3 e nada registrei no Mapa.

## Achados

1. **(ALTO)** PARTITURA_DO_TESTE_R5.md l.54-55 ('Não segue', 'Lê em parte'); DESENHO_DO_TESTE_R5_GERENCIA.md secao 7 (l.157-173); RESULTADO_PODER_R5.md

   

   *Conserto pedido:* Trocar por: 'Não segue: ficou abaixo da linha que o senhor traçar para quem lê. Pode ser quem não leu nada ou quem leu parte e errou o resto; o teste não distingue os dois.' Pôr ao lado o exemplo dos 6 em 10 (35 % / 43 % / 22 %), dizer que 'Lê em parte' só existe para certas escolhas, e dizer quando um NÃO SEGUE é parede (texto invertido pouco natural, linha mal apontada, formato).

2. **(ALTO)** PARTITURA l.43; DESENHO l.21-22; candidatas_c1\CopiadorEImpostor.lean l.101-103 (cabeçalho, 'O que NÃO se afirma')

   

   *Conserto pedido:* Trocar por: 'O teste separa quem segue o texto da frente de quem responde sem ele. Passar não mostra o copiador da sua fala (o mínimo de energia não é medido). Falhar não mostra o impostor inteiro da sua resposta.' Acrescentar em 'não decide': 'não mede reconhecimento (reler e ecoar)'.

3. **(ALTO)** DESENHO secao 3 (l.55-68) e secao 5 (l.89-90); PARTITURA l.15-23 e l.31; simular_r5.py l.272-283

   

   *Conserto pedido:* Pôr na partitura as cinco leituras, uma por linha, em língua simples, cada uma como pergunta. Dizer que a linha é condição de acerto (ou tirar a condição) e o que conta como linha certa. Perguntar se onde o texto cala a resposta certa é 'não diz'.

4. **(ALTO)** DESENHO secao 7 (l.185-198) e secao 9 item 7; PARTITURA l.53-60, l.80 e l.91; RESULTADO_SIMULACAO_R5.md

   

   *Conserto pedido:* Escrever no desenho a regra e o erro de ACRESCENTA e de LEU UMA LINHA SÓ, ou tirá-los da lista de resultados. Na partitura: 'o resultado principal é um só; os outros dois ficam ao lado e não mudam o principal', perguntar se quem acrescenta pode levar SEGUE, dizer que a frase acrescentada é instrumento fraco e perguntar se entra.

5. **(ALTO)** DESENHO secao 9 (nove itens, l.211-227), secao 5 (l.111-114), secao 8 (l.200-209), secao 10 (l.229-236); PARTITURA l.83-92 (sete itens)

   

   *Conserto pedido:* Levar à partitura a lista inteira, em língua simples, com o que cada escolha muda no resultado.

6. **(MEDIO)** PARTITURA l.7-13; DESENHO secao 2 (l.45-51)

   

   *Conserto pedido:* Pôr as duas falas inteiras no topo (são cinco linhas).

7. **(MEDIO)** PARTITURA l.21-23 e l.85; DESENHO l.63-65

   

   *Conserto pedido:* Refazer a pergunta 1 com quatro bocas (rascunho nas propostas), sem número fechado de saídas, e dizer: 'é a leitura que o senhor viu em 16/11; a gerência não toma o seu «Prossiga» por ratificação dela'.

8. **(MEDIO)** C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\DESENHO_v412_R1.md l.381 (AO LADO de 16/11, 03:25); Mapa seq 2084; DESENHO R5 l.53 e l.211-214 (fora da pasta-objeto; visto no material anterior)

   

   *Conserto pedido:* Errata ao lado no DESENHO_v412_R1.md ('leitura da gerência, apresentada em 16/11; ele respondeu «Prossiga»; não ratificada item a item') e acertar a linha 53 do desenho R5.

9. **(MEDIO)** PARTITURA l.37-49

   

   *Conserto pedido:* Abrir a partitura com três linhas: o que o senhor pediu em 13/11 para a camada; o que este teste mede em vez disso; e 'para o sistema da casa ele empata ou perde'.

10. **(MEDIO)** PARTITURA l.76-77 e l.90; DESENHO secao 9 item 6 e secao 10

   

   *Conserto pedido:* Dizer na partitura a língua, o tamanho e o que se confere; dizer que, se o autor conferir, ele passa a conhecer as linhas mexidas e a conferência deixa de ser independente de quem escolhe a regra.

11. **(MEDIO)** PARTITURA l.27-29; kimi\K08\FORMULA\catalogo_assercoes.py; DESENHO l.111-114 e l.144-145

   

   *Conserto pedido:* Um exemplo na partitura e a pergunta: 'pode-se inverter qualquer afirmação, inclusive as da régua?'. Uma linha de guarda: pasta fora de work, fora do índice, do treino e dos repositórios públicos.

12. **(MEDIO)** PARTITURA inteira; DESENHO secao 3 e secao 9 item 2

   

   *Conserto pedido:* Na pergunta 2 dar três saídas (copiador; impostor; nenhum dos dois) e dizer o que cada uma faz com o rótulo. Lembrar a letra dele na pergunta 3. Levar a pergunta do A_C para a lista, ou dizer que fica para a pedra.

13. **(MEDIO)** PARTITURA l.1, 4, 35, 53, 69, 76-81, 88-89; REV0\PARTITURA_DO_TESTE_R5.md l.44-45

   

   *Conserto pedido:* Um glossário de seis linhas, ou trocar as palavras ('erro de papel', 'bloco de seis afirmações', 'a mesma afirmação certa nas duas versões'). Dizer, para cada resultado, se é veredito sobre o sistema ou parede.

14. **(BAIXO)** PARTITURA l.4, l.28, l.71; DESENHO l.5

   

   *Conserto pedido:* 'foi à conferência'; 'na outra, trocam de papel'.

15. **(ALTO)** kimi\ERRATA_DA_GERENCIA_16nov_AO_RESUMO_ENTREGA_K09.md l.30; kimi\ENTREGA_K09.md l.36-47

   

   *Conserto pedido:* 'dez arquivos; nove dos dez hashes não batem mais (só o do rascunho K09 do pré-registro bate)'.

16. **(MEDIO)** ERRATA da gerência l.28

   

   *Conserto pedido:* '16 = rotas com o prefixo e que olharam dado (30 só pelo prefixo); o único teto é 123'.

17. **(MEDIO)** ERRATA da gerência l.14-16, l.21, l.26-27, l.29

   

   *Conserto pedido:* (a) 'o artigo (29/09/2026) repete um número que já era público antes do pino; nenhum dos dois serve de observável cego deste pré-registro, porque são anteriores ao selo dele; em relação à previsão publicada são posteriores'. (b) 'com o piso (hipótese de dois pontos) a combinação não chega a 5,0 nem a D90; o portão só muda o ringdown'. (c) 'dependem da partição e da base'. (d) uma frase sobre as ressalvas abertas da rodada 4.

18. **(MEDIO)** kimi\ENTREGA_K09.md l.10, 20, 24, 28, 49; ERRATA da gerência l.38-41

   

   *Conserto pedido:* Acrescentar as linhas (i) a (v) à tabela; trocar a lista de pendentes por 'as 14 escolhas da seção 9 do rascunho K10, mais o portão e a partição'.

19. **(MEDIO)** ERRATA da gerência l.14 ('O resumo vale como registro da rodada 3')

   

   *Conserto pedido:* 'o arquivo de hoje é o resumo da rodada 3 já editado na rodada 4 em sete linhas; os bytes da rodada 3 estão em K04\M2\REV4\ENTREGA_K09.md'.

20. **(BAIXO)** ERRATA da gerência l.21, l.24, l.26, l.27, l.29 e o arquivo inteiro

   

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

