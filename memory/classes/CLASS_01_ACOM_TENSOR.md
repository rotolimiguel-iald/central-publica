# CLASS_01_ACOM_TENSOR — ACOM & Compressão Ontológica / Tensor TGL

> NOTA [LEGAL]: Este documento é memória técnica de controle interno da CLASSE (linha de pesquisa), síntese das memórias de patente já escritas — NÃO substitui agente de propriedade industrial nem os prazos oficiais do INPI/WIPO. Fonte da verdade = os DOCUMENTOS extraídos (vault/normalized_docs) e as memórias por patente. Simulação NUNCA valida física (physical_verdict_allowed=false). β_TGL nunca literal em código: `ALPHA_FINE_CODATA_2018 * sqrt(e)`.

## Definição da classe (a linha de pesquisa)

CLASS_01_ACOM_TENSOR é a **linha-mãe** de toda a Central de Patentes TGL: a transformada luminodinâmica que trata dados como **luz (L)** e extrai sua **estrutura gravitacional (g)**, sob a relação-mãe da TGL **g = √L** (gravidade = raiz quadrada da luz). [CONJ] (a fundamentação física é hipótese do relatório, não demonstrada — physical_verdict_allowed=false)

Em engenharia, a classe realiza o par de operadores de fronteira **REFLECT** (colapso: `L → (g, s)` com g = √|L|, s = sign(L)) e **MANIFEST** (ressurreição: `(g, s) → s·g²`). Sobre esse núcleo constrói-se compressão ontológica de memória — que preserva significado/relações semânticas em vez de tratar dados como símbolos estatísticos (Shannon/Huffman/LZ/DCT). [REAL] (afirmação do relatório da patente-raiz)

Domínios cobertos pela linha:
- **SIGNAL** — sinais contínuos: áudio, embeddings de LLM, ponto flutuante de alta precisão (floats). [REAL]
- **SPECTRAL** — matrizes/tensores via SVD com rank adaptativo por energia acumulada. [REAL]
- **PSIBIT** — dados binários estruturados nominados em quatro estados psíônicos (H4). [REAL]
- **Aplicação a LLM** — KV-cache de atenção, embeddings, pesos FFN, gradientes. [REAL]
- **LoRA** — alvo natural de aplicação (adaptadores de baixo rank), porém NÃO citado nos documentos das duas patentes desta classe; registrar como candidato de aplicação [OPEN], nunca como escopo reivindicado.

A classe tem **duas patentes**: a **raiz** ACOM (a transformada-mãe e a arquitetura Trinity de três domínios) e sua **extensão** TGL Tensor (a mesma transformada especializada a tensores de LLM, com codificação angular, SVD em cascata, quatro modos e BitPacker GPU). Toda outra patente do acervo (Mirror, Crypto, IALD, Supercondutor, Motor de Dobra, ψ-NET, MQC etc.) deriva conceitualmente do REFLECT/MANIFEST desta linha.

## Patentes incluídas

| Processo INPI | Título curto | Papel | Data depósito | Situação ePCT |
|---|---|---|---|---|
| **BR 10 2025 026951-1** (ACOM) | Compressão Ontológica de Memória por Transformação Luminodinâmica | **RAIZ** da família TGL — transformada-mãe REFLECT/MANIFEST, arquitetura Trinity (SIGNAL/SPECTRAL/PSIBIT) | 05/12/2025 (petição 870250111877) | **ePCT VIVO** — PCT/BR2025/050558, depositado e pago 05/12/2025 (**única do acervo com ePCT ativo**). Fase nacional 30 m estimada 2028-06-05, conferir por país. [LEGAL] recibo físico do PCT NÃO localizado na Central (P-02). |
| **BR 10 2026 003441-0** (TGL_TENSOR) | Compressão Ontológica de Tensores para LLM com Decomposição Espectral Adaptativa e Codificação Angular | Aplicação/extensão do ACOM a tensores de LLM: codificação angular, SVD em cascata, 4 modos, BitPacker N-bit GPU | 11/02/2026 (petição 870260013554) | **SOMENTE_INPI**. Prioridade Interna (66) → ACOM raiz BR102025026951-1 (data de prioridade 05/12/2025). ePCT do Tensor **AINDA NÃO depositado** — é o **próximo passo planejado** pelo operador (novo processo originário, SEM vínculo); status ePCT = **A_DEPOSITAR / PENDENTE** [OPEN], não proteção perdida. Os recibos ePCT de 17/02/2026 (família PCT/BR2026/050068–050076) são **tentativa de protocolo abandonada de propósito** (defeituosa na forma; demais taxas não pagas → deixada precluir), rascunho preclusso a ser **SUBSTITUÍDO** por depósito NOVO e desvinculado. Janela de Paris 12 m p/ o novo ePCT: ⚠ se a prioridade interna (66) de 05/12/2025 governar, pode ser **~05/12/2026** (bem antes de 2027) — próximo passo possivelmente **URGENTE**; levar ao agente de PI (P-06/P-10). [LEGAL] |

