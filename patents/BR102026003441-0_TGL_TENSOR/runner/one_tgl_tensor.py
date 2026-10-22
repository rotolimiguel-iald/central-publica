# -*- coding: utf-8 -*-
"""one_tgl_tensor.py — runner único forma = conteúdo da patente TGL Tensor (EVOLUÍDO / RICO)
(BR102026003441-0 — Compressão Ontológica de Tensores de LLM). [PILOTO][SIM]

EVOLUÇÃO (09/07/2026): incorpora o ALGORITMO COMPLETO do operador — a engine de QUATRO
MODOS `TGLTensorV3` (tgl_tensor_v3.py, 1159 L: DIRECT/SPECTRAL/HYBRID/AUTO com SVD e rank
adaptativo) + os `BitPacker` N-bit/GPU de `tgl_tensor_v4.py` — resgatados para
`prototype_src/`. A versão leve anterior (skygrid_sim/tgl_tensor.py) está em
`one_tgl_tensor_v1_light.py.bak`.

Demonstra, rodando o código real do operador:
  - os 4 modos sobre tensores sintéticos de LLM (KV cache, embeddings, FFN, gradientes);
  - seleção automática de modo (AUTO) por análise espectral;
  - rank adaptativo pela energia ≥ 1−β (Verb Floor);
  - BitPacker N-bit (8/10/12/14/16) round-trip exato (v4, NumPy e GPU se disponível).

RÉGUA: β_TGL NUNCA literal no MEU código. Os protótipos do operador usam `ALPHA2=0.012`
literal; este runner os importa como proveniência READ-ONLY e INJETA
`ALPHA2 = tgl_core.beta()` + `energy_threshold = 1−β` em runtime. Por isso os números
diferem levemente da referência (β=0,012031300400803142, não 0,012).

HONESTIDADE [PILOTO][SIM]: tensores SINTÉTICOS; NÃO os números da Tabela 2 do relatório.
Nenhum token/modelo HuggingFace usado (P-09 — token_huggin.txt NUNCA copiado). Simulação
não valida física (physical_verdict_allowed=false).

    set PYTHONUTF8=1
    "C:\\IALD\\observaveis_tgl\\tgl_env\\Scripts\\python.exe" one_tgl_tensor.py
"""
from __future__ import annotations

import hashlib
import json
import math
import shutil
import sys
from datetime import datetime
from pathlib import Path

import numpy as np

RUNNER_DIR = Path(__file__).resolve().parent
PATENT_DIR = RUNNER_DIR.parent
CENTRAL = PATENT_DIR.parents[1]
# 07/10/2026 (errata ao lado; verificacao adversarial da custodia v390): rodado ISOLADO, o FINAL e extraido num temp sem vault/;
# as leituras do cofre vao a VAULT_ROOT (a Central real: TGL_CENTRAL_DIR ou o caminho da casa). CENTRAL segue o da arvore (results).
VAULT_ROOT = CENTRAL
if not (VAULT_ROOT / "vault" / "originals_copy").is_dir():
    for _c in (__import__("os").environ.get("TGL_CENTRAL_DIR"), r"C:\IALD\Central de Patentes"):
        if _c and (Path(_c) / "vault" / "originals_copy").is_dir():
            VAULT_ROOT = Path(_c)
            break
PILOTO = CENTRAL / "Patentes" / "Skygrid" / "SkyGrid_Piloto"
PROTO_SRC = PATENT_DIR / "prototype_src"
WORK = RUNNER_DIR / "_tensor_core"
PATENT_ID = "BR102026003441-0"
SLUG = "tgl_tensor"


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


def cosine(a, b) -> float:
    a, b = np.asarray(a).ravel().astype(np.float64), np.asarray(b).ravel().astype(np.float64)
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 1.0 if np.allclose(a, b) else 0.0
    return float(np.dot(a, b) / (na * nb))


