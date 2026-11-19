# Nota de arquivamento — GH_III1.lean (tipagem oca)

**Ação:** arquivamento **por referência**, sem criar nova candidata e sem editar, mover ou apagar a fonte original.

**Fonte preservada:** `C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K02\candidatas\GH_III1.lean`.

**SHA-256, lido por script:** `8b56968adeaeaeef6a373ed2f0ddd53ada78ced5aebec35f63a001df653e4a10`.

## Diagnóstico

1. `classical_gh_self` prova apenas `ghDist X X = 0`, irrelevante para III₁.
2. `QuantumMetricSpace` não liga `State` a `Elem` por avaliação nem liga a métrica dos estados a `lip`; portanto não tipa um espaço métrico quântico no sentido exigido pela conjectura.
3. `TypeIII1GHConjecture` recebe `IsTypeIII1`, `IsSpectralTruncationOf` e `qghDist` como parâmetros livres. Há instanciações triviais que tornam o esquema falso; ele não constrói III₁, truncamentos ou qGH.
4. `typeIII1_of_named_hypothesis` é apenas `H_GH_III1 H_limit H_truncations`: modus ponens sobre a hipótese nomeada, sem conteúdo matemático novo.

## Estatuto

**[ARQUIVADA COMO OCA — não é pedra, não é prova, não entra no kernel].** A conjectura GH-III₁ não precisa de candidata Lean. O trabalho matemático pertinente está em `../../GH_III1_R2.md`, com os três lemas condicionais e os bloqueios explícitos. Nenhuma compilação foi executada nesta rodada.
