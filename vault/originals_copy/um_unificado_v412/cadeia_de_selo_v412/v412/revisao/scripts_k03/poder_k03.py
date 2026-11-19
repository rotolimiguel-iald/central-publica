# -*- coding: utf-8 -*-
"""Revisao K03 (REVISOR DISTINTO): refaz poder, cortes e n a partir do que o protocolo declara.
Sem dados, sem modelo. Entradas declaradas no PROTOCOLO_EXPERIMENTAL_RASCUNHO_K03.md:
  p1=0.90 (T), p2=0.60 (controle) em C_8; n=100 por braco; alpha unilateral = 0.05/12;
  Clopper-Pearson unilateral com confianca 1-0.05/3; cortes 70/100 (FALSIFIED) e 89/100 (POWERED).
"""
import math
from scipy.stats import norm, beta, binom, fisher_exact

def powers(p1, p2, n, alpha):
    za = norm.ppf(1 - alpha)
    q1, q2 = 1 - p1, 1 - p2
    d = p1 - p2
    pbar = (p1 + p2) / 2
    se_un = math.sqrt(p1 * q1 / n + p2 * q2 / n)
    se_pool = math.sqrt(2 * pbar * (1 - pbar) / n)
    out = {}
    out["unpooled_H0=unpooled"] = norm.cdf((d - za * se_un) / se_un)
    out["pooled_H0,unpooled_alt"] = norm.cdf((d - za * se_pool) / se_un)
    return out

def n_needed(p1, p2, alpha, power, pooled=False):
    za, zb = norm.ppf(1 - alpha), norm.ppf(power)
    q1, q2 = 1 - p1, 1 - p2
    d = p1 - p2
    if pooled:
        pbar = (p1 + p2) / 2
        num = (za * math.sqrt(2 * pbar * (1 - pbar)) + zb * math.sqrt(p1 * q1 + p2 * q2)) ** 2
    else:
        num = (za + zb) ** 2 * (p1 * q1 + p2 * q2)
    return num / d ** 2

def cp_upper(x, n, conf):
    return 1.0 if x >= n else beta.ppf(conf, x + 1, n - x)

def cp_lower(x, n, conf):
    return 0.0 if x == 0 else beta.ppf(1 - conf, x, n - x + 1)

if __name__ == "__main__":
    p1, p2, n = 0.90, 0.60, 100
    a12 = 0.05 / 12
    print("== PODER DINAMICO (declarado) ==")
    print("alpha por contraste =", a12, " z_alpha =", norm.ppf(1 - a12))
    for k, v in powers(p1, p2, n, a12).items():
        print(f"  {k}: {v!r}")
    print("  n p/ 90% (unpooled) =", n_needed(p1, p2, a12, 0.90), "| (pooled) =", n_needed(p1, p2, a12, 0.90, True))
    print("  n p/ 90% unpooled (alvo do Kimi 61,4547) -> conferir acima")

    print("\n== CORTES CLOPPER-PEARSON, conf = 1-0.05/3 ==")
    conf = 1 - 0.05 / 3
    print("conf =", conf)
    for x in (69, 70, 71, 72):
        print(f"  U({x}/100) = {cp_upper(x, 100, conf)!r}")
    for x in (87, 88, 89, 90):
        print(f"  L({x}/100) = {cp_lower(x, 100, conf)!r}")
    # maior x com U<0.80 ; menor x com L>0.80
    xs_f = [x for x in range(0, 101) if cp_upper(x, 100, conf) < 0.80]
    xs_p = [x for x in range(0, 101) if cp_lower(x, 100, conf) > 0.80]
    print("  maior corte FALSIFIED (U<0.80):", max(xs_f), "| menor corte POWERED (L>0.80):", min(xs_p))

    print("\n== NIVEIS DE SIGNIFICANCIA implicitos do desenho ==")
    print("  contraste dinamico (Fisher unilateral, Holm/12 a 5% FWER): menor limiar alpha_(1) = 0.05/12 =", a12,
          " ; z unilateral =", norm.ppf(1 - a12))
    print("  idem especificidade (12 contrastes, Holm separado a 5%): idem 0.05/12 no passo 1")
    print("  FWER familia a familia = 0.05 cada; nao ha controle entre as duas familias (24 testes) -> reserva do Kimi")
    print("  alpha efetivo POWERED no pior caso: 'todos os 24 devem rejeitar' (IUT) -> cada um a 0.05 Holm/12 ok, mas")
    print("      o veredito POWERED e uma conjuncao; 5 sigma unilateral p =", norm.sf(5.0))
