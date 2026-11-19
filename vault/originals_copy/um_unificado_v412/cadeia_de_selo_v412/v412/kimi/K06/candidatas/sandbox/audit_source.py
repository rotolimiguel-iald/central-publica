from __future__ import annotations

import hashlib
from pathlib import Path
import re
import sys

SANDBOX = Path(__file__).resolve().parent
CANDIDATAS = SANDBOX.parent
KIMI = SANDBOX.parents[2]
SOURCE = SANDBOX / "LeitorFinito.lean"
LEAN_LOG = CANDIDATAS / "logs" / "LeitorFinito.txt"
MODEL = KIMI / "MODELO_FORMAL_R3_K06.md"
OUT = CANDIDATAS / "logs" / "auditoria_fonte.txt"
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    source = SOURCE.read_text(encoding="utf-8")
    log = LEAN_LOG.read_text(encoding="utf-8")
    checks: list[tuple[str, bool]] = []
    checks.append(("fonte_sem_sorry", re.search(r"\bsorry\b", source) is None))
    checks.append(("fonte_sem_admit_ou_axiom", re.search(r"(?m)^\s*(?:axiom|admit)\b", source) is None))
    checks.append(("fonte_sem_native_decide", "native_decide" not in source))
    checks.append(("lean_rc_zero", "RC: 0" in log))
    checks.append(("lean_4_31_0", "VERSION: Lean (version 4.31.0," in log))
    checks.append(("log_sem_sorryAx", "sorryAx" not in log))
    axiom_lines = [line for line in log.splitlines() if "depends on axioms:" in line]
    unexpected: list[str] = []
    for line in axiom_lines:
        match = re.search(r"depends on axioms: \[([^]]*)\]", line)
        if not match:
            unexpected.append(line)
            continue
        for name in (part.strip() for part in match.group(1).split(",")):
            if name not in ALLOWED:
                unexpected.append(f"{name}: {line}")
    checks.append(("axiomas_presentes", len(axiom_lines) > 0))
    checks.append(("axiomas_somente_trio", not unexpected))
    model = MODEL.read_text(encoding="utf-8")
    checks.append(("ponte_open_no_modelo", "permanece **OPEN**" in model))
    checks.append(("a8_quatro_estados", "quatro estados finais no alvo" in model))
    rc = 0 if all(result for _, result in checks) else 1
    lines = [
        f"COMMAND: {sys.executable} {Path(__file__).resolve()}",
        f"CWD: {SANDBOX}",
        "VERSION: auditoria estática 1; Lean 4.31.0 conferido no log final",
        f"RC: {rc}",
    ]
    lines.extend(f"CHECK {name}: {'PASS' if result else 'FAIL'}" for name, result in checks)
    lines.append(f"AXIOM_LINES: {len(axiom_lines)}")
    lines.extend(f"UNEXPECTED: {item}" for item in unexpected)
    lines.append(f"SHA256 LeitorFinito.lean: {sha256(SOURCE)}")
    lines.append(f"SHA256 MODELO_FORMAL_R3_K06.md: {sha256(MODEL)}")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(lines))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