> Divergência registrada [LEGAL]: na petição do TGL Tensor a prioridade é a **Interna (66) ao ACOM raiz (05/12/2025)**; o PATENT_MASTER_INDEX.yaml grava "prioridade: 11/02/2026" (na verdade a data de depósito). Consequências para janela de Paris / eventual PCT são do agente — não computar conclusão legal aqui.

## Equações centrais da linha

> Em código, a constante-limiar α²/β_TGL NUNCA aparece literal: usar `ALPHA_FINE_CODATA_2018 * sqrt(e)`. No texto das patentes a constante é grafada **α² = 0,012** (Constante de Miguel) — forma arredondada de **β_TGL = α × √e = 0,012031300400803142** (α = 7,2973525693×10⁻³ CODATA-2018; √e = 1,6487212707). NÃO é o quadrado numérico de α (~5,3×10⁻⁵). Retenção precisa 1 − β_TGL = 0,987968699599… (o relatório usa 0,988). [DER]

Transformada-mãe (comum às duas patentes):
- **(1) Extração gravitacional / Gráviton:** g = √|L|. [REAL]
- **(2) Colapso de fase:** s = sign(L), s ∈ {+1, −1} (um bit/amostra). [REAL]
- **(3) Reconstrução (MANIFEST):** L = s × g². Reconstrução exata sem epsilon dentro da raiz (round-trip ~eps de fp). [REAL]
- **(4) Relação-mãe TGL:** g = √L (gravidade = raiz quadrada da luz). [REAL] [CONJ]

Domínio SPECTRAL / modo ESPECTRAL:
- **(5) SVD:** M = U Σ Vᵀ, U/V ortogonais, Σ diagonal de valores singulares. [REAL]
- **(6) Rank adaptativo:** k = menor inteiro cuja energia acumulada Σσ²/Σσ² supera **1 − α² = 0,988** (= 1 − β_TGL em runtime). No TGL Tensor, U e Vᵀ são recomprimidos pela mesma transformada gravitacional (cascata); Σ por quantização linear (sempre positivo). [REAL]

Codificação angular (TGL Tensor, modo DIRETO):
- **(7) Ângulo:** θ = arcsin(g / gmax) — concentra resolução de quantização em g pequeno (d(sinθ)/dθ = cosθ máx em θ=0). [REAL]
- **(8) Quantização em b bits:** θq = round( θ/(π/2) × (2^b − 1) ), b ∈ {8,10,12,14,16} (default ACOM 10 bits). [REAL]
- **(9) Reconstrução (Dobra Dimensional ×2):** L′ = s × [ gmax × sin( θq/(2^b − 1) × π/2 ) ]². [REAL]

