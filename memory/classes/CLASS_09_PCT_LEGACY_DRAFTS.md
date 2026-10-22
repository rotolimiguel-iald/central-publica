# CLASS_09_PCT_LEGACY_DRAFTS · PCT Legacy & Rascunhos não depositados

> Memória de classe da Central de Patentes TGL. Fonte da verdade = os DOCUMENTOS extraídos (`vault\normalized_docs`), os rascunhos locais citados e o `PATENT_MASTER_INDEX.yaml`. Herda `TGL_CORE_MEMORY.md` como fundação. **Simulação NUNCA valida física** (`physical_verdict_allowed=false`). Em código, α₂ (Constante de Miguel = 0,012) e **β_TGL NUNCA aparecem literais**: usar `ALPHA_FINE_CODATA_2018 * sqrt(e)`. Marcadores em toda afirmação. PT-BR na documentação; inglês no código. [LEGAL] controle interno — não substitui agente de propriedade industrial.
>
> **Classe SEM patente depositada.** É o *pipeline* de patentes futuras: o que ainda é rascunho, artigo teórico ou dossiê legado. Nenhum item desta classe tem número BR no Acervo do INPI. Ver `PENDENCIAS.md` P-05 (dossiês PCT legacy em inglês não localizados) e P-08 (rascunhos não depositados).

## Definição da classe (a linha de pesquisa)

A CLASS_09 é o **funil de pré-depósito** da Central: reúne os artefatos que **ainda não são patente** mas alimentam a linha de patentes futuras. Três naturezas distintas convivem aqui, e a régua exige tratá-las separadamente — nenhuma é "proteção ativa": [REAL/LEGAL]

- **(a) Rascunho de invenção não depositada — Luminídio Hunter:** um método/sistema computacional (astrofísica), com relatório descritivo e quadro reivindicatório completos em `.tex`/`.pdf`, mas **sem número BR no Acervo**. É a candidata mais madura a virar depósito real. [PILOTO — já tem protótipo que roda]
- **(b) Artigo teórico, NÃO patenteável — Fatoração da Constante de Miguel:** a derivação de β_TGL = α × √e. É **física** — e a régua do TGL Core §5.8 é explícita: *"a teoria física não é patenteável e sua reprodução científica/simulada é livre"*. Entra na classe como **fundamento teórico de referência**, jamais como pedido de patente nem como runner que alegue validação física. [DER/CONJ]
- **(c) Manuscrito de origem de patente já depositada — Psion Engine:** o `.tex` fonte cujo **título é idêntico** ao da patente já depositada **BR102026005477-1 (Aprendizado Contínuo)**, que vive em CLASS_03. Aqui é registrado como **rascunho de origem** (legado editorial), não como invenção nova. A proteção real dele está em CLASS_03. [LEGAL]
- **(d) Dossiês PCT legacy em inglês (P-05) — NÃO localizados:** dez dossiês pré-INPT em inglês citados nos rascunhos, ausentes de `C:\IALD\Central de Patentes`. Alguns têm contraparte já depositada em outras classes ([CONJ] de mapeamento); outros não têm contraparte conhecida. Carregam travas **[DEFENSE]/[MEDICAL]/[ENERGY]**: conteúdo sensível — **não vira runner**. [OPEN]

Fio condutor: esta classe é onde a Central **respira antes de depositar**. Enquanto o operador não confirmar rota (depósito INPI novo, ou arquivamento), o material fica em quarentena de pipeline — visível, marcado, sem alegação de proteção. É também o único ponto da Central que toca **física pura** (a Fatoração) e **conteúdo de duplo uso** (dossiês [DEFENSE]).

## Patentes incluídas

Tabela de **pré-depósitos** (nenhum é patente ativa; a coluna "processo" registra o estado real):

