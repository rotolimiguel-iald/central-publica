import json, sys
P = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json"
raw = open(P, "rb").read()
import hashlib
print("sha256", hashlib.sha256(raw).hexdigest())
d = json.loads(raw.decode("utf-8"))
print(type(d), len(d))
def find(o, key, path=""):
    out = []
    if isinstance(o, dict):
        for k, v in o.items():
            p = path + "/" + str(k)
            if k == key:
                out.append(p)
            out += find(v, key, p)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            out += find(v, key, path + "[" + str(i) + "]")
    return out
for k in ["ressalvas_secao8", "neff_channel", "neutrino_m2", "h0dn_bg1_v411", "f2b_errata_v404", "rotulos_das_sete_ressalvas"]:
    print(k, find(d, k)[:10])
