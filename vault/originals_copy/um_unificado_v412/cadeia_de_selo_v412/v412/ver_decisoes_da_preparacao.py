# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: so' leitura. Mostra de PREPARACAO_v412_PRONTA.json as chaves e, por extenso, decisoes_e_pontos_para_a_gerencia."""
import json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
j = json.loads((Path(__file__).resolve().parent / "PREPARACAO_v412_PRONTA.json").read_bytes())
print("chaves:", list(j))
d = j.get("decisoes_e_pontos_para_a_gerencia")
for i, x in enumerate(d if isinstance(d, list) else (list(d.items()) if isinstance(d, dict) else [d]), 1):
    print("%d." % i, json.dumps(x, ensure_ascii=False)[:1600])
for k in ("o_que_nao_foi_feito", "nao_feito", "falta"):
    if k in j:
        print(k, ":", json.dumps(j[k], ensure_ascii=False)[:2500])
