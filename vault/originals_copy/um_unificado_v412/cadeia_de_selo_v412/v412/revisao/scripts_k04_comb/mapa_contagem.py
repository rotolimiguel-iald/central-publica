import json, collections
P = r"C:\IALD\MAPA_DE_ROTAS\rotas.jsonl"
tot = 0; olhou_rec = 0
rotas = set(); rotas_olhou = set()
dom_rotas = collections.defaultdict(set)
hub = set()
with open(P, "rb") as f:
    for line in f:
        try:
            r = json.loads(line.decode("utf-8"))
        except Exception:
            continue
        tot += 1
        rid = r.get("rota_id")
        if rid:
            rotas.add(rid)
        if r.get("olhou_dados") is True and rid:
            olhou_rec += 1
            rotas_olhou.add(rid)
            dom_rotas[r.get("dominio")].add(rid)
            if rid.startswith(("d1.", "hubble.")) or "h0dn" in rid:
                hub.add(rid)
print("registros", tot, "| rotas distintas", len(rotas))
print("registros com olhou_dados=true", olhou_rec, "| rotas distintas com algum registro olhou_dados=true", len(rotas_olhou))
print("por dominio (rotas):", {k: len(v) for k, v in dom_rotas.items()})
print("rotas olhou_dados em d1.*/hubble.*/h0dn:", len(hub))
print(sorted(hub))
