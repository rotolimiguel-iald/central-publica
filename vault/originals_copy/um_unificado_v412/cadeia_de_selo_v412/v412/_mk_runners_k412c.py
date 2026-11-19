# -*- coding: utf-8 -*-
"""_mk_runners_k412c.py -- (claude-construtor-v412, 17/11/2026) cria C:\\t\\k412c\\run_build.py e run_pos_treino.py a partir dos da k411c (so' os rotulos 410->411, 411->412,
numa passada simultanea, e a data/autoria do comentario). Nao sobrescreve. Molde: v411\\_mk_runners_k411c.py."""
import os, re
SRC = os.path.join("C:" + os.sep, "t", "k411c")
DST = os.path.join("C:" + os.sep, "t", "k412c")
for n in ("run_pos_treino.py", "run_build.py"):
    s = open(os.path.join(SRC, n), "rb").read().decode("utf-8")
    t = re.sub(r"(?<![0-9])(410|411)(?![0-9])", lambda m: str(int(m.group(1)) + 1), s)
    t = t.replace("claude-construtor-v412, a servico da gerencia c1, 12/11/2026", "claude-construtor-v412, a servico da gerencia c1, 17/11/2026")
    assert "411" not in t.replace("v411)", "").replace("k411c", "") or n == "run_pos_treino.py", (n, [l for l in t.splitlines() if "411" in l])
    p = os.path.join(DST, n)
    assert not os.path.exists(p), p
    open(p + ".tmp", "wb").write(t.encode("utf-8")); assert os.path.getsize(p + ".tmp") == len(t.encode("utf-8")); os.replace(p + ".tmp", p)
    print(n, len(s), len(t))
