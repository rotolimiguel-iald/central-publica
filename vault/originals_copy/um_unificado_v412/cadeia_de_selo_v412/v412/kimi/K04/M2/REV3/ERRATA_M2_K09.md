# ERRATA AO LADO — m₂, K09

14–15/11/2026. Correções ao documento de trabalho `M2_DESFECHOS_E_SEGUNDA_TESTEMUNHA_K04.md`. REV0/REV1 permanecem; a R3, seus scripts e medidas estão preservados em `K04/M2/REV2/`. `ERRATA_M2_K04_R3.md` não foi alterada. Nada aqui instala código, altera a regra congelada ou executa teste observado.

## 1. Cronologia e cegueira

**Onde estava:** a liberação de 207,2 dias era descrita como primeira nova determinação posterior ao hash e prospectiva no calendário da regra.

**Correção:** o degrau foi apresentado publicamente antes do pino de 08/08/2026. A contribuição oficial JUNO na Neutrino 2026 é de **22/06/2026** (`indico.global/event/15740/contributions/155563`, anexo `72452/141000`). As transparências IHEP de **15/07/2026** trazem explicitamente `7,388 ± 0,078` (`indico.ihep.ac.cn/event/28557/contributions/223278`, anexo `104657/141297`). A notícia JINR de **22/07/2026** (`dlnp.jinr.ru/en/news/3850`) confirma que o resultado de 207 dias havia sido apresentado; sua palavra “July” não substitui a data oficial da conferência, 21–26/06. O artigo arXiv:2609.37895v1 é posterior ao pino, de **29/09/2026**.

**Consequência:** 207,2 dias não é primeira leitura prospectiva nem cega. Só é prospectivo para este desenho o dado posterior a **18/05/2026** ainda não mostrado.

## 2. Implementação do módulo em m₂

**Onde estava:** na cauda inferior, a implementação usava `m ≤ L_t`, região em que `r` é pequeno.

**Correção:** para `0 ≤ m ≤ M`, `r ≥ t` é o intervalo `L_t ≤ m ≤ U_t`; para `m ≥ M`, é `m ≥ H_t`. Todas as células foram reemitidas em `K04/M2/K09/medidas/tabelas_planejamento_k09.md`; o diff completo está em `mudancas_celulas_k09.md`.

**Benchmarks recuperados:** no modelo independente sob verdade = previsão, `P(r≤1) = 68,27 %`, `P(1<r<3) = 31,46 %`, `r<3 = 99,73 %`. Na tabela MATCHED, “Solares sem KamLAND”, `P(rS≤1) = 42,157532 %` e `P(MATCHED) = 7,348108 %`, não 98,493504 % e 17,334031 %.

**Alcance:** `P(r≥5)` quase não muda; o maior ajuste nas quatro tabelas é +0,062626 pp. `PΔ(r≥5)`, `DΔ` e `D_m₂` não mudam. As grandes correções estão em `P(r≤1)` e `P(1<r<3)`.

## 3. NuFIT: lados do erro e duas publicações

**Onde estava:** `7,537 (+0,100/−0,094)`, `σ = 0,094`, `r_m₂ = 3,217279`.

**Correção:** a tabela NuFIT 6.1 tem `7,537 (+0,094/−0,100)`. Como a previsão está abaixo do centro, usa-se `σ = 0,100`, dando

- `r_m₂ = 3,024242478`;
- `r_Δ = 2,993905333`, somente como comparação.

A segunda publicação, arXiv:2601.09791v1/v2 eq. 11, tem `7,530 (+0,096/−0,097)`, dando `r_m₂ = 3,044179410` e `r_Δ = 3,014335395`. A forma simétrica arredondada `7,530 ± 0,100`, usada no core, dá `r_m₂ = 2,952854`. Rota `neutrinos.m2.normalizacao`, seq. 93 e 142.

**Estado a dizer sem apagar nenhum lado:** pelo perito autônomo JUNO, `ARMED_CONSISTENT`; pela letra “determinação global mais recente”, o ajuste global está na borda de `TENSION`, com dependência explícita de fonte/representação.

