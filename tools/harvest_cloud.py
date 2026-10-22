# -*- coding: utf-8 -*-
"""COLHEITA da nuvem — traz para o disco local o que foi escrito no ar (Evolução v2, Eixo 2).

O ciclo completo do Prompt Compiler remoto:
  operador escreve notas/instruções em https://central.iald.ia.br (de qualquer lugar)
  → a nuvem registra cada escrita no overlay persistente (dual-write, sobrevive a redeploy)
  → ESTA ferramenta (na máquina do operador) autentica com a criptografia dele, baixa os
    registros pendentes, INSCREVE nos .md locais (com backup .bak_colheita_<ts>), reindexa
  → operador confere, commita e dá push (GitHub Desktop) → o repo passa a carregar o
    conteúdo → com --ack os registros saem do overlay da nuvem.

Uso (na raiz da Central):
  backend\\.venv\\Scripts\\python.exe tools\\harvest_cloud.py                (só mostra)
  backend\\.venv\\Scripts\\python.exe tools\\harvest_cloud.py --apply       (inscreve local)
  backend\\.venv\\Scripts\\python.exe tools\\harvest_cloud.py --apply --ack (inscreve + reconhece)
  opções: --url https://central.iald.ia.br (padrão) · --secret-env NOME_DA_ENV · --dry-run

Segurança: o segredo NUNCA vai em argumento de linha de comando por padrão (ficaria no
histórico) — é lido de variável de ambiente (--secret-env) ou digitado sem eco (getpass).
Stdlib pura (urllib + cookiejar): nenhuma dependência nova. 2FA por e-mail suportada.
"""
from __future__ import annotations

import argparse
import getpass
import http.cookiejar
import json
import os
import ssl
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# console Windows pode ser cp1252 — UTF-8 sempre (a saída tem acentos e setas)
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

CENTRAL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CENTRAL))
from backend.app import cloudwrites as CW  # noqa: E402  (apliers idempotentes compartilhados)

DEFAULT_URL = "https://central.iald.ia.br"


class Client:
    def __init__(self, base: str):
        self.base = base.rstrip("/")
        self.jar = http.cookiejar.CookieJar()
        ctx = ssl.create_default_context()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPSHandler(context=ctx),
            urllib.request.HTTPCookieProcessor(self.jar))

    def call(self, method: str, path: str, payload: dict | None = None) -> dict:
        data = json.dumps(payload).encode("utf-8") if payload is not None else None
        req = urllib.request.Request(self.base + path, data=data, method=method,
                                     headers={"Content-Type": "application/json"})
        try:
            with self.opener.open(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")[:400]
            raise SystemExit(f"[colheita] HTTP {e.code} em {path}: {body}")


def login(cli: Client, secret: str) -> None:
    st = cli.call("GET", "/api/auth/status")
    if not st.get("enabled"):
        print("[colheita] servidor sem cripto ativa (modo local) — sem login.")
        return
    r = cli.call("POST", "/api/auth/login", {"secret": secret})
    if r.get("twofa_required"):
        code = input(f"[colheita] código 2FA enviado ({r.get('email_hint', '?')}); digite: ").strip()
        r = cli.call("POST", "/api/auth/2fa", {"challenge": r["challenge"], "code": code})
    role = r.get("role")
    print(f"[colheita] autenticado como {r.get('name')} (papel: {role})")
    if role != "admin":
        raise SystemExit("[colheita] a colheita exige papel ADMIN.")


def backup_targets(records: list[dict]) -> None:
    """Um backup por arquivo-alvo antes da primeira escrita da colheita (a régua)."""
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    seen: set[Path] = set()
    for r in records:
        p = r.get("payload") or {}
        if r.get("kind") == "note_add":
            t = CENTRAL / "patents" / p.get("dir_name", "?") / "notes" / "initial_notes.md"
        elif r.get("kind") == "note_toggle":
            t = CENTRAL / p.get("source_file", "?")
        else:
            continue  # compiled: arquivo NOVO, não sobrescreve nada
        if t.exists() and t not in seen:
            bak = t.with_name(t.name + f".bak_colheita_{ts}")
            bak.write_bytes(t.read_bytes())
            seen.add(t)
    if seen:
        print(f"[colheita] backups .bak_colheita_{ts}: {len(seen)} arquivo(s)")


def run_reindex() -> None:
    py = CENTRAL / "backend" / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    exe = str(py) if py.exists() else sys.executable
    r = subprocess.run([exe, "-m", "backend.app.reindex", "--full"], cwd=str(CENTRAL),
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    tail = (r.stdout or r.stderr or "").strip().splitlines()[-1:]
    print(f"[colheita] reindex --full: rc={r.returncode} {tail}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Colheita do overlay de escrita da nuvem")
    ap.add_argument("--url", default=DEFAULT_URL)
    ap.add_argument("--secret-env", default="", help="nome da env com o segredo (senão getpass)")
    ap.add_argument("--apply", action="store_true", help="inscreve os registros nos .md locais")
    ap.add_argument("--ack", action="store_true", help="reconhece na nuvem os aplicados (com --apply)")
    ap.add_argument("--dry-run", action="store_true", help="lista o que faria, não escreve")
    args = ap.parse_args()

    cli = Client(args.url)
    st = cli.call("GET", "/api/auth/status")
    if st.get("enabled"):
        secret = os.environ.get(args.secret_env, "") if args.secret_env else ""
        if not secret:
            secret = getpass.getpass("[colheita] seu segredo (não ecoa): ")
        login(cli, secret)

    data = cli.call("GET", "/api/cloud-writes")
    recs = data.get("records", [])
    print(f"[colheita] overlay da nuvem: enabled={data.get('enabled')} · pendentes={len(recs)}")
    for r in recs[:50]:
        p = r.get("payload") or {}
        alvo = p.get("dir_name") or p.get("source_file") or p.get("filename") or "?"
        print(f"  · {r.get('ts_utc')} [{r.get('kind')}] por {r.get('user')} → {alvo}")
    if not recs:
        return 0
    if args.dry_run or not args.apply:
        print("[colheita] nada escrito (use --apply para inscrever localmente).")
        return 0

    backup_targets(recs)
    summary = CW.apply_records(CENTRAL, recs)
    print(f"[colheita] aplicação local: { {k: v['n'] for k, v in summary.items() if k != 'pending'} }")
    run_reindex()

    ok_ids = [i for k in ("aplicado", "ja_presente") for i in summary.get(k, {}).get("ids", [])]
    if args.ack:
        r = cli.call("POST", "/api/cloud-writes/ack", {"ids": ok_ids})
        print(f"[colheita] ack na nuvem: {r} (só os aplicados/já-presentes; falhas seguem pendentes)")
    else:
        print("[colheita] registros SEGUEM pendentes na nuvem (rode com --ack após commit+push).")
    print("[colheita] pronto — confira, commite e dê push (GitHub Desktop) para o repo carregar o conteúdo.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
