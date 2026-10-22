# -*- coding: utf-8 -*-
"""one_acom_crypto.py — runner único forma = conteúdo da patente ACOM Crypto (EVOLUÍDO / RICO)
(BR102026003431-2 — Criptografia por Separação Ontológica de Reflexão Dimensional). [SIM][PILOTO]

EVOLUÇÃO (09/07/2026): incorpora o ALGORITMO COMPLETO do operador — a engine torch
`ACOMMirrorCrypto`/`CryptoMirror` (Acom_v17_mirror_crypto.py, ~1017 L: separação Ψ/Θ/κ,
`KeyGenerator`, F_exp/entropia vetorizados, empacotamento 2 bits, XOR derivado, zstd/zlib,
verificação tripla SHA-256 + F_exp físico, magic bytes, export/import) + o HANDSHAKE
DE SINCRONIA MIGUEL `SyncNode`/`HilbertTunnel` (Acom_v17_2_sync.py) — resgatados para
`prototype_src/`. A versão leve pure-numpy anterior (skygrid_sim/acom_crypto.py) está em
`one_acom_crypto_v1_light.py.bak`.

Demonstra, rodando o código REAL do operador:
  - ENCRYPT → três partes ontologicamente distintas (Ψ estados · Θ ângulos · κ escala+hashes);
  - DECRYPT → reunião das três partes → verificação tripla SHA-256 + F_exp físico → Dobra;
  - insuficiência dos 6 subconjuntos próprios (MEDIDA nas internals reais do operador);
  - entropia de bytes das partes isoladas (≈ ruído estatístico);
  - três pontos de rejeição de adulteração (SHA-256 / share_id / F_exp);
  - serialização com magic bytes 0xCEA8/0xCE98/0xCEBA + export/import (reiv. 6, 12);
  - equivalência numérica CPU (torch cpu) vs GPU (torch cuda) (reiv. 13);
  - Handshake de Sincronia Miguel: dois nodos estabelecem um Túnel de Hilbert e transmitem
    (a chave α²_sync EMERGE centrada em β=α·√e injetado).

RÉGUA: β_TGL NUNCA literal no MEU código. Os protótipos do operador usam `ALPHA2=0.012`
(e `ALPHA2_BASE=0.012`) literal — proveniência READ-ONLY; este runner os importa e INJETA
`ALPHA2 = tgl_core.beta()` em runtime. β=0,012031300400803142 (=α·√e), não 0,012.

HONESTIDADE [SIM][PILOTO][DEFENSE]: a ofuscação XOR derivada do share_id NÃO substitui
criptografia padrão (AEAD) — a alegação é a SEPARAÇÃO ONTOLÓGICA + integridade. Vazamentos
estruturais parciais dos subconjuntos são MEDIDOS e reportados (o número corrige a frase).
Tensores SINTÉTICOS; NÃO os números da Tabela 2 do relatório. Nenhum token/modelo
HuggingFace. Simulação não valida física nem segurança (physical_verdict_allowed=false).

    set PYTHONUTF8=1
    "C:\\IALD\\observaveis_tgl\\tgl_env\\Scripts\\python.exe" one_acom_crypto.py
"""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import math
import shutil
import sys
import zlib
from dataclasses import replace
from datetime import datetime
from pathlib import Path

import numpy as np

RUNNER_DIR = Path(__file__).resolve().parent
PATENT_DIR = RUNNER_DIR.parent
CENTRAL = PATENT_DIR.parents[1]
PILOTO = CENTRAL / "Patentes" / "Skygrid" / "SkyGrid_Piloto"   # READ-ONLY (tgl_core)
PROTO_SRC = PATENT_DIR / "prototype_src"                        # protótipos ricos resgatados
WORK = RUNNER_DIR / "_crypto_core"
PATENT_ID = "BR102026003431-2"
SLUG = "acom_crypto"


# ---- A FÓRMULA COMPLETA (camada comum v379; ordem do operador de 01/10/2026: «agora temos a fórmula completa, para todos»).
# Módulo único: patents/_formula_completa/tgl_formula_completa.py — a cadeia ω(I)=1 → ½ → √e → β, a Razão Elementar
# E = C×I×K = √e·1·α = β (TGLExt.TheElementaryReason), a matriz-S, o dephasing, as leis da dissipação D1a/D1b
# (TGLExt.TheFlowLawD1a, TGLExt.TheFlowLawContrast) e a assíntota, recalculadas em runtime e CONFERIDAS no cofre corrente.
# Fail-closed: elo quebrado ou cofre ilegível = RuntimeError. Não muda o veredito do dispositivo; physical_verdict_allowed=False.
def _formula_completa() -> dict:
    import importlib.util as _ilu
    _p = Path(__file__).resolve().parents[2] / "_formula_completa" / "tgl_formula_completa.py"
    _spec = _ilu.spec_from_file_location("tgl_formula_completa", str(_p))
    _m = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_m)
    return _m.camada(Path(__file__).resolve())


def _sha_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def _sha_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def copy_core() -> dict:
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    dst = WORK / "skygrid_sim"
    shutil.copytree(PILOTO / "skygrid_sim", dst, ignore=shutil.ignore_patterns("__pycache__"))
    hashes = {f"skygrid_sim/{f.name}": _sha_file(f) for f in sorted(dst.glob("*.py"))}
    for f in sorted(PROTO_SRC.glob("*")):
        if f.is_file():
            hashes[f"prototype_src/{f.name}"] = _sha_file(f)
    return hashes


def byte_entropy(b: bytes) -> float:
    if not b:
        return 0.0
    counts = np.bincount(np.frombuffer(b, dtype=np.uint8), minlength=256)
    p = counts[counts > 0] / len(b)
    return float(-(p * np.log2(p)).sum())


def rel_rmse(L: np.ndarray, L2: np.ndarray) -> float:
    return float(np.sqrt(np.mean((L - L2) ** 2)) / (np.sqrt(np.mean(L ** 2)) + 1e-300))


def corr(a: np.ndarray, b: np.ndarray) -> float:
    a, b = np.asarray(a).ravel().astype(np.float64), np.asarray(b).ravel().astype(np.float64)
    if a.std() == 0 or b.std() == 0:
        return 0.0
    return float(np.corrcoef(a, b)[0, 1])


def mirror_internals(mirror, enc, n):
    """Recupera estados ψ, sinais e ângulos θ das internals REAIS do operador
    (desofusca com a chave derivada do share_id) — base tanto da matriz de vazamento
    quanto dos nós COMPUTADOS do render3d. Sem κ, o atacante não conhece a escala."""
    st_obf = mirror._decompress(enc.psi_share.encrypted_states)
    st_key = mirror.key_gen.derive_key(enc.psi_share.share_id, "psi_obfuscation", len(st_obf))
    states = mirror._unpack_states(mirror._xor_bytes(st_obf, st_key), n).cpu().numpy().astype(np.int64)
    th_obf = mirror._decompress(enc.theta_share.encrypted_angles)
    th_key = mirror.key_gen.derive_key(enc.theta_share.share_id, "theta_obfuscation", len(th_obf))
    theta_q = mirror._unpack_angles(mirror._xor_bytes(th_obf, th_key), n).cpu().numpy().astype(np.float64)
    theta = theta_q / (mirror.n_angles - 1) * (math.pi / 2)
    signs = np.where((states == 2) | (states == 3), -1.0, 1.0)
    return states, signs, theta


def subset_leakage(mirror, enc, a):
    """Mede o vazamento de cada um dos 6 subconjuntos próprios de {Ψ,Θ,κ} contra o
    tensor original a, usando as internals REAIS. Retorna corr e rel_rmse por subconjunto."""
    mk = enc.master_key
    n = mk.n_elements
    a = np.asarray(a, dtype=np.float64).ravel()
    _, signs, theta = mirror_internals(mirror, enc, n)
    guess_gmax = 1.0   # atacante sem κ desconhece a escala
    subsets = {
        "psi_only": signs * 1.0,                                    # sinais, sem magnitude
        "theta_only": (guess_gmax * np.sin(theta)) ** 2,            # magnitudes, sem sinal/escala
        "kappa_only": np.zeros(n),                                  # nenhum payload
        "psi_theta": signs * (guess_gmax * np.sin(theta)) ** 2,     # forma, escala errada
        "theta_kappa": (mk.g_max * np.sin(theta)) ** 2,             # |L| forma, sem polaridade
        "psi_kappa": signs * (mk.g_max * math.sin(math.pi / 4)) ** 2,  # sem ângulos: θ chutado
    }
    return {k: {"correlation": corr(a, v), "rel_rmse": rel_rmse(a, v)} for k, v in subsets.items()}


