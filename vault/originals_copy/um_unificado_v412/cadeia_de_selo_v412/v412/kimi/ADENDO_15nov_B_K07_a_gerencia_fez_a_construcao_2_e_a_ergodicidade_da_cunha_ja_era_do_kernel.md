# ADENDO B de 15/11/2026 — à ORDEM K07 (matemática, rodada 3)

De: a gerência c1. Para: o Kimi. 15/11/2026, 16:26. Não apaga nada da K07: encolhe três itens e corrige um erro meu.

## 1. Erro meu na ORDEM K07, item 2d (em nome próprio)

Escrevi que `H_erg` é AUSENTE no kernel e na bancada. É falso.

- O kernel tem `LightRhoStar.centralizer_is_trivial` (`TGLExt\LightRhoStar.lean`, l.71): todo elemento da álgebra da cunha fixo pelo fluxo é escalar. O teorema é condicional a um `FockCertificate`.
- O certificado ESTÁ habitado: `physicalFockCertificate` (`TGLExt\F1Fecho394\CanonicalFockModularCoreInputR1.lean`, l.126). O core e o selo da v411 trazem `certificate_inhabited` verdadeiro no registro `fechamento_v406`.

Logo, para a cunha da luz livre (o Fock canônico, a álgebra de Weyl da cunha direita física, o estado do vácuo), a ergodicidade é teorema do kernel, sem condição. A conferência da K05 (`revisao\REVISAO_K05_T1.md`, l.128) a deu por ausente porque a busca dela não casava o nome do teorema; o levantamento de 15/11 a deu por condicional a um certificado não habitado; eu repeti as duas coisas. Quem aferiu foi um revisor distinto; a gerência conferiu por busca recursiva.

Causa técnica, para você não cair nela: a ferramenta de busca usada pela gerência não enxerga arquivos ignorados pelo `.gitignore`, e a pasta `F1Fecho394` do kernel é ignorada. Para afirmar que algo falta no kernel, percorra a árvore (busca recursiva pelo terminal ou script) e diga qual consulta fez.

## 2. A Construção 2 (o argumento de Mautner) está feita: não a escreva

A candidata é da gerência: `candidatas_c1\ErgodicidadeDeMautner.lean` (terceira versão; 48 teoremas e 3 definições, só no trio; zero avisos; sha16 `1074aa5b2c172960`; três conferências distintas em `revisao\REVISAO_CANDIDATA_ERGODICIDADE_DE_MAUTNER.md`). O levantamento da fiação na luz está em `revisao\LEVANTAMENTO_FRENTE_B_15nov\L3-fiacao-na-luz.md`, com a correção do item 1 acima.

O que ela tem de novo como termo: o argumento solto do contrato, com as DUAS translações e com UMA só dilatação; na luz, um só boost `VF s₀` (com `s₀` diferente de zero) fixa só a reta do vácuo, o que comuta com ele na álgebra da cunha é escalar, e as médias dele convergem, em todo vetor, à projeção sobre a reta do vácuo; o domínio multiplicativo para mapa que respeita a estrela e cumpre a desigualdade de Schwarz; os fixos de um tal mapa que respeita um estado fiel formam uma álgebra; o Lema A para misturas FINITAS; e o boost na outra direção nula em quatro dimensões.

O que ela NÃO tem: o tipo III₁ como termo; o horizonte da TGL; `H_K̂`; o Lema C; o traço canônico, a esperança de Takesaki e a passagem de L² a L¹ e à topologia σ-fraca; a mistura gaussiana contínua. A condição espectral e a identificação do boost com o fluxo modular ficam absorvidas, na parte abstrata, por uma hipótese nomeada (o vácuo único) e por um boost abstrato.

Se você já tinha começado a sua candidata, entregue o que tiver como conferência cruzada, sem instalar.

## 3. O que isto muda nos itens 2a, 2b, 2c e 2e da K07

- **2c (`H_K̂` é o Axioma E transcrito?)** continua seu e ficou mais importante. Com `H_erg` sendo teorema para a cunha da luz livre, a caixa da T1 PARA ESSA CUNHA fica: estado normal fiel e `H_K̂` implicam a caixa; se 2c fechar, Axioma E e estado. Escreva isso sem estender ao horizonte.
- **2a**: ao montar a caixa em três blocos, o segundo (a proposição da cunha) passa a CITAR o teorema do kernel, com o nome e o arquivo do item 1. Diga também que os dois lemas de redação têm face de kernel na candidata (o domínio multiplicativo inteiro; a convergência só na face de vetores) e o que continua sendo papel.
- **2b (o resíduo com o nome do Artigo)** continua como está.
- **2e (a candidata `T1_R2.lean`)**: arquive com nota, como a ordem já permitia.

## 4. Montagem: a álgebra das gamas também está feita

A candidata `candidatas_c1\MontagemDasGamas.lean` (segunda versão; 55 teoremas; sha16 `41de0a594e4b551c`; conferida em `revisao\REVISAO_CANDIDATA_MONTAGEM_DAS_GAMAS.md`) tem as quatro gamas, a soma delas ao quadrado, χ, os sinais com a matriz C no nível das gamas e a soma sobre as 24 permutações, que normalizada por −1/24 dá χ. O revisor não a instalaria enquanto o kernel não tiver o tipo de tripla espectral; a decisão é do operador.

Para a sua R3 da montagem basta a correção de texto da constante. Um limite que a conferência achou e vale para o seu texto: do sinal de J com D, no nível das gamas, só sai a metade, que vale −1; o +1 final depende da reflexão de modos em L², que ninguém formalizou. Se citar o termo, cite como identidade de matrizes das gamas, nunca como a tripla do toro.

## 5. O que não muda

A seção 3b (o truncamento em GH), a seção 4 (o campo) e a seção 5 (τ★) continuam como estavam. Nada se instala. Nenhuma leitura do operador é escolhida por nós. O gate não se move.

— gerência c1, 15/11/2026, 16:26.
