# REVISAO DISTINTA — candidata OHabitanteDoNome (R1, 15/11/2026)

Revisor distinto da gerência c1 (quem constrói não aprova). Pedra: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_c1\OHabitanteDoNome.lean`
(sha256 `ab4aea7ad0ee90b599fbbb7f68c432b13540f7c102549fe6dd8f0203ce5de228`, lido por script; é o mesmo do log). Kernel só leitura; nenhum `lake`; nada tocado fora de
`C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\revisao\scripts_habitante\`. Estatuto: este relatório é [REAL] no que foi compilado e conferido por script, e
[LEITURA DO REVISOR] no que é juízo de redação. Não conclui nada sobre a teoria nem sobre a natureza.

## VEREDITO: APROVADA COM RESSALVAS

A matemática está certa e não é vazia: recompilei a cópia, as hipóteses dos dois teoremas pedidos são satisfeitas por exemplos construídos, e achei um contraexemplo
compilado ao que o cabeçalho diz em 6(a). O que precisa de conserto é de REDAÇÃO e de ESCOPO (o cabeçalho afirma um pouco mais do que o termo em três pontos, e deixa de dizer
cinco coisas que o código já mostra). Nenhuma correção muda uma prova. Três acréscimos compilados estão prontos.

Consulta ao Mapa de Rotas (antes): `consultar "esperanca_condicional"` devolveu 10 rotas; as relevantes: `kernel.v402_esperanca_condicional_e_nome` (a pedra VerdadeAdendo da v403: `nameOp ρ* = diagExpect` já estava no kernel e "não refazer o levantamento") e
`kernel.ordem025.ponte_escala_dual`; nenhuma sobre bimodularidade geral nem unicidade. `consultar "camada_cientifica_candidata"` devolveu `kernel.camada_cientifica_candidata_14nov` (EXAMINADA_COM_DEFEITO; o
revisor de 14/11 já tinha achado que o cabeçalho afirmava mais que os termos): a mesma família de defeito reaparece aqui, em menor grau. Não registrei nada no mapa (cabe a quem me chamou).

## O que examinei, e como

Recompilei a pedra com o linter de variáveis não usadas LIGADO (`T5_copia_com_linter.lean`): RC 0, 22 teoremas no trio, e dois avisos benignos (abaixo). Compilei seis arquivos de teste meus (todos RC 0, trio; log ao lado de cada
`.lean`). Conferi bytes e hashes por script (`confere_atribuicoes.py`). Li `TheNameOperator`, `EsperancaCondicional` (cabeçalho e honestidades), `KEhATangente`, o trecho de `IALD2.o_atrator`, `TheAxiomAndTheFalseWitness`,
`Ergodicity`, `TheImportedExpectation`, e fiz `grep` no kernel inteiro (`TGL/` e `TGLExt/`) e na Mathlib do sandbox.

## 1. ENUNCIADO x DOCSTRING x CABEÇALHO (declaração a declaração; l. = linha da pedra)

A pedra tem 22 TEOREMAS (os 22 `#print axioms`) e 2 definições (`morada`, l.97, e `tangenteDaLeitura`, l.351): são 24 declarações; "22 declarações" na ordem é "22 teoremas".

