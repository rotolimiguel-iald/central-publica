# ORDEM K07 — matemática, rodada 3: as ressalvas da conferência distinta da K05 e três construções

De: a gerência c1. Para: o Kimi. 14/11/2026 08:03. Continua a K05. Nada da K05 se apaga: correção AO LADO, versão anterior preservada, como você já fez.

## 0. O que aconteceu com a K05

Quatro revisores distintos conferiram a K05, cada um com script próprio e, onde havia Lean, recompilando em cópia própria. As quatro frentes saíram **aprovadas com ressalvas**. Leia os quatro relatórios INTEIROS antes de tocar em qualquer documento. Cada ressalva está neles com arquivo:linha e a consulta; esta ordem não os repete.

- `C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\revisao\REVISAO_K05_T1.md` (sha16 `28afc655196093b1`)
- `C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\revisao\REVISAO_K05_MONTAGEM_GH.md` (sha16 `6c63ac7f6ceb2cf6`)
- `C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\revisao\REVISAO_K05_TAU.md` (sha16 `6ed7b49cd1322165`)
- `C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\revisao\REVISAO_K05_CAMPO.md` (sha16 `79087c94d3930355`)

Conferido e certo (não refazer): os 20 pinos da sua validação; todos os números da frente τ★; as duas candidatas Lean (rc 0, só o trio, zero `sorry`); na T1, os Lemas C e A, a paridade, a passagem L² → L¹ → σ-fraca e a prova da cunha; na montagem, `D`, `J`, `χ`, a KO-dimensão 4 e o rótulo ímpar×ímpar; em GH, as citações de Rieffel, van Suijlekom, Kaad–Kyed e Haagerup–Musat; no campo, o 1/12 e as duas massas.

## 1. Erros materiais (primeiro)

1. **T1, o peso** [T1 R1]. `c_φ = φ(1)`: a restrição do traço canônico a `L(ℝ)` é semifinita se e somente se `φ(1) < ∞`. A caixa vale para **estado normal fiel**; com `φ(1) = ∞` não existe `E_τ`. Corrija l.22, l.166–168 e a caixa. As suas erratas E1 e E3 repousam nisso.
2. **Montagem, a orientação** [MONTAGEM_GH §5, item 1]. A constante do ciclo é `−1/24`, não `−1/18`: a soma de shuffles dá `24·Γ₁Γ₂Γ₃Γ₄`.
3. **τ★, a atribuição: erro MEU, não seu** [TAU R5]. Na ORDEM K05, seção D, item 5, eu escrevi que o operador “já disse” que no laboratório vale Planck e que, onde o sistema tem horizonte próprio, entra o tempo do horizonte. Isso é leitura MEDIDA PELA GERÊNCIA em 27/10 (a descrição da memória `C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\cinco-sigma-fora-da-cosmologia-27out.md` o diz), não fala dele. Dele é: o tempo é um só fluxo, lido duas vezes, e a segunda leitura é a fase de retorno, onde entra c³ (05/10); e a segunda leitura é «o pedágio de planck lido na propagação» (28/10). No mesmo 28/10 a rota do ramo B (o período do horizonte na fonte) ficou superada pela leitura dele mais a calibração; ver `C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\ramo-b-reaberto-05out.md`. Consequência para o seu §6: a exigência “uma definição para dois regimes” nasceu de leitura da gerência. Refaça o §6 dizendo isso e responda: retirada essa premissa, a `PAREDE_RELOGIO_E_PONTE_HUBBLE` continua parede, ou o que resta é só “âncora G medida mais um número puro não fixado”, com o O(1) da cosmologia vindo da lei do fluxo e não de τ★?
4. **τ★, o fator 2** [TAU R2]. Para o remanescente de 60 massas solares, a sua candidata R1 dá `4πGM/c³`; o ramo B pré-registrado dava `8πGM/c³` em χ = 0. Ponha as duas linhas na tabela, com o estado do ramo B dito (item 3).
5. **Campo, a aferição** [CAMPO R1, R2]. O kernel e o acervo têm peças que o levantamento não trouxe. Ver a seção 4.

## 2. T1: o resto e duas construções

a. Aplique T1 R2 a R7: a definição de “essencialmente injetiva”, com Lusin–Souslin, como condição necessária e suficiente; a prova de `ker A_e = L²(eNe)`; a ordem dos quantificadores no §5.2; Choi fora da lista do que entra por citação; Segal/Dixmier no lugar do rótulo “Realização Lp”; a caixa em três blocos (Teorema, Proposição da cunha, Resíduo).

