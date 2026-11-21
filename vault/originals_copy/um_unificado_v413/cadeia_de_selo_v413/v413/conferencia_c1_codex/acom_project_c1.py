# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: ACOM project (so' leitura) da referencia EXATA da sessao c1. Imprime revisao, fase e
proxima acao, procurando as chaves em qualquer profundidade do recibo."""
import json, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8")
REF = r"C:\IALD\Central de Patentes\work\cinco_sigma_fora_da_cosmologia_27out\SESSION_REFERENCE_c1_27e28out.json"
req = json.dumps({"operation": "project", "reference": REF}, ensure_ascii=False).encode("utf-8")
out = subprocess.run([r"C:\Python314\python.exe", "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"], input=req,
                     capture_output=True)
txt = out.stdout.decode("utf-8", "replace")
try:
    d = json.loads(txt)
except json.JSONDecodeError:
    print("FALHA de leitura:", txt[:800], out.stderr.decode("utf-8", "replace")[:800])
    sys.exit(1)


def acha(x, k):
    if isinstance(x, dict):
        for a, b in x.items():
            if a == k:
                return b
            v = acha(b, k)
            if v is not None:
                return v
    elif isinstance(x, list):
        for b in x:
            v = acha(b, k)
            if v is not None:
                return v
    return None


print("ok:", d.get("ok"), "| erro:", d.get("error"), str(d.get("message", ""))[:200])
print("revision:", acha(d, "revision"))
for k in ("phase", "fase", "next_action", "proxima_acao"):
    v = acha(d, k)
    if v is not None:
        print(k + ":", str(v)[:600])
