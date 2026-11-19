# CONFERÊNCIA DISTINTA — as entregas do Codex (unidade do tipo III) e do Kimi (K10), examinadas por ordem do operador — Q3-K10-hubble-combinacao-e-processo

> Montado pela gerência c1 em 15/11/2026 19:34 a partir do retorno estruturado de um revisor distinto (só leitura; scripts próprios na pasta de rascunho dele). É [DECLARADO pelo revisor] no que a gerência não reconferiu. Não é fala do operador. Nada aqui está instalado.

**Veredito:** APROVADO_COM_RESSALVAS — achados: 1 ALTO, 9 MEDIO, 5 BAIXO

## Resumo

1. Das 14 ressalvas do relatório de Hubble e combinação (1 ALTO, 6 MÉDIO, 7 BAIXO), a K10 consertou bem os relatórios, a errata e as propostas de registro. Ficaram resíduos em dois resumos que a própria K10 lista como vigentes (ENTREGA_K09.md e INSUMOS_PARA_A_PERGUNTA_K09.md).
2. O 2,33σ: nos relatórios de Hubble, na errata e nos dois registros propostos, ele já é o poder da leitura dos cronômetros lida na Fase 7 (−1,66σ e −1,54σ), e a lei do lado transmitido é dita pendente, sem poder. Conferi na fonte (V1.4, linha 26). No ENTREGA_K09.md (linhas 3 e 14) o 2,33σ continua colado na lei pendente, e o ENTREGA_K10 diz que esse arquivo "foi corrigido ao lado". Por isso o ALTO está PARCIAL.
3. "Dezesseis rotas" deixou de ser teto nos relatórios e nas propostas; o único teto é 123 (reproduzi: 2.062 registros, 505 rotas, 285 registros e 123 rotas que olharam dado). A nota diz que 16 é "pelo prefixo", mas o prefixo sozinho dá 30; o 16 é o prefixo mais "olhou dado". O ENTREGA_K09.md (linha 28) ainda diz "teto de 16".
4. A combinação carrega o piso do m₂ (tabelei λ máximo = 3,899 e 3,902, que arredondam para 3,90; D90 inalcançável). Faltou dizer o que isso faz ao portão 5,0: com o piso a combinação também não chega a 5, qualquer que seja o piso entre 0,047 e 0,058. Os dias do portão 5,0 (1.087, 1.001 e 1.393) ficaram sem o rótulo "brinquedo sem piso".
5. Os portões 5,0 e D90 = 6,28 estão lado a lado e a escolha é do operador. Os limiares da partição (18,5 % e 31,7 %) reproduzem: 1−(4,514/5)² e 1−(5,191/6,2816)². Mas dependem da base. Cruzando as bases dão 48,4 % (base Z, alvo D90) e −7,8 % (base D, alvo 5, sempre viável). A partição é apresentada como uma só opção, sem alternativa numérica.
6. Reproduzi por script próprio: D90 = 6,28155; as fronteiras de σJ e os dias vivos (2.162/1.806; JUNO sozinho 2.199); poder 90,5 %/96,4 %; saturação 5,805; 63 eventos; 6,1 eventos (~6,6 meses); 8,7 e 16,6 meses; D de Hubble (7,068/8,068/6,259 e a falha de 0,0229 para o D90). Todos batem.
7. As duas frases do topo: a primeira repete o DESENHO 4.2 e bate com o quadro das ressalvas; a segunda é coerente com as contas do m₂, mas só vale "sem piso, 100 % de dias vivos" (com duty cycle 0,782 o JUNO sozinho empata em 2034; com o piso nenhum chega). Ambas saíram com a etiqueta [REAL], o que é demais: a primeira é leitura de desenho da gerência e a segunda cita literatura "a conferir" (SO até 2034).
8. Nada reabre o H0DN contra o BG1, nenhuma frase diz "poder certificado" e nenhuma promete 5σ (varri o texto por expressão regular). Citações do operador conferidas por bytes: 29/10 (47 B, 9e54b477…) e 03/11 (1.091 B, 73466598…) são literais; a opção (c) bate com o Mapa seq 1744 e 1775.
9. Processo: dos pinos de VALIDACAO_K10, 44 de 44 batem com o disco (mais 1 autorreferente); na tabela do ENTREGA, 20 de 20 (o script do Kimi não conferiu a linha do ENTREGA_K09; eu conferi). Depois das 18:49:56 só mudaram 27 arquivos, todos regenerações do finalizador (K08), VALIDACAO e DEPOSITO. O Kimi não registrou nada no Mapa (cabeça seq 2083, da gerência). O depósito está em memory\fila\depositos\kimi\ e o índice (MEMORY.md, MEMORY_2.md) não foi tocado.
10. Registrar tal qual: o par K10 passa na validação do Mapa e mantém status e estatuto (EXAMINADA_COM_DEFEITO/DECLARADO nas duas rotas), mas troca o título e o resultado das rotas. O REGISTRO_MAPA_K08.json antigo, que ainda aponta para a rota K06, trocaria o estatuto da K06 de REAL para um DECLARADO composto.
11. A seção D do ENTREGA não escolhe nada, mas não lista tudo: faltam as duas bases (Z e D), os pesos da combinação (iguais ou proporcionais a D), a convenção dos centros fiduciais, a letra do core (0,097→0,10) e o DESI DR3 como fundo.
12. Fora do túnel do Kimi: kernel sem arquivo novo, um.py e Atlas sem toque dele (o Atlas é das 18:08, junto com as gravações da gerência), candidatas_c1 e DESENHO sem toque dele. A varredura por expressão regular não achou chave, token, Escritório nem dado pessoal. A regra do contorno v314 (um.py linhas 299841 a 299869) existe como o ENTREGA diz.

