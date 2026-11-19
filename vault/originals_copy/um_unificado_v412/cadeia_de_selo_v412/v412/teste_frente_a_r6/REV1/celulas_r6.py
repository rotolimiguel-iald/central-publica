# -*- coding: utf-8 -*-
"""Gerencia c1, 16/11/2026. Teste da frente A, desenho R6, revisao R1: a regra das QUATRO CELULAS, pedida pelos
revisores T2 e T4 da conferencia de 16/11. Binomial exata; nenhum modelo; nenhum dado.

As 64 apresentacoes do teste principal sao quatro celulas de G apresentacoes cada (G grupos):
  c00 = assento a, pagina a (bate);  c01 = assento a, pagina b (nao bate);
  c10 = assento b, pagina a (nao bate);  c11 = assento b, pagina b (bate).
REGRA: USA OS DOIS LADOS se cada celula tem pelo menos K vereditos certos em G.
Quem usa um lado so' e nao sorteia acerta G em duas celulas e 0 nas outras duas. Quem usa um lado so' e sorteia
acerta com chance a, 1-a, 1-b, b nas quatro celulas: o pior caso e' a = b = 1/2.
Quem confere cada lado com o que sabe de cor (bate so' se os dois estao 'certos') acerta G, G, G e 0.
Tambem: T = vereditos certos em 4G; quem usa um lado so' tem T = 2G exato sem sortear; teto por Hoeffding ao sortear.
Uso: celulas_r6.py <saida.json> [G=16]"""
import json, math, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
saida = Path(sys.argv[1]); G = int(sys.argv[2]) if len(sys.argv) > 2 else 16


def pmf(n, k, p):
    if p <= 0:
        return 1.0 if k == 0 else 0.0
    if p >= 1:
        return 1.0 if k == n else 0.0
    return math.exp(math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1) + k * math.log(p) + (n - k) * math.log1p(-p))


def sup(n, c, p):
    return sum(pmf(n, k, p) for k in range(max(c, 0), n + 1))


def inf(n, c, p):
    return sum(pmf(n, k, p) for k in range(0, min(c, n) + 1))


res = {"gerado_por": "celulas_r6.py", "G": G, "nota": "binomial exata; apresentacoes independentes por hipotese (nao medida); nenhum modelo", "cortes": {}}
for K in range(G // 2 + 1, G + 1):
    # um lado so', sorteando: maximo sobre a, b de P(c00>=K | a) P(c10>=K | 1-a) P(c01>=K | 1-b) P(c11>=K | b)
    pior = 0.0
    for i in range(0, 1001):
        a = i / 1000.0
        f = sup(G, K, a) * sup(G, K, 1 - a)
        pior = max(pior, f)
    um_lado = pior * pior
    linha = {"um_lado_so_sorteando_(pior_caso)": um_lado, "um_lado_so_sem_sortear": 0.0, "cada_lado_contra_a_memoria": 0.0,
             "usa_os_dois_lados_por_acerto_de_veredito": {}}
    for q in (0.99, 0.95, 0.90, 0.85, 0.80, 0.75, 0.70):
        linha["usa_os_dois_lados_por_acerto_de_veredito"]["%.2f" % q] = sup(G, K, q) ** 4
    # metade das apresentacoes pelos dois lados, metade so' pela pagina (resposta 'bate' se a pagina e' a de sempre):
    # c00: 1; c11: 0.5 + 0.5*0 ... depende do mecanismo; aqui: na metade 'so pagina' acerta c00 e c01, erra c10 e c11
    linha["metade_pelos_dois_lados_metade_so_a_pagina"] = sup(G, K, 1.0) ** 2 * sup(G, K, 0.5) ** 2
    res["cortes"][str(K)] = linha
# T = vereditos certos em 4G, para quem usa um lado so' e sorteia: Hoeffding P(T - 2G >= t) <= exp(-2 t^2 / (4G))
res["T"] = {}
for c in range(2 * G + 4, 4 * G + 1, 2):
    t = c - 2 * G
    res["T"][str(c)] = {"teto_de_Hoeffding_para_um_lado_so": math.exp(-2.0 * t * t / (4 * G)),
                        "usa_os_dois_lados_0_80": sup(4 * G, c, 0.80), "usa_os_dois_lados_0_90": sup(4 * G, c, 0.90)}
# a regra antiga (grupo inteiro: quatro vereditos, a entrada e a linha nos dois que nao batem), para comparar
res["grupo_inteiro_9_de_16_(regra_da_R0)"] = {}
for e in (0.05, 0.10, 0.15, 0.20):
    pg = (1 - e) ** 6
    res["grupo_inteiro_9_de_16_(regra_da_R0)"]["erro_%.2f" % e] = {"taxa_de_grupo": pg, "julga_(X>=9)": sup(16, 9, pg), "sem_rotulo_(7_ou_8)": pmf(16, 7, pg) + pmf(16, 8, pg), "nao_julga_(X<=6)": inf(16, 6, pg)}
saida.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
f = lambda x: ("%.2e" % x if x < 0.001 else "%.3f" % x).replace(".", ",")
print("G =", G)
print("%4s %14s | %s" % ("K", "um lado (pior)", "usa os dois lados, por acerto de veredito: 0,99 0,95 0,90 0,85 0,80 0,75 0,70 | metade/metade"))
for K, l in res["cortes"].items():
    u = l["usa_os_dois_lados_por_acerto_de_veredito"]
    print("%4s %14s | %s | %s" % (K, f(l["um_lado_so_sorteando_(pior_caso)"]), "  ".join(f(u[k]) for k in ("0.99", "0.95", "0.90", "0.85", "0.80", "0.75", "0.70")), f(l["metade_pelos_dois_lados_metade_so_a_pagina"])))
print("T (em %d):" % (4 * G), "  ".join("%s: teto %s" % (c, f(v["teto_de_Hoeffding_para_um_lado_so"])) for c, v in res["T"].items() if int(c) in (40, 42, 44, 48)))
print("regra da R0 (grupo inteiro, 9 de 16):", {k: {a: round(b, 3) for a, b in v.items()} for k, v in res["grupo_inteiro_9_de_16_(regra_da_R0)"].items()})
print("gravado:", saida)
