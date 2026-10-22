# -*- coding: utf-8 -*-
"""Prove the originals were never modified.

Re-hashes every file under Patentes\\ and compares against the baseline captured
at inventory time (source_inventory/original_hashes.json). Any add / remove /
change is reported. Exit 0 == originals intact.
"""
import hashlib
import json
import sys
from pathlib import Path

CENTRAL = Path(r"C:\IALD\Central de Patentes")
ORIGINALS = CENTRAL / "Patentes"
BASELINE = CENTRAL / "source_inventory" / "original_hashes.json"


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))["hashes"]
    # only the Patentes\ originals are covered by the immutability guarantee
    baseline = {k: v for k, v in baseline.items() if k.startswith("Patentes\\")}

    current = {}
    for path in sorted(ORIGINALS.rglob("*")):
        if path.is_file():
            rel = "Patentes\\" + str(path.relative_to(ORIGINALS))
            current[rel] = sha256_of(path)

    base_keys, cur_keys = set(baseline), set(current)
    added = sorted(cur_keys - base_keys)
    removed = sorted(base_keys - cur_keys)
    changed = sorted(k for k in base_keys & cur_keys if baseline[k] != current[k])

    print(f"baseline={len(baseline)} current={len(current)}")
    print(f"added={len(added)} removed={len(removed)} changed={len(changed)}")
    for k in added:
        print(f"  [ADDED]   {k}")
    for k in removed:
        print(f"  [REMOVED] {k}")
    for k in changed:
        print(f"  [CHANGED] {k}")

    intact = not (added or removed or changed)
    print("VERDICT:", "ORIGINALS_INTACT" if intact else "DRIFT_DETECTED")
    return 0 if intact else 1


if __name__ == "__main__":
    sys.exit(main())
