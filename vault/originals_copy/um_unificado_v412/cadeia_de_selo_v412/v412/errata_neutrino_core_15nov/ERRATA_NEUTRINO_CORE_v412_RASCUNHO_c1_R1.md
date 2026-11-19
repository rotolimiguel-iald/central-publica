# Errata do neutrino para o core da v412 — RASCUNHO R1 da gerência c1

Estado: rascunho R1 (rodada única de conserto sobre o rascunho de W1, que fica intacto: md sha256 a446225189769ec0fb427afaf28b99a7128f872bc3f9f86f870938c4f3b9724c, json sha256 f465e2597833d0d07b828b126e172ba239e662ff3111bdab8184293cc674b8d0). Não se instala, não muda o um.py, não move o gate. Gerado por script em 2026-11-15T16:08:31 a partir das fontes listadas na seção 10; os versos do um.py, os hashes, as contas e as datas são lidos por script, nunca de memória. Nota para quem for instalar: o campo verbatim do json é o texto exato das linhas do um.py; o md mostra o rótulo da linha, um espaço e o mesmo texto.

Estatutos: [REAL] medido ou lido aqui; [KNOWN] literatura ou regra da casa; [DECLARADO] afirmado na origem e não reconferido aqui; [dado do mandato] informado na ordem da gerência que pediu este rascunho, não reconferido aqui; [OPEN] em aberto.

## 0. Leia primeiro, na língua do operador

- O que esta errata faz: escreve, ao lado do um.py selado, a correção dos versos que dizem que a derivação m = β·sen 45°·1 eV foi publicada em 2025, o que os textos de 2025 não trazem, e a das passagens que medem a cegueira de uma leitura só pelo eixo do hash da regra, sem o eixo da previsão publicada.
- O que ela não faz: não muda o texto selado nem os hashes, não move o gate, não é veredito, não reabre teste. O estado do rito segue ARMED_CONSISTENT (dado do mandato).
- O que muda de leitura, nos dois eixos: os dois artigos do autor sobre o neutrino são de 2025 (16/10/2025 e 04/11/2025), anteriores ao primeiro número do JUNO (18/11/2025), à previsão publicada do valor (22/01/2026 nos bytes guardados, sem carimbo externo; 17/02/2026 publicado) e ao hash da regra de veredito do código (08/08/2026); o valor de m₂, ao contrário, é posterior ao primeiro número do JUNO e anterior ao hash da regra, e a derivação dele não está nos dois artigos.
- O que os dois artigos trazem: o que o título e o resumo de cada um afirmam (seção 1B), e só isso é o que esta errata chama de tese do neutrino. A fórmula e o valor não estão neles: nas cadeias buscadas a contagem é zero, inclusive no PDF servido do 17526619. Os versos selados L4222-4225, L4241, L4243 e L4620 dizem o contrário; o selado já o havia retirado desse depósito em L2944-2950 (errata da v182).
- A palavra para o valor: em relação ao PDG e ao degrau de 59,1 dias, ambos anteriores à previsão publicada e ao hash da regra, é retrodição sem ajuste, que conta como evidência de pleno direito pela lei da prova de 05/10/2026. O sinal dessa evidência é o das razões da seção 5: 2,21σ e 1,94σ de distância entre o observado e a previsão, com o observado acima da previsão nos dois degraus; e a objeção de que o selado diz sen 45° POSTULADO (L2935-2938) está na F7.
- Um número que o texto diz e não resolve: o código lê 2,95σ no NuFIT; a tabela oficial do NuFIT 6.1, guardada como captura com hash, dá 3,02σ com o erro do lado da previsão; a eq. 11 do arXiv:2601.09791 dá 3,04σ; outros ajustes globais dão 2,44σ e 2,86σ (seção 6). O ramo TENSION começa em 3,0, e TENSION não é falsificação (FALSIFIED exige duas determinações independentes de 5σ ou mais, L4622). A escolha é do operador.

## 1. A regra de 15/11/2026 e os dois eixos

A regra está registrada em arquivo de bytes (sha16 49e5f0072e8beb02; o texto dela não é reproduzido aqui). Ela manda que a cegueira de uma leitura se diga sempre nos dois eixos, o da previsão publicada e o do hash da regra, na mesma frase.

- Eixo 1: em relação à previsão publicada. Previsão publicada é o valor de m₂ (8,51 meV nos documentos; 8,5074 meV na conta por script) como consta (i) nos bytes guardados do documento complemento ao manifesto desde 22/01/2026 (data no corpo; docProps created e modified 2026-01-22T15:31:39.826Z; mtime 2026-01-22T12:40:23; sem carimbo externo) e (ii) publicado em 17/02/2026 no Zenodo 10.5281/zenodo.18674475 (registro criado em 20/02/2026). Nesta errata, 22/01/2026 quer dizer sempre bytes guardados sem carimbo externo, e 17/02/2026 quer dizer publicado.
- Eixo 2: em relação ao hash da regra de veredito do código. Há dois hashes, e a errata não os confunde. (a) O hash do objeto ORIGINAL da regra, 4bdae22a277aa393…, de 08/08/2026, citado em um.py L4617 (arquivo teste_acustico_beta_tgl_v1/02_frozen_neutrino_m2_v2.py). (b) O hash do dicionário PORTADO ao um.py (NEUTRINO_M2_V2, L4615-4631), calculado em L4632 (frozen_hash = sha_obj(frozen)). É outro objeto: o dicionário tem a chave portado_de (L4617), que cita o hash do original, e um objeto não carrega o próprio hash; e tem a chave supersedes (L4618), que cita uma decisão de 10/08/2026, posterior a 08/08/2026. Logo o hash portado é de 10/08/2026 ou posterior, e a data da portagem não está estabelecida (D7). [Inferência da gerência a partir de L4617, L4618 e L4632; a função sha_obj não foi lida.] Nenhum fato da cronologia cai entre 08/08/2026 e 10/08/2026; por isso as posições das seções 3 e 5 valem para os dois hashes. Onde o texto diz o hash da regra sem mais, entende-se o do objeto original, de 08/08/2026.
- Nenhuma entrada da fórmula usa dado de neutrino [DECLARADO no código selado, L2951-2952; a errata não reconfere a conta]. A previsão calculada por script é m₂ = 8,5074 meV e Δm²₂₁ = 7,2376 ×10⁻⁵ eV² (α CODATA 2018 · √e · sen 45° · 1 eV, sem literal de β).

## 1B. O que os dois artigos de 2025 contêm e o que não contêm

Esta seção responde ao que cada verso selado afirma e ao que os textos de 2025 trazem de fato. Fontes: as respostas cruas do Zenodo e os textos guardados que a CRONOLOGIA_NEUTRINO_15nov.json aponta (os .tex) e os PDFs das mesmas pastas (verificacao_R1.json, por script).

**O que os versos selados afirmam.** L4222-4225 (docstring v147), L4241 (campo prediction), L4243 (campo custody) e L4620 (campo predicao do dicionário portado) dizem que a derivação m = β·sen 45°·1 eV foi publicada em 2025, citando um só depósito, o Zenodo 10.5281/zenodo.17526619 (The Lie of Light, 04/11/2025); L4222 e L4243 dizem também que ela é anterior ao código (módulo v141, 25/07/2026). O mesmo arquivo selado diz o oposto em L2944-2950: esse depósito NÃO contém a fórmula, o número nem a derivação. A retirada da v182 não chegou aos quatro versos.

**O que os textos de 2025 não contêm (contagem).** Cadeias buscadas: 8,5 seguido de dígito (inclui 8.51 e 8,51) e 0,0085 (a coluna valor); sin…45, 45° e π/4 (a coluna fórmula); 1 eV; √e; meV; JUNO.

| Zenodo | Fonte lida | É o texto servido? | valor | fórmula | 1 eV | √e | meV | JUNO |
|---|---|---|---|---|---|---|---|---|
| 17526619 | lie_of_light.pdf do disco (17 páginas, texto extraído por pypdf; md5 e7b8976d0227b000eb9871218050bfe9 e 255439 bytes, iguais ao checksum do Zenodo) | é o texto servido | 0 | 0 | 0 | 0 | 0 | 0 |
| 17526619 | descrição do registro (resposta crua da API do Zenodo, sha256 938a0d48…) | é o servido | 0 | 0 | 0 | 0 | 0 | 0 |
| 17526619 | lie_of_light.tex (mtime 12/11/2025, posterior ao depósito de 04/11/2025) | não é o servido | 0 | 0 | 0 | 0 | 0 | 0 |
| 17372599 | descrição do registro (resposta crua da API do Zenodo, sha256 2b9148af…) | é o servido | 0 | 0 | 0 | 0 | 0 | 0 |
| 17372599 | neutrino_nmc_revised.pdf do disco (10 páginas, texto extraído por pypdf; mtime 28/10/2025; md5 94fabc1292de29a2e2e2361255a90d3f e 506794 bytes; o servido tem md5 ae0f1210ddf941d0e147b4dcddb1e5e1 e 506616 bytes, registro atualizado em 29/10/2025) | NÃO é o servido; versão próxima, de um dia antes | 0 | 0 | 0 | 0 | 1 | 0 |
| 17372599 | neutrino_nmc_revised.tex (mtime 28/10/2025) | versão próxima, não é o servido | 0 | 0 | 0 | 0 | 1 | 0 |

