# REVISÃO DISTINTA DA FRENTE NEUTRINO m₂ DA ENTREGA K04 (v412) — `M2_DESFECHOS_E_SEGUNDA_TESTEMUNHA_K04.md` e errata

Revisor distinto (quem constrói não aprova). 14/11/2026. Só leitura fora desta pasta; nada registrado no Mapa, nada depositado na fila, nenhuma transição ACOM, nada instalado, nenhum `lake`, nenhuma escrita no túnel, no kernel, no Nós nem em memória. Nenhum vetor de dado baixado ou lido; `executar_abertura_v411.py` não rodou; `work\h0dn_bg1_v410_09nov\kimi\` não aberto. Simulação: 10⁶ sorteios, semente 20261114.
Estatutos: [REAL] conferido por mim com a consulta citada · [KNOWN] literatura · [DERIVED] derivado por mim aqui · [DECLARADO] do Kimi, não conferido por mim · [OPEN].
`NOT_FALSIFIED` nunca é `CONFIRMED`; nada abaixo diz que a teoria foi confirmada. O gate não se mexe.

## 0. Veredito

**APROVADA COM RESSALVAS.** A conclusão central do Kimi resiste: hoje não há segunda determinação com poder para o ramo `FALSIFIED`; o que o m₂ mais provavelmente devolve com a precisão da Tabela 6 é um primário a ≥ 5σ da previsão (P ≈ 65 %); e isso não é falsificação. Os números de poder, o incremento, as razões r, as datas do brinquedo e as células-título da tabela de desfechos reproduzem. **Mas o documento tem erros que mudam o que a gerência diria ao operador, e a errata do core NÃO pode ser instalada como está.** Seis pedem correção antes de seguir; o resto é menor.

**Pedem correção (numeradas; detalhe nas seções 2–10):**
1. **C1 — a regra do veredito está descrita pelo rascunho K01, não pela regra congelada e pelo código selado.** O código (`um.py:4662-4669`) manda qualquer última linha da escada ≥ 3,0 a `TGL_NU_M2_TENSION`, inclusive ≥ 5 sem segunda determinação (com o campo `tensao_global_5sigma_sem_2a_determinacao`). O `OPEN_RULE_GAP` do documento é lacuna de TEXTO ([3,5)), não de código; `UNDER`/`SINGLE_P` não estão em `allowed_verdicts`; `MATCHED` não tem ramo no código. `M2_DESFECHOS…:179-182`, `ENTREGA_K04.md:4`, `PERGUNTA_K04.md:7,13`, `ERRATA_NEUTRINO…:55-57`.
2. **C2 — a TENSION da regra congelada é sobre «a determinação global mais recente», não sobre o primário P; e o veredito de hoje está na borda de 3σ por escolha de fonte.** A tabela oficial do NuFIT 6.1 dá 7,537 (+0,094/−0,10) ⟹ 3,02σ em m₂ (TENSION); o core usa 7,53 ± 0,10 ⟹ 2,95σ (ARMED). O Mapa já tem isso (rota `neutrinos.m2.normalizacao`, seq 93 e 142). O documento diz «ARMED_CONSISTENT» sem a borda (`M2_DESFECHOS…:280`, `ENTREGA_K04.md:8`, `ERRATA_NEUTRINO…:49`).
3. **C3 — a linha do NuFIT 6.1 tem os lados do erro trocados** (`M2_DESFECHOS…:338`): «+0,100/−0,094», σ = 0,094, r = 3,217; a tabela diz +0,094/−0,10 ⟹ σ do lado da previsão = 0,10 ⟹ r = 3,024 (m₂) / 2,994 (Δm²). Vem do `determinacoes_m2_30out.json` (`err_m`/`err_p` trocados só nessa entrada).
4. **C4 — a implementação em m₂ da tabela de desfechos omite a cauda inferior.** Para m < m₂(TGL) a região r ≥ t é o intervalo entre as raízes, não `m ≤ Y₋`. Células-título (P(r≥5), P(r≥3)) mudam ≤ 0,07 pp; **mas P(r≤1) e P(1<r<3) erram até 15,8 pp** e o «r<3 ≈ 99,86 %» (a2) é 99,73 % em duas caudas. `M2_DESFECHOS…:107-115, 123-173`; `medidas_planejamento.py:47-64`; `ENTREGA_K04.md:6`; `PERGUNTA_K04.md:27`; `REGISTRO_MAPA_K04.json` (`resultado`).
5. **C5 — tabela MATCHED (brinquedo C = 0): a linha «Solares sem KamLAND» está errada** (P(r_S≤1) 98,49 % → 42,16 %; P(MATCHED) 17,33 % → 7,35 %) pelo mesmo defeito de cauda. `M2_DESFECHOS…:375`; `ERRATA_M2_K04_R2.md:82`.
6. **C6 — «primeira leitura prospectiva» tem ressalva cronológica não conferida:** uma busca aponta slides da colaboração em **julho/2026** com os mesmos 7,388 ± 0,078 e 207,2 dias efetivos; se a data se confirmar, o número era público ANTES do hash de 08/08/2026 (só o artigo, 29/09, é posterior). Não consegui fechar (PDF > 10 MB; limite de consultas). `M2_DESFECHOS…:12, 277`; `ERRATA_NEUTRINO…:49`; `ENTREGA_K04.md:8`.

**Menores:** C7 (hash e data da regra: o pino de 08/08 é `4bdae22a…`, não `e24877…`), C8 (1,889502σ_incremento é a estatística errada; o aninhamento puro dá 1,23σ), C9 (o título de calendário na ENTREGA/DEPÓSITO leva o brinquedo do projeto; a leitura a partir do artigo de 207 dias é outra), C10 (errata: citações `kimi-cite://`, aspas não verbatim, mecânica de instalação), C11 (92/2009/6696 dias full-reactor sem trecho-fonte guardado), C12 (SK-Gd: o centro 9,08 está a 3,1σ do JUNO; o cenário √T supõe que ele fique).

