"""Compila módulos adicionais sem escrever na oficina nem nas dependências."""
from pathlib import Path
import hashlib
import os
import subprocess
import sys

root = Path(__file__).resolve().parent
old = root.parent
workshop = old.parents[1] / "v412"
lake = Path("C:/t/k411c/final/.lake")
compiler = Path.home() / ".elan/toolchains/leanprover--lean4---v4.31.0/bin/lean.exe"
allowed = ["SimBase", "SimLiteral", "SimExterior", "SimCompleta"]
modules = sys.argv[1:] or allowed
if any(name not in allowed for name in modules):
    raise SystemExit("Módulo fora da lista.")
libs = [root, old, lake/"build/lib/lean", *(p/".lake/build/lib/lean" for p in sorted((lake/"packages").iterdir())), workshop/"candidatas_c1/build", workshop/"candidatas_c1/build_sobre_limpas", workshop/"candidatas_kimi/build"]
env = dict(os.environ, LEAN_PATH=os.pathsep.join(str(p) for p in libs if p.is_dir()))
for module in modules:
    source = root/(module+".lean")
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    r = subprocess.run([str(compiler), "-j", "4", "-o", module+".olean", source.name], env=env, cwd=root, capture_output=True)
    msg = (r.stdout+r.stderr).decode("utf8")
    log = f"{module} | SHA256 {digest} | RC {r.returncode}\n{msg}"
    (root/(module+".log")).write_text(log, encoding="utf8")
    print(log, flush=True)
    if r.returncode or "sorryAx" in msg: sys.exit(1)

