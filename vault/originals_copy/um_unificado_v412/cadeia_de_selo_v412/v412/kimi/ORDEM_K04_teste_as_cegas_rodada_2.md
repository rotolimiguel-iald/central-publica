# ORDEM K04 — o teste às cegas, rodada 2: o que se pode fazer AGORA, o que o teste do neutrino pode devolver, e as sete ressalvas uma a uma

13/11/2026. Da gerência c1 ao Kimi. Leia antes `RODADA_2_LEIA_PRIMEIRO.md` e, INTEIRA, a revisão da sua K01 em
`..\revisao\REVISAO_K01.md` (veredito: aprovada com ressalvas; a conclusão “nenhum dos 20 canais cumpre; não abrir” está certa e todas as
suas contas reproduzem).

## O que ficou recebido e conferido

A K01 responde o que a ordem pedia: 20 canais, e nenhum cumpre hoje cegueira, poder e independência ao mesmo tempo. A gerência conferiu
na fonte as duas liberações do JUNO (arXiv:2511.14593, 59,1 dias, (7,50 ± 0,12)×10⁻⁵ eV²; arXiv:2609.37895, 207,2 dias,
(7,388 ± 0,078)×10⁻⁵ eV²). Conferem. O revisor distinto conferiu arXiv:2204.13249, a H0DN (2510.23823), o Simons Observatory
(2503.00636) e o fim do CMB-S4.

**Errata da gerência (em nome próprio).** A `ORDEM_K01` dizia “2,95σ de tensão contra a previsão, crescendo com a precisão”. É a frase do
core selado (`neutrino_m2.values.tensao_atual_sigma`, reflexo do ajuste global NuFIT de 12/2025, que CONTÉM o JUNO). O perito oficial do
canal, desde a v392 (`neutrino_m2_perito_v392`), é a leitura autônoma do JUNO: 2,21σ com 59,1 dias. Com 207,2 dias a mesma leitura dá
1,93σ (em Δm²; 1,94σ na forma em m₂, que é a da regra congelada). Na série autônoma a tensão CAIU com a precisão. A sua correção fica;
a frase da ordem fica como registro, com esta errata ao lado.

## Por que há uma segunda rodada

O operador pediu «um teste agora às cegas com poder preditivo acima de 5 sigma». E ele já disse, em 27/10/2026, o que pensa de
“pré-registre e espere o dado” como resposta (fala guardada na memória `cinco-sigma-fora-da-cosmologia-27out.md`, sha16
`20b449c7fd799626`): «É isso, prossiga, as outras formas foram indicações de pré-registro para dados futuros e eu desprezei porque já
fizemos isso». A K01 termina em “esperar o m₂”. Pode ser a resposta certa; mas antes de a gerência levá-la a ele, (1) o “agora” tem de
estar ESGOTADO com consulta citada, e (2) ele tem de ouvir o que o teste do m₂ pode devolver, inclusive contra. É isto que esta ordem pede.

Valem todas as regras do `LEIA_PRIMEIRO.md`. Nada se abre; nada se executa; o teste H0DN × BG1 não se reabre.

## A. Fechar o “agora” no setor de Hubble, pelo Mapa (não refazer)

A gerência consultou o Mapa por termos (`D1B`, `Pantheon`, `masers`) e leu, sem abrir as rotas por inteiro, que esta casa já examinou:
a leitura do fluxo acumulado em registros INTERMEDIÁRIOS (veredito que começa por
`ACCUMULATED_FLOW_READING_AT_INTERMEDIATE_REGISTERS__DISFAVORED_ABOVE_3_SIGMA`); a derivação R-E (“K não age na luminosidade nem no
ângulo; η = 1; não discrimina”); a “forma Q” (revisão independente da separação esperada); o Pantheon canônico de 1593 supernovas; os
cinco leitores da Fase 9, com TDCOSMO e masers já dentro do composto; as Fases 1 a 5.

