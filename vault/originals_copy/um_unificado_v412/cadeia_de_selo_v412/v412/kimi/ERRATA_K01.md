# ERRATA K01 — TRÊS FALHAS MATERIAIS E CORREÇÕES AO LADO

[DECLARADO] Errata documental de 13/11/2026, posterior à revisão independente que deu FAIL. A versão inicial não foi apagada: está preservada em `K01\REV0\` com nomes datados. As correções são [DECLARADO] até nova conferência. Nenhum teste foi executado, nenhum vetor observado foi aberto e nenhuma estatística observada foi calculada. Nada foi registrado no Mapa nem depositado na fila.

## 1. Falha 1 — precedência tornava TENSION_SINGLE inalcançável e a guarda divergia

### O erro, preservado

[REAL] Na versão REV0, o ramo 0 capturava S ausente antes de uma única determinação P ≥5 poder chegar a `TENSION_SINGLE`; o ramo 1 capturava S não independente antes do mesmo destino. Além disso, “primary e stress discordam” podia vetar `FALSIFIED` sem critério objetivo congelado. A alteração de versão devolvia `INCONCLUSIVE_SYSTEMATICS` na função, mas `AWAITING_SOURCE` na guarda.

### A correção

[DECLARADO] O pré-registro agora valida P separadamente antes de classificar S e contém uma tabela-verdade completa para P/S e faixas de r:

- [DECLARADO] **S ausente (`ABSENT`)**: P ≥5 vai diretamente a `TENSION_SINGLE(P)_AWAITING_S` ou, sem ratificação do operador, `OPEN_RULE_GAP`; não é capturado por `AWAITING_SOURCE`.
- [DECLARADO] **S não independente (`NONINDEPENDENT`)**: P ≥5 vai diretamente a `TENSION_SINGLE(P)_NONINDEPENDENT` ou `OPEN_RULE_GAP`; não é capturado por `INCONCLUSIVE`.
- [DECLARADO] **S independente com r_S <5**: P ≥5 também vai a `TENSION_SINGLE(P)_SECOND_BELOW_5` ou `OPEN_RULE_GAP`.
- [DECLARADO] **S independente com r_S ≥5 e r_P ≥5**: somente essa combinação devolve `TGL_NU_M2_FALSIFIED`.
- [DECLARADO] **Falha objetiva de integridade (`INVALID`)**: devolve `INCONCLUSIVE_SYSTEMATICS__INTEGRITY_P` ou `..._S`, fail-closed. Inclui hash/versão divergente, unidade errada, centro não finito, σ ≤0 ou não finito, fonte/covariância ausente, timestamp inválido, código/regra alterado depois da guarda ou r não finito.
- [DECLARADO] **Estresses**: são publicados sempre ao lado e não vetam a regra principal sem uma falha objetiva previamente congelada.

[DECLARADO] A tabela também cobre 3≤r<5, 1<r<3 e r≤1 para P/S, com `TENSION_BOTH`, `MATCHED_PROSPECTIVELY`, `UNDERPOWERED` e `ARMED_CONSISTENT` quando cabíveis. O poder conjunto não é presumido.

[DECLARADO] A guarda agora é consistente com a tabela: alteração de versão/código depois da tranca é falha objetiva e devolve `INCONCLUSIVE_SYSTEMATICS__INTEGRITY`, não `AWAITING_SOURCE`.

## 2. Falha 2 — planning sem fonte dos centros e omissão da determinação de 29/09/2026

### O erro, preservado

[REAL] A versão REV0 usava centros históricos do core sem acompanhar a determinação pública mais recente apontada pelo revisor, `arXiv:2609.37895`. Também apresentava uma futura determinação JUNO sem separar corretamente as liberações já públicas.

### Fontes efetivamente consultadas e versionamento

[REAL] As duas fontes foram lidas por `FetchURL` e `WebSearch`, sem abrir vetor de dados:

| Liberação | Centro e precisão publicados | Estatuto adotado |
|---|---|---|
| JUNO Collaboration, **First measurement of reactor neutrino oscillations at JUNO**, `arXiv:2511.14593v1`, 18/11/2025, 59,1 dias | [KNOWN, a conferir] Δm²₂₁ = **(7,50 ± 0,12) × 10⁻⁵ eV²** | [DECLARADO] **Histórico**, já público e conhecido; não é planning atual nem testemunha independente da liberação de 207,2 dias. [JUNO Collaboration, 2025](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2511.14593&text=using%20the%20first%2059.1%20days%20of%20data "citation") |
| JUNO Collaboration, **Measurement of Neutrino Oscillation Parameters at JUNO and Indication of the Neutrino Mass Ordering**, `arXiv:2609.37895v1`, 29/09/2026, 207,2 dias | [KNOWN, a conferir] Δm²₂₁ = **(7,388 ± 0,078) × 10⁻⁵ eV²**, precisão publicada de **1,1 %** | [DECLARADO] **Planning público elegível mais recente**, já público e conhecido; não é futuro nem abertura cega da casa. [JUNO Collaboration, 2026](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2609.37895&text=207.2%20live%20days%20of%20data "citation") |

[REAL] A página oficial `JUNO publications` foi consultada para o rol de liberações e para distinguir determinações da colaboração de análises de terceiros. [JUNO publications](kimi-cite://web?url=https%3A%2F%2Fjuno.ihep.ac.cn%2Fmediawiki%2Findex.php%2FPublication%3AJUNO_publications "citation")

[DECLARADO] P só pode ser uma determinação posterior a 29/09/2026 e ainda não comunicada à casa. A blinding experimental da colaboração não é herdada pela casa. As duas liberações acima entram somente como planning documental.

[DERIVED] A liberação de 207,2 dias contém/estende a de 59,1 dias. Conteúdo incremental de observação não equivale a independência estatística: liberações cumulativas exigem **covariância condicional**. A próxima liberação cumulativa também conterá dados anteriores e não poderá ser contada como independente só por acrescentar dias.

## 3. Falha 3 — mistura m₂/Δm² e linearização apresentada como exata

### O erro, preservado

[REAL] REV0 usou `D = 2(1−m₂pred/m₂planning)/r` como se fosse exato. Essa é uma aproximação de primeira ordem em m₂ e não a forma integral em Δm²₂₁.

### A correção

[DERIVED] Todo o poder e todo o veredito agora são definidos em Δm²₂₁:

\[
\Delta m^2_{21,\rm pred}=m_{2,\rm pred}^2
=7,237609466718292\times10^{-5}\ {\rm eV}^2,
\]

\[
D_{\rm exato}=\frac{|1-\Delta m^2_{21,\rm pred}/\Delta m^2_{21,\rm planning}|}{r}
=\frac{|\Delta m^2_{21,\rm planning}-\Delta m^2_{21,\rm pred}|}{\sigma_{\rm total}},
\qquad r=\frac{\sigma(\Delta m^2_{21})}{\Delta m^2_{21,\rm planning}} .
\]

[DECLARADO] Se m₂ aparecer, a conversão é `m₂ = √Δm²₂₁`. Propagação `σ_m₂ ≈ σ(Δm²₂₁)/(2m₂)` é apenas aproximação de primeira ordem e não entra no D nem no veredito.

### Novos números, com o planning mais recente

| Quantidade de desenho | Valor calculado por `K01_validar.py desenho` |
|---|---|
| [DERIVED] Δm²₂₁,pred | **7,237609466718292 × 10⁻⁵ eV²** |
| [DERIVED] Δm²₂₁,planning, `arXiv:2609.37895v1` | **7,388 × 10⁻⁵ eV²** |
| [DERIVED] σ_total, mesma fonte | **0,078 × 10⁻⁵ eV²** |
| [DERIVED] m₂,planning, apenas conversão exata √Δm²₂₁ | **8,59534757877772 meV** |
| [DERIVED] D com o σ publicado | **1,9280837600219034 ≈ 1,9281**, não um Z observado |
| [DERIVED] razão σ/planning | **0,010557661072008662 = 1,0558 %**, enquanto a fonte arredonda a precisão para 1,1 % |
| [DERIVED] precisão relativa necessária para 5σ | **0,004071210971351058 = 0,407121 %** |
| [DERIVED] precisão relativa necessária para D90 = 6,2815515655 | **0,003240609369253893 = 0,324061 %** |
| [DERIVED] D para r = 0,005 = 0,5 % | **4,071210971351058 ≈ 4,0712**, abaixo de 5 e de D90 |
| [DERIVED] D para r = 0,003 = 0,3 % | **6,78535161891843 ≈ 6,7854**, acima de 5 e de D90 |

[DERIVED] **Histórico, não vigente:** a liberação de 59,1 dias daria, pela mesma fórmula exata, **D = 6,997080887512208 ≈ 6,9971** para 0,5 % e exigiria **0,005569548235417194 = 0,55695 %** para D90. Isso coincide com a verificação do revisor, mas não é mantido como planning atual. Os números lineares antigos, 7,0594 e 0,56191 %, permanecem somente em REV0 e nesta explicação do erro.

[OPEN] **O poder conjunto de P e S não foi calculado.** D_P e D_S permanecem separados até que fonte, precisão, independência e covariância condicional sejam conhecidas.

## 4. Correções adicionais de guarda e validação

- [DECLARADO] **Timestamp:** a guarda deve ser anterior à **liberação pública da determinação, à abertura pela casa e à comunicação de centro/erro à casa**, não apenas à aquisição de bytes. Aquisição não é o marco de cegueira.
- [DECLARADO] **Poder conjunto:** permanece [OPEN] e não é substituído por uma média 1/σ².
- [DECLARADO] **Cumulativas:** conteúdo incremental e covariância condicional foram distinguidos em todas as superfícies canônicas.
- [DECLARADO] **Validador:** agora exige exatamente 20 canais, todos os campos, IDs únicos, classificações válidas, sete ressalvas por canal e fontes resolvidas; consulta efetivamente `rotas.py consultar "estatistica.v412.k01_canais_teste_cego"` e exige que a rota não exista, em vez de fixar um booleano declarativo.
- [REAL] **Resumo:** continua abaixo de 15 linhas não vazias; a ordem original continua com 886 bytes e o mesmo sha256.

## 5. REV0 — preservação com tamanhos e hashes calculados por script

[REAL] Os arquivos alterados foram copiados antes das correções para `K01\REV0\`. A tabela registra os valores da versão inicial, não da versão corrigida.

| Arquivo REV0 | Bytes | sha256 |
|---|---:|---|
| `2026-11-13_REV0_ENTREGA_K01.md` | 24391 | `c21cf76acc3cf16d95ae6f3cd050578de3f618aa30ad60ead883bee063ee66cf` |
| `2026-11-13_REV0_CANAIS_K01.json` | 83527 | `4caf58e61e30d03dd9d7f4c624d06d33a3846d12dcff183e4c9d5396bb7535d1` |
| `2026-11-13_REV0_PRE_REGISTRO_CEGO_RASCUNHO_K01.md` | 16431 | `667f321f0a91a90a00282d3706d34f91fc6dfc1e3e3656868003e2d892846735` |
| `2026-11-13_REV0_REGISTRO_MAPA_K01.json` | 5444 | `332d80cb6eecb2847f9adda428ee66c6d6e821d789f50ae127580919f9386c61` |
| `2026-11-13_REV0_PERGUNTA_K01.md` | 4466 | `a7a61ef03b55a12666d56ac987859cf0b705e67781b04e7b4158d7acea55fe76` |
| `2026-11-13_REV0_K01_validar.py` | 8773 | `f5a527706e6f9bebf713006d75b98bac4947b6d0df139771ff34a0e5d1e248f9` |
| `2026-11-13_REV0_VALIDACAO_K01.json` | 1581 | `ea695619e241f595b08df68705eb4e59cc2b460d0e10963c60e296c9e91acea0` |

[REAL] Backup local: [REV0](C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K01\REV0). Os hashes e tamanhos atuais dos arquivos canônicos são regenerados por `K01_validar.py validar` e gravados em `VALIDACAO_K01.json`, incluindo uma seção própria para REV0.

## 6. Estatuto após a errata

[DERIVED] A conclusão geral permanece: **nenhum canal está pronto hoje com cegueira, poder e independência**. A nova determinação pública dá D = 1,9281; 0,5 % falha; a tabela de 0,3 % dá D = 6,7854 e cruza D90 apenas no primário. A segunda testemunha e o poder conjunto permanecem [OPEN].

[DECLARADO] `FALSIFIED` continua restrito a duas determinações independentes ≥5. P ≥5 com S ausente ou não independente segue diretamente para `TENSION_SINGLE` ou `OPEN_RULE_GAP`; falha objetiva de integridade segue para `INCONCLUSIVE`. Nada disso autoriza abrir dados. `NOT_FALSIFIED ≠ CONFIRMED`; o gate permanece imóvel; a máquina não credita.
