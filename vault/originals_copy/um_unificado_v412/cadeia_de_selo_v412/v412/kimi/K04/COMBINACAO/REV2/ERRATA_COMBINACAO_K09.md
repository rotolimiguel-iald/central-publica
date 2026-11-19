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

**2034 é o fim do levantamento do SO; a combinação não antecipa o JUNO sozinho, que chega antes ao portão no cenário ideal.** Não é data prometida de abertura.

## 3. Ringdown e F2b

- **25,5/25,7 eventos equivalentes é piso sem viés.** Com viés 0,0686, o poder de D10 satura em aproximadamente **5,8**, não em D90; contagem sozinha não alcança D90.
- A taxa de referência usa **somente O4b**: **D14 em 8,7 meses** e **D10 em 16,6 meses**. A antiga faixa 17–27 para D10 fica apenas como contexto da taxa mista O4a+O4b, não base única.
- A cifra cumulativa sem lastro no resumo citado foi retirada AO LADO e não entra em contas.
- **A retirada do canal F2b é conclusão da gerência, não do operador.** D foi **AUTORIZADO pelo operador em 29/10** e a **opção (c) foi escolhida em 03/11**; **nada foi aberto**. D só decide o par \(k=2\pi/\hat\kappa\), \(M_X=M_f\), identificação/envoltória; **não decide retirada alguma**.

## 4. R5 — substituição da conta

A conta do piso somente nas 72 direções tem denominador zero por construção e fica retirada como desenho executável. A partitura corrigida usa **ruído independente e homoscedástico por linha nas 111 linhas brutas**, pesos congelados e

\[
D_m(\tau)=\frac{A_m}{\sqrt{\sigma_{0,m}^2+\tau^2S_m}},\qquad
\tau_{m,q}^2=\frac{A_m^2/q^2-\sigma_{0,m}^2}{S_m},
\]

sem avaliação. Insumos/pinos: `estimator_frozen.npz` sha256 `059ef7b6f2c671406058fdb6e647c011851e5761da91784b4ce213e9abbe07b8`, `estimador_s0_v411.npz` sha256 `6cc9a23c4aa7b9ffe4d925273d044ac007d3646506bc5d3d80160e1ee839a617`, e `values.decomposicao_conferencias.soma_w2/sum_w2_touched` no core sha256 `36c69fc767f8d47f318f134ecdfb6bd2d39ad25f17f9b9310b196afb0a19064e`.

Os valores **6,66 com 0,035 mag**, **6,31 com 0,10 mag** e **0,104 mag no portão D90** são pré-registrados; **6,69 com τ≈0,0222** é selo pós-observação, não cego. Só se desenham os pontos de 5σ do primário e das Cefeidas livres; nenhum foi calculado.

## 5. R3/R4 — partição e bases

Fica fixada antes, para deliberação da gerência, a partição dos 104 fatores de `network\factors.json`, sha256 `2de3cbfe475441765c1c9eb34d57a1eb56b95faab58b6cb203e0545c2ed02212`:

- **calibração:** 3 âncoras geométricas (LMC, MW, N4258) + 9 MAS (method–anchor–source);
- **fora da calibração:** 92 HMS (host–method–source), termos de medidas de hospedeiros, em \(V_{\rm other}\).

A razão documental e os nomes das 9 MAS estão nas notas. O alvo 5 usa **Z esperado contra o nulo** (4,514141429613277); D90 usa **D** (5,19131201002441). **Não se mistura Z=4,514 com D=5,192.** Permanecem ao lado S1 5,489825/4,743268, S2 5,527887/4,773510 e S4 4,378058/3,871970, publicado/Cefeidas livres. Nenhum \(f_q\) foi avaliado.

## 6. R7 — p e censo

Entra `values.primario.p_unilateral` = 5,115711574207153×10⁻¹⁰, contra o nulo, pois R7 trata da diluição da tensão de Hubble; acordo com K é outra pergunta. Não se calculou \(N_\star\), \(p_{\rm global}\) ou \(Z_{\rm global}\).

Foram criados `CENSO_R7_MAPA_K09.json` e `MANIFESTO_CENSO_R7_MAPA_K09.json`, somente com metadados, consulta `seq ≤ 2062`, data e hashes. O censo reproduz 2.062 registros/505 rotas, 285 registros que olharam dado, **123 rotas no Mapa** e **16 rotas Hubble**. **São tetos, não N independente nem denominador de Šidák.**

## 7. P7 e bloqueios finais

**P7 está em desenho e BLOQUEADA_PARA_PRODUCAO**, não “executável hoje”. Pergunta sobre o leitor, não sobre a natureza, e não resolve R1–R7.

Antes de qualquer execução futura: ratificar a partição R3/R4 e as duas bases; usar somente a R5 por linha; manter 16/123 como tetos até fechar dependências; não chamar abertura, vetor, estimador ou `executar_abertura_v411.py`; não apresentar P7 como pronta. Número ruim futuro mede fragilidade do desenho/erro, não falsificação automática da lei. `NOT_FALSIFIED` não é `CONFIRMED`; o gate não se move.
