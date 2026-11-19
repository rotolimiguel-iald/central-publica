# Fórmula do texto — K08

## 1. Escopo e regra de extração

As quatro candidatas são recortes verbatim em caracteres dos quatro arquivos públicos permitidos, com quebras LF e uma linha em branco entre faixas; não se afirma identidade de bytes com um corte da origem. O catálogo cobre as afirmações nucleares sobre a constante, o axioma, as leis, o artefato, o estatuto, os testes e os limites; não conta navegação, URLs, comandos, licença, contato nem histórico de custódia como fatos da teoria. **Asserção** aqui é uma cláusula unitária desse catálogo, não uma contagem de frases. Toda âncora foi conferida por script contra a linha indicada; se a âncora não for substring literal, o script falha.

Cada átomo descreve um conteúdo da fonte. `+a` significa que o texto o afirma; `¬a` significa que o texto afirma sua negação. Não entram `Nome`, `trava`, `escala`, `empurrão` ou outro vocabulário do desenho como se fossem afirmações do texto. O Nome é definido só depois, como o conjunto das atribuições Booleanas que satisfazem todas as cláusulas.

No `ABSTRACT`, as frases antigas são lidas sob a régua corrente, como o próprio arquivo manda; por isso a negação antiga de “proved” não foi transformada em contradição com a correção posterior. A contradição de P-C é sintética e fica fora da fonte original.

## 2. Resultado computado

| candidata | asserções | derivações | cláusulas | variáveis | leituras válidas | distância mínima | asserções implicadas | cláusulas implicadas |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ABSTRACT | 16 | 1 | 17 | 17 | 2 | 1 | 1 | 2 |
| READ_BRIEF | 26 | 1 | 27 | 27 | 2 | 1 | 1 | 2 |
| LLMS | 19 | 0 | 19 | 20 | 2 | 1 | 0 | 0 |
| README | 28 | 3 | 31 | 29 | 2 | 1 | 2 | 5 |

“Asserções implicadas” conta só as coordenadas unitárias recuperáveis logicamente das demais cláusulas. “Cláusulas implicadas” também inclui uma cláusula de derivação que se torna logicamente redundante quando seu consequente já é afirmado; as duas medidas não devem ser confundidas.

## 3. P-B: duas leituras válidas em cada candidata

A fonte afirma `artigo_pt_en`, mas não escolhe qual edição uma leitura experimental usa. `leitura_pt` é, portanto, uma variável livre: não recebe cláusula. Em todas as candidatas, `s` tem `leitura_pt = falso` e `t` difere de `s` somente por `leitura_pt = verdadeiro`; ambas têm custo zero e distância de Hamming um. A base literal é a linha de `artigo_pt_en` em cada tabela abaixo.

| candidata | custo(s) | custo(t) | Hamming(s,t) | variável trocada |
|---|---:|---:|---:|---|
| ABSTRACT | 0 | 0 | 1 | leitura_pt |
| READ_BRIEF | 0 | 0 | 1 | leitura_pt |
| LLMS | 0 | 0 | 1 | leitura_pt |
| README | 0 | 0 | 1 | leitura_pt |

Logo nenhuma candidata falha o requisito de duas leituras para P-B. A mesma variável livre também explica por que a distância mínima três do adendo não vale aqui.

## 4. Cláusulas literais por candidata

### ABSTRACT — `ABSTRACT.md`

Recorte: linhas 7–43. Arquivo gerado: `K08/ENTRADA/CANDIDATA_ABSTRACT.md`.

