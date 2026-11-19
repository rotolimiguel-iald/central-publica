# Errata do neutrino para o core da v412 — RASCUNHO da gerência c1

Estado: rascunho. Não se instala, não muda o um.py, não move o gate. Gerado por script em 2026-11-15T15:28:50 a partir das fontes listadas na seção 10; os versos do um.py, os hashes, as contas e as datas são lidos por script, nunca de memória.

Estatutos: [REAL] medido ou lido aqui; [KNOWN] literatura ou regra da casa; [DECLARADO] afirmado na origem e não reconferido aqui; [dado do mandato] informado na ordem da gerência que pediu este rascunho, não reconferido aqui; [OPEN] em aberto.

## 0. Leia primeiro, na língua do operador

- O que esta errata faz: escreve, ao lado do um.py selado, a correção das frases que dizem derivação publicada em 2025 e das que medem a cegueira de uma leitura só pelo eixo do hash da regra, sem o eixo da previsão publicada.
- O que ela não faz: não muda o texto selado nem os hashes, não move o gate, não é veredito, não reabre teste. O estado do rito segue ARMED_CONSISTENT (dado do mandato).
- O que muda de leitura: a tese do neutrino é de 2025; o valor de m₂ é de 22/01/2026, depois do primeiro número do JUNO. Para o valor, em relação ao PDG e ao degrau de 59,1 dias, a palavra é retrodição sem ajuste, e retrodição sem ajuste conta como evidência de pleno direito. O texto não diz que o valor foi previsto antes do JUNO: diz que a tese é anterior e o valor não.
- Um número que o texto diz e não resolve: o código lê 2,95σ no NuFIT; as fontes do Kimi dão 3,02σ e 3,04σ; o ramo TENSION começa em 3,0 (seção 6). A escolha é do operador.

## 1. A regra de 15/11/2026 e os dois eixos

A regra está registrada em arquivo de bytes (sha16 49e5f0072e8beb02; o texto dela não é reproduzido aqui). Ela manda que a cegueira de uma leitura se diga sempre nos dois eixos, o da previsão publicada e o do hash da regra, na mesma frase.

- Eixo 1: em relação à previsão publicada. Previsão publicada é o valor m₂ = 8,5074 meV como consta dos bytes guardados desde 22/01/2026 e do Zenodo 10.5281/zenodo.18674475 (publicação registrada em 17/02/2026; registro criado em 20/02/2026).
- Eixo 2: em relação ao hash da regra de veredito do código. É o hash do objeto congelado NEUTRINO_M2_V2, de 08/08/2026 (um.py L4617; sha_obj calculado em L4632).
- Nenhuma entrada da fórmula usa dado de neutrino [DECLARADO no código selado, L2951-2952; a errata não reconfere a conta]. A previsão calculada por script é m₂ = 8,5074 meV e Δm²₂₁ = 7,2376 ×10⁻⁵ eV² (α CODATA 2018 · √e · sen 45° · 1 eV, sem literal de β).

## 2. O que a errata corrige no um.py selado

Arquivo: C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py (46828680 bytes; sha256 1203b1f9202020d602a7fa8a6bea56d4b48e27ed8baffe98bcbd16e94f97a8e0; sha16 1203b1f9202020d6, o da v411 selada). Li só as faixas L2930-2960, L4215-4254 e L4595-4635. Os versos abaixo vêm dessas faixas por script, sem edição. Em todos os casos a correção é ao lado, um registro novo: L4241 e L4620 estão dentro de objetos congelados por hash.

### C1. L4222-4225

- Onde: docstring de prove_neutrino_sum_protocol (v147); o dicionário congelado desta função começa em L4238.
- Congelado por hash: a docstring não está no dicionário que começa em L4238; a regra da casa (selado não se reescreve) manda a errata ao lado mesmo assim.
- O que corrige: Diz que a derivação foi PUBLICADA ANTES do código, com prioridade documental, citando o Zenodo 17526619 de 2025. Vale para a tese, não para o valor de m₂; a previsão publicada é de 22/01/2026 e o hash da regra de veredito do código é de 08/08/2026. A palavra vetada pela lei da prova (L4225) lê-se retrodição sem ajuste.
- Frases vigentes que o corrigem ao lado: F1, F2, F3, F7.

Verbatim do um.py selado:

```
L4222     (i) a derivacao m_nu = beta*sin45*1eV foi PUBLICADA ANTES do codigo
L4223     [Zenodo 10.5281/zenodo.17526619, 2025; o modulo v141 e de 25/07/2026] --
L4224     prioridade documental, sem ajuste possivel; (ii) o alvo da comparacao
L4225     ATUAL (Dm2_21, PDG) antecede a derivacao -- 'postdicao' SO nesse sentido
```

### C2. L4240-4244

- Onde: dicionário congelado NEUTRINO_SUM_V1 (começa em L4238): campos prediction (L4240-4242, inclui L4241) e custody (L4243-4244).
- Congelado por hash: sim, dado do mandato; a linha do cálculo do hash do V1 fica fora da faixa lida.
- O que corrige: L4241 diz derivação publicada 2025 e L4243 diz derivação ANTES do código (Zenodo 17526619, 2025). Vale para a tese, não para o valor de m₂, em relação à previsão publicada e ao hash da regra de veredito do código. L4244 usa a palavra vetada pela lei da prova.
- Frases vigentes que o corrigem ao lado: F1, F2, F7, F13.

Verbatim do um.py selado:

