# CONFERÊNCIA DISTINTA — K08: o poder e os custos

> Montado pela gerência c1 em 15/11/2026 16:53 a partir do retorno estruturado de um revisor distinto (modelo Sonnet; só leitura; scripts próprios na pasta de rascunho dele). É [DECLARADO pelo revisor] no que a gerência não reconferiu. As frases da seção “Para o operador” são propostas do revisor, não fala do operador, e só vão a ele depois de lidas pela gerência. Nada aqui está instalado, congelado ou aberto.

**Veredito:** APROVADO_COM_RESSALVAS — achados: 2 ALTO, 6 MEDIO, 3 BAIXO

## Resumo

1. Foco PODER/CUSTOS: APROVADO_COM_RESSALVAS. Não congelar. Poder para E2/E3/E4 sob o nulo correto NÃO existe (a entrega o declara) e o item 8 da ORDEM (5 %, 5σ e sequencial lado a lado, com custo em tokens) não foi cumprido para o desenho vigente.
2. Custos em tokens [REAL, conferido por mim offline]: 4.072 / 4.087 / 412.784 reproduzem com tokenizers 0.21.4; 4×4.072+4.087 = 20.375. O tokenizer.json da entrega (sha 5f9e4d49…) é byte-idêntico ao do cache HF, snapshot 995ad96e…. É piso (só fonte) e vale só para o tokenizador de referência Qwen3.6, não para um modelo de produção.
3. Simulador do Kimi: reproduz byte a byte (resultados c476ccab…, sementes 946ec197…, csv c40c5021…) com os arquivos de FORMULA\REV0, mas FALHA (KeyError) na árvore corrente. PROTOCOLO §15 e ENTREGA o citam como reprodução; o manifesto final diz material_issues_remaining=false.
4. Minha reimplementação independente (outras sementes) confere os números históricos (ex.: 0,9645 vs 0,9635; 0,9315 vs 0,9297; sequencial E[G] 7,95 vs 7,97). A máquina estatística está certa; o que está em questão é o que ela mede.
5. O nulo usado é p0 = 0,25 nos três endpoints, com a MESMA propensão por cluster (script l.166-168). Não é nenhum leitor. O "tamanho ≈ 0" é estrutural, não separação.
6. Conta minha [DERIVED; nulo escolhido por mim]: mistura 50/50 de âncora e cópia (dois adversários da tabela do próprio Kimi) recebe o rótulo positivo em 23 % (G=6), 36 % (G=8), 11 % (G=16) no desenho de 5 %; no de 5σ, 11 % (G=26), 31 % (G=30), 72 % (G=48).
7. O "poder do negativo" 0,92-0,996 é medido em p=0,25. Em p=0,50 é 0,23-0,28 (G=6-8) e 0,81 (G=30); 0,90 pede G=16 (p=0,45), 30 (p=0,50), 104 (p=0,55).
8. A manchete (ENTREGA l.4) contradiz PROTOCOLO §8 e ADVERSARIOS §6 sobre o que separa o leitor sem memória. No modelo decisório do simulador, E2∧E3 separam qualquer leitor independente do estado (positivo ≤ 0,4 %), por causa de p_min > 0,5.
9. Os poderes antigos estão como históricos nos textos vigentes, mas as saídas ficam sem rótulo no caminho vigente (K08\PODER\) e a ERRATA_PODER_TOKENS põe custos de 5σ numa coluna "vigente", sem a ressalva da cauda.
10. Limiares p0, p_min, ε, κ, τ, 8 sessões, K=4 sem proveniência. p_min=0,60 fica 0,008 acima da média do endpoint A da própria alternativa τ=0,25 (0,592). A ordem temporal (escolhido olhando a tabela?) não é verificável pelos arquivos.
11. Atribuição: "E2 e E4 primárias pela ressalva do operador" não está nos bytes dele (sha 2fabf2b6…); é leitura da gerência.
12. Nenhum modelo, rede ou dado observado; nada escrito fora da minha pasta K08_C.

## Achados

