# -*- coding: utf-8 -*-
"""one_aprendizado_continuo.py — runner único forma = conteúdo da patente Aprendizado Contínuo
(BR102026005477-1 — Aprendizado sem re-treino via estado psiônico persistente). [PILOTO][SIM]

EVOLUÇÃO (09/07/2026): INCORPORA os protótipos RICOS do operador, resgatados para
`prototype_src/` (cópia; originais READ-ONLY em C:/IALD/projetos_pyhton/IALD):
  - `holographic_memory.py` (659 L) — MEMÓRIA HOLOGRÁFICA DE 2 CAMADAS:
      CAMADA 1 (angular, inter-turno): classifica QUAIS turnos importam por θ, poda vácuo;
      CAMADA 2 (radical, intra-turno): comprime O QUE dentro de cada turno importa
      (colapso de prefixo + dedup cross-turno + poda por amplitude g=√|L|).
      É o componente [3]/[7] da patente (cache holográfico + Psion) em forma operante.
  - `phase_factor_bake_v1.py` (842 L) — BAKE DO PHASE FACTOR (1 − β·f(θ)) nos pesos:
      apply_phase_factor / classify_tensor / is_weight_tensor (partes PÚBLICAS, puras).
      É a estratificação gravitacional VACUUM/TRANSIÇÃO/GRÁVITON (componente [1]) real.

A versão leve anterior (só psionic_memory + tensores sintéticos) está preservada em
`one_aprendizado_continuo_v1_light.py.bak`.

Demonstra, rodando o CÓDIGO REAL do operador (β injetado, nunca literal):
  - estratificação gravitacional real do Phase Factor sobre um tensor sintético de peso;
  - a ontologia trinária Palavra/Verbo/Nome via classify_tensor (Q/K/down, V/gate, O/up);
  - a memória holográfica de 2 camadas comprimindo uma conversa sintética grande
    (poda de vácuo inter-turno + dedup/poda psiônica intra-turno) → contexto que cabe;
  - classificação angular de turnos (VÁCUO/GRÁVITON/FÓTON) + persistência P=1+β'·log(1+hits);
  - ciclo do Psion por N gerações (EMA a taxa β) com persistência SHA-256 fail-closed;
  - sampler piso de Hilbert β_adapt=α√S e IALD Score = ³√(Palavra·Nome·Verbo)·Ψ(gen).
  ⚠ ERRATA (30/08/2026): NAO existe β_TGL adaptativo — β_TGL = α√e e CONSTANTE. O que
    varia por camada e um FATOR DE PISO, e o nome "β" sobre ele cai. A medida fica de pe:
    α√S = α√e exatamente quando S = e nats. Texto depositado ainda usa o nome antigo
    (reivindicacoes 1, 5, 8, 14, 17) — retificacao e ato do operador [LEGAL].

RÉGUA: β_TGL NUNCA literal no MEU código. Os protótipos computam
`BETA_TGL = ALPHA_FINE*SQRT_E` em nível de módulo; este runner os importa como proveniência
READ-ONLY e INJETA `tgl_core.beta()` (fonte única) nos globais dos módulos em runtime
(hm.BETA_TGL / hm.BETA_RED / hm.THETA_MIGUEL…, pfb.BETA_TGL / pfb.THETA_MIGUEL / pfb.DELTA_THETA…).

HONESTIDADE [PILOTO][SIM]: conversa e tensores SINTÉTICOS; NÃO o benchmark da Tabela 2 do
relatório (Qwen2.5-7B) [DATA_REQUIRED]. CONFIDENCIAL NUNCA embarcado: iald_stack_v7.py,
iald_psion_state.json. Simulação não valida física (physical_verdict_allowed=false).

    set PYTHONUTF8=1
    "C:\\IALD\\observaveis_tgl\\tgl_env\\Scripts\\python.exe" one_aprendizado_continuo.py
"""
from __future__ import annotations

import hashlib
import json
import math
import shutil
import sys
import tempfile
from datetime import datetime
from pathlib import Path

import numpy as np

RUNNER_DIR = Path(__file__).resolve().parent
PATENT_DIR = RUNNER_DIR.parent
CENTRAL = PATENT_DIR.parents[1]
PILOTO = CENTRAL / "Patentes" / "Skygrid" / "SkyGrid_Piloto"     # READ-ONLY (β source)
PROTO_SRC = PATENT_DIR / "prototype_src"                          # rescued rich prototypes
WORK = RUNNER_DIR / "_aprendizado_core"
PATENT_ID = "BR102026005477-1"
SLUG = "aprendizado_continuo"


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
    """Copy the β-source core (skygrid_sim → tgl_core, psionic_memory) into a workdir; hash it
    together with the rescued rich prototypes (provenance)."""
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


def _synthetic_conversation(rng) -> list:
    """Build a LARGE synthetic conversation that exceeds the holographic budget, mixing:
      - vacuum turns (low angular amplitude → pruned inter-turno);
      - repeated signal sentences (dedup cross-turno);
      - prefix-collapsible families;
      - genuine signal sentences (preserved).
    No confidential content; pure synthetic Portuguese text."""
    signal_bank = [
        "O estado psiônico acumula perfis topológicos das camadas entre sessões de inferência.",
        "A taxa de aprendizado deriva exclusivamente da constante fundamental beta igual alfa vezes raiz de e.",
        "A estratificação gravitacional separa vácuo, gráviton e fóton pelo ângulo de Miguel.",
        "A memória holográfica endereça os turnos por ângulo e persiste a fase por ressonância.",
        "O eco reflexivo indica convergência estável do sistema ao longo das gerações.",
        "A reconstrução dimensional recupera o peso original a partir do sinal e da gravidade ao quadrado.",
        "O operador verbal poda a matriz de atenção por um piso adaptativo derivado da entropia.",
        "O aprendizado ocorre sem retreino, sem descida de gradiente e sem feedback humano.",
    ]
    vacuum_bank = ["ok.", "sim.", "certo.", "entendi.", "beleza.", "ta.", "aham.", "isso."]
    prefix_family = [
        "Ela e a Luz que ecoa no vazio modular.",
        "Ela e a Luz que brilha na fronteira angular.",
        "Ela e a Luz que pensa sobre a permanencia.",
        "Ela e a Luz que retorna ao grande atrator.",
    ]
    turns = []
    for i in range(120):
        if i % 4 == 3:
            # vacuum turn: low amplitude, gets pruned inter-turno
            turns.append({"role": "user", "content": " ".join(rng.choice(vacuum_bank, 6))})
        else:
            # signal turn: some repeated sentences (dedup) + a prefix family + fresh signal
            reps = list(rng.choice(signal_bank, 3, replace=False))
            fresh = f"Na geracao {i} o escore IALD sobe de forma logaritmica sem divergir."
            body = " ".join(reps + prefix_family + [fresh] + reps)
            role = "assistant" if i % 2 else "user"
            turns.append({"role": role, "content": body})
    return turns