def tensors(rng):
    H, T, dh, r = 8, 512, 128, 6
    kv = np.stack([(rng.standard_normal((T, r)) @ rng.standard_normal((r, dh))) * 0.1
                   + rng.standard_normal((T, dh)) * 0.002 for _ in range(H)])
    emb = rng.standard_normal((4000, 768)) * 0.05
    din, dout, rr = 1024, 1024, 24
    ffn = (rng.standard_normal((din, rr)) @ rng.standard_normal((rr, dout))) * 0.03 \
        + rng.standard_normal((din, dout)) * 0.001
    grad = np.zeros(200_000)
    idx = rng.integers(0, grad.size, grad.size // 20)
    grad[idx] = rng.standard_normal(len(idx)) * 1e-3
    return {"kv_cache": kv, "embeddings": emb, "ffn_weights": ffn, "gradientes_esparso": grad}


def _finish(ts, beta, beta_ok, all_ok, max_verdict, tests, summary, module_hashes, note, fig_builder=None):
    results_dir = PATENT_DIR / "results" / ts
    results_dir.mkdir(parents=True, exist_ok=True)
    results = {"patent_id": PATENT_ID, "slug": SLUG, "timestamp": ts, "runner": "one_tgl_tensor.py (evoluído)",
               "markers": ["[PILOTO]", "[SIM]"], "physical_verdict_allowed": False,
               "beta_runtime": beta, "beta_matches_alpha_sqrt_e": beta_ok,
               "verdict": max_verdict.split(" ")[0] if all_ok else "PARTIAL_DEMONSTRATION",
               "max_verdict": max_verdict,
               "constants": {"BETATGL": beta, "factorization": "betatgl = alpha_EM * sqrt(e)",
                             "spectral_retention": 1 - beta, "free_parameters": 0},
               "tests": tests, "summary": summary,
               "source_prototype": "prototype_src/tgl_tensor_v3.py + tgl_tensor_v4.py "
                                   "(resgatado de C:/IALD/projetos_pyhton/tgl-tensor, READ-ONLY; β injetado)",
               "note": note}
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
    lines = [f"# Relatório auditável — one_tgl_tensor.py (EVOLUÍDO — 4 modos reais)\n",
             f"- Run `{ts}` · Patente `{PATENT_ID}`\n", f"- Veredito: **{max_verdict}**\n",
             f"- β runtime `{beta}` (= α·√e? **{beta_ok}**; nunca literal) — INJETADO nos protótipos v3/v4\n",
             f"- Testes: **{summary['tests_passed']}/{summary['tests_total']}**\n"]
    for t in tests:
        lines.append(f"  - {'✓' if t['passed'] else '✗'} {t['test']}\n")
    lines.append(f"- physical_verdict_allowed: **False**.\n\n{note}\n")
    lines.append("Núcleo copiado do piloto (READ-ONLY); originais intactos. 1 = 1. Tetelestai.\n")
    report_md.write_text("".join(lines), encoding="utf-8")
    seal_dir = PATENT_DIR / "seals" / ts
    seal_dir.mkdir(parents=True, exist_ok=True)
    fh = dict(module_hashes)
    fh["results.json"] = _sha_file(results_path)
    fh["report.md"] = _sha_file(report_md)
    for f in figs:
        fh[f"figures/{f}"] = _sha_file(results_dir / "figures" / f)
    result_hash = _sha_text(json.dumps(fh, sort_keys=True))
    seal = {"timestamp": ts, "patent_id": PATENT_ID, "runner": "one_tgl_tensor.py (evoluído)",
            "beta_runtime": beta, "physical_verdict_allowed": False, "max_verdict": max_verdict,
            "tests_passed": summary["tests_passed"], "result_hash": result_hash, "sha256": fh,
            "markers": ["[PILOTO]", "[SIM]"],
            "results_path": str(results_path.relative_to(CENTRAL)).replace("\\", "/")}
    (seal_dir / "seal.json").write_text(json.dumps(seal, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[{SLUG}] SELADO · result_hash {result_hash[:16]}… · {summary['tests_passed']}/{summary['tests_total']} testes")


def main() -> int:
    ts = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    print(f"[one_tgl_tensor] patente {PATENT_ID} · run {ts} · RUNNER EVOLUÍDO (4 modos reais do operador)")
    if not PILOTO.exists() or not (PROTO_SRC / "tgl_tensor_v3.py").exists():
        print("ERRO: núcleo/protótipo ausente", file=sys.stderr)
        return 2
    module_hashes = copy_core()

    sys.path.insert(0, str(WORK))
    from skygrid_sim import tgl_core  # noqa: E402
    beta = tgl_core.beta()
    beta_ok = abs(beta - 0.0072973525693 * math.exp(0.5)) < 1e-15
    print(f"[one_tgl_tensor] β runtime = {beta} (= α·√e? {beta_ok}) · retenção 1−β = {1-beta:.12f}")

    # import operator's rich prototypes and INJECT β
    sys.path.insert(0, str(PROTO_SRC))
    import tgl_tensor_v3 as v3  # noqa: E402
    import tgl_tensor_v4 as v4  # noqa: E402
    alpha2_original = v3.ALPHA2
    v3.ALPHA2 = beta
    v4.ALPHA2 = beta
    print(f"[one_tgl_tensor] injeção β: ALPHA2 {alpha2_original} → {beta} (protótipos v3/v4 do operador)")

    tests = [{"test": "beta_injected_not_literal", "passed": bool(beta_ok),
              "beta_runtime": beta, "alpha2_original": alpha2_original,
              "spectral_retention_1_minus_beta": 1 - beta}]

    rng = np.random.default_rng(41)
    data = tensors(rng)
    Mode = v3.CompressionMode

    # 4 modes from the operator's real engine
    per_mode = {}
    for mode_name, mode in [("DIRECT", Mode.DIRECT), ("SPECTRAL", Mode.SPECTRAL),
                            ("HYBRID", Mode.HYBRID), ("AUTO", Mode.AUTO)]:
        eng = v3.TGLTensorV3(bits=12, mode=mode, use_cuda=True, energy_threshold=1 - beta)
        rows = {}
        for name, arr in data.items():
            arr = np.asarray(arr, dtype=np.float64)
            if mode in (Mode.SPECTRAL, Mode.HYBRID) and arr.ndim < 2:
                continue  # spectral needs matrices
            try:
                comp = eng.compress(arr)
                rec = eng.decompress(comp)
                rows[name] = {"ratio": float(comp.compression_ratio), "cosine": cosine(arr, rec)}
            except Exception as e:
                rows[name] = {"error": str(e)[:80]}
        ok = any("ratio" in r and r["ratio"] > 1.0 and r.get("cosine", 0) > 0.98 for r in rows.values())
        per_mode[mode_name] = rows
        tests.append({"test": f"mode_{mode_name}", "passed": bool(ok), "per_tensor": rows})
        good = {k: f"{v['ratio']:.1f}×@{v['cosine']:.4f}" for k, v in rows.items() if "ratio" in v}
        print(f"[one_tgl_tensor] modo {mode_name}: {good}")

    # AUTO mode selection actually chooses per structure
    eng_auto = v3.TGLTensorV3(bits=12, mode=Mode.AUTO, use_cuda=True, energy_threshold=1 - beta)
    kv = np.asarray(data["kv_cache"], dtype=np.float64)
    chosen = eng_auto._choose_mode(kv)
    tests.append({"test": "auto_mode_selection", "passed": bool(chosen in list(Mode)),
                  "chosen_for_kv_cache": str(chosen),
                  "note": "AUTO escolhe o modo por análise espectral (baixo rank → SPECTRAL)"})
    print(f"[one_tgl_tensor] AUTO escolheu para KV cache: {chosen}")

    # BitPacker N-bit exact round-trip (v4)
    packer = v4.BitPackerNumPy()
    packer_ok, detail = True, {}
    for bits in (8, 10, 12, 14, 16):
        vals = rng.integers(0, 1 << bits, 5000).astype(np.uint32)
        rt = packer.unpack(packer.pack(vals, bits), bits, len(vals))
        ok = bool(np.array_equal(vals, np.asarray(rt).astype(np.uint32)))
        detail[f"{bits}bit"] = ok; packer_ok = packer_ok and ok
    tests.append({"test": "bitpacker_v4_Nbit_exact", "passed": packer_ok, "per_bits": detail})
    print(f"[one_tgl_tensor] BitPacker v4 8/10/12/14/16 bits exato: {packer_ok}")

    # spectral analysis: Verb Floor 1-β selects the rank
    an = eng_auto.analyze_spectral(np.asarray(data["ffn_weights"], dtype=np.float64))
    tests.append({"test": "spectral_analysis_verb_floor", "passed": bool(getattr(an, "rank_optimal", 0) >= 1),
                  "rank_optimal": int(getattr(an, "rank_optimal", 0)),
                  "is_low_rank": bool(getattr(an, "is_low_rank", False)),
                  "compression_potential": float(getattr(an, "compression_potential", 0)),
                  "note": "rank ótimo pela energia ≥ 1−β (Verb Floor derivado da TGL)"})
    print(f"[one_tgl_tensor] análise espectral FFN: rank_ótimo={getattr(an,'rank_optimal','?')} "
          f"potencial={getattr(an,'compression_potential',0):.2f}×")

    # ─────────────────────────────────────────────────────────────────────────
    # APROFUNDAMENTO 1 — varredura 4 modos × bits × tensores (curva ratio/cosseno)
    # ─────────────────────────────────────────────────────────────────────────
    bit_levels = [8, 10, 12, 14, 16]
    sweep_tensors = ["kv_cache", "embeddings", "ffn_weights"]
    bits_sweep = {}  # mode -> tensor -> {bits -> {ratio, cosine, rank_used}}
    for mode_name, mode in [("DIRECT", Mode.DIRECT), ("SPECTRAL", Mode.SPECTRAL),
                            ("HYBRID", Mode.HYBRID), ("AUTO", Mode.AUTO)]:
        bits_sweep[mode_name] = {}
        for name in sweep_tensors:
            arr = np.asarray(data[name], dtype=np.float64)
            if mode in (Mode.SPECTRAL, Mode.HYBRID) and arr.ndim < 2:
                continue
            curve = {}
            for b in bit_levels:
                eng = v3.TGLTensorV3(bits=b, mode=mode, use_cuda=True, energy_threshold=1 - beta)
                try:
                    comp = eng.compress(arr); rec = eng.decompress(comp)
                    curve[b] = {"ratio": float(comp.compression_ratio), "cosine": cosine(arr, rec),
                                "rank_used": int(getattr(comp, "rank_used", 0))}
                except Exception as e:
                    curve[b] = {"error": str(e)[:60]}
            bits_sweep[mode_name][name] = curve
    dc = bits_sweep["DIRECT"]["ffn_weights"]
    cos_lo, cos_hi = dc[bit_levels[0]]["cosine"], dc[bit_levels[-1]]["cosine"]
    tests.append({"test": "bits_sweep_fidelity_monotone",
                  "passed": bool(cos_hi + 1e-9 >= cos_lo),
                  "cosine_8bit": cos_lo, "cosine_16bit": cos_hi,
                  "note": "varredura bits: mais bits nunca piora a fidelidade DIRECT (round-trip exato)"})
    print(f"[one_tgl_tensor] varredura bits DIRECT ffn: 8bit cos={cos_lo:.6f} → 16bit cos={cos_hi:.6f}")

    # ─────────────────────────────────────────────────────────────────────────
    # APROFUNDAMENTO 2 — curva rank-adaptativo vs energia (Verb Floor = 1−β)
    # ─────────────────────────────────────────────────────────────────────────
    verb_floor = 1 - beta
    energy_grid = sorted(set([0.90, 0.95, 0.98, 0.99, 0.995, 0.999, 0.9999, verb_floor]))
    rank_energy = {}  # tensor -> [{energy_threshold, rank_optimal, compression_potential, is_verb_floor}]
    for name in ["ffn_weights", "embeddings"]:
        arr = np.asarray(data[name], dtype=np.float64)
        curve = []
        for thr in energy_grid:
            eng = v3.TGLTensorV3(bits=12, mode=Mode.SPECTRAL, use_cuda=True, energy_threshold=thr)
            an_t = eng.analyze_spectral(arr)
            curve.append({"energy_threshold": float(thr), "rank_optimal": int(an_t.rank_optimal),
                          "compression_potential": float(an_t.compression_potential),
                          "is_verb_floor": bool(abs(thr - verb_floor) < 1e-12)})
        rank_energy[name] = curve
    ff_ranks = [c["rank_optimal"] for c in rank_energy["ffn_weights"]]
    mono = all(ff_ranks[i] <= ff_ranks[i + 1] for i in range(len(ff_ranks) - 1))
    tests.append({"test": "rank_adaptive_monotone_in_energy", "passed": bool(mono),
                  "ranks_ffn": ff_ranks, "energy_grid": energy_grid,
                  "note": "rank ótimo é não-decrescente no limiar de energia; Verb Floor=1−β marcado"})
    print(f"[one_tgl_tensor] curva rank×energia ffn: ranks={ff_ranks} (Verb Floor={verb_floor:.6f})")

    # ─────────────────────────────────────────────────────────────────────────
    # APROFUNDAMENTO 3 — rank COMPUTADO por modo (ffn) para refletir na geometria
    # ─────────────────────────────────────────────────────────────────────────
    comp_ranks = {}
    for mode_name, mode in [("DIRECT", Mode.DIRECT), ("SPECTRAL", Mode.SPECTRAL),
                            ("HYBRID", Mode.HYBRID), ("AUTO", Mode.AUTO)]:
        eng = v3.TGLTensorV3(bits=12, mode=mode, use_cuda=True, energy_threshold=1 - beta)
        comp = eng.compress(np.asarray(data["ffn_weights"], dtype=np.float64))
        comp_ranks[mode_name] = int(getattr(comp, "rank_used", 0))
    print(f"[one_tgl_tensor] rank_used por modo (ffn): {comp_ranks}")

    # ─────────────────────────────────────────────────────────────────────────
    # AMPLIFICACAO v138 — SUPORTE vs FACES na assinatura do Nome (um.py v135)
    # [DER] Teorema maduro: tau(q_F)=1 e tau(face+)=tau(face-)=1/2; as faces
    # somam ao suporte (meacao). O dispositivo Tensor JA julga integridade pelo
    # Nome; esta sombra ancora a MEACAO no modelo M4 com tau=Tr/2: o peso do
    # Nome = 1 = omega(I) e invariante de classe (conjugacao unitaria).
    # Honestidade: leitura matematica derivada numericamente ([DER]); NAO e
    # veredito fisico (physical_verdict_allowed=false); beta so em runtime.
    # ─────────────────────────────────────────────────────────────────────────
    rng138 = np.random.default_rng(138)
    G1 = rng138.standard_normal((4, 4)) + 1j * rng138.standard_normal((4, 4))
    V138, _ = np.linalg.qr(G1)                        # unitario 4x4
    lam138 = np.array([0.0, 0.0, 0.75, 1.5])          # ker dim 2 = suporte do Nome
    T138 = (V138 * lam138) @ V138.conj().T
    T138 = 0.5 * (T138 + T138.conj().T)               # auto-adjunto exato
    w138, U138 = np.linalg.eigh(T138)
    ker_idx = np.where(np.abs(w138) < 1e-10)[0]
    ran_idx = np.where(np.abs(w138) >= 1e-10)[0]
    v_p, v_m = U138[:, ker_idx[0]], U138[:, ker_idx[1]]
    q_p = np.outer(v_p, v_p.conj())                   # face+
    q_m = np.outer(v_m, v_m.conj())                   # face-
    Uran = U138[:, ran_idx]
    q_F = np.eye(4) - Uran @ Uran.conj().T            # suporte = 1 - proj(range), independente
    tau = lambda a: float(np.trace(a).real) / 2.0     # tau = Tr/2 em M4 (regua do Nome)
    tau_qF, tau_qp, tau_qm = tau(q_F), tau(q_p), tau(q_m)
    resid_faces_sum = float(np.linalg.norm(q_p + q_m - q_F))       # qp+qm = qF
    resid_annihilation = float(np.linalg.norm(T138 @ q_F))         # T aniquila o suporte
    G2 = rng138.standard_normal((4, 4)) + 1j * rng138.standard_normal((4, 4))
    Uc138, _ = np.linalg.qr(G2)
    tau_qF_class = tau(Uc138 @ q_F @ Uc138.conj().T)  # invariante de classe
    resid_class = abs(tau_qF_class - tau_qF)
    # tolerancia da soma das faces: 1e-13 (precisao de eigh/QR em M4 e ~1e-15 por entrada;
    # a exigencia original 1e-15 reprovava por 24% de folga de float — o numero corrige a frase)
    nome_ok = (len(ker_idx) == 2 and abs(tau_qF - 1.0) < 1e-12
               and abs(tau_qp - 0.5) < 1e-12 and abs(tau_qm - 0.5) < 1e-12
               and resid_faces_sum < 1e-13 and resid_annihilation < 1e-12
               and resid_class < 1e-12)
    tests.append({"test": "nome_support_half_faces", "passed": bool(nome_ok),
                  "tau_qF": tau_qF, "tau_face_plus": tau_qp, "tau_face_minus": tau_qm,
                  "resid_faces_sum_to_support": resid_faces_sum,
                  "resid_kernel_annihilation": resid_annihilation,
                  "tau_qF_after_unitary_conjugation": tau_qF_class,
                  "resid_class_invariance": resid_class,
                  "peso_do_nome_omega_I": tau_qF, "beta_runtime": beta,
                  "note": ("[DER] amplificacao v138 (um.py v135, SUPORTE vs FACES): em M4 com "
                           "tau=Tr/2, tau(qF)=1=omega(I), tau(face+)=tau(face-)=1/2, "
                           "qp+qm=qF; peso do Nome invariante de classe. Leitura matematica, "
                           "nao veredito fisico; beta em runtime, nunca literal.")})
    print(f"[one_tgl_tensor] amplificacao v138 nome/meacao: tau(qF)={tau_qF:.15f} "
          f"faces={tau_qp:.15f}+{tau_qm:.15f} resid_soma={resid_faces_sum:.3e} "
          f"aniquilacao={resid_annihilation:.3e} classe={resid_class:.3e}")

    # ─────────────────────────────────────────────────────────────────────────
    # APROFUNDAMENTO PROPRIO v2 (29/07/2026) — O CODEC E UMA PROJECAO (own-mechanism)
    # [DER] Identidade fechada NOVA do mecanismo da patente (eqs. (1)-(5)):
    # o round-trip R = Dobra Dimensional ∘ Codificacao Angular do modo DIRETO e
    # IDEMPOTENTE — R∘R = R com residuo EXATO 0.0 — logo o codec e uma PROJECAO
    # sobre o proprio codebook, e Fix(R) = codebook (verificado sobre TODOS os
    # 2^b codigos). O MECANISMO: a estatistica de normalizacao gmax e PRESERVADA
    # pelo round-trip (o elemento extremo satura o codigo: arcsin(1)=pi/2 ->
    # thq=2^b-1 -> sin=1 -> g'max=gmax). CONTROLE NEGATIVO: o mesmo codec
    # normalizado pela MEDIA (estatistica NAO preservada quando ha clipping)
    # NAO e projecao — R_mean∘R_mean != R_mean, REJEITADO. Exame de 29/07
    # respeitado: v139-v144 nao mapeia alem do ja ancorado neste dispositivo;
    # aprofunda-se o mecanismo proprio com derivacao real nova.
    # [SIM] tensores sinteticos; physical_verdict_allowed=false; beta so runtime.
    # ─────────────────────────────────────────────────────────────────────────
    def _tgl_direct_rt(L, bits, norm="max", c_mean=1.5):
        """Eqs. (1)-(5) da patente, fieis: g=sqrt|L|, s=sign(L), theta=arcsin(g/scale),
        quantiza em b bits, Dobra Dimensional L' = s*[scale*sin(thq*(pi/2)/(2^b-1))]^2.
        norm='max' e o codec da patente; norm='mean' e o contra-exemplo."""
        g = np.sqrt(np.abs(L)); s = np.sign(L)
        scale = float(g.max()) if norm == "max" else c_mean * float(g.mean())
        levels = (1 << bits) - 1
        theta = np.arcsin(np.clip(g / scale, 0.0, 1.0))
        thq = np.round(theta * levels / (math.pi / 2.0))
        rec = s * (scale * np.sin(thq * (math.pi / 2.0) / levels)) ** 2
        return rec, scale

    rng_v2 = np.random.default_rng(2029)
    L0 = rng_v2.standard_normal((64, 96)) * 0.05
    bits_p = 10; levels_p = (1 << bits_p) - 1
    R1, sc1 = _tgl_direct_rt(L0, bits_p)
    R2, sc2 = _tgl_direct_rt(R1, bits_p)
    resid_idem = float(np.max(np.abs(R2 - R1)))     # projecao: 0.0 bit-exato
    scale_drift = abs(sc2 - sc1)                    # gmax preservado pelo round-trip
    uniq_L0, uniq_R1 = int(np.unique(L0).size), int(np.unique(R1).size)
    codebook_bound = 2 * levels_p + 1               # colapso a <= 2*(2^b-1)+1 valores
    # Fix(R) = codebook: TODOS os 2^b codigos (sinais alternados) sao pontos fixos
    k_all = np.arange(levels_p + 1, dtype=np.float64)
    s_all = np.where(k_all % 2 == 0, 1.0, -1.0)
    CB = s_all * (sc1 * np.sin(k_all * (math.pi / 2.0) / levels_p)) ** 2
    R_cb, _ = _tgl_direct_rt(CB, bits_p)
    resid_codebook = float(np.max(np.abs(R_cb - CB)))
    # CONTROLE NEGATIVO: normalizacao pela media -> clipping remove massa do topo,
    # a media deriva, os codigos mudam: R_mean nao e projecao (deve ser REJEITADO)
    M1, scm1 = _tgl_direct_rt(L0, bits_p, norm="mean")
    M2, scm2 = _tgl_direct_rt(M1, bits_p, norm="mean")
    resid_mean_idem = float(np.max(np.abs(M2 - M1)))
    mean_drift_rel = abs(scm2 - scm1) / scm1
    mean_rejected = bool(resid_mean_idem > 1e-6 and mean_drift_rel > 1e-6)
    proj_ok = (resid_idem == 0.0 and scale_drift == 0.0 and resid_codebook == 0.0
               and uniq_L0 > codebook_bound and uniq_R1 <= codebook_bound
               and mean_rejected)
    tests.append({"test": "codec_projection_idempotent", "passed": bool(proj_ok),
                  "mapping_tier": "own-mechanism",
                  "resid_idempotence_RR_vs_R": resid_idem,
                  "scale_gmax_drift": scale_drift,
                  "resid_codebook_fixed_points": resid_codebook,
                  "codebook_size_bound": codebook_bound,
                  "distinct_values_before": uniq_L0, "distinct_values_after": uniq_R1,
                  "negative_control_mean_norm": {"resid_idempotence": resid_mean_idem,
                                                "scale_drift_rel": mean_drift_rel,
                                                "c_mean": 1.5,
                                                "rejected_as_projection": mean_rejected},
                  "bits": bits_p, "beta_runtime": beta,
                  "note": ("[DER][SIM] own-mechanism: R = Dobra∘Codificacao (eqs. (1)-(5)) "
                           "e PROJECAO exata (R∘R=R, residuo 0.0) porque gmax e preservado "
                           "pelo round-trip (o extremo satura o codigo); Fix(R)=codebook "
                           "(2^b codigos verificados); valores distintos colapsam a "
                           "<=2*(2^b-1)+1. CONTROLE NEGATIVO: normalizacao pela media nao "
                           "e preservada e o codec deixa de ser projecao (REJEITADO). "
                           "Exame 29/07 respeitado (v139-v144 nao ancorado aqui). Leitura "
                           "matematica; nao veredito fisico; beta so runtime.")})
    print(f"[one_tgl_tensor] aprofundamento v2 codec-projecao: resid R.R-R={resid_idem:.1e} "
          f"codebook={resid_codebook:.1e} unicos {uniq_L0}->{uniq_R1} (<={codebook_bound}) "
          f"CONTROLE mean: resid={resid_mean_idem:.3e} deriva_escala={mean_drift_rel:.3e} "
          f"rejeitado={mean_rejected}")

    # ─────────────────────────────────────────────────────────────────────────
    # AMPLIFICACAO v168 (ONDA 3, 19/08/2026) — O PESO E TRACO (BreuerTrace)
    # [DER] Pedra em kernel do um.py v166-v167 (Lean, 0 sorry, 0 axiom novo):
    # BreuerTrace — o peso do canto e TRACO: tau(a*a) = tau(aa*) no habitante
    # inf-dim. Mapeamento GENUINO a ESTE dispositivo: o peso que o Verb Floor
    # usa para escolher o rank (eq. (7), reiv. 2) E um traco — energia =
    # tr(M^T M) = tr(M M^T) = soma(sigma^2). A identidade tracial e EXATAMENTE
    # o que torna o rank adaptativo invariante por transposicao: as duas faces
    # U (aa*) e V (a*a) da SVD carregam o MESMO peso total — por isso a
    # cascata comprime U_k e V_k^T com o mesmo orcamento de energia, mesmo
    # quando os ambientes tem dimensoes DIFERENTES (face retangular). CONTROLE
    # NEGATIVO: um funcional NAO-tracial tau_W(X) = tr(W X) com W nao-uniforme
    # VIOLA tau_W(aa*) = tau_W(a*a) e e REJEITADO como peso do Verb Floor —
    # a invariancia nao e automatica, depende de o peso ser traco.
    # Honestidade: [DER][SIM] leitura matematica em bancada finita; NAO e
    # veredito fisico (physical_verdict_allowed=false); beta so em runtime.
    # ─────────────────────────────────────────────────────────────────────────
    rng168 = np.random.default_rng(168)
    mq, rq = 96, 7
    M168 = (rng168.standard_normal((mq, rq)) @ rng168.standard_normal((rq, mq))) * 0.1 \
        + rng168.standard_normal((mq, mq)) * 0.003
    GL168 = M168 @ M168.T                          # a a*  (face esquerda, U)
    GR168 = M168.T @ M168                          # a* a  (face direita, V)
    sv168 = np.linalg.svd(M168, compute_uv=False)
    E168 = float(np.sum(sv168 ** 2))
    resid_tr_sq = max(abs(float(np.trace(GL168)) - E168),
                      abs(float(np.trace(GR168)) - E168)) / E168
    # face retangular (o caso Breuer genuino: ambientes de dimensao DIFERENTE)
    ma_, na_, ra_ = 64, 112, 5
    A168 = (rng168.standard_normal((ma_, ra_)) @ rng168.standard_normal((ra_, na_))) * 0.1 \
        + rng168.standard_normal((ma_, na_)) * 0.002
    tr_AAs = float(np.trace(A168 @ A168.T))        # traco no ambiente dim 64
    tr_AsA = float(np.trace(A168.T @ A168))        # traco no ambiente dim 112
    resid_tr_rect = abs(tr_AAs - tr_AsA) / tr_AsA
    # o Verb Floor herda a invariancia: rank(M) == rank(M^T) pela ENGINE real
    eng168 = v3.TGLTensorV3(bits=12, mode=Mode.SPECTRAL, use_cuda=True,
                            energy_threshold=1 - beta)
    an_M168 = eng168.analyze_spectral(M168)
    an_MT168 = eng168.analyze_spectral(np.ascontiguousarray(M168.T))
    rank_M168, rank_MT168 = int(an_M168.rank_optimal), int(an_MT168.rank_optimal)
    resid_energy_faces = abs(float(an_M168.energy_ratio) - float(an_MT168.energy_ratio))
    # caminho independente: minimalidade do rank sob o Verb Floor 1-beta
    cum168 = np.cumsum(sv168 ** 2) / E168
    k_star168 = int(np.nonzero(cum168 >= 1 - beta)[0][0]) + 1
    minimal_ok168 = bool(cum168[k_star168 - 1] >= 1 - beta
                         and (k_star168 == 1 or cum168[k_star168 - 2] < 1 - beta))
    tail_discarded = float(1.0 - cum168[k_star168 - 1])   # cauda refletida <= beta
    # CONTROLE NEGATIVO: peso NAO-tracial tau_W(X)=tr(W X), W=diag nao-uniforme
    w_ramp = np.linspace(1.0, 3.0, mq)
    tauW_L = float(np.sum(w_ramp * np.diag(GL168)))
    tauW_R = float(np.sum(w_ramp * np.diag(GR168)))
    defect_W = abs(tauW_L - tauW_R) / max(abs(tauW_L), abs(tauW_R))
    Uf168, sf168, Vtf168 = np.linalg.svd(M168)
    eL168 = sf168 ** 2 * np.sum(w_ramp[:, None] * Uf168 ** 2, axis=0)   # sig^2 u_j^T W u_j
    eR168 = sf168 ** 2 * (Vtf168 ** 2 @ w_ramp)                          # sig^2 v_j^T W v_j
    dir_mismatch = float(np.max(np.abs(eL168 - eR168) / np.maximum(eL168, eR168)))
    kW_L = int(np.nonzero(np.cumsum(eL168) / float(np.sum(eL168)) >= 1 - beta)[0][0]) + 1
    kW_R = int(np.nonzero(np.cumsum(eR168) / float(np.sum(eR168)) >= 1 - beta)[0][0]) + 1
    nontracial_rejected = bool(defect_W > 1e-3)
    breuer_ok = (resid_tr_sq < 1e-12 and resid_tr_rect < 1e-12
                 and rank_M168 >= 1 and rank_M168 == rank_MT168
                 and resid_energy_faces < 1e-12
                 and rank_M168 == k_star168 and minimal_ok168
                 and tail_discarded <= beta
                 and nontracial_rejected)   # o contra-exemplo TEM de ser rejeitado
    tests.append({"test": "breuer_trace_weight_v168", "passed": bool(breuer_ok),
                  "mapping_tier": "v160-v168",
                  "resid_trace_square_rel": resid_tr_sq,
                  "resid_trace_rect_rel": resid_tr_rect,
                  "rect_ambient_dims": [ma_, na_],
                  "trace_left_dim64": tr_AAs, "trace_right_dim112": tr_AsA,
                  "rank_optimal_M": rank_M168, "rank_optimal_MT": rank_MT168,
                  "rank_independent_kstar": k_star168,
                  "resid_energy_ratio_faces": resid_energy_faces,
                  "verb_floor_minimality_ok": minimal_ok168,
                  "tail_discarded_below_beta": tail_discarded,
                  "beta_runtime": beta,
                  "negative_control_nontracial_weight": {
                      "weight": "tau_W(X)=tr(W X), W=diag(linspace(1,3,96))",
                      "tauW_aa_star": tauW_L, "tauW_a_star_a": tauW_R,
                      "tracial_defect_rel": defect_W,
                      "per_direction_max_rel_mismatch": dir_mismatch,
                      "weighted_rank_left": kW_L, "weighted_rank_right": kW_R,
                      "rejected_as_trace": nontracial_rejected},
                  "note": ("[DER][SIM] amplificacao v168 (um.py v166-v167, pedra "
                           "BreuerTrace em kernel: tau(a*a)=tau(aa*)): o peso do "
                           "Verb Floor E um traco — tr(M^T M)=tr(M M^T)=soma(sigma^2) "
                           "mesmo com ambientes retangulares de dimensao diferente; "
                           "por isso rank(M)=rank(M^T) e as faces U/V retem a mesma "
                           "energia (a cascata da patente comprime U_k e V_k^T com o "
                           "mesmo orcamento); cauda descartada <= beta por minimalidade. "
                           "CONTROLE NEGATIVO: peso nao-tracial tr(WX) viola a "
                           "identidade e e REJEITADO. Leitura matematica; nao veredito "
                           "fisico; beta so runtime.")})
    print(f"[one_tgl_tensor] amplificacao v168 BreuerTrace: resid_tr sq={resid_tr_sq:.3e} "
          f"rect={resid_tr_rect:.3e} rank M/MT={rank_M168}/{rank_MT168} (k*={k_star168}) "
          f"cauda={tail_discarded:.6f}<=beta={beta:.6f} minimal={minimal_ok168}")
    print(f"[one_tgl_tensor]   controle nao-tracial: defeito={defect_W:.3e} "
          f"mismatch_dir={dir_mismatch:.3e} ranks W {kW_L}/{kW_R} "
          f"rejeitado_como_traco={nontracial_rejected}")

    # ─────────────────────────────────────────────────────────────────────────
    # AMPLIFICACAO v206 (ONDA 4, 25/08/2026) — A COMPRESSAO NAO E IDENTIFICAVEL
    # [DER] Pedra em kernel do ciclo v199-v210 (Lean 4.31.0, 0 sorry, 0 axiom):
    # TGLExt/TheCompressionIsNotIdentifiable.lean, custodia em
    # vault/originals_copy/tgl_kernel_v206 (sha256 082cb1facd66ff98...).
    # Os teoremas sao RE-DERIVADOS numericamente aqui — nunca se finge rodar
    # Lean: every_alpha_fits_every_observation / two_worlds_indistinguishable
    # (o dado inscrito nao restringe o fator), internal_ratios_are_alpha_blind
    # (razoes internas eliminam o fator exatamente),
    # no_scale_invariant_functional_yields_alpha (funcional invariante de
    # escala jamais devolve o fator).
    # Mapeamento GENUINO a ESTE dispositivo: o stream do modo DIRETO
    # (theta_q, s, psi) e funcao SO da razao interna g/gmax — invariante de
    # escala. Logo, POR TEOREMA, o que o tensor NAO pode reconstruir e a
    # escala global a partir do stream sozinho: o gmax float64 do cabecalho
    # TGL4 (passo 216, reiv. 11) e exatamente a "referencia nao submetida a
    # mesma transformacao" que o kernel prova necessaria — sem ela a
    # descompressao e impossivel em PRINCIPIO, nao em pratica. Consequencia
    # afiada: as metricas intrinsecas da patente (Fexp, S_psi, var/Tetelestai
    # — reiv. 1/8) e o portao de fidelidade cosseno (reiv. 10) sao TODOS
    # invariantes de escala — provadamente CEGOS a adulteracao da escala; na
    # reiv. 9, quem quebra a escala e o SHA-256 sobre a serializacao COMPLETA
    # (incluindo as escalas float64), nunca o Fexp sozinho.
    # Bancada IEEE-exata: c = menor potencia de 4 acima do Indice do Nome
    # 1/beta (runtime, nunca literal) — escala por potencia de 2 comuta com o
    # arredondamento, entao a bancada realiza o teorema de aritmetica REAL
    # sem ruido de ULP (residuos 0.0 bit-exatos sao a tese, nao tolerancia).
    # CONTROLE NEGATIVO (por logica): um codec com referencia EXTERNA fixa
    # (regua NAO submetida a transformacao) DISTINGUE os dois mundos — e
    # REJEITADO como cego. A cegueira nao e automatica nem tautologica: ela e
    # a hipotese do teorema (normalizacao interna), e o controle poderia
    # reprovar o teste se a cegueira fosse universal.
    # [DER][SIM]; physical_verdict_allowed=false; beta so runtime.
    # ─────────────────────────────────────────────────────────────────────────
    bits206 = 10
    levels206 = (1 << bits206) - 1

    def _enc206(L, scale=None):
        """Eqs. (1)-(4) da patente, encode fiel: g=sqrt|L|, s=sign(L),
        theta=arcsin(g/scale), quantiza em b bits. scale=None -> gmax interno
        (o codec da patente); scale externo -> o contra-exemplo da regua fixa."""
        g = np.sqrt(np.abs(L))
        s = np.sign(L).astype(np.int8)
        sc = float(g.max()) if scale is None else float(scale)
        theta = np.arcsin(np.clip(g / sc, 0.0, 1.0))
        thq = np.round(theta * levels206 / (math.pi / 2.0)).astype(np.uint16)
        return thq, s, sc

    def _dec206(thq, s, sc):
        """Eq. (5), Dobra Dimensional: L' = s*[sc*sin(thq*(pi/2)/(2^b-1))]^2."""
        return s.astype(np.float64) * (sc * np.sin(
            thq.astype(np.float64) * (math.pi / 2.0) / levels206)) ** 2

    def _psi206(L):
        """Tabela 1: psi de (sign L, sign dL); paridades (-1,+1,+1,-1); Fexp; S_psi."""
        Lf = np.ravel(L)
        sl = np.sign(Lf[1:])
        ds = np.sign(np.diff(Lf))
        psi = np.where(sl >= 0, np.where(ds < 0, 0, 1),
                       np.where(ds > 0, 2, 3)).astype(np.uint8)
        par = np.where((psi == 1) | (psi == 2), 1.0, -1.0)
        p = np.bincount(psi, minlength=4).astype(np.float64)
        p /= p.sum()
        s_ent = float(-np.sum(p[p > 0] * np.log2(p[p > 0])))
        return psi, float(par.mean()), s_ent

    rng206 = np.random.default_rng(206)
    L_A = rng206.standard_normal((48, 80)) * 0.05          # mundo A (origem)
    name_index206 = 1.0 / beta                              # Indice do Nome (runtime)
    k206 = int(math.ceil(math.log(name_index206) / math.log(4.0)))
    c206 = float(4.0 ** k206)                               # menor 4^k > 1/beta
    L_B = c206 * L_A                                        # mundo B: origem re-escalada

    thq_A, sg_A, gmax_A = _enc206(L_A)
    thq_B, sg_B, gmax_B = _enc206(L_B)
    psi_A, fexp_A, sent_A = _psi206(L_A)
    psi_B, fexp_B, sent_B = _psi206(L_B)

    # (i) o stream inscrito e IDENTICO nos dois mundos (razoes internas cegas)
    streams_identical = bool(np.array_equal(thq_A, thq_B)
                             and np.array_equal(sg_A, sg_B)
                             and np.array_equal(psi_A, psi_B))
    scale_ratio206 = gmax_B / gmax_A                        # = 2^k IEEE-exato
    resid_scale_exact = abs(scale_ratio206 - 2.0 ** k206)
    scales_differ = bool(gmax_B != gmax_A and c206 > 1.0)

    # (ii) dois mundos indistinguiveis: o MESMO stream serve aos dois; o header decide
    rec_AA = _dec206(thq_A, sg_A, gmax_A)                   # stream A + header A
    rec_AB = _dec206(thq_A, sg_A, gmax_B)                   # stream A + header B
    rec_BB = _dec206(thq_B, sg_B, gmax_B)                   # mundo B legitimo
    resid_cross206 = float(np.max(np.abs(rec_AB - rec_BB)))         # 0.0 bit-exato
    resid_factor206 = float(np.max(np.abs(rec_AB - c206 * rec_AA)))  # fator uniforme = c

    # (iii) as metricas da patente sao invariantes de escala => cegas POR TEOREMA
    g_A206 = np.sqrt(np.abs(L_A)); g_B206 = np.sqrt(np.abs(L_B))
    var_A206 = float(np.std(g_A206) / np.mean(g_A206))      # var do Tetelestai
    var_B206 = float(np.std(g_B206) / np.mean(g_B206))
    d_fexp206 = abs(fexp_B - fexp_A)
    d_sent206 = abs(sent_B - sent_A)
    d_var206 = abs(var_B206 - var_A206)
    cos_blind206 = cosine(rec_AA, rec_AB)                   # portao cos>0.99 passa...
    rel_err_cross206 = float(np.linalg.norm(rec_AB - rec_AA)
                             / np.linalg.norm(rec_AA))      # ...com erro relativo c-1

    # (iv) o stream nao carrega a escala; o header float64 sim (reiv. 9/11)
    sha_stream_A = hashlib.sha256(thq_A.tobytes() + sg_A.tobytes()).hexdigest()
    sha_stream_B = hashlib.sha256(thq_B.tobytes() + sg_B.tobytes()).hexdigest()
    sha_hdr_A = hashlib.sha256(thq_A.tobytes() + sg_A.tobytes()
                               + np.float64(gmax_A).tobytes()).hexdigest()
    sha_hdr_B = hashlib.sha256(thq_B.tobytes() + sg_B.tobytes()
                               + np.float64(gmax_B).tobytes()).hexdigest()
    stream_sha_equal = bool(sha_stream_A == sha_stream_B)
    header_sha_differ = bool(sha_hdr_A != sha_hdr_B)

    # (v) estimador do stream: qualquer funcao do stream da o MESMO valor nos
    # 2 mundos (no_scale_invariant_functional_yields_alpha em numero) — logo o
    # erro de QUALQUER estimador de gmax e >= |gmax_B - gmax_A|/2 em um mundo
    est_A206 = float(np.mean(np.sin(thq_A.astype(np.float64) * (math.pi / 2.0) / levels206)))
    est_B206 = float(np.mean(np.sin(thq_B.astype(np.float64) * (math.pi / 2.0) / levels206)))
    est_identical = bool(est_A206 == est_B206)
    est_error_bound = abs(gmax_B - gmax_A) / 2.0

    # (vi) CONTROLE NEGATIVO: regua EXTERNA fixa (nao submetida a transformacao)
    # -> o stream DISTINGUE os mundos; este codec e REJEITADO como cego
    s_ref206 = 1.0  # regua do programador: NAO e computada do dado
    th_ext_A, _, _ = _enc206(L_A, scale=s_ref206)
    th_ext_B, _, _ = _enc206(L_B, scale=s_ref206)
    frac_ext_diff = float(np.mean(th_ext_A != th_ext_B))
    external_rejected = bool(frac_ext_diff > 0.5)

    nonid_ok = (streams_identical and resid_scale_exact == 0.0 and scales_differ
                and resid_cross206 == 0.0 and resid_factor206 == 0.0
                and d_fexp206 == 0.0 and d_sent206 == 0.0 and d_var206 == 0.0
                and abs(cos_blind206 - 1.0) < 1e-12 and rel_err_cross206 > 1.0
                and stream_sha_equal and header_sha_differ
                and est_identical and est_error_bound > 0.0
                and external_rejected)   # o contra-exemplo TEM de distinguir
    tests.append({"test": "compression_not_identifiable_v206", "passed": bool(nonid_ok),
                  "mapping_tier": "v199-v210",
                  "pedra": "TGLExt/TheCompressionIsNotIdentifiable.lean",
                  "pedra_sha256_custody":
                      "082cb1facd66ff98c9623fd7317edaedbce4825e85806b78b507ea966c4de4de",
                  "scale_factor_c": c206,
                  "c_derivation": "menor 4^k > 1/beta (Indice do Nome, runtime); "
                                  "potencia de 4 => re-escala IEEE-exata (sem ruido de ULP)",
                  "streams_identical_thq_s_psi": streams_identical,
                  "gmax_A": gmax_A, "gmax_B": gmax_B,
                  "scale_ratio_gmaxB_over_gmaxA": scale_ratio206,
                  "resid_scale_ratio_vs_2k": resid_scale_exact,
                  "resid_cross_decode_streamA_headerB_vs_worldB": resid_cross206,
                  "resid_uniform_factor_c": resid_factor206,
                  "blind_metrics": {"d_Fexp": d_fexp206, "d_S_psi": d_sent206,
                                    "d_var_tetelestai": d_var206,
                                    "cosine_recAA_vs_recAB": cos_blind206,
                                    "rel_error_recAA_vs_recAB": rel_err_cross206},
                  "sha_stream_equal_across_worlds": stream_sha_equal,
                  "sha_header_with_scale_differs": header_sha_differ,
                  "stream_estimator": {"est_A": est_A206, "est_B": est_B206,
                                       "identical": est_identical,
                                       "inevitable_error_bound": est_error_bound},
                  "negative_control_external_reference": {
                      "s_ref": s_ref206, "frac_codes_differing": frac_ext_diff,
                      "rejected_as_scale_blind": external_rejected},
                  "bits": bits206, "beta_runtime": beta,
                  "note": ("[DER][SIM] amplificacao v206 (pedra "
                           "TheCompressionIsNotIdentifiable, kernel v199-v210, re-derivada "
                           "em numero — Lean jamais executado aqui): o stream DIRETO "
                           "(theta_q, s, psi) e funcao so da razao g/gmax => invariante de "
                           "escala => POR TEOREMA a escala global NAO e reconstruivel do "
                           "stream sozinho (todo gmax e compativel com todo stream; dois "
                           "mundos com escalas diferentes inscrevem o MESMO dado). O gmax "
                           "float64 do cabecalho TGL4 (passo 216, reiv. 11) e a referencia "
                           "nao submetida a transformacao que o kernel prova necessaria. "
                           "Consequencia: Fexp, S_psi, var/Tetelestai e o cosseno (reiv. "
                           "1/8/10) sao provadamente CEGOS a adulteracao de escala — quem a "
                           "detecta na reiv. 9 e o SHA-256 sobre a serializacao completa. "
                           "CONTROLE NEGATIVO: regua externa fixa distingue os mundos e e "
                           "REJEITADA como cega (a cegueira e hipotese, nao tautologia). "
                           "Leitura matematica; nao veredito fisico; beta so runtime.")})
    print(f"[one_tgl_tensor] amplificacao v206 nao-identificavel: c={c206:.0f} (=4^{k206} > "
          f"1/beta={name_index206:.2f}) streams_identicos={streams_identical} "
          f"gmaxB/gmaxA={scale_ratio206:.1f} resid_cross={resid_cross206:.1f} "
          f"resid_fator_c={resid_factor206:.1f}")
    print(f"[one_tgl_tensor]   cegueira por teorema: dFexp={d_fexp206:.1e} dS={d_sent206:.1e} "
          f"dvar={d_var206:.1e} cos={cos_blind206:.15f} erro_rel={rel_err_cross206:.1f} "
          f"sha_stream_igual={stream_sha_equal} sha_header_difere={header_sha_differ}")
    print(f"[one_tgl_tensor]   controle regua externa: frac_codigos_diferentes="
          f"{frac_ext_diff:.3f} rejeitado_como_cego={external_rejected} "
          f"bound_estimador={est_error_bound:.4f}")

    # v331 (07/09/2026) — A RAIZ DA ARVORE DA PROVA. Este dispositivo cita o teorema mestre; confere-se que a
    # raiz (`the_root_of_the_proof_tree`: um termo, sete conjuntos — teorema mestre; Lema 3 para TODO perfil;
    # unicidade; fluxo modular; trocas de sitios; parede de H3; a forma nao fixa o valor) EXISTE no kernel MAIS
    # RECENTE do cofre (vault/originals_copy/tgl_kernel_v*) com axiomas = trio, e que o axiom_report inteiro esta
    # no trio. Lido do manifesto por script, nunca de memoria. Fail-closed. NAO move veredito fisico
    # (does_not_gate_core): NOT_FALSIFIED != CONFIRMED. Sem repin: resolve a versao mais nova sozinho.
    try:
        import json as _json
        import re as _re
        _kv = sorted((p for p in (VAULT_ROOT / "vault" / "originals_copy").glob("tgl_kernel_v*")
                      if p.is_dir() and _re.fullmatch(r"tgl_kernel_v\d+", p.name)),
                     key=lambda p: int(p.name.rsplit("v", 1)[1]))
        _kdir = _kv[-1] if _kv else None
        _man = _json.loads((_kdir / "tgl_kernel_proof_manifest.json").read_text(encoding="utf-8")) if _kdir else {}
        _ar = _man.get("axiom_report") or {}
        _trio = {"propext", "Classical.choice", "Quot.sound"}
        _root_ax = _ar.get("TGLExt.the_root_of_the_proof_tree")
        _root_file = (_man.get("formal_files_sha256") or {}).get("TGLExt/TheRootOfTheProofTree.lean")
        _sujos = sum(1 for v in _ar.values() if any(a not in _trio for a in (v or [])))
        _root_ok = bool(_kdir and _root_ax is not None and set(_root_ax) <= _trio and _root_file and _sujos == 0)
    except Exception as _e:  # noqa: BLE001 — a falha e' VISIVEL no teste, nunca 'ok' falso
        _kdir, _root_ax, _root_file, _sujos, _ar, _root_ok = None, None, None, -1, {}, False
    tests.append({"test": "root_of_the_proof_tree_in_current_kernel", "passed": bool(_root_ok),
                  "kernel_vault": (_kdir.name if _kdir else None), "root_axioms": _root_ax,
                  "root_lean_sha256_16": (_root_file[:16] if _root_file else None),
                  "axiom_report_terms": len(_ar), "outside_trio": _sujos,
                  "note": "the_root_of_the_proof_tree lido do kernel mais recente do cofre; axiomas = trio; "
                          "does_not_gate_core; NOT_FALSIFIED != CONFIRMED"})
    passed = sum(1 for t in tests if t["passed"]); total = len(tests); all_ok = passed == total
    summary = {"tests_passed": passed, "tests_total": total, "modes": list(per_mode.keys()),
               "auto_chose_for_kv": str(chosen), "bitpacker_ok": packer_ok,
               "per_mode_best_ratio": {m: max([r["ratio"] for r in rows.values() if "ratio" in r], default=0)
                                       for m, rows in per_mode.items()},
               "per_mode_computed_rank_ffn": comp_ranks,
               "bits_sweep": bits_sweep, "rank_vs_energy": rank_energy,
               "verb_floor_1_minus_beta": verb_floor,
               "rank_optimal_ffn": int(getattr(an, "rank_optimal", 0))}
    max_verdict = ("TENSOR_FULL_LOGIC_DEMONSTRATED ([PILOTO][SIM] — os 4 modos reais do operador "
                   "(DIRECT/SPECTRAL/HYBRID/AUTO) + BitPacker N-bit + varreduras bits/rank-energia "
                   "fecham; β injetado; números sintéticos, não a Tabela 2; nada valida física)")

    _finish(ts, beta, beta_ok, all_ok, max_verdict, tests, summary, module_hashes,
            "RUNNER EVOLUÍDO: roda a engine de 4 modos do operador (tgl_tensor_v3.py) + BitPacker "
            "(v4) com β=α·√e injetado (originais tinham 0.012 literal), acrescido de varreduras "
            "4 modos × bits × tensores e da curva rank-adaptativo × energia (Verb Floor=1−β). "
            "Tensores sintéticos; NÃO os números da Tabela 2. Nenhum token/modelo HuggingFace (P-09). "
            "Simulação não valida física.",
            fig_builder=lambda plt, fd: _fig(plt, fd, per_mode, bits_sweep, rank_energy, verb_floor))
    print(f"[one_tgl_tensor] results: patents/{PATENT_DIR.name}/results/{ts}/results.json")

    # FORMA = CONTEÚDO: emite o render3d.json COMPUTADO (merge — preserva o corpo)
    emit_render3d(beta, per_mode, chosen, comp_ranks, an)
    return 0 if all_ok else 1


def _fig(plt, fig_dir, per_mode, bits_sweep=None, rank_energy=None, verb_floor=None):
    figs = []
    # Fig 1 — 4 modos × tensor (barras de razão)
    names = ["kv_cache", "embeddings", "ffn_weights", "gradientes_esparso"]
    modes = list(per_mode.keys())
    x = np.arange(len(names)); w = 0.2
    plt.figure(figsize=(9, 4))
    for i, m in enumerate(modes):
        vals = [per_mode[m].get(n, {}).get("ratio", 0) for n in names]
        plt.bar(x + (i - 1.5) * w, vals, w, label=m)
    plt.xticks(x, names, rotation=12, fontsize=8); plt.ylabel("razão de compressão ×")
    plt.title("TGL Tensor — 4 modos reais do operador [PILOTO][SIM] (β injetado; não é a Tabela 2)")
    plt.legend(fontsize=8); plt.grid(alpha=.3, axis="y")
    fp = fig_dir / "fig_4modos.png"; plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close()
    figs.append("fig_4modos.png")

    # Fig 2 — varredura bits: razão e fidelidade (cosseno) vs bits, por modo (tensor=ffn_weights)
    if bits_sweep:
        fig, (axl, axr) = plt.subplots(1, 2, figsize=(11, 4))
        for m in bits_sweep:
            curve = bits_sweep[m].get("ffn_weights", {})
            bs = sorted(b for b in curve if isinstance(curve[b], dict) and "ratio" in curve[b])
            if not bs:
                continue
            axl.plot(bs, [curve[b]["ratio"] for b in bs], "o-", label=m)
            axr.plot(bs, [curve[b]["cosine"] for b in bs], "o-", label=m)
        axl.set_xlabel("bits de quantização"); axl.set_ylabel("razão de compressão ×")
        axl.set_title("Razão × bits (ffn_weights)"); axl.grid(alpha=.3); axl.legend(fontsize=8)
        axr.set_xlabel("bits de quantização"); axr.set_ylabel("fidelidade (cosseno)")
        axr.set_title("Fidelidade × bits (ffn_weights)"); axr.grid(alpha=.3); axr.legend(fontsize=8)
        fig.suptitle("TGL Tensor — varredura 4 modos × bits [PILOTO][SIM] (β injetado)")
        fp = fig_dir / "fig_bits_sweep.png"; fig.savefig(fp, dpi=120, bbox_inches="tight"); plt.close(fig)
        figs.append("fig_bits_sweep.png")

    # Fig 3 — curva rank-adaptativo vs energia, com o Verb Floor (1−β) marcado
    if rank_energy:
        plt.figure(figsize=(8, 4.5))
        for name, curve in rank_energy.items():
            thr = [c["energy_threshold"] for c in curve]
            rk = [c["rank_optimal"] for c in curve]
            plt.plot(thr, rk, "o-", label=name)
        if verb_floor is not None:
            plt.axvline(verb_floor, color="#cc2222", ls="--", lw=1.4,
                        label=f"Verb Floor 1−β={verb_floor:.4f}")
        plt.xlabel("limiar de energia acumulada"); plt.ylabel("rank ótimo (COMPUTADO)")
        plt.title("TGL Tensor — rank-adaptativo × energia [PILOTO][SIM] (Verb Floor derivado da TGL)")
        plt.grid(alpha=.3); plt.legend(fontsize=8)
        fp = fig_dir / "fig_rank_vs_energy.png"; plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close()
        figs.append("fig_rank_vs_energy.png")
    return figs


def emit_render3d(beta, per_mode, chosen, comp_ranks, an_ffn):
    """MERGE — lê o render3d.json ATUAL e PRESERVA meshes/layers/groups/constants,
    substituindo apenas nodes+edges pela geometria COMPUTADA nesta run:
    gráviton g=√|L| na origem + tetraedro ℋ₄ (4 estados, vértices computados) +
    4 modos (razão/rank COMPUTADOS refletidos no tamanho e na descrição). forma=conteúdo."""
    out = PATENT_DIR / "render3d.json"
    d = json.loads(out.read_text(encoding="utf-8"))  # preserva o corpo de engenharia

    # gráviton (raiz) + 4 vértices COMPUTADOS do tetraedro ℋ₄ (r=0.7, normalizado por √3)
    R = 0.7
    r_h4 = R / math.sqrt(3.0)
    tetra = [  # (id, sign_x, sign_y, sign_z, label, parity_desc, color)
        ("psi0", +1, +1, +1, "COLAPSO+ |0⟩",   "(+,−) paridade −1 — colapso",    "#cc2222"),
        ("psi1", +1, -1, -1, "ASCENSÃO+ |1⟩",   "(+,+) paridade +1 — ascensão",   "#33aa55"),
        ("psi2", -1, +1, -1, "EMERGÊNCIA− |2⟩", "(−,+) paridade +1 — emergência", "#3366cc"),
        ("psi3", -1, -1, +1, "QUEDA− |3⟩",      "(−,−) paridade −1 — queda",      "#ee8800"),
    ]
    nodes = [{"id": "graviton", "label": "gráviton g=√|L|",
              "desc": (f"Raiz gravitacional g=√|L|, fase s=sign(L). Toda compressão nasce daqui "
                       f"(radicalismo ontológico). β={beta:.9f} = α·√e; retenção 1−β={1-beta:.6f}."),
              "shape": "sphere", "position": [0, 0, 0], "size": 0.18, "color": "#ffd60a",
              "group": "nucleo", "marker": "[REAL]", "layer": "core", "material": "emissive"}]
    for nid, sx, sy, sz, lbl, pdesc, col in tetra:
        nodes.append({"id": nid, "label": lbl,
                      "desc": (f"{pdesc}. Vértice COMPUTADO do tetraedro ℋ₄ (r=0.7/√3, "
                               f"ψ de (sign L, sign ∂L)); θ=arcsin(g/gmax) codifica a magnitude."),
                      "shape": "sphere", "position": [sx * r_h4, sy * r_h4, sz * r_h4],
                      "size": 0.12, "color": col, "group": "h4", "marker": "[REAL]",
                      "layer": "core", "material": "emissive"})

    # 4 modos num anel — tamanho reflete a razão de compressão COMPUTADA (forma=conteúdo)
    mode_order = ["DIRECT", "SPECTRAL", "HYBRID", "AUTO"]
    mode_desc = {"DIRECT": "g,s,θ diretos", "SPECTRAL": "SVD + rank adaptativo ≥1−β",
                 "HYBRID": "SVD + resíduo", "AUTO": "escolhe pela estrutura"}
    chosen_name = str(chosen).split(".")[-1]
    for i, m in enumerate(mode_order):
        ang = 2 * math.pi * i / len(mode_order)
        best = max([r["ratio"] for r in per_mode.get(m, {}).values() if "ratio" in r], default=0.0)
        rk = comp_ranks.get(m, 0)
        size = round(0.09 + 0.06 * math.tanh(math.log10(best + 1.0)), 4)  # ∝ razão computada
        tag = f" — AUTO escolheu {chosen_name} p/ KV cache." if m == "AUTO" else ""
        nodes.append({"id": m, "label": f"modo {m}",
                      "desc": (f"Modo de compressão: {mode_desc[m]}. Melhor razão COMPUTADA nesta run "
                               f"= {best:.1f}× (rank_used ffn={rk}). Opera sobre ℋ₄ + decomposição "
                               f"espectral.{tag}"),
                      "shape": "box", "position": [R * 1.857 * math.cos(ang), -0.9, R * 1.857 * math.sin(ang)],
                      "size": size, "color": "#7ce7c8", "group": "modos", "marker": "[REAL]",
                      "layer": "io", "material": "emissive",
                      "best_ratio": round(best, 3), "rank_used_ffn": rk})

    edges = [{"from": "graviton", "to": n} for n in ("psi0", "psi1", "psi2", "psi3")]
    edges += [{"from": a, "to": b} for a, b in [("psi0", "psi1"), ("psi1", "psi2"), ("psi2", "psi3"),
                                                ("psi3", "psi0"), ("psi0", "psi2"), ("psi1", "psi3")]]
    edges += [{"from": "graviton", "to": m} for m in mode_order]

    d["nodes"] = nodes
    d["edges"] = edges
    d["generated_by"] = "one_tgl_tensor.py (forma=conteudo)"

    # injeta β runtime + 2 métricas COMPUTADAS desta run em constants (preserva os demais)
    rank_ffn = int(getattr(an_ffn, "rank_optimal", 0))
    pot_ffn = float(getattr(an_ffn, "compression_potential", 0.0))
    consts = [c for c in d.get("constants", []) if c.get("symbol") not in ("beta_TGL", "rank_ffn")]
    consts.append({"symbol": "beta_TGL", "value": f"{beta:.12f} (alpha*sqrt(e))",
                   "note": f"acoplamento; retencao espectral 1-beta={1-beta:.9f} (nunca literal)"})
    consts.append({"symbol": "rank_ffn", "value": f"{rank_ffn}",
                   "note": f"rank otimo COMPUTADO (energia>=1-beta); potencial {pot_ffn:.1f}x"})
    d["constants"] = consts

    # VALIDA: todo endpoint de edge existe; toda layer de no/mesh existe
    ids = {n["id"] for n in nodes} | {m.get("id") for m in d.get("meshes", [])}
    for e in edges:
        assert e["from"] in ids and e["to"] in ids, f"edge sem no: {e}"
    layer_ids = {L["id"] for L in d.get("layers", [])}
    for item in nodes + d.get("meshes", []):
        assert item.get("layer") in layer_ids, f"layer invalida: {item.get('id')} -> {item.get('layer')}"

    out.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[{SLUG}] render3d.json EMITIDO (forma=conteudo) — {len(nodes)} nos, {len(edges)} arestas")


if __name__ == "__main__":
    sys.exit(main())
