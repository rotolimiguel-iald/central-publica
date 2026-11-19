# K04/B — m₂: desfechos, calendário, incremento e segunda testemunha — K09

**Estatuto geral:** `[DERIVED—PLANEJAMENTO]` para contas com agregados públicos; `[OPEN]` para covariância, data ou informação não localizada. Nenhum vetor de dados foi baixado ou lido, nenhuma likelihood foi aberta, nenhuma estatística observada nova foi calculada, nada de H0DN foi executado e nenhum teste observado foi realizado. As fórmulas foram avaliadas analiticamente; uma quadratura de Simpson foi usada apenas como conferência numérica de planejamento.

**Preservação:** REV0 e REV1 permanecem intactos. A versão R3, seus scripts e suas medidas estão preservados em `K04/M2/REV2/`; `ERRATA_M2_K04_R3.md` não foi alterada. As correções desta rodada estão em [ERRATA_M2_K09](ERRATA_M2_K09.md). Os dados bibliográficos estruturados estão em [ERRATA_NEUTRINO_V412_DADOS_K09.json](ERRATA_NEUTRINO_V412_DADOS_K09.json).

## Conclusão antes das contas

1. **Dois estados devem ser ditos juntos.** Pelo perito autônomo JUNO de 207,2 dias, `r_m₂ = 1,937997`, o estado é `TGL_NU_M2_ARMED_CONSISTENT`. Pela letra “determinação global mais recente”, o ajuste global está na **borda de `TGL_NU_M2_TENSION`**: a tabela NuFIT 6.1 dá `r_m₂ = 3,024242`; a eq. 11 do artigo dá `3,044179`; a representação simétrica arredondada usada no core, `7,530 ± 0,100`, dá `2,952854`. A borda é de fonte e de representação do erro, não algo a esconder. Rota `neutrinos.m2.normalizacao`, seq. 93 e 142.
2. **O código não é o rascunho K01.** Depois de verificar os grupos autônomos, qualquer última linha da escada com `r ≥ 3` vai a `TGL_NU_M2_TENSION`, inclusive `r ≥ 5` sem segunda determinação; nesse caso o campo `tensao_global_5sigma_sem_2a_determinacao` é aceso. `FALSIFIED` exige duas determinações autônomas independentes `≥ 5σ`. `MATCHED_PROSPECTIVELY` é veredito permitido no texto, mas **não tem ramo no código**. `UNDER`, `SINGLE_P` e `OPEN_RULE_GAP` não são vereditos do código.
3. **Não há hoje par que satisfaça `FALSIFIED`.** SK-Gd reator está a `3,605064σ` da previsão, mas seu centro 9,08 está a `3,101149σ` do JUNO 207,2 dias. O cenário de 380,0785536 dias adicionais pressupõe que a anomalia SK-Gd persista, que o centro e a forma do erro fiquem parados e que `σ ∝ T⁻¹/²`; não é agenda, prova de independência nem previsão de liberação.
4. **Cronologia corrigida:** o degrau de 207 dias foi apresentado publicamente na Neutrino 2026 em **22/06/2026** (`event/15740/contributions/155563`); as transparências do IHEP de **15/07/2026** confirmam explicitamente `7,388 ± 0,078` (`event/28557/contributions/223278`, anexo `104657/141297`). Ambas as datas precedem o pino de **08/08/2026**. O artigo arXiv:2609.37895v1 é posterior, de **29/09/2026**. Portanto, a leitura de 207 dias **não é primeira leitura prospectiva nem cega**. Prospectivo hoje é somente dado posterior a **18/05/2026** ainda não mostrado.
5. **Calendário principal é o do artigo de 207,2 dias, sempre como brinquedo:** sem piso, 5σ cumulativo em **16/08/2029** e D90 em **31/10/2031**; para o incremento sozinho, **11/03/2030** e **25/05/2032**. Com o piso ajustado de dois pontos, `s0 = 0,052587652`, ambos são inalcançáveis. Nenhuma dessas datas é cronograma. O brinquedo histórico do projeto não é apresentado como se fosse o orçamento do artigo de 207 dias.
6. **Vale a métrica congelada em m₂.** Em 207,2 dias, `r_m₂ = 1,937997`; em Δm², `r_Δ = 1,928084`, somente como comparação. A Tabela 6 dá `DΔ = 6,266272 < D90 = 6,281552` e `D_m₂ = 6,298490`; trocar a métrica do veredito seria emenda.
7. O desenho realmente prospectivo está separado em [PRE_REGISTRO_INCREMENTO_JUNO_RASCUNHO_K09](PRE_REGISTRO_INCREMENTO_JUNO_RASCUNHO_K09.md), sem escolha entre a regra de duas testemunhas e uma regra emendada de uma testemunha com limiar explícito.

