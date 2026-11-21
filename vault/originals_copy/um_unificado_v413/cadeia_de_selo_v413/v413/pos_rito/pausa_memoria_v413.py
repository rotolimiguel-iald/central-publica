# -*- coding: utf-8 -*-
"""pausa_memoria_v413.py criar|remover -- gerencia c1, 21/11/2026: o marcador fila\\PAUSA_VIGIA.json que o pos-rito cria ANTES de escrever o
MEMORY.md e remove DEPOIS de `memoria.py pinar` (memoria.py: enquanto ativo, o vigiar --enforcar so' relata; teto de 4 h a contar da criacao).
Recusa criar por cima de uma pausa de outro dono; so' remove a pausa desta gerencia."""
import datetime, json, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
P = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\fila\PAUSA_VIGIA.json")
QUEM = "claude-c1 pos-rito v413"
op = sys.argv[1]
if op == "criar":
    if P.exists():
        d = json.loads(P.read_text(encoding="utf-8"))
        assert d.get("quem") == QUEM, ("ja existe uma pausa de outro dono: nao sobrescrevo", d.get("quem"))
    ate = (datetime.datetime.now().astimezone() + datetime.timedelta(hours=1)).isoformat(timespec="seconds")
    b = json.dumps({"quem": QUEM, "ate": ate, "motivo": "a linha do HANDOFF v413 no MEMORY.md (e quatro linhas movidas verbatim ao MEMORY_2.md); pinar logo depois"}, ensure_ascii=False, indent=1).encode("utf-8")
    tmp = P.with_name(P.name + ".tmp"); tmp.write_bytes(b); assert tmp.read_bytes() == b; tmp.replace(P)
    print("pausa criada ate", ate)
elif op == "remover":
    if not P.exists():
        print("sem pausa")
    else:
        d = json.loads(P.read_text(encoding="utf-8"))
        assert d.get("quem") == QUEM, ("a pausa e' de outro dono: nao removo", d.get("quem"))
        P.unlink()
        print("pausa removida")
else:
    raise SystemExit("uso: pausa_memoria_v413.py criar|remover")
