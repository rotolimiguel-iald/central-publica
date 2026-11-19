import json, math
from statistics import NormalDist
N = NormalDist()
P = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json"
d = json.loads(open(P, "rb").read().decode("utf-8"))
core = d["core"]

ALPHA = 7.2973525693e-3  # CODATA 2018
beta = ALPHA * math.sqrt(math.e)
print("beta runtime", repr(beta))
m2 = beta * math.sin(math.pi/4)   # eV, E0 = 1 eV
dm2 = (m2**2) * 1e5               # x1e-5 eV^2
print("m2 meV", m2*1e3, "dm2_pred (x1e-5 eV2)", repr(dm2))

D90 = 5 + N.inv_cdf(0.90)
print("D90", repr(D90))

# neff
ne = core["neff_channel"]
print("neff_channel keys", list(ne.keys())[:30])
for k in ne:
    if "delta" in k.lower() or "dn" in k.lower():
        print("  ", k, ne[k] if not isinstance(ne[k], (dict, list)) else "...")
dNeff_core = ne.get("delta_neff") or ne.get("DeltaNeff") or None
dNeff = 9.9296062166 * beta
print("9.9296062166*beta", dNeff)
print("e^? : 9.9296 = ", 3*math.sqrt(math.e)*... if False else "")
dN = 0.11946607525373273
sigN = 0.045
D_N = dN / sigN
print("D_N", D_N, "sigma_N for D90", dN / D90)

planning = 7.388
sep = planning - dm2
print("sep", repr(sep))
# Stouffer iguais
DJ_req = math.sqrt(D90**2 - D_N**2)
sigJ_req = sep / DJ_req
print("DJ_req", DJ_req, "sigma_J_req", repr(sigJ_req), "rel to planning %", 100*sigJ_req/planning)
for sg in (0.024, 0.0264169, 0.02642):
    DJ = sep/sg
    lam = math.hypot(DJ, D_N)
    print("sigma_J", sg, "D_J", DJ, "lambda", lam, "poder", N.cdf(lam-5), "poder(5sigma, nao 6.28)", N.cdf(lam - 5))
# poder de 90% a 5 sigma: lambda >= 5 + z90 = D90 -> poder = Phi(lambda-5)
# dias vivos
for sg in (sigJ_req, 0.024):
    print("T_novo dias vivos para sigma", sg, "=", 207.2*(0.078/sg)**2, " (anos vivos", 207.2*(0.078/sg)**2/365.25, ")")
# D so JUNO
for sg in (0.0241, 0.024, 0.02216):
    print("D JUNO sozinho sigma", sg, sep/sg)
# D_N alone sigma for D90; with other pesos
# Ringdown
D10, D14 = 3.9346337577944936, 4.63741267778178
F10 = (D90/D10)**2; F14 = (D90/D14)**2
print("F10", F10, "F14", F14, "Neq10", 10*F10, "Neq14", 14*F14, "add10", 10*F10-10, "add14", 14*F14-14)
from datetime import date
o4a = (date(2024,1,16)-date(2023,5,24)).days
o4b = (date(2025,1,28)-date(2024,4,10)).days
print("O4a days", o4a, "O4b days", o4b, "sum", o4a+o4b, "sum+2 (inclusive)", o4a+o4b+2)
for win in (530, o4a+o4b, o4a+o4b+2):
    yrs = win/365.25
    print("window", win, "rate14", 14/yrs, "rate10", 10/yrs, "t10 meses", (10*F10-10)/(10/yrs)*12, "t14 meses", (14*F14-14)/(14/yrs)*12)
print("req/yr 6 months D10", (10*F10-10)/0.5, "D14", (14*F14-14)/0.5)
print("req/yr 6 months vs retro rates ratio D10", ((10*F10-10)/0.5)/(10/(530/365.25)), " D14", ((14*F14-14)/0.5)/(14/(530/365.25)))