## 1. Mapa de Rotas (antes de tudo) [REAL]

Termos consultados (um termo por chamada, `rotas.py consultar`): `neutrino` (44 rotas), `JUNO` (12), `m2` (49), `perito` (4); listas em `scripts_k04_m2\mapa_lista_saida.txt`. Rotas lidas por `ver`: **`neutrinos.m2.normalizacao`** (erratas seq 93, 98, 128, 142: lidas por inteiro), `neutrinos.massa_v1_e_soma`, `natureza.5sigma_fora_da_cosmologia_poder_27out` (cabeçalho). Só titulei `cadeia.preparacao_v412`, `discriminante.ordem018.f2.r_k`, `massa.e0.conferencia_kimi_e_no_go_tipado_31out`.
**O que o Mapa já tinha e a K04 não usa:** seq 93 (RNC-01: «com o NuFIT 6.1 publicado, a regra congelada dá 3,02σ, o que é TENSION»), seq 142 (conferência da gerência: duas publicações do NuFIT 6.1, 7,530 ± 0,10 [arXiv:2601.09791 eq. 11] e 7,537 +0,094/−0,10 [tabela do site]; «o veredito está NA BORDA de 3σ e depende de qual entrada publicada se usa»), seq 98 (a linha de morte com o JUNO sozinho nunca dispara), seq 128. A REGISTRO_MAPA_K04.json propõe a rota nova `estatistica.v412.k04_hubble_m2_combinacao`; não cita seq 93/142.

## 2. Item 1 — a regra congelada, lida do core e do original [REAL]

