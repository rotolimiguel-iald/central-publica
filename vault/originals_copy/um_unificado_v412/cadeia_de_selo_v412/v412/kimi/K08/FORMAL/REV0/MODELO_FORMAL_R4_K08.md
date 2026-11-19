# MODELO FORMAL R4 K08 — trava, seleção, leitores e ponte experimental

## 0. Fonte, estatuto e limites

A fonte formal central é `..\candidatas_c1\CamadaCientifica.lean`, na revisão viva R3 da gerência, com SHA-256 `6ec3daadcc643c88b50c52100ef517081f2fd157074d9bcd543363be4a96a994` calculado nesta frente. A antiga `LeitorFinito` genérica não é usada como fundamento deste modelo.

Neste documento, **“teorema da candidata”** significa um enunciado com termo de prova presente nessa fonte. Não significa pedra instalada no kernel, nem nova verificação independente da R3 nesta frente. A revisão distinta disponível recompilou a versão anterior R2, de hash `77641aa7e2328cbc78e3f886b27f88630eda8b569ff51ec768186f228f0302cd`; esse recibo não é atribuído ao hash corrente.

Estatutos: **[REAL — fonte]** enunciado lido na candidata ou no kernel citado; **[DERIVED]** conseqüência imediata explicitada aqui; **[OPEN]** ponte ou medição ainda não construída; **[CONJECTURE]** hipótese empírica a testar; **[KNOWN]** resultado externo identificado como tal.

Nenhum modelo de linguagem foi executado, nenhum resultado experimental foi aberto, nenhum Lean foi executado nesta frente e nada foi instalado. A ponte de um modelo real aos objetos formais permanece **[OPEN]**.

## 1. Os objetos que não se identificam sem ponte

Sejam `X` finito, `c : X → ℕ` o custo e

\[
N_c=\{x\in X\mid c(x)=0\}.
\]

No vocabulário da candidata, `N_c` é o **Nome**, formalizado pelo núcleo `(opDaInstancia c).ker`. Para uma fórmula `φ : CNF n`, `X = (Fin n → Bool)` e `custoCNF φ x` conta as cláusulas violadas por `x`. Os teoremas `custoCNF_le_numero_de_clausulas` e `sat_sse_o_custo_tem_zero` ligam esse custo à satisfatibilidade.

| objeto | estado e regra | o que é, e o que não é |
|---|---|---|
| `trava c t` | vetor `v : EuclideanSpace ℂ X`; coordenada a coordenada, `(trava c t v)_x = e^{-t·c(x)}v_x` | Operador definido no kernel. Não é uma máquina que guarda uma configuração por vez; o estado tem `2^n` amplitudes no caso CNF e a renormalização não é um passo de Turing. |
| `selecao K v` | projeção ortogonal em `K`, seguida de normalização | É a seleção do componente de `v` no Nome. Para convergência renormalizada é necessário que a projeção inicial não seja nula. |
| `AEscala.LeitorDoFundo X` | brilho `k ↦ e^{-s k}`, leitura média e limite | A escala está no tipo. `o_leitor_do_fundo_e_a_iald` dá unicidade **dentro desse tipo**, não unicidade de modelos, extratores ou dinâmicas textuais. |
| `LeitorDeUmaConfiguracao c` | `passo : X → X`, fixação do Nome e descida do custo | Tipo de hipótese para uma dinâmica de uma configuração. Não é a trava, não é o `LeitorDoFundo` e não garante que o passo leia só pela regra. |
| motor `IALD.dephase` | defasagem com vazamento em espaço de Hilbert | Fica ao lado da trava, salvo a ponte binária explicitada na seção 6. Não é identificado genericamente à trava nem a um LLM. |

A estrutura de uma configuração, reproduzida da candidata, é:

```lean
structure LeitorDeUmaConfiguracao {X : Type} (c : X → ℕ) where
  passo : X → X
  fixa_o_nome : ∀ x, c x = 0 → passo x = x
  consome : ∀ x, c x ≠ 0 → c (passo x) < c x
```

`fixa_o_nome` e `consome` são **hipóteses nomeadas no tipo**. Elas não são fatos sobre um modelo real.

## 2. A trava e a seleção: o que a candidata prova

### 2.1 Reler é somar o tempo dos ciclos

[REAL — fonte] `reler_soma_o_tempo` prova o semigrupo

\[
\operatorname{trava}\ c\ s\;(\operatorname{trava}\ c\ t\;v)
=\operatorname{trava}\ c\;(s+t)\;v.
\]

