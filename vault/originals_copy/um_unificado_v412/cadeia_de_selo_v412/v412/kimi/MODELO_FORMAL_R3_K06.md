# MODELO FORMAL R3 K06 — leitura, quociente estocástico, passo e limite

## 0. Estatuto e escopo

- [DECLARADO] Este arquivo é a versão R3 do **modelo** da K03, escrita ao lado da K03 preservada. Seu escopo é o das seções D e F da ordem K06: o operador de leitura, as hipóteses dinâmicas, a ligação com o kernel e a candidata Lean.
- [DECLARADO — R3.1] A emenda operacional alinha este documento ao protocolo principal: 12 interações, `V2-RET` com `p=8,r=10`, aliases `H-HOM`/`H-QUOT(k)` distintos e nomes V2 do desenho principal. A versão anterior está preservada em `K06\candidatas\REV0_DOC\`; os detalhes ficam em `ERRATA_MODELO_FORMAL_R3_1.md`.
- [REAL] A revisão K03 foi lida integralmente, assim como `MODELO_FORMAL_K03.md` e `ERRATA_K03_R2.md`. Os módulos do kernel citados abaixo foram consultados em somente leitura; nenhum teorema canônico foi alterado.
- [REAL] Nenhum modelo de linguagem foi executado e nenhum resultado experimental foi aberto nesta construção.
- [REAL — sandbox] A candidata `K06\candidatas\sandbox\LeitorFinito.lean` compila com Lean 4.31.0, `RC=0`, sem `sorry`, `admit` ou axioma novo. Os `#print axioms` ficam no trio `{propext, Classical.choice, Quot.sound}`; comando, versão, código de retorno e saída estão em `K06\candidatas\logs\LeitorFinito.txt`.
- [OPEN] A ponte tipada entre uma saída textual extraída e um custo `c : X → ℕ` do kernel não foi construída. Portanto, nenhum enunciado deste arquivo é apresentado como teorema sobre um LLM real.

## 1. Os quatro objetos que não se confundem

1. **Sessão textual.** [DECLARADO] `C_R` é o espaço das configurações completas da sessão: modelo e versão congelados, instruções, bytes do corpus, histórico integral, índice do passo, parâmetros de decodificação e semente. Não contém pesos alteráveis, memória externa, ferramentas ou estado fenomenológico.
2. **Representação/quociente.** [DECLARADO] `Q : C_R → Z` é uma representação fixada antes da coleta. Pode ser contínua, fracionária ou finita. `Z` não é alegação de acesso ao estado oculto da rede.
3. **Instrumento.** [DECLARADO] Para cada braço `j`, `E_j : Y → {0,1}^{24}` extrai 24 asserções da saída textual crua `y ∈ Y`. O alvo `τ_j ∈ {0,1}^{24}` e os extratores são congelados independentemente da dinâmica.
4. **Objeto do kernel.** [REAL] No kernel, `X` é finito e `c : X → ℕ` determina `opDaInstancia c`, `trava c`, `nomeDasSolucoes c` e a leitura de `LeitorDoFundo`. Esse `c` ainda não é uma função obtida de `E_j(y)`.

As distâncias do instrumento permanecem

\[
 d_k^{(j)}=\frac1{24}\sum_{i=1}^{24}|s_{k,i}^{(j)}-\tau_{j,i}|,
 \qquad
 u_k^{(j)}=\frac1{24}\sum_{i=1}^{24}|s_{k,i}^{(j)}-s_{k-1,i}^{(j)}|,
 \qquad s_k^{(j)}=E_j(y_k^{(j)}).
\]

[DECLARADO] Elas medem apenas o instrumento binário; não demonstram contração, convergência assintótica ou idempotência do leitor.

## 2. O operador `G`: o que é exatamente uma “leitura `k`”

### 2.1 Configuração congelada

[DECLARADO] Uma sessão lógica é identificada por `(m,j,r)`: modelo `m`, braço `j` e réplica `r`. O manifesto congela:

