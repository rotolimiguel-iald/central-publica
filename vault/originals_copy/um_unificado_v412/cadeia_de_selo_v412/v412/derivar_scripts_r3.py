# -*- coding: utf-8 -*-
"""Gerencia c1, 17/11/2026: deriva, por trocas exatas sobre os scripts da segunda lista, os da terceira lista de pedras da v412
(40 modulos: os 39 da segunda, com as emendas da ordem 025, e a composicao OTestemunhoDeTakesakiEmCasa, que entrou pela regra do
operador sobre a torre). Grava manifesto_pedras_v412_r3.py e ancoras_propostas_v412_r3.py; nao toca nos anteriores.
Uso: derivar_scripts_r3.py [--executar]"""
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent


def trocar(t, pares):
    for a, b, n in pares:
        assert t.count(a) == n, (t.count(a), n, a[:70])
        t = t.replace(a, b)
    return t


man = trocar((V / "manifesto_pedras_v412_r2.py").read_text(encoding="utf-8"), [
    ('DEST = V / "insumos" / "pedras_r2"\n', 'DEST = V / "insumos" / "pedras_r3"\n', 1),
    ('out = V / "insumos" / "MANIFESTO_PEDRAS_v412_R2.json"', 'out = V / "insumos" / "MANIFESTO_PEDRAS_v412_R3.json"', 1),
    ('"R2 (REV44); aprovada com ressalvas na ordem 024; emenda na ordem 025"', '"R3 (REV51); emendas das ordens 024 e 025; conferencia na 026"', 1),
    ('"R1 (REV45); aprovada com ressalvas na ordem 024; emenda na ordem 025"', '"R2 (REV52); emendas das ordens 024 e 025; conferencia na 026"', 1),
    ('"R1 (REV46); na ordem 025"', '"R2 (REV53); aprovada com ressalvas na ordem 025, emendada; conferencia na 026"', 1),
    ('"R1 (REV48); na ordem 025"', '"R2 (REV54); aprovada com ressalvas na ordem 025, emendada; conferencia na 026"', 1),
    ('    (C / "OHamiltonianoOcultoEOCusto.lean", "B", "gerencia", "R0 (REV49); na ordem 025"),\n',
     '    (C / "OHamiltonianoOcultoEOCusto.lean", "B", "gerencia", "R1 (REV55); reprovada na ordem 025 pelo texto, emendada; conferencia na 026"),\n'
     '    (C / "OTestemunhoDeTakesakiEmCasa.lean", "B", "gerencia", "R0 (REV50); composicao de termos selados; conferencia na 026"),\n', 1),
    ('segunda lista, de 17/11: 39 modulos', 'terceira lista, de 17/11: 40 modulos; a segunda tinha 39 modulos', 1),
    ('a ordem 025 pode mudar TEXTO: regerar depois dela', 'a ordem 026 pode mudar TEXTO: regerar depois dela', 1),
])
anc = trocar((V / "ancoras_propostas_v412_r2.py").read_text(encoding="utf-8"), [
    ('(V / "insumos" / "MANIFESTO_PEDRAS_v412_R2.json")', '(V / "insumos" / "MANIFESTO_PEDRAS_v412_R3.json")', 2),
    ('(V / "insumos" / "pedras_r2" / (nome + ".lean"))', '(V / "insumos" / "pedras_r3" / (nome + ".lean"))', 1),
    ('"OParFixaORelogio", "OHamiltonianoOcultoEOCusto", ', '"OParFixaORelogio", "OHamiltonianoOcultoEOCusto", "OTestemunhoDeTakesakiEmCasa", ', 1),
    ('out = V / "insumos" / "ANCORAS_PROPOSTAS_v412_R2.json"', 'out = V / "insumos" / "ANCORAS_PROPOSTAS_v412_R3.json"', 1),
])
for nome, txt in (("manifesto_pedras_v412_r3.py", man), ("ancoras_propostas_v412_r3.py", anc)):
    alvo = V / nome
    print(nome, len(txt.encode("utf-8")), "B", "| ja' existe" if alvo.exists() else "")
    if "--executar" in sys.argv:
        assert not alvo.exists(), "nao sobrescrevo: " + nome
        alvo.write_bytes(txt.encode("utf-8"))
print("gravado" if "--executar" in sys.argv else "ENSAIO A SECO")