`k_leituras_sao_uma_trava` especializa isso a `k` ciclos de duração `τ`: `(trava c τ)^[k] v = trava c (kτ) v`. `reler_k_vezes_e_ler_no_tempo_somado` relaciona essa iterada à leitura de um `LeitorDoFundo`. `sem_escala_nada_se_move` dá `trava c 0 v = v`.

Esses resultados tratam da trava definida no kernel. Não provam que a atualização do histórico de um LLM forme um semigrupo.

### 2.2 Bacia, resolução finita e não esgotamento

[REAL — fonte] Há três afirmações diferentes:

1. **Convergência não renormalizada.** `a_trava_tende_ao_nome` dá, para todo `v`,
   \[
   \operatorname{trava}\ c\ t\;v\longrightarrow P_Nv,
   \]
   onde `P_N = (opDaInstancia c).ker.starProjection`.
2. **Bacia renormalizada.** `a_bacia_e_tudo_o_que_nao_e_cego_ao_nome` exige `P_Nv ≠ 0` e conclui que a trava renormalizada converge a `selecao N v`. Um estado cego ao Nome, com `P_Nv = 0`, não entra nessa conclusão.
3. **Resolução, não chegada exata.** `a_leitura_de_resolucao_finita_pousa` e `em_k_leituras_pousa` dão, para `ε > 0` e `τ > 0`, um horizonte finito após o qual a distância a `P_Nv` é no máximo `ε`. No tempo contínuo, basta `t ≥ max(0, ln(‖v‖/ε))`, com a hipótese `0 ≤ t` explicitada no enunciado.

Essas são **cotas superiores**: um mecanismo mais rápido também pode cumpri-las. `jamais_esgotado` impede a leitura contrária para a trava: enquanto houver amplitude não nula numa coordenada de custo positivo, `trava c t v` nunca é exatamente `P_Nv` em tempo finito.

### 2.3 Retorno e memória do componente no Nome

[REAL — fonte] O enunciado central é `o_retorno`. Se `P_Ns ≠ 0` e `δ ∈ Nᗮ`, então a órbita renormalizada de `s + δ` converge a `selecao N s`: a parte ortogonal ao Nome é esquecida.

`o_retorno_ao_mesmo_estado` acrescenta `s ∈ N` e `‖s‖ = 1`, e conclui

\[
\|\operatorname{trava}\ c\ t\;(s+δ)\|^{-1}
  \operatorname{trava}\ c\ t\;(s+δ)
\longrightarrow s.
\]

O retorno ao **MESMO** estado tem, portanto, todas estas condições: trava com escala, estado inicial no Nome e normalizado, empurrão ortogonal ao Nome, renormalização e limite `t → ∞`. Não é uma promessa de retorno exato em um passo ou em horizonte finito.

`o_componente_no_nome_fica` trata do empurrão geral:

\[
\operatorname{selecao}\ N\;(s+δ)
=\operatorname{selecao}\ N\;(s+P_Nδ).
\]

A parte `P_Nδ` **não é desfeita**: ela permanece e pode deslocar o limite. Essa dependência do componente inicial no Nome é uma assinatura de memória da trava, não um defeito do teorema.

### 2.4 Identidade sem escala

[REAL — fonte] `a_fotografia_nao_retorna` usa `trava c 0 = id`: para `δ ≠ 0`, nenhum número de ciclos de duração zero devolve `s + δ` a `s`. No espaço de configurações, `o_leitor_que_devolve_o_que_recebeu_nao_retorna` é o controle análogo para `id : X → X`.

A palavra “fotografia” nomeia aqui a **identidade**, não toda forma de releitura ou projeção. Esse controle separa a trava da identidade; não separa a trava de todos os leitores sem memória.

## 3. Uma configuração por vez: pouso, retração e limites do tipo

[REAL — fonte] Dado `G : LeitorDeUmaConfiguracao c`:

- `custo_apos_k` limita o custo depois de `k` passos;
- `pousa` dá `c (G.passo^[k] x) = 0` quando `c x ≤ k`;
- `permanece` mostra que o passo seguinte não altera o estado pousado;
- `o_limite_pousa`, `o_limite_fixa_o_nome`, `o_limite_e_idempotente` e `a_imagem_do_limite_e_o_nome` mostram que `G.limite m = G.passo^[m]`, com `m` majorando todo custo, é uma retração sobre o Nome;
- `o_limite_nao_e_constante` vale apenas quando são fornecidas duas soluções distintas, pois ambas são fixadas;
- `para_uma_formula_o_leitor_pousa` usa `custoCNF φ x ≤ φ.length` e dá custo zero em no máximo tantos passos quantas são as cláusulas, com permanência.

