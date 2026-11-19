import json, io, hashlib, os
R = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi"
v = json.load(io.open(os.path.join(R, "VALIDACAO_K01.json"), encoding="utf-8"))
bad = 0
for f in v["arquivos"]:
    p = os.path.join(R, f["arquivo"])
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    ok = h == f["sha256"] and os.path.getsize(p) == f["bytes"]
    bad += (not ok)
    print(("OK  " if ok else "DIVERGE "), f["arquivo"], f["bytes"], os.path.getsize(p))
print("divergentes:", bad)
