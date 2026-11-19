"""R8: o contrato vigente passou a R8 (pagina R22). Troca, nos scripts de derivacao e_7 (meus), as referencias R7/R21 por R8/R22, por texto exato com contagem; backup de bytes antes de tocar. Nao toca fonte congelada nem arquivo da gerencia."""
import datetime, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
D = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
COMUM = [('("contrato R5", "contrato R7", 0)', '("contrato R5", "contrato R8", 0)'), ('("pagina R18", "pagina R21", 0)', '("pagina R18", "pagina R22", 0)'), ('("texto_publico_r18", "texto_publico_r21", 0)', '("texto_publico_r18", "texto_publico_r22", 0)')]
PLANO = {
    "e7_deriv_v412.py": [('("CONTRATO_v412_R5", "CONTRATO_v412_R7")', '("CONTRATO_v412_R5", "CONTRATO_v412_R8")'), ('("O_QUE_FICA_CLARO_v412_R18_EN", "O_QUE_FICA_CLARO_v412_R21_EN")', '("O_QUE_FICA_CLARO_v412_R18_EN", "O_QUE_FICA_CLARO_v412_R22_EN")'),
                         ('("O_QUE_FICA_CLARO_v412_R18", "O_QUE_FICA_CLARO_v412_R21")', '("O_QUE_FICA_CLARO_v412_R18", "O_QUE_FICA_CLARO_v412_R22")'), ('("o_que_fica_claro_REV18", "o_que_fica_claro_REV21")', '("o_que_fica_claro_REV18", "o_que_fica_claro_REV22")'),
                         ('("INICIO_R5_v412", "INICIO_R7_v412")', '("INICIO_R5_v412", "INICIO_R8_v412")'), ("(contrato R7)] copia de", "(contrato R8)] copia de")],
    "e7_02_derivar_kernel_v412.py": COMUM + [('("(a pagina R18)", "(a pagina R21)", 0)', '("(a pagina R18)", "(a pagina R22)", 0)')],
    "e7_04_derivar_texto_v412.py": COMUM,
    "e7_05_derivar_gerador_v412.py": COMUM + [('("a pagina R9", "a pagina R21", 0)', '("a pagina R9", "a pagina R22", 0)')],
    "e7_06_derivar_ensaio_v412.py": COMUM,
    "e7_07_derivar_fecho_v412.py": COMUM + [('Exame("fecho_R7")', 'Exame("fecho_R8")'), ('"CANDIDATO REGERADO PELO CONTRATO R7 E ENSAIADO"', '"CANDIDATO REGERADO PELO CONTRATO R8 E ENSAIADO"'), ('"ETAPA 2 PELO R7 NAO FECHOU"', '"ETAPA 2 PELO R8 NAO FECHOU"'),
                                            ("(6) a pagina e' a R21 (sha16 lido do arquivo, pinado pelo contrato R7)", "(6) a pagina e' a R22 (sha16 lido do arquivo, pinado pelo contrato R8)"),
                                            ("a pagina R21 cita `a_trava_no_nome` (a fonte esta' em TraducaoTuring, kernel selado da v411, e nao em modulo da lista de 156): por isso nao e' ancora de nenhum registro desta versao;",
                                             "a pagina R22 cita `a_trava_no_nome` (em TraducaoTuring), `the_angle_is_prior` e `the_name_is_the_born_reading_of_the_post` (declaracoes do kernel selado da v411, nao de modulo da lista de 156): por isso nao sao ancora de nenhum registro desta versao;"),
                                            ("(inicio 18/11", "(inicio 18/11")],
}
for nome, trocas in PLANO.items():
    p = D / nome
    b = p.read_bytes()
    t = b.decode("utf-8")
    nt = t
    for velho, novo in trocas:
        c = nt.count(velho)
        print("%-34s %-70s ocorrencias %d" % (nome, velho[:70], c))
        nt = nt.replace(velho, novo)
    if nt != t:
        bk = Path(str(p) + ".bak_" + TS); bk.write_bytes(b); assert bk.read_bytes() == b
        tmp = Path(str(p) + ".tmp"); tmp.write_bytes(nt.encode("utf-8")); assert tmp.stat().st_size == len(nt.encode("utf-8")); tmp.replace(p)
        compile(nt, nome, "exec")
