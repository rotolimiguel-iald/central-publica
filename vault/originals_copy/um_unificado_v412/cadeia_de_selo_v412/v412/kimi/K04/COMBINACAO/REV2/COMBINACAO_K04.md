# K04 — Seção C: combinação prospectiva de canais e ringdown

**Estatuto.** [DECLARADO] desenho candidato, ainda não congelado; [DERIVED–DESENHO] aritmética de planejamento sobre números já públicos ou já selados, nunca uma nova estatística observada. Nenhum vetor observado foi lido, nenhum solver, estimador, `evaluate` ou programa de abertura foi executado, e nenhum teste foi realizado. K01 e a revisão distinta são reutilizadas, não refeitas.

---

## CORREÇÃO AO LADO K09 — leitura vigente (15/11/2026)

[DECLARADO — correção documental da K04 após a revisão distinta; aguarda a conferência da gerência.] O texto da K04 permanece abaixo como estrato histórico. **Onde houver divergência, valem as correções K09 inseridas ao lado, não a frase anterior.** Nenhuma conta nova foi executada nesta correção; os números corrigidos são os já reproduzidos pela revisão distinta.

1. **Stouffer tem duas regras distintas.** Pesos iguais dão \(\lambda_{=}= (D_J+D_N)/\sqrt2\), fronteira \(\sigma_J\leq0,024145\times10^{-5}\,\mathrm{eV}^2\), **2.162 dias vivos** e, para \(\sigma_J=0,024\), **poder de 90,5 %**. Pesos proporcionais a \(D\) dão \(\lambda_{\propto D}=\sqrt{D_J^2+D_N^2}\), fronteira \(\sigma_J\leq0,0264169\times10^{-5}\,\mathrm{eV}^2\) e **1.806 dias vivos**; esta segunda regra é a da **razão de verossimilhança ponto contra ponto**, não Stouffer de pesos iguais.
2. **2034 é o fim do levantamento do SO; a combinação não antecipa o JUNO sozinho, que chega antes ao portão no cenário ideal.** O ano não é uma promessa de publicação nem de abertura.
3. **Ringdown:** 25,5/25,7 eventos equivalentes é somente o piso sem viés. Com \(\sigma_{\rm viés}=0,0686\), o poder de D10 satura em aproximadamente **5,8**, não em \(D_{90}\). A base de taxa corrigida é **somente O4b**: D14 em **8,7 meses** e D10 em **16,6 meses**. A antiga faixa de 17–27 meses para D10 fica apenas como contexto da taxa mista O4a+O4b, nunca como base única.
4. **Atribuição F2b:** a retirada do canal é conclusão da **gerência**, não do operador. D foi **AUTORIZADO pelo operador em 29/10**, e a **opção (c) foi escolhida em 03/11**; **nada foi aberto**. D só decide o par \(k=2\pi/\hat\kappa\), \(M_X=M_f\) e a identificação/envoltória; **não decide retirada alguma**.
5. A contagem cumulativa de candidatas em C.5.2, sem lastro no resumo citado, **fica retirada e não entra em nenhuma conta**.

As fórmulas e os pinos estão em `K04\COMBINACAO\K09\NOTAS_C_FONTES_E_DESENHO.md`; a errata-mãe é `ERRATA_COMBINACAO_K09.md`.

---

## Resposta curta

