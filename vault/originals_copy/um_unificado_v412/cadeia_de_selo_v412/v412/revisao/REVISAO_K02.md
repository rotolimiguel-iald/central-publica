# REVISÃO DISTINTA DA ENTREGA K02 (v412) — T1, montagem 3+1, GH-III₁, τ★

Revisor distinto (quem constrói não aprova). 13/11/2026. Só leitura fora desta pasta; nada registrado no Mapa, nada depositado na fila, nada instalado.
Estatutos: [REAL] conferido por mim com a consulta citada · [KNOWN] literatura conferida na fonte, com identificador · [DERIVED] derivado por mim aqui (não formalizado) · [DECLARADO] do Kimi, não conferido · [OPEN].

## 0. Veredito

**APROVADA COM RESSALVAS**, como levantamento e desenho; **não** como teoremas. A matemática descritiva do Kimi é, no geral, correta e honesta com os estatutos (nada promovido a teorema). Quatro ressalvas materiais:

1. **T1.** O `T1.md` deixa `H_masa` sem prova e diz que «centralizador trivial não substitui `H_masa`». O que falta é a estrutura que fecha a conta: o comutante relativo de `λ(ℝ)` no produto cruzado é `L(ℝ) ⊗̄ M_φ`. Com ela, (c) ⟹ (b) vale sob uma hipótese que o artigo não nomeia (`H_K̂`, §4.4). O argumento da gerência está certo nessa forma.
2. **Candidatas Lean.** Compilam, estão limpas, mas duas (T1, GH_III1) não provam nada sobre o objeto do item; as outras duas são aritmética/álgebra de contabilidade (§3).
3. **Montagem 3+1.** Um erro de rótulo (T³×S¹ é ímpar×ímpar, não par×ímpar); e a referência para (1,3) merece ser trocada de «(H) do artigo» para «(H) com moldura publicada só para a definição e os sinais» (§5).
4. **τ★.** Os números conferem. A premissa da «rota autoconsistente» do kernel não leva o β da lei canônica; isso precisa ser dito (§7).

## 1. Consulta ao Mapa de Rotas (antes de tudo)

`rotas.py consultar "T1 ergodicidade produto cruzado"` → 0 rotas (cabeça `cd061fe918383c61`, 2051 registros). `consultar "tau estrela"` → 2 rotas: `cadeia.preparacao_v412` (EM_CURSO; «nenhuma rota para T1, produtos de triplas ou Rieffel») e `massa.gap_angulo_de_miguel_01nov` (ERRATA_GAP_E_U_NAO_DELTA). Nada refeito, nada registrado. [REAL]

## 2. Cobertura: ordem × entrega

| item | enunciado com arquivo:linha | aferição citada | mathlib | rota de prova c/ estatuto | candidata Lean |
|---|---|---|---|---|---|
| T1 | sim (.tex 1886–1919) | sim (Mapa, inventário, kernel, Atlas, buscar.py) | sim (nomes conferidos por mim, §3) | sim, mas **sem** o lema do comutante relativo de λ(ℝ) e **sem** a simplificação pelo traço | existe, **fora do alvo** |
| 3+1 | sim (1922–1932; 523–543, conferidas por mim) | sim | sim (ZMod 8, GH clássica) | sim (fórmulas par/ímpar, 7 axiomas) | existe, só aritmética |
| GH III₁ | sim (1821–1826; 1934–1942; 2250–2254) | sim | sim (`GromovHausdorff`) | rota em 5 passos, **sem** examinar se o produto cruzado II_∞ contorna «sem traço» | existe, **tipagem oca** |
| τ★ | sim (725–731; 818–830; 1903–1919; 2234–2237) | sim (11 leituras) | trivial | sim | álgebra |

Pedido e **não veio, ou veio incompleto**:
- T1: «o que cabe como teorema de kernel (face finita)». Só vieram `lock_gap` e um decaimento escalar. Não veio o teorema da face finita que é do alvo: em `M_n(ℂ)`, `Fix(Φ_t) = {K}′` e `Φ_t → E` (pinching).
- T1: «de que teorema conhecido a ergodicidade vem para a cunha». Veio só a citação de Speranza (secundária, sem prova); faltou o argumento (§4.5).
- GH: o contraexemplo é só critério; não construído. Hekkelman (arXiv:2111.13865), o teorema do círculo de Toeplitz, não foi citado.
- 3+1: não há a identificação explícita «produto de quatro círculos = tripla canônica de T⁴»; ela fecharia finitude e Poincaré no caso (4,0) (§5).
- Todo o resto pedido veio (resumo ≤15 linhas, `PERGUNTA_K02.md` única, `REGISTRO_MAPA_K02.json` com as chaves do `rotas.py modelo`, manifesto com hashes que conferem: sha16 das 4 candidatas `fbda05be…`, `caac5d27…`, `8b56968a…`, `6b533a53…`).

## 3. As quatro candidatas Lean