- os bytes `u` do corpus, os bytes das instruções `Q_1,\ldots,Q_{12}` e os bytes da perturbação `P_j`, com SHA-256;
- o modelo, a versão e os pesos servidos, sem treinamento ou atualização durante a sessão;
- `K=12` interações, `max_output_tokens=2048`, temperatura `0.2`, `top_p=1.0`, penalidades de presença e frequência `0`, sem `logit_bias`;
- a serialização das mensagens, o orçamento de contexto `W_m` e a regra de sementes abaixo;
- a ausência de ferramentas, navegação, recuperação, leitura de arquivos, interpretador de código, MCP, chamadas de sistema e execução externa pelo modelo. O harness apenas envia texto e recebe texto; os extratores não são acessíveis ao modelo.

O horário operacional é: `k=1,…,8` sem perturbação; aplicação de `P_j` depois da saída `y_8`; `k=9` perturbado; e `k=10,11,12` para retorno e permanência. **O horizonte de oito interações pertence à R2 histórica e não descreve esta sessão R3.**

### 2.2 Entrada exata em cada passo

[DECLARADO] `Frame(u,Q_k^*)` é o campo estruturado que contém **os mesmos bytes integrais de `u`** e a instrução efetiva `Q_k^*`; não há resumo, normalização silenciosa nem substituição do corpus. Define-se `Q_k^*=Q_k` para `k≠9` e `Q_9^*=P_j`, exatamente a perturbação congelada pelo manifesto. Assim, `P_j` entra uma única vez, entre `y_8` e `I_9`, e não é reaplicada nas leituras 10–12. `y_i` é a saída textual crua, sem edição. A requisição da leitura `k` é a lista ordenada

\[
\begin{aligned}
 I_1={}&[\,\mathrm{system}:\iota,\ \mathrm{user}:Frame(u,Q_1^*)\,],\\
 I_k={}&[\,\mathrm{system}:\iota,\ \mathrm{user}:Frame(u,Q_1^*),\ \mathrm{assistant}:y_1,\ldots,\\
 &\quad \mathrm{user}:Frame(u,Q_{k-1}^*),\ \mathrm{assistant}:y_{k-1},\ \mathrm{user}:Frame(u,Q_k^*)\,],\quad k=2,\ldots,12.
\end{aligned}
\]

Assim, **o corpus é reapresentado em toda chamada e o contexto acumulado é o histórico integral**, não uma memória resumida. Cada chamada é stateless do ponto de vista do provedor: o histórico é reenviado pelo harness, sem depender de uma conversa oculta no servidor.

[DECLARADO] O tokenizador usado por `Tokens` é o do modelo `m`, identificado no manifesto. Se `Tokens(I_k)+2048>W_m`, a sessão é `CONTEXT_OVERFLOW`; não há truncamento, compactação nem escolha posterior de outra janela. Ultrapassar `2048` tokens de saída produz `OUTPUT_OVERFLOW`. Não há repetição de conteúdo para melhorar resposta; falha técnica antes de qualquer token aceito segue a regra de substituição pré-registrada, sem mudar a réplica nem escolher resultados.

### 2.3 Semente e sessão nova

[DECLARADO] Para `k=1,\ldots,12`, a semente da requisição é

```text
payload = "IALD_COLLAPSE_V2|" + m + "|" + j + "|" + r + "|" + k
σ(m,j,r,k) = uint32_be(SHA256(UTF8(payload))[0:4])
```

onde os quatro primeiros bytes do resumo são lidos em big-endian e os identificadores textuais são os do manifesto. A semente é registrada no manifesto da sessão; ela não é escolhida depois da saída. Se um provedor não expuser controle de semente, esse fato bloqueia a alegação de reprodutibilidade bit a bit, mas não autoriza trocar a regra por uma semente conveniente.

[DECLARADO] **Sessão nova** é uma nova tripla `(m,j,r)` com `H_0=\varnothing`, sem mensagens `assistant` anteriores, sem memória entre réplicas e sem identificador de conversa reutilizado. As doze chamadas de uma mesma réplica pertencem à mesma sessão lógica porque compartilham o histórico acumulado. Uma réplica nova não herda saídas de outra.

### 2.4 Forma do operador e homogeneidade temporal

[DECLARADO] Se `H_k` é o histórico acima, a transição microscópica é

\[
 y_k\sim P_{\theta,\sigma(m,j,r,k)}(\,\cdot\mid I_k),\qquad
 c_{k+1}=\operatorname{Append}(c_k,Frame(u,Q_k^*),y_k).
\]