| Processo INPI | Título curto | Data (rascunho) | Situação ePCT |
|---|---|---|---|
| **— não depositado** (rascunho INPI pronto) | **Luminídio Hunter** — método/sistema computacional de identificação espectroscópica de elementos superpesados (Z>118) em espectros astrofísicos por predições de estabilidade holográfica + correlação multi-época | 10/02/2026 (`.tex`/`.pdf`); protótipo dez/2025–jan/2026 | **N/A** — sem depósito; sem ePCT. Rota futura = depósito INPI + eventual PCT dentro de 12 m da prioridade [OPEN/LEGAL] |
| **— não patenteável** (artigo de física) | **Fatoração da Constante de Miguel** — decomposição β_TGL = α × √e (interpretação física dos fatores, tensor de Einstein fatorado, χ² sobre 13 protocolos, critérios de falsificação) | 02/03/2026 (`.tex`/`.pdf`) | **N/A** — teoria física, livre e não patenteável (TGL Core §5.8). Não é pedido de patente [DER] |
| **→ depositada em CLASS_03** como **BR102026005477-1** | **Psion Engine** — manuscrito `.tex` fonte de "Aprendizado Contínuo / iald Integrated Stack v7.0" (título idêntico ao depósito) | 09/03/2026 (`.tex`); depósito INPI **09/03/2026** | **SOMENTE_INPI** via CLASS_03; ePCT **A_DEPOSITAR / PENDENTE** — o ePCT de 17/02/2026 (família PCT/BR2026/050068–050076) foi **tentativa de protocolo abandonada de propósito** (taxas não pagas, deixada precluir por ser defeituosa na forma): rascunho preclusso a **substituir** por um depósito NOVO e desvinculado, não proteção que se perdeu. Próximo passo planejado = novo ePCT originário, sem vínculo, dentro de 12 m da prioridade (Convenção de Paris); ⚠ se a prioridade interna (66) de 05/12/2025 governar, pode ser ~05/12/2026 (antes de 2027-03-09) — próximo passo possivelmente URGENTE, levar ao agente de PI (P-06/P-10). O `.tex` aqui é o rascunho de origem, não invenção nova [LEGAL][OPEN — ação a fazer] |
| **— não localizados** (10 dossiês em inglês, P-05) | **Sonic Intelligence · Cubic Quantum Microprocessor · Planetary Energy System · Automotive Reversal Cell · Resonant Luminodynamic Therapy · TGL Singularity Theory · Terrestrial BNI · Gravitational Motor · Atmospheric Reentry Heat Shield · Nuclear Warhead Deactivation Device** | desconhecida | **N/A / desconhecida** — não localizados na Central; perguntar ao operador onde estão [OPEN][DEFENSE][MEDICAL][ENERGY] |

Titular (dos rascunhos que declaram inventor): Luiz Antonio Rotoli Miguel / IALD Ltda. (CNPJ 62.757.606/0001-23, Goiânia/GO). [REAL]
**Regra ePCT (palavra do operador, 09/07/2026):** SÓ o ACOM raiz BR102025026951-1 tem ePCT vivo (PCT/BR2025/050558, 05/12/2025, depositado e pago). **Nada nesta classe tem ePCT vivo** — não há sequer depósito. [LEGAL]

## Equações centrais da linha

Espinha comum da classe (herdada do TGL Core; em código sempre em runtime, nunca literal):
- **Constante de Miguel (o Verbo):** β_TGL = α × √e = **0,012031300400803142**, com α = 7,2973525693 × 10⁻³ (estrutura fina, CODATA 2018) e √e = 1,6487212707 (custo entrópico mínimo da projeção fronteira→bulk, ½ nat). Verificado em runtime nesta sessão. β′_TGL = β_TGL(1+β_TGL) = **0,012176053**. [REAL/DER]
- **Ângulo de Miguel:** θ_Miguel = arcsin(√β_TGL) ≈ **6,297°** (≈ 6,29°–6,30°). [DER]
- **Fatoração trinária:** β_TGL = α × √e ⇔ **Verbo = Nome × Palavra** (Nome=α eletromagnetismo/filtro; Palavra=√e termodinâmica/compressão; Verbo=β_TGL a fronteira/poda). [REAL âncora / CONJ leitura]
- **Convenção de símbolo:** os rascunhos escrevem a Constante de Miguel como **α₂ (ou a₂) = 0,012031**, numericamente = β_TGL. Isto NÃO é α² da estrutura fina (α²_fina = 5,33 × 10⁻⁵). Manter a distinção; em código, `beta = ALPHA_FINE_CODATA_2018 * sqrt(e)`. [OPEN — confirmar notação com o operador]

