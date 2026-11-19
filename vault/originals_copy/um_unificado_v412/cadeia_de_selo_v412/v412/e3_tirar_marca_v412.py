# -*- coding: utf-8 -*-
"""e3_tirar_marca_v412.py <arquivo> <texto>: troca a linha `# [A ADAPTAR v412] SUBIDA MECANICA ...` do arquivo por uma linha `# [ADAPTADO v412, ...] <texto>` (backup de bytes .bak_antes_da_marca_e3). So' se usa depois de o script ter sido CONFERIDO de verdade (rodou e deu o resultado esperado). Script da cadeia."""
import hashlib, os, sys

p = os.path.join(os.path.dirname(os.path.abspath(__file__)), sys.argv[1]); txt = sys.argv[2]
raw = open(p, "rb").read(); s = raw.decode("utf-8")
if s.count("# [A ADAPTAR v412] SUBIDA") != 1:
    print(sys.argv[1], ": sem a marca (ou mais de uma): nada feito"); sys.exit(0)
bak = p + ".bak_antes_da_marca_e3"
if not os.path.exists(bak):
    open(bak, "wb").write(raw)
i = s.index("# [A ADAPTAR v412] SUBIDA"); j = s.index("\n", i)
s = s[:i] + "# [ADAPTADO v412, 17/11/2026, claude-construtor-v412-ensaio] " + txt + s[j:]
open(p + ".tmp", "wb").write(s.encode("utf-8")); assert os.path.getsize(p + ".tmp") >= len(raw) - 400
os.replace(p + ".tmp", p)
print(sys.argv[1], "marca retirada;", hashlib.sha256(open(p, "rb").read()).hexdigest()[:16])
