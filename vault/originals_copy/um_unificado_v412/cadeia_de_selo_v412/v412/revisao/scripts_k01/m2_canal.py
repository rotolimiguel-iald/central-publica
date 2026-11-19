import json, io, sys
p = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\CANAIS_K01.json"
d = json.load(io.open(p, encoding="utf-8"))
for c in d["canais"]:
    if c["id"] == sys.argv[1]:
        print(json.dumps(c, ensure_ascii=False, indent=1))
