import hashlib, os
os.chdir(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi")
alvos = [
 "M2_DESFECHOS_E_SEGUNDA_TESTEMUNHA_K04.md",
 "ERRATA_M2_K09.md",
 "ERRATA_M2_K09_15nov.md",
 "ERRATA_NEUTRINO_V412_DADOS_K09.json",
 "ENTREGA_K09.md",
 "ERRATA_RESIDUOS_EIXOS_K01_K04.md",
 "ERRATA_K10_M2.md",
 "K04/M2/K09/scripts/validar_k09.py",
 "K04/M2/K09/scripts/fechar_auditoria_k09.py",
 "K04/M2/K09/medidas/validacao_estatica_k09.json",
 "K04/M2/K09/medidas/validacao_estatica_k09_stdout.txt",
]
print("=== ARQUIVOS MODIFICADOS/CRIADOS (K10) ===")
for a in alvos:
    b = open(a, "rb").read()
    print(f"{hashlib.sha256(b).hexdigest()}  {len(b):>7}  {a}")
print()
print("=== BACKUPS REV4 (preservados, pre-K10) ===")
for raiz, _, fs in os.walk("K04/M2/REV4"):
    for f in sorted(fs):
        p = os.path.join(raiz, f)
        b = open(p, "rb").read()
        print(f"{hashlib.sha256(b).hexdigest()}  {len(b):>7}  {p}")