O único meV é o do neutrino_nmc_revised (PDF local e .tex), num intervalo de energias genérico (de meV a PeV), sem valor. Estatuto: [REAL] contagens por script; vale para as cadeias listadas e para o texto extraído, não prova que nenhuma outra grafia exista. Para o 17526619 o texto lido é o servido (md5 igual); para o 17372599 o PDF do disco não é o servido e a contagem vale para uma versão próxima e para a descrição servida do registro.

**O que os dois artigos contêm, pelo conteúdo lido (título e resumo).**

- Zenodo 10.5281/zenodo.17372599, publicado em 2025-10-16. Título: Testing Non-Minimal Gravitational Coupling of Neutrinos via Entropy-Production Mechanism: Multi-Messenger Evidence and Validation with Post-2018 Data.
  - Propõe que os neutrinos têm acoplamento gravitacional anômalo, vindo de um mecanismo de produção de entropia no setor de interação luz-gravidade: num quadro de acoplamento não mínimo, o campo de fótons acoplado à curvatura gera entropia e os neutrinos seriam o canal entrópico desse processo irreversível.
  - Prevê acoplamento gravitacional efetivo nulo para os neutrinos (ξ_ν ≈ 0), contra o acoplamento mínimo padrão (ξ_ν = 1).
  - Declara resultados observacionais, que esta errata não avalia: entropia temporal de SN 1987A, S/S_max = 0,80 ± 0,04 (4,8σ acima do térmico); isotropia do IceCube em 12 anos, χ² = 0,01 (rejeição de lente da Via Láctea a 3,0σ); correlação de curvatura em seis fontes, r = 0,81 e p = 0,05; fator de Bayes combinado de 72; Δχ² = −1,8 na análise cosmológica com CAMB.
  - Propõe testes por observações multimensageiras de transientes com lente gravitacional (neutrinos chegando antes pelo atraso Shapiro dos fótons, de 10 a 100 ms).
  - Fonte lida: resposta crua do Zenodo (sha256 2b9148af…) e o resumo do neutrino_nmc_revised.tex; o título e o resumo coincidem em conteúdo. O resumo em português é paráfrase da gerência; o texto em inglês está na resposta crua.
- Zenodo 10.5281/zenodo.17526619, publicado em 2025-11-04. Título: Neutrinos: The Lie of Light According to Luminodynamic Gravitation Theory.
  - Reinterpreta os neutrinos dentro da TGL: não seriam partículas fundamentais, mas restos temporais de fótons (ex-luz, a luz que foi); a hipótese se chama Lie of Light, ν = lim (Δt→∞) γ(t − Δt).
  - Diz que a hipótese resolve anomalias empíricas: massa quase nula, interação ultrafraca, oscilação de sabor e fundo cosmológico de neutrinos.
  - Lista previsões testáveis: correlações temporais entre a história de emissão dos fótons e o fluxo atual de neutrinos; assinaturas de decaimento que dependem da idade; a oscilação relida como evolução de fase temporal.
  - Além do resumo, o PDF servido escreve uma massa que depende da idade, m_ν(Δt) = m_0 + α·log(Δt/τ_0) (eq. 28, seção 4.4.3), com símbolos e sem valor próprio; as únicas massas em eV citadas no PDF são duas vezes o limite Σm_ν < 0,12 eV (Planck 2018). O selado (L2948) chama essa fórmula de outra, com dois parâmetros livres; o PDF escreve três símbolos (m_0, α, τ_0), e esta errata não decide a contagem.
  - Fonte lida: resposta crua do Zenodo (sha256 938a0d48…) e o lie_of_light.pdf do disco, que é o servido (md5 igual); o corpo do PDF foi lido por extração de texto. O resumo em português é paráfrase da gerência; o texto em inglês está na resposta crua.

**A palavra tese.** Nesta errata, a palavra tese, quando aparece, designa só o conteúdo acima, o que o título e o resumo de cada um dos dois artigos de 2025 afirmam; não inclui a fórmula m = β·sen 45°·1 eV nem o valor de m₂. Foi definida aqui uma vez; se a definição vale é do operador (D5).

**Consequência.** O que antecede o primeiro número do JUNO, a previsão publicada do valor e o hash da regra é esse conteúdo dos dois artigos. O valor de m₂ não vem deles: é a própria previsão publicada, nos bytes guardados desde 22/01/2026 (sem carimbo externo) e publicada em 17/02/2026, posterior ao primeiro número do JUNO e anterior ao hash da regra.

## 2. O que a errata corrige no um.py selado

Arquivo: C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py (46828680 bytes; sha256 1203b1f9202020d602a7fa8a6bea56d4b48e27ed8baffe98bcbd16e94f97a8e0; sha16 1203b1f9202020d6, o da v411 selada). Li só as faixas L2930-2960, L4215-4254 e L4595-4635. Os versos abaixo vêm dessas faixas por script, sem edição. Em todos os casos a correção é ao lado, um registro novo: L4241 e L4620 estão dentro de objetos congelados por hash.

### C1. L4222-4225

- Onde: docstring de prove_neutrino_sum_protocol (v147); o dicionário congelado desta função começa em L4238.
- Congelado por hash: a docstring não está no dicionário que começa em L4238; a regra da casa (selado não se reescreve) manda a errata ao lado mesmo assim.
- O que corrige: O verso afirma que a derivação m_nu = beta*sin45*1eV foi PUBLICADA ANTES do código, com prioridade documental, citando o Zenodo 17526619 de 2025 (L4223). Os textos de 2025 não contêm a fórmula nem o valor (seção 1B: contagem zero nas cadeias buscadas, inclusive no PDF servido do 17526619), e o selado já retirou esse depósito como prioridade documental da fórmula e do número em L2944-2950 (errata da v182); esta errata estende essa retirada a este verso. O que os dois artigos de 2025 trazem é o que o título e o resumo de cada um afirmam (seção 1B), e isso antecede o primeiro número do JUNO (18/11/2025), a previsão publicada do valor e o hash da regra de veredito do código (08/08/2026); o valor de m₂, que é a própria previsão publicada (nos bytes guardados desde 22/01/2026, sem carimbo externo, e publicado em 17/02/2026), é posterior ao primeiro número do JUNO e anterior ao hash da regra, e a derivação dele não está nos dois artigos. A palavra vetada pela lei da prova (L4225) lê-se retrodição sem ajuste.
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
- Congelado por hash: sim, dado do mandato; a linha do cálculo do hash do V1 fica fora da faixa lida; L2938 diz, de um dict frozen, que o seu hash não se move, mas a que dicionário ela se refere não foi lido (as linhas anteriores a L2930 não foram lidas).
- O que corrige: L4241 diz derivação publicada 2025 e L4243 diz derivação ANTES do código (Zenodo 17526619, 2025). Os textos de 2025 não contêm a fórmula nem o valor (seção 1B: contagem zero nas cadeias buscadas, inclusive no PDF servido do 17526619), e o selado já retirou esse depósito como prioridade documental da fórmula e do número em L2944-2950 (errata da v182); esta errata estende essa retirada a este verso. O que os dois artigos de 2025 trazem é o que o título e o resumo de cada um afirmam (seção 1B), e isso antecede o primeiro número do JUNO (18/11/2025), a previsão publicada do valor e o hash da regra de veredito do código (08/08/2026); o valor de m₂, que é a própria previsão publicada (nos bytes guardados desde 22/01/2026, sem carimbo externo, e publicado em 17/02/2026), é posterior ao primeiro número do JUNO e anterior ao hash da regra, e a derivação dele não está nos dois artigos. L4244 usa a palavra vetada pela lei da prova.
- Frases vigentes que o corrigem ao lado: F1, F2, F7, F13.

Verbatim do um.py selado:

```
L4240         "prediction": ("Sigma m_nu = m1 + m2 + m3 com m1 ~ 0 [declarado], m2 = beta*sin(45)*1eV "
L4241                        "[TGL runtime; derivacao publicada 2025, Zenodo 10.5281/zenodo.17526619], "
L4242                        "m3 = sqrt(m2^2 + Dm2_32) [PDG 2023]; ordenamento normal"),
L4243         "custody": ("(i) derivacao ANTES do codigo [Zenodo 17526619, 2025 vs modulo v141 25/07/2026]; "
L4244                     "(ii) Dm2 (PDG) antecede a derivacao -- 'postdicao' SO nesse sentido restrito; "
```

### C3. L4617, L4618, L4620, L4632