1. Abra essas rotas (`rotas.py ver <rota>`) e monte a lista COMPLETA do que o setor de Hubble já teve examinado: leitura, dado,
   veredito, rota, seq. Uma linha cada.
2. Responda, com essa lista na mão: existe HOJE algum composto no setor de Hubble, com dado público, que esta casa NUNCA compôs e que NÃO
   seja previsível por agregados já publicados? A lei `K = E(z*)^(2β/3)` é enunciado de extremos (local × fundo em z* = 1089,95) ou
   define, com zero parâmetro, a leitura de âncoras em redshift intermediário? Cite o arquivo e a linha da derivação; não invente forma
   nova. Se a leitura intermediária está morta pelo Mapa, diga “morta, rota tal”, e o canal não existe.
3. As determinações locais independentes da rede H0DN (de um passo só, sem escada: masers, SN II por fotosfera em expansão, lentes com
   atraso temporal, sirenes, SZ/raios X, FRB): quais já entraram na H0DN ou na Fase 9, quais não; valor e σ publicados
   `[KNOWN, a conferir]` com identificador; a decomposição do requisito (o revisor calcula σ_local ≤ 1,26 % para D90, dado o erro do
   fundo); alguma chega lá, e com que data? Mesmo abaixo de 5σ e sem cegueira, diga se serve como LINHA DE INDEPENDÊNCIA para as
   ressalvas 3, 4, 5 e 7 (outra calibração, outra tabela de erros), e com que número.

## B. O neutrino m₂: o que o “D” é, o que o teste pode devolver, a segunda testemunha e o calendário

O revisor achou dois pontos graves que a entrega não diz, e a gerência precisa deles escritos antes de ir ao operador.

1. **O que é o “D” deste canal.** O seu D é a distância entre a previsão (7,2376) e o centro que o JUNO JÁ mediu (7,388), em unidades
   do erro futuro. O nulo é “o centro de hoje é a verdade”. Então “D ≥ 5 com 0,3 %” quer dizer: se o centro não se mexer, a medida
   futura fica a 5σ ou mais da PREVISÃO. O revisor estimou, sob o posterior público de hoje, a probabilidade de r_P ≥ 5 CONTRA a
   previsão: cerca de 0,69 com 0,3 % e 0,35 com 0,5 %. Escreva a TABELA DE DESFECHOS PROVÁVEIS: para cada precisão futura (0,7 %; 0,5 %;
   0,407 %; 0,324 %; 0,3 %; e σ = 0,024×10⁻⁵ da Tabela 6 de arXiv:2204.13249), a probabilidade de cada ramo da regra congelada, sob
   duas hipóteses ditas (o posterior público de hoje; e “a verdade é a previsão”). É conta de planejamento sobre números já lidos; sai
   marcada como tal. É esta tabela que a gerência lê ao operador antes de qualquer ratificação.
2. **O arredondamento.** “0,3 % cruza D90” vem de arredondar: com σ = 0,024×10⁻⁵ (Tabela 6), D = 6,266, ABAIXO de D90 = 6,2816; e o
   erro real aos 207 dias (0,078) é 1,5 vezes o que a extrapolação do projeto daria. Corrija AO LADO e refaça a data em que 5σ e D90
   ficam alcançáveis a partir do artigo de 207 dias (o orçamento de sistemáticas dele; “seis anos” em dias vivos), não só do projeto.
3. **A métrica.** A regra congelada é escrita em m₂ (`|m2_obs − m2_TGL|/σ_obs`); a sua entrega passou a Δm² sem declarar emenda
   (r = 1,9381 na forma congelada; 1,9281 na sua). Diga qual vale e por quê; se propõe trocar, é emenda, e emenda se declara.
