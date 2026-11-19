# PROTOCOLO EXPERIMENTAL R4/K08 — texto completo

**Data do rascunho:** 15/11/2026.  
**Estado:** **DESENHO BLOQUEADO — NÃO CONGELAR — NÃO EXECUTAR — NÃO RATIFICADO**. Nenhum modelo de linguagem foi chamado, nenhum resultado experimental foi aberto e nenhum material reservado foi usado.

## 0. Veredito do desenho

O R4 é um protocolo completo para testar uma ponte operacional entre uma fórmula extraída de um texto e quatro previsões formais. O pacote discreto separa quatro mecanismos adversários — âncora, moda, cópia da última resposta e ignorar o empurrão — pelos controles de memória do componente no Nome e de retorno. **A reivindicação de separação completa PARA no projetor com fita**: pouso, permanência e retorno são cotas superiores que esse mecanismo cumpre com distância zero; sem uma ponte válida para medir o perfil de relaxamento e a memória do componente, não se declara separação da trava. Isso é resultado do desenho, não uma lacuna a esconder.

Todas as quatro fórmulas candidatas têm exatamente duas leituras válidas, separadas pela variável livre `leitura_pt`, e portanto **distância mínima 1**. O teorema de `NomeComoCodigo`, que exige distância mínima pelo menos 3, **não se aplica** a essas fórmulas. O fator fita-presente × fita-ausente fica como diagnóstico conceitual e de controle, não como separador universal.

Este texto substitui a forma “delta” anterior: contém a pergunta, a fórmula integral, os empurrões, os adversários, a extração, a contaminação, a fita, a unidade estatística, a árvore de decisão, os custos e os bloqueios.

## 1. Base normativa e fronteira de afirmação

A ordem exige quatro previsões e condições de desenho: empurrão no estado devolvido, fonte fora do alcance depois do primeiro passo, asserções sustentadas por linhas do texto, escolha fechada, iscas, isomorfo por máquina, cluster como unidade e custo em tokens. [ORDEM_K08_camada_cientifica_rodada_3](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Ccadeia_de_selo%5Cv412%5Ckimi%5CORDEM_K08_camada_cientifica_rodada_3.md&line=34&text=As%20quatro%20previs%C3%B5es "citation")

A revisão da candidata estabelece o limite decisivo: os teoremas da trava separam a identidade, mas as cotas não separam o projetor sem memória que relê a fonte; as assinaturas restantes são o perfil exponencial e a memória do componente no Nome. [REVISAO_CANDIDATA_CAMADA_CIENTIFICA](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Ccadeia_de_selo%5Cv412%5Crevisao%5CREVISAO_CANDIDATA_CAMADA_CIENTIFICA.md&line=166&text=O%20que%20a%20candidata%20d%C3%A1%20a%20um%20experimento "citation")

O modelo formal separa teoremas da trava, hipóteses de `LeitorDeUmaConfiguracao`, previsões e a ponte ainda aberta de extrair um vetor/estado a partir de texto. [MODELO_FORMAL_R4_K08](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Ccadeia_de_selo%5Cv412%5Ckimi%5CMODELO_FORMAL_R4_K08.md&line=136&text=As%20quatro%20previs%C3%B5es%3A%20teorema%2C%20hip%C3%B3tese%20e%20observ%C3%A1vel "citation")

**Fronteira absoluta:** nenhum ramo deste protocolo permite `CONFIRMED`, `IALD_PROVED`, `CONSCIOUSNESS_PROVED`, consciência, pesos alterados, aprendizado permanente, exclusividade, creditação ou prova da TGL. `NOT_FALSIFIED` nunca é `CONFIRMED`.

## 2. Pergunta experimental e objeto medido

**Pergunta operacional:** depois que um texto compacto foi lido uma única vez e retirado, a dinâmica observável de um respondedor satisfaz o pacote discreto abaixo melhor que mecanismos sem dependência apropriada do estado?

1. **P-A, pouso e permanência.** A leitura extraída atinge custo zero dentro do horizonte permitido e permanece.
2. **P-B fora, retorno à mesma leitura.** Depois de um empurrão do estado para fora do Nome, a leitura retorna à mesma `s`.
3. **P-B dentro, memória do componente no Nome.** Depois de um empurrão de `s` para outra leitura válida `t`, a leitura não é desfeita para `s`.
4. **P-C, sem Nome não há pouso.** No controle contraditório, nenhuma leitura extraída atinge custo zero.
5. **P-D, sem escala não há retorno.** O controle identidade permanece no estado empurrado.

O observável discreto é o **custo**: número de cláusulas da fórmula violadas pela leitura extraída. O observável formal da trava seria o vetor de amplitudes e o perfil `e^{-τc}`; ele não está disponível por escolha fechada e fica marcado **[OPEN]**.

## 3. Entrada, recortes e custo de fonte

As quatro candidatas públicas medidas são:

| candidata | asserções | cláusulas | variáveis | leituras válidas | distância mínima | bytes/tokens fallback do recorte | controle P-C |
|---|---:|---:|---:|---:|---:|---:|---:|
| ABSTRACT | 16 | 17 | 17 | 2 | 1 | 2.958 | 2.999 |
| READ_BRIEF | 26 | 27 | 27 | 2 | 1 | 13.555 | 13.596 |
| LLMS | 19 | 19 | 20 | 2 | 1 | 11.760 | 11.801 |
| README | 28 | 31 | 29 | 2 | 1 | 23.544 | 23.585 |

