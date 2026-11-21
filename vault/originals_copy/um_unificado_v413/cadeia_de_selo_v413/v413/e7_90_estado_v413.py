# -*- coding: utf-8 -*-
"""Etapa 2 da v413: grava no ETAPA_2_ESTADO_v413.json o bloco pedido na linha de comando (por temporario e troca, guardando o anterior com .bak_<data>), com os arquivos e os sha16 LIDOS deles.
uso: e7_90_estado_v413.py <bloco> <feito 0|1> <proximo comando> [rotulo=caminho ...] [--nota "..."]"""
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import e7_lib_v413 as L

a = sys.argv[1:]
nota = ""
if "--nota" in a:
    i = a.index("--nota"); nota = a[i + 1]; a = a[:i] + a[i + 2:]
bloco, feito, proximo = a[0], a[1] == "1", a[2]
arquivos = {}
for x in a[3:]:
    k, v = x.split("=", 1)
    arquivos[k] = Path(v) if Path(v).is_absolute() else L.D / v
L.estado_bloco(bloco, feito, arquivos, nota=nota, proximo=proximo)
print("estado gravado:", bloco, feito, "| arquivos:", len(arquivos), "| sha16 do estado:", L.sha16_arq(L.ESTADO))
