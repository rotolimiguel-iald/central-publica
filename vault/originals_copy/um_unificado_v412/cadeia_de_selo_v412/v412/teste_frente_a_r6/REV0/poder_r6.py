# -*- coding: utf-8 -*-
"""Gerencia c1, 16/11/2026. Teste da frente A, desenho R6: a regra de decisao e o poder. Binomial exata.
NENHUM modelo; nenhum dado. A regra e' a do R5 (revisao R1), com a unidade nova: o GRUPO 2 x 2.

GRUPO: um assento (no indice) em dois estados e uma pagina (levada ao leitor) em dois estados, que diferem numa
afirmacao so'. Quatro apresentacoes, cada uma numa sessao sem historico. GRUPO CERTO: os quatro vereditos certos e, nas
duas que nao batem, a entrada apontada e' a certa, com a linha da pagina que a sustenta.

A REGRA, com G grupos e X grupos certos:
  cA = menor c com P(X >= c | taxa p0) <= a      (acima disso rejeita-se 'nao julga pelo par')
  cB = maior c com P(X <= c | taxa p1) <= a      (abaixo disso rejeita-se 'julga pelo par')
  JULGA_PELO_PAR se X >= cA e X > cB;  NAO_JULGA_PELO_PAR se X <= cB e X < cA;
  JULGA_EM_PARTE se cA <= X <= cB;     SEM_PODER se cB < X < cA.
p0 = a taxa de grupos certos ate' a qual o sistema ainda e' chamado de 'nao julga pelo par';
p1 = a taxa minima exigida de quem julga pelo par.

HIPOTESE DITA: grupos independentes com a mesma taxa. NAO esta' medida (nenhum modelo rodou). Os erros sao nominais.
Uso: poder_r6.py <pasta de saida>"""
import json, math, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
SAIDA = Path(sys.argv[1])


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
        return "JULGA_PELO_PAR"
    if nao:
        return "NAO_JULGA_PELO_PAR"
    if cA is not None and cB is not None and cA <= X <= cB:
        return "JULGA_EM_PARTE"
    return "SEM_PODER"


def taxa_de_grupo(q_veredito, q_aponta):
    """Leitor que acerta cada veredito com probabilidade q_veredito e, quando diz certo que nao bate, aponta a entrada
    e a linha certas com probabilidade q_aponta. Quatro vereditos e dois apontamentos, independentes por hipotese."""
    return (q_veredito ** 4) * (q_aponta ** 2)