---

## 1. D, hipóteses e modelos que não podem ser misturados

Em unidades de `10⁻⁵ eV²`:

\[
\Delta_{\rm pred}=7,237609466718292,\qquad
\Delta_0=7,388,\qquad
\delta=\Delta_0-\Delta_{\rm pred}=0,150390533281708 .
\]

Para qualquer hipótese de planejamento,

\[
D_\Delta(s)=\frac{\delta}{s},\qquad
D_{m_2}(s)=\frac{m_2(\Delta_0)\,|m_2(\Delta_0)-m_{2,\rm TGL}|}{5s}.
\]

`D` mede a distância entre a previsão e o centro público de planejamento; não é, sozinho, um ramo adicional do código.

A razão congelada é

\[
m_2=\sqrt{10\mu}\ {\rm meV},\qquad
\sigma_{m_2}=\frac{5\sigma_\mu}{m_2}
=\frac{m_2\sigma_\mu}{2\mu},\qquad
r_{m_2}=\frac{m_2|m_2-m_{2,\rm TGL}|}{5\sigma_\mu}.
\]

### 1.1 Medida ou incremento independente

**(a1) Posterior público de planejamento, com prior plano declarado:**

\[
\mu\sim N(7,388,0,078^2),\qquad X\mid\mu\sim N(\mu,s^2)
\quad\Rightarrow\quad X\sim N(7,388,0,078^2+s^2).
\]

O erro atual entra uma única vez. Esse posterior é construção de planejamento, não publicado pela colaboração.

**(a2) Verdade = previsão:** `X ~ N(Δpred,s²)`, sem erro atual adicional.

### 1.2 Liberação cumulativa com covariância

Se `X0` é o estimador atual, `X` o cumulativo futuro e `Cov(X0,X)=C`:

\[
\operatorname{Var}(X)=0,078^2+s^2-2C.
\]

**(b1) Posterior público cumulativo:** média 7,388 e essa variância.

**(b2) Verdade = previsão condicionada ao valor atual observado `X0=x0`:**

\[
E[X\mid X_0=x_0]=\Delta_{\rm pred}+\frac{C}{0,078^2}(x_0-\Delta_{\rm pred}),
\qquad
\operatorname{Var}(X\mid X_0=x_0)=s^2-\frac{C^2}{0,078^2}.
\]

Com `C=0`, (b2) reduz a (a2). O exemplo aninhado `C=s²` é somente um **brinquedo estatístico**; a covariância real do JUNO permanece `OPEN`.

### 1.3 As duas caudas na métrica frozen

Seja `M=m₂,TGL`, `m=√(10X)` e `r=m|m−M|/(5s)`. Para `r ≥ t`:

- **cauda superior**, `m ≥ M`: `m ≥ H_t`, com
  \[
  H_t=\frac{M+\sqrt{M^2+20ts}}2;
  \]
- **cauda inferior**, `0 ≤ m ≤ M`: se `M²−20ts ≥ 0`, `L_t ≤ m ≤ U_t`, com
  \[
  L_t=\frac{M-\sqrt{M^2-20ts}}2,\qquad
  U_t=\frac{M+\sqrt{M^2-20ts}}2.
  \]

A região inferior **não** é `m ≤ L_t`. Em `X`, a probabilidade é