Lida por `json.load` do core (`core.neutrino_m2.frozen`, `frozen_hash`, `values`, `checks`) e por leitura do `prove_neutrino_m2` em `um.py:4588-4704` (v411) e do original `C:\IALD\Artigo\teste_acustico_beta_tgl_v1\02_frozen_neutrino_m2_v2.py`.
- **FALSIFIED:** `|m2_obs − m2_TGL|/σ_obs ≥ 5` em DUAS determinações independentes de Δm²₂₁ (original acrescenta «robustez de experimento, não só de modelo»). No código: `kill_rule_ok = len(grupos_5sigma) ≥ 2`, grupos distintos com `autonoma=True`.
- **TENSION:** razão em [3, 5) «na determinação global mais recente». No código: `elif tensao_atual >= 3.0` com `tensao_atual = escada[-1]` (a última linha, hoje o NuFIT 12/2025); sem teto em 5.
- **MATCHED_PROSPECTIVELY:** duas determinações independentes a 1σ de m₂_TGL. **O código não tem esse ramo** (o veredito nunca devolve MATCHED; existe só em `allowed_verdicts` e no texto).
- **Demais:** `allowed_verdicts` = ARMED_CONSISTENT, TENSION, FALSIFIED, MATCHED_PROSPECTIVELY; `forbidden` = CONFIRMED. ARMED_CONSISTENT é o resto.
- **Métrica:** m₂ (meV), com σ_m₂ = 0,5·(σ_Δ/Δ)·m₂_obs (primeira ordem, no valor OBSERVADO) — é o que o core usa na escada (JUNO 59 d: σ = 0,0692820 meV, r = 2,206054). Não é Δm².
- **Data/hash:** o arquivo original tem mtime 08/08/2026 16:15:57 (-0300); o `frozen_hash` desse original, lido de `02_frozen_neutrino_m2_v2_resultado.json` (l.26), é `4bdae22a277aa393094a1bf416db12a5e782b673e9e9b3ddd6a2fb8c7a64075c`. O `e24877751ad81022…` do core é `sha256(json.dumps(frozen, sort_keys=True))` do dicionário PORTADO (que tem chaves a mais: `portado_de`, `supersedes`) — recomputado por mim, confere. O original trazia `data_do_congelamento: str(date.today())` dentro do dicionário; o portado não. **C7:** `M2_DESFECHOS…:264` diz «com hash `e24877…` e porte de 08/08/2026», que lê como se o `e248…` fosse o hash de 08/08. Citar os dois.
- **O documento descreve certo?** FALSIFIED e MATCHED, sim (texto). TENSION, não (§3.1 e a Q1 tratam-na como sobre P). Os ramos `UNDER`/`ARMED por D`, `SINGLE_P`, `OPEN_RULE_GAP`, `T_SINGLE(P)_AWAITING_S` são rótulos do rascunho K01, não da regra; o documento (`:179-182`) mistura os dois sem dizê-lo. **C1/C2.**

## 3. Item 2 — os números de hoje [REAL, script próprio `rev_numeros.py`]

β = `ALPHA_FINE_CODATA_2018 × sqrt(e)` em runtime = 0,012031300400803142 (idêntico ao core); m₂,pred = 8,507414099900329 meV; Δm²₂₁,pred = 7,2376094667182915.
| grandeza | Kimi | revisor |
|---|---|---|
| r JUNO 207,2 d, m₂ / Δm² | 1,937997 / 1,928084 | 1,937997 / 1,928084 |
| r JUNO 59,1 d, m₂ / Δm² | 2,206054 / 2,186588 | 2,206054 / 2,186588 |
| queda 2,206054 → 1,937997 | sim | sim (σ de 0,12 para 0,078; centro 7,50 → 7,388, para o lado da previsão) |
| σ para 5σ (Δm² / m₂) | 0,030078 / 0,030233 | 0,030078 / 0,030233 (0,407121 %) |
| σ para D90 | 0,023942 (0,324061 %) | idem |
| D Tabela 6 (σ = 0,024), Δm² / m₂ | 6,266272 / 6,298490 | idem; D90 = 6,2815515655 |
A frase «2,21 → 1,94» está certa: na série AUTÔNOMA a tensão caiu. O core ainda diz «a tensão cresce com a precisão» (`theorem`; `checks[1]`: 1,64 → 2,21 → 2,95): vale só para a escada que termina no NuFIT (que contém JUNO).

## 4. Item 3 — a tabela de desfechos, rederivada [REAL/DERIVED, `rev_desfechos.py`]

