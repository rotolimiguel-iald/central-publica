import hashlib, sys
from pathlib import Path
d = Path(r"C:\IALD\Central de Patentes\work\cunhagens_13out")
alvos = sys.argv[1:]
for p in sorted(d.iterdir()):
    if not p.is_file():
        continue
    raw = p.read_bytes()
    h = hashlib.sha256(raw).hexdigest()
    for a in alvos:
        if h.startswith(a):
            print("HASH", a, "->", p.name, len(raw), "bytes", h)
            print(raw.decode("utf-8", "replace")[:1500])