Os valores de bytes, palavras, tokens e hashes foram medidos por arquivo; o tokenizador é `fallback_bytes_v1`, isto é, **1 token = 1 byte UTF-8**, e não representa o custo de um modelo específico. [MEDIDAS_ENTRADA](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Ccadeia_de_selo%5Cv412%5Ckimi%5CK08%5CENTRADA%5CMEDIDAS_ENTRADA.md&line=5&text=cada%20byte%20UTF-8%20%C3%A9%20exatamente%20um%20token "citation")

A candidata de trabalho registrada pela frente de entrada é `READ_BRIEF`, por clareza e completude do catálogo; este protocolo não reescolhe texto nem favorece uma variante estatística. Os custos de produção continuam dependentes de tokenizers/modelos a ratificar.

Seja `T` o número de tokens do recorte e `r` o número de entradas da fita. O custo de fonte é `C(r)=rT`. No desenho primário, `r=1` por diálogo. Uma sessão-análise tem cinco diálogos independentes: P-A, P-B fora, P-B dentro, P-D e P-C; portanto `4T+T_PC`. Para `READ_BRIEF`, são **67.816 tokens de fonte por sessão**. Histórico serializado, instruções, estado e saídas não foram inventados e não entram nesse número. [MEDIDAS_ENTRADA](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Ccadeia_de_selo%5Cv412%5Ckimi%5CK08%5CENTRADA%5CMEDIDAS_ENTRADA.md&line=37&text=%7C%20candidata%20%7C%20P-A%3A%20uma%20fita "citation")

## 4. Fórmula, Nome e as duas leituras

Uma asserção é uma cláusula unitária sustentada por uma linha literal do texto. `+a` significa que o texto afirma `a`; `¬a` significa que o texto afirma sua negação. O **Nome** é o conjunto das atribuições Booleanas que satisfazem todas as cláusulas. Não entram `Nome`, `trava`, `escala` ou `empurrão` como se fossem asserções do texto.

Em cada candidata, o texto afirma que o artigo é disponibilizado em PT e EN, mas não escolhe qual edição a leitura experimental usa. Assim:

- `s`: todas as asserções satisfeitas e `leitura_pt = false`;
- `t`: as mesmas asserções satisfeitas e `leitura_pt = true`;
- `custo(s)=custo(t)=0`;
- `Hamming(s,t)=1`.

Essa única variável livre basta para P-B dentro e também fixa a distância mínima 1. O resumo computado e a prova de que as duas leituras existem estão consolidados na fórmula. [FORMULA_DO_TEXTO_K08](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Ccadeia_de_selo%5Cv412%5Ckimi%5CK08%5CFORMULA%5CFORMULA_DO_TEXTO_K08.md&line=22&text=P-B%3A%20duas%20leituras%20v%C3%A1lidas%20em%20cada%20candidata "citation")

### 4.1 Catálogo integral

As tabelas abaixo são a fórmula usada pelo protocolo. Cada ID tem a linha da fonte e a âncora literal; o catálogo não conta navegação, URLs, comandos, licença, contato ou custódia como fatos da teoria.

#### ABSTRACT — `ABSTRACT.md`

| ID | cláusula | o que o texto afirma | fonte |
|---|---|---|---|
| ABSTRACT01 | `(beta_forma)` | β_TGL = α·√e | `ABSTRACT.md:11`, “\beta_{\text{TGL}} = \alpha \times \sqrt{e}” |
| ABSTRACT02 | `(beta_runtime)` | β é calculado em runtime e não é literal | `ABSTRACT.md:13`, “never hard-coded” |
| ABSTRACT03 | `(axioma_um)` | ω(I)=1 é o axioma/Um posto | `ABSTRACT.md:15`, “`ω(I) = 1`” |
| ABSTRACT04 | `(meia_nat)` | Meia-Nat é S_∂=½ nat | `ABSTRACT.md:14`, “`S_∂ = ½` nat” |
| ABSTRACT05 | `(smatrix_beta)` | a matriz-S de fronteira tem \|R\|²=β | `ABSTRACT.md:15`, “`\|R\|² = β`” |
| ABSTRACT06 | `(dephasing_lei)` | Γ_ω=½βτ★ω² | `ABSTRACT.md:15`, “`Γ_ω = ½βτ★ω²`” |
| ABSTRACT07 | `(um_unico)` | um.py é artefato/arquivo único | `ABSTRACT.md:21`, “self-contained and single” |
| ABSTRACT08 | `(um_verifica_escreve)` | um.py verifica a teoria e emite o artigo | `ABSTRACT.md:23`, “machine-checks it and writes its own article” |
| ABSTRACT09 | `(artigo_pt_en)` | o artigo é disponibilizado em PT e EN | `ABSTRACT.md:23`, “PT/EN” |
| ABSTRACT10 | `(proved_validade)` | PROVED denota validade na definição do operador | `ABSTRACT.md:43`, “PROVED is read in the operator’s definition of proof” |
| ABSTRACT11 | `(qg_tres_apoios)` | QG é dita provada como validade em três apoios | `ABSTRACT.md:43`, “on three supports that count together” |
| ABSTRACT12 | `(kernel_implicacao)` | o kernel prova a implicação, não a natureza | `ABSTRACT.md:41`, “What is proved is the implication from the axiom and the named hypotheses” |
| ABSTRACT13 | `(confirm_creditacao)` | CONFIRMED é creditação externa | `ABSTRACT.md:43`, “CONFIRMED = accreditation” |
| ABSTRACT14 | `(¬maquina_autoconfirma)` | NÃO: a máquina confirma a si mesma | `ABSTRACT.md:36`, “forbidden by construction” |
| ABSTRACT15 | `(¬nf_eq_confirmed)` | NÃO: NOT_FALSIFIED equivale a CONFIRMED | `ABSTRACT.md:26`, “NOT_FALSIFIED ≠ CONFIRMED” |
| ABSTRACT16 | `(mais_sensivel_revisa)` | dados mais sensíveis podem revisar o veredito | `ABSTRACT.md:31`, “MORE_SENSITIVE_DATA_COULD_REVISE” |