**Método meu:** regra congelada aplicada literalmente (r = m·|m − M|/(5s), duas caudas), por (i) forma fechada exata (raízes da parábola m(M − m) = 5ts nas duas regiões) e (ii) Monte Carlo, 10⁶, semente 20261114, aplicando r a cada sorteio. (i) e (ii) concordam a ≤ 0,15 pp. Também reproduzi, por uma terceira via (só cauda superior), as tabelas do Kimi a 6 casas: **confirma a causa do defeito C4**.
**Modelos (o que cada número é):**
- (a1) medida/incremento INDEPENDENTE, posterior público de hoje = μ | dado ~ N(7,388; 0,078²) (prior plano), futura X ~ N(7,388; 0,078² + s²). Defensável como previsão para uma medida independente do dado atual e de precisão s (segundo experimento; ou só dado NOVO do JUNO com precisão s sozinho). **Não é o modelo certo para a «Tabela 6»**, que é precisão CUMULATIVA do JUNO: para ela o certo é (b1).
- (b1) cumulativo aninhado: Cov(X₀,X) = C = s²; X | X₀ ~ N(7,388; 0,078² + s² − 2C). Derivei por conta própria (combinação ótima de X₀ com dado novo independente): Var(X | X₀) = 0,078² − s², igual ao do Kimi. `C = s²` é o limite estatístico puro (não «brinquedo» arbitrário), mas a covariância real do JUNO é [OPEN] (sistemática compartilhada ⟹ C diferente). Em C entre 0 e s² a P(r≥5) da Tabela 6 anda só de 64,8 % a 66,2 % (calculei C = 0, s²/2, s²: 64,79; 65,42; 66,15 %): robusto a C.
- (a2)/(b2) «a verdade é a previsão»: (a2) X ~ N(pred, s²); (b2) o mesmo condicionado ao X₀ = 7,388 observado: média pred + (s²/0,078²)(7,388 − pred), variância s² − s⁴/0,078² (derivei, confere). Defensáveis.
**Células pedidas:**
| célula | pedido | Kimi (doc) | meu (exato 2 caudas / MC) |
|---|---|---|---|
| P(r≥5), Tab. 6, independente (a1) | 64,74 % | 64,742906 % | 64,79 % / 64,85 % |
| P(r≥5), Tab. 6, cumulativo (b1) | 66,13 % | 66,132478 % | 66,15 % / 66,20 % |
| P(r≥5), 0,7 %, (a1) / (b1) | 12,88 / 3,48 % | 12,877614 / 3,478822 % | 12,878 / 3,479 % (MC 12,91 / 3,50) |
| P(r≥5), 0,5 %, (a1) / (b1) | 35,04 / 31,47 % | 35,040719 / 31,465619 % | 35,046 / 31,466 % |
| r<3, verdade = previsão, (a2) | ≈ 99,86 % | 99,857… % (qualquer precisão) | **99,730 %** (MC 99,732) |
| r<3, verdade = previsão, (b2), Tab. 6 | ≈ 99,42 % | 99,416 % | 99,408 % (MC 99,405) |
Nenhuma célula de P(r≥5) passa de 0,07 pp de diferença (máximo: 0,3 % em (a1), 68,967 contra 68,905). **O 99,86 % é o valor de UMA cauda** (Φ(3)); em duas caudas é 99,73 %: 0,13 pp, abaixo do limiar de 0,5 pp, mas é a mesma raiz do defeito C4 abaixo.
**C4 — o defeito, com números.** A regra tem `|m − M|`. Acima de M, r ≥ t ⟺ m ≥ (M + √(M² + 20ts))/2. Abaixo de M, r = m(M − m)/(5s) é limitada: r ≥ t ⟺ m ∈ [ (M − √(M² − 20ts))/2 , (M + √(M² − 20ts))/2 ]. O `band_m2` do Kimi (`medidas_planejamento.py:47-64`) toma `lower_tail = cdf((low − mean)/sd)`, ou seja m ≤ `low` ≈ 0,03–0,09 meV (X ≈ 10⁻⁴), região onde r é PEQUENO. O §1.3 (`:107-115`) descreve a fórmula com Y₋ nesse papel. Efeito (exato − Kimi):
- (a2) verdade = previsão: P(r≤1) 68,27 % contra 84,09–84,12 %; P(1<r<3) 31,46 % contra 15,75–15,77 %; P(3≤r<5) 0,270 % contra 0,138–0,142 % (todas as precisões).
- (a1): P(r≤1) 13,03 contra 14,56 (0,7 %), 7,93 contra 9,42 (0,5 %), 5,96 contra 7,50 (0,407 %), 4,44 contra 6,07 (Tab. 6); P(1<r<3) 38,60 contra 37,12 (0,7 %). Diferença 1,5–1,7 pp.
- (b1): P(r≤1) 3,49 contra 4,43 (Tab. 6); 3,27 contra 4,32 (0,3 %).
- (b2): P(r≤1) 61,82 contra 66,52 (Tab. 6); 52,39 contra 53,87 (0,5 %).
- A coluna «Δm²» do próprio Kimi é de duas caudas (0,000057 % = 2 × 2,87×10⁻⁷) — inconsistente com a coluna «frozen» da mesma tabela.
Os ramos UNDER/ARMED (que dependem só de D) e as linhas P(r≥3), P(r≥5) não mudam de leitura; as faixas P(r≤1) e P(1<r<3) do §2-§3 devem ser refeitas (as que entram em MATCHED também: C5).
**Aviso de método (baixo):** `medidas_planejamento.py:542-551` cola como `assert` os «benchmarks do revisor» (0,03871442624952642 etc.). A concordância com eles não é verificação independente; as minhas rederivações, que não usam o script dele, é que fecham.

