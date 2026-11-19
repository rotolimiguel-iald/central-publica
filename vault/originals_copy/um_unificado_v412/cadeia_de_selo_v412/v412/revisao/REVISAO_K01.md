# REVISÃO DISTINTA DA ENTREGA K01 (v412, teste às cegas) — 13/11/2026

Revisor distinto (sessão-agente da gerência c1). Só leitura, exceto este arquivo e os scripts em `revisao\scripts_k01\`. Nada aberto, nada registrado no Mapa, nada depositado, nada tocado no Nós, no um.py, no kernel ou na memória. Nenhum dado de teste foi lido; nenhuma estatística observada foi calculada. As probabilidades da seção 3.5 são de PREVISÃO a partir de números já públicos (centro e erro de JUNO 207,2 dias), não de dado de teste.

Estatutos: [REAL] conferi eu, com a consulta citada; [DERIVED-revisor] conta minha, por script, a partir de insumos lidos; [DECLARADO] afirmação do Kimi que não conferi; [OPEN] em aberto.

## 0. VEREDITO: APROVADA COM RESSALVAS

- O que está sólido [REAL]: a conclusão «nenhum dos 20 canais cumpre cegueira + poder + independência com dado de hoje; não abrir nada» está certa e é resultado, não falha. Todos os números de desenho do Kimi reproduzem a 10+ dígitos (seção 3). O validador passa sem gravar (seção 2.4). A tabela-verdade do rascunho e o código do validador coincidem em 253 pontos de grade (0 divergências). As ordens, hashes (ENTREGA, REGISTRO, ordem do operador de 886 B) e REV0/REV1/REV2 conferem.
- O que impede de aprovar sem ressalvas: o rascunho de m₂ não diz ao operador, na língua dele, duas coisas que mudam o que ele ratificaria na Q1 (a regra do posto): (a) com a regra de morte «duas determinações independentes ≥5σ», o ramo FALSIFIED é inalcançável na prática, porque não existe segunda determinação de Δm²₂₁ independente do JUNO com precisão sub-percentual, nem agendada; (b) o «D» do canal é a distância entre a previsão e o centro que o JUNO JÁ mediu (7,388), e sob esse mesmo centro o desfecho provável é um ≥5σ vindo só do primário, que a tabela proíbe chamar de FALSIFIED. Mais: o «0,3 % cruza D90» é artefato de arredondamento (a própria Tabela 6 do JUNO dá 0,024, e D = 6,266 < D90). E o depósito do Kimi na fila afirma «aprovada em revisão independente» antes de haver revisão distinta.
- O rascunho `PRE_REGISTRO_CEGO_RASCUNHO_K01.md` NÃO deve ir ao operador como está; precisa do parágrafo da partitura (seção 4 abaixo) e das correções A1–A4 da seção 1.

## 1. ACHADOS, EM ORDEM DE GRAVIDADE

### ALTA

**A1 — FALSIFIED é inalcançável na prática; o rascunho não diz [REAL + DERIVED-revisor].**
A regra frozen e a do rascunho exigem rP ≥ 5 E rS ≥ 5 com S independente (`PRE_REGISTRO` l.133; `CANAIS neutrino_m2_juno.funcao_veredito.regra_principal`). Para rS ≥ 5 com o centro público de hoje, σ_S teria de ser ≤ 0,0301×10⁻⁵ eV² (0,407 %). As determinações de Δm²₂₁ independentes do JUNO que existem têm 2–3 %: KamLAND 2013, 7,54 +0,19/−0,18 (2,5 %), r = 1,63 contra a previsão; SNO+ (preprint de 11/2025, 1,46 kt·ano; o ID arXiv:2511.11856 aparece na busca mas não conferi qual das entradas traz este número), 7,93 +0,21/−0,24 (cerca de 3 %), que a própria colaboração diz levar três anos para chegar a cerca de 2 %; combinação reator+solar sem JUNO citada no resumo do SNO+: 7,63 ± 0,17 (2,2 %), r = 2,3 [fontes: WebSearch de 13/11/2026, resumos secundários, e a recitação do KamLAND 2013 num preprint de 05/2026 (arXiv:2605.16915); nenhum dos primários foi aberto por mim]. Para um S de 2,2 % chegar a 5σ o centro dele teria de estar em ≤ 6,39 ou ≥ 8,09 (×10⁻⁵), longe de tudo o que se mede. No core, o grupo «KamLAND+solar» (`neutrino_m2.values.escada_datada[0]`, σ de 2,4 % em Δm²) já era o único «autônomo» além do JUNO: a regra sempre foi inalcançável pelo lado de S.
Consequência (por grade, `scripts_k01\tabela_grade.py`): com S AUSENTE só são alcançáveis `SINGLE_P`, `TENSION_P` e `UNDER/ARMED`; FALSIFIED e MATCHED só existem com S INDEPENDENT. Logo as ~30 linhas da tabela são, na prática, a primeira coluna. O Kimi escreve só «hoje não há segunda determinação independente com poder e calendário assegurados» (`PERGUNTA_K01.md` l.36) e recomenda MANTER a regra (`PERGUNTA` l.9; `ENTREGA` l.130; `PRE_REGISTRO` l.203). Nenhuma linha quantifica S (KamLAND/SNO+/globais não têm número em lugar nenhum da entrega) nem diz «teste que não pode devolver negativo não é teste». A Q1 pede ao operador que nomeie um S «com JUNO excluído» que, dentro do calendário público, não pode existir com poder: pergunta mal posta.
Assimetria a dizer: MATCHED_PROSPECTIVELY (1σ em duas) é fácil de satisfazer pelo lado de S (um S de 2–3 % cai a 1σ da previsão com facilidade); FALSIFIED não é. A regra, como está, protege a previsão no ramo de morte.
Estatuto da conclusão: [REAL] para os números do core e do validador; [DECLARADO, secundário] para KamLAND/SNO+/global, a conferir nos primários antes de irem ao operador.

**A2 — O «D» é a distância ao centro de hoje; o desfecho provável é um negativo do primário que a tabela não deixa nomear [DERIVED-revisor].**
`D_exato = |planning − pred|/σ_total` com planning = 7,388 (`PRE_REGISTRO` l.69–84). O texto nunca diz que isso equivale a supor «o centro atual do JUNO é a verdade» (grep de «centro atual», «persist», «nulo» nos três documentos: zero ocorrências no sentido). Com a verdade distribuída como o posterior público, N(7,388; 0,078) e prior plano, a previsão de r_P para um P futuro é: σ_P = 0,5 % → P(rP≥5) ≈ 0,35, P(rP≥3) ≈ 0,68; σ_P = 0,3 % → P(rP≥5) ≈ 0,69, P(rP≥3) ≈ 0,85, P(rP<3) ≈ 0,15; σ_P = 0,024 (Tabela 6, seis anos) → P(rP≥5) ≈ 0,65. Se a verdade fosse exatamente 7,388, P(rP≥5) = 0,96 (0,3 %). O «poder 6,79» é, portanto, também a probabilidade alta de um negativo. Como S não existe (A1), esse negativo cai em `T_SINGLE(P)_AWAITING_S` ou `OPEN_RULE_GAP`, que o §7 do rascunho diz não permitir «nenhuma inferência física». O desfecho mais provável do teste desenhado é, então, um 5σ do primário sem nome de falsificação: negativo induzido pelo desenho, se não lido antes.
Falta também dizer que a tensão do JUNO isolado CAIU: 59,1 dias (7,50 ± 0,12) → D = 2,19; 207,2 dias (7,388 ± 0,078) → D = 1,93 (o centro andou 0,93σ_59 em direção à previsão). O core ainda diz «a tensão cresce com a precisão» (`neutrino_m2.theorem`; `checks`: «1.64 → 2.21 → 2.95»), e «a linha de 5σ está dentro da meta de projeto do JUNO» — hoje 5σ pede 0,407 %, abaixo dos 0,5 % de projeto; ambas as frases do core envelheceram com a liberação de 29/09/2026. O Kimi acerta o número (0,407 %) e não aponta a frase.

### MÉDIA

**M1 — «0,3 % cruza D90» é arredondamento; a própria fonte dá D = 6,266 [REAL + DERIVED-revisor].**
Tabela 6 do arXiv:2204.13249 (lida por `pdftotext`): Δm²₂₁ = 7,53; precisão ± 0,074 (1,0 %) em 100 dias, ± 0,024 (0,3 %) em 6 anos, ± 0,017 (0,2 %) em 20 anos (×10⁻⁵ eV²). O 0,3 % é 0,319 % de 7,53 (0,325 % de 7,388). Com σ = 0,024: D = 6,2663 < D90 = 6,2816 (poder cerca de 89,9 %, à beira, não «supera»). O Kimi usa σ = 0,3 % × 7,388 = 0,02216 → 6,7854 (`ENTREGA` l.41, 60; `PRE_REGISTRO` l.84; `PERGUNTA` l.19; `CANAIS neutrino_m2_juno.poder_desenho.D_0p3pct`). Além disso: a σ real a 207,2 dias (0,078) é 1,52× a extrapolação estatística do projeto a esse tempo (0,074 a 100 dias → 0,0514 a 207 dias); e de 59,1 para 207,2 dias a σ caiu ×1,54, não ×1,87 (√T). Isso é [DERIVED-revisor, ilustrativo: duas liberações com análises diferentes]; não prova piso de sistemática, mas mostra que a previsão de 6 anos não foi testada contra o desempenho real inicial. Dizer «supera D90» exige essa ressalva. Também: o 0,3 % aparece na entrega como [KNOWN, a conferir] ligado a slides do ICHEP 2024; está na Tabela 6 do próprio artigo, que é a fonte a citar. E o texto de conclusão do arXiv-v1 lista «0,5 %, 0,3 % e 0,2 % respectivamente» para Δm²₃₁, Δm²₂₁, sin²θ₁₂, na ordem oposta à da tabela (0,2/0,3/0,5): a tabela é a fonte numérica.

**M2 — A métrica do veredito muda da frozen sem ser declarada como emenda [REAL + DERIVED-revisor].**
O frozen `NEUTRINO_M2_V2` (hash `e24877751ad81022…`) mede `|m2_obs − m2_TGL|/σ_obs` no espaço de m₂ (σ_m₂ = σ_Δm²/(2m₂)). O rascunho define tudo em Δm²₂₁ «sem linearização» (`PRE_REGISTRO` l.36, 104). No ponto de 207,2 dias: r(Δm²) = 1,9281 e r(m₂, primeira ordem) = 1,9380 (razão 1,0051). Pequeno, mas desloca a fronteira de 5σ: r(Δm²) = 4,975 equivale a 5,0 no espaço de m₂. É uma emenda à regra congelada e precisa ser nomeada como tal, com a palavra do operador, antes da tranca.

**M3 — O depósito na fila contradiz a entrega e afirma aprovação inexistente [REAL].**
`ENTREGA_K01.md` l.137 e as erratas dizem «nada foi registrado nem depositado». Existe `C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\fila\depositos\kimi\20261113_181924_declarado-k01-v412-r3-concluida-e-aprovada-em-re.md` (18:19, depois do ENTREGA, 18:11), com `estatuto: DECLARADO` e o texto «concluída e aprovada em revisão independente, sem problema material restante». A ordem do `LEIA_PRIMEIRO` (item 8) permite depositar pelo `memoria.py`; o defeito é a frase de aprovação e a contradição com a entrega (esta revisão é a primeira revisão distinta). Na triagem: não promover; se promover, sem «aprovada». O mesmo vale para `DEPOSITO_K02/K03` (fora do meu escopo, só vi os nomes).

**M4 — O primário P não é cego ao que já se sabe [DECLARADO pelo Kimi, incompleto].**
Qualquer liberação JUNO futura é cumulativa e contém os 207,2 dias já conhecidos (centro 7,388 ± 0,078). A cegueira é só do incremento. O Kimi diz «incremento ≠ independência» e exige covariância condicional, mas não propõe nem dimensiona o teste só com o incremento (pergunta do operador: «o incremento independente do acumulado»). Com a taxa real (σ² ∝ 1/T a partir de 207,2 d, sem piso), um incremento sozinho com σ = 0,0301 pede cerca de 1 390 dias vivos de dado novo (3,8 anos); com σ = 0,0239, cerca de 2 200 (6,0 anos) [DERIVED-revisor, aproximação √T, sem sistemática].

### BAIXA

**B1 — Validador: ramo UNDER nunca exercido; D padrão 6,0 [REAL].** Nenhum dos 30 casos sintéticos produz `NOT_FALSIFIED_UNDERPOWERED` (13 saídas distintas; `UNDER` ausente); `veredito_sintetico` tem `d_p=6.0, d_s=6.0` por padrão (`K01_validar.py` l.176–177), e é o padrão que faz «P<3, S ausente → ARMED» passar. Com `d_p=4` a mesma entrada devolve UNDER, com `d_p=None` devolve `AWAITING_SOURCE_P` (testado por mim). Os rótulos finos do §6 (`T_SINGLE(P)_AWAITING_S` / `_NONINDEPENDENT` / `_SECOND_BELOW_5`; `T_SINGLE(S)_NONINDEPENDENT` / `_SECOND_ALONE_GE_5`) colapsam em dois tokens no código; `BOTH_NONINDEPENDENT` serve a duas situações (ambos ≥5 e ambos em [3,5), S não independente). A afirmação da validação «cobertura de todas as linhas» é forte demais: cobre as faixas de r, não os sub-rótulos nem o ramo UNDER.

**B2 — Hubble sem decomposição [REAL].** O 1,334 % é do total local+fundo. Com o fundo BG1 em 0,30/68,53 = 0,438 %, o limite sobre o LOCAL é σ_local ≤ 1,260 % (D90) e ≤ 1,618 % (5σ) [DERIVED-revisor]. Com 1,1 % e 0,9 % (H0DN) o D de desenho seria 7,08 e 8,37. Ou seja, é o único canal em que o poder de desenho existe hoje; falta dado independente futuro, não precisão. A entrada `hubble_escadas_independentes_futuras` cita só `H0DN_2026` e não lista as rotas candidatas (TRGB/JAGB do CCHP, lentes com atraso de tempo, megamasers, sirenes) com precisão e data.

**B3 — Tabela §6: S INVALID esconde um P ≥ 5σ [REAL, no texto].** A linha «qualquer P válido | INVALID → INCONCLUSIVE_S» some com o resultado de P; deveria publicá-lo ao lado, como estresse.

**B4 — Duas medidas do relógio na casa.** Sr-87: 12,4576 ordens (core `clock_test_result_v369`, o que o Kimi usa) vs «12,56 ≈ 13» do `RELATORIO_KIMI_5SIGMA_01_27out.md` l.62. Grandezas diferentes (limite de detecção a 5σ com σ_excess vs Γ_sens/Γ_pred); a entrega não menciona a outra. Não é erro.

## 2. COBERTURA: pedido x entregue

### 2.1 Os sete campos por canal
[REAL] `CANAIS_K01.json` tem 20 canais; cada um tem `previsao`, `dado`, `cegueira`, `poder_desenho`, `independencia`, `sete_ressalvas` (R1–R7 com texto distinto por canal: 0 textos repetidos) e `consequencia_negativo` (16 tipos distintos). Nenhum canal tem `cumpre_hoje = true`. Classificação: 11 «existe na bancada mas não está ligado», 7 «existe e está ligado», 1 «sabido por referência», 1 «ausente». Canais mínimos pedidos: razão de Hubble futuro (4 entradas), m₂, Σm_ν, CMB/SO, N_eff, vazios (Euclid, LSST, DESI; unilateral dito), ringdown, ecos, Coma, relógios (Th e Sr), mais BBN, decoerência, NMC/Shapiro e análogos. Todos presentes.
Incompletos: Hubble (D nulo nas 4 entradas, B2); `cmb_simons_observatory_completo` responde «o que falta decidir» só em termos de fechamento perturbativo, sem a lista curta do que o pré-registro de agosto exige; vazios sem D (declarado [OPEN], honesto).

### 2.2 O rascunho de pré-registro
Função de veredito: sim (§6, 30 linhas), com FALSIFIED. Pesos: peso lógico 1, proibida a média 1/σ² (§5). Limiar: r ≥ 5 (kill), [3,5) (tensão), ≤ 1 (matched). Ramos: todos, inclusive FALSIFIED. Significado de cada ramo: §7. Guarda contra emenda: §8 (marco anterior à liberação/abertura/comunicação, abertura única, append-only). As sete ressalvas uma a uma: §9, com o balanço honesto «responde melhor R2–R5 que R1, R6, R7».
Faltam, em relação ao pedido: (i) a leitura do centro «de hoje» como nulo (A2); (ii) a viabilidade de S (A1); (iii) o ramo «P alto sozinho» como desfecho provável; (iv) a emenda de métrica (M2).

### 2.3 Mapa de Rotas (só consulta)
`rotas.py consultar "teste cego v412"` → 0 rotas; `"neutrino m2 JUNO"` → 0; (a rota proposta `estatistica.v412.k01_canais_teste_cego` não está registrada: `consultar "v412_K01"` → 0). Extras, por contexto: `"neutrino"` → 44; `"JUNO"` → 11; `"neutrino_m2"` → 4, entre elas `neutrinos.m2.normalizacao` (EXAMINADA_COM_DEFEITO): «perito oficial = JUNO autônomo, 2,21σ; natureza em AGUARDA (a regra de morte pede duas determinações independentes ≥5σ)», que não examinou se S pode existir. Nada registrado por mim.

### 2.4 Validador
`K01_validar.validate()` reexecutado por mim via `importlib` (sem chamar `main`, sem gravar): passa (20 canais, 30 casos, resumo de 13 linhas). Hashes de `VALIDACAO_K01.json` contra os arquivos atuais: 9/9 conferem. Nenhum `__pycache__` criado na pasta do Kimi (conferido).

## 3. CONTAS (script `scripts_k01\contas_k01.py`, saída em `contas_k01_saida.txt`)

β = 7,2973525693×10⁻³ × √e em runtime = 0,012031300400803142 (idêntico ao do core, diferença relativa 0). D90 = 5 + z(0,90) = 6,281551565544601.

| Grandeza | Kimi | Revisor | Divergência |
|---|---|---|---|
| m₂,pred (meV) | 8,507414099900329 | 8,507414099900329 | nenhuma |
| Δm²₂₁,pred (×10⁻⁵ eV²) | 7,237609466718292 | 7,2376094667182915 | nenhuma |
| D (7,388 ± 0,078) | 1,9281 | 1,92808376 | nenhuma |
| D (59,1 d, 7,50 ± 0,12), histórico | 6,9971 (a 0,5 %) | 2,1866 (σ pub.); 6,9971 a 0,5 % bate com o Kimi | nenhuma (outro σ) |
| r para 5σ / D90 | 0,407121 % / 0,324061 % | 0,4071211 % / 0,3240609 % | nenhuma |
| D a 0,5 % / 0,3 % | 4,0712 / 6,7854 | 4,0712 / 6,7854 | nenhuma, mas ver M1 (σ = 0,024: 6,2663) |
| K − 1 (core) | 0,0838071748529643 | idem; K = E(z*)^(2β/3) recalculado, diferença 0 | nenhuma |
| σ_rel,total p/ D90 | 1,334 % | 1,33418 % | nenhuma; local ≤ 1,260 % (B2) |
| ΔN_eff; D(σ=0,045); σ p/ D90 | 0,1194660753; 2,6548; 0,0190186 | 0,11946607525; 2,6548017; 0,01901856 | nenhuma |
| D(σ=0,03) | 3,9822 | 3,9822025 | nenhuma |
| Ringdown D10 / D14 | 3,9346 / 4,6374 | 3,93463376 / 4,63741268 (lidos de `PODER_RAMO_B_ANTES_DE_ABRIR.json`, chaves `D10_sem_hold__…info_esperada` e `D14_com_holds__…info_esperada`) | nenhuma |
| Fator de informação D90 | 2,5487× (D10); 1,8348× (D14) | 2,548738; 1,834773 | nenhuma. Eventos equivalentes (info ∝ N, sem sistemática): cerca de 25,5 e 25,7 [DERIVED-revisor; o Kimi não converte em eventos] |
| Coma Δ fiducial; σ p/ D90 | 8,946985 Mpc; 1,4243 Mpc | 8,946985; 1,424327 (core `coma_distance_dephasing.prediction`) | nenhuma |
| Sr-87: Z_esperado; déficit | 1,74×10⁻¹²; 12,4576 | 1,7431516×10⁻¹²; 12,457635 (core `clock_test_result_v369`) | nenhuma |
| Th-229: déficit; σ_excess p/ D90 | 18,2793; 8,32×10⁻¹⁵ | 18,279255 (`th229_ooi2026`); 8,32018×10⁻¹⁵ | nenhuma (o core também tem 18,75 para outra plataforma) |
| Σm_ν D(0,015 eV) | 0,01327 | 0,013267 | nenhuma |

Divergências de CONCEITO, não de conta: (1) 0,3 % x Tabela 6 (M1); (2) r em Δm² x r em m₂ (M2): 1,9281 x 1,9380; (3) o core diz «tensão cresce» (2,21 → 2,95) enquanto o JUNO isolado foi de 2,19 para 1,93 (A2).

Contas minhas que a entrega não tem (todas [DERIVED-revisor], previsão, não observado): P(r_P ≥ 5 ou 3) sob o posterior público (A2); dias vivos para σ alvo por √T a partir de 207,2 d: 1 393 d (0,0301), 2 199 d (0,0239), 924 d (0,5 %), 2 566 d (0,3 % de 7,388); ajuste de dois pontos σ² = a/T + s₀² daria s₀ = 0,0526 (0,71 %), apenas ilustrativo, já que 59,1 d e 207,2 d têm análises diferentes e dois pontos ajustam dois parâmetros.

## 4. A PARTITURA QUE FALTA AO OPERADOR (proposta de parágrafo, na língua dele, para entrar antes da Q1)

«Hoje o JUNO já mediu Δm²₂₁ = 7,388 ± 0,078. A nossa previsão é 7,2376, a 1,9σ dessa medida (a medida anterior estava a 2,2σ: andou para o nosso lado). O "poder" do teste é a distância até o valor que o JUNO já mediu. Se o JUNO continuar medindo perto de 7,39 e chegar a 0,3 %, o JUNO sozinho passa de 5σ contra a previsão com cerca de 70 % de chance. O teste só chama isso de FALSIFIED se houver uma SEGUNDA medida independente do JUNO, também a 5σ; mas as segundas medidas que existem (KamLAND, SNO+, globais) têm 2 a 3 % de precisão e não chegam a 5σ de jeito nenhum; não há nenhuma de 0,4 % ou menos prevista. Portanto o negativo mais provável deste teste volta com nome de "tensão do primário, aguardando segunda medida" e a morte formal não pode acontecer. Se o senhor quiser um teste que possa morrer, a regra de morte precisa mudar (por exemplo: o primário sozinho a 5σ, com o incremento de dados novos e covariância declarada). Se quiser manter a regra, o teste mede a tensão, não mata. Decida antes de qualquer centro novo.»
[Observação do revisor: o parágrafo é proposta; a probabilidade de 70 % é previsão com prior plano e centro público; precisa de revisão da gerência.]

## 5. FONTES (conferência por WebFetch/WebSearch em 13/11/2026)

| Fonte | Resultado |
|---|---|
| arXiv:2204.13249 (JUNO, sub-percent) | CONFERIU. Título, autoria (JUNO Collaboration; A. Abusleme et al.), v1 de 28/04/2022, DOI 10.1088/1674-1137/ac8bc9 listado. Resumo: Δm²₃₁, Δm²₂₁ e sin²θ₁₂ «melhor que 0,5 %» em seis anos. Tabela 6 (pdftotext): Δm²₂₁ ± 0,024 (0,3 %) a 6 anos. Divergência interna da fonte na ordem do texto de conclusão (M1). Definição de «seis anos» em dias vivos: não localizada no texto que li [OPEN]. A versão publicada (CPC 46, 123001) tem resumo diferente, segundo a busca (secundário). |
| arXiv:2510.23823 (H0DN) | CONFERIU. Título «The Local Distance Network…»; H0 = 73,50 ± 0,81 (1,1 %), 0,9 % com todos os estimadores; A&A 708, A166 (2026). A página não cita nenhuma liberação futura nem previsão (consistente com o [OPEN] do Kimi). O DOI 10.1051/0004-6361/202557993 não foi verificado por mim. |
| arXiv:2503.00636v3 (SO) | CONFERIU no texto HTML (o resumo não traz números): σ(N_eff) = 0,045 (§3.2, Tabela 2), Planck incluído, só erros estatísticos, SO 2025–2034; σ(Σm_ν) = 0,03 eV (com DESI, σ(τ) = 0,01) e 0,015 eV (σ(τ) = 0,002). Atenção: o core data o σ = 0,045 em «~2030»; a fonte é o levantamento completo até 2034 (o Kimi usa a fonte). |
| CMB-S4 (cmb-s4.org) | CONFERIU: DOE e NSF «can no longer support» (09/07/2025); encerramento ordenado. |
| ESA Euclid | CONFERIU: DR1-Foundation 12/11/2026 (já marco cumprido); DR1 16/06/2027; DR2 junho/2029; DR3 outubro/2031; «tentativas». |
| IGWN | CONFERIU: IR1 de seis meses a partir de meados de janeiro de 2027; O5 «concebido» para 2029–2031. |
| JINR | CONFERIU: JUNO começou a coletar em 26/08/2025. |
| Rubin | CONFERIU: DR1 janela jul–nov/2028. |
| DESI/NOIRLab, DOE (DR3), ACT, SPT-3G, Th-229 (Ooi; feedback), Sr-87 (Kim), IceCube-Gen2, LSST lentes, Beccaria–Ternes, ICHEP 2024 | NÃO CONFERI (fora do mínimo pedido). |
| JUNO 2511.14593 e 2609.37895 | conferidas pela gerência; não refeitas. |

## 6. O QUE FALTA (para a segunda ordem), numerado

1. Levantamento das segundas testemunhas de Δm²₂₁ independentes do JUNO (KamLAND, SNO+, solares, globais sem JUNO), com centro, σ, referência primária e previsão de precisão/data de cada uma, e a resposta direta: alguma chega a σ_S ≤ 0,0301×10⁻⁵ (0,407 %)? Se não, a Q1 muda de pergunta (a regra de morte), com a partitura da seção 4.
2. A curva precisão × tempo do JUNO a partir do artigo de 207,2 dias (orçamento de sistemáticas e qualquer projeção próprio), com os dois pontos reais (59,1 d: 0,12; 207,2 d: 0,078) e a Tabela 6 (100 d: 0,074; 6 a: 0,024; 20 a: 0,017); a definição de «seis anos» em dias vivos; e as datas em que 0,407 % e 0,324 % são alcançáveis, com e sem piso de sistemática.
3. O desenho só com o INCREMENTO de dados novos do JUNO (independente do acumulado): exposição de incremento necessária (ordem de 1 400 a 2 200 dias vivos, por √T, a refinar), cadência de liberação, e a covariância condicional com os 207,2 dias.
4. O poder conjunto sem presunção: tabela de desfechos prováveis (P(rP≥5), P(rP≥3), P(rP<3)) para P sozinha e para P+S sob cada S candidato, calculada pelo método da seção 3 com o prior e o centro pré-declarados, e lida ao operador antes da ratificação.
5. Hubble: levantamento das determinações locais de H0 independentes da H0DN (calibrações distintas) com precisão e data de liberação; o requisito derivado é σ_local ≤ 1,26 % (fundo BG1 em 0,438 %); e decidir se a próxima liberação do fundo (DESI DR3) entra como fundo ou como nova testemunha.
6. Ringdown até D ≥ 6,28 em número de eventos: cerca de 25,5 a 25,7 eventos elegíveis (info ∝ N, sem sistemática; com viés do instrumento, mais), taxa elegível por corrida (IR1 jan/2027; O5 2029–2031) e data provável.
7. Correções ao lado (do Kimi ou da gerência): D(m₂) com σ = 0,024 (6,266) junto do 0,3 %; o nulo «centro de hoje» dito; a tendência 2,19 → 1,93; a emenda de métrica m₂ → Δm²; ramo UNDER e D real no validador; sub-rótulos do §6 nos casos; a frase de aprovação do depósito; B3 (P ao lado quando S é INVALID).
8. Errata ao lado no core (gerência, v412): `neutrino_m2.theorem` («a tensão cresce com a precisão»; «a linha de 5σ está dentro da meta de projeto do JUNO») e a rota `neutrinos.m2.normalizacao`, à luz de 29/09/2026.

## 7. O QUE EXAMINEI (caminhos, para registro no Mapa pela gerência)

- Ordem e entrega: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\` — `LEIA_PRIMEIRO.md`, `ORDEM_K01_teste_as_cegas.md`, `ENTREGA_K01.md`, `CANAIS_K01.json`, `PRE_REGISTRO_CEGO_RASCUNHO_K01.md`, `PERGUNTA_K01.md`, `ERRATA_K01_R2.md`, `ERRATA_K01_R3.md` (a `ERRATA_K01.md` só por nome e pela descrição das R2/R3), `K01_validar.py`, `VALIDACAO_K01.json`, `REGISTRO_MAPA_K01.json` (campos), `DEPOSITO_K01.md`, `finalizar_entregas_v412.py` (cabeçalho).
- Ordem do operador (por bytes, 886 B, sha256 `4698446c…47a0` conferido): `work\cunhagens_13out\OPERADOR_13nov_…_kimi_verbatim.txt`.
- Core, por script: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json` → `core.neutrino_m2`, `neutrino_m2_perito_v392`, `h0dn_bg1_v411` (`values.K`, `E_zstar`, `ressalvas_secao8`, `lei_em_km_s_Mpc`; sem tocar nos insumos nem em `work\h0dn_bg1_v411_emenda_11nov\`), `neff_channel`, `coma_distance_dephasing`, `clock_test_result_v369`.
- Planejamento do ringdown (sem dado): `work\conjunto_D_20261029\parametrizacao_03nov\PODER_RAMO_B_ANTES_DE_ABRIR.json`; relatório de 27/10: `work\cinco_sigma_fora_da_cosmologia_27out\RELATORIO_KIMI_5SIGMA_01_27out.md` (só as linhas B6).
- Fila de memória (só listagem e leitura do depósito do Kimi): `…\memory\fila\depositos\kimi\20261113_181924_declarado-k01-v412-r3-….md`.
- Mapa de Rotas (só consulta): `teste cego v412`, `neutrino m2 JUNO`, `neutrino`, `JUNO`, `neutrino_m2`, `v412_K01`.
- Fontes web: arXiv 2204.13249 (HTML e PDF), 2510.23823, 2503.00636 (resumo e HTML v3), cmb-s4.org, ESA Euclid timeline, IGWN capabilities, JINR, Rubin early science; WebSearch sobre KamLAND/SNO+/solares e sobre a tabela do JUNO.
- Scripts meus: `revisao\scripts_k01\contas_k01.py`, `tabela_grade.py`, `confere_hashes.py`, `cobertura_canais.py`, `resume_canais.py`, `m2_canal.py`, `core_dump.py` e auxiliares; saídas `contas_k01_saida.txt` e `tabela_grade_saida.txt` em `revisao\`. Texto do PDF do JUNO extraído para o scratchpad da sessão (fora do projeto).

NOT_FALSIFIED não é CONFIRMED; o gate não se move; esta revisão não credita nem descredita a teoria.