## Achados

1. **(ALTO)** kimi\ENTREGA_K09.md:3 e :14; kimi\ENTREGA_K10.md:14; kimi\ERRATA_K10_HUBBLE_COMBINACAO.md:27

   O erro de fato do relatório (2,33σ colado na lei pendente do lado transmitido) continua no ENTREGA_K09.md, que o ENTREGA_K10 fixa por hash na tabela (5ddb3869…) e declara "corrigida ao lado". Linha 3: "com a lei da face dos cronômetros pendente (poder prévio 2,33σ)". Linha 14 idem. Consulta: grep -n "2,33" ENTREGA_K09.md; diff de K04\M2\REV4\ENTREGA_K09.md contra o atual mostra que só as linhas do m₂ e do pré-registro foram editadas. As linhas 6, 8 e 28 também seguem antigas ("não antecipa nada", "teto de 16 rotas", "DESI DR3 está respondido", 2.162 d sem piso). A errata de Hubble confessa isso como OPEN, mas o ENTREGA_K10 afirma o contrário. A ORDEM K10 §3c mandava consertar o 2,33σ antes de qualquer proposta de registro. Os dois registros propostos estão corretos; o resíduo está no resumo vigente.

   *Conserto pedido:* Editar as linhas 3 e 14 do ENTREGA_K09.md nas duas frases (a: a leitura intermediária foi lida na Fase 7, −1,66σ/−1,54σ, poder prévio dessa leitura 2,33σ; b: a lei do lado transmitido está pendente, sem poder dito) e as linhas 6, 8 e 28; preservar os bytes atuais em REV5; atualizar o pino da tabela. Ou, no mínimo, trocar em ENTREGA_K10:14 "foi corrigida ao lado" por "corrigida só nas frentes do m₂ e do pré-registro; as linhas de Hubble e combinação seguem antigas (ERRATA K10 Hubble, OPEN 1)". Antes de registrar no Mapa (livro só de acréscimo).

