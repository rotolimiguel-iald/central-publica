import json
P = r"C:\IALD\Central de Patentes\work\conjunto_D_20261029\parametrizacao_03nov\PODER_RAMO_B_ANTES_DE_ABRIR.json"
d = json.loads(open(P, "rb").read().decode("utf-8"))
print("AVISO:", d["aviso"])
print("LEITURA:", d["leitura"])
print([k for k in d.keys()])
for k in d:
    if "D14" in k or "D10" in k:
        v = d[k]
        print("==", k, ":", (json.dumps(v)[:300] if isinstance(v,(dict,list)) else v))
