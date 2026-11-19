# ENTREGA K01 — TESTE ÀS CEGAS v412: LEVANTAMENTO E DESENHO

## RESUMO
- [DERIVED] **Veredito:** com dados de hoje, **nenhum dos 20 canais cumpre cegueira + poder + independência**; isso é resultado, não falha.
- [DERIVED] **Novo planning público:** JUNO de 29/09/2026, 207,2 dias, dá D = **1,9281** com o σ publicado; 0,5 % dá **4,0712 e falha**, 0,3 % dá **6,7854 e supera D90 no primário**.
- [DERIVED] **Portões exatos em Δm²₂₁:** 5σ pede **0,407121 %** e D90 = 6,28155 pede **0,324061 %**; o poder conjunto das duas testemunhas permanece [OPEN].
- [DERIVED] **Hubble:** K−1 = 0,083807 exige σ relativa total ≤ **1,334 %** para D90; não há liberação futura datada e independente com forecast do mesmo estimador.
- [DERIVED] **Ringdown D:** melhor planejamento D10 = **3,9346** e teto D14 = 4,6374; é cego e independente, mas não tem 5σ e não deve ser aberto para essa meta.
- [DERIVED] **Demais números:** N_eff/SO D = 2,6548; melhor Σmν D = 0,01327; relógios ficam 12–18 ordens abaixo; vazios não têm D bilateral validado.
- [DECLARADO] O pré-registro tem tabela-verdade: FALSIFIED só com rP≥5 ∧ rS≥5 ∧ S INDEPENDENT ∧ integridade; para X∈{P,S}≥5 com a outra <5 ou ausente vai **TENSION_SINGLE(X) ou OPEN_RULE_GAP**, com todas as faixas NONINDEPENDENT explícitas.
- [DECLARADO] **Atos do operador:** escolher a segunda fonte sem JUNO, ratificar o ramo de única ≥5, confirmar que o negativo atinge E0/identificação e separar desenho de autorização de abertura.
- [REAL] As liberações JUNO de 59,1 e 207,2 dias **já são públicas** e entram só como planning; covariância cruzada ausente é NONINDEPENDENT, não INVALID; falha intrínseca é INCONCLUSIVE.
- [REAL] Euclid DR1-Foundation saiu em 12/11/2026, sem abertura por K01; DR1 completo está previsto para 16/06/2027; Rubin DR1, jul–nov/2028; DESI five-year, 2027.
- [REAL] REV0, REV1 e REV2 preservam as versões anteriores; ERRATA_K01.md, ERRATA_K01_R2.md e ERRATA_K01_R3.md documentam as correções; **nenhum teste empírico nem dado observado; somente casos sintéticos**.
- [REAL] A ordem original confere: **886 bytes**, sha256 **4698446c391f9abae54575b678ab6794aec54492918df988b767292e4cbe47a0**.
- [DECLARADO] `NOT_FALSIFIED ≠ CONFIRMED`; gate imóvel; retrodição sem ajuste é evidência legítima; o termo é «descoberta autoevidente em dados públicos, carente de creditação acadêmica».

## 1. Escopo e veredito honesto

