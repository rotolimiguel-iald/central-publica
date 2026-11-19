"""Check the local Lean imports against read-only canonical project sources."""
from pathlib import Path
from hashlib import sha256
import json
import re
import sys

HERE = Path(__file__).resolve().parent
BUILD = Path("C:/t/k411c/final")
CANON = Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel")
FAMILIES = {"TGL", "TGLExt"}
SOURCE_DIRS = [HERE, *(HERE / x for x in ("Horizonte", "Torre", "Nucleo", "Espectro"))]

def digest(path):
    return sha256(path.read_bytes()).hexdigest()

def imports(path):
    # Strip nested Lean comments before reading the initial import commands.
    raw = path.read_text(encoding="utf-8-sig")
    depth = 0
    for line in raw.splitlines():
        clean = ""
        for part in re.split(r"(/-|-\/|--)", line):
            if part == "--" and not depth:
                break
            if part == "/-":
                depth += 1
            elif part == "-/" and depth:
                depth -= 1
            elif not depth:
                clean += part
        match = re.match(r"^\s*(?:(?:public|private|meta)\s+)*import\s+(.*)$", clean)
        if match:
            yield from match[1].split()

def main():
    local = {p.stem:p for d in SOURCE_DIRS for p in d.glob("*.lean")}
    targets = sys.argv[1:] or ["Classificacao"]
    unknown = set(targets) - local.keys()
    if unknown:
        raise ValueError(f"unknown local modules: {sorted(unknown)}")
    stack = list(targets)
    seen = set()
    records = {}
    while stack:
        name = stack.pop()
        if name in seen:
            continue
        seen.add(name)
        if name in local:
            path = local[name]
        elif name.split(".")[0] in FAMILIES:
            rel = Path(*name.split(".")).with_suffix(".lean")
            path = BUILD / rel
            canon = CANON / rel
            obj = BUILD / ".lake/build/lib/lean" / rel.with_suffix(".olean")
            records[name] = {"build_source":digest(path), "canonical_source":digest(canon),
                             "imported_olean":digest(obj)}
        else:
            continue
        stack.extend(imports(path))
    diff = [k for k,v in records.items() if v["build_source"] != v["canonical_source"]]
    report = {"canonical_root":str(CANON), "compiled_tree":str(BUILD), "compared":len(records),
              "targets":targets, "differences":diff, "kernel_imports":dict(sorted(records.items())),
              "scope":"Imported TGL/TGLExt project sources and object hashes. Third-party caches reused."}
    print(json.dumps(report,ensure_ascii=True,indent=2))
    return bool(diff) or not records
if __name__ == "__main__":
    sys.exit(main())