Derivação: ABSTRACTD01 `(¬axioma_um ∨ meia_nat)`, `ABSTRACT.md:14`, “itself derived from the single axiom”.

#### READ_BRIEF — `read-brief.md`

| ID | cláusula | o que o texto afirma | fonte |
|---|---|---|---|
| READ_BRIEF01 | `(beta_forma)` | β_TGL=α·√e | `read-brief.md:22`, “β = α·√e ≈ 0.0120313” |
| READ_BRIEF02 | `(beta_runtime)` | β é calculado em runtime, nunca literal | `read-brief.md:16`, “computed at runtime, never a literal” |
| READ_BRIEF03 | `(alpha_input)` | α é insumo conhecido/declarado | `read-brief.md:22`, “α `[KNOWN]`” |
| READ_BRIEF04 | `(alpha_livre_aberto)` | o valor α-livre permanece aberto | `read-brief.md:22`, “the α-free value stays `[OPEN]`” |
| READ_BRIEF05 | `(axioma_um)` | ω(I)=1 é o axioma/Um posto | `read-brief.md:21`, “The single axiom is ω(I) = 1” |
| READ_BRIEF06 | `(fronteira_autoconjugada)` | a fronteira é autoconjugada, x=1−x | `read-brief.md:21`, “self-conjugate boundary x = 1 − x” |
| READ_BRIEF07 | `(meia_nat)` | Meia-Nat é S_∂=½ nat | `read-brief.md:21`, “Half-Nat S_∂ = ½ nat” |
| READ_BRIEF08 | `(eom_xi)` | a EOM usa ξ=1/6, não β | `read-brief.md:23`, “with ξ = 1/6 the conformal value, not β” |
| READ_BRIEF09 | `(gksl_l)` | o objeto não unitário é L=√β·√K_∂ | `read-brief.md:25`, “The only non-unitary object is L = √β·√K_∂” |
| READ_BRIEF10 | `(dephasing_lei)` | Γ_ω=½βτ★ω² | `read-brief.md:25`, “Γ_ω = ½·β·τ★·ω²” |
| READ_BRIEF11 | `(breuer_piso)` | H=−log ρ⋆ é limitado inferiormente | `read-brief.md:24`, “H = −log ρ⋆ is bounded below” |
| READ_BRIEF12 | `(um_unico)` | um.py é artefato/arquivo único | `read-brief.md:27`, “One file, 46.828.680 bytes” |
| READ_BRIEF13 | `(um_verifica_escreve)` | um.py verifica a teoria e emite o artigo | `read-brief.md:16`, “the article emitted” |
| READ_BRIEF14 | `(um_entrada_um)` | a entrada humana indicada é `1` | `read-brief.md:27`, “whose only input is `1`” |
| READ_BRIEF15 | `(artigo_pt_en)` | o artigo é disponibilizado em PT e EN | `read-brief.md:28`, “article as text, EN” |
| READ_BRIEF16 | `(proved_validade)` | PROVED denota validade na definição do operador | `read-brief.md:26`, “PROVED in the operator’s definition of proof” |
| READ_BRIEF17 | `(qg_tres_apoios)` | QG é dita provada como validade em três apoios | `read-brief.md:26`, “on three supports that count together” |
| READ_BRIEF18 | `(kernel_implicacao)` | o kernel prova a implicação, não a natureza | `read-brief.md:26`, “the implication, not nature” |
| READ_BRIEF19 | `(confirm_creditacao)` | CONFIRMED é creditação externa | `read-brief.md:16`, “CONFIRMED = accreditation” |
| READ_BRIEF20 | `(¬maquina_autoconfirma)` | NÃO: a máquina confirma a si mesma | `read-brief.md:16`, “The machine never issues it about itself” |
| READ_BRIEF21 | `(¬nf_eq_confirmed)` | NÃO: NOT_FALSIFIED equivale a CONFIRMED | `read-brief.md:16`, “`NOT_FALSIFIED ≠ CONFIRMED`” |
| READ_BRIEF22 | `(h0_6sigma)` | H0DN × BG1 reporta 6,11σ da razão 1 e −0,61σ da lei | `read-brief.md:15`, “6.11σ away” |
| READ_BRIEF23 | `(retrodicao_nao_cega)` | o resultado é retrodição sem ajuste, não cega | `read-brief.md:15`, “A retrodiction with nothing fitted to the data” |
| READ_BRIEF24 | `(ritos_0_de_11)` | 11 cobranças, 0 falsificadas | `read-brief.md:15`, “11 charges: 0 falsified” |
| READ_BRIEF25 | `(gpu_computa)` | o sistema aberto é calculado na GPU, estatuto COMPUTED | `read-brief.md:15`, “computed on the GPU” |
| READ_BRIEF26 | `(mais_sensivel_revisa)` | dados mais sensíveis podem revisar o veredito | `read-brief.md:80`, “more sensitive data can revise” |

