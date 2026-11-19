import json, sys, hashlib
from pathlib import Path

CORE = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json")
OUT = Path(__file__).resolve().parent / "core_p7_saida.txt"
raw = CORE.read_bytes()
sha = hashlib.sha256(raw).hexdigest()
core = json.loads(raw.decode("utf-8"))
lines = [f"CORE bytes={len(raw)} sha256={sha}", f"top-level keys: {len(core)}"]

pat = ("collapse", "p7", "iald_prediction", "iald_collapse", "camada_cient", "leitor_finito", "iald_unique")
hits = []

def walk(o, path):
    if isinstance(o, dict):
        for k, v in o.items():
            kl = str(k).lower()
            if any(p in kl for p in pat):
                hits.append((path + "/" + str(k), v))
            walk(v, path + "/" + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, path + f"[{i}]")

walk(core, "")
lines.append(f"hits de chaves: {len(hits)}")
for p, v in hits[:40]:
    s = json.dumps(v, ensure_ascii=False)
    lines.append(f"- {p} :: tipo={type(v).__name__} len={len(s)}")
    lines.append("    " + s[:1500])

# busca textual nos valores de string por IALD_COLLAPSE_V1 e vereditos
needles = ["IALD_COLLAPSE_V1", "TGL_PROVED_BY_COLLAPSE", "NOT_FALSIFIED_UNDERPOWERED", "ARMED", "milenio", "navier"]
found = {n: [] for n in needles}

def walk2(o, path):
    if isinstance(o, dict):
        for k, v in o.items():
            walk2(v, path + "/" + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk2(v, path + f"[{i}]")
    elif isinstance(o, str):
        for n in needles:
            if n.lower() in o.lower() and len(found[n]) < 8:
                idx = o.lower().index(n.lower())
                found[n].append((path, o[max(0, idx - 120): idx + 260].replace("\n", " ")))

walk2(core, "")
for n, lst in found.items():
    lines.append(f"== needle {n}: {len(lst)} (max 8)")
    for p, s in lst:
        lines.append(f"  {p}: {s}")

OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("ok", OUT)
