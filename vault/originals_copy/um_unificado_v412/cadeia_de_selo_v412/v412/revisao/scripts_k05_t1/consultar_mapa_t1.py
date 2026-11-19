# Revisor K05/T1: consulta SOMENTE LEITURA ao Mapa de Rotas (nao registra nada) com termos unicos.
import json, subprocess, sys
PY = r"C:\Python314\python.exe"
ROTAS = r"C:\IALD\MAPA_DE_ROTAS\rotas.py"
termos = ["ergodicidade", "T1", "cunha", "centralizador", "Borchers", "Mautner", "Bisognano", "Digernes", "Choi", "tau_estrela", "produto cruzado"]
saida = {}
for t in termos:
    p = subprocess.run([PY, "-B", "-X", "utf8", ROTAS, "consultar", t], capture_output=True, text=True, encoding="utf-8")
    try:
        j = json.loads(p.stdout)
        saida[t] = {"n": j.get("n"), "cabeca": j.get("cabeca"), "n_registros": j.get("n_registros"),
                    "rotas": [(r["rota_id"], r["status"], (r["titulo"] or "")[:110]) for r in j.get("rotas", [])]}
    except Exception as e:
        saida[t] = {"erro": repr(e), "stdout": p.stdout[:200], "stderr": p.stderr[:200]}
json.dump(saida, open("consultar_mapa_t1_saida.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for t, v in saida.items():
    print("==", t, "n=", v.get("n"), "cabeca=", v.get("cabeca"))
    for r in v.get("rotas", []):
        print("   ", r)
