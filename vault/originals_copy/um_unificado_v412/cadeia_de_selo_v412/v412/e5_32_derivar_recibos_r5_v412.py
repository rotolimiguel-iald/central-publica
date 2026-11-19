"""R5: deriva e5_40_recibos_v412.py (a travessia sobre todas as superficies de texto novo, os blocos, os marcadores herdados) e e5_60_registros_v412.py (o recibo dos cinco registros) dos scripts do R4, que ficam intactos."""
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
from e5_deriv_v412 import derivar
EU = "e5_32_derivar_recibos_r5_v412.py"
derivar("e4_40_recibos_v412.py", "e5_40_recibos_v412.py", [
    ('"""R4: os recibos do texto novo da v412: a travessia sobre TODAS as superficies (os quatro registros,', '"""R5: os recibos do texto novo da v412: a travessia sobre TODAS as superficies (os cinco registros,', 1),
    ("uso: C:\\\\Python314\\\\python.exe -B -X utf8 e4_40_recibos_v412.py [--contagem N]", "uso: C:\\\\Python314\\\\python.exe -B -X utf8 e5_40_recibos_v412.py [--contagem N]", 1),
    ("from e2_lib_v412 import D, salvar_json, sha16_arq, Exame, ler_json", "from e5_lib_v412 import D, salvar_json, sha16_arq, Exame, ler_json", 1),
    ('"regra": "contrato R4, secao 5.1: um ponto de chamada', '"regra": "contrato R5, secao 5.1 (a do R4, sem mudanca): um ponto de chamada', 1),
    ('"pagina": {"arquivo": "o_que_fica_claro_REV13/O_QUE_FICA_CLARO_v412_R13.md", "sha16": sha16_arq(D / "o_que_fica_claro_REV13" / "O_QUE_FICA_CLARO_v412_R13.md"), "traducao_en_sha16": sha16_arq(D / "O_QUE_FICA_CLARO_v412_R13_EN.md")},',
     '"pagina": {"arquivo": "o_que_fica_claro_REV18/O_QUE_FICA_CLARO_v412_R18.md", "sha16": sha16_arq(D / "o_que_fica_claro_REV18" / "O_QUE_FICA_CLARO_v412_R18.md"), "traducao_en": "O_QUE_FICA_CLARO_v412_R18_EN.md", "traducao_en_sha16": sha16_arq(D / "O_QUE_FICA_CLARO_v412_R18_EN.md")},', 1),
    ("montados da pagina R13; os 34 marcadores herdados nao estao aqui", "montados da pagina R18; os 34 marcadores herdados nao estao aqui", 1),
    ('       "f43": {"formas": f43.pattern, "achados": achou43}, "historia": {"autoteste": {"n": auto["n"], "n_ok": auto["n_ok"]}, "n_unidades": hist["n_unidades_examinadas"],',
     '       "f43": {"formas": f43.pattern, "achados": achou43}, "historia": {"verificador": "verificar_historia_texto_v412_r5.py", "identificadores_do_kernel_fora_da_prosa": hist["n_identificadores_do_kernel_fora_da_prosa"], "autoteste": {"n": auto["n"], "n_ok": auto["n_ok"]}, "n_unidades": hist["n_unidades_examinadas"],', 1),
    ('salvar_json(D / "GUARDA_v412_UNIDADES.json", out, backup=False)', 'salvar_json(D / "GUARDA_v412_UNIDADES.json", out, backup=True)', 1),
    ('salvar_json(D / "BLOCOS_TEXTO_PUBLICO_v412.json", backup=False,', 'salvar_json(D / "BLOCOS_TEXTO_PUBLICO_v412.json", backup=True,', 1),
], EU)
derivar("e4_60_registros_v412.py", "e5_60_registros_v412.py", [
    ('"""R4: confere os quatro registros: veredito igual ao do contrato R4 (copiado por script);', '"""R5: confere os cinco registros: veredito igual ao do contrato R5 (copiado por script);', 1),
    ("from e2_lib_v412 import D, salvar_json, sha16_arq, estado_bloco, Exame", "from e5_lib_v412 import D, salvar_json, sha16_arq, estado_bloco, Exame", 1),
    ("a palavra de veredito e' exatamente a do contrato R4 (copiada por script)", "a palavra de veredito e' exatamente a do contrato R5 (copiada por script)", 1),
    ('"contrato_seguido": {"arquivo": "CONTRATO_v412_R4.md", "sha16": sha16_arq(D / "CONTRATO_v412_R4.md")}', '"contrato_seguido": {"arquivo": "CONTRATO_v412_R5.md", "sha16": sha16_arq(D / "CONTRATO_v412_R5.md")}', 1),
    ('"p18": len(v_p18), "historia_achados": hist["n_achados"], "historia_unidades": hist["n_unidades_examinadas"]}',
     '"p18": len(v_p18), "historia_achados": hist["n_achados"], "historia_unidades": hist["n_unidades_examinadas"], "historia_identificadores_do_kernel_fora_da_prosa": hist["n_identificadores_do_kernel_fora_da_prosa"], "n_nao_diz": len(s["nao_diz"]), "usa_p_igual_np": "P = nP" in json.dumps(corpo, ensure_ascii=False)}', 1),
    ('out = {"contrato": "REGISTROS_v412_RECIBO", "ok": ex.ok,',
     'ex.chk("o registro leitor_da_formula_v412 nao usa a expressao P = nP (contrato R5, secao 2)", "leitor_da_formula_v412" in rec and rec["leitor_da_formula_v412"]["usa_p_igual_np"] is False, 1)\n'
     'ex.chk("sao cinco registros, na ordem do contrato, e cunhagens_v412 cobra o selo dos outros quatro por ids sem forma de numero de revisao", [s["nome"] for s in specs] == RG.NOMES and len(specs) == 5 and sorted(c["id"] for c in specs[-1]["checks"] if c["id"].startswith("selo_")) == sorted(RG.ID_DO_SELO.values()), len(specs), [c["id"] for c in specs[-1]["checks"] if c["id"].startswith("selo_")])\n'
     'out = {"contrato": "REGISTROS_v412_RECIBO", "ok": ex.ok,', 1),
], EU)
