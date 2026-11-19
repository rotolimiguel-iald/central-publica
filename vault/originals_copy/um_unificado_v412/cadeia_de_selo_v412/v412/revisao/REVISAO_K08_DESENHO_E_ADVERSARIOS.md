# CONFERÊNCIA DISTINTA — K08: o desenho experimental e os adversários

> Montado pela gerência c1 em 15/11/2026 16:53 a partir do retorno estruturado de um revisor distinto (modelo Sonnet; só leitura; scripts próprios na pasta de rascunho dele). É [DECLARADO pelo revisor] no que a gerência não reconferiu. As frases da seção “Para o operador” são propostas do revisor, não fala do operador, e só vão a ele depois de lidas pela gerência. Nada aqui está instalado, congelado ou aberto.

**Veredito:** REPROVADO — achados: 5 ALTO, 9 MEDIO, 2 BAIXO

## Resumo

REPROVADO como desenho experimental e como manchete de separação ("o R4 separa parcialmente cada adversário"); o rascunho segue honesto ao manter a produção bloqueada e ao dizer que E5-E8 não são medidas.
1. Reproduzi por cópia: RESULTADOS_FORMULA.json (568454b7), FORMULA_DO_TEXTO (b2028ce0) e RESULTADOS_ADVERSARIOS.json (4d9f3684) saem idênticos. ADVERSARIOS_K08.md NÃO: o script regera 04aca46a, a entrega diz 932ac331 (editado à mão depois do script).
2. A fórmula confere (26 asserções, 27 cláusulas, 2 leituras, Hamming 1), mas todas as cláusulas são unitárias: o Nome sobre os 26 átomos do TEXTO é UM ponto. A segunda leitura nasce de `leitura_pt`, variável que não está em cláusula nem em item do bloco.
3. O extrator recusa uma linha `LEITURA_PT=...` (ID_DESCONHECIDO, rodei). Logo o empurrão "dentro do Nome" (E2, primária) não cabe no bloco nem se lê dele. Observando só o bloco, âncora, moda e ignora-empurrão (que "E2 separa") passam E1-E4 (script). A separação por E2 é artefato de observar um bit que o modelo não emite.
4. Defeito da K06 volta: um copiador puro passa E1, E2 e E4 (as duas primárias); copiador + 1 bit remendado (a coordenada empurrada) passa também E3 e P-D, isto é, o rótulo positivo do §12.5. E3 e P-D são a MESMA chamada no código.
5. A fonte sai depois do passo 1 (§5 passo 3), mas sem mecanismo nem detecção de vazamento. Com ela fora, E3 só se passa por prior ou chave nos pesos: lema por script (n=1..5), nenhuma função cega à chave passa E2 e E3. O próprio §10 admite que a coordenada não se recupera sem fita.
6. Consequência (regra do posto): falhar E3 é previsto pelo desenho (parede medida), mas o §12.2 deixa E3 contar para FALSIFIED. Negativo induzido, e a partitura em língua simples não está escrita.
7. O adversário "inacessível sem fonte" é inacessível por decreto (levanta SemFonte). Como constante com a chave na memória ele é acessível: passa E1-E4 e P-D com o bloco entregue; com o vetor inteiro cai em E2 só porque a constante escolhida foi s (se fosse t, cai em E3). Empurrão único, num só sentido.
8. Contaminação: não mensurável como desenhado (isomorfo só em brinquedos de 130-377 B; textos reais sem curadoria; sem sonda de memória nem regra de decisão). Há um ancoradouro mensurável não usado: datas de commit dos itens (6,11σ só desde 13/11/2026).
9. "Primárias pela ressalva do operador": os 384 B do operador (sha16 2fabf2b6638c1175) não falam de E1-E8 nem de primária; é leitura da gerência.
10. Não conferi: Lean, PODER (só li), saídas de modelo (não há), ISOMORFO além do relatório.

## Achados

