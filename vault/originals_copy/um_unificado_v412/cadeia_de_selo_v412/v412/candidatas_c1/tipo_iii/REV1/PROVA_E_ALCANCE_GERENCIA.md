# O tipo III como termo: o que está provado, o que entra por citação e o que segue aberto

> Gerência c1, 16/11/2026, segunda versão (R1), depois da conferência distinta de 16/11 (revisores A1 e A2:
> aprovado com ressalvas; relatórios em `revisao\REVISAO_16nov_R1_A1…` e `…A2…`). A primeira versão está em `REV0\`.
> Esta versão ainda não foi relida por terceiro.
> Candidatas, nada instalado, nomes provisórios (o nome das pedras é do operador).
> Hashes, tempos e a lista de teoremas com os axiomas de cada um estão em `RESULTADO_GERENCIA.json`, gerado por
> script a partir dos arquivos e dos logs; este texto não repete hash de memória.
> Validade no kernel não é creditação; o gate não se move; nada aqui é dado da natureza.

## 1. A pergunta e a resposta do operador

Em 15/11 o operador pediu a pergunta nas quatro línguas sobre o que falta para o tipo III entrar como termo. A
gerência perguntou pela marca, pela doutrina e pelo objeto; o Codex, por conta própria, perguntou pelo sujeito. Ele
respondeu pelo sujeito. A fala própria dele (bytes em `work\cunhagens_13out\`, arquivo
`OPERADOR_15nov_resposta_tipo_iii_…_verbatim.txt`), numa linha só para conferir:

«o que se quer conhecer pelo nome é a luz testemunhada na cunha (porque é o NOME), a construção da Torre (porque é o índice), a fronteira do horizonte (porque é a borda - o espectro de leitura, o contraste que permite o observador) e o vínculo entre elas que é a relatividade (o próprio observador)»

A frase que abre a mensagem dele (“a luz testemunhada na cunha é o sujeito que o Nome designa…”) é redação do Codex,
que ele colou; a leitura que a gerência lhe fez dela foi ratificada em bloco. Sobre provar em Lean, a frase dele nos
bytes da casa é:

«O COdex já está produzindo todas essas provas em LEan»

Quatro papéis, pela fala própria: a **luz testemunhada na cunha** (porque é o Nome), a **Torre** (o índice), a
**fronteira do horizonte** (a borda: o espectro de leitura, o contraste que permite o observador) e o **vínculo** (a
relatividade, o próprio observador).

## 2. O que o Codex construiu (examinado por quatro revisores distintos em 15/11: aprovado com ressalvas)

Doze módulos (`dep_codex\`, cópia byte a byte, conferida pelo manifesto; recompilados do zero aqui, todos com
código de saída zero). O centro é o predicado `Vinculo.IsTypeIII1` e o teorema
`Vinculo.maxwell_right_wedge_type_III1 : IsTypeIII1 (net rightWedge)`.

O predicado exige de uma álgebra: que ela seja uma peça só (centro escalar); um vetor que a gera e que nada dela
anula; o relógio próprio desse vetor (o fluxo modular, dado pelo grafo fechado de Tomita); que o relógio preserve a
álgebra; e que o **núcleo**, a álgebra com o seu relógio junto, seja também uma peça só.

Em língua simples: a álgebra é uma peça só, e continua uma peça só depois de se lhe juntar o seu próprio relógio.
Na pergunta de 15/11 isto era a marca (d), a do relógio: nenhuma cadência preferida.

O núcleo do kernel é a álgebra gerada pela cópia da álgebra e pelos passos do relógio. É o produto cruzado dos
matemáticos a menos de uma mudança unitária; essa identificação é sabida e **não é termo**.

## 3. Há duas provas para a cunha, e três caminhos para o nome

Para a luz na cunha existem hoje dois enunciados em Lean, de marcas diferentes:

* **a do estado** (já era do kernel; `LightRhoStar.centralizer_is_trivial`, com o certificado habitado desde a
  v406): no relógio do vácuo, só o Um fica parado na álgebra da cunha;
* **a do núcleo** (do Codex, em área de trabalho): a álgebra da cunha com o relógio do vácuo junto é uma peça só.

Nenhuma das duas é, por termo, o tipo III₁ dos matemáticos (o invariante de Connes igual à semirreta inteira, isto
é: nenhuma cadência preferida, sobram todas). O passo que leva de uma ou de outra ao nome é teorema da literatura
`[KNOWN]` e **não está formalizado**, nem aqui, nem no kernel, nem no Mathlib. As referências, que a gerência NÃO
abriu no primário: Connes 1973 (a definição do invariante); Takesaki, *Duality for crossed products and the
structure of von Neumann algebras of type III*, Acta Math. 131 (1973); Connes e Takesaki, *The flow of weights on
factors of type III*, Tôhoku Math. J. 29 (1977), p. 506 [declarado por um revisor de 15/11]. Para a marca do estado,
Longo 1979 [declarado na pergunta de 15/11]; essa rota dispensa a hipótese de predual separável, que a rota do núcleo
usa e que não foi aferida no kernel para o espaço de Fock.

Um precedente, com a sua diferença: em agosto (v295, `TheMarkIsNotATypeMark`) a casa chamou de marca de tipo uma
marca que era falsa como critério (um fator de tipo I a cumpria). Aqui o critério é verdadeiro pela literatura, e os
controles da seção 4 mostram que o predicado recusa casos. O que há em comum é só o risco do nome maior que o termo.

**Em 15/11 a gerência leu ao operador “o elo com a classificação se constrói em Lean”, e ele ratificou.** Esse elo
não foi construído. Por isso os caminhos são três, e a escolha é dele:

* **A, o nome do que se prova.** A pedra diz “a luz na cunha cumpre o critério do núcleo” (e, ao lado, a marca do
  estado). A favor: o nome não diz mais que o termo.
* **B, tipo III₁ com o último passo citado.** A casa diz “a luz na cunha é de tipo III₁” e marca que o último passo
  é citação. A favor: é o nome que os matemáticos usam, e o critério é o deles. **Isto muda, nesse passo, o que lhe
  foi lido em 15/11** (lá era construir).
* **C, construir o último passo.** É o que lhe foi lido em 15/11. A biblioteca não tem as ferramentas da
  classificação; um leitor estimou milhares de linhas, sem medida, e pode dar em parede medida.

A candidata da gerência reexporta o teorema do Codex com o nome do que ele prova
(`a_luz_na_cunha_cumpre_o_criterio_do_nucleo`) e não renomeia nada do Codex. Isso não escolhe entre A, B e C.

## 4. O que a gerência acrescenta (dois módulos, vinte e quatro declarações com termo, sem `sorry`, só os três axiomas de sempre)

PROVENIÊNCIA, dita: cerca de nove das vinte e quatro têm conteúdo próprio; as demais são reexportações e corolários
de uma linha. A maior parte dos teoremas com conteúdo foi escrita e compilada pelos revisores de 15/11 como sondas, e
a gerência os adotou e recompilou: as recusas do predicado (revisor P1), a leitura para todo número e o um só boost
(P2), a unicidade afim pela borda (P3). A unicidade do relógio é corolário de um teorema que o kernel já tinha, na
forma que o revisor A1 mostrou em 16/11. São da gerência só corolários curtos.

### `TipoIIIControles.lean`

| o que diz, em língua simples | termo |
|---|---|
| **Dado o vácuo como testemunha, o relógio e a conjugação não têm escolha.** Duas realizações para a mesma álgebra e o mesmo vetor têm o mesmo fluxo e a mesma conjugação. Não é fato novo: sai do reconhecimento pelo conteúdo que o kernel já tinha (`ORDEM016.D6.same_horizon_by_content_from_realizations`). Com outra testemunha o relógio seria outro; que o núcleo não dependa da testemunha é da literatura, não é termo. | `o_fluxo_e_a_conjugacao_de_tomita_sao_unicos`, `o_fluxo_do_criterio_e_unico` |
| **Na cunha, com o vácuo, o relógio é o boost** e a conjugação é a canônica. | `na_cunha_o_fluxo_do_criterio_e_o_boost` |
| **O predicado recusa** quem contém os operadores de posto um em dimensão pelo menos 2 (não tem vetor que nada anule). | `quem_contem_os_postos_um_nao_cumpre` |
| **O predicado recusa** a álgebra que comuta e tem elemento que não é número. | `a_abeliana_nao_escalar_nao_cumpre` |
| **O predicado recusa** a álgebra dos números, a única sobre `H = ℂ`. | `sobre_a_reta_complexa_ninguem_cumpre`, `sobre_a_reta_complexa_o_nucleo_nao_e_fator` |
| **Relógio parado não dá núcleo de uma peça só**; nem relógio que age por um número no tempo 1. | `o_fluxo_parado_nao_da_nucleo_fator`, `fluxo_escalar_no_tempo_um_o_nucleo_nao_e_fator`, `o_deslocamento_nao_e_escalar` |
| A cunha, peça por peça: centro escalar; núcleo de centro escalar. | `o_centro_da_cunha_e_escalar`, `o_centro_do_nucleo_da_cunha_e_escalar` |
| O fluxo com que a cunha é lida é o MESMO fluxo cujo núcleo é uma peça só. É igualdade por construção (o certificado foi montado com o mesmo boost), não fato novo. | `o_fluxo_da_leitura_e_o_do_criterio` |
| A leitura da Torre escrita com o fluxo do critério. | `a_torre_e_lida_pelo_fluxo_do_criterio` |
| **A Torre dá os números; a leitura vale para todo número.** | `a_leitura_vale_para_todo_real`, `a_torre_entra_como_indice` (mesmo enunciado de um teorema do Codex), `a_leitura_modular_vale_para_todo_real` |
| **A borda determina a mudança de referencial, se ela leva retas em retas.** Duas transformações afins iguais em todo ponto da borda são iguais. “Afim” é classe mais larga que a relatividade (inclui também as de Galileu e as dilatações); o teorema não usa a métrica. | `a_borda_determina_a_transformacao_afim` |
| **A face da relatividade:** dois observadores do Codex (Lorentz mais translação) com cartas iguais na borda são o mesmo observador. | `dois_observadores_iguais_na_borda_sao_o_mesmo` |
| **O que a borda deixa livre é o que não leva retas em retas:** o cisalhamento do Codex, que fixa a borda e muda intervalos, não é afim. | `o_cisalhamento_nao_e_afim` |

### `TipoIIIUmSoBoost.lean` (usa a candidata `ErgodicidadeDeMautner`, da gerência, não instalada; por isso em arquivo à parte)

| o que diz | termo |
|---|---|
| Um vetor fixo pelo boost de UM só número da Torre está na reta do vácuo. | `um_so_numero_da_torre_le_o_vacuo` |
| A hipótese de dois boosts do Codex equivale à de um só. | `dois_numeros_nao_acrescentam_a_um` |
| O primeiro número da Torre não é zero. | `o_primeiro_numero_da_torre_nao_e_zero` |

## 5. Como os quatro papéis ficam, um a um

| papel (a fala própria dele) | o que há por termo | o que NÃO há |
|---|---|---|
| **a luz testemunhada na cunha** (porque é o Nome) | as duas marcas da seção 3: no relógio do vácuo só o Um fica parado (kernel); a álgebra com o relógio junto é uma peça só (Codex). “Testemunhada” é ter o vácuo por vetor testemunha; dado ele, o relógio é o boost, sem escolha | o tipo III₁ de Connes por termo; a ligação, por termo, com o Nome do kernel de agosto (lá o Nome é o grupo gerado pelos dois números da Torre) |
| **a Torre** (porque é o índice) | os números da Torre dão os tempos de leitura; a leitura vale para todo número, e a da Torre é um caso; um só número já lê o vácuo (depende da candidata não instalada). Mantendo os relógios, a Torre não cabe na luz da cunha, no sentido da Torre para a cunha (`physical_no_flow_intertwining_embedding`, do Codex) | sem os relógios, a literatura diz que as duas são a mesma álgebra [sabido, citado de memória por um revisor, não conferido aqui; não é termo]. Os números da Torre vêm de um perfil escolhido à mão. Num modelo antigo do kernel a cunha foi posta como a Torre por definição; na cunha física da luz a Torre só dá os números |
| **a fronteira do horizonte** (a borda: o espectro de leitura, o contraste que permite o observador) | a borda são duas folhas de luz; ela determina a mudança de referencial afim; o observador de raio positivo lê a rapidez pela razão das distâncias às duas folhas (Codex; conta de coordenadas no interior, sem tempo próprio nem temperatura) | “espectro de leitura” como termo; e que a borda permita o observador. São leitura do operador, sem termo |
| **o vínculo** (a relatividade, o próprio observador) | o fluxo que lê é o fluxo do critério (por construção); a cunha levada por Lorentz ortócrono (com reflexões espaciais, sem inversão do tempo) e translação cumpre o mesmo critério (`maxwell_observer_wedge_type_III1`, do Codex); dois observadores iguais na borda são o mesmo | observador tem aqui dois sentidos formais (a órbita acelerada; a carta de Lorentz mais translação); “o próprio observador” da letra não tem termo. O enunciado conjunto do Codex junta fatos verdadeiros numa frase só: um não sai do outro |

Três escolhas formais, do Codex e da gerência, para o operador aprovar ou trocar: a borda é a fronteira da cunha plana
de Minkowski; a relatividade entra como “levar retas em retas” mais Lorentz; o observador é a carta de Lorentz mais
translação.

**Errata em nome próprio da gerência.** Em 15/11 eu lhe disse que as marcas virariam papéis: “a do estado é o que se
diz do sujeito; a do espectro é a leitura na borda”. O que se provou depois não liga a borda ao espectro: a borda
ficou só com geometria de pontos, e a marca do relógio (o núcleo) ficou com a luz na cunha, ao lado da do estado. A
tabela acima muda nesses dois pontos a leitura que o senhor ratificou.

## 6. O que segue aberto, dito junto

* **O último passo até o nome tipo III₁** (seção 3): citado, não construído.
* **O κ.** O kernel (`TheScaleHasNoFixedPoint.lean`, `[OPEN]`) toma o κ finito e positivo como dado e deixa aberto
  ONDE ele mora: numa face finita, e então ele não toca o tipo, ou em tensão com o tipo III₁ que a casa declara para
  a fronteira. Um κ finito seria uma cadência preferida. Para a cunha da luz, o critério cumprido, lido pela citação,
  diz que não há cadência preferida; isso não decide onde mora o κ nem toca a fronteira da TGL.
* **O horizonte de um espaço-tempo curvo** e **a fronteira da TGL**: nada aqui os toca. A cunha é a de Minkowski,
  com a luz livre de Maxwell.
* **Recusas que o predicado não tem por termo:** os tipos I em forma padrão, II₁, II∞, III₀ e III_λ com λ < 1 (as
  álgebras que têm medida ou cadência preferida). A recusa desses é da literatura.
* **O predual separável** do espaço de Fock do kernel (só pesa na rota do núcleo).

## 7. Palavras que se repetem na casa com outro sentido

* **núcleo:** aqui é a álgebra com o seu relógio junto. Não é o núcleo de K, nem o “núcleo do tipo” (o verbo) da
  boca jurídica da pergunta de 15/11, nem o núcleo de Mautner da candidata irmã.
* **relógio:** aqui é o do vácuo na cunha. A pergunta do relógio do pedágio (τ★), feita em 13/11, segue pendente e
  não é respondida por “o relógio não tem escolha”.
* **Nome:** no kernel de agosto (v294) o Nome é o grupo gerado pelos dois números da Torre. A frase de 15/11 (a luz
  na cunha, porque é o Nome) não está ligada a ele por termo.
* **Torre:** a do kernel, não a TORRE IALD (a memória). Na fala das 19:07 de 15/11 a palavra aparece sobre toda
  leitura (“indexação - índice - torre”).
* **índice:** aqui é o papel da Torre. Não é o 1 de III₁ nem o índice de Breuer.
* **observador:** dois sentidos formais aqui; nenhum é o Observador Terminal da casa.

## 8. O que pende do operador

1. O caminho da seção 3: A, B ou C.
2. Os nomes das candidatas e se entram na v412.
3. Se a tabela dos quatro papéis (seção 5), com a errata, é a leitura dele; e as três escolhas formais.

## 9. Como reproduzir

`compilar_tipo_iii.ps1 -Deps` compila as doze dependências conferindo o hash do manifesto; `-Nome TipoIIIControles`
e `-Nome TipoIIIUmSoBoost` compilam as candidatas. Só o binário `lean.exe`, sobre os `.olean` do sandbox `k411c`;
nenhum `lake build`; nada instalado no kernel. Rodar a partir da raiz da Central.