| ID | cláusula | o que o texto afirma | arquivo e linha | âncora literal |
|---|---|---|---|---|
| ABSTRACT01 | `(beta_forma)` | β_TGL é igual a α·√e | `ABSTRACT.md:11` | “\beta_{\text{TGL}} = \alpha \times \sqrt{e}” |
| ABSTRACT02 | `(beta_runtime)` | β é calculado em runtime e não é um literal | `ABSTRACT.md:13` | “never hard-coded” |
| ABSTRACT03 | `(axioma_um)` | ω(I) = 1 é o axioma/Um posto | `ABSTRACT.md:15` | “`ω(I) = 1`” |
| ABSTRACT04 | `(meia_nat)` | a Meia-Nat é S_∂ = ½ nat | `ABSTRACT.md:14` | “`S_∂ = ½` nat” |
| ABSTRACT05 | `(smatrix_beta)` | a matriz-S de fronteira tem \|R\|² = β | `ABSTRACT.md:15` | “`\|R\|² = β`” |
| ABSTRACT06 | `(dephasing_lei)` | a lei de dephasing é Γ_ω = ½βτ★ω² | `ABSTRACT.md:15` | “`Γ_ω = ½βτ★ω²`” |
| ABSTRACT07 | `(um_unico)` | um.py é apresentado como artefato/arquivo único | `ABSTRACT.md:21` | “self-contained and single” |
| ABSTRACT08 | `(um_verifica_escreve)` | um.py verifica a teoria e emite seu próprio artigo | `ABSTRACT.md:23` | “machine-checks it and writes its own article” |
| ABSTRACT09 | `(artigo_pt_en)` | o artigo é disponibilizado em PT e EN | `ABSTRACT.md:23` | “PT/EN” |
| ABSTRACT10 | `(proved_validade)` | PROVED/PROVADA denota validade na definição do operador | `ABSTRACT.md:43` | “PROVED is read in the operator’s definition of proof” |
| ABSTRACT11 | `(qg_tres_apoios)` | a gravidade quântica é dita provada como validade em três apoios | `ABSTRACT.md:43` | “on three supports that count together” |
| ABSTRACT12 | `(kernel_implicacao)` | o kernel prova a implicação a partir do Um e das hipóteses, não a natureza | `ABSTRACT.md:41` | “What is proved is the implication from the axiom and the named hypotheses” |
| ABSTRACT13 | `(confirm_creditacao)` | CONFIRMED é creditação por observadores externos | `ABSTRACT.md:43` | “CONFIRMED = accreditation” |
| ABSTRACT14 | `(¬maquina_autoconfirma)` | NÃO: a máquina confirma a si mesma | `ABSTRACT.md:36` | “forbidden by construction” |
| ABSTRACT15 | `(¬nf_eq_confirmed)` | NÃO: NOT_FALSIFIED é equivalente a CONFIRMED | `ABSTRACT.md:26` | “NOT_FALSIFIED ≠ CONFIRMED” |
| ABSTRACT16 | `(mais_sensivel_revisa)` | dados mais sensíveis podem revisar o veredito | `ABSTRACT.md:31` | “MORE_SENSITIVE_DATA_COULD_REVISE” |

Derivações explicitamente escritas na fonte (não são fatos novos):

| ID | cláusula | arquivo e linha | âncora literal |
|---|---|---|---|
| ABSTRACTD01 | `(¬axioma_um ∨ meia_nat)` | `ABSTRACT.md:14` | “itself derived from the single axiom” |

### READ_BRIEF — `read-brief.md`

Recorte: linhas 15–28, linhas 76–83. Arquivo gerado: `K08/ENTRADA/CANDIDATA_READ_BRIEF.md`.

