import json, sys
P = r"C:\IALD\MAPA_DE_ROTAS\rotas.jsonl"
want = {}
for a in sys.argv[2:]:
    want[int(a)] = True
maxc = int(sys.argv[1])
with open(P, "rb") as f:
    for ln, line in enumerate(f, 1):
        try:
            r = json.loads(line.decode("utf-8"))
        except Exception:
            continue
        if r.get("seq") in want:
            print("--- seq", r.get("seq"), r.get("rota_id"), r.get("tipo"), r.get("registrado_em") or "", "olhou_dados=", r.get("olhou_dados"))
            for k in ("titulo", "pergunta", "metodo", "resultado", "veredito", "defeito", "nota"):
                if r.get(k):
                    print("  ", k, ":", str(r[k])[:maxc])