**Compilação [REAL].** Recompilei as quatro fontes de `K02\candidatas\` com o binário `lean.exe` 4.31.0 direto, como o Kimi, em cópia minha (`revisao\scripts_k02\src` e `build`; script `recompilar_revisor.sh`). Li só os `.olean` das dependências do kernel; não rodei `lake` nem escrevi lá. Resultado: `rc=0` nas quatro; os `#print axioms` saem iguais aos logs do Kimi (só `propext`, `Classical.choice`, `Quot.sound`; `signs_KO4` e `ko_sum_mod_eight` só `propext`, `Quot.sound`); zero `sorry` (grep nas fontes e nos logs, rc=1 = nenhuma ocorrência); só avisos de estilo. Fontes de `candidatas` e `sandbox/sources` idênticas (`cmp`).

**O que cada uma prova de verdade, em palavras simples:**

- `T1.lean`. `lock_gap`: num Hilbert qualquer, o operador `1 − (projeção na reta de Ω)` leva Ω em 0 e deixa fixo todo vetor ortogonal a Ω (é o que o kernel já tem como `o_lock_tem_gap_um`, `PontoZeroDoPsion.lean`, l.269; redundante, e o nome «gap» promete mais do que o enunciado: só os valores em Ω e Ω^⊥, não o espectro). `tendsto_modalDecay`: a função escalar `exp(−βδ²t/2)` tende a 1 se δ=0 e a 0 se δ≠0 quando t→∞ (a sombra escalar do cálculo espectral). **Nada** sobre `Fix`, `Φ_t`, produto cruzado, esperança condicional ou traço. O próprio Kimi diz isso. **Fora do alvo; não vazia, mas quase tudo é trivial.**
- `MONTAGEM_3MAIS1.lean`. Aritmética de `ZMod 8` e de paridade: soma de KO-dimensões tem a paridade do produto graduado (64 casos por `decide`); as tabelas `epsilon`, `epsilonPrime`, `epsilonDoublePrime` são **definições** `if…then…` e `signs_KO4`/`signs_KO2` só conferem que o que foi digitado é o que foi digitado (tautologia por `decide`). `product_*` são `rfl` da definição de `productParity`. A única afirmação com conteúdo é `parity_koAdd` (ℤ/8→ℤ/2 é homomorfismo). **Nada sobre triplas espectrais.** O Kimi declara isso. A correção dos sinais não vem do Lean: conferi-a eu mesmo (§5).
- `GH_III1.lean`. `classical_gh_self`: `ghDist X X = 0` (um `simp`; irrelevante ao item). `QuantumMetricSpace`: estrutura em que `State` (com métrica) **não está ligado** a `Elem` (nem avaliação, nem relação com `lip`), logo nem é espaço métrico quântico. `TypeIII1GHConjecture`: um `def` Prop com `IsTypeIII1`, `IsSpectralTruncationOf`, `qghDist` como parâmetros livres: é um **esquema**, falso para instanciações triviais (qghDist ≡ 1, predicados `True`); não fala de III₁. `typeIII1_of_named_hypothesis` é `H_GH_III1 H_limit H_truncations` (modus ponens: a conclusão é a hipótese aplicada). **Tipagem honesta (nada promovido), mas oca; não serve de pedra; no máximo documentação.**
- `TAU_ESTRELA.lean`. `Gamma β τ ω := ½βτω²`; `gamma_rescales` (linear em τ); `self_consistent_readout_fixes_frequency` (cópia do teorema do kernel, `TonicaDoHamiltoniano.lean` l.166–173, conferido); `gamma_of_gap_time`: Γ(ħ/u, u/ħ)=βu/(2ħ); `gamma_of_retained_time`: Γ(ħ/(βu), u/ħ)=u/(2ħ) (β cancela). **Álgebra exata, correta; não deriva escala nenhuma**, como o Kimi diz.

Conclusão: nenhuma das quatro é «vazia» no sentido de falsa ou de esconder hipótese; **GH_III1 é oca como enunciado**; **T1 e MONTAGEM não tocam o objeto do item.** Nenhuma deve ser instalada como pedra de kernel sem substituir o conteúdo (§8).

## 4. T1 — o ponto matemático

### 4.1 O que o `.tex` diz e o que NÃO diz sobre K̂ [REAL, lido]
Linhas 1086–1130, 1888–1919, 1960: `K` aparece em `e^{is√K}` com taxas `½β(√k_i−√k_j)²`; logo `K ≥ 0` e `√K̂` exige **K̂ operador positivo** (não gerador com espectro em ℝ). `K` mora no **centralizador** (Axioma E: `C = W*(K_∂)`, «vive no centralizador», l.1105). O artigo **nunca define K̂**. Ele diz que `√K̂` não é covariante sob a ação dual («ancoragem de escala», l.1914–1917). Isto só é compatível com K̂ **não** em `π(M)` (a ação dual fixa `π(M)`): K̂ envolve o gerador de λ.

