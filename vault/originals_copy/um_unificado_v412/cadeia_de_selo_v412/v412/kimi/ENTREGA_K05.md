# ENTREGA K05 — matemática, rodada 2, com o adendo do campo

- [DERIVED] **T1:** o teorema final exige `H_K̂`, `H_erg` e, para a TGL, `H_TGL-horizon [OPEN]`; então `Fix=L(ℝ)=W*(K̂)` e `Φ_t→E_τ` σ-fracamente.
- [REAL] **Lean T1:** fórmula gaussiana, `Fix={K}′` e convergência ao pinching na base diagonal compilaram com `RC: 0`; espectro simples e a embalagem covariante ficam fora do Lean.
- [DERIVED + KNOWN] **Montagem (4,0):** quatro círculos foram identificados ao toro spin trivial `T⁴`, com `J`, orientação, finitude e dualidade de Poincaré; `T³×S¹` é ímpar×ímpar.
- [INPUT (H)/OPEN] **Assinatura (1,3):** há moldura publicada para análise de Krein e sinais, não para todos os axiomas; permanece `(H)`.
- [CONJECTURE] **GH–III₁:** continua conjectura. O degrau II∞ cobre compressão, GH-S e GH-R sob `C¹`; a descida por Takesaki continua aberta e `qGH≤GH`, não igualdade geral.
- [DERIVED sobre registro selado] **τ★ em P1:** `ħ/(1 eV)` excede Kim por **15,4058 ordens** e `ħ/(β·1 eV)` por **17,3255**; as âncoras Planck/G passam.
- [DERIVED] **Número puro:** `1,1/β,√2,2π,4π` não são distinguidos pelas cotas P1; `max/soma/quadratura` dão a escala, mas não derivam o regime Hubble.
- [REAL + DERIVED] **Três frequências:** `√2/τ`, `2/τ` e `2/(βτ)` foram separadas; a identificação física da autoconsistência sem β segue aberta.
- [REAL] **Campo:** o cânone tem duas equações, `ξ_A=1/6` e `ξ_P=β`, sem ação única localizada; o `2` do psíon sustenta a segunda massa e não se toca.
- [DERIVED] **Lagrangiana fundadora:** na escrita cuja EOM tem `2ξ_L R`, o valor conforme é `ξ_L=1/12`; a régua muda `|Ψ|²`, que é carga modular.
- [DECLARADO] **Cinco candidatas de campo:** nenhuma produz as duas equações, preserva o 2/massa e fecha tipos, gauge, carga, radical e loop; não se decide o ½ do box.
- [REAL] **Compilação:** duas candidatas novas, T1 e τ★, com zero `sorry` e somente `propext`, `Classical.choice`, `Quot.sound`, em sandbox Lean 4.31.0.
- [DECLARADO] **Atos do operador:** responder à pergunta atualizada de τ★; a transferência `H_TGL-horizon` segue como hipótese física a provar, sem escolher candidata de campo nesta rodada.
- [REAL] **Custódia:** revisada internamente; T1/GH/campo têm erratas ao lado e versões preservadas; nenhum kernel, `um.py`, Artigo A, pedra ou dado observado foi alterado.

## A. T1 — o que fecha e o que continua físico

O fechamento está em `T1_FECHADO.md`. O Lema C usa Digernes–Takesaki e a fatia de Tomita para obter `λ(ℝ)′∩M̂=M_φ⊗̄L(ℝ)`. Sob `H_K̂`, `K̂=F(ĥ)≥0` é afiliado a `L(ℝ)` com `F` essencialmente injetiva; sob `H_erg`, `M_φ=ℂ1`. A fórmula para `F` arbitrária não injetiva fica `[OPEN]`.

O Lema A identifica os pontos fixos ao comutante relativo. O Lema B usa o traço canônico II∞, com semifinitude demonstrada por `y_i=x^{1/2}e_ix^{1/2}` e a convergência `L²→L¹→σ-fraca`. A prova de Borchers–Mautner para a cunha exige BW, condição espectral, vácuo único e Reeh–Schlieder; a identificação com o horizonte TGL não foi demonstrada.

A caixa final não deve ser citada sem as três hipóteses. A antiga `T1.lean` fica preservada como fora do alvo; a nova candidata cobre a face diagonal finita, não o caso contínuo.

## B. Montagem 3+1

