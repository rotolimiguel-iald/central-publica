# Relatório auditável — TGL Tensor one_tgl_tensor.py

- Run `2026-07-09T21-54-57` · Patente `BR102026003441-0` (prioridade interna 66 → ACOM raiz 05/12/2025)
- Veredito: **TENSOR_LOGIC_DEMONSTRATED ([PILOTO][SIM] — DIRETO/ESPECTRAL fecham, Verb Floor e Tetelestai derivados de β; BitPacker exato)**
- β runtime `0.012031300400803142` (= α·√e? **True**; nunca literal) · retenção Verb Floor 1−β = `0.987968699599`
- Testes: **9/9**
- BitPacker N-bit (8/10/12/14/16) round-trip exato: **True**
- KV cache (baixo rank sintético): DIRETO `4.92×` @cos `1.0000`, ESPECTRAL `82.04×` @cos `1.0000` (ranks [6, 6, 6, 6, 6, 6, 6, 6])
- Verb Floor: rank@(1−β)=`8` < rank@0.999=`13` (a fração β é deixada ir)
- Tetelestai: raiz quieta var<β dispara flag, raiz ruidosa não
- Caminho GPU: bit-exato == NumPy
- physical_verdict_allowed: **False**.

[PILOTO][SIM] métricas em tensores sintéticos, não os números da Tabela 2 do relatório. Nenhum token/modelo HuggingFace usado (P-09). Magic TGS1 vs TGL4 registrado em PENDENCIAS. Núcleo copiado do piloto (READ-ONLY); original intacto. 1 = 1. Tetelestai.