b. **O resíduo não é hipótese nova.** O revisor aferiu que o que você chamou `H_TGL-horizon` é a lacuna que o artigo já nomeia (“BW não-perturbativo para horizontes não-Killing”, l.1566 e 2238; T1, l.1571) e que o kernel declara aberta (`BisognanoWichmann.lean`, `PonteDaEscalaDual.lean`). Escreva-a com o nome do artigo.

c. **CONSTRUÇÃO 1: `H_K̂` é o Axioma E transcrito?** O revisor derivou (relatório da T1, §7, iii): em `M̂`, `σ^{φ̃}_t = Ad λ(t)`; logo o centralizador do peso dual é `λ(ℝ)′ ∩ M̂ = M_φ ⊗̄ L(ℝ)`, e sob `H_erg` é `L(ℝ)`. Então “`K̂` mora no centralizador” é a afiliação, e a igualdade do Axioma E, `𝒞 = W*(K_∂)`, é a injetividade essencial (pelo R2, condição necessária e suficiente para `W*(K̂) = L(ℝ)`). Leia o texto exato do Axioma E em `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\A Ponte Einstein Cartan Miguel.tex` (l.1084–1112 e 2013–2018) e decida, com prova escrita: `H_K̂` é exatamente o Axioma E em `M̂` sob `H_erg`, ou onde difere. Se for, a T1 fica “Axioma E, `H_erg` e estado ⟹ a caixa”, e `H_K̂` sai da lista de hipóteses novas. O candidato `K̂ = c·e^{ĥ}` e as duas leituras de “covariante” ficam ditos, sem escolher.

d. **CONSTRUÇÃO 2: `H_erg` como termo. O argumento de Mautner num Hilbert abstrato.** Hoje `H_erg` é AUSENTE no kernel e na bancada (consultas no relatório, §7, ii). Escreva a candidata Lean, sem hipótese oca, em sandbox, sem `lake`:
   - Dados: `δ, T₊, T₋ : ℝ → (H →L[ℂ] H)` que preservam o produto interno; `δ s ∘ T₊ a = T₊ (exp s · a) ∘ δ s` e `δ s ∘ T₋ a = T₋ (exp (−s) · a) ∘ δ s`; `T± 0 = 1`; `a ↦ T± a v` contínua em 0.
   - Teorema 1: `(∀ s, δ s ξ = ξ) → ∀ a, T₊ a ξ = ξ ∧ T₋ a ξ = ξ`. Prova: `f(a) = ⟪ξ, T a ξ⟫` satisfaz `f(a) = f(e^{∓n}·a)`, que tende a `f(0) = ‖ξ‖²`; a igualdade em Cauchy–Schwarz fecha.
   - Teorema 2: para uma subálgebra `M` com `Ω` separador, `δ s Ω = Ω`, e a hipótese NOMEADA de vácuo único (“todo vetor fixo por `T₊` e por `T₋` é múltiplo de `Ω`”): se `x ∈ M` comuta com todo `δ s`, então `x` é escalar.
   - Fiação (só levantamento, com a classe e a consulta: EXISTE E LIGADO / EXISTE E NÃO LIGADO / MEDIDA / AUSENTE): que objetos do kernel dão `δ`, `T±`, `Ω` e a relação de comutação NA LUZ. Onde olhar: `TGLExt\O16` (`DilationGeometry_v2`, `DilationModularRecognition_v2`, os `LightRay*`) e `TGLExt\F1Fecho394` (`CanonicalWedge*`, `WedgeCyclicR3`, `PhysicalWedgeNullGeometryR3`, os `CanonicalFockWeightInvariance*`).
   - Diga o que essa pedra compra e o que não compra: `H_erg` vira teorema dado o par boost–translação na luz e o vácuo único; ela não toca o resíduo do item b.

e. A candidata `T1_R2.lean` não será instalada: o revisor mediu redundância com `Ergodicity.lean` e `AperiodicPhaseAverage.lean`. Se for barato, dê-lhe músculo: prove que o multiplicador É a média gaussiana, com `gaussianWeight_fourier` de `F1Fecho394\GaussianProbabilityKernelR4.lean`. Se não for, arquive com nota e corrija as três docstrings que prometem mais do que o enunciado.

## 3. Montagem e GH

a. Aplique os seis itens do §5 do relatório: a constante; os dois itens que faltam na lista de axiomas e a citação de Connes 2008; onde se sustentam finitude e Poincaré em T⁴; dizer que os Lemas 1 e 2 não dependem do tipo; “deve usar” por “pode usar”; a linha de Blackadar na errata.

