# -*- coding: utf-8 -*-
"""Rasterize the patent DRAWINGS PDFs into PNGs for the Render tab.

READS the original drawings PDF under Patentes\\ (read-only) and WRITES PNGs to
patents/<ID>_<SLUG>/renders/drawings/prancha_NN.png (inside the Central). One PNG
per page (a "prancha" may hold several figures). High DPI so the UI can zoom in.
"""
import json
import sqlite3
import sys
from pathlib import Path

import fitz  # PyMuPDF

CENTRAL = Path(r"C:\IALD\Central de Patentes")
DB = CENTRAL / "backend" / "data" / "central.db"
DPI = 180  # good for deep-zoom without huge files


def drawings_docs() -> list[tuple[str, str]]:
    c = sqlite3.connect(str(DB))
    c.row_factory = sqlite3.Row
    rows = c.execute(
        "SELECT patent_id, rel_path FROM document "
        "WHERE doc_role='desenhos' AND patent_id IS NOT NULL AND ext='.pdf' "
        "ORDER BY patent_id").fetchall()
    dir_by_id = {r["id"]: r["dir_name"] for r in c.execute("SELECT id,dir_name FROM patent")}
    c.close()
    return [(r["patent_id"], r["rel_path"], dir_by_id.get(r["patent_id"])) for r in rows]


def rasterize(pdf_path: Path, out_dir: Path) -> list[dict]:
    if out_dir.exists():
        for p in out_dir.glob("prancha_*.png"):
            p.unlink()
    out_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(str(pdf_path))
    zoom = DPI / 72.0
    mat = fitz.Matrix(zoom, zoom)
    made = []
    for i, page in enumerate(doc, 1):
        pix = page.get_pixmap(matrix=mat, alpha=False)
        name = f"prancha_{i:02d}.png"
        pix.save(str(out_dir / name))
        made.append({"file": name, "page": i, "w": pix.width, "h": pix.height})
    doc.close()
    return made


def main() -> None:
    total_imgs = 0
    manifest = {}
    for pid, rel_path, dir_name in drawings_docs():
        if not dir_name:
            continue
        src = CENTRAL / rel_path
        if not src.exists():
            print(f"  [SKIP] ausente: {rel_path}")
            continue
        out = CENTRAL / "patents" / dir_name / "renders" / "drawings"
        made = rasterize(src, out)
        manifest[pid] = {"source": rel_path.replace("\\", "/"),
                         "dir": f"patents/{dir_name}/renders/drawings", "pranchas": made}
        total_imgs += len(made)
        print(f"  {pid}: {len(made)} prancha(s) -> {out.relative_to(CENTRAL)}")
    (CENTRAL / "source_inventory" / "renders_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"total de imagens: {total_imgs} em {len(manifest)} patentes")


if __name__ == "__main__":
    sys.exit(main())