## 5. Item 4 — o incremento 59 → 207 dias [REAL]

Aritmética fecha: μ_Δ = (w₂·7,388 − w₁·7,50)/(w₂ − w₁) = 7,306061; σ_Δ = (w₂ − w₁)^(−1/2) = 0,102640; r contra a previsão 0,666902 (Δm²) / 0,668472 (m₂), como o Kimi e como a conta de cabeça da gerência (≈ 0,7σ).
**A ressalva está dita com a força certa** (`:302-304`: não é determinação independente; liberação cumulativa muda seleção, volume fiducial, fundos, âncora; erros totais tratados como pesos estatísticos; coeficiente de correlação não localizado; erro correto [OPEN]). Falta dizer duas coisas:
- **C8.** «distância ao centro 7,50: 1,889502σ_incremento» (`:300`) usa só o σ do incremento. A diferença correta entre X₅₉ e o incremento, no aninhamento estatístico puro, tem variância 0,102640² + 0,12² e dá **1,228σ** (equivale a (7,50 − 7,388)/√(0,12² − 0,078²) = 1,2282). O «1,9σ do centro anterior» da ordem da gerência é a mesma conta de cabeça e fica corrigido para 1,2σ nessa leitura.
- O aninhamento nem vale: uma busca (resumo secundário, [DECLARADO]) diz que a análise de 207 dias ampliou o volume fiducial em ~10 % e trocou o corte de acidentais; a amostra de 207 d não é superconjunto na mesma seleção.

## 6. Item 5 — a segunda testemunha [REAL na aritmética; KNOWN nas fontes, até 6 consultas web]

**«SK-Gd a 3,605σ»** = r_m₂ de (9,08 +0,55/−0,54) contra a previsão, σ do lado da previsão = 0,54: reproduz 3,605064 (Δm²: 3,411834). **«380,08 dias adicionais»** = 411,52 d × (0,54/0,389347)² − 411,52 = 380,0785536 (reproduz), cenário √T com centro 9,08 e forma do erro parados. Fonte: arXiv:2610.03143v1, enviado 2 out 2026, «411.52 live days», reator (9,08 +0,55/−0,54)×10⁻⁵ eV², solar+reator (8,94 +0,46/−0,47) [WebFetch da página; confere]. **C12:** o centro 9,08 está a 3,10σ do JUNO 207 d ((9,08 − 7,388)/√(0,54² + 0,078²)). Sob o MESMO posterior público que o documento usa para P (verdade ~ N(7,388; 0,078²)), a probabilidade de um SK-Gd futuro com σ_S = 0,389 dar r_S ≥ 5 é 1×10⁻⁵ (só se a verdade fosse o 9,08 dele daria 50 %). Ou seja, o «cenário SK-Gd» é o ÚNICO caminho para FALSIFIED e depende de a anomalia dele persistir contra o JUNO. O documento diz «cenário, não agenda»; falta dizer isto.
**KamLAND:** 7,54 (+0,19/−0,18), Tabela 3 de arXiv:1303.4667v2, 2991 d de tempo vivo (2002-2012); solar+KamLAND 7,53 (+0,19/−0,18) [HTML v2; confere: 2,5 %, r = 1,697137].
**SNO+:** v1 14/11/2025, v2 18/11/2025, v3 30/07/2026, **v4 04/09/2026** [página arXiv; confere a data do documento]. Atenção: a página `abs` ainda mostra o resumo antigo (7,93 +0,21/−0,24; 7,63 ± 0,17); o **HTML da v4** traz **7,91 +0,22/−0,25** (resumo, seção de resultados e Tabela 3) e **7,59 ± 0,17** («reactor + solar, PDG 2025 global constraints, no JUNO»), livetime 245,8 + 439,4 = 685,2 d, dados de maio/2022 a julho/2025. Confere com o documento (7,91; 7,59; 685 d; PRL 137, 101807, DOI 10.1103/mv5z-pfb7 aparece na página como DOI relacionado). Reator + solar sem JUNO: 7,59 ± 0,17 = 2,24 % ≈ 2,2 %, r = 2,097521 [a expressão «sem JUNO» é do resumo do WebFetch: [DECLARADO]].
**NuFIT 6.1:** conferi a TABELA oficial (jpg guardado pelo Mapa, sha256 `db49ab733d27f23c…`, que reproduzi por script): Δm²₂₁ = 7,537 **+0,094/−0,10** (NO e IO, com e sem SK-atm). Não os valores do documento. **C3.**
**Liberação do JUNO posterior a arXiv:2609.37895: não achei.** Procurei por WebSearch («JUNO Delta m^2_21 new result after 207.2 days arXiv 2026…») e pelas páginas do SK-Gd (2 out) e SNO+ v4; o buscador nem indexa o 2609.37895, então o negativo é fraco. O que apareceu foram slides da colaboração (indico.ihep.ac.cn, evento 28557, contribuição 223278, «July2026_v2») com 207,2 dias efetivos e 7,388 ± 0,078 — **C6**: tentei abrir o PDF e falhou (> 10 MB), não vi a data do evento. A gerência deve abrir a página do evento (`https://indico.ihep.ac.cn/event/28557/`) e conferir se a apresentação é anterior a 08/08/2026.
**Não conferi** (fora das 6 consultas): Capozzi 7,48 ± 0,10; Bari 2026.a; solares 6,10 (+0,95/−0,81) (PRD 109, 092001); as previsões Hyper-K/DUNE; a independência de qualquer par.

