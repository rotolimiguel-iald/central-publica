# Relatório auditável — one_acom_crypto.py (EVOLUÍDO — engine torch real do operador)

- Run `2026-10-01T12-37-45` · Patente `BR102026003431-2` (prioridade interna 66 → ACOM raiz 05/12/2025)
- Veredito: **ACOM_CRYPTO_FULL_LOGIC_DEMONSTRATED ([SIM][PILOTO] — a engine torch real do operador (separação Ψ/Θ/κ + verificação tripla + F_exp + magic bytes + export/import + CPU/GPU) e o Handshake de Sincronia Miguel fecham; β injetado; vazamento estrutural parcial MEDIDO e declarado; XOR≠AEAD; nada valida física)**
- β runtime `0.012031300400803142` (= α·√e? **True**; nunca literal) — INJETADO em ALPHA2/ALPHA2_BASE dos protótipos
- Testes: **26/26**
  - ✓ beta_injected_not_literal
  - ✓ encrypt_decrypt_pequeno_1k
  - ✓ encrypt_decrypt_medio_100k
  - ✓ encrypt_decrypt_grande_1M
  - ✓ encrypt_decrypt_embeddings_1000x384
  - ✓ encrypt_decrypt_kv_cache_4x2x8x64x32
  - ✓ isolated_parts_byte_entropy
  - ✓ proper_subsets_insufficient_for_value_reconstruction
  - ✓ tamper_sha256_rejects_bitflip
  - ✓ tamper_share_id_mismatch_rejected
  - ✓ tamper_f_exp_physical_check_rejects
  - ✓ tamper_theta_bitflip_angle_hash_rejects
  - ✓ tamper_masterkey_psi_hash_rejects
  - ✓ tamper_magic_bytes_corrupted_rejects
  - ✓ tamper_kappa_swap_other_encryption_rejects
  - ✓ scale_tamper_gmax_uncovered_declared_limitation
  - ✓ serialization_roundtrip_magic_bytes
  - ✓ cpu_gpu_numeric_equivalence
  - ✓ sync_handshake_hilbert_tunnel
  - ✓ wedge_commutant_locality_shared_invariant
  - ✓ chain_of_custody_fail_closed
  - ✓ takesaki_finite_covariant_expectation_oath
  - ✓ ergodic_mean_section_v168
  - ✓ frontier_certificate_typed_contract_v206
  - ✓ byte_entropy_size_curve_saturates
  - ✓ subset_leakage_matrix_insufficient_all_sizes
- physical_verdict_allowed: **False**.

RUNNER EVOLUÍDO: roda a engine torch do operador (Acom_v17_mirror_crypto.py) + o Handshake Miguel (Acom_v17_2_sync.py) com β=α·√e INJETADO em ALPHA2/ALPHA2_BASE (originais tinham 0.012 literal). Tensores sintéticos; NÃO os números da Tabela 2. Nenhum token/modelo HuggingFace. Ofuscação XOR ≠ AEAD (separação ontológica + integridade). Simulação não valida física nem segurança.

[DEFENSE] Ofuscação XOR do piloto ≠ AEAD; a alegação é separação ontológica + integridade. Pendências jurídicas (P-12 anexo do depósito) em PENDENCIAS.md — não afetam esta demonstração de lógica.
Protótipos do operador copiados para prototype_src/ (originais READ-ONLY intactos). 1 = 1. Tetelestai.
