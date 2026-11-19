"""Revisor K04/Hubble: 'rotas.py ver <id>' para varias rotas (so leitura); grava JSON em ver/ e imprime campos-chave."""
import json
import subprocess
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
(OUT / "ver").mkdir(exist_ok=True)
ROTAS = r"C:\IALD\MAPA_DE_ROTAS\rotas.py"
PY = r"C:\Python314\python.exe"
ids = sys.argv[1:]
CAMPOS = ["rota_id", "status", "titulo", "pergunta", "dados", "metodo", "resultado", "veredito", "defeito", "nao_refazer", "proximo_passo"]
LIM = 900
for i in ids:
    p = subprocess.run([PY, "-B", "-X", "utf8", ROTAS, "ver", i], capture_output=True, text=True, encoding="utf-8")
    fn = OUT / "ver" / (i.replace("/", "_") + ".json")
    fn.write_text(p.stdout, encoding="utf-8")
    try:
        j = json.loads(p.stdout)
    except Exception as e:
        print("ERRO", i, e, p.stdout[:200], p.stderr[:200])
        continue
    r = j.get("rota", {})
    print("=" * 100)
    for c in CAMPOS:
        v = r.get(c)
        if v:
            print(f"[{c}] {str(v)[:LIM]}")
    regs = j.get("registros", [])
    print(f"[n_registros] {len(regs)} seq: {[x.get('seq') for x in regs][:60]}")