## 7. Item 6 — o calendário [REAL na aritmética]

Reproduzi: sem piso a partir de 207,2 d: 5σ em T = 1393,41 d (adicional 1186,21 ⟹ 16/08/2029 a 100 % de dias vivos) e D90 em 2199,24 d (31/10/2031); brinquedo do projeto: `s0_full` = 0,018034202, `s0_nominal` = 0,018057366; 5σ em 869,416 d full-reactor ⟹ 31/03/2028 (nominal 29/03/2028); D90 em 2031,675 d ⟹ 19/09/2031.
- **Não parte do orçamento de sistemáticas do artigo de 207 dias.** As datas 31/03/2028 e 19/09/2031 saem da decomposição do PROJETO (Tabela 6: σ = 0,074 em 100 d; 0,024 em seis anos), com piso ajustado para fechar 0,024. O orçamento do artigo de 207 dias (volume 0,96 %, eficiência 1,4 %, espectro 1,2 %…) é citado em `:213` e não entra em conta. A leitura a partir do artigo de 207 dias é a SEM PISO (2029/2031) ou o piso de dois pontos (inalcançável, `s0` = 0,052588, que reproduzi).
- **O brinquedo do projeto contradiz o único ponto real:** com os parâmetros dele σ(207,2 d) seria 0,0525 e σ(59,1 d) 0,0941; o publicado é 0,078 (×1,49) e 0,12 (×1,28). Reproduzi. `:216-258` mostra o 1,517 de §4.1 e não o repete em §4.3.
- Os 207,2 dias são «dias efetivos»; em 265 dias de calendário (26/08/2025 a 18/05/2026) são 78 % de duty cycle; as datas «ideais» a 100 % são limites inferiores (com 78 %: 5σ sem piso ≈ 13/07/2030; D90 ≈ 08/05/2033 [DERIVED]). O documento põe isso numa nota de rodapé (`:224`).
- **Marcação como brinquedo:** grep de `31/03/2028|19/09/2031|29/03/2028` em todos os arquivos de topo do túnel: `ENTREGA_K04.md:9`, `DEPOSITO_K04.md`, `REGISTRO_MAPA_K04.json`, `ERRATA_M2_K04_R2:64-65`, `ERRATA_M2_K04_R3:56-57`, `ERRATA_NEUTRINO…:42-43`, `M2_DESFECHOS…:253-254`. **Em todos há «brinquedo» e/ou «não cronograma».** Sem violação. Mas **C9:** a linha de calendário da ENTREGA e do DEPÓSITO leva só o brinquedo do projeto (2028/2031); a leitura que a ordem pediu (a partir do artigo de 207 dias) não está no resumo, e é a mais pessimista.

## 8. Item 7 — «com S ABSENT e a regra atual, um teste que não pode devolver o negativo não é teste»

