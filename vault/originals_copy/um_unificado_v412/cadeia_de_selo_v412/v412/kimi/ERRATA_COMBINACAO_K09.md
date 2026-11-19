# ERRATA AO LADO K09 — COMBINAÇÃO, RINGDOWN, RESSALVAS D/E E ATRIBUIÇÕES

15/11/2026. [DECLARADO — correção documental após revisão distinta; aguarda conferência da gerência.] Esta errata não apaga a K04. As correções foram inseridas **AO LADO** nos dois documentos principais; REV0 permanece intacto e REV2 conserva a versão corrigida. **Nenhuma das três contas da seção D foi executada, nenhum ponto novo de 5σ foi calculado e nenhum vetor/dado de teste foi aberto.**

## 1. Documentos corrigidos e preservação

- `COMBINACAO_K04.md`: hash imediatamente anterior à K09 `b166e0afeccd2a6fe57fa3a017d5c470e7e585b00ed7d52c66426618c7e90a2c`.
- `RESSALVAS_UMA_A_UMA_K04.md`: hash imediatamente anterior `7119440be0353010f59b527c001d3ca13e8fe9fb0e27bb838258a7bf9e0c2eee`.
- Estratos originais: `K04\COMBINACAO\REV0\`.
- Notas e censo: `K04\COMBINACAO\K09\`.
- Cópia corrigida e hashes finais: `K04\COMBINACAO\REV2\`.

## 2. Stouffer e calendário

A antiga identidade \(\sqrt{D_J^2+D_N^2}\), rotulada “pesos iguais”, estava errada. A leitura vigente é:

- **pesos iguais:** \((D_J+D_N)/\sqrt2\); fronteira **σJ = 0,024145×10⁻⁵ eV²**, **2.162 dias vivos**, e **90,5 %** de poder para σJ = 0,024;
- **pesos proporcionais a D:** \(\sqrt{D_J^2+D_N^2}\); fronteira **0,0264169×10⁻⁵ eV²**, **1.806 dias vivos**, e 96,4 % para σJ = 0,024. Esta é a regra da **razão de verossimilhança ponto contra ponto**, não Stouffer de pesos iguais.

**Piso do m₂ na combinação (K10).** A combinação carrega o mesmo piso do m₂, na mesma frase: **sem piso: 2.162 d (pesos iguais) / 1.806 d (pesos prop. a D), poder 90,5 % / 96,4 %; com o piso s0 do m₂ (ajuste de dois pontos, sem graus de liberdade) λ ≤ 3,90 nas duas regras, D90 inalcançável.** Os dias vivos sem piso ficam rotulados **BRINQUEDO**.

**2034 é o fim do levantamento do SO; a combinação poupa dias vivos do ramo JUNO, mas a data é travada pelo SO e o JUNO sozinho chega antes no cenário ideal.** Não é data prometida de abertura.

## 3. Ringdown e F2b

- **25,5/25,7 eventos equivalentes é piso sem viés.** Com viés 0,0686, o poder de D10 satura em **5,805** (≈5,8) — valor **para C2 ampla (50 PE)** —: fica **abaixo de D90** (contagem sozinha não alcança D90) mas **acima do portão 5,0**; para o portão 5 são **~63 eventos (~4,7 anos à taxa O4b de 11,2/ano)** e, **sem viés**, 1,61× a informação (**6,1 eventos, ~6,6 meses**). Na combinação com o portão 5: **σJ ≤ 0,0341 (1.087 d, pesos iguais) ou ≤ 0,0355 (1.001 d, pesos prop.)**, contra 0,0301 (1.393 d) do JUNO sozinho. **Os dois portões (5,0 e D90 = 6,28) ficam lado a lado, e a escolha entre eles é do operador.** Fonte: `C:\IALD\Central de Patentes\work\conjunto_D_20261029\parametrizacao_03nov\PODER_RAMO_B_ANTES_DE_ABRIR.json` (regra da casa `poder_min = 5,0`; sha256 `05bc5a1f2592b776…a4935`); valores reproduzidos da revisão, não recalculados.
- A taxa de referência usa **somente O4b**: **D14 em 8,7 meses** e **D10 em 16,6 meses**, **ambos sem viés**. A antiga faixa 17–27 para D10 fica apenas como contexto da taxa mista O4a+O4b, não base única.
- A cifra cumulativa sem lastro no resumo citado foi retirada AO LADO e não entra em contas.
- **A retirada do canal F2b é conclusão da gerência, não do operador.** D foi **AUTORIZADO pelo operador em 29/10** e a **opção (c) foi escolhida em 03/11**; **nada foi aberto**. D só decide o par \(k=2\pi/\hat\kappa\), \(M_X=M_f\), identificação/envoltória; **não decide retirada alguma**. A **opção (c)** é: **rodar até o estágio cego; a abertura não está na fila; só roda com a palavra do operador (Mapa seq 1775); só entra no `um.py` se tiver poder**. Cronologia registrada: a autorização de 29/10 foi dada sobre a premissa de então (z_excl ~ 7 → FALSIFIED), que a gerência corrigiu no mesmo dia (poder 3,7–3,9 < 5, `NOT_FALSIFIED_UNDERPOWERED`); o operador decidiu de novo em 03/11 (bytes citados na revisão; não reabertos).

## 4. R5 — substituição da conta

A conta do piso somente nas 72 direções tem denominador zero por construção e fica retirada como desenho executável. A partitura corrigida usa **ruído independente e homoscedástico por linha nas 111 linhas brutas**, pesos congelados e

\[
D_m(\tau)=\frac{A_m}{\sqrt{\sigma_{0,m}^2+\tau^2S_m}},\qquad
\tau_{m,q}^2=\frac{A_m^2/q^2-\sigma_{0,m}^2}{S_m},
\]

sem avaliação. Insumos/pinos: `estimator_frozen.npz` sha256 `059ef7b6f2c671406058fdb6e647c011851e5761da91784b4ce213e9abbe07b8`, `estimador_s0_v411.npz` sha256 `6cc9a23c4aa7b9ffe4d925273d044ac007d3646506bc5d3d80160e1ee839a617`, e `values.decomposicao_conferencias.soma_w2/sum_w2_touched` no core sha256 `36c69fc767f8d47f318f134ecdfb6bd2d39ad25f17f9b9310b196afb0a19064e`.

Os valores **6,66 com 0,035 mag**, **6,31 com 0,10 mag** e **0,104 mag no portão D90** são pré-registrados; **6,69 com τ≈0,0222** é selo pós-observação, não cego. Só se desenham os pontos de 5σ do primário e das Cefeidas livres; nenhum foi calculado.

## 5. R3/R4 — partição e bases: alternativas ao operador

Fica **apresentada ao operador como alternativa, a ratificar por ele depois da leitura — não fixada pela gerência** — a partição dos 104 fatores de `network\factors.json`, sha256 `2de3cbfe475441765c1c9eb34d57a1eb56b95faab58b6cb203e0545c2ed02212`:

- **calibração:** 3 âncoras geométricas (LMC, MW, N4258) + 9 MAS (method–anchor–source);
- **fora da calibração:** 92 HMS (host–method–source), termos de medidas de hospedeiros, em \(V_{\rm other}\).

A razão documental e os nomes das 9 MAS estão nas notas. O alvo 5 usa **Z esperado contra o nulo** (4,514141429613277); D90 usa **D** (5,19131201002441). **Não se mistura Z=4,514 com D=5,192.** Permanecem ao lado S1 5,489825/4,743268, S2 5,527887/4,773510 e S4 4,378058/3,871970, publicado/Cefeidas livres. Nenhum \(f_q\) foi avaliado.

**O que a partição decide, o que não decide e o que o negativo significaria (K10).** A partição decide a **viabilidade do alvo já no desenho**: com calibração perfeita, o alvo 5 (base **Z = 4,514**) só é viável se as 3 âncoras + 9 MAS carregarem **≥ 18,5 %** da variância total, e o alvo D90 (base **D = 5,191**) só se carregarem **≥ 31,7 %**; do contrário \(f_q<0\) **por construção da partição**, não por causa do erro publicado nem do dado. A partição **não decide** a lei nem o dado. Um negativo significaria **fragilidade da partição e do erro publicado, não falsificação**. **Itens a ratificar PELO OPERADOR depois da leitura, como alternativas:** a partição (3 âncoras + 9 MAS / 92 HMS fora), as duas bases (Z contra o nulo; D) e o \(p\) da R7.

## 6. R7 — p e censo

Entra `values.primario.p_unilateral` = 5,115711574207153×10⁻¹⁰, contra o nulo, pois R7 trata da diluição da tensão de Hubble; acordo com K é outra pergunta. Não se calculou \(N_\star\), \(p_{\rm global}\) ou \(Z_{\rm global}\).

Foram criados `CENSO_R7_MAPA_K09.json` e `MANIFESTO_CENSO_R7_MAPA_K09.json`, somente com metadados, consulta `seq ≤ 2062`, data e hashes. O censo reproduz 2.062 registros/505 rotas, 285 registros que olharam dado, **123 rotas no Mapa** e **16 rotas Hubble**. **Correção K10: 16 = contagem pelo prefixo `d1.`/`hubble.`/`h0dn`; há rotas de Hubble fora do prefixo; o único teto é 123. Não é N independente nem denominador de Šidák.** O \(p\) escolhido para a R7 (contra o nulo; `z_null` = 6,106, o mais favorável à diluição) está dito com a razão e entra, **junto com a partição e as duas bases, como item a ratificar PELO OPERADOR depois da leitura**.

## 7. P7 e bloqueios finais

**P7 está em desenho e BLOQUEADA_PARA_PRODUCAO**, não “executável hoje”. Pergunta sobre o leitor, não sobre a natureza, e não resolve R1–R7.

Antes de qualquer execução futura: **o operador** ratifica — como alternativas lidas a ele, não como decisão da gerência — a partição R3/R4, as duas bases e o \(p\) da R7; usar somente a R5 por linha; 16/123: **16 é contagem por prefixo e não limita nada — o único teto é 123** — e nenhum dos dois é N independente até fechar dependências; não chamar abertura, vetor, estimador ou `executar_abertura_v411.py`; não apresentar P7 como pronta. Número ruim futuro mede fragilidade do desenho/erro, não falsificação automática da lei. `NOT_FALSIFIED` não é `CONFIRMED`; o gate não se move.

## 8. Consertos K10: C3 aplicado, quadro das ressalvas, pinos e manifesto

**8.1 (C3 da K04, aplicado).** Linha ao operador: **se o mundo ficar como hoje, este teste tem ~90 % de chance de devolver 5σ contra o pacote; os dois centros de planejamento foram escolhidos assim (JUNO persiste, N_eff migra ao padrão); o core tem a outra convenção (4,30σ persistindo; 2,65 migrando); é escolha.** Citadas as três rotas do Mapa — `estatistica.coincidencia_conjunta`, `neff.frozen_v1_08ago`, `cmb.fisher_gates_e_prereg_so_s4_14ago` — com a nota **não refazer**. Nas superfícies desta frente não há “revisores distintos/conferências distintas” sobre revisão interna do construtor; onde houvesse, leria-se **revisão interna**.

**8.2 (Quadro das ressalvas).** Aplicado em `RESSALVAS_UMA_A_UMA_K04.md`: R7 = «só se declara: história + livro; réplica disjunta cria evidência nova mas não apaga»; R4 = «covariância e sistemáticas independentes»; R5 = «orçamento independente; a conta que existe é o ruído por linha (τ)», com a nota: **um τ5 pequeno mede fragilidade da tabela de erros, não falsificação**. **Anotado para a ENTREGA_K10 (a gerência a escreve):** a frase-resumo do DESENHO — «um teste cego novo resolve 1, 2, 6 e, com calibração e covariância independentes, 3 a 5; a 7 só se declara» — deve ir ao topo da ENTREGA_K10.

**8.3 (Pino da ORDEM_K09 corrigido).** `NOTAS_C_FONTES_E_DESENHO.md` §1 pinava `f5a9985b…`, que é o `.bak_20261115_080717` anterior ao AO LADO de 15/11. Conferido por sha256sum nesta rodada: a ORDEM_K09 vigente é sha256 **`4607f0f0829a58c2ba92c0626a4dc461cd1445c8cd26634d43034a13eaa3247f`**; o `.bak` é `f5a9985bb6773aa73539e3ee1848daf34b2adc5b412fc297812c9281308d28b4`. Corrigido nas NOTAS_C.

**8.4 (Manifesto do censo).** Gravado em `MANIFESTO_CENSO_R7_MAPA_K09.json`: o hash do Mapa (`558d49b9…`) reproduz como prefixo das primeiras **2066 linhas** do `rotas.jsonl`. O CENSO ganhou a nota «16 = contagem pelo prefixo; há rotas de Hubble fora do prefixo; o único teto é 123» **sem refazer o censo**; o hash e os bytes do artefato foram atualizados no manifesto (o conteúdo mudou só pela nota).
