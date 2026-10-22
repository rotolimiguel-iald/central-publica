# Relatório auditável — SkyGrid one_skygrid.py

- Run: `2026-08-30T06-57-36` · Patente: `BR102026004850-0`
- Veredito máximo: **MODEL_CLOSES / ENERGY_BALANCE_OK ([SIM] sob [CONJ])**
- β runtime: `0.012031300400803142` (= α·√e? **True**; nunca literal)
- Testes v3: **44** · invariants_hash: `6bfef5f6d45b5136d6966cb4fbe3ad9da611afb5f460bb1cf26efd9603ce47f5`
- physical_verdict_allowed: **False** — simulação não valida física.
- η_sys: `0.6704569384754266` · resíduo: `8.149072527885437e-10 J`

## Varreduras de projeto [SIM] (aprofundamento)

- Famílias varridas: **6** (Q, eta_geo, S_field_W_m2, eta_rt, f_drive_MHz, n_sats) · **52** pontos, cada um re-auditando a conservação (fail-closed).
- Balanço fecha em TODOS os pontos: **True**.
- Curva de ressonância: pico em `1667.3590` MHz = ω_OH (`1667.3590`) → ressonante? **True**.
- Ponto de operação: P=3278 W · η_sys=0.268.
- Checks de varredura: **4/4** — {'sweeps_all_points_balanced': True, 'resonance_peak_at_omega_OH': True, 'constellation_scaling_monotone': True, 'operating_point_physical_range': True}
- Figuras novas: `fig_resonance.png`, `fig_scaling.png`.

## Amplificacao v138 [DER] — known-composed + cone emergente

- Teste `known_composed_cone_identity`: **True** — cone nulo no ansatz cosh (kappa^2 = beta runtime): resid_cone = `4.615e-13`, Bianchi G00=G11=0 resid `1.657e-13`, G22-beta resid `1.163e-11` (72 amostras nulas).
- Meta-composicao (16 blocos): estavel sob sort = True, sensivel a 1 bit = True (`b7faecdded88b570...`).
- [DER] sombra matematica; NAO e veredito fisico.

## Amplificacao v144 [DER] — o fechamento da compilacao (ledger + meta-cadeia)

- Teste `compilation_closure_ledger`: **True** — meta-cadeia `94d0c97cd81a5646...` (64 hex = True), DETERMINISTICA sob 8 re-ordenacoes = True, SENSIVEL a 1 bit em qualquer modulo = 16/16.
- Ledger do fechamento (CODE_CLOSURE_COMPLETE, um.py v143): 8 itens, 3 abertos, todos com fiador em {BY_DESIGN, EXTERNAL_KNOWN, NAMED_PROGRAM} = True; compilacao com aberto ORFAO rejeitada (assert negativo) = True; fiador invalido rejeitado = True.
- Ancora no artefato vivo `skygrid_compilation.json` (READ-ONLY): {'path': 'skygrid_compilation.json', 'meta_cadeia_real': '8179118dd12f7296', 'meta_cadeia_64hex': True, 'n_entries': 16, 'all_16_entries_ok': True, 'this_patent_listed': True}.
- [DER]/[SIM] gramatica de compilacao; physical_verdict_allowed=false; beta runtime, nunca literal.

## Amplificacao v143-lift [DER] — o levantamento global condicional (pedra 99)

- Teste `global_lift_conditional_expectation`: **True** — Takesaki finito na forma da eq. (5) da patente: theta_M = `0.109908` (arcsin(sqrt(beta)) runtime); juramento mantido delta_inv = `0.000e+00` < tol reivind. 7 (`1e-04`) ==> E covariante: local `0.000e+00`, LIFT global E1(x)E2 em 16 dim `0.000e+00` (rho-preservante: local `0.000e+00`, global `0.000e+00`).
- CONTROLE NEGATIVO: no com juramento QUEBRADO (delta_inv = `2.632e-01` > tol) ==> covariancia FALHA: local `2.205e-01`, e 1 no ruim derruba o GLOBAL `2.696e-01` (Prova de Fase); E' nao rho-preservante (defeito `2.928e-03`).
- Periodo modular DERIVADO: sigma_(2pi/theta_M) = id na subalgebra invariante (resid `6.026e-15`); o MEIO-periodo NAO retorna (defeito `2.000`).
- [DER]/[SIM] sombra matematica; physical_verdict_allowed=false; beta runtime, nunca literal.

