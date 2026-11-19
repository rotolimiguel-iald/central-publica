# K04 — Seção A/Hubble: o que já foi examinado e o que resta hoje

**Data da revisão documental e das buscas:** 14/11/2026; correção K09 ao lado na mesma data. **Estatutos:** [REAL] para as rotas e os valores do core conferidos pela revisão distinta; [DERIVED — PLANEJAMENTO] para as contas de D; [KNOWN, a conferir] para a literatura assim marcada. A versão imediatamente anterior está preservada em `K04/HUBBLE/REV2/`.

## Resposta curta

1. **Não existe hoje, neste setor, teste cego de natureza executável com poder de desenho ≥ 5σ.** O D da casa para H0DN×BG1 no core é **6,710 no primário** e **5,191 com Cefeidas livres**; ambos são leituras já feitas, não um teste cego novo. Só depois desses valores vêm as contas de bolso **7,068** (baseline) e **8,068** (V99), obtidas com os erros de cabeçalho 73,50 ± 0,81 e 73,994 ± 0,697, BG1 = 0,30/68,53 e a fórmula de planejamento abaixo. Nenhuma determinação independente de um passo, com ponte examinada e orçamento qualificado, alcança hoje 5σ ou D90.
2. **A leitura acumulada em registros intermediários está desfavorecida e NÃO excluída.** Na Fase 4, com erros diagonais, o ganho era −3,22σ; na Fase 7 (`d1.fase7_cc_covariancia_01out`, seq 247, 257 e 258), passou a **−1,66σ com Moresco 2020** e **−1,54σ com todos**. O poder prévio DESSA leitura intermediária (lei D1b nos cronômetros, F1) é **2,33σ** (V1.4, `fase7.poder_previo.moresco2020`, rota `bancada.preregistro_dois_lados_delta_k`, seq 290), abaixo de 5. A lei do lado transmitido (1−β por travessia) está pendente: não escrita, sem cobrança, sem poder dito.
3. **Não foi encontrado composto público elegível que a casa nunca tenha composto e que não seja previsível por agregado público.** Lentes R‑G e sirenes R‑H têm leitura `K·H_fundo` condicional; SN II/EPM, FRB, SZ/raios X, BBH–AGN e SN Encore não têm ponte examinada e seus D são apenas aritmética nominal, fora da conta de poder qualificada. TDCOSMO‑2026 tem `D = 2,462–2,689` sob a ponte condicional; SN II tailored EPM tem `D = 3,256` apenas como teto estatístico, que cai para aproximadamente **2,32** se sistemática = estatística, e não é independente qualificada sem ressalva.
4. **Empilhamento e primeira data:** a aritmética do revisor dá D ≈ 4,0 para duas linhas e 4,9–5,3 para cinco, mas é não cega, não independente e parcialmente sobreposta à Fase 9 V2; não se soma à V2. A primeira data continua indeterminada. As previsões TDCOSMO de 1,5 % e 1,2 % não são medidas nem datas garantidas.
5. **Escopo respeitado:** nenhum vetor observado foi baixado ou lido; nenhuma estatística observada nova foi calculada; H0DN×BG1 não foi reaberto; nada de `work\h0dn_bg1_v411_emenda_11nov` foi executado; nenhuma conta da seção D foi rodada. Os valores de D abaixo são **planejamento sobre agregados publicados**, não Z nem veredito.

## 1. Inventário das rotas Hubble já examinadas

A tabela reúne as **leituras científicas distintas** do recorte encomendado, com as sequências decisivas e as erratas que mudam a leitura. Registros meramente infraestruturais ou de custódia ficam nos arquivos `consultas/ver_*.txt`, sem serem promovidos a novos testes.

