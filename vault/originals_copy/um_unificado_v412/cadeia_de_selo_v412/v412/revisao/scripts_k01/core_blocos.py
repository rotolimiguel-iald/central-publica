import json, io, sys
p = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json"
d = json.load(io.open(p, encoding="utf-8"))
print("top keys:", len(d), list(d.keys())[:30])
core = d.get("core", d)
print("core keys:", len(core))
for k in core:
    kl = k.lower()
    if any(s in kl for s in ("neutrino","m2","h0dn","ringdown","relogio","clock","neff","coma","th229","sigma")):
        print(k, type(core[k]).__name__)
