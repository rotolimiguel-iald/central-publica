import json
P = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json"
d = json.loads(open(P, "rb").read().decode("utf-8"))
n = d["core"]["neff_channel"]
print("theorem:", str(n["theorem"])[:1500])
print("frozen_ref:", json.dumps(n["frozen_ref"], ensure_ascii=False)[:800])
print("values:", json.dumps(n["values"], ensure_ascii=False, indent=1)[:3500])
print("verdict:", n["verdict"])