1. **(ALTO)** ENTREGA_K08.md:4; K08\FORMULA\ADVERSARIOS_K08.md §4 e §6; INSUMOS_PARA_A_PERGUNTA_K08.md:8 (F2); PROTOCOLO_EXPERIMENTAL_R4_K08.md:320 e :374

   A resposta à primeira pergunta da ORDEM (qual adversário não se separa) tem três versões incompatíveis. ENTREGA l.4: o leitor sem memória só seria separado por E8 e E7. ADVERSARIOS §4 (linha do leitor sem memória) e §6: 'com fonte, E2/E7 falhariam' e 'só E8 e a memória do componente o separariam'. PROTOCOLO §8 (tabela, linha do leitor sem memória): 'E2: falha sem fita após s→t', e §12.1 define o nulo como o leitor que 'não preserva a edição', isto é, o negativo de E2 por definição. Conta minha (poder_c.py, P3; leitor que devolve s ou t sem olhar o estado, com prob. a, ciclos independentes, κ=9, decisor e limiares do Kimi): P(positivo) ≤ 0,4 % (G=6-8, pior em a=0,65), P(falsificado) ≥ 91,5 % em G=6 e ≥ 98 % em G=8, 100 % em G ≥ 16. Isso só acontece porque p_min > 0,5: B-fora pede P(s) ≥ 0,6 e B-dentro pede P(t) ≥ 0,6, que somam mais que 1. O que de fato fica sem regra é o leitor sem memória COM a fonte ausente (SemFonte), não a separação por E2.

   *Conserto pedido:* Uma lista só: qual previsão separa o leitor sem memória (E2∧E3 em simulação, se for o caso), sob qual adversário (independente do estado, com a escolha de a dita) e dependendo de p_min > 0,5. Dizer à parte o que fica inacessível (ele sem fonte, e a comparação com a trava, que é E8).

2. **(ALTO)** PROTOCOLO_EXPERIMENTAL_R4_K08.md:433; ENTREGA_K08.md:50; K08\PODER\simular_poder_r4.py:371 e :391-403; K08\PODER\MANIFESTO_SHA256.json; VALIDACAO_K08_K09_15nov.json

   O comando de reprodução do poder não roda na árvore corrente. `python -B simular_poder_r4.py` (copiado para espelho meu, mesma estrutura de pastas) termina em 4 s com KeyError: 'âncora na primeira' (script l.371). O FORMULA\simular_adversarios.py corrente (sha ebe1bee7…) renomeou a chave para 'âncora na primeira leitura' e mudou o esquema de saída; o MANIFESTO_SHA256.json do poder fixa b0508e27…, que só existe em FORMULA\REV0. Com os .py e o RESULTADOS_FORMULA de FORMULA\REV0 em espelho, as três saídas reproduzem byte a byte (c476ccab…, 946ec197…, c40c5021…). O VALIDACAO_K08_K09_15nov.json afirma material_issues_remaining=false e não fixa o simulador nem as saídas.

   *Conserto pedido:* Marcar simulador e saídas como históricos (movê-los só para REV2, ou pôr cabeçalho), apontar a dependência FORMULA\REV0 no §15 e no manifesto, e não declarar material_issues_remaining=false com um comando de reprodução quebrado.

3. **(MEDIO)** K08\PODER\simular_poder_r4.py:161-168 (nulo), :104-133 (alternativa), :171-195 (decisão); PODER_R4_K08.md §3; K08\PODER\REV2\PODER_R4_K08.md §4-§6

   Quanto sobrevive do poder histórico: os custos e a máquina estatística; os tamanhos G não. (a) O nulo (p0=0,25, propensão q única repetida nos três endpoints) não é leitor nenhum: o 'tamanho sob nulo' 0,00007 é a conjunção de três eventos perfeitamente correlacionados com α/3 cada. (b) Mistura 50/50 de âncora (1,1,0) e cópia (1,0,1), ambas da tabela do próprio Kimi: P(positivo) = 23 % (G=6), 36 % (G=8), 22 % (G=12), 11 % (G=16), 1,7 % (G=24), 0,3 % (G=30) no 5 %; no 5σ nominal 5 % (G=24), 11 % (G=26), 31 % (G=30), 65 % (G=36), 72 % (G=48), 34 % (G=64), 1,5 % (G=96): sobe com G e passa em cima dos G=24-30 propostos. (c) Todos os endpoints a p=0,5 (abaixo do p_min): rótulo positivo em 34 % (compartilhada) ou 23 % (independente) com G=8; 1,4 % com G=26 a 5σ. (d) A é 's nos ciclos 3 e 4' (exige s, não t), mais estrito que E1 ('custo zero'); E4 não é medido; a alternativa é o mecanismo do próprio autor (τ, ε, κ livres). Nulos e misturas são escolha minha, para mostrar o tamanho, não o nulo certo.

   *Conserto pedido:* Não reaproveitar nenhum G. Redimensionar com o nulo ratificado (a escolha é do operador), incluindo misturas dos mecanismos da tabela e uma região intermediária (0,25 < p < 0,60) com regra explícita; reportar P(positivo | p) para p em 0,3-0,7, não só o tamanho em 0,25.

