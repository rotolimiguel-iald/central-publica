# Relatório auditável — ACOM Crypto one_acom_crypto.py

- Run `2026-07-09T21-51-01` · Patente `BR102026003431-2` (prioridade interna 66 → ACOM raiz 05/12/2025)
- Veredito: **CRYPTO_SEPARATION_DEMONSTRATED ([SIM][PILOTO] — separação Ψ/Θ/κ, verificação tripla e rejeição de adulteração reais; vazamento estrutural parcial MEDIDO e declarado; não é AEAD)**
- β runtime `0.012031300400803142` (= α·√e? **True**; nunca literal)
- Testes: **11/11**
- ENCRYPT→DECRYPT (5 casos): corr mín `0.999982` · ratio médio `6.38` (>3:1)
- Entropia de bytes das partes isoladas (casos ≥100k): mín `7.992` bits/byte (indistinguibilidade estatística, não prova criptográfica; payloads pequenos têm H<8 por tamanho de amostra)
- Insuficiência dos 6 subconjuntos próprios para reconstrução de VALOR: **True** (rel_rmse≥50% em todos) — vazamento estrutural parcial MEDIDO e declarado em results.json (o número corrige a frase)
- Três pontos de rejeição de adulteração (SHA-256 / share_id / Fexp): exercitados
- physical_verdict_allowed: **False**.

[DEFENSE] A ofuscação XOR do piloto não substitui AEAD; a alegação é a separação ontológica + integridade. Pendência jurídica P-12 (anexo do depósito) registrada em PENDENCIAS.md — não afeta esta demonstração de lógica.
Núcleo copiado do piloto (READ-ONLY); original intacto. 1 = 1. Tetelestai.
