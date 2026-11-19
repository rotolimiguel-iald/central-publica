# Notas C — fontes, pinos e pressupostos do desenho

Estas notas acompanham `COMBINACAO_K04.md`. Não são registro no Mapa, depósito, pré-registro nem autorização de execução. Nenhum teste foi realizado.

## 1. Material reutilizado integralmente, sem refazer

- `kimi\CANAIS_K01.json`: previsões, cegueira, independência e poder dos 20 canais; itens usados: `neutrino_m2_juno`, `neff_simons_observatory`, `vazios_euclid`, `nmc_shapiro_multimensageiro`, `ringdown_ramo_b_conjunto_D`.
- `revisao\REVISAO_K01.md`: veredito aprovado com ressalvas; §3 traz \(D_{90}=6,281551565544601\), \(D_N=2,654801672305172\), os fatores 2,548738 e 1,834773 e os cerca de 25,5/25,7 eventos equivalentes; §1-M1 traz \(D=6,2663\) para \(\sigma=0,024\) na forma \(\Delta m^2\); §1-M2 separa essa forma da métrica congelada em \(m_2\); §5 traz SO e IGWN.
- `um_absoluto.json → neff_channel`: \(\Delta N_\mathrm{eff}=0,11946607525373273\). O degrau histórico “SO-ASO ~2030” não foi usado como data; a fonte primária situa o forecast no levantamento completo 2025–2034.
- `um_absoluto.json → h0dn_bg1_v411`: somente regras, ressalvas e valores já selados. Nenhum insumo observado foi aberto.

## 2. Literatura pública, todas [KNOWN, a conferir]

| Assunto | Identificador e uso |
|---|---|
| JUNO, 207,2 dias | JUNO Collaboration, **arXiv:2609.37895v1**, 29/09/2026. Centro \(7,388\) e erro \(0,078\), usados só como alternativa de planejamento; liberação cumulativa não é incremento independente. |
| JUNO, sensibilidade | JUNO Collaboration, Abusleme et al., **arXiv:2204.13249**, DOI **10.1088/1674-1137/ac8bc9**, Tabela 6. \(\sigma=0,024\) em seis anos é previsão acumulada; “seis anos” em dias vivos e data de publicação ficam [OPEN]. |
| JUNO, primeira liberação | JUNO Collaboration, **arXiv:2511.14593v1**, 59,1 dias. Só contexto histórico; não entra como testemunha independente da liberação posterior. |
| SO | Simons Observatory Collaboration, Abitbol et al., **arXiv:2503.00636v3**, JCAP 08 (2025) 034. Tabela 2 e §§2, 3.2, 4: \(\sigma(N_\mathrm{eff})=0,045\), survey 2025–2034, Planck incluído e só erros estatísticos. |
| GWTC-5.0 e datas O4 | LVK, **arXiv:2605.27223v2**, §III.4: O4a/O4b/O4c e cobertura de GWTC-5.0 até O4b; LVK, **arXiv:2608.12193v1**: cerca de 390 candidatas significativas ao fim de O4b. |
| Dados públicos O4 | LVK/GWOSC, **arXiv:2605.27090v1**, §II.1: O4a 24/05/2023–16/01/2024; O4b 10/04/2024–28/01/2025. Usado apenas para taxa retrospectiva bruta. |
| IGWN | **IGWN Public Alerts User Guide — Observing Capabilities**, atualização 26/10/2026, `https://rtd.igwn.org/projects/userguide/en/latest/capabilities.html`: IR1 de seis meses desde meados de janeiro de 2027; O5 concebido para 2029–2031; sensibilidade IR1 provavelmente O4-like; taxas de alertas, não de elegíveis só-220. |
| Censo cosmológico complementar | ESA Euclid timeline, DR1 tentativo 16/06/2027, conforme K01. Calendário não foi convertido em poder. |

## 3. Fontes locais do ringdown e seus hashes

- `work\conjunto_D_20261029\parametrizacao_03nov\PODER_RAMO_B_ANTES_DE_ABRIR.json`; sha256 registrado no Mapa: `05bc5a1f2592b776accbcc9ae2a247623a929ddac0136cf90aaa9490840a4935`.
  - D10 sem hold, informação esperada, sem viés: `poder = 3,9346337577944936`, `n = 10`.
  - D14 com holds, informação esperada, sem viés: `poder = 4,63741267778178`, `n = 14`.
  - O arquivo é planejamento NOT_BLIND calibrado em A; não contém nem produz \(\sigma\) real de D.
