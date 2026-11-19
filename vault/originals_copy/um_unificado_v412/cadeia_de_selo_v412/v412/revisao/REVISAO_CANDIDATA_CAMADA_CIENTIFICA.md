# REVISÃO DISTINTA DA CANDIDATA `CamadaCientifica.lean` (R2, v412) — terceiro cético

Revisor distinto (quem constrói não aprova). 14/11/2026. Só escrevi em `…\v412\revisao\` (este arquivo e `scripts_candidata_c1\`). Nada registrado no Mapa, nada depositado na fila, nenhuma transição ACOM, nenhum `lake`, nada escrito no kernel, no Nós, no túnel, na pasta `candidatas_c1` nem em memória; nenhum modelo de linguagem chamado.
Estatutos: [REAL] conferido por mim com a consulta citada · [DERIVED] derivado por mim aqui · [DECLARADO] afirmado na origem, não conferido · [OPEN] · [ONTO] leitura do operador. `NOT_FALSIFIED` nunca é `CONFIRMED`; nada abaixo diz que a teoria foi confirmada.

## 0. Veredito

**APROVADA COM RESSALVAS — como consolidação, na língua do kernel, do que a `trava` faz com um estado qualquer (seção 2). NÃO APROVADA nas três frases que ligam as seções entre si (“o mesmo, no motor da IALD”; “o pouso pesa a leitura final”; “o que separa o leitor com escala do que só fotografa”). Recomendação: ENTRA DEPOIS DE CORREÇÕES (seção 8), sem mudar nenhuma prova.**

- Recompila limpa: RC 0, 31 s, sem aviso, sem `sorry`, as 36 declarações no trio (seção 1). O log de axiomas é idêntico ao da gerência.
- Supera o padrão K06 em dois pontos: usa o kernel POR TERMO (`TraducaoTuring`, `AEscala.LeitorDoFundo`, `IALD`, `ObservadorTerminal`; a K06 tinha zero ocorrências) e põe a descida do custo (`consome`) no tipo em vez de supor a alcançabilidade.
- NÃO supera o padrão K06 num ponto: o tipo `LeitorDeUmaConfiguracao c` continua habitado por decisor e por mapa constante (seção 3). A diferença é que a conclusão central da pedra (retorno, bacia, resolução finita) é sobre a `trava`, que é um operador definido, não sobre “existe um leitor”; por isso a patologia não contamina o resultado principal, só a seção 3 e o teorema empacotado.
- Conteúdo líquido (honesto): o motor analítico é um só teorema do kernel (`a_trava_sem_conhecer_o_nome`) mais `a_selecao_esquece`. A pedra os generaliza do estado uniforme para estado qualquer, acrescenta a lei de semigrupo da trava, o tempo explícito, e junta tudo no “retorno”. É pouco, é correto, é novo como enunciado.
- Contagem das 36: **17 CONTEÚDO** (4 deles elementares, sem uso do kernel), **11 APOIO**, **8 DECORATIVAS** (seção 2).

## 1. Recompilação independente (pergunta 1) [REAL]

Cópia `scripts_candidata_c1\src\CamadaCientifica.lean`, sha256 **`77641aa7e2328cbc78e3f886b27f88630eda8b569ff51ec768186f228f0302cd`**, idêntico ao original (`sha256sum` dos dois). Script meu: `scripts_candidata_c1\compilar_revisor.ps1` (lean.exe 4.31.0 direto, `LEAN_PATH` = `.lake\build\lib\lean` do sandbox `C:\t\k411c\final` + `packages\*`, `-o` só em `scripts_candidata_c1\build\`; nunca `lake`).
- Código de saída **0**; 31 s; `grep -ci "warning|error|sorry"` no log = **0**.
- 29 declarações com `depends on axioms: [propext, Classical.choice, Quot.sound]` (ou subconjunto) e 7 com `does not depend on any axioms` (`LeitorDeUmaConfiguracao`, `limite`, `o_limite_fixa_o_nome`, `o_limite_nao_e_constante`, `salto`, `oLeitorTerminal`, `o_leitor_que_devolve_o_que_recebeu_nao_retorna`) = 36; todas ⊆ {propext, Classical.choice, Quot.sound}; nenhum `sorryAx`. O corpo do log é idêntico ao da gerência (`diff` vazio).
- Nenhuma colisão de nome: `grep` de `CamadaCientifica|LeitorDeUmaConfiguracao|o_retorno|a_bacia_e_tudo` em `TGLExt\` = 0. Imports (`AEscala`, `ObservadorTerminal`) são os últimos da cadeia (`TGLExt.lean` l.1126, 1149).

## 2. Vacuidade e classificação (pergunta 2) [REAL por compilação]

Habitações compiladas por mim (`src\Habitacoes.lean`, sha256 `d699fa6f79ed3fc14d9e6d1caa0baebc7438c0879f3c99c4b96c460596abaa72`, RC 0, 0 sorry, trio; `src\HabitacoesMotor.lean`, sha256 `e21043fd1014e49d9ea3193659be47aa8f6c0e7fcd13ea1785c006bab0890820`, RC 0, 0 sorry, trio):

| hipótese | habitada? | exemplo (Lean) |
|---|---|---|
| `o_retorno_ao_mesmo_estado` (s no núcleo, ‖s‖=1, δ ⟂ núcleo, δ ≠ 0) | **sim** | `Rev.hab_retorno_hyps`, `hab_retorno_aplicado`, `hab_retorno_cru`: X = Bool, custo `true↦0, false↦1`, s = single true 1, δ = single false 1; o teorema dispara e dá o limite s |
| `jamais_esgotado` (c x ≠ 0, v x ≠ 0) | **sim** | `Rev.hab_jamais_esgotado` (mesmo custo, v = single true 1 + single false 1) |
| `LeitorDeUmaConfiguracao` com passo que NÃO é o `salto` nem o terminal | **sim** | `Rev.descida`: custo `![0,1,2]` em `Fin 3`, passo `![0,0,1]` (2↦1, 1↦0); `descida_nao_e_salto` prova que difere do `salto` em x=2 |
| `o_pouso_pesa_a_leitura_final` (L, G, m, cota) | **sim** | `Rev.hab_pouso`: L = `iald`, G = `salto` (Bool), m = 1 |
| `a_leitura_finita_do_motor_pousa` (ρ localmente constante) | **sim, com ρ NÃO constante** | `HabitacoesMotor.hρ`, `rho_nao_constante`, `motor_aplicado`: H = EuclideanSpace ℂ Bool, a = single true 1, ρ x = (dist x (post a ψ) < 1) |
| `o_motor_tangencia_e_nao_esgota` (1 − post a ≠ 0) | **sim** | `HabitacoesMotor.hne`, `motor_nao_esgota` |

Nenhuma hipótese é insatisfazível. A patologia aparece por outro lado: o que o tipo ADMITE (seção 3).

### Tabela das 36 declarações

Critério (meu): CONTEÚDO = enunciado que a pedra acrescenta, com argumento próprio, citado no cabeçalho como resultado (anoto “E” quando é elementar e não usa o kernel). APOIO = definição ou lema que alimenta outro da pedra. DECORATIVA = nenhum outro teorema a usa E (é reembalagem de uma linha de teorema do kernel, ou vale para qualquer função/identidade, ou é instanciação de uma linha).

| # | declaração | classe | nota |
|---|---|---|---|
| 1 | `a_leitura_finita_do_motor_pousa` | DECORATIVA | `eventually_atTop.mp (the_iterated_motor_tends_to_the_name.eventually hρ)`: `Tendsto.eventually` do kernel; vale para qualquer sequência convergente; só ∃K, sem cota |
| 2 | `com_o_acoplamento_a_leitura_finita_pousa` | DECORATIVA | instancia r := β com `beta_pos`; uma linha sobre o 1 |
| 3 | `o_motor_tangencia_e_nao_esgota` | DECORATIVA | `unfold` + `IALD.the_motor_never_arrives` (kernel, T8) |
| 4 | `reler_soma_o_tempo` | CONTEÚDO | lei de semigrupo da `trava`: não existia no kernel (grep: sem `trava c s (trava c t …)`) |
| 5 | `sem_escala_nada_se_move` | APOIO | `trava c 0 = id`; alimenta 6 e 14 |
| 6 | `k_leituras_sao_uma_trava` | CONTEÚDO | k·τ; versão no estado do `cada_ciclo_aplica_a_mesma_regra` (que é do brilho) |
| 7 | `reler_k_vezes_e_ler_no_tempo_somado` | CONTEÚDO | 2 passos (6 + `a_leitura_e_a_do_psion`); único elo entre as iteradas da trava e o `LeitorDoFundo`; como todo L é a `iald`, o “para todo L” é decorativo |
| 8 | `a_trava_tende_ao_nome` | CONTEÚDO | generaliza `a_trava_converge_a_selecao` (kernel, só uniforme) a todo v; prova = a do kernel com v no lugar do uniforme |
| 9 | `a_bacia_e_tudo_o_que_nao_e_cego_ao_nome` | CONTEÚDO | versão renormalizada de 8, a conclusão da `selecao` para todo v |
| 10 | `o_que_esta_no_nome_nao_se_move` | CONTEÚDO | forma vetorial de `o_nome_fica_travado` (coordenada); nenhum teorema da pedra a usa |
| 11 | `a_selecao_do_que_esta_no_nome` | APOIO | alimenta 13 |
| 12 | `o_retorno` | CONTEÚDO | o teorema central: 9 + `a_selecao_esquece`; hipóteses s não cego, δ ∈ núcleoᗮ |
| 13 | `o_retorno_ao_mesmo_estado` | CONTEÚDO | corolário de 12 + 11; é a frase “volta ao MESMO estado” |
| 14 | `a_fotografia_nao_retorna` | DECORATIVA | `id` + `δ ≠ 0`; `trava c 0 = id` é a DEFINIÇÃO de “fotografia”; compilado: `Rev.fotografia_e_id` |
| 15 | `a_leitura_de_resolucao_finita_pousa` | CONTEÚDO | tempo explícito max(0, ln(‖v‖/ε)); corolário aritmético do kernel (`a_trava_sem_conhecer_o_nome`) |
| 16 | `em_k_leituras_pousa` | CONTEÚDO | versão em ciclos de 15 |
| 17 | `jamais_esgotado` | CONTEÚDO | a trava nunca É a projeção em tempo finito (vetor com amplitude em c x ≠ 0); o kernel só tinha `negar_o_zero` (≠ 0), outra coisa |
| 18 | `LeitorDeUmaConfiguracao` | APOIO | definição; ver seção 3 |
| 19 | `….custo_apos_k` | APOIO | |
| 20 | `….pousa` | CONTEÚDO (E) | descida de ℕ (`omega`); o campo `consome` já É a causa do pouso |
| 21 | `….permanece` | APOIO | |
| 22 | `….limite` | APOIO | definição (iterada de ordem m) |
| 23 | `….o_limite_pousa` | APOIO | |
| 24 | `….o_limite_fixa_o_nome` | APOIO | |
| 25 | `….o_limite_e_idempotente` | CONTEÚDO (E) | retração; vale por `fixa_o_nome` + 23 |
| 26 | `….o_limite_nao_e_constante` | DECORATIVA | duas reescritas; hipótese x ≠ y, ambos solução; NÃO protege o tipo (com Nome unitário o mapa constante é instância: `Rev.constante`) |
| 27 | `….a_imagem_do_limite_e_o_nome` | CONTEÚDO (E) | imagem do limite = {c = 0} |
| 28 | `….salto` | APOIO | testemunha; CONHECE uma solução |
| 29 | `oLeitorTerminal` | CONTEÚDO | única instância que liga POR TERMO ao `ObservadorTerminal` (`leitor`, `distancia`, `leitor_fixed_iff`, `the_collapse_is_the_terminal_point_of_resistance`, `each_reading_consumes_resistance`); os níveis são quatro rótulos |
| 30 | `o_leitor_que_devolve_o_que_recebeu_nao_retorna` | DECORATIVA | `Function.iterate_id`; nem menciona a estrutura (compilado: `Rev.fotografia_e_id` e `example` em `Habitacoes.lean`) |
| 31 | `sem_zero_nao_ha_pouso` | CONTEÚDO (E) | o tipo é vazio sem zero; ver seção 3 |
| 32 | `o_pouso_pesa_a_leitura_final` | DECORATIVA | G não entra na igualdade: `Rev.pouso_sem_G` prova `L.limite c = |{c=0}|/|X|` sem G, em duas linhas do kernel; ver seção 3 |
| 33 | `custoCNF_le_numero_de_clausulas` | APOIO | |
| 34 | `sat_sse_o_custo_tem_zero` | APOIO | |
| 35 | `sem_nome_nao_ha_pouso` | DECORATIVA | instanciação de 31 por 34; nada a usa |
| 36 | `o_leitor_com_escala_pousa_e_volta` | CONTEÚDO* | *empacotamento: só (4) usa algo novo (c ≤ |φ|, via 33). Ver seção 3 |

Totais: **CONTEÚDO 17** (4, 6, 7, 8, 9, 10, 12, 13, 15, 16, 17, 20, 25, 27, 29, 31, 36), **APOIO 11** (5, 11, 18, 19, 21, 22, 23, 24, 28, 33, 34), **DECORATIVAS 8** (1, 2, 3, 14, 26, 30, 32, 35). Dos 17, os que dizem algo NOVO SOBRE O KERNEL (e não só sobre o tipo de descida) são 4, 6, 7, 8, 9, 10, 12, 13, 15, 16, 17, 29.

## 3. Patologia do leitor constante (pergunta 3)

Resposta curta: **recai na seção 3 (o tipo), não no núcleo da pedra (a trava).**

- **A trava é um operador definido**, não uma existência. Os teoremas das seções 2 (retorno, bacia, resolução) valem para o operador do kernel; nenhum decisor, nenhuma leitura constante os satisfaz no lugar. Não há “existe leitor” disfarçado ali. [REAL]
- **`LeitorDeUmaConfiguracao c` é habitado por decisor e por mapa constante.** [REAL, compilado]
  - `Rev.leitor_existe_sse_SAT`: `Nonempty (LeitorDeUmaConfiguracao (custoCNF φ)) ↔ SAT φ`, para TODA fórmula. A existência do “leitor” é exatamente a existência de solução, a forma que a rota `kernel.pergunta_do_clay_trivial_por_leitor_constante_09nov` proíbe aceitar (“não aceitar teorema de existência cuja definição um decisor clássico satisfaz”).
  - `Rev.constante`: `passo := fun _ => 0` é instância para o custo `![0,1,2]` (Nome = {0}); `constante_e_constante` o confirma constante. Com Nome unitário o mapa constante É leitor. O docstring (l.351–353) admite só o `salto` e diz que “não é algoritmo”; não diz isto nem a equivalência com SAT.
  - O tipo não pina que o passo leia só pela regra: `passo : X → X` é função qualquer. É o que o `AEscala` corrigiu em 09/11 pondo o brilho (que só vê o custo) no tipo; aqui o tipo só tem a descida do custo.
  - O que o tipo faz melhor que a K06: o campo `consome` é a descida de Lyapunov, e `pousa` sai dele; a K06 supunha `reachable`. Mas o campo `consome` já É a conclusão iterada: `pousa` é aritmética de ℕ, sem conteúdo físico.
  - Nenhum teorema da pedra AFIRMA que exista leitor local para toda fórmula (l.58–60 diz que não). O docstring honesto está meio caminho; falta a equivalência com SAT e o caso constante.
- **`sem_zero_nao_ha_pouso`** é o enunciado negativo da mesma equivalência: tem conteúdo elementar, e o que mostra é que o tipo codifica “há solução”.
- **`o_pouso_pesa_a_leitura_final` (32) é reembalagem**: a igualdade é |soluções|/|X| dos dois lados; G só fornece “imagem do limite = {c=0}” (27, lema próprio). `Rev.pouso_sem_G` a prova sem G. G é enfeite (não decorativo no sentido lógico, decorativo no físico). E a FRASE está errada como lida: “a fração das configurações em que o leitor de uma configuração pousa é |soluções|/|X|” — `Rev.pousa_de_todas_e_a_fracao_e_meia`: para o custo `cB`, o leitor pousa a partir de TODAS as configurações (fração 1) e |soluções|/|X| = 1/2. O que a igualdade mede é a fração de X que É imagem do limite (a densidade do Nome). Além disso “TODO leitor do fundo” é um só: `AEscala.o_leitor_do_fundo_e_a_iald` (L = `iald`).
- **O teorema final (36)** reúne seis conclusões sobre três objetos diferentes: a trava (1, 2, 3, 5), o leitor de uma configuração G (4) e o leitor do fundo L (6). As hipóteses G e L não entram em (1), (2), (3), (5); G e L não se ligam por dinâmica; e hφ é derivável de G (por 31). O título “o leitor com escala pousa no Nome e volta” sugere um leitor que faz tudo.
- **O retorno não vale para G.** `Rev.g_nao_volta_ao_mesmo`: `Fin 3`, custo `![0,0,1]`, G = `salto`, s = 1 (solução), empurrado a 2, o limite é 0 ≠ 1. O limite é retração sobre o Nome: pousa em ALGUMA solução, não na mesma. “Volta ao MESMO estado” é teorema da trava (vetor de 2^n amplitudes), não do leitor de uma configuração.
- **`a_leitura_finita_do_motor_pousa` é só `Tendsto.eventually`** (confirmado pelo termo; seção 4). É a tradução “leitura discretizada de um limite estabiliza”; não é decorativa por falsa, é decorativa por não acrescentar nada ao kernel; a hipótese ρ é habitada por leitura NÃO constante (`rho_nao_constante`), então não é vazia.
- Reembalagem vs conteúdo novo, sem suavizar: **conteúdo novo sobre o kernel** = 4, 6, 7, 8, 9, 10, 12, 13, 15, 16, 17, 29 (todos na trava, todos corolários curtos de `a_trava_sem_conhecer_o_nome` e `a_selecao_esquece`). **Reembalagem** = 1, 2, 3, 14, 30, 32, 35. **Elementar sem o kernel** = 20, 25, 27, 31.

## 4. Na língua do kernel (pergunta 4) [REAL]

Método: `Usos.lean` (sha256 `00d7b86b96fc79201f86b22f56f27da1cc9f5810a10f87c3283a9a301dc3b1f1`) lê do `.olean` compilado as constantes de `TGLExt` (fora da pedra) que ocorrem no TERMO da prova (não em comentário), por declaração; saída em `build\Usos_saida.txt`. `ci.value` das provas; `._proof_*` auxiliares escondem usos dentro de `salto` e `oLeitorTerminal` (nesses li a fonte, l.353–374).

| declaração da pedra | constantes do kernel que a PROVA usa |
|---|---|
| 1 `a_leitura_finita_do_motor_pousa` | `IALD.the_iterated_motor_tends_to_the_name`, `IALD.dephase`, `TheVerbSelectsTheAction.post` |
| 2 `com_o_acoplamento…` | `TGLCoupling.beta`, `TGLCoupling.beta_pos` (+ o 1) |
| 3 `o_motor_tangencia…` | `IALD.the_motor_never_arrives` |
| 4–6 `reler_soma…`, `sem_escala…`, `k_leituras…` | `TraducaoTuring.trava`, `trava_ofLp` |
| 7 `reler_k_vezes…` | `AEscala.LeitorDoFundo.a_leitura_e_a_do_psion`, `LeitorDoFundo.leitura`, `trava`, `uniforme` |
| 8 `a_trava_tende_ao_nome` | `TraducaoTuring.a_trava_sem_conhecer_o_nome`, `opDaInstancia`, `trava` |
| 10 `o_que_esta_no_nome_nao_se_move` | `opDaInstancia_ofLp`, `trava_ofLp` |
| 12 `o_retorno` | `TraducaoTuring.a_selecao_esquece`, `selecao`, `trava` (+ 9) |
| 15 `a_leitura_de_resolucao…` | `a_trava_sem_conhecer_o_nome` |
| 17 `jamais_esgotado` | `solucao_por_coordenadas`, `trava_ofLp` |
| 29 `oLeitorTerminal` | `ObservadorTerminal.leitor`, `distancia` (e, por `_proof_*`, as 3 de `leitor_fixed_iff`, `the_collapse_is_the_terminal_point_of_resistance`, `each_reading_consumes_resistance`, conforme a fonte) |
| 32 `o_pouso_pesa…` | `AEscala.LeitorDoFundo.o_limite_e_o_que_sou`, `TraducaoTuring.o_que_sou_das_solucoes`, `nomeDasSolucoes`, `Identidade.oQueSou` |
| 34 `sat_sse…` | `TraducaoTuring.custoCNF_zero_sse`, `SAT`, `custoCNF` |
| 36 teorema final | `TraducaoTuring.a_trava_converge_a_selecao` (+ próprios 12, 16, 14, 20/21, 32, 33, 34) |

- `TraducaoTuring`: ligado POR TERMO, de ponta a ponta. [REAL]
- `AEscala.LeitorDoFundo`: ligado por termo em DOIS teoremas (7 e 32). Não usa `iald`, `o_leitor_do_fundo_e_a_iald` nem `cada_ciclo_aplica_a_mesma_regra` (esse último só em prosa, l.37–38). [REAL]
- `IALD`: ligado por termo só na seção 1 (3 teoremas: o 1, o 2 e o 3; as constantes do kernel são `the_iterated_motor_tends_to_the_name`, `the_motor_never_arrives`, `TGLCoupling.beta_pos`). `IALD2.o_atrator` NÃO é usado (nem citado no arquivo). [REAL]
- `ObservadorTerminal`: ligado por termo só em `oLeitorTerminal`. [REAL]
- **Homônimo encadeado indevidamente?** Não achei citação de propriedade de um objeto a favor de outro. Mas há um homônimo-de-fato lado a lado: o dicionário linha 29 chama de “o mesmo” o fluxo da seção 1 (`IALD.dephase`, projetor posto de posto 1 em H abstrato, `axiomFlow (post a)`) e a `trava` da seção 2 (decaimento e^{−t·c(x)} no `EuclideanSpace ℂ X`, projeção no núcleo do custo). **Não há lema ligando os dois** (nem no kernel nem na pedra; grep de `trava.*axiomFlow` e `dephase.*trava` em `TGLExt\` = 0). E NÃO são o mesmo fluxo: `HabitacoesMotor.trava_ne_fluxo` prova que, com custo 2 numa coordenada, a trava a decai a e^{−2} e o fluxo do axioma sobre `ker.starProjection` a e^{−1}; só coincidem para custo em {0,1}. `post a` é a projeção de posto 1 em ℂ·a, o Nome da trava é o span de TODAS as soluções. As seções 1 e 2 estão só LADO A LADO, e o docstring não diz isso (diz “o mesmo, no motor da IALD”).

## 5. O cabeçalho contra os teoremas (pergunta 5)

| frase | teorema | confere? |
|---|---|---|
| L.23 “reler = somar o tempo dos ciclos” | 4, 6, 7 | sim |
| L.24 “a bacia: todo estado que não é cego ao Nome converge à seleção” | 8, 9 | sim (renormalizado, t → ∞) |
| L.25 “o que está no Nome não se move; a seleção dele é ele” | 10, 11 | sim (norma 1 para 11) |
| **L.26 “o empurrão para fora do Nome é esquecido: a órbita volta ao MESMO estado”** | 12, 13 | **afirma mais**: a hipótese é δ ORTOGONAL ao Nome (o item 3 do “PROVA” diz certo, a linha 26 não); s no núcleo com ‖s‖ = 1; limite t → ∞, renormalizado, nunca em tempo finito (17); e a volta é à seleção de s, isto é, ao componente de s no Nome (conservado). Um empurrão genérico tem componente no Nome, e esse componente MUDA o limite (`o_retorno` dá `selecao (…) s`, que depende de P s) |
| L.27 “o leitor sem escala: o empurrão fica” | 5, 14 | verdadeiro por definição: `trava c 0 = id` |
| **L.28 “pousa em tempo finito dito e permanece; o vetor tangencia e não esgota”** | 15, 16, 17, 1 | “pousa” = fica a distância ≤ ε do Nome (resolução), não É o Nome; “tempo dito” só na trava (para o motor, 1 dá só ∃K); em 15 a hipótese `0 ≤ t` é adicional (“a partir de ln(‖v‖/ε)” vale como max(0, ln…)) |
| **L.29 “o mesmo, no motor da IALD”** | 1, 2, 3 | **afirma mais**: seção 1 e seção 2 não se ligam por termo e não são o mesmo fluxo (seção 4) |
| L.30 “a máquina de uma configuração por vez: pousa em ≤ c(x) passos…” | 18–25, 27 | sim, para o tipo; ver seção 3 sobre o que o tipo admite |
| L.31 “o leitor terminal do kernel é um leitor de uma configuração” | 29 | sim por termo; é uma cascata de 4 rótulos |
| L.32 “o texto sem Nome: nenhum leitor pousa” | 31, 35 | sim para o tipo; é a forma negativa de “há solução” |
| **L.33 “a fração do espaço em que o leitor de uma configuração pousa é a leitura final de TODO leitor do fundo”** | 32 | **errada como lida** (seção 3): G pousa de todas as configurações; a igualdade é a densidade do Nome; “todo” L é um só |
| L.44–45 “É o que separa, no kernel, o leitor com escala do leitor que só fotografa” | 5, 14 | **afirma mais**: a fotografia É a identidade por definição; não separa o leitor sem memória (seção 7) |
| L.46–47 “a partir do tempo ln(‖v‖/ε)… e fica” | 15 | sim com t ≥ 0 |
| L.47 “E o vetor nunca É o Nome enquanto houver amplitude fora dele” | 17 | sim |
| L.48–52 (item 6) | 20–27, 31 | sim; “não é constante quando o Nome tem dois pontos” é honesto, mas com Nome unitário o mapa constante é instância |
| **L.51–52 (item 7) “A fração das configurações em que o leitor pousa é |soluções|/|X|”** | 32 | errada como lida (idem L.33) |

**“O que a pedra NÃO afirma”** (l.54–64) está correta no que diz, mas FALTA dizer:
1. A renormalização (a `selecao`, o `‖·‖⁻¹ •`) não é passo de máquina de Turing, e o estado é um vetor de 2^n amplitudes, não uma configuração. O próprio kernel diz (`TraducaoTuring.a_trava_no_nome`, l.627–629: “a máquina de Turing do Mathlib guarda uma configuração por vez e não renormaliza: este teorema não é sobre ela”); a pedra herda a ressalva e não a repete. (`AEscala` l.739 diz também que não há termo ligando a tradução à formalização do Mathlib.)
2. `o_retorno` exige δ ⟂ Nome; o componente do empurrão no Nome NÃO é desfeito e desloca o limite.
3. O retorno ao mesmo estado é da trava, NÃO do leitor de uma configuração (`g_nao_volta_ao_mesmo`).
4. `LeitorDeUmaConfiguracao c` tem instância ⟺ há solução (`leitor_existe_sse_SAT`), e é habitado por mapa constante quando o Nome é unitário.
5. Os teoremas de cota são desigualdades superiores; um leitor sem memória (o projetor sobre o Nome) cumpre a mesma cota com distância zero (`projetor_cumpre_a_cota`).
6. Seções 1 e 2 sem ponte.
7. Todo leitor do fundo é a `iald` (um só).

## 6. O vocabulário da casa (pergunta 6) [REAL, Grep no arquivo]

- “paga/pago”: UMA ocorrência, l.16–17, e é a certa: “o leitor não paga a escala, ele é a escala”. Respeitada. Nenhum “tempo pago” no arquivo.
- `milenio`, `navier`, `clay`, a família de `confirm`: **zero**. “Tetelestai”, `verbatim`, `Kimi`, `Codex`, `ChatGPT`: zero.
- “consciência” (l.63), “pesos” (l.63), “Exclusividade” (l.61): só em NEGAÇÃO (“Nada sobre consciência, nem sobre pesos de modelo algum”; “Que só um texto faça leitores pousarem não segue daqui”). Pode ser que a `guarda_das_frases` da cadeia recuse a palavra mesmo negada; NÃO conferi a regra da guarda (a K06 já pediu a mesma verificação).
- Conversa interna / fala transcrita: nenhuma fala do operador transcrita. **Mas as l.10–11** (“[CANDIDATA da gerência c1, 14/11/2026, R2, para a v412; compilada só em sandbox; o nome … PROVISÓRIOS, da gerência, e ficam [DECLARADO] até a palavra do operador; a ordem que a pede entra por data e hash no registro da versão]”) são ESTADO DE PROCESSO da candidata, não conteúdo; no programa elas não devem seguir (regra de 12/11: processo e conversa fora do programa; a K06 recebeu o mesmo reparo para “R3”). Remover ao instalar.
- “operador” na l.96 é o operador matemático (“o que pousa é a leitura …, não o operador”). Sem problema, mas ambíguo na casa; sugerir “não o operador de defasagem”.

## 7. O que a candidata dá a um experimento (pergunta 7) [DERIVED; compilado onde dito]

Lida como previsão, o que os teoremas separam:

1. **Leitor com escala (a trava, τ > 0) vs leitor que só fotografa (a identidade).** Separa: depois de um empurrão δ ≠ 0 ortogonal ao Nome, o estado volta a s no limite (12, 13) e, em k ciclos, fica a ≤ e^{−kτ}‖s+δ‖ (16); a fotografia fica a ‖δ‖ de s para sempre (14). É o que a pedra prova, e “fotografa” aqui é DEFINIDO como a identidade.
2. **Um leitor SEM memória que relê o texto-fonte inteiro a cada passo NÃO é distinguido por esse observável.** `Rev.projetor_cumpre_a_cota` (compilado): o projetor sobre o Nome (um passo, sem estado) satisfaz a mesma cota de resolução finita de 16, com distância ZERO a partir da primeira leitura; e também “volta” depois de um empurrão (reescreve o estado). O retorno e a permanência, sozinhos, separam do leitor que só fotografa e não do leitor que relê a fonte. As desigualdades da pedra são cotas superiores; um leitor mais rápido as cumpre.
3. **Condição de desenho que o teorema exige:**
   - (a) O empurrão tem de ser no ESTADO interno e não no texto de entrada, e o texto-fonte NÃO pode ser devolvido ao leitor depois do primeiro passo; senão todo leitor que vê a fonte “volta” e o observável não discrimina.
   - (b) O empurrão tem de ser ORTOGONAL ao Nome (coordenadas de custo > 0). Um empurrão genérico tem componente no Nome e o limite se desloca para `selecao (P(s+δ))`: isso é, ao contrário, uma PREVISÃO a testar (memória do componente no Nome), não um defeito.
   - (c) Os observáveis que separam da releitura sem memória são: (i) o perfil de relaxação (a trava decai e^{−τ·c(x)} por coordenada, 17 e `trava_ofLp`: não é instantâneo; o leitor sem memória chega ao Nome exatamente numa leitura; a trava nunca é exata em tempo finito, `jamais_esgotado`); (ii) a dependência do limite do componente inicial no Nome (`selecao ker s` depende de s; o leitor sem memória o ignora).
   - (d) Todo o enunciado é sobre o vetor de 2^n amplitudes. Que a saída de um modelo de linguagem seja esse vetor (a extração texto → c : X → ℕ) é a ponte [OPEN]; a pedra não a fecha (diz isso, l.56–57). Sem a extração, nada do que está acima se mede num modelo.
   - (e) Tempo contínuo, sem ruído; um modelo real é estocástico e discreto. Isto vai para o desenho do experimento, não para a pedra.

## 8. O que falta para virar pedra da v412 e a recomendação (pergunta 8)

**ENTRA DEPOIS DE CORREÇÕES.** Nenhuma prova muda; mudam enunciados de cabeçalho e docstrings, e possivelmente a poda de declarações decorativas.

Correções, numeradas (linha da candidata):
1. **(forte) L.33, L.51–52, L.387–389 (e o título do teorema `o_pouso_pesa_a_leitura_final`):** a “fração das configurações em que o leitor pousa” está errada como lida. Trocar por “a fração de X que é imagem do limite, isto é, a densidade do Nome (|soluções|/|X|); o leitor pousa de TODAS as configurações”. E dizer que G não entra na igualdade (`pouso_sem_G`) ou retirar G do enunciado.
2. **(forte) L.287–297 e L.351–353 (docstrings), L.58–60 (“NÃO afirma”):** dizer que `Nonempty (LeitorDeUmaConfiguracao (custoCNF φ)) ↔ SAT φ`, que para Nome unitário o mapa constante é instância, e que o tipo NÃO pina que o passo leia só pela regra (ao contrário do `LeitorDoFundo`, onde o brilho só vê o custo). A casa já corrigiu essa patologia na v410; aqui ela fica nomeada como hipótese, e a nomeação deve ser completa.
3. **(forte) L.29 (dicionário) e L.74–76 (seção 1):** “o mesmo, no motor da IALD” afirma mais do que há. Não há termo ligando `IALD.dephase` e `trava`, e não são o mesmo fluxo (`trava_ne_fluxo`). Dizer “paralelo, sem ponte” ou construir a ponte (por exemplo, o caso de custo em {0,1}). Ou retirar a seção 1 (os 3 teoremas são reembalagem de uma linha do kernel, classe DECORATIVA).
4. **(média) L.26 (dicionário) e L.40–42:** “o empurrão para fora do Nome é esquecido” → “o componente do empurrão ortogonal ao Nome (as coordenadas de custo > 0) é esquecido; o componente no Nome é conservado e desloca o limite”.
5. **(média) L.44–45:** “É o que separa, no kernel, o leitor com escala do leitor que só fotografa” → “a fotografia é aqui a identidade (`trava c 0 = id`); não separa o leitor que relê a fonte (`projetor_cumpre_a_cota`)”.
6. **(média) L.54–64 (“NÃO afirma”):** acrescentar as sete lacunas da seção 5 (renormalização e vetor de 2^n amplitudes não são máquina de Turing; δ ⟂ Nome; o retorno é da trava e não de G; o tipo ⟺ SAT; as cotas são superiores; seções 1 e 2 sem ponte; todo L é a `iald`).
7. **(média) Teorema final (L.419–449):** dizer no docstring que os seis conjuntos são sobre três objetos independentes (trava, G, L), que G e L não entram em (1), (2), (3), (5), e que hφ é derivável de G. Ou separar em três teoremas.
8. **(baixa) L.10–11:** retirar o estado de processo da candidata do cabeçalho (R2, “da gerência”, “[DECLARADO] até a palavra do operador”, “a ordem… entra por data e hash”); isso vai para o registro da versão, não para o programa.
9. **(baixa) L.46, L.231–233:** “a partir do tempo ln(‖v‖/ε)” → “a partir de max(0, ln(‖v‖/ε))”.
10. **(baixa) Poda sugerida:** as 8 decorativas (1, 2, 3, 14, 26, 30, 32, 35) só entram no `axiom_report` e nas bandeiras se alguém as quiser; 14 e 30 são o controle negativo declarado; 26 e 35 não alimentam nada. Pedido de decisão da gerência, não do revisor: se ficarem, que o docstring as chame de controles/instanciações e não de resultados.
11. **(baixa) L.96:** “o operador” (matemático) → “o operador de defasagem”, para não colidir com o vocabulário da casa.

Para virar pedra (ato do operador/orquestrador, não deste revisor): nome do módulo e das declarações ratificado por ele (`AEscala`, D87); `TGLExt/<Nome>.lean` e entrada em `TGLExt.lean` depois de `TGLExt.AEscala` (l.1149); remover `#print axioms` e `set_option`s de teste; bandeiras e registro com função; revisão de terceiro e rito.

