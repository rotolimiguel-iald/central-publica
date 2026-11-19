# ERRATA T1_R2 — semifinitude e duas reservas editoriais

## Proveniência

A revisão independente apontou uma falha local na justificativa da semifinitude em `T1_FECHADO.md`. A versão anterior foi preservada, sem edição, em `K05/T1/REV0/T1_FECHADO.md`. A correção foi feita ao lado da errata; a caixa final e as demais conclusões foram mantidas.

## E1 — semifinitude da restrição do traço

**Defeito.** A frase “`e_i x e_i` tem traço finito e aumenta para `x`” usava monotonicidade que compressões por projeções crescentes não possuem em geral.

**Correção.** Em §6.2, a justificativa foi substituída pela prova seguinte. Para `x∈N_+`, ponha

`y_i=x^{1/2}e_i x^{1/2}`.

Então `y_i∈N_+`, `0≤y_i≤x` e

`τ(y_i)=τ(e_i x e_i)≤‖x‖τ(e_i)<∞`.

Se `x≠0`, algum `y_i≠0`, pois `e_i→1` fortemente. Logo todo elemento positivo não nulo de `N` domina um elemento positivo não nulo de traço finito, e `τ|_N` é semifinito. Takesaki 1972 fornece a única expectativa condicional normal `E_τ` com `τ∘E_τ=τ`.

## E2 — escopo da identidade geral do setor fixo

**Reserva editorial.** “Sem H_K̂” podia sugerir que a testemunha fiel estava disponível sem afiliação de `K̂` a `L(ℝ)`.

**Correção.** Em §5.1, a formulação passou a delimitar explicitamente: “sem injetividade essencial, mas mantendo `K̂` afiliado a `L(ℝ)` — ou supondo explicitamente as hipóteses do Lema A —”. A identidade permanece `Fix=W*(√K̂)′∩M̂`; nenhuma conclusão adicional foi introduzida.

## E3 — normalização da densidade fiel

**Reserva editorial.** A integral escrita para a testemunha `d=e^{-ĥ²-ĥ}` omitia o fator `e^{-p}` da medida do traço.

**Correção.** Como `τ(f(ĥ))=c_φ∫f(p)e^{-p}dp`, a formulação correta é

`τ(d)=c_φ∫_ℝe^{-p²-2p}dp<∞`.

## Integridade e escopo

- `REV0/T1_FECHADO.md` SHA-256: `c8c810ba69647498a868c624506fad89b32eb1a9120c43d3bc53e321efa2b604`.
- `T1_FECHADO.md` corrigido SHA-256: `b74d8c421e9137114a7fe231fceb3e4cc41e02d3adf68ccc18c2d901fc2b2f9e`.
- A comparação mostrou somente as três alterações acima; a caixa final permaneceu inalterada.
- `K05/candidatas/T1_R2.lean` e todos os logs anteriores ficaram intactos. Não houve necessidade de recompilação.
- Nada foi registrado, depositado, instalado ou promovido. Pronto para revisão curta.