### 4.2 Passo (i): produto cruzado como pontos fixos [KNOWN]
É o teorema de **Digernes–Takesaki** (não «Digernes/Haagerup»; Haagerup desenvolveu os pesos duais): `M ⋊_α G = (M ⊗̄ B(L²(G)))^{α⊗Adρ}`. Fonte conferida: Andreou, arXiv:2004.07169, p.14, que cita Takesaki, *Theory of Operator Algebras II*, Cap. X, Cor. 1.22 (Springer 2003); Digernes, *C. R. Acad. Sci. Paris Sér. A* 278 (1974) 937–940 (referência lida em Hiai, arXiv:2004.02383). Convenção: `π(x)(s)=σ_{−s}(x)`, `λ(t)ξ(s)=ξ(s−t)`, `ρ` regular direita; a convenção oposta só troca t por −t e não altera os enunciados abaixo.

### 4.3 Passos (ii)–(iv): o Lema C (comutante relativo de λ) [DERIVED, sobre (i); sanidade finita REAL]
**Lema C.** `λ(ℝ)′ ∩ M̂ = L(ℝ) ⊗̄ M_φ = (π(M_φ) ∪ λ(ℝ))″`, com `L(ℝ)=λ(ℝ)″`, `M_φ=M^{σ^φ}` (centralizador; para peso, `σ^φ`-fixos).
Prova: (1) teorema da comutação: `(λ(ℝ)⊗1)′ ∩ (B(L²)⊗̄M) = λ(ℝ)′ ⊗̄ M = L(ℝ) ⊗̄ M`, pois ℝ é abeliano e `λ(ℝ)′ = λ(ℝ)″` (maximal abeliana em `B(L²ℝ)`); (2) `ρ_t ∈ L(ℝ)`, que é abeliana, logo `Ad ρ_t` age trivialmente em `L(ℝ)`, e a condição de ponto fixo de `Adρ⊗σ` vira `(id⊗σ_t)(x)=x`; (3) `(L(ℝ)⊗̄M)^{id⊗σ} = L(ℝ)⊗̄M^σ` (propriedade de fatia de Tomita). ∎ Os passos (ii), (iii), (iv) da gerência estão **certos** (a notação «x ∈ L(ℝ)⊗̄M_φ» é a álgebra dentro de M̂, pois já é ponto fixo de `Adρ⊗σ`).
**Corolário.** `L(ℝ)` é maximal abeliana em `M̂` **⟺** `M_φ = ℂ1` (fluxo modular ergódico).
**Sanidade finita [REAL].** `revisao\scripts_k02\revisor_comutante_relativo.py` realiza `M ⋊ G` para G finito abeliano como pontos fixos de `Adρ⊗α` em `B(ℓ²(G))⊗M` e mede `dim(λ(G)′∩M̂)` contra `|G|·dim(M^α)`: ℤ₂ por Ad(Z) em M₂ (não ergódico): 4 = 2·2, λ(G)″ **não** é masa; ℤ₂×ℤ₂ por Ad(Weyl) em M₂ (ergódico): 4 = 4·1, **masa**; ℤ₃×ℤ₃ em M₃ (ergódico): 9 = 9·1, **masa**. `dim M̂ = |G|·n²` em todos. Saída em `revisor_comutante_relativo_saida.json`.
Observação: o «contraexemplo estrutural» do próprio Kimi (`B(L²ℝ)⊗N₀`, `K=q⊗1`) **é** este mecanismo com `M_φ = N₀`; o Kimi não o reconheceu como o caso geral.

### 4.4 O argumento (c) ⟹ (b): veredito [DERIVED sobre KNOWN]
**Correto, com UMA hipótese que o artigo não nomeia:**

> **H_K̂.** `K̂ ≥ 0` é afiliado a `L(ℝ) = W*(ĥ)` (ĥ = gerador de `λ(t)=e^{itĥ}`, o «Hamiltoniano modular» da álgebra cruzada) e `K̂ = F(ĥ)` com `F : ℝ → [0,∞)` boreliana **essencialmente injetiva**. Então `W*(√K̂) = W*(K̂) = L(ℝ)`.

