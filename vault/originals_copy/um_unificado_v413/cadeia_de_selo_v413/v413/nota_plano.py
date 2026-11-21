# -*- coding: utf-8 -*-
"""gerencia c1, 21/11/2026: acrescenta uma nota datada no fim do PLANO_DA_NOITE_v413_20nov.md (registro AO LADO; nada e' apagado).
Uso: nota_plano.py "<texto>". Backup de bytes; escrita por temporario; confere que o arquivo cresceu."""
import sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
P = Path(__file__).resolve().parent / "PLANO_DA_NOITE_v413_20nov.md"
texto = sys.argv[1]
assert len(texto) >= 10
b = P.read_bytes()
t = b.decode("utf-8").rstrip("\n") + "\n- %s (%s)\n" % (texto, time.strftime("%d/%m %H:%M"))
nb = t.encode("utf-8")
assert len(nb) > len(b)
(P.with_name(P.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S"))).write_bytes(b)
tmp = P.with_name(P.name + ".tmp")
tmp.write_bytes(nb)
assert tmp.read_bytes() == nb
tmp.replace(P)
print("nota acrescentada (%d -> %d B)" % (len(b), len(nb)))
