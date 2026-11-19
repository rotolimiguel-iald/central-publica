import json, sys
P = r"C:\IALD\MAPA_DE_ROTAS\rotas.jsonl"
rota = sys.argv[1]; smin = int(sys.argv[2]); maxc = int(sys.argv[3])
with open(P, "rb") as f:
    for ln, line in enumerate(f, 1):
        try:
            r = json.loads(line.decode("utf-8"))
        except Exception:
            continue
        if r.get("rota_id") != rota or (r.get("seq") or 0) < smin:
            continue
        print("--- seq", r.get("seq"), r.get("tipo"), r.get("registrado_em") or r.get("quando") or "", "olhou_dados=", r.get("olhou_dados"))
        for k in ("titulo", "veredito", "defeito"):
            if r.get(k):
                print("  ", k, ":", str(r[k])[:maxc])