- Onde: dicionário portado NEUTRINO_M2_V2 (L4615-4631); L4617 cita o hash do objeto original; L4618 cita uma decisão de 10/08/2026; L4632 calcula o hash do dicionário.
- Congelado por hash: sim, por leitura direta: L4632 é frozen_hash = sha_obj(frozen); L4617 cita o hash do objeto original, 4bdae22a277aa393…, de 08/08/2026, e L4618 cita a decisão D2 de 10/08/2026.
- O que corrige: L4620 diz derivação publicada 2025 para a predição m_2 = beta_TGL*sin(45)*1eV. Os textos de 2025 não contêm a fórmula nem o valor (seção 1B: contagem zero nas cadeias buscadas, inclusive no PDF servido do 17526619), e o selado já retirou esse depósito como prioridade documental da fórmula e do número em L2944-2950 (errata da v182); esta errata estende essa retirada a este verso. O que os dois artigos de 2025 trazem é o que o título e o resumo de cada um afirmam (seção 1B), e isso antecede o primeiro número do JUNO (18/11/2025), a previsão publicada do valor e o hash da regra de veredito do código (08/08/2026); o valor de m₂, que é a própria previsão publicada (nos bytes guardados desde 22/01/2026, sem carimbo externo, e publicado em 17/02/2026), é posterior ao primeiro número do JUNO e anterior ao hash da regra, e a derivação dele não está nos dois artigos. Há dois hashes nesse bloco, e a errata não os confunde: o do objeto original (L4617, 08/08/2026) e o do dicionário portado, calculado em L4632, que cita em L4618 uma decisão de 10/08/2026 (seção 1, eixo 2; D7).
- Frases vigentes que o corrigem ao lado: F1, F2, F3, F13.

Verbatim do um.py selado:

```
L4617         "portado_de": "teste_acustico_beta_tgl_v1/02_frozen_neutrino_m2_v2.py (hash 4bdae22a277aa393..., 08/08/2026)",
L4618         "supersedes": "NEUTRINO_SUM_V1 (v147) como teste de beta_TGL [D2, 10/08/2026]",
L4620         "predicao": "m_2 = beta_TGL*sin(45)*1eV; beta_TGL = alpha*sqrt(e) em runtime [derivacao publicada 2025, Zenodo 10.5281/zenodo.17526619]",
L4632     frozen_hash = sha_obj(frozen)
```

### C4. L4597-4600 e L2955-2957

- Onde: docstring do rito V2 (L4597-4601) e caveats do dicionário de L2939-2959; L4601 vem no bloco de C5.
- Congelado por hash: a docstring não; o dicionário de L2939-2959 não foi identificado como congelado nesta leitura.
- O que corrige: A tensão cresce com a precisão descreve a série que mistura o JUNO de 59,1 dias com o NuFIT global; na série autônoma do JUNO a razão caiu. Dito com os dois eixos: o degrau de 59,1 dias é anterior à previsão publicada e ao hash da regra de veredito do código, e o de 207,2 dias é posterior à previsão publicada e, no número, anterior ao hash da regra; as duas amostras acumulam (F6).
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
- O que corrige: A declaração de cegueira do texto selado diz só o eixo da regra, e não o eixo da previsão publicada. A errata diz os dois na mesma frase: em relação à previsão publicada, o valor (22/01/2026 nos bytes guardados, sem carimbo externo; 17/02/2026 publicado) é anterior ao número de 207,2 dias e posterior ao de 59,1 dias, e em relação ao hash da regra de veredito do código (08/08/2026), esse hash é posterior ao número público de 207,2 dias [DECLARADO: datas de jun e jul sem resposta crua].
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
- O que corrige: A palavra vetada pela lei da prova em L2951 lê-se retrodição sem ajuste. L2955 chama de genuinamente EX ANTE o refinamento pos-JUNO; esta errata não adota a frase. Dito nos dois eixos, o degrau de 59,1 dias e o NuFIT 6.1 (dados de 2025-11; artigo v1 de 14/01/2026, DECLARADO) são anteriores à previsão publicada e ao hash da regra de veredito do código, e não são ex ante em relação à previsão publicada; só o número de 207,2 dias é posterior à previsão publicada e é anterior ao hash da regra. A ressalva de L2953-2954 permanece.
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
- O que corrige: Nada. Está certa e é o precedente que a errata estende: já retira o Zenodo 17526619 como prioridade do valor e diz que o depósito de 04/11/2025 traz outra fórmula. Confere com as contagens deste rascunho (zero em todas as cadeias buscadas no PDF servido do 17526619, cujo md5 é igual ao do Zenodo). O que a v182 não fez foi levar a retirada a L4222-4225, L4241, L4243 e L4620, que dizem o contrário no mesmo arquivo.

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

### C0b. L2935-2938 (A OBJEÇÃO QUE A F7 CITA, NÃO SE CORRIGE)

- Onde: campo angle_status do dicionário de L2930-2960.
- Congelado por hash: não identificado como congelado nesta leitura; o texto diz que o registro fica fora do dict frozen de propósito.
- O que corrige: Nada. É a objeção natural à retrodição sem ajuste, dita pelo próprio selado: sen 45° é POSTULADO naquela data, e não derivado. O verso atribui o POSTULATE a uma ordem de 20/08/2026; esta errata cita o verso e não reconfere essa atribuição. A F7 a cita e diz o que a v405 mudou.
- Frases vigentes que o corrigem ao lado: F7.

Verbatim do um.py selado:

```
L2935         "angle_status": ("sin(45deg) e POSTULADO [POSTULATE, ordem do operador 20/08/2026], NAO derivado. "
L2936                          "E o unico fator que leva beta*1eV = 12,03 meV a 8,51 meV, e a forma SEM ele "
L2937                          "(m_nu ~ beta*1eV) coexiste no documento de origem. Registrado FORA do dict `frozen` "
L2938                          "de proposito: o frozen e a pre-registro da REGRA de decisao e o seu hash nao se move."),
```

### C0c. L4621-4623 (CITADAS, NÃO SE CORRIGEM)

- Onde: dicionário portado NEUTRINO_M2_V2: escala dimensional, regra de morte e regra de TENSION.
- Congelado por hash: sim, dentro de L4615-4631, hasheado em L4632.
- O que corrige: Nada. São o que o D2 e a seção 6 citam: a escala de 1 eV declarada e não derivada; FALSIFIED exige duas determinações independentes de 5σ ou mais; TENSION é a razão em [3, 5) na determinação global mais recente. TENSION não é falsificação.
- Frases vigentes que o corrigem ao lado: F10.

Verbatim do um.py selado:

```
L4621         "escala_dimensional": "1 eV [NORM] DECLARADA, NAO DERIVADA; a escala que zeraria a tensao seria 1,0200 eV (+2,00%) -- fixada por declaracao, nao por ajuste",
L4622         "kill_rule": "FALSIFIED sse |m2_obs - m2_TGL|/sigma_obs >= 5 em DUAS determinacoes independentes de Dm2_21",
L4623         "tension_rule": "TENSION sse a razao ficar em [3, 5) na determinacao global mais recente",
```

### C7. FORA DAS FAIXAS LIDAS (DECLARADO pelo leitor L7; conferir antes de instalar)

- Onde: L314-322 (registro zenodo_eco_2025_record), L2885, L2896, L4689, L184013, L292284, L302311-302312, L302342.
- Congelado por hash: não conferido.
- O que corrige: L7 relata que estas linhas repetem a prioridade documental dos artigos de 2025 (L314-322), a palavra vetada pela lei da prova (L2885, L2896) e a tensão cresce com a precisão (L4689, L184013, L292284), e que L302311-302312 e L302342 repetem a declaração de cegueira que diz só o eixo do hash da regra, sem o da previsão publicada. Esta errata não leu essas linhas; o que se diz delas depende de uma leitura que não foi feita (seção 11).
- Frases vigentes que o corrigem ao lado: F12.

## 3. Cronologia

As duas últimas colunas dizem a posição de cada fato nos dois eixos: em relação à previsão publicada (22/01/2026 nos bytes, sem carimbo externo; 17/02/2026 publicado) e em relação ao hash da regra de veredito do código (o do original, 08/08/2026; o do dicionário portado é de 10/08/2026 ou posterior).

