# -*- coding: utf-8 -*-
import json
from pathlib import Path
orig = json.loads(Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K06\PODER\resultados_r32.json").read_text(encoding="utf-8"))
mine = json.loads(Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\revisao\scripts_k06_poder\copia_motor\saida_base_rev.json").read_text(encoding="utf-8"))
a = next(s for s in orig["scenarios"] if s["id"] == "BASE_INDEPENDENTE_R32")
b = next(s for s in mine["scenarios"] if s["id"] == "BASE_INDEPENDENTE_R32")
def walk(x, y, path=""):
    if isinstance(x, dict):
        for k in sorted(set(x) | set(y)):
            if k not in x or k not in y:
                print("so em um lado:", path + "/" + k); continue
            walk(x[k], y[k], path + "/" + k)
    elif isinstance(x, list):
        if len(x) != len(y):
            print("tamanho difere", path); return
        for i, (u, v) in enumerate(zip(x, y)):
            walk(u, v, path + f"[{i}]")
    else:
        if x != y:
            print("DIFERE", path, x, y)
walk(a, b)
print("fim da comparacao; schema orig", orig["schema"], "| meu", mine["schema"])
print("chaves do meu arquivo:", sorted(mine.keys()), "n cenarios", len(mine["scenarios"]))
