# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: so' leitura. Conta, nas fontes novas de pedras_novas\\, quantos modulos abrem cada espaco de nome (pela
primeira parte do nome), no conjunto inteiro e no conjunto sem as pastas passadas em --sem (para medir um estado anterior)."""
import json, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent; N = V / "pedras_novas"
sem = sys.argv[sys.argv.index("--sem") + 1].split(";") if "--sem" in sys.argv else []
orig = json.loads((N / "ORIGENS.json").read_text(encoding="utf-8"))["itens"]
for rot, itens in (("todos", orig), ("sem " + ", ".join(sem), [o for o in orig if o["pasta_de_origem"] not in sem])):
    c = {}
    for o in itens:
        t = (N / (o["modulo"] + ".lean")).read_text(encoding="utf-8")
        for r in {n.split(".")[0] for n in re.findall(r"^namespace\s+(\S+)", t, flags=re.M)}:
            c[r] = c.get(r, 0) + 1
    print(rot, "|", len(itens), "modulos |", dict(sorted(c.items(), key=lambda kv: -kv[1])))
