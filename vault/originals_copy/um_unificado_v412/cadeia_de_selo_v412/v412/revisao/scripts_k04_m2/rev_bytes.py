import hashlib, re, json, sys
def sha(p):
    return hashlib.sha256(open(p,"rb").read()).hexdigest()
core = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json"
print("core sha256", sha(core))
selo = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_selo.json"
print("selo sha256", sha(selo))
# determinacoes
p = r"C:\IALD\Central de Patentes\work\neutrino_E0_autonomia_30out\determinacoes_m2_30out.json"
t = open(p, encoding="utf-8").read()
for s in ['"z_sigma": 1.9379969609289271', '"exposicao_adicional_dias": 380.07855357458413']:
    print(repr(s), s in t)
print("determinacoes sha256", sha(p))
# PRE_REGISTRO l.36
p2 = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\PRE_REGISTRO_CEGO_RASCUNHO_K01.md"
L = open(p2, encoding="utf-8").read().splitlines()
print("PRE l.36:", L[35][:300])
print("contém 'propagação σ_m₂ ≈ σ(Δm²₂₁)/(2m₂)':", "propagação σ_m₂ ≈ σ(Δm²₂₁)/(2m₂)" in L[35])
# DEPOSITO / ENTREGA hashes citados
base = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi"
for f, claimed in (("ENTREGA_K04.md","a744eca8bb6ff589a6be3187690742e06c8cb374c8d820a3204d96d2b7ba0ba2"),("REGISTRO_MAPA_K04.json","faeda571b777e0191509258ca5db0aabe6847f2d1fe58c395e8a14be1d4f8971"),("VALIDACAO_K04.json","5e728a295f99602a466f91ac94a31913c047f62845e42bfdedaf0ab37333bce4")):
    try:
        h = sha(base + "\\" + f); print(f, h[:16], "== declarado?", h == claimed)
    except Exception as e: print(f, "ERRO", e)
# core: frozen hash recompute
d = json.load(open(core, encoding="utf-8"))
fz = d["core"]["neutrino_m2"]["frozen"]
for ks in ({"sort_keys":True},{"sort_keys":True,"ensure_ascii":False},{}):
    for sep in ((",", ":"), None):
        s = json.dumps(fz, separators=sep, **ks) if sep else json.dumps(fz, **ks)
        print(ks, sep, hashlib.sha256(s.encode("utf-8")).hexdigest()[:16])
print("core frozen_hash", d["core"]["neutrino_m2"]["frozen_hash"][:16])
# frases citadas do core
nm = d["core"]["neutrino_m2"]
for q in ("a tensao cresce com a precisao", "A linha de morte de 5 sigma esta dentro da meta de projeto do JUNO", "linha de morte dentro da meta de projeto", "a regra hasheada julga as proximas medidas", "a meta de 0,5"):
    in_theorem = q in nm["theorem"]; in_checks = any(q in c[0] for c in nm["checks"])
    print(repr(q), "theorem:", in_theorem, "checks:", in_checks)
