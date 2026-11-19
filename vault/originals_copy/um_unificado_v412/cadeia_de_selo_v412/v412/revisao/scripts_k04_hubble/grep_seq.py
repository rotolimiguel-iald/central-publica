import json, sys
from pathlib import Path
here = Path(__file__).resolve().parent
rid = sys.argv[1]; want = set(int(x) for x in sys.argv[2:])
j = json.loads((here / "ver" / (rid + ".json")).read_text(encoding="utf-8"))
regs = list(j.get("registros", [])) + [h for h in (j.get("rota", {}).get("historico") or []) if isinstance(h, dict)] + [h for h in (j.get("historico") or []) if isinstance(h, dict)]
seen = set()
for r in regs:
    s = r.get("seq")
    if s in want and s not in seen:
        seen.add(s)
        print("seq", s, "|", {k: (str(v)[:900]) for k, v in r.items() if k not in ("seq",) and v})
