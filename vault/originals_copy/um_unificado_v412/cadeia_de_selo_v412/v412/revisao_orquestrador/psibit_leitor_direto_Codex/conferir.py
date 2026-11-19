"""Compile as candidatas em diretório isolado. Cada recibo vincula a fonte, o Lean e a saída."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
V412 = HERE.parents[1]
REFERENCE = HERE.parent / "conferencia_029_Codex" / "ADENDO_A" / "COMPILACAO_R1.json"
MODULES = {"LeitorDaFormula", "LeiturasComFolga", "ParPonderado", "PontePalavraVerbo",
           "InformacaoDoResumo", "OPsibitEACompressao", "OPassoEOFim"}

def pin(path):
    raw = path.read_bytes()
    return {"path": str(path), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}

def compile_module(name):
    if name not in MODULES:
        raise ValueError(name)
    ref = json.loads(REFERENCE.read_text(encoding="utf-8-sig"))
    lean = Path(ref["lean"]["arquivo"])
    roots = [str(HERE), *ref["lean_path"], str(V412 / "candidatas_c1" / "build_sobre_limpas")]
    env = dict(os.environ, LEAN_PATH=os.pathsep.join(roots))
    src, obj = HERE / (name + ".lean"), HERE / (name + ".olean")
    before = pin(src)
    started = time.monotonic()
    proc = subprocess.run([str(lean), "-o", obj.name, src.name], cwd=HERE, env=env,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    log = proc.stdout.decode("utf-8", "replace")
    after = pin(src)
    imports = []
    for module in re.findall(r"^import ([\w.]+)$", src.read_text(encoding="utf-8"), re.M):
        rel = Path(*module.split(".")).with_suffix(".olean")
        inputs = [Path(root) / rel for root in roots if (Path(root) / rel).is_file()]
        if not inputs:
            raise RuntimeError("Importação não localizada: " + module)
        imports.append(pin(inputs[0]))
    expected = re.findall(r"^#print axioms ([\w.]+)$", src.read_text(encoding="utf-8"), re.M)
    axioms = {th: sorted(set(ax.strip() for ax in axlist.split(",") if ax.strip()))
              for th, axlist in re.findall(r"'([\w.]+)' depends on axioms: \[([^\]]*)\]", log)}
    for th in re.findall(r"'([\w.]+)' does not depend on any axioms", log):
        axioms[th] = []
    allowed = {"propext", "Classical.choice", "Quot.sound"}
    checked = set(expected) <= set(axioms) and all(set(a) <= allowed for a in axioms.values())
    ok = proc.returncode == 0 and before == after and checked and obj.is_file()
    receipt = dict(source=before, lean=pin(lean), imports=imports, lean_path=roots, rc=proc.returncode,
                   seconds=round(time.monotonic()-started,3), axioms=axioms,
                   required_checks=expected, verified=ok, output=pin(obj) if ok else None,
                   log=log)
    target = HERE / (name + (".verificado.json" if ok else ".diagnostico.json"))
    tmp = target.with_suffix(".tmp")
    tmp.write_bytes((json.dumps(receipt, ensure_ascii=False, indent=2)+"\n").encode())
    if json.loads(tmp.read_bytes()) != receipt:
        raise IOError("Recibo divergente")
    os.replace(tmp, target)
    print(log, end="")
    print("VERIFICADO =",ok)
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(compile_module(sys.argv[1]))