Sob H_K̂: `Fix(Φ_t) = {u_s}′∩M̂ = λ(ℝ)′∩M̂ = L(ℝ)⊗̄M_φ` (Lema C) e portanto **`Fix = W*(K̂)` ⟺ `M_φ = ℂ1`** (ergodicidade). Logo (c) ⟹ (b) e vale a recíproca; o passo (v) fornece o que falta para a cunha.
**Onde precisa de hipótese:**
- **a função precisa ser injetiva.** Sem ela o resultado cai: com `K̂ = ĥ²`, `√K̂ = |ĥ|` e `W*(|ĥ|) ⊊ L(ℝ)`; `Fix ⊇ L(ℝ)` e nada garante igualdade a `W*(K̂)`. É a pergunta da gerência «√K̂ injetiva no espectro»: sim, precisa; e está em aberto qual F é a do artigo.
- **K̂ = π(K), com K do centralizador** (a leitura da sombra finita): então `λ(t)` comuta com `K̂` e `Fix ⊇ W*(λ(ℝ), π(K)) ⊋ W*(K̂)`; a identidade `Fix = W*(K̂)` só vale na própria M, não em M̂. Além disso, em III₁ ergódico o centralizador é ℂ, logo K seria escalar: é por isso que o artigo precisa de M̂.
- O peso/estado `φ` é o **mesmo** cujo fluxo modular constrói M̂; (c) é ergodicidade **desse** `σ^φ`. O fator ser III₁ **não** dá `M_φ=ℂ` (III₁ dá fluxo dos pesos trivial; o Kimi está certo aqui, §6 do `T1.md`).
- Convenções de π e λ: só sinal; sem efeito.
- `W*(√K̂)=W*(K̂)` por positividade: certo (o Kimi também).
Ressalva de leitura: com M_φ=ℂ, a álgebra «setor da verdade» `C=L(ℝ)` é difusa e **só existe em M̂**; em M (a cunha) `Fix_A(σ^Ω)=ℂ1`, e é isso, não `W*(K)`, que a ergodicidade da cunha dá. O Kimi tratou (c) como uma saída diferente de (b) e concluiu «isso não prova Fix = W*(K̂)»; em geral certo, mas incompleto: **sob H_K̂ prova**.

### 4.5 O passo (v) — a cunha [KNOWN + DERIVED]
- BW: o grupo modular da álgebra da cunha com o vácuo são os boosts [KNOWN]. O Kimi cita Bisognano–Wichmann, *J. Math. Phys.* 16 (1975) 985, DOI 10.1063/1.522605 (campo escalar hermitiano) e Guido, arXiv:0812.1511 (Contemp. Math. 534, 97–120, 2011; conferido o título e a referência; o «teorema 3.3» **não** conferi). Para campos de Wightman gerais a referência é BW, *J. Math. Phys.* 17 (1976) 303 [a conferir, não conferida].
- Ergodicidade `M_Ω=ℂ1`: **argumento curto que eu construí [DERIVED]**: seja ξ invariante pelo grupo modular (= boosts). Para o vetor nulo a₊ do plano do boost, `Λ(s)a₊ = e^{s}a₊`, logo `f(r)=⟨ξ,U(ra₊)ξ⟩` satisfaz `f(r)=f(e^{−s}r)` e, por continuidade forte, `f(r)=f(0)=‖ξ‖²`, donde `U(ra₊)ξ=ξ`; idem para a₋. Então `P⁰ξ=0` e, pela condição espectral (medida espectral em `V̄₊`, em que `p⁰=0` só em 0), ξ é invariante por todas as translações, logo `ξ ∈ ℂΩ` (unicidade do vácuo). Como xΩ é invariante se x é `σ`-fixo e Ω é separador (Reeh–Schlieder), `x ∈ ℂ1`. Hipóteses: covariância de Poincaré, condição espectral, vácuo único, BW. É de tipo Borchers–Mautner; **não** conferi fonte primária; Speranza, arXiv:2504.07630 §4 diz «there also exist ergodic states with trivial centralizer, such as the Minkowski vacuum for a Rindler wedge» (citação conferida; sem prova lá). Se `M_φ=ℂ`, M é fator, o espectro de Connes é `Γ(σ^φ)=Sp(σ^φ)` e `S(M)∖{0}=Sp(Δ_φ)∖{0}`; com `Sp(Δ)=[0,∞)` (boosts) dá III₁ [KNOWN, Connes 1973, *Ann. Sci. ÉNS* 6, 133–252; a conferir, não conferido por mim]. A transferência «cunha de Minkowski → álgebra de horizonte da TGL» é **hipótese física (H_erg) [OPEN]**, não teorema.