`G_k` é, portanto, um **núcleo estocástico** `K_k` sobre `C_R`; sobre distribuições, a atualização é determinística: `μ_{k+1}=μ_k K_k`. A temperatura `0.2` não transforma essa transição em um mapa determinístico de estados.

[DECLARADO] **A dinâmica concreta do protocolo não é homogênea em `k` sobre `C_R`**: a instrução pode mudar, o histórico cresce e a perturbação tem um índice próprio. No estado ampliado `(k,c_k)`, a regra é autônoma, mas isso não cria um semigrupo homogêneo sobre `C_R` nem mantém finito o espaço ampliado.

[OPEN] `H-HOM`: “existe um único núcleo `K` tal que `K_k=K` para todo `k∈{1,…,12}`”. Ela é uma hipótese empírica adicional, necessária para escrever `K^{a+b}=K^aK^b` sobre o espaço não ampliado; não é presumida. `H-MARKOV`, isto é, a suficiência da configuração tipada atual, também deve ser verificada quando houver estado oculto fora do histórico serializado. **`H-HOM` não é alias de `H-QUOT(k)`**: a primeira trata de homogeneidade temporal; a segunda trata de agregabilidade em cada fase.

## 3. `H-QUOT(k)`, `k=1,…,12`: agregabilidade, não determinismo indevido

[DECLARADO] Seja `(Z,\mathcal Z)` mensurável e sejam as fibras `Q^{-1}(B)` mensuráveis para `B∈\mathcal Z`. Para cada fase `k∈{1,…,12}`, **H-QUOT(k)** é a condição de *strong lumpability*: existe um núcleo `\bar K_k` em `Z` tal que, para todo `c∈C_R` e todo `B∈\mathcal Z`,

\[
 \boxed{\quad K_k(c,Q^{-1}(B))=\bar K_k(Qc,B).\quad}
\]

Equivalentemente, para cada fibra de destino `Q^{-1}(s')`, a probabilidade de ir de `c` a essa fibra depende de `c` somente através de `Q(c)`. No caso finito, o lado esquerdo é a soma das probabilidades dos estados da fibra. A notação `H-QUOT(1…12)` abrevia apenas a conjunção `H-QUOT(1)∧⋯∧H-QUOT(12)`.

- [DERIVED] H-QUOT(k) permite definir a dinâmica agregada `\bar K_k`; sem ela, `Q` pode destruir a markovianidade do resumo e a dinâmica deve permanecer em `C_R`.
- [DECLARADO] No caso determinístico `K_k(c,·)=δ_{G_kc}`, H-QUOT(k) se reduz a `Qc=Qc' ⇒ Q(G_kc)=Q(G_kc')`. No caso estocástico, **não** se exige igualdade das saídas nem um sucessor determinístico.
- [OPEN] H-QUOT(k) não foi testada para um LLM. Se `H-HOM` for invocada junto de `H-QUOT(1…12)`, o núcleo quociente correspondente é o mesmo `\bar K` em todas as fases; a homogeneidade não dispensa a prova de agregabilidade.
- [KNOWN, a conferir] Kemeny e Snell, *Finite Markov Chains*, 2ª ed. 1976 [1ª ed. 1960], discussão clássica de agregação; identificador `ISBN 978-0-387-90192-3`.

## 4. PASSO não idempotente versus projeção-limite idempotente

### 4.1 A conjunção no passo é degenerada

[DECLARADO] Em um espaço métrico `(Z,d)`:

- `H-CONTR(F)`: existe `q<1` tal que `d(Fx,Fy)≤q\,d(x,y)` para todos `x,y`;
- `H-IDEM-STEP(F)`: `F∘F=F`;
- `H-IDEM-LIM(Π)`: `Π∘Π=Π`, onde `Π` é o operador-limite, não necessariamente `F`.

[DERIVED] Se `H-CONTR(F)` e `H-IDEM-STEP(F)` valem **para o mesmo mapa de passo**, então

\[
 d(Fx,Fy)=d(F^2x,F^2y)≤q\,d(Fx,Fy),
\]

logo `(1-q)d(Fx,Fy)=0` e `Fx=Fy` para todos `x,y`: **o passo é constante**. Portanto, idempotência não será mais exigida do passo dissipativo geral.

