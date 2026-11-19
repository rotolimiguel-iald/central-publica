"""Rebuild REV21 and the Hermitian-to-vector bridge with the installed Lean toolchain."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

BASE = Path(__file__).resolve().parent
BUILD = BASE / "build"
SANDBOX = Path("C:/t/k411c/final")
CANDIDATE = BASE.parents[1] / "candidatas_c1/REV21/BoostEDissipador.lean"
TOOLCHAIN = SANDBOX / "lean-toolchain"
LEAN = Path(os.environ["USERPROFILE"]) / ".elan/toolchains" / TOOLCHAIN.read_text().strip().replace("/", "--").replace(":", "---") / "bin/lean.exe"
STANDARD_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}

def pin(path):
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size}

def run_unit(source, env):
    target = BUILD / (source.stem + ".olean")
    command = [str(LEAN), "-R", str(source.parent), "-o", str(target), str(source)]
    run = subprocess.run(command, cwd=source.parent, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    log = BASE / (source.stem + ".log")
    log.write_bytes(run.stdout)
    output = run.stdout.decode("utf8")
    print(output, flush=True)
    reports = re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", output)
    names = {item.strip() for _, group in reports for item in group.split(",")}
    declarations = re.findall(r"^#print axioms\s+(\S+)", source.read_text(encoding="utf-8-sig"), flags=re.M)
    if run.returncode or not declarations or [name for name, _ in reports] != declarations or names != STANDARD_AXIOMS or re.search(r"(?im)\b(error|warning):", output):
        raise SystemExit(run.returncode or 1)
    return {"source": pin(source), "object": pin(target), "log": pin(log), "command": command,
            "returncode": run.returncode, "declarations_checked": declarations, "reported_axioms": sorted(names)}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--unit", choices=["all", "candidate", "bridge"], default="all")
    unit = parser.parse_args().unit
    BUILD.mkdir(exist_ok=True)
    libs = [BUILD, SANDBOX / ".lake/build/lib/lean", *sorted((SANDBOX / ".lake/packages").glob("*/.lake/build/lib/lean"))]
    env = dict(os.environ, LEAN_PATH=os.pathsep.join(map(str,libs)))
    source = BUILD / CANDIDATE.name
    candidate_receipt = BASE / "REV21_COMPILADA.json"
    if unit in ("all", "candidate"):
        source.write_bytes(CANDIDATE.read_bytes())
        result = run_unit(source, env)
        result["original"] = pin(CANDIDATE)
        assert result["original"]["sha256"] == result["source"]["sha256"]
        candidate_receipt.write_text(json.dumps(result, indent=2, ensure_ascii=False)+"\n",encoding="utf8")
    if unit in ("all", "bridge"):
        previous = json.loads(candidate_receipt.read_text(encoding="utf8"))
        for key in ("original", "source", "object", "log"):
            assert previous[key] == pin(Path(previous[key]["path"])), key
        bridge = run_unit(BASE / "SpinorToSolder.lean", env)
        receipt = {"status": "CANDIDATA_COMPILADA", "toolchain": pin(TOOLCHAIN), "executable": pin(LEAN),
                   "version": subprocess.check_output([str(LEAN),"--version"], text=True).strip(),
                   "lean_path": list(map(str, libs)), "builder": pin(Path(__file__)), "candidate": previous,
                   "bridge": bridge, "solder_object": pin(SANDBOX / ".lake/build/lib/lean/TGLExt/Solder4D.olean")}
        canonical = Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt")
        dependencies = ["Solder4D", "HermitianLocalCoordinates", "TensorNullCone",
                        "SitePauliObservables", "TheAxiomAndTheFalseWitness"]
        receipt["dependencies"] = []
        for name in dependencies:
            release_source = pin(canonical / (name + ".lean"))
            compiled_source = pin(SANDBOX / "TGLExt" / (name + ".lean"))
            assert release_source["sha256"] == compiled_source["sha256"], name
            receipt["dependencies"].append({"canonical_source": release_source, "sandbox_source": compiled_source,
                "sandbox_object": pin(SANDBOX / ".lake/build/lib/lean/TGLExt" / (name + ".olean"))})
        (BASE / "COMPILACAO.json").write_text(json.dumps(receipt, indent=2, ensure_ascii=False)+"\n",encoding="utf8")

if __name__ == "__main__":
    main()
