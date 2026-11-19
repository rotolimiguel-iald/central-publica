# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: so' leitura. Mostra ETAPA_2_R5_ESTADO_v412.json do construtor (blocos, quando, nota curta, proximo comando)."""
import json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
p = Path(__file__).resolve().parent / "ETAPA_2_R5_ESTADO_v412.json"
j = json.loads(p.read_bytes())
print("chaves:", list(j))
for k, v in j.items():
    if k == "blocos" and isinstance(v, dict):
        for nome, b in v.items():
            print("==", nome, "|", (b.get("quando") if isinstance(b, dict) else ""), "|", str((b.get("nota") if isinstance(b, dict) else b))[:420])
    else:
        print(k, ":", json.dumps(v, ensure_ascii=False)[:600])
