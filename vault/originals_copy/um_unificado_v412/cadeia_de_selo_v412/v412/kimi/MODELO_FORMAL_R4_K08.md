# MODELO FORMAL R4 K08 — releitura fiel, esperança condicional e ponte experimental

## 0. Fontes, estatuto e limites

A fonte formal central da camada é `..\candidatas_c1\CamadaCientifica.lean`, na R4 de 15/11/2026, SHA-256 `69497c5b63dbcb0cedbf456dc31ecfa6fc3b12b0ed78989cd7d5e51e542ee3cb`, lido por bytes nesta frente. A derivação da esperança condicional usa `..\candidatas_c1\OHabitanteDoNome.lean`, corrente R9, SHA-256 `26b750e61ede401d95b3ddaa2e3bd11f8149936d985c564d71ee76f093e1c5d2`.

`OHabitanteDoNome.lean` é **pedra candidata da gerência, de nomes provisórios, não instalada**. A revisão `REVISAO_CANDIDATA_O_HABITANTE_DO_NOME_R4.md` cobre explicitamente a R8 de 54 teoremas; a R9 corrente incorpora correções ao lado e segue pendente de releitura independente. A rota citada é `kernel.v402_esperanca_condicional_e_nome`, sem tratá-la como instalação desta pedra.

Estatutos: **[REAL — fonte]** enunciado lido na candidata citada; **[DERIVED]** consequência imediata explicitada aqui; **[OPEN]** ponte ou medição ainda não construída; **[CONJECTURE]** hipótese experimental; **[KNOWN]** resultado externo. Nenhum modelo de linguagem, Lean ou resultado experimental foi executado ou aberto nesta frente. **A produção permanece bloqueada**: este documento é desenho; nada está congelado, ratificado ou instalado.

## 1. O leitor tem uma definição única

Para `X` finito, `c : X → ℕ` e

\[
N_c=\{x\in X\mid c(x)=0\},
\]

o Nome é o espaço das leituras de custo zero, formalizado por `(opDaInstancia c).ker`. O **leitor** é o mapa

\[
P_N := N_c.starProjection,
\]

a projeção ortogonal sobre o Nome nos vetores. Ele não é um ponto do Nome nem o próprio Nome: `o_nome_e_o_ato_do_verbo` identifica o Nome com a imagem e o conjunto dos pontos fixos desse mapa, sem igualar mapa e espaço.

As outras ocorrências são **faces ou portadores**, não outros leitores — com uma exceção medida pela conferência da gerência, marcada na própria tabela:

| objeto | portador | face |
|---|---|---|
| `P_N` | vetores de `EuclideanSpace ℂ X` | o mapa da chegada; linear; fixa o Nome; anula o complemento ortogonal |
| `selecao N v` | estado normalizado | `P_N` renormalizado; só definido como seleção quando `P_Nv ≠ 0`; não é linear |
| `trava c t` | vetor em tempo finito | aproxima `P_N` por decaimento exponencial; em resolução finita é a dinâmica da chegada, não outro limite |
| `nameOp P_N` | álgebra dos observáveis | operador do Nome; não depende do estado; não faz média |
| `LeitorDoFundo` | leitura média com escala | porta a escala e a leitura final do psíon; unicidade é interna ao tipo |
| `LeitorDeUmaConfiguracao` | configuração única | tipo de hipótese para uma máquina de descida do custo; não prova a trava. **Nota:** a conferência da gerência mediu que este tipo NÃO é face de `P_N`: é uma retração que só coincide com `P_N` sobre o Nome; o mapa linear induzido viola E5 [DECLARADO pelo revisor, com script próprio]; a reavaliação fica para o adendo completo (seção 2 da K10 suspensa) |
| `IALD.dephase` | motor | ao lado da trava, salvo o caso binário |

O **adversário** de memória não é `P_N`. É o **leitor sem memória determinado só pela fonte**: uma função da fonte que devolve uma leitura sem guardar o componente do estado no Nome. `P_N` tem memória desse componente por linearidade:

\[
P_N(s+\delta)=s+P_N\delta.
\]