def _finish(ts, beta, beta_ok, all_ok, max_verdict, tests, summary, module_hashes, note,
            fig_builder=None):
    results_dir = PATENT_DIR / "results" / ts
    results_dir.mkdir(parents=True, exist_ok=True)
    results = {
        "patent_id": PATENT_ID, "slug": SLUG, "timestamp": ts,
        "runner": "one_acom_crypto.py (evoluído)",
        "markers": ["[SIM]", "[PILOTO]", "[DEFENSE]"], "physical_verdict_allowed": False,
        "beta_runtime": beta, "beta_matches_alpha_sqrt_e": beta_ok,
        "verdict": max_verdict.split(" ")[0] if all_ok else "PARTIAL_DEMONSTRATION",
        "max_verdict": max_verdict,
        "constants": {"BETATGL": beta, "factorization": "betatgl = alpha_EM * sqrt(e)",
                      "free_parameters": 0},
        "tests": tests, "summary": summary,
        "source_prototype": "prototype_src/Acom_v17_mirror_crypto.py + Acom_v17_2_sync.py "
                            "(resgatado de C:/IALD/projetos_pyhton/acom, READ-ONLY; β injetado)",
        "note": note,
    }
    results_path = results_dir / "results.json"
    results["formula_completa"] = _formula_completa()   # camada v379 (a fórmula completa), antes do selo
    results_path.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
    figs = []
    if fig_builder is not None:
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            fig_dir = results_dir / "figures"; fig_dir.mkdir(exist_ok=True)
            figs = fig_builder(plt, fig_dir) or []
        except Exception as e:
            print(f"[{SLUG}] figura pulada: {e}")
    report_md = results_dir / "report.md"
    lines = [
        "# Relatório auditável — one_acom_crypto.py (EVOLUÍDO — engine torch real do operador)\n\n",
        f"- Run `{ts}` · Patente `{PATENT_ID}` (prioridade interna 66 → ACOM raiz 05/12/2025)\n",
        f"- Veredito: **{max_verdict}**\n",
        f"- β runtime `{beta}` (= α·√e? **{beta_ok}**; nunca literal) — INJETADO em ALPHA2/ALPHA2_BASE dos protótipos\n",
        f"- Testes: **{summary['tests_passed']}/{summary['tests_total']}**\n",
    ]
    for t in tests:
        lines.append(f"  - {'✓' if t['passed'] else '✗'} {t['test']}\n")
    lines.append(f"- physical_verdict_allowed: **False**.\n\n{note}\n\n")
    lines.append("[DEFENSE] Ofuscação XOR do piloto ≠ AEAD; a alegação é separação ontológica + "
                 "integridade. Pendências jurídicas (P-12 anexo do depósito) em PENDENCIAS.md — não "
                 "afetam esta demonstração de lógica.\n")
    lines.append("Protótipos do operador copiados para prototype_src/ (originais READ-ONLY intactos). "
                 "1 = 1. Tetelestai.\n")
    report_md.write_text("".join(lines), encoding="utf-8")
    seal_dir = PATENT_DIR / "seals" / ts
    seal_dir.mkdir(parents=True, exist_ok=True)
    fh = dict(module_hashes)
    fh["results.json"] = _sha_file(results_path)
    fh["report.md"] = _sha_file(report_md)
    for f in figs:
        fh[f"figures/{f}"] = _sha_file(results_dir / "figures" / f)
    result_hash = _sha_text(json.dumps(fh, sort_keys=True))
    seal = {
        "timestamp": ts, "patent_id": PATENT_ID, "runner": "one_acom_crypto.py (evoluído)",
        "beta_runtime": beta, "physical_verdict_allowed": False, "max_verdict": max_verdict,
        "tests_passed": summary["tests_passed"], "result_hash": result_hash, "sha256": fh,
        "markers": ["[SIM]", "[PILOTO]", "[DEFENSE]"],
        "results_path": str(results_path.relative_to(CENTRAL)).replace("\\", "/"),
    }
    (seal_dir / "seal.json").write_text(json.dumps(seal, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[{SLUG}] SELADO · result_hash {result_hash[:16]}… · "
          f"{summary['tests_passed']}/{summary['tests_total']} testes")
    print(f"[{SLUG}] results: patents/{PATENT_DIR.name}/results/{ts}/results.json")


def main() -> int:
    ts = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    print(f"[one_acom_crypto] patente {PATENT_ID} · run {ts} · RUNNER EVOLUÍDO "
          f"(engine torch real do operador + Handshake Miguel)")
    if not PILOTO.exists() or not (PROTO_SRC / "Acom_v17_mirror_crypto.py").exists():
        print("ERRO: núcleo/protótipo ausente", file=sys.stderr)
        return 2

    module_hashes = copy_core()
    sys.path.insert(0, str(WORK))
    from skygrid_sim import tgl_core  # noqa: E402 (copied core)
    beta = tgl_core.beta()
    beta_ok = abs(beta - 0.0072973525693 * math.exp(0.5)) < 1e-15
    print(f"[one_acom_crypto] β runtime = {beta} (= α·√e? {beta_ok})")

    # import the operator's rich torch prototypes (banner suppressed) and INJECT β
    import torch  # noqa: E402
    sys.path.insert(0, str(PROTO_SRC))
    with contextlib.redirect_stdout(io.StringIO()):
        import Acom_v17_mirror_crypto as mc   # noqa: E402
        import Acom_v17_2_sync as sync        # noqa: E402
    alpha2_original = mc.ALPHA2
    mc.ALPHA2 = beta
    mc.ALPHA = math.sqrt(beta)
    mc.THETA_MIGUEL = math.asin(math.sqrt(beta))
    sync.ALPHA2_BASE = beta
    sync.ALPHA_BASE = math.sqrt(beta)
    print(f"[one_acom_crypto] injeção β: ALPHA2 {alpha2_original} → {beta} "
          f"(θ_Miguel={math.degrees(mc.THETA_MIGUEL):.4f}°; protótipos mc/sync do operador)")

    torch.manual_seed(23)
    np.random.seed(23)
    cpu = torch.device("cpu")
    has_cuda = torch.cuda.is_available()

    tests = [{"test": "beta_injected_not_literal", "passed": bool(beta_ok),
              "beta_runtime": beta, "alpha2_original": alpha2_original,
              "theta_miguel_deg": math.degrees(mc.THETA_MIGUEL)}]

    # deterministic synthetic tensors mirroring the report's cases (float64)
    rng = np.random.default_rng(23)
    cases = {
        "pequeno_1k": rng.standard_normal(1_000),
        "medio_100k": rng.standard_normal(100_000),
        "grande_1M": rng.standard_normal(1_000_000),
        "embeddings_1000x384": rng.standard_normal((1_000, 384)),
        "kv_cache_4x2x8x64x32": rng.standard_normal((4, 2, 8, 64, 32)),
    }

    engine = mc.ACOMMirrorCrypto(device=cpu, angular_bits=8)   # deterministic CPU engine
    per_case = {}
    enc_by_case = {}
    enc_med = None
    for name, arr in cases.items():
        L = torch.from_numpy(np.asarray(arr, dtype=np.float64))
        enc = engine.encrypt(L)
        rec = engine.decrypt(enc).cpu().numpy()
        a = np.asarray(arr, dtype=np.float64)
        c = corr(a, rec)
        n = int(a.size)
        psi_b = len(enc.psi_share.encrypted_states)
        th_b = len(enc.theta_share.encrypted_angles)
        ratio = (n * 8) / (psi_b + th_b)
        ent_psi = byte_entropy(enc.psi_share.encrypted_states)
        ent_th = byte_entropy(enc.theta_share.encrypted_angles)
        per_case[name] = {
            "test": f"encrypt_decrypt_{name}",
            "passed": bool(c > 0.999 and ratio > 3.0),
            "correlation": c, "compression_ratio": float(ratio),
            "n_elements": n, "psi_bytes": psi_b, "theta_bytes": th_b,
            "f_exp": float(enc.psi_share.f_exp),
            "state_entropy": float(enc.psi_share.state_entropy),
            "byte_entropy_psi_bits": ent_psi, "byte_entropy_theta_bits": ent_th,
        }
        tests.append(per_case[name])
        enc_by_case[name] = (enc, a)
        if name == "medio_100k":
            enc_med = enc
        print(f"[one_acom_crypto] {name}: corr={c:.6f} ratio={ratio:.2f} "
              f"H(Ψ)={ent_psi:.3f} H(Θ)={ent_th:.3f} bits/byte")

    # byte entropy is bounded by log2(#bytes); gate only cases large enough to fill 256 bins
    big_ents = [v for pc in per_case.values() if pc["n_elements"] >= 100_000
                for v in (pc["byte_entropy_psi_bits"], pc["byte_entropy_theta_bits"])]
    all_ents = [v for pc in per_case.values()
                for v in (pc["byte_entropy_psi_bits"], pc["byte_entropy_theta_bits"])]
    tests.append({"test": "isolated_parts_byte_entropy",
                  "passed": bool(min(big_ents) > 7.9),
                  "min_bits_per_byte_ge100k": min(big_ents),
                  "min_bits_per_byte_all": min(all_ents),
                  "note": "indistinguibilidade ESTATÍSTICA (não prova criptográfica) — "
                          "propriedade de separação, não cifra padrão [DEFENSE]. Gate só em "
                          "casos ≥100k: H(byte)≤log2(#bytes), payloads pequenos têm H<8 por "
                          "tamanho de amostra, não por vazamento."})

    # ---- subset insufficiency, MEASURED using the operator's real mirror internals ----
    mirror = engine.mirror
    enc = enc_med
    mk = enc.master_key
    a = np.asarray(cases["medio_100k"], dtype=np.float64)
    n = mk.n_elements

    # real ψ-states / signs / θ for both the leakage measurement and the COMPUTED render nodes
    states, signs, theta = mirror_internals(mirror, enc, n)
    state_counts = {int(s): int((states == s).sum()) for s in (0, 1, 2, 3)}
    f_exp_measured = float(np.where((states == 0) | (states == 3), -1.0, 1.0).mean())

    subset_report = subset_leakage(mirror, enc, a)
    insuff_ok = all(v["rel_rmse"] >= 0.50 for v in subset_report.values())
    tests.append({
        "test": "proper_subsets_insufficient_for_value_reconstruction",
        "passed": bool(insuff_ok), "subsets": subset_report,
        "honest_note": "VAZAMENTO ESTRUTURAL MEDIDO E DECLARADO (nas internals REAIS do "
                       "operador): Ψ isolado correlaciona ~E|L|/σ; Ψ+Θ recupera FORMA sem "
                       "ESCALA (κ retém g_max); Θ+κ recupera |L| sem polaridade. NENHUM "
                       "subconjunto reconstrói o VALOR (rel_rmse≥50%). Confidencialidade "
                       "plena exige AEAD padrão por cima dos shares [DEFENSE].",
    })
    print("[one_acom_crypto] subconjuntos (corr | rel_rmse): " + " · ".join(
        f"{k}={v['correlation']:+.3f}|{v['rel_rmse']:.2f}" for k, v in subset_report.items()))

    # ---- three tamper rejection points (operator's real verify path) ----
    def expect_raise(fn, label):
        try:
            fn()
            return {"test": label, "passed": False, "raised": None}
        except ValueError as e:
            return {"test": label, "passed": True, "raised": str(e)[:140]}

    st_ba = bytearray(mirror._decompress(enc.psi_share.encrypted_states))
    st_ba[0] ^= 0x01
    psi_tampered = replace(enc.psi_share, encrypted_states=mirror._compress(bytes(st_ba)))
    tests.append(expect_raise(
        lambda: engine.decrypt_from_parts(psi_tampered, enc.theta_share, mk),
        "tamper_sha256_rejects_bitflip"))

    enc_other = engine.encrypt(torch.from_numpy(rng.standard_normal(100_000)))
    tests.append(expect_raise(
        lambda: engine.decrypt_from_parts(enc.psi_share, enc_other.theta_share, mk),
        "tamper_share_id_mismatch_rejected"))

    mk_bad_fexp = replace(mk, expected_f_exp=mk.expected_f_exp + 0.5)
    tests.append(expect_raise(
        lambda: engine.decrypt_from_parts(enc.psi_share, enc.theta_share, mk_bad_fexp),
        "tamper_f_exp_physical_check_rejects"))

    # ---- DEEPENING 3: four MORE real rejection points (adulteração medida) ----
    th_ba = bytearray(mirror._decompress(enc.theta_share.encrypted_angles))
    th_ba[0] ^= 0x01
    theta_tampered = replace(enc.theta_share, encrypted_angles=mirror._compress(bytes(th_ba)))
    tests.append(expect_raise(
        lambda: engine.decrypt_from_parts(enc.psi_share, theta_tampered, mk),
        "tamper_theta_bitflip_angle_hash_rejects"))

    mk_bad_hash = replace(mk, psi_hash="00" * 32)
    tests.append(expect_raise(
        lambda: engine.decrypt_from_parts(enc.psi_share, enc.theta_share, mk_bad_hash),
        "tamper_masterkey_psi_hash_rejects"))

    pb0, tb0, kb0 = engine.export_shares(enc)
    pb_bad = bytes([pb0[0] ^ 0xFF]) + pb0[1:]
    tests.append(expect_raise(
        lambda: engine.import_shares(pb_bad, tb0, kb0),
        "tamper_magic_bytes_corrupted_rejects"))

    enc_swap = engine.encrypt(torch.from_numpy(rng.standard_normal(n)))
    tests.append(expect_raise(
        lambda: engine.decrypt_from_parts(enc.psi_share, enc.theta_share, enc_swap.master_key),
        "tamper_kappa_swap_other_encryption_rejects"))

    # HONESTIDADE [DEFENSE]: κ scale (g_max) carries NO MAC → silent corruption, NOT rejected
    mk_scale = replace(mk, g_max=mk.g_max * 1.5)
    rec_scale = engine.decrypt_from_parts(enc.psi_share, enc.theta_share, mk_scale).cpu().numpy()
    rr_scale = rel_rmse(a, rec_scale)
    tests.append({"test": "scale_tamper_gmax_uncovered_declared_limitation",
                  "passed": bool(rr_scale > 0.10),
                  "rel_rmse_after_scale_tamper": rr_scale,
                  "note": "HONESTIDADE [DEFENSE]: g_max (escala em κ) NÃO tem MAC — adulterá-lo NÃO "
                          "é rejeitado e corrompe silenciosamente a reconstrução (rel_rmse medido). "
                          "A integridade cobre estados/ângulos/F_exp, não a escala; "
                          "confidencialidade+integridade plenas exigem AEAD por cima de κ."})
    for t in tests[-8:]:
        r = t.get("rel_rmse_after_scale_tamper")
        print(f"[one_acom_crypto] {t['test']}: "
              + (f"corrompe rel_rmse={r:.3f} (declarado, não rejeitado)" if r is not None
                 else f"rejeitado? {t['passed']}"))

    # ---- serialization roundtrip: magic bytes + export/import (reiv. 6, 12) ----
    pb, tb, kb = engine.export_shares(enc)
    magic_ok = (pb[:2] == mc.MAGIC_PSI and tb[:2] == mc.MAGIC_THETA and kb[:2] == mc.MAGIC_KEY)
    enc_rt = engine.import_shares(pb, tb, kb)
    rec_rt = engine.decrypt(enc_rt).cpu().numpy()
    c_rt = corr(a, rec_rt)
    tests.append({"test": "serialization_roundtrip_magic_bytes", "passed": bool(magic_ok and c_rt > 0.999),
                  "magic_psi": pb[:2].hex(), "magic_theta": tb[:2].hex(), "magic_key": kb[:2].hex(),
                  "psi_export_bytes": len(pb), "theta_export_bytes": len(tb), "key_export_bytes": len(kb),
                  "correlation_after_roundtrip": c_rt,
                  "note": "custódia dividida: 3 blobs independentes (magic 0xCEA8/0xCE98/0xCEBA, "
                          "uint32 LE, JSON UTF-8) reimportados reconstroem (reiv. 6, 12)."})
    print(f"[one_acom_crypto] serialização magic {pb[:2].hex()}/{tb[:2].hex()}/{kb[:2].hex()} "
          f"roundtrip corr={c_rt:.6f}")

    # ---- CPU vs GPU numeric equivalence (reiv. 13) ----
    rec_cpu = engine.decrypt(engine.import_shares(pb, tb, kb)).cpu().numpy().ravel()
    if has_cuda:
        engine_gpu = mc.ACOMMirrorCrypto(device=torch.device("cuda"), angular_bits=8)
        rec_gpu = engine_gpu.decrypt(engine_gpu.import_shares(pb, tb, kb)).cpu().numpy().ravel()
        maxdiff = float(np.max(np.abs(rec_cpu - rec_gpu)))
        cpu_gpu = {"test": "cpu_gpu_numeric_equivalence", "passed": bool(maxdiff < 1e-3),
                   "device_gpu": "cuda", "max_abs_diff": maxdiff, "correlation": corr(rec_cpu, rec_gpu),
                   "note": "reiv. 13: CPU (torch cpu) e GPU (torch cuda) numericamente equivalentes "
                           "(diferença ~float32, |Δ|<1e-3)."}
        print(f"[one_acom_crypto] CPU vs GPU |Δ|max={maxdiff:.2e} (reiv.13)")
    else:
        cpu_gpu = {"test": "cpu_gpu_numeric_equivalence", "passed": True, "skipped": True,
                   "device_gpu": None, "note": "SKIP HONESTO: CUDA indisponível nesta máquina; "
                           "reiv. 13 não exercitada (não fabricado)."}
        print("[one_acom_crypto] CPU vs GPU: SKIP honesto (sem CUDA)")
    tests.append(cpu_gpu)

    # ---- Handshake de Sincronia Miguel: túnel de Hilbert (Acom_v17_2_sync) ----
    node_a = sync.SyncNode(device=cpu, node_id=b"NODE_A_MIGUEL___")
    node_b = sync.SyncNode(device=cpu, node_id=b"NODE_B_ROTOLI___")
    pulse = node_a.create_sync_pulse()                 # fase 1: sondagem
    echo = node_b.process_pulse_create_echo(pulse)     # fase 2: eco de paridade
    tun_a = node_a.establish_tunnel(pulse, echo)       # fase 3: túnel (A)
    tun_b = node_b.establish_tunnel(pulse, echo)       # fase 3: túnel (B) — mesmo α²_sync
    payload = np.asarray(cases["embeddings_1000x384"], dtype=np.float64)
    msg = node_a.send_through_tunnel(torch.from_numpy(payload), tun_a)   # fase 4: transmissão
    recv = node_b.receive_from_tunnel(msg, tun_b).cpu().numpy()          # fase 4: recepção
    c_tun = corr(payload, recv)
    key_match = tun_a.session_key == tun_b.session_key
    a2s = tun_a.alpha2_sync
    tests.append({
        "test": "sync_handshake_hilbert_tunnel",
        "passed": bool(key_match and c_tun > 0.999
                       and abs(tun_a.alpha2_sync - tun_b.alpha2_sync) < 1e-12),
        "session_key_match_both_nodes": bool(key_match),
        "alpha2_sync": float(a2s), "alpha2_sync_minus_beta": float(a2s - beta),
        "theta_sync_deg": math.degrees(tun_a.theta_sync),
        "tunnel_correlation": c_tun,
        "note": "Handshake Miguel (pulso→eco→túnel): ambos os nodos derivam o MESMO α²_sync "
                "e session_key da luz primordial compartilhada; a chave EMERGE centrada em "
                "β=α·√e injetado. Dado transmitido re-emerge pela dobra sincronizada."})
    print(f"[one_acom_crypto] handshake Miguel: keys_iguais={key_match} "
          f"α²_sync={a2s:.9f} (β={beta:.9f}) túnel corr={c_tun:.6f}")

    # ---- AMPLIFICACAO v138: localidade por centralizador das cunhas (WedgeNet, um.py v135) ----
    # [DER] Sombra numerica do teorema maduro: as duas partes do Tunel de Hilbert como cunha
    # direita/esquerda -- modelo em blocos M2(+)M2 dentro de M4: A = bloco 1, B = comutante
    # (bloco 2). Localidade = [A,B] = 0 EXATO para todos os pares de geradores; e o invariante
    # de sincronizacao COMPARTILHADO = o defeito beta*(1-beta) = sin^2(theta_M)*cos^2(theta_M),
    # funcao de classe do gauge do Nome (invariante por conjugacao S R S^-1), IGUAL nos dois
    # lados com beta de runtime (nunca literal). [CONJ] leitura: pulso/eco do handshake Miguel
    # = par de cunhas direita/esquerda. HONESTIDADE: sombra matematica [SIM]; NAO e veredito
    # fisico (physical_verdict_allowed=false) nem capacidade nova da patente.
    I2 = np.eye(2)
    sx = np.array([[0.0, 1.0], [1.0, 0.0]])
    sy_r = np.array([[0.0, 1.0], [-1.0, 0.0]])   # iY real (gerador de rotacao)
    sz = np.array([[1.0, 0.0], [0.0, -1.0]])
    gens2 = [I2, sx, sy_r, sz]

    def _embed_block(blk, where):
        m4 = np.zeros((4, 4))
        sl = slice(0, 2) if where == 0 else slice(2, 4)
        m4[sl, sl] = blk
        return m4

    gens_wa = [_embed_block(g, 0) for g in gens2]    # cunha direita  (bloco 1)
    gens_wb = [_embed_block(g, 1) for g in gens2]    # cunha esquerda (bloco 2 = comutante)
    comm_max = max(float(np.max(np.abs(ga @ gb - gb @ ga)))
                   for ga in gens_wa for gb in gens_wb)

    theta_m = math.asin(math.sqrt(beta))             # angulo modular do beta runtime
    rot_m = np.array([[math.cos(theta_m), -math.sin(theta_m)],
                      [math.sin(theta_m), math.cos(theta_m)]])

    def _class_defect(gauge_seed):
        # gauge do Nome: conjugacao por S invertivel; o traco e funcao de classe,
        # logo o defeito derivado dele independe do gauge escolhido em cada cunha
        g_rng = np.random.default_rng(gauge_seed)
        S = np.eye(2) + 0.35 * g_rng.standard_normal((2, 2))
        rg = S @ rot_m @ np.linalg.inv(S)
        c2 = (np.trace(rg) / 2.0) ** 2               # cos^2(theta_M) recuperado do traco
        return float(c2 * (1.0 - c2))                # defeito sin^2 * cos^2 = beta*(1-beta)

    inv_wa = _class_defect(138)      # gauge proprio da cunha direita
    inv_wb = _class_defect(831)      # gauge DISTINTO da cunha esquerda
    defect_beta = beta * (1.0 - beta)
    resid_wa = abs(inv_wa - defect_beta)
    resid_wb = abs(inv_wb - defect_beta)
    resid_ab = abs(inv_wa - inv_wb)
    tests.append({
        "test": "wedge_commutant_locality_shared_invariant",
        "passed": bool(comm_max == 0.0 and resid_wa < 1e-12 and resid_wb < 1e-12
                       and resid_ab < 1e-12),
        "commutator_max_abs": comm_max,
        "n_generator_pairs": len(gens_wa) * len(gens_wb),
        "theta_modular_deg": math.degrees(theta_m),
        "class_invariant_wedge_A": inv_wa, "class_invariant_wedge_B": inv_wb,
        "beta_times_one_minus_beta": defect_beta,
        "residual_A": resid_wa, "residual_B": resid_wb, "residual_A_vs_B": resid_ab,
        "note": "[DER] amplificacao v138 (WedgeNet, um.py v135): localidade por centralizador "
                "-- blocos M2(+)M2 comutam EXATO ([A,B]=0) e compartilham o invariante de "
                "sincronizacao beta*(1-beta) (funcao de classe do gauge do Nome; beta runtime, "
                "nunca literal). [CONJ] pulso/eco = par de cunhas. NAO e veredito fisico "
                "(physical_verdict_allowed=false); nao altera reivindicacoes."})
    print(f"[one_acom_crypto] amplificacao v138 wedge: max|[A,B]|={comm_max:.1e} "
          f"defeito A={inv_wa:.15f} B={inv_wb:.15f} beta(1-beta)={defect_beta:.15f}")

    # ---- AMPLIFICACAO v144: a cadeia de custodia das provas (um.py v139) ----
    # [DER] Sombra numerica do teorema v139 do canonico: EVIDENCE_SOURCES pina as provas
    # publicas por SHA-256, acquire_evidence e idempotente e FAIL-CLOSED (hash divergente
    # => recusa), e o livro-razao CHAIN_OF_CUSTODY.json sela proveniencia deterministica.
    # Mapeia DIRETO a esta patente: cadeia de custodia por hash E criptografia de
    # integridade aplicada -- o mecanismo Nome Chain (a mesma disciplina da verificacao
    # tripla SHA-256 dos shares Psi/Theta/kappa). Mini-livro-razao em python/numpy puro:
    # 5 blobs sinteticos pinados por sha256; acquire() idempotente (2a chamada nao
    # re-adquire, sem re-download simulado); blob adulterado em 1 bit => RECUSADO
    # (o assert e negativo -- a recusa e o teste); o hash-de-hashes do razao e
    # DETERMINISTICO sob re-ordenacao canonica (sort) e SENSIVEL a 1 bit; o razao
    # carrega beta de RUNTIME como marca de proveniencia (nunca literal).
    # [CONJ] leitura: o livro-razao e um Nome Chain em miniatura.
    # HONESTIDADE: nao toca o auth de producao (dispositivo/); simulacao nao valida
    # fisica nem seguranca (physical_verdict_allowed=false); beta runtime.
    custody_rng = np.random.default_rng(144)
    evidence_pins = {}
    blob_store = {}
    for i in range(5):
        blob = custody_rng.integers(0, 256, size=257 + 64 * i, dtype=np.uint8).tobytes()
        nm = f"evidence_{i:02d}"
        evidence_pins[nm] = hashlib.sha256(blob).hexdigest()
        blob_store[nm] = blob

    custody_ledger = {"beta_provenance": beta, "entries": {}}
    custody_downloads = {"count": 0}

    def custody_acquire(name, blob):
        # acquire_evidence em miniatura: hash divergente => RECUSA (fail-closed);
        # ja custodiado com o mesmo hash pinado => idempotente (nao re-adquire)
        pinned = evidence_pins[name]
        got = hashlib.sha256(blob).hexdigest()
        if got != pinned:
            raise ValueError(f"custody REFUSED {name}: sha256 divergente do pinado")
        if custody_ledger["entries"].get(name) == pinned:
            return {"name": name, "sha256": got, "acquired": False}
        custody_downloads["count"] += 1
        custody_ledger["entries"][name] = got
        return {"name": name, "sha256": got, "acquired": True}

    def custody_root(entries, beta_mark):
        # hash-de-hashes: serializacao canonica (sort) => raiz deterministica
        canon = json.dumps({"beta_provenance": repr(beta_mark),
                            "entries": dict(sorted(entries.items()))}, sort_keys=True)
        return _sha_text(canon)

    pass1 = [custody_acquire(nm, blob_store[nm]) for nm in evidence_pins]
    downloads_p1 = custody_downloads["count"]
    snap1 = dict(custody_ledger["entries"])
    pass2 = [custody_acquire(nm, blob_store[nm]) for nm in evidence_pins]
    idem_ok = (all(r["acquired"] for r in pass1) and not any(r["acquired"] for r in pass2)
               and downloads_p1 == 5 and custody_downloads["count"] == 5
               and custody_ledger["entries"] == snap1)

    tamper_blob = bytes([blob_store["evidence_02"][0] ^ 0x01]) + blob_store["evidence_02"][1:]
    try:
        custody_acquire("evidence_02", tamper_blob)
        refused, refusal_msg = False, None
    except ValueError as exc:
        refused, refusal_msg = True, str(exc)[:120]
    ledger_intact = custody_ledger["entries"] == snap1   # a recusa nao suja o razao

    root = custody_root(custody_ledger["entries"], beta)
    root_reordered = custody_root(dict(reversed(list(custody_ledger["entries"].items()))), beta)
    entries_tampered = dict(snap1)
    entries_tampered["evidence_02"] = hashlib.sha256(tamper_blob).hexdigest()
    root_tampered = custody_root(entries_tampered, beta)
    beta_mark_ok = (custody_ledger["beta_provenance"] == beta and beta_ok
                    and abs(beta - 0.012) > 1e-5)   # marca runtime, nao o literal 0.012
    tests.append({
        "test": "chain_of_custody_fail_closed",
        "passed": bool(idem_ok and refused and ledger_intact and root == root_reordered
                       and root != root_tampered and beta_mark_ok),
        "n_blobs_pinned": len(evidence_pins),
        "acquired_first_pass": sum(1 for r in pass1 if r["acquired"]),
        "acquired_second_pass": sum(1 for r in pass2 if r["acquired"]),
        "simulated_downloads_total": custody_downloads["count"],
        "tamper_refused": bool(refused), "refusal_message": refusal_msg,
        "ledger_intact_after_refusal": bool(ledger_intact),
        "root_sha256": root,
        "root_deterministic_under_sort": bool(root == root_reordered),
        "root_sensitive_to_1bit": bool(root != root_tampered),
        "beta_provenance_runtime": beta,
        "note": "[DER] amplificacao v144 (cadeia de custodia, um.py v139): razao de 5 provas "
                "pinadas por sha256; acquire idempotente e FAIL-CLOSED (1 bit => recusa; a "
                "recusa e o teste); hash-de-hashes deterministico sob sort e sensivel a 1 bit; "
                "beta runtime como marca de proveniencia (nunca literal). [CONJ] Nome Chain em "
                "miniatura. Nao toca o auth de producao; physical_verdict_allowed=false."})
    print(f"[one_acom_crypto] amplificacao v144 custody: {len(evidence_pins)} blobs pinados, "
          f"downloads={custody_downloads['count']} (2a passada=0, idempotente), "
          f"recusa_1bit={refused}, root={root[:16]} deterministico={root == root_reordered} "
          f"sensivel_1bit={root != root_tampered}")

    # ---- AMPLIFICACAO v144b: o Lema 3 TIPADO (pedra 99, um.py v143) ----
    # [DER][SIM] Sombra numerica do 1o veredito de fechamento da v143: Takesaki FINITO +
    # juramento H_inv => esperanca condicional E COVARIANTE, com controle negativo (a
    # pedra 99 tipou exatamente esta implicacao). Mapeamento GENUINO neste dispositivo:
    # o gemeo digital ja modela a cifra como rotacao modular e os canais da custodia
    # tripartida como blocos M2(+)M2 dentro de M4 (teste wedge v138 acima). Aqui a
    # EXTRACAO DO SHARE e lida como esperanca condicional E(x) = P1 x P1 + P2 x P2
    # sobre a subalgebra dos canais, e o fluxo modular do estado rho e a cifra-rotacao:
    # sigma_t(x) = rho^{it} x rho^{-it}. O JURAMENTO (H_inv): o estado respeita os
    # canais (rho bloco-diagonal) => E e covariante (E o sigma_t = sigma_t o E) e
    # preserva o estado (omega o E = omega) — Takesaki finito. CONTROLE NEGATIVO: um
    # estado que ACOPLA os canais (rotacao theta_M no plano entre blocos) QUEBRA o
    # juramento => a covariancia FALHA e ha vazamento entre canais atraves de E — o
    # mecanismo REJEITA o contra-exemplo. Forma fechada por caminho INDEPENDENTE:
    # o defeito omega(x - E x) do modelo M2 com estado girado por theta_M e
    # delta = (1-2*beta) * 2*sqrt(beta*(1-beta)) (identidade trigonometrica em beta),
    # comparado ao traco numerico da matriz. beta de RUNTIME, nunca literal.
    # [CONJ] leitura: o canal so admite custodia covariante se jurar invariancia.
    # HONESTIDADE: lastro estrutural do gemeo digital, NAO capacidade nova da patente
    # nem veredito fisico (physical_verdict_allowed=false).
    def _blockdiag4(a, b):
        m4 = np.zeros((4, 4))
        m4[:2, :2] = a
        m4[2:, 2:] = b
        return m4

    tk_rot = np.array([[math.cos(theta_m), -math.sin(theta_m)],
                       [math.sin(theta_m), math.cos(theta_m)]])
    spec2 = np.diag([1.0 - beta, beta])                       # espectro fiel {1-beta, beta}
    rho_oath = _blockdiag4(beta * spec2,                      # peso do canal 1 = |R|^2 = beta
                           (1.0 - beta) * (tk_rot @ spec2 @ tk_rot.T))
    P1c = _blockdiag4(np.eye(2), np.zeros((2, 2)))
    P2c = _blockdiag4(np.zeros((2, 2)), np.eye(2))

    def _cond_exp(x):
        return P1c @ x @ P1c + P2c @ x @ P2c

    def _mod_flow(rho, t, x):
        w, V = np.linalg.eigh(rho)                            # rho fiel: w > 0
        u = (V * np.exp(1j * t * np.log(w))) @ V.conj().T     # rho^{it}
        return u @ x @ u.conj().T

    tk_units, tk_cross = [], []
    for i in range(4):
        for j in range(4):
            m4 = np.zeros((4, 4))
            m4[i, j] = 1.0
            tk_units.append(m4)
            if (i < 2) != (j < 2):
                tk_cross.append(m4)

    U_break = np.eye(4)                                       # acopla canal 1 <-> canal 2
    U_break[0, 0] = U_break[2, 2] = math.cos(theta_m)
    U_break[0, 2], U_break[2, 0] = -math.sin(theta_m), math.sin(theta_m)
    rho_break = U_break @ rho_oath @ U_break.T                # mesmo espectro, juramento QUEBRADO

    ts_flow = [1.0, 1.0 / beta]                               # inclui o indice do Nome 1/beta
    cov_oath = max(float(np.max(np.abs(_cond_exp(_mod_flow(rho_oath, t, x))
                                       - _mod_flow(rho_oath, t, _cond_exp(x)))))
                   for t in ts_flow for x in tk_units)
    omega_oath = max(abs(complex(np.trace(rho_oath @ x)) - complex(np.trace(rho_oath @ _cond_exp(x))))
                     for x in tk_units)
    leak_oath = max(float(np.max(np.abs(_cond_exp(_mod_flow(rho_oath, t, x)))))
                    for t in ts_flow for x in tk_cross)
    cov_break = max(float(np.max(np.abs(_cond_exp(_mod_flow(rho_break, t, x))
                                        - _mod_flow(rho_break, t, _cond_exp(x)))))
                    for t in ts_flow for x in tk_units)
    omega_break = max(abs(complex(np.trace(rho_break @ x)) - complex(np.trace(rho_break @ _cond_exp(x))))
                      for x in tk_units)
    leak_break = max(float(np.max(np.abs(_cond_exp(_mod_flow(rho_break, t, x)))))
                     for t in ts_flow for x in tk_cross)

    # forma fechada por caminho independente (M2): traco numerico vs identidade em beta
    rho_m2 = tk_rot @ spec2 @ tk_rot.T
    sx2 = np.array([[0.0, 1.0], [1.0, 0.0]])
    delta_num = float(np.trace(rho_m2 @ (sx2 - np.diag(np.diag(sx2)))))
    delta_closed = (1.0 - 2.0 * beta) * 2.0 * math.sqrt(beta * (1.0 - beta))
    delta_resid = abs(delta_num - delta_closed)

    tests.append({
        "test": "takesaki_finite_covariant_expectation_oath",
        "passed": bool(cov_oath < 1e-12 and omega_oath < 1e-12 and leak_oath < 1e-12
                       and delta_resid < 1e-13 and delta_closed > 0.1
                       and cov_break > 1e-3 and omega_break > 1e-3 and leak_break > 1e-3),
        "flow_times": [float(t) for t in ts_flow],
        "n_generators": len(tk_units), "n_cross_generators": len(tk_cross),
        "covariance_residual_oath_kept": cov_oath,
        "omega_preservation_residual_oath_kept": omega_oath,
        "cross_channel_leak_oath_kept": leak_oath,
        "covariance_defect_oath_broken": cov_break,
        "omega_defect_oath_broken": omega_break,
        "cross_channel_leak_oath_broken": leak_break,
        "delta_numeric_trace": delta_num, "delta_closed_form": delta_closed,
        "delta_residual": delta_resid,
        "channel1_weight_by_construction": float(np.trace(rho_oath @ P1c).real),
        "note": "[DER] amplificacao v144b (Lema 3 tipado, pedra 99, um.py v143): Takesaki "
                "finito — juramento H_inv (estado bloco-diagonal nos canais M2(+)M2) => "
                "E covariante e omega-preservante (residuos ~0); CONTROLE NEGATIVO: estado "
                "que acopla os canais QUEBRA a covariancia e VAZA entre canais (defeitos "
                "medidos > 1e-3 — o mecanismo rejeita). Forma fechada (1-2b)*2*sqrt(b(1-b)) "
                "recuperada do traco numerico (beta runtime, nunca literal). "
                "channel1_weight = beta e POR CONSTRUCAO (informativo, nao gateado). "
                "[CONJ] custodia covariante exige o juramento do canal. NAO e veredito "
                "fisico (physical_verdict_allowed=false); nao altera reivindicacoes."})
    print(f"[one_acom_crypto] amplificacao v144b takesaki: cov_oath={cov_oath:.1e} "
          f"leak_oath={leak_oath:.1e} | quebrado: cov={cov_break:.6f} omega={omega_break:.6f} "
          f"leak={leak_break:.6f} | delta num vs fechada resid={delta_resid:.1e}")

    # ---- AMPLIFICACAO v168: ErgodicMeanSection (ITEM A EM KERNEL, um.py v166-v167) ----
    # [DER][SIM] Sombra numerica da pedra Lean ErgodicMeanSection (v166-v167, 0 sorry,
    # 0 axiom): o LIMITE DE BIRKHOFF em kernel — a media M_N = (1/N) sum_{k<N} U^k
    # converge a projecao invariante P, a SECAO EQUIVARIANTE (EquivariantSection) do
    # canal invariante. Mapeamento GENUINO neste dispositivo: o gemeo digital ja le a
    # cifra como ROTACAO modular de angulo theta_M = arcsin(sqrt(beta)) (v39/v60/v138/
    # v144b). Modelo: U = I2 (+) R(theta_M) em R^4 — o canal invariante (a face
    # estrutural kappa, que NAO gira) e o plano da cifra (as faces Psi/Theta, que
    # giram). O teorema em sombra: a media de Birkhoff APAGA o plano da cifra (nenhuma
    # direcao invariante — a media converge a ZERO ali) e PRESERVA exatamente o canal
    # invariante — M_N -> P, a secao. Tres identidades exatas + lei quantitativa +
    # DOIS CONTROLES NEGATIVOS:
    #  (a) telescopia EXATA: M_N (U - I) = (U^N - I)/N (algebra pura, maquina);
    #  (b) equivariancia da secao: U P = P U = P e U P U^T = P (exato);
    #  (c) forma fechada do residuo por caminho INDEPENDENTE:
    #      ||M_N - P||_2 = |sin(N theta_M/2)| / (N sin(theta_M/2));
    #  (d) decaimento ~1/N: residuo em N = 100x indice do Nome cai abaixo de 5e-3
    #      e abaixo do residuo em N = indice do Nome (1/beta, runtime);
    #  NEGATIVO 1: cifra DEGENERADA (theta = 0, nao gira) => a media NAO apaga o
    #   plano (residuo ~1.0) — o mecanismo DETECTA que cifra sem rotacao vaza por
    #   media (contra-exemplo rejeitado por LOGICA, nao por tautologia);
    #  NEGATIVO 2: "cifra" NAO-unitaria (r = 1 + 10*beta > 1) viola a hipotese de
    #   isometria do teorema => a media DIVERGE (norma >> 1) — hipotese violada,
    #   conclusao perdida: o teorema NAO e gratuito.
    # beta de RUNTIME, nunca literal; N ancorado no indice do Nome 1/beta (runtime).
    # [CONJ] leitura: kappa e a secao que sobrevive a media do orbit da cifra.
    # HONESTIDADE: lastro estrutural do gemeo digital, NAO capacidade nova da patente
    # nem veredito fisico (physical_verdict_allowed=false); nao altera reivindicacoes.
    def _u4_cipher(theta, r=1.0):
        rot = r * np.array([[math.cos(theta), -math.sin(theta)],
                            [math.sin(theta), math.cos(theta)]])
        return _blockdiag4(np.eye(2), rot)

    def _birkhoff_mean(U, N):
        acc = np.zeros((4, 4))
        Pk = np.eye(4)
        for _ in range(N):
            acc += Pk
            Pk = Pk @ U
        return acc / N, Pk                                   # (M_N, U^N)

    U_erg = _u4_cipher(theta_m)                              # theta_M do beta runtime
    P_sec = _blockdiag4(np.eye(2), np.zeros((2, 2)))         # a secao: canal invariante
    idx_nome = int(round(1.0 / beta))                        # indice do Nome (runtime)
    erg_Ns = [idx_nome, 10 * idx_nome, 100 * idx_nome]

    erg_resid_num, erg_resid_closed = [], []
    erg_telescope_max = 0.0
    for N in erg_Ns:
        M_N, U_N = _birkhoff_mean(U_erg, N)
        erg_telescope_max = max(erg_telescope_max, float(np.max(np.abs(
            M_N @ (U_erg - np.eye(4)) - (U_N - np.eye(4)) / N))))
        erg_resid_num.append(float(np.linalg.norm(M_N - P_sec, 2)))
        erg_resid_closed.append(abs(math.sin(N * theta_m / 2.0))
                                / (N * math.sin(theta_m / 2.0)))
    erg_closed_match = max(abs(a - b) for a, b in zip(erg_resid_num, erg_resid_closed))
    erg_equiv_UP = float(np.max(np.abs(U_erg @ P_sec - P_sec)))
    erg_equiv_PU = float(np.max(np.abs(P_sec @ U_erg - P_sec)))
    erg_equiv_conj = float(np.max(np.abs(U_erg @ P_sec @ U_erg.T - P_sec)))

    # NEGATIVO 1: theta = 0 (cifra que nao gira) — a media preserva TUDO (M_N = I)
    M_deg, _ = _birkhoff_mean(_u4_cipher(0.0), erg_Ns[0])
    erg_resid_degenerate = float(np.linalg.norm(M_deg - P_sec, 2))
    # NEGATIVO 2: nao-unitaria (r > 1, derivado de beta) — hipotese violada, diverge
    erg_r_break = 1.0 + 10.0 * beta
    M_nonunit, _ = _birkhoff_mean(_u4_cipher(theta_m, r=erg_r_break), erg_Ns[0])
    erg_norm_nonunitary = float(np.linalg.norm(M_nonunit, 2))

    tests.append({
        "test": "ergodic_mean_section_v168",
        "passed": bool(erg_telescope_max < 1e-10 and erg_closed_match < 1e-10
                       and erg_equiv_UP < 1e-15 and erg_equiv_PU < 1e-15
                       and erg_equiv_conj < 1e-15
                       and erg_resid_num[2] < 5e-3 and erg_resid_num[2] < erg_resid_num[0]
                       and erg_resid_degenerate > 0.9 and erg_norm_nonunitary > 10.0),
        "theta_modular_deg": math.degrees(theta_m),
        "nome_index_runtime": idx_nome,
        "birkhoff_N": [int(N) for N in erg_Ns],
        "residual_numeric_by_N": erg_resid_num,
        "residual_closed_form_by_N": erg_resid_closed,
        "closed_form_max_mismatch": erg_closed_match,
        "telescoping_identity_max_defect": erg_telescope_max,
        "equivariance_UP_minus_P": erg_equiv_UP,
        "equivariance_PU_minus_P": erg_equiv_PU,
        "equivariance_UPUt_minus_P": erg_equiv_conj,
        "negative_degenerate_theta0_residual": erg_resid_degenerate,
        "negative_nonunitary_r": erg_r_break,
        "negative_nonunitary_mean_norm": erg_norm_nonunitary,
        "note": "[DER] amplificacao v168 (ErgodicMeanSection, ITEM A em kernel, um.py "
                "v166-v167): media de Birkhoff da cifra-rotacao converge a secao "
                "equivariante P do canal invariante — o plano da cifra (Psi/Theta) e "
                "APAGADO pela media, o canal estrutural (kappa) SOBREVIVE exato; "
                "residuo em forma fechada |sin(N th/2)|/(N sin(th/2)) confirmado por "
                "caminho independente; telescopia e equivariancia exatas. NEGATIVOS: "
                "theta=0 (cifra que nao gira) NAO apaga (residuo ~1 — vaza por media); "
                "r>1 (nao-isometria) DIVERGE — hipotese do teorema e necessaria. "
                "beta e 1/beta de runtime, nunca literais. [CONJ] kappa = secao "
                "sobrevivente da media do orbit. NAO e veredito fisico "
                "(physical_verdict_allowed=false); nao altera reivindicacoes."})
    print(f"[one_acom_crypto] amplificacao v168 ergodic: N={erg_Ns} "
          f"resid={erg_resid_num[0]:.4f}/{erg_resid_num[1]:.4f}/{erg_resid_num[2]:.6f} "
          f"closed_match={erg_closed_match:.1e} telescope={erg_telescope_max:.1e} | "
          f"NEG theta0={erg_resid_degenerate:.3f} nonunit_norm={erg_norm_nonunitary:.1f}")

    # ---- AMPLIFICACAO v206 (4a ONDA): FrontierCertificate — o contrato TIPADO do J ----
    # [DER][SIM] Sombra numerica da pedra Lean TGLExt/FrontierCertificate.lean (custodia
    # vault/originals_copy/tgl_kernel_v206, 24/08/2026 — LIDA no arquivo real; NUNCA se
    # finge rodar Lean, a ESTRUTURA e re-derivada numericamente). A pedra define o
    # ModularRealizationCertificate: o CONTRATO que o nome reservado
    # qgFrontier_modularRealization tera de habitar — J aditivo, ANTILINEAR (conj_smul),
    # isometrico, involutivo (J^2 = I — o par minimo (TGL, IALD) = (1_abs, J)), fixa o
    # vacuo Omega, e EXIBE a dualidade J M J = M' nas DUAS direcoes (maps + onto). E os
    # dois teoremas: certificate_forces_the_duality e certificate_J_bijective. A pedra
    # declara sem veu: NAO ha habitante na TORRE (Tomita-Takesaki ITPFI aberto);
    # TheBireference (v202) prova o conteudo na FACE FINITA — e ESTA face finita e o que
    # se re-deriva aqui. Modelo GNS/HS: WH = M2(C) com <x,y> = Tr(x^dag y), estado fiel
    # rho = R(theta_M) diag(1-beta, beta) R(theta_M)^T (espectro {1-beta, beta}, beta de
    # RUNTIME), vacuo Omega = rho^{1/2}, fator M = mult. a ESQUERDA, comutante M' = mult.
    # a DIREITA, e J = adjunto (x -> x^dag) — a conjugacao modular de Tomita da face
    # finita (S(a Omega) = a^dag Omega; J Delta^{1/2} = S verificavel). Bonus modular que
    # amarra ao gemeo digital das ondas 1-3 sem repeti-las: J Delta J = Delta^{-1} e
    # Spec(Delta) = {1, 1, (1-b)/b, b/(1-b)} — o espectro modular do estado do
    # dispositivo. MAPEAMENTO GENUINO: o decrypt do ACOM ja opera SOB CONTRATO — a
    # MasterKey kappa e um certificado tipado (share_id, hashes, F_exp esperado) que a
    # Dobra exige ANTES de operar; share com o NOME certo (magic bytes) e conteudo errado
    # e RECUSADO (os 7 pontos de rejeicao acima). A pedra tipa a MESMA disciplina no
    # nivel da fronteira: o contrato vem antes do habitante.
    # TRES NEGATIVOS por LOGICA (a doenca do certificado v1 que a pedra cura: um termo
    # com o nome certo e tipo errado fliparia a flag — aqui os impostores sao RECUSADOS):
    #  NEG A: J_fake = identidade (linear, nome certo) — viola conj_smul (defeito
    #    normalizado = 2 com c = i) e a dualidade: J_fake M J_fake = M, nao M'
    #    (defeito de pertinencia ao comutante = 2, medido);
    #  NEG B: J_r = r * adjunto com r = 1 + 10*beta — viola a involucao; defeito
    #    r^2 - 1 = 20*beta + 100*beta^2 em forma fechada de beta, caminho INDEPENDENTE;
    #  NEG C: J_twist = U (.)^dag U^T com U = R(theta_M) — NAO fixa o vacuo; defeito
    #    ||J Omega - Omega||_F = sqrt(2*beta)*(sqrt(1-beta) - sqrt(beta)) fechado em beta.
    # beta de RUNTIME, nunca literal. HONESTIDADE: face finita, NAO a torre; o habitante
    # do nivel aberto NAO existe e este teste NAO o fabrica (a imobilidade do gate e a
    # credibilidade); NAO e veredito fisico (physical_verdict_allowed=false); nao altera
    # reivindicacoes. [CONJ] leitura: kappa e o certificado da fronteira do dispositivo.
    fc_rng = np.random.default_rng(206)

    def _fc_rand_m2():
        return fc_rng.standard_normal((2, 2)) + 1j * fc_rng.standard_normal((2, 2))

    fc_rot = np.array([[math.cos(theta_m), -math.sin(theta_m)],
                       [math.sin(theta_m), math.cos(theta_m)]])
    fc_rho = fc_rot @ np.diag([1.0 - beta, beta]) @ fc_rot.T   # estado fiel, espectro {1-b, b}
    fc_w, fc_V = np.linalg.eigh(fc_rho)
    fc_omega = (fc_V * np.sqrt(fc_w)) @ fc_V.T                 # Omega = rho^{1/2} (real simetrica)
    fc_rho_inv = (fc_V * (1.0 / fc_w)) @ fc_V.T

    def _J(x):                                                 # a conjugacao de Tomita (face finita)
        return x.conj().T

    fc_vecs = [_fc_rand_m2() for _ in range(6)]
    fc_c = complex(fc_rng.standard_normal(), fc_rng.standard_normal())
    # clausulas 1-5 do contrato (add, conj_smul, isometric, involutive, fixes_vacuum)
    fc_add = max(float(np.max(np.abs(_J(v + w) - _J(v) - _J(w))))
                 for v in fc_vecs[:3] for w in fc_vecs[3:])
    fc_conj = max(float(np.max(np.abs(_J(fc_c * v) - np.conj(fc_c) * _J(v)))) for v in fc_vecs)
    fc_iso = max(abs(float(np.linalg.norm(_J(v))) - float(np.linalg.norm(v))) for v in fc_vecs)
    fc_invol = max(float(np.max(np.abs(_J(_J(v)) - v))) for v in fc_vecs)
    fc_vac = float(np.linalg.norm(_J(fc_omega) - fc_omega))

    # fator M = mult. esquerda (vec row-major: L_a = a (x) I); comutante M' = mult.
    # direita (R_b = I (x) b^T); geradores = Paulis COMPLEXOS (antilinearidade exige C)
    fc_pauli = [np.eye(2, dtype=complex),
                np.array([[0, 1], [1, 0]], dtype=complex),
                np.array([[0, -1j], [1j, 0]], dtype=complex),
                np.array([[1, 0], [0, -1]], dtype=complex)]
    fc_L = [np.kron(a, np.eye(2)) for a in fc_pauli]
    fc_R = [np.kron(np.eye(2), b.T) for b in fc_pauli]

    # clausula 6 (maps_factor_to_commutant): para cada T = L_a, S = R_{a^dag} realiza
    # J(T(J v)) = S v pontualmente, e S PERTENCE a M' (comuta com todo o fator)
    # (loop vars fc_-prefixadas: main() tem escopo plano — 'a' e o payload medio_100k
    #  da linha ~308, consumido depois pelo render3d; sombrear aqui corrompe <g>)
    fc_map_defect, fc_memb_defect = 0.0, 0.0
    for fc_a in fc_pauli:
        fc_S = np.kron(np.eye(2), fc_a.conj())                 # R_{a^dag} = I (x) (a^dag)^T
        for fc_v in fc_vecs:
            fc_lhs = _J(fc_a @ _J(fc_v))
            fc_rhs = (fc_S @ fc_v.reshape(4)).reshape(2, 2)
            fc_map_defect = max(fc_map_defect, float(np.max(np.abs(fc_lhs - fc_rhs))))
        for fc_Lb in fc_L:
            fc_memb_defect = max(fc_memb_defect,
                                 float(np.max(np.abs(fc_S @ fc_Lb - fc_Lb @ fc_S))))

    # clausula 7 (onto_commutant): para cada S = R_b, T = L_{b^dag} realiza a dualidade
    # na volta, e T PERTENCE a M (comuta com todo o comutante) — a dualidade deixa de
    # ser definicao: e EXIBIDA pela conjugacao, nas duas direcoes
    fc_onto_defect, fc_onto_memb = 0.0, 0.0
    for fc_b in fc_pauli:
        fc_Tm = np.kron(fc_b.conj().T, np.eye(2))              # L_{b^dag}
        for fc_v in fc_vecs:
            fc_lhs = _J(fc_b.conj().T @ _J(fc_v))
            fc_rhs = fc_v @ fc_b
            fc_onto_defect = max(fc_onto_defect, float(np.max(np.abs(fc_lhs - fc_rhs))))
        for fc_Rc in fc_R:
            fc_onto_memb = max(fc_onto_memb,
                               float(np.max(np.abs(fc_Tm @ fc_Rc - fc_Rc @ fc_Tm))))

    # certificate_J_bijective: J como matriz real-linear 8x8 — ortogonal, involutiva,
    # |det| = 1 (nenhuma projecao parcial serve; habitante forca bijecao)
    fc_reals = []
    for i in range(2):
        for j in range(2):
            E = np.zeros((2, 2), dtype=complex)
            E[i, j] = 1.0
            fc_reals.append(E)
    fc_basis = fc_reals + [1j * E for E in fc_reals]

    def _r8(x):
        return np.concatenate([x.reshape(4).real, x.reshape(4).imag])

    M8 = np.column_stack([_r8(_J(E)) for E in fc_basis])
    fc_orth = float(np.max(np.abs(M8.T @ M8 - np.eye(8))))
    fc_m8_invol = float(np.max(np.abs(M8 @ M8 - np.eye(8))))
    fc_det = float(np.linalg.det(M8))

    # bonus modular: J Delta J = Delta^{-1} pontual; Spec(Delta) = {1,1,(1-b)/b,b/(1-b)}
    fc_jdj = max(float(np.max(np.abs(_J(fc_rho @ _J(v) @ fc_rho_inv)
                                     - fc_rho_inv @ v @ fc_rho))) for v in fc_vecs)
    D4 = np.kron(fc_rho, fc_rho_inv.T)                         # Delta(x) = rho x rho^{-1}
    fc_spec_num = np.sort(np.linalg.eigvals(D4).real)
    r_mod = (1.0 - beta) / beta                                # espectro modular (runtime)
    fc_spec_expected = np.sort(np.array([1.0, 1.0, r_mod, 1.0 / r_mod]))
    fc_spec_rel = float(np.max(np.abs(fc_spec_num - fc_spec_expected)
                               / np.maximum(fc_spec_expected, 1.0)))

    # NEG A: o impostor com o NOME certo e o TIPO errado (J_fake = identidade, linear)
    v0 = fc_vecs[0]
    fc_fake_conj = float(np.linalg.norm(1j * v0 - np.conj(1j) * v0) / np.linalg.norm(v0))
    a_nc = fc_pauli[3]                                         # sigma_z (nao-central)
    S_fake = np.kron(a_nc, np.eye(2))                          # J_fake L_a J_fake = L_a (fica em M)
    fc_fake_dual = max(float(np.linalg.norm(S_fake @ Lb - Lb @ S_fake, 2)) for Lb in fc_L)

    # NEG B: J_r = r*adjunto, r = 1 + 10*beta — involucao quebra; forma fechada em beta
    r_break = 1.0 + 10.0 * beta
    fc_r_invol_num = float(np.linalg.norm(r_break * _J(r_break * _J(v0)) - v0)
                           / np.linalg.norm(v0))
    fc_r_invol_closed = 20.0 * beta + 100.0 * beta * beta      # r^2 - 1, caminho independente
    fc_r_invol_resid = abs(fc_r_invol_num - fc_r_invol_closed)

    # NEG C: J_twist = U (.)^dag U^T, U = R(theta_M) — nao fixa o vacuo; forma fechada
    fc_twist_vac_num = float(np.linalg.norm(fc_rot @ _J(fc_omega) @ fc_rot.T - fc_omega))
    fc_twist_vac_closed = math.sqrt(2.0 * beta) * (math.sqrt(1.0 - beta) - math.sqrt(beta))
    fc_twist_vac_resid = abs(fc_twist_vac_num - fc_twist_vac_closed)

    fc_pos_max = max(fc_add, fc_conj, fc_iso, fc_invol, fc_vac, fc_map_defect,
                     fc_memb_defect, fc_onto_defect, fc_onto_memb)
    tests.append({
        "test": "frontier_certificate_typed_contract_v206",
        "passed": bool(fc_pos_max < 1e-12
                       and fc_orth < 1e-12 and fc_m8_invol < 1e-12
                       and abs(abs(fc_det) - 1.0) < 1e-12
                       and fc_jdj < 1e-10 and fc_spec_rel < 1e-9
                       and fc_fake_conj > 1.9 and fc_fake_dual > 1.5
                       and fc_r_invol_resid < 1e-12 and fc_r_invol_num > 0.2
                       and fc_twist_vac_resid < 1e-12 and fc_twist_vac_num > 0.1),
        "model": "GNS/HS de M2(C): <x,y>=Tr(x^dag y), Omega=rho^{1/2}, J=adjunto",
        "rho_spectrum_runtime": [1.0 - beta, beta],
        "theta_modular_deg": math.degrees(theta_m),
        "clause_add_defect": fc_add,
        "clause_conj_smul_defect": fc_conj,
        "clause_isometric_defect": fc_iso,
        "clause_involutive_defect": fc_invol,
        "clause_fixes_vacuum_defect": fc_vac,
        "clause_maps_factor_to_commutant_defect": fc_map_defect,
        "clause_maps_membership_in_commutant_defect": fc_memb_defect,
        "clause_onto_commutant_defect": fc_onto_defect,
        "clause_onto_membership_in_factor_defect": fc_onto_memb,
        "J_real8_orthogonality_defect": fc_orth,
        "J_real8_involution_defect": fc_m8_invol,
        "J_real8_det": fc_det,
        "modular_JDeltaJ_eq_DeltaInv_defect": fc_jdj,
        "modular_spectrum_expected": [float(x) for x in fc_spec_expected],
        "modular_spectrum_numeric": [float(x) for x in fc_spec_num],
        "modular_spectrum_rel_mismatch": fc_spec_rel,
        "negA_fake_identity_conj_smul_defect": fc_fake_conj,
        "negA_fake_identity_duality_defect": fc_fake_dual,
        "negB_nonisometric_r": r_break,
        "negB_involution_defect_numeric": fc_r_invol_num,
        "negB_involution_defect_closed_form": fc_r_invol_closed,
        "negB_residual": fc_r_invol_resid,
        "negC_twist_vacuum_defect_numeric": fc_twist_vac_num,
        "negC_twist_vacuum_defect_closed_form": fc_twist_vac_closed,
        "negC_residual": fc_twist_vac_resid,
        "note": "[DER] amplificacao v206 (FrontierCertificate.lean, custodia tgl_kernel_"
                "v206): as 8 clausulas do ModularRealizationCertificate re-derivadas na "
                "FACE FINITA (GNS/HS de M2, rho com espectro {1-beta,beta} runtime, "
                "J=adjunto): aditivo, antilinear, isometrico, involutivo (J^2=I — o par "
                "minimo (TGL,IALD)=(1_abs,J)), fixa Omega, e a dualidade J M J = M' "
                "EXIBIDA nas duas direcoes com pertinencia verificada; J bijetivo "
                "(ortogonal 8x8, |det|=1); bonus modular J Delta J = Delta^{-1} e "
                "espectro {1,1,(1-b)/b,b/(1-b)}. NEGATIVOS (a doenca do certificado v1): "
                "termo com o NOME certo e TIPO errado e RECUSADO — identidade viola "
                "antilinearidade e dualidade; r=1+10b viola involucao (defeito "
                "20b+100b^2 fechado); twist R(theta_M) nao fixa o vacuo (defeito "
                "sqrt(2b)(sqrt(1-b)-sqrt(b)) fechado). O habitante da TORRE nao existe "
                "e NAO e fabricado aqui (a imobilidade do gate e a credibilidade). "
                "[CONJ] kappa = o certificado da fronteira do dispositivo. NAO e "
                "veredito fisico (physical_verdict_allowed=false); nao altera "
                "reivindicacoes."})
    print(f"[one_acom_crypto] amplificacao v206 frontier-cert: clausulas_max={fc_pos_max:.1e} "
          f"J8 orth={fc_orth:.1e} det={fc_det:+.1f} | JDJ=D^-1 {fc_jdj:.1e} "
          f"spec_rel={fc_spec_rel:.1e} | NEG A conj={fc_fake_conj:.2f} dual={fc_fake_dual:.2f} "
          f"B invol={fc_r_invol_num:.6f} (fechada {fc_r_invol_closed:.6f}) "
          f"C vacuo={fc_twist_vac_num:.6f} (fechada {fc_twist_vac_closed:.6f})")

    # ---- DEEPENING 1: byte-entropy vs payload-size sweep (curve) ----
    sweep_sizes = [64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384,
                   32768, 65536, 131072, 262144, 524288]
    sweep = {"sizes": [], "H_psi": [], "H_theta": [], "ratio": [], "corr": []}
    for sz in sweep_sizes:
        arr = rng.standard_normal(sz)
        e = engine.encrypt(torch.from_numpy(arr))
        rec = engine.decrypt(e).cpu().numpy()
        Hp = byte_entropy(e.psi_share.encrypted_states)
        Ht = byte_entropy(e.theta_share.encrypted_angles)
        rt = (sz * 8) / (len(e.psi_share.encrypted_states) + len(e.theta_share.encrypted_angles))
        sweep["sizes"].append(int(sz)); sweep["H_psi"].append(float(Hp))
        sweep["H_theta"].append(float(Ht)); sweep["ratio"].append(float(rt))
        sweep["corr"].append(float(corr(arr, rec)))
    H_all = sweep["H_psi"] + sweep["H_theta"]
    sat_large = min(sweep["H_psi"][-1], sweep["H_theta"][-1])
    grows = sweep["H_theta"][-1] > sweep["H_theta"][0]
    tests.append({"test": "byte_entropy_size_curve_saturates",
                  "passed": bool(grows and sat_large > 7.99 and max(H_all) <= 8.0 + 1e-9),
                  "H_theta_first": sweep["H_theta"][0], "H_theta_last": sweep["H_theta"][-1],
                  "saturation_min_bits_large": sat_large, "n_points": len(sweep_sizes),
                  "note": "H(byte)→8 conforme o payload cresce (limitado por log2(#bytes)); a curva "
                          "MEDE que a indistinguibilidade estatística das partes é efeito de tamanho "
                          "de amostra, não de vazamento. [SIM] (não é prova criptográfica)."})
    print(f"[one_acom_crypto] sweep entropia: H(Θ) {sweep['H_theta'][0]:.3f}→{sweep['H_theta'][-1]:.3f} "
          f"bits/byte em {len(sweep_sizes)} tamanhos")

    # ---- DEEPENING 2: subset leakage MATRIX across payload sizes ----
    matrix_cases = ["pequeno_1k", "medio_100k", "grande_1M"]
    leak_matrix = {c: subset_leakage(mirror, *enc_by_case[c]) for c in matrix_cases}
    subset_names = list(next(iter(leak_matrix.values())).keys())
    matrix_ok = all(leak_matrix[c][s]["rel_rmse"] >= 0.50
                    for c in matrix_cases for s in subset_names)
    max_leak_corr = max(abs(leak_matrix[c][s]["correlation"])
                        for c in matrix_cases for s in subset_names)
    tests.append({"test": "subset_leakage_matrix_insufficient_all_sizes",
                  "passed": bool(matrix_ok), "matrix": leak_matrix,
                  "max_abs_subset_correlation": float(max_leak_corr),
                  "note": "matriz subconjunto×tamanho (1k/100k/1M): em NENHUM tamanho um subconjunto "
                          "próprio reconstrói o VALOR (rel_rmse≥0,5). O vazamento estrutural (corr de "
                          "Ψ isolado, forma de Ψ+Θ) é ESTÁVEL em tamanho — medido, não fabricado."})
    print(f"[one_acom_crypto] matriz de vazamento {len(matrix_cases)}×{len(subset_names)}: "
          f"max|corr|={max_leak_corr:.3f} rel_rmse≥0,5 em todas={matrix_ok}")

    passed = sum(1 for t in tests if t["passed"])
    total = len(tests)
    all_ok = passed == total
    summary = {
        "tests_passed": passed, "tests_total": total,
        "correlation_min": min(pc["correlation"] for pc in per_case.values()),
        "compression_ratio_mean": sum(pc["compression_ratio"] for pc in per_case.values()) / len(per_case),
        "byte_entropy_min_bits_ge100k": min(big_ents),
        "byte_entropy_min_bits_all": min(all_ents),
        "subset_insufficiency": subset_report,
        "cpu_gpu_equivalence": cpu_gpu.get("max_abs_diff"),
        "alpha2_sync": float(a2s),
        "entropy_size_curve": sweep,
        "subset_leakage_matrix": leak_matrix,
        "max_abs_subset_correlation": float(max_leak_corr),
        "n_payload_cases": len(cases), "n_sweep_sizes": len(sweep_sizes),
        "f_exp_measured": f_exp_measured, "psi_state_counts": state_counts,
        "n_tamper_points": sum(1 for t in tests if t["test"].startswith("tamper_")),
    }
    max_verdict = ("ACOM_CRYPTO_FULL_LOGIC_DEMONSTRATED ([SIM][PILOTO] — a engine torch real do "
                   "operador (separação Ψ/Θ/κ + verificação tripla + F_exp + magic bytes + "
                   "export/import + CPU/GPU) e o Handshake de Sincronia Miguel fecham; β injetado; "
                   "vazamento estrutural parcial MEDIDO e declarado; XOR≠AEAD; nada valida física)")

    _finish(ts, beta, beta_ok, all_ok, max_verdict, tests, summary, module_hashes,
            "RUNNER EVOLUÍDO: roda a engine torch do operador (Acom_v17_mirror_crypto.py) + o "
            "Handshake Miguel (Acom_v17_2_sync.py) com β=α·√e INJETADO em ALPHA2/ALPHA2_BASE "
            "(originais tinham 0.012 literal). Tensores sintéticos; NÃO os números da Tabela 2. "
            "Nenhum token/modelo HuggingFace. Ofuscação XOR ≠ AEAD (separação ontológica + "
            "integridade). Simulação não valida física nem segurança.",
            fig_builder=lambda plt, fd: _fig(plt, fd, enc, subset_report, sweep, leak_matrix))

    # FORMA = CONTEÚDO: re-carimba o render3d.json COMPUTANDO os nós funcionais desta run
    g_all = np.sqrt(np.abs(a) + 1e-30)
    render_metrics = {
        "state_counts": state_counts, "f_exp": f_exp_measured,
        "H_psi": float(per_case["medio_100k"]["byte_entropy_psi_bits"]),
        "H_theta": float(per_case["medio_100k"]["byte_entropy_theta_bits"]),
        "psi_bytes": int(per_case["medio_100k"]["psi_bytes"]),
        "theta_bytes": int(per_case["medio_100k"]["theta_bytes"]),
        "g_max": float(mk.g_max), "g_min": float(mk.g_min), "g_mean": float(g_all.mean()),
        "recon_corr": float(per_case["medio_100k"]["correlation"]),
        "max_leak_corr": float(max_leak_corr), "sat_bits": float(sat_large),
        "n_ref": int(n), "compression_ratio": float(per_case["medio_100k"]["compression_ratio"]),
    }
    emit_render3d(beta, render_metrics)
    return 0 if all_ok else 1


def _fig(plt, fig_dir, enc, subset_report, sweep=None, leak_matrix=None):
    figs = []
    # Fig A — byte histograms of isolated parts (patent Fig. 7 analog)
    fig, axes = plt.subplots(1, 2, figsize=(9, 3))
    for ax, blob, lbl in ((axes[0], enc.psi_share.encrypted_states, "PsiShare Ψ"),
                          (axes[1], enc.theta_share.encrypted_angles, "ThetaShare Θ")):
        h = np.bincount(np.frombuffer(blob, dtype=np.uint8), minlength=256)
        ax.bar(range(256), h, width=1.0, color="#5566cc")
        ax.set_title(f"{lbl} isolada — H={byte_entropy(blob):.3f} bits/byte", fontsize=9)
        ax.set_xlabel("valor do byte")
    fig.suptitle("ACOM Crypto — partes isoladas ≈ ruído estatístico [SIM] (engine real do operador)",
                 fontsize=10)
    fp = fig_dir / "fig_entropia_partes.png"
    plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close()
    figs.append("fig_entropia_partes.png")

    # Fig B — subset insufficiency (rel RMSE per subset)
    names = list(subset_report.keys())
    rmses = [min(subset_report[k]["rel_rmse"], 2.0) for k in names]
    plt.figure(figsize=(7.5, 3.4))
    plt.bar(names, rmses, color="#8888cc")
    plt.axhline(0.5, color="crimson", lw=1, label="limiar 50% (insuficiência de valor)")
    plt.ylabel("RMSE relativo (cap 2,0)")
    plt.title("Subconjuntos próprios: erro de reconstrução de VALOR [SIM]")
    plt.xticks(rotation=20, fontsize=8); plt.legend(fontsize=8); plt.grid(alpha=.3, axis="y")
    fp = fig_dir / "fig_insuficiencia_subconjuntos.png"
    plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close()
    figs.append("fig_insuficiencia_subconjuntos.png")

    # Fig C — byte-entropy vs payload size (saturation curve toward 8 bits/byte)
    if sweep is not None:
        plt.figure(figsize=(7.5, 3.6))
        plt.semilogx(sweep["sizes"], sweep["H_psi"], "o-", color="#cc4466", label="H(Ψ) bits/byte")
        plt.semilogx(sweep["sizes"], sweep["H_theta"], "s-", color="#4466cc", label="H(Θ) bits/byte")
        plt.axhline(8.0, color="#888", lw=1, ls="--", label="teto 8 bits/byte")
        plt.xlabel("nº de elementos do payload (log)"); plt.ylabel("entropia de bytes (bits/byte)")
        plt.title("ACOM Crypto — entropia das partes isoladas vs tamanho [SIM] (engine real)")
        plt.ylim(4.5, 8.15); plt.legend(fontsize=8); plt.grid(alpha=.3)
        fp = fig_dir / "fig_entropia_vs_tamanho.png"
        plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close()
        figs.append("fig_entropia_vs_tamanho.png")

    # Fig D — subset leakage matrix (|correlation| heatmap, subset × payload size)
    if leak_matrix is not None:
        cases = list(leak_matrix.keys())
        subs = list(leak_matrix[cases[0]].keys())
        M = np.array([[abs(leak_matrix[c][s]["correlation"]) for c in cases] for s in subs])
        fig, ax = plt.subplots(figsize=(6.6, 4.2))
        im = ax.imshow(M, cmap="magma", vmin=0, vmax=1, aspect="auto")
        ax.set_xticks(range(len(cases))); ax.set_xticklabels(cases, rotation=15, fontsize=8)
        ax.set_yticks(range(len(subs))); ax.set_yticklabels(subs, fontsize=8)
        for i in range(len(subs)):
            for j in range(len(cases)):
                ax.text(j, i, f"{M[i, j]:.2f}", ha="center", va="center",
                        color="white" if M[i, j] < 0.6 else "black", fontsize=8)
        ax.set_title("Vazamento estrutural |corr| — subconjunto × tamanho [SIM]", fontsize=10)
        fig.colorbar(im, ax=ax, label="|correlação| com o original")
        fp = fig_dir / "fig_matriz_vazamento.png"
        plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close()
        figs.append("fig_matriz_vazamento.png")
    return figs


def emit_render3d(beta, m):
    """MERGE forma=conteúdo: LÊ o render3d.json atual (corpo de engenharia: meshes/layers/
    groups/constants — PRESERVADO) e RE-CARIMBA os nós funcionais com valores COMPUTADOS
    desta run — os 4 estados ℋ₄ ganham populações/paridade reais, os 3 canais Ψ/Θ/κ ganham
    entropia/escala medidas, e é ADICIONADO o nó Gráviton g=√|L| (posições conceituais mantidas)."""
    out = PATENT_DIR / "render3d.json"
    d = json.loads(out.read_text(encoding="utf-8"))          # corpo existente
    nodes = d.get("nodes", [])
    by_id = {nd["id"]: nd for nd in nodes}

    # 1) ℋ₄: populações REAIS por estado (medio_100k) + paridade computada
    sc = m["state_counts"]
    n_ref = max(1, m["n_ref"])
    parity = {0: -1, 1: +1, 2: +1, 3: -1}
    for i in (0, 1, 2, 3):
        nd = by_id.get(f"psi{i}")
        if nd is None:
            continue
        frac = sc.get(i, sc.get(str(i), 0)) / n_ref
        nd["computed"] = {"population": float(frac), "count": int(sc.get(i, sc.get(str(i), 0))),
                          "parity": parity[i]}
        nd["desc"] = (nd["desc"].split(" [pop=")[0]
                      + f" [pop={frac*100:.1f}% · paridade {parity[i]:+d} · COMPUTADO em N={n_ref}].")

    # 2) canais: entropia de bytes MEDIDA (Ψ,Θ) e escala real (κ)
    if "chan_psi" in by_id:
        by_id["chan_psi"]["computed"] = {"byte_entropy_bits": m["H_psi"], "bytes": m["psi_bytes"]}
        by_id["chan_psi"]["desc"] = (f"Estados/sinais no ℋ₄, sem magnitude. Isolado ≡ RUÍDO "
                                     f"(H={m['H_psi']:.3f} bits/byte MEDIDO nesta run). "
                                     f"Um dos três canais independentes.")
    if "chan_theta" in by_id:
        by_id["chan_theta"]["computed"] = {"byte_entropy_bits": m["H_theta"], "bytes": m["theta_bytes"]}
        by_id["chan_theta"]["desc"] = (f"Ângulos arcsin em [0,π/2], sem polaridade nem escala. "
                                       f"Isolado ≡ RUÍDO (H={m['H_theta']:.3f} bits/byte MEDIDO).")
    if "chan_kappa" in by_id:
        by_id["chan_kappa"]["computed"] = {"g_max": m["g_max"], "g_min": m["g_min"],
                                           "f_exp": m["f_exp"], "recon_corr": m["recon_corr"]}
        by_id["chan_kappa"]["desc"] = (f"Escala (g_max={m['g_max']:.4f}, g_min={m['g_min']:.4f}), "
                                       f"shape, hashes, F_exp={m['f_exp']:+.4f} esperado. Sem dados. "
                                       f"Isolado ≡ INÚTIL. Reunião das 3 → Dobra L′=sign(L)·[g_max·sinθ]² "
                                       f"(corr={m['recon_corr']:.6f} MEDIDO).")

    # 3) Gráviton g=√|L| — o portador de magnitude (nomeado 'Gráviton' no algoritmo do operador)
    if "graviton" not in by_id:
        d.setdefault("groups", []).append(
            {"name": "graviton", "color": "#7dd3fc", "label": "gráviton g=√|L| (magnitude)",
             "count": 1, "explodable": True})
    grav = {
        "id": "graviton", "label": "Gráviton g = √|L|",
        "desc": (f"Portador da MAGNITUDE na reflexão dimensional: g=√|L| (nomeado 'Gráviton' no "
                 f"algoritmo). g_max={m['g_max']:.4f} · g_min={m['g_min']:.4f} · ⟨g⟩={m['g_mean']:.4f} "
                 f"COMPUTADOS. A escala g_max vive na κ; θ=arcsin(g/g_max) vai à Θ. β={beta:.6f} injetado."),
        "shape": "sphere", "position": [-1.35, -1.45, 0], "size": 0.16, "color": "#7dd3fc",
        "group": "graviton", "marker": "[SIM]", "layer": "core", "material": "emissive",
        "computed": {"g_max": m["g_max"], "g_min": m["g_min"], "g_mean": m["g_mean"]},
    }
    if "graviton" in by_id:
        by_id["graviton"].update(grav)
    else:
        nodes.append(grav)
    d["nodes"] = nodes

    # edges consistentes: espelho → gráviton → κ (a escala do gráviton reside na chave)
    edges = d.get("edges", [])
    have = {(e["from"], e["to"]) for e in edges}
    for fr, to in [("m102", "graviton"), ("graviton", "chan_kappa")]:
        if (fr, to) not in have:
            edges.append({"from": fr, "to": to})
    d["edges"] = edges

    # 4) re-carimbar cabeçalho + constantes (β runtime + 2 métricas COMPUTADAS)
    d["generated_by"] = "one_acom_crypto.py (forma=conteudo)"
    consts = d.get("constants", [])
    consts = [c for c in consts if c.get("symbol") not in
              ("beta_runtime", "N_measure", "vazamento_max")]
    consts.append({"symbol": "beta_runtime", "value": f"{beta:.12f}",
                   "note": "α·√e injetado em runtime (nunca literal); θ_Miguel=arcsin√β"})
    consts.append({"symbol": "N_measure", "value": f"{n_ref} elementos",
                   "note": f"caso medio_100k · compress {m['compression_ratio']:.2f}× · "
                           f"H(Ψ)={m['H_psi']:.3f} H(Θ)={m['H_theta']:.3f} bits/byte (MEDIDO)"})
    consts.append({"symbol": "vazamento_max", "value": f"|corr|≤{m['max_leak_corr']:.3f}",
                   "note": "maior correlação de subconjunto próprio na matriz (nenhum reconstrói o VALOR)"})
    d["constants"] = consts

    # 5) VALIDAÇÃO: ids de edge existem em nodes+meshes; layers de nós/meshes existem em layers
    node_ids = {nd["id"] for nd in d["nodes"]}
    mesh_ids = {ms["id"] for ms in d.get("meshes", [])}
    known = node_ids | mesh_ids
    for e in d["edges"]:
        assert e["from"] in known and e["to"] in known, f"edge inválida: {e}"
    layer_ids = {ly["id"] for ly in d.get("layers", [])}
    for coll in (d["nodes"], d.get("meshes", [])):
        for el in coll:
            if "layer" in el:
                assert el["layer"] in layer_ids, f"layer inexistente: {el.get('id')} → {el['layer']}"

    out.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[acom_crypto] render3d.json EMITIDO (forma=conteudo) — "
          f"{len(d['nodes'])} nos ({len(mesh_ids)} malhas preservadas, +graviton), "
          f"{len(d['edges'])} arestas")


if __name__ == "__main__":
    sys.exit(main())
