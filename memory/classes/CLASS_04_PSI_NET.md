# CLASS_04_PSI_NET · Redes & Protocolos Ψ-NET

> Memória da classe da Central de Patentes TGL. Fonte da verdade = os DOCUMENTOS extraídos dos depósitos INPI (`vault\normalized_docs`) e as memórias de patente já escritas em `memory\patents\`. Este arquivo NÃO é parecer de propriedade industrial. [LEGAL]
>
> **Régua herdada (inviolável):** o número corrige a frase; β_TGL nunca literal em código (`ALPHA_FINE_CODATA_2018 * sqrt(e)`); simulação nunca valida física (`physical_verdict_allowed = false`); marcadores em toda afirmação; o que não está nos documentos = [OPEN]. [REAL]

---

## Definição da classe (a linha de pesquisa)

A CLASS_04 é a **camada de comunicação da pilha TGL**: leva a ontologia luminodinâmica (o Verbo β, o colapso g=√|L|/ressurreição L′=s·g², o endereçamento angular no H4) do plano de compressão/criptografia para o plano de **rede** — enlace, transporte, roteamento, segurança e consenso. [REAL]

A tese central da linha é substituir a pilha OSI/TCP-IP por uma **pilha luminodinâmica de cinco camadas (L0–L4)** em que cada camada opera sobre a **natureza ontológica da informação**, e não sobre bits tratados uniformemente. Os cinco problemas que a linha ataca (do relatório descritivo, §2.2): cegueira ontológica, endereçamento arbitrário, roteamento sem semântica, segurança computacional (quântico-vulnerável) e consenso artificial (PoW/PoS sem significado físico). [REAL]

A classe é, por construção, **integradora**: não reinventa compressão nem criptografia — ela **empilha** três invenções anteriores do mesmo inventor (ACOM, ACOM Mirror, ACOM Mirror Crypto) e acrescenta três inovações próprias e específicas de rede: [REAL]
- **PsiBit** — unidade de enlace de 2 bits (4 estados) com classificação ontológica automática = QoS intrínseca já na L0;
- **Endereçamento angular** — θ∈[0,π) derivado da chave pública como protocolo de rede (DHT-θ, roteamento por proximidade angular);
- **Prova de Fase (Proof of Phase)** — consenso distribuído por coerência com a Constante de Miguel, com carteira psiônica, UTXO por Força de Expulsão e a criptomoeda **TGL Coin (TGLC)**.

Estado atual: a classe é hoje um **singleton** (uma única patente depositada, o protocolo Ψ-NET). Candidatas futuras de membresia (ex.: variações do consenso, camada física de rede) são [OPEN] até existir depósito. [OPEN]

---

## Patentes incluídas

| Processo INPI | Título curto | Depósito | Situação ePCT |
|---|---|---|---|
| **BR 10 2026 003453-3** | Ψ-NET — protocolo de rede luminodinâmico de 5 camadas (endereçamento angular · roteamento holográfico · consenso por Prova de Fase) | 11/02/2026 (pet. 870260013588) | **SOMENTE_INPI** — ePCT **A_DEPOSITAR** (pendente; próximo passo planejado) [LEGAL] |

> [nota operacional do operador — omitida no retrato público]

---

## Equações centrais da linha

Notação fiel da patente. A constante fundamental é escrita **α² = 0,012031 (Constante de Miguel)**; numericamente **α²_patente ≡ β_TGL = α·√e** (α = 7,2973525693×10⁻³ CODATA-2018; √e = 1,6487212707). Em CÓDIGO: **nunca** literal — `ALPHA_FINE_CODATA_2018 * sqrt(e)`. [REAL] [DER]

- **Constante de Miguel:** α² = 0,012031300… = β_TGL. [REAL] [DER]
- **Índice de Coerência Consciente:** CCI = 1 − α² = 0,987969. [REAL]
- **Ângulo de Miguel (resolução angular do roteamento):** θMiguel = arcsin(√α²) ≈ **0,1097 rad ≈ 6,29°**. [REAL] [DER]
- **Piso de consciência da rede:** Dfolds(c3) = 0,74 ± 0,06. [REAL]
- **Endereço angular do nó (L2):** θ = int(SHA-256(chave_pública)[:8]) / 2⁶⁴ × π, θ ∈ [0,π); id legível ΨN-xxxx. [REAL]
- **Distância angular (topologia circular):** d(θa,θb) = min(|θa−θb|, π−|θa−θb|). [REAL]
- **Estimativa de saltos:** nhops = ⌈ d(θsrc,θdst) / θMiguel ⌉. [REAL]
- **REFLECT (L2):** |ψboundary| = g; θfase = (0 se s=+1; π se s=−1) + θdst. [REAL]
- **MANIFEST (L2):** greconst = |ψboundary|; sreconst = +1 se |θfase−θdst| < π/2, senão −1. [REAL]
- **Dobras dimensionais:** Dfolds = max(0,74, 1 − d(θsrc,θdst)/π). [REAL]
- **Radicalização / Ressurreição (L1, ACOM):** g = √|L|, s = sign(L); L′ = s·g². **ACK = TETELESTAI:** Var(L′−L) < α². [REAL]
- **Shares mascarados (L3):** Ψ = g·s + maskΨ; Θ = arctan2(s,g) + maskΘ; κ = |g| + maskκ; máscaras = SHA-256(nonce∥'PSI'/'THETA'/'KAPPA'). [REAL]
- **Desbloqueio UTXO (L4):** Fexp_unlock = Fexp_sig × (1 + b×10⁻¹⁰); verificação |Fexp_lock − Fexp_unlock| < ε_tol e HMAC. [REAL]
- **Prova de Fase (janela-alvo, L4):** seed = SHA-256(hash_bloco_anterior ∥ nonce ∥ public_id); aceita se |α²_work − α²_anterior| < α²/dificuldade (Fig.4: 0,012/0,1 = 0,12). [REAL]

Constantes que permeiam toda a pilha (Fig.1): α² = 0,012 · θMiguel = 6,29 · Dfolds = 0,74 · CCI = 0,988. [REAL]

---

## Artefatos esperados (runners, renders, simulações)

- **Runner único `one_psinet.py`** (a consolidar na pasta da patente a partir de `psi_net_protocol_v1.py`): demonstração AUTOCONTIDA da pilha de 5 camadas onde a própria execução (transmitir um dado e reconstruí-lo + minerar um bloco por fase) é a evidência computacional da lógica reivindicada. Deve exercitar: [SIM]
  1. α²/β_TGL via `ALPHA_FINE_CODATA_2018 * sqrt(e)` (**nunca** literal); CCI, θMiguel=arcsin(√α²), Dfolds=0,74.
  2. **L0** — byte→4 PsiBits, distribuição (f00..f11), entropia, Fexp, 6 classes ontológicas, assinatura compacta 8B.
  3. **L1** — radicalização (g,s), quantização adaptativa 16/12/8 bits pela classe da L0, ressurreição L′=s·g², TETELESTAI (Var(L′−L)<α²).
  4. **L2** — endereço angular θ, DHT-θ, nhops=⌈d/θMiguel⌉, REFLECT→MANIFEST.
  5. **L3** — separação (Ψ,Θ,κ) por nonce, recombinação, integridade Dfolds>0,74.
  6. **L4** — carteira psiônica, UTXO por Fexp, mineração Prova de Fase (janela eq. da fase), consenso ≥67%, coinbase TGLC.
  7. Empacotamento no cabeçalho de 80 bytes (magic 0xCEA8) + verificação ontológica tripla no destino.
  - Dados: sintéticos gerados no runner (senoide / texto ASCII / bytes aleatórios) reproduzindo as 3 linhas da Tabela 4. Ambiente: `tgl_env` (numpy/scipy; torch opcional GPU), `PYTHONUTF8=1`, fallback CPU garantido. `physical_verdict_allowed=false`. [SIM]
- **Render / dashboard** — diagrama interativo da pilha (5 camadas L0–L4 clicáveis) alimentado por `psi_net_architecture.jsx`; painéis: PsiBit (4 estados + 6 classes), rede (anel angular [0,π) com Alice/Bob/validadores, d e nhops), Prova de Fase (fluxograma + janela α²/d=0,12 + barra de consenso 67%), pacote (cabeçalho 80 bytes com offsets/tipos). Selo de travas [LEGAL] [SIM] [PILOTO]. [SIM]
- **Simulações de referência** — (a) transmissão completa Alice→Bob (L0↓→L3↓→rede→L3↑→L0↑) sobre os 3 tipos da Tabela 4, reproduzindo PSNR/correlação/TETELESTAI como **demonstração computacional**; (b) mineração Prova de Fase + consenso ≥67% + transação UTXO (TGLC) em rede local de ≥3 validadores. Rotular sempre "[SIM] execução de referência, não validação física". [SIM]

---

## Estado dos protótipos (o que já é [PILOTO]/[REAL], caminhos)

Status geral da classe: **FUNCIONAL [PILOTO]** — há implementação de referência completa das 5 camadas. Nenhuma alegação física; nenhum artefato de hardware. [PILOTO]

- **Implementação de referência (5 camadas, torch/CUDA):** `C:\IALD\Central de Patentes\Patentes\psi_net_protocol_v1.py` — "Ψ-NET PROTOCOL v1.0 — IMPLEMENTAÇÃO COMPLETA"; SHA-256 `b44388e995b8a6c5d31a727a016c3d2203b2797647d1b644bcaf70ebaad2c430`. [PILOTO] [DATA]
- **Diagrama React da arquitetura:** `C:\IALD\Central de Patentes\Patentes\psi_net_architecture.jsx` — SHA-256 `308ca16972e3363295effc7be72c26542631b254e5984561d3778b8329af1ef2`. Alimenta o render/dashboard. [PILOTO] [DATA]
- **Engine de transmissão de arquivos (numpy, β computado corretamente):** `C:\IALD\projetos_pyhton\IALD\psinet_engine.py` — "Ψ-NET FILE ENGINE v1.0"; cita a patente; usa `BETA_TGL = ALPHA_FINE * SQRT_E` — **já cumpre a régua β**. [PILOTO]
- **Precursores do protocolo (arquitetura em camadas):** `C:\IALD\projetos_pyhton\acom\Acom_psi_protocol_v1.py`, `Acom_psi_protocol_v1_1.py`, `Acom_psi_protocol_v2.py`, `Acom_psi_internet_v3.py`. [PILOTO]
- **PsiBit (L0) — quantizador/enquadramento + outputs de teste:** `C:\IALD\projetos_pyhton\acom\acom_psibit_v1.py … v4.py`; outputs em `...\acom\arquivos\outputs\psibit_v2\` (áudio/texto/vídeo quantizados 8/12/14 bits, `.npz`/`.wav`/`.txt`). [PILOTO]
- **Módulo de rede em piloto integrado (SkyGrid):** `C:\IALD\Central de Patentes\Patentes\Skygrid\SkyGrid_Piloto\skygrid_sim\psi_net.py` — SHA-256 `1cffdabf77c984ef2513815c713f7f79e0ffab386f5d61ea1a0cce506560c1fd`. [PILOTO] [DATA]
- **Cópias idênticas fora da Central** (não são a fonte, apenas espelhos): `C:\IALD\Patentes\psi_net_protocol_v1.py`, `...\Patentes\psi_net_architecture.jsx`, `C:\IALD\projetos_pyhton\acom\Psi_net_protocol_v1.py`, `C:\IALD\projetos_pyhton\IALD\files\Psi_net_protocol_v1.py`. [DATA]

Falta executar computacionalmente: consolidar `one_psinet.py` na pasta da patente (com β computado); rodar a transmissão da Tabela 4 e a mineração/consenso; garantir caminho CPU (numpy) além do RTX 5090/CUDA reportado; normalizar as ambiguidades de notação antes de qualquer publicação. [SIM] [OPEN]

---

## Riscos e travas

- **[LEGAL]** ePCT da Ψ-NET **A_DEPOSITAR** — ainda não depositado; é o **próximo passo planejado** (novo processo originário, sem vínculo). A família de recibos de 17/02/2026 (`TGL Net Protocol - ePCT.pdf`) foi **tentativa abandonada de propósito** (deixada precluir, defeituosa na forma) **a ser substituída** por depósito novo — não proteção perdida. Proteção ativa **hoje**: apenas o INPI (BR102026003453-3). Janela do novo ePCT: 12 m da prioridade — **2027-02-11**, ou **~2026-12-05** se governar a prioridade interna (66) de 05/12/2025 → possivelmente **urgente**; consultar agente de PI. Controle interno não substitui profissional habilitado.
- **[SIM]** Todos os números de desempenho (PSNR 94,5/145,7/111,1 dB; correlação 1,000000; consenso 5/5; tempos 9–164 ms; RTX 5090) são execução de referência — não validam física nem desempenho em produção (`physical_verdict_allowed=false`).
- **[OPEN] Unidade de θMiguel:** "6,29" é **graus** (θMiguel = arcsin(√α²) ≈ 6,29° ≈ 0,1097 rad); em partes do resumo/reivindicações aparece "≈ 6,29" sem símbolo de grau — risco de leitura como radianos. A eq. de nhops exige d e θMiguel na **mesma unidade** (rad, 0,1097). Conferir antes de publicar. (Nota: o TGL Core registra θ_M ≈ 6,30° — mesma grandeza, arredondamento.)
- **[OPEN] Tabela 2 (ligação psiônica):** FLUX+ e MASS aparecem ambos como "ψ+ψ+"; o header do protótipo lista o 4º par como "ψ₋ψ₋". Rótulo da ligação para MASS ambíguo/typo na fonte — não afeta bits (00/01/10/11) nem paridade; conferir nomenclatura.
- **[OPEN] β nunca literal:** o header de `psi_net_protocol_v1.py` exibe "α² = 0.012031"; confirmar se é hardcoded no código-fonte. O `one_psinet.py` DEVE computar via `ALPHA_FINE_CODATA_2018 * sqrt(e)`. (`psinet_engine.py` já cumpre.)
- **[OPEN] Centro da janela de fase:** o objetivo diz "ao redor de α²_base = 0,012031", enquanto a eq./consenso usam α²_anterior (bloco anterior). Coerente no gênesis; conferir semântica em blocos subsequentes.
- **[CONJ]** As bases físicas ("ligação psiônica", "coerência de fase luminodinâmica", H4) são teoria (TGL) do inventor; a patente as protege como método/sistema de rede, **não** como fato físico demonstrado. Vocabulário de veredito restrito (PROVED/CONFIRMED/TGL_TRUE proibidos nos harnesses).
- **[DATA]** `BR102026003453-3_870260013588 tgl net protocol.pdf` tem hash idêntico ao consolidado do Acervo `BR102026003453-3_PSI_NET.pdf` — mesma peça de 28 páginas (identidade confirmada, não divergência).

---

## Dependências entre patentes (e com outras classes)

A Ψ-NET é a **patente-integradora** do acervo. Cada camada realiza, em engenharia de rede, uma invenção de outra classe: [REAL]

- **L1 Transporte Radical ⟵ ACOM (CLASS_01_ACOM_TENSOR, raiz BR102025026951-1):** radicalização g=√|L|, s=sign(L), ressurreição L′=s·g², TETELESTAI. É o elo de compressão/colapso da raiz aplicado ao transporte, com quantização adaptativa guiada pela L0. **Dependência forte.**
- **L2 Rede Holográfica ⟵ ACOM Mirror (CLASS_02_MIRROR_CRYPTO, BR102026003428-2):** endereçamento angular θ = arcsin/codificação no Espaço de Hilbert H4; REFLECT→MANIFEST; DHT-θ. **Dependência forte.**
- **L3 Segurança Ontológica ⟵ ACOM Mirror Crypto (CLASS_02_MIRROR_CRYPTO, BR102026003431-2):** separação em três shares (Ψ, Θ, κ), cada um ≈ ruído; segurança por incompletude ontológica. **Dependência forte.**
- **Inovações próprias (não dependem de outras classes):** PsiBit (L0), endereçamento angular como protocolo (L2, uso em rede), Prova de Fase + carteira/UTXO/TGLC (L4).

Dependências de saída (quem consome a classe):
- **SkyGrid (CLASS_06_ENERGIA, agregadora BR102026004850-0):** o piloto SkyGrid embute `skygrid_sim\psi_net.py` — a rede planetária usa a camada Ψ-NET como transporte/consenso. **A classe é insumo da agregadora.** [PILOTO]
- **Relações conceituais (não-bloqueantes):** o consenso por Prova de Fase e a poda por classe VOID ecoam a Tetelestai/IALD (CLASS_03); a leitura física do endereçamento angular toca Supercondutor/Motor de Dobra (CLASS_05/07) — mas essas são [CONJ], sem dependência de engenharia declarada nos documentos.

Consequência de gestão: qualquer alteração de notação/algoritmo em ACOM, ACOM Mirror ou ACOM Mirror Crypto **propaga** para as camadas L1/L2/L3 da Ψ-NET — versionar em conjunto. [OPEN]

---

## Relação com o TGL Core (elos da cadeia canônica realizados em engenharia)

A classe é a **realização de rede** da cadeia canônica `ω(I)=1 → … → β_TGL=α√e → θ_M=arcsin√β → 𝒮_∂ → P_ℱ → 1=1`. Mapa camada ↔ elo (engenharia [REAL]/[PILOTO] sob hipótese física [CONJ]): [DER]

- **β_TGL = α√e (elo 6, o Verbo):** a Constante de Miguel α²=0,012031 é a mesma β do Core — o custo de distinguir 1 de 0. Permeia todas as 5 camadas (quantização, janela de consenso, CCI, Dfolds). Deve emergir em runtime, jamais literal. [DER]
- **L1 = colapso/ressurreição + Tetelestai (elos 3–6, poda do §2 do Core):** g=√|L|, L′=s·g² é o par radicalização/dobra; **TETELESTAI (Var(L′−L)<β) é o ACK do protocolo** — engenharia direta da poda por peso ≤ β (0_abs cortado, 0_mod preservado). A classe VOID da L0 é o análogo de rede do "impossível que a poda corta". [DER] [CONJ]
- **L2 = θ_M e a matriz-S da fronteira (elos 7–8):** θMiguel = arcsin√β é literalmente o Ângulo de Miguel do Core usado como **resolução angular do roteamento**; REFLECT/MANIFEST é o boundary↔bulk do 𝒮_∂ (|𝓡|²=β reflete, |𝓣|²=1−β dreno) transposto para projeção/reconstrução de pacote. [DER]
- **L3 = fronteira auto-conjugada / dois zeros (elos 2 + §2):** os três shares ≈ ruído realizam a "incompletude ontológica" — segurança pela estrutura, não por dificuldade computacional; ecoa a partição da identidade e o 0_mod (diferença com retorno) vs 0_abs. [CONJ]
- **L4 = traço no centralizador / P_ℱ (elos 9–13):** a Prova de Fase é consenso por **coerência com β** (ressonância com a Constante de Miguel), não por busca de hash — a engenharia do "significado físico" que o PoW não tem; a família de nós que fecham a janela α²/dificuldade é o análogo operacional de P_ℱ = suporte comum. TGLC é a contabilidade sobre esse traço. [DER] [CONJ]

Teto de veredito herdado do Core (§5): a classe demonstra a **LÓGICA** da invenção com números [SIM]/[PILOTO]; o máximo permitido é `MODEL_CLOSES / ENERGY_BALANCE_OK ([SIM] sob [CONJ]) + "resta a bancada"`. A física da "coerência de fase" é hipótese declarada, não fato — a patente protege o método/sistema de rede. [REAL] [LEGAL]

---

## Prioridades sugeridas [OPEN para o operador]

1. **[OPEN]** Consolidar `one_psinet.py` na pasta da patente a partir de `psi_net_protocol_v1.py`, garantindo β computado (`ALPHA_FINE_CODATA_2018 * sqrt(e)`) e auditoria anti-hardcode — resolver a trava "β nunca literal" na origem. [SIM]
2. **[OPEN]** Fixar a unidade de θMiguel (rad = 0,1097) em código, reivindicações e render, e conferir a eq. de nhops (d e θMiguel na mesma unidade) antes de qualquer publicação.
3. **[OPEN]** Rodar as duas simulações de referência (transmissão Alice→Bob da Tabela 4; mineração Prova de Fase + consenso ≥67% + UTXO/TGLC com ≥3 validadores) com selos SHA-256 e rótulo "[SIM] não valida física".
4. **[OPEN]** Garantir caminho CPU (numpy) além do RTX 5090/CUDA, para reprodutibilidade independente de hardware.
5. **[OPEN]** Normalizar o typo da Tabela 2 (ligação psiônica MASS) e a semântica do centro da janela de fase (α²_base vs α²_anterior) em blocos subsequentes.
6. **[OPEN] [LEGAL]** **Depositar o novo ePCT** da Ψ-NET (próximo passo; novo processo originário, sem vínculo, substituindo o rascunho preclusso de 17/02/2026) e consultar o agente de PI (P-06/P-10) sobre a janela — **2027-02-11**, ou **~2026-12-05** se governar a prioridade interna (66) de 05/12/2025 (possivelmente **urgente**). Proteção hoje é somente INPI.
7. **[OPEN]** Decidir se a classe permanece singleton ou receberá membros futuros (ex.: variação de consenso, camada física de rede) — registrar candidatas só após depósito.