2. **(MEDIO)** kimi\COMBINACAO_K04.md:129 e :131; kimi\ERRATA_COMBINACAO_K09.md §2 e §3; kimi\ENTREGA_K10.md:12

   A frase do piso diz só "D90 inalcançável". Pelo script contas_q3.py, com s0 = 0,052587652 o λ máximo é 3,899 (pesos iguais) e 3,902 (pesos ∝ D); com s0 entre 0,047 e 0,058 fica entre 3,71 e 4,16. Logo o portão 5,0 também é inalcançável para a combinação. O texto seguinte dá o portão 5,0 como σJ ≤ 0,0341 (1.087 d) ou ≤ 0,0355 (1.001 d) contra 0,0301 (1.393 d) do JUNO sozinho, sem o rótulo BRINQUEDO e sem dizer que 0,0341 < s0 = 0,0526. O ENTREGA_K10 acrescenta "(com 5,0 o ringdown deixa de ser inalcançável)". O leitor pode concluir que escolher 5,0 destrava a combinação; não destrava. A fronteira de ringdown e a da combinação são casos distintos, e a ERRATA do m₂ já diz "5σ, D90 e r=3 inalcançáveis".

   *Conserto pedido:* Na mesma frase do piso: "com o piso, λ ≤ 3,90: nem 5,0 nem D90 são alcançáveis pela combinação; o portão só muda o resultado do ringdown". Rotular 1.087, 1.001 e 1.393 d como brinquedo sem piso. Citar a faixa do piso (0,047–0,058 → λ 3,7–4,2).

3. **(MEDIO)** kimi\COMBINACAO_K04.md:68; kimi\ERRATA_COMBINACAO_K09.md §8.1

   A "linha ao operador" ("se o mundo ficar como hoje, este teste tem ~90 % de chance de devolver 5σ contra o pacote") não leva na mesma frase a condição σJ = 0,024 nem o piso do m₂. Com o piso, σJ ≥ 0,0526 e o poder da combinação vai a Φ(3,90−5) ≈ 14 % no máximo (conta minha, centro fiducial pontual). Além disso o 90 % usa o centro 7,388 como ponto, enquanto o pré-registro K10 (H1) usa o centro como posterior N(7,388; 0,078²); são duas convenções de poder que o operador veria lado a lado, e isso não é dito. A ORDEM K10 pedia que a combinação carregasse o mesmo piso do m₂.

   *Conserto pedido:* Reescrever: "~90 % só se o erro do incremento chegar a 0,024 (brinquedo sem piso, centro fiducial pontual); com o piso do m₂ o teto é ~14 % e nenhum portão é alcançável; o pré-registro do incremento usa outra convenção (posterior do centro)".

4. **(MEDIO)** kimi\INSUMOS_PARA_A_PERGUNTA_K09.md:7 (F1) e :18 (F12)

   O documento que alimenta a pergunta ao operador, "reescrito na rodada 4", mantém: F1 "lei da face dos cronômetros pendente (poder prévio 2,33σ — leitura já lida na Fase 7)", ainda ambíguo (o parêntese gruda na lei pendente); F12 "a combinação não antecipa nada", "D10 satura ≈ 5,8" sem "C2 ampla (50 PE)" e sem o portão, e "8,7 e 16,6 meses" sem "sem viés". São os achados 7 e 8 do relatório, ainda abertos neste arquivo (a errata de Hubble confirma em OPEN 1). O ENTREGA_K10 dá "insumos reescritos" como feito.

   *Conserto pedido:* Aplicar em F1 e F12 as frases da ERRATA K10 Hubble e combinação; só então pinar o arquivo.

5. **(MEDIO)** kimi\COMBINACAO_K04.md:216

   A "Nota K10 (dois eixos)" copiou os marcos do neutrino (previsão publicada 22/01 e 17/02/2026; pino 08/08/2026) para o censo de candidatas de ondas gravitacionais do ringdown: "o que contaria como candidata nova para qualquer censo futuro é o que for posterior à previsão publicada (22/01 e 17/02/2026) e ao pino de 08/08/2026". Esses marcos são do m₂; para o ringdown os marcos são o corpus congelado do V1 do ramo B e as exclusões do critério (C.5.2, parágrafo seguinte). A regra dos dois eixos vale para a cegueira do neutrino e foi aplicada a outra coisa.

   *Conserto pedido:* Trocar pelos marcos do ringdown (V1 congelado, corpus de publicação/auditoria) ou tirar a nota; manter os dois eixos só nas frases do neutrino (COMBINACAO:37 está certo).