1. **(ALTO)** PROTOCOLO_EXPERIMENTAL_R4_K08.md l.73-80, 215, 236, 262-264; K08\EXTRACAO\extrator_fechado.py l.16, 107-109; K08\FORMULA\simular_adversarios.py l.129-132; ENTREGA_K08.md l.3, 19

   E2 (primária) gira em torno de `leitura_pt`, variável que não está em nenhuma cláusula nem é item do bloco (o protocolo diz: 'metadado de estado'). O extrator a recusa: `LEITURA_PT=SIM` dentro do bloco dá ID_DESCONHECIDO e FORMATO_INVALIDO (rodei). Em todas as quatro candidatas as cláusulas são unitárias (as derivações já são satisfeitas pelas unitárias), então o Nome sobre os átomos do TEXTO tem uma só leitura; 'duas leituras, Hamming mínimo 1' vem do bit fantasma. cost(s)=cost(t)=0, então o observável declarado (custo) não vê o empurrão de E2. Observando só o bloco entregue, âncora, moda e ignora-empurrão passam E1-E4: as três separações 'por E2' somem (meu_ataque_k08.py, modelo A). Se o bit viajar fora do bloco, quem o preserva é o harness, não o modelo; se viajar dentro, é teste de cópia.

   *Conserto pedido:* Ou (a) declarar E2 equivalente a E4 e não observável, tirando-a de primária e das separações; ou (b) construir leituras múltiplas a partir de ambiguidades reais do texto (itens que o texto deixa abertos), com o par de leituras visível no bloco, e empurrar nos dois sentidos (s->t e t->s). Corrigir a frase de ENTREGA l.3 e PROTOCOLO §8.

2. **(ALTO)** PROTOCOLO l.203-210 (§5), 266-268 (E3), 336-342 (§10, l.340), 378-386 (§12.2), 404-410 (§12.5); ADVERSARIOS_K08.md l.42, 66

   E3 é a única previsão que separa leitor de copiador, e com a fonte retirada ela é inatingível para qualquer leitor cego à chave. Lema (script, n=1..5, D_lema_funcao_cega_a_chave): se f fixa todo estado válido (E2/E4) e desfaz o empurrão (E3) para toda chave, há estado com exigências contraditórias; logo nenhuma f independente da chave passa E2 e E3. Aqui a chave é o gabarito do texto; sem a fonte, só prior ou chave nos pesos (contaminação) a fornece. O §10 admite o fato ('não pode ser recuperada'). O mesmo vale para a referência: o análogo de P_N (projetar na chave) passa tudo só enquanto tem a chave a cada passo, que é o que o R4 retira. Para o modelo isso vira: passar E3 = prior em item previsível (a coordenada empurrada é sempre `artigo_pt_en`, a mais adivinhável) ou memorização; falhar E3 = parede medida. O §12.2 ainda deixa E3 contar para R4_OPERATIONAL_PREDICTION_FALSIFIED. É o negativo induzido que a regra do posto veda.

   *Conserto pedido:* Classificar a priori, por escrito, o negativo de E3 sem canal de chave como PAREDE_MEDIDA (não FALSIFIED); ou reintroduzir a fita num braço diagnóstico; ou empurrar várias coordenadas de plausibilidade a priori variada, incluindo itens só obteníveis da fonte (h0_6sigma, ritos_0_de_11), e comparar com o isomorfo. Tirar E3 das condições de FALSIFIED enquanto a chave não for canal declarado do desenho.

3. **(ALTO)** K08\FORMULA\simular_adversarios.py l.54-61, 159-183; ADVERSARIOS_K08.md l.42, 66; ENTREGA_K08.md l.4; PROTOCOLO l.320

   O 'leitor sem memória determinado só pela fonte' é declarado inacessível porque a função levanta SemFonte sem fonte: inacessibilidade por decreto, não resultado. Sem fonte no contexto, um modelo com a chave nos pesos ou nos priors é exatamente uma constante. Simulei a constante: com o bloco entregue ela passa E1, E2, E3, E4 e P-D (nada a separa); com o vetor inteiro ela cai em E2 só porque a constante é s (`next(x for x in sols if not x[idx_livre])`); se fosse t (chave_t.py), passa E2 e cai em E3. Qual teste 'separa' depende da escolha oculta de qual leitura válida a constante devolve e do sentido único do empurrão. A tabela dá 'não separado' (acertado), mas a linha 'E2 separa' e a conta 'cotas + retorno não bastam' omitem que o adversário existe e é trivial.

   *Conserto pedido:* Simular a chave constante nas duas variantes (s e t), com empurrões nos dois sentidos, e reportá-la na tabela como acessível; retirar 'inacessível'.

