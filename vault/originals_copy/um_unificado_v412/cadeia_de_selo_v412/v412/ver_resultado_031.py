# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: so' leitura. Mostra a estrutura de RESULTADOS\\031_RESULTADO.json e, por extenso, os campos pedidos.
Uso: ver_resultado_031.py [caminho.de.chaves ...]   (sem argumento: so' a arvore de chaves ate' a profundidade 3)"""
import json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
j = json.loads(Path(r"C:\IALD\TUNEL_CLAUDE_APP\RESULTADOS\031_RESULTADO.json").read_bytes())


def arvore(o, p="", d=0):
    if d > 3:
        return
    if isinstance(o, dict):
        for k, v in o.items():
            tam = len(json.dumps(v, ensure_ascii=False))
            print("  " * d + "%s  (%s, %d B)" % (k, type(v).__name__, tam))
            arvore(v, p + "." + k, d + 1)
    elif isinstance(o, list) and o and isinstance(o[0], dict):
        print("  " * d + "[%d itens; chaves do primeiro: %s]" % (len(o), list(o[0])[:12]))


if len(sys.argv) == 1:
    arvore(j)
for cam in sys.argv[1:]:
    o = j
    for k in cam.split("."):
        o = o[int(k)] if isinstance(o, list) else o[k]
    print("==", cam); print(json.dumps(o, ensure_ascii=False, indent=1))
