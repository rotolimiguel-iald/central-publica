# Revisor K05/tau (tarefa 4): confere cada citacao kimi-cite:// do TAU_ESTRELA_R2.md.
# Para cada uma: arquivo existe? linha existe? o trecho citado esta no arquivo? esta NA linha (ou a +-3 linhas)?
import re, sys, json
from pathlib import Path
from urllib.parse import urlparse, parse_qs

REPORT = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\TAU_ESTRELA_R2.md")
OUT = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\revisao\scripts_k05_tau\revisor_citacoes_saida.json")
text = REPORT.read_text(encoding="utf-8")
cites = re.findall(r"\[([^\]]+)\]\((kimi-cite://[^)\s]+)(?: \"citation\")?\)", text)
rows = []
for label, url in cites:
    p = urlparse(url)
    q = parse_qs(p.query)
    path = Path(q.get("path", [""])[0])
    snippet = q.get("text", [""])[0]
    line = int(q["line"][0]) if "line" in q else None
    row = {"label": label, "kind": p.netloc, "path": str(path), "line": line, "snippet": snippet[:80]}
    if not path.is_file():
        row["status"] = "ARQUIVO_INEXISTENTE"
        rows.append(row); continue
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    full = "\n".join(lines)
    row["n_lines"] = len(lines)
    row["snippet_in_file"] = snippet in full if snippet else None
    if line is not None:
        if not 1 <= line <= len(lines):
            row["status"] = "LINHA_FORA"
        else:
            lo, hi = max(0, line - 4), min(len(lines), line + 3)
            window = "\n".join(lines[lo:hi])
            row["snippet_near_line"] = (snippet in window) if snippet else None
            # onde de fato esta o trecho
            if snippet:
                locs = [i + 1 for i, l in enumerate(lines) if snippet.split("\n")[0] in l]
                row["snippet_lines"] = locs[:6]
            row["status"] = "OK" if row["snippet_near_line"] or not snippet else "TRECHO_FORA_DA_LINHA"
    else:
        if snippet:
            locs = [i + 1 for i, l in enumerate(lines) if snippet.split("\n")[0] in l]
            row["snippet_lines"] = locs[:6]
        row["status"] = "OK" if row["snippet_in_file"] else "TRECHO_AUSENTE"
    rows.append(row)
OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
for r in rows:
    print(r["status"], "|", r["label"], "|", Path(r["path"]).name, "| linha", r["line"], "| trecho em", r.get("snippet_lines"), "|", r["snippet"][:50])
print("total", len(rows), "nao-OK", sum(1 for r in rows if r["status"] != "OK"))
