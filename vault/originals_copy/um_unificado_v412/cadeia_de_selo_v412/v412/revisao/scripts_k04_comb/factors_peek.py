import json, hashlib
base = r"C:\IALD\Central de Patentes\work\astra_bell_fock_tt_05nov\h0dn_bg1_06nov\network"
for n in ("factors.json", "MANIFEST.json", "parameters.json"):
    b = open(base + "\\" + n, "rb").read()
    print("=====", n, len(b), hashlib.sha256(b).hexdigest())
    d = json.loads(b.decode("utf-8"))
    if isinstance(d, dict):
        for k, v in d.items():
            if isinstance(v, (dict, list)):
                print(" ", k, type(v).__name__, len(v), (list(v)[:8] if isinstance(v, dict) else str(v[:2])[:200]))
            else:
                print(" ", k, "=", str(v)[:160])
    else:
        print(type(d), len(d), str(d[:2])[:300])