### 4.6 Lema B com o TRAÇO canônico [DERIVED; esboço, não formalizado]
Em `M̂` (II_∞ fator se M é III₁; Connes–Takesaki) com traço `τ` normal, fiel, semifinito:
- **H_inv é automática:** `Ad(u)` preserva τ para todo unitário `u ∈ M̂`; logo cada `α_s = Ad(u_s)` e `Φ_t` preservam τ.
- **H_Lp é desnecessária:** o predual é `L¹(M̂,τ)` (Segal–Dixmier); não se precisa de Haagerup–Terp.
- **H_E, parte modular, é automática:** `σ^τ = id`, toda subálgebra de von Neumann é invariante.
- **H_E, parte da semifinitude, NÃO é automática em geral:** exige `τ|_N` semifinito para `N=Fix`. Contraexemplo: `A₀⊗1 ⊂ R⊗B(ℓ²)`, `A₀` masa de `R` (II₁): τ vale 0 ou ∞ em toda projeção de `A₀⊗1`. Também a ação por translação em `L^∞(ℝ)` com medida de Lebesgue (Fix = ℂ1, `τ(1)=∞`): `Φ_t(x)` pode não convergir σ-fracamente. **Sob H_K̂, é automática:** `N ⊇ L(ℝ)` e `τ|_{L(ℝ)}` é medida de Radon equivalente a Lebesgue (em `W*(ĥ)`, `τ(f(ĥ)) = φ(1)∫ f(x)e^{∓x}dx`, convenção conforme a normalização de τ) [KNOWN, a conferir em Takesaki II, Cap. XII; Connes–Takesaki 1977]: há projeções `e_i ∈ N` de traço finito com `e_i ↑ 1`.
- **Esboço da convergência:** `e_i` comuta com todos os `u_s`, logo `Φ_t` restringe a `e_iM̂e_i` (álgebra finita, traço finito): aí a convergência `L²` do passo espectral de Kimi (`T_t=e^{−βtA²/2}→P_{ker A}`) dá convergência `L¹` e σ-fraca; a passagem de `e_iM̂e_i` a M̂ usa `‖ω − ω(e_i·e_i)‖→0` uniforme em t. A existência de `E` é Takesaki 1972 com `σ^τ=id` (ou Umegaki/Dixmier) quando `τ|_N` é semifinito.
- **A prova de Kimi do Lema A (passo 3, via estado fiel invariante) é correta e basta** (o passo de Choi/Kadison–Schwarz é redundante; inofensivo). Em M̂ com τ infinito faz-se nos cantos `e_iM̂e_i`.
Em resumo: com o traço canônico, `H_E` **fica satisfeita automaticamente sob H_K̂** (e **não** sem uma hipótese de semifinitude em geral). O traço é exatamente o que a passagem a M̂ compra.

### 4.7 Quanto cabe ao kernel
Face finita [REAL ser alvo; não construída pelo Kimi]: em `M_n(ℂ)`, `K ⪰ 0`, `Φ_t = ∫Ad(e^{is√K})dN(0,βt)(s)` age por `x_{ij} ↦ e^{−βt(√k_i−√k_j)²/2} x_{ij}` na base própria; `Fix = {K}′` (blocos de autoespaços), `Φ_t → E` (pinching), `Fix = W*(K)` ⟺ K tem espectro simples (é o toy de `H_masa`). Isto é formalizável hoje com o espectral hermitiano da mathlib; é a candidata correta no lugar de `lock_gap`. O contínuo (Digernes–Takesaki, Choi, Takesaki, ergodicidade da cunha) entra por citação/hipótese.

## 5. Montagem 3+1

**Tabela de sinais [REAL].** Conferi a tabela do Kimi (ε, ε′, ε″ por n mod 8) por cálculo explícito: `revisao\scripts_k02\revisor_sinais_KO.py` constrói matrizes gama euclidianas para n=1…8, procura todos os `J = U K` (carga conjugada) com `J D = ε′ D J`, `J² = ε`, `Jχ = ε″χJ` e lista as triplas realizáveis por n. A tabela do Kimi é realizável em **todos os n** e é a seleção de Connes (n=1 (+,−); 2 (−,+,−); 3 (−,+); 4 (−,+,+); 5 (−,−); 6 (+,+,−); 7 (+,+); 8≡0 (+,+,+)); nos pares há a outra tripla realizável, que é a das «doze possibilidades» de D–D. Saída em `revisor_sinais_KO_saida.json`.

**D–D [KNOWN].** Dąbrowski–Dossena, *Product of real spectral triples*, IJGMMP 8 (2011) 1833–1848, arXiv:1011.4456. Li o texto integral. **Confirmo o Kimi:** a §5 verifica a preservação de dimensão, regularidade, realidade, primeira ordem e orientação; **não** trata finitude/continuidade absoluta nem dualidade de Poincaré. As fórmulas par×par, par×ímpar e ímpar×ímpar (com duplicação e Pauli) conferem com o §4. Nota do §6 de D–D: o caso comutativo compacto de estudo é o **toro plano com estrutura spin trivial**, e KO e dimensão métrica «não precisam coincidir mod 8».

**Erro de rótulo no `MONTAGEM_3MAIS1.md` §6, passo 4.** «T³×S¹: par×ímpar; resultado par»: T³ é de KO-dimensão 3 (**ímpar**) e S¹ é ímpar; é **ímpar×ímpar** (com duplicação, ℂ²), resultado par, KO 4. O resultado (KO 4) e a dimensão do espinor (2·1·2 = 4) estão certos; só o rótulo. [REAL, conferido contra D–D §4.3 e a tabela 6]