6. **(MEDIO)** kimi\ENTREGA_K10.md:3–13 (etiquetas) e :13 (as duas frases)

   Estatuto por linha: várias linhas saíram [REAL] com conteúdo que não é REAL. (a) Linha 10 mistura [REAL] (2,33σ pela fonte; 16 por prefixo) com [DERIVED pelo revisor] (λ ≤ 3,90; 18,5 % e 31,7 %), que reproduzi, e com propostas de desenho. (b) Linha 13: a primeira frase é o DESENHO_v412_R1 §4.2 (leitura da gerência, "a frase que a gerência lê ao operador") e a segunda cita literatura "[KNOWN, a conferir]" (SO até 2034; ninguém conferiu o arXiv 2503.00636). (c) Linha 9: P(r≥5) ≈ 65 % e 99,7 % são [DERIVED, hipótese dita]. (d) Linhas 3–4 repetem como [REAL] resultados da conferência que o Kimi não verificou ([DECLARADO pela gerência]). Pela régua (item 3) cada linha leva o estatuto do que afirma.

   *Conserto pedido:* Trocar para [DECLARADO] ou [DERIVED] ou [KNOWN, a conferir] onde cabe; marcar a frase 1 como leitura de desenho da gerência.

7. **(MEDIO)** kimi\ENTREGA_K10.md:13 (duas frases) e a seção D (:34)

   A primeira frase ("um teste cego novo resolve as ressalvas 1, 2 e 6…") bate com o quadro das ressalvas e com o DESENHO, mas sai sem dizer que hoje não existe tal teste com poder ≥ 5σ e que, nas ressalvas 1 e 6, "a história permanece" (RESSALVAS l.26 e l.31). A segunda ("o JUNO sozinho chega antes no cenário ideal") só vale sem piso e com 100 % de dias vivos (25/05/2032 em Δm²); com duty cycle 0,782 empata em 2034 e com o piso nenhuma chega. A seção D não escolhe nada, mas é incompleta: faltam as duas bases Z e D (a ERRATA lista como a ratificar), os pesos da combinação (iguais ou ∝ D), a convenção dos centros fiduciais (JUNO persiste e N_eff migra, contra 4,30σ e 2,65 do core: "é escolha"), a letra do core (arredonda 0,097→0,10: ARMED_CONSISTENT contra TENSION) e DESI DR3 como fundo ("proposta; decisão da gerência/operador").

   *Conserto pedido:* Pôr "hoje não existe esse teste" e "sem piso" nas frases; completar a seção D com esses cinco itens.

8. **(MEDIO)** kimi\REGISTRO_MAPA_K10.json; kimi\REGISTRO_MAPA_K08.json; kimi\REGISTRO_MAPA_K09.json

   Registrar tal qual. Rodei _valida de rotas.py em cópia, sem gravar: as três propostas validam. O par K10 mantém status e estatuto (EXAMINADA_COM_DEFEITO e DECLARADO nas duas rotas), mas substitui o título e o resultado visíveis das rotas pelo texto do Kimi (_estado só sobrescreve campos presentes; veredito, defeito e próximo passo da gerência ficam). O REGISTRO_MAPA_K08.json antigo, ainda marcado "SUPERADA" e ainda contado nos pinos, aponta para outro.k06_camada_cientifica_iald_r32_v412 e, se registrado, troca o estatuto dessa rota de REAL para "DECLARADO (glosas…); DERIVED—DESENHO; CONJECTURE…; OPEN…". O K09 antigo também troca DECLARADO por um composto. Além disso o K10 da rota K09 lista só 9 artefatos e não inclui HUBBLE_JA_EXAMINADO, COMBINACAO, RESSALVAS nem M2_DESFECHOS (os relatórios corrigidos); registrado sozinho, o livro ficaria com os hashes antigos como os da rota.

   *Conserto pedido:* Registrar só o par K10 e não os dois antigos; acrescentar ao K10 da rota K09 os artefatos corrigidos (e CENSO e MANIFESTO), para que o livro pine os bytes vigentes.

