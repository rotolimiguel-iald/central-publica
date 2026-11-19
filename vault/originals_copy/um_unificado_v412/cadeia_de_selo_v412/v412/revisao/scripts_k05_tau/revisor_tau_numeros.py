# Revisor K05/tau (tarefa 1, 5, 6, 7): refaz TODOS os numeros do TAU_ESTRELA_R2.md a partir do core selado
# (clock_test_result_v369, SO LEITURA) e de constantes CODATA 2018 digitadas por mim. Independente do script do Kimi.
# beta = ALPHA_FINE_CODATA_2018 * sqrt(e) em runtime. Nenhum dado observado novo, nenhuma estatistica.
import json, math, hashlib
from pathlib import Path
CORE = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json")
OUT = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\revisao\scripts_k05_tau\revisor_tau_numeros_saida.json")

ALPHA_FINE_CODATA_2018 = 7.2973525693e-3
beta = ALPHA_FINE_CODATA_2018 * math.sqrt(math.e)
h = 6.62607015e-34
hbar = h / (2 * math.pi)
c = 299792458.0
e_C = 1.602176634e-19       # 1 eV em J (exato)
G2018 = 6.67430e-11
G_core = 6.674e-11          # o que o core v369 usa (tau_star_s do core)
m_u = 1.66053906660e-27
GM_earth = 3.986004418e14
GM_sun = 1.3271244e20
g_std = 9.80665
Mpc = 3.0856775814913673e22
H0 = 67.4e3 / Mpc

raw = CORE.read_bytes()
sha = hashlib.sha256(raw).hexdigest()
doc = json.loads(raw.decode("utf-8"))
res = doc["core"]["clock_test_result_v369"]
proto = doc["core"]["clock_test_protocol_v369"]
P1 = {p["id"]: p for p in res["P1"]["platforms"]}

out = {"core_sha256": sha, "beta": beta, "beta_core": res["beta_runtime"], "beta_diff": beta - res["beta_runtime"]}

tP = math.sqrt(hbar * G2018 / c**5)
tP_core = math.sqrt(hbar * G_core / c**5)
out["tP_G2018"] = tP
out["tP_Gcore"] = tP_core
out["tP_core_field"] = res["tau_star_s"]
out["tP_Gcore_vs_field_rel"] = (tP_core - res["tau_star_s"]) / res["tau_star_s"]

bounds = {k: v["tau_star_max_s"] for k, v in P1.items()}
bounds["atlas_1p8e-33"] = 1.8e-33
out["bounds"] = bounds

# (1) as 15,4058 e 17,3255 ordens
tau_gap = hbar / e_C
tau_ret = hbar / (beta * e_C)
def orders(tau, b): return math.log10(tau / b)
out["gap_1eV"] = {"tau": tau_gap, **{k: {"ratio": tau_gap / b, "orders": orders(tau_gap, b)} for k, b in bounds.items()}}
out["ret_1eV"] = {"tau": tau_ret, **{k: {"ratio": tau_ret / b, "orders": orders(tau_ret, b)} for k, b in bounds.items()}}

# (1b) margens para c* (tP_G2018 como o Kimi; tambem com tP do core)
cst = {"1": 1.0, "1/beta": 1 / beta, "sqrt2": math.sqrt(2), "2pi": 2 * math.pi, "4pi": 4 * math.pi}
out["cstar"] = {}
for name, v in cst.items():
    out["cstar"][name] = {"tau": v * tP, **{k: {"ratio": v * tP / b, "orders": orders(v * tP, b)} for k, b in bounds.items()}}
out["cstar_core_tP_1_over_beta"] = {k: orders(tP_core / beta, b) for k, b in bounds.items()}
out["cstar_core_tP_1"] = {k: orders(tP_core, b) for k, b in bounds.items()}

# o que o core diz sozinho
out["core_tau_star_alternatives"] = res["tau_star_alternatives"]
out["core_deficit_orders_bound"] = {k: v["deficit_orders_bound"] for k, v in P1.items()}

# (1c) alternativas v369 (Unruh-g, Terra, atomo Sr) vs campos selados
omega_sr = P1["sr87_kim2025"]["omega_rad_s"]
def Gam(tau, w): return 0.5 * beta * tau * w * w
alt = res["tau_star_alternatives"]
cands = {
  "unruh_g_Gamma_Sr_per_s": 2 * math.pi * c / g_std,
  "GM_earth_over_c3_Gamma_Sr_per_s": GM_earth / c**3,
  "Gm_atom_over_c3_Gamma_Sr_per_s": G_core * 87.0 * m_u / c**3,
}
out["alt_check"] = {}
for k, tau in cands.items():
    gcalc = Gam(tau, omega_sr)
    out["alt_check"][k] = {"tau": tau, "Gamma_calc": gcalc, "Gamma_sealed": alt[k], "rel_diff": abs(gcalc - alt[k]) / alt[k],
                           "orders_vs_Kim": {kk: orders(tau, b) for kk, b in bounds.items()}}
out["alt_atom_G2018"] = G2018 * 87.0 * m_u / c**3

# monopolo 1 eV
mono = 4 * math.pi * G2018 * e_C / c**5
out["mono_1eV"] = {"tau": mono, "over_tP": mono / tP, **{k: orders(mono, b) for k, b in bounds.items()}}

