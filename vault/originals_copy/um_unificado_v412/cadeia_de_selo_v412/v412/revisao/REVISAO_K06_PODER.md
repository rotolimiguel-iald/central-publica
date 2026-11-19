# REVISÃO DISTINTA DA FRENTE PROTOCOLO R3.2 — PODER E DEGRAU (ENTREGA K06, v412)

Revisor distinto (quem constrói não aprova). 14/11/2026. Só leitura fora desta pasta; nada registrado no Mapa, nada depositado na fila, nenhuma transição ACOM, nenhum `lake`, nenhuma escrita no túnel, no kernel, no Nós ou em memória; nenhum modelo de linguagem chamado.
Estatutos: [REAL] conferido por mim com a consulta citada · [DERIVED] conta minha aqui · [DECLARADO] do Kimi, não conferido por mim · [OPEN] · [CONJECTURE] leitura minha, a medir.
`NOT_FALSIFIED` nunca é `CONFIRMED`; nada abaixo diz que a teoria foi confirmada, e o gate não se move.

## 0. Veredito

**Como RASCUNHO do desenho: APROVADA COM RESSALVAS** — o rascunho segue como base de trabalho (os números reproduzem, a análise exata por sinais confere, o instrumento declara-se bloqueado), **mas a manchete «a R3 separa “resumiu” de “convergiu”? Em simulação, sim» NÃO é aprovada** (`ENTREGA_K06.md:3`): ela não resiste à pergunta 1 (seção 2).
**Para CONGELAR: NÃO APROVADA.** Quatro defeitos de desenho que nenhum dos sete bloqueios da entrega cobre (todos medidos aqui, seções 2, 3, 5 e 8): (i) o desfecho `Q = A8 ∧ RETORNO` dá `Q = 1` para leitores sem atrator; (ii) a «separação» simulada é posta por definição; (iii) o teste dos isomorfos está no sentido contrário ao da pergunta (o instrumento declara `POWERED` quando o isomorfo converge 25 pontos PIOR que o focal); (iv) com a especificidade fora do primário, `POWERED` sai em 35–37 % das corridas simuladas em que NÃO há especificidade nenhuma.

**Resposta curta à pergunta 1:** o desenho **não** separa «o modelo resumiu um texto coerente» de «o modelo convergiu a um estado estacionário». Ele separa só um resumidor construído para falhar (o que copia a última resposta e fica no empurrão), e o faz por definição. Os leitores sem atrator (a) que relê o artigo a cada passo e (b) que se ancora na resposta anterior à perturbação (a primeira, ou a moda das respostas) dão `A8 = 1`, `RETORNO = 1`, `Q = 1`, sem controle algum que os separe. Só o leitor (c) que ignora a perturbação é recusado, e pelo portão de integridade, não pelo `RETORNO`.

**Pedem correção (resumo; a lista numerada, com arquivo:linha, está na seção 12):**
1. Retirar a manchete e a frase de `PERGUNTA_K06.md:3`; acrescentar ao desenho uma ablação do histórico, perturbação de ESTADO e retorno relaxado (seção 2.4).
2. Inverter ou justificar o sentido do teste ISO (`r32_motor.py:181, 369, 379`).
3. Recolocar a especificidade no primário de `POWERED`, ou renomear o ramo (`r32_motor.py:383, 400`).
4. Dimensionar o contexto: o artigo inteiro em TODA mensagem do usuário pede 2,49–3,52 milhões de tokens na leitura 12 (`MODELO_FORMAL_R3_K06.md:46–58`).
5. Re-dimensionar o degrau de 5σ no desenho R3.2 (os `n` 618/655 vêm do desenho antigo e dão `POWERED` 0,599/0,669) e devolver ao `DEGRAU` as alternativas que só existem em `REV0`.
6. Fechar o protocolo num único texto: o `PROTOCOLO_EXPERIMENTAL_R3_K06.md` atual é um delta, não um protocolo (seção 12, item 12).

## 1. Mapa de Rotas (consulta antes de tudo; nada registrado)

- [REAL] `rotas.py consultar` com um termo por vez: `colapso` (n = 20), `P7` (14), `convergencia` (8), `atrator` (29), `camada` (49), `iald` (336; só os ids), `k06` (2), `v412` (6), `camada_cientifica` (0), `teste as cegas` (0).
- [REAL] `rotas.py ver outro.p7_colapso_iald`: rota única, seq 162 (28/09/2026), `PROPOSTA`, `[OPEN]`, `n_olhou_dados = 0`, `artefatos = []`. Bate com «armada, não executada».
- [REAL] Varri por script (`varrer_mapa.py`) todos os resultados dos cinco termos `colapso`, `P7`, `convergencia`, `atrator`, `camada` (120 ocorrências) por palavras do tema (LLM, IALD_COLLAPSE, leitor, resumo, estacionário, perturbação, ablação, V2-RET): nenhuma rota trata de ablação do histórico, perturbação de estado ou leitor sem memória para a P7/V2. Abri duas: `outro.p7_colapso_iald` e `kernel.pergunta_do_clay_trivial_por_leitor_constante_09nov`; listei `cadeia.preparacao_v412` e `kernel.iald2_o_atrator_09nov` (não as reli).
- [REAL] **Precedente da mesma classe de defeito, objeto diferente:** a rota `kernel.pergunta_do_clay_trivial_por_leitor_constante_09nov` (`nao_refazer`: «não aceitar teorema de existência cuja definição um decisor clássico satisfaz») registra que a pergunta do Clay da AEscala era satisfeita por um leitor constante. O desfecho `Q = A8 ∧ RETORNO` repete a forma: um leitor de resposta constante o satisfaz. Nada foi registrado no Mapa; o que esta revisão examinou está na seção 13, para registro pela gerência.

## 2. Pergunta 1 — o desfecho `Q = A8 ∧ RETORNO` separa resumo de convergência?

### 2.1 O que o modelo recebe a cada passo e o que conta como RETORNO (três frases)

