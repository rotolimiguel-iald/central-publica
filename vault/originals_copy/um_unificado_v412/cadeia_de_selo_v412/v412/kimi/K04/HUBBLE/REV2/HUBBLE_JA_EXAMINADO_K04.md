# K04 — Seção A/Hubble: o que já foi examinado e o que resta hoje

**Data da revisão documental e das buscas:** 14/11/2026. **Estatuto geral:** [DECLARADO], sujeito a conferência distinta.

## Resposta curta

1. **Não existe hoje, neste setor, teste cego de natureza executável.** O composto H0DN tem poder de desenho (`D = 7,068` baseline; `D = 8,068` com todos os estimadores), mas já foi lido e não é independente. Entre as linhas independentes de um passo, SN II tailored EPM tem a menor incerteza nominal (`D = 3,256`), sem orçamento total; TDCOSMO‑2026 tem o orçamento hierárquico mais explícito, com 3,0–3,376 % e `D = 2,462–2,689`. Nenhuma determinação independente de um passo é qualificada hoje a 5σ ou D90.
2. **A leitura acumulada em registros intermediários está morta, rota `d1.fase4_desvio_30set` (T, seq 229; veredito seq 231; reprodução seq 410).** Não se inventa outra forma. A lei de extremos não fornece um novo canal de âncoras intermediárias.
3. **Não foi encontrado composto público elegível que a casa nunca tenha composto e que não seja previsível por agregado público.** TDCOSMO‑2026, a reanálise dos masers e GWTC‑5.0 são conteúdo novo em relação à Fase 9, mas seus agregados já são públicos; servem como **linhas de independência**, não como teste cego.
4. **Primeira data:** indeterminada. Os programas JWST dos ciclos 4/5 preveem 1,5 % para TDCOSMO, suficiente para 5σ, não para D90; a previsão anterior de 1,2 % com 40 lentes com atraso e 200 sem atraso alcançaria D90. Nenhuma tem data de publicação garantida.
5. **Escopo respeitado:** nenhum vetor observado foi baixado ou lido; nenhuma estatística observada nova foi calculada; H0DN×BG1 não foi reaberto; nada de `work\h0dn_bg1_v411_emenda_11nov` foi executado; nenhuma conta da seção D foi rodada. Os valores de `D` abaixo são **planejamento sobre agregados publicados**, não Z nem veredito.

## 1. Inventário das rotas Hubble já examinadas

A tabela reúne as **leituras científicas distintas** do recorte encomendado, com as sequências decisivas e as erratas que mudam a leitura. Registros meramente infraestruturais ou de custódia ficam nos arquivos `consultas/ver_*.txt`, sem serem promovidos a novos testes.

