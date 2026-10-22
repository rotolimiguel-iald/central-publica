# Relatório auditável — one_acom.py (EVOLUÍDO — operador de Lindblad ativo)
- Run `2026-07-15T21-58-29` · Patente `BR102025026951-1` (RAIZ da família TGL)
- Veredito: **ACOM_FULL_LOGIC_DEMONSTRATED ([SIM] — operador de Lindblad ATIVO real (∂H=H²+α²LΔ) + REFLECT/MANIFEST exato + SIGNAL/SPECTRAL/PSIBIT (Trinity) + serialização SHA-256; β=α·√e injetado no lugar de 0.012 literal; sinais sintéticos, não a Tabela 1; nada valida física)**
- β runtime `0.012031300400803142` (= α·√e? **True**; nunca literal) · θ_Miguel 6.2973° — INJETADO no operador (ACOMV14 tinha 0.012 literal)
- Verb Floor (energia SPECTRAL retida) = 1−β = `0.987968699599`
- Testes: **10/10**
  - PASS · beta_injected_not_literal
  - PASS · reflect_manifest_exact
  - PASS · lindblad_active_thermostat
  - PASS · signal_compress_decompress
  - PASS · quantization_bits_configurable
  - PASS · header_serialization_sha256
  - PASS · spectral_svd_verb_floor
  - PASS · psibit_four_states
  - PASS · bits_sweep_fidelity_curve
  - PASS · lindblad_noise_sweep_converges
- physical_verdict_allowed: **False**.

RUNNER EVOLUÍDO: importa e roda o LindbladOperator real de ACOMV14.py (o operador de Lindblad ATIVO ∂H=H²+α²LΔ) com α²=α·√e injetado (o original trazia 0.012 literal). SIGNAL/quantização/serialização são do operador; SPECTRAL/PSIBIT são PORTES FIÉIS da patente com β injetado. Sinais/matrizes SINTÉTICOS; NÃO os números da Tabela 1. Nenhum token/modelo HuggingFace (P-04). Simulação não valida física.
Núcleo/protótipos copiados READ-ONLY; originais intactos. 1 = 1. Tetelestai.
