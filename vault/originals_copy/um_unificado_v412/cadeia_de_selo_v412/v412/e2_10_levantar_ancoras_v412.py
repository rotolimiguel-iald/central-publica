"""Etapa 2, bloco 2 (levantamento): por registro e modulo, quantas declaracoes com estrela e sem estrela; quais nomes a pagina R9 cita entre crases; quais desses nomes existem nos modulos."""
import json, re, sys
from pathlib import Path

sys.path.insert(0, r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
from e2_lib_v412 import D, ler_json

C = ler_json(D / "kernel" / "ANCORAS_PROPOSTAS_CONFERIDAS_v412_R3.json")
P = ler_json(D / "insumos" / "ANCORAS_PROPOSTAS_v412_R5.json")
page = (D / "o_que_fica_claro_REV9" / "O_QUE_FICA_CLARO_v412_R9.md").read_bytes().decode("utf-8")
cit = sorted(set(re.findall(r"`([^`\s]+)`", page)))
print("nomes entre crases na pagina:", len(cit))
por_mod = {}
for reg, itens in C["por_registro"].items():
    for it in itens:
        por_mod.setdefault((reg, it["modulo"]), {"com_estrela": [], "sem_estrela": []})[it["lista"]].append(it)
todos_nomes = {}
for (reg, mod), d in por_mod.items():
    for lst in ("com_estrela", "sem_estrela"):
        for it in d[lst]:
            todos_nomes.setdefault(it["nome_proposto"].split(".")[-1], []).append((mod, it["classe"]))
for (reg, mod), d in sorted(por_mod.items()):
    nomes_mod = {it["nome_proposto"].split(".")[-1] for l in d.values() for it in l}
    citados = sorted(n for n in cit if n in nomes_mod)
    print("%-34s %-30s estrela=%3d sem=%3d citados_pela_pagina=%2d" % (reg[:34], mod, len(d["com_estrela"]), len(d["sem_estrela"]), len(citados)))
print("--- nomes citados na pagina que nao sao nome de declaracao de nenhum modulo:")
for n in cit:
    if n not in todos_nomes:
        print("   ", n)
print("registros:", {r: len(v) for r, v in C["por_registro"].items()})
print("claves de P.registros[r][0]:", list(next(iter(P["registros"].values()))[0].keys()))
