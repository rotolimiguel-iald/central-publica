# ERRATA AO LADO — m₂, K09

14–15/11/2026. Correções ao documento de trabalho `M2_DESFECHOS_E_SEGUNDA_TESTEMUNHA_K04.md`. REV0/REV1 permanecem; a R3, seus scripts e medidas estão preservados em `K04/M2/REV2/`; o estado K09 anterior ao adendo de 15/11 está em `K04/M2/REV3/`; `ERRATA_M2_K04_R3.md` não foi alterada. Nada aqui instala código, altera a regra congelada ou executa teste observado.

## 1. Cronologia do número de 207,2 dias: dois eixos

**Onde estava:** a liberação de 207,2 dias era descrita como primeira nova determinação posterior ao hash e prospectiva no calendário da regra.

**Correção em dois eixos, sempre juntos:**

1. **Em relação à previsão publicada:** a tese do neutrino — “tese” = o que o título e o resumo afirmam — é de 2025 (Zenodo 17372599, 16/10; Zenodo 17526619, 04/11), e os dois artigos não contêm a fórmula nem o valor 8,51 [DECLARADO pelo revisor da conferência]. O valor aparece no acervo em **22/01/2026** (`complemento ao manifesto.docx`, sha256 `83ba9e81…31f6`; data do corpo, do docProps e do mtime, **sem carimbo externo**) e na publicação Zenodo em **17/02/2026** (Zenodo 18674475; `created` 20/02/2026; PDF local sha256 `f4150623…ba48`). O número JUNO de 207,2 dias veio depois dessa previsão publicada.
2. **Em relação ao pino da função de veredito:** o pino é **08/08/2026**. A apresentação do degrau em **22/06/2026** é `[DECLARADO]`, porque não há resposta crua guardada; a confirmação explícita do valor é de **15/07/2026** (IHEP, contribuição 223278, anexo 104657/141297); a notícia JINR é de **22/07/2026**. O artigo arXiv:2609.37895v1 é posterior ao pino, de **29/09/2026**.

**Consequência:** a função de veredito foi hasheada depois de o número de 207,2 dias ser público; a previsão publicada é anterior a esse número. Os dois artigos de 2025 não contêm a fórmula nem o valor [DECLARADO pelo revisor da conferência], e as entradas da fórmula não usam dado de neutrino. Esta nota fala só de datas e das entradas da fórmula; não diz o que o autor leu ou deixou de ler. A amostra de 207,2 dias acumula a de 59,1; não são determinações independentes; a cegueira dita é a do número, não a dos dados. Só um **número** do JUNO tornado público pela primeira vez depois de 08/08/2026 (e antes de qualquer acesso do selo) é posterior à previsão publicada e ao hash da regra; o dado tomado depois de **18/05/2026** `[DECLARADO, sem resposta crua guardada]`, ainda não mostrado `[DECLARADO]`, não é, por si só, posterior aos dois marcos.

**59,1 dias:** o degrau de 59,1 d era público (18/11/2025) quando o valor foi escrito (22/01/2026) — anterior ao valor público e anterior ao pino de 08/08/2026 —, portanto é retrodição sem ajuste, não leitura prospectiva do valor.

## 2. Implementação do módulo em m₂

**Onde estava:** na cauda inferior, a implementação usava `m ≤ L_t`, região em que `r` é pequeno.

**Correção:** para `0 ≤ m ≤ M`, `r ≥ t` é o intervalo `L_t ≤ m ≤ U_t`; para `m ≥ M`, é `m ≥ H_t`. Todas as células foram reemitidas em `K04/M2/K09/medidas/tabelas_planejamento_k09.md`; o diff completo está em `mudancas_celulas_k09.md`.

**Benchmarks recuperados:** no modelo independente sob verdade = previsão, `P(r≤1) = 68,27 %`, `P(1<r<3) = 31,46 %`, `r<3 = 99,73 %`.

