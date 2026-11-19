# -*- coding: utf-8 -*-
import json
from pathlib import Path
orig = json.loads(Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K06\PODER\resultados_r32.json").read_text(encoding="utf-8"))
mine = json.loads(Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\revisao\scripts_k06_poder\copia_motor\saida_base_rev.json").read_text(encoding="utf-8"))
a = next(s for s in orig["scenarios"] if s["id"] == "BASE_INDEPENDENTE_R32")
b = next(s for s in mine["scenarios"] if s["id"] == "BASE_INDEPENDENTE_R32")
print("linha identica ao resultados_r32.json:", json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True))
print("seed", a["seed"], b["seed"], "powered", a["rates"]["powered"], b["rates"]["powered"])
