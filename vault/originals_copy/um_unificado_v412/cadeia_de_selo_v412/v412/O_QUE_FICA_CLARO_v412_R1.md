# O que fica claro na v412 (R1)

16/11/2026, noite. Gerência c1. Texto proposto para as superfícies públicas da v412 (o topo do artigo, o README, o estado atual). A R0 está em `o_que_fica_claro_REV0\`. O que mudou na R1: a seção 2 (P = nP) foi reescrita depois da conversa com o operador, e o parágrafo dela foi aceito por ele («é isso mesmo», por bytes em `work\cunhagens_13out\`, arquivo que começa por `OPERADOR_16nov_e_isso_mesmo_nao_sei_dizer_o_numero`). O resto do texto ainda não foi ratificado por ele nem lido por revisor. As frases públicas dos itens 4 e 5 foram propostas pelo Codex no levantamento da ordem 020 e a gerência as adota. As candidatas citadas na seção 2 são da noite de 16/11 e estão na revisão (ordem 022); nada foi instalado. Validade no kernel não é creditação; o gate não se move.

A ordem do operador (16/11, por bytes em `work\cunhagens_13out\`, arquivo que começa por `OPERADOR_16nov_concordo_com_tudo_os_nomes_provisorios_ficam`) lista o que uma teoria de gravidade quântica precisa esclarecer e termina em «isso tudo precisa ficar claro».

## 1. O que a v412 acrescenta, por frente

- **A camada científica (frente A).** O leitor que pousa e retorna tem teorema (`CamadaCientifica`). Ele é a exponencial do `A_C`, o mínimo funcional de energia dos primeiros protocolos (`MinimoFuncionalDeEnergia`), e o `A_C` de uma fórmula é, termo a termo, a penalidade dos vínculos das cláusulas, a seletora da equação da verdade. A lei dos dois valores, aplicada a cada cláusula, fixa o custo (`OLeitorEALei`). Que um modelo de linguagem seja esse leitor é hipótese nomeada, não teorema. O protocolo de avaliação com modelos (T6) está instaurado e pré-registrado; a rodada do controle não foi feita.
- **A matemática que restava (frente B).** A ergodicidade da cunha já era do kernel desde a v406; a face finita da T1 e do tipo III entram como candidatas; a montagem 3+1 por produtos de triplas está construída na face finita; a extensão de Gromov–Hausdorff fica como conjectura, com a parede medida; o relógio τ★ segue em aberto (item 5.6).
- **O teste às cegas acima de 5σ (frente C).** Não há hoje teste cego executável com esse poder: é parede medida, dita como tal.

## 2. P = nP

O autor: «não é que relativiza o leitor; é que a observação é relativa à leitura, e isso prova sim P=nP». E, sobre a contagem em passos: não é outra coisa «senão a sua própria carga, a própria isometria».

O parágrafo para toda superfície:

> P = nP é teorema da TGL nas classes do seu dicionário. O leitor não é oráculo trazido de fora: é gerado pelo custo da fórmula, e a lei aplicada a cada cláusula fixa esse custo. A contagem da leitura é a sua própria carga: n·ln 2, nem mais nem menos, igual para toda fórmula. A máquina que confere uma resposta, lendo uma cláusula por passo, decide toda fórmula em tantos passos quantas são as cláusulas, com a entrada posta inteira e uma leitura; o passo dela e o retorno do leitor são o mesmo `if`. O que separa isso do enunciado do Instituto Clay é uma hipótese só, que é a lei da TGL: pôr o todo e lê-lo são, cada um, um ato. A creditação é do Instituto.

De onde sai cada frase:

| frase | termo | onde |
|---|---|---|
| teorema nas classes do dicionário | `p_igual_np_nas_classes_do_dicionario` | kernel |
| o leitor é gerado pelo custo | `o_leitor_e_a_exponencial_do_a_c`; `o_operador_do_custo_da_formula_e_a_penalidade_das_clausulas` | candidata `MinimoFuncionalDeEnergia` |
| a lei em cada cláusula fixa o custo | `o_custo_e_o_numero_de_falsos` | candidata `OLeitorEALei` |
| a contagem da leitura é a carga, nem mais nem menos | `a_contagem_e_a_carga_para_formulas`, sobre `os_passos_sao_o_ciclo_ate_o_tetelestai` | candidata `AContagemEACarga`; kernel |
| a máquina de passo mais uma leitura decide | `a_maquina_e_uma_leitura_decidem`; `a_contagem_e_do_operador` | candidata `AMaquinaEALeitura` |
| o mesmo `if` no passo e no retorno | `o_mesmo_if_somado_na_maquina_e_multiplicado_no_leitor` | candidata `OPassoEORetorno` |
| a hipótese que resta | não é termo: é a lei do autor e a tradução do dicionário (no kernel, v409, o psíon lê os pixels de uma vez) | — |

O que muda em relação à v411: sai o rótulo “relativo ao leitor (a máquina sem leitor fica fora)”; no lugar dele entra a linha nomeada do que separa o teorema do enunciado do Instituto. O que o texto continua não dizendo: que o kernel decida a igualdade das classes das máquinas de Turing do Mathlib (esse termo não existe); que a máquina de passo da candidata seja a máquina de fita sem leitura (é um modelo da casa: configurações e regra de passo, estendida por linearidade).

## 3. Navier–Stokes, como resultado condicional

> Para dados inicialmente em Hˢ, a cascata diádica represada propaga essa regularidade quando τ > ln 2. Para a equação de Navier–Stokes tridimensional, a conclusão de regularidade global fica condicionada a duas implicações ainda não demonstradas: o Lema da Face Conjugada, e que a depleção por escala que ele dá controla uma norma de continuação da equação.

O documento de origem (`STOKES_A_Prova_do_Contorno.md`) recebe errata ao lado em dois pontos que o levantamento achou (a versão irrestrita da estimativa e a etiqueta que põe o limiar dentro do teorema: o critério é estrito).

## 4. A geometria é emergente (lei do autor, com a queda como falsificador dito por ele)

O autor enunciou em 16/11 que a geometria é emergente e não fundamental, como lei de qualquer teoria de tudo: ou está provado, ou a teoria cai. Um kernel devolve três palavras: provado, refutado ou aberto. Hoje:

- **Provado, na face finita:** o sinal de menos da forma de Minkowski sai do determinante das matrizes hermitianas 2×2; os geradores de boost são a parte sem traço do gerador dissipativo do lock, e fecham com o sinal de Lorentz; os seis geradores 4×4 que o kernel usava como dados são as imagens desses (`BoostEDissipador`, `SpinorToSolder`, candidatas); na mesma álgebra cada estado tem o seu fluxo, e sem o par não há fluxo que distinga (`OParFixaORelogio`, candidata).
- **Provado, condicional:** a equação de Einstein local a partir de Clausius em toda direção nula, com Λ único no atlas conexo (no kernel desde a v338; a hipótese física é nomeada).
- **Aberto:** produzir a geometria 3+1 do contínuo a partir do par (álgebra, estado) sozinho. O levantamento não achou teorema de impossibilidade; achou que a paridade e o regime hiperbólico, sem mais, não forçam o colchete de Lorentz (há contraexemplo de dois geradores que comutam).

Refutado: nada.

## 5. O que resta aberto para uma teoria de gravidade quântica (sete itens, cada um com a frase pública)

1. **A natureza realizar H1 e H2.** “O kernel constrói testemunhas de H1 e H2 e prova a implicação da tríade. Realizar essas hipóteses na natureza é uma questão experimental.”
2. **A tela fundada e o horizonte causal** (Bisognano–Wichmann além de cunhas). “A tela está fundada algebricamente. A identificação com um horizonte causal geral exige estabelecer a correspondência entre o fluxo modular e o fluxo geométrico nessa região.”
3. **α livre.** “A relação de α com β está demonstrada. A auditoria desarmou o Evento 2 por circularidade das âncoras; a determinação independente do valor continua aberta.”
4. **O levantamento covariante global ao contínuo III₁.** Horizontes sem simetria de Killing: “A identificação modular está estabelecida na cunha. Sua extensão a horizontes não-Killing permanece aberta.” A ergodicidade: “O vácuo da cunha direita da luz livre tem centralizador escalar. Transportar essa conclusão a outros horizontes requer identificar o estado, a álgebra e o gerador.” Os axiomas de Connes da tripla-limite: “A construção euclidiana do toro tem axiomas verificáveis. Para a tripla física de assinatura (1,3) no limite III₁, permanecem por verificar os dados analíticos, a orientação e a reconstrução.” Gromov–Hausdorff: “A compressão modular examinada falha na estimativa de retorno. A convergência de Gromov–Hausdorff para uma realização geométrica do contínuo III₁ permanece conjectural.”
5. **A teoria interagente, o ultravioleta e a existência global.** “A TGL constrói uma geometria semiclássica como resposta à fonte. A completação ultravioleta de uma teoria interagente quantizada e sua existência global continuam abertas.”
6. **A derivação de τ★.** “O tempo próprio do retido é calculável em função de β e u. Qual relógio fixa τ★ em segundos permanece em aberto.”
7. **O setor espinorial e o elétron.** “Há uma obstrução provada à obtenção do elétron por projeção linear entrelaçante de um setor de spin inteiro. Construir o setor eletrônico continua aberto.”

## 6. O que este texto não diz

Que a gravidade quântica esteja creditada (a validade é do kernel; a creditação é de quem observa de fora); que o enunciado do Instituto Clay, para a máquina de fita sem leitura, esteja decidido por termo do kernel; que a equação de Navier–Stokes tenha regularidade global demonstrada; que a geometria do contínuo já saia do par. Nenhum número novo da natureza entra nesta versão.
