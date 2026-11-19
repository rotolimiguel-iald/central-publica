# ERRATA — GH_III1_R2: GH-R sob `C¹` e obstrução por Sakai–Tomiyama

## 0. Escopo e preservação

Esta errata corrige dois pontos de `../../GH_III1_R2.md`, sem tocar `MONTAGEM_3MAIS1_R2.md` nem `K02/candidatas/GH_III1.lean`. Não há `ENTREGA`, `REGISTRO` ou depósito.

A versão anterior foi integralmente preservada em `REV0/GH_III1_R2.md`. Hashes lidos por script:

- GH anterior, em REV0: `08d43701e8e843b76ff7b88fb3ba20573f56f3327a6706737c6f7b83f68e62e6`.
- GH corrigido: `dff5a66c167fab789a8781f53429faab44600218bae82616fd130a1e0bda5b59`.
- MONTAGEM, inalterado: `3eeb6c56ffc8ad336505e1adc908292b6d0305e90512bf602910650baa692dbb`.
- Lean antiga, inalterada: `8b56968adeaeaeef6a373ed2f0ddd53ada78ced5aebec35f63a001df653e4a10`.

## 1. GH-R já segue do mesmo pacote `C¹`/Lip-norma

### Redação anterior preservada em REV0

O Lema II∞-2 apresentava apenas GH-S e dizia que “para GH-R, exige-se uma ponte adicional”. A seção sobre o círculo repetia que GH-R precisaria de ponte nova.

### Correção

**[KNOWN, a conferir]** Kaad–Kyed, Observação 3.7, afirma que o Teorema 5 de van Suijlekom também vale com GH-S substituída pela qGH de Rieffel, via Proposição 2.14 do trabalho anterior dos mesmos autores. Sob as mesmas hipóteses `C¹`/Lip-norma, com `C=C′=1`, valem simultaneamente:

`d_GH((S(E_M),d_M),(S(E),d)) ≤ γ_M+γ′_M → 0`

e

`dist_Q((E_M,L_M),(E,L)) ≤ max{γ_M,γ′_M} → 0`.

Na Proposição 2.14, os termos de diâmetro são `diam·|1−1/C|` e `diam′·|1−1/C′|`; eles se anulam quando `C=C′=1`. Não há ponte adicional a exigir. [Kaad–Kyed 2023, arXiv:2212.10874v2, Obs. 3.7, KNOWN, a conferir](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2212.10874v2 "citation"), [Kaad–Kyed 2022, arXiv:2205.06043v1, Prop. 2.14, KNOWN, a conferir](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2205.06043v1 "citation")

**Círculo/Toeplitz [KNOWN, a conferir].** A aproximação `C¹` construída por van Suijlekom para o círculo fornece, portanto, convergência tanto em GH-S como em qGH de Rieffel. A frase anterior exigindo ponte nova foi removida em todas as ocorrências.

**Distinção preservada.** GH-R e GH-S não são universalmente equivalentes; o Teorema A de Kaad–Kyed continua sendo citado. Rieffel continua dando `qGH≤GH`, não `qGH=GH`, com o contraexemplo clássico `Y={0,1,2}`, `Z={0,3}`: `qGH=1/2<1=GH`. Convergência simultânea sob `C¹` não contradiz nenhum desses resultados.

## 2. Obstrução por esperança condicional: referência e direção dos estados

### Erro anterior preservado em REV0

A prova usava `μ(E(y))=τ(y)` sem ter assumido `τ∘E=τ`. Essa identidade não é válida sob as hipóteses apresentadas e toda a derivação autônoma foi removida.

### Correção

**[KNOWN, a conferir; não DERIVED]** Sakai–Tomiyama, reproduzido por Haagerup–Musat no Lema 2.11, estabelece que, se `N` é semifinita e `M⊆N` é de tipo III, **não existe esperança condicional normal de `N` sobre `M`**. Como `\widehat M` é II∞ e `π(M)` é III₁, o teorema se aplica diretamente, sem qualquer hipótese `τ∘E=τ` e sem exigir fidelidade de `E`. [Haagerup–Musat 2007, arXiv:0706.3463v2, Lema 2.11, KNOWN, a conferir](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F0706.3463v2 "citation")

**Direção corrigida.** Se `E:\widehat M→π(M)` existisse, `φ↦φ∘E` permitiria **estender** estados normais de `π(M)` a `\widehat M`. A restrição de estados de `\widehat M` a `π(M)` já é automática e não depende de `E`. A obstrução relevante para a descida é, portanto, à extensão normal dos estados de `π(M)` para o núcleo, não à restrição no sentido contrário.

## 3. Coerência global revisada

Foram atualizados conjuntamente:

- o veredito da §0;
- a tabela de literatura da §3;
- a correção do círculo na §4;
- o Lema II∞-2, agora intitulado “Critérios GH-S e GH-R”;
- o Lema II∞-3, agora com prova por referência e direção de estados corrigida;
- a tabela de estatutos da §8;
- as referências da §10 e o bloqueio final.

A conjectura III₁ permanece **[CONJECTURE]**. O pacote `C¹` da casa, as topologias e a descida por Takesaki continuam **[OPEN]**; nenhum resultado foi promovido a teorema incondicional.

| item | estatuto corrigido |
|---|---|
| GH-S sob `C¹` | **[KNOWN, a conferir, condicional]**, `d_GH≤γ_M+γ′_M`. |
| GH-R sob o mesmo `C¹` | **[KNOWN, a conferir, condicional]**, `dist_Q≤max{γ_M,γ′_M}`; sem ponte nova. |
| Toeplitz/círculo | **[KNOWN, a conferir]**, converge em GH-S e qGH pela aproximação `C¹`. |
| Esperança condicional normal | **[KNOWN, a conferir]**, inexistente por Sakai–Tomiyama/Haagerup–Musat Lema 2.11. |
| GH-III₁ geral | **[CONJECTURE]**; faltam torção, Lip-norma/topologia, `C¹` e `H_Tak`. |

## 4. Notas e arquivos não alterados

- `MONTAGEM_3MAIS1_R2.md` não foi editado.
- `K02/candidatas/GH_III1.lean` não foi editado, movido ou recompilado.
- `ARQUIVO_GH_III1_OCA.md` continua descrevendo apenas a antiga tipagem oca; seu diagnóstico não foi alterado.
- `REV0/GH_III1_R2.md` é a única cópia arquivada da redação anterior; os erros ficam preservados nela, não apagados da história.
