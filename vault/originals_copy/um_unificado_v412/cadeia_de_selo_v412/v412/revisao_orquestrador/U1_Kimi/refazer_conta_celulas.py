# -*- coding: utf-8 -*-
"""Revisor Kimi, ORDEM 018, U1, item 3: refaz a regra das quatro combinacoes do zero,
com aritmetica exata (Fraction), e compara com RESULTADO_CELULAS_R6.json da gerencia.

Modelo conferido: 16 grupos; quatro celulas de 16 apresentacoes (c00, c01, c10, c11).
REGRA: passa se CADA celula tem >= K vereditos certos.
- um lado so, sem sortear: acerta 16 em duas celulas e 0 nas outras duas -> nunca passa (K >= 9 > 0... K>0 basta).
- um lado so, sorteando: acerta com probs a, 1-a, 1-b, b nas quatro celulas; pior caso em a, b.
- usa os dois lados com acerto q por veredito: sup(16,K,q)^4.
- metade/metade (compara / so a pagina): celulas c00,c01 sempre 16; c10,c11 ~ Bin(16, 1/2).
- controle letra igual: 8 paginas; passa com 7 ou 8: moeda e q=0.95.
- tabela T (total em 64): teto de Hoeffding para um lado so sorteando (media 32) e binomiais 0.80/0.90.
- regra antiga da R0: grupo inteiro (6 itens) em 9 de 16 grupos, erro e por item.
"""
import json, sys
from fractions import Fraction
from math import comb, exp
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
BASE = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\teste_frente_a_r6\REV1")
JSON = json.loads((BASE / "RESULTADO_CELULAS_R6.json").read_text(encoding="utf-8"))
G = 16

def supF(n, c, p):
    """P(X >= c), X ~ Bin(n, p), exato em Fraction."""
    p = Fraction(p)
    return float(sum(Fraction(comb(n, k)) * p**k * (1 - p)**(n - k) for k in range(c, n + 1)))

def infF(n, c, p):
    p = Fraction(p)
    return float(sum(Fraction(comb(n, k)) * p**k * (1 - p)**(n - k) for k in range(0, c + 1)))

print("== 1. pior caso de um lado so, sorteando: grade fina (4001 pontos) ==")
for K in (9, 10, 11, 12):
    melhor = Fraction(0)
    melhor_a = None
    for i in range(0, 4001):
        a = Fraction(i, 4000)
        f = Fraction(0)
        # f(a) = P(c00>=K|a) * P(c10>=K|1-a)  [as outras duas celulas sao o mesmo fator com b]
        s1 = sum(Fraction(comb(G, k)) * a**k * (1 - a)**(G - k) for k in range(K, G + 1))
        s2 = sum(Fraction(comb(G, k)) * (1 - a)**k * a**(G - k) for k in range(K, G + 1))
        f = s1 * s2
        if f > melhor:
            melhor, melhor_a = f, a
    um_lado = float(melhor) ** 2
    print(f"K={K}: pior um-lado = {um_lado:.10f}  (a* = {float(melhor_a):.4f})  | JSON: {JSON['cortes'][str(K)]['um_lado_so_sorteando_(pior_caso)']:.10f}  diff = {um_lado - JSON['cortes'][str(K)]['um_lado_so_sorteando_(pior_caso)']:.2e}")

print()
print("== 2. usa os dois lados, por acerto q de veredito: sup(16,K,q)^4 ==")
for K in (9, 10, 11, 12, 13, 14, 15, 16):
    for q in ("0.99", "0.95", "0.90", "0.85", "0.80", "0.75", "0.70"):
        meu = supF(G, K, Fraction(q)) ** 4
        deles = JSON["cortes"][str(K)]["usa_os_dois_lados_por_acerto_de_veredito"][q]
        if abs(meu - deles) > 1e-9:
            print(f"  DIVERGE K={K} q={q}: meu {meu:.12f} vs {deles:.12f}")
    print(f"K={K} conferido (7 valores de q)")

print()
print("== 3. metade/metade ==")
for K in (9, 10, 11, 12):
    meu = 1.0 * 1.0 * supF(G, K, Fraction(1, 2)) ** 2
    deles = JSON["cortes"][str(K)]["metade_pelos_dois_lados_metade_so_a_pagina"]
    print(f"K={K}: meu {meu:.10f} vs JSON {deles:.10f}  diff {meu-deles:.2e}")

