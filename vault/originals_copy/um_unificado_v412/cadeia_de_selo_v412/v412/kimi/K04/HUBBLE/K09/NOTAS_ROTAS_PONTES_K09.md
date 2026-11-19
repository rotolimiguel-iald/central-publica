# Notas K09 — rotas restabelecidas e pontes `K·H_fundo`

**Base documental:** `ORDEM_K09_teste_as_cegas_rodada_3.md` §A, `REVISAO_K04_HUBBLE.md` inteira, consultas K04 já arquivadas e registros do Mapa citados. Nenhum vetor de dado foi reaberto; nenhum executor H0DN foi chamado.

## 1. Leitura, dado, veredito e razão das nove inclusões

| Rota | Leitura/dado | Veredito e seq | Por que importa |
|---|---|---|---|
| `d1.fase7_cc_covariancia_01out` | CC32 com diagonal, Moresco 2020 e todos; Planck comprimido + DR2 | `Q1_TENSION_1_TO_3_SIGMA_WEAKENS`; ganho −3,22 → −1,66 → −1,54σ; seq 247, 257, 258 | Corrige o modelo diagonal da Fase 4; estado desfavorecido e não excluído |
| `bancada.preregistro_dois_lados_delta_k` | Livro de cobranças dos dois lados; lei transmitida nos cronômetros | `EM_CURSO`; a lei do lado transmitido está pendente (não escrita, sem cobrança, sem poder dito); o poder prévio 2,33σ é o da leitura F1 já lida na Fase 7 (V1.4, `fase7.poder_previo.moresco2020`, seq 290), abaixo de 5; seq 275–303, sobretudo 282, 290 e 291 | Impede tratar desfavorecimento como exclusão; não há 5σ |
| `um_py.v380.fases_5_6_7_por_hash` | Fases 5–7 e seus bytes/hashes no core v380 | `EXAMINADA`; seq 262–264 | Estabelece que a Fase 7 entrou no core |
| `discriminante.lentes_5sigma_20261019` | Lentes R1–R16, fatores, G matching, calibração e forecasts | `EM_CURSO`; seq 1225–1245; seq 1226 sem 5σ em ramos limitados; seq 1245 sem σ numérico de lente | Condiciona TDCOSMO e impede promover forecasts |
| `discriminante.ordem018.r_h_sirenes` | Sirenes; H_sirene = K·H_fundo = 74,27 sob extensão | `EXAMINADA`; seq 401, 1638; 5σ exige 1,15 contra cerca de 11 | Dá ponte condicional e poder das GWTC, não de BBH–AGN |
| `d1.fase9.auditoria_suficiencia_20261019` | Extremos por sigmas; primário BG1 e sem Cefeidas | `EXAMINADA_COM_DEFEITO`; D = 5,721–6,623 e 3,938–4,395; seq 1247 | Números da casa para suficiência e perda sem Cefeidas |
| `d1.fase9.integracao_20261019` | Componentes, K comum, cobertura, atos e sintéticos | `EXAMINADA_COM_DEFEITO`; `PARTIAL_PROGRESS__NO_NEW_OBSERVED_SIGMA`; seq 1248–1257 | Componentes parciais não viram composto nem σ observado |
| `estatistica.h0dn_bg1.cov_injecoes_06nov` | Matriz publicada, injeções cegas, covariância física incompleta | `EXAMINADA_COM_DEFEITO`; **seq 1867** | Ressalva R5; não reabrir nem substituir o D primário do core |
| `natureza.5sigma_fora_da_cosmologia_poder_27out` | Devolução ORDEM 5σ‑01 e conferência | `EXAMINADA`; `NO_NEW_ROUTE_GAP_LE_1`; seq 1479–1482 | O esgotamento de rotas novas já era examinado em outubro |

**Divergência corrigida:** a revisão tabula “seq 1” para cov_injecoes; o registro vivo tem `seq = 1867`, rota `estatistica.h0dn_bg1.cov_injecoes_06nov`, com D = 6,823355/5,316944 e poder MC = 0,96609/0,62485 para baseline/Cefeidas livre naquele desenho. Esses números são daquela rota e não substituem 6,710/5,191 do core.

## 2. Matriz de pontes por linha das medidas

`SIM` sempre significa **condicional**, não ponte fechada. `NÃO` significa que nenhuma rota específica examinada foi localizada; nesse caso `entra_conta_poder_qualificada = false` no JSON.

| IDs das medidas/previsões | Ponte | Rota/seq | Uso permitido |
|---|---|---|---|
| `masers_pesce`, `masers_reanalysis` | SIM, R‑G | `discriminante.ordem018.f2.r_g`, seq 379, 391, 393, 1637 | D condicional; sobreposição V2/H0DN continua |
| `tdcosmo2025`, `tdcosmo_xxv`, `tdcosmo2026`, `tdcosmo2026_all`, `tdcosmo_approved`, `tdcosmo_40_200` | SIM, R‑G + R16 | R‑G seq 379, 391, 393, 1637; `discriminante.lentes_5sigma_20261019`, seq 1225–1245 | D/forecast condicional; não prometer medida nem calibração fechada |
| `sirens_gwtc4`, `sirens_gwtc5` | SIM, R‑H | `discriminante.ordem018.r_h_sirenes`, seq 401, 1638 | D condicional; extensão não derivada de propagação GW |
| `sn2_vogl`, `sn2_dejaeger` | NÃO | Nenhuma localizada | D apenas nominal; EPM 3,256 é teto e ≈ 2,32 com sys = stat |
| `sz_colago` | NÃO | Nenhuma localizada | D apenas nominal |
| `frb_local`, `frb_pseudo`, `frb_2026`, `frb_126`, `frb_500` | NÃO | Nenhuma localizada | D/forecast apenas nominal |
| `bbh_agn`, `bbh_agn_extended`, `bbh_agn_planck`, `bbh_agn_shoes` | NÃO | Nenhuma específica; R‑H não se transfere automaticamente | D apenas nominal; âncoras não independentes |
| `sn_encore` | NÃO | Nenhuma específica para esta determinação | D apenas nominal |
| `h0dn_baseline`, `h0dn_all`, `sh0es_jwst`, `sh0es_trgb`, `cchp_trgb`, `sbf_trgb`, `sbf_goal` | Não são novas linhas de um passo | Rede/compostos já examinados | Sem independência nova; H0DN usa primeiro 6,710/5,191 do core |

## 3. Regra de leitura dos números

- D continua `[DERIVED — PLANEJAMENTO]`, não Z nem veredito observado.
- O D da casa vem antes: primário **6,710**, Cefeidas livres **5,191**. Os 7,068/8,068 são contas de bolso com 73,50 ± 0,81 e 73,994 ± 0,697, respectivamente, mais BG1 = 0,30/68,53.
- A leitura intermediária (lei D1b nos cronômetros, F1) é desfavorecida e não excluída; foi lida na Fase 7: **−1,66σ (Moresco 2020)** e **−1,54 (todos)**; o poder prévio DESSA leitura é **2,33σ** (V1.4, `fase7.poder_previo.moresco2020`, seq 290), abaixo de 5. A lei do lado transmitido (1−β por travessia) está pendente: não escrita, sem cobrança, sem poder dito.
- Fase 3 usa 203–212, 214 e 221; seq 213 não pertence à rota.