b. **O que a ordem pediu e veio pela metade.** Nenhum truncamento concreto da casa em `M̂` foi tratado. Trate um: os cantos espectrais `e_i = 1_{[−i,i]}(ĥ)`, os mesmos do Lema B da T1. Diga, hipótese por hipótese do seu Lema 2, o que vale, o que falha e o que falta definir (em especial: qual é o operador da tripla em `M̂` e qual é a sua Lip-norma). Se nada concreto fecha, diga isso. A conjectura continua conjectura.

## 4. Campo: as peças que faltaram e a rota de “provar ou podar”

A fala, por bytes: «eu acho que é dual (porque é conjugado), eu traduziria como campo de processamento dual estabilizado radicalmente por vetor cinético (que é o loop recursivo)». A memória da casa manda não ler “dual” como “complexo” por conta própria (`C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\campo-dual-vetor-cinetico-13nov.md`), e a sua candidata A herdou essa leitura da minha ordem. Acrescente, sem escolher:

- **F: a luz de Wigner, que o kernel tem desde a v375.** `TGLExt\LightHelicityWigner.lean`: a fase do fóton como caractere U(1) do pequeno grupo, a lei de composição (o cociclo), e a conjugação que leva a helicidade `h` a `−h` e troca as duas seções circulares (`light_helicities_exchanged_by_conjugation`). O cabeçalho da pedra anota que “a distinção fóton/escalar sem massa duplicado segue FORA do tipo”. Ao lado, em `TGLExt\F1Fecho394`: `ScreenGeometricReflectionR4` e `CanonicalWedge` (a conjugação antilinear), `CircularConjugationR1`, `MaxwellOnShellBivectorR2` (F = p∧e, gauge, Bianchi), `MaxwellScreenDualTensorR2`, `LorentzTimeStabilizerR4`.
- **G: a Lagrangiana radicalizada do autor (2025).** `C:\IALD\papers_latex\luz\luz.tex`, l.66–112: `𝓛 = √|g⁻¹(F ∧ ⋆F)|`, com a não linearidade que satura em campo intenso. No Atlas, os verbetes “Lagrangiana radicalizada (2025)” e “Luz = razão = radicalizar = encontrar”.
- **H: o par.** `TGLExt\Par.lean` e o verbete “Gráviton” do Atlas (dois psíons conjugados, `A_C` e `J A_C J`).
- **I: o dual de Hodge.** O mesmo `luz.tex`, l.142–175, e `MaxwellScreenDualTensorR2`.

Entregue UMA tabela: cada palavra da fala (campo; de processamento; dual; conjugado; estabilizado; radicalmente; vetor cinético; loop recursivo) contra cada candidata (A a I), com o objeto tipado (arquivo:linha e nome do teorema) e a classe. Em F, afira no kernel, sem supor: o pequeno grupo está definido como o grupo que fixa um vetor nulo? Onde? Depois, para cada candidata: a ROTA (que enunciado Lean a provaria, com que estrutura) e o CRITÉRIO DE PODA (que resultado a derruba). O revisor propôs um critério mínimo (relatório do campo, §7); parta dele. Aplique também CAMPO R3 a R13.

Quem lê a fala é o operador. Você tipa as leituras possíveis; não escolhe.

## 5. τ★: o resto

Aplique TAU R1 (o Mapa por termo único; cite as rotas que o revisor listou), R3, R4 e R6 a R9. E feche a premissa de β lendo a fonte: `paper_PT.tex`, l.809–838, que o revisor não abriu. A ausência de β na leitura autoconsistente é intencional pelo que está escrito? Responda com arquivo e linha. Ao operador vai só a ratificação.

## 6. Integração e entrega

- `REGISTRO_MAPA`: tire do campo `nota` a palavra da creditação. `VALIDACAO`: “conferidas por revisores distintos” é expressão da gerência; diga “revisada internamente”. `ENTREGA`, l.11: o prefixo de uma ausência é `[OPEN]`.
- Entregue `ENTREGA_K07.md` (resumo em até 15 linhas, com estatuto por linha); os documentos `_R3` ao lado dos `_R2`, com as versões preservadas e uma errata por frente; as candidatas Lean com log; `REGISTRO_MAPA_K07.json` (proposta, sem registrar); e o depósito pela fila, com `[DECLARADO]`. `PERGUNTA_K07.md` só se sobrar resíduo que o acervo não responde.
- Ordem de trabalho sugerida: a seção 1; depois 2d e 4, que são as construções; depois o resto.

## 7. O que não se toca

O kernel canônico, o `um.py`, o Artigo A, o Atlas, o Mapa (só consulta, por termo único), a memória (só depósito). Nenhum dado observado se abre. Nenhuma candidata se instala. Nenhuma leitura do operador é escolhida por nós. Leitura de teste selado não é teste novo. O gate não se move.

— gerência c1, 14/11/2026 08:03.
