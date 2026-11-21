# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: marca um passo do PLANO_DA_NOITE_v413_20nov.md (ao lado, com hora) e acrescenta uma nota no fim.
Uso: marcar_plano.py <numero do passo> "<nota curta>" [--nota-final "<texto>"]. Backup de bytes; troca atomica."""
import re, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
P = Path(__file__).resolve().parent / "PLANO_DA_NOITE_v413_20nov.md"
n, nota = sys.argv[1], sys.argv[2]
extra = sys.argv[sys.argv.index("--nota-final") + 1] if "--nota-final" in sys.argv else None
t = P.read_bytes().decode("utf-8")
m = re.search(r"^%s\. \[ \] " % re.escape(n), t, re.M)
assert m, "passo %s nao esta' aberto" % n
t = t[:m.start()] + "%s. [x] (%s; %s) " % (n, time.strftime("%H:%M"), nota) + t[m.end():]
if extra:
    t = t.rstrip("\n") + "\n- %s (%s)\n" % (extra, time.strftime("%d/%m %H:%M"))
bk = P.with_name(P.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S"))
bk.write_bytes(P.read_bytes())
tmp = P.with_name(P.name + ".tmp")
tmp.write_bytes(t.encode("utf-8"))
tmp.replace(P)
print("passo %s marcado" % n)