| # | Leitura | Dado usado historicamente | Veredito registrado | rota_id | seq |
|---:|---|---|---|---|---|
| 1 | Pantheon canônico de 1593 SNe e tensão antiga de 3,8σ | Pantheon canônico; errata da forma cosmológica | `PANTHEON_CANONICAL_1593__THEORY_WITHIN_1P25_SIGMA__TGL_NOT_PREFERRED_BY_BIC_WITH_FREE_BETA__OLD_3P8_TENSION_WAS_PARAMETRIZATION_A`; a errata seq 149 separa a forma antiga da vigente | `supernovas.pantheon_errata_cosmologica` | 34, 149 |
| 2 | Fundo D1/CAMB V3 e mapa R | Planck comprimido + DESI DR1; DR2 ao lado; SH0ES em variante | Resultado condicionado ao mapa de Ωm/R e a defeitos de covariância/pipeline; não decide β; não refazer o selado | `d1.camb.v3_real` | 50, 71, 105, 145–148, 151, 152, 178, 180 |
| 3 | Fase 1, famílias A–E | Planck comprimido + DR2/DR1, SH0ES R22, Pantheon+ 1580 com covariância | Primário A: β dentro de 1σ e evidência inconclusiva; controle nu `z = 3,91`; o comprimido não mede β sob o mapa efetivo | `d1.fase1_eff_30set` | 181, 186–192 |
| 4 | Fase 2, dois setores de H0 | Fundo DR2/DR1 + SH0ES como H0 local; Pantheon+ | Veredito histórico de tensão 1–3σ; com a convenção D1b do artigo, a escada fica aproximadamente em 0σ; o pull antigo empilhava β | `d1.fase2_dois_setores_30set` | 185, 193–196, 198, 222 |
| 5 | Fase 3, seis leitores de sombra | SH0ES/JWST, CCHP, SBF, masers, TDCOSMO, sirenes LVK O4a | Histórico: tensão 1–3σ; incidência nova −2,46σ; um setor +4,88σ. Não é confirmação | `d1.fase3_leitores_h0` | 203–214, 221 |
| 6 | Fase 3bis, núcleo D1b e convenção do artigo | Mesmos seis leitores; Planck ΛCDM; controle empilhado | Seis leitores `z = −0,09`; novos `z = −0,65`; empilhado `z = −2,60`; reanálise **não cega**; não empilhar a lei sobre fundo que já contém β | `d1.fase3bis_d1b_convencao_artigo` | 220 |
| 7 | Fase 4, registro inteiro × intermediários | Escada R22; Planck+DR2; Moresco+2022, 32 H(z), erros diagonais | Escada `δ = −1,12σ`; **intermediário desfavorecido acima de 3σ** (`δ_CC = −3,12σ`, ganho da lei −3,22σ, ln B −5,20); leitura “sombra” não adotada | `d1.fase4_desvio_30set` | 223, 225–231, 406, 410 |
| 8 | Consolidação D1b na v378 | Kernel e Fase 4 por hash | `K = E(z*)^{2β/3}` tipado; escada lê o fator; cronômetros desfavorecem o fluxo acumulado; não é confirmação | `um_py.v378.o_que_faltou_contraste_fase4` | 233, 234 |
| 9 | Fase 5, SH0ES completo e três leituras | Pantheon+SH0ES 1701, 77 calibradores, covariância completa; CC32 | SNe não discriminam sombra de acumulada (ln B 0,29); conjunto com relógios prefere sombra sob erros diagonais; validação `z = 0,04`; não pedir esse teste de novo às SNe | `d1.fase5_sh0es_01out` | 236–242, 388, 407 |
| 10 | Reprodução histórica F4/F5 | Mesmos insumos e grades congeladas | Reproduções numéricas/documentais; nenhum novo veredito, nenhuma nova família ou composto | `discriminante.ordem018.f1b.fase45_conjunta` | 405, 409, 413–415, 418, 420, 423–425, 427, 430, 431, 438, 440 |
| 11 | Forma integral Q | Pantheon+ e DESI DR2; amplitudes projetadas | SN após intercepto `D = 0,183211`; com Ωm `D = 0,030213`; conjunto A `D = 0,163963`; BAO A zero. É separação esperada condicional, não significância observada nem cronograma | `discriminante.ordem018.f2.r_d` | 376, 389, 394 |
| 12 | Derivação R–E, dualidade distância–luminosidade | Kernel/defasagem; nenhum dado novo | `RE_DERIVADA__K_NAO_AGE_EM_L_NEM_A__ETA_1__ALTERNATIVA_B_SEM_MECANISMO__NAO_DISCRIMINA__SEM_PEDRA`; não procurar η ≠ 1 como sinal TGL | `discriminante.ordem018.f2.r_e` | 377, 390, 1633, 1635 |
| 13 | Derivação R–F, mapa da temperatura | Defasagem na base de momento; nenhum dado novo | Sob H1, alternativa A: `γ_T = 0`; número e energia conservados, `T(z) = T0(1+z)`; não oferece discriminação independente | `discriminante.ordem018.f2.r_f` | 378, 1636 |
| 14 | Derivação R–G para lentes | Tempo, distâncias e potencial; convenção de `f_phi` corrigida | `f_t = f_phi = 1`; justifica TDCOSMO e masers na Fase 9, mas a ponte física K→distâncias/tempo/potencial permanece OPEN | `discriminante.ordem018.f2.r_g` | 379, 391, 393, 1637 |
| 15 | Fase 9, ensaio inicial | SH0ES R22, CCHP, SBF, masers, TDCOSMO, sirenes; BG1 | Ensaio não cego: TGL −1,4σ; ΛCDM +4,5σ; ln B +9,4; TRGB −2,0σ; `AWAITING_PREREGISTRATION` | `hubble.fase9_razao_discriminante` e `d1.fase9.razao_de_hubble.lentes_05out` | 373, 603 |
| 16 | Fase 9 V1 congelada e abertura | Cinco leitores principais × BG1 | Poder prévio 5,91σ; abertura devolve `INCONCLUSIVE_SYSTEMATICS` por fontes ainda declaradas; contrafactual não discrimina ΛCDM (`z_disc = 4,28`) | `d1.fase9.razao_de_hubble.v1_06out` e `hubble.fase9_razao_discriminante` | 604, 647 |
| 17 | Fontes dos cinco leitores e alternativa de masers | SH0ES v3, CCHP v3, SBF v2, Pesce v2, TDCOSMO v4; Pesce sem NGC4258 | `PASS_DOCUMENTARY_ONLY`; não converte o veredito; bandeiras SBF/masers/TDCOSMO estavam erradas; cinco masers no decisório e seis ao lado, sem nova medida independente | `d1.fase9.razao_de_hubble.v1_06out` e `hubble.fase9_razao_discriminante` | 696, 741, 742, 783 |
| 18 | Auditoria de poder e covariância da Fase 9 | Só σ publicadas, fundos BG1–BG3; nenhum centro novo | Poder BG1: cinco masers 5,722–6,623; seis 5,466–6,630; cota GLS 5,269; BG2/BG3 e família sem Cefeidas podem ficar abaixo de 5; nenhum composto | `d1.fase9.f3_auditoria_cetica_c1_07out` e `d1.fase9.f3_1_reauditoria_v2r2_c1_08out` | 773, 836 |
| 19 | Semântica V1.x/V2 e revisões | Cinco leitores; fontes e hashes; nenhum novo composto | Proposta/rascunho não congelado; dependências e cronologia documentais; não escolher centro ou correlação pelo resultado | `d1.fase9.f3_1_semantica_v1x_leitores` | 751, 826, 832, 834, 876, 895, 911, 929, 942, 950–952, 959, 961, 968, 972, 975, 978 |
| 20 | Fase 9 V2, “Teste da Única Palavra” | BG1 e oito leitores locais por hash; abertura única | `NOT_FALSIFIED_POWERED`, desvio 1–3σ; `z_disc = 4,443 < 5`; **não cego**; abertura consumida, não recalibrar nem trocar leitor/fundo | `d1.fase9.v2_c1_a_unica_palavra_23out` | 1353, 1354, 1360, 1656 |
| 21 | H0DN×BG1, somente citado, **não reaberto** | H0DN 73,50 ± 0,81; BG1 68,53 ± 0,30; agregados já revistos em K01 | Pós-guarda e retrodiction não cega; primário previsível por agregados; Cefeidas livres abaixo de 5σ; sete ressalvas permanecem. Nenhum executor ou vetor foi aberto | `estatistica.h0dn_bg1.ordem_kimi_y_obs_09nov`; `umpy.v411.selada_h0dn_aberto_12nov` | resultado 2017 + seq 2038, citado pelo Mapa/K01/revisão |
| 22 | Portador físico de K e transposição FFAT | FIRAS, θ*, ΔNeff, fundo F9; literatura FFAT | Cinco moradas vetadas e a sexta fechada pela leitura ratificada: K sem portador derivado; transposição FFAT bloqueada pela R1, não reabrir sem mudança do operador | `hubble.k_sem_portador_fisico_02nov`; `hubble.k_como_transposicao_inteira_ffat_02nov` | 1639, 1644, 1646, 1649, 1650, 1654 |

