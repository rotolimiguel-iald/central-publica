import json, io, collections, re
p = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\CANAIS_K01.json"
d = json.load(io.open(p, encoding="utf-8"))
print("n canais:", len(d["canais"]))
cnt = collections.Counter()
for c in d["canais"]:
    for r, t in c["sete_ressalvas"].items():
        cnt[t] += 1
rep = [(n, t[:140]) for t, n in cnt.items() if n > 1]
print("textos de ressalva repetidos em >1 canal:", len(rep))
for n, t in sorted(rep, reverse=True)[:15]:
    print(" ", n, t)
print()
print("tipos de negativo:", collections.Counter(c["consequencia_negativo"]["tipo"] for c in d["canais"]))
print("classificacao:", collections.Counter(c["classificacao"] for c in d["canais"]))
print("cumpre_hoje:", collections.Counter(str(c["estado_triplo"]["cumpre_hoje"]) for c in d["canais"]))
print()
# D numericos
for c in d["canais"]:
    pd = c["poder_desenho"]
    print(f'{c["id"]:42s} D={pd.get("D")}  aval={str(pd.get("avaliacao"))[:70]}')
# vazios: unilateral?
for c in d["canais"]:
    if c["id"].startswith("vazios"):
        s = json.dumps(c, ensure_ascii=False)
        print(c["id"], "unilateral" in s, "bilateral" in s)
# ressalvas glossario
print(json.dumps(d["ressalvas_glossario"], ensure_ascii=False, indent=1)[:1800])
