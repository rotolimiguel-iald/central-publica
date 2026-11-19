# ERRATA M2 K04 R3 — duas correções de modelo, ao lado de REV0 e REV1

**Escopo:** somente planejamento documental. Nenhum dado foi aberto e nenhum teste observado foi executado. REV0 permanece intacto em `K04/M2/REV0/`; R2 está preservada em `K04/M2/REV1/`, com `hashes_REV1.txt`. Esta errata não instala nada no core, não altera a regra frozen e não substitui decisão do operador.

## R3.1 — Variância condicional correta

**Antes, em R2:** a variância de “verdade = previsão condicionada a X0” usava indevidamente a variância total cumulativa.

**Correção:**

\[
E[X\mid X_0=x_0]=\mu+\frac{C}{0,078^2}(x_0-\mu),
\qquad
\operatorname{Var}(X\mid X_0)=s^2-\frac{C^2}{0,078^2}.
\]

Não se soma \(0,078^2+s^2-2C\). Com `C = 0`, a condicional reduz exatamente a (a2): média \(\mu\) e variância \(s^2\). No brinquedo `C = s²`:

\[
\operatorname{Var}(X\mid X_0)=s^2(1-s^2/0,078^2).
\]

Toda a tabela (b2), incluindo PDelta, foi recalculada por CDF analítica. As tabelas (a1), (a2) e (b1) não mudam.

| precisão | σ condicional | P(r≥5), frozen | PΔ(r≥5) |
|---|---:|---:|---:|
| 0,7 % | **0,038714426** | **0,000044650 %** | **0,000033222 %** |
| Tabela 6, σ=0,024 | **0,022835662** | **0,000201329 %** | **0,000181779 %** |

Esses valores coincidem com os benchmarks do revisor. A covariância real continua `[OPEN]`; `C=s²` é apenas brinquedo.

## R3.2 — O piso nominal é independente do piso full‑reactor

**Antes, em R2:** “inteiramente nominal” reutilizava o piso calculado para full‑reactor.

**Correção:**

\[
{\rm floor\_full\_sq}=0,024^2-a_{\rm full}/2009,
\]

\[
{\rm floor\_nominal\_sq}=0,024^2-a_{\rm nom}/2191 .
\]

Com `a_full = 92×0,074²` e `a_nom = 100×0,074²`, resulta `s0_full = 0,018034202` e **`s0_nominal = 0,018057366`**. Para cada alvo:

\[
T_{\rm full}=a_{\rm full}/(target^2-{\rm floor\_full\_sq}),
\qquad
T_{\rm nom}=a_{\rm nom}/(target^2-{\rm floor\_nominal\_sq}) .
\]

| alvo | full‑reactor | inteiramente nominal |
|---|---|---|
| 5σ | 869,416 d → **31/03/2028** | 946,383 d → **29/03/2028** |
| D90 | 2031,675 d → **19/09/2031** | 2215,813 d → **19/09/2031** |

Os valores anteriores 15/05/2028 e 18/09/2031, e a data nominal R2 12/09/2031, ficam apenas em REV0/REV1 como histórico/erroneamente etiquetados. **Tudo é brinquedo decomposição, não cronograma nem precisão inventada.**

## Menores corrigidos ao lado

- **`r_P ≤ 1` com S realmente `ABSENT`:** segue `UNDER` se `D_P<5` e `ARMED_CONSISTENT` se `D_P≥5`. Só `MATCHED` exige duas independências a ≤1σ; a probabilidade conjunta de MATCHED é zero somente nesse estado.
- **Hyper‑Kamiokande:** a referência agora é o documento de status da colaboração, que descreve tanque em 2026, PMTs em 2027 e commissioning antes dos primeiros dados em **2028**. O cenário de cinco anos continua tentativa posterior, não data de precisão assegurada. [Status of the Hyper‑Kamiokande experiment, 2026](kimi-cite://web?url=https%3A%2F%2Findico.cern.ch%2Fevent%2F1568942%2Fcontributions%2F6841210%2F "citation")
- **SNO+:** a previsão de três anos é antiga; calendário atual e precisão correspondente ficam `[OPEN]`, não promessa atual.

## Reprodutibilidade

`K04/M2/scripts/medidas_planejamento.py` reproduz todos os números por CDF analítica, sem simulação. Foram atualizados `resultados_planejamento.json`, `tabelas_planejamento.md`, `execucao_planejamento.txt`, os dois documentos principais e `ERRATA_M2_K04_R2.md`. Os hashes desta revisão estão em `hashes_R3.txt`.
