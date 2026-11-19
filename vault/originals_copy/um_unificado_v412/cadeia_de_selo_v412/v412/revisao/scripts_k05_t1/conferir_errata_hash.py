# Revisor K05/T1: confere por script os hashes declarados na ERRATA_T1_R2.md e lista o diff REV0 -> corrigido.
import hashlib, difflib, sys, io
K = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi"
arqs = {
 "REV0": K + r"\K05\T1\REV0\T1_FECHADO.md",
 "ATUAL": K + r"\T1_FECHADO.md",
 "ERRATA": K + r"\ERRATA_T1_R2.md",
 "LEAN_candidata": K + r"\K05\candidatas\T1_R2.lean",
 "LEAN_sandbox_kimi": K + r"\K05\sandbox_t1\sources\T1_R2.lean",
}
decl = {"REV0": "c8c810ba69647498a868c624506fad89b32eb1a9120c43d3bc53e321efa2b604",
        "ATUAL": "b74d8c421e9137114a7fe231fceb3e4cc41e02d3adf68ccc18c2d901fc2b2f9e"}
dados = {}
for k, p in arqs.items():
    b = open(p, "rb").read()
    dados[k] = b
    h = hashlib.sha256(b).hexdigest()
    ok = ""
    if k in decl:
        ok = "  DECLARADO=" + decl[k] + ("  CONFERE" if h == decl[k] else "  NAO CONFERE")
    print(f"{k}: {len(b)} bytes sha256={h}{ok}")
a = dados["REV0"].decode("utf-8").splitlines()
b = dados["ATUAL"].decode("utf-8").splitlines()
print("\n--- diff REV0 -> ATUAL (unified, 0 linhas de contexto) ---")
for l in difflib.unified_diff(a, b, "REV0", "ATUAL", n=0, lineterm=""):
    print(l[:400])
