# -*- coding: utf-8 -*-
"""gerencia c1, 21/11/2026: a pagina publica R2 da v413, por troca EXATA sobre a R1 (que fica): o ajuste B2 da revisao de
terceiro do candidato, ja aplicado no artigo e nos blocos pelo construtor: o enunciado e' `2 <= resposta`, logo «passa de 2»
vira «chega a 2 ou mais». O contrato R2 (secao 5) manda a pagina receber o mesmo ajuste numa revisao nova. Nenhuma afirmacao
muda. Depois troca, no compositor do handoff, a referencia da pagina R1 pela R2 (backup de bytes)."""
import hashlib, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
D = Path(__file__).resolve().parent
R1, R2 = D / "O_QUE_FICA_CLARO_v413_R1.md", D / "O_QUE_FICA_CLARO_v413_R2.md"
t = R1.read_bytes().decode("utf-8")
a = "> inclinação m acima de ln 2/β, a resposta da leitura, um número de n + 3 bits, passa de 2 se, e só se, a fórmula tem\n"
b = "> inclinação m acima de ln 2/β, a resposta da leitura, um número de n + 3 bits, chega a 2 ou mais se, e só se, a fórmula tem\n"
assert t.count(a) == 1, "trecho nao achado"
t = t.replace(a, b)
assert "passa de 2" not in t
d = t.encode("utf-8")
tmp = R2.with_name(R2.name + ".tmp")
tmp.write_bytes(d)
assert tmp.read_bytes() == d
tmp.replace(R2)
print("R1 %s -> R2 %s" % (hashlib.sha256(R1.read_bytes()).hexdigest()[:16], hashlib.sha256(d).hexdigest()[:16]))
C = D.parent / "montar_handoff_e_linhagem_v413.py"
cb = C.read_bytes()
ct = cb.decode("utf-8")
n1, n2 = ct.count("O_QUE_FICA_CLARO_v413_R1.md"), ct.count("p\\u00fablica R1")
ct = ct.replace("O_QUE_FICA_CLARO_v413_R1.md", "O_QUE_FICA_CLARO_v413_R2.md").replace("p\\u00fablica R1", "p\\u00fablica R2")
assert n1 >= 1
bk = C.with_name(C.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_pag_r2")
bk.write_bytes(cb)
tmp = C.with_name(C.name + ".tmp")
tmp.write_bytes(ct.encode("utf-8"))
tmp.replace(C)
print("compositor: pagina R1->R2 x%d, 'publica R1'->'R2' x%d | sha16 %s" % (n1, n2, hashlib.sha256(C.read_bytes()).hexdigest()[:16]))
