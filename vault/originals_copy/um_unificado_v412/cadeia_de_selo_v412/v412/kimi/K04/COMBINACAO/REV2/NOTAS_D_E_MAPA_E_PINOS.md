# NOTAS D–E K09 — fórmulas, partição, censo e bloqueios

15/11/2026. Estas notas acompanham as correções AO LADO de `RESSALVAS_UMA_A_UMA_K04.md`. **Nenhuma das três contas foi executada.** Não se avaliou \(f_q\), \(\tau_{m,5}\), \(N_\star\), \(p_{\rm global}\), \(Z_{\rm global}\) ou qualquer estatística nova. Nenhum NPZ ou vetor observado foi aberto; os NPZ são apenas nomeados com seus pinos.

## 1. Fontes e hashes

- `ORDEM_K09_teste_as_cegas_rodada_3.md`, seções D/E, sha256 `f5a9985bb6773aa73539e3ee1848daf34b2adc5b412fc297812c9281308d28b4`.
- `REVISAO_K04_COMBINACAO_RESSALVAS.md`, integral, sha256 `c49a911a263fe6bcfc07ca9807a673dc827903a62063696055fb4901061472b4`.
- `RESSALVAS_UMA_A_UMA_K04.md` antes da K09, sha256 `7119440be0353010f59b527c001d3ca13e8fe9fb0e27bb838258a7bf9e0c2eee`.
- `EMENDA_E_PRE_REGISTRO_V411.md`, especialmente §7, sha256 `06af740a8812a622a6bc0c7fbd252f4d824c1428c7b0c62e313ccd3ae75199c8`.
- `um_absoluto.json`, registro `h0dn_bg1_v411`, sha256 `36c69fc767f8d47f318f134ecdfb6bd2d39ad25f17f9b9310b196afb0a19064e`.
- `estimator_frozen.npz`, sha256 `059ef7b6f2c671406058fdb6e647c011851e5761da91784b4ce213e9abbe07b8` — pesos/base congelados; não aberto.
- `estimador_s0_v411.npz`, sha256 `6cc9a23c4aa7b9ffe4d925273d044ac007d3646506bc5d3d80160e1ee839a617` — desenho primário; não aberto.
- `network.npz`, sha256 `3dd073c3a74abf34ef3d80368456a2698e8405a52417057149a35a8a5a5a6832` — tabela publicada; não aberto.

## 2. R5 — ruído por linha nas 111 brutas

### 2.1 Por que a fórmula anterior não existe como conta

A fórmula do piso somente nas 72 direções tem \(g^TP_{72}g=0\) **por construção**: os pesos estão no suporte da covariância e são ortogonais à base nula. O pré-registro §7(i) já dizia que ruído somente nessas direções não acrescenta nada. A fórmula histórica permanece no documento K04, mas está expressamente retirada como desenho executável pela correção K09.

### 2.2 Fórmula corrigida, sem avaliação

Para \(m\in\{\mathrm{primário},\mathrm{Cefeidas\ livres}\}\), \(\mathcal R\) contém as 111 linhas brutas. Mantêm-se os pesos \(w_m\), a separação teórica \(A_m\) e a variância de desenho \(\sigma_{0,m}^2\), todos sem vetor observado. O ruído adicional é independente e homoscedástico, \(R_{\rm extra}=\tau^2I_{111}\), com \(\tau\) em mag:

\[
S_m=\sum_{r\in\mathcal R}w_{m,r}^2,\qquad
D_m(\tau)=\frac{A_m}{\sqrt{\sigma_{0,m}^2+\tau^2S_m}}
=\frac{D_{0,m}}{\sqrt{1+\tau^2S_m/\sigma_{0,m}^2}}.
\]

Para \(q<D_{0,m}\), o ponto de limiar é somente uma expressão:

\[
\tau_{m,q}=\sqrt{\frac{\sigma_{0,m}^2[(D_{0,m}/q)^2-1]}{S_m}}
\quad\Longleftrightarrow\quad
\tau_{m,q}^2=\frac{A_m^2/q^2-\sigma_{0,m}^2}{S_m}.
\]

Referências já seladas: \(D_{0,\rm primário}=6,710150598579069\) e \(D_{0,\rm Cefeidas}=5,19131201002441\). Em `values.decomposicao_conferencias`:

- `soma_w2 = [0,00035410915546846196; 0,0003247313944942674]`;
- `sum_w2_touched = [0,00035410915546846196; 0,00032473139449426747]`;
- ordem: [primário; Cefeidas livres]; o pré-registro arredonda o primeiro para 0,000354.