| # | Leitura | Dado usado historicamente | Veredito registrado | rota_id | seq |
|---:|---|---|---|---|---|
| 1 | Pantheon canônico de 1593 SNe e tensão antiga de 3,8σ | Pantheon canônico; errata da forma cosmológica | `PANTHEON_CANONICAL_1593__THEORY_WITHIN_1P25_SIGMA__TGL_NOT_PREFERRED_BY_BIC_WITH_FREE_BETA__OLD_3P8_TENSION_WAS_PARAMETRIZATION_A`; a errata seq 149 separa a forma antiga da vigente | `supernovas.pantheon_errata_cosmologica` | 34, 149 |
| 2 | Fundo D1/CAMB V3 e mapa R | Planck comprimido + DESI DR1; DR2 ao lado; SH0ES em variante | Resultado condicionado ao mapa de Ωm/R e a defeitos de covariância/pipeline; não decide β; não refazer o selado | `d1.camb.v3_real` | 50, 71, 105, 145–148, 151, 152, 178, 180 |
| 3 | Fase 1, famílias A–E | Planck comprimido + DR2/DR1, SH0ES R22, Pantheon+ 1580 com covariância | Primário A: β dentro de 1σ e evidência inconclusiva; controle nu `z = 3,91`; o comprimido não mede β sob o mapa efetivo | `d1.fase1_eff_30set` | 181, 186–192 |
| 4 | Fase 2, dois setores de H0 | Fundo DR2/DR1 + SH0ES como H0 local; Pantheon+ | Veredito histórico de tensão 1–3σ; com a convenção D1b do artigo, a escada fica aproximadamente em 0σ; o pull antigo empilhava β | `d1.fase2_dois_setores_30set` | 185, 193–196, 198, 222 |
| 5 | Fase 3, seis leitores de sombra | SH0ES/JWST, CCHP, SBF, masers, TDCOSMO, sirenes LVK O4a | Histórico: tensão 1–3σ; incidência nova −2,46σ; um setor +4,88σ. Não é confirmação | `d1.fase3_leitores_h0` | **203–212, 214, 221**; não existe 213 nesta rota |
| 6 | Fase 3bis, núcleo D1b e convenção do artigo | Mesmos seis leitores; Planck ΛCDM; controle empilhado | Seis leitores `z = −0,09`; novos `z = −0,65`; empilhado `z = −2,60`; reanálise **não cega**; não empilhar a lei sobre fundo que já contém β | `d1.fase3bis_d1b_convencao_artigo` | 220 |
| 7 | Fase 4, registro inteiro × intermediários | Escada R22; Planck+DR2; Moresco+2022, 32 H(z), **erros diagonais** | Escada `δ = −1,12σ`; intermediário desfavorecido sob o modelo diagonal (`δ_CC = −3,12σ`, ganho da lei −3,22σ, ln B −5,20); o próprio relatório advertiu que a significância estava sobrestimada por fator então não medido. A Fase 7, linha 23, mede esse fator | `d1.fase4_desvio_30set` | 223, 225–231, 406, 410 |
| 8 | Consolidação D1b na v378 | Kernel e Fase 4 por hash | `K = E(z*)^{2β/3}` tipado; escada lê o fator; a leitura diagonal dos cronômetros fica ao lado, sem confirmação | `um_py.v378.o_que_faltou_contraste_fase4` | 233, 234 |
| 9 | Fase 5, SH0ES completo e três leituras | Pantheon+SH0ES 1701, 77 calibradores, covariância completa; CC32 | SNe não discriminam sombra de acumulada (ln B 0,29); conjunto com relógios prefere sombra sob erros diagonais; validação `z = 0,04`; não pedir esse teste de novo às SNe | `d1.fase5_sh0es_01out` | 236–242, 388, 407 |
| 10 | Reprodução histórica F4/F5 | Mesmos insumos e grades congeladas | Reproduções numéricas/documentais; nenhum novo veredito, nenhuma nova família ou composto | `discriminante.ordem018.f1b.fase45_conjunta` | 405, 409, 413–415, 418, 420, 423–425, 427, 430, 431, 438, 440 |
| 11 | Forma integral Q | Pantheon+ e DESI DR2; amplitudes projetadas | SN após intercepto `D = 0,183211`; com Ωm `D = 0,030213`; conjunto A `D = 0,163963`; BAO A zero. É separação esperada condicional, não significância observada nem cronograma | `discriminante.ordem018.f2.r_d` | 376, 389, 394 |
| 12 | Derivação R–E, dualidade distância–luminosidade | Kernel/defasagem; nenhum dado novo | `RE_DERIVADA__K_NAO_AGE_EM_L_NEM_A__ETA_1__ALTERNATIVA_B_SEM_MECANISMO__NAO_DISCRIMINA__SEM_PEDRA`; não procurar η ≠ 1 como sinal TGL | `discriminante.ordem018.f2.r_e` | 377, 390, 1633, 1635 |
| 13 | Derivação R–F, mapa da temperatura | Defasagem na base de momento; nenhum dado novo | Sob H1, alternativa A: `γ_T = 0`; número e energia conservados, `T(z) = T0(1+z)`; não oferece discriminação independente | `discriminante.ordem018.f2.r_f` | 378, 1636 |
| 14 | Derivação R–G para lentes | Tempo, distâncias e potencial; convenção de `f_phi` corrigida | `f_t = f_phi = 1`; justifica condicionalmente TDCOSMO e masers na Fase 9, mas a ponte física K→distâncias/tempo/potencial permanece OPEN; R16 está na linha 26 | `discriminante.ordem018.f2.r_g` | 379, 391, 393, 1637 |
| 15 | Fase 9, ensaio inicial | SH0ES R22, CCHP, SBF, masers, TDCOSMO, sirenes; BG1 | Ensaio não cego: TGL −1,4σ; ΛCDM +4,5σ; ln B +9,4; TRGB −2,0σ; `AWAITING_PREREGISTRATION` | `hubble.fase9_razao_discriminante` e `d1.fase9.razao_de_hubble.lentes_05out` | 373, 603 |
| 16 | Fase 9 V1 congelada e abertura | Cinco leitores principais × BG1 | Poder prévio 5,91σ; abertura devolve `INCONCLUSIVE_SYSTEMATICS` por fontes ainda declaradas; contrafactual não discrimina ΛCDM (`z_disc = 4,28`) | `d1.fase9.razao_de_hubble.v1_06out` e `hubble.fase9_razao_discriminante` | 604, 647 |
| 17 | Fontes dos cinco leitores e alternativa de masers | SH0ES v3, CCHP v3, SBF v2, Pesce v2, TDCOSMO v4; Pesce sem NGC4258 | `PASS_DOCUMENTARY_ONLY`; não converte o veredito; bandeiras SBF/masers/TDCOSMO estavam erradas; cinco masers no decisório e seis ao lado, sem nova medida independente | `d1.fase9.razao_de_hubble.v1_06out` e `hubble.fase9_razao_discriminante` | 696, 741, 742, 783 |
| 18 | Auditoria de poder e covariância da Fase 9 | Só σ publicadas, fundos BG1–BG3; nenhum centro novo | Poder BG1: cinco masers 5,722–6,623; seis 5,466–6,630; cota GLS 5,269; BG2/BG3 e família sem Cefeidas podem ficar abaixo de 5; nenhum composto | `d1.fase9.f3_auditoria_cetica_c1_07out` e `d1.fase9.f3_1_reauditoria_v2r2_c1_08out` | 773, 836 |
| 19 | Semântica V1.x/V2 e revisões | Cinco leitores; fontes e hashes; nenhum novo composto | Proposta/rascunho não congelado; dependências e cronologia documentais; não escolher centro ou correlação pelo resultado | `d1.fase9.f3_1_semantica_v1x_leitores` | 751, 826, 832, 834, 876, 895, 911, 929, 942, 950–952, 959, 961, 968, 972, 975, 978 |
| 20 | Fase 9 V2, “Teste da Única Palavra” | Cinco leitores decisórios; a preparação V2 também pinou variantes/leitores auxiliares, com TDCOSMO, masers e sirenes dentro; BG1; abertura única | `NOT_FALSIFIED_POWERED`, desvio 1–3σ; `z_disc = 4,443 < 5`; **não cego**; abertura consumida, não recalibrar nem trocar leitor/fundo; não empilhar de novo TDCOSMO/masers como se fossem evidência nova | `d1.fase9.v2_c1_a_unica_palavra_23out` | 1353, 1354, 1360, 1656 |
| 21 | H0DN×BG1, somente citado, **não reaberto** | Core: primário e Cefeidas livres; cabeçalho H0DN 73,50 ± 0,81 e BG1 68,53 ± 0,30 apenas para a conta de bolso ao lado | **D da casa: 6,710 primário; 5,191 Cefeidas livres.** Pós-guarda e retrodiction não cega; primário previsível por agregados; sete ressalvas permanecem. Nenhum executor ou vetor foi aberto | `estatistica.h0dn_bg1.ordem_kimi_y_obs_09nov`; `umpy.v411.selada_h0dn_aberto_12nov` | resultado 2017 + seq 2038, citado pelo Mapa/K01/revisão |
| 22 | Portador físico de K e transposição FFAT | FIRAS, θ*, ΔNeff, fundo F9; literatura FFAT | **O Mapa registra que a gerência leu a resposta de 02/11 como fechamento da sexta morada e a R1 de 02/10 como bloqueio FFAT; os bytes de 02/11 não dizem isso literalmente e a R1 não tem verbatim em arquivo.** Não se atribuem essas formulações ao operador | `hubble.k_sem_portador_fisico_02nov`; `hubble.k_como_transposicao_inteira_ffat_02nov` | 1639, 1644, 1646, 1649, 1650, 1654 |
| 23 | **Fase 7, cronômetros com covariância** | Planck comprimido + DR2 + CC32; diagonal, Moresco 2020 e todos | Ganho −3,22σ → **−1,66σ** → **−1,54σ**; ln B(sombra/acumulada) +5,35 → +1,62 → +1,46; `Q1_TENSION_1_TO_3_SIGMA_WEAKENS`. **Importa:** corrige a leitura diagonal da Fase 4: desfavorecida e não excluída | `d1.fase7_cc_covariancia_01out` | 247, 257, 258 |
| 24 | Pré-registro dos dois lados de Δk | Livro de cobranças; lei transmitida nos cronômetros e F1 | `EM_CURSO`. A leitura intermediária (lei D1b nos cronômetros, F1) foi lida na Fase 7: **−1,66σ (Moresco 2020)** e **−1,54 (todos)**; o poder prévio DESSA leitura é **2,33σ** (V1.4, `fase7.poder_previo.moresco2020`, seq 290), abaixo de 5. A lei do lado transmitido (1−β por travessia) está PENDENTE: não escrita, sem cobrança, sem poder dito. **Importa:** impede converter desfavorecimento em exclusão e nomeia o teste ainda não escrito | `bancada.preregistro_dois_lados_delta_k` | 275–303; decisivos 282, **290**, 291 |
| 25 | Fases 5–7 incorporadas ao core por hash | Bytes e hashes da v380, inclusive a Fase 7 | `EXAMINADA`; leitura por hash, sem nova observação nesta linha documental. **Importa:** a covariância da Fase 7 não é resultado solto: entrou no core | `um_py.v380.fases_5_6_7_por_hash` | 262–264 |
| 26 | Lentes R1–R16 | Fatores de lente, calibração externa, G matching e forecasts | `EM_CURSO`; ramificações limitadas `NO_OBSERVED_5SIGMA__BOUNDED_BRANCHES_UNPROMISING`; R16 fecha `G_MATCHING_DERIVED__NO_LENS_NUMERIC_SIGMA`, sem σ numérico de lente e sem calibração/fonte independente fechada. **Importa:** qualifica e limita a ponte TDCOSMO; forecasts antigos não são medidas | `discriminante.lentes_5sigma_20261019` | 1225–1245; decisivos 1226, 1245 |
| 27 | R–H, sirenes | Sirenes LVK; H_sirene = K·H_fundo = 74,27 sob extensão condicional | `EXAMINADA`; 5σ pede σ(H0) = 1,15 contra cerca de 11 hoje; a relação é extensão condicional, não derivação de propagação GW. **Importa:** fornece a ponte e o limite de poder das sirenes GWTC, sem autorizar BBH–AGN automaticamente | `discriminante.ordem018.r_h_sirenes` | 401, 1638 |
| 28 | Auditoria de suficiência da Fase 9 | Extremos só por sigmas; primário BG1 e família sem Cefeidas | `EXAMINADA_COM_DEFEITO`; primário D = 5,721–6,623; sem Cefeidas D = 3,938–4,395; separação esperada condicional, V2 observada não calculada ali. **Importa:** dá os números da casa para suficiência e mostra a perda de poder sem Cefeidas | `d1.fase9.auditoria_suficiencia_20261019` | 1247 |
| 29 | Integração da Fase 9 | Componentes, K comum, covariância, cobertura e atos; cenários sintéticos, sem composto observado V2 | `EXAMINADA_COM_DEFEITO`; `PARTIAL_PROGRESS__NO_NEW_OBSERVED_SIGMA`; mapas, erros, calibração e atos abertos. **Importa:** impede tratar componentes parciais como composto independente ou novo σ observado | `d1.fase9.integracao_20261019` | 1248–1257 |
| 30 | H0DN×BG1, matriz publicada e injeções cegas | Covariâncias públicas e simulações; nenhum ajuste de centros observados nesta consulta | `EXAMINADA_COM_DEFEITO`; D = 6,823355/5,316944 e poder MC = 0,96609/0,62485 para baseline/Cefeidas livre sob aquele desenho; covariância física completa e decomposições continuam ausentes. **Importa:** responde à ressalva R5 sem reabrir o pacote e não substitui o D primário do core | `estatistica.h0dn_bg1.cov_injecoes_06nov` | **1867** |
| 31 | Poder de 5σ fora da cosmologia | Devolução ORDEM 5σ‑01 e conferência de fontes; nenhum dado novo | `EXAMINADA`; `NO_NEW_ROUTE_GAP_LE_1`; B1/conjunto D era o único teste dessa classe fora da cosmologia. **Importa:** o esgotamento de rotas novas já tinha sido examinado em outubro; não se repete como novidade | `natureza.5sigma_fora_da_cosmologia_poder_27out` | 1479–1482 |