# (1d) tau_eff = max(tP, tau_hor)
def hor(E, G=G2018): return 4 * math.pi * G * E / c**5
E_sr_opt = hbar * omega_sr
E_sr_rest = 87.0 * m_u * c**2
tau_bh = 4 * math.pi * 60 * GM_sun / c**3
E_H = c**5 / (2 * G2018 * H0)
# massa critica dentro do raio de Hubble, calculada INDEPENDENTEMENTE da formula fechada
rho_c = 3 * H0**2 / (8 * math.pi * G2018)
R_H = c / H0
M_H = (4 * math.pi / 3) * rho_c * R_H**3
E_H_indep = M_H * c**2
out["hubble"] = {"H0_per_s": H0, "1/H0": 1 / H0, "E_H_closed": E_H, "E_H_independent": E_H_indep,
                 "E_H_rel": (E_H - E_H_indep) / E_H, "tau_hor_via_E": hor(E_H_indep), "2pi/H0": 2 * math.pi / H0,
                 "Gamma_over_H0_max": Gam(2 * math.pi / H0, H0) / H0, "pi_beta": math.pi * beta, "2beta/3": 2 * beta / 3}
sysrows = {}
for name, th in (("1eV", hor(e_C)), ("Sr_transicao", hor(E_sr_opt)), ("Sr_repouso", hor(E_sr_rest)),
                 ("60Msun", tau_bh), ("Hubble", 2 * math.pi / H0)):
    sysrows[name] = {"tau_hor": th, "max": max(tP, th), "soma": tP + th, "quadratura": math.hypot(tP, th),
                     "max_over_tP": max(tP, th) / tP, "soma_over_max_rel": (tP + th) / max(tP, th) - 1,
                     "quad_over_max_rel": math.hypot(tP, th) / max(tP, th) - 1}
sysrows["60Msun"]["GM_over_c3"] = 60 * GM_sun / c**3
out["sistemas"] = sysrows

# (1e) tres frequencias com tau = tP
out["freq"] = {"sqrt2/tP": math.sqrt(2) / tP, "2/tP": 2 / tP, "2/(beta tP)": 2 / (beta * tP), "ratio": (2 / (beta * tP)) / (2 / tP), "1/beta": 1 / beta}

# (3 Lema) N = E_P/u, E_P
E_P = math.sqrt(hbar * c**5 / G2018)
out["lema"] = {"E_P_J": E_P, "N_1eV": E_P / e_C, "tau_u_over_tP": tau_gap / tP, "tau_ret_over_tP": tau_ret / tP,
               "N": E_P / e_C, "N/beta": E_P / e_C / beta,
               "G_from_N": hbar * c**5 / ((E_P / e_C) ** 2 * e_C**2), "G2018": G2018,
               "tP_from_hbar_over_EP": hbar / E_P}
# protocolo: nomes das alternativas
out["protocol_tau_star_alternatives_text"] = proto["record"]["tau_star_alternatives"]
out["protocol_P3"] = proto["record"]["readings"]["P3_UNIVERSAL"]
OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

# impressao compacta
def f(x): return f"{x:.6g}"
print("core sha256", sha)
print("beta", repr(beta), "dif core", beta - res["beta_runtime"])
print("tP(G2018)", repr(tP), "tP(G_core)", repr(tP_core), "campo core", res["tau_star_s"], "rel", (tP_core - res["tau_star_s"]) / res["tau_star_s"])
for k, b in bounds.items(): print("cota", k, b)
print("--- gap ħ/(1eV)", tau_gap)
for k in bounds: print("  ", k, f(tau_gap / bounds[k]), f"{orders(tau_gap, bounds[k]):+.4f}")
print("--- ret ħ/(β·1eV)", tau_ret)
for k in bounds: print("  ", k, f(tau_ret / bounds[k]), f"{orders(tau_ret, bounds[k]):+.4f}")
print("--- c* margens (cota/tau em ordens, + = abaixo da cota)")
for n in cst:
    print("  c*=", n, f(cst[n] * tP), {k: f"{-orders(cst[n]*tP, b):.4f}" for k, b in bounds.items()})
print("1/beta com tP_core:", {k: f"{-v:.4f}" for k, v in out["cstar_core_tP_1_over_beta"].items()})
print("core: tP/beta vs 5sigma", alt["tP_over_beta_vs_clock_5sigma_orders"], "vs best matter", alt["tP_over_beta_vs_best_matter_bound_orders"])
print("--- alt check")
for k, v in out["alt_check"].items(): print("  ", k, "tau", f(v["tau"]), "rel_diff", v["rel_diff"], {kk: f"{vv:+.2f}" for kk, vv in v["orders_vs_Kim"].items()})
print("atom G2018", out["alt_atom_G2018"])
print("mono 1eV", mono, mono / tP, {k: f"{v:+.2f}" for k, v in ((k, orders(mono, b)) for k, b in bounds.items())})
print("--- sistemas")
for k, v in sysrows.items(): print("  ", k, {kk: f(vv) for kk, vv in v.items()})
print("Hubble", {k: f(v) for k, v in out["hubble"].items()})
print("--- freq", {k: f(v) for k, v in out["freq"].items()})
print("--- lema", {k: f(v) for k, v in out["lema"].items()})
