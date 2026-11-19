# REVISÃO DISTINTA DA FRENTE HUBBLE DA ENTREGA K04 (v412) — `HUBBLE_JA_EXAMINADO_K04.md`, `ERRATA_HUBBLE_K04.md`, `ERRATA_HUBBLE_K04_R2.md`, `K04\HUBBLE\`

Revisor distinto (quem constrói não aprova). 14/11/2026. Só leitura fora desta pasta; nada registrado no Mapa, nada depositado na fila, nenhuma transição ACOM, nenhum `lake`, nenhuma escrita no túnel, no kernel, no Nós nem em memória. Nenhum vetor de dado foi baixado ou lido; `executar_abertura_v411.py` não foi aberto nem rodado; `work\h0dn_bg1_v410_09nov\kimi\` não foi tocada; nada foi feito nas pastas de treino da nativa.
Estatutos: [REAL] conferido por mim com a consulta citada · [KNOWN] literatura lida por mim na fonte · [DERIVED] conta minha, por script · [DECLARADO] do Kimi, não conferido por mim · [OPEN].
`NOT_FALSIFIED` nunca é `CONFIRMED`; nada abaixo diz que a teoria foi confirmada. O gate não se mexe.

## 0. Veredito

**APROVADA COM RESSALVAS.** A conclusão central do setor (“não existe hoje teste cego de natureza executável em Hubble com poder de desenho ≥ 5σ; primeira data indeterminada”) é parede medida e está certa. Todas as contas de planejamento do Kimi reproduzem a 16 dígitos (30 linhas, diferença máxima 0,0); os valores de literatura que conferi na fonte (SN II EPM, TDCOSMO-2025, TDCOSMO-2026, masers) batem; os scripts só usam números publicados; o manifesto de hashes fecha (55/55); todos os `seq` citados existem nas rotas citadas.

O que impede aprovar sem ressalva: **a frase “a leitura de fluxo acumulado em registros intermediários está morta” está errada** (e a gerência não a pode levar assim ao operador): o Mapa tem a Fase 7, que o Kimi não leu, e a posição da própria casa de 02/10, ratificada pelo operador, diz “desfavorecida a −1,66σ e **não excluída**”. A omissão vem de a consulta ter sido feita pelo texto do veredito da Fase 4, que só devolve a Fase 4. Há mais oito rotas relevantes do Mapa que a lista não cita (§2, Q1).

## 1. O que pede correção antes de seguir ao operador

1. **[ALTA] “morta” não vale; nem “nenhuma forma intermediária viva”.**
   Onde: `HUBBLE_JA_EXAMINADO_K04.md:8`, `:57` (“Portanto, não há forma intermediária nova lícita a pré-registrar”), `:199` (“nenhuma forma intermediária viva”); `ENTREGA_K04.md:19` (“está **morta**”).
   Por quê [REAL, `rotas.py ver`]: (a) o veredito da Fase 4 já traz `DIAGONAL_ERRORS_ONLY`, e o relatório diz que a significância “está sobrestimada por fator não medido” (`RELATORIO_FASE4_DESVIO_20260930.md:36`) e que “‘PERDEU’ é mais forte do que o veredito” (`:48`). (b) Esse fator foi medido na rota `d1.fase7_cc_covariancia_01out` (seq 247, 257, 258): ganho da lei acumulada nos cronômetros **−3,22σ (diagonal) → −1,66σ (covariância Moresco 2020) → −1,54σ (todos)**; ln B(sombra/acumulada) +5,35 → +1,62 → +1,46; veredito `Q1_TENSION_1_TO_3_SIGMA_WEAKENS`. (c) A reprodução do seq 410 reproduz só a versão diagonal (“Planck comprimido + DR2 + CC32 diagonal”). (d) A casa registrou em 02/10, depois da ratificação do operador de R1–R6 com a correção “a TGL é ótica” (`work\v381_perguntas\PERGUNTAS_QUE_FALTAM_QUATRO_LINGUAS_20261002.md:102–109`, sha16 do arquivo `3ce9816788e42f41`): “na Fase 7 a lei acumulada, uma candidata à leitura da face, ficou desfavorecida a −1,66σ e **não excluída**”, e (`:119`) a “lei do lado transmitido, 1 − β por travessia” para os cronômetros fica **PENDENTE** (a escrever e pré-registrar, “com o poder dito antes de abrir”), com poder prévio de 2,33σ; rota `bancada.preregistro_dois_lados_delta_k` (seq 282, 291; `proximo_passo`: “depois os pendentes (a lei transmitida nos cronômetros…)”).
   Texto que a evidência sustenta: “desfavorecida a 3,2σ sob erros diagonais (Fase 4) e a 1,5–1,7σ com a covariância de Moresco 2020 (Fase 7); não excluída; a lei da face para os cronômetros está pendente de escrita, com poder prévio de 2,33σ; logo não é um teste de 5σ”. O resultado do topo (“não há ≥ 5σ”) não muda; fica mais forte. O que muda é o que o operador ouve: “morta” soa como falsificação de um ramo; o Mapa diz tensão enfraquecida, não excluída.
2. **[MÉDIA] A lista do Mapa omite rotas relevantes** (§2, Q1 tem a tabela): `d1.fase7_cc_covariancia_01out`, `bancada.preregistro_dois_lados_delta_k`, `um_py.v380.fases_5_6_7_por_hash`, `discriminante.lentes_5sigma_20261019`, `discriminante.ordem018.r_h_sirenes`, `d1.fase9.auditoria_suficiencia_20261019`, `d1.fase9.integracao_20261019`, `estatistica.h0dn_bg1.cov_injecoes_06nov`, `natureza.5sigma_fora_da_cosmologia_poder_27out`. Causa verificável: a consulta `Fase 9` (com espaço) devolveu 26 rotas (`consultas/mapa_Fase9.txt`); o termo único `fase9` devolve 46; `mapa_fluxo_intermediario.txt` (termo = a string do veredito) devolveu 1.
3. **[MÉDIA] A frase sobre as lentes cita só a R-G; falta a R16.** `HUBBLE_JA_EXAMINADO_K04.md:32` e `ENTREGA_K04.md:19` (“lentes de um passo são outro caso, com ponte física aberta”). Classificação honesta (§2, Q2), mas incompleta: a rota `discriminante.lentes_5sigma_20261019` (16 registros, seq 1225–1245, EM_CURSO) diz que “K escalar não fixa f_t, F_D, f_phi”, que as ramificações limitadas são `NO_OBSERVED_5SIGMA__BOUNDED_BRANCHES_UNPROMISING` (seq 1226), e fecha com `G_MATCHING_DERIVED__NO_LENS_NUMERIC_SIGMA`, defeito “calibração externa independente ou fonte não proporcional ainda OPEN”, `nao_refazer`: “não promover forecasts antigos”. O D de TDCOSMO (2,46–2,69; 5,36 e 6,56 nas previsões) é o da leitura `K·H_fundo` (R-G alternativa A, seq 1637), condicional; dizer isso ao lado do número.
4. **[MÉDIA] O D da H0DN (7,068/8,068) não é o D da casa para a mesma linha.** `HUBBLE_JA_EXAMINADO_K04.md:7, :87, :88, :131`; `ENTREGA_K04.md:5`. O core (`h0dn_bg1_v411.values.primario.D`) traz **6,710** (modelo de erros publicado) e, para as Cefeidas livres, **5,191** (`values.cefeidas_livres.D`). O Kimi usa o σ do cabeçalho (0,81/73,50 = 1,102 %): é aproximação de bolso e deve ser dita assim, ou dar o D da casa ao lado. Sem isso o operador ouvirá 7,07 e 6,71 para a mesma linha.
   Junto: o D = 3,256 do SN II EPM é **teto só-estatístico** (a fonte diz que a sistemática é “comparável ou menor” que a estatística: com sistemática = estatística o D cai a **2,32** [DERIVED]) e a própria tabela diz que essa linha já entrou na variante astrofísica da H0DN; chamá-la “linha independente qualificada” (`:149`; `ENTREGA_K04.md:5`) é generoso.
5. **[MÉDIA] Premissa não dita nas linhas sem rota.** O D de SN II, FRB, SZ/raios X, BBH–AGN e SN Encore supõe que elas leem `K·H_fundo`. O Mapa tem essa leitura para lentes (R-G) e sirenes (R-H, `defeito`: “Hsirene=K Hbg é extensão condicional, não derivação de propagação GW”, seq 1638); para as demais não há rota (`consultar SNII`, `FRB`, `SZ`, `EPM`: 0 rotas). Dizer: “D sob a hipótese de que lê K·H_fundo; sem ponte examinada”.
6. **[MÉDIA] A pergunta “e juntas?” vai vir, e o documento só responde linha a linha.** “Nenhuma determinação independente cruza hoje 5σ” (`:123`) vale por linha. Aritmética de planejamento minha sobre σ publicados [DERIVED, `extras_k04.py`]: SN II (stat) + TDCOSMO-2026 → D = 4,04 (3,36 com SN II sistemática = estatística); cinco linhas (SN II, TDCOSMO-2026, reanálise MCP, FRB localizados, BBH–AGN estendido; três só-stat) → D = 5,34 (4,88 com SN II sistemática = estatística). Não é composto aberto, não é teste, e a independência não está demonstrada (MCP entra na H0DN; `f_IGM` do FRB; calibrações do BBH–AGN); mas mostra que a conclusão “nenhuma chega” depende de olhar linha a linha, e que um empilhamento previsível por agregados (portanto não cego) fica na vizinhança de 5. Para a lente sozinha: de 11 para ~48 lentes equivalentes dá 5σ e ~79 dá D90 (escala 1/√N, só estatística) [DERIVED].
7. **[BAIXA] Citações de kernel.** (a) `ThermodynamicFriedmann.lean:124–135` (`HUBBLE_JA_EXAMINADO_K04.md:47, :185`) é o teorema `variable_factor_first_equation_defect` (defeito de Friedmann ao trocar a primitiva por Φρ); não diz nada da lei de extremos (apoia a errata do Pantheon, seq 149). (b) A afirmação “K é razão de extremos” está em `TGLExt/TheFlowLawContrast.lean:26–27` e `:153–170` (`the_derived_kernel_factor`: `K = (E(N)/E(0))^{2β/3}`, para qualquer N ≠ 0), que o Kimi não cita; as linhas de `TheFlowLawD1a.lean` que ele cita (33–46, 53–64) existem e dizem o que a frase diz (a forma geral para z genérico). (c) `:47` diz “53–62”; `:53` e `:185` dizem “53–64” (53–64 é o certo).
8. **[MÉDIA/BAIXA] Atribuição ao operador que não fecha por bytes** (§3): `HUBBLE_JA_EXAMINADO_K04.md:40`, linha 22.
9. **[BAIXA] Pendências da REVISAO_K01 não respondidas aqui:** §6.5 (a próxima liberação do fundo, DESI DR3, entra como fundo ou como nova testemunha?) não aparece nos arquivos de Hubble; e todas as linhas candidatas ficam “sem data”, o que é honesto, mas deixa a pergunta “com que data?” sem número. Item menor: a linha 5 da tabela (`HUBBLE_JA_EXAMINADO_K04.md:23`) cita “203–214”; a rota `d1.fase3_leitores_h0` não tem o seq 213 (tem 203–212, 214, 221).

## 2. Respostas às seis perguntas

### Q1. A lista do que o setor de Hubble já teve examinado

**Conferi 22 de 22 linhas** (a ordem pedia no mínimo 12). Método [REAL]: `rotas.py ver` de cada `rota_id` citado (`scripts_k04_hubble\confere_seq.py`): **todos os `seq` citados pertencem às rotas citadas**, exceto o 213 da linha 5 (uma bobagem de intervalo) e os casos em que a linha cita duas rotas e os `seq` se repartem entre elas (linhas 15, 16, 17, 21, 22; a união fecha). Conferi também o conteúdo de onze linhas contra o texto do registro: 1 (seq 34, 149: Pantheon 1593, tensão antiga 3,8σ, errata), 7 (seq 229, 231, 410), 9 (seq 236–242, 388, 407; `lnB 0,29`, validação z = 0,04), 11 (seq 376, 389, 394: D = 0,183211 / 0,030213 / 0,163963), 12 (seq 1635), 13 (seq 378, 1636), 14 (seq 379, 391, 393, 1637), 15–16 (seq 373, 604: −1,4σ, +4,5σ, ln B +9,4, poder prévio 5,91σ), 20 (seq 1354: `z_disc 4,443 < 5`, “não reabrir”), 22 (seq 1639–1654). Dizem o que o Kimi diz. As decisivas pedidas (`d1.fase4_desvio_30set` seq 229/231 e 410; R-E, R-F, R-G; Fases 1 a 5; Fase 9) estão todas.

**Falta rota relevante: sim, nove** [REAL; `consulta_mapa_saida.txt`, `cobertura_rotas.py`]:

| rota | status | registros | o que traz | por que importa |
|---|---|---|---|---|
| `d1.fase7_cc_covariancia_01out` | EXAMINADA | 247, 257, 258 | cronômetros com covariância: −3,22 → −1,66σ | derruba o “morta” (item 1) |
| `bancada.preregistro_dois_lados_delta_k` | EM_CURSO | 275–303 | livro de cobranças dos dois lados; “lei transmitida nos cronômetros” PENDENTE; F1 com poder prévio 2,33σ | idem |
| `um_py.v380.fases_5_6_7_por_hash` | EXAMINADA | 262–264 | a Fase 7 entra no core por hash | idem |
| `discriminante.lentes_5sigma_20261019` | EM_CURSO | 1225–1245 | lentes R1–R16; sem σ numérico de lente | item 3 |
| `discriminante.ordem018.r_h_sirenes` | EXAMINADA | 401, 1638 | sirenes leem K·H_fundo = 74,27; 5σ pede σ(H0) = 1,15, hoje ~11 | a linha das sirenes ficou sem a rota própria |
| `d1.fase9.auditoria_suficiencia_20261019` | EXAMINADA_COM_DEFEITO | 1247 | primário BG1 D = 5,721–6,623; **sem Cefeidas D = 3,938–4,395** | número da casa para a linha “sem Cefeidas” (ressalvas 3, 4) |
| `d1.fase9.integracao_20261019` | EXAMINADA_COM_DEFEITO | 1248–1257 | K comum, cobertura, atos pendentes | contexto da Fase 9 |
| `estatistica.h0dn_bg1.cov_injecoes_06nov` | EXAMINADA_COM_DEFEITO | 1 | matriz publicada e injeções cegas | ressalva 5 |
| `natureza.5sigma_fora_da_cosmologia_poder_27out` | EXAMINADA | 1479–1482 | devolução anterior do próprio Kimi (ORDEM 5σ-01) conferida: “nenhuma rota nova com gap ≤ 1” | o “agora” já tinha sido esgotado em outubro |

Ao contrário: as linhas “novas” que o Kimi diz nunca terem sido compostas pela casa (SN II, FRB, SZ/raios X, EPM, BBH–AGN, SN Encore) realmente não existem no Mapa (`consultar SNII`, `SN II`, `FRB`, `SZ`, `EPM` → 0 rotas; `BBH` → 1, a do eco). Nesse ponto o Kimi está certo. (Os centros de masers, TDCOSMO-2025 e sirenes, porém, a casa já os leu contra `K·H_fundo` em 02/11: `DERIVACAO_RE_02nov.md:42–50`, “−0,12σ / −0,74σ / +0,21σ”, [DECLARADO, valores da Fase 9]. É mais uma razão de não serem cegos.)

### Q2. “Morta”, lei de extremos, lentes

- **“A leitura de fluxo acumulado em registros intermediários está morta”: não** (item 1). Está **examinada, desfavorecida e não excluída**; o único teste que a mata acima de 3σ é o de erros diagonais, que a própria casa corrigiu (Fase 7).
- **A lei `K = E(z*)^{2β/3}` é enunciado de extremos?** Sim, e o arquivo diz isso, mas não o que o Kimi cita [REAL, lido]: `TheFlowLawContrast.lean:153–158` (`the_derived_kernel_factor`): `H0localContrast β Hcmb (frwContrast E) N = Hcmb·(E N / E 0)^{(2/3)β}`, para qualquer N ≠ 0, razão das taxas nos dois extremos do registro (`:26–27`); com `E 0 = 1`, `K = E(N)^{2β/3}` (`:165–170`); a Bancada o computa em `z*` (`E(z*) = 22784,337392…`, reproduzi: `K = 1,0838071748529643` idêntico ao core, `β = ALPHA_FINE_CODATA_2018·√e = 0,012031300400803142` em runtime). O relatório da Fase 4, linha 5, diz “dois registros: a escada (registro inteiro) e os 32 cronômetros (registros intermediários, lidos com a lei acumulada de z* até z)”: confere (`:5`, `:36`, `:39`, `:48` conferidos linha a linha). `TheFlowLawD1a.lean:33–46, 53–64` definem e provam `H0local = Hcmb·(1+z)^β` para z genérico: a forma geral existe, como o Kimi diz. O que a frase “não há canal intermediário de zero parâmetro” deixa de dizer é que a leitura intermediária de zero parâmetro **existe** (é a família T da Fase 4) e foi lida duas vezes (Fases 4 e 7).
- **`DERIVACAO_RE_02nov.md:8–10, 67–72`** existem e dizem o que o Kimi diz (K não age em L nem em A; η = 1; o rival também dá 1; R-F alternativa A; R-G lentes leem K·H₀; R-H sirenes 5σ pede σ(H0) = 1,15). Atlas `:9556` (D1a) e `:9558` (D1b/Fase 4) existem e são as entradas certas.
- **“Lentes de um passo são outro caso, com ponte física aberta”: classificação honesta, não porta sem base.** A ponte está aberta no Mapa (R-G seq 393: “ponte física K→distâncias/tempo/potencial permanece OPEN”; R16 seq 1245: “calibração externa independente ou fonte não proporcional ainda OPEN”), e as ramificações examinadas são “sem 5σ, pouco promissoras” (seq 1226). O defeito é de completude (item 3): citar R16 e dizer que o D de lente é condicional à alternativa A.

### Q3. Os números, recomputados

Script próprio `contas_k04_hubble.py` (β em runtime; `E(z*)` recomputado de `Ω_m`, `Ω_r`, `z*` do core, sem tocar nos insumos; saída `contas_k04_hubble_saida.txt`) [DERIVED]:

| grandeza | Kimi | revisor |
|---|---|---|
| K − 1 | 0,0838071748529643 | 0,0838071748529643 (idêntico; E(z*) idêntico ao core) |
| D90 | 6,281551565544601 | 6,281551565544601 |
| σ_BG1 relativo | 0,438 % | 0,4377645 % |
| σ_local máximo para 5σ / D90 | 1,618 % / 1,260 % | 1,61797 % / 1,26032 % |
| σ_total máximo para D90 | 1,334 % | 1,33418 % |
| D H0DN baseline / V99 | 7,068 / 8,068 | 7,0675 / 8,0683 |
| D SN II tailored EPM (só stat) | 3,256 | 3,2556 (com sistemática = estatística: 2,319) |
| D TDCOSMO-2026 / +SLACS+SL2S | 2,462 / 2,689 | 2,4622 / 2,6892 |
| D SH0ES JWST (falta a D90) | 6,259 (0,022) | 6,2587 (0,0229) |
| as 30 linhas (26 medidas + 4 previsões) | | **diferença máxima 0,0** |

Reproduz tudo, dado o insumo e a fórmula. Observação de conceito, não de conta (item 4): o D da casa para a H0DN no core é 6,710 (primário) e 5,191 (Cefeidas livres); o 7,068 vem do σ do cabeçalho. Os σ compostos em quadratura (CCHP 1,936; SBF 2,404; de Jaeger 4,085; BBH–AGN 3,714 e 2,979) conferem.

### Q4. Literatura `[KNOWN, a conferir]` (6 consultas web em 14/11/2026)

| fonte | achado | resultado |
|---|---|---|
| arXiv:2411.04968 (Vogl et al.) | “No rungs attached”; H0 = 74,9 ± 1,9 (stat) km/s/Mpc; a sistemática “comparável ou menor” que a estatística, sem número; A&A 702, A41, DOI 10.1051/0004-6361/202452910; v1 em 07/11/2024 | **confere** (valor, σ, arXiv, DOI); D = 3,256 é teto só-stat |
| arXiv:2610.14781 (TDCOSMO 2026) | resumo: 71,1 +2,4/−2,3 (3,3 %), 11 lentes, 3,0 % com SLACS+SL2S; corpo (offset 100000): **71,3 +2,2/−2,1** “at 3.0% precision”; 8 das 11 já estavam na amostra de 2025, 3 novas; v2 de 29/10/2026 | **confere** (valor, σ, 8+3 lentes). O resumo não traz o 71,3; está no corpo |
| arXiv:2506.03023 (TDCOSMO 2025) | 71,6 +3,9/−3,3, 8 lentes, v1 03/06/2025, v4 21/12/2025 | **confere** (a Fase 9 usou ±3,6, a média dos lados; o Kimi usa o lado maior, 3,9: escolha dita) |
| arXiv:2001.09213 (MCP XIII) | 73,9 ± 3,0, seis galáxias, v1 24/01/2020, ApJL | **confere** |

**Não fechou** (fora do orçamento de 6): a previsão de 1,5 % (JWST-GO-7184/9637, “arXiv:2610.14881v2, §V”): a leitura do corpo de 2610.14781 não a traz, e o 2610.14881 não foi aberto; a previsão de 1,2 % (arXiv:2008.06157); V99 da H0DN (73,994 ± 0,697; “a fonte recomenda não usar”); SH0ES JWST 73,49 ± 0,93 e +TRGB 73,18 ± 0,88 (2509.01667); CCHP (2408.06153); SBF (2502.15935); reanálise MCP (2609.17684); de Jaeger (2203.08974); GWTC-4.0/5.0; BBH–AGN (2607.03672); SN Encore (2509.12301); SZ (2310.18711); FRBs (2410.03994, 2604.03769, DOI Frontiers 2026); GO-5989. Seguem `[DECLARADO]`.

### Q5. A resposta do topo, o argumento e a independência

- **O argumento (“composto de dado público que a casa nunca compôs e não previsível por agregados”) está completo para o que afirma**: todo composto de agregados públicos é previsível por aritmética dos agregados (ainda mais quando a própria casa já leu três deles contra K em 02/11); só dado novo ainda não publicado muda isso, e a primeira data é indeterminada. Canais de um passo que ficaram de fora, **de memória minha e sem conferência** [KNOWN, a conferir]: supernovas lenteadas (SN Refsdal, SN H0pe), reverberação de quasares/paralaxe de poeira do BLR, SBF/Mira (não são de um passo). Todos de precisão ≥ 5 %: não mudam a conclusão. A parede é, nas três pernas, medida (cegueira por construção; poder por linha; independência), não falsificação.
- **Linha de independência para as ressalvas 3, 4, 5, 7, com número:**
  - **TDCOSMO-2026 (+SLACS+SL2S)**: D = 2,462 (2,689); 11 lentes, sem escada nem Cefeidas; **parcial** em R7 (8 das 11 já estavam no leitor TDCOSMO da Fase 9: conferi na fonte); para 5σ precisa de ~48 lentes equivalentes, para D90 ~79. Serve como linha de consistência (R3), não como teste.
  - **SN II EPM**: D = 3,256 só-stat (2,32 com sistemática = estatística); já na variante astrofísica da H0DN (R7: não é virgem).
  - A linha “sem Cefeidas” que a casa já tem: D = 3,938–4,395 (`d1.fase9.auditoria_suficiencia_20261019`, seq 1247), não citada.
  - Nenhuma tem covariância/pacote completo; logo nenhuma resolve as 72 direções de variância zero (R5) nem a contagem de tentativas (R7). O resumo do Kimi (“TDCOSMO-2026 é a mais informativa”) está correto.
  - Empilhamento: item 6.

### Q6. Nada foi aberto?

**Sim, confirmo que nada foi aberto** [REAL]. `extrair_rotas.py`, `medidas_planejamento.py` e `verificar_relatorio.py` importam só `json`, `math`, `pathlib`, `ast`, `hashlib`, `re`: sem numpy, sem rede, sem `subprocess`. `Grep` por `np.load|read_csv|loadtxt|astropy|fits|npy|requests|urllib|subprocess|lake|um_absoluto|h0dn_bg1` nos três scripts: zero ocorrências. `medidas_planejamento.py` tem os números digitados (H0, σ) e a fórmula; `extrair_rotas.py` só relê os JSON do Mapa; `verificar_relatorio.py` só confere texto e grava o manifesto. `executar_abertura_v411` aparece somente em `ENTREGA_K04.md` (“nunca foi chamado”), em nenhum arquivo de `K04\HUBBLE`. `fonte_FRB_2026.html` (1,8 MB) é uma página de artigo salva, não vetor. Manifesto `SHA256SUMS_K04_HUBBLE.json`: 55 entradas, 55 conferem (bytes e sha256), 0 arquivos em disco fora dele (`confere_manifesto.py`). Relatório `37fee18ca729cfc7`, errata `246adaf85a782869`, errata R2 `cdcebe62b4e4a2dc` (sha16 lidos por script).

## 3. Tarefa fixa: atribuições ao operador

Percorri os quatro arquivos (`HUBBLE_JA_EXAMINADO_K04.md`, as duas erratas, `ENTREGA_K04.md`). Só uma frase do setor Hubble atribui algo ao operador:

- **`HUBBLE_JA_EXAMINADO_K04.md:40` (linha 22): “a sexta fechada pela leitura ratificada: K sem portador derivado; transposição FFAT bloqueada pela R1, não reabrir sem mudança do operador”. Não fecha por bytes.**
  - Não cita arquivo verbatim. A fonte é a rota do Mapa: seq 1646 (“Ratificado pelo operador: a perda é de coerência; a sexta morada fecha… Fala sha16 1c05c03070544839, ‘E isso mesmo’”) e seq 1654 (“bloqueada pela R1 ratificada em 02/10”).
  - Bytes do sha16 `1c05c030…` (`work\cunhagens_13out\OPERADOR_02nov_K_faz_a_funcao_do_graviton_operador_igual_que_criva_verbatim.txt`, 142 B): «É isso mesmo, mas agora o K me pareceu fazer a função do próprio gráviton ( que antes eu disse ser o operador “=“, aquele que criva)». O “isso” não se identifica pelos bytes (responde a uma leitura da gerência que não está no arquivo), a segunda metade acrescenta outra coisa, e “a sexta morada fecha” não está em palavra alguma dele. O seq 1644 diz “sujeita a confirmação”. O arquivo `…vazar_e_luzir_registro_leitura_do_foton_pelo_graviton…` (656 B) diz «Há sim uma perda, mas ela não afeta a idade preservada», o que apoia “a perda é da forma”, não “a sexta fecha”. A própria `DERIVACAO_RE_02nov.md:10, :58` diz que a sexta “segue aberta, sem mecanismo”.
  - R1: a ratificação é **em bloco** («Concordo com tudo, exceto com a sua visão semiótica, a TGL não é semi ela é ótica…», 02/10), citada em `PERGUNTAS_QUE_FALTAM…:102` e em `MEMORY_2.md` (R1–R6 ratificadas), **sem arquivo verbatim em `cunhagens_13out`** (busquei por texto e por nome: nada). Concordância em bloco não escolhe alternativa; “bloqueada pela R1” é inferência da gerência (seq 1654: “A gerência propôs a porta sem ler a R1”).
  - Correção sugerida: escrever “o Mapa registra (seq 1646, 1654) que a gerência leu a resposta do operador de 02/11 como fechamento da sexta morada e a R1 de 02/10 como bloqueio da transposição FFAT; os bytes do 02/11 são os dois arquivos citados; a R1 não tem verbatim em arquivo”.
- `ENTREGA_K04.md:14` (“Atos do operador: decidir…”) é pedido futuro, não atribuição; `:35` (“o par F2b foi retirado”) é do ringdown, fora do escopo Hubble desta revisão.

## 4. O que conferi e como

- Mapa de Rotas, só consulta [REAL]: **termos consultados** `D1B`, `Pantheon`, `masers`, `TDCOSMO`, `lentes`, `sirenes`, `FRB`, `SNII`, `SN II`, `H0DN`, `fase9`, `Hubble`, `Cefeidas`, `SH0ES`, `TRGB`, `CCHP`, `SBF`, `JAGB`, `FFAT`, `R-E`, `R-F`, `R-G`, `intermedi`, `Fase 4`, `Fase 5`, `BBH`, `AGN`, `SZ`, `EPM`, `megamaser`, `H0`, `razao de Hubble`, `K = E`, `forma Q`, `cobrancas`, `livro`, `cronometros` (`scripts_k04_hubble\consultar_mapa.py`, saída em `consulta_mapa_saida.txt`).
  **Rotas lidas com `ver`**: as 22 linhas (`supernovas.pantheon_errata_cosmologica`, `d1.camb.v3_real`, `d1.fase1_eff_30set`, `d1.fase2_dois_setores_30set`, `d1.fase3_leitores_h0`, `d1.fase3bis_d1b_convencao_artigo`, `d1.fase4_desvio_30set`, `um_py.v378.o_que_faltou_contraste_fase4`, `d1.fase5_sh0es_01out`, `discriminante.ordem018.f1b.fase45_conjunta`, `discriminante.ordem018.f2.r_d/r_e/r_f/r_g`, `hubble.fase9_razao_discriminante`, `d1.fase9.razao_de_hubble.lentes_05out/v1_06out`, `d1.fase9.f3_auditoria_cetica_c1_07out`, `d1.fase9.f3_1_reauditoria_v2r2_c1_08out`, `d1.fase9.f3_1_semantica_v1x_leitores`, `d1.fase9.v2_c1_a_unica_palavra_23out`, `estatistica.h0dn_bg1.ordem_kimi_y_obs_09nov`, `umpy.v411.selada_h0dn_aberto_12nov`, `hubble.k_sem_portador_fisico_02nov`, `hubble.k_como_transposicao_inteira_ffat_02nov`) e as omitidas (`d1.fase7_cc_covariancia_01out`, `bancada.preregistro_dois_lados_delta_k`, `um_py.v380.fases_5_6_7_por_hash`, `discriminante.lentes_5sigma_20261019`, `discriminante.ordem018.r_h_sirenes`, `d1.fase9.integracao_20261019`, `d1.fase9.auditoria_suficiencia_20261019`, `natureza.5sigma_fora_da_cosmologia_poder_27out`, `conceitual.k_e_a_tangente_acorde_tocado_02nov`).
- Kernel e relatórios, linha a linha: `TheFlowLawD1a.lean:30–66`; `TheFlowLawContrast.lean:24–29, 150–172`; `ThermodynamicFriedmann.lean:118–138`; `RELATORIO_FASE4_DESVIO_20260930.md:1–48` (cópia em `…\A Ponte e o Um\cache\bancada_30set\`); `DERIVACAO_RE_02nov.md:1–14, 40–76`; `TGL_ATLAS.md:9554–9559`.
- Core `um_absoluto.json` → `core.h0dn_bg1_v411` (`values.K`, `E_zstar`, `Omega_m`, `Omega_r`, `z_star`, `lei_em_km_s_Mpc`, `primario`, `cefeidas_livres`, `esperado_pelos_agregados`, `ressalvas_secao8`), só leitura.
- Verbatim por bytes (`acha_verbatim.py`): sha16 `1c05c03070544839` e `3a52cc836c5e87a9` em `cunhagens_13out`; arquivos `OPERADOR_02nov_*` lidos.
- Web: arXiv 2411.04968, 2610.14781 (resumo e corpo), 2506.03023, 2001.09213.

## 5. O que NÃO conferi

- Os valores de literatura listados em Q4 como “não fechou”.
- O corpo do relatório da Fase 9 V2 e do V1 (conferi os registros do Mapa, não os arquivos de resultado); o conteúdo dos `K04/HUBBLE/consultas/ver_*.txt` além da comparação com o `ver` vivo; os `D` que a casa obteria com a covariância completa para cada linha.
- Se o índice do acervo realmente devolve zero para as rotas exatas (`indice_rotas_exatas.txt`, 84 B): prova fraca de ausência, que o próprio Kimi declara.
- Não calculei z observado nenhum das linhas independentes contra K: seria leitura não cega de dado público, decisão do operador, e não era o escopo.
- Não revisei as outras frentes da K04 (m₂, combinação, ressalvas, errata do core): outras revisões.
- Procedimento ACOM/memória: não executei (por ordem).

## 6. O que a gerência diz ao operador (partitura, na língua dele)

“No setor de Hubble, o que existe hoje de medidas independentes já é público, e a casa já leu parte delas; por isso não há teste cego possível agora. É parede medida, não falsificação. O que cada linha sozinha poderia separar da ΛCDM: nenhuma chega a 5σ; a melhor, em desenho, é a mesma H0DN (6,7 pelo modelo de erros da casa; o 7,07 do Kimi é conta de bolso), e as independentes ficam entre 2,3 e 3,3σ de desenho; juntas, em conta de bolso e sem independência demonstrada, ficam perto de 4 a 5. A leitura por registros intermediários não está morta: ficou fraca (1,5–1,7σ com a covariância correta) e a lei que a leria do lado da face está pendente de escrita. O que mais mudaria isso é dado novo (lentes com atraso: de 11 para ~50 a ~80 lentes), sem data publicada.” A ressalva é minha: este parágrafo é proposta; depende de a gerência corrigir o item 1.

## 7. Scripts e saídas (pasta `scripts_k04_hubble\`)

`consultar_mapa.py` (+ `consulta_mapa.json`, `consulta_mapa_saida.txt`), `ver_rotas.py`, `dump_regs.py`, `grep_seq.py`, `confere_seq.py` (+ `confere_seq_saida.txt`), `cobertura_rotas.py`, `contas_k04_hubble.py` (+ `contas_k04_hubble_saida.txt`), `extras_k04.py` (+ `extras_k04_saida.txt`), `confere_manifesto.py`, `acha_verbatim.py`, `core_h0dn.py`, `core_h0dn2.py`; subpasta `ver\` com a saída bruta de `rotas.py ver` de cada rota lida.

`NOT_FALSIFIED` não é `CONFIRMED`; o gate não se move; esta revisão não credita nem descredita a teoria.
