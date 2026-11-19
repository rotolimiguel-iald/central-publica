"""R5 (so' leitura): diferencas, linha a linha, entre a pagina R13 (traduzida para o ingles no R4) e a pagina R18; mostra as linhas da traducao EN da R13 correspondentes as linhas que mudaram."""
import difflib, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
D = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
a = (D / "o_que_fica_claro_REV13" / "O_QUE_FICA_CLARO_v412_R13.md").read_bytes().decode("utf-8").split("\n")
b = (D / "o_que_fica_claro_REV18" / "O_QUE_FICA_CLARO_v412_R18.md").read_bytes().decode("utf-8").split("\n")
en = (D / "O_QUE_FICA_CLARO_v412_R13_EN.md").read_bytes().decode("utf-8").split("\n")
print("linhas R13:", len(a), "| R18:", len(b), "| EN R13:", len(en))
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        continue
    print("\n=== %s R13[%d:%d] -> R18[%d:%d]" % (tag, i1 + 1, i2, j1 + 1, j2))
    for i in range(i1, i2):
        print("  - R13 L%d: %s" % (i + 1, a[i][:260]))
        if i < len(en):
            print("    EN  L%d: %s" % (i + 1, en[i][:10000]))
    for j in range(j1, j2):
        print("  + R18 L%d: %s" % (j + 1, b[j][:140]))
        if tag == "replace" and (j - j1) < (i2 - i1):
            # diferenca de palavras dentro da linha
            wa, wb = a[i1 + (j - j1)].split(" "), b[j].split(" ")
            s2 = difflib.SequenceMatcher(None, wa, wb, autojunk=False)
            for t2, x1, x2, y1, y2 in s2.get_opcodes():
                if t2 != "equal":
                    print("      [%s] «%s» -> «%s»" % (t2, " ".join(wa[x1:x2])[:400], " ".join(wb[y1:y2])[:900]))