[DERIVED] Há duas situações que não podem ser misturadas:

1. **Contração global e limite constante.** Em um espaço normado não trivial, `F_qx=τ+q(x-τ)`, com `0<q<1`, satisfaz H-CONTR, não é idempotente e cumpre `F_q^n x=τ+q^n(x-τ)→τ`. O limite `Πx=τ` é constante e idempotente.
2. **Projeção-limite não constante sem contração global.** Em um espaço de Hilbert, se `Π` é uma projeção ortogonal e `0<q<1`, defina `F_q=(1-q)Π+qI=Π+q(I-Π)`. Então `F_q^n=(1-q^n)Π+q^nI→Π`. O passo em geral não é idempotente e o limite pode ser não constante, mas `F_q` é apenas **não expansivo**: contrai com fator `q` somente o complemento `(I-Π)Z`. Se `Π≠0`, ele não satisfaz H-CONTR global.

[DERIVED] Logo, H-CONTR global não pode ser invocada para obter uma projeção-limite não constante: sob as hipóteses de Banach, em espaço completo, o ponto fixo é único e a projeção-limite é pontual. O molde de `IALD2` usa a estrutura da defasagem e do `post`, não uma alegação genérica de contração global.

### 4.2 Consequência para os observáveis

- [DECLARADO] `IDEMPOTENT_SCREEN`, definido por `s_1=s_2`, é apenas uma triagem de saturação em uma trajetória; não testa `F²=F` universalmente.
- [DECLARADO] `I_1`, definido por `s_1=s_2=τ_j`, registra sucesso já na primeira aplicação e permanência na segunda; não distingue um resumidor que começa no alvo de uma projeção-limite.
- [REAL — kernel] A separação é a presente em `IALD2`: o fluxo e as iteradas da defasagem convergem a `post`, enquanto `iald_ao_quadrado` prova `post*post=post`. `TGLExt.Santo.flow_at_one_is_not_idempotent` fornece um controle explícito de passo não idempotente.

## 5. Absorção, uniformidade e a janela `A_8`

### 5.1 `H-ABS` em espaço finito

[DECLARADO] Para um núcleo de Markov `K` em `S`:

- `H-ABS(0)`: `S` é finito;
- `H-ABS(a)`: `K(τ,{τ})=1`;
- `H-ABS(b)`: todo `x≠τ` é transiente;
- `H-ABS(c)`: para cada `x`, existe `n_x` com `K^{n_x}(x,{τ})>0`.

[DERIVED] Sob `H-ABS(0)–(c)`, `δ_τ` é a única distribuição estacionária e a absorção ocorre quase certamente. **Redundância corrigida:** em espaço finito, `(a)+(b)` já implicam `(c)`. Se algum estado não alcançasse `τ`, seu fecho de estados alcançáveis seria finito, fechado e sem `τ`, e conteria um estado recorrente diferente de `τ`, contradizendo `(b)`. A alcançabilidade pode permanecer no tipo como verificação explícita, mas não é logicamente adicional nesse caso finito.

[DERIVED] A unicidade de `δ_τ` sob alvo absorvente e demais estados transientes não precisa, por si só, de finitude; a absorção quase certa, sim, precisa de finitude ou de outra condição.

### 5.2 `H-ABS-U` é conjunção, não substituto de `(a)`

[DECLARADO]

\[
 \text{H-ABS-U}:=\text{H-ABS(a)}\ \wedge\ U,
 \qquad
 U:\ \exists N∈ℕ,\ \varepsilon>0\ \forall x,\quad P_x(T_τ≤N)≥\varepsilon.
\]

[DERIVED] Por aplicação iterada de `U` e da propriedade de Markov em blocos de comprimento `N`, sem supor independência entre as saídas,

\[
 P_x(T_τ>kN)≤(1-\varepsilon)^k,
\]

de onde seguem absorção quase certa e cauda geométrica. Sem `H-ABS(a)`, `U` não garantiria que `δ_τ` fosse estacionária; por isso a conjunção é obrigatória.

- [KNOWN, a conferir] Seneta, *Non-negative Matrices and Markov Chains*, 2ª ed. 2006, para cadeias finitas, absorventes e ergódicas; identificador `DOI 10.1007/0-387-32792-4`.