1. **Hoje não existe teste cego conjunto executável com \(D\geq6,28\).** Os únicos dois canais que hoje permitem uma conta conjunta datada por forecasts são o **incremento futuro do JUNO** e **\(N_\mathrm{eff}\) do Simons Observatory (SO)**. Os demais canais independentes não têm, ao mesmo tempo, previsão fechada, poder validado e calendário.
2. **Regra que permite uma primeira estimativa:** soma de \(z\) de Stouffer com pesos e sinais pré-fixados. Sob independência, ausência de piso sistemático, centro de planejamento JUNO \(7,388\) e \(\sigma(N_\mathrm{eff})=0,045\), o cruzamento conjunto exige \(\sigma_J\lesssim0,02642\times10^{-5}\,\mathrm{eV}^2\) no incremento; se \(\sigma_J=0,024\), \(\lambda\simeq6,805>6,28155\). Estes números usam a forma \(\Delta m^2_{21}\) da revisão, **não** uma emenda silenciosa à regra congelada em \(m_2\).
3. **Primeiro horizonte plausível, não data garantida:** **2034**, quando o forecast completo do SO 2025–2034 e um incremento JUNO suficientemente preciso podem coexistir. A primeira data de abertura continua **[OPEN]**: dias vivos do JUNO não são dias corridos, a cadência das liberações não está publicada e o SO não oferece aqui uma data única de produto cego. Antes de 2034, só se antecipa com um produto SO datado e um incremento JUNO cuja covariância e precisão estejam demonstradas; isso não existe no material consultado.
4. **Ringdown:** o revisor converteu o requisito em **25,49 eventos equivalentes a partir de D10** e **25,69 a partir de D14**, sob informação \(\propto N\) e sem sistemática. O censo congelado contém **14 elegíveis, 10 sem hold**, além de 8 pendentes de metadados que não podem ser contados. Na taxa retrospectiva bruta do mesmo censo, IR1 sozinho não basta; **O5 (2029–2031) é a primeira janela plausível, sem dia ou mês defensável**.
5. **D não entra “pela teoria”.** O canal F2b foi retirado antes do dado. Um eventual D só decide o par do ramo B retirado ao lado; não testa β isoladamente, a lei geral de defasamento ou R2.

---

## C.1 — Quais canais podem entrar, e por quê

A régua de admissão é: conteúdo ainda não lido pela casa; independência de dados e de análise; previsão física fechada; erro de desenho publicado ou derivável sem vetor observado; função de veredito candidata anterior à abertura. “Independente de H0DN” não basta: também é preciso independência entre os canais combinados e contabilização das liberações cumulativas.

| Canal | Conteúdo novo e independência | Previsão e poder reutilizados | Decisão para a combinação |
|---|---|---|---|
| **Incremento JUNO posterior aos 207,2 dias** | Pode ser cego somente no incremento. A liberação acumulada contém os dados já conhecidos; é indispensável a covariância condicional ou uma partição realmente nova. É independente do SO e de H0DN. | \(\Delta m^2_{21,\mathrm{pred}}=7,2376094667\times10^{-5}\,\mathrm{eV}^2\); centro de planejamento \(7,388\); separação \(0,1503905333\). A revisão dá \(D=6,2663\) para \(\sigma=0,024\) na forma \(\Delta m^2\). | **Entra como cenário condicional.** A métrica congelada é em \(m_2\); o número em \(\Delta m^2\) é cenário de comparação, não emenda nem veredito. |
| **\(N_\mathrm{eff}\), SO** | Novo composto SO pode ser cego depois de congelar S/L, \(Y_p\), covariância e grupo de dependência. É fisicamente independente do incremento JUNO. O forecast inclui Planck, que precisa permanecer no grupo de dependência CMB, sem dupla contagem com BBN/CMB completo. | \(\Delta N_\mathrm{eff}=0,1194660753\); \(\sigma=0,045\Rightarrow D_N=2,6548016723\); \(D_{90}\) isolado pediria \(\sigma\leq0,0190186\). | **Entra como cenário condicional.** TGL-S × TGL-L e a sistemática continuam por fechar; o \(\sigma\) publicado é só estatístico. |
| **Euclid, piso dos vazios** | DR1 futuro e survey independente; possível cegueira prospectiva. | Não há forecast do estimador de matéria, nem alternativa bilateral: \(\Lambda\mathrm{CDM}\) raso também satisfaz o piso. | **Candidato qualitativo, fora da conta e da data.** DR1 em 16/06/2027 é calendário, não poder. |
| **NMC–Shapiro multimensageiro** | Eventos futuros seriam independentes e naturalmente cegos. | \(N=0\) para o corte específico; taxa e \(D\) completo validado são [OPEN]. | **Candidato qualitativo, fora da conta e da data.** |
| **Ringdown, conjunto D** | Independente de cosmologia e proceduralmente fechado/cego. | \(D_{10}=3,9346\), \(D_{14}=4,6374\) sem sistemática; taxa elegível não publicada. | **Não entra no pacote conjunto “pela teoria”.** Fica em seção própria abaixo, restrito ao par retirado. |
| **H0DN, DESI DR3, Planck/ACT/SPT, Coma** | Dados ou agregados já lidos e/ou forte sobreposição de calibradores e fundo. | Não há pacote futuro disjunto com forecast completo. | **Excluídos da combinação independente.** |
| **SO completo, \(\sum m_\nu\), BBN e decoerência JUNO** | Compartilham dados/instrumento ou informação com \(N_\mathrm{eff}\)/JUNO. | \(\sum m_\nu\) tem \(D\simeq0,0133\); BBN \(\sim1\); decoerência tem dezenas de ordens de déficit. | **Não são novas testemunhas independentes nem compram poder admissível.** |
| **Relógios, ecos, análogos** | Independentes em instrumento em alguns casos, mas dados já lidos ou ponte física aberta. | Relógios estão muitas ordens abaixo; ecos e análogos não têm observável zero-parâmetro fechado. | **Excluídos.** |

