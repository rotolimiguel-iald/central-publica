# -*- coding: utf-8 -*-
"""Etapa 2 da v413: confere, por sha256 lido dos bytes, os pinos do contrato R2 (congelado) que a gerencia passou: o contrato R2 (94982ebbc29d81b8, com a copia em contrato_REV2\\) e a pagina R1 (3dc953e37c6739f4),
mais os quatro insumos que o R2 herda do R1 (manifesto, ancoras, inventario e o fecho da Etapa 1). Sai com 2 se algum nao bate (PARAR). Grava CONFERENCIA_ENTRADA_R2_ETAPA2_v413.json."""
import hashlib, json, os, sys
from datetime import datetime
BASE = os.path.dirname(os.path.abspath(__file__))
ESPERADOS = [("CONTRATO_v413_R2.md", "94982ebbc29d81b8"), (os.path.join("contrato_REV2", "CONTRATO_v413_R2.md"), "94982ebbc29d81b8"),
             (os.path.join("o_que_fica_claro_v413", "O_QUE_FICA_CLARO_v413_R1.md"), "3dc953e37c6739f4"), ("PRONTO_PARA_CANDIDATO_v413.json", "ea57114bfd524579"),
             (os.path.join("insumos", "MANIFESTO_PEDRAS_v413.json"), "08c5ef6bbfb74384"), (os.path.join("insumos", "ANCORAS_PROPOSTAS_v413.json"), "aaee9804be6bff61"), ("INVENTARIO_CADEIA_v413.json", "39deb7ec0a85ec68")]
linhas, ok = [], True
for rel, esp in ESPERADOS:
    p = os.path.join(BASE, rel)
    s = hashlib.sha256(open(p, "rb").read()).hexdigest() if os.path.isfile(p) else None
    linhas.append({"arquivo": rel, "esperado_sha16": esp, "medido_sha16": s[:16] if s else None, "ok": bool(s and s[:16] == esp)})
    ok = ok and linhas[-1]["ok"]
out = {"o_que_e": "conferencia de entrada do contrato R2 da v413", "quando": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "linhas": linhas, "ok": ok}
dst = os.path.join(BASE, "CONFERENCIA_ENTRADA_R2_ETAPA2_v413.json"); tmp = dst + ".tmp"
b = json.dumps(out, ensure_ascii=False, indent=2).encode("utf-8"); open(tmp, "wb").write(b); assert os.path.getsize(tmp) == len(b); os.replace(tmp, dst)
for x in linhas:
    print(("OK   " if x["ok"] else "FALHA ") + x["arquivo"], x["medido_sha16"])
print("RESULTADO:", "OK" if ok else "PARAR")
sys.exit(0 if ok else 2)