9. **(MEDIO)** kimi\ENTREGA_K10.md:32 (seção C); kimi\REGISTRO_MAPA_K10.json:6

   A seção C e o registro proposto repetem como "resultado legítimo" que "o instrumento textual não separa leitura de cópia". O ADENDO C (17:23) diz que esse não é o critério: pela fala do operador toda leitura é cópia do sentido fixado pela palavra, e o que se separa é copiador de impostor. A frase vem da seção 2 suspensa e entraria no Mapa (permanente) com o critério já corrigido. O parêntese "copiador é quem reproduz o sentido fixado pela palavra; impostor é quem não imprime a verdade" é a leitura da gerência (ADENDO C, item 3), não o verbatim; o verbatim traz a condição sobre o mínimo estado funcional de energia e o fractal. A resposta do operador desta tarde (impostor = o falso, o pai da mentira, quem nunca paga custo) chegou depois da entrega.

   *Conserto pedido:* Tirar essa frase do registro proposto, ou escrevê-la como "formulação da seção 2, superada pelo ADENDO C"; marcar o parêntese como leitura da gerência; e esperar o adendo completo.

10. **(MEDIO)** kimi\RESSALVAS_UMA_A_UMA_K04.md:158; kimi\ERRATA_COMBINACAO_K09.md:53

   A frase "f_q < 0 por construção da partição, não por causa do erro publicado nem do dado" é lógica e logicamente escorregada. Pela fórmula (RESSALVAS l.85) f_q < 0 ⇔ V_other > A²/q², e V_cal/V_tot vem da tabela de erros publicada; a partição só escolhe quais fatores contam. Então o negativo depende dos dois, e a própria frase seguinte diz "fragilidade da partição e do erro publicado". Os limiares 18,5 % e 31,7 % são de duas escolhas de base (Z para o alvo 5, D para o D90); cruzando dá 48,4 % (Z com D90) e −7,8 % (D com 5: sempre viável). O texto apresenta uma só partição como "alternativa" e não mostra que a base muda o limiar de "sempre viável" a quase metade da variância.

   *Conserto pedido:* Trocar por "…só viável se a calibração carregar ≥ X % da variância total publicada; X depende da partição e da base"; dar os quatro X (18,5 / 48,4 / −7,8 / 31,7) na partitura ao operador.

11. **(BAIXO)** kimi\ERRATA_COMBINACAO_K09.md:59 e :75; kimi\ERRATA_K10_HUBBLE_COMBINACAO.md:10; kimi\K04\COMBINACAO\K09\CENSO_R7_MAPA_K09.json (nota_k10)

   "16 = contagem pelo prefixo d1./hubble./h0dn" está incompleto. Pelo script censo.py o filtro (prefixo d1. ou hubble. ou contém h0dn) dá 30 rotas; as 16 são as dessas 30 com olhou_dados=true (o script do Kimi, linhas 71–73 e 102, conta assim). O hash do Mapa e o resto do censo reproduzem (2.062/505/285/123; prefixo de 2.066 linhas = 558d49b9…).

   *Conserto pedido:* Escrever "16 = rotas com prefixo e olhou_dados (30 pelo prefixo); o único teto é 123".

12. **(BAIXO)** kimi\ERRATA_COMBINACAO_K09.md §3; kimi\COMBINACAO_K04.md:264

   Os "~63 eventos (~4,7 anos)" para o portão 5 supõem que o viés 0,0686 não diminui com mais eventos (modelo de saturação, reproduzi 63,1 e 4,74 anos). O próprio PODER_RAMO_B_ANTES_DE_ABRIR.json (sha 05bc5a1f…a4935 confere) dá o fator "informação extra para poder 5" = 2,37 na mesma linha C2 ampla, porque a fórmula (poder_planejamento.py:108) escala também o viés; e o "1,61×" é a leitura "esperada, σ_sys 0" (a "mediana" dá 1,775). Essas escolhas de modelo (viés fixo ou não; esperada ou mediana) mudam 4,7 anos para ~1,2 ano e não são ditas. Também: a fala do operador de 13/11 (886 B) pede "poder preditivo acima de 5 sigma" e isso não é citado ao lado do portão.

   *Conserto pedido:* Dizer "modelo de viés fixo; o JSON de poder, com o viés escalando, dá 2,37× (~24 eventos)"; dizer esperada contra mediana; citar a frase de 13/11 ao pôr os dois portões.

