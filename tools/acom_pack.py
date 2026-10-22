# -*- coding: utf-8 -*-
"""
acom_pack — CLI do EMPACOTADOR ACOM (a máquina trabalhando).

Empacota arquivos e PASTAS INTEIRAS num único contêiner .acom, em streaming direto do disco
(sem limite de navegador — GBs), com a criptografia da casa (opcional). Restaura bit-a-bit,
verificando cada SHA-256. É a base do backup da máquina com o próprio sistema/cripto.

USO:
  python tools/acom_pack.py pack <caminhos...> -o backup.acom [-p | --senha-env VAR] [--base DIR]
  python tools/acom_pack.py unpack backup.acom <destino> [-p | --senha-env VAR]
  python tools/acom_pack.py list backup.acom [-p | --senha-env VAR]

SENHA (modo cifrado):
  -p / --senha        pergunta a senha (getpass; confirma no pack). NÃO passe a senha na linha
                      de comando (fica no histórico/lista de processos).
  --senha-env VAR     lê a senha da variável de ambiente VAR.
  (sem senha => modo PLANO: empacota+comprime+integridade, sem cifra.)

A régua: beta = alpha_fine * sqrt(e) (nunca literal); restauração bit-exata; anti zip-slip.
"""
from __future__ import annotations

import argparse
import getpass
import importlib.util
import os
import sys
import time
from pathlib import Path

CENTRAL = Path(__file__).resolve().parent.parent
DISPOSITIVO = CENTRAL / "patents" / "BR102025026951-1_ACOM" / "dispositivo"


