# ERRATA AO LADO K09 — K04/Hubble: covariância, rotas, pontes e contabilidade de poder

**Data:** 14/11/2026. **Escopo:** somente seção A/Hubble da K09. **Conclusão principal preservada:** não existe hoje teste cego de natureza executável no setor Hubble com poder de desenho ≥ 5σ; é parede medida, não falsificação.

A versão imediatamente anterior está preservada em `K04/HUBBLE/REV2/`, com relatório, erratas anteriores, medidas, gerador, validador e manifesto. O SHA‑256 do relatório REV2 é `37fee18ca729cfc7dadd4cf9ea7fb9c239146d8bca4f5afd52a878a726542f76`. REV0 e REV1 permanecem intactas.

## 1. Leitura intermediária: estado correto

As formulações anteriores que apresentavam a leitura intermediária como definitivamente excluída, ou negavam qualquer forma intermediária vigente, ficam **SUPERSEDADAS** por esta errata. O estado examinado é:

- Fase 4, `d1.fase4_desvio_30set`, seq 229, 231 e 410: modelo com erros diagonais; ganho da lei acumulada −3,22σ, com advertência de significância sobrestimada.
- Fase 7, `d1.fase7_cc_covariancia_01out`, seq **247, 257 e 258**: **−3,22σ (diagonal) → −1,66σ (Moresco 2020) → −1,54σ (todos)**; ln B(sombra/acumulada) +5,35 → +1,62 → +1,46; veredito `Q1_TENSION_1_TO_3_SIGMA_WEAKENS`.
- A formulação correta é **desfavorecida e NÃO excluída**. A leitura intermediária (lei D1b nos cronômetros, F1) foi lida na Fase 7: **−1,66σ (Moresco 2020)** e **−1,54 (todos)**; o poder prévio DESSA leitura é **2,33σ** (V1.4, `fase7.poder_previo.moresco2020`), abaixo de 5 — registro em `bancada.preregistro_dois_lados_delta_k`, seq 282, **290** e 291. A lei do lado transmitido (1−β por travessia) está PENDENTE: não escrita, sem cobrança, sem poder dito; não há teste de 5σ nesse canal.

A incorporação da Fase 7 ao core por hash está em `um_py.v380.fases_5_6_7_por_hash`, seq 262–264. Isso corrige a leitura intermediária sem alterar a parede de cegueira/poder.

## 2. Nove rotas restabelecidas no inventário

| Rota | Conteúdo que passa a constar | seq |
|---|---|---|
| `d1.fase7_cc_covariancia_01out` | Covariância dos cronômetros; enfraquecimento −3,22 → −1,66 → −1,54σ | 247, 257, 258 |
| `bancada.preregistro_dois_lados_delta_k` | Dois lados de Δk; lei do lado transmitido pendente (não escrita, sem cobrança, sem poder dito); o poder prévio 2,33σ é o da leitura F1 já lida na Fase 7 (V1.4, `fase7.poder_previo.moresco2020`), abaixo de 5 | 275–303; decisivos 282, **290**, 291 |
| `um_py.v380.fases_5_6_7_por_hash` | Fase 7 incorporada ao core por hash | 262–264 |
| `discriminante.lentes_5sigma_20261019` | R1–R16; ramificações sem 5σ; R16 sem σ numérico de lente | 1225–1245; decisivos 1226, 1245 |
| `discriminante.ordem018.r_h_sirenes` | Sirenes `K·H_fundo` condicional; 5σ pede σ(H0) = 1,15 contra cerca de 11 | 401, 1638 |
| `d1.fase9.auditoria_suficiencia_20261019` | Primário BG1 D = 5,721–6,623; sem Cefeidas D = 3,938–4,395 | 1247 |
| `d1.fase9.integracao_20261019` | K comum, cobertura e atos; progresso parcial sem novo σ observado | 1248–1257 |
| `estatistica.h0dn_bg1.cov_injecoes_06nov` | Matriz publicada e injeções cegas; covariância física ainda incompleta | **1867** |
| `natureza.5sigma_fora_da_cosmologia_poder_27out` | Devolução anterior já conferida: nenhuma rota nova com gap ≤ 1 | 1479–1482 |

**Correção documental adicional:** a tabela da revisão K04 indica “seq 1” para `estatistica.h0dn_bg1.cov_injecoes_06nov`; a consulta ao registro vivo do Mapa devolve **seq 1867**. Prevalece o identificador vivo. Nenhum pacote H0DN foi reaberto.

## 3. Pontes e poder por linha local

- **Lentes e masers:** R‑G, `discriminante.ordem018.f2.r_g`, seq 379, 391, 393 e 1637, com ponte condicional e parte física ainda OPEN. Para lentes, R16 (`discriminante.lentes_5sigma_20261019`, seq 1225–1245) é indispensável: G matching derivado, mas sem σ numérico de lente e sem calibração/fonte independente fechada.
- **Sirenes GWTC:** R‑H, `discriminante.ordem018.r_h_sirenes`, seq 401 e 1638, é extensão condicional, não derivação de propagação GW.
- **SN II/EPM, FRB, SZ/raios X, BBH–AGN e SN Encore:** nenhuma ponte específica examinada localizada. Seus D permanecem aritmética nominal e **não entram em conta de poder qualificada**. R‑H não se transfere automaticamente a BBH–AGN; ser uma lente não basta para importar TDCOSMO a SN Encore.

