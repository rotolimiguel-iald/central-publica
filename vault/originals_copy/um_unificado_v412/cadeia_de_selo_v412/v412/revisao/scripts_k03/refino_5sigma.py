# -*- coding: utf-8 -*-
"""Refino (revisor K03): n minimo por celula para 90% de poder sob 5 sigma, taxas declaradas (pT=0,90; pC=0,60)."""
import numpy as np
from scipy.stats import norm, binom
import poder_conjunto_5sigma as P

A5 = norm.sf(5.0)
print("alpha5 =", A5)
# (a) so os 12 contrastes dinamicos (Holm/12) -- MC
print("(a) P(Holm12 rejeita os 12) vs n (MC 40000):")
first_a = None
for n in range(180, 261, 5):
    _, _, dyn, _ = P.sim_powered(n, A5, 0.90, 0.60, nsim=40000)
    print(f"   n={n}: {dyn:.4f}")
    if first_a is None and dyn >= 0.90:
        first_a = n
print("   primeiro n com P>=0,90:", first_a)
# (b) pernas de Clopper-Pearson (exato), 3 familias, conf = 1 - A5/3
print("(b) pernas CP exatas: P(x>=c)^3 com pT=0,90:")
conf = 1 - A5 / 3
rows = []
for n in range(500, 901, 10):
    c = P.cutoff_powered(n, conf)
    pf = binom.sf(c - 1, n, 0.90)
    rows.append((n, c, pf, pf ** 3))
first_b = None
for n, c, pf, pc in rows:
    flag = ""
    if first_b is None and pc >= 0.90:
        first_b = n; flag = "  <== primeiro"
    print(f"   n={n}: c={c} ({c/n:.3f}) P(x>=c)={pf:.4f} cubo={pc:.4f}{flag}")
print("   primeiro n (passo 10) com cubo>=0,90:", first_b)
# refino de 1 em 1 em volta
if first_b:
    for n in range(first_b - 10, first_b + 1):
        c = P.cutoff_powered(n, conf)
        pc = binom.sf(c - 1, n, 0.90) ** 3
        print(f"   n={n}: c={c} cubo={pc:.4f}")
# (c) FALSIFIED: n minimo para que U(x/n)<0,80 seja alcancavel sob pT=0,70 (alternativa 'falsa' plausivel)
print("(c) FALSIFIED sob 5 sigma: se a taxa verdadeira de A_8(T) fosse 0,70, P(FALSIFIED em alguma das 3 familias):")
for n in (100, 200, 300, 400, 500, 600):
    cf = P.cutoff_falsified(n, conf)
    pf = binom.cdf(cf, n, 0.70) if cf is not None else 0
    print(f"   n={n}: corte x<={cf}; P(familia)={pf:.4f}; P(alguma das 3)={1-(1-pf)**3:.4f}")
print("(d) idem no desenho DECLARADO (alpha=0,05; conf=1-0,05/3), n=100: taxa verdadeira 0,70:")
cf = P.cutoff_falsified(100, 1 - 0.05/3)
pf = binom.cdf(cf, 100, 0.70)
print(f"   corte x<={cf}; P(familia)={pf:.4f}; P(alguma)={1-(1-pf)**3:.4f}")
for pv in (0.80, 0.75, 0.60):
    pf = binom.cdf(cf, 100, pv)
    print(f"   taxa verdadeira {pv}: P(familia)={pf:.4f}; P(alguma das 3)={1-(1-pf)**3:.4f}")