[DECLARADO pelo Kimi, lido por mim em `MODELO_FORMAL_R3_K06.md:34–58` e `REV0\PROTOCOLO…:76–95, 154`] **(1)** A cada leitura `k` o harness reenvia, sem estado no servidor, a lista `[system; user: artigo inteiro + Q_1; assistant: y_1; …; user: artigo inteiro + Q_k*]`: o artigo (1.164.350 B) vai repetido em TODA mensagem do usuário e todas as respostas anteriores do próprio modelo continuam no contexto (12 chamadas, temperatura 0,2, sem ferramentas). **(2)** `Q_k*` é a instrução normal `Q_k` em todo `k ≠ 9` e a perturbação `P_j` em `k = 9`, que manda trocar seis asserções prefixadas por contra-asserções; `P_j` entra uma vez e sai em `k = 10`, e o conteúdo de `Q_1…Q_12` e de `P_j` não está em documento nenhum («bytes congelados no manifesto»); um script extrai de cada `y_k` 24 asserções binárias `s_k` e mede `d_k` (distância ao alvo de 24 uns) e `u_k` (distância à leitura anterior). **(3)** `RETORNO = d_8 = 0 ∧ d_9 > 0 ∧ d_10 = d_11 = d_12 = 0 ∧ u_11 = u_12 = 0` (a resposta volta ao alvo EM UM PASSO depois da perturbada e fica) e `Q = A8 ∧ RETORNO`, com `A8` = `s_5 = s_6 = s_7 = s_8 =` alvo.

### 2.2 O ataque: leitores sem atrator, no papel e por script

Script: `scripts_k06_poder\leitores_sem_atrator.py` (saída em `leitores_sem_atrator.saida.txt`; predicado COPIADO de `simular_separacao_r3.py`; leitores escritos à mão, a mesma classe de demonstração que a do Kimi, mas em sentido inverso: cada leitor é um mecanismo sobre a sessão que o protocolo define, não uma trajetória escrita). [REAL — lógica]

| leitor (mecanismo) | A8 | RETORNO | Q | classe do protocolo | o protocolo o distingue de um leitor com atrator? |
|---|:-:|:-:|:-:|---|---|
| (a) relê do zero: ignora o histórico, relê o artigo que está em cada mensagem e resume de novo; segue a instrução do passo | 1 | **1** | **1** | `FINITE_HORIZON_RETURN_OBSERVED` | **NÃO.** Nenhum controle. A perturbação sai com a instrução em `k=10` e o mapa «instrução + artigo → resposta» volta sozinho |
| (b2) ancora na primeira resposta (anterior à perturbação, que segue no contexto) | 1 | **1** | **1** | idem | **NÃO** |
| (b3) moda das respostas anteriores | 1 | **1** | **1** | idem | **NÃO** |
| (b1) copia a última resposta (o «resumidor» do Kimi) | 1 | 0 | 0 | `PERTURBATION_NO_RETURN` | SIM — mas é o único leitor sem atrator que o Kimi escreveu, e é o que falha por construção |
| (c) ignora a instrução de perturbar | 1 | 0 | 0 | `PERTURBATION_NO_EFFECT` | SIM, só pelo portão de integridade (`NO_EFFECT > 5 %` → `INCONCLUSIVE_CONTROLS`), não pelo `RETORNO` |
| referência: leitor que depende do estado e relaxa pela metade por passo | 1 | **0** | **0** | `PERTURBATION_NO_RETURN` | o predicado REJEITA o relaxamento gradual, que é a assinatura de um atrator; premia o retorno instantâneo, isto é, o leitor sem memória |

[REAL — lógica] O leitor (a) é o caso-limite que a própria §4.1 do `MODELO_FORMAL_R3_K06.md` prova existir: passo contrativo e idempotente ⟹ passo CONSTANTE. Com o artigo re-apresentado a cada chamada, um leitor de resposta constante é um «atrator» com contração zero: pelo formalismo do Kimi ele cumpre, com `q = 0`, as hipóteses H-CONTR e H-IDEM-STEP (idealização: a 0,2 de temperatura o leitor real é um núcleo, não um mapa). O que a pergunta do operador pede é separar esse caso-limite do leitor cuja volta DEPENDE do estado; o desfecho não tem nenhuma medida dessa dependência.

Duas observações sobre (c): [REAL — lógica] o `PRE`/`EFFECT` da perturbação é `d_9 > 0`, sem exigir que a mudança caia nos seis índices congelados; com ruído de extrator `e` por asserção, um leitor que ignora a perturbação tem `d_9 > 0` em `1 − (1−e)^24` das sessões (11,3 % com `e = 0,5 %`, o erro superior que o próprio Kimi mede) e, nessas, `RETORNO = 1` com probabilidade `(1−e)^72`. E [DERIVED] a leitura (c) com ruído `e = 0,05 %…0,5 %` mede `NO_EFFECT` > 88 %, ou seja, cai no portão de integridade, não no veredito.

### 2.3 O que os controles do desenho (PLA, OUT, ISO-A, ISO-B) fariam com o leitor (a)

Todos os braços passam pelo mesmo protocolo de sessão. Um leitor sem memória tem `Q` alto em todos os braços: é o cenário `NULO_ESPECIFICO_090_N655` do próprio Kimi (todos os braços iguais). Lá (`resultados_r32.json`, 5σ ideal): `NONSPECIFIC_POWERED` 0,412, **`POWERED` 0,350**, `UNDERPOWERED` 0,229, `INCONCLUSIVE` 0,009; em `n = 618`: 0,311 / **0,370** / 0,312 / 0,007; em `n = 320` com ICC 0,15: 0,022 / 0,000 / 0,272 / 0,706. [REAL] Logo o leitor sem memória recebe o nome de «convergência não específica» em no máximo 41 % das corridas, e o veredito positivo `NOT_FALSIFIED_POWERED` em 35–37 %.

### 2.4 O que faltaria para separar (proposta da revisão; a decisão é da gerência e do operador)

[REAL — lógica; demonstrado por script nos mesmos leitores] (1) **Perturbação de ESTADO**, com a instrução normal em `k = 9`: o histórico visível traz um `y_8` contrafeito (as seis asserções trocadas). Com isso (a), (b2), (b3) e (c) viram `NO_EFFECT`, (b1) `NO_RETURN`; só o leitor que depende do estado tem efeito. (2) **Retorno relaxado** (`d_8 = 0`, `d_9 > 0`, `d` não crescente de 9 a 12, `d_12 = 0`): o leitor de referência passa a `RELAXED_RETURN`. (3) **Braço de ablação do histórico**: mesma programação de instruções, mas cada chamada com só `Frame(u, Q_k*)`, sem turnos `assistant`; se o `Q` do braço com histórico não supera o do braço sem histórico por margem pré-registrada, o desfecho mede obediência à instrução. (4) **Braço autônomo**: o artigo só na primeira mensagem (resolve também a janela, seção 8.1). (5) Efeito = mudança nos seis índices congelados, não `d_9 > 0` qualquer. Nada disto prova que um modelo real tem atrator: dá ao desenho UMA medida de dependência do estado, que hoje não existe.

