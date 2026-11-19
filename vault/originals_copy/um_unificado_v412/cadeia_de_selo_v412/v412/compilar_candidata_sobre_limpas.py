# -*- coding: utf-8 -*-
"""Gerencia c1, 17/11/2026: compila UMA candidata nova (candidatas_c1\\<Nome>.lean) so' com o binario do Lean, sobre os compilados
do sandbox k411c MAIS os compilados das pedras da lista vigente (pedras_limpas\\build). NUNCA lake. O .olean e o log vao para
candidatas_c1\\build_sobre_limpas\\. O log traz o sha256 da fonte, o RC e a saida inteira.
Uso: compilar_candidata_sobre_limpas.py <Nome>"""
import hashlib, os, subprocess, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
nome = sys.argv[1]
fonte = V / "candidatas_c1" / (nome + ".lean")
assert fonte.exists(), fonte
LEAN = r"C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe"
SANDBOX = Path(r"C:\t\k411c\final\.lake")
assert Path(LEAN).exists() and SANDBOX.exists()
build = V / "candidatas_c1" / "build_sobre_limpas"; build.mkdir(exist_ok=True)
caminhos = [str(SANDBOX / "build" / "lib" / "lean")]
for p in sorted((SANDBOX / "packages").iterdir()):
    d = p / ".lake" / "build" / "lib" / "lean"
    if d.exists():
        caminhos.append(str(d))
caminhos.append(str(V / "pedras_limpas" / "build")); caminhos.append(str(build))
env = dict(os.environ); env["LEAN_PATH"] = ";".join(caminhos)
t0 = time.time()
r = subprocess.run([LEAN, "-o", str(build / (nome + ".olean")), str(fonte)], env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
saida = (r.stdout or "") + (r.stderr or "")
sha = hashlib.sha256(fonte.read_bytes()).hexdigest()
(build / (nome + ".log")).write_text("FONTE: %s\nSHA256: %s\nRC: %d\nSAIDA:\n%s" % (fonte, sha, r.returncode, saida), encoding="utf-8")
print("%s | RC %d | %d s | avisos %d | erros %d | sorryAx %s | sha16 %s" % (nome, r.returncode, round(time.time() - t0), saida.count("warning:"), saida.count("error:"), "sorryAx" in saida, sha[:16]))
print(saida[-6000:])