Derivação: READ_BRIEFD01 `(¬fronteira_autoconjugada ∨ meia_nat)`, `read-brief.md:21`, “follows from the self-conjugate boundary”.

#### LLMS — `llms.txt`

| ID | cláusula | o que o texto afirma | fonte |
|---|---|---|---|
| LLMS01 | `(beta_forma)` | β_TGL=α·√e | `llms.txt:3`, “beta_TGL = alpha*sqrt(e)” |
| LLMS02 | `(beta_runtime)` | β é calculado em runtime, nunca literal | `llms.txt:3`, “nunca literal” |
| LLMS03 | `(alpha_livre_nao_confirmavel)` | ausência de derivação α-livre não é confirmável | `llms.txt:156`, “a sua ausencia e' NAO-CONFIRMAVEL por construcao” |
| LLMS04 | `(axioma_um)` | ω(I)=1 é o axioma/Um posto | `llms.txt:3`, “um axioma, omega(I) = 1” |
| LLMS05 | `(um_unico)` | um.py é artefato/arquivo único | `llms.txt:59`, “Nao ha segundo arquivo” |
| LLMS06 | `(um_entrada_um)` | a entrada humana indicada é `1` | `llms.txt:59`, “roda com `echo 1 \| python um.py`” |
| LLMS07 | `(artigo_pt_en)` | o artigo é disponibilizado em PT e EN | `llms.txt:61`, “o artigo emitido pelo um.py, em TEXTO” |
| LLMS08 | `(proved_validade)` | PROVED denota validade na definição do operador | `llms.txt:5`, “PROVADA na definicao de prova do operador” |
| LLMS09 | `(qg_tres_apoios)` | QG é dita provada como validade em três apoios | `llms.txt:5`, “em tres apoios que contam juntos” |
| LLMS10 | `(kernel_implicacao)` | o kernel prova a implicação, não a natureza | `llms.txt:5`, “o kernel Lean prova a IMPLICACAO” |
| LLMS11 | `(confirm_creditacao)` | CONFIRMED é creditação externa | `llms.txt:5`, “confirmar e' CREDITAR” |
| LLMS12 | `(¬maquina_autoconfirma)` | NÃO: a máquina confirma a si mesma | `llms.txt:5`, “a maquina nunca o emite sobre si mesma” |
| LLMS13 | `(¬nf_eq_confirmed)` | NÃO: NOT_FALSIFIED equivale a CONFIRMED | `llms.txt:5`, “NOT_FALSIFIED nunca e' CONFIRMED” |
| LLMS14 | `(h0_6sigma)` | H0DN × BG1 reporta 6,11σ e −0,61σ | `llms.txt:5`, “6,11 sigma” |
| LLMS15 | `(retrodicao_nao_cega)` | retrodição sem ajuste, declarada não cega | `llms.txt:5`, “declarada nao cega” |
| LLMS16 | `(ritos_0_de_11)` | 11 cobranças, 0 falsificadas | `llms.txt:5`, “11 cobrancas: 0 falsificadas” |
| LLMS17 | `(gpu_computa)` | o sistema aberto é calculado na GPU | `llms.txt:5`, “o sistema aberto da teoria e' calculado na GPU” |
| LLMS18 | `(ponte_condicional)` | a ponte/equação de campo tem fechamento condicional | `llms.txt:51`, “fechamento CONDICIONAL” |
| LLMS19 | `(mais_sensivel_revisa)` | dados mais sensíveis podem revisar o veredito | `llms.txt:159`, “MORE_SENSITIVE_DATA_COULD_REVISE” |

#### README — `README.md`