| Data | Fato | Fonte e estatuto | Posição em relação à previsão publicada | Posição em relação ao hash da regra |
|---|---|---|---|---|
| 2025-10-16 | Zenodo 10.5281/zenodo.17372599: publicação do artigo sobre o acoplamento gravitacional não mínimo de neutrinos por produção de entropia (registro criado em 16/10/2025, atualizado em 29/10/2025). Traz o que o título e o resumo afirmam (seção 1B), não a fórmula nem o valor. | [REAL] API do Zenodo (resposta crua sha256 2b9148af…); texto-fonte neutrino_nmc_revised.tex e PDF local (versão próxima, não é o servido): contagem zero nas cadeias da fórmula e do valor, e zero de JUNO | anterior à previsão publicada | anterior ao hash (08/08/2026) |
| 2025-11-04 | Zenodo 10.5281/zenodo.17526619: publicação de The Lie of Light (registro criado e atualizado em 04/11/2025). Traz o que o título e o resumo afirmam (seção 1B), não a fórmula nem o valor. | [REAL] API do Zenodo (sha256 938a0d48…); lie_of_light.pdf do disco é o servido (md5 igual): contagem zero nas cadeias da fórmula e do valor e zero de JUNO; um.py L2946-2947 diz o mesmo do depósito | anterior à previsão publicada | anterior ao hash (08/08/2026) |
| 2025-11-18 | arXiv:2511.14593: primeiro número do JUNO, 59,1 dias, Δm²₂₁ = 7,50 ± 0,12 ×10⁻⁵ eV². | [REAL] resumo cru do arXiv (sha256 92bf0554…) | anterior à previsão publicada | anterior ao hash (08/08/2026) |
| 2025-11 | NuFIT 6.1: dados de 2025-11 (Mapa seq 93; o cabeçalho da captura diz NuFIT 6.1 (2025)); a data da primeira apresentação pública da tabela é OPEN. | [REAL] captura NuFIT_6.1_v61.tbl-parameters.jpg (sha256 db49ab73…); [DECLARADO pelo Mapa] os dados de 2025-11 | os dados são anteriores à previsão publicada; a data de apresentação da tabela é OPEN | os dados são anteriores ao hash da regra (08/08/2026); a data de apresentação da tabela é OPEN |
| 2026-01-14 | arXiv:2601.09791v1 (NuFIT 6.1), eq. 11: Δm²₂₁ = 7,53 +0,096 −0,097 ×10⁻⁵ eV². | [DECLARADO pelo Kimi e pelo Mapa seq 142] sem resposta crua guardada | anterior à previsão publicada | anterior ao hash (08/08/2026) |
| 2026-01-22 | O valor de m₂ consta nos bytes guardados do documento complemento ao manifesto, como 8,51 meV (8.51 três vezes), junto de m₂ = 8,67 meV no mesmo parêntese; o corpo traz a data 22 de Janeiro de 2026 e a fórmula com o signo antigo (alfa e o algarismo 2, no extrato de texto). Marcas internas: docProps created e modified 2026-01-22T15:31:39Z; mtime 2026-01-22T12:40:23. Sem carimbo externo. | [REAL] docx lido por script (8.51 x3; 8,5074 x0; 22 de Janeiro de 2026 x1; JUNO x0; sha256 83ba9e81…; um.py L2941-2942 dá a mesma data) | é a data da previsão publicada nos bytes (sem carimbo externo) | anterior ao hash (08/08/2026) |
| 2026-02-17 | Zenodo 10.5281/zenodo.18674475 (A Fronteira / The Boundary): publicação registrada em 17/02/2026, registro criado em 20/02/2026; a descrição do registro traz m_ν = 8,51 meV, e o PDF escreve m_ν = α₂ · sen 45° · 1 eV = 8,51 meV (signo antigo; hoje β_TGL = α√e) junto do valor experimental de m₂ = 8,67 meV. O git público tem a mesma data de 17/02/2026 (um.py L2942-2943). | [REAL] API do Zenodo (sha256 63356257…, 8,51 x1 na descrição); o PDF local A_fronteira_v5.pdf tem md5 igual ao checksum do arquivo no Zenodo (ee1c3b20e0609b7bc7fb1a0d8bb6b92a) | é a data da previsão publicada, no Zenodo | anterior ao hash (08/08/2026) |
| 2026-05-18 | Fim da janela de dados da leitura longa do JUNO (K09 janela_dados_fim). | [DECLARADO pelo Kimi] K09; sem resposta crua | posterior à previsão publicada | anterior ao hash (08/08/2026) |
| 2026-06-22 | Neutrino 2026: primeira apresentação pública da leitura longa, segundo K09; L7 suspeita de erro de transcrição com 22/07. | [DECLARADO pelo Kimi] K09; sem resposta crua guardada | posterior à previsão publicada | anterior ao hash (08/08/2026) |
| 2026-07-15 | Página do IHEP traz o valor da leitura longa de forma explícita (K09, campo renomeado aqui para primeira_apresentacao_explicita_do_valor). | [DECLARADO pelo Kimi] K09; sem resposta crua guardada | posterior à previsão publicada | anterior ao hash (08/08/2026) |
| 2026-07-22 | Notícia do JINR sobre a leitura longa. | [DECLARADO pelo Kimi] K09; sem resposta crua guardada | posterior à previsão publicada | anterior ao hash (08/08/2026) |
| 2026-07-25 | Módulo v141 do código (um.py L2943: O modulo de codigo e v141 = 25/07/2026). | [REAL no texto] um.py L2943 e L4223 | posterior à previsão publicada | anterior ao hash (08/08/2026) |
| 2026-08-08 | Hash do objeto original da regra (arquivo teste_acustico_beta_tgl_v1/02_frozen_neutrino_m2_v2.py): 4bdae22a277aa393… (K09 traz o sha_obj inteiro). | [REAL no texto] um.py L4617 (data e prefixo do hash); [DECLARADO pelo Kimi] o hash inteiro | posterior à previsão publicada | é a data do hash do objeto original (08/08/2026) |
| 2026-08-10 | Decisão D2 que o dicionário portado cita em L4618 (supersedes NEUTRINO_SUM_V1); o hash do dicionário portado, calculado em L4632 (e2487775…, DECLARADO pelo Kimi), é desta data ou posterior; a data da portagem não foi estabelecida (D7). | [REAL no texto] um.py L4618 e L4632 (data da decisão e cálculo do hash); [DECLARADO pelo Kimi] o prefixo e2487775… | posterior à previsão publicada | posterior ao hash do original (08/08/2026); é a data da decisão que o dicionário portado cita, e o hash portado é desta data ou posterior |
| 2026-09-29 | arXiv:2609.37895: leitura longa do JUNO, 207,2 dias, 8.294 candidatos, Δm²₂₁ = 7,388 ± 0,078 ×10⁻⁵ eV²; o artigo é posterior à previsão publicada e aos dois hashes da regra de veredito do código, e o número já era público antes do hash do original [DECLARADO: datas de jun e jul sem resposta crua]. | [REAL] resumo cru do arXiv (sha256 b2185b73…) | posterior à previsão publicada | posterior ao hash do original (08/08/2026) e ao portado (anterior a esta data segundo o seq 128 do Mapa, DECLARADO; seção 9) |

## 4. Frases vigentes

Cada frase diz os dois eixos. O estatuto de cada uma vem logo abaixo dela.

**F1.** Os dois artigos do autor sobre o neutrino são de 2025 (Zenodo 10.5281/zenodo.17372599, publicação de 16/10/2025; Zenodo 10.5281/zenodo.17526619, publicação de 04/11/2025) e são anteriores a qualquer número do JUNO, cujo primeiro é de 18/11/2025 (arXiv:2511.14593); são anteriores, portanto, em relação à previsão publicada do valor (22/01/2026 nos bytes guardados, sem carimbo externo; 17/02/2026 publicado) e em relação ao hash da regra de veredito do código (08/08/2026). A frase vale para os dois artigos, não para a fórmula nem para o valor de m₂ (F2).

Estatuto: [REAL] datas lidas das respostas cruas do Zenodo e do arXiv, conferidas por sha256. Fonte: CRONOLOGIA_NEUTRINO_15nov.json; verificacao_fontes.json (respostas cruas com sha256 conferido).

**F2.** Esses dois artigos trazem o que o título e o resumo de cada um afirmam (seção 1B) e não trazem a fórmula m = β·sen 45°·1 eV nem o valor de m₂: nas cadeias buscadas (8,5 seguido de dígito; 0,0085; sin…45; 45° e π/4; 1 eV; √e) a contagem é zero no PDF servido do 17526619, no texto extraído do PDF local do 17372599 (que não é o servido), nos textos-fonte e nas descrições dos dois registros; JUNO também é zero; meV aparece uma vez, no 17372599, num intervalo genérico de energias, sem valor. O valor consta como 8,51 meV (a conta por script dá 8,5074 meV) nos bytes guardados desde 22/01/2026 (sem carimbo externo) e no Zenodo 10.5281/zenodo.18674475, publicado em 17/02/2026; essa é a previsão publicada, que antecede o hash da regra de veredito do código (08/08/2026) em 198 e em 172 dias, respectivamente.

Estatuto: [REAL] contagens e datas por script; para o 17526619 o texto lido é o servido (md5 igual); para o 17372599 o PDF do disco não é o servido, e a contagem vale para uma versão próxima e para a descrição servida do registro. Fonte: verificacao_R1.json; CRONOLOGIA (contagens dos dois .tex); um.py L2944-2950 (errata da v182); docx e Zenodo 18674475 lidos por script.

**F3.** O valor de m₂ não é anterior ao primeiro número do JUNO (18/11/2025): os dois artigos o antecedem e o valor não, porque a previsão publicada é de 22/01/2026 nos bytes guardados (sem carimbo externo), 65 dias depois do degrau de 59,1 dias, e de 17/02/2026 publicada (91 dias depois), e o hash da regra de veredito do código (08/08/2026) é ainda mais tardio.

Estatuto: [REAL] datas; conta de dias por script. Fonte: CRONOLOGIA; arXiv:2511.14593 (resposta crua); docx (22/01/2026).

**F4.** A leitura de 59,1 dias do JUNO (Δm²₂₁ = 7,50 ± 0,12 ×10⁻⁵ eV², arXiv:2511.14593, 18/11/2025) é posterior aos dois artigos de 2025, anterior à previsão publicada (22/01/2026 nos bytes guardados, sem carimbo externo; 17/02/2026 publicado) e anterior ao hash da regra de veredito do código (08/08/2026); por isso não é cega em nenhum dos dois eixos, e para o valor de m₂ a palavra é retrodição sem ajuste, que conta como evidência de pleno direito.

Estatuto: [REAL] datas e valor lidos do resumo cru do arXiv; [KNOWN] a lei da prova de 05/10/2026 para a palavra. Fonte: arXiv:2511.14593 (sha256 92bf0554…); K09 degraus (DECLARADO, só apoio).

