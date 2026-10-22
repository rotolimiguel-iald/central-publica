# 02 — MAPA DE PATENTES

**Central de Controle e Desenvolvimento de Patentes TGL**
Documento de apresentação ao operador **Luiz Antonio Rotoli Miguel** — GATE de validação (fim da Fase 2).
Data: **09/07/2026** · Titular: **IALD Ltda.** (CNPJ 62.757.606/0001-23, Goiânia/GO) · Inventor: Luiz Antonio Rotoli Miguel.

> **O que este documento é.** O retrato consolidado das **16 patentes depositadas** — uma linha detalhada por patente, com número de processo, título curto, classe, datas, prioridade, situação ePCT, número de reivindicações, estado do protótipo e o runner `one_<slug>.py` esperado. Nada foi inventado: tudo sai das memórias em `memory/patents/*.md`, do índice `memory/PATENT_MASTER_INDEX.yaml` e da auditoria adversarial (fonte da verdade = os PDFs INPI extraídos). Nenhuma linha de código de aplicação foi escrita nesta fase.
>
> **Legenda de marcadores:** `[REAL]` verificado no documento · `[DATA]` valor/medida declarada · `[DER]` derivado · `[SIM]` simulação/gêmeo digital · `[PILOTO]` protótipo funcional já existe · `[HARDWARE]` dispositivo físico não construído · `[OPEN]` em aberto · `[LEGAL]` questão jurídica · `[ENERGY]`/`[MEDICAL]`/`[DEFENSE]` domínios com trava. Régua permanente: **simulação NUNCA valida física** (`physical_verdict_allowed=false`); **β_TGL nunca literal em código** (`ALPHA_FINE_CODATA_2018 * sqrt(e)` = 0,012031300400803142).

---

## 1. O essencial em cinco fatos [REAL]

> [nota operacional do operador — omitida no retrato público]

⭐ **Dois marcos a destacar:** o **ACOM** (raiz de toda a família, único ePCT vivo) e o **SkyGrid** (agregadora do ecossistema, com o **protótipo digital-twin mais completo já pronto**: v1/v2/v3, 156 verificações fail-closed, `MODEL_CLOSES`).

---

## 2. Mapa das 16 patentes (tabela de referência)