**MATCHED:** a tabela usa `X_P ~ N(7,388,0,078²)` e `X_S ~ N(centro_S,σ_S²)`, não o modelo (a1) com variância futura adicionada. Em “Solares sem KamLAND”, `P(rS≤1) = 42,157532 %` e `P(MATCHED) = 7,348108 %`, não 98,493504 % e 17,334031 %.

**Alcance:** `P(r≥5)` quase não muda; o maior ajuste nas quatro tabelas é +0,062626 pp. `PΔ(r≥5)`, `DΔ` e `D_m₂` não mudam. As grandes correções estão em `P(r≤1)` e `P(1<r<3)`.

## 3. NuFIT: lados do erro e duas publicações

**Onde estava:** `7,537 (+0,100/−0,094)`, `σ = 0,094`, `r_m₂ = 3,217279`.

**Correção:** a tabela NuFIT 6.1 tem `7,537 (+0,094/−0,100)`. Como a previsão está abaixo do centro, usa-se `σ = 0,100`, dando `r_m₂ = 3,024242478` e `r_Δ = 2,993905333`.

A segunda publicação, arXiv:2601.09791v1/v2 eq. 11, tem `7,530 (+0,096/−0,097)`, dando `r_m₂ = 3,044179410` e `r_Δ = 3,014335395`. A forma simétrica arredondada `7,530 ± 0,100`, usada no core, dá `r_m₂ = 2,952854`. Rota `neutrinos.m2.normalizacao`, seq. 93 e 142.

**Estado a dizer sem apagar nenhum lado, com números e lado:** o core selado lê `2,952854` (representação simétrica arredondada `7,530 ± 0,100`) e devolve `ARMED_CONSISTENT`; com o erro publicado do lado da previsão seria `3,024242` (tabela) ou `3,044179` (eq. 11) e o rótulo seria `TENSION`; a letra não escolhe; escolher é do operador; `TENSION` não é falsificação. O perito autônomo JUNO (R3) do core carrega o degrau de 59,1 dias [DECLARADO pelo revisor da conferência]; se o perito (R3) fosse atualizado para 207,2 d, a razão seria `1,937997 (< 3)`.

## 4. Vereditos do código, não rótulos do rascunho

O código manda qualquer última linha da escada `r ≥ 3` a `TGL_NU_M2_TENSION`, inclusive `r ≥ 5` sem segunda determinação autônoma, e acende `tensao_global_5sigma_sem_2a_determinacao`. `FALSIFIED` exige dois grupos autônomos independentes `≥5σ`. `MATCHED_PROSPECTIVELY` é permitido no texto, mas não tem ramo no código.

`UNDER`, `SINGLE_P` e `OPEN_RULE_GAP` não são vereditos do código. As lacunas de escada, fonte global, MATCHED, covariância, fonte preliminar e escolha entre uma/duas testemunhas ficam listadas para a gerência e o operador, sem recomendação embutida.

## 5. Calendário: Δm² e m₂ lado a lado

A leitura usa o agregado do artigo de 207,2 dias, sempre como brinquedo. O veredito continua em m₂; as datas em Δm² são comparação.

| Alvo | Métrica | Data cumulativa | Data do incremento |
|---|---|---|---|
| 5σ | Δm² | 16/08/2029 | 11/03/2030 |
| 5σ | m₂ | 01/08/2029 | 25/02/2030 |
| D90 | Δm² | 31/10/2031 | 25/05/2032 |
| D90 | m₂ | 08/10/2031 | 02/05/2032 |
| r=3 | Δm² | 08/03/2027 | 01/10/2027 |
| r=3 | m₂ | 03/03/2027 | 26/09/2027 |

Com o piso ajustado de dois pontos, `s0 = 0,052587652`, 5σ, D90 e r=3 são inalcançáveis. Duty cycle, se usado, é só cenário e está em `calendario_metricas_duplas_k09.md`. O brinquedo histórico do projeto não é apresentado como orçamento do artigo nem como cronograma.

## 6. Incremento 59,1 → 207,2

**Onde estava:** distância ao centro 7,50 de `1,889502σ_incremento`.

