# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: para a revisao da limpeza, o diff unificado de cada modulo entre origem e pedras_limpas
(como o codigo e' identico, o diff so' mostra texto). Tambem confere, por modulo, que o codigo sem comentarios e'
identico e conta as marcas de historia que sobraram (a mesma expressao do verificador da v412). Saida:
insumos\\DIFF_DA_LIMPEZA_v413.txt e um resumo na tela. Uso: diff_da_limpeza_v413.py [Modulo ...]"""
import difflib, hashlib, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).resolve().parent
O, L = AQUI / "origem" / "TGLExt", AQUI / "pedras_limpas" / "TGLExt"
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


def so_texto(t):
    """as linhas de comentario/docstring, para contar marcas so' no texto (o codigo nao se limpa)."""
    linhas, prof = [], 0
    for l in t.split("\n"):
        tem_texto = prof > 0 or "/-" in l or "--" in l
        prof += l.count("/-") - l.count("-/")
        prof = max(prof, 0)
        if tem_texto:
            linhas.append(l)
    return linhas


nomes = sys.argv[1:] or sorted(p.stem for p in O.glob("*.lean"))
saida, linhas_resumo = [], []
for n in nomes:
    fo, fl = O / (n + ".lean"), L / (n + ".lean")
    if not fl.exists():
        linhas_resumo.append("%-27s FALTA a pedra limpa" % n)
        continue
    a, b = fo.read_text(encoding="utf-8"), fl.read_text(encoding="utf-8")
    ident = sem_comentarios(a) == sem_comentarios(b)
    marcas = [l.strip()[:120] for l in so_texto(b) if MARCAS.search(l)]
    d = list(difflib.unified_diff(a.split("\n"), b.split("\n"), "origem/" + n, "limpa/" + n, lineterm="", n=1))
    saida.append("\n".join(d))
    saida.append("== %s: codigo %s | marcas no texto %d" % (n, "IDENTICO" if ident else "DIFERE", len(marcas)))
    saida.extend("   marca: " + m for m in marcas)
    linhas_resumo.append("%-27s codigo %-8s | %5d -> %5d B | linhas mudadas %4d | marcas no texto %d | sha16 %s" % (
        n, "IDENTICO" if ident else "DIFERE", len(a.encode()), len(b.encode()),
        sum(1 for x in d if x[:1] in "+-" and x[:3] not in ("+++", "---")), len(marcas),
        hashlib.sha256(fl.read_bytes()).hexdigest()[:16]))
dest = AQUI / "DIFF_DA_LIMPEZA_v413.txt"
dados = "\n\n".join(saida).encode("utf-8")
tmp = dest.with_name(dest.name + ".tmp")
tmp.write_bytes(dados)
tmp.replace(dest)
print("\n".join(linhas_resumo))
print("diff completo: %s" % dest)
