# Relatório auditável — Dípolo Transistor one_dipolo.py

- Run `2026-07-15T21-15-21` · Patente `BR102026004688-4`
- Veredito: **DIPOLO_SWITCHING_LOGIC_DEMONSTRATED ([SIM][HARDWARE][PILOTO] — máquina de estados de chaveamento por piso do Verbo fecha; dispositivo físico NÃO construído, dinâmica quântica QuTiP ausente)**
- β runtime `0.012031300400803142` (= α·√e? **True**; nunca literal)
- Testes: **9/9**
- Porta aberta (MANIFEST) com round-trip exato; porta fechada (REFLECT) em sinal ausente
- Piso do Verbo β·g_max separa sinal de ruído dephased · fração@β = `0.9997`
- **Varredura de limiar**: 101 pontos f∈[0,1]; curva de sobrevivência monotônica; β é um ponto dela
- **6 famílias de sinal**: gaussiano→MANIFEST, pico_esparso→MANIFEST, uniforme→MANIFEST, exponencial→MANIFEST, bimodal→MANIFEST, ausente→REFLECT
- **Cobertura FSM**: 100% (4/4 transições) · determinística
- Figuras: []
- physical_verdict_allowed: **False**.

[SIM][HARDWARE] Dispositivo físico não construído/medido; dinâmica quântica QuTiP ausente. Núcleo copiado do piloto (READ-ONLY); original intacto. 1 = 1. Tetelestai.