Fatoração da Constante de Miguel (artigo teórico — conteúdo lido pelo índice `.toc`; corpo do PDF não extraído nesta sessão por falta de lib PDF, ver [OPEN]): [DER/CONJ]
- **A decomposição:** β_TGL = α × √e; verificação numérica direta; propagação de incertezas; **forma quadrática** (§2.3, §7). α = fator eletromagnético (Nome); √e = fator termodinâmico (½ nat, Palavra); o produto = **a fronteira** (Verbo). [DER]
- **Tensor de Einstein fatorado (§4):** *"o tensor não é estável, a projeção é"*; equação de Einstein reescrita como produto fatorado; leitura do problema da hierarquia gravitacional. [CONJ — leitura ontológica firewalled da álgebra]
- **Amplificação holográfica decomposta (§5):** o inverso de α₂ (1/β_TGL ≈ **83,12** = tempo/amplificação característica, o mesmo 1/β do TGL Core e do T_c ≈ 80 mK da Fusão a Frio); verificação nos protocolos. [DER]
- **Forma primordial (§7):** *"a gravidade é o preço entrópico da autointerferência da luz"*; interpretação de α² e de e. [CONJ]
- **Verificação (§8) e falsificação (§9):** convergência do valor fatorado sobre 13 protocolos computacionais; teste χ²; critérios de falsificação direta e previsão quantitativa. Apêndices: alta precisão numérica; relações termodinâmicas do √e (nat, meio-nat, limite de Landauer). [DER — coerente com a evidência de β do TGL Core §4.1: BBN centra em α√e a 0,0σ]

Luminídio Hunter (rascunho — do relatório descritivo lido integralmente): [DER de teoria + REAL de algoritmo]
- **Número atômico crítico (predição TGL):** o rascunho afirma **Z_crítico = 1/(α × α₂) ≈ 156** (elemento "Luminídio", Lm; isótopo ⁴⁰⁰Lm, Z=156, N=244). ⚠ **Inconsistência numérica interna:** 1/(7,297×10⁻³ × 0,012031) = **11.389,96**, não 156 — a fórmula transcrita **não fecha** com o resultado alegado. Registrar como [OPEN] para o operador; a estabilidade holográfica (fronteira 2D/3D, tensão de paridade) resolveria Z>137, mas a *equação-âncora* precisa de correção. [OPEN — o número corrige a frase]
- **Algoritmo (o que É engenharia [REAL]):** janela de busca **adaptativa** proporcional à incerteza ab initio (Δλ_k = λ_k^obs × u_k, u_k∈{0,25;0,30;0,35;0,40}); correção de redshift λ_obs = λ_rest(1+z); contínuo por Savitzky-Golay ordem 3; SNR = (F−C)/max(σ,10⁻²⁵); classificação DETECTADO/TENTATIVO/MARGINAL/NÃO-DETECTADO; discriminação vs processo-r (offset < 5% = ambíguo); persistência multi-época (r = SNR(t₂)/SNR(t₁) ∈ [0,1;1,0]); significância P = Π_k(2Δλ_k/Δλ_total). [REAL de método]

## Artefatos esperados (runners `one_<slug>.py`, renders, simulações)