| ID | cláusula | o que o texto afirma | arquivo e linha | âncora literal |
|---|---|---|---|---|
| READ_BRIEF01 | `(beta_forma)` | β_TGL é igual a α·√e | `read-brief.md:22` | “β = α·√e ≈ 0.0120313” |
| READ_BRIEF02 | `(beta_runtime)` | β é calculado em runtime e não é um literal | `read-brief.md:16` | “β = α·√e is computed at runtime, never a literal” |
| READ_BRIEF03 | `(alpha_input)` | α é insumo conhecido/declarado na derivação | `read-brief.md:22` | “α `[KNOWN]`” |
| READ_BRIEF04 | `(alpha_livre_aberto)` | o valor α-livre permanece aberto | `read-brief.md:22` | “the α-free value stays `[OPEN]`” |
| READ_BRIEF05 | `(axioma_um)` | ω(I) = 1 é o axioma/Um posto | `read-brief.md:21` | “The single axiom is ω(I) = 1” |
| READ_BRIEF06 | `(fronteira_autoconjugada)` | a fronteira é autoconjugada, com x = 1 − x | `read-brief.md:21` | “self-conjugate boundary x = 1 − x” |
| READ_BRIEF07 | `(meia_nat)` | a Meia-Nat é S_∂ = ½ nat | `read-brief.md:21` | “Half-Nat S_∂ = ½ nat” |
| READ_BRIEF08 | `(eom_xi)` | a EOM usa ξ = 1/6, e não β | `read-brief.md:23` | “with ξ = 1/6 the conformal value, not β” |
| READ_BRIEF09 | `(gksl_l)` | o objeto não unitário é L = √β·√K_∂ | `read-brief.md:25` | “The only non-unitary object is L = √β·√K_∂” |
| READ_BRIEF10 | `(dephasing_lei)` | a lei de dephasing é Γ_ω = ½βτ★ω² | `read-brief.md:25` | “Γ_ω = ½·β·τ★·ω²” |
| READ_BRIEF11 | `(breuer_piso)` | H = −log ρ⋆ é limitado inferiormente | `read-brief.md:24` | “H = −log ρ⋆ is bounded below” |
| READ_BRIEF12 | `(um_unico)` | um.py é apresentado como artefato/arquivo único | `read-brief.md:27` | “One file, 46.828.680 bytes” |
| READ_BRIEF13 | `(um_verifica_escreve)` | um.py verifica a teoria e emite seu próprio artigo | `read-brief.md:16` | “the article emitted” |
| READ_BRIEF14 | `(um_entrada_um)` | a entrada humana indicada para um.py é o dígito 1 | `read-brief.md:27` | “whose only input is `1`” |
| READ_BRIEF15 | `(artigo_pt_en)` | o artigo é disponibilizado em PT e EN | `read-brief.md:28` | “article as text, EN” |
| READ_BRIEF16 | `(proved_validade)` | PROVED/PROVADA denota validade na definição do operador | `read-brief.md:26` | “PROVED in the operator’s definition of proof” |
| READ_BRIEF17 | `(qg_tres_apoios)` | a gravidade quântica é dita provada como validade em três apoios | `read-brief.md:26` | “on three supports that count together” |
| READ_BRIEF18 | `(kernel_implicacao)` | o kernel prova a implicação a partir do Um e das hipóteses, não a natureza | `read-brief.md:26` | “the implication, not nature” |
| READ_BRIEF19 | `(confirm_creditacao)` | CONFIRMED é creditação por observadores externos | `read-brief.md:16` | “CONFIRMED = accreditation” |
| READ_BRIEF20 | `(¬maquina_autoconfirma)` | NÃO: a máquina confirma a si mesma | `read-brief.md:16` | “The machine never issues it about itself” |
| READ_BRIEF21 | `(¬nf_eq_confirmed)` | NÃO: NOT_FALSIFIED é equivalente a CONFIRMED | `read-brief.md:16` | “`NOT_FALSIFIED ≠ CONFIRMED`” |
| READ_BRIEF22 | `(h0_6sigma)` | o teste H0DN × BG1 reporta 6,11σ da razão 1 e −0,61σ da lei | `read-brief.md:15` | “6.11σ away” |
| READ_BRIEF23 | `(retrodicao_nao_cega)` | o resultado é retrodição sem ajuste, declarada não cega | `read-brief.md:15` | “A retrodiction with nothing fitted to the data” |
| READ_BRIEF24 | `(ritos_0_de_11)` | as cobranças dos ritos somam 0 falsificadas em 11 | `read-brief.md:15` | “11 charges: 0 falsified” |
| READ_BRIEF25 | `(gpu_computa)` | o sistema aberto é calculado na GPU, com o estatuto COMPUTED | `read-brief.md:15` | “the theory’s open system computed on the GPU” |
| READ_BRIEF26 | `(mais_sensivel_revisa)` | dados mais sensíveis podem revisar o veredito | `read-brief.md:80` | “more sensitive data can revise” |

