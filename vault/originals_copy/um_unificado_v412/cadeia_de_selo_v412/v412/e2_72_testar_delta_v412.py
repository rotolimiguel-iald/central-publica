import re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
D = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
sys.path.insert(0, str(D))
import delta_v412 as DL
print("delta_v412 importou:", len(vars(DL)), "nomes; UM_VERSION", DL.UM_VERSION, "base", DL.BASE_VERSION, DL.BASE_SHA16_DA_ORDEM, "bundle", DL.N_BUNDLE, "escada", DL.ESCADA_BASE, "->", DL.ESCADA_NOVA, "flags", DL.N_FLAGS)
uso = {}
for p in list(D.glob("*.py")) + list(D.glob("*/*.py")):
    if p.name.startswith(("e2_", "_")) or "bump" in p.parts:
        continue
    t = p.read_bytes().decode("utf-8", "replace")
    if "delta_v412" not in t:
        continue
    for m in re.finditer(r"\bDL\.([A-Za-z_][A-Za-z_0-9]*)", t):
        uso.setdefault(m.group(1), set()).add(p.name)
faltam = {a: sorted(v) for a, v in uso.items() if not hasattr(DL, a)}
print("atributos usados:", len(uso), "| FALTAM:", len(faltam))
for a, v in faltam.items():
    print("   ", a, "<-", v[:4])