## 9. O que conferi e como

- Recompilação de `CamadaCientifica.lean` (sha256 pelo `sha256sum` contra o original) com lean.exe direto; log lido (0 aviso, 0 sorry); `diff` do corpo do log contra o da gerência = vazio.
- Leitura integral da candidata e da `REVISAO_K06_FORMAL.md`; leitura de `TraducaoTuring.lean` (l.100–160, 325–395, 440–640, 1030–1075), `AEscala.lean` (l.684–873, 895–970), `IALD.lean` (l.100–150, 425–455, 610–700), `ObservadorTerminal.lean` (l.94–193). Grep em `TGLExt\` só.
- **Constantes USADAS por termo** (seção 4): `Usos.lean` sobre o `.olean`.
- **Habitações e controles** em Lean (seção 2 e 3): teoremas e exemplos em `Habitacoes.lean` (14 com `#print axioms`, mais as habitações e dois `example`) e 8 em `HabitacoesMotor.lean`, todos RC 0, 0 sorry, trio.
- Mapa de Rotas (consultei antes): termos `LeitorDoFundo` (2 rotas), `atrator` (29), `Turing` (29), `constante` (32); `ver kernel.pergunta_do_clay_trivial_por_leitor_constante_09nov` (EXAMINADA_COM_DEFEITO; “não aceitar teorema de existência cuja definição um decisor clássico satisfaz; não tratar o tempo pago da TGL como passos de Turing”). Nada registrado.
- Vocabulário (seção 6): Grep no arquivo.