Segue, **para FALSIFIED**: com S ausente nenhuma linha da escada acumula dois grupos autônomos ≥ 5σ. A frase vem condicionada («condicionalmente à regra e ao desenho») e o documento não afirma o universal falso: bem.
**Desfechos alcançáveis que o documento esqueceu ou descreve errado:**
1. **TENSION pelo reflexo global**, hoje na borda: NuFIT 6.1 (tabela) 3,02σ; Bari 2,86σ; Capozzi 2,44σ; core 2,95σ. É desfecho alcançável sem S e sem P (C2).
2. **O primário ≥ 5 sem S já tem nome no código: TENSION** (+ campo). O documento chama de lacuna aberta e a PERGUNTA_K04.md l.13 pergunta ao operador se «passa a TENSION» — o código já faz isso (C1).
3. **MATCHED não existe no código**; «MATCHED alcançável por S» (§3.1, §8) é sobre uma saída que a função não tem; o texto da regra sim.
A frase certa para o operador: «com a regra e o código selados, o canal só devolve ARMED_CONSISTENT ou TENSION; FALSIFIED exige duas determinações autônomas ≥ 5σ, e a única candidata hoje (SK-Gd) exige que a anomalia dele persista; MATCHED não tem ramo no código». Isto é parede medida, não falsificação, e vale dito sem suavizar.

## 9. Item 8 — a errata para a v412 (`ERRATA_NEUTRINO_V412_RASCUNHO_K04.md`)

**Fiel ao core nos números** (lidos por script de `neutrino_m2.values` e `checks`): 2,206054 e 1,937997 (JUNO), 2,952854 (NuFIT), 0,7842905784 %, `projecao_2031_sigma` = 7,842905784155273 e o centro 8,677557259966656 meV; a conta do 7,84 (0,5 % em Δm² = 0,25 % em m₂) reproduz. **Vai AO LADO** (blocos «ERRATA AO LADO», o core não é tocado): sim. A premissa da projeção (centro parado) está dita: sim.
**Não pode ser instalada como está; falta:**
- **C1/C2/C3:** o §4 (`:49-51`) e o §5 (`:55-57`) repetem `UNDER/ARMED`, `SINGLE_P/OPEN_RULE_GAP` e «estado documental ARMED_CONSISTENT» sem a regra do código, sem a borda de 3σ do NuFIT e sem a seq 93/142 do Mapa. O §6 (`:63-65`) leva as probabilidades de C4.
- **C10 (forma):** 6 ocorrências de `kimi-cite://…` (`:14,16,26,28,51,59`) são marcadores da ferramenta do Kimi, não referências instaláveis. As aspas «linha de morte dentro da meta de projeto» (`:18`) e “a meta de 0,5 %” (`:20`) NÃO são trechos verbatim do core (o `theorem` diz «A linha de morte de 5 sigma esta dentro da meta de projeto do JUNO (~2031)»; `checks[2]`: «linha de morte: 5 sigma quando Dm2_21 for medido a 0.78% (JUNO projeta 0,5%, ~2031)»); «a tensão cresce com a precisão» e «a regra hasheada julga as próximas medidas» conferem (core sem acentos). Assinatura: o rascunho diz «rascunho K04 R3»; ao instalar, a errata é da gerência, em nome próprio.
- **Mecânica da instalação (não dita):** «a escada datada ganha o degrau» é mudança de CÓDIGO em `prove_neutrino_m2` (a lista `dets`), não só texto: `tensao_atual = escada[-1]` (a linha de baixo passaria a ser o JUNO e o 2,95 deixaria de ser a tensão do canal e o veredito leria 1,94), `um.py:284323` lê `escada_datada[1]` como o JUNO, e o registro `neutrino_m2_perito_v392` confere «a escada tem 3 linhas» e `m2_juno_sigma = 2,206`. Uma errata AO LADO pura (texto) não resolve esses leitores; é decisão da gerência se a escada muda ou se o degrau fica ao lado só como texto.
- **C11:** o §3 afirma «a fonte converte 100 dias nominais em ≈ 92 dias full-reactor, seis anos em 2009 e vinte em 6696» citando arXiv:2204.13249. Os valores são constantes no script (`medidas_planejamento.py:229`) e o trecho citado como âncora (kimi-cite «will be determined to better than 0.5% precision in six years») não os sustenta; a REVISAO_K01 não localizou essa definição. **Não conferi** (sem consulta restante). Se não se confirmar, as datas do §3 mudam.
- A «escala dos 207 dias»: a errata chama o 207 d de «perito autônomo atual»; a R3 de 02/10 ratificou o JUNO como perito, não «59 dias»: razoável, mas é decisão de gerência marcar a troca (o perito v392 diz 59 dias nos `limites`).

