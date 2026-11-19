# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: so' leitura. A matriz da U3 da ordem 031, linha a linha (afirmacao, modulo, termos, parecer), e os
campos frase_proposta, adicoes_ao_quadro e lotes_fechados_depois_da_ordem."""
import json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
u = json.loads(Path(r"C:\IALD\TUNEL_CLAUDE_APP\RESULTADOS\031_RESULTADO.json").read_bytes())["U3"]
for m in u["matriz"]:
    print("%2s | %s | %s | %s" % (m["linha_tabela"], m["modulo"], json.dumps(m["termos"], ensure_ascii=False)[:160], m["afirmacao_examinada"][:70]))
    print("     PARECER:", m["parecer"])
print("== frase_proposta:", u["frase_proposta"]); print("== adicoes_ao_quadro:", u["adicoes_ao_quadro"])
print("== projecao_geral:", json.dumps(u["projecao_geral"], ensure_ascii=False))
print("== lotes:", json.dumps(u["lotes_fechados_depois_da_ordem"], ensure_ascii=False, indent=1))
