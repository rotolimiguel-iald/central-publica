import json, sys
sys.stdout.reconfigure(encoding="utf-8")
j = json.load(open(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\GUARDA_MATERIAL_PRIVADO_v412.json", encoding="utf-8"))
print("limpo:", j["limpo"], "| n arquivos:", j["n_arquivos"])
for a in j["arquivos"]:
    if a["ocorrencias"]:
        print("  ocorrencias (so' a contagem):", a["ocorrencias"], a["arquivo"].split("\\")[-1])
