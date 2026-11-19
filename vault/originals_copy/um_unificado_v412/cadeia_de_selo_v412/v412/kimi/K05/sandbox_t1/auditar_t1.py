from pathlib import Path
import re
import subprocess
import sys

BASE = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K05")
CAND = BASE / "candidatas" / "T1_R2.lean"
SRC = BASE / "sandbox_t1" / "sources" / "T1_R2.lean"
OLEAN = BASE / "sandbox_t1" / "build" / "T1_R2.olean"
LOG = BASE / "sandbox_t1" / "logs" / "T1_R2.log"
AUDIT = BASE / "sandbox_t1" / "logs" / "T1_R2_audit.log"
LEAN = Path(r"C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe")

lines = [f'COMMAND: python "{Path(__file__)}"']
try:
    version = subprocess.run([str(LEAN), "--version"], check=True, capture_output=True, text=True).stdout.strip()
except Exception as exc:
    version = f"FALHA ao obter versão: {exc}"
lines.append(f"LEAN_VERSION: {version}")
failures = []

source = CAND.read_text(encoding="utf-8")
compiled_source = SRC.read_text(encoding="utf-8")
log = LOG.read_text(encoding="utf-8")

if source != compiled_source:
    failures.append("candidata e cópia compilada diferem")
if not OLEAN.is_file():
    failures.append("objeto .olean ausente")
if "RC: 0" not in log:
    failures.append("log final não contém RC: 0")
if "Lean (version 4.31.0" not in log or "Lean (version 4.31.0" not in version:
    failures.append("versão Lean 4.31.0 não confirmada")
if re.search(r"\b(?:sorry|admit|axiom)\b|sorryAx", source):
    failures.append("termo proibido na fonte")
if "sorryAx" in log or "declaration uses 'sorry'" in log:
    failures.append("sorry no log")

allowed = {"propext", "Classical.choice", "Quot.sound"}
axiom_lines = [line for line in log.splitlines() if "depends on axioms:" in line]
if not axiom_lines:
    failures.append("nenhum registro de axiomas encontrado")
for line in axiom_lines:
    deps_text = line.split("depends on axioms:", 1)[1].strip()
    deps = {item.strip() for item in deps_text.strip("[]").split(",")}
    if not deps <= allowed:
        failures.append(f"axiomas fora do permitido: {line}")

lines.append(f"ARQUIVOS_IDENTICOS: {source == compiled_source}")
lines.append(f"OLEAN_PRESENTE: {OLEAN.is_file()}")
lines.append(f"PRINT_AXIOMS_REGISTRADOS: {len(axiom_lines)}")
lines.append("AXIOMAS_PERMITIDOS: propext; Classical.choice; Quot.sound")
lines.append(f"FALHAS: {len(failures)}")
for failure in failures:
    lines.append(f"FALHA: {failure}")
rc = 1 if failures else 0
lines.append(f"RC: {rc}")
AUDIT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines[-6:]))
sys.exit(rc)