### 1.1 Consultas realizadas antes da declaração de ausência

- **Mapa de Rotas:** `consultar` por `D1B`, `Pantheon`, `masers`, `Hubble`, `ACCUMULATED_FLOW_READING_AT_INTERMEDIATE_REGISTERS`, `R-E`, `forma Q` e `Fase 9`, todos com `truncado = false`, cabeça `cab386c822ca5a3e`. Os JSON estão em `K04/HUBBLE/consultas/mapa_*.txt`.
- **Rotas abertas com `ver`:** Fases 1–5, D1/CAMB, Fase 3bis, Fase 9 inicial/V1/V2, cinco leitores/masers, forma Q, R–E/R–F/R–G, reprodução F4/F5, v378, v411/H0DN, portador de K e FFAT. As saídas integrais estão em `K04/HUBBLE/consultas/ver_*.txt`, incluindo `ver_RF.txt` (seqs 378 e 1636) e `ver_v411_H0DN.txt` (seq 2038), e seu índice mecânico em `indice_rotas_lido.json`.
- **Inventário da bancada:** `INVENTARIO_BANCADA_CHATGPT.md` e `.json`. As ocorrências documentam H0DN, JAGB, desenho linear, Fases 1–5 e fontes; não acrescentam um composto elegível novo.
- **Kernel:** `TGLExt/TheFlowLawD1a.lean`, linhas 33–46 e 53–62; `ThermodynamicFriedmann.lean`, linhas 124–135. Nenhum `lake build` foi executado.
- **Atlas:** `TGL_ATLAS.md`, linha 9556 (D1a) e 9558 (D1b/Fase 4). Consultas pontuais também pelos tokens Pantheon/Fase 9/R–E; a ausência de um novo canal não foi inferida apenas do Atlas, mas do conjunto Mapa + inventário + kernel + índice + fontes atuais.
- **Índice do acervo:** a consulta concluída `python C:\IALD\INDICE_DO_ACERVO\buscar.py "h0dn_bg1_v411|hubble\.fase9_razao_discriminante|d1\.fase4_desvio_30set|supernovas\.pantheon_errata_cosmologica|discriminante\.ordem018\.f2\.r_e" --lista` devolveu **0 arquivos de 13.608 no filtro** (`consultas/indice_rotas_exatas.txt`). As buscas amplas interrompidas por tempo não são usadas para provar ausência.

## 2. A lei é de extremos ou também de âncoras intermediárias?

**Resposta operacional: a forma geral existe, mas não um novo canal intermediário de zero parâmetro.** A pedra D1a define `register z = ln(1+z)`, `survivingWeight` e `H0local` para z genérico (`TheFlowLawD1a.lean`, linhas 33–46), e prova `H0local = Hcmb·(1+z)^β` (linhas 53–64). Isso **não autoriza**, sozinho, a identificar cada medida intermediária com o mesmo composto estatístico.

