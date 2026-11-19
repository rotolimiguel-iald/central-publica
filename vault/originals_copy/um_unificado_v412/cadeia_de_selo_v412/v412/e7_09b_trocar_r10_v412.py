"""R10: o contrato vigente passou a R10 (pagina R24). Troca, nos MEUS scripts de derivacao, as referencias R8/R22 por R10/R24 (texto exato, com contagem; backup de bytes), e gera e7_00c_conferir_r10_v412.py a partir de e7_00b_conferir_r8_v412.py
(mesmas checagens, com os sha16 do R10 e da R24). Nao toca fonte congelada nem arquivo da gerencia."""
import datetime, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
D = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
TROCAS = [("REV22", "REV24"), ("R22", "R24"), ("r22", "r24"), ("R8", "R10"), ("REV8", "REV10")]
ALVOS = ["e7_lib_v412.py", "e7_deriv_v412.py", "e7_02_derivar_kernel_v412.py", "e7_04_derivar_texto_v412.py", "e7_05_derivar_gerador_v412.py", "e7_06_derivar_ensaio_v412.py", "e7_07_derivar_fecho_v412.py"]
for nome in ALVOS:
    p = D / nome; b = p.read_bytes(); t = b.decode("utf-8"); nt = t; cs = []
    for v, n in TROCAS:
        cs.append((v, nt.count(v))); nt = nt.replace(v, n)
    print("%-32s %s" % (nome, cs))
    if nt != t:
        bk = Path(str(p) + ".bak_" + TS); bk.write_bytes(b); assert bk.read_bytes() == b
        tmp = Path(str(p) + ".tmp"); tmp.write_bytes(nt.encode("utf-8")); assert tmp.stat().st_size == len(nt.encode("utf-8")); tmp.replace(p); compile(nt, nome, "exec")
t = (D / "e7_00b_conferir_r8_v412.py").read_bytes().decode("utf-8")
for v, n in [("f9d68ee5a1529186", "c1305cad6036468b"), ("92edc64b5038f4eb", "4869b970c17eacf4"), ("REV22", "REV24"), ("R22", "R24"), ("REV8", "REV10"), ("R8", "R10"), ("contrato_r8", "contrato_r10"), ("0b_", "0c_"), ("passou a R10 (pagina R24", "passou a R10 (pagina R24"),
             ("e7_22_en_r22_v412.py", "e7_22b_en_r24_v412.py"), ("da R21 para a R24", "da R22 para a R24"), ("e7_04, e7_05, e7_06, e7_07, depois da build do kernel e7_02", "e7_04, e7_05, e7_06, e7_07, depois da build do kernel e7_02")]:
    t = t.replace(v, n)
(D / "e7_00c_conferir_r10_v412.py").write_bytes(t.encode("utf-8")); compile(t, "e7_00c", "exec")
print("e7_00c gerado")
