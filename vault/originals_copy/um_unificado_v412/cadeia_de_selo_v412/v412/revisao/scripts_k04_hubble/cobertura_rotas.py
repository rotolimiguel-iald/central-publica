import json
from pathlib import Path
here = Path(__file__).resolve().parent
j = json.loads((here / "consulta_mapa.json").read_text(encoding="utf-8"))
doc = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\HUBBLE_JA_EXAMINADO_K04.md").read_text(encoding="utf-8")
termos = ["D1B","Pantheon","masers","TDCOSMO","lentes","sirenes","H0DN","fase9","Hubble","Cefeidas","SH0ES","TRGB","CCHP","SBF","JAGB","FFAT","R-E","R-G","intermedi","Fase 4","Fase 5","razao de Hubble","K = E"]
uni = {}
for t in termos:
    for r in j[t].get("rotas", []):
        uni.setdefault(r["rota_id"], {"status": r["status"], "n": r["n_registros"], "titulo": r["titulo"], "termos": []})["termos"].append(t)
rel = [k for k in uni if k.startswith(("d1.", "hubble.", "discriminante.", "estatistica.h0dn", "natureza.", "bancada.preregistro", "supernovas.", "um_py.v378", "um_py.v380", "umpy.v411", "kernel.k_", "conceitual.k_"))]
print("rotas relevantes por prefixo:", len(rel))
faltam = []
for k in sorted(rel):
    # a rota esta citada no doc?
    citada = k in doc
    if not citada:
        faltam.append(k)
        print("NAO CITADA:", k, "|", uni[k]["status"], "| nreg", uni[k]["n"], "| termos:", ",".join(uni[k]["termos"][:6]), "|", uni[k]["titulo"][:90])
print("total nao citadas:", len(faltam))
