# Revisor K05/tau: explora a estrutura do clock_test_result_v369 no core selado (SO LEITURA).
import json, hashlib, sys
from pathlib import Path
CORE = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json")
raw = CORE.read_bytes()
print("sha256", hashlib.sha256(raw).hexdigest(), "bytes", len(raw))
doc = json.loads(raw.decode("utf-8"))
found = []
def walk(v, p=()):
    if isinstance(v, dict):
        for k, c in v.items():
            if k in ("clock_test_result_v369", "clock_test_protocol_v369"):
                found.append((p + (k,), c))
            walk(c, p + (k,))
    elif isinstance(v, list):
        for i, c in enumerate(v):
            walk(c, p + (str(i),))
walk(doc)
for p, c in found:
    print("PATH", p, type(c).__name__, (list(c.keys()) if isinstance(c, dict) else None))
res = [c for p, c in found if p[-1] == "clock_test_result_v369"]
for i, r in enumerate(res):
    print("--- result", i, "keys", list(r.keys()))
r = max(res, key=lambda x: len(json.dumps(x)))
print(json.dumps({k: (v if k != "P1" else "...") for k, v in r.items()}, ensure_ascii=False, indent=1)[:6000])
print(json.dumps(r["P1"], ensure_ascii=False, indent=1)[:9000])