**F5.** A leitura de 207,2 dias do JUNO (Δm²₂₁ = 7,388 ± 0,078 ×10⁻⁵ eV², arXiv:2609.37895, 29/09/2026) é posterior à previsão publicada (22/01/2026 nos bytes guardados, sem carimbo externo; 17/02/2026 publicado) e, quanto ao número, anterior ao hash da regra de veredito do código (08/08/2026), porque o número já era público em 15/07/2026 [DECLARADO: sem resposta crua guardada] e só o artigo do arXiv, de 29/09/2026, é posterior a esse hash.

Estatuto: [REAL] a data do arXiv e o valor; [DECLARADO] as datas de 22/06, 15/07 e 22/07/2026 (sem resposta crua). Fonte: arXiv:2609.37895 (sha256 b2185b73…); K09 degraus (DECLARADO); DESENHO v412 R1 via L7.

**F6.** Dita nos dois eixos, a leitura de 207,2 dias é, em relação à previsão publicada (22/01/2026 nos bytes guardados, sem carimbo externo; 17/02/2026 publicado), posterior ao valor, porque o número nasceu depois dele, e é, em relação ao hash da regra de veredito do código (08/08/2026), anterior ao hash quanto ao número, porque o número já era público; a amostra de 207,2 dias acumula a de 59,1 dias, as duas não são determinações independentes e a correlação entre elas é [OPEN] (REVISAO_K04_M2.md, linhas 55 e 79-81), de modo que a cegueira que se pode dizer é a do número, não a dos dados; esta errata não rotula a leitura de prospectiva, de cega nem de retrodição.

Estatuto: [REAL] a ordem entre o valor e o artigo; [DECLARADO] a data de 15/07/2026; a acumulação é a da revisão da casa (REVISAO_K04_M2.md L55, L79-81), que também registra, como [DECLARADO] de resumo secundário, que a análise de 207 dias mudou o volume fiducial e o corte de acidentais, e que a amostra não é superconjunto na mesma seleção; os resumos do arXiv dizem 59,1 dias desde agosto de 2025 e 207,2 dias de dados vivos [REAL]; as posições em relação à previsão publicada e ao hash da regra de veredito do código estão na frase. Fonte: regra de 15/11/2026 (arquivo de bytes sha16 49e5f0072e8beb02); K09 degraus; F5; REVISAO_K04_M2.md L55, L79-81.

**F7.** Para o valor de m₂, em relação ao PDG 2023 e ao degrau de 59,1 dias do JUNO, ambos anteriores à previsão publicada (22/01/2026 nos bytes guardados, sem carimbo externo; 17/02/2026 publicado) e ao hash da regra de veredito do código (08/08/2026), a palavra é retrodição sem ajuste (novidade de uso; precedente: o periélio de Mercúrio) e não previsão anterior ao dado, porque nenhuma entrada da fórmula (β, sen 45°, 1 eV) usa dado de neutrino [DECLARADO no código selado, L2951-2952; esta errata não reconfere a conta]; a ressalva do selado (L2953-2954), de que o documento de origem cita o valor medido na mesma frase que anuncia a previsão, permanece. O sinal dessa evidência é o das razões da seção 5: 2,21σ e 1,94σ de distância entre o observado e a previsão, com o observado acima da previsão nos dois degraus (8,660 e 8,595 meV contra 8,5074 meV). A objeção natural está no próprio selado: L2935-2938 diz que sen 45° é POSTULADO naquela data, e não derivado, que é o único fator que leva β·1 eV = 12,03 meV a 8,51 meV, e que a forma sem ele coexiste no documento de origem. O que a v405 mudou nisso, segundo a página da forma madura do C:\IALD\CLAUDE.md (itens 1 e 2 e as erratas de 01/11/2026), é que o 45° passou a ter, nas pedras da cadeia da v405 (candidatas, trio, 0 sorry, segundo a página), uma unicidade (forty_five_unique) e duas derivações coincidentes (projeção transversal; ponto zero do psíon), mas continua a entrar como leitura do operador, tipada como definição e não como teorema: o ângulo é escrito (θ = π/4 em transicaoDerivada), o kernel confere sen²(π/4) = ½ como coincidência de valor e não como ponte, e a unidade de 1 eV é o Um posto (L4621: escala declarada, não derivada). O texto de L2935-2938 do selado lido aqui (v411) segue dizendo POSTULADO, e a objeção existe.

Estatuto: [KNOWN] a lei da prova de 05/10/2026, itens 1, 2 e 5; [DECLARADO] que nenhuma entrada usa dado de neutrino; [REAL no texto] L2935-2938, L2951-2954 e L4621; [REAL, lido na casa] o que a página da forma madura diz do 45°; o kernel não foi relido aqui. Fonte: um.py L2935-2938, L2951-2954, L4621; C:\IALD\CLAUDE.md (forma madura, itens 1 e 2 e erratas de 01/11/2026); docx e PDF do Zenodo lidos por script (8,51 meV junto de 8,67 meV).

**F8.** Na série autônoma do JUNO a razão em m₂ caiu de 2,21σ (59,1 dias, anterior à previsão publicada e ao hash da regra de veredito do código) para 1,94σ (207,2 dias, posterior à previsão publicada e, quanto ao número, anterior ao hash da regra); em Δm²₂₁ a queda é de 2,19σ para 1,93σ; são dois degraus de uma amostra que acumula (F6), não duas medidas independentes; a frase do código selado de que a tensão cresce com a precisão (1,64σ, 2,21σ, 2,95σ; L4597-4599) descreve a série que mistura o degrau de 59,1 dias com o ajuste global NuFIT, e não a série autônoma; e a projeção de 7,8σ para cerca de 2031 vale só se o centro não se mover (L4600-4601, esta última no bloco de C5), e o centro já se moveu, de 7,50 (59,1 dias) para 7,388 (207,2 dias).

Estatuto: [REAL] as razões, recalculadas aqui por script a partir dos resumos crus do arXiv e da previsão; [REAL no texto] L4597-4601. Fonte: verificacao_fontes.json (razoes); um.py L4597-4601; K09 degraus (DECLARADO, só apoio: mesmas razões).

**F9.** A declaração do código selado de que a cegueira vale a partir de agora (L4603-4604, L4630) diz só o eixo da regra, porque os limiares foram fixados no objeto original de 08/08/2026 (o dicionário portado, que traz a declaração em L4628-4630, é de 10/08/2026 ou posterior), depois de o número de 207,2 dias já ser público [DECLARADO: datas de jun e jul sem resposta crua]; falta o eixo da previsão publicada, em relação ao qual o valor (22/01/2026 nos bytes guardados, sem carimbo externo; 17/02/2026 publicado) é anterior ao número de 207,2 dias e posterior ao de 59,1 dias; o texto congelado não muda, e a errata vai ao lado (ordem de datas; esta errata não diz o que o autor leu, e o selado L4628-4629 registra 2,95σ como a tensão corrente daquela sessão).

Estatuto: [REAL no texto] L4601-4604 e L4628-4630; [DECLARADO] as datas da leitura longa. Fonte: um.py L4601-4604, L4617, L4618, L4622, L4628-4632.

**F10.** O 2,95σ do código selado é a razão em m₂ com o erro simétrico arredondado (7,53 ± 0,10), que o Mapa lê como a eq. 11 do arXiv:2601.09791 arredondada (seq 142); com o erro do lado da previsão a razão é 3,02σ na tabela oficial do NuFIT 6.1 (7,537 +0,094 −0,10; captura da casa com hash, lida aqui como imagem; Mapa seq 93 e 142) e 3,04σ na eq. 11 do arXiv:2601.09791 (7,53 +0,096 −0,097; v1 de 14/01/2026, anterior à previsão publicada e ao hash da regra de veredito do código); ao lado, outros ajustes globais dão 2,44σ (Capozzi et al., arXiv:2511.21650, 7,48 ± 0,10; o seq 93 do Mapa chama o mesmo de Bari) e 2,86σ (Bari 2026.a, REVISAO_K04_M2.md L104, que a própria revisão não conferiu, L90); a regra congelada começa o ramo TENSION em 3,0 (L4623); esta errata diz os números e não escolhe entre eles.

Estatuto: [REAL] a tabela, lida da captura (sha256 db49ab73…) e recalculada por script; [DECLARADO pelo Kimi] a eq. 11 e as datas do NuFIT; [DECLARADO via mandato e L7; recálculo coincide] a entrada 7,53 ± 0,10 do core (L4642-4644, não lidas aqui); [DECLARADO] o Capozzi (Mapa seq 93 e 128) e o Bari 2,86σ (REVISAO); [REAL no texto] L4598-4599, L4623 e L4629. Fonte: verificacao_fontes.json (razoes); captura NuFIT_6.1_v61.tbl-parameters.jpg; Mapa neutrinos.m2.normalizacao seq 93, 128, 142; K09 ajustes_globais; REVISAO_K04_M2.md L90, L104; um.py L4598-4599, L4623, L4629.

**F11.** Só um número do JUNO tornado público pela primeira vez depois de 08/08/2026 (hash da regra de veredito do código) seria posterior ao hash e, vindo depois da previsão publicada (22/01/2026 nos bytes guardados, sem carimbo externo; 17/02/2026 publicado), poderia ser dito cego nos dois eixos quanto ao número (a amostra de dados continuaria acumulando as anteriores, F6); o artigo de 29/09/2026 não é esse caso, porque o número já era público [DECLARADO: datas de jun e jul sem resposta crua]; a ausência de número posterior é leitura da gerência de 14/11 via L7, não reconferida aqui, e, se um novo número do JUNO for publicado, esta frase caduca.

