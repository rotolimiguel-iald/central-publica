# -*- coding: utf-8 -*-
"""Gerencia c1, 17/11/2026: deriva, por trocas exatas sobre os scripts da primeira lista, os scripts da segunda lista de pedras da
v412 (39 modulos: os 34, com as emendas das ordens 023 e 024, e cinco candidatas novas que o operador mandou entrar em 17/11).
Grava manifesto_pedras_v412_r2.py e ancoras_propostas_v412_r2.py ao lado dos originais; nao toca nos originais. Nao sobrescreve.
Uso: derivar_scripts_r2.py [--executar]"""
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent


def trocar(t, pares):
    for a, b, n in pares:
        assert t.count(a) == n, (t.count(a), n, a[:70])
        t = t.replace(a, b)
    return t


man = trocar((V / "manifesto_pedras_v412.py").read_text(encoding="utf-8"), [
    ('DEST = V / "insumos" / "pedras"\n', 'DEST = V / "insumos" / "pedras_r2"\n', 1),
    ('out = V / "insumos" / "MANIFESTO_PEDRAS_v412.json"', 'out = V / "insumos" / "MANIFESTO_PEDRAS_v412_R2.json"', 1),
    ('"R2 (REV32); ordem 023 pendente"', '"R2 (REV32); aprovada com ressalvas na ordem 023"', 1),
    ('"R1 (REV30); ordem 023 pendente"', '"R1 (REV30); aprovada com ressalvas na ordem 023"', 1),
    ('"R1 (REV34); ordem 023 pendente"', '"R2 (REV39); residuo editorial da ordem 023 aplicado"', 1),
    ('"R1 (REV35); ordem 023 pendente"', '"R2 (REV40); residuo editorial da ordem 023 aplicado"', 1),
    ('"R1 (REV36); ordem 023 pendente"', '"R1 (REV36); aprovada com ressalvas na ordem 023"', 1),
    ('"R1 (REV31); ordem 023 pendente"', '"R2 (REV38); residuo editorial da ordem 023 aplicado"', 1),
    ('"R1 (REV33); ordem 023 pendente"),\n',
     '"R1 (REV33); aprovada com ressalvas na ordem 023"),\n'
     '    (C / "OHamiltonianoOcultoEOCusto.lean", "B", "gerencia", "R0 (REV49); na ordem 025"),\n', 1),
    ('    (C / "CopiadorEImpostor.lean", "A", "gerencia", "R9 (REV23); aprovada na ordem 022"),\n',
     '    (C / "CopiadorEImpostor.lean", "A", "gerencia", "R9 (REV23); aprovada na ordem 022"),\n'
     '    (C / "OTempoEACauda.lean", "A", "gerencia", "R2 (REV44); aprovada com ressalvas na ordem 024; emenda na ordem 025"),\n'
     '    (C / "AFitaEACauda.lean", "A", "gerencia", "R1 (REV45); aprovada com ressalvas na ordem 024; emenda na ordem 025"),\n'
     '    (C / "AMedidaEOIf.lean", "A", "gerencia", "R1 (REV46); na ordem 025"),\n'
     '    (C / "AEsperancaEOIf.lean", "A", "gerencia", "R1 (REV48); na ordem 025"),\n', 1),
    ('a ordem 023 pode mudar TEXTO (cabecalhos e docstrings) de sete fontes: regerar depois dela',
     'segunda lista, de 17/11: 39 modulos (os 34 da primeira, com as emendas das ordens 023 e 024, e cinco candidatas novas que o '
     'operador mandou entrar); a ordem 025 pode mudar TEXTO: regerar depois dela', 1),
])
anc = trocar((V / "ancoras_propostas_v412.py").read_text(encoding="utf-8"), [
    ('(V / "insumos" / "MANIFESTO_PEDRAS_v412.json")', '(V / "insumos" / "MANIFESTO_PEDRAS_v412_R2.json")', 2),
    ('(V / "insumos" / "pedras" / (nome + ".lean"))', '(V / "insumos" / "pedras_r2" / (nome + ".lean"))', 1),
    ('"OPassoEORetorno", "OHabitanteDoNome", "NomeComoCodigo", "CopiadorEImpostor"]',
     '"OPassoEORetorno", "OHabitanteDoNome", "NomeComoCodigo", "CopiadorEImpostor",\n'
     '                                    "OTempoEACauda", "AFitaEACauda", "AMedidaEOIf", "AEsperancaEOIf"]', 1),
    ('"BoostEDissipador", "OParFixaORelogio", ', '"BoostEDissipador", "OParFixaORelogio", "OHamiltonianoOcultoEOCusto", ', 1),
    ('out = V / "insumos" / "ANCORAS_PROPOSTAS_v412.json"', 'out = V / "insumos" / "ANCORAS_PROPOSTAS_v412_R2.json"', 1),
])
for nome, txt in (("manifesto_pedras_v412_r2.py", man), ("ancoras_propostas_v412_r2.py", anc)):
    alvo = V / nome
    print(nome, len(txt.encode("utf-8")), "B", "| ja' existe" if alvo.exists() else "")
    if "--executar" in sys.argv:
        assert not alvo.exists(), "nao sobrescrevo: " + nome
        alvo.write_bytes(txt.encode("utf-8"))
print("gravado" if "--executar" in sys.argv else "ENSAIO A SECO")
