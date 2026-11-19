"""lista os atributos DL.<nome> (delta_v412) usados pelos scripts da cadeia v412, por arquivo, e quais ja existem no delta_v411 (import por caminho)."""
import importlib.util, os, re, sys, collections
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
D = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
uso = collections.defaultdict(set)
for p in list(D.glob("*.py")) + list(D.glob("*/*.py")):
    if p.name.startswith(("e2_", "_")) or "bump" in p.parts:
        continue
    t = p.read_bytes().decode("utf-8", "replace")
    if not re.search(r"delta_v412", t):
        continue
    for m in re.finditer(r"\bDL\.([A-Za-z_][A-Za-z_0-9]*)", t):
        uso[m.group(1)].add(str(p.relative_to(D)))
print("atributos usados:", len(uso))
# importa o delta_v411 por caminho (so' leitura) para ver o que ja existe
V411 = D.parent / "v411"
sys.path.insert(0, str(V411))
spec = importlib.util.spec_from_file_location("delta_v411", str(V411 / "delta_v411.py"))
try:
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    nomes11 = set(vars(mod))
    print("delta_v411 importou: %d nomes" % len(nomes11))
except Exception as e:
    import traceback; traceback.print_exc(); nomes11 = set()
faltam = {}
for a, arqs in sorted(uso.items()):
    a11 = a.replace("V412", "V411").replace("v412", "v411")
    if a not in nomes11 and a11 not in nomes11:
        faltam[a] = sorted(arqs)
print("usados e SEM equivalente no delta_v411:", len(faltam))
for a, arqs in faltam.items():
    print("  ", a, "<-", ", ".join(x.split("\\")[-1] for x in arqs)[:140])
renomeados = [a for a in uso if (a not in nomes11) and (a.replace("V412", "V411").replace("v412", "v411") in nomes11)]
print("usados com o nome subido (V412) e equivalente V411 no delta:", len(renomeados), renomeados[:60])
