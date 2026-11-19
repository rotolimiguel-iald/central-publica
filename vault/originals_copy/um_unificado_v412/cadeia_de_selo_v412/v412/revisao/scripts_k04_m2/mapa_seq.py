import json, subprocess, sys
out = subprocess.run([r"C:\Python314\python.exe","-B","-X","utf8",r"C:\IALD\MAPA_DE_ROTAS\rotas.py","ver","neutrinos.m2.normalizacao"],capture_output=True,text=True,encoding="utf-8").stdout
d = json.loads(out)
for e in d["rota"]["erratas"]:
    if e["seq"] in (93,98,128,142):
        print("--- seq",e["seq"]); print(e["texto"]); print()
