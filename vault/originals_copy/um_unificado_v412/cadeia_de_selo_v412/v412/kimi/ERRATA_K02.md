# ERRATA K02 — correções da revisão independente

## Proveniência

A revisão independente apontou FAIL por duas omissões materiais. As versões anteriores foram preservadas em `K02/REV0/`; nenhum original foi apagado ou reescrito em `REV0`. Esta errata fica ao lado da versão corrente. Nada foi registrado, depositado, instalado ou selado.

## E1 — Lema B de T1: `H_E` passa a ser explícita e necessária

**Defeito.** `T1.md` afirmava a existência de expectativa condicional normal `E:M→N` e a convergência predual com invariância modular de `N`, sem incluir claramente a semifinitude de `ρ|_N` nas hipóteses.

**Correção.** Foi acrescentada `H_E`: `N = Fix(α_s)` é invariante por `σ^ρ` **e** `ρ|_N` é semifinito. Takesaki 1972 usa as duas condições; a invariância modular sozinha não basta. A existência de `E` e a convergência predual dependem agora de `H_E`.

- Em estado normal fiel, a semifinitude é automática e `H_E` reduz-se à invariância modular.
- Em peso fiel normal semifinito, sem `H_E`, o caso geral fica **[OPEN]**, não **[DERIVED]**.
- Os passos espectrais em Hilbert permanecem válidos; não são apresentados como prova da existência de `E` sem `H_E`.

Referência: Takesaki 1972, *Journal of Functional Analysis* 9, 306–321, DOI `10.1016/0022-1236(72)90004-3`. [KNOWN, a conferir, enunciado consultado](kimi-cite://web?url=https%3A%2F%2Fwww.fields.utoronto.ca%2Ftalk-media%2F1%2F42%2F06%2Fslides.pdf "citation")

## E2 — τ★: inclusão da rota autoconsistente omitida

**Defeito.** O inventário não incluía `self_consistent_readout_fixes_the_frequency`, embora o mesmo `TonicaDoHamiltoniano.lean` já consultado a contivesse.

**Correção.** Foram conferidas as linhas 166–173: se `ħ≠0`, `τ★≠0`, `ω≠0` e `ħω=ħ·½τ★ω²`, então `ω=2/τ★`. A prova cancela `ħ`, fatora `ω` e usa `ω≠0` para descartar a raiz nula. [TonicaDoHamiltoniano, linhas 166–173](kimi-cite://md-line?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2FN%C3%B3s%2Ftgl_kernel%2FTGLExt%2FTonicaDoHamiltoniano.lean&line=166 "citation")

O comentário nas linhas 33–35 liga `τ★=t_P` a `2E_P` e o tempo de horizonte a `E_P/√(2π)`. [TonicaDoHamiltoniano, linhas 33–35](kimi-cite://md-line?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2FN%C3%B3s%2Ftgl_kernel%2FTGLExt%2FTonicaDoHamiltoniano.lean&line=33 "citation")

**[DERIVED sob as não-nulidades]** A rota fixa a **FREQUÊNCIA** em função de `τ★`; não fixa `τ★` nem a unidade, não muda o no-go de `E₀` e não altera os números de `Γ`. A candidata `K02.Tau.self_consistent_readout_fixes_frequency` foi acrescentada e compilada com as mesmas hipóteses explícitas.

## Reservas objetivas corrigidas

1. **Borel versus pontos fixos.** `W*(√K̂)=W*(K̂)` foi separada por positividade/projeções espectrais; `Fix_{M̂}(Φ_t)=A` continua dependente de `H_masa`.
2. **Notação da cunha.** A ergodicidade usa `Fix_A(σ^Ω)=ℂ1`, distinguindo-a de `Fix_{M̂}(Φ_t)`.
3. **Escopo do manifesto.** `MANIFESTO_K02.json` inclui somente artefatos K02, exclui K01/K03 e também `K02/REV0`.
4. **Metadados reais.** Todos os logs contêm `COMMAND`, `Lean (version 4.31.0)` e `RC: 0`. O script usado é `K02/sandbox/compilar.sh`; nenhum `lake`/`build` foi executado no kernel canônico.
5. **Padronização.** Referências novas e revistas usam `[KNOWN, a conferir]`; Connes–Moscovici é citado diretamente como *Type III and spectral triples*, 2008, arXiv:math/0609703. [Connes–Moscovici 2008](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2Fmath%2F0609703 "citation")

## Verificação final

- Quatro candidatas compiladas no sandbox: `rc=0` em todas.
- Zero `sorry`/`sorryAx`; axiomas somente `propext`, `Classical.choice`, `Quot.sound`.
- `REGISTRO_MAPA_K02.json` atualizado, sem registro.
- Resumo de `ENTREGA_K02.md` mantido em 12 linhas numeradas (15 linhas totais no bloco superior).
- Uma única pergunta residual preservada em `PERGUNTA_K02.md`.