## 10. Item 9 — nada foi aberto [REAL]

Grep em `K04\M2` (scripts atuais, REV0, REV1) por `executar_abertura|np.load|numpy|read_csv|.fits|.npy|.npz|h5py|astropy|pandas|open(|read_text|urlopen|requests|subprocess|work.h0dn_bg1`: só `medidas_planejamento.py` (importa `math`, `json`, `datetime`, `pathlib`; lê UM JSON de agregados, `determinacoes_m2_30out.json`, `read_text` em `:287`) e `extrair_contexto_juno.py` (`urlopen` de PDFs de artigos arXiv, em memória, `pypdf`; é leitura bibliográfica, não vetor de dado). `executar_abertura_v411` aparece só em texto de negação (ENTREGA_K04:41, RESSALVAS_K04:3,27,236, REGISTRO_MAPA_K04 `nao_refazer`). Nenhum script chama o rito. Os hashes de `ENTREGA_K04.md`, `REGISTRO_MAPA_K04.json` e `VALIDACAO_K04.json` conferem com o DEPOSITO_K04.md; o sha256 do core citado (`36c69fc7…`) confere.

## 11. TAREFA FIXA — atribuições ao operador

Nos cinco arquivos revisados não há fala atribuída ao operador entre aspas nem «o operador disse/pediu/ratificou/concordou». As ocorrências de «operador» são procedimentais («emenda… ato do operador») e as aspas citam o core (conferidas por bytes, item 9 acima) ou rótulos do próprio Kimi. **Nenhuma atribuição para listar.** Conferi por bytes as citações a arquivos: `determinacoes_m2_30out.json` contém `"z_sigma": 1.9379969609289271` e `"exposicao_adicional_dias": 380.07855357458413`; a memória `e0-cadeia-conferencia-kimi-e-no-go-31out.md` l.10 traz «dez determinações públicas (JUNO 207 d 1,94σ … SK-Gd 3,61σ…)» (sustenta «esta casa leu o 1,94σ em 30–31/10»); REVISAO_K01 l.47 = «B3». **Não fecha:** a âncora `PRE_REGISTRO_CEGO_RASCUNHO_K01.md l.36` é citada com o texto «propagação σ_m₂ ≈ σ(Δm²₂₁)/(2m₂)» (`M2_DESFECHOS…:55`); a linha 36 existe e fala dessa propagação, mas o texto exato é `σ_m₂ ≈ σ(Δm²₂₁)/(2m₂)` precedido de «propagação `»; a diferença é de formatação, só aviso. Registre-se também: a memória citada (l.19) já diz «regra do posto antes de JUNO-only/SK-Gd».

## 12. O que conferi, como, e o que NÃO conferi

**Conferi:** regra e código por script/leitura (core, `um.py` 4588-4704, original de 08/08); todas as razões r, D, σ de 5σ/D90, incremento, SK-Gd, calendário (script `rev_numeros.py`); a tabela de desfechos por forma fechada e MC, com reprodução do defeito (`rev_desfechos.py`); MATCHED (`rev_matched.py`); faixa de C e cenário SK-Gd (`rev_extras.py`); os lados do erro do NuFIT 6.1 contra a tabela oficial guardada pelo Mapa; o pino de 08/08; fontes SK-Gd, SNO+ v4, KamLAND; item 9 e a tarefa fixa. Saídas em `scripts_k04_m2\`.
**NÃO conferi:** o 92/2009/6696 (C11); os percentuais da Tabela II–III do artigo de 207 dias; Capozzi, Bari 2026.a, solares, Hyper-K, DUNE, DESI; a data dos slides de julho/2026 (C6); se existe liberação do JUNO posterior (negativo fraco); a independência física de qualquer par; os documentos COMBINACAO, HUBBLE e RESSALVAS (fora do meu recorte). Não rodei `session_memory`/ACOM por ordem de só leitura.

NOT_FALSIFIED não é CONFIRMED; o gate não se move; esta revisão não credita nem descredita a teoria.