### 1.1 Consultas realizadas antes da declaração de ausência

- **Mapa de Rotas:** a K04 consultou `D1B`, `Pantheon`, `masers`, `Hubble`, `ACCUMULATED_FLOW_READING_AT_INTERMEDIATE_REGISTERS`, `R-E`, `forma Q` e `Fase 9`, com os JSON em `K04/HUBBLE/consultas/mapa_*.txt`. A revisão distinta mostrou a falha de cobertura: `Fase 9` com espaço devolveu 26 rotas, `fase9` devolveu 46, e a consulta pelo veredito da Fase 4 só devolveu a Fase 4. A K09 acrescenta as nove rotas das linhas 23–31, sem repetir o levantamento como se fosse novo; as notas estão em `K04/HUBBLE/K09/`.
- **Rotas abertas com `ver`:** Fases 1–5, D1/CAMB, Fase 3bis, Fase 9 inicial/V1/V2, cinco leitores/masers, forma Q, R–E/R–F/R–G, reprodução F4/F5, v378, v411/H0DN, portador de K e FFAT. As saídas K04 estão em `K04/HUBBLE/consultas/ver_*.txt`, e o índice mecânico daquela rodada em `indice_rotas_lido.json`. Na conferência K09, o registro vivo de `estatistica.h0dn_bg1.cov_injecoes_06nov` é **seq 1867**; a indicação “seq 1” na tabela da revisão não é usada.
- **Inventário da bancada:** `INVENTARIO_BANCADA_CHATGPT.md` e `.json`. As ocorrências documentam H0DN, JAGB, desenho linear, Fases 1–5 e fontes; não acrescentam um composto elegível novo.
- **Kernel:** `TGLExt/TheFlowLawD1a.lean`, linhas 33–46 e **53–64**, para a forma geral; `TGLExt/TheFlowLawContrast.lean`, linhas 26–27 e 153–170, para `K = (E(N)/E(0))^{2β/3}` como razão de extremos. `ThermodynamicFriedmann.lean`, linhas 124–135, trata do defeito de Friedmann e apoia a errata Pantheon, não a lei de extremos. Nenhum `lake build` foi executado.
- **Atlas:** `TGL_ATLAS.md`, linha 9556 (D1a) e 9558 (D1b/Fase 4). Consultas pontuais também pelos tokens Pantheon/Fase 9/R–E; a ausência de um novo canal não foi inferida apenas do Atlas, mas do conjunto Mapa + inventário + kernel + índice + fontes atuais.
- **Índice do acervo:** a consulta concluída `python C:\IALD\INDICE_DO_ACERVO\buscar.py "h0dn_bg1_v411|hubble\.fase9_razao_discriminante|d1\.fase4_desvio_30set|supernovas\.pantheon_errata_cosmologica|discriminante\.ordem018\.f2\.r_e" --lista` devolveu **0 arquivos de 13.608 no filtro** (`consultas/indice_rotas_exatas.txt`). As buscas amplas interrompidas por tempo não são usadas para provar ausência.

