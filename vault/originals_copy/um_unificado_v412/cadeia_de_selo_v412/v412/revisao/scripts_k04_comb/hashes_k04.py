import hashlib, json, os, re
base = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi"
val = json.loads(open(os.path.join(base, "VALIDACAO_K04.json"), "rb").read().decode("utf-8"))
bad = 0
for nome, d in val["pins"].items():
    p = d["path"]
    b = open(p, "rb").read()
    h = hashlib.sha256(b).hexdigest()
    ok = (h == d["sha256"] and len(b) == d["bytes"])
    if not ok: bad += 1
    print(("OK  " if ok else "DIFF"), nome, len(b), h[:16], "esperado", d["sha256"][:16], d["bytes"])
for k, d in val["operator_order_pins"].items():
    b = open(d["path"], "rb").read()
    h = hashlib.sha256(b).hexdigest()
    print(("OK  " if h == d["sha256"] and len(b) == d["bytes"] else "DIFF"), k, len(b), h[:16])
# hashes do DEPOSITO
dep = open(os.path.join(base, "DEPOSITO_K04.md"), "rb").read().decode("utf-8")
for nome in ("ENTREGA_K04.md", "REGISTRO_MAPA_K04.json", "VALIDACAO_K04.json"):
    h = hashlib.sha256(open(os.path.join(base, nome), "rb").read()).hexdigest()
    print("DEPOSITO cita", nome, h in dep)
print("palavras no DEPOSITO: 'aprovad' =", "aprovad" in dep.lower(), "| 'revisada internamente' =", "revisada internamente" in dep)
# refs do registro existem?
import importlib.util
spec = importlib.util.spec_from_file_location("rotas_mod", r"C:\IALD\MAPA_DE_ROTAS\rotas.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
regs = m._parse(m._ler_bytes(m.LIVRO))
ids = {r["rota_id"] for r in regs if r["tipo"] == "ROTA"}
reg = json.loads(open(os.path.join(base, "REGISTRO_MAPA_K04.json"), "rb").read().decode("utf-8"))
for r in reg["refs"]:
    print("ref", r, "existe" if r in ids else "NAO EXISTE")
print("registro 'aprovad':", "aprovad" in json.dumps(reg, ensure_ascii=False).lower(), "| 'distint':", "distint" in json.dumps(reg, ensure_ascii=False).lower())
print("validacao 'distint':", [l.strip() for l in open(os.path.join(base,"VALIDACAO_K04.json"), encoding="utf-8") if "distint" in l])
