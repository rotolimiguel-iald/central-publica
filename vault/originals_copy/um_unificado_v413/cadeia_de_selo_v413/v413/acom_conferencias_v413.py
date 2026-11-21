# -*- coding: utf-8 -*-
# [DERIVADO v413, claude-construtor-v413] do molde v412\acom_conferencias_v412.py (que fica intacto): a v413 NAO muda a secao do selo pela propria tecnologia; reexporta, por caminho, as conferencias da v412 (que reexportam as da v411).
"""acom_conferencias_v413.py -- as CONFERENCIAS da cadeia sobre a SECAO do selo pela propria tecnologia (esboco_da_bancada, regexes_da_bancada, conferir_alfa_unico, conferir_secao, extrair_bloco, bloco_das_fontes,
nomes_de_nivel_de_modulo, literais_de_beta, proveniencia). A v413 nao muda essa secao: este modulo apenas REEXPORTA, por caminho, as da v412. Nada daqui e' digitado de memoria."""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
V412 = os.path.join(os.path.dirname(HERE), "v412")
_spec = importlib.util.spec_from_file_location("acom_conferencias_v412", os.path.join(V412, "acom_conferencias_v412.py"))
A0 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(A0)
globals().update({k: v for k, v in vars(A0).items() if not k.startswith("__")})
