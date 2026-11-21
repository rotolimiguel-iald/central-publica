# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: le do RESULTADO.json da leitura do Codex das pedras limpas (CODEX_PEDRAS_LIMPAS_R1) os
vereditos com ressalva e as substituicoes propostas por modulo, e imprime de forma compacta. So' le."""
import json, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
R = Path(__file__).resolve().parents[1] / "revisao_codex" / "CODEX_PEDRAS_LIMPAS_R1" / "RESULTADO.json"
d = json.loads(R.read_text(encoding="utf-8"))
print("chaves:", ", ".join(d.keys()))


def mostra(o, prof=0):
    if prof > 6:
        return
    if isinstance(o, dict):
        mod = o.get("module") or o.get("modulo")
        ver = o.get("verdict") or o.get("veredito")
        if mod and ver and "RESSALVA" in str(ver):
            print("=" * 100)
            print(json.dumps(o, ensure_ascii=False, indent=1)[:6000])
            return
        for v in o.values():
            mostra(v, prof + 1)
    elif isinstance(o, list):
        for v in o:
            mostra(v, prof + 1)


mostra(d)
for k in ("metadata", "metadado", "manifest_note", "findings"):
    if k in d:
        print("== %s" % k)
        print(json.dumps(d[k], ensure_ascii=False, indent=1)[:3000])
