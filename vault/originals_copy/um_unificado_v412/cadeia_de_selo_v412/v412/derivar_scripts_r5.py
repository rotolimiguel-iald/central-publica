# -*- coding: utf-8 -*-
"""Gerencia c1, 17/11/2026: deriva, por trocas exatas, os scripts da QUINTA lista de pedras (a quarta mais as emendas de texto
da ordem 027): manifesto_pedras_v412_r5.py (do r4) e ancoras_propostas_v412_r5.py (do r4). Nao toca nos anteriores.
Uso: derivar_scripts_r5.py [--executar]"""
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
PLANO = {
    "manifesto_pedras_v412_r4.py": ("manifesto_pedras_v412_r5.py", [
        ('LIMPAS, R3, DEST = V / "pedras_limpas", V / "insumos" / "pedras_r3", V / "insumos" / "pedras_r4"',
         'LIMPAS, R3, DEST = V / "pedras_limpas", V / "insumos" / "pedras_r3", V / "insumos" / "pedras_r5"\nR4 = V / "insumos" / "pedras_r4"', 1),
        ('"fonte_revista_sha256": hashlib.sha256(o).hexdigest(), "codigo_identico_ao_da_fonte_revista": True,',
         '"fonte_revista_sha256": hashlib.sha256(o).hexdigest(), "codigo_identico_ao_da_fonte_revista": True,\n'
         '                  "mudou_da_quarta_lista": b != (R4 / (nome + ".lean")).read_bytes(),', 1),
        ('"nota": "quarta lista, de 17/11: os 40 modulos da terceira, com comentarios e docstrings limpos pelo metodo (so\' o que e\' verdade); codigo identico ao das fontes revistas; cada log de compilacao e\' da fonte congelada",',
         '"nota": "quinta lista, de 17/11: a quarta mais as emendas de texto pedidas pelo revisor na ordem 027 (so\' comentarios e docstrings); codigo identico ao das fontes revistas; cada log de compilacao e\' da fonte congelada",\n'
         '       "mudaram_da_quarta_lista": sorted(i["modulo"] for i in itens if i["mudou_da_quarta_lista"]),', 1),
        ('out = V / "insumos" / "MANIFESTO_PEDRAS_v412_R4.json"', 'out = V / "insumos" / "MANIFESTO_PEDRAS_v412_R5.json"', 1),
        ('"| avisos nos logs:", sum(i["avisos_no_log"] for i in itens))',
         '"| avisos nos logs:", sum(i["avisos_no_log"] for i in itens), "| mudaram da quarta:", man["mudaram_da_quarta_lista"])', 1),
    ]),
    "ancoras_propostas_v412_r4.py": ("ancoras_propostas_v412_r5.py", [
        ('(V / "insumos" / "MANIFESTO_PEDRAS_v412_R4.json")', '(V / "insumos" / "MANIFESTO_PEDRAS_v412_R5.json")', 2),
        ('(V / "insumos" / "pedras_r4" / (nome + ".lean"))', '(V / "insumos" / "pedras_r5" / (nome + ".lean"))', 1),
        ('out = V / "insumos" / "ANCORAS_PROPOSTAS_v412_R4.json"', 'out = V / "insumos" / "ANCORAS_PROPOSTAS_v412_R5.json"', 1),
    ]),
}
for origem, (alvo, trocas) in PLANO.items():
    t = (V / origem).read_text(encoding="utf-8")
    for a, b, n in trocas:
        assert t.count(a) == n, (origem, t.count(a), n, a[:70])
        t = t.replace(a, b)
    f = V / alvo
    print(alvo, len(t.encode("utf-8")), "B")
    if "--executar" in sys.argv:
        assert not f.exists(), "ja' existe: " + alvo
        f.write_bytes(t.encode("utf-8"))
print("gravado" if "--executar" in sys.argv else "ENSAIO A SECO")
