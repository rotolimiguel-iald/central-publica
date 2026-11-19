# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: exame da PROPOSTA da pagina R15 com a guarda herdada da v411 (a funcao do um.py selado), unidade a unidade
(titulo, paragrafo, item, celula de tabela). Compara com a R14: lista as unidades da R15 que NAO estao na R14 e as violacoes de cada
uma. So' leitura. Nao e' a travessia da v412 (essa e' do construtor); serve para a gerencia nao levar a ele texto que a regra herdada
ja' recusa. Uso: guarda_herdada_sobre_r15.py <arquivo R15>"""
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
sys.path.insert(0, str(V))
import base_um_v411 as B

NS = B.carregar(["_v392_guarda_texto", "_v411_guarda_frases"])
B.chamar_resolvendo(NS, "_v411_guarda_frases", "aquecimento")
g = NS["_v411_guarda_frases"]


def unidades(t):
    out = []
    for bloco in [b for b in t.split("\n\n") if b.strip()]:
        linhas = bloco.split("\n")
        if all(l.lstrip().startswith("|") for l in linhas):
            for l in linhas:
                for c in l.strip().strip("|").split("|"):
                    if c.strip() and not set(c.strip()) <= set("-"):
                        out.append(c.strip())
        elif all(l.lstrip().startswith("- ") or l.lstrip()[:2].rstrip(".").isdigit() for l in linhas):
            out.extend(l.strip() for l in linhas)
        else:
            out.append(bloco.strip())
    return out


r14 = (V / "o_que_fica_claro_REV14" / "O_QUE_FICA_CLARO_v412_R14.md").read_bytes().decode("utf-8")
r15 = Path(sys.argv[1]).read_bytes().decode("utf-8")
u14 = set(unidades(r14)); novas = [u for u in unidades(r15) if u not in u14]
print("unidades na R14:", len(unidades(r14)), "| na R15:", len(unidades(r15)), "| novas ou mudadas:", len(novas))
assert novas, "zero unidades novas examinadas"
com = 0
for u in novas:
    v = g(u)
    if v:
        com += 1
        print("VIOLA:", sorted({x[0] for x in v}), "|", u[:110].replace("\n", " "))
print("unidades novas com violacao da guarda herdada:", com, "de", len(novas))
ref = [u for u in unidades(r14) if "P = nP" in u]
print("referencia (R14, unidades com P = nP):", [(sorted({x[0] for x in g(u)}), u[:50]) for u in ref])