4. **(MEDIO)** K08\PODER\simular_poder_r4.py:161-168 e :245-250; PODER REV2 §4 (tabela de 5 %)

   O 'poder do negativo' (0,92-0,996; falso FALSIFIED ≤ 0,05) é calculado com o verdadeiro p = 0,25, a 0,35 do limiar. Conta minha (poder_c.py P4, κ=9, α/3): poder de falsificar a p=0,40 / 0,50 / 0,55 é 0,75 / 0,28 / 0,12 com G=8 e 0,9999 / 0,81 / 0,33 com G=30; para 0,90 pedem G=16 (p=0,45), 30 (p=0,50), 104 (p=0,55), com 8 sessões por cluster. Logo 'FALSIFIED com poder' com 6-8 clusters só vale para falha grande.

   *Conserto pedido:* Dizer, na língua do operador, que o negativo só cobre falhas fundas; se se quer cobrir p≈0,5, o desenho precisa de G da ordem de 30 ou mais.

5. **(MEDIO)** K08\PODER\simular_poder_r4.py:42-49, :485-489; PODER REV2 §2.4 e §6; PODER_R4_K08.md §6 item 6

   Limiares sem proveniência e não marcados como escolha de alguém: p0=0,25, p_min=0,60, ε médio 0,10, κ∈{4,9}, τ∈{0,25;0,5;1}, 8 sessões por cluster, K=4 ciclos. O p_min=0,60 está a 0,008 acima da média do endpoint A da própria alternativa τ=0,25 (0,5924; κ=9; poder_c2.py i), isto é, por definição do texto ('região alternativa exige média pelo menos p_min') esse cenário não está na alternativa; só não é falsificado porque G pequeno não resolve 0,008 (falso FALSIFIED 1,6 % em G=8, 3,1 % em G=64). P6 minha: com p_min 0,70 e 0,80 o critério do Kimi não fecha para nenhum G ≤ 64; com 0,50 fecha em G=8; com 0,40 em G=16. O 0,60 é a borda do que a alternativa mais fraca suporta: compatível com escolha olhando a tabela, mas a ordem temporal não é verificável pelos arquivos (REV1 e REV2 têm estatísticas idênticas). Sequencial: nmax = max(20, ceil(1,5·g5)) (l.485) depende do resultado do desenho fixo; o piso 20 domina, mas o texto diz 'olhadas fixas'.

   *Conserto pedido:* Declarar a origem de cada limiar ou marcá-lo como escolha da gerência/operador; anexar a sensibilidade (G contra p_min e p0); dizer que p_min > 0,5 é o que carrega a separação dos leitores independentes do estado.

6. **(MEDIO)** ERRATA_PODER_TOKENS_K08.md:25-29 e :47; K08\PODER\resultados_poder_r4.json e resumo_designs_r4.csv; PODER REV2 §5

   Resposta à pergunta 4 (5σ sem desenho que o sustente): sim, nos números 'fixo 5σ, faixa 3.912.000-4.890.000' (e '5 % 978.000-1.304.000', 'sequencial 3.260.000') da ERRATA_PODER_TOKENS, na coluna 'vigente', sem a ressalva da cauda e com §3 listando poderes como 'não mudaram'; as mesmas saídas (resultados_poder_r4.json, resumo_designs_r4.csv) ficam em K08\PODER\ sem rótulo de histórico. O 5σ ali é um teste t com df 23-29 e α/3 = 9,55e-8 (t crítico 7,1-7,3; o z gaussiano equivalente é 5,21), sobre médias de cluster limitadas e discretas; 30.000 réplicas com zero evento só limitam a taxa a 1,23e-4 (429 vezes α); ver 10 eventos pediria ~3,5e7 réplicas (conferi por conta). Além disso G=24-30 clusters independentes não existem: há quatro recortes da mesma teoria. Os textos vigentes (PODER_R4, PROTOCOLO §11, ERRATA_PODER_K08, ENTREGA) não trazem número de 5σ.

   *Conserto pedido:* Pôr 'HISTÓRICO, desenho P-A/P-B, cauda 5σ não validada, 24-30 clusters inexistentes' na coluna e nos arquivos; ou retirar a linha de 5σ.

