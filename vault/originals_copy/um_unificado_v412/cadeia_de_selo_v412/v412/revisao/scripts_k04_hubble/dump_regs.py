import json, sys
from pathlib import Path
here = Path(__file__).resolve().parent
rid = sys.argv[1]
want = set(int(x) for x in sys.argv[2:]) if len(sys.argv) > 2 else None
j = json.loads((here / "ver" / (rid + ".json")).read_text(encoding="utf-8"))
for r in j.get("registros", []):
    if want is None or int(r.get("seq", -1)) in want:
        print("-" * 80)
        for k in ("seq", "tipo", "titulo", "status", "veredito", "resultado", "defeito", "nao_refazer", "dados", "nota"):
            if r.get(k):
                print(f"[{k}] {str(r[k])[:700]}")
