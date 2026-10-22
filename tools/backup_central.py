# -*- coding: utf-8 -*-
"""Backup dos DADOS VIVOS da Central (patents/ + fronteira_tgl/ + os selos/manifests), num zip
timestampado, para `backups/` (fora do controle de versao). NAO toca os originais do INPI (que
sao READ-ONLY e ja hasheados). Exclui venvs/caches/node_modules e nunca inclui confidenciais.

Uso:  python tools/backup_central.py [--full]
  (padrao: patents/ + fronteira_tgl/ + tools/ + backend/app/ + SEGURANCA_REMOTA.md;
   --full inclui tambem os results/seals volumosos)
"""
import sys, zipfile, hashlib, json
from pathlib import Path
from datetime import datetime, timezone

CENTRAL = Path(__file__).resolve().parent.parent
BACKUPS = CENTRAL / "backups"
CONFIDENTIAL = ("iald_stack_v7", "iald_psion_state", "iald_web_server", "token_huggin")
SKIP_PARTS = ("__pycache__", "node_modules", ".venv", "tgl_env", "site-packages", ".git", "backups")
FULL = "--full" in sys.argv

# o que entra no backup (dados vivos + o codigo da plataforma)
INCLUDE = ["patents", "fronteira_tgl", "tools", "backend/app", "frontend/src",
           "architecture", "SEGURANCA_REMOTA.md", "CLAUDE.md"]
# pesados: so' com --full
HEAVY = ("results", "seals", "renders")


def _skip(rel_parts, name):
    if any(p in SKIP_PARTS for p in rel_parts):
        return True
    if any(c in name.lower() for c in CONFIDENTIAL):
        return True
    if not FULL and any(h in rel_parts for h in HEAVY):
        return True
    return False


def main():
    BACKUPS.mkdir(exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
    out = BACKUPS / f"central_backup_{ts}{'_full' if FULL else ''}.zip"
    n, total = 0, 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for item in INCLUDE:
            base = CENTRAL / item
            if not base.exists():
                continue
            if base.is_file():
                z.write(base, item); n += 1; total += base.stat().st_size
                continue
            for f in base.rglob("*"):
                if not f.is_file():
                    continue
                rel = f.relative_to(CENTRAL)
                if _skip(rel.parts, f.name) or f.stat().st_size > 50_000_000:
                    continue
                z.write(f, rel.as_posix()); n += 1; total += f.stat().st_size
    sha = hashlib.sha256(out.read_bytes()).hexdigest()
    manifest = {"backup": out.name, "created_utc": ts, "files": n,
                "uncompressed_bytes": total, "zip_bytes": out.stat().st_size,
                "sha256": sha, "full": FULL,
                "note": "dados vivos da Central; originais INPI nao incluidos (READ-ONLY, ja hasheados); confidenciais excluidos"}
    (BACKUPS / f"central_backup_{ts}.manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"backup: {out.name} — {n} arquivos, {out.stat().st_size // 1024} KB, sha256 {sha[:16]}")
    # retencao: mantem os 10 zips mais recentes
    zips = sorted(BACKUPS.glob("central_backup_*.zip"), key=lambda p: p.stat().st_mtime, reverse=True)
    for old in zips[10:]:
        old.unlink(missing_ok=True)
        (old.with_suffix("").with_suffix(".manifest.json")).unlink(missing_ok=True)
    print(f"retencao: {min(len(zips), 10)} backups mantidos em backups/")


if __name__ == "__main__":
    main()