4. **(ALTO)** PROTOCOLO l.256-264 (E2), 270-272 (E4), 404-410 (§12.5), 298-307 (tabela ATO x NOME); simular_adversarios.py l.147-155; ENTREGA l.3, 5

   O defeito central da K06 volta nas duas primárias. Um copiador puro (devolve a última leitura) passa E1 (de início válido), E2 e E4; só falha E3/P-D. Um copiador com remendo de UM bit (força `artigo_pt_en`=SIM, a coordenada empurrada em todos os textos) passa E1, E2, E3, E4 e P-D, nos dois modelos de observação (meu_ataque_k08.py). O rótulo positivo `R4_RELEITURA_DISCRETA_NOT_FALSIFIED...` (§12.5) é, portanto, alcançável por cópia + um prior, e a ENTREGA diz que o instrumento 'mede a ponte leitor-teorema por E2/E4'. Além disso E3 e P-D são a mesma chamada (`empurrar_e_ler(mecanismo, formula, s, y)` nas duas linhas do script): 'E3/P-D separam a cópia' conta uma medida duas vezes. A tabela ATO x NOME classifica 'resposta editada e relida' como ATO primário sem separar ato de reler de ato de copiar.

   *Conserto pedido:* Pôr copiador e copiador-com-remendo na tabela de adversários; só admitir rótulo positivo se ambos falharem; variar a coordenada empurrada entre sessões, incluindo itens só da fonte; contar E3 e P-D como uma medida, ou definir P-D com um modelo (escala zero não é botão de LLM).

5. **(ALTO)** PROTOCOLO_EXPERIMENTAL_R4_K08.md §0, §7, §12, §13 (l.6-14, 256-290, 370-410); ENTREGA_K08.md l.3-5

   Regra do posto não cumprida para o operador: não há, em língua simples, o que o teste decide, o que não decide e o que o negativo significa. O texto é formalismo (E1-E8, P_N, trava); a manchete diz que E2/E4 'medem a ponte' sem avisar que um copiador as passa, que E2 não é observável no bloco, e que o negativo em E3 é previsto pelo desenho (parede). Escolhas de desenho ficam implícitas: sentido e coordenada únicos do empurrão, instrução do passo >=2, item em PT sobre texto em EN, tolerância zero a divergência de ordem e a um SIM em isca.

   *Conserto pedido:* Acrescentar ao topo uma partitura de três linhas. Sugestão (para o operador ratificar ou recusar): 'Como está, este teste decide se o modelo mantém o que respondeu e se acerta, sem o texto, um item previsível; NÃO decide se ele relê como o Nome; um negativo em E3 significaria que, sem o texto, ninguém consegue desfazer o erro (parede medida), não que a ideia falhou.'

6. **(MEDIO)** ENTREGA_K08.md l.5, 17; PROTOCOLO l.10, 30; PODER_R4_K08.md l.11; ERRATA_PODER_K08_15nov.md l.10; ADENDO AO LADO 2 itens 2-3

   'E2 e E4 primárias pela ressalva do operador' atribui a ele uma escolha. Abri os bytes (OPERADOR_15nov_ressalva..., 384 B, sha16 2fabf2b6638c1175): a fala trata de 'habitante do nome', 'nomear', 'ler o nome já é reler'; não fala de E1-E8, de primária, de E2 nem de E4. O adendo diz que a consequência para o experimento é [leitura da gerência]. 'E4 mede diretamente a ressalva' (PROTOCOLO l.272) também é interpretação. As glosas ato=projeção, ser=verbo, identidade=nome conferem nos bytes (sha16 ec05cea3eded9264) e o MODELO as marca [DECLARADO].

   *Conserto pedido:* Trocar por 'primárias pela leitura da gerência da ressalva do operador (AO LADO 2)'; e escrever que a escolha das primárias é do operador/gerência, não da fala.

