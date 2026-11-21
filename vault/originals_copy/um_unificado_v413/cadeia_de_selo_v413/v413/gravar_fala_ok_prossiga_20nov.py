# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: grava por bytes a fala do operador «ok, prossiga» (resposta ao relato da Bancada e da
leitura do Codex das pedras limpas). Fail-closed se o arquivo ja existir com outro conteudo."""
import hashlib, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
CUNH = Path(__file__).resolve().parents[3] / "work" / "cunhagens_13out"
assert CUNH.is_dir(), CUNH
FALA = CUNH / "OPERADOR_20nov_ok_prossiga_depois_da_bancada_e_da_leitura_das_pedras_verbatim.txt"
d = "ok, prossiga\n".encode("utf-8")
if FALA.exists():
    assert FALA.read_bytes() == d, "fala ja existe com outro conteudo"
else:
    tmp = FALA.with_name(FALA.name + ".tmp")
    tmp.write_bytes(d)
    assert tmp.read_bytes() == d
    tmp.replace(FALA)
print("%s | sha16 %s | %d B" % (FALA.name, hashlib.sha256(FALA.read_bytes()).hexdigest()[:16], len(d)))