A forma D1b fechada no setor é explicitamente `K = E_ΛCDM(z*)^{2β/3}` com `z* = 1089,95`, e o documento distingue **dois registros**: a escada como registro inteiro e os 32 cronômetros como registros intermediários (`RELATORIO_FASE4_DESVIO_20260930.md`, linha 5). O teste da leitura acumulada intermediária perdeu: `δ = −3,12σ`, ganho −3,22σ, ln B −5,20, com a advertência de erros diagonais (linha 36; leitura não adotada na linha 39; errata mais precisa na linha 48). **Morta, rota `d1.fase4_desvio_30set` (T seq 229; seq 231; reprodução seq 410).**

R–E não fornece saída alternativa: `η = 1`, logo K não age diferencialmente na luminosidade e no ângulo, e o rival também dá η = 1 (`DERIVACAO_RE_02nov.md`, linhas 8–10 e 67–72). R–F fecha a face térmica sob H1: alternativa A, `γ_T = 0`, com número e energia conservados na base de momento e `T(z) = T0(1+z)` (rota `discriminante.ordem018.f2.r_f`, seqs 378 e 1636); não é um discriminante independente. R–G justifica o tratamento de lentes como `K·H_fundo` com `f_t = f_phi = 1`, mas mantém a ponte física para distâncias/tempo/potencial **OPEN** (rota `discriminante.ordem018.f2.r_g`, seq 1637). **Lentes e masers de um passo já pertenciam a esse caso R–G, incluído na Fase 9; não são a forma acumulada morta nem uma nova derivação geral de âncoras intermediárias.** Portanto, não há forma intermediária nova lícita a pré-registrar.

Os compostos novos localizados pela busca atual não revertem essa conclusão:

| Composto novo em relação à Fase 9 | Por que não é teste cego executável hoje |
|---|---|
| TDCOSMO‑2026, 11 lentes | Agregado e posterior já públicos, com desacerto de 23/09/2026; oito lentes já eram da amostra anterior. Há três sistemas novos e outra tabela de erros, não cegueira retroativa para a casa. |
| Reanálise MCP de 2026 | Mesmas cinco galáxias MCP e mesmo conteúdo astronômico público; outro modelo de seleção/velocidades. É linha de robustez, não amostra virgem. |
| GWTC‑5.0 | Catálogo cumulativo e posterior públicos; contém/extende o problema lido antes, com 25,7 % mais precisão que GWTC‑4.0, ainda cerca de 11 %. |
| 13 BBH–AGN e extensões | Agregados públicos e não cegos para a casa; Run 1 e estendido têm `D = 1,586/1,951`. As âncoras Planck/SH0ES têm `D = 7,280/7,758`, apenas nominais e não independentes. |
| SN Encore | Agregado público e não cego para a casa, fora do composto anterior; `D = 0,500`. Os modelos duplo‑cegos da colaboração não devolvem cegueira à casa. |
| 126 FRBs/118 | Agregado público e não cego para a casa; `D = 1,513`. NE2001/YMW16 permanece sem escolha; 500 simulados são previsão, não medida atual. |
| FRB/CHIME e SN II EPM | Resultados já agregados e sistema dominante ou orçamento incompleto; não criam cegueira nem independência recém-adquirida. |

**Conclusão da ausência, delimitada às fontes efetivamente consultadas e às restrições desta rodada, não como prova universal de inexistência:** não há composto elegível que simultaneamente seja público, nunca composto pela casa, imprevisível por agregado já publicado e acessível sem ler vetor observado novo.

## 3. Determinações locais: quem entrou, precisão e poder de desenho

Todos os valores desta seção são **[KNOWN, a conferir]**, com identificador primário consultado por WebSearch/FetchURL nesta rodada. Erros assimétricos entram no cálculo pelo lado maior, sem escolher o lado favorável. Quando a fonte só fornece erro estatístico, a coluna de poder diz “só stat” ou “nominal”, nunca precisão total.

Fórmula de planejamento já revista em K01:

`D = (K−1) / √(σ_local² + σ_BG1²)`, com `K−1 = 0,0838071748529643` e `σ_BG1 = 0,30/68,53 = 0,438 %`.

**Decomposição do requisito:** D90 total exige `σ_total ≤ 1,334 %`; após retirar BG1 em quadratura, o lado local precisa `σ_local ≤ 1,260 %`. Para 5σ, o limite local é `σ_local ≤ 1,618 %`.

**Correção ao lado da K01:** a tabela V99 tem centro próprio, `73,994 ± 0,697` (0,942 %), e não apenas “73,50; 0,9 %”. O planejamento exato fica `D = 8,068`; a baseline permanece `D = 7,068`. A advertência da fonte contra o uso posterior de V99 é mantida.