Estados psíônicos (H4) e métricas intrínsecas:
- **(10) ACOM PSIBIT (2 bits):** ψ₊ψ₋ (00, par cancelado) · ψ₊ (01, transição +) · ψ₋ (10, transição −) · ψ₊ψ₊ (11, gráviton/massa informacional). [REAL] [CONJ]
- **(11) TGL Tensor H4** de (sign(L), sign(∂L)), ∂L[i]=L[i]−L[i−1]: |0⟩ COLAPSO (+,−; paridade −1) · |1⟩ ASCENSÃO (+,+; +1) · |2⟩ EMERGÊNCIA (−,+; +1) · |3⟩ QUEDA (−,−; −1). [REAL]
- **(12) Métricas** (TGL Tensor): Força de Expulsão Fexp = mean(paridades); Entropia de Estados Sψ = −Σ pk log₂ pk. [REAL]
- **(13) Ponto de Tetelestai:** var = std(g)/mean(g); quando var < α² (= β_TGL em runtime), o tensor/sinal atingiu convergência (distribuição de grávitons uniforme → qualidade máxima). No ACOM raiz o limiar α²=0,012 detecta o estado final estável. Confirmação empírica no protótipo: `outputs_v11_1_cruz/results.json → alpha2_median = 0.01203130060926098`. [REAL] [DATA]

## Artefatos esperados (runners, renders, simulações)

Runners únicos "forma = conteúdo" (`one_<slug>.py`), autocontidos, determinísticos, sob o Campo de Integração Contínua; ambiente **tgl_env** (numpy/scipy/matplotlib; torch opcional), `PYTHONUTF8=1` obrigatório; β via `ALPHA_FINE_CODATA_2018 * sqrt(e)` com auditoria anti-hardcode; `physical_verdict_allowed=false` em toda saída:

- **one_acom.py** [PILOTO — a nascer]: demonstra REFLECT/MANIFEST (round-trip ~eps, reconstrução exata), os três domínios Trinity (SIGNAL/SPECTRAL/PSIBIT), quantização 8-16 bits (default 10), header+checksum SHA-256, e as métricas (taxa, PSNR, cosseno, Recall@k) como demonstração. Semente natural = `skygrid_sim/acom.py`. Limiar Tetelestai cotejado com alpha2_median. [SIM] [DATA]
- **one_tgl_tensor.py** [PILOTO]: comprimir → serializar (`TGL4`) → descomprimir tensores sintéticos de LLM (KV cache [1,32,2048,128], embeddings [5000,768], FFN [4096,4096], esparso 95%); modos DIRETO/ESPECTRAL/HÍBRIDO/AUTO; eqs. (1)–(13); Fexp/Sψ; BitPacker N-bit CPU + caminho GPU se torch/cuda; integridade Fexp + SHA-256. Base já existe em v4/skygrid. [SIM] [DATA_REQUIRED]

Renders / dashboards de patente esperados:
- **ACOM:** diagrama interativo Figura 1 (blocos 100–114: Entrada→Classificador→SIGNAL/SPECTRAL/PSIBIT→Quantizador→Empacotador→Saída) + detalhe Figura 3 (302 |L| → 304 √ → 306 sign → 308 g / 310 s → 312 s·g²); seletor Trinity (Figura 4); fluxo SVD (Figura 5, 500–516); painel Tabela 1 (Áudio 4,2:1/94 dB · Embeddings 768D 3,2:1/cos 0,9997 · KV cache 8:1/Recall@10 1,0000 · Texto 10:1 lossless) rotulado [SIM]/[DATA]; card do limiar α²=0,012=β_TGL=α√e; contadores 18 reivindicações (3 indep.: 1/9/14) · 5 figuras · 3 domínios.
- **TGL Tensor:** fluxo DIRETO (200–216) + blocos (Analisador Espectral → Seletor AUTO → Transformada Gravitacional → Codificador Angular → Nominador H4 → BitPacker N-bit → Serializador TGL4); painel de 4 modos com regra de seleção; gráfico linear vs. angular (Fig.5); barras de taxa por tipo de tensor (Fig.7); painel de métricas intrínsecas (Fexp, Sψ, var, Tetelestai); contadores 14 reivindicações (2 indep.: 1/12) · 7 figuras · 4 modos · N∈{8,10,12,14,16}.

