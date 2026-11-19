import json, sys
sys.stdout.reconfigure(encoding="utf-8")
D = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412"
core = json.load(open(D + r"\base_v411\um_absoluto.json", encoding="utf-8"))["core"]
h = core["h0dn_bg1_v411"]
print("chaves do registro:", list(h.keys()))
v = h["values"]
print("values:", list(v.keys()))
for k in ("ressalvas_secao8", "o_que_o_teste_nao_decide"):
    x = h.get(k) if k in h else v.get(k)
    print(k, type(x).__name__, len(x) if x is not None else None)
    if isinstance(x, list):
        for it in x:
            print("   -", str(it)[:260])
print("verdict:", h["verdict"][:300])
print("outcome:", str(h.get("outcome"))[:300])
print("estatuto:", str(h.get("estatuto"))[:200])
