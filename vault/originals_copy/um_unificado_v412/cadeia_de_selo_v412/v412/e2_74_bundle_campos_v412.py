import json, sys
sys.stdout.reconfigure(encoding="utf-8")
b = json.load(open(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\BUNDLE_v412.json", encoding="utf-8"))
print(sorted(b["modulos"][0].keys()))
print({k: str(v)[:70] for k, v in b["modulos"][0].items() if k.startswith("sha") or k in ("bytes", "print_axioms_removidos")})
