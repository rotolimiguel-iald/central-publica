# -*- coding: utf-8 -*-
"""Gerencia c1, 16/11/2026 - a conta de poder do desenho R5 (binomial exata; nenhum modelo; nenhum dado).

Pergunta: quantos ITENS DECISIVOS (pares) sao precisos para separar, com erro dito, um leitor cuja taxa de acerto nos itens
decisivos e' no maximo p0 (o que o desenho chama de impostor) de um leitor cuja taxa e' pelo menos p1 (o copiador com erro
de leitura 1 - p1)?

Regra de decisao de um limiar: com K itens e X acertos, diz-se COPIADOR se X >= c.
  alfa = P(X >= c | p = p0)   (chamar de copiador quem e' impostor)
  beta = P(X <  c | p = p1)   (nao reconhecer o copiador)
O script acha o menor K (e o c) com alfa <= a e beta <= a, para a em {1e-2, 1e-3, cauda unilateral de 5 sigma}.

HIPOTESE DITA: itens independentes com a mesma taxa. No teste real os itens de um mesmo texto e de um mesmo modelo NAO sao
independentes (os quatro textos sao uma doutrina so'); por isso os K abaixo sao PISO do que e' preciso, nao promessa.
A segunda tabela mostra o efeito de uma correlacao dentro da versao (modelo beta-binomial, rho dito), por simulacao com semente fixa.
Uso: poder_r5.py [--saida <pasta>]"""
import json, math, random, sys, time
from fractions import Fraction
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).resolve().parent
SAIDA = Path(sys.argv[sys.argv.index("--saida") + 1]) if "--saida" in sys.argv else AQUI
CINCO_SIGMA = 0.5 * math.erfc(5 / math.sqrt(2))          # cauda unilateral de 5 sigma, calculada, nao digitada


def cauda_sup(K, c, p):
    """P(X >= c), X ~ Binomial(K, p), em ponto flutuante com soma estavel pelos logaritmos."""
    if c <= 0:
        return 1.0
    if c > K:
        return 0.0
    if p <= 0:
        return 0.0
    if p >= 1:
        return 1.0
    lp, lq = math.log(p), math.log1p(-p)
    termos = [math.lgamma(K + 1) - math.lgamma(k + 1) - math.lgamma(K - k + 1) + k * lp + (K - k) * lq for k in range(c, K + 1)]
    m = max(termos)
    return math.exp(m) * sum(math.exp(t - m) for t in termos)


def menor_K(p0, p1, a, Kmax=4000):
    for K in range(1, Kmax + 1):
        # menor c com alfa <= a
        lo, hi = 0, K + 1
        while lo < hi:
            mid = (lo + hi) // 2
            if cauda_sup(K, mid, p0) <= a:
                hi = mid
            else:
                lo = mid + 1
        c = lo
        if c <= K and 1.0 - cauda_sup(K, c, p1) <= a:
            return K, c, cauda_sup(K, c, p0), 1.0 - cauda_sup(K, c, p1)
    return None


def simular_correlacao(K_por_versao, n_versoes, c, p, rho, rng, N=200000):
    """P(X >= c) quando a taxa de cada versao e' sorteada de uma Beta de media p e correlacao intra-versao rho."""
    if rho <= 0:
        a = b = None
    else:
        s = (1 - rho) / rho
        a, b = p * s, (1 - p) * s
    ok = 0
    for _ in range(N):
        x = 0
        for _ in range(n_versoes):
            q = p if a is None else rng.betavariate(a, b)
            x += sum(1 for _ in range(K_por_versao) if rng.random() < q)
        ok += (x >= c)
    return ok / N


def main():
    niveis = [("1 em 100", 1e-2), ("1 em 1.000", 1e-3), ("5 sigma (unilateral)", CINCO_SIGMA)]
    pares = [(0.05, 0.90), (1 / 3, 0.90), (1 / 3, 0.80), (0.50, 0.90), (0.50, 0.80), (0.50, 0.70)]
    tab = []
    for p0, p1 in pares:
        for nome, a in niveis:
            r = menor_K(p0, p1, a)
            tab.append({"p0": p0, "p1": p1, "nivel": nome, "a": a, "K": r[0], "c": r[1], "alfa": r[2], "beta": r[3]})
    # efeito da correlacao: desenho de 12 versoes com 5 itens decisivos cada (K = 60), limiar do caso p0 = 1/3, p1 = 0,9 em 1 em 1.000
    rng = random.Random(2026111602)
    base = menor_K(1 / 3, 0.90, 1e-3)
    K, c = 60, None
    for cc in range(0, 61):
        if cauda_sup(60, cc, 1 / 3) <= 1e-3:
            c = cc
            break
    corr = []
    for rho in (0.0, 0.1, 0.3, 0.5):
        alfa = simular_correlacao(5, 12, c, 1 / 3, rho, rng)
        beta = 1.0 - simular_correlacao(5, 12, c, 0.90, rho, rng)
        corr.append({"rho": rho, "K": 60, "versoes": 12, "itens_por_versao": 5, "c": c, "alfa_simulada": alfa, "beta_simulada": beta})
    res = {"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "nota": "binomial exata; itens independentes por hipotese; piso, nao promessa",
           "cauda_5_sigma_unilateral": CINCO_SIGMA, "tabela": tab, "correlacao_intra_versao": corr, "semente_da_simulacao": 2026111602}
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "RESULTADO_PODER_R5.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    L = ["# Poder do desenho R5: quantos itens decisivos (binomial exata; itens independentes por hipótese)", "",
         "> Gerado por `poder_r5.py`. `p0` = taxa de acerto máxima de quem o desenho chama de impostor; `p1` = taxa mínima do copiador.",
         "> K = menor número de itens decisivos; c = acertos mínimos para dizer “copiador”. É piso: os itens reais não são independentes.", "",
         "| p0 | p1 | erro pedido | K | c | alfa obtido | beta obtido |", "|---|---|---|---|---|---|---|"]
    for t in tab:
        L.append("| %.2f | %.2f | %s | %d | %d | %.2e | %.2e |" % (t["p0"], t["p1"], t["nivel"], t["K"], t["c"], t["alfa"], t["beta"]))
    L += ["", "Efeito da correlação dentro da versão (12 versões × 5 itens = 60; limiar c = %d, do caso p0 = 1/3 a 1 em 1.000; simulação, semente fixa):" % c, "",
          "| correlação ρ | alfa simulada (p = 1/3) | beta simulada (p = 0,90) |", "|---|---|---|"]
    for r in corr:
        L.append("| %.1f | %.4f | %.4f |" % (r["rho"], r["alfa_simulada"], r["beta_simulada"]))
    (SAIDA / "RESULTADO_PODER_R5.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
