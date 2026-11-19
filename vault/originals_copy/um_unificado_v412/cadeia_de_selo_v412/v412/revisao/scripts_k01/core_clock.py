import json, io
p = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json"
d = json.load(io.open(p, encoding="utf-8"))
r = d["core"]["clock_test_result_v369"]
print(list(r.keys()))
P1 = r.get("P1", {})
print(list(P1.keys()) if isinstance(P1, dict) else type(P1))
for pl in P1.get("platforms", []):
    print(json.dumps(pl, ensure_ascii=False)[:700])
for k in r:
    if "deficit" in k or "today" in k or "5sigma" in k:
        print(k, "=", json.dumps(r[k], ensure_ascii=False)[:300])