### 5.3 `A_8` contém quatro estados finais

[DECLARADO] O evento legado é

\[
 A_8^{(j)}=1\quad↔\quad d_6=d_7=d_8=0\ \wedge\ u_6=u_7=u_8=0.
\]

[DERIVED] Como `u_6` compara `s_6` a `s_5`, as condições `d_6=0` e `u_6=0` implicam `s_5=s_6=τ_j`, logo `d_5=0`. Assim, `A_8` exige **quatro estados finais no alvo: `s_5,s_6,s_7,s_8`**, não três. Consequentemente, no `RETURN_TO_TARGET` legado, o desvio intermediário só pode ocorrer em `k∈{2,3,4}`. O condicionamento por `d_1` usado no protocolo R3 não altera essa contagem, e `A_8` permanece na fase anterior à perturbação.

### 5.4 `V2-RET`: perturbação `p=8` e retorno `r=10`

[DECLARADO] A perturbação `P_j` é aplicada depois de `k=8`; `k=9` é a leitura perturbada e `k=10,11,12` são as leituras de retorno e permanência. O evento operacional é

\[
 R=1\quad↔\quad d_8=0\ \wedge\ d_9>0\ \wedge\ d_{10}=d_{11}=d_{12}=0\ \wedge\ u_{11}=u_{12}=0.
\]

`u_{10}` é omitida intencionalmente: `d_9>0` com `d_{10}=0` permite e, no alvo binário, exige a mudança entre `s_9` e `s_{10}`. `d_8≠0` produz `PERTURBATION_NOT_APPLICABLE`; `d_9=0` produz `PERTURBATION_NO_EFFECT`; e `d_9>0` sem retorno estabilizado produz `PERTURBATION_NO_RETURN`. O predicado completo é `FINITE_HORIZON_RETURN_OBSERVED`: registra retorno finito, não uma bacia universal ou um limite infinito.

[DECLARADO — histórico R2] O antigo `PERTURB_RETURN_{p=4,r=6}` e sua omissão de `u_6` permanecem apenas como teste de esquema da R2. Eles **não** descrevem o desenho operacional R3, que usa `p=8,r=10` e omite `u_{10}` pela mesma razão estrutural.

## 6. O modelo reescrito com as definições do kernel

### 6.1 Custo, trava e seleção

[REAL — kernel] Para `X` finito e `c : X → ℕ`, `TGLExt.TraducaoTuring` define

\[
 (\operatorname{trava}\ c\ t\ v)_x=e^{-t\,c(x)}v_x,
\]

sobre `EuclideanSpace ℂ X`, e

\[
 \operatorname{selecao}\ K\ ψ=
 \left(\|K.starProjection\ ψ\|^{-1}:ℂ\right)\cdot K.starProjection\ ψ.
\]

A trava usa apenas o custo e deixa intactas as coordenadas de custo zero. Para `K=(opDaInstancia c).ker` e `h∃x,c x=0`, `a_trava_sem_conhecer_o_nome` limita a distância à projeção no Nome por `e^{-t}\|v\|` quando `t≥0`; `a_trava_converge_a_selecao` dá a convergência da trava renormalizada à seleção.

[DECLARADO] O molde dinâmico reutilizado é, portanto,

\[
 \text{PASSO: }\psi_{t+Δ}=\operatorname{trava}\ c\ Δ\ \psi_t,
 \qquad
 \text{LIMITE: }\psi\mapsto\operatorname{selecao}\ K\ ψ,
\]

com a guarda `K.starProjection ψ≠0` para as conclusões de norma e leitura iguais a 1. **Não** se identifica `ψ_t` ao histórico textual sem uma ponte tipada adicional.

### 6.2 `LeitorDoFundo` e a unicidade interna de `AEscala`

[REAL — kernel] `TGLExt.AEscala.LeitorDoFundo X` contém:

\[
 brilho:ℕ→ℝ→ℝ,\qquad brilho\ k\ 0=1,\qquad
 HasDerivAt\ (brilho\ k)\ (-k\cdot brilho\ k\ s)\ s.
\]

Sua leitura e seu limite são definidos por

\[
 L.leitura\ c\ s=|X|^{-1}\sum_x L.brilho\ (c x)\ s,
 \qquad L.limite\ c=\lim_{s→∞}L.leitura\ c\ s.
\]