```
L4240         "prediction": ("Sigma m_nu = m1 + m2 + m3 com m1 ~ 0 [declarado], m2 = beta*sin(45)*1eV "
L4241                        "[TGL runtime; derivacao publicada 2025, Zenodo 10.5281/zenodo.17526619], "
L4242                        "m3 = sqrt(m2^2 + Dm2_32) [PDG 2023]; ordenamento normal"),
L4243         "custody": ("(i) derivacao ANTES do codigo [Zenodo 17526619, 2025 vs modulo v141 25/07/2026]; "
L4244                     "(ii) Dm2 (PDG) antecede a derivacao -- 'postdicao' SO nesse sentido restrito; "
```

### C3. L4617, L4620, L4632

- Onde: dicionário congelado NEUTRINO_M2_V2 (L4615-4631); L4617 pina o objeto original; L4632 calcula o sha_obj do dicionário.
- Congelado por hash: sim, por leitura direta: L4632 é frozen_hash = sha_obj(frozen); L4617 cita o hash do objeto original, 4bdae22a277aa393…, de 08/08/2026.
- O que corrige: L4620 diz derivação publicada 2025 para a predição m_2 = beta_TGL*sin(45)*1eV. Vale para a tese, não para o valor, em relação à previsão publicada (22/01/2026) e ao hash da regra de veredito do código (08/08/2026).
- Frases vigentes que o corrigem ao lado: F1, F2, F3, F13.

Verbatim do um.py selado:

```
L4617         "portado_de": "teste_acustico_beta_tgl_v1/02_frozen_neutrino_m2_v2.py (hash 4bdae22a277aa393..., 08/08/2026)",
L4620         "predicao": "m_2 = beta_TGL*sin(45)*1eV; beta_TGL = alpha*sqrt(e) em runtime [derivacao publicada 2025, Zenodo 10.5281/zenodo.17526619]",
L4632     frozen_hash = sha_obj(frozen)
```

### C4. L4597-4600 (e L2955-2956)

- Onde: docstring do rito V2 (L4597-4601) e caveats do dicionário de L2939-2959.
- Congelado por hash: a docstring não; o dicionário de L2939-2959 não foi identificado como congelado nesta leitura.
- O que corrige: A tensão cresce com a precisão descreve a série que mistura o JUNO de 59,1 dias com o NuFIT global; na série autônoma do JUNO a razão caiu. Dito com os dois eixos: o degrau de 59,1 dias é anterior à previsão publicada e o de 207,2 dias é posterior à previsão publicada e, no número, anterior ao hash da regra.
- Frases vigentes que o corrigem ao lado: F8, F10.

Verbatim do um.py selado:

```
L4597     8,5074 meV e o mundo mede 8,68 -- e A TENSAO CRESCE COM A PRECISAO:
L4598     1,64 sigma (PDG 2023) -> 2,21 sigma (JUNO nov/2025, INDEPENDENTE) ->
L4599     2,95 sigma (NuFIT global pos-JUNO). Linha de morte 5 sigma quando
L4600     Dm2_21 chegar a 0,784%% (JUNO projeta 0,5%%, ~2031: tensao projetada
L2955                     "(iii) o elemento genuinamente EX ANTE e o refinamento pos-JUNO, e ele vai CONTRA: a "
L2956                     "tensao cresce com a precisao (1,64 -> 2,21 -> 2,95 sigma), com projecao de 7,83 sigma na "
L2957                     "meta do JUNO contra a linha de morte de 5 sigma ja hasheada; "
```

### C5. L4601-4604 e L4628-4630

- Onde: docstring do rito V2 (L4601-4604) e campo nao_e_cego_nesta_emissao do dicionário congelado NEUTRINO_M2_V2 (L4628-4630); as duas passagens dizem o eixo do hash da regra e não o da previsão publicada.
- Congelado por hash: L4628-4630 sim (dentro de L4615-4631, hasheado em L4632); L4601-4604 não.
- O que corrige: A declaração de cegueira do texto selado diz só o eixo da regra, e não o eixo da previsão publicada. A errata diz os dois na mesma frase: em relação à previsão publicada, o valor de 22/01/2026 é anterior ao número de 207,2 dias e posterior ao de 59,1 dias, e em relação ao hash da regra de veredito do código (08/08/2026), esse hash é posterior ao número público de 207,2 dias.
- Frases vigentes que o corrigem ao lado: F9, F5, F6, F11.

Verbatim do um.py selado:

```
L4601     7,8 sigma SE o centro nao se mover). NAO-CEGO DECLARADO: os limiares
L4602     (5/3 sigma) foram fixados na mesma sessao em que a tensao corrente ja
L4603     era conhecida -- esta emissao e uma REESPECIFICACAO; a cegueira vale
L4604     a partir de agora (regra ja hasheada julga as proximas medidas).
L4628         "nao_e_cego_nesta_emissao": ("DECLARACAO OBRIGATORIA: os limiares foram fixados na mesma sessao em que a tensao "
L4629                                      "corrente (2,95 sigma) ja havia sido calculada; esta emissao e REESPECIFICACAO, "
L4630                                      "nao veredito cego; a cegueira vale a partir de agora"),
```

### C6. L2951-2957

- Onde: caveats do dicionário de L2939-2959 (custódia da v182).
- Congelado por hash: não identificado como congelado nesta leitura.
- O que corrige: A palavra vetada pela lei da prova em L2951 lê-se retrodição sem ajuste. O elemento genuinamente EX ANTE é o refinamento pos-JUNO, de L2955: em relação à previsão publicada só o número de 207,2 dias é posterior, e em relação ao hash da regra de veredito do código esse número é anterior; o degrau de 59,1 dias e o NuFIT de dados de 2025-11 (artigo v1 de 14/01/2026, DECLARADO) são anteriores à previsão publicada. A ressalva de L2953-2954 permanece.
- Frases vigentes que o corrigem ao lado: F5, F6, F7, F8.