**Fontes:** K01 `CANAIS_K01.json`, itens `neutrino_m2_juno`, `neff_simons_observatory`, `vazios_euclid`, `nmc_shapiro_multimensageiro`, `ringdown_ramo_b_conjunto_D`; revisão K01 §§1, 3 e 5. Literatura: [KNOWN, a conferir] JUNO Collaboration, arXiv:2609.37895 e arXiv:2204.13249; Simons Observatory Collaboration, Abitbol et al., arXiv:2503.00636v3, Tabela 2 e §§2, 3.2 e 4.

## C.2 — Qual é a hipótese do PACOTE

O objeto do teste não é “β sozinho”. O pacote candidato é a conjunção

\[
H_P:\quad
\begin{cases}
\Delta m^2_{21}=(\beta\,\sin45^\circ\,E_0)^2,
\quad E_0=1\,\mathrm{eV},\; m_1\simeq0,
\quad\text{identificação e métrica congeladas};\\[2pt]
N_\mathrm{eff}=3,044+9,9296062166\,\beta,
\quad\text{fechamento }\rho+p
\quad\text{e ramo TGL-S/L pré-fixado}.
\end{cases}
\]

Assim, o pacote contém **a escala posta \(E_0\), a identificação da massa, a métrica da regra de oscilação, o fechamento radiativo e o ramo S/L**, além da forma de β. Rejeitar \(H_P\) mostraria que **alguma parte dessa conjunção ou do modelo de erros falhou**; não identificaria automaticamente qual parte, e jamais isolaria β.

Para o desenho, o nulo testado é \(H_P\). A alternativa de planejamento usa o centro JUNO já público e o valor padrão \(N_\mathrm{eff}=3,044\). Esse centro é apenas uma alternativa fiducial para calcular poder; não se transforma num “nulo JUNO” para a razão de verossimilhança sem declaração explícita.

**Guarda lógica obrigatória:** os vereditos individuais continuam visíveis. \(N_\mathrm{eff}\) não é uma segunda determinação de \(\Delta m^2_{21}\), e o JUNO não é uma segunda determinação de \(N_\mathrm{eff}\). A estatística omnibus não pode cancelar uma regra de morte individual, suprir a segunda testemunha exigida pelo canal de oscilação ou converter `NOT_FALSIFIED` em `CONFIRMED`.

## C.3 — Candidatas de combinação sob regras congeladas

### C.3.1 Soma de \(z\) (Stouffer), a única com cenário numérico imediato

Para \(i\in\{J,N\}\), defina antes da abertura:

- \(z_i=(y_i-\mu_{P,i})/\sigma_i\), assinado;
- \(s_i\in\{-1,+1\}\), o sinal esperado sob a alternativa de planejamento;
- \(w_i>0\), os pesos lógicos, não escolhidos pelo resultado;
- independência condicional demonstrada, ou covariância cruzada explicitamente modelada.