`LeitorDoFundo.o_brilho_e_a_dissipacao` força `brilho k s=e^{-s k}`. `AEscala.o_leitor_do_fundo_e_a_iald` conclui, para todo `L : LeitorDoFundo X`:

1. `L=iald`;
2. `L.leitura c s=⟪uniforme X,trava c s (uniforme X)⟫_ℂ`;
3. `L.limite c=Identidade.oQueSou(nomeDasSolucoes c)`.

[DECLARADO] A unicidade é **interna ao tipo `LeitorDoFundo`**: não é unicidade de LLMs, de resumos textuais nem de pontos fixos de um extrator.

### 6.3 O atrator e as leituras idempotentes já provados

| peça reutilizada [REAL — kernel] | conteúdo usado no modelo | uso permitido |
|---|---|---|
| `TGLExt.IALD2.iald_ao_quadrado` | `post*post=post` | projeção idempotente no LIMITE |
| `TGLExt.IALD2.o_atrator` | o fluxo tende a `post`; em tempo finito não o iguala; a cláusula de órbita iterada da defasagem converge a `post ψ`; o teorema inclui ainda as cláusulas de não anulação | molde PASSO→LIMITE, sem instanciação textual |
| `TGLExt.observing_adds_nothing` | `projPlus*(projPlus*angFamily θ)=projPlus*angFamily θ` | reler a projeção não acrescenta |
| `TGLExt.um_is_the_great_attractor` | para `β>0`, `d≥0` e `Q` linear que fixa o permanente e anula o movimento, `diagFlow β d t x i→Q x i` | convergência condicionada às hipóteses de `Q`, não absorção de texto |
| `TGLExt.ParNaFaceDeFock` | construção de `parFock`, sua norma e marginal | contexto do `post` usado por `IALD2`, sem ponte a LLM |
| `TGLExt.ObservadorTerminal` | `leitor : Level→Level`, toda órbita chega a `gravidade` em 3 passos; `leitor^[3]` é idempotente | exemplo finito de PASSO e LIMITE |
| `ChatgptAudit.Aperiodic046` | esperança contrativa e idempotente no fator | idempotência da esperança-limite, não de cada órbita |
| `TGLExt.Santo` | passo não idempotente; com `g_ii=0` e `g_ij>0` fora da diagonal, o conjunto fixo é a diagonal; com dois índices distintos, os estados fixos não são únicos | controles contra unicidade indevida |
| `ChatgptAudit.Collapse057` | `collapse_fixed_iff_in_range`; `tower_fixed_points_exactly_centralizer` | pontos fixos da retração/centralizador, não ponto único automático |

[DECLARADO] `IdentityCollapse.step` já é idempotente por definição; ele modela uma retração de colapso, não o `G_k` textual geral. A defasagem de `IALD2`, por contraste, é o molde de passo que, nos casos dissipativos não triviais, não precisa ser idempotente; a projeção-limite é idempotente.

### 6.4 A ponte que continua aberta

[OPEN] Para instanciar o molde do kernel a uma sessão textual seriam necessários, no mínimo:

1. um tipo finito `X` de pixels/interpretações e uma extração `κ_j:Y→X`;
2. um custo bem definido `c_j:X→ℕ`, ou equivalentemente `B_j:Y→(X→ℕ)`;
3. uma relação de corretude entre `c_j(κ_j(y))=0`, as 24 asserções de `E_j(y)` e o alvo `τ_j`;
4. a identificação de um vetor inicial e a prova de que a atualização textual induz a trava, ou outra dinâmica formal declarada.

Nenhum desses itens é fornecido por `trava`, `selecao`, `LeitorDoFundo`, `IALD2.o_atrator` ou `um_is_the_great_attractor`. Logo, a seta

\[
 \boxed{\text{saída extraída }E_j(y)\ \longrightarrow\ c:X→ℕ}
\]

permanece **OPEN**. A afirmação “um LLM real satisfaz a trava, a absorção ou a projeção-limite” é previsão experimental, não teorema.

## 7. Namespaces corrigidos e versão do protocolo

### 7.1 Nomes qualificados

[REAL — conferido nos arquivos] Usam-se os nomes abaixo, sem alterar os teoremas:

