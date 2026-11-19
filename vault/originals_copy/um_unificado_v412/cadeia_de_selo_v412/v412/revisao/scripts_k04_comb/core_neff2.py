import json, math
P = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json"
d = json.loads(open(P, "rb").read().decode("utf-8"))
n = d["core"]["neff_channel"]
for c in n["checks"]:
    print("-", str(c)[:420])
b = n["values"]["beta"]; dn = n["values"]["Delta_Neff"]
print("dN/beta =", repr(dn / b))
# hipotese: dN = (8/7)*(11/4)^(4/3)*... testar candidatos simples
cands = {"(8/7)(11/4)^(4/3)": 8/7*(11/4)**(4/3), "4*(11/4)^(4/3)*(7/8)^-1": 0}
print(cands)
m = d["core"]["neutrino_m2"]
print("neutrino_m2 keys:", list(m.keys()))
v = m.get("values", {})
print("values keys:", list(v.keys())[:40])
for k in ("m2_TGL_meV", "m2_tgl_meV", "m2_pred", "projecao_2031_sigma", "tensao_atual_sigma"):
    if k in v: print(k, "=", v[k])
fz = m.get("frozen", {})
print("frozen keys:", list(fz.keys())[:20])
print("kill_rule:", str(fz.get("kill_rule"))[:300])
