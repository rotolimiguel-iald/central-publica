import difflib, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
D = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
a = (D / "o_que_fica_claro_REV9/O_QUE_FICA_CLARO_v412_R9.md").read_bytes().decode("utf-8").split("\n")
b = (D / "o_que_fica_claro_REV13/O_QUE_FICA_CLARO_v412_R13.md").read_bytes().decode("utf-8").split("\n")
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag != "equal":
        print(tag, "R9[%d:%d]" % (i1 + 1, i2), "R13[%d:%d]" % (j1 + 1, j2))
        for l in a[i1:i2]:
            print("  - ", l[:160])
        for l in b[j1:j2]:
            print("  + ", l[:160])