Regra desta classe: **só (a) pode virar runner.** (b) é física livre (não vira runner que alegue validação); (c) já tem runner em CLASS_03; (d) está sob trava [DEFENSE]/[MEDICAL]/[ENERGY] e **não vira runner**. [LEGAL]

- **`one_luminidio_hunter.py`** (buildable, autocontido; tgl_env com scipy/numpy/matplotlib; `PYTHONUTF8=1`; `physical_verdict_allowed=false`): pipeline de 6 módulos (100 entrada/pré-proc → 200 predição TGL → 300 correlação adaptativa → 400 discriminação processo-r → 500 multi-época → 600 significância/relatório JSON), demonstrando a **LÓGICA** sobre os espectros JWST NIRSpec **reais e públicos** da kilonova AT2023v (+29d/+61d) já presentes no disco. Rótulo **[PILOTO]/[SIM]**: é análise de dados astronômicos públicos — sem sensibilidade [DEFENSE]/[MEDICAL]. Reuso direto de `Luminidio_hunter.py`. Veredito máximo: `LINES_MATCH_TEMPLATE_WITHIN_UNCERTAINTY [SIM]` + "resta revisão por par astrofísico"; **nunca** "elemento Z=156 descoberto". [PILOTO]
- **Render / painel:** sobreposição espectro observado × 5 posições preditas com barras de incerteza; barras de offset vs contaminantes (limiar 5%); painel multi-época +29d/+61d com r de decaimento. Reuso do `luminidium_results.png` existente. [PILOTO]
- **Fatoração da Constante de Miguel — SEM runner de validação física.** No máximo, um **render didático** da fatoração β=α×√e e da convergência de β (reprodução livre da física, rotulada [DER], `physical_verdict_allowed=false`, vocabulário PROVED/CONFIRMED proibido). O χ² dos 13 protocolos é resultado DECLARADO no artigo, não reproduzido como prova aqui. [DER/OPEN]
- **Psion Engine — SEM runner próprio nesta classe.** O runner é **`one_aprendizado_continuo.py` em CLASS_03** (Psion por N gerações, EMA taxa β_TGL, eco reflexivo/passivo, persistência JSON). Aqui só se guarda o `.tex` de origem. [LEGAL]
- **Dossiês PCT legacy (P-05) — SEM runner.** Bloqueados por trava [DEFENSE]/[MEDICAL]/[ENERGY] até localização e triagem do operador. [OPEN]

## Estado dos protótipos (o que já é [PILOTO]/[REAL], caminhos)

- **Luminídio Hunter — [PILOTO] já roda, com DADOS REAIS.** [REAL de engenharia]
  - Relatório/rascunho INPI: `C:\IALD\Central de Patentes\Patentes\Luminidio_Hunter_PI_INPI.pdf` e `...\.tex` (10/02/2026); extração normalizada em `vault\normalized_docs\Patentes\Luminidio_Hunter_PI_INPI.pdf.txt`. IPC declarada: G01J 3/28; G06F 18/24; G01N 21/31. [REAL]
  - Protótipo executável + dados: `C:\IALD\Artigo\the_boundary\Genesis da Unificação\Luminidio\Luminidio_hunter.py` (27/01/2026) com **espectros JWST reais** `AT2023vfi_JWST_29d_fluxcal.txt` / `_61d_fluxcal.txt`, saídas `luminidium_results.json` + `luminidium_results.png`. [REAL/PILOTO]
  - Modelagem nuclear/atômica complementar: `C:\IALD\observaveis_tgl\luminidio.py`, `luminidio_analysis.py`, `luminidio_results.json`, `magnetar_luminidio_analysis.py` (17/12/2025). [PILOTO]
  - ⚠ **[OPEN/DATA] Tabelas de transição divergem entre artefatos:** o rascunho INPI (Tabela 1) usa 5 linhas NIR λ_rest {12455, 15942, 18832, 21124, 27899} Å e config [Og]5f¹⁴6d¹⁰7s²7p⁶8s²5g¹⁸6f⁸; a Figura 7 do mesmo rascunho usa λ_pred {13261, 16973, 20050, 22491, 29704} Å; o protótipo `luminidio_results.json` (dez/2025) lista transições ópticas/raio-X **diferentes** (8p3/2→8s1/2 @4123Å, Kα1 @242,1 keV…). Consolidar antes de qualquer depósito. [OPEN]
