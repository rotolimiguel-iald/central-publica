# -*- coding: utf-8 -*-
"""Immutable inventory of the Central de Patentes originals.

READ-ONLY over `Patentes\\` (the originals): walks the tree, hashes every file
(SHA-256), extracts text from every PDF, and unzips the ePCT bundles — always
writing results OUTSIDE the originals (source_inventory/, vault/).

Outputs:
  source_inventory/discovered_files.json   — path, size, mtime, ext per file
  source_inventory/original_hashes.json    — relpath -> sha256
  vault/normalized_docs/<relpath>.txt      — extracted PDF text (mirror tree)
  vault/originals_copy/zips/<name>/        — extracted COPIES of the ePCT zips
  source_inventory/extraction_report.json  — per-PDF extraction status
"""
import hashlib
import json
import shutil
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from pypdf import PdfReader

CENTRAL = Path(r"C:\IALD\Central de Patentes")
ORIGINALS = CENTRAL / "Patentes"
INV = CENTRAL / "source_inventory"
NORM = CENTRAL / "vault" / "normalized_docs"
ZIPS_OUT = CENTRAL / "vault" / "originals_copy" / "zips"


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def extract_pdf(pdf: Path, out_txt: Path) -> dict:
    status = {"pages": 0, "chars": 0, "ok": False, "error": None}
    try:
        reader = PdfReader(str(pdf))
        parts = []
        for page in reader.pages:
            try:
                parts.append(page.extract_text() or "")
            except Exception as e:  # page-level failure: keep going
                parts.append(f"[[PAGE_EXTRACT_ERROR: {e}]]")
        text = "\n\f\n".join(parts)
        out_txt.parent.mkdir(parents=True, exist_ok=True)
        out_txt.write_text(text, encoding="utf-8")
        status.update(pages=len(reader.pages), chars=len(text), ok=True)
    except Exception as e:
        status["error"] = str(e)
    return status


def walk_and_record(root: Path, rel_prefix: str, discovered: list, hashes: dict,
                    extraction: dict) -> None:
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = rel_prefix + str(path.relative_to(root))
        st = path.stat()
        discovered.append({
            "path": rel,
            "size": st.st_size,
            "mtime": datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds"),
            "ext": path.suffix.lower(),
        })
        hashes[rel] = sha256_of(path)
        if path.suffix.lower() == ".pdf":
            out_txt = NORM / (rel.replace("\\", "/") + ".txt")
            extraction[rel] = extract_pdf(path, out_txt)


def main() -> None:
    INV.mkdir(exist_ok=True)
    NORM.mkdir(parents=True, exist_ok=True)
    ZIPS_OUT.mkdir(parents=True, exist_ok=True)

    discovered, hashes, extraction = [], {}, {}
    walk_and_record(ORIGINALS, "Patentes\\", discovered, hashes, extraction)

    # ePCT zips: copy out of the originals, extract the COPY, then inventory it
    for z in sorted(ORIGINALS.rglob("*.zip")):
        rel = z.relative_to(ORIGINALS)
        dest_zip = ZIPS_OUT / rel.name
        if not dest_zip.exists():
            shutil.copy2(z, dest_zip)
        target = ZIPS_OUT / rel.stem
        try:
            with zipfile.ZipFile(dest_zip) as zf:
                zf.extractall(target)
            walk_and_record(target, f"vault_zip::{rel.stem}\\",
                            discovered, hashes, extraction)
        except Exception as e:
            extraction[f"zip::{rel}"] = {"ok": False, "error": str(e)}

    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    (INV / "discovered_files.json").write_text(
        json.dumps({"generated_utc": stamp, "root": str(ORIGINALS),
                    "count": len(discovered), "files": discovered},
                   ensure_ascii=False, indent=1), encoding="utf-8")
    (INV / "original_hashes.json").write_text(
        json.dumps({"generated_utc": stamp, "algorithm": "sha256",
                    "count": len(hashes), "hashes": hashes},
                   ensure_ascii=False, indent=1), encoding="utf-8")
    (INV / "extraction_report.json").write_text(
        json.dumps({"generated_utc": stamp, "count": len(extraction),
                    "pdfs": extraction}, ensure_ascii=False, indent=1),
        encoding="utf-8")

    ok = sum(1 for v in extraction.values() if v.get("ok"))
    print(f"files={len(discovered)} hashed={len(hashes)} "
          f"pdfs_extracted_ok={ok}/{len(extraction)}")


if __name__ == "__main__":
    sys.exit(main())