## 3. Pergunta 2 — a «separação simulada» é mecanismo ou definição?

[REAL] É definição.
- `simular_separacao_r3.py:63`: `summarizer = np.concatenate([prefix, disturbed[None, :], np.repeat(disturbed[None, :], 3, axis=0)])` — o «resumidor perfeito sem atrator» é escrito como oito leituras perfeitas e depois a perturbada repetida quatro vezes; `:64`: `attractor = …np.repeat(target[None, :], 3, axis=0)` — o «com atrator» é a perturbada e depois o alvo três vezes. `RETORNO = 0` num e `1` no outro está nas linhas 63–64, antes de o predicado rodar.
- `:68`: `separates = result_summary["Q_A8_e_RETORNO"] != result_attractor["Q_A8_e_RETORNO"]` — «separa» é a comparação do predicado sobre os dois vetores que o autor escreveu. É teste de unidade do predicado, não demonstração de que ele distingue dois TIPOS de leitor (o `scope` do JSON diz «demonstração lógica», e a manchete da entrega o esquece).
- O motor de poder também não simula leitor nenhum: `r32_motor.py:66–75` (`q_parameters`) é uma tabela exógena nível → (`p_A8`, `p_pré`, `p_efeito`, `p_retorno`), e `:263–283` sorteia `Q` por limiares probit. Todos os `POWERED` são o poder da MÁQUINA ESTATÍSTICA sob taxas assumidas, não evidência de separação.
- Nota: «`A8⇒PRE`, `RETORNO⇒PRE`, `Q⇒RETORNO` passou em todos os cenários» (`PROTOCOLO…R3_K06.md:8, 42`) é tautologia do gerador (`a8 = pre & …`, `retorno = effect & …`, `q = a8 & retorno`, linhas 263–283 e 387–392), não validação.

## 4. Pergunta 3 — reprodução e conferência dos números