print()
print("== 4. tabela T (teto de Hoeffding e binomiais 0.80/0.90) ==")
for c, v in JSON["T"].items():
    c = int(c); t = c - 2 * G
    h = exp(-2.0 * t * t / (4 * G))
    ok_h = abs(h - v["teto_de_Hoeffding_para_um_lado_so"]) < 1e-12
    meu80 = supF(4 * G, c, Fraction(80, 100)); meu90 = supF(4 * G, c, Fraction(90, 100))
    ok = ok_h and abs(meu80 - v["usa_os_dois_lados_0_80"]) < 1e-9 and abs(meu90 - v["usa_os_dois_lados_0_90"]) < 1e-9
    if not ok:
        print(f"  DIVERGE c={c}: h {h:.6e} vs {v['teto_de_Hoeffding_para_um_lado_so']:.6e}; 0.80 {meu80:.6f} vs {v['usa_os_dois_lados_0_80']:.6f}; 0.90 {meu90:.6f} vs {v['usa_os_dois_lados_0_90']:.6f}")
print("  (so' se imprime o que diverge; nada acima = tudo confere)")

print()
print("== 5. regra antiga da R0 (grupo inteiro, 9 de 16) ==")
for ek, v in JSON["grupo_inteiro_9_de_16_(regra_da_R0)"].items():
    e = Fraction(int(ek.split("_")[1].split(".")[1]), 100)
    pg = float((1 - e) ** 6)
    julga = supF(16, 9, Fraction(pg).limit_denominator(10**12))
    # cuidado: pg nao e' decimal exato; uso Fraction direto:
    pgF = (1 - e) ** 6
    def supFx(n, c, p):
        return float(sum(Fraction(comb(n, k)) * p**k * (1 - p)**(n - k) for k in range(c, n + 1)))
    def pmfF(n, k, p):
        return float(Fraction(comb(n, k)) * p**k * (1 - p)**(n - k))
    julga = supFx(16, 9, pgF); sem = pmfF(16, 7, pgF) + pmfF(16, 8, pgF)
    def infFx(n, c, p):
        return float(sum(Fraction(comb(n, k)) * p**k * (1 - p)**(n - k) for k in range(0, c + 1)))
    naoj = infFx(16, 6, pgF)
    print(f"{ek}: taxa {float(pgF):.6f} vs {v['taxa_de_grupo']:.6f} | julga {julga:.6f} vs {v['julga_(X>=9)']:.6f} | sem {sem:.6f} vs {v['sem_rotulo_(7_ou_8)']:.6f} | naoj {naoj:.6f} vs {v['nao_julga_(X<=6)']:.6f}")

print()
print("== 6. numeros derivados lidos no desenho e na partitura ==")
print(f"letra igual, passa com 7 ou 8: moeda {supF(8, 7, Fraction(1,2)) * 100:.2f} % (desenho: 3,5 %) ; q=0.95: {supF(8, 7, Fraction(95,100)) * 100:.2f} % (desenho: 94 %)")
print(f"K=10, q=0.90: {supF(16, 10, Fraction(9,10)) ** 4 * 100:.2f} % (textos: 99,8 %)")
print(f"K=10, q=0.80: {supF(16, 10, Fraction(8,10)) ** 4 * 100:.2f} % (textos: 89,8 %)")
print(f"K=10, q=0.70: {supF(16, 10, Fraction(7,10)) ** 4 * 100:.2f} % (textos: 46,3 %)")
print(f"K=11, q=0.80: {supF(16, 11, Fraction(8,10)) ** 4 * 100:.2f} % (secao 9.3: 'sete de dez')")
print(f"K=12, q=0.80: {supF(16, 12, Fraction(8,10)) ** 4 * 100:.2f} % (secao 9.3: 'quatro de dez')")
print(f"metade/metade K=10: {supF(16, 10, Fraction(1,2)) ** 2 * 100:.2f} % (textos: 5,2 %)")
print(f"R0, erro 0.20, nao julga: ver acima (textos: 90 %)")
print(f"esperados por celula: q=0.90 -> {16 * 0.9:.1f} (texto 'cerca de 14'); q=0.80 -> {16 * 0.8:.1f} ('cerca de 13'); q=0.70 -> {16 * 0.7:.1f} ('cerca de 11'); moeda -> 8")

print()
print("== 7. quem confere cada lado com o que sabe de cor: celulas (16,16,16,0) -> nunca passa (K>=9>0): confere com a tabela da secao 6 ==")
print("== 8. corte do vazamento sem indice: 42+ vereditos em 64 sob moeda ==")
print(f"P(X>=42 | Bin(64, 1/2)) = {supF(64, 42, Fraction(1,2)) * 100:.4f} %  (referencia: T2 dizia 0,84 % para um lado so; sob moeda da isto)")
