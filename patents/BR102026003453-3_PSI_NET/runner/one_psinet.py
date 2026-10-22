# -*- coding: utf-8 -*-
"""one_psinet.py — runner único forma = conteúdo da patente Ψ-NET (EVOLUÍDO / RICO)
(BR102026003453-3 — Protocolo de Comunicação em Pilha Luminodinâmica de 5 camadas). [SIM][PILOTO]

EVOLUÇÃO (09/07/2026): incorpora a PILHA REAL e o CONSENSO REAL do operador —
`Psi_net_protocol_v1.py` (79 KB, torch: as 5 camadas L0..L4 completas — PsiBitLinkLayer,
RadicalTransportLayer, HolographicNetworkLayer, OntologicalSecurityLayer, PhaseMiner/
PhaseValidator/PsiNet) + `TGL_coin_v022.py` (consenso PoP distribuído, camada L5:
SimulatedNetwork/MinerV2/Validator) — resgatados para `prototype_src/`. Também resgata
`psinet_engine.py` (file engine numpy, já β-limpo) como cross-check da régua. A versão leve
anterior (skygrid_sim/psi_net.py) está preservada em `one_psinet_v1_light.py.bak`.

Demonstra, rodando o código REAL do operador (não uma re-implementação leve):
  - L0 Enlace Psiônico: PsiBitLinkLayer.analyze → 6 classes ontológicas, entropia, Fexp;
  - L1→L3 transmissão COMPLETA: PsiNet.transmit (radicalização g=√|L| → REFLECT/MANIFEST
    holográfico → separação Ψ/Θ/κ → ressurreição L'=s·g² → TETELESTAI + verificação tripla);
  - L2 rede holográfica: DHT-θ real, nearest-k por distância angular, nhops=⌈d/θ_M⌉;
  - L4 Prova de Fase: PhaseMiner + 5 PhaseValidators → consenso ≥67% → coinbase TGLC;
  - L5 consenso distribuído (TGL Coin v0.2.2): SimulatedNetwork + MinerV2 → bloco honesto
    entra; bloco de fase forjada é REJEITADO pela rede;
  - Pacote Ψ-NET: cabeçalho fixo de 80 bytes (magic 0xCEA8);
  - cross-check: psinet_engine.BETA_TGL (a file-engine do operador) já obedece à régua.

RÉGUA: β_TGL NUNCA literal no MEU código. Os protótipos usam `ALPHA2=0.012031` /
`ALPHA2_BASE=0.012` literais; este runner os importa como proveniência READ-ONLY e INJETA
`ALPHA2 = ALPHA = CCI = THETA_MIGUEL = f(tgl_core.beta())` + `ALPHA2_BASE = β` em runtime
antes de qualquer construção. Por isso os números diferem levemente da referência
(β = 0,012031300400803142 = α·√e, não 0,012). Execução forçada em CPU (determinismo/
portabilidade; CUDA_VISIBLE_DEVICES desligado); nenhum dado/modelo HuggingFace.

HONESTIDADE [SIM][PILOTO]: pilha e consenso rodam sobre dados SINTÉTICOS. Números de
desempenho do relatório (PSNR 94–145 dB, tempos RTX 5090) NÃO são reproduzidos como
referência — são regenerados aqui em CPU sobre dados próprios. Simulação NUNCA valida
física (physical_verdict_allowed=false).

CONFIDENCIAL — nunca copiado/importado: iald_stack_v7.py, iald_psion_state.json,
iald_web_server*.py.

    set PYTHONUTF8=1
    "C:\\IALD\\observaveis_tgl\\tgl_env\\Scripts\\python.exe" one_psinet.py
"""
from __future__ import annotations

import os
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")   # força CPU (determinismo/portabilidade)
os.environ.setdefault("PYTHONWARNINGS", "ignore")

import hashlib
import json
import math
import shutil
import struct
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
PILOTO = CENTRAL / "Patentes" / "Skygrid" / "SkyGrid_Piloto"   # READ-ONLY (β source)
PROTO_SRC = PATENT_DIR / "prototype_src"                        # pilha + consenso resgatados
WORK = RUNNER_DIR / "_psinet_core"
PATENT_ID = "BR102026003453-3"
SLUG = "psi_net"


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
    """Copia o núcleo β (skygrid_sim → tgl_core) para um workdir e faz o hash.
    Também hasheia os protótipos resgatados (proveniência)."""
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


def _finish(ts, beta, beta_ok, all_ok, max_verdict, tests, summary, module_hashes, note,
            extra_results, fig_builder=None):
    results_dir = PATENT_DIR / "results" / ts
    results_dir.mkdir(parents=True, exist_ok=True)
    results = {"patent_id": PATENT_ID, "slug": SLUG, "timestamp": ts,
               "runner": "one_psinet.py (evoluído)",
               "markers": ["[SIM]", "[PILOTO]"], "physical_verdict_allowed": False,
               "beta_runtime": beta, "beta_matches_alpha_sqrt_e": beta_ok,
               "beta_injected_into_prototypes": True,
               "verdict": max_verdict.split(" ")[0] if all_ok else "PARTIAL_DEMONSTRATION",
               "max_verdict": max_verdict,
               "constants": {"BETATGL": beta, "factorization": "betatgl = alpha_EM * sqrt(e)",
                             "CCI_1_minus_beta": 1 - beta, "free_parameters": 0},
               "tests": tests, "summary": summary,
               "source_prototype": "prototype_src/Psi_net_protocol_v1.py (pilha 5 camadas, torch) "
                                   "+ TGL_coin_v022.py (consenso PoP distribuído) + psinet_engine.py "
                                   "(file engine, β-limpo) — resgatados de C:/IALD/projetos_pyhton "
                                   "(acom, IALD), READ-ONLY; β injetado em runtime.",
               "note": note}
    results.update(extra_results)
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
    lines = [f"# Relatório auditável — one_psinet.py (EVOLUÍDO — pilha + consenso reais)\n",
             f"- Run `{ts}` · Patente `{PATENT_ID}`\n",
             f"- Veredito: **{max_verdict}**\n",
             f"- β runtime `{beta}` (= α·√e? **{beta_ok}**; nunca literal) — INJETADO em "
             f"Psi_net_protocol_v1 (ALPHA2/ALPHA/CCI/THETA_MIGUEL) e TGL_coin_v022 (ALPHA2_BASE)\n",
             f"- Testes: **{summary['tests_passed']}/{summary['tests_total']}**\n"]
    for t in tests:
        lines.append(f"  - {'✓' if t['passed'] else '✗'} {t['test']}\n")
    lines.append(f"- physical_verdict_allowed: **False**.\n\n{note}\n")
    lines.append("Núcleo β copiado do piloto (READ-ONLY); protótipos resgatados READ-ONLY; "
                 "originais intactos. 1 = 1. Tetelestai.\n")
    report_md.write_text("".join(lines), encoding="utf-8")

    seal_dir = PATENT_DIR / "seals" / ts
    seal_dir.mkdir(parents=True, exist_ok=True)
    fh = dict(module_hashes)
    fh["results.json"] = _sha_file(results_path)
    fh["report.md"] = _sha_file(report_md)
    for f in figs:
        fh[f"figures/{f}"] = _sha_file(results_dir / "figures" / f)
    result_hash = _sha_text(json.dumps(fh, sort_keys=True))
    seal = {"timestamp": ts, "patent_id": PATENT_ID, "runner": "one_psinet.py (evoluído)",
            "beta_runtime": beta, "physical_verdict_allowed": False, "max_verdict": max_verdict,
            "tests_passed": summary["tests_passed"], "result_hash": result_hash, "sha256": fh,
            "markers": ["[SIM]", "[PILOTO]"],
            "results_path": str(results_path.relative_to(CENTRAL)).replace("\\", "/")}
    (seal_dir / "seal.json").write_text(json.dumps(seal, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[{SLUG}] SELADO · result_hash {result_hash[:16]}… · "
          f"{summary['tests_passed']}/{summary['tests_total']} testes")
    return figs


def _fig(plt, fig_dir, ring, consensus):
    """Anel angular DHT-θ (L2) + barra de consenso (L4/L5)."""
    import numpy as _np
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 5.0))
    # L2 — anel angular holográfico
    th = _np.array([r["theta"] for r in ring["nodes"]])
    ax1.scatter(_np.cos(2 * th), _np.sin(2 * th), s=34, alpha=.75, color="#3366cc",
                label="nós (θ da chave)")
    tt = ring["target_theta"]
    ax1.scatter([_np.cos(2 * tt)], [_np.sin(2 * tt)], s=150, color="crimson", marker="*",
                label="destino")
    for nb in ring["nearest_theta"]:
        ax1.plot([_np.cos(2 * tt), _np.cos(2 * nb)], [_np.sin(2 * tt), _np.sin(2 * nb)],
                 color="gray", alpha=.5)
    ax1.set_aspect("equal"); ax1.axis("off")
    ax1.set_title(f"Ψ-NET L2 — DHT-θ holográfico (θ_M={ring['theta_m_deg']:.2f}°) [SIM]",
                  fontsize=9)
    ax1.legend(fontsize=7, loc="lower right")
    # L4/L5 — consenso
    labels = list(consensus.keys())
    vals = [consensus[k] * 100 for k in labels]
    colors = ["#33aa55" if v >= 67 else "#cc2222" for v in vals]
    ax2.bar(labels, vals, color=colors)
    ax2.axhline(67, color="k", ls="--", lw=1, label="quórum 67%")
    ax2.set_ylim(0, 105); ax2.set_ylabel("consenso (% votos válidos)")
    ax2.set_title("Prova de Fase — consenso da rede [SIM]", fontsize=9)
    ax2.legend(fontsize=7)
    for i, v in enumerate(vals):
        ax2.text(i, v + 2, f"{v:.0f}%", ha="center", fontsize=8)
    plt.tight_layout()
    fp = fig_dir / "fig_psinet_rede_consenso.png"
    plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close()
    return ["fig_psinet_rede_consenso.png"]