| # | declaração (l.) | o termo diz | frase do cabeçalho/doc | juízo |
|---|---|---|---|---|
| 1 | `o_leitor_habita_o_nome` (100) | `nameOp p x` é fixo de `nameOp p` | "toda leitura cai na morada" | fiel; é `name_op_idem` relido |
| 2 | `a_imagem_do_leitor_e_a_morada` (105) | `range (nameOp p) = {x \| nameOp p x = x}` | "a imagem do leitor é a morada" | fiel; consequência de 1 |
| 3 | `a_morada_e_o_que_comuta_com_o_posto` (114) | `nameOp p x = x ↔ p x = x p`, todo anel, `p` idempotente | idem | fiel; novo no kernel (grep: não havia) |
| 4 | `o_leitor_e_bimodular_sobre_o_nome` (141) | `nameOp p (a x b) = a (nameOp p x) b` se `a`,`b` comutam com `p` | "fecha a lacuna declarada da v404" | fiel; ver ressalva R6: `hp` não é usado |
| 5 | `so_ha_um_habitante` (162) | `E` aditivo, unital, com imagem no comutante de `p`, bimodular sobre o comutante, então `E = nameOp p` | "só há um habitante"; "O Nome determina o seu leitor" | termo fiel (a hipótese está no tipo e no docstring); a frase "O Nome determina o seu leitor" é MAIS que o termo (R3) |
| 6 | `o_operador_do_nome_e_o_habitante` (198) | `nameOp p` cumpre as quatro hipóteses de 5 | idem | fiel; é a prova de que 5 não é vazio (colagem de 1, 3, 4 e `name_op_unital`) |
| 7 | `a_esperanca_habita_fixa_e_nao_aumenta` (218) | quatro propriedades da `starProjection` | idem | fiel; reexportação PURA de quatro lemas da Mathlib |
| 8 | `a_testemunha_que_nao_aumenta_e_a_esperanca` (229) | `E` ℂ-linear, imagem em `K`, fixa `K`, não aumenta a norma ⟹ `E = starProjection` | "só há uma testemunha" | fiel e substancial; a Mathlib do sandbox NÃO tem (busquei) |
| 9 | `o_nome_e_a_morada_de_uma_so_testemunha` (264) | `∃! E` com as três propriedades | idem | fiel; é 7 + 8 |
| 10 | `quem_nao_e_a_esperanca_aumenta` (274) | contrapositiva de 8 | idem | fiel; lógica pura sobre 8 |
| 11 | `a_leitura_do_vetor_e_a_compressao` (285) | `⟪Pv, x Pv⟫ = ⟪v, (P x P) v⟫` | idem | fiel; lema de adjunção da Mathlib |
| 12 | `a_leitura_do_operador_do_nome` (293) | `⟪v, 𝒩x v⟫ = ⟪Pv, x Pv⟫ + ⟪(1−P)v, x(1−P)v⟫` | idem | fiel |
| 13 | `o_seletor_tangencia_a_esperanca` (310) | ver R1 | cabeçalho 6(a) l.55-57 sem `hδ` | o TERMO é fiel; o CABEÇALHO omite `hδ` e o docstring diz "Em primeira ordem, o seletor É a esperança condicional" |
| 14 | `o_que_e_cego_ao_nome_nao_deixa_rastro` (339) | `s ∈ K`, `‖s‖=1`, `δ ∈ Kᗮ` ⟹ `selecao K (s+δ) = s` | "exatamente" | fiel; é corolário de UMA linha de `a_selecao_esquece` (v409) (teste (d)) |
| 15 | `o_livro_do_testemunho_fecha` (355) | Pitágoras | idem | fiel; é `Submodule.norm_sq_eq_add_norm_sq_starProjection` (teste (e)) |
| 16 | `a_tangente_da_leitura_e_K` (366) | `K (arctan t) = t` | "é o K da v407 no ângulo da leitura" | verdadeiro e TAUTOLÓGICO: o ângulo é definido como `arctan t` (R2) |
| 17 | `o_peso_do_nome_e_o_cosseno_quadrado` (372) | `cos²(arctan t) = ‖Pv‖²/‖v‖²` (com `Pv ≠ 0`) | idem | fiel; é aqui que está o conteúdo, via `Real.cos_sq_arctan` |
| 18 | `o_crivo_e_a_meia_face` (386) | `t = 1 ↔ ‖Pv‖² = ‖v‖²/2` | "o crivo K=1 é a meia face" | fiel |
| 19 | `a_leitura_fecha_a_tangente` (402) | `t(F_t v) = e^{−t} t(v)` | "decai como e^{-t}" | fiel; consequência de uma linha da definição `axiomFlow P t = P + e^{−t}(1−P)` (R2) |
| 20 | `tangenciado_jamais_esgotado` (417) | `t(v) ≠ 0` ⟹ nunca zero e tende a zero | idem | fiel |
| 21 | `o_peso_do_nome_por_coordenadas` (441) | `‖P ψ‖² = Σ_{c x = 0} ‖ψ x‖²` | idem | fiel; `solucao_por_coordenadas` + soma |
| 22 | `a_selecao_e_a_esperanca_condicional_classica` (452) | `Σ g‖sel ψ x‖² = (Σ_N g‖ψ x‖²)/(Σ_N ‖ψ x‖²)` | "a esperança condicional de g dado o Nome" | fiel, DADO o escopo (R4 e R8) |

