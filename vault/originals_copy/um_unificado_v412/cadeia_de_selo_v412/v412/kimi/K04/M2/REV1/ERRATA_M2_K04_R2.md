# ERRATA M2 K04 R2 — cinco correções de revisão, ao lado de REV0

**Escopo:** somente planejamento documental. Nenhum dado foi aberto e nenhum teste observado foi executado. A versão anterior completa está preservada em `K04/M2/REV0/`, com `hashes_REV0.txt`. Esta errata não instala nada no core, não altera a regra frozen e não substitui decisão do operador.

## R2.1 — D não zera sob “verdade = previsão”

**Antes:** a tabela de ramo dizia que, sob verdade = previsão, `D = 0` e todo `r<3` ia a UNDER.

**Correção:** D é sempre calculado com o centro de planejamento 7,388 e a precisão futura:

\[
D_\Delta=|7,388-7,237609466718292|/s.
\]

Logo `r<3` devolve UNDER a 0,7 %/0,5 % e `ARMED_CONSISTENT` desde 0,407121 %, **inclusive sob verdade = previsão**. O D não depende da hipótese física atribuída à verdade.

## R2.2 — Independente, cumulativo e condicional são modelos distintos

**Antes:** `N(7,388,0,078²+s²)` era usado sem delimitar o escopo e podia ser lido junto das datas cumulativas.

**Correção:** essa distribuição vale apenas para medida/incremento independente. A liberação cumulativa usa `Cov(X0,X)=C`:

\[
\operatorname{Var}(X)=0,078^2+s^2-2C.
\]

Sob verdade = previsão, condiciona-se ao valor atual observado:

\[
E[X\mid X_0]=\Delta_{\rm pred}+(C/0,078^2)(x_0-\Delta_{\rm pred}),
\]

\[
\operatorname{Var}(X\mid X_0)=0,078^2+s^2-2C-C^2/0,078^2.
\]

O exemplo aninhado `C=s²` é **brinquedo**, não covariância atribuída ao JUNO; a covariância real permanece `[OPEN]`.

Benchmarks analíticos em m₂:

| cenário | 0,7 % | Tabela 6, σ=0,024 |
|---|---:|---:|
| independente | 12,877614 % | 64,742906 % |
| cumulativo `C=s²`, brinquedo | **3,478822 %** | **66,132478 %** |

Essas probabilidades não estão ligadas às datas cumulativas √T.

## R2.3 — Dias nominais não são dias full‑reactor

**Antes:** `a = 100×0,074²` foi usado numa variável full‑reactor, e as datas 15/05/2028 e 18/09/2031 foram etiquetadas incorretamente.

**Correção:** a fonte converte 100 nominais em ≈92 full‑reactor e seis anos em 2009 full‑reactor. O brinquedo corrigido usa

\[
a_{\rm full}=92\times0,074^2,\quad
a_{\rm nom}=100\times0,074^2,\quad
s_0=0,018034202 .
\]

| alvo | full‑reactor, data convertida por 2009 dias em 6 anos | inteiramente nominal |
|---|---|---|
| 5σ | **31/03/2028** | **28/03/2028** |
| D90 | **19/09/2031** | **12/09/2031** |

As datas anteriores ficam apenas em REV0 como histórico/erroneamente etiquetadas. A aproximação D90 ≈20/09/2031 fica a um dia da rota full‑reactor e a oito dias da rota nominal; mantive os resultados exatos do script em vez de forçar a data. **Tudo é brinquedo decomposição, não cronograma nem precisão inventada.**

## R2.4 — `r ≤ 1` separado de `1 < r < 3`, e MATCHED avaliado por S

**Antes:** `r<3` escondia a condição de MATCHED e não havia avaliação conjunta P+S.

**Correção:** MATCHED exige **duas determinações independentes a ≤1σ**. A probabilidade conjunta é zero **somente quando S é realmente `ABSENT`**.

Modelo identificável apenas como brinquedo: `P~N(7,388,0,078²)`, `S~N(μ_S,σ_S²)`, `C_PS=0`. Não é prova de independência de fluxos ou nuisances.

| S | P(r_S≤1) | P(MATCHED), brinquedo C=0 | C real |
|---|---:|---:|---|
| SNO+ | 4,476223 % | **0,787778 %** | OPEN |
| SK‑Gd reator | 0,756582 % | **0,133152 %** | OPEN |
| KamLAND | 24,635184 % | **4,335586 %** | OPEN |
| Solares sem KamLAND | 98,493504 % | **17,334031 %** | OPEN |

Em todos, `P(r_P≤1) = 17,599161 %`. Para JUNO 59 d, NuFIT, Capozzi, Bari, SK‑Gd solar+reator e SNO+ reator+solar, a distribuição conjunta é **OPEN não identificável**, não zero presumido. Hyper‑K/DUNE não têm centro medido nem covariância P+S: MATCHED também é `OPEN`.

## R2.5 — Classes e datas das fontes

- **Bari 2026.a:** *paper in preparation/preliminary*; não é artigo primário publicado. Fica como estresse preliminar, não como independência publicada.
- **Hyper‑Kamiokande:** primeiros dados previstos para **2028**; o estudo de cinco anos é tentativa posterior, não data de precisão assegurada.
- **DUNE solar:** 5,9 %/100 kton·ano é previsão de **Capozzi et al., teóricos**, não da DUNE Collaboration.
- **SNO+ v4:** depositado em **04/09/2026**, antes do JUNO 207 d de 29/09, mas é revisão do mesmo conjunto. A formulação correta é **“primeira nova determinação JUNO posterior ao hash”**, não primeira medida mundial irrestrita.
- **SK‑Gd:** 3,605064σ e 380,0785536 dias permanecem como cenário condicional, não agenda nem prova de independência. A conclusão “teste sem negativo não é teste” permanece condicional à regra e ao desenho, sem universal falso.

## Reprodutibilidade

`K04/M2/scripts/medidas_planejamento.py` reproduz todos os números por CDF analítica, sem simulação. Saídas atualizadas: `resultados_planejamento.json`, `tabelas_planejamento.md`, `execucao_planejamento.txt` e `hashes_R2.txt`.
