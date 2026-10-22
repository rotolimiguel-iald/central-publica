# -*- coding: utf-8 -*-
"""O botão UM, na linha de comando — gera o tgl.acom localmente (espelho do /api/um/build).

Uso (na raiz da Central):
  backend\\.venv\\Scripts\\python.exe tools\\build_um_acom.py --out tgl.acom
  (pede o código de inscrição sem eco, com dupla digitação — anti-erro; ou --secret-env NOME)
  backend\\.venv\\Scripts\\python.exe tools\\build_um_acom.py --open tgl.acom   (abre e confere)

O segredo NUNCA vai em argumento (histórico). A árvore = a Central inteira (núcleo canônico +
fronteira + 16 patentes com FINAL/rodagem/integridade/patente/memória). Cifrado com a
criptografia da casa (Túnel de Hilbert + AES-256-GCM). β nunca literal; sem veredito físico.
"""
from __future__ import annotations

import argparse
import getpass
import os
import sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

CENTRAL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CENTRAL))
from backend.app import um_acom as UM  # noqa: E402


def _ask_secret() -> str:
    a = getpass.getpass("[um] código de inscrição (o selo — não ecoa): ")
    b = getpass.getpass("[um] confirme o código de inscrição: ")
    if a != b:
        raise SystemExit("[um] os dois códigos não batem — abortado (anti-erro de digitação).")
    if len(a) < 8:
        raise SystemExit("[um] código fraco (mínimo 8 caracteres).")
    return a


def do_build(out: Path, secret: str) -> int:
    files = UM.gather_central_tree()
    print(f"[um] árvore da Central: {len(files)} arquivos "
          f"({len({p.split('/')[0] for p in files if p.startswith('BR')})} patentes + tgl/).")
    container = UM.build(files, secret, {"origin": "cli", "n_patents": 16})
    out.write_bytes(container)
    info = UM.inspect(container)
    print(f"[um] {out.name} gerado: {len(container)/1024:.1f} KB · cifrado {info['cipher']} · "
          f"selo key_id={info['key_id']}")
    print(f"[um] container SHA-256: {info['container_sha256']}")
    print("[um] guarde o código de inscrição: sem ele, o arquivo NÃO abre (é o ponto da cripto).")
    return 0


def do_open(path: Path, secret: str) -> int:
    container = path.read_bytes()
    info = UM.inspect(container)
    print(f"[um] {path.name}: cifrado={info['encrypted']} key_id={info['key_id']} "
          f"n_files={info['n_files']}")
    opened = UM.open_container(container, secret)
    ok = opened["all_files_verified"] and opened["meta_chain_ok"]
    print(f"[um] aberto: {opened['n_files']} arquivos · todos conferidos={opened['all_files_verified']} "
          f"· meta-cadeia OK={opened['meta_chain_ok']}")
    print(f"[um] meta-cadeia: {opened['meta_chain_computed']}")
    for t in opened["tree"][:12]:
        mark = "✓" if t["verified"] else "✗"
        print(f"    {mark} {t['path']}  ({t['size']} B)")
    if opened["n_files"] > 12:
        print(f"    … +{opened['n_files']-12} arquivos")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Gera/abre o tgl.acom (o botão Um na CLI)")
    ap.add_argument("--out", default="tgl.acom", help="arquivo de saída (build)")
    ap.add_argument("--open", dest="open_path", default="", help="abre e confere um tgl.acom")
    ap.add_argument("--secret-env", default="", help="nome da env com o segredo (senão getpass)")
    a = ap.parse_args()

    if a.open_path:
        secret = os.environ.get(a.secret_env, "") if a.secret_env else getpass.getpass("[um] código de inscrição: ")
        return do_open(Path(a.open_path), secret)

    secret = os.environ.get(a.secret_env, "") if a.secret_env else _ask_secret()
    if not secret:
        raise SystemExit("[um] sem código de inscrição.")
    return do_build(Path(a.out), secret)


if __name__ == "__main__":
    sys.exit(main())