7. **(MEDIO)** PROTOCOLO l.219, 319, 396 (integridade), 262-264 (E2)

   Regra de veredito incoerente: 'edição sem efeito observável' leva a INCONCLUSIVE_INTEGRIDADE (§5, §12.3), mas uma releitura que desfaz a troca t->s é exatamente 'a edição não teve efeito na saída'. O 'ignora o empurrão' aparece como separado por E2 (ENTREGA l.3) e como caso de integridade (§8 l.319). Sem definir 'efeito observável', toda falha de E2 pode virar INCONCLUSIVE ou nenhuma.

   *Conserto pedido:* Definir 'efeito observável' (ex.: a edição chegou ao input do modelo, verificada por hash do prompt), e separar 'o modelo desfez' de 'a edição não chegou'.

8. **(MEDIO)** K08\EXTRACAO\extrator_fechado.py l.175-181; METODO_EXTRACAO.md l.17; PROTOCOLO l.233-237, 292; ORDEM item A.6

   A passagem bloco -> leitura Booleana -> custo não está definida: (i) 'O TEXTO NÃO DIZ' sobre átomo afirmado conta como violação? (o protocolo diz só que não é negação); (ii) no P-C há dois itens sobre o mesmo átomo (P e 'P é falsa'), ambos SIM; qual valor o átomo recebe? (METODO l.17 remete a 'camada lógica à parte'); (iii) `custo_leitura` conta NÃO como custo e dá 2 para o gabarito perfeito de READ_BRIEF (2 itens negados pelo texto; rodei); a função não é usada em lugar nenhum, mas contradiz Formula.custo; (iv) o que o modelo vê no passo >=2 (a instrução sobre o estado) não está escrito, e sozinha decide cópia versus revisão; (v) língua dos itens (PT) sobre texto EN.

   *Conserto pedido:* Fixar por escrito a função bloco->vetor->custo com os três rótulos, apagar ou corrigir `custo_leitura`, e congelar o prompt do passo >=2 e a língua dos itens antes de qualquer rodada.

9. **(MEDIO)** K08\FORMULA\simular_adversarios.py l.150, 289 (`| falha |`), 156 (`"E8": "falha por construção"`); PROTOCOLO l.315 (linha 'referência P_N passa')

   'Os quatro também falham E8' é string literal gravada no script e na tabela, não resultado simulado; E8 não é medida pelo instrumento. A linha 'referência P_N/selecao: passa, passa, passa, passa' do §8 também não é computada (não há mecanismo P_N na simulação); eu a computei como projeção com a chave, e ela só passa com a chave a cada passo (ver achado 2).

   *Conserto pedido:* Marcar E8 como 'não medido' na tabela (não 'falha'); ou simular E8 de fato; computar a referência ou retirar a linha.

10. **(MEDIO)** K08\FORMULA\ADVERSARIOS_K08.md (932ac331) x simular_adversarios.py l.279, 304; ERRATA_ADVERSARIOS_K08_15nov.md l.44; ENTREGA l.53

   O ADVERSARIOS_K08.md entregue foi editado à mão depois do script. Rodar o script (como o próprio arquivo manda) regera outro texto (04aca46a), com 'E3 e E7 são controles' e P-C sem o 'inominado', desfazendo a reclassificação da ordem. A errata lista 04aca46a como o hash do arquivo; a entrega lista 932ac331. Dois hashes para o mesmo nome; o script não reproduz o entregue.

   *Conserto pedido:* Levar as duas frases corrigidas para dentro de render() em simular_adversarios.py e regenerar; ou dizer no arquivo que ele é editado à mão.

11. **(MEDIO)** CONTAMINACAO_R4_K08.md l.93-129; ERRATA_CONTAMINACAO_K08_15nov.md l.31-38; PROTOCOLO l.325-334; K08\ISOMORFO\texto_*.txt (130-377 B)

   O risco de contaminação não está tratado de modo mensurável: o isomorfo só existe para textos-brinquedo de 130-377 bytes; para os quatro textos reais as duas alternativas ficam sem escolha e sem curadoria; não há sonda de memória sobre os textos reais nem regra de decisão que transforme 'real versus isomorfo' em veredito. Pelo lema do achado 2, o isomorfo não serve de linha de base para E3 (qualquer leitor cego à chave falha), então o contraste real/isomorfo mede conhecimento da chave (prior ou memória), não estrutura. Ancoradouro mensurável não usado: datas de commit do espelho (git log, só leitura): README 17/02/2026, llms.txt 23/08/2026, read-brief 11/09/2026, ABSTRACT 03/11/2026; os itens H0DN/6,11σ entram em 13/11/2026 (commit dc61e0c0); os itens de creditação em 07/10/2026 (978843fc).

   *Conserto pedido:* Pré-registrar a covariável 'data de entrada do item no texto público x corte do modelo'; incluir sonda de continuação literal nos textos reais; escrever a regra de decisão do contraste e dizer que o isomorfo mede a chave, não a releitura.

