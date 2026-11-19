# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: compila UMA candidata da gerencia (candidatas_c1\\<Nome>.lean) so' com o binario do Lean, sobre os
compilados do k411c, os das 44 da oitava lista (pedras_limpas\\build) e os das fontes novas (pedras_novas\\build). Saida em
candidatas_c1\\build_sobre_novas\\. NUNCA lake. Uso: compilar_candidata_c1_sobre_novas.py <Nome>"""
import hashlib, os, subprocess, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent; nome = sys.argv[1]
f = V / "candidatas_c1" / (nome + ".lean"); build = V / "candidatas_c1" / "build_sobre_novas"; build.mkdir(exist_ok=True)
LEAN = r"C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe"
SANDBOX = Path(r"C:\t\k411c\final\.lake")
caminhos = [str(SANDBOX / "build" / "lib" / "lean")] + [str(p / ".lake" / "build" / "lib" / "lean") for p in sorted((SANDBOX / "packages").iterdir()) if (p / ".lake" / "build" / "lib" / "lean").exists()]
caminhos += [str(V / "pedras_limpas" / "build"), str(V / "pedras_novas" / "build")]
env = dict(os.environ); env["LEAN_PATH"] = ";".join(caminhos); t0 = time.time()
r = subprocess.run([LEAN, "-o", str(build / (nome + ".olean")), str(f)], env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
saida = (r.stdout or "") + (r.stderr or ""); sha = hashlib.sha256(f.read_bytes()).hexdigest()
(build / (nome + ".log")).write_text("FONTE: %s\nSHA256: %s\nRC: %d\nSAIDA:\n%s" % (f, sha, r.returncode, saida), encoding="utf-8")
print("%s RC %d | %d s | avisos %d | erros %d | sorryAx %s | sha16 %s" % (nome, r.returncode, round(time.time() - t0), saida.count("warning:"), saida.count("error:"), "sorryAx" in saida, sha[:16]))
print(saida[-3500:])