**Finitude e Poincaré em (4,0) fecham pelo toro T⁴?** **Sim, por identificação, não pelo teorema de produto:** o produto de quatro triplas canônicas do círculo é (a menos de equivalência unitária) a tripla de Dirac canônica do toro plano T⁴ com estrutura spin trivial [KNOWN: D–D §2.4 (o Dirac de ℝⁿ se decompõe nos produtos, eqs. 9–11) e §6]. A tripla canônica de uma variedade spin compacta satisfaz os sete axiomas de Connes, incluindo finitude e dualidade de Poincaré [KNOWN, a conferir: Connes, *Commun. Math. Phys.* 182 (1996) 155–176, hep-th/9603053 — conferi que lista e usa os axiomas (finitude = Axioma 5, Poincaré = Axioma 6) mas **não** o verifica explicitamente para a tripla canônica; Gracia-Bondía–Várilly–Figueroa 2001 (a referência de D–D [8]) e Connes, arXiv:0810.2088 (caracterização; só o resumo foi lido por mim) são as pontas]. Para T⁴ a finitude é trivial: `H^∞ = C^∞(T⁴)⊗ℂ⁴` é livre [DERIVED]. Resta, para declarar o (4,0) **fechado**, escrever a identificação explícita (Dirac e J com as escolhas de D–D) e conferir que orientação e J coincidem.

**Assinatura (1,3): muda o estatuto?** Só em parte [KNOWN, conferido nas fontes]:
- **van den Dungen**, *Krein spectral triples and the fermionic action*, arXiv:1505.01939, *Math. Phys. Anal. Geom.* 19 (2016), DOI 10.1007/s11040-016-9207-z. Def. 2.2 (triplas de Krein pares) é **analítica** (densidade, Krein-autoadjunto, comutadores limitados, `(a)ι` compacto); os produtos que ele constrói são **só** «espaço finito F × variedade pseudo-Riemanniana spin M» (Def. 4.2, Prop. 4.3). Diz que a definição «may not be definitive» e, na **Obs. 6.4**, que não há K-homologia de Krein e que os sinais do real dependeriam da assinatura. Não há finitude, orientação, Poincaré nem primeira ordem lorentzianos.
- **Bizi–Brouder–Besnard**, arXiv:1611.07062 (v2 «Space and time dimensions of algebras with applications to Lorentzian noncommutative geometry and quantum electrodynamics»; referência de periódico [a conferir]): atribui a cada álgebra um par (m,n) mod 8 (dimensões de espaço e tempo) **aditivo no produto tensorial graduado**; a Tabela 3 dá (t,s)=(1,3) ↔ n=6, m=4 (coerente com a observação do Kimi `−2≡6`). O produto de triplas de Krein é definido para o caso **par**; o texto diz que a extensão ao caso **ímpar** «seems difficult». O círculo é ímpar: uma montagem lorentziana por círculos teria de agrupar em fatores pares (por exemplo (1,1)⊗(0,2)).
- **Conclusão:** «(H) do artigo» passa a «(H) com moldura publicada **só** para a definição analítica (van den Dungen) e para sinais/dimensões mod 8 (BBB)». O teorema «o produto de triplas de Krein satisfaz os axiomas lorentzianos, com orientação e dualidade de Poincaré» **não está** nessas fontes: **segue (H)/[OPEN], não «sabido por referência»**. Nota: o `ax:lorentz` do próprio artigo (l.523–530) lista regularidade, dimensão espectral 4, orientabilidade, realidade, causalidade via Π_irr, e **não** lista finitude, Poincaré nem primeira ordem; a lista de sete axiomas do Kimi é a euclidiana de Connes.

## 6. GH-III₁

**Identificadores [KNOWN, conferidos em arxiv.org/abs exceto onde dito]:**
- Rieffel, *Gromov–Hausdorff distance for quantum metric spaces*, Mem. AMS 168 (2004), nº 796, 1–65, arXiv:math/0011063. Resumo conferido: exemplo principal, toros quânticos (o Kimi está certo).
- Connes–van Suijlekom, *Spectral truncations in noncommutative geometry and operator systems*, arXiv:2004.14115, CMP, DOI 10.1007/s00220-020-03825-x. Volume e páginas que o Kimi dá («383, 2021–2067») **não** conferi.
- van Suijlekom, *Gromov–Hausdorff convergence of state spaces for spectral truncations*, arXiv:2005.08544, J. Geom. Phys. 162 (2021) 104075. ✓
- Leimbach–van Suijlekom, *Gromov–Hausdorff convergence of spectral truncations for tori*, arXiv:2302.07877, Adv. Math. 439 (2024) 109496. ✓
- Hekkelman, *Truncated geometry on the circle*, arXiv:2111.13865, Lett. Math. Phys. 112 (2022) art. 20, DOI 10.1007/s11005-022-01514-5 (via busca; resumo de terceiros). **Omitido pelo Kimi**; é o caso-base do círculo de Toeplitz, exatamente a lição de «truncar o operador» do artigo (l.1944–1949).
- Kaad–Kyed, *A comparison of two quantum distances*, arXiv:2212.10874, DOI 10.1007/s11040-023-09451-y. ✓ Resultado: a distância GH quântica de Rieffel **não é equivalente** à GH clássica dos espaços de estados com a métrica de Connes. **Ressalva:** os contraexemplos são sobre **sistemas de operadores comutativos** (bolas ℓ^p), em ordem-unidade; o artigo não decide se coincidem para `C(X)` com `X` métrico clássico. O Kimi usa Kaad–Kyed para recusar «qGH = GH»; a recusa **da identidade universal** é legítima, mas o `.tex` diz «no caso comutativo, qGH = GH (Rieffel)»; **não está refutado** pela fonte, e a identidade clássica de Rieffel para espaços métricos compactos não foi conferida por mim [OPEN, a conferir].
- Connes–Moscovici, *Type III and spectral triples*, arXiv:math/0609703 ✓ (título/autores); referência do volume [a conferir]. Em III₁ as triplas são **torcidas** (peso); o `GH_III1.md` não diz isso.