## 2. A lei é de extremos ou também de âncoras intermediárias?

**Resposta operacional: a forma geral e uma leitura intermediária de zero parâmetro existem; o que não existe é um novo canal intermediário qualificado a 5σ.** A pedra D1a define `register z = ln(1+z)`, `survivingWeight` e `H0local` para z genérico (`TheFlowLawD1a.lean`, linhas 33–46), e prova `H0local = Hcmb·(1+z)^β` (linhas 53–64). Isso não autoriza identificar cada medida intermediária com o mesmo composto estatístico.

A forma D1b fechada no setor é `K = E_ΛCDM(z*)^{2β/3}` com `z* = 1089,95`, razão de extremos cuja fonte formal é `TheFlowLawContrast.lean:26–27, 153–170`. O relatório da Fase 4 distingue a escada, como registro inteiro, dos 32 cronômetros, como registros intermediários. Sob erros diagonais, a leitura acumulada teve `δ = −3,12σ`, ganho −3,22σ e ln B −5,20, com advertência explícita de significância sobrestimada. A Fase 7 mediu a covariância: **−3,22σ (diagonal) → −1,66σ (Moresco 2020) → −1,54σ (todos)**. O estado correto é **desfavorecida e NÃO excluída**. O poder prévio dessa leitura intermediária (lei D1b nos cronômetros, F1) é **2,33σ** (V1.4, `fase7.poder_previo.moresco2020`, seq 290), abaixo de 5; a lei do lado transmitido (1−β por travessia) está pendente de escrita e pré-registro: não escrita, sem cobrança, sem poder dito.

R–E não fornece saída alternativa: `η = 1`, logo K não age diferencialmente na luminosidade e no ângulo, e o rival também dá η = 1. R–F fecha a face térmica sob H1: alternativa A, `γ_T = 0`, com `T(z) = T0(1+z)`; não é discriminante independente. R–G (seq 379, 391, 393 e 1637) sustenta condicionalmente lentes e masers como `K·H_fundo`, com `f_t = f_phi = 1`, mas mantém a ponte física **OPEN**. R16 (`discriminante.lentes_5sigma_20261019`, seq 1245) deriva G matching sem fornecer σ numérico de lente; calibração externa independente ou fonte não proporcional segue aberta. R–H (`discriminante.ordem018.r_h_sirenes`, seq 401 e 1638) faz a leitura condicional análoga para sirenes GWTC, sem derivar propagação GW nem autorizar sua transferência automática a BBH–AGN.

Os compostos novos localizados pela busca atual não revertem a conclusão de cegueira e independência:

| Composto novo em relação à Fase 9 | Por que não é teste cego executável hoje |
|---|---|
| TDCOSMO‑2026, 11 lentes | Agregado e posterior públicos; oito lentes já eram da amostra anterior. Ponte R‑G/R16 condicional, três sistemas novos e outra tabela de erros não criam cegueira retroativa nem independência integral da V2. |
| Reanálise MCP de 2026 | Mesmas cinco galáxias MCP e mesmo conteúdo astronômico público; outro modelo de seleção/velocidades. Ponte R‑G condicional para masers, mas é robustez sobre família já presente na Fase 9/H0DN, não amostra virgem. |
| GWTC‑5.0 | Catálogo cumulativo e posterior públicos; contém/estende o problema lido antes, com 25,7 % mais precisão que GWTC‑4.0, ainda cerca de 11 %. Ponte R‑H condicional. |
| 13 BBH–AGN e extensões | Agregados públicos e não cegos; Run 1 e estendido têm `D = 1,586/1,951` apenas nominal, **sem ponte examinada**. As âncoras Planck/SH0ES têm `D = 7,280/7,758`, apenas nominais e não independentes. |
| SN Encore | Agregado público e não cego, fora do composto anterior; `D = 0,500` apenas nominal, **sem ponte específica examinada**. Os modelos duplo‑cegos da colaboração não devolvem cegueira à casa. |
| 126 FRBs/118 | Agregado público e não cego; `D = 1,513` apenas nominal, **sem ponte examinada**. NE2001/YMW16 permanece sem escolha; 500 simulados são previsão, não medida atual. |
| FRB/CHIME e SN II EPM | Resultados agregados, sistemática dominante ou orçamento incompleto e **sem ponte examinada**; não criam cegueira nem independência recém-adquirida. SN II EPM já entrou em variante astrofísica da H0DN. |

