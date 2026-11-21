# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: monta a CAIXA da v413 para compilar as pedras novas na forma do kernel (TGLExt.X). O Lean
procura um pacote numa raiz so' (a primeira que tem a pasta TGLExt), entao os .olean da v412 e os novos tem de morar na
mesma arvore. Faz LINKS FISICOS (os.link) de cada TGLExt\\**\\*.olean da caixa da v412 (C:\\t\\k412c\\final, so' leitura)
em insumos\\caixa_v413\\TGLExt\\...; nada e' copiado nem escrito na caixa da v412. Um modulo do kernel que a v413 corrige
(OResumoEPsiBit) tem o link desfeito antes de compilar (desfazer o link nao toca o arquivo da v412).
Recibo: insumos\\caixa_v413\\CAIXA.json."""
import hashlib, json, os, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).resolve().parent
ORIG = Path(r"C:\t\k412c\final\.lake\build\lib\lean\TGLExt")
CAIXA = AQUI / "caixa_v413"
assert ORIG.is_dir()
n_novos, n_ja = 0, 0
for f in ORIG.rglob("*.olean"):
    dest = CAIXA / "TGLExt" / f.relative_to(ORIG)
    if dest.exists():
        assert os.path.samefile(f, dest) or dest.stat().st_nlink == 1, dest
        n_ja += 1
        continue
    dest.parent.mkdir(parents=True, exist_ok=True)
    os.link(f, dest)
    assert os.path.samefile(f, dest)
    n_novos += 1
total = sum(1 for _ in ORIG.rglob("*.olean"))
rec = {"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "origem": str(ORIG), "caixa": str(CAIXA / "TGLExt"),
       "oleans_da_v412": total, "links_novos": n_novos, "ja_existiam": n_ja, "modo": "links fisicos (os.link)"}
d = json.dumps(rec, ensure_ascii=False, indent=1).encode("utf-8")
tmp = CAIXA / "CAIXA.json.tmp"
tmp.write_bytes(d)
assert tmp.read_bytes() == d
tmp.replace(CAIXA / "CAIXA.json")
print("caixa_v413: %d oleans da v412 | links novos %d | ja existiam %d" % (total, n_novos, n_ja))