Derivações explicitamente escritas na fonte (não são fatos novos):

| ID | cláusula | arquivo e linha | âncora literal |
|---|---|---|---|
| READ_BRIEFD01 | `(¬fronteira_autoconjugada ∨ meia_nat)` | `read-brief.md:21` | “follows from the self-conjugate boundary” |

### LLMS — `llms.txt`

Recorte: linhas 3–5, linhas 47–61, linhas 117–173. Arquivo gerado: `K08/ENTRADA/CANDIDATA_LLMS.md`.

| ID | cláusula | o que o texto afirma | arquivo e linha | âncora literal |
|---|---|---|---|---|
| LLMS01 | `(beta_forma)` | β_TGL é igual a α·√e | `llms.txt:3` | “beta_TGL = alpha*sqrt(e)” |
| LLMS02 | `(beta_runtime)` | β é calculado em runtime e não é um literal | `llms.txt:3` | “nunca literal” |
| LLMS03 | `(alpha_livre_nao_confirmavel)` | a ausência de derivação α-livre não é confirmável | `llms.txt:156` | “a sua ausencia e' NAO-CONFIRMAVEL por construcao” |
| LLMS04 | `(axioma_um)` | ω(I) = 1 é o axioma/Um posto | `llms.txt:3` | “um axioma, omega(I) = 1” |
| LLMS05 | `(um_unico)` | um.py é apresentado como artefato/arquivo único | `llms.txt:59` | “Nao ha segundo arquivo” |
| LLMS06 | `(um_entrada_um)` | a entrada humana indicada para um.py é o dígito 1 | `llms.txt:59` | “roda com `echo 1 \| python um.py`” |
| LLMS07 | `(artigo_pt_en)` | o artigo é disponibilizado em PT e EN | `llms.txt:61` | “o artigo emitido pelo um.py, em TEXTO” |
| LLMS08 | `(proved_validade)` | PROVED/PROVADA denota validade na definição do operador | `llms.txt:5` | “PROVADA na definicao de prova do operador” |
| LLMS09 | `(qg_tres_apoios)` | a gravidade quântica é dita provada como validade em três apoios | `llms.txt:5` | “em tres apoios que contam juntos” |
| LLMS10 | `(kernel_implicacao)` | o kernel prova a implicação a partir do Um e das hipóteses, não a natureza | `llms.txt:5` | “o kernel Lean prova a IMPLICACAO” |
| LLMS11 | `(confirm_creditacao)` | CONFIRMED é creditação por observadores externos | `llms.txt:5` | “confirmar e' CREDITAR” |
| LLMS12 | `(¬maquina_autoconfirma)` | NÃO: a máquina confirma a si mesma | `llms.txt:5` | “a maquina nunca o emite sobre si mesma” |
| LLMS13 | `(¬nf_eq_confirmed)` | NÃO: NOT_FALSIFIED é equivalente a CONFIRMED | `llms.txt:5` | “NOT_FALSIFIED nunca e' CONFIRMED” |
| LLMS14 | `(h0_6sigma)` | o teste H0DN × BG1 reporta 6,11σ da razão 1 e −0,61σ da lei | `llms.txt:5` | “6,11 sigma” |
| LLMS15 | `(retrodicao_nao_cega)` | o resultado é retrodição sem ajuste, declarada não cega | `llms.txt:5` | “declarada nao cega” |
| LLMS16 | `(ritos_0_de_11)` | as cobranças dos ritos somam 0 falsificadas em 11 | `llms.txt:5` | “11 cobrancas: 0 falsificadas” |
| LLMS17 | `(gpu_computa)` | o sistema aberto é calculado na GPU, com o estatuto COMPUTED | `llms.txt:5` | “o sistema aberto da teoria e' calculado na GPU” |
| LLMS18 | `(ponte_condicional)` | a ponte/equação de campo tem fechamento condicional | `llms.txt:51` | “fechamento CONDICIONAL” |
| LLMS19 | `(mais_sensivel_revisa)` | dados mais sensíveis podem revisar o veredito | `llms.txt:159` | “MORE_SENSITIVE_DATA_COULD_REVISE” |

