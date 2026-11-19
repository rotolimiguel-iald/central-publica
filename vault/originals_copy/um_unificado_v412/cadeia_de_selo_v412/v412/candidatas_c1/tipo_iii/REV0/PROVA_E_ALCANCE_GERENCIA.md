# O tipo III como termo: o que está provado, o que entra por citação e o que segue aberto

> Gerência c1, 16/11/2026. Candidatas, nada instalado, nomes provisórios (o nome das pedras é do operador).
> Hashes, tempos e a lista de teoremas com os axiomas de cada um estão em `RESULTADO_GERENCIA.json`, gerado por
> script a partir dos arquivos e dos logs; este texto não repete hash de memória.
> Validade no kernel não é creditação; o gate não se move; nada aqui é dado da natureza.

## 1. A pergunta e a resposta do operador

A gerência perguntou, em 15/11, o que faltava para o tipo III entrar no kernel como termo. A resposta (bytes em
`work\cunhagens_13out\`, arquivo `OPERADOR_15nov_resposta_tipo_iii_…_verbatim.txt`), numa linha só para conferir:

«a luz testemunhada na cunha é o sujeito que o Nome designa. A Torre a indexa, a borda do horizonte oferece o contraste pelo qual ela é lida, e a relatividade vincula essa leitura ao observador.»

Quatro papéis: o **sujeito** (a luz testemunhada na cunha), o **índice** (a Torre), o **contraste** (a borda do
horizonte) e o **vínculo** (a relatividade, o próprio observador). A ordem foi provar em Lean.

## 2. O que o Codex construiu (examinado por revisores distintos em 15/11: aprovado com ressalvas)

Doze módulos (`dep_codex\`, cópia byte a byte, conferida pelo manifesto; recompilados do zero aqui, todos com
código de saída zero). O centro é o predicado `Vinculo.IsTypeIII1` e o teorema
`Vinculo.maxwell_right_wedge_type_III1 : IsTypeIII1 (net rightWedge)`.

O predicado exige de uma álgebra `A`: centro escalar; um vetor unitário cíclico e separador; um fluxo unitário que
é o do grafo fechado de Tomita desse vetor; que o fluxo preserve `A`; e que o **núcleo** (o produto cruzado
concreto de `A` por esse fluxo, em `L²(ℝ; H)`) tenha centro escalar.

Em língua simples: a álgebra é uma peça só, e continua uma peça só depois de se lhe juntar o seu próprio relógio.

## 3. A ressalva principal: o nome do predicado diz mais do que o termo

O que o termo prova é o **critério do núcleo**. Que uma álgebra que cumpre o critério seja de tipo III₁ no sentido
de Connes (o invariante `S(M)` igual à semirreta inteira) é teorema da literatura `[KNOWN]`: Takesaki, *Duality for
crossed products and the structure of von Neumann algebras of type III*, Acta Math. 131 (1973); Connes e Takesaki,
*The flow of weights on factors of type III*, Tôhoku Math. J. 29 (1977). Esse passo **não está formalizado**, nem
aqui, nem no kernel, nem no Mathlib; e a hipótese de predual separável, que a literatura usa, não foi aferida no
kernel para o espaço de Fock (a instância não é sintetizada).

Logo há duas frases possíveis, e a escolha é do operador:

* **frase A (o termo):** “a álgebra da luz na cunha cumpre o critério do núcleo”;
* **frase B (termo + citação):** “a álgebra da luz na cunha é de tipo III₁”, com o passo de Connes e Takesaki dito
  como citação.

A casa já errou nesse ponto em agosto (v295, `TheMarkIsNotATypeMark`: a marca que não era marca de tipo). Por isso a candidata da
gerência reexporta o teorema com o nome do que ele prova (`a_luz_na_cunha_cumpre_o_criterio_do_nucleo`) e não
renomeia nada do Codex.

## 4. O que a gerência acrescenta (dois módulos, vinte e quatro teoremas, sem `sorry`, só os três axiomas de sempre)

### `TipoIIIControles.lean`

| o que diz, em língua simples | termo |
|---|---|
| **O relógio não tem escolha.** Dois fluxos realizados para a mesma álgebra, o mesmo vetor e a mesma conjugação são iguais. O núcleo do critério não é “um produto cruzado por um fluxo qualquer”. | `o_fluxo_de_tomita_e_unico`, `a_realizacao_tem_um_so_resolvente`, `o_fluxo_do_criterio_e_unico` |
| **Na cunha o relógio é o boost**, sem escolha. | `na_cunha_o_fluxo_do_criterio_e_o_boost` |
| **O predicado recusa** quem contém os operadores de posto um em dimensão ≥ 2 (não tem vetor separador). | `quem_contem_os_postos_um_nao_cumpre` |
| **O predicado recusa** a álgebra abeliana com elemento não escalar. | `a_abeliana_nao_escalar_nao_cumpre` |
| **O predicado recusa** toda álgebra sobre `H = ℂ`. | `sobre_a_reta_complexa_ninguem_cumpre` |
| **Relógio parado não dá núcleo de uma peça só**; nem relógio que age por um número no tempo 1. | `o_fluxo_parado_nao_da_nucleo_fator`, `fluxo_escalar_no_tempo_um_o_nucleo_nao_e_fator`, `o_deslocamento_nao_e_escalar` |
| A cunha, peça por peça: centro escalar; núcleo de centro escalar. | `o_centro_da_cunha_e_escalar`, `o_centro_do_nucleo_da_cunha_e_escalar` |
| **O vínculo como dependência:** o fluxo com que a cunha é lida é o MESMO fluxo cujo núcleo é uma peça só (igualdade por definição). | `o_fluxo_da_leitura_e_o_do_criterio` |
| A leitura da Torre escrita com o fluxo do critério. | `a_torre_e_lida_pelo_fluxo_do_criterio` |
| **A Torre dá os números; a leitura vale para todo número.** A Torre entra como índice. | `a_leitura_vale_para_todo_real`, `a_torre_entra_como_indice`, `a_leitura_modular_vale_para_todo_real` |
| **A borda, com a regra da relatividade, determina tudo:** duas transformações afins iguais em todo ponto da borda são iguais. | `a_borda_determina_a_transformacao_afim` |
| **O que a borda deixa livre é exatamente o que não é afim:** o cisalhamento do Codex, que fixa a borda e muda intervalos, não é afim. | `o_cisalhamento_nao_e_afim` |

### `TipoIIIUmSoBoost.lean` (usa a candidata `ErgodicidadeDeMautner`, por isso em arquivo à parte)

| o que diz | termo |
|---|---|
| Um vetor fixo pelo boost de UM só número da Torre está na reta do vácuo. | `um_so_numero_da_torre_le_o_vacuo` |
| A hipótese de dois boosts do Codex equivale à de um só. | `dois_numeros_nao_acrescentam_a_um` |
| O primeiro número da Torre não é zero. | `o_primeiro_numero_da_torre_nao_e_zero` |

## 5. Como os quatro papéis ficam, um a um

| papel (letra do operador) | o que há por termo | o que NÃO há |
|---|---|---|
| **sujeito**: a luz testemunhada na cunha | a álgebra da cunha cumpre o critério do núcleo; o relógio é único e é o boost | o tipo III₁ de Connes por termo (entra por citação) |
| **índice**: a Torre | os números da Torre (o logaritmo da razão dos pesos) dão os tempos de leitura; a leitura vale para todo número, e a da Torre é um caso; um só número já lê o vácuo | a Torre **dentro** da cunha: o Codex prova que não há injeção da Torre na cunha que respeite os fluxos (`physical_no_flow_intertwining_embedding`). É índice que aponta, não parte que contém |
| **contraste**: a borda do horizonte | a borda são duas folhas nulas; com a regra afim ela determina a transformação; sem a regra, não (o cisalhamento) | “espectro de leitura” como termo: o que há é geometria de pontos. A leitura é do operador |
| **vínculo**: a relatividade | o fluxo que lê é o fluxo do critério (por definição); a cunha transportada por Lorentz e translação cumpre o mesmo critério (`maxwell_observer_wedge_type_III1`, do Codex) | o enunciado conjunto do Codex é uma conjunção: o critério não depende da Torre nem do observador. A dependência provada é só a do fluxo |

## 6. O que segue aberto, dito junto

* **O κ.** `TheScaleHasNoFixedPoint.lean` deixa `[OPEN]` se o κ é finito. Um κ finito seria um ritmo preferido;
  a cunha cumprir o critério não fecha esse item.
* **O horizonte de um espaço-tempo curvo** e **a fronteira da TGL**: nada aqui os toca. A cunha é a de Minkowski,
  com a luz livre de Maxwell.
* **Recusas que o predicado não tem por termo:** os tipos I em forma padrão, II₁ e III_λ com λ < 1. A recusa
  desses é da literatura.
* **O predual separável** do espaço de Fock do kernel.

## 7. O que pende do operador

1. Qual das duas frases da seção 3 vale na casa (A, o termo; ou B, termo mais citação).
2. Os nomes das candidatas e se entram na v412.
3. Se a leitura dos quatro papéis da seção 5 é a dele (em 15/11 ele ratificou a leitura da gerência em bloco; a
   tabela acima é mais fina e ele ainda não a leu).

## 8. Como reproduzir

`compilar_tipo_iii.ps1 -Deps` compila as doze dependências conferindo o hash do manifesto; `-Nome TipoIIIControles`
e `-Nome TipoIIIUmSoBoost` compilam as candidatas. Só o binário `lean.exe`, sobre os `.olean` do sandbox `k411c`;
nenhum `lake build`; nada instalado no kernel.
