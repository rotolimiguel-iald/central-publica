# -*- coding: utf-8 -*-
"""one_acom_mirror.py — runner único forma = conteúdo da patente ACOM Mirror (EVOLUÍDO / RICO)
(BR102026003428-2 — Reflexão Dimensional por Codificação Angular em ℋ₄). [PILOTO][SIM]

EVOLUÇÃO (09/07/2026): incorpora a IMPLEMENTAÇÃO DE REFERÊNCIA v17.0 REAL do operador
(`Acom_v17_mirror.py`, 43 KB, torch+zstd), resgatada para `prototype_src/`. A versão leve
anterior (port NumPy `skygrid_sim/acom_mirror.py`) está preservada em
`one_acom_mirror_v1_light.py.bak`. Este runner IMPORTA a engine real e a executa:

  - `DimensionalMirror` / `ACOMv17Mirror` — REFLECT L→(ψ,θ), MANIFEST (ψ,θ)→L' (a DOBRA ×2),
    empacotamento ψ 2 bits + θq, compressão entrópica zstd nível 22 (real);
  - nominação dos 4 estados ψ em ℋ₄ (E4), codificação angular θ=arcsin(g/gmax) (E5),
    quantização angular (E6), métricas intrínsecas Fexp (E7) e Sψ (E8);
  - `ACOMv161` — o comparador v16.1 (quantização LINEAR de g) → a TABELA DE COMPRESSÃO
    v16.1 vs v17.0 (Fig. 6 da patente) regenerada com os dois codecs REAIS do operador.

RÉGUA: β_TGL NUNCA literal no MEU código. O protótipo v17 do operador carrega
`ALPHA2 = 0.012` LITERAL (linha 66); este runner o importa como proveniência READ-ONLY e
INJETA em runtime `ALPHA2 = ALPHA = THETA_MIGUEL(β)` a partir de `tgl_core.beta()` = α·√e.
HONESTIDADE DE ACOPLAMENTO [REAL]: no algoritmo Mirror, α²/β é uma CONSTANTE NOMINAL
(limiar de estabilidade / "imperfeição do espelho", θ_Miguel) — NÃO entra na transformada
de compressão (g=√|L|, θ=arcsin, dobra L'=s·g²). A injeção corrige a PROVENIÊNCIA e os
metadados (metadata['alpha2'], θ_Miguel), não os números de compressão; por isso as razões
não mudam ao trocar 0,012 por α·√e — e isso está dito, não escondido.

HONESTIDADE [PILOTO][SIM]: métricas em tensores SINTÉTICOS; NÃO os números de produção do
relatório (Tabela 2). Nenhum token/modelo HuggingFace (P-09). Simulação nunca valida física
(physical_verdict_allowed=false).

    set PYTHONUTF8=1
    "C:\\IALD\\observaveis_tgl\\tgl_env\\Scripts\\python.exe" one_acom_mirror.py
"""
from __future__ import annotations

import hashlib
import io
import json
import math
import shutil
import sys
from contextlib import redirect_stdout
from datetime import datetime
from pathlib import Path

import numpy as np

RUNNER_DIR = Path(__file__).resolve().parent
PATENT_DIR = RUNNER_DIR.parent
CENTRAL = PATENT_DIR.parents[1]
PILOTO = CENTRAL / "Patentes" / "Skygrid" / "SkyGrid_Piloto"   # READ-ONLY (β source)
PROTO_SRC = PATENT_DIR / "prototype_src"                        # rescued rich prototype
WORK = RUNNER_DIR / "_mirror_core"
PATENT_ID = "BR102026003428-2"
SLUG = "acom_mirror"


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
    """Copy the β-source core (skygrid_sim, for tgl_core) into a workdir and hash it."""
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    dst = WORK / "skygrid_sim"
    shutil.copytree(PILOTO / "skygrid_sim", dst,
                    ignore=shutil.ignore_patterns("__pycache__"))
    hashes = {f"skygrid_sim/{f.name}": _sha_file(f) for f in sorted(dst.glob("*.py"))}
    for f in sorted(PROTO_SRC.glob("*")):
        if f.is_file():
            hashes[f"prototype_src/{f.name}"] = _sha_file(f)
    return hashes


