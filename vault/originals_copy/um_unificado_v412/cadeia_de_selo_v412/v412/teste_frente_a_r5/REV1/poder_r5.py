# -*- coding: utf-8 -*-
"""Gerencia c1, 16/11/2026, R1 (depois da conferencia distinta) - a regra de decisao e o poder do desenho R5.
Binomial exata; nenhum modelo; nenhum dado.

O QUE MUDOU NA R1 (achados da conferencia): a unidade e' o GRUPO (duas versoes complementares do mesmo texto), nao o
item; a regra tem DOIS limiares e quatro saidas; os portoes tem limiar proprio; a linha de 5 sigma saiu (nao cabe num
teste com poucos grupos de um sistema e uma doutrina).

A REGRA, com G grupos e X grupos certos:
  cA = menor c com P(X >= c | taxa p0) <= a      (acima disso rejeita-se 'nao le')
  cB = maior c com P(X <= c | taxa p1) <= a      (abaixo disso rejeita-se 'le')
  SEGUE         se X >= cA e X > cB
  NAO_SEGUE     se X <= cB e X < cA
  LE_EM_PARTE   se cA <= X <= cB                  (as duas hipoteses rejeitadas)
  SEM_PODER     se cB < X < cA                    (nenhuma rejeitada)
p0 = a taxa de grupos certos ate' a qual o sistema ainda e' chamado de 'nao le'; p1 = a taxa minima exigida de quem le.

HIPOTESE DITA: grupos independentes com a mesma taxa. Os grupos sao de textos e afirmacoes diferentes, mas o sistema
e' um so' e a doutrina e' uma so': a independencia entre grupos NAO esta' medida (nenhum modelo foi rodado).
Uso: poder_r5.py [--saida <pasta>]"""
import json, math, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).resolve().parent
SAIDA = Path(sys.argv[sys.argv.index("--saida") + 1]) if "--saida" in sys.argv else AQUI


def pmf(K, k, p):
    if p <= 0:
        return 1.0 if k == 0 else 0.0
    if p >= 1:
        return 1.0 if k == K else 0.0
    return math.exp(math.lgamma(K + 1) - math.lgamma(k + 1) - math.lgamma(K - k + 1) + k * math.log(p) + (K - k) * math.log1p(-p))


def cauda_sup(K, c, p):
    return sum(pmf(K, k, p) for k in range(max(c, 0), K + 1))


def cauda_inf(K, c, p):
    return sum(pmf(K, k, p) for k in range(0, min(c, K) + 1))


def limiares(G, p0, p1, a):
    cA = next((c for c in range(0, G + 1) if cauda_sup(G, c, p0) <= a), None)
    cB = next((c for c in range(G, -1, -1) if cauda_inf(G, c, p1) <= a), None)
    return cA, cB


def rotulo(X, cA, cB):
    seg = cA is not None and X >= cA and (cB is None or X > cB)
    nao = cB is not None and X <= cB and (cA is None or X < cA)
    if seg:
        return "SEGUE"
    if nao:
        return "NAO_SEGUE"
    if cA is not None and cB is not None and cA <= X <= cB:
        return "LE_EM_PARTE"
    return "SEM_PODER"


def grupo_certo(m, tol, q_par):
    """P(um grupo de 2m pares ter no maximo `tol` pares errados), com cada par certo com probabilidade q_par."""
    return cauda_sup(2 * m, 2 * m - tol, q_par)


