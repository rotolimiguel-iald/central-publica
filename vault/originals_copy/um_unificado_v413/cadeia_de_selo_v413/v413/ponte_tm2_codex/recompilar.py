"""Recompila as duas candidatas na caixa usada pelo Kimi, em ordem de importação."""
from pathlib import Path
import hashlib
import os
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
WORKSHOP = ROOT.parents[1] / "v412"
LAKE = Path("C:/t/k411c/final/.lake")
LEAN = Path.home() / ".elan/toolchains/leanprover--lean4---v4.31.0/bin/lean.exe"


def main():
    libraries = [
        ROOT, LAKE / "build/lib/lean",
        *(p / ".lake/build/lib/lean" for p in sorted((LAKE / "packages").iterdir())),
        WORKSHOP / "candidatas_c1/build", WORKSHOP / "candidatas_c1/build_sobre_limpas",
        WORKSHOP / "candidatas_kimi/build",
    ]
    env = dict(os.environ, LEAN_PATH=os.pathsep.join(str(p) for p in libraries if p.is_dir()))
    version = subprocess.check_output([str(LEAN), "--version"], encoding="utf8").strip()
    names = ["APonteAoTM2", "AMaquinaTM2DaVerificacao"]
    if sys.argv[1:] == ["--maquina"]:
        bridge = ROOT / "APonteAoTM2.lean"
        bridge_log = bridge.with_suffix(".log").read_text(encoding="utf8")
        if hashlib.sha256(bridge.read_bytes()).hexdigest() not in bridge_log or "RC 0" not in bridge_log:
            raise ValueError("Recompile a ponte antes da máquina.")
        names = names[1:]
    elif sys.argv[1:]:
        raise SystemExit("Uso: recompilar.py [--maquina]")
    for name in names:
        source = ROOT / (name + ".lean")
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        started = time.monotonic()
        result = subprocess.run([str(LEAN), "-j", "2", "-o", name + ".olean", source.name],
                                cwd=ROOT, env=env, capture_output=True)
        output = (result.stdout + result.stderr).decode("utf8")
        log = f"{version}\n{source.name} SHA256 {digest}\nRC {result.returncode}\n{output}"
        print(f"{name} | RC {result.returncode} | {time.monotonic()-started:.1f}s", flush=True)
        print(output, flush=True)
        destination = ROOT / (name + ".log")
        temporary = ROOT / (name + f".{os.getpid()}.tmp")
        raw = log.encode("utf8")
        temporary.write_bytes(raw)
        if temporary.read_bytes() != raw:
            raise OSError(f"Falha ao verificar {temporary}")
        temporary.replace(destination)
        if result.returncode or any(s in output for s in ("warning:", "error:", "sorryAx")):
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
