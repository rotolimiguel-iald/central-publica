import importlib.util, json, sys, os, copy
RP = r"C:\IALD\MAPA_DE_ROTAS\rotas.py"
spec = importlib.util.spec_from_file_location("rotas_mod", RP)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
regs = m._parse(m._ler_bytes(m.LIVRO))
ids = {r["rota_id"] for r in regs if r["tipo"] == "ROTA"}
seqs = {r["seq"] for r in regs}
print("livro lido:", len(regs), "registros; rotas", len(ids))
alvos = {
 "K04": r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\REGISTRO_MAPA_K04.json",
 "K05_ref": r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\registro_mapa_k05_conferida_14nov.json",
}
docs = {}
for nome, p in alvos.items():
    b = open(p, "rb").read()
    d = json.loads(b.decode("utf-8"))
    docs[nome] = d
    print("=====", nome, len(b), "B")
    lst = d if isinstance(d, list) else [d]
    for reg in lst:
        print(" campos:", sorted(reg.keys()))
        print(" tipo", reg.get("tipo"), "| rota_id", reg.get("rota_id"), "| existe no Mapa?", reg.get("rota_id") in ids)
        txt = json.dumps(reg, ensure_ascii=False)
        print(" tem aspas « »?", ("«" in txt or "»" in txt), "| tem 'confirm' (qualquer caixa)?", "confirm" in txt.lower())
        for k, v in reg.items():
            if isinstance(v, str) and len(v) > 6000:
                print(" campo longo:", k, len(v))
        try:
            r2 = m._valida(copy.deepcopy(reg), ids, seqs)
            print(" _valida: OK")
        except Exception as e:
            print(" _valida: RECUSA ->", type(e).__name__, str(e)[:300])