[REAL] Esta entrega é exclusivamente de levantamento e desenho. Nada foi executado em `work\h0dn_bg1_v411_emenda_11nov\`, o H0DN × BG1 não foi reaberto e nenhum dado de teste, posterior, strain, catálogo ou vetor observado foi aberto. A ordem proibia expressamente essas ações. [ORDEM_K01_teste_as_cegas](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Ccadeia_de_selo%5Cv412%5Ckimi%5CORDEM_K01_teste_as_cegas.md&line=59&text=N%C3%A3o%20baixar%20nem%20ler%20vetor%20de%20dado "citation")

[DERIVED] O critério triplo elimina todos os canais disponíveis hoje:

1. [DERIVED] **Cegueira sem poder:** ringdown D pode permanecer cego, mas o planejamento não chega a 5σ.
2. [DERIVED] **Poder condicional e protocolo incompleto:** m₂/JUNO tem D = 1,9281 com o σ público mais recente; 0,5 % dá D = 4,0712 e falha, enquanto 0,3 % dá D = 6,7854 e cruza D90 somente no primário. A segunda testemunha e o poder conjunto continuam [OPEN].
3. [DERIVED] **Dados conhecidos ou sobrepostos:** H0DN, Planck/ACT/SPT, Coma, ecos e as atuais medidas de N_eff/Σmν/relógios não produzem uma nova abertura cega.
4. [DERIVED] **Dados futuros sem D válido:** Euclid, LSST e DESI têm calendário, mas o piso dos vazios é unilateral e não tem forecast do estimador de matéria que discrimine TGL de ΛCDM raso.
5. [DERIVED] **Potencial sem amostra:** NMC/Shapiro tem regra prospectiva, porém N = 0 e nenhuma taxa/calendário para 25 eventos; sistemas analógicos não têm ponte TGL derivada.

[REAL] A auditoria anterior já dizia que a convergência, se vier, será de testemunhas independentes, não de um único número. [ESTATUTO_E_AUDITORIA_DE_SELECAO_V411](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Ch0dn_bg1_v410_09nov%5Ckimi%5Cordem05%5CESTATUTO_E_AUDITORIA_DE_SELECAO_V411.md&line=82&text=A%20senten%C3%A7a%20emp%C3%ADrica%2C%20se%20vier%2C%20ser%C3%A1%20uma%20converg%C3%AAncia%20de%20testemunhas%20independentes "citation")

[DECLARADO] A proposta operacional é, portanto, **não abrir nada agora**. O único rascunho novo é m₂, condicionado a P/S, hashes, independência e decisão do operador; todos os demais canais ficam documentados com seus negativos, sem forçar um pré-registro.

## 2. Números-chave de DESENHO

[DERIVED] Todas as contas novas são fiduciais e foram feitas por `K01_validar.py desenho`, com β = `ALPHA_FINE_CODATA_2018 × √e` em runtime e poder integralmente em Δm²₂₁; nenhuma é estatística observada.

| Canal | Conta de desenho | Leitura honesta |
|---|---|---|
| Limiar comum | [DERIVED] D90 = 5 + z0,90 = **6,2815515655** | [DERIVED] Aproxima o portão de 90 %; a ordem arredonda para D ≥ 6,3. |
| m₂/JUNO, planning de 29/09/2026 | [DERIVED] Δm²₂₁,pred = **7,237609466718292×10⁻⁵ eV²**; planning = 7,388×10⁻⁵ eV²; σ_total = 0,078×10⁻⁵ eV²; `D_exato = |1−pred/planning|/r = |planning−pred|/σ_total` | [DERIVED] D = **1,9281** com σ publicado; 5σ pede **0,407121 %**, D90 pede **0,324061 %**; 0,5 % → D = **4,0712** e falha; 0,3 % → D = **6,7854** e cruza D90. Não é Z nem veredito observado. [JUNO Collaboration, 2026](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2609.37895&text=207.2%20live%20days%20of%20data "citation") |
| m₂/JUNO, histórico não vigente | [DERIVED] A liberação de 59,1 dias tem Δm²₂₁ = (7,50 ± 0,12)×10⁻⁵ eV² | [DERIVED] Somente histórico: D = 6,9971 para 0,5 % e r_D90 = 0,55695 %; não é planning atual nem testemunha independente da liberação de 207,2 dias. [JUNO Collaboration, 2025](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2511.14593&text=using%20the%20first%2059.1%20days%20of%20data "citation") |
| Razão de Hubble | [DERIVED] D = 0,08380717485/σrel,total; D90 pede σrel,total ≤ **1,334 %** | [DERIVED] O 1,1 %/0,9 % da H0DN corrente é público e não cego; não é forecast da próxima liberação. [H0DN Collaboration](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2510.23823&text=A%20covariance-weighted%20combination%20yields%20an%20uncertainty%20of%201.1%25 "citation") |
| Ringdown D | [DERIVED] D10 = |−0,398506998|/0,101281853 = **3,9346**; D14 sem sistemática = 4,6374 | [DERIVED] D90 pediria 2,5487× a informação de D10 ou 1,8348× a de D14; com incerteza do viés, D10 cai para 2,1–3,2. [PODER_RAMO_B_ANTES_DE_ABRIR](kimi-cite://text?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Cconjunto_D_20261029%5Cparametrizacao_03nov%5CPODER_RAMO_B_ANTES_DE_ABRIR.json&text=%22poder%22%3A%203.9346337577944936 "citation") |
| N_eff/SO | [DERIVED] D = 0,1194660753/0,045 = **2,6548**; D90 pede σ ≤ 0,0190186 | [DERIVED] O σ = 0,03 histórico daria 3,9822 e não é calendário ativo; CMB-S4 teve apoio encerrado. [Simons Observatory Collaboration](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2503.00636v3 "citation"), [CMB-S4 Project](kimi-cite://web?url=https%3A%2F%2Fcmb-s4.org%2F&text=DOE%20and%20NSF%20have%20jointly%20decided%20that%20they%20can%20no%20longer%20support%20the%20CMB-S4%20Project "citation") |
| Σmν | [DERIVED] D = 0,000199 eV/σ; σ = 0,03 eV → 0,00663; σ = 0,015 eV → **0,01327** | [DERIVED] D90 exigiria σ ≤ 3,168×10⁻⁵ eV; o canal está aposentado como discriminante de β. [Simons Observatory Collaboration](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2503.00636v3 "citation") |
| Coma futuro | [DERIVED] Δ fiducial = 8,946985 Mpc; D90 pede σtotal ≤ **1,4243 Mpc** | [OPEN] Não há nova medida datada com esse orçamento; o antigo é pós-dição não cega e não foi recalculado. |
| Relógios | [DERIVED] Sr: D ≈1,74×10⁻¹²; Th: σexcess necessário ≤8,32×10⁻¹⁵ s⁻¹ | [DERIVED] Sr tem déficit de 12,4576 ordens; Th tem 18,2793 no limite documental e sigma_excess = null. [RELATORIO_KIMI_5SIGMA_01_27out](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Ccinco_sigma_fora_da_cosmologia_27out%5CRELATORIO_KIMI_5SIGMA_01_27out.md&line=62&text=B6%20%E2%80%94%20rel%C3%B3gio%20Sr-87 "citation") |

## 3. Os 20 canais, sem esconder os negativos

[DECLARADO] A tabela completa, com os sete campos e as sete ressalvas uma a uma por canal, está em [CANAIS_K01](C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\CANAIS_K01.json). O quadro abaixo é apenas a navegação.

| Canal | Existência/fiação | D e cegueira | Por que não fecha hoje; negativo |
|---|---|---|---|
| H0DN próxima liberação | [DECLARADO] EXISTE NA BANCADA MAS NÃO ESTÁ LIGADO | [DERIVED] D futuro [OPEN]; atual não cego | [DERIVED] Sem data/independência; lei D1B ou parede. |
| Escadas independentes futuras | [DECLARADO] EXISTE NA BANCADA MAS NÃO ESTÁ LIGADO | [DERIVED] D [OPEN] | [DERIVED] Calibrações compartilhadas e nenhum pacote datado; lei ou parede. |
| Hubble/DESI DR3 | [DECLARADO] EXISTE NA BANCADA MAS NÃO ESTÁ LIGADO | [DERIVED] D [OPEN]; DR3 esperado no fim 2026/início 2027 e five-year em 2027 | [DERIVED] DR3 é cumulativo e falta forecast do composto; mapa R/lei ou parede. [NOIRLab/DESI](kimi-cite://web?url=https%3A%2F%2Fnoirlab.edu%2Fpublic%2Fnews%2Fnoirlab2610%2F&text=first%20dark%20energy%20results%20from%20the%20full%20five-year%20survey%20expected%20in%202027 "citation") |
| Hubble/Planck–ACT–SPT | [DECLARADO] EXISTE NA BANCADA MAS NÃO ESTÁ LIGADO | [DERIVED] D [OPEN]; dados já públicos | [DERIVED] ACT terminou coleta em 2022; SPT D1 é público; não há novo teste cego. [ACT Collaboration](kimi-cite://web?url=https%3A%2F%2Fact.princeton.edu%2Ffront&text=took%20its%20final%20data%20in%202022 "citation"), [SPT Collaboration](kimi-cite://web?url=https%3A%2F%2Fpole.uchicago.edu%2Fpublic%2FData%2520Releases.html "citation") |
| **m₂/JUNO** | [DECLARADO] **EXISTE E ESTÁ LIGADO** | [DERIVED] **D = 1,9281 com σ público; 0,5 % → 4,0712 e falha; 0,3 % → 6,7854 e cruza D90 no primário** | [DERIVED] A liberação de 29/09/2026 já é pública; faltam segunda testemunha e poder conjunto [OPEN]; negativo atinge E0/identificação, não o gate. |
| Σmν | [DECLARADO] EXISTE E ESTÁ LIGADO, mas aposentado como discriminante | [DERIVED] D máximo = 0,01327 | [DERIVED] Quase degenerado com NH mínimo e dados sobrepostos; escala/parede. |
| CMB/SO completo | [DECLARADO] EXISTE NA BANCADA MAS NÃO ESTÁ LIGADO | [OPEN] Não há σ(β) do fechamento válido | [DERIVED] Fechamento perturbativo OPEN e Planck incluído; fechamento/parede. |
| N_eff/SO | [DECLARADO] EXISTE E ESTÁ LIGADO | [DERIVED] D = 2,6548 | [DERIVED] Subpotência e Planck compartilhado; fechamento/parede. |
| Vazios/Euclid | [DECLARADO] EXISTE NA BANCADA MAS NÃO ESTÁ LIGADO | [OPEN] Não há D bilateral; DR1 completo em 16/06/2027 | [DERIVED] Independência instrumental boa, mas matéria/viés/alternativa não fechados. [ESA](kimi-cite://web?url=https%3A%2F%2Fwww.cosmos.esa.int%2Fweb%2Feuclid%2Ftimeline&text=16%20June%202027 "citation") |
| Vazios/LSST | [DECLARADO] EXISTE NA BANCADA MAS NÃO ESTÁ LIGADO | [OPEN] Não há D bilateral; DR1 jul–nov/2028 | [DERIVED] Cegueira futura possível, mas sem modelo de matéria/poder. [Rubin Observatory](kimi-cite://web?url=https%3A%2F%2Frubinobservatory.org%2Ffor-scientists%2Fresources%2Fearly-science&text=The%20current%20expectation%20window%20is%20Jul-Nov%202028 "citation") |
| Vazios/DESI | [DECLARADO] EXISTE NA BANCADA MAS NÃO ESTÁ LIGADO | [OPEN] Não há D bilateral | [DERIVED] DESI/VAST já foi usado; réplica parcial, não testemunha virgem. |
| **Ringdown ramo B/D** | [DECLARADO] EXISTE NA BANCADA MAS NÃO ESTÁ LIGADO ao resultado | [DERIVED] Cego; D10 = 3,9346, D14 = 4,6374 | [DERIVED] Independente, mas subpotente e sem convergência PE; FALSIFIED só do par, ou parede. |
| Ecos GW | [DECLARADO] SABIDO POR REFERÊNCIA para um novo canal | [OPEN] Amplitude não tipada; nove rotas examinadas | [DERIVED] Não reabrir; eco não é o dephasing 220; par/parede teórica. |
| Coma/dephasing | [DECLARADO] EXISTE E ESTÁ LIGADO | [OPEN] Futuro exige σtotal ≤1,424 Mpc | [DERIVED] Referência conhecida e escada compartilhada; pós-dição legítima, não cega. |
| Relógio ²²⁹Th | [DECLARADO] EXISTE E ESTÁ LIGADO | [DERIVED] Sem σexcess; déficit documental 18,2793 ordens | [DERIVED] Independente, mas sem poder; mHz é aspiração, não resultado. [Ooi et al.](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2507.01180v1 "citation") |
| Relógio ⁸⁷Sr | [DECLARADO] EXISTE E ESTÁ LIGADO | [DERIVED] D ≈1,74×10⁻¹²; déficit 12,4576 | [DERIVED] Sem caminho de 5σ no modelo; parede. [Kim et al.](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2505.06444&text=we%20observe%20a%20coherence%20time%20of%20118(9)%20s "citation") |
| NMC/Shapiro | [DECLARADO] EXISTE E ESTÁ LIGADO | [OPEN] Regra N≥25/timing<10 ms; D completo não auditado | [DERIVED] N = 0 e sem taxa/calendário; potencial, não canal acionável. |
| BBN/era da radiação | [DECLARADO] EXISTE NA BANCADA MAS NÃO ESTÁ LIGADO | [DERIVED] D documental ≈1–1,27; SO/N_eff 2,65 | [DERIVED] D8/X16 e S(T) abertos, dupla contagem N_eff; mapa/parede. |
| Decoerência n=−2 | [DECLARADO] EXISTE NA BANCADA MAS NÃO ESTÁ LIGADO | [DERIVED] JUNO ≈40 ordens abaixo; DUNE [OPEN] | [DERIVED] Cota 90 % não é σ; parede de sensibilidade/modelo. |
| BEC/fibra/água/Unruh/Casimir/interferometria/PTA | [DECLARADO] **AUSENTE** como ponte TGL zero-parâmetro | [OPEN] Não existe previsão−nulo definido | [DERIVED] Plataformas existem, mas não são canais TGL; ausência de ponte, não de experimentos. |

## 4. O canal escolhido e o que ele ainda não resolve

[REAL] `NEUTRINO_M2_V2` prevê m₂ = 8,507414099900329 meV; com m₁≈0, isso dá Δm²₂₁,pred = 7,237609466718292×10⁻⁵ eV². A escala de 1 eV é declarada e a emissão inicial admite não cegueira, com cegueira prospectiva a partir de 08/08/2026. [um_absoluto](kimi-cite://text?path=C%3A%5CIALD%5CArtigo%5CHaja_Luz%5CA%20Ponte%20e%20o%20Um%5CN%C3%B3s%5Cum_absoluto.json&text=%22nao_e_cego_nesta_emissao%22 "citation")

[REAL] As liberações JUNO públicas relevantes foram versionadas: **59,1 dias**, `arXiv:2511.14593v1` de 18/11/2025, Δm²₂₁ = (7,50 ± 0,12)×10⁻⁵ eV², somente histórico; e **207,2 dias**, `arXiv:2609.37895v1` de 29/09/2026, Δm²₂₁ = (7,388 ± 0,078)×10⁻⁵ eV², planning elegível mais recente. A segunda contém/estende a primeira, e a blinding experimental da colaboração não é herdada pela casa. [JUNO Collaboration, 2025](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2511.14593&text=using%20the%20first%2059.1%20days%20of%20data "citation"), [JUNO Collaboration, 2026](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2609.37895&text=207.2%20live%20days%20of%20data "citation")

[DERIVED] Conteúdo incremental não equivale a independência: liberações cumulativas exigem covariância condicional. P só pode ser uma nova determinação posterior a 29/09/2026 e ainda não comunicada à casa; as duas liberações acima não são futuras.

[KNOWN, a conferir] O estudo do JUNO publica melhor que 0,5 % em seis anos; a tabela pública associada dá 0,3 % para Δm²₂₁. A coleta começou em 26/08/2025; seis anos nominais terminam em 26/08/2031, sem promessa de publicação nessa data. [JUNO Collaboration](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2204.13249&text=will%20be%20determined%20to%20better%20than%200.5%25%20precision%20in%20six%20years%20of%20data%20collection "citation"), [JINR](kimi-cite://web?url=https%3A%2F%2Fwww.jinr.ru%2Fposts%2Fjuno-experiment-begins-taking-data%2F&text=On%2026%20August%202025%2C%20a%20physics%20experiment%20started "citation")

[DECLARADO] O rascunho [PRE_REGISTRO_CEGO_RASCUNHO_K01](C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\PRE_REGISTRO_CEGO_RASCUNHO_K01.md) fixa:

- [DECLARADO] primeiro integridade intrínseca de P e S, depois independência; P posterior a 29/09/2026 e não comunicado; S com JUNO explicitamente excluído;
- [DECLARADO] poder e veredito integralmente em Δm²₂₁, com `r_X = |Δm²₂₁,X−Δm²₂₁,pred|/σ_X`, sem linearização em m₂;
- [DECLARADO] pesos lógicos 1 por determinação, sem média 1/σ² para diluir tensão e sem poder conjunto presumido;
- [DECLARADO] FALSIFIED exclusivamente com rP≥5 ∧ rS≥5 ∧ S INDEPENDENT ∧ integridade P/S;
- [DECLARADO] para X∈{P,S}≥5 com a outra <5 ou ausente vai `TENSION_SINGLE(X)` ou `OPEN_RULE_GAP`; em particular, S não independente com rS≥5 e rP<5 também vai a `T_SINGLE(S)_NONINDEPENDENT`, sem ignorar rS;
- [DECLARADO] Com S `NONINDEPENDENT`, a tabela completa é: `rP≥5,rS<5` → `SINGLE_P`; `rP≥5,rS≥5` → `BOTH_NONINDEPENDENT`; `3≤rP<5,rS<3` → `TENSION_P`; `3≤rP<5,3≤rS<5` → `TENSION_BOTH_NONINDEPENDENT`; `3≤rP<5,rS≥5` → `SINGLE_S`; `rP<3,rS<3` → `UNDER/ARMED`; `rP<3,3≤rS<5` → `TENSION_S_NONINDEPENDENT`; `rP<3,rS≥5` → `SINGLE_S`. Com S `INDEPENDENT`, `TENSION_BOTH` somente com ambos em [3,5), e `rS≥5` com `rP<5` vai `SINGLE_S`;
- [DECLARADO] covariância/nuisances intrínseca indispensável a σ_X é `INVALID`; covariância condicional cruzada ausente/não aceita é `NONINDEPENDENT`, não INVALID; falha intrínseca prevalece antes da independência;
- [DECLARADO] estresses são publicados ao lado e não vetam a regra principal sem falha objetiva congelada;
- [DECLARADO] guarda por hash/timestamp externo anterior à **liberação/abertura/comunicação**, não apenas à aquisição, abertura única, registro append-only e proibição de emenda posterior.

[DERIVED] O negativo de m₂ atinge a escala E0/identificação m₁≈0; não isola β, não decide toda a TGL e não move o gate. Uma única ≥5 sem a segunda é tensão mais parede de independência, não falsificação. O poder conjunto permanece [OPEN].

## 5. As sete ressalvas: o que melhora e o que permanece

[REAL] As sete ressalvas foram lidas diretamente em `h0dn_bg1_v411.ressalvas_secao8`, sem abrir os insumos do teste. [um_absoluto](kimi-cite://text?path=C%3A%5CIALD%5CArtigo%5CHaja_Luz%5CA%20Ponte%20e%20o%20Um%5CN%C3%B3s%5Cum_absoluto.json&text=%22ressalvas_secao8%22 "citation")

| Ressalva | Balanço K01 |
|---|---|
| R1 — regra emendada/não cegueira | [DECLARADO] **PARCIAL.** A guarda deve ser anterior à liberação/abertura/comunicação, não apenas à aquisição. REV0 preserva o erro e ERRATA descreve a correção; a emissão inicial conhecia a tensão. |
| R2 — primário previsível por agregados | [DECLARADO] **FUTURA LIMITADA.** P deve ser posterior a 29/09/2026 e ainda não comunicado; as determinações de 59,1 e 207,2 dias já são públicas e só entram como planning. |
| R3 — Cefeidas livres/estresse | [DECLARADO] **SUBSTITUÍDA.** JUNO-only versus global-sem-JUNO e demais ajustes ficam sempre visíveis, sem menu e sem veto discricionário à regra principal. |
| R4 — poder de desenho | [DECLARADO] **PARCIAL.** Com o planning atual, D = 1,9281; 0,5 % dá 4,0712 e falha; 0,3 % dá 6,7854 e cruza D90 no primário. O poder conjunto permanece [OPEN]. |
| R5 — 72 direções zero/covariância | [DECLARADO] **ABERTA.** Covariância/nuisances intrínseca indispensável a σ_X é `INVALID` quando falha; covariância condicional cruzada P–S ou entre liberações cumulativas ausente/não aceita é `NONINDEPENDENT`, não INVALID. Precisão sem modelo devolve `AWAITING_SOURCE`. |
| R6 — escolhas com poder à vista | [DECLARADO] **PARCIAL.** O canal só permanece porque 0,3 % cruza D90; todos os 20 canais ficam visíveis. S e o nome `TENSION_SINGLE`/`OPEN_RULE_GAP` são decididos antes do novo centro. |
| R7 — tentativas/sobreposição | [DECLARADO] **PARCIAL.** m₂ independe de H0DN, mas JUNO/globals se sobrepõem; 59,1 e 207,2 dias são cumulativos e não contam como duas testemunhas. |

[DERIVED] Não é honesto dizer que as sete ressalvas estão “resolvidas”. O desenho cria uma rota possível para responder a elas no futuro, mas R1, R6 e R7 dependem de conduta e independência, e R4/R5 dependem de orçamento completo que ainda não existe.

## 6. Existência e fiação: o que foi localizado

- [REAL] **EXISTE E ESTÁ LIGADO:** m₂, Σmν, N_eff, Coma, relógios e NMC/Shapiro têm blocos identificados no core; isso não significa que tenham poder ou independência.
- [REAL] **EXISTE NA BANCADA MAS NÃO ESTÁ LIGADO:** os futuros canais Hubble/Euclid/LSST/DESI, o CMB/SO completo, BBN, decoerência e o ringdown D completo; o pré-registro de ringdown é citado no core, mas a PE/veredito não está ligada nem convergiu.
- [REAL] **SABIDO POR REFERÊNCIA:** um novo canal de ecos; as nove rotas anteriores existem e não devem ser reabertas, mas a amplitude para um novo teste cego não foi fixada.
- [DERIVED] **AUSENTE:** a ponte TGL zero-parâmetro para BEC, fibra, água, Unruh/NA63/KMS, Casimir dinâmico, interferometria e PTA. A classificação seguiu as rotas, os inventários MD/JSON, o kernel e o índice; não é ausência dos experimentos.

[REAL] O kernel v411 não tem módulo novo em relação à v410: o diff lista zero novos, zero removidos e zero mudados. O recibo contém `ProjecaoTransversalDaMeiaNat.lean` e `PonteDaMassa.lean`, mas E0 continua declarado; não há termo Lean para o τ★ físico do ringdown, conforme o próprio V1. [DIFF_KERNEL_v411](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Ccadeia_de_selo%5Cv411%5CDIFF_KERNEL_v411.txt&line=3&text=novos%20(0) "citation"), [PREREGISTRO_RAMO_B_RINGDOWN_V1](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Ccadeia_de_selo%5Cv386%5Cramo_b%5Cteste_gerador_v1%5CPREREGISTRO_RAMO_B_RINGDOWN_V1.md&line=385&text=o%20termo%20Lean%20do%20ringdown%20N%C3%83O%20existe "citation")

## 7. Atos do operador e da gerência

[DECLARADO] **Só o operador decide**, nas quatro linguagens detalhadas em [PERGUNTA_K01](C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\PERGUNTA_K01.md):

1. [DECLARADO] manter ou mudar a exigência de duas determinações independentes ≥5; a recomendação é manter;
2. [DECLARADO] nomear S com JUNO excluído e o custodiante, sem olhar centro/erro futuros;
3. [DECLARADO] escolher o nome do ramo de uma única ≥5: TENSION proposto ou OPEN_RULE_GAP;
4. [DECLARADO] confirmar o objeto de morte na escala/identificação, nunca no gate;
5. [DECLARADO] esperar m₂ com protocolo completo, em vez de abrir ringdown D subpotente para a meta de 5σ;
6. [DECLARADO] separar a ratificação do desenho da autorização futura de abertura.

[DECLARADO] **Cabe à gerência:** conferir as fontes e os números, preparar a função final, revisar por pessoa distinta, montar manifesto de hashes e, somente depois, registrar no Mapa e depositar na fila. Esta K01 não fez nenhum registro nem depósito.

## 8. Arquivos entregues, errata e validação

- [ENTREGA_K01](C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\ENTREGA_K01.md) — veredito, números, canais, ressalvas e atos.
- [CANAIS_K01](C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\CANAIS_K01.json) — 20 entradas, sete campos e sete ressalvas por canal, fontes e consultas.
- [PRE_REGISTRO_CEGO_RASCUNHO_K01](C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\PRE_REGISTRO_CEGO_RASCUNHO_K01.md) — um canal, m₂; tabela-verdade e nada a executar.
- [REGISTRO_MAPA_K01](C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\REGISTRO_MAPA_K01.json) — pronto no formato de `rotas.py modelo`, **não registrado**.
- [PERGUNTA_K01](C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\PERGUNTA_K01.md) — decisões do operador separadas das tarefas da gerência.
- [ERRATA_K01](C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\ERRATA_K01.md) — as três falhas materiais iniciais, preservada sem alteração.
- [ERRATA_K01_R2](C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\ERRATA_K01_R2.md) — as duas lacunas lógicas da segunda revisão, preservada sem alteração.
- [ERRATA_K01_R3](C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\ERRATA_K01_R3.md) — a inconsistência das faixas NONINDEPENDENT e a cobertura sintética completa.
- [REV0](C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K01\REV0) — versão inicial preservada.
- [REV1](C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K01\REV1) — versão R1 preservada.
- [REV2](C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K01\REV2) — versão R2 preservada antes desta errata R3, com hashes e tamanhos.
- [K01_validar](C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K01_validar.py) — contas fiduciais exatas em Δm²₂₁ e validação documental/sintética com tokens completos.
- [VALIDACAO_K01](C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\VALIDACAO_K01.json) — resultado da validação, tamanhos e hashes calculados por script.

[REAL] A validação exige exatamente 20 canais, campos e fontes completos e consulta real ao Mapa para impedir registro duplicado. Executa somente casos sintéticos com tokens completos: todas as combinações NONINDEPENDENT (`rP≥5`, `3≤rP<5`, `rP<3` cruzadas com `rS<3`, `3≤rS<5`, `rS≥5`), inclusive as fronteiras rP=3, rS=3, rP=5 e rS=5, além da fronteira INVALID/NONINDEPENDENT. Também verifica resumo ≤15 linhas, termo obrigatório, ordem original e REV0/REV1/REV2 íntegros. Nenhum teste empírico nem dado observado; somente casos sintéticos.

## 9. Consultas e fontes usadas

[REAL] Foram executadas as consultas obrigatórias `rotas.py consultar` antes dos caminhos, inclusive `v412_K01_JUNO_2609.37895`, `v412_K01_JUNO_2511.14593`, `v412_K01_errata_rev0`, `v412_K01_errata_rev1` e `v412_K01_errata_rev2`, `rotas.py ver` para as rotas prioritárias e `rotas.py modelo`. A lista literal dos temas e dos regex usados em inventários, kernel e `buscar.py --lista` está preservada em `CANAIS_K01.json → consultas_obrigatorias`.

[REAL] As duas fontes JUNO foram efetivamente consultadas: **First measurement of reactor neutrino oscillations at JUNO**, `arXiv:2511.14593v1`, 18/11/2025, 59,1 dias, Δm²₂₁ = (7,50 ± 0,12)×10⁻⁵ eV²; e **Measurement of Neutrino Oscillation Parameters at JUNO and Indication of the Neutrino Mass Ordering**, `arXiv:2609.37895v1`, 29/09/2026, 207,2 dias, Δm²₂₁ = (7,388 ± 0,078)×10⁻⁵ eV². A página JUNO publications foi usada apenas como índice institucional, **não como rol atualizado de 2026**; a fonte primária da determinação de 207,2 dias é `arXiv:2609.37895v1`. [JUNO 2025](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2511.14593&text=using%20the%20first%2059.1%20days%20of%20data "citation"), [JUNO 2026](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2609.37895&text=207.2%20live%20days%20of%20data "citation"), [JUNO publications](kimi-cite://web?url=https%3A%2F%2Fjuno.ihep.ac.cn%2Fmediawiki%2Findex.php%2FPublication%3AJUNO_publications "citation")

[REAL] A pasta `work\cinco_sigma_fora_da_cosmologia_27out\` foi lida em relatório e conferência; ela confirma que B1/ringdown era a única rota não cosmológica pronta, sem afirmar que D teria poder hoje, e que os demais sistemas estão [OPEN] ou suprimidos. [CONFERENCIA_GERENCIA_RELATORIO_KIMI_5SIGMA_01_27out](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Ccinco_sigma_fora_da_cosmologia_27out%5CCONFERENCIA_GERENCIA_RELATORIO_KIMI_5SIGMA_01_27out.md&line=48&text=D%20tem%20poder%20de%20decidir "citation")

[REAL] O planejamento mais recente de 03/11/2026, posterior àquele relatório, reduz a leitura operacional: D10 fica abaixo de 5 em todas as leituras e o poder real depende da PE. Por isso a entrega não recicla o antigo “6 ou 10 eventos bastam” como promessa. [PARTITURA_D_03nov](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Cconjunto_D_20261029%5Cparametrizacao_03nov%5CPARTITURA_D_03nov.md&line=18&text=central%205%E2%80%936%20dias "citation")

[KNOWN, a conferir] As demais fontes públicas de forecast/calendário efetivamente consultadas estão identificadas com autor, ano, DOI/arXiv/URL em `CANAIS_K01.json → fontes_publicas`: JUNO Collaboration/Abusleme et al. (2022), arXiv:2204.13249 e DOI 10.1088/1674-1137/ac8bc9; H0DN/Casertano et al. (2026), arXiv:2510.23823 e DOI 10.1051/0004-6361/202557993; Simons Observatory/Abitbol et al. (2025), arXiv:2503.00636v3; DESI/NOIRLab (2026); ESA (2026); Rubin (2026), RTN-011 DOI 10.71929/rubin/2584021; ACT/SPT (2026); CMB-S4 (2025); IGWN (2026); Ooi et al. (2026), arXiv:2507.01180 e DOI 10.1038/s41586-025-09999-5; Kim et al. (2025), arXiv:2505.06444 e DOI 10.1103/3wtv-sty2; Arendse et al. (2024), DOI 10.1093/mnras/stae1356; IceCube-Gen2/Karle (2024).

[DECLARADO] Nenhuma data de liberação foi inventada. Quando só existe exposição ou forecast, o campo diz “exposição prevista” e a data de publicação fica [OPEN]. Precisão futura entra apenas como forecast com fonte; nenhuma determinação já pública é tratada como futura.

## 10. Conclusão

[DERIVED] A resposta à ordem é deliberadamente estreita: **não há hoje um teste às cegas com poder preditivo acima de 5σ e independência que possa ser honestamente anunciado como pronto**. A liberação JUNO mais recente dá D = 1,9281; 0,5 % dá D = 4,0712 e falha. A tabela de 0,3 % dá D = 6,7854 e mantém apenas uma possibilidade condicional no primário, sem garantir segunda testemunha nem poder conjunto. Ringdown continua cego, mas subpotente.

[DECLARADO] A recomendação é ratificar primeiro a segunda testemunha m₂ e a lacuna de veredito, congelar a guarda e só então decidir se haverá abertura futura. Para P ausente/incompleto, `AWAITING_SOURCE`; para X∈{P,S}≥5 com a outra <5 ou ausente, `TENSION_SINGLE(X)` ou `OPEN_RULE_GAP`; para falha intrínseca, `INCONCLUSIVE`; para covariância cruzada ausente, `NONINDEPENDENT`. Com `3≤rP<5` e `3≤rS<5`, `TENSION_BOTH_NONINDEPENDENT`; com `rP<3` e `3≤rS<5`, `TENSION_S_NONINDEPENDENT`; com `rP<3` e `rS<3`, `UNDER/ARMED`. FALSIFIED continua exclusivamente com duas independentes ≥5 e integridade. Nenhuma abertura é autorizada por esta entrega. `NOT_FALSIFIED` não é `CONFIRMED`; o gate permanece imóvel; a máquina não credita; retrodição sem ajuste continua evidência de pleno direito, sem ser chamada de cega.