**Conclusão da ausência, delimitada às fontes efetivamente consultadas e às restrições desta rodada, não como prova universal de inexistência:** não há composto elegível que simultaneamente seja público, nunca composto pela casa, imprevisível por agregado já publicado e acessível sem ler vetor observado novo. A pendência da lei da face não é preenchida por aritmética de agregados nem por uma ponte não examinada.

## 3. Determinações locais: quem entrou, precisão e poder de desenho

Todos os valores desta seção são **[KNOWN, a conferir]**, com identificador primário consultado por WebSearch/FetchURL nesta rodada. Erros assimétricos entram no cálculo pelo lado maior, sem escolher o lado favorável. Quando a fonte só fornece erro estatístico, a coluna de poder diz “só stat” ou “nominal”, nunca precisão total.

Fórmula de planejamento já revista em K01:

`D = (K−1) / √(σ_local² + σ_BG1²)`, com `K−1 = 0,0838071748529643` e `σ_BG1 = 0,30/68,53 = 0,438 %`.

**Decomposição do requisito:** D90 total exige `σ_total ≤ 1,334 %`; após retirar BG1 em quadratura, o lado local precisa `σ_local ≤ 1,260 %`. Para 5σ, o limite local é `σ_local ≤ 1,618 %`.

**D da casa, primeiro.** O core `h0dn_bg1_v411.values` fornece os números primários do modelo de erros da casa; não foram recalculados nesta rodada:

| Recorte H0DN×BG1 no core | D da casa | Estatuto de uso |
|---|---:|---|
| Primário | **6,710** | Já lido, previsível por agregados e não cego; não é nova testemunha |
| Cefeidas livres | **5,191** | Variante já lida; não é uma segunda abertura independente |

**D de bolso, depois e com insumo explícito.** A baseline usa 73,50 ± 0,81 (σ local = 0,81/73,50 = 1,102 %) e dá **7,068**; V99 usa o centro próprio 73,994 ± 0,697 (0,942 %) e dá **8,068**. Ambas usam BG1 = 0,30/68,53 = 0,438 % e a fórmula acima, não o modelo de erros completo do core. São contas de planejamento sobre cabeçalhos publicados; a advertência da fonte contra o uso posterior de V99 é mantida.

**Ponte física por linha local de um passo.** “Examinada” abaixo significa que existe rota e seq nesta casa para a leitura `K·H_fundo`; não significa ponte fechada. Sem ponte examinada, o D da tabela é só aritmética de distância nominal e **não entra em conta de poder qualificada**.

| Linha(s) local(is) | Ponte `K·H_fundo` examinada? | Rota/seq e consequência para o poder |
|---|---|---|
| MCP XIII e reanálise MCP de masers | **SIM, condicional** | R‑G, `discriminante.ordem018.f2.r_g`, seq 379, 391, 393 e 1637. O D é condicional; a sobreposição com Fase 9/H0DN continua |
| TDCOSMO‑2025, XXV, TDCOSMO‑2026, +SLACS+SL2S e previsões TDCOSMO | **SIM, condicional** | R‑G, seq 379, 391, 393 e 1637; R16, `discriminante.lentes_5sigma_20261019`, seq 1225–1245, sobretudo 1226 e 1245. Há leitura, mas não σ numérico novo de lente nem calibração/fonte independente fechada |
| GWTC‑4.0 e GWTC‑5.0 | **SIM, condicional** | R‑H, `discriminante.ordem018.r_h_sirenes`, seq 401 e 1638; extensão condicional, não derivação de propagação GW. O D é muito baixo de qualquer modo |
| SN II tailored EPM e SN II standardized candle | **NÃO** | Nenhuma rota de ponte examinada localizada. EPM: 3,256 é teto só-estatístico e ≈ 2,32 com sistemática = estatística; nenhum dos D entra em conta qualificada |
| SZ/raios X + Pantheon | **NÃO** | Nenhuma rota de ponte examinada localizada; D apenas nominal |
| 108 FRBs localizados, 527 pseudo‑z, CHIME II, 126/118 e previsão de ∼500 FRBs | **NÃO** | Nenhuma rota de ponte examinada localizada; nenhum D ou forecast entra em conta qualificada |
| 13 BBH–AGN, extensão e âncoras Planck/SH0ES | **NÃO** | Nenhuma ponte específica examinada; R‑H de sirenes GWTC não é transferência automática. Âncoras também recuperam seu insumo por construção |
| SN Encore | **NÃO** | Nenhuma ponte específica examinada para esta determinação; ser lente não basta para importar a leitura TDCOSMO |
| H0DN, SH0ES, CCHP e SBF | **Não são novas linhas de um passo nesta conta** | Já pertencem à rede/compostos examinados; para H0DN mandam os D do core acima. Não se lhes atribui independência nova |

