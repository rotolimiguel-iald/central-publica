import json, io, sys
p = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json"
d = json.load(io.open(p, encoding="utf-8"))
core = d["core"]
for k in sys.argv[1:]:
    print("=====", k)
    print(json.dumps(core[k], ensure_ascii=False, indent=1)[:12000])
