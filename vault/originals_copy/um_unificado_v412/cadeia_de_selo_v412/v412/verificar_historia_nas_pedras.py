# -*- coding: utf-8 -*-
"""Gerencia c1, 17/11/2026: confere, nas fontes Lean de uma pasta, se sobrou HISTORIA DE CONVERSA (regra do operador de 17/11: o
um.py e' a compilacao do que e' verdade; a conversa se registra em paralelo). So' leitura. Lista, por arquivo, as linhas que trazem
marcas de historia. Com --contra <pasta original>, confere tambem que o CODIGO (tudo fora de comentarios e docstrings) e' identico.
Uso: verificar_historia_nas_pedras.py <pasta> [--contra <pasta original>] [--detalhe]"""
import re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
pasta = Path(sys.argv[1])
contra = Path(sys.argv[sys.argv.index("--contra") + 1]) if "--contra" in sys.argv else None
MARCAS = re.compile(
    r"operador|\bautor\b|ger[eê]ncia|revisor|revis[aã]o|parecer|Codex|Kimi|ChatGPT|bancada|\b[Oo]rdem \d+|ORDEM|ENTREGA|\bREV\d+|"
    r"\bR\d\b|\d{2}/\d{2}(?:/20\d\d)?|«|candidata|provis[oó]rio|ratific|\bfala\b|\bfalas\b|por bytes|cunhagens_13out|"
    r"errata|conferid|transpost|sess[aã]o|aferi[cç][aã]o|emenda|ressalva|aprovad|reprovad|\baceito\b|mandou|pediu|respondeu|disse",
    re.I)


def sem_comentarios(t):
    out, i, n, prof = [], 0, len(t), 0
    while i < n:
        if t.startswith("/-", i):
            prof += 1; i += 2; continue
        if prof and t.startswith("-/", i):
            prof -= 1; i += 2; continue
        if prof:
            i += 1; continue
        if t.startswith("--", i):
            while i < n and t[i] != "\n":
                i += 1
            continue
        out.append(t[i]); i += 1
    return "\n".join(l.rstrip() for l in "".join(out).split("\n") if l.strip())


tot = 0
for f in sorted(pasta.glob("*.lean")):
    t = f.read_text(encoding="utf-8")
    achadas = [(k + 1, l.strip()[:110]) for k, l in enumerate(t.split("\n")) if MARCAS.search(l)]
    tot += len(achadas)
    cod = ""
    if contra is not None:
        o = contra / f.name
        cod = " | codigo " + ("IDENTICO" if o.exists() and sem_comentarios(o.read_text(encoding="utf-8")) == sem_comentarios(t) else "DIFERE OU SEM ORIGINAL")
    print("%-34s linhas com marca: %4d%s" % (f.name, len(achadas), cod))
    if "--detalhe" in sys.argv:
        for k, l in achadas[:40]:
            print("     L%-4d %s" % (k, l))
print("TOTAL de linhas com marca:", tot)