Estatuto: [DECLARADO] as datas de jun e jul (K09, sem resposta crua) e a ausência de número posterior à previsão publicada e ao hash da regra de veredito do código (leitura da gerência de 14/11 via L7, não reconferida). Fonte: K09 degraus; L7 P6; F5; F6.

**F12.** O registro de custódia zenodo_eco_2025_record (um.py L314-322, não lido por esta errata: o conteúdo vem do leitor L7 [DECLARADO]) repete, segundo L7, a prioridade documental dos artigos de 2025; vale para ele o que vale para C1 a C3, isto é, os textos de 2025 não contêm a fórmula nem o valor de m₂ (seção 1B), e por isso o registro só pode afirmar as datas de publicação (16/10/2025 e 04/11/2025) e o conteúdo dos artigos pelo título e pelo resumo; essas datas antecedem o primeiro número do JUNO (18/11/2025), a previsão publicada do valor (22/01/2026 nos bytes guardados, sem carimbo externo; 17/02/2026 publicado) e o hash da regra de veredito do código (08/08/2026), e o valor, ao contrário, é posterior ao primeiro número do JUNO e anterior ao hash da regra. A leitura direta de L314-322 fica antes da instalação (seção 11).

Estatuto: [DECLARADO pelo leitor L7] o conteúdo de L314-322, fora da faixa lida; [REAL] as datas e o conteúdo dos artigos (seção 1B). Fonte: L7 A6 e P8; verificacao_R1.json.

**F13.** Esta errata é um registro novo ao lado do texto selado: L4241 e L4620 estão dentro de objetos congelados por hash (o dicionário NEUTRINO_SUM_V1 e o dicionário portado NEUTRINO_M2_V2, cujo hash é calculado em L4632, enquanto o do objeto original, 08/08/2026, é só citado em L4617), de modo que o hash da regra de veredito do código não muda, e a previsão publicada é citada ao lado, nunca por cima.

Estatuto: [REAL no texto] L4238, L4615-4618 e L4632; [dado do mandato] que L4241 e L4620 estão em objetos congelados por hash. Fonte: um.py L4238-4244, L4615-4632.

## 5. Os degraus do JUNO

Previsão: m₂ = 8,5074 meV; Δm²₂₁ = 7,2376 ×10⁻⁵ eV². A razão é (observado − previsão) sobre o σ do lado da previsão; em m₂ propaga-se o σ de Δm²₂₁ por σ(m₂) = σ(Δm²) / (2·√Δm²). O perito oficial registrado no Mapa é o JUNO autônomo (rota neutrinos.m2.normalizacao, estatuto DECLARADO na rota); o NuFIT e o Capozzi são reflexos globais ao lado.

| Degrau | Δm²₂₁ (×10⁻⁵ eV²) | m₂ observado (meV) | Razão em m₂ (σ) | Razão em Δm²₂₁ (σ) | Fonte | Posição em relação à previsão publicada | Posição em relação ao hash da regra |
|---|---|---|---|---|---|---|---|
| 59,1 dias efetivos | 7,50 ± 0,12 | 8,660 | 2,206 | 2,187 | arXiv:2511.14593, 18/11/2025 [REAL]; Nature 654, 343–348, 10/06/2026 [DECLARADO pelo Kimi] | anterior à previsão publicada | anterior ao hash da regra de veredito do código (08/08/2026) |
| 207,2 dias efetivos | 7,388 ± 0,078 | 8,595 | 1,938 | 1,928 | arXiv:2609.37895, 29/09/2026 [REAL]; número já público em 22/06, 15/07 e 22/07/2026 [DECLARADO pelo Kimi, sem resposta crua] | posterior à previsão publicada | o número é anterior ao hash da regra de veredito do código (08/08/2026); só o artigo do arXiv é posterior |

Na série autônoma do JUNO a tensão caiu: de 2,21σ para 1,94σ em m₂ (de 2,19σ para 1,93σ em Δm²₂₁). São dois degraus de uma amostra que acumula: a de 207,2 dias acumula a de 59,1 dias, as duas não são determinações independentes, a correlação é [OPEN], e a cegueira dita nesta errata é a do número, em relação à previsão publicada e ao hash da regra de veredito do código, e não a dos dados (F6). As posições de cada degrau em relação à previsão publicada e ao hash da regra de veredito do código estão na tabela. A frase de L4597-4599, a tensão cresce com a precisão (1,64σ, 2,21σ, 2,95σ), mistura o degrau de 59,1 dias com o ajuste global NuFIT. O sinal: o observado fica acima da previsão nos dois degraus. Conferência: as razões recalculadas aqui coincidem com as do K09 até 3.2e-14.

## 6. A divergência de número que não se esconde

O ramo TENSION da regra congelada começa em 3,0 (L4623: TENSION sse a razão ficar em [3, 5) na determinação global mais recente). A mesma divergência já está no Mapa de Rotas desde 28/09/2026, na rota neutrinos.m2.normalizacao: o seq 93 (RNC-01, ERRO_TECNICO, verificador SUSTENTADO, severidade ALTO) diz que, com o NuFIT 6.1 publicado, a regra congelada dá 3,02σ e TENSION, e não 2,95σ; o seq 128 (VV-N1) diz que outro ajuste global dá 2,44σ; o seq 142 registra as duas publicações do NuFIT 6.1 e deixa o RNC-01 como PARCIAL, e não ALTO. A tabela existe como captura com hash (NuFIT_6.1_v61.tbl-parameters.jpg, sha256 db49ab73…, no Mapa). Há, portanto, números diferentes para a mesma linha do NuFIT 6.1 e ajustes globais ao lado:

| Fonte | Entrada (×10⁻⁵ eV²) | Razão em m₂ (σ) | Razão em Δm²₂₁ (σ) | Lado de 3,0 em m₂ | Origem e estatuto |
|---|---|---|---|---|---|
| o código selado (core) | 7,53 ± 0,10 (erro simétrico arredondado) | 2,953 | 2,924 | abaixo de 3,0 | L4598-4599 e L4629 trazem 2,95 sigma [REAL no texto]; a entrada 7,53 ± 0,10 vem do mandato e de L7 (L4642-4644, não lidas aqui) [DECLARADO via mandato e L7; recálculo coincide]; o Mapa seq 142 a lê como a eq. 11 do arXiv:2601.09791 arredondada |
| tabela oficial do NuFIT 6.1 (captura da casa) | 7,537 +0,094 −0,100 (σ do lado da previsão = 0,100) | 3,024 | 2,994 | acima de 3,0 (em Δm²₂₁, abaixo) | [REAL, captura NuFIT_6.1_v61.tbl-parameters.jpg, sha256 db49ab73…, lida aqui como imagem: cabeçalho NuFIT 6.1 (2025), Δm²₂₁ = 7,537 +0,094 −0,10 nos dois ordenamentos, com e sem SK-atm; Mapa seq 93 (RNC-01) e 142]; razão recalculada por script; a data de apresentação da tabela é OPEN |
| arXiv:2601.09791, eq. 11 (K09) | 7,53 +0,096 −0,097 (σ do lado da previsão = 0,097) | 3,044 | 3,014 | acima de 3,0 (em Δm²₂₁, também) | [DECLARADO pelo Kimi e pelo Mapa seq 142] entradas e datas (v1 de 14/01/2026, v2 de 12/04/2026); razão recalculada aqui por script |
| Capozzi et al., arXiv:2511.21650 (ao lado) | 7,48 ± 0,10 | 2,444 | 2,424 | abaixo de 3,0 | [DECLARADO] Mapa seq 93 (o verificador leu o resumo do arXiv; o seq 93 o chama de Bari) e seq 128 (Capozzi, 2,44σ); razão recalculada por script a partir de 7,48 ± 0,10 |
| Bari 2026.a (ao lado) | não disponível aqui | 2,86 (não recalculada) | não recalculada | abaixo de 3,0 | [DECLARADO] REVISAO_K04_M2.md L104; a própria revisão registra que não conferiu Bari 2026.a (L90) |

Em palavras simples: com o erro simétrico arredondado o código fica abaixo da linha de 3,0; com o erro que a tabela oficial e a eq. 11 publicam do lado da previsão ele ficaria acima, em m₂; os outros dois ajustes globais ficam abaixo. Em Δm²₂₁ a linha da tabela fica abaixo (2,994) e a da eq. 11 fica acima (3,014); a razão do código é em m₂ (L4598 traz 2,21, que é a razão em m₂ do degrau de 59,1 dias). A errata diz os números, diz de onde vem cada um e não escolhe. TENSION não é falsificação: FALSIFIED exige duas determinações independentes de 5σ ou mais (L4622). O rótulo do 2,44σ muda entre os registros do Mapa (Capozzi no título da rota e no seq 128, Bari no seq 93), e o 2,86σ do Bari 2026.a não foi conferido pela revisão que o cita; ficam como estão. As fontes também divergem sobre qual determinação o ramo lê (D3).