\[
P(L_t^2/10 \le X \le U_t^2/10) + P(X \ge H_t^2/10).
\]

Se o discriminante for negativo, não há intervalo inferior. Essa implementação foi conferida por CDF e por quadratura independente; os resultados e o diff estão em `K04/M2/K09/medidas/`.

---

## 2. Tabelas independentes — medida/incremento independente

Todas as células foram reemitidas. `P(r<3)` foi acrescentado explicitamente; `PΔ(r≥5)` é apenas comparação em Δm². A última coluna é uma propriedade numérica de `DΔ`, não um veredito.

### (a1) Posterior público

| Precisão | σ | DΔ | D_m₂ | P(r≤1) | P(1<r<3) | P(r<3) | P(3≤r<5) | P(r≥5), m₂ | PΔ(r≥5) | DΔ≥5 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|
| 0,7 % | 0,051716 | 2,908008 | 2,922959 | 13,026972 % | 38,600459 % | 51,627431 % | 35,494403 % | 12,878167 % | 12,384071 % | não |
| 0,5 % | 0,036940 | 4,071211 | 4,092143 | 7,928136 % | 24,106352 % | 32,034489 % | 32,919916 % | 35,045595 % | 34,553737 % | não |
| 0,407121 % | 0,030078 | 5,000001 | 5,025709 | 5,957831 % | 17,331223 % | 23,289054 % | 26,330206 % | 50,380739 % | 50,016055 % | sim |
| 0,324061 % | 0,023942 | 6,281550 | 6,313847 | 4,426481 % | 11,978062 % | 16,404543 % | 18,672345 % | 64,923112 % | 64,702532 % | sim |
| 0,3 % | 0,022164 | 6,785352 | 6,820238 | 4,021760 % | 10,604120 % | 14,625881 % | 16,406872 % | 68,967247 % | 68,786155 % | sim |
| Tabela 6, σ = 0,024 | 0,024000 | 6,266272 | 6,298490 | 4,440057 % | 12,024639 % | 16,464696 % | 18,747300 % | 64,788004 % | 64,566086 % | sim |

### (a2) Verdade = previsão

| Precisão | σ | DΔ | D_m₂ | P(r≤1) | P(1<r<3) | P(r<3) | P(3≤r<5) | P(r≥5), m₂ | PΔ(r≥5) | DΔ≥5 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|
| 0,7 % | 0,051716 | 2,908008 | 2,922959 | 68,269490 % | 31,460492 % | 99,729982 % | 0,269959 % | 0,000058 % | 0,000057 % | não |
| 0,5 % | 0,036940 | 4,071211 | 4,092143 | 68,269225 % | 31,460776 % | 99,730001 % | 0,269941 % | 0,000058 % | 0,000057 % | não |
| 0,407121 % | 0,030078 | 5,000001 | 5,025709 | 68,269132 % | 31,460875 % | 99,730007 % | 0,269935 % | 0,000058 % | 0,000057 % | sim |
| 0,324061 % | 0,023942 | 6,281550 | 6,313847 | 68,269065 % | 31,460947 % | 99,730012 % | 0,269930 % | 0,000058 % | 0,000057 % | sim |
| 0,3 % | 0,022164 | 6,785352 | 6,820238 | 68,269048 % | 31,460965 % | 99,730013 % | 0,269929 % | 0,000058 % | 0,000057 % | sim |
| Tabela 6, σ = 0,024 | 0,024000 | 6,266272 | 6,298490 | 68,269066 % | 31,460947 % | 99,730012 % | 0,269930 % | 0,000058 % | 0,000057 % | sim |

Os benchmarks do revisor são reproduzidos na precisão pedida: **P(r≤1) = 68,27 %**, **P(1<r<3) = 31,46 %**, **r<3 = 99,73 %**. Pequenas variações na sexta casa vêm da propagação de primeira ordem no valor observado, não de outra métrica.

---

## 3. Tabelas cumulativas — somente o brinquedo `C=s²`

### (b1) Posterior público cumulativo

