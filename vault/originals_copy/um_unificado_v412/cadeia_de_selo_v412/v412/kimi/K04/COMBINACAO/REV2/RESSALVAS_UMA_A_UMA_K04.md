# K04 — Seções D e E: as sete ressalvas, uma a uma, e o lugar de P7/K06

**Estatuto e proibição cumprida.** [DECLARADO] partitura para deliberação, não resultado. **Nenhuma conta desta seção foi executada.** Os números citados são apenas insumos já existentes no core, na revisão K01 ou no Mapa. Nenhum vetor observado foi lido; nenhum estimador, solver, `evaluate`, rotina de abertura ou `executar_abertura_v411.py` foi chamado; H0DN não foi reaberto.

A fonte das sete é `um_absoluto.json → h0dn_bg1_v411.values.ressalvas_secao8` (repetida no nível superior do registro). O que “resolve” é separado do que apenas “mede”: um número de desenho pode dimensionar uma fragilidade, mas não cria cegueira, independência, covariância ou história nova.

---

## CORREÇÃO AO LADO K09 — leitura vigente (15/11/2026)

[DECLARADO — redesenho documental após a revisão distinta; aguarda conferência da gerência.] O texto K04 permanece como estrato histórico. **Nenhuma das três contas foi executada, nenhum ponto novo de 5σ foi calculado, nenhum vetor foi lido e H0DN não foi reaberto.**

1. **R5:** a conta do piso somente nas 72 direções é inaplicável porque \(g^TP_{72}g=0\) por construção. A conta corrigida é o ruído independente e homoscedástico **por linha nas 111 linhas brutas**, com os pesos congelados. Os valores 6,66/6,31/0,104 e o selo 6,69 com \(\tau=0,0222\) são apenas histórico já pré-registrado/selado; os pontos de 5σ do primário e das Cefeidas livres ficam **desenhados, sem avaliar**.
2. **R3/R4:** “calibração” fica fixada **antes** como as **3 âncoras + 9 MAS** de `network\factors.json`; as **92 HMS** ficam fora da calibração e entram em \(V_{\rm other}\). O alvo 5 usa **\(Z\) esperado contra o nulo**; o alvo \(D_{90}\) usa **\(D\)**. Não se mistura \(Z=4,514\) com \(D=5,192\).
3. **R7:** entra o **\(p\) unilateral contra o nulo** (`values.primario.p_unilateral`), porque a multiplicidade diz respeito à tensão de Hubble; o acordo com K responde a outra pergunta. O censo exportado dá somente tetos — **16 rotas Hubble e 123 no Mapa** —, nunca \(N\) independente, e tem manifesto com consulta, data e SHA-256.
4. **P7/K06:** hoje está **em desenho e BLOQUEADA_PARA_PRODUCAO**, não “executável hoje”. P7 pergunta sobre o leitor, não sobre a natureza, e não resolve R1–R7.

