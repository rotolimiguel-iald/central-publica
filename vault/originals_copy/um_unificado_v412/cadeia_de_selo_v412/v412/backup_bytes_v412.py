# -*- coding: utf-8 -*-
"""backup_bytes_v412.py -- (gerencia c1, 19/11/2026) backup de BYTES de cada arquivo passado na linha de comando, na mesma pasta, como
<nome>.bak_<AAAAMMDD_HHMMSS>_<sufixo>; confere byte a byte. Uso: backup_bytes_v412.py <sufixo> <arquivo> [<arquivo> ...]"""
import hashlib, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
suf, arqs = sys.argv[1], sys.argv[2:]
assert suf and arqs, "uso: backup_bytes_v412.py <sufixo> <arquivo> [...]"
ts = time.strftime("%Y%m%d_%H%M%S")
for a in arqs:
    p = Path(a)
    b = p.read_bytes()
    bk = p.with_name("%s.bak_%s_%s" % (p.name, ts, suf))
    assert not bk.exists(), bk
    bk.write_bytes(b)
    assert bk.read_bytes() == b
    print("backup", bk, "| sha16", hashlib.sha256(b).hexdigest()[:16], "|", len(b), "B")