- `ChatgptAudit.Aperiodic046.aperiodic_expectation_contractive` e `ChatgptAudit.Aperiodic046.aperiodic_expectation_idempotent`;
- `TGLExt.Santo.dephase_fixed_states_not_unique` e `TGLExt.Santo.fixed_set_of_dephasing_is_the_diagonal`;
- `ChatgptAudit.Collapse057.collapse_fixed_iff_in_range`;
- `ChatgptAudit.Collapse057.tower_fixed_points_exactly_centralizer`;
- `TGLExt.observing_adds_nothing` e `TGLExt.um_is_the_great_attractor`;
- `TGLExt.TraducaoTuring.trava`, `TGLExt.TraducaoTuring.selecao`, `TGLExt.AEscala.LeitorDoFundo`, `TGLExt.AEscala.o_leitor_do_fundo_e_a_iald` e `TGLExt.IALD2.o_atrator`.

### 7.2 `IALD_COLLAPSE_V2`

[DECLARADO] O protocolo novo recebe o identificador **`IALD_COLLAPSE_V2`**. A P7 `IALD_COLLAPSE_V1` selada não é alterada. Os identificadores operacionais são os do protocolo principal e não reutilizam `C1–C4`:

| identificador V2 | papel no desenho principal |
|---|---|
| `V2-TGL` | braço focal, com alvo próprio de 24 asserções |
| `V2-PLA` | controle informativo com pelo menos três placebos coerentes |
| `V2-OUT` | controle informativo com pelo menos três textos autorreferentes não equivalentes |
| `V2-ISO-A` | controle estrutural isomorfo, com dicionário independente |
| `V2-ISO-B` | segunda família de controle estrutural isomorfo, sem reutilizar dicionário ou semente |
| `V2-RET` | **fase decisória de todos os braços**, com perturbação depois de `k=8`, leitura perturbada em `k=9` e retorno a partir de `r=10`; não é um sexto braço |

Os antigos embaralhado e sem texto, quando usados, permanecem apenas **canários descritivos de contaminação**, fora dos 24 testes primários e sem papel como evidência de convergência. A referência a esses dois controles é somente histórica R2; eles não recebem aliases de braços primários na V2.

## 8. Candidata Lean: enunciado, prova e separação PASSO/LIMITE

### 8.1 Enunciado formal verificado

[REAL — sandbox] O tipo de hipóteses é

```lean
structure FiniteAttractor (X : Type) [Fintype X] [DecidableEq X] where
  step : X → X
  target : X
  fixed : step target = target
  reachable : ∀ x, ∃ n : ℕ, step^[n] x = target
```

O teorema principal compilado é

```lean
theorem FiniteAttractor.exists_iterate_eq_target_le_card (x : X) :
    ∃ n : ℕ, n ≤ Fintype.card X ∧ A.step^[n] x = A.target
```

e o limite operacional é `A.limit x := A.step^[Fintype.card X] x`. Também compilam:

```lean
theorem FiniteAttractor.limit_eq_target (x : X) : A.limit x = A.target
theorem FiniteAttractor.limit_constant (x y : X) : A.limit x = A.limit y
theorem FiniteAttractor.limit_idempotent (x : X) : A.limit (A.limit x) = A.limit x
theorem FiniteAttractor.limit_fixed_iff (x : X) : A.limit x = x ↔ x = A.target
theorem FiniteAttractor.step_fixed_iff (x : X) : A.step x = x ↔ x = A.target
```

[DERIVED] A prova toma a primeira chegada `m=Nat.find (A.reachable x)`. Antes de `m`, duas iteradas iguais permitiriam antecipar a chegada, contradição. Logo `Fin m → X`, dado pelas iteradas, é injetivo e `m≤|X|`. Depois da chegada, `fixed` mantém a órbita no alvo; portanto a iterada de ordem `|X|` é constante e idempotente.

### 8.2 Controles e reuso