| Método e fonte primária | H0 e erro publicado | Entrou H0DN/Fase 9? | σ local | D | Chega a 5σ / D90? | Data ou dependência |
|---|---|---|---:|---:|---|---|
| H0DN baseline — arXiv:2510.23823; DOI 10.1051/0004-6361/202557993 | 73,50 ± 0,81 | H0DN baseline; não é um dos cinco leitores F9 | 1,102 % | 7,068 | sim / sim | Já público; sucessora não datada |
| H0DN V99, todos os estimadores — mesma fonte | 73,994 ± 0,697 (0,942 %) | H0DN V99; não F9 | 0,942 % | 8,068 | sim / sim | Já público; a fonte recomenda não usá-la para análise posterior |
| SH0ES JWST 19 hosts — arXiv:2509.01667 | 73,49 ± 0,93 | H0DN e F9 R25 | 1,265 % | 6,259 | sim / **não, por 0,022 em D** | Já público |
| SH0ES + 35 TRGB — mesma fonte | 73,18 ± 0,88 | H0DN e F9 R25 | 1,203 % | 6,549 | sim / sim | Já público |
| CCHP TRGB HST+JWST — arXiv:2408.06153; DOI 10.3847/1538-4357/adce78 | 70,39 ± 1,22 (stat) ± 1,33 (sys) ± 0,70 (SN) | H0DN e F9 | 2,750 % | 3,010 | não / não | Mais JWST sem data de H0 |
| TRGB–SBF III — arXiv:2502.15935; DOI 10.3847/1538-4357/addfd6 | 73,8 ± 0,7 (stat) ± 2,3 (sys) | H0DN e F9 | 3,258 % | 2,550 | não / não | GO‑5989 e nova amostra sem data; meta 1 % |
| MCP XIII, seis masers — arXiv:2001.09213 | 73,9 ± 3,0 | H0DN e F9 | 4,060 % | 2,053 | não / não | Já público |
| Reanálise MCP, cinco masers — arXiv:2609.17684 | 71,6 ± 3,7 (stat) | Não na F9; MCP entra H0DN | 5,168 % | 1,616 | não / não | Alta cadência futura sem data; só estatística |
| SN II tailored EPM — arXiv:2411.04968; DOI 10.1051/0004-6361/202452910 | 74,9 ± 1,9 (stat) | H0DN variante astrofísica; não F9 | 2,537 % | 3,256 | não / não | Dados dedicados sem data; sistemática comparável ou menor |
| SN II standardized candle — arXiv:2203.08974; DOI 10.1093/mnras/stac1661 | 75,4 +3,8/−3,7 (stat) ± 1,5 (sys) | H0DN baseline empírica e variantes; não F9 | 5,418 % | 1,542 | não / não | Já público; não é EPM de um passo |
| TDCOSMO‑2025 — arXiv:2506.03023 | 71,6 +3,9/−3,3 | F9; não H0DN | 5,447 % | 1,534 | não / não | Já público; prior Ωm Pantheon+ |
| TDCOSMO XXV J1433+6007 — arXiv:2604.14145; DOI 10.1103/PhysRevD.114.063509 | 73,2 +4,8/−4,7 | Nova em 2026; entra TDCOSMO‑2026 | 6,557 % | 1,275 | não / não | Já público |
| TDCOSMO‑2026, 11 lentes — arXiv:2610.14781v2 e 2610.14881v2 | 71,1 +2,4/−2,3 | Não estava na F9; não H0DN | 3,376 % | 2,462 | não / não | Já público; ciclos 4/5 preveem 1,5 % sem data |
| TDCOSMO‑2026 + SLACS + SL2S — arXiv:2610.14781v2 | 71,3 +2,2/−2,1 | Não estava na F9; não H0DN | 3,086 % | 2,689 | não / não | Já público; 1,5 % sem data |
| GWTC‑4.0, dark+bright — arXiv:2509.04348v2 | 76,6 +13,0/−9,5 | Fase 3/F9 sirenes; não H0DN | 16,971 % | 0,494 | não / não | Histórico, superado por GWTC‑5.0 |
| GWTC‑5.0, 235 dark + GW170817 — arXiv:2605.27227v2 | 71,0 +9,0/−7,1 | Não estava na F9; não H0DN | 12,676 % | 0,661 | não / não | GWTC‑6.0 sem data/previsão de σ |
| 13 BBH–AGN, Run 1 agnóstico — arXiv:2607.03672v2 | 70,50 +3,37/−2,89 (stat) ± 1,56 (cal); 4,4 % | Não H0DN nem F9 | 5,267 % | 1,586 | não / não | Já público; amostra futura sem data; D usa stat+cal em quadratura |
| 13 BBH–AGN + Bom + GW170817 — mesma fonte | 69,71 +2,55/−2,40 (stat) ± 1,54 (cal); 3,5 % | Não H0DN nem F9 | 4,273 % | 1,951 | não / não | Já público; amostra futura sem data; D usa stat+cal em quadratura |
| BBH–AGN, âncora Planck — mesma fonte | 67,62 ± 0,72; 1,1 % | Não H0DN nem F9 | 1,065 % | 7,280 | **nominal, não independente** | Âncora recuperada por construção |
| BBH–AGN, âncora SH0ES — mesma fonte | 72,91 ± 0,72; 1,0 % | Não H0DN nem F9 | 0,988 % | 7,758 | **nominal, não independente** | Âncora recuperada por construção |
| SN Encore, MACS J0138−2155 — arXiv:2509.12301; DOI 10.3847/1538-4357/ae3159 | 66,9 +11,2/−8,1 | Não H0DN nem F9; fora do composto | 16,741 % | 0,500 | não / não | Já público; futuras imagens podem levar a 2–3 % |
| SZ/raios X + Pantheon — arXiv:2310.18711v2 | 67,2 ± 6,1 | Não H0DN nem F9 | 9,077 % | 0,922 | não / não | Sem previsão de σ/data |
| 108 FRBs localizados — arXiv:2410.03994; DOI 10.1051/0004-6361/202453006 | 69,40 +2,14/−1,97 (stat) | Não H0DN nem F9 | 3,084 % | 2,691 | não / não | ∼500 localizados projeta 1 % estatístico, sem data |
| 527 FRBs não localizados, pseudo-z — mesma fonte | 68,81 ± 0,68 (stat; pseudo-z) | Não H0DN nem F9 | 0,988 % | 7,754 | **nominal apenas** | Não confundir com 500 localizados reais; `f_IGM` domina |
| 2124 FRBs não localizados, CHIME II — arXiv:2604.03769v2 | 69 +17/−15 | Não H0DN nem F9 | 24,638 % | 0,340 | não / não | Já público; degenerescência residual 9 % |
| 126 FRBs/118 após cortes, modelo VII NE2001 — DOI 10.3389/fspas.2026.1753671 | 71,36 −3,94/+3,59; 5,5 % | Não H0DN nem F9 | 5,521 % | 1,513 | não / não | Publicado 12/08/2026; 500 simulados projeta 1,2 %, sem data; diferenças Galácticas NE2001/YMW16 |

