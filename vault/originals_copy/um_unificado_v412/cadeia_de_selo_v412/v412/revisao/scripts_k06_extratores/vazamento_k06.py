"""Sobreposicao de sequencias de N palavras entre o T6 reservado e os arquivos do Kimi.
IMPRIME SO CONTAGENS. O texto do T6 nunca e impresso nem gravado."""
import re, sys, hashlib
from pathlib import Path
T6 = Path(r"C:\IALD\Artigo\Termostato_Modular\T6_protocol_prompts.txt")
KIMI = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi")
def words(s): return re.findall(r"\w+", s.lower())
def grams(w, n): return {hash(tuple(w[i:i+n])) for i in range(len(w)-n+1)}
raw = T6.read_bytes()
tw = words(raw.decode("utf-8", errors="replace"))
print("T6: bytes", len(raw), "palavras", len(tw))
res = {}
for N in (8, 5):
    res[N] = grams(tw, N)
    print(f"T6: sequencias distintas de {N} palavras:", len(res[N]))
files = [p for p in (KIMI/"K06").rglob("*") if p.is_file() and p.suffix.lower() in {".md",".json",".py",".txt",".lean",".csv"}]
files += [p for p in KIMI.glob("*") if p.is_file() and p.suffix.lower() in {".md",".json",".py",".txt"} and re.search(r"K06|R3|K03", p.name)]
files = sorted(set(files))
tot8 = 0; tot5 = 0; hit = []
for p in files:
    try:
        w = words(p.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        continue
    g8 = grams(w, 8) & res[8]; g5 = grams(w, 5) & res[5]
    tot8 += len(g8); tot5 += len(g5)
    if g8 or g5: hit.append((str(p.relative_to(KIMI)), len(g8), len(g5), len(w)))
print("arquivos varridos:", len(files))
print("arquivos com sobreposicao de 8 palavras:", sum(1 for h in hit if h[1]>0), "| total de sequencias-8 em comum:", tot8)
print("arquivos com sobreposicao de 5 palavras:", sum(1 for h in hit if h[2]>0), "| total de sequencias-5 em comum:", tot5)
for h in sorted(hit, key=lambda x: (-x[1], -x[2]))[:25]:
    print("  ", h[0], "8p=", h[1], "5p=", h[2], "palavras_no_arquivo=", h[3])