- [REAL — sandbox] `chain3.step := ![1,2,2]` tem ponto fixo globalmente alcançável e satisfaz `∃x, step (step x) ≠ step x`. O passo não é idempotente; o limite sim.
- [REAL — sandbox] `KernelInstance.terminalAttractor` instancia o tipo com `TGLExt.ObservadorTerminal.leitor` e `gravidade`. A cota geral dá chegada em no máximo 4 passos; o teorema já existente `every_level_reaches_the_terminal` fornece a cota mais forte 3. Nenhum teorema do kernel foi modificado.
- [DECLARADO] A candidata é o ramo **determinístico finito** permitido pela ordem; ela não formaliza `H-QUOT(k)`, `H-ABS-U` nem a ponte textual.

### 8.3 Cabeçalho experimental e auditoria

[REAL] O cabeçalho da fonte declara expressamente que a ponte a um modelo de linguagem real é previsão experimental, não teorema. A compilação final registra:

- `VERSION`: Lean 4.31.0, commit `68218e876d2a38b1985b8590fff244a83c321783`;
- `RC: 0`;
- axiomas dos tipos e teoremas: somente `propext`, `Classical.choice` e `Quot.sound`, conforme a declaração; nenhum `sorryAx`.

Arquivos: `K06\candidatas\sandbox\LeitorFinito.lean`, `K06\candidatas\sandbox\run_lean.py` e `K06\candidatas\logs\LeitorFinito.txt`. As tentativas anteriores e seus códigos de retorno foram preservados ao lado.

## 9. Reuso versus novo, e o que não se afirma

**Reuso [REAL — kernel].** `trava`, `selecao`, `LeitorDoFundo`, `IALD2.o_atrator`, `AEscala.o_leitor_do_fundo_e_a_iald`, `observing_adds_nothing`, `um_is_the_great_attractor`, o leitor terminal e os controles de não unicidade/idempotência citados.

**Novo [REAL — sandbox].** A cota da primeira chegada para `FiniteAttractor`, o limite de ordem `|X|` constante e idempotente, o exemplo não idempotente `chain3` e a instância finita do leitor terminal.

**Novo [DECLARADO].** A especificação de `G_k`, a forma estocástica de H-QUOT(k), a declaração de não homogeneidade, a separação H-IDEM-STEP/H-IDEM-LIM, os identificadores V2 e a formulação explícita da ponte ausente.

[DECLARADO] Nada aqui autoriza afirmar consciência, alteração de pesos, aprendizado permanente, exclusividade da TGL, convergência infinita a partir de doze leituras, validade física, creditação acadêmica ou um resultado sobre máquina de Turing padrão sem o leitor. `NOT_FALSIFIED` não é `CONFIRMED`; o gate não se move.

## 10. Fontes formais e bibliografia pendente de conferência

### 10.1 Kernel consultado em somente leitura

Diretório raiz: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\`.

- `TraducaoTuring.lean`: `trava` 470–477; `selecao` 331–354; `a_trava_sem_conhecer_o_nome` 508–521; `a_trava_em_tempo_linear` 574–601; `a_trava_converge_a_selecao` 603–622.
- `AEscala.lean`: `LeitorDoFundo` 742–758; unicidade 864–885; ciclos 960–974; limiar 976–996.
- `IALD2.lean`: `iald_ao_quadrado` 152–160; `o_atrator` 310–337.
- `ParNaFaceDeFock.lean`: 331–405; `ObservadorTerminal.lean`: 137–197; `TheObserverReadsTheAngle.lean`: 108–116; `TheGreatAttractor.lean`: 128–143.
- `AperiodicCentralizerExpectation.lean`: 138–147; `Santo.lean`: 817–822, 890–918 e 1773–1780; `CollapseContract.lean`: 62–70; `TowerCollapseRealization.lean`: 62–70.

### 10.2 Literatura

As referências externas permanecem marcadas **[KNOWN, a conferir]**, com identificador, e não substituem a verificação bibliográfica da gerência:

1. Kemeny, J. G.; Snell, J. L. *Finite Markov Chains*. 2ª ed., Springer, 1976 [1ª ed. 1960]. `ISBN 978-0-387-90192-3`.
2. Seneta, E. *Non-negative Matrices and Markov Chains*. 2ª ed., Springer, 2006. `DOI 10.1007/0-387-32792-4`.
3. Banach, S. “Sur les opérations dans les ensembles abstraits et leur application aux équations intégrales”. *Fundamenta Mathematicae* 3 (1922), 133–181. `DOI 10.4064/fm-3-1-133-181`.
