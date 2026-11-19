"""R5: deriva as copias _r5 dos modulos do texto publico e da guarda (a pagina passa a R18): texto_publico_v412_r5.py (mais tres caracteres que a pagina R18 traz: o expoente dois, menor-ou-igual e maior-ou-igual),
blocos_texto_publico_v412_r5.py, guarda_frases_v412_r5.py (os controles sobre a pagina R18; a fonte da guarda, runtime_v412_guarda.py, NAO muda: a secao 5 do contrato e' a do R4) e e5_23_texto_publico_gerar_v412.py."""
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
from e5_deriv_v412 import derivar
EU = "e5_22_derivar_texto_r5_v412.py"
R13R18 = [('"o_que_fica_claro_REV13" / "O_QUE_FICA_CLARO_v412_R13.md"', '"o_que_fica_claro_REV18" / "O_QUE_FICA_CLARO_v412_R18.md"', 1), ('"O_QUE_FICA_CLARO_v412_R13_EN.md"', '"O_QUE_FICA_CLARO_v412_R18_EN.md"', 1)]
derivar("texto_publico_v412.py", "texto_publico_v412_r5.py", [
    ('SUB_SUP = {"₁": "_1", "ⁿ": "^n", "ˢ": "^s"}', 'SUB_SUP = {"₁": "_1", "ⁿ": "^n", "ˢ": "^s", "²": "^2"}', 1),
    ('t = t.replace("−", "$-$").replace("★", r"$\\star$").replace("≠", r"$\\neq$")', 't = t.replace("−", "$-$").replace("★", r"$\\star$").replace("≠", r"$\\neq$").replace("≤", r"$\\leq$").replace("≥", r"$\\geq$")', 2),
    ('                assert len(r) == 3, ("a tabela da pagina tem 3 colunas", r)', '                assert len(r) == 3, ("a tabela da pagina tem 3 colunas", r)\n                assert not any(" --- " in c for c in r), ("celula com o separador da linha de tabela", r)', 1),
], EU)
derivar("blocos_texto_publico_v412.py", "blocos_texto_publico_v412_r5.py", R13R18 + [("contrato R4 secao 6) monta, da pagina publica R13 (PT)", "contrato R5 secao 6) monta, da pagina publica R18 (PT)", 1)], EU)
derivar("guarda_frases_v412.py", "guarda_frases_v412_r5.py", [
    ("from e2_lib_v412 import D, salvar_json, sha16_arq", "from e5_lib_v412 import D, salvar_json, sha16_arq", 1),
    ('(D / "o_que_fica_claro_REV13" / "O_QUE_FICA_CLARO_v412_R13.md").read_bytes()', '(D / "o_que_fica_claro_REV18" / "O_QUE_FICA_CLARO_v412_R18.md").read_bytes()', 1),
    ('(D / "O_QUE_FICA_CLARO_v412_R13_EN.md").read_bytes()', '(D / "O_QUE_FICA_CLARO_v412_R18_EN.md").read_bytes()', 1),
    ('"o titulo da secao 2 da pagina R13 passa"', '"o titulo da secao 2 da pagina R18 passa"', 1),
    ('"regra": "contrato R4, secao 5.3: 21 controles obrigatorios', '"regra": "contrato R5, secao 5.3 (a do R4, sem mudanca): 21 controles obrigatorios', 1),
    ('"pagina": {"arquivo": "o_que_fica_claro_REV13/O_QUE_FICA_CLARO_v412_R13.md", "sha16": sha16_arq(D / "o_que_fica_claro_REV13" / "O_QUE_FICA_CLARO_v412_R13.md")}',
     '"pagina": {"arquivo": "o_que_fica_claro_REV18/O_QUE_FICA_CLARO_v412_R18.md", "sha16": sha16_arq(D / "o_que_fica_claro_REV18" / "O_QUE_FICA_CLARO_v412_R18.md"), "traducao_en_sha16": sha16_arq(D / "O_QUE_FICA_CLARO_v412_R18_EN.md")}', 1),
    ("(contrato R4, secao 5) a GUARDA DE FRASES da cadeia da v412", "(contrato R5, secao 5, que e' a do R4) a GUARDA DE FRASES da cadeia da v412", 1),
], EU)
derivar("e4_21_texto_publico_gerar_v412.py", "e5_23_texto_publico_gerar_v412.py", R13R18 + [
    ("from e2_lib_v412 import D, salvar_json, sha16_arq, estado_bloco", "from e5_lib_v412 import D, salvar_json, sha16_arq, estado_bloco", 1),
    ("import texto_publico_v412 as TP", "import texto_publico_v412_r5 as TP", 1),
    ('assert sha16_arq(PT_ARQ) == "256a71e1bdf03239", "a pagina R13 nao e\' a do contrato"', 'import re as _re5\n_m5 = _re5.search(r"o_que_fica_claro_REV18\\\\O_QUE_FICA_CLARO_v412_R18\\.md` \\(sha16 `([0-9a-f]{16})`; (\\d+) bytes\\)", (D / "CONTRATO_v412_R5.md").read_bytes().decode("utf-8"))\nassert _m5 and sha16_arq(PT_ARQ) == _m5.group(1) and PT_ARQ.stat().st_size == int(_m5.group(2)), "a pagina R18 nao e\' a do contrato R5"', 1),
    ('"arquivo": "o_que_fica_claro_REV13/O_QUE_FICA_CLARO_v412_R13.md"', '"arquivo": "o_que_fica_claro_REV18/O_QUE_FICA_CLARO_v412_R18.md"', 1),
    ('estado_bloco("5a_texto_publico_c4", rec["ok"], {"texto_publico": saida, "traducao_en": EN_ARQ, "conversor": D / "texto_publico_v412.py", "pdflatex": D / "TEXTO_PUBLICO_PDFLATEX_v412.json"},',
     'estado_bloco("4a_texto_publico_r18", rec["ok"], {"texto_publico": saida, "traducao_en": EN_ARQ, "conversor": D / "texto_publico_v412_r5.py", "pdflatex": D / "TEXTO_PUBLICO_PDFLATEX_v412.json", "tradutor": D / "e5_21_en_r18_v412.py"},', 1),
    ('nota="secao do artigo PT/EN em TeX montada da pagina R13; EN traducao fiel (mesma estrutura, mesmos termos); pdflatex isolado", proximo="guarda de frases (bloco 4); depois registros e gerador")',
     'nota="secao do artigo PT/EN em TeX montada da pagina R18 (o bloco novo do leitor da formula com a tabela de 30 linhas); EN traducao fiel (mesma estrutura, mesmos termos entre crases na mesma ordem, mesmos numeros); pdflatex isolado", proximo="controles da guarda sobre a R18; registros; gerador")', 1),
], EU, imports=False)