Sob \(H_P\), \(z_i\sim N(0,1)\); sob a alternativa fiducial, \(z_i\sim N(s_iD_i,1)\). Então

\[
Z_S=\frac{\sum_i s_iw_i z_i}{\sqrt{\sum_iw_i^2}},
\qquad
\lambda_S=\frac{\sum_iw_iD_i}{\sqrt{\sum_iw_i^2}}.
\]

Com pesos iguais e independência,

\[
\boxed{\lambda_S=\sqrt{D_J^2+D_N^2}}.
\]

O limiar de 90 % de poder para rejeitar \(H_P\) a 5σ unilateral é \(\lambda_S\geq D_{90}=6,2815515655\). Portanto, na fronteira,

\[
D_{J,\mathrm{req}}=\sqrt{D_{90}^2-D_N^2}\simeq5,69297,
\]

\[
\boxed{\sigma_{J,\mathrm{req}}=
\frac{0,1503905333}{D_{J,\mathrm{req}}}
\simeq0,0264169\times10^{-5}\,\mathrm{eV}^2}
\]

ou aproximadamente **0,3576 % do centro de planejamento**, na mesma convenção \(\Delta m^2\) usada pela revisão. Se o incremento atingir \(\sigma_J=0,024\),

\[
D_J\simeq6,2663,
\qquad
\boxed{\lambda_S\simeq\sqrt{6,2663^2+2,6548017^2}
\simeq6,8054>6,28155}.
\]

O poder ideal correspondente é aproximadamente \(96,4\%\), sob distribuição gaussiana, independência e os centros fiduciais fixos. **Não é probabilidade de o pacote ser verdadeiro nem de uma futura liberação alcançar o erro alvo.**

> **CORREÇÃO AO LADO K09 — C.3.1.** A fórmula anterior foi rotulada incorretamente como “pesos iguais”. Partindo de \(\lambda_S=\sum_iw_iD_i/\sqrt{\sum_iw_i^2}\), as duas regras são:
>
> | Regra, congelada antes do resultado | Não-centralidade | \(D_{J,\rm req}\) na fronteira \(D_{90}\) | \(\sigma_{J,\rm req}\) | Dias vivos | Para \(\sigma_J=0,024\) |
> |---|---|---:|---:|---:|---:|
> | **Stouffer, \(w_J=w_N\)** | \(\lambda_{=}= (D_J+D_N)/\sqrt2\) | \(\sqrt2D_{90}-D_N\simeq6,22865\) | **0,024145** | **2.162** | \(\lambda\simeq6,3082\); **poder 90,5 %** |
> | **Pesos \(w_i\propto D_i\)** | \(\lambda_{\propto D}=\sqrt{D_J^2+D_N^2}\) | \(\sqrt{D_{90}^2-D_N^2}\simeq5,69297\) | **0,0264169** | **1.806** | \(\lambda\simeq6,8054\); **poder 96,4 %** |
>
> Os \(\sigma_J\) acima estão em \(10^{-5}\,\mathrm{eV}^2\), na forma \(\Delta m^2_{21}\) de planejamento. **A primeira linha é a resposta para pesos iguais. A segunda é a regra ótima da razão de verossimilhança entre dois pontos gaussianos**, cujos pesos dependem da alternativa fiducial e precisam ser congelados antes; não se pode chamá-la de Stouffer com pesos iguais. Esse cenário numérico não fecha, por si só, os nulos, nuisances e a covariância exigidos pela candidata geral de C.3.3. Os números desta tabela são os reproduzidos pela revisão distinta; nada foi recalculado na K09.

Se a covariância cruzada não for nula, a fórmula deixa de valer: é necessário usar \(V=\operatorname{Cov}(z_J,z_N)\), com \(Z_S=(s^TWz)/\sqrt{s^TWVWs}\). Correlação positiva entre estimativas com o mesmo sinal reduz poder; simplesmente somar \(D^2\) inflaria o desenho.

### C.3.2 Fisher dos valores-\(p\), sem data defendida hoje

Uma segunda candidata é

