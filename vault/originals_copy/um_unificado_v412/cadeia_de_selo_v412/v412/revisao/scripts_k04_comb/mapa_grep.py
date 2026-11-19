import json, sys, re
P = r"C:\IALD\MAPA_DE_ROTAS\rotas.jsonl"
pat = re.compile(sys.argv[1], re.I)
rota = sys.argv[2] if len(sys.argv) > 2 else None
maxc = int(sys.argv[3]) if len(sys.argv) > 3 else 600
n = 0
with open(P, "rb") as f:
    for ln, line in enumerate(f, 1):
        try:
            r = json.loads(line.decode("utf-8"))
        except Exception:
            continue
        if rota and r.get("rota_id") != rota:
            continue
        s = json.dumps(r, ensure_ascii=False)
        if pat.search(s):
            n += 1
            print("--- linha", ln, "seq", r.get("seq"), r.get("rota_id"), r.get("tipo"), r.get("registrado_em") or r.get("quando") or "")
            for k in ("titulo", "pergunta", "resultado", "veredito", "defeito", "nota", "texto"):
                if r.get(k):
                    print("  ", k, ":", str(r[k])[:maxc])
print("total", n)
