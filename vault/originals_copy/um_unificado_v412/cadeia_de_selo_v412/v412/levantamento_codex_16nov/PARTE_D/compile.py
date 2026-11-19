"""Compile the original gamma candidate and the consumer with the pinned Lean binary."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
SANDBOX = Path("C:/t/k411c/final")
GAMMA = HERE.parents[1] / "candidatas_c1/MontagemDasGamas.lean"
VERSION = (SANDBOX / "lean-toolchain").read_text().strip()
LEAN = Path(os.environ["USERPROFILE"]) / ".elan/toolchains" / VERSION.replace("/", "--").replace(":", "---") / "bin/lean.exe"
O = HERE / "build"
O.mkdir(exist_ok=True)

def pin(path):
    return {"path":str(path),"bytes":path.stat().st_size,"sha256":hashlib.sha256(path.read_bytes()).hexdigest()}

def main():
    args=argparse.ArgumentParser()
    args.add_argument("--step",choices=["all","gamma","product","spatial","real"],default="all")
    step=args.parse_args().step
    env=os.environ.copy()
    libs=[O, SANDBOX/".lake/build/lib/lean"]
    libs.extend(sorted((SANDBOX/".lake/packages").glob("*/.lake/build/lib/lean")))
    env["LEAN_PATH"]=os.pathsep.join(map(str,libs))
    gamma_copy=O/"MontagemDasGamas.lean"
    if step in ["gamma","all"]:
        gamma_copy.write_bytes(GAMMA.read_bytes())
        assert pin(gamma_copy)["sha256"]==pin(GAMMA)["sha256"]
    units=[("gamma",gamma_copy),("product",HERE/"ProdutoFinito.lean"),("spatial",HERE/"ProdutoTresUm.lean"),("real",HERE/"ConjugacaoFinita.lean")]
    for name,src in units:
        if step!="all" and step!=name:continue
        target=O/(src.stem+".olean")
        cmd=[str(LEAN),"-R",str(src.parent),"-o",str(target),str(src)]
        proc=subprocess.run(cmd,cwd=src.parent,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        raw=proc.stdout
        (HERE/(name+".log")).write_bytes(raw)
        content=raw.decode("utf-8",errors="replace")
        print(content)
        if proc.returncode or re.search(r"(?im)^.*(?:warning: declaration uses 'sorry'|error:)",content):
            return proc.returncode or 1
        if name=="real":
            axiom_names=set()
            combined="\n".join((HERE/(label+".log")).read_text(encoding="utf-8") for label,_ in units)
            assert not re.search(r"(?im)^.*(?:warning: declaration uses 'sorry'|error:)",combined)
            for match in re.finditer(r"depends on axioms:\s*\[([^\]]+)\]",combined):
                axiom_names.update(x.strip() for x in match.group(1).split(","))
            assert axiom_names == {"propext","Classical.choice","Quot.sound"}, axiom_names
            sources=[GAMMA,*(s for n,s in units if n!="gamma"),HERE/"compile.py",LEAN,SANDBOX/"lean-toolchain",*(O/(s.stem+".olean") for _,s in units)]
            receipt={"status":"COMPILED_CANDIDATE_AWAITING_DISTINCT_REVIEW","lean_version":subprocess.check_output([str(LEAN),"--version"],env=env,text=True).strip(),
                "source_and_build_pins":[pin(p) for p in sources],"commands":["lean.exe -R <source_dir> -o <local_build>/<stem>.olean <source>"],
                "lean_path":list(map(str,libs)),"axioms_reported":sorted(axiom_names),"log_pins":[pin(HERE/(label+".log")) for label,_ in units]}
            (HERE/"COMPILACAO.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return 0

if __name__=="__main__":
    sys.exit(main())