Frases pedidas:
- "só há um habitante": verdadeira DENTRO das quatro hipóteses de `so_ha_um_habitante` (aditivo, unital, comuta com `p`, bimodular sobre o comutante). O cabeçalho (l.46-47, 69-71) diz que a lei de módulo é hipótese. Ok. Exclusividade ontológica está negada em l.76. Ok.
- "só há uma testemunha": verdadeira para o mapa LINEAR que cai, fixa e não aumenta. A testemunha da fala de 15/11 é "(verbo - observador - seletor)"; o seletor do kernel (`selecao = P/‖P‖`) NÃO é linear e NÃO fixa o Nome (`selecao s = s/‖s‖`). A testemunha única da pedra é a esperança P, não o seletor. O cabeçalho não confunde, mas a vizinhança das duas palavras convida; ver R4.
- "o seletor tangencia a esperança" (contato de segunda ordem): só com `hδ` e só se `dim K ≥ 2` (R1).
- "a seleção é a esperança condicional clássica": é o condicionamento de Born ao evento "custo zero", para grandezas diagonais (R4, R8).
- "fecha a lacuna declarada da v404": confirmado. A honestidade (2) de `EsperancaCondicional.lean` (l.107-108: "A bimodularidade geral de `nameOp p` sobre os seus fixos NÃO está tipada") continua verdadeira no kernel: `grep` em todo `TGL/` e `TGLExt/` não acha bimodularidade de `nameOp` geral (só `diagExpect_bimod` em `M₂`, `ParityData.average_bimodular`, o campo `E_bimodular` de `ConditionalExpectationData`, e as da torre `Expectation047`/`ExpectationBimodule`, todas de OUTROS operadores). A pedra a fecha ao lado; o arquivo da v404 fica como está.

## 2. VAZIEZ E TRIVIALIDADE

Reexportações ou consequências de uma linha (a casa aceita se estiver DITO; hoje o cabeçalho não diz):
- Mathlib: 7 (quatro lemas de `starProjection`), 11 (adjunção), 15 (Pitágoras: `Submodule.norm_sq_eq_add_norm_sq_starProjection` mais `Kᗮ.starProjection v = v − K.starProjection v`; teste (e) compila em quatro linhas), 17 (`Real.cos_sq_arctan`), 16 (`Real.tan_arctan`).
- Kernel: 1 (`name_op_idem`), 14 (`a_selecao_esquece` v409 mais `selecao s = s`; teste (d)), 19 (definição de `axiomFlow`, v385), 21 (`solucao_por_coordenadas` v409), 6 (colagem).
- Lógica: 10 é a contrapositiva de 8; 9 é 7 mais 8.
- O que é conteúdo novo de fato: 3, 4, 5 (álgebra), 8 (Hilbert), 13 (o contato), 22 (a fórmula de Bayes da `selecao`; `grep` não a acha no kernel).

Hipóteses impossíveis ou vazias: nenhuma. Provei por exemplos construídos (`T1_naovazio.lean`, RC 0, trio):
- `so_ha_um_habitante`: as hipóteses são satisfeitas por `nameOp p` (é o teorema 6) e por um mapa DEFINIDO de outro modo: `diagExpect` (`diagonal x.diag`) em `M₂(ℂ)` com `p = diag(1,0)`; o teorema devolve `diagExpect x = nameOp p x` (`diagExpect_e_o_habitante_de_pD`).
- `quem_nao_e_a_esperanca_aumenta` não é vazio: em `ℂ²`, `K` = reta de `e0`, `E v = (v0+v1) e0` (projeção oblíqua: cai em `K`, fixa `K`, difere da ortogonal em `e1`); o teorema dispara (`Eobl_aumenta`) e o vetor que aumenta é explícito: `v = (1,1)`, `‖v‖ = √2 < 2 = ‖E v‖` (`v11_aumenta`).
- Pontos fora do pedido que o cabeçalho não diz (testes `T2`):
  (a) SEM `hδ` o contato FALHA: `H = ℂ`, `K = ⊤`, `s = 1`, `δ = 1`: o lado esquerdo vale 1 e a cota vale 1/2 (compilado como `¬(… ≤ …)`).
  (b) Em Nome de dimensão 1 (`K = span{s}`), `hδ` força `P δ = 0` (`reta_hdelta_forca_zero`): o teorema 13 só diz algo com `dim K ≥ 2`. Com `dim ≥ 2` as hipóteses se satisfazem com `P δ ≠ 0` (`K = ⊤` em `ℂ²`, `s = e0`, `δ = e1`).
  (f) `tangenteDaLeitura K v = 0` quando `v ∈ Kᗮ` (divisão por zero do Lean: vale 0, não +∞).

