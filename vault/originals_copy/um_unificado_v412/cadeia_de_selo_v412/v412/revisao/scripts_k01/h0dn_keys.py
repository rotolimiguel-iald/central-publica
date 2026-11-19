import json, io, sys
p = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json"
d = json.load(io.open(p, encoding="utf-8"))
b = d["core"]["h0dn_bg1_v411"]
def walk(o, pre="", depth=0):
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, (dict, list)) and depth < 3:
                print(pre + k, type(v).__name__, len(v))
                walk(v, pre + "  ", depth + 1)
            else:
                s = json.dumps(v, ensure_ascii=False)
                print(pre + k, "=", s[:160])
    elif isinstance(o, list):
        for i, v in enumerate(o[:12]):
            if isinstance(v, (dict, list)):
                print(pre + f"[{i}]", type(v).__name__, len(v))
            else:
                print(pre + f"[{i}]", json.dumps(v, ensure_ascii=False)[:160])
walk(b)
