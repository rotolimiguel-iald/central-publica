# -*- coding: utf-8 -*-
"""e3_patch_6r_a.py -- ajusta o bloco (6r) (e3_bloco_6r_v412.pytxt): (c) por termos nomeados (o relatorio diz qual termo falhou); (e) as frases PLANTADAS sao as que a guarda P18 do motor recusa (as das regras R2, R3 e R5), nao as do exame dos registros de pedra. Script da cadeia."""
import os, sys
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "e3_bloco_6r_v412.pytxt")
s = open(P, "rb").read().decode("utf-8")
if "_c12 = {" in s:
    print("ja'"); sys.exit(0)
open(P + ".bak_antes_do_patch_a", "wb").write(s.encode("utf-8"))
a = s.index('U["v412_a_escada_so_fecha_com_as_bandeiras_novas_e_nenhuma_chave_antiga_muda"]'); b = s.index("# --- (d) a heranca")
s = s[:a] + open(r"C:\t\k412c\ensaio_adapt\novo_c.txt", encoding="utf-8").read() + s[b:]
old = '("tudo é teorema", "tudo derivado", "nenhuma hipótese resta", "everything is a theorem", "everything is derived", "no hypothesis remains")'
assert s.count(old) == 1
s = s.replace(old, '("a singularidade converge", "o Nome fixo", "não provou", "singularity converges", "the Name is fixed", "post-diction")   # (as da guarda P18 do motor: as regras R3, R2 e R5)')
old2 = '"ligacao": {k_: v_ for k_, v_ in _lig12.items()},'
assert s.count(old2) == 1
s = s.replace(old2, old2 + ' "escada_termos": _c12,')
open(P, "wb").write(s.encode("utf-8"))
print("ok")