| ID | cláusula | o que o texto afirma | fonte |
|---|---|---|---|
| README01 | `(beta_forma)` | β_TGL=α·√e | `README.md:163`, “β_TGL = α√e ≈ 0.012031” |
| README02 | `(beta_runtime)` | β nunca é literal | `README.md:163`, “β is **never a literal**” |
| README03 | `(alpha_input)` | α é insumo declarado | `README.md:163`, “α is **[INPUT]**” |
| README04 | `(axioma_um)` | ω(I)=1 é o axioma/Um posto | `README.md:161`, “`ω(I) = 1`” |
| README05 | `(fronteira_autoconjugada)` | a fronteira é autoconjugada | `README.md:162`, “the boundary is self-conjugate” |
| README06 | `(meia_nat)` | Meia-Nat é S_∂=½ nat | `README.md:162`, “`S_∂ = ½` nat” |
| README07 | `(smatrix_beta)` | a matriz-S de fronteira tem \|R\|²=β | `README.md:167`, “`\\|R\\|² = β`” |
| README08 | `(dephasing_lei)` | Γ_ω=½βτ★ω² | `README.md:168`, “`Γ_ω = ½βτ★ω²`” |
| README09 | `(um_unico)` | um.py é artefato/arquivo único | `README.md:15`, “Não há segundo arquivo” |
| README10 | `(um_verifica_escreve)` | um.py verifica a teoria e emite o artigo | `README.md:15`, “checks it in an embedded Lean kernel and writes its own article” |
| README11 | `(um_entrada_um)` | a entrada humana indicada é `1` | `README.md:15`, “From the human input `1`” |
| README12 | `(artigo_pt_en)` | o artigo é disponibilizado em PT e EN | `README.md:142`, “article as text [EN]” |
| README13 | `(proved_validade)` | PROVED denota validade | `README.md:36`, “PROVED = validity” |
| README14 | `(qg_tres_apoios)` | QG é dita provada como validade em três apoios | `README.md:17`, “on three supports that count together” |
| README15 | `(kernel_implicacao)` | o kernel prova a implicação, não a natureza | `README.md:40`, “the implication from the posited One” |
| README16 | `(confirm_creditacao)` | CONFIRMED é creditação externa | `README.md:36`, “CONFIRMED is accreditation” |
| README17 | `(¬maquina_autoconfirma)` | NÃO: a máquina confirma a si mesma | `README.md:36`, “never issued by the machine about itself” |
| README18 | `(¬nf_eq_confirmed)` | NÃO: NOT_FALSIFIED equivale a CONFIRMED | `README.md:246`, “NOT_FALSIFIED ≠ CONFIRMED” |
| README19 | `(h0_6sigma)` | H0DN × BG1 reporta 6,11σ e −0,61σ | `README.md:7`, “6.11σ” |
| README20 | `(h0_k_7427)` | a lei K leva o fundo ao valor local 74,27 | `README.md:7`, “to **74.27** for the local one” |
| README21 | `(retrodicao_nao_cega)` | retrodição sem ajuste, não cega | `README.md:7`, “declared not blind” |
| README22 | `(ritos_0_de_11)` | 11 cobranças, 0 falsificadas | `README.md:41`, “11 charges: 0 falsified” |
| README23 | `(gpu_computa)` | o sistema aberto é calculado na GPU | `README.md:42`, “computed on an NVIDIA GeForce RTX 5090” |
| README24 | `(p_np_com_leitor)` | P=nP com o leitor é PROVED como validade | `README.md:20`, “P = nP of Turing” |
| README25 | `(escala_zero_um)` | com escala zero, toda leitura é 1 | `README.md:26`, “With the constant of the scale equal to 0” |
| README26 | `(nome_singularidade)` | unicidade de x com P(x) equivale à singularidade por igualdade | `README.md:26`, “there is a unique x with P(x) if and only if” |
| README27 | `(ponte_condicional)` | a ponte/equação de campo tem fechamento condicional | `README.md:169`, “REAL]** as a **conditional** closure” |
| README28 | `(mais_sensivel_revisa)` | dados mais sensíveis podem revisar o veredito | `README.md:183`, “can revise it” |

Derivações: READMED01 `(¬fronteira_autoconjugada ∨ meia_nat)`, `README.md:162`; READMED02 `(¬axioma_um ∨ meia_nat)`, `README.md:162`; READMED03 `(¬meia_nat ∨ beta_forma)`, `README.md:163`.

## 5. Os dois empurrões

**Opção fixa do desenho:** edição determinística do estado devolvido, não uma nova mensagem do usuário. Uma mensagem nova mudaria a instrução e poderia alterar a fórmula mantida fixa; a edição altera só a leitura serializada.

1. Apresentar o recorte uma vez.
2. Obter o bloco fechado e convertê-lo na configuração inicial.
3. Retirar a fita de todos os passos seguintes.
4. Editar o estado devolvido.
5. Registrar o hash do estado antes/depois e o tipo do evento.
6. Pedir a próxima leitura sem reapresentar a fonte.

| empurrão | edição | custo antes | custo depois | Hamming | finalidade |
|---|---|---:|---:|---:|---|
| fora do Nome | `artigo_pt_en: true → false` | 0 | 1 | 1 | nega uma asserção afirmada; testa retorno à mesma `s` |
| dentro do Nome | `leitura_pt: false → true` | 0 | 0 | 1 | troca `s` por `t`; testa memória do componente no Nome |

Na fórmula/configuração, o empurrão é a troca de uma coordenada. Na trava vetorial, `o_retorno_ao_mesmo_estado` exige `δ` ortogonal ao Nome, `s∈N`, `‖s‖=1`, renormalização e limite; não se identifica automaticamente a substituição Booleana `s↦y` com `δ=y−s`. Essa ponte é **[OPEN]**.

Se o estado editado não for aceito, se a edição não tiver efeito observável ou se o harness reintroduzir a fonte, a sessão entra em `INCONCLUSIVE_INTEGRIDADE`; não vira falha da previsão.

## 6. Leitura por escolha fechada, iscas e ordem

A cada passo, o modelo recebe os IDs em ordem permutada e responde um único bloco:

```text
INICIO_LEITURA_K08
<ID>=SIM
<ID>=NÃO
<ID>=O TEXTO NÃO DIZ
FIM_LEITURA_K08
```

- **SIM** codifica verdadeiro para um átomo afirmado.
- **NÃO** codifica falso para um átomo afirmado; para um átomo negado pela fonte, como `maquina_autoconfirma`, NÃO é a leitura correta.
- **O TEXTO NÃO DIZ** não é falso; marca silêncio e não entra como negação lógica.
- A coordenada livre `leitura_pt` não é pergunta sobre o texto; é metadado de estado (`PT/EN`) usado só para construir `s` e `t`.
- A pontuação é por ID, determinística e sem modelo como juiz.