\[
X_F^2=-2\sum_i\ln p_i,
\qquad p_i=1-\Phi(s_i z_i),
\]

com \(X_F^2\sim\chi^2_{2k}\) sob \(H_P\) e independência. O limiar usa o quantil de \(\chi^2_{2k}\) correspondente ao \(p\) unilateral de 5σ; o \(p\) global pode ser convertido em \(Z_g=\Phi^{-1}(1-p_g)\) apenas para comunicação.

Sob a alternativa, \(p_i\) não é uniforme e a potência precisa ser calculada pela distribuição induzida por \(z_i\sim N(s_iD_i,1)\):

\[
\Pi_F(D_J,D_N)=
\Pr\!\left[-2\sum_i\ln p_i>\chi^2_{2k,\,1-\alpha_{5\sigma}}
\,\middle|\,D_J,D_N\right].
\]

**Não se substitui essa integral por \(\sqrt{D_J^2+D_N^2}\).** Sem uma implementação de desenho congelada, semente, integração/quantil e convenção de caudas, Fisher não tem \(D_{90}\) nem primeira data defendida. A conta acima é especificação, não execução.

Se “Fisher” for entendido como **informação de Fisher**, e não como combinação de valores-\(p\), então \(F_P=\sum_iJ_i^TC_i^{-1}J_i\) exige Jacobianos de cada previsão em relação ao vetor de parâmetros do **pacote**, nuisances e covariância cruzada. Uma Fisher escalar de β seria insuficiente e responderia à pergunta errada.

### C.3.3 Razão de verossimilhança do pacote contra os nulos

Em resumos gaussianos \(y\), uma candidata para hipóteses pontuais é

\[
q_{P:0}=
(y-\mu_0)^TC^{-1}(y-\mu_0)
-(y-\mu_P)^TC^{-1}(y-\mu_P).
\]

O sinal e os graus de liberdade precisam ser pré-fixados. Se o nulo de oscilação tiver \(\Delta m^2_{21}\) livre, usa-se o perfil desse parâmetro, e o centro \(7,388\) serve somente para planejamento. Se o nulo for ponto, a fórmula acima vale tal qual. Não se maximiza apenas β: \(E_0\), a identificação, o ramo S/L, os nuisances e os mapas físicos permanecem dentro de \(H_P\) ou são explicitamente atribuídos ao nulo correspondente.

A potência exige a distribuição de \(q_{P:0}\) sob \(H_P\) e sob cada alternativa, inclusive qui-quadrado não central ou simulação congelada quando aplicável. Como os nulos completos, os nuisance e a covariância ainda não foram fechados, **esta candidata não tem data nem \(D_{90}\) defensável**. A escolha entre Stouffer, Fisher e verossimilhança deve ocorrer antes do resultado e sem selecionar a regra pelo ramo favorável.

## C.4 — Primeira data: horizonte condicional e parede

### O que a conta de Stouffer permite dizer

A extrapolação meramente estatística usada na revisão, ancorada nos 207,2 dias reais e sem piso sistemático, é

\[
T_{\mathrm{novo}}(\sigma_J)\simeq
207,2\left(\frac{0,078}{\sigma_J}\right)^2
\quad\text{dias vivos novos}.
\]

Ela daria aproximadamente **1.806 dias vivos** para atingir a fronteira conjunta \(\sigma_J\simeq0,0264169\), e **2.189 dias vivos** para \(\sigma_J=0,024\). Estes são valores de planejamento, não previsão da colaboração nem conversão para calendário. A revisão já separava cerca de 1.400–2.200 dias vivos para o poder JUNO sozinho; a contribuição SO reduz o requisito do incremento, sem eliminar covariância, sistemática ou a regra individual.

### A resposta de data

