# Revisor K05/T1: sha256 por script dos arquivos examinados (nada digitado a mao).
import hashlib, os
R = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412"
lista = [
 R + r"\kimi\T1_FECHADO.md", R + r"\kimi\ERRATA_T1_R2.md", R + r"\kimi\K05\T1\REV0\T1_FECHADO.md",
 R + r"\kimi\K05\candidatas\T1_R2.lean", R + r"\kimi\K05\sandbox_t1\logs\T1_R2.log",
 R + r"\kimi\K05\sandbox_t1\refs\choi_1974.pdf", R + r"\kimi\K05\sandbox_t1\refs\andreou_2004.07169.txt",
 R + r"\kimi\ORDEM_K05_matematica_rodada_2.md", R + r"\revisao\REVISAO_K02.md",
 R + r"\revisao\scripts_k05_t1\build\T1_R2.revisor.log", R + r"\revisao\scripts_k05_t1\build\T1_R2.olean",
 r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\A Ponte Einstein Cartan Miguel.tex",
 r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\BisognanoWichmann.lean",
 r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\Ergodicity.lean",
 r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\PonteDaEscalaDual.lean",
]
for p in lista:
    b = open(p, "rb").read()
    print(f"{hashlib.sha256(b).hexdigest()[:16]}  {len(b):>9}  {p}")
