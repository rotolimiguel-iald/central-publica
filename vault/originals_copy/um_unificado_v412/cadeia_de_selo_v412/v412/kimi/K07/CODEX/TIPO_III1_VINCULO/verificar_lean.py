"""Recompile local proof modules in an empty directory with the installed Lean 4.31."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile

from conferir_imports import BUILD, HERE, SOURCE_DIRS, imports

LEAN = Path(os.environ.get("USERPROFILE", "C:/Users/rotol")) / ".elan/toolchains/leanprover--lean4---v4.31.0/bin/lean.exe"
TARGET = "Classificacao"
def verify(extra):
    local = {p.stem:p for folder in SOURCE_DIRS for p in folder.glob("*.lean")}
    imported = [BUILD / ".lake/build/lib/lean"]
    imported.extend(sorted((BUILD / ".lake/packages").glob("*/.lake/build/lib/lean")))
    done = set()
    with tempfile.TemporaryDirectory(prefix="iald-lean-vinculo-") as stage:
        env = {**os.environ, "LEAN_PATH": os.pathsep.join(map(str,[stage,*imported]))}
        def build(name):
            if name in done:
                return
            path = local[name]
            for dep in imports(path):
                if dep in local:
                    build(dep)
            obj = Path(stage) / (name + ".olean")
            run = subprocess.run([str(LEAN),"-R",str(path.parent),"-o",str(obj),str(path)],
                env=env,cwd=stage,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
                encoding="utf-8",errors="replace")
            print(run.stdout, flush=True)
            if run.returncode or not obj.is_file() or "sorryAx" in run.stdout:
                raise RuntimeError("Falha na verificação de " + name)
            done.add(name)
        build(TARGET)
        for name in extra:
            build(name)
    print(f"{len(done)} módulos locais compilados em diretório temporário inicialmente vazio.")
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("extra", nargs="*", help="Módulos complementares para recompilar")
    verify(parser.parse_args().extra)