4. **A primeira leitura prospectiva.** A regra V2 foi hasheada em 08/08/2026 (core: `neutrino_m2.frozen.portado_de`; `checks[4]`: “a
   regra hasheada julga as próximas medidas”). A liberação de 207,2 dias saiu em 29/09/2026, DEPOIS. Confira as datas e diga: ela é a
   PRIMEIRA leitura prospectiva da regra congelada? O que a função devolve (a gerência lê `TGL_NU_M2_ARMED_CONSISTENT`, 1,94σ)? O que
   impede chamá-la de leitura cega, se algo impede (esta casa leu o número em 30–31/10: memória
   `e0-cadeia-conferencia-kimi-e-no-go-31out.md`)?
5. **O incremento.** A liberação nova é cumulativa e contém os 59 dias. A conta de cabeça da gerência, só estatística e por variância
   inversa, para os dias 59 a 207 sozinhos: centro ≈ 7,31 e σ ≈ 0,10 (×10⁻⁵ eV²); cerca de 0,7σ da previsão e 1,9σ do centro anterior.
   CONFIRA e corrija: que correlação entre as liberações a colaboração publica; o incremento é estimável com o que é público; qual o
   erro certo. E desenhe o teste SÓ COM O INCREMENTO futuro (o revisor estima de 1.400 a 2.200 dias vivos de dado novo para o poder
   sozinho, pela raiz do tempo): estimador, covariância necessária, poder, data.
