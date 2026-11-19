import os, re
base = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi"
files = ["M2_DESFECHOS_E_SEGUNDA_TESTEMUNHA_K04.md", "ERRATA_M2_K04_R2.md", "ERRATA_M2_K04_R3.md", r"K04\M2\medidas\tabelas_planejamento.md", r"K04\M2\medidas\resultados_planejamento.json"]
pats = [r"31[,.]4\d*", r"0[,.]314\d*", r"99[,.]8\d*", r"99[,.]4\d*", r"0[,.]998\d*", r"0[,.]994\d*", r"380[,.]0\d*", r"3[,.]4[78]\d*", r"12[,.]8\d*", r"0[,.]128\d*", r"64[,.]7\d*", r"66[,.]1\d*"]
for f in files:
    t = open(os.path.join(base, f), "rb").read().decode("utf-8")
    print("==", f)
    for p in pats:
        m = [x for x in re.findall(p, t)][:6]
        if m: print("   ", p, "->", m)