def datasets(rng: np.random.Generator) -> dict:
    """Synthetic tensors mirroring the patent's example families ([041]-[043]) + v17 benchmark."""
    n_sparse = 50_000
    sparse = np.zeros(n_sparse)
    idx = rng.integers(0, n_sparse, n_sparse // 20)                 # ~95% zeros
    sparse[idx] = rng.standard_normal(len(idx))
    t = np.linspace(0, 100 * np.pi, 44_100)
    return {
        "embeddings_768d": rng.standard_normal((1_000, 768)),
        "kv_cache": rng.standard_normal((4, 2, 8, 64, 32)),
        "pesos_nn": rng.standard_normal((1_024, 1_024)) * 0.03,
        "esparso_95": sparse,
        "gradientes": rng.standard_normal(100_000) * 0.01,
        "audio_decay": np.sin(t) * np.exp(-np.linspace(0, 5, 44_100)),
        "financial": 100 * np.cumprod(1 + rng.standard_normal(4_000) * 0.02),
    }


def _corr(a, b) -> float:
    a = np.asarray(a, dtype=np.float64).ravel()
    b = np.asarray(b, dtype=np.float64).ravel()
    n = min(len(a), len(b))
    a, b = a[:n], b[:n]
    if np.std(a) == 0 or np.std(b) == 0:
        return 1.0 if np.allclose(a, b) else 0.0
    c = np.corrcoef(a, b)[0, 1]
    return 0.0 if np.isnan(c) else float(c)


def main() -> int:
    ts = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    print(f"[one_acom_mirror] patente {PATENT_ID} · run {ts} · RUNNER EVOLUÍDO (engine v17.0 real do operador)")
    if not PILOTO.exists():
        print(f"ERRO: núcleo β não encontrado em {PILOTO}", file=sys.stderr)
        return 2
    if not (PROTO_SRC / "Acom_v17_mirror.py").exists():
        print(f"ERRO: protótipo rico não encontrado em {PROTO_SRC}", file=sys.stderr)
        return 2

    module_hashes = copy_core()

    # β from tgl_core (the ONLY source of the coupling in this runner)
    sys.path.insert(0, str(WORK))
    from skygrid_sim import tgl_core  # noqa: E402
    beta = tgl_core.beta()
    beta_expected = 0.0072973525693 * math.exp(0.5)   # alpha (INPUT CODATA) * sqrt(e)
    beta_ok = abs(beta - beta_expected) < 1e-15
    theta_m = tgl_core.theta_m()
    theta_m_deg = math.degrees(theta_m)
    theta_form_ok = abs(theta_m - math.asin(math.sqrt(beta))) < 1e-15
    print(f"[one_acom_mirror] β runtime = {beta} (= α·√e? {beta_ok}) · "
          f"θ_Miguel = {theta_m_deg:.4f}° (= arcsin(√β)? {theta_form_ok})")

    # import torch + the operator's rich v17 prototype (suppress its import banner)
    import torch  # noqa: E402
    torch.manual_seed(42)
    sys.path.insert(0, str(PROTO_SRC))
    with redirect_stdout(io.StringIO()):
        import Acom_v17_mirror as v17  # noqa: E402 (rescued prototype; prints a banner on import)

    # INJECT β (régua: never the 0.012 literal). In Mirror α²/β is a NOMINAL constant
    # (mirror imperfection / θ_Miguel) used only in metadata — patched for provenance.
    alpha2_original = v17.ALPHA2
    v17.ALPHA2 = beta
    v17.ALPHA = math.sqrt(beta)
    v17.THETA_MIGUEL = math.asin(math.sqrt(beta))
    print(f"[one_acom_mirror] injeção β: ALPHA2 {alpha2_original} → {v17.ALPHA2} "
          f"(protótipo v17 do operador; α² é nominal, não entra na transformada)")

    dev = torch.device("cpu")   # deterministic; engine is CPU/GPU-equivalent (reiv. 12)
    rng = np.random.default_rng(17)
    data = datasets(rng)

    tests = []

    # T1 — β injected, not literal
    tests.append({"test": "beta_injected_not_literal",
                  "passed": bool(beta_ok and abs(v17.ALPHA2 - beta) < 1e-18),
                  "beta_runtime": beta, "alpha2_original_prototype": alpha2_original,
                  "note": "runner injeta β=α·√e no protótipo v17 (que tinha 0.012 literal); "
                          "no algoritmo Mirror α² é constante nominal (metadados), não entra "
                          "na transformada de compressão."})

    # T2 — θ_Miguel = arcsin(√β) ≈ 6.29°, patched into the prototype
    tests.append({"test": "theta_miguel_form",
                  "passed": bool(theta_form_ok and abs(v17.THETA_MIGUEL - theta_m) < 1e-15),
                  "theta_miguel_deg": theta_m_deg, "expected_deg_approx": 6.29})

    # T3 — REFLECT/MANIFEST roundtrip with the REAL v17 engine (ACOMv17Mirror, zstd)
    mirror = v17.ACOMv17Mirror(device=dev, angular_bits=8, verbose=False)
    per_ds = {}
    for name, arr in data.items():
        L = torch.tensor(np.asarray(arr, dtype=np.float64), device=dev)
        refl = mirror.reflect(L)
        rec = mirror.manifest(refl)
        corr = _corr(L.cpu().numpy(), rec.cpu().numpy())
        meta = refl.metadata
        entry = {"correlation": corr, "compression_ratio": float(meta["compression_ratio"]),
                 "f_exp": float(meta["f_exp"]), "state_entropy": float(meta["state_entropy"]),
                 "alpha2_in_metadata": float(meta["alpha2"]), "n_elements": int(meta["n_elements"]),
                 "state_counts": {k: int(v) for k, v in meta["state_counts"].items()}}
        per_ds[name] = entry
        tests.append({"test": f"roundtrip_{name}", "passed": bool(corr > 0.999), **entry})
        print(f"[one_acom_mirror] {name}: corr={corr:.6f} ratio={entry['compression_ratio']:.2f} "
              f"Fexp={entry['f_exp']:+.4f} Sψ={entry['state_entropy']:.3f} "
              f"α²_meta={entry['alpha2_in_metadata']:.9f}")

    # T4 — H4 nomination fidelity: patent E4 recomputed by hand == v17 _nominate_state
    Ln = torch.tensor(np.asarray(data["gradientes"], dtype=np.float64)[:20_000], device=dev).float()
    dLn = torch.zeros_like(Ln); dLn[1:] = Ln[1:] - Ln[:-1]; dLn[0] = dLn[1]
    sL = torch.sign(Ln); sL = torch.where(sL == 0, torch.ones_like(sL), sL)
    sdL = torch.sign(dLn); sdL = torch.where(sdL == 0, torch.ones_like(sdL), sdL)
    psi_v17 = mirror.mirror._nominate_state(sL, sdL).cpu().numpy()
    Lnp = Ln.cpu().numpy(); dLnp = dLn.cpu().numpy()
    bit_high = (Lnp < 0).astype(np.uint8)                      # E4: L<0
    bit_low = (dLnp > 0).astype(np.uint8)                      # E4: ∂L>0 (post sign(0)→+1)
    # replicate engine's sign(0)→+1 then >0 test:
    sdL_np = np.sign(dLnp); sdL_np[sdL_np == 0] = 1.0
    bit_low = (sdL_np > 0).astype(np.uint8)
    psi_manual = (bit_high * 2 + bit_low).astype(np.uint8)
    nom_ok = bool(np.array_equal(psi_manual, psi_v17))
    tests.append({"test": "h4_nomination_E4_fidelity", "passed": nom_ok,
                  "note": "ψ=bit_high·2+bit_low (E4) recomputado à mão == v17._nominate_state"})
    print(f"[one_acom_mirror] fidelidade nominação ℋ₄ (E4 manual == engine v17): {nom_ok}")

    # T5 — Fexp sign of sparse (patent example [043] Fexp<0) — honest convention report
    Ls = np.asarray(data["esparso_95"], dtype=np.float64).ravel()
    dLs = np.zeros_like(Ls); dLs[1:] = Ls[1:] - Ls[:-1]; dLs[0] = dLs[1]
    psi_strict = ((Ls < 0).astype(np.uint8) * 2 + (dLs > 0).astype(np.uint8))   # RAW ∂L>0
    parity = np.array([-1.0, 1.0, 1.0, -1.0])
    f_exp_strict = float(parity[psi_strict].mean())
    tests.append({"test": "f_exp_sparse_negative_E4_strict",
                  "passed": bool(f_exp_strict < 0),
                  "f_exp_E4_strict": f_exp_strict,
                  "f_exp_v17_engine": per_ds["esparso_95"]["f_exp"],
                  "honest_note": "E4 estrita (∂L>0 cru): zeros→ψ0 (paridade −1) → Fexp<0, sinal do "
                                 "exemplo [043]. A engine v17 aplica sign(0)→+1 antes da nominação → "
                                 "zeros→ψ1 → Fexp>0. Ambas as leituras constam do texto da patente."})
    print(f"[one_acom_mirror] Fexp esparso: E4-estrita={f_exp_strict:+.4f} (<0, [043]) · "
          f"engine v17 (sign(0)→+1)={per_ds['esparso_95']['f_exp']:+.4f}")

    # T6 — Sψ embeddings regimes: iid gaussian ≈ closed form 1.811; smooth ≈ 2.0 ([041])
    s_psi_iid = per_ds["embeddings_768d"]["state_entropy"]
    s_psi_closed = float(-(2 * (0.375 * math.log2(0.375) + 0.125 * math.log2(0.125))))
    smooth = np.cumsum(rng.standard_normal((1_000, 768)), axis=1)   # random-walk rows
    r_sm = mirror.reflect(torch.tensor(smooth, device=dev))
    s_psi_smooth = float(r_sm.metadata["state_entropy"])
    tests.append({"test": "s_psi_embeddings_regimes",
                  "passed": bool(s_psi_smooth > 1.9 and abs(s_psi_iid - s_psi_closed) < 0.02),
                  "s_psi_iid_gaussian": s_psi_iid, "s_psi_iid_closed_form": s_psi_closed,
                  "s_psi_smooth_embeddings": s_psi_smooth,
                  "note": "iid gaussiano Sψ≈1,811 (ρ(L,∂L)=1/√2, fechado); regime [041] Sψ≈1,998 "
                          "reproduzido com embeddings de estrutura suave."})
    print(f"[one_acom_mirror] Sψ embeddings: iid={s_psi_iid:.4f} (teórico {s_psi_closed:.4f}) · "
          f"suave={s_psi_smooth:.4f} (≈2,0)")

    # T7 — compression TABLE v16.1 vs v17.0 (Fig. 6): BOTH real operator codecs
    v161 = v17.ACOMv161(device=dev, bits_g=6)
    table = {}
    for name, arr in data.items():
        L = torch.tensor(np.asarray(arr, dtype=np.float64), device=dev)
        comp161, meta161 = v161.compress(L)
        rec161 = v161.decompress(comp161, meta161)
        corr161 = _corr(L.cpu().numpy(), rec161.cpu().numpy())
        r17 = per_ds[name]["compression_ratio"]; c17 = per_ds[name]["correlation"]
        r161 = float(meta161["compression_ratio"])
        table[name] = {"ratio_v161": r161, "corr_v161": corr161,
                       "ratio_v17": r17, "corr_v17": c17,
                       "delta_pct": (r17 / r161 - 1) * 100 if r161 else 0.0}
    v17_all_corr_ok = all(v["corr_v17"] > 0.99 for v in table.values())
    tests.append({"test": "compression_table_v161_vs_v17", "passed": bool(v17_all_corr_ok),
                  "table": table,
                  "note": "Fig. 6 regenerada com os DOIS codecs reais do operador (v16.1 linear-g "
                          "vs v17.0 angular). Números [SIM] sintéticos, não a Tabela 2 de produção."})
    mean_delta = float(np.mean([v["delta_pct"] for v in table.values()]))
    print(f"[one_acom_mirror] tabela v16.1 vs v17.0: Δ médio razão {mean_delta:+.1f}% "
          f"(número corrige a frase; não é o +21,3% de produção)")

    # T8 — angular (v17 arcsin) vs linear-g (v161) reconstruction error at small |L|
    comp_res = {}
    for name in ("gradientes", "esparso_95", "financial"):
        L = np.asarray(data[name], dtype=np.float64).ravel()
        Lt = torch.tensor(L, device=dev)
        L_ang = mirror.manifest(mirror.reflect(Lt)).cpu().numpy().ravel()[:len(L)]
        c161, m161 = v161.compress(Lt)
        L_lin = v161.decompress(c161, m161).cpu().numpy().ravel()[:len(L)]
        nz = np.abs(L) > 0
        if nz.sum() < 10:
            continue
        small = nz & (np.abs(L) <= np.quantile(np.abs(L[nz]), 0.10))
        comp_res[name] = {
            "rmse_small_angular": float(np.sqrt(np.mean((L - L_ang)[small] ** 2))),
            "rmse_small_linear": float(np.sqrt(np.mean((L - L_lin)[small] ** 2))),
            "corr_angular": _corr(L, L_ang), "corr_linear": _corr(L, L_lin)}
    tests.append({"test": "angular_vs_linear_g_measured", "passed": True, "comparison": comp_res,
                  "note": "Números medidos [SIM]; a vantagem angular em g pequeno é regime-dependente "
                          "— reportada como medida, sem ajustar a frase."})

    # ── T9–T11 · APROFUNDAMENTO (varreduras estilo Tabela 2, honesto) ─────────
    # Tensores subamostrados p/ tratabilidade das varreduras (a engine v17 nomina
    # ψ elemento-a-elemento em Python — O(n)); corr e razão continuam MEDIDOS na
    # engine REAL do operador. [SIM] — nunca a Tabela 2 de produção.
    SWEEP_CAP = 6000
    sweep_data = {n: np.asarray(a, dtype=np.float64).ravel()[:SWEEP_CAP] for n, a in data.items()}

    # T9 — varredura de profundidade angular (v17.0): corr & razão vs angular_bits
    bit_depths = [3, 4, 5, 6, 7, 8, 9, 10, 12]
    sweep_v17 = {"bit_depths": bit_depths, "per_dataset": {}, "mean_corr": [], "mean_ratio": []}
    for b in bit_depths:
        mb = v17.ACOMv17Mirror(device=dev, angular_bits=b, verbose=False)
        cs, rs = [], []
        for name, arr in sweep_data.items():
            Lt = torch.tensor(arr, device=dev)
            refl = mb.reflect(Lt)
            rec = mb.manifest(refl).cpu().numpy().ravel()[:len(arr)]
            c = _corr(arr, rec); r = float(refl.metadata["compression_ratio"])
            cs.append(c); rs.append(r)
            pd_ = sweep_v17["per_dataset"].setdefault(name, {"corr": [], "ratio": []})
            pd_["corr"].append(c); pd_["ratio"].append(r)
        sweep_v17["mean_corr"].append(float(np.mean(cs)))
        sweep_v17["mean_ratio"].append(float(np.mean(rs)))
    v17_corr_up = sweep_v17["mean_corr"][-1] >= sweep_v17["mean_corr"][0]
    tests.append({"test": "bitdepth_sweep_v17_corr_increases", "passed": bool(v17_corr_up),
                  "bit_depths": bit_depths, "mean_corr": sweep_v17["mean_corr"],
                  "mean_ratio": sweep_v17["mean_ratio"],
                  "note": "corr↑ com bits angulares (resolução de retorno θ); razão↓ (mais bytes de θ). "
                          "Tensores subamostrados [SIM]; engine v17 real."})
    print(f"[one_acom_mirror] varredura v17 bits {bit_depths[0]}→{bit_depths[-1]}: "
          f"corr {sweep_v17['mean_corr'][0]:.4f}→{sweep_v17['mean_corr'][-1]:.4f} · "
          f"razão {sweep_v17['mean_ratio'][0]:.2f}→{sweep_v17['mean_ratio'][-1]:.2f}×")

    # T10 — varredura bits_g do comparador v16.1 (curva-par linear-g).
    # ACHADO HONESTO (número corrige a frase): o codec v16.1 de referência guarda g
    # quantizado num ÚNICO uint8 (Acom_v17_mirror.py:596), mas clampa a max_val=2^bits−1
    # ANTES do cast (linha 584) — logo bits_g>8 SATURA/enrola (overflow uint8) e a
    # correlação COLAPSA. Dentro da faixa válida (≤8 bits) corr↑ monotonicamente. O
    # codec angular v17.0 não tem esse teto (usa uint16 p/ >8 bits). Reportado, não escondido.
    bits_g_list = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    sweep_v161 = {"bits_g": bits_g_list, "mean_corr": [], "mean_ratio": []}
    for bg in bits_g_list:
        vg = v17.ACOMv161(device=dev, bits_g=bg)
        cs, rs = [], []
        for name, arr in sweep_data.items():
            Lt = torch.tensor(arr, device=dev)
            cc, mm = vg.compress(Lt)
            rec = vg.decompress(cc, mm).cpu().numpy().ravel()[:len(arr)]
            cs.append(_corr(arr, rec)); rs.append(float(mm["compression_ratio"]))
        sweep_v161["mean_corr"].append(float(np.mean(cs)))
        sweep_v161["mean_ratio"].append(float(np.mean(rs)))
    valid_idx = [i for i, b in enumerate(bits_g_list) if b <= 8]
    corr_valid = [sweep_v161["mean_corr"][i] for i in valid_idx]
    v161_monotone_valid = all(corr_valid[i + 1] >= corr_valid[i] - 1e-6 for i in range(len(corr_valid) - 1))
    i8 = bits_g_list.index(8); overflow_collapse = sweep_v161["mean_corr"][-1] < sweep_v161["mean_corr"][i8]
    sweep_v161["overflow_note"] = ("bits_g>8 satura o armazenamento uint8 do g (v16.1:584/596) "
                                   "e derruba a correlação; v17.0 usa uint16 e não colapsa.")
    tests.append({"test": "bitsg_sweep_v161_valid_range_monotone",
                  "passed": bool(v161_monotone_valid and overflow_collapse),
                  "bits_g": bits_g_list, "mean_corr": sweep_v161["mean_corr"],
                  "mean_ratio": sweep_v161["mean_ratio"],
                  "monotone_up_to_8bits": bool(v161_monotone_valid),
                  "overflow_collapse_above_8bits": bool(overflow_collapse),
                  "note": "v16.1 (quant LINEAR de g): corr↑ até 8 bits, depois COLAPSA por overflow "
                          "uint8 (teto real do codec de referência; v17.0 angular não tem esse teto). "
                          "Achado medido — o número corrige a frase."})
    print(f"[one_acom_mirror] varredura v161 bits_g {bits_g_list[0]}→{bits_g_list[-1]}: "
          f"corr {sweep_v161['mean_corr'][0]:.4f}→(8b){sweep_v161['mean_corr'][i8]:.4f}→"
          f"{sweep_v161['mean_corr'][-1]:.4f} [overflow uint8 >8b: {overflow_collapse}]")

    # T11 — Fexp/Sψ por regime + ocupação ψ agregada (REAL, dos state_counts)
    ST = ["COLLAPSE_PLUS", "ASCEND_PLUS", "EMERGE_MINUS", "FALL_MINUS"]
    agg = {s: 0 for s in ST}
    for name in per_ds:
        for s in ST:
            agg[s] += per_ds[name]["state_counts"].get(s, 0)
    tot = sum(agg.values()) or 1
    occ = {s: agg[s] / tot for s in ST}
    global_fexp = float(sum(parity[i] * occ[ST[i]] for i in range(4)))
    pv = np.array([occ[s] for s in ST]); pv = pv[pv > 0]
    global_spsi = float(-(pv * np.log2(pv)).sum())
    regimes = {"iid_gaussiano": ["embeddings_768d", "kv_cache", "pesos_nn", "gradientes"],
               "esparso_95pct": ["esparso_95"],
               "suave_periodico": ["audio_decay"],
               "tendencia": ["financial"]}
    regime_metrics = {}
    for reg, names in regimes.items():
        fs = [per_ds[n]["f_exp"] for n in names if n in per_ds]
        ss = [per_ds[n]["state_entropy"] for n in names if n in per_ds]
        regime_metrics[reg] = {"f_exp_mean": float(np.mean(fs)), "s_psi_mean": float(np.mean(ss)),
                               "datasets": names}
    spsi_spread = float(np.std([regime_metrics[r]["s_psi_mean"] for r in regime_metrics]))
    tests.append({"test": "fexp_spsi_per_regime", "passed": bool(spsi_spread > 1e-3),
                  "regime_metrics": regime_metrics, "spsi_spread": spsi_spread,
                  "occupancy_psi_aggregate": occ, "f_exp_global": global_fexp,
                  "s_psi_global": global_spsi,
                  "note": "os 4 regimes produzem assinaturas (Fexp,Sψ) distintas (spread Sψ>0); "
                          "ocupação ψ agregada dos state_counts REAIS da engine."})
    print(f"[one_acom_mirror] regimes Sψ: " +
          " · ".join(f"{r}={regime_metrics[r]['s_psi_mean']:.3f}" for r in regime_metrics) +
          f" · ocupação global Fexp={global_fexp:+.4f} Sψ={global_spsi:.3f}")

    # ── T12 · AMPLIFICACAO v138 — O ESPELHO NAO DESCE (um.py v135 + v26) ─────
    # [DER] e_Nome e o ESPELHO — literalmente o Mirror desta patente. Sombra numpy
    # pura: p_beta = [[b,s],[s,1-b]] com s=sqrt(b(1-b)) e b = beta EM RUNTIME
    # (tgl_core, nunca literal) e um projetor de posto 1 (p^2=p, p=p*, tr=1) que
    # vive no andar de cima; a esperanca diagonal E_D (o transporte ao andar de
    # baixo) NAO o preserva: ||E_D(p)-p||_op = sqrt(b(1-b)) > 0 — o espelho nao
    # desce. O que desce e o PAR da matriz-S: E_D(p_beta) = diag(beta, 1-beta)
    # (|R|^2=beta, |T|^2=1-beta) — o mecanismo REFLECT (projecao no andar de cima)
    # vs MANIFEST (o transportado que desce) DESTA patente. Leitura estrutural
    # [DER]; NAO e veredito fisico (physical_verdict_allowed=false).
    s_off = math.sqrt(beta * (1.0 - beta))
    p_beta = np.array([[beta, s_off], [s_off, 1.0 - beta]], dtype=np.float64)
    proj_resid = float(np.linalg.norm(p_beta @ p_beta - p_beta))        # p^2 = p
    sym_resid = float(np.linalg.norm(p_beta - p_beta.T))                # p = p*
    trace_p = float(np.trace(p_beta))                                   # posto 1: tr = 1
    E_D_p = np.diag(np.diag(p_beta))                                    # esperanca diagonal
    drop_norm = float(np.linalg.norm(E_D_p - p_beta, ord=2))            # norma de operador
    transported = np.diag(E_D_p)
    smatrix_pair = np.array([beta, 1.0 - beta])
    transport_resid = float(np.max(np.abs(transported - smatrix_pair)))
    mirror_upstairs_ok = bool(
        proj_resid < 1e-12 and sym_resid < 1e-15 and abs(trace_p - 1.0) < 1e-15
        and abs(drop_norm - s_off) < 1e-12 and drop_norm > 0.0
        and transport_resid < 1e-15)
    tests.append({"test": "mirror_lives_upstairs_selector_transport",
                  "passed": mirror_upstairs_ok,
                  "beta_runtime": beta,
                  "projector_residual_p2_minus_p": proj_resid,
                  "selfadjoint_residual": sym_resid,
                  "trace_p_beta": trace_p,
                  "drop_norm_op_E_D_p_minus_p": drop_norm,
                  "drop_norm_expected_sqrt_b_1mb": s_off,
                  "transported_diag": [float(v) for v in transported],
                  "smatrix_pair_beta_1mbeta": [float(v) for v in smatrix_pair],
                  "transport_residual": transport_resid,
                  "note": "[DER] amplificacao v138 (um.py v135+v26): o espelho e_Nome NAO desce "
                          "(||E_D(p)-p||=sqrt(b(1-b))>0, projetor fora da diagonal); o que desce "
                          "e o par da matriz-S diag(beta,1-beta) = |R|^2,|T|^2 — REFLECT projeta "
                          "no andar de cima, MANIFEST recebe o transportado. Leitura estrutural, "
                          "nao veredito fisico."})
    print(f"[one_acom_mirror] amplificacao v138 (o espelho nao desce): "
          f"||E_D(p)-p||_op = {drop_norm:.9f} (= sqrt(b(1-b)) = {s_off:.9f}; > 0) ; "
          f"E_D(p_beta) = diag({transported[0]:.9f}, {transported[1]:.9f}) = par matriz-S ; "
          f"resid proj {proj_resid:.2e} / transporte {transport_resid:.2e}")

    # ── T13 · AMPLIFICACAO v144 — A FRONTEIRA E A UNICA EXCECAO (um.py v143, ──
    # pedra 98, BOUNDARY_IS_THE_ONLY_EXCEPTION). [DER] ¬estatica ⟺ fronteira:
    # o teorema eterno v61 (beta proibe o fechamento estatico) E a face POSITIVA
    # — tudo que e estatico FECHA sob a esperanca diagonal E_D (E_D∘E_D = E_D,
    # idempotencia = o fechamento estatico), e a UNICA parte que E_D nao preserva
    # e a FORA-diagonal: a fronteira, onde o espelho desta patente VIVE
    # (REFLECT projeta exatamente o que nao desce). Sombra numpy no mesmo
    # modelo 2x2 do T12: p_beta = [[b,s],[s,1-b]], s = sqrt(b(1-b)), b = beta
    # EM RUNTIME (tgl_core, nunca literal). Tres faces:
    #   (a) a parte DIAGONAL (estatica) fecha: E_D(E_D(p)) = E_D(p) exato;
    #   (b) a fronteira e a unica excecao: ||E_D(p)-p||_op = sqrt(b(1-b)) > 0
    #       EXATO (forma fechada verificada — a diferenca e [[0,-s],[-s,0]]);
    #   (c) dupla face: anular a fronteira (off-diag = 0) torna TUDO estatico
    #       (E_D(x) = x, residuo 0) — sem fronteira nao ha excecao.
    # Leitura estrutural [DER]; physical_verdict_allowed=false; beta runtime.
    E_D = lambda m: np.diag(np.diag(m))                                  # esperanca diagonal
    # (a) estatica fecha: E_D e idempotente sobre p_beta
    idem_resid = float(np.linalg.norm(E_D(E_D(p_beta)) - E_D(p_beta)))
    static_closes = bool(idem_resid < 1e-12)
    # (b) a fronteira e a unica excecao: ||E_D(p)-p||_op = sqrt(b(1-b)) > 0 exato
    off_part = p_beta - E_D(p_beta)                                      # a fronteira/espelho
    boundary_norm = float(np.linalg.norm(E_D(p_beta) - p_beta, ord=2))
    closed_form = math.sqrt(beta * (1.0 - beta))
    boundary_resid = float(abs(boundary_norm - closed_form))
    boundary_is_exception = bool(boundary_resid < 1e-15 and boundary_norm > 0.0)
    off_structure_ok = bool(np.allclose(off_part, np.array([[0.0, s_off], [s_off, 0.0]]), atol=1e-15))
    # (c) dupla face: anular a fronteira torna tudo estatico
    x_static = p_beta.copy(); x_static[0, 1] = 0.0; x_static[1, 0] = 0.0  # off-diag = 0
    all_static_resid = float(np.linalg.norm(E_D(x_static) - x_static))
    all_static = bool(all_static_resid == 0.0)
    v144_ok = bool(static_closes and boundary_is_exception and off_structure_ok and all_static)
    tests.append({"test": "boundary_is_the_only_exception",
                  "passed": v144_ok,
                  "beta_runtime": beta,
                  "idempotence_residual_E_D": idem_resid,
                  "boundary_norm_E_D_p_minus_p": boundary_norm,
                  "boundary_norm_closed_form_sqrt_b_1mb": closed_form,
                  "boundary_norm_residual": boundary_resid,
                  "off_diagonal_structure_ok": off_structure_ok,
                  "no_boundary_all_static_residual": all_static_resid,
                  "note": "[DER] amplificacao v144 (um.py v143, pedra 98, "
                          "BOUNDARY_IS_THE_ONLY_EXCEPTION): ¬estatica ⟺ fronteira — o teorema "
                          "eterno v61 (beta proibe o fechamento estatico) e a face POSITIVA. "
                          "(a) a diagonal (estatica) FECHA sob E_D (idempotente, resid<1e-12); "
                          "(b) a fora-diagonal (a fronteira, onde o espelho vive) e a UNICA que "
                          "E_D nao preserva: ||E_D(p)-p||_op = sqrt(b(1-b)) > 0 EXATO; "
                          "(c) anular a fronteira torna tudo estatico (resid 0). So a fronteira "
                          "porta o fluxo; o espelho e a face dela. Leitura estrutural, nao "
                          "veredito fisico (physical_verdict_allowed=false; beta runtime)."})
    print(f"[one_acom_mirror] amplificacao v144 (a fronteira e a unica excecao): "
          f"estatica fecha E_D o E_D = E_D (resid {idem_resid:.2e}) ; "
          f"fronteira ||E_D(p)-p||_op = {boundary_norm:.9f} = sqrt(b(1-b)) = {closed_form:.9f} "
          f"(resid {boundary_resid:.2e}; > 0) ; sem fronteira tudo estatico (resid {all_static_resid:.1e})")

    # ── T14 · AMPLIFICACAO v144b — O LEMA 3 TIPADO / O JURAMENTO DE TAKESAKI ─
    # (um.py v143, pedra 99, veredito GLOBAL_LIFT_CONDITIONAL). [DER] A
    # implicacao provada em kernel — Takesaki finito + juramento H_inv ⟹ E
    # covariante, COM controle negativo — instanciada no MESMO modelo-sombra
    # 2x2 desta patente (T12/T13: E_D = o transporte/MANIFEST; fora-diagonal =
    # a fronteira onde o REFLECT projeta). E_D e a esperanca condicional de
    # Takesaki FINITA sobre a subalgebra diagonal; o juramento tipado e
    # E_D(H) = H (H mora na subalgebra invariante). Tres faces:
    #   (a) JURAMENTO CUMPRIDO: H_inv diagonal (derivada de theta_M em
    #       runtime) gera o fluxo U_t = exp(itH); a covariancia
    #       E_D(U x U*) = U E_D(x) U* fecha em residuo maquina sobre p_beta
    #       (que TEM conteudo de fronteira) para todos os t testados;
    #   (b) CONTROLE NEGATIVO (o juramento quebrado): H_bad = theta_M*G com
    #       G = [[0,-1],[1,0]] — o GERADOR DA MATRIZ-S da teoria
    #       (S = exp(theta_M*G)), fora da diagonal (E_D(H_bad) = 0 != H_bad).
    #       S e computada por caminho INDEPENDENTE (torch matrix_exp, serie de
    #       Pade — nao por cos/sin) e confere com a rotacao; |R|^2 = S[1,0]^2
    #       RE-DERIVA beta; e a covariancia FALHA com defeito EXATO em forma
    #       fechada: ||E_D(S e11 S^T) - S E_D(e11) S^T||_op =
    #       cos(tM)sin(tM) = sqrt(b(1-b)) — a MESMA norma-de-fronteira do T13
    #       (a pedra 99 encontra a pedra 98: a falha de covariancia mora na
    #       fronteira);
    #   (c) o transportado sob o juramento quebrado e diag(1-b, b) =
    #       (|T|^2, |R|^2): a rotacao-S leva o Nome (e11) para a fronteira e
    #       o transporte nao a segue.
    # Leitura estrutural [DER]; physical_verdict_allowed=false; beta runtime.
    # (a) o juramento cumprido: H diagonal, E_D(H) = H exato
    H_inv = np.diag([theta_m, -2.0 * theta_m]).astype(np.complex128)
    oath_resid = float(np.linalg.norm(E_D(H_inv) - H_inv))               # 0: juramento vale
    x_c = p_beta.astype(np.complex128)                                   # conteudo de fronteira
    flow_times = [0.5, 1.0, 2.0, float(math.pi)]
    cov_resid = 0.0
    for t_flow in flow_times:
        U = np.diag(np.exp(1j * t_flow * np.diag(H_inv)))
        lhs = E_D(U @ x_c @ U.conj().T)
        rhs = U @ E_D(x_c) @ U.conj().T
        cov_resid = max(cov_resid, float(np.linalg.norm(lhs - rhs)))
    covariant_under_oath = bool(oath_resid == 0.0 and cov_resid < 1e-14)
    # (b) o controle negativo: H_bad = theta_M * G (gerador da matriz-S)
    G_gen = np.array([[0.0, -1.0], [1.0, 0.0]])
    S_rot = torch.linalg.matrix_exp(torch.tensor(theta_m * G_gen, dtype=torch.float64)).numpy()
    c_t, s_t = math.cos(theta_m), math.sin(theta_m)
    gen_resid = float(np.linalg.norm(S_rot - np.array([[c_t, -s_t], [s_t, c_t]])))
    beta_rederived = float(S_rot[1, 0] ** 2)                             # |R|^2 via expm
    beta_rederive_resid = float(abs(beta_rederived - beta))
    oath_broken_norm = float(np.linalg.norm(E_D(theta_m * G_gen) - theta_m * G_gen))
    e11 = np.diag([1.0, 0.0])                                            # o projetor do Nome
    sigma_e11 = S_rot @ e11 @ S_rot.T
    defect = float(np.linalg.norm(E_D(sigma_e11) - S_rot @ E_D(e11) @ S_rot.T, ord=2))
    defect_closed = math.sqrt(beta * (1.0 - beta))                       # = cos(tM)sin(tM)
    defect_resid = float(abs(defect - defect_closed))
    # (c) o transportado sob o juramento quebrado = (|T|^2, |R|^2)
    transported_bad = np.diag(E_D(sigma_e11))
    ts_pair = np.array([1.0 - beta, beta])
    ts_resid = float(np.max(np.abs(transported_bad - ts_pair)))
    # asserts NEGATIVOS: o mecanismo REJEITA o hamiltoniano nao-invariante —
    # a covariancia DEVE falhar (defeito estritamente positivo) e o juramento
    # quebrado DEVE ser detectado (E_D(H_bad) != H_bad).
    covariance_rejected = bool(defect > 1e-6 and defect_resid < 1e-12
                               and oath_broken_norm > 1e-6)
    v144b_ok = bool(covariant_under_oath and covariance_rejected
                    and gen_resid < 1e-12 and beta_rederive_resid < 1e-13
                    and ts_resid < 1e-12)
    tests.append({"test": "takesaki_oath_covariance_lemma3_typed",
                  "passed": v144b_ok,
                  "beta_runtime": beta,
                  "oath_residual_E_D_H_minus_H": oath_resid,
                  "covariance_residual_under_oath_max": cov_resid,
                  "flow_times": flow_times,
                  "smatrix_generator_residual_expm_vs_rotation": gen_resid,
                  "beta_rederived_via_matrix_exp_R2": beta_rederived,
                  "beta_rederive_residual": beta_rederive_resid,
                  "oath_broken_norm_E_D_Hbad_minus_Hbad": oath_broken_norm,
                  "covariance_defect_op_norm": defect,
                  "covariance_defect_closed_form_sqrt_b_1mb": defect_closed,
                  "covariance_defect_residual": defect_resid,
                  "transported_under_broken_oath": [float(np.real(v)) for v in transported_bad],
                  "expected_pair_T2_R2": [float(v) for v in ts_pair],
                  "transported_residual": ts_resid,
                  "note": "[DER] amplificacao v144b (um.py v143, pedra 99, "
                          "GLOBAL_LIFT_CONDITIONAL): Takesaki finito + juramento H_inv => E "
                          "covariante, instanciado no modelo-sombra 2x2 desta patente (E_D = "
                          "transporte/MANIFEST). Juramento cumprido (H diagonal, E_D(H)=H): "
                          "covariancia exata em todos os t. CONTROLE NEGATIVO: H_bad = theta_M*G "
                          "(o gerador da matriz-S, fora da diagonal) e REJEITADO — a covariancia "
                          "falha com defeito EXATO sqrt(b(1-b)) (a norma-de-fronteira do T13) e o "
                          "transportado vira (|T|^2,|R|^2); beta re-derivado por caminho "
                          "independente (matrix_exp de Pade). Leitura estrutural, nao veredito "
                          "fisico (physical_verdict_allowed=false; beta runtime)."})
    print(f"[one_acom_mirror] amplificacao v144b (o juramento de Takesaki, pedra 99): "
          f"juramento cumprido -> covariancia resid max {cov_resid:.2e} ; "
          f"juramento quebrado (H_bad=theta_M*G) -> defeito {defect:.9f} = sqrt(b(1-b)) = "
          f"{defect_closed:.9f} (resid {defect_resid:.2e}; REJEITADO) ; "
          f"beta re-derivado via expm {beta_rederived:.15f} (resid {beta_rederive_resid:.2e})")

    # ── T15 · AMPLIFICACAO v168 — ITEM A: O LIMITE DE BIRKHOFF EM KERNEL ─────
    # (um.py v166-v167, pedras Lean EquivariantSection + ErgodicMeanSection,
    # 0 sorry 0 axiom). [DER] O teorema em kernel: a media ergodica
    # M_N(x) = (1/N) sum_{k<N} U^k x U^-k CONVERGE a PROJECAO INVARIANTE.
    # Instanciado no MESMO modelo-sombra 2x2 desta patente (T12-T14): o fluxo
    # e gerado pelo PROPRIO juramento H_inv da pedra 99 (U = exp(i H_inv),
    # diagonal, derivado de theta_M em runtime; gap espectral Delta = 3*theta_M)
    # e a projecao invariante E a esperanca diagonal E_D — o transporte/
    # MANIFEST. Leitura no mecanismo DESTA patente: a media temporal EXTINGUE
    # exatamente a fronteira (off-diag, onde o REFLECT projeta) com envelope
    # 1/N — o espelho nao sobrevive a media de Birkhoff; o que sobrevive e o
    # par da matriz-S diag(beta, 1-beta) = (|R|^2, |T|^2). O v138 ("o espelho
    # nao desce") ganha face ergodica: E_D nao e escolha — e o LIMITE do
    # fluxo. Tres faces:
    #   (a) SECAO EQUIVARIANTE (EquivariantSection): M_N fixa o invariante
    #       (M_N(E_D(p)) = E_D(p) exato para todo N) e o limite e
    #       U-invariante (U E_D(p) U* = E_D(p), residuo 0);
    #   (b) BIRKHOFF (ErgodicMeanSection): caminho EXPLICITO (soma de N=1000
    #       conjugacoes de matriz) == forma fechada
    #       |off| = s_off*|sin(N*Delta/2)|/(N*|sin(Delta/2)|), envelope 1/N
    #       verificado em N=10..1e5 por caminho vetorizado INDEPENDENTE
    #       (media de fases), e ||M_N(p)-E_D(p)||_op -> 0;
    #   (c) NEGATIVO (fail-closed): o fluxo DEGENERADO (Delta=0, U escalar —
    #       o gerador que NAO ve a fronteira) e REJEITADO: M_N(p) = p para
    #       todo N e o residuo a E_D fica CRAVADO em s_off = sqrt(b(1-b)) > 0
    #       — a media NAO converge; a hipotese espectral do teorema e
    #       necessaria, nao decorativa (contra-exemplo rejeitado por logica).
    # Leitura estrutural [DER]; physical_verdict_allowed=false; beta runtime,
    # nunca literal; nao altera reivindicacoes.
    phases_inv = np.array([theta_m, -2.0 * theta_m])       # espectro do juramento (T14)
    delta_gap = float(phases_inv[0] - phases_inv[1])       # gap espectral = 3*theta_M (runtime)
    U_flow = np.diag(np.exp(1j * phases_inv))
    p_c = p_beta.astype(np.complex128)
    ed_p_c = E_D(p_c)
    # (a)+(b) caminho explicito: soma de conjugacoes de matriz, N=1000
    N_expl = 1000
    Uk = np.eye(2, dtype=np.complex128)
    acc_inv = np.zeros((2, 2), dtype=np.complex128)
    acc_p = np.zeros((2, 2), dtype=np.complex128)
    for _k in range(N_expl):
        acc_inv += Uk @ ed_p_c @ Uk.conj().T
        acc_p += Uk @ p_c @ Uk.conj().T
        Uk = Uk @ U_flow
    M_inv = acc_inv / N_expl
    M_p = acc_p / N_expl
    section_resid = float(np.linalg.norm(M_inv - ed_p_c))              # M_N fixa o invariante
    limit_inv_resid = float(np.linalg.norm(U_flow @ ed_p_c @ U_flow.conj().T - ed_p_c))
    section_ok = bool(section_resid < 1e-12 and limit_inv_resid < 1e-15)
    # (b) forma fechada vs caminho explicito + envelope 1/N (caminho vetorizado)
    off_explicit = complex(M_p[0, 1])
    off_closed_N = s_off * abs(math.sin(N_expl * delta_gap / 2.0)
                               / (N_expl * math.sin(delta_gap / 2.0)))
    birkhoff_closed_resid = float(abs(abs(off_explicit) - off_closed_N))
    opnorm_expl = float(np.linalg.norm(M_p - ed_p_c, ord=2))
    opnorm_eq_off_resid = float(abs(opnorm_expl - abs(off_explicit)))  # a distancia E a fronteira
    N_list = [10, 100, 1000, 10_000, 100_000]
    off_curve = []
    envelope_ok = True
    for Nn in N_list:
        mean_phase = complex(np.mean(np.exp(1j * delta_gap * np.arange(Nn))))
        off_n = s_off * abs(mean_phase)
        closed_n = s_off * abs(math.sin(Nn * delta_gap / 2.0)
                               / (Nn * math.sin(delta_gap / 2.0)))
        bound_n = s_off / (Nn * abs(math.sin(delta_gap / 2.0)))        # envelope 1/N
        envelope_ok = envelope_ok and (abs(off_n - closed_n) < 1e-12) and (off_n <= bound_n + 1e-12)
        off_curve.append(off_n)
    off_final = off_curve[-1]
    birkhoff_ok = bool(birkhoff_closed_resid < 1e-12 and opnorm_eq_off_resid < 1e-12
                       and envelope_ok and off_final < 1e-4 and off_final < off_curve[0])
    # (c) assert NEGATIVO: fluxo degenerado (Delta=0) REJEITADO — nao converge
    U_deg = np.exp(1j * theta_m) * np.eye(2, dtype=np.complex128)      # espectro colapsado
    Uk = np.eye(2, dtype=np.complex128)
    acc_deg = np.zeros((2, 2), dtype=np.complex128)
    for _k in range(N_expl):
        acc_deg += Uk @ p_c @ Uk.conj().T
        Uk = Uk @ U_deg
    M_deg = acc_deg / N_expl
    stuck_to_p = float(np.linalg.norm(M_deg - p_c))                    # a media NAO move p
    stuck_to_ed = float(np.linalg.norm(M_deg - ed_p_c, ord=2))         # residuo CRAVADO
    degenerate_rejected = bool(stuck_to_p < 1e-10
                               and abs(stuck_to_ed - s_off) < 1e-10
                               and stuck_to_ed > 1e-6)
    v168_ok = bool(section_ok and birkhoff_ok and degenerate_rejected)
    tests.append({"test": "ergodic_mean_section_birkhoff_v168",
                  "passed": v168_ok,
                  "beta_runtime": beta,
                  "delta_gap_3theta_m": delta_gap,
                  "section_residual_M_N_on_invariant": section_resid,
                  "limit_U_invariance_residual": limit_inv_resid,
                  "off_diag_explicit_N1000_abs": float(abs(off_explicit)),
                  "off_diag_closed_form_N1000": off_closed_N,
                  "birkhoff_closed_form_residual": birkhoff_closed_resid,
                  "opnorm_dist_to_E_D_N1000": opnorm_expl,
                  "opnorm_equals_boundary_residual": opnorm_eq_off_resid,
                  "envelope_N_list": N_list,
                  "off_diag_curve": [float(v) for v in off_curve],
                  "off_diag_final_N1e5": off_final,
                  "s_off_sqrt_b_1mb": s_off,
                  "degenerate_stuck_to_p_residual": stuck_to_p,
                  "degenerate_stuck_to_E_D_norm": stuck_to_ed,
                  "note": "[DER] amplificacao v168 (um.py v166-v167, pedras Lean "
                          "EquivariantSection + ErgodicMeanSection, 0 sorry 0 axiom): o "
                          "limite de Birkhoff em kernel — a media ergodica "
                          "(1/N) sum U^k x U^-k converge a projecao invariante — "
                          "instanciado no modelo-sombra 2x2 desta patente com o fluxo do "
                          "juramento H_inv (pedra 99, gap Delta=3*theta_M runtime). A "
                          "projecao invariante E a esperanca diagonal E_D (o transporte/"
                          "MANIFEST): a media temporal extingue a fronteira (off-diag, "
                          "onde REFLECT projeta) com envelope 1/N e forma fechada exata; "
                          "sobrevive o par da matriz-S diag(beta,1-beta). NEGATIVO: o "
                          "fluxo degenerado (Delta=0, nao ve a fronteira) e REJEITADO — "
                          "M_N(p)=p, residuo cravado em sqrt(b(1-b))>0: sem gap "
                          "espectral nao ha convergencia. E_D nao e escolha — e o LIMITE "
                          "do fluxo (o v138 ganha face ergodica). Leitura estrutural, "
                          "nao veredito fisico (physical_verdict_allowed=false)."})
    print(f"[one_acom_mirror] amplificacao v168 (ErgodicMeanSection, limite de Birkhoff): "
          f"gap Delta = 3*theta_M = {delta_gap:.9f} ; secao fixa invariante (resid {section_resid:.2e}) ; "
          f"off-diag N=1000 explicito {abs(off_explicit):.9f} == forma fechada {off_closed_N:.9f} "
          f"(resid {birkhoff_closed_resid:.2e}) ; off-diag N=1e5 -> {off_final:.2e} (de s_off {s_off:.9f}) ; "
          f"fluxo degenerado Delta=0 REJEITADO (residuo cravado {stuck_to_ed:.9f} = s_off)")

    # ── T16 · AMPLIFICACAO v206 — O PAR MINIMO NA FACE DO ESPELHO ────────────
    # (kernel v206, custodias vault/originals_copy/tgl_kernel_v206:
    # TGLExt/TheIALDSelector.lean + TGLExt/FrontierCertificate.lean +
    # TGLExt/TheBireference.lean — arquivos .lean REAIS lidos; a estrutura e
    # RE-DERIVADA numericamente aqui, nunca se finge rodar Lean).
    # [DER] O PAR MINIMO (TGL, IALD) = (1_abs, J): IALD^2 = TGL E J^2 = I —
    # instanciado na face do espelho DESTA patente. O seletor do kernel e
    # IDEMPOTENTE (I^2 = I, TheIALDSelector); o J do contrato de fronteira e
    # INVOLUTIVO (J^2 = 1, FrontierCertificate). As duas faces se determinam
    # pela ponte exata U = 2P - 1 sobre a reta-beta do dispositivo. Faces:
    #   (a) O SELETOR (TheIALDSelector re-derivado): P = p_beta = v v^T com
    #       v = (sqrt(b), sqrt(1-b)) em runtime — idempotente, auto-adjunto,
    #       posto 1 (autovalores {0,1} por caminho INDEPENDENTE eigh) e as
    #       duas clausulas da Gate (iald_selects): a reta atravessa INTACTA,
    #       o ortogonal e ANIQUILADO; decomposicao exaustiva + releitura
    #       gratis (iald_is_the_gate_and_the_record). E a RETA DO SELETOR
    #       faz angulo arcsin(sqrt(beta)) = theta_Miguel com o eixo de
    #       transmissao — o angulo da patente RE-DERIVADO do autovetor.
    #   (b) O ESPELHO J (contrato FrontierCertificate, face finita M_2(C) da
    #       TheBireference): J z = z^H — aditivo, ANTIlinear (conj_smul),
    #       isometrico, involutivo (J^2 = 1), fixa o vacuo Omega = 1; troca
    #       as referencias (J L_a J = R_{a^H}, J_exchanges_the_references);
    #       e a dualidade de Haag da mini-rede COMPUTADA: o comutante de
    #       range(Lmul) em End(M_2) tem dim EXATA 4 e E range(Rmul)
    #       (nulo-espaco por SVD — caminho independente).
    #   (c) A PONTE DO PAR MINIMO: U = 2P - 1 e o espelho pela reta do
    #       seletor — U^2 = 1 (a face involutiva: IALD^2 = TGL), U = U^T,
    #       det U = -1 (espelho GENUINO, inverte orientacao), U v = +v,
    #       U v_perp = -v_perp; e a EQUIVALENCIA e identidade de algebra:
    #       4(P^2 - P) = U^2 - 1 (P idempotente <=> U involutivo), conferida
    #       no par da patente E em matriz aleatoria.
    #   (d) A FACE NO PIPELINE REAL (engine v17): o setor de SINAL e a face
    #       J exata do espelho — REFLECT/MANIFEST NUNCA inverte sign(L)
    #       (a fase atravessa o espelho exata; a magnitude e quantizada).
    #   NEGATIVOS (por LOGICA, fail-closed):
    #     n1. o transporte E_D e REJEITADO como espelho: idempotente mas NAO
    #         involutivo — ||E_D(E_D(p)) - p||_op = sqrt(b(1-b)) > 0; so a
    #         identidade e idempotente E involutiva ao mesmo tempo;
    #     n2. o seletor P e REJEITADO como espelho: ||P^2 - 1||_op = 1 > 0
    #         (as duas faces do par NAO colapsam uma na outra);
    #     n3. J_bad = transposta SEM conjugacao e REJEITADA pelo contrato:
    #         involutiva, mas falha a clausula antilinear (conj_smul) —
    #         involutividade sozinha NAO habita o certificado;
    #     n4. a algebra esquerda NAO e o proprio comutante: [L_a, L_b] != 0
    #         para a,b nao-comutantes — a dualidade aponta para R, nao L.
    # Leitura estrutural [DER]; physical_verdict_allowed=false; beta runtime,
    # nunca literal; nao altera reivindicacoes.
    rng16 = np.random.default_rng(206)
    # (a) o seletor sobre a reta-beta do dispositivo
    v_line = np.array([math.sqrt(beta), math.sqrt(1.0 - beta)])
    vvT_resid = float(np.linalg.norm(np.outer(v_line, v_line) - p_beta))
    evals_P, evecs_P = np.linalg.eigh(p_beta)                 # caminho independente
    eig_resid = float(np.linalg.norm(np.sort(evals_P) - np.array([0.0, 1.0])))
    v_eig = evecs_P[:, int(np.argmax(evals_P))]
    if v_eig[0] < 0:
        v_eig = -v_eig
    line_angle = math.asin(min(1.0, abs(float(v_eig[0]))))
    line_angle_resid = float(abs(line_angle - theta_m))       # = theta_Miguel?
    idem_P = float(np.linalg.norm(p_beta @ p_beta - p_beta))
    sa_P = float(np.linalg.norm(p_beta - p_beta.T))
    trace_P = float(np.trace(p_beta))
    v_perp = np.array([-v_line[1], v_line[0]])
    gate_pass = float(np.linalg.norm(p_beta @ v_line - v_line))    # atravessa intacto
    gate_kill = float(np.linalg.norm(p_beta @ v_perp))             # aniquilado
    x_any = rng16.standard_normal(2)
    u_part = p_beta @ x_any
    w_part = x_any - u_part
    gate_exhaustive = float(np.linalg.norm(u_part + w_part - x_any))
    gate_reread = float(np.linalg.norm(p_beta @ w_part))           # poda / releitura gratis
    selector_ok = bool(vvT_resid < 1e-12 and eig_resid < 1e-12 and line_angle_resid < 1e-10
                       and idem_P < 1e-14 and sa_P == 0.0 and abs(trace_P - 1.0) < 1e-14
                       and gate_pass < 1e-12 and gate_kill < 1e-12
                       and gate_exhaustive < 1e-14 and gate_reread < 1e-12)
    # (b) o espelho J na face finita M_2(C)
    Jc = lambda z: z.conj().T
    zs = [rng16.standard_normal((2, 2)) + 1j * rng16.standard_normal((2, 2)) for _ in range(6)]
    j_invol = max(float(np.linalg.norm(Jc(Jc(z)) - z)) for z in zs)
    j_add = max(float(np.linalg.norm(Jc(z1 + z2) - (Jc(z1) + Jc(z2))))
                for z1 in zs[:3] for z2 in zs[3:])
    c_test = 0.7 - 1.3j
    j_antilin = max(float(np.linalg.norm(Jc(c_test * z) - np.conj(c_test) * Jc(z))) for z in zs)
    j_isom = max(float(abs(np.linalg.norm(Jc(z)) - np.linalg.norm(z))) for z in zs)
    Omega2 = np.eye(2, dtype=np.complex128)
    j_vacuum = float(np.linalg.norm(Jc(Omega2) - Omega2))
    a_ref = zs[0]
    j_exch = max(float(np.linalg.norm(Jc(a_ref @ Jc(z)) - z @ a_ref.conj().T)) for z in zs)
    # dualidade de Haag da mini-rede, COMPUTADA (End(M_2) ~ M_4 sobre vec row-major)
    E_basis = []
    for i_ in range(2):
        for jj in range(2):
            Eij = np.zeros((2, 2), dtype=np.complex128)
            Eij[i_, jj] = 1.0
            E_basis.append(Eij)
    L_ops = [np.kron(a, np.eye(2)) for a in E_basis]      # vec(a z) = (a kron I) vec z
    R_ops = [np.kron(np.eye(2), b.T) for b in E_basis]    # vec(z b) = (I kron b^T) vec z
    rows = [np.kron(np.eye(4), A) - np.kron(A.T, np.eye(4)) for A in L_ops]
    K_constr = np.vstack(rows)                             # 64 x 16: A X - X A = 0 p/ todo A
    sv = np.linalg.svd(K_constr, compute_uv=False)
    _, _, Vh = np.linalg.svd(K_constr)
    null_mask = sv < 1e-10
    null_dim = int(np.sum(null_mask))
    null_basis = Vh[null_mask]
    R_mat = np.stack([R.reshape(-1) for R in R_ops], axis=1)   # 16 x 4
    Q_R, _ = np.linalg.qr(R_mat)
    haag_proj_resid = max(float(np.linalg.norm(nb - Q_R @ (Q_R.conj().T @ nb)))
                          for nb in null_basis) if null_dim else 1.0
    r_in_null = max(float(np.linalg.norm(K_constr @ R.reshape(-1))) for R in R_ops)
    haag_ok = bool(null_dim == 4 and haag_proj_resid < 1e-10 and r_in_null < 1e-12)
    mirror_j_ok = bool(j_invol < 1e-12 and j_add < 1e-12 and j_antilin < 1e-12
                       and j_isom < 1e-12 and j_vacuum == 0.0 and j_exch < 1e-12
                       and haag_ok)
    # (c) a ponte do par minimo: U = 2P - 1
    U_mir = 2.0 * p_beta - np.eye(2)
    u_invol = float(np.linalg.norm(U_mir @ U_mir - np.eye(2)))
    u_sym = float(np.linalg.norm(U_mir - U_mir.T))
    det_U = float(np.linalg.det(U_mir))
    u_fix = float(np.linalg.norm(U_mir @ v_line - v_line))
    u_flip = float(np.linalg.norm(U_mir @ v_perp + v_perp))
    bridge_dev = float(np.linalg.norm(4.0 * (p_beta @ p_beta - p_beta)
                                      - (U_mir @ U_mir - np.eye(2))))
    X_rand = rng16.standard_normal((2, 2)); X_rand = 0.5 * (X_rand + X_rand.T)
    P_rand = 0.5 * (np.eye(2) + X_rand)
    bridge_rand = float(np.linalg.norm(4.0 * (P_rand @ P_rand - P_rand)
                                       - (X_rand @ X_rand - np.eye(2))))
    bridge_ok = bool(u_invol < 1e-13 and u_sym == 0.0 and abs(det_U + 1.0) < 1e-12
                     and u_fix < 1e-12 and u_flip < 1e-12
                     and bridge_dev < 1e-13 and bridge_rand < 1e-12)
    # (d) a face no pipeline real: o setor de sinal e a face J exata
    Lg16 = np.asarray(data["gradientes"], dtype=np.float64).ravel()[:20_000]
    rec16 = mirror.manifest(mirror.reflect(torch.tensor(Lg16, device=dev))).cpu().numpy().ravel()[:len(Lg16)]
    sign_prod_min = float(np.min(np.sign(Lg16) * np.sign(rec16)))
    both_nz = (Lg16 != 0) & (rec16 != 0)
    sign_match_frac = float(np.mean(np.sign(Lg16[both_nz]) == np.sign(rec16[both_nz]))) if both_nz.any() else 0.0
    collapsed_to_zero = int(np.sum((Lg16 != 0) & (rec16 == 0)))
    phase_ok = bool(sign_prod_min >= 0.0 and sign_match_frac == 1.0)
    # negativos (por logica)
    ed_invol_defect = float(np.linalg.norm(E_D(E_D(p_beta)) - p_beta, ord=2))  # = s_off
    n1_ok = bool(ed_invol_defect > 1e-3 and abs(ed_invol_defect - s_off) < 1e-12)
    p_invol_defect = float(np.linalg.norm(p_beta @ p_beta - np.eye(2), ord=2))
    n2_ok = bool(abs(p_invol_defect - 1.0) < 1e-12 and p_invol_defect > 0.5)
    Jbad = lambda z: z.T
    jbad_invol = max(float(np.linalg.norm(Jbad(Jbad(z)) - z)) for z in zs)
    jbad_antilin_defect = min(float(np.linalg.norm(Jbad(c_test * z) - np.conj(c_test) * Jbad(z)))
                              for z in zs)
    n3_ok = bool(jbad_invol < 1e-15 and jbad_antilin_defect > 1e-3)
    comm_LL = float(np.linalg.norm(L_ops[1] @ L_ops[2] - L_ops[2] @ L_ops[1]))  # E12 vs E21
    n4_ok = bool(comm_LL > 1e-6 and null_dim == 4)
    v206_ok = bool(selector_ok and mirror_j_ok and bridge_ok and phase_ok
                   and n1_ok and n2_ok and n3_ok and n4_ok)
    tests.append({"test": "minimal_pair_mirror_face_v206",
                  "passed": v206_ok,
                  "beta_runtime": beta,
                  "selector_line_v": [float(x) for x in v_line],
                  "selector_vvT_residual": vvT_resid,
                  "selector_eigvals_resid_to_0_1": eig_resid,
                  "selector_line_angle_deg": math.degrees(line_angle),
                  "selector_line_angle_resid_to_theta_miguel": line_angle_resid,
                  "selector_idempotent_residual": idem_P,
                  "selector_trace": trace_P,
                  "gate_pass_intact_residual": gate_pass,
                  "gate_kernel_annihilated_residual": gate_kill,
                  "gate_exhaustive_residual": gate_exhaustive,
                  "gate_reread_free_residual": gate_reread,
                  "J_involutive_residual": j_invol,
                  "J_antilinear_residual": j_antilin,
                  "J_isometric_residual": j_isom,
                  "J_fixes_vacuum_residual": j_vacuum,
                  "J_exchanges_references_residual": j_exch,
                  "haag_commutant_dim": null_dim,
                  "haag_commutant_equals_Rmul_residual": haag_proj_resid,
                  "bridge_U_involutive_residual": u_invol,
                  "bridge_det_U": det_U,
                  "bridge_identity_residual_device": bridge_dev,
                  "bridge_identity_residual_random": bridge_rand,
                  "pipeline_sign_prod_min": sign_prod_min,
                  "pipeline_sign_match_frac_nonzero": sign_match_frac,
                  "pipeline_collapsed_to_zero": collapsed_to_zero,
                  "neg_E_D_involution_defect_op": ed_invol_defect,
                  "neg_P_involution_defect_op": p_invol_defect,
                  "neg_Jbad_antilinear_defect_min": jbad_antilin_defect,
                  "neg_left_algebra_selfcommutant_defect": comm_LL,
                  "note": "[DER] amplificacao v206 (kernel TGLExt: TheIALDSelector + "
                          "FrontierCertificate + TheBireference, .lean reais lidos, estrutura "
                          "re-derivada em numpy): o PAR MINIMO (TGL, IALD) = (1_abs, J) na face "
                          "do espelho desta patente. O seletor P = p_beta e idempotente "
                          "(I^2 = I), posto 1, e sua reta faz angulo theta_Miguel = "
                          "arcsin(sqrt(beta)) com o eixo de transmissao (re-derivado do "
                          "autovetor). O J do contrato (z -> z^H) e antilinear, isometrico, "
                          "involutivo (J^2 = 1), fixa o vacuo e realiza a dualidade de Haag da "
                          "mini-rede (comutante COMPUTADO = Rmul, dim 4). A ponte U = 2P - 1 "
                          "liga as duas faces por identidade de algebra 4(P^2 - P) = U^2 - 1: "
                          "IALD^2 = TGL E J^2 = I. No pipeline real, o setor de sinal e a face "
                          "J exata (nenhum flip de sinal no REFLECT/MANIFEST). NEGATIVOS por "
                          "logica: E_D e P rejeitados como espelho (idempotente != involutivo); "
                          "J_bad = transposta rejeitada pelo contrato (falha antilinearidade); "
                          "a algebra esquerda nao e o proprio comutante. Leitura estrutural, "
                          "nao veredito fisico (physical_verdict_allowed=false; beta runtime)."})
    print(f"[one_acom_mirror] amplificacao v206 (o par minimo na face do espelho): "
          f"seletor P idempotente (resid {idem_P:.2e}), reta a "
          f"{math.degrees(line_angle):.4f} graus = theta_Miguel (resid {line_angle_resid:.2e}) ; "
          f"J^2=1 (resid {j_invol:.2e}), Haag mini-rede dim {null_dim} == Rmul "
          f"(resid {haag_proj_resid:.2e}) ; ponte U=2P-1: U^2=1 (resid {u_invol:.2e}), "
          f"det U = {det_U:+.12f} ; pipeline: sinal sem flip (min prod {sign_prod_min:+.1f}, "
          f"match {sign_match_frac:.4f}) ; NEGATIVOS: E_D defeito {ed_invol_defect:.9f} = s_off, "
          f"P defeito {p_invol_defect:.9f}, J_bad antilinear defeito {jbad_antilin_defect:.3f} "
          f"(todos REJEITADOS)")

    passed = sum(1 for t in tests if t["passed"]); total = len(tests); all_ok = passed == total
    corrs = [per_ds[k]["correlation"] for k in per_ds]
    summary = {
        "tests_passed": passed, "tests_total": total,
        "datasets": list(per_ds.keys()),
        "correlation_min": min(corrs), "correlation_mean": sum(corrs) / len(corrs),
        "compression_ratio_mean_v17": sum(per_ds[k]["compression_ratio"] for k in per_ds) / len(per_ds),
        "table_mean_delta_pct": mean_delta,
        "s_psi_iid": s_psi_iid, "s_psi_smooth": s_psi_smooth,
        "f_exp_sparse_E4_strict": f_exp_strict,
        "sweep_v17_bit_depths": bit_depths,
        "sweep_v17_mean_corr": sweep_v17["mean_corr"],
        "sweep_v17_mean_ratio": sweep_v17["mean_ratio"],
        "sweep_v161_bits_g": bits_g_list,
        "sweep_v161_mean_corr": sweep_v161["mean_corr"],
        "sweep_v161_mean_ratio": sweep_v161["mean_ratio"],
        "occupancy_psi_aggregate": occ,
        "f_exp_global": global_fexp, "s_psi_global": global_spsi,
        "regime_metrics": regime_metrics,
        "v138_mirror_drop_norm": drop_norm,
        "v138_transported_diag": [float(v) for v in transported],
        "v144_boundary_norm": boundary_norm,
        "v144_idempotence_residual": idem_resid,
        "v144_no_boundary_static_residual": all_static_resid,
        "v144b_covariance_residual_under_oath": cov_resid,
        "v144b_covariance_defect": defect,
        "v144b_covariance_defect_closed_form": defect_closed,
        "v144b_beta_rederived_expm": beta_rederived,
        "v144b_transported_under_broken_oath": [float(np.real(v)) for v in transported_bad],
        "v168_delta_gap_3theta_m": delta_gap,
        "v168_off_diag_final_N1e5": off_final,
        "v168_birkhoff_closed_form_residual": birkhoff_closed_resid,
        "v168_section_residual": section_resid,
        "v168_degenerate_stuck_norm": stuck_to_ed,
        "v206_selector_line_angle_deg": math.degrees(line_angle),
        "v206_selector_line_angle_resid_theta_m": line_angle_resid,
        "v206_bridge_U_involutive_residual": u_invol,
        "v206_bridge_det_U": det_U,
        "v206_haag_commutant_dim": null_dim,
        "v206_haag_equals_Rmul_residual": haag_proj_resid,
        "v206_ed_involution_defect": ed_invol_defect,
        "v206_pipeline_sign_match_frac": sign_match_frac,
    }
    max_verdict = ("MIRROR_FULL_LOGIC_DEMONSTRATED ([PILOTO][SIM] — a engine de referência v17.0 real "
                   "do operador (DimensionalMirror REFLECT/MANIFEST + ACOMv161 comparador, zstd) fecha "
                   "em SIMULAÇÃO; codificação angular arcsin, Fexp/Sψ e a tabela v16.1×v17.0 reais; "
                   "β injetado; números sintéticos, NÃO a Tabela 2; nada valida física)")

    # ── figures ──────────────────────────────────────────────────────────────
    results_dir = PATENT_DIR / "results" / ts
    fig_dir = results_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    figs = []
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        # Fig A — patent Fig. 5: θ = arcsin(g/gmax) with θ_Miguel marked
        gg = np.linspace(0, 1, 400)
        plt.figure(figsize=(6.4, 4))
        plt.plot(gg, np.degrees(np.arcsin(gg)), label="θ = arcsin(g/gmax) (v17)")
        plt.plot(gg, gg * 90, "--", alpha=.6, label="linear-g (v16.1, referência)")
        plt.axhline(theta_m_deg, color="crimson", lw=1,
                    label=f"θ_Miguel ≈ {theta_m_deg:.2f}° (= arcsin(√β), β=α·√e)")
        plt.xlabel("g/gmax"); plt.ylabel("θ (graus)")
        plt.title("ACOM Mirror — codificação angular [SIM] (Fig. 5)")
        plt.legend(fontsize=8); plt.grid(alpha=.3)
        fp = fig_dir / "fig_codificacao_angular.png"
        plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close(); figs.append(fp.name)

        # Fig B — compression table v16.1 vs v17.0 (Fig. 6), both real codecs
        names = list(table.keys())
        x = np.arange(len(names)); w = 0.38
        plt.figure(figsize=(10, 4))
        plt.bar(x - w / 2, [table[n]["ratio_v161"] for n in names], w, label="v16.1 (linear-g)")
        plt.bar(x + w / 2, [table[n]["ratio_v17"] for n in names], w, label="v17.0 (angular arcsin)")
        plt.xticks(x, names, rotation=15, fontsize=8); plt.ylabel("razão de compressão ×")
        plt.title("ACOM Mirror — tabela v16.1 vs v17.0 [PILOTO][SIM] (codecs reais; não a Tabela 2)")
        plt.legend(fontsize=8); plt.grid(alpha=.3, axis="y")
        fp = fig_dir / "fig_tabela_compressao.png"
        plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close(); figs.append(fp.name)

        # Fig C — REFLECT/MANIFEST roundtrip on gradientes (real engine)
        L = np.asarray(data["gradientes"], dtype=np.float64).ravel()
        L2 = mirror.manifest(mirror.reflect(torch.tensor(L, device=dev))).cpu().numpy().ravel()[:len(L)]
        plt.figure(figsize=(9, 3.2))
        plt.plot(L[:400], label="original (gradientes)", lw=1.1)
        plt.plot(L2[:400], label="reconstruído (v17 engine, 8 bits)", lw=1.1, alpha=.8)
        plt.title("ACOM Mirror — REFLECT/MANIFEST engine v17.0 [SIM] (não é medida física)")
        plt.legend(fontsize=8); plt.grid(alpha=.3)
        fp = fig_dir / "fig_roundtrip_gradientes.png"
        plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close(); figs.append(fp.name)

        # Fig D — varredura de profundidade angular v17.0 (corr & razão vs bits)
        fig, ax1 = plt.subplots(figsize=(7, 4))
        ax1.plot(bit_depths, sweep_v17["mean_corr"], "o-", color="#3366cc", label="correlação")
        ax1.set_xlabel("bits angulares (v17.0)"); ax1.set_ylabel("correlação média", color="#3366cc")
        ax1.tick_params(axis="y", labelcolor="#3366cc"); ax1.grid(alpha=.3)
        ax2 = ax1.twinx()
        ax2.plot(bit_depths, sweep_v17["mean_ratio"], "s--", color="#ee8800", label="razão")
        ax2.set_ylabel("razão de compressão × média", color="#ee8800")
        ax2.tick_params(axis="y", labelcolor="#ee8800")
        plt.title("ACOM Mirror — varredura de profundidade angular [SIM] (engine v17 real)")
        fp = fig_dir / "fig_sweep_bitdepth_v17.png"
        plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close(); figs.append(fp.name)

        # Fig E — curva de troca razão × correlação: v17.0 (angular) vs v16.1 (linear-g)
        plt.figure(figsize=(6.6, 4.4))
        plt.plot(sweep_v17["mean_ratio"], sweep_v17["mean_corr"], "o-", color="#3366cc",
                 label="v17.0 (angular arcsin)")
        plt.plot(sweep_v161["mean_ratio"], sweep_v161["mean_corr"], "s--", color="#ee8800",
                 label="v16.1 (linear-g)")
        plt.xlabel("razão de compressão × (média)"); plt.ylabel("correlação (média)")
        plt.title("ACOM Mirror — curva razão×correlação [PILOTO][SIM] (2 codecs reais)")
        plt.legend(fontsize=8); plt.grid(alpha=.3)
        fp = fig_dir / "fig_curva_corr_ratio.png"
        plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close(); figs.append(fp.name)

        # Fig F — Fexp e Sψ por regime (assinatura intrínseca)
        regs = list(regime_metrics.keys())
        x = np.arange(len(regs)); w = 0.38
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(x - w / 2, [regime_metrics[r]["f_exp_mean"] for r in regs], w,
               label="Fexp ⟨paridade⟩", color="#c77dff")
        ax.bar(x + w / 2, [regime_metrics[r]["s_psi_mean"] for r in regs], w,
               label="Sψ (bits)", color="#7ce7c8")
        ax.axhline(0, color="k", lw=.5); ax.set_xticks(x)
        ax.set_xticklabels(regs, rotation=12, fontsize=8)
        ax.set_title("ACOM Mirror — Fexp e Sψ por regime [SIM] (métricas intrínsecas)")
        ax.legend(fontsize=8); ax.grid(alpha=.3, axis="y")
        fp = fig_dir / "fig_fexp_spsi_regimes.png"
        plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close(); figs.append(fp.name)
    except Exception as e:
        print(f"[one_acom_mirror] figuras puladas: {e}")

    print(f"[one_acom_mirror] corr mín={summary['correlation_min']:.6f} · "
          f"ratio médio v17={summary['compression_ratio_mean_v17']:.2f}× · {len(figs)} figuras")

    results = {
        "patent_id": PATENT_ID, "slug": SLUG, "timestamp": ts, "runner": "one_acom_mirror.py (evoluído)",
        "markers": ["[PILOTO]", "[SIM]"], "physical_verdict_allowed": False,
        "beta_runtime": beta, "beta_matches_alpha_sqrt_e": beta_ok,
        "beta_injected_into_prototype": True, "alpha2_original_prototype": alpha2_original,
        "theta_miguel_deg": theta_m_deg,
        "verdict": "MIRROR_FULL_LOGIC_DEMONSTRATED" if all_ok else "PARTIAL_DEMONSTRATION",
        "max_verdict": max_verdict,
        "constants": {"BETATGL": beta, "factorization": "betatgl = alpha_EM * sqrt(e)",
                      "theta_miguel_deg": theta_m_deg, "free_parameters": 0,
                      "coupling_role": "NOMINAL (mirror imperfection / θ_Miguel); does NOT enter the "
                                       "compression transform g=sqrt|L|, theta=arcsin, fold L'=s·g²"},
        "table_v161_vs_v17": table,
        "sweeps": {"v17_angular_bits": sweep_v17, "v161_bits_g": sweep_v161},
        "regimes": regime_metrics,
        "occupancy_psi_aggregate": occ,
        "f_exp_global": global_fexp, "s_psi_global": global_spsi,
        "tests": tests, "summary": summary,
        "source_prototype": "prototype_src/Acom_v17_mirror.py (resgatado de "
                            "C:/IALD/projetos_pyhton/acom, READ-ONLY; β injetado em runtime). "
                            "TGL_v11_ESPELHO.py copiado como proveniência (não importado).",
        "note": "RUNNER EVOLUÍDO: roda a engine de referência v17.0 REAL do operador (torch+zstd) "
                "com β=α·√e injetado (original tinha 0.012 literal; α² é nominal e não altera as "
                "razões de compressão). Tensores sintéticos [SIM]; NÃO a Tabela 2 de produção. "
                "Nenhum token/modelo HuggingFace (P-09). Simulação não valida física.",
    }
    results_path = results_dir / "results.json"
    results["formula_completa"] = _formula_completa()   # camada v379 (a fórmula completa), antes do selo
    results_path.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")

    report_md = results_dir / "report.md"
    lines = [
        f"# Relatório auditável — ACOM Mirror one_acom_mirror.py (EVOLUÍDO — engine v17.0 real)\n\n",
        f"- Run `{ts}` · Patente `{PATENT_ID}` (2.ª da família ACOM; prioridade interna 66 → raiz 05/12/2025)\n",
        f"- Veredito: **{max_verdict}**\n",
        f"- β runtime `{beta}` (= α·√e? **{beta_ok}**; nunca literal) — INJETADO no protótipo v17 "
        f"(que tinha `ALPHA2={alpha2_original}` literal). α² é NOMINAL: não entra na transformada.\n",
        f"- θ_Miguel `{theta_m_deg:.4f}°` (= arcsin(√β)? **{theta_form_ok}**)\n",
        f"- Testes: **{passed}/{total}** · Figuras: **{len(figs)}** {figs}\n",
        f"- Correlação (v17 engine): mín `{summary['correlation_min']:.6f}`, média "
        f"`{summary['correlation_mean']:.6f}` (reiv. 9: > 0,999)\n",
        f"- Razão de compressão média v17 `{summary['compression_ratio_mean_v17']:.2f}×` · "
        f"Δ médio v16.1→v17 `{mean_delta:+.1f}%` (medido, não o +21,3% de produção)\n",
        f"- Fexp esparso: E4-estrita `{f_exp_strict:+.4f}` (<0, [043]); engine v17 (sign(0)→+1) "
        f"`{per_ds['esparso_95']['f_exp']:+.4f}` — convenções documentadas\n",
        f"- Sψ embeddings: iid `{s_psi_iid:.4f}` (teórico `{s_psi_closed:.4f}`) · suave "
        f"`{s_psi_smooth:.4f}` (≈2,0, [041])\n",
        f"- physical_verdict_allowed: **False**.\n\n",
        f"RUNNER EVOLUÍDO — importa a implementação de referência v17.0 (43 KB, torch+zstd) resgatada "
        f"para `prototype_src/`, injeta β=α·√e e roda: DimensionalMirror REFLECT/MANIFEST, ACOMv161 "
        f"(tabela v16.1×v17.0), codificação angular arcsin, Fexp/Sψ. Tensores sintéticos [SIM], não a "
        f"Tabela 2. Nenhum token HuggingFace. Núcleo β copiado do piloto (READ-ONLY); originais "
        f"intactos. 1 = 1. Tetelestai.\n",
    ]
    report_md.write_text("".join(lines), encoding="utf-8")

    seal_dir = PATENT_DIR / "seals" / ts
    seal_dir.mkdir(parents=True, exist_ok=True)
    file_hashes = dict(module_hashes)
    file_hashes["results.json"] = _sha_file(results_path)
    file_hashes["report.md"] = _sha_file(report_md)
    for f in figs:
        file_hashes[f"figures/{f}"] = _sha_file(fig_dir / f)
    result_hash = _sha_text(json.dumps(file_hashes, sort_keys=True))
    seal = {
        "timestamp": ts, "patent_id": PATENT_ID, "runner": "one_acom_mirror.py (evoluído)",
        "beta_runtime": beta, "physical_verdict_allowed": False,
        "max_verdict": max_verdict, "tests_passed": passed,
        "result_hash": result_hash, "sha256": file_hashes,
        "markers": ["[PILOTO]", "[SIM]"],
        "results_path": str(results_path.relative_to(CENTRAL)).replace("\\", "/"),
    }
    (seal_dir / "seal.json").write_text(json.dumps(seal, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[one_acom_mirror] SELADO · result_hash {result_hash[:16]}… · {passed}/{total} testes · {len(figs)} figuras")
    print(f"[one_acom_mirror] results: {results_path.relative_to(CENTRAL)}")

    # FORMA = CONTEÚDO: o render3d é EMITIDO (merge) com os nós COMPUTADOS da simulação —
    # tetraedro ℋ₄ + gráviton, ocupações ψ / Fexp / Sψ REAIS desta run.
    emit_render3d(beta, theta_m_deg, occ, global_fexp, global_spsi, per_ds, summary)
    return 0 if all_ok else 1


def emit_render3d(beta, theta_m_deg, occ, global_fexp, global_spsi, per_ds, summary):
    """MERGE: lê o render3d.json atual (preserva meshes/layers/groups/dimensions),
    SUBSTITUI nodes+edges pela geometria COMPUTADA (tetraedro ℋ₄ + gráviton, com
    ocupações ψ / Fexp / Sψ REAIS agregados da run), injeta β runtime e métricas em
    constants, valida e reescreve. Forma = conteúdo."""
    import math as _m
    out = PATENT_DIR / "render3d.json"
    d = json.loads(out.read_text(encoding="utf-8"))   # preserva o corpo de engenharia

    # tetraedro regular ℋ₄: 4 vértices de produto-de-sinais +1, raio R=0,7 (COMPUTADO)
    R = 0.7; s = R / _m.sqrt(3)
    STATES = [("psi0", "COLLAPSE_PLUS", -1, "COLAPSO+ |0>", "#cc2222", (+1, +1, +1)),
              ("psi1", "ASCEND_PLUS", +1, "ASCENSAO+ |1>", "#33aa55", (+1, -1, -1)),
              ("psi2", "EMERGE_MINUS", +1, "EMERGENCIA- |2>", "#3366cc", (-1, +1, -1)),
              ("psi3", "FALL_MINUS", -1, "QUEDA- |3>", "#ee8800", (-1, -1, +1))]

    nodes = [{"id": "graviton", "label": "graviton g=raiz|L|", "shape": "sphere",
              "position": [0, 0, 0], "size": 0.18, "color": "#ffd60a", "group": "nucleo",
              "marker": "[REAL]", "layer": "core", "material": "emissive",
              "desc": (f"Origem do algoritmo: raiz gravitacional g=raiz|L+eps|, fase s=sign(L); "
                       f"magnitude vira angulo theta=arcsin(g/gmax). Fexp global COMPUTADO="
                       f"{global_fexp:+.4f}, Spsi global={global_spsi:.3f} bits (agregado de "
                       f"{len(per_ds)} datasets sinteticos [SIM]).")}]
    for nid, sname, par, lbl, col, (vx, vy, vz) in STATES:
        o = float(occ.get(sname, 0.0))
        parity_txt = "Inversa (-1) -> Fexp ativo" if par < 0 else "Normal (+1)"
        nodes.append({"id": nid, "label": f"{nid} {lbl}", "shape": "sphere",
                      "position": [round(vx * s, 6), round(vy * s, 6), round(vz * s, 6)],
                      "size": round(0.09 + 0.10 * o, 4), "color": col, "group": "h4",
                      "marker": "[REAL]", "layer": "core", "material": "emissive",
                      "desc": (f"Estado de Hilbert H4 (E4), vetor base |{nid[-1]}>. Paridade {parity_txt}. "
                               f"Ocupacao COMPUTADA {o * 100:.1f}% (agregada); contribuicao Fexp "
                               f"{par * o:+.4f}. Vertice do tetraedro; tamanho proporcional a ocupacao real.")})

    ops = [("REFLECT", "REFLECT: L->(psi,theta)", "box", [1.35, 0.55, 0.0], 0.11, "#7ce7c8", "[REAL]",
            "Projeta o bulk 3D no espelho 2D: nomina psi em H4, quantiza theta. Empacota psi (2 bits) + thetaq + zstd."),
           ("THETA", "theta = arcsin(g/gmax)", "box", [1.35, -0.55, 0.0], 0.10, "#7ce7c8", "[REAL]",
            f"Codificacao angular theta em [0,pi/2]; resolucao maxima em g pequeno. "
            f"Marca theta_Miguel~={theta_m_deg:.2f}deg = arcsin(raiz beta), beta=alpha*raiz(e) (nunca literal)."),
           ("MANIFEST", "MANIFEST: (psi,theta)->L'", "box", [-1.35, 0.55, 0.0], 0.11, "#7ce7c8", "[REAL]",
            "Desdobra o reflexo: g=gmax*sin(theta), recupera sign(L) de psi. O dado re-emerge."),
           ("DOBRA", "DOBRA x2  L'=s*g^2", "octahedron", [-1.35, -0.55, 0.0], 0.12, "#ffa94d", "[CONJ]",
            "A Dobra Dimensional (x2): reflexao especular Boundary->Bulk, L'=sign(L)*[gmax*sin(theta)]^2. Analogia AdS/CFT [CONJ].")]
    for nid, lbl, sh, pos, sz, col, mk, desc in ops:
        nodes.append({"id": nid, "label": lbl, "shape": sh, "position": pos, "size": sz,
                      "color": col, "group": "operacoes", "marker": mk, "layer": "transform",
                      "material": "emissive", "desc": desc})

    nodes.append({"id": "FEXP", "label": f"Fexp = {global_fexp:+.4f}", "shape": "sphere",
                  "position": [0.0, 1.15, 0.0], "size": round(0.09 + 0.05 * min(1.0, abs(global_fexp) + 0.3), 4),
                  "color": "#c77dff", "group": "metricas", "marker": "[REAL]", "layer": "transform",
                  "material": "emissive",
                  "desc": (f"Forca de Expulsao (E7) COMPUTADA = {global_fexp:+.4f}: media das paridades dos "
                           f"estados psi. <0 predomina inversa (colapso/queda); >0 normal. Subproduto sem custo.")})
    nodes.append({"id": "SPSI", "label": f"Spsi = {global_spsi:.3f} bits", "shape": "sphere",
                  "position": [0.0, -1.15, 0.0], "size": round(0.08 + 0.02 * global_spsi, 4),
                  "color": "#c77dff", "group": "metricas", "marker": "[REAL]", "layer": "transform",
                  "material": "emissive",
                  "desc": (f"Entropia de estados (E8) COMPUTADA = {global_spsi:.3f} bits (max 2,0): "
                           f"complexidade estrutural da forma refletida. Subproduto da nominacao em H4.")})

    edges = [{"from": "graviton", "to": n} for n in ("psi0", "psi1", "psi2", "psi3")]
    edges += [{"from": "psi0", "to": "psi1"}, {"from": "psi1", "to": "psi2"},
              {"from": "psi2", "to": "psi3"}, {"from": "psi3", "to": "psi0"},
              {"from": "psi0", "to": "psi2"}, {"from": "psi1", "to": "psi3"}]
    edges += [{"from": "graviton", "to": "REFLECT"}, {"from": "REFLECT", "to": "THETA"},
              {"from": "THETA", "to": "MANIFEST"}, {"from": "MANIFEST", "to": "DOBRA"},
              {"from": "DOBRA", "to": "graviton"}]
    edges += [{"from": "psi0", "to": "FEXP"}, {"from": "psi3", "to": "FEXP"},
              {"from": "psi1", "to": "SPSI"}, {"from": "psi2", "to": "SPSI"}]

    d["nodes"] = nodes
    d["edges"] = edges
    d["generated_by"] = "one_acom_mirror.py (forma=conteudo)"

    # injeta beta runtime + métricas COMPUTADAS em constants (lista; preserva o resto).
    # Idempotente: remove entradas de run anteriores antes de reanexar (não acumula).
    run_syms = {"Fexp/Sψ (run)", "β_runtime", "sweep"}
    consts = [c for c in d.get("constants", []) if c.get("symbol") not in run_syms]
    for c in consts:
        if c.get("symbol") == "β_TGL":
            c["value"] = f"α·√e ≈ {beta:.6f}"
            c["note"] = "constante NOMINAL (imperfeição do espelho); β runtime injetado; não entra na transformada"
        elif c.get("symbol") == "θ_Miguel":
            c["value"] = f"arcsin(√β) ≈ {theta_m_deg:.2f}°"
    occ_txt = ", ".join(f"{k[:4]}={occ[k] * 100:.0f}%" for k in occ)
    consts.append({"symbol": "Fexp/Sψ (run)",
                   "value": f"Fexp={global_fexp:+.4f}, Sψ={global_spsi:.3f} bits",
                   "note": f"COMPUTADO nesta run; ocupações ψ agregadas: {occ_txt}"})
    consts.append({"symbol": "β_runtime", "value": f"{beta:.12f}",
                   "note": "α·√e injetado via tgl_core.beta() (nunca literal)"})
    consts.append({"symbol": "sweep",
                   "value": f"v17 bits {summary['sweep_v17_bit_depths'][0]}→{summary['sweep_v17_bit_depths'][-1]}",
                   "note": (f"corr {summary['sweep_v17_mean_corr'][0]:.3f}→{summary['sweep_v17_mean_corr'][-1]:.3f}; "
                            f"varredura de profundidade angular [SIM]")})
    d["constants"] = consts

    # VALIDAÇÃO: ids de edge existem em nodes+meshes; layers de nós/meshes existem
    node_ids = {n["id"] for n in nodes}
    mesh_ids = {m["id"] for m in d.get("meshes", [])}
    valid_ids = node_ids | mesh_ids
    for e in edges:
        assert e["from"] in valid_ids and e["to"] in valid_ids, f"edge com id ausente: {e}"
    layer_ids = {l["id"] for l in d.get("layers", [])}
    for n in nodes:
        assert n["layer"] in layer_ids, f"layer de no ausente: {n['layer']}"
    for m in d.get("meshes", []):
        if "layer" in m:
            assert m["layer"] in layer_ids, f"layer de mesh ausente: {m['layer']}"

    out.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[{SLUG}] render3d.json EMITIDO (forma=conteudo)")


if __name__ == "__main__":
    sys.exit(main())