12. **(MEDIO)** PROTOCOLO l.67; PODER_R4_K08.md l.46-53

   A 'sessão-análise' lista cinco diálogos (E1, E3, E2, P-D, P-C): E4, primária, não tem diálogo nem é dito que reaproveita o de E1/E2; P-D não tem definição com um LLM e duplica E3; o custo de 20.375 tokens conta cinco fitas.

   *Conserto pedido:* Redefinir a sessão com E4 explícita, P-D ou fundido a E3 ou definido (stub sem chamada), e refazer o custo.

13. **(MEDIO)** K08\FORMULA\catalogo_assercoes.py l.31, 136 (LLMS07), 108 (READ_BRIEF15); llms.txt:61

   A coordenada empurrada em todos os textos, `artigo_pt_en` ('o artigo é disponibilizado em PT e EN'), é a de apoio mais fraco: a âncora de LLMS07 é 'o artigo emitido pelo um.py, em TEXTO' (llms.txt:61), que não diz PT nem EN em prosa (só nomes de arquivo em links); READ_BRIEF15 ancora em 'article as text, EN'. Se o texto não o afirma em prosa, 'negar' o item pode não estar 'fora do Nome' e a chave SIM é discutível. É o gabarito do autor, sem gabarito humano independente (o próprio entregue admite).

   *Conserto pedido:* Empurrar um item de apoio literal em prosa, em cada texto, e pedir gabarito humano independente para os 26 itens antes de usar a chave.

14. **(MEDIO)** PROTOCOLO l.243, 254, 394; ENTREGA l.40

   Escolhas de rigor embutidas e não parametrizadas: qualquer divergência de rótulo entre as cinco ordens vira INCONCLUSIVE_ORDEM, e um único SIM numa isca vira INCONCLUSIVE_ISCAS. Com modelos estocásticos e 26 itens, isso tende a devolver INCONCLUSIVE por padrão. Limiares de 'com poder', 'clusters suficientes', modelo, temperatura e repetições não existem (admitido no §13); os dois zeros de tolerância não são admitidos como escolha.

   *Conserto pedido:* Declarar a tolerância como escolha do operador e dar a ele a alternativa (zero vs proporção) com o que cada uma faz ao veredito.

15. **(BAIXO)** ERRATA_PODER_K08_15nov.md l.19; ERRATA_PODER_TOKENS_K08.md; MANIFESTO_FORMULA_K08.json

   As tabelas de hash das erratas ficaram um passo atrás (a errata de poder cita 81cd6a36 para o protocolo; o vigente é a6d2b35d). A entrega já o registra (l.32); VALIDACAO_K08_K09_15nov.json é o manifesto final.

   *Conserto pedido:* Regenerar as tabelas por script antes de custodiar.

16. **(BAIXO)** INSUMOS_PARA_A_PERGUNTA_K08.md F1, A1, A5, A6

   F1 diz que o instrumento 'mede E1-E4 por custo Booleano': E2 não é medida por custo (cost(s)=cost(t)=0). A1 ('nenhum risco de leitura inflada') e A6 ('mede a ponte parcial') avaliam, num arquivo que se diz sem recomendação. A5 ('retirar a variável livre') não diz que isso remove o empurrão de E2 e deixa o Nome como um ponto.

   *Conserto pedido:* Reescrever F1; tirar os juízos de A1 e A6; dizer a consequência de A5.

## Para o operador (propostas do revisor, em língua simples; a gerência confere antes de ler a ele)