**Correção:** no aninhamento estatístico puro, a variância da comparação é `0,102640² + 0,12²`, dando **1,228176σ**. Forma equivalente: `(7,50−7,388)/√(0,12²−0,078²)`. O valor 1,889502 usa só o erro do incremento e não é a estatística correta para essa comparação.

A extração por variância inversa continua ilustrativa: sem covariância inter-liberações e resposta conjunta de nuisances, centro e erro do incremento não são identificáveis.

## 7. Segunda testemunha SK-Gd

`r_m₂ = 3,605064` e `r_Δ = 3,411834` permanecem, mas o centro 9,08 está a **3,101149σ** do JUNO 207,2 dias. O cenário de **380,0785536 dias adicionais** supõe que essa anomalia persista, com centro e forma do erro parados e `σ ∝ T⁻¹/²`; não é agenda nem prova de independência.

## 8. Pinos distintos

- `frozen_hash` do objeto congelado de 08/08/2026: `4bdae22a277aa393094a1bf416db12a5e782b673e9e9b3ddd6a2fb8c7a64075c`;
- sha256 do arquivo `02_frozen_neutrino_m2_v2.py`: `2564d7c944f1d338d0bafb96a294a2bdc97fdd617f36c1d5511db5ca868771f0`;
- sha256 do arquivo `02_frozen_neutrino_m2_v2_resultado.json`: `6f0963a54b7d2f5a68b711f77beb9d743448d44443d7b4ebb06ba0cf1817239b`;
- dicionário portado no core: `e24877751ad810225412cc294c06b83eefeaedc67e4c5cabc7779ac01e4b19c3`.

O JSON usa nomes de campo explícitos para não sugerir que o hash do objeto seja o hash de arquivo.

## 9. Entregáveis desta errata

- documento corrigido: `M2_DESFECHOS_E_SEGUNDA_TESTEMUNHA_K04.md`;
- dados estruturados, sem prosa de instalação nem marcadores: `ERRATA_NEUTRINO_V412_DADOS_K09.json`;
- desenho prospectivo, sem regra escolhida: `PRE_REGISTRO_INCREMENTO_JUNO_RASCUNHO_K09.md`;
- scripts e medidas: `K04/M2/K09/scripts/` e `K04/M2/K09/medidas/`;
- preservação: `K04/M2/REV2/` (R3), `K04/M2/REV3/` (K09 anterior ao adendo) e `ERRATA_M2_K04_R3.md`;
- correções específicas do adendo: `ERRATA_M2_K09_15nov.md`.

**Bloqueio residual:** a data exata da primeira disponibilização pública da tabela NuFIT não foi localizada; o JSON marca esse campo como nulo em vez de inferi-la. A data de referência dos dados da análise é novembro/2025, e o arquivo atual tem modificação posterior, que não prova primeira publicação.

## 10. Os dois mundos, sem escolha (achado ALTO-1 da conferência de 15/11)

A frase anterior da K09, que apresentava a tensão do primário como o desfecho mais provável, valia só no mundo em que o valor verdadeiro é o centro público (a1/b1) — e a condição estava escondida. Vale a forma dos dois mundos, sem escolher: sem segunda testemunha elegível, o canal só devolve `ARMED_CONSISTENT` ou `TENSION`; nenhum dos dois falsifica (parede medida). Se o valor verdadeiro for o centro público de hoje (a1/b1), o primário passa de `r=5` com `P ≈ 65 %` no desenho da Tabela 6; se a previsão for verdadeira (a2/b2), devolve `ARMED_CONSISTENT` com `P ≈ 99,7 %`. Esta errata **não adota nenhuma das duas hipóteses**.

## 11. Itens do código para a gerência [DECLARADO pelo revisor da conferência]

O `um.py` selado afirma em L4222–4225, L4241, L4243 e L4620 que a derivação foi “publicada 2025, Zenodo 17526619”, enquanto L2944–2950 (v182) já a retirou; a K09 não mencionava essa contradição. Fica listada aqui como item para a gerência (C1 a C3 do rascunho R1 da gerência). Esta errata não abre o kernel; a leitura das linhas é do revisor da conferência.