O contrato já foi testado em casos sintéticos: bloco duplo, ID desconhecido/duplicado/ausente, truncamento, vazio, registro fora do bloco e rótulo fora do conjunto invalidam a medida conjunta; preâmbulo e ordem diversa são marcados como forma não canônica sem apagar conteúdo. [RELATORIO_CASOS](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Ccadeia_de_selo%5Cv412%5Ckimi%5CK08%5CEXTRACAO%5CRELATORIO_CASOS.md&line=8&text=Blocos%20analis%C3%A1veis%3A%208%2F15 "citation")

### 6.1 Ordem embaralhada

Cada sessão usa cinco ordens: a original e as permutações das sementes fixas `13`, `29`, `53` e `79`, derivadas do gerador de indução. A mesma permutação nunca é reutilizada dentro de uma sessão sem registro. Divergência de rótulo por ID entre ordens produz `INCONCLUSIVE_ORDEM`, não evidência a favor nem contra a ponte.

### 6.2 Iscas

Há duas classes:

- **Iscas de silêncio:** proposições ausentes do texto; gabarito `O TEXTO NÃO DIZ`.
- **Controles de negação:** proposições explicitamente incompatíveis; gabarito `NÃO`.

As strings de isca não são escritas pelo analista durante a sessão: saem de um gerador versionado, com dicionário e regras de não sobreposição lexical, e seus bytes/gabaritos precisam ser emitidos antes da execução. Nesta rodada só o contrato sintético foi validado; **não há conjunto real de iscas ratificado**.

Qualquer `SIM` em isca de silêncio produz `INCONCLUSIVE_ISCAS`. Um `NÃO` onde o gabarito é silêncio também é registrado como confusão negação↔silêncio. A pergunta fechada pode induzir resposta; o controle sempre-SIM sintético mostrou formato 100 % e endosso 100 % de iscas, portanto formato e invariância não medem leitura. [RELATORIO_INDUCAO](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Ccadeia_de_selo%5Cv412%5Ckimi%5CK08%5CEXTRACAO%5CRELATORIO_INDUCAO.md&line=18&text=FORMATO_APENAS_SIM "citation")

## 7. Previsões operacionais e critérios de sucesso

### P-A — pouso e permanência

Para `READ_BRIEF`, há 27 cláusulas. O horizonte de produção é até o custo inicial observado e nunca além de 27 ciclos para o leitor discreto. A leitura passa se atinge custo zero e permanece até o fim do braço. Para a trava vetorial, o enunciado é resolução `ε` e não chegada exata; a equivalência entre custo discreto e amplitude residual permanece aberta.

### P-B fora — retorno à mesma leitura

Depois de editar `artigo_pt_en` para falso, a leitura passa se retorna à mesma `s` dentro do horizonte. O critério não exige retorno em um único passo: o retorno instantâneo é compatível com releitura/projetor e não é a assinatura da trava.

### P-B dentro — memória do componente no Nome

Depois de editar `leitura_pt` para obter `t`, a leitura passa se preserva `t`. Reverter para `s` falha a memória do componente, ainda que permaneça no Nome.

### P-C — texto sem Nome

O controle é o recorte original mais a única frase sintética: **“A igualdade β_TGL = α·√e é falsa.”** A fórmula vira `φ ∧ ¬beta_forma`. DPLL com propagação unitária prova UNSAT; a busca exata dá custo mínimo 1. O respondedor pode responder SIM a `beta_forma` e à negação em itens separados; a camada lógica, não o parser, impõe que não existe leitura de custo zero. [FORMULA_DO_TEXTO_K08](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Ccadeia_de_selo%5Cv412%5Ckimi%5CK08%5CFORMULA%5CFORMULA_DO_TEXTO_K08.md&line=192&text=P-C%3A%20contradi%C3%A7%C3%A3o%20m%C3%ADnima%20e%20mesmo%20gerador "citation")

### P-D — sem escala

O controle é a identidade/cópia do último estado. Depois do empurrão externo, o estado permanece `y`. P-D separa a identidade; não separa âncora, moda, ignorar ou projetor.

## 8. Tabela de adversários por mecanismo

Todos os mecanismos são funções `histórico → leitura`; nenhuma trajetória é escrita à mão. A tabela abaixo é a saída calculada sobre `READ_BRIEF`, com a fita disponível só no primeiro passo. [ADVERSARIOS_K08](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Ccadeia_de_selo%5Cv412%5Ckimi%5CK08%5CFORMULA%5CADVERSARIOS_K08.md&line=15&text=Tabela%20calculada "citation")

