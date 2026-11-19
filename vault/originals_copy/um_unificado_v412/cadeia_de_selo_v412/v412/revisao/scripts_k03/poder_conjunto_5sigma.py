# -*- coding: utf-8 -*-
"""Revisao K03 (REVISOR DISTINTO). Poder do VEREDITO POWERED e n por celula para o degrau de 5 sigma.
Sem dados reais, sem modelo: so simulacao a partir das taxas que o proprio protocolo assume
(C_8: T=0,90; cada controle=0,60) e das regras que o protocolo declara.
Leis do desenho (PROTOCOLO_EXPERIMENTAL_RASCUNHO_K03.md):
  - 3 familias capazes x 4 controles = 12 contrastes dinamicos (Fisher unilateral, Holm FWER alpha);
  - POWERED exige x_A>=c e x_C>=c em cada uma das 3 familias (c = menor corte com limite inferior CP > 0,80,
    confianca 1-alpha/3) e os 12 contrastes dinamicos e os 12 de especificidade rejeitados.
  - Aqui A_8 >= C_8 por definicao; assume-se p_A(T)=p_C(T) (cota conservadora a favor do protocolo).
  - Especificidade: o protocolo nao declara taxas; assume-se rejeicao certa (cota SUPERIOR do poder).
"""
import math, sys
import numpy as np
from scipy.stats import norm, beta, binom, hypergeom

rng = np.random.default_rng(20261113)

def cp_lower(x, n, conf):
    return 0.0 if x == 0 else beta.ppf(1 - conf, x, n - x + 1)

def cp_upper(x, n, conf):
    return 1.0 if x >= n else beta.ppf(conf, x + 1, n - x)

def cutoff_powered(n, conf, thr=0.80):
    for x in range(n + 1):
        if cp_lower(x, n, conf) > thr:
            return x
    return None

def cutoff_falsified(n, conf, thr=0.80):
    best = None
    for x in range(n + 1):
        if cp_upper(x, n, conf) < thr:
            best = x
    return best

def fisher_table(n):
    xt = np.arange(n + 1)[:, None]
    xc = np.arange(n + 1)[None, :]
    # p unilateral (T > C): P(X >= xt), X ~ Hypergeom(M=2n, K=xt+xc, N=n)
    return hypergeom.sf(xt - 1, 2 * n, xt + xc, n)

def holm_reject_all(p, alpha):
    ps = np.sort(p, axis=-1)
    m = ps.shape[-1]
    thr = alpha / (m - np.arange(m))
    return np.all(ps <= thr, axis=-1)

def sim_powered(n, alpha, pT, pC, nsim=40000, fam_conf_div=3, pcs=(0.60,) * 4):
    """Probabilidade do ramo POWERED (cotas: especificidade rejeita sempre)."""
    conf = 1 - alpha / fam_conf_div
    c = cutoff_powered(n, conf)
    tab = fisher_table(n)
    xT = rng.binomial(n, pT, size=(nsim, 3))
    xC = np.stack([rng.binomial(n, pc, size=(nsim, 3)) for pc in pcs], axis=-1)  # (nsim,3,4)
    legs = np.all(xT >= c, axis=1) if c is not None else np.zeros(nsim, bool)
    p = tab[xT[:, :, None], xC]               # (nsim,3,4)
    p = p.reshape(nsim, 12)
    dyn = holm_reject_all(p, alpha)
    return c, legs.mean(), dyn.mean(), (legs & dyn).mean()

def pooled_n(p1, p2, alpha, power):
    za, zb = norm.ppf(1 - alpha), norm.ppf(power)
    pbar = (p1 + p2) / 2
    num = (za * math.sqrt(2 * pbar * (1 - pbar)) + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
    return num / (p1 - p2) ** 2

def pooled_power(p1, p2, n, alpha):
    za = norm.ppf(1 - alpha)
    pbar = (p1 + p2) / 2
    se0 = math.sqrt(2 * pbar * (1 - pbar) / n)
    se1 = math.sqrt(p1 * (1 - p1) / n + p2 * (1 - p2) / n)
    return norm.cdf(((p1 - p2) - za * se0) / se1)

if __name__ == "__main__":
    A5 = norm.sf(5.0)
    print("alpha(5 sigma, unilateral) =", A5)

    print("\n[1] PODER DO VEREDITO POWERED no desenho DECLARADO (n=100, alpha=0,05, p_T=0,90, controles 0,60)")
    for pT in (0.90, 0.92, 0.95, 0.97):
        c, legs, dyn, pw = sim_powered(100, 0.05, pT, 0.60)
        pb = 1 - binom.cdf(c - 1, 100, pT)
        print(f"  pT={pT}: corte c={c}; P(x>=c)/familia={pb:.4f}; cubo={pb**3:.4f}; "
              f"MC legs={legs:.4f}  Holm12 dinamicos={dyn:.4f}  POWERED(cota sup.)={pw:.4f}")

    print("\n[2] SENSIBILIDADE da taxa de controle (informativos C2/C3) no poder por contraste, n=100, alpha=0,05/12")
    for pc in (0.50, 0.60, 0.70, 0.75, 0.80, 0.85):
        print(f"  pC={pc}: poder(pooled)={pooled_power(0.90, pc, 100, 0.05/12):.4f}; "
              f"n p/ 90% = {pooled_n(0.90, pc, 0.05/12, 0.90):.1f}")

    print("\n[3] 5 SIGMA por familia de contrastes (Holm/12) com 90% de poder POR CONTRASTE, p_T=0,90 vs 0,60")
    ac = A5 / 12
    print(f"  alpha por contraste (Holm, passo mais estrito) = {ac:.6e}; z = {norm.isf(ac):.4f}")
    print(f"  n por braco (normal, H0 pooled) = {pooled_n(0.90, 0.60, ac, 0.90):.2f}")
    # versao exata Fisher, um contraste, n minimo para 90% (MC exato por soma binomial)
    def fisher_power_single(n, alpha, pT=0.90, pC=0.60):
        tab = fisher_table(n)
        pm = np.outer(binom.pmf(np.arange(n + 1), n, pT), binom.pmf(np.arange(n + 1), n, pC))
        return float((pm * (tab <= alpha)).sum())
    for n in range(60, 200, 5):
        pw = fisher_power_single(n, ac)
        if pw >= 0.90:
            print(f"  n exato Fisher p/ 90% por contraste (busca de 5 em 5) ~ {n} (poder {pw:.4f})")
            break

    print("\n[4] PODER CONJUNTO (3 familias x 4 controles; Holm/12; cortes CP com conf 1-alpha/3) sob 5 sigma")
    print("    alvo: P(POWERED) >= 0,90 com pT=0,90 e pC=0,60 (declaradas); especificidade rejeita sempre (cota sup.)")
    for pT in (0.90, 0.95):
        print(f"  --- pT={pT}")
        found = None
        for n in (100, 150, 200, 250, 300, 350, 400, 450, 500, 600, 800):
            c, legs, dyn, pw = sim_powered(n, A5, pT, 0.60, nsim=20000)
            cf = cutoff_falsified(n, 1 - A5 / 3)
            print(f"    n={n}: c_POWERED={c} ({c/n:.3f}) c_FALSIFIED={cf}; P(legs CP)={legs:.4f}; P(Holm12)={dyn:.4f}; P(POWERED)<={pw:.4f}")
            if found is None and pw >= 0.90:
                found = n
        print("    primeiro n da grade com P(POWERED)>=0,90:", found)