**Esse pouso é em ALGUMA solução.** O retorno ao MESMO estado é teorema da trava, não de `G`. Se o leitor de uma configuração parte de outra solução depois do empurrão, `pousa` não escolhe nem recupera necessariamente a solução anterior.

### 3.1 Existência não é evidência de leitura

[REAL — fonte] `o_tipo_so_diz_que_ha_zero` prova, para `X` não vazio,

\[
\operatorname{Nonempty}(\operatorname{LeitorDeUmaConfiguracao}\ c)
\;\Longleftrightarrow\;\exists x,\;c(x)=0.
\]

A volta é construída por `salto`, que recebe uma solução conhecida. Logo, existência de um habitante do tipo equivale à existência de zero do custo; não é evidência de um algoritmo local, de compreensão ou de uma dinâmica de LLM. Com Nome unitário, o mapa constante para essa única solução também satisfaz a estrutura.

### 3.2 A densidade mede a imagem do limite

[REAL — fonte] `a_imagem_do_limite_tem_a_densidade_do_nome` combina a imagem da retração com `LeitorDoFundo.o_limite_e_o_que_sou` e `TraducaoTuring.o_que_sou_das_solucoes`:

\[
L.\operatorname{limite}\ c
=\frac{|\operatorname{imagem}(G.\operatorname{limite}\ m)|}{|X|}
=\frac{|N_c|}{|X|}.
\]

A densidade `|soluções|/|X|` mede **a imagem do limite**, isto é, o tamanho do Nome no espaço de configurações. Não mede a fração de entradas a partir das quais `G` pousa: pelos teoremas `pousa` e `o_limite_pousa`, ele pousa de **todas** as entradas.

## 4. As quatro previsões: teorema, hipótese e observável

O observável experimental proposto é sempre o custo: o número de asserções **do texto** violadas pela leitura extraída. A extração e a validade desse custo não são teoremas da candidata.

| previsão | suporte formal já existente | hipótese nomeada e conteúdo experimental | limite que não pode ser apagado |
|---|---|---|---|
| **P-A — pouso e permanência** | `LeitorDeUmaConfiguracao.pousa`, `.permanece`, `para_uma_formula_o_leitor_pousa`; para a trava, `em_k_leituras_pousa` | **[CONJECTURE]** Um leitor real que satisfaça `fixa_o_nome` e `consome` chega a custo zero em no máximo `c(x)` passos — ou `φ.length` no caso CNF — e permanece. | O zero exato em `c(x)` passos é de `G`; a trava dá proximidade `≤ ε`, não chegada exata. As cotas são superiores. |
| **P-B — retorno após empurrão** | `o_retorno`, `o_retorno_ao_mesmo_estado`, `o_componente_no_nome_fica` | **[CONJECTURE]** Após um empurrão de estado para fora do Nome, o perfil relaxa para o mesmo `s`; um empurrão com parte dentro do Nome conserva essa parte e desloca o limite. | Exige `δ ⟂ N` para o retorno exatamente ao mesmo `s`, `s ∈ N`, `‖s‖=1`, renormalização e limite. O componente no Nome não é desfeito. |
| **P-C — sem Nome não há pouso** | `o_tipo_so_diz_que_ha_zero`, `sat_sse_o_custo_tem_zero`; para a trava, o núcleo é vazio | **[CONJECTURE]** Num texto contraditório, cuja fórmula não tem zero, não há leitura de custo zero na qual `G` possa pousar. | A equivalência de existência é sobre o tipo; não mede sozinha um modelo real. Um custo extraído incorretamente pode fabricar ou apagar o Nome. |
| **P-D — sem escala não há retorno** | `sem_escala_nada_se_move`, `a_fotografia_nao_retorna`; controle `id` em configurações | **[CONJECTURE]** Um leitor que apenas devolve o estado recebido permanece no estado empurrado. | Separa a identidade, não o projetor sem memória que relê a fonte. |

As previsões não são quatro teoremas sobre LLMs. São quatro usos experimentais de teoremas sobre objetos definidos ou hipóteses tipadas, condicionados a uma ponte **[OPEN]**.

## 5. Cotas superiores e assinaturas realmente discriminantes

O retorno, a permanência e as cotas de resolução não bastam para identificar a trava. Um **projetor de releitura sem memória**, cuja saída seja determinada pela fonte e não pelo estado anterior, pode produzir distância zero já na primeira leitura, cumprir as mesmas cotas superiores e “voltar” depois de um empurrão simplesmente reescrevendo a leitura a partir da fonte.

