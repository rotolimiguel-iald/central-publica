import json, sys
sys.stdout.reconfigure(encoding="utf-8")
d = json.load(open(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\GUARDA_FRASES_v412.json", encoding="utf-8"))
for g in ("pnp", "fluidos", "f43", "premio"):
    for x in d["controles"][g]:
        print("%-8s %-3s esp=%-6s %s | %s" % (g, "OK" if x["ok"] else "XX", x.get("esperado", "-"), x.get("regras_devolvidas", x.get("regras")), x["controle"][:95]))
print("heranca: n =", len(d["controles"]["heranca"]), "ok =", sum(1 for x in d["controles"]["heranca"] if x["ok"]))
print([ (x["v411"]) for x in d["controles"]["heranca"][:6]])
