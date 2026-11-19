import json, io, sys
p = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\CANAIS_K01.json"
d = json.load(io.open(p, encoding="utf-8"))
ids = sys.argv[1:]
for c in d["canais"]:
    if ids and c["id"] not in ids: continue
    print("=====", c["id"], "|", c["classificacao"], "|", json.dumps(c["estado_triplo"], ensure_ascii=False))
    print("PREV:", c["previsao"]["formula"][:300], "||", str(c["previsao"]["valor"])[:300])
    print("DADO.cal:", c["dado"]["calendario"][:500])
    print("CEG:", c["cegueira"]["possivel"], "|", c["cegueira"]["impedimento"][:300])
    print("PODER:", json.dumps(c["poder_desenho"], ensure_ascii=False)[:900])
    print("NEG:", json.dumps(c["consequencia_negativo"], ensure_ascii=False)[:500])
