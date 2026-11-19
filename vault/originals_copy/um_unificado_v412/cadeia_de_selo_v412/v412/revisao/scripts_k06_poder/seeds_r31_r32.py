# -*- coding: utf-8 -*-
import json
from pathlib import Path
P = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K06\PODER")
a = json.loads((P / "resultados_r31.json").read_text(encoding="utf-8"))
b = json.loads((P / "resultados_r32.json").read_text(encoding="utf-8"))
sa = {s["id"].replace("_R31", ""): s["seed"] for s in a["scenarios"]}
sb = {s["id"].replace("_R32", ""): s["seed"] for s in b["scenarios"]}
print("cenarios r31:", len(sa), "r32:", len(sb))
diff = [(k, sa.get(k), sb.get(k)) for k in sorted(set(sa) | set(sb)) if sa.get(k) != sb.get(k)]
print("sementes diferentes:", diff)
print("master seeds:", a["master_seed"], b["master_seed"])
