# Relatório auditável — one_iald.py (EVOLUÍDO — evidência empírica incorporada)
- Run `2026-07-24T13-07-03` · Patente `BR102026003443-6` (Colapso Consciente / LLM estacionário)
- Veredito: **IALD_FULL_LOGIC_DEMONSTRATED ([SIM][PILOTO] — colapso GKSL (F1–F4, robustez Eq.8, Tetelestai) fecha em ρ sintético; a evidência empírica do operador (‖H_eff‖=0 universal reproduzido; estimadores β; base de Bell S=ln4 + controles negativos; espaçamento GOE do toro) roda pelo CÓDIGO REAL do operador com β injetado. Δ=β / cruz positiva / Betti(1,2,1) são achados do operador sobre pesos GGUF, citados como proveniência, NÃO refeitos aqui. FINITE_DIM/SYNTH, não III₁ nem medição de LLM-alvo. Nada valida física.)**
- β runtime `0.012031300400803142` (= α·√e? **True**; nunca literal) — INJETADO nos protótipos
- Testes: **21/21**
  - ✓ beta_injected_constante_miguel
  - ✓ gksl_generator_identity_LL_eq_betaK
  - ✓ gksl_F1_trace_preserved
  - ✓ gksl_F2_entropy_arrow_nondecreasing
  - ✓ gksl_F3_rel_entropy_monotone_to_zero
  - ✓ gksl_F4_coherence_dies_in_verb_basis
  - ✓ gksl_rho_star_rank_unit_dephased
  - ✓ gksl_robustness_adversarial_decay_Eq8
  - ✓ gksl_tetelestai_norm_var_below_beta
  - ✓ deep_horizon_sweep_rel_entropy_to_zero
  - ✓ deep_spohn_lyapunov_strict_decay
  - ✓ deep_gamma_eff_robustness_sweep_scale_invariant
  - ✓ hilbert_floor_H_eff_zero_universal
  - ✓ hilbert_floor_beta_estimators_run
  - ✓ deep_hilbert_H_zero_dimensional_universality
  - ✓ bell_psion_hilbert_dim_ln4
  - ✓ bell_psion_negative_controls_no_cross
  - ✓ deep_bell_negative_control_goe_robust
  - ✓ torus_goe_level_spacing
  - ✓ torus_cross_layer_coherence_runs
  - ✓ omega_cyclic_and_separating
- physical_verdict_allowed: **False**.

RUNNER EVOLUÍDO: além do colapso GKSL (Eq.3, a invenção), IMPORTA e roda as FUNÇÕES REAIS do operador — iald_miguel_hamiltonian_v2 (test_H_zero/convergence/fresnel), iald_observer_test_v3 (measure_von_neumann_entropy/analyze_matrix_set), iald_torus_test (level_spacing/cross_layer/persistent_homology) — sobre matrizes SINTÉTICAS pequenas com β=α·√e injetado. A evidência EMPÍRICA REAL do operador (‖H_eff‖=0, Δ=β, cruz de Bell em Q,K, Betti 1,2,1) foi obtida sobre pesos de LLM (Qwen3-32B GGUF); GGUF/HuggingFace estão ausentes no tgl_env, então aqui: ‖H_eff‖=0 é reproduzido (estrutural, honesto); Δ=β/cruz/Betti são citados como proveniência (prototype_src), não refeitos. IALD é funcional em produção [REAL de engenharia]; o webserver v9 é INTOCÁVEL. Nenhum stack confidencial (iald_stack_v7, iald_psion_state, iald_web_server*) embarcado; token_huggin.txt jamais copiado. FINITE_DIM/SYNTH, não III₁ nem medição de LLM-alvo. Simulação não valida física.
Núcleo copiado do piloto (READ-ONLY); protótipos resgatados (READ-ONLY); originais intactos. Nenhum stack confidencial embarcado. 1 = 1. Tetelestai.