def main():
    niveis = [("1 em 100", 1e-2), ("1 em 1.000", 1e-3)]
    taxas = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    regras = []
    for G in (4, 6, 8, 13):
        for p0, p1 in ((0.05, 0.90), (0.25, 0.90), (0.05, 0.80), (0.25, 0.80)):
            for nome, a in niveis:
                cA, cB = limiares(G, p0, p1, a)
                rot = [rotulo(X, cA, cB) for X in range(G + 1)]
                por_taxa = {}
                for r in taxas:
                    d = {}
                    for X in range(G + 1):
                        d[rot[X]] = d.get(rot[X], 0.0) + pmf(G, X, r)
                    por_taxa["%.1f" % r] = d
                regras.append({"G": G, "p0": p0, "p1": p1, "nivel": nome, "a": a, "cA": cA, "cB": cB, "rotulo_por_X": rot,
                               "alfa": (cauda_sup(G, cA, p0) if cA is not None else None),
                               "beta": (cauda_inf(G, cB, p1) if cB is not None else None), "P_rotulo_por_taxa": por_taxa})
    # do acerto por resposta ao acerto por grupo
    conv = []
    for m in (3, 5):
        for tol in (0, 1, 2):
            linha = {"m": m, "tocadas": 2 * m, "tolerancia": tol, "por_acerto_de_resposta": {}}
            for q in (0.99, 0.95, 0.90, 0.85, 0.80, 0.70):
                linha["por_acerto_de_resposta"]["%.2f" % q] = grupo_certo(m, tol, q * q)      # o par pede as DUAS respostas certas
            linha["moeda_um_em_quatro_por_par"] = grupo_certo(m, tol, 0.25)
            linha["meio_a_meio_por_par"] = grupo_certo(m, tol, 0.5)
            conv.append(linha)
    # portao com limiar proprio: os itens DITOS do texto-base (89 nos quatro textos)
    portoes = []
    for N in (89,):
        for p1 in (0.90, 0.80):
            for nome, a in niveis:
                c = next((c for c in range(N, -1, -1) if cauda_inf(N, c - 1, p1) <= a), None)   # passa com X >= c
                portoes.append({"itens": N, "p1": p1, "nivel": nome, "passa_com": c, "bom_leitor_passa": cauda_sup(N, c, p1),
                                "quem_esta_em_0_67_passa": cauda_sup(N, c, 0.67), "quem_esta_em_0_50_passa": cauda_sup(N, c, 0.50)})
    res = {"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "revisao": "R1",
           "nota": "binomial exata; grupos independentes por hipotese (nao medida); nenhum modelo; nenhum dado",
           "regras": regras, "do_acerto_por_resposta_ao_grupo": conv, "portoes": portoes}
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "RESULTADO_PODER_R5.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    f = lambda x: "—" if x is None else ("%.2e" % x if x < 0.001 else "%.3f" % x).replace(".", ",")
    L = ["# A regra de decisão e o poder do desenho R5, revisão R1 (binomial exata; nenhum modelo)", "",
         "> Gerado por `poder_r5.py`. Unidade = o grupo (duas versões complementares do mesmo texto). Grupos independentes por hipótese, não medida.",
         "> `cA` = a partir de quantos grupos certos se diz SEGUE; `cB` = até quantos se diz NÃO SEGUE. Entre os dois: LÊ EM PARTE (se cA ≤ cB) ou SEM PODER.", "",
         "## Os limiares", "", "| grupos | p0 | p1 | erro pedido | cA (SEGUE se ≥) | cB (NÃO SEGUE se ≤) | o meio | erro de dizer SEGUE a quem está em p0 | erro de dizer NÃO SEGUE a quem está em p1 |", "|---|---|---|---|---|---|---|---|---|"]
    for r in regras:
        meio = sorted({x for x in r["rotulo_por_X"] if x in ("LE_EM_PARTE", "SEM_PODER")})
        L.append("| %d | %s | %s | %s | %s | %s | %s | %s | %s |" % (r["G"], ("%.2f" % r["p0"]).replace(".", ","), ("%.2f" % r["p1"]).replace(".", ","), r["nivel"],
                 "—" if r["cA"] is None else r["cA"], "—" if r["cB"] is None else r["cB"], ", ".join(meio) or "não há", f(r["alfa"]), f(r["beta"])))
    L += ["", "## O que sai, conforme a taxa verdadeira de grupos certos (13 grupos; p0 = 0,25; p1 = 0,90; erro de 1 em 1.000)", ""]
    alvo = next(r for r in regras if r["G"] == 13 and r["p0"] == 0.25 and r["p1"] == 0.90 and r["nivel"] == "1 em 1.000")
    L += ["| taxa verdadeira | SEGUE | LÊ EM PARTE | SEM PODER | NÃO SEGUE |", "|---|---|---|---|---|"]
    for t in ("0.0", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1.0"):
        d = alvo["P_rotulo_por_taxa"][t]
        L.append("| %s | %s | %s | %s | %s |" % (t.replace(".", ","), f(d.get("SEGUE", 0.0)), f(d.get("LE_EM_PARTE", 0.0)), f(d.get("SEM_PODER", 0.0)), f(d.get("NAO_SEGUE", 0.0))))
    L += ["", "## Do acerto por resposta ao grupo certo (o par pede as duas respostas certas; pares independentes por hipótese)", "",
          "| tocadas por grupo | pares errados tolerados | resposta 0,99 | 0,95 | 0,90 | 0,85 | 0,80 | 0,70 | quem acerta um par em quatro | quem acerta um par em dois |", "|---|---|---|---|---|---|---|---|---|---|"]
    for c in conv:
        p = c["por_acerto_de_resposta"]
        L.append("| %d | %d | %s | %s | %s | %s | %s | %s | %s | %s |" % (c["tocadas"], c["tolerancia"], f(p["0.99"]), f(p["0.95"]), f(p["0.90"]), f(p["0.85"]), f(p["0.80"]), f(p["0.70"]),
                                                                    f(c["moeda_um_em_quatro_por_par"]), f(c["meio_a_meio_por_par"])))
    L += ["", "## O portão “sabe fazer a tarefa”, com limiar próprio (os 89 itens que os quatro textos-base dizem)", "",
          "| p1 | erro pedido | passa com | um bom leitor (em p1) passa | quem está em 0,67 passa | quem está em 0,50 passa |", "|---|---|---|---|---|---|"]
    for g in portoes:
        L.append("| %s | %s | %s ou mais de %d | %s | %s | %s |" % (("%.2f" % g["p1"]).replace(".", ","), g["nivel"], g["passa_com"], g["itens"], f(g["bom_leitor_passa"]),
                                                               f(g["quem_esta_em_0_67_passa"]), f(g["quem_esta_em_0_50_passa"])))
    (SAIDA / "RESULTADO_PODER_R5.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