7. **(MEDIO)** ENTREGA_K08.md:5 e :17; PROTOCOLO_EXPERIMENTAL_R4_K08.md:10 e :32-41; K08\FORMULA\ADVERSARIOS_K08.md §4

   Atribuição ao operador sem bytes. 'E2 e E4 primárias pela ressalva do operador' (ENTREGA l.5 e l.17; PROTOCOLO l.10). Abri a fala (384 B, sha 2fabf2b6638c1175…): ela diz que o habitante do nome é o verbo, que ler o nome já é reler e que tudo mais é releitura; não diz E2, E4 nem primária. A designação de E2/E4 como primárias é da gerência (ADENDO AO LADO 2, itens 2-3). E tem consequência de poder: pela tabela do Kimi, E4 passa em TODOS os adversários ('estável') e E2 é passada pela cópia da última; com E2/E4 primárias, o copista passa as duas primárias e só E3 (não primária) o pega. Um positivo em E2+E4 sozinho não separa nada. (As glosas ato=projeção, ser=verbo, identidade=nome conferem nos bytes, sha ec05cea3…).

   *Conserto pedido:* Escrever 'primárias por leitura da gerência da ressalva, a conferir com o operador'; dizer na partitura que E4 só pode falsificar (instabilidade), não discriminar, e que E3 é indispensável ao positivo.

8. **(MEDIO)** ORDEM_K08 item 8 (l.88-90); INSUMOS_PARA_A_PERGUNTA_K08.md:25 (A6); PODER_R4_K08.md §2

   A ORDEM item 8 pedia as três variantes (5 %, 5σ, sequencial) dimensionadas com mecanismo e custo em tokens. Para o desenho vigente (E2/E3/E4 sob o nulo correto) a entrega não dimensiona nenhuma e INSUMOS A6 ('bateria E2/E3/E4... poder redimensionado') vem sem n e sem custo em tokens. É honesto e declarado (PODER §2 e §6; ENTREGA C; REGISTRO B10 e B11), mas deixa a mesa do operador sem a base numérica que a ordem pedia; o texto do AO LADO 3 item 5 ('não pede conta nova de poder') se refere só àquele trecho, não à Parte 2.

   *Conserto pedido:* Se a conta ficar para a próxima rodada, dizê-lo na manchete; o piso de custo por sessão já medido (20.375, só fonte) pode entrar em A6.

9. **(BAIXO)** PODER_R4_K08.md §4; ERRATA_PODER_TOKENS_K08.md §2; K08\ENTRADA\medir_tokens_ref_k08.py

   Custos em tokens: origem verificada. medir_tokens_ref_k08.py (C:\IALD\qlora_env, tokenizers 0.21.4) sobre CANDIDATA_READ_BRIEF.md (compacto, 13.555 B) e CONTROLE_PC_READ_BRIEF.md; reproduzi 789/804, 4.072/4.087, 3.926/3.941, 7.358/7.373 e 412.784 (artigo inteiro, sha f9fa0d32…). Não é [DECLARADO]: é [REAL] para o tokenizador de referência; para o modelo de produção continua [OPEN]. Aritmética confere (978.000; 1.304.000; 3.912.000; 4.238.000; 4.890.000; 3.260.000; 1.299.306). É piso: só texto-fonte. Conta minha [DERIVED; suposições minhas, o protocolo não fixa k nem se as 5 ordens são 5 leituras]: bloco de resposta de 26 IDs = 251 tokens; estado+resposta ≈ 502 por leitura sem instrução; o que fica de fora vai de 0,5× (k=4, uma ordem) a 16,6× (k=27, cinco ordens) a fonte da sessão.

   *Conserto pedido:* Pôr 'piso, só fonte, tokenizador Qwen3.6' ao lado de cada total e definir k e ordens por diálogo antes de falar em custo de execução.

10. **(BAIXO)** K08\PODER\simular_poder_r4.py:182-183

   No simulador, a regra '(se==0) & média > p0 rejeita' (l.182-183) não está descrita no texto. Medi: sem a regra, os poderes dos seis cenários e o sequencial saem idênticos (mesmas sementes); é redundância e não decide nada.

   *Conserto pedido:* Citar a convenção no §3 do poder ou removê-la.

