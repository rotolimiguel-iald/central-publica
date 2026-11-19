"""R11: o contrato vigente passou a R11 (lista R12, pagina R25). Troca, nos MEUS scripts de derivacao, as referencias por texto exato com contagem (as especificas por arquivo, depois as comuns); backup de bytes antes de tocar.
Gera e7_00d_conferir_r11_v412.py a partir de e7_00c_conferir_r10_v412.py (mesmas checagens, com os sha16 do R11, da R25 e da lista R12). Nao toca fonte congelada nem arquivo da gerencia."""
import datetime, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
D = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def aplicar(nome, pares):
    p = D / nome; b = p.read_bytes(); t = b.decode("utf-8"); nt = t; cs = []
    for v, n in pares:
        cs.append((v[:36], nt.count(v))); nt = nt.replace(v, n)
    print("%-32s %s" % (nome, cs))
    if nt != t:
        bk = Path(str(p) + ".bak_" + TS); bk.write_bytes(b); assert bk.read_bytes() == b
        tmp = Path(str(p) + ".tmp"); tmp.write_bytes(nt.encode("utf-8")); assert tmp.stat().st_size == len(nt.encode("utf-8")); tmp.replace(p); compile(nt, nome, "exec")


aplicar("e7_lib_v412.py", [('"CONTRATO_v412_R10.md"', '"CONTRATO_v412_R11.md"'), ("MANIFESTO_PEDRAS_v412_R11.json", "MANIFESTO_PEDRAS_v412_R12.json"), ("ANCORAS_PROPOSTAS_v412_R11.json", "ANCORAS_PROPOSTAS_v412_R12.json"), ("REV24", "REV25"), ("R24", "R25"),
                           ('"pedras_r11"', '"pedras_r12"'), ("..._ADENDO_R10.md", "..._ADENDO_R10.md + ..._ADENDO_R11.md")])
aplicar("e7_deriv_v412.py", [('("CONTRATO_v412_R5", "CONTRATO_v412_R10")', '("CONTRATO_v412_R5", "CONTRATO_v412_R11")'), ("(contrato R10)] copia de", "(contrato R11)] copia de"), ('("MANIFESTO_PEDRAS_v412_R10", "MANIFESTO_PEDRAS_v412_R11")', '("MANIFESTO_PEDRAS_v412_R10", "MANIFESTO_PEDRAS_v412_R12")'),
                             ('("ANCORAS_PROPOSTAS_v412_R10", "ANCORAS_PROPOSTAS_v412_R11")', '("ANCORAS_PROPOSTAS_v412_R10", "ANCORAS_PROPOSTAS_v412_R12")'), ('("pedras_r10", "pedras_r11")', '("pedras_r10", "pedras_r12")'), ("R24", "R25"), ("REV24", "REV25"),
                             ('"INICIO_R10_v412"', '"INICIO_R11_v412"'), ('"conferir_undecima_lista_v412"', '"conferir_duodecima_lista_v412"')])
COMUM = [('"contrato R10"', '"contrato R11"'), ("CONTRATO R10", "CONTRATO R11"), ('"pagina R24"', '"pagina R25"'), ("(a pagina R24)", "(a pagina R25)"), ("texto_publico_r24", "texto_publico_r25"), ("UNDECIMA_LISTA_CONFERIDA_v412", "DUODECIMA_LISTA_CONFERIDA_v412"),
         ('("manifesto R10", "manifesto R11", 0)', '("manifesto R10", "manifesto R12", 0)'), ('("ancoras R10", "ancoras R11", 0)', '("ancoras R10", "ancoras R12", 0)'), ('("pedras_r10", "pedras_r11", 0)', '("pedras_r10", "pedras_r12", 0)'),
         ("DECIMA PRIMEIRA", "DECIMA SEGUNDA"), ("decima primeira", "decima segunda"), ("pelo R10 NAO", "pelo R11 NAO"), ("PELO R10 NAO", "PELO R11 NAO"), ('fecho_R10', 'fecho_R11')]
for nome in ("e7_02_derivar_kernel_v412.py", "e7_04_derivar_texto_v412.py", "e7_05_derivar_gerador_v412.py", "e7_06_derivar_ensaio_v412.py", "e7_07_derivar_fecho_v412.py"):
    extra = []
    if nome == "e7_04_derivar_texto_v412.py":
        extra = [("'\"lista\": \"decima (insumos/pedras_r11)\"', '\"lista\": \"undecima (insumos/pedras_r11)\"'", "'\"lista\": \"decima (insumos/pedras_r12)\"', '\"lista\": \"duodecima (insumos/pedras_r12)\"'")]
    if nome == "e7_07_derivar_fecho_v412.py":
        extra = [("MANIFESTO_PEDRAS_v412_R11", "MANIFESTO_PEDRAS_v412_R12"), ("undecima (insumos", "duodecima (insumos"), ("pinado pelo contrato R10", "pinado pelo contrato R11"), ("a pagina R24 cita", "a pagina R25 cita"), ("(6) a pagina e' a R24", "(6) a pagina e' a R25")]
    if nome == "e7_02_derivar_kernel_v412.py":
        extra = [('"conferir_undecima_lista_v412.py"', '"conferir_duodecima_lista_v412.py"')]
    aplicar(nome, extra + COMUM)
t = (D / "e7_00c_conferir_r10_v412.py").read_bytes().decode("utf-8")
for v, n in [("c1305cad6036468b", "30fe6e3d93e9bc15"), ("4869b970c17eacf4", "ce313a4c57dec103"), ("REV24", "REV25"), ("R24", "R25"), ("REV10", "REV11"), ("R10", "R11"), ("contrato_r10", "contrato_r11"), ("0c_", "0d_"), ("e7_22b_en_r24_v412.py", "e7_22c_en_r25_v412.py"),
             ("MANIFESTO_PEDRAS_v412_R11", "MANIFESTO_PEDRAS_v412_R12"), ("ANCORAS_PROPOSTAS_v412_R11", "ANCORAS_PROPOSTAS_v412_R12"), ("63b37d347da3c2c1", "1028adf7293b432f"), ("cd9155b05c9dbae6", "31af18a86183002f"), ("da R22 para a R25", "da R24 para a R25")]:
    t = t.replace(v, n)
(D / "e7_00d_conferir_r11_v412.py").write_bytes(t.encode("utf-8")); compile(t, "e7_00d", "exec")
print("e7_00d gerado")