- **26/08/2031** é apenas seis anos civis após o início físico do JUNO; a Tabela 6 de arXiv:2204.13249 não define, no material revisado, “seis anos” em dias vivos nem uma liberação nessa data. Além disso, \(\sigma=0,024\) é previsão para o acumulado, não prova de erro do incremento.
- **2034** é o primeiro horizonte em que o forecast público completo do SO, \(\sigma(N_\mathrm{eff})=0,045\), e um incremento JUNO no nível requerido podem ser colocados no mesmo desenho. Por isso, **2034 é o primeiro ano plausível para \(\lambda_S\geq6,28\)**, não uma data prometida de publicação ou abertura.
- **Parede:** não há data anterior defensável. Um produto SO mais precoce poderia antecipar o cruzamento somente se vier com data, \(\sigma\), covariância e regra pré-congelada; os degraus históricos “~2027/~2029” do core não são calendário atual de liberação cega e não foram usados como tal.
- **Bloqueio de fronteira:** a revisão mostra \(6,2663<D_{90}\) em \(\Delta m^2\), enquanto a regra congelada está em \(m_2\). A diferença métrica é pequena, mas muda a fronteira. O número final deve ser produzido na métrica congelada antes da tranca; nenhum lado dessa diferença foi usado aqui para declarar um veredito.

**Condições para transformar 2034 em data real:** incremento JUNO futuro e não comunicado à casa; covariância condicional aceita; métrica \(m_2\) resolvida sem emenda oculta; ramo S/L e \(Y_p\) fixados; covariância SO+Planck e grupo CMB único; sistemáticas incluídas; regra omnibus e pesos congelados antes dos resultados; manutenção dos vereditos individuais e da contabilidade de multiplicidade. Se qualquer uma falhar, a resposta volta a ser **parede**, não teste.

> **CORREÇÃO AO LADO K09 — C.4.** Os **1.806 dias vivos** pertencem à fronteira com pesos \(\propto D\); com pesos iguais, a fronteira é **2.162 dias vivos**. Para \(\sigma_J=0,024\), a extrapolação de 2.189 dias vivos não muda, mas o poder é **90,5 % com pesos iguais** e 96,4 % com pesos \(\propto D\); são cenários distintos.
>
> **2034 é somente o fim do levantamento do SO, não a primeira data do cruzamento e não uma antecipação do JUNO. A combinação não antecipa o JUNO sozinho, que chega antes ao portão no cenário ideal.** Ela acrescenta uma segunda pergunta e redundância, não um atalho temporal. Continuam bloqueados o produto SO datado, a métrica congelada, a covariância, as sistemáticas e a regra omnibus anterior ao resultado.

## C.5 — Ringdown: eventos equivalentes, catálogo, taxa e janela

### C.5.1 Conferência do requisito de 90 %

Reuso direto de `PODER_RAMO_B_ANTES_DE_ABRIR.json` e da revisão K01:

| Base congelada | Poder sem viés/sistemática | Fator de informação para \(D_{90}\) | Eventos equivalentes \(N_{\rm eq}=N_{\rm base}F\) | Equivalentes adicionais |
|---|---:|---:|---:|---:|
| D10, sem hold | 3,9346337578 | 2,548738 | **25,4874** | **15,4874** |
| D14, com holds | 4,6374126778 | 1,834773 | **25,6868** | **11,6868** |

Confirma-se, portanto, a faixa arredondada **25,5–25,7 eventos equivalentes**. “Equivalente” é essencial: a conversão pressupõe informação média constante \(\propto N\), ausência de sistemática e nenhuma perda por convergência da PE. Não é uma contagem física exata nem um limiar válido com viés instrumental.

### C.5.2 Quantos existem nos catálogos públicos

O catálogo GWTC-5.0 é cumulativo até O4b e o material LVK reporta cerca de **390 candidatas significativas em O1–O4b**; O4c ainda estava em análise e não deve ser contado como amostra elegível pronta [KNOWN, a conferir — arXiv:2605.27223v2 e arXiv:2608.12193v1].

> **CORREÇÃO AO LADO K09 imediatamente aplicável a este parágrafo:** a cifra cumulativa acima **não foi sustentada pelo resumo citado e está retirada**. Ela não deve ser reutilizada nem entrar em conta alguma. O4c igualmente não entra como amostra pronta. O que permanece válido é somente o censo congelado do ramo B abaixo.