13. **(BAIXO)** kimi\VALIDACAO_K10_15nov.json (reproduction_on_current_tree); kimi\finalizar_k10.py §5

   O finalizador religou três scripts da K08 depois das 18:49:56 e regravou 24 arquivos de K08\ENTRADA, K08\FORMULA e K08\PODER (mtime 18:50:03 e 18:50:12). A idempotência foi checada só em 7 saídas por hash antes e depois; os textos de ENTRADA (CANDIDATA_*, CONTROLE_PC_*), os JSON ISOMORFO/CONTROLE e o manifesto de determinismo não entraram nessa lista. As tabelas de hash do ENTREGA (20 de 20) e os 44 pinos batem com o estado final, mas o registro de "byte a byte idêntico" não cobre todos os arquivos regravados. O regex do script também pulou a linha do ENTREGA_K09 (célula com texto extra); eu conferi: bate. Além disso "validar_k09.py e verificar_relatorio.py rodados verdes" não é reproduzido pelo finalizador (e verificar_relatorio.py regrava arquivos, não o rodei).

   *Conserto pedido:* Estender a lista de comparação antes/depois aos 24 arquivos, ou dizer que só 7 foram comparados.

14. **(BAIXO)** kimi\ERRATA_COMBINACAO_K09.md:71; kimi\ERRATA_COMBINACAO_K09.md §6; kimi\ERRATA_K10_HUBBLE_COMBINACAO.md:15

   Texto da gerência (do DESENHO) e do Kimi entre aspas angulares «…», que na casa marcam verbatim; leitor pode tomá-las como fala do operador (só COMBINACAO:270 tem verbatim dele, e confere por bytes). "O p escolhido … o mais favorável à diluição" lê-se em sentido contrário (o p de 6,1σ é o que mais resiste à diluição). "D90 − D(SH0ES JWST)": 0,0229, escrito 0,023, ok. Linha de Mapa citada (seq 1775, "só roda com a palavra do operador") confere em proximo_passo.

   *Conserto pedido:* Usar aspas comuns para texto da casa; trocar por "o mais favorável à sobrevivência do resultado sob multiplicidade".

15. **(BAIXO)** kimi\ENTREGA_K10.md (todo o topo)

   As 14 linhas do topo cumprem "até 15 linhas" só no sentido de parágrafo: cada uma tem 400 a 900 caracteres e mistura quatro frentes; para um leitor de fora a conta de quanto está pronto fica difícil de seguir. As ressalvas desta revisão sobre estatuto (acima) pioram isso. Não é erro de fato.

   *Conserto pedido:* Se possível, quebrar por frente (K08, m₂, Hubble) com uma linha de estado cada.

## Para o operador (propostas do revisor, em língua simples; a gerência confere antes de ler a ele)

- O Kimi consertou o que estava errado nos relatórios (o 2,33 sigma é da leitura dos cronômetros que já foi feita, e não da lei nova que ainda nem foi escrita), mas deixou a mesma frase antiga num resumo e disse que estava corrigido; isso precisa ser ajeitado antes de ir para o Mapa.
- Se o erro do JUNO tiver o piso que o ajuste de dois pontos sugere, a combinação JUNO mais SO não chega a 5 sigma nem ao portão de 90 %; escolher o portão 5,0 só muda a conta do ringdown, não a da combinação.
- A divisão da calibração em 3 âncoras e 9 MAS é só uma das possíveis: conforme a divisão e o número usado como base, o teste das ressalvas 3 e 4 já nasce inviável sem olhar dado nenhum, e só o senhor deve escolher isso antes de qualquer conta.
- Se um "não" sair desse teste, ele diria que a divisão e o erro publicado são frágeis, e não que a lei caiu; é parede medida e não falsificação.