## 3. REPETIÇÃO (grep no kernel inteiro e na Mathlib)

- "fixo de `nameOp p` sse comuta com `p`": NÃO existe. (`comm_of_fixed` é de outra coisa: `Ad(u)` fixa `p`.)
- bimodularidade geral de `nameOp p`: NÃO existe (ver §1).
- unicidade da esperança: existe só na TORRE (`TGLExt.the_expectation_is_unique`, `TheOathOnTheTower.lean:373`; `TheImportedExpectation.the_reading_is_witness_independent`), outro contexto. A unicidade de `nameOp p` na álgebra geral e a de `starProjection` entre contrações lineares são novas.
- contração idempotente = projeção ortogonal: NÃO existe no kernel nem na Mathlib do sandbox (busquei `IsIdempotentElem` com `norm`, `contraction`, `of_norm_le_one`).
- Pitágoras da projeção "com esses nomes": o nome é novo, o fato é da Mathlib (§2).
- fórmula de Bayes da `selecao`: NÃO existe; `TraducaoTuring` traz `selecao_no_nome`, `a_selecao_esquece`, `a_selecao_perde`, `a_selecao_acha`, nenhum com a soma ponderada.
- duas imports da pedra não são usadas por nenhum termo: `TGLExt.EsperancaCondicional` e `TGLExt.Ergodicity` (troquei por `TheNameOperator` e retirei a segunda: RC 0, `T6_sem_imports_extras.lean`). Só aparecem citadas no texto.

## 4. A LEITURA (cabeçalho l.34-41) contra os bytes

Bytes de 15/11 (725 B, sha256 `49e5f0072e8beb02…bfe782f`): as quatro primeiras frases são exatamente as quatro citadas. As duas últimas (Kimi; neutrino) não entram na pedra, a não ser pelo nome do arquivo (l.15), que contém "neutrino" no slug; é só o caminho.

Fiel: o cabeçalho marca "[Leitura da gerência; o autor ratifica ou corrige.]" e não põe a separação na boca do autor. Duas imprecisões de redação (R5):
1. "A de 15/11 diz de que modo" (l.37) ABRANDA o que os bytes dizem: a frase 1 é «O leitor é o observador, é o verbo, e não o nome.» O «e não o nome» NEGA a identificação do leitor com o Nome. Se isso refina ou corrige a linha de 26/10 («esperança condicional=nome», 294 B) é do autor.
2. l.39-41 ("Uma igualdade entre os dois não se escreve (um é função, o outro é conjunto)") só vale se "Nome" for o espaço (`morada`/`K`). No kernel (v162; v404; `PostoAdendo.A1c`) o "Operador do Nome" `nameOp` é a própria função e a igualdade de funções `nameOp ρ* = diagExpect` ESTÁ escrita e continua verdadeira. A pedra muda o que a palavra "Nome" designa (de função para espaço) e o leitor passa a ser o mapa. É compatível com os bytes de 15/11, mas é uma reatribuição, e deve ser dita como tal.