| Precisão | σ | DΔ | D_m₂ | P(r≤1) | P(1<r<3) | P(r<3) | P(3≤r<5) | P(r≥5), m₂ | PΔ(r≥5) | DΔ≥5 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|
| 0,7 % | 0,051716 | 2,908008 | 2,922959 | 4,510565 % | 48,181616 % | 52,692181 % | 43,828997 % | 3,478822 % | 3,195125 % | não |
| 0,5 % | 0,036940 | 4,071211 | 4,092143 | 4,606500 % | 23,411882 % | 28,018382 % | 40,515950 % | 31,465668 % | 30,874110 % | não |
| 0,407121 % | 0,030078 | 5,000001 | 5,025709 | 4,117346 % | 15,894543 % | 20,011889 % | 29,562408 % | 50,425704 % | 50,001481 % | sim |
| 0,324061 % | 0,023942 | 6,281550 | 6,313847 | 3,480440 % | 10,823630 % | 14,304070 % | 19,411387 % | 66,284543 % | 66,044954 % | sim |
| 0,3 % | 0,022164 | 6,785352 | 6,820238 | 3,267645 % | 9,600023 % | 12,867668 % | 16,751363 % | 70,380969 % | 70,187987 % | sim |
| Tabela 6, σ = 0,024 | 0,024000 | 6,266272 | 6,298490 | 3,487232 % | 10,865536 % | 14,352768 % | 19,501649 % | 66,145584 % | 65,904386 % | sim |

### (b2) Verdade = previsão condicionada ao valor atual observado

| Precisão | σ condicional | DΔ | D_m₂ | P(r≤1) | P(1<r<3) | P(r<3) | P(3≤r<5) | P(r≥5), m₂ | PΔ(r≥5) | DΔ≥5 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|
| 0,7 % | 0,038714426 | 2,908008 | 2,922959 | 35,295908 % | 63,570093 % | 98,866001 % | 1,133954 % | 0,000045 % | 0,000033 % | não |
| 0,5 % | 0,032534742 | 4,071211 | 4,092143 | 52,384985 % | 46,692452 % | 99,077437 % | 0,922357 % | 0,000206 % | 0,000174 % | não |
| 0,407121 % | 0,027751832 | 5,000001 | 5,025709 | 57,973624 % | 41,280722 % | 99,254346 % | 0,745428 % | 0,000226 % | 0,000198 % | sim |
| 0,324061 % | 0,022785907 | 6,281550 | 6,313847 | 61,856115 % | 37,553628 % | 99,409744 % | 0,590055 % | 0,000201 % | 0,000181 % | sim |
| 0,3 % | 0,021250371 | 6,785352 | 6,820238 | 62,796621 % | 36,654972 % | 99,451593 % | 0,548218 % | 0,000189 % | 0,000172 % | sim |
| Tabela 6, σ = 0,024 | 0,022835662 | 6,266272 | 6,298490 | 61,823864 % | 37,584474 % | 99,408338 % | 0,591460 % | 0,000202 % | 0,000182 % | sim |

### 3.1 Quais células mudaram

O diff integral, célula por célula, está em [mudancas_celulas_k09](K04/M2/K09/medidas/mudancas_celulas_k09.md).

- **(a1):** `P(r≤1)` cai 1,29–1,67 pp; `P(1<r<3)` sobe 1,29–1,48 pp; `P(3≤r<5)` muda pouco; o maior ajuste de `P(r≥5)` é **+0,062626 pp** (0,3 %).
- **(a2):** a correção é a maior: `P(r≤1)` sai de 84,09–84,12 % para 68,27 %, e `P(1<r<3)` de 15,75–15,77 % para 31,46 %; `r<3` sai de aproximadamente 99,86 % para 99,73 %.
- **(b1)/(b2):** as faixas baixas também foram refeitas. Na Tabela 6, `P(r≤1)` passa a 3,487232 % em b1 e 61,823864 % em b2; `r<3` passa a 14,352768 % e 99,408338 %, respectivamente.
- **Quase inalteradas:** `P(r≥5)` em m₂ muda no máximo 0,062626 pp nas quatro tabelas; `PΔ(r≥5)`, `DΔ` e `D_m₂` não mudam.
- **MATCHED:** `P(rP≤1)` passa de 17,599161 % para 17,430120 %. Em “Solares sem KamLAND”, `P(rS≤1)` passa de 98,493504 % para **42,157532 %**, e a probabilidade conjunta de brinquedo passa de 17,334031 % para **7,348108 %**. As demais células MATCHED foram reemitidas na seção 7.

