import json, sys
P = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json"
core = json.load(open(P, encoding="utf-8"))
print("top keys sample:", list(core.keys())[:5], len(core))
def find(d, key, path=""):
    out = []
    if isinstance(d, dict):
        for k, v in d.items():
            if k == key:
                out.append((path + "/" + k, v))
            out += find(v, key, path + "/" + k)
    elif isinstance(d, list):
        for i, v in enumerate(d):
            out += find(v, key, path + "[%d]" % i)
    return out
for key in ("neutrino_m2", "neutrino_m2_perito_v392"):
    r = find(core, key)
    print("###", key, [p for p, _ in r])
    for p, v in r[:1]:
        print(json.dumps(v, ensure_ascii=False, indent=1)[:20000])