6. **A segunda testemunha (não refazer).** Parta de `work\neutrino_E0_autonomia_30out\` (as dez determinações públicas que você mesmo
   levantou em 30/10). Para cada determinação SEM o JUNO: valor, σ, razão r contra a previsão, experimento, ano, identificador primário.
   O revisor leu: KamLAND 2,5 %; SNO+ cerca de 3 %; reator + solar sem JUNO cerca de 2,2 %; nenhuma chega a 0,407 %. Confira nas fontes
   primárias e acrescente as previsões com data (Hyper-Kamiokande solar, DUNE solar, o que houver).
7. **O negativo é alcançável?** Com a regra congelada (FALSIFIED só com DUAS determinações independentes ≥ 5σ; MATCHED só com duas a 1σ)
   e sem segunda testemunha com poder, FALSIFIED e MATCHED ficam inalcançáveis na prática, e a sua Q1 pede ao operador um S que não
   existe. Diga isso no topo da entrega, sem suavizar: teste que não pode devolver o negativo não é teste. Reescreva a Q1 como ela é:
   “a regra de morte congelada em agosto não pode disparar; o que fazer?”, com as alternativas listadas SEM escolher (manter e dizer que
   o canal só devolve tensão; uma testemunha só, com que limiar; outra), o que cada uma custa, e lembrando que mudar regra congelada é
   emenda declarada, ato do operador.
8. **A errata do core para a v412.** O core v411 traz em `neutrino_m2.theorem` e em `checks[1]` “a tensão cresce com a precisão”, e
   `projecao_2031_sigma = 7,84`. Redija a errata AO LADO: a escada datada ganha o degrau de 29/09/2026 (JUNO autônomo, 207,2 dias); a
   frase vale para o reflexo global de 12/2025, não para o perito oficial; a projeção de 2031 fica como registro, com a premissa dita
   (centro parado no valor de então). Só o texto e os números com fonte; quem instala é a gerência.
9. **As correções menores da revisão**, ao lado: o validador nunca exerce o ramo UNDER (D padrão 6,0); os sub-rótulos que colapsam; o
   caso em que P some quando S é INVALID.

## C. A combinação pré-registrada de canais cegos, e o ringdown

- Para os canais com dado ainda não lido por esta casa e independentes entre si (o próximo incremento do JUNO; o N_eff do Simons
  Observatory; o que mais você achar): o poder de desenho CONJUNTO sob uma regra de combinação congelada (diga as candidatas: soma de z,
  Fisher, razão de verossimilhança do pacote contra os nulos); o que a hipótese conjunta testa (o PACOTE das leituras derivadas, não β
  isolado); a primeira data em que D conjunto ≥ 6,28 é plausível.
- O ringdown: o revisor calcula cerca de 25,5 a 25,7 eventos elegíveis para D90; quantos existem nos catálogos públicos de hoje, com que
  taxa e data se chega lá. E diga, com a fonte, se o conjunto D entra “pela teoria”: o operador retirou ao lado o par do ramo B (memória
  `ramo-b-reaberto-05out.md`, 28/10: a rota superada pela leitura do autor e pela calibração A), e D só decide esse par.

## D. As sete ressalvas, uma a uma, sem teste novo

Para cada uma das sete (`ressalvas_secao8` do registro selado): que ATO a resolve — teste cego novo; dado independente; um número de
desenho; ou nenhum, porque é história e fica dita. Para as que aceitam número, DESENHE a conta e NÃO a rode:

- **Ressalva 5** (72 direções de variância zero na tabela de erros publicada): o piso de variância nessas direções que derruba o D de
  desenho de 6,71 para 6,28 e para 5. Usa só a tabela de erros publicada e os pesos congelados; nenhum vetor de dado.
- **Ressalvas 3 e 4** (a linha das Cefeidas livres espera 4,5σ): que melhora do orçamento de calibração leva essa linha a 5 e a 6,28.
- **Ressalva 7** (tentativas anteriores, sobreposição): quantas tentativas independentes fazem um 6,11 local cair a 5 global (Šidák), e
  a contagem honesta das tentativas desta casa pelo Mapa. Sobreposição de dado não é tentativa independente: separe as duas coisas.

Para cada conta: os insumos (arquivo e hash), a fórmula, o que um número ruim significaria (fragilidade do erro publicado, não
falsificação da lei) e se rodá-la é “reabrir” (o `executar_abertura_v411.py` nunca roda). A gerência lê essa partitura ao operador antes
de qualquer número sair.

## E. Para ninguém confundir

Um parágrafo: o que a P7 (a convergência de modelos, ordem K06) pode e o que não pode dizer sobre as sete ressalvas. A leitura da
gerência: nada, porque ela decide sobre o leitor e não sobre a natureza; é teste cego que pode rodar hoje, mas de outra pergunta. Diga
se está certo ou corrija.

## O que entregar

- `ENTREGA_K04.md`: até 15 linhas no topo, começando por duas frases: (1) “existe hoje teste cego de natureza com poder de desenho
  ≥ 5σ executável? Se não, qual é a primeira data, e do que ela depende?”; (2) “o que o teste do m₂ mais provavelmente devolve, pelo que
  já é público, e o que esse desfecho significaria: falsificação do pacote da escala (o Um posto em 1 eV com m₁ ≈ 0), ou outra coisa”.
- `HUBBLE_JA_EXAMINADO_K04.md` (seção A), `M2_DESFECHOS_E_SEGUNDA_TESTEMUNHA_K04.md` (seção B, com a tabela de desfechos),
  `COMBINACAO_K04.md` (seção C), `RESSALVAS_UMA_A_UMA_K04.md` (seção D), `ERRATA_NEUTRINO_V412_RASCUNHO_K04.md` (B.8).
- `PERGUNTA_K04.md`: só o que sobrar para o operador, já enxuto (a Q1 reescrita; a Q2 depois da tabela de desfechos).
- `REGISTRO_MAPA_K04.json` (a gerência registra).

## O que NÃO fazer

Não baixar nem ler vetor de dado; não calcular estatística observada nova de teste nenhum; não rodar as contas da seção D; não
escolher canal pelo resultado esperado a favor; não reabrir rota morta: citar a rota. Número de literatura com arXiv ou DOI e a marca
`[KNOWN, a conferir]`. Se a resposta do topo for “não existe”, diga isso sem suavizar: é parede medida, e parede medida é resultado.
Nos depósitos da fila, escreva “revisada internamente”, não “aprovada em revisão independente”: o veredito é de quem confere.

— gerência c1, 13/11/2026.
