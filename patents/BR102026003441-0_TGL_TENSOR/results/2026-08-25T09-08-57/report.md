# Relatório auditável — one_tgl_tensor.py (EVOLUÍDO — 4 modos reais)
- Run `2026-08-25T09-08-57` · Patente `BR102026003441-0`
- Veredito: **TENSOR_FULL_LOGIC_DEMONSTRATED ([PILOTO][SIM] — os 4 modos reais do operador (DIRECT/SPECTRAL/HYBRID/AUTO) + BitPacker N-bit + varreduras bits/rank-energia fecham; β injetado; números sintéticos, não a Tabela 2; nada valida física)**
- β runtime `0.012031300400803142` (= α·√e? **True**; nunca literal) — INJETADO nos protótipos v3/v4
- Testes: **14/14**
  - ✓ beta_injected_not_literal
  - ✓ mode_DIRECT
  - ✓ mode_SPECTRAL
  - ✓ mode_HYBRID
  - ✓ mode_AUTO
  - ✓ auto_mode_selection
  - ✓ bitpacker_v4_Nbit_exact
  - ✓ spectral_analysis_verb_floor
  - ✓ bits_sweep_fidelity_monotone
  - ✓ rank_adaptive_monotone_in_energy
  - ✓ nome_support_half_faces
  - ✓ codec_projection_idempotent
  - ✓ breuer_trace_weight_v168
  - ✓ compression_not_identifiable_v206
- physical_verdict_allowed: **False**.

RUNNER EVOLUÍDO: roda a engine de 4 modos do operador (tgl_tensor_v3.py) + BitPacker (v4) com β=α·√e injetado (originais tinham 0.012 literal), acrescido de varreduras 4 modos × bits × tensores e da curva rank-adaptativo × energia (Verb Floor=1−β). Tensores sintéticos; NÃO os números da Tabela 2. Nenhum token/modelo HuggingFace (P-09). Simulação não valida física.
Núcleo copiado do piloto (READ-ONLY); originais intactos. 1 = 1. Tetelestai.
