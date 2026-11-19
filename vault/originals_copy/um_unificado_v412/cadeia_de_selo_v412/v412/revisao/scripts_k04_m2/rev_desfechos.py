# Revisor K04/M2 — item 3: tabela de desfechos REDERIVADA do zero (não usa o script do Kimi).
# Regra congelada: r = |m_obs - M| / sigma_m, sigma_m = 0.5*(s/mu_obs)*m_obs = 5 s / m_obs (1a ordem, no valor OBSERVADO), duas caudas.
import math, json
import numpy as np
from scipy.stats import norm
ALPHA = 0.0072973525693
beta = ALPHA*math.sqrt(math.e); M = beta*math.sin(math.pi/4)*1000.0; pred = (M/1000)**2/1e-5
MU0, S0 = 7.388, 0.078

def r_frozen(X, s):                     # vetorizado
    m = np.sqrt(10.0*X); return np.abs(m-M)*m/(5.0*s)

def P_ge(t, mean, sd, s, two_sided=True):
    """P(r>=t) EXATO para X~N(mean,sd^2), r pela regra congelada em m2 (duas caudas), via raízes da parábola m(M-m)=5ts."""
    mhi = (M + math.sqrt(M*M + 20*t*s))/2.0
    p = norm.sf((mhi**2/10.0 - mean)/sd)
    if two_sided:
        disc = M*M - 20*t*s
        if disc >= 0:
            ma, mb = (M - math.sqrt(disc))/2.0, (M + math.sqrt(disc))/2.0
            p += norm.cdf((mb**2/10.0 - mean)/sd) - norm.cdf((ma**2/10.0 - mean)/sd)
    return p

def P_ge_dm(t, mean, sd, s):            # métrica Δm² (duas caudas)
    return norm.sf((pred+t*s-mean)/sd) + norm.cdf((pred-t*s-mean)/sd)

def bands(mean, sd, s, f=P_ge):
    g1, g3, g5 = f(1, mean, sd, s), f(3, mean, sd, s), f(5, mean, sd, s)
    return dict(r_le_1=1-g1, r_1_3=g1-g3, r_3_5=g3-g5, r_ge_5=g5, r_lt_3=1-g3)

def bands_kimi_style(mean, sd, s):      # só a cauda superior (o que o script do Kimi calcula em m2): para provar a diferença
    f = lambda t, mean, sd, s: P_ge(t, mean, sd, s, two_sided=False)
    return bands(mean, sd, s, f)

def models(s):
    out = {}
    out["a1_independente_posterior_publico"] = (MU0, math.hypot(S0, s))
    out["a2_independente_verdade_previsao"]  = (pred, s)
    C = s*s
    out["b1_cumulativo_C=s2_posterior_publico"] = (MU0, math.sqrt(S0**2 + s**2 - 2*C))
    out["b2_cumulativo_C=s2_verdade_previsao_condicional"] = (pred + (C/S0**2)*(MU0-pred), math.sqrt(s**2 - C**2/S0**2))
    return out

precs = [("0,7 %", 0.007*MU0), ("0,5 %", 0.005*MU0), ("0,407121 %", 0.00407121*MU0), ("0,324061 %", 0.00324061*MU0), ("0,3 %", 0.003*MU0), ("Tabela 6 σ=0,024", 0.024)]
res = {}
for lab, s in precs:
    res[lab] = {}
    for name, (mean, sd) in models(s).items():
        b2 = bands(mean, sd, s)
        b1 = bands_kimi_style(mean, sd, s)
        bd = bands(mean, sd, s, P_ge_dm)
        # Monte Carlo (semente fixa, 1e6) aplicando a regra congelada diretamente a cada sorteio
        rng = np.random.default_rng(20261114)
        X = rng.normal(mean, sd, 1_000_000)
        r = r_frozen(X, s)
        mc = dict(r_le_1=float(np.mean(r<=1)), r_1_3=float(np.mean((r>1)&(r<3))), r_3_5=float(np.mean((r>=3)&(r<5))), r_ge_5=float(np.mean(r>=5)), r_lt_3=float(np.mean(r<3)))
        res[lab][name] = dict(mean=mean, sd=sd, exato_duas_caudas=b2, so_cauda_superior=b1, delta_m2_duas_caudas=bd, monte_carlo_1e6_semente_20261114=mc)

def pc(x): return "%9.4f %%" % (100*x)
for lab in res:
    print("=====", lab)
    for name, v in res[lab].items():
        e, u, mc, bd = v["exato_duas_caudas"], v["so_cauda_superior"], v["monte_carlo_1e6_semente_20261114"], v["delta_m2_duas_caudas"]
        print(" ", name, "mean=%.6f sd=%.6f" % (v["mean"], v["sd"]))
        print("     exato 2 caudas   : r<=1 %s | 1<r<3 %s | 3<=r<5 %s | r>=5 %s | r<3 %s" % tuple(pc(e[k]) for k in ("r_le_1","r_1_3","r_3_5","r_ge_5","r_lt_3")))
        print("     só cauda superior: r<=1 %s | 1<r<3 %s | 3<=r<5 %s | r>=5 %s | r<3 %s   (forma do script do Kimi)" % tuple(pc(u[k]) for k in ("r_le_1","r_1_3","r_3_5","r_ge_5","r_lt_3")))
        print("     MC 1e6           : r<=1 %s | 1<r<3 %s | 3<=r<5 %s | r>=5 %s | r<3 %s" % tuple(pc(mc[k]) for k in ("r_le_1","r_1_3","r_3_5","r_ge_5","r_lt_3")))
        print("     Δm² 2 caudas     : r<=1 %s | 1<r<3 %s | 3<=r<5 %s | r>=5 %s" % tuple(pc(bd[k]) for k in ("r_le_1","r_1_3","r_3_5","r_ge_5")))
json.dump(res, open("rev_desfechos_resultado.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
