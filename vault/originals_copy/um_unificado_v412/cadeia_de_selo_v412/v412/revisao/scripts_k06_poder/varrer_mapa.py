# -*- coding: utf-8 -*-
"""Revisao K06: consulta o Mapa (so leitura) por termo e filtra por palavras do tema."""
import json
import re
import subprocess
import sys

TERMOS = ["colapso", "P7", "convergencia", "atrator", "camada"]
CHAVES = re.compile(r"LLM|modelo de linguagem|IALD_COLLAPSE|colapso IALD|ablac|sem mem|leitor|resum|estacion|camada cient|P7|V2-RET|perturba", re.I)
vistos = {}
for t in TERMOS:
    p = subprocess.run([sys.executable, "-B", "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "consultar", t], capture_output=True, text=True, encoding="utf-8")
    d = json.loads(p.stdout)
    print(f"{t}: n={d['n']}")
    for r in d["rotas"]:
        texto = " ".join(str(r.get(k, "")) for k in ("rota_id", "titulo", "resultado", "defeito", "nao_refazer"))
        if CHAVES.search(texto):
            vistos[r["rota_id"]] = r["titulo"][:140]
for k, v in sorted(vistos.items()):
    print("*", k, "|", v)