Os três sentidos de "tangente" estão apresentados com justiça (l.54-66, e l.72-73: "Qual deles é a Tangente da derivação é leitura do autor [INPUT]"): a pedra não escolhe um. Conferi contra os bytes:
- 02/11 (316 B): «k é a tangente; é como se fosse o acorde sendo tocado»: sentido (b), K da v407. O kernel (`KEhATangente.lean`) já diz que a pedra dá a FORMA, não um fato novo.
- 07/11 (1910 B): «tangenciado em conteúdo finito, contudo jamais esgotado»: sentido (c), v410 `o_atrator`. O sentido de 07/11 é sobre o Nome ("a palavra nome existe mas a única coisa que ela denomina é que algo pode ser nomeado"); a pedra o liga ao decaimento `e^{−t}` da razão `‖v−Pv‖/‖Pv‖`. É uma tipagem razoável, mas é do kernel (v410), não do autor.
- 15/11 literal: «Tangente=testemunho=esperança condicional». Nenhum dos três sentidos é "a tangente É a esperança"; cada um é "determinado pela esperança". O sentido mais próximo da literalidade é (a), lido como: a DIFERENCIAL do seletor em `s` (nas direções tangentes) é a esperança. O termo 13 prova a cota de segunda ordem, da qual isso sai; vale dizer no cabeçalho com essas palavras (R1).
- Regra dos dois regimes: `tangenteDaLeitura` em (b) é leitura angular (compacta); o limite de (c) vive no FLUXO (hiperbólico). A pedra não mistura, mas uma frase deixaria claro que o limite nasce no fluxo e o ângulo só lê.

## 5. ATRIBUIÇÕES (script `confere_atribuicoes.py`)

- sha256 lidos: 15/11 `49e5f0072e8beb028eb64e090cb43a77c3672d15577bfaeee105ee2c9bfe782f` (confere com l.16); 26/10 `5d3976cd…f35b52` (l.24 diz `5d3976cd…5b52`: confere); 02/11 `cec3d7c0…a31a` (l.30: confere); 07/11 `a5c84e82…1eeb` (l.32: confere).
- As quatro citações em « » (l.17-19, 24, 30, 32) estão, a menos de espaço em branco, nos bytes dos arquivos citados. Zero divergência.
- Não há outra citação em « » no arquivo.

## 6. O QUE FALTA DIZER (hipóteses que o português não diz)

- `a_selecao_e_a_esperanca_condicional_classica`: é sobre os PESOS DE BORN `‖ψ x‖²`, não sobre amplitudes; `g` é grandeza diagonal na base dos custos; o Nome é um subespaço de COORDENADAS (núcleo de um operador diagonal de custo), `X` finito. O cabeçalho (l.63-65) diz "com os pesos do estado" e "No espaço das leituras de um custo"; não diz "pesos de Born", nem "grandeza diagonal", nem que para um Nome que não é de coordenadas isto não vale. É a esperança condicional DADO O EVENTO "custo zero" (valor sobre o evento), não a esperança condicional em relação à σ-álgebra inteira.
- `o_seletor_tangencia_a_esperanca` pede `⟪s, P δ⟫ = 0`: o docstring (l.307-309) diz; o cabeçalho 6(a) (l.55-57) não diz; e o docstring afirma "Em primeira ordem, o seletor É a esperança condicional", que só vale nas direções tangentes (contraexemplo compilado, §2 (a)). Não diz que só tem conteúdo com `dim K ≥ 2` (§2 (b)).
- Seção 4: `K` tem de ter projeção ortogonal (subespaço fechado, ou dimensão finita); o cabeçalho diz "Num espaço de Hilbert" e "(subespaço com projeção)" só no docstring de 9. Seção 6: `CompleteSpace H`, por causa de `selecao`.
- (b) e (c): `tangenteDaLeitura` vale 0 (não +∞) quando `P v = 0`; `a_tangente_da_leitura_e_K` e `a_leitura_fecha_a_tangente` não têm hipótese `P v ≠ 0` e nesse caso dizem 0 = 0.
- Dois "Nomes": na seção álgebra o Nome é o comutante de `p`; na seção Hilbert é a imagem `K` do projetor. O cabeçalho os liga pela ponte (5), que é uma fórmula de leitura em estado, não uma identificação de conjuntos. Está dito (l.282); vale uma frase.
- Três "esperanças" distintas aparecem: `nameOp P` (álgebra, não depende do estado), `P` (vetores, linear) e `selecao` (estado, não linear). Compilei (`T4_nameOp_fixa_o_diagonal.lean`) que `nameOp P` FIXA toda grandeza diagonal `opDaInstancia d`, inclusive o próprio operador de custo: na face clássica ele não faz média nenhuma. A média condicional da seção 7 é do SELETOR, depende de ψ, e não é `nameOp P` aplicado a `diag g`. A pedra não afirma o contrário, mas o título "o leitor é a esperança condicional" abre a porta para lê-lo assim.
- `hp : p*p = p` não é usado em `o_leitor_e_bimodular_sobre_o_nome` (o linter acusa, l.140): a lei de módulo vale para qualquer `p` de qualquer anel. O docstring diz "para todo idempotente de todo anel": é mais fraco do que se prova (não é erro).