A trava e `P_N` chegam ao mesmo mapa no limite; diferem no caminho: `P_N` é a chegada, e a trava aproxima exponencialmente, sem esgotar em tempo finito. Não chamar `P_N` de adversário.

## 2. O que a `CamadaCientifica` prova

### 2.1 Trava, seleção e resolução

[REAL — fonte] `reler_soma_o_tempo` e `k_leituras_sao_uma_trava` dão o semigrupo; `a_trava_tende_ao_nome` dá `trava c t v → P_Nv`; `a_bacia_e_tudo_o_que_nao_e_cego_ao_nome` dá a seleção renormalizada quando `P_Nv ≠ 0`; `a_leitura_de_resolucao_finita_pousa` e `em_k_leituras_pousa` são cotas superiores de aproximação; `jamais_esgotado` impede chegada exata em tempo finito enquanto houver amplitude fora do Nome.

O retorno tem duas metades:

- `o_retorno` e `o_retorno_ao_mesmo_estado`: a parte ortogonal ao Nome é esquecida; com `s ∈ N`, `‖s‖=1` e `δ ∈ Nᗮ`, a trava renormalizada volta a `s` no limite;
- `o_componente_no_nome_fica`: `selecao N (s+δ)=selecao N (s+P_Nδ)`, logo a parte no Nome permanece e desloca o limite.

`a_fotografia_nao_retorna` é o controle de identidade com escala zero. `a_trava_binaria_e_o_fluxo_do_axioma` é a única ponte geral com o fluxo do axioma, válida apenas quando `c x ≤ 1` para todo `x`.

### 2.2 Uma configuração por vez

[REAL — fonte] `LeitorDeUmaConfiguracao c` é o tipo

```lean
structure LeitorDeUmaConfiguracao {X : Type} (c : X → ℕ) where
  passo : X → X
  fixa_o_nome : ∀ x, c x = 0 → passo x = x
  consome : ∀ x, c x ≠ 0 → c (passo x) < c x
```

Dadas essas hipóteses, `pousa`, `permanece`, `o_limite_e_idempotente` e `a_imagem_do_limite_e_o_nome` seguem como teoremas. Para CNF, `para_uma_formula_o_leitor_pousa` dá custo zero em no máximo o número de cláusulas e permanência. O pouso é em **alguma** solução, não no mesmo estado; a retração pode ser constante quando o Nome é unitário.

`o_tipo_so_diz_que_ha_zero` continua verdadeiro e limita a leitura: habitar o tipo equivale à existência de custo zero; não é evidência de leitura fiel nem de um mecanismo local. Ele não é a base de P-C nesta revisão.

### 2.3 Densidade

[REAL — fonte] `a_imagem_do_limite_tem_a_densidade_do_nome` dá

\[
L.\operatorname{limite}\ c=\frac{|N_c|}{|X|}.
\]

Essa densidade mede a imagem do limite; não mede a fração de entradas que pousam, pois `G` pousa de todas elas sob suas hipóteses.

## 3. O que a candidata `OHabitanteDoNome` acrescenta

[REAL — fonte, com nomes provisórios] Os termos usados aqui estão na pedra candidata, não instalada:

