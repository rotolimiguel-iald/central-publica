# Revisor K04/M2 — itens 2, 4, 5 (aritmética), 6 (aritmética). Só números públicos agregados.
import math, json, datetime as dt
ALPHA_FINE_CODATA_2018 = 0.0072973525693
beta = ALPHA_FINE_CODATA_2018 * math.sqrt(math.e)
M = beta * math.sin(math.pi/4) * 1000.0          # meV, E0 = 1 eV
pred = (M/1000.0)**2 / 1e-5                       # 1e-5 eV^2
print("beta", repr(beta)); print("m2_pred_meV", repr(M)); print("dm2_pred", repr(pred))

def r_m2(mu, s):          # regra congelada: sigma_m = 0.5*(s/mu)*m_obs  (primeira ordem, no valor observado)
    m = math.sqrt(10*mu); sm = 0.5*(s/mu)*m
    return abs(m-M)/sm
def r_dm(mu, s): return abs(mu-pred)/s

for nome, mu, s in [("JUNO207", 7.388, 0.078), ("JUNO59", 7.50, 0.12)]:
    print(nome, "r_m2=%.6f r_dm2=%.6f" % (r_m2(mu,s), r_dm(mu,s)))

# queda
print("queda 59->207 (m2):", r_m2(7.50,0.12), "->", r_m2(7.388,0.078))

# D / 5 sigma / D90
D90 = 5 + 1.2815515655446004
delta = 7.388 - pred
print("delta", delta, "sigma5(dm2)", delta/5, "rel", delta/5/7.388*100, "sigmaD90", delta/D90, "rel", delta/D90/7.388*100)
print("D(0.024) dm2", delta/0.024, " D(0.024) m2 (D=m|m-M|/(5s))", math.sqrt(73.88)*abs(math.sqrt(73.88)-M)/(5*0.024))
print("D90", D90)

# incremento
w1, w2 = 1/0.12**2, 1/0.078**2
mu_i = (w2*7.388 - w1*7.50)/(w2-w1); s_i = (w2-w1)**-0.5
print("incremento: mu=%.6f sigma=%.6f  r_dm=%.6f r_m2=%.6f  dist_to_7.50=%.6f sigma_inc" % (mu_i, s_i, r_dm(mu_i,s_i), r_m2(mu_i,s_i), abs(mu_i-7.50)/s_i))
# incremento: se erro fosse correlacionado (rho entre cumulativos): variância de diferença de estimadores nested: V(d)=V59 - V207 por eficiência (Hausman) -> mesma conta
print("Hausman nested: Var(X59 - X207) = 0.12^2-0.078^2 =", 0.12**2-0.078**2, "-> sd", math.sqrt(0.12**2-0.078**2), " (d = 7.50-7.388 = 0.112 ; z=%.4f)" % (0.112/math.sqrt(0.12**2-0.078**2)))

# SK-Gd
print("SK-Gd r_m2 (9.08,0.54) = %.6f ; r_dm=%.6f ; sigma5_m2" % (r_m2(9.08,0.54), r_dm(9.08,0.54)))
def sigma_for_5(mu):
    m = math.sqrt(10*mu); return 2*mu*abs(m-M)/(5*m)
s5 = sigma_for_5(9.08); print("sigma5 SK", s5, " T_tot = 411.52*(0.54/s5)^2 =", 411.52*(0.54/s5)**2, " adicional", 411.52*(0.54/s5)**2-411.52)
print("SK-Gd vs JUNO207 discrepancy: (9.08-7.388)/sqrt(0.54^2+0.078^2) =", (9.08-7.388)/math.hypot(0.54,0.078))
# NuFIT 6.1: +0.094 -0.10
print("NuFIT6.1 7.537 (+0.094/-0.10): sigma lado previsao = 0.10 -> r_m2=%.6f r_dm=%.6f ; Kimi sigma 0.094 -> r_m2=%.6f" % (r_m2(7.537,0.10), r_dm(7.537,0.10), r_m2(7.537,0.094)))
print("core NuFIT 7.53 +-0.10 -> r_m2=%.6f" % r_m2(7.53,0.10))
for nome,mu,s in [("SNO+ 7.91 (+.22/-.25)",7.91,0.25),("KamLAND 7.54 (+.19/-.18)",7.54,0.18),("Solares 6.10 (+.95/-.81)",6.10,0.95),("SNO+ rs final 7.59+-0.17",7.59,0.17),("Capozzi 7.48+-0.10",7.48,0.10),("Bari 7.465 (+.072/-.080)",7.465,0.08),("SK-Gd s+r 8.94 (+.46/-.47)",8.94,0.47)]:
    print(nome, "r_m2=%.6f r_dm=%.6f rel_sigma=%.3f%%" % (r_m2(mu,s), r_dm(mu,s), 100*s/mu))

# Calendário
START = dt.date(2025,8,26); CUT = dt.date(2026,5,18)
print("dias calendario START->CUT:", (CUT-START).days, " uptime se 207.2 live:", 207.2/(CUT-START).days)
sig5, sigD90 = delta/5, delta/D90
info = 207.2*0.078**2
for nome,t in (("5sigma",sig5),("D90",sigD90)):
    T = info/t**2
    print("sem piso", nome, "T_total=%.2f adicional=%.2f data(100%% vivo)=%s ; com uptime 78%%: +%.0f d -> %s" % (T, T-207.2, CUT+dt.timedelta(days=T-207.2), (T-207.2)/(207.2/(CUT-START).days), CUT+dt.timedelta(days=(T-207.2)/(207.2/(CUT-START).days))))
# brinquedo do projeto, full-reactor
a_full = 92*0.074**2; fl_full = 0.024**2 - a_full/2009.0
a_nom = 100*0.074**2; DAYS6 = (dt.date(2031,8,26)-START).days; fl_nom = 0.024**2 - a_nom/DAYS6
print("DAYS6", DAYS6, "s0_full %.9f s0_nom %.9f" % (math.sqrt(fl_full), math.sqrt(fl_nom)))
for nome,t in (("5sigma",sig5),("D90",sigD90)):
    Tf = a_full/(t**2-fl_full); Tn = a_nom/(t**2-fl_nom)
    print(nome, "full: %.3f d -> cal %.1f d -> %s | nominal: %.3f d -> %s" % (Tf, Tf*DAYS6/2009.0, START+dt.timedelta(days=Tf*DAYS6/2009.0), Tn, START+dt.timedelta(days=Tn)))
# o que o brinquedo prevê para sigma em 207.2 d (full) e em 59.1:
for T in (59.1, 207.2):
    print("brinquedo full-reactor T=%.1f -> sigma=%.5f (real: %s)" % (T, math.sqrt(a_full/T+fl_full), {59.1:0.12,207.2:0.078}[T]))
# Tabela 6 check: 100 nom ->0.074 ; 6 anos 0.024
print("check s(2009 full)=", math.sqrt(a_full/2009+fl_full), " s(92)=", math.sqrt(a_full/92+fl_full))
# piso 2 pontos
a2 = (0.078**2-0.12**2)/(1/207.2-1/59.1); s0sq = 0.078**2 - a2/207.2
print("2 pontos: a=%.6f s0=%.6f" % (a2, math.sqrt(s0sq)))
