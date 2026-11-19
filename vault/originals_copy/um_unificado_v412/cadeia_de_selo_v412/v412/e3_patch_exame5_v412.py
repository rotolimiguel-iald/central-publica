# -*- coding: utf-8 -*-
"""e3_patch_exame5_v412.py -- quinta adaptacao do exame_pontos_v412.py (contrato R4; backup .bak_r1c): a lista `nao_verdes.novas` tambem le all_verified das chaves novas do core; a chave guarda_frases_v412 (resultado da travessia, sem all_verified proprio)
e' julgada pelo veredito que o exame lhe da (out["core.guarda_frases_v412"], da quarta adaptacao): vermelha se faltar resultado por registro, unidade examinada ou sobrar violacao; nunca omitida. Script da cadeia."""
import os, sys
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exame_pontos_v412.py")
s = open(P, "rb").read().decode("utf-8")
old = '"novas": [k for k in R["chaves_novas_no_core"] if isinstance(core.get(k), dict) and core[k].get("all_verified") is not True]}'
if s.count(old) != 1:
    print("ja'/nao achado", s.count(old)); sys.exit(0)
open(P + ".bak_r1c", "wb").write(s.encode("utf-8"))
new = '"novas": [k for k in R["chaves_novas_no_core"] if isinstance(core.get(k), dict) and (out.get("core." + k, {}).get("all_verified") if k == "guarda_frases_v412" else core[k].get("all_verified")) is not True]}   # (v412, R4: a travessia da guarda de frases e\' julgada pelo veredito do exame, nao por all_verified proprio)'
s = s.replace(old, new)
open(P, "wb").write(s.encode("utf-8"))
print("exame_pontos_v412.py (5) adaptado")