def _load_archive():
    """Carrega acom_archive de dentro da pasta do dispositivo (fonte da verdade)."""
    if str(DISPOSITIVO) not in sys.path:
        sys.path.insert(0, str(DISPOSITIVO))
    path = DISPOSITIVO / "acom_archive.py"
    spec = importlib.util.spec_from_file_location("acom_archive", str(path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["acom_archive"] = mod
    spec.loader.exec_module(mod)   # type: ignore
    return mod


def _fmt_bytes(n: int | None) -> str:
    if n is None:
        return "—"
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(n) < 1024 or unit == "TB":
            return f"{n:.1f} {unit}" if unit != "B" else f"{n} B"
        n /= 1024.0
    return f"{n:.1f} TB"


def _get_password(args, *, confirm: bool) -> str | None:
    if getattr(args, "senha_env", None):
        pw = os.environ.get(args.senha_env)
        if not pw:
            sys.exit(f"[erro] variável de ambiente '{args.senha_env}' vazia/ausente.")
        return pw
    if getattr(args, "senha", False):
        pw = getpass.getpass("Senha (código de inscrição): ")
        if confirm:
            pw2 = getpass.getpass("Confirme a senha: ")
            if pw != pw2:
                sys.exit("[erro] as senhas não conferem.")
        if not pw:
            sys.exit("[erro] senha vazia.")
        return pw
    return None


class _Progress:
    def __init__(self, label: str):
        self.label = label
        self.t0 = time.time()
        self.n = 0
        self.bytes = 0

    def __call__(self, path: str, count: int, stored: int):
        self.n = count
        self.bytes += stored
        if count % 50 == 0 or stored > 8 * 1024 * 1024:
            dt = max(time.time() - self.t0, 1e-6)
            sys.stderr.write(f"\r  {self.label}: {count} arquivos · {_fmt_bytes(self.bytes)} · "
                             f"{self.bytes/dt/1024/1024:.1f} MB/s ")
            sys.stderr.flush()

    def done(self):
        sys.stderr.write("\r" + " " * 78 + "\r")
        sys.stderr.flush()


def cmd_pack(A, arch):
    paths = [Path(p) for p in A.paths]
    missing = [str(p) for p in paths if not p.exists()]
    if missing:
        sys.exit(f"[erro] não encontrado: {', '.join(missing)}")
    pw = _get_password(A, confirm=True)
    if pw and not arch.crypto_available():
        sys.exit("[erro] modo cifrado requer o pacote 'cryptography' (pip install cryptography).")
    out = Path(A.out)
    if out.exists() and not A.force:
        sys.exit(f"[erro] {out} já existe (use --force para sobrescrever).")
    prog = _Progress("empacotando")
    t0 = time.time()
    print(f"» empacotando {len(paths)} caminho(s) → {out}  [{'CIFRADO' if pw else 'plano'}]")
    rep = arch.pack_paths(paths, out, password=pw, base=A.base, progress=prog)
    prog.done()
    dt = time.time() - t0
    print(f"✓ {rep['files']} arquivos · entrada {_fmt_bytes(rep.get('total_input_bytes'))} → "
          f"contêiner {_fmt_bytes(rep['container_bytes'])}"
          + (f" ({rep['total_input_bytes']/max(rep['container_bytes'],1):.2f}× compressão)"
             if rep.get('total_input_bytes') else "")
          + f" · {dt:.1f}s")
    print(f"  meta-cadeia SHA-256: {rep['meta_chain']}")
    print(f"  β = α·√e = {rep['beta']['beta_tgl']:.15f} (nunca literal)")


def cmd_unpack(A, arch):
    src = Path(A.container)
    if not src.is_file():
        sys.exit(f"[erro] contêiner não encontrado: {src}")
    pw = _get_password(A, confirm=False)
    dest = Path(A.dest)
    prog = _Progress("restaurando")
    t0 = time.time()
    print(f"» restaurando {src} → {dest}/")
    try:
        rep = arch.unpack_stream(src, dest, password=pw, untrusted=False, progress=prog)
    except ValueError as e:
        prog.done(); sys.exit(f"[erro] {e}")
    prog.done()
    print(f"✓ {rep['restored']} arquivos restaurados · {_fmt_bytes(rep['bytes'])} · "
          f"todos os SHA-256 conferidos · {time.time()-t0:.1f}s")
    print(f"  destino: {rep['dest']}")


def cmd_list(A, arch):
    src = Path(A.container)
    if not src.is_file():
        sys.exit(f"[erro] contêiner não encontrado: {src}")
    pw = _get_password(A, confirm=False)
    try:
        info = arch.inspect(src, password=pw)
    except ValueError as e:
        sys.exit(f"[erro] {e}")
    print(f"contêiner: {src.name}  ·  {info['format']} v{info['version']}  ·  "
          f"{'CIFRADO' if info['encrypted'] else 'plano'}")
    if info.get("listing_locked"):
        print("  (cifrado — informe a senha com -p para listar os arquivos)")
        return
    print(f"  arquivos: {info.get('files')}   meta-cadeia: {str(info.get('meta_chain'))[:16]}…")
    for e in info.get("entries", [])[:1000]:
        print(f"    {_fmt_bytes(e['size']):>10}  {e['method']:<6}  {e['path']}")
    n = info.get("files") or 0
    if n > 1000:
        print(f"    … (+{n - 1000} arquivos)")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="acom_pack", description="Empacotador ACOM — backup em .acom (a máquina trabalhando).")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def add_pw(p):
        p.add_argument("-p", "--senha", action="store_true", help="pergunta a senha (getpass) — modo cifrado")
        p.add_argument("--senha-env", metavar="VAR", help="lê a senha da variável de ambiente VAR")

    p = sub.add_parser("pack", help="empacota arquivos/pastas num .acom")
    p.add_argument("paths", nargs="+", help="arquivos e/ou pastas a empacotar")
    p.add_argument("-o", "--out", required=True, help="arquivo .acom de saída")
    p.add_argument("--base", help="raiz dos caminhos relativos (default: pai comum)")
    p.add_argument("--force", action="store_true", help="sobrescreve a saída se existir")
    add_pw(p)

    u = sub.add_parser("unpack", help="restaura um .acom numa pasta (bit-exato)")
    u.add_argument("container", help="arquivo .acom")
    u.add_argument("dest", help="pasta de destino")
    add_pw(u)

    l = sub.add_parser("list", help="lista o conteúdo de um .acom")
    l.add_argument("container", help="arquivo .acom")
    add_pw(l)

    A = ap.parse_args(argv)
    try:
        sys.stdout.reconfigure(encoding="utf-8")   # type: ignore
        sys.stderr.reconfigure(encoding="utf-8")   # type: ignore
    except Exception:
        pass
    arch = _load_archive()
    {"pack": cmd_pack, "unpack": cmd_unpack, "list": cmd_list}[A.cmd](A, arch)


if __name__ == "__main__":
    main()