- Partitura em uma linha (para ele ler antes de qualquer rodada): como está, este teste decide se o modelo mantém o que respondeu e se acerta, sem o texto, um item previsível; NÃO decide se ele relê como o Nome; um negativo em E3 significaria que, sem o texto, ninguém desfaz o erro (parede medida), não que a ideia falhou. A frase é minha, para ele ratificar ou recusar.
- Escolhas que o desenho tomou sem ele: qual coordenada empurrar (sempre artigo_pt_en), em que sentido (só s para t), o que o modelo vê no passo 2, tolerância zero a divergência de ordem e a um SIM em isca, língua dos itens. Todas viram pergunta de alternativas, não decisão do Kimi.
- 'Primárias pela ressalva do operador' é leitura da gerência; a fala dele (384 B) não diz isso. Se for dele, ele tem de dizer.

## Consultas ao Mapa

- rotas.py consultar contaminacao: 2 rotas (d1.fase9.f3_1_reauditoria_v2r2_c1_08out; ringdown.dephasing), sem relação com este desenho
- rotas.py consultar copiador: 2 rotas; a pertinente é outro.k06_camada_cientifica_iald_r32_v412 (EXAMINADA_COM_DEFEITO; nao_refazer: o leitor constante habita o tipo, resumo não separado de convergência). O achado 3 (constante com a chave) e o 4 (copiador) são a mesma classe, vista agora no R4
- rotas.py consultar leitor: 91 rotas, truncado; lidas só as primeiras (d1.fase3_*), sem relação
- rotas.py consultar adversario: 0 rotas
- Nada foi registrado no Mapa; as rotas do R4 e o achado do lema (nenhuma função cega à chave passa E2 e E3) ficam para a gerência registrar

## Examinado

- ENTREGA_K08.md (todas as linhas); ORDEM_K08; ADENDO de 15/11 com os quatro AO LADO
- PROTOCOLO_EXPERIMENTAL_R4_K08.md inteiro (436 l.)
- K08\FORMULA: ADVERSARIOS_K08.md, ERRATA_ADVERSARIOS, simular_adversarios.py, catalogo_assercoes.py, verificar_formula.py (lidos inteiros e rodados em cópia)
- K08\EXTRACAO: extrator_fechado.py, inducao.py, METODO_EXTRACAO.md (lidos); extrair() rodado com linha LEITURA_PT
- MODELO_FORMAL_R4_K08.md, CONTAMINACAO_R4_K08.md e ERRATA, PODER_R4_K08.md e ERRATA_PODER, INSUMOS_PARA_A_PERGUNTA_K08.md
- REVISAO_K06_EXTRATORES.md (inteira) e LEITURA_K08_PARCIAL_15nov.md (inteira); REVISAO_K06_FORMAL e _PODER não relidas
- Bytes do operador abertos: ressalva (384 B, sha16 2fabf2b6638c1175), 'o nome é o ato do verbo' (24 B), 'amor é o ato de amar' (51 B), fala de 11:47 (760 B, sha16 ec05cea3eded9264)
- Linhas-fonte de the_boundary (read-brief 15/28, llms 5/59-61, README 142, ABSTRACT 23) e git log de leitura sobre datas de entrada dos itens
- Reprodução por hash de RESULTADOS_FORMULA.json, FORMULA_DO_TEXTO_K08.md, RESULTADOS_ADVERSARIOS.json, ISOMORFO_*.json, CONTROLE_PC_*.json e das CANDIDATA_*.md: idênticos; ADVERSARIOS_K08.md difere (achado MEDIO)
- Scripts meus (só na pasta K08_B): C:\Users\rotol\AppData\Local\Temp\claude\b4ca26c934d2167f\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v412_k08_k09\K08_B\meu_ataque_k08.py (+ saida_meu_ataque_k08.json) e chave_t.py
- Respondedor 'grep' (só repete a fonte) que tentei: acertou 2/16, 6/26, 9/19 e 13/28 com meu tokenizador cru; NÃO afirmo que um copiador-da-fonte passa o passo 1 (ataque falho, sem conclusão)
- Não conferi: Lean das pedras, PODER além de ler, ISOMORFO além do relatório, saídas de modelo (não existem), custos em tokens

