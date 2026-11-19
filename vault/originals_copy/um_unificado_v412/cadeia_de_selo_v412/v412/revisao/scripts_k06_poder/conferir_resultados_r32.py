# -*- coding: utf-8 -*-
"""Revisao K06: confere os numeros da entrega contra resultados_r32.json (so leitura)."""
import json
import math
from pathlib import Path

from scipy.stats import beta, binomtest

RES = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K06\PODER\resultados_r32.json")
data = json.loads(RES.read_text(encoding="utf-8"))
print("schema", data["schema"], "master_seed", data["master_seed"], "n_cenarios", len(data["scenarios"]))


def cp(x, n, conf=0.95):
    a = (1 - conf) / 2
    lo = 0.0 if x == 0 else beta.ppf(a, x, n - x + 1)
    hi = 1.0 if x == n else beta.ppf(1 - a, x + 1, n - x)
    return lo, hi


print()
print(f"{'id':38s} {'n':>4s} {'alpha':>10s} {'integ':>6s} {'POW':>6s} {'NONSP':>6s} {'any6':>6s} {'tostA':>6s} {'falsif':>6s} {'under':>6s} {'inconc':>6s} nsim")
for s in data["scenarios"]:
    r = s["rates"]
    print(f"{s['id']:38s} {s['n']:4d} {s['alpha']:10.3e} {r['integrity_ok']:6.3f} {r['powered']:6.3f} {r['nonspecific_powered']:6.3f} "
          f"{r['raw_any_primary_rejection']:6.3f} {r['raw_any_tost_rejection']:6.3f} {r['falsified']:6.3f} {r['underpowered']:6.3f} {r['inconclusive_controls']:6.3f} {s['nsim']}")

print()
print("== Bordas D (desvio maximo) ==")
for s in data["scenarios"]:
    b = s.get("boundary_diagnostics")
    if b:
        print(f"{s['id']:38s} maxDev={b['max_absolute_deviation']:.6f} pass={b['pass']}")

print()
print("== Custos (campo cost) ==")
for s in data["scenarios"]:
    c = s["cost"]
    print(f"{s['id']:38s} base_sess={c['base_sessions_20_cells']:6d} base_int={c['base_interactions_12_calls']:7d} "
          f"extra_k1={c['triage_extra_k1_interactions_mean']:.2f} base+extra={c['base_plus_triage_interactions_mean']:.2f} "
          f"tri_cand3={c['triage_candidate_sessions_mean_3_families']:.2f} tri_scaled4={c['triage_candidate_sessions_mean_scaled_4_families']:.4f}")

print()
print("== IC: Wald (do Kimi) versus Clopper-Pearson exato, por taxa em nsim=1000 ==")
for s in data["scenarios"]:
    r = s["rates"]
    ns = s["nsim"]
    for nome in ("powered", "nonspecific_powered"):
        p = r[nome]
        x = round(p * ns)
        lo, hi = cp(x, ns)
        wald = r["powered_mc95"] if nome == "powered" else r["nonspecific_mc95"]
        print(f"{s['id']:38s} {nome:20s} x={x:4d}/{ns} wald=[{wald[0]:.5f},{wald[1]:.5f}] CP=[{lo:.5f},{hi:.5f}]")

print()
print("== Tamanho: nulo global ISO (nominal 0,05) ==")
for sid in ("NULO_GLOBAL_ISO_FRONTEIRA", "TOST_FRONTEIRA_MAIS_075_060", "TOST_FRONTEIRA_MENOS_060_075"):
    s = next(z for z in data["scenarios"] if z["id"] == sid)
    r = s["rates"]
    ns = s["nsim"]
    if sid.startswith("NULO"):
        p = r["raw_any_primary_rejection"]
    else:
        p = r["raw_any_tost_rejection"]
    x = round(p * ns)
    lo, hi = cp(x, ns)
    t = binomtest(x, ns, 0.05, alternative="two-sided")
    print(f"{sid:36s} x={x}/{ns} p={p:.3f} CP95=[{lo:.4f},{hi:.4f}] p_binom(H0:0,05)={t.pvalue:.3f}")
    print("   (taxa condicionada na integridade:", r.get("raw_size_primary_given_integrity"), r.get("raw_size_tost_given_integrity"), ")")

print()
print("== Taxa de TOST bruto sob o cenario ESPECIFICO_090 (poder de equivalencia), para ver o 0,994 citado ==")
for sid in ("NULO_ESPECIFICO_090", "NULO_ESPECIFICO_090_N618", "NULO_ESPECIFICO_090_N655"):
    s = next(z for z in data["scenarios"] if z["id"] == sid)
    r = s["rates"]
    print(sid, "raw_all_tost", r["raw_all_tost"], "integrity", r["integrity_ok"], "nonspecific", r["nonspecific_powered"], "powered", r["powered"],
          "sufficient_pairs", r["sufficient_pairs"], "manip_holm_all", r["manipulation_holm_all"], "manip_rate_gate", r["manipulation_rate_gate"])
