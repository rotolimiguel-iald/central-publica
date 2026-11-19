import json, io, sys
p = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json"
d = json.load(io.open(p, encoding="utf-8"))
b = d["core"]["h0dn_bg1_v411"]
print([k for k in b.keys()])
v = b.get("values", {})
for k, x in v.items():
    s = json.dumps(x, ensure_ascii=False)
    print(k, "=", s[:260])
print("---- ressalvas_secao8")
for r in b.get("ressalvas_secao8", []):
    print(r if isinstance(r, str) else json.dumps(r, ensure_ascii=False))
