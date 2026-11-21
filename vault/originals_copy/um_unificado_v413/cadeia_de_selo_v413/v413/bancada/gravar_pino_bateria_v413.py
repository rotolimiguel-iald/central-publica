# -*- coding: utf-8 -*-
# [AUTORAL v413, 20/11/2026, construtor do B(n) da v413, agente da gerencia c1] o pino ao lado da bateria da v413 (o que o bn_v412.sh gravava com `python -c`; os runners da v413 nao usam `python -c`).
"""gravar_pino_bateria_v413.py -- grava, NOVO, o pino ao lado da bateria gerada pelo bn_v413.sh: {bateria: {path, sha256}, pino_um_py: {path, sha256}, nota}; os sha256 sao LIDOS dos arquivos.
uso: python -I -B -X utf8 gravar_pino_bateria_v413.py <BATERIA_VINCULO_v413.json> <PINO_UM_PY_v413.json> <PINOS_BATERIA_v413.json (novo)>"""
import os
import sys

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import util_bn_v413 as U  # noqa: E402

if len(sys.argv) != 4:
    raise SystemExit(__doc__)
bat, pum, saida = (os.path.abspath(x_) for x_ in sys.argv[1:4])
assert os.path.isfile(bat) and os.path.isfile(pum), (bat, pum)
U.gravar_json_novo(saida, {"bateria": {"path": bat, "sha256": U.sha256_arquivo(bat)}, "pino_um_py": {"path": pum, "sha256": U.sha256_arquivo(pum)},
                           "nota": "pino ao lado da bateria da v413, gravado quando o bn_v413.sh a gerou (gerador do pino gerador_bateria de PINOS_BN_v413.json; esboco R3.6)"})
print(saida, U.sha256_arquivo(saida))
