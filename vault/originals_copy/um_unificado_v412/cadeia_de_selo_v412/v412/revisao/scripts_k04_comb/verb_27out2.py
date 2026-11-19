import hashlib, os
p = r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_27out_e_isso_prossiga_pre_registro_ja_fizemos_verbatim.txt"
b = open(p, "rb").read()
print(len(b), hashlib.sha256(b).hexdigest()[:16])
print(b.decode("utf-8", "replace"))