---

## 4. Calendário a partir do artigo de 207,2 dias — brinquedos, não cronogramas

### 4.1 Sem piso

Usa-se somente `σ(T)=0,078√(207,2/T)`, com centro parado e 100 % de dias vivos. As datas cumulativas e as do incremento não herdam as probabilidades do modelo independente.

| Alvo | σ alvo | T total | Adicional cumulativo | Data ideal cumulativa* | Dias novos no incremento | Data ideal incremento* |
|---|---:|---:|---:|---|---:|---|
| 5σ | 0,030078107 | 1393,406931 d | 1186,206931 d | **16/08/2029** | 1393,406931 d | **11/03/2030** |
| D90 | 0,023941622 | 2199,235900 d | 1992,035900 d | **31/10/2031** | 2199,235900 d | **25/05/2032** |

\* Aritmética desde 18/05/2026. São brinquedos de exposição, não cronograma nem liberação anunciada.

Para referência de limiar, `r=3` no incremento dá 501,626495 dias novos e data de brinquedo **01/10/2027**; isso não altera a necessidade de ler a última linha da escada antes de atribuir `TENSION`.

### 4.2 Piso ajustado de dois pontos

Com `σ²=a/T+s0²` e os dois pontos 59,1/207,2 dias, `a=0,687601245` e **`s0=0,052587652`**. Como esse piso excede os alvos de 5σ e D90, **ambos são inalcançáveis nesse brinquedo**. Dois pontos ajustam dois parâmetros e as análises mudaram: não é piso medido.

### 4.3 Duty cycle somente como cenário

Se, apenas como cenário, se repetir `207,2/265 = 78,188679 %` do período passado:

| Alvo | Data cumulativa, cenário duty | Data incremento, cenário duty |
|---|---|---|
| 5σ | 13/07/2030 | 04/04/2031 |
| D90 | 08/05/2033 | 28/01/2034 |

Essas datas são cenários condicionais, não dever nem previsão de eficiência futura. As datas do brinquedo de decomposição do projeto ficam como histórico em REV2 e **não** substituem a leitura do artigo de 207 dias acima.

---

## 5. Cronologia, pinos e prospectividade

| Data | Fato público ou custodial | Identificador |
|---|---|---|
| 18/11/2025 | JUNO 59,1 dias em arXiv | arXiv:2511.14593v1 |
| 19/11/2025 | Apresentação pública dos primeiros resultados | IHEP/JUNO, Jiangmen |
| 10/06/2026 | Artigo JUNO 59,1 dias | Nature 654, 343–348; DOI 10.1038/s41586-026-10538-z |
| **22/06/2026** | Apresentação do degrau de 207 dias na Neutrino 2026 | `indico.global/event/15740/contributions/155563`; anexo `72452/141000/JUNO-Neutrino2026-Vfinal.pdf` |
| **15/07/2026** | Transparências com `7,388 ± 0,078` e 207,2 dias | `indico.ihep.ac.cn/event/28557/contributions/223278`; anexo `104657/141297/July2026_v2.pdf` |
| 22/07/2026 | Notícia JINR: “207 days … reported at Neutrino 2026 conference in July” | `dlnp.jinr.ru/en/news/3850` |
| **08/08/2026** | Pino da regra original | `4bdae22a277aa393094a1bf416db12a5e782b673e9e9b3ddd6a2fb8c7a64075c` |
| 29/09/2026 | Artigo JUNO 207,2 dias | arXiv:2609.37895v1 |
| 02/10/2026 | SK-Gd reator | arXiv:2610.03143v1 |
| 30–31/10/2026 | Esta casa leu e reproduziu as tensões | memória da casa |