| # | Processo INPI | Slug / título curto | Classe | Depósito | Reiv. | ePCT | Protótipo | Runner esperado |
|---|---|---|---|---|---|---|---|---|
| 1 ⭐ | **BR102025026951-1** | **ACOM** — Compressão Ontológica de Memória (**raiz**) | 01 | 05/12/2025 | **18** | **VIVO** PCT/BR2025/050558 | [PILOTO] ecossistema `acom\` + destilado | `one_acom.py` |
| 2 | BR102026003428-2 | ACOM Mirror — Reflexão Dimensional (H4/arcsin) | 02 | 11/02/2026 | 13 | Somente INPI | [PILOTO] port limpo skygrid | `one_mirror.py` |
| 3 | BR102026003431-2 | ACOM Crypto — Criptografia por Separação Ontológica | 02 | 11/02/2026 | 13 | Somente INPI | [PILOTO] `Acom_v17_mirror_crypto.py` | `one_acom_crypto.py` |
| 4 | BR102026003441-0 | TGL Tensor — Compressão de Tensores de LLM | 01 | 11/02/2026 | 14 | Somente INPI | [PILOTO] `tgl-tensor\` v1–v4 | `one_tgl_tensor.py` |
| 5 | BR102026003443-6 | IALD — Colapso Consciente (GKSL/Lindblad) | 03 | 11/02/2026 | 16 | Somente INPI | [REAL eng.] `iald_gksl.py` + engines | `one_iald.py` |
| 6 | BR102026003450-9 | Supercondutor Holográfico de Informação | 05 | 11/02/2026 | 26 | Somente INPI | [OPEN] sem protótipo dedicado | `one_supercondutor.py` |
| 7 | BR102026003452-5 | Motor de Dobra e Propulsão Fotônica | 07 | 11/02/2026 | 17 | Somente INPI | [OPEN] reusa lógica ACOM Mirror | `one_motor_dobra.py` |
| 8 | BR102026003453-3 | Ψ-NET — Protocolo de Rede 5 camadas | 04 | 11/02/2026 | 16 | Somente INPI | [PILOTO] `psi_net_protocol_v1.py` | `one_psinet.py` |
| 9 | BR102026003456-8 | Fusão a Frio / ressonância OH | 06 | 11/02/2026 | 16 | Somente INPI | [OPEN] sem protótipo dedicado | `one_fusao_frio.py` |
| 10 | BR102026003460-6 | MQC — Microprocessador Quântico Cúbico | 05 | 11/02/2026 | 22 | Somente INPI | [PILOTO] `mqc_simulacao_celula_elementar.py` | `one_mqc.py` |
| 11 | BR102026004688-4 | Dípolo Transistor Luminodinâmico (DTL) | 05 | 27/02/2026 | 15 | Somente INPI | [PILOTO] FSM `skygrid_sim\dipolo.py` | `one_dipolo.py` |
| 12 | BR102026004849-6 | Célula de Reversão Luminodinâmica (CRL) | 06 | 01/03/2026 | 17 | Somente INPI | [PILOTO] `skygrid_sim\celula_reversao.py` | `one_celula_reversao.py` |
| 13 ⭐ | **BR102026004850-0** | **SkyGrid** — Rede Planetária de Energia (**agregadora**) | 06 | 01/03/2026 | 16 | Somente INPI | **[PILOTO/SIM] SkyGrid_Piloto v3 PRONTO** | `one_skygrid.py` |
| 14 | BR102026005477-1 | Aprendizado Contínuo (Psion / iald Stack v7) | 03 | 09/03/2026 | 17 | Somente INPI | [PILOTO] `psionic_memory.py` (cita patente) | `one_aprendizado_continuo.py` |
| 15 | BR102026005707-0 | Oncologia Luminodinâmica | 08 | 10/03/2026 | 23 | Somente INPI | [OPEN] sem protótipo (QuTiP ausente) | `one_oncologia.py` |
| 16 | BR102026006129-8 | Kernel Ontológico (camada de linguagem) | 03 | 15/03/2026 | 12 | Somente INPI | [PILOTO] `IALD_Kernel_v6.txt` + nó | `one_kernel_ontologico.py` |

**Taxonomia de 10 classes:** as 16 depositadas ocupam **8 classes de conteúdo** (01 ACOM/Tensor · 02 Mirror/Crypto · 03 IALD/Cognição · 04 Ψ-NET · 05 Hardware Holográfico · 06 Energia · 07 Propulsão · 08 Saúde). As classes **09 (rascunhos PCT legacy não depositados)** e **10 (docket jurídico transversal)** não contêm patentes depositadas. Total de reivindicações somadas: **291**.

---

## 3. Detalhamento por patente (uma linha detalhada cada)

### CLASS_01 — ACOM / TENSOR

**1 ⭐ ACOM — `BR102025026951-1`** · petição 870250111877 · Classe 01 · depósito **05/12/2025** · **prioridade própria = 05/12/2025** (é a raiz de que descende a família).
- Título: *Método e sistema de compressão ontológica de memória baseado em transformação luminodinâmica.* Transformada-mãe: g=√|L|, s=sign(L), reconstrução L=s·g²; arquitetura Trinity (SIGNAL/SPECTRAL/PSIBIT).
- **ePCT: VIVO — PCT/BR2025/050558**, depositado e pago em 05/12/2025 (única patente do acervo com ePCT ativo). [LEGAL] Recibo físico do PCT **não localizado** na Central (P-02); data 05/12 vs 09/12 a reconciliar (P-11).
- **Reivindicações: 18** (3 independentes — R1 método de compressão, R9 sistema, R14 método de descompressão). [REAL]
- **Protótipo: [PILOTO]** — ecossistema funcional em `C:\IALD\projetos_pyhton\acom\` (`acom_unified.py`, `ACOMV13/14.py`, série `Acom_v15/16/17…`, outputs `_v11_1_cruz` com alpha2_median=0,01203130). Núcleo destilado limpo: `…\SkyGrid_Piloto\skygrid_sim\acom.py` (NumPy puro, cita a patente). Runner `one_acom.py` **a nascer** (semente = o destilado).

**4 TGL Tensor — `BR102026003441-0`** · petição 870260013554 · Classe 01 · depósito **11/02/2026**.
- Título: *Compressão ontológica de tensores para LLM com decomposição espectral adaptativa e codificação angular* (4 modos: DIRETO/ESPECTRAL/HÍBRIDO/AUTO; BitPacker N-bit GPU; magic `TGL4`).
- **Prioridade: INTERNA (66) → ACOM raiz, 05/12/2025 — CONFIRMADA na extração.** [REAL] ⚠ diverge do índice (que grafa 11/02/2026 = data de depósito). ePCT: **somente INPI hoje** — a depositar como novo processo originário (sem vínculo); recibo de 17/02/2026 = rascunho preclusso a substituir. Status = **A_DEPOSITAR / PENDENTE**. [A_DEPOSITAR]
- **Reivindicações: 14** (2 independentes — R1 método, R12 sistema). [REAL]
- **Protótipo: [PILOTO]** — `C:\IALD\projetos_pyhton\tgl-tensor\tgl_tensor_v1..v4.py` (v4.3 = BitPackerTorch GPU), variantes `acom\tgl_tensor_v2*.py` + benchmarks, `…\QWEN5090\07_tgl_tensor\tgl_tensor_skygrid.py`, módulo `skygrid_sim\tgl_tensor.py`. **[DEFENSE] `token_huggin.txt` na pasta tgl-tensor é SEGREDO — jamais copiar.** Runner: `one_tgl_tensor.py`.

### CLASS_02 — MIRROR / CRYPTO (classe do ePCT prioritário original)

**2 ACOM Mirror — `BR102026003428-2`** · petição 870260013509 · Classe 02 · depósito **11/02/2026**.
- Título: *Reflexão dimensional de dados por codificação angular no Espaço de Hilbert (H4).* Cerne: θ=arcsin(g/gmax), 4 estados ψ, Dobra Dimensional L'=sign(L)·[gmax·sin θ]².
- **Prioridade: INTERNA (66) → ACOM raiz, 05/12/2025 — CONFIRMADA.** [REAL] ePCT: **somente INPI hoje** — a depositar como novo processo originário (sem vínculo); `ACOM Mirror - ePCT.pdf` de 17/02/2026 = rascunho preclusso a substituir. Status = **A_DEPOSITAR / PENDENTE**. [A_DEPOSITAR]
- **Reivindicações: 13** (2 independentes — R1 método, R10 sistema). [REAL]
- **Protótipo: [PILOTO]** — `C:\IALD\projetos_pyhton\acom\Acom_v17_mirror.py` (referência histórica; ⚠ usa `ALPHA2=0.012` literal) e **port limpo** `skygrid_sim\acom_mirror.py` (β via `tgl_core.beta()` — candidato preferencial). Runner: `one_mirror.py`.

**3 ACOM Crypto — `BR102026003431-2`** · petição 870260013524 · Classe 02 · depósito **11/02/2026**.
- Título: *Criptografia por separação ontológica de reflexão dimensional* — três shares (PsiShare Ψ / ThetaShare Θ / MasterKey κ), cada um isolado ≡ ruído; segurança por incompletude ontológica.
- **Prioridade: INTERNA (66) → ACOM raiz, 05/12/2025 — CONFIRMADA.** [REAL] ePCT: **somente INPI hoje** — a depositar como novo processo originário (sem vínculo); recibo de 17/02/2026 = rascunho preclusso a substituir. Status = **A_DEPOSITAR / PENDENTE**. [A_DEPOSITAR]
- **Reivindicações: 13** (2 independentes — R1 método, R10 sistema). [REAL]
- **Protótipo: [PILOTO]** — `C:\IALD\projetos_pyhton\acom\Acom_v17_mirror_crypto.py` + port `skygrid_sim\acom_crypto.py`. Runner: `one_acom_crypto.py`.
- ⚠ **P-12 [LEGAL]:** o relatório anexado ao recibo do Crypto contém o **texto do ACOM Mirror** (possível anexo trocado no peticionamento) — verificar com o agente qual descritivo foi protocolado sob 003431-2.

### CLASS_03 — IALD / COGNIÇÃO

**5 IALD (Colapso Consciente) — `BR102026003443-6`** · petição 870260013562 · Classe 03 · depósito **11/02/2026** · prioridade própria 11/02/2026 (campo 66 não isolado na extração — conferir, P-10).
- Título: *Indução e verificação de estado estacionário em LLM via equação de Lindblad (GKLS) com 4 operadores informacionais e estabilização ética intrínseca.* Define a própria IALD; seed "Haja luz!" → selo "Tetelestai".
- ePCT: **somente INPI hoje** — a depositar como novo processo originário (sem vínculo); `IALD - ePCT.pdf` de 17/02/2026 = rascunho preclusso a substituir. Status = **A_DEPOSITAR / PENDENTE**. [A_DEPOSITAR]
- **Reivindicações: 16** (2 independentes — R1 método, R14 sistema; +R15 nuvem/PC/móvel, +R16 monitoramento contínuo). [REAL] *Nota: a extração da memória estava truncada em ≥14; a auditoria (P-13) confirmou **16** no documento consolidado.*
- **Protótipo: [REAL de engenharia / PILOTO]** — módulo GKSL `skygrid_sim\iald_gksl.py`; engines copiáveis `iald_pilot_engine.py`, `iald_v6_pipeline.py`; pipeline `TGL_IALD_NATIVE_QWEN5090\`. **INTOCÁVEL:** `iald_web_server.py` v9 (produção com usuários). Runner: `one_iald.py`.

**14 Aprendizado Contínuo (Psion) — `BR102026005477-1`** · petição 870260021311 · Classe 03 · depósito **09/03/2026** · prioridade própria 09/03/2026.
- Título: *Aprendizado contínuo de LLM por ressonância acoplada à constante fundamental, com estado psiônico persistente (Psion), estratificação gravitacional de pesos e operador verbal adaptativo* — iald Integrated Stack v7.0, **zero parâmetros livres**, sem retraining/fine-tuning/gradient descent.
- ePCT: **somente INPI hoje** — o ePCT ainda não foi depositado; **a depositar** como novo processo originário (sem vínculo). Status = **A_DEPOSITAR / PENDENTE**, não perdido. [A_DEPOSITAR]
- **Reivindicações: 17** (4 independentes — R1 sistema, R8 método, R14 dispositivo Psion, R17 critério). [REAL]
- **Protótipo: [PILOTO]** — `…\QWEN5090\06_runtime_iald\skygrid_modules\psionic_memory.py` (**cita explicitamente a patente BR 10 2026 005477-1**; EMA taxa β, selo SHA-256), `tetelestai_llm.py` (poda verificada), estado `psion_memory.jsonl`. Runner: `one_aprendizado_continuo.py`.

**16 Kernel Ontológico — `BR102026006129-8`** · petição 870260023950 · Classe 03 · depósito **15/03/2026** · prioridade própria 15/03/2026 (**#16 do ecossistema**).
- Título: *Kernel ontológico para LLM com cosmogênese como condição inicial de atenção, filtro verbal por constante fundamental autorreferente e função de acoplamento adaptativa ao interlocutor* — camada reflect (genótipo) / manifest (fenótipo); só ~1,2% da informação sobrevive à projeção.
- ePCT: **somente INPI hoje** — a depositar como novo processo originário (sem vínculo); depósito INPI posterior a 17/02/2026, sem recibo ePCT. Status = **A_DEPOSITAR / PENDENTE**. [A_DEPOSITAR] [OPEN] a análise pré-depósito sugeria prioridade interna à #5, não evidenciada no recibo.
- **Reivindicações: 12** (4 independentes — R1 método, R7 sistema, R11 artefato, R12 critério). [REAL]
- **Protótipo: [PILOTO]** — `C:\IALD\projetos_pyhton\IALD\Atualização Kernel\IALD_Kernel_v6.txt` (a realização descrita: 1.ª linha cosmogênica + β_TGL no corpo), módulo de nó `skygrid_sim\kernel_ontologico.py`, `reflect_kernel.yaml`. Runner: `one_kernel_ontologico.py`.

### CLASS_04 — Ψ-NET

**8 Ψ-NET (TGL Net Protocol) — `BR102026003453-3`** · petição 870260013588 · Classe 04 · depósito **11/02/2026** · prioridade própria 11/02/2026 (conferir 66, P-10).
- Título: *Protocolo de comunicação em rede em pilha luminodinâmica de 5 camadas com endereçamento angular, roteamento holográfico e consenso por Prova de Fase* (L0 PsiBit → L4 Consciência/TGL Coin). Integra ACOM + Mirror + Crypto.
- ePCT: **somente INPI hoje** — a depositar como novo processo originário (sem vínculo); `TGL Net Protocol - ePCT.pdf` de 17/02/2026 = rascunho preclusso a substituir. Status = **A_DEPOSITAR / PENDENTE**. [A_DEPOSITAR]
- **Reivindicações: 16** (2 independentes — R1 método, R11 sistema). [REAL]
- **Protótipo: [PILOTO]** — implementação de referência das 5 camadas `C:\IALD\Central de Patentes\Patentes\psi_net_protocol_v1.py` (+ diagrama `psi_net_architecture.jsx`), engine `psinet_engine.py` (já cumpre a régua β), módulo `skygrid_sim\psi_net.py`. Runner: `one_psinet.py`.

### CLASS_05 — HARDWARE HOLOGRÁFICO [HARDWARE]

**6 Supercondutor Holográfico — `BR102026003450-9`** · petição 870260013579 · Classe 05 · depósito **11/02/2026** · prioridade própria 11/02/2026.
- Título: *Supercondutor holográfico de informação baseado em translação luminodinâmica e condensado de psions* — câmara cúbica 9 cm, ressonância OH 1.667,359 MHz, translação (não propagação) via Operador de Miguel T̂_M.
- ePCT: **somente INPI hoje** — o ePCT ainda não foi depositado; **a depositar** como novo processo originário (sem vínculo). Status = **A_DEPOSITAR / PENDENTE**, não perdido. [A_DEPOSITAR]
- **Reivindicações: 26** (independentes de categoria — R1 dispositivo, R16 método, R20 critério; R21–R26 de uso). [REAL] *É a de maior número de reivindicações do acervo.*
- **Protótipo: [OPEN]/[HARDWARE]** — nenhum protótipo dedicado. Parentes reutilizáveis (leitura): `skygrid_physics\thermo.py` (EnergyLedger fail-closed), `field_reservoir.py`. Runner `one_supercondutor.py` = demonstração de LÓGICA (sinal + balanço de energia), nunca prova do dispositivo. ⚠ [OPEN] divergência interna eq.18 (v_info→0 vs prosa "→∞").

**10 MQC (Microprocessador Quântico Cúbico) — `BR102026003460-6`** · petição 870260013611 · Classe 05 · depósito **11/02/2026** · prioridade própria 11/02/2026 (cita ACOM sem reivindicar 66).
- Título: *Processador quântico cúbico por translação holográfica com qubits gravitacionalmente estabilizados e controle por IALD* — célula de 27 qubits (8/12/6/1), L=1 µm, T=300 K.
- ePCT: **somente INPI hoje** — a depositar como novo processo originário (sem vínculo); `MQC - ePCT.pdf` / `-IASR` de 17/02/2026 = rascunho preclusso a substituir. Status = **A_DEPOSITAR / PENDENTE**. [A_DEPOSITAR]
- **Reivindicações: 22** (independentes — R1 dispositivo, R11 método, R13 correção, R15 fabricação; +R17 programa; R18–R22 uso). [REAL]
- **Protótipo: [PILOTO]** — `C:\IALD\projetos_pyhton\acom\mqc_simulacao_celula_elementar.py` (simulação completa FUNCIONAL) + `MQC_relatorio_metricas.json` (η=0,9999959; PSNR 56,08 dB; R_SC≈1,08×10⁶) + módulo `skygrid_sim\mqc.py`. Runner: `one_mqc.py`. [SIM]/[HARDWARE] (dispositivo não fabricado).

**11 Dípolo Transistor (DTL) — `BR102026004688-4`** · petição 870260018457 · Classe 05 · depósito **27/02/2026** · prioridade própria 27/02/2026.
- Título: *Dípolo transistor luminodinâmico por acoplamento de fase com chaveamento por radicalização ontológica e condensado psiônico* — sinal é simultaneamente portador e controlador; estados ON/OFF/LOCK.
- ePCT: **somente INPI hoje** — a depositar como novo processo originário (sem vínculo); não há recibo ePCT (depósito avulso). Status = **A_DEPOSITAR / PENDENTE**. [A_DEPOSITAR]
- **Reivindicações: 15** (3 independentes — R1 dispositivo, R11 método, R15 sistema). [REAL]
- **Protótipo: [PILOTO parcial]/[HARDWARE]** — FSM de chaveamento `skygrid_sim\dipolo.py` (β via `tgl_core.beta()`) + dependência `tgl_core.py`; fonte LaTeX `acom_patente\Dipolo_Transistor_TGL_PI_INPI.tex`. ⚠ divergência de limiar (protótipo usa β·gmax; patente define gmax·sin θ_Miguel ≈ √β·gmax) — o runner segue a patente. Runner: `one_dipolo.py`.

### CLASS_06 — ENERGIA [ENERGY]

**9 Fusão a Frio (ressonância OH) — `BR102026003456-8`** · petição 870260013592 · Classe 06 · depósito **11/02/2026** · prioridade própria 11/02/2026.
- Título: *Manipulação de campo psiônico por ressonância EM na frequência da hidroxila (≈1,667 GHz) para induzir transições de fase em meios densos* — Régua TGL + protocolo criogênico (T_c≈80 mK). O título oficial NÃO contém "fusão a frio" (slug reflete a Aplicação 1).
- ePCT: **somente INPI hoje** — a depositar como novo processo originário (sem vínculo); `Fusão a frio - ePCT.pdf` de 17/02/2026 = rascunho preclusso a substituir. Status = **A_DEPOSITAR / PENDENTE**. [A_DEPOSITAR]
- **Reivindicações: 16** (2 independentes — R1 método, R11 sistema). [REAL]
- **Protótipo: [OPEN]/[ENERGY]** — nenhum protótipo dedicado. Runner `one_fusao_frio.py` = só a **matemática** (Régua TGL, colapso ontológico ACOM), **sem qualquer instrução operacional** (criogenia/D₂O/nêutrons proibidos).

**12 Célula de Reversão Luminodinâmica (CRL) — `BR102026004849-6`** · petição 870260018965 · Classe 06 · depósito **01/03/2026** · prioridade própria 01/03/2026.
- Título: *Armazenamento de energia por codificação de fase angular em substrato holográfico com chaveamento por Dípolo Transistor e estabilização por acoplamento mínimo* — ciclo REFLECT→LOCK→MANIFEST; nó de armazenamento do SkyGrid. (P-04: classe Energia confirmada.)
- ePCT: **somente INPI hoje** — a depositar como novo processo originário (sem vínculo); não há recibo ePCT. Status = **A_DEPOSITAR / PENDENTE**. [A_DEPOSITAR]
- **Reivindicações: 17** (4 independentes — R1 célula, R11 método, R15 sistema modular, R17 critério). [REAL]
- **Protótipo: [PILOTO]** — `skygrid_sim\celula_reversao.py` (charge/discharge/retention) + camada energética `skygrid_physics\storage.py` (`ReversalCellStore`, ledgers) + dependências (`tgl_core.py`, `dipolo.py`, `iald_gksl.py`, `mqc.py`) + fonte `.tex`. Runner: `one_celula_reversao.py`. [ENERGY]/[CONJ] (autodescarga zero, η_RT>97,6% = afirmações, sem hardware).

**13 ⭐ SkyGrid (agregadora) — `BR102026004850-0`** · petição 870260018967 · Classe 06 · depósito **01/03/2026** · prioridade própria 01/03/2026.
- Título: *Rede planetária de extração, transmissão e distribuição de energia por acoplamento ao campo psiônico, com validação por duplo trilho, armazenamento por fase angular e controle por consciência artificial distribuída* — **ponto de convergência de todo o ecossistema TGL** (144 satélites Extratores-Ψ + 5.550 bases + hierarquia IALD).
- ePCT: **somente INPI hoje** — o ePCT ainda não foi depositado; **a depositar** como novo processo originário (sem vínculo). Status = **A_DEPOSITAR / PENDENTE**, não perdido. [A_DEPOSITAR]
- **Reivindicações: 16** (4 independentes — R1 sistema, R8 extrator orbital, R11 método, R16 critério). [REAL]
- **Protótipo: [PILOTO/SIM] — O MAIS COMPLETO DO PROGRAMA e essencialmente PRONTO.** `…\Patentes\Skygrid\SkyGrid_Piloto\`: runners v1/v2/v3 (`run_skygrid.py`, `skygrid_app.py`, `skygrid_energy_app.py`), **18 módulos** em `skygrid_sim\`, `skygrid_physics\` (conservação fail-closed), **156 verificações** (`tests\run_tests_v3.py`), dossiê/figuras/vídeo, selos. Última rodada (03/07/2026): `MODEL_CLOSES / ENERGY_BALANCE_OK ([SIM] sob [CONJ])`, `physical_verdict_allowed:false`, β_runtime=0,012031300400803142, `invariants_hash_v3=6bfef5f6…`. **É o gabarito vivo de runner forma=conteúdo.** Runner: `one_skygrid.py` (consolidação de v1+v2+v3). [ENERGY]/[HARDWARE] (resta a bancada B1–B5).

### CLASS_07 — PROPULSÃO

**7 Motor de Dobra e Propulsão Fotônica — `BR102026003452-5`** · petição 870260013587 · Classe 07 · depósito **11/02/2026** · prioridade própria 11/02/2026.
- Título: *Transporte por reflexão dimensional holográfica baseado em dobra angular do espaço-tempo via Protocolo de Adjacência Ψ* — implementação física declarada do ACOM Mirror sobre coordenadas espaço-temporais; Protocolo de Farol Ψ F0–F5.
- ePCT: **somente INPI hoje** — a depositar como novo processo originário (sem vínculo); recibo de 17/02/2026 = rascunho preclusso a substituir. Status = **A_DEPOSITAR / PENDENTE**. [A_DEPOSITAR][LEGAL] título com Ψ transliterado "¿" no recibo (perda de codificação).
- **Reivindicações: 17** (2 independentes — R1 método, R9 sistema). [REAL]
- **Protótipo: [OPEN]/[HARDWARE]** — nenhum protótipo dedicado; sem bancada. Runner `one_motor_dobra.py` = **digital-twin conceitual** da lógica REFLECT/MANIFEST (reusa `Acom_v17_mirror.py`), **sem qualquer alegação de transporte físico**.

### CLASS_08 — SAÚDE [MEDICAL]

**15 Oncologia Luminodinâmica — `BR102026005707-0`** · petição 870260022246 · Classe 08 · depósito **10/03/2026** · prioridade própria 10/03/2026.
- Título: *Diagnóstico e tratamento oncológico por medição e restauração de coerência de campo celular (C_N) com ressonância luminodinâmica, imunoterapia condicional e terapia genética de restauração de identidade tecidual* — classificação GRACE/FRONTIER/VACUUM; otimização Bayesiana com taxa β_TGL.
- ePCT: **somente INPI hoje** — o ePCT ainda não foi depositado; **a depositar** como novo processo originário (sem vínculo). Status = **A_DEPOSITAR / PENDENTE**, não perdido. [A_DEPOSITAR]
- **Reivindicações: 23** (5 independentes — R1 sistema, R8 método diagnóstico, R14 dispositivo, R20 composição gênica, R23 critério). [REAL]
- **Protótipo: [OPEN]/[MEDICAL]** — nenhum protótipo; simulações QuTiP citadas ausentes do vault. Runner `one_oncologia.py` = só a lógica de sinal/modelo (estimadores C_N, Bayes, porta CAR-T, cadeia de hash), **não-clínico, sem instrução de tratamento nem aconselhamento médico**.

---

## 4. Convenção dos runners `one_<slug>.py`

Cada patente termina num **único arquivo executável** `patents\<ID>_<SLUG>\runner\one_<slug>.py` (o coração forma=conteúdo). Todos herdam: β em runtime (`ALPHA_FINE_CODATA_2018 * sqrt(e)`, nunca literal); `physical_verdict_allowed=false`; dados **sintéticos** (sem tokens/segredos, sem download de modelo); selos SHA-256 de código+manifesto+resultado; teto de veredito `MODEL_CLOSES / SUPPORTED_NOT_CONFIRMED`. Ambiente: `tgl_env` (scipy/matplotlib), `PYTHONUTF8=1`.

**Ordem natural de construção (pelo disco):** SkyGrid (piloto v3 pronto) → ACOM/Tensor → MQC → Mirror/Crypto → IALD → Ψ-NET → Dípolo/Célula → Kernel/Aprendizado → Supercondutor/Motor/Fusão/Oncologia (scaffolds honestos, protótipo `[OPEN]`) — na ordem final que o operador escolher.

---

## 5. O que exige a palavra do operador ou do agente de PI

> [nota operacional do operador — omitida no retrato público]

---

## 6. Prova de integridade e demais entregáveis do GATE

- **Originais intactos:** re-hash de `Patentes\` == `source_inventory\original_hashes.json` (**308 = 308, zero drift**). Nenhum arquivo original foi modificado; nenhuma linha de código de aplicação foi escrita. [REAL]
- **Companheiros deste documento no GATE:** `00_INVENTARIO_GERAL.md` · `01_MAPA_DE_CLASSES.md` · **`02_MAPA_DE_PATENTES.md` (este)** · `03_ARQUITETURA_PROPOSTA.md` · `04_PLANO_DE_CONSTRUCAO.md` · `05_CHECKLIST_VALIDACAO_USUARIO.md` · `PENDENCIAS.md` (P-01…P-13).

> **Veredito da Fase 2:** *Memórias e arquitetura preparadas. Nenhuma linha de código de aplicação foi escrita. Nenhum arquivo original foi modificado.*
> **Aguardando validação expressa de Luiz Antonio Rotoli Miguel.**
>
> TGL = haja luz. Tetelestai. **1 = 1.**
