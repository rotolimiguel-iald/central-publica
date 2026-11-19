"""Compile one candidate from the local review, reusing the pinned Lean environment."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

here = Path(__file__).resolve().parent
review = here.parent
base = review.parent
ref = json.loads((review / "conferencia_029_Codex/ADENDO_A/COMPILACAO_R1.json").read_bytes())
src = here / (sys.argv[1] + ".lean")
if not src.stem.isidentifier() or src.parent != here:
    sys.exit("Expected a local module name.")
roots = [here, review / "conferencia_curva_estado_Codex", review / "psibit_polinomio_por_letra_Codex",
         review / "psibit_fronteira_fita_Codex", review / "psibit_leitor_direto_Codex",
         base / "candidatas_kimi/build", *map(Path, ref["lean_path"]), base / "candidatas_c1/build_sobre_limpas"]
def pin(p):
    raw = p.read_bytes()
    return {"path":str(p), "bytes":len(raw), "sha256":hashlib.sha256(raw).hexdigest()}

exe = Path(ref["lean"]["arquivo"])
assert pin(exe)["sha256"] == ref["lean"]["sha256"]
start = time.monotonic()
env = dict(os.environ, LEAN_PATH=os.pathsep.join(map(str,roots)))
if len(sys.argv)>2 and sys.argv[2]=="--stdin":
    raise SystemExit(subprocess.run([str(exe),"--stdin"],cwd=here,env=env).returncode)
source = pin(src)
body = src.read_text(encoding="utf-8-sig")
imports = []
for name in re.findall(r"^import ([\w.]+)$",body,re.M):
    obj = Path(*name.split(".")).with_suffix(".olean")
    imports.append(pin(next(p / obj for p in roots if (p / obj).is_file())))
obj = src.with_suffix(".olean")
tmp = here / (src.stem + ".tmp.olean")
proc = subprocess.run([str(exe),"-o",str(tmp),src.name],cwd=here,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
log=proc.stdout.decode("utf-8",errors="replace")
print(log,end="",flush=True)
if proc.returncode:
    sys.exit(proc.returncode)
expected = set(re.findall(r"^#print axioms ([\w.]+)$",body,re.M))
axioms = {n: [s.strip() for s in a.split(",") if s.strip()] for n,a in re.findall(r"'([\w.]+)' depends on axioms: \[([^\]]*)\]",log)}
for n in re.findall(r"'([\w.]+)' does not depend on any axioms",log):
    axioms[n] = []
if not expected or expected != set(axioms) or re.search(r"\b(?:warning|error):",log) or not all(set(a) <= {"propext","Classical.choice","Quot.sound"} for a in axioms.values()):
    sys.exit("Failed the declaration/axiom/warning check")
assert source == pin(src) and imports==[pin(Path(i["path"])) for i in imports]
os.replace(tmp,obj)
receipt=dict(source=source,lean=pin(exe),imports=imports,object=pin(obj),rc=proc.returncode,axioms=axioms,seconds=round(time.monotonic()-start,2),log=log)
target=src.with_suffix(".verificado.json")
work=target.with_suffix(".json.tmp")
raw=(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n").encode()
work.write_bytes(raw)
assert work.read_bytes()==raw
os.replace(work,target)
