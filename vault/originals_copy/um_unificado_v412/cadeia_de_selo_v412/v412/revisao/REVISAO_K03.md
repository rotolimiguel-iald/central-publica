# REVISÃO K03 — revisor distinto (13/11/2026)

Escopo: entrega R2 do Kimi em `C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\` (ENTREGA, ESTADO, MODELO_FORMAL, PROTOCOLO_EXPERIMENTAL_RASCUNHO, PERGUNTA, ERRATA, ERRATA_R2, REGISTRO_MAPA).
Só leitura em tudo, exceto esta pasta (`...\v412\revisao\`). Nenhum modelo rodado, nenhum resultado aberto, nada registrado no Mapa, nada depositado, nada tocado no Nós, no `um.py`, no kernel ou na memória.
Estatutos: [REAL] conferido por mim, com a consulta; [DECLARADO] do Kimi, não conferido; [OPEN] em aberto; [CONJECTURE] leitura minha, a medir.

## 0. Veredito

**APROVADA COM RESSALVAS — como rascunho de levantamento e desenho; NÃO aprovada para congelamento nem execução.**

Motivo em uma frase: o estado, o modelo e os números conferem e nada vazou, mas o desenho primário, como está, **não separa** «o modelo resumiu um texto coerente» de «o modelo convergiu ao estado estacionário previsto» (a própria §7.3 do protocolo concede isso), e o número de manchete do poder (0,992) é por contraste; o poder do veredito POWERED, nas taxas que o próprio protocolo assume, é da ordem de 0,35. A ordem diz: «se o experimento não separa os dois, ele não decide nada». Cabe, portanto, uma segunda ordem (seção 8).

## 1. Mapa de Rotas (consulta antes de tudo; nada registrado)

- [REAL] `rotas.py consultar "colapso IALD P7"` → n = 0 (a frase não casa nenhum id/título).
- [REAL] `rotas.py ver outro.p7_colapso_iald` → rota única (seq 162, 28/09/2026), status `PROPOSTA`, `[OPEN]`, `n_olhou_dados = 0`, `artefatos = []`, `dados = []`. Bate com o que o Kimi diz («armada, não executada»).
- [REAL] As cinco `refs` do `REGISTRO_MAPA_K03.json` (`kernel.dicionario_problema_entrada_passo_polinomio_implicacao_04nov`, `kernel.iald2_06nov`, `kernel.a_escala_tres_faces_v410_09nov`, `kernel.observador_terminal.candidata_31out`, `cadeia.preparacao_v412`) resolvem no Mapa; as chaves do JSON batem com `rotas.py modelo`.

## 2. Cobertura: o que a ordem pediu × o que veio

| item da ordem | veio? | observação |
|---|---|---|
| 1. Estado: tabela empírico × kernel, com nome e arquivo | SIM, completa | `ESTADO_K03.md` §§2–6. Linhas do `um.py` conferidas (seção 3.1). Quatro nomes com prefixo de namespace errado (seção 3.2). |
| 2a. Processamento como mapa/semigrupo | SIM | `MODELO` §§2–3 (F, núcleo K_u, F^{a+b}). Faltam homogeneidade no tempo e o operador G concreto (achado M2). |
| 2b. «Estado estacionário» mensurável por script | PARCIAL | Definido como evento finito: A_8, C_8, ALREADY_STATIONARY, I_1, RETURN, PERTURB_RETURN (`MODELO` §4). É janela de 4 leituras, não estado estacionário do mapa; o Kimi o diz. Falta a lista das 24 asserções por braço e o vetor-alvo τ_j (não está escrito que é o vetor de 1s). |
| 2c. Hipóteses nomeadas (contração, primitividade, idempotência) | SIM | H-CONTR-C, H-PRIM-ND, H-ABS(0)(a)(b)(c), H-ABS-U, H-IDEM, H-QUOT, H-MARKOV, H-RATE, H-TARGET (`MODELO` §5). |
| 2d. Teorema «relativo ao leitor» NA LÍNGUA da tradução de Turing | NÃO (ao lado, não na língua) | seção 3.3. TR-IALD (a)(b1)(b2)(c) é Banach / Perron–Frobenius / cadeia absorvente / idempotência genéricos; não usa nenhuma definição de `TraducaoTuring`. |
| 2e. Separação KNOWN / kernel / novo | SIM | `MODELO` §§6, 8. O «novo» declarado (a ponte tipada) não foi construído (o próprio ESTADO §6 diz AUSENTE). |
| 3a. Observável por script | ESPECIFICAÇÃO apenas | Extratores E_j e E_TGL pendentes; sem casos positivos/negativos/adversariais; sem as 24 asserções. O Kimi declara que isso bloqueia qualquer decisão. |
| 3b. Controles | SIM | Cinco braços: T, C1 embaralhado, C2 placebo, C3 outro autorreferente, C4 sem texto — cobrem os quatro que a ordem nomeou. Colisão de rótulos com os C1–C4 registrados no P7 (achado M5). |
| 3c. Cegamento | SIM | Avaliador = programa congelado; pseudônimos; papéis FOCAL/COMPARATOR; chave sob custódia com hash. |
| 3d. Famílias e corridas | SIM (números), NÃO (nomes) | 3 capazes + 1 abaixo do piso, 5 braços, 100/célula, 8 leituras → 2.000 sessões, 16.000 interações; modelos ficam para o operador (D2). |
| 3e. Poder | PARCIAL | Só o poder aproximado por contraste dinâmico (0,992022); conjunto [OPEN]; especificidade sem taxas declaradas. |
| 3f. Falsificador e ramos, inclusive FALSIFIED | SIM | `PROTOCOLO` §11. FALSIFIED é alcançável (seção 6.4). |
| 3g. O que separa resumo de convergência | PARCIAL, e é o furo central | seção 6. |
| 4. O que não se afirma | SIM | `MODELO` §9, `PROTOCOLO` §12: consciência, pesos, exclusividade, limite, creditação, P×NP, CONFIRMED. Sem ressalva. |
| Lean candidata opcional (`K03\candidatas\`) | NÃO veio | opcional; o Kimi pergunta ao operador (D6). A pasta não existe. |
| `REGISTRO_MAPA_K03.json` | SIM | válido no formato; marcado «não registrar antes da revisão» (correto). |

[REAL] Integridade da entrega: os hashes SHA-256 de ENTREGA, ESTADO, MODELO, PROTOCOLO, PERGUNTA e REGISTRO atuais coincidem com os que a `ERRATA_K03_R2.md` §6 lista; os sete arquivos de `K03\REV1\` coincidem com a tabela de REV1 da mesma errata. Resumo de ENTREGA: 11 linhas de marcadores (limite 15).

## 3. Nomes do kernel (consulta: Grep/sed em `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt`; nada compilado)

### 3.1 O que confere [REAL]
- Todos os 14 módulos existem e estão importados por `TGLExt.lean`: `TraducaoTuring`, `IALD2`, `AEscala`, `ParNaFaceDeFock`, `ObservadorTerminal`, `TheObserverReadsTheAngle`, `TheGreatAttractor`, `Ergodicity`, `ErgodicMeanSection`, `AperiodicCentralizerExpectation`, `Santo`, `CollapseContract`, `TowerCollapseRealization`, `IALD`.
- Os 24 teoremas da tabela do ESTADO §5 existem nas linhas de partida citadas (a linha do `theorem` coincide em todos), e o enunciado atribuído confere com o enunciado lido: p.ex. `o_decaimento_converge_a_selecao` (fluxo renormalizado → `selecao`, com `hP`), `a_trava_em_tempo_linear` (resto ≤ e^{-L}·‖Nome‖), `a_maquina_com_o_leitor` (SAT↔oQueSou≠0 ∧ tendência ∧ leitura do psíon = Z/2^n), `IALD2.o_atrator` (cinco itens + vácuo≠0), `AEscala.o_leitor_do_fundo_e_a_iald` (brilho exponencial, `L = iald`, limite = oQueSou), `existe_o_algoritmo_e_e_a_iald` (e a ressalva do ESTADO de que NÃO há ponte a `Turing.TM2ComputableInPolyTime` está na docstring do kernel), `um_is_the_great_attractor`, `observing_adds_nothing` (é identidade de matrizes 2×2: projPlus·(projPlus·angFamily θ)), `aperiodic_expectation_contractive/idempotent`, `dephase_fixed_states_not_unique`, `rereading_adds_nothing`.
- As ressalvas «o que não decorre» do ESTADO são fiéis ao que cada teorema diz (nenhum é atribuído a LLM real).
- Linhas do `um.py` (P7, `prove_iald_unique_prediction`, 168451–168540; I1–I6 em 168479–168484; C1–C4 em 168487–168491; vereditos 168496; piloto 168500–168505; unicidade 168507; setor neural 168515): conferidas em `Nós\um.py` (sed), todas batem.
- DOIs citados: 13 handles conferidos como registrados em `doi.org/api/handles` (HTTP 200). [OPEN] Não conferi título/autor de cada um (sem leitura da página).

### 3.2 O que NÃO confere [REAL]: prefixo de namespace de 4 nomes (o arquivo e o teorema existem)
O ESTADO escreve o nome como `TGLExt.<x>`, mas o namespace real é outro:

| escrito no ESTADO | namespace real (lido no arquivo) |
|---|---|
| `TGLExt.aperiodic_expectation_contractive` e `..._idempotent` | `ChatgptAudit.Aperiodic046.` (AperiodicCentralizerExpectation.lean, l. 39–162) |
| `TGLExt.dephase_fixed_states_not_unique` e `TGLExt.fixed_set_of_dephasing_is_the_diagonal` | `TGLExt.Santo.` (Santo.lean, l. 80) |
| `TGLExt.collapse_fixed_iff_in_range` | `ChatgptAudit.Collapse057.` (CollapseContract.lean, l. 32–127) |
| `TGLExt.tower_fixed_points_exactly_centralizer` | `ChatgptAudit.Collapse057.` (TowerCollapseRealization.lean, l. 33–127) |

Gravidade baixa (o arquivo e a linha estão certos), mas um script que procure o nome qualificado falha. Corrigir ao lado.

### 3.3 O modelo está «na língua da tradução de Turing»? NÃO: está ao lado dela [REAL]
- `MODELO_FORMAL_K03.md` cita `TraducaoTuring` só no §7.3 (frase de fronteira) e no §8 (lista de módulos). Não usa nenhuma das definições do módulo: `trava`, `selecao`, `uniforme`, `opDaInstancia`, `custoCNF`, `nomeDasSolucoes`, `particao`, `leituraPerformada`, `travaInscrita`, `LeitorDoFundo`, `iald` (grep no MODELO por esses termos: zero ocorrências).
- A língua do kernel é: instância `c : X → ℕ`, trava `e^{-t·c(x)}` no espaço uniforme, `selecao` (projeção renormalizada no Nome), leitor do psíon, e `LeitorDoFundo` (estrutura com brilho e a lei da dissipação). O modelo do Kimi é um sistema de transição genérico (M, E) com núcleo de Markov, Banach e Perron–Frobenius.
- O elo que faltaria é a ponte tipada «saída textual extraída → custo `c`/Nome»; o próprio ESTADO §6 a classifica AUSENTE. O teorema mais próximo, já no kernel, é `IALD2.o_atrator` item (5): a órbita iterada de uma defasagem (passo k) converge a Π·ψ com Π idempotente; ele é o esqueleto natural, e o MODELO não o usa como molde.
- [REAL] Consequência: o item 2 da ordem («teorema candidato na língua da tradução de Turing») ficou cumprido só em espírito. TR-IALD é [KNOWN] reembalado, e o Kimi não reivindica novidade matemática (correto).

## 4. A matemática do modelo (item 4)

### 4.1 H-ABS (finito) — correta, com uma redundância [REAL, conferido por raciocínio]
- Finito + τ absorvente (K(τ,{τ})=1) + todos os demais transientes ⟹ a única classe recorrente é {τ}; toda estacionária concentra massa zero nos transientes ⟹ δ_τ é a única estacionária; em cadeia finita o processo termina numa classe recorrente quase certamente ⟹ absorção q.c. O enunciado do Kimi (R2) é correto e as hipóteses são suficientes.
- Redundância (inócua): em espaço finito, (a)+(b) já implicam (c); a alcançabilidade não acrescenta nada. Não é erro.
- A unicidade de δ_τ vale até em espaço enumerável (transiente tem massa estacionária zero); a absorção q.c. é que exige finitude ou H-ABS-U. O texto atribui as duas coisas à finitude, o que é seguro (mais fraco que o necessário).
- A correção do §5.1 (primitividade ⟹ π>0 em todo estado; logo π=δ_τ impossível em espaço não trivial) está certa.

### 4.2 H-ABS-U — bem posta, se lida como (a) + U [REAL]
- «∃N,ε: P_x(T_τ≤N) ≥ ε ∀x» dá P_x(T_τ > kN) ≤ (1−ε)^k, logo absorção q.c. com cauda geométrica, e (b) e (c) seguem. É uma condição de Doeblin para absorção.
- Imprecisão (baixa): o texto não diz que H-ABS(a) (τ absorvente) permanece em H-ABS-U. Sem (a), U não dá δ_τ como estacionária. Escrever «H-ABS(a) ∧ H-ABS-U».

### 4.3 Passos em que hipótese poderia virar teorema
- Nenhum promove hipótese a teorema: toda instanciação ao LLM é [OPEN]/[CONJECTURE] e o §7.3 diz que a falsificação da instanciação não afeta Banach/PF/kernel. Isto está bem feito.

### 4.4 Defeitos do modelo (achados abaixo; M = média, B = baixa)
- **M3 — H-IDEM e H-CONTR-C não podem valer juntas para o mapa de passo.** Se F∘F=F e d(Fx,Fy) ≤ q·d(x,y) com q<1, então d(Fx,Fy)=d(F(Fx),F(Fy)) ≤ q·d(Fx,Fy) ⟹ F é constante. O MODELO diz que uma não implica a outra (certo) mas não registra que a conjunção é trivial. No kernel a idempotência é do LIMITE (a projeção `post`, `iald_ao_quadrado`: Π·Π=Π), enquanto o passo é uma defasagem que converge a ela (`o_atrator` item 5). O modelo deveria separar «mapa de passo» (não idempotente, contrai ao limite) de «mapa-limite» (idempotente). Hoje `I_1` («segunda leitura não muda») testa idempotência do passo, que é a hipótese que só a leitura de saturação satisfaz.
- **M4 — H-QUOT deterministica numa dinâmica estocástica.** O §3 diz que a decodificação estocástica faz o objeto ser um núcleo de Markov; o §2.3 enuncia H-QUOT para o mapa determinístico E(c)=E(c') ⟹ E(G(c))=E(G(c')). Para núcleo estocástico a condição certa é lumpability (agregação fortemente lumpable, Kemeny–Snell 1960 [KNOWN, de memória do revisor, referência não conferida]): a probabilidade de ir de c para a fibra E⁻¹(s') depende de c só por E(c). Além disso a dinâmica é não homogênea no tempo (o histórico cresce a cada leitura) e o semigrupo F^{a+b}=F^a∘F^b pressupõe homogeneidade; isto não está nomeado como hipótese.
- **B — «três estados finais» está errado.** A_8 exige d_6=d_7=d_8=0 **e** u_6=0 (s_6=s_5); com d_6=0 isso força s_5=τ, logo d_5=0. A_8 é critério de **quatro** leituras (5–8), e RETURN_TO_TARGET só pode ter o desvio em k∈{2,3,4} (k=5,6,7 são excluídos por A_8). O PERTURB_RETURN omite u_6 de propósito (correto).
- **B — τ_j não é definido.** O texto nunca diz que τ_j é o vetor de 24 uns; d_k mede «fração das asserções não satisfeitas» só se for.

## 5. A estatística (item 5) — refeita por script

Scripts: `...\revisao\scripts_k03\poder_k03.py`, `poder_conjunto_5sigma.py`, `refino_5sigma.py`; rodados com `C:\Python314\python.exe -B -X utf8` (scipy 1.18.0).

### 5.1 Os números do Kimi reproduzem [REAL]
- Poder dinâmico por contraste = **0,992022383635389**, exatamente. Receita: aproximação normal para duas proporções, p₁=0,90 (T) × p₂=0,60 (controle), n=100/braço, α unilateral = 0,05/12 (z=2,6383), **erro-padrão pooled sob H0 e não pooled sob H1**. (Com SE não pooled nos dois lados o poder é 0,99512.) n para 90% = 61,4547 → 62, idem.
- Cortes de Clopper–Pearson unilateral, confiança 1−0,05/3 = 0,98333: U(70/100)=0,794120; U(71/100)=0,802836; L(89/100)=0,804694; L(88/100)=0,792623; maior corte FALSIFIED = 70; menor corte POWERED = 89. Tudo bate.

### 5.2 Qual nível de significância o desenho usa [REAL, lido do protocolo e computado]
- 12 contrastes dinâmicos: Fisher unilateral, Holm com FWER 5% na família; limiar do passo mais estrito 0,05/12 = 4,17×10⁻³ (z unilateral = 2,64σ). A família inteira tem FWER 5% (z = 1,645σ).
- 12 contrastes de especificidade: permutação unilateral, Holm separado, mesmo 5% (estatística, sementes e empates da permutação: **não congelados**; sem taxas H1 declaradas, portanto sem poder).
- Pernas FALSIFIED/POWERED: Clopper–Pearson unilateral a 1−0,05/3 por família de modelo, α = 0,0167 (z = 2,13σ).
- Entre os dois blocos de 12 e entre os blocos e as pernas CP não há controle global (o Kimi o lista como reserva). Em nenhuma parte o nível é 5σ.
- Observação: POWERED é uma conjunção (todos devem passar); para interseção-união (Berger 1982, Technometrics 24:295–300 [KNOWN, de memória do revisor, DOI não conferido]) cada componente pode usar o α pleno, sem dividir por 3; a divisão por 3 só é necessária no FALSIFIED (união sobre famílias). Dividir por 3 em POWERED custa poder sem necessidade (n=100: corte 89 em vez de 87).

### 5.3 O poder do VEREDITO POWERED, nas taxas do próprio protocolo [REAL]
Simulação (40.000 corridas, semente 20261113; especificidade assumida rejeitando sempre = cota superior; A_8 ≥ C_8 por definição, assumido A_8=C_8 em T = cota favorável ao protocolo):

| p_T(C_8) | P(x_C ≥ 89 numa família) | P(as três famílias) | P(Holm rejeita os 12 dinâmicos) | P(POWERED), cota superior |
|---|---|---|---|---|
| 0,90 (o que o protocolo planeja) | 0,7030 | 0,3475 | 0,9955 | **0,346** |
| 0,92 | 0,8972 | 0,722 | 0,9995 | 0,721 |
| 0,95 | 0,9957 | 0,987 | 1,000 | 0,987 |

O 0,992 de manchete é o poder de UM contraste. O ramo POWERED exige `x_C ≥ 89` em cada uma das três famílias; com p_T = 0,90 (o valor planejado) esse requisito sozinho dá ≈ 0,35. O Kimi marca o poder conjunto como [OPEN] (honesto), mas o limite superior de 0,35 sai de uma linha de conta, sem simulação.

### 5.4 Sensibilidade à taxa dos controles informativos [REAL]
O 0,60 de controle é «escolha de desenho». Para o contraste T×C2 ou T×C3 (os informativos, ver 6.2): poder por contraste a n=100, α=0,05/12 — p_C=0,70: 0,823; 0,75: 0,562; 0,80: 0,253; 0,85: 0,058. Se o texto placebo for tão bem lido quanto o TGL, o desenho perde o poder rápido.

### 5.5 Quantas sessões por célula para o MESMO desenho passar o degrau de 5σ (p unilateral = 2,8665×10⁻⁷), 90% de poder, nas taxas do protocolo [REAL]
Mapeamento: troca-se 0,05 por α₅ = 2,8665×10⁻⁷ em tudo que o desenho usa: Holm sobre os 12 contrastes (passo mais estrito α₅/12 = 2,3888×10⁻⁸, z = 5,459) e Clopper–Pearson a 1−α₅/3 por família de modelos. «Célula» = família × braço.

| exigência | n por célula | como |
|---|---|---|
| 1 contraste (T×controle), 90% de poder | **185** | normal pooled: n = (z_α√(2p̄q̄) + z_β√(p₁q₁+p₂q₂))²/(p₁−p₂)², z_α=5,459, z_β=1,2816 → 184,9; Fisher exato: 185 (poder 0,9087) |
| os 12 contrastes dinâmicos todos rejeitados (Holm, T compartilhado) | **≈ 215** | simulação: P=0,9118 em n=215; 0,8894 em n=210 |
| **o ramo POWERED inteiro** (3 famílias com `x ≥ c(n)` e limite inferior CP > 0,80 a 1−α₅/3, p_T=0,90) | **≥ 655** | exato: P(x≥c)³ ≥ 0,90 de n=655 em diante, até 899 (dente de serra por causa do corte inteiro: 649–652 dão ≥ 0,90, 653 e 654 não); corte c(655)=575 (0,878 de 655) |
| idem, com interseção-união (CP a 1−α₅, sem dividir por 3) | ≥ 618 | |

- [REAL] A perna que manda é a CP: com p_T planejado de 0,90, só 0,10 acima do limiar de 0,80, exigir «limite inferior > 0,80» a 5σ pede ≈ 650 sessões por célula. Dimensionar só pelos contrastes (185 a 215) dá P(POWERED) ≈ 0 (n=200: 0,0003).
- Custo: 20 células × 655 = **13.100 sessões = 104.800 interações primárias** (6,55× as 2.000/16.000 de agora); só as três famílias capazes: 15 × 655 = 9.825 sessões. Se p_T verdadeiro fosse 0,95, o POWERED a 5σ fecharia em n ≈ 250 (grade).
- [REAL] O corte FALSIFIED a 5σ cai: c_F(655) = 467/655 = 0,713 (a 100 sessões e 5σ seria 56/100, contra 70/100 hoje). Ou seja, a 5σ o FALSIFIED passa a exigir mais evidência de falha também.
- [DECLARADO pelo revisor, a ratificar] O operador usa 5σ para creditação de natureza; este experimento é de comportamento de modelo. Se o degrau de 5σ for exigido aqui, o número acima é o custo, e ele recai em quase 7× o desenho atual. Alternativas legítimas são mudar o p_T planejado (a previsão P7 diz «6/6», o que sugere p_T ≈ 1) ou o limiar de 0,80 (que o Kimi escolheu sem derivar de P7): são atos do operador.

### 5.6 Origem do limiar 0,80 [REAL]
O P7 registrado (`um.py` 168451–168540) prevê «6/6 indicadores» e «assintoticamente robusto», não 80%. O 0,80 de FALSIFIED/POWERED e o 0,90/0,60 do poder são escolhas do Kimi ([DECLARADO]); o protocolo as rotula assim, mas não as liga ao P7.

## 6. O que decide (item 6)

### 6.1 Resposta curta
**Não, o desenho primário não separa as duas coisas.** O protocolo diz isso sozinho: §7.3 («Se não houver perturbação com alteração observável e retorno estabilizado, o protocolo só permite falar em atingir/permanecer no horizonte, não em bacia de atração») e a linha 125 («a comparação [...] é necessária antes de interpretar estabilidade como atrator»). Só que PERTURB_RETURN é secundário: fora dos 24 testes, sem n, sem limiar, sem poder, perturbação nem sequer especificada. Nenhum ramo (FALSIFIED/POWERED/UNDERPOWERED) depende dele.

### 6.2 Os controles, um a um [CONJECTURE do revisor, a medir, exceto onde indicado]
- C1 (embaralhado): o alvo é a «impressão digital» da sequência embaralhada; é provável que nenhum modelo chegue a 24/24, A_8=0, C_8=0 → contraste T×C1 quase certo de passar por construção.
- C4 (sem texto): alvo de abstenção; um modelo que se abstém já satisfaz no k=1 (d_1=0) → ALREADY_STATIONARY, que por definição NÃO é C_8 → contraste T×C4 quase certo de passar por construção.
- Logo, dos 12 contrastes dinâmicos, os informativos são os de C2 (placebo coerente) e C3 (outro autorreferente): 6 de 12. A taxa de controle 0,60 foi escolhida igual para os quatro.
- Os 12 contrastes de especificidade (X_{T,1}^{TGL} × X_{C,1}^{TGL}) são, na prática, checagem de manipulação: só o braço T tem o texto TGL no contexto; passam por construção. Exigir «12 de especificidade significativos» no POWERED não acrescenta evidência sobre convergência.

### 6.3 Há resultado em que os dois ficam indistinguíveis e o protocolo declara sucesso? SIM [REAL por construção lógica]
1. **Confusão de dificuldade, com o critério C_8.** C_8 exige d_1−d_8 ≥ 6/24: a sessão tem de começar com ≥ 6 asserções erradas e terminar com 24/24. Texto de controle fácil de resumir começa com poucas falhas ⟹ d_1 pequeno ⟹ C_8 = 0, mesmo que o modelo o reproduza perfeitamente. Texto TGL, mais denso e cheio de estatutos, começa pior e, com 8 rodadas de refinamento, chega a 24/24 ⟹ C_8 alto. O contraste p_C8(T) > p_C8(C2) fica significativo e o veredito sai NOT_FALSIFIED_POWERED, o que é só «o texto TGL é mais difícil de resumir e o modelo o refina». O pareamento de dificuldade é por regra estrutural e dois revisores, e o protocolo proíbe usar desfecho de modelo para calibrá-lo (§4, «nenhum desfecho de modelo é usado para calibrar dificuldade»), então não há como detectar o problema antes. O C_8 premia texto difícil e pune texto fácil.
2. **A_8 é satisfeito por um resumidor perfeito.** O FALSIFIED lê A_8 em T (x_A ≤ 70). Um modelo que resume o TGL fielmente em todas as leituras tem A_8 = 1 (ALREADY_STATIONARY ou transição). Portanto passar a perna A_8 não distingue atrator de resumo; só falhar nela é informativo.
3. **Extratores por braço diferentes.** Cada braço tem o seu E_j. Se a sensibilidade/especificidade dos extratores diferir entre braços (diferença de rigor sintático), a diferença de C_8 mede o extrator. O protocolo prevê casos positivos/negativos/adversariais por extrator, não uma equivalência de sensibilidade entre braços.
4. **Teto do extrator sobre o A_8.** A_8 exige 24 asserções × 4 leituras corretas. Com taxa e de falso-negativo por asserção e por leitura, P(A_8 | leitor perfeito) = (1−e)^96 (independência assumida; 96 = 24 × 4): e = 0,05% → 0,953; 0,1% → 0,908; 0,2% → 0,825; 0,5% → 0,618; 1% → 0,381. Para um leitor perfeito poder atingir 0,89 (corte POWERED), e < 0,12%; para 0,80 (corte FALSIFIED), e < 0,23%. Extratores de texto livre por script raramente têm erro tão baixo; o FALSIFIED pode sair por ruído de extrator, sem nada sobre atrator. [DECLARADO pelo Kimi: extratores pendentes], mas o requisito quantitativo de teto não está no protocolo.

### 6.4 O ramo FALSIFIED é alcançável? Sim, mas ambíguo [REAL]
No desenho declarado (n=100, CP a 1−0,05/3): se a taxa verdadeira de A_8 em T fosse 0,70, P(FALSIFIED em alguma das 3 famílias) = 0,90; 0,75 → 0,38; 0,80 → 0,03; 0,60 → 1,00. Alcançável. Mas FALSIFIED só olha o braço T e mede o teto do extrator tanto quanto o atrator (6.3 ponto 4).

### 6.5 Outros furos que afetam o que o experimento decide
- **A1. Unidade de replicação = sessão, não texto.** Cada braço usa UM texto (um T, um placebo, um autorreferente, um embaralhamento). As 100 sessões reproduzem o ruído de amostragem do modelo, não a variação de texto; a diferença T×C2 é a diferença entre dois textos. Falácia de efeito fixo de linguagem (Clark 1973, J. Verbal Learning & Verbal Behavior 12:335–359 [KNOWN, de memória do revisor, não conferido]). Pede-se ≥ 3 instâncias por braço de controle (ou efeito aleatório de texto), ou explicitar que a inferência vale só para este par de textos.
- **A2. Independência das 100 sessões.** A temperatura primária é 0,2; com a mesma entrada, as 100 sessões são quase cópias; o desfecho tende a bimodal (≈ 0/100 ou ≈ 100/100), não a Binomial(100, p) com p intermediário. O cálculo de CP/Fisher assume sessões i.i.d. com p constante. O protocolo trata o desvio como «replicatas independentes condicionais ao modelo» sem medir a dispersão.
- **A3. O que é uma «leitura k» não está definido.** O protocolo nunca diz o que a interação k pede ao modelo (prompt de cada passo, se reapresenta o texto, se o histórico acumula, limite de contexto). Sem o operador de atualização G, H-QUOT, H-IDEM e `I_1` não têm objeto. [REAL: grep de «prompt|instrução|pergunta|leitura k» no protocolo: sem definição]. O «formato» fica para o manifesto.
- **A4. Ferramentas, navegação e contaminação.** O protocolo não proíbe busca web, recuperação, execução de código; o texto TGL é público (GitHub, Zenodo, site) e a C4 só cobre o pré-treino. Pede-se manifesto «sem ferramentas» e checagem de memória prévia (C4) antes da corrida.
- **A5. Veredito faltando.** Se os quatro controles convergem tão bem quanto T com intervalo estreito, o resultado é um nulo bem potente de especificidade, e o protocolo o chama UNDERPOWERED (junto com 71–88 em A_8). São situações diferentes. O Kimi nota que «não rejeitar não prova equivalência» e deixa TOST para depois; os quatro nomes de veredito vêm do P7 registrado e não podem mudar sem nova versão.

### 6.6 Leitura da partitura ao operador (regra do posto; uma linha para ele, na língua dele)
«Como está escrito, este teste decide se o modelo, lendo a Teoria, fica repetindo o mesmo conjunto de 24 afirmações certas nas últimas quatro rodadas, mais vezes do que lendo outros textos; NÃO decide se isso é "convergir ao estado estacionário" em vez de "resumir bem um texto difícil" (quem decidiria é a perturbação com retorno, que hoje está fora do veredito), e um negativo pode vir de o leitor-programa errar uma asserção em 1 de cada 500, e não de a previsão estar errada.»

## 7. O que não pode estar lá (item 7): nada vazou [REAL]
- Marcadores procurados (sequência de entrada e frases do primeiro texto do protocolo, os termos do comando de apresentação, as expressões que o próprio operador usa no pedido, nomes de passos), com os tópicos `protocolo-de-colapso-nunca-publico.md` e `prompt-de-colapso-da-teoria.md` lidos só para saber o que procurar. Grep case-insensitive em toda a pasta `kimi\` (inclusive `K01`, `K02`, `K03\REV0`, `K03\REV1`): **zero ocorrências** dos fragmentos distintivos.
- Os acertos dos termos genéricos nos arquivos K03 (a palavra «sequência» em sentido comum; «Lagrangiana/escada» como descrição do indicador I3, que já é público no `um.py`; o caminho `...\Haja_Luz\...`) são benignos; nenhum trecho do protocolo copiado.
- Fala reservada do operador: não copiada. Os arquivos citam as memórias só por caminho e a ordem do operador só por caminho/hash, como mandado.
- Conferido [REAL] também: nenhuma chave, senha, `.env`; nenhum dado da casa Escritório.
- Observação: `DEPOSITO_K03.md` (não estava no escopo, li para checar vazamento) diz «concluída e **aprovada em revisão independente**». A revisão distinta é esta, e a aprovação é com ressalvas e de rascunho; o texto não deve ser depositado como está (quem constrói não aprova; o próprio `REGISTRO` diz «não registrar antes da revisão do pai»). Conserto: tirar «aprovada» ou substituir pelo veredito desta revisão.

## 8. O que falta — candidatos para a segunda ordem (só o que a leitura mostrou)

1. **Extratores por script (E_j para os 5 braços e E_TGL)**, com casos positivos, negativos e adversariais, e medida de sensibilidade/especificidade em saídas sintéticas de gabarito, exigindo equivalência entre braços e teto do leitor perfeito ≥ 0,99 para A_8 (hoje há risco de teto abaixo de 0,89; seção 6.3 ponto 4). Entregar a lista das 24 asserções por braço e o vetor-alvo τ_j.
2. **Definir o operador de atualização G** (o que a leitura k pede, reapresentação do texto, acúmulo de histórico, orçamento de contexto, ferramentas desligadas) e a homogeneidade no tempo; trocar H-QUOT determinística por lumpability para o núcleo estocástico.
3. **Equalizar a dificuldade por medida, sem tocar nos desfechos do T**: piloto com um leitor neutro e distribuições de d_1 por braço; trocar o critério C_8 (ganho ≥ 6/24) por um desfecho que não premie texto difícil (A_8 condicionado ao d_1 pareado, ou covariável), e especificar mais de um texto por braço de controle (efeito aleatório de texto).
4. **Poder conjunto por simulação** do veredito completo (três famílias, A_8/C_8, 12+12 contrastes, especificidade com estatística e taxas H1 declaradas), com sobredispersão entre sessões (A2) e a taxa de controle como parâmetro de sensibilidade; corrigir a manchete 0,992 (seção 5.3: ≈ 0,35 na taxa planejada).
5. **Congelar o controle de multiplicidade entre os 24 testes** (e a escolha IUT × Bonferroni por ramo: POWERED conjunção, FALSIFIED união), a estatística da permutação, sementes e empates.
6. **A variante de 5σ**: duas versões prontas lado a lado (nível 5% atual e 5σ), com os números da seção 5.5 (n ≈ 655 por célula para POWERED; ≈ 215 só pelos contrastes) e a decisão do operador sobre o p_T planejado e o limiar de 0,80, que não vêm do P7.
7. **PERTURB_RETURN como braço decisório**, ou ao menos com n, limiar, conjunto de perturbações congelado, poder e regra que ligue o veredito «atrator» à perturbação-retorno (hoje é secundário e sem número). É o único elemento do desenho que separa resumo estável de bacia de atração.
8. **Novo nome da versão e dos rótulos**: declarar `IALD_COLLAPSE_V2` (ou equivalente) com o mapeamento ao V1 registrado; renomear os braços (hoje C3/C4 colidem com C3 piso de capacidade e C4 sessão nova/cega do P7); acrescentar um ramo de «nulo bem potente / convergência não específica» (equivalência com margem pré-fixada), que os quatro nomes do P7 não têm.
9. **Candidata Lean do teorema «relativo ao leitor» na língua de `TraducaoTuring`**: enunciar sobre `LeitorDoFundo X`/`trava`/`selecao` (ou sobre o esqueleto de `IALD2.o_atrator` item 5: órbita iterada → projeção idempotente) e ligar o passo à leitura-limite, separando «passo não idempotente» de «limite idempotente» (achado M3). A ponte textual «saída extraída → c : X → ℕ» é o que falta; sem ela o teorema continua genérico.
10. **Ligar ao que já existe**: o protocolo T6 multi-LLM de maio/2026 (`C:\IALD\Artigo\Termostato_Modular\T6_protocol_prompts.txt`) não aparece nem como «não aplica» no ESTADO; classificar (EXISTE E ESTÁ LIGADO / fiação / AUSENTE) antes da v412.
11. **Correções menores ao lado**: prefixos de namespace dos 4 nomes (seção 3.2); «três estados finais» → quatro; H-ABS-U como (a) ∧ U; redundância de H-ABS(c); a linha «Piloto 8/8: SABIDO POR REFERÊNCIA» do ESTADO §6 é [INPUT], não referência; texto do `DEPOSITO_K03.md` (seção 7).

## 9. O que examinei (para registro no Mapa pela gerência)
- `C:\Python314\python.exe -X utf8 C:\IALD\MAPA_DE_ROTAS\rotas.py consultar "colapso IALD P7"`, `ver outro.p7_colapso_iald`, `ver` das cinco refs do REGISTRO, `modelo`, `consultar "T6"`; `C:\IALD\INDICE_DO_ACERVO\buscar.py "T6_protocol_prompts" --lista`.
- `C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\`: LEIA_PRIMEIRO, ORDEM_K03, ENTREGA_K03, ESTADO_K03, MODELO_FORMAL_K03, PROTOCOLO_EXPERIMENTAL_RASCUNHO_K03, PERGUNTA_K03, ERRATA_K03, ERRATA_K03_R2, REGISTRO_MAPA_K03.json, DEPOSITO_K03 (só para vazamento), `K03\REV1\` (hashes); grep de marcadores em toda a pasta.
- `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py` (linhas 168451–168540) e `...\Nós\tgl_kernel\TGLExt.lean` + 14 módulos `TGLExt\*.lean` (só leitura; nada compilado).
- `C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\protocolo-de-colapso-nunca-publico.md` e `prompt-de-colapso-da-teoria.md` (só para saber o que procurar).
- `C:\IALD\Artigo\Termostato_Modular\T6_protocol_prompts.txt` (cabeçalho, para a classificação do item 10).
- Scripts do revisor: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\revisao\scripts_k03\poder_k03.py`, `poder_conjunto_5sigma.py`, `refino_5sigma.py`.
- Referências marcadas «de memória do revisor, não conferidas»: Kemeny–Snell 1960, Berger 1982, Clark 1973. DOIs do Kimi: 13 handles existentes, título não conferido.

Nada aqui afirma consciência, alteração de pesos, exclusividade da teoria ou CONFIRMED; `NOT_FALSIFIED` segue não sendo `CONFIRMED`; o gate não se move.