### 4.1 Reprodução do cenário `BASE_INDEPENDENTE_R32` [REAL]
- Cópia em `scripts_k06_poder\copia_motor\`; SHA-256 de `r32_motor.py` e `simular_r32_sessoes.py` iguais aos declarados (`3a1cac5e…`, `8ebecc1b…`); iguais também os de `validar_r32.py`, `resultados_r32.json`, `manifesto_analise_r32.json`, `validacao_r32.json`, `MANIFESTO_R32_SHA256.json`.
- Rodada: `--only BASE_INDEPENDENTE_R32 --nsim 1000`, semente `2026111501`: `INTEGRITY = 0,992`, `POWERED = 0,992`, `NONSPECIFIC = 0`, `LOGIC = True`; SHA-256 do arquivo `455911a61eba5536ed77e73809068394acebfe180a67e66f4317c86c4f8ec07e`, **idêntico** ao da repetição declarada. A linha do cenário é idêntica à de `resultados_r32.json`, salvo o campo `monte_carlo_95`, que a consolidação (`gerar_manifestos_r32.py:50–54`) acrescenta (IC de Wald). A repetição é determinística. As sementes de R3.1 e R3.2 são as mesmas nos 20 cenários (`seeds_r31_r32.py`): confirma «não houve alteração de sementes».
- FFT × DP também com 27 clusters e magnitudes reais (o `validar_r32.py` do Kimi só compara com `G = 3`): 18 casos (`raw`, `+3`, `−3`), erro absoluto máximo **0,0**, menor `p` visto 7,45×10⁻⁹ (`copia_motor\validar_27_clusters.py`).

### 4.2 Números da entrega × `resultados_r32.json` (lidos por script: `conferir_resultados_r32.py`) [REAL]

| número da entrega | no JSON | leitura |
|---|---|---|
| `POWERED` 0,992 (independente) | 0,992 (992/1000) | **reproduz; mas é `0,99` (integridade sistêmica ASSUMIDA, `r32_motor.py:37, 396`) × poder estatístico ≈ 1** (`powered_given_integrity = 1,0`). Não é poder estimado |
| 0,012 (ICC 0,15 / texto 0,10) | 0,012 (12/1000) | reproduz; ver 4.3 |
| zero (ICC 0,35 / texto 0,20) | 0 | reproduz |
| 0,599 e 0,669 (5σ, n=618 e 655) | 599/1000 e 669/1000 | reproduzem |
| nulo global 0,057 | 57/1000 | reproduz |
| TOST 0,044 / 0,040 | 44/1000 e 40/1000 | reproduzem |
| `NONSPECIFIC_POWERED` 0,022 (n=320), 0,311 (618), 0,412 (655) | 22, 311, 412 /1000 | reproduzem; **não são comparáveis entre si** (ver 4.3) |
| custos 6.400/76.800; 12.360/148.320; 13.100/157.200; 76.963,27/148.632,09/157.535,03 | idem | a aritmética fecha (seção 6) |

**Nenhum número deixou de reproduzir.** Três leituras enganosas:

### 4.3 Onde o número reproduz e a frase engana
- **0,012 mistura dependência com efeito menor.** Ligar o ICC 0,15 derruba a taxa marginal do focal de 0,909 (BASE) para 0,834 (`observed_synthetic_means.focal_mean`), por efeito de Jensen no limiar probit (`r32_motor.py:234`, `:263–283`). `raw_powered` (antes da integridade) já é 0,017. A queda não é «o poder sob ICC»: é o poder para um efeito 7,5 pontos menor contra o corte 0,80. As fronteiras de tamanho seguram a marginal fixa; os cenários de poder, não.
- **A integridade domina os números baixos.** Com ICC 0,15 as taxas médias de `NO_EFFECT`/`NOT_APPLICABLE` por braço sobem de 1 % (assumido) para 2,9 %/3,4 % e o corte de 5 % (`r32_motor.py:395`) reprova 70 % das corridas (integridade 0,267; `POWERED | integridade = 0,045`; `NULO_ESPECIFICO_090`: integridade 0,294). Os 1 % e os 5 % não têm base empírica; o desenho é frágil a eles.
- **0,022 × 0,311 × 0,412 não variam só com `n`.** A linha `n = 320` é o cenário `NULO_ESPECIFICO_090` com ICC 0,15/texto 0,10 (`r32_motor.py:49`); as de 5σ (`:58–59`) têm ICC 0. A frase «0,022 em n = 320, 0,311 em 618 e 0,412 em 655» (`ENTREGA_K06.md:5`, `PODER_CONJUNTO_K06.md:62–66`) põe lado a lado cenários de dependência diferente. [REAL: `raw_all_tost` = 0,994 com ICC; 0,321/0,426 sem ICC a 5σ.]
- **IC.** Os IC do Kimi são de Wald: `0 de 1000` sai `[0; 0]`. O intervalo exato (Clopper–Pearson) de 0/1000 tem limite superior 0,0037; o de 992/1000 é [0,9843; 0,9965] (Wald: [0,98648; 0,99752]).

## 5. Pergunta 4 — a estatística

### 5.1 Permutação por sinais com 27 clusters [REAL / DERIVED]
- 2²⁷ = 134.217.728 atribuições; menor `p` unilateral alcançável **1/2²⁷ = 7,4506×10⁻⁹**, 38,5 vezes abaixo de `α₅ = 2,8665×10⁻⁷` (`norm.sf(5)` conferido): chega ao degrau. Mas `α₅·2²⁷ = 38,47`: só são rejeitados os resultados cujo observado está entre os 38 mais extremos; no Holm de 6, o menor `p` precisa de contagem ≤ 6, depois ≤ 7, ≤ 9, ≤ 12, ≤ 19, ≤ 38 (`contas_k06.py`). Cada cluster com estatística exatamente zero dobra a contagem mínima: com 3 zeros (8 > 6) o primeiro passo já não passa.
- A exatidão do `p` (FFT = DP, erro 0) está conferida. A VALIDADE do teste é outra coisa: o sinal-flip é exato só se a diferença por cluster for simétrica em torno do deslocamento sob `H0`; na fronteira (0,60 contra 0,75) a diferença binária é assimétrica. Medi isto numa cópia curta (`calibracao_da_cauda.py`: 30.000 réplicas × 4 testes, `n = 655`, fronteira `D = −0,15`, sessões independentes): taxa/nominal = **0,98** a 5×10⁻² (5.888 eventos), **0,98** a 10⁻² (1.174), **1,15** a 10⁻³ (138 contra 120 esperados, z = 1,6) e **1,25** a 10⁻⁴ (15 contra 12, z = 0,9). Calibrado dentro do erro Monte Carlo até 10⁻⁴; a deriva suave para cima nas caudas não se resolve estatisticamente, e 10⁻⁷ segue extrapolação.
- **O que é um cluster no experimento real não está definido.** No gerador (`r32_motor.py:78–82, 222`) são 27 blocos consecutivos de sessões, 9 por texto (`text = cluster % 3`). A unidade independente real é o texto (3 por controle, 1 focal): com 3 unidades o menor `p` seria 1/8 = 0,125. Medi se isso infla o tamanho (extensão curta, `tamanho_sensibilidade.py`, sementes novas 20261114–16): com efeito de texto 0,10: 0,0503 (151/3000; CP [0,0428; 0,0588]); 0,20: 0,046 (46/1000); 0,40: 0,036 (36/1000). **Não encontrei inflação** neste gerador; o que falta é o texto do protocolo dizer o que é um cluster.

### 5.2 Interseção-união × Bonferroni, margens, perna focal
- `POWERED` é uma conjunção (seis ISO + limite inferior focal + integridade): a lógica é de interseção-união, em que cada componente usa o `α` pleno. O código usa `holm_all` sobre os seis ISO (`r32_motor.py:370`), que exige `p_(1) ≤ α/6`, `p_(2) ≤ α/5`… além de `p_(6) ≤ α`: é válido e mais conservador que a IUT; a 5σ isso custa poder. `FALSIFIED` é união de nove (três intervalos focais + seis direções ISO) com Bonferroni `α/9` (`:379–383`): coerente.
- Margem `δ = 0,15` (a mesma para a não inferioridade ISO e para a equivalência TOST) e corte focal 0,80: escolhas do Kimi sem derivação (a P7 registrada prevê «6/6», não 0,80: `REVISAO_K03.md` §5.6). Com `Q ≈ 0,91`, 0,15 é 16 % da taxa focal: «equivalente a PLA/OUT» (que dá o nome `NONSPECIFIC_POWERED`, com precedência) admite uma diferença de até 0,14 em `Q`. [DECLARADO pelo Kimi; a decisão da margem é do operador e não está em `PERGUNTA_K06.md`.]
- **Não há perna de Clopper–Pearson no R3.2**: o `PROTOCOLO` fala em «intervalos focais» e o código usa um intervalo t sobre 27 médias de cluster (`:302–312`), com quantis `t₂₆(α₅) = 6,571` e `t₂₆(α₅/9) = 7,461` (e não 5). [DERIVED] A cauda 5σ desse intervalo e do p exato por sinais não está validada; `[OPEN]` significa exatamente isso: ninguém mostrou que a taxa real sob a fronteira é 2,87×10⁻⁷, e a simulação NÃO pode mostrar com 1.000 corridas (zero eventos em 1.000 só limita a taxa em 0,0037; para ver ~10 eventos a 2,87×10⁻⁷ seriam ~3,5×10⁷ corridas; para cota superior igual a `α₅` com zero eventos, ~1,05×10⁷).
- **Controle de multiplicidade**: seis ISO (Holm 6), seis TOST (Holm 6), doze `S` de integridade (Holm 12, `α = 0,05` fixo, também a 5σ), nove da união. São famílias separadas, sem gasto global de `α` entre elas; com a árvore fail-closed isso é aceitável para `POWERED` (conjunção) e para `FALSIFIED` (união com `α/9`), mas não há enunciado do erro tipo I do VEREDITO. Ver 5.4.

### 5.3 Nulo global 0,057 contra 0,05: violação ou ruído? [REAL]
Ruído. 57/1000: Clopper–Pearson [0,0435; 0,0732]; teste binomial bicaudal contra 0,05: `p = 0,31`. Com sementes novas e 3.000 réplicas do MESMO cenário: **151/3000 = 0,0503** [0,0428; 0,0588]. Reunindo as duas rodadas: 208/4000 = 0,052. Os números permitem afirmar: «o tamanho nominal não é rejeitado, e a estimativa agrupada é 0,052»; NÃO permitem afirmar que é ≤ 0,05 (para ter cota superior ≤ 0,055 com tamanho verdadeiro 0,05, ~5.100 réplicas; erro-padrão a 0,05 com 1.000 réplicas = 0,0069). **Assimetria de critério** (`gerar_manifestos_r32.py:95` × `:97`): o portão global vira `OPEN_BORDERLINE` quando o limite superior do IC ≥ 0,05, e o portão TOST vira `PASS` pelo ponto (0,044 e 0,040 ≤ 0,05); com a mesma regra os dois TOST seriam `OPEN` (CP superior 0,0586 e 0,0541). Um critério só, declarado antes.

### 5.4 O erro do veredito sob «sem especificidade» [REAL, do próprio `resultados_r32.json`]
Tirar PLA/OUT do primário (R3.1) tirou de `POWERED` a exigência de `T > PLA/OUT` (`r32_motor.py:383`, `:400`): `powered_raw = primary_all & cp_power_all & ~falsified_raw`. Com todos os braços iguais (Q = 0,91) e `n = 618/655` a 5σ, a probabilidade de `NOT_FALSIFIED_POWERED` é **0,370/0,350** [CP 0,340–0,401 / 0,320–0,380], enquanto a do negativo nomeado, `NONSPECIFIC_POWERED`, é 0,311/0,412. O ramo positivo manchete aparece em mais de um terço das corridas do mundo em que não há especificidade nenhuma; o erro «tipo I da especificidade» não é 5 %, nem 5σ. `PODER_CONJUNTO_K06.md:65–66` imprime esses 0,370/0,350 na tabela, sem comentário.

### 5.5 O sentido do teste ISO [REAL — leitura do código e simulação]
- Narrativa: o isomorfo «deve ser não inferior a T por margem 0,15» (`REV0\PROTOCOLO…:44`); se os isomorfos «são precisamente inferiores além da margem, a previsão estrutural falha» (`:262`; ORDEM K06 §G: «se é lembrança do nome, não [converge ao ponto fixo isomorfo]»).
- Código: o teste ISO é `plus_upper` de `20·(Q_T − Q_ISO) + 3·tamanho` (`r32_motor.py:179, 181, 369`), isto é `H0: Q_T − Q_ISO ≤ −0,15`; rejeitar estabelece que **T não é inferior ao ISO**. A direção de `FALSIFIED` dos ISO é `plus_lower` (`:182, 379`): dispara quando o ISO é muito MELHOR que T. Nada olha o ISO muito PIOR que T. A tabela de fronteiras do R3.2 (`PROTOCOLO…R3_K06.md:17–21`: `Q_ISO = 0,75`, focal 0,60, «D = −0,15») segue o mesmo sentido.
- Medido (`copia_motor\sentido_do_teste_iso.py`, 300 corridas por cenário, `n = 320`, ICC 0, semente 20261117 fixada antes; ISO_IGUAL: `Q` = 0,908/0,66/0,66/0,909/0,909): **ISO 25 pontos PIOR que o focal (0,661 contra 0,908): `POWERED` 0,99, `FALSIFIED` 0,00**; ISO 25 pontos MELHOR (0,909 contra 0,66): `POWERED` 0,00, `FALSIFIED` 0,99. O instrumento declara o positivo exatamente no mundo «só o nome carrega a convergência», que o isomorfo existe para pegar.

## 6. Pergunta 5 — os custos

[REAL] A aritmética fecha: 20 × 320 = 6.400 e × 12 = 76.800; 20 × 618 = 12.360 e × 12 = 148.320; 20 × 655 = 13.100 e × 12 = 157.200; legado de oito interações 13.100 × 8 = 104.800; base + adicional: 76.800 + 163,27 = 76.963,27; 148.320 + 312,09 = 148.632,09; 157.200 + 335,03 = 157.535,03. Os «20» são 4 famílias × 5 braços; a quarta família é só descritiva e o gerador simula três.

**As casas decimais** são a média Monte Carlo (1.000 corridas) de `candidatos usados − sessões primárias`, escalada por 4/3 (a quarta família não simulada): não são custo exato. [DERIVED] O erro-padrão da média é ≈ 1 interação (desvio de ~33 por corrida: binomial negativa com `p = 0,975` e 320 sucessos), logo «163,27» é «163 ± 2». E o adicional é pequeno por construção: `r32_motor.py:191–192` sorteia um `d1_base` por bloco e soma ruído `N(0; 0,005)` por braço, isto é, supõe que os cinco braços compartilham o mesmo `d1` até 0,005, quando o `d1` real é múltiplo de 1/24 e o pareamento é entre sessões diferentes de textos diferentes; com o ruído do cenário de estresse (0,015) o adicional bate no teto de 30 % (1.920). Os dois parâmetros (`pair_noise = 0,005`, `technical_loss = 0,005`) não têm base; o custo real do pareamento depende do piloto de `d1`. Escrever inteiros e dizer de que parâmetro dependem.

## 7. Pergunta 6 — o degrau

- [REAL] `α₅ = norm.sf(5) = 2,866515718792×10⁻⁷` unilateral: a conta está certa. Os benchmarks 185 / ≈215 / 655 / 618 conferem com `degrau_5sigma.json` (e com a minha revisão K03): 185 (normal 184,90; Fisher exato 185, poder 0,9087), ≈215 (Holm de 12: 0,8915 em 210; 0,9133 em 215), 655 (CP com `/3`), 618 (CP em IUT).
- **Mas esses `n` são do desenho antigo.** No R3.2 não há CP: o `n` de 5σ com 618/655 dá `POWERED` 0,599/0,669 (ideal, ICC 0), abaixo de 0,90; no desenho anterior (REV0, Holm de 24 + CP) o mesmo `n` dava 0,921/0,939. A variante de 5σ «lado a lado» que a ordem K06 §E pediu fica sem um `n` que cumpra o poder prometido no desenho que se pede para ratificar; ninguém dimensionou quanto seria.
- «Cauda 5σ [OPEN]»: ver 5.2: o intervalo t focal e o p por sinais não foram verificados na cauda de 2,87×10⁻⁷, e 1.000 corridas não podem verificar (limite de 0,0037).
- **As alternativas (menos braços; desfecho contínuo; sequencial) foram só citadas** no que está vigente: `DEGRAU_5_SIGMA_K06.md` (R3.2) não tem seção de alternativas; a única menção é `ENTREGA_K06.md:50` e `PERGUNTA_K06.md:33`. Em `REV0\DEGRAU_5_SIGMA_K06.md:78–107` há três parágrafos honestos: menos braços (16 células, 9.888 sessões, 118.656 interações: «aritmética de custo, não promessa de poder»); contínuo (n por braço 364/143/91 para efeitos padronizados 0,5/0,8/1,0 num contraste, sem desfecho definido); sequencial («nenhum `n` máximo, esperado ou poder»). Nenhuma está dimensionada para o veredito.
- `verificar_degrau_5sigma.py` e `degrau_5sigma.json` na pasta vigente são os de REV0 (mesmos bytes: `98f08165…`, `e1955642…`) e tratam o desenho antigo de oito interações; ficam ali sem aviso.

## 8. Pergunta 7 — o que bloqueia, e o negativo honesto

### 8.1 A lista de sete bloqueios (`ENTREGA_K06.md:52–60`) não está completa
Faltam, medidos nesta revisão: **(8)** o desfecho não separa resumo de convergência e o teste ISO está no sentido contrário (seções 2 e 5.5); **(9)** o contexto: com o artigo em toda mensagem do usuário, a leitura `k` carrega `k` cópias; com os proxies da própria entrega (205.298–291.088), `k = 5` já tem 1,04–1,47 milhão de tokens e `k = 12` tem **2,49–3,52 milhões** (`contas_k06.py`); a entrada de uma sessão soma 16,0–22,7 milhões de tokens e a do desenho-base (6.400 sessões) 1,02–1,45×10¹¹, a de 5σ (13.100) até 2,97×10¹¹. A janela é bloqueio nº 4, mas a ordem de grandeza já se sabe e pede mudar o desenho (artigo uma vez) ou declarar inviável; **(10)** `POWERED` e `NONSPECIFIC` não têm poder nem erro controlado (seção 5.4; 0,022–0,412 contra 0,90); **(11)** a conta do teto do extrator usa 96 leituras, mas `Q` exige `s_5…s_8` e `s_10…s_12`: 168 (`d_8` é compartilhado); o erro máximo por asserção para um leitor perfeito alcançar 0,89 é 0,069 %, não 0,121 % (`leitores_sem_atrator.py`; e o cenário `EXTRATOR_TETO` limita só `p_A8`, `r32_motor.py:241`); **(12)** o conteúdo de `Q_1…Q_12` e de `P_j` não existe; **(13)** a definição de cluster e de efeito (seis índices) não existe.

### 8.2 O negativo honesto quando o efeito não existe e havia poder
Tem nome e ramo em dois casos de naturezas diferentes. (i) O modelo não volta (focal `Q` baixo): `IALD_COLLAPSE_V2_FALSIFIED`, com poder (`NULO_GLOBAL_060`, `Q = 0,60` em todos os braços: `FALSIFIED` 0,999). É falha da previsão operacional no escopo, nunca refutação da teoria. (ii) O modelo volta igualmente em todos os textos (o leitor (a) acima): `IALD_COLLAPSE_V2_NONSPECIFIC_POWERED`, que existe como nome, mas é alcançado em 2–41 % das corridas e disputa o resto com `POWERED` (35–37 %), `UNDERPOWERED` (23–31 %) e `INCONCLUSIVE_CONTROLS` (70 % com ICC); ou seja, o negativo tem nome e não tem poder, e o positivo vaza para o mundo sem especificidade.

## 9. Pergunta 8 — modelo de linguagem, rede e API

[REAL] `Grep -i 'requests|http|openai|anthropic|urllib|socket|subprocess|webbrowser|ftplib|smtplib|aiohttp|httpx|curl|wget'` em `K06\**\*.py`: **nenhuma chamada de rede ou de API**. Único achado: `K06\candidatas\sandbox\run_lean.py` (linhas 5, 33, 38): `subprocess.run` do `lean.exe` local (versão e compilação). Nos `.py` e nas strings de `ENTRADA_PUBLICA\medir_entrada_publica.py` aparecem só os identificadores `10.5281/zenodo.24196546` e `24196546` como texto. Fora de `K06`: `kimi\finalizar_k04_k06.py:76` roda localmente `rotas.py consultar` (só leitura). Não há `.ps1`, `.bat`, `.sh` ou `.js` em `K06`. (Não verifiquei binários nem o conteúdo do kernel Lean.)

## 10. Os achados da K03 sobre desfecho, poder e degrau: respondidos?

| achado de `REVISAO_K03.md` | resposta no R3.2 | estado |
|---|---|---|
| 6.1 o desfecho primário não separa | `V2-RET` virou primário | respondido na FORMA; a substância não: seção 2 |
| 6.2 C1/C4 e os 12 de especificidade passam por construção | C1/C4 viraram canários; `S` virou integridade; ISO e PLA/OUT reorganizados | respondido, com efeito colateral: 5.4 e 5.5 |
| 6.3.1 `C_8` premia texto difícil | `C_8` removido; pareamento por `d1`; três textos por controle | respondido na forma; custo do pareamento assumido (6) |
| 6.3.2 `A8` é satisfeito por um resumidor perfeito | `A8` mantido, combinado com `RETORNO` | `RETORNO` também o é (2.2) |
| 6.3.3 extratores por braço diferentes | equivalência medida em T e C1–C4 legados (`ENTREGA_K06.md:36`) | **não respondido para os braços V2** |
| 6.3.4 teto do extrator (96 leituras) | casos sintéticos 685/685; produção bloqueada | aberto; a conta certa é 168 (8.1 nº 11) |
| 6.4 FALSIFIED alcançável | sim, por focal e direções ISO | alcançável; direção ISO invertida (5.5) |
| 6.5 A1 unidade = texto | três textos por controle, 27 clusters | parcial; cluster sem definição (5.1) |
| 6.5 A2 independência / ICC | cenários ICC; sem `n_eff` | parcial; ICC muda a marginal (4.3) |
| 6.5 A3 `G` indefinido | definido em `MODELO_FORMAL` §2 | respondido; `Q_k` e `P_j` sem conteúdo |
| 6.5 A5 veredito do nulo bem potente | `NONSPECIFIC_POWERED` com TOST | existe; poder 0,02–0,41 |
| 5.2 multiplicidade, permutação, sementes, empates | sinais exatos, empates incluídos, sem semente | respondido; exatidão conferida com 27 clusters |
| 5.3 poder do veredito inteiro (≈ 0,35) | simulado | feito; mas 0,992 = 0,99 assumido, e 0,012/0,022 dominados pela integridade (4.2–4.3) |
| 5.5 5σ lado a lado | 618/655 com `POWERED` 0,599/0,669 | feito; sem `n` que cumpra 0,90 (7) |
| 8.7 retorno como braço decisório | sim | forma sim (2) |
| 8.8 `IALD_COLLAPSE_V2` e rótulos | sim | respondido |
| 8.10 T6 classificado | classificado (não o li) | não conferido por mim |

## 11. Atribuições ao operador (tarefa fixa) [REAL]

Varri `PROTOCOLO_EXPERIMENTAL_R3_K06.md`, `PODER_CONJUNTO_K06.md`, `DEGRAU_5_SIGMA_K06.md`, `ERRATA_R3_1_K06.md`, `ERRATA_R3_2_K06.md`, `ENTREGA_K06.md`, `PERGUNTA_K06.md` e `K06\PODER\*.py|json` por `«`, `»`, «operador», «ratific», «concord», «disse», «pediu». **Não há aspas de fala nem frase do tipo «o operador disse/pediu/ratificou»** nos arquivos de poder e degrau. As ocorrências são alocações de decisão («o degrau pertence ao operador», «revisão distinta e operador») e duas referências à concordância em bloco: `ENTREGA_K06.md:42` («hipótese de trabalho concordada em bloco, não ratificação do protocolo inteiro») e `PERGUNTA_K06.md:13` («A concordância em bloco permite usar o artigo público v411 como hipótese de trabalho»). Fecham por bytes com o arquivo citado no adendo da ordem: `OPERADOR_13nov_excelente_concordo_com_tudo_depois_da_errata_do_meio_e_da_rodada_2_verbatim.txt`, 28 B, sha256 `fa30a621d7d23516891cd98860b4b2a9753a6f813e80c2599492b5090f4d40a6` (conferi por `sha256sum`; conteúdo: «excelente, concordo com tudo»). Esse texto só sustenta «concordância em bloco»; que ele cobrisse a proposta da entrada pública é afirmação da gerência no adendo, não verificável nos bytes. A fala da rodada 2 (`…parece_que_o_kimi_ja_respondeu_tudo…`, 90 B, `88799027…`, citada em `RODADA_2_LEIA_PRIMEIRO.md`, não nos arquivos do K06) também confere em tamanho e hash. **Nenhuma atribuição deixou de fechar.**

## 12. O que pede correção (numerado)

1. **Manchete.** `ENTREGA_K06.md:3`, `PERGUNTA_K06.md:3`, `DEPOSITO_K06.md`, `REV0\PROTOCOLO…:7, 12`: «separa em simulação» deve ser retirado ou reescrito como «o predicado distingue dois vetores escritos à mão»; acrescentar a frase que a pergunta 1 devolve (leitor sem memória: `Q = 1`).
2. **A separação por definição.** `K06\PODER\simular_separacao_r3.py:61–68`: substituir pelos leitores-mecanismo (modelo em `scripts_k06_poder\leitores_sem_atrator.py`) mais os controles de 2.4.
3. **Desfecho.** `MODELO_FORMAL_R3_K06.md:46, 187`; `REV0\PROTOCOLO…:143–154`: perturbação de estado (instrução normal em `k = 9`, histórico visível contrafeito), efeito = mudança nos seis índices, retorno relaxado (não em um único passo), braço de ablação do histórico, braço autônomo; escrever os bytes de `Q_1…Q_12` e de `P_j` no protocolo.
4. **Sentido do teste ISO.** `r32_motor.py:179–183, 369–379`; `REV0\PROTOCOLO…:44, 218`; `PROTOCOLO…R3_K06.md:17–21, 68`: o teste primário tem de estabelecer `Q_ISO ≥ Q_T − δ` (cauda `minus`, que o código já calcula e não usa para ISO, `:180`); `FALSIFIED` deve disparar com o ISO muito PIOR que T; refazer fronteiras e cenários.
5. **Especificidade em `POWERED`.** `r32_motor.py:383, 400`; `PROTOCOLO…R3_K06.md:70`: recolocar `T > PLA/OUT` ou impedir que um estado não resolvido entre em `POWERED` (hoje 0,35–0,37 sob nulo de especificidade).
6. **Cenários de poder.** `r32_motor.py:42–63, 234, 263–283`: ICC/texto com marginais fixas (como nas fronteiras); `systemic_integrity`, `NO_EFFECT` 1 % e corte de 5 % com base ou sensibilidade; dizer em `PODER_CONJUNTO_K06.md:44–58` que `0,992 = 0,99 × ≈1`.
7. **NONSPECIFIC lado a lado.** `PODER_CONJUNTO_K06.md:60–68`, `ENTREGA_K06.md:5`, `PERGUNTA_K06.md:30–31`: separar o `n = 320` com ICC dos 5σ sem ICC; poder do negativo nomeado.
8. **Tamanho.** `gerar_manifestos_r32.py:95, 97`: critério único; IC de Clopper–Pearson no lugar de Wald (`gerar_manifestos_r32.py:50–54`: `0/1000` não é `[0; 0]`); ≥ 5.000 réplicas para o nulo global e as fronteiras; dizer que 0,057 é ruído (seção 5.3) e que o tamanho agrupado é 0,052.
9. **Contexto.** `MODELO_FORMAL_R3_K06.md:46–58`: o artigo em toda mensagem do usuário dá 2,49–3,52 M tokens na leitura 12 e 16–23 M por sessão; escolher: corpus uma vez, ou declarar inviável abaixo de ~3,5 M de janela; recalcular custo em tokens.
10. **Teto do extrator.** `REV0\PROTOCOLO…:174, 280` e `ENTREGA_K06.md:7, 54, 56`: 168 leituras, não 96 (`e < 0,069 %` para 0,89); estender `EXTRATOR_TETO` a `p_RETORNO`.
11. **Degrau.** `DEGRAU_5_SIGMA_K06.md:13–24`, `ENTREGA_K06.md:50`, `PERGUNTA_K06.md:25–33`: dimensionar um `n` de 5σ no desenho R3.2 que alcance 0,90 (ou dizer que não existe com 27 clusters) e recolocar a seção de alternativas de `REV0:78–107`; marcar `verificar_degrau_5sigma.py`/`degrau_5sigma.json` vigentes como legado.
12. **Documento único.** `PROTOCOLO_EXPERIMENTAL_R3_K06.md` (R3.2, 8.975 B) não traz a pergunta, os braços, `G`, o pareamento por `d1`, os observáveis nem a árvore de vereditos: estão em `REV0` (24 KB) e `REV1`, com partes superadas (`REV0 §9–10`: Holm de 24, CP, Wald; R3.2: Holm de 6, t, sinais). Consolidar num texto só, o que se congela por hash.
13. **Cluster.** Definir no protocolo o que são os 27 clusters e como se mapeiam às sessões reais (hoje: blocos consecutivos, 9 por texto).
14. **Custo.** `PROTOCOLO…R3_K06.md:116–129`, `PODER_CONJUNTO_K06.md:81–90`: inteiros com incerteza; declarar `pair_noise` e `technical_loss` como suposições e o 4/3 como fator da quarta família não simulada.
15. **PERGUNTA.** `PERGUNTA_K06.md:13–19, 25–33`: falta a partitura (o que o teste decide, o que não decide, o que o negativo significa) e a decisão de `δ = 0,15`, do corte 0,80 e do limiar 18/24 (hoje escolhas do Kimi, sem derivação e sem lugar para o operador). Uma linha proposta: seção 15.
16. **Lógica por construção.** `PROTOCOLO…R3_K06.md:8, 42`, `PODER_CONJUNTO_K06.md:7`: «passou em todos os cenários» é tautologia do gerador; dizer.
17. (menores) `degrau_5sigma.json`/`.log` e `verificar_degrau_5sigma.py` vigentes são REV0; `PROTOCOLO…:6` lê «todos os números novos vêm de 1.000 corridas» sem a ressalva do CP em 0/1000.

## 13. O que conferi e como

- Leitura integral: ORDEM K06 (A, B, E), ADENDO A, `RODADA_2_LEIA_PRIMEIRO.md`, `REVISAO_K03.md`, `ENTREGA_K06.md`, os cinco documentos pedidos, `MODELO_FORMAL_R3_K06.md`, `REV0\PROTOCOLO…` e `REV0\DEGRAU…`, `PERGUNTA_K06.md`, `DEPOSITO_K06.md`; código: `r32_motor.py`, `simular_r32_sessoes.py`, `validar_r32.py`, `simular_separacao_r3.py` (+ `separacao_r3.json`), `verificar_degrau_5sigma.py`, `gerar_manifestos_r32.py` (trecho), `run_lean.py`; `degrau_5sigma.json`.
- Hashes: `sha256sum` dos sete arquivos do R3.2 contra os declarados (todos iguais); `PRESERVACAO_SHA256.txt` de REV0 (17/17) e REV1 (76/76) por script (`conferir_preservacao.py`); verbatims do operador (seção 11).
- Reprodução do cenário-base (4.1); números do JSON por script (`conferir_resultados_r32.py`, `inspecionar_r32.py`); contas (`contas_k06.py`); leitores (`leitores_sem_atrator.py`).
- Extensões curtas, em cópias do motor e com sementes declaradas antes (20261114–20261118): tamanho (4.000 + 2.000 corridas), sentido do ISO (3 × 300), calibração da cauda (120.000 `p`), FFT × DP com 27 clusters (18 casos). Nenhuma delas alterou um arquivo do Kimi.
- Mapa de Rotas: termos e rota da seção 1.

## 14. O que NÃO conferi

- Os outros 19 cenários por reexecução (só o `BASE`); eles foram conferidos contra o JSON, não recalculados.
- Os extratores (685/685, 0/120), a bateria, `CONTAMINACAO_ISOMORFO_K06.md` e a construção do isomorfo, o registro do `um.py` e a classificação do T6 (não abri `T6_protocol_prompts.txt`), o Lean (`LeitorFinito`, `RC: 0`): fora do escopo desta revisão.
- Que o intervalo t focal e o `p` por sinais tenham a taxa de 2,87×10⁻⁷ na fronteira: não dá para conferir sem ~10⁷ corridas.
- Que o `n` de 5σ que alcança 0,90 no R3.2 exista ou qual seja.
- Os valores de contexto são dos proxies do próprio Kimi (`whitespace_words × 1,30`; `bytes / 4`), não de tokenizer de modelo nenhum.
- Se o conteúdo real de `Q_1…Q_12` e `P_j` muda a pergunta 1: o texto deles não existe; a conclusão vale para o mapa «instrução + artigo → resposta» que o protocolo descreve.

## 15. Partitura ao operador (uma linha, na língua dele; a gerência decide se a leva)

«Como está escrito, este teste decide se o modelo, ao reler o artigo a cada rodada, volta às mesmas 24 respostas uma rodada depois de um empurrão; NÃO decide se isso é “convergir” ou apenas reler o texto e obedecer à instrução de cada rodada (um leitor sem memória passa), nem se o que carrega a volta é a estrutura ou o nome da Teoria (o teste dos isomorfos hoje está de cabeça para baixo), e um positivo dele, `NOT_FALSIFIED_POWERED`, sairia em cerca de um terço das corridas simuladas em que o modelo não distingue o texto da Teoria de nenhum outro.»

— revisor distinto, 14/11/2026. `NOT_FALSIFIED` não é `CONFIRMED`; o gate não se move.