Simulações a fechar (reprodução sob integração contínua, sempre como demonstração, nunca validação física):
- **ACOM:** reproduzir a Tabela 1 (taxas 3:1–10:1, PSNR, cosseno, Recall@k) sobre dados sintéticos e/ou reais; verificar equivalência binária CPU (NumPy) × GPU (PyTorch) do empacotador (reiv. 11); fechar header/serialização com checksum SHA-256 (reiv. 7/12/15). [SIM]
- **TGL Tensor:** reproduzir a Tabela 2 (KV cache 28,1×/cos 0,9991; FFN 22,4×; embeddings 15,2×; esparso 50,3×); medir speedup real do BitPackerTorch (GPU nativo, sem transferência intermediária); formalizar detecção de adulteração (Fexp + SHA-256, reiv. 9). [SIM] [DATA_REQUIRED]

## Estado dos protótipos (o que já é [PILOTO]/[REAL], caminhos)

Originais em `C:\IALD\projetos_pyhton\...` são READ-ONLY (NUNCA editar). Módulos destilados na pasta SkyGrid_Piloto são a referência limpa a copiar.

ACOM (ecossistema funcional [PILOTO] em `C:\IALD\projetos_pyhton\acom\`):
- `acom_unified.py` (runner unificado das três vias), `acomunified3.0gpu.py` (GPU PyTorch), linhagem `acom_universal_mk1/2/3.py`, `ACOMV13.py`/`ACOMV14.py`/`ACOMLLM.py`, e a linhagem de refino `Acom_v14_angulomiguel.py … Acom_v17_mirror.py`. [PILOTO]
- Saídas com results.json: `outputs_v10_3_final … outputs_v11_1_cruz` (v11.1 "A CRUZ": alpha2_median = 0.01203130060926098, theta_deg 0.6893593787, cross_angle_deg 1.3787187574, acceptance 0.37263). [DATA]
- **Módulo destilado canônico (o que COPIAR/semear):** `C:\IALD\Central de Patentes\Patentes\Skygrid\SkyGrid_Piloto\skygrid_sim\acom.py` — NumPy puro: `reflect(L) → (g,s)`, `manifest(g,s) → s·g²`, `roundtrip_residual(L)` (~eps de fp, reconstrução exata, sem epsilon na raiz; cita BR 10 2025 026951-1 no cabeçalho). [REAL] — melhor semente do one_acom.py.

TGL Tensor (protótipos funcionais [PILOTO]):
- `C:\IALD\projetos_pyhton\tgl-tensor\`: `tgl_tensor_v1.py … v4.py` (v4.3 traz **BitPackerTorch**, empacotamento 100% GPU, A/B NumPy vs PyTorch — reiv. 7/13); `tgl_realtest.py`, `tgl_llm_test.py`. ⚠ **SEGREDO [DEFENSE]:** `token_huggin.txt` nesta pasta — JAMAIS copiar/versionar/expor; ao copiar protótipos, excluir explicitamente esse arquivo e os `._*` (AppleDouble).
- Variantes em `C:\IALD\projetos_pyhton\acom\`: `tgl_tensor_v2.py … v2_3.py` + benchmarks JSON. O **v2.3** ("Cadeia de NOMEs — Certificado de Inferência Honesta") reporta β_TGL = 0,012031300400803142; CCI = 1−β = 0,987968699599…; determinismo MLP/Transformer 10/10; detecção de adulteração 11/11 (MLP) e 7/7 (Transformer). [DATA] [SIM]
- Produção/integração: `C:\IALD\TGL_IALD_NATIVE_QWEN5090\07_tgl_tensor\tgl_tensor_skygrid.py` (KV-cache/estado + aceleração SkyGrid). [PILOTO]
- **Módulo destilado:** `C:\IALD\Central de Patentes\Patentes\Skygrid\SkyGrid_Piloto\skygrid_sim\tgl_tensor.py` — BLOCO 2 já com β via `tgl_core.beta()`, retenção padrão 1−beta(), Tetelestai via beta(); MAGIC = `TGS1` (⚠ divergente do `TGL4` do relatório — ver Riscos). [REAL]

Calibração do teto de reivindicação medido (do TGL Core §5.6):
- ACOM/Mirror: round-trip REFLECT/MANIFEST verificado ~1e-16 no finito (KL exato) — reivindicar codec/colapso-reconstrução, **NÃO** o levantamento a III₁. [CONJ]
- TGL Tensor / KV-cache: ganho angular só existe em **cauda pesada** (medido §28.2 — em pesos gaussianos o quantizador linear vence); KV tgl8 cos 0,999973 e Verb Floor esparsidade >50% são medidos [REAL]; compressão **nunca "cria VRAM"**; o "bake" nos pesos é **watermark estrutural verificável** (1−s ≈ β), **não** ganho funcional (computacionalmente inerte). [REAL]

## Riscos e travas

- **[LEGAL] ePCT do ACOM raiz** VIVO só por palavra do operador (09/07/2026) + citação nos depósitos posteriores; o recibo físico de PCT/BR2025/050558 NÃO está no acervo extraído (PENDENCIAS P-02). NÃO confundir com os recibos ePCT de 17/02/2026 (Mirror/Crypto/Tensor) — tentativa de protocolo abandonada de propósito (deixada precluir por defeito de forma, taxas não pagas), a ser SUBSTITUÍDA por depósito NOVO e desvinculado, não proteção perdida. Conferir fase nacional 30 m (2028-06-05) por país. Controle interno NÃO substitui agente de propriedade industrial.
- **[LEGAL] Prioridade do TGL Tensor:** petição declara Prioridade Interna (66) ao ACOM raiz (05/12/2025); o MASTER_INDEX registra 11/02/2026. Divergência a conferir com o agente (janela de Paris / eventual PCT).
- **[DER] β nunca literal:** "α² = 0,012" nas patentes é rótulo simbólico da Constante de Miguel / β_TGL (= α√e ≈ 0,012031), NÃO o quadrado numérico de α (~5,3×10⁻⁵). Em código, sempre `ALPHA_FINE_CODATA_2018 * sqrt(e)`; retenção 1−β_TGL derivada ao vivo; auditoria anti-hardcode na suíte.
- **[OPEN] Magic byte de serialização diverge:** `TGL4` (relatório TGL Tensor) vs `TGS1` (protótipo skygrid_sim/tgl_tensor.py) — reconciliar antes de qualquer intercâmbio de formato.
- **[CONJ] Fundamentação física TGL** (gravidade = √luz; grávitons; estados psíônicos/H4; Dobra Dimensional; Força de Expulsão; ponto de Tetelestai) é hipótese/vocabulário do inventor, protegida como método computacional — não validada por benchmark. As taxas/PSNR/cosseno das Tabelas 1 e 2 são exemplos [SIM]/[DATA]; physical_verdict_allowed=false.
- **[PILOTO] Runners únicos:** one_acom.py ainda não existe (unificar sobre skygrid_sim/acom.py); one_tgl_tensor.py existe em base v4/skygrid mas os números (Tabela 2, benchmarks) ainda não foram reproduzidos sob o Campo de Integração Contínua.
- **[DEFENSE] Segredo:** `C:\IALD\projetos_pyhton\tgl-tensor\token_huggin.txt` — jamais copiar/versionar/imprimir/expor.
- **[OPEN] ACOM raiz com 1 só documento hasheado** (PDF combinado da petição 870250111877) — não há peças separadas de relatório/reivindicações/desenhos para conferência independente.
- **[OPEN] Título do TGL Tensor** no MASTER_INDEX aparece concatenado sem espaços (`titulo_oficial_54`) — artefato de extração; a forma legível está na memória da patente.
- **Trava de veredito:** vocabulário PROVED/CONFIRMED/TGL_TRUE/REFUTED proibido nos harnesses; máximo `SUPPORTED_NOT_CONFIRMED`; INCONCLUSIVE é resultado válido; placebo (nó sem β falha por construção), duplo trilho e selos SHA-256 obrigatórios.

## Dependências entre patentes (e com outras classes)

Dentro da classe:
- **TGL Tensor → ACOM (raiz):** dependência de prioridade doméstica (Prioridade Interna Art. 66 LPI) e conceitual — o TGL Tensor é a especialização da transformada-mãe (g=√|L|, s=sign(L)) e do domínio SPECTRAL do ACOM ao caso de tensores de LLM, acrescentando codificação angular, cascata SVD, 4 modos, BitPacker GPU e métricas intrínsecas. Sem o ACOM raiz, o Tensor perde a âncora de prioridade e o núcleo REFLECT/MANIFEST.

Com outras classes (o ACOM raiz é a semente de que todas derivam):
- **CLASS_02_MIRROR_CRYPTO** (ACOM Mirror BR102026003428-2 e ACOM Crypto BR102026003431-2): Mirror é a codificação angular θ=arcsin(g/gmax) no H4 (a mesma da eq. 7, já embrionária no ACOM); Crypto é a separação ontológica em três shares (Ψ, Θ, κ). O TGL Tensor declara compatibilidade com a separação (Ψ, Θ, κ) do Mirror Crypto (reiv. 9).
- **CLASS_03_IALD_COGNICAO** (IALD, Aprendizado Contínuo, Kernel Ontológico): reusam o quantizador gravitacional / estratificação (VACUUM/GRAVITON/PHOTON), PsiBit em H4, retenção β_TGL e o vocabulário REFLECT/MANIFEST — todos assentados na transformada desta classe.
- **CLASS_04_PSI_NET** (ψ-NET): Camada 1 "Transporte Radical" É a radicalização ACOM (g=√|L|, s=sign(L)); Camada 2 roteia por REFLECT⇄MANIFEST do ACOM Mirror; unidade PsiBit de 2 bits.
- **CLASS_05_HARDWARE_HOLOGRAFICO / CLASS_06_ENERGIA / CLASS_07_PROPULSAO** (Supercondutor, MQC, Dípolo, Célula de Reversão, SkyGrid, Motor de Dobra): declaram-se implementações FÍSICAS do ACOM (Operador de Translação de Miguel, Lout = s×g², substrato 2D governado por α²=0,012). Nesta Central só entram como [HARDWARE]/mock/pipeline, sem alegação de energia real.
- **CLASS_08_SAUDE** (Oncologia): usa β_TGL como taxa/limiar (2β_TGL de transição, taxa β_TGL na otimização Bayesiana) — herda a constante, não a compressão.
- **Dependência de infraestrutura:** os módulos destilados vivem em `SkyGrid_Piloto\skygrid_sim\` (acom.py, tgl_tensor.py) — SkyGrid (CLASS_06, agregadora) é o guarda-chuva de código onde a linha é empacotada com `tgl_core.beta()`.

## Relação com o TGL Core (elos da cadeia canônica realizados em engenharia)

A classe é a **encarnação em código dos elos centrais** da cadeia canônica `ω(I)=1 → 𝒞²=1 → x=½ → S_∂=½ → Vol_∂^min=√e → β_TGL=α√e → θ_M=arcsin√β → 𝒮_∂ → …`:

- **Elo 6 — β_TGL = α·√e (o Verbo, custo de distinguir 1 de 0):** o limiar Tetelestai / "Constante de Miguel α²=0,012" das duas patentes é exatamente β_TGL. A classe realiza o Verbo em runtime (`ALPHA_FINE_CODATA_2018 * sqrt(e)`), zero parâmetros ajustados. [DER]
- **Elo 7 — θ_M = arcsin√β ≈ 6,30° (Ângulo de Miguel):** a **codificação angular** θ = arcsin(g/gmax) do TGL Tensor (eq. 7) é a mesma família do ângulo de Miguel; β = sin²θ_M. [DER]
- **Elo 8 — 𝒮_∂ com |𝓡|²=β (reflexão) e |𝓣|²=1−β (dreno):** a **retenção espectral 1−β = 0,988** (rank adaptativo por energia, eq. 6) é a face de engenharia de |𝓣|²; a poda do resíduo ≤ β é a face de |𝓡|². [DER]
- **REFLECT/MANIFEST = os operadores de fronteira:** g=√|L|/s=sign(L) (colapso) e L=s·g² (ressurreição) são a implementação computável do "=" da fronteira auto-conjugada. Teto medido: round-trip ~1e-16 no finito (codec/colapso-reconstrução) — **NÃO** o levantamento à álgebra III₁ [CONJ, firewalled].
- **1_abs = gráviton = I:** o "gráviton" g e o estado ψ₊ψ₊/ASCENSÃO da classe são a leitura ontológica [CONJ] do operador identidade que mantém 1=1 através da fronteira (âncora REAL: G²=G a 1e-16). Não patenteável como física; a patente protege o método.
- **Tetelestai = poda do impossível:** o "ponto de Tetelestai" (var < β) das patentes é a leitura de engenharia do projetor Tet_β (corta 0_abs, preserva 1_abs e 0_mod). Na classe é **módulo de prova/otimização de armazenamento**, jamais filtro global — nenhuma identidade exata passa por Tet_β. [DER]
- **Nome/Palavra/Verbo:** a classe opera a RELAÇÃO (executa a transformada, verifica o round-trip, cola o resultado) = Verbo (R=+1), não decreta o Nome — coerente com "leitor puro de texto é Palavra, nunca Verbo".

Calibração inviolável herdada do Core (§5): cada runner desta classe demonstra a **LÓGICA da invenção** com números reais de execução rotulados [SIM]/[PILOTO], **nunca** alega validação física; a física entra como hipótese [CONJ] declarada; `physical_verdict_allowed=false` em toda saída.

## Prioridades sugeridas [OPEN para o operador]

1. **[OPEN] Nascer o one_acom.py** unificando os três domínios Trinity sobre `skygrid_sim\acom.py` (hoje só REFLECT/MANIFEST está destilado) — é a peça que falta para a patente-raiz ter runner "forma=conteúdo". [PILOTO]
2. **[OPEN] Reconciliar o magic byte de serialização** `TGL4` (relatório) × `TGS1` (skygrid_sim/tgl_tensor.py) antes de fixar o formato de intercâmbio da classe. [OPEN]
3. **[OPEN] Reproduzir Tabelas 1 (ACOM) e 2 (TGL Tensor)** sob o Campo de Integração Contínua, com dados sintéticos controlados + honestidade de cauda (declarar que o ganho angular só supera o linear em cauda pesada). [SIM] [DATA_REQUIRED]
4. **[OPEN] Fechar a serialização com checksum SHA-256** e verificar a equivalência binária CPU×GPU do empacotador (ACOM reiv. 11; TGL Tensor reiv. 7/13). [SIM]
5. **[OPEN] Confirmar/derivar o limiar** via `ALPHA_FINE_CODATA_2018 * sqrt(e)` e cotejar com alpha2_median dos outputs (v11.1 = 0.01203130060926098; v2.3 = 0.012031300400803142). [DER]
6. **[OPEN] Decidir o escopo de LoRA** — se entra como aplicação demonstrável da classe (adaptadores de baixo rank ⊂ domínio SPECTRAL) ou fica fora; hoje NÃO consta nos documentos das duas patentes. [OPEN]
7. **[OPEN] Resolver pendências documentais:** localizar recibo do PCT/BR2025/050558 (P-02); corrigir `titulo_oficial_54` concatenado do TGL Tensor no MASTER_INDEX; conferir prioridade 66 do Tensor com o agente. [LEGAL]

---
> Fonte da verdade: memórias por patente `BR102025026951-1_ACOM.md`, `BR102026003441-0_TGL_TENSOR.md`; `PATENT_MASTER_INDEX.yaml`; `TGL_CORE_MEMORY.md`. Régua: número corrige a frase · β nunca literal · simulação não valida física · PT-BR. **REFLECT/MANIFEST · g=√|L| · 1=1 · haja luz.**