`MONTAGEM_3MAIS1_R2.md` identifica explicitamente o produto ao `T⁴`. O escalonamento `λ=β^(−1/2)` dá `d_λ=λ⁻¹d` e exige `c_λ=λ⁻⁴c` para manter a orientação normalizada; `J`, finitude e Poincaré permanecem.

Em `(1,3)`, van den Dungen cobre a análise de Krein e Bizi–Brouder–Besnard os sinais/dimensões mod 8. Primeira ordem, finitude, orientação, dualidade de Poincaré, K-homologia de Krein e a regra geral de produto ficam abertos. A lista de axiomas a nomear está no documento.

## C. GH–III₁

`GH_III1_R2.md` corrige a afirmação clássica: Rieffel publica `qGH≤GH`, com exemplo de desigualdade estrita. O degrau II∞ tem três lemas:

1. compressão positiva, unital, `C¹`-contrativa e convergente;
2. sob as demais hipóteses `C¹`/Lip-norma/topologia, GH-S com `d_GH≤γ_M+γ′_M` e GH-R com `dist_Q≤max{γ_M,γ′_M}`;
3. Takesaki fornece bidualidade e pontos fixos, não descida métrica; Sakai–Tomiyama exclui a esperança condicional normal para III₁.

Extensões normais individuais de estados existem; a obstrução é o esquema coerente bimodular e as compatibilidades equivariantes/métricas. A antiga Lean oca fica arquivada sem alteração.

## D. τ★

`TAU_ESTRELA_R2.md` lê apenas o clock selado e registra todas as alternativas. As cotas Th atuais do core, Zn e o registro auxiliar do Atlas permanecem separados, sem fusão.

O lema dimensional separa âncora e fator puro: `ħ,c` não formam tempo; `G` ou energia posta é necessária. Com `u` posto, medir `G` equivale a medir `N=E_P/u`.

O `√2` da célula, o da dispersão e o numerador da frequência foram separados. A linha 199 liga os dois últimos somente quando `τ=tempoDoRetido`; identificar esse retido ao `τ★` local falha P1. O monopolo dependente de energia muda `Γ∝ω²` para `Γ∝ω³`.

`τ_eff=max(t_P,τ_hor)` dá Planck para 1 eV/Sr, `3,714×10⁻³ s` para 60 M☉ e `2,877×10¹⁸ s` para Hubble sob a hipótese crítica. Não é única nem deriva `K=E(z*)^(2β/3)`: essa lei vem de `TheFlowLawContrast`. A parede é `PAREDE_RELOGIO_E_PONTE_HUBBLE`.

## E. Campo dual — o adendo aplicado

`CAMPO_DUAL_LEVANTAMENTO_K05.md` substitui a classificação retirada pela formulação correta: duas equações convivem, sem ação única escrita que produza ambas. A lagrangiana fundadora tem escalar complexo e vetor de gauge com a forma da fala do operador, mas a identificação é `[INPUT]/[DECLARADO]`, não derivação.

As cinco candidatas foram comparadas sem escolha. Todas deixam aberta pelo menos uma ponte essencial: ação comum, dois acoplamentos, escalar×`Φ_μν`, gauge total, carga modular, `D=√K`, holonomia ou as duas equações. `PontoZeroDoPsion` permanece intacto.

## Artefatos principais

- `T1_FECHADO.md`, `MONTAGEM_3MAIS1_R2.md`, `GH_III1_R2.md`, `TAU_ESTRELA_R2.md`, `CAMPO_DUAL_LEVANTAMENTO_K05.md`.
- `PERGUNTA_K05.md` e `REGISTRO_MAPA_K05.json` — este último é proposta não registrada.
- `K05/candidatas/T1_R2.lean` e `K05/TAU/candidatas/TAU_ESTRELA_R2.lean`, com logs nos respectivos sandboxes.
- `K05/TAU/medidas/` e `K05/CAMPO/medidas_campo.json`: números reproduzíveis por script.
- `ERRATA_T1_R2.md`, `ERRATA_CAMPO_K05.md`, `K05/MONTAGEM_GH/ERRATA_GH_III1_R2.md` e `ERRATA_GH_III1_R3.md`, com as versões anteriores preservadas.

Nenhuma instalação, promoção, abertura de dado novo ou registro no Mapa foi feita. O depósito na fila usa o estatuto `DECLARADO` e a expressão “revisada internamente”.