### 2.3 O que os números antigos significam

| Origem | Valor já existente | Leitura correta |
|---|---|---|
| Pré-registro §7(i), primário | \(D=6,6571\) com \(\tau=0,035\) mag | Arredondado, **6,66**; não é cálculo K09. |
| Pré-registro §7(i), primário | \(D=6,3109\) com \(\tau=0,10\) mag | Arredondado, **6,31**; ainda acima de \(D_{90}\) por pouco. |
| Pré-registro §7(i), primário | perda do portão em \(\tau=0,104\) mag | É o ponto \(D_{90}\) já pré-registrado; não se recalcula. |
| Selo `values.estresse.i_tau_por_linha` | \(\hat\tau=0,0222442927187763\), \(D=[6,688588090522991;5,182135752620312]\) | **6,69 com τ≈0,0222** no primário e 5,1821 nas Cefeidas; \(\hat\tau\) veio do próprio vetor, **pós-observação, não cego**. |

Falta somente a futura avaliação autorizada dos pontos de 5σ: \(\tau_{\rm primário,5}\) e \(\tau_{\rm Cefeidas,5}\). A K09 escreve a fórmula dos dois e não avalia nenhum. Como \(D_{0,\rm Cefeidas}<D_{90}\), ruído adicional não pode fazê-la alcançar \(D_{90}\). O \(\hat\tau\) pós-observação não entra como insumo de um novo desenho cego.

## 3. R3/R4 — calibração definida antes e duas bases

### 3.1 Partição documental fixada

Arquivo: `work\astra_bell_fock_tt_05nov\h0dn_bg1_06nov\network\factors.json`; **104 fatores**; sha256 lido dos bytes e conferido no `MANIFEST.json`:

`2de3cbfe475441765c1c9eb34d57a1eb56b95faab58b6cb203e0545c2ed02212`.

| Família | Papel documental | Partição fixada |
|---|---|---|
| **3 `anchor`**: LMC, MW, N4258 | Incerteza geométrica das âncoras de referência; `all_pairs_including_diagonal`. | **CALIBRAÇÃO** |
| **9 `MAS`**: method–anchor–source | Incerteza das referências método–âncora–fonte ligadas às linhas de âncora; `all_pairs_including_diagonal`. | **CALIBRAÇÃO** |
| **92 `HMS`**: host–method–source | Incerteza de medidas de hospedeiros; `off_diagonal_only`, com diagonal já em `mu_error`. | **OUTRO**, não calibração |

As 9 MAS são: `ceph_hst&LMC&R22`, `ceph_hst&MW&R22`, `ceph_hst&N4258&R22`, `ceph_jwst&N4258&SH0ES`, `trgb_hst&N4258&CCHP`, `trgb_hst&N4258&Ex`, `trgb_jwst&N4258&A25`, `trgb_jwst&N4258&CCHP`, `trgb_jwst&N4258&SH0ES`.

A razão da partição é impedir que melhora da referência da escada seja confundida com reduzir erros individuais de hospedeiros. Ela é **[DECLARADO]**, fixada antes de qualquer resultado e não poderá ser trocada depois de ver \(f_q\); a gerência precisa ratificá-la antes de rodar.

Com \(F_{\rm cal}=(F_{\rm anchor}\;F_{\rm MAS})\):

\[
C_{\rm cal}=F_{\rm cal}F_{\rm cal}^T,\quad
V_{\rm cal,0}=w^TC_{\rm cal}w,\quad
V_{\rm other}=V_{\rm tot,0}-V_{\rm cal,0}.
\]

As 92 HMS e os demais termos estatísticos/covariância/sistemática/modelo permanecem em \(V_{\rm other}\). Não se remove a diagonal HMS duas vezes: sua contribuição upstream é somente fora da diagonal.

### 3.2 Duas bases, sem misturar Z e D

A expressão comum, não avaliada, é

\[
f(q;A)=\frac{A^2/q^2-V_{\rm other}}{V_{\rm cal,0}}.
\]

- **Alvo 5, base Z:** \(A_Z/\sqrt{V_{\rm tot,0}}=Z_{\rm nulo,exp}=4,514141429613277\), campo `values.esperado_pelos_agregados[1].z_nulo_esperado`. A expressão é \(f(5;A_Z)\). Os 23 % já existentes são só o contexto da chance de passar de 5.
- **Portão de 90 %, base D:** \(A_D/\sqrt{V_{\rm tot,0}}=D_0=5,19131201002441\), campo `values.cefeidas_livres.D`. A expressão é \(f(D_{90};A_D)\), \(D_{90}=6,281551565544601\).

