"""Etapa 2: deriva base_um_v411.py (leitor de trechos de topo do um.py da v411 selada, copia de bytes em base_v411\\um.py) do base_um_v410.py da v411 por trocas de texto exato."""
import hashlib, sys
from pathlib import Path

D = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
SRC = D.parent / "v411" / "base_um_v410.py"
DST = D / "base_um_v411.py"
t = SRC.read_bytes().decode("utf-8")


def troca(t, a, b, n=1):
    c = t.count(a)
    assert c == n, (a[:60], c, n)
    return t.replace(a, b)


t = troca(t, "# [AUTORAL v411, 12/11/2026, claude-construtor-v411] leitor de trechos do um.py BASE (a v410 selada, copia de bytes em base_v410\\um.py)", "# [DERIVADO v412 pela Etapa 2, de base_um_v410.py] leitor de trechos do um.py BASE (a v411 selada, copia de bytes em base_v411\\um.py)")
t = troca(t, "base_um_v410.py -- extrai do um.py da v410 selada (base_v410\\\\um.py", "base_um_v411.py -- extrai do um.py da v411 selada (base_v411\\\\um.py")
t = troca(t, 'UM = os.path.join(HERE, "base_v410", "um.py")', 'UM = os.path.join(HERE, "base_v411", "um.py")')
t = troca(t, 'os.path.join(HERE, "base_v410", "um_absoluto_selo.json")', 'os.path.join(HERE, "base_v411", "um_absoluto_selo.json")')
t = troca(t, 'selo["um_version"] == "v410", "base_v410\\\\um.py nao e\' a v410 selada"', 'selo["um_version"] == "v411", "base_v411\\\\um.py nao e\' a v411 selada"')
t = t.replace("<base_v410:um.py:%s>", "<base_v411:um.py:%s>").replace('"__name__": "base_um_v410"', '"__name__": "base_um_v411"')
DST.write_bytes(t.encode("utf-8"))
print("gravado", DST, DST.stat().st_size, hashlib.sha256(DST.read_bytes()).hexdigest()[:16])