## Amplificacao v168 [DER] — a media de Birkhoff e a fase LOCK (ONDA 3)

- Teste `ergodic_mean_phase_lock`: **True** — ErgodicMeanSection (um.py v166-v167, item A em kernel): a media (1/N) sum U^k converge a projecao invariante. Instanciada no A_phi (eq. 5) e no REFLECT->LOCK da crl-TGL: theta_M = `0.109908` (arcsin(sqrt(beta)) runtime); peso do LOCK tau(P) = `2.0` (o peso e TRACO — eco BreuerTrace: tau(a*a) = `2.000000000000` = tau(aa*) = `2.000000000000`); secao equivariante [U,P] = 0 (resid `0.000e+00`, eco EquivariantSection).
- Convergencia com bound derivado C = 1/sin(theta_M/2) = `18.206`: err(N=100) = `1.290e-01`, err(N=10000) = `4.267e-04` (bound C/N em todos = True); reivindicacao 7 como criterio: N_min = `182062` ciclos ==> err = `7.822e-05` < `1e-04` = **True**.
- NEGATIVOS (fail-closed): U adulterado (perturbacao = beta) RECUSADO pelo gate = True; secao FALSA sobre drift rejeitada (defeito equivar `1.097e-01`, gap da media `1.000`) = True; media INSUFICIENTE (N = `1820`) NAO cumpre a reivind. 7 (err = `4.921e-03` > tol) = True.
- [DER]/[SIM] sombra do teorema ergodico de von Neumann; physical_verdict_allowed=false; beta runtime, nunca literal.

## Amplificacao v206 [DER] — a maquina do veredito-alvo (ONDA 4)

- Teste `verdict_target_machine_claim16`: **True** — a MAQUINA DO VEREDITO-ALVO (um.py v200, custodia um_unificado_v206) instanciada na reivindicacao 16 (C1..C5 SIMULTANEOS) e na Camada 4 (rito multicanal com placebo): a maquina NUNCA declara — computa fail-closed sobre os numeros REAIS desta run.
- Canais emitidos: **6/6** (C1 ressonancia na banda da reivind. 16: f_peak = `1667.359` MHz em [1607, 1727]; C2 duplo trilho; C3 armazenamento; C4 controle distribuido; C5 beta runtime; H2 placebo nulo); exclusoes MEDIDAS: **6** (residuo `8.149e-10` J; colapso fora-da-banda em 4 pontos).
- Veredito emitido (o limite NO NOME): `SKYGRID_C1_C5_SIMULTANEOUS_ON_THE_DIGITAL_BENCH__ALL_CHANNELS_EMITTED__ZERO_REFUTATIONS__EXCLUSIONS_MEASURED__SIM_ONLY__NOT_A_CONFIRMATION`.
- NEGATIVOS por logica (a recusa e o bootstrap em ato, eco v205): canal pendente RECUSA = True; canal refutado derruba (classificador NOT_REFUTED correto) = True; palavra proibida em canal => RECUSA = True; ledger insuficiente => RECUSA = True; bancada morta => RECUSA = True.
- Duas clausulas da Gate (eco kernel TheIALDSelector, `iald_selects`, estrutura re-derivada numericamente): alvo intacto XOR recusa com razoes, nada no meio, nos 6 desfechos = True; maquina idempotente (I^2 = I).
- [DER]/[SIM] canais SIM_ONLY (gemeo digital, nao dado publico fisico); physical_verdict_allowed=false; beta runtime, nunca literal.

Núcleo copiado do piloto (READ-ONLY) para `runner/_piloto_core/`; original intacto.

**[ENERGY][SIM][CONJ]** · Controle interno. Famílias de curvas, não número mágico. 1 = 1. Tetelestai.