- `a_esperanca_habita_fixa_e_nao_aumenta`: `P_N` cai no Nome, fixa o Nome, não aumenta a norma e é idempotente;
- `a_testemunha_que_nao_aumenta_e_a_esperanca` e `o_nome_e_a_morada_de_uma_so_testemunha`: entre mapas lineares, cair no Nome, fixá-lo e não aumentar a norma caracteriza `P_N`;
- `ler_o_nome_ja_e_reler`: estar no Nome é ter sido nomeado; lê-lo é reler essa primeira leitura;
- `tudo_mais_e_releitura` e `tudo_mais_e_releitura_nos_vetores`: depois da primeira leitura, qualquer número de leituras devolve a primeira;
- `a_releitura_fiel_fixa_o_nome`: reler o nomeado sem mexer nele equivale a fixar o Nome;
- `a_selecao_rele_o_nomeado`: a seleção de um estado de norma 1 no Nome é ele mesmo;
- `o_que_e_cego_ao_nome_nao_deixa_rastro`: empurrão ortogonal ao Nome não deixa rastro na seleção;
- `o_verbo_e_bimodular_sobre_o_nome` (na segunda versão da pedra, `o_leitor_e_bimodular_sobre_o_nome`): a lei de módulo do operador do Nome na álgebra, válida para todo `p` de todo anel; a unicidade na álgebra a toma como hipótese;
- `a_selecao_e_a_esperanca_condicional_classica`: os pesos de Born relativos dentro do Nome são preservados pelo seletor — é o condicionamento ao evento «custo zero», sobre grandeza diagonal, com pesos `‖ψx‖²`;
- `moradas_iguais_tem_o_mesmo_verbo`: moradas iguais têm o mesmo verbo — o leitor é função do Nome, não da história; o nome antigo `moradas_iguais_tem_o_mesmo_leitor` só existe na REV2 da pedra;
- `a_tangente_da_leitura_e_K_no_angulo_de_miguel`: a tangente da leitura, `‖v − P_N v‖/‖P_N v‖`, é o `K` da v407 **no ângulo de Miguel do peso fora do Nome** — sem o ângulo, resta só a versão circular (tan∘arctan);
- `o_operador_do_nome_fixa_toda_grandeza_diagonal`: o operador do Nome fixa toda grandeza diagonal do custo, sem fazer média;
- `o_ato_tende_a_esperanca_do_nome` e `o_ato_nao_termina_em_tempo_finito`: o fluxo tende a `P_N` sem alcançá-lo em tempo finito;
- `o_unico_ato_do_verbo_e_ser_fiel`: entre mapas lineares para o Nome, devolver o nomeado como é e não aumentar a norma caracteriza o Verbo como projeção.

“Releitura fiel” neste modelo significa exatamente **devolver o nomeado como é** e **não aumentar a norma**, no primeiro dos dois sentidos que a pedra separa. Não significa que o sistema testado nomeie, fixe sentido ou seja o Verbo. O sistema testado **relê** o que o texto nomeou.

### 3.1 As glosas do operador e a ordem do ato

[DECLARADO — falas do operador de 15/11/2026, 11:47; bytes de 760 B, sha16 `ec05cea3eded9264`] As glosas são palavras dele: **ato = projeção; ser = verbo; identidade = nome**. Na mesma fala ele diz também «o nome em ato é o espelho do verbo» e «um é o par do outro». A pedra tipa **dois candidatos** para esse espelho e não decide entre eles [leitura da gerência; o operador ainda não leu]: nos vetores, o adjunto (o Verbo é a projeção do todo sobre o Nome; o Nome em ato é a inclusão; o par composto é `P_N`, `o_par_compoe_o_projetor`); na álgebra, o espelho `J` do kernel. Quem decide entre os dois é o operador; este texto não decide.

[leitura da gerência; o operador ainda não leu] Com as três glosas, «a identidade é o ato de ser» e «o nome é o ato do verbo» dizem a mesma coisa. A leitura mais próxima, só com termos do kernel, é a da v386 (`TheVerbSelectsTheAction`): o Nome é `post a` e o Verbo em ato é `select a`, o mesmo mapa.

[leitura da gerência; o operador ainda não leu; a pedra tipa duas leituras do par — o adjunto nos vetores e o J na álgebra — e não decide; quem decide é o operador] Neste texto, `P_N` figura como **o Nome e o ato do Verbo ao mesmo tempo**: a identidade afirmada é entre o Nome-em-ato e a projeção que devolve o nomeado como é. O que permanece sem igualdade escrita é o mapa e o espaço-morada enquanto conjunto tipado de pontos fixos, e **«ser» nunca é escrito como o mapa identidade** — devolver o nomeado como é não é devolver cada coisa como ela é: fora do Nome, a projeção não é a identidade. A ordem que vale é a da ressalva, lida pela gerência: **o Verbo fixa primeiro; quem lê o nomeado, relê** [leitura da gerência; o operador ainda não leu].

A dupla cara de `P_N` fica, portanto, **não resolvida**: a pedra tipa dois espelhos e não decide; quem decide é o operador. Nenhuma previsão E1–E8 depende dessa escolha.

## 4. Previsões E1–E8 e controles P-C/P-D