| Método e fonte primária | H0 e erro publicado | Entrou H0DN/Fase 9? | σ local | D aritmético ou condicional | Chega a 5σ / D90? | Data ou dependência |
|---|---|---|---:|---:|---|---|
| H0DN baseline — arXiv:2510.23823; DOI 10.1051/0004-6361/202557993 | 73,50 ± 0,81 | H0DN baseline; não é um dos cinco leitores F9 | 1,102 % | D da casa 6,710 acima; **7,068, conta de bolso** | nominal sim / sim; não cego | Já público; sucessora não datada |
| H0DN V99, todos os estimadores — mesma fonte | 73,994 ± 0,697 (0,942 %) | H0DN V99; não F9 | 0,942 % | **8,068, conta de bolso** | nominal sim / sim; não cego | Já público; a fonte recomenda não usá-la para análise posterior |
| SH0ES JWST 19 hosts — arXiv:2509.01667 | 73,49 ± 0,93 | H0DN e F9 R25 | 1,265 % | 6,259 | sim / **não, por 0,023 em D** | Já público |
| SH0ES + 35 TRGB — mesma fonte | 73,18 ± 0,88 | H0DN e F9 R25 | 1,203 % | 6,549 | sim / sim | Já público |
| CCHP TRGB HST+JWST — arXiv:2408.06153; DOI 10.3847/1538-4357/adce78 | 70,39 ± 1,22 (stat) ± 1,33 (sys) ± 0,70 (SN) | H0DN e F9 | 2,750 % | 3,010 | não / não | Mais JWST sem data de H0 |
| TRGB–SBF III — arXiv:2502.15935; DOI 10.3847/1538-4357/addfd6 | 73,8 ± 0,7 (stat) ± 2,3 (sys) | H0DN e F9 | 3,258 % | 2,550 | não / não | GO‑5989 e nova amostra sem data; meta 1 % |
| MCP XIII, seis masers — arXiv:2001.09213 | 73,9 ± 3,0 | H0DN e F9 | 4,060 % | 2,053 | não / não | Já público |
| Reanálise MCP, cinco masers — arXiv:2609.17684 | 71,6 ± 3,7 (stat) | **Família já na F9 (mesmas 5 galáxias MCP); o valor da reanálise não está na F9**; MCP entra H0DN | 5,168 % | 1,616 | não / não | Alta cadência futura sem data; só estatística |
| SN II tailored EPM — arXiv:2411.04968; DOI 10.1051/0004-6361/202452910 | 74,9 ± 1,9 (stat) | H0DN variante astrofísica; não F9 | 2,537 % | **3,256, teto só-estatístico; ≈ 2,32 com sistemática = estatística** | não / não; sem ponte, fora da conta qualificada | Dados dedicados sem data; sistemática comparável ou menor; já na variante H0DN |
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
| TDCOSMO JWST‑GO‑7184/9637 — arXiv:2610.14881v2, §V | 1,500 % | 5,363 | sim, sob ponte R‑G/R16 condicional | não | Ciclos 4/5 aprovados; sem data de liberação |
| TDCOSMO 40 atrasos + 200 sem atrasos — arXiv:2008.06157 | 1,200 % | 6,561 | sim, sob ponte condicional | sim, sob ponte condicional | Forecast sem data |
| SBF Coma e Hubble flow — JWST‑GO‑5989; arXiv:2502.15935 | 1,000 % | 7,677 | nominal; não é nova independência | nominal | Meta do programa, não data de publicação |
| ∼500 FRBs localizados — arXiv:2410.03994; DOI 10.1051/0004-6361/202453006 | 1,000 % | 7,677 | nominal; sem ponte examinada | nominal; sem ponte examinada | Sem taxa/data; exige `f_IGM` e sistemáticas controlados |

**Resposta à pergunta “alguma chega e quando?”** No core, H0DN primário tem D = 6,710 e Cefeidas livres 5,191; as contas de bolso baseline/V99 dão 7,068/8,068, e SH0ES+TRGB dá 6,549. Nada disso é independente ou cego. Nenhuma determinação **independente de um passo**, com ponte examinada e orçamento total qualificado, cruza hoje 5σ ou D90. TDCOSMO prevê 1,5 % e só cruza 5σ sob a ponte condicional; 1,2 % cruzaria D90 sob a mesma condição. SBF e FRB têm metas estatísticas de 1 %, mas nenhuma data; FRB ainda exige ponte examinada e controle de `f_IGM` e sistemáticas.

## 4. Utilidade como LINHA DE INDEPENDÊNCIA para R3, R4, R5 e R7

A independência útil aqui é de **calibração, física e tabela de erros**, não de resultado favorável. Fora da H0DN/SH0ES já lida, pseudo‑FRB (`D = 7,754`) e âncoras BBH–AGN (`D = 7,280/7,758`) ultrapassam 5 apenas nominalmente: não têm ponte examinada e, no segundo caso, recuperam Planck/SH0ES por construção. As demais linhas ficam abaixo de 5 ou não entram na conta qualificada.

