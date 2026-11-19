import json, collections, os
base = r"C:\IALD\Central de Patentes\work\astra_bell_fock_tt_05nov\h0dn_bg1_06nov\network"
d = json.loads(open(os.path.join(base, "factors.json"), "rb").read().decode("utf-8"))
c = collections.Counter(x["family"] for x in d)
print(c)
print(sorted(set(k for x in d for k in x.keys())))