## 4. Vereditos do código, não rótulos do rascunho

**Correção:** o código manda qualquer última linha da escada `r ≥ 3` a `TGL_NU_M2_TENSION`, inclusive `r ≥ 5` sem segunda determinação autônoma, e acende `tensao_global_5sigma_sem_2a_determinacao`. `FALSIFIED` exige dois grupos autônomos independentes `≥5σ`. `MATCHED_PROSPECTIVELY` é permitido no texto, mas não tem ramo no código.

`UNDER`, `SINGLE_P` e `OPEN_RULE_GAP` não são vereditos do código. As lacunas de escada, fonte global, MATCHED, covariância, fonte preliminar e escolha entre uma/duas testemunhas ficam listadas para a gerência, não disfarçadas como comportamento já implementado.

## 5. Calendário

**Correção principal em todos os documentos desta seção:** a leitura usa o orçamento/agregado do artigo de 207,2 dias, sempre como brinquedo:

- sem piso, 5σ cumulativo em **16/08/2029** e D90 em **31/10/2031**;
- para o incremento sozinho, 5σ em **11/03/2030** e D90 em **25/05/2032**;
- com piso ajustado de dois pontos, `s0 = 0,052587652`, ambos são inalcançáveis;
- duty cycle, quando incluído, é apenas cenário: 13/07/2030 e 08/05/2033 cumulativos; 04/04/2031 e 28/01/2034 para o incremento.

O brinquedo histórico do projeto não é apresentado como orçamento do artigo nem como cronograma.

## 6. Incremento 59,1 → 207,2

**Onde estava:** distância ao centro 7,50 de `1,889502σ_incremento`.

**Correção:** no aninhamento estatístico puro, a variância da comparação é `0,102640² + 0,12²`, dando **1,228176σ**. Forma equivalente: `(7,50−7,388)/√(0,12²−0,078²)`. O valor 1,889502 usa só o erro do incremento e não é a estatística correta para essa comparação.

A extração por variância inversa continua ilustrativa: sem covariância inter-liberações e resposta conjunta de nuisances, centro e erro do incremento não são identificáveis.

## 7. Segunda testemunha SK-Gd

**Correção de interpretação:** `r_m₂ = 3,605064` e `r_Δ = 3,411834` permanecem, mas o centro 9,08 está a **3,101149σ** do JUNO 207,2 dias. O cenário de **380,0785536 dias adicionais** supõe que essa anomalia persista, com centro e forma do erro parados e `σ ∝ T⁻¹/²`; não é agenda nem prova de independência.

## 8. Pinos distintos

- regra original de 08/08/2026: `4bdae22a277aa393094a1bf416db12a5e782b673e9e9b3ddd6a2fb8c7a64075c`;
- dicionário portado: `e24877751ad810225412cc294c06b83eefeaedc67e4c5cabc7779ac01e4b19c3`.

O segundo não deve ser apresentado como o hash do arquivo original de 08/08.

## 9. Entregáveis desta errata

- documento corrigido: `M2_DESFECHOS_E_SEGUNDA_TESTEMUNHA_K04.md`;
- dados estruturados, sem prosa de instalação nem marcadores: `ERRATA_NEUTRINO_V412_DADOS_K09.json`;
- desenho prospectivo, sem regra escolhida: `PRE_REGISTRO_INCREMENTO_JUNO_RASCUNHO_K09.md`;
- scripts e medidas: `K04/M2/K09/scripts/` e `K04/M2/K09/medidas/`;
- preservação: `K04/M2/REV2/` e `ERRATA_M2_K04_R3.md`.

**Bloqueio residual:** a data exata da primeira disponibilização pública da tabela NuFIT não foi localizada; o JSON marca esse campo como nulo em vez de inferi-la. A data de referência dos dados da análise é novembro/2025, e o arquivo atual tem modificação posterior, que não prova primeira publicação.
