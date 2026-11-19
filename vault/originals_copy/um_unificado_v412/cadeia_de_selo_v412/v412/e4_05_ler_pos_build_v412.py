import json, sys
sys.stdout.reconfigure(encoding="utf-8")
D = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412"
f0 = json.load(open(D + r"\kernel\FLAGS_v412.json", encoding="utf-8"))
p = json.load(open(D + r"\kernel\POS_BUILD_v412.json", encoding="utf-8"))
print("ok:", p["ok"], "| criterios:", p.get("criterios"))
for k in ("n_flags", "n_decl_audit", "escada", "E411", "linha_TOTAL", "linha_TOTAL_v411", "delta_vs_v411", "todos_os_modulos_a_frio", "aviso_conhecido_TowerWedgeIndex", "pedras_sem_declaracao", "n_declaracoes_no_recibo"):
    print(k, "=", str(p.get(k))[:200])
print("chaves_antigas:", str(p.get("chaves_antigas"))[:200])
print("avisos fora o conhecido:", {m: v["n"] for m, v in p["avisos_por_modulo"].items() if v["n"] and m != "TGLExt.TowerWedgeIndex"})
print("n_por_modulo Token2/AMaquina:", f0["n_por_modulo"].get("TGLExt.Token2"), f0["n_por_modulo"].get("TGLExt.AMaquina"), "| n modulos:", len(f0["n_por_modulo"]))
print("falhas:", p.get("falhas"), p.get("falhas_informativas"))
print("modo dos modulos (Built):", [m for m, v in p["modo_dos_modulos_no_build"].items() if v == "Built"])
print("sinais com Built exigidos:", [s["checagem"][:150] + " -> " + str(s["detalhe"])[:100] for s in p["sinais"] if "tinha de compilar" in s["checagem"]])
f = json.load(open(D + r"\kernel\FLAGS_v412.json", encoding="utf-8"))
print("flags:", f["n_flags"], f["escada"])
