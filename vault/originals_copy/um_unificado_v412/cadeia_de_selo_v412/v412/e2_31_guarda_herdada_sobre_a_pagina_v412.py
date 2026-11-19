"""Etapa 2, bloco 4 (exame): roda a guarda herdada da v411 (a funcao do proprio um.py selado, por trecho) sobre a pagina R9 PT e EN, por unidade (pagina inteira, cada bloco separado por linha em branco) e mostra as violacoes."""
import sys, json
from pathlib import Path
sys.path.insert(0, r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
from e2_lib_v412 import D
import base_um_v411 as B

NS = B.carregar(["_v392_guarda_texto", "_v411_guarda_frases"])
B.chamar_resolvendo(NS, "_v411_guarda_frases", "aquecimento")
g = NS["_v411_guarda_frases"]
for nome, arq in (("PT", D / "o_que_fica_claro_REV9" / "O_QUE_FICA_CLARO_v412_R9.md"), ("EN", D / "O_QUE_FICA_CLARO_v412_R9_EN.md")):
    t = arq.read_bytes().decode("utf-8")
    v = g(t)
    print("== %s pagina inteira: %d violacoes" % (nome, len(v)))
    for x in v[:12]:
        print("   ", x[0], "|", x[1][:140])
    por_bloco = []
    for i, b in enumerate([b for b in t.split("\n\n") if b.strip()]):
        vb = g(b)
        if vb:
            por_bloco.append((i, [x[0] for x in vb]))
    print("   por bloco:", por_bloco[:20])