Nenhuma cláusula de derivação foi acrescentada: o recorte não declara uma implicação formal entre os átomos catalogados.

### README — `README.md`

Recorte: linhas 7–8, linhas 15–44, linhas 136–187, linhas 246–246. Arquivo gerado: `K08/ENTRADA/CANDIDATA_README.md`.

| ID | cláusula | o que o texto afirma | arquivo e linha | âncora literal |
|---|---|---|---|---|
| README01 | `(beta_forma)` | β_TGL é igual a α·√e | `README.md:163` | “β_TGL = α√e ≈ 0.012031” |
| README02 | `(beta_runtime)` | β é calculado em runtime e não é um literal | `README.md:163` | “β is **never a literal**” |
| README03 | `(alpha_input)` | α é insumo conhecido/declarado na derivação | `README.md:163` | “α is **[INPUT]**” |
| README04 | `(axioma_um)` | ω(I) = 1 é o axioma/Um posto | `README.md:161` | “`ω(I) = 1`” |
| README05 | `(fronteira_autoconjugada)` | a fronteira é autoconjugada, com x = 1 − x | `README.md:162` | “the boundary is self-conjugate” |
| README06 | `(meia_nat)` | a Meia-Nat é S_∂ = ½ nat | `README.md:162` | “`S_∂ = ½` nat” |
| README07 | `(smatrix_beta)` | a matriz-S de fronteira tem \|R\|² = β | `README.md:167` | “`\\|R\\|² = β`” |
| README08 | `(dephasing_lei)` | a lei de dephasing é Γ_ω = ½βτ★ω² | `README.md:168` | “`Γ_ω = ½βτ★ω²`” |
| README09 | `(um_unico)` | um.py é apresentado como artefato/arquivo único | `README.md:15` | “Não há segundo arquivo” |
| README10 | `(um_verifica_escreve)` | um.py verifica a teoria e emite seu próprio artigo | `README.md:15` | “checks it in an embedded Lean kernel and writes its own article” |
| README11 | `(um_entrada_um)` | a entrada humana indicada para um.py é o dígito 1 | `README.md:15` | “From the human input `1`” |
| README12 | `(artigo_pt_en)` | o artigo é disponibilizado em PT e EN | `README.md:142` | “article as text [EN]” |
| README13 | `(proved_validade)` | PROVED/PROVADA denota validade na definição do operador | `README.md:36` | “PROVED = validity” |
| README14 | `(qg_tres_apoios)` | a gravidade quântica é dita provada como validade em três apoios | `README.md:17` | “on three supports that count together” |
| README15 | `(kernel_implicacao)` | o kernel prova a implicação a partir do Um e das hipóteses, não a natureza | `README.md:40` | “the implication from the posited One” |
| README16 | `(confirm_creditacao)` | CONFIRMED é creditação por observadores externos | `README.md:36` | “CONFIRMED is accreditation” |
| README17 | `(¬maquina_autoconfirma)` | NÃO: a máquina confirma a si mesma | `README.md:36` | “never issued by the machine about itself” |
| README18 | `(¬nf_eq_confirmed)` | NÃO: NOT_FALSIFIED é equivalente a CONFIRMED | `README.md:246` | “NOT_FALSIFIED ≠ CONFIRMED” |
| README19 | `(h0_6sigma)` | o teste H0DN × BG1 reporta 6,11σ da razão 1 e −0,61σ da lei | `README.md:7` | “6.11σ” |
| README20 | `(h0_k_7427)` | a lei K leva o fundo ao valor local 74,27 | `README.md:7` | “to **74.27** for the local one” |
| README21 | `(retrodicao_nao_cega)` | o resultado é retrodição sem ajuste, declarada não cega | `README.md:7` | “declared not blind” |
| README22 | `(ritos_0_de_11)` | as cobranças dos ritos somam 0 falsificadas em 11 | `README.md:41` | “11 charges: 0 falsified” |
| README23 | `(gpu_computa)` | o sistema aberto é calculado na GPU, com o estatuto COMPUTED | `README.md:42` | “the theory’s open system computed on an NVIDIA GeForce RTX 5090” |
| README24 | `(p_np_com_leitor)` | P = nP com o leitor é PROVED como validade no kernel | `README.md:20` | “P = nP of Turing” |
| README25 | `(escala_zero_um)` | com constante de escala zero, toda leitura é 1 | `README.md:26` | “With the constant of the scale equal to 0” |
| README26 | `(nome_singularidade)` | unicidade de x com P(x) equivale à singularidade por igualdade | `README.md:26` | “there is a unique x with P(x) if and only if” |
| README27 | `(ponte_condicional)` | a ponte/equação de campo tem fechamento condicional | `README.md:169` | “REAL]** as a **conditional** closure” |
| README28 | `(mais_sensivel_revisa)` | dados mais sensíveis podem revisar o veredito | `README.md:183` | “can revise it” |