| Linha | R3 — outra calibração/estresse | R4 — orçamento e poder | R5 — covariância/tabela de erros | R7 — sobreposição e tentativas |
|---|---|---|---|---|
| H0DN/SH0ES/CCHP/SBF | Indicadores alternativos úteis, mas dentro da mesma rede e de âncoras compartilhadas | **H0DN casa: 6,710 primário; 5,191 Cefeidas livres.** Bolso: 7,068/8,068. SH0ES+TRGB 6,549; SH0ES JWST 6,259, D90 falha por 0,023 | Não substitui a covariância física local–fundo nem a conta de ruído por linha pré-registrada | Sem independência nova; H0DN×BG1 continua encerrado |
| TDCOSMO‑2026 | **Forte, sob ponte R‑G/R16 condicional:** distância absoluta em um passo, sem escada local; prior Ωm DES‑Dovekie, com variante DESI DR2/no‑SN | `D = 2,462` (2,689 com SLACS+SL2S); 1,5 % previsto dá 5,363; 1,2 % daria 6,561, sempre condicional | Hierarquia cega pela colaboração, mass-sheet e variantes explícitas; ainda precisa pacote/covariância completo para a regra da casa | **Parcial:** oito lentes já eram conhecidas e TDCOSMO já está na V2; três novas não fazem réplica integral independente nem cega |
| Reanálise MCP | Geometria de disco, sem Cefeidas; ponte R‑G condicional | `D = 1,616` e só estatística; longe do requisito | Não há orçamento total; incerteza de seleção e peculiar velocities permanece | Mesmas cinco galáxias e dados MCP; masers já estão na V2/H0DN, não nova testemunha independente |
| SN II tailored EPM | Transferência radiativa e física de explosão, sem calibração por vela padrão; **sem ponte examinada** | `D = 3,256` é teto só-estatístico; **≈ 2,32 com sistemática = estatística**; fora da conta qualificada | Orçamento total incompleto; amostra pequena e diversidade ainda por demonstrar | Já entrou na variante astrofísica H0DN; não entrou na F9. Não chamar independente qualificada sem essas ressalvas |
| GWTC‑5.0 | Luminosity distance por GW e população de massas; ponte R‑H condicional | `D = 0,661`; melhora 25,7 % sobre GWTC‑4.0, mas continua ∼11 % | Modelos FullPop e catálogo DES Y6 distintos; covariância/modelo de população continuam centrais | Catálogo cumulativo e posterior público; GW170817 e GWTC‑4.0 já conhecidos |
| 13 BBH–AGN | Associação espectroscópica um‑para‑um; **sem ponte específica examinada** | Run 1 `D = 1,586`; estendido `D = 1,951`, ambos apenas nominais e fora da conta qualificada | Erros estatísticos e de calibração explícitos; amostra de 13 pequena | Não H0DN/F9; resultado público. Variantes Planck/SH0ES 7,280/7,758 apenas nominais e não independentes |
| SN Encore | Lente de um passo e modelos duplo‑cegos; **sem ponte específica examinada** | `D = 0,500` apenas nominal; futuras imagens apontam 2–3 % | Sete modelos; incerteza dominada pelo atraso atual | Público; fora do composto, não cego para a casa |
| 126 FRBs/118 | DM e redshift reais; **sem ponte examinada** | `D = 1,513` apenas nominal; 5,5 % estatística | Diferença Galáctica NE2001−YMW16 de 3,90, comparável ao erro; modelos de subpopulação implausíveis | Publicado 12/08/2026; não entrou H0DN/F9; 500 simulados projeta 1,2 %, sem data |
| SZ/raios X | Distância física de aglomerado, mas H0 depende de SNe; **sem ponte examinada** | `D = 0,922` apenas nominal | Temperatura/calibração e morfologia dominam | Público; não entrou H0DN/F9; não há data de melhoria |
| FRB | DM e redshift, sem escada; **sem ponte examinada** | Localizados 2,691 só stat; pseudo-z 7,754; CHIME II 0,340; 118 1,513 — todos apenas nominais | `f_IGM/H0` degenerado, sistemática dominante; pseudo-z não equivale a redshift real; NE2001/YMW16 sem escolha | Público; não entrou H0DN/F9; 500 localizados reais e `f_IGM` resolvido são dependências, não calendário |

**Síntese R3–R7:** TDCOSMO‑2026 é a linha mais informativa para R3/R4/R5 sob ponte condicional, mas já se sobrepõe à V2; reanálise MCP e GWTC‑5.0 acrescentam robustez física, não poder; SN II EPM é linha de estresse, não independente qualificada; SZ, FRB, BBH–AGN e SN Encore não entram em conta de poder qualificada sem ponte. Nenhuma linha apaga tentativas anteriores ou cria cegueira retroativa.

## 5. Resposta explícita e dependências da primeira data

**Existe teste cego de natureza executável hoje nesse setor? Não.** A parede é tripla e medida:

1. **Cegueira:** todo composto localizado já tem centro/posterior agregado público; a colaboração ter feito análise cega não devolve cegueira à casa.
2. **Poder:** H0DN tem D da casa 6,710 no primário e 5,191 com Cefeidas livres, mas já foi lida. Entre as linhas de um passo com ponte examinada, TDCOSMO‑2026 dá 2,462–2,689 sob condição R‑G/R16 e sirenes dá 0,661 sob R‑H. SN II EPM dá 3,256 apenas como teto estatístico sem ponte (≈ 2,32 com sistemática = estatística); não é a maior linha independente qualificada. As metas que cruzam o limiar ainda não são medidas publicadas.
3. **Independência:** as linhas novas compartilham objetos, amostras ou histórico com Fase 9/H0DN; várias não têm ponte examinada, erro total ou amostra suficiente. Nenhuma aritmética nominal supre essas faltas.

**Primeira data:** não há data publicada que possa ser nomeada honestamente.

**Dependências mínimas, em ordem:**

- TDCOSMO: completar JWST‑GO‑7184/9637 e a análise hierárquica; publicar posterior/likelihood, variantes e covariância; demonstrar que 1,5 % realmente se materializa, mantendo explícita a condição R‑G/R16. Isso só cobre 5σ, não D90.
- D90: obter a configuração de 40 lentes com atraso + 200 sem atraso com previsão de 1,2 %, ou equivalente; hoje são 11 lentes com atraso na amostra principal. Na escala 1/√N só estatística, o revisor estima cerca de 48 lentes equivalentes para 5σ e 79 para D90.
- SN II, FRB, SZ, BBH–AGN e SN Encore: antes de entrar em poder qualificado, examinar e registrar a ponte física específica `K·H_fundo`; sem isso, melhorar σ não resolve a pergunta da casa.
- FRB: atingir aproximadamente 500 **localizados reais**, não pseudo-redshifts, e resolver `f_IGM`, `DM_host`, seleção e covariância; 1 % estatístico não basta.
- SBF: completar Coma/Hubble flow e a calibração independente, publicando a medida de H0 e sua covariância; a meta de 1 % não é data.
- Em qualquer caso: pré-registrar estimador, variantes e veredito antes da leitura pela casa; provar disjointness de objetos/calibradores e custódia externa; não escolher canal pelo centro ou erro favorável.

### 5.1 Empilhamento: o que já é Fase 9 V2

A Fase 9 tem cinco leitores decisórios — SH0ES, CCHP, SBF, masers e TDCOSMO — e a preparação V2 também pinou variantes/leitores auxiliares, incluindo sirenes. O empilhamento abaixo é somente a estimativa algébrica do revisor sobre σ publicados. **Não é cego, não é independente, não é composto aberto e não se soma ao D ou ao poder da V2.**