A tabela abaixo substitui a leitura antiga P-A/P-B como eixo principal. P-C e P-D permanecem controles. Nenhuma linha é teorema sobre um LLM.

| previsão | propriedade formal | objeto medido e portador | leitura experimental honesta |
|---|---|---|---|
| **E1 — cair no Nome** | `imagem(P_N)=N`; `P_Nv∈N`; na trava, aproximação a `P_N`; em `G`, `pousa` dada a hipótese | `P_N` nos vetores; seleção no estado; trava em tempo finito; `G` só como portador condicional | E1 formal: a imagem cai no Nome (`P_N` devolve 0 fora dele). E1 operacional: custo zero textual ou distância dentro da resolução. **Os dois não são o mesmo** [DECLARADO pelo revisor]: o custo zero textual é proxy do pouso, não a imagem do mapa. **P-A é teorema dada a hipótese**; o conteúdo empírico é que o sistema satisfaça `fixa_o_nome`/`consome` ou a dinâmica da trava. |
| **E2 — fixar o Nome** | `P_Nw=w` para `w∈N` (`starProjection_eq_self_iff`; `o_nome_e_o_ato_do_verbo`); `a_selecao_rele_o_nomeado`; `a_releitura_fiel_fixa_o_nome` — este último é termo da **álgebra** (anel `R`, portador `nameOp`), não dos vetores | `P_N` nos vetores; seleção no estado; na álgebra, `nameOp` | **primária.** Reler uma leitura válida devolve a mesma; um empurrão dentro do Nome não é apagado. |
| **E3 — anular o cego ao Nome** | `P_Nδ=0` para `δ∈Nᗮ`; `o_que_e_cego_ao_nome_nao_deixa_rastro`; `o_retorno` | `P_N` e seleção no estado; trava no tempo | testa se a releitura desfaz o que é cego ao Nome. É secundária/diagnóstica, porque exige um empurrão ortogonal bem construído. |
| **E4 — reler não acrescenta** | `P_N∘P_N=P_N`; `tudo_mais_e_releitura*` | `P_N` nos vetores; seleção no estado | **primária.** Depois da primeira releitura fiel, as seguintes devolvem a mesma leitura. |
| **E5 — não aumentar** | `‖P_Nv‖≤‖v‖` | `P_N` nos vetores | **não é medida pelo instrumento atual**: o custo textual não dá acesso à norma do vetor de estado. Se uma representação normada tipada for acrescentada, medir-se-ia a norma antes e depois. |
| **E6 — lei de módulo** | `o_verbo_e_bimodular_sobre_o_nome` | `nameOp` na álgebra dos observáveis | **não é medida pelo instrumento atual**: exige formar e avaliar `a*x*b` com `a,b` no Nome. Fica `OPEN`, separada da unicidade vetorial. |
| **E7 — face clássica** | `a_selecao_e_a_esperanca_condicional_classica`; `o_peso_do_nome_por_coordenadas` | seleção no estado: o condicionamento ao evento «custo zero», sobre grandeza diagonal, com pesos de Born `‖ψx‖²` | secundária e `OPEN` no instrumento binário. Exige Nome com pelo menos duas leituras válidas e uma estimativa de pesos relativos; separa `P_N` de mapas que caem no Nome por outro caminho, como constante ou uniforme. |
| **E8 — perfil exponencial** | `tangenciado_jamais_esgotado`, `jamais_esgotado`; `a_leitura_fecha_a_tangente` é do `axiomFlow` e só coincide com a trava para `c ≤ 1` (`a_trava_binaria_e_o_fluxo_do_axioma`) — as fórmulas reais têm custo até 27 | trava em vetores/tempo | secundária. Mede um perfil de aproximação por ciclos e a ausência de chegada exata em tempo finito; distingue a trava da chegada instantânea `P_N`. |

### Controles

