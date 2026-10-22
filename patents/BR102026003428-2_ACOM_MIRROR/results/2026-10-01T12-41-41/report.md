# Relatório auditável — ACOM Mirror one_acom_mirror.py (EVOLUÍDO — engine v17.0 real)

- Run `2026-10-01T12-41-41` · Patente `BR102026003428-2` (2.ª da família ACOM; prioridade interna 66 → raiz 05/12/2025)
- Veredito: **MIRROR_FULL_LOGIC_DEMONSTRATED ([PILOTO][SIM] — a engine de referência v17.0 real do operador (DimensionalMirror REFLECT/MANIFEST + ACOMv161 comparador, zstd) fecha em SIMULAÇÃO; codificação angular arcsin, Fexp/Sψ e a tabela v16.1×v17.0 reais; β injetado; números sintéticos, NÃO a Tabela 2; nada valida física)**
- β runtime `0.012031300400803142` (= α·√e? **True**; nunca literal) — INJETADO no protótipo v17 (que tinha `ALPHA2=0.012` literal). α² é NOMINAL: não entra na transformada.
- θ_Miguel `6.2973°` (= arcsin(√β)? **True**)
- Testes: **22/22** · Figuras: **6** ['fig_codificacao_angular.png', 'fig_tabela_compressao.png', 'fig_roundtrip_gradientes.png', 'fig_sweep_bitdepth_v17.png', 'fig_curva_corr_ratio.png', 'fig_fexp_spsi_regimes.png']
- Correlação (v17 engine): mín `0.999948`, média `0.999979` (reiv. 9: > 0,999)
- Razão de compressão média v17 `20.36×` · Δ médio v16.1→v17 `-20.9%` (medido, não o +21,3% de produção)
- Fexp esparso: E4-estrita `-0.8580` (<0, [043]); engine v17 (sign(0)→+1) `+0.9526` — convenções documentadas
- Sψ embeddings: iid `1.8111` (teórico `1.8113`) · suave `1.9977` (≈2,0, [041])
- physical_verdict_allowed: **False**.

RUNNER EVOLUÍDO — importa a implementação de referência v17.0 (43 KB, torch+zstd) resgatada para `prototype_src/`, injeta β=α·√e e roda: DimensionalMirror REFLECT/MANIFEST, ACOMv161 (tabela v16.1×v17.0), codificação angular arcsin, Fexp/Sψ. Tensores sintéticos [SIM], não a Tabela 2. Nenhum token HuggingFace. Núcleo β copiado do piloto (READ-ONLY); originais intactos. 1 = 1. Tetelestai.