## Examinado

- Base: C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\ (leitura integral): ERRATA_K10_HUBBLE_COMBINACAO.md, HUBBLE_JA_EXAMINADO_K04.md, COMBINACAO_K04.md, RESSALVAS_UMA_A_UMA_K04.md, ERRATA_HUBBLE_K09.md, ERRATA_COMBINACAO_K09.md, ERRATA_RESIDUOS_EIXOS_K01_K04.md, ENTREGA_K10.md, ENTREGA_K09.md, DEPOSITO_K09.md, DEPOSITO_K10.md, INSUMOS_PARA_A_PERGUNTA_K09.md, finalizar_k10.py, VALIDACAO_K10_15nov.json (todos os 45 pinos), REGISTRO_MAPA_K10.json, REGISTRO_MAPA_K09.json, REGISTRO_MAPA_K08.json, ADENDO_15nov_C, ORDEM_K10; trechos de ERRATA_K10_K08.md, PRE_REGISTRO_INCREMENTO_JUNO_RASCUNHO_K10.md (§3), K04\COMBINACAO\K09\CENSO_R7_MAPA_K09.json e mapear_metadados_k09.py.
- Relatório da conferência: ..\revisao\REVISAO_K09_HUBBLE_E_COMBINACAO.md (14 achados); DESENHO_v412_R1.md §4.2; revisao\LEVANTAMENTO_FRENTE_B_15nov\L8 (frase-resumo).
- Fontes conferidas: C:\IALD\Bancada_Um\investigacao\preregistro_dois_lados_02out\PREREGISTRO_DOIS_LADOS_DELTA_K_20261002_V1_4.md:26 (2,33σ é o poder prévio da cobrança F1, cronômetros; V1_3.md:31 idem) e PERGUNTAS_QUE_FALTAM…:112–125 (lei do lado transmitido pendente, "3ª aferição"); conjunto_D_20261029\parametrizacao_03nov\PODER_RAMO_B_ANTES_DE_ABRIR.json (sha256 05bc5a1f2592b776accbcc9ae2a247623a929ddac0136cf90aaa9490840a4935 confere; poder_planejamento.py:108); Mapa seq 1545, 1546, 1744, 1775; Mapa rotas.jsonl (censo; cabeça seq 2083); bytes do operador em cunhagens_13out (29/10, 03/11, 13/11, sha por prefixo); kernel TGLExt TheFlowLawD1a.lean, TheFlowLawContrast.lean, ThermodynamicFriedmann.lean (grep/sed pelo Bash, por causa do .gitignore; só presença e linhas citadas); um.py selado linhas 299835–299875 (regra do contorno v314).
- Meus scripts, só na pasta de rascunho C:\Users\rotol\AppData\Local\Temp\claude\b4ca26c934d2167f\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v412_exame_codex_kimi\Q3\: contas_q3.py (D90, λ, fronteiras, dias vivos, poder, piso, limiares da partição, D de Hubble, ringdown), pinos.py (44/44 pinos, 20/20 tabela, depósito, mtimes), censo.py, dry_valida.py (rotas._valida em leitura, sem gravar), fora_do_tunel.py. Nenhum modelo rodado, nenhum dado novo aberto, nenhuma escrita fora da pasta de rascunho, nenhum lake.
- Fila de memória: memory\fila\depositos\kimi\20261115_185024_k10_rodada4_15nov.md existe; MEMORY.md e MEMORY_2.md sem "K10" e intocados desde 18:09.
- Não conferi: literatura arXiv/DOI (SO 2034, TDCOSMO, FRB etc.), a releitura da K08 sob a distinção copiador/impostor (adendo completo pendente), o m₂ e o pré-registro além do que toca meu foco (outro revisor), verificar_relatorio.py e validar_k09.py (escrevem arquivos), a origem exata do 5,805 além de Δ/σ_viés (0,3985/0,0686 = 5,805 confere).