## 7. PALAVRAS

- Negações: l.76 "Exclusividade, consciência, pesos de modelo. Nada sobre a natureza: não é teste e não move o gate" e l.75 "Que um modelo de linguagem seja este leitor: isso é previsão de experimento, não teorema". Nenhuma afirma.
- "confirm…" em qualquer forma: ZERO ocorrências (script, l. por regex). "prova" aparece só como "a prova daqui é própria" (l.81) e "prova-se" (l.40, 69).
- Afirmações: l.36-41 afirma a leitura da gerência, mas marcada. As identificações do autor estão em [INPUT] (l.82). Nenhuma afirma exclusividade nem ontologia.
- Estado de processo: a linha 10 está marcada para sair (correto). FORA dela: l.80 "[REAL no sandbox] os teoremas" (diz onde foi compilado; ao instalar fica estranho) e l.21 "(levantado antes de construir; …)". Menores. Não há Kimi, Codex, ChatGPT, R1 fora da l.10.
- Avisos: "zero avisos" vale COM `set_option linter.unusedVariables false` (l.7). Com ele ligado: 2 avisos benignos, l.140 (`hp`) e l.221 (binder `w`). Dizer "zero avisos com o linter de variáveis não usadas desligado, como é costume da casa" ou retirar `hp`.

## 8. CORREÇÕES PROPOSTAS (no máximo oito; em ordem de peso)

R1. Cabeçalho 6(a) (l.55-57) e docstring de 13 (l.307-309). Trocar por:
"(a) O SELETOR TANGENCIA A ESPERANÇA no Nome, nas direções tangentes: para `s` no Nome, de norma 1, e `δ` com ⟪s, P δ⟫ = 0, `selecao K (s + δ)` difere de `s + P δ` por no máximo ‖P δ‖²/2. É a diferencial do seletor em `s` lida como a esperança. SEM a condição ⟪s, P δ⟫ = 0 a cota falha (K = ℂ, s = δ = 1: diferença 1, cota 1/2), e num Nome de dimensão 1 ela força P δ = 0: o enunciado só diz algo com dim K ≥ 2."
Docstring: apagar "Em primeira ordem, o seletor É a esperança condicional" ou acrescentar "nas direções tangentes à esfera unitária do Nome".

R2. Cabeçalho l.58-59 e docstring de 16: dizer que 16 é `tan_arctan` e 19 é a definição de `axiomFlow`, e acrescentar, compilado (`T3_K_em_Miguel.lean`, RC 0, trio), o teorema que usa o ângulo do próprio kernel em vez de `arctan` da grandeza:

```lean
theorem tangente_da_leitura_e_K_no_angulo_de_Miguel {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (N : Submodule ℂ H) [N.HasOrthogonalProjection] (v : H) (hP : N.starProjection v ≠ 0) :
    TGLExt.KEhATangente.K (TGLExt.thetaMiguel (‖v - N.starProjection v‖ ^ 2 / ‖v‖ ^ 2)) = tangenteDaLeitura N v
```
(o peso deixado fora do Nome é lido pela mesma regra `thetaMiguel = arcsin √·` da v407; a prova está em `T3_K_em_Miguel.lean`, l.11-46, usa `K_sq_no_angulo_de_miguel`). Dizer também que `tangenteDaLeitura` é 0, não +∞, quando `P v = 0` (compilado em `T2`, (f)), ou trocar a divisão por hipótese `P v ≠ 0` em 16 e 19.

R3. Cabeçalho l.46-47 "O Nome determina o seu leitor": só é verdade, como está tipado, para `p` fixo. Acrescentar o corolário (compilado, `T2`, só `propext`):