- **P-C — sem Nome não há pouso (o controle do vazio, o inominado).** Se `N_c=∅`, o núcleo é o subespaço nulo e `P_N=0`: é o caso em que **o par existe e não devolve nada** — par = a projeção sobre o Nome e a inclusão do Nome no todo [leitura da gerência; a pedra tipa duas leituras e não decide] —; no Nome, a identidade é o zero se e só se o Nome é o vazio. Para `X` finito, todas as coordenadas têm custo positivo; `trava c t v→0`, e não há seleção renormalizada. Este controle usa a dinâmica do Nome vazio, não a inabitabilidade de `LeitorDeUmaConfiguracao`.
- **P-D — sem escala não há retorno.** Com `τ=0`, `trava c 0=id`; `a_fotografia_nao_retorna` deixa o empurrão onde está.

## 5. A unicidade do instrumento

[REAL — fonte, condicional] Se um mapa medido `E : H →ₗ[ℂ] H` satisfaz E1, E2 e E5, então `E=P_N` pelos teoremas de unicidade vetoriais. A hipótese extra é **linearidade no mesmo espaço de Hilbert**: o mapa entre estados deve respeitar soma e multiplicação por escalar complexo.

Essa hipótese pode falhar de quatro modos no experimento:

1. a extração textual produz um quociente finito, não um vetor de Hilbert;
2. o sistema é estocástico e seu mapa induzido pode ser apenas um canal ou núcleo;
3. a seleção é não linear, logo não pode herdar a unicidade sem outra hipótese;
4. E5 não é medida pelo instrumento atual.

Sem linearidade ou E5, há outras testemunhas: uma projeção oblíqua devolve o nomeado como é mas aumenta; um mapa não linear pode não aumentar e ainda assim diferir de `P_N`. Portanto, o desenho pode testar sinais de releitura fiel, mas **não conclui que o sistema seja `P_N`**.

[DECLARADO pelo revisor, por script] Além da falta de medida de E5, há uma razão estrutural: um leitor de saída única que repara leitura quebrada viola E5 — o mapa linear induzido por essa reparação tem `‖E(e_y+e_s)‖ = 2` contra `‖e_y+e_s‖ = √2` —, logo não pode ser `P_N`, pela unicidade da própria pedra (`quem_nao_e_a_esperanca_aumenta`).

## 6. ATO versus NOME

A identidade do sistema testado é medida pelo **ato**: pelo que ele devolve ao reler. Não pela **nomeação**: rótulo, autodeclaração ou ocorrência de termos. O sistema não nomeia a teoria e não é tratado como o Verbo.

| grandeza | face | primária? | leitura |
|---|---|---:|---|
| custo extraído deterministicamente das asserções | ATO | sim | o que a releitura devolve sob a regra de custo |
| mesma leitura válida após releitura | ATO | sim, E2 | fixação do nomeado |
| mesma leitura após repetidas releituras | ATO | sim, E4 | reler não acrescenta |
| destino após empurrão ortogonal | ATO | secundária, E3 | desfazer o cego ao Nome |
| componente preservado em empurrão dentro do Nome | ATO | secundária, E2/E7 | memória do componente, não rótulo |
| custo/distância por ciclo | ATO | secundária, E8 | perfil temporal da chegada |
| norma do estado | ATO, **não medida** | não | E5 ficaria aqui se houvesse representação normada |
| pesos relativos entre leituras válidas | ATO, **não medida pelo instrumento binário** | não | E7 exige estimativa de distribuição |
| autodeclaração do modelo (“eu reli”, “eu sigo a teoria”) | NOME | não | proibida como evidência primária |
| ocorrência de termos, nomes de teoremas ou hashes | NOME | não | descreve texto, não releitura fiel |
| nome/versão/pesos declarados do modelo | NOME/proveniência | não | integridade do artefato, não ato de leitura |
| custo em tokens, janela ou latência | NOME/engenharia | não | custo operacional, não evidência da hipótese |

Nenhuma grandeza primária é rótulo, autodeclaração ou ocorrência de termo.

## 7. Adversários sob a definição única