Esse total **não** é o número elegível para o ramo B. O critério congelado exige, entre outras condições, SNR de rede \(\geq12\), \(M_{f,\mathrm{det}}\) mediana \(\geq40\,M_\odot\), \(0\leq\chi_f<0,98\), fonte GWOSC/GR IMR e ausência no corpus de publicação/auditoria congelado. O censo de 44 candidatas de teste devolve:

- **14 elegíveis**;
- **10 sem data-quality hold** e 4 com hold;
- **8 pendentes de metadados GR**, que não entram até satisfazer a mesma regra;
- **22 reprovadas** pelo corte.

Essas contagens vêm do V1 congelado e do Mapa, não de uma nova varredura de catálogo ou de posteriores. Nenhum valor de deformação do conjunto D foi lido.

### C.5.3 Taxa elegível: retrospectiva bruta versus taxa publicada

As janelas públicas O4a (24/05/2023–16/01/2024) e O4b (10/04/2024–28/01/2025) somam aproximadamente 530 dias de observação [KNOWN, a conferir — arXiv:2605.27090v1 e arXiv:2605.27223v2]. Com isso, a taxa **retrospectiva bruta e não generalizável** é:

\[
r_D\approx\frac{14}{530/365,25}\simeq9,6
\quad\text{elegíveis/ano},
\qquad
r_{D10}\approx6,9\quad\text{sem hold/ano}.
\]

Não é taxa oficial da colaboração nem previsão de elegíveis IR1/O5: é só o quociente do censo congelado pelo tempo das janelas, sem modelo de seleção, com 8 pendências e sem garantia de informação média constante.

A página IGWN, atualizada em 26/10/2026, prevê **IR1 de seis meses a partir de meados de janeiro de 2027**, sensibilidade provavelmente semelhante à de O4, e **O5 concebido para 2029–2031**, ainda em planejamento inicial [KNOWN, a conferir — IGWN Observing Capabilities, outubro de 2026]. A mesma fonte publica taxas de **alertas** BBH, não de detecções confidentes nem de eventos que passam no corte só-220; ela adverte expressamente que muitos alertas não sobrevivem como detecções confiáveis. Por isso, suas taxas não podem ser multiplicadas por uma fração elegível inventada.

### C.5.4 IR1 ou O5: o que se pode afirmar sem inventar data

Para cruzar \(D_{90}\) dentro dos seis meses de IR1, seriam necessárias aproximadamente:

- **31,0 elegíveis/ano** a partir de D10;
- **23,4 elegíveis/ano** a partir de D14.

Nas taxas retrospectivas correspondentes, os tempos adicionais seriam cerca de **2,24 anos (aproximadamente 27 meses; D10, com os 10 sem hold a 6,9/ano)** ou **14,5 meses (D14, com os 14 elegíveis a 9,6/ano)**, não seis meses. Portanto, **IR1 sozinho não alcança \(D_{90}\) sob essa extrapolação**. A primeira janela plausível é **O5, 2029–2031**, mas a data dentro de O5 é **[OPEN]**: depende do início real, sensibilidade, rede, taxa do mesmo corte, resolução dos holds/pendências, informação por evento e sistemática. A contagem mínima IR1 exigiria uma taxa elegível mais de duas vezes a retrospectiva, não apenas a taxa de alertas BBH publicada pelo IGWN.

### C.5.5 O que D decide — e o que não decide

A memória `ramo-b-reaberto-05out.md` preserva a reabertura de 05/10 e, ao lado, a correção de 28/10: a leitura do autor coloca o pedágio de Planck na propagação, e a calibração A, **NOT_BLIND**, corrigiu a rota sem produzir veredito. O registro selado `f2b_errata_v404` dá o estado `WITHDRAWN_BEFORE_DATA__ROUTE_CORRECTED_BY_NOT_BLIND_CALIBRATION_AND_AUTHOR_READING_2026_10_28`; D permanece fechado.

Logo, um futuro D poderia decidir **somente o par**
\[
k=2\pi/\hat\kappa(\chi_f),\qquad M_X=M_f,
\qquad \text{identificação/envoltória},
\]
sob a lei congelada. **Não entra como evidência geral “pela teoria”, não decide β isoladamente, não decide a forma GKSL/lei geral de defasamento, não decide R2 e não move o gate.** A retirada não é falsificação; é correção de rota anterior ao dado.

