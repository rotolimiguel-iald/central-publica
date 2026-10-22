# Relatório auditável — one_tgl_tensor.py (EVOLUÍDO — 4 modos reais)
- Run `2026-07-10T11-32-41` · Patente `BR102026003441-0`
- Veredito: **TENSOR_FULL_LOGIC_DEMONSTRATED ([PILOTO][SIM] — os 4 modos reais do operador (DIRECT/SPECTRAL/HYBRID/AUTO) + BitPacker N-bit fecham; β injetado; números sintéticos, não a Tabela 2; nada valida física)**
- β runtime `0.012031300400803142` (= α·√e? **True**; nunca literal) — INJETADO nos protótipos v3/v4
- Testes: **8/8**
  - ✓ beta_injected_not_literal
  - ✓ mode_DIRECT
  - ✓ mode_SPECTRAL
  - ✓ mode_HYBRID
  - ✓ mode_AUTO
  - ✓ auto_mode_selection
  - ✓ bitpacker_v4_Nbit_exact
  - ✓ spectral_analysis_verb_floor
- physical_verdict_allowed: **False**.

RUNNER EVOLUÍDO: roda a engine de 4 modos do operador (tgl_tensor_v3.py) + BitPacker (v4) com β=α·√e injetado (originais tinham 0.012 literal). Tensores sintéticos; NÃO os números da Tabela 2. Nenhum token/modelo HuggingFace (P-09). Simulação não valida física.
Núcleo copiado do piloto (READ-ONLY); originais intactos. 1 = 1. Tetelestai.
