# ERRATA R3 — precisão sobre extensões normais de estados

## 0. Escopo e preservação

Esta errata altera somente a formulação sobre extensão de estados em `../../GH_III1_R2.md`, atualmente nas linhas 148–150 e na linha 165. Não altera Sakai–Tomiyama, GH-R/GH-S, a conjectura, `MONTAGEM_3MAIS1_R2.md` nem `K02/candidatas/GH_III1.lean`. Não há `ENTREGA`, `REGISTRO` ou depósito.

A versão imediatamente anterior foi preservada em `REV1/GH_III1_R2.md`. `REV0` e `ERRATA_GH_III1_R2.md` permanecem intactos como histórico.

Hashes lidos por script:

- GH anterior, em REV1: `dff5a66c167fab789a8781f53429faab44600218bae82616fd130a1e0bda5b59`.
- GH com a presente precisão: `0f5e367db38f68c3aa3ac15e19cb10ea8d557a5f7c2d24ac88b0bf25edff9745`.
- MONTAGEM, inalterado: `3eeb6c56ffc8ad336505e1adc908292b6d0305e90512bf602910650baa692dbb`.
- Lean antiga, inalterada: `8b56968adeaeaeef6a373ed2f0ddd53ada78ced5aebec35f63a001df653e4a10`.

## 1. Precisão material

A redação anterior dizia que “a obstrução é à extensão normal dos estados de `π(M)` para `\widehat M`”. Essa frase era ampla demais.

**[KNOWN, a conferir]** Blackadar, Cor. III.2.1.10, garante que **todo estado normal numa subálgebra de von Neumann admite extensão normal à álgebra ambiente, sem esperança condicional**. Logo, extensões normais **individuais** de estados de `π(M)` a `\widehat M` existem e não são o obstáculo. [Blackadar 2006, DOI 10.1007/3-540-28517-2, Cor. III.2.1.10, KNOWN, a conferir](kimi-cite://web?url=https%3A%2F%2Fdoi.org%2F10.1007%2F3-540-28517-2 "citation")

Restringir estados de `\widehat M` a `π(M)` também continua sendo automático e não depende de esperança condicional.

## 2. Formulação corrigida

A obstrução agora é delimitada a dois níveis:

1. **Esquema coerente:** a existência de um esquema coerente de extensão via UMA esperança condicional normal, positiva, unital e `π(M)`-bimodular. Sakai–Tomiyama, via Haagerup–Musat Lema 2.11, exclui precisamente essa esperança condicional, não as extensões individuais. [Haagerup–Musat 2007, arXiv:0706.3463v2, Lema 2.11, KNOWN, a conferir](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F0706.3463v2 "citation")
2. **Compatibilidade métrica:** a existência de extensões equivariantes compatíveis com Lip-normas, constantes `C¹` e truncamentos. A bidualidade não fornece essas compatibilidades; elas permanecem parte de `H_Tak` e **[OPEN]**.

Se tal esperança condicional `E` existisse, `φ↦φ∘E` daria o esquema coerente do primeiro nível. Sua inexistência não elimina as extensões normais individuais garantidas por Blackadar.

## 3. O que não mudou

- GH-S continua com `d_GH≤γ_M+γ′_M`.
- GH-R continua com `dist_Q≤max{γ_M,γ′_M}` sob o mesmo pacote `C¹`, sem ponte nova.
- GH-R e GH-S não são apresentadas como universalmente equivalentes; `qGH=GH` continua falso em geral.
- A conjectura III₁ permanece **[CONJECTURE]**.
- A inexistência de esperança condicional normal de álgebra semifinita sobre subálgebra tipo III permanece **[KNOWN, a conferir]** por Sakai–Tomiyama/Haagerup–Musat, sem derivação autônoma.
- A Lean antiga continua arquivada como oca, sem edição ou recompilação.

A tabela da §8 agora registra explicitamente: **extensões normais INDIVIDUAIS existem e não são o obstáculo; o bloqueio é o esquema coerente/equivariante compatível com a métrica.**