As fórmulas, a partição nominal dos fatores, os hashes e o manifesto estão em `K04\COMBINACAO\K09\`; a errata-mãe é `ERRATA_COMBINACAO_K09.md`.

---

## Quadro-síntese: qual ATO resolve cada ressalva

| Ressalva | Ato que resolve de fato | O número de desenho pode fazer |
|---|---|---|
| **R1 — emenda pós-guarda; não cego** | **Teste cego novo**, com regra e custódia anteriores ao dado. A história da emenda permanece escrita. | Nada que apague a emenda passada. |
| **R2 — primário previsível por agregados** | **Dado independente e ainda não lido**, em teste cego novo. Retrodição sem ajuste continua evidência legítima, mas não vira novidade cega. | Nada que transforme agregado conhecido em dado novo. |
| **R3 — Cefeidas livres abaixo de 5** | **Dado/calibração independente** que melhore o orçamento e permaneça sempre visível. | Partitura da melhoria necessária para 5 e \(D_{90}\), sem executá-la. |
| **R4 — poder só no modelo publicado** | **Dado independente + covariância/sistemáticas certificadas**; linhas de estresse ao lado de qualquer \(D\) nominal. | Partitura do orçamento necessário e teste de viabilidade dos demais componentes do erro. |
| **R5 — 72 direções de variância zero** | **Orçamento/covariância independente** que substitua ou justifique os zeros. | Partitura do piso comum que levaria \(D=6,71\) a \(D_{90}\) e a 5, só com tabela e pesos congelados. |
| **R6 — escolhas com tabela de poder à vista** | **Teste cego novo**, com primário, portão, hipóteses e variantes fixados antes da tabela de poder e dos resultados. A história permanece. | Nenhum número retrospectivo elimina a seleção já ocorrida. |
| **R7 — tentativas e sobreposição** | **História declarada + livro de famílias/dependências**; futuras réplicas disjuntas e função global pré-registrada. | Partitura de Šidák somente para tentativas realmente independentes; não corrige sobreposição por si. |

---

## R1 — Emenda posterior à guarda e ausência de cegueira

**Texto da ressalva.** O ramo (1) foi emendado depois de se saber que o vetor público o reprovava; pela função anterior o desfecho seria inconclusivo por sistemática.

**Resolução.** Somente um **teste cego novo**, com hash público antes da liberação/abertura/comunicação, função de veredito completa e nenhuma emenda posterior. Não há partitura capaz de apagar a emenda histórica. O teste anterior deve continuar rotulado como retrodição sem ajuste, com emenda pós-guarda e não cego.

**Número ruim e reabertura.** Não se aplica. Qualquer reexecução do antigo pacote para “melhorar” o desfecho seria nova análise pós-hoc, não reparação retrospectiva; `executar_abertura_v411.py` nunca roda.

## R2 — Previsibilidade do primário por dois agregados públicos

**Texto da ressalva.** O primário era previsível por agregados públicos a menos de 0,18 desvio; o rito conferiu a conta, não descobriu um número novo.

**Resolução.** Exige **dado independente, ainda não lido**, guardado por terceiro e aberto uma única vez sob regra anterior. Reanalisar a mesma rede ou reproduzir os mesmos agregados não resolve. Retrodição sem ajuste não é demérito; apenas pertence a outra categoria epistêmica.

**Número ruim e reabertura.** Não se aplica. Repetir a estimativa com os dados já conhecidos seria reabrir a pergunta sem criar cegueira.

## R3 — A linha das Cefeidas livres precisa alcançar 5 e \(D_{90}\)

**Texto da ressalva.** A linha ao lado tinha esperança de desenho de aproximadamente 4,5σ e 23 % de chance de passar de 5; nas três linhas de estresse, o esperado também ficava abaixo de 5.

**Ato.** Resolver exige **nova calibração/dado independente**. A conta abaixo apenas informa qual melhoria de erro seria necessária e se os demais componentes impediriam o alvo.

### Partitura R3 — não executada

**Insumos, sem vetor observado:**

- `network.npz`, sha256 `3dd073c3a74abf34ef3d80368456a2698e8405a52417057149a35a8a5a5a6832` — tabela pública e decomposição do orçamento;
- `estimator_frozen.npz`, sha256 `059ef7b6f2c671406058fdb6e647c011851e5761da91784b4ce213e9abbe07b8` — pesos congelados da linha;
- `BG1.json`, sha256 `87b475a05700ddc2074217761502e239d6f33b1ad74ff5a763e1b577b724f6ca` — fundo e convenção;
- `EMENDA_E_PRE_REGISTRO_V411.md`, sha256 `06af740a8812a622a6bc0c7fbd252f4d824c1428c7b0c62e313ccd3ae75199c8` — definição da linha e regras;
- core `h0dn_bg1_v411.values.esperado_pelos_agregados`: \(Z_{\rm exp}=4,514141429613277\) para Cefeidas livres, usado como **planejamento**, não como novo resultado.

**Definições.** Seja \(A=|\mu_{0,C}-\mu_{P,C}|\) a separação esperada entre nulo e previsão na linha, calculada exclusivamente dos pesos e da lei congelados. Decomponha

\[
V_{\rm tot,0}=V_{\rm other}+V_{\rm cal,0},
\qquad Z_{\rm exp}=A/\sqrt{V_{\rm tot,0}}.
\]

Aqui \(V_{\rm cal,0}\) é a variância atribuível à calibração a melhorar e \(V_{\rm other}\) reúne todos os outros termos, sem reajustar nenhum ao resultado. Se a variância de calibração for multiplicada por \(f>0\),

\[
Z_C(f)=\frac{A}{\sqrt{V_{\rm other}+fV_{\rm cal,0}}}.
\]

Para cada alvo \(q\in\{5,\;D_{90}=6,281551565544601\}\), a partitura pede:

\[
\boxed{
f_q=\frac{A^2/q^2-V_{\rm other}}{V_{\rm cal,0}},
\qquad
r_q=\sqrt{f_q},
\qquad
\Delta V_q=1-f_q
}
\]

onde \(r_q\) é o fator sobre o **desvio-padrão** de calibração e \(\Delta V_q\) a redução fracionária de **variância**. Não se avalia \(f_q\), \(r_q\) ou \(\Delta V_q\) nesta K04.

Como caso-limite, somente se \(V_{\rm other}=0\), a fórmula se reduz a \(f_q=(Z_{\rm exp}/q)^2\); essa suposição não pode ser adotada sem a decomposição real do orçamento.

**Leitura de um número ruim.** \(f_q<0\) significa que os outros erros, sozinhos, já impediriam o alvo mesmo com calibração perfeita; \(f_q>1\) indicaria que a suposta “melhoria” na verdade pioraria o erro. Uma redução de variância irrealizável também mostraria fragilidade do orçamento/poder publicado. **Nada disso falsifica a lei**: mede a fragilidade do modelo de erros e do desenho.

**Rodar é reabrir?** Uma futura conta autônoma, apenas com a tabela, os pesos e a separação teórica, não reabriria H0DN; ler o vetor, reestimar a linha ou chamar o estimador/abertura seria nova análise e está fora da permissão. Melhorar a calibração com dados novos constitui experimento novo, não reabertura retrospectiva. **Nada foi rodado.**

## R4 — Poder de desenho condicionado ao modelo publicado

**Texto da ressalva.** O \(D\) é de desenho no modelo publicado; as linhas de estresse devem acompanhá-lo.

**Ato.** Exige **covariância física e orçamento de sistemáticas independentes**, além de eventual dado novo. A mesma partitura de R3 informa o alvo nominal, mas R4 só é respondida quando as linhas de estresse e a covariância conjunta deixam de ser uma advertência aberta.

### Partitura R4 — não executada

Reutilizam-se os arquivos e hashes de R3, mais:

- `estimador_s0_v411.npz`, sha256 `6cc9a23c4aa7b9ffe4d925273d044ac007d3646506bc5d3d80160e1ee839a617` — convenção do suporte/estimador, sem uso de vetor;
- core `h0dn_bg1_v411.values.cefeidas_livres.D=5,19131201002441`, somente como referência histórica já selada, não como insumo para novo Z.

**Conta desenhada.** Repetir a decomposição de R3 separando explicitamente

\[
V_{\rm other}=V_{\rm stat}+V_{\rm cov}+V_{\rm sys}+V_{\rm model}.
\]

Para cada \(q\in\{5,D_{90}\}\), verificar **antes** de aceitar qualquer \(f_q\):

1. \(V_{\rm stat}+V_{\rm cov}+V_{\rm sys}+V_{\rm model}\leq A^2/q^2\), caso contrário não existe melhoria de calibração suficiente;
2. as mesmas quatro parcelas aparecem nas três linhas de estresse previamente nomeadas, sem escolher a mais favorável;
3. o \(D\) nominal e os \(D\) de estresse são apresentados no mesmo item, sem substituir o modelo publicado por um modelo escolhido depois.

**Leitura de um número ruim.** Se o orçamento residual impede o alvo ou uma linha de estresse perde o portão, a conclusão é **fragilidade do erro publicado/modelo de covariância**, não falsificação da lei. Um \(D\) nominal alto com estresse baixo não resolve R4.

**Rodar é reabrir?** Não se se limitar à álgebra de desenho sem vetor; torna-se nova análise se recalcular covariância física com dados, estimadores ou resultados observados. Isso exigiria ato novo e não foi feito.

> **CORREÇÃO AO LADO K09 — R3/R4: partição e duas bases fixadas antes.**
>
> **1. O que é “calibração” nesta partitura.** Fica fixada, antes de qualquer \(f_q\), a partição documental dos **104 fatores** de `work\astra_bell_fock_tt_05nov\h0dn_bg1_06nov\network\factors.json`, sha256 **`2de3cbfe475441765c1c9eb34d57a1eb56b95faab58b6cb203e0545c2ed02212`**:
>
> - **ENTRAM em \(V_{\rm cal,0}\): as 3 âncoras** (`anchor` 0–2: LMC, MW, N4258), incertezas geométricas de referência, e **as 9 MAS** (`MAS` 0–8), incertezas *method–anchor–source* associadas às linhas de referência das âncoras: `ceph_hst&LMC&R22`, `ceph_hst&MW&R22`, `ceph_hst&N4258&R22`, `ceph_jwst&N4258&SH0ES`, `trgb_hst&N4258&CCHP`, `trgb_hst&N4258&Ex`, `trgb_jwst&N4258&A25`, `trgb_jwst&N4258&CCHP`, `trgb_jwst&N4258&SH0ES`. Ambas têm semântica `all_pairs_including_diagonal`.
> - **NÃO ENTRAM: as 92 HMS** (`HMS` 0–91), incertezas *host–method–source* de medidas de hospedeiros; sua semântica é `off_diagonal_only`, com a diagonal já contida em `mu_error` do hospedeiro. Elas ficam em \(V_{\rm other}\), junto com os demais termos estatísticos, de covariância, sistemática e modelo.
>
> **Razão documental:** a pergunta é melhorar a referência de calibração da escada, não reduzir retroativamente erros de medidas individuais de hospedeiros. O código-fonte upstream nomeia âncoras geométricas, referências MAS e medidas HMS exatamente com esses três papéis. A partição é uma escolha de desenho **[DECLARADO]**, fixada agora e não mutável depois de ver \(f_q\); a gerência deve ratificá-la antes de rodar. O hash acima foi lido dos bytes e também consta no `MANIFEST.json` da rede.
>
> Com \(F_{\rm cal}=(F_{\rm anchor}\;F_{\rm MAS})\), define-se **sem avaliar**:
> \[
> C_{\rm cal}=F_{\rm cal}F_{\rm cal}^T,\qquad
> V_{\rm cal,0}=w^TC_{\rm cal}w,\qquad
> V_{\rm other}=V_{\rm tot,0}-V_{\rm cal,0}.
> \]
>
> **2. Duas bases, sem mistura.** A fórmula comum, apenas simbólica, é
> \[
> f(q;A)=\frac{A^2/q^2-V_{\rm other}}{V_{\rm cal,0}}.
> \]
>
> - **Base Z, somente para o alvo 5:** \(A_Z/\sqrt{V_{\rm tot,0}}=Z_{\rm nulo,exp}=4,514141429613277\), de `values.esperado_pelos_agregados[1].z_nulo_esperado`; usa-se \(f(5;A_Z)\). É a esperança contra o nulo dado o agregado, com os 23 % já pré-registrados apenas como contexto.
> - **Base D, somente para o portão de 90 %:** \(A_D/\sqrt{V_{\rm tot,0}}=D_0=5,19131201002441\), de `values.cefeidas_livres.D`; usa-se \(f(D_{90};A_D)\), com \(D_{90}=6,281551565544601\).
>
> **\(Z=4,514\) não entra como \(D=5,192\), nem o inverso.** São perguntas e numeradores distintos, ainda que próximos numericamente; o acordo esperado com K (`z_K_esperado=-0,6777408098403498`) fica nomeado à parte e não é trocado pelo \(D\).
>
> **3. Estresses que devem ficar ao lado.** O pré-registro §7 já traz, para o modelo publicado e Cefeidas livres, respectivamente: **S1: 5,489825 / 4,743268; S2: 5,527887 / 4,773510; S4: 4,378058 / 3,871970** `[DECLARADO pelo Kimi no pré-registro]`. S4 já está abaixo de 5. Também permanecem o viés comum desfavorável de **0,0156 mag** que tira o primário do portão de 90 % e o de **0,1816 mag** que fabricaria 5σ. Nenhuma partição ou fórmula acima foi avaliada na K09.

## R5 — Piso de variância nas 72 direções

**Texto da ressalva.** A tabela publicada declara variância zero em 72 direções. Isso não move o valor estimado, mas pesa no crédito do desvio.

**Ato.** Resolver exige **orçamento/covariância independente**. A partitura apenas responde: “se essas direções receberem um piso comum \(v\), qual \(v\) faria o \(D\) nominal cruzar os dois limiares?”

### Partitura R5 — não executada

**Insumos estritamente permitidos:**

- `network.npz`, sha256 `3dd073c3a74abf34ef3d80368456a2698e8405a52417057149a35a8a5a5a6832` — tabela de erros publicada;
- `estimator_frozen.npz`, sha256 `059ef7b6f2c671406058fdb6e647c011851e5761da91784b4ce213e9abbe07b8` — base e pesos congelados;
- `BG1.json`, sha256 `87b475a05700ddc2074217761502e239d6f33b1ad74ff5a763e1b577b724f6ca` — previsão congelada;
- core `h0dn_bg1_v411.values.primario.D=6,710150598579069`, usado apenas como ponto de referência do desenho já selado;
- `EMENDA_E_PRE_REGISTRO_V411.md`, sha256 `06af740a8812a622a6bc0c7fbd252f4d824c1428c7b0c62e313ccd3ae75199c8` — definição do \(D\) de desenho.

**Proibido como insumo:** `vetor_y255.npz`, qualquer resultado observado, posterior ou amostra. O executor citado no registro, sha256 `2e5837a7a3794dadefdc6ea812d6da0232e1f18cbc3c8e5a0d890ea48edc8655`, **nunca roda**.

**Construção.** Na base congelada do estimador, escreva

\[
C_0=U\operatorname{diag}(c_j)U^T,
\qquad \mathcal Z=\{j:c_j=0\},
\qquad |\mathcal Z|=72.
\]

Defina \(P_{72}\) como o projetor sobre essas direções e \(C(v)=C_0+vP_{72}\), com \(v\geq0\) em unidades de variância da tabela. Seja \(g\) o contraste congelado entre a previsão e o nulo e \(A=|g^T\Delta\mu|\) a separação teórica, **sem uso do vetor observado**. Então

\[
\sigma^2(v)=g^TC(v)g=\sigma_0^2+v\,g^TP_{72}g,
\qquad
D(v)=\frac{A}{\sigma(v)}.
\]

Para \(q\in\{D_{90}=6,281551565544601,\;5\}\), o piso procurado é a expressão **não avaliada**

\[
\boxed{
v_q=\frac{A^2/q^2-\sigma_0^2}{g^TP_{72}g}
=\frac{\sigma_0^2\left[(D_0/q)^2-1\right]}{g^TP_{72}g},
\qquad D_0=6,710150598579069.
}
\]

Pesos, base e previsão permanecem fixos; não se faz nova diagonalização, pseudoinversa, normalização, escolha de piso ou otimização. Se \(g^TP_{72}g=0\), essas direções não afetam o contraste e a fórmula não se aplica; se o numerador for negativo, o limiar já foi cruzado sem piso adicional.

**Leitura de um número ruim.** Um piso pequeno que derruba \(D\) abaixo de \(D_{90}\) ou de 5 indica **fragilidade do erro publicado**, não falsificação da lei. Um piso grande sem efeito não certifica que os zeros eram fisicamente corretos: pode significar apenas que o contraste não recebe informação daquelas direções.

**Rodar é reabrir?** Uma avaliação futura puramente algébrica de \(C_0,g,P_{72}\), sem vetor nem resultado, é análise de desenho e não reabre H0DN. Ler `vetor_y255.npz`, recalcular \(t\), Z ou ramo, ou chamar qualquer módulo da pasta de abertura ultrapassa a permissão e caracteriza nova análise/abertura. **Nada foi rodado.**

> **CORREÇÃO AO LADO K09 — R5: a conta que existe é por linha, não nas 72 direções.**
>
> O denominador \(g^TP_{72}g\) da fórmula anterior é **zero por construção**, não um caso excepcional: os pesos ficam no suporte da covariância e são ortogonais à base nula, como o próprio pré-registro §7(i) declara. Aquela fórmula fica retirada como desenho executável. A R5 continua exigindo orçamento/covariância independente; nenhum ruído calculado substitui esse ato.
>
> **Modelo corrigido, somente simbólico.** Seja \(\mathcal R\) o conjunto das **111 linhas brutas** e \(m\in\{\mathrm{primário},\mathrm{Cefeidas\ livres}\}\). Mantenha os pesos \(w_m\) congelados e acrescente \(R_{\rm extra}=\tau^2I_{111}\), com \(\tau\) em mag. Defina \(A_m\) e \(\sigma_{0,m}\) somente pelo desenho, sem vetor observado:
> \[
> S_m=\sum_{r\in\mathcal R}w_{m,r}^2,\qquad
> D_m(\tau)=\frac{A_m}{\sqrt{\sigma_{0,m}^2+\tau^2S_m}}
> =\frac{D_{0,m}}{\sqrt{1+\tau^2S_m/\sigma_{0,m}^2}}.
> \]
> Para \(q<D_{0,m}\), o ponto procurado é a expressão **não avaliada**
> \[
> \boxed{\tau_{m,q}=\sqrt{\frac{\sigma_{0,m}^2[(D_{0,m}/q)^2-1]}{S_m}}}
> \qquad\text{ou, equivalentemente,}\qquad
> \boxed{\tau^2_{m,q}=\frac{A_m^2/q^2-\sigma_{0,m}^2}{S_m}}.
> \]
>
> **Insumos e pinos, sem abrir NPZ:**
>
> - `estimator_frozen.npz`, pesos/base congelados, sha256 `059ef7b6f2c671406058fdb6e647c011851e5761da91784b4ce213e9abbe07b8`; `estimador_s0_v411.npz`, pesos do desenho primário, sha256 `6cc9a23c4aa7b9ffe4d925273d044ac007d3646506bc5d3d80160e1ee839a617`;
> - `EMENDA_E_PRE_REGISTRO_V411.md` §7(i), sha256 `06af740a8812a622a6bc0c7fbd252f4d824c1428c7b0c62e313ccd3ae75199c8`;
> - core `h0dn_bg1_v411.values.decomposicao_conferencias`, arquivo sha256 `36c69fc767f8d47f318f134ecdfb6bd2d39ad25f17f9b9310b196afb0a19064e`: `soma_w2 = [0,00035410915546846196; 0,0003247313944942674]` e `sum_w2_touched = [0,00035410915546846196; 0,00032473139449426747]`, na ordem [primário; Cefeidas livres]. O valor 0,000354 do pré-registro é o arredondamento do primeiro.
>
> **O que já existia — e o que falta.** O pré-registro já trazia, para o primário, **6,6571 (≈6,66) com \(\tau=0,035\) mag**, **6,3109 (≈6,31) com 0,10 mag** e a perda do portão de 90 % em **0,104 mag**. O selo traz \(\hat\tau=0,0222442927187763\) (≈0,0222), estimado do próprio vetor, portanto **pós-observação e não cego**, com **D = 6,688588 (≈6,69) no primário e 5,182136 nas Cefeidas livres**. Esses números são histórico citado, não resultado novo. **Ficam nomeados os dois pontos de 5σ:** \(\tau_{\rm primário,5}\) e \(\tau_{\rm Cefeidas,5}\); falta apenas a sua avaliação, somente se autorizada depois. O ponto \(D_{90}\) do primário já está pré-registrado; nas Cefeidas livres \(D_0<D_{90}\), logo ruído adicional não pode “alcançar” \(D_{90}\). \(\hat\tau\) não entra como insumo de um novo desenho cego.
>
> **Nada foi avaliado:** nem os dois pontos de 5σ, nem \(D_m(\tau)\), nem qualquer vetor, projeção ou reestimativa.

## R6 — Escolhas feitas com a tabela de poder à vista

**Texto da ressalva.** Primário, portão de 90 % e hipóteses foram escolhidos com a tabela de poder à vista; os agregados dos dois lados eram públicos.

**Resolução.** Exige **teste cego novo**, com a família completa de primário, portão, hipóteses, variantes, pesos e regra de combinação fixada antes de qualquer tabela de poder ou resultado. Não se escolhe agora a variante que melhor performa. A seleção anterior permanece como história e não é apagada por um novo teste.

**Número ruim e reabertura.** Não se aplica. Repetir variantes para selecionar a melhor seria continuar a mesma contaminação, não resolvê-la.

## R7 — Tentativas anteriores, independência e sobreposição

**Texto da ressalva.** Há tentativas anteriores e sobreposição dos dados locais; o próprio core nega independência das Fases 4, 5 e 9.

**Ato.** Resolver exige **história declarada e um livro de famílias/dependências**, não um denominador conveniente. Uma futura réplica disjunta pode criar evidência nova, mas não apaga tentativas passadas. Se a independência não for demonstrável, a correção deve usar a distribuição conjunta do máximo, modelo hierárquico ou outra regra pré-registrada que reconheça a dependência.

### Partitura R7-A — número de tentativas independentes, não executado

**Insumos:**

- arquivo `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json`, chave `h0dn_bg1_v411.values.primario`; SHA-256 atual, lido por script: `36c69fc767f8d47f318f134ecdfb6bd2d39ad25f17f9b9310b196afb0a19064e`;
- nessa chave, já selados: \(z_{\rm local}=6,1057575347088955\) e \(p_{\rm local}=5,115711574207153\times10^{-10}\);
- definição unilateral \(p_{5\sigma}=1-\Phi(5)\);
- Mapa de Rotas, abaixo, para o livro de tentativas e dependências.

Sob **independência verdadeira** entre \(N\) tentativas,

\[
p_{\rm global}(N)=1-(1-p_{\rm local})^N,
\qquad
Z_{\rm global}=\Phi^{-1}(1-p_{\rm global}).
\]

O menor número que faria o resultado global atingir ou perder o nível unilateral de 5σ seria a expressão **não avaliada**

\[
\boxed{
N_\star=\left\lceil
\frac{\ln(1-p_{5\sigma})}{\ln(1-p_{\rm local})}
\right\rceil.
}
\]

Não se calcula \(N_\star\), \(p_{\rm global}\) nem \(Z_{\rm global}\) nesta K04. A fórmula de Šidák não se aplica a DR1/DR2 como se fossem independentes, a reanálises do mesmo vetor, a variantes do mesmo fundo, a reproduções computacionais nem a Fases 4/5/9/H0DN como blocos separados sem covariância.

**Leitura de um número ruim.** Um \(N_\star\) pequeno mostraria fragilidade do crédito global diante do look-elsewhere, **não falsificação da lei**. Um \(N_\star\) grande não demonstra independência nem validade do erro publicado; só caracteriza o quanto a significância local seria diluída sob a hipótese idealizada.

**Rodar é reabrir?** Avaliar a fórmula sobre o \(p\) já selado seria aritmética pós-hoc, não reabertura mecânica de H0DN, mas seria uma **nova avaliação estatística observada**, exigindo deliberação separada. Não foi feita. Reabrir vetor, estimador ou executor permanece proibido.

### Partitura R7-B — contagem honesta pelo Mapa

O Mapa **não fornece hoje um \(N_{\rm indep}\) fechado e defensável**. O que ele fornece é:

1. `investigacao.bancada_um_28set`, seq 65: o cálculo histórico de P2 usou **4 famílias** no livro de Šidák; seq 66: P1 usou **5 famílias**. Esses números são os denominadores adotados naqueles dois relatórios, não uma prova de independência.
2. `gate.maquina_do_veredito_final`, seq 122 (EV-07): a própria auditoria registra ausência de correção entre famílias e que o fator do Mapa **conta menos tentativas do que o core**. Logo, nem 4 nem 5 podem ser promovidos a censo completo.
3. Fases 1–5, Fase 9 e H0DN contêm variantes com Planck, DESI DR1/DR2, Pantheon/SH0ES, calibradores e fundos compartilhados. A Fase 4 diz explicitamente que DR1 e DR2 não se somam; o core v411 diz que H0DN não é evidência independente das Fases 4, 5 e 9.
4. Reproduções independentes de código, conferências de hash e reanálises do mesmo resultado aumentam confiança computacional, **não** o número de tentativas independentes de dados.

**Contagem honesta resultante:** as rotas citadas **não identificam uma réplica integralmente disjunta que autorizasse tratar as fases como tentativas independentes**. Isso não autoriza usar \(N=0\) para escapar da multiplicidade: significa que o denominador independente é **[OPEN]** e que a correção por dependência é obrigatória. Contar 20 canais de K01, todas as fases ou todas as linhas do Mapa como \(N\) seria tão inválido quanto adotar 4 ou 5 sem a auditoria.

**Partitura para fechar o livro antes de qualquer correção global:** uma linha por tentativa com `rota_id`, seq, hipótese, dados, calibradores, fundo, sobreposição de objetos, covariância, data de conhecimento, cegueira e papel (teste, réplica, validação ou reprodução). Para o futuro censo, é obrigatória uma consulta/exportação do Mapa acompanhada de **manifesto de snapshot**, com caminho, data, consulta realizada, SHA-256 do manifesto e SHA-256 do artefato exportado; leituras soltas sem esse pacote não bastam. Só então decidir quais entram em Šidák, quais entram numa distribuição conjunta e quais não são tentativa estatística.

> **CORREÇÃO AO LADO K09 — R7: o \(p\) escolhido e o censo exportado.**
>
> **1. O \(p\) que entra é o contra o nulo.** Usa-se `h0dn_bg1_v411.values.primario.p_unilateral` = **5,115711574207153×10⁻¹⁰**, associado a `z_null` = **6,1057575347088955**, não um \(p\) de acordo com K. A razão é que R7 trata das tentativas anteriores da mesma lei e da diluição da **tensão de Hubble contra o nulo**; o acordo com K responde a outra pergunta e não mede essa tensão. Os nomes de campo reais são `z_null` e `p_unilateral`. **Não se calcula \(N_\star\), \(p_{\rm global}\), \(Z_{\rm global}\) nem qualquer correção de Šidák.** A fórmula só teria sentido sob independência demonstrada; as contagens abaixo não a estabelecem.
>
> **2. Censo e manifesto entregues.** A exportação `K04\COMBINACAO\K09\CENSO_R7_MAPA_K09.json` contém apenas metadados (`seq`, `rota_id`, data, tipo, domínio e a marca `olhou_dados`), sem resultado científico. O manifesto `MANIFESTO_CENSO_R7_MAPA_K09.json` registra a consulta, a data de 15/11/2026, o filtro `seq ≤ 2062` que preserva o universo examinado pelo revisor, o SHA-256 do Mapa vivo lido (`558d49b9d9cd04a9b198152e8aac75201d309ac91a5b5586247d97e46044bc6c`) e o SHA-256 da exportação (`08ad355c3b647a2db07128d826281c724f61206c329e284635cf9f63cfc125ea`).
>
> O recorte contém 2.062 registros e 505 rotas; 285 registros marcaram `olhou_dados=true`, correspondendo a **123 rotas no Mapa**; o subconjunto `d1.*`/`hubble.*`/`h0dn` contém **16 rotas**. **16 e 123 são tetos de contagem, não números de tentativas independentes e não denominadores de Šidák.** Rotas podem repetir dados, hipóteses, calibradores, fundos e análises. \(N_{\rm indep}\) permanece **[OPEN]**.

---

## E — O que P7/K06 pode e não pode dizer

A leitura da gerência está **correta no plano empírico, com uma precisão pequena**: P7/K06 é um teste cego executável hoje sobre **convergência do leitor**, não sobre natureza, e portanto não resolve nenhuma das sete ressalvas de H0DN — não desfaz a emenda (R1), não cria dado novo (R2), não melhora calibração (R3), não certifica o modelo de erros (R4), não preenche as 72 variâncias (R5), não apaga escolhas com poder à vista (R6) e não fornece tentativas independentes ou covariância (R7). A precisão é que P7 pode oferecer **disciplina metodológica** de tranca, controles, extração e função de veredito para um experimento futuro, mas isso é resposta a outra pergunta e não reduz nenhuma ressalva empírica; convergência do leitor não é evidência sobre H0, Cefeidas, covariância ou β na natureza.

> **CORREÇÃO AO LADO K09 — E/P7.** A frase “executável hoje” fica superada. **P7/K06 está em desenho e BLOQUEADA_PARA_PRODUCAO.** A R3.2 não fecha a separação entre resumo e convergência; o extrator está FAIL/bloqueado, modelos/tokenizers/janelas estão OPEN/bloqueados, e os poderes ideais já relatados de 0,599 e 0,669 não atingem 0,90. P7 continua sendo pergunta sobre o **leitor**, não sobre a natureza, e não resolve R1–R7. Fonte: `DEGRAU_5_SIGMA_K06.md`, sha256 `a82819f4dc726a6e8de9d99cfc8e7d433d75b27faa4cb88ad97613139019cb66`; nenhum modelo foi executado nesta K09.

## Bloqueios para qualquer execução futura

1. Decomposição real do orçamento de calibração e das covariâncias, sem vetor observado.
2. Contraste e projeção das 72 direções lidos apenas dos objetos congelados e validados por hash.
3. Livro de tentativas e dependências fechado; Šidák somente onde independência for demonstrada.
4. Autorização explícita para qualquer cálculo novo de desenho; nenhum programa de abertura, sobretudo `executar_abertura_v411.py`.
5. Número ruim significa fragilidade do erro/desenho, nunca falsificação automática da lei; `NOT_FALSIFIED` não é `CONFIRMED`, e o gate não se move.

**Nenhum teste, cálculo de piso, melhoria de orçamento ou correção global foi executado.**

> **Bloqueios corrigidos K09.** O item 2 acima é substituído, para qualquer desenho futuro, por: **pesos das 111 linhas e \(S_m\) lidos dos objetos congelados/selados por hash; a fórmula nas 72 direções não roda**. Antes de R3/R4, a gerência precisa ratificar a partição 3 âncoras + 9 MAS / 92 HMS fora e as duas bases \(Z\)-contra-o-nulo e \(D\). Antes de R7, o livro de dependências continua aberto: 16/123 são tetos, não independência. P7 não entra como saída operacional enquanto permanecer bloqueada. **Nenhum teste, ponto de 5σ, \(f_q\), \(N_\star\), valor global, vetor, estimador ou abertura foi executado na K09.**
