"""Compila somente a candidata isolada, sem tocar fontes canônicas."""
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
libs = [root, old, lake/"build/lib/lean", *(p/".lake/build/lib/lean" for p in sorted((lake/"packages").iterdir())), workshop/"candidatas_c1/build", workshop/"candidatas_c1/build_sobre_limpas", workshop/"candidatas_kimi/build"]
env = dict(os.environ, LEAN_PATH=os.pathsep.join(str(p) for p in libs if p.is_dir()))
source = root/"LeituraBeta.lean"
digest = hashlib.sha256(source.read_bytes()).hexdigest()
r = subprocess.run([str(compiler), "-j", "4", "-o", "LeituraBeta.olean", source.name], env=env, cwd=root, capture_output=True)
msg = (r.stdout+r.stderr).decode("utf8")
log = f"LeituraBeta | SHA256 {digest} | RC {r.returncode}\n{msg}"
(root/"LeituraBeta.log").write_text(log, encoding="utf8")
print(log, flush=True)
sys.exit(1 if r.returncode or "sorryAx" in msg else 0)