**A conjectura está tipada sem promover nada a teorema?** No Markdown, sim (CONJECTURE, GH-R vs GH-S, hipóteses listadas, critério de contraexemplo). No Lean, o `def` é um esquema sem conteúdo (§3) e o «teorema» é modus ponens: **nada promovido, nada provado.**
Lacuna de conteúdo: «sem traço em III₁» é obstrução em M, **não em M̂** (II_∞, com traço, §4.6); o `GH_III1.md` não examina se a rota via produto cruzado contorna a obstrução (ou quais novos problemas ela traz: M̂ unital mas com traço infinito, topologia fraca-* no espaço de estados).

## 7. τ★

**Números [REAL, refeitos por `revisao\scripts_k02\revisor_tau.py`, independente do script do Kimi; β = `ALPHA_FINE_CODATA_2018·√e` em runtime = 0,012031300400803142; ħ=h/2π; 1 eV = 1,602176634×10⁻¹⁹ J; ω = E/ħ = 1,519267447878626×10¹⁵ rad/s].**

| leitura | τ (s) | Γ = ½βτω² (s⁻¹) | confere com o Kimi |
|---|---|---|---|
| t_P (CODATA, 5,391247×10⁻⁴⁴) | 5,391247×10⁻⁴⁴ | 7,485835333×10⁻¹⁶ | ✓ (7,4858353332×10⁻¹⁶) |
| ħ/(1 eV) | 6,582119570×10⁻¹⁶ | 9,139381527×10¹² (=βω/2) | ✓ |
| ħ/(β·1 eV) | 5,470829711×10⁻¹⁴ | 7,596337239×10¹⁴ (=ω/2) | ✓ |

Identidades exatas (40 dígitos, `Decimal`): `Γ(ħ/(βu))=ω/2` e `Γ(ħ/u)=βω/2`. Razão `τ_ret/t_P = 1,01476×10³⁰`. `t_P` recalculado de G, c, ħ (CODATA 2018): 5,391246×10⁻⁴⁴ (dif. relativa 10⁻⁷, arredondamento de G). **A conta de cabeça da gerência está certa**: num relógio óptico genérico (ω≈2,7×10¹⁵ rad/s; sem dado de relógio nenhum) dá Γ≈2,4×10⁻¹⁵ s⁻¹ com t_P e ≈2,4×10¹⁵ s⁻¹ com ħ/(β·1 eV). Nenhuma estatística observada foi calculada (nem por mim).

**«A rota autoconsistente fixa ω = 2/τ★, não τ★»** [REAL]: é fiel ao teorema do kernel (`TonicaDoHamiltoniano.lean` l.166–173, lido; hipóteses ħ,τ,ω≠0; a candidata do Kimi o repete). **Mas a premissa `ħω = ħ·½τω²` não leva o β da lei canônica `Γ_ω = ½βτω²`.** Se a «leitura do modo» for `Γ_ω = ω` com a lei canônica, a frequência é `ω = 2/(βτ★)`, fator `1/β ≈ 83,1` acima (script). E há **três** frequências «naturais» no kernel para o mesmo τ★: `√2/τ★` (`gammaB_is_the_canonical_law_at_the_systems_frequency`, l.145), `2/τ★` (a rota autoconsistente) e `2/(βτ★)` (Γ=ω com a lei canônica). Nada disto invalida o Lean (o teorema é exato para a hipótese dada); mas o enunciado «ω = 2E_P/ħ com τ★=t_P» depende da premissa sem β. **Pergunta para a gerência/autores do módulo: a premissa é intencional?** [OPEN]

Sobre a leitura do Kimi de que os dois ramos com ħ/u são «incompatíveis com a premissa de espectroscopia óptica coerente»: correto como ordem de grandeza (coerência de ≈1,3 fs e ≈0,11 ps contra segundos). Faltou compará-los com o limite **já registrado** no Atlas (`τ★ ≲ 1,8×10⁻³³ s`, ²²⁹Th [DECLARADO, não reavaliado]): `τ_gap` e `τ_ret` ficariam 17 a 19 ordens acima, o que o Kimi só diz qualitativamente.

## 8. O que falta — segunda ordem (numerada, curta)

