# CONFERENCIAS DISTINTAS DO RASCUNHO DA ERRATA DO NEUTRINO PARA O CORE DA v412 (15/11/2026)

> Montado pela gerencia c1 em 15/11/2026 16:20 a partir dos retornos estruturados dos agentes (modelo Sonnet, salvo o construtor da fiacao na luz). Cada retorno e' [DECLARADO pelo agente]; o que a gerencia conferiu por conta propria esta' dito na secao "O que a gerencia fez". Nada aqui e' fala do operador. Nada esta' instalado, selado ou aberto.

## O que a gerencia fez

1. Um redator montou o rascunho (R0) a partir da cronologia de 15/11, do um.py selado e do levantamento; um revisor distinto o aprovou com ressalvas (1 achado alto, 8 medios, 7 baixos).
2. Rodada unica de conserto (R1) por outro redator, e conferencia do conserto por outro revisor: aprovado com ressalvas (1 medio: o arquivo de dados e' subconjunto do texto; 6 baixos). O medio esta' respondido na nota que acompanha o rascunho (`errata_neutrino_core_15nov\NOTA_DA_GERENCIA.md`); os baixos ficam como ressalva.
3. O rascunho NAO esta' instalado e pede decisoes do operador antes de virar registro do core.

## Primeira conferencia (sobre o R0)

**Veredito:** APROVADO_COM_RESSALVAS

Revisão distinta do rascunho da errata do neutrino (md 37.849 B a4462251..., json 40.583 B f465e259..., sha lidos por mim). Não há Lean aqui; nada foi compilado.
Passou: as 40 linhas verbatim do um.py (md e json) batem byte a byte com o um.py selado 1203b1f9202020d6 (verificado por script, numeração por quebra de linha binária). Datas e números batem com CRONOLOGIA_NEUTRINO_15nov.json; recalculei a previsão (8,507414 meV; 7,23761 e-5 eV2), as cinco razões (2,206/2,187; 1,938/1,928; 2,953; 3,024; 3,044) e os dias (198, 172, 65). Varredura própria: zero ocorrências da raiz vetada, de poder certificado, de sombra e de aspas angulares; a palavra vetada pela lei da prova só aparece dentro das citações verbatim. Nenhuma fala atribuída ao operador. Nenhuma frase diz ou sugere que o autor viu dado de neutrino antes; a disciplina dos dois eixos está respeitada nas F1 a F13 e nas tabelas.
Não passa como está: 1 ALTO (C1 a C3 e F12 dizem que o verso vale para a tese, mas os versos afirmam publicada a DERIVAÇÃO da fórmula, que os próprios textos de 2025 não contêm; a palavra tese segue sem definição, D5), 7 MEDIO (eixo 2 confunde o hash do objeto original com o do dicionário portado, que cita 10/08/2026 em L4618; F6 tira conclusão de um eixo só; amostras de 59,1 e 207,2 dias não são independentes; a divergência 2,95 e 3,02 já está no Mapa desde 28/09 e a tabela do NuFIT existe como captura com hash; um dos PDFs de 2025 está no disco e o outro difere do servido; F7 omite L2935-2938; F11 usa a chave de tempo errada) e 7 BAIXO.
Em relação ao congelado: a errata é só ao lado (nenhum verso muda; L4241 e L4620 ficam; o hash de cada dicionário congelado permanece, desde que o registro novo fique fora deles); o um.py novo terá, naturalmente, outro sha. Não instalável até corrigir o ALTO e os MEDIO; os consertos são pontuais e nenhum exige refazer a estrutura.

### Achados

1. **(ALTO)** md L30 (C1), L46 (C2), L63 (C3), F12 (L225), D5 (L278); a palavra tese aparece 15 vezes no md

   C1, C2 e C3 dizem que o verso selado vale para a tese, não para o valor de m2. Mas os versos L4222, L4241, L4243 e L4620 dizem que a DERIVAÇÃO m_nu = beta*sin45*1eV foi publicada em 2025 (Zenodo 17526619). O próprio rascunho mostra que isso é falso para a fórmula: 0 de 8.51 e 0 de sin(45 nos dois textos-fonte (conferi também variantes: sin 45, pi/4, 0.0085, 8,5: zero), e o selado L2946-2948 (errata v182) já retirou esse depósito como prioridade da fórmula, do número e da derivação, dizendo que a fórmula que ele traz é outra. Dizer que o verso vale para a tese devolve em parte o que a v182 retirou, e a palavra tese segue sem definição (D5 aberto) enquanto decide o conteúdo de 3 correções.

   *Conserto pedido:* Reescrever o que corrige de C1, C2 e C3 e a F12: o verso afirma que a derivação m = beta*sen45*1 eV foi publicada em 2025; os textos de 2025 não contêm a fórmula nem o valor (0 de 8.51, 0 de sin(45; L2946-2948 já o diz do 17526619); o que os dois artigos de 2025 trazem é [definir: por exemplo o acoplamento não mínimo e a produção de entropia do neutrino, por título], e é isso que antecede o primeiro número do JUNO. Resolver D5 antes de instalar ou trocar a palavra tese por essa descrição literal.

2. **(MEDIO)** md seção 1 Eixo 2 (L19), C3 (L61-64), F9 (L213), F13 (L229), seção 9 (L288)

   O eixo 2 mistura dois hashes. O 4bdae22a277aa393 é do objeto original (arquivo teste_acustico_beta_tgl_v1/02_frozen_neutrino_m2_v2.py, 08/08/2026). O frozen_hash = sha_obj(frozen) de L4632 é de OUTRO objeto: o dicionário L4615-4631 contém a chave portado_de (que cita o hash do original, logo não pode estar dentro dele) e, em L4618, supersedes com '[D2, 10/08/2026]', data posterior a 08/08. Logo o hash que o código calcula não tem data de 08/08, tem data igual ou posterior a 10/08/2026 e a portagem não está datada (D7). A seção 1 escreve 'é o hash do objeto congelado NEUTRINO_M2_V2, de 08/08/2026 (L4617; sha_obj calculado em L4632)', e a F13 e a F9 tratam os dois como um. O rascunho nunca cita o 10/08 de L4618, que está dentro da faixa lida. Para as posições dos degraus não muda nada (22/06 a 22/07 antecedem os dois), mas a frase do eixo fica imprecisa.

   *Conserto pedido:* Na seção 1 e na F13: eixo 2 = hash do objeto original (4bdae22a..., 08/08/2026, L4617); o dicionário portado ao um.py tem hash próprio (L4632), cita uma decisão de 10/08/2026 (L4618) e não está datado (D7). Citar L4618 em C3.

3. **(MEDIO)** md F6 (L201); seção 7 (L269); D8 (L281)

   A F6 termina com 'por isso ela não é a primeira leitura prospectiva da regra congelada'. Essa conclusão sai só do eixo do hash (o número era público antes dele); em relação à previsão publicada a leitura é posterior ao valor. É a forma de frase que a regra de 15/11 proíbe (conclusão sobre prospectiva com um eixo só) e contradiz a seção 7, que diz que a errata não rotula a leitura de 207,2 dias, e o D8, que deixa o rótulo para o operador.

   *Conserto pedido:* Cortar a oração final. Se quiser manter a consequência: 'em relação à previsão publicada, é leitura posterior ao valor; em relação ao hash da regra do código, o número é anterior ao hash; esta errata não a rotula de prospectiva'.

4. **(MEDIO)** md F6 (L201), F8 (L209), seção 5 (L242)

   F6 chama a leitura de 207,2 dias de cega em relação à previsão publicada, e F8 e a seção 5 comparam 2,21 sigma (59,1 dias) com 1,94 sigma (207,2 dias) como série autônoma que caiu. Nada diz que as duas amostras não são independentes. O abstract de 2511.14593 diz 59,1 dias desde agosto de 2025 e o de 2609.37895 diz 207,2 dias de dados; a revisão da casa (REVISAO_K04_M2.md, linhas 55 e 79-81) já registra que a leitura de 207 dias é cumulativa, que não é determinação independente e que a covariância é [OPEN]. Parte dos dados de 207,2 dias existia (e uma parte já era pública, os 59,1 dias) antes da previsão; só o NÚMERO é posterior. Cega pela data do número não é cega pela amostra.

   *Conserto pedido:* Em F6, F8 e seção 5 acrescentar: 'a amostra de 207,2 dias acumula a de 59,1 dias; não são determinações independentes; a correlação é [OPEN]; a cegueira dita é a do número, não a dos dados'.

5. **(MEDIO)** md seção 6 (L246-254), F10 (L217-219), seção 0 (L12), D2 (L275), linha da tabela L165

   A divergência 2,95 versus 3,02 é apresentada como nova e como vinda das fontes do Kimi [DECLARADO]. Ela já está no Mapa desde 28/09: rota neutrinos.m2.normalizacao, seq 93 (RNC-01, ERRO_TECNICO, verificador SUSTENTADO, severidade ALTO: com o NuFIT 6.1 publicado a regra congelada dá 3,02 sigma, TENSION, e não 2,95) e seq 128 (VV-N1: outro ajuste global dá 2,44 sigma); a REVISAO_K04_M2.md (C2) soma Bari 2,86. A rota tem como artefato a captura NuFIT_6.1_v61.tbl-parameters.jpg (sha256 db49ab73...); li a imagem: cabeçalho NuFIT 6.1 (2025), Dm2_21 = 7,537 +0,094 -0,10 nas duas linhas. Portanto a entrada da tabela é [REAL, lida da captura] e não DECLARADO. A frase 'a errata diz os três números' omite 2,44 e 2,86, e faz a divergência parecer só para cima de 3,0. D2 não lê a partitura da consequência: pela revisão C1 o código manda qualquer última linha da escada global maior ou igual a 3,0 a TENSION, e TENSION não é refutação (FALSIFIED exige duas determinações independentes maiores ou iguais a 5 sigma, L4622).

   *Conserto pedido:* Citar seq 93, 128 e 142 e a captura por sha; trocar [DECLARADO pelo Kimi] por [REAL, imagem da casa] na linha 7,537; dizer também 2,86 e 2,44 como reflexos globais ao lado; em D2 acrescentar uma linha: com um erro o código fica em ARMED_CONSISTENT, com o outro em TENSION; TENSION não é falsificação.

6. **(MEDIO)** md seção 9 (L287), F2 (L185-187), C0 (L135), cronologia linhas 1 e 2

   A seção 9 diz que os PDFs servidos pelo Zenodo para os dois artigos de 2025 não estão no disco. Não é assim. C:\IALD\papers_latex\lie_of_light\lie_of_light.pdf tem md5 e7b8976d0227b000eb9871218050bfe9 e 255439 B, idênticos ao checksum do Zenodo 17526619; extraí o texto: 0 de 8.51, 8,51, sin(45, JUNO e meV. Para esse artigo F2 deixa de ser [DECLARADO que o texto-fonte é o do PDF servido] e passa a [REAL]. Para o outro, neutrino_nmc_revised.pdf local tem md5 94fabc12... e 506794 B, diferente do Zenodo 17372599 (ae0f1210..., 506616 B; registro atualizado em 29/10/2025, o PDF local é de 28/10): a checagem de F2 para o primeiro artigo vale para uma versão próxima, não a servida; também 0 de 8.51 e sin(45 nele.

   *Conserto pedido:* Corrigir a seção 9: lie_of_light.pdf do disco é o servido (md5 igual); neutrino_nmc_revised.pdf do disco não é o servido (md5 e tamanho diferem; a versão de 29/10/2025 não está no disco). Registrar em F2 e na cronologia.

7. **(MEDIO)** md F7 (L205), seção 0 (L11)

   F7 sustenta retrodição sem ajuste só em L2951-2952 e na ressalva L2953-2954. Na mesma faixa lida, L2935-2938 diz que sin(45deg) é POSTULADO, não derivado, que é o único fator que leva beta*1eV = 12,03 meV a 8,51 meV, e que a forma sem ele coexiste no documento de origem. Essa é a objeção natural ao sem ajuste e fica omitida. Além disso a seção 0 diz que retrodição sem ajuste conta como evidência de pleno direito sem dizer o sinal: as razões são 2,21 e 1,64 sigma de distância, isto é, evidência com desvio, não a favor por si.

   *Conserto pedido:* Em F7, citar L2935-2938 (ou dizer por que a v405 a supera: o 45 graus é derivado no kernel sob as leituras nomeadas) e acrescentar na seção 0: 'o sinal dessa evidência é o das razões da seção 5 (2,21 e 1,94 sigma de distância)'.

8. **(MEDIO)** md F11 (L221)

   F11 diz que só um número do JUNO 'tomado depois de 18/05/2026' seria cego nos dois eixos. A chave está trocada: 18/05/2026 é o fim da janela de dados da leitura de 207,2 dias, e a cegueira dos dois eixos depende da data da PRIMEIRA PUBLICAÇÃO do número (depois de 08/08/2026, que implica depois de 17/02/2026), não da data de tomada de dados. Um número de dados tomados depois de 18/05 mas tornado público antes de 08/08 seria anterior ao hash; e um número de dados antigos publicado depois não seria informação nova. A frase também afirma a ausência de número posterior por leitura da gerência não reconferida.

   *Conserto pedido:* Reescrever: 'só um número do JUNO tornado público pela primeira vez depois de 08/08/2026 (hash da regra) seria posterior à previsão publicada e ao hash; o artigo de 29/09/2026 não é esse caso, porque o número já era público'. Ou cortar F11 e deixar no desenho da v412 (D8).

9. **(MEDIO)** md seção 0 (L11), F3 (L189), F9 (L213), C5 (L97), cronologia linha 22/01

   Várias frases dizem 'o valor de m2 é de 22/01/2026' ou 'a previsão publicada é de 22/01/2026'. A publicação é de 17/02/2026 (Zenodo, e git público L2942-2943); 22/01/2026 é a data de um documento guardado (mtime 12:40:23, data no corpo e docProps created 2026-01-22T15:31:39Z, este último não usado pelo rascunho), sem carimbo externo. F1 e F2 dizem os dois; as demais só uma. O operador distinguiu acervo (22/01) e Zenodo (17/02).

   *Conserto pedido:* Padronizar: 'nos bytes guardados desde 22/01/2026 (sem carimbo externo) e publicado em 17/02/2026'; citar o docProps como segunda marca interna. Nenhuma posição de degrau muda.

10. **(BAIXO)** md L11 (duas frases), L262, L285

   Frases de antes e depois com um eixo só: 'o valor de m2 é de 22/01/2026, depois do primeiro número do JUNO'; 'diz que a tese é anterior e o valor não'; 'a tese o antecede e o valor não'; 'o número era público antes do hash de 08/08/2026'. A regra do operador pede os dois eixos na mesma frase em tudo que seja antes ou depois. Nenhuma sugere que o autor viu dado; são ordens de datas.

   *Conserto pedido:* Acrescentar o outro eixo em cada uma: 'depois do primeiro número do JUNO (18/11/2025) e antes do hash da regra (08/08/2026)'; 'a tese antecede o primeiro número do JUNO e o valor não, e ambos antecedem o hash'; 'o número era público depois da previsão publicada e antes do hash'.

11. **(BAIXO)** md C6 (L116)

   Em C6 o 'O que corrige' diz, na voz da errata, 'O elemento genuinamente EX ANTE é o refinamento pos-JUNO, de L2955'. É a frase do selado, mas dita sem aspas, parece que a errata a adota; e o resto da mesma frase mostra que o refinamento de 59,1 dias e o NuFIT de jan/2026 são anteriores à previsão publicada, logo não ex ante.

   *Conserto pedido:* Escrever: 'L2955 chama de genuinamente EX ANTE o refinamento pós-JUNO; dito nos dois eixos, o degrau de 59,1 dias e o NuFIT de jan/2026 são anteriores à previsão publicada e não são ex ante em relação a ela; só o número de 207,2 dias é posterior à previsão e é anterior ao hash'.

12. **(BAIXO)** md F9 (L213)

   F9 põe lado a lado 'os limiares foram fixados no objeto congelado de 08/08/2026' e 'depois de o número de 207,2 dias já ser público'. É ordem de datas e o segundo eixo exigido, mas sem a guarda na mesma frase pode ser lida como insinuação de que o autor o via. O selado L4628-4629 diz que a tensão corrente na sessão era 2,95 sigma (NuFIT), e L7 diz que a lista de medidas da regra termina em 2025-12.

   *Conserto pedido:* Acrescentar na frase: '(ordem de datas; a errata não diz o que o autor leu, e o selado L4628-4629 registra 2,95 sigma como a tensão corrente daquela sessão)'.

13. **(BAIXO)** md C4 (L74), F8 (L209), F10 (L217-219)

   Pequenas imprecisões de referência: o cabeçalho de C4 diz L4597-4600 (e L2955-2956) mas o bloco traz L2955-2957; F8 cita L4601 para o 7,8 sigma, linha que está no bloco de C5, não no de C4; F10 diz que o 2,95 do código é a razão em m2 com 7,53 +- 0,10 mas a linha de estatuto só marca como DECLARADO as entradas do Kimi (a entrada do core vem do mandato e de L7, L4642-4644 não lidas; o recálculo 2,953 coincide com os 2,95 de L4598-4599). F8 diz que a projeção de 7,8 sigma vale só se o centro não se mover sem dizer que o centro já se moveu (7,50 para 7,388).

   *Conserto pedido:* Ajustar o cabeçalho de C4 para L2955-2957, citar L4601 em C5 e em F8, marcar a entrada 7,53 +- 0,10 como [DECLARADO via mandato e L7; recálculo coincide], e acrescentar em F8 que o centro já se moveu.

14. **(BAIXO)** md C2 (L45), C7 (L149-154), seção 9 (L290)

   Itens dependentes de leitura não feita: C2 afirma congelado por hash 'dado do mandato' (a linha do hash do V1 fica fora das faixas; só L2935-2938 diz que o frozen não se move); C7 cobre oito lugares que ninguém leu; a escada global (L4636-4669) e a linha do core do NuFIT não foram lidas, e é nelas que o ramo TENSION decide. O rascunho diz isso, mas o que depende da escada (D2, D3, F10) fica sem apoio no selado.

   *Conserto pedido:* Antes do core: ler L4636-4669 e L314-322, L2885, L2896, L4689, L184013, L292284, L302311-302342 por script e anexar as linhas verbatim, ou retirar C7 e D3 da errata.

15. **(BAIXO)** md/json blocos verbatim

   O md normaliza a indentação das linhas citadas (rótulo L#### mais um espaço e a indentação original). O json guarda o texto exato com indentação. Os 40 versos conferem nos dois (0 divergências), então não é defeito de conteúdo; só avisar quem for instalar que a fonte exata é o json.

   *Conserto pedido:* Nota de uma linha: o campo verbatim do json é o exato.

16. **(BAIXO)** o que falta para virar registro do core

   O que falta antes de a errata virar registro do core: (1) corrigir o ALTO e os MEDIO e rerodar gera_rascunho e a varredura (reuso de meu confere_verbatim.py e varre_eixos.py); (2) decisões D1 a D8, em especial D1 (forma e id; o E44 é só DECLARADO via L7, a conferir no core), D2 e D3 (qual determinação e qual erro do NuFIT), D5 (tese); (3) o registro novo fica FORA de qualquer dicionário frozen, com o sha256 do md e do json pinados nele, e um teste de que sha_obj(frozen) de NEUTRINO_SUM_V1 e de NEUTRINO_M2_V2 é idêntico antes e depois; o um.py novo muda de sha, os frozen não; (4) fontes: captura bruta das datas de 22/06, 15/07, 22/07/2026 e 18/05/2026 (D4), do arXiv 2601.09791 v1 e v2 (eq. 11) e da data de 10/06/2026 da Nature; (5) conciliar com ERRATA_NEUTRINO_V412_RASCUNHO_K04.md e REVISAO_K04_M2.md; (6) registrar no Mapa com sha (a rota K04 já cita a cronologia); (7) segunda revisão distinta das correções; (8) o operador ler a seção 0 e o D2 na língua dele antes de qualquer desfecho do rito.

   *Conserto pedido:* Seguir a lista; nada disso é feito pelo rascunho.

## O conserto (R1), achado por achado

Rodada unica de conserto feita: R1 gerada por script (gera_rascunho_R1.py), md e json iguais em conteudo (224 campos conferidos, 0 ausentes). W1 ficou intacta (md a4462251..., json f465e259..., mtime 15:28). Os 16 achados foram tratados: o ALTO e os 8 MEDIO aplicados, 6 BAIXOS aplicados e 1 aplicado em parte. Varredura do rascunho: 0 achados. Varredura propria, mais estrita: 0 vetos, 0 atribuicao ao operador, 0 postdic fora de citacao; 8 unidades no md e 10 no json ficam sinalizadas, todas conferidas a mao (citacao de verso, data de arquivo ou de hash, uma quebra falsa em eq.), nenhuma de leitura do neutrino. Conferidor verbatim: sha do um.py igual ao selado v411, 48 versos (45 linhas distintas) iguais ao um.py em md e json, blocos do md iguais aos do json. Nao li o um.py fora das faixas; nada instalado, nada registrado no Mapa (so consultas), nada tocado fora de W1b.

- **ALTO: C1, C2, C3, F12 dizem que o verso vale para a tese; D5 sem definicao**: Nova secao 1B: o que cada verso afirma (L4222-4225, L4241, L4243, L4620 citam so o Zenodo 17526619 e dizem derivacao publicada em 2025); o que os textos de 2025 NAO contem, com contagem por script (8,5x/0,0085, sin..45, 45 graus/pi/4, 1 eV, raiz de e, meV, JUNO: zero no PDF servido do 17526619, na descricao dos dois registros e nos .tex; meV=1 so no 17372599, intervalo generico); o que contem, por titulo e resumo (A: acoplamento nao minimo por producao de entropia, xi_nu ~ 0; B: neutrino como resto temporal de foton, mais eq. 28 m_nu(dt)=m_0+alfa*log(dt/tau_0), tres simbolos contra os 'dois parametros livres' de L2948). C1-C3, F12, F2, F3 e a secao 0 reescritos: o verso erra na derivacao, o selado ja retirou em L2944-2950 e a R1 estende; tese definida uma vez (so titulo+resumo, sem formula nem valor); D5 passa a perguntar se essa definicao vale.
- **MEDIO (a): eixo 2 mistura dois hashes**: Secao 1, C3, F9, F13, cronologia, D7, limites: hash do objeto original (4bdae22a277aa393, 08/08/2026, L4617) separado do hash do dicionario portado (calculado em L4632; cita decisao de 10/08/2026 em L4618; logo 10/08/2026 ou posterior; data da portagem nao estabelecida). Marcado como inferencia da gerencia (sha_obj nao lida). Nova linha 2026-08-10 na cronologia; L4618 incluido no verbatim de C3. Nenhuma data inventada; o limite superior (seq 128 do Mapa, 28/09) fica como DECLARADO e dito nao ser data.
- **MEDIO (b): F6 conclui prospectiva com um eixo**: Oracao final cortada. F6 agora diz posterior ao valor (previsao publicada), numero anterior ao hash, e que a errata nao rotula a leitura de prospectiva, cega nem retrodicao.
- **MEDIO (c): 59,1 e 207,2 dias nao independentes**: F6, F8, F11 e secao 5: a amostra de 207,2 dias acumula a de 59,1; nao sao determinacoes independentes; correlacao [OPEN] (REVISAO_K04_M2.md L55, L79-81); a cegueira dita e a do numero, nao a dos dados. Acrescentado, como DECLARADO de resumo secundario da revisao, que a selecao mudou (volume fiducial e corte de acidentais). F8 diz tambem que o centro ja se moveu (7,50 para 7,388).
- **MEDIO (d): divergencia 2,95 x 3,02 ja esta no Mapa**: Secao 6 e F10 citam seq 93 (RNC-01), 128 (VV-N1) e 142 (que reclassifica RNC-01 como PARCIAL) da rota neutrinos.m2.normalizacao e a captura NuFIT_6.1_v61.tbl-parameters.jpg (sha256 db49ab73..., conferido por script contra o Mapa e lido como imagem: 7,537 +0,094 -0,10, cabecalho NuFIT 6.1 (2025)). Linha da tabela passa de DECLARADO pelo Kimi a REAL, captura da casa. Adicionados ao lado Capozzi 2,444 (recalculado de 7,48 +- 0,10) e Bari 2,86 (REVISAO L104, nao conferido). D2 ganhou: um erro da ARMED_CONSISTENT, outro TENSION (seq 93); TENSION nao e falsificacao (L4622); REVISAO item 7: parede medida. Novo bloco C0c cita L4621-4623 verbatim.
- **MEDIO (e): PDFs de 2025 no disco**: Medido por script: lie_of_light.pdf do disco e o servido (md5 e7b8976d..., 255439 B, igual ao Zenodo 17526619; texto extraido tem zero em todas as cadeias); neutrino_nmc_revised.pdf do disco NAO e o servido (md5 94fabc12..., 506794 B, 28/10/2025, contra ae0f1210..., 506616 B, atualizado em 29/10/2025). Secao 9, 1B, F2, cronologia e verificacoes corrigidas; F2 sai de DECLARADO para REAL no 17526619 e fica 'versao proxima' no 17372599. O .tex do 17526619 (12/11/2025) e posterior ao deposito: vale o PDF.
- **MEDIO (f): F7 omite L2935-2938 e o sinal**: F7 cita L2935-2938 (sen 45 POSTULADO, unico fator de 12,03 a 8,51 meV), em bloco verbatim novo C0b, com a nota de que a atribuicao a uma ordem de 20/08/2026 e do verso e nao foi reconferida. Diz o que a v405 mudou segundo C:\IALD\CLAUDE.md (itens 1 e 2, erratas de 01/11): unicidade do 45 e duas derivacoes nas pedras candidatas, mas o angulo continua leitura do operador (escrito em transicaoDerivada), sen2(pi/4)=1/2 e coincidencia de valor e nao ponte, 1 eV e o Um posto (L4621); o selado v411 segue dizendo POSTULADO. Sinal da evidencia dito: 2,21 e 1,94 sigma de distancia, observado acima da previsao (8,660 e 8,595 contra 8,5074 meV).
- **MEDIO (g): F11 com chave de tempo errada**: F11 reescrita: so um numero tornado publico pela primeira vez depois de 08/08/2026 seria posterior ao hash e a previsao publicada; o artigo de 29/09 nao e esse caso; a data de 18/05/2026 deixou de ser a chave. D8 ajustado.
- **MEDIO (h): 22/01 x 17/02 padronizados**: Constante unica em todas as frases: 22/01/2026 nos bytes guardados, sem carimbo externo; 17/02/2026 publicado. Marcas internas do docx lidas por script (docProps created e modified 2026-01-22T15:31:39Z, mtime 12:40:23). De passagem corrigido o texto anterior, que dizia 8,5074 nos documentos: eles trazem 8,51 meV (8,5074 tem contagem zero no docx; e conta por script).
- **BAIXO 1: ordens de datas com um eixo**: Secao 0, F3, F12, NAO_DIZ, limites e a cronologia do NuFIT de 2025-11 passaram a dizer previsao publicada e hash da regra na mesma frase. Varredura propria estendida a anterior/posterior/antecede/depois/antes.
- **BAIXO 2: C6 adota a frase do selado**: C6 reescrito como o revisor propos: L2955 chama de EX ANTE o refinamento pos-JUNO e a errata nao adota a frase; 59,1 dias e NuFIT de 2025-11 sao anteriores a previsao publicada; so o numero de 207,2 dias e posterior a ela e anterior ao hash.
- **BAIXO 3: guarda na F9**: Parentese de guarda acrescentado: ordem de datas, a errata nao diz o que o autor leu, L4628-4629 registra 2,95 sigma como a tensao corrente daquela sessao.
- **BAIXO 4: referencias de linha e estatutos**: Cabecalho de C4 vira L4597-4600 e L2955-2957; F8 cita L4600-4601 dizendo que L4601 esta no bloco de C5; entrada 7,53 +- 0,10 marcada DECLARADO via mandato e L7 (recalculo coincide; Mapa seq 142 a le como a eq. 11 arredondada); F8 diz que o centro ja se moveu.
- **BAIXO 6: nota sobre o campo verbatim exato**: Nota no cabecalho do md e campo nota_sobre_o_verbatim no json: o json guarda o texto exato; o md traz rotulo L, um espaco e o mesmo texto.
- **BAIXO 7: lista do que falta antes do core**: Nova secao 11 (e campo o_que_falta_antes_do_core no json) com os oito itens, ajustados ao que a R1 ja fez (item 1 vira: falta a segunda revisao distinta da R1).
- **BAIXO 5 (em parte): itens que dependem de leitura nao feita**: C2 ganhou a ressalva de que L2938 diz que o hash de um dict frozen nao se move mas nao se sabe a qual; C7, D3, D2, F10 e F12 marcados como dependentes de linhas nao lidas (secoes 9 e 11). Nenhuma linha fora das faixas foi lida nem inventada.

### Nao aplicados, com a razao

- **BAIXO 5, parte: ler L4636-4669, L314-322, L2885, L2896, L4689, L184013, L292284, L302311-302342 e anexar verbatim, ou retirar C7 e D3**: A ordem manda deixar na lista do que falta o que depende de leitura grande fora das faixas. C7, D3 e a escada global ficaram, marcados como DECLARADO via L7 e listados na secao 11 item 4. Nao retirei C7 nem D3 porque isso e decisao do operador (D6).
- **Conciliar o rotulo do 2,44 sigma (Capozzi no titulo da rota e no seq 128; Bari no seq 93) e conferir o 2,86 do Bari 2026.a**: Sem as entradas do Bari 2026.a nem fonte do 2,86 nao ha como conferir por script e a rede esta proibida. Dito ao lado na secao 6, com a divergencia de rotulo explicita, e na secao 11 item 6. O 2,44 foi recalculado de 7,48 +- 0,10 (2,444).
- **Fonte guardada para as datas de 22/06, 15/07, 22/07/2026, de 18/05/2026, do arXiv 2601.09791 v1/v2 e da Nature de 10/06/2026**: Exige rede, vedada nesta tarefa. Continuam [DECLARADO pelo Kimi]; D4 e secao 11 item 5 as listam.
- **Serie de 8 unidades no md e 10 no json que a varredura propria ainda sinaliza (ordem de datas sem os dois eixos)**: Revistas a mao: sao paráfrases de verso selado (ANTES do codigo, L4223 e L4241-4243), datas de arquivo (.tex de 12/11/2025 posterior ao deposito de 04/11/2025), datas dos dois hashes entre si (10/08/2026 posterior a 08/08/2026) e uma quebra falsa em 'eq. 11'. Nenhuma e leitura do neutrino; acrescentar os eixos ali seria ruido. Ficam listadas aqui para o revisor.

## Conferencia do conserto (sobre o R1)

**Veredito:** APROVADO_COM_RESSALVAS

Conferi só o conserto do R1 (md 68.115 B sha256 4672e904..., json 66.058 B sha256 e0fba147..., lidos por mim). O ALTO (a palavra tese) e os 8 MEDIO foram aplicados como pedido, ou com razão boa, e nenhum defeito novo de conteúdo apareceu nas frases. Verificado por script próprio, não pelos do redator: (1) o um.py tem 46.828.680 B e sha256 1203b1f9202020d6..., o da v411 selada; os 48 versos citados (45 linhas distintas) são iguais byte a byte ao um.py, no md e no json. (2) Varredura própria de todas as frases com antes, depois, anterior, posterior, cega, prospectiva ou 207: todas as que falam de leitura de neutrino trazem os dois eixos; as poucas sem os dois falam de mtime de arquivo, de ordem de instalação ou de um verso citado. Zero ocorrências da raiz vetada, de sombra, de poder certificado, de aspas angulares e de fala atribuída ao operador; a palavra vetada pela lei da prova só aparece dentro dos versos citados. (3) Fontes de 2025: título e resumo de cada artigo batem com as respostas cruas do Zenodo; a eq. 28 e a seção 4.4.3 do lie_of_light.pdf existem; as contagens zero (valor, fórmula, 1 eV, raiz de e, JUNO) e o único meV do neutrino_nmc_revised conferem; md5 e tamanhos dos dois PDFs do disco conferem (um é o servido, o outro não). (4) Mapa seq 93, 128 e 142 (RNC-01 ALTO, depois PARCIAL; Capozzi 2,44), REVISAO_K04_M2.md L55, L79-81, L90, L104 e o item 7, a captura NuFIT (li a imagem: 7,537 +0,094 -0,10 nos dois ordenamentos), o docx (docProps 2026-01-22T15:31:39Z, 8.51 três vezes) e os dias 198, 172, 65, 91 conferem. W1 segue intacta. Ressalva que impede dizer que md e json são iguais: o json é um subconjunto estruturado do md, e a checagem do redator só ia do json para o md (um único sentido). Há prosa só no md, incluindo o parágrafo que define a palavra tese e a introdução da seção 6 com os estatutos do Mapa. Nenhuma contradição entre os dois foi achada, salvo a referência de linha do achado BAIXO 3. Scripts e saídas em C:\Users\rotol\AppData\Local\Temp\claude\b4ca26c934d2167f\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v412_frente_b\V_W1b.

### Achados

1. **(MEDIO)** md seção 0; seção 1B (parágrafos O que os versos selados afirmam, A palavra tese e Consequência); seção 5 (parágrafo final); seção 6 (introdução com Mapa seq 93, 128 e 142 e o parágrafo Em palavras simples); json inteiro

   O md e o json não dizem o mesmo. O json é um subconjunto estruturado do md; a checagem do redator (confere_md_json_R1.py) só verifica que cada campo do json aparece no md, nunca o inverso, então a frase md e json iguais em conteúdo não está demonstrada. Conferi nos dois sentidos: a seção 0, os três parágrafos da 1B, o parágrafo final da seção 5 e a introdução da seção 6 existem só no md. Perde-se no json a definição própria da palavra tese (só sobra a versão inline do D5, que remete a uma seção 1B que o json não tem), e os estatutos do Mapa citados no conserto do achado de divergência 2,95 e 3,02 (SUSTENTADO, ERRO_TECNICO, ALTO e depois PARCIAL; os termos SUSTENTADO, ERRO_TECNICO e PARCIAL têm zero ocorrências no json). Como o próprio rascunho diz que na instalação vale o json, esse conteúdo não seria registrado.

   *Conserto pedido:* Ou acrescentar ao json um campo com essas prosas (secao_0, secao_1B_prosa, secao_5_paragrafo, secao_6_introducao), ou declarar no cabeçalho de ambos que o md é o superset e o json o subconjunto estruturado, e fixar o sha256 dos dois. Rodar a conferência nos dois sentidos antes de afirmar igualdade.

2. **(BAIXO)** md seção 1B, primeiro artigo de 2025 (linha Declara resultados observacionais)

   A frase lista resultados do artigo de 2025 sobre SN 1987A e IceCube (dados de neutrino astrofísico) sem dizer que são outros conjuntos de dados, e que não há número do JUNO nem de Δm²₂₁ nele (JUNO tem contagem zero). A frase é fiel ao resumo, mas é a forma que a regra de 15/11 existe para evitar que se leia como o autor olhou dado de neutrino antes.

   *Conserto pedido:* Acrescentar uma cláusula: conjuntos de outros experimentos, sem o número do JUNO e sem Δm²₂₁; esta errata não diz o que o autor leu.

3. **(BAIXO)** md seção 9 (penúltimo item de carimbo externo) e eixo 1 da seção 1

   Diz que a publicação com carimbo externo é a de 17/02/2026. No registro do Zenodo 18674475, 17/02/2026 é o publication_date e o registro foi criado em 20/02/2026 (a seção 1 já diz isso). Nenhuma posição de degrau muda (172 dias até o hash contra 169).

   *Conserto pedido:* Escrever: publicado em 17/02/2026 segundo o publication_date do registro e o git; carimbo de criação do registro 20/02/2026.

4. **(BAIXO)** json divergencia_nufit, campo no_um_py da linha juno_longa; md seção 6, linha do código selado

   O json diz L4636-4644 e o md diz L4642-4644 para a entrada NuFIT do core, não lida aqui. O próprio L7 usa as duas grafias.

   *Conserto pedido:* Uniformizar na leitura de L4636-4669 já listada no item 4 da seção 11.

5. **(BAIXO)** md C3 (L4618), seção 3 (linha 2026-08-10), D7

   Chama de decisão D2 o que o verso traz como [D2, 10/08/2026]; o verso não diz que é decisão, e a sigla D2 colide com o D2 da seção 8 desta errata.

   *Conserto pedido:* Dizer: a marca D2 de 10/08/2026 em L4618 (referência não identificada) e usar outro rótulo.

6. **(BAIXO)** md F9

   A primeira oração fala em depois do número de 207,2 dias com o eixo do hash escrito como objeto original de 08/08/2026, sem a palavra hash. É o segundo eixo, mas só implícito.

   *Conserto pedido:* Trocar por: fixados no objeto original, de hash de 08/08/2026.

7. **(BAIXO)** md seção 3 (linha 2026-01-22), F7

   O 8,67 meV, valor experimental que o documento de 22/01/2026 cita junto da previsão, não tem fonte identificada na errata; as contas do próprio rascunho o põem mais perto do PDG e do NuFIT (8,677) do que do JUNO de 59,1 dias (8,660), mas isso é inferência de quem lê.

   *Conserto pedido:* Dizer que a origem do 8,67 não foi identificada, e deixar a leitura para a decisão do operador.