## 7. O que a errata NÃO diz

- Não move o gate. Nenhum resultado desta errata entra no qg_closure; NOT_FALSIFIED segue não sendo a palavra da creditação.
- Não é veredito. Nenhum desfecho do rito é emitido, tocado ou relido por ela.
- Não reabre teste. Não escolhe regra de morte, limiar, métrica ou classe de pré-registro.
- O estado do rito segue TGL_NU_M2_ARMED_CONSISTENT (dado do mandato; esta leitura não reconferiu o core).
- Não afirma que o valor de m₂ é previsão anterior ao primeiro número do JUNO: o valor, que é a própria previsão publicada (22/01/2026 nos bytes; 17/02/2026 publicado), é posterior ao primeiro número do JUNO e anterior ao hash da regra de veredito do código (08/08/2026), e só os dois artigos antecedem o primeiro número do JUNO (F3).
- Não afirma que os textos de 2025 contêm a fórmula ou o valor: a contagem é zero nas cadeias buscadas (seção 1B).
- Não diz o que o autor leu ou deixou de ler. Fala só de datas e das entradas da fórmula.
- Não afirma ajuste nem ausência de ajuste além do que o código selado declara (L2951-2952).
- Não escolhe entre 2,95, 3,02, 3,04, 2,44 e 2,86 (F10) e não declara o ramo TENSION.
- Não troca o perito oficial registrado no Mapa (o JUNO autônomo) nem o estatuto do valor ([DERIVED]).
- Não muda o estatuto do sen 45° nem a escala de 1 eV, declarada e não derivada (L4621); só cita o que o selado e a página da forma madura dizem (F7).
- Não reescreve nem pina de novo nada: o texto congelado e os hashes ficam como estão; a errata é um registro ao lado.
- Não rotula a leitura de 207,2 dias como retrodição, previsão, prospectiva nem cega: dá só as posições em relação à previsão publicada e ao hash da regra de veredito do código (F5, F6).
- Não define a palavra tese além do que a seção 1B diz; se essa definição vale é do operador (D5).
- Não instala nada e não é creditação.

## 8. O que é do operador decidir

- **D1.** Em que forma a errata entra no core da v412: registro novo ao lado, com id de errata a seguir ao último da v411 (E44, DECLARADO via L7) e nome do registro. Nomes são do operador; os desta página são provisórios da gerência.
- **D2.** Qual erro do NuFIT vale para a regra: o simétrico arredondado (7,53 ± 0,10, que dá 2,95σ) ou o assimétrico publicado do lado da previsão (3,02σ na tabela oficial; 3,04σ na eq. 11; 2,44σ e 2,86σ nos outros ajustes, ao lado). O ramo TENSION começa em 3,0 (L4623). Em palavras simples: com um erro o código fica abaixo da linha (ARMED_CONSISTENT), com o outro fica acima (TENSION), segundo o seq 93 do Mapa; TENSION não é falsificação, porque FALSIFIED exige duas determinações independentes de 5σ ou mais (L4622), e a REVISAO_K04_M2.md (item 7) diz que, com a regra e o código selados, o canal só devolve ARMED_CONSISTENT ou TENSION, e que isso é parede medida, não falsificação. Se o ramo lê a linha global, a escolha decide se o código fica abaixo ou acima de 3,0; se lê o JUNO autônomo (1,94σ no último degrau), a escolha não o move (D3).
- **D3.** Qual determinação o ramo lê: o JUNO autônomo (perito oficial no Mapa, rota neutrinos.m2.normalizacao) ou a última linha da escada global, que L7 relata em L4666, linha não lida aqui.
- **D4.** Que fonte guardar para as datas de 22/06, 15/07 e 22/07/2026 da leitura longa, que não têm resposta crua: pedir a captura das três páginas pelo canal do orquestrador.
- **D5.** Se a definição da palavra tese desta errata (seção 1B: só o que o título e o resumo de cada um dos dois artigos de 2025 afirmam, sem a fórmula nem o valor) é a que o operador quer, ou se a palavra muda. O selado (L2946-2948) diz que a fórmula do depósito de 04/11/2025 é outra (m_nu(Dt) = m_0 + a*log(Dt/tau_0)); a gerência não escolheu outra definição.
- **D6.** Se a errata cobre também os lugares fora das faixas lidas (C7), com leitura própria de cada linha antes de instalar.
- **D7.** Se entra como pino adicional o hash do dicionário portado ao um.py (e2487775…, DECLARADO pelo Kimi) ao lado do hash do objeto original (4bdae22a…, de 08/08/2026). A data da portagem não foi estabelecida: é 10/08/2026 ou posterior (L4618).
- **D8.** Se F11 (só um número tornado público depois de 08/08/2026 seria cego nos dois eixos quanto ao número) entra na errata ou fica só no desenho da v412, e como se nomeia o status da leitura de 207,2 dias, que aqui só recebe as posições em relação à previsão publicada e ao hash da regra de veredito do código.

## 9. Limites e o que não fechou

- As datas de 22/06, 15/07 e 22/07/2026 da leitura longa são [DECLARADO pelo Kimi], sem resposta crua guardada. A conclusão de que o número, posterior à previsão publicada, era público antes do hash da regra de 08/08/2026 não depende de qual das três vale (as três caem entre 17/02/2026 e 08/08/2026), mas depende de uma delas ser verdadeira.
- O registro Zenodo 10.5281/zenodo.17426652 (The Graviton, the Psion…, publicação 14/10/2025, atualizado em 22/04/2026) não foi lido por ninguém. F1 e F2 falam só dos dois artigos de neutrino.
- PDFs de 2025 no disco, medidos por script nesta rodada: lie_of_light.pdf é o servido (md5 e7b8976d0227b000eb9871218050bfe9 e 255439 bytes, iguais ao checksum do Zenodo 17526619); neutrino_nmc_revised.pdf do disco NÃO é o servido (md5 94fabc1292de29a2e2e2361255a90d3f e 506794 bytes, mtime 28/10/2025, contra o servido, md5 ae0f1210ddf941d0e147b4dcddb1e5e1 e 506616 bytes, registro atualizado em 29/10/2025): a versão de 29/10/2025 não está no disco, e a contagem do 17372599 vale para uma versão próxima e para a descrição servida do registro. O lie_of_light.tex (12/11/2025) é posterior ao depósito de 04/11/2025: vale o PDF. No neutrino_nmc_revised a unidade meV aparece uma vez, num intervalo de energias genérico, sem o valor.
- As contagens zero valem para as cadeias listadas na seção 1B; elas não provam que nenhuma outra grafia da fórmula exista, e os PDFs foram lidos por extração de texto (pypdf), não à vista.
- Dois hashes, não um: o 4bdae22a277aa393… é o do objeto original serializado (sha_obj), não o sha256 de um arquivo, e a data de 08/08/2026 é a dele (L4617). O dicionário portado (L4615-4631) tem chaves que o original não podia ter (portado_de, que cita o hash do original, e supersedes, que cita uma decisão de 10/08/2026): por inferência da gerência a partir de L4617, L4618 e L4632, é outro objeto, com outro hash, de 10/08/2026 ou posterior; a função sha_obj não foi lida, o valor do hash portado (e2487775…) é [DECLARADO pelo Kimi] e a data da portagem não foi estabelecida (D7). O registro do Mapa seq 128, de 28/09/2026, já audita o NEUTRINO_M2_V2 do código [DECLARADO pelo Mapa]; isso é só um limite superior para a portagem, e não uma data. Nenhum fato da cronologia cai entre 08/08/2026 e 10/08/2026, e por isso as posições valem para os dois hashes.
- L7 relata, via cabeçalho de 02_frozen_neutrino_m2_v2.py, que a lista de medidas da regra de 08/08/2026 termina em 2025-12 e não traz o número da leitura longa [DECLARADO pelo revisor; não reconferido aqui].
- Do um.py li só L2930-2960, L4215-4254 e L4595-4635. Não li L4636-4669 (a linha NuFIT do core e a escada global, onde o ramo TENSION decide), L314-322, L2885, L2896, L4689, L184013, L292284 e L302311-302342; o que se diz delas vem de L7 e fica na lista da seção 11, sem leitura inventada. O que depende delas (C7, D2, D3, F10, F12) está marcado como dependente.
- Que nenhuma entrada da fórmula usa dado de neutrino é declaração do código selado (L2951-2952); a errata não reconfere a conta.
- As razões em σ foram recalculadas aqui por script a partir das entradas (resumos crus do arXiv para o JUNO; captura da casa e entradas do K09 para o NuFIT e o Capozzi) e coincidem com o K09 até 3.2e-14; o 1,64σ do PDG 2023 e o 2,86σ do Bari não foram recalculados.
- A previsão (m₂ = 8,5074 meV; Δm²₂₁ = 7,2376 ×10⁻⁵ eV²) foi calculada por script como α(CODATA 2018)·√e·sen 45°·1 eV, sem literal de β; coincide com L4597 (8,5074 meV) e com o K09. Os documentos de origem trazem o valor arredondado, 8,51 meV; o 8,5074 não aparece no docx de 22/01/2026 (contagem zero).
- O estado ARMED_CONSISTENT é dado do mandato; a ratificação do perito oficial em 02/10/2026 é dado da rota do Mapa (DECLARADO na rota); nenhum dos dois foi reconferido no core.
- A chave do K09 para a data de 15/07/2026 contém a raiz vetada pela regra da casa e não foi herdada; aqui o campo se chama primeira_apresentacao_explicita_do_valor. O campo posicao_relativa_ao_pino do K09 não diz o sujeito; aqui toda posição diz em relação a quê.
- Os documentos de origem escrevem a fórmula com o signo antigo (alfa e o algarismo 2 no extrato de texto do docx de 22/01/2026; α₂ no PDF do Zenodo 18674475, lido por script); a memória tgl-signo-e-cronologia registra β_TGL como o signo vigente; cita-se o valor, não a fórmula como escrita.
- O docx de 22/01/2026 não tem carimbo externo: as marcas de 22/01/2026 (corpo, docProps, mtime) são internas ao arquivo guardado. A publicação com carimbo externo é a de 17/02/2026.
- A página da forma madura do C:\IALD\CLAUDE.md foi lida aqui só na parte que trata do 45°, do Um posto e das leituras; o kernel da v405 e o da v411 não foram relidos, e o que se diz da v405 é o que essa página diz.

