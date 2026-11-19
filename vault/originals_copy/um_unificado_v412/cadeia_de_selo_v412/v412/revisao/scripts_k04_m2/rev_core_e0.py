import json
core=json.load(open(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json",encoding="utf-8"))
c=core["core"]
ks=[k for k in c if "e0" in k.lower() or "scale_open" in k.lower() or "neutrino" in k.lower()]
print(ks)
for k in ks:
    v=c[k]
    if isinstance(v,dict):
        print("##",k, "verdict:", str(v.get("verdict"))[:300])
        for kk in ("theorem","estatuto","diz","nao_diz"):
            if kk in v: print("   ",kk,":",str(v[kk])[:600])
