# -*- coding: utf-8 -*-
import json
from pathlib import Path
RES = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K06\PODER\resultados_r32.json")
d = json.loads(RES.read_text(encoding="utf-8"))
for sid in ("BASE_INDEPENDENTE_R32", "ICC_015_TEXTO_010", "CONTROLE_070", "CINCO_SIGMA_N655", "NULO_ESPECIFICO_090_N655"):
    s = next(z for z in d["scenarios"] if z["id"] == sid)
    print("==", sid)
    for k, v in s["rates"].items():
        print("   ", k, v)
    print("    means:", s["observed_synthetic_means"])
