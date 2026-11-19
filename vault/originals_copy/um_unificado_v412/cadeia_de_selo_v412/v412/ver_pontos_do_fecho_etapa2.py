# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: so' leitura. Mostra, de ETAPA_2_ESTADO_v412.json, os blocos e, por extenso, os pontos que o construtor
deixou para a gerencia decidir no fecho da Etapa 2."""
import json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
j = json.loads((Path(__file__).resolve().parent / "ETAPA_2_ESTADO_v412.json").read_bytes())
print("chaves:", list(j)); print("proximo_comando:", j.get("proximo_comando"))
for nome, b in j.get("blocos", {}).items():
    print("==", nome, "|", b.get("quando"), "| ok:", b.get("ok")); print("   nota:", (b.get("nota") or "")[:600])
    for k, v in (b.get("extra") or {}).items():
        print("   extra.%s:" % k)
        for x in (v if isinstance(v, list) else [v]):
            print("      -", str(x)[:900])
