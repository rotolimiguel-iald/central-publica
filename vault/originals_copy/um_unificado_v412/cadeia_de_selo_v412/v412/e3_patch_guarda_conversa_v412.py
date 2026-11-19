# -*- coding: utf-8 -*-
"""e3_patch_guarda_conversa_v412.py -- adapta guarda_conversa_v412.py (backup .bak_antes_do_patch_e3): a v412 NAO embute falas (DL.FALAS_V412 = [] por desenho) e a guarda de conversa continua protegendo o programa e os rendidos contra as MESMAS 11 falas da casa
(a lista herdada da v411, DL.FALAS_V411): usar DL.FALAS_V412 examinaria ZERO falas, o que seria relaxar o validador herdado. Troca so' isso e a marca. Script da cadeia."""
import hashlib, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "guarda_conversa_v412.py")
raw = open(P, "rb").read(); s = raw.decode("utf-8")
if "[A ADAPTAR v412]" not in s:
    print("ja' adaptado"); sys.exit(0)
bak = P + ".bak_antes_do_patch_e3"
if not os.path.exists(bak):
    open(bak, "wb").write(raw)
i = s.index("# [A ADAPTAR v412]"); j = s.index("\n", i)
s = s[:i] + "# [ADAPTADO v412, 17/11/2026, claude-construtor-v412-ensaio] a v412 NAO embute falas (DL.FALAS_V412 = [] por desenho): a guarda segue contra as MESMAS 11 falas da casa, a lista herdada DL.FALAS_V411 (usar a vazia examinaria zero falas = relaxar o validador); a base da regra (b) e' a da v411 selada (GUARDA_CONVERSA_BASE_v411.json, gerada com --gerar-base)" + s[j:]
assert s.count("enumerate(DL.FALAS_V412)") == 1
s = s.replace("enumerate(DL.FALAS_V412)", "enumerate(DL.FALAS_V411)")
s = s.replace("(DL.FALAS_V412)", "(DL.FALAS_V411, a lista herdada: a v412 nao embute falas)")
tmp = P + ".tmp"
open(tmp, "wb").write(s.encode("utf-8")); assert os.path.getsize(tmp) > len(raw) - 100
os.replace(tmp, P)
print("guarda_conversa_v412.py adaptada:", hashlib.sha256(open(P, "rb").read()).hexdigest()[:16])