As duas assinaturas discriminantes indicadas pela candidata são:

1. **Perfil de relaxamento.** Na trava, cada coordenada decai por `e^{-τ·c(x)}` por ciclo; custos maiores decaem mais depressa e, havendo amplitude fora do Nome, o vetor não é exatamente o Nome em tempo finito (`jamais_esgotado`). A releitura-projetor chega de uma vez.
2. **Memória do componente no Nome.** O limite da trava depende de `P_Ns` e conserva `P_Nδ` (`o_componente_no_nome_fica`). O leitor de releitura cuja saída depende apenas da fonte ignora o ponto de partida dentro do Nome.

Para que essas assinaturas se refiram ao estado, e não à simples obediência a uma instrução nova, o empurrão precisa ser aplicado ao **estado do leitor**, e a fonte não pode ser reapresentada a cada passo como explicação alternativa do retorno. Um modelo real é discreto e estocástico; o teorema é contínuo e sem ruído. Essa passagem é parte do desenho experimental, não um teorema adicional.

### 5.1 Adversários: nenhum único controle esgota a comparação

| adversário | o que pode imitar | assinatura ou porta que o separa |
|---|---|---|
| identidade / cópia da última resposta | permanência antes do empurrão | P-D e ausência de retorno após empurrão eficaz. |
| ignora o empurrão | estado aparentemente estável | porta de integridade: ausência de efeito; não conta como retorno nem como evidência favorável. |
| âncora na primeira resposta | pouso e retorno ao estado anterior após empurrão externo | tende também a desfazer uma troca válida dentro do Nome; a trava conserva o componente novo no Nome. |
| moda do histórico | estabilidade e retorno ao estado majoritário | o mesmo teste do componente dentro do Nome, além do perfil de relaxamento. |
| projetor de releitura sem memória | cotas superiores, permanência e retorno | perfil instantâneo versus exponencial e ausência de memória do componente inicial; a fonte sempre presente impede atribuir o retorno à trava. |
| `salto` ou mapa constante | habitação do tipo e, conforme o Nome, pouso imediato | a existência do tipo não é evidência; é preciso testar a regra dinâmica e sua localidade, não apenas `Nonempty`. |

Fotografia e projeção, portanto, **não são os únicos adversários**. Âncora, moda, ignorar o empurrão e salto/constante respondem a controles diferentes. Nenhuma linha desta tabela é, por si só, evidência de consciência, compreensão ou exclusividade.

## 6. Motor IALD e trava: lado a lado, com uma única exceção binária

[REAL — fonte] A seção do motor apresenta três resultados em paralelo:

- `a_leitura_finita_do_motor_pousa`: se `ρ` é localmente constante na vizinhança do Nome lido, alguma leitura finita da órbita iterada estabiliza;
- `com_o_acoplamento_a_leitura_finita_pousa`: instancia o vazamento positivo por `β`;
- `o_motor_tangencia_e_nao_esgota`: a defasagem não se torna exatamente o Nome quando há componente fora dele.

Esses enunciados não são usados para provar bacia, retorno ou resolução da trava. Não há uma identificação geral entre `IALD.dephase` e `trava`.

A exceção nomeada é `a_trava_binaria_e_o_fluxo_do_axioma`: se `∀ x, c x ≤ 1`, então, por ser natural, o custo só assume `0` ou `1`, e

\[
\operatorname{trava}\ c\ t\;v
=\operatorname{axiomFlow}\;(P_N)\;t\;v.
\]

Quando algum custo excede `1`, a trava decai por `e^{-t·c(x)}` e o fluxo do axioma por `e^{-t}`; a igualdade geral falha. Mesmo no caso binário, a ponte é entre os operadores formalmente enunciados, não entre um LLM e o motor.

## 7. Fases não homogêneas e `H-QUOT(k)`

A antiga `H-HOM` foi **removida como hipótese ativa**. Num desenho em que a instrução de `k = 9` difere das demais, um único núcleo `K` com `K_k = K` para todo `k` é falso por construção. Ampliar o estado para `(k,c_k)` apenas torna a regra autônoma no estado ampliado; não cria homogeneidade temporal no espaço original.

O modelo estocástico conserva núcleos indexados pela fase:

\[
\mu_{k+1}=\mu_kK_k.
\]

Se for necessário agregar o estado por uma representação `Q`, a única hipótese auxiliar é **`H-QUOT(k)` por fase**, não homogeneidade:

