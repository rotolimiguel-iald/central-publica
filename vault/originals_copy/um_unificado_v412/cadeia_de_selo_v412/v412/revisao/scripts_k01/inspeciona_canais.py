import json, io
p = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\CANAIS_K01.json"
d = json.load(io.open(p, encoding="utf-8"))
print(type(d), list(d.keys()) if isinstance(d, dict) else len(d))
for k, v in d.items():
    if isinstance(v, (list, dict)):
        print(k, type(v).__name__, len(v))
    else:
        print(k, repr(v)[:200])
