import json, io
p = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\CANAIS_K01.json"
d = json.load(io.open(p, encoding="utf-8"))
for i, c in enumerate(d["canais"], 1):
    print(i, c.get("id"), "|", list(c.keys()))
print()
c0 = d["canais"][0]
for k, v in c0.items():
    print("==", k, type(v).__name__, (list(v.keys()) if isinstance(v, dict) else ""))
print()
print(json.dumps(d["fontes_publicas"], ensure_ascii=False, indent=1)[:9000])
