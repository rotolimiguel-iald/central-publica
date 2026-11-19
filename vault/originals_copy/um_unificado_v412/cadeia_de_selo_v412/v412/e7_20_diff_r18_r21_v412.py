"""R7: so' leitura. Mede as diferencas da pagina R18 para a R21: por linha, a diferenca por palavras (trechos que saem e trechos que entram) e as linhas inteiras novas. Serve para emendar a traducao EN da R18 sem retraduzir o que nao mudou."""
import difflib, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
D = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
_v0, _v1 = (sys.argv[1], sys.argv[2]) if len(sys.argv) > 2 else ("18", "21")
a = (D / ("o_que_fica_claro_REV" + _v0) / ("O_QUE_FICA_CLARO_v412_R%s.md" % _v0)).read_bytes().decode("utf-8").split("\n")
b = (D / ("o_que_fica_claro_REV" + _v1) / ("O_QUE_FICA_CLARO_v412_R%s.md" % _v1)).read_bytes().decode("utf-8").split("\n")
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        continue
    print("=== %s a[%d:%d] b[%d:%d]" % (tag, i1 + 1, i2, j1 + 1, j2))
    if tag == "replace" and i2 - i1 == j2 - j1:
        for x, y in zip(a[i1:i2], b[j1:j2]):
            wa, wb = x.split(" "), y.split(" ")
            s2 = difflib.SequenceMatcher(None, wa, wb, autojunk=False)
            for t, p1, p2, q1, q2 in s2.get_opcodes():
                if t != "equal":
                    print("  [%s] SAI: %s" % (t, " ".join(wa[p1:p2])))
                    print("       ENTRA: %s" % " ".join(wb[q1:q2]))
    else:
        for l in b[j1:j2]:
            print("  NOVA: " + l)
        for l in a[i1:i2]:
            print("  SAI: " + l[:200])