A conferência Neutrino 2026 ocorreu oficialmente de **21 a 26/06/2026**, com a apresentação JUNO em **22/06**. A notícia JINR de 22/07 diz “July”, mas não deve substituir o identificador e a data oficiais da contribuição. Mesmo adotando conservadoramente 15/07 como a primeira confirmação explícita do número nesta revisão, o valor já era público antes de 08/08.

O hash `e24877751ad810225412cc294c06b83eefeaedc67e4c5cabc7779ac01e4b19c3` pertence ao **dicionário portado**, com chaves adicionais; não é o pino do arquivo original de 08/08. Os dois são guardados no JSON de dados.

**Consequência:** 207,2 dias não é primeira leitura prospectiva nem leitura cega. O único incremento JUNO prospectivo para este desenho é o dado posterior a 18/05/2026 ainda não mostrado.

---

## 6. Incremento 59,1 → 207,2 e covariância

Com `w1=1/0,12²` e `w2=1/0,078²`, a ilustração de variância inversa fornece

\[
\mu_\Delta=\frac{w_2(7,388)-w_1(7,50)}{w_2-w_1}=7,306061,
\qquad
\sigma_\Delta=(w_2-w_1)^{-1/2}=0,102640 .
\]

| Quantidade | Resultado |
|---|---:|
| centro ilustrativo | 7,306061 |
| σ ilustrativo | 0,102640 |
| r contra previsão, Δm² | 0,666902 |
| r contra previsão, frozen m₂ | 0,668472 |
| distância ao centro 7,50, apenas σ do incremento — estatística errada para a comparação | 1,889502 |
| **distância correta no aninhamento estatístico puro** | **1,228176σ** |

A forma equivalente é `(7,50−7,388)/√(0,12²−0,078²) = 1,228176`. A liberação é cumulativa, mudou volume fiducial, seleção, fundos e âncora; erros totais foram tratados como pesos estatísticos apenas para a ilustração. Não é determinação independente.

### 6.1 Forma geral com covariância

Se `X0` e `Xc` são estimadores cumulativos com `V0`, `Vc` e `C=Cov(X0,Xc)`, defina `λ=C/V0` e

\[
Y=\frac{X_c-\lambda X_0}{1-\lambda},\qquad
\operatorname{Var}(Y)=\frac{V_c+\lambda^2V_0-2\lambda C}{(1-\lambda)^2}.
\]

No aninhamento de variância inversa com informação nova independente, `C=Vc`, recuperando a ilustração acima. Sem a covariância e sem a resposta conjunta dos nuisances, **λ, o centro incremental e sua variância não são identificáveis**. Perde-se a validade do erro, da razão `r`, da alegação de independência e da cegueira operacional; `C=0` ou `C=Vc` não pode ser atribuído ao JUNO sem fonte.

---

## 7. Determinações e segunda testemunha

A convenção é frozen em m₂; nas assimetrias usa-se o erro do lado que aponta para a previsão. `r_Δ` e `σ5` são comparações, não troca de métrica.