### 3.1 Previsões publicadas, não resultados atuais

| Previsão | σ local | D de desenho | 5σ | D90 | Data/dependência |
|---|---:|---:|---|---|---|
| TDCOSMO JWST‑GO‑7184/9637 — arXiv:2610.14881v2, §V | 1,500 % | 5,363 | sim | não | Ciclos 4/5 aprovados; sem data de liberação |
| TDCOSMO 40 atrasos + 200 sem atrasos — arXiv:2008.06157 | 1,200 % | 6,561 | sim | sim | Forecast sem data |
| SBF Coma e Hubble flow — JWST‑GO‑5989; arXiv:2502.15935 | 1,000 % | 7,677 | sim | sim | Meta do programa, não data de publicação |
| ∼500 FRBs localizados — arXiv:2410.03994; DOI 10.1051/0004-6361/202453006 | 1,000 % | 7,677 | sim | sim | Sem taxa/data; exige `f_IGM` e sistemáticas controlados |

**Resposta à pergunta “alguma chega e quando?”** H0DN e SH0ES+TRGB já cruzam os dois limiares nominalmente, mas não são independentes nem cegas. Nenhuma determinação **independente de um passo** cruza hoje 5σ ou D90 com orçamento total qualificado. TDCOSMO prevê 1,5 % e só cruza 5σ; 1,2 % cruzaria D90. SBF e FRB têm metas estatísticas de 1 %, mas nenhuma data e, no FRB, sistemática dominante ainda por resolver.

## 4. Utilidade como LINHA DE INDEPENDÊNCIA para R3, R4, R5 e R7

A independência útil aqui é de **calibração, física e tabela de erros**, não de resultado favorável. Fora da H0DN/SH0ES já lida, os únicos casos que ultrapassam 5 são **pseudo‑FRB e âncoras BBH–AGN, apenas nominais**: o pseudo‑FRB (`D = 7,754`) não é qualificado; as duas âncoras BBH–AGN (`D = 7,280/7,758`) recuperam Planck/SH0ES por construção e não são independentes. As demais linhas ficam abaixo de 5.