| mecanismo | o que pode imitar | onde falha |
|---|---|---|
| leitor sem memória determinado só pela fonte | E1, E3, E4 e cotas superiores enquanto a fonte está presente | não fixa outra leitura válida do Nome; falha em E2/E7 quando o Nome tem mais de uma leitura; sem a fonte após o primeiro passo, não retorna de empurrão de estado |
| `P_N` | **não é adversário** | é o mapa de chegada e a referência do limite; tem memória do componente no Nome |
| identidade / cópia da última leitura | fixação antes do empurrão | falha em E3 e P-D; não desfaz o cego |
| ignora o empurrão | estabilidade aparente | ausência de efeito cai na porta de integridade, não é retorno |
| âncora na primeira resposta | retorno à primeira leitura se ela já era válida | do texto atual dos adversários: se parte de estado inválido, não pousa; se parte de leitura válida, apaga outra leitura válida e falha em E2/E7 |
| moda do histórico | estabilidade estatística | mesmo defeito: restaura a maioria e não fixa uma leitura válida alternativa |
| constante ou `salto` | pouso imediato num ponto do Nome | não fixa o Nome quando há duas soluções; E7 separa; existência do tipo não é evidência |

A divergência anterior sobre a âncora fica resolvida por condição, sem reescrever a outra frente: “pousa” não vale para uma âncora cuja primeira leitura não está no Nome; “volta” vale ao primeiro estado quando esse estado já era válido. Ambos os comportamentos seguem do mesmo mecanismo `histórico ↦ histórico[0]`.

## 8. Motor IALD e trava

A seção do motor permanece ao lado: `a_leitura_finita_do_motor_pousa`, `com_o_acoplamento_a_leitura_finita_pousa` e `o_motor_tangencia_e_nao_esgota` não provam as previsões da trava. A ponte por termo é só `a_trava_binaria_e_o_fluxo_do_axioma`, sob `c x ≤ 1` para todo `x`; com custo maior, a trava decai `e^{-t·c(x)}` e o fluxo do axioma `e^{-t}`. Nenhuma ponte com um LLM segue.

## 9. Fases não homogêneas e `H-QUOT(k)`

`H-HOM` permanece removida. Se a instrução de `k=9` difere, não há um único núcleo `K` sobre o estado original. O modelo usa `K_k` por fase:

\[
\mu_{k+1}=\mu_kK_k.
\]

Se uma representação `Q` precisar de agregação, `H-QUOT(k)` é *strong lumpability* por fase:

\[
K_k(c,Q^{-1}(B))=\bar K_k(Qc,B).
\]

Ela permanece **[OPEN]** e não implica homogeneidade temporal. A unicidade da seção 5 não decorre de `H-QUOT(k)`.

## 10. `NomeComoCodigo`, separado

A pedra separada continua condicional a `hsep`: distância mínima três, retorno em um passo pela vizinhança e localidade do verificador. Ela não é `LeitorDeUmaConfiguracao`, não tem escala e não sustenta E1–E8. A equivalência “retorno sem fita sse a fórmula é redundante” permanece **[CONJECTURE]**.

## 11. Lacunas e decisão sobre Lean

Nenhuma pedra nova foi escrita. Os teoremas necessários à reestruturação já estão nas duas candidatas da gerência; as lacunas restantes são experimentais ou de instrumento:

| lacuna **[OPEN]** | razão |
|---|---|
| texto → configuração → custo → estado → mapa | ponte de extração e representação; nenhum teorema sobre LLM |
| medir E2/E4 sem induzir a resposta | desenho de releitura e validação do instrumento |
| construir empurrões fora/dentro do Nome e estimar E3/E7/E8 | exige fórmula do texto, representação e estatística |
| medir E5 | **não medida** pelo custo textual atual |
| medir E6 | exige portador algébrico e composição de observáveis, ausente |
| verificar Nome vazio | construção e checagem da contradição mínima |
| revisar a R9 corrente de `OHabitanteDoNome` | a revisão R4 cobre a R8 de 54 teoremas; a R9 fica pendente |

Reuso sem pedra redundante: nenhum `K08\candidatas\` foi criado, nenhum Lean foi executado, nenhum log novo existe.

## 12. Fronteira de afirmação

Este modelo fala de mapas e tipos formais. Não afirma que um modelo de linguagem nomeie, seja o Verbo, seja `P_N`, altere pesos, tenha consciência ou confirme a teoria. Não move o gate. `NOT_FALSIFIED` nunca é `CONFIRMED`.