A matriz linha a linha está no relatório §3 e em `K04/HUBBLE/K09/NOTAS_ROTAS_PONTES_K09.md`; os mesmos campos foram gravados nas medidas JSON.

## 4. D da casa, D de bolso e SN II

1. **Primeiro o core:** H0DN×BG1 tem **D = 6,710 no primário** (`values.primario.D`) e **D = 5,191 com Cefeidas livres** (`values.cefeidas_livres.D`). São leituras já feitas, não teste cego novo.
2. **Depois o bolso:** 7,068 usa 73,50 ± 0,81; 8,068 usa 73,994 ± 0,697; ambos usam BG1 = 0,30/68,53 e a fórmula de planejamento. São aproximações com erros de cabeçalho, não substitutos do modelo do core.
3. **SN II tailored EPM:** 3,256 é **teto só-estatístico**. Com sistemática = estatística, D ≈ **2,32** (2,318915 no JSON). Sem ponte examinada, orçamento total incompleto e presença prévia em variante astrofísica H0DN, não se chama “independente qualificada” sem essas ressalvas.

## 5. Empilhamento sem dupla contagem

Os valores do revisor permanecem marcados como **não cegos e não independentes**:

- Duas linhas, SN II + TDCOSMO‑2026: D = 4,04; 3,36 com sistemática SN II = estatística. **TDCOSMO é uma das duas linhas e já está na Fase 9 V2**; oito das 11 lentes de 2026 já estavam na amostra anterior.
- Cinco linhas, SN II + TDCOSMO‑2026 + reanálise MCP + FRB localizados + BBH–AGN estendido: D = 5,34; 4,88 com sistemática SN II = estatística. **TDCOSMO e masers são duas das cinco linhas e já são famílias da V2**; SN II, FRB e BBH–AGN não estão na V2, mas não têm ponte examinada.

Nenhum desses valores é composto aberto ou incremento a somar à V2. A Fase 9 tem cinco leitores decisórios; sua preparação V2 também pinou variantes/leitores auxiliares. A nota de delimitação está em `K04/HUBBLE/K09/NOTAS_EMPILHAMENTO_DESI_K09.md`.

## 6. DESI DR3

**Proposta [DECLARADO]: tratar como fundo até cumprir as cinco condições abaixo; decisão da gerência/operador. Sob a proposta: Fundo por padrão, não nova testemunha local.** DR1/DR2 já estão na rota D1/CAMB e BG1 contém DESI DR2. Uso testemunhal separado de DR3 exigiria, antes da leitura: pergunta e nulo; mapa Ωm/R; likelihood/covariância; variantes e veredito; pré-registro por hash; custódia e abertura única; regra contra dupla contagem com BG1/DR2. Faltam data nomeável, pacote, regra congelada e demonstração de não dupla contagem. Sem isso, DR3 é atualização de fundo não cega.

## 7. Atribuição ao operador reescrita

A antiga linha 22 do inventário foi substituída pela formulação da revisão:

> O Mapa registra que a gerência leu a resposta de 02/11 como fechamento da sexta morada e a R1 de 02/10 como bloqueio FFAT; os bytes de 02/11 não dizem isso literalmente e a R1 não tem verbatim em arquivo.

Não se atribuem ao operador as conclusões da gerência.

## 8. Outras correções documentais

- Fase 3: sequências corrigidas para **203–212, 214 e 221**; o intervalo anterior incluía indevidamente 213.
- Kernel: `TheFlowLawD1a.lean:33–46, 53–64` para a forma geral; `TheFlowLawContrast.lean:26–27, 153–170` para a razão de extremos. `ThermodynamicFriedmann.lean:124–135` não é fonte dessa lei; apoia apenas o defeito de Friedmann/errata Pantheon.
- A conclusão de ausência continua delimitada às fontes consultadas; não virou prova universal de inexistência nem exclusão ampliada da leitura intermediária.

## 9. Arquivos e validação

- Corrigido: `HUBBLE_JA_EXAMINADO_K04.md`.
- Criados: esta errata e `K04/HUBBLE/K09/NOTAS_ROTAS_PONTES_K09.md`, `NOTAS_EMPILHAMENTO_DESI_K09.md` e `VALIDACAO_DOCUMENTAL_K09.json`.
- Atualizados: `MEDIDAS_PLANEJAMENTO_K04.md/.json`, `medidas_planejamento.py`, `verificar_relatorio.py` e `SHA256SUMS_K04_HUBBLE.json`.
- A validação é documental e algébrica: confere D e identificadores, presença das nove rotas, pontes, ressalvas, preservação REV0/REV1/REV2 e hashes dos bytes finais. Nenhum vetor observado foi lido e nenhuma estatística observada nova foi calculada.

`NOT_FALSIFIED` não é `CONFIRMED`; o gate não se move.
