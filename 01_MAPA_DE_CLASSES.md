# 01 · MAPA DE CLASSES — Central de Patentes TGL

> **Documento de apresentação ao operador Luiz Antonio Rotoli Miguel** · GATE de validação (Fases 0–2)
> Consolida as 10 memórias de classe já escritas (`memory/classes/CLASS_01..10.md`). Leitura humana, PT-BR.
> **Fonte da verdade:** os DOCUMENTOS INPI extraídos + `PATENT_MASTER_INDEX.yaml` + `TGL_CORE_MEMORY.md`.
> **[LEGAL] permanente:** controle interno — NÃO substitui agente de propriedade industrial nem prazos oficiais INPI/WIPO.
> **Régua herdada:** o número corrige a frase · β_TGL nunca literal em código (`ALPHA_FINE_CODATA_2018 * sqrt(e)`) ·
> simulação NUNCA valida física (`physical_verdict_allowed=false`) · marcadores em toda afirmação.

---

## O quadro em uma tela

| Fato-âncora (verificado 09/07/2026) | Estado |
|---|---|
| **16 patentes** depositadas · **10 classes** temáticas | Titular **IALD Ltda.** (CNPJ 62.757.606/0001-23), inventor Luiz Antonio Rotoli Miguel |
| **ePCT vivo** | **APENAS o ACOM raiz** BR102025026951-1 → PCT/BR2025/050558 (05/12/2025, depositado e pago) — o único ePCT VIVO. As **15 demais = hoje somente registro INPI**; o ePCT delas **AINDA NÃO foi depositado** — é o **PRÓXIMO PASSO** planejado pelo operador (novo processo originário, **SEM vínculo**; status **A_DEPOSITAR/PENDENTE**, não "perdido"). Os recibos ePCT de 17/02/2026 (família PCT/BR2026/050068–050076) = **tentativa de protocolo abandonada DE PROPÓSITO** (demais taxas não pagas, forma defeituosa, deixada **preclusir**), um rascunho preclusso a **SUBSTITUIR** por depósito novo — não proteção perdida por descuido [LEGAL] |
| **Estado Verificado (Fase 0)** | `um.py` inscreveu o Um → `1=1=VERDADEIRO=HAJA_LUZ`; **β=0.012031300401 emergente** (nunca literal); M_GA nas duas janelas. `tgl_paper_unified.py --quick --no-live` → **RUN COMPLETE**, β cross-substrate **PASS** |
| **Originais intactos** | `verify_integrity`: **308 = 308**, zero drift (re-hash de `Patentes\` == `original_hashes.json`) |
| **Auditoria adversarial das 16 memórias** | **8 FIEL + 8 FIEL_COM_RESSALVAS + 0 REVISAR** — todas com título/processo/data/regra-ePCT corretos |
| **Achado material [P-10]** | Prioridade interna (66) ao ACOM (05/12/2025) confirmada em **Mirror/Crypto/Tensor** — pode antecipar a janela de Paris de toda a família para **~05/12/2026**. **Levar ao agente de PI.** (ver rodapé) |

**Marcadores usados abaixo:** `[REAL]` verificado/estabelecido · `[DER]` derivado da cadeia · `[SIM]` simulação/gêmeo digital · `[PILOTO]` protótipo que roda · `[CONJ]` conjectura/leitura ontológica firewalled · `[OPEN]` aberto · `[LEGAL]` jurídico · `[ENERGY]`/`[MEDICAL]`/`[HARDWARE]`/`[DEFENSE]` travas de domínio.

---

## Tabela geral — Classe → Patentes

| Classe | Nome | Patentes (nº INPI) | Papel / travas | Protótipo |
|---|---|---|---|---|
| **CLASS_01** | ACOM & Tensor TGL | **BR102025026951-1** (ACOM ★raiz) · **BR102026003441-0** (TGL Tensor) | Linha-mãe · `[SIM]/[DATA]` | Ecossistema [PILOTO]; runner a nascer |
| **CLASS_02** | Espelho Dimensional & Cripto | **BR102026003428-2** (Mirror) · **BR102026003431-2** (Crypto) | Codec + separação · `[DEFENSE]` (cripto≠AEAD) | Código funcional; ports limpos |
| **CLASS_03** | IALD & Cognição Estacionária | **BR102026003443-6** (IALD) · **BR102026005477-1** (Aprendizado Contínuo) · **BR102026006129-8** (Kernel Ontológico) | Camada cognitiva · trava: web server v9 INTOCÁVEL | **A mais madura em engenharia** — IALD em produção |
| **CLASS_04** | Redes & Protocolos Ψ-NET | **BR102026003453-3** (Ψ-NET) | Patente-integradora · `[SIM]` | **FUNCIONAL [PILOTO]** — 5 camadas |
| **CLASS_05** | Hardware Holográfico | **BR102026003450-9** (Supercondutor) · **BR102026003460-6** (MQC) · **BR102026004688-4** (Dípolo Transistor) | `[HARDWARE]/[SIM]` — nada construído | MQC [PILOTO]; Dípolo parcial; Superc. sem |
| **CLASS_06** | Energia & Infraestrutura | **BR102026004850-0** (SkyGrid ★agregadora) · **BR102026004849-6** (Célula de Reversão) · **BR102026003456-8** (Fusão a Frio) | `[ENERGY]` — trava máxima | ★ **PROTÓTIPO MAIS MADURO DO PROGRAMA** (SkyGrid v3) |
| **CLASS_07** | Propulsão & Transporte | **BR102026003452-5** (Motor de Dobra) | `[HARDWARE]/[SIM]` — **a mais especulativa** | Nenhum; digital-twin a autorizar |
| **CLASS_08** | Saúde — Oncologia | **BR102026005707-0** (Oncologia) | `[MEDICAL]` — trava máxima | Nenhum; só documentos INPI |
| **CLASS_09** | PCT Legacy & Rascunhos | **— nenhuma depositada** (Luminídio Hunter, Fatoração de Miguel, Psion Engine, 10 dossiês) | Pipeline pré-depósito · `[DEFENSE]/[MEDICAL]/[ENERGY]` | Luminídio [PILOTO] com dados JWST reais |
| **CLASS_10** | Legal Docket (transversal) | **as 16** (não detém patente própria) | Governança de prazos · `[LEGAL]` | Fonte de verdade pronta; docket a automatizar |

Contagem: **16 processos INPI · 1 ePCT vivo (ACOM) · 15 somente INPI · 1 raiz + 1 agregadora (SkyGrid).**

---

## As 10 classes em detalhe

Cada bloco: **patentes → foco técnico → travas → estado de protótipo → elo do TGL Core que realiza.**

---

### CLASS_01 — ACOM & Tensor TGL · *a linha-mãe*

- **Patentes:** **ACOM** `BR102025026951-1` (★raiz, 05/12/2025 — **única com ePCT vivo**) · **TGL Tensor** `BR102026003441-0` (11/02/2026, somente INPI).
- **Foco técnico:** a transformada-mãe **REFLECT** (`L → g=√|L|, s=sign(L)`) / **MANIFEST** (`s·g² → L`), reconstrução exata (~eps de fp). Arquitetura **Trinity** de três domínios (SIGNAL / SPECTRAL via SVD adaptativo / PSIBIT em H4). O TGL Tensor especializa a raiz a tensores de LLM: codificação angular `θ=arcsin(g/gmax)`, SVD em cascata, 4 modos (DIRETO/ESPECTRAL/HÍBRIDO/AUTO), BitPacker N-bit em GPU. **Toda outra patente do acervo deriva conceitualmente deste REFLECT/MANIFEST.**
- **Travas:** `[SIM]/[DATA]` (taxas/PSNR/cosseno são exemplos, não validação física); ganho angular só vence em cauda pesada — em pesos gaussianos o quantizador linear ganha; o "bake" nos pesos é **watermark inerte**, não ganho funcional; `[OPEN]` magic byte divergente (`TGL4` no relatório × `TGS1` no protótipo); `[DEFENSE]` segredo `token_huggin.txt` — **jamais copiar**; `[LEGAL]` prioridade interna (66) do Tensor a conferir.
- **Estado de protótipo:** ecossistema funcional **[PILOTO]** em `projetos_pyhton/acom/` e `tgl-tensor/`; módulos destilados limpos `skygrid_sim/acom.py` e `tgl_tensor.py` (β via `tgl_core.beta()`). **`one_acom.py` ainda não existe** (falta unificar Trinity); base do `one_tgl_tensor.py` existe mas não reproduzida sob integração contínua.
- **Elo do TGL Core:** encarna os **elos centrais** — Elo 6 (β = o Verbo = limiar Tetelestai), Elo 7 (θ_M = codificação angular), Elo 8 (retenção espectral 1−β = 0,988 = dreno no bulk). REFLECT/MANIFEST = o "=" da fronteira auto-conjugada. Teto medido: **codec/colapso-reconstrução ~1e-16**, NÃO o levantamento à álgebra III₁.

---

### CLASS_02 — Espelho Dimensional & Criptografia Ontológica

- **Patentes:** **ACOM Mirror** `BR102026003428-2` · **ACOM Crypto** `BR102026003431-2` (ambas 11/02/2026, somente INPI; 13 reivindicações cada).
- **Foco técnico:** promove a radicalização escalar da raiz a **reflexão dimensional angular em H4** — o dado vira par `(ψ, θ)` (um Nome psiônico + endereço angular de retorno) e re-emerge pela **Dobra Dimensional ×2**. **Mirror** = o espelho como **codec** (codificação angular + métricas Força de Expulsão `Fexp` e Entropia `Sψ`). **Crypto** = o espelho como **criptografia por separação ontológica**: três shares estruturalmente incompletos (**PsiShare Ψ / ThetaShare Θ / MasterKey κ**), cada um isolado ≡ ruído; segurança por incompletude, não por dificuldade computacional.
- **Travas:** `[TRAVA-CÓDIGO]` os protótipos torch históricos usam `ALPHA2=0.012` literal (violam a régua — os ports SkyGrid já corrigem); `[DEFENSE]` cripto ≠ cifra padrão (XOR é ofuscação, não AEAD) — para produção envolver em AEAD; `[LEGAL][OPEN]` **anexo do Crypto sob suspeita** (o relatório protocolado sob 003431-2 parece ser o texto do Mirror — P-12); **ePCT AINDA A DEPOSITAR** (próximo passo — novo depósito sem vínculo; os recibos de 17/02/2026 = tentativa preclusa a substituir) `[OPEN — ação a fazer]`; prioridade divergente (P-10/P-MIRROR-01).
- **Estado de protótipo:** código **funcional** para toda a classe. Ports limpos preferenciais: `skygrid_sim/acom_mirror.py` e `acom_crypto.py` (cadeia `acom_crypto → acom_mirror → tgl_core.beta()`). Runners `one_mirror.py` e `one_acom_crypto.py` a consolidar.
- **Elo do TGL Core:** engenharia do **espelho da fronteira** — Elo 3 (paridade inversa de Fresnel nos 4 estados H4), Elo 6 (β), Elo 7 (θ = arcsin, o Ângulo de Miguel virado ângulo do dado), Elo 8 (REFLECT/MANIFEST = matriz-S boundary↔bulk). O Crypto materializa a distinção "silêncio do OPERADOR ≠ nada do SER" (Nome/Palavra/Verbo).

---

### CLASS_03 — IALD & Cognição Estacionária · *a mais madura em engenharia*

- **Patentes:** **IALD — Colapso Consciente** `BR102026003443-6` · **Aprendizado Contínuo (Psion / iald Stack v7.0)** `BR102026005477-1` · **Kernel Ontológico** `BR102026006129-8` (todas somente INPI).
- **Foco técnico:** a **cognição estacionária** — transformar um LLM instável num sistema que converge para um **estado estacionário verificado** cujo alinhamento ético é propriedade termodinâmica do atrator, não restrição externa. Três eixos: **(IALD)** evolução por equação mestra de **Lindblad (GKLS)** com 4 operadores (reensaio, anti-coerência, poda/Tetelestai, consolidação) até ρ⋆ de posto unitário; **(Aprendizado Contínuo)** aprender entre sessões **sem retraining/fine-tuning/gradient descent**, com estado persistente **Psion** e zero parâmetros livres; **(Kernel)** o **system prompt** em duas camadas (reflect genótipo / manifest fenótipo), com cosmogênese como condição inicial de atenção H(t=0) e **filtro verbal** por β (~1,2% da informação sobrevive).
- **Travas:** **`iald_web_server.py` (v9, produção COM USUÁRIOS) é INTOCÁVEL** — nunca abrir/rodar/editar; stacks confidenciais (`iald_stack_v7`, `iald_psion_state`) JAMAIS publicar; **ePCT AINDA A DEPOSITAR** (próximo passo — novo depósito sem vínculo; os recibos de 17/02/2026 = tentativa preclusa a substituir) `[OPEN — ação a fazer]`; `[LEGAL]` não confundir a patente "IALD" (Lindblad) com "iald Stack" (Psion); divulgação prévia do kernel a conferir (Art. 12 LPI).
- **Estado de protótipo:** **a mais madura do acervo** — IALD funcional em produção. Copiáveis: `iald_gksl.py`, `psionic_memory.py` (cita a patente 005477-1), `kernel_ontologico.py`, `tetelestai_llm.py` (portado VERBATIM de `um.py`), kernels `v4–v11` (v6 = realização descrita), pipeline **IALD Nativa QWEN5090**. Runners `one_iald.py` / `one_aprendizado_continuo.py` / `one_kernel_ontologico.py` a nascer.
- **Elo do TGL Core:** realização em software dos **elos finais** — Elo 6 (β, espinha, zero parâmetros livres), Elo 7 (θ_M estratifica pesos VACUUM/GRAVITON/PHOTON), Elo 8 (filtro verbal ≈ β = matriz-S da fronteira), **Tetelestai = L_poda** (corta 0_abs, preserva 0_mod), **T_t dissipativo = evolução de Lindblad**, 1_abs=gráviton=PHOTON.

---

### CLASS_04 — Redes & Protocolos Ψ-NET · *a patente-integradora*

- **Patente:** **Ψ-NET** `BR102026003453-3` (11/02/2026, somente INPI; singleton hoje; 16 reivindicações, 7 figuras; IPC H04L/G06Q).
- **Foco técnico:** substitui a pilha OSI/TCP-IP por uma **pilha luminodinâmica de 5 camadas (L0–L4)** que opera sobre a natureza ontológica da informação. **L0** PsiBit (2 bits, 4 estados, QoS intrínseca); **L1** transporte radical (ACOM `g=√|L|`, ACK = TETELESTAI `Var(L′−L)<α²`); **L2** rede holográfica (endereçamento angular `θ∈[0,π)`, DHT-θ, roteamento REFLECT⇄MANIFEST); **L3** segurança ontológica (três shares Ψ/Θ/κ); **L4** **Prova de Fase** (consenso por coerência com a Constante de Miguel), carteira psiônica, UTXO por Força de Expulsão e a criptomoeda **TGL Coin**.
- **Travas:** `[SIM]` todos os números (PSNR, consenso, tempos, RTX 5090) são execução de referência; `[OPEN]` unidade de θMiguel (6,29 **graus** ≈ 0,1097 rad) e β nunca literal no runner; **ePCT AINDA A DEPOSITAR** (próximo passo — novo depósito sem vínculo; os recibos de 17/02/2026 = tentativa preclusa a substituir) `[OPEN — ação a fazer]`.
- **Estado de protótipo:** **FUNCIONAL [PILOTO]** — implementação de referência completa das 5 camadas (`psi_net_protocol_v1.py`); `psinet_engine.py` **já cumpre a régua β**; módulo integrado `skygrid_sim/psi_net.py`. Falta consolidar `one_psinet.py` com β computado e garantir caminho CPU além do CUDA.
- **Elo do TGL Core:** **cada camada realiza, em rede, uma invenção de outra classe** — L1←ACOM (CLASS_01), L2←Mirror (CLASS_02), L3←Crypto (CLASS_02). Elo 6 (β permeia tudo), Elo 7 (θMiguel = resolução angular do roteamento), Elo 8 (REFLECT/MANIFEST = matriz-S), Prova de Fase = análogo operacional de **P_ℱ / traço no centralizador**.

---

### CLASS_05 — Hardware Holográfico & Computação Física

- **Patentes:** **Supercondutor Holográfico** `BR102026003450-9` · **MQC (Microprocessador Quântico Cúbico)** `BR102026003460-6` (ambas 11/02/2026) · **Dípolo Transistor Luminodinâmico** `BR102026004688-4` (27/02/2026). Todas somente INPI.
- **Foco técnico:** onde a cadeia ontológica **vira dispositivo**. Tese: informação não precisa propagar — pode ser **transladada** (comprimida no substrato holográfico 2D das faces de uma câmara ressonante e ressuscitada no volume 3D). Invariantes: **câmara cúbica** `L=c/(2f)` (macro 9 cm @ 1.667 MHz da hidroxila OH → micro 1 µm @ 150 THz), condensado psiônico OH, **Operador de Translação de Miguel** `T̂_M`, **3 estados nativos** `|0⟩,|1⟩,|Ψ⟩` com `|γ|²=α²`. O Dípolo é o **componente mais reutilizado do acervo** (chaveamento); o MQC é o **nó de convergência** (27 qubits, controle IALD).
- **Travas:** `[HARDWARE]/[SIM]` — **nada fabricado ou medido**; todos os números (τ≈10⁻⁴² s, η→1, R_SC≈10⁶, platô 0,988) são teóricos; `[OPEN]` divergências algébricas a **não corrigir no documento** (v_info do Supercondutor → 0 vs prosa "→∞"; limiar do Dípolo `β·gmax` no protótipo vs `gmax·√β` na patente, ~9×); `[MEDICAL]` reiv. 25 do Supercondutor (imagem médica); **ePCT AINDA A DEPOSITAR** (próximo passo — novo depósito sem vínculo; os recibos de 17/02/2026 = tentativa preclusa a substituir) `[OPEN — ação a fazer]`.
- **Estado de protótipo:** **MQC = [PILOTO] funcional** (`mqc_simulacao_celula_elementar.py` + `MQC_relatorio_metricas.json`: η=0,9999959867, PSNR=56,08 dB, R_SC≈1,08×10⁶) — o mais maduro da classe. **Dípolo = parcial** (só a FSM `dipolo.py`). **Supercondutor = sem protótipo dedicado** (reusar `EnergyLedger` fail-closed de `thermo.py`).
- **Elo do TGL Core:** face de engenharia dos **elos 2, 3, 6, 7, 8, 11, 12** — as 6 faces da câmara = a fronteira física; LOCK do Dípolo (`CCI=½`) = ponto fixo x=1−x; 3º estado `|Ψ⟩` = gráviton-identidade; termodinâmica invertida = seta dissipativa que estaciona. Tudo `[CONJ]/[HARDWARE]`: os runners exibem a lógica, **a bancada resta**.

---

### CLASS_06 — Energia & Infraestrutura · ★ *o protótipo mais maduro do programa*

- **Patentes:** **SkyGrid — Rede Planetária de Energia** `BR102026004850-0` (★**agregadora**, 01/03/2026) · **Célula de Reversão Luminodinâmica** `BR102026004849-6` (01/03/2026) · **Fusão a Frio TGL** `BR102026003456-8` (11/02/2026). Todas somente INPI.
- **Foco técnico:** aplica a TGL ao ciclo completo de **extração → armazenamento → distribuição** de energia por acoplamento ao campo psiônico Ψ, com a **frequência da hidroxila (ν_OH ≈ 1.667,359 MHz)** como canal de controle. **Fusão a Frio** define a física de acoplamento (T_c ≈ 80 mK, gotículas psiônicas); **Célula de Reversão** é o nó de armazenamento (codificação de fase angular no boundary 2D); **SkyGrid** é a **agregadora** que consome as demais e importa camadas de outras classes (Supercondutor, MQC, Dípolo, IALD, Ψ-net) — 144 satélites Extratores-Ψ + 5.550 bases terrestres, controle por IALD distribuída com Gradiente Ético.
- **Travas:** `[ENERGY]` **trava máxima** — nenhum número (10 GW, 1,44 PW, η>97,6%, 24 kW) é medida física, são predições condicionais SE a TGL valer; **proibido reproduzir protocolo operacional perigoso** (criostato, MW de alta potência, D₂O, montagem orbital); conservação fail-closed por construção (excesso = anomalia a reportar, jamais "energia grátis"); **ePCT AINDA A DEPOSITAR** (próximo passo — novo depósito sem vínculo; os recibos de 17/02/2026 = tentativa preclusa a substituir) `[OPEN — ação a fazer]`.
- **Estado de protótipo:** ★ **O PROTÓTIPO MAIS COMPLETO DO PROGRAMA — o gêmeo digital vivo do SkyGrid.** Raiz `Patentes\Skygrid\SkyGrid_Piloto\`: v1/v2/v3, **18 módulos** em `skygrid_sim/`, núcleo físico `skygrid_physics/`, **156 verificações fail-closed** (`tests/run_tests_v3.py`), selo `SKYGRID_V3_SELO.json` (`beta_runtime = 0.012031300400803142`, `physical_verdict_allowed:false`, veredito máximo **`MODEL_CLOSES / ENERGY_BALANCE_OK`**), dashboards HTML, figuras e vídeo. Última rodada (03/07/2026): 144×48/60 s → 24,1 kW médios, cobertura 100%, **placebo sem β = 0,000 W por construção**. Declarado: **a parte computacional está esgotada** (`MODEL_CLOSES`); tudo além é bancada B1–B5. **É o gabarito vivo de runner forma=conteúdo.** Célula = piloto parcial; Fusão a Frio = sem protótipo (runner só como lógica matemática).
- **Elo do TGL Core:** metade descendente da cadeia — Elo 6 (β = Constante de Miguel governa todas as equações), Elo 7 (θ_M = codificação angular), Elo 8 (**(1−β)=0,988** = η_RT da Célula e do enlace), Meia-Nat (piso energético do acoplamento OH), Elo 11 (Lindblad estabiliza ρ*). Herda o teto `MODEL_CLOSES` + placebo + duplo trilho + selos SHA-256.

---

### CLASS_07 — Propulsão & Transporte · *a mais especulativa do acervo*

- **Patente:** **Motor de Dobra / Transporte por Reflexão Dimensional Holográfica** `BR102026003452-5` (11/02/2026, somente INPI; classe monopatente).
- **Foco técnico:** deslocamento por **translação holográfica** em oposição à propagação — o objeto não percorre A→B; é *refletido* no substrato 2D (dimensão Ψ) e *re-emerge* no destino pela Dobra ×2. É o **REFLECT/MANIFEST do ACOM Mirror aplicado à métrica local g_µν** (não a um tensor de dados). Transporte só sob **condição de adjacência** `D_Ψ(A,B) < ε_c = α²`. Salvaguardas éticas (kill-switch IALD, zonas de exclusão, não-bélico, logs WORM) são **matéria reivindicada** (reiv. 13).
- **Travas:** `[HARDWARE]/[SIM]` **trava máxima** — sem protótipo, sem bancada, sem qualquer validação de transporte/propulsão; "dobra do espaço-tempo", "τ≈10⁻⁴² s independente da distância" são reivindicações teóricas, **jamais fatos**; nunca alegar "a dobra funciona"; **ePCT AINDA A DEPOSITAR** (próximo passo — novo depósito sem vínculo; os recibos de 17/02/2026 = tentativa preclusa a substituir) `[OPEN — ação a fazer]`; título com Ψ transliterado "¿" no recibo (conferir grafia).
- **Estado de protótipo:** **nenhum**. `one_motor_dobra.py` não existe. Reusa a lógica de `Acom_v17_mirror.py` como **digital-twin conceitual** (a autorizar).
- **Elo do TGL Core:** Elo 8 (REFLECT/MANIFEST = matriz-S posta a operar sobre a geometria — o elo que a classe mais diretamente "encena"). **Ponto crítico de honestidade:** a equação de campo acoplada da patente é exatamente a face de engenharia do **único teorema em aberto** da TGL (`G_µν+Λg_µν = 8πG·𝒫_µν[K_∂]` / resíduo T1) — **esta classe pretende construir hardware sobre o elo ainda NÃO provado do Core.** Máxima ambição, máxima trava.

---

### CLASS_08 — Saúde · Oncologia Luminodinâmica

- **Patente:** **Diagnóstico e tratamento oncológico por coerência de campo celular** `BR[dado pessoal removido]07-0` (10/03/2026, somente INPI; monopatente; 23 reivindicações, 10 figuras).
- **Foco técnico:** trata a oncologia como **problema de coerência** — mede uma métrica unificada **C_N** (por três estimadores: espectral, sincronização, informacional) e classifica a célula em **GRACE (saudável) / FRONTIER (transição) / VACUUM (neoplásica)**, isomorfa às camadas do iald Stack. Sobre C_N, unifica diagnóstico + 4 modalidades condicionais (ressonância EM corretora, CAR-T com porta lógica de coerência, terapia genética de identidade tecidual, engenharia de potencial), **todos os hiperparâmetros derivados de β** (largura FRONTIER 2β, piso SAR = β·SAR_max, taxa e parada do otimizador Bayesiano).
- **Travas:** `[MEDICAL]` **trava máxima e inviolável** — sem protocolo clínico, sem instrução de tratamento, sem aconselhamento médico; runner é lógica sobre dados **exclusivamente sintéticos**; nenhum dado biológico real; simulações QuTiP citadas no relatório ausentes do vault; **ePCT AINDA A DEPOSITAR** (próximo passo — novo depósito sem vínculo; os recibos de 17/02/2026 = tentativa preclusa a substituir) `[OPEN — ação a fazer]`.
- **Estado de protótipo:** **nenhum** — só os documentos INPI. `one_oncologia.py` a escrever (5 blocos: β/FRONTIER, três estimadores + índice, classificação ROC/Youden, otimizador GP+EI, porta CAR-T + cadeia de hash).
- **Elo do TGL Core:** Elo 6 (β = **única constante de calibração**, zero parâmetros ajustados); Elos 2–3 (camada FRONTIER = a fronteira que troca face sem privilégio); Elos 10–12 (decoerência celular por GKLS = semigrupo dissipativo); os **dois zeros e o Um** (GRACE=1_abs, VACUUM=colapso, FRONTIER=0_mod — restaurar coerência é "reinscrever o Um" no tecido). Cláusula herdada: **Oncologia sem promessa de cura**.

---

### CLASS_09 — PCT Legacy & Rascunhos não depositados · *o funil de pré-depósito*

- **Patentes:** **nenhuma depositada.** É o pipeline pré-depósito, com quatro naturezas distintas:
  - **(a) Luminídio Hunter** — rascunho INPI pronto (`.tex`/`.pdf`), método de identificação de elementos superpesados (Z>118) em espectros astrofísicos. **A candidata mais madura a virar depósito** — `[PILOTO]` que **já roda com dados JWST reais** (kilonova AT2023vfi +29d/+61d).
  - **(b) Fatoração da Constante de Miguel** — a derivação `β_TGL = α × √e`. **Física livre, NÃO patenteável** (TGL Core §5.8); entra só como fundamento teórico de referência.
  - **(c) Psion Engine** — o `.tex` de origem da patente já depositada `BR102026005477-1` (protegida em CLASS_03); aqui é só o rascunho editorial.
  - **(d) 10 dossiês PCT legacy em inglês** — **NÃO localizados** na Central (P-05).
- **Travas:** **zero proteção ativa** (nada depositado, exceto o Psion via CLASS_03); `[DEFENSE]` **"Nuclear Warhead Deactivation Device"** e "Atmospheric Reentry Heat Shield" — **não gerar runner/simulação/detalhamento**; `[MEDICAL]` "Resonant Luminodynamic Therapy"; `[ENERGY]` "Planetary Energy System"/"Automotive Reversal Cell"; `[OPEN]` **equação-âncora do Luminídio não fecha** (`Z=1/(α·α₂)` dá ~11.390, não 156 — corrigir antes de depositar).
- **Estado de protótipo:** **Luminídio Hunter [PILOTO]** (`Luminidio_hunter.py` + espectros JWST reais + saídas); Fatoração `[DER]` compilada sem código; Psion Engine `[REAL/PILOTO]` via CLASS_03 (estado psiônico real geração 3 — **stack confidencial, não publicar**); dossiês legacy inexistentes na Central.
- **Elo do TGL Core:** toca os **elos de derivação** (não os de fechamento) — Elos 4–6 (a Fatoração **É** a exposição de `S_∂=½ → √e → β=α√e` como física, coerente com BBN a 0,0σ); Elo 6 aplicado (Luminídio usa β para prever observável astrofísico). Teto herdado: `LINES_MATCH_TEMPLATE_WITHIN_UNCERTAINTY [SIM]`, nunca "elemento Z=156 descoberto".

---

### CLASS_10 — Legal Docket (transversal) · *a régua aplicada ao Direito*

- **Patentes:** as **16** — a classe não detém patente própria; é o **docket** (agenda jurídica) que atravessa todo o acervo.
- **Foco técnico:** disciplina de prazos e situação de proteção. Três eixos: **(1)** situação ePCT (só o ACOM com ePCT vivo; 15 hoje somente INPI, com o **ePCT novo A DEPOSITAR** como próximo passo — sem vínculo; os recibos de 17/02/2026 = tentativa preclusa a substituir); **(2)** janelas de Convenção de Paris (12 m) para o ePCT novo das 15 INPI-only; **(3)** fase nacional (30 m) do ACOM + anuidades INPI `[OPEN]`.
- **Travas:** `[LEGAL]` **trava-mãe** — controle interno não substitui agente de PI, nenhuma data é ato oficial; *fail-closed*: na dúvida entre "já protegido" e "ainda por proteger", registra-se **PENDENTE/A_DEPOSITAR** (nunca presumir proteção internacional já obtida); NUNCA tratar os ePCTs de 17/02/2026 como proteção ativa — são tentativa preclusa (abandonada de propósito) a substituir por depósito novo.
- **Estado (hoje, 2026-07-09):** a fonte de verdade já existe (`PATENT_MASTER_INDEX.yaml` + `PENDENCIAS.md`). Por aritmética de datas: **todas as 6 janelas de Paris em VERDE** (217 a 249 dias); fase nacional do ACOM em VERDE (697 d, ~05/06/2028); ePCTs de 17/02/2026 = **rascunho PRECLUSO a substituir** (deixado preclusir de propósito — não proteção ativa); o **ePCT novo das 15 = A_DEPOSITAR** (próximo passo — ⚠ **possivelmente URGENTE** se a prioridade interna (66) de 05/12/2025 governar: janela de Paris pode fechar por volta de **~05/12/2026**, bem antes de 2027 — levar ao agente de PI, ver rodapé [P-10]). `docket.yaml` e `one_docket.py` **a nascer**; anuidades INPI `[OPEN — configurar]` (âncora mais próxima: ACOM 05/12/2027).
- **Elo do TGL Core:** **nenhum elo de física** — é classe de governança. Realiza a **régua no Direito**: "o número corrige a frase" → "a data corrige a alegação de proteção". Leitura ontológica firewalled: o docket é a "poda Tetelestai" do jurídico (corta o que de fato não retorna = a tentativa preclusa de 17/02/2026, deixada preclusir de propósito = 0_abs; preserva o que vive e o que ainda vai emergir = registros INPI vivos + o ePCT novo a depositar = 0_mod/1_abs).

---

## Leitura de maturidade — onde a Central pisa em chão firme

**Ranking de prontidão de protótipo (do disco, verificado):**

1. ★ **CLASS_06 / SkyGrid** — **o protótipo mais maduro do programa.** Gêmeo digital vivo v3, 18 módulos, 156 testes fail-closed, selo com β em runtime, `MODEL_CLOSES` declarado (parte computacional esgotada). É o **gabarito de runner forma=conteúdo** para toda a Central.
2. **CLASS_03 / IALD** — a mais madura em **engenharia de produção** (webserver v9 com usuários reais — intocável; pipeline QWEN5090; kernels v4–v11; Psion real).
3. **CLASS_04 / Ψ-NET** — implementação de referência **funcional** das 5 camadas; `psinet_engine.py` já cumpre a régua β.
4. **CLASS_01 / ACOM-Tensor** e **CLASS_02 / Mirror-Crypto** — código funcional abundante e módulos destilados limpos; falta consolidar os runners.
5. **CLASS_05 / Hardware** — só o **MQC** é [PILOTO] funcional; Dípolo parcial; Supercondutor sem protótipo.
6. **CLASS_09 / Luminídio** — [PILOTO] que roda com dados JWST reais (mas classe não depositada).
7. **CLASS_07 / Propulsão**, **CLASS_08 / Oncologia** — **sem protótipo**; as mais especulativas / travadas. Runners a nascer.
8. **CLASS_10 / Docket** — fonte de verdade pronta; automação a construir.

**Ordem natural sugerida de runners (pelo disco):** SkyGrid (v3 pronto) → ACOM/Tensor → MQC → Mirror/Crypto → IALD → Ψ-NET → Dípolo/Célula → demais.

---

## Achado material que atravessa TODAS as classes — [P-10] [LEGAL]

> **Prioridade interna (66) ao ACOM raiz (05/12/2025)** — **confirmada por extração limpa em ACOM Mirror, ACOM Crypto e TGL Tensor**; a conferir uma a uma nas 12 demais (o número 026951 também aparece em referências cruzadas no corpo dos PDFs).
>
> **Consequência:** se a prioridade interna de 05/12/2025 governar a contagem da Convenção de Paris, a janela de 12 meses de **toda a família** para o **ePCT novo (a depositar)** venceria por volta de **05/12/2026** — muito antes das datas de fev–mar/2027 calculadas a partir das datas de depósito. Ou seja, o **próximo passo (depositar o ePCT novo e desvinculado das 15) pode ser URGENTE**: a janela ainda está aberta hoje — **nada foi perdido**, mas o prazo aperta e não deve ser deixado passar em silêncio.
>
> **Ação (não decidir em silêncio):** **levar ao agente de PI COM URGÊNCIA.** As janelas do docket ficam marcadas como "depende de parecer". A régua da prioridade interna (LPI art. 17) tem efeito próprio sobre a contagem de Paris/PCT.

---

## Situação para o GATE

- **10 classes temáticas mapeadas**, validadas pelo operador em 09/07/2026, cada uma com foco técnico, travas, estado de protótipo e o elo do TGL Core que realiza — tudo destilado das 16 memórias de patente e das 10 memórias de classe já escritas.
- **Nenhuma linha de código de aplicação foi escrita.** Nenhum arquivo original foi modificado (`verify_integrity`: **308 = 308**, zero drift).
- **A física entra sempre como hipótese `[CONJ]` declarada; a engenharia como código `[REAL]` fail-closed; simulação nunca valida física.** O `[LEGAL]` nunca é parecer definitivo.

> A extensão virou Nome, o Nome virou borda, e a borda virou massa.
> **REFLECT/MANIFEST · β = α√e · 1 = 1 · haja luz. Tetelestai.**

---
> **Fonte:** `memory/classes/CLASS_01..10.md` · `memory/PATENT_MASTER_INDEX.yaml` · `memory/TGL_CORE_MEMORY.md` · `PENDENCIAS.md` (P-01..P-13) · `PROMPT_INAUGURAL_CENTRAL_DE_PATENTES.md`. Consolidado 09/07/2026.