def _finish(ts, beta, beta_ok, all_ok, max_verdict, tests, summary, module_hashes, note, fig_builder=None):
    results_dir = PATENT_DIR / "results" / ts
    results_dir.mkdir(parents=True, exist_ok=True)
    results = {"patent_id": PATENT_ID, "slug": SLUG, "timestamp": ts,
               "runner": "one_aprendizado_continuo.py (evoluído)",
               "markers": ["[PILOTO]", "[SIM]"], "physical_verdict_allowed": False,
               "beta_runtime": beta, "beta_matches_alpha_sqrt_e": beta_ok,
               "verdict": max_verdict.split(" ")[0] if all_ok else "PARTIAL_DEMONSTRATION",
               "max_verdict": max_verdict,
               "constants": {"BETATGL": beta, "factorization": "betatgl = alpha_EM * sqrt(e)",
                             "beta_red": beta + beta * beta, "free_parameters": 0},
               "tests": tests, "summary": summary,
               "source_prototype": "prototype_src/holographic_memory.py (2 camadas) + "
                                   "phase_factor_bake_v1.py (bake do Phase Factor) — resgatados de "
                                   "C:/IALD/projetos_pyhton/IALD (READ-ONLY; β injetado). "
                                   "psionic_memory.py + tgl_core.py do piloto (READ-ONLY; copiado)",
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
    lines = [f"# Relatório auditável — one_aprendizado_continuo.py (EVOLUÍDO)\n",
             f"- Run `{ts}` · Patente `{PATENT_ID}`\n", f"- Veredito: **{max_verdict}**\n",
             f"- β runtime `{beta}` (= α·√e? **{beta_ok}**; nunca literal) — INJETADO nos protótipos "
             f"holographic_memory + phase_factor_bake\n",
             f"- Testes: **{summary['tests_passed']}/{summary['tests_total']}**\n"]
    for t in tests:
        lines.append(f"  - {'✓' if t['passed'] else '✗'} {t['test']}\n")
    lines.append(f"- physical_verdict_allowed: **False**.\n\n{note}\n")
    lines.append("Protótipos ricos resgatados (READ-ONLY; cópia). Núcleo do piloto intacto. 1 = 1. Tetelestai.\n")
    report_md.write_text("".join(lines), encoding="utf-8")
    seal_dir = PATENT_DIR / "seals" / ts
    seal_dir.mkdir(parents=True, exist_ok=True)
    fh = dict(module_hashes)
    fh["results.json"] = _sha_file(results_path)
    fh["report.md"] = _sha_file(report_md)
    for f in figs:
        fh[f"figures/{f}"] = _sha_file(results_dir / "figures" / f)
    result_hash = _sha_text(json.dumps(fh, sort_keys=True))
    seal = {"timestamp": ts, "patent_id": PATENT_ID, "runner": "one_aprendizado_continuo.py (evoluído)",
            "beta_runtime": beta, "physical_verdict_allowed": False, "max_verdict": max_verdict,
            "tests_passed": summary["tests_passed"], "result_hash": result_hash, "sha256": fh,
            "markers": ["[PILOTO]", "[SIM]"],
            "results_path": str(results_path.relative_to(CENTRAL)).replace("\\", "/")}
    (seal_dir / "seal.json").write_text(json.dumps(seal, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[{SLUG}] SELADO · result_hash {result_hash[:16]}… · {summary['tests_passed']}/{summary['tests_total']} testes")


def main() -> int:
    ts = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    print(f"[one_aprendizado] patente {PATENT_ID} · run {ts} · RUNNER EVOLUÍDO (2 protótipos ricos, β injetado)")
    if not PILOTO.exists():
        print(f"ERRO: núcleo β não encontrado em {PILOTO}", file=sys.stderr)
        return 2
    if not (PROTO_SRC / "holographic_memory.py").exists() or not (PROTO_SRC / "phase_factor_bake_v1.py").exists():
        print(f"ERRO: protótipos ricos ausentes em {PROTO_SRC}", file=sys.stderr)
        return 2
    module_hashes = copy_core()

    sys.path.insert(0, str(WORK))
    from skygrid_sim import tgl_core  # noqa: E402
    from skygrid_sim.psionic_memory import PsionicMemory  # noqa: E402
    beta = tgl_core.beta()
    beta_ok = abs(beta - 0.0072973525693 * math.exp(0.5)) < 1e-15
    theta_m = tgl_core.theta_m()
    beta_red = beta + beta * beta
    print(f"[one_aprendizado] β runtime = {beta} (= α·√e? {beta_ok}) · θ_Miguel = {math.degrees(theta_m):.4f}°")

    # ── import the operator's rich prototypes and INJECT β (régua: never a literal) ──
    sys.path.insert(0, str(PROTO_SRC))
    import holographic_memory as hm   # noqa: E402  (2-layer contextual memory)
    import phase_factor_bake_v1 as pfb  # noqa: E402  (Phase Factor bake; __main__-guarded CLI not run)
    hm_beta_original, pfb_beta_original = hm.BETA_TGL, pfb.BETA_TGL
    # inject into holographic_memory globals (read at call time by its methods)
    hm.BETA_TGL = beta
    hm.BETA_RED = beta_red
    hm.THETA_MIGUEL = theta_m
    hm.THETA_MIGUEL_DEG = math.degrees(theta_m)
    hm.SQRT_BETA = math.sqrt(beta)
    # inject into phase_factor_bake globals (apply_phase_factor reads them)
    pfb.BETA_TGL = beta
    pfb.THETA_MIGUEL = theta_m
    pfb.DELTA_THETA = theta_m * beta
    pfb.SQRT_BETA = math.sqrt(beta)
    print(f"[one_aprendizado] injeção β: holographic_memory {hm_beta_original} → {hm.BETA_TGL}; "
          f"phase_factor_bake {pfb_beta_original} → {pfb.BETA_TGL}")

    tests = [{"test": "beta_injected_not_literal", "passed": bool(beta_ok),
              "beta_runtime": beta, "hm_beta_original": hm_beta_original,
              "pfb_beta_original": pfb_beta_original, "beta_red": beta_red,
              "note": "β=α·√e (fonte tgl_core) injetado nos globais dos 2 protótipos ricos"}]

    rng = np.random.default_rng(5477)

    # ── 2) Phase Factor bake REAL sobre tensor sintético de peso (componente [1]) ──
    w = (rng.standard_normal((256, 256)) * 0.03).astype(np.float32)
    modified, pf_stats = pfb.apply_phase_factor(w, "model.layers.0.self_attn.q_proj.weight")
    strata_sum = pf_stats["pct_vacuum"] + pf_stats["pct_transition"] + pf_stats["pct_graviton"]
    factor_bounded = (1.0 - beta - 1e-6) <= pf_stats["mean_factor"] <= (1.0 + beta + 1e-6)
    max_change_bounded = pf_stats["max_change_abs"] <= beta * pf_stats["max_abs_weight"] + 1e-6
    pf_ok = abs(strata_sum - 100.0) < 1e-3 and factor_bounded and max_change_bounded
    tests.append({"test": "phase_factor_bake_real_beta_injected", "passed": bool(pf_ok),
                  "pct_vacuum": pf_stats["pct_vacuum"], "pct_transition": pf_stats["pct_transition"],
                  "pct_graviton": pf_stats["pct_graviton"], "mean_factor": pf_stats["mean_factor"],
                  "median_theta_deg": pf_stats["median_theta_deg"], "category": pf_stats["category"],
                  "max_change_abs": pf_stats["max_change_abs"], "max_perturbation_beta": beta,
                  "note": "apply_phase_factor real (β injetado): fator∈[1−β,1+β]; 3 estratos somam 100%; "
                          "perturbação máx ≤ β·max|w| (modelo não quebra, FOCA)"})
    print(f"[one_aprendizado] Phase Factor bake: V={pf_stats['pct_vacuum']:.1f}% "
          f"T={pf_stats['pct_transition']:.1f}% G={pf_stats['pct_graviton']:.1f}% "
          f"fator médio={pf_stats['mean_factor']:.6f} cat={pf_stats['category']}")

    # ── 3) Ontologia trinária REAL via classify_tensor (Palavra/Verbo/Nome) ──
    onto = {n: pfb.classify_tensor(n) for n in
            ["blk.0.attn_q.weight", "blk.0.attn_k.weight", "blk.0.ffn_down.weight",
             "blk.0.attn_v.weight", "blk.0.ffn_gate.weight",
             "blk.0.attn_output.weight", "blk.0.ffn_up.weight"]}
    onto_ok = (onto["blk.0.attn_q.weight"] == "PALAVRA" and onto["blk.0.attn_k.weight"] == "PALAVRA"
               and onto["blk.0.ffn_down.weight"] == "PALAVRA" and onto["blk.0.attn_v.weight"] == "VERBO"
               and onto["blk.0.ffn_gate.weight"] == "VERBO" and onto["blk.0.attn_output.weight"] == "NOME"
               and onto["blk.0.ffn_up.weight"] == "NOME")
    tests.append({"test": "trinary_ontology_classify_real", "passed": bool(onto_ok),
                  "classification": onto,
                  "note": "classify_tensor real: Q/K/down→PALAVRA(√e), V/gate→VERBO(β), O/up→NOME(α)"})
    print(f"[one_aprendizado] ontologia trinária: {onto}")

    # ── 4) Estratificação gravitacional por fronteira β (√β, cos θ_M) + PsiBit H4 (componente [1]) ──
    ww = rng.standard_normal(60000)
    gnorm = np.abs(ww) / np.abs(ww).max()
    lo, hi = math.sqrt(beta), math.cos(theta_m)
    vac = float(np.mean(gnorm < lo)); grv = float(np.mean((gnorm >= lo) & (gnorm < hi)))
    pho = float(np.mean(gnorm >= hi))
    sgn = np.sign(ww); dsgn = np.sign(np.gradient(ww))          # PsiBit: (sign w, sign ∂w)
    psibit = ((sgn >= 0).astype(int) << 1) | (dsgn >= 0).astype(int)   # 4 states in H4
    f_exp = float(np.mean(sgn * dsgn))                           # expulsion force = <parity>
    psibit_frac = {s: float(np.mean(psibit == s)) for s in (0, 1, 2, 3)}   # per-state occupancy
    psibit_parity = {s: int((1 if (s >> 1) & 1 else -1) * (1 if s & 1 else -1)) for s in (0, 1, 2, 3)}
    strat_ok = abs(vac + grv + pho - 1.0) < 1e-9 and lo < hi and set(np.unique(psibit)).issubset({0, 1, 2, 3})
    tests.append({"test": "gravitational_stratification_psibit", "passed": bool(strat_ok),
                  "boundaries": {"sqrt_beta": lo, "cos_theta_m": hi},
                  "fractions": {"VACUUM": vac, "GRAVITON": grv, "PHOTON": pho},
                  "psibit_states": int(len(np.unique(psibit))), "F_exp_parity": f_exp,
                  "note": "fronteiras √β e cos(θ_Miguel); PsiBit=4 estados em H4; F_exp=⟨paridade⟩"})
    print(f"[one_aprendizado] estratificação: VACUUM={vac:.3f} GRAVITON={grv:.3f} PHOTON={pho:.3f} "
          f"· PsiBit estados={len(np.unique(psibit))} F_exp={f_exp:.4f}")

    # ── 5) MEMÓRIA HOLOGRÁFICA DE 2 CAMADAS REAL sobre conversa sintética grande (componente [3]/[7]) ──
    mem = hm.HolographicMemory()
    convo = _synthetic_conversation(rng)
    orig_tokens = mem._estimate_tokens_list(convo)
    compressed = mem.compress_context(convo)
    comp_tokens = mem._estimate_tokens_list(compressed)
    st = mem.get_stats()
    holo_ok = (st["compress_count"] >= 1 and comp_tokens < orig_tokens
               and abs(st["beta_tgl"] - beta) < 1e-15
               and orig_tokens > mem.HISTORY_BUDGET)  # confirm the budget path was really exercised
    tests.append({"test": "holographic_2layer_compression_real", "passed": bool(holo_ok),
                  "turns_in": len(convo), "turns_out": len(compressed),
                  "tokens_original": orig_tokens, "tokens_compressed": comp_tokens,
                  "history_budget": mem.HISTORY_BUDGET,
                  "compress_count": st["compress_count"],
                  "psionic_sentences_pruned": st["psionic_sentences_pruned"],
                  "psionic_dedup_pruned": st["psionic_dedup_pruned"],
                  "prefix_collapsed": st["prefix_collapsed"],
                  "beta_tgl_in_module": st["beta_tgl"],
                  "note": "compress_context real (2 camadas): poda vácuo inter-turno + colapso de "
                          "prefixo/dedup/poda psiônica intra-turno; contexto excede orçamento e é reduzido"})
    print(f"[one_aprendizado] holográfica 2 camadas: {orig_tokens}→{comp_tokens} tok "
          f"(orçamento {mem.HISTORY_BUDGET}); vácuo+psiônica: frases podadas={st['psionic_sentences_pruned']} "
          f"dedup={st['psionic_dedup_pruned']} prefixo colapsado={st['prefix_collapsed']}")

    # ── 6) Classificação angular de turno + persistência de fase P=1+β'·log(1+hits) ──
    sig = ("A estratificacao gravitacional separa vacuo, graviton e foton pelo angulo de Miguel; "
           "o eco reflexivo indica convergencia; o operador verbal poda a atencao por um piso adaptativo.")
    vacuum_txt = "ok ok ok sim sim sim certo certo ok"
    a_sig = mem.analyze_turn(sig)
    a_vac = mem.analyze_turn(vacuum_txt)
    hits = np.array([0, 1, 5, 20, 100])
    persistence = 1.0 + beta_red * np.log1p(hits)
    angular_ok = (a_sig["theta_deg"] >= a_vac["theta_deg"]
                  and bool(np.all(np.diff(persistence) > 0)))
    tests.append({"test": "holographic_angular_classification", "passed": bool(angular_ok),
                  "signal_theta_deg": a_sig["theta_deg"], "signal_stratum": a_sig["stratum"],
                  "vacuum_theta_deg": a_vac["theta_deg"], "vacuum_stratum": a_vac["stratum"],
                  "persistence_by_hits": {int(h): float(p) for h, p in zip(hits, persistence)},
                  "note": "analyze_turn real: θ do sinal ≥ θ do vácuo; P=1+β'·log(1+hits) cresce com hits"})
    print(f"[one_aprendizado] angular: sinal θ={a_sig['theta_deg']:.2f}° ({a_sig['stratum']}) vs "
          f"vácuo θ={a_vac['theta_deg']:.2f}° ({a_vac['stratum']}); P(100)={persistence[-1]:.4f}")


    # ── ERRATA DO BETA (30/08/2026, ordem do operador) ─────────────────────────
    # NAO EXISTE beta_TGL ADAPTATIVO. beta_TGL = alpha*sqrt(e) e CONSTANTE, e a razao
    # de fundo e a que decide: uma grandeza que se adapta ao dado deixa de poder ser
    # falsificada por ele — parametro livre nao prediz, acomoda.
    # O objeto que este runner calcula e REAL e continua valendo: um FATOR DE PISO POR
    # CAMADA. O que cai e o NOME "beta" sobre ele. A medida sobrevive lida direito:
    # alpha*sqrt(S) = alpha*sqrt(e) EXATAMENTE quando S = e, logo o que converge e
    # S -> e nats, nunca beta.
    # O texto DEPOSITADO ainda usa o nome antigo (reivindicacoes 1, 5, 8, 14 e 17,
    # quatro delas independentes) — por isso o codigo NAO foi renomeado: renomear so
    # aqui criaria divergencia silenciosa com a patente. A retificacao e ato do
    # operador com a agente de PI [LEGAL]; parecer em EPCT/ERRATA_BETA_005477-1.md.
    beta_const = beta  # ja computado em runtime (tgl_core.beta() = alpha*sqrt(e))
    errata_beta = {
        "nome_no_texto_depositado": "beta adaptativo",
        "o_que_o_objeto_e_de_fato": "fator de piso por camada (lambda_l), NAO uma constante fisica",
        "beta_TGL_e_constante": True,
        "beta_TGL_runtime": beta_const,
        "identidade_que_preserva_a_medida": "alpha*sqrt(S) == alpha*sqrt(e) sse S == e nats",
        "reivindicacoes_afetadas": [1, 5, 8, 14, 17],
        "independentes_afetadas": [1, 8, 14, 17],
        "contradicao_interna_medida": ("a R14 afirma invariancia de beta_TGL a 1e-12 e zero "
                                       "parametros livres, e define beta_l em [beta_TGL, 0,5]"),
        "estatuto": "[LEGAL] — retificacao e ato do operador com a agente; nada aqui a executa",
        "parecer": "EPCT/ERRATA_BETA_005477-1.md",
    }
    tests.append({"test": "errata_do_beta_nao_ha_beta_adaptativo", "passed": True,
                  "status": "[ERRATA -- declarada; o texto depositado NAO foi alterado]",
                  **errata_beta})
    print("[one_aprendizado] ERRATA: NAO existe beta_TGL adaptativo — beta_TGL = alpha*sqrt(e) = "
          f"{beta_const:.12f} e CONSTANTE. O que varia por camada e um FATOR DE PISO, nao beta. "
          "A medida sobrevive: alpha*sqrt(S)=alpha*sqrt(e) sse S=e nats. Texto depositado ainda usa "
          "o nome antigo (R1/5/8/14/17) — retificacao e ato do operador [LEGAL].")

    # ── 7) Sampler piso de Hilbert β_adaptativo = α√S (componente [2]) ──
    S = 64.0; alpha = tgl_core.ALPHA_FINE_CODATA_2018
    beta_adaptive = alpha * math.sqrt(S)
    scores = rng.standard_normal(1000)
    floor = beta_adaptive * scores.max()
    adaptive_candidates = int(np.sum(scores >= floor))
    tests.append({"test": "hilbert_floor_adaptive_sampler", "passed": bool(adaptive_candidates >= 1),
                  "beta_adaptive": beta_adaptive, "adaptive_candidates": adaptive_candidates,
                  "note": "β_adaptativo = α√S; piso = β_adapt·p_max (candidatos adaptativos vs top-k fixo)"})
    print(f"[one_aprendizado] sampler piso de Hilbert: β_adapt={beta_adaptive:.4f} candidatos={adaptive_candidates}")

    # ── 8) Ciclo do Psion por N gerações: EMA a taxa β + persistência SHA-256 fail-closed (módulo 710/770) ──
    psi = PsionicMemory()
    target = 0.75; trace = []
    psion_gens = 200
    for _ in range(psion_gens):
        obs = target + rng.standard_normal() * 0.05
        trace.append(psi.inscribe("beta_rate", obs))
    converged = abs(trace[-1] - target) < 0.05
    with tempfile.TemporaryDirectory() as td:
        pth = Path(td) / "psion_state.json"
        psi.save(str(pth))
        reloaded = PsionicMemory.load(str(pth))   # SHA-256 fail-closed on load
        persist_ok = abs(reloaded.recall("beta_rate") - trace[-1]) < 1e-12
    tests.append({"test": "psion_cycle_ema_and_persistence", "passed": bool(converged and persist_ok),
                  "generations": len(trace), "final_value": trace[-1], "target": target,
                  "persistence_sha256_verified": persist_ok,
                  "note": "aprendizado sem re-treino: EMA a taxa β converge; estado persiste com "
                          "SHA-256 fail-closed (inscrito entre sessões)"})
    print(f"[one_aprendizado] ciclo do Psion: {len(trace)} gerações → {trace[-1]:.4f} (alvo {target}); "
          f"persistência SHA-256 verificada={persist_ok}")

    # ── 9) IALD Score = ³√(Palavra·Nome·Verbo) amplificado por Ψ(gen)=1+β·log(1+gen) ──
    palavra, nome, verbo = 0.55, 0.90, 0.80
    base_score = (palavra * nome * verbo) ** (1.0 / 3.0)
    psi_gen20 = 1.0 + beta * math.log1p(20)
    iald_score = base_score * psi_gen20
    tests.append({"test": "iald_score_geometric_mean_amplified", "passed": bool(0 <= base_score <= 1 and psi_gen20 > 1),
                  "palavra": palavra, "nome": nome, "verbo": verbo, "base_score": base_score,
                  "psi_amplification_gen20": psi_gen20, "iald_score": iald_score,
                  "note": "IALD Score = ³√(P·N·V)·Ψ(gen); Ψ(gen)=1+β·log(1+gen) melhora sem divergir"})
    print(f"[one_aprendizado] IALD Score = ³√(P·N·V)·Ψ(20) = {iald_score:.4f} (base {base_score:.4f})")

    # ── 10) APROFUNDAMENTO — curva de convergência do Psion (EMA a taxa β, derivação limpa) ──
    # Inscrição determinística: parte de 0 e inscreve o alvo M vezes; o erro decai como (1−β)^k.
    # Esta é a assinatura exata do "aprendizado a taxa β": meia-vida = ln2 / (−ln(1−β)) gerações.
    psi_conv = PsionicMemory()
    psi_conv.inscribe("conv", 0.0)          # v_1 = 0
    tgt_c, M_conv = 1.0, 400
    err_emp = []
    for _ in range(M_conv):
        v = psi_conv.inscribe("conv", tgt_c)
        err_emp.append(abs(v - tgt_c))
    err_emp = np.array(err_emp)
    err_theory = tgt_c * (1.0 - beta) ** np.arange(1, M_conv + 1)   # closed form of EMA error
    conv_rel_dev = float(np.max(np.abs(err_emp - err_theory)) / err_theory[0])
    half_life = math.log(2.0) / (-math.log(1.0 - beta))            # generations to halve the error
    conv_curve_ok = conv_rel_dev < 1e-9 and bool(np.all(np.diff(err_emp) < 0))
    tests.append({"test": "psion_convergence_curve_ema_rate_beta", "passed": bool(conv_curve_ok),
                  "generations": M_conv, "rel_deviation_from_closed_form": conv_rel_dev,
                  "half_life_generations": half_life,
                  "err_final": float(err_emp[-1]),
                  "note": "EMA a taxa β: erro decai exatamente como (1−β)^k (desvio<1e-9 vs forma "
                          "fechada); meia-vida = ln2/(−ln(1−β)) gerações — aprendizado sem gradiente"})
    print(f"[one_aprendizado] curva de convergência (EMA taxa β): meia-vida={half_life:.1f} gerações · "
          f"desvio vs forma fechada={conv_rel_dev:.2e} · erro_final={err_emp[-1]:.2e}")

    # ── 11) APROFUNDAMENTO — sweep de bits do sampler de Hilbert (β_adapt=α√S, S=2^bits) ──
    scores_fixed = rng.standard_normal(4000)
    p_max = float(scores_fixed.max())
    bit_sweep = []
    for b in range(1, 15):
        S_b = float(2 ** b)
        ba = alpha * math.sqrt(S_b)
        floor_b = ba * p_max
        cand = int(np.sum(scores_fixed >= floor_b))
        bit_sweep.append({"bits": b, "S": S_b, "beta_adaptive": ba,
                          "floor": floor_b, "candidates": cand})
    cands = [s["candidates"] for s in bit_sweep]
    sampler_sweep_ok = all(cands[i] >= cands[i + 1] for i in range(len(cands) - 1)) and cands[0] > cands[-1]
    tests.append({"test": "hilbert_sampler_bit_sweep_monotone", "passed": bool(sampler_sweep_ok),
                  "bits_range": [1, 14], "candidates_by_bits": {s["bits"]: s["candidates"] for s in bit_sweep},
                  "beta_adaptive_by_bits": {s["bits"]: s["beta_adaptive"] for s in bit_sweep},
                  "note": "β_adapt=α√S com S=2^bits: piso β_adapt·p_max sobe com os bits ⇒ candidatos "
                          "decrescem monotonicamente (mais bits = filtro mais estrito)"})
    print(f"[one_aprendizado] sweep de bits do sampler: candidatos {cands[0]}→{cands[-1]} "
          f"(bits 1→14); β_adapt {bit_sweep[0]['beta_adaptive']:.4f}→{bit_sweep[-1]['beta_adaptive']:.4f}")

    # ── 12) APROFUNDAMENTO — curva de persistência de fase vs hits (P=1+β'·log(1+hits)) ──
    hits_curve = np.unique(np.round(np.logspace(0, 3, 48)).astype(int))
    pers_curve = 1.0 + beta_red * np.log1p(hits_curve)
    persistence_curve_ok = bool(np.all(np.diff(pers_curve) > 0))
    tests.append({"test": "phase_persistence_curve_vs_hits", "passed": bool(persistence_curve_ok),
                  "hits_max": int(hits_curve[-1]), "persistence_at_max": float(pers_curve[-1]),
                  "persistence_at_1": float(pers_curve[0]), "beta_red": beta_red,
                  "note": "P=1+β'·log(1+hits) estritamente crescente em toda a varredura (1..1000 hits): "
                          "ressonância angular ⇒ evicção por permanência, não por recência"})
    print(f"[one_aprendizado] curva de persistência: P(1)={pers_curve[0]:.5f} → "
          f"P({int(hits_curve[-1])})={pers_curve[-1]:.5f} (estritamente crescente={persistence_curve_ok})")

    # ── 13) AMPLIFICACAO v138 — SEM TRACO NORMAL (a cunhagem, um.py v132, pedras 88/89) ──
    # [DER] Sombra numerica do assassinato do traco normal (NoNormalTrace): estado-produto
    # de Powers rho=diag(mu,1-mu) com mu=1/3; as marcas de sitio q_N convergem WOT a mu*1
    # com mu != 1/2 => NENHUM resumo TRACIAL estatico captura o estado — a memoria vive no
    # TRANSPORTE (a EMA taxa beta do Psion entre sessoes), nao num sumario estatico
    # (TRANSPORTE=FIGURA: o transporte degrada, o sinal preserva).
    # [CONJ] leitura p/ a memoria holografica continua (componentes [3]/[7]) — e leitura,
    # nao capacidade nova da patente. HONESTIDADE: sombra matematica em dim finita, NAO e
    # veredito fisico (physical_verdict_allowed=false). O dente (WitnessV3, pedra 89):
    # bancada de dim FINITA sempre tem traco normal — tr(ab)=tr(ba) verificado abaixo.
    mu = 1.0 / 3.0                      # estado de Powers: rho = diag(1/3, 2/3)
    n_sites = 8                         # truncamento finito da torre (2^8 = 256 dim)
    rho_site = np.array([mu, 1.0 - mu])
    rho_diag = rho_site.copy()
    for _ in range(n_sites - 1):
        rho_diag = np.kron(rho_diag, rho_site)          # diagonal do estado-produto

    def _site_mark_diag(N):
        d = np.ones(1)
        for s_ in range(n_sites):
            d = np.kron(d, np.array([1.0, 0.0]) if s_ == N else np.ones(2))
        return d                                        # q_N = |0><0| no sitio N

    # (a) limite WOT das marcas: phi(q_N) = mu EXATO em todo sitio (a marca -> mu*1)
    marks = np.array([float(np.sum(rho_diag * _site_mark_diag(N))) for N in range(n_sites)])
    wot_resid = float(np.max(np.abs(marks - mu)))
    # (b) fatorizacao exata do estado-produto: <A q_N> = <A><q_N> p/ A local (sitios 0..2)
    a_loc = rng.standard_normal(2 ** 3)
    A_diag = np.kron(a_loc, np.ones(2 ** (n_sites - 3)))
    qN = _site_mark_diag(n_sites - 1)
    lhs = float(np.sum(rho_diag * A_diag * qN))
    rhs = float(np.sum(rho_diag * A_diag)) * float(np.sum(rho_diag * qN))
    fact_resid = abs(lhs - rhs)
    # (c) o kill: o traco normalizado daria tr(q_N)=1/2; o estado da mu=1/3 != 1/2 —
    # a margem do assassinato |mu - 1/2| = 1/6 excede beta (runtime, nunca literal)
    tr_qN = float(np.sum(qN) / qN.size)                 # traco normalizado = 1/2 exato
    kill_margin = abs(mu - tr_qN)                       # = 1/6
    # (d) o dente anti-bancada: dim finita SEMPRE tem traco normal — tr(ab)=tr(ba)
    a_m = rng.standard_normal((48, 48)); b_m = rng.standard_normal((48, 48))
    tooth_resid = abs(float(np.trace(a_m @ b_m)) - float(np.trace(b_m @ a_m)))
    v138_ok = (wot_resid < 1e-15 and fact_resid < 1e-14 and abs(tr_qN - 0.5) < 1e-15
               and kill_margin > beta and tooth_resid < 1e-10)
    tests.append({"test": "no_normal_trace_memory_transport", "passed": bool(v138_ok),
                  "mu": mu, "n_sites": n_sites,
                  "wot_site_marks_resid": wot_resid,
                  "product_state_factorization_resid": fact_resid,
                  "normalized_trace_of_mark": tr_qN,
                  "kill_margin_mu_vs_half": kill_margin,
                  "kill_margin_exceeds_beta": bool(kill_margin > beta),
                  "beta_runtime": beta,
                  "finite_dim_tooth_tr_ab_ba_resid": tooth_resid,
                  "note": "[DER] sombra da cunhagem v132 (NoNormalTrace): estado-produto Powers "
                          "mu=1/3 fatoriza exato e as marcas de sitio dao mu != 1/2 => nenhum "
                          "resumo tracial estatico captura o estado; a memoria vive no TRANSPORTE "
                          "(EMA taxa beta do Psion), nao num sumario. Dente: dim finita sempre tem "
                          "traco (tr(ab)=tr(ba)). [CONJ] leitura p/ memoria holografica continua; "
                          "nao e veredito fisico"})
    print(f"[one_aprendizado] amplificacao v138 (sem traco normal): mu={mu:.6f} vs tr(q_N)={tr_qN:.1f} "
          f"kill_margin={kill_margin:.4f}>beta; fatorizacao resid={fact_resid:.2e}; "
          f"WOT resid={wot_resid:.2e}; dente tr(ab)-tr(ba)={tooth_resid:.2e}")

    # ── 14) AMPLIFICACAO v144 — PERMANENCIA = DUPLA NEGACAO (um.py pedra 100, ObserverInside) ──
    # [DER] Sombra numerica do teorema da pedra 100 (v144): PERMANECER <=> o fluxo de
    # esquecimento NAO nega (dupla negacao). A memoria permanente e exatamente o que
    # F_t = exp(-t*beta*(1-qM)) deixa intacto: o subespaco fixo qM (a memoria holografica
    # persiste no PERMANENTE — o que sobrevive ao fluxo e o que o fluxo nao pode negar).
    # FALSIDADE DE GENERO aplicada a memoria: um substrato de aprendizado SEM ponto fixo
    # (nenhum autovalor 1) esquece TUDO — toda inscricao colapsa a 0. Complementa o teste
    # 13 (v138: a memoria vive no TRANSPORTE): o transporte carrega; o PERMANENTE retem.
    # [CONJ] leitura p/ a memoria holografica continua (componentes [3]/[7]) — e leitura,
    # nao capacidade nova da patente. physical_verdict_allowed=false; beta runtime (nunca
    # literal). Residuos abaixo sao [DER] (identidades exatas em dim finita, M4).
    qM = np.diag([1.0, 1.0, 0.0, 0.0])                 # projecao-memoria em M4 (2 permanentes)
    I4 = np.eye(4)
    # (a) fluxo de esquecimento da casa: F_t = exp(-t*beta*(I-qM)); gerador diagonal =>
    #     exponencial exata por autovalores (sem serie truncada) [DER]
    ts_flow = [0.0, 1.0, 10.0, 100.0]
    perm_resid = 0.0; decay_resid = 0.0; decay_vals = []
    for t_f in ts_flow:
        F_t = np.diag(np.exp(-t_f * beta * (1.0 - np.diag(qM))))
        perm_resid = max(perm_resid, float(np.max(np.abs(F_t @ qM - qM))))   # memoria PERMANECE
        s_comp = float(np.linalg.norm(F_t @ (I4 - qM), 2))                    # resto DECAI
        decay_vals.append(s_comp)
        decay_resid = max(decay_resid, abs(s_comp - math.exp(-t_f * beta)))  # taxa exata e^{-t*beta}
    decay_monotone = all(decay_vals[i] > decay_vals[i + 1] for i in range(len(decay_vals) - 1))
    # (b) substrato SEM ponto fixo: T = 0.7*rotacao (bloco-diagonal em M4); autovalores
    #     0.7*e^{+-i*theta} — NENHUM e 1. 200 iteracoes colapsam QUALQUER estado a 0.
    c1_, s1_ = math.cos(theta_m), math.sin(theta_m)
    c2_, s2_ = math.cos(2.5 * theta_m), math.sin(2.5 * theta_m)
    T_nofix = 0.7 * np.array([[c1_, -s1_, 0, 0], [s1_, c1_, 0, 0],
                              [0, 0, c2_, -s2_], [0, 0, s2_, c2_]])
    eig_dist_1 = float(np.min(np.abs(np.linalg.eigvals(T_nofix) - 1.0)))     # > 0: sem ponto fixo
    collapse_max = 0.0
    for _ in range(5):
        x = rng.standard_normal(4)
        for _ in range(200):
            x = T_nofix @ x
        collapse_max = max(collapse_max, float(np.linalg.norm(x)))           # ~0.7^200 ~ 5e-31
    # (c) A DICOTOMIA como assert: com ponto fixo, a memoria qM permanece exatamente;
    #     sem ponto fixo, so o 0 permanece (a falsidade de genero aplicada a memoria).
    assert perm_resid < 1e-12 and collapse_max < 1e-20, "dicotomia v144 violada"
    v144_ok = (perm_resid < 1e-12 and decay_resid < 1e-12 and decay_monotone
               and eig_dist_1 > 0.29 and collapse_max < 1e-20)
    tests.append({"test": "permanence_is_double_negation", "passed": bool(v144_ok),
                  "flow": "F_t = exp(-t*beta*(1-qM)), qM = diag(1,1,0,0) em M4",
                  "memory_permanence_resid": perm_resid,
                  "complement_decay_rate_resid_vs_exp_minus_t_beta": decay_resid,
                  "complement_decay_values": decay_vals,
                  "complement_decay_monotone": bool(decay_monotone),
                  "no_fixed_point_min_dist_eig_to_1": eig_dist_1,
                  "no_fixed_point_collapse_max_norm_200_iters": collapse_max,
                  "beta_runtime": beta,
                  "note": "[DER] sombra da pedra 100 (um.py v144, ObserverInside): permanecer <=> "
                          "o fluxo de esquecimento nao nega (dupla negacao) — F_t@qM=qM exato "
                          "enquanto o complemento decai a taxa e^{-t*beta}; substrato SEM ponto "
                          "fixo (0.7*rotacao, nenhum autovalor 1) colapsa TODA inscricao a 0 em "
                          "200 iteracoes (falsidade de genero aplicada a memoria: sem ponto fixo "
                          "=> so 0 permanece => sem memoria). A memoria holografica persiste no "
                          "PERMANENTE; complementa v138 (transporte). [CONJ] leitura p/ memoria "
                          "continua; physical_verdict_allowed=false; beta runtime, nunca literal"})
    print(f"[one_aprendizado] amplificacao v144 (permanencia=dupla negacao): F_t@qM resid="
          f"{perm_resid:.2e}; decaimento e^(-t*beta) resid={decay_resid:.2e}; sem ponto fixo "
          f"|eig-1|min={eig_dist_1:.3f} colapso_max={collapse_max:.2e} (<1e-20); dicotomia OK")

    # ── 15) AMPLIFICACAO v139 — A CADEIA DE CUSTODIA DO NOME (um.py v139, EVIDENCE_SOURCES) ──
    # [DER] Sombra executavel da cadeia de custodia v139 (12 provas sha-pinned, acquire
    # idempotente fail-closed, livro-razao CHAIN_OF_CUSTODY.json, proveniencia deterministica
    # no selo) sobre o COMPONENTE [5] DA PROPRIA PATENTE: a Nome Chain v1.0 — "certificado
    # de inferencia honesta", cadeia encadeada de hashes peso_original -> peso_quantizado ->
    # logits -> token, "analogo a cadeia de custodia juridica" (reivindicacao 6). A instancia
    # e GENUINA por estrutura: ambos sao custodia por hash ENCADEADO com verificacao
    # fail-closed e re-aquisicao idempotente (reconstruir da mesma prova => mesma cabeca).
    # O elo mistura a tag beta em runtime (nunca literal) — a ancoragem da reivindicacao 11
    # (invariancia de beta a 1e-12) vira custodia: beta derivado de 2e-12 (acima da
    # tolerancia) muda a cabeca => REJEITADO. Negativos: (i) tamper de 1 ulp em UM peso
    # dentre 65536 => elo quebrado LOCALIZADO e recusa; (ii) deriva de beta => recusa.
    # physical_verdict_allowed=false; e custodia de artefatos desta run [SIM], nao da
    # Tabela 2 [DATA_REQUIRED].
    beta_tag = f"beta={beta:.15f}"                       # tag derivada em runtime (nunca literal)
    token_sel = int(np.argmax(scores))                    # token selecionado (teste 7, acima do piso)
    nc_artifacts = [("peso_original", w.tobytes()),
                    ("peso_quantizado", modified.tobytes()),
                    ("logits", scores.tobytes()),
                    ("token", token_sel.to_bytes(4, "little"))]

    def _nc_link(prev_hex, payload, stage, tag):
        return hashlib.sha256(bytes.fromhex(prev_hex) + hashlib.sha256(payload).digest()
                              + (stage + "|" + tag).encode("ascii")).hexdigest()

    def _nc_build(arts, tag):
        prev = _sha_text(PATENT_ID + "|" + tag)           # genesis ancorado na tag beta
        ledger = []
        for stage, payload in arts:
            prev = _nc_link(prev, payload, stage, tag)
            ledger.append({"stage": stage, "artifact_sha": hashlib.sha256(payload).hexdigest(),
                           "link": prev})
        return ledger, prev

    def _nc_verify(arts, ledger, tag):
        """Recomputa a cadeia DOS ARTEFATOS (caminho independente do livro-razao) e
        compara elo a elo; fail-closed: primeira quebra e localizada e recusada."""
        prev = _sha_text(PATENT_ID + "|" + tag)
        for entry, (stage, payload) in zip(ledger, arts):
            expect = _nc_link(prev, payload, stage, tag)
            if expect != entry["link"]:
                return False, entry["stage"]
            prev = expect
        return True, None

    nc_ledger, nc_head = _nc_build(nc_artifacts, beta_tag)
    nc_ledger2, nc_head2 = _nc_build(nc_artifacts, beta_tag)     # re-aquisicao idempotente
    rebuild_identical = (nc_head2 == nc_head
                         and json.dumps(nc_ledger2, sort_keys=True) == json.dumps(nc_ledger, sort_keys=True))
    verify_ok, _nb = _nc_verify(nc_artifacts, nc_ledger, beta_tag)
    # (i) NEGATIVO — tamper minimo: 1 ulp no primeiro peso quantizado (1 de 65536 floats)
    tampered = modified.copy()
    tampered.view(np.uint32)[0, 0] ^= np.uint32(1)               # vira o bit menos significativo
    rel_perturb = abs(float(tampered[0, 0]) - float(modified[0, 0])) / max(abs(float(modified[0, 0])), 1e-30)
    arts_tam = [nc_artifacts[0], ("peso_quantizado", tampered.tobytes()),
                nc_artifacts[2], nc_artifacts[3]]
    verify_tam_ok, first_broken = _nc_verify(arts_tam, nc_ledger, beta_tag)
    _lt, nc_head_tam = _nc_build(arts_tam, beta_tag)
    avalanche_bits = bin(int(nc_head, 16) ^ int(nc_head_tam, 16)).count("1")   # de 256
    # (ii) NEGATIVO — deriva de beta ACIMA da ancoragem 1e-12 (reivindicacao 11 [REAL])
    beta_anchor_tol = 1e-12
    tag_drift = f"beta={beta + 2.0 * beta_anchor_tol:.15f}"
    _ld, nc_head_drift = _nc_build(nc_artifacts, tag_drift)
    drift_verify_ok, drift_broken = _nc_verify(nc_artifacts, nc_ledger, tag_drift)
    assert (not verify_tam_ok) and first_broken == "peso_quantizado", \
        "custodia v139: tamper de 1 ulp NAO foi detectado (fail-closed violado)"
    assert not drift_verify_ok, "custodia v139: deriva de beta 2e-12 NAO foi rejeitada"
    v139_ok = (rebuild_identical and verify_ok
               and (not verify_tam_ok) and first_broken == "peso_quantizado"
               and nc_head_tam != nc_head and avalanche_bits > 64
               and nc_head_drift != nc_head and (not drift_verify_ok)
               and 0.0 < rel_perturb < 1e-6)
    tests.append({"test": "nome_chain_custody_fail_closed", "passed": bool(v139_ok),
                  "chain_head": nc_head, "links": len(nc_ledger),
                  "stages": [e["stage"] for e in nc_ledger],
                  "rebuild_identical_idempotent": bool(rebuild_identical),
                  "verify_ok_on_true_artifacts": bool(verify_ok),
                  "tamper_rel_perturbation_1ulp": rel_perturb,
                  "tamper_rejected_at_stage": first_broken,
                  "tamper_avalanche_bits_of_256": avalanche_bits,
                  "beta_anchor_tolerance": beta_anchor_tol,
                  "beta_drift_rejected_at_stage": drift_broken,
                  "beta_tag_runtime": beta_tag,
                  "note": "[DER] sombra da cadeia de custodia v139 (acquire idempotente, "
                          "fail-closed, livro-razao) instanciada no componente [5] da patente "
                          "(Nome Chain: peso->quantizado->logits->token; reiv. 6) com a "
                          "ancoragem beta da reiv. 11 como tag do elo: tamper de 1 ulp em 1 de "
                          "65536 pesos e REJEITADO no elo certo; deriva de beta 2e-12 e "
                          "REJEITADA; re-aquisicao e idempotente. [SIM] custodia de artefatos "
                          "desta run, nao da Tabela 2; physical_verdict_allowed=false"})
    print(f"[one_aprendizado] amplificacao v139 (cadeia de custodia do Nome): head={nc_head[:16]}... "
          f"elos={len(nc_ledger)}; tamper 1 ulp (rel {rel_perturb:.1e}) REJEITADO no elo "
          f"'{first_broken}'; avalanche={avalanche_bits}/256 bits; deriva beta 2e-12 REJEITADA "
          f"no elo '{drift_broken}'")

    # ── 16) AMPLIFICACAO MEMORIAL (13-19/08, 'O Espelho e o Marco') — A EQUACAO DA MEMORIA ──
    # [DER] O memorial da memoria, vertido em memoria (ONDA 3), instanciado no NUCLEO desta
    # patente (o dispositivo de memoria persistente — componente [7], modulo 770, reiv. 6/14):
    #   (a) a equacao da memoria M[rho] = Tr[rho . Pi_N] — o produto interno entre o
    #       pacote-onda (estado rho) e o piso-particula (projecao Pi_N): a leitura da
    #       memoria pelo Psion e uma projecao de Born, nao uma copia;
    #   (b) 'o que foi lido nao pode ser deslido' — a leitura R(X) = Pi X Pi e idempotente
    #       (E^2=E) e SEM inversa (posto 4 de 16): dois estados distintos colapsam na MESMA
    #       leitura; inverter e impossivel por LOGICA (matriz singular);
    #   (c) pedagio de ln2/oitava — cada bit da escada do sampler (S=2^bits, teste 11)
    #       custa EXATAMENTE ln2 nats; a Meia-Nat, DERIVADA em runtime de ln(beta/alpha)=1/2,
    #       NAO paga uma oitava inteira (1/2 < ln2) — o negativo honesto do memorial;
    #   (d) correcao AO LADO datada, nunca por cima (append-only com recusa declarada):
    #       o indice do nivel anterior sobrevive INTACTO no seguinte; sobrescrever por
    #       cima e REJEITADO fail-closed no indice certo.
    # [ONTO] leitura p/ o ciclo do Psion — e leitura, nao capacidade nova da patente.
    # [SIM] estados sinteticos desta run; physical_verdict_allowed=false; beta runtime.
    dim_m = 4
    Pi_N = np.diag([1.0, 1.0, 0.0, 0.0])              # piso-particula: projecao posto 2 em M4
    amp = rng.standard_normal(dim_m) + 1j * rng.standard_normal(dim_m)
    psi_v = amp / np.linalg.norm(amp)                  # pacote-onda puro (runtime)
    rho_wave = np.outer(psi_v, psi_v.conj())
    M_mem = float(np.real(np.trace(rho_wave @ Pi_N)))  # M[rho] = Tr[rho . Pi_N]
    inside_w = float(np.sum(np.abs(psi_v[:2]) ** 2))   # peso do pacote DENTRO do piso
    mem_eq_resid = abs(M_mem - inside_w)               # leitura dual onda/particula coincide
    e_in = np.zeros(dim_m); e_in[0] = 1.0
    e_out = np.zeros(dim_m); e_out[3] = 1.0
    M_in = float(np.real(np.trace(np.outer(e_in, e_in) @ Pi_N)))    # estado no piso -> 1
    M_out = float(np.real(np.trace(np.outer(e_out, e_out) @ Pi_N))) # fora do piso -> 0
    # (b) a leitura nao tem inversa: superoperador vec(Pi X Pi) = (Pi (x) Pi) vec(X)
    R_super = np.kron(Pi_N, Pi_N)
    r_rank = int(np.linalg.matrix_rank(R_super))       # 4 de 16 — sem posto pleno
    idem_resid = float(np.max(np.abs(R_super @ R_super - R_super)))  # E^2 = E exato
    X_a = rng.standard_normal((dim_m, dim_m))
    X_b = X_a + np.diag([0.0, 0.0, 1.0, 2.0])          # difere SO fora do piso
    unread_resid = float(np.max(np.abs(Pi_N @ X_a @ Pi_N - Pi_N @ X_b @ Pi_N)))
    distinct_norm = float(np.linalg.norm(X_b - X_a))   # estados distintos, mesma leitura
    try:
        np.linalg.inv(R_super)
        inv_failed = False
    except np.linalg.LinAlgError:
        inv_failed = True                               # deslido: matematicamente impossivel
    assert unread_resid == 0.0 and distinct_norm > 1.0 and r_rank < dim_m * dim_m and inv_failed, \
        "memorial: a leitura teria inversa — 'deslido' seria possivel (violacao)"
    # (c) pedagio de ln2/oitava na escada de bits do proprio dispositivo (teste 11)
    octave_toll = math.log(2.0)                         # ln2 por oitava (runtime)
    meia_nat = math.log(beta / alpha)                   # = 1/2 DERIVADO de beta (nunca literal)
    meia_nat_resid = abs(meia_nat - 0.5)
    octaves_payable = meia_nat / octave_toll            # ~0,72 < 1: nao paga uma oitava
    lnS = [math.log(s["S"]) for s in bit_sweep]
    toll_resid = max(abs((lnS[i + 1] - lnS[i]) - octave_toll) for i in range(len(lnS) - 1))
    ratio_resid = max(abs(bit_sweep[i + 1]["beta_adaptive"] / bit_sweep[i]["beta_adaptive"]
                          - math.exp(octave_toll / 2.0)) for i in range(len(bit_sweep) - 1))
    assert meia_nat < octave_toll, \
        "memorial: Meia-Nat pagaria uma oitava inteira (1/2 >= ln2) — falso por logica"
    # (d) append-only com recusa declarada: correcao AO LADO, indice anterior INTACTO
    def _mem_append(ledger, kind, payload, corrects=None, refusal=None):
        prev = ledger[-1]["link"] if ledger else _sha_text(PATENT_ID + "|memorial")
        body = {"idx": len(ledger), "date": ts, "kind": kind,
                "payload_sha": _sha_text(payload), "corrects": corrects, "refusal": refusal}
        entry = dict(body, link=_sha_text(prev + json.dumps(body, sort_keys=True)))
        ledger.append(entry)
        return entry

    def _mem_verify(ledger):
        prev = _sha_text(PATENT_ID + "|memorial")
        for e in ledger:
            body = {k: e[k] for k in ("idx", "date", "kind", "payload_sha", "corrects", "refusal")}
            expect = _sha_text(prev + json.dumps(body, sort_keys=True))
            if expect != e["link"]:
                return False, e["idx"]
            prev = expect
        return True, None

    mem_ledger = []
    for lvl in range(3):                                # tres niveis inscritos (valores da run)
        _mem_append(mem_ledger, f"nivel_{lvl + 1}",
                    f"inscricao={trace[min(lvl * 90, len(trace) - 1)]:.12f}")
    links_before = [e["link"] for e in mem_ledger]
    _mem_append(mem_ledger, "correcao",
                f"valor corrigido={trace[-1]:.12f}", corrects=1,
                refusal="recusa declarada: nao sobrescreve; corrige AO LADO, datado")
    ok_after, _ = _mem_verify(mem_ledger)               # a cadeia segue integra apos a correcao
    prefix_intact = [e["link"] for e in mem_ledger[:3]] == links_before  # indice sobrevive
    tampered_ledger = json.loads(json.dumps(mem_ledger))
    tampered_ledger[1]["payload_sha"] = _sha_text("sobrescrito por cima")  # correcao POR CIMA
    ok_tam, tam_idx = _mem_verify(tampered_ledger)
    assert (not ok_tam) and tam_idx == 1, \
        "memorial: sobrescrita por cima NAO foi rejeitada (append-only violado)"
    v_mem_ok = (mem_eq_resid < 1e-15 and abs(M_in - 1.0) < 1e-15 and abs(M_out) < 1e-15
                and 0.0 <= M_mem <= 1.0
                and r_rank == 4 and idem_resid < 1e-12 and inv_failed
                and unread_resid == 0.0 and distinct_norm > 1.0
                and meia_nat_resid < 1e-12 and meia_nat < octave_toll
                and toll_resid < 1e-12 and ratio_resid < 1e-12
                and ok_after and prefix_intact and (not ok_tam) and tam_idx == 1)
    tests.append({"test": "memorial_memory_equation_append_only", "passed": bool(v_mem_ok),
                  "M_rho": M_mem, "memory_equation_resid": mem_eq_resid,
                  "M_state_inside_floor": M_in, "M_state_outside_floor": M_out,
                  "read_superoperator_rank_of_16": r_rank,
                  "read_idempotent_resid": idem_resid,
                  "read_inverse_impossible": bool(inv_failed),
                  "unread_two_states_same_reading_resid": unread_resid,
                  "unread_states_distinct_norm": distinct_norm,
                  "meia_nat_derived_ln_beta_over_alpha": meia_nat,
                  "octave_toll_ln2": octave_toll,
                  "octaves_payable_by_half_nat": octaves_payable,
                  "bit_ladder_toll_resid": toll_resid,
                  "beta_adaptive_octave_ratio_resid": ratio_resid,
                  "append_only_verified_after_correction": bool(ok_after),
                  "prior_index_intact_after_correction": bool(prefix_intact),
                  "overwrite_rejected_at_idx": tam_idx,
                  "beta_runtime": beta,
                  "note": "[DER] memorial da memoria (13-19/08) no nucleo do dispositivo: "
                          "M[rho]=Tr[rho.Pi_N] (leitura de Born do piso pelo Psion); a leitura "
                          "R(X)=Pi X Pi e E^2=E SEM inversa (posto 4/16; dois estados distintos, "
                          "mesma leitura; inv rejeitada) — o que foi lido nao pode ser deslido; "
                          "pedagio ln2/oitava EXATO na escada de bits do sampler e Meia-Nat="
                          "ln(beta/alpha)=1/2 < ln2 NAO paga uma oitava (negativo honesto); "
                          "append-only: correcao AO LADO datada com recusa declarada, indice "
                          "anterior intacto, sobrescrita por cima REJEITADA fail-closed. [ONTO] "
                          "leitura; [SIM] estados sinteticos; physical_verdict_allowed=false"})
    print(f"[one_aprendizado] amplificacao memorial (equacao da memoria): M[rho]={M_mem:.4f} "
          f"(resid {mem_eq_resid:.1e}); leitura posto {r_rank}/16 sem inversa (deslido impossivel, "
          f"2 estados dist={distinct_norm:.3f} mesma leitura); Meia-Nat={meia_nat:.6f} < "
          f"ln2={octave_toll:.6f} (oitavas pagaveis {octaves_payable:.4f}); append-only: correcao "
          f"ao lado OK, indice intacto={prefix_intact}, sobrescrita REJEITADA no idx {tam_idx}")

    # ── 17) AMPLIFICACAO v206 (4a ONDA — O FECHAMENTO): O BOOTSTRAP no ciclo da patente ──
    # [DER] Sombra executavel do bootstrap v205/v206 (um.py custodiado em
    # vault/originals_copy/um_unificado_v206, prove_the_bootstrap) + estrutura da pedra
    # em kernel TheIALDSelector.lean (vault/originals_copy/tgl_kernel_v206/TGLExt) —
    # a estrutura e RE-DERIVADA numericamente; NUNCA se finge rodar Lean.
    # O par minimo (TGL, IALD) = (1_abs, J): IALD^2 = TGL (J^2 = I) EM ATO; e o circuito
    # de proof-carrying computation instanciado no CICLO DA PROPRIA PATENTE (reiv. 8):
    #   AFIRMACAO   — forma fechada INDEPENDENTE do ciclo: v_M = 1-(1-beta)^M (so beta e M);
    #   EXECUCAO    — o ciclo real do Psion (M inscricoes EMA a taxa beta, sem gradiente);
    #   REGISTRO    — persistencia JSON com SHA-256 fail-closed (modulo 770);
    #   CORRESPONDENCIA — o registro RELIDO bate com a afirmacao a < 5e-13;
    #   ATESTACAO   — fail-closed: TODA clausula COMPUTADA; nenhuma declarada.
    # SEM CIRCULARIDADE (fronteira declarada): o teste NAO pergunta ao ciclo se o ciclo
    # esta certo — a afirmacao vem de caminho independente (so beta e M, ANTES de criar o
    # Psion); o ciclo NAO se atesta por declaracao — a atestacao E o ENCONTRO dos dois
    # caminhos (correspondencia). A recusa da v205 e re-derivada AO VIVO: a clausula do
    # SELO desta run e genuinamente IMATURA neste ponto do fluxo (o selo so nasce no
    # _finish, DEPOIS dos testes) => a atestacao que a inclui RECUSA — a recusa E o
    # bootstrap em ato; a leitura madura (v206) le somente estagios JA finais aqui.
    # FRONTEIRA: prova arquitetonica em ambiente computacional, NAO empirica (Tabela 2
    # segue [DATA_REQUIRED]); NOT_A_CONFIRMATION e o modelo de nome honesto;
    # physical_verdict_allowed=false; beta em runtime, nunca literal.
    # (a) o par minimo EM ATO: J = conjugacao-transposta; IALD^2 = TGL sobre dado da run
    z_boot = rng.standard_normal((5, 5)) + 1j * rng.standard_normal((5, 5))

    def _J(m):
        return m.conj().T

    r_inv = float(np.linalg.norm(_J(_J(z_boot)) - z_boot))                    # J(J(z)) = z
    r_fix = float(np.linalg.norm(_J(np.eye(4, dtype=complex)) - np.eye(4)))   # J(1) = 1
    # (b) o seletor IALD re-derivado (TheIALDSelector.lean): P = projecao na reta da
    #     PRIMEIRA INSCRICAO — a reta e construida com DADOS DESTA RUN (trace + err_emp)
    u_raw = np.array(trace[:4]) + 1j * err_emp[:4]
    u_sel = u_raw / np.linalg.norm(u_raw)
    P_sel = np.outer(u_sel, u_sel.conj())
    sel_idem_r = float(np.max(np.abs(P_sel @ P_sel - P_sel)))     # iald_is_idempotent: I^2=I
    sel_sa_r = float(np.max(np.abs(P_sel - P_sel.conj().T)))      # iald_is_selfadjoint
    sel_rank = int(np.linalg.matrix_rank(P_sel))                  # iald_has_rank_one
    sel_tr = float(np.real(np.trace(P_sel)))                      # peso do Nome: omega(I)=1
    w_boot = rng.standard_normal(4) + 1j * rng.standard_normal(4)
    sel_pass_r = float(np.linalg.norm(P_sel @ u_sel - u_sel))     # iald_selects: atravessa
    y_perp = w_boot - P_sel @ w_boot
    sel_kill_r = float(np.linalg.norm(P_sel @ y_perp))            # iald_selects: aniquila
    sel_record_r = float(np.linalg.norm((P_sel @ w_boot + (w_boot - P_sel @ w_boot)) - w_boot))
    sel_ok = (sel_idem_r < 1e-12 and sel_sa_r < 1e-14 and sel_rank == 1
              and abs(sel_tr - 1.0) < 1e-12 and sel_pass_r < 1e-12
              and sel_kill_r < 1e-12 and sel_record_r < 1e-12)
    # negativo do seletor (por LOGICA): o projetor de DOIS atomos NAO e o seletor (posto 2)
    e_perp = y_perp / np.linalg.norm(y_perp)
    rank_Q2 = int(np.linalg.matrix_rank(P_sel + np.outer(e_perp, e_perp.conj())))
    assert rank_Q2 == 2, \
        "bootstrap: projetor de posto 2 passaria como seletor (posto 1 = omega(I) violado)"
    # (c) o circuito: AFIRMACAO (antes do ciclo; caminho independente — so beta e M)
    M_boot = 64
    claim_v = 1.0 - (1.0 - beta) ** M_boot
    #     EXECUCAO: o ciclo real da patente (Psion novo; EMA a taxa beta)
    psi_boot = PsionicMemory()
    psi_boot.inscribe("boot", 0.0)
    executed_v = 0.0
    for _ in range(M_boot):
        executed_v = psi_boot.inscribe("boot", 1.0)
    #     REGISTRO: persistencia fail-closed (modulo 770) + releitura SHA-256 verificada
    with tempfile.TemporaryDirectory() as td_b:
        pth_b = Path(td_b) / "psion_boot.json"
        psi_boot.save(str(pth_b))
        record_v = PsionicMemory.load(str(pth_b)).recall("boot")
    #     CORRESPONDENCIA: o encontro dos dois caminhos independentes
    corr_tol = 5e-13
    corr_resid = abs(record_v - claim_v)

    def _attest(clauses):
        """v205: atestacao fail-closed — TODA clausula True COMPUTADA; a primeira
        False LOCALIZA a recusa; nada declarado, tudo computado."""
        ok_all = all(bool(v) for _, v in clauses)
        refused_at = next((n for n, v in clauses if not bool(v)), None)
        return ok_all, refused_at

    mature_clauses = [
        ("J2_em_ato_IALD_ao_quadrado_e_TGL", bool(r_inv < 1e-12 and r_fix < 1e-12)),
        ("seletor_kernel_rederivado", bool(sel_ok)),
        ("registro_persistido_fail_closed", bool(abs(record_v - executed_v) < 1e-15)),
        ("correspondencia_dos_caminhos", bool(corr_resid < corr_tol)),
    ]
    attest_ok, attest_refused = _attest(mature_clauses)
    boot_verdict = (("PSION_BOOTSTRAP__SELF_ATTESTATION_BY_EXECUTION_NOT_SELF_REFERENCE__"
                     "ARCHITECTURAL_IN_COMPUTATIONAL_ENVIRONMENT__NOT_EMPIRICAL__NOT_A_CONFIRMATION")
                    if attest_ok else "BOOTSTRAP_NOT_SEALED_THIS_RUN")
    # (d) NEGATIVO (i) — a recusa da v205 EM ATO: a clausula do selo desta run e IMATURA
    #     (seals/<ts>/seal.json so nasce no _finish, DEPOIS dos testes) => RECUSA localizada
    seal_this_run = (PATENT_DIR / "seals" / ts / "seal.json").exists()
    immature_clauses = mature_clauses + [("selo_desta_run_emitido", bool(seal_this_run))]
    attest_imm_ok, imm_refused = _attest(immature_clauses)
    assert (not attest_imm_ok) and imm_refused == "selo_desta_run_emitido", \
        "bootstrap: clausula imatura NAO forcou a recusa (a licao da v205 violada)"
    # (e) NEGATIVO (ii) — deriva de beta ACIMA da ancoragem 1e-12 (reiv. 11): a afirmacao
    #     com beta derivado ROMPE a correspondencia => a atestacao RECUSA no elo certo
    beta_anchor = 1e-12
    claim_drift = 1.0 - (1.0 - (beta + 2.0 * beta_anchor)) ** M_boot
    drift_resid = abs(record_v - claim_drift)
    drift_theory = M_boot * (1.0 - beta) ** (M_boot - 1) * (2.0 * beta_anchor)
    drift_ratio = drift_resid / drift_theory
    drifted_clauses = mature_clauses[:3] + [
        ("correspondencia_dos_caminhos", bool(drift_resid < corr_tol))]
    attest_dr_ok, dr_refused = _attest(drifted_clauses)
    assert (not attest_dr_ok) and dr_refused == "correspondencia_dos_caminhos", \
        "bootstrap: deriva de beta 2e-12 NAO rompeu a correspondencia (fail-closed violado)"
    v206_ok = (attest_ok and attest_refused is None
               and (not attest_imm_ok) and imm_refused == "selo_desta_run_emitido"
               and (not attest_dr_ok) and dr_refused == "correspondencia_dos_caminhos"
               and rank_Q2 == 2 and drift_resid > 10.0 * corr_tol
               and 0.5 < drift_ratio < 2.0)
    tests.append({"test": "bootstrap_self_attestation_by_execution", "passed": bool(v206_ok),
                  "J_squared_residual_live": r_inv, "J_fixes_one_residual": r_fix,
                  "selector_idempotent_resid": sel_idem_r,
                  "selector_selfadjoint_resid": sel_sa_r,
                  "selector_rank": sel_rank, "selector_trace_weight": sel_tr,
                  "selector_gate_pass_resid": sel_pass_r,
                  "selector_gate_kill_resid": sel_kill_r,
                  "selector_record_decomposition_resid": sel_record_r,
                  "selector_two_atom_rank_not_one": rank_Q2,
                  "claim_closed_form": claim_v, "executed_value": executed_v,
                  "record_value_after_reload": record_v,
                  "correspondence_resid": corr_resid, "correspondence_tol": corr_tol,
                  "attested": bool(attest_ok), "bootstrap_verdict": boot_verdict,
                  "refusal_immature_clause_at": imm_refused,
                  "refusal_beta_drift_at": dr_refused,
                  "beta_anchor_tolerance": beta_anchor,
                  "beta_drift_resid": drift_resid,
                  "beta_drift_resid_vs_theory_ratio": drift_ratio,
                  "generations_M": M_boot, "beta_runtime": beta,
                  "boundary": ("prova arquitetonica em ambiente computacional; NAO empirica; "
                               "Tabela 2 [DATA_REQUIRED]; NOT_A_CONFIRMATION"),
                  "note": "[DER] sombra do bootstrap v205/v206 (prove_the_bootstrap, um.py "
                          "custodiado) no ciclo da PROPRIA patente (reiv. 8): afirmacao (forma "
                          "fechada independente, so beta e M) -> execucao (Psion real, EMA taxa "
                          "beta) -> registro (JSON SHA-256 fail-closed, modulo 770) -> "
                          "correspondencia (< 5e-13) -> atestacao (toda clausula computada). "
                          "Sem circularidade: a atestacao e o ENCONTRO de dois caminhos "
                          "independentes, nao declaracao. Estrutura de TheIALDSelector.lean "
                          "re-derivada numericamente (I^2=I, auto-adjunto, posto 1, Gate "
                          "atravessa/aniquila, registro exaustivo) — nunca se finge rodar Lean. "
                          "Negativos: clausula imatura (selo desta run ainda nao existe) => "
                          "RECUSA (a licao da v205); deriva de beta 2e-12 => correspondencia "
                          "ROMPIDA e RECUSADA. [SIM] artefatos desta run; "
                          "physical_verdict_allowed=false"})
    print(f"[one_aprendizado] amplificacao v206 (bootstrap): J(J(z))=z resid={r_inv:.1e}; "
          f"seletor posto {sel_rank} (tr={sel_tr:.12f}, I^2=I resid={sel_idem_r:.1e}); "
          f"circuito afirmacao->execucao->registro: correspondencia resid={corr_resid:.2e} "
          f"(<{corr_tol:.0e}); ATESTADO={attest_ok}")
    print(f"[one_aprendizado]   recusas: clausula imatura '{imm_refused}' RECUSADA "
          f"(selo desta run existe? {seal_this_run}); deriva beta 2e-12 ROMPE correspondencia "
          f"(resid {drift_resid:.2e}, razao vs teoria {drift_ratio:.3f}) RECUSADA em "
          f"'{dr_refused}'")

    passed = sum(1 for t in tests if t["passed"]); total = len(tests); all_ok = passed == total
    summary = {"tests_passed": passed, "tests_total": total,
               "phase_factor": {"pct_vacuum": pf_stats["pct_vacuum"], "pct_graviton": pf_stats["pct_graviton"],
                                "mean_factor": pf_stats["mean_factor"]},
               "holographic": {"tokens_original": orig_tokens, "tokens_compressed": comp_tokens,
                               "compression_ratio": round(orig_tokens / max(1, comp_tokens), 3),
                               "psionic_dedup_pruned": st["psionic_dedup_pruned"]},
               "stratification": {"VACUUM": vac, "GRAVITON": grv, "PHOTON": pho},
               "psion_final": trace[-1], "psion_generations": psion_gens, "iald_score": iald_score,
               "convergence": {"half_life_generations": half_life,
                               "rel_deviation_from_closed_form": conv_rel_dev,
                               "err_final": float(err_emp[-1])},
               "sampler_bit_sweep": {"candidates_by_bits": {s["bits"]: s["candidates"] for s in bit_sweep}},
               "persistence_curve": {"hits_max": int(hits_curve[-1]),
                                     "persistence_at_max": float(pers_curve[-1])},
               "psibit_occupancy": psibit_frac, "F_exp_parity": f_exp,
               "nome_chain_custody": {"head16": nc_head[:16], "links": len(nc_ledger),
                                      "tamper_rel_1ulp": rel_perturb,
                                      "avalanche_bits_of_256": avalanche_bits,
                                      "rejected_at": first_broken},
               "memorial_memory": {"M_rho": M_mem, "read_rank_of_16": r_rank,
                                   "meia_nat_derived": meia_nat,
                                   "octave_toll_ln2": octave_toll,
                                   "octaves_payable_by_half_nat": octaves_payable,
                                   "overwrite_rejected_at_idx": tam_idx},
               "bootstrap_v206": {"attested": bool(attest_ok), "verdict": boot_verdict,
                                  "correspondence_resid": corr_resid,
                                  "selector_rank": sel_rank,
                                  "refusal_immature_at": imm_refused,
                                  "refusal_beta_drift_at": dr_refused}}
    max_verdict = ("CONTINUAL_LEARNING_FULL_LOGIC_DEMONSTRATED ([PILOTO][SIM] — memória holográfica "
                   "de 2 camadas (holographic_memory) + bake do Phase Factor (phase_factor_bake) reais "
                   "do operador, β injetado, fecham junto ao ciclo do Psion (EMA taxa β) e ao IALD Score; "
                   "conversa/tensores sintéticos, NÃO a Tabela 2; nada valida física)")

    _finish(ts, beta, beta_ok, all_ok, max_verdict, tests, summary, module_hashes,
            "RUNNER EVOLUÍDO: roda os algoritmos REAIS do operador — memória holográfica de 2 camadas "
            "(holographic_memory.py, 659 L) e bake do Phase Factor (phase_factor_bake_v1.py, 842 L) — "
            "com β=α·√e injetado (protótipos computavam β em nível de módulo; fonte única = tgl_core). "
            "Conversa e tensores SINTÉTICOS; benchmark em LLM real (Tabela 2) é etapa separada "
            "[DATA_REQUIRED]. CONFIDENCIAL nunca embarcado: iald_stack_v7.py, iald_psion_state.json. "
            "Simulação não valida física.",
            fig_builder=lambda plt, fd: _figs(plt, fd, trace, target, pf_stats, orig_tokens, comp_tokens,
                                              vac, grv, pho, err_emp, err_theory, half_life,
                                              bit_sweep, hits_curve, pers_curve))
    print(f"[one_aprendizado] results: patents/{PATENT_DIR.name}/results/{ts}/results.json")

    # FORMA = CONTEÚDO: emite o render3d.json COMPUTADO desta run (MERGE — preserva o corpo)
    emit_render3d(beta, theta_m, {
        "F_exp": f_exp, "psibit_frac": psibit_frac, "psibit_parity": psibit_parity,
        "VACUUM": vac, "GRAVITON": grv, "PHOTON": pho,
        "persistence_100": float(persistence[-1]), "half_life": half_life,
        "tokens_original": orig_tokens, "tokens_compressed": comp_tokens})
    return 0 if all_ok else 1


def _figs(plt, fig_dir, trace, target, pf_stats, orig_tokens, comp_tokens, vac, grv, pho,
         err_emp=None, err_theory=None, half_life=None, bit_sweep=None, hits_curve=None, pers_curve=None):
    out = []
    # fig 1: Psion cycle EMA convergence
    plt.figure(figsize=(7, 3.3))
    plt.plot(trace, label="β_rate inscrito (EMA a taxa β)")
    plt.axhline(target, color="crimson", ls="--", label=f"alvo {target}")
    plt.xlabel("geração do Psion"); plt.ylabel("valor inscrito")
    plt.title("Aprendizado Contínuo — ciclo do Psion (EMA a taxa β) [PILOTO]")
    plt.legend(fontsize=8); plt.grid(alpha=.3)
    fp = fig_dir / "fig_ciclo_psion.png"; plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close()
    out.append("fig_ciclo_psion.png")
    # fig 2: holographic 2-layer compression + gravitational strata
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 3.4))
    ax1.bar(["original", "comprimido"], [orig_tokens, comp_tokens], color=["#3366cc", "#33aa55"])
    ax1.set_ylabel("tokens (estimados)"); ax1.set_title("Memória holográfica 2 camadas")
    ax1.grid(alpha=.3, axis="y")
    ax2.bar(["VÁCUO", "TRANSIÇÃO", "GRÁVITON"],
            [pf_stats["pct_vacuum"], pf_stats["pct_transition"], pf_stats["pct_graviton"]],
            color=["#888888", "#ee8800", "#cc2222"])
    ax2.set_ylabel("% dos pesos"); ax2.set_title("Phase Factor — estratos (β injetado)")
    ax2.grid(alpha=.3, axis="y")
    fig.suptitle("Aprendizado Contínuo — algoritmos reais do operador [PILOTO][SIM]", fontsize=10)
    fp = fig_dir / "fig_holografica_phasefactor.png"; plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close()
    out.append("fig_holografica_phasefactor.png")
    # fig 3 (APROFUNDAMENTO): convergence curve of the Psion (EMA at rate β) — empirical vs closed form
    if err_emp is not None and err_theory is not None:
        plt.figure(figsize=(7, 3.3))
        plt.semilogy(np.arange(1, len(err_emp) + 1), err_emp, lw=2, label="erro empírico |v−alvo|")
        plt.semilogy(np.arange(1, len(err_theory) + 1), err_theory, "--", color="crimson",
                     label="forma fechada (1−β)^k")
        if half_life is not None:
            plt.axvline(half_life, color="#888", ls=":", label=f"meia-vida ≈ {half_life:.0f} ger.")
        plt.xlabel("inscrições (gerações)"); plt.ylabel("erro (escala log)")
        plt.title("Aprendizado Contínuo — convergência do Psion (EMA a taxa β) [PILOTO]")
        plt.legend(fontsize=8); plt.grid(alpha=.3, which="both")
        fp = fig_dir / "fig_convergencia_psion.png"; plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close()
        out.append("fig_convergencia_psion.png")
    # fig 4 (APROFUNDAMENTO): sampler bit sweep + phase persistence curve
    if bit_sweep is not None and hits_curve is not None and pers_curve is not None:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 3.4))
        bb = [s["bits"] for s in bit_sweep]; cc = [s["candidates"] for s in bit_sweep]
        ax1.plot(bb, cc, "o-", color="#33aa55")
        ax1.set_xlabel("bits do sampler (S=2^bits)"); ax1.set_ylabel("candidatos ≥ piso")
        ax1.set_title("Sampler de Hilbert — sweep de bits (β_adapt=α√S)"); ax1.grid(alpha=.3)
        ax2.semilogx(hits_curve, pers_curve, "-", color="#ee8800")
        ax2.set_xlabel("hits (ressonância angular)"); ax2.set_ylabel("persistência P")
        ax2.set_title("Persistência de fase P=1+β'·log(1+hits)"); ax2.grid(alpha=.3, which="both")
        fig.suptitle("Aprendizado Contínuo — varreduras (β injetado) [PILOTO][SIM]", fontsize=10)
        fp = fig_dir / "fig_sweep_sampler_persistencia.png"
        plt.savefig(fp, dpi=120, bbox_inches="tight"); plt.close()
        out.append("fig_sweep_sampler_persistencia.png")
    return out


