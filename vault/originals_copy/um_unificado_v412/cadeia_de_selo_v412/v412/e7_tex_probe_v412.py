"""R10 (diagnostico, fora do candidato): pega o dry_v412_<lg>.tex que o ensaio deixou, escapa o sublinhado SO' na coluna do nome das linhas do livro de pedras (`v412 & nome & \\texttt{`), compila com pdflatex em C:\\t\\k412c\\tex_conserto (fora de work)
e lista os erros restantes. Serve para saber se o sublinhado dos dois modulos de nome em minusculas e' o unico defeito do artigo completo, antes de regerar o candidato. Nao toca o candidato nem o ensaio."""
import re, shutil, subprocess, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
SRC = Path(r"C:\t\k412c\dry_v412"); T = Path(r"C:\t\k412c\tex_conserto"); T.mkdir(parents=True, exist_ok=True)
for lg in ("pt", "en"):
    t = (SRC / ("dry_v412_%s.tex" % lg)).read_bytes().decode("utf-8")
    n = 0
    def esc(m):
        global n
        n += 1
        return m.group(1) + m.group(2).replace("_", r"\_") + m.group(3)
    t2 = re.sub(r"(?m)^(v412 & )([A-Za-z0-9_]+)( & )", esc, t)
    f = T / ("c_%s.tex" % lg); f.write_bytes(t2.encode("utf-8"))
    for k in range(2):
        r = subprocess.run(["pdflatex", "-interaction=nonstopmode", f.name], cwd=str(T), capture_output=True, timeout=900)
    log = (T / ("c_%s.log" % lg)).read_bytes().decode("utf-8", "replace")
    errs = [l for l in log.splitlines() if l.startswith("! ")]
    print(lg, "linhas escapadas:", n, "| rc", r.returncode, "| erros:", errs[:8], "| pdf:", (T / ("c_%s.pdf" % lg)).exists())