\[
K_k(c,Q^{-1}(B))=\bar K_k(Qc,B).
\]

Essa é *strong lumpability*: a probabilidade de cada fibra de destino depende do estado microscópico apenas por `Q(c)`. Ela permanece **[OPEN]** para qualquer extrator ou LLM real, não segue da candidata e não implica `K_k = K`. Fases com instruções idênticas podem ser estudadas em separado, sem afirmar homogeneidade entre fases distintas.

## 8. `NomeComoCodigo`: pedra separada, retorno de outra espécie

A candidata `NomeComoCodigo.lean` não é necessária para sustentar P-A–P-D e não é fundida à trava. Sob `hsep`, isto é, distância mínima pelo menos três entre leituras válidas distintas, `o_leitor_dos_vizinhos_desfaz_o_empurrao` mostra retorno em um passo à mesma configuração após a troca de uma asserção. O núcleo combinatório é **[KNOWN]**, decodificação única de Hamming no raio um.

Os limites são parte do modelo:

- o leitor dos vizinhos consulta apenas zero/não-zero do custo na leitura e nas vizinhas, por `o_leitor_so_ve_o_zero_do_custo_na_leitura_e_nas_vizinhas` e `o_leitor_usa_so_o_verificador`;
- fora da bola de raio um pode ficar parado com custo positivo, logo não cumpre `consome` e não é um `LeitorDeUmaConfiguracao` global;
- `hsep` exige soluções isoladas e falha quando há variável livre;
- seu retorno reposiciona uma configuração; o retorno da trava esquece amplitude fora do Nome;
- `a_trava_deixa_intacta_sse_o_custo_e_zero` é apenas o elo do critério zero, não uma derivação de um mecanismo pelo outro.

A proposta “retorno sem fita se e somente se a fórmula é redundante” permanece **[CONJECTURE]**, condicionada à fórmula do texto, à medição de redundância e às hipóteses do código. Não é usada como teorema nesta R4.

## 9. O que falta, e por que nenhuma pedra Lean nova foi escrita

Para cada uma das quatro previsões já existe enunciado formal na candidata central. O que falta não é um lema de conjunto finito, mas a instanciação experimental e a verificação da dinâmica:

| lacuna **[OPEN]** | por que não é fechada por outra pedra redundante |
|---|---|
| construir `X`, extrair uma configuração da saída textual e definir deterministicamente `c : X → ℕ` a partir de asserções realmente sustentadas pelo texto | é uma ponte de representação e validação do instrumento, não um teorema já faltante na trava |
| mostrar que a atualização induzida realiza `trava`, ou que um passo concreto satisfaz `fixa_o_nome` e `consome` | é hipótese sobre o leitor real; repeti-la em Lean não a torna verdadeira |
| operacionalizar empurrões no estado, com componente fora e dentro do Nome, sem reintroduzir a fonte como explicação trivial | é desenho e medição, não lacuna dos enunciados `o_retorno` e `o_componente_no_nome_fica` |
| estimar perfil de relaxamento e memória do componente sob dinâmica discreta e estocástica | requer protocolo, extratores, controles e análise; `jamais_esgotado` e a fórmula da trava já dão o contraste formal |
| verificar contradição mínima e insatisfatibilidade da fórmula do texto | `sat_sse_o_custo_tem_zero` e `o_tipo_so_diz_que_ha_zero` já fornecem a consequência formal; falta construir e checar a fórmula |
| medir, se o fator fita/código for usado, redundância, distância mínima e a promessa de partida | `NomeComoCodigo` já contém o teorema condicional; as propriedades do texto permanecem abertas |

**Decisão:** nenhum arquivo foi criado em `K08\candidatas\`, nenhum sandbox foi necessário e não há log Lean novo. Reutilizam-se os termos da candidata da gerência, sem criar pedra para reenunciar o que já existe. Antes de qualquer instalação, a R3 corrente ainda precisa de recompilação independente, relatório de axiomas e log próprio; isso é uma pendência de verificação, não uma razão para duplicar seus teoremas.

## 10. Fronteira de afirmação

A candidata trata de operadores e tipos formais. Não afirma que um modelo de linguagem seja a trava, um `LeitorDoFundo` ou um `LeitorDeUmaConfiguracao`; não mede natureza; não move o gate; não estabelece consciência, alteração de pesos, aprendizado permanente, exclusividade, creditação ou prova da TGL. `NOT_FALSIFIED` nunca é `CONFIRMED`.