| Linha | R3 — outra calibração/estresse | R4 — orçamento e poder | R5 — covariância/tabela de erros | R7 — sobreposição e tentativas |
|---|---|---|---|---|
| H0DN/SH0ES/CCHP/SBF | Indicadores alternativos úteis, mas dentro da mesma rede e de âncoras compartilhadas | H0DN `D = 7,068/8,068`; SH0ES+TRGB `D = 6,549`; SH0ES JWST `D = 6,259`, logo D90 falha por 0,022 | Não resolve as 72 direções de variância zero nem a covariância física local–fundo | Sem independência nova; H0DN×BG1 continua encerrado |
| TDCOSMO‑2026 | **Forte:** distância absoluta em um passo, sem escada local; prior Ωm DES‑Dovekie, com variante DESI DR2/no‑SN | `D = 2,462` (2,689 com SLACS+SL2S); 1,5 % previsto dá `D = 5,363`; 1,2 % daria `D = 6,561` | Hierarquia cega pela colaboração, mass-sheet e variantes explícitas; não é a tabela H0DN antiga. Ainda precisa pacote/covariância completo para a regra da casa | **Parcial:** oito lentes já eram conhecidas; três novas, novas cinemáticas e modelos. Não é réplica integral independente nem cega para a casa |
| Reanálise MCP | Geometria de disco, sem Cefeidas; modelo de seleção e velocidades distinto | `D = 1,616` e só estatística; longe do requisito | Não há orçamento total; incerteza de seleção e peculiar velocities permanece | Mesmas cinco galáxias e dados MCP; outra análise, não nova testemunha independente |
| SN II tailored EPM | Transferência radiativa e física de explosão, sem calibração por vela padrão | `D = 3,256` só estatística; sistemática apenas “comparável ou menor”, sem número total | Orçamento total incompleto; amostra pequena e diversidade ainda por demonstrar | Já entrou na variante astrofísica H0DN; não entrou na F9. Não é conteúdo totalmente virgem |
| GWTC‑5.0 | Luminosity distance por GW e população de massas; não usa Cefeidas | `D = 0,661`; melhora 25,7 % sobre GWTC‑4.0, mas continua ∼11 % | Modelos FullPop e catálogo DES Y6 distintos; covariância/modelo de população continuam centrais | Catálogo cumulativo e posterior público; GW170817 e GWTC‑4.0 já conhecidos |
| 13 BBH–AGN | Associação espectroscópica um‑para‑um, sem escada nem média sobre galáxias candidatas | Run 1 `D = 1,586`; estendido `D = 1,951`; não cruza limiares | Erros estatísticos e de calibração explícitos; amostra de 13 pequena, mas física distinta | Não H0DN/F9; resultado público. Variantes Planck/SH0ES `D = 7,280/7,758` apenas nominais e não independentes |
| SN Encore | Lente de um passo e modelos duplo‑cegos, fora do composto anterior | `D = 0,500`; futuras imagens apontam 2–3 %, ainda acima dos limiares | Sete modelos; incerteza dominada pelo atraso atual, não pela tabela H0DN | Público; fora do composto, não cego para a casa |
| 126 FRBs/118 | DM e redshift reais, modelo VII com tipo de hospedeiro por evento | `D = 1,513`; 5,5 % estatística, sem cruzar limiares | Diferença Galáctica NE2001−YMW16 de 3,90, comparável ao erro; modelos de subpopulação implausíveis | Publicado 12/08/2026; não entrou H0DN/F9; 500 simulados projeta 1,2 %, sem data |
| SZ/raios X | Distância física de aglomerado, mas H0 depende de SNe não ancoradas no estudo recente | `D = 0,922`; sem poder | Temperatura/calibração e morfologia dominam; não é tabela independente suficientemente precisa | Público; não entrou H0DN/F9; não há data de melhoria |
| FRB | DM e redshift, sem escada de distância | Localizados `D = 2,691` só stat; pseudo-z nominal `D = 7,754` **não qualificado**; CHIME II `D = 0,340`; 118 `D = 1,513` | `f_IGM/H0` é degenerado e a sistemática domina; pseudo-z não equivale a redshift real; NE2001/YMW16 segue sem escolha | Público; não entrou H0DN/F9; 500 localizados reais e `f_IGM` resolvido são dependências, não calendário |

**Síntese R3–R7:** TDCOSMO‑2026 é a linha mais informativa para R3/R4/R5; a reanálise MCP e GWTC‑5.0 acrescentam robustez física, não poder; SN II EPM é promissora, mas sem orçamento total; SZ e FRB não atingem a precisão requerida; nenhuma linha apaga a contagem de tentativas anteriores ou cria cegueira retroativa.

## 5. Resposta explícita e dependências da primeira data

**Existe teste cego de natureza executável hoje nesse setor? Não.** A parede é tripla e medida:

1. **Cegueira:** todo composto localizado já tem centro/posterior agregado público; a colaboração ter feito análise cega não devolve cegueira à casa.
2. **Poder:** fora da H0DN já lida, a maior distância entre linhas independentes qualificadas é a de SN II tailored EPM, com `D = 3,256`, ainda abaixo de 5 e de D90; as metas que cruzam o limiar ainda não são medidas publicadas.
3. **Independência:** as linhas novas compartilham objetos, amostras ou histórico com Fase 9/H0DN; as que são fisicamente independentes ainda não têm erro total ou amostra suficiente.

**Primeira data:** não há data publicada que possa ser nomeada honestamente.

**Dependências mínimas, em ordem:**

