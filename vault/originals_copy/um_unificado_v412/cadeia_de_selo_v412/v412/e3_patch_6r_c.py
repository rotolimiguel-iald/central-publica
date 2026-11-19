# -*- coding: utf-8 -*-
"""e3_patch_6r_c.py -- (6r): os numeros de bandeiras e de entradas saem do manifesto e dos specs (o R4 trouxe 952 bandeiras e 10 entradas; o bloco tinha 903 e 8 digitados): lidos, nunca digitados; as entradas apontam para modulos do bundle e para ancoras verdadeiras. Backup .bak_r1b. Script da cadeia."""
import os, sys
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "e3_bloco_6r_v412.pytxt")
s = open(P, "rb").read().decode("utf-8")
if "n_entradas_lidas" in s:
    print("ja'"); sys.exit(0)
open(P + ".bak_r1b", "wb").write(s.encode("utf-8"))


def troca(old, new, n=1):
    global s
    assert s.count(old) == n, (old[:90], s.count(old))
    s = s.replace(old, new)


troca('== CM["n_bandeiras"] == DL.N_FLAGS == 903)', '== CM["n_bandeiras"] == DL.N_FLAGS > 0)')
troca('"os_40_modulos_no_hash_formal"', '"os_modulos_novos_no_hash_formal"')
troca('len(_ent12) == _sp_cn12["extras"]["n_entradas"] == 8 and all(', 'len(_ent12) == _sp_cn12["extras"]["n_entradas"] > 0 and {e_["modulo"] for e_ in _ent12} <= {m_.split("/")[-1][:-5] for m_ in DL.BUNDLE_RELS} and all(_kf12.get(a_["bandeira"]) is True for e_ in _ent12 for a_ in e_["ancoras"]) and all(')
troca('and _lig12["n_entradas"] == 8)', 'and _lig12["n_entradas"] > 0)   # n_entradas_lidas do spec: o numero de leis e definicoes da teoria que o registro lista, lido, nao digitado')
open(P, "wb").write(s.encode("utf-8"))
print("ok")