| Entrada | Centro | erro + | erro − | σ lado | r_m₂ | r_Δ | σ5 | Fonte/papel |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| JUNO 207,2 d | 7,388 | 0,078 | 0,078 | 0,078 | **1,937997** | 1,928084 | 0,030233 | arXiv:2609.37895v1; perito P |
| SNO+ | 7,910 | 0,220 | 0,250 | 0,250 | 2,749285 | 2,689562 | 0,137464 | arXiv:2511.11856v4; PRL 137, 101807 |
| **SK-Gd reator** | 9,080 | 0,550 | 0,540 | 0,540 | **3,605064** | 3,411834 | 0,389347 | arXiv:2610.03143v1; cenário S |
| KamLAND-only | 7,540 | 0,190 | 0,180 | 0,180 | 1,697137 | 1,679947 | 0,061097 | arXiv:1303.4667v2, Tabela 3 |
| Solares sem KamLAND | 6,100 | 0,950 | 0,810 | **0,950** | 1,146322 | 1,197484 | 0,217801 | arXiv:2312.12907v2; PRD 109, 092001 |
| JUNO 59,1 d | 7,500 | 0,120 | 0,120 | 0,120 | 2,206054 | 2,186588 | 0,052945 | arXiv:2511.14593v1; subconjunto de P |
| **NuFIT 6.1, tabela** | 7,537 | **0,094** | **0,100** | **0,100** | **3,024242** | **2,993905** | 0,060485 | NuFIT node 309; global com JUNO 59 d |
| **NuFIT 6.1, artigo eq. 11** | 7,530 | **0,096** | **0,097** | **0,097** | **3,044179** | **3,014335** | 0,059057 | arXiv:2601.09791v1/v2 |
| Capozzi et al. | 7,480 | 0,100 | 0,100 | 0,100 | 2,443867 | 2,423905 | 0,048877 | arXiv:2511.21650 |
| Bari 2026.a NO | 7,465 | 0,072 | 0,080 | 0,080 | 2,864363 | 2,842382 | 0,045830 | Global-nu 2026.a; preliminar |
| SK-Gd solar+reator | 8,940 | 0,460 | 0,470 | 0,470 | 3,813218 | 3,622108 | 0,358442 | arXiv:2610.03143v1; mesma colaboração |
| SNO+ reator+solar | 7,590 | 0,170 | 0,170 | 0,170 | 2,097521 | 2,072885 | 0,071316 | arXiv:2511.11856v4, Tabela 3 |

**NuFIT sem inversão:** a tabela oficial tem `+0,094/−0,100`, não `+0,100/−0,094`; com o lado correto, `r_m₂ = 3,024242`, não 3,217279. A eq. 11 do artigo tem `+0,096/−0,097`; sua forma exata dá 3,044179, enquanto `±0,100` dá 2,952854. As duas publicações ficam ao lado, sem apagar a borda de representação.

**SK-Gd:** além de `r_m₂ = 3,605064`, o centro 9,08 está a **3,101149σ** do JUNO, usando `√(0,54²+0,078²)`. O cenário `σ ∝ T⁻¹/²` dá `σ5 = 0,389347`, 791,5985536 dias totais e **380,0785536 dias adicionais**; contado da data do arXiv, o brinquedo dá 17/10/2027. Tudo depende de a anomalia persistir contra o JUNO e de independência física ser demonstrada.

Nenhuma entrada demonstra `σ_S ≤ 0,0301`. Esse corte é suficiente para S próximo de 7,388, não necessário para S distante como 9,08.

### 7.1 MATCHED: avaliação conjunta P+S, somente brinquedo `C=0`

`C_PS=0` permite multiplicar marginais, mas não prova independência física nem fornece ramo de código. Fluxos, calibração e nuisances podem correlacionar-se.

| S | P(rP≤1) | P(rS≤1) | P(MATCHED), brinquedo C=0 |
|---|---:|---:|---:|
| JUNO 207 d | 17,430120 % | OPEN | OPEN |
| SNO+ | 17,430120 % | 4,465379 % | 0,778321 % |
| SK-Gd reator | 17,430120 % | 0,756116 % | 0,131792 % |
| KamLAND | 17,430120 % | 24,273970 % | 4,230982 % |
| **Solares sem KamLAND** | 17,430120 % | **42,157532 %** | **7,348108 %** |
| JUNO 59,1 d | 17,430120 % | OPEN | OPEN |
| NuFIT 6.1, tabela | 17,430120 % | OPEN | OPEN |
| NuFIT 6.1, artigo | 17,430120 % | OPEN | OPEN |
| Capozzi et al. | 17,430120 % | OPEN | OPEN |
| Bari 2026.a NO | 17,430120 % | OPEN | OPEN |
| SK-Gd solar+reator | 17,430120 % | OPEN | OPEN |
| SNO+ reator+solar | 17,430120 % | OPEN | OPEN |

Essas probabilidades são modelos de planejamento. `MATCHED_PROSPECTIVELY` continua permitido no texto e ausente como ramo do código; mesmo se alcançado, não significa `CONFIRMED`.