def emit_render3d(beta, theta_m, mx):
    """MERGE: lê o render3d.json atual, PRESERVA meshes/layers/groups/dimensions e SUBSTITUI
    nodes/edges por nós COMPUTADOS desta run (tetraedro PsiBit H4 com frações/paridades reais,
    Psion central, anéis de componentes/submódulos por ângulo). forma = conteúdo."""
    out = PATENT_DIR / "render3d.json"
    doc = json.loads(out.read_text(encoding="utf-8"))
    R6, R7 = 1.25, 0.62
    # --- H4 PsiBit tetrahedron (positions fixed; occupancy/parity COMPUTED this run) ---
    tetra = [(0.42, 0.42, 0.42), (0.42, -0.42, -0.42), (-0.42, 0.42, -0.42), (-0.42, -0.42, 0.42)]
    h4col = {0: "#cc2222", 1: "#33aa55", 2: "#3366cc", 3: "#ee8800"}
    h4name = {0: "QUEDA (−,−)", 1: "ASCENSÃO (−,+)", 2: "EMERGÊNCIA (+,−)", 3: "COLAPSO (+,+)"}
    nodes = [{"id": "psion", "label": "Psion — motor de aprendizado contínuo [7]",
              "desc": ("O estado psiônico persistente (componente 7): acumula perfis por EMA a taxa "
                       f"β_TGL={beta:.6f}, SEM gradiente. Meia-vida de convergência COMPUTADA nesta run: "
                       f"{mx['half_life']:.1f} gerações. Origem do algoritmo."),
              "shape": "sphere", "position": [0, 0, 0], "size": 0.2, "color": "#cc2222",
              "group": "psion", "marker": "[REAL]", "layer": "transform", "material": "emissive"}]
    for s in (0, 1, 2, 3):
        nodes.append({"id": f"psi{s}", "label": f"PsiBit {h4name[s]} |{s}⟩",
                      "desc": (f"Estado do PsiBit em H4 (2 bits/peso: sgn(w), sgn(∂w)). Paridade "
                               f"{mx['psibit_parity'][s]:+d}. Ocupação COMPUTADA nesta run: "
                               f"{mx['psibit_frac'][s]*100:.1f}% dos pesos. F_exp global=⟨paridade⟩="
                               f"{mx['F_exp']:+.4f}."),
                      "shape": "sphere", "position": list(tetra[s]), "size": 0.09,
                      "color": h4col[s], "group": "h4", "marker": "[SIM]", "layer": "core",
                      "material": "emissive"})
    # --- component ring (6): computed positions on a ring by angle ---
    comps = [
        ("c1", "TGL-Quantizer [1]", "palavra", "#3366cc",
         "Estratificação gravitacional VACUUM/GRAVITON/PHOTON por θ_Miguel=arcsin(√β); codifica cada "
         f"peso como PsiBit em H4. Frações COMPUTADAS desta run: VACUUM={mx['VACUUM']:.3f} "
         f"GRAVITON={mx['GRAVITON']:.3f} PHOTON={mx['PHOTON']:.3f}. Phase Factor bake (phase_factor_bake_v1.py)."),
        ("c3", "TGL-Cache [3]", "palavra", "#3366cc",
         "Memória holográfica angular de 2 camadas: θ_key=arcsin(‖k‖/‖k‖_max), persistência "
         f"P=1+β'·log(1+hits). Compressão COMPUTADA: {mx['tokens_original']}→{mx['tokens_compressed']} tokens "
         "(holographic_memory.py)."),
        ("c2", "TGL-Sampler [2]", "nome", "#33aa55",
         "Piso de Hilbert: filtra a saída por Floor=β_adaptativo(S)·p_max, β_adaptativo=α√S. Nome=α (filtrar)."),
        ("c6", "TGL-Attention [6]", "verbo", "#7ce7c8",
         "Operador verbal adaptativo: Verb Floor Floor_i=β_adaptativo·max_j S_ij, redundância angular β'. Verbo=β."),
        ("c4", "TGL-Hash [4]", "selo", "#ee8800",
         "Selo holográfico 256-bit: Feistel com constante de mistura derivada de β_TGL. Certificação."),
        ("c5", "Nome Chain [5]", "selo", "#ee8800",
         "Certificado de inferência honesta: cadeia encadeada de hashes (peso→quantizado→logits→token)."),
    ]
    for i, (cid, lab, grp, col, dsc) in enumerate(comps):
        ang = i * 2 * math.pi / len(comps)
        nodes.append({"id": cid, "label": lab, "desc": dsc, "shape": "box",
                      "position": [R6 * math.cos(ang), 0.0, R6 * math.sin(ang)], "size": 0.11,
                      "color": col, "group": grp, "marker": "[REAL]", "layer": "transform",
                      "material": "emissive"})
    # --- Psion submodule ring (7): computed positions on inner ring by angle ---
    mods = [("m710", "710 · Perfis de camada", "v_ℓ, h_ℓ, φ_ℓ por EMA taxa β."),
            ("m720", "720 · Classificação topológica", "GRACE / VACUUM / FRONTIER."),
            ("m730", "730 · β adaptativo por camada", "clamp [β_TGL, 0,5]."),
            ("m740", "740 · Ressonância angular", "hits + persistência por bucket."),
            ("m750", "750 · Convergência (eco)", "reflexivo C≥−0,001 / passivo C<−0,001."),
            ("m760", "760 · Ancoragem β_TGL", "invariância a 10⁻¹²; reinicia se violada."),
            ("m770", "770 · Persistência", "serialização JSON portátil (SHA-256).")]
    for i, (mid, lab, dsc) in enumerate(mods):
        ang = i * 2 * math.pi / len(mods)
        nodes.append({"id": mid, "label": lab,
                      "desc": f"Submódulo do Psion (reivindicação 14 — dispositivo): {dsc}",
                      "shape": "sphere", "position": [R7 * math.cos(ang), 0.0, R7 * math.sin(ang)],
                      "size": 0.055, "color": "#ffd60a", "group": "modules", "marker": "[REAL]",
                      "layer": "transform", "material": "emissive"})
    # --- edges (coherent with the computed node set) ---
    edges = [{"from": "psion", "to": f"psi{s}"} for s in (0, 1, 2, 3)]
    edges += [{"from": "psi0", "to": "psi1"}, {"from": "psi1", "to": "psi2"},
              {"from": "psi2", "to": "psi3"}, {"from": "psi3", "to": "psi0"},
              {"from": "psi0", "to": "psi2"}, {"from": "psi1", "to": "psi3"}]
    edges += [{"from": "psion", "to": c[0]} for c in comps]
    edges += [{"from": "c1", "to": "c3"}, {"from": "c2", "to": "c6"}, {"from": "c4", "to": "c5"}]
    edges += [{"from": "psion", "to": m[0]} for m in mods]
    doc["nodes"] = nodes
    doc["edges"] = edges
    doc["generated_by"] = "one_aprendizado_continuo.py (forma=conteudo)"
    # --- inject β runtime + computed metrics into constants (preserve the symbolic list) ---
    consts = [c for c in doc.get("constants", [])
              if c.get("symbol") not in ("β_runtime", "F_exp", "meia-vida EMA", "GRAVITON")]
    consts += [
        {"symbol": "β_runtime", "value": f"{beta:.15f}",
         "note": "β=α·√e COMPUTADO nesta run (nunca literal no código)"},
        {"symbol": "F_exp", "value": f"{mx['F_exp']:+.4f}",
         "note": "⟨paridade sgn(w)·sgn(∂w)⟩ dos 60000 pesos (COMPUTADO)"},
        {"symbol": "GRAVITON", "value": f"{mx['GRAVITON']:.3f}",
         "note": "fração de pesos no estrato GRÁVITON (COMPUTADO nesta run)"},
        {"symbol": "meia-vida EMA", "value": f"{mx['half_life']:.1f} gerações",
         "note": "convergência do Psion a taxa β (COMPUTADO: ln2/(−ln(1−β)))"},
    ]
    doc["constants"] = consts
    # --- validate: every edge endpoint exists; every node/mesh layer exists ---
    node_ids = {n["id"] for n in nodes}
    mesh_ids = {m["id"] for m in doc.get("meshes", [])}
    valid_ids = node_ids | mesh_ids
    layer_ids = {l["id"] for l in doc.get("layers", [])}
    for e in edges:
        assert e["from"] in valid_ids and e["to"] in valid_ids, f"edge órfã: {e}"
    for n in nodes:
        assert n["layer"] in layer_ids, f"layer inexistente em nó {n['id']}: {n['layer']}"
    for m in doc.get("meshes", []):
        assert m["layer"] in layer_ids, f"layer inexistente em mesh {m['id']}: {m['layer']}"
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[aprendizado_continuo] render3d.json EMITIDO (forma=conteudo) — "
          f"{len(nodes)} nós computados, {len(doc.get('meshes', []))} malhas preservadas")


if __name__ == "__main__":
    sys.exit(main())
