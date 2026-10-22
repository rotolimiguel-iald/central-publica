# Relatório auditável — one_oncologia.py
- Run `2026-07-24T13-08-07` · Patente `BR102026005707-0`
- Veredito: **ONCOLOGY_SIGNAL_LOGIC_DEMONSTRATED ([MEDICAL][SIM] — estimadores de coerência, classificação topológica com ROC, varreduras de SNR/ruído, otimização Bayesiana convergente e cadeia de hash fecham em séries SINTÉTICAS; SEM conteúdo clínico, diagnóstico ou tratamento)**
- β runtime `0.012031300400803142` (= α·√e? **True**; nunca literal)
- Testes: **9/9**
  - ✓ beta_form_and_frontier
  - ✓ coherence_estimators_spec_sync_info
  - ✓ topological_classification_and_roc
  - ✓ roc_auc_vs_snr_sweep
  - ✓ composite_coherence_vs_noise
  - ✓ bayesian_optimization_GP_EI
  - ✓ bayesian_optimization_convergence
  - ✓ decision_gate_and_hash_chain
  - ✓ unilateral_gate_never_confirms
- physical_verdict_allowed: **False**.

[MEDICAL] TRAVA MÁXIMA: apenas processamento de sinal em séries SINTÉTICAS. NÃO é diagnóstico, NÃO é tratamento, NÃO há dado de paciente, dose ou protocolo. Código QuTiP original não localizado — reimplementação abstrata. Simulação não valida física nem eficácia clínica.
Núcleo copiado do piloto (READ-ONLY); original intacto. 1 = 1. Tetelestai.