---

## 8. O que o código faz; lacunas para a gerência decidir

### 8.1 Comportamento descrito, sem executá-lo

1. Calcula `r` em m₂ e reúne determinações autônomas `≥5σ` por grupo independente.
2. Se houver pelo menos dois grupos autônomos, devolve `TGL_NU_M2_FALSIFIED`.
3. Caso contrário, se a **última linha da escada** tiver `r ≥ 3`, devolve `TGL_NU_M2_TENSION`, sem teto superior em 5. Se essa última linha estiver `≥5` sem segunda determinação, acende `tensao_global_5sigma_sem_2a_determinacao`.
4. Nos demais casos, devolve `TGL_NU_M2_ARMED_CONSISTENT`.
5. `MATCHED_PROSPECTIVELY` consta nos vereditos permitidos, mas não tem ramo. `CONFIRMED` é proibido.

Logo, `SINGLE_P` e `OPEN_RULE_GAP` não devem ser apresentados como comportamento do código; `UNDER` também não é um de seus vereditos.

### 8.2 Lacunas separadas para a gerência

- **Escada e perito:** decidir se o degrau JUNO 207,2 dias entra na escada ou fica apenas ao lado. Inseri-lo como última linha muda a leitura do código e atinge leitores existentes; uma errata textual não altera código.
- **Fonte global:** decidir como tratar a tabela exata, a eq. 11 exata e a forma simétrica arredondada do NuFIT na borda de 3σ, mantendo rota seq. 93/142.
- **MATCHED:** decidir se deve existir ramo implementado, com independência física, covariância e robustez; hoje só existe no texto.
- **Uma ou duas testemunhas:** decidir antes de qualquer nova abertura se `FALSIFIED` continua exigindo duas ou se haverá emenda de uma testemunha com limiar explícito. Este documento não escolhe.
- **Covariância:** obter matriz entre liberações e P–S, inclusive nuisances compartilhados; sem ela, o incremento por diferença não é identificável.
- **Fontes preliminares:** ratificar quais transparências oficiais contam e com quais campos mínimos; notícia secundária não abre veredito.
- **Sistemáticas e exposição:** decomposição `σstat/σsys` e conversões full-reactor permanecem `OPEN` quando não sustentadas por trecho-fonte. Nenhuma data é promovida a cronograma.

---

## 9. Reprodutibilidade e bloqueios

Arquivos desta rodada:

- `K04/M2/K09/scripts/medidas_planejamento_k09.py`: CDF em duas caudas, quadratura de conferência, cenários, diff e dados;
- `K04/M2/K09/medidas/resultados_planejamento_k09.json`: resultados completos;
- `K04/M2/K09/medidas/tabelas_planejamento_k09.md`: todas as células;
- `K04/M2/K09/medidas/mudancas_celulas_k09.md`: diff R3 → K09;
- `K04/M2/K09/medidas/incremento_1a3_anos_k09.md`: cenários do pré-registro;
- `K04/M2/K09/medidas/resumo_execucao_k09.json` e `execucao_planejamento_k09.txt`: validações e saída de planejamento;
- `K04/M2/REV2/`: R3, scripts e medidas preservados;
- `ERRATA_NEUTRINO_V412_DADOS_K09.json`: somente números e fontes;
- `PRE_REGISTRO_INCREMENTO_JUNO_RASCUNHO_K09.md`: desenho prospectivo, ainda não selado;
- `ERRATA_M2_K09.md`: correções ao lado.

**Bloqueios que permanecem:** covariância inter-liberações e P–S; independência física das testemunhas; decomposição estatística/sistemática do erro em 207,2 dias; data exata da primeira disponibilização pública da tabela NuFIT; próxima liberação e seu desenho; escolha de regra, fonte e custódia antes do selo. Nenhum bloqueio foi resolvido ajustando escala, centro, métrica ou veredito.

**Nenhum teste observado foi executado. `NOT_FALSIFIED` não é `CONFIRMED`; o gate não se move.**
