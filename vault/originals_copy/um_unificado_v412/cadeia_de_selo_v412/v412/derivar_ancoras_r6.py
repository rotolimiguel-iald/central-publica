# -*- coding: utf-8 -*-
"""Gerencia c1, 17/11/2026: deriva o script das ancoras propostas da sexta lista (42 modulos) por trocas exatas sobre o da quinta.
Grava ancoras_propostas_v412_r6.py; nao toca no anterior. Uso: derivar_ancoras_r6.py [--executar]"""
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
t = (V / "ancoras_propostas_v412_r5.py").read_text(encoding="utf-8")
for a, b, n in [
    ('(V / "insumos" / "MANIFESTO_PEDRAS_v412_R5.json")', '(V / "insumos" / "MANIFESTO_PEDRAS_v412_R6.json")', 2),
    ('(V / "insumos" / "pedras_r5" / (nome + ".lean"))', '(V / "insumos" / "pedras_r6" / (nome + ".lean"))', 1),
    ('out = V / "insumos" / "ANCORAS_PROPOSTAS_v412_R5.json"', 'out = V / "insumos" / "ANCORAS_PROPOSTAS_v412_R6.json"', 1),
]:
    assert t.count(a) == n, (t.count(a), n, a[:60])
    t = t.replace(a, b)
alvo = V / "ancoras_propostas_v412_r6.py"
print(alvo.name, len(t.encode("utf-8")), "B")
if "--executar" in sys.argv:
    assert not alvo.exists(); alvo.write_bytes(t.encode("utf-8")); print("gravado")