Verbatim do um.py selado:

```
L2951                     "(ii) postdicao NAO-AJUSTADA: as entradas (beta,sin45,1eV) nao usam dado de neutrino e o "
L2952                     "digito nunca se moveu desde 22/01/2026; a escala que zeraria a tensao (1,0200 eV) foi "
L2953                     "calculada no acervo e RECUSADA. Mas o valor medido e citado na MESMA frase que anuncia a "
L2954                     "predicao no documento de origem -- nao e predicao ex ante; "
L2955                     "(iii) o elemento genuinamente EX ANTE e o refinamento pos-JUNO, e ele vai CONTRA: a "
L2956                     "tensao cresce com a precisao (1,64 -> 2,21 -> 2,95 sigma), com projecao de 7,83 sigma na "
L2957                     "meta do JUNO contra a linha de morte de 5 sigma ja hasheada; "
```

### C0. L2944-2950 (PRECEDENTE, NÃO SE CORRIGE)

- Onde: errata da v182, dentro de L2939-2959.
- Congelado por hash: não se aplica.
- O que corrige: Nada. Está certa e é o precedente que a errata estende: já retira o Zenodo 17526619 como prioridade do valor e diz que o depósito de 04/11/2025 traz outra fórmula, com dois parâmetros livres. Confere com as contagens deste rascunho (zero ocorrências de 8.51 e sin(45 no texto-fonte de lie_of_light).

Verbatim do um.py selado:

```
L2944                     "logo a formula antecede o codigo. ERRATA v182: a redacao anterior invocava "
L2945                     "[Zenodo 10.5281/zenodo.17526619, 2025] como prioridade documental -- VERIFICADO e "
L2946                     "RETIRADO: aquele deposito (lie_of_light, November 2025) NAO contem a formula, NAO "
L2947                     "contem o numero e NAO contem a derivacao (0 ocorrencias de 8.51/meV/sin(45)); a formula "
L2948                     "que ele traz e outra, m_nu(Dt) = m_0 + a*log(Dt/tau_0), com dois parametros livres. "
L2949                     "Nenhuma alegacao de anterioridade a Dm2_21 e feita: Dm2_21 (PDG) antecede a derivacao "
L2950                     "em mais de uma decada; "
```

### C7. FORA DAS FAIXAS LIDAS (DECLARADO pelo leitor L7; conferir antes de instalar)

- Onde: L314-322 (registro zenodo_eco_2025_record), L2885, L2896, L4689, L184013, L292284, L302311-302312, L302342.
- Congelado por hash: não conferido.
- O que corrige: L7 relata que estas linhas repetem a prioridade documental da tese (L314-322), a palavra vetada pela lei da prova (L2885, L2896) e a tensão cresce com a precisão (L4689, L184013, L292284), e que L302311-302312 e L302342 repetem a declaração de cegueira que diz só o eixo do hash da regra, sem o da previsão publicada. Esta errata não leu essas linhas.
- Frases vigentes que o corrigem ao lado: F12.

## 3. Cronologia

As duas últimas colunas dizem a posição de cada fato nos dois eixos: em relação à previsão publicada (22/01/2026 nos bytes; 17/02/2026 no Zenodo) e em relação ao hash da regra de veredito do código (08/08/2026).

| Data | Fato | Fonte e estatuto | Posição em relação à previsão publicada | Posição em relação ao hash da regra |
|---|---|---|---|---|
| 2025-10-16 | Zenodo 10.5281/zenodo.17372599: publicação do artigo sobre o acoplamento não mínimo de neutrinos (registro criado em 16/10/2025, atualizado em 29/10/2025). Traz a tese, não o valor. | [REAL] API do Zenodo (resposta crua sha256 2b9148af…); texto-fonte neutrino_nmc_revised.tex: 8.51, sin(45 e JUNO com zero ocorrências | anterior à previsão publicada | anterior ao hash (08/08/2026) |
| 2025-11-04 | Zenodo 10.5281/zenodo.17526619: publicação de The Lie of Light (registro criado e atualizado em 04/11/2025). Traz a tese, não o valor. | [REAL] API do Zenodo (sha256 938a0d48…); lie_of_light.tex: zero ocorrências de 8.51, meV, sin(45 e JUNO; um.py L2946-2947 diz o mesmo do depósito | anterior à previsão publicada | anterior ao hash (08/08/2026) |
| 2025-11-18 | arXiv:2511.14593: primeiro número do JUNO, 59,1 dias, Δm²₂₁ = 7,50 ± 0,12 ×10⁻⁵ eV². | [REAL] resumo cru do arXiv (sha256 92bf0554…) | anterior à previsão publicada | anterior ao hash (08/08/2026) |
| 2025-11 | NuFIT 6.1: dados de referência de 2025-11; a data da primeira apresentação pública da tabela (node 309) é OPEN. | [DECLARADO pelo Kimi] K09 ajustes_globais | os dados são anteriores; a data de apresentação da tabela é OPEN | os dados são anteriores; a data de apresentação da tabela é OPEN |
| 2026-01-14 | arXiv:2601.09791v1 (NuFIT 6.1), eq. 11: Δm²₂₁ = 7,53 +0,096 −0,097 ×10⁻⁵ eV². | [DECLARADO pelo Kimi] K09 ajustes_globais; sem resposta crua guardada | anterior à previsão publicada | anterior ao hash (08/08/2026) |
| 2026-01-22 | O valor m₂ = 8,5074 meV consta dos bytes guardados (documento complemento ao manifesto, corpo datado 22 de Janeiro de 2026; 8,51 meV junto de m₂ = 8,67 meV no mesmo parêntese). | [REAL] docx lido por script (8.51 x3; 22 de Janeiro de 2026 x1; JUNO x0; sha256 83ba9e81…; um.py L2941-2942 dá a mesma data) | é a data da previsão publicada nos bytes | anterior ao hash (08/08/2026) |
| 2026-02-17 | Zenodo 10.5281/zenodo.18674475 (A Fronteira / The Boundary): publicação registrada em 17/02/2026, registro criado em 20/02/2026; a descrição do registro traz m_ν = 8,51 meV, e o PDF escreve m_ν = α₂ · sen 45° · 1 eV = 8,51 meV (signo antigo; hoje β_TGL = α√e) junto do valor experimental de m₂ = 8,67 meV. O git público tem a mesma data de 17/02/2026 (um.py L2942-2943). | [REAL] API do Zenodo (sha256 63356257…, 8,51 x1 na descrição); o PDF local A_fronteira_v5.pdf tem md5 igual ao checksum do arquivo no Zenodo (ee1c3b20e0609b7bc7fb1a0d8bb6b92a) | é a data da previsão publicada no Zenodo | anterior ao hash (08/08/2026) |
| 2026-05-18 | Fim da janela de dados da leitura longa do JUNO (K09 janela_dados_fim). | [DECLARADO pelo Kimi] K09; sem resposta crua | posterior à previsão publicada | anterior ao hash (08/08/2026) |
| 2026-06-22 | Neutrino 2026: primeira apresentação pública da leitura longa, segundo K09; L7 suspeita de erro de transcrição com 22/07. | [DECLARADO pelo Kimi] K09; sem resposta crua guardada | posterior à previsão publicada | anterior ao hash (08/08/2026) |
| 2026-07-15 | Página do IHEP traz o valor da leitura longa de forma explícita (K09, campo renomeado aqui para primeira_apresentacao_explicita_do_valor). | [DECLARADO pelo Kimi] K09; sem resposta crua guardada | posterior à previsão publicada | anterior ao hash (08/08/2026) |
| 2026-07-22 | Notícia do JINR sobre a leitura longa. | [DECLARADO pelo Kimi] K09; sem resposta crua guardada | posterior à previsão publicada | anterior ao hash (08/08/2026) |
| 2026-07-25 | Módulo v141 do código (um.py L2943: O modulo de codigo e v141 = 25/07/2026). | [REAL no texto] um.py L2943 e L4223 | posterior à previsão publicada | anterior ao hash (08/08/2026) |
| 2026-08-08 | Hash do objeto congelado NEUTRINO_M2_V2: 4bdae22a277aa393… (K09 traz o sha_obj inteiro). | [REAL no texto] um.py L4617 (data e prefixo do hash); [DECLARADO pelo Kimi] o hash inteiro e o do dicionário portado (e2487775…) | posterior à previsão publicada | é a data do hash (08/08/2026) |
| 2026-09-29 | arXiv:2609.37895: leitura longa do JUNO, 207,2 dias, 8.294 candidatos, Δm²₂₁ = 7,388 ± 0,078 ×10⁻⁵ eV²; o artigo é posterior à previsão publicada e ao hash da regra de veredito do código, e o número já era público antes desse hash [DECLARADO: datas de jun e jul sem resposta crua]. | [REAL] resumo cru do arXiv (sha256 b2185b73…) | posterior à previsão publicada | posterior ao hash (08/08/2026) |

## 4. Frases vigentes

Cada frase diz os dois eixos. O estatuto de cada uma vem logo abaixo dela.

**F1.** Os dois artigos do autor sobre o neutrino são de 2025 (Zenodo 10.5281/zenodo.17372599, publicação de 16/10/2025; Zenodo 10.5281/zenodo.17526619, publicação de 04/11/2025) e são anteriores a qualquer número do JUNO, cujo primeiro é de 18/11/2025 (arXiv:2511.14593); são anteriores, portanto, em relação à previsão publicada do valor (22/01/2026 nos bytes guardados; 17/02/2026 no Zenodo) e em relação ao hash da regra de veredito do código (08/08/2026).

Estatuto: [REAL] datas lidas das respostas cruas do Zenodo e do arXiv, conferidas por sha256. Fonte: CRONOLOGIA_NEUTRINO_15nov.json; verificacao_fontes.json (respostas cruas com sha256 conferido).

**F2.** Esses dois artigos trazem a tese do neutrino e não o valor de m₂ (nos textos-fonte guardados as cadeias 8.51, sin(45 e JUNO têm zero ocorrências); o valor consta dos bytes guardados desde 22/01/2026 e do Zenodo 10.5281/zenodo.18674475 desde 17/02/2026, e essa é a previsão publicada, que antecede o hash da regra de veredito do código (08/08/2026) em 198 e em 172 dias, respectivamente.

Estatuto: [REAL] contagens e datas por script; [DECLARADO] que o texto-fonte guardado é o do PDF servido. Fonte: CRONOLOGIA (contagens dos dois .tex); um.py L2944-2950 (errata da v182); docx e Zenodo 18674475 lidos por script.

**F3.** O valor de m₂ não é anterior ao primeiro número do JUNO (18/11/2025): a tese o antecede e o valor não, porque a previsão publicada é de 22/01/2026, 65 dias depois do degrau de 59,1 dias, e o hash da regra de veredito do código (08/08/2026) é ainda mais tardio.

Estatuto: [REAL] datas; conta de dias por script. Fonte: CRONOLOGIA; arXiv:2511.14593 (resposta crua); docx (22/01/2026).

**F4.** A leitura de 59,1 dias do JUNO (Δm²₂₁ = 7,50 ± 0,12 ×10⁻⁵ eV², arXiv:2511.14593, 18/11/2025) é posterior aos dois artigos de 2025, anterior à previsão publicada (22/01/2026) e anterior ao hash da regra de veredito do código (08/08/2026); por isso não é cega em nenhum dos dois eixos, e para o valor de m₂ a palavra é retrodição sem ajuste, que conta como evidência de pleno direito.

Estatuto: [REAL] datas e valor lidos do resumo cru do arXiv; [KNOWN] a lei da prova de 05/10/2026 para a palavra. Fonte: arXiv:2511.14593 (sha256 92bf0554…); K09 degraus (DECLARADO, só apoio).

**F5.** A leitura de 207,2 dias do JUNO (Δm²₂₁ = 7,388 ± 0,078 ×10⁻⁵ eV², arXiv:2609.37895, 29/09/2026) é posterior à previsão publicada (22/01/2026 nos bytes; 17/02/2026 no Zenodo) e, quanto ao número, anterior ao hash da regra de veredito do código (08/08/2026), porque o número já era público em 15/07/2026 [DECLARADO: sem resposta crua guardada] e só o artigo do arXiv, de 29/09/2026, é posterior a esse hash.

Estatuto: [REAL] a data do arXiv e o valor; [DECLARADO] as datas de 22/06, 15/07 e 22/07/2026 (sem resposta crua). Fonte: arXiv:2609.37895 (sha256 b2185b73…); K09 degraus (DECLARADO); DESENHO v412 R1 via L7.

**F6.** Dita nos dois eixos, a leitura de 207,2 dias é cega em relação à previsão publicada, porque o número nasceu depois do valor, e não é cega em relação ao hash da regra de veredito do código, porque o número era público antes dele; por isso ela não é a primeira leitura prospectiva da regra congelada.

Estatuto: [REAL] a ordem entre o valor e o artigo; [DECLARADO] a data de 15/07/2026. Fonte: regra de 15/11/2026 (arquivo de bytes sha16 49e5f0072e8beb02); K09 degraus; F5.

**F7.** Para o valor de m₂, em relação ao PDG 2023 e ao degrau de 59,1 dias do JUNO, ambos anteriores à previsão publicada (22/01/2026) e ao hash da regra de veredito do código (08/08/2026), a palavra é retrodição sem ajuste (novidade de uso; precedente: o periélio de Mercúrio) e não previsão anterior ao dado, porque nenhuma entrada da fórmula (β, sen 45°, 1 eV) usa dado de neutrino [DECLARADO no código selado, L2951-2952; esta errata não reconfere a conta]; a ressalva do código selado (L2953-2954), de que o documento de origem cita o valor medido junto do valor da TGL, permanece.

Estatuto: [KNOWN] a lei da prova de 05/10/2026, itens 1, 2 e 5; [DECLARADO] que nenhuma entrada usa dado de neutrino. Fonte: um.py L2951-2954; docx e PDF do Zenodo lidos por script (8,51 meV junto de 8,67 meV).

**F8.** Na série autônoma do JUNO a razão em m₂ caiu de 2,21σ (59,1 dias, anterior à previsão publicada) para 1,94σ (207,2 dias, posterior à previsão publicada e, quanto ao número, anterior ao hash da regra de veredito do código); em Δm²₂₁ a queda é de 2,19σ para 1,93σ; a frase do código selado de que a tensão cresce com a precisão (1,64σ, 2,21σ, 2,95σ; L4597-4599) descreve a série que mistura o degrau de 59,1 dias com o ajuste global NuFIT, e não a série autônoma, e a projeção de 7,8σ para cerca de 2031 vale só se o centro não se mover (L4600-4601).

Estatuto: [REAL] as razões, recalculadas aqui por script a partir dos resumos crus do arXiv e da previsão; [REAL no texto] L4597-4601. Fonte: verificacao_fontes.json (razoes); um.py L4597-4601; K09 degraus (DECLARADO, só apoio: mesmas razões).

**F9.** A declaração do código selado de que a cegueira vale a partir de agora (L4603-4604, L4630) diz só o eixo da regra, porque os limiares foram fixados no objeto congelado de 08/08/2026, depois de o número de 207,2 dias já ser público [DECLARADO: datas de jun e jul sem resposta crua]; falta o eixo da previsão publicada, em relação ao qual o valor de 22/01/2026 é anterior ao número de 207,2 dias e posterior ao de 59,1 dias; o texto congelado não muda, e a errata vai ao lado.

Estatuto: [REAL no texto] L4601-4604 e L4628-4630; [DECLARADO] as datas da leitura longa. Fonte: um.py L4601-4604, L4617, L4622, L4628-4632.

**F10.** O 2,95σ do código selado é a razão em m₂ com o erro simétrico arredondado (7,53 ± 0,10); com os erros assimétricos publicados do lado da previsão a razão é 3,02σ (tabela do node 309, dados de 2025-11, data de apresentação OPEN) e 3,04σ (eq. 11 do arXiv:2601.09791v1, de 14/01/2026, anterior à previsão publicada e ao hash da regra de veredito do código), e a regra congelada começa o ramo TENSION em 3,0 (L4623); esta errata diz os três números e não escolhe entre eles.

Estatuto: [REAL] as razões, recalculadas aqui por script; [DECLARADO pelo Kimi] as entradas 7,537 +0,094 −0,100 e 7,53 +0,096 −0,097 e as datas do NuFIT; [REAL no texto] L4598-4599, L4623 e L4629. Fonte: verificacao_fontes.json (razoes); K09 ajustes_globais; um.py L4598-4599, L4623, L4629.

**F11.** Só um número do JUNO tomado depois de 18/05/2026 [DECLARADO: fim da janela de dados da leitura de 207,2 dias, K09] seria posterior à previsão publicada e posterior ao hash da regra de veredito do código, e só ele poderia ser dito cego nos dois eixos; esta errata não registra nenhum número desse tipo e, se um novo número do JUNO for publicado, esta frase caduca.

Estatuto: [DECLARADO] a data de 18/05/2026 (K09, sem resposta crua) e a ausência de número posterior (leitura da gerência de 14/11 via L7, não reconferida). Fonte: K09 degraus (janela_dados_fim); L7 P6.

**F12.** O registro de custódia zenodo_eco_2025_record (um.py L314-322, lido pelo leitor L7 e não por esta errata) vale para a tese, publicada em 04/11/2025 e anterior ao módulo v141 do código (25/07/2026), e não para o valor de m₂, cuja previsão publicada é de 22/01/2026 e cujo hash da regra de veredito do código é de 08/08/2026; em relação ao primeiro número do JUNO a tese o antecede e o valor não.

Estatuto: [DECLARADO pelo leitor L7] o conteúdo de L314-322, fora da faixa lida; [REAL no texto] a data do módulo v141 em L2943 e L4223. Fonte: L7 A6 e P8; um.py L2943, L4223.

**F13.** Esta errata é um registro novo ao lado do texto selado: L4241 e L4620 estão dentro de objetos congelados por hash (o dicionário NEUTRINO_SUM_V1 e o NEUTRINO_M2_V2, este com sha_obj em L4632), de modo que o hash da regra de veredito do código não muda, e a previsão publicada é citada ao lado, nunca por cima.

Estatuto: [REAL no texto] L4238, L4615-4617 e L4632; [dado do mandato] que L4241 e L4620 estão em objetos congelados por hash. Fonte: um.py L4238-4244, L4615-4632.

## 5. Os degraus do JUNO

Previsão: m₂ = 8,5074 meV; Δm²₂₁ = 7,2376 ×10⁻⁵ eV². A razão é (observado − previsão) sobre o σ do lado da previsão; em m₂ propaga-se o σ de Δm²₂₁ por σ(m₂) = σ(Δm²) / (2·√Δm²). O perito oficial registrado no Mapa é o JUNO autônomo (rota neutrinos.m2.normalizacao, estatuto DECLARADO na rota); o NuFIT e o Capozzi são reflexos globais ao lado.

| Degrau | Δm²₂₁ (×10⁻⁵ eV²) | m₂ observado (meV) | Razão em m₂ (σ) | Razão em Δm²₂₁ (σ) | Fonte | Posição em relação à previsão publicada | Posição em relação ao hash da regra |
|---|---|---|---|---|---|---|---|
| 59,1 dias efetivos | 7,50 ± 0,12 | 8,660 | 2,206 | 2,187 | arXiv:2511.14593, 18/11/2025 [REAL]; Nature 654, 343–348, 10/06/2026 [DECLARADO pelo Kimi] | anterior à previsão publicada | anterior ao hash da regra de veredito do código (08/08/2026) |
| 207,2 dias efetivos | 7,388 ± 0,078 | 8,595 | 1,938 | 1,928 | arXiv:2609.37895, 29/09/2026 [REAL]; número já público em 22/06, 15/07 e 22/07/2026 [DECLARADO pelo Kimi, sem resposta crua] | posterior à previsão publicada | o número é anterior ao hash da regra de veredito do código (08/08/2026); só o artigo do arXiv é posterior |

Na série autônoma do JUNO a tensão caiu: de 2,21σ para 1,94σ em m₂ (de 2,19σ para 1,93σ em Δm²₂₁). A frase de L4597-4599, a tensão cresce com a precisão (1,64σ, 2,21σ, 2,95σ), mistura o degrau de 59,1 dias com o ajuste global NuFIT. Conferência: as razões recalculadas aqui coincidem com as do K09 até 3.2e-14.

## 6. A divergência de número que não se esconde

O ramo TENSION da regra congelada começa em 3,0 (L4623: TENSION sse a razão ficar em [3, 5) na determinação global mais recente). Há três números para a mesma linha do NuFIT 6.1:

| Fonte | Entrada (×10⁻⁵ eV²) | Razão em m₂ (σ) | Razão em Δm²₂₁ (σ) | Lado de 3,0 em m₂ | Origem e estatuto |
|---|---|---|---|---|---|
| o código selado (core) | 7,53 ± 0,10 (erro simétrico arredondado) | 2,953 | 2,924 | abaixo de 3,0 | L4598-4599 e L4629 trazem 2,95 sigma [REAL no texto]; a entrada 7,53 ± 0,10 vem do mandato e de L7 (L4642-4644, não lidas aqui) [DECLARADO]; K09 a registra como representação simétrica arredondada |
| tabela NuFIT 6.1, node 309 (K09) | 7,537 +0,094 −0,100 (σ do lado da previsão = 0,100) | 3,024 | 2,994 | acima de 3,0 (em Δm²₂₁, abaixo) | [DECLARADO pelo Kimi] entradas e data (OPEN); razão recalculada aqui por script |
| arXiv:2601.09791, eq. 11 (K09) | 7,53 +0,096 −0,097 (σ do lado da previsão = 0,097) | 3,044 | 3,014 | acima de 3,0 (em Δm²₂₁, também) | [DECLARADO pelo Kimi] entradas e datas (v1 de 14/01/2026, v2 de 12/04/2026); razão recalculada aqui por script |

Em palavras simples: com o erro simétrico arredondado o código fica abaixo da linha de 3,0; com o erro que as fontes publicam do lado da previsão ele ficaria acima, em m₂. Em Δm²₂₁ a linha da tabela fica abaixo (2,994) e a da eq. 11 fica acima (3,014); a razão do código é em m₂ (L4598 traz 2,21, que é a razão em m₂ do degrau de 59,1 dias). A errata diz os três números, diz de onde vem cada um e não escolhe. As fontes também divergem sobre qual determinação o ramo lê (D3).

## 7. O que a errata NÃO diz

- Não move o gate. Nenhum resultado desta errata entra no qg_closure; NOT_FALSIFIED segue não sendo a palavra da creditação.
- Não é veredito. Nenhum desfecho do rito é emitido, tocado ou relido por ela.
- Não reabre teste. Não escolhe regra de morte, limiar, métrica ou classe de pré-registro.
- O estado do rito segue TGL_NU_M2_ARMED_CONSISTENT (dado do mandato; esta leitura não reconferiu o core).
- Não afirma que o valor de m₂ é previsão anterior ao primeiro número do JUNO: a tese o antecede e o valor não (F3).
- Não diz o que o autor leu ou deixou de ler. Fala só de datas e das entradas da fórmula.
- Não afirma ajuste nem ausência de ajuste além do que o código selado declara (L2951-2952).
- Não escolhe entre 2,95, 3,02 e 3,04 (F10) e não declara o ramo TENSION.
- Não troca o perito oficial registrado no Mapa (o JUNO autônomo) nem o estatuto do valor ([DERIVED]).
- Não muda o estatuto do sen 45° nem a escala de 1 eV, declarada e não derivada (L4621).
- Não reescreve nem pina de novo nada: o texto congelado e os hashes ficam como estão; a errata é um registro ao lado.
- Não rotula a leitura de 207,2 dias como retrodição nem como previsão: dá só as posições em relação à previsão publicada e ao hash da regra de veredito do código (F5, F6).
- Não instala nada e não é creditação.

## 8. O que é do operador decidir

- **D1.** Em que forma a errata entra no core da v412: registro novo ao lado, com id de errata a seguir ao último da v411 (E44, DECLARADO via L7) e nome do registro. Nomes são do operador; os desta página são provisórios da gerência.
- **D2.** Qual erro do NuFIT vale para a regra: o simétrico arredondado (7,53 ± 0,10, que dá 2,95σ) ou o assimétrico publicado do lado da previsão (3,02σ e 3,04σ). O ramo TENSION começa em 3,0 (L4623). Em palavras simples: com um erro o código fica abaixo da linha, com o outro fica acima. Se o ramo lê a linha global, a escolha decide se o código fica abaixo ou acima de 3,0; se lê o JUNO autônomo (1,94σ no último degrau), a escolha não o move (D3).
- **D3.** Qual determinação o ramo lê: o JUNO autônomo (perito oficial no Mapa, rota neutrinos.m2.normalizacao) ou a última linha da escada global, que L7 relata em L4666, linha não lida aqui.
- **D4.** Que fonte guardar para as datas de 22/06, 15/07 e 22/07/2026 da leitura longa, que não têm resposta crua: pedir a captura das três páginas pelo canal do orquestrador.
- **D5.** Se a palavra tese precisa de definição na errata. O código selado (L2946-2948) diz que a fórmula do depósito de 04/11/2025 é outra (m_nu(Dt) = m_0 + a*log(Dt/tau_0), dois parâmetros livres); o mandato diz que os dois artigos trazem a tese. A errata usa a palavra sem defini-la.
- **D6.** Se a errata cobre também os lugares fora das faixas lidas (C7), com leitura própria de cada linha antes de instalar.
- **D7.** Se entra como pino adicional o hash do dicionário portado ao um.py (e2487775…, DECLARADO pelo Kimi) ao lado do hash do objeto original (4bdae22a…, de 08/08/2026). A data da portagem não foi estabelecida aqui.
- **D8.** Se F11 (o único dado cego nos dois eixos seria posterior a 18/05/2026) entra na errata ou fica só no desenho da v412, e como se nomeia o status da leitura de 207,2 dias, que aqui só recebe as posições em relação à previsão publicada e ao hash da regra de veredito do código.

## 9. Limites e o que não fechou

- As datas de 22/06, 15/07 e 22/07/2026 da leitura longa são [DECLARADO pelo Kimi], sem resposta crua guardada. A conclusão de que o número era público antes do hash de 08/08/2026 não depende de qual das três vale (as três caem entre 17/02/2026 e 08/08/2026), mas depende de uma delas ser verdadeira.
- O registro Zenodo 10.5281/zenodo.17426652 (The Graviton, the Psion…, publicação 14/10/2025, atualizado em 22/04/2026) não foi lido por ninguém. F1 e F2 falam só dos dois artigos de neutrino.
- Os PDFs servidos pelo Zenodo para os dois artigos de 2025 não estão no disco; F2 repousa nos textos-fonte .tex guardados (mtime 28/10/2025 e 12/11/2025; o segundo é posterior ao depósito de 04/11/2025) e, para o depósito de 04/11/2025, também no texto do código selado (L2946-2947). No primeiro texto-fonte a unidade meV aparece uma vez, num intervalo de energias genérico, sem o valor.
- O hash 4bdae22a277aa393… é o do objeto original serializado (sha_obj), não o sha256 de um arquivo; a data de 08/08/2026 é a dele. O hash do dicionário portado (e2487775…) é [DECLARADO pelo Kimi] e a data da portagem não foi estabelecida aqui.
- L7 relata, via cabeçalho de 02_frozen_neutrino_m2_v2.py, que a lista de medidas da regra de 08/08/2026 termina em 2025-12 e não traz o número da leitura longa [DECLARADO pelo revisor; não reconferido aqui].
- Do um.py li só L2930-2960, L4215-4254 e L4595-4635. Não li L4636-4666 (a linha NuFIT do core e a escada), L314-322, L2885, L2896, L4689, L184013, L292284 e L302311-302342; o que se diz delas vem de L7.
- Que nenhuma entrada da fórmula usa dado de neutrino é declaração do código selado (L2951-2952); a errata não reconfere a conta.
- As razões em σ foram recalculadas aqui por script a partir das entradas (resumos crus do arXiv para o JUNO; entradas do K09 para o NuFIT) e coincidem com o K09 até 3.2e-14; o 1,64σ do PDG 2023 não foi recalculado.
- A previsão (m₂ = 8,5074 meV; Δm²₂₁ = 7,2376 ×10⁻⁵ eV²) foi calculada por script como α(CODATA 2018)·√e·sen 45°·1 eV, sem literal de β; coincide com L4597 (8,5074 meV) e com o K09.
- O estado ARMED_CONSISTENT é dado do mandato; a ratificação do perito oficial em 02/10/2026 é dado da rota do Mapa (DECLARADO na rota); nenhum dos dois foi reconferido no core.
- A chave do K09 para a data de 15/07/2026 contém a raiz vetada pela regra da casa e não foi herdada; aqui o campo se chama primeira_apresentacao_explicita_do_valor. O campo posicao_relativa_ao_pino do K09 não diz o sujeito; aqui toda posição diz em relação a quê.
- Os documentos de origem escrevem a fórmula com o signo antigo α₂ (verificado por script no PDF do Zenodo; L7 relata o mesmo do documento de 22/01/2026, não reconferido aqui); a memória tgl-signo-e-cronologia registra β_TGL como o signo vigente; cita-se o valor, não a fórmula como escrita.

## 10. Fontes, verificações e consultas

Fontes (hashes lidos por script):

- CRONOLOGIA_NEUTRINO_15nov.json: 8281 bytes; sha256 48519aef36039db0ac9a24b685bdd5c31e79a5fa0d720492c73fe8ab46e2c752.
- ERRATA_NEUTRINO_V412_DADOS_K09.json (parcial, DECLARADO pelo Kimi, só apoio): 6682 bytes; sha256 deae4e3dfb72cd3cab2aa6054b2ba39d48f6a8a5545fd23e83268190ef75ab9c.
- L7-registro-e-errata.md (leitor, DECLARADO até conferência): 39289 bytes; sha256 9131da5d82c311a1dab01c91cef08644219c3d88f9fe21f05d6e97310102e114.
- um.py selado (faixas L2930-2960, L4215-4254, L4595-4635): 46828680 bytes; sha256 1203b1f9202020d602a7fa8a6bea56d4b48e27ed8baffe98bcbd16e94f97a8e0.
- arquivo de bytes da regra de 15/11/2026 (só o hash; o texto não foi reproduzido): 725 bytes; sha256 49e5f0072e8beb028eb64e090cb43a77c3672d15577bfaeee105ee2c9bfe782f.

Verificações feitas aqui:

- [REAL] As seis respostas cruas (4 do Zenodo, 2 do arXiv) têm sha256 igual ao da CRONOLOGIA_NEUTRINO_15nov.json.
- [REAL] O PDF local A_fronteira_v5.pdf tem md5 ee1c3b20e0609b7bc7fb1a0d8bb6b92a, igual ao checksum do arquivo no registro do Zenodo 18674475.
- [REAL] Os resumos crus do arXiv trazem 7.50, 0.12 e 59.1 (2511.14593) e 7.388, 0.078 e 207.2 dias (2609.37895; posterior à previsão publicada e, no número, anterior ao hash da regra de veredito do código).
- [REAL] Contagens nos textos-fonte: neutrino_nmc_revised.tex e lie_of_light.tex têm zero ocorrências de 8.51, sin(45 e JUNO; docx do acervo tem 8.51 x3 e a data 22 de Janeiro de 2026 x1; a descrição do registro 18674475 tem 8,51 x1.
- [REAL] O PDF do Zenodo 18674475 traz, por extração de texto (pypdf, 73 páginas), m_ν = 8,51 meV com o signo antigo α₂ e o valor experimental de m₂ de 8,67 meV.
- [REAL] Dias entre as datas, por script: 22/01 a 08/08/2026 = 198; 17/02 a 08/08/2026 = 172; 18/11/2025 a 22/01/2026 = 65.
- [REAL] O um.py tem 46828680 bytes e sha256 1203b1f9202020d602a7fa8a6bea56d4b48e27ed8baffe98bcbd16e94f97a8e0 (sha16 1203b1f9202020d6, o da v411 selada).

Mapa de Rotas consultado, um termo por vez: neutrino (45 rotas); errata (160, truncado); JUNO (13); m2 (50); retrodicao (7); cronologia (8); NuFIT (4); rotas lidas: neutrinos.m2.normalizacao; estatistica.v412.k04_hubble_m2_combinacao; estatistica.coincidencia_conjunta; cadeia.preparacao_v412. Nada foi registrado no Mapa.

Fim do rascunho. Nada aqui foi instalado, selado, aberto ou registrado.
