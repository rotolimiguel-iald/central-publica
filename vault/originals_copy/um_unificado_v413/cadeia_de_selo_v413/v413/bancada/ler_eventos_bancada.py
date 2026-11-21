# -*- coding: utf-8 -*-
"""Diagnostico da Bancada para o B(n) da v413 (20/11/2026). SO LEITURA.
Le do quadro (C:/IALD/PROGRAMA_IALD/eventos.jsonl) os eventos pedidos (seq 1617, 1686, 1687, 1689) e lista,
de seq >= 1500, os que citam a F0.6 ou a Bancada; imprime cada um com a linha do arquivo e o sha16 do elo.
Confere tambem a cadeia de hash do livro inteiro (anterior == hash do elo anterior; hash == sha256 do elo sem 'hash'),
a mesma regra de sincronizar_bancada.py R3.6 verificar_evento (l.693-707). Nada e gravado."""
import hashlib
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EV = Path("C:/IALD/PROGRAMA_IALD/eventos.jsonl")
PEDIDOS = {1617, 1686, 1687, 1689}
raw = EV.read_bytes()
print("eventos.jsonl | %d B | sha16 %s" % (len(raw), hashlib.sha256(raw).hexdigest()[:16]))


def h(e):
    return hashlib.sha256(json.dumps({k: v for k, v in e.items() if k != "hash"}, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


ant, n, quebras, ilegiveis = "0" * 64, 0, [], []
relevantes = []
for i, linha in enumerate(raw.decode("utf-8").splitlines(), 1):
    if not linha.strip():
        continue
    try:
        e = json.loads(linha)
    except ValueError as exc:
        ilegiveis.append((i, str(exc)))
        continue
    n += 1
    if e.get("anterior") != ant or e.get("hash") != h(e):
        quebras.append((i, e.get("seq")))
    ant = e.get("hash")
    s = e.get("seq")
    txt = json.dumps(e, ensure_ascii=False)
    if s in PEDIDOS or (isinstance(s, int) and s >= 1500 and ("F0.6" in txt or "ancada" in txt or "18777" in txt)):
        relevantes.append((i, e))
print("elos lidos: %d | quebras da cadeia: %s | linhas ilegiveis: %s" % (n, quebras[:5] or "nenhuma", ilegiveis[:5] or "nenhuma"))
print()
for i, e in relevantes:
    marca = "PEDIDO" if e.get("seq") in PEDIDOS else "citado"
    print("=" * 100)
    print("[%s] linha %d | seq %s | %s | tipo %s | quem %s | hash16 %s" % (marca, i, e.get("seq"), e.get("quando"), e.get("tipo"), e.get("quem"), str(e.get("hash"))[:16]))
    corpo = json.dumps(e.get("dados"), ensure_ascii=False, indent=1)
    if e.get("seq") not in PEDIDOS and len(corpo) > 1200:
        corpo = corpo[:1200] + " ...[cortado na impressao; integral no livro]"
    print(corpo)
