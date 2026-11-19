"""Revisor K04/Hubble: consulta o Mapa de Rotas por termos unicos (so leitura).
Saida: tabela de rotas por termo em consulta_mapa_saida.txt e consulta_mapa.json
"""
import json
import subprocess
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROTAS = r"C:\IALD\MAPA_DE_ROTAS\rotas.py"
PY = r"C:\Python314\python.exe"

TERMOS = ["D1B", "Pantheon", "masers", "TDCOSMO", "lentes", "sirenes", "FRB", "SNII", "SN II",
          "H0DN", "fase9", "Hubble", "Cefeidas", "SH0ES", "TRGB", "CCHP", "SBF", "JAGB",
          "FFAT", "R-E", "R-F", "R-G", "intermedi", "Fase 4", "Fase 5", "BBH", "AGN", "SZ",
          "EPM", "megamaser", "H0", "razao de Hubble", "K = E", "forma Q"]

resumo = {}
linhas = []
for t in TERMOS:
    p = subprocess.run([PY, "-B", "-X", "utf8", ROTAS, "consultar", t], capture_output=True, text=True, encoding="utf-8")
    txt = p.stdout
    try:
        j = json.loads(txt)
    except Exception as e:
        resumo[t] = {"erro": str(e), "stdout": txt[:300], "stderr": p.stderr[:300]}
        linhas.append(f"## {t}: ERRO {e}")
        continue
    rs = j.get("rotas", [])
    resumo[t] = {"n": j.get("n"), "truncado": j.get("truncado"), "rotas": [
        {"rota_id": r["rota_id"], "status": r["status"], "n_registros": r.get("n_registros"), "atualizada": r.get("atualizada"),
         "titulo": (r.get("titulo") or "")[:110]} for r in rs]}
    linhas.append(f"## {t}: n={j.get('n')} truncado={j.get('truncado')}")
    for r in rs:
        linhas.append(f"   {r['rota_id']} | {r['status']} | nreg={r.get('n_registros')} | {(r.get('titulo') or '')[:100]}")

(OUT / "consulta_mapa.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=1), encoding="utf-8")
(OUT / "consulta_mapa_saida.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")
print("\n".join(linhas))
