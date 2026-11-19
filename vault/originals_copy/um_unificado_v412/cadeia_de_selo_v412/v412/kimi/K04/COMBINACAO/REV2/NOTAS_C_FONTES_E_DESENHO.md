# NOTAS C K09 — fontes, valores corrigidos e bloqueios

15/11/2026. Estas notas acompanham as correções AO LADO de `COMBINACAO_K04.md`. São documentação de desenho, não autorização de execução nem novo resultado. Nenhuma conta foi refeita; os valores corrigidos vêm da revisão distinta já concluída.

## 1. Fontes de trabalho e pinos

- `ORDEM_K09_teste_as_cegas_rodada_3.md`, especialmente D, sha256 `f5a9985bb6773aa73539e3ee1848daf34b2adc5b412fc297812c9281308d28b4`.
- `REVISAO_K04_COMBINACAO_RESSALVAS.md`, lida integralmente, sha256 `c49a911a263fe6bcfc07ca9807a673dc827903a62063696055fb4901061472b4`.
- `COMBINACAO_K04.md` antes da K09, sha256 `b166e0afeccd2a6fe57fa3a017d5c470e7e585b00ed7d52c66426618c7e90a2c`; o estrato REV0 permanece em `K04\COMBINACAO\REV0\`.
- `PODER_RAMO_B_ANTES_DE_ABRIR.json`, sha256 `05bc5a1f2592b776accbcc9ae2a247623a929ddac0136cf90aaa9490840a4935`.
- Core `f2b_errata_v404` e Mapa `ringdown.ramo_b_preregistro_v386`, seq 1545, 1744 e 1775.

## 2. Stouffer: qual regra dá qual número

Insumos já reproduzidos: \(D_{90}=6,281551565544601\), \(D_N=2,654801672305172\), separação JUNO de planejamento 0,1503905333 e \(\sigma_J\) na convenção \(\Delta m^2_{21}\), em unidades de \(10^{-5}\,\mathrm{eV}^2\). A forma geral é

\[
\lambda_S=\frac{w_JD_J+w_ND_N}{\sqrt{w_J^2+w_N^2}}.
\]

| Regra | Álgebra | Fronteira | Dias vivos | \(\sigma_J=0,024\) |
|---|---|---|---:|---|
| **Pesos iguais, \(w_J=w_N\)** | \(\lambda_{=}= (D_J+D_N)/\sqrt2\); \(D_{J,\rm req}=\sqrt2D_{90}-D_N\simeq6,22865\) | **\(\sigma_J\leq0,024145\)** | **2.162** | \(\lambda\simeq6,3082\); **90,5 %** |
| **Pesos proporcionais a \(D\)** | \(\lambda_{\propto D}=\sqrt{D_J^2+D_N^2}\); \(D_{J,\rm req}=\sqrt{D_{90}^2-D_N^2}\simeq5,69297\) | **\(\sigma_J\leq0,0264169\)** | **1.806** | \(\lambda\simeq6,8054\); **96,4 %** |

A raiz da soma dos quadrados **não** é Stouffer de pesos iguais. Ela resulta de \(w_i\propto D_i\), a regra ótima da **razão de verossimilhança ponto contra ponto** sob a alternativa gaussiana fiducial. Os pesos dependem da alternativa e precisam ser fixados antes do resultado. O cenário numérico não elimina os bloqueios da candidata geral de verossimilhança: nulos, nuisances, covariância, métrica e função de veredito continuam por fechar.

Para \(\sigma_J=0,024\), a extrapolação de 2.189 dias vivos é a mesma nas duas linhas porque depende apenas de \(\sigma_J\); o que muda é a não-centralidade e o poder. Nenhuma dessas contas é uma nova estatística observada nem aplica silenciosamente a regra congelada em \(m_2\).

## 3. O significado exato de 2034

**2034 é o fim do levantamento do SO; a combinação não antecipa o JUNO sozinho, que chega antes ao portão no cenário ideal.** O ano não é data prometida de produto, publicação ou abertura. A combinação acrescenta redundância e uma segunda pergunta, não um atalho temporal.

Permanecem bloqueados: produto SO datado; incremento JUNO realmente novo; covariância condicional; métrica congelada; ramo S/L e \(Y_p\); covariância SO+Planck e grupo CMB; sistemáticas; regra omnibus, sinais e pesos anteriores ao resultado; vereditos individuais e multiplicidade.

## 4. Ringdown: piso, viés e taxa somente O4b

### 4.1 O piso não vale com viés

- D10 sem hold: 25,4874 eventos equivalentes; D14: 25,6868. Arredondados, **25,5/25,7**.
- Esses valores pressupõem informação média constante \(\propto N\), sem viés/sistemática e sem perda de convergência da PE.
- Com \(\sigma_{\rm viés}=0,06864722987593155\) (≈0,0686, C2 ampla), a revisão obtém saturação do poder de D10 em aproximadamente **5,8**, abaixo de \(D_{90}=6,28155\). **D90 não é alcançável por simples aumento de contagem.** O5 não é uma janela suficiente sem informação extra e sistemática resolvida.

### 4.2 A taxa de referência deixa de misturar O4a

O censo V1 contém 14 elegíveis, 10 sem hold, 8 pendentes e 22 reprovados entre 44 candidatas. GW230919_215712 é o único elegível de O4a; os outros 13 são de O4b. Entre os 10 sem hold, 9 são de O4b.

| Base corrigida, 293 dias de O4b | Taxa retrospectiva | Tempo adicional já reproduzido |
|---|---:|---:|
| D14: 13 elegíveis O4b | **16,2/ano** | **8,7 meses** |
| D10: 9 sem hold O4b | **11,2/ano** | **16,6 meses** |

A antiga faixa **17–27 meses para D10** permanece somente como contexto conservador da taxa mista O4a+O4b. A taxa mista não é base única. Nenhuma dessas taxas é previsão oficial; IR1 continua insuficiente e, com o viés medido, contagem não resolve \(D_{90}\).

A cifra cumulativa de candidatas usada na antiga C.5.2 não tem lastro no resumo citado e foi retirada AO LADO. Ela não entra em nenhuma conta destas notas.

## 5. Atribuição F2b e estado de D

- **A retirada do canal F2b é conclusão da gerência**, conforme `f2b_errata_v404`; não é decisão a atribuir ao operador. O verbatim de 28/10 ratifica «calibrar Não significa validar», não nomeia retirada; sha256 `56703faadf2b3cc25fae3d3bd1efaa538233e5eafca0f4e8b872c12c3e17d3ef`.
- **D foi AUTORIZADO pelo operador em 29/10.** Verbatim: «autorizo a realização do teste do conjunto D». Arquivo `work\cunhagens_13out\OPERADOR_29out_autoriza_conjunto_D_verbatim.txt`, sha256 `9e54b47780dab1010785726f2fb55d0675b6c59d5d7118ad0f77be8c650bdbc9`; Mapa seq 1545.
- **A opção (c) foi escolhida em 03/11.** Verbatim: «concordo com c, porque se o teste não tiver poder não vou inseri-lo no um.py». Arquivo `work\cunhagens_13out\OPERADOR_03nov_decisoes_psion_graviton_estado_ligado_projetor_4x4_nomes_ratificados_teste_d_opcao_c_motor_banho_holografico_verbatim.txt`, sha256 `73466598d3419fb0603c4fcb74d455770cbf1ecf4ad058d240728cd9b1b18289`; seq 1744.
- **Nada foi aberto** (seq 1775). D não entra no `um.py` sem poder.
- **D só decide o par** \(k=2\pi/\hat\kappa(\chi_f)\), \(M_X=M_f\) e a identificação/envoltória. **D não decide a retirada**, não testa β isoladamente, não decide a lei geral de defasamento/GKSL ou R2 e não move o gate.

## 6. Bloqueios vigentes

1. Não apresentar 0,0264169/1.806 como resposta de pesos iguais; esses números pertencem a \(w_i\propto D_i\).
2. Não apresentar 2034 como antecipação nem como data de abertura.
3. Não apresentar 25,5/25,7 como limiar com viés; D10 satura em aproximadamente 5,8 com 0,0686.
4. Não usar taxa mista O4a como base única; a referência corrigida é O4b.
5. Não atribuir a retirada F2b ao operador e não confundir autorização de D com abertura.
6. Nenhuma abertura, PE, solver, posterior, strain ou teste foi executado nesta correção.
