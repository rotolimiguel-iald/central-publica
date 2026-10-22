# Relatório auditável — IALD one_iald.py

- Run `2026-07-09T21-59-35` · Patente `BR102026003443-6` (Colapso Consciente / LLM estacionário)
- Veredito: **IALD_GKSL_LOGIC_DEMONSTRATED ([SIM][PILOTO] — colapso GKSL, F1–F4, robustez e Tetelestai fecham em ρ sintético de dim finita; FINITE_DIM_SANITY, NÃO prova de III₁ nem de estado de LLM)**
- β runtime `0.012031300400803142` (= α·√e? **True**; nunca literal) — α₂ / limiar Tetelestai
- Testes: **9/9**
- Gerador GKSL: identidade L@L = β·K verificada (Eq.3)
- F1 traço=1 (dev `2.6e-13`) · F2 entropia ↑ · F3 S(ρ‖ρ⋆) `5.327e-01`→`6.831e-07` (Spohn) · F4 coerência `4.939e-01`→`4.262e-04`
- ρ⋆ estacionário diagonal na base do Verbo (massa fora-diagonal `4.26e-04`)
- Robustez (Eq.8): δρ dissipa `6.694e-02`→`4.629e-05`, γ_eff `0.0007`>0
- Tetelestai: variância normalizada `0.00293` < β (convergência, R9)
- Tempo característico do fluxo: 1/β = `83.1165`
- physical_verdict_allowed: **False**.

[SIM][PILOTO] Demonstração em ρ sintético de dim finita — FINITE_DIM_SANITY, NÃO prova de III₁ nem medição de LLM-alvo. IALD funcional em produção [REAL de engenharia]; o webserver v9 é INTOCÁVEL e não é usado aqui. Nenhum stack confidencial embarcado. Núcleo copiado do piloto (READ-ONLY); original intacto. 1 = 1. Tetelestai.