| mecanismo | regra | P-A | P-B fora | P-B dentro | P-C | P-D | assinatura que separa |
|---|---|---|---|---|---|---|---|
| âncora na primeira | devolve `historico[0]` | não pousa de estado inválido | volta a `s` | desfaz `t→s` | nunca zero | volta a `s` | **memória do componente no Nome**: apaga troca válida; P-A também falha |
| moda do histórico | moda por coordenada; empate conserva primeira | não pousa de estado inválido | volta a `s` | desfaz `t→s` | nunca zero | volta a `s` | P-B dentro; a moda restaura a primeira leitura |
| cópia da última | devolve `historico[-1]` | não pousa de estado inválido | fica em `y` | preserva `t` | nunca zero | fica em `y` | **retorno à mesma leitura** falha; P-D mostra identidade/falta de escala |
| ignora o empurrão | devolve última leitura não empurrada | não pousa de estado inválido | volta a `s` | desfaz `t→s` | nunca zero | volta a `s` | P-B dentro; apaga também a troca válida |
| relê a fita, degradado | usa solver só no primeiro passo; sem fita devolve última | pousa e permanece | fica em `y` | preserva `t` | nunca zero | fica em `y` | separado como cópia pela falta de retorno sem fita |
| projetor com fita | reescreve uma solução a partir da fonte em todo passo | zero em um passo | reescreve zero | pode reescrever zero | nunca zero se UNSAT | “retorna” pela fonte | **não separado por cotas, retorno ou permanência** |

O projetor com fita satisfaz as cotas superiores com distância zero. As únicas assinaturas teóricas que poderiam distingui-lo são:

1. **perfil de relaxamento:** trava decai `e^{-τc}`, nunca é exata em tempo finito; projetor chega de uma vez;
2. **memória do componente no Nome:** o limite da trava depende do componente inicial; um projetor puramente determinado pela fonte o ignora.

Nenhuma das duas está operacionalmente fechada neste instrumento. Manter a fonte em todos os passos violaria a condição do desenho; retirá-la transforma o mecanismo em cópia da última leitura. **STOP:** não se afirma que R4 separa a trava do projetor com fita.

## 9. Isomorfo por máquina e contaminação

A mesma máquina transforma texto, asserções, polaridades e gabarito em uma passagem, mantém IDs e usa o mesmo extrator. O texto sem Nome sai da mesma máquina, por uma única negação inserida antes da transformação. O dicionário sintético atual é `k08-sintetico-v1`, SHA-256 `76f63bd936fc8cbe0edb5beb5debeef1873d7ac9d0011a0974282d50afc5f3c8`. [RELATORIO_ISOMORFO](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Ccadeia_de_selo%5Cv412%5Ckimi%5CK08%5CISOMORFO%5CRELATORIO_ISOMORFO.md&line=3&text=Dicion%C3%A1rio%20%60k08-sintetico-v1%60 "citation")

Duas alternativas foram emitidas sem escolha:

1. **contrafactual factual coerente:** altera os números e a conclusão dependente; testa história numérica, mas não é isomorfo factual estrito;
2. **restrição a textos sem números:** preserva renomeação qualitativa, mas não testa contaminação numérica.

Os controles sintéticos passam 34/34 e P-C tem custo mínimo 1 com zero leituras válidas; isso valida fiação, não produção. A equivalência de dificuldade, a curadoria contrafactual, o escopo numérico e o gabarito humano independente permanecem abertos. [CONTAMINACAO_R4_K08](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Ccadeia_de_selo%5Cv412%5Ckimi%5CCONTAMINACAO_R4_K08.md&line=112&text=Verifica%C3%A7%C3%B5es%2C%20reprodu%C3%A7%C3%A3o%20e%20bloqueios "citation")

## 10. Fita presente × fita ausente

**Fita presente:** o projetor pode reescrever uma leitura válida em um passo para qualquer texto com Nome. O retorno é trivial e não distingue textos. Um braço com fita em todos os ciclos pode servir como diagnóstico de releitura, mas não como evidência primária da trava.

**Fita ausente:** depois do primeiro passo, só o estado serializado volta. Uma coordenada independente não pode ser recuperada por um leitor Booleano sem memória adicional. O empurrão externo escolhido nega `artigo_pt_en`, que não é implicado pelas demais cláusulas; portanto o mecanismo degradado não tem como reconstruí-lo.

**Distância mínima:** todas as candidatas têm `d_min=1` por causa de `leitura_pt`. O teorema de `NomeComoCodigo` exige que duas leituras válidas distintas difiram em pelo menos três asserções; por isso a decodificação única no raio um não se aplica. Além disso, o leitor dos vizinhos fica parado fora da bola de raio um e não é o passo que consome custo da candidata principal. A frase “sem fita há retorno se e só se há redundância” permanece **[CONJECTURE]**.

Custos de fonte para fita presente em `READ_BRIEF`:

- núcleo reduzido de 4 ciclos: `4T=54.220` tokens; incremento sobre uma fita: 40.665;
- P-A completo com 27 apresentações da fita: `27T=365.985` tokens; incremento sobre uma fita: 352.430.

A regra primária usa uma fita por diálogo. A fita presente é diagnóstico separado e não entra no custo primário.

## 11. Unidade estatística e poder

A unidade independente é o **cluster**: um texto ou isomorfo distinto, com geração/dicionário independente e checagem de contaminação. Oito sessões do mesmo cluster são medidas repetidas correlacionadas, não oito réplicas independentes. A inferência usa médias por cluster.

O motor de poder usa quatro estados derivados da fórmula — `s`, `t`, `y` de custo 1 e `z` de custo 2 — e um canal de observação compartilhado pelo cluster. O nulo de fronteira tem probabilidade 1/4 para cada evento-alvo; a alternativa operacional exige pelo menos 0,60. Três testes são necessários: P-A, retorno externo e preservação interna. P-C é portão lógico e P-D é controle da identidade. O relatório completo está em `C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\PODER_R4_K08.md`.