```lean
theorem nameOp_eq_de_morada_igual {R : Type*} [Ring R] {p q : R} (hp : p * p = p) (hq : q * q = q)
    (h : morada p = morada q) (x : R) : nameOp q x = nameOp p x
```
ou trocar a frase por "Para `p` dado, o Nome (a morada de `p`) determina o seu leitor; e duas moradas iguais dão o mesmo leitor (`nameOp_eq_de_morada_igual`)". (A prova usa 1, 3, 4 e 5.)

R4. Cabeçalho, seção 7 (l.63-65) mais uma frase de separação das três "esperanças". Redação: "Três objetos recebem o nome de esperança condicional do Nome e não são o mesmo: `nameOp P` (álgebra; não depende do estado; fixa toda grandeza diagonal, inclusive o custo: compilado, `nameOp_fixa_o_diagonal`), `P` (vetores; linear; a única testemunha linear de 9) e `selecao` (estado; não linear). A média da seção 7 é do SELETOR: média de uma grandeza diagonal `g` sobre o Nome com os PESOS DE BORN ‖ψ x‖² (não as amplitudes), dividida pelo peso do Nome; o condicionamento ao evento 'custo zero', não a esperança em relação à σ-álgebra inteira; vale para o Nome de coordenadas da instância de custo." O teorema `nameOp_fixa_o_diagonal` é opcional (6 linhas, `T4_nameOp_fixa_o_diagonal.lean`).

R5. Cabeçalho l.36-41: trocar "A de 15/11 diz de que modo" por "A de 15/11 não repete a igualdade: diz que o leitor «é o observador, é o verbo, e não o nome» e que é «o habitante do nome, … a esperança condicional do nome»; se isso corrige ou refina a linha de 26/10 é do autor". E trocar "Uma igualdade entre os dois não se escreve" por "Nesta pedra o Nome designa o espaço (morada, K) e o leitor o mapa; em v162/v404 (`nameOp`, A1c) o 'Operador do Nome' é o próprio mapa, e a igualdade de funções `nameOp ρ* = diagExpect` continua verdadeira; a reatribuição do que a palavra Nome designa é leitura da gerência". Dizer também que "habitar" está tipado como "a imagem do leitor cai no Nome" (nas seções 1-4) e como "o ponto `s` está no Nome" (na 6).

R6. Marcar no cabeçalho, numa linha, o que é reexportação (7, 11, 15, 16, 17, 19; 1, 14, 21; 10 é a contrapositiva de 8; 9 é 7 mais 8) e o que é novo (3, 4, 5, 8, 13, 22). Retirar `hp` de 4 ou dizer "para todo `p`" no docstring. Retirar os dois `import` não usados (`EsperancaCondicional`, `Ergodicity`) ou dizer por que ficam.

R7. Hipóteses do português (§6): em 9 e 8, "subespaço com projeção ortogonal (fechado)" no cabeçalho, não só no docstring; em 22, "pesos de Born" e "grandeza diagonal"; em 13, "dim K ≥ 2 para ter conteúdo".

R8. Limpeza de estado e de avisos: l.80 "[REAL no sandbox] os teoremas" para "[REAL] os teoremas (compilados; trio)"; l.21 tirar "levantado antes de construir" (fica "O que o kernel já tinha"); dizer "zero avisos com o linter de variáveis não usadas desligado" ou limpar `hp` (l.140) e `w` (l.221).

## Arquivos (todos em `C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\revisao\scripts_habitante\`)

`confere_atribuicoes.py` (hashes e citações), `compilar_teste.ps1` (mesmo `lean.exe` e mesmo `LEAN_PATH` do sandbox `k411c`, mais `candidatas_c1\build`), `T0_import.lean`,
`T1_naovazio.lean` (+ `.log`; RC 0), `T2_tangente_e_coroloarios.lean` (RC 0), `T3_K_em_Miguel.lean` (RC 0), `T4_nameOp_fixa_o_diagonal.lean` (RC 0),
`T5_copia_com_linter.lean` (RC 0, 2 avisos), `T6_sem_imports_extras.lean` (RC 0). Nada foi escrito na pedra, no kernel nem em `candidatas_c1\`; nada foi registrado no Mapa de Rotas nem em memória.
