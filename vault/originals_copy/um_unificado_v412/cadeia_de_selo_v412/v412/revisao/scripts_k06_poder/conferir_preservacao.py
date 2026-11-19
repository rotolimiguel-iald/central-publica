# -*- coding: utf-8 -*-
"""Revisao K06: confere as listas PRESERVACAO_SHA256.txt de REV0 e REV1 (caminhos relativos a pasta kimi)."""
import hashlib
import re
from pathlib import Path

ROOT = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi")
for rev in ("REV0", "REV1"):
    f = ROOT / "K06" / "PODER" / rev / "PRESERVACAO_SHA256.txt"
    ok = bad = miss = 0
    for line in f.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^([0-9a-f]{64})\s+\*?(.+)$", line.strip())
        if not m:
            continue
        h, name = m.groups()
        cand = ROOT / name
        if not cand.is_file():
            miss += 1
            print(rev, "ausente:", name)
            continue
        if hashlib.sha256(cand.read_bytes()).hexdigest() == h:
            ok += 1
        else:
            bad += 1
            print(rev, "hash difere:", name)
    print(rev, "ok", ok, "difere", bad, "ausente", miss)