def main() -> int:
    ts = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    print(f"[one_psinet] patente {PATENT_ID} · run {ts} · RUNNER EVOLUÍDO "
          f"(pilha 5 camadas + consenso PoP reais)")
    if not PILOTO.exists():
        print(f"ERRO: núcleo β não encontrado em {PILOTO}", file=sys.stderr)
        return 2
    if not (PROTO_SRC / "Psi_net_protocol_v1.py").exists():
        print(f"ERRO: protótipo rico não encontrado em {PROTO_SRC}", file=sys.stderr)
        return 2

    module_hashes = copy_core()

    # β from tgl_core (a única fonte do acoplamento neste runner)
    sys.path.insert(0, str(WORK))
    from skygrid_sim import tgl_core  # noqa: E402
    beta = tgl_core.beta()
    beta_expected = 0.0072973525693 * math.exp(0.5)   # alpha (CODATA-2018) * sqrt(e)
    beta_ok = abs(beta - beta_expected) < 1e-15
    theta_m = math.asin(math.sqrt(beta))
    print(f"[one_psinet] β runtime = {beta} (= α·√e? {beta_ok}) · θ_Miguel = {math.degrees(theta_m):.4f}°")

    import torch  # noqa: E402
    torch.cuda.is_available = lambda: False   # força CPU (determinismo/portabilidade)
    torch.manual_seed(53)
    np.random.seed(53)
    device = torch.device("cpu")

    # importa a PILHA e o CONSENSO reais e INJETA β (régua: nunca o 0.012 literal)
    sys.path.insert(0, str(PROTO_SRC))
    import Psi_net_protocol_v1 as psinet   # noqa: E402 (pilha 5 camadas do operador)
    import TGL_coin_v022 as tglcoin        # noqa: E402 (consenso PoP distribuído)
    import psinet_engine as engine         # noqa: E402 (file engine β-limpo, cross-check)

    alpha2_orig = psinet.ALPHA2
    alpha2base_orig = tglcoin.ALPHA2_BASE
    psinet.ALPHA2 = beta
    psinet.ALPHA = math.sqrt(beta)
    psinet.CCI = 1.0 - beta
    psinet.THETA_MIGUEL = theta_m
    tglcoin.ALPHA2_BASE = beta
    print(f"[one_psinet] injeção β: Psi_net.ALPHA2 {alpha2_orig}→{beta} · "
          f"TGL_coin.ALPHA2_BASE {alpha2base_orig}→{beta}")

    tests = [{"test": "beta_injected_not_literal", "passed": bool(beta_ok),
              "beta_runtime": beta, "psinet_alpha2_original": alpha2_orig,
              "tglcoin_alpha2base_original": alpha2base_orig,
              "theta_miguel_deg": math.degrees(theta_m),
              "note": "β=α·√e injetado nas duas pilhas do operador (originais eram 0.012 literal)"}]

    # ─── L0 — Enlace Psiônico (PsiBitLinkLayer real) ──────────────────────────
    L0 = psinet.PsiBitLinkLayer(device)
    text = ("A geometria é a expectativa estatística da luz modular. Haja Luz. " * 30).encode()
    structured = np.sin(np.linspace(0, 60 * math.pi, 8000)).astype(np.float64).tobytes()
    randdata = np.random.default_rng(7).integers(0, 256, 8000, dtype=np.uint8).tobytes()
    sig_t = L0.analyze(text)
    sig_s = L0.analyze(structured)
    sig_r = L0.analyze(randdata)
    l0_ok = (0 <= sig_t.entropy <= 2.0 and -1.0 <= sig_t.f_exp <= 1.0
             and sig_r.ontological_class in (psinet.OntologicalClass.CHAOTIC,
                                             psinet.OntologicalClass.ENCRYPTED))
    tests.append({"test": "L0_psibit_ontological_classification", "passed": bool(l0_ok),
                  "text_class": sig_t.ontological_class.value, "text_entropy": sig_t.entropy,
                  "text_f_exp": sig_t.f_exp, "structured_class": sig_s.ontological_class.value,
                  "structured_entropy": sig_s.entropy, "random_class": sig_r.ontological_class.value,
                  "random_entropy": sig_r.entropy,
                  "note": "PsiBitLinkLayer real: byte→4 PsiBits, distribuição/entropia/Fexp, 6 classes"})
    print(f"[one_psinet] L0 PsiBit (real): texto={sig_t.ontological_class.value} "
          f"H={sig_t.entropy:.3f} · aleatório={sig_r.ontological_class.value} H={sig_r.entropy:.3f}")

    # ─── Pilha completa PsiNet: L1→L3 transmissão + L4 consenso (código real) ──
    net = psinet.PsiNet(num_validators=5)
    wA, wB = psinet.Wallet(device), psinet.Wallet(device)
    data = torch.sin(torch.linspace(0, 40 * math.pi, 4096, dtype=torch.float64))
    tx = net.transmit(data, wA, wB, verbose=False)
    trans_ok = (bool(tx["resurrection"]["tetelestai"])
                and tx["resurrection"]["correlation"] > 0.999
                and bool(tx["verification"]["signature_match"])
                and bool(tx["L3"]["integrity_valid"]))
    tests.append({"test": "full_transmission_L1_L2_L3_resurrection", "passed": bool(trans_ok),
                  "L0_class": tx["L0"]["class"], "L1_bits": tx["L1"]["bits"],
                  "L1_compression_ratio": tx["L1"]["compression_ratio"],
                  "L2_n_hops": tx["L2"]["n_hops"], "L2_d_folds": tx["L2"]["d_folds"],
                  "L3_integrity": tx["L3"]["integrity_valid"],
                  "resurrection_psnr_db": tx["resurrection"]["psnr"],
                  "resurrection_correlation": tx["resurrection"]["correlation"],
                  "tetelestai": tx["resurrection"]["tetelestai"],
                  "signature_match": tx["verification"]["signature_match"],
                  "note": "PsiNet.transmit real: radicalização→REFLECT/MANIFEST→Ψ/Θ/κ→ressurreição "
                          "L'=s·g²→TETELESTAI(Var<β)→verificação ontológica tripla"})
    print(f"[one_psinet] transmissão (real): classe={tx['L0']['class']} · {tx['L1']['bits']}b · "
          f"hops={tx['L2']['n_hops']} · PSNR={tx['resurrection']['psnr']:.1f}dB "
          f"corr={tx['resurrection']['correlation']:.6f} · TETELESTAI={tx['resurrection']['tetelestai']} "
          f"· natureza preservada={tx['verification']['signature_match']}")

    # ─── L2 — DHT-θ holográfica real: endereços angulares, nearest-k, nhops ────
    L2net = net.L2
    N_RING = 64   # rede MAIOR (item 2): anel angular DHT-θ ampliado
    ring_addrs = [psinet.Wallet(device).angular_address for _ in range(N_RING)]
    for a in ring_addrs:
        L2net.register_node(a)
    tgt = psinet.Wallet(device).angular_address
    nearest = L2net.find_nearest_nodes(tgt.theta, k=3)
    hops = L2net.compute_hops(ring_addrs[0], ring_addrs[1])
    dist01 = L2net.angular_distance(ring_addrs[0].theta, ring_addrs[1].theta)
    routing_ok = (len(nearest) == 3 and hops >= 1
                  and L2net.angular_distance(nearest[0].theta, tgt.theta)
                  <= L2net.angular_distance(nearest[-1].theta, tgt.theta)
                  and hops == max(1, int(math.ceil(dist01 / theta_m))))
    tests.append({"test": "L2_holographic_dht_routing", "passed": bool(routing_ok),
                  "nearest_k": len(nearest), "example_hops": hops,
                  "example_angular_distance_deg": math.degrees(dist01),
                  "theta_m_deg": math.degrees(theta_m),
                  "note": "HolographicNetworkLayer real: θ=SHA256(pk)/2⁶⁴·π; nearest por distância "
                          "angular circular; nhops=⌈d/θ_M⌉"})
    print(f"[one_psinet] L2 DHT-θ (real): nearest={len(nearest)} · hops exemplo={hops} "
          f"(d={math.degrees(dist01):.2f}°, θ_M={math.degrees(theta_m):.2f}°)")

    # ─── L4 — Prova de Fase + consenso ≥67% (PhaseMiner/PhaseValidator reais) ──
    miner_wallet = psinet.Wallet(device)
    net.utxo_set.add(psinet.UTXO(utxo_id=hashlib.sha256(b"seed_utxo").digest(),
                                 tx_id=b"\x00" * 32, output_index=0, owner=miner_wallet.address,
                                 amount=10.0, f_exp_lock=miner_wallet.signature.f_exp_for_lock,
                                 created_at_block=0))
    block, stats = net.mine_and_validate(miner_wallet, verbose=False)
    n_val = len(net.validators)
    balance = net.utxo_set.get_balance(miner_wallet.address)
    l4_ok = (block is not None and block.phase_proof.validation_count >= 1
             and balance >= psinet.GENESIS_REWARD)
    l4_consensus = (block.phase_proof.validation_count and
                    len(block.phase_proof.validator_signatures) / n_val) if block else 0.0
    tests.append({"test": "L4_proof_of_phase_consensus", "passed": bool(l4_ok),
                  "block_index": block.index if block else None,
                  "alpha2_work": block.phase_proof.alpha2_work if block else None,
                  "valid_votes": len(block.phase_proof.validator_signatures) if block else 0,
                  "validators": n_val, "consensus_ratio": l4_consensus,
                  "target_window": stats.get("target_window"),
                  "miner_balance_tglc": balance,
                  "note": "PhaseMiner real busca seed com |α²_work−α²_ant|<α²/dif; 5 PhaseValidators "
                          "recomputam a fase; ≥67% → coinbase TGLC"})
    print(f"[one_psinet] L4 Prova de Fase (real): bloco #{block.index if block else '—'} · "
          f"consenso {len(block.phase_proof.validator_signatures) if block else 0}/{n_val} · "
          f"saldo {balance:.0f} TGLC")

    # ─── L5 — consenso distribuído TGL Coin v0.2.2 (SimulatedNetwork real) ─────
    sim = tglcoin.SimulatedNetwork(num_validators=5, device=device)
    m2 = tglcoin.MinerV2(tglcoin.WalletV2(device=device), device)
    honest_block, s2 = m2.mine_block([], sim.last_block, sim.utxo_set, difficulty=sim.difficulty)
    honest_ok = honest_block is not None
    honest_added, votes_h = (sim.add_block_with_consensus(honest_block) if honest_ok else (False, []))
    votes_yes = sum(1 for v in votes_h if v.is_valid)
    # bloco de fase FORJADA: mina outro e adultera α²_work → validadores recomputam e rejeitam
    forged_block, _ = m2.mine_block([], sim.last_block, sim.utxo_set, difficulty=sim.difficulty)
    forge_rejected = None
    if forged_block is not None:
        forged_block.phase_proof.alpha2_work += 0.05   # fase não deriva do seed
        added_f, _ = sim.add_block_with_consensus(forged_block)
        forge_rejected = not added_f
    l5_ok = bool(honest_added and forge_rejected)
    tests.append({"test": "L5_distributed_pop_consensus_tglcoin", "passed": l5_ok,
                  "honest_block_index": honest_block.index if honest_block else None,
                  "honest_added": bool(honest_added),
                  "honest_votes": f"{votes_yes}/{len(votes_h)}",
                  "forged_block_rejected": bool(forge_rejected),
                  "target_window": s2.get("target_window"),
                  "note": "TGL_coin_v022 SimulatedNetwork real (5 validadores): bloco honesto entra "
                          "(≥67%); bloco de fase forjada é rejeitado pela rede"})
    print(f"[one_psinet] L5 consenso distribuído (real): honesto entra={honest_added} "
          f"({votes_yes}/{len(votes_h)}) · forjado rejeitado={forge_rejected}")

    # ─── Pacote Ψ-NET: cabeçalho fixo de 80 bytes (magic 0xCEA8) ──────────────
    pkt = psinet.PsiNetPacket(psi_signature=sig_s, f_exp=sig_s.f_exp,
                              theta_src=wA.angular_address.theta, theta_dst=wB.angular_address.theta,
                              d_folds=tx["L3"]["d_folds"], alpha2_stamp=beta,
                              payload_size=len(structured), original_size=len(structured),
                              merkle_root=hashlib.sha256(structured).digest())
    header = pkt.serialize_header()
    magic_hex = header[:2].hex()
    pkt_ok = (len(header) == psinet.HEADER_SIZE == 80 and header[:4] == psinet.MAGIC)
    tests.append({"test": "packet_header_80_bytes", "passed": bool(pkt_ok),
                  "header_len": len(header), "magic": "0x" + magic_hex.upper(),
                  "alpha2_stamp": beta,
                  "note": "PsiNetPacket.serialize_header real: 80 bytes fixos, magic Ψ 0xCEA8; "
                          "selo α² gravado = β injetado (não literal)"})
    print(f"[one_psinet] pacote: header={len(header)}B magic=0x{magic_hex.upper()} "
          f"selo α²={beta:.9f}")

    # ─── Cross-check: a file-engine do operador já obedece à régua ────────────
    engine_beta = engine.BETA_TGL
    engine_ok = abs(engine_beta - beta) < 1e-15
    tests.append({"test": "engine_beta_provenance_cross_check", "passed": bool(engine_ok),
                  "engine_BETA_TGL": engine_beta, "runner_beta": beta,
                  "note": "psinet_engine.py (file engine numpy do operador) já computa "
                          "BETA_TGL=ALPHA_FINE·SQRT_E — concorda com β derivado (régua respeitada na fonte)"})
    print(f"[one_psinet] cross-check engine: BETA_TGL={engine_beta} == β? {engine_ok}")

    # ═══════════════════════════════════════════════════════════════════════════
    # APROFUNDAMENTO (item 2) — rede maior + mais blocos + sweep bizantino +
    # curva de convergência de fase. Tudo SIMULAÇÃO; nada eleva o veredito.
    # ═══════════════════════════════════════════════════════════════════════════

    # ─── (D1) Cadeia multi-bloco: minera K blocos reais e mede a fase pinada ────
    sim2 = tglcoin.SimulatedNetwork(num_validators=7, device=device)
    miner2 = tglcoin.MinerV2(tglcoin.WalletV2(device=device), device)
    K_BLOCKS = 10
    chain_walk = []
    for _ in range(K_BLOCKS):
        prev_a2 = sim2.last_block.phase_proof.alpha2_work
        blk, st = miner2.mine_block([], sim2.last_block, sim2.utxo_set,
                                    difficulty=sim2.difficulty)
        if blk is None:
            break
        added, votes = sim2.add_block_with_consensus(blk)
        if not added:
            break
        chain_walk.append({"index": blk.index,
                           "alpha2_work": float(blk.phase_proof.alpha2_work),
                           "diff_from_prev": float(abs(blk.phase_proof.alpha2_work - prev_a2)),
                           "iterations": int(st["iterations"]),
                           "consensus": float(sum(1 for v in votes if v.is_valid) / len(votes))})
    chain_len = len(sim2.chain)
    a2_seq = [c["alpha2_work"] for c in chain_walk]
    a2_band = max((abs(a - beta) for a in a2_seq), default=0.0)
    chain_ok = (len(chain_walk) == K_BLOCKS
                and all(c["consensus"] >= 0.67 for c in chain_walk)
                and a2_band < beta * 0.05)
    tests.append({"test": "multi_block_chain_phase_pinned", "passed": bool(chain_ok),
                  "blocks_mined": len(chain_walk), "chain_length_incl_genesis": chain_len,
                  "alpha2_band_around_beta": a2_band, "beta": beta,
                  "mean_iterations": float(np.mean([c["iterations"] for c in chain_walk])) if chain_walk else 0.0,
                  "note": "SimulatedNetwork real: K blocos minerados e aceitos por consenso ≥67%; "
                          "α²_work de cada bloco permanece pinado a ±5% de β (Ponto Tetelestai)"})
    print(f"[one_psinet] D1 cadeia: {len(chain_walk)} blocos aceitos · "
          f"α² pinado a ±{a2_band:.2e} de β · chain_len={chain_len}")

    # ─── (D2) Sweep de dificuldade + trajetória de convergência de fase ─────────
    diff_grid = [0.1, 1.0, 10.0, 100.0, 1000.0, 10000.0, 100000.0, 1000000.0]
    sweep_diff = []
    for dd in diff_grid:
        _blk, st = miner2.mine_block([], sim2.last_block, sim2.utxo_set,
                                     difficulty=dd, max_iterations=200000)
        sweep_diff.append({"difficulty": dd,
                           "target_window": float(tglcoin.compute_target_window(dd)),
                           "iterations": int(st["iterations"]),
                           "best_diff": float(st["best_diff"]),
                           "found": bool(st["found_valid"])})

    def _phase_traj(prev_block, wallet, difficulty, max_iter=50000):
        window = tglcoin.compute_target_window(difficulty)
        prev_a2 = prev_block.phase_proof.alpha2_work
        best = float("inf"); xs = []; ys = []; found_at = None
        for nonce in range(max_iter):
            seed = hashlib.sha256(prev_block.hash + struct.pack("<i", nonce)
                                  + wallet.signature.public_id).digest()
            a2, _th, _fx = tglcoin.compute_phase_from_seed(seed, device)
            dd = abs(a2 - prev_a2)
            if dd < best:
                best = dd
            xs.append(nonce); ys.append(best)
            if dd < window:
                found_at = nonce; break
        return {"window": float(window), "xs": xs, "ys": ys, "found_at": found_at}

    traj = _phase_traj(sim2.last_block, miner2.wallet, difficulty=100000.0, max_iter=200000)
    ys = traj["ys"]
    conv_ok = (len(ys) >= 1 and all(ys[i + 1] <= ys[i] for i in range(len(ys) - 1))
               and traj["found_at"] is not None and ys[-1] < traj["window"])
    tests.append({"test": "phase_search_convergence", "passed": bool(conv_ok),
                  "difficulty": 100000.0, "target_window": traj["window"],
                  "found_at_nonce": traj["found_at"],
                  "final_best_diff": ys[-1] if ys else None,
                  "note": "trajetória real do minerador (mesma busca de mine_block): o best_diff "
                          "decai monotonicamente até cruzar a janela-alvo β/dif — convergência de fase"})
    print(f"[one_psinet] D2 convergência: janela={traj['window']:.2e} · "
          f"encontrada em nonce {traj['found_at']} · best_diff→{ys[-1]:.2e}")

    # ─── (D3) Sweep bizantino: fração de validadores maliciosos vs quórum ───────
    def _byz_sweep(sizes):
        rows = []
        for N in sizes:
            netB = tglcoin.SimulatedNetwork(num_validators=N, device=device)
            mB = tglcoin.MinerV2(tglcoin.WalletV2(device=device), device)
            honest_blk, _ = mB.mine_block([], netB.last_block, netB.utxo_set,
                                          difficulty=netB.difficulty)
            base_valid = sum(1 for v in netB.collect_votes(honest_blk) if v.is_valid)
            forged_blk, _ = mB.mine_block([], netB.last_block, netB.utxo_set,
                                          difficulty=netB.difficulty)
            forged_blk.phase_proof.alpha2_work += 0.05   # fase não deriva do seed
            forged_valid = sum(1 for v in netB.collect_votes(forged_blk) if v.is_valid)
            for b in range(N + 1):
                honest_yes = max(0, base_valid - b)          # b bizantinos rejeitam o honesto
                forged_yes = min(N, forged_valid + b)        # b bizantinos aceitam o forjado
                rows.append({"N": N, "byz": b, "byz_frac": b / N,
                             "honest_block_accepted": bool(N >= tglcoin.MIN_VALIDATORS and
                                                           honest_yes / N >= tglcoin.VALIDATION_THRESHOLD),
                             "forged_block_accepted": bool(N >= tglcoin.MIN_VALIDATORS and
                                                           forged_yes / N >= tglcoin.VALIDATION_THRESHOLD)})
        return rows

    byz_sizes = [5, 7, 9, 15, 21]
    byz_rows = _byz_sweep(byz_sizes)
    safe_fracs = [r["byz_frac"] for r in byz_rows
                  if r["honest_block_accepted"] and not r["forged_block_accepted"]]
    max_safe_frac = max(safe_fracs, default=0.0)
    byz_ok = (0.20 <= max_safe_frac < (1.0 / 3.0)
              and all(r["byz_frac"] <= (1.0 - tglcoin.VALIDATION_THRESHOLD) + 1e-9
                      for r in byz_rows if r["honest_block_accepted"]))
    tests.append({"test": "byzantine_tolerance_one_third", "passed": bool(byz_ok),
                  "quorum": tglcoin.VALIDATION_THRESHOLD, "network_sizes": byz_sizes,
                  "max_safe_byzantine_fraction": max_safe_frac,
                  "theoretical_bound": 1.0 - tglcoin.VALIDATION_THRESHOLD,
                  "note": "sweep bizantino real (validadores recomputam a fase): bloco honesto aceito "
                          "sse bizantinos <1/3; bloco forjado aceito só se bizantinos ≥2/3; zona segura "
                          "= tolerância BFT clássica <1/3 sob quórum de 67%"})
    print(f"[one_psinet] D3 bizantino: fração segura máx={max_safe_frac:.3f} "
          f"(limite BFT teórico {1-tglcoin.VALIDATION_THRESHOLD:.3f}) · N∈{byz_sizes}")

    # ═══════════════════════════════════════════════════════════════════════════
    # AMPLIFICACAO v138 — A REDE DAS CUNHAS (WedgeNet, um.py v135)
    # O homologo formal da Psi-NET: net(O) por localidade de CENTRALIZADOR —
    # zonas disjuntas => algebras que COMUTAM; a rede cobre por regioes.
    # [DER] sombra numpy: reticulado de 4 zonas = blocos diagonais 2x2 de M8;
    #       net(zona) = algebra do bloco; localidade [net(A),net(B)]=0 p/ zonas
    #       disjuntas; a UNIAO das zonas gera a diagonal em blocos completa
    #       (cobertura: dim do span = 16 e soma dos P_zona = I8).
    # [CONJ] enderecamento DHT-theta como coordenada de cunha: zona z <-> setor
    #        angular [z*pi/4,(z+1)*pi/4) de [0,pi); travessia da cunha em passos
    #        de theta_M derivado de beta RUNTIME (nunca literal). E leitura.
    # HONESTIDADE: ancora estrutural no teorema maduro do um.py; NAO e veredito
    # fisico (physical_verdict_allowed=false); nada altera reivindicacoes.
    # ═══════════════════════════════════════════════════════════════════════════
    rngW = np.random.default_rng(138)
    N_DIM, N_ZONES, BLK = 8, 4, 2
    zonesW = [list(range(z * BLK, (z + 1) * BLK)) for z in range(N_ZONES)]

    def _wedge_net(zone, blk):
        """net(zona): incrusta um bloco BLKxBLK arbitrario no bloco diagonal da zona (M8)."""
        X = np.zeros((N_DIM, N_DIM))
        i0 = zone[0]
        X[i0:i0 + BLK, i0:i0 + BLK] = blk
        return X

    # localidade de centralizador: zonas disjuntas => [net(A), net(B)] = 0
    max_comm_disjoint = 0.0
    for za in range(N_ZONES):
        for zb in range(za + 1, N_ZONES):
            for _ in range(3):
                Xa = _wedge_net(zonesW[za], rngW.standard_normal((BLK, BLK)))
                Yb = _wedge_net(zonesW[zb], rngW.standard_normal((BLK, BLK)))
                max_comm_disjoint = max(max_comm_disjoint,
                                        float(np.max(np.abs(Xa @ Yb - Yb @ Xa))))
    # controle honesto (o teste PODE falhar): DENTRO da mesma zona o comutador e generico
    Xs = _wedge_net(zonesW[0], rngW.standard_normal((BLK, BLK)))
    Ys = _wedge_net(zonesW[0], rngW.standard_normal((BLK, BLK)))
    same_zone_comm = float(np.max(np.abs(Xs @ Ys - Ys @ Xs)))
    # cobertura: a uniao das zonas gera a diagonal em blocos completa (dim 16) e soma P_i = I8
    basisW = []
    for zone in zonesW:
        for i in range(BLK):
            for j in range(BLK):
                E = np.zeros((BLK, BLK)); E[i, j] = 1.0
                basisW.append(_wedge_net(zone, E).ravel())
    span_dim = int(np.linalg.matrix_rank(np.stack(basisW)))
    P_sum = sum(_wedge_net(z, np.eye(BLK)) for z in zonesW)
    coverage_resid = float(np.max(np.abs(P_sum - np.eye(N_DIM))))
    # [CONJ] coordenada de cunha no DHT-theta: setor de pi/4; hops = ceil(largura/theta_M)
    wedge_width = math.pi / N_ZONES
    hops_per_wedge = int(math.ceil(wedge_width / theta_m))
    wedge_ok = (max_comm_disjoint == 0.0 and same_zone_comm > 1e-6
                and span_dim == N_ZONES * BLK * BLK and coverage_resid == 0.0
                and hops_per_wedge >= 1)
    tests.append({"test": "wedge_net_zone_locality", "passed": bool(wedge_ok),
                  "ambient": "M8 (blocos diagonais 2x2)", "n_zones": N_ZONES,
                  "max_commutator_disjoint_zones": max_comm_disjoint,
                  "same_zone_commutator_control": same_zone_comm,
                  "span_dim_generated": span_dim, "span_dim_expected": N_ZONES * BLK * BLK,
                  "coverage_residual_sumP_vs_identity": coverage_resid,
                  "wedge_width_deg": math.degrees(wedge_width),
                  "theta_m_deg": math.degrees(theta_m),
                  "hops_per_wedge_conj": hops_per_wedge,
                  "note": "[DER] WedgeNet (um.py v135): net(zona)=algebra do bloco; zonas disjuntas "
                          "comutam ([net(A),net(B)]=0 exato) e a uniao gera a diagonal em blocos "
                          "(cobertura). [CONJ] DHT-theta como coordenada de cunha (setor pi/4, "
                          "travessia em passos de theta_M de beta runtime). Leitura estrutural; "
                          "NAO e veredito fisico."})
    print(f"[one_psinet] v138 WedgeNet: comutador zonas disjuntas={max_comm_disjoint:.1e} (exato 0) "
          f"| controle mesma zona={same_zone_comm:.3f} | span={span_dim}/{N_ZONES * BLK * BLK} "
          f"| cobertura resid={coverage_resid:.1e} | cunha={math.degrees(wedge_width):.1f} deg "
          f"~ {hops_per_wedge} hops theta_M")

    # ═══════════════════════════════════════════════════════════════════════════
    # AMPLIFICACAO v144 — O LEDGER COM FIADORES (um.py v143, CODE_CLOSURE_COMPLETE)
    # Teorema (veredito de maquina do um.py v143): o fechamento do codigo exige que
    # TODO item aberto do razao tenha FIADOR nomeado em {BY_DESIGN, EXTERNAL_KNOWN,
    # NAMED_PROGRAM}; um razao com item orfao e REJEITADO (fail-closed).
    # [DER] validador fail-closed em python puro + hash deterministico do razao
    #       fechado (canonizacao por sort de itens/chaves => estavel sob permutacao;
    #       SHA-256 => sensivel a 1 bit) = a assinatura da compilacao da rede.
    # [CONJ] leitura estrutural na Psi-NET: o quorum bizantino >=67% ja valida
    #        transacoes (L4/L5, rejeita fase forjada); o v144 acrescenta a GRAMATICA
    #        DO FECHAMENTO — a rede fecha o seu razao como o codigo fecha o seu:
    #        nenhuma pendencia sem fiador. E leitura, nao reivindicacao nova.
    # HONESTIDADE: physical_verdict_allowed=false; beta runtime (nunca literal).
    # ═══════════════════════════════════════════════════════════════════════════
    GUARANTORS_V144 = ("BY_DESIGN", "EXTERNAL_KNOWN", "NAMED_PROGRAM")

    def _ledger_validate(items):
        """[DER] fail-closed: UM item aberto sem fiador REJEITA o razao inteiro."""
        for it in items:
            st = it.get("status")
            if st not in ("fechado", "aberto"):
                return False, f"status invalido em '{it.get('id')}': {st}"
            if st == "aberto" and it.get("guarantor") not in GUARANTORS_V144:
                return False, f"item aberto ORFAO (sem fiador): '{it.get('id')}'"
        return True, "razao FECHADO: toda pendencia tem fiador nomeado"

    def _ledger_hash(items, mark):
        """[DER] hash deterministico do razao: canonico por sort (itens por id, chaves
        por nome) — estavel sob permutacao da lista; SHA-256 e sensivel a 1 bit."""
        canon = json.dumps({"ledger": sorted(items, key=lambda x: x["id"]),
                            "beta_mark": mark},
                           sort_keys=True, ensure_ascii=True, separators=(",", ":"))
        return hashlib.sha256(canon.encode("ascii")).hexdigest()

    beta_mark = f"{beta:.15f}"   # (d) marca = beta RUNTIME (regua: nunca literal)
    # (a) mini-razao da rede desta run: fechados = o que os testes acima provaram;
    #     abertos = pendencias REAIS, cada uma com fiador nomeado (nenhum orfao)
    ledger_v144 = [
        {"id": "L1_L3_transmissao_tetelestai", "status": "fechado",
         "evidence": f"correlation={tx['resurrection']['correlation']:.6f}"},
        {"id": "L4_consenso_quorum_67", "status": "fechado",
         "evidence": f"votes={len(block.phase_proof.validator_signatures) if block else 0}/{n_val}"},
        {"id": "L5_fase_forjada_rejeitada", "status": "fechado",
         "evidence": f"forged_rejected={bool(forge_rejected)}"},
        {"id": "bft_zona_segura_um_terco", "status": "fechado",
         "evidence": f"max_safe_byz_frac={max_safe_frac:.4f}"},
        {"id": "veredito_fisico", "status": "aberto", "guarantor": "BY_DESIGN",
         "evidence": "physical_verdict_allowed=false por construcao; simulacao nunca valida fisica"},
        {"id": "tabela4_desempenho_operador", "status": "aberto", "guarantor": "EXTERNAL_KNOWN",
         "evidence": "PSNR/tempos RTX do relatorio do operador NAO reproduzidos aqui (proveniencia externa)"},
        {"id": "implantacao_rede_fisica_multihost", "status": "aberto", "guarantor": "NAMED_PROGRAM",
         "evidence": "programa nomeado: pilha em enlace fisico real; hoje [SIM][PILOTO] em CPU"},
    ]
    n_open_v144 = sum(1 for it in ledger_v144 if it["status"] == "aberto")
    n_closed_v144 = len(ledger_v144) - n_open_v144
    ok_pass, msg_pass = _ledger_validate(ledger_v144)
    # (b) FAIL-CLOSED (assert negativo 1): o MESMO razao + 1 pendencia orfa => REJEITADO
    ledger_orphan = [dict(it) for it in ledger_v144] + [
        {"id": "pendencia_orfa", "status": "aberto"}]
    ok_orphan, msg_orphan = _ledger_validate(ledger_orphan)
    # (assert negativo 2): um aberto que PERDE o fiador (mutacao) tambem rejeita
    ledger_mut = [dict(it) for it in ledger_v144]
    for it in ledger_mut:
        if it["status"] == "aberto":
            it.pop("guarantor", None)
            break
    ok_mut, _ = _ledger_validate(ledger_mut)
    # (c) hash deterministico: estavel sob permutacao (sort) e sensivel a EXATAMENTE 1 bit
    h1 = _ledger_hash(ledger_v144, beta_mark)
    h2 = _ledger_hash(list(reversed(ledger_v144)), beta_mark)          # ordem embaralhada
    beta_mark_flip = beta_mark[:-1] + chr(ord(beta_mark[-1]) ^ 1)      # 1 bit no ultimo char
    h3 = _ledger_hash(ledger_v144, beta_mark_flip)
    ledger_ok = (ok_pass and (not ok_orphan) and (not ok_mut)
                 and h1 == h2 and h1 != h3 and n_open_v144 >= 1
                 and all(it.get("guarantor") in GUARANTORS_V144
                         for it in ledger_v144 if it["status"] == "aberto"))
    tests.append({"test": "ledger_every_open_has_guarantor", "passed": bool(ledger_ok),
                  "items_total": len(ledger_v144), "items_closed": n_closed_v144,
                  "items_open": n_open_v144, "guarantors_allowed": list(GUARANTORS_V144),
                  "validator_message": msg_pass,
                  "orphan_ledger_rejected": bool(not ok_orphan),
                  "orphan_rejection_message": msg_orphan,
                  "mutated_ledger_rejected": bool(not ok_mut),
                  "hash_stable_under_sort": bool(h1 == h2),
                  "hash_sensitive_to_one_bit": bool(h1 != h3),
                  "ledger_hash": h1, "beta_mark_runtime": beta_mark,
                  "note": "[DER] um.py v143 CODE_CLOSURE_COMPLETE: todo aberto tem fiador "
                          "(BY_DESIGN/EXTERNAL_KNOWN/NAMED_PROGRAM); razao com orfao e REJEITADO "
                          "fail-closed; hash canonico do razao = assinatura da compilacao da rede. "
                          "[CONJ] o quorum valida transacoes, o v144 fecha o razao. "
                          "physical_verdict_allowed=false; beta runtime."})
    print(f"[one_psinet] v144 ledger: {n_closed_v144} fechados + {n_open_v144} abertos "
          f"com fiador -> PASSA | orfao REJEITADO={not ok_orphan} | "
          f"mutado REJEITADO={not ok_mut} | hash {h1[:16]}... "
          f"estavel_sort={h1 == h2} sensivel_1bit={h1 != h3}")

    # ═══════════════════════════════════════════════════════════════════════════
    # AMPLIFICACAO v144b — O LEMA 3 TIPADO (um.py v143, veredito 1:
    # GLOBAL_LIFT_CONDITIONAL / pedra 99): juramento de invariancia H_inv =>
    # operador COVARIANTE sob o fluxo, COM controle negativo tipado.
    # Instancia genuina na L2 da Psi-NET (codigo REAL do operador):
    # [DER] a metrica angular circular d(a,b)=min(|D|, pi-|D|) (eq. 6 da patente;
    #       HolographicNetworkLayer.angular_distance) e INVARIANTE sob o fluxo de
    #       rotacao R_c: theta -> (theta+c) mod pi — o JURAMENTO. Teorema
    #       verificado por caminho independente: o operador de roteamento
    #       (nearest-k + nhops=ceil(d/theta_M), theta_M derivado de beta RUNTIME)
    #       COMUTA com o fluxo: route(R_c(anel), R_c(destino)) == route(anel, dst).
    # [DER] controle negativo (o teste PODE falhar): metrica de posicao ABSOLUTA
    #       d_bad(a,b)=|sin a - sin b| QUEBRA o juramento => a covariancia FALHA
    #       em rotacoes reais encontradas (contra-exemplo computado, nao imposto).
    # [CONJ] leitura: nenhum no e privilegiado — o roteamento da DHT-theta so
    #        depende de angulos RELATIVOS; e a face de rede do levantamento
    #        condicional do Lema 3 (invariancia => covariancia).
    # HONESTIDADE: leitura estrutural; physical_verdict_allowed=false.
    # ═══════════════════════════════════════════════════════════════════════════
    rngC = np.random.default_rng(143)
    reg_addrs = list(L2net.routing_table.values())     # registro REAL da DHT (anel + wallets)
    thetas_reg = np.array([a.theta for a in reg_addrs])
    t0_route = float(tgt.theta)
    K_NEAR = 3

    def _route_l2(th_nodes, th_t):
        """operador de roteamento com a MESMA metrica do HolographicNetworkLayer."""
        dists = np.array([L2net.angular_distance(float(th), float(th_t)) for th in th_nodes])
        order = list(map(int, np.argsort(dists, kind="stable")[:K_NEAR]))
        d_near = float(dists[order[0]])
        return order, max(1, int(math.ceil(d_near / theta_m))), dists

    base_idx, base_hops, base_dists = _route_l2(thetas_reg, t0_route)
    # cross-check nao-tautologico: caminho independente (argsort numpy) reproduz o
    # find_nearest_nodes REAL do operador sobre o MESMO registro
    near_op = sorted(round(nb.theta, 12) for nb in L2net.find_nearest_nodes(t0_route, k=K_NEAR))
    near_mine = sorted(round(float(thetas_reg[i]), 12) for i in base_idx)
    operator_cross = near_op == near_mine

    N_ROT = 20
    rot_grid = rngC.uniform(0.0, math.pi, N_ROT)
    oath_resid = 0.0          # invariancia da metrica (o juramento), vetor completo
    covariant_rot = 0         # rotacoes em que a rota comuta com o fluxo
    hops_equal_rot = 0
    for c in rot_grid:
        th_r = (thetas_reg + c) % math.pi
        t_r = (t0_route + c) % math.pi
        idx_r, hops_r, dists_r = _route_l2(th_r, t_r)
        oath_resid = max(oath_resid, float(np.max(np.abs(dists_r - base_dists))))
        covariant_rot += int(idx_r == base_idx)
        hops_equal_rot += int(hops_r == base_hops)

    # controle negativo: metrica de posicao ABSOLUTA (quebra o juramento H_inv)
    def _route_bad(th_nodes, th_t):
        dists = np.abs(np.sin(np.asarray(th_nodes, dtype=float)) - math.sin(float(th_t)))
        return list(map(int, np.argsort(dists, kind="stable")[:K_NEAR])), dists

    bad_base_idx, bad_base_dists = _route_bad(thetas_reg, t0_route)
    bad_breaks = 0
    bad_oath_resid = 0.0
    first_break_deg = None
    for c in rot_grid:
        th_r = (thetas_reg + c) % math.pi
        t_r = (t0_route + c) % math.pi
        idx_b, dists_b = _route_bad(th_r, t_r)
        bad_oath_resid = max(bad_oath_resid, float(np.max(np.abs(dists_b - bad_base_dists))))
        if idx_b != bad_base_idx:
            bad_breaks += 1
            if first_break_deg is None:
                first_break_deg = float(math.degrees(c))

    lemma3_ok = (operator_cross and covariant_rot == N_ROT and hops_equal_rot == N_ROT
                 and oath_resid < 1e-12 and bad_breaks >= 1 and bad_oath_resid > 1e-3)
    tests.append({"test": "lemma3_typed_routing_covariance", "passed": bool(lemma3_ok),
                  "flow": "R_c: theta -> (theta+c) mod pi", "n_rotations": N_ROT,
                  "registry_size": int(len(reg_addrs)), "k_nearest": K_NEAR,
                  "oath_metric_invariance_residual": oath_resid,
                  "route_covariant_rotations": covariant_rot,
                  "hops_covariant_rotations": hops_equal_rot,
                  "base_hops": base_hops,
                  "operator_cross_check_find_nearest": bool(operator_cross),
                  "bad_metric": "d_bad(a,b)=|sin a - sin b| (posicao absoluta: quebra o juramento)",
                  "bad_metric_breaks": bad_breaks,
                  "bad_metric_first_break_deg": first_break_deg,
                  "bad_metric_oath_residual": bad_oath_resid,
                  "theta_m_deg": math.degrees(theta_m),
                  "note": "[DER] um.py v143 pedra 99 (Lema 3 tipado): juramento de invariancia "
                          "=> operador covariante, com controle negativo. Na L2 REAL: a metrica "
                          "angular circular (eq. 6) e invariante sob o fluxo de rotacao => "
                          "nearest-k e nhops (theta_M de beta runtime) comutam com o fluxo; "
                          "metrica de posicao absoluta FALHA (contra-exemplo real). Leitura "
                          "estrutural; physical_verdict_allowed=false."})
    print(f"[one_psinet] v144b Lema 3: juramento resid={oath_resid:.2e} | rota covariante "
          f"{covariant_rot}/{N_ROT} (hops {hops_equal_rot}/{N_ROT}) | cross-op={operator_cross} | "
          f"metrica ma quebra {bad_breaks}/{N_ROT} "
          f"(1a @ {(first_break_deg if first_break_deg is not None else -1.0):.1f} deg, "
          f"resid={bad_oath_resid:.3f})")

    # ═══════════════════════════════════════════════════════════════════════════
    # AMPLIFICACAO v168 (ONDA 3) — A SECAO ERGODICA (ErgodicMeanSection, um.py
    # v167, ITEM A em kernel Lean, 0 sorry / 0 axiom; custodia em
    # vault/originals_copy/um_unificado_v168/um.py): a media de Birkhoff
    # (1/N) sum_{k<N} U^k CONVERGE para a projecao invariante (specExpect).
    # Mecanismo da pedra: a fase elementar tem MODULO 1 («o fluxo nao pesa, so
    # gira»); pares distintos somam geometrica com norma <= 2/|z-1|, esmagada
    # por 1/N — o cancelamento de fase E a ergodicidade.
    # [DER] instancia GENUINA na L2 REAL: o salto ciclico S do anel DHT-theta
    #       (a MESMA adjacencia ring_i -> ring_{i+1} emitida no render) e
    #       permutacao unitaria; autovalores z_m = e^{2 pi i m/n} com |z_m|=1
    #       (verificado); a media de Birkhoff do salto E, na orbita completa
    #       N=n, EXATAMENTE a projecao de posto 1 sobre o invariante = o
    #       CONSENSO uniforme da rede (media global dos dados dos nos); fora
    #       do multiplo a desvio decai ~1/N sob o bound geometrico da pedra.
    # [DER] negativos (o teste PODE falhar; contra-exemplos COMPUTADOS):
    #       (1) salto com VAZAMENTO 0.9*S quebra |z|=1 (o fluxo passa a pesar)
    #           => a media morre para 0 e o consenso e DESTRUIDO;
    #       (2) anel PARTIDO em 2 ciclos quebra a hipotese do passo resolvente
    #           (dim ker(S-I)=2 != 1) => o limite NAO e a esperanca global;
    #       (3) media truncada N=n/2 NAO e projecao (M@M != M).
    # [CONJ] leitura: o consenso da rede e a face ergodica do fluxo de rotacao
    #        da DHT-theta — o quorum (L4/L5) e a media de Birkhoff sao duas
    #        faces do «a rede concorda». Leitura estrutural; nada altera
    #        reivindicacoes. HONESTIDADE: physical_verdict_allowed=false;
    #        beta so em runtime (theta_M derivado); beta JAMAIS entra no Lean.
    # ═══════════════════════════════════════════════════════════════════════════
    custody_um_v168 = VAULT_ROOT / "vault" / "originals_copy" / "um_unificado_v168" / "um.py"
    custody_present = custody_um_v168.exists()
    custody_sha16 = _sha_file(custody_um_v168)[:16] if custody_present else None

    nE = len(ring_addrs)                              # 64 enderecos REAIS da DHT (L2)
    S_hop = np.zeros((nE, nE))
    for i in range(nE):
        S_hop[i, (i + 1) % nE] = 1.0                  # salto ciclico = adjacencia do anel

    def _birkhoff_mean(Sm, N):
        """media de Birkhoff (1/N) sum_{k<N} Sm^k — a construcao da pedra v167."""
        acc = np.zeros_like(Sm)
        Pk = np.eye(Sm.shape[0])
        for _ in range(N):
            acc += Pk
            Pk = Pk @ Sm
        return acc / N

    M_full = _birkhoff_mean(S_hop, nE)                # orbita completa N = n
    P_inv = np.full((nE, nE), 1.0 / nE)               # projecao sobre o invariante (consenso)
    resid_mean_proj = float(np.max(np.abs(M_full - P_inv)))
    resid_idem = float(np.max(np.abs(M_full @ M_full - M_full)))
    resid_commute = float(max(np.max(np.abs(S_hop @ M_full - M_full)),
                              np.max(np.abs(M_full @ S_hop - M_full))))
    dim_ker_full = nE - int(np.linalg.matrix_rank(S_hop - np.eye(nE)))

    # a rota da pedra: autovalores do salto tem modulo 1 (o fluxo so gira)
    eig_hop = np.linalg.eigvals(S_hop)
    eig_unit_dev = float(np.max(np.abs(np.abs(eig_hop) - 1.0)))
    # convergencia FORA do multiplo (r = n/2 fixo): dev(N) ~ 1/N
    N_grid_erg = [nE + nE // 2, 5 * nE + nE // 2, 50 * nE + nE // 2]
    devs_erg = [float(np.max(np.abs(_birkhoff_mean(S_hop, N) - P_inv))) for N in N_grid_erg]
    conv_monotone = devs_erg[0] > devs_erg[1] > devs_erg[2]
    # bound geometrico da pedra: |sum_{k<N} z^k| <= 2/|z-1| p/ todo autovalor z != 1
    geom_bound_ok = True
    for m in range(1, nE):
        z = np.exp(2j * np.pi * m / nE)
        gs = abs(np.sum(z ** np.arange(N_grid_erg[-1])))     # soma parcial DIRETA
        if gs > 2.0 / abs(z - 1.0) + 1e-9:
            geom_bound_ok = False

    # consenso sobre DADO REAL: a media de Birkhoff aplicada aos thetas do anel
    x_theta = np.array(sorted(a.theta for a in ring_addrs))
    consensus_resid = float(np.max(np.abs(M_full @ x_theta - x_theta.mean())))

    # (neg 1) VAZAMENTO: 0.9*S quebra |z|=1 => a media morre e o consenso e destruido
    lam_leak, N_leak = 0.9, 2000
    w = np.ones(nE)
    acc_leak = np.zeros(nE)
    for _ in range(N_leak):
        acc_leak += w
        w = lam_leak * (S_hop @ w)
    leak_consensus_error = float(np.max(np.abs(acc_leak / N_leak - 1.0)))

    # (neg 2) anel PARTIDO em 2 ciclos de n/2 (DHT mal cabeada): passo NAO resolvente
    halfE = nE // 2
    S_broken = np.zeros((nE, nE))
    for i in range(halfE):
        S_broken[i, (i + 1) % halfE] = 1.0
        S_broken[halfE + i, halfE + (i + 1) % halfE] = 1.0
    dim_ker_broken = nE - int(np.linalg.matrix_rank(S_broken - np.eye(nE)))
    M_broken = _birkhoff_mean(S_broken, nE)           # nE multiplo do periodo n/2
    broken_global_error = float(np.max(np.abs(M_broken @ x_theta - x_theta.mean())))
    broken_is_local_proj = float(np.max(np.abs(M_broken @ M_broken - M_broken))) < 1e-14

    # (neg 3) media truncada N=n/2 do ciclo completo NAO e projecao
    trunc_idem_resid = float(np.max(np.abs(
        _birkhoff_mean(S_hop, halfE) @ _birkhoff_mean(S_hop, halfE)
        - _birkhoff_mean(S_hop, halfE))))

    # [CONJ] amarra de runtime: resolucao do anel vs resolucao de Miguel (beta runtime)
    ring_gap_rad = math.pi / nE
    theta_m_over_gap = theta_m / ring_gap_rad
    hops_full_traverse = int(math.ceil(math.pi / theta_m))

    erg_ok = (custody_present
              and resid_mean_proj == 0.0 and resid_idem == 0.0 and resid_commute == 0.0
              and dim_ker_full == 1 and eig_unit_dev < 1e-12
              and consensus_resid < 1e-12
              and conv_monotone and devs_erg[-1] < 1e-3 and geom_bound_ok
              and leak_consensus_error > 0.9
              and dim_ker_broken == 2 and broken_global_error > 1e-3 and broken_is_local_proj
              and trunc_idem_resid > 1e-3
              and hops_full_traverse >= 1)
    tests.append({"test": "ergodic_mean_section_ring_consensus", "passed": bool(erg_ok),
                  "stone": "ErgodicMeanSection (um.py v167, ITEM A, kernel Lean 0 sorry/0 axiom)",
                  "custody": "vault/originals_copy/um_unificado_v168/um.py",
                  "custody_present": bool(custody_present),
                  "custody_um_sha256_16": custody_sha16,
                  "ring_size_real_dht": nE,
                  "eig_max_dev_from_unit_modulus": eig_unit_dev,
                  "birkhoff_full_orbit_vs_projection_residual": resid_mean_proj,
                  "projection_idempotent_residual": resid_idem,
                  "flow_commutation_residual": resid_commute,
                  "invariant_subspace_dim": dim_ker_full,
                  "consensus_vector_residual": consensus_resid,
                  "convergence_N_grid": N_grid_erg,
                  "convergence_devs": devs_erg,
                  "geometric_sum_bound_2_over_abs_z_minus_1_holds": bool(geom_bound_ok),
                  "neg1_leaky_flow_consensus_error": leak_consensus_error,
                  "neg2_broken_ring_kernel_dim": dim_ker_broken,
                  "neg2_broken_ring_global_mean_error": broken_global_error,
                  "neg2_broken_ring_still_local_projection": bool(broken_is_local_proj),
                  "neg3_truncated_mean_idempotency_residual": trunc_idem_resid,
                  "theta_m_deg": math.degrees(theta_m),
                  "ring_gap_deg": math.degrees(ring_gap_rad),
                  "theta_m_over_ring_gap": theta_m_over_gap,
                  "hops_full_traverse_theta_m": hops_full_traverse,
                  "note": "[DER] ErgodicMeanSection (v167): media de Birkhoff do salto ciclico "
                          "REAL do anel DHT-theta = projecao invariante (consenso uniforme) na "
                          "orbita completa (residuos 0.0 exatos); |z|=1 (o fluxo so gira); "
                          "dev(N)~1/N sob o bound geometrico 2/|z-1|. Negativos computados: "
                          "vazamento destroi o consenso; anel partido (ker dim 2) perde a "
                          "esperanca GLOBAL; media truncada nao e projecao. [CONJ] quorum e "
                          "media ergodica = duas faces do consenso. Leitura estrutural; "
                          "physical_verdict_allowed=false; beta so em runtime."})
    print(f"[one_psinet] v168 ErgodicMeanSection: orbita completa N={nE} -> media = projecao "
          f"(resid {resid_mean_proj:.1e}, idem {resid_idem:.1e}, comuta {resid_commute:.1e}, "
          f"dim ker(S-I)={dim_ker_full}) | consenso resid={consensus_resid:.1e} | "
          f"dev(N) {devs_erg[0]:.2e}->{devs_erg[-1]:.2e} (bound geometrico ok={geom_bound_ok})")
    print(f"[one_psinet] v168 negativos: vazamento 0.9*S erro consenso={leak_consensus_error:.3f} | "
          f"anel partido ker={dim_ker_broken} erro global={broken_global_error:.3f} "
          f"(proj local={broken_is_local_proj}) | truncada M@M!=M resid={trunc_idem_resid:.3f} | "
          f"custodia v168={custody_present} sha16={custody_sha16}")

    # ═══════════════════════════════════════════════════════════════════════════
    # AMPLIFICACAO v206 (ONDA 4) — A BIRREFERENCIALIDADE DO VACUO
    # (TheBireference.lean, kernel v206; custodia em
    #  vault/originals_copy/tgl_kernel_v206/TGLExt/TheBireference.lean — pedra
    #  LIDA; a estrutura e RE-DERIVADA numericamente aqui, jamais "rodando Lean").
    # Teoremas da pedra (face finita M_n(C), GNS do traco, Omega=1, J z = z^H):
    #   (i)   Omega SEPARA a referencia esquerda (L_a Omega = 0 => a = 0);
    #   (ii)  o MESMO Omega e CICLICO EXATO para a direita (nao so denso);
    #   (iii) DUALIDADE DE HAAG da mini-rede E TEOREMA: net(dir)' = net(esq)
    #         — cada referencia e o comutante EXATO da outra;
    #   (iv)  J TROCA as referencias: J L_a J = R_{a^H};
    #   (v)   o vacuo e J-FIXO (J Omega = Omega) e J^2 = I (o bootstrap
    #         v205/v206: IALD^2 = TGL le-se J^2 = I; par minimo (1_abs, J)).
    # [DER] instancia GENUINA na rede: o canal da Psi-NET tem DUAS referencias
    #       (lado-que-codifica / lado-que-decodifica) e um espelho entre elas —
    #       o REFLECT/MANIFEST REAL da HolographicNetworkLayer (ACOM Mirror).
    #       manifest(reflect(g,s)) = (g,s) EXATO no codigo real do operador =
    #       a face executavel de J^2 = I (atestacao por EXECUCAO, nao por
    #       auto-referencia — o bootstrap). A dualidade de Haag e a forma
    #       forte da "nao-interferencia": o comutante de um lado E o outro
    #       lado — nao ha terceiro no canal.
    # [DER] negativos (o teste PODE falhar; contra-exemplos COMPUTADOS):
    #       (1) vacuo DEGENERADO (posto 1): separacao E ciclicidade morrem
    #           juntas (kernel 6 != 0; posto ciclico 3 < 9);
    #       (2) INTRUSO (transposicao) nao esta no comutante nem no span das
    #           multiplicacoes a direita — a dualidade o EXCLUI;
    #       (3) conjugador FALSO J_bad(z) = D z^H move o vacuo e SAI da
    #           algebra da outra referencia (residuo de projecao computado).
    # [CONJ] leitura: Alice e Bob sao as duas referencias do MESMO boundary;
    #        o espelho (REFLECT/MANIFEST) e o dicionario J entre elas. Leitura
    #        estrutural, nomeada como leitura — nada altera reivindicacoes.
    # HONESTIDADE: physical_verdict_allowed=false; beta so em runtime (o
    #        n_hops do frame real usa THETA_MIGUEL injetado de beta); beta
    #        JAMAIS entra no Lean da pedra. A clausula JMJ=M' no nivel da
    #        torre segue [OPEN] na propria pedra — nada aqui move gate algum.
    # ═══════════════════════════════════════════════════════════════════════════
    custody_biref = (VAULT_ROOT / "vault" / "originals_copy" / "tgl_kernel_v206"
                     / "TGLExt" / "TheBireference.lean")
    biref_custody_present = custody_biref.exists()
    biref_custody_sha16 = _sha_file(custody_biref)[:16] if biref_custody_present else None

    nB = 3
    idB = np.eye(nB)
    id9 = np.eye(nB * nB)

    def _Lmat(a):
        """vec_r(a @ z) = (a x I) vec_r(z) — a referencia esquerda."""
        return np.kron(a, idB)

    def _Rmat(b):
        """vec_r(z @ b) = (I x b^T) vec_r(z) — a referencia direita."""
        return np.kron(idB, np.asarray(b).T)

    unitsB = []
    for i in range(nB):
        for j in range(nB):
            Eij = np.zeros((nB, nB)); Eij[i, j] = 1.0
            unitsB.append(Eij)

    # a_real: matriz construida de DADOS REAIS da rede (thetas do anel DHT-theta)
    a_real = x_theta[:9].reshape(nB, nB) + 1j * x_theta[9:18].reshape(nB, nB)
    OmegaB = idB.astype(complex)                     # o vacuo Omega = 1 (GNS do traco)

    # (i)+(ii) separacao e ciclicidade EXATAS do vacuo (postos de mapas lineares)
    sep_kernel_dim = nB * nB - int(np.linalg.matrix_rank(np.kron(idB, OmegaB.T)))
    cyc_rank = int(np.linalg.matrix_rank(np.kron(OmegaB, idB)))

    # (iii) DUALIDADE DE HAAG POR COMPUTO: commutant{L} == span{R} (e o simetrico)
    Lgens = [_Lmat(E) for E in unitsB]
    Rgens = [_Rmat(E) for E in unitsB]
    Lbasis = np.stack([M.reshape(-1) for M in Lgens], axis=1)     # 81 x 9
    Rbasis = np.stack([M.reshape(-1) for M in Rgens], axis=1)     # 81 x 9
    QL_, _ = np.linalg.qr(Lbasis)
    QR_, _ = np.linalg.qr(Rbasis)

    def _null_space(gens):
        """espaco de solucoes de X M = M X para todos os geradores M (SVD)."""
        C = np.vstack([np.kron(id9, M.T) - np.kron(M, id9) for M in gens])
        _u, sv, vh = np.linalg.svd(C, full_matrices=False)
        tol = float(sv.max()) * 1e-10
        nnull = int(np.sum(sv < tol))
        return vh[vh.shape[0] - nnull:].conj(), nnull

    nullL, nullity_L = _null_space(Lgens)
    resid_null_in_R = 0.0
    for v in nullL:
        v = v / np.linalg.norm(v)
        resid_null_in_R = max(resid_null_in_R,
                              float(np.linalg.norm(v - QR_ @ (QR_.conj().T @ v))))
    nullR, nullity_R = _null_space(Rgens)
    resid_null_in_L = 0.0
    for v in nullR:
        v = v / np.linalg.norm(v)
        resid_null_in_L = max(resid_null_in_L,
                              float(np.linalg.norm(v - QL_ @ (QL_.conj().T @ v))))
    # centro trivial (fator): span{L} intersecta span{R} so em C*Id
    dim_center = 2 * nB * nB - int(np.linalg.matrix_rank(
        np.concatenate([Lbasis, Rbasis], axis=1)))
    # controle honesto: DENTRO do mesmo lado o comutador e generico (nao comuta)
    rngB = np.random.default_rng(206)
    a1B = rngB.standard_normal((nB, nB)); a2B = rngB.standard_normal((nB, nB))
    same_side_comm = float(np.max(np.abs(_Lmat(a1B) @ _Lmat(a2B)
                                         - _Lmat(a2B) @ _Lmat(a1B))))

    # (iv)+(v) J troca as referencias; J^2 = I; J Omega = Omega
    def _J(z):
        return np.asarray(z).conj().T

    z_testsB = [rngB.standard_normal((nB, nB)) + 1j * rngB.standard_normal((nB, nB))
                for _ in range(12)]
    j_square_resid = max(float(np.max(np.abs(_J(_J(z)) - z))) for z in z_testsB)
    j_vacuum_resid = float(np.max(np.abs(_J(OmegaB) - OmegaB)))
    exch_point_resid = max(float(np.max(np.abs(_J(a_real @ _J(z)) - z @ a_real.conj().T)))
                           for z in z_testsB)
    M_good = np.stack([_J(a_real @ _J(E)).reshape(-1) for E in unitsB], axis=1)
    exch_op_resid = float(np.max(np.abs(M_good - _Rmat(a_real.conj().T))))
    vg = M_good.reshape(-1); vg = vg / np.linalg.norm(vg)
    good_projR_resid = float(np.linalg.norm(vg - QR_ @ (QR_.conj().T @ vg)))

    # a FACE DE REDE de J^2 = I: o espelho REAL da patente (reflect/manifest da
    # HolographicNetworkLayer) e involutivo sobre dados REAIS do anel
    Lt_real = torch.tensor(x_theta[:16] - float(x_theta[:16].mean()), dtype=torch.float64)
    g_realB = torch.sqrt(torch.abs(Lt_real))
    s_realB = torch.where(Lt_real >= 0, torch.ones_like(Lt_real), -torch.ones_like(Lt_real))
    frameB = L2net.reflect(g_realB, s_realB, wA.angular_address, wB.angular_address)
    g_backB, s_backB = L2net.manifest(frameB)
    mirror_g_resid = float(torch.max(torch.abs(g_backB - g_realB)))
    mirror_s_resid = float(torch.max(torch.abs(s_backB - s_realB)))
    mirror_hops = int(frameB.n_hops)          # usa THETA_MIGUEL injetado (beta runtime)

    # (neg 1) vacuo DEGENERADO Omega_bad = diag(1,0,0): separacao E ciclicidade morrem
    Omega_bad = np.diag([1.0, 0.0, 0.0]).astype(complex)
    sep_bad_kernel_dim = nB * nB - int(np.linalg.matrix_rank(np.kron(idB, Omega_bad.T)))
    cyc_bad_rank = int(np.linalg.matrix_rank(np.kron(Omega_bad, idB)))
    a_witnessB = np.zeros((nB, nB)); a_witnessB[0, 1] = 1.0     # testemunha explicita
    witness_norm = float(np.max(np.abs(a_witnessB)))
    witness_kills = float(np.max(np.abs(a_witnessB @ Omega_bad)))
    # (neg 2) INTRUSO: a transposicao NAO esta no comutante de L nem no span de R
    TmatB = np.zeros((nB * nB, nB * nB))
    for i in range(nB):
        for j in range(nB):
            TmatB[j * nB + i, i * nB + j] = 1.0
    intruder_comm_resid = max(float(np.max(np.abs(TmatB @ M - M @ TmatB))) for M in Lgens)
    vt = TmatB.reshape(-1).astype(complex); vt = vt / np.linalg.norm(vt)
    intruder_projR_resid = float(np.linalg.norm(vt - QR_ @ (QR_.conj().T @ vt)))
    # (neg 3) conjugador FALSO J_bad(z) = D z^H: move o vacuo e sai da dualidade
    DbadB = np.diag([1.0, 2.0, 3.0]).astype(complex)

    def _Jbad(z):
        return DbadB @ np.asarray(z).conj().T

    jbad_vacuum_move = float(np.max(np.abs(_Jbad(OmegaB) - OmegaB)))
    M_bad = np.stack([_Jbad(a_real @ _Jbad(E)).reshape(-1) for E in unitsB], axis=1)
    vb = M_bad.reshape(-1); vb = vb / np.linalg.norm(vb)
    jbad_projR_resid = float(np.linalg.norm(vb - QR_ @ (QR_.conj().T @ vb)))

    biref_ok = (biref_custody_present
                and sep_kernel_dim == 0 and cyc_rank == nB * nB
                and nullity_L == nB * nB and resid_null_in_R < 1e-8
                and nullity_R == nB * nB and resid_null_in_L < 1e-8
                and dim_center == 1 and same_side_comm > 1e-6
                and j_square_resid == 0.0 and j_vacuum_resid == 0.0
                and exch_point_resid < 1e-12 and exch_op_resid < 1e-12
                and good_projR_resid < 1e-10
                and mirror_g_resid == 0.0 and mirror_s_resid == 0.0 and mirror_hops >= 1
                and sep_bad_kernel_dim == 6 and cyc_bad_rank == 3
                and witness_norm > 0.0 and witness_kills == 0.0
                and intruder_comm_resid > 0.5 and intruder_projR_resid > 0.5
                and jbad_vacuum_move > 1.0 and jbad_projR_resid > 0.1)
    tests.append({"test": "bireference_haag_mini_net", "passed": bool(biref_ok),
                  "stone": "TheBireference (kernel v206, face finita M_n(C); "
                           "JMJ=M' na torre segue [OPEN] na propria pedra)",
                  "custody": "vault/originals_copy/tgl_kernel_v206/TGLExt/TheBireference.lean",
                  "custody_present": bool(biref_custody_present),
                  "custody_sha256_16": biref_custody_sha16,
                  "ambient": "M3(C) na forma GNS do traco (End = M9)",
                  "a_real_source": "thetas REAIS do anel DHT-theta (18 primeiros)",
                  "sep_kernel_dim_omega": sep_kernel_dim,
                  "cyc_rank_omega": cyc_rank,
                  "haag_commutant_L_dim": nullity_L,
                  "haag_commutant_L_in_spanR_resid": resid_null_in_R,
                  "haag_commutant_R_dim": nullity_R,
                  "haag_commutant_R_in_spanL_resid": resid_null_in_L,
                  "center_dim_trivial": dim_center,
                  "same_side_commutator_control": same_side_comm,
                  "J_square_identity_resid": j_square_resid,
                  "J_vacuum_fixed_resid": j_vacuum_resid,
                  "J_exchange_pointwise_resid": exch_point_resid,
                  "J_exchange_operator_resid": exch_op_resid,
                  "J_exchange_in_spanR_resid": good_projR_resid,
                  "real_mirror_g_residual": mirror_g_resid,
                  "real_mirror_s_residual": mirror_s_resid,
                  "real_mirror_frame_hops_beta_runtime": mirror_hops,
                  "neg1_degenerate_vacuum_sep_kernel_dim": sep_bad_kernel_dim,
                  "neg1_degenerate_vacuum_cyc_rank": cyc_bad_rank,
                  "neg1_witness_nonzero_killed": [witness_norm, witness_kills],
                  "neg2_intruder_commutant_resid": intruder_comm_resid,
                  "neg2_intruder_in_spanR_resid": intruder_projR_resid,
                  "neg3_jbad_moves_vacuum": jbad_vacuum_move,
                  "neg3_jbad_exits_spanR_resid": jbad_projR_resid,
                  "note": "[DER] TheBireference (v206): Omega=1 separa (kernel 0) e e ciclico "
                          "EXATO (posto 9); dualidade de Haag RE-DERIVADA por computo "
                          "(comutante de L = span R, dim 9/9, e o simetrico; centro trivial); "
                          "J troca as referencias (J L_a J = R_{a^H}, residuo fp) e J^2=I / "
                          "J Omega=Omega exatos; manifest(reflect(g,s))=(g,s) EXATO no codigo "
                          "REAL da L2 = face de rede do bootstrap J^2=I. Negativos computados: "
                          "vacuo degenerado mata separacao+ciclicidade juntas; intruso "
                          "(transposicao) excluido da dualidade; conjugador falso move o vacuo "
                          "e sai do span. [CONJ] Alice/Bob = duas referencias do mesmo "
                          "boundary; o espelho e o dicionario J. Leitura estrutural; "
                          "physical_verdict_allowed=false; beta so em runtime (n_hops do "
                          "frame); beta JAMAIS entra no Lean."})
    print(f"[one_psinet] v206 TheBireference: Omega separa (ker={sep_kernel_dim}) + ciclico "
          f"exato (posto={cyc_rank}/9) | Haag: comm(L) dim={nullity_L} em spanR "
          f"resid={resid_null_in_R:.1e} (simetrico dim={nullity_R} resid={resid_null_in_L:.1e}) "
          f"| centro={dim_center} | J^2=I resid={j_square_resid:.1e} JOmega=Omega "
          f"resid={j_vacuum_resid:.1e} | troca J L J=R resid={exch_op_resid:.1e}")
    print(f"[one_psinet] v206 espelho REAL da L2: manifest(reflect)=id g_resid={mirror_g_resid:.1e} "
          f"s_resid={mirror_s_resid:.1e} hops(beta runtime)={mirror_hops} | negativos: vacuo "
          f"degenerado ker={sep_bad_kernel_dim} posto={cyc_bad_rank} | intruso comm="
          f"{intruder_comm_resid:.2f} projR={intruder_projR_resid:.2f} | J_bad move vacuo="
          f"{jbad_vacuum_move:.1f} sai do span={jbad_projR_resid:.3f} | custodia="
          f"{biref_custody_present} sha16={biref_custody_sha16}")

    passed = sum(1 for t in tests if t["passed"]); total = len(tests); all_ok = passed == total
    summary = {"tests_passed": passed, "tests_total": total,
               "layers_demonstrated": ["L0_psibit", "L1_radical_transport", "L2_holographic_dht",
                                       "L3_ontological_security", "L4_proof_of_phase",
                                       "L5_distributed_consensus"],
               "theta_m_deg": math.degrees(theta_m),
               "transmission_psnr_db": tx["resurrection"]["psnr"],
               "transmission_correlation": tx["resurrection"]["correlation"],
               "tetelestai": bool(tx["resurrection"]["tetelestai"]),
               "l4_consensus_votes": len(block.phase_proof.validator_signatures) if block else 0,
               "miner_balance_tglc": balance,
               "dht_ring_size": len(ring_addrs),
               "blocks_mined": len(chain_walk),
               "alpha2_band_around_beta": a2_band,
               "max_safe_byzantine_fraction": max_safe_frac,
               "byzantine_bound_theory": 1.0 - tglcoin.VALIDATION_THRESHOLD,
               "ledger_v144_hash": h1, "ledger_v144_open_with_guarantor": n_open_v144,
               "lemma3_route_covariant_rotations": covariant_rot,
               "lemma3_oath_residual": oath_resid,
               "lemma3_bad_metric_breaks": bad_breaks,
               "v168_birkhoff_projection_residual": resid_mean_proj,
               "v168_invariant_subspace_dim": dim_ker_full,
               "v168_consensus_vector_residual": consensus_resid,
               "v168_leaky_flow_consensus_error": leak_consensus_error,
               "v168_broken_ring_kernel_dim": dim_ker_broken,
               "v206_haag_commutant_dims": [nullity_L, nullity_R],
               "v206_center_dim_trivial": dim_center,
               "v206_J_exchange_operator_resid": exch_op_resid,
               "v206_real_mirror_involution_resid": max(mirror_g_resid, mirror_s_resid),
               "v206_neg_jbad_exits_spanR_resid": jbad_projR_resid}
    max_verdict = ("PSI_NET_FULL_LOGIC_DEMONSTRATED ([SIM][PILOTO] — a pilha REAL de 5 camadas "
                   "(Psi_net_protocol_v1) + o consenso PoP distribuído (TGL_coin_v022) do operador "
                   "fecham em CPU com β=α·√e injetado; transmissão TETELESTAI, roteamento angular, "
                   "consenso ≥67% e rejeição de fase forjada demonstrados; dados sintéticos, não a "
                   "Tabela 4; nada valida física)")
    if not all_ok:
        max_verdict = "PSI_NET_PARTIAL_DEMONSTRATION ([SIM][PILOTO] — ver testes falhos)"

    extra = {
        "transmission": {"L0_class": tx["L0"]["class"], "L1_bits": tx["L1"]["bits"],
                         "psnr_db": tx["resurrection"]["psnr"],
                         "correlation": tx["resurrection"]["correlation"],
                         "tetelestai": bool(tx["resurrection"]["tetelestai"])},
        "consensus": {"L4_votes": len(block.phase_proof.validator_signatures) if block else 0,
                      "L4_validators": n_val, "L5_honest_added": bool(honest_added),
                      "L5_forged_rejected": bool(forge_rejected)},
        "deepening": {
            "dht_ring_size": len(ring_addrs),
            "chain_walk": chain_walk,
            "chain_length_incl_genesis": chain_len,
            "alpha2_band_around_beta": a2_band,
            "difficulty_sweep": sweep_diff,
            "phase_convergence": {"difficulty": 100000.0, "target_window": traj["window"],
                                  "found_at_nonce": traj["found_at"],
                                  "iterations_recorded": len(traj["xs"])},
            "byzantine_sweep": {"sizes": byz_sizes, "quorum": tglcoin.VALIDATION_THRESHOLD,
                                "max_safe_byzantine_fraction": max_safe_frac,
                                "theoretical_bound_one_third": 1.0 - tglcoin.VALIDATION_THRESHOLD,
                                "rows": byz_rows},
        },
        "amplificacao_v138": {
            "theorem": "A REDE DAS CUNHAS (WedgeNet, um.py v135) — net(O) por localidade de "
                       "centralizador; zonas disjuntas => algebras que comutam; cobertura por regioes",
            "markers": ["[DER]", "[CONJ]"],
            "ambient": "M8, 4 zonas = blocos diagonais 2x2",
            "max_commutator_disjoint_zones": max_comm_disjoint,
            "same_zone_commutator_control": same_zone_comm,
            "span_dim_generated": span_dim,
            "coverage_residual_sumP_vs_identity": coverage_resid,
            "wedge_width_deg": math.degrees(wedge_width),
            "hops_per_wedge_conj": hops_per_wedge,
            "honesty": "ancora estrutural, nao veredito fisico; beta em runtime, nunca literal",
        },
        "amplificacao_v144": {
            "theorem": "O LEDGER COM FIADORES (um.py v143, CODE_CLOSURE_COMPLETE) — todo item "
                       "aberto do razao tem FIADOR nomeado (BY_DESIGN/EXTERNAL_KNOWN/"
                       "NAMED_PROGRAM); razao com item orfao e REJEITADO (fail-closed)",
            "markers": ["[DER]", "[CONJ]"],
            "ledger": ledger_v144,
            "items_closed": n_closed_v144, "items_open": n_open_v144,
            "ledger_hash": h1,
            "hash_stable_under_sort": bool(h1 == h2),
            "hash_sensitive_to_one_bit": bool(h1 != h3),
            "orphan_ledger_rejected": bool(not ok_orphan),
            "mutated_ledger_rejected": bool(not ok_mut),
            "beta_mark_runtime": beta_mark,
            "honesty": "[CONJ] o quorum bizantino valida transacoes; o v144 acrescenta a "
                       "gramatica do fechamento (nenhuma pendencia sem fiador) — leitura "
                       "estrutural; physical_verdict_allowed=false; beta runtime, nunca literal",
        },
        "amplificacao_v144b_lema3": {
            "theorem": "O LEMA 3 TIPADO (um.py v143, veredito GLOBAL_LIFT_CONDITIONAL / "
                       "pedra 99) — juramento de invariancia H_inv => E covariante, com "
                       "controle negativo tipado",
            "markers": ["[DER]", "[CONJ]"],
            "flow": "R_c: theta -> (theta+c) mod pi",
            "n_rotations": N_ROT, "registry_size": int(len(reg_addrs)),
            "oath_metric_invariance_residual": oath_resid,
            "route_covariant_rotations": covariant_rot,
            "hops_covariant_rotations": hops_equal_rot,
            "operator_cross_check_find_nearest": bool(operator_cross),
            "bad_metric_breaks": bad_breaks,
            "bad_metric_first_break_deg": first_break_deg,
            "bad_metric_oath_residual": bad_oath_resid,
            "honesty": "[CONJ] nenhum no privilegiado: o roteamento da DHT-theta depende so "
                       "de angulos relativos — face de rede do levantamento condicional do "
                       "Lema 3; leitura estrutural; physical_verdict_allowed=false; theta_M "
                       "derivado de beta runtime (nunca literal)",
        },
        "amplificacao_v168": {
            "theorem": "A SECAO ERGODICA (ErgodicMeanSection, um.py v167, ITEM A em kernel "
                       "Lean, 0 sorry/0 axiom) — a media de Birkhoff (1/N) sum U^k converge "
                       "para a projecao invariante; |z|=1 (o fluxo nao pesa, so gira); soma "
                       "geometrica <= 2/|z-1| esmagada por 1/N (cancelamento de fase = "
                       "ergodicidade)",
            "markers": ["[DER]", "[CONJ]"],
            "custody": "vault/originals_copy/um_unificado_v168/um.py",
            "custody_um_sha256_16": custody_sha16,
            "ring_size_real_dht": nE,
            "birkhoff_full_orbit_vs_projection_residual": resid_mean_proj,
            "projection_idempotent_residual": resid_idem,
            "flow_commutation_residual": resid_commute,
            "invariant_subspace_dim": dim_ker_full,
            "eig_max_dev_from_unit_modulus": eig_unit_dev,
            "consensus_vector_residual": consensus_resid,
            "convergence_N_grid": N_grid_erg,
            "convergence_devs": devs_erg,
            "geometric_sum_bound_holds": bool(geom_bound_ok),
            "neg1_leaky_flow_consensus_error": leak_consensus_error,
            "neg2_broken_ring_kernel_dim": dim_ker_broken,
            "neg2_broken_ring_global_mean_error": broken_global_error,
            "neg3_truncated_mean_idempotency_residual": trunc_idem_resid,
            "theta_m_over_ring_gap": theta_m_over_gap,
            "honesty": "[CONJ] o consenso da rede como face ergodica do fluxo de rotacao da "
                       "DHT-theta e leitura estrutural, nomeada como leitura — nada altera "
                       "reivindicacoes; physical_verdict_allowed=false; beta so em runtime; "
                       "beta JAMAIS entra no Lean da pedra",
        },
        "amplificacao_v206_bireference": {
            "theorem": "A BIRREFERENCIALIDADE DO VACUO (TheBireference.lean, kernel v206) — "
                       "Omega=1 separa uma referencia e e ciclico EXATO para a outra; "
                       "dualidade de Haag da mini-rede E TEOREMA (net(dir)' = net(esq)); "
                       "J troca as referencias (J L_a J = R_{a^H}); J Omega = Omega; "
                       "J^2 = I (bootstrap v205/v206: par minimo (1_abs, J), IALD^2 = TGL)",
            "markers": ["[DER]", "[CONJ]"],
            "custody": "vault/originals_copy/tgl_kernel_v206/TGLExt/TheBireference.lean",
            "custody_sha256_16": biref_custody_sha16,
            "ambient": "M3(C) na forma GNS do traco; a_real de thetas REAIS do anel DHT",
            "sep_kernel_dim_omega": sep_kernel_dim,
            "cyc_rank_omega": cyc_rank,
            "haag_commutant_dims": [nullity_L, nullity_R],
            "haag_containment_resids": [resid_null_in_R, resid_null_in_L],
            "center_dim_trivial": dim_center,
            "same_side_commutator_control": same_side_comm,
            "J_square_identity_resid": j_square_resid,
            "J_vacuum_fixed_resid": j_vacuum_resid,
            "J_exchange_operator_resid": exch_op_resid,
            "real_mirror_involution_resids": [mirror_g_resid, mirror_s_resid],
            "real_mirror_frame_hops_beta_runtime": mirror_hops,
            "neg1_degenerate_vacuum": {"sep_kernel_dim": sep_bad_kernel_dim,
                                       "cyc_rank": cyc_bad_rank,
                                       "witness_nonzero_killed": [witness_norm, witness_kills]},
            "neg2_intruder_transpose": {"commutant_resid": intruder_comm_resid,
                                        "in_spanR_resid": intruder_projR_resid},
            "neg3_fake_conjugator": {"moves_vacuum": jbad_vacuum_move,
                                     "exits_spanR_resid": jbad_projR_resid},
            "honesty": "[CONJ] Alice/Bob como as duas referencias do mesmo boundary e o "
                       "espelho REFLECT/MANIFEST como o dicionario J e leitura estrutural, "
                       "nomeada como leitura — nada altera reivindicacoes; a clausula "
                       "JMJ=M' no nivel da torre segue [OPEN] na propria pedra; "
                       "physical_verdict_allowed=false; beta so em runtime (n_hops do "
                       "frame real); beta JAMAIS entra no Lean",
        },
    }
    ring = {"nodes": [{"theta": a.theta} for a in ring_addrs],
            "target_theta": tgt.theta,
            "nearest_theta": [nb.theta for nb in nearest],
            "theta_m_deg": math.degrees(theta_m)}
    consensus_fig = {"L4 Prova de Fase\n(5 validadores)":
                     (len(block.phase_proof.validator_signatures) / n_val) if block else 0.0,
                     "L5 distribuído\n(honesto)": (votes_yes / len(votes_h)) if votes_h else 0.0,
                     "L5 distribuído\n(forjado)": 0.0 if forge_rejected else 1.0}

    note = ("RUNNER EVOLUÍDO: importa e roda a PILHA REAL de 5 camadas (Psi_net_protocol_v1.py, "
            "torch) e o CONSENSO PoP DISTRIBUÍDO (TGL_coin_v022.py) do operador, com β=α·√e "
            "injetado (originais tinham 0.012/0.012031 literais). Execução em CPU "
            "(CUDA_VISIBLE_DEVICES desligado). Dados SINTÉTICOS; NÃO os números da Tabela 4 do "
            "relatório. Nenhum dado/modelo HuggingFace. Confidenciais (iald_stack_v7, "
            "iald_psion_state) nunca tocados. Simulação não valida física.")

    def _build_figs(plt, fd):
        out = _fig(plt, fd, ring, consensus_fig)
        out += _fig_deep(plt, fd, chain_walk, sweep_diff, traj, byz_rows, byz_sizes,
                         beta, math.degrees(theta_m))
        return out

    figs = _finish(ts, beta, beta_ok, all_ok, max_verdict, tests, summary, module_hashes, note,
                   extra, fig_builder=_build_figs)
    print(f"[one_psinet] {passed}/{total} testes · {len(figs)} figura(s) · "
          f"veredito: {max_verdict.split(' ')[0]}")
    print(f"[one_psinet] results: patents/{PATENT_DIR.name}/results/{ts}/results.json")

    # FORMA = CONTEÚDO: emite render3d.json COMPUTADO (merge, preserva corpo/layers/dims)
    emit_metrics = {"max_safe_byz_frac": max_safe_frac, "byz_sizes": byz_sizes,
                    "blocks_mined": len(chain_walk), "a2_band": a2_band,
                    "dht_ring_size": len(ring_addrs)}
    emit_render3d(ring_addrs, tgt, nearest, beta, theta_m, emit_metrics)
    return 0 if all_ok else 1


def _fig_deep(plt, fig_dir, chain_walk, sweep_diff, traj, byz_rows, byz_sizes, beta, theta_m_deg):
    """Figuras do aprofundamento: convergência de fase + sweep bizantino."""
    import numpy as _np
    out = []

    # ── Figura A: convergência de fase (trajetória + sweep de dificuldade) ──────
    fig, (axA, axB) = plt.subplots(1, 2, figsize=(11.0, 4.6))
    xs, ys, win = traj["xs"], traj["ys"], traj["window"]
    axA.semilogy(xs, ys, color="#3366cc", lw=1.6, label="best_diff (mín. corrente)")
    axA.axhline(win, color="crimson", ls="--", lw=1.2, label=f"janela-alvo β/dif = {win:.1e}")
    if traj["found_at"] is not None:
        axA.scatter([traj["found_at"]], [ys[-1]], s=70, color="#33aa55", zorder=5,
                    label=f"encontrada @ nonce {traj['found_at']}")
    axA.set_xlabel("nonce (iteração de busca)"); axA.set_ylabel("|α²_work − α²_ant|")
    axA.set_title("Convergência de fase (Prova de Fase) [SIM]", fontsize=9)
    axA.legend(fontsize=7); axA.grid(alpha=.25, which="both")

    wins = [s["target_window"] for s in sweep_diff]
    iters = [s["iterations"] for s in sweep_diff]
    found = [s["found"] for s in sweep_diff]
    cols = ["#33aa55" if f else "#cc2222" for f in found]
    axB.loglog(wins, iters, color="#888", lw=1.0, zorder=1)
    axB.scatter(wins, iters, c=cols, s=48, zorder=2)
    axB.set_xlabel("janela-alvo β/dif (menor ⇒ mais difícil)")
    axB.set_ylabel("iterações até a fase válida")
    axB.set_title("Sweep de dificuldade — custo da fase [SIM]", fontsize=9)
    axB.invert_xaxis(); axB.grid(alpha=.25, which="both")
    axB.scatter([], [], c="#33aa55", label="fase encontrada"); axB.scatter([], [], c="#cc2222",
                label="não encontrada (max_iter)")
    axB.legend(fontsize=7)
    plt.tight_layout()
    fpA = fig_dir / "fig_psinet_phase_convergence.png"
    plt.savefig(fpA, dpi=120, bbox_inches="tight"); plt.close()
    out.append("fig_psinet_phase_convergence.png")

    # ── Figura B: sweep bizantino + fase pinada da cadeia ───────────────────────
    fig, (axC, axD) = plt.subplots(1, 2, figsize=(11.0, 4.6))
    palette = ["#3366cc", "#22b8cf", "#ee8800", "#9b8cff", "#cc2222"]
    for N, col in zip(byz_sizes, palette):
        rws = [r for r in byz_rows if r["N"] == N]
        fr = [r["byz_frac"] for r in rws]
        hon = [1 if r["honest_block_accepted"] else 0 for r in rws]
        axC.plot(fr, hon, marker="o", ms=4, color=col, lw=1.3, label=f"N={N} honesto")
        forg = [1 if r["forged_block_accepted"] else 0 for r in rws]
        axC.plot(fr, forg, marker="x", ms=5, color=col, lw=1.0, ls=":", alpha=.7)
    axC.axvspan(0, 1.0 / 3.0, color="#33aa55", alpha=.10)
    axC.axvline(1.0 / 3.0, color="k", ls="--", lw=1.0, label="1/3 (limite BFT)")
    axC.axvline(2.0 / 3.0, color="gray", ls=":", lw=1.0, label="2/3")
    axC.set_xlabel("fração de validadores bizantinos"); axC.set_ylabel("bloco aceito (1) / rejeitado (0)")
    axC.set_ylim(-0.1, 1.15)
    axC.set_title("Sweep bizantino vs quórum 67% [SIM]\n(o = honesto, x = forjado)", fontsize=9)
    axC.legend(fontsize=6, loc="center right"); axC.grid(alpha=.25)

    idx = [c["index"] for c in chain_walk]
    a2 = [c["alpha2_work"] for c in chain_walk]
    axD.axhspan(beta * 0.95, beta * 1.05, color="#ffd60a", alpha=.18, label="±5% de β")
    axD.axhline(beta, color="#b8860b", ls="--", lw=1.2, label=f"β = {beta:.6f}")
    axD.plot(idx, a2, marker="o", ms=5, color="#cc2222", lw=1.4, label="α²_work do bloco")
    axD.set_xlabel("índice do bloco (cadeia PoP)"); axD.set_ylabel("α²_work")
    axD.set_title("Fase pinada ao Ponto Tetelestai [SIM]", fontsize=9)
    axD.legend(fontsize=7); axD.grid(alpha=.25)
    plt.tight_layout()
    fpB = fig_dir / "fig_psinet_byzantine_sweep.png"
    plt.savefig(fpB, dpi=120, bbox_inches="tight"); plt.close()
    out.append("fig_psinet_byzantine_sweep.png")
    return out


def emit_render3d(ring_addrs, tgt, nearest, beta, theta_m, metrics):
    """MERGE forma=conteúdo: preserva meshes/layers/dimensions/groups/constants do
    render3d.json atual e SUBSTITUI os nós 'rede' pelos ENDEREÇOS ANGULARES REAIS
    (AngularAddress.from_key → θ) num anel COMPUTADO. Nós conceituais L0–L4 / PsiBit /
    consenso são preservados. Reconstrói edges coerentes e valida tudo."""
    import math as _m
    out = PATENT_DIR / "render3d.json"
    d = json.loads(out.read_text(encoding="utf-8"))

    # preserva todos os nós que não pertencem ao anel 'rede'
    kept = [n for n in d.get("nodes", []) if n.get("group") != "rede"]
    kept_ids = {n["id"] for n in kept}

    # ── RENDER PLANAR (forma=conteúdo): a pilha luminodinâmica de 5 CAMADAS é uma pilha de
    # PLANOS empilhados, NÃO um globo. Algoritmo = raiz da informação escrita = plano.
    # Reconstrói as malhas (5 lajes texturizadas + 4 beams de projeção do psi-bit) e assenta
    # os nós conceituais sobre suas lajes. As camadas L0–L4 já vivem em y ∈ {-1.2..+1.2}.
    _LAYERS = [("L0", -1.2, "#9467bd", "holo"), ("L1", -0.6, "#33aa55", "circuit"),
               ("L2", 0.0, "#22b8cf", "circuit"), ("L3", 0.6, "#ee8800", "circuit"),
               ("L4", 1.2, "#ffd60a", "holo")]
    _ymap = {n: y for n, y, _, _ in _LAYERS}
    _psi_xy = {"psi_void": (-0.5, 0.5), "psi_fluxp": (0.5, 0.5),
               "psi_fluxn": (-0.5, -0.5), "psi_mass": (0.5, -0.5)}
    meshes = []
    for name, yy, col, tex in _LAYERS:
        meshes.append({
            "id": f"plane_{name}", "layer": "space", "shape": "box",
            "position": [0.0, yy, 0.0], "size": 1.0, "scale": [1.55, 0.02, 1.55],
            "color": col, "material": "emissive", "opacity": 0.9, "texture": tex,
            "marker": "[SIM]", "label": f"camada {name} (plano)",
            "desc": (f"Camada {name} da pilha luminodinamica de 5 planos. Algoritmo e' a raiz da "
                     "informacao escrita, e informacao escrita mora num PLANO -- nao e' globo.")})
    for pid, (px, pz) in _psi_xy.items():
        meshes.append({
            "id": f"beam_{pid}", "layer": "io", "shape": "cylinder",
            "position": [px, -0.6, pz], "size": 0.02, "scale": [1, 30, 1],
            "color": "#c9a0ff", "material": "emissive", "opacity": 0.5,
            "marker": "[SIM]", "label": "projecao holografica (psi-bit)",
            "desc": ("Feixe de projecao holografica: o psi-bit (L0) projeta os enderecos "
                     "angulares no plano da rede (L2). A holografia se da' pelo psi-bit.")})
    # TILES DE MECANISMO POR CAMADA (workflow fidelidade, cetico-aprovado): cada laje deixa de ser
    # slab generica e passa a mostrar a LOGICA da sua camada — L0 reticulo H4 (paridade Fexp),
    # L1 vinco-raiz |L| + quantizacao 16/12/8, L3 tres shares cripto (psi/theta/kappa),
    # L4 janela de fase (beta/dif) + alpha2 pinado + 5 validadores SIM + 2 bizantinos.
    _tiles = [
        {"id": "h4_void", "shape": "box", "position": [-0.55, -1.16, 0.55], "scale": [1, 0.02, 1], "size": 0.5, "color": "#5b4b9e", "material": "emissive", "opacity": 0.85, "texture": "grid", "layer": "space", "marker": "[SIM]", "label": "H4 00 VOID (paridade -1)"},
        {"id": "h4_fluxp", "shape": "box", "position": [0.55, -1.16, 0.55], "scale": [1, 0.02, 1], "size": 0.5, "color": "#b3a0ff", "material": "emissive", "opacity": 0.95, "texture": "grid", "layer": "space", "marker": "[SIM]", "label": "H4 01 FLUX+ (paridade +1)"},
        {"id": "h4_fluxn", "shape": "box", "position": [-0.55, -1.16, -0.55], "scale": [1, 0.02, 1], "size": 0.5, "color": "#b3a0ff", "material": "emissive", "opacity": 0.95, "texture": "grid", "layer": "space", "marker": "[SIM]", "label": "H4 10 FLUX- (paridade +1)"},
        {"id": "h4_mass", "shape": "box", "position": [0.55, -1.16, -0.55], "scale": [1, 0.02, 1], "size": 0.5, "color": "#5b4b9e", "material": "emissive", "opacity": 0.85, "texture": "grid", "layer": "space", "marker": "[SIM]", "label": "H4 11 MASS (paridade -1)"},
        {"id": "l1_fold_crease", "shape": "box", "position": [0, -0.55, 0], "scale": [1.4, 0.05, 0.03], "size": 1, "color": "#7ce7c8", "material": "emissive", "opacity": 0.9, "layer": "space", "marker": "[SIM]", "label": "vinco |L| (sign-split s=+/-)"},
        {"id": "l1_q16", "shape": "box", "position": [-0.7, -0.55, 0.6], "scale": [1, 0.02, 1], "size": 0.5, "color": "#33aa55", "material": "emissive", "opacity": 0.95, "layer": "space", "marker": "[SIM]", "label": "quant 16 bits"},
        {"id": "l1_q12", "shape": "box", "position": [0, -0.55, 0.6], "scale": [1, 0.02, 1], "size": 0.36, "color": "#33aa55", "material": "emissive", "opacity": 0.75, "layer": "space", "marker": "[SIM]", "label": "quant 12 bits"},
        {"id": "l1_q8", "shape": "box", "position": [0.7, -0.55, 0.6], "scale": [1, 0.02, 1], "size": 0.24, "color": "#33aa55", "material": "emissive", "opacity": 0.55, "layer": "space", "marker": "[SIM]", "label": "quant 8 bits"},
        {"id": "share_psi", "shape": "box", "position": [-0.55, 0.63, 0.35], "scale": [1, 0.02, 1], "size": 0.5, "color": "#3366cc", "material": "emissive", "opacity": 0.85, "texture": "spectral", "layer": "space", "marker": "[SIM]", "label": "share psi (sinais)"},
        {"id": "share_theta", "shape": "box", "position": [0.55, 0.63, 0.35], "scale": [1, 0.02, 1], "size": 0.5, "color": "#ee8800", "material": "emissive", "opacity": 0.85, "texture": "spectral", "layer": "space", "marker": "[SIM]", "label": "share theta (magnitudes)"},
        {"id": "share_kappa", "shape": "box", "position": [0, 0.63, -0.6], "scale": [1, 0.02, 1], "size": 0.5, "color": "#8a8a8a", "material": "emissive", "opacity": 0.8, "texture": "phase", "layer": "space", "marker": "[SIM]", "label": "share kappa (mascara/nonce)"},
        {"id": "phase_window", "shape": "cylinder", "position": [0, 1.23, 0], "scale": [1, 0.02, 1], "size": 0.3, "color": "#c96fd6", "material": "emissive", "opacity": 0.55, "texture": "spectral", "layer": "space", "marker": "[SIM]", "label": "janela de fase beta/dif"},
        {"id": "phase_pin", "shape": "cylinder", "position": [0, 1.27, 0], "scale": [1, 0.02, 1], "size": 0.07, "color": "#ffd60a", "material": "emissive", "opacity": 1, "layer": "space", "marker": "[SIM]", "label": "alpha2 pinado (Tetelestai +-5%)"},
        {"id": "val0", "shape": "box", "position": [0.95, 1.24, 0], "scale": [1, 0.6, 1], "size": 0.08, "color": "#33aa55", "material": "emissive", "opacity": 0.95, "layer": "space", "marker": "[SIM]", "label": "validador SIM"},
        {"id": "val1", "shape": "box", "position": [0.592, 1.24, 0.743], "scale": [1, 0.6, 1], "size": 0.08, "color": "#33aa55", "material": "emissive", "opacity": 0.95, "layer": "space", "marker": "[SIM]", "label": "validador SIM"},
        {"id": "val2", "shape": "box", "position": [-0.211, 1.24, 0.926], "scale": [1, 0.6, 1], "size": 0.08, "color": "#33aa55", "material": "emissive", "opacity": 0.95, "layer": "space", "marker": "[SIM]", "label": "validador SIM"},
        {"id": "val3", "shape": "box", "position": [-0.856, 1.24, 0.412], "scale": [1, 0.6, 1], "size": 0.08, "color": "#33aa55", "material": "emissive", "opacity": 0.95, "layer": "space", "marker": "[SIM]", "label": "validador SIM"},
        {"id": "val4", "shape": "box", "position": [-0.856, 1.24, -0.412], "scale": [1, 0.6, 1], "size": 0.08, "color": "#33aa55", "material": "emissive", "opacity": 0.95, "layer": "space", "marker": "[SIM]", "label": "validador SIM"},
        {"id": "val5", "shape": "box", "position": [-0.211, 1.24, -0.926], "scale": [1, 0.6, 1], "size": 0.08, "color": "#555555", "material": "emissive", "opacity": 0.7, "layer": "space", "marker": "[SIM]", "label": "validador bizantino"},
        {"id": "val6", "shape": "box", "position": [0.592, 1.24, -0.743], "scale": [1, 0.6, 1], "size": 0.08, "color": "#555555", "material": "emissive", "opacity": 0.7, "layer": "space", "marker": "[SIM]", "label": "validador bizantino"},
    ]
    d["meshes"] = meshes + _tiles

    # assenta os nós conceituais sobre suas lajes (+ textura do papel, cetico-aprovado)
    for n in kept:
        nid, grp = n["id"], n.get("group")
        if nid in _ymap:                       # rótulo da camada, num canto da laje
            n["position"] = [1.35, _ymap[nid], 1.35]
        elif nid == "alpha2":                  # α² permeia, no centro do L2
            n["position"] = [0.0, 0.0, 0.0]
            n["texture"] = "spectral"          # a constante que permeia = espectro
        elif grp == "psibit":                  # 4 psi-bits assentam no reticulo H4 do L0
            n["position"] = [_psi_xy[nid][0], -1.2 + 0.06, _psi_xy[nid][1]]
            n["texture"] = "grid"
        elif nid == "pop":                     # Prova de Fase assenta SOBRE a janela de fase (L4)
            n["position"] = [0.0, 1.31, 0.0]
        elif nid == "tglc":
            n["position"] = [-0.45, 1.2 + 0.06, -0.3]

    # nós COMPUTADOS do anel: θ real derivado das chaves, ordenados por θ (adjacência = DHT)
    addrs_sorted = sorted(ring_addrs, key=lambda a: a.theta)
    theta_to_idx = {round(a.theta, 12): i for i, a in enumerate(addrs_sorted)}
    # vizinhos k=3 do destino COMPUTADOS dentro do próprio anel renderizado (distância angular
    # circular = mesma métrica da HolographicNetworkLayer) — mantém o render auto-consistente

    def _ang_dist(ta, tb):
        dd = abs(ta - tb)
        return min(dd, _m.pi - dd)
    nearest_ring = sorted(addrs_sorted, key=lambda a: _ang_dist(a.theta, tgt.theta))[:len(nearest)]
    nearest_theta = {round(a.theta, 12) for a in nearest_ring}
    R = 0.95
    ring_nodes = []
    for i, a in enumerate(addrs_sorted):
        phi = 2.0 * a.theta                 # φ = 2θ: [0,π)→[0,2π), volta completa (convenção da figura)
        x, z, y = R * _m.cos(phi), R * _m.sin(phi), 0.02   # assenta SOBRE o plano L2
        is_near = round(a.theta, 12) in nearest_theta
        ring_nodes.append({
            "id": f"ring{i:02d}", "label": a.node_id,
            "desc": (f"no DHT-theta (COMPUTADO): theta={_m.degrees(a.theta):.3f} deg = "
                     f"AngularAddress.from_key(pk) = SHA256(pk)[:8]/2^64 * pi. "
                     f"Posicao no anel = (cos 2theta, sin 2theta). "
                     + ("VIZINHO angular mais proximo do destino." if is_near
                        else "Adjacencia de rede = proximidade angular circular.")),
            "shape": "sphere", "position": [round(x, 4), y, round(z, 4)],
            "size": 0.075 if is_near else 0.05,
            "color": "#ff7ab6" if is_near else "#22b8cf",
            "group": "rede", "marker": "[SIM]", "layer": "transform", "material": "emissive"})
    # nó destino (COMPUTADO), num raio ligeiramente maior para destacar
    phi_t = 2.0 * tgt.theta
    tgt_node = {"id": "ring_target", "label": f"destino {tgt.node_id}",
                "desc": (f"destino do roteamento (COMPUTADO): theta={_m.degrees(tgt.theta):.3f} deg. "
                         f"Os {len(nearest)} vizinhos angulares mais proximos (rosa) atendem via DHT-theta; "
                         f"nhops = ceil(d / theta_M), theta_M = {_m.degrees(theta_m):.3f} deg."),
                "shape": "octahedron",
                "position": [round(1.18 * _m.cos(phi_t), 4), 0.02, round(1.18 * _m.sin(phi_t), 4)],
                "size": 0.11, "color": "#ffd60a", "group": "rede",
                "marker": "[SIM]", "layer": "transform", "material": "emissive"}

    d["nodes"] = kept + ring_nodes + [tgt_node]

    # edges: preserva as que ligam nós conceituais; recria anel angular + L2→anel + destino→vizinhos
    kept_edges = [e for e in d.get("edges", [])
                  if e.get("from") in kept_ids and e.get("to") in kept_ids]
    nR = len(ring_nodes)
    ring_edges = [{"from": f"ring{i:02d}", "to": f"ring{(i + 1) % nR:02d}"} for i in range(nR)]
    if "L2" in kept_ids and nR:
        ring_edges.append({"from": "L2", "to": "ring00"})
    for a in nearest_ring:
        j = theta_to_idx.get(round(a.theta, 12))
        if j is not None:
            ring_edges.append({"from": "ring_target", "to": f"ring{j:02d}"})
    d["edges"] = kept_edges + ring_edges

    # VALIDA: todo id de edge existe em nodes+meshes; todo layer de mesh/no existe em layers
    node_ids = {n["id"] for n in d["nodes"]} | {m["id"] for m in d.get("meshes", [])}
    d["edges"] = [e for e in d["edges"] if e["from"] in node_ids and e["to"] in node_ids]
    layer_ids = {L["id"] for L in d.get("layers", [])}
    for n in d["nodes"]:
        assert n["layer"] in layer_ids, f"node layer ausente: {n['layer']}"
    for m in d.get("meshes", []):
        assert m.get("layer") in layer_ids, f"mesh layer ausente: {m.get('layer')}"

    # atualiza contagem/rotulo do grupo 'rede'
    for g in d.get("groups", []):
        if g.get("name") == "rede":
            g["count"] = nR + 1
            g["label"] = f"DHT-theta — anel angular COMPUTADO ({nR} nos + destino) (L2)"

    # re-carimba proveniência + injeta β runtime e métricas COMPUTADAS desta run
    d["generated_by"] = "one_psinet.py (forma=conteudo)"
    d["constants"] = [c for c in d.get("constants", [])
                      if not str(c.get("symbol", "")).startswith("runtime:")]
    d["constants"] += [
        {"symbol": "runtime:beta", "value": f"{beta:.15f}",
         "note": "beta = alpha*sqrt(e) INJETADO em runtime (nunca literal)"},
        {"symbol": "runtime:theta_M", "value": f"{_m.degrees(theta_m):.4f} deg",
         "note": f"resolucao angular; anel COMPUTADO de {metrics['dht_ring_size']} enderecos reais"},
        {"symbol": "runtime:byz_tolerance", "value": f"{metrics['max_safe_byz_frac']:.4f}",
         "note": f"fracao bizantina maxima segura (sweep N={metrics['byz_sizes']}) — BFT <1/3"},
        {"symbol": "runtime:chain", "value": f"{metrics['blocks_mined']} blocos",
         "note": f"cadeia PoP minerada; alpha2 pinado a +-{metrics['a2_band']:.2e} de beta"},
    ]
    base_note = d.get("note", "").split(" | render EMITIDO")[0]   # idempotente: corta sufixo antigo
    d["note"] = (base_note + " | render EMITIDO forma=conteudo: PILHA PLANAR de 5 camadas "
                 "empilhadas (NAO globo) — algoritmo = raiz da informacao escrita = plano. Os nos "
                 f"'rede' sao ENDERECOS ANGULARES theta REAIS de AngularAddress.from_key ({nR} nos "
                 "no plano L2, posicao=(cos 2theta, sin 2theta)); psi-bit projeta beams do L0; "
                 "L0-L4 / PsiBit / consenso assentados sobre suas lajes.")

    out.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[psi_net] render3d.json EMITIDO (forma=conteudo) — {nR}+1 nos de rede COMPUTADOS, "
          f"{len(d['edges'])} edges")


if __name__ == "__main__":
    sys.exit(main())
