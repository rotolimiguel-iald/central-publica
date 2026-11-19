import json, io, sys
p = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json"
d = json.load(io.open(p, encoding="utf-8"))
core = d["core"]
b = core["h0dn_bg1_v411"]
def short(o, n=300):
    s = json.dumps(o, ensure_ascii=False)
    return s[:n]
print(list(b.keys()))
v = b.get("values", {})
print(list(v.keys()))
for k in ("K","E_zstar","beta","z_star","lei_em_km_s_Mpc","BG1","bg1","H0DN","h0dn"):
    if k in v: print(k, short(v[k], 500))