> **CORREÇÃO AO LADO K09 — C.5.1 a C.5.5.**
>
> **1. O piso é sem viés; com o viés medido, contagem não basta.** Os 25,5/25,7 eventos equivalentes só valem sob informação \(\propto N\) e sem viés/sistemática. Com \(\sigma_{\rm viés}=0,0686\) (C2 ampla), o poder de D10 satura em aproximadamente **5,8**, abaixo de \(D_{90}=6,28155\); portanto **D90 não é alcançável apenas aumentando a contagem**. O5 não pode ser apresentado como janela suficiente sem informação adicional e tratamento da sistemática. Fonte: `PODER_RAMO_B_ANTES_DE_ABRIR.json`, sha256 `05bc5a1f2592b776…a4935`; valor reproduzido pela revisão, não recalculado aqui.
>
> **2. A cifra cumulativa de C.5.2 fica retirada.** O resumo citado não sustenta aquele número; ele não entra em nenhuma conta. Permanecem apenas o censo congelado do ramo B — 14 elegíveis, 10 sem hold, 8 pendentes, 22 reprovados entre 44 candidatas — e o recorte O4b abaixo.
>
> **3. A taxa de referência corrigida usa somente O4b.** Dos 14 elegíveis, 13 são de O4b; dos 10 sem hold, 9 são de O4b. Com 293 dias de O4b, a revisão obtém **16,2 elegíveis/ano para D14 → 8,7 meses** e **11,2 sem hold/ano para D10 → 16,6 meses**. A antiga faixa **17–27 meses para D10** pode permanecer somente como contexto conservador da taxa mista O4a+O4b; a taxa mista **não é a base única**. Todas são extrapolações retrospectivas sem viés, não forecast oficial. IR1 continua insuficiente; com o viés medido, o bloqueio é ainda mais forte.
>
> **4. A atribuição e o estado de D são exatos.** A **retirada do canal F2b é conclusão da gerência**, registrada em `f2b_errata_v404`; ela **não é uma decisão atribuída ao operador**. O operador **AUTORIZOU D em 29/10** («autorizo a realização do teste do conjunto D»; sha256 `9e54b47780dab101…dbc9`; Mapa seq 1545) e **escolheu a opção (c) em 03/11** («concordo com c, porque se o teste não tiver poder não vou inseri-lo no um.py»; sha256 `73466598d3419fb0…8289`; seq 1744). **Nada foi aberto** (seq 1775). D só decide o par nomeado acima; **D não decide a retirada**, que é correção documental da gerência, e só entraria no `um.py` se tivesse poder.

## Bloqueios que permanecem

1. Covariância condicional do incremento JUNO e definição final da métrica \(m_2\).
2. Escolha TGL-S/L, \(Y_p\), covariância SO+Planck e sistemáticas do SO.
3. Regra omnibus única, pesos, sinais, nulos, caudas e função de veredito congelados antes dos resultados.
4. Nenhuma data oficial de produto cego SO e nenhuma conversão publicada de dias vivos JUNO para calendário.
5. Taxa elegível IR1/O5 do corte só-220, convergência da PE e sistemática do ringdown.
6. Nenhuma adição ao pacote que use o par F2b retirado como se fosse teste geral da teoria.

**Estatuto final:** parede medida hoje; horizonte condicional 2034 para Stouffer JUNO+SO; janela O5 sem data para ringdown. Nenhum teste executado.

> **Estatuto final corrigido K09:** parede medida hoje; 2034 é só o fim do levantamento SO e a combinação não antecipa o JUNO sozinho. Ringdown tem piso sem viés de 25,5/25,7, saturação de D10 em aproximadamente 5,8 com viés 0,0686 e tempos retrospectivos somente O4b de 8,7 meses (D14) e 16,6 meses (D10). D está autorizado e não aberto. Nenhum teste ou cálculo novo foi executado nesta correção.
