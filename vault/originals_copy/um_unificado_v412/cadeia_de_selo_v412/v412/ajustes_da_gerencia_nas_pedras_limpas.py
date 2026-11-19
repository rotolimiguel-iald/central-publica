# -*- coding: utf-8 -*-
"""Gerencia c1, 17/11/2026: dois ajustes de TEXTO da gerencia sobre a limpeza feita pelo agente (pedras_limpas), por troca exata:
(1) BoostEDissipador: volta o estatuto 'citado de memoria', que a limpeza tirou por engano (e' estatuto, nao historia);
(2) OPassoEORetorno: sai o residuo de processo 'melhoria que fica anotada'.
Backup de bytes ao lado; nao toca em codigo. Uso: ajustes_da_gerencia_nas_pedras_limpas.py [--executar]"""
import sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
P = Path(__file__).resolve().parent / "pedras_limpas"
TROCAS = [
    ("BoostEDissipador.lean", "[KNOWN; a conferir na fonte]", "[KNOWN; citado de memória, a conferir na fonte]"),
    ("OPassoEORetorno.lean", "Trocar a indução por uma especialização do lema do\nkernel é melhoria que fica anotada.",
     "A prova daqui é por indução; não usa a\nespecialização do lema do kernel."),
]
for nome, a, b in TROCAS:
    f = P / nome
    bruto = f.read_bytes()
    crlf = b"\r\n" in bruto
    t = bruto.decode("utf-8").replace("\r\n", "\n")
    assert t.count(a) == 1, (nome, t.count(a))
    novo = t.replace(a, b)
    dados = (novo.replace("\n", "\r\n") if crlf else novo).encode("utf-8")
    print(nome, len(bruto), "->", len(dados), "B")
    if "--executar" in sys.argv:
        bak = f.with_name(f.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")); bak.write_bytes(bruto)
        tmp = f.with_name(f.name + ".tmp_c1"); tmp.write_bytes(dados); tmp.replace(f)
print("gravado" if "--executar" in sys.argv else "ENSAIO A SECO")