- `Bancada_Um\investigacao\preregistro_ramo_b_05out\PREREGISTRO_RAMO_B_RINGDOWN_V1.md`; sha256 `294b88a3632c1cea8e024b1471dd44ef3968614ca582e054307fffecb296da1c`.
  - §7: 14 elegíveis, 10 sem pendência; 8 pendentes GR; 22 reprovados; 44 candidatas de teste.
  - Critério: SNR ≥ 12, massa remanescente ≥ 40 \(M_\odot\), spin no intervalo, fonte IMR/GWOSC e exclusão do corpus de publicação/auditoria.
  - O V1 é anterior à retirada; seus números de poder A/B/C não são evidência cega.
- JSON V1 correspondente; sha256 `86f98fcc124dd9cae04fdb06bd10c14175893253d5b139496bd4c05f109feee0`.
- Mapa `ringdown.ramo_b_preregistro_v386`, registros de 29/10 e 03/11: 14 de O4, 10 sem hold, nenhum posterior/centro D aberto.
- Memória `ramo-b-reaberto-05out.md`, itens de 28/10: leitura do autor, sha16 `597fff4a38e62f42`; ratificação “calibrar não é validar”, sha16 `56703faadf2b3cc2`. Nenhuma fala reservada foi copiada para a entrega.
- Core `f2b_errata_v404`: `WITHDRAWN_BEFORE_DATA__ROUTE_CORRECTED_BY_NOT_BLIND_CALIBRATION_AND_AUTHOR_READING_2026_10_28`. A retirada é declarada pela gerência; A é calibração, não teste; D permanece fechado.

## 4. Aritmética de desenho usada em C — sem vetor e sem código executado

### Stouffer

Com \(D_{90}=6,2815515655\) e \(D_N=2,6548016723\):

\[
D_{J,\mathrm{req}}=\sqrt{D_{90}^2-D_N^2}\simeq5,69297.
\]

Com a separação JUNO de planejamento \(0,1503905333\):

\[
\sigma_{J,\mathrm{req}}\simeq0,0264169\times10^{-5}\,\mathrm{eV}^2.
\]

Com \(\sigma_J=0,024\), \(D_J\simeq6,2663\), e portanto \(\lambda\simeq6,8054\). É um cenário na forma \(\Delta m^2\), não a aplicação da regra congelada em \(m_2\), que deve ser fechada antes de qualquer tranca.

### Dias vivos

A forma reutilizada da revisão é \(T_{\rm novo}\simeq207,2(0,078/\sigma_J)^2\). Ela produz os valores de planejamento aproximados 1.806 dias para a fronteira conjunta e 2.189 dias para \(\sigma_J=0,024\). Não há conversão defensável para data civil sem taxa de dias vivos por ano e calendário de liberação.

### Ringdown

- D10: \(N_{\rm eq}=10\times2,548738\simeq25,4874\); faltam 15,4874 equivalentes.
- D14: \(N_{\rm eq}=14\times1,834773\simeq25,6868\); faltam 11,6868 equivalentes.
- Taxa retrospectiva: \(14/(530/365,25)\simeq9,6\) por ano; não é forecast oficial.
- Taxa necessária em seis meses: D10 \(15,4874/0,5\simeq31,0\)/ano; D14 \(11,6868/0,5\simeq23,4\)/ano.
- Tempo à taxa retrospectiva: D10 \(15,4874/9,6\simeq1,61\) ano; D14 \(11,6868/9,6\simeq1,22\) ano.

Essas operações são contas de desenho permitidas na seção C; nenhuma estatística observada nova foi calculada e nenhum posterior, strain ou vetor foi lido.

## 5. Por que 2034 não é promessa

2034 é apenas o fim do survey no forecast SO. A data real depende de: produto SO público e não comunicado; erro com sistemáticas; covariância SO+Planck; incremento JUNO condicional; métrica congelada; TGL-S/L; função omnibus e nulos congelados; abertura única. A alternativa “mais cedo” exige fonte datada para um produto SO e para o incremento JUNO. Na ausência dessas fontes, a resposta operacional é **parede de calendário**, não antecipação otimista.

## 6. Exclusões deliberadas

- Não se soma \(N_\mathrm{eff}\) com BBN, SO completo ou \(\sum m_\nu\) como se fossem canais independentes.
- Não se usa JUNO acumulado como incremento cego.
- Não se usa Euclid/LSST sem alternativa discriminante e erro do estimador de matéria.
- Não se usa NMC–Shapiro sem eventos e sem \(D\) validado.
- Não se usa ringdown como teste geral da teoria: o canal F2b está retirado e o escopo é apenas o par nomeado.
- Não se usa CMB-S4 como calendário ativo; a revisão confirma o encerramento do apoio em 09/07/2025.