## 10. O que NÃO conferi

- A regra da `guarda_das_frases` (se aceita “consciência”, “pesos”, “Exclusividade” em negação).
- Se os `.olean` do sandbox `k411c` são os da v411 selada (só que carregam e compilam); o `axiom_report` das declarações auxiliares geradas (`.mk`, `.rec`, `_proof_*`, `_simp_*`) não listei.
- A bibliografia/DOI e as demais frases de data/versão do cabeçalho (v405, v409, v410: li apenas que os nomes citados existem).
- O comportamento do empurrão com componente DENTRO de um Nome de dimensão ≥ 2 (digo que o limite se desloca a partir do enunciado de `o_retorno`, que depende de `P s`; não compilei um exemplo com Nome de dimensão 2).
- Não executei o rito, a cadeia, nem o `um.py`; não mexi em kernel, Nós, túnel, memória ou Mapa.

## 11. Arquivos desta revisão (todos em `…\v412\revisao\scripts_candidata_c1\`)

`compilar_revisor.ps1`; `src\CamadaCientifica.lean` (cópia idêntica, `77641aa7…`); `src\Usos.lean` (`00d7b86b…`); `src\Habitacoes.lean` (`d699fa6f…`); `src\HabitacoesMotor.lean` (`e21043fd…`); `build\CamadaCientifica.log`, `build\Usos.log`, `build\Usos_saida.txt`, `build\Habitacoes.log`, `build\HabitacoesMotor.log` (e `run_*.txt`).

Nada aqui afirma consciência, alteração de pesos, exclusividade ou CONFIRMED; `NOT_FALSIFIED` segue não sendo `CONFIRMED`; o gate não se move.