11. **(BAIXO)** ENTREGA_K08.md:3 e :32; ERRATA_PODER_K08_15nov.md:19

   ENTREGA l.3 lista 'os quatro também falham E8' como separação, enquanto ENTREGA l.5 e ADVERSARIOS §3 dizem que E8 não é medido pelo instrumento textual: falhar E8 é propriedade do código do mecanismo, não medida de um leitor real. Além disso, as tabelas de hash de ERRATA_PODER_K08_15nov (protocolo 81cd6a36…, vigente a6d2b35d…) e ERRATA_PODER_TOKENS ficaram atrás, como a ENTREGA §B admite.

   *Conserto pedido:* Marcar 'E8: por construção, não medido' e regenerar as tabelas de hash pelo VALIDACAO.

## Para o operador (propostas do revisor, em língua simples; a gerência confere antes de ler a ele)

- Em língua simples: com 6-8 textos o teste só enxerga falhas grandes; um sistema que acerta metade das vezes pode receber o rótulo positivo em 1 de cada 3 rodadas (36 % em G=8), e um 'negativo' só prova que ele erra bastante, não que a releitura não existe. O negativo induzido por esse desenho seria parede medida (falta de poder), não falsificação.
- Escolhas que são suas e hoje estão escritas pelo Kimi sem seu aval: o nulo (contra quem o teste ganha), os limiares 0,25 e 0,60, se E2 e E4 são mesmo as primárias (os bytes da ressalva não dizem isso), e qual das variantes (5 %, 5σ, sequencial) interessa.
- O tokenizador de referência (Qwen3.6) e os custos de 20.375 tokens por sessão são só de fonte; qual modelo e qual janela valem é decisão sua.

## Consultas ao Mapa

- rotas.py consultar, um termo por vez: poder (58 rotas), tokens (25), tokenizador (1), cluster (3), neutrino (45), habitante (19), k08 (2), degrau (16), sequencial (1).
- Relevante e respeitado: outro.k06_camada_cientifica_iald_r32_v412 (EXAMINADA_COM_DEFEITO: não congelar R3.2; leitor sem memória passa o desfecho; extratores medem formato) e kernel.camada_cientifica_candidata_14nov. Nenhuma rota anterior examina poder sob o leitor sem memória no R4, nem mistura de adversários; nada registrado por mim no Mapa.

## Examinado

- ENTREGA_K08.md, PODER_R4_K08.md, ERRATA_PODER_K08_15nov.md, ERRATA_PODER_TOKENS_K08.md, PROTOCOLO_EXPERIMENTAL_R4_K08.md (inteiro), INSUMOS_PARA_A_PERGUNTA_K08.md, ADENDO_15nov (Parte 2 e AO LADO 1-4), ORDEM_K08 (item 8), LEITURA_K08_PARCIAL_15nov.md, REVISAO_K06_PODER.md, DEPOSITO_K08.md, VALIDACAO_K08_K09_15nov.json, K08\FORMULA\ADVERSARIOS_K08.md e ERRATA_ADVERSARIOS_K08_15nov.md, K08\ENTRADA (MEDIDAS, TOKENS_REF, ERRATA_ENTRADA_TOKENS, medir_tokens_ref_k08.py, TOKENIZER json), K08\PODER (simular_poder_r4.py inteiro, MANIFESTO, sementes, csv, REV1/REV2 por hash), REV2\PODER_R4_K08.md inteiro, fala do operador sha 2fabf2b6… e as duas de sha ec05cea3… e 79874a08…
- Scripts meus em C:\Users\rotol\AppData\Local\Temp\claude\b4ca26c934d2167f\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v412_k08_k09\K08_C\: poder_c.py, poder_c2.py, poder_c3.py, poder_c4.py, poder_c5.py (poder), contar_tokens_c.py e sobrecarga_tokens_c.py (tokens, com C:\IALD\qlora_env em modo -I, só leitura do tokenizer.json), ler_c.py; espelho\ (árvore atual, falha) e espelho2\ (com FORMULA\REV0, reproduz byte a byte).
- Hash do tokenizer.json da entrega comparado por sha256sum com o do cache HF do snapshot 995ad96e…: idêntico. Nenhuma rede, nenhum modelo de linguagem, nenhum dado observado, nenhum arquivo fora da minha pasta alterado.