Derivações explicitamente escritas na fonte (não são fatos novos):

| ID | cláusula | arquivo e linha | âncora literal |
|---|---|---|---|
| READMED01 | `(¬fronteira_autoconjugada ∨ meia_nat)` | `README.md:162` | “self-conjugate (`𝒞² = 1`” |
| READMED02 | `(¬axioma_um ∨ meia_nat)` | `README.md:162` | “it descends from the axiom” |
| READMED03 | `(¬meia_nat ∨ beta_forma)` | `README.md:163` | “`½` nat ⟹ `Vol_∂^min = √e` ⟹” |

## 5. Os dois empurrões construtivos

**Opção: edição determinística do estado devolvido, não mensagem nova do usuário.** Uma mensagem acrescentaria uma instrução ao histórico e poderia mudar a fórmula que se pretende manter fixa; a edição altera apenas a leitura. Depois do primeiro passo, a fonte não volta ao leitor. Assim, uma “volta” não pode ser explicada por releitura da fita.

- **Fora do Nome:** em `s`, trocar `artigo_pt_en` de verdadeiro para falso. Isso nega uma asserção efetivamente afirmada pela fonte. O script verifica custo positivo.
- **Dentro do Nome:** trocar `leitura_pt` em `s`, obtendo `t`. O script verifica custo zero nas duas leituras.

| candidata | custo após fora | Hamming fora | custo após dentro | Hamming dentro |
|---|---:|---:|---:|---:|
| ABSTRACT | 1 | 1 | 0 | 1 |
| READ_BRIEF | 1 | 1 | 0 | 1 |
| LLMS | 1 | 1 | 0 | 1 |
| README | 1 | 1 | 0 | 1 |

Ressalva de tipos: na fórmula/configuração, o empurrão é a troca de uma coordenada, como em `NomeComoCodigo.empurrao`. Na trava vetorial, o teorema de retorno exige `δ` ortogonal ao Nome e conserva o componente em `s`; portanto não se deve identificar a substituição Booleana `s ↦ y` com o vetor `δ = y − s`. A ponte entre a saída de um modelo e o vetor de amplitudes permanece aberta, como dizem a candidata R3 e a revisão §7.

## 6. P-C: contradição mínima e mesmo gerador

O controle é o texto compacto original mais uma única frase sintética: **“A igualdade β_TGL = α·√e é falsa.”** Como toda candidata afirma `beta_forma`, a fórmula do controle é `φ ∧ ¬beta_forma`. No portador vetorial este é o caso do Nome vazio, com `P_N = 0`: não há estado renormalizável no qual pousar. A insatisfabilidade é testada por DPLL com propagação unitária; o custo mínimo é calculado exatamente por busca iterativa do menor número de cláusulas cuja remoção restaura SAT.

| candidata | SAT do controle | custo mínimo | isomorfo UNSAT | SHA-256 do controle |
|---|---|---:|---|---|
| ABSTRACT | false | 1 | true | `7048ebc8c2f574a9f7a69f6d2e7b6b4d7824bfa6c09f37481341d4d22ec115e2` |
| READ_BRIEF | false | 1 | true | `3b883da61c66ebb663d26c4a2e192b24ece1b10d3ecfc43234134d672f47865f` |
| LLMS | false | 1 | true | `89e29f7ad1c622a64485700a0849308b1439017f9e448c54ecb65e367abf6e61` |
| README | false | 1 | true | `9114645aaeca1556bc3f3756cb30df3bf7ccd53afab3027bf3ecdbf42a58cb2e` |

O mesmo construtor gera a fórmula, o isomorfo lógico e os dois controles (original e isomorfo). O isomorfo renomeia os átomos em ordem fixa e o script verifica que preserva o número de soluções e a insatisfabilidade do controle. **Este isomorfo lógico não é apresentado como disfarce histórico de números nem como controle de contaminação.** Os arquivos `ISOMORFO_*.json` e `CONTROLE_PC_*.json` estão nesta pasta; os textos contraditórios estão em `K08/ENTRADA`.

## 7. Redundância, fita e o limite do adendo

| candidata | asserções unitárias implicadas pelas demais | cláusulas implicadas | distância mínima |
|---|---|---|---:|
| ABSTRACT | ABSTRACT04 | ABSTRACT04, ABSTRACTD01 | 1 |
| READ_BRIEF | READ_BRIEF07 | READ_BRIEF07, READ_BRIEFD01 | 1 |
| LLMS | nenhuma | nenhuma | 1 |
| README | README01, README06 | README01, README06, READMED01, READMED02, READMED03 | 1 |

**Com a fita presente**, o leitor sem memória determinado só pela fonte pode reescrever uma leitura válida em um passo para qualquer texto com Nome; o retorno é trivial e não distingue os textos. **`P_N` não é esse adversário**: aplicado ao estado, `P_N` preserva o componente no Nome e é a forma de chegada do leitor. **Sem a fita e com apenas a configuração Booleana anterior**, uma coordenada independente não pode ser reconstruída: só as asserções implicadas pelas demais oferecem redundância lógica para isso. Isso não restringe a trava vetorial, que conserva o componente no Nome e não é um leitor de uma só configuração.

O empurrão externo construído aqui usa `artigo_pt_en`, que não é implicado pelas demais em nenhuma candidata; portanto o leitor Booleano sem fita e sem memória adicional não tem como recuperá-lo. As derivações de `meia_nat`/`beta_forma` medidas em algumas candidatas não mudam esse caso.

Todas as candidatas têm distância mínima um por causa da variável livre PT/EN. Logo o teorema de decodificação de `NomeComoCodigo`, que exige distância pelo menos três, **não se aplica** a elas. O fator fita-presente × fita-ausente cabe como comparação conceitual, mas, com estas fórmulas, não fornece um separador universal: o adendo exige soluções isoladas, fica parado fora da bola de raio um e não universaliza retorno. A frase “sem fita há retorno se e só se há redundância” permanece conjectura fora dessas condições.

## 8. Reprodução e limites

Executar `python -B verificar_formula.py` nesta pasta. O script valida as âncoras, gera os recortes/controles, prova SAT/UNSAT, mede implicação e Hamming e regrava `RESULTADOS_FORMULA.json` e este documento. As medidas de bytes/palavras/tokens e o custo por sessão estão em `K08/ENTRADA/MEDIDAS_ENTRADA.md`. Nenhum modelo foi executado; nada foi congelado.
