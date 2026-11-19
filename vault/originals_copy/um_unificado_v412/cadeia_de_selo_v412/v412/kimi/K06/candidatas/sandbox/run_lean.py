from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys

CANDIDATAS = Path(__file__).resolve().parent.parent
SANDBOX = CANDIDATAS / "sandbox"
LOGS = CANDIDATAS / "logs"
KERNEL = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel")
LEAN = Path(r"C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe")


def main() -> int:
    if len(sys.argv) != 3:
        print("uso: python run_lean.py <arquivo.lean> <nome-log>", file=sys.stderr)
        return 64
    source = SANDBOX / sys.argv[1]
    log = LOGS / sys.argv[2]
    LOGS.mkdir(parents=True, exist_ok=True)

    library_paths = [KERNEL / ".lake" / "build" / "lib" / "lean"]
    packages = KERNEL / ".lake" / "packages"
    if packages.is_dir():
        for package in sorted(packages.iterdir()):
            candidate = package / ".lake" / "build" / "lib" / "lean"
            if candidate.is_dir():
                library_paths.append(candidate)
    env = os.environ.copy()
    env["LEAN_PATH"] = os.pathsep.join(str(path) for path in library_paths)

    version_run = subprocess.run(
        [str(LEAN), "--version"], cwd=SANDBOX, env=env,
        text=True, encoding="utf-8", errors="replace", capture_output=True,
    )
    command = [str(LEAN), source.name]
    run = subprocess.run(
        command, cwd=SANDBOX, env=env,
        text=True, encoding="utf-8", errors="replace", capture_output=True,
    )
    text = (
        f"COMMAND: {' '.join(command)}\n"
        f"CWD: {SANDBOX}\n"
        f"VERSION_RC: {version_run.returncode}\n"
        f"VERSION: {version_run.stdout.strip()}{version_run.stderr.strip()}\n"
        f"RC: {run.returncode}\n"
        "STDOUT:\n" + run.stdout +
        "STDERR:\n" + run.stderr
    )
    log.write_text(text, encoding="utf-8", newline="\n")
    print(f"LOG: {log}")
    print(f"VERSION: {version_run.stdout.strip()}")
    print(f"RC: {run.returncode}")
    if run.stdout:
        print(run.stdout, end="")
    if run.stderr:
        print(run.stderr, end="", file=sys.stderr)
    return run.returncode


if __name__ == "__main__":
    raise SystemExit(main())
