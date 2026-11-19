import hashlib, json
from pathlib import Path
BASE = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K04\HUBBLE")
ROOT = BASE.parent.parent
m = json.loads((BASE / "SHA256SUMS_K04_HUBBLE.json").read_text(encoding="utf-8"))
ok = bad = 0
for it in m["arquivos"]:
    p = (ROOT / it["path"][3:]) if it["path"].startswith("../") else (BASE / it["path"])
    if not p.exists():
        print("AUSENTE", it["path"]); bad += 1; continue
    raw = p.read_bytes()
    if len(raw) == it["bytes"] and hashlib.sha256(raw).hexdigest() == it["sha256"]:
        ok += 1
    else:
        print("DIVERGE", it["path"], len(raw), it["bytes"]); bad += 1
print("entradas:", len(m["arquivos"]), "ok:", ok, "divergentes/ausentes:", bad)
# arquivos em disco nao listados
listed = {it["path"] for it in m["arquivos"]}
extra = []
for p in sorted(BASE.rglob("*")):
    if p.is_file() and p.name != "SHA256SUMS_K04_HUBBLE.json" and "__pycache__" not in p.parts:
        rel = str(p.relative_to(BASE)).replace("\\", "/")
        if rel not in listed:
            extra.append(rel)
print("arquivos em disco fora do manifesto:", extra[:10], len(extra))
for n in ("HUBBLE_JA_EXAMINADO_K04.md", "ERRATA_HUBBLE_K04.md", "ERRATA_HUBBLE_K04_R2.md"):
    print(n, hashlib.sha256((ROOT / n).read_bytes()).hexdigest()[:16])
