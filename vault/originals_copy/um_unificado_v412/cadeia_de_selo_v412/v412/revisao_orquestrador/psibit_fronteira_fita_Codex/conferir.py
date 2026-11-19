"""Recompile the candidate sources with the recorded Lean toolchain and check printed axioms."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

ROOT = Path(__file__).resolve().parent
PREVIOUS = ROOT.parent / "psibit_leitor_direto_Codex"
V412 = ROOT.parents[1]
REF = ROOT.parent / "conferencia_029_Codex" / "ADENDO_A" / "COMPILACAO_R1.json"
MODULES = ["OResumoEPsiBit", "PsiBitNaFronteira", "RelacaoFronteira", "CorrelacoesDistintas", "FitaComCusto", "CustoDaTabela", "TrabalhoPorCorte", "SeletorCompartilhado"]
ALLOWED = {"propext", "Quot.sound", "Classical.choice"}

def pin(path):
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}

def check(module):
    ref = json.loads(REF.read_bytes())
    exe = Path(ref["lean"]["arquivo"])
    assert pin(exe)["sha256"] == ref["lean"]["sha256"]
    roots = [ROOT, PREVIOUS, *map(Path, ref["lean_path"]), V412 / "candidatas_c1" / "build_sobre_limpas"]
    env = dict(os.environ, LEAN_PATH=os.pathsep.join(map(str, roots)))
    src = ROOT / (module + ".lean")
    if module == "OResumoEPsiBit":
        original = V412 / "candidatas_kimi" / src.name
        if not src.exists():
            with src.open("xb") as stream:
                stream.write(original.read_bytes())
        assert src.read_bytes() == original.read_bytes()
    source = pin(src)
    body = src.read_text(encoding="utf-8-sig")
    imports = []
    for name in re.findall(r"^import ([\w.]+)$", body, re.M):
        obj = Path(*name.split(".")).with_suffix(".olean")
        imports.append(pin(next(base / obj for base in roots if (base / obj).exists())))
    needed = re.findall(r"^#print axioms ([\w.]+)$", body, re.M)
    assert needed, "Missing axiom audit"
    obj = ROOT / (module + ".olean")
    begin = time.monotonic()
    proc = subprocess.run([str(exe), "-o", obj.name, src.name], cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    log = proc.stdout.decode("utf-8", errors="replace")
    print(log, end="")
    axioms = {name: [a.strip() for a in values.split(",") if a.strip()] for name, values in re.findall(r"'([\w.]+)' depends on axioms: \[([^\]]*)\]", log)}
    for name in re.findall(r"'([\w.]+)' does not depend on any axioms", log):
        axioms[name] = []
    ok = proc.returncode == 0 and not re.search(r"\b(?:warning|error):", log) and source == pin(src) and set(needed) <= set(axioms) and all(set(v) <= ALLOWED for v in axioms.values())
    if ok:
        receipt = dict(source=source, revision_lean=ref["lean"], imports=imports, object=pin(obj), seconds=round(time.monotonic()-begin,2), rc=proc.returncode, axioms=axioms, log=log)
        path = ROOT / (module + ".verificado.json")
        raw = (json.dumps(receipt, ensure_ascii=False, indent=2)+"\n").encode()
        tmp = path.with_suffix(".json.tmp")
        tmp.write_bytes(raw)
        assert tmp.read_bytes() == raw
        os.replace(tmp,path)
    return ok

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("module", choices=MODULES)
    raise SystemExit(0 if check(parser.parse_args().module) else 1)
