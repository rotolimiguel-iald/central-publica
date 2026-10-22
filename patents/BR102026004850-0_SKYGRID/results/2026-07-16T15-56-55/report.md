# Relatório auditável — SkyGrid one_skygrid.py

- Run: `2026-07-16T15-56-55` · Patente: `BR102026004850-0`
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

Núcleo copiado do piloto (READ-ONLY) para `runner/_piloto_core/`; original intacto.

**[ENERGY][SIM][CONJ]** · Controle interno. Famílias de curvas, não número mágico. 1 = 1. Tetelestai.