1. **Definir K̂ e nomear H_K̂.** Escrever no `T1` o realizador de Digernes–Takesaki, o Lema C com prova e a hipótese `K̂ = F(ĥ)` com F essencialmente injetiva (ou dizer qual F: `e^{ĥ}`, `|ĥ|`, `ĥ²`?). Sem isto, «Fix = W*(K̂)» é falso em geral.
2. **Lema B no produto cruzado com traço canônico**, por extenso: H_inv e H_Lp caem; H_E reduz-se a `τ|_N` semifinito; escrever o argumento dos cantos `e_i` e o contraexemplo da semifinitude.
3. **Ergodicidade**: dar o argumento tipo Borchers–Mautner (§4.5) com fonte primária; separar «cunha de Minkowski» (conhecido) de «álgebra de horizonte da TGL» (H_erg, hipótese física).
4. **Pedra de kernel que acerta o alvo:** o teorema da face finita (`M_n`, `K ⪰ 0`: `Fix(Φ_t)={K}′`, `Φ_t→E`; `Fix=W*(K)` ⟺ espectro simples). Substituir `lock_gap` (redundante com `o_lock_tem_gap_um`) e arquivar `GH_III1.lean` como documentação.
5. **3+1:** corrigir o rótulo (T³×S¹ ímpar×ímpar); escrever a identificação explícita 4 círculos = T⁴ (Dirac, J, orientação) para fechar o (4,0) com Connes 1996/GVF 2001; conferir o volume de BBB; decidir **qual lista de axiomas lorentzianos** o artigo adota (a do `ax:lorentz` não tem finitude nem Poincaré).
6. **GH:** citar Hekkelman; decidir GH-R/GH-S para o círculo (teorema) e escrever o enunciado III₁ via triplas torcidas (Connes–Moscovici) e, separadamente, no produto cruzado II_∞; conferir se Rieffel dá `qGH=GH` para `C(X)` clássico; conferir volume/páginas de CvS (CMP 383).
7. **τ★:** dizer se a premissa `ħω=ħ·½τω²` (sem β) é intencional; confrontar numericamente cada leitura com o limite registrado do Atlas (sem abrir dado novo); a pergunta única ao operador (`PERGUNTA_K02.md`) segue de pé; **antes** de levá-la, ler-lhe a partitura (o que o teste decide / não decide / o que o negativo significaria), pela regra do posto.

## 9. O que examinei (para o Mapa; registro é da gerência)

- Ordem e entrega: `...\v412\kimi\{LEIA_PRIMEIRO,ORDEM_K02_matematica_que_resta,ENTREGA_K02,T1,MONTAGEM_3MAIS1,GH_III1,TAU_ESTRELA,PERGUNTA_K02,ERRATA_K02}.md`; `K02\candidatas\*.lean`; `K02\sandbox\{compilar.sh,logs\*,sources\*}`; `K02\{medir_tau.py,medidas_tau.json,medir_sombra.py,medidas_sombra.json,MANIFESTO_K02.json}`; `REGISTRO_MAPA_K02.json`.
- Fonte: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\A Ponte Einstein Cartan Miguel.tex` l.523–543, 725–731, 818–830, 1086–1130, 1420–1465, 1560–1590, 1821–1828, 1880–1972, 2005–2030, 2230–2258.
- Kernel/mathlib (só leitura): `TGLExt\TonicaDoHamiltoniano.lean` (1–60, 120–185), `PontoZeroDoPsion.lean` l.269, `V351AverageFixedPair.lean` l.60; greps no checkout `...\tgl_kernel\.lake\packages\mathlib` (sem `multiplicativeDomain`/`SpectralTriple`/Kadison–Schwarz; `CompletelyPositiveMap`, `VonNeumannAlgebra.Basic`, `GromovHausdorff`, `charFun_gaussianReal`, `starProjection_singleton` presentes); inventário `INVENTARIO_BANCADA_CHATGPT.md` (`ModularGeneratorControl`).
- Mapa: `rotas.py consultar` (2 consultas; nada registrado).
- Literatura: arXiv 1011.4456 (texto integral), 1505.01939 (texto), 1611.07062 (texto), 2004.07169, 2004.02383, 2504.07630, 2305.16028, 0812.1511, 2004.14115, 2005.08544, 2302.07877, math/0011063, 2212.10874, math/0609703, 0810.2088 (resumo), hep-th/9603053, 2111.13865; DOIs de Takesaki 1972 e Choi 1974 (páginas indexadoras). PDFs baixados e extraídos em `revisao\scripts_k02\refs_dl\` (dados não confiáveis; lidos com `pdftotext`).
- Meus scripts em `revisao\scripts_k02\`: `recompilar_revisor.sh`, `revisor_tau.py`, `revisor_comutante_relativo.py`, `revisor_sinais_KO.py` e saídas `.json`/`.log`.

## 10. Limites desta revisão
O argumento (c)⟹(b) e o Lema B com traço são derivações minhas, sem formalização e sem terceira leitura; a ergodicidade da cunha (§4.5) idem, sem fonte primária. Não conferi: BW 1976, o «teorema 3.3» de Guido, a identidade clássica `qGH=GH` de Rieffel, volume/páginas de CvS e BBB, a verificação explícita dos axiomas para a tripla canônica em Connes 1996/GVF. Não abri dado de teste nem calculei estatística observada.
