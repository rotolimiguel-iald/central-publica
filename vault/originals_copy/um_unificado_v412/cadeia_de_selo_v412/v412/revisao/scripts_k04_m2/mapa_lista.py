import json, subprocess, sys
for t in ("neutrino","JUNO","m2","perito"):
    out = subprocess.run([r"C:\Python314\python.exe","-B","-X","utf8",r"C:\IALD\MAPA_DE_ROTAS\rotas.py","consultar",t],capture_output=True,text=True,encoding="utf-8").stdout
    d = json.loads(out)
    print("===",t,d["n"])
    for r in d["rotas"]:
        print(r["rota_id"],"|",r["status"],"|",r["titulo"][:110])
