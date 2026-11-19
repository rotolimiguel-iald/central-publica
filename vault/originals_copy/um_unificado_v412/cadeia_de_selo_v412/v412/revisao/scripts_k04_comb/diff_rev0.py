import difflib, hashlib, os
base = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi"
pairs = [
 (base + r"\K04\COMBINACAO\REV0\COMBINACAO_K04.md", base + r"\COMBINACAO_K04.md"),
 (base + r"\K04\COMBINACAO\REV0\NOTAS_C_FONTES_E_DESENHO.md", base + r"\K04\COMBINACAO\NOTAS_C_FONTES_E_DESENHO.md"),
 (base + r"\K04\COMBINACAO\REV0\NOTAS_D_E_MAPA_E_PINOS.md", base + r"\K04\COMBINACAO\NOTAS_D_E_MAPA_E_PINOS.md"),
 (base + r"\K04\COMBINACAO\REV0\RESSALVAS_UMA_A_UMA_K04.md", base + r"\RESSALVAS_UMA_A_UMA_K04.md"),
]
for a, b in pairs:
    A = open(a, "rb").read().decode("utf-8").splitlines()
    B = open(b, "rb").read().decode("utf-8").splitlines()
    print("=====", os.path.basename(a), "REV0 bytes", os.path.getsize(a), "atual", os.path.getsize(b))
    for l in difflib.unified_diff(A, B, "REV0", "atual", lineterm="", n=0):
        print(l[:400])