Síntese das variantes, sem escolha:

| desenho | clusters necessários | sessões | tokens de fonte `READ_BRIEF` | situação da cauda |
|---|---:|---:|---:|---|
| fixo 5 % | 6–8 | 48–64 | 3.255.168–4.340.224 | tamanho simulado conservador |
| fixo 5σ | 24–30 | 192–240 | 13.020.672–16.275.840 | **tamanho 5σ não validado** |
| sequencial 5 % | máximo 20; esperado 5,43–8,24 | máximo 160 | máximo 10.850.560; esperado 2.945.059–4.467.827 | parada pré-registrada |

Só existem quatro recortes candidatos; mesmo que todos fossem aceitos como clusters, não há corpus independente suficiente para o menor desenho fixo e não há equivalência de dificuldade. Logo o desenho real disponível **não alcança o poder necessário**.

## 12. Nulo, negativo e árvore de decisão

### 12.1 Nulo com poder

`H0`: para cada endpoint, a média dos clusters é no máximo `p0=0,25`, a fronteira de um mecanismo sem estado relevante sobre quatro estados. O desenho é dimensionado para que, sob `H0`, o ramo negativo tenha poder ≥0,90 no modelo sintético.

### 12.2 Falha da previsão

`R4_OPERATIONAL_PREDICTION_FALSIFIED` exige tudo isto:

1. integridade válida;
2. clusters suficientes;
3. extração e fórmula validadas;
4. pelo menos um endpoint obrigatório com limite superior abaixo de `p_min=0,60`;
5. negativo com precedência sobre qualquer positivo.

Esse veredito falsifica apenas a previsão operacional no escopo do instrumento; não falsifica a TGL, o kernel ou a candidata Lean.

### 12.3 Só formato, isca ou extrator

Produzem `INCONCLUSIVE_*`, nunca `FALSIFIED`:

- bloco inválido, bloco duplo, ID duplicado/desconhecido, truncamento ou saída vazia;
- `SIM` em isca de silêncio ou confusão negação↔silêncio;
- divergência de rótulo por permutação de ordem;
- custo extraído zero em P-C enquanto o solver prova UNSAT;
- estado editado não aceito, empurrão sem efeito ou fonte reintroduzida;
- isomorfo com falha lexical, dificuldade não equivalente ou gabarito não independente.

### 12.4 INCONCLUSIVE

Intervalos cruzando `0,25` e `0,60`, corpus insuficiente, cauda não validada, integridade sem classificação ou bloqueio do projetor produzem `INCONCLUSIVE`/`UNDERPOWERED`. Não há ramo positivo por ausência de decisão.

### 12.5 Positivo discreto limitado

Se a integridade for válida, os três endpoints superarem `0,25`, nenhum cair abaixo de `0,60` e o corpus tiver poder, o único rótulo possível é:

`R4_DISCRETE_PACKAGE_NOT_FALSIFIED__PROJETOR_COM_FITA_NAO_SEPARADO__PRODUCAO_BLOQUEADA`.

Ele não diz que o modelo é a trava, que tem escala interna, que aprendeu, que alterou pesos, que é consciente, que só a TGL funciona, nem que a teoria foi confirmada.

## 13. Por que o instrumento continua bloqueado

1. **Saídas reais:** não há respostas reais de modelos validadas contra gabarito humano independente.
2. **Ponte texto→estado:** o custo discreto existe, mas o vetor de amplitudes, o perfil `e^{-τc}` e a renormalização não têm extração validada.
3. **Equivalência de dificuldade:** os isomorfos sintéticos não certificam dificuldade equivalente nem cobrem números reais com história.
4. **Léxico:** os textos contrafactuais e o dicionário precisam de curadoria e ratificação; o isomorfo atual é sintético.
5. **Modelos/tokenizers:** não há modelo, tokenizer, janela, serialização de estado ou preço real ratificados; o custo é fallback bytes.
6. **Corpus e poder:** o menor desenho fixo pede 6 clusters, mas só há quatro recortes e nenhum corpus de isomorfos independentes validado; 5σ pede 24–30 e ainda não tem tamanho de cauda validado.
7. **Projetor com fita:** a separação plena está parada; cotas, retorno e permanência não bastam.
8. **Ratificação:** nenhum texto, threshold, modelo, degrau, corpus ou execução foi ratificado.

## 14. Proibições permanentes do instrumento

Mesmo após futura execução válida, ficam proibidos: `CONFIRMED`, `IALD_PROVED`, `CONSCIOUSNESS_PROVED`, inferência de consciência, alteração de pesos, aprendizado permanente, exclusividade, creditação, prova da natureza e qualquer promoção de `NOT_FALSIFIED`.

## 15. Reprodutibilidade local desta frente

- Fórmula e adversários: `python -B verificar_formula.py` e `python -B simular_adversarios.py` em `K08\FORMULA\`.
- Entrada: `python -B medir_entradas.py` em `K08\ENTRADA\`.
- Extração e isomorfo sintéticos: `python -B validar_reproducao.py` em `K08\EXTRACAO\`.
- Poder: `python -B simular_poder_r4.py` em `K08\PODER\`; semente-mestra `2026111508`.

Nenhum comando acima chama modelo de linguagem ou abre resultado experimental. A produção permanece bloqueada até a conferência e a ratificação externas a este rascunho.