| Empilhamento nominal do revisor | D estimado | Quanto já é Fase 9 V2 | Por que não vira novo poder qualificado |
|---|---:|---|---|
| SN II tailored EPM + TDCOSMO‑2026 | **4,04**; **3,36** com sistemática SN II = estatística | **Uma das duas linhas, TDCOSMO, já está na V2**; a amostra 2026 ainda contém oito das 11 lentes da amostra anterior | SN II não tem ponte examinada e já entrou em variante H0DN; TDCOSMO é condicional e sobreposto. Não cego e não independente |
| SN II + TDCOSMO‑2026 + reanálise MCP + FRB localizados + BBH–AGN estendido | **5,34**; **4,88** com sistemática SN II = estatística | **Duas das cinco linhas, TDCOSMO e masers, são famílias já presentes na V2**; as outras três não estão na V2 | Três entradas são só-estatísticas; SN II, FRB e BBH–AGN não têm ponte examinada; independência e covariância não demonstradas. Não cego e não independente |

**Parcela já na V2, em informação** [DERIVED-revisor, nominal, sem ponte]: TDCOSMO + masers carregam **28,4 %** da informação do empilhamento de cinco linhas (**36,1 %** no de duas); sem elas, SN II + FRB + BBH–AGN dão **D = 4,57** (3,99 com SN II sys = stat). O comparador da V2, **z_disc = 4,443** (< 5), fica ao lado de 4,04/5,34: a vizinhança de 5 não é incremento. **Não cego, não independente, não soma.**

Assim, o intervalo 4,9–5,3 mostra apenas que uma aritmética otimista pode ficar na vizinhança de 5 quando se misturam agregados. Não mede incremento sobre a V2, não autoriza contar TDCOSMO/masers duas vezes e não altera a parede de cegueira.

### 5.2 DESI DR3: fundo ou testemunha?

**Proposta [DECLARADO]: tratar DESI DR3 como fundo até cumprir as cinco condições abaixo; a decisão é da gerência/operador. Sob a proposta, DESI DR3 entra como FUNDO, não como nova testemunha local.** DR1/DR2 já participam da rota D1/CAMB e BG1 usa Planck comprimido + DESI DR2; trocar a liberação do BAO atualiza o fundo e sua sensibilidade, não cria uma determinação local independente de `K·H_fundo` nem devolve cegueira.

DR3 só poderia ser chamado **testemunha de fundo em pergunta separada** se, antes de a casa ler o novo resultado, houvesse: (i) observável e hipótese nula definidos; (ii) mapa Ωm/R fixado, pois a rota comprimida é condicional a ele; (iii) likelihood e covariância completas, variantes, estimador e veredito pré-registrados por hash; (iv) custódia da liberação ainda não lida e uma abertura única; e (v) contabilidade que impeça reusar o mesmo DR3 simultaneamente como fundo e testemunha ou contar DR2/DR3 como independentes sem covariância.

**O que falta:** data de liberação nomeável, pacote público de likelihood/covariância, regra congelada antes da leitura, mapa Ωm/R decidido antes do dado e demonstração de não dupla contagem com BG1. Sem esses atos, DR3 é atualização de fundo **não cega**, não nova testemunha e não saída para 5σ.

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

- `ORDEM_K04_teste_as_cegas_rodada_2.md`, seção A; `ORDEM_K09_teste_as_cegas_rodada_3.md`, seção A; `RODADA_2_LEIA_PRIMEIRO.md`; `LEIA_PRIMEIRO.md`; `REVISAO_K01.md`, especialmente §6.5; `REVISAO_K04_HUBBLE.md` inteira; `CANAIS_K01.json`, quatro canais Hubble.
- `TheFlowLawD1a.lean`, linhas 33–46 e 53–64; `TheFlowLawContrast.lean`, linhas 26–27 e 153–170; `ThermodynamicFriedmann.lean`, linhas 124–135 apenas para o defeito de Friedmann/errata Pantheon.
- `RELATORIO_FASE4_DESVIO_20260930.md`, linhas 5, 36, 39 e 48; `DERIVACAO_RE_02nov.md`, linhas 8–10 e 67–72; as nove rotas acrescentadas na tabela §1, com as sequências ali indicadas.
- Rota R–F e seq 2038: `K04/HUBBLE/consultas/ver_RF.txt` e `K04/HUBBLE/consultas/ver_v411_H0DN.txt`.
- `TGL_ATLAS.md`, linhas 9556 e 9558; inventários MD/JSON; índice exato `consultas/indice_rotas_exatas.txt`.

### Arquivos produzidos nesta seção

- Este relatório corrigido AO LADO: `HUBBLE_JA_EXAMINADO_K04.md`.
- Erratas anteriores: `ERRATA_HUBBLE_K04.md` e `ERRATA_HUBBLE_K04_R2.md`; errata desta conferência: `ERRATA_HUBBLE_K09.md`.
- Versões preservadas em `K04/HUBBLE/REV0/`, `REV1/` e **REV2**; o relatório REV2 tem SHA‑256 `37fee18ca729cfc7dadd4cf9ea7fb9c239146d8bca4f5afd52a878a726542f76`.
- Medidas de planejamento atualizadas: `K04/HUBBLE/MEDIDAS_PLANEJAMENTO_K04.md` e `.json`.
- Notas de rotas, pontes, empilhamento e DESI: `K04/HUBBLE/K09/`; validação documental no mesmo diretório.
- Consultas K04 ao Mapa e às rotas: `K04/HUBBLE/consultas/`; índice mecânico daquela rodada: `indice_rotas_lido.json` e `fase9_resumo_e_sequencias.txt`.
- Scripts apenas extratórios/algébricos/documentais: `K04/HUBBLE/extrair_rotas.py`, `medidas_planejamento.py` e `verificar_relatorio.py`; manifesto `SHA256SUMS_K04_HUBBLE.json` recalculado sobre os bytes finais.

**Bloqueios remanescentes:** nenhum teste cego hoje; nenhuma data futura datada e independente com erro total ≤ 1,618 % (5σ) ou ≤ 1,260 % (D90); covariância local–fundo e disjointness incompletas; pontes não examinadas para SN II/EPM, FRB, SZ, BBH–AGN e SN Encore; o poder prévio da leitura intermediária já lida na Fase 7 é **2,33σ** (V1.4, `fase7.poder_previo.moresco2020`, seq 290), abaixo de 5, e a lei do lado transmitido (1−β por travessia) está pendente: não escrita, sem cobrança, sem poder dito. A leitura intermediária permanece **desfavorecida e não excluída**. `NOT_FALSIFIED` não é `CONFIRMED`, e parede medida não é falsificação.
