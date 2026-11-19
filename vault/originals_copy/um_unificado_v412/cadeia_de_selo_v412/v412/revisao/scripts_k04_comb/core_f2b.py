import json
P = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json"
d = json.loads(open(P, "rb").read().decode("utf-8"))
f = d["core"]["f2b_errata_v404"]
print(json.dumps(f, ensure_ascii=False, indent=1)[:7000])