- **Fatoração da Constante de Miguel — [DER] compilado, sem protótipo de código.** `C:\IALD\projetos_pyhton\acom\acom_patente\fatoracao_constante_miguel_v1.pdf` (+ `.tex`/`.aux`/`.log`/`.toc`, 02/03/2026). Documento de física; a "verificação" é o próprio TGL Core (β via `um.py`, BBN 0,0σ). [DER]
- **Psion Engine — [REAL/PILOTO] via CLASS_03.** Manuscrito `C:\IALD\projetos_pyhton\IALD\files\Psion_Engine_PI_INPI.tex` (09/03/2026, 872 linhas). Estado psiônico real ao lado: `C:\IALD\projetos_pyhton\IALD\files\iald_psion_state.json` — **geração 3**, β_TGL = 0,012031300400803142 ancorado, perfis de camadas 0/1/2 (GRACE) e 27 (VACUUM), ressonância angular 15 buckets, histórico de convergência (runs 1/2/3, score 2,805→2,891→2,647 com run 3 = eco PASSIVO diagnosticado). É o mesmo Psion citado em CLASS_03 (`psionic_memory.py` cita "patent BR 10 2026 005477-1"). **Stack confidencial — não publicar.** [REAL de engenharia / LEGAL]
- **Dossiês PCT legacy (P-05) — INEXISTENTES na Central.** Nenhum caminho localizado. [OPEN]

## Riscos e travas

- **[LEGAL] Zero proteção ativa.** Nada nesta classe é patente concedida nem sequer depositada (exceto o Psion Engine, cuja proteção está em CLASS_03). Não anunciar "patente" para Luminídio, Fatoração ou os dossiês legacy. Controle interno NÃO substitui agente de propriedade industrial.
- **[LEGAL] Física não é patenteável.** A Fatoração da Constante de Miguel é teoria (TGL Core §5.8): reprodução científica/simulada é livre; **não** convertê-la em pedido de patente nem em runner com veredito físico.
- **[DEFENSE] Trava de duplo uso.** O dossiê **"Nuclear Warhead Deactivation Device"** é conteúdo de defesa; **não** gerar runner, simulação, render ou detalhamento técnico. **"Atmospheric Reentry Heat Shield"** é adjacente a defesa/aeroespacial — mesma cautela. [DEFENSE]
- **[MEDICAL] "Resonant Luminodynamic Therapy"** toca terapêutica humana — sem promessa de cura, sem parâmetros clínicos, sem runner. Alinha à trava da Oncologia (CLASS_08). [MEDICAL]
- **[ENERGY] "Planetary Energy System" / "Automotive Reversal Cell"** tocam extração/armazenamento de energia — sem alegação de energia real; só como pipeline/mock se algum dia. Alinha às travas de CLASS_06. [ENERGY]
- **[OPEN] Localização dos dossiês (P-05).** Não estão na Central (outro disco? zip? nuvem?). Perguntar ao operador antes de qualquer ação; enquanto isso, a classe guarda só os rascunhos locais.
- **[OPEN] Equação-âncora do Luminídio.** Z_crítico = 1/(α×α₂) ≈ 156 **não fecha** aritmeticamente (dá ~11.390). Corrigir a fórmula OU o valor antes de depositar — é a reivindicação-caracterizante do quadro. O número corrige a frase.
- **[OPEN] Notação α₂ vs α².** α₂ (Constante de Miguel = 0,012031 = β_TGL) ≠ α²_fina (5,33×10⁻⁵). Padronizar antes do depósito para não induzir erro de leitura no examinador.
- **[DATA] Métricas declaradas ≠ reproduzidas.** "5/5 linhas > 5σ" (Luminídio) e "χ² dos 13 protocolos" (Fatoração) e "score/eco por geração" (Psion) são resultados DECLARADOS nos documentos; simulação/benchmark NUNCA valida física.
- **[LEGAL] Divulgação prévia.** Se Luminídio, dossiês ou a Fatoração já foram publicados (the_boundary / Zenodo / GitHub), o período de graça de 12 meses (Art. 12 LPI) pode já estar correndo — conferir datas de publicação vs. eventual depósito futuro.

