import unicodedata
from pathlib import Path
t = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\o_que_fica_claro_REV9\O_QUE_FICA_CLARO_v412_R9.md").read_bytes().decode("utf-8")
cs = {}
for ch in t:
    if ord(ch) > 127:
        cs[ch] = cs.get(ch, 0) + 1
for ch, n in sorted(cs.items(), key=lambda x: -x[1]):
    print(repr(ch), "U+%04X" % ord(ch), unicodedata.name(ch, "?"), n)
print("CRLF?", "\r\n" in t, "bytes", len(t.encode("utf-8")), "linhas", t.count("\n"))