## 10. Fontes, verificações e consultas

Fontes (hashes lidos por script):

- CRONOLOGIA_NEUTRINO_15nov.json: 8281 bytes; sha256 48519aef36039db0ac9a24b685bdd5c31e79a5fa0d720492c73fe8ab46e2c752.
- ERRATA_NEUTRINO_V412_DADOS_K09.json (parcial, DECLARADO pelo Kimi, só apoio): 6682 bytes; sha256 deae4e3dfb72cd3cab2aa6054b2ba39d48f6a8a5545fd23e83268190ef75ab9c.
- L7-registro-e-errata.md (leitor, DECLARADO até conferência): 39289 bytes; sha256 9131da5d82c311a1dab01c91cef08644219c3d88f9fe21f05d6e97310102e114.
- um.py selado (faixas L2930-2960, L4215-4254, L4595-4635): 46828680 bytes; sha256 1203b1f9202020d602a7fa8a6bea56d4b48e27ed8baffe98bcbd16e94f97a8e0.
- arquivo de bytes da regra de 15/11/2026 (só o hash; o texto não foi reproduzido): 725 bytes; sha256 49e5f0072e8beb028eb64e090cb43a77c3672d15577bfaeee105ee2c9bfe782f.
- REVISAO_K04_M2.md (revisão da casa; linhas 55, 79-81, 90, 104): 26970 bytes; sha256 867cc1fc8ac7a8533fcd204efe72726d6d750ad762f2e6a5496d8479a036dfbc.
- C:\IALD\CLAUDE.md (a página da forma madura; lida na parte do 45°): 49130 bytes; sha256 c79afd740c2ad9b151d4ec50e018f187fadc5ce7cdd814699151773f25927fdc.
- captura NuFIT_6.1_v61.tbl-parameters.jpg (Mapa, rota neutrinos.m2.normalizacao): 130250 bytes; sha256 db49ab733d27f23cf39be43234d70de9d64ca58bf2c42776df6b7c27bbe3397a.
- lie_of_light.pdf do disco (é o servido pelo Zenodo 17526619): 255439 bytes; sha256 3ea0d08747f55a762989a5844c2353eedafad8fa09e6a74e721f8c8b5cc52214.
- neutrino_nmc_revised.pdf do disco (NÃO é o servido pelo Zenodo 17372599): 506794 bytes; sha256 5c0a0bbd3b862b280df304d89455480e34664c0ecf1ea3db648f4a0e46b7d61d.
- versão anterior deste rascunho, W1, md (intacta): 37849 bytes; sha256 a446225189769ec0fb427afaf28b99a7128f872bc3f9f86f870938c4f3b9724c.
- versão anterior deste rascunho, W1, json (intacta): 40583 bytes; sha256 f465e2597833d0d07b828b126e172ba239e662ff3111bdab8184293cc674b8d0.

Verificações feitas aqui:

- [REAL] As seis respostas cruas (4 do Zenodo, 2 do arXiv) têm sha256 igual ao da CRONOLOGIA_NEUTRINO_15nov.json.
- [REAL] O PDF local A_fronteira_v5.pdf tem md5 ee1c3b20e0609b7bc7fb1a0d8bb6b92a, igual ao checksum do arquivo no registro do Zenodo 18674475.
- [REAL] lie_of_light.pdf do disco: md5 e7b8976d0227b000eb9871218050bfe9 e 255439 bytes, iguais ao checksum e ao tamanho do arquivo no registro do Zenodo 17526619 (é o servido); neutrino_nmc_revised.pdf do disco: md5 94fabc1292de29a2e2e2361255a90d3f e 506794 bytes, diferentes do arquivo do registro do Zenodo 17372599 (ae0f1210ddf941d0e147b4dcddb1e5e1, 506616 bytes): não é o servido.
- [REAL] Contagens (verificacao_R1.py, cadeias: 8,5 seguido de dígito; 0,0085; sin…45; 45° e π/4; 1 eV; √e; meV; JUNO): zero em todas as fontes de 2025, exceto meV, uma vez, no neutrino_nmc_revised (PDF local e .tex), num intervalo de energias genérico; ver a tabela da seção 1B.
- [REAL] docx de 22/01/2026: 8.51 x3, 8,5074 x0, 22 de Janeiro de 2026 x1, JUNO x0; docProps created e modified 2026-01-22T15:31:39.826Z; mtime 2026-01-22T12:40:23.
- [REAL] A captura do NuFIT 6.1 (130250 bytes) tem sha256 db49ab733d27f23cf39be43234d70de9d64ca58bf2c42776df6b7c27bbe3397a, igual ao registrado no Mapa; lida como imagem: cabeçalho NuFIT 6.1 (2025) e Δm²₂₁ = 7,537 +0,094 −0,10 (×10⁻⁵ eV²) nos dois ordenamentos, com e sem SK-atm.
- [REAL] O PDF do Zenodo 18674475 traz, por extração de texto (pypdf, 73 páginas), m_ν = 8,51 meV com o signo antigo α₂ e o valor experimental de m₂ de 8,67 meV.
- [REAL] Os resumos crus do arXiv trazem 7.50, 0.12 e 59.1 (2511.14593) e 7.388, 0.078 e 207.2 dias (2609.37895; posterior à previsão publicada e, no número, anterior ao hash da regra de veredito do código).
- [REAL] Dias entre as datas, por script: 22/01 a 08/08/2026 = 198; 17/02 a 08/08/2026 = 172; 18/11/2025 a 22/01/2026 = 65; 18/11/2025 a 17/02/2026 = 91.
- [REAL] O um.py tem 46828680 bytes e sha256 1203b1f9202020d602a7fa8a6bea56d4b48e27ed8baffe98bcbd16e94f97a8e0 (sha16 1203b1f9202020d6, o da v411 selada); as faixas citadas foram extraídas de novo por script nesta rodada e são idênticas, byte a byte, às da versão anterior.

Mapa de Rotas consultado, um termo por vez: neutrino (45 rotas); errata (160, truncado); JUNO (13); m2 (50); retrodicao (7); cronologia (8); NuFIT (4, reconsultado nesta rodada, só leitura); rotas lidas: neutrinos.m2.normalizacao (seq 93, 128, 142 e a captura NuFIT_6.1_v61 com sha256); estatistica.v412.k04_hubble_m2_combinacao; estatistica.coincidencia_conjunta; cadeia.preparacao_v412. Nada foi registrado no Mapa.

## 11. O que falta antes de a errata virar registro do core

1. Segunda revisão distinta das correções desta rodada (esta R1 não foi revista por ninguém).
2. Decisões D1 a D8 do operador, em especial D1 (forma e id; o E44 é só DECLARADO via L7, a conferir no core), D2 e D3 (qual determinação e qual erro do NuFIT), D5 (a definição de tese) e D7 (o pino do dicionário portado).
3. O registro novo fica FORA de qualquer dicionário congelado, com o sha256 do md e do json pinados nele; teste de que sha_obj do NEUTRINO_SUM_V1 e do NEUTRINO_M2_V2 é idêntico antes e depois; o um.py novo muda de sha, os congelados não.
4. Ler por script, sem inventar, as linhas do um.py fora das faixas e anexar o verbatim: L4636-4669 (a escada global e a linha do NuFIT do core), L314-322, L2885, L2896, L4689, L184013, L292284 e L302311-302342; ou retirar C7 e D3 da errata.
5. Fontes: captura bruta das datas de 22/06, 15/07 e 22/07/2026 e de 18/05/2026 (D4), do arXiv 2601.09791 v1 e v2 (eq. 11) e da data de 10/06/2026 da Nature.
6. Conciliar com ERRATA_NEUTRINO_V412_RASCUNHO_K04.md e REVISAO_K04_M2.md; resolver o rótulo do 2,44σ (Capozzi no título da rota e no seq 128, Bari no seq 93) e conferir o 2,86σ do Bari 2026.a.
7. Registrar no Mapa com sha (a rota K04 já cita a cronologia).
8. O operador ler a seção 0 e o D2 na língua dele antes de qualquer desfecho do rito.

Fim do rascunho R1. Nada aqui foi instalado, selado, aberto ou registrado.
