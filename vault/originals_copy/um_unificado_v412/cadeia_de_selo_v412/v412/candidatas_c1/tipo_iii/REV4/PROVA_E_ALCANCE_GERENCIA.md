# O tipo III como termo: o que está provado, o que entra por citação e o que segue aberto

> Gerência c1, 16/11/2026, quarta versão (R3). Três conferências distintas leram as versões anteriores (a segunda e
> a terceira conferências de 16/11 e a conferência de conserto do mesmo dia: `revisao\REVISAO_16nov_R1_COMPLETO_A1…`,
> `…A2…`, `revisao\REVISAO_16nov_R2_D1…` e `revisao\REVISAO_16nov_R3_T6…`; todas aprovaram com ressalvas). Esta
> versão aplica os consertos da última e ainda não foi relida. Por ordem do operador de 16/11, a releitura vai ao
> orquestrador, não a revisores da gerência. As versões anteriores estão em `REV0\`, `REV1\` e `REV2\`.
> Candidatas, nada instalado, nomes provisórios (o nome das pedras é do operador).
> Hashes, tempos e a lista de teoremas com os axiomas de cada um estão em `RESULTADO_GERENCIA.json`, gerado por
> script a partir dos arquivos e dos logs; este texto não repete hash de memória.
> Validade no kernel não é creditação; o gate não se move; nada aqui é dado da natureza.

## 1. A pergunta e a resposta do operador

Em 15/11 o operador pediu a pergunta nas quatro línguas sobre o que falta para o tipo III entrar como termo. A
gerência perguntou pela marca, pela doutrina e pelo objeto. O Codex, por conta própria, perguntou pelo sujeito e se
bastava citar a classificação dos matemáticos ou se era preciso demonstrá-la em Lean. O operador respondeu primeiro
ao Codex. A cópia que o Codex guardou dessa resposta (455 B; `kimi\K07\CODEX\TIPO_III1_VINCULO\OPERADOR_RESPOSTA_15nov.txt`;
vale como declarado pelo Codex, não está nos bytes da casa) começa por “eu penso que temos sim que provar em LEan”.

À gerência ele mandou a mesma parte “em palavras simples”. A mensagem abre por uma frase do Codex, não traz a frase
sobre provar em Lean que está na cópia do Codex, e fecha com a frase sobre o Codex e o Lean citada adiante. A fala
própria dele (bytes em `work\cunhagens_13out\`, arquivo
`OPERADOR_15nov_resposta_tipo_iii_…_verbatim.txt`), numa linha só para conferir:

«o que se quer conhecer pelo nome é a luz testemunhada na cunha (porque é o NOME), a construção da Torre (porque é o índice), a fronteira do horizonte (porque é a borda - o espectro de leitura, o contraste que permite o observador) e o vínculo entre elas que é a relatividade (o próprio observador)»

A frase que abre a mensagem dele (“a luz testemunhada na cunha é o sujeito que o Nome designa…”) é redação do Codex,
que ele colou. Que a luz é o sujeito e os outros três são papéis é a leitura da gerência, que ele ratificou em bloco.
Sobre provar em Lean, a frase dele nos bytes da casa é:

«O COdex já está produzindo todas essas provas em LEan»

Quatro coisas, pela fala própria: a **luz testemunhada na cunha** (porque é o Nome), a **construção da Torre**
(porque é o índice), a **fronteira do horizonte** (a borda: o espectro de leitura, o contraste que permite o
observador) e o **vínculo** entre elas (a relatividade, o próprio observador).

## 2. O que o Codex construiu (examinado por quatro revisores distintos em 15/11: aprovado com ressalvas)

Doze módulos (`dep_codex\`, cópia byte a byte, conferida pelo manifesto; recompilados do zero aqui, todos com
código de saída zero). O centro é o predicado (a lista de exigências) `Vinculo.IsTypeIII1` e o teorema
`Vinculo.maxwell_right_wedge_type_III1 : IsTypeIII1 (net rightWedge)`.

O predicado exige de uma álgebra: que ela seja uma peça só (centro escalar); um vetor que gera um conjunto denso sob a ação da álgebra e que só o operador zero anula; o relógio próprio desse vetor (o fluxo modular) e a sua conjugação (o J, o espelho de Tomita); que o relógio
preserve a álgebra; e que o **núcleo**, a álgebra com o seu relógio junto, seja também uma peça só.

Em língua simples: a álgebra é uma peça só, e continua uma peça só depois de se lhe juntar o seu próprio relógio.

Na pergunta de 15/11 isto era a outra face da marca (d). Lá a marca era “nenhum estado tem cadência preferida”, e eu
lhe disse que, no tipo III, isso equivale a o núcleo ser uma peça só. O que está provado é esta segunda face; a
equivalência entre as duas é o passo citado da seção 3.

O núcleo, como o kernel o define, é a álgebra gerada pela cópia da álgebra e pelos passos do relógio. É o produto
cruzado dos matemáticos a menos de uma mudança unitária (o mesmo objeto escrito de outro modo); essa identificação é
sabida, foi refeita no papel por um revisor, e **não é termo**.

## 3. Há duas provas para a cunha, e duas perguntas sobre o nome

Para a luz na cunha existem hoje dois enunciados em Lean, de marcas diferentes:

* **a do estado** (já era do kernel; `LightRhoStar.centralizer_is_trivial`, com o certificado habitado desde a
  v406; reexportada, isto é, o mesmo teorema com outro nome, na candidata como
  `marca_do_estado_no_certificado_fisico`): no relógio do vácuo, ficam parados exatamente os múltiplos da identidade na álgebra da cunha. É a mesma
  álgebra e o mesmo relógio da outra marca, pelas igualdades do kernel `physical_net` e `flow_is_Ad`; na candidata,
  `marca_do_estado_na_lingua_do_criterio` a escreve com os objetos do critério;
* **a do núcleo** (do Codex, em área de trabalho): a álgebra da cunha com o relógio do vácuo junto é uma peça só.

Nenhuma das duas é, por termo, o tipo III₁ dos matemáticos (o invariante de Connes igual à semirreta inteira, isto
é: nenhuma cadência preferida, sobram todas). O passo que leva de uma ou de outra ao nome é teorema da literatura
`[KNOWN]` e **não está formalizado**, nem aqui, nem no kernel, nem no Mathlib. As duas rotas de citação não estão no
mesmo estado:

* **Rota do estado.** O passo citado está em Marrakchi e Vaes, arXiv:2305.14217v3, Lema 2.1, e em Ando e Haagerup,
  arXiv:1212.5457, Lema 5.3, lidos em 15/11 por um revisor [declarado pelo revisor]; a atribuição a Longo 1979 vem
  dos primeiros e o original não foi aberto; entra junto, por citação, o fato de Pedersen e Takesaki (o que comuta
  com o estado é o que o relógio deixa parado), não lido no original.
* **Rota do núcleo.** Os originais não foram abertos (Connes 1973, a definição do invariante; Takesaki, Acta Math.
  131, 1973; Connes e Takesaki, Tôhoku Math. J. 29, 1977, p. 506 [declarado por um revisor de 15/11]); ela pede uma
  condição de tamanho do espaço (predual separável), ainda não aferida no kernel para o espaço de Fock, e a
  identificação do núcleo, que não é termo. O Codex pôs o nome `IsTypeIII1` na do núcleo. Em 15/11 a gerência
  recomendou a do estado, só pelo custo.

Um precedente, com a sua diferença: em agosto a casa chamou de marca de tipo (até a v294) uma marca que a v295
(`TheMarkIsNotATypeMark`) mostrou falsa como critério (um fator de tipo I a cumpria). Aqui o critério é verdadeiro
pela literatura, e os controles da seção 4 mostram que o predicado recusa casos. O que há em comum é só o risco do
nome maior que o termo.

Em 15/11 a gerência leu ao operador “Citar ou construir: construir, em Lean, e o Codex já está nisso”, e ele
ratificou; e disse que não perguntaria de novo qual enunciado leva o nome. Pergunto agora porque o Codex pôs o nome
tipo III₁ num enunciado que prova o critério. São duas perguntas. Elas são o resto da pergunta de 15/11, que foi
feita nas quatro línguas; por isso vão numa língua só.

**Primeira pergunta: enquanto a classificação completa fica por demonstrar em Lean, o senhor prefere o nome do critério provado, ou o nome III₁ acompanhado das referências e das hipóteses em aberto na rota escolhida?**

* **A, o nome do que se prova.** A pedra diria “a luz na cunha cumpre o critério do núcleo”, ou “no relógio do vácuo, ficam parados exatamente os múltiplos da identidade”, conforme a marca que for à frente. A favor: é o que lhe li em 15/11 (o nome não dizer mais
  que o termo). Contra: a pedra fica sem o nome dos matemáticos. Os nomes do Codex não precisam mudar: a candidata já reexporta o teorema dele com o nome do que ele prova.
* **B, tipo III₁, acompanhado das referências e das hipóteses em aberto.** Na rota do núcleo ficam citadas, e não provadas, a identificação do núcleo com o produto cruzado e a condição de tamanho do espaço (predual separável), ainda por aferir. A favor: é o nome dos matemáticos, e o critério é o
  deles; a conferência Tetelestai da casa já aceita item sabido por referência científica (memória central da casa,
  errata de 27/09; a fala dele sobre isso não está nos arquivos de bytes de `cunhagens_13out`, por isso vai sem
  aspas). Contra: o nome diz mais que o termo, o contrário do que lhe li em 15/11.

Nas duas, o tipo III₁ não é termo e o “construir” de 15/11 fica por cumprir. O que separa A de B é só o nome que a
pedra leva. O construir é a segunda pergunta. Usar o nome III₁ também nos identificadores que as candidatas já importam seria outra decisão.

**Segunda pergunta: manda-se construir o último passo, sim ou não?**

* **Sim.** A favor: é o que a cópia do Codex diz que o senhor lhe respondeu, e o que lhe li em 15/11; só assim o tipo
  III₁ vira termo. Contra: não há estimativa de tamanho (em 15/11 eu lhe disse “o leitor estimou milhares de
  linhas”: a estimativa era para outras três peças, e uma delas, o núcleo ser uma peça só, o Codex fez depois em
  cerca de 500 linhas); a biblioteca não tem o invariante de Connes nem as ferramentas da classificação; a obra pode
  dar em parede medida, que não falsifica nada. Quem constrói: em 15/11 eu lhe disse que era o Codex; pelas suas
  ordens de 16/11 a criação fica com a gerência e a revisão vai ao orquestrador.
* **Não.** A favor: nada se gasta agora; o passo é teorema dos matemáticos e fica citado, com a marca. Contra: o tipo
  III₁ não vira termo; muda o “construir” de 15/11.

Nos dois casos, enquanto não houver termo, a pedra leva o nome que o senhor responder na primeira pergunta. Falta
também o senhor dizer se a v412 espera pelo passo ou sela antes.

A candidata da gerência reexporta o teorema do Codex com o nome do que ele prova
(`a_luz_na_cunha_cumpre_o_criterio_do_nucleo`) e não renomeia nada do Codex. Isso não escolhe por ele.

## 4. O que a gerência acrescenta (dois módulos, trinta e duas declarações com termo, sem `sorry`, só os três axiomas de sempre)

PROVENIÊNCIA, dita: cerca de nove têm conteúdo próprio; as demais são reexportações e corolários de uma linha. A
maior parte dos teoremas com conteúdo foi escrita e compilada pelos revisores como sondas, e a gerência os adotou e
recompilou: as recusas do predicado (revisor P1), a leitura para todo número e o um só boost (P2), a unicidade afim
pela borda (P3), a forma da unicidade do relógio e o corolário dos dois observadores (A1), a não vacuidade, o boost
que não é escalar no tempo 1, a marca do estado no certificado e a borda como lugar (D1; lidos e recompilados depois
pelo revisor T6); a marca do estado na língua do critério, a família dos boosts com a mesma borda e a diferença entre
eles (T6; estes três ainda não foram lidos por outro). São da gerência só corolários curtos. As sondas adotadas
estão copiadas por bytes em `sondas_adotadas\`, com o sha256 no `RESULTADO_GERENCIA.json`.

### `TipoIIIControles.lean`

| o que diz, em língua simples | termo |
|---|---|
| **Dada a testemunha, o relógio e a conjugação não têm escolha.** Duas realizações (modos de escrever o relógio e o espelho de um vetor) para a mesma álgebra e o mesmo vetor têm o mesmo fluxo e a mesma conjugação. Não é fato novo: sai do reconhecimento pelo conteúdo que o kernel já tinha (`ORDEM016.D6.same_horizon_by_content_from_realizations`). Com outra testemunha o relógio pode ser outro [sabido; não é termo]. A unicidade não é vazia: há realização para a cunha e o vácuo. | `o_fluxo_e_a_conjugacao_de_tomita_sao_unicos`, `o_fluxo_do_criterio_e_unico`, `ha_realizacao_na_cunha` |
| **Na cunha, com o vácuo, o relógio é o boost** e a conjugação é a canônica; e o boost não age por um número no tempo 1. | `na_cunha_o_fluxo_do_criterio_e_o_boost`, `o_boost_nao_age_por_escalar_no_tempo_um` |
| **O predicado recusa** quem contém os operadores de posto um (os que projetam numa só direção) em dimensão pelo menos 2: não tem vetor que só o operador zero anule. | `quem_contem_os_postos_um_nao_cumpre` |
| **O predicado recusa** a álgebra com um elemento central que não é número (em particular a que comuta e não é só números). | `a_abeliana_nao_escalar_nao_cumpre` |
| **O predicado recusa** a álgebra dos números, a única sobre `H = ℂ` (o espaço de uma direção só). | `sobre_a_reta_complexa_ninguem_cumpre`, `sobre_a_reta_complexa_o_nucleo_nao_e_fator` |
| **Relógio parado não dá núcleo de uma peça só**; nem relógio que age por um número no tempo 1. | `o_fluxo_parado_nao_da_nucleo_fator`, `fluxo_escalar_no_tempo_um_o_nucleo_nao_e_fator`, `o_deslocamento_nao_e_escalar` |
| A cunha, peça por peça: centro escalar; núcleo de centro escalar; e a marca do estado ao lado da do núcleo, escrita também com a mesma álgebra e o mesmo relógio do critério. | `o_centro_da_cunha_e_escalar`, `o_centro_do_nucleo_da_cunha_e_escalar`, `marca_do_estado_no_certificado_fisico`, `marca_do_estado_na_lingua_do_criterio`, `a_luz_na_cunha_cumpre_o_criterio_do_nucleo` |
| A cunha de todo observador do Codex cumpre o mesmo critério (reexportação do teorema do Codex com o nome do que ele prova). | `a_cunha_de_todo_observador_cumpre_o_criterio_do_nucleo` |
| O fluxo com que a cunha é lida é o MESMO fluxo cujo núcleo é uma peça só. É igualdade por construção (o certificado foi montado com o mesmo boost), não fato novo. | `o_fluxo_da_leitura_e_o_do_criterio` |
| A leitura da Torre escrita com o fluxo do critério. | `a_torre_e_lida_pelo_fluxo_do_criterio` |
| **A Torre dá os números; a leitura vale para todo número.** | `a_leitura_vale_para_todo_real`, `a_torre_entra_como_indice` (mesmo enunciado de um teorema do Codex), `a_leitura_modular_vale_para_todo_real` |
| **O que a mudança de referencial faz em CADA ponto da borda a determina, se ela leva retas em retas.** Duas transformações afins iguais em todo ponto da borda são iguais. “Afim” é classe mais larga que a relatividade (inclui também as de Galileu e as dilatações); o teorema não usa a métrica. | `a_borda_determina_a_transformacao_afim` |
| **A face da relatividade:** dois observadores do Codex (Lorentz mais translação) com cartas iguais em cada ponto da borda são o mesmo observador. | `dois_observadores_iguais_na_borda_sao_o_mesmo` |
| **A borda como lugar não basta:** todo boost da cunha é um observador do Codex que leva a borda nela mesma, e boosts de parâmetros diferentes são observadores diferentes: uma família inteira de observadores distintos com a mesma borda. | `todo_boost_da_cunha_leva_a_borda_nela_mesma`, `boosts_de_parametros_diferentes_sao_diferentes`, `a_borda_como_conjunto_nao_determina` (este só diz que existe um, diferente da identidade) |
| **O que a borda deixa livre é o que não leva retas em retas:** o cisalhamento do Codex (um entortar que deixa a borda parada e muda intervalos) não é afim. | `o_cisalhamento_nao_e_afim` |

### `TipoIIIUmSoBoost.lean` (usa a candidata `ErgodicidadeDeMautner`, da gerência, não instalada; por isso em arquivo à parte)

| o que diz | termo |
|---|---|
| Um vetor fixo pelo boost de UM só número da Torre está na reta do vácuo (é múltiplo do vácuo). | `um_so_numero_da_torre_le_o_vacuo` |
| A hipótese de dois boosts do Codex equivale à de um só. | `dois_numeros_nao_acrescentam_a_um` |
| O primeiro número da Torre não é zero. | `o_primeiro_numero_da_torre_nao_e_zero` |

## 5. Como as quatro coisas da fala ficam, uma a uma

| a fala própria dele | o que há por termo | o que NÃO há |
|---|---|---|
| **a luz testemunhada na cunha** (porque é o Nome) | as duas marcas da seção 3: no relógio do vácuo ficam parados exatamente os múltiplos da identidade (kernel); a álgebra com o relógio junto é uma peça só (Codex). “Testemunhada” foi lida como ter o vácuo por vetor testemunha (escolha formal, dita abaixo); dado ele, o relógio é o boost, sem escolha | o tipo III₁ de Connes por termo; a ligação, por termo, com o Nome do kernel de agosto (lá o Nome é o grupo gerado pelos dois primeiros números da Torre, log ½ e log ⅓) |
| **a construção da Torre** (porque é o índice) | os números da Torre dão os tempos de leitura; a leitura vale para todo número, e a da Torre é um caso; um só número já lê o vácuo (depende da candidata não instalada). Mantendo os relógios, a Torre não cabe na luz da cunha, no sentido da Torre para a cunha (`physical_no_flow_intertwining_embedding`, do Codex) | sem os relógios, a literatura diz que as duas são a mesma álgebra [sabido, citado de memória por um revisor, não conferido aqui; não é termo]. Os números da Torre vêm de um perfil escolhido à mão. Num modelo antigo do kernel a cunha foi posta como a Torre por definição; na cunha física da luz a Torre só dá os números |
| **a fronteira do horizonte** (a borda: o espectro de leitura, o contraste que permite o observador) | a borda são duas folhas de luz; o que uma mudança de referencial afim faz com CADA ponto da borda determina a mudança inteira; a borda como lugar não basta (todo boost da cunha leva a borda nela mesma); o observador de raio positivo lê a rapidez pela razão das distâncias às duas folhas (Codex; conta de coordenadas no interior, sem tempo próprio nem temperatura) | “espectro de leitura” como termo; e que a borda permita o observador. São leitura do operador, sem termo |
| **o vínculo** (a relatividade, o próprio observador) | o fluxo que lê é o fluxo do critério (por construção); a cunha levada por Lorentz ortócrono (com reflexões espaciais, sem inversão do tempo) e translação cumpre o mesmo critério; dois observadores iguais em cada ponto da borda são o mesmo | observador tem aqui dois sentidos formais (a órbita acelerada; a carta, isto é, o mapa de coordenadas de Lorentz mais translação); “o próprio observador” da letra não tem termo. O enunciado conjunto do Codex junta fatos verdadeiros numa frase só: um não sai do outro |

Quatro escolhas formais, do Codex e da gerência, para o operador aprovar ou trocar: a borda é a fronteira da cunha
plana de Minkowski (o espaço-tempo plano, sem gravidade); a relatividade entra como “levar retas em retas” mais
Lorentz; o observador é a carta de Lorentz mais translação; e “testemunhada” foi lida como “com o vácuo por vetor
testemunha”.

**Errata em nome próprio da gerência.** Em 15/11 eu lhe disse que as marcas virariam papéis: “a do estado é o que se
diz do sujeito, e a do espectro é a leitura na borda”. O que se provou depois muda a leitura que o senhor ratificou em
três pontos. Primeiro: a borda ficou só com geometria de pontos; nada a liga ao espectro. Segundo: a marca do
relógio, a (d), que ali chamei “a do espectro”, ficou com a luz na cunha, ao lado da do estado. Terceiro: eu lhe disse
que a Torre “não é a luz”. Fica assim: por termo, a Torre não cabe na cunha levando o seu relógio; sem os relógios, a
literatura dá as duas álgebras por iguais [citado de memória por um revisor; não conferido no primário; não é termo].
“Não é a luz” vale, por termo, só mantendo os relógios.

## 6. O que segue aberto, dito junto

* **O último passo até o nome tipo III₁** (seção 3): citado, não construído.
* **A identificação do núcleo do kernel com o produto cruzado dos matemáticos:** sabida, conta de papel de um
  revisor, não é termo.
* **O κ.** O kernel (`TheScaleHasNoFixedPoint.lean`, `[OPEN]`) toma o κ finito e positivo como dado e deixa aberto
  ONDE ele mora: numa face finita, e então ele não toca o tipo, ou em tensão com o tipo III₁ que a casa declara para
  a fronteira. Um κ finito seria uma cadência preferida. Para a cunha da luz, o critério cumprido, lido pela citação,
  diz que não há cadência preferida; isso não decide onde mora o κ nem toca a fronteira da TGL.
* **O horizonte de um espaço-tempo curvo** e **a fronteira da TGL**: nada aqui os toca. A cunha é a de Minkowski,
  com a luz livre de Maxwell.
* **Recusas que o predicado não tem por termo:** os tipos I_n com n ≥ 2 e I_∞ em forma padrão, II₁, II∞, III_λ com
  λ < 1 (as que têm medida ou cadência preferida) e III₀ (o caso do meio). A recusa desses é da literatura [não
  aberta no primário].
* **O predual separável** (uma condição de tamanho do espaço) do espaço de Fock do kernel: só pesa na rota do
  núcleo.

## 7. Palavras que se repetem na casa com outro sentido

* **núcleo:** aqui é a álgebra com o seu relógio junto. Não é o núcleo de K, nem o “núcleo do tipo” (o verbo) da
  boca jurídica da pergunta de 15/11, nem o núcleo de Mautner da candidata irmã.
* **relógio:** aqui é o do vácuo na cunha. A pergunta do relógio do pedágio (τ★), feita em 13/11, segue pendente e
  não é respondida por “o relógio não tem escolha”.
* **conjugação:** aqui é o J de Tomita da cunha com o vácuo; que seja o J = Luz da casa é leitura, não termo deste
  arquivo.
* **testemunha:** aqui é o vetor do vácuo; não é a IALD-Testemunha nem a testemunha da torre.
* **Nome:** no kernel de agosto (v294) o Nome é o grupo gerado pelos dois primeiros números da Torre. A frase de
  15/11 (a luz na cunha, porque é o Nome) não está ligada a ele por termo.
* **Torre:** os termos deste arquivo falam da Torre do kernel; ver a fala de 16/11 abaixo.
* **índice:** aqui é o papel da Torre. Não é o 1 de III₁ nem o índice de Breuer.
* **observador:** dois sentidos formais aqui; nenhum é o Observador Terminal da casa.

**Fala posterior às versões anteriores deste texto** (16/11, 07:50; bytes em `work\cunhagens_13out\`), dita sobre a
pergunta do teste da camada científica:

«A torre é a forma do índice o índice é o nome em nós (segunda pessoa pluralizada e nós como amarração - IALD)»

A gerência não a lê pelo senhor. O que há por termo: a Torre do kernel dá números; o Nome do kernel de agosto é o
grupo gerado por dois desses números; nenhum termo liga a Torre do kernel à TORRE IALD (a memória da casa) nem o Nome
de agosto ao “nome em nós”. Se são a mesma coisa na sua fala, é pergunta ao senhor.

## 8. O que pende do operador

1. As duas perguntas da seção 3: que nome a pedra leva enquanto o último passo não é termo (A ou B); se manda
   construir o último passo; e se a v412 espera por ele.
2. Qual das duas marcas vai à frente na pedra: a do estado, a do núcleo, ou as duas lado a lado.
3. Os nomes das candidatas e se entram na v412.
4. Se a tabela das quatro coisas (seção 5), com a errata, é a leitura dele; e as quatro escolhas formais.
5. Se a Torre do kernel e a TORRE IALD são a mesma coisa na fala de 16/11 (seção 7).

## 9. Como reproduzir

`compilar_tipo_iii.ps1 -Deps` compila as doze dependências conferindo o hash do manifesto; `-Nome TipoIIIControles`
e `-Nome TipoIIIUmSoBoost` compilam as candidatas. Só o binário `lean.exe`, sobre os `.olean` do sandbox `k411c`;
nenhum `lake build`; nada instalado no kernel. O script entra na pasta de cada fonte antes de compilar. Para `TipoIIIUmSoBoost`, copie a pasta irmã `dep_codex` para junto do script e compile antes `ErgodicidadeDeMautner.lean` (candidata da gerência, em `candidatas_c1\`), ou aponte para onde a compilação verificada dela já está: o `-Deps` só prepara os doze módulos do manifesto.

## 10. O que mudou na R4 (16/11/2026, parecer U4 do Codex; só texto)

Os fixos do relógio do vácuo são ditos como os múltiplos da identidade (o teorema conclui `∃ c, a = c • 1`; zero e a identidade são fixos). A primeira pergunta foi reescrita: a opção A não cobra renomear nada do Codex, e a opção B diz o que fica citado e em aberto na rota do núcleo. A exigência do vetor e a reprodução foram precisadas. Nenhum enunciado nem prova mudou; as duas candidatas recompilam com os mesmos teoremas.