**Não se usa Z=4,514 como D=5,192.** O `z_K_esperado=-0,6777408098403498` permanece separado; acordo com K não é a base do alvo contra o nulo.

Os estresses pré-registrados §7 acompanham obrigatoriamente qualquer desenho: S1 = **5,489825 / 4,743268**, S2 = **5,527887 / 4,773510**, S4 = **4,378058 / 3,871970**, respectivamente publicado/Cefeidas livres `[DECLARADO pelo Kimi]`. S4 já está abaixo de 5. Também ficam o viés comum de 0,0156 mag que tira o primário do portão e o de 0,1816 mag que fabricaria 5σ.

## 4. R7 — p contra o nulo e censo com manifesto

### 4.1 Escolha de p, sem calcular

Entra `values.primario.p_unilateral` = **5,115711574207153×10⁻¹⁰**, associado a `z_null` = **6,1057575347088955**. Esses são os nomes reais dos campos. R7 pergunta pela diluição da tensão de Hubble contra o nulo diante de tentativas anteriores; o \(p\) de acordo com K mede outra pergunta e não entra.

Não se avaliou a fórmula de Šidák. Os valores 16/123 abaixo não são \(N\) independente nem autorizam \(N_\star\), \(p_{\rm global}\) ou \(Z_{\rm global}\).

### 4.2 Exportação e manifesto

Arquivos nesta pasta:

- `CENSO_R7_MAPA_K09.json`, sha256 `08ad355c3b647a2db07128d826281c724f61206c329e284635cf9f63cfc125ea`;
- `MANIFESTO_CENSO_R7_MAPA_K09.json`, com consulta, data `2026-11-15T05:28:42-03:00`, fonte e hashes;
- `mapear_metadados_k09.py`, reprodução da extração de metadados, sem NPZ e sem conta estatística.

Consulta: `C:\IALD\MAPA_DE_ROTAS\rotas.jsonl`, registros JSONL válidos com `seq ≤ 2062`, preservando o universo de 14/11 examinado pelo revisor; `olhou_dados is true` e `rota_id` presente; Hubble = prefixo `d1.`/`hubble.` ou substring `h0dn`. SHA-256 do Mapa vivo lido: `558d49b9d9cd04a9b198152e8aac75201d309ac91a5b5586247d97e46044bc6c`.

Totais: 2.062 registros, 505 rotas, 285 registros que olharam dado, **123 rotas** no Mapa e **16 rotas Hubble**. A exportação contém somente `seq`, `rota_id`, data, tipo, domínio e marcações de consulta. **16 e 123 são tetos de contagem, não tentativas independentes.** \(N_{\rm indep}\) continua [OPEN]; dependências e duplicidades exigem o livro de famílias antes de qualquer correção global.

## 5. P7/K06 — desenho bloqueado

P7/K06 pergunta sobre convergência do leitor, não sobre natureza, e não resolve R1–R7. Hoje está **em desenho e BLOQUEADA_PARA_PRODUCAO**, não “executável hoje”: a separação resumo/convergência não fecha, o extrator está FAIL/bloqueado, modelos/tokenizers/janelas estão OPEN/bloqueados e os poderes ideais já relatados de 0,599/0,669 ficam abaixo de 0,90. Fonte: `DEGRAU_5_SIGMA_K06.md`, sha256 `a82819f4dc726a6e8de9d99cfc8e7d433d75b27faa4cb88ad97613139019cb66`. Nenhum modelo foi executado nesta K09.

## 6. Bloqueios finais

1. R5: nunca rodar a fração com denominador \(g^TP_{72}g\); usar somente a fórmula por linha, após autorização.
2. R3/R4: ratificar a partição 3+9/92 e as bases separadas antes de qualquer \(f_q\).
3. R7: 16/123 são tetos; sem independência demonstrada, não há Šidák.
4. P7: não apresentar como executável enquanto bloqueada.
5. Não ler vetor, não reestimar, não chamar `executar_abertura_v411.py`, não reabrir H0DN e não executar nenhuma das três contas nesta etapa.
6. Número ruim futuro mede fragilidade de desenho/erro/covariância, não falsificação automática da lei; `NOT_FALSIFIED` não é `CONFIRMED`, e o gate não se move.
