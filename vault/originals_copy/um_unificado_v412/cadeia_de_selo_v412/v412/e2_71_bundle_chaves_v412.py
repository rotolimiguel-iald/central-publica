import json, sys
sys.stdout.reconfigure(encoding="utf-8")
D = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412"
b = json.load(open(D + r"\BUNDLE_v412.json", encoding="utf-8"))
print("BUNDLE chaves:", list(b.keys()))
print({k: (v if not isinstance(v, (list, dict)) else type(v).__name__ + str(len(v))) for k, v in b.items()})
m0 = b["modulos"][0]
print("modulo[0]:", {k: (str(v)[:80]) for k, v in m0.items()})
print("root_suffix:", repr(b.get("root_suffix"))[:300])
bl = json.load(open(D + r"\kernel_modulos_novos_v412.json", encoding="utf-8"))
print("kernel_modulos_novos chaves:", list(bl.keys()), bl["n"], bl["novos"][:2])
f = json.load(open(D + r"\kernel\FLAGS_v412.json", encoding="utf-8"))
print("prefixos[0..2]:", list(f["prefixos"].items())[:3])
print("escada:", f["escada"], "n_flags", f["n_flags"], "por_origem sample", list(f["por_origem"].items())[:2])
pb = json.load(open(D + r"\kernel\POS_BUILD_v412.json", encoding="utf-8"))
print("POS_BUILD chaves:", list(pb.keys())[:40])
kr = json.load(open(D + r"\kernel\KERNEL_RECIBO_v412.json", encoding="utf-8"))
print("KERNEL_RECIBO chaves:", list(kr.keys())[:30])