- TDCOSMO: completar JWST‑GO‑7184/9637 e a análise hierárquica; publicar posterior/likelihood, variantes e covariância; demonstrar que 1,5 % realmente se materializa. Isso só cobre 5σ, não D90.
- D90: obter a configuração de 40 lentes com atraso + 200 sem atraso com previsão de 1,2 %, ou equivalente; hoje são 11 lentes com atraso na amostra principal.
- FRB: atingir aproximadamente 500 **localizados reais**, não pseudo-redshifts, e resolver `f_IGM`, `DM_host`, seleção e covariância; 1 % estatístico não basta.
- SBF: completar Coma/Hubble flow e a calibração independente, publicando a medida de H0 e sua covariância; a meta de 1 % não é data.
- Em qualquer caso: pré-registrar estimador, variantes e veredito antes da leitura pela casa; provar disjointness de objetos/calibradores e custódia externa; não escolher canal pelo centro ou erro favorável.

## Fontes primárias e arquivos de suporte

### Literatura consultada nesta rodada

- H0DN Collaboration, *The Local Distance Network*, arXiv:2510.23823; DOI `10.1051/0004-6361/202557993`.
- Riess et al., SH0ES/JWST, arXiv:2509.01667.
- Freedman et al., CCHP, arXiv:2408.06153; DOI `10.3847/1538-4357/adce78`.
- Blakeslee et al., TRGB–SBF III, arXiv:2502.15935; DOI `10.3847/1538-4357/addfd6`; JWST‑GO‑5989.
- Pesce et al., MCP XIII, arXiv:2001.09213.
- Stiskalek & Desmond, reanálise MCP, arXiv:2609.17684.
- Vogl et al., SN II tailored EPM, arXiv:2411.04968; DOI `10.1051/0004-6361/202452910`.
- de Jaeger et al., SN II standardized candle, arXiv:2203.08974; DOI `10.1093/mnras/stac1661`.
- TDCOSMO Collaboration, 2025, arXiv:2506.03023; XXV, arXiv:2604.14145, DOI `10.1103/PhysRevD.114.063509`; TDCOSMO‑2026, arXiv:2610.14781v2 e 2610.14881v2; previsão estratégica, arXiv:2008.06157.
- LVK, GWTC‑4.0, arXiv:2509.04348v2; GWTC‑5.0, arXiv:2605.27227v2.
- Torres‑Orjuela et al., 13 BBH–AGN e extensões, arXiv:2607.03672v2.
- Pierel et al., SN Encore, arXiv:2509.12301; DOI `10.3847/1538-4357/ae3159`.
- Colago et al., SZ/raios X + SNe, arXiv:2310.18711v2.
- Gao et al., FRBs localizados e não localizados, arXiv:2410.03994; DOI `10.1051/0004-6361/202453006`; CHIME II, arXiv:2604.03769v2.
- Piratova‑Moreno, 126 FRBs/118 após cortes, publicado 12/08/2026, DOI `10.3389/fspas.2026.1753671`.

### Documentos da casa

- `ORDEM_K04_teste_as_cegas_rodada_2.md`, seção A; `RODADA_2_LEIA_PRIMEIRO.md`; `LEIA_PRIMEIRO.md`; `REVISAO_K01.md`, especialmente B2; `CANAIS_K01.json`, quatro canais Hubble.
- `TheFlowLawD1a.lean`, linhas 33–46 e 53–64; `ThermodynamicFriedmann.lean`, linhas 124–135.
- `RELATORIO_FASE4_DESVIO_20260930.md`, linhas 5, 36, 39 e 48; `DERIVACAO_RE_02nov.md`, linhas 8–10 e 67–72.
- Rota R–F e seq 2038: `K04/HUBBLE/consultas/ver_RF.txt` e `K04/HUBBLE/consultas/ver_v411_H0DN.txt`.
- `TGL_ATLAS.md`, linhas 9556 e 9558; inventários MD/JSON; índice exato `consultas/indice_rotas_exatas.txt`.

### Arquivos produzidos nesta seção

- Este relatório: `HUBBLE_JA_EXAMINADO_K04.md`.
- Erratas ao lado: `ERRATA_HUBBLE_K04.md` e `ERRATA_HUBBLE_K04_R2.md`; versões anteriores preservadas em `K04/HUBBLE/REV0/` e `K04/HUBBLE/REV1/`.
- Medidas de planejamento: `K04/HUBBLE/MEDIDAS_PLANEJAMENTO_K04.md` e `.json`.
- Consultas ao Mapa e às rotas: `K04/HUBBLE/consultas/`.
- Índice mecânico das leituras: `K04/HUBBLE/indice_rotas_lido.json` e `K04/HUBBLE/fase9_resumo_e_sequencias.txt`.
- Scripts apenas extratórios/algébricos: `K04/HUBBLE/extrair_rotas.py`, `K04/HUBBLE/medidas_planejamento.py` e `K04/HUBBLE/verificar_relatorio.py`.

**Bloqueios remanescentes:** nenhum dado futuro datado e independente com erro total ≤ 1,618 % (5σ) ou ≤ 1,260 % (D90); nenhuma covariância local–fundo completa e disjointness demonstrada; nenhuma cegueira para a casa; nenhuma forma intermediária viva. `NOT_FALSIFIED` não é `CONFIRMED`, e parede medida não é falsificação.