## Dependências entre patentes (e com outras classes)

Esta classe é upstream (rascunho) e downstream (legado) ao mesmo tempo:

- **Luminídio Hunter → TGL Core:** depende inteiramente da Constante de Miguel (α₂/β_TGL) como fonte da predição de Z=156; é a **aplicação astrofísica** da fatoração. Não depende das outras patentes de engenharia. [DER]
- **Fatoração da Constante de Miguel → TODAS as classes:** é a **derivação de β_TGL = α×√e** que as 16 patentes citam como "Constante de Miguel / a₂ = 0,012". É o fundamento teórico comum — CLASS_01 (ACOM/Tensor), CLASS_03 (IALD/Psion/Kernel), CLASS_05/06 (a²_c = 0,012 como Ponto Tetelestai / população do estado |ψ⟩), CLASS_07/08 — todas herdam esta fatoração. Mas por ser física, **não é reivindicável**; sustenta as reivindicações sem ser uma delas. [DER]
- **Psion Engine ↔ CLASS_03 (BR102026005477-1):** relação de **identidade** — o `.tex` desta classe é o manuscrito de origem da patente Aprendizado Contínuo. A memória viva da invenção está em `CLASS_03_IALD_COGNICAO.md` e em `memory\patents\`. Aqui é só o rascunho editorial. Não duplicar reivindicações. [LEGAL]
- **Dossiês PCT legacy (P-05) ↔ patentes já depositadas — [CONJ] de mapeamento (a confirmar):**
  - *Cubic Quantum Microprocessor* ↔ **MQC** BR102026003460-6 (CLASS_05) [CONJ]
  - *Gravitational Motor* ↔ **Motor de Dobra** BR102026003452-5 (CLASS_07) [CONJ]
  - *Planetary Energy System* ↔ **SkyGrid** BR102026004850-0 (CLASS_06) [CONJ][ENERGY]
  - *Automotive Reversal Cell* ↔ **Célula de Reversão** BR102026004849-6 (CLASS_06) [CONJ][ENERGY]
  - *Resonant Luminodynamic Therapy* ↔ **Oncologia** BR102026005707-0 (CLASS_08) [CONJ][MEDICAL]
  - *TGL Singularity Theory* ↔ física/teoria (não patenteável), parenta a Fatoração [CONJ]
  - *Sonic Intelligence · Terrestrial BNI · Atmospheric Reentry Heat Shield · Nuclear Warhead Deactivation Device* — **sem contraparte depositada conhecida** — pipeline genuíno de futuro [OPEN][DEFENSE]
  - Se o mapeamento se confirmar, os dossiês legacy são as **versões em inglês pré-INPT** das invenções que já foram depositadas em português — úteis para eventual PCT internacional dentro das janelas de Paris (ver P-06), **sob orientação do agente de PI**. [LEGAL]

## Relação com o TGL Core (que elos da cadeia canônica a classe realiza em engenharia)

A cadeia canônica é `ω(I)=1 → 𝒞²=1 → x=½ → S_∂=½ → √e → β_TGL → θ_M → 𝒮_∂ → P_ℱ → II₁ → ergodicidade → traço → 1=1`. Esta classe toca os elos **de derivação** (não os de fechamento), porque é onde a teoria ainda vira aplicação:

- **Elos 4–6 — S_∂=½ nat → Vol_∂^min=√e → β_TGL=α√e (a própria Fatoração):** a "Fatoração da Constante de Miguel" É a exposição em artigo destes três elos: β decomposto em Nome (α) × Palavra (√e), com √e = e^{S_∂} = e^{½} como custo entrópico mínimo da fronteira. A classe **é o lugar onde a cadeia é escrita como física**, antes de descer para engenharia nas outras classes. Coerente com a evidência primária do TGL Core §4.1 (BBN centra em α√e a 0,0σ). [DER]
- **Elo 6 aplicado — Z_crítico = 1/(α·α₂) (Luminídio):** a única patente-rascunho que usa β_TGL para **prever um observável astrofísico** (elemento superpesado). Realiza o elo β em *predição*, não em compressão/cognição. ⚠ com a ressalva aritmética [OPEN] acima. [DER + OPEN]
- **Elo 7 — θ_M = arcsin√β:** herdado por todos os itens (fronteira sinal/vácuo; janelas adaptativas do Luminídio ecoam a "fronteira natural entre sinal e vácuo em qualquer domínio informacional"). [DER]
- **1/β ≈ 83,12 (tempo/amplificação característica):** a "amplificação holográfica decomposta" (§5 da Fatoração) é a mesma escala 1/β do TGL Core (T_t = e^{−tβ|K_∂|}, 1/β≈83) e do T_c≈80 mK da Fusão a Frio. [DER]
- **Teto de veredito herdado (inviolável):** qualquer runner desta classe (na prática, só `one_luminidio_hunter.py`) demonstra a LÓGICA com dados reais rotulados [SIM]/[PILOTO], **nunca** alega validação física nem descoberta; vocabulário PROVED/CONFIRMED/TGL_TRUE/REFUTED proibido; `physical_verdict_allowed=false`; selos SHA-256. A física (Fatoração) é reprodução livre, não prova interna — apresentar β α-livre como "prova" **falsifica** a TGL (blocklist §4.2). [REAL]

## Prioridades sugeridas [OPEN para o operador]

- [ ] **[OPEN][LEGAL]** Localizar os 10 dossiês PCT legacy em inglês (P-05): em que disco/zip/nuvem estão? Sem eles, a triagem [DEFENSE]/[MEDICAL]/[ENERGY] e o eventual PCT ficam bloqueados.
- [ ] **[OPEN]** Corrigir a equação-âncora do Luminídio: Z_crítico = 1/(α×α₂) dá ~11.390, não 156. É a reivindicação caracterizante — decidir a fórmula/valor corretos antes de qualquer depósito.
- [ ] **[OPEN/DATA]** Consolidar UMA tabela de transições do Luminídio (Tabela 1 do rascunho vs Figura 7 vs `luminidio_results.json`) — hoje três conjuntos divergentes.
- [ ] **[PILOTO]** Autorizar `one_luminidio_hunter.py` como primeiro runner da classe (dados JWST reais já no disco; sem trava de sensibilidade) — o único item pronto para virar demonstração forma=conteúdo.
- [ ] **[LEGAL]** Decidir a rota de cada rascunho: **depositar no INPI** (Luminídio), **arquivar como física livre** (Fatoração + TGL Singularity Theory), ou **manter como fonte** (Psion Engine, já protegido em CLASS_03). Conferir período de graça (Art. 12 LPI) se houve publicação prévia.
- [ ] **[OPEN]** Confirmar/rejeitar o mapeamento [CONJ] dossiê-legacy ↔ patente-depositada (Cubic↔MQC, Gravitational Motor↔Motor de Dobra, Planetary↔SkyGrid, Automotive↔Célula, Therapy↔Oncologia) para saber quais legados já estão cobertos e quais são pipeline genuíno.
- [ ] **[LEGAL]** Padronizar a notação α₂ (Constante de Miguel = β_TGL) para não colidir com α²_fina nos textos de depósito.