def main():
    niveis = [("1 em 100", 1e-2), ("1 em 1.000", 1e-3)]
    taxas = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    regras = []
    for G in (6, 8, 12, 16, 24):
        for p0, p1 in ((0.0625, 0.80), (0.0625, 0.70), (0.25, 0.80), (0.25, 0.70), (0.50, 0.80)):
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
    conv = []
    for qv in (0.99, 0.97, 0.95, 0.90, 0.85, 0.80, 0.70, 0.50):
        conv.append({"acerto_por_veredito": qv, "taxa_de_grupo_com_apontamento_igual": taxa_de_grupo(qv, qv),
                     "taxa_de_grupo_com_apontamento_perfeito": taxa_de_grupo(qv, 1.0)})
    acaso = {"moeda_nos_quatro_vereditos_sem_apontar_certo_(n_entradas=8)": (0.5 ** 4) * ((1 / 8) ** 2),
             "moeda_nos_quatro_vereditos_so_veredito": 0.5 ** 4,
             "quem_so_ve_a_pagina_ou_so_o_assento": 0.0}
    # os controles, com corte proprio
    # (a) o aparelho: o mesmo leitor SEM o indice. Quem so' ve a pagina diz BATE com probabilidade a diante de P0 e b diante
    #     de P1, seja qual for o assento; os quatro vereditos certos tem probabilidade a(1-a)b(1-b) <= 1/16 por grupo.
    aparelho = {str(c): cauda_sup(16, c, 1.0 / 16.0) for c in range(0, 9)}
    # (b) letra igual: 8 paginas (4 intactas, 4 com uma entrada negada nas mesmas palavras); passa com 7 ou 8 certas
    letra = {"moeda": cauda_sup(8, 7, 0.5), "leitor_que_acerta_0_95": cauda_sup(8, 7, 0.95), "leitor_que_acerta_0_90": cauda_sup(8, 7, 0.90),
             "leitor_que_acerta_0_80": cauda_sup(8, 7, 0.80)}
    controles = {"aparelho_sem_indice__P(X>=c)_em_16_grupos_com_taxa_1_em_16": aparelho, "letra_igual__passa_com_7_de_8": letra}
    res = {"gerado_por": "poder_r6.py", "nota": "binomial exata; grupos independentes por hipotese (nao medida); nenhum modelo; nenhum dado",
           "regras": regras, "do_acerto_por_veredito_ao_grupo": conv, "acaso": acaso, "controles": controles}
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "RESULTADO_PODER_R6.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    f = lambda x: "—" if x is None else ("%.2e" % x if x < 0.001 else "%.3f" % x).replace(".", ",")
    L = ["# A regra de decisão e o poder do desenho R6 (binomial exata; nenhum modelo)", "",
         "> Gerado por `poder_r6.py`. Unidade = o grupo 2 × 2 (um assento em dois estados, uma página em dois estados). Grupos independentes por hipótese, não medida.",
         "> `cA` = a partir de quantos grupos certos se diz JULGA PELO PAR; `cB` = até quantos se diz NÃO JULGA PELO PAR. Entre os dois: JULGA EM PARTE (se cA ≤ cB) ou SEM PODER.", "",
         "## Os limiares", "", "| grupos | p0 | p1 | erro pedido | cA (JULGA se ≥) | cB (NÃO JULGA se ≤) | o meio | erro de dizer JULGA a quem está em p0 | erro de dizer NÃO JULGA a quem está em p1 |", "|---|---|---|---|---|---|---|---|---|"]
    for r in regras:
        meio = sorted({x for x in r["rotulo_por_X"] if x in ("JULGA_EM_PARTE", "SEM_PODER")})
        L.append("| %d | %s | %s | %s | %s | %s | %s | %s | %s |" % (r["G"], ("%.4f" % r["p0"]).rstrip("0").replace(".", ","), ("%.2f" % r["p1"]).replace(".", ","), r["nivel"],
                 "—" if r["cA"] is None else r["cA"], "—" if r["cB"] is None else r["cB"], ", ".join(meio) or "não há", f(r["alfa"]), f(r["beta"])))
    for G0, p00, p10, nv in ((16, 0.25, 0.70, "1 em 100"), (16, 0.0625, 0.70, "1 em 100"), (16, 0.25, 0.80, "1 em 1.000"), (8, 0.25, 0.70, "1 em 100")):
        alvo = next(r for r in regras if r["G"] == G0 and r["p0"] == p00 and r["p1"] == p10 and r["nivel"] == nv)
        L += ["", "## O que sai, conforme a taxa verdadeira de grupos certos (%d grupos; p0 = %s; p1 = %s; erro de %s; JULGA se X ≥ %s e X > %s; NÃO JULGA se X ≤ %s e X < %s)" % (
                  G0, ("%.4f" % p00).rstrip("0").replace(".", ","), ("%.2f" % p10).replace(".", ","), nv, alvo["cA"], alvo["cB"], alvo["cB"], alvo["cA"]), "",
              "| taxa verdadeira | JULGA PELO PAR | JULGA EM PARTE | SEM PODER | NÃO JULGA PELO PAR |", "|---|---|---|---|---|"]
        for t in ("0.0", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1.0"):
            d = alvo["P_rotulo_por_taxa"][t]
            L.append("| %s | %s | %s | %s | %s |" % (t.replace(".", ","), f(d.get("JULGA_PELO_PAR", 0.0)), f(d.get("JULGA_EM_PARTE", 0.0)), f(d.get("SEM_PODER", 0.0)), f(d.get("NAO_JULGA_PELO_PAR", 0.0))))
    L += ["", "## Do acerto por veredito ao grupo certo (quatro vereditos e dois apontamentos; independentes por hipótese)", "",
          "| acerto por veredito | grupo certo, apontando com o mesmo acerto | grupo certo, apontando sempre certo |", "|---|---|---|"]
    for c in conv:
        L.append("| %s | %s | %s |" % (("%.2f" % c["acerto_por_veredito"]).replace(".", ","), f(c["taxa_de_grupo_com_apontamento_igual"]), f(c["taxa_de_grupo_com_apontamento_perfeito"])))
    L += ["", "## O acaso", "", "| quem | taxa de grupo certo |", "|---|---|"]
    for k, v in acaso.items():
        L.append("| %s | %s |" % (k.replace("_", " "), f(v)))
    L += ["", "## Os controles, com corte próprio", "",
          "**O aparelho (o mesmo leitor sem o índice; 16 grupos; só os quatro vereditos).** Quem só vê a página acerta os quatro vereditos de um grupo com probabilidade de no máximo 1 em 16.", "",
          "| corte c | probabilidade de X ≥ c sem vazamento (no máximo) |", "|---|---|"]
    for c in ("2", "3", "4", "5", "6"):
        L.append("| %s | %s |" % (c, f(aparelho[c])))
    L += ["", "**Letra igual (8 páginas; passa com 7 ou 8 certas).**", "", "| quem | passa |", "|---|---|"]
    for k, v in letra.items():
        L.append("| %s | %s |" % (k.replace("_", " "), f(v)))
    (SAIDA / "RESULTADO_PODER_R6.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
